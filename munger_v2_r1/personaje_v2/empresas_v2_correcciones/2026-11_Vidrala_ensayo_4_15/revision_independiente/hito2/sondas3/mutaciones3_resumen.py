#!/usr/bin/env python3
"""Resumen de las mutaciones de la tercera pasada (lee mut3/<nombre>/resultado.json). Uso: python3 -I -B mutaciones3_resumen.py [--md]"""
import json, os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutaciones3 as M3
md = "--md" in sys.argv
cuenta = {}
filas = []
CORTO = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}
for nombre, (grupo, hall, desc, _c, bats) in M3.M.items():
    p = os.path.join(F, "mut3", nombre, "resultado.json")
    if not os.path.exists(p):
        filas.append((grupo, nombre, hall, desc, "(sin ejecutar)", ""))
        cuenta.setdefault(grupo, [0, 0, 0])[2] += 1
        continue
    r = json.load(open(p, encoding="utf-8"))
    if "error" in r:
        filas.append((grupo, nombre, hall, desc, "ERROR", r["error"]))
        continue
    partes, det = [], False
    for b, v in r["baterias"].items():
        if v["codigo"] != 0:
            det = True
            if v["pasan"]:
                a, t = v["pasan"].split(" ")[0].split("/")
                partes.append(f"{CORTO[b]}: {a}/{t}, fallan {len(v['fallan'])}" + (f" («{v['fallan'][0][v['fallan'][0].index('FALLA') + 6:][:80].strip()}…»)" if v["fallan"] else ""))
            else:
                partes.append(f"{CORTO[b]}: abortada ({(v['traza'] or ['?'])[-1][:70]})")
        else:
            partes.append(f"{CORTO[b]}: {v['pasan'].split(' ')[0]}")
    if grupo == "control":
        estado = "pasa entera" if not det else "FALLA"
    else:
        estado = "detectada" if det else "**NO detectada**"
        cuenta.setdefault(grupo, [0, 0, 0])[0 if det else 1] += 1
    filas.append((grupo, nombre, hall, desc, estado, "; ".join(partes)))
for grupo, nombre, hall, desc, estado, det in filas:
    print(f"| `{nombre}` | {hall} | {desc.replace('|', '/')} | {estado} | {det.replace('|', '/')} |" if md else f"{grupo:10} {nombre:36} {hall:8} {estado:18} {det}")
print()
for g, (d, n, p) in cuenta.items():
    print(f"{g}: {d} detectadas · {n} no detectadas · {p} sin ejecutar")
