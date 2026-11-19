#!/usr/bin/env python3
"""Batería de la normalización declarada del circulante de la reinversión (V-CIRC, decisión (a) de la persona responsable del 19-nov-2026) en la
capa F1 (motor_a_f1.py), en la aplicación de la declaración al libro (f1_libro_v631.py) y en la plantilla V6.3.2 F1 (selección, huella de
entradas, volcado a las fases), sin LibreOffice. Lo que exige recálculo está en v6/v632_f1/scripts/probar_v632_f1.py (a0 y circ).

Uso (desde personaje_v2/): python3 -B pruebas/test_circulante_f1.py
Grupos:
  VINCI   caso tipo Vinci: los valores del libro de datos del expediente de examen (pruebas/datos_circulante/vinci_libro_v631.json; circulante
          negativo estructural excluido de la caja base, C46): sin la declaración K3c bloquea (f 4,49 %, flujo sin crecimiento 3.016); con ella, f,
          el flujo sin crecimiento y el ancla son los del cálculo independiente (1,57 %, 5.191, 2,32), K3c no salta y el libro V6.3.1 no lo calcula.
  G       la declaración: forma, cobertura de los años que usa la reinversión, fundamento, registro, norma y coherencia con la caja base (F1-CIRC);
          vacío = sin declarar; una normalización inválida no se aplica.
  CAJA    (revisión C1) la exclusión del circulante en C46 se demuestra con el cálculo declarado de C46 del expediente sintético
          (datos_circulante/expediente_tipo_vinci.py: fase1_v63.json y su texto), no con partidas: la sonda del revisor (dos partidas C46 que se
          compensan) con libros V6.3.1 y V6.3.2, cálculos amañados con y sin fuente, sin cálculo o sin carpeta (INCOMPLETO), cálculos que no son
          la media de la ventana con CFO + fila 14 o que no describen el libro.
  K3      el puente lleva la partida del circulante excluido y cuadra; K3c mide la reinversión normalizada y sigue bloqueando si es negativa.
  LIBRO   oráculo y réplica con libros V6.3, V6.3.1 y V6.3.2 sintéticos (las celdas que dependen de las entradas se recalculan aquí, en coma
          flotante, como las fórmulas de la plantilla e independientemente de la capa).
  APLICAR f1_libro_v631.celdas y aplicar sobre las plantillas V6.3.1 y V6.3.2 reales (sin recalcular).
  EE, SEL, DATOS, MD  huella y universo de entradas, selección de la plantilla, volcado a las fases e informe.
"""
import copy
import hashlib
import json
import os
import shutil
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
RAIZ = os.path.dirname(PV)
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.path.insert(0, os.path.join(AQUI, "datos_circulante"))
sys.dont_write_bytecode = True
import motor_a_f1 as M  # noqa: E402
import f1_libro_v631 as V631  # noqa: E402
import expediente_tipo_vinci as EXP  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


COLS = "CDEFGHIJKL"
ANIOS = list(range(2016, 2026))
COL = dict(zip(ANIOS, COLS))
REG = {"fecha": "2026-11-19", "persona": "prueba sintética V-CIRC", "motivo": "caso de prueba (no es una decisión)"}
FIX = json.load(open(os.path.join(AQUI, "datos_circulante", "vinci_libro_v631.json"), encoding="utf-8"))
PLANTILLA_V631 = os.path.join(RAIZ, "v6", "v631_f1", "entregables", "Plantilla_V6.3.1_F1.xlsx")
PLANTILLA_V632 = os.path.join(RAIZ, "v6", "v632_f1", "entregables", "Plantilla_V6.3.2_F1.xlsx")
ROU = {2021: 605, 2022: 623, 2023: 668, 2024: 714, 2025: 817}
PPA = {2021: 0, 2022: 128, 2023: 128, 2024: 108, 2025: 38}
FUENTE_TXT = "fuente_tipo_vinci.txt"
FUENTE = "[PDF PAGE 1]\nInforme sintético (tipo Vinci): 605 623 668 714 817 0 128 108 38\n[PDF PAGE 2]\n"
CONC = [{"componente": "C46", "importe": -2090.0, "partida": "entrada de caja del circulante excluida del CFO en C46 (media de la fila 14 de la ventana)",
         "fuente": {"documento": "informe sintético", "pagina": 1}},
        {"componente": "C46", "importe": 37.333333, "partida": "dividendos de sociedades no consolidadas sumados en C46", "fuente": {"documento": "informe sintético", "pagina": 1}},
        {"componente": "C47", "importe": -213.0, "partida": "cuentas a cobrar financieras de contratos PPP sumadas al capex", "fuente": {"documento": "informe sintético", "pagina": 1}},
        {"componente": "C47", "importe": 165.666667, "partida": "cobros por ventas de inmovilizado restados del capex", "fuente": {"documento": "informe sintético", "pagina": 1}},
        {"componente": "C50", "importe": 119.333333, "partida": "SBC de C50 frente al gasto IFRS 2 de la fila 18", "fuente": {"documento": "informe sintético", "pagina": 1}}]
NORM = {"regla": "circulante_a_cero", "anios": [2021, 2022, 2023, 2024, 2025],
        "fundamento": "prueba: la caja base (C46) excluye el circulante (como Control maestro M43 en VINCI); decisión V-CIRC (a): tampoco en la reinversión",
        "registro": REG}
CARPETA = tempfile.mkdtemp(prefix="circ_f1_")
open(os.path.join(CARPETA, FUENTE_TXT), "w", encoding="utf-8").write(FUENTE)
# (revisión C1) el expediente sintético: fase1_v63.json con el cálculo declarado de C46 (CFO + fila 14 + dividendos, con su fuente) y su texto
EXP.escribir(CARPETA, FIX["valores"])
TMP_C46 = tempfile.mkdtemp(prefix="circ_c46_")


def carpeta_con(f1=None, sin_f1=False):
    """Otra carpeta de expediente sintético: la fuente de las series, el texto conservado y fase1_v63.json (el del expediente tipo, otro, o ninguno)."""
    c = tempfile.mkdtemp(dir=TMP_C46)
    open(os.path.join(c, FUENTE_TXT), "w", encoding="utf-8").write(FUENTE)
    return EXP.escribir(c, None if sin_f1 else FIX["valores"], f1=f1)


def f1_c46(terminos=None, componentes=None, quitar_calculo=False, **cambios):
    """fase1_v63.json del expediente tipo con el cálculo declarado de C46 cambiado (términos, componentes añadidos y claves del cálculo)."""
    f = EXP.fase1(FIX["valores"])
    d = f["analisis"]["C46"]
    if quitar_calculo:
        del d["calculo"]
        return f
    cal = d["calculo"]
    if terminos is not None:
        cal["terminos"] = terminos
    cal["componentes"].update(copy.deepcopy(componentes or {}))
    for k, v in cambios.items():
        if k == "valor":
            d["valor"] = v
        else:
            cal[k] = v
    return f


def serie(vals):
    return {str(y): {"valor_fuente": v, "signo": 1, "tratamiento": "ninguno", "documento": "informe sintético", "pagina": 1, "literal": str(v),
                     "archivo": FUENTE_TXT} for y, v in vals.items()}


def decl(norm=None, per="A2_propio", norma="NIIF", conc=None, **extra):
    d = {"norma_contable": {"valor": norma, "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
         "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": per, "registro": REG},
         "perimetro_roic": {"valor": per, "registro": REG},
         "clasificacion_compras": {"valor": "crecimiento_por_hipotesis", "registro": REG, "fundamento": "prueba: las compras se tratan como crecimiento"},
         "transicion": {"conocida": False, "tratamiento": None, "registro": REG}, "series": {"da_rou": serie(ROU), "da_ppa": serie(PPA)},
         "conciliacion_fcf_base": copy.deepcopy(CONC if conc is None else conc),
         "fuentes_series": {"informe sintético": {"archivo": FUENTE_TXT, "sha256": hashlib.sha256(FUENTE.encode("utf-8")).hexdigest()}}}
    if norm is not None:
        d["normalizacion_circulante"] = copy.deepcopy(norm)
    d.update(extra)
    return d


def norm(**cambios):
    n = copy.deepcopy(NORM)
    for k, v in cambios.items():
        if v is _QUITAR:
            n.pop(k, None)
        else:
            n[k] = v
    return n


