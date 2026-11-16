#!/usr/bin/env python3
"""r7 · N9/U7 (tercera pasada): la exención nueva del «tipo de cambio» en _unidad_monetaria_no_reconocida. La regla U7 deja PENDIENTE una
unidad que nombra una moneda y no está en el vocabulario (su escala no puede contrastarse). La exención nueva la quita si la unidad contiene
«tipo de cambio», «exchange rate» o «(por|per|/) + moneda». ¿Qué IMPORTES (no tipos de cambio) escapan ahora de U7?
A) unidad a unidad (candidata anterior → tercera);  B) en el registro completo: un importe en miles con la unidad «miles de euros a tipo de
cambio constante» y escala 1 (mal: debería ser 0,001), frente a la misma entrada con «miles de euros» (error de escala) y «miles de €» (pendiente).
Uso: python3 -I -B r7_u7_tipo_de_cambio.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, ACT, ANT
print(f"VE = {ACT} · VP = {ANT}")
print("== A · ¿unidad monetaria no reconocida (pendiente por U7)?   anterior → tercera")
UN = [("tipos de cambio (lo que N9 quería eximir)", ["USD por EUR", "EUR/USD", "tipo de cambio EUR/USD", "tipo de cambio medio USD por EUR", "exchange rate EUR/USD", "GBP per EUR"]),
      ("IMPORTES con una mención del tipo de cambio", ["millones de euros a tipo de cambio constante", "miles de euros (a tipo de cambio constante)", "millones de euros al tipo de cambio de cierre",
                                                      "EUR million at constant exchange rates", "miles de USD convertidos al tipo de cambio medio", "M€ a tipos de cambio constantes",
                                                      "millones de dólares (tipo de cambio de cierre)"]),
      ("IMPORTES con barra o «por» seguidos de moneda", ["miles de euros / thousand euros", "millones de euros/EUR million", "Miles de € / € thousand", "MM€/M€", "millones de pesos por euros",
                                                          "USD (millones) / EUR (millones)", "importe en USD por contravalor en euros", "miles de coronas/euros"]),
      ("otros importes no reconocidos (siguen pendientes)", ["miles de €", "MM€", "EUR millones", "millones de DKK", "millones de euros (reexpresado)"])]
for titulo, us in UN:
    print(f"   -- {titulo}")
    for u in us:
        a, b = VP._unidad_monetaria_no_reconocida(u), VE._unidad_monetaria_no_reconocida(u)
        marca = "   <<< un importe deja de quedar pendiente: su escala ya no se contrasta" if (a and not b and "IMPORTES" in titulo) else ""
        print(f"      {u!r:56} {'PENDIENTE' if a else 'no monetaria'} → {'PENDIENTE' if b else 'no monetaria'}{marca}")

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
K = X.K
print("\n== B · registro completo (fixture de la batería); código:", "tercera (f3d15e8)" if X.VE.__file__ == VE.__file__ else X.VE.__file__)
print("   control positivo:", X.resumen(X.con())[:70])
e0 = X.ent(X.REG, K)
vf, vm = e0["fuente"]["valor_fuente"], e0["valor_modelo"]
print(f"   la entrada {K}: valor_fuente {vf!r} en «{e0['fuente']['unidad']}», escala {e0['fuente']['escala']!r}, valor del modelo {vm!r} (millones)")
print("   En cada caso se declara escala 1 con el valor_fuente igual al del modelo en miles… es decir, una fuente que publica MILES leída como si fueran millones:")
for unidad in ("miles de euros", "miles de €", "miles de euros a tipo de cambio constante", "EUR thousand at constant exchange rates", "miles de euros / thousand euros", "millones de euros/EUR million"):
    def cambio(g, unidad=unidad):
        e = X.ent(g, K)
        # la fuente publica vm (p. ej. 849,697) «en miles»; el registro lo lleva al modelo con escala 1: mil veces más de lo debido
        e["fuente"].update(unidad=unidad, escala=1.0, valor_fuente=vm, cita=f"Partida sintética de {K}: {vm:.3f}")
    n = X.nueva_pagina(f"Partida sintética de {K}: {vm:.3f}")
    r = X.con(lambda g: (cambio(g), X.ent(g, K)["fuente"].update(pagina=n)), resellar=True)
    print(f"      unidad {unidad!r:48} → " + ("COMPROBADA (escala 1 con una unidad en miles: no se contrasta)" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:170]))
print("   control positivo al final:", X.resumen(X.con())[:70])
X.limpiar()
