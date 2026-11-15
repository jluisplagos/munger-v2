#!/usr/bin/env python3
"""Genera y recalcula (LibreOffice, en secuencia) un libro V6.4 por cada caso de casos_v64.py.

Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/generar_libros_casos.py DIR_SALIDA [--solo id1,id2] [--plantilla P.xlsx]
Escribe DIR_SALIDA/<id>.xlsx (sin recalcular), DIR_SALIDA/rc/<id>.xlsx (recalculado) y DIR_SALIDA/manifiesto_casos.json
(caso, entradas escritas, rutas y huellas). Nunca ejecuta dos LibreOffice a la vez; un recálculo que no produce el libro se registra
como fallo del caso (no se reintenta en bucle).
"""
import hashlib
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
sys.path.insert(0, AQUI)
sys.path.insert(0, os.path.join(RAIZ, "v6", "v64_experimental", "scripts"))
import casos_v64 as K  # noqa: E402
from trasladar_entradas import trasladar  # noqa: E402

PLANTILLA = os.path.join(RAIZ, "v6", "v64_experimental", "entregables", "Plantilla_V6.4_experimental.xlsx")
RECALC = os.path.join(RAIZ, "personaje_v2", "scripts", "recalc.sh")


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def generar(dir_salida, solo=None, plantilla=PLANTILLA):
    os.makedirs(os.path.join(dir_salida, "rc"), exist_ok=True)
    perfil = os.path.join(dir_salida, "perfil_lo")
    casos = K.CASOS + K.casos_rechazo()
    if solo:
        casos = [c for c in casos if c["id"] in solo]
    man = {"plantilla": os.path.relpath(plantilla, RAIZ), "plantilla_sha256": sha(plantilla), "casos": []}
    for c in casos:
        t0 = time.time()
        src = os.path.join(RAIZ, K.BASES[c["base"]])
        out = os.path.join(dir_salida, c["id"] + ".xlsx")
        trasladar(src, plantilla, out, c["config"] or None, False, c["entradas"] or None)
        r = subprocess.run(["bash", RECALC, out, os.path.join(dir_salida, "rc"), perfil], capture_output=True, text=True, timeout=300)
        rc = os.path.join(dir_salida, "rc", c["id"] + ".xlsx")
        ok = r.returncode == 0 and os.path.exists(rc)
        man["casos"].append({**c, "libro": os.path.relpath(out, dir_salida), "recalculado": os.path.relpath(rc, dir_salida) if ok else None,
                             "base_sha256": sha(src), "recalculo_ok": ok, "segundos": round(time.time() - t0, 1)})
        print(f"{c['id']:40s} {'ok' if ok else 'FALLO DEL RECÁLCULO'} {time.time() - t0:.1f} s", flush=True)
    json.dump(man, open(os.path.join(dir_salida, "manifiesto_casos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return man


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    solo = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
    pl = sys.argv[sys.argv.index("--plantilla") + 1] if "--plantilla" in sys.argv else PLANTILLA
    m = generar(os.path.abspath(sys.argv[1]), solo, pl)
    sys.exit(0 if all(c["recalculo_ok"] for c in m["casos"]) else 1)