_QUITAR = object()


def h(L, fila, y):
    return L.get(f"Historia!{COL[y]}{fila}")


def _fila_h(k):
    return int("".join(ch for ch in k.split("!")[1] if ch.isdigit()))


def recalcular(L):
    """Las celdas del libro sintético que dependen de las entradas, recalculadas en coma flotante como las fórmulas de la plantilla (V6.3.1 F1 en su
    rama de D_X; V6.3.2 F1 con su normalización): fila 88 (D_X), filas 95–97 (V6.3.2), C58 (f), C76 y C53 (ancla). Independiente de motor_a_f1."""
    per = L.get("Historia!C89") or "A0_total"
    for y in ANIOS:
        da, rou, ppa = h(L, 8, y), h(L, 86, y), h(L, 87, y)
        dx = (da if per == "A0_total" else (da - rou if (da is not None and rou is not None) else None) if per == "A1_sin_ROU"
              else (da - rou - ppa if None not in (da, rou, ppa) else None) if per == "A2_propio" else None)
        L[f"Historia!{COL[y]}88"] = dx
    v632 = "NORMALIZACIÓN DEL CIRCULANTE" in str(L.get("Historia!A92") or "")
    ef = "ninguna"
    if v632:
        regla, marcas = L.get("Historia!C93"), {y: h(L, 94, y) for y in ANIOS}
        if regla in (None, "") and all(m in (None, "") for m in marcas.values()):
            ef = "ninguna"
        elif regla == "circulante_a_cero" and all(m in (None, "") or (m == 1 and not isinstance(m, (str, bool))) for m in marcas.values()):
            ef = "circulante_a_cero"
        else:
            ef = "no reconocida"
        L["Historia!C97"] = ef
        for y in ANIOS:
            w = h(L, 14, y)
            e95 = (w or 0.0) if (ef == "circulante_a_cero" and marcas[y] == 1) else 0
            L[f"Historia!{COL[y]}95"] = e95
            L[f"Historia!{COL[y]}96"] = (w - e95) if isinstance(w, (int, float)) else ""
    n = L["Historia!C57"]
    win, hl = ANIOS[-n:], ANIOS[-5:]

    def wc(y):
        v = h(L, 96, y) if v632 else h(L, 14, y)
        return v if isinstance(v, (int, float)) else 0.0

    def r30(y):
        return h(L, 12, y) - h(L, 88, y) + wc(y)
    f = None
    if ef != "no reconocida" and not (ef == "circulante_a_cero" and any(h(L, 94, y) != 1 for y in win)) and all(h(L, 88, y) is not None for y in win):
        S = sum(h(L, 6, y) for y in win) / n
        nop = sum(h(L, 7, y) * (1 - h(L, 10, y)) for y in win) / n
        rei = sum(r30(y) for y in win) / n
        f = ((nop - rei) - L["Historia!C70"]) / S
        L["Historia!C76"] = rei
    else:
        L["Historia!C76"] = None
    L["Historia!C58"] = f
    anc = None
    completo = all(isinstance(h(L, fi, y), (int, float)) for fi in (12, 13, 14, 88) for y in hl)
    if ef != "no reconocida" and completo and not (ef == "circulante_a_cero" and any(h(L, 94, y) != 1 for y in hl)):
        den = sum(r30(y) + (h(L, 13, y) or 0.0) for y in hl)
        anc = (h(L, 6, 2025) - h(L, 6, 2020)) / den if den > 0 else None
    L["Historia!C53"] = anc
    return L


def libro_vinci(v632=False, regla=None, anios_norm=(), **cambios):
    L = dict(FIX["valores"])
    L["sha256"] = "tipo_vinci"
    L.update(cambios)
    if v632:
        L["Historia!A92"] = "  NORMALIZACIÓN DEL CIRCULANTE · motor A (V6.3.2 F1): prueba"
        L["Historia!C93"] = regla
        for y in ANIOS:
            L[f"Historia!{COL[y]}94"] = 1 if y in anios_norm else None
    return recalcular(L)


def ev(L, d, carpeta=CARPETA):
    return M.evaluar(L, d, carpeta=carpeta)


def g(r, gid):
    return [x for x in r["guardas"] if x["id"] == gid]


def salta(r, gid):
    return any(x["salta"] for x in g(r, gid))


def bloquea(r, gid):
    return any(x["salta"] and x["severidad"] == "BLOQUEA" for x in g(r, gid))


def efecto(r, gid):
    return [x["efecto"] for x in g(r, gid) if x["salta"]]


def bloquean(r):
    return sorted({x["id"] for x in r["guardas"] if x["salta"] and x["severidad"] == "BLOQUEA"})


def cd(r):
    return r.get("calculo_perimetro_declarado") or {}


# ------------------------------------------------------------------------------------------------ cálculo independiente (fracciones)
def Fq(x):
    return Fr(repr(x)) if isinstance(x, float) else Fr(x)


def esperado(L, normalizado):
    """f, flujo sin crecimiento, reinversión media y ancla del perímetro A2 con el circulante de la fila 14 o normalizado a cero (sin motor_a_f1)."""
    win, hl = ANIOS[-3:], ANIOS[-5:]
    V = {y: Fq(h(L, 6, y)) for y in ANIOS}
    dx = {y: Fq(h(L, 8, y)) - ROU.get(y, 0) - PPA.get(y, 0) for y in hl}
    wc = {y: (Fr(0) if normalizado else Fq(h(L, 14, y))) for y in hl}
    S = sum(V[y] for y in win) / 3
    nop = sum(Fq(h(L, 7, y)) * (1 - Fq(h(L, 10, y))) for y in win) / 3
    rei = sum(Fq(h(L, 12, y)) - dx[y] + wc[y] for y in win) / 3
    f = (nop - rei - Fq(L["Historia!C70"])) / S
    tau5 = sum(Fq(h(L, 10, y)) for y in hl) / 5
    m0 = Fq(h(L, 7, 2025)) / V[2025]
    F0 = V[2025] * (m0 * (1 - tau5) - f)
    den = sum(Fq(h(L, 12, y)) - dx[y] + wc[y] + Fq(h(L, 13, y)) for y in hl)
    return {"f": f, "F0": F0, "reinv": rei, "ancla": (V[2025] - V[2020]) / den}


L0 = libro_vinci()
E_SIN, E_NORM = esperado(L0, False), esperado(L0, True)

# ------------------------------------------------------------------------------------------------ VINCI
r_sin = ev(L0, decl())
paso("VINCI · control: el libro sintético reproduce el de datos del expediente (f = Historia C58 = 0,0448986…, ancla C53 = 5,9595…) y la capa lo replica",
     abs(Fq(FIX["valores"]["Historia!C58"]) - E_SIN["f"]) < Fr(1, 10 ** 12) and abs(Fq(L0["Historia!C58"]) - E_SIN["f"]) < Fr(1, 10 ** 12)
     and not salta(r_sin, "F1-REPLICA"), f"f {float(E_SIN['f']):.12f} · C53 {L0['Historia!C53']}")
paso("VINCI · (control) sin la declaración (estado actual): F1-K3c BLOQUEA (reinversión media −1.514,333 con ventas al alza) y solo él; f 4,49 %, flujo sin crecimiento 3.016,07",
     bloquean(r_sin) == ["F1-K3c"] and abs(cd(r_sin)["reinversion_media"] + 1514.333333) < 1e-5 and abs(cd(r_sin)["f"] - 0.044898608760346) < 1e-12
     and abs(cd(r_sin)["flujo_sin_crecimiento"] - 3016.068605) < 1e-5, f"{bloquean(r_sin)} · F0 {cd(r_sin).get('flujo_sin_crecimiento')}")
paso("VINCI · (control) sin la declaración no hay bloque ni guarda de la normalización (nada cambia)",
     "normalizacion_circulante" not in r_sin and not g(r_sin, "F1-CIRC") and not any(ln["clase"] == "normalizacion_declarada" for ln in cd(r_sin)["K3"]["lineas"]))
