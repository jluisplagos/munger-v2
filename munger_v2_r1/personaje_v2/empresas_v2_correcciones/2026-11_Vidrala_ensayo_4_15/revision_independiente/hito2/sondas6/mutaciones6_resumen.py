#!/usr/bin/env python3
"""Resumen de mut6/<nombre>/resultado.json (mutaciones de la sexta comprobación con la batería entera).  Uso: python3 -I -B mutaciones6_resumen.py [md]"""
import json, os, sys
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
import mutantes6 as MU  # noqa: E402
NOM = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}
md = sys.argv[1:] == ["md"]
codigos = set()
filas = []
for k, v in MU.M.items():
    p = os.path.join(F, "mut6", k, "resultado.json")
    if not os.path.exists(p):
        filas.append((k, v[1], v[2], "(no ejecutada con la batería entera)", ""))
        continue
    r = json.load(open(p, encoding="utf-8"))
    if "error" in r:
        filas.append((k, v[1], v[2], "ERROR: " + r["error"], ""))
        continue
    bats, detect = [], False
    for b, x in r["baterias"].items():
        codigos.add(x["codigo"])
        falla = x["codigo"] != 0 or bool(x["fallan"])
        detect = detect or falla
        bats.append(f"{NOM[b]}: {x['pasan'].replace(' pruebas', '') if x['pasan'] else 'sin recuento'}" + (f", fallan {len(x['fallan'])} («{x['fallan'][0][:90]}…»)" if x["fallan"] else "") + f" [{x['segundos']} s]")
    estado = "pasa entera" if v[0] == "control" and not detect else ("detectada" if detect else "**NO detectada**")
    filas.append((k, v[1], v[2], estado, "; ".join(bats)))
if md:
    print("| Mutación | Hallazgo | Qué se quita o altera | Resultado | Baterías |\n|---|---|---|---|---|")
    for f in filas:
        print("| `" + f[0] + "` | " + " | ".join(x.replace("|", "\\|") for x in f[1:]) + " |")
else:
    for f in filas:
        print(f"{f[0]:36} {f[1]:3} {f[3]:22} {f[4][:230]}")
print(f"\ncódigos de salida vistos: {sorted(codigos, key=str)} · ejecutadas {sum(1 for f in filas if not f[3].startswith('(no'))} de {len(filas)}")
