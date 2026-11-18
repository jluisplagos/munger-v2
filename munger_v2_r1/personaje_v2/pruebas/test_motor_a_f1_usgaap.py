#!/usr/bin/env python3
"""Batería F1 · US GAAP (ASC 842): motor A con arrendamientos operativos y financieros por separado, puente de deuda y K3 (F1_USGAAP.md).

Uso (desde personaje_v2/): python3 -B pruebas/test_motor_a_f1_usgaap.py
Sin LibreOffice: libros sintéticos con valores; las anclas (Historia C52, C53, C58) se calculan aquí con las fórmulas de la plantilla, en
coma flotante e independientes de motor_a_f1. Empresa estable de referencia: ventas 1.000; resultado antes de alquileres y amortizaciones
100; capex propio = D&A propia = 20; alquiler operativo 12 (coste lineal = pago: 10 de amortización no monetaria del derecho de uso y 2 de
actualización del pasivo). EBIT 68, CFO 88, FCF base 68: la caja sin crecimiento es 68. Con financieros: derecho de uso 5, interés 1 y
principal 5 → EBIT 63, CFO 87, FCF base 62.
Grupos: N (norma como valor cerrado y mezcla), U1–U7 (operativos: tramos fuera, dentro de la fila 8, dentro de la fila 14), U2 y U4
(financieros y C49), U5 (desglose ausente), H (hipótesis D-US1 y su cota), D (D-US2: pagos frente a coste lineal), P (puente de deuda y
motor B), K3, S (fuentes de las series y citas), V631 (fila 86 del libro), G13 (crecimiento e impuestos), NIIF (no cambia), EX (exigencia,
vigencia y gancho del pipeline) y CLI.
"""
import copy
import hashlib
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
sys.dont_write_bytecode = True
import motor_a_f1 as M  # noqa: E402
import f1_libro_v631 as V631  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


COLS = "CDEFGHIJKL"
ANIOS = list(range(2016, 2026))
REG = {"fecha": "2026-11-18", "persona": "prueba sintética (no es una decisión)", "motivo": "caso de prueba US GAAP"}
DOC = "10-K sintético"
FUENTE = "fuente_sintetica_us.txt"
PAG2 = ("CONSOLIDATED STATEMENTS OF CASH FLOWS\nNet income 51\nDepreciation and amortization 20\nStock-based compensation 0\n"
        "Other non-cash items, net 3\nAccounts receivable (4)\nAccounts payable and accrued liabilities 6\nNet cash provided by operating activities 88\n"
        "Principal payments on finance lease obligations (5)\nRight-of-use assets obtained in exchange for new operating lease liabilities 15\n")
PAG3 = ("CONSOLIDATED STATEMENTS OF CASH FLOWS\nNet income 51\nDepreciation and amortization 20\nNon-cash lease expense 10\n"
        "Accounts receivable (4)\nOperating lease liabilities (10)\nNet cash provided by operating activities 88\n")


def lista(x):
    return [float(x)] * 10 if isinstance(x, (int, float)) else [float(v) for v in x]


def libro(ebit=68.0, da=20.0, dwc=0.0, C70=68.0, C49=0.0, princ=0.0, tau=0.0, capex=20.0, adq=0.0, ventas=1000.0, l4="US GAAP", c48=0.0, int16=0.0,
          fila22=100.0, fila23=0.0, motor="A", n=3, palancas=True, r=0.09):
    """Libro sintético V6.3 (solo valores): las mismas fórmulas de la plantilla que usa test_motor_a_f1.py, más las filas 22 y 23 (puente)."""
    V, E, D, T, K, A, W, PR = (lista(x) for x in (ventas, ebit, da, tau, capex, adq, dwc, princ))
    L = {"sha256": "sintetico", "Diagnóstico V6!C5": motor, "Control maestro!L4": l4, "Diagnóstico V6!C179": 0.05, "Análisis!C56": r}
    for i, c in enumerate(COLS):
        for fila, serie_ in ((5, ANIOS), (6, V), (7, E), (8, D), (10, T), (12, K), (13, A), (14, W), (17, PR)):
            L[f"Historia!{c}{fila}"] = serie_[i]
        L[f"Historia!{c}22"], L[f"Historia!{c}23"] = fila22, fila23
    w = range(10 - n, 10)
    S = sum(V[i] for i in w) / n
    nop = sum(E[i] * (1 - T[i]) for i in w) / n
    rei = sum(K[i] - D[i] + W[i] for i in w) / n
    L.update({"Historia!C58": ((nop - rei) - C70) / S, "Historia!C57": n, "Historia!C70": C70, "Historia!C44": V[-1], "Historia!C48": E[-1] / V[-1],
              "Historia!C52": sum(T[5:]) / 5, "Historia!C64": fila22 + fila23})
    den = sum(K[i] - D[i] + W[i] + A[i] for i in range(5, 10))
    L["Historia!C53"] = (V[-1] - V[4]) / den if den > 0 else ""
    for i, c in enumerate(COLS):   # FCF base y su segunda vía (fila 35), coherentes por construcción
        L[f"Historia!{c}11"] = C70 + K[i] + c48 + C49
        L[f"Historia!{c}16"], L[f"Historia!{c}18"] = int16, 0.0
        L[f"Historia!{c}35"] = L[f"Historia!{c}11"] - K[i] - int16 - PR[i]
    L["Análisis!C46"] = sum(L[f"Historia!{COLS[i]}11"] for i in w) / n
    L["Análisis!C47"], L["Análisis!C48"], L["Análisis!C49"], L["Análisis!C50"], L["Análisis!C51"], L["Análisis!C52"] = sum(K[i] for i in w) / n, c48, C49, 0.0, "Sí", C70
    if palancas:
        for c, (g15, mo, s2c, gi, roic) in {"B": (0.02, 0.07, 1.0, 0.01, 0.08), "C": (0.03, 0.07, 1.2, 0.02, 0.10), "D": (0.04, 0.08, 1.5, 0.025, 0.12)}.items():
            L[f"Palancas!{c}14"], L[f"Palancas!{c}15"], L[f"Palancas!{c}16"], L[f"Palancas!{c}18"], L[f"Análisis!{c}68"] = g15, mo, s2c, roic, gi
    for c, s in zip("BCD", (0.0047, 0.0068, 0.0241)):
        L[f"Diagnóstico V6!{c}178"], L[f"Diagnóstico V6!{c}176"], L[f"Diagnóstico V6!{c}177"] = s, s + 0.1, 0.1
    return L


def serie(vals, signo=1, pagina=1):
    """Serie declarada: signo 1 = cifra publicada en positivo; −1 = publicada entre paréntesis (cargo o salida) y magnitud positiva en el modelo."""
    vals = vals if isinstance(vals, dict) else {y: vals for y in ANIOS}
    out = {}
    for y, v in vals.items():
        vf = -v if signo == -1 else v
        out[str(y)] = {"valor_fuente": vf, "signo": signo, "tratamiento": "publicado entre paréntesis" if signo == -1 else "ninguno", "documento": DOC, "pagina": pagina,
                       "literal": f"({abs(vf)})" if vf < 0 else f"{vf}"}
    return out


CITAS = {("op", True): "Operating lease cost", ("op", False): "The Company has no operating leases", ("fin", True): "Finance lease cost",
         ("fin", False): "The Company has no finance leases", ("am", "fila_8"): "Depreciation and amortization, including amortization of operating lease right-of-use assets",
         ("am", "fila_14"): "Operating lease right-of-use assets and other assets", ("am", "fuera_de_las_filas_8_y_14"): "Non-cash lease expense",
         ("pas", "fila_14"): "Operating lease liabilities", ("pas", "fuera_de_las_filas_8_y_14"): "Other operating activities, net"}


def ev(clave, valor):
    return {"documento": DOC, "pagina": 1, "cita": CITAS[(clave, valor)]}


def ubic(clave, u, pagina_np=2):
    if u is None:
        return {}
    if u == "no_publicada":
        return {"ubicacion": u, "documento": DOC, "pagina": pagina_np}
    return dict(ev(clave, u), ubicacion=u) if (clave, u) in CITAS else {"ubicacion": u, "documento": DOC, "pagina": 1, "cita": "Other operating activities, net"}


