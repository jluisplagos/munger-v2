"""Recálculo independiente · revisión dirigida a P1–P4 · propuesta de decisiones F1 · Elis.

Script de revisión, de solo lectura. No importa ningún módulo del autor: lee el CSV de cifras verificadas con el
módulo estándar `csv`, reconstruye las partidas con sus propios identificadores, calibra f, recalcula el tipo de
cada año y el de cinco años, y reimplementa el motor A desde `v6/docs/Convenciones_financieras_V6_3.md` (§1–§3 y §10).
No calcula valores por acción ni adopta nada: son comprobaciones de las cifras que da la propuesta.

Tres clases de entrada, que se rotulan en la salida:
  [CSV]     cifra del CSV verificado del autor (commit congelado);
  [LIBRO]   celda del libro de Elis, leída en solo lectura con valores en caché (opcional: --libro);
  [LECTURA] cifra que el revisor ha leído en el PDF y que NO está en el CSV verificado. Cada una lleva documento,
            página PDF y literal; `evidencia_pdf.py` comprueba que el literal está en esa página.

Uso (desde esta carpeta):
  python3 -I recalculo_independiente.py --cifras <frente>/datos/cifras_fuente.csv \
      [--libro <base414>/.../Elis_v63_evaluada.xlsx] [--copia-autor <frente>/resultados/copia_investigacion_f1.json] \
      --salida ../resultados_revisor_p1_p4/recalculo_independiente.json \
      --informe ../resultados_revisor_p1_p4/recalculo_independiente.txt
Termina con 1 si alguna comparación con el libro o con la salida del autor no coincide.
"""
import argparse
import csv
import hashlib
import json
import sys
from decimal import Decimal, ROUND_HALF_EVEN, ROUND_HALF_UP
from fractions import Fraction as Fr
from pathlib import Path

VENTANA = (2023, 2024, 2025)
HORIZONTE = (2021, 2022, 2023, 2024, 2025)
# Edición de la que sale cada ejercicio: la publicación más reciente que lo contiene (se contrasta con la Historia).
SUF = {2025: "_2025", 2024: "_2024", 2023: "_FR_2023", 2022: "_U23_2022", 2021: "_U22_2021"}
SHA_LIBRO = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
# Palancas del libro (Palancas B14:D18). Constantes de este script; si se pasa --libro se comprueban contra él.
PALANCAS = {
    "MALO": dict(g15=Fr("0.02"), m_obj=Fr("0.105"), s2c=Fr("1"), g_inf=Fr("0.01"), roic=Fr("0.07")),
    "NORMAL": dict(g15=Fr("0.045"), m_obj=Fr("0.125"), s2c=Fr("1.2"), g_inf=Fr("0.02"), roic=Fr("0.10")),
    "BUENO": dict(g15=Fr("0.055"), m_obj=Fr("0.135"), s2c=Fr("1.5"), g_inf=Fr("0.025"), roic=Fr("0.12")),
}
# Cifras leídas por el revisor en los PDF; no están en el CSV verificado. Se usan solo en sensibilidades rotuladas.
LECTURA = {
    "actualizacion_earnout_2023": (Fr("12.4"), "DEU2024FR", 259, "12,4"),
    "actualizacion_earnout_2024": (Fr("5.6"), "DEU2024FR", 259, "5,6"),
    "actualizacion_earnout_2025": (Fr("0.7"), "URD2025", 313, "0.7"),
    "linea_fiscal_earnout_2023": (Fr("-15.8"), "DEU2024FR", 337, "(15,8)"),
    "linea_fiscal_earnout_2024": (Fr("0.8"), "URD2025", 392, "0.8"),
    "linea_fiscal_earnout_2025": (Fr("-0.2"), "URD2025", 392, "(0.2)"),
    "ajuste_earnout_2022": (Fr("2.4"), "URD2023", 302, "2.4"),
    "ajuste_earnout_2021": (Fr("-3.0"), "URD2022", 285, "(3.0)"),
    "adq_earnouts_y_diferidos_2023": (Fr("34.4"), "DEU2024FR", 288, "(34,4)"),
    "adq_earnouts_y_diferidos_2024": (Fr("93.9"), "URD2025", 342, "(93.9)"),
    "adq_earnouts_y_diferidos_2025": (Fr("23.3"), "URD2025", 341, "(23.3)"),
    "adq_lavartex_2023": (Fr("31.4"), "DEU2024FR", 288, "(31,4)"),
    "adq_lavartex_2024": (Fr("83.2"), "URD2025", 342, "(83.2)"),
    "adq_lavartex_2025": (Fr("19.7"), "URD2025", 341, "(19.7)"),
    "adq_otras_flujo_neto_2023": (Fr("35.3"), "DEU2024FR", 288, "(35,3)"),
    "adq_otras_flujo_neto_2024": (Fr("22.0"), "URD2025", 342, "(22.0)"),
    "adq_otras_flujo_neto_2025": (Fr("37.3"), "URD2025", 341, "(37.3)"),
}


def r(x, n=6):
    return round(float(x), n)


def leer_csv(ruta):
    filas = {}
    with open(ruta, encoding="utf-8", newline="") as fh:
        for f in csv.DictReader(fh, delimiter=";"):
            if f["tipo"] != "tabla":
                continue
            if f["id"] in filas:
                sys.exit("identificador repetido en el CSV: " + f["id"])
            filas[f["id"]] = f
    return filas


class Cifras:
    def __init__(self, ruta):
        self.filas = leer_csv(ruta)
        self.usadas = {}

    def __call__(self, ident, unidad="mm EUR"):
        f = self.filas[ident]
        if f["unidad"] != unidad:
            sys.exit(f"{ident}: unidad {f['unidad']!r}, se esperaba {unidad!r}")
        if f["edicion"] != "vigente":
            sys.exit(f"{ident}: edición {f['edicion']!r}")
        self.usadas[ident] = f"{f['doc']} p.{f['pagina']} «{f['literal']}»"
        return Fr(f["valor_publicado"])


