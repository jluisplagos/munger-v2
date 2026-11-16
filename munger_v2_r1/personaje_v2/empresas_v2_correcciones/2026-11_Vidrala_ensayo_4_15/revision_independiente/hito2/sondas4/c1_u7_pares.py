#!/usr/bin/env python3
"""c1 · T1 (cuarta comprobación): la exención del tipo de cambio de U7 tras la corrección (la unidad ENTERA es un par de monedas, sin
palabra de escala). A) unidad a unidad, candidata anterior (f3d15e8) → cuarta (7a6583b): pares de monedas DISTINTAS (tipos de cambio),
pares de la MISMA moneda (cabeceras bilingües de un importe: «euros/EUR», «EUR/€»), pares con calificativo y unidades con escala.
B) en el registro completo (fixture de la batería, como r7b): la fuente publica 849,697 en la unidad declarada y el registro lo lleva al
modelo (849,697 millones) con escala 1; con «euros» eso es un error de escala de un millón.
Uso: python3 -I -B c1_u7_pares.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
from comun3 import VE, VP, ACT, ANT  # noqa: E402

print(f"VE = {ACT} · VP = {ANT}")
print("== A · ¿unidad monetaria no reconocida (pendiente por U7)?   anterior → cuarta")
GRUPOS = [
    ("pares de monedas DISTINTAS (tipos de cambio: no deben quedar pendientes)",
     ["USD por EUR", "EUR/USD", "eur / usd", "tipo de cambio EUR/GBP", "tipo de cambio: EUR/USD", "exchange rate USD per EUR", "(EUR/USD)", "$/€", "€/$", "dólar por euro",
      "euros por dólar", "GBP per EUR", "coronas/euros", "libras por euro"]),
    ("pares de la MISMA moneda (cabecera bilingüe de un importe en unidades: es un importe, se espera PENDIENTE o reconocida)",
     ["euros/EUR", "EUR/€", "€/EUR", "Euros / Euro", "euro/euros", "EUR/EUR", "USD/$", "$/USD", "libras/GBP", "GBP/£", "eur por eur", "(€/EUR)", "tipo de cambio EUR/EUR"]),
    ("tipos de cambio con calificativo (quedan pendientes: conservador)",
     ["tipo de cambio medio USD por EUR", "USD por EUR (cierre)", "EUR/USD medio", "dólares por euro", "USD por 1 EUR", "tipo de cambio EUR/USD a 31-12"]),
    ("importes (deben quedar pendientes)",
     ["miles de euros a tipo de cambio constante", "millones de euros/EUR million", "Miles de € / € thousand", "k€/usd", "meur/keur", "mm€/usd", "EUR m / USD m",
      "milliers d'euros / EUR", "Tsd. EUR/USD", "EUR'000/USD'000", "saldo en USD por EUR", "importe en euros/dólares", "euros/usd miles"]),
    ("controles: unidades reconocidas o por acción (no pendientes)", ["euros", "eur", "miles de euros", "millones de euros", "EUR por acción", "euros/acción", "€ per share"]),
]
senalados = []
for titulo, unidades in GRUPOS:
    print(f"   -- {titulo}")
    for u in unidades:
        a, b = VP._unidad_monetaria_no_reconocida(u), VE._unidad_monetaria_no_reconocida(u)
        rec = VE.UNIDADES.get(VE._norm_txt(u))
        est = lambda x: "PENDIENTE" if x else ("reconocida" if rec is not None else "no monetaria")  # noqa: E731
        marca = ""
        if titulo.startswith("pares de la MISMA") and not b and rec is None:
            marca = "   <<< un importe en unidades de la moneda queda como «no monetaria» (cualquier potencia de diez vale como escala)"
            senalados.append(u)
        if titulo.startswith("importes") and not b:
            marca = "   <<< IMPORTE no pendiente"
            senalados.append(u)
        print(f"      {u!r:46} {est(a):12} → {est(b):12}{marca}")
print(f"   señalados: {len(senalados)} · {senalados}")

import fx5 as X  # noqa: E402
K = X.K
print("\n== B · registro completo (fixture de la batería); código:", ACT if X.VE.__file__ == VE.__file__ else X.VE.__file__)
print("   control positivo:", X.resumen(X.con())[:80])
vm = X.ent(X.REG, K)["valor_modelo"]
print(f"   {K}: valor del modelo {vm} (millones). La página nueva dice «Partida sintética de {K}: {vm:.3f}» y se declara escala 1 con cada unidad:")
n = X.nueva_pagina(f"Partida sintética de {K}: {vm:.3f}")
for unidad in ("euros", "eur", "euros/EUR", "EUR/€", "€/EUR", "Euros / Euro", "USD/$", "USD por EUR", "miles de euros", "miles de euros a tipo de cambio constante"):
    r = X.con(lambda g, u=unidad: X.ent(g, K)["fuente"].update(unidad=u, escala=1.0, valor_fuente=vm, cita=f"Partida sintética de {K}: {vm:.3f}", pagina=n), resellar=True)
    print(f"      unidad {unidad!r:44} escala 1 → " + ("COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:170]))
print("   control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