def decl(per="A0_total", norma="US_GAAP", op=True, fin=False, ub_am="fuera_de_las_filas_8_y_14", ub_pas="fuera_de_las_filas_8_y_14", P=12, Lc=12, a8=None,
         ajuste=None, pasivo=0, rou_fin=None, fin_princ=None, ppa=0, us=True, pagina_np=2):
    d = {"norma_contable": {"valor": norma, "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
         "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": per, "registro": REG},
         "perimetro_roic": {"valor": per, "registro": REG}, "clasificacion_compras": {"valor": "sin_compras", "registro": REG},
         "transicion": {"conocida": False, "tratamiento": None, "registro": REG}, "series": {"da_ppa": serie(ppa)}}
    if us:
        d["arrendamientos_us_gaap"] = {"registro": REG, "operativos": None if op is None else dict(ev("op", op), existen=op),
                                       "financieros": None if fin is None else dict(ev("fin", fin), existen=fin)}
        if op:
            d["arrendamientos_us_gaap"]["operativos"].update({"amortizacion_rou": ubic("am", ub_am, pagina_np), "variacion_pasivo": ubic("pas", ub_pas, pagina_np)})
            for nombre, v in (("pagos_arr_operativo", P), ("coste_arr_operativo", Lc)):
                if v is not None:
                    d["series"][nombre] = serie(v)
            if pasivo is not None:
                d["series"]["pasivo_arr_operativo"] = serie({2025: pasivo})
    if a8 is not None:
        d["series"]["da_rou_operativo"] = serie(a8)
    if ajuste is not None:
        d["series"]["circulante_arr_operativo"] = serie(ajuste, signo=-1 if (isinstance(ajuste, (int, float)) and ajuste > 0) else 1)
    if rou_fin is not None:
        d["series"]["da_rou"] = serie(rou_fin)
    if fin_princ is not None:
        d["series"]["pagos_arr_financiero_principal"] = serie(fin_princ, signo=-1)
    return d


def fuentes(d, carpeta=None, paginas=(PAG2, PAG3)):
    """Escribe la fuente sintética del expediente (página 1: las cifras publicadas y las citas de la declaración; página 2: un estado de flujos
    sin líneas del arrendamiento operativo; página 3: uno con ellas) y registra en la declaración su archivo y su huella."""
    carpeta = carpeta or tempfile.mkdtemp(prefix="f1_us_")
    lits = sorted({str(e.get("literal")) for s_ in (d.get("series") or {}).values() for e in s_.values() if isinstance(e, dict)})
    citas = []
    b = d.get("arrendamientos_us_gaap") or {}
    for k in ("operativos", "financieros"):
        x = b.get(k) or {}
        citas += [x.get("cita")] + [(x.get(t) or {}).get("cita") for t in ("amortizacion_rou", "variacion_pasivo")]
    txt = "[PDF PAGE 1]\nNotas sintéticas: " + " ".join(lits) + "\n" + "\n".join(sorted({c for c in citas if c})) + "\n"
    txt += "".join(f"[PDF PAGE {i + 2}]\n{p}" for i, p in enumerate(paginas)) + f"[PDF PAGE {len(paginas) + 2}]\n"
    os.makedirs(carpeta, exist_ok=True)
    open(os.path.join(carpeta, FUENTE), "w", encoding="utf-8").write(txt)
    d["fuentes_series"] = {DOC: {"archivo": FUENTE, "sha256": hashlib.sha256(txt.encode("utf-8")).hexdigest()}}
    return carpeta


TMP = []


def ev_(L, d, con_fuentes=True, **k):
    """Evalúa con la fuente sintética escrita (F1-SERIES examina cifras y citas)."""
    c = None
    if con_fuentes:
        c = fuentes(d)
        TMP.append(c)
    return M.evaluar(L, d, carpeta=c, **k)


def g(r, gid):
    return [x for x in r["guardas"] if x["id"] == gid]


def salta(r, gid):
    return any(x["salta"] for x in g(r, gid))


def bloquea(r, gid):
    return any(x["salta"] and x["severidad"] == "BLOQUEA" for x in g(r, gid))


def bloquean(r):
    return sorted({x["id"] for x in r["guardas"] if x["salta"] and x["severidad"] == "BLOQUEA"})


def F0(r, p=None):
    return (r["diagnostico_por_perimetro"][p] if p else r["calculo_perimetro_declarado"])["flujo_sin_crecimiento"]


def cerca(a, b, tol=1e-9):
    return a is not None and abs(a - b) < tol


# ================================================================== N · la norma es un valor cerrado (H13) y no se mezcla
LN = libro(l4="IFRS (adoptadas por la Unión Europea)")
dN = decl(norma="NIIF", us=False, ppa=0)
dN["series"]["da_rou"] = serie(0)
rN = ev_(LN, dN)
paso("N · NIIF con el libro «IFRS (adoptadas por la Unión Europea)» (variante histórica registrada): F1-NORMA no salta", not salta(rN, "F1-NORMA"))
for l4, txt in (("US GAAP (no IFRS)", "H13: «US GAAP (no IFRS)» ya no pasa como NIIF"), ("Otro", "«Otro»"), ("IFRS y US GAAP", "un texto con las dos normas"), ("", "L4 vacío")):
    paso(f"N · NIIF declarada y libro con {txt}: F1-NORMA bloquea", bloquea(ev_(libro(l4=l4), dN), "F1-NORMA"), g(ev_(libro(l4=l4), dN), "F1-NORMA")[0]["detalle"][:90])
paso("N · mezcla: NIIF declarada y libro «US GAAP» → F1-NORMA (DATOS INVÁLIDOS, «mezcla de normas»)",
     bloquea(ev_(libro(), dN), "F1-NORMA") and "mezcla de normas" in g(ev_(libro(), dN), "F1-NORMA")[0]["detalle"])
rmz = ev_(libro(l4="IFRS"), decl())
paso("N · mezcla: US_GAAP declarada y libro «IFRS» → F1-NORMA (DATOS INVÁLIDOS)", bloquea(rmz, "F1-NORMA") and g(rmz, "F1-NORMA")[0]["efecto"] == "DATOS INVÁLIDOS"
     and rmz["estado_propuesto"] == "pendiente_de_datos")
d_esp = decl()
d_esp["norma_contable"]["valor"] = "US GAAP"
paso("N · la declaración solo admite los identificadores NIIF y US_GAAP: «US GAAP» (con espacio) bloquea", bloquea(ev_(libro(), d_esp), "F1-NORMA"))
paso("N · libro «us gaap» (sin distinguir mayúsculas ni espacios de más) y «US GAAP» son el mismo valor de la lista", M.norma_del_libro({"Control maestro!L4": " us  gaap "}) == "US_GAAP"
     and M.norma_del_libro({"Control maestro!L4": "US GAAP"}) == "US_GAAP" and M.norma_del_libro({"Control maestro!L4": "US-GAAP"}) is None)
d_mix = copy.deepcopy(dN)
d_mix["arrendamientos_us_gaap"] = decl()["arrendamientos_us_gaap"]
paso("N · F1-US-MEZCLA: declaración NIIF con «arrendamientos_us_gaap» o con series de US GAAP → DATOS INVÁLIDOS", bloquea(ev_(LN, d_mix), "F1-US-MEZCLA")
     and bloquea(ev_(LN, dict(dN, series=dict(dN["series"], pagos_arr_operativo=serie(12)))), "F1-US-MEZCLA"))
r48 = ev_(libro(c48=3.0, C70=65.0), decl())
paso("N · F1-US-MEZCLA: US GAAP con intereses pagados «en financiación» (C48 = 3) → DATOS INVÁLIDOS (se restarían dos veces)", bloquea(r48, "F1-US-MEZCLA")
     and g(r48, "F1-US-MEZCLA")[0]["efecto"] == "DATOS INVÁLIDOS")
paso("N · con NIIF no aparece ninguna guarda F1-US-* ni el bloque us_gaap", not [x for x in rN["guardas"] if x["id"].startswith("F1-US")] and "us_gaap" not in rN)

# ================================================================== U1 · solo operativos, los dos tramos fuera de las filas 8 y 14
L1 = libro()
r1 = ev_(L1, decl("A0_total"))
paso("U1 · solo operativos, tramos fuera de las filas: A0 da 68 = FCF base (el alquiler ya está una vez en el EBIT y en el CFO)", cerca(F0(r1), 68) and cerca(F0(r1, "A2_propio"), 68))
paso("U1 · ninguna guarda bloquea: utilizable (libro V6.3, A0), sin hipótesis ni condición", r1["utilizable_para_conclusion"] and not bloquean(r1) and "condicionada" not in r1
     and "CONDICIONADA" not in r1["rotulo"], str(bloquean(r1)))
paso("U1 · K3b: alquiler contado una vez (operativos); K3 conforme", r1["K3"]["K3b_alquiler_contado"] == "una vez" and r1["K3"]["K3b_por_clase"] == {"operativos": "una vez"}
     and r1["K3"]["conforme"] is True)
paso("U1 · F1-SERIES examina las series de US GAAP y las cuatro citas de clasificación en su página", not salta(r1, "F1-SERIES")
     and r1["F1_SERIES"]["citas_de_clasificacion_comprobadas"] == 4, g(r1, "F1-SERIES")[0]["detalle"][:120])
r1b = ev_(L1, decl("A2_propio"))
paso("U1 · con A2 declarado en un libro V6.3 solo bloquea F1-LIBRO (el libro calcula A0): límite declarado, como en NIIF", bloquean(r1b) == ["F1-LIBRO"] and cerca(F0(r1b), 68))
rsin = ev_(L1, decl("A0_total", op=False, P=None, Lc=None, pasivo=None))
paso("U1 · US GAAP sin arrendamientos de ninguna clase (declarado con su evidencia): A0 utilizable; K3b «ninguna vez (sin arrendamientos)»",
     rsin["utilizable_para_conclusion"] and rsin["K3"]["K3b_alquiler_contado"] == "ninguna vez (sin arrendamientos)", str(bloquean(rsin)))

