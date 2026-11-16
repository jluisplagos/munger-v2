#!/usr/bin/env python3
"""g1 · séptima comprobación · el límite inicial de la cifra en _lectura_cifra (verificacion_entradas.py:542).
La sexta propuso «(?<!\\d['’])» (ASCII y tipográfico); la candidata lleva «(?<!\\d[’])» (solo el tipográfico): el apóstrofo ASCII, que
8196522 sí tenía («(?<!\\d')», corrección de V7), ha desaparecido de ese límite.
A) las tres expresiones, tal como están en cada código;
B) casos a nivel de unidad con 8196522, 45ff57c y la propuesta: la cifra de DETRÁS de un apóstrofo ASCII leída dentro del número, cuando la
   cita se localiza (cita completa, o que empieza antes del número);
C) qué vía resuelve los casos de la batería («849,7» en «1'849,7» y en «1’849,7»): ¿llegan a _lectura_cifra?
Uso: python3 -I -B g1_lectura_apostrofo_ascii.py"""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, V876, ACT, ANT, PROP  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · VQ = {PROP} · V876 = 876bfc2")

print("\n== A · la línea del límite de la cifra en _lectura_cifra, en cada código")
for nombre, mod in (("876bfc2", V876), ("8196522", VP), ("45ff57c", VE), ("propuesta 6.ª", VQ)):
    for n, l in enumerate(open(mod.__file__, encoding="utf-8").read().split("\n"), 1):
        if "for m in re.finditer(r\"(?<![\\d.,])" in l and "re.escape(c)" in l:
            exp = l.strip().split("  #")[0]
            print(f"   {nombre:14} :{n}  {exp}")
            m = re.search(r'\(\?<!\\d([^)]*)\)" \+ re\.escape', exp)
            print(f"   {'':14} caracteres del límite «cifra + X» por delante: {[('U+%04X' % ord(ch)) for ch in (m.group(1).strip('[]') if m else '')] or 'NINGUNO (no hay ese límite)'}")

print("\n== B · casos")
n_reab = 0


def caso(nombre, pag, cita, vf, esperado):
    global n_reab
    r = [m._cita_cifra(cita, vf, pag)[0] for m in (V876, VP, VE, VQ)]
    marca = ""
    if r[2] != esperado:
        marca = f"   <<< el revisor esperaba «{esperado}»"
        if r[2] == "ok" and r[1] != "ok":
            n_reab += 1
            marca += " · REABIERTO (8196522 no lo aceptaba)"
    print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf!r}\n      876bfc2: {r[0]:20} 8196522: {r[1]:20} 45ff57c: {r[2]:20} propuesta: {r[3]}{marca}")
    return r


