#!/usr/bin/env python3
"""Batería F1-IMPL (4.15): motor A con el perímetro F1, guardas V-F1a…m y F1-*, comprobación K3 e integración.

Uso (desde personaje_v2/): python3 -B pruebas/test_motor_a_f1.py
Sin LibreOffice: los libros sintéticos se escriben con valores (openpyxl) y la capa F1 solo lee valores. Con el libro real de Elis
(d2593777…, materializado desde la Release base-4.14) comprueba E9 (T1–T3b) y T16; si no está, esas pruebas FALLAN (no se saltan).
Grupos: SIN (T5, T6, T7), G (T8: cada guarda salta cuando debe y no cuando no debe), K3, T4, T9, T10, T11, T15 (mecanismos de
correspondencia de caja), AH (NIIF 16 con arrendamientos pesados tipo Ahold, sintético), US (US GAAP: límite declarado),
ELIS (libro real), CLI (códigos de salida y archivos) y PIPE (el gancho del pipeline, comprobación textual y exigencia).
"""
import copy
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
import motor_a_f1 as M  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


COLS = "CDEFGHIJKL"
ANIOS = list(range(2016, 2026))
REG = {"fecha": "2026-11-17", "persona": "prueba sintética", "motivo": "caso de prueba"}


def libro(ventas, ebit, da, tau, capex, adq, dwc, princ, C70, C49, n=3, pal=None, l4="IFRS (adoptadas por la Unión Europea)", c179=0.05,
          saltos=(0.0047, 0.0068, 0.0241), c48=0.0, int16=0.0, fila35=None):
    """Libro sintético V6.3 (solo valores). Las anclas se calculan aquí con las fórmulas de la plantilla (Historia C52, C53, C58),
    escritas de forma independiente de motor_a_f1 (en coma flotante)."""
    L = {"sha256": "sintetico", "Diagnóstico V6!C5": "A", "Control maestro!L4": l4, "Diagnóstico V6!C179": c179}
    for i, (c, y) in enumerate(zip(COLS, ANIOS)):
        for fila, serie in ((5, ANIOS), (6, ventas), (7, ebit), (8, da), (10, tau), (12, capex), (13, adq), (14, dwc), (17, princ)):
            L[f"Historia!{c}{fila}"] = serie[i]
    w = range(10 - n, 10)
    S = sum(ventas[i] for i in w) / n
    nop = sum(ebit[i] * (1 - tau[i]) for i in w) / n
    rei = sum(capex[i] - da[i] + dwc[i] for i in w) / n
    L["Historia!C58"] = ((nop - rei) - C70) / S
    L["Historia!C57"] = n
    L["Historia!C70"] = C70
    L["Historia!C44"] = ventas[-1]
    L["Historia!C48"] = ebit[-1] / ventas[-1]
    L["Historia!C52"] = sum(tau[5:]) / 5
    den = sum(capex[i] - da[i] + dwc[i] + adq[i] for i in range(5, 10))
    L["Historia!C53"] = (ventas[-1] - ventas[4]) / den if den > 0 else ""
    # FCF base y su segunda vía (fila 35 = CFO − capex − intereses en financiación − principal − SBC), coherentes por construcción:
    # C52 = C46 − C47 − C48 − C49 − C50; la fila 11 (CFO) se escribe para que la media de la ventana dé C46
    w5 = range(10 - n, 10)
    C47 = sum(capex[i] for i in w5) / n
    for i, c in enumerate(COLS):
        L[f"Historia!{c}11"] = C70 + capex[i] + c48 + C49
        L[f"Historia!{c}16"], L[f"Historia!{c}18"] = int16, 0.0
        L[f"Historia!{c}35"] = (L[f"Historia!{c}11"] - capex[i] - int16 - princ[i] - 0.0) if fila35 is None else fila35[i]
    L["Análisis!C46"] = sum(L[f"Historia!{COLS[i]}11"] for i in w5) / n
    L["Análisis!C47"], L["Análisis!C48"], L["Análisis!C49"], L["Análisis!C50"], L["Análisis!C51"], L["Análisis!C52"] = C47, c48, C49, 0.0, "Sí", C70
    pal = pal or {"B": (0.02, 0.10, 1.0, 0.01, 0.08), "C": (0.03, 0.10, 1.2, 0.02, 0.10), "D": (0.04, 0.11, 1.5, 0.025, 0.12)}
    for c, (g15, mo, s2c, gi, roic) in pal.items():
        L[f"Palancas!{c}14"], L[f"Palancas!{c}15"], L[f"Palancas!{c}16"], L[f"Palancas!{c}18"], L[f"Análisis!{c}68"] = g15, mo, s2c, roic, gi
    for c, s in zip("BCD", saltos):
        L[f"Diagnóstico V6!{c}178"] = s
        L[f"Diagnóstico V6!{c}176"] = s + 0.1
        L[f"Diagnóstico V6!{c}177"] = 0.1
    return L


def serie(vals, signo=-1, trat="publicado entre paréntesis"):
    return {str(y): {"valor_fuente": -v if signo == -1 else v, "signo": signo, "tratamiento": trat if signo == -1 else "ninguno",
                     "documento": "sintético", "pagina": 1} for y, v in vals.items()}


def decl(per="A0_total", rou=None, ppa=None, norma="NIIF", margen="EBIT_NIIF16_PPA_constante", pal=None, roic=None, compras="sin_compras",
         trans=False, conc=None, **extra):
    d = {"norma_contable": {"valor": norma, "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
         "perimetro_margen": {"valor": margen, "registro": REG}, "perimetro_palancas_s2c": {"valor": pal or per, "registro": REG},
         "perimetro_roic": {"valor": roic or pal or per, "registro": REG}, "clasificacion_compras": {"valor": compras, "registro": REG},
         "transicion": {"conocida": trans, "tratamiento": None, "registro": REG}, "series": {}}
    if conc:
        d["conciliacion_fcf_base"] = conc
    if rou is not None:
        d["series"]["da_rou"] = serie(rou)
    if ppa is not None:
        d["series"]["da_ppa"] = serie(ppa)
    d.update(extra)
    return d


def todos(v):
    return {y: v for y in ANIOS}


def g(r, gid):
    gs = [x for x in r["guardas"] if x["id"] == gid]
    return any(x["salta"] for x in gs), gs


def salta(r, gid):
    return g(r, gid)[0]


def bloquea(r, gid):
    return any(x["salta"] and x["severidad"] == "BLOQUEA" for x in g(r, gid)[1])


# ------------------------------------------------------------------ caso estacionario (T5/T6): τ = 0, sin crecimiento
def estacionario(rou=10, ppa=0, C49=None, pagos_int=2):
    """EBITDA 100 sobre ventas 1000; capex propio = D&A propia = 20; ROU `rou`; pagos = rou + interés; PPA `ppa` sin reposición.
    FCF verdadero = 100 − 20 − pagos = 68 (con rou 10). C48 lleva el interés y C49 el principal."""
    V = [1000.0] * 10
    da = 20 + rou + ppa
    ebit = 100 - da
    pagos = rou + (pagos_int if rou else 0)
    fcf = 100 - 20 - pagos
    L = libro(V, [float(ebit)] * 10, [float(da)] * 10, [0.0] * 10, [20.0] * 10, [0.0] * 10, [0.0] * 10, [float(rou)] * 10, float(fcf),
              float(rou if C49 is None else C49), c48=float(pagos - rou))
    return L, fcf


def F0(r, p):
    return r["diagnostico_por_perimetro"][p]["flujo_sin_crecimiento"]


# ================================================================== SIN · T5, T6, T7
L5, verdadero = estacionario(10, 0)
r5 = M.evaluar(L5, decl("A1_sin_ROU", rou=todos(10), ppa=todos(0)))
paso("T5 · solo arrendamientos: FCF verdadero 68; A1 y A2 dan 68; A0 da 58", verdadero == 68 and abs(F0(r5, "A1_sin_ROU") - 68) < 1e-9
     and abs(F0(r5, "A2_propio") - 68) < 1e-9 and abs(F0(r5, "A0_total") - 58) < 1e-9,
     f"A0 {F0(r5, 'A0_total')} · A1 {F0(r5, 'A1_sin_ROU')} · A2 {F0(r5, 'A2_propio')}")
L6, v6 = estacionario(10, 5)
CONC_T = [{"componente": "C48", "importe": -2, "partida": "interés de caja de los arrendamientos dentro de C48 (no está en la fila 16)",
           "fuente": {"documento": "sintético", "pagina": 1}}]
r6 = M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), conc=CONC_T))
paso("T6 · con PPA 5 sin reposición: A2 = 68, A1 = 63, A0 = 53", abs(F0(r6, "A2_propio") - 68) < 1e-9 and abs(F0(r6, "A1_sin_ROU") - 63) < 1e-9
     and abs(F0(r6, "A0_total") - 53) < 1e-9, f"A0 {F0(r6, 'A0_total')} · A1 {F0(r6, 'A1_sin_ROU')} · A2 {F0(r6, 'A2_propio')}")
