#!/usr/bin/env python3
"""r5 · octava comprobación · el registro CORREGIDO (`HITO_2_4_15.md` §1 y §5 de 0a0020b) frente al código del árbol, a nivel de unidad.
Para cada forma: lo que el registro dice ahora que pasa y lo que pasa con `verificacion_entradas._cita_cifra` de 0a0020b.
«pendiente» = signo_indeterminado o no_localizada; «discrepancia» = ausente o signo_distinto; «aceptada» = ok. Se marca lo que no coincide.
(Las formas son las de sondas7/g7, reordenadas según el texto nuevo, más las frases corregidas de §1 y lo nuevo de §5.)
Uso: python3 -I -B r5_registro_limites.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, PV, PVP, cargar, huella  # noqa: E402
VE = cargar(os.path.join(PV, "scripts", "verificacion_entradas.py"), "ve_0a0020b", os.path.join(PV, "scripts"))
VP = cargar(os.path.join(PVP, "scripts", "verificacion_entradas.py"), "ve_45ff57c", os.path.join(PVP, "scripts"))
assert huella(VE.__file__).startswith("4b00aa2a") and huella(VP.__file__).startswith("7abbb081")
CLASE = {"ok": "aceptada", "signo_indeterminado": "pendiente", "no_localizada": "pendiente", "ausente": "discrepancia", "signo_distinto": "discrepancia"}
T = "’"
n_mal = 0


def caso(nombre, pag, cita, vf, declarado):
    global n_mal
    a, b = VP._cita_cifra(cita, vf, pag)[0], VE._cita_cifra(cita, vf, pag)[0]
    marca = ""
    if declarado and CLASE[b] != declarado:
        n_mal += 1
        marca = f"   <<< el registro dice «{declarado}»"
    print(f"   {nombre:92} 45ff57c: {a:20} 0a0020b: {b:20} ({CLASE[b]}){marca}")


print("== §5 · Signo, «en el sentido de aceptar»")
caso("H3: guion separado por varios espacios, «Total -   849,7» con +849,7", "Total -   849,7\n", "Total -   849,7", 849.7, "aceptada")
caso("carácter invisible entre el signo y la cifra «-<U+200B>849,7» con +849,7", "Resultado -​849,7\n", "Resultado -​849,7", 849.7, "aceptada")
caso("signo escrito con palabras «menos 149,5» con +149,5", "Resultado menos 149,5\n", "Resultado menos 149,5", 149.5, "aceptada")
caso("importe que parece un año «Saldo 2023-2049» (publica −2049) con +2049", "Saldo 2023-2049\n", "Saldo 2023-2049", 2049, "aceptada")
caso("regla de la fecha «Notas 5-6-1849» con +1849", "Notas 5-6-1849\n", "Notas 5-6-1849", 1849, "aceptada")
print("== §5 · Signo, «pendientes por prudencia»")
caso("«(149.5m)» con −149,5", "Resultado (149.5m)\n", "Resultado (149.5m)", -149.5, "pendiente")
caso("«(-x)»: «(-149,5)» con −149,5", "Resultado (-149,5)\n", "Resultado (-149,5)", -149.5, "pendiente")
caso("«31-dic-2024» con 2024", "Cierre 31-dic-2024\n", "Cierre 31-dic-2024", 2024, "pendiente")
caso("«2024-25» con 25", "Ejercicio 2024-25\n", "Ejercicio 2024-25", 25, "pendiente")
caso("«12-2024» con 2024", "Periodo 12-2024\n", "Periodo 12-2024", 2024, "pendiente")
caso("«7-7,5 %» con 7,5", "Rango 7-7,5 %\n", "Rango 7-7,5 %", 7.5, "pendiente")
caso("«2-3 %» con 3", "Rango 2-3 %\n", "Rango 2-3 %", 3, "pendiente")
caso("«100-150» con 150", "Entre 100-150 millones\n", "Entre 100-150 millones", 150, "pendiente")
caso("años decrecientes «2024-2023» con 2023", "Variación 2024-2023\n", "Variación 2024-2023", 2023, "pendiente")
caso("el día de una fecha ISO «2024-12-31» con 31", "Cierre 2024-12-31\n", "Cierre 2024-12-31", 31, "pendiente")
caso("«31-12-24» con 24", "Cierre 31-12-24\n", "Cierre 31-12-24", 24, "pendiente")
print("== §5 · Signo y cifra, «discrepancias por prudencia (bloquean siempre)»")
caso("intervalo partido por un salto de línea «Plan 2023⏎–2026» con +2026 (cita de las dos líneas)", "Plan 2023\n–2026\n", "Plan 2023 –2026", 2026, "discrepancia")
caso("   … citando solo «–2026»", "Plan 2023\n–2026\n", "–2026", 2026, "discrepancia")
caso("«. . . .130,8» citada desde la cifra", "Total . . . .130,8\n", "130,8", 130.8, "discrepancia")
caso("   … con la cita completa", "Total . . . .130,8\n", "Total . . . .130,8", 130.8, "discrepancia")
caso("«ejercicio .849,7» citada «849,7 millones»", "al cierre del ejercicio .849,7 millones\n", "849,7 millones", 849.7, "discrepancia")
caso("   … con la cita completa", "al cierre del ejercicio .849,7 millones\n", "al cierre del ejercicio .849,7 millones", 849.7, "discrepancia")
caso("«Q1'24» con 24 (cita completa)", "Ventas Q1'24 crecen\n", "Ventas Q1'24 crecen", 24, "discrepancia")
caso("   … citando desde la cifra «24 crecen»", "Ventas Q1'24 crecen\n", "24 crecen", 24, "discrepancia")
caso(f"«Q1{T}24» con 24 (cita completa)", f"Ventas Q1{T}24 crecen\n", f"Ventas Q1{T}24 crecen", 24, "discrepancia")
caso(f"«5{T}30» con 30", f"Tiempo 5{T}30\n", f"Tiempo 5{T}30", 30, "discrepancia")
caso(f"«2{T}5» con 5", f"sube 2{T}5 puntos\n", f"sube 2{T}5 puntos", 5, "discrepancia")
caso(f"llamada de nota tras comilla de cierre «‘Vision 2030{T}1» con 2030", f"the ‘Vision 2030{T}1 plan\n", f"the ‘Vision 2030{T}1 plan", 2030, "discrepancia")
caso(f"la cifra entera con «’»: «1{T}849.7» = 1849,7 («da discrepancia con el valor correcto»)", f"Total 1{T}849.7\n", f"Total 1{T}849.7", 1849.7, "discrepancia")
caso("   (control, no declarado como límite) la cifra entera con «'»: «1'849.7» = 1849,7", "Total 1'849.7\n", "Total 1'849.7", 1849.7, "aceptada")
print("== §5 · Apóstrofos y espacios, «en el sentido de aceptar»")
for nom, ap in (("U+02BC ʼ", "ʼ"), ("U+2032 ′", "′"), ("U+00B4 ´", "´"), ("U+0060 `", "`"), ("U+2018 ‘", "‘")):
    caso(f"signo parecido al apóstrofo {nom}: «1{ap}849,7» citada «849,7»", f"Total 1{ap}849,7\n", "849,7", 849.7, "aceptada")
caso("miles con espacio «1 849,7» citada «849,7» («queda comprobada»)", "Total 1 849,7\n", "849,7", 849.7, "aceptada")
print("== §5 · lo que el registro ya NO declara (X3 b): «$» en en_numero tras una línea que acaba en cifra")
caso("«Ventas 2023⏎849,7 millones» citada «849,7 mill» (ahora pendiente; antes se declaraba discrepancia)", "Ventas 2023\n849,7 millones\n", "849,7 mill", 849.7, "pendiente")
print("== §1 · las dos frases corregidas (X3 c)")
caso("«un intervalo entre dos años crecientes de 1900 a 2100»: «Periodo 2019-2020» con 2020", "Periodo 2019-2020\n", "Periodo 2019-2020", 2020, "aceptada")
caso("   «con prefijo como palabra»: «FY2023-2024» con 2024", "Plan FY2023-2024\n", "Plan FY2023-2024", 2024, "aceptada")
caso("   prefijo que no es palabra suelta: «XFY2023-2024» con 2024", "Plan XFY2023-2024\n", "Plan XFY2023-2024", 2024, "pendiente")
caso("   «o una fecha d-m-aaaa»: «31-12-2024» con 2024", "Cierre 31-12-2024\n", "Cierre 31-12-2024", 2024, "aceptada")
caso("   «entre otros enteros el signo queda pendiente»: «9-10» con 10", "Notas 9-10\n", "Notas 9-10", 10, "pendiente")
caso("   años fuera de 1900–2100: «1850-1899» con 1899", "Serie 1850-1899\n", "Serie 1850-1899", 1899, "pendiente")
caso("   años iguales «2023-2023» con 2023 (el código admite ≤, el registro dice «crecientes»)", "Plan 2023-2023\n", "Plan 2023-2023", 2023, None)
caso("«cortada dentro de un número → discrepancia»: «849,7» en «1849,7»", "Total 1849,7\n", "849,7", 849.7, "discrepancia")
caso("«cortada dentro de una palabra → pendiente»: «otal 849,7» en «Total 849,7»", "Total 849,7\n", "otal 849,7", 849.7, "pendiente")
caso("«no localizada → pendiente»: la cita no está en la página", "Total 849,7\n", "Suma 849,7", 849.7, "pendiente")
print(f"\nformas en las que el registro corregido no coincide con lo que hace el código de 0a0020b: {n_mal}")

print("\n== lo que el registro NO dice de X5 (`fase1_historia.importe_completo`, el control de la fase 1): los mismos límites y costes, allí")
for nota, imp, texto in (("acepta (apóstrofo raro)", "849,7", "Total 1ʼ849,7"), ("acepta (miles con espacio)", "849,7", "Total 1 849,7"),
                         ("rechaza (coste prudente: «Q1'24»)", "24", "Ventas Q1'24 crecen"), (f"rechaza (coste prudente: nota tras comilla)", "2030", f"the ‘Vision 2030{T}1 plan")):
    print(f"   importe_completo({imp!r}, {texto!r}) = {FN.importe_completo(FN.norm(imp), FN.norm(texto))} · {nota}")
try:
    FN.numero("1'849,7")
    print("   numero(\"1'849,7\") se admite")
except ValueError as ex:
    print(f"   numero(\"1'849,7\") → ValueError: {ex} (un impreso con apóstrofo de miles no es numérico para la fase 1: error, prudente, ya existía)")
sys.exit(0 if n_mal == 0 else 1)
