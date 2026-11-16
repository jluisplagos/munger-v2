#!/usr/bin/env python3
"""d1b · Q1 (quinta comprobación), en el registro completo (fixture de la batería, como c1 B): la página publica 849.697 en la unidad
declarada y el registro lo lleva al modelo (849,697 millones) con escala 1 (un error de escala de un millón si la unidad es la moneda
en unidades). Pares de la misma moneda que la corrección cubre (EUR, USD, GBP, JPY) y los que no (francos, coronas, reales).
PV=<prev>/personaje_v2 para la candidata anterior.  Uso: python3 -I -B d1b_q1_registro_resto.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
VE = X.VE
K = X.K
print("código:", "quinta (876bfc2)" if "MAX_APARICIONES_CITA" in open(VE.__file__, encoding="utf-8").read() else "anterior (7a6583b, 4.ª comprobación)")
print("control positivo:", X.resumen(X.con())[:80])
vm = X.ent(X.REG, K)["valor_modelo"]
print(f"{K}: valor del modelo {vm} (millones). La página nueva dice «Partida sintética de {K}: {vm:.3f}» y se declara escala 1 con cada unidad:")
n = X.nueva_pagina(f"Partida sintética de {K}: {vm:.3f}")
for unidad in ("euros", "euros/EUR", "EUR/€", "USD/$", "libras/GBP", "JPY/¥", "coronas/DKK", "DKK/coronas", "corona/coronas", "francos/CHF", "CHF/francos", "franco/francos",
               "reales/BRL", "BRL/reales", "coronas/SEK", "USD por EUR", "DKK/SEK"):
    r = X.con(lambda g, u=unidad: X.ent(g, K)["fuente"].update(unidad=u, escala=1.0, valor_fuente=vm, cita=f"Partida sintética de {K}: {vm:.3f}", pagina=n), resellar=True)
    print(f"   unidad {unidad!r:22} escala 1 → " + ("COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:150]))
print("control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
