"""Hallazgo 16 (I9): informe.py del árbol CONGELADO sobre la ficha guardada de la 4.14 (copia en /tmp; sin regenerar la ficha)."""
import json, os, re, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable2/congelado/personaje_v2")
tmp = tempfile.mkdtemp(prefix="rev_fable_i9_")
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala"):
    src = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", exp); nom = os.path.basename(src); d = os.path.join(tmp, exp.split("/")[0], nom)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("recalc", "variantes_v64", ".lo_perfil", "prompts_generados", "fuentes_pdf", "texto"))
    cfg = os.path.join(PV, json.load(open(os.path.join(d, "plantilla_activa.json"), encoding="utf-8"))["config"])
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), d, "--provisional"], capture_output=True, text=True, env=dict(os.environ, MUNGER_CONFIG=cfg))
    inf = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read()
    m = re.search(r"Verificación de las entradas financieras:\*\*.{0,260}", inf)
    print(f"{exp}: informe.py rc {r.returncode} | {m.group(0) if m else '(sin línea)'} | «330 de 232»/«347 de 226» presente: {bool(re.search(r'(330 de 232|347 de 226)', inf))}")
shutil.rmtree(tmp, ignore_errors=True)
