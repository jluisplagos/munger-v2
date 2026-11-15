"""Diagnóstico (no acredita nada): aplica R1–R3 a los registros reales de la 4.14 con un vínculo SIMULADO (huella actual) y sin las
celdas de juicio, para saber si su contenido tiene defectos de página, conservación o redondeo. Trabaja en copias temporales.
Uso (desde personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/): python3 -I -B ../2026-11_Vidrala_ensayo_4_15/scripts/diagnostico_registros_4_14.py
    ../../../personaje_v2 viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala elis_decisiones/Elis > SALIDA.json"""
import json, os, shutil, sys, tempfile
PV = sys.argv[1]; sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE
res = {}
for exp in sys.argv[2:]:
    tmp = tempfile.mkdtemp(prefix="diag_"); dst = os.path.join(tmp, os.path.basename(exp))
    shutil.copytree(exp, dst, ignore=shutil.ignore_patterns("recalc", "variantes_v64", "prompts_generados", ".lo_perfil", "historial_cierres", "antecedentes"))
    reg = json.load(open(os.path.join(dst, VE.REGISTRO), encoding="utf-8")); reg["formato"] = "4.15"
    hs = VE.huellas_registro(dst, reg)
    for e in reg["entradas"]:
        c = e.setdefault("comprobacion", {}) or {}
        e["comprobacion"] = c; c["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": c.get("revisor"), "fecha": c.get("fecha")}
    json.dump(reg, open(os.path.join(dst, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False)
    r = VE.comprobar(dst)
    calc = {k for k, a in VE.universo(dst)["ambito"].items() if a == "calculo"}
    pend_calc = [x for x in r["pendientes"] if x.split(":")[0] in calc or x.startswith("aux:")]
    res[os.path.basename(exp)] = {"comprobadas_calculo": r["comprobadas_calculo"], "universo_calculo": r["universo_calculo"],
        "errores": r["errores"], "discrepancias": r["discrepancias"], "desactualizadas": r["desactualizadas"],
        "pendientes_calculo_o_aux": pend_calc, "lecturas_externas": r["lecturas_externas"], "datos_como_hipotesis": r["datos_como_hipotesis"],
        "entradas_no_reproducibles": r["entradas_no_reproducibles"]}
    shutil.rmtree(tmp, ignore_errors=True)
json.dump(res, sys.stdout, ensure_ascii=False, indent=1)