r_n = ev(L0, decl(NORM))
paso("VINCI · con la normalización 2021–2025: f = cálculo independiente (NOPAT − (capex − D_X) − C70) ÷ ventas = 1,574 % (10⁻¹²)",
     abs(Fr(repr(cd(r_n)["f"])) - E_NORM["f"]) < Fr(1, 10 ** 12) and abs(cd(r_n)["f"] - 0.015744) < 1e-6, f"{cd(r_n).get('f')} · esperado {float(E_NORM['f'])}")
paso("VINCI · reinversión media normalizada = capex − D_X = +575,667; flujo sin crecimiento = 5.190,98 (≈ 5.191,0 del diagnóstico; +2.174,9)",
     abs(cd(r_n)["reinversion_media"] - 575.666667) < 1e-5 and abs(Fr(repr(cd(r_n)["flujo_sin_crecimiento"])) - E_NORM["F0"]) < Fr(1, 10 ** 6)
     and abs(cd(r_n)["flujo_sin_crecimiento"] - cd(r_sin)["flujo_sin_crecimiento"] - 2174.9) < 0.1, f"F0 {cd(r_n).get('flujo_sin_crecimiento')}")
paso("VINCI · ancla de S2C normalizada en los cinco años H–L = ΔV ÷ Σ (capex − D_X + adquisiciones) = 31.365 ÷ 13.504 = 2,3226 (10⁻⁹)",
     abs(Fr(repr(cd(r_n)["ancla_s2c_E4"])) - E_NORM["ancla"]) < Fr(1, 10 ** 9) and abs(cd(r_n)["ancla_s2c_E4"] - 31365 / 13504) < 1e-9, f"{cd(r_n).get('ancla_s2c_E4')}")
paso("VINCI · F1-K3c NO salta (mide la reinversión normalizada) y F1-CIRC no salta: cubre 2021–2025 y el cálculo declarado de C46 del expediente "
     "(fase1_v63.json: CFO + fila 14 + dividendos, con sus fuentes) excluye el circulante y es el C46 del libro",
     not salta(r_n, "F1-K3c") and g(r_n, "F1-CIRC") and not salta(r_n, "F1-CIRC") and "normalizado" in g(r_n, "F1-K3c")[0]["detalle"]
     and "cálculo declarado de C46" in g(r_n, "F1-CIRC")[0]["detalle"] and "fase1_v63.json" in g(r_n, "F1-CIRC")[0]["detalle"],
     g(r_n, "F1-CIRC")[0]["detalle"][:200])
paso("VINCI · con el libro V6.3.1 F1 la conclusión no se toma del libro: F1-LIBRO BLOQUEA como límite declarado (la salida es la V6.3.2 F1 en un expediente nuevo) y solo él",
     bloquean(r_n) == ["F1-LIBRO"] and "V6.3.2 F1" in g(r_n, "F1-LIBRO")[0]["detalle"] and r_n["estado_propuesto"] == "no_entregable · limite_del_modelo"
     and "no normaliza el circulante" in g(r_n, "F1-LIBRO")[0]["detalle"] and not salta(r_n, "F1-REPLICA"), g(r_n, "F1-LIBRO")[0]["detalle"][:160])
nc = r_n.get("normalizacion_circulante") or {}
paso("VINCI · el resultado enseña la normalización: años, lo excluido por año (= fila 14), la partida C46 de la caja base y el efecto (sin normalizar → normalizado)",
     nc.get("aplicada") is True and nc.get("anios") == NORM["anios"] and nc.get("excluido_por_anio") == {"2021": -1579.0, "2022": -392.0, "2023": -1463.0, "2024": -2311.0, "2025": -2496.0}
     and (nc.get("caja_base") or {}).get("importe") == -2090.0 and nc["efecto_en_el_perimetro_declarado"]["sin_normalizar"]["f"] == cd(r_sin)["f"]
     and nc["efecto_en_el_perimetro_declarado"]["normalizado"]["f"] == cd(r_n)["f"] and nc.get("libro") == "V6.3 o V6.3.1 F1: el libro no normaliza el circulante")
c46n = nc.get("calculo_C46") or {}
paso("VINCI · el resultado enseña el cálculo declarado de C46 que lo demuestra (años, términos, valor = C46 del libro) y, para la revisión de entradas, "
     "cada componente con su fuente, su página y su cita",
     c46n.get("demostrado") is True and c46n.get("anios") == [2023, 2024, 2025] and c46n.get("valor_calculado") == 9327.333 and c46n.get("C46_del_libro") == 9327.333
     and "circulante" in str(c46n.get("terminos")) and list((c46n.get("componentes") or {})) == ["dividendos_sociedades_no_consolidadas"]
     and abs(c46n["componentes"]["dividendos_sociedades_no_consolidadas"]["media"] - 37.333333) < 1e-6
     and any("p.2" in x and "Other 41 31" in x for x in c46n["componentes"]["dividendos_sociedades_no_consolidadas"]["fuentes"])
     and "revisión de entradas" in str(c46n.get("revision")), json.dumps(c46n, ensure_ascii=False)[:200])
paso("VINCI · (control) la fila 14 (cifra publicada) no cambia: el libro y el resultado conservan −1.463 / −2.311 / −2.496",
     [h(L0, 14, y) for y in (2023, 2024, 2025)] == [-1463, -2311, -2496] and r_n["entradas_registradas"]["Historia!C70 (FCF base que calibra f)"] == 4419.333)
paso("VINCI · los diagnósticos por perímetro usan la misma normalización (A0, A1, A2 y la cota B; la PPA y la ROU no cambian)",
     all(abs(r_n["diagnostico_por_perimetro"][p]["reinversion_media"] - r_sin["diagnostico_por_perimetro"][p]["reinversion_media"] - 2090) < 1e-6
         for p in ("A0_total", "A1_sin_ROU", "A2_propio")))
