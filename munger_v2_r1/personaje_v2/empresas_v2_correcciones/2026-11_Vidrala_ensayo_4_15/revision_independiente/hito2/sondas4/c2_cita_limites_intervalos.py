#!/usr/bin/env python3
"""c2 · T2 y T8 (cuarta comprobación), a nivel de unidad (_cita_cifra con la página), candidata anterior (f3d15e8) → cuarta (7a6583b).
A) límites de la cita según el carácter del borde: lo que la regla nueva ACEPTA de más (¿algo indebido?) y lo que sigue rechazando.
B) «ausente» (discrepancia) frente a «no_localizada» (pendiente) de una cita cortada: ¿el corte dentro de un número se clasifica siempre
   como discrepancia, y el corte dentro de una palabra como pendiente? Casos en que un punto o una coma pegados NO son de un número.
C) intervalos y fechas: enteros de la misma longitud (lo que sigue leyéndose como intervalo), rangos legítimos que ahora quedan pendientes
   y los prefijos FY/AF/EJ.
`esp` es lo que el revisor espera: «ok», un estado concreto, o «no ok» (cualquier cosa menos «ok»).
Uso: python3 -I -B c2_cita_limites_intervalos.py"""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, VP, ACT, ANT  # noqa: E402

print(f"VE = {ACT} · VP = {ANT}")
N = {"distintos": 0, "acepta_contrario": 0, "nuevos_ok": 0}


def caso(nombre, pagina, cita, vf, esp, nota=""):
    a, (b, det) = VP._cita_cifra(cita, vf, pagina)[0], VE._cita_cifra(cita, vf, pagina)
    bien = (b == esp) or (esp == "no ok" and b != "ok")
    marca = ""
    if not bien:
        N["distintos"] += 1
        marca = f"   <<< el revisor esperaba «{esp}»" + (" (ACEPTA)" if b == "ok" else "")
    if a != "ok" and b == "ok":
        N["nuevos_ok"] += 1
    print(f"   {nombre}\n      página={pagina!r} cita={cita!r} vf={vf!r}\n      anterior: {a:20} cuarta: {b} ({det[:95]}){marca}" + (f"\n      nota: {nota}" if nota else ""))


print("\n== A · límites de la cita: lo que la regla nueva acepta de más")
caso("A1 la cita empieza en la cifra y la página lleva una letra pegada delante (identificador): «T5»", "Nota T5 del anexo\n", "5 del anexo", 5, "ok", "la cifra se publica entera; qué es «T5» lo decide el revisor (igual que en 92b2362)")
caso("A2 negativo con letra pegada delante del guion: «T4-15,2», la cita empieza en la cifra", "Variación T4-15,2\n", "15,2", 15.2, "signo_indeterminado")
caso("A3 lo mismo con el valor negativo", "Variación T4-15,2\n", "15,2", -15.2, "signo_indeterminado")
caso("A4 la cita acaba en la cifra y sigue una letra de unidad que cambia la magnitud: «849.7bn» (la escala es otro control)", "Revenue 849.7bn\n", "Revenue 849.7", 849.7, "ok")
caso("A5 la cita acaba en la cifra y sigue un superíndice numérico Unicode «²» (llamada de nota)", "Ventas 849,7²\n", "Ventas 849,7", 849.7, "ok")
caso("A6 la cita acaba en la cifra y sigue un exponente «e3» (notación científica: 849,7e3 es otro número)", "Importe 849,7e3\n", "Importe 849,7", 849.7, "no ok", "un número en notación científica no es la cifra citada")
caso("A7 cifra hexadecimal o código: «0x1F849» y la cita «849»", "Código 0x1F849\n", "849", 849, "no ok", "«849» va pegado a letras y cifras de un código")
caso("A8 la cita empieza en una letra pegada a una cifra: «2024Total 849,7»", "2024Total 849,7\n", "Total 849,7", 849.7, "ok")
caso("A9 la cita acaba en una letra pegada a una cifra: «EBITDA2024 849,7» citada «849,7» (control) y «EBITDA» + cifra", "EBITDA2024 849,7\n", "EBITDA2024 849,7", 849.7, "ok")
caso("A10 subrayado pegado: «total_849,7» citada «849,7»", "total_849,7\n", "849,7", 849.7, "ok")
caso("A11 la cita empieza por una letra con tilde dentro de una palabra: «Año» de «Baño 849,7»", "Baño 849,7\n", "año 849,7", 849.7, "no_localizada")
caso("A12 control (N10): «Total 5» dentro de «Subtotal 5,01»", "Subtotal 5,01\n", "Total 5", 5, "ausente")
caso("A13 control: «Total 5» dentro de «Subtotal 5» (corte solo en la palabra)", "Subtotal 5\n", "Total 5", 5, "no_localizada")
caso("A14 la cita «5» aparece limpia y además dentro de un código «A5» en otra línea, con signo distinto: «A-5»", "Resultado 5\nReferencia A-5\n", "5", 5, "signo_indeterminado", "dos apariciones con lecturas distintas: pendiente")
caso("A15 miles con espacio: la cita «697» de «849 697» (límite declarado: no se distingue de dos cifras)", "Total 849 697\n", "697", 697, "ok", "límite declarado en _cita_contiene")

