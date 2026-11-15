#!/usr/bin/env python3
"""n10 · H14 (esquema): ¿alguna ficha del árbol deja de validar con el esquema de la estable (aptitud_de_uso.apto_para_dinero_real fijado
en false, motivo_modo)? Valida todas las ficha*.json del árbol con el esquema de la estable y con el de la candidata (solo lectura).
Uso: python3 -I -B n10_esquema_fichas.py"""
import collections, json, os, subprocess, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PVS = {"estable": os.path.join(F, "copia", "munger_v2_r1", "personaje_v2"), "candidata": os.path.join(F, "cand", "munger_v2_r1", "personaje_v2")}
raiz = os.path.join(F, "copia", "munger_v2_r1")
fichas = []
for d, ds, fs in os.walk(raiz):
    ds[:] = [x for x in ds if x not in ("__pycache__", ".lo_perfil")]
    for f in fs:
        if f in ("ficha.json", "ficha_provisional.json"):
            fichas.append(os.path.join(d, f))
c = collections.Counter()
dif = []
adr = collections.Counter()
for p in sorted(fichas):
    try:
        fi = json.load(open(p, encoding="utf-8"))
    except Exception:  # noqa: BLE001
        c["ilegible"] += 1
        continue
    au = fi.get("aptitud_de_uso") if isinstance(fi, dict) else None
    adr[repr((au or {}).get("apto_para_dinero_real", "(sin clave)")) if isinstance(au, dict) else "(sin aptitud_de_uso)"] += 1
    rc = {}
    for et, pv in PVS.items():
        r = subprocess.run([sys.executable, "-I", "-B", os.path.join(pv, "scripts", "validar_esquema.py"), p, "ficha"], capture_output=True, text=True)
        rc[et] = r.returncode
    c[(rc["candidata"], rc["estable"])] += 1
    if rc["candidata"] != rc["estable"]:
        dif.append((os.path.relpath(p, raiz), rc))
print(f"fichas en el árbol: {len(fichas)}")
print("aptitud_de_uso.apto_para_dinero_real:", dict(adr))
print("(código con el esquema de la candidata, código con el de la estable): nº de fichas →", {str(k): v for k, v in c.items()})
print("fichas cuyo resultado cambia:", len(dif), dif[:5])
