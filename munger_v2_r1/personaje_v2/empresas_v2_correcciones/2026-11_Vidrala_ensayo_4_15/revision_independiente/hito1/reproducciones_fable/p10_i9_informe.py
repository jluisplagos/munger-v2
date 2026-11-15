"""I9: informe.py vigente sobre la ficha guardada de un expediente final de la 4.14 (copia en /tmp; sin regenerar la ficha): ¿sigue saliendo «330 de 232»?"""
import hashlib, json, os, re, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable/trabajo_copia/personaje_v2")
tmp = tempfile.mkdtemp(prefix="rev_fable_i9_")
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala"):
    src = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", exp); nom = os.path.basename(src); d = os.path.join(tmp, exp.split("/")[0], nom)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("recalc", "variantes_v64", ".lo_perfil", "prompts_generados", "fuentes_pdf", "texto"))
    cfg = os.path.join(PV, json.load(open(os.path.join(d, "plantilla_activa.json"), encoding="utf-8"))["config"])
    ve = (json.load(open(os.path.join(d, "ficha_provisional.json"), encoding="utf-8")).get("aptitud_de_uso") or {}).get("verificacion_entradas") or {}
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), d, "--provisional"], capture_output=True, text=True, env=dict(os.environ, MUNGER_CONFIG=cfg))
    inf = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read()
    m = re.search(r"Verificación de las entradas financieras:\*\* [^·]*·", inf)
    print(f"{exp}: ficha guardada → comprobadas {ve.get('comprobadas')}, universo {ve.get('universo')}, 'comprobadas_universo' presente: {'comprobadas_universo' in ve} | informe.py rc {r.returncode} | {m.group(0) if m else '(sin línea)'}")
shutil.rmtree(tmp, ignore_errors=True)
