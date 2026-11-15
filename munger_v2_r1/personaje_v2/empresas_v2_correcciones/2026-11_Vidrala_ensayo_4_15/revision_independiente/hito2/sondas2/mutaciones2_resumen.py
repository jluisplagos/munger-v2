#!/usr/bin/env python3
"""Resumen de las mutaciones de la segunda pasada (lee mut2/<nombre>/resultado.json). Uso: python3 -I -B mutaciones2_resumen.py [--md]"""
import json, os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutaciones2 as M2
md = "--md" in sys.argv
n_det = n_no = n_pend = 0
filas = []
for nombre, (hall, desc, _c, bats) in M2.M.items():
    p = os.path.join(F, "mut2", nombre, "resultado.json")
    if not os.path.exists(p):
        n_pend += 1
        filas.append((nombre, hall, desc, "(sin ejecutar)", ""))
        continue
    r = json.load(open(p, encoding="utf-8"))
    if "error" in r:
        filas.append((nombre, hall, desc, "ERROR", r["error"]))
        continue
    partes, det = [], False
    for b, v in r["baterias"].items():
        corto = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}[b]
        if v["codigo"] != 0:
            det = True
            if v["pasan"]:
                a, t = v["pasan"].split(" ")[0].split("/")
                partes.append(f"{corto}: {a}/{t}, fallan {len(v['fallan'])}" + (f" («{v['fallan'][0][v['fallan'][0].index('FALLA') + 6:][:70].strip()}…»)" if v["fallan"] else ""))
            else:
                partes.append(f"{corto}: abortada ({(v['traza'] or ['?'])[-1][:70]})")
        else:
            partes.append(f"{corto}: {v['pasan'].split(' ')[0]}")
    if nombre.startswith(("c00", "p1_")):
        estado = "pasa entera" if not det else "FALLA"
    else:
        estado = "detectada" if det else "**NO detectada**"
        n_det += det
        n_no += not det
    filas.append((nombre, hall, desc, estado, "; ".join(partes)))
for nombre, hall, desc, estado, det in filas:
    hall = "N4 (propuesta)" if nombre.startswith("p1_") else hall  # la etiqueta del arnés se escribió antes de numerar los hallazgos
    print(f"| `{nombre}` | {hall} | {desc.replace('|', '/')} | {estado} | {det.replace('|', '/')} |" if md else f"{nombre:36} {hall:14} {estado:18} {det}")
print(f"\n{n_det} detectadas · {n_no} no detectadas · {n_pend} sin ejecutar (aparte, el control y la propuesta)")