r_v = ev(libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"]), decl(NORM))
paso("VINCI · con un libro V6.3.2 F1 que lleva la normalización declarada: utilizable (ninguna guarda bloquea); F1-LIBRO dice V6.3.2 y la réplica usa el circulante del libro",
     r_v["utilizable_para_conclusion"] is True and not salta(r_v, "F1-LIBRO") and "V6.3.2 F1" in g(r_v, "F1-LIBRO")[0]["detalle"]
     and not salta(r_v, "F1-REPLICA") and (r_v["replica_del_libro"].get("normalizacion_circulante_del_libro") or {}).get("efectiva") == "circulante_a_cero",
     f"{bloquean(r_v)} · {g(r_v, 'F1-LIBRO')[0]['detalle'][:120]}")
paso("VINCI · la capa (declaración) y el libro V6.3.2 (sus filas 93–97) dan la misma f normalizada, la misma ancla y la misma reinversión",
     abs(cd(r_v)["f"] - 0.015744) < 1e-6 and abs(cd(r_v)["f"] - cd(r_n)["f"]) < 1e-15 and abs(cd(r_v)["ancla_s2c_E4"] - cd(r_n)["ancla_s2c_E4"]) < 1e-12
     and abs(r_v["replica_del_libro"]["f"] - cd(r_n)["f"]) < 1e-12)

# ------------------------------------------------------------------------------------------------ G · la declaración
r_w = ev(L0, decl(norm(anios=[2023, 2024, 2025])))
paso("G · solo la ventana (2023–2025): F1-CIRC INCOMPLETO por los años 2021–2022 del ancla; f se calcula (ventana cubierta) y el ancla no (no se mezclan)",
     efecto(r_w, "F1-CIRC") == ["INCOMPLETO"] and "[2021, 2022]" in g(r_w, "F1-CIRC")[0]["detalle"] and cd(r_w).get("ancla_s2c_E4") is None
     and abs(cd(r_w)["f"] - cd(r_n)["f"]) < 1e-15, g(r_w, "F1-CIRC")[0]["detalle"][:160])
r_v2 = ev(L0, decl(norm(anios=[2021, 2022, 2023, 2025])))
paso("G · la ventana sin 2024: f no se calcula (F1-PERIMETRO lo dice con la normalización) y F1-CIRC INCOMPLETO; sin excepción ni F1-REPLICA",
     cd(r_v2) == {} and efecto(r_v2, "F1-CIRC") == ["INCOMPLETO"] and "[2024]" in g(r_v2, "F1-CIRC")[0]["detalle"] and bloquea(r_v2, "F1-PERIMETRO")
     and "normalización" in [x for x in g(r_v2, "F1-PERIMETRO") if x["salta"]][0]["detalle"] and not salta(r_v2, "F1-REPLICA"), str(bloquean(r_v2)))
for nombre, n_, ef_, frag in (("regla distinta", norm(regla="circulante_medio"), "DATOS INVÁLIDOS", "no admitida"),
                              ("sin regla", norm(regla=_QUITAR), "INCOMPLETO", "regla sin declarar"),
                              ("años que no son una lista", norm(anios="2021-2025"), "DATOS INVÁLIDOS", "no es una lista"),
                              ("un año fuera de la Historia", norm(anios=[2015, 2021, 2022, 2023, 2024, 2025]), "DATOS INVÁLIDOS", "no está en la Historia"),
                              ("un año repetido", norm(anios=[2021, 2022, 2023, 2024, 2025, 2025]), "DATOS INVÁLIDOS", "repetido"),
                              ("un año como texto", norm(anios=[2021, 2022, "2023", 2024, 2025]), "DATOS INVÁLIDOS", "no es un año"),
                              ("una clave desconocida", norm(anyos=[2021]), "DATOS INVÁLIDOS", "claves no reconocidas"),
                              ("sin años", norm(anios=[]), "INCOMPLETO", "anios sin declarar")):
    r_ = ev(L0, decl(n_))
    paso(f"G · {nombre}: F1-CIRC {ef_} y la normalización NO se aplica (f y K3c como sin declarar)",
         efecto(r_, "F1-CIRC") == [ef_] and frag in g(r_, "F1-CIRC")[0]["detalle"] and abs(cd(r_)["f"] - cd(r_sin)["f"]) < 1e-15 and bloquea(r_, "F1-K3c")
         and (r_.get("normalizacion_circulante") or {}).get("aplicada") is False, g(r_, "F1-CIRC")[0]["detalle"][:140])
r_f = ev(L0, decl(norm(fundamento="")))
paso("G · sin fundamento: F1-CIRC INCOMPLETO (la forma es válida: el cálculo la aplica, como un perímetro declarado sin registro)",
     efecto(r_f, "F1-CIRC") == ["INCOMPLETO"] and "fundamento" in g(r_f, "F1-CIRC")[0]["detalle"] and abs(cd(r_f)["f"] - cd(r_n)["f"]) < 1e-15)
r_r = ev(L0, decl(norm(registro=_QUITAR)))
paso("G · sin registro: F1-REGISTRO INCOMPLETO (es una decisión de la persona, no la rellena el agente)",
     any(x["salta"] and "normalizacion_circulante sin registro" in x["detalle"] for x in g(r_r, "F1-REGISTRO")) and not salta(r_r, "F1-CIRC"))
conc_mal = [dict(e, importe=-2000.0) if e["importe"] == -2090.0 else e for e in CONC]
r_c = ev(L0, decl(NORM, conc=conc_mal))
paso("G · la partida C46 del circulante con otro importe (−2.000 frente a la media −2.090): F1-CIRC DATOS INVÁLIDOS (y K3a ve la caja base sin explicar)",
     efecto(r_c, "F1-CIRC") == ["DATOS INVÁLIDOS"] and "no declara que excluye el circulante" in g(r_c, "F1-CIRC")[0]["detalle"] and bloquea(r_c, "F1-K3a"))
conc_c70 = [dict(e, componente="C70") if e["importe"] == -2090.0 else e for e in CONC]
r_c70 = ev(L0, decl(NORM, conc=conc_c70))
paso("G · la partida del circulante declarada en otro componente (C70 en lugar de C46): F1-CIRC DATOS INVÁLIDOS (la exclusión del circulante es de C46, "
     "C46 − CFO medio) y K3a ve los componentes sin explicar", efecto(r_c70, "F1-CIRC") == ["DATOS INVÁLIDOS"] and bloquea(r_c70, "F1-K3a"))
# caja base que INCLUYE el circulante (C46 = CFO + dividendos): K3a cuadra y la normalización haría pasar K3c; F1-CIRC lo impide
c46_con = round(sum(h(L0, 11, y) for y in (2023, 2024, 2025)) / 3 + 37.333333, 3)
c52_con = round(c46_con - L0["Análisis!C47"] - L0["Análisis!C48"] - L0["Análisis!C49"] - L0["Análisis!C50"], 3)
L_con = libro_vinci(**{"Análisis!C46": c46_con, "Análisis!C52": c52_con, "Historia!C70": c52_con})
conc_sin = [e for e in CONC if e["importe"] != -2090.0] + [{"componente": "C70", "importe": c52_con - (c46_con - L0["Análisis!C47"] - L0["Análisis!C48"] - L0["Análisis!C49"] - L0["Análisis!C50"]),
                                                            "partida": "redondeo", "fuente": {"documento": "prueba", "pagina": 1}}]
r_k = ev(L_con, decl(conc=conc_sin))
r_kn = ev(L_con, decl(NORM, conc=conc_sin))
paso("G · caja base CON el circulante (opción (b) del diagnóstico, sin la partida de M43): sin normalizar, K3a cuadra y K3c sigue BLOQUEANDO (reinversión −1.514,333)",
     not salta(r_k, "F1-K3a") and bloquea(r_k, "F1-K3c") and abs(cd(r_k)["f"] - cd(r_n)["f"]) < 1e-6, str(bloquean(r_k)))
paso("G · la misma con la normalización declarada y sin partida C46 del circulante: K3c ya no saltaría (+575,667), pero F1-CIRC DATOS INVÁLIDOS "
     "(ninguna partida C46 es la media de la fila 14; contaría el circulante como caja permanente dentro de C70). Las partidas que se compensan: grupo CAJA",
     efecto(r_kn, "F1-CIRC") == ["DATOS INVÁLIDOS"] and "caja permanente" in g(r_kn, "F1-CIRC")[0]["detalle"] and not salta(r_kn, "F1-K3c")
     and r_kn["utilizable_para_conclusion"] is False, g(r_kn, "F1-CIRC")[0]["detalle"][:160])
r_us = ev(dict(L0, **{"Control maestro!L4": "US GAAP"}), decl(NORM, norma="US_GAAP"))
paso("G · US GAAP: F1-CIRC MODELO NO APLICABLE (solo NIIF) y la normalización no se aplica",
     "MODELO NO APLICABLE" in efecto(r_us, "F1-CIRC") and (r_us.get("normalizacion_circulante") or {}).get("aplicada") is False)
d_nn = decl(NORM)
del d_nn["norma_contable"]
r_nn = ev(L0, d_nn)
paso("G · norma sin declarar: F1-NORMA bloquea, F1-CIRC INCOMPLETO y no se aplica", bloquea(r_nn, "F1-NORMA") and efecto(r_nn, "F1-CIRC") == ["INCOMPLETO"]
     and (r_nn.get("normalizacion_circulante") or {}).get("aplicada") is False)
base_ = {k: v for k, v in r_sin.items() if k not in ("declaracion_sha256", "fecha")}
iguales = []
for vacio in (None, {}):
    rv = ev(L0, decl(vacio) if vacio is not None else dict(decl(), normalizacion_circulante=None))
    iguales.append({k: v for k, v in rv.items() if k not in ("declaracion_sha256", "fecha")} == base_)
paso("G · vacío = sin declarar: «normalizacion_circulante»: null o {} da el mismo resultado que sin la clave (salvo la huella de la declaración)", all(iguales), str(iguales))
for valor in ("sí", [2023, 2024, 2025], 1):
    rv = ev(L0, dict(decl(), normalizacion_circulante=valor))
    paso(f"G · con contenido y sin ser un objeto ({valor!r}): F1-DECLARACION DATOS INVÁLIDOS y no se aplica",
         any(x["salta"] and x["efecto"] == "DATOS INVÁLIDOS" and "«normalizacion_circulante» no es un objeto" in x["detalle"] for x in g(rv, "F1-DECLARACION"))
         and abs(cd(rv)["f"] - cd(r_sin)["f"]) < 1e-15)
r_todos = ev(L0, decl(norm(anios=ANIOS)))
paso("G · años de más (2016–2025): se admiten; f y el ancla son los mismos que con 2021–2025 (solo cuentan la ventana y H–L)",
     g(r_todos, "F1-CIRC") and not salta(r_todos, "F1-CIRC") and r_todos["normalizacion_circulante"]["aplicada"] is True and abs(cd(r_todos)["f"] - cd(r_n)["f"]) < 1e-15 and abs(cd(r_todos)["ancla_s2c_E4"] - cd(r_n)["ancla_s2c_E4"]) < 1e-15)
r_nota = ev(L0, decl(norm(nota="texto")))
paso("G · la nota dentro de la declaración se admite (clave «nota»): F1-CIRC conforme y la normalización aplicada",
     g(r_nota, "F1-CIRC") and not salta(r_nota, "F1-CIRC") and r_nota["normalizacion_circulante"]["aplicada"] is True)
r_cero = ev(libro_vinci(**{f"Historia!{COL[y]}14": 0 for y in ANIOS}), decl(NORM, conc=[e for e in CONC if e["importe"] != -2090.0]))
paso("G · sin circulante (fila 14 = 0): la normalización no cambia nada, no exige partida en la caja base y el libro V6.3.1 la calcula (F1-LIBRO no salta por ella)",
     g(r_cero, "F1-CIRC") and not salta(r_cero, "F1-CIRC") and r_cero["normalizacion_circulante"]["aplicada"] is True
     and "circulante normalizado" not in g(r_cero, "F1-LIBRO")[0]["detalle"], str(bloquean(r_cero)))

# ------------------------------------------------------------------------------------------------ CAJA · la exclusión del circulante en C46, demostrada
# (revisión C1 del 19-nov-2026) F1-CIRC no se fía de las partidas de conciliacion_fcf_base, que son declaraciones: la exclusión del circulante se
# demuestra con el cálculo declarado de C46 del expediente (fase1_v63.json), reproducido con sus fuentes y atado al libro; si no, bloquea.
COMPENSA = [{"componente": "C46", "importe": -2090.0, "partida": "circulante excluido", "fuente": {"documento": "x", "pagina": 1}},
            {"componente": "C46", "importe": 2090.0, "partida": "compensación", "fuente": {"documento": "x", "pagina": 1}}]
conc_comp = conc_sin + COMPENSA
L_con2 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"],
                     **{"Análisis!C46": c46_con, "Análisis!C52": c52_con, "Historia!C70": c52_con})