L7, v7 = estacionario(0, 0, C49=0)
r7 = M.evaluar(L7, decl("A0_total", rou=todos(0), ppa=todos(0)))
iguales = len({round(r7["diagnostico_por_perimetro"][p]["f"], 15) for p in ("A0_total", "A1_sin_ROU", "A2_propio")}) == 1
paso("T7 · sin NIIF 16 ni PPA: A0 = A1 = A2 = la V6.3 (f del libro) y A0 admisible: ninguna guarda bloquea; utilizable",
     iguales and r7["utilizable_para_conclusion"] and abs(r7["diagnostico_por_perimetro"]["A0_total"]["f"] - L7["Historia!C58"]) < 1e-12,
     f"bloquean: {[x['id'] for x in r7['guardas'] if x['salta'] and x['severidad'] == 'BLOQUEA']}")

# ================================================================== G · T8, cada guarda en los dos sentidos
# V-F1a / V-F1m / V-F1b (W3: los cuatro casos de A0)
Lw = {}
for rou_pos, c49_pos in ((True, True), (False, False), (True, False), (False, True)):
    L, _ = estacionario(10 if rou_pos else 0, 0, C49=10 if c49_pos else 0)
    rr = M.evaluar(L, decl("A0_total", rou=todos(10 if rou_pos else 0), ppa=todos(0)))
    Lw[(rou_pos, c49_pos)] = rr
paso("G · W3 · ROU y C49 positivos: V-F1a bloquea (MODELO NO APLICABLE)", bloquea(Lw[(True, True)], "V-F1a") and not salta(Lw[(True, True)], "V-F1m"))
paso("G · W3 · los dos a cero: A0 admisible (ni V-F1a ni V-F1m)", not salta(Lw[(False, False)], "V-F1a") and not salta(Lw[(False, False)], "V-F1m"))
paso("G · W3 · solo ROU positiva: V-F1m (FUERA DEL DOMINIO), no V-F1a", bloquea(Lw[(True, False)], "V-F1m") and not salta(Lw[(True, False)], "V-F1a")
     and g(Lw[(True, False)], "V-F1m")[1][0]["efecto"] == "FUERA DEL DOMINIO")
paso("G · W3 · solo C49 positivo: V-F1m, no V-F1a", bloquea(Lw[(False, True)], "V-F1m") and not salta(Lw[(False, True)], "V-F1a"))
Ltiny, _ = estacionario(10, 0)
rt = M.evaluar(Ltiny, decl("A0_total", rou={**todos(0), 2025: 0.001}, ppa=todos(0)))
paso("G · V-F1a sin umbral: bloquea con cualquier importe (ROU 0,001 en un año)", bloquea(rt, "V-F1a"))
rt2 = M.evaluar(Ltiny, decl("A0_total", rou=todos(10), ppa=todos(0), umbral_v_f1a=0.005))
paso("G · umbral de V-F1a declarado: no se aplica (F1-PARAM bloquea) y V-F1a sigue bloqueando", bloquea(rt2, "F1-PARAM") and bloquea(rt2, "V-F1a"))
rb = M.evaluar(L5, decl("A1_sin_ROU", rou={y: 10 for y in ANIOS if y != 2024}, ppa=todos(0)))
paso("G · V-F1b: C49 > 0 y D&A ROU vacía en un año de la ventana → INCOMPLETO", bloquea(rb, "V-F1b") and g(rb, "V-F1b")[1][0]["efecto"] == "INCOMPLETO")
paso("G · V-F1b no salta con la ROU declarada en la ventana", not salta(r5, "V-F1b"))
L0, _ = estacionario(0, 0, C49=0)
rb2 = M.evaluar(L0, decl("A0_total", ppa=todos(0)))
paso("G · V-F1b (extensión declarada): A0 con C49 = 0 y ROU vacía no se admite (vacío ≠ 0)", bloquea(rb2, "V-F1b"))
# V-F1e
re1 = M.evaluar(L5, decl("A1_sin_ROU", rou={**todos(10), 2025: 40}, ppa=todos(0)))
paso("G · V-F1e: D&A ROU > D&A total → DATOS INVÁLIDOS", bloquea(re1, "V-F1e"))
d_e2 = decl("A1_sin_ROU", rou=todos(10), ppa=todos(0))
d_e2["series"]["da_rou"]["2025"]["tratamiento"] = "ninguno"
paso("G · V-F1e: signo −1 con el tratamiento «ninguno» (R415-SIGNO, T9)", bloquea(M.evaluar(L5, d_e2), "V-F1e"))
d_e3 = decl("A1_sin_ROU", rou=todos(10), ppa=todos(0))
d_e3["series"]["da_rou"]["2025"] = {"valor_fuente": 10, "signo": -1, "tratamiento": "x", "documento": "s", "pagina": 1}
paso("G · V-F1e / T9: magnitud positiva publicada como «(10)» sin signo coherente (signo −1 sobre +10 da −10) → rechazada", bloquea(M.evaluar(L5, d_e3), "V-F1e"))
paso("G · V-F1e no salta con invariantes y signos correctos", not salta(r5, "V-F1e"))
# F1-2i (política (2)(i))
r2i = M.evaluar(L6, decl("A1_sin_ROU", rou=todos(10), ppa=todos(5)))
paso("G · F1-2i: A1 con PPA > 0 trata la PPA como reposición, contra (2)(i) → bloquea", bloquea(r2i, "F1-2i"))
paso("G · F1-2i no salta con A2 ni con A1 y PPA = 0", not salta(r6, "F1-2i") and not salta(r5, "F1-2i"))
# V-F1h
paso("G · V-F1h: A2 con PPA decreciente → no admisible", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), margen="EBIT_NIIF16_PPA_decreciente")), "V-F1h"))
paso("G · V-F1h: margen después de arrendamientos → no admisible (N4)", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), margen="margen_despues_de_arrendamientos")), "V-F1h"))
paso("G · V-F1h no salta con A2 y PPA constante", not salta(r6, "V-F1h"))
# V-F1g, V-F1k (perímetro)
paso("G · V-F1g: palancas S2C en A0 con perímetro A2 → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), pal="A0_total", roic="A0_total")), "V-F1g"))
dg = decl("A2_propio", rou=todos(10), ppa=todos(5))
dg["perimetro_palancas_s2c"]["valor"] = None
rg = M.evaluar(L6, dg)
paso("G · V-F1g: palancas sin perímetro declarado → bloquea; V-F1k también (ROIC ≠ palancas)", bloquea(rg, "V-F1g") and bloquea(rg, "V-F1k"))
paso("G · V-F1k: ROIC en otro perímetro que las palancas → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), roic="A1_sin_ROU")), "V-F1k"))
paso("G · V-F1g y V-F1k no saltan con un solo perímetro", not salta(r6, "V-F1g") and not salta(r6, "V-F1k"))
# V-F1k numérico (W2): aviso con G8 solo si |salto| > C179, en las dos direcciones, no en la frontera
for s_, esperado, txt in ((0.06, True, "cae 6 puntos"), (-0.06, True, "sube 6 puntos"), (0.05, False, "frontera +0,05"), (-0.05, False, "frontera −0,05"),
                          (0.0501, True, "justo encima"), (0.004739, False, "Elis MALO")):
    Lk = copy.deepcopy(L6)
    Lk["Diagnóstico V6!B178"] = s_
    rk = M.evaluar(Lk, decl("A2_propio", rou=todos(10), ppa=todos(5)))
    gk = g(rk, "V-F1k (salto del terminal)")[1][0]
    paso(f"G · V-F1k numérico ({txt}): aviso {'sí' if esperado else 'no'}, nunca bloquea", gk["salta"] == esperado and (gk["severidad"] in (None, "AVISO")))
# V-F1j
paso("G · V-F1j: compras pendientes (opción A de 4b) → INCOMPLETO", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), compras="pendiente")), "V-F1j"))
Ladq = copy.deepcopy(L6)
Ladq["Historia!L13"] = 7.0
paso("G · V-F1j: «sin_compras» con adquisiciones en la Historia → DATOS INVÁLIDOS", bloquea(M.evaluar(Ladq, decl("A2_propio", rou=todos(10), ppa=todos(5))), "V-F1j"))
dj = decl("A2_propio", rou=todos(10), ppa=todos(5), compras="reposicion_con_importe")
dj["clasificacion_compras"]["proporcion_ventas"] = 0.009
paso("G · V-F1j: compras de reposición como término y también en el ancla (sin declarar que el ancla las excluye) → bloquea", bloquea(M.evaluar(L6, dj), "V-F1j"))
dj["clasificacion_compras"]["ancla_s2c_excluye_terminos"] = True
paso("G · V-F1j no salta con compras de reposición como término fuera del ancla", not salta(M.evaluar(L6, dj), "V-F1j"))
dj2 = decl("A2_propio", rou=todos(10), ppa=todos(5), compras="crecimiento_por_hipotesis")
dj2["clasificacion_compras"]["fundamento"] = "hipótesis declarada (4b, opción B)"
paso("G · V-F1j no salta con la hipótesis «crecimiento» registrada y su fundamento", not salta(M.evaluar(L6, dj2), "V-F1j"))
# V-F1i
dti = decl("A2_propio", rou=todos(10), ppa=todos(5), trans=True)
dti["transicion"]["tratamiento"] = "pendiente"
paso("G · V-F1i: transición conocida sin tratamiento (pendiente) → INCOMPLETO; nunca cero por defecto", bloquea(M.evaluar(L6, dti), "V-F1i"))
dtj = decl("A2_propio", rou=todos(10), ppa=todos(5))
dtj["transicion"] = {"conocida": None}
paso("G · V-F1i: sin declarar si hay transición → bloquea", bloquea(M.evaluar(L6, dtj), "V-F1i"))


