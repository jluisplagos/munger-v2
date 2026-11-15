#!/usr/bin/env python3
"""s20 · ¿Se ha rebajado alguna prueba existente? Las baterías del HITO 1 (test_verificacion_entradas_415.py, 105 pruebas, y
test_entrada_efectiva_415.py, 40 pruebas; copias de reproduccion/codigo_4_15_hito1/) ejecutadas contra el CÓDIGO del hito 2, en un árbol
ligero aparte. Única adaptación: la aserción de R3 que el hito 2 cambia a propósito («(149,5)» ya no vale para +149,5) se quita de la
batería vieja para que el resto se ejecute (una aserción que falla aborta el guion). Todo lo demás, sin tocar."""
import importlib.util, json, os, re, shutil, subprocess, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("mutaciones", os.path.join(F, "sondas", "mutaciones.py"))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
m.MUT = os.path.join(F, "mut_pruebas_hito1")
d = m.preparar("codigo_hito2")
H1 = os.path.join(m.COPIA, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "reproduccion", "codigo_4_15_hito1")
env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ["PATH"], TMPDIR=os.path.join(F, "tmp"))
for b in ("test_entrada_efectiva_415.py", "test_verificacion_entradas_415.py"):
    s = open(os.path.join(H1, b + ".txt"), encoding="utf-8").read()
    if b == "test_verificacion_entradas_415.py":
        viejo = ' and VE._cita_contiene("(149,5)", 149.5)\n'
        assert s.count(viejo) == 1
        s = s.replace(viejo, "  # (revisor) aserción de «(149,5)» para +149,5 retirada: el hito 2 la cambia a propósito\n")
    open(os.path.join(d, "personaje_v2", "pruebas", b), "w", encoding="utf-8").write(s)
    r = subprocess.run([sys.executable, "-B", os.path.join("pruebas", b)], cwd=os.path.join(d, "personaje_v2"), capture_output=True, text=True, env=env, timeout=1500)
    out = r.stdout + r.stderr
    open(os.path.join(m.MUT, "codigo_hito2", b + ".log"), "w", encoding="utf-8").write(out)
    fallan = [l[:330] for l in out.splitlines() if re.match(r"^\[[A-Za-z0-9]+\] FALLA", l)]
    mm = re.search(r"(?m)^(\d+)/(\d+) pruebas.*$", out)
    print(f"{b} (hito 1) con el código del hito 2: código {r.returncode} · {mm.group(0) if mm else out.strip().splitlines()[-1][:200]}")
    for x in fallan:
        print("    ", x)
shutil.rmtree(d, ignore_errors=True)