r_cp, r_cp2 = ev(L_con, decl(NORM, conc=conc_comp)), ev(L_con2, decl(NORM, conc=conc_comp))
paso("CAJA · (C1, sonda del revisor) caja base CON el circulante y dos partidas C46 que se compensan (−2.090 «circulante excluido» y +2.090 "
     "«compensación», documento «x»): K3a cuadra y K3c no salta, pero F1-CIRC BLOQUEA (DATOS INVÁLIDOS): el libro lleva C46 = 11.417,333 y el "
     "cálculo declarado de C46 del expediente da 9.327,333",
     not salta(r_cp, "F1-K3a") and not salta(r_cp, "F1-K3c") and efecto(r_cp, "F1-CIRC") == ["DATOS INVÁLIDOS"]
     and "11417.333" in g(r_cp, "F1-CIRC")[0]["detalle"] and "9327.333" in g(r_cp, "F1-CIRC")[0]["detalle"], g(r_cp, "F1-CIRC")[0]["detalle"][:200])
paso("CAJA · (C1) la misma sonda con un libro V6.3.2 (antes: nada bloqueaba, utilizable con f −1,34 % y flujo sin crecimiento 7.365,9): ya no es "
     "utilizable y bloquea F1-CIRC, y solo él",
     bloquean(r_cp2) == ["F1-CIRC"] and r_cp2["utilizable_para_conclusion"] is False and abs(cd(r_cp2)["f"] + 0.013411) < 1e-5
     and abs(cd(r_cp2)["flujo_sin_crecimiento"] - 7365.885) < 1e-2, f"{bloquean(r_cp2)} · f {cd(r_cp2).get('f')} · F0 {cd(r_cp2).get('flujo_sin_crecimiento')}")
# la declaración amañada de forma coherente: también el cálculo declarado de C46 del expediente (fase1_v63.json) cuenta el circulante
CARPETAS_AMANADAS = (
    ("sin la fila 14 (C46 = CFO + dividendos)", f1_c46(terminos=[{"partida": "cfo", "signo": 1}, {"componente": "dividendos_sociedades_no_consolidadas", "signo": 1}],
                                                        valor=11417.333), "no suma la fila 14"),
    ("con la fila 14 y un componente «compensación» de 2.090 que cita un documento que no existe («x», p. 1)",
     f1_c46(terminos=EXP.CALCULO["terminos"] + [{"componente": "compensacion", "signo": 1}],
            componentes={"compensacion": {str(y): {"valor": 2090, "fuente": "x", "pagina": 1, "cita": "x"} for y in (2023, 2024, 2025)}}, valor=11417.333),
     "no se reproduce con sus fuentes"),
    ("con la fila 14 y la línea del circulante del estado de flujos como componente (fuente verdadera: 1.463 / 2.311 / 2.496)",
     f1_c46(terminos=EXP.CALCULO["terminos"] + [{"componente": "otros", "signo": 1}], componentes={"otros": EXP.CIRCULANTE_DEL_ESTADO_DE_FLUJOS}, valor=11417.333),
     "devuelve el circulante"),
    ("con la fila 14 y el circulante repartido en dos componentes con fuente (clientes y provisiones)",
     f1_c46(terminos=EXP.CALCULO["terminos"] + [{"componente": "clientes", "signo": 1}, {"componente": "provisiones", "signo": 1}],
            componentes={"clientes": EXP.CLIENTES, "provisiones": EXP.PROVISIONES}, valor=11417.333), "devuelven el circulante"),
    ("con la fila 14 y un componente con fuente que lo compensa en media (2.090 cada año)",
     f1_c46(terminos=EXP.CALCULO["terminos"] + [{"componente": "otros", "signo": 1}], componentes={"otros": EXP.OTROS_2090}, valor=11417.333),
     "devuelve el circulante"))
for nombre, f1_, frag in CARPETAS_AMANADAS:
    r_ = ev(L_con, decl(NORM, conc=conc_comp), carpeta=carpeta_con(f1_))
    paso(f"CAJA · caja base CON el circulante, partidas que se compensan y el cálculo de C46 {nombre}: F1-CIRC DATOS INVÁLIDOS",
         efecto(r_, "F1-CIRC") == ["DATOS INVÁLIDOS"] and frag in g(r_, "F1-CIRC")[0]["detalle"] and not salta(r_, "F1-K3a") and not salta(r_, "F1-K3c"),
         g(r_, "F1-CIRC")[0]["detalle"][:220])
# sin el cálculo que lo demuestre, la partida no basta: INCOMPLETO
for nombre, c_, frag in (("sin la carpeta del expediente", None, "sin la carpeta del expediente"),
                         ("sin fase1_v63.json", carpeta_con(sin_f1=True), "no tiene fase1_v63.json"),
                         ("con C46 sin cálculo declarado (una cifra)", carpeta_con(f1_c46(quitar_calculo=True)), "no tiene cálculo declarado")):
    r_ = ev(L0, decl(NORM), carpeta=c_)
    paso(f"CAJA · caja base genuina y la partida C46 de −2.090, pero {nombre}: F1-CIRC INCOMPLETO (no se puede demostrar que C46 excluye el circulante)",
         efecto(r_, "F1-CIRC") == ["INCOMPLETO"] and frag in g(r_, "F1-CIRC")[0]["detalle"], g(r_, "F1-CIRC")[0]["detalle"][:200])
