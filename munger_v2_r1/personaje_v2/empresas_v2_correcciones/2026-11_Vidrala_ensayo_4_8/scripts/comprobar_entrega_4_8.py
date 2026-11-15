#!/usr/bin/env python3
"""Control de la entrega 4.8 (X-a, X-c y P-M1). Se ejecuta sobre una descompresión limpia, después de `verificar_paquete.sh completa`.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8/scripts/comprobar_entrega_4_8.py   (desde munger_v2_r1/)

Cada comprobación se marca con su naturaleza: [reejecuta] vuelve a ejecutar código; [recalcula] recalcula una cifra desde los datos;
[constata] comprueba que un archivo o un texto existe o no cambió. Escribe en temporales; analisis_pm1.py reescribe sus propias
salidas de ../financiero con el mismo contenido (se comprueba con las huellas del manifiesto). Código 0 si todo cumple.
"""
import csv
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
P2 = os.path.abspath(os.path.join(CORR, ".."))
RAIZ = os.path.dirname(P2)
PY = sys.executable
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}
R = []


def ok(n, natur, cond, det=""):
    R.append(bool(cond))
    print(("CUMPLE  " if cond else "NO CUMPLE") + f" · [{natur}] {n}" + (f" · {det}" if det else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def manifiesto(p):
    out = {}
    for l in open(p, encoding="utf-8"):
        if l.startswith("#") or not l.strip():
            continue
        h, ruta = l.rstrip("\n").split("  ", 1)
        out[ruta] = h
    return out


def run(cmd, cwd=None):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, env=ENV)
    return r.returncode, r.stdout + r.stderr


def arbol_codigo_471(tmp):
    """Árbol de código de la 4.7.1: el de este paquete con pipeline.py y ficha.py sustituidos por las copias de la 4.7.1
    (reproduccion/codigo_4_7_1/*.py.txt), comprobadas contra el manifiesto de la 4.7.1. v6 y el kit se enlazan."""
    m471 = manifiesto(os.path.join(AQUI, "reproduccion", "MANIFIESTO_SHA256_4_7_1.txt"))
    raiz = os.path.join(tmp, "arbol471")
    os.makedirs(raiz)
    shutil.copytree(P2, os.path.join(raiz, "personaje_v2"), ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", ".lo_perfil", "__pycache__", "sintetico"))
    os.makedirs(os.path.join(raiz, "personaje_v2", "empresas_v2_correcciones"))
    os.symlink(os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1"), os.path.join(raiz, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(RAIZ, x), os.path.join(raiz, x))
    iguales = True
    for f in ("pipeline.py", "ficha.py"):
        dst = os.path.join(raiz, "personaje_v2", "scripts", f)
        shutil.copy(os.path.join(AQUI, "reproduccion", "codigo_4_7_1", f + ".txt"), dst)
        iguales &= sha(dst) == m471[f"personaje_v2/scripts/{f}"]
    for f in ("cierre_v2.py", "informe.py", "resumen.py", "diagnostico.py", "validar_esquema.py"):
        iguales &= sha(os.path.join(raiz, "personaje_v2", "scripts", f)) == m471[f"personaje_v2/scripts/{f}"]
    return raiz, iguales


tmp = tempfile.mkdtemp(prefix="c48_")
try:
    m48 = manifiesto(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"))
    m471 = manifiesto(os.path.join(AQUI, "reproduccion", "MANIFIESTO_SHA256_4_7_1.txt"))
    ok("VERSION dice entrega 4.8", "constata", "entrega 4.8" in open(os.path.join(RAIZ, "VERSION"), encoding="utf-8").readline())
    ok("el manifiesto de la 4.7.1 conservado es el de su paquete (1.454 archivos)", "constata", len(m471) == 1454)
    # --- X-a y X-c
    raiz471, iguales471 = arbol_codigo_471(tmp)
    ok("el código 4.7.1 reconstruido (pipeline.py, ficha.py) tiene las huellas del manifiesto 4.7.1, y el resto del código del cierre no cambió", "constata", iguales471)
    rep = os.path.join(AQUI, "scripts", "reproducir_xa_xc.py")
    rc, out = run([PY, "-I", rep, "--raiz", raiz471, "--etiqueta", "entrega 4.7.1"])
    ok("reproducción con el código 4.7.1: X-a y X-c incoherentes, salida idéntica a la de referencia", "reejecuta",
       out == open(os.path.join(AQUI, "reproduccion", "reproduccion_xa_xc_codigo_4_7_1.txt"), encoding="utf-8").read(), out.strip().splitlines()[-1] if out.strip() else "")
    rc, out = run([PY, "-I", rep, "--raiz", RAIZ, "--etiqueta", "entrega 4.8"])
    ok("reproducción con el código 4.8: X-a y X-c coherentes en la primera ejecución, salida idéntica a la de referencia", "reejecuta",
       out == open(os.path.join(AQUI, "reproduccion", "reproduccion_xa_xc_codigo_4_8.txt"), encoding="utf-8").read() and "X-A coherente · X-C coherente" in out, out.strip().splitlines()[-1] if out.strip() else "")
    rc, out = run([PY, "-B", os.path.join("pruebas", "test_estados_v2.py")], cwd=P2)
    ok("batería de estados con el código 4.8: 28/28", "reejecuta", rc == 0 and out.strip().endswith("28/28 pruebas de coherencia de estados PASAN"), out.strip().splitlines()[-1])
    shutil.copy(os.path.join(P2, "pruebas", "test_estados_v2.py"), os.path.join(raiz471, "personaje_v2", "pruebas", "test_estados_v2.py"))
    rc, out = run([PY, "-B", os.path.join("pruebas", "test_estados_v2.py"), "--expediente", os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")], cwd=os.path.join(raiz471, "personaje_v2"))
    ref = open(os.path.join(AQUI, "reproduccion", "test_estados_con_codigo_4_7_1.txt"), encoding="utf-8").read()
    fallan = lambda t: sorted(l.split(" · ")[1] + " · " + l.split(" · ")[2] for l in t.splitlines() if l.startswith("FALLA"))
    ok("batería de estados con el código 4.7.1: 17/28, con las mismas 11 pruebas fallidas que la referencia (X-a, incluida la vía del código 5; X-c, incluida la subsanación con el diagnóstico anterior)", "reejecuta",
       out.strip().endswith("17/28 pruebas de coherencia de estados PASAN") and fallan(out) == fallan(ref) and len(fallan(out)) == 11, f"{len(fallan(out))} fallan")
    sys.path.insert(0, os.path.join(P2, "scripts"))
    sys.dont_write_bytecode = True
    import pipeline  # noqa: E402
    ok("la regla H2 (Pipeline.veredicto_auditoria) es idéntica a la de la 4.7.1", "recalcula",
       hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest() == "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422")
    vp = open(os.path.join(RAIZ, "verificar_paquete.sh"), encoding="utf-8").read()
    ok("verificar_paquete.sh completa ejecuta la batería de estados como obligatoria (al menos 28 pruebas), antes del bloque del resumen", "constata",
       "pruebas/test_estados_v2.py" in vp and '-ge 28' in vp and "RESULTADO estados: FALLA" in vp and vp.index("== batería de coherencia de estados") < vp.index("== batería del resumen") < vp.index("== batería de cierre"))
    ok("verificar_paquete.sh conserva las baterías del resumen (≥ 45) y de cierre (≥ 55)", "constata", '-ge 45' in vp and '-ge 55' in vp)
    ad = open(os.path.join(P2, "ANEXO_D_salidas_y_formatos.md"), encoding="utf-8").read()
    ok("el Anexo D describe X-a, X-c y las precisiones de X-d", "constata", "(4.8, X-a)" in ad and "(4.8, X-c)" in ad and "precisión X-d" in ad and "3-Nov-26" in ad)
    # --- P-M1
    pm1 = os.path.join(AQUI, "scripts", "analisis_pm1.py")
    sal_tmp = os.path.join(tmp, "pm1_salidas")
    rc, out = run([PY, "-I", pm1, "--salida", sal_tmp])
    ok("analisis_pm1.py (en un temporal): réplica 4.7.1 idéntica, 94 datos de evidencia reproducidos y controles cumplidos", "reejecuta",
       rc == 0 and "evidencia: 94 datos, 94 reproducen" in out and "RESULTADO: todos los controles cumplen" in out, out.strip().splitlines()[-1] if out.strip() else "")
    salidas = sorted(f for f in os.listdir(sal_tmp)) if os.path.isdir(sal_tmp) else []
    ok("las salidas pm1_* regeneradas en el temporal son idénticas byte a byte a las del paquete y a sus huellas del manifiesto (las 7 pm1_*)", "reejecuta",
       len(salidas) == 7 and all(sha(os.path.join(sal_tmp, f)) == sha(os.path.join(AQUI, "financiero", f)) == m48.get(f"personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8/financiero/{f}") for f in salidas), f"{len(salidas)} archivos")
    res = json.load(open(os.path.join(AQUI, "financiero", "pm1_resultados.json"), encoding="utf-8"))
    alt = {r["clave"]: r for r in csv.DictReader(open(os.path.join(AQUI, "financiero", "pm1_alternativas.csv"), encoding="utf-8"))}
    ok("REF reproduce T1·M1·R1 de la 4.7.1 (ponderado 69,2447; precio de Sí 64,2622)", "recalcula", alt["REF"]["ponderado"] == "69.2447" and alt["REF"]["precio_si"] == "64.2622")
    s471 = [r for r in csv.DictReader(open(os.path.join(CORR, "2026-11_Vidrala_ensayo_4_7_1", "financiero", "sensibilidades_n3.csv"), encoding="utf-8"))
            if r["base"] == "T1·M1" and r["regla"] == "R1" and r["alcance"] == "todos los escenarios" and r["mantenimiento"].endswith("(exceso de 2025)")]
    ok("X41 reproduce exactamente (4 decimales) la sensibilidad de la 4.7.1 «+41,8 % todos los escenarios»", "recalcula",
       len(s471) == 1 and alt["X41"]["ponderado"] == s471[0]["ponderado"] and alt["X41"]["precio_si"] == s471[0]["precio_si"] and res["controles"]["x41"], f"{alt['X41']['ponderado']} / {alt['X41']['precio_si']}")
    lam = lambda L, pi: 1 / (sum((1 + pi) ** -k for k in range(L)) / L)
    c = res["constantes"]
    ok("λ recalculado: (12 años, 2 %) = 1,112; (12, 3 %) = 1,170; (16, 3 %) = 1,237; balance 1 + π·VNC/dotación = 1,192 (2 %); central 1,15 y rango 1,10–1,25", "recalcula",
       abs(lam(12, .02) - c["lambda"]["l12_pi2"]) < 1e-12 and abs(lam(12, .03) - c["lambda"]["l12_pi3"]) < 1e-12 and abs(lam(16, .03) - c["lambda"]["l16_pi3"]) < 1e-12
       and abs(1 + 0.02 * (2194513 - 1026815 - 32569) / 118275 - c["lambda"]["balance"]["0.02"]) < 1e-9 and (c["lambda"]["central"], c["lambda"]["bajo"], c["lambda"]["alto"]) == (1.15, 1.10, 1.25))
    seg = list(csv.DictReader(open(os.path.join(AQUI, "financiero", "pm1_segmentos.csv"), encoding="utf-8")))
    uk = [r for r in seg if r["segmento"] == "Reino Unido e Irlanda"]
    ok("ciclo del Reino Unido 2018–2025 recalculado desde la tabla de segmentos = 1,095", "recalcula",
       len(uk) == 8 and abs(sum(float(r["inversiones"]) for r in uk) / sum(float(r["amortizacion"]) for r in uk) - c["uk_ciclo"][0]) < 1e-6 and abs(c["uk_ciclo"][0] - 1.0954) < 1e-3)
    filas = list(csv.DictReader(open(os.path.join(AQUI, "financiero", "pm1_anio_a_anio.csv"), encoding="utf-8")))
    m1 = [f for f in filas if f["alternativa"] == "P1" and f["escenario"] == "MALO" and f["anio"] == "1"][0]
    ok("P1, MALO, año 1: reposición adicional = 0,15 × (132,948 − 4,492) = 19,2684 con inversión fija neta 0", "recalcula",
       abs(float(m1["reposicion_adicional"]) - 0.15 * (132.948 - 4.492)) < 1e-4 and float(m1["inversion_fija_neta"]) == 0.0)
    p5 = [f for f in filas if f["alternativa"] == "P5" and f["escenario"] == "NORMAL" and f["anio"] == "1"][0]
    ex = (sum(c_ for c_ in [188.503 - 132.948, 168.8 - 117.72, 151.7 - 87.21, 120.2 - 85.46, 109.8 - 86.284]) + 4.921 + 4.492) / 5
    ok("P5, NORMAL, año 1: adicional = exceso medio 2021–2025 sobre la amortización que se repone (47,7588) − inversión fija neta del modelo", "recalcula",
       abs(float(p5["reposicion_adicional"]) - (c["exceso_medio_propio"] - float(p5["inversion_fija_neta"]))) < 1e-4 and abs(c["exceso_medio_propio"] - ex) < 1e-3)
    p3 = [f for f in filas if f["alternativa"] == "P3" and f["escenario"] == "MALO" and f["anio"] == "10"][0]
    ok("P3, MALO, año 10: la inversión que recupera capacidad no rebaja el adicional de reposición (Z-c): adicional = 0,15 × (D&A − cartera)", "recalcula",
       float(p3["inversion_fija_neta"]) > 0 and abs(float(p3["reposicion_adicional"]) - 0.15 * c["DA25"]) < 1e-4 and float(alt["P3"]["ponderado"]) < float(alt["P1"]["ponderado"]))
    ident = all(abs(float(f["fcf"]) - (float(f["nopat"]) + c["DA25"] - float(f["inversion_bruta_caja"]) - float(f["delta_circulante"]) + float(f["escudo_fiscal_ola"]))) < 1e-3
                for f in filas if f["anio"] != "11")
    ok("identidad FCF = NOPAT + D&A − inversión bruta de caja − Δcirculante (+ escudo de la ola) en todas las filas de los años 1–10", "recalcula", ident)
    nrm = [f for f in filas if f["alternativa"] == "REF" and f["escenario"] == "NORMAL" and f["anio"] != "11"]
    x = res["constantes"]["exceso_2025"] / c["DA25"]
    ok("doble cómputo de X41 en el NORMAL recalculado = Σ min(0,418 × D&A, inversión fija neta) ≈ 309", "recalcula",
       abs(sum(min(x * c["DA25"], max(0.0, float(f["inversion_fija_neta"]))) for f in nrm) - res["doble_computo_x41"]["NORMAL"]) < 0.5 and abs(res["doble_computo_x41"]["NORMAL"] - 309.3) < 0.1)
    ev = {e["clave"]: e for e in json.load(open(os.path.join(AQUI, "financiero", "pm1_evidencia.json"), encoding="utf-8"))}
    ok("X-e: depreciación de derechos de uso 2025 = 6.760 en el PDF español (p. 58) y en el texto inglés; 2024 = 4.768", "recalcula",
       ev["rou_dep_2025"]["reproduce"] and ev["rou_dep_2025"]["pagina_pdf"] == 58 and ev["rou_dep_2025_en"]["reproduce"] and ev["rou_dep_2024"]["valor"] == "4.768")
    fx = json.load(open(os.path.join(AQUI, "fuentes", "fuentes_externas_pm1.json"), encoding="utf-8"))
    ok("fuentes externas: cada una con URL, fecha y marca de posterior a la base; las oficiales con huella SHA-256 y página de cada cita", "constata",
       all(f.get("url") and f.get("fecha") and "posterior_a_base" in f for f in fx["fuentes"])
       and all(re.fullmatch(r"[0-9a-f]{64}", f.get("sha256", "")) and all("pagina" in c_ for c_ in f["citas"]) for f in fx["fuentes"] if f["tipo"].startswith("oficial")))
    dec = json.load(open(os.path.join(AQUI, "financiero", "decisiones_y_preguntas_4_8.json"), encoding="utf-8"))
    ok("decisiones: ningún campo humano relleno (decision, fecha, confirmado_por vacíos)", "constata",
       all(d.get("decision") in (None, "") and d.get("fecha") in (None, "") and d.get("confirmado_por") in (None, "") for d in dec["decisiones"]))
    # --- conservación
    cambian = {"VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "CAMBIOS_ARCHIVOS.txt", "MANIFIESTO_SHA256.txt", "verificar_paquete.sh",
               "personaje_v2/scripts/pipeline.py", "personaje_v2/scripts/ficha.py", "personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/DECISIONES.md"}
    distintos = sorted(r for r, h in m471.items() if r not in cambian and m48.get(r) != h)
    ok("respecto a la 4.7.1 solo cambian los archivos declarados; ninguno desaparece", "constata", not distintos and all(r in m48 for r in m471 if r != "MANIFIESTO_SHA256.txt"), str(distintos[:5]))
    orig = [r for r in m471 if r.startswith("personaje_v2/empresas_v2/")]
    ok("los 489 originales de personaje_v2/empresas_v2/ conservan su huella", "constata", len(orig) == 489 and all(m48.get(r) == m471[r] for r in orig))
    prev = [r for r in m471 if r.startswith("personaje_v2/empresas_v2_correcciones/")]
    ok("los expedientes de correcciones anteriores (4.4 a 4.7.1) conservan su huella en los archivos reales", "constata",
       all(os.path.exists(os.path.join(RAIZ, r)) and sha(os.path.join(RAIZ, r)) == m471[r] for r in prev + orig), f"{len(prev)} + {len(orig)} archivos")
    protegidos = ("personaje_v2/empresas_v2/", "personaje_v2/empresas_v2_correcciones/")
    nuevos = sorted(r for r in m48 if r.startswith(protegidos) and r not in m471 and not r.startswith("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8/"))
    reales = []
    for d_, _, fs in os.walk(os.path.join(P2, "empresas_v2")):
        reales += [os.path.relpath(os.path.join(d_, f), RAIZ) for f in fs]
    for x in os.listdir(CORR):
        if x != "2026-11_Vidrala_ensayo_4_8":
            for d_, _, fs in os.walk(os.path.join(CORR, x)):
                reales += [os.path.relpath(os.path.join(d_, f), RAIZ) for f in fs]
    de_mas = sorted(r for r in reales if r not in m471)
    ok("ningún archivo añadido en los originales ni en los expedientes anteriores (ni en el manifiesto ni en el disco)", "constata", not nuevos and not de_mas, str((nuevos + de_mas)[:3]))
    for nombre, guion, ref in (("4.6.1", "2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_integracion_verificador.py", "2026-11_Vidrala_ensayo_4_6_1/resultados/comprobar_integracion_verificador_salida.txt"),
                               ("4.7.1", "2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_integracion_verificador_471.py", "2026-11_Vidrala_ensayo_4_7_1/resultados/comprobar_integracion_verificador_471_salida.txt"),
                               ("4.8", "2026-11_Vidrala_ensayo_4_8/scripts/comprobar_integracion_verificador_48.py", "2026-11_Vidrala_ensayo_4_8/resultados/comprobar_integracion_verificador_48_salida.txt")):
        rc, out = run([PY, "-I", os.path.join(CORR, guion)])
        ok(f"control de integración del verificador de la {nombre}: 13 de 13 y salida idéntica a la de referencia", "reejecuta",
           rc == 0 and out.strip() == open(os.path.join(CORR, ref), encoding="utf-8").read().strip(), out.strip().splitlines()[-1] if out.strip() else "")
    p1 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "fase1_decisiones.json")
    ok("registro humano P1 intacto (b4e47afc…c445a4)", "constata", sha(p1) == "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4")
    for f in ("CIERRE_TECNICO_4_8.md", "INFORME_PM1.md", "REGISTRO_ENTREGA_4.8.md"):
        ok(f"existe {f}", "constata", os.path.exists(os.path.join(AQUI, f)))
finally:
    shutil.rmtree(tmp, ignore_errors=True)
n = sum(R)
print(f"\nRESULTADO: {n} de {len(R)} comprobaciones cumplen.")
sys.exit(0 if n == len(R) else 1)
