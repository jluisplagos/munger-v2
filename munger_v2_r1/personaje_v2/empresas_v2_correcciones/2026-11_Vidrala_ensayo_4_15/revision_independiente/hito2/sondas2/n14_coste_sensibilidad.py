#!/usr/bin/env python3
"""n14 · U3/H6 (segunda pasada): coste de _sensibilidad con los puntos nuevos (6 genéricos + 2 extremos por origen, dos sentidos) en fórmulas
dentro de los límites (2000 caracteres, 400 nodos). Estable frente a candidata.  Uso: python3 -I -B n14_coste_sensibilidad.py"""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dos_codigos import VE, VC


def medir(nombre, formula, vals):
    ks = sorted(VE._claves_formula(formula))
    fila = f"   {nombre:72} {len(formula):5} car. {len(ks):3} orígenes"
    for et, mod in (("candidata", VC), ("estable", VE)):
        try:
            mod._validar_formula(formula)
            t0 = time.time()
            ine, loc = mod._sensibilidad(formula, vals, ks)
            fila += f" · {et}: {time.time() - t0:6.2f} s (inertes {len(ine)})"
        except Exception as ex:  # noqa: BLE001
            fila += f" · {et}: {type(ex).__name__} {str(ex)[:40]}"
    print(fila)


for n in (10, 40, 70):
    ks = [f"a{i}" for i in range(n)]
    vals = {k: 100.0 + i for i, k in enumerate(ks)}
    medir(f"suma de {n} orígenes (todos influyen)", "sum([" + ", ".join(f'o["{k}"]' for k in ks) + "])", vals)
    medir(f"max de {n} orígenes (solo influye el mayor en cada punto)", "max(" + ", ".join(f'o["{k}"]' for k in ks) + ")", vals)
for n in (10, 20, 30):
    ks = [f"a{i}" for i in range(n)]
    vals = dict({k: 100.0 + i for i, k in enumerate(ks)}, b=5.0)
    medir(f"b + Σ (a_i − a_i), {n} orígenes inertes (caso peor: ninguno se da por vivo)", 'o["b"] + ' + " + ".join(f'(o["{k}"] - o["{k}"])' for k in ks), vals)