def transicion(H, excluye=True, naturaleza="temporal", trat="termino_explicito"):
    d = decl("A2_propio", rou=todos(10), ppa=todos(5), trans=True)
    d["transicion"].update({"tratamiento": trat, "importes": {str(t): 7 for t in range(1, H + 1)}, "horizonte": H, "naturaleza": naturaleza,
                            "finalidad_documentada": "plan sintético (fuente de prueba)", "ancla_s2c_excluye_terminos": excluye})
    return d


paso("G · V-F1i: término explícito con H = 11 > 10 → bloquea (W1: no implementado)", bloquea(M.evaluar(L6, transicion(11)), "V-F1i"))
paso("G · V-F1i: término explícito y también en el ancla → bloquea", bloquea(M.evaluar(L6, transicion(5, excluye=False)), "V-F1i"))
paso("G · V-F1i: transición temporal en R → bloquea (se cobraría de más después del plan, P1a)", bloquea(M.evaluar(L6, transicion(5, trat="en_R")), "V-F1i"))
paso("G · V-F1i no salta: término explícito H = 5 con importes, finalidad y fuera del ancla", not salta(M.evaluar(L6, transicion(5)), "V-F1i"))
paso("G · V-F1i no salta sin transición conocida", not salta(r6, "V-F1i"))
# V-F1d, V-F1c (A3)


def a3(Rp, Rc=0, tr=0, completo=True, just=None, adq=None):
    d = decl("A3_estimado", rou=todos(10), ppa=todos(5), margen="EBIT_NIIF16_PPA_constante")
    re_ = {"por_anio": {str(y): {"R_propia": Rp, "R_compras": Rc, "transicion": tr} for y in ANIOS[-5:]}}
    if completo:
        re_.update({"fuente": "estimación sintética", "metodo": "m", "rango": "±2", "responsable": "r", "reposicion_clientes": "en R_propia",
                    "transicion": "sin transición", "incluye_gasto_comercial": False})
    if just:
        re_["justificacion_infrainversion"] = just
    d["reinversion_estimada"] = re_
    if Rc:
        d["clasificacion_compras"] = {"valor": "reposicion_con_importe", "registro": REG}
    return d


paso("G · V-F1d: A3 sin estimación → INCOMPLETO", bloquea(M.evaluar(L6, decl("A3_estimado", rou=todos(10), ppa=todos(5))), "V-F1d"))
paso("G · V-F1d: A3 sin fuente, método, rango ni responsable → INCOMPLETO", bloquea(M.evaluar(L6, a3(20, completo=False)), "V-F1d"))
d_gc = a3(20)
d_gc["reinversion_estimada"]["incluye_gasto_comercial"] = True
paso("G · V-F1d: R que incluye el gasto comercial (P2f) → bloquea", bloquea(M.evaluar(L6, d_gc), "V-F1d"))
paso("G · V-F1d no salta con una estimación documentada", not salta(M.evaluar(L6, a3(20)), "V-F1d"))
def L6_con_adq(a):
    """El caso T6 con adquisiciones `a` cada año (FCF base sin cambios: las compras están fuera del FCF base)."""
    return libro([1000.0] * 10, [65.0] * 10, [35.0] * 10, [0.0] * 10, [20.0] * 10, [float(a)] * 10, [0.0] * 10, [10.0] * 10, 68.0, 10.0)


Lc = L6_con_adq(14)
rc1 = M.evaluar(Lc, a3(20, 9))
paso("G · V-F1c no salta con R = 20 + 9 (compras de cartera), capex propio 20 y compras 14", not salta(rc1, "V-F1c"))
rc2 = M.evaluar(Lc, a3(25))
paso("G · V-F1c salta con R_propia 25 frente a capex propio 20; sin justificación BLOQUEA", bloquea(rc2, "V-F1c"))
rc3 = M.evaluar(Lc, a3(25, just="infrainversión documentada (sintética)"))
paso("G · V-F1c con justificación: AVISO, no bloquea", salta(rc3, "V-F1c") and not bloquea(rc3, "V-F1c"))
Lc5 = L6_con_adq(5)
paso("G · V-F1c salta con R_compras 9 frente a compras 5", salta(M.evaluar(Lc5, a3(20, 9)), "V-F1c"))
# V-F1f (INFORMA)
paso("G · V-F1f informa con A2 y PPA > 0 (no bloquea)", salta(r6, "V-F1f") and not bloquea(r6, "V-F1f"))
paso("G · V-F1f no informa con A0", not salta(Lw[(False, False)], "V-F1f"))
# V-F1l
n1_ok = {"ajustes": [{"regla": "N1", "anio": 2025, "partida": "ajuste de earnout", "importe": -5, "fuente": {"documento": "s", "pagina": 1},
                      "regla_fiscal": "no_deducible", "ubicacion_caja": "adquisiciones, fuera del FCF base"}],
         "bai": {"2025": {"valor": 50, "documento": "s"}}, "gasto_impuesto": {"2025": {"valor": 0, "documento": "s"}},
         "margen_objetivo_sin_ajustes": True, "actualizacion_financiera_earnout_declarada": False}
rl0 = M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=n1_ok))
paso("G · V-F1l no salta con un ajuste N1 completo (fuente, regla fiscal, caja, BAI y gasto); F1-PARAM sí (alcance de N1 sin decidir: no se elige por omisión, H9)",
     not salta(rl0, "V-F1l") and bloquea(rl0, "F1-PARAM"))
n2 = copy.deepcopy(n1_ok)
n2["ajustes"][0]["regla"] = "N2"
paso("G · V-F1l: regla N2 (pendiente) → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=n2)), "V-F1l"))
nd = copy.deepcopy(n1_ok)
nd["deducir_diagnostico_partidas_puntuales"] = True
paso("G · V-F1l: deducir el diagnóstico de partidas puntuales → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=nd)), "V-F1l"))
nsf = copy.deepcopy(n1_ok)
del nsf["ajustes"][0]["ubicacion_caja"]
paso("G · V-F1l: ajuste sin ubicación de su caja → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=nsf)), "V-F1l"))
ntf = copy.deepcopy(n1_ok)
ntf["ajustes"][0]["regla_fiscal"] = "tau_fijo"
paso("G · V-F1l: N1 con tipo fijo (no es la regla aprobada) → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=ntf)), "V-F1l"))
nfu = copy.deepcopy(n1_ok)
nfu["ajustes"].append(dict(nfu["ajustes"][0], anio=2022))
nfu["bai"]["2022"], nfu["gasto_impuesto"]["2022"] = {"valor": 50, "documento": "s"}, {"valor": 0, "documento": "s"}
rfu = M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), normalizacion=nfu))
paso("G · F1-PARAM: ajuste N1 en un ejercicio del τ fuera de la ventana → alcance sin decidir: variantes calculadas y bloquea",
     bloquea(rfu, "F1-PARAM") and len(rfu.get("variantes_parametros_sin_valor") or {}) == 2)
# F1-NORMA
paso("G · F1-NORMA: norma sin declarar → bloquea", bloquea(M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5), norma=None)), "F1-NORMA"))
Lus = copy.deepcopy(L6)
Lus["Control maestro!L4"] = "US GAAP"
paso("G · F1-NORMA: NIIF declarada y el libro dice US GAAP → DATOS INVÁLIDOS", bloquea(M.evaluar(Lus, decl("A2_propio", rou=todos(10), ppa=todos(5))), "F1-NORMA"))
paso("G · F1-NORMA no salta con NIIF y libro IFRS", not salta(r6, "F1-NORMA"))
# F1-REGISTRO
dr = decl("A2_propio", rou=todos(10), ppa=todos(5))
dr["perimetro_reinversion"]["registro"] = {"fecha": "2026-11-17", "persona": "", "motivo": "x"}
paso("G · F1-REGISTRO: perímetro sin persona → bloquea (las decisiones no las rellena el agente)", bloquea(M.evaluar(L6, dr), "F1-REGISTRO"))
paso("G · F1-REGISTRO no salta con los registros completos", not salta(r6, "F1-REGISTRO"))
# F1-REPLICA
Lr = copy.deepcopy(L6)
Lr["Historia!C58"] = Lr["Historia!C58"] + 1e-6
paso("G · F1-REPLICA: el libro no coincide con la réplica (C58 alterada) → fallo de implementación", bloquea(M.evaluar(Lr, decl("A2_propio", rou=todos(10), ppa=todos(5))), "F1-REPLICA")
     and M.evaluar(Lr, decl("A2_propio", rou=todos(10), ppa=todos(5)))["estado_propuesto"].endswith("fallo_de_implementacion"))