def tipo_fila10(imp, bai):
    """Fila 10 de la Historia: gasto ÷ BAI con cuatro decimales. Se calcula con dos modos de redondeo; deben coincidir."""
    q = Decimal(imp.numerator) / Decimal(imp.denominator) / (Decimal(bai.numerator) / Decimal(bai.denominator))
    a = q.quantize(Decimal("0.0001"), rounding=ROUND_HALF_UP)
    b = q.quantize(Decimal("0.0001"), rounding=ROUND_HALF_EVEN)
    if a != b:
        sys.exit("el tipo cae en un empate de redondeo: hay que declarar el modo")
    return Fr(str(a))


def partidas(C, y):
    s = SUF[y]
    d = {"ventas": C("IS_VENTAS" + s), "fin": -C("IS_FIN" + s), "bai": C("IS_BAI" + s), "imp": -C("IS_IMP" + s)}
    d["ebit"] = d["bai"] + d["fin"]                       # definición de la Historia: BAI + gasto financiero neto
    d["capex"] = -C("CF_CAPINT" + s) - C("CF_CAPMAT" + s)
    d["dwc"] = -(sum(C(b + s) for b in ("CF_EXIS", "CF_CLI", "CF_OAC", "CF_PROV", "CF_PCON", "CF_OTRV")) + C("CF_EMPL" + s))
    d["da_total"], d["da_rou"], d["da_ppa"] = -C("DA_TOTAL" + s), -C("DA_ROU" + s), -C("DA_PPA" + s)
    d["adq"] = -C("CF_ADQ" + s)
    if y in VENTANA:
        d["cfo"], d["capnet"], d["sbc"] = C("CF_CFO" + s), -C("FCF_CAPNET" + s), C("CF_SBC" + s)
        d["intereses"], d["pagos_arr"], d["principal_arr"] = -C("CF_INT" + s), -C("CF_LEASE" + s), -C(f"LS_PRINC_PAS_{y}")
        d["nota46_earnout"], d["nota46_bajas"] = C("OOIE_EARN" + s), C("OOIE_PLUSV" + s)
        d["nota46_total"], d["nota46_monetarios"] = C("OOIE_TOT" + s), C("OOIE_MON" + s)
        d["efe_earnout"], d["efe_plusv"] = C("CF_EARN" + s), C("CF_PLUSV" + s)
        d["cobros_bajas"] = C("CF_DESMAT" + s) + C("CF_DESINT" + s)
    return d


