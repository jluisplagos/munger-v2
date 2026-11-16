#!/usr/bin/env python3
"""(ADAPTADA en la séptima comprobación: VE = 45ff57c, VP = 8196522, VPR = 8196522 con las propuestas de la sexta; solo cambian el arnés y los rótulos; las notas de los casos son las de la quinta)
d7 · bordes a nivel de unidad (quinta comprobación), 7a6583b → 8196522 (y la propuesta del revisor de la cuarta, que no es código
entregado). A) Q3: casos que DISCRIMINAN cada condición de la regla nueva (los que la prueba de la batería no tiene) y otros bordes.
B) Q4: el punto o la coma delante de la cifra: fin de frase, abreviatura, puntos conductores, fecha, y el DECIMAL SIN CERO DELANTE
(«.5», «-.5», «(.5)», «$.85», «,5»), donde el separador sí es de un número. C) límites ya existentes que se cruzan con lo cambiado.
Uso: python3 -I -B d7_unidad_bordes.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun7 import VE, VP, VQ as VPR, ACT, ANT  # noqa: E402
print(f"VE = {ACT} · VP = {ANT} · VPR = 45ff57c con las propuestas W3–W5 del revisor de la sexta comprobación")


def caso(nombre, pagina, cita, vf, esperado=None, nota=""):
    a, b, p = VP._cita_cifra(cita, vf, pagina), VE._cita_cifra(cita, vf, pagina), VPR._cita_cifra(cita, vf, pagina)
    marca = "" if esperado is None or b[0] == esperado or (esperado == "no ok" and b[0] != "ok") else f"   <<< el revisor esperaba «{esperado}»"
    print(f"   {nombre}\n      página={pagina!r} cita={cita!r} vf={vf!r}\n      8196522: {a[0]:20} 45ff57c: {b[0]:20} propuesta 6.ª: {p[0]:20}{marca}" + (f"\n      nota: {nota}" if nota else ""))
    return b


print("\n== A · Q3: una condición cada vez")
caso("A1 prefijo sin anclar con dos años crecientes: «Graf2023-2024» (discrimina el anclaje; la batería usa «Graf2023-1849», que no)", "Graf2023-2024\n", "Graf2023-2024", 2024, "signo_indeterminado")
caso("A2 «Staff2023-2024» (acaba en «af»)", "Staff2023-2024\n", "Staff2023-2024", 2024, "signo_indeterminado")
caso("A3 fuera del rango por arriba: «Saldo 2023-2849» (publica −2849) con +2849 (discrimina el rango)", "Saldo 2023-2849\n", "Saldo 2023-2849", 2849, "signo_indeterminado")
caso("A4 fuera del rango por abajo: «1849-1850» para 1850", "Periodo 1849-1850\n", "Periodo 1849-1850", 1850, "signo_indeterminado", "años anteriores a 1900: pendiente (conservador)")
caso("A5 años decrecientes: «Variación 2024-2023» para 2023 (discrimina «crecientes»)", "Variación 2024-2023\n", "Variación 2024-2023", 2023, "signo_indeterminado", "forma habitual de una comparación: pendiente (conservador)")
caso("A6 el mismo año: «2024-2024»", "Periodo 2024-2024\n", "Periodo 2024-2024", 2024, "ok")
caso("A7 límites del rango: «1900-2100»", "Periodo 1900-2100\n", "Periodo 1900-2100", 2100, "ok")
caso("A8 «2100-2101»", "Periodo 2100-2101\n", "Periodo 2100-2101", 2101, "signo_indeterminado")
caso("A9 importe de cuatro cifras entre 1900 y 2100 tras un año menor: «Saldo 2023-2049» (publica −2049) con +2049", "Saldo 2023-2049\n", "Saldo 2023-2049", 2049, None,
     "indistinguible de un intervalo de años: se lee en positivo (límite inherente a la regla)")
caso("A10 lo mismo con el valor publicado −2049", "Saldo 2023-2049\n", "Saldo 2023-2049", -2049, None, "discrepancia en falso si la página publicaba −2049")
caso("A11 cadena de años «2018-2019-2020», el último", "Periodo 2018-2019-2020\n", "Periodo 2018-2019-2020", 2020, "ok")
caso("A12 con raya y con menos Unicode: «2019–2020», «2019−2020»", "Periodo 2019–2020 y 2021−2022\n", "Periodo 2019–2020 y 2021−2022", 2022, "ok")
caso("A13 año tras barra: «2023/2024-2025»", "Plan 2023/2024-2025\n", "Plan 2023/2024-2025", 2025, "ok")
caso("A14 prefijo con espacio: «FY 2023-2024»", "FY 2023-2024\n", "FY 2023-2024", 2024, "ok")
caso("A15 prefijo en minúsculas y tras paréntesis: «(fy2023-2024)»", "(fy2023-2024)\n", "(fy2023-2024)", 2024, "ok")
caso("A16 prefijo tras guion bajo: «_FY2023-2024»", "x_FY2023-2024\n", "x_FY2023-2024", 2024, "signo_indeterminado")
caso("A17 ejercicio partido con cuatro cifras y espacio: «2023 - 2024» (un espacio a cada lado)", "Ejercicio 2023 - 2024\n", "Ejercicio 2023 - 2024", 2024, None, "guion a un espacio: indeterminado (ya era así)")
caso("A18 fecha «31-12-2024» y «1-1-2024»", "Cierre 31-12-2024 y apertura 1-1-2024\n", "Cierre 31-12-2024", 2024, "ok")
caso("A19 «d-m-» seguido de un importe de cuatro cifras: «Notas 5-6-1849» con +1849 (sin cambio: la regla de la fecha solo mira la forma)", "Notas 5-6-1849\n", "Notas 5-6-1849", 1849, None)

print("\n== B · Q4: punto o coma pegados delante de la cifra citada")
caso("B1 fin de frase pegado: «ejercicio.849,7»", "al cierre del ejercicio.849,7 millones\n", "849,7 millones", 849.7, "no_localizada")
caso("B2 abreviatura: «p.12»", "véase p.12 del informe\n", "12 del informe", 12, "no_localizada")
caso("B3 puntos conductores: «....130,8»", "Total ............130,8\n", "130,8", 130.8, "no_localizada")
caso("B4 dentro de un número: «1.849,7» citada «849,7»", "total 1.849,7\n", "849,7", 849.7, "ausente")
caso("B5 fecha con puntos: «31.12.2024 849,7» citada desde el año", "Cierre 31.12.2024 849,7\n", "2024 849,7", 849.7, None, "el corte cae en una fecha: sigue en discrepancia (conservador)")
caso("B6 DECIMAL SIN CERO DELANTE: la página publica «.5» (0,5) y la cita es «5» con valor 5", "Ratio .5 veces\n", "5 veces", 5, "ausente",
     "el punto SÍ es de un número (0,5): antes discrepancia; ahora pendiente con el mensaje «dentro de una palabra»")
caso("B7 lo mismo con signo: «-.5»", "Variación -.5 puntos\n", "5 puntos", 5, "ausente")
caso("B8 lo mismo entre paréntesis: «(.5)»", "Resultado (.5)\n", "5)", 5, "ausente")
caso("B9 lo mismo con moneda (BPA en un informe de EE. UU.): «$.85»", "Earnings per share $.85 $1.02\n", "85 $1.02", 85, "ausente")
caso("B10 lo mismo con coma decimal: «,5»", "Ratio ,5 veces\n", "5 veces", 5, "ausente")
caso("B11 control: el mismo decimal citado CON su punto («.5») y valor 5", "Ratio .5 veces\n", ".5 veces", 5, "no ok", "con la cita completa la cifra se lee en la línea: «ausente»")
caso("B12 control: «.5» citado con su punto y valor 0,5 (la forma «.5» no es una de las de _cifras)", "Ratio .5 veces\n", ".5 veces", 0.5, None, "límite ya existente: un decimal sin cero no se reconoce")
caso("B13 coma de enumeración pegada: «2023,849» citada «849»", "Notas 2023,849 y 850\n", "849 y 850", 849, None, "cifra + coma + cifra: se toma por un número (discrepancia), como antes")
caso("B14 punto tras una cifra de nota: «(1).849,7»", "Ventas (1).849,7\n", "849,7", 849.7, "no_localizada")
caso("B15 punto tras cifra de un código: «F6.849697.000» (c5 B4)", "Partida F6.849697.000\n", "849697.000", 849697, None, "cifra + punto: discrepancia, como antes")

print("\n== C · límites ya existentes que se cruzan con lo cambiado (no son de este diff)")
caso("C1 miles con apóstrofo: «1'849,7» citada «849,7» con valor 849,7", "Total 1'849,7\n", "849,7", 849.7, "no ok", "el apóstrofo no cuenta como parte del número en el límite de la cita")
caso("C2 miles con espacio: «1 849,7» citada «849,7» (límite declarado en _cita_contiene)", "Total 1 849,7\n", "849,7", 849.7, None)
caso("C3 «real» (singular) no es una marca de moneda: unidad «miles de real»", "x\n", "x", 1, None)
print("   _unidad_monetaria_no_reconocida('miles de real') =", VE._unidad_monetaria_no_reconocida("miles de real"), "· ('miles de reales') =", VE._unidad_monetaria_no_reconocida("miles de reales"),
      "· ('reale/usd') =", VE._unidad_monetaria_no_reconocida("reale/usd"))

print("\n== D · el ancla «$» de en_numero y el salto de línea (ya era así con 7a6583b)")
caso("D1 cita cortada dentro de una PALABRA al principio de una línea; la línea anterior acaba en una cifra", "Ventas 2023\n849,7 millones\n", "849,7 mill", 849.7, "no_localizada",
     "«$» casa antes del salto de línea final: la cifra de la línea ANTERIOR se toma por pegada → «ausente» (discrepancia) en vez de pendiente; conservador")
caso("D2 control: la línea anterior acaba en una letra", "Ventas netas\n849,7 millones\n", "849,7 mill", 849.7, "no_localizada")
caso("D3 control: lo mismo en la misma línea, con un espacio", "Ventas 2023 849,7 millones\n", "849,7 mill", 849.7, "no_localizada")