# un cálculo de C46 que no demuestra la exclusión del circulante de la ventana de f, o que no describe este libro: DATOS INVÁLIDOS
T_SIN_C = [t for t in EXP.CALCULO["terminos"] if t.get("partida") != "circulante"]
f1_hist = f1_c46()
f1_hist["historia"]["partidas"]["cfo"]["valores"][8], f1_hist["historia"]["partidas"]["circulante"]["valores"][8] = 11403, -2000   # 2024: misma suma
for nombre, f1_, frag in (("es una suma, no la media", f1_c46(operacion="suma", valor=None), "no la media"),
                          ("usa otros años (2022–2024, CFO + fila 14)", f1_c46(terminos=[{"partida": "cfo", "signo": 1}, {"partida": "circulante", "signo": 1}],
                                                                            anios=[2022, 2023, 2024], valor=None), "ventana de f"),
                          ("resta la fila 14", f1_c46(terminos=T_SIN_C + [{"partida": "circulante", "signo": -1}], valor=None), "no suma la fila 14"),
                          ("suma la fila 14 dos veces", f1_c46(terminos=EXP.CALCULO["terminos"] + [{"partida": "circulante", "signo": 1}], valor=None), "no suma la fila 14"),
                          ("no lleva el CFO", f1_c46(terminos=[t for t in EXP.CALCULO["terminos"] if t.get("partida") != "cfo"], valor=None), "no suma el CFO"),
                          ("cita una página que no existe (p. 99)", f1_c46(componentes={"dividendos_sociedades_no_consolidadas": dict(
                              EXP.DIVIDENDOS, **{"2024": dict(EXP.DIVIDENDOS["2024"], pagina=99)})}), "no se reproduce con sus fuentes"),
                          ("cita un texto que no está en la página", f1_c46(componentes={"dividendos_sociedades_no_consolidadas": dict(
                              EXP.DIVIDENDOS, **{"2023": dict(EXP.DIVIDENDOS["2023"], cita="Dividends 31")})}), "no se reproduce con sus fuentes"),
                          ("se hace con otra Historia (2024: CFO 11.403 y fila 14 −2.000, misma suma; el libro lleva 11.714 y −2.311)", f1_hist, "no es la")):
    r_ = ev(L0, decl(NORM), carpeta=carpeta_con(f1_))
    paso(f"CAJA · el cálculo declarado de C46 {nombre}: F1-CIRC DATOS INVÁLIDOS", efecto(r_, "F1-CIRC") == ["DATOS INVÁLIDOS"] and frag in g(r_, "F1-CIRC")[0]["detalle"],
         g(r_, "F1-CIRC")[0]["detalle"][:220])
# el C46 del libro es el cálculo redondeado a los decimales con que lo escribe (no otra cifra)
r_2d = ev(dict(L0, **{"Análisis!C46": 9327.33}), decl(NORM))
r_mal = ev(dict(L0, **{"Análisis!C46": 9327.34}), decl(NORM))
paso("CAJA · C46 del libro con dos decimales (9.327,33 = el cálculo 9.327,333… redondeado): F1-CIRC no salta; con 9.327,34, DATOS INVÁLIDOS («el libro lleva C46»)",
     g(r_2d, "F1-CIRC") and not salta(r_2d, "F1-CIRC") and efecto(r_mal, "F1-CIRC") == ["DATOS INVÁLIDOS"] and "el libro lleva C46" in g(r_mal, "F1-CIRC")[0]["detalle"],
     g(r_mal, "F1-CIRC")[0]["detalle"][:160])
paso("CAJA · (control) sin la declaración nada de esto cuenta: la sonda del revisor sin normalizar sigue bloqueando por K3c y no hay F1-CIRC",
     bloquea(ev(L_con, decl(conc=conc_comp)), "F1-K3c") and not g(ev(L_con, decl(conc=conc_comp), carpeta=None), "F1-CIRC"))

# ------------------------------------------------------------------------------------------------ K3 · puente y K3c
lineas = cd(r_n)["K3"]["lineas"]
ln = [x for x in lineas if x["clase"] == "normalizacion_declarada"]
paso("K3 · el puente lleva la partida «circulante que la normalización excluye» (+2.090 = −media de la fila 14) y cuadra a 10⁻⁹",
     len(ln) == 1 and abs(ln[0]["mm"] - 2090.0) < 1e-9 and cd(r_n)["K3"]["identidad_cuadra"] and not salta(r_n, "F1-K3"))
paso("K3 · la partida del circulante excluido no es «sin explicar» y K3 queda conforme", not any("normalización" in p for p in cd(r_n)["K3"]["partidas_sin_explicar"])
     and r_n["K3"]["conforme"] is True)
paso("K3 · (control) el puente sin normalizar no lleva esa partida", not any(x["clase"] == "normalizacion_declarada" for x in cd(r_sin)["K3"]["lineas"]))
L_neg = libro_vinci(**{f"Historia!{COL[y]}8": h(L0, 8, y) + 1000 for y in (2023, 2024, 2025)})
r_neg = ev(L_neg, decl(NORM))
paso("K3 · K3c no se debilita: con la D&A propia por encima del capex (capex − D_X < 0 con ventas al alza), la reinversión normalizada es negativa y K3c BLOQUEA",
     bloquea(r_neg, "F1-K3c") and cd(r_neg)["reinversion_media"] < 0 and "normalizado" in g(r_neg, "F1-K3c")[0]["detalle"],
     f"{cd(r_neg).get('reinversion_media')} · {g(r_neg, 'F1-K3c')[0]['detalle'][:100]}")
paso("K3 · ese mismo caso con una justificación declarada: K3c AVISA (la salida de siempre, sin cambios)",
     [(x["severidad"], "normalizado" in x["detalle"]) for x in g(ev(L_neg, decl(NORM, justificacion_reinversion_negativa="prueba")), "F1-K3c") if x["salta"]] == [("AVISO", True)])

# ------------------------------------------------------------------------------------------------ LIBRO · oráculo y réplica
r_l2 = ev(libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=[2022, 2023, 2024, 2025]), decl(NORM))
paso("LIBRO · V6.3.2 con otros años normalizados (sin 2021) que la declaración: F1-LIBRO bloquea («años normalizados del libro … ≠ declarados»)",
     bloquea(r_l2, "F1-LIBRO") and "años normalizados" in g(r_l2, "F1-LIBRO")[0]["detalle"] and not salta(r_l2, "F1-REPLICA"), str(bloquean(r_l2)))
r_l3 = ev(libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"]), decl())
paso("LIBRO · V6.3.2 con la normalización efectiva y la declaración sin ella: F1-LIBRO bloquea; la réplica usa el circulante del libro (F1-REPLICA no salta)",
     bloquea(r_l3, "F1-LIBRO") and "no tiene una normalización aplicable" in g(r_l3, "F1-LIBRO")[0]["detalle"] and not salta(r_l3, "F1-REPLICA"),
     str(bloquean(r_l3)))
L4 = libro_vinci(v632=True)
r_l4 = ev(L4, decl())
paso("LIBRO · (control) V6.3.2 sin normalización y sin declaración: el mismo resultado que con el libro V6.3.1 (f, flujo, K3c, guardas que saltan); C97 «ninguna»",
     L4["Historia!C97"] == "ninguna" and cd(r_l4)["f"] == cd(r_sin)["f"] and cd(r_l4)["flujo_sin_crecimiento"] == cd(r_sin)["flujo_sin_crecimiento"]
     and bloquean(r_l4) == bloquean(r_sin) and "normalizacion_circulante" not in r_l4)
L5 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"])
L5["Historia!K95"] = 0.0
r_l5 = ev(L5, decl(NORM))
paso("LIBRO · V6.3.2 con la fila 95 manipulada (2024 = 0): F1-REPLICA bloquea (fallo de implementación) y la nombra",
     bloquea(r_l5, "F1-REPLICA") and "K95" in g(r_l5, "F1-REPLICA")[0]["detalle"] and "fallo_de_implementacion" in r_l5["estado_propuesto"])
L6 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"])
L6["Historia!H94"] = 2
r_l6 = ev(recalcular(L6), decl(NORM))
paso("LIBRO · V6.3.2 con una marca que no es 1 (2021 = 2): C97 «no reconocida», f y C53 vacías en el libro; la capa no falla: F1-LIBRO bloquea, F1-REPLICA no",
     L6["Historia!C97"] == "no reconocida" and L6["Historia!C58"] is None and bloquea(r_l6, "F1-LIBRO") and not salta(r_l6, "F1-REPLICA"), str(bloquean(r_l6)))
L7 = libro_vinci(v632=True, regla="otra", anios_norm=NORM["anios"])
r_l7 = ev(L7, decl(NORM))
paso("LIBRO · V6.3.2 con otra regla en C93: «no reconocida»; F1-LIBRO bloquea y dice la normalización efectiva del libro",
     L7["Historia!C97"] == "no reconocida" and bloquea(r_l7, "F1-LIBRO") and "«no reconocida» ≠ declarada" in g(r_l7, "F1-LIBRO")[0]["detalle"])
# libro V6.3: sin la sección F1 (filas 84 y siguientes) y con lo que calcula la V6.3 (A0: D_X = D&A total)
L8 = {k: v for k, v in recalcular(dict(L0, **{"Historia!C89": "A0_total"})).items() if not k.startswith("Historia!") or _fila_h(k) < 84}
r_l8 = ev(L8, decl(NORM))
paso("LIBRO · libro V6.3 (sin la sección F1) con la normalización: F1-LIBRO bloquea como límite declarado y nombra el circulante normalizado",
     bloquea(r_l8, "F1-LIBRO") and "LÍMITE DECLARADO" in g(r_l8, "F1-LIBRO")[0]["detalle"] and "circulante normalizado" in g(r_l8, "F1-LIBRO")[0]["detalle"]
     and not salta(r_l8, "F1-REPLICA"), str(bloquean(r_l8)))
L8b = dict(L8)
r_l8b = ev(L8b, decl(NORM, per="A0_total"))
paso("LIBRO · libro V6.3 con A0 y la normalización: solo la normalización hace saltar F1-LIBRO (límite declarado); la réplica A0 es la del libro (sin normalizar)",
     bloquea(r_l8b, "F1-LIBRO") and "circulante normalizado" in g(r_l8b, "F1-LIBRO")[0]["detalle"] and not salta(r_l8b, "F1-REPLICA")
     and not salta(ev(L8b, decl(per="A0_total")), "F1-LIBRO"), str(bloquean(r_l8b)))
L9 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=[2023, 2024, 2025])
r_l9 = ev(L9, decl(norm(anios=[2023, 2024, 2025])))
paso("LIBRO · V6.3.2 y declaración solo con la ventana: el libro deja C53 vacía como la capa; F1-LIBRO no salta por el ancla (bloquea F1-CIRC)",
     L9["Historia!C53"] is None and isinstance(L9["Historia!C58"], float) and not salta(r_l9, "F1-LIBRO") and bloquea(r_l9, "F1-CIRC"), str(bloquean(r_l9)))