paso("G · F1-REPLICA no salta con el libro conforme", not salta(r6, "F1-REPLICA"))
# F1-LIBRO
paso("G · F1-LIBRO: perímetro A2 en un libro V6.3 (que calcula A0) → límite declarado, bloquea", bloquea(r6, "F1-LIBRO") and r6["estado_propuesto"] == "no_entregable · limite_del_modelo")
paso("G · F1-LIBRO no salta con A0 sin normalizar", not salta(r7, "F1-LIBRO"))
dx = decl("A0_total", rou=todos(0), ppa=todos(0))
dx["C48"] = 82.933
paso("G · T10: una declaración no puede tocar las entradas registradas (clave desconocida → bloquea)", bloquea(M.evaluar(L7, dx), "F1-DECLARACION"))

# ================================================================== K3
k3_6 = r6["diagnostico_por_perimetro"]
paso("K3 · T6: el puente cuadra en todos los perímetros", all(v["K3"]["identidad_cuadra"] for v in k3_6.values()))
paso("K3 · T6 A0: señala 10 de doble cómputo del arrendamiento y 5 de PPA como reposición no monetaria",
     abs(k3_6["A0_total"]["K3"]["doble_computo_por_clase_a_la_escala_del_año_base"]["doble_computo"] - 10) < 1e-9
     and abs(k3_6["A0_total"]["K3"]["doble_computo_por_clase_a_la_escala_del_año_base"]["reposicion_no_monetaria"] - 5) < 1e-9)
paso("K3 · T6 A2: flujo sin crecimiento = FCF base (68) y ninguna partida sin explicar", abs(k3_6["A2_propio"]["flujo_sin_crecimiento"] - 68) < 1e-9
     and not k3_6["A2_propio"]["K3"]["partidas_sin_explicar"])
paso("K3 · T6 A1: solo la PPA queda sin explicar (5)", k3_6["A1_sin_ROU"]["K3"]["partidas_sin_explicar"] == ["− amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i))"])

# ================================================================== T4 · identidad de calibración
ok4 = True
for p, v in k3_6.items():
    S = 1000
    ok4 &= abs(v["f"] * S - (v["nopat_medio"] - v["reinversion_media"] - L6["Historia!C70"])) < 1e-9
paso("T4 · f·ventas medias = NOPAT medio − reinversión media − FCF base en todos los perímetros", ok4)

# ================================================================== T11 · motor B
LB = copy.deepcopy(L6)
LB["Diagnóstico V6!C5"] = "B"
rB = M.evaluar(LB, decl("A2_propio"))
paso("T11 · motor B: F1 no aplica (sin guardas, sin bloqueo)", rB["aplica"] is False and not rB["bloquea"])

# ================================================================== T15 · correspondencia de caja (mecanismos; importes ficticios)
# Ventana con crecimiento: ventas 1000·1,05^t; margen 10 %; τ 25 %; capex propio = D&A propia + 0,5·ΔV (crecimiento); ROU 3 % de ventas
V = [1000 * 1.05 ** i for i in range(10)]
rouv = [0.03 * v for v in V]
dao = [0.02 * v for v in V]
capex = [dao[i] + 0.5 * (V[i] - (V[i - 1] if i else V[0] / 1.05)) for i in range(10)]
ebit = [0.10 * v for v in V]
fcf_y = [ebit[i] * 0.75 + dao[i] + rouv[i] - capex[i] - rouv[i] - 0.004 * V[i] for i in range(10)]   # pagos = ROU + interés 0,4 %
C70 = sum(fcf_y[-3:]) / 3
L15 = libro(V, ebit, [dao[i] + rouv[i] for i in range(10)], [0.25] * 10, capex, [0.0] * 10, [0.0] * 10, rouv, C70, sum(rouv[-3:]) / 3)
r15 = M.evaluar(L15, decl("A2_propio", rou={y: rouv[i] for i, y in enumerate(ANIOS)}, ppa=todos(0)))
d15 = r15["diagnostico_por_perimetro"]
# caja sostenible a crecimiento cero en el año base: EBIT(1−τ) − interés del arrendamiento (lo que f debe contener) = 0,075·V0 − 0,004·V0
caja0 = (0.075 - 0.004) * V[-1]
paso("T15 · arrendamiento una vez con crecimiento en la ventana: A2 (= A1 sin PPA) da la caja sostenible a crecimiento cero",
     abs(d15["A2_propio"]["flujo_sin_crecimiento"] - caja0) < 1e-6, f"{d15['A2_propio']['flujo_sin_crecimiento']:.6f} frente a {caja0:.6f}")
paso("T15 · A0 con crecimiento: cobra de más la ROU del año base (P4d) también a crecimiento cero",
     abs((d15["A2_propio"]["flujo_sin_crecimiento"] - d15["A0_total"]["flujo_sin_crecimiento"]) - sum(rouv[-3:]) / sum(V[-3:]) * V[-1]) < 1e-6)
paso("T15 · ancla E4 con el perímetro: S2C de A2 = ΔV ÷ inversión de crecimiento propia = 2,0", abs(d15["A2_propio"]["ancla_s2c_E4"] - 2.0) < 1e-9,
     f"{d15['A2_propio']['ancla_s2c_E4']}")
# P1b · transición temporal como término explícito: X_t = 7 en los años 1–5, y X^v fuera del ancla
dP1b = transicion(5)
rP1b = M.evaluar(L6, dP1b)
base_sin = M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5)))
fl_con = rP1b["calculo_perimetro_declarado"]["escenarios"]["NORMAL"]
fl_sin = base_sin["calculo_perimetro_declarado"]["escenarios"]["NORMAL"]
dif = [a - b for a, b in zip(fl_con["anios_1_10"] + [fl_con["anio_11"]], fl_sin["anios_1_10"] + [fl_sin["anio_11"]])]
paso("T15 · P1b: el término explícito cobra 7 en los años 1–5 y nada en los años 6–10 ni en el año 11", all(abs(x + 7) < 1e-9 for x in dif[:5])
     and all(abs(x) < 1e-9 for x in dif[5:]), str([round(x, 6) for x in dif]))
# P2d / V2g · compras de reposición proporcionales como término explícito: X_t = a·V_t, también en el año 11
dP2d = decl("A2_propio", rou=todos(10), ppa=todos(5), compras="reposicion_con_importe")
dP2d["clasificacion_compras"].update({"proporcion_ventas": 0.009, "ancla_s2c_excluye_terminos": True})
rP2d = M.evaluar(L6, dP2d)
c2 = rP2d["calculo_perimetro_declarado"]["escenarios"]["NORMAL"]
mo = M.motor(Fr(1000), Fr(65, 1000), Fr(0), Fr(str(rP2d["calculo_perimetro_declarado"]["f"])), g15=Fr("0.03"), m_obj=Fr("0.10"), s2c=Fr("1.2"),
             g_inf=Fr("0.02"), roic=Fr("0.10"))
V11 = mo["V"][-1] * Fr("1.02")
paso("T15 · P2d: compras de reposición proporcionales: X_t = a·V_t en los años 1–10 y a·V₁₁ en el año 11",
     all(abs((float(mo["flujos"][t]) - 0.009 * float(mo["V"][t])) - c2["anios_1_10"][t]) < 1e-9 for t in range(10))
     and abs(float(mo["flujo_11"] - Fr("0.009") * V11) - c2["anio_11"]) < 1e-9)
