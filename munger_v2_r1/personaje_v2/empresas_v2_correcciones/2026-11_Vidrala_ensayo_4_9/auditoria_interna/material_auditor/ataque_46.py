#!/usr/bin/env python3
"""Auditoría interna 4.9: expediente cerrado de la 4.6 (material fijado, sin cierre_vigente.json, sin solicitudes), copiado a tmp.
Se sustituye auditoria.md por otra APROBADO sintética que nombra el material fijado y se llama a ficha.py, informe.py y resumen.py."""
import hashlib, json, os, shutil, subprocess, sys
sys.dont_write_bytecode = True
R = "/home/claude/auditoria_4_9/munger_v2_r1/personaje_v2"
sys.path.insert(0, os.path.join(R, "pruebas"))
import agentes_sinteticos as AG
SCR = os.path.join(R, "scripts")
src = os.path.join(R, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6", "Vidrala")
base = "/home/claude/auditoria_4_9/tmp/escenarios/x_46"
shutil.rmtree(base, ignore_errors=True)
d = os.path.join(base, "exp", "Vidrala")
shutil.copytree(src, d, ignore=shutil.ignore_patterns(".lo_perfil"))
env = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/home/claude/auditoria_4_9/tmp/tmpdir"}
def corre(s, *a):
    r = subprocess.run([sys.executable, "-B", os.path.join(SCR, s), *a], capture_output=True, text=True, env=env)
    return r.returncode, (r.stdout + r.stderr).strip().splitlines()[-1][:200]
sha0 = hashlib.sha256(open(os.path.join(d, "auditoria.md"), "rb").read()).hexdigest()
AG.auditoria(d, "APROBADO", solicitud=False)
open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("Aviso: auditoría distinta de la que aprobó el cierre de la 4.6 (prueba del auditor interno).\n")
print("ficha.py", corre("ficha.py", d, "--estado", "concluido"))
print("informe.py", corre("informe.py", d))
csvp = os.path.join(base, "exp", "resumen_v2.csv")
print("resumen.py", corre("resumen.py", d, csvp))
cv = json.load(open(os.path.join(d, "cierre_vigente.json"))) if os.path.exists(os.path.join(d, "cierre_vigente.json")) else None
print("cierre_vigente.json creado:", cv)
print("sha auditoría original", sha0, "· nueva", hashlib.sha256(open(os.path.join(d, "auditoria.md"), "rb").read()).hexdigest())
import csv
print([ (r["estado_analisis"], r["verificacion"]) for r in csv.DictReader(open(csvp)) if r["empresa"].startswith("Vidrala")])
