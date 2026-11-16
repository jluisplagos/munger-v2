#!/usr/bin/env python3
"""Octava comprobación · mutaciones de X5 con la BATERÍA ENTERA `test_entrada_efectiva_415.py` (permitida; no usa LibreOffice).
Para cada mutación pedida: árbol ligero en fable/mut8/<nombre>/munger_v2_r1 (scripts/, pruebas/ y esquema/ copiados de fable/copia; el
resto, enlaces al árbol congelado, que solo se lee), se sustituye la línea del «return» de importe_completo y se ejecuta la batería como
la lanza verificar_paquete.sh (cd personaje_v2 && python3 -B pruebas/…), con el sustituto de soffice delante en el PATH.
Uso: python3 -I -B mutaciones8.py m0_sin_el_cambio m1_solo_delante …   (resultado en mut8/<nombre>/resultado.json y bateria.log)"""
import json, os, re, shutil, subprocess, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mutantes8 import LINEA, MUT  # noqa: E402
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1")
COPIA = os.path.join(F, "copia", "munger_v2_r1")


def arbol(nombre):
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
        elif x == "pruebas":   # del árbol congelado (la copia ya tiene salidas de las baterías ejecutadas)
            shutil.copytree(os.path.join(CONG, "personaje_v2", x), n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
        elif x != ".lo_perfil":
            os.symlink(os.path.join(CONG, "personaje_v2", x), n)
    return base, dst


for nombre in sys.argv[1:]:
    linea, sentido, que = MUT[nombre]
    base, dst = arbol(nombre)
    p = os.path.join(dst, "personaje_v2", "scripts", "fase1_historia.py")
    s = open(p, encoding="utf-8").read()
    assert s.count(LINEA) == 1
    open(p, "w", encoding="utf-8").write(s.replace(LINEA, linea))
    env = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ.get("PATH", ""), PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(F, "tmp", "mut8_" + nombre))
    os.makedirs(env["TMPDIR"], exist_ok=True)
    t0 = time.time()
    r = subprocess.run(["nice", "-n", "10", sys.executable, "-B", "pruebas/test_entrada_efectiva_415.py"], cwd=os.path.join(dst, "personaje_v2"), env=env, capture_output=True, text=True)
    out = r.stdout + r.stderr
    open(os.path.join(base, "bateria.log"), "w", encoding="utf-8").write(out + f"\n### rc={r.returncode} segundos={round(time.time() - t0)}\n")
    fallan = [l[:230] for l in out.split("\n") if re.match(r"^\[.*\] FALLA", l)]
    m = re.search(r"^(\d+)/(\d+) pruebas de la entrada efectiva \(4\.15\) PASAN$", out, re.M)
    res = {"mutacion": nombre, "sentido": sentido, "que": que, "linea": linea.strip(), "rc": r.returncode, "recuento": m.group(0) if m else None,
           "detectada": r.returncode != 0 and bool(fallan), "fallan": fallan, "segundos": round(time.time() - t0)}
    json.dump(res, open(os.path.join(base, "resultado.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{nombre}: rc={r.returncode} · {m.group(0) if m else 'sin recuento'} · {'DETECTADA' if res['detectada'] else 'NO detectada'} · fallan {len(fallan)}: {[x[:140] for x in fallan]}", flush=True)
