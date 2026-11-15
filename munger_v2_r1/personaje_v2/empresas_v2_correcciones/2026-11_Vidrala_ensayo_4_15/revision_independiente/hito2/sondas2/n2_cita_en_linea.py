#!/usr/bin/env python3
"""n2 · H1 (segunda pasada): la lectura de la cifra en la LÍNEA de la página (_apariciones_en_pagina, _lectura_cifra, _cita_cifra).
Cada caso: página, cita, valor_fuente y lo que el revisor espera («ok», «rechazo» = discrepancia o pendiente). Se compara la estable con la
candidata de la primera pasada. A) citas reales de varias líneas, columnas y cifras que cruzan el límite del pasaje (¿rechazos falsos?);
B) citas recortadas y cortadas (¿aceptaciones indebidas?); C) lo que ahora acredita una cita que solo TOCA la cifra.
Uso: python3 -I -B n2_cita_en_linea.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dos_codigos import VE, VC

OKS = ("ok",)


def fila(nombre, pag, cita, vf, espera):
    en_pag = VE._norm_txt(cita) in VE._norm_txt(pag)
    e2 = VE._cita_cifra(cita, vf, pag)
    e1 = VC._cita_cifra(cita, vf, pag)
    real = "ok" if e2[0] in OKS else "rechazo"
    marca = "" if real == espera else ("   <<< ACEPTA lo que no debería" if real == "ok" else "   <<< rechazo falso")
    if not en_pag:
        marca += "   (la cita no está en la página: discrepancia antes de llegar aquí)"
    print(f"   {nombre}\n      cita={cita!r} vf={vf!r}\n      candidata: {e1[0]:20} estable: {e2[0]} ({e2[1][:90]}){marca}")
    return real == espera


n_mal = 0
print("== A · citas legítimas (se espera «ok»)")
P1 = ("Consolidated statement of cash flows\n"
      "(In millions of euros)                                         Notes        2025        2024\n"
      "Lease liability payments (including interest on\n"
      "lease liabilities)                                              6.4       (177.9)     (150.8)\n"
      "Dividends paid                                                              (95.1)         -\n"
      "Net increase (decrease) in cash                                              12.3      (45.6)\n"
      "Acquisition of intangible assets                                   -          13       2.245\n"
      "Free cash flow                                          FY 2023-2024       849,697.000\n")
A = [("A1 cita de dos líneas (rótulo partido) y la cifra de la primera columna", P1, "Lease liability payments (including interest on lease liabilities) 6.4 (177.9)", -177.9),
     ("A2 la misma, la cifra de la segunda columna", P1, "lease liabilities) 6.4 (177.9) (150.8)", -150.8),
     ("A3 cita que solo es la cifra con sus paréntesis", P1, "(150.8)", -150.8),
     ("A4 cita recortada a la cifra, valor_fuente NEGATIVO (lo que publica la página)", P1, "150.8", -150.8),
     ("A5 positivo junto a un negativo de la misma línea", P1, "Net increase (decrease) in cash 12.3", 12.3),
     ("A6 cero impreso como guion al final de la línea", P1, "Dividends paid (95.1) -", 0),
     ("A7 cifra tras un guion de otra columna (2+ espacios): positiva", P1, "Acquisition of intangible assets - 13", 13),
     ("A8 cifra tras un intervalo de años en la misma línea", P1, "Free cash flow FY 2023-2024 849,697.000", 849697),
     ("A9 año final de un intervalo", P1, "FY 2023-2024", 2024),
     ("A10 cita de tres líneas que empieza a mitad de una y acaba a mitad de otra", P1, "interest on lease liabilities) 6.4 (177.9) (150.8) Dividends paid (95.1)", -95.1),
     ("A11 la cifra con miles separados por espacio, la cita la contiene entera", "Chiffre d'affaires      4 573,7      4 309,1\n", "Chiffre d'affaires 4 573,7", 4573.7),
     ("A12 página con retorno de carro (CRLF)", "Total assets\r\n   (849,697.000)\r\nOtros 1\r\n", "Total assets (849,697.000)", -849697),
     ("A13 página con espacio de no separación entre signo de moneda y cifra", "Importe : (€ 149,5)\n", "Importe : (€ 149,5)", -149.5),
     ("A14 cita con mayúsculas distintas de las de la página", "TOTAL REVENUE     1,234.5\n", "Total revenue 1,234.5", 1234.5),
     ("A15 la cifra pegada a una llamada de nota: «1,234.5(1)»", "Revenue 1,234.5(1)\n", "Revenue 1,234.5(1)", 1234.5),
     ("A16 la misma cita dos veces en la página, las dos con la misma lectura", "Total (130.8)\nResumen\nTotal (130.8)\n", "Total (130.8)", -130.8),
     ("A17 cita al final de la página, sin salto de línea final", "Resultado -849697.000", "Resultado -849697.000", -849697),
     ("A18 porcentaje negativo entre paréntesis", "Variación (3,2 %)\n", "Variación (3,2 %)", -3.2),
     ("A19 negativo con el código de moneda dentro del paréntesis", "Pago (EUR 149,5)\n", "Pago (EUR 149,5)", -149.5),
     ("A20 «$-149.5»", "Amount $-149.5\n", "Amount $-149.5", -149.5),
     ("A21 fecha con guiones", "Cierre a 31-12-2024\n", "a 31-12-2024", 2024),
     ("A22 cero «−» (U+2212) aislado en su columna", "Net gains on site disposals        −                 42.2\n", "Net gains on site disposals − 42.2", 0),
     ("A23 la cifra de esa línea (42,2) tras el «−» de otra columna", "Net gains on site disposals        −                 42.2\n", "Net gains on site disposals − 42.2", 42.2)]
for a in A:
    n_mal += not fila(*a, "ok")

print("\n== B · citas recortadas o cortadas, o con otro signo en la página (se espera rechazo)")
B = [("B1 recortada a la cifra; la página la publica entre paréntesis", P1, "150.8", 150.8),
     ("B2 recortada tras «(»", P1, "177.9) (150.8)", 177.9),
     ("B3 cita cortada dentro de la cifra (la página publica 849,697.000)", P1, "FY 2023-2024 849,697", 849697),
     ("B4 cita que empieza dentro de la cifra", P1, "9,697.000", 9697),
     ("B5 cero «acreditado» con el 0 de 2024", P1, "2024", 0),
     ("B6 cero con el 0 de «2.245» cortado", P1, "13 2", 2),
     ("B7 la cita es un guion que en la página es el menos de la cifra siguiente (cero)", "Dividendos -12,5\n", "Dividendos -", 0),
     ("B8 cita en dos líneas: la segunda línea de la página empieza por «(» fuera de la cita… imposible; control: paréntesis en la línea anterior", "Pagos (\n130,8)\n", "130,8", 130.8),
     ("B9 dos apariciones con lecturas distintas", "Total 849697.000\nTotal -849697.000\n", "849697.000", 849697),
     ("B10 dos apariciones solapadas de la cita: «5 -5» en «5 -5 -5»", "5 -5 -5\n", "5 -5", 5),
     ("B11 menos al final de la línea anterior y cifra al principio de la siguiente, cita de dos líneas", "Resultado -\n849697.000\n", "Resultado - 849697.000", 849697),
     ("B12 negativo publicado como «849697.000-» (menos detrás), cita recortada", "Saldo 849697.000-\n", "849697.000", 849697),
     ("B13 negativo «(849697.000)» con la cita «849697.000)» y valor_fuente positivo", "Saldo (849697.000)\n", "849697.000)", 849697),
     ("B14 «CR»/«DR» contable no se interpreta; control de que el signo «-» pegado manda", "Saldo -849697.000 CR\n", "849697.000 CR", 849697)]
for b in B:
    n_mal += not fila(*b, "rechazo")

print("\n== C · la cita solo TOCA la cifra de la página (no la contiene): ¿qué se acredita?")
C = [("C1 la cita es «697.000» y el valor 849697 (página «849 697.000»)", "Total 849 697.000\n", "697.000", 849697, "rechazo"),
     ("C2 la cita es «0» y el valor 849697.000 (la página solo tiene esa cifra)", "Total 849697.000\n", "0", 849697, "rechazo"),
     ("C3 la cita es «Total 8» y el valor 849697", "Total 849697.000\n", "Total 8", 849697, "rechazo"),
     ("C4 la cita es «(» + nada: «Total (» y el valor −130,8", "Total (130.8)\n", "Total (1", -130.8, "rechazo"),
     ("C5 control: la cita contiene la cifra entera", "Total 849697.000\n", "Total 849697.000", 849697, "ok")]
for c in C:
    n_mal += not fila(*c)
print(f"\n{n_mal} casos distintos de lo esperado por el revisor")