def motor_a(V0, m0, tau, f, g15, m_obj, s2c, g_inf, roic):
    """Convenciones V6.3 §1–§3: g 1–5 de la palanca y 6–10 lineal hasta g∞; margen lineal a 5 años;
    flujo_t = V_t·[m_t(1−τ) − f] − (V_t − V_{t−1})/S2C; año 11 = V_10·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f]."""
    V, ant, flujos = [], V0, []
    for t in range(1, 11):
        g = g15 if t <= 5 else g15 - (g15 - g_inf) * Fr(t - 5, 5)
        v = ant * (1 + g)
        m = m0 + (m_obj - m0) * Fr(min(t, 5), 5)
        flujos.append(v * (m * (1 - tau) - f) - (v - ant) / s2c)
        V.append(v)
        ant = v
    anio11 = V[-1] * (1 + g_inf) * (m_obj * (1 - tau) * (1 - g_inf / roic) - f)
    return flujos, anio11, V


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--libro", type=Path)
    ap.add_argument("--copia-autor", type=Path, help="resultados/copia_investigacion_f1.json del autor (solo para comparar)")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    a = ap.parse_args()
    C = Cifras(a.cifras)
    A = {y: partidas(C, y) for y in HORIZONTE}
    V2020 = C("IS_VENTAS_U21_2020")
    t_teorico = C("TAX_TEOR_2025", "%") / 100
    out, lineas, fallos = {}, [], []

    def p(s=""):
        lineas.append(s)

    def comparar(nombre, mio, ref, tol=Fr(1, 10 ** 9)):
        ok = abs(Fr(mio) - Fr(ref)) <= tol
        if not ok:
            fallos.append(f"{nombre}: {float(mio)!r} frente a {float(ref)!r}")
        return ok

    media = lambda fn: sum(fn(A[y]) for y in VENTANA) / 3          # noqa: E731
    S, V0 = media(lambda d: d["ventas"]), A[2025]["ventas"]
    k = V0 / S

    def red3(x):
        """Convención «redondeo: 3» del registro de C46, C47 y C50."""
        return Fr(str((Decimal(x.numerator) / Decimal(x.denominator)).quantize(Decimal("0.001"), rounding=ROUND_HALF_UP)))

    C46, C47, C50 = red3(media(lambda d: d["cfo"])), red3(media(lambda d: d["capnet"])), red3(media(lambda d: d["sbc"]))
    C48 = media(lambda d: d["intereses"]) + media(lambda d: d["pagos_arr"] - d["principal_arr"])
    C49 = media(lambda d: d["principal_arr"])
    FCFB = C46 - C47 - C48 - C49 - C50
    PER = {"A0": lambda d: d["da_total"], "A1": lambda d: d["da_total"] - d["da_rou"],
           "A2": lambda d: d["da_total"] - d["da_rou"] - d["da_ppa"]}

    def calcular(d_ebit=None, d_bai=None, d_imp=None, tipo_fijo=False, horizonte_tau=HORIZONTE, fijo_en=()):
        """d_ebit, d_bai, d_imp: {año: variación}. tipo_fijo: la fila 10 no se recalcula (fijo_en: solo en esos años)."""
        d_ebit, d_bai, d_imp = d_ebit or {}, d_bai or {}, d_imp or {}
        tau, ebit = {}, {}
        for y in HORIZONTE:
            ebit[y] = A[y]["ebit"] + d_ebit.get(y, 0)
            if tipo_fijo or y in fijo_en:
                tau[y] = tipo_fila10(A[y]["imp"], A[y]["bai"])
            else:
                tau[y] = tipo_fila10(A[y]["imp"] + d_imp.get(y, 0), A[y]["bai"] + d_bai.get(y, 0))
        nopat = sum(ebit[y] * (1 - tau[y]) for y in VENTANA) / 3
        tau_p = sum(tau[y] for y in horizonte_tau) / len(horizonte_tau)
        m0 = ebit[2025] / V0
        res = {"tau": tau, "tau_proyeccion": tau_p, "m0": m0, "nopat_medio": nopat, "per": {}}
        for nombre, DX in PER.items():
            reinv = media(lambda d: d["capex"] - DX(d) + d["dwc"])
            f = (nopat - reinv - FCFB) / S
            esc = {n: motor_a(V0, m0, tau_p, f, **pal) for n, pal in PALANCAS.items()}
            res["per"][nombre] = {"f": f, "reinv": reinv, "F0": V0 * (m0 * (1 - tau_p) - f), "esc": esc}
        return res

    base = calcular()
    b0 = base["per"]["A0"]

    # ------------------------------------------------------------------ A. reproducción de la base
    p("A. BASE SIN AJUSTES [CSV]")
    p(f"  ventas medias {r(S)}; V0 {r(V0)}; k = V0/ventas medias {r(k, 9)}")
    p(f"  FCF base con la convención de registro: {r(FCFB)}  (C46 {r(C46, 3)}, C47 {r(C47, 3)}, C48 {r(C48)}, C49 {r(C49)}, C50 {r(C50, 3)})")
    p(f"  tipos fila 10, 2021–25: {[r(base['tau'][y], 4) for y in HORIZONTE]}; τ de 5 años {r(base['tau_proyeccion'], 6)}")
    p(f"  NOPAT medio {r(base['nopat_medio'])}; m0 {r(base['m0'], 9)}")
    for n in PER:
        q = base["per"][n]
        p(f"  {n}: reinversión media {r(q['reinv'])}; f {r(q['f'], 12)}; flujo sin crecimiento {r(q['F0'], 9)}")
    comparar("FCF base = 307,933", FCFB, Fr("307.933"))
    comparar("C48 = 108", C48, 108)
    comparar("f A0 = 0,041681455273796 (E9, T1)", b0["f"], Fr("0.041681455273796"), Fr(1, 10 ** 12))
    comparar("F0 A0 = 248,496395342656 (E9, T1)", b0["F0"], Fr("248.496395342656"))
    comparar("f A1 = 0,012624225323285 (E9, T2)", base["per"]["A1"]["f"], Fr("0.012624225323285"), Fr(1, 10 ** 12))
    comparar("f A2 = −0,006118601744165 (E9, T3)", base["per"]["A2"]["f"], Fr("-0.006118601744165"), Fr(1, 10 ** 12))
    out["A_base"] = {"FCF_base": r(FCFB), "C48": r(C48), "tau_2021_25": [r(base["tau"][y], 4) for y in HORIZONTE],
                     "tau_5": r(base["tau_proyeccion"], 6), "m0": r(base["m0"], 9), "nopat_medio": r(base["nopat_medio"]),
                     "por_perimetro": {n: {"f": r(base["per"][n]["f"], 12), "F0": r(base["per"][n]["F0"], 9),
                                           "reinversion_media": r(base["per"][n]["reinv"])} for n in PER}}

    libro = None
    if a.libro:
        h = hashlib.sha256(a.libro.read_bytes()).hexdigest()
        if h != SHA_LIBRO:
            sys.exit("huella del libro distinta: " + h)
        import openpyxl
        wb = openpyxl.load_workbook(a.libro, data_only=True, read_only=True)
        H, PL, MO, DG = wb["Historia"], wb["Palancas"], wb["Motor"], wb["Diagnóstico V6"]
        col = {2021: "H", 2022: "I", 2023: "J", 2024: "K", 2025: "L"}
        n_ok = 0
        for y in HORIZONTE:
            for fila, clave in ((6, "ventas"), (7, "ebit"), (8, "da_total"), (12, "capex"), (13, "adq"), (14, "dwc")):
                n_ok += comparar(f"Historia!{col[y]}{fila}", A[y][clave], Fr(str(H[f"{col[y]}{fila}"].value)), Fr(1, 10 ** 6))
            n_ok += comparar(f"Historia!{col[y]}10 (tipo)", base["tau"][y], Fr(str(H[f"{col[y]}10"].value)), Fr(1, 10 ** 9))
        n_ok += comparar("Historia!C52 (τ de 5 años)", base["tau_proyeccion"], Fr(str(H["C52"].value)), Fr(1, 10 ** 12))
        n_ok += comparar("Historia!C58 (f)", b0["f"], Fr(H["C58"].value), Fr(1, 10 ** 12))
        n_ok += comparar("Historia!C70 (FCF base)", FCFB, Fr(H["C70"].value))
        n_ok += comparar("Historia!C75 (NOPAT medio)", base["nopat_medio"], Fr(H["C75"].value), Fr(1, 10 ** 9))
        n_ok += comparar("Historia!C76 (reinversión media)", b0["reinv"], Fr(H["C76"].value), Fr(1, 10 ** 9))
        s2c_53 = (V0 - V2020) / sum(A[y]["capex"] - A[y]["da_total"] + A[y]["dwc"] + A[y]["adq"] for y in HORIZONTE)
        n_ok += comparar("Historia!C53 (S2C marginal de 5 años)", s2c_53, Fr(H["C53"].value), Fr(1, 10 ** 9))
        for n, c in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D")):
            for clave, fila in (("g15", 14), ("m_obj", 15), ("s2c", 16), ("g_inf", 17), ("roic", 18)):
                n_ok += comparar(f"Palancas!{c}{fila}", PALANCAS[n][clave], Fr(str(PL[f"{c}{fila}"].value)), Fr(0))
        for fila, n in ((6, "MALO"), (7, "NORMAL"), (8, "BUENO")):
            fl, a11, _ = b0["esc"][n]
            for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD"]):
                n_ok += comparar(f"Motor!{c}{fila}", fl[t], Fr(MO[f"{c}{fila}"].value))
            n_ok += comparar(f"Motor!BF{fila}", a11, Fr(MO[f"BF{fila}"].value))
        libro = {"sha256": h, "comparaciones_que_coinciden": n_ok,
                 "diagnostico_bloque_10": {
                     "rentabilidad_marginal_años_1_10 (fila 176)": [DG[f"{c}176"].value for c in "BCD"],
                     "ROIC_del_terminal (fila 177)": [DG[f"{c}177"].value for c in "BCD"],
                     "salto_en_el_año_11 (fila 178)": [DG[f"{c}178"].value for c in "BCD"],
                     "umbral_del_aviso (fila 179)": {"rotulo": DG["A179"].value, "valor": DG["C179"].value}}}
        p(f"  [LIBRO] {n_ok} comparaciones con celdas del libro coinciden (Historia 2021–25, C52, C53, C58, C70, C75, C76, palancas y 33 flujos del Motor)")
        out["A_libro"] = libro

    # ------------------------------------------------------------------ B. N1 y demás escenarios de la propuesta
    earn = {y: A[y]["nota46_earnout"] for y in VENTANA}
    bajas = {y: A[y]["nota46_bajas"] for y in VENTANA}
    tot46 = {y: A[y]["nota46_total"] for y in VENTANA}
    quitar = lambda dic, ys=VENTANA: {y: -dic[y] for y in ys}       # noqa: E731

    def fila(nombre, res):
        q = res["per"]["A0"]
        d = {"tau_2023_25": [r(res["tau"][y], 4) for y in VENTANA], "tau_proyeccion": r(res["tau_proyeccion"], 6),
             "m0": r(res["m0"], 6), "f_A0": r(q["f"], 9), "F0_A0": r(q["F0"], 3),
             "variacion_F0": r(q["F0"] - b0["F0"], 3),
             "de_ella": {"f": r(-V0 * (q["f"] - b0["f"]), 3),
                         "m0": r(V0 * (res["m0"] - base["m0"]) * (1 - res["tau_proyeccion"]), 3),
                         "tau": r(-V0 * base["m0"] * (res["tau_proyeccion"] - base["tau_proyeccion"]), 3)},
             "variacion_año11_MALO_NORMAL_BUENO": [r(q["esc"][n][1] - b0["esc"][n][1], 3) for n in PALANCAS],
             "variacion_NORMAL_años_1_5_10": [r(q["esc"]["NORMAL"][0][t] - b0["esc"]["NORMAL"][0][t], 3) for t in (0, 4, 9)]}
        igual = True
        for per in ("A1", "A2"):
            igual &= (res["per"][per]["F0"] - base["per"][per]["F0"]) == (q["F0"] - b0["F0"])
            for n in PALANCAS:
                igual &= (res["per"][per]["esc"][n][1] - base["per"][per]["esc"][n][1]) == (q["esc"][n][1] - b0["esc"][n][1])
        d["misma_variacion_en_A1_y_A2"] = igual
        p(f"  {nombre}")
        p(f"      τ 2023/24/25 {d['tau_2023_25']}  τ proy. {d['tau_proyeccion']}  m0 {d['m0']}  f {d['f_A0']}  F0 {d['F0_A0']}")
        p(f"      ΔF0 {d['variacion_F0']}  (f {d['de_ella']['f']} / m0 {d['de_ella']['m0']} / τ {d['de_ella']['tau']})"
          f"  Δ año 11 M/N/B {d['variacion_año11_MALO_NORMAL_BUENO']}  igual en A1 y A2: {igual}")
        return d

    p()
    p("B. ESCENARIOS DE LA PROPUESTA, RECALCULADOS [CSV]")
    esc = {
        "N1a · earnout 2023, tipo fijo": calcular(d_ebit=quitar(earn, (2023,)), tipo_fijo=True),
        "N1a · earnout 2023, no deducible": calcular(d_ebit=quitar(earn, (2023,)), d_bai=quitar(earn, (2023,))),
        "N1 · earnout 2023–25, tipo fijo": calcular(d_ebit=quitar(earn), tipo_fijo=True),
        "N1 · earnout 2023–25, no deducibles": calcular(d_ebit=quitar(earn), d_bai=quitar(earn)),
        "N2 · bajas 2025, tipo fijo": calcular(d_ebit=quitar(bajas, (2025,)), tipo_fijo=True),
        "N2 · bajas 2025, gravadas al tipo teórico": calcular(d_ebit=quitar(bajas, (2025,)), d_bai=quitar(bajas, (2025,)),
                                                            d_imp={2025: -t_teorico * bajas[2025]}),
        "N2 · bajas 2025, no gravadas": calcular(d_ebit=quitar(bajas, (2025,)), d_bai=quitar(bajas, (2025,))),
        "N2s · bajas 2023–25, tipo fijo": calcular(d_ebit=quitar(bajas), tipo_fijo=True),
        "N1 + N2 · earnout no deducible; bajas 2025 con tipo fijo": calcular(
            d_ebit={y: -earn[y] - (bajas[y] if y == 2025 else 0) for y in VENTANA},
            d_bai={y: -earn[y] for y in (2023, 2024)}, fijo_en=(2025,)),
        "N1 + N2 · earnout no deducible; bajas 2025 gravadas al tipo teórico": calcular(
            d_ebit={y: -earn[y] - (bajas[y] if y == 2025 else 0) for y in VENTANA},
            d_bai={y: -earn[y] - (bajas[y] if y == 2025 else 0) for y in VENTANA}, d_imp={2025: -t_teorico * bajas[2025]}),
        "N1 + N2 · earnout no deducible; bajas 2025 no gravadas": calcular(
            d_ebit={y: -earn[y] - (bajas[y] if y == 2025 else 0) for y in VENTANA},
            d_bai={y: -earn[y] - (bajas[y] if y == 2025 else 0) for y in VENTANA}),
        "Contraejemplo · nota 4.6 entera, tipo fijo": calcular(d_ebit=quitar(tot46), tipo_fijo=True),
    }
    out["B_escenarios"] = {n: fila(n, res) for n, res in esc.items()}
    n1 = esc["N1 · earnout 2023–25, no deducibles"]
    n1f = esc["N1 · earnout 2023–25, tipo fijo"]
    # valores de referencia de T16
    comparar("T16 τ de 5 años = 0,28234", n1["tau_proyeccion"], Fr("0.28234"), Fr(1, 10 ** 9))
    comparar("T16 m0 = 0,131379", n1["m0"], Fr("0.131379"), Fr(1, 10 ** 6) / 2)
    comparar("T16 f = 0,044900433", n1["per"]["A0"]["f"], Fr("0.044900433"), Fr(1, 10 ** 9))
    comparar("T16 F0 = 236,891", n1["per"]["A0"]["F0"], Fr("236.891"), Fr(1, 10 ** 3))
    comparar("T16 ΔF0 = −11,605", n1["per"]["A0"]["F0"] - b0["F0"], Fr("-11.605"), Fr(1, 10 ** 3))
    comparar("T16 Δ año 11 NORMAL = −18,609", n1["per"]["A0"]["esc"]["NORMAL"][1] - b0["esc"]["NORMAL"][1], Fr("-18.609"), Fr(1, 10 ** 3))

    if a.copia_autor:
        au = json.loads(a.copia_autor.read_text(encoding="utf-8"))["P3_normalizacion"]["escenarios"]
        pares = {"N1a · earnout 2023, tipo fijo": "N1a · earnout de 2023, tipo fijo (fila 10 sin cambios)",
                 "N1a · earnout 2023, no deducible": "N1a · earnout de 2023, no deducible (gasto sin cambios)",
                 "N1 · earnout 2023–25, tipo fijo": "N1 · ajustes de earnout 2023–25, tipo fijo",
                 "N1 · earnout 2023–25, no deducibles": "N1 · ajustes de earnout 2023–25, no deducibles",
                 "N2 · bajas 2025, tipo fijo": "N2 · bajas de 2025 (seguros), tipo fijo",
                 "N2 · bajas 2025, gravadas al tipo teórico": "N2 · bajas de 2025 (seguros), gravadas al tipo teórico",
                 "N2 · bajas 2025, no gravadas": "N2 · bajas de 2025 (seguros), no gravadas",
                 "N2s · bajas 2023–25, tipo fijo": "N2s · bajas de inmovilizado 2023–25 (simétrica), tipo fijo",
                 "N1 + N2 · earnout no deducible; bajas 2025 con tipo fijo":
                     "N1 + N2 conjuntos · earnout no deducible; bajas de 2025 tipo fijo",
                 "N1 + N2 · earnout no deducible; bajas 2025 gravadas al tipo teórico":
                     "N1 + N2 conjuntos · earnout no deducible; bajas de 2025 gravadas al tipo teórico",
                 "N1 + N2 · earnout no deducible; bajas 2025 no gravadas":
                     "N1 + N2 conjuntos · earnout no deducible; bajas de 2025 no gravadas",
                 "Contraejemplo · nota 4.6 entera, tipo fijo":
                     "Contraejemplo · regla literal «todo lo publicado como no recurrente» (nota 4.6 entera), tipo fijo"}
        n_ok = 0
        for mio, suyo in pares.items():
            m, s = out["B_escenarios"][mio], au[suyo]
            n_ok += comparar(f"autor · {mio} · τ5", Fr(str(m["tau_proyeccion"])), Fr(str(s["tau_5_anios"])), Fr(1, 10 ** 6))
            n_ok += comparar(f"autor · {mio} · f", Fr(str(m["f_A0"])), Fr(str(s["f_A0"])), Fr(1, 10 ** 9))
            n_ok += comparar(f"autor · {mio} · ΔF0", Fr(str(m["variacion_F0"])), Fr(str(s["variacion_flujo_sin_crecimiento"])), Fr(1, 10 ** 3))
            for i in range(3):
                n_ok += comparar(f"autor · {mio} · Δ año 11 [{i}]", Fr(str(m["variacion_año11_MALO_NORMAL_BUENO"][i])),
                                 Fr(str(s["variacion_terminal_MALO_NORMAL_BUENO"][i])), Fr(1, 10 ** 3))
                n_ok += comparar(f"autor · {mio} · τ [{i}]", Fr(str(m["tau_2023_25"][i])), Fr(str(s["tau_2023_25"][i])), Fr(0))
        p(f"  comparación con `copia_investigacion_f1.json` del autor: {n_ok} valores coinciden en {len(pares)} escenarios; "
          f"el autor tiene {len(au)}")
        out["B_comparacion_con_autor"] = {"valores_que_coinciden": n_ok, "escenarios_comparados": len(pares), "escenarios_del_autor": len(au)}

    # ------------------------------------------------------------------ C. qué parte de N1 depende de la convención del tipo
    p()
    p("C. N1: LA DIFERENCIA ENTRE «NO DEDUCIBLE» Y «TIPO FIJO» ES LA CONVENCIÓN DEL TIPO (E8.1), NO LA FISCALIDAD [CSV]")
    base_w = calcular(horizonte_tau=VENTANA)
    n1_w = calcular(d_ebit=quitar(earn), d_bai=quitar(earn), horizonte_tau=VENTANA)
    n1f_w = calcular(d_ebit=quitar(earn), tipo_fijo=True, horizonte_tau=VENTANA)
    c = {"con τ de proyección de 5 años (convención registrada)": {
            "no_deducible": r(n1["per"]["A0"]["F0"] - b0["F0"], 3), "tipo_fijo": r(n1f["per"]["A0"]["F0"] - b0["F0"], 3),
            "diferencia": r((n1["per"]["A0"]["F0"] - b0["F0"]) - (n1f["per"]["A0"]["F0"] - b0["F0"]), 3),
            "año11_NORMAL_no_deducible": r(n1["per"]["A0"]["esc"]["NORMAL"][1] - b0["esc"]["NORMAL"][1], 3),
            "año11_NORMAL_tipo_fijo": r(n1f["per"]["A0"]["esc"]["NORMAL"][1] - b0["esc"]["NORMAL"][1], 3)},
         "si el τ de proyección fuera la media de la ventana (los mismos tres años que calibran f)": {
            "no_deducible": r(n1_w["per"]["A0"]["F0"] - base_w["per"]["A0"]["F0"], 3),
            "tipo_fijo": r(n1f_w["per"]["A0"]["F0"] - base_w["per"]["A0"]["F0"], 3),
            "diferencia": r((n1_w["per"]["A0"]["F0"] - base_w["per"]["A0"]["F0"]) - (n1f_w["per"]["A0"]["F0"] - base_w["per"]["A0"]["F0"]), 3),
            "año11_NORMAL_no_deducible": r(n1_w["per"]["A0"]["esc"]["NORMAL"][1] - base_w["per"]["A0"]["esc"]["NORMAL"][1], 3),
            "año11_NORMAL_tipo_fijo": r(n1f_w["per"]["A0"]["esc"]["NORMAL"][1] - base_w["per"]["A0"]["esc"]["NORMAL"][1], 3)}}
    d_ebit_medio = sum(-earn[y] for y in VENTANA) / 3
    c["referencia antes de impuestos"] = {
        "EBIT medio de la ventana: variación": r(d_ebit_medio, 3),
        "EBIT 2025 − k·EBIT medio: variación (lo único que cambia en caja antes de impuestos)": r(-earn[2025] - k * d_ebit_medio, 3)}
    for kx, v in c.items():
        p(f"  {kx}: {v}")
    out["C_convencion_del_tipo"] = c

    # ------------------------------------------------------------------ D. límite de N1: actualización del earnout y 2021–22
    p()
    p("D. LO QUE LA RESPUESTA DEJA SIN CALCULAR EN N1 [LECTURA: cifras leídas por el revisor, no están en el CSV]")
    L = {kk: v[0] for kk, v in LECTURA.items()}
    act = {2023: L["actualizacion_earnout_2023"], 2024: L["actualizacion_earnout_2024"], 2025: L["actualizacion_earnout_2025"]}
    lin = {2023: L["linea_fiscal_earnout_2023"], 2024: L["linea_fiscal_earnout_2024"], 2025: L["linea_fiscal_earnout_2025"]}
    conc = {}
    for y in VENTANA:
        base_no_ded = -earn[y] + act[y]              # gasto no deducible del año: ajuste (con su signo) y actualización
        conc[y] = {"ajuste_nota_4_6": r(earn[y], 1), "actualizacion": r(act[y], 1), "gasto_no_deducible": r(base_no_ded, 1),
                   "al_25_83_%": r(-t_teorico * base_no_ded, 3), "linea_publicada": r(lin[y], 1),
                   "cuadra_al_redondeo": abs(-t_teorico * base_no_ded - lin[y]) <= Fr(1, 10)}
        p(f"  {y}: ajuste {r(earn[y], 1)}; actualización {r(act[y], 1)}; −25,83 % × ({r(-earn[y], 1)} + {r(act[y], 1)}) = "
          f"{r(-t_teorico * base_no_ded, 3)}; línea publicada {r(lin[y], 1)}; cuadra: {conc[y]['cuadra_al_redondeo']}")
    n1_act = calcular(d_ebit=quitar(earn), d_bai={y: -earn[y] + act[y] for y in VENTANA})
    d1 = fila("N1 + actualización del earnout fuera del BAI que da el tipo (EBIT como N1)", n1_act)
    e2122 = {2021: L["ajuste_earnout_2021"], 2022: L["ajuste_earnout_2022"]}
    n1_h = calcular(d_ebit=quitar(earn), d_bai={**{y: -earn[y] for y in VENTANA}, **{y: -e2122[y] for y in (2021, 2022)}})
    d2 = fila("N1 + los ajustes de earnout de 2021–22 fuera del BAI de su año (solo cambia el τ de 5 años)", n1_h)
    out["D_limite_de_N1"] = {"conciliacion_linea_fiscal": {str(y): v for y, v in conc.items()},
                             "N1_mas_actualizacion": d1, "N1_mas_2021_22": d2,
                             "variacion_frente_a_N1": {
                                 "actualizacion · F0": r(n1_act["per"]["A0"]["F0"] - n1["per"]["A0"]["F0"], 3),
                                 "actualizacion · año 11 NORMAL": r(n1_act["per"]["A0"]["esc"]["NORMAL"][1] - n1["per"]["A0"]["esc"]["NORMAL"][1], 3),
                                 "2021–22 · F0": r(n1_h["per"]["A0"]["F0"] - n1["per"]["A0"]["F0"], 3),
                                 "2021–22 · año 11 NORMAL": r(n1_h["per"]["A0"]["esc"]["NORMAL"][1] - n1["per"]["A0"]["esc"]["NORMAL"][1], 3)}}
    p(f"  frente a N1: {out['D_limite_de_N1']['variacion_frente_a_N1']}")

    # ------------------------------------------------------------------ E. diagnóstico 27,936
    p()
    p("E. DIAGNÓSTICO 27,936 Y SUS TRES DIFERENCIAS CON UNA REGLA [CSV]")
    e_f = media(lambda d: d["efe_earnout"]) * k
    pl_f = media(lambda d: d["efe_plusv"]) * k
    pl_m0 = bajas[2025] * (1 - base["tau_proyeccion"])
    dif_lineas = {y: r(A[y]["efe_plusv"] + bajas[y], 1) for y in VENTANA}
    out["E_diagnostico"] = {"earnout_y_otros_en_f (línea del EFE × k)": r(e_f, 3), "plusvalias_en_f (línea del EFE × k)": r(pl_f, 3),
                            "plusvalia_2025_en_m0 (25,7 × (1 − τ5))": r(pl_m0, 3), "suma": r(e_f + pl_f + pl_m0, 3),
                            "línea del EFE − línea de la nota 4.6, bajas (pérdidas ordinarias)": dif_lineas,
                            "línea del EFE + ajuste de la nota 4.6, earnout (otros no monetarios)": {y: r(A[y]["efe_earnout"] + earn[y], 1) for y in VENTANA},
                            "monetarios de la nota 4.6": {y: r(A[y]["nota46_monetarios"], 1) for y in VENTANA},
                            "cobros por bajas 2025 frente a plusvalía del EFE 2025": [r(A[2025]["cobros_bajas"], 1), r(-A[2025]["efe_plusv"], 1)]}
    for kx, v in out["E_diagnostico"].items():
        p(f"  {kx}: {v}")
    comparar("diagnóstico = 27,936", Fr(str(r(e_f + pl_f + pl_m0, 3))), Fr("27.936"), Fr(0))

    # ------------------------------------------------------------------ F. arrendamientos
    p()
    p("F. ARRENDAMIENTOS (1b) [CSV]")
    w_pag_m, w_pag_25 = media(lambda d: d["pagos_arr"]) / S, A[2025]["pagos_arr"] / V0
    w_rou_m, w_rou_25 = media(lambda d: d["da_rou"]) / S, A[2025]["da_rou"] / V0
    sens_pagos = -(w_pag_25 - w_pag_m) * V0
    sens_rou = (w_rou_25 - w_rou_m) * V0
    out["F_arrendamientos"] = {
        "pagos ÷ ventas: media y 2025 (%)": [r(100 * w_pag_m, 4), r(100 * w_pag_25, 4)],
        "amortización ROU ÷ ventas: media y 2025 (%)": [r(100 * w_rou_m, 4), r(100 * w_rou_25, 4)],
        "pagos: media escalada y 2025": [r(w_pag_m * V0, 6), r(A[2025]["pagos_arr"], 1)],
        "amortización ROU: media escalada (lo que devuelve f en A1 y A2) y 2025 (lo que lleva m0)": [r(w_rou_m * V0, 6), r(A[2025]["da_rou"], 1)],
        "F0 con el peso de 2025 en los pagos (A0, A1 y A2)": r(sens_pagos, 6),
        "F0 con el peso de 2025 también en la amortización ROU que devuelve f (solo A1 y A2)": r(sens_rou, 6),
        "F0 con el peso de 2025 en las dos cosas (A1 y A2)": r(sens_pagos + sens_rou, 6)}
    for kx, v in out["F_arrendamientos"].items():
        p(f"  {kx}: {v}")
    comparar("sensibilidad de pagos = −16,778237414", sens_pagos, Fr("-16.778237414016186"))

    # ------------------------------------------------------------------ G. PPA
    p()
    p("G. «PPA CONSTANTE» (2) [CSV]")
    p_f, p_m0 = media(lambda d: d["da_ppa"]) / S, A[2025]["da_ppa"] / V0
    out["G_PPA"] = {"PPA media ÷ ventas medias (%)": r(100 * p_f, 4), "PPA 2025 ÷ ventas 2025 (%)": r(100 * p_m0, 4),
                    "PPA que devuelve f sobre las ventas de 2025": r(p_f * V0, 3), "PPA de 2025 en m0": r(A[2025]["da_ppa"], 1),
                    "f devuelve de más (sube el flujo sin crecimiento de A2)": r((p_f - p_m0) * V0, 3),
                    "ROU: f devuelve de menos (baja el flujo sin crecimiento de A1 y A2)": r(-sens_rou, 3),
                    "los dos efectos de escala juntos en A2": r((p_f - p_m0) * V0 - sens_rou, 3)}
    for kx, v in out["G_PPA"].items():
        p(f"  {kx}: {v}")

    # ------------------------------------------------------------------ H. terminal
    p()
    p("H. ROIC DEL TERMINAL Y S2C (4a) [CSV + palancas]")
    tau5 = base["tau_proyeccion"]
    out["H_terminal"] = {}
    for n, pal in PALANCAS.items():
        fl, a11, V = b0["esc"][n]
        V10, V11 = V[-1], V[-1] * (1 + pal["g_inf"])
        nopat11 = V11 * pal["m_obj"] * (1 - tau5)
        inv_roic, inv_s2c = nopat11 * pal["g_inf"] / pal["roic"], (V11 - V10) / pal["s2c"]
        roic_motor = (1 + pal["g_inf"]) * pal["m_obj"] * (1 - tau5) * pal["s2c"]      # condición de la propuesta
        roic_conv = pal["m_obj"] * (1 - tau5) * pal["s2c"]                             # Convenciones §3 y Diagnóstico, bloque 10
        inv_con = lambda ro: nopat11 * pal["g_inf"] / ro                               # noqa: E731
        out["H_terminal"][n] = {
            "ROIC de la palanca": r(pal["roic"], 4),
            "ROIC que iguala la inversión del año 11 con ΔV/S2C: (1+g∞)·m_obj·(1−τ)·S2C": r(roic_motor, 6),
            "rentabilidad marginal de los años 1–10 según Convenciones §3: m_obj·(1−τ)·S2C": r(roic_conv, 6),
            "inversión del año 11 con el ROIC de la palanca": r(inv_roic, 3), "con ΔV/S2C": r(inv_s2c, 3),
            "diferencia": r(inv_roic - inv_s2c, 3),
            "comprobación: con el ROIC de la propuesta la inversión es ΔV/S2C": inv_con(roic_motor) == inv_s2c,
            "con el de Convenciones §3 la inversión es (1+g∞) veces ΔV/S2C": inv_con(roic_conv) == (1 + pal["g_inf"]) * inv_s2c,
            "salto del año 11 según el libro (puntos): m_obj·(1−τ)·S2C − ROIC": r(100 * (roic_conv - pal["roic"]), 4),
            "salto con la fórmula de la propuesta (puntos)": r(100 * (roic_motor - pal["roic"]), 4)}
        p(f"  {n}: {out['H_terminal'][n]}")
    if libro:
        for i, n in enumerate(PALANCAS):
            comparar(f"Diagnóstico V6 fila 176 {n}", PALANCAS[n]["m_obj"] * (1 - tau5) * PALANCAS[n]["s2c"],
                     Fr(libro["diagnostico_bloque_10"]["rentabilidad_marginal_años_1_10 (fila 176)"][i]), Fr(1, 10 ** 9))
        p(f"  [LIBRO] Diagnóstico V6, bloque 10 (filas 176–178): {libro['diagnostico_bloque_10']}")

    # ------------------------------------------------------------------ I. compras de sociedades
    p()
    p("I. COMPRAS DE SOCIEDADES (4b, 3a) [CSV; composición: LECTURA]")
    adq_m = media(lambda d: d["adq"])
    capex_m = media(lambda d: d["capex"])
    comp = {}
    for y in VENTANA:
        comp[y] = {"adquisiciones netas (EFE)": r(A[y]["adq"], 1),
                   "de ellas, earnouts y pagos aplazados": r(L[f"adq_earnouts_y_diferidos_{y}"], 1),
                   "de ellos, Lavartex (México, comprada en 2022)": r(L[f"adq_lavartex_{y}"], 1),
                   "flujo neto de «otras adquisiciones» (por debajo del umbral de «importantes»)": r(L[f"adq_otras_flujo_neto_{y}"], 1)}
    otras_m = sum(L[f"adq_otras_flujo_neto_{y}"] for y in VENTANA) / 3
    lav = sum(L[f"adq_lavartex_{y}"] for y in VENTANA)
    out["I_compras"] = {
        "adquisiciones netas, media 2023–25": r(adq_m, 3), "escalada a las ventas de 2025": r(adq_m * k, 3),
        "en % del FCF base": r(100 * adq_m / FCFB, 1),
        "capex propio medio": r(capex_m, 3), "capex propio + adquisiciones, media": r(capex_m + adq_m, 3),
        "composicion_por_año": {str(y): v for y, v in comp.items()},
        "Lavartex: pagos de 2023–25 (earnout y aplazados)": r(lav, 1),
        "«otras adquisiciones»: flujo neto medio 2023–25": r(otras_m, 3), "en % del FCF base (otras)": r(100 * otras_m / FCFB, 1),
        "crecimiento orgánico publicado 2021–25 (%)": {str(y): r(C(f"CREC_ORG_{y}", "%"), 1) for y in HORIZONTE},
        "crecimiento externo publicado 2022–25 (%)": {str(y): r(C(f"CREC_EXT_{y}", "%"), 1) for y in HORIZONTE if y != 2021}}
    for kx, v in out["I_compras"].items():
        p(f"  {kx}: {v}")

    out["fuentes"] = {"csv_sha256": hashlib.sha256(a.cifras.read_bytes()).hexdigest(), "cifras_csv_usadas": len(C.usadas),
                      "lecturas_del_revisor": {kk: {"valor": r(v[0], 1), "doc": v[1], "pagina_pdf": v[2], "literal": v[3]}
                                               for kk, v in LECTURA.items()}}
    out["resumen"] = {"fallos": fallos, "libro_contrastado": bool(libro), "comparado_con_el_autor": bool(a.copia_autor)}
    p()
    p(f"RESUMEN: fallos {len(fallos)}; cifras del CSV usadas {len(C.usadas)}; libro contrastado: {bool(libro)}; "
      f"comparado con la salida del autor: {bool(a.copia_autor)}")
    for f_ in fallos:
        p("  FALLO " + f_)
    a.salida.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    a.informe.write_text("\n".join(lineas) + "\n", encoding="utf-8")
    print("\n".join(lineas))
    return 1 if fallos else 0


if __name__ == "__main__":
    sys.exit(main())