print("\n== B · «ausente» frente a «no_localizada» de una cita cortada")
caso("B1 corte al principio dentro de un número", "Total 849,697.000\n", "697.000", 697, "ausente")
caso("B2 corte al final dentro de un número", "Total 8496970\n", "Total 849697", 849697, "ausente")
caso("B3 corte al final ante separador decimal", "Ratio 0,49\n", "Ratio 0", 0, "ausente")
caso("B4 corte al principio dentro de una palabra", "Subtotal 849,7\n", "total 849,7", 849.7, "no_localizada")
caso("B5 corte al final dentro de una palabra", "Ventas 849,7 millones\n", "Ventas 849,7 mill", 849.7, "no_localizada")
caso("B6 punto final de frase pegado delante de la cifra (no es de un número): «ejercicio.849,7»", "al cierre del ejercicio.849,7 millones\n", "849,7 millones", 849.7, "no_localizada",
     "el punto pegado se toma por separador de un número: sale «ausente» (discrepancia) con el mensaje de la cifra")
caso("B7 abreviatura pegada: «p.12» para 12", "véase p.12 del informe\n", "12 del informe", 12, "no_localizada", "ídem")
caso("B8 fecha con puntos y la cita empieza en el año: «31.12.2024 849,7»", "Cierre 31.12.2024 849,7\n", "2024 849,7", 849.7, "no_localizada", "ídem: el corte cae dentro de una FECHA, no de la cifra citada")
caso("B9 puntos conductores pegados: «.......130,8» (r2 C25)", "Total ............130,8\n", "130,8", 130.8, "no_localizada", "ídem")
caso("B10 corte dentro de una palabra en una aparición y dentro de un número en otra", "Subtotal 5\nTotal 51\n", "Total 5", 5, "ausente")
caso("B11 la cita limpia existe: los fragmentos de otras líneas no cuentan", "Total 5\nSubtotal 51\n", "Total 5", 5, "ok")
caso("B12 cita cortada dentro de una palabra con el signo CONTRARIO al publicado", "Subtotal (849,7)\n", "total (849,7)", 849.7, "no ok")

print("\n== C · intervalos y fechas")
caso("C1 año pegado a un negativo de CUATRO cifras: «Saldo 2023-1849» (publica −1849), contrastado con +1849", "Saldo 2023-1849\n", "Saldo 2023-1849", 1849, "no ok",
     "dos enteros de la misma longitud se leen como intervalo: +1849 vale")
