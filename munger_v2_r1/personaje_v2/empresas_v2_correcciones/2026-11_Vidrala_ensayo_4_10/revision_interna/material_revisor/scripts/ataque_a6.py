"""A6 (revisión interna 4.10): ficha sin marcadores (ambos) con cierre_vigente.json ilegible (JSON roto) y con cierre_vigente.json que es una carpeta."""
import csv, json, os, shutil, subprocess, sys, tempfile
RAIZ = os.path.abspath(sys.argv[1]); SCR = os.path.join(RAIZ, "scripts")
sys.path.insert(0, SCR); sys.path.insert(0, os.path.join(RAIZ, "pruebas")); sys.dont_write_bytecode = True
import agentes_sinteticos as AG  # noqa
PY = sys.executable
EXP = os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
TMP = tempfile.mkdtemp(prefix="rev410a6_", dir=os.environ.get("TMPDIR"))
def corre(s, *a):
    r = subprocess.run([PY, "-B", os.path.join(SCR, s), *a], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}); return r.returncode, (r.stdout + r.stderr).strip()
base = os.path.join(TMP, "c"); d = os.path.join(base, "exp", "Vidrala"); pred = os.path.join(base, "exp", "resumen_v2.csv")
shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
    if os.path.exists(os.path.join(os.path.dirname(EXP), f)): shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(base, "exp", f))
corre("pipeline.py", d, "--desde", "13"); AG.auditoria(d, "APROBADO"); rc0, _ = corre("pipeline.py", d)
for nombre in ("cv_json_roto", "cv_carpeta"):
    b2 = os.path.join(TMP, nombre); shutil.copytree(base, b2, symlinks=True); d2 = os.path.join(b2, "exp", "Vidrala"); p2 = os.path.join(b2, "exp", "resumen_v2.csv")
    F = json.load(open(os.path.join(d2, "ficha.json"), encoding="utf-8")); F.pop("cierre", None); F["estado_analisis"] = "pendiente_de_datos"
    json.dump(F, open(os.path.join(d2, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False)
    cv = os.path.join(d2, "cierre_vigente.json"); os.remove(cv)
    if nombre == "cv_json_roto": open(cv, "w").write("{roto")
    else: os.makedirs(cv)
    rc, out = corre("resumen.py", d2, p2)
    st = json.load(open(os.path.join(d2, "estado_pipeline.json"), encoding="utf-8"))
    fil = [(r.get("estado_analisis"), (r.get("verificacion") or "")[:24]) for r in csv.DictReader(open(p2, encoding="utf-8"))]
    print(f"A6 {nombre}: cierre de partida {rc0} · resumen.py → {rc} · filas {fil} · auditoria {st.get('auditoria')!r} · {out[-170:]}")
shutil.rmtree(TMP, ignore_errors=True)
