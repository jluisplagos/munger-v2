#!/usr/bin/env python3
"""Auditoría interna 4.9: intentos de engañar las comprobaciones de n4_investigacion.py con estados SINTÉTICOS (identificados como
tales). Se replican exactamente las expresiones de clasificación de main() (líneas 334, 362, 420 y 439 de n4_investigacion.py).
Un caso «ACEPTADO» que debía rechazarse es un falso positivo de la comprobación. Solo lectura; no escribe en la copia auditada."""
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/claude/auditoria_4_9/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/scripts")
import n4_investigacion as N  # noqa: E402

R = []


def clase_intereses(texto):
    c = N.ch_financiacion(2025, {7: texto}, 7)
    ok = N.cuadre_actual(c["cuadre_financiacion"]) and not c["lineas_intereses_en_financiacion"] and bool(c["intereses_pagados_en_explotacion"])
    return 2 if ok else 3, c


def clase_adq(texto):
    c = N.ch_inversion(2020, {13: texto}, 13)
    cu = c["cuadre_inversion"]
    adq_actual = [l for l in c["linea_adquisiciones_un_importe"] if l["columna"] == "actual"] + c["linea_adquisiciones_dos_importes"]
    return (2 if (cu.get("ok") and not adq_actual) else 3), c


def clase_otros(texto):
    c = N.ch_activo_corriente(2020, {2: texto}, 2)
    cu = c["cuadre_activo_corriente"]
    return (2 if (cu.get("ok") and not c["lineas_inversiones_financieras_corrientes"]) else 3), c


def caso(nombre, clase, debia):
    acepta = clase == 2
    R.append((nombre, acepta, debia))
    print(("FALSO POSITIVO" if acepta and not debia else ("ok (rechaza)" if not acepta and not debia else ("ok (acepta)" if acepta else "rechazo inesperado"))), "·", nombre, "· clase", clase)


EXP = """(sintético)
Cash flows from operating activities
Profit for the year  100  90
Interest paid  (5)  (4)
Net cash from operating activities  150  140
"""
FIN = """Cash flows from financing activities
Proceeds from loans and borrowings  20  10
Payments of loans and borrowings  (30)  (12)
Dividends paid  (10)  (9)
Net cash from/(used in) financing activities  (20)  (11)
"""

# 1. intereses pagados dentro de financiación con otro rótulo («Finance costs paid» / «Gastos financieros pagados»)
caso("intereses en financiación rotulados «Finance costs paid»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Finance costs paid  (3)  (2)\nDividends paid  (7)  (7)"))[0], False)
caso("intereses en financiación rotulados «Gastos financieros pagados»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Gastos financieros pagados  (3)  (2)\nDividends paid  (7)  (7)"))[0], False)
# 2. «Interest paid» en explotación con importe 0 en el año, y los intereses del año en financiación bajo otro rótulo
caso("«Interest paid» en explotación a «-» y «Borrowing costs paid» en financiación",
     clase_intereses(EXP.replace("Interest paid  (5)  (4)", "Interest paid  -  (4)") + FIN.replace("Dividends paid  (10)  (9)", "Borrowing costs paid  (3)  (2)\nDividends paid  (7)  (7)"))[0], False)
# 3. errata ilegible en la columna DEL AÑO de una línea que vale 0 en el año: cuadre_actual acepta (ilegibles no vacío)
caso("importe ilegible en la columna del año (línea de intereses camuflada «Other financing payments 0,00»)",
     clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Dividends paid  (10)  (9)\nOther financing payments  0,00  -"))[0], False)

INV = """(sintético)
Cash flows from investing activities
Acquisition of property, plant and equipment  (100)  (90)
{linea}
Net cash used in investing activities  (140)  (90)
"""
# 4. adquisición del año con otro rótulo
for rot in ("Acquisition of businesses, net of cash acquired  (40)  -", "Business combinations, net of cash acquired  (40)  -",
            "Purchase of subsidiaries  (40)  -", "Adquisición de negocios, neta de la caja adquirida  (40)  -", "Combinaciones de negocios  (40)  -"):
    caso(f"adquisición del año con el rótulo «{rot.split('  ')[0]}»", clase_adq(INV.format(linea=rot))[0], False)
caso("control: «Acquisition of a subsidiary» con importe en el año (debe rechazar)", clase_adq(INV.format(linea="Acquisition of a subsidiary, net of the cash acquired  (40)  -"))[0], False)

AC = """(sintético)
Current assets
Inventories  10  100  90
{linea}
Cash and cash equivalents  30  25
  150  130
"""
# 5. activos financieros corrientes con otro rótulo
for rot in ("Short-term investments  20  15", "Current financial assets  20  15", "Marketable securities  20  15", "Imposiciones a corto plazo  20  15",
            "Inversiones a corto plazo  20  15", "Activos financieros corrientes  20  15"):
    caso(f"activo financiero corriente rotulado «{rot.split('  ')[0]}»", clase_otros(AC.format(linea=rot))[0], False)

fp = [n for n, a, d in R if a and not d]
print(f"\n{len(fp)} falsos positivos de {sum(1 for _, _, d in R if not d)} casos que debían rechazarse")
