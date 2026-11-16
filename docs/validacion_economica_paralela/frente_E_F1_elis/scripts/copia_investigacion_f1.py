"""Copia de investigación · F1 · Elis (respuesta a la revisión de la propuesta, P2–P4). Solo lectura.

No es una entrada registrada, ni una política adoptada, ni una valoración. Recalcula con las mismas funciones de
`contraste_f1.py` (`Fuente`, `datos_anio`, `motor_a`, `leer_libro`) y solo con cifras verificadas lo que la revisión
de la propuesta (rama auditoria/revision-propuesta-f1, commit 1a07188) pide calcular conjuntamente:

  P3. Normalización de partidas de la ventana. Cada ajuste concreto, con su regla fiscal, cambia a la vez el EBIT de
      su año, el tipo de la fila 10 de ese año (gasto ÷ BAI, 4 decimales), f, el τ de 5 años y m0. El diagnóstico
      27,936 del contraste se reproduce como control: es una descomposición del cálculo conservado, no un ajuste.
  P2. «PPA constante»: la proporción de las ventas que devuelve f (perímetro A2) frente a la que lleva m0.
  P4. Peso del arrendamiento (media de la ventana como referencia de ensayo y sensibilidad 16,8) y compatibilidad
      del ROIC del terminal con S2C en las palancas del libro.
Correcciones V1–V11 de la revisión dirigida (8fcc7fd): efecto de escala de la amortización ROU y sensibilidad conjunta
del arrendamiento (V5); bloque 10 del diagnóstico del libro frente a la condición del terminal (V6); dependencia de N1
de la convención del tipo de proyección y de los ejercicios 2021–22 (V4); actualización del earnout (V3). Las cifras
que no están en el CSV verificado van rotuladas [LECTURA], con documento, página y literal; con --raiz, el script
comprueba que el literal está en su página del PDF (pdftotext) y que el PDF tiene la huella de datos/fuentes.json.

Los históricos, el CSV, la verificación y el libro no cambian. El libro se lee en solo lectura y con su huella; de él
se toman las palancas y el FCF base registrado (Historia!C70 = 307,933), que se contrasta con el cálculo.

Uso:
  python3 -I copia_investigacion_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
     --libro <ruta>/Elis_v63_evaluada.xlsx --contraste ../resultados/contraste_f1.json \
     --salida ../resultados/copia_investigacion_f1.json --informe ../resultados/copia_investigacion_f1.md
Termina con 1 si un control falla (reproducción de f, F0, flujos del libro o diagnóstico del contraste).
"""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("contraste_f1", Path(__file__).with_name("contraste_f1.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
VENT, HOR = C.VENTANA, C.HORIZONTE


def f6(x, n=6):
    return C.f6(x, n)


# [LECTURA] cifras que no están en el CSV verificado (revisión dirigida, 8fcc7fd, LECTURA de recalculo_independiente.py).
# Signo: ajustes de earnout como en la nota 4.6 (cargo negativo); actualización como gasto (positivo).
LECTURAS = {
    "actualizacion_earnout_2023": (Fr("12.4"), "DEU2024FR", 259, "12,4"),
    "actualizacion_earnout_2024": (Fr("5.6"), "DEU2024FR", 259, "5,6"),
    "actualizacion_earnout_2025": (Fr("0.7"), "URD2025", 313, "0.7"),
    "ajuste_earnout_2021": (Fr("-3.0"), "URD2022", 285, "(3.0)"),
    "ajuste_earnout_2022": (Fr("2.4"), "URD2023", 302, "2.4"),
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
# Pasajes que fundan las correcciones (V1 y V3); se buscan en la página del PDF con el texto normalizado.
PASAJES = [
    ("definición del crecimiento orgánico (V1)", "URD2025", 313, ["changes in the scope of consolidation of “major acquisitions” and",
                                                                  "revenue of more than €5.0 million in France and €3.0 million in"]),
    ("definición del crecimiento orgánico, 2024 (V1)", "DEU2024FR", 259, ["consolidation des « acquisitions importantes » et des « cessions"]),
    ("definición del crecimiento orgánico, 2023 (V1)", "URD2023", 267, ["the impacts of changes in the scope of consolidation of “major"]),
    ("compras pequeñas que consolidan la posición (V1)", "URD2025", 339, ["These bolt-on acquisitions help to consolidate the Group"]),
    ("actualización del earnout de México, 2025 y 2024 (V3)", "URD2025", 313, ["Accretion expense for the earnout pertaining to the acquisition in Mexico"]),
    ("actualización del earnout de México, 2024 y 2023 (V3)", "DEU2024FR", 259, ["Charge de désactualisation du complément de prix de l'acquisition réalisée au Mexique"]),
    ("pagos de earnouts dentro de las adquisiciones, 2025 (V3)", "URD2025", 341, ["CASH FLOWS FROM ACQUISITIONS", "Earnouts and deferred"]),
    ("pagos de earnouts dentro de las adquisiciones, 2024 (V3)", "URD2025", 342, ["CASH FLOWS FROM ACQUISITIONS", "Earnouts and deferred consideration"]),
    ("pagos de earnouts dentro de las adquisiciones, 2023 (V3)", "DEU2024FR", 288, ["FLUX DE TRÉSORERIE LIÉS AUX ACQUISITIONS", "Compléments de prix et paiements différés"]),
    ("liquidación del earnout de México (V3)", "URD2025", 352, ["settlement of the second installment and the balance of the Mexican earnout in 2024 and"]),
    ("ajustes de earnout de 2022 (V4)", "URD2023", 302, ["Earnout adjustments"]),
    ("ajustes de earnout de 2021 (V4)", "URD2022", 285, ["Earnout adjustments"]),
]


def _norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'")
    return re.sub(r"\s+", " ", s)


def comprobar_lecturas(raiz, fuentes):
    """Comprueba en el PDF (pdftotext -layout, una página) cada literal [LECTURA] y cada pasaje. Un solo extractor."""
    fu = json.loads(Path(fuentes).read_text(encoding="utf-8"))["fuentes"]
    paginas, huellas, res = {}, {}, {"literales": {}, "pasajes": [], "huellas_pdf": {}}

    def texto(doc, pag):
        if (doc, pag) not in paginas:
            ruta = Path(raiz) / fu[doc]["archivo"]
            if doc not in huellas:
                huellas[doc] = hashlib.sha256(ruta.read_bytes()).hexdigest() == fu[doc]["sha256"]
            out = subprocess.run(["pdftotext", "-layout", "-f", str(pag), "-l", str(pag), str(ruta), "-"],
                                 capture_output=True, text=True, check=True).stdout
            paginas[(doc, pag)] = _norm(out)
        return paginas[(doc, pag)]
    for k, (v, doc, pag, lit) in LECTURAS.items():
        res["literales"][k] = {"valor": f6(v, 1), "doc": doc, "pagina_pdf": pag, "literal": lit, "en_la_pagina": _norm(lit) in texto(doc, pag)}
    for nombre, doc, pag, frs in PASAJES:
        res["pasajes"].append({"pasaje": nombre, "doc": doc, "pagina_pdf": pag, "encontrado": all(_norm(x) in texto(doc, pag) for x in frs)})
    res["huellas_pdf"] = huellas
    return res


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--verificacion", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--contraste", required=True, type=Path, help="resultados/contraste_f1.json (diagnóstico conservado)")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    ap.add_argument("--raiz", type=Path, help="árbol munger_v2_r1 materializado: comprueba las [LECTURA] en los PDF")
    ap.add_argument("--fuentes", type=Path, default=Path(__file__).resolve().parent.parent / "datos" / "fuentes.json")
    a = ap.parse_args()
    F = C.Fuente(a.cifras, a.verificacion)
    A = {y: C.datos_anio(F, y) for y in HOR}
    L = C.leer_libro(a.libro)
    CT = json.loads(a.contraste.read_text(encoding="utf-8"))
    controles, errores = [], []

    def control(nombre, calc, ref, tol=Fr(0)):
        ok = abs(calc - ref) <= tol
        controles.append({"control": nombre, "calculado": f6(calc, 9), "referencia": f6(ref, 9), "ok": ok})
        if not ok:
            errores.append(nombre)

    def avg(fn):
        return sum(fn(A[y]) for y in VENT) / 3

    S_avg, V0 = avg(lambda d: d["ventas"]), A[2025]["ventas"]
    r3 = lambda x: Fr(round(x, 3)).limit_denominator(1000)   # noqa: E731  convención «redondeo: 3» del registro
    C46, C47, C50 = avg(lambda d: d["cfo"]), avg(lambda d: d["capnet"]), avg(lambda d: d["sbc"])
    C48 = avg(lambda d: d["int"]) + avg(lambda d: d["leasepay"] - d["ls_princ"])
    C49 = avg(lambda d: d["ls_princ"])
    C52 = r3(C46) - r3(C47) - C48 - C49 - r3(C50)
    control("FCF base registrado (Historia!C70) = cálculo con la convención de registro", C52, Fr(L["Historia!C70"]), Fr(1, 10 ** 9))
    control("C48 = 108", C48, Fr(108))
    pal = {}
    for nombre, col in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D")):
        pal[nombre] = {k: Fr(str(L[f"{h}!{col}{n}"])) for k, h, n in [("g15", "Palancas", 14), ("m_obj", "Palancas", 15),
                                                                         ("s2c", "Palancas", 16), ("roic", "Palancas", 18),
                                                                         ("g_inf", "Análisis", 68)]}
    PER = {"A0": lambda d: d["da_total"], "A1": lambda d: d["da_total"] - d["da_rou"], "A2": lambda d: d["d_own"]}
    t_teor = F.pct("TAX_TEOR_2025") / 100       # 25,83 %: tipo teórico de la matriz (URD 2025 p.392)

    def calcular(aj, aj_bai=None, tau_proy="cinco_años"):
        """aj: {año: [(ΔEBIT, regla)]}, regla ∈ {«tau_fijo», «no_deducible», «tipo_teorico»}. aj_bai: {año: ΔBAI} sin
        cambio del EBIT ni del gasto (partidas financieras no deducibles, como la actualización del earnout).
        tau_proy: «cinco_años» (convención registrada, C52) o «ventana» (sensibilidad de E8.1, no adoptada).
        Devuelve el cálculo conjunto con las mismas ecuaciones que el contraste (f, τ de proyección, m0 y motor A)."""
        aj_bai = aj_bai or {}
        tau, ebit = {}, {}
        for y in HOR:
            d = A[y]
            dE = sum((x for x, _ in aj.get(y, [])), Fr(0))
            reglas = {r for _, r in aj.get(y, [])}
            ebit[y] = d["ebit_h"] + dE
            dB = aj_bai.get(y, Fr(0))
            if (not aj.get(y) or reglas == {"tau_fijo"}) and not dB:
                tau[y] = d["tau"]                       # fila 10 registrada, sin cambios
            else:
                if "tau_fijo" in reglas:
                    raise ValueError("no se mezclan reglas en el mismo año")
                bai, imp = d["bai"] + dE + dB, d["imp"]
                for x, r in aj[y]:
                    if r == "tipo_teorico":
                        imp += t_teor * x               # el ajuste lleva su impuesto al tipo teórico
                    elif r == "tau_fijo":
                        raise ValueError("no se mezclan reglas en el mismo año")
                tau[y] = Fr(round(imp / bai, 4)).limit_denominator(10 ** 4)   # fila 10: 4 decimales
        nopat = sum(ebit[y] * (1 - tau[y]) for y in VENT) / 3
        tau5 = sum(tau[y] for y in HOR) / 5 if tau_proy == "cinco_años" else sum(tau[y] for y in VENT) / 3
        m0 = ebit[2025] / V0
        out = {"tau": {y: tau[y] for y in VENT}, "tau5": tau5, "m0": m0, "nopat_medio": nopat, "por_perimetro": {}}
        for k, DX in PER.items():
            f = (nopat - avg(lambda d: d["capex"] - DX(d) + d["dwc"]) - C52) / S_avg
            esc = {n: C.motor_a(V0, m0, tau5, f, **p) for n, p in pal.items()}
            out["por_perimetro"][k] = {"f": f, "F0": V0 * (m0 * (1 - tau5) - f), "escenarios": esc}
        return out

    base = calcular({})
    # controles: el cálculo sin ajustes reproduce el libro y el contraste
    control("f A0 sin ajustes = Historia!C58", base["por_perimetro"]["A0"]["f"], Fr(L["Historia!C58"]), Fr(1, 10 ** 12))
    control("τ de 5 años = Historia!C52", base["tau5"], Fr(str(L["Historia!C52"])), Fr(1, 10 ** 12))
    control("flujo sin crecimiento A0 = referencia de E9 (248,496395342656)", base["por_perimetro"]["A0"]["F0"],
            Fr("248.496395342656"), Fr(1, 10 ** 9))
    for fila, n in ((6, "MALO"), (7, "NORMAL"), (8, "BUENO")):
        mo = base["por_perimetro"]["A0"]["escenarios"][n]
        for t, col in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD"]):
            control(f"Motor!{col}{fila} sin ajustes = libro", mo["flujos"][t], Fr(L[f"Motor!{col}{fila}"]), Fr(1, 10 ** 9))
        control(f"Motor!BF{fila} sin ajustes = libro", mo["flujo_11"], Fr(L[f"Motor!BF{fila}"]), Fr(1, 10 ** 9))
    # diagnóstico conservado del contraste (no es un ajuste)
    earn_f = avg(lambda d: d["earn"]) / S_avg * V0
    plusv_f = avg(lambda d: d["plusv"]) / S_avg * V0
    plusv_m0 = A[2025]["ooie_plusv"] * (1 - base["tau5"])
    diag = {"earnout y otros no monetarios dentro de f (línea del EFE, tres años)": earn_f,
            "plusvalías netas de la ventana dentro de f (línea del EFE, tres años)": plusv_f,
            "resultado por bajas de inmovilizado 2025 dentro de m0 (25,7 de la nota 4.6, al τ de 5 años)": plusv_m0,
            "suma (diagnóstico 27,936)": earn_f + plusv_f + plusv_m0}
    pp = CT["tablas"]["partidas_puntuales_en_flujo_sin_crecimiento"]
    for (k, v), ref in zip(diag.items(), [pp[x] for x in pp]):
        control(f"diagnóstico del contraste: {k}", Fr(str(round(float(v), 3))), Fr(str(ref)))

    # ---------------------------------------------------------------- P3 · ajustes concretos
    earn = {y: A[y]["ooie_earn"] for y in VENT}        # nota 4.6: «Earnout adjustments» / «Ajustements de compléments de prix»
    bajas = {y: A[y]["ooie_plusv"] for y in VENT}      # nota 4.6: resultado por bajas de inmovilizado
    ooie_tot = {2023: F("OOIE_TOT_FR_2023", contraparte=True), 2024: A[2024]["ooie_tot"], 2025: A[2025]["ooie_tot"]}
    quitar = lambda x: -x                                # noqa: E731  normalizar = sacar la partida del EBIT del año
    escenarios = {
        "N1a · earnout de 2023, tipo fijo (fila 10 sin cambios)": {2023: [(quitar(earn[2023]), "tau_fijo")]},
        "N1a · earnout de 2023, no deducible (gasto sin cambios)": {2023: [(quitar(earn[2023]), "no_deducible")]},
        "N1 · ajustes de earnout 2023–25, tipo fijo": {y: [(quitar(earn[y]), "tau_fijo")] for y in VENT},
        "N1 · ajustes de earnout 2023–25, no deducibles": {y: [(quitar(earn[y]), "no_deducible")] for y in VENT},
        "N2 · bajas de 2025 (seguros), tipo fijo": {2025: [(quitar(bajas[2025]), "tau_fijo")]},
        "N2 · bajas de 2025 (seguros), gravadas al tipo teórico": {2025: [(quitar(bajas[2025]), "tipo_teorico")]},
        "N2 · bajas de 2025 (seguros), no gravadas": {2025: [(quitar(bajas[2025]), "no_deducible")]},
        "N2s · bajas de inmovilizado 2023–25 (simétrica), tipo fijo": {y: [(quitar(bajas[y]), "tau_fijo")] for y in VENT},
    }
    for regla_n2, nombre_n2 in (("tau_fijo", "tipo fijo"), ("tipo_teorico", "gravadas al tipo teórico"), ("no_deducible", "no gravadas")):
        aj = {y: [(quitar(earn[y]), "no_deducible")] for y in VENT}
        if regla_n2 == "tau_fijo":
            # no se mezclan reglas en 2025: el ajuste de earnout de 2025 (−0,2) se trata también con tipo fijo
            aj[2025] = [(quitar(earn[2025]) + quitar(bajas[2025]), "tau_fijo")]
        else:
            aj[2025] = [(quitar(earn[2025]), "no_deducible"), (quitar(bajas[2025]), regla_n2)]
        escenarios[f"N1 + N2 conjuntos · earnout no deducible; bajas de 2025 {nombre_n2}"] = aj
    escenarios["Contraejemplo · regla literal «todo lo publicado como no recurrente» (nota 4.6 entera), tipo fijo"] = \
        {y: [(quitar(ooie_tot[y]), "tau_fijo")] for y in VENT}

    tabla = {}
    b0 = base["por_perimetro"]["A0"]
    for nombre, aj in escenarios.items():
        r = calcular(aj)
        r0 = r["por_perimetro"]["A0"]
        dif_comun = Fr(0)
        for k in ("A1", "A2"):
            rk, bk = r["por_perimetro"][k], base["por_perimetro"][k]
            dif_comun = max(dif_comun, abs((rk["F0"] - bk["F0"]) - (r0["F0"] - b0["F0"])))
            for n in pal:
                for t in range(10):
                    dif_comun = max(dif_comun, abs((rk["escenarios"][n]["flujos"][t] - bk["escenarios"][n]["flujos"][t])
                                                   - (r0["escenarios"][n]["flujos"][t] - b0["escenarios"][n]["flujos"][t])))
                dif_comun = max(dif_comun, abs((rk["escenarios"][n]["flujo_11"] - bk["escenarios"][n]["flujo_11"])
                                               - (r0["escenarios"][n]["flujo_11"] - b0["escenarios"][n]["flujo_11"])))
        fila = {"ajustes_EBIT": {str(y): [f6(x, 3) for x, _ in v] for y, v in aj.items()},
                "reglas": sorted({rr for v in aj.values() for _, rr in v}),
                "tau_2023_25": [f6(r["tau"][y], 4) for y in VENT], "tau_5_anios": f6(r["tau5"], 6), "m0": f6(r["m0"], 6),
                "f_A0": f6(r0["f"], 9), "flujo_sin_crecimiento_A0": f6(r0["F0"], 3),
                "variacion_flujo_sin_crecimiento": f6(r0["F0"] - b0["F0"], 3),
                "variacion_por_componente": {
                    "f": f6(-V0 * (r0["f"] - b0["f"]), 3),
                    "m0": f6(V0 * (r["m0"] - base["m0"]) * (1 - r["tau5"]), 3),
                    "τ de 5 años": f6(-V0 * base["m0"] * (r["tau5"] - base["tau5"]), 3)},
                "variacion_NORMAL": {"año_1": f6(r0["escenarios"]["NORMAL"]["flujos"][0] - b0["escenarios"]["NORMAL"]["flujos"][0], 3),
                                     "año_5": f6(r0["escenarios"]["NORMAL"]["flujos"][4] - b0["escenarios"]["NORMAL"]["flujos"][4], 3),
                                     "año_10": f6(r0["escenarios"]["NORMAL"]["flujos"][9] - b0["escenarios"]["NORMAL"]["flujos"][9], 3),
                                     "terminal": f6(r0["escenarios"]["NORMAL"]["flujo_11"] - b0["escenarios"]["NORMAL"]["flujo_11"], 3)},
                "variacion_terminal_MALO_NORMAL_BUENO": [f6(r0["escenarios"][n]["flujo_11"] - b0["escenarios"][n]["flujo_11"], 3) for n in pal],
                "misma_variacion_en_A0_A1_A2": dif_comun == 0}
        if dif_comun != 0:
            errores.append(f"variación distinta entre perímetros: {nombre}")
        tabla[nombre] = fila

    # ---------------------------------------------------------------- V3 y V4 · de qué depende la cifra de N1 (no son propuestas)
    LV = {k: v[0] for k, v in LECTURAS.items()}
    n1_nd = {y: [(quitar(earn[y]), "no_deducible")] for y in VENT}

    def delta(r, b):
        r0, s0 = r["por_perimetro"]["A0"], b["por_perimetro"]["A0"]
        return {"tau_2023_25": [f6(r["tau"][y], 4) for y in VENT], "tau_de_proyeccion": f6(r["tau5"], 6),
                "variacion_flujo_sin_crecimiento": f6(r0["F0"] - s0["F0"], 3),
                "variacion_año_11_MALO_NORMAL_BUENO": [f6(r0["escenarios"][n]["flujo_11"] - s0["escenarios"][n]["flujo_11"], 3) for n in pal]}
    aj21 = dict(n1_nd)
    aj21[2021] = [(-LV["ajuste_earnout_2021"], "no_deducible")]
    aj21[2022] = [(-LV["ajuste_earnout_2022"], "no_deducible")]
    base_v = calcular({}, tau_proy="ventana")
    dep = {
        "N1 + actualización del earnout fuera del BAI que da el tipo [LECTURA]": delta(calcular(
            n1_nd, aj_bai={2023: LV["actualizacion_earnout_2023"], 2024: LV["actualizacion_earnout_2024"], 2025: LV["actualizacion_earnout_2025"]}), base),
        "N1 + ajustes de earnout de 2021–22 fuera del BAI de su año, en el τ de cinco años [LECTURA]": delta(calcular(aj21), base),
        "N1 no deducible con el τ de proyección de la ventana (E8.1; convención no adoptada)": delta(calcular(n1_nd, tau_proy="ventana"), base_v),
        "N1 con tipo fijo y el τ de proyección de la ventana (E8.1; convención no adoptada)": delta(calcular(
            {y: [(quitar(earn[y]), "tau_fijo")] for y in VENT}, tau_proy="ventana"), base_v),
    }
    # reproducción de las cifras de la revisión dirigida (recalculo_independiente.txt, secciones C y D; 3 decimales)
    for (k, campo, i), ref in [((0, "variacion_flujo_sin_crecimiento", None), "-12.396"), ((0, "variacion_año_11_MALO_NORMAL_BUENO", 1), "-20.270"),
                               ((1, "variacion_flujo_sin_crecimiento", None), "-11.190"), ((1, "variacion_año_11_MALO_NORMAL_BUENO", 1), "-18.142"),
                               ((2, "variacion_flujo_sin_crecimiento", None), "-9.141"), ((2, "variacion_año_11_MALO_NORMAL_BUENO", 1), "-15.848"),
                               ((3, "variacion_flujo_sin_crecimiento", None), "-9.763")]:
        nombre_d = list(dep)[k]
        v = dep[nombre_d][campo] if i is None else dep[nombre_d][campo][i]
        control(f"revisión dirigida reproducida: {nombre_d} · {campo}{'' if i is None else ' NORMAL'}", Fr(str(v)), Fr(ref), Fr(6, 10 ** 4))

    # ---------------------------------------------------------------- P2 · «PPA constante»
    p_f = avg(lambda d: d["da_ppa"]) / S_avg
    p_m0 = A[2025]["da_ppa"] / V0
    ppa = {"PPA media 2023–25 ÷ ventas medias (lo que devuelve f en A2)": f6(100 * p_f, 4),
           "PPA 2025 ÷ ventas 2025 (lo que lleva m0)": f6(100 * p_m0, 4),
           "diferencia aplicada a las ventas 2025 (mm)": f6((p_f - p_m0) * V0, 3),
           "PPA 2025 (mm)": f6(A[2025]["da_ppa"], 1),
           "PPA que f devuelve sobre las ventas 2025 (mm)": f6(p_f * V0, 3),
           "sentido de la diferencia de la PPA": "sube el flujo sin crecimiento de A2" if p_f > p_m0 else "baja el flujo sin crecimiento de A2"}
    # (V5) la misma condición vale para la amortización ROU, que f devuelve en A1 y A2
    r_f = avg(lambda d: d["da_rou"]) / S_avg
    r_m0 = A[2025]["da_rou"] / V0
    ppa |= {"ROU media 2023–25 ÷ ventas medias (lo que devuelve f en A1 y A2)": f6(100 * r_f, 4),
            "ROU 2025 ÷ ventas 2025 (lo que lleva m0)": f6(100 * r_m0, 4),
            "ROU que f devuelve sobre las ventas 2025 (mm)": f6(r_f * V0, 3), "ROU 2025 (mm)": f6(A[2025]["da_rou"], 1),
            "diferencia de la ROU aplicada a las ventas 2025 (mm; baja el flujo sin crecimiento de A1 y A2)": f6((r_f - r_m0) * V0, 3),
            "los dos efectos de escala juntos en A2 (mm)": f6((p_f - p_m0 + r_f - r_m0) * V0, 3)}
    control("efecto de escala de la ROU = el de la revisión dirigida (−10,118279)", (r_f - r_m0) * V0, Fr("-10.118279"), Fr(1, 10 ** 6))

    # ---------------------------------------------------------------- P4 · arrendamientos y terminal
    w_avg = avg(lambda d: d["leasepay"]) / S_avg
    w_25 = A[2025]["leasepay"] / V0
    arr = {"pagos ÷ ventas, media de la ventana (%)": f6(100 * w_avg, 4), "pagos ÷ ventas 2025 (%)": f6(100 * w_25, 4),
           "media escalada a las ventas 2025 (mm)": f6(w_avg * V0, 6), "pagos 2025 (mm)": f6(A[2025]["leasepay"], 1),
           "sensibilidad del flujo sin crecimiento con el peso de 2025 (mm)": f6(-(w_25 - w_avg) * V0, 6),
           "parte de los pagos (A0, A1 y A2; mm)": f6(-(w_25 - w_avg) * V0, 6),
           "parte de la amortización ROU que devuelve f, con el peso de 2025 (solo A1 y A2; mm)": f6((r_m0 - r_f) * V0, 6),
           "sensibilidad con el peso de 2025 en las dos cosas (A1 y A2; mm)": f6(-(w_25 - w_avg) * V0 + (r_m0 - r_f) * V0, 6)}
    control("sensibilidad conjunta de arrendamientos en A1 y A2 = la de la revisión dirigida (−6,659958)",
            -(w_25 - w_avg) * V0 + (r_m0 - r_f) * V0, Fr("-6.659958"), Fr(1, 10 ** 6))
    control("sensibilidad de arrendamientos = la de la revisión (16,778237414)", (w_25 - w_avg) * V0,
            Fr("16.778237414016186"), Fr(1, 10 ** 9))
    roic = {}
    for n, p in pal.items():
        mo = base["por_perimetro"]["A0"]["escenarios"][n]
        V10 = mo["V"][-1]
        nopat11 = V10 * (1 + p["g_inf"]) * p["m_obj"] * (1 - base["tau5"])
        inv_roic = nopat11 * p["g_inf"] / p["roic"]
        inv_s2c = V10 * p["g_inf"] / p["s2c"]
        roic[n] = {"g_inf": f6(p["g_inf"], 4), "m_obj": f6(p["m_obj"], 4), "S2C_años_1_10": f6(p["s2c"], 4), "ROIC": f6(p["roic"], 4),
                   "ROIC_que_reproduce_S2C ((1+g∞)·m_obj·(1−τ)·S2C)": f6((1 + p["g_inf"]) * p["m_obj"] * (1 - base["tau5"]) * p["s2c"], 6),
                   "S2C_implícita_en_el_ROIC": f6(p["roic"] / ((1 + p["g_inf"]) * p["m_obj"] * (1 - base["tau5"])), 6),
                   "inversión_de_crecimiento_del_terminal_con_ROIC (mm)": f6(inv_roic, 3),
                   "la_misma_con_S2C (mm)": f6(inv_s2c, 3), "diferencia (mm)": f6(inv_roic - inv_s2c, 3),
                   "rentabilidad_marginal_del_libro (m_obj·(1−τ)·S2C; Convenciones V6.3 §3)": f6(p["m_obj"] * (1 - base["tau5"]) * p["s2c"], 6)}
    # (V6) bloque 10 del diagnóstico del libro: la comprobación que ya existe, con su umbral
    import openpyxl
    wb = openpyxl.load_workbook(a.libro, data_only=True, read_only=True)
    DG = wb["Diagnóstico V6"]
    celda = lambda c, f: DG.cell(row=f, column=" ABCD".index(c)).value   # noqa: E731
    bloque10 = {"fila_176_rentabilidad_marginal_años_1_10": [celda(c, 176) for c in "BCD"],
                "fila_177_ROIC_del_terminal": [celda(c, 177) for c in "BCD"],
                "fila_178_salto_en_el_año_11": [celda(c, 178) for c in "BCD"],
                "fila_179": {"rótulo": celda("A", 179), "valor_C179": celda("C", 179)}}
    for i, (n, pp) in enumerate(pal.items()):
        control(f"Diagnóstico V6!{'BCD'[i]}176 = m_obj·(1−τ)·S2C ({n})", pp["m_obj"] * (1 - base["tau5"]) * pp["s2c"],
                Fr(str(bloque10["fila_176_rentabilidad_marginal_años_1_10"][i])), Fr(1, 10 ** 9))
        roic[n]["salto_del_libro (fila 178: ROIC − rentabilidad marginal), puntos"] = f6(100 * (pp["roic"] - pp["m_obj"] * (1 - base["tau5"]) * pp["s2c"]), 3)
        roic[n]["salto_con_la_igualdad_exacta (ROIC − (1+g∞)·m_obj·(1−τ)·S2C), puntos"] = f6(100 * (pp["roic"] - (1 + pp["g_inf"]) * pp["m_obj"] * (1 - base["tau5"]) * pp["s2c"]), 3)
    wb.close()
    # comprobación de las [LECTURA] y de los pasajes en los PDF (si se da el árbol materializado)
    lecturas = comprobar_lecturas(a.raiz, a.fuentes) if a.raiz else None
    if lecturas:
        fallan = [k for k, v in lecturas["literales"].items() if not v["en_la_pagina"]] + \
                 [x["pasaje"] for x in lecturas["pasajes"] if not x["encontrado"]] + [d for d, ok in lecturas["huellas_pdf"].items() if not ok]
        lecturas["fallan"] = fallan
        if fallan:
            errores.append(f"lecturas no encontradas en el PDF: {fallan}")

    res = {"naturaleza": "copia de investigación; no es una entrada registrada, una política adoptada ni una valoración; "
                         "Elis sigue en pendiente_de_datos",
           "huella_libro": L["sha256"], "controles": controles,
           "diagnostico_del_contraste": {k: f6(v, 3) for k, v in diag.items()},
           "P3_normalizacion": {"base_sin_ajustes": {"tau_2023_25": [f6(base["tau"][y], 4) for y in VENT], "tau_5_anios": f6(base["tau5"], 6),
                                                     "m0": f6(base["m0"], 6), "f_A0": f6(b0["f"], 9), "flujo_sin_crecimiento_A0": f6(b0["F0"], 3)},
                                "partidas": {"ajustes de earnout (nota 4.6)": {str(y): f6(earn[y], 1) for y in VENT},
                                             "resultado por bajas de inmovilizado (nota 4.6)": {str(y): f6(bajas[y], 1) for y in VENT},
                                             "otros ingresos y gastos operativos, total (nota 4.6)": {str(y): f6(ooie_tot[y], 1) for y in VENT},
                                             "tipo teórico de la matriz (regla «tipo_teorico»)": f6(100 * t_teor, 2)},
                                "escenarios": tabla},
           "P2_PPA_constante": ppa, "P4_arrendamientos": arr, "P4_ROIC_terminal": roic,
           "V3_V4_de_que_depende_N1": {"nota": "sensibilidades, no propuestas: las [LECTURA] no están en el CSV verificado y la "
                                               "convención del τ de proyección es la registrada (cinco años) salvo que se diga",
                                       "escenarios": dep},
           "V6_bloque_10_del_libro": bloque10,
           "lecturas": {"valores": {k: {"valor": f6(v[0], 1), "doc": v[1], "pagina_pdf": v[2], "literal": v[3]} for k, v in LECTURAS.items()},
                        "comprobacion_en_pdf": lecturas},
           "resumen": {"controles": len(controles), "fallidos": [c["control"] for c in controles if not c["ok"]], "errores": errores}}
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = ["# Copia de investigación F1 · Elis (P2–P4 y correcciones V1–V11)", "",
          "Generado por `scripts/copia_investigacion_f1.py`. **No es una entrada registrada, ni una política adoptada, ni una valoración.** "
          "Elis sigue en `pendiente_de_datos`. Mismas funciones que `contraste_f1.py`; solo cifras verificadas; libro en solo lectura.", "",
          f"Controles: {len(controles)}, fallidos: {len(res['resumen']['fallidos'])}.", "",
          "## P3 · Ajustes y cálculo conjunto (perímetro A0; la variación es la misma en A1 y A2)", "",
          "| Escenario | τ 2023 / 2024 / 2025 | τ 5 años | f (A0) | Flujo sin crecimiento | Variación | de ella: f / m0 / τ | Terminal NORMAL |",
          "|---|---|---|---|---|---|---|---|",
          f"| Sin ajustes (libro) | {' / '.join(str(x) for x in res['P3_normalizacion']['base_sin_ajustes']['tau_2023_25'])} | "
          f"{res['P3_normalizacion']['base_sin_ajustes']['tau_5_anios']} | {res['P3_normalizacion']['base_sin_ajustes']['f_A0']} | "
          f"{res['P3_normalizacion']['base_sin_ajustes']['flujo_sin_crecimiento_A0']} | — | — | — |"]
    for nombre, fl in tabla.items():
        vc = fl["variacion_por_componente"]
        md.append(f"| {nombre} | {' / '.join(str(x) for x in fl['tau_2023_25'])} | {fl['tau_5_anios']} | {fl['f_A0']} | "
                  f"{fl['flujo_sin_crecimiento_A0']} | {fl['variacion_flujo_sin_crecimiento']} | {vc['f']} / {vc['m0']} / {vc['τ de 5 años']} | "
                  f"{fl['variacion_NORMAL']['terminal']} |")
    md += ["", "Diagnóstico conservado del contraste (no es un ajuste): " +
           "; ".join(f"{k}: {f6(v, 3)}" for k, v in diag.items()) + ".", "",
           "## P2 · «PPA constante»", ""] + [f"- {k}: {v}" for k, v in ppa.items()] + \
          ["", "## P4 · Arrendamientos", ""] + [f"- {k}: {v}" for k, v in arr.items()] + \
          ["", "## P4 · ROIC del terminal frente a S2C (palancas del libro)", "",
           "| Escenario | g∞ | m_obj | S2C | ROIC | ROIC que reproduce S2C | S2C implícita | Inversión del terminal con ROIC | con S2C | Diferencia |",
           "|---|---|---|---|---|---|---|---|---|---|"]
    for n, v in roic.items():
        md.append(f"| {n} | " + " | ".join(str(x) for x in list(v.values())[:9]) + " |")
    md += ["", "## V6 · Bloque 10 del diagnóstico del libro (Convenciones V6.3 §3) frente a la igualdad exacta", "",
           "| Escenario | Rentabilidad marginal del libro (fila 176) | ROIC (fila 177) | Salto del libro, puntos | Salto con la igualdad exacta, puntos |",
           "|---|---|---|---|---|"]
    for n, v in roic.items():
        md.append(f"| {n} | {v['rentabilidad_marginal_del_libro (m_obj·(1−τ)·S2C; Convenciones V6.3 §3)']} | {v['ROIC']} | "
                  f"{v['salto_del_libro (fila 178: ROIC − rentabilidad marginal), puntos']} | {v['salto_con_la_igualdad_exacta (ROIC − (1+g∞)·m_obj·(1−τ)·S2C), puntos']} |")
    md += [f"", f"Umbral del aviso del libro: {bloque10['fila_179']['rótulo']} = {bloque10['fila_179']['valor_C179']}.", "",
           "## V3 y V4 · De qué depende la cifra de N1 (sensibilidades, no propuestas)", "",
           "| Escenario | τ 2023 / 2024 / 2025 | τ de proyección | Variación del flujo sin crecimiento | Variación del año 11 MALO / NORMAL / BUENO |",
           "|---|---|---|---|---|"]
    for n, v in dep.items():
        md.append(f"| {n} | {' / '.join(str(x) for x in v['tau_2023_25'])} | {v['tau_de_proyeccion']} | {v['variacion_flujo_sin_crecimiento']} | "
                  f"{' / '.join(str(x) for x in v['variacion_año_11_MALO_NORMAL_BUENO'])} |")
    md += ["", "[LECTURA]: cifras que no están en el CSV verificado; documento, página y literal en el JSON."]
    if lecturas:
        md += [f"Comprobación en el PDF (pdftotext, una página): {sum(v['en_la_pagina'] for v in lecturas['literales'].values())} de "
               f"{len(lecturas['literales'])} literales y {sum(x['encontrado'] for x in lecturas['pasajes'])} de {len(lecturas['pasajes'])} pasajes "
               f"encontrados; huellas de los PDF: {'todas iguales a datos/fuentes.json' if all(lecturas['huellas_pdf'].values()) else 'alguna distinta'}."]
    a.informe.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