caso("B1 (= e3 A2) la cita completa con el valor cortado: «Total 1'849,7» con valor 849,7", "Total 1'849,7\n", "Total 1'849,7", 849.7, "ausente")
caso("B2 la cita es solo el número: «1'849,7» con valor 849,7", "Total 1'849,7\n", "1'849,7", 849.7, "ausente")
caso("B3 (= e3 A10) «Total 1'234'567» con valor 567", "Total 1'234'567\n", "Total 1'234'567", 567, "ausente")
caso("B4 «Total 1'234'567» con valor 234567", "Total 1'234'567\n", "Total 1'234'567", 234567, "ausente")
caso("B5 (= e3 A11) «Total 1'234'567» con valor 234 (entre dos apóstrofos: lo para el límite final)", "Total 1'234'567\n", "Total 1'234'567", 234, "ausente")
caso("B6 miles con apóstrofo y punto decimal «1'849.7» con valor 849,7", "Total 1'849.7\n", "Total 1'849.7", 849.7, "ausente")
caso("B7 entero «12'345» con valor 345", "Empleados 12'345\n", "Empleados 12'345", 345, "ausente")
caso("B8 con signo delante del número: «Resultado -1'849,7» con valor +849,7", "Resultado -1'849,7\n", "Resultado -1'849,7", 849.7, "ausente")
caso("B9 lo mismo con valor −849,7", "Resultado -1'849,7\n", "Resultado -1'849,7", -849.7, "ausente")
caso("B10 entre paréntesis: «Resultado (1'849,7)» con valor +849,7", "Resultado (1'849,7)\n", "Resultado (1'849,7)", 849.7, "ausente")
caso("B11 lo mismo con valor −849,7", "Resultado (1'849,7)\n", "Resultado (1'849,7)", -849.7, "ausente")
caso("B12 con moneda: «CHF 1'849,7 millones» con valor 849,7", "Ventas CHF 1'849,7 millones\n", "Ventas CHF 1'849,7 millones", 849.7, "ausente")
caso("B13 tabla con dos columnas: «Ventas 1'849,7 1'702,3» con valor 702,3", "Ventas 1'849,7 1'702,3\n", "Ventas 1'849,7 1'702,3", 702.3, "ausente")
caso("B14 la cita empieza antes y acaba en la cifra: «de 1'849,7» en «Total de 1'849,7 millones», valor 849,7", "Total de 1'849,7 millones\n", "de 1'849,7", 849.7, "ausente")
print("   -- lo que SÍ sigue cerrado (lo fija la batería o lo para otro límite)")
caso("B15 (= e3 A1) cita cortada por delante: «849,7» en «1'849,7»", "Total 1'849,7\n", "849,7", 849.7, "ausente")
caso("B16 (= e3 A3) corte por detrás: «Total 849» en «849'697»", "Total 849'697\n", "Total 849", 849, "ausente")
caso("B17 (= e3 A4) «Total 849'697» con valor 849", "Total 849'697\n", "Total 849'697", 849, "ausente")
caso("B18 (= e3 A12) doble corte «849,7 mill» en «1'849,7 millones»", "Total 1'849,7 millones\n", "849,7 mill", 849.7, "ausente")
print("   -- el apóstrofo TIPOGRÁFICO (W3): lo mismo con «’»")
caso("B19 «Total 1’849,7» (cita completa) con valor 849,7", "Total 1’849,7\n", "Total 1’849,7", 849.7, "ausente")
caso("B20 «849,7» en «1’849,7»", "Total 1’849,7\n", "849,7", 849.7, "ausente")
caso("B21 «Total 849» en «849’697»", "Total 849’697\n", "Total 849", 849, "ausente")
caso("B22 «Total 849’697» con valor 849", "Total 849’697\n", "Total 849’697", 849, "ausente")
print("   -- controles: la cifra entera")
caso("B23 «1'849.7» = 1849,7", "Total 1'849.7\n", "Total 1'849.7", 1849.7, "ok")
caso("B24 «849'697» = 849697", "Total 849'697\n", "Total 849'697", 849697, "ok")
caso("B25 «1'234'567» = 1234567", "Total 1'234'567\n", "Total 1'234'567", 1234567, "ok")
print(f"\n   casos REABIERTOS (45ff57c da «ok» donde 8196522 no): {n_reab}")

print("\n== C · ¿por qué vía se resuelven los casos de la batería? (apariciones de la cita según _apariciones_en_pagina; si son 0, _lectura_cifra no se ejecuta)")
for cita, vf, pag in (("849,7", 849.7, "Total 1'849,7"), ("849,7", 849.7, "Total 1’849,7"), ("Total 849", 849, "Total 849'697"), ("849,7 mill", 849.7, "Total 1'849,7 millones"),
                      ("Total 1'849,7", 849.7, "Total 1'849,7")):
    print(f"   cita={cita!r:18} página={pag!r:26} apariciones: 8196522 {len(VP._apariciones_en_pagina(cita, pag))} · 45ff57c {len(VE._apariciones_en_pagina(cita, pag))}"
          f" · estado 45ff57c: {VE._cita_cifra(cita, vf, pag)}")
