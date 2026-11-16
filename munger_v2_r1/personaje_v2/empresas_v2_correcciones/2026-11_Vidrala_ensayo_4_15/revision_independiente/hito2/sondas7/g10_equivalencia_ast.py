#!/usr/bin/env python3
"""g10 · séptima comprobación · equivalencia de programas por árbol sintáctico (los comentarios no cuentan; las cadenas, los docstrings y las
expresiones regulares, sí): ¿es `verificacion_entradas.py` de la candidata con el carácter repuesto (fix7) EL MISMO PROGRAMA que el que la
sexta comprobación propuso y probó (prop6 = 8196522 + sus propuestas W3–W5)? ¿Y la candidata tal cual?
Uso: python3 -I -B g10_equivalencia_ast.py"""
import ast, hashlib, os
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = "munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py"


def cargar(nombre):
    s = open(os.path.join(F, nombre, R), encoding="utf-8").read()
    return s, ast.dump(ast.parse(s), include_attributes=False)


src = {n: cargar(n) for n in ("prev", "copia", "prop6", "fix7")}
rot = {"prev": "8196522", "copia": "45ff57c (candidata)", "prop6": "8196522 + propuestas de la 6.ª", "fix7": "45ff57c + el carácter de :542"}
for n, (s, d) in src.items():
    print(f"   {rot[n]:34} SHA-256 del archivo {hashlib.sha256(s.encode('utf-8')).hexdigest()[:8]}… · del árbol sintáctico {hashlib.sha256(d.encode('utf-8')).hexdigest()[:16]}")
for a, b in (("fix7", "prop6"), ("copia", "prop6"), ("copia", "prev"), ("fix7", "copia")):
    print(f"   árbol sintáctico de «{rot[a]}» {'==' if src[a][1] == src[b][1] else '!='} «{rot[b]}»")
# dónde difieren los árboles de la candidata y de la propuesta: nodos constantes distintos
ta, tb = ast.parse(src["copia"][0]), ast.parse(src["prop6"][0])
dif = [(x.lineno, x.value, y.value) for x, y in zip(ast.walk(ta), ast.walk(tb)) if isinstance(x, ast.Constant) and isinstance(y, ast.Constant) and x.value != y.value]
print(f"   constantes distintas entre la candidata y la propuesta de la 6.ª: {len(dif)}")
for l, x, y in dif:
    print(f"      línea {l}: candidata {x!r} · propuesta {y!r}")
