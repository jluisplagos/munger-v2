#!/usr/bin/env python3
"""r5 · N4, N5 y N10 a nivel de unidad (_cita_cifra con la página), candidata anterior (92b2362) frente a la tercera (f3d15e8).
A) N4: casos que SOLO decide la regla «la cifra dentro de la cita» (la cita no empieza ni acaba dentro de una palabra o de una cifra según
   la regla de N10, pero no contiene la cifra entera): la cita acaba en «.» o «,», empieza por «.», o la cifra lleva los miles con espacio.
B) N5: enteros pegados por un guion (lo que la regla sigue leyendo como intervalo) y rangos que ahora quedan pendientes.
C) N10: «cifra)» sin «(» en la línea, con paréntesis anteriores, de varias líneas y enumeraciones.
Uso: python3 -I -B r5_n4_n5_n10_unidad.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, ACT, ANT

n_mal = 0


def fila(nombre, pag, cita, vf, espera):
    """espera: «ok», «rechazo» (cualquier estado distinto de ok), o un estado concreto."""
    global n_mal
    e2, e1 = VE._cita_cifra(cita, vf, pag), VP._cita_cifra(cita, vf, pag)
    real = "ok" if e2[0] == "ok" else "rechazo"
    bien = espera in (real, e2[0])
    marca = "" if bien else ("   <<< ACEPTA lo que no debería" if real == "ok" else f"   <<< el revisor esperaba «{espera}»")
    if not bien and e1[0] == "ok" and real != "ok":
        marca += " (la anterior daba «ok»)"
    print(f"   {nombre}\n      página={pag!r} cita={cita!r} vf={vf!r}\n      anterior: {e1[0]:20} tercera: {e2[0]} ({e2[1][:90]}){marca}")
    n_mal += not bien


print(f"VE = {ACT} · VP = {ANT}")
print("\n== A · N4: la cita toca la cifra sin contenerla y NO empieza ni acaba dentro de una palabra o cifra según la regla del fragmento")
for a in [("A1 la cita acaba en el punto de los miles: «Total 849.» (página «Total 849.697», valor 849697)", "Total 849.697\n", "Total 849.", 849697, "ausente"),
          ("A2 la cita acaba en la coma decimal: «Total 849,» (página «Total 849,697», valor 849,697)", "Total 849,697\n", "Total 849,", 849.697, "ausente"),
          ("A3 la cita empieza por el punto: «.000» (página «849697.000»)", "Total 849697.000\n", ".000", 849697, "ausente"),
          ("A4 miles con espacio: la cita «697.000» (página «849 697.000», valor 849697)", "Total 849 697.000\n", "697.000", 849697, "ausente"),
          ("A5 miles con espacio: la cita «Total 849» (página «Total 849 697,5», valor 849697,5)", "Total 849 697,5\n", "Total 849", 849697.5, "ausente"),
          ("A6 la cita «(» + parte: «Pagos (130.» (página «Pagos (130.8)», valor −130,8)", "Pagos (130.8)\n", "Pagos (130.", -130.8, "ausente"),
          ("A7 control: la cita contiene la cifra y acaba en el punto final de la frase", "Total 849.697.\n", "Total 849.697.", 849697, "ok")]:
    fila(*a)

print("\n== B · N5: guion pegado entre cifras")
for b in [("B1 año de la columna pegado a un negativo ENTERO: «Saldo 2023-849» (publica −849), contrastado con +849", "Saldo 2023-849\n", "Saldo 2023-849", 849, "rechazo"),
          ("B2 lo mismo contrastado con el valor publicado −849", "Saldo 2023-849\n", "Saldo 2023-849", -849, "rechazo"),
          ("B3 llamada de nota separada del rótulo y pegada a un negativo entero: «Resultado financiero 1-149», con +149", "Resultado financiero 1-149\n", "Resultado financiero 1-149", 149, "rechazo"),
          ("B4 trimestre pegado a un negativo entero: «T4-15» con +15", "Variación T4-15\n", "Variación T4-15", 15, "rechazo"),
          ("B5 miles con punto y negativo entero pegado: «1.234-567» con +567", "Flujo 1.234-567\n", "Flujo 1.234-567", 567, "rechazo"),
          ("B6 intervalo de años", "Periodo 2019-2020\n", "Periodo 2019-2020", 2020, "ok"),
          ("B7 intervalo de años con raya", "Periodo 2019–2020\n", "Periodo 2019–2020", 2020, "ok"),
          ("B8 fecha dd-mm-aaaa", "Cierre 31-12-2024\n", "Cierre 31-12-2024", 2024, "ok"),
          ("B9 fecha aaaa-mm-dd, el día", "Cierre 2024-12-31\n", "Cierre 2024-12-31", 31, "ok"),
          ("B10 ejercicio partido «2024-25»", "Ejercicio 2024-25\n", "Ejercicio 2024-25", 25, "ok"),
          ("B11 intervalo de años con prefijo pegado: «FY2023-2024»", "FY2023-2024 results\n", "FY2023-2024", 2024, "ok"),
          ("B12 rango de enteros de más de cuatro cifras: «10000-20000 empleados»", "Entre 10000-20000 empleados\n", "10000-20000 empleados", 20000, "ok"),
          ("B13 rango con miles: «10.000-20.000»", "Entre 10.000-20.000 empleados\n", "10.000-20.000 empleados", 20000, "ok"),
          ("B14 rango de porcentajes con decimales: «7-7,5 %»", "Margen del 7-7,5 %\n", "7-7,5 %", 7.5, "ok"),
          ("B15 rango de importes con decimales: «1,5-2,5 millones»", "Entre 1,5-2,5 millones\n", "1,5-2,5 millones", 2.5, "ok"),
          ("B16 artículo de ley «L. 225-129-5» (el 5)", "art. L. 225-129-5\n", "L. 225-129-5", 5, "ok"),
          ("B17 negativo con decimales pegado a un año (lo que corrige N5): «2023-849,7» con +849,7", "Saldo 2023-849,7\n", "Saldo 2023-849,7", 849.7, "rechazo"),
          ("B18 lo mismo con el valor publicado −849,7 (pendiente: no puede determinarse)", "Saldo 2023-849,7\n", "Saldo 2023-849,7", -849.7, "signo_indeterminado")]:
    fila(*b)

print("\n== C · N10: «cifra)» sin «(» en la línea")
for c_ in [("C1 «(» en la línea anterior, la cita es la segunda línea: positivo → pendiente", "Pagos (\n849,7)\n", "849,7", 849.7, "signo_indeterminado"),
           ("C2 lo mismo con el valor negativo y la cita de las dos líneas", "Pagos (\n849,7)\n", "Pagos ( 849,7)", -849.7, "ok"),
           ("C3 hay OTRO paréntesis, ya cerrado, antes en la línea: «(nota 5) 849,7)» y el «(» del negativo está en la línea anterior", "Arrendamientos (\n(nota 5) 849,7)\n", "(nota 5) 849,7", 849.7, "rechazo"),
           ("C4 positivo al final de un inciso de dos líneas: «(incluye amortización de⏎849,7)», la cita es la segunda línea", "Gastos (incluye amortización de\n849,7) y otros\n", "849,7", 849.7, "ok"),
           ("C5 lo mismo con la cita de las dos líneas", "Gastos (incluye amortización de\n849,7) y otros\n", "(incluye amortización de 849,7)", 849.7, "ok"),
           ("C6 positivo dentro de un inciso en la misma línea: «(2024: 849,7)»", "EBITDA (2024: 849,7)\n", "2024: 849,7", 849.7, "ok"),
           ("C7 remisión: «(véase la nota 12)» para 12", "Deuda (véase la nota 12)\n", "nota 12", 12, "ok"),
           ("C8 enumeración: «1) Ventas» para 1", "1) Ventas 849,7\n", "1) Ventas", 1, "ok"),
           ("C9 cifra seguida de «)» de una llamada de nota: «849,7 1)»", "Ventas 849,7 1)\n", "Ventas 849,7", 849.7, "ok")]:
    fila(*c_)
print(f"\n{n_mal} casos distintos de lo esperado por el revisor")
