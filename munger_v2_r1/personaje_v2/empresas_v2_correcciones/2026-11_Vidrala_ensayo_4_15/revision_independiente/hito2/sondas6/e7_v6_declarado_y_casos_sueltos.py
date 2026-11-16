#!/usr/bin/env python3
"""e7 · sexta comprobación · V6 (declaración) y casos sueltos.
A) lo que el docstring de _signo_en_cita declara AHORA en su línea «+1» (V6): cada ejemplo, contra el código;
B) incoherencia entre los límites de la CITA (_apariciones_en_pagina, sin apóstrofo) y los de la CIFRA (_lectura_cifra, con apóstrofo):
   la cifra citada sola que aparece además dentro de un número con apóstrofo;
C) el mensaje del máximo de apariciones (recuento cortado);
D) «real» en el registro completo (fixture de la batería): una entrada con la unidad «% real» (y otras), con los dos códigos (PV).
Uso: python3 -I -B e7_v6_declarado_y_casos_sueltos.py   (PV=<prev>/personaje_v2 para la parte D con la candidata anterior)"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
SOLO_D = os.environ.get("PV") is not None
if not SOLO_D:
    from comun6 import VE, VP, ACT, ANT  # noqa: E402
    print(f"VE = {ACT} · VP = {ANT}")
    print("\n== A · la línea «+1» del docstring (V6): «un guion pegado al año anterior de un intervalo de años crecientes y plausibles o a una fecha no es un signo;")
    print("       cualquier otro guion pegado entre cifras deja el signo indeterminado («2023-849», «2024-2023», «2-3 %», «100-150», el día de una fecha ISO, «31-12-24»)»")
    doc = VE._signo_en_cita.__doc__
    print("   el docstring menciona V6:", "(V6)" in doc, "· menciona «2024-2023»:", "2024-2023" in doc, "· «31-12-24»:", "31-12-24" in doc, "· la frase antigua «un guion pegado a otra cifra es un intervalo o una fecha»:",
          "un guion pegado a otra cifra es un intervalo o una fecha" in doc)
    for nombre, pag, vf, declarado in (("«2019-2020», el 2020", "Periodo 2019-2020", 2020, "ok"), ("«FY2023-2024», el 2024", "FY2023-2024", 2024, "ok"), ("«31-12-2024», el 2024", "Cierre 31-12-2024", 2024, "ok"),
                                       ("«2023-849», el 849", "Saldo 2023-849", 849, "pendiente"), ("«2024-2023», el 2023", "Variación 2024-2023", 2023, "pendiente"),
                                       ("«2-3 %», el 3", "Rango 2-3 %", 3, "pendiente"), ("«100-150», el 150", "Entre 100-150 millones", 150, "pendiente"),
                                       ("fecha ISO «2024-12-31», el día 31", "Cierre 2024-12-31", 31, "pendiente"), ("fecha ISO «2024-12-31», el mes 12", "Cierre 2024-12-31", 12, "pendiente"),
                                       ("«31-12-24», el 24", "Cierre 31-12-24", 24, "pendiente")):
        r = VE._cita_cifra(pag, vf, pag + "\n")
        hace = {"ok": "ok", "signo_indeterminado": "pendiente", "no_localizada": "pendiente"}.get(r[0], "discrepancia")
        print(f"   {nombre:38} declarado: {declarado:10} hace: {r[0]:20} {'conforme' if hace == declarado else '<<< NO conforme'}")
    print("   -- no declarados en el docstring (los anotó la quinta comprobación; sin cambio): ")
    for nombre, pag, vf in (("«Notas 5-6-1849» con +1849 (la regla de la fecha solo mira la forma)", "Notas 5-6-1849", 1849), ("«Saldo 2023-2049» con +2049 (importe que parece un año)", "Saldo 2023-2049", 2049),
                            ("«Notas 5-6-849,7» con +849,7 (mutación t8d)", "Notas 5-6-849,7", 849.7)):
        print(f"   {nombre:72} 876bfc2: {VP._cita_cifra(pag, vf, pag + chr(10))[0]:20} 8196522: {VE._cita_cifra(pag, vf, pag + chr(10))[0]}")

    print("\n== B · límites de la cita (sin apóstrofo) frente a límites de la cifra (con apóstrofo)")
    for nombre, pag, cita, vf in (("la cifra sola, que está además dentro de «1'849,7»", "Total 1'849,7\nOtros 849,7\n", "849,7", 849.7),
                                  ("lo mismo con la cita distintiva", "Total 1'849,7\nOtros 849,7\n", "Otros 849,7", 849.7),
                                  ("«Total 849» que está además en «Total 849'697»", "Total 849'697\nTotal 849\n", "Total 849", 849),
                                  ("la cifra sola en negativo de verdad y dentro de «1'849,7» (valor +849,7)", "Total 1'849,7\nOtros -849,7\n", "849,7", 849.7),
                                  ("la cifra sola en positivo dos veces y dentro de «9'774» (valor −9): antes discrepancia", "9'774\n 9 320\n", "9", -9),
                                  ("cita cortada por delante dentro de una palabra y por detrás ante «'697»", "Total 849'697\n", "otal 849", 849)):
        a, b = VP._cita_cifra(cita, vf, pag), VE._cita_cifra(cita, vf, pag)
        print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf} · 876bfc2: {a[0]:20} 8196522: {b[0]:20} ({b[1][:95]})")
    print("   apariciones de la cita «849,7» en «Total 1'849,7» según _apariciones_en_pagina:", len(VE._apariciones_en_pagina("849,7", "Total 1'849,7")),
          "· y «Total 849» en «Total 849'697»:", len(VE._apariciones_en_pagina("Total 849", "Total 849'697")))

    print("\n== C · mensaje del máximo de apariciones")
    for N in (201, 202, 400, 100000):
        print(f"   la cita aparece {N} veces: 876bfc2 dice «{VP._cita_cifra('Total: 5.5', 5.5, ' '.join(['Total: 5.5'] * N))[1][:32]}…» · 8196522 dice «{VE._cita_cifra('Total: 5.5', 5.5, ' '.join(['Total: 5.5'] * N))[1][:32]}…»")

print("\n== D · «real» en el registro completo (fixture de la batería)")
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
VEX = X.VE
K = X.K
print("   código:", "sexta (8196522)" if "(hito 2, V2)" in open(VEX.__file__, encoding="utf-8").read() else "anterior (876bfc2, 5.ª comprobación)")
print("   control positivo:", X.resumen(X.con())[:80])
vm = X.ent(X.REG, K)["valor_modelo"]
n = X.nueva_pagina(f"Partida sintética de {K}: {vm:.3f}")
print(f"   {K}: valor del modelo {vm}; la página nueva dice «Partida sintética de {K}: {vm:.3f}»; escala 1 con cada unidad (ninguna es un importe en reales):")
for unidad in ("%", "% real", "tipo real", "crecimiento real (%)", "valor real", "real estate", "tipo de cambio real", "% en términos reales", "veces", "real por euro", "EUR/real", "miles de reales", "reales/BRL"):
    r = X.con(lambda g, u=unidad: X.ent(g, K)["fuente"].update(unidad=u, escala=1.0, valor_fuente=vm, cita=f"Partida sintética de {K}: {vm:.3f}", pagina=n), resellar=True)
    print(f"      unidad {unidad!r:24} → " + ("COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:120]) + f" · apto={r['apto_por_entradas']}")
print("   control positivo al final:", X.resumen(X.con())[:80])
X.limpiar()
