#!/usr/bin/env python3
"""Resumen de mut4/*/resultado.json (tabla en Markdown).  Uso: python3 -I -B mutaciones5_resumen.py [--md]"""
import glob, json, os, re, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import importlib.util
spec = importlib.util.spec_from_file_location("mutaciones5", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutaciones5.py"))
M5 = importlib.util.module_from_spec(spec); spec.loader.exec_module(M5)
NOMBRE_B = {"test_verificacion_entradas_415.py": "entradas 4.15", "test_entrada_efectiva_415.py": "entrada efectiva", "test_verificacion_entradas_414.py": "entradas 4.14"}
filas, falta = [], []
for nombre, (grupo, hall, desc, _c, bats) in M5.M.items():
    p = os.path.join(F, "mut5", nombre, "resultado.json")
    if not os.path.exists(p):
        falta.append(nombre)
        continue
    r = json.load(open(p, encoding="utf-8"))
    det, partes = False, []
    for b, x in r.get("baterias", {}).items():
        m = re.match(r"(\d+)/(\d+)", x.get("pasan") or "")
        if x.get("fallan") or x.get("codigo") not in (0,) or not m or m.group(1) != m.group(2):
            det = True
        if x.get("fallan"):
            partes.append(f"{NOMBRE_B[b]}: {x.get('pasan', '').split(' ')[0] if x.get('pasan') else '—'}, fallan {len(x['fallan'])} («{re.sub(r'^.[A-Za-z0-9]+. FALLA +', '', x['fallan'][0])[:95]}…»)")
        elif x.get("codigo") != 0 or not m:
            partes.append(f"{NOMBRE_B[b]}: abortada (código {x.get('codigo')}; {(x.get('traza') or ['sin traza'])[-1][:90]})")
        else:
            partes.append(f"{NOMBRE_B[b]}: {m.group(0)}")
    res = "pasa entera" if nombre == "c00_control" and not det else ("detectada" if det else "**NO detectada**")
    filas.append((nombre, grupo, hall, desc, res, "; ".join(partes), sum(x.get("segundos", 0) for x in r.get("baterias", {}).values())))
if "--md" in sys.argv:
    print("| Mutación | Hallazgo | Qué se quita o altera | Resultado | Baterías |\n|---|---|---|---|---|")
    for n, g, h, d, res, part, seg in filas:
        print(f"| `{n}` | {h} | {d.replace('|', '/').replace('<', '&lt;')} | {res} | {part.replace('|', '/').replace('<', '&lt;')} |")
else:
    for n, g, h, d, res, part, seg in filas:
        print(f"{n:38} {g:7} {h:6} {res:18} {seg:5}s  {part[:170]}")
tn = [f for f in filas if f[1] != "control"]
print(f"\n{len(filas)} con resultado ({sum(1 for f in tn if f[4] == 'detectada')} detectadas, {sum(1 for f in tn if 'NO' in f[4])} no detectadas, sin contar el control) · sin resultado todavía: {len(falta)} {falta if len(falta) < 60 else ''}")
