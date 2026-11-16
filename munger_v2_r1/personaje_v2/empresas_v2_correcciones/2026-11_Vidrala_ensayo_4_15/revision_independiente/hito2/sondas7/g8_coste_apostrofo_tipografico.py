#!/usr/bin/env python3
"""g8 · séptima comprobación · el COSTE de W3 y W4 (rechazos prudentes nuevos): «cifra + ’ + cifra» que NO es un separador de miles, con
el apóstrofo tipográfico (lo mismo que W6 anotó para el ASCII) y con el ASCII (que con la candidata vuelven a aceptarse por X1).
Estados con 8196522, 45ff57c, la propuesta de la sexta y la corrección de :542 (fix7).
Uso: python3 -I -B g8_coste_apostrofo_tipografico.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ, F, ACT, ANT, PROP, cargar  # noqa: E402
VF7 = cargar(os.path.join(F, "fix7", "munger_v2_r1", "personaje_v2", "scripts", "verificacion_entradas.py"), "verificacion_entradas_fix7")
print(f"VE = {ACT} · VP = {ANT} · VQ = {PROP} · VF7 = 45ff57c con la corrección de :542")
CASOS = [
    ("periodo abreviado «Q1{a}24», valor 24, cita completa", "Ventas Q1{a}24 crecen\n", "Ventas Q1{a}24 crecen", 24),
    ("«Q1{a}24» citando desde la cifra «24 crecen»", "Ventas Q1{a}24 crecen\n", "24 crecen", 24),
    ("«Q1{a}24» citando hasta la cifra «Ventas Q1» con valor 1", "Ventas Q1{a}24 crecen\n", "Ventas Q1", 1),
    ("«9M{a}24 849,7»: la cifra de después", "Ventas 9M{a}24 849,7\n", "Ventas 9M{a}24 849,7", 849.7),
    ("«H1{a}24: 24 tiendas» (el 24 aparece además suelto)", "H1{a}24: 24 tiendas\n", "H1{a}24: 24 tiendas", 24),
    ("«FY{a}24» con valor 24 (no hay cifra delante)", "Ventas FY{a}24\n", "Ventas FY{a}24", 24),
    ("minutos y segundos «5{a}30» con valor 30", "Tiempo 5{a}30\n", "Tiempo 5{a}30", 30),
    ("llamada de nota tras comilla de cierre «Vision 2030{a}1» con valor 2030", "the ‘Vision 2030{a}1 plan\n", "the ‘Vision 2030{a}1 plan", 2030),
    ("   … citando «Vision 2030»", "the ‘Vision 2030{a}1 plan\n", "Vision 2030", 2030),
    ("posesivo «SBF 120{a}s» con valor 120 (forma real de Elis)", "the SBF 120{a}s circular economy\n", "the SBF 120{a}s circular", 120),
    ("elisión «d{a}1,5 %» con valor 1,5", "une hausse d{a}1,5 %\n", "une hausse d{a}1,5 %", 1.5),
    ("«l{a}exercice 2023» con valor 2023", "l{a}exercice 2023\n", "l{a}exercice 2023", 2023),
    ("decimal con apóstrofo «2{a}5 puntos» con valor 2,5 (forma que _cifras no genera)", "sube 2{a}5 puntos\n", "sube 2{a}5 puntos", 2.5),
    ("   … el mismo texto con valor 5", "sube 2{a}5 puntos\n", "sube 2{a}5 puntos", 5),
    ("la cifra entera con miles «1{a}849.7» = 1849,7", "Total 1{a}849.7\n", "Total 1{a}849.7", 1849.7),
    ("la cifra entera «849{a}697» = 849697", "Total 849{a}697\n", "Total 849{a}697", 849697),
]
for nom, ap in (("ASCII '", "'"), ("tipográfico ’", "’")):
    print(f"\n== apóstrofo {nom}")
    for nombre, pag, cita, vf in CASOS:
        pag, cita, nombre = pag.replace("{a}", ap), cita.replace("{a}", ap), nombre.replace("{a}", ap)
        r = [m._cita_cifra(cita, vf, pag)[0] for m in (VP, VE, VQ, VF7)]
        marca = ("   ← cambia con la candidata" if r[0] != r[1] else "") + ("   <<< 45ff57c ≠ corrección" if r[1] != r[3] else "") + ("   <<< corrección ≠ propuesta 6.ª" if r[2] != r[3] else "")
        print(f"   {nombre:82} 8196522: {r[0]:20} 45ff57c: {r[1]:20} propuesta 6.ª: {r[2]:20} fix7: {r[3]:20}{marca}")