# P2b / V2h · compras de reposición dentro de R (A3): f las cobra a perpetuidad
rP2b = M.evaluar(Lc, a3(20, 9))
paso("T15 · P2b: compras de reposición en R (A3): f sube en R_compras ÷ ventas medias frente a R = 20",
     abs((rP2b["calculo_perimetro_declarado"]["f"] - M.evaluar(Lc, a3(20))["calculo_perimetro_declarado"]["f"]) - 9 / 1000) < 1e-12)
# P2g · PPA constante como proporción de las ventas: A2 la devuelve entera y el flujo sin crecimiento es la caja (68)
paso("T15 · P2g: PPA como proporción constante (A2) → flujo sin crecimiento = caja (68)", abs(F0(r6, "A2_propio") - 68) < 1e-9)
# P4a/P4f · la senda del motor coincide con motor() sin términos (es el motor A del libro)
paso("T15 · P4f: sin términos explícitos, la capa F1 es el motor A del libro (réplica conforme en el caso sintético)", not salta(r6, "F1-REPLICA"))

# ================================================================== AH · NIIF 16 con arrendamientos pesados (tipo Ahold, sintético)
# ventas 90.000; EBIT 3.500; τ 25 %; D&A propia 1.700 = capex; ROU 1.450 = principal; interés de arrendamientos 494 (pagos 1.944);
# PPA 50; intereses financieros 150. FCF base = CFO − capex − intereses − principal = 2.192 (orden de los ~2.000 de Ahold)
Vah, EB, DO, RO, PP, IL, IF = 90000.0, 3500.0, 1700.0, 1450.0, 50.0, 494.0, 150.0
tax = 0.25 * (EB - IL - IF)
fcf_ah = (EB + DO + RO + PP - tax) - DO - (IF + IL) - RO
Lah = libro([Vah] * 10, [EB] * 10, [DO + RO + PP] * 10, [tax / (EB - IL - IF)] * 10, [DO] * 10, [0.0] * 10, [0.0] * 10, [RO] * 10, fcf_ah, RO,
           c48=IL + IF, int16=IF)
CONC_AH = [{"componente": "C48", "importe": -IL, "partida": "interés de caja de los arrendamientos dentro de C48 (no está en la fila 16)", "fuente": {"documento": "sintético", "pagina": 1}}]
rah = M.evaluar(Lah, decl("A2_propio", rou=todos(RO), ppa=todos(PP), conc=CONC_AH))
dah = rah["diagnostico_por_perimetro"]
paso("AH · pagos 1.944 frente a FCF base 2.192: A2 reproduce la caja sostenible; A0 la infravalora en ROU + PPA (1.500, el 68 % del FCF)",
     abs(dah["A2_propio"]["flujo_sin_crecimiento"] - fcf_ah) < 1e-6 and abs(fcf_ah - dah["A0_total"]["flujo_sin_crecimiento"] - (RO + PP)) < 1e-6,
     f"FCF {fcf_ah:.1f} · A0 {dah['A0_total']['flujo_sin_crecimiento']:.1f} · A1 {dah['A1_sin_ROU']['flujo_sin_crecimiento']:.1f} · A2 {dah['A2_propio']['flujo_sin_crecimiento']:.1f}")
rah0 = M.evaluar(Lah, decl("A0_total", rou=todos(RO), ppa=todos(PP)))
paso("AH · con A0 bloquean V-F1a y F1-2i; K3 señala 1.450 de doble cómputo y 50 de PPA", bloquea(rah0, "V-F1a") and bloquea(rah0, "F1-2i")
     and abs(rah0["calculo_perimetro_declarado"]["K3"]["doble_computo_por_clase_a_la_escala_del_año_base"]["doble_computo"] - RO) < 1e-6)
paso("AH · con A2 y todo declarado solo bloquea F1-LIBRO (el libro V6.3 calcula A0): límite declarado, no un resultado silencioso",
     sorted({x["id"] for x in rah["guardas"] if x["salta"] and x["severidad"] == "BLOQUEA"}) == ["F1-LIBRO"])

# ================================================================== US · US GAAP (ASC 842): límite declarado, demostrado
# Arrendamiento operativo: coste lineal 12 (= amortización 10 + interés 2) en el EBIT; pagos 12 en el CFO; sin principal en financiación.
# La fila 8 (D&A del estado de flujos) incluye la amortización no monetaria del derecho de uso (10). FCF verdadero = 100 − 12 − 20 = 68.
#   US1: la variación del pasivo por arrendamiento (−10) NO está en la fila 14 → el perímetro correcto es A1 (excluir 10 de D_X);
#   US2: la variación SÍ está en la fila 14 (+10, consume caja) → el perímetro correcto es A0.
# Las mismas entradas F1 (D&A ROU 10, C49 = 0) piden perímetros distintos según una clasificación que F1 no tiene: no se puede dar una regla.
us = {}
for nombre, dwc in (("US1", 0.0), ("US2", 10.0)):
    Lu = libro([1000.0] * 10, [68.0] * 10, [30.0] * 10, [0.0] * 10, [20.0] * 10, [0.0] * 10, [dwc] * 10, [0.0] * 10, 68.0, 0.0, l4="US GAAP")
    ru = M.evaluar(Lu, decl("A1_sin_ROU", rou=todos(10), ppa=todos(0), norma="US_GAAP"))
    us[nombre] = ru
correcto_US1 = abs(F0(us["US1"], "A1_sin_ROU") - 68) < 1e-9 and abs(F0(us["US1"], "A0_total") - 58) < 1e-9
correcto_US2 = abs(F0(us["US2"], "A0_total") - 68) < 1e-9 and abs(F0(us["US2"], "A1_sin_ROU") - 78) < 1e-9
paso("US · demostración: con las mismas entradas F1, US1 exige A1 y US2 exige A0 (la fila 14 decide y F1 no la clasifica)", correcto_US1 and correcto_US2,
     f"US1 A0 {F0(us['US1'], 'A0_total')} A1 {F0(us['US1'], 'A1_sin_ROU')} · US2 A0 {F0(us['US2'], 'A0_total')} A1 {F0(us['US2'], 'A1_sin_ROU')}")
paso("US · por eso US GAAP bloquea con un mensaje de límite declarado (F1-NORMA, MODELO NO APLICABLE), nunca un resultado silencioso",
     all(bloquea(r, "F1-NORMA") and "LÍMITE DECLARADO" in g(r, "F1-NORMA")[1][0]["detalle"] for r in us.values()))