# ================================================================== U2 · operativos + financieros (los financieros, como NIIF 16)
L2 = libro(ebit=63.0, da=25.0, C70=62.0, C49=5.0, princ=5.0)
d2 = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5)
r2 = ev_(L2, d2)
paso("U2 · operativos + financieros: A2 da 62 = FCF base; A0 da 57 (la amortización del derecho de uso financiero contada dos veces)", cerca(F0(r2), 62)
     and cerca(F0(r2, "A0_total"), 57))
paso("U2 · con A2 solo bloquea F1-LIBRO; K3b una vez en las dos clases; F1-US-C49 no salta (C49 = principal financiero publicado)",
     bloquean(r2) == ["F1-LIBRO"] and r2["K3"]["K3b_por_clase"] == {"operativos": "una vez", "financieros": "una vez"} and not salta(r2, "F1-US-C49"), str(bloquean(r2)))
r2a = ev_(L2, decl("A0_total", fin=True, rou_fin=5, fin_princ=5))
paso("U2 · con A0 bloquea V-F1a (financieros) y K3b dice «financieros: dos veces»", bloquea(r2a, "V-F1a") and bloquea(r2a, "F1-K3b")
     and r2a["K3"]["K3b_por_clase"]["financieros"] == "dos veces" and r2a["K3"]["K3b_por_clase"]["operativos"] == "una vez", r2a["K3"]["K3b_alquiler_contado"])
r2s = ev_(libro(ebit=63.0, da=25.0, C70=67.0, C49=0.0), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U9 · simétrica de los financieros: A2 con derecho de uso financiero y C49 = 0 → F1-M-SIM y F1-US-C49 (principal publicado omitido); K3b «financieros: ninguna vez»",
     bloquea(r2s, "F1-M-SIM") and bloquea(r2s, "F1-US-C49") and "se omitiría" in g(r2s, "F1-US-C49")[0]["detalle"] and r2s["K3"]["K3b_por_clase"]["financieros"] == "ninguna vez")
r2n = ev_(L2, decl("A2_propio", fin=True, rou_fin=5))
paso("U2 · financieros sin su principal publicado declarado → F1-US-C49 INCOMPLETO (no se puede descartar que C49 lleve pagos operativos)",
     bloquea(r2n, "F1-US-C49") and g(r2n, "F1-US-C49")[0]["efecto"] == "INCOMPLETO")
