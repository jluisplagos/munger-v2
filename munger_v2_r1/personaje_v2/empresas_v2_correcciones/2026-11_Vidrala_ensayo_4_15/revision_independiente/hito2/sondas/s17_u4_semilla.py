#!/usr/bin/env python3
"""s17 · U4: la parte «estructural» de _sensibilidad usa 3 puntos pseudoaleatorios con una semilla que depende del TEXTO de la fórmula.
¿Con qué frecuencia una derivación legítima con un argumento localmente inactivo (el menor de un max, el mayor de un min, un suelo) se
declara «inerte» según cómo se escriba (nombres de los orígenes, espacios)? Se prueban 2000 escrituras equivalentes de cada fórmula."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE

casos = {
    "max(a, b), b es el menor": ('max(o["{a}"], o["{b}"])', {"a": 849.697, "b": 100.25}),
    "min(a, b), b es el mayor": ('min(o["{a}"], o["{b}"])', {"a": 100.25, "b": 849.697}),
    "max(a − b, c − d), el segundo es el menor": ('max(o["{a}"] - o["{b}"], o["{c}"] - o["{d}"])', {"a": 900.0, "b": 50.0, "c": 300.0, "d": 100.0}),
    "max(a, b, c), a es el mayor": ('max(o["{a}"], o["{b}"], o["{c}"])', {"a": 900.0, "b": 50.0, "c": 300.0}),
    "min(max(a, b), c): tope c inactivo": ('min(max(o["{a}"], o["{b}"]), o["{c}"])', {"a": 10.0, "b": 5.0, "c": 300.0}),
    "a × z con z = 0 (control)": ('o["{a}"] * o["{z}"]', {"a": 0.25, "z": 0.0}),
    "0 / d (control)": ('o["{a}"] / o["{d}"]', {"a": 0.0, "d": 190.537}),
}
N = 2000
for nombre, (plantilla, vals) in casos.items():
    inertes = 0
    ejemplo = None
    for i in range(N):
        nombres = {k: f"aux:{k}{i}" for k in vals}
        f = plantilla.format(**nombres)
        v = {nombres[k]: x for k, x in vals.items()}
        ine, loc = VE._sensibilidad(f, v, list(v))
        if ine:
            inertes += 1
            ejemplo = ejemplo or (f, ine)
    print(f"   {nombre:45} declarada con orígenes inertes en {inertes} de {N} escrituras ({100 * inertes / N:.1f} %)" + (f" · p. ej. {ejemplo[0]} → inertes {ejemplo[1]}" if ejemplo else ""))
# la misma fórmula con espacios distintos
f1, f2 = 'max(o["aux:p1"], o["aux:p2"])', 'max(o["aux:p1"],  o["aux:p2"])'
v = {"aux:p1": 849.697, "aux:p2": 100.25}
import itertools
res = {}
for n_esp in range(1, 40):
    f = 'max(o["aux:p1"],' + " " * n_esp + 'o["aux:p2"])'
    res[n_esp] = bool(VE._sensibilidad(f, v, list(v))[0])
print("   max(o[\"aux:p1\"],<n espacios>o[\"aux:p2\"]) con aux:p2 el menor: «inerte» con n =", [n for n, x in res.items() if x], "de 1..39")
