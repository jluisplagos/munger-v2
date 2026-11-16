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

Los históricos, el CSV, la verificación y el libro no cambian. El libro se lee en solo lectura y con su huella; de él
se toman las palancas y el FCF base registrado (Historia!C70 = 307,933), que se contrasta con el cálculo.

Uso:
  python3 -I copia_investigacion_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json \
     --libro <ruta>/Elis_v63_evaluada.xlsx --contraste ../resultados/contraste_f1.json \
     --salida ../resultados/copia_investigacion_f1.json --informe ../resultados/copia_investigacion_f1.md
Termina con 1 si un control falla (reproducción de f, F0, flujos del libro o diagnóstico del contraste).
"""
import argparse
import importlib.util
import json
import sys
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("contraste_f1", Path(__file__).with_name("contraste_f1.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
VENT, HOR = C.VENTANA, C.HORIZONTE


def f6(x, n=6):
    return C.f6(x, n)


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--verificacion", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--contraste", required=True, type=Path, help="resultados/contraste_f1.json (diagnóstico conservado)")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
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

    def calcular(aj):
        """aj: {año: [(ΔEBIT, regla)]}, regla ∈ {«tau_fijo», «no_deducible», «tipo_teorico»}. Devuelve el cálculo
        conjunto con las mismas ecuaciones que el contraste (f de la plantilla, τ de 5 años, m0 y motor A)."""
        tau, ebit = {}, {}
        for y in HOR:
            d = A[y]
            dE = sum((x for x, _ in aj.get(y, [])), Fr(0))
            reglas = {r for _, r in aj.get(y, [])}
            ebit[y] = d["ebit_h"] + dE
            if not aj.get(y) or reglas == {"tau_fijo"}:
                tau[y] = d["tau"]                       # fila 10 registrada, sin cambios
            else:
                bai, imp = d["bai"] + dE, d["imp"]
                for x, r in aj[y]:
                    if r == "tipo_teorico":
                        imp += t_teor * x               # el ajuste lleva su impuesto al tipo teórico
                    elif r == "tau_fijo":
                        raise ValueError("no se mezclan reglas en el mismo año")
                tau[y] = Fr(round(imp / bai, 4)).limit_denominator(10 ** 4)   # fila 10: 4 decimales
        nopat = sum(ebit[y] * (1 - tau[y]) for y in VENT) / 3
        tau5 = sum(tau[y] for y in HOR) / 5
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

    # ---------------------------------------------------------------- P2 · «PPA constante»
    p_f = avg(lambda d: d["da_ppa"]) / S_avg
    p_m0 = A[2025]["da_ppa"] / V0
    ppa = {"PPA media 2023–25 ÷ ventas medias (lo que devuelve f en A2)": f6(100 * p_f, 4),
           "PPA 2025 ÷ ventas 2025 (lo que lleva m0)": f6(100 * p_m0, 4),
           "diferencia aplicada a las ventas 2025 (mm)": f6((p_f - p_m0) * V0, 3),
           "PPA 2025 (mm)": f6(A[2025]["da_ppa"], 1),
           "PPA que f devuelve sobre las ventas 2025 (mm)": f6(p_f * V0, 3)}

    # ---------------------------------------------------------------- P4 · arrendamientos y terminal
    w_avg = avg(lambda d: d["leasepay"]) / S_avg
    w_25 = A[2025]["leasepay"] / V0
    arr = {"pagos ÷ ventas, media de la ventana (%)": f6(100 * w_avg, 4), "pagos ÷ ventas 2025 (%)": f6(100 * w_25, 4),
           "media escalada a las ventas 2025 (mm)": f6(w_avg * V0, 6), "pagos 2025 (mm)": f6(A[2025]["leasepay"], 1),
           "sensibilidad del flujo sin crecimiento con el peso de 2025 (mm)": f6(-(w_25 - w_avg) * V0, 6)}
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
                   "la_misma_con_S2C (mm)": f6(inv_s2c, 3), "diferencia (mm)": f6(inv_roic - inv_s2c, 3)}

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
           "resumen": {"controles": len(controles), "fallidos": [c["control"] for c in controles if not c["ok"]], "errores": errores}}
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    md = ["# Copia de investigación F1 · Elis (P2–P4)", "",
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
        md.append(f"| {n} | " + " | ".join(str(x) for x in v.values()) + " |")
    a.informe.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