r2i = ev_(L2, decl("A2_propio", fin=False, rou_fin=5))
paso("U2 · «financieros.existen = false» con importes en da_rou → F1-US-DESGLOSE DATOS INVÁLIDOS (incoherencia)", bloquea(r2i, "F1-US-DESGLOSE")
     and g(r2i, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")

# ================================================================== U3 · la D&A (fila 8) lleva la amortización del derecho de uso operativo
L3 = libro(da=30.0)
r3 = ev_(L3, decl("A0_total", ub_am="fila_8", a8=10))
paso("U3 · derecho de uso operativo dentro de la D&A con A0: F1-US-DA bloquea (MODELO NO APLICABLE); A0 daría 58 frente a la caja 68", bloquea(r3, "F1-US-DA")
     and g(r3, "F1-US-DA")[0]["efecto"] == "MODELO NO APLICABLE" and cerca(F0(r3, "A0_total"), 58))
paso("U3 · K3b «operativos: dos veces» (F1-K3b bloquea) y K3c también (reinversión media −10 con ventas estables)", bloquea(r3, "F1-K3b")
     and r3["K3"]["K3b_por_clase"] == {"operativos": "dos veces"} and bloquea(r3, "F1-K3c") and r3["K3"]["conforme"] is False)
paso("U3 · el puente K3 de A0 señala 10 de doble cómputo (clase doble_computo)",
     cerca(r3["diagnostico_por_perimetro"]["A0_total"]["K3"]["doble_computo_por_clase_a_la_escala_del_año_base"]["doble_computo"], 10))
r3b = ev_(L3, decl("A2_propio", ub_am="fila_8", a8=10))
paso("U3 · con A2 la excluye de D_X ((1a) b): 68; alquiler una vez; solo bloquea F1-LIBRO en un libro V6.3", cerca(F0(r3b), 68) and bloquean(r3b) == ["F1-LIBRO"]
     and r3b["K3"]["K3b_alquiler_contado"] == "una vez", str(bloquean(r3b)))
r3c = ev_(L3, decl("A2_propio", ub_am="fila_8"))
paso("U3 · ubicación «fila_8» sin su serie da_rou_operativo: F1-US-DESGLOSE INCOMPLETO y el perímetro no es calculable (vacío ≠ 0)", bloquea(r3c, "F1-US-DESGLOSE")
     and bloquea(r3c, "F1-PERIMETRO") and r3c["calculo_perimetro_declarado"] is None and r3c["estado_propuesto"] == "pendiente_de_datos")
r3d = ev_(L3, decl("A2_propio", a8=10))
paso("U3 · importes en da_rou_operativo con la amortización declarada fuera de la fila 8 → incoherencia (DATOS INVÁLIDOS)", bloquea(r3d, "F1-US-DESGLOSE")
     and g(r3d, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
r9 = ev_(L3, decl("A2_propio", ub_am="fila_8", a8=10, P=0))
paso("U9 · simétrica de los operativos: amortización excluida de D_X sin pagos dentro del CFO (pagos declarados a cero) → F1-US-SIM (FUERA DEL DOMINIO); K3b «ninguna vez»",
     bloquea(r9, "F1-US-SIM") and g(r9, "F1-US-SIM")[0]["efecto"] == "FUERA DEL DOMINIO" and r9["K3"]["K3b_por_clase"]["operativos"] == "ninguna vez")

# ================================================================== U4 · C49 con pagos de arrendamientos operativos (ya están en el CFO)
L4 = libro(C70=56.0, C49=12.0, princ=12.0)
r4 = ev_(L4, decl("A0_total"))
paso("U4 · C49 = 12 sin arrendamientos financieros: F1-US-C49 bloquea (DATOS INVÁLIDOS: los pagos operativos se restan dos veces); FCF base 56 frente a 68",
     bloquea(r4, "F1-US-C49") and g(r4, "F1-US-C49")[0]["efecto"] == "DATOS INVÁLIDOS" and "dos veces" in g(r4, "F1-US-C49")[0]["detalle"] and cerca(F0(r4), 56))
paso("U4 · K3a no lo ve (C49 y la fila 17 llevan el mismo error) pero K3b sí: «operativos: dos veces»", not salta(r4, "F1-K3a") and bloquea(r4, "F1-K3b")
     and r4["K3"]["K3b_por_clase"] == {"operativos": "dos veces"})
r4b = ev_(libro(ebit=63.0, da=25.0, C70=50.0, C49=17.0, princ=17.0), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U4 · con financieros: C49 = 17 frente a 5 de principal financiero publicado → exceso de 12 (pagos operativos): bloquea; operativos dos veces, financieros una",
     bloquea(r4b, "F1-US-C49") and "12.0" in g(r4b, "F1-US-C49")[0]["detalle"] and r4b["K3"]["K3b_por_clase"] == {"operativos": "dos veces", "financieros": "una vez"})
r4c = ev_(libro(ebit=63.0, da=25.0, C70=62.0, C49=5.004, princ=5.004), decl("A2_propio", fin=True, rou_fin=5, fin_princ=5))
paso("U4 · tolerancia de redondeo: C49 = 5,004 frente a 5 de principal (≤ 0,005) no salta", not salta(r4c, "F1-US-C49"))

# ================================================================== U5 · desglose operativo/financiero ausente
r5 = ev_(L1, decl("A0_total", us=False))
paso("U5 · US GAAP sin «arrendamientos_us_gaap»: F1-US-DESGLOSE (INCOMPLETO) → pendiente_de_datos; ya no es un límite del modelo por F1-NORMA",
     bloquea(r5, "F1-US-DESGLOSE") and g(r5, "F1-US-DESGLOSE")[0]["efecto"] == "INCOMPLETO" and r5["estado_propuesto"] == "pendiente_de_datos" and not salta(r5, "F1-NORMA"))
paso("U5 · sin el desglose K3b no afirma nada («no evaluable») y K3 no es conforme", "no evaluable" in r5["K3"]["K3b_alquiler_contado"] and r5["K3"]["conforme"] is False)
for nombre, d_ in (("sin decir si hay financieros", decl(fin=None)), ("sin decir si hay operativos", decl(op=None)),
                   ("sin la ubicación de la variación del pasivo", decl(ub_pas=None)), ("sin la ubicación de la amortización", decl(ub_am=None)),
                   ("sin los pagos operativos", decl(P=None)), ("sin el coste lineal (D-US2: la diferencia tiene que quedar a la vista)", decl(Lc=None))):
    rr = ev_(L1, d_)
    paso(f"U5 · {nombre}: F1-US-DESGLOSE bloquea (INCOMPLETO)", bloquea(rr, "F1-US-DESGLOSE") and g(rr, "F1-US-DESGLOSE")[0]["efecto"] == "INCOMPLETO",
         g(rr, "F1-US-DESGLOSE")[0]["detalle"][:110])
r5p = ev_(L1, decl(pasivo=None))
paso("U5 · motor A sin el pasivo operativo del último ejercicio: no bloquea (el motor A no resta deuda); F1-US-PUENTE avisa de que el puente no se puede comprobar",
     r5p["utilizable_para_conclusion"] and g(r5p, "F1-US-PUENTE")[0]["severidad"] == "AVISO", g(r5p, "F1-US-PUENTE")[0]["detalle"][:110])
r5h = ev_(libro(dwc=10.0), decl("A0_total", ub_pas="fila_14", ajuste={y: 10 for y in ANIOS[-3:]}))
paso("U5 · el importe que se retira del circulante hace falta en la ventana de f y en los años H–L del ancla: declarado solo en la ventana → INCOMPLETO",
     bloquea(r5h, "F1-US-DESGLOSE") and "2021" in g(r5h, "F1-US-DESGLOSE")[0]["detalle"] and "2022" in g(r5h, "F1-US-DESGLOSE")[0]["detalle"])
d5r = decl()
d5r["arrendamientos_us_gaap"]["registro"] = {"fecha": "2026-11-18", "persona": "", "motivo": "x"}
paso("U5 · «arrendamientos_us_gaap» sin registro (fecha, persona, motivo) → bloquea: lo declara la persona, no el agente", bloquea(ev_(L1, d5r), "F1-US-DESGLOSE"))
d5u = decl()
d5u["arrendamientos_us_gaap"]["operativos"]["variacion_pasivo"]["ubicacion"] = "fila_8"
paso("U5 · ubicación no admitida (la variación del pasivo no puede estar en la fila 8) → DATOS INVÁLIDOS", g(ev_(L1, d5u), "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
d5x = decl()
del d5x["arrendamientos_us_gaap"]["financieros"]["cita"]
paso("U5 · «financieros.existen = false» sin su evidencia (documento, página y cita) → INCOMPLETO: la ausencia también se documenta",
     bloquea(ev_(L1, d5x), "F1-US-DESGLOSE") and "financieros" in g(ev_(L1, d5x), "F1-US-DESGLOSE")[0]["detalle"])
d5e = decl()
del d5e["arrendamientos_us_gaap"]["operativos"]["amortizacion_rou"]["cita"]
paso("U5 · clasificación sin su cita literal → INCOMPLETO", bloquea(ev_(L1, d5e), "F1-US-DESGLOSE") and "cita" in g(ev_(L1, d5e), "F1-US-DESGLOSE")[0]["detalle"])

# ================================================================== U6 · la variación del pasivo, sola dentro de la fila 14
L6 = libro(dwc=10.0)
r6 = ev_(L6, decl("A0_total", ub_pas="fila_14", ajuste=10))
paso("U6 · variación del pasivo sola en la fila 14: el libro tal cual daría 78 (omite el alquiler); la capa la retira del circulante y da 68",
     cerca(L6["Historia!C58"], -0.01) and cerca(F0(r6), 68) and cerca(F0(r6, "A2_propio"), 68))
paso("U6 · ningún libro la retira: F1-LIBRO bloquea (límite declarado, con su salida) y es lo único que bloquea; la réplica del libro sigue conforme",
     bloquean(r6) == ["F1-LIBRO"] and "LÍMITE DECLARADO" in g(r6, "F1-LIBRO")[0]["detalle"] and "corrección registrada" in g(r6, "F1-LIBRO")[0]["detalle"]
     and not salta(r6, "F1-REPLICA") and r6["estado_propuesto"] == "no_entregable · limite_del_modelo", str(bloquean(r6)))
paso("U6 · K3b con el ajuste: una vez; el puente K3 muestra la partida retirada (−10) y cuadra",
     r6["K3"]["K3b_alquiler_contado"] == "una vez" and r6["calculo_perimetro_declarado"]["K3"]["identidad_cuadra"]
     and any("se retira del circulante" in ln["partida"] and cerca(ln["mm"], -10) for ln in r6["calculo_perimetro_declarado"]["K3"]["lineas"]))
r6b = ev_(L6, decl("A0_total", ub_pas="fila_14"))
paso("U6 · sin el importe declarado: F1-US-SIM (FUERA DEL DOMINIO: el alquiler se omitiría) y F1-US-DESGLOSE; K3b «operativos: ninguna vez»; no calculable",
     bloquea(r6b, "F1-US-SIM") and bloquea(r6b, "F1-US-DESGLOSE") and bloquea(r6b, "F1-K3b") and r6b["K3"]["K3b_por_clase"] == {"operativos": "ninguna vez"}
     and r6b["calculo_perimetro_declarado"] is None and r6b["estado_propuesto"] == "pendiente_de_datos")
r6c = ev_(L6, decl("A0_total", ub_pas="fila_14", ajuste=10), motor_libro="A")
L6p7 = libro(dwc=10.0, palancas=False)
r6p7 = ev_(L6p7, decl("A0_total", ub_pas="fila_14", ajuste=10))
paso("U6 · también en el paso 7 (sin palancas ni flujos en el libro) F1-LIBRO bloquea por el ajuste declarado", bloquea(r6p7, "F1-LIBRO") and bloquea(r6c, "F1-LIBRO"))
r6d = ev_(L1, decl("A0_total", ajuste=10))
paso("U6 · importes en circulante_arr_operativo sin ningún tramo declarado dentro de la fila 14 → incoherencia (DATOS INVÁLIDOS)",
     g(r6d, "F1-US-DESGLOSE")[0]["efecto"] == "DATOS INVÁLIDOS")
r6e = ev_(libro(dwc=-10.0), decl("A0_total", ub_am="fila_14", ajuste=-10))
paso("U6 · la amortización (baja del activo) sola en la fila 14 (−10): tal cual se contaría dos veces (58); retirada con su signo, 68",
     cerca(F0(r6e), 68) and bloquean(r6e) == ["F1-LIBRO"])
r6f = ev_(libro(dwc=-10.0), decl("A0_total", ub_am="fila_14"))
paso("U6 · …y sin su importe: F1-US-DA (dos veces) y K3b «operativos: dos veces»", bloquea(r6f, "F1-US-DA") and r6f["K3"]["K3b_por_clase"] == {"operativos": "dos veces"})

# ================================================================== U7 · los dos tramos dentro de la fila 14 · D · D-US2 (se cuentan los pagos)
r7 = ev_(L1, decl("A0_total", ub_am="fila_14", ub_pas="fila_14"))
paso("U7 · los dos tramos dentro de la fila 14 con coste lineal = pagos: lo que se retira (pagos − coste) es 0; 68; utilizable sin tocar nada",
     cerca(F0(r7), 68) and r7["utilizable_para_conclusion"] and r7["us_gaap"]["operativos"]["retirado_del_circulante_medio"] == 0.0, str(bloquean(r7)))
# coste lineal 12, pagos 11: EBIT 68, CFO 89, FCF base 69. Con los dos tramos netos en la fila 14, la fila 14 lleva pagos − coste = −1
L7 = libro(dwc=-1.0, C70=69.0)
r7b = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=11, Lc=12))
paso("D · D-US2 con los dos tramos netos en la fila 14 y pagos 11 ≠ coste 12: el libro tal cual contaría el coste lineal (68); la capa cuenta los pagos (69)",
     cerca(L7["Historia!C58"], 0.0) and cerca(F0(r7b), 69) and r7b["us_gaap"]["operativos"]["retirado_derivado_de_pagos_menos_coste_lineal_en"] == ANIOS)
paso("D · …y como el libro no retira esa diferencia, F1-LIBRO bloquea (límite declarado); la diferencia coste − pagos (+1) queda a la vista en F1-US-BASE",
     bloquean(r7b) == ["F1-LIBRO"] and salta(r7b, "F1-US-BASE") and not bloquea(r7b, "F1-US-BASE")
     and cerca(r7b["us_gaap"]["diferencia_coste_lineal_menos_pagos"]["coste_menos_pagos_medio"], 1.0), g(r7b, "F1-US-BASE")[0]["detalle"][:150])
r7c = ev_(L7, decl("A0_total", ub_am="fila_14", ub_pas="fila_14", P=11, Lc=12, ajuste=-1))
paso("D · con la línea neta publicada declarada (−1) manda el dato: mismo resultado (69) sin derivar nada", cerca(F0(r7c), 69)
     and r7c["us_gaap"]["operativos"]["retirado_derivado_de_pagos_menos_coste_lineal_en"] == [])
L7d = libro(C70=69.0)
r7d = ev_(L7d, decl("A0_total", P=11, Lc=12))
paso("D · tramos fuera de las filas con pagos 11 ≠ coste 12: se cuentan los pagos sin ajuste (69 = FCF base); utilizable; la diferencia (+1) a la vista, sin bloquear",
     cerca(F0(r7d), 69) and r7d["utilizable_para_conclusion"] and "+1.000" in g(r7d, "F1-US-BASE")[0]["detalle"]
     and g(r7d, "F1-US-BASE")[0]["severidad"] == "INFORMA", g(r7d, "F1-US-BASE")[0]["detalle"][:160])

# ================================================================== H · hipótesis general declarada D-US1 (tramos que la empresa no publica)
rh = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"))
paso("H · D-US1: los dos tramos «no_publicada» → se suponen fuera de las filas 8 y 14; no bloquea: utilizable para una conclusión CONDICIONADA",
     rh["utilizable_para_conclusion"] and "CONDICIONADA" in rh["rotulo"] and rh["condicionada"]["hipotesis"] == "D-US1" and cerca(F0(rh), 68), rh["rotulo"][:140])
paso("H · la regla lleva su registro (18-nov-2026, persona responsable, DECISIONES_PARA_EL_USUARIO.md) y es una hipótesis, no un dato",
     rh["condicionada"]["registro"]["fecha"] == "2026-11-18" and "DECISIONES_PARA_EL_USUARIO.md" in rh["condicionada"]["registro"]["motivo"]
     and "no es un dato" in rh["condicionada"]["texto"] and rh["us_gaap"]["operativos"]["hipotesis_D_US1_en"] == ["amortizacion_rou", "variacion_pasivo"])
gh = g(rh, "F1-US-HIPOTESIS")[0]
ch = rh["condicionada"]["cota"]
k_pas = next(k for k in ch if k.startswith("si la variación del pasivo"))
k_am = next(k for k in ch if k.startswith("si la amortización"))
paso("H · F1-US-HIPOTESIS avisa (no bloquea) con la cota: si la variación del pasivo estuviera sola en la fila 14, el flujo bajaría como máximo en los pagos "
     "(−12; −17,6 %); si la amortización estuviera en la fila 8, subiría como máximo en el coste lineal (+12)",
     gh["salta"] and gh["severidad"] == "AVISO" and cerca(ch[k_pas]["variacion_maxima_del_flujo_sin_crecimiento_mm"], -12)
     and cerca(ch[k_am]["variacion_maxima_del_flujo_sin_crecimiento_mm"], 12) and cerca(ch[k_pas]["variacion_maxima_del_flujo_sin_crecimiento_%"], -17.647, 1e-3), gh["detalle"][:200])
vp = ch[k_pas]["por_escenario (valor presente de los flujos a la r del libro, sin exceso de caja ni quiebra)"]
# réplica independiente de la cota en valor presente (NORMAL): Δf = pagos ÷ ventas medias; ΔVP = −Δf·[Σ V_t/(1+r)^t + V_10(1+g)/((r−g)(1+r)^10)]
Vt, v = [], 1000.0
for t in range(1, 11):
    v *= 1 + (0.03 if t <= 5 else 0.03 - (0.03 - 0.02) * (t - 5) / 5)
    Vt.append(v)
kk = sum(Vt[t] / 1.09 ** (t + 1) for t in range(10)) + Vt[-1] * 1.02 / ((0.09 - 0.02) * 1.09 ** 10)
paso("H · la cota también en valor presente de los flujos, por escenario (NORMAL: −0,012 × Σ ventas descontadas; réplica independiente)",
     set(vp) == {"MALO", "NORMAL", "BUENO"} and cerca(vp["NORMAL"]["variacion_maxima_del_valor_presente_de_los_flujos_mm"], -0.012 * kk, 1e-3)
     and vp["NORMAL"]["variacion_maxima_%"] < 0, f"{vp['NORMAL']} · réplica {-0.012 * kk:.3f}")
paso("H · F1-SERIES comprueba que la página citada del estado de flujos existe y no muestra una línea propia del arrendamiento operativo (2 páginas examinadas)",
     not salta(rh, "F1-SERIES") and rh["F1_SERIES"]["paginas_sin_linea_propia_del_arrendamiento_operativo"] == 2)
rh3 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", pagina_np=3))
paso("H · donde la empresa publica la línea manda el dato: «no_publicada» citando una página que muestra «Non-cash lease expense» → F1-SERIES DATOS INVÁLIDOS",
     bloquea(rh3, "F1-SERIES") and g(rh3, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS" and "manda el dato" in g(rh3, "F1-SERIES")[0]["detalle"]
     and not rh3["utilizable_para_conclusion"], g(rh3, "F1-SERIES")[0]["detalle"][:160])
rh9 = ev_(L1, decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada", pagina_np=9))
paso("H · «no_publicada» citando una página que no existe → F1-SERIES DATOS INVÁLIDOS", bloquea(rh9, "F1-SERIES") and g(rh9, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS")
dhs = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
del dhs["arrendamientos_us_gaap"]["operativos"]["variacion_pasivo"]["pagina"]
paso("H · «no_publicada» sin la página del estado de flujos examinada → F1-US-DESGLOSE INCOMPLETO", bloquea(ev_(L1, dhs), "F1-US-DESGLOSE"))
rh1 = ev_(L6, decl("A0_total", ub_am="no_publicada", ub_pas="fila_14", ajuste=10, pagina_np=2))
paso("H · un tramo publicado y otro no: el publicado se trata con su dato (pasivo en la fila 14: se retira; 68) y la hipótesis vale solo para el otro (cota solo al alza)",
     cerca(F0(rh1), 68) and rh1["condicionada"]["tramos"] == ["amortizacion_rou"] and not any(k.startswith("si la variación del pasivo") for k in rh1["condicionada"]["cota"])
     and any(k.startswith("si la amortización") for k in rh1["condicionada"]["cota"]))
paso("H · sin hipótesis (tramos declarados con su línea) F1-US-HIPOTESIS no salta y el rótulo no dice «condicionada»", not salta(r1, "F1-US-HIPOTESIS")
     and "condicionada" not in r1["rotulo"].lower())

# ================================================================== P · puente de deuda (motor B) y motor A
LP = libro(fila22=100.0, fila23=50.0)
rp = ev_(LP, decl("A0_total", pasivo=50))
gp = g(rp, "F1-US-PUENTE")[0]
pu = rp["us_gaap"]["puente_de_deuda"]
paso("P · motor A con 50 de pasivo operativo en la fila 23: F1-US-PUENTE informa (el motor A no resta deuda) y no bloquea; deuda coherente de un puente = 100",
     gp["salta"] and gp["severidad"] == "INFORMA" and rp["utilizable_para_conclusion"] and cerca(pu["deuda_del_puente_coherente"], 100)
     and cerca(pu["deuda_del_puente_del_libro_C64"], 150), gp["detalle"][:130])
LB = libro(fila22=100.0, fila23=50.0, motor="B")
rb = ev_(LB, decl("A0_total", pasivo=50))
paso("P · motor B con US GAAP: F1 evalúa solo el puente; el pasivo operativo dentro de la fila 23 se restaría además del EBIT → F1-US-PUENTE BLOQUEA (límite declarado)",
     rb["aplica"] is True and "puente" in rb["alcance"] and bloquean(rb) == ["F1-US-PUENTE"] and rb["estado_propuesto"] == "no_entregable · limite_del_modelo"
     and "motor B" in rb["rotulo"] and "dos veces" in rb["K3"]["K3b_alquiler_contado"], rb["rotulo"][:120])
rb0 = ev_(libro(fila22=100.0, fila23=0.0, motor="B"), decl("A0_total", pasivo=0))
paso("P · motor B con la fila 23 sin pasivo operativo (0 declarado): utilizable; alquiler una vez", rb0["utilizable_para_conclusion"] and rb0["K3"]["K3b_alquiler_contado"] == "una vez"
     and "motor B utilizable" in rb0["rotulo"], str(bloquean(rb0)))
rbf = ev_(libro(fila22=100.0, fila23=30.0, motor="B"), decl("A0_total", fin=True, rou_fin=5, fin_princ=5, pasivo=0))
paso("P · motor B con 30 de pasivo por arrendamientos FINANCIEROS en la fila 23 y 0 operativo: no bloquea (los financieros sí son deuda del puente: 130)",
     rbf["utilizable_para_conclusion"] and cerca(rbf["us_gaap"]["puente_de_deuda"]["deuda_del_puente_coherente"], 130))
rbs = ev_(LB, decl("A0_total", us=False))
paso("P · motor B con US GAAP y sin declaración de arrendamientos → F1-US-DESGLOSE (pendiente_de_datos): nunca un puente silencioso",
     bloquea(rbs, "F1-US-DESGLOSE") and rbs["estado_propuesto"] == "pendiente_de_datos")
rbu = ev_(LB, decl("A0_total", ub_am=None, ub_pas=None, pasivo=50))
paso("P · motor B: no exige las ubicaciones de los tramos en el flujo (son del motor A); con el pasivo declarado, lo que bloquea es el puente",
     bloquean(rbu) == ["F1-US-PUENTE"], str(bloquean(rbu)))
rbx = ev_(LB, decl("A0_total", pasivo=60))
paso("P · pasivo operativo declarado (60) mayor que la fila 23 (50) → DATOS INVÁLIDOS", bloquea(rbx, "F1-US-PUENTE") and g(rbx, "F1-US-PUENTE")[0]["efecto"] == "DATOS INVÁLIDOS")
rbn = M.evaluar(libro(l4="IFRS", motor="B"), dN)
paso("P · motor B con NIIF: F1 sigue sin aplicar (T11 no cambia)", rbn["aplica"] is False and not rbn["bloquea"] and rbn["guardas"] == [])
rbm = ev_(libro(l4="US GAAP", motor="B"), dN)
paso("P · motor B, libro US GAAP y declaración NIIF → se evalúa (por el libro) y F1-NORMA bloquea por mezcla de normas", rbm["aplica"] is True and bloquea(rbm, "F1-NORMA"))

# ================================================================== S · fuentes de las series y citas de US GAAP (F1-SERIES)
dS = decl("A0_total")
dS["series"]["pagos_arr_operativo"]["2025"].update({"valor_fuente": -12, "signo": -1, "tratamiento": "publicado entre paréntesis"})   # literal «12» y valor −12
rS = ev_(L1, dS)
paso("S · serie de US GAAP con «valor_fuente» distinto de la cifra publicada con su signo → F1-SERIES DATOS INVÁLIDOS (R415-SIGNO)",
     bloquea(rS, "F1-SERIES") and g(rS, "F1-SERIES")[0]["efecto"] == "DATOS INVÁLIDOS" and "pagos_arr_operativo.2025" in g(rS, "F1-SERIES")[0]["detalle"])
dS2 = decl("A0_total")
cS = fuentes(dS2)
TMP.append(cS)
dS2["arrendamientos_us_gaap"]["operativos"]["amortizacion_rou"]["cita"] = "Amortization of operating lease right-of-use assets"
rS2 = M.evaluar(L1, dS2, carpeta=cS)
paso("S · cita de una clasificación que no está en la página citada → F1-SERIES DATOS INVÁLIDOS", bloquea(rS2, "F1-SERIES") and "la cita no está" in g(rS2, "F1-SERIES")[0]["detalle"])
dS3 = decl("A0_total")
dS3["arrendamientos_us_gaap"]["financieros"]["cita"] = "no"
rS3 = ev_(L1, dS3)
paso("S · cita de menos de diez caracteres → F1-SERIES INCOMPLETO (no identifica una línea)", bloquea(rS3, "F1-SERIES") and g(rS3, "F1-SERIES")[0]["efecto"] == "INCOMPLETO")
rS4 = M.evaluar(L1, decl("A0_total"))
paso("S · sin la carpeta del expediente (fuentes no examinadas) → F1-SERIES bloquea (INCOMPLETO): un «utilizable» exige las fuentes", bloquea(rS4, "F1-SERIES")
     and rS4["estado_propuesto"] == "pendiente_de_datos")
dS5 = decl("A0_total", ub_pas="fila_14", ajuste=10)
dS5["series"]["circulante_arr_operativo"]["2024"].update({"valor_fuente": 10, "signo": 1, "tratamiento": "ninguno", "literal": "10"})
uS5 = M.leer_us(dS5, ANIOS)
paso("S · la partida del circulante lleva el signo de la fila 14: «(10)» publicado con signo −1 es +10 (consume caja) y admite importes negativos",
     uS5["ajuste"][2025] == Fr(10) and M.leer_serie({"series": {"circulante_arr_operativo": serie(-3)}}, "circulante_arr_operativo", ANIOS, con_signo=True)[0][2025] == Fr(-3)
     and M.leer_serie({"series": {"da_rou_operativo": serie(-3)}}, "da_rou_operativo", ANIOS)[0] == {})

# ================================================================== F · F1-US-FILAS: las ubicaciones declaradas frente a lo que la fase 1 sumó en las filas 8 y 14
def con_partes(d, da=("Depreciation and amortization",), wc=("Accounts receivable", "Accounts payable and accrued liabilities")):
    """Carpeta de expediente con la fuente y un fase1_partes/AR_2025.json sintético (componentes de la fila 8 y de la fila 14)."""
    c = fuentes(d)
    TMP.append(c)
    os.makedirs(os.path.join(c, "fase1_partes"))
    comp = lambda xs: {"actual": [{"concepto": x, "impreso": "1", "pagina": 2, "linea": x + "   1   2"} for x in xs], "anterior": [], "cero": None}  # noqa: E731
    json.dump({"anio": 2025, "archivo": "10K_2025.txt", "partidas": {"da": comp(da), "circulante_lineas": comp(wc)}},
              open(os.path.join(c, "fase1_partes", "AR_2025.json"), "w", encoding="utf-8"))
    return c


dF = decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada")
rF = M.evaluar(L1, dF, carpeta=con_partes(dF))
paso("F · fase1_partes sin líneas de arrendamiento en las filas 8 y 14: F1-US-FILAS no salta y la hipótesis D-US1 se sostiene (utilizable, condicionada)",
     not salta(rF, "F1-US-FILAS") and rF["utilizable_para_conclusion"] and "CONDICIONADA" in rF["rotulo"], g(rF, "F1-US-FILAS")[0]["detalle"][:120])
rF2 = M.evaluar(L1, dF, carpeta=con_partes(dF, wc=("Accounts receivable", "Operating lease liabilities")))
paso("F · «no_publicada» cuando la fase 1 sumó «Operating lease liabilities» en la fila 14: F1-US-FILAS bloquea (DATOS INVÁLIDOS: manda el dato); no utilizable",
     bloquea(rF2, "F1-US-FILAS") and g(rF2, "F1-US-FILAS")[0]["efecto"] == "DATOS INVÁLIDOS" and "manda el dato" in g(rF2, "F1-US-FILAS")[0]["detalle"]
     and not rF2["utilizable_para_conclusion"], g(rF2, "F1-US-FILAS")[0]["detalle"][:170])
dF3 = decl("A0_total")
rF3 = M.evaluar(L1, dF3, carpeta=con_partes(dF3, wc=("Prepaid expenses, ROU assets and other assets", "Accounts payable")))
paso("F · tramos declarados «fuera de las filas» con cita, pero la fila 14 suma «Prepaid expenses, ROU assets and other assets» → F1-US-FILAS bloquea",
     bloquea(rF3, "F1-US-FILAS"))
dF4 = decl("A0_total")
rF4 = M.evaluar(L1, dF4, carpeta=con_partes(dF4, da=("Depreciation and amortization, including amortization of operating lease right-of-use assets",)))
paso("F · la fila 8 suma una línea que nombra el derecho de uso y la amortización no está declarada dentro de la fila 8 → F1-US-FILAS bloquea", bloquea(rF4, "F1-US-FILAS")
     and "fila 8" in g(rF4, "F1-US-FILAS")[0]["detalle"])
dF5 = decl("A0_total", ub_pas="fila_14", ajuste=10)
rF5 = M.evaluar(libro(dwc=10.0), dF5, carpeta=con_partes(dF5, wc=("Accounts receivable", "Operating lease liabilities")))
paso("F · con la línea declarada dentro de la fila 14 (y su importe) no hay contradicción: F1-US-FILAS no salta", not salta(rF5, "F1-US-FILAS") and bloquean(rF5) == ["F1-LIBRO"])
paso("F · sin fase1_partes el contraste no se puede hacer: informa y no bloquea", g(r1, "F1-US-FILAS")[0]["severidad"] == "INFORMA" and r1["utilizable_para_conclusion"])
paso("F · con NIIF no existe (nada cambia)", not g(rN, "F1-US-FILAS"))

# ================================================================== V631 · libro V6.3.1 F1: la fila 86 lleva financieros + operativos dentro de la fila 8
dV = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5, ub_am="fila_8", a8=10)
cel = V631.celdas(dV, ANIOS)
paso("V631 · celdas: la fila 86 del libro lleva la suma (5 financieros + 10 operativos dentro de la fila 8 = 15) y su procedencia nombra las dos series",
     cel["Historia!C85"] == "A2_propio" and all(cel[f"Historia!{c}86"] == 15.0 for c in COLS) and "da_rou + series.da_rou_operativo" in cel["Historia!M86"])
dV0 = decl("A2_propio", fin=True, rou_fin=5, fin_princ=5)
paso("V631 · celdas: sin operativos dentro de la fila 8 la fila 86 es la de los financieros (5); con una ubicación sin declarar queda VACÍA (vacío ≠ 0)",
     all(V631.celdas(dV0, ANIOS)[f"Historia!{c}86"] == 5.0 for c in COLS)
     and all(V631.celdas(decl("A2_propio", fin=True, rou_fin=5, ub_am=None), ANIOS)[f"Historia!{c}86"] is None for c in COLS))
dNi = copy.deepcopy(dN)
dNi["perimetro_reinversion"]["valor"] = "A1_sin_ROU"
dNi["series"]["da_rou"] = serie(7)
paso("V631 · celdas con NIIF: la fila 86 sigue siendo series.da_rou (sin cambio)", all(V631.celdas(dNi, ANIOS)[f"Historia!{c}86"] == 7.0 for c in COLS)
     and V631.celdas(dNi, ANIOS)["Historia!M86"].startswith("motor_a_f1.json · series.da_rou (documento"))


def libro_v631(base, per, rou8, ppa=0.0):
    """Libro V6.3.1 F1 sintético (paso 7, sin palancas): sección F1 de la Historia y f y ancla con D_X, como las fórmulas de la plantilla."""
    L = dict(base)
    L.update({"Historia!A84": "  PERÍMETRO F1 DE LA REINVERSIÓN · motor A (V6.3.1 F1)", "Historia!C85": per, "Historia!C89": per})
    dx = []
    for i, c in enumerate(COLS):
        L[f"Historia!{c}86"], L[f"Historia!{c}87"] = rou8, ppa
        dx.append(L[f"Historia!{c}8"] - (rou8 if per != "A0_total" else 0) - (ppa if per == "A2_propio" else 0))
        L[f"Historia!{c}88"] = dx[-1]
    k = lambda f: [L[f"Historia!{c}{f}"] for c in COLS]  # noqa: E731
    V, E, T, K, A, W = k(6), k(7), k(10), k(12), k(13), k(14)
    w = range(7, 10)
    L["Historia!C58"] = (sum(E[i] * (1 - T[i]) for i in w) / 3 - sum(K[i] - dx[i] + W[i] for i in w) / 3 - L["Historia!C70"]) / (sum(V[i] for i in w) / 3)
    den = sum(K[i] - dx[i] + W[i] + A[i] for i in range(5, 10))
    L["Historia!C53"] = (V[-1] - V[4]) / den if den > 0 else None
    return L


# EBIT 63 (el coste lineal y la amortización financiera ya están dentro); fila 8 = 20 propia + 5 financiera + 10 operativa = 35; FCF base 62
LV = libro_v631(libro(ebit=63.0, da=35.0, C70=62.0, C49=5.0, princ=5.0, palancas=False), "A2_propio", 15.0)
rV = ev_(LV, dV)
paso("V631 · el libro V6.3.1 tal cual calcula el caso «operativos dentro de la fila 8 + financieros» con A2 (62 = FCF base): F1-LIBRO no salta y nada bloquea (utilizable)",
     not salta(rV, "F1-LIBRO") and rV["libro_v631_f1"]["motivos"] == [] and rV["utilizable_para_conclusion"] and not salta(rV, "F1-REPLICA") and cerca(F0(rV), 62),
     f"{bloquean(rV)} · {rV.get('libro_v631_f1')}")
LVm = dict(LV, **{"Historia!L86": 5.0})
paso("V631 · si la fila 86 del libro no es la suma declarada (solo los financieros en 2025) → F1-LIBRO bloquea (el oráculo compara la serie)",
     bloquea(ev_(LVm, dV), "F1-LIBRO"))
LVh = libro_v631(libro(palancas=False), "A2_propio", 0.0)
rVh = ev_(LVh, decl("A2_propio", ub_am="no_publicada", ub_pas="no_publicada"))
paso("V631 · caso habitual con D-US1 (tramos no publicados) y A2 en el libro V6.3.1 tal cual: calculable, utilizable y CONDICIONADO",
     rVh["utilizable_para_conclusion"] and "CONDICIONADA" in rVh["rotulo"] and not salta(rVh, "F1-LIBRO") and cerca(F0(rVh), 68), str(bloquean(rVh)))
LV6 = libro_v631(libro(dwc=10.0, palancas=False), "A2_propio", 0.0)
rV6 = ev_(LV6, decl("A2_propio", ub_pas="fila_14", ajuste=10))
paso("V631 · variación del pasivo en la fila 14: el libro V6.3.1 no retira nada del circulante → F1-LIBRO bloquea (f del libro ≠ capa) y es lo único que bloquea",
     bloquean(rV6) == ["F1-LIBRO"] and "retirada del circulante" in g(rV6, "F1-LIBRO")[0]["detalle"] and cerca(F0(rV6), 68) and not salta(rV6, "F1-REPLICA"), str(bloquean(rV6)))

# ================================================================== G13 · con crecimiento e impuestos
V13 = [1000 * 1.05 ** i for i in range(10)]
dao = [0.02 * v for v in V13]
cap = [dao[i] + 0.5 * (V13[i] - (V13[i - 1] if i else V13[0] / 1.05)) for i in range(10)]
eb = [0.10 * v for v in V13]                                   # margen después del alquiler operativo (coste = pago = 3 % de las ventas)
fcf = [eb[i] * 0.75 + dao[i] - cap[i] for i in range(10)]      # CFO − capex: el pago ya está dentro del CFO
P13, A13, PR13 = ({y: 0.03 * V13[i] for i, y in enumerate(ANIOS)}, {y: 0.025 * V13[i] for i, y in enumerate(ANIOS)}, {y: 0.025 * V13[i] for i, y in enumerate(ANIOS)})
caja0 = 0.075 * V13[-1]
L13 = libro(ventas=V13, ebit=eb, da=dao, tau=0.25, capex=cap, C70=sum(fcf[-3:]) / 3)
r13 = ev_(L13, decl("A2_propio", P=P13, Lc=P13), con_fuentes=False)
paso("G13 · crecimiento 5 % y τ 25 %, tramos fuera: A2 da la caja sostenible a crecimiento cero (7,5 % de las ventas del año base); ancla S2C = 2,0",
     cerca(F0(r13), caja0, 1e-6) and cerca(r13["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0), f"{F0(r13):.6f} frente a {caja0:.6f}")
L13a = libro(ventas=V13, ebit=eb, da=[dao[i] + A13[y] for i, y in enumerate(ANIOS)], tau=0.25, capex=cap, C70=sum(fcf[-3:]) / 3)
r13a = ev_(L13a, decl("A2_propio", P=P13, Lc=P13, ub_am="fila_8", a8=A13), con_fuentes=False)
paso("G13 · con la amortización operativa (2,5 % de las ventas) dentro de la fila 8: A2 da la misma caja; A0 la infravalora en esa amortización a la escala del año base",
     cerca(F0(r13a), caja0, 1e-6) and cerca(caja0 - F0(r13a, "A0_total"), sum(A13[y] for y in ANIOS[-3:]) / sum(V13[-3:]) * V13[-1], 1e-6)
     and cerca(r13a["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0))
L13b = libro(ventas=V13, ebit=eb, da=dao, tau=0.25, capex=cap, dwc=[PR13[y] for y in ANIOS], C70=sum(fcf[-3:]) / 3)
r13b = ev_(L13b, decl("A2_propio", P=P13, Lc=P13, ub_pas="fila_14", ajuste=PR13), con_fuentes=False)
f_libro = L13b["Historia!C58"]
paso("G13 · con la variación del pasivo (2,5 % de las ventas) sola en la fila 14: retirada, A2 da la caja sostenible y el ancla 2,0; el libro tal cual la sobrevaloraría en ese importe",
     cerca(F0(r13b), caja0, 1e-6) and cerca(r13b["calculo_perimetro_declarado"]["ancla_s2c_E4"], 2.0)
     and cerca(V13[-1] * (0.075 - f_libro) - caja0, sum(PR13[y] for y in ANIOS[-3:]) / sum(V13[-3:]) * V13[-1], 1e-6))
L14 = libro(tau=0.25, C70=51.0)
r14 = ev_(L14, decl("A0_total"))
paso("G13 · estable con τ 25 %: EBIT 68, impuesto 17, FCF base 51 → A0 da 51; utilizable", cerca(F0(r14), 51) and r14["utilizable_para_conclusion"])

# ================================================================== NIIF · no cambia
paso("NIIF · sin arrendamientos ni PPA: A0 = la V6.3; utilizable; mismas guardas que antes (ninguna F1-US-*)", rN["utilizable_para_conclusion"] and cerca(F0(rN), 68)
     and rN["K3"]["K3b_alquiler_contado"] == "ninguna vez (sin arrendamientos)" and "K3b_por_clase" not in rN["K3"])
LNi = libro(ebit=70.0, da=30.0, C70=68.0, C49=10.0, princ=10.0, c48=2.0, l4="IFRS")
dNa = copy.deepcopy(dN)
dNa["perimetro_reinversion"]["valor"] = "A1_sin_ROU"
dNa["perimetro_palancas_s2c"]["valor"] = dNa["perimetro_roic"]["valor"] = "A1_sin_ROU"
dNa["series"]["da_rou"] = serie(10)
dNa["conciliacion_fcf_base"] = [{"componente": "C48", "importe": -2, "partida": "interés de caja de los arrendamientos dentro de C48", "fuente": {"documento": DOC, "pagina": 1}}]
rNa = ev_(LNi, dNa)
paso("NIIF · caso T5 (derecho de uso 10, principal en C49): A1 = 68 y A0 = 58; solo bloquea F1-LIBRO; K3b «una vez»; la versión de la capa nombra US GAAP",
     cerca(F0(rNa, "A1_sin_ROU"), 68) and cerca(F0(rNa, "A0_total"), 58) and bloquean(rNa) == ["F1-LIBRO"] and rNa["K3"]["K3b_alquiler_contado"] == "una vez"
     and "US GAAP" in rNa["version"], str(bloquean(rNa)))
paso("NIIF · rou_fila8 con NIIF es series.da_rou; un resultado NIIF no lleva bloque us_gaap, condición ni hipótesis", M.rou_fila8(dNa, ANIOS) == {y: Fr(10) for y in ANIOS}
     and "us_gaap" not in rNa and "condicionada" not in rNa and "hipótesis" not in rNa["rotulo"])

# ================================================================== EX · exigencia, vigencia y gancho del pipeline
tmp = tempfile.mkdtemp(prefix="f1_us_ex_")
TMP.append(tmp)
paso("EX · con el motor A, un libro US GAAP exige F1 aunque no muestre arrendamientos (C49 = 0, filas 17 y 23 a cero); uno NIIF sin arrendamientos, no",
     M.exigido(tmp, L=libro()) and not M.exigido(tmp, L=libro(l4="IFRS")) and not M.arrendamientos_en_el_libro(libro()))
paso("EX · con el motor B, F1 se exige solo con US GAAP (por el libro o por la declaración): exigido_puente", M.exigido_puente(tmp, L=libro(motor="B"))
     and not M.exigido_puente(tmp, L=libro(l4="IFRS", motor="B")))


def escribir_xlsx(L, ruta):
    import openpyxl
    wb = openpyxl.Workbook()
    for h in ("Historia", "Análisis", "Palancas", "Motor", "Diagnóstico V6", "Control maestro"):
        wb.create_sheet(h)
    for k_, v_ in L.items():
        if "!" in k_:
            h, c = k_.split("!")
            wb[h][c] = v_
    wb.save(ruta)


def cli(c, libro_, motor=None, origen=None):
    return subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", libro_]
                          + (["--motor", motor] if motor else []) + (["--libro-origen", origen] if origen else []), capture_output=True, text=True)


try:
    import cierre_v2 as CIE
    c = os.path.join(tmp, "EmpresaUS")
    os.makedirs(os.path.join(c, "recalc"))
    pl_b, pl_b0 = os.path.join(tmp, "b.xlsx"), os.path.join(tmp, "b0.xlsx")
    escribir_xlsx(LB, pl_b)
    escribir_xlsx(libro(fila22=100.0, fila23=0.0, motor="B"), pl_b0)
    ev_libro = os.path.join(c, "EmpresaUS_v63_evaluada.xlsx")
    shutil.copy(pl_b, ev_libro)
    st = {"motor": "B", "estado_pendiente": "concluido", "historial": [], "paso": 12}
    json.dump(st, open(os.path.join(c, "estado_pipeline.json"), "w"))
    v0 = M.vigencia(c, motor="B")
    paso("EX · vigencia con el motor B y libro US GAAP: F1 exigido; sin evaluación, un cierre «concluido» se rechaza", v0["exigido"] is True and v0["vigente"] is False
         and "sin evaluación F1" in str(CIE.motivo_f1(c, st)), str(v0.get("motivo")))
    dB = decl("A0_total", pasivo=50)
    fuentes(dB, c)
    json.dump(dB, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    rc = cli(c, pl_b, "B", ev_libro)
    vb = M.vigencia(c, motor="B")
    paso("EX · CLI con el motor B y el pasivo operativo en la fila 23: código 4 (límite del modelo); vigente y no utilizable; el cierre «concluido» se rechaza",
         rc.returncode == 4 and vb["vigente"] is True and vb["utilizable"] is False and "concluido" in str(CIE.motivo_f1(c, st)), f"código {rc.returncode} · {rc.stdout.strip()[-100:]}")
    shutil.copy(pl_b0, ev_libro)
    dB0 = decl("A0_total", pasivo=0)
    fuentes(dB0, c)
    json.dump(dB0, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    rc = cli(c, pl_b0, "B", ev_libro)
    paso("EX · con la fila 23 sin pasivo operativo: código 0; vigente y utilizable; el cierre no tiene objeción F1; sin el motor en el estado se toma del resultado (B)",
         rc.returncode == 0 and M.vigencia(c, motor="B")["utilizable"] is True and CIE.motivo_f1(c, st) is None and M.vigencia(c)["motor"] == "B",
         f"código {rc.returncode} · {rc.stdout.strip()[-100:]}")
    json.dump(dict(st, motor="B"), open(os.path.join(c, "estado_pipeline.json"), "w"))
    cn = os.path.join(tmp, "EmpresaNIIF")
    os.makedirs(cn)
    escribir_xlsx(libro(l4="IFRS", motor="B"), os.path.join(cn, "EmpresaNIIF_v63_evaluada.xlsx"))
    paso("EX · vigencia con el motor B y libro NIIF: no exigido («el motor no es el A»), como antes", M.vigencia(cn, motor="B")["exigido"] is False
         and M.vigencia(cn, motor="B")["motivo"] == "el motor no es el A" and CIE.motivo_f1(cn, {"motor": "B", "estado_pendiente": "concluido"}) is None)
    # el gancho del pipeline, ejecutado: Pipeline.motor_a_f1 con el motor B
    import pipeline as PL
    fin_ = []
    Pp = PL.Pipeline.__new__(PL.Pipeline)
    Pp.c, Pp.E, Pp.st = c, "EmpresaUS", {"motor": "B", "historial": [], "paso": 7}
    Pp.estado_path = os.path.join(tmp, "estado_pipeline_prueba.json")
    Pp.terminar = lambda estado, tipo, detalle, paso_, **k: fin_.append((estado, tipo, paso_, detalle))
    t0 = Pp.motor_a_f1(pl_b0, 7)
    paso("EX · gancho del pipeline con el motor B y US GAAP: evalúa el puente y deja seguir cuando es utilizable", t0 is False and not fin_
         and (Pp.st.get("motor_a_f1") or {}).get("bloquea") is False)
    shutil.copy(pl_b, ev_libro)
    json.dump(dB, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    fuentes(dB, c)
    json.dump(dB, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    t4 = Pp.motor_a_f1(pl_b, 7)
    paso("EX · gancho con el motor B y pasivo operativo en la fila 23: termina en no_entregable · limite_del_modelo y el detalle nombra el motor B",
         t4 is True and fin_[-1][:2] == ("no_entregable", "limite_del_modelo") and "motor B · F1" in fin_[-1][3] and "F1-US-PUENTE" in fin_[-1][3], str(fin_[-1:])[:200])
    Pp.c, Pp.E = cn, "EmpresaNIIF"
    paso("EX · gancho con el motor B y NIIF: no actúa (como antes)", Pp.motor_a_f1(os.path.join(cn, "EmpresaNIIF_v63_evaluada.xlsx"), 7) is False)
    # CLI con el motor A
    ca = os.path.join(tmp, "EmpresaUSA")
    os.makedirs(ca)
    pl_a, pl_a6 = os.path.join(tmp, "a.xlsx"), os.path.join(tmp, "a6.xlsx")
    escribir_xlsx(L1, pl_a)
    escribir_xlsx(L6, pl_a6)
    for nombre, d_, lib, esperado in (("U1 utilizable", decl("A0_total"), pl_a, 0), ("desglose ausente", decl("A0_total", us=False), pl_a, 3),
                                      ("ajuste del circulante que ningún libro calcula", decl("A0_total", ub_pas="fila_14", ajuste=10), pl_a6, 4),
                                      ("hipótesis D-US1", decl("A0_total", ub_am="no_publicada", ub_pas="no_publicada"), pl_a, 0)):
        fuentes(d_, ca)
        json.dump(d_, open(os.path.join(ca, "motor_a_f1.json"), "w", encoding="utf-8"))
        rc = cli(ca, lib, "A")
        md = open(os.path.join(ca, M.RESULTADO_MD), encoding="utf-8").read() if os.path.exists(os.path.join(ca, M.RESULTADO_MD)) else ""
        paso(f"CLI · motor A · {nombre}: código {esperado}; el informe .md lleva la sección de US GAAP", rc.returncode == esperado and "## US GAAP (ASC 842)" in md,
             f"código {rc.returncode} · {rc.stdout.strip()[-110:]}")
    paso("CLI · con la hipótesis D-US1 la salida dice CONDICIONADA", "CONDICIONADA" in rc.stdout)
finally:
    for t in TMP:
        shutil.rmtree(t, ignore_errors=True)

n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} pruebas del motor A F1 con US GAAP PASAN")
sys.exit(0 if n_ok == len(R) else 1)
