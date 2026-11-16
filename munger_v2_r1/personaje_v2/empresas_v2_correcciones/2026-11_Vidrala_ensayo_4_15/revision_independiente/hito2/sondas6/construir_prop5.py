#!/usr/bin/env python3
"""Reconstruye «prop5»: el código de 876bfc2 (fable/prev) con las propuestas V1, V2 y V3 del revisor de la QUINTA comprobación (los mismos
cambios de sondas5/propuestas5.py). NO es código entregado ni revisado: sirve de referencia para comparar lo que hizo el autor con lo que
se proponía. Solo escribe fable/prop5/…/scripts/verificacion_entradas.py.   Uso: python3 -I -B construir_prop5.py"""
import importlib.util, os, subprocess
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
spec = importlib.util.spec_from_file_location("p5", os.path.join(F, "sondas5", "propuestas5.py"))
src = open(os.path.join(F, "sondas5", "propuestas5.py"), encoding="utf-8").read()
ini, fin = src.index("CAMBIOS = ["), src.index("for viejo, nuevo in CAMBIOS:")
ns = {}
exec(src[ini:fin], ns)  # solo la lista CAMBIOS (texto del revisor de la quinta comprobación); no ejecuta el resto del script
PREV = os.path.join(F, "prev", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py")
dst = os.path.join(F, "prop5", "munger_v2_r1", "personaje_v2", "scripts")
os.makedirs(dst, exist_ok=True)
s = open(PREV, encoding="utf-8").read()
for viejo, nuevo in ns["CAMBIOS"]:
    assert s.count(viejo) == 1, viejo[:80]
    s = s.replace(viejo, nuevo)
open(os.path.join(dst, "verificacion_entradas.py"), "w", encoding="utf-8").write(s)
d = subprocess.run(["diff", "-u", PREV, os.path.join(dst, "verificacion_entradas.py")], capture_output=True, text=True).stdout
open(os.path.join(F, "salidas", "prop5_reconstruida.diff"), "w", encoding="utf-8").write(d)
print(f"{len(ns['CAMBIOS'])} cambios aplicados · {len(d.splitlines())} líneas de diff")