# ================================================================== ELIS · libro real (E9 T1–T3b, T16 en test de regresión aparte)
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis", "Elis_v63_evaluada.xlsx")
CIF = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "f1_impl", "datos", "elis_cifras_f1.json")
if os.path.exists(ELIS):
    import hashlib
    ok_sha = hashlib.sha256(open(ELIS, "rb").read()).hexdigest() == "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
    cif = json.load(open(CIF, encoding="utf-8"))
    LE = M.leer_libro(ELIS)
    s_ = lambda n: {int(y): -e["valor_publicado"] for y, e in cif["series"][n].items()}  # noqa: E731
    rE = M.evaluar(LE, decl("A0_total", rou=s_("da_rou"), ppa=s_("da_ppa"), compras="pendiente"))
    ref = cif["referencia_E9"]["perimetros"]
    dE = rE["diagnostico_por_perimetro"]
    okE = all(abs(dE[k]["f"] - ref[kr]["f"]) < 1e-12 and abs(dE[k]["flujo_sin_crecimiento"] - ref[kr]["flujo_sin_crecimiento"]) < 1e-9
              and abs(dE[k]["ancla_s2c_E4"] - ref[kr]["S2C_C53"]) < 1e-9 for k, kr in (("A0_total", "A0"), ("A1_sin_ROU", "A1"), ("A2_propio", "A2"), ("B_cota_capex", "B")))
    paso("ELIS · libro d2593777: réplica conforme (33 flujos) y E9 T1, T2, T3 y T3b(a) a 10⁻¹² en f y 10⁻⁹ en flujos y C53",
         ok_sha and rE["replica_del_libro"]["conforme"] and rE["replica_del_libro"]["flujos_contrastados"] == 33 and okE)
    paso("ELIS · K3: el puente cuadra en A0, A1, A2 y la cota B, con τ de proyección distinto del de la ventana (−7,965), y F1-K3 no salta",
         all(v["K3"]["identidad_cuadra"] for v in dE.values()) and not salta(rE, "F1-K3")
         and abs([ln["mm"] for ln in dE["A0_total"]["K3"]["lineas"]][2] + 7.964853) < 1e-6)
    paso("ELIS · A1 frente a A0: +139,4 en la base 2025 (139,381721)", abs(rE["diferencias_frente_a_A0_flujo_sin_crecimiento"]["A1_sin_ROU"] - 139.381721) < 1e-6)
    paso("ELIS · el libro tal cual (A0) dispara V-F1a y el resultado no se usa para una conclusión", bloquea(rE, "V-F1a") and not rE["utilizable_para_conclusion"])
    # T16: N1 en A0 con la convención registrada del τ de cinco años (E8.1) y las cifras verificadas del frente E
    src = lambda e: {"documento": e["documento"], "pagina": e["pagina"]}  # noqa: E731
    n1 = {"ajustes": [{"regla": "N1", "anio": int(y), "partida": "ajuste de earnout", "importe": e["valor_publicado"], "fuente": src(e),
                       "regla_fiscal": "no_deducible", "ubicacion_caja": "adquisiciones (inversión), fuera del FCF base"}
                      for y, e in cif["series"]["ajuste_earnout"].items() if int(y) >= 2023],
          "bai": {y: dict(src(e), valor=e["valor_publicado"]) for y, e in cif["series"]["bai"].items()},
          "gasto_impuesto": {y: dict(src(e), valor=-e["valor_publicado"]) for y, e in cif["series"]["gasto_impuesto"].items()},
          "margen_objetivo_sin_ajustes": True, "actualizacion_financiera_earnout_declarada": False}
    rN = M.evaluar(LE, decl("A0_total", rou=s_("da_rou"), ppa=s_("da_ppa"), compras="pendiente", normalizacion=n1))
    cN = rN["calculo_perimetro_declarado"]
    t16 = cif["referencia_T16"]["N1"]
    paso("ELIS · T16: N1 (−48,9 / +8,7 / −0,2) sin efecto fiscal: τ 0,2619/0,2806/0,2559, τ5 0,28234, f 0,044900433, flujo 236,891 (−11,605), año 11 NORMAL −18,609",
         [round(cN["tau_ventana"][y], 4) for y in ("2023", "2024", "2025")] == t16["tau_2023_25"] and abs(cN["tau_proyeccion"] - 0.28234) < 1e-12
         and abs(cN["f"] - t16["f_A0"]) < 1e-9 and abs(cN["flujo_sin_crecimiento"] - dE["A0_total"]["flujo_sin_crecimiento"] - t16["variacion_flujo_sin_crecimiento"]) < 1e-3
         and abs(cN["escenarios"]["NORMAL"]["anio_11"] - dE["A0_total"]["escenarios"]["NORMAL"]["anio_11"] - t16["variacion_NORMAL"]["terminal"]) < 1e-3,
         f"f {cN['f']} · flujo {cN['flujo_sin_crecimiento']}")
    paso("ELIS · T16: la variación de N1 es la misma en A0, A1 y A2 (perímetro A1 con N1 frente a A1 sin N1)",
         abs(M.evaluar(LE, decl("A1_sin_ROU", rou=s_("da_rou"), ppa=s_("da_ppa"), normalizacion=n1))["calculo_perimetro_declarado"]["flujo_sin_crecimiento"]
             - dE["A1_sin_ROU"]["flujo_sin_crecimiento"] - t16["variacion_flujo_sin_crecimiento"]) < 1e-3)
    paso("ELIS · T16 control negativo: deducir el diagnóstico 27,936 no es N1 y dispara V-F1l",
         bloquea(M.evaluar(LE, decl("A0_total", rou=s_("da_rou"), ppa=s_("da_ppa"), normalizacion=dict(n1, deducir_diagnostico_partidas_puntuales=True))), "V-F1l"))
    paso("ELIS · con N1 en A0, F1-LIBRO bloquea (el libro no normaliza) y F1-PARAM también (alcance sin decidir, H9)", bloquea(rN, "F1-LIBRO") and bloquea(rN, "F1-PARAM"))
    ctrl = cif["referencia_E9"]["desvio_anio_11_implementacion_parcial"]["A1"]["NORMAL"]
    a11 = dE["A1_sin_ROU"]["escenarios"]["NORMAL"]["anio_11"] - dE["A0_total"]["escenarios"]["NORMAL"]["anio_11"]
    paso("ELIS · T2 control negativo: el año 11 de A1 se aparta del de A0 en V₁₀(1+g)(f_A0 − f_A1) = 205,4 (NORMAL)", abs(a11 - ctrl) < 1e-3, f"{a11:.3f}")
else:
    paso("ELIS · libro real de Elis disponible (materializar la base 4.14)", False, ELIS)