L10 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=[2021, 2022, 2023, 2025])
r_l10 = ev(L10, decl(norm(anios=[2021, 2022, 2023, 2025])))
paso("LIBRO · V6.3.2 y declaración sin un año de la ventana: f vacía en el libro y en la capa, sin excepción; F1-REPLICA no salta",
     L10["Historia!C58"] is None and cd(r_l10) == {} and not salta(r_l10, "F1-REPLICA") and not salta(r_l10, "F1-LIBRO"), str(bloquean(r_l10)))
L12 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=[2021, 2022, 2023, 2025], **{"Historia!C89": "A0_total"})
try:
    r_l12 = ev(L12, decl(norm(anios=[2021, 2022, 2023, 2025]), per="A0_total"))
    ok12 = L12["Historia!C58"] is None and bloquea(r_l12, "F1-CIRC") and not salta(r_l12, "F1-REPLICA")
    det12 = str(bloquean(r_l12))
except M.ErrorDeclaracion as ex:
    ok12, det12 = False, f"ErrorDeclaracion: {ex}"
paso("LIBRO · V6.3.2 con A0 y la ventana sin normalizar entera: C58 vacía no es un libro ilegible (sin ErrorDeclaracion); F1-CIRC bloquea, F1-REPLICA no", ok12, det12)
L11 = libro_vinci(v632=True, regla="circulante_a_cero", anios_norm=NORM["anios"])
L11["Historia!C97"] = None
r_l11 = ev(L11, decl(NORM))
paso("LIBRO · V6.3.2 sin el valor calculado de C97 (libro sin recalcular): F1-LIBRO bloquea y lo dice", bloquea(r_l11, "F1-LIBRO")
     and "sin recalcular" in g(r_l11, "F1-LIBRO")[0]["detalle"])
paso("LIBRO · (control) corresponde() de un libro V6.3.1 sin normalización declarada: los mismos motivos que antes (ninguno nuevo)",
     V631.corresponde(dict(L0), "A2_propio", {y: Fr(v) for y, v in ROU.items()}, {y: Fr(v) for y, v in PPA.items()}, ANIOS, COL,
                      lambda y: M.Q(L0.get(f"Historia!{COL[y]}88")), {"f": Fr(repr(L0["Historia!C58"])), "ancla": Fr(repr(L0["Historia!C53"]))}, []) == [])
paso("LIBRO · normalizacion_del_libro y replica_circulante: None y [] en un libro V6.3.1", V631.normalizacion_del_libro(L0, ANIOS, COL) is None
     and V631.replica_circulante(L0, ANIOS, COL) == [])
paso("LIBRO · replica_circulante: [] en un libro V6.3.2 coherente y nombra la fila 96 manipulada",
     V631.replica_circulante(L5 | {"Historia!K95": -2311}, ANIOS, COL) == [] and any("K96" in x for x in V631.replica_circulante(dict(L5, **{"Historia!K95": -2311, "Historia!K96": 5.0}), ANIOS, COL)))

# ------------------------------------------------------------------------------------------------ APLICAR · f1_libro_v631
cel = V631.celdas(decl(NORM), ANIOS, circulante=True)
paso("APLICAR · V6.3.2: C93 = «circulante_a_cero», C94:L94 = 1 en 2021–2025 y vacías en 2016–2020, con su procedencia en M93:M94",
     cel["Historia!C93"] == "circulante_a_cero" and [cel[f"Historia!{c}94"] for c in COLS] == [None] * 5 + [1] * 5
     and "normalizacion_circulante" in str(cel["Historia!M93"]) and "2021" in str(cel["Historia!M94"]))
cel631 = V631.celdas(decl(NORM), ANIOS)
paso("APLICAR · (control) V6.3.1 (por omisión): las mismas 24 celdas de siempre, sin las de la normalización (el libro V6.3.1 no las tiene)",
     len(cel631) == 24 and not any(k[-2:] in ("93", "94") for k in cel631))
for nombre, d_ in (("regla inválida", decl(norm(regla="otra"))), ("un año fuera de la Historia", decl(norm(anios=[2015, 2021]))), ("US GAAP", decl(NORM, norma="US_GAAP")),
                   ("sin declarar", decl())):
    c_ = V631.celdas(d_, ANIOS, circulante=True)
    paso(f"APLICAR · {nombre}: C93 y C94:L94 vacías (= sin normalización; la capa bloquea con F1-CIRC si se declaró)",
         c_["Historia!C93"] is None and all(c_[f"Historia!{c}94"] is None for c in COLS) and c_["Historia!M93"] is None)
