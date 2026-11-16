#!/usr/bin/env python3
"""Octava comprobación · X2 con la BATERÍA ENTERA `test_verificacion_entradas_415.py` (permitida; no usa LibreOffice): las dos mutaciones de
la línea :542 de verificacion_entradas.py que en la séptima pasaban 190/190 con las pruebas de 45ff57c:
  v7c_lectura_sin_apostrofo_detras  · el límite final sin apóstrofos: «849» vuelve a leerse dentro de «849'697» (la de W1 que quedó sin prueba)
  x1_solo_tipografico_delante       · el límite inicial solo con «’» (la línea de 45ff57c: el descuido X1)
Árbol ligero en fable/mut8/<nombre>/munger_v2_r1 (scripts/ y esquema/ de fable/copia; pruebas/ del árbol congelado; el resto, enlaces).
Uso: python3 -I -B mutaciones8_ve.py [nombre …]"""
import json, os, re, shutil, subprocess, sys, time
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1")
COPIA = os.path.join(F, "copia", "munger_v2_r1")
LINEA = r'''        for m in re.finditer(r"(?<![\d.,])(?<!\d['’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7'''
MUT = {"v7c_lectura_sin_apostrofo_detras": LINEA.replace(r"""(?!\d|[.,'’]\d)", t)""", r"""(?!\d|[.,]\d)", t)"""),
       "x1_solo_tipografico_delante": LINEA.replace(r"""(?<!\d['’])" + re.escape(c)""", r"""(?<!\d[’])" + re.escape(c)""")}
assert all(v != LINEA for v in MUT.values())
for nombre in sys.argv[1:] or list(MUT):
    base = os.path.join(F, "mut8", nombre)
    if os.path.lexists(base):
        shutil.rmtree(base)
    dst = os.path.join(base, "munger_v2_r1")
    os.makedirs(os.path.join(dst, "personaje_v2"))
    for x in os.listdir(CONG):
        if x != "personaje_v2":
            os.symlink(os.path.join(CONG, x), os.path.join(dst, x))
    for x in os.listdir(os.path.join(CONG, "personaje_v2")):
        n = os.path.join(dst, "personaje_v2", x)
        if x in ("scripts", "esquema"):
            shutil.copytree(os.path.join(COPIA, "personaje_v2", x), n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
        elif x == "pruebas":
            shutil.copytree(os.path.join(CONG, "personaje_v2", x), n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
        elif x != ".lo_perfil":
            os.symlink(os.path.join(CONG, "personaje_v2", x), n)
    p = os.path.join(dst, "personaje_v2", "scripts", "verificacion_entradas.py")
    s = open(p, encoding="utf-8").read()
    assert s.count(LINEA) == 1
    open(p, "w", encoding="utf-8").write(s.replace(LINEA, MUT[nombre]))
    env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", ""), PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(F, "tmp", "mut8_" + nombre))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    t0 = time.time()
    r = subprocess.run(["nice", "-n", "10", sys.executable, "-B", "pruebas/test_verificacion_entradas_415.py"], cwd=os.path.join(dst, "personaje_v2"), env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    open(os.path.join(base, "bateria.log"), "w", encoding="utf-8").write(out + f"\n### rc={r.returncode} segundos={round(time.time() - t0)}\n")
    fallan = [l[:260] for l in out.split("\n") if re.match(r"^\[.*\] FALLA", l)]
    m = re.search(r"^(\d+)/(\d+) pruebas de la corrección de la verificación de las entradas \(4\.15\) PASAN$", out, re.M)
    res = {"mutacion": nombre, "linea": MUT[nombre].strip(), "rc": r.returncode, "recuento": m.group(0) if m else None, "detectada": r.returncode != 0 and bool(fallan), "fallan": fallan, "segundos": round(time.time() - t0)}
    json.dump(res, open(os.path.join(base, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{nombre}: rc={r.returncode} · {m.group(0) if m else 'sin recuento'} · {'DETECTADA' if res['detectada'] else 'NO detectada'} · fallan {len(fallan)}: {[x[:200] for x in fallan]}", flush=True)