# ================================================================== CLI · archivos y códigos de salida (libro sintético en .xlsx)
tmp = tempfile.mkdtemp(prefix="f1_cli_")
try:
    import openpyxl
    wb = openpyxl.Workbook()
    for h in ("Historia", "Análisis", "Palancas", "Motor", "Diagnóstico V6", "Control maestro"):
        wb.create_sheet(h)
    for k, v in L6.items():
        if "!" in k:
            h, c = k.split("!")
            wb[h][c] = v
    pl = os.path.join(tmp, "libro.xlsx")
    wb.save(pl)
    for nombre, d_, esperado in (("A2 con todo declarado (F1-LIBRO)", decl("A2_propio", rou=todos(10), ppa=todos(5), conc=CONC_T), 4),
                                 ("compras pendientes (V-F1j)", decl("A2_propio", rou=todos(10), ppa=todos(5), compras="pendiente"), 3)):
        c = os.path.join(tmp, nombre[:2])
        os.makedirs(c)
        json.dump(json.loads(json.dumps(d_)), open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
        rr = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", pl], capture_output=True, text=True)
        paso(f"CLI · {nombre}: código {esperado} y resultado .json/.md escritos", rr.returncode == esperado and os.path.exists(os.path.join(c, M.RESULTADO))
             and os.path.exists(os.path.join(c, M.RESULTADO_MD)), f"código {rr.returncode} · {rr.stdout.strip()[-120:]}")
    c = os.path.join(tmp, "roto")
    os.makedirs(c)
    open(os.path.join(c, "motor_a_f1.json"), "w").write("{roto")
    rr = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", pl], capture_output=True, text=True)
    paso("CLI · declaración ilegible: código 2, no evalúa nada (falla en cerrado)", rr.returncode == 2 and not os.path.exists(os.path.join(c, M.RESULTADO)))
    c = os.path.join(tmp, "sin")
    os.makedirs(c)
    rr = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", pl], capture_output=True, text=True)
    paso("CLI · sin declaración: todo sin declarar → bloquea con falta de datos (código 3)", rr.returncode == 3)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ================================================================== REV · correcciones de la revisión independiente (primera ronda)
# H4 · guarda simétrica de V-F1m: A1/A2/A3 con ROU > 0 y C49 cero o vacío omiten el alquiler
Lh4, _ = estacionario(10, 0, C49=0)
rh4 = M.evaluar(Lh4, decl("A1_sin_ROU", rou=todos(10), ppa=todos(0)))
paso("REV · H4: A1 con ROU > 0 y C49 = 0 → F1-M-SIM (fuera del dominio); el flujo A1 omitiría el alquiler (78 frente a la caja 68)",
     bloquea(rh4, "F1-M-SIM") and g(rh4, "F1-M-SIM")[1][0]["efecto"] == "FUERA DEL DOMINIO" and abs(F0(rh4, "A1_sin_ROU") - 80) < 1e-9 or
     (bloquea(rh4, "F1-M-SIM") and F0(rh4, "A1_sin_ROU") > F0(rh4, "A0_total")), f"A1 {F0(rh4, 'A1_sin_ROU')} · A0 {F0(rh4, 'A0_total')}")
paso("REV · H4: no salta con A1 y C49 > 0", not salta(r5, "F1-M-SIM"))
# H11 · C49 vacío y ROU = 0 con arrendamientos en la Historia
Lc49 = copy.deepcopy(L7)
Lc49["Análisis!C49"] = None
paso("REV · H11: C49 vacío → F1-C49 bloquea (vacío ≠ 0)", bloquea(M.evaluar(Lc49, decl("A0_total", rou=todos(0), ppa=todos(0))), "F1-C49"))
Lr0, _ = estacionario(0, 0, C49=0)
for c in COLS:
    Lr0[f"Historia!{c}17"] = 3.0
paso("REV · H11: ROU declarada a cero con principal en la fila 17 → F1-ROU-HISTORIA (DATOS INVÁLIDOS)", bloquea(M.evaluar(Lr0, decl("A0_total", rou=todos(0), ppa=todos(0))), "F1-ROU-HISTORIA"))
paso("REV · H11: sin conflicto cuando las filas 17 y 23 están a cero (T7)", not salta(r7, "F1-ROU-HISTORIA") and not salta(r7, "F1-C49"))
# H3 · F1-LIBRO con términos explícitos en A0
dh3 = decl("A0_total", rou=todos(0), ppa=todos(0), trans=True)
dh3["transicion"].update({"tratamiento": "termino_explicito", "importes": {str(t): 7 for t in range(1, 6)}, "horizonte": 5, "naturaleza": "temporal",
                          "finalidad_documentada": "plan sintético", "ancla_s2c_excluye_terminos": True})
rh3 = M.evaluar(L7, dh3)
paso("REV · H3: A0 sin arrendamientos con una transición como término explícito → F1-LIBRO (el libro no la cobra)", bloquea(rh3, "F1-LIBRO") and not rh3["utilizable_para_conclusion"])
dh3b = decl("A0_total", rou=todos(0), ppa=todos(0), compras="reposicion_con_importe")
dh3b["clasificacion_compras"].update({"proporcion_ventas": 0.009, "ancla_s2c_excluye_terminos": True})
paso("REV · H3: A0 con compras de reposición proporcionales como término → F1-LIBRO", bloquea(M.evaluar(L7, dh3b), "F1-LIBRO"))
L7m = copy.deepcopy(L7)
for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF"]):
    mo7 = r7["diagnostico_por_perimetro"]["A0_total"]["escenarios"]["NORMAL"]
    L7m[f"Motor!{c}7"] = (mo7["anios_1_10"] + [mo7["anio_11"]])[t] + (5.0 if t == 3 else 0.0)
r7m = M.evaluar(L7m, decl("A0_total", rou=todos(0), ppa=todos(0)))
paso("REV · H3: un flujo del Motor distinto del de la capa en A0 → F1-REPLICA y F1-LIBRO (comparación numérica)", bloquea(r7m, "F1-LIBRO") and bloquea(r7m, "F1-REPLICA"))
paso("REV · H3: A0 sin términos ni diferencias con el Motor → F1-LIBRO no salta (T7 sigue utilizable)", not salta(r7, "F1-LIBRO") and r7["utilizable_para_conclusion"])
# H5 · K3 falsable
r6s = M.evaluar(L6, decl("A2_propio", rou=todos(10), ppa=todos(5)))
paso("REV · K3a: el interés de arrendamientos en C48 sin declarar → la caja base por dos vías no cuadra (componente C48, −2)",
     bloquea(r6s, "F1-K3a") and abs(r6s["K3a_caja_base"]["componentes"]["C48"] + 2) < 1e-9)
paso("REV · K3a: con la partida declarada y su fuente → conforme", not salta(r6, "F1-K3a") and r6["K3"]["K3a_caja_base_dos_vias"] is True)
L56, _ = estacionario(10, 0)
L56 = libro([1000.0] * 10, [70.0] * 10, [30.0] * 10, [0.0] * 10, [20.0] * 10, [0.0] * 10, [0.0] * 10, [10.0] * 10, 56.0, 10.0, c48=2.0,
            fila35=[68.0 - 2.0 + 2.0] * 10)
r56 = M.evaluar(L56, decl("A1_sin_ROU", rou=todos(10), ppa=todos(0), conc=CONC_T))
# realista: C49 lleva los pagos enteros (12 = principal 10 + interés 2) y C48 también el interés: FCF base 56 frente a la caja 68
L56b = libro([1000.0] * 10, [70.0] * 10, [30.0] * 10, [0.0] * 10, [20.0] * 10, [0.0] * 10, [0.0] * 10, [10.0] * 10, 56.0, 12.0, c48=2.0)
r56b = M.evaluar(L56b, decl("A1_sin_ROU", rou=todos(10), ppa=todos(0), conc=CONC_T))
paso("REV · K3a: C49 con los pagos enteros y C48 con el interés (alquiler restado dos veces en el FCF base) → componente C49 sin explicar, bloquea",
     bloquea(r56b, "F1-K3a") and abs(r56b["K3a_caja_base"]["componentes"]["C49"] + 2) < 1e-9, str(r56b.get("K3a_caja_base")))
paso("REV · K3a (S10): FCF base que resta el alquiler dos veces (56 frente a la fila 35, 68): bloquea con DATOS INVÁLIDOS; el puente sigue cuadrando",
     bloquea(r56, "F1-K3a") and g(r56, "F1-K3a")[1][0]["efecto"] == "DATOS INVÁLIDOS" and r56["calculo_perimetro_declarado"]["K3"]["identidad_cuadra"]
     and r56["K3"]["conforme"] is False, str(r56.get("K3a_caja_base")))
paso("REV · K3b: A0 con arrendamientos → alquiler contado dos veces (bloquea)", bloquea(Lw[(True, True)], "F1-K3b") and Lw[(True, True)]["K3"]["K3b_alquiler_contado"] == "dos veces")
paso("REV · K3b: A1 con C49 = 0 → ninguna vez (bloquea)", bloquea(rh4, "F1-K3b") and rh4["K3"]["K3b_alquiler_contado"] == "ninguna vez")
paso("REV · K3b: A2 con C49 > 0 → una vez; sin arrendamientos → ninguna vez (sin arrendamientos); ninguno bloquea",
     not salta(r6, "F1-K3b") and r6["K3"]["K3b_alquiler_contado"] == "una vez" and not salta(r7, "F1-K3b"))
r6a0 = M.evaluar(L6, decl("A0_total", rou=todos(10), ppa=todos(5), conc=CONC_T))
paso("REV · K3c: A0 con reinversión media negativa (−15) y ventas estables → bloquea sin justificación", bloquea(r6a0, "F1-K3c"))
paso("REV · K3c: con justificación declarada → AVISO, no bloquea", (lambda r: salta(r, "F1-K3c") and not bloquea(r, "F1-K3c"))(
     M.evaluar(L6, decl("A0_total", rou=todos(10), ppa=todos(5), conc=CONC_T, justificacion_reinversion_negativa="infrainversión documentada (sintética)"))))
paso("REV · K3c: A2 (reinversión 0) no salta", not salta(r6, "F1-K3c"))
if os.path.exists(ELIS):
    CONC_E = [{"componente": "C48", "importe": -25.067, "partida": "interés de caja de los arrendamientos dentro de C48 (E6: 82,933 + 25,067)", "fuente": {"documento": "registro E6", "pagina": None}},
              {"componente": "C47", "importe": 10.0, "partida": "capex neto de cesiones y subvenciones (C47) frente al bruto (fila 12)", "fuente": {"documento": "URD25", "pagina": 327}}]
    rEk = M.evaluar(LE, decl("A0_total", rou=s_("da_rou"), ppa=s_("da_ppa"), compras="pendiente", conc=CONC_E))
    paso("REV · ELIS K3a: C70 307,933 frente a la fila 35 323,000; −15,067 = −25,067 (C48) + 10,0 (C47): conforme con las dos partidas declaradas",
         not salta(rEk, "F1-K3a") and abs(rEk["K3a_caja_base"]["media_fila_35"] - 323.0) < 1e-9, json.dumps(rEk["K3a_caja_base"]))
    paso("REV · ELIS K3a sin declarar las partidas → bloquea", bloquea(rE, "F1-K3a"))
    paso("REV · ELIS K3b y K3c: el libro tal cual (A0) cuenta el alquiler dos veces y su reinversión media es −81,2: bloquean",
         bloquea(rEk, "F1-K3b") and bloquea(rEk, "F1-K3c"))

# H7 (R6) · V-F1c compara R_propia MÁS la transición con el capex propio
paso("REV · H7/R6: V-F1c salta con R_propia 18 + transición 7 frente a capex propio 20 (la transición está dentro del capex)",
     salta(M.evaluar(Lc, a3(18, tr=7)), "V-F1c") and not salta(M.evaluar(Lc, a3(18, tr=0)), "V-F1c"))
# H7 (R9) · el ancla E4 resta X^v (compras de reposición cobradas como término explícito) de su denominador
d9 = decl("A2_propio", rou={y: rouv[i] for i, y in enumerate(ANIOS)}, ppa=todos(0), compras="reposicion_con_importe")
d9["clasificacion_compras"].update({"proporcion_ventas": 0.009, "ancla_s2c_excluye_terminos": True})
r9 = M.evaluar(L15, d9)
den9 = sum(capex[i] - dao[i] for i in range(5, 10)) - 0.009 * sum(V[5:10])
paso("REV · H7/R9: ancla de S2C con X^v fuera del denominador (V2g): ΔV ÷ (Σ inversión de crecimiento − Σ a·V)",
     abs(r9["calculo_perimetro_declarado"]["ancla_s2c_E4"] - (V[-1] - V[4]) / den9) < 1e-9, f"{r9['calculo_perimetro_declarado']['ancla_s2c_E4']} frente a {(V[-1] - V[4]) / den9}")

# H2 · exigencia y exenciones explícitas
tmp = tempfile.mkdtemp(prefix="f1_ex_")
try:
    e_sin = M.exigido(tmp)
    json.dump({"empresa": "Empresa X (inventada)"}, open(os.path.join(tmp, "fase1_v63.json"), "w"))
    e_sint = M.exigido(tmp, L=L6)
    ex_sint = M.exencion(tmp)
    open(os.path.join(tmp, "entrada_efectiva.json"), "w").write('{"modo": "estricta"}')
    e_sint415 = M.exigido(tmp, L=L7)
    os.remove(os.path.join(tmp, "entrada_efectiva.json"))
    os.remove(os.path.join(tmp, "fase1_v63.json"))
    e_real_arr, e_real_sin = M.exigido(tmp, L=L6), M.exigido(tmp, L=L7)
    json.dump({"entrada_efectiva": "estricta"}, open(os.path.join(tmp, "alcance_v2.json"), "w"))
    e_alc = M.exigido(tmp, L=L7)
    paso("REV · H2: F1 se exige sin libro (falla en cerrado), con arrendamientos en el libro aunque no haya archivos, con entrada_efectiva.json o con el modo en alcance_v2.json",
         e_sin and e_real_arr and e_sint415 and e_alc, f"{(e_sin, e_real_arr, e_sint415, e_alc)}")
    paso("REV · H2: no se exige en un libro sin arrendamientos de un expediente anterior, ni en la línea de base sintética (exención explícita y registrada)",
         not e_real_sin and not e_sint and "sintética" in str(ex_sint), str(ex_sint))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
EXP_ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
paso("REV · H2: los cierres históricos del motor A están exentos por la huella de su cierre_vigente.json (registro esquema/motor_a_f1_exenciones.json)",
     "cierre histórico" in str(M.exencion(EXP_ELIS)))
tmp = tempfile.mkdtemp(prefix="f1_ex2_")
try:
    open(os.path.join(tmp, "cierre_vigente.json"), "w").write('{"otro": "cierre nuevo"}')
    paso("REV · H2: un cierre nuevo (otra huella) no queda exento", M.exencion(tmp) is None)
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# H1 y H6 · vigencia, cierre y material auditado


def escribir_xlsx(L, ruta):
    import openpyxl
    wb = openpyxl.Workbook()
    for h in ("Historia", "Análisis", "Palancas", "Motor", "Diagnóstico V6", "Control maestro"):
        wb.create_sheet(h)
    for k, v in L.items():
        if "!" in k:
            h, c = k.split("!")
            wb[h][c] = v
    wb.save(ruta)


import cierre_v2 as CIE  # noqa: E402

tmp = tempfile.mkdtemp(prefix="f1_cierre_")
try:
    c = os.path.join(tmp, "EmpresaF1")
    os.makedirs(os.path.join(c, "recalc"))
    pl_ok, pl_bl = os.path.join(tmp, "ok.xlsx"), os.path.join(tmp, "bl.xlsx")
    escribir_xlsx(L7, pl_ok)
    escribir_xlsx(L6, pl_bl)
    shutil.copy(pl_ok, os.path.join(c, "EmpresaF1_v63_evaluada.xlsx"))
    open(os.path.join(c, "entrada_efectiva.json"), "w").write('{"modo": "estricta"}')
    st = {"motor": "A", "estado_pendiente": "concluido", "historial": [], "paso": 12}
    json.dump(st, open(os.path.join(c, "estado_pipeline.json"), "w"))

    def evaluar_cli(d, libro):
        json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
        return subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", libro, "--motor", "A",
                               "--libro-origen", os.path.join(c, "EmpresaF1_v63_evaluada.xlsx")], capture_output=True, text=True).returncode

    paso("REV · H1: sin evaluación F1, el cierre de un «concluido» del motor A se rechaza", "sin evaluación F1" in str(CIE.motivo_f1(c, st)))
    rc_ok = evaluar_cli(decl("A0_total", rou=todos(0), ppa=todos(0)), pl_ok)
    m_ok = CIE.motivo_f1(c, st)
    paso("REV · H1: con una evaluación F1 vigente y utilizable, el cierre no tiene objeción F1", rc_ok == 0 and m_ok is None, f"código {rc_ok} · {m_ok}")
    id0, _ = CIE.material(c, "EmpresaF1")
    d_cambiada = decl("A0_total", rou=todos(0), ppa=todos(0))
    d_cambiada["perimetro_margen"]["registro"] = dict(REG, motivo="otra")
    json.dump(d_cambiada, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    id1, h1 = CIE.material(c, "EmpresaF1")
    paso("REV · H6: la declaración y el resultado F1 están en el material auditado; cambiar la declaración cambia el material",
         "motor_a_f1.json" in CIE.MATERIAL_FIJO and "motor_a_f1_resultado.json" in CIE.MATERIAL_FIJO and id0 != id1 and "motor_a_f1_resultado.json" in h1)
    paso("REV · H1/H6: declaración cambiada tras la evaluación → no vigente → el cierre se rechaza", "cambió" in str(CIE.motivo_f1(c, st)))
    evaluar_cli(decl("A0_total", rou=todos(0), ppa=todos(0)), pl_ok)
    open(os.path.join(c, "EmpresaF1_v63_evaluada.xlsx"), "ab").write(b"\0")
    paso("REV · H1/H6: libro evaluado cambiado tras la evaluación → no vigente → el cierre se rechaza", "libro evaluado" in str(CIE.motivo_f1(c, st)))
    shutil.copy(pl_ok, os.path.join(c, "EmpresaF1_v63_evaluada.xlsx"))
    rc_bl = evaluar_cli(decl("A2_propio", rou=todos(10), ppa=todos(5), conc=CONC_T), pl_bl)
    paso("REV · H1: con F1 bloqueando (F1-LIBRO), un cierre «concluido» se rechaza", rc_bl == 4 and "concluido" in str(CIE.motivo_f1(c, st)))
    paso("REV · H1: con F1 bloqueando, un cierre «pendiente_de_datos» sí se admite (Elis)", CIE.motivo_f1(c, dict(st, estado_pendiente="pendiente_de_datos")) is None)
    paso("REV · H1: motivo_rechazo_cierre llama a la comprobación F1", "motivo_f1(carpeta, st)" in open(os.path.join(PV, "scripts", "cierre_v2.py"), encoding="utf-8").read())

    # H7 · el gancho del pipeline, ejecutado (no solo leído): Pipeline.motor_a_f1 con terminar() registrado
    import pipeline as PL
    fin = []
    P = PL.Pipeline.__new__(PL.Pipeline)
    P.c, P.E, P.st = c, "EmpresaF1", {"motor": "A", "historial": [], "paso": 7}
    P.estado_path = os.path.join(tmp, "estado_pipeline_prueba.json")
    P.terminar = lambda estado, tipo, detalle, paso_, **k: fin.append((estado, tipo, paso_))
    json.dump(decl("A2_propio", rou=todos(10), ppa=todos(5), conc=CONC_T), open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    t4 = P.motor_a_f1(pl_bl, 7)
    paso("REV · H7: el gancho termina el análisis con un bloqueo de límite (código 4) → no_entregable · limite_del_modelo", t4 is True and fin[-1][:2] == ("no_entregable", "limite_del_modelo"), str(fin[-1:]))
    json.dump(decl("A2_propio", rou=todos(10), ppa=todos(5), compras="pendiente", conc=CONC_T), open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    t3 = P.motor_a_f1(pl_bl, 7)
    paso("REV · H7: el gancho termina con falta de datos (código 3) → pendiente_de_datos", t3 is True and fin[-1][:2] == ("pendiente_de_datos", "falta_de_datos"), str(fin[-1:]))
    json.dump(decl("A0_total", rou=todos(0), ppa=todos(0)), open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    n_fin = len(fin)
    t0 = P.motor_a_f1(pl_ok, 7)
    paso("REV · H7: con F1 utilizable el gancho deja seguir y registra el resultado", t0 is False and len(fin) == n_fin and (P.st.get("motor_a_f1") or {}).get("bloquea") is False)
    P.st["motor"] = "B"
    paso("REV · H7: con el motor B el gancho no actúa", P.motor_a_f1(pl_bl, 7) is False)
finally:
    shutil.rmtree(tmp, ignore_errors=True)
src = open(os.path.join(PV, "scripts", "pipeline.py"), encoding="utf-8").read()
paso("PIPE · el pipeline evalúa F1 en el paso 7, en el paso 12 (tras verificar el libro) y comprueba su vigencia en el paso 13 antes de fijar el material",
     'self.motor_a_f1(self.p("recalc", os.path.basename(libro_ev)), 7)' in src and "self.motor_a_f1(rec, 12)" in src and "_F1.vigencia(self.c" in src
     and src.index("self.motor_a_f1(rec, 12)") > src.index('"verificar_todo.sh"'))

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} pruebas del motor A F1 (4.15) PASAN")
sys.exit(0 if n_ok == len(R) else 1)