tmp = tempfile.mkdtemp(prefix="circ_aplicar_")
try:
    sys.path.insert(0, os.path.join(PV, "scripts"))
    from v63_xml import LibroV63  # noqa: E402
    dp = os.path.join(tmp, "motor_a_f1.json")
    json.dump(decl(NORM), open(dp, "w", encoding="utf-8"), ensure_ascii=False)
    ok_pl = os.path.isfile(PLANTILLA_V632) and os.path.isfile(PLANTILLA_V631)
    if ok_pl:
        for nom, pl in (("v632", PLANTILLA_V632), ("v631", PLANTILLA_V631)):
            lb = LibroV63(pl)
            lb.escribir_celdas({f"Historia!{c}5": y for c, y in zip(COLS, ANIOS)})
            lb.guardar(os.path.join(tmp, f"{nom}_base.xlsx"))
            V631.aplicar(os.path.join(tmp, f"{nom}_base.xlsx"), os.path.join(tmp, f"{nom}.xlsx"), dp)
        l2, l1 = LibroV63(os.path.join(tmp, "v632.xlsx")), LibroV63(os.path.join(tmp, "v631.xlsx"))
        import entradas_economicas as EE  # noqa: E402
        lec2 = EE._Lector(os.path.join(tmp, "v632.xlsx"))
        paso("APLICAR · sobre la plantilla V6.3.2 real: escribe C93 y C94:L94 (texto y números), sin tocar sus fórmulas (C95:L97)",
             V631.es_v632(l2) and lec2.leer("Historia", "C93") == "circulante_a_cero" and l2.leer("Historia", "H94") == 1 and l2.leer("Historia", "G94") is None
             and l2.tiene_formula("Historia", "C97") and l2.tiene_formula("Historia", "H95") and l2.tiene_formula("Historia", "H96"))
        paso("APLICAR · sobre la plantilla V6.3.1 real: no escribe nada en las filas 93–94 (no existen) y su perímetro sí",
             not V631.es_v632(l1) and l1.leer("Historia", "C93") is None and l1.leer("Historia", "H94") is None and EE._Lector(os.path.join(tmp, "v631.xlsx")).leer("Historia", "C85") == "A2_propio")
        # ------------------------------------------------------------------------------------------- EE · huella y universo de entradas
        i2 = EE.instantanea(os.path.join(tmp, "v632.xlsx"))
        json.dump(decl(), open(dp, "w", encoding="utf-8"), ensure_ascii=False)
        V631.aplicar(os.path.join(tmp, "v632_base.xlsx"), os.path.join(tmp, "v632_sin.xlsx"), dp)
        i2s = EE.instantanea(os.path.join(tmp, "v632_sin.xlsx"))
        i1 = EE.instantanea(os.path.join(tmp, "v631.xlsx"))
        paso("EE · V6.3.2: C93 y C94:L94 entran en la huella de entradas como configuración; con y sin normalización las huellas son distintas",
             i2["tipos"].get("Historia!C93") == "configuracion" and i2["celdas"]["Historia!H94"] == 1 and i2["celdas"]["Historia!C93"] == "circulante_a_cero"
             and i2["huella"] != i2s["huella"] and i2s["celdas"]["Historia!C93"] is None)
        paso("EE · un libro V6.3.1 no lleva esas celdas (su huella no cambia con la V6.3.2)", not any(k in i1["celdas"] for k in ("Historia!C93", "Historia!H94")))
    else:
        paso("APLICAR · las plantillas V6.3.1 y V6.3.2 están materializadas (v6/v631_f1/entregables, v6/v632_f1/entregables)", False, f"{PLANTILLA_V632}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ------------------------------------------------------------------------------------------------ SEL · selección de la plantilla
import config_v2  # noqa: E402
import seleccion_plantilla as SEL  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
CFG631, CFG632 = config_v2.cargar(os.path.join(PV, "config_v2_v631_f1.json")), config_v2.cargar(os.path.join(PV, "config_v2_v632_f1.json"))
pl = CFG632["plantilla"]
paso("SEL · config_v2_v632_f1.json: V6.3.2 F1, de la familia V6.3.1 (el paso 2 le aplica la declaración), con su plantilla, referencia, verificador e inventario",
     SEL.version(CFG632) == SEL.V632 and SEL.es_v631(CFG632) and SEL.es_v632(CFG632) and not SEL.es_v632(CFG631) and SEL.registra(CFG632)
     and pl["archivo"].endswith("Plantilla_V6.3.2_F1.xlsx") and pl["referencia"].endswith("referencia_V6.3.2_F1.json") and pl["verificador"].endswith("verificar_v632.py")
     and all(os.path.isfile(pl[k]) for k in ("archivo", "referencia", "verificador", "add_sliders")) and os.path.isfile(os.path.join(pl["scripts_v63"], "inventario_entradas.py")))
c631 = {k: v for k, v in CFG631.items() if k not in ("plantilla", "_nota", "_nota_resumen", "version_config", "resumen_csv_nombre", "_ruta_config")}
c632 = {k: v for k, v in CFG632.items() if k not in ("plantilla", "_nota", "_nota_resumen", "version_config", "resumen_csv_nombre", "_ruta_config")}
paso("SEL · config_v2_v632_f1.json es la de la V6.3.1 salvo la plantilla, la versión, las notas y el resumen; resumen propio resumen_v2_v632_f1.csv",
     c631 == c632 and {k: v for k, v in CFG632["plantilla"].items() if k not in ("version", "archivo", "referencia", "verificador", "scripts_v63", "add_sliders", "docs")}
     == {k: v for k, v in CFG631["plantilla"].items() if k not in ("version", "archivo", "referencia", "verificador", "scripts_v63", "add_sliders", "docs")}
     and CIE.nombre_resumen("/nonexistent", CFG632) == "resumen_v2_v632_f1.csv")
tmp = tempfile.mkdtemp(prefix="circ_sel_")
try:
    c = os.path.join(tmp, "nuevo")
    os.makedirs(c)
    paso("SEL · expediente nuevo con la V6.3.2: se acepta y registra plantilla_activa.json; después no se ejecuta con la V6.3.1 (ni al revés)",
         SEL.comprobar(c, CFG632) is None and SEL.registrar(c, CFG632) and (SEL.leer(c) or {}).get("version") == SEL.V632 and bool(SEL.comprobar(c, CFG631))
         and CIE.nombre_resumen(c) == "resumen_v2_v632_f1.csv", str(SEL.comprobar(c, CFG631))[:100])
    c2 = os.path.join(tmp, "v631")
    os.makedirs(c2)
    SEL.registrar(c2, CFG631)
    paso("SEL · un expediente V6.3.1 (plantilla_activa.json V6.3.1, como vinci/Vinci) no se ejecuta con la V6.3.2: para cambiar de plantilla, un expediente nuevo",
         "expediente nuevo" in str(SEL.comprobar(c2, CFG632)))
    c3 = os.path.join(tmp, "conf")
    os.makedirs(c3)
    open(os.path.join(c3, SEL.CONF), "w").write("{}")
    paso("SEL · configuración económica con la V6.3.2: se rechaza (no se ignora)", "V6.3.2 F1" in str(SEL.comprobar(c3, CFG632)))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
esq = json.load(open(os.path.join(PV, "esquema", "ficha.esquema.json"), encoding="utf-8"))
paso("SEL · ficha.esquema.json admite «V6.3.2 F1»", "V6.3.2 F1" in esq["properties"]["versiones"]["properties"]["plantilla"]["enum"])

# ------------------------------------------------------------------------------------------------ DATOS y MD
import volcar_datos_v63 as VD  # noqa: E402
import openpyxl  # noqa: E402
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Historia"
for c, y in zip(COLS, ANIOS):
    ws[f"{c}5"] = y
ws["A92"], ws["C97"] = "  NORMALIZACIÓN DEL CIRCULANTE · motor A (V6.3.2 F1)", "circulante_a_cero"
for c, y in zip(COLS, ANIOS):
    if y >= 2021:
        ws[f"{c}94"], ws[f"{c}95"] = 1, float(-y)
nd = VD.normalizacion_circulante(wb)
ws["C97"] = "ninguna"
paso("DATOS · el volcado a las fases dice los años normalizados y lo excluido (libro V6.3.2 efectivo); con «ninguna» o un libro V6.3.1, nada",
     nd == {"anios": [2021, 2022, 2023, 2024, 2025], "excluido": {str(y): float(-y) for y in range(2021, 2026)}} and VD.normalizacion_circulante(wb) is None
     and VD.normalizacion_circulante(openpyxl.Workbook()) is None)
md = M.informe_md(r_n)
paso("MD · el informe lleva la sección «Normalización declarada del circulante (V-CIRC)» con el efecto y el cálculo declarado de C46 que demuestra la "
     "exclusión, con sus componentes para la revisión de entradas; sin la declaración, no",
     "## Normalización declarada del circulante (V-CIRC)" in md and "5190.97" in md and "Normalización declarada del circulante" not in M.informe_md(r_sin)
     and "Cálculo declarado de C46" in md and "dividendos_sociedades_no_consolidadas" in md and "revisión de entradas" in md)
paso("MD · la plantilla de la declaración documenta la clave (vacía = sin declarar)", "normalizacion_circulante" in M.plantilla_declaracion()
     and M.plantilla_declaracion()["normalizacion_circulante"] is None and "normalizacion_circulante" in M.CLAVES_DECL)

shutil.rmtree(CARPETA, ignore_errors=True)
shutil.rmtree(TMP_C46, ignore_errors=True)
n = sum(ok for _, ok in R)
print(f"{n}/{len(R)} pruebas de la normalización del circulante (V-CIRC) PASAN" if n == len(R) else
      f"{n}/{len(R)} pruebas de la normalización del circulante (V-CIRC): FALLAN {len(R) - n}")
sys.exit(0 if n == len(R) else 1)
