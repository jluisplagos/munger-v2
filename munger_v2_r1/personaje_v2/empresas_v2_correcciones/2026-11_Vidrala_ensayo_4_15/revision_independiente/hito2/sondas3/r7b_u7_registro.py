#!/usr/bin/env python3
"""r7b · N9/U7 (tercera pasada): la parte B de r7 (registro completo), ejecutable con los dos códigos (PV=<prev>/personaje_v2 para la
candidata anterior). La fuente publica 849,697 «en miles» y el registro lo lleva al modelo (849,697 millones) con escala 1: mil veces de más.
Uso: python3 -I -B r7b_u7_registro.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE, K = X.VE, X.K
print("código:", "tercera (f3d15e8)" if "textos_fuente" in open(VE.__file__, encoding="utf-8").read() else "anterior (92b2362, 2.ª pasada)")
print("control positivo:", X.resumen(X.con())[:70])
vm = X.ent(X.REG, K)["valor_modelo"]
n = X.nueva_pagina(f"Partida sintética de {K}: {vm:.3f}")
for unidad in ("miles de euros", "miles de €", "miles de euros a tipo de cambio constante", "EUR thousand at constant exchange rates", "miles de euros / thousand euros", "millones de euros/EUR million",
               "Miles de € / € thousand", "USD por EUR"):
    r = X.con(lambda g, u=unidad: X.ent(g, K)["fuente"].update(unidad=u, escala=1.0, valor_fuente=vm, cita=f"Partida sintética de {K}: {vm:.3f}", pagina=n), resellar=True)
    print(f"   unidad {unidad!r:48} escala 1 → " + ("COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:150]))
print("control positivo al final:", X.resumen(X.con())[:70])
X.limpiar()
