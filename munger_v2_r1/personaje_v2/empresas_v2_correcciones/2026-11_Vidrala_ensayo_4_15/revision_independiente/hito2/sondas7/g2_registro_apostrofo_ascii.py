#!/usr/bin/env python3
"""g2 · séptima comprobación · el hueco de g1 en el REGISTRO COMPLETO (fixture sintético de la batería, fx5): una entrada cuya fuente publica
la cifra con miles separados por apóstrofo ASCII («1'849'697,000», es decir, 1.849.697) y cuyo valor_fuente es el trozo de detrás del
primer apóstrofo (849697, el valor del modelo: un error de un millar de millares), citando la línea entera.
Con 8196522 es una discrepancia (no apto); ¿y con 45ff57c?
Uso: python3 -I -B g2_registro_apostrofo_ascii.py     (PV=<fable>/prev/munger_v2_r1/personaje_v2 para el código de 8196522;
     PV=<fable>/fix7/munger_v2_r1/personaje_v2 para la candidata con la corrección propuesta)"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X  # noqa: E402
VE, K = X.VE, X.K
src = open(VE.__file__, encoding="utf-8").read()
CORR = """(?<![\\d.,])(?<!\\d['’])" + re.escape(c)"""
print("código:", "45ff57c con la corrección propuesta de :542 (fix7)" if "(hito 2, W5)" in src and CORR in src else "séptima (45ff57c)" if "(hito 2, W5)" in src else "8196522 con las propuestas de la 6.ª (prop6)" if CORR in src else "anterior (8196522)" if "(hito 2, V2)" in src else "¿?")
print("control positivo:", X.resumen(X.con())[:90])
vm = X.ent(X.REG, K)["valor_modelo"]
vf = X.ent(X.REG, K)["fuente"]["valor_fuente"]
print(f"{K}: valor del modelo {vm}; valor_fuente {vf} ({X.ent(X.REG, K)['fuente']['unidad']}, escala {X.ent(X.REG, K)['fuente']['escala']})")
ent, dec = f"{vf:.3f}".split(".")
miles = f"{int(ent):,}".replace(",", "'")  # 849'697


def probar(nombre, linea, cita=None, valor=None, esperado_apto=False):
    n = X.nueva_pagina(linea)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(cita=cita or linea, pagina=n, **({"valor_fuente": valor} if valor is not None else {})), resellar=True)
    est = "COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:150]
    marca = "" if r["apto_por_entradas"] == esperado_apto else "   <<< el revisor esperaba apto=" + str(esperado_apto)
    print(f"   {nombre}\n      página: {linea!r} · cita: {(cita or linea)!r}\n      → {est} · apto_por_entradas={r['apto_por_entradas']}{marca}")
    return r


print("\n== la fuente publica un número MAYOR con miles separados por apóstrofo ASCII; el registro declara el trozo de detrás")
probar("G1 «1'" + miles + "," + dec + "» (1 millón más) citando la línea entera", f"Partida sintética de {K}: 1'{miles},{dec}")
probar("G2 lo mismo sin decimales «1'" + miles + "»", f"Partida sintética de {K}: 1'{miles}")
probar("G3 «23'" + miles + "» (23 millones más)", f"Partida sintética de {K}: 23'{miles}")
probar("G4 la cita es solo el número «1'" + miles + "»", f"Partida sintética de {K}: 1'{miles}", cita=f"1'{miles}")
probar("G5 con punto decimal «1'" + miles + "." + dec + "»", f"Partida sintética de {K}: 1'{miles}.{dec}")
print("\n== lo mismo con el apóstrofo tipográfico (W3: corregido)")
probar("G6 «1’" + miles.replace("'", "’") + "»", f"Partida sintética de {K}: 1’{miles.replace(chr(39), '’')}")
print("\n== la cita cortada (lo que fija la batería)")
probar("G7 cita «" + miles + "» en «1'" + miles + "»", f"Partida sintética de {K}: 1'{miles}", cita=miles)
print("\n== controles positivos: la cifra del registro, entera, con apóstrofo")
probar("G8 «" + miles + "» (la cifra entera con apóstrofo de miles)", f"Partida sintética de {K}: {miles}", esperado_apto=True)
probar("G9 «" + miles + "." + dec + "»", f"Partida sintética de {K}: {miles}.{dec}", esperado_apto=True)
print("\n== valor con decimales y unidad no monetaria (escala 1): la fuente publica «1<apóstrofo>" + f"{vm:.3f}" + "» y el registro declara " + f"{vm:.3f}")


def probar_u(nombre, linea, esperado_apto=False):
    n = X.nueva_pagina(linea)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(unidad="veces", escala=1.0, valor_fuente=vm, cita=linea, pagina=n), resellar=True)
    est = "COMPROBADA" if K in r["comprobadas"] else "no comprobada · " + "; ".join(X.con_k(r, K))[:150]
    marca = "" if r["apto_por_entradas"] == esperado_apto else "   <<< el revisor esperaba apto=" + str(esperado_apto)
    print(f"   {nombre}\n      página y cita: {linea!r}\n      → {est} · apto_por_entradas={r['apto_por_entradas']}{marca}")


probar_u("G10 apóstrofo ASCII «1'" + f"{vm:.3f}" + "» (X1)", f"Partida sintética de {K}: 1'{vm:.3f}")
probar_u("G11 apóstrofo tipográfico «1’" + f"{vm:.3f}" + "» (W3)", f"Partida sintética de {K}: 1’{vm:.3f}")
probar_u("G12 control: la cifra del registro «" + f"{vm:.3f}" + "»", f"Partida sintética de {K}: {vm:.3f}", esperado_apto=True)
print("\ncontrol positivo al final:", X.resumen(X.con())[:90])
X.limpiar()
