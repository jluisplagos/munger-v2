#!/usr/bin/env python3
"""Regresión F1 de Elis sobre una COPIA de su expediente (F1-IMPL, 4.15). El expediente original no se toca (se comprueba con huellas).

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_impl/scripts/regresion_elis_f1.py DESTINO_COPIA
  DESTINO_COPIA: carpeta nueva FUERA del repositorio (la copia lleva PDF y libros, que no se versionan).
Hace:
  1. copia 2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis (libro d2593777…, el que concilió el frente E) a DESTINO_COPIA/Elis;
  2. escribe en la copia dos declaraciones F1 con las cifras verificadas de `datos/elis_cifras_f1.json`:
     a) «libro tal cual»: perímetro A0 (lo que calcula el libro V6.3) → debe saltar V-F1a;
     b) «decisiones del 17-nov-2026»: (1a) sin ROU, (2) PPA no es reposición y margen con proporción constante, (3a)/(3b iv) R pendiente
        (A3_estimado sin estimación), (4a) palancas y ROIC sin perímetro declarado (como están), (4b) opción A (pendiente),
        (5a) N1 con sus opciones sin decidir, (5b) transición conocida sin importe ni horizonte, E8.1 τ de cinco años;
  3. ejecuta motor_a_f1.py evaluar sobre la copia con cada una, y ficha.py --provisional e informe.py sobre la copia;
  4. comprueba: réplica del libro, E9 T1–T3b, +139,4 de A1 frente a A0, T16, Elis en pendiente_de_datos, invariantes (C48 = 108,
     C49 = 128,1, C70 = 307,933), el libro y el original sin cambios.
Escribe f1_impl/resultados/regresion_elis_f1.{json,md} y copia los resultados F1 de la copia.
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
F1D = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(F1D, "..", "..", ".."))
ORIG = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
SHA_LIBRO = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
PY = sys.executable
REG17 = {"fecha": "2026-11-17", "persona": "persona responsable del proyecto (decisión registrada; no se firma aquí)",
         "motivo": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md:68–83"}
SIN_REG = {"fecha": None, "persona": None, "motivo": None}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def huellas(d):
    out = {}
    for r, _, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = sha(p)
    return out


def serie(cif, nombre, tratamiento):
    out = {}
    for y, e in cif["series"][nombre].items():
        vp = e["valor_publicado"]
        out[y] = {"valor_fuente": vp, "signo": -1 if vp < 0 else 1, "tratamiento": tratamiento if vp < 0 else "ninguno",
                  "documento": e["documento"], "pagina": e["pagina"], "literal": e["literal"], "id_fila_frente_E": e["id_fila"]}
    return out


def declaracion(cif, a0, n1=False):
    trat = "importe publicado entre paréntesis (cargo); magnitud positiva en el modelo"
    src = lambda e: {"documento": e["documento"], "pagina": e["pagina"], "literal": e["literal"], "id_fila_frente_E": e["id_fila"]}  # noqa: E731
    bai = {y: dict(src(e), valor=e["valor_publicado"]) for y, e in cif["series"]["bai"].items()}
    imp = {y: dict(src(e), valor=-e["valor_publicado"]) for y, e in cif["series"]["gasto_impuesto"].items()}
    aj = [{"regla": "N1", "anio": int(y), "partida": "ajuste de earnout (nota 4.6)", "importe": e["valor_publicado"], "fuente": src(e),
           "regla_fiscal": "no_deducible", "ubicacion_caja": "pagos de earnouts en «Acquisition of subsidiaries, net of cash acquired» (inversión), fuera del FCF base"}
          for y, e in cif["series"]["ajuste_earnout"].items()]
    aj += [{"tipo": "actualizacion_financiera_earnout", "anio": int(y), "importe": -e["valor_publicado"], "fuente": src(e),
            "nota": "gasto financiero publicado en positivo; efecto en el BAI negativo"} for y, e in cif["series"]["actualizacion_earnout"].items()]
    d = {
        "formato": "motor_a_f1 v1",
        "nota": ("Declaración de la regresión F1-IMPL sobre una COPIA del expediente de Elis. Las decisiones citan su registro del 17-nov-2026; "
                 "lo que el registro no dice literalmente queda sin persona (F1-REGISTRO lo señala). No es una entrada registrada del expediente."),
        "norma_contable": {"valor": "NIIF", "registro": dict(SIN_REG, origen="Control maestro L4 del libro (IFRS adoptadas por la UE); sin declaración humana F1")},
        "perimetro_reinversion": {"valor": "A0_total" if a0 else "A3_estimado",
                                  "registro": SIN_REG if a0 else dict(SIN_REG, origen="derivado por el agente F1-IMPL de (1a), (2)(i) y (3a): R = R_propia + R_compras (+ transición), pendiente")},
        "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": dict(REG17, motivo=REG17["motivo"] + " · (2)(v)")},
        "perimetro_palancas_s2c": {"valor": None, "registro": SIN_REG, "nota": "en Elis las palancas no declaran perímetro (4a)"},
        "perimetro_roic": {"valor": None, "registro": SIN_REG},
        "clasificacion_compras": {"valor": "pendiente", "registro": dict(REG17, motivo=REG17["motivo"] + " · (4b) opción A, hasta M6")},
        "transicion": {"conocida": True, "tratamiento": "pendiente", "registro": dict(REG17, motivo=REG17["motivo"] + " · (5b)"),
                       "importes": None, "horizonte": None, "finalidad_documentada": None,
                       "nota": "plan climático dentro del capex, sin importe separado (URD25 p.122); M1 pendiente"},
        "reinversion_estimada": None,
        "series": {"da_rou": serie(cif, "da_rou", trat), "da_ppa": serie(cif, "da_ppa", trat),
                   "pagos_arrendamiento": serie(cif, "pagos_arrendamiento", "pago publicado entre paréntesis; magnitud positiva"),
                   "vnc_intangibles_adquiridos": {"valor": cif["series"]["vnc_relaciones_clientes"]["2025"]["valor_publicado"],
                                                  "nota": "solo relaciones con clientes (275,1; URD25 p.364)"}},
        "normalizacion": {"ajustes": aj, "bai": bai, "gasto_impuesto": imp, "margen_objetivo_sin_ajustes": None,
                          "deducir_diagnostico_partidas_puntuales": False},
        "umbral_v_f1a": None,
        # K3a: C70 (307,933) frente a la media de la fila 35 de la Historia (323,000); la diferencia, −15,067, son dos partidas registradas
        "conciliacion_fcf_base": [
            {"componente": "C48", "importe": -25.067, "partida": "interés de caja de los arrendamientos dentro de C48 (C48 = 82,933 + 25,067; E6)",
             "fuente": {"documento": "registro E6 y configuracion/cambio_elis_c48_4_15.json", "pagina": None}},
            {"componente": "C47", "importe": 10.0, "partida": "capex neto de cesiones y subvenciones en C47 (857,167) frente al bruto de la fila 12 (867,167)",
             "fuente": {"documento": "INFORME_CONCILIACION_F1.md §4.1-4.2 (frente E)", "pagina": None}}],
    }
    if a0 and not n1:
        d["normalizacion"] = {"ajustes": [], "bai": {}, "gasto_impuesto": {}, "deducir_diagnostico_partidas_puntuales": False}
    return d


def main():
    dest = os.path.abspath(sys.argv[1])
    if os.path.exists(dest):
        sys.exit(f"{dest} ya existe: la copia se hace en una carpeta nueva")
    if os.path.commonpath([dest, PV]) == PV:
        sys.exit("la copia va fuera del repositorio")
    cif = json.load(open(os.path.join(F1D, "datos", "elis_cifras_f1.json"), encoding="utf-8"))
    h0 = huellas(ORIG)
    c = os.path.join(dest, "Elis")
    shutil.copytree(ORIG, c)
    libro = os.path.join(c, "Elis_v63_evaluada.xlsx")
    assert sha(libro) == SHA_LIBRO, "el libro de la copia no es d2593777…"
    est0 = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
    comp = []

    def chk(nombre, ok, detalle=""):
        comp.append({"comprobacion": nombre, "ok": bool(ok), "detalle": detalle})
        print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))

    res = {}
    for clave, a0, n1 in (("libro_tal_cual_A0", True, False), ("decisiones_17nov", False, True), ("T16_A0_con_N1", True, True)):
        dp = os.path.join(dest, f"motor_a_f1.{clave}.json")
        json.dump(declaracion(cif, a0, n1), open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        out = os.path.join(dest, f"resultado_{clave}")
        r = subprocess.run([PY, "-I", os.path.join(PV, "scripts", "motor_a_f1.py"), "evaluar", c, "--libro", libro, "--declaracion", dp, "--salida", out],
                           capture_output=True, text=True)
        res[clave] = {"codigo": r.returncode, "salida": r.stdout.strip()[-400:], "resultado": json.load(open(os.path.join(out, "motor_a_f1_resultado.json"), encoding="utf-8"))}
    ref = cif["referencia_E9"]
    rA = res["libro_tal_cual_A0"]["resultado"]
    rD = res["decisiones_17nov"]["resultado"]
    salta = lambda r, i: any(g["id"] == i and g["salta"] for g in r["guardas"])  # noqa: E731
    chk("réplica: la capa F1 reproduce el libro en A0 (f, τ, m0, ancla y 33 flujos)", rA["replica_del_libro"]["conforme"] and rA["replica_del_libro"]["flujos_contrastados"] == 33,
        json.dumps(rA["replica_del_libro"]))
    dg = rD["diagnostico_por_perimetro"]
    for k, kr in (("A0_total", "A0"), ("A1_sin_ROU", "A1"), ("A2_propio", "A2"), ("B_cota_capex", "B")):
        e = ref["perimetros"][kr]
        chk(f"E9 {kr}: f, flujo sin crecimiento y C53", abs(dg[k]["f"] - e["f"]) <= 1e-12 and abs(dg[k]["flujo_sin_crecimiento"] - e["flujo_sin_crecimiento"]) <= 1e-9
            and abs(dg[k]["ancla_s2c_E4"] - e["S2C_C53"]) <= 1e-9, f"f {dg[k]['f']} · F0 {dg[k]['flujo_sin_crecimiento']} · C53 {dg[k]['ancla_s2c_E4']}")
    for k, kr in (("A1_sin_ROU", "A1"), ("A2_propio", "A2")):
        mx = max(abs(a - b) for n in ("MALO", "NORMAL", "BUENO") for a, b in zip(dg[k]["escenarios"][n]["anios_1_10"] + [dg[k]["escenarios"][n]["anio_11"]],
                                                                                   ref["A1_A2_flujos_palancas_actuales"][kr][n]))
        chk(f"E9 {kr}: flujos de los años 1–10 y año 11 con las palancas actuales", mx <= 1e-9, f"desviación máxima {mx:.2e}")
    mx = max(abs(a - b) for n in ("MALO", "NORMAL", "BUENO") for a, b in zip(dg["A0_total"]["escenarios"][n]["anios_1_10"] + [dg["A0_total"]["escenarios"][n]["anio_11"]],
                                                                                 ref["A0_flujos_libro"][n]))
    chk("E9 T1: flujos A0 = los del libro", mx <= 1e-9, f"desviación máxima {mx:.2e}")
    d139 = rD["diferencias_frente_a_A0_flujo_sin_crecimiento"]["A1_sin_ROU"]
    chk("(1a) flujo corregido frente a A0 en la base 2025: +139,4", abs(d139 - 139.381721) < 1e-6, f"{d139:+.6f}")
    chk("V-F1a salta con el libro tal cual (A0 con ROU y C49 > 0)", salta(rA, "V-F1a") and res["libro_tal_cual_A0"]["codigo"] in (3, 4))
    k3 = dg["A0_total"]["K3"]
    chk("K3 en A0: puente cuadrado y doble cómputo del arrendamiento señalado (132,5 de media; 139,4 a la escala de 2025)",
        k3["identidad_cuadra"] and abs(k3["doble_computo_por_clase_a_la_escala_del_año_base"]["doble_computo"] - 139.381721) < 1e-6,
        json.dumps(k3["doble_computo_por_clase_a_la_escala_del_año_base"]))
    chk("K3 en A2: sin doble cómputo (partidas sin explicar: ninguna)", dg["A2_propio"]["K3"]["identidad_cuadra"] and not dg["A2_propio"]["K3"]["partidas_sin_explicar"])
    chk("K3a: caja base por dos vías conforme (307,933 frente a 323,000; −25,067 de C48 y +10,0 de C47 declarados)",
        not salta(rD, "F1-K3a") and abs(rD["K3a_caja_base"]["media_fila_35"] - 323.0) < 1e-9, json.dumps(rD["K3a_caja_base"]))
    chk("K3b/K3c con el libro tal cual (A0): alquiler contado dos veces y reinversión media −81,2: bloquean",
        salta(rA, "F1-K3b") and rA["K3"]["K3b_alquiler_contado"] == "dos veces" and salta(rA, "F1-K3c"))
    chk("K3b con las decisiones (A3: f devuelve la ROU, pagos en el FCF base): alquiler contado una vez", rD["K3"]["K3b_alquiler_contado"] == "una vez" and not salta(rD, "F1-K3b"))
    t16 = cif["referencia_T16"]["N1"]
    rT = res["T16_A0_con_N1"]["resultado"]
    cT = rT["calculo_perimetro_declarado"]
    chk("T16: N1 en A0 (τ 0,2619/0,2806/0,2559; τ5 0,28234; m0 0,131379; f 0,044900433; flujo 236,891)",
        abs(cT["f"] - t16["f_A0"]) < 1e-9 and abs(cT["flujo_sin_crecimiento"] - t16["flujo_sin_crecimiento_A0"]) < 1e-3
        and [round(cT["tau_ventana"][y], 4) for y in ("2023", "2024", "2025")] == t16["tau_2023_25"] and abs(cT["tau_proyeccion"] - t16["tau_5_anios"]) < 1e-9
        and abs(cT["m0"] - t16["m0"]) < 1e-6, f"f {cT['f']} · F0 {cT['flujo_sin_crecimiento']} · τ {cT['tau_ventana']} · τ5 {cT['tau_proyeccion']}")
    efT = rT.get("efecto_N1_frente_a_sin_normalizar") or {}
    v34 = cif["referencia_T16"]["V3_V4"]
    chk("T16: −11,605 (solo ventana) y variantes sin decidir −11,190 (2021–22) y −12,396 (actualización)",
        abs(efT.get("N1 solo en la ventana, sin la actualización financiera", 0) - t16["variacion_flujo_sin_crecimiento"]) < 1e-3
        and abs(efT.get("N1 también en los ejercicios del τ fuera de la ventana", 0) - v34["N1 + ajustes de earnout de 2021–22 fuera del BAI de su año, en el τ de cinco años [cifras verificadas]"]["variacion_flujo_sin_crecimiento"]) < 1e-3
        and abs(efT.get("N1 con la actualización financiera fuera del BAI que da el tipo", 0) - v34["N1 + actualización del earnout fuera del BAI que da el tipo [cifras verificadas]"]["variacion_flujo_sin_crecimiento"]) < 1e-3,
        json.dumps(efT, ensure_ascii=False))
    a11 = cT["escenarios"]["NORMAL"]["anio_11"] - ref["A0_flujos_libro"]["NORMAL"][10]
    chk("T16: variación del año 11 NORMAL −18,609", abs(a11 - t16["variacion_NORMAL"]["terminal"]) < 1e-3, f"{a11:+.6f}")
    chk("T16: con N1 sin decidir sus opciones, F1-PARAM bloquea y F1-LIBRO también (el libro no normaliza)", salta(rT, "F1-PARAM") and salta(rT, "F1-LIBRO"))
    chk("Elis sigue en pendiente_de_datos: estado del expediente sin cambios", est0.get("estado_analisis") == "pendiente_de_datos")
    chk("Elis: la evaluación F1 con las decisiones propone pendiente_de_datos (código 3)", rD["estado_propuesto"] == "pendiente_de_datos" and res["decisiones_17nov"]["codigo"] == 3,
        rD["rotulo"])
    for gid in ("V-F1d", "V-F1j", "V-F1i", "V-F1g", "V-F1k", "F1-PARAM", "F1-LIBRO", "V-F1l"):
        chk(f"Elis con las decisiones: {gid} bloquea", salta(rD, gid), next((g["detalle"][:160] for g in rD["guardas"] if g["id"] == gid and g["salta"]), ""))
    chk("Elis con las decisiones: V-F1a no salta (el perímetro no es A0)", not salta(rD, "V-F1a"))
    er = rD["entradas_registradas"]
    chk("invariantes: C48 = 108, C49 = 128,1, C70 = 307,933", er["Análisis!C48"] == 108 and er["Análisis!C49 (principal de arrendamientos)"] == 128.1
        and er["Historia!C70 (FCF base que calibra f)"] == 307.933)
    chk("(1b) sensibilidad: pagos −16,8; ROU +10,1; total −6,7", rD["sensibilidad_peso_arrendamiento_1b"] is not None and
        abs(rD["sensibilidad_peso_arrendamiento_1b"]["sensibilidad_pagos_mm (A0, A1 y A2)"] + 16.778) < 1e-3
        and abs(rD["sensibilidad_peso_arrendamiento_1b"]["total_A1_A2_mm"] + 6.660) < 1e-3, json.dumps(rD["sensibilidad_peso_arrendamiento_1b"], ensure_ascii=False))
    ff = next(g for g in rD["guardas"] if g["id"] == "V-F1f")
    chk("V-F1f informa (escala PPA +4,206; ROU −10,118) con el perímetro A2 · aquí se muestra como diagnóstico", "4.206" in ff["detalle"] and "-10.118" in ff["detalle"], ff["detalle"][:200])
    chk("V-F1k (bloque 10): saltos +0,47/+0,68/+2,41 puntos ≤ C179: no avisa", rD["bloque_10_del_libro"] and not any(v["supera_umbral"] for v in rD["bloque_10_del_libro"].values()))
    # integración: ficha e informe provisionales sobre la copia, con la evaluación de las decisiones
    for n in ("motor_a_f1_resultado.json", "motor_a_f1_resultado.md"):
        shutil.copy(os.path.join(dest, "resultado_decisiones_17nov", n), os.path.join(c, n))
    shutil.copy(os.path.join(dest, "motor_a_f1.decisiones_17nov.json"), os.path.join(c, "motor_a_f1.json"))
    rf = subprocess.run([PY, "-I", os.path.join(PV, "scripts", "ficha.py"), c, "--provisional"], capture_output=True, text=True)
    fp = json.load(open(os.path.join(c, "ficha_provisional.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha_provisional.json")) else {}
    chk("ficha provisional de la copia: bloque motor_a_f1 presente, no utilizable, estado pendiente_de_datos",
        rf.returncode == 0 and isinstance(fp.get("motor_a_f1"), dict) and fp["motor_a_f1"]["utilizable_para_conclusion"] is False and fp.get("estado_analisis") == "pendiente_de_datos",
        f"código {rf.returncode} · {rf.stdout.strip()[-200:]} {rf.stderr.strip()[-200:]}")
    rv = subprocess.run([PY, "-I", os.path.join(PV, "scripts", "validar_esquema.py"), os.path.join(c, "ficha_provisional.json"), "ficha"], capture_output=True, text=True)
    chk("la ficha provisional cumple su esquema", rv.returncode == 0, rv.stdout.strip()[-300:])
    ri = subprocess.run([PY, "-I", os.path.join(PV, "scripts", "informe.py"), c, "--provisional"], capture_output=True, text=True)
    inf = open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe_provisional.md")) else ""
    chk("informe provisional de la copia: línea «Motor A · F1»", "Motor A · F1:" in inf, f"código {ri.returncode} {ri.stderr.strip()[-200:]}")
    chk("el libro de la copia no cambia", sha(libro) == SHA_LIBRO)
    chk("el expediente original no cambia (huellas de todos sus archivos)", huellas(ORIG) == h0)
    salida = os.path.join(F1D, "resultados")
    for clave in res:
        for n in ("motor_a_f1_resultado.json", "motor_a_f1_resultado.md"):
            shutil.copy(os.path.join(dest, f"resultado_{clave}", n), os.path.join(salida, f"elis_{clave}_{n}"))
        shutil.copy(os.path.join(dest, f"motor_a_f1.{clave}.json"), os.path.join(salida, f"elis_declaracion_{clave}.json"))
    if "Motor A · F1:" in inf:
        open(os.path.join(salida, "elis_informe_provisional_linea_F1.txt"), "w", encoding="utf-8").write(
            next(l for l in inf.splitlines() if "Motor A · F1:" in l) + "\n")
    out = {"copia": dest, "libro_sha256": SHA_LIBRO, "comprobaciones": comp, "resumen": {"total": len(comp), "pasan": sum(x["ok"] for x in comp)}}
    json.dump(out, open(os.path.join(salida, "regresion_elis_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Regresión F1 de Elis sobre una copia del expediente", "", f"Copia: `{dest}` (fuera del repositorio) · libro `{SHA_LIBRO[:16]}…`", "",
          f"**{out['resumen']['pasan']} de {out['resumen']['total']} comprobaciones pasan.**", "", "| Comprobación | Resultado | Detalle |", "|---|---|---|"]
    md += [f"| {x['comprobacion']} | {'PASA' if x['ok'] else 'FALLA'} | {str(x['detalle']).replace('|', '/')[:220]} |" for x in comp]
    open(os.path.join(salida, "regresion_elis_f1.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{out['resumen']['pasan']}/{out['resumen']['total']} PASAN")
    return 0 if out["resumen"]["pasan"] == out["resumen"]["total"] else 1


if __name__ == "__main__":
    sys.exit(main())
