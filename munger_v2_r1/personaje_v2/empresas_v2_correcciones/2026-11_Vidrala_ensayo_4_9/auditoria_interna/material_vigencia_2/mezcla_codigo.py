"""Combinación histórica: cierre_v2.py (y pipeline.py) antiguos con ficha.py, informe.py y resumen.py actuales, en un árbol temporal
(como arbol_de_codigo de test_integridad_auditoria_v2.py), sobre una copia del cierre de la 4.6.1. Solo ficha.py, informe.py y resumen.py."""
import os, shutil, subprocess, sys, csv
R = "/home/claude/vigencia2_4_9/munger_v2_r1"
B = "/home/claude/vigencia2_4_9/tmp/mezcla"
VERS = {"4.8.1": {"cierre_v2.py": R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/reproduccion/codigo_4_8_1/cierre_v2.py",
                  "pipeline.py": R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/reproduccion/codigo_4_8_1/pipeline.py"},
        "4.8": {"cierre_v2.py": R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/reproduccion/codigo_4_8/cierre_v2.py.txt",
                "pipeline.py": R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/reproduccion/codigo_4_8/pipeline.py.txt"}}
if os.path.exists(B): shutil.rmtree(B)
for v, fs in VERS.items():
    raiz = os.path.join(B, v)
    shutil.copytree(R + "/personaje_v2", raiz + "/personaje_v2", ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(R, x), os.path.join(raiz, x))
    for dst, src in fs.items():
        shutil.copy2(src, raiz + "/personaje_v2/scripts/" + dst)
    exp = os.path.join(raiz, "exp", "Vidrala")
    shutil.copytree(R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala", exp, ignore=shutil.ignore_patterns(".lo_perfil"))
    shutil.copy2(R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/resumen_v2.csv", os.path.join(raiz, "exp", "resumen_v2.csv"))
    scr = raiz + "/personaje_v2/scripts/"
    for s, args in (("informe.py", [exp]), ("resumen.py", [exp, os.path.join(raiz, "exp", "resumen_v2.csv")]), ("ficha.py", [exp, "--estado", "concluido"])):
        r = subprocess.run([sys.executable, "-I", "-B", scr + s, *args], capture_output=True, text=True)
        out = (r.stdout + r.stderr).strip().splitlines()
        print(f"cierre_v2 {v} + {s} actual: código {r.returncode} · traza {'Traceback' in r.stdout + r.stderr} · {out[-1][:120] if out else ''}")
    print("   fila:", [x["verificacion"] for x in csv.DictReader(open(os.path.join(raiz, "exp", "resumen_v2.csv"))) if x["empresa"].startswith("Vidrala")])