caso("C2 lo mismo con el valor publicado −1849", "Saldo 2023-1849\n", "Saldo 2023-1849", -1849, "no ok", "no puede darse por bueno ni por malo: debería ser pendiente; sale «signo_distinto»")
caso("C3 nota de una cifra pegada a un negativo de una cifra: «Resultado financiero 1-5» con +5", "Resultado financiero 1-5\n", "Resultado financiero 1-5", 5, "no ok", "ídem")
caso("C4 nota de dos cifras y negativo de dos: «Dotaciones 12-45» con +45", "Dotaciones 12-45\n", "Dotaciones 12-45", 45, "no ok", "ídem")
caso("C5 (corregido) «Saldo 2023-849» con +849", "Saldo 2023-849\n", "Saldo 2023-849", 849, "signo_indeterminado")
caso("C6 (corregido) «Resultado financiero 1-149» con +149", "Resultado financiero 1-149\n", "Resultado financiero 1-149", 149, "signo_indeterminado")
caso("C7 intervalo de años", "Periodo 2019-2020\n", "Periodo 2019-2020", 2020, "ok")
caso("C8 «FY2023-2024»", "FY2023-2024 results\n", "FY2023-2024", 2024, "ok")
caso("C9 «AF2023-2024» / «EJ2023–2024»", "EJ2023–2024\n", "EJ2023–2024", 2024, "ok")
caso("C10 prefijo que no es FY/AF/EJ: «H2023-2024»", "H2023-2024\n", "H2023-2024", 2024, "signo_indeterminado")
caso("C11 palabra que acaba en «af» pegada a un año y un negativo de cuatro cifras: «Graf2023-1849» con +1849", "Graf2023-1849\n", "Graf2023-1849", 1849, "no ok", "el prefijo no se ancla: cualquier palabra que acabe en fy, af o ej")
caso("C12 ejercicio partido «2024-25» para 25 (antes «ok»)", "Ejercicio 2024-25\n", "Ejercicio 2024-25", 25, "ok", "ahora pendiente: los dos enteros no tienen la misma longitud")
caso("C13 páginas «9-10» para 10 (antes «ok»)", "Páginas 9-10\n", "Páginas 9-10", 10, "ok", "ídem")
caso("C14 vida útil «5-10 años» para 10 (antes «ok»)", "Vida útil 5-10 años\n", "Vida útil 5-10 años", 10, "ok", "ídem")
caso("C15 mes y año «12-2024» para 2024 (antes «ok»)", "Cierre 12-2024\n", "Cierre 12-2024", 2024, "ok", "ídem")
caso("C16 fecha ISO «2024-12-31», el mes 12 (antes «ok»)", "Cierre 2024-12-31\n", "Cierre 2024-12-31", 12, "ok", "ídem")
caso("C17 fecha ISO, el día 31", "Cierre 2024-12-31\n", "Cierre 2024-12-31", 31, "ok")
caso("C18 fecha «31-12-2024», el año", "Cierre 31-12-2024\n", "Cierre 31-12-2024", 2024, "ok")
caso("C19 fecha «1-1-2024», el año", "Cierre 1-1-2024\n", "Cierre 1-1-2024", 2024, "ok")
caso("C20 fecha «31-12-24», el año con dos cifras", "Cierre 31-12-24\n", "Cierre 31-12-24", 24, "ok")
caso("C21 «d-m-» seguido de un importe de cuatro cifras: «Notas 5-6-1849» (publica −1849) con +1849", "Notas 5-6-1849\n", "Notas 5-6-1849", 1849, "no ok", "la regla de la fecha solo mira la forma «d-m-aaaa»")
caso("C22 año de la columna y negativo entero de cuatro cifras con raya: «2023–1849»", "Saldo 2023–1849\n", "Saldo 2023–1849", 1849, "no ok", "como C1, con raya")
print(f"\n{N['distintos']} casos distintos de lo esperado por el revisor · {N['nuevos_ok']} pasan de rechazo a «ok» con la cuarta")
