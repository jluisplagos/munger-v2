"""Especificación de las cifras citadas (frente E · F1 · Elis) → datos/cifras_fuente.csv.

Cada entrada declara documento, página PDF, etiqueta de la línea, posición del token (por la derecha) y el
valor que el autor leyó en la página, CON EL SIGNO IMPRESO (paréntesis = negativo). El script extrae el literal
del PDF original (pdftotext sobre los bytes, huella comprobada) y se detiene si el literal no coincide con el
valor leído: es un doble control de transcripción (lectura del autor frente a extracción automática).
La comprobación reproducible para terceros es verificar_cifras.py sobre el CSV resultante.

Ediciones: cada ejercicio se toma de la publicación MÁS RECIENTE que lo presenta (comparativo reexpresado),
la misma regla que la Historia del libro. Cada fila de tabla declara en «edicion» si su fuente es la vigente para
ese ejercicio según esa regla o una publicación «anterior» (las cifras de la edición original, que se conservan
para comparar ediciones). verificar_cifras.py lo contrasta con el pie de página de cada página citada.

Uso: python3 -I especificacion_cifras.py --raiz <ruta>/munger_v2_r1 --fuentes ../datos/fuentes.json --salida ../datos/cifras_fuente.csv
"""
import argparse
import csv
import json
import sys
from fractions import Fraction
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import verificar_cifras as V  # noqa: E402

MM = "mm EUR"
# (doc, pagina, etiqueta, ocurrencia, [(pos, anio, id, valor_leido_con_signo)], concepto, unidad, perimetro/nota)
T = []


def t(doc, pag, etq, occ, cols, concepto, unidad=MM, nota=""):
    T.append((doc, pag, etq, occ, cols, concepto, unidad, nota))


def dos(doc, pag, etq, idb, a1, v1, a2, v2, concepto, occ=0, unidad=MM, nota=""):
    t(doc, pag, etq, occ, [(-2, a1, f"{idb}_{a1}", v1), (-1, a2, f"{idb}_{a2}", v2)], concepto, unidad, nota)


# ---------------- URD 2025 (2025 y 2024 reexpresado) ----------------
U = "URD2025"
# Cuenta de resultados, PDF p.324
for etq, idb, v25, v24, c in [
    ("Revenue", "IS_VENTAS", "4796.8", "4573.7", "Ventas"),
    ("Amortization of intangible assets recognized in a business combination", "IS_PPA", "-85.7", "-85.0", "Amortización de intangibles reconocidos en combinaciones (PPA)"),
    ("Other operating income and expenses", "IS_OOIE", "-3.1", "-18.5", "Otros ingresos y gastos operativos"),
    ("re:^\\s*Operating income\\s{2,}", "IS_EBIT", "629.9", "596.3", "Resultado operativo (EBIT publicado)"),
    ("Net financial income (expense)", "IS_FIN", "-137.1", "-130.4", "Resultado financiero neto"),
    ("Net income (loss) before tax", "IS_BAI", "492.9", "465.9", "Resultado antes de impuestos"),
    ("Income tax expense", "IS_IMP", "-126.2", "-128.3", "Gasto por impuesto (devengado)"),
    ("re:^\\s*NET INCOME \\(LOSS\\)\\s", "IS_BN", "366.6", "337.7", "Resultado neto"),
]:
    dos(U, 324, etq, idb, 2025, v25, 2024, v24, c)
# Estado de flujos, PDF p.327
for etq, idb, v25, v24, c in [
    ("re:^\\s*NET INCOME \\(LOSS\\)\\s", "CF_BN", "366.6", "337.7", "EFE: resultado neto"),
    ("Income tax expense", "CF_IMP", "126.2", "128.3", "EFE: gasto por impuesto (ajuste)"),
    ("Net financial income (expense)", "CF_FIN", "137.1", "130.4", "EFE: resultado financiero (ajuste)"),
    ("Share-based payments", "CF_SBC", "34.7", "27.1", "EFE: pagos en acciones no monetarios (IFRS 2)"),
    ("Depreciation, amortization and provisions", "CF_DAP", "1020.8", "963.4", "EFE: amortizaciones y provisiones"),
    ("Portion of grants transferred to income", "CF_SUBV", "-1.0", "-0.9", "EFE: subvenciones imputadas"),
    ("and intangible assets", "CF_PLUSV", "-23.1", "7.3", "EFE: resultados por enajenación de inmovilizado"),
    ("Earnout adjustments and other elements with no impact on cash", "CF_EARN", "-0.1", "-9.3", "EFE: ajustes de earnout y otros no monetarios"),
    ("CASH FLOW BEFORE FINANCE COSTS AND TAX", "CF_ANTES", "1661.3", "1584.0", "EFE: caja antes de costes financieros e impuestos"),
    ("Change in inventories", "CF_EXIS", "-5.3", "-14.0", "EFE: variación de existencias"),
    ("Change in trade and other receivables and contract assets", "CF_CLI", "-63.6", "-15.8", "EFE: variación de clientes"),
    ("Change in other assets", "CF_OAC", "-2.4", "-3.5", "EFE: variación de otros activos"),
    ("Change in trade and other payables", "CF_PROV", "11.4", "10.6", "EFE: variación de proveedores"),
    ("Change in contract liabilities and other liabilities", "CF_PCON", "59.9", "21.3", "EFE: variación de pasivos de contrato y otros"),
    ("Other changes", "CF_OTRV", "-1.2", "-3.2", "EFE: otras variaciones"),
    ("Employee benefits", "CF_EMPL", "-2.8", "-2.3", "EFE: prestaciones a empleados"),
    ("Tax paid", "CF_IMPPAG", "-146.7", "-124.9", "EFE: impuestos pagados"),
    ("NET CASH FROM OPERATING ACTIVITIES", "CF_CFO", "1510.6", "1452.1", "EFE: caja de las operaciones (CFO)"),
    ("Acquisition of intangible assets", "CF_CAPINT", "-26.2", "-26.6", "EFE: compras de intangibles"),
    ("Proceeds from disposal of intangible assets", "CF_DESINT", "0.0", "0.0", "EFE: cobros por venta de intangibles"),
    ("Acquisition of property, plant and equipment", "CF_CAPMAT", "-864.0", "-860.8", "EFE: compras de inmovilizado material"),
    ("Proceeds from disposal of property, plant and equipment", "CF_DESMAT", "15.3", "7.3", "EFE: cobros por venta de inmovilizado material"),
    ("Acquisition of subsidiaries, net of cash acquired", "CF_ADQ", "-117.6", "-183.3", "EFE: adquisiciones de filiales netas de caja"),
    ("Investment grants", "CF_SUBVINV", "0.2", "4.1", "EFE: subvenciones de inversión cobradas"),
    ("Capital increase", "CF_AMPL", "14.8", "10.4", "EFE: ampliaciones de capital"),
    ("Treasury shares", "CF_AUTOC", "-153.8", "-2.2", "EFE: acciones propias"),
    ("Dividends paid", "CF_DIV", "-105.1", "-101.3", "EFE: dividendos pagados"),
    ("Proceeds from new borrowings", "CF_EMPR", "2268.1", "1207.8", "EFE: nuevos préstamos"),
    ("Repayments of borrowings", "CF_REEMB", "-2478.7", "-1303.6", "EFE: devolución de préstamos"),
    ("Lease liability payments (including interest on lease liabilities)", "CF_LEASE", "-177.9", "-150.8", "EFE: pagos de arrendamientos (principal + intereses)"),
    ("Net interest paid", "CF_INT", "-99.4", "-78.9", "EFE: intereses financieros netos pagados (sin arrendamientos)"),
    ("Other cash flows related to financing activities", "CF_OFIN", "-12.7", "-4.8", "EFE: otros flujos de financiación"),
]:
    dos(U, 327, etq, idb, 2025, v25, 2024, v24, c)
# Free cash flow y deuda neta, PDF p.314
for etq, idb, v25, v24, c in [
    ("ADJUSTED EBITDA", "FCF_EBITDA", "1700.1", "1609.8", "APM: EBITDA ajustado"),
    ("Cancellation of capital gains/losses on disposals of fixed assets and changes in provisions", "FCF_CANC", "2.4", "2.5", "APM: anulación de plusvalías y provisiones"),
    ("Non-current monetary items included in Other operating income and expenses", "FCF_NOCOR", "-28.2", "-22.2", "APM: partidas monetarias no corrientes en OOIE"),
    ("Expenses related to share-based payments (social contributions)", "FCF_SBCSOC", "-11.2", "-4.3", "APM: cargas sociales de pagos en acciones (caja)"),
    ("Miscellaneous financial items (banking services recognized in operating income)", "FCF_FINDIV", "-1.9", "-1.8", "APM: gastos financieros diversos en resultado operativo"),
    ("Cash flow before finance costs and tax", "FCF_ANTES", "1661.3", "1584.0", "APM: caja antes de costes financieros e impuestos"),
    ("Net capex", "FCF_CAPNET", "-874.7", "-876.0", "APM: capex neto (definición de Elis)"),
    ("Change in working capital requirement", "FCF_BFR", "-4.0", "-6.9", "APM: variación del circulante"),
    ("Net interest paid", "FCF_INT", "-99.4", "-78.9", "APM: intereses netos pagados"),
    ("Tax paid", "FCF_IMP", "-146.7", "-124.9", "APM: impuestos pagados"),
    ("Lease liability payments (including interest on lease liabilities)", "FCF_LEASE", "-177.9", "-150.8", "APM: pagos de arrendamientos"),
    ("FREE CASH FLOW", "FCF_FCF", "358.6", "346.3", "APM: free cash flow publicado"),
    ("Acquisitions of subsidiaries, net of cash acquired", "DN_ADQ", "-117.6", "-183.3", "Deuda neta: adquisiciones"),
    ("Gross debt from acquired companies", "DN_DEUADQ", "-9.1", "-22.4", "Deuda neta: deuda de sociedades adquiridas"),
    ("Other cash flows related to financing activities", "DN_OFIN", "-12.7", "-4.8", "Deuda neta: otros flujos de financiación"),
    ("Dividends paid", "DN_DIV", "-105.1", "-101.3", "Deuda neta: dividendos"),
    ("Capital increase, treasury shares", "DN_CAP", "-139.0", "8.3", "Deuda neta: capital y acciones propias"),
    ("re:^\\s*Other\\s{2,}", "DN_OTROS", "42.7", "-55.5", "Deuda neta: otros (incl. tipo de cambio, OCEANE)"),
    ("Change in net financial debt", "DN_VAR", "17.8", "-12.6", "Variación de la deuda financiera neta (positivo = baja)"),
    ("NET FINANCIAL DEBT", "DN_DN", "3020.2", "3038.0", "Deuda financiera neta (sin NIIF 16)"),
]:
    dos(U, 314, etq, idb, 2025, v25, 2024, v24, c)
# Capex por tipo de activo (caja), PDF p.311
for etq, idb, v25, v24, c in [
    ("Linen purchases", "CAPX_LINO", "-594.2", "-594.3", "Capex: compras de lino"),
    ("Purchases of other items for rental/laundry/maintenance services", "CAPX_OART", "-40.8", "-34.6", "Capex: otros artículos en alquiler-mantenimiento"),
    ("Other acquisitions of property, plant and equipment and intangible assets", "CAPX_OTRO", "-255.2", "-258.6", "Capex: resto de inmovilizado material e intangible"),
    ("Asset disposals", "CAPX_CES", "15.3", "7.3", "Capex: cesiones de activos"),
    ("Investment grants", "CAPX_SUBV", "0.2", "4.1", "Capex: subvenciones de inversión"),
    ("OUTFLOWS/INFLOWS RELATING TO PROPERTY, PLANT AND EQUIPMENT AND INTANGIBLE ASSETS", "CAPX_NETO", "-874.7", "-876.0", "Capex neto (salidas/entradas de inmovilizado)"),
]:
    dos(U, 311, etq, idb, 2025, v25, 2024, v24, c)
t(U, 307, "re:^\\s*TOTAL\\s{2,}", 0, [(-4, 2025, "CREC_ORG_2025", "3.8"), (-3, 2025, "CREC_EXT_2025", "1.8"), (-2, 2025, "CREC_FX_2025", "-0.7"), (-1, 2025, "CREC_PUB_2025", "4.9")], "Crecimiento de ventas: orgánico / externo / divisa / publicado", "%")
# Conciliación con el EBIT ajustado, PDF p.345
for etq, idb, v25, v24, c in [
    ("re:^\\s*ADJUSTED EBIT\\s{2,}[0-9.]+\\s{2,}[0-9.]+\\s*$", "EBITA_ADJ", "766.6", "732.9", "EBIT ajustado (APM)"),
    ("Expenses related to share-based payments", "EBITA_SBC", "-45.9", "-31.4", "Gasto IFRS 2 total (incl. cargas sociales)"),
    ("OPERATING INCOME", "EBITA_EBIT", "629.9", "596.3", "Resultado operativo (conciliación)"),
]:
    dos(U, 345, etq, idb, 2025, v25, 2024, v24, c)
# D&A por componentes (nota 4.5) y OOIE (nota 4.6), PDF p.350
for etq, idb, v25, v24, c in [
    ("in EBIT:", "DA_EBIT", "-933.5", "-876.8", "D&A incluida en el EBIT ajustado"),
    ("Textile rental & maintenance items", "DA_TEXT", "-565.1", "-537.6", "D&A: lino y textil propio en alquiler-mantenimiento"),
    ("Other rental & maintenance items", "DA_OART", "-36.3", "-35.3", "D&A: otros artículos propios en alquiler-mantenimiento"),
    ("Other property, plant and equipment and intangible assets", "DA_OTRO", "-183.6", "-172.5", "D&A: resto de inmovilizado material e intangible"),
    ("Right-of-use assets", "DA_ROU", "-149.5", "-132.2", "D&A: derechos de uso NIIF 16"),
    ("Portion of grants transferred to income", "DA_SUBV", "1.0", "0.9", "D&A: subvenciones imputadas"),
    ("Impairment losses recognized in Other operating income and expenses", "DA_DETER", "-0.1", "-3.3", "D&A: deterioros en OOIE"),
    ("Amortization of intangible assets recognized in a business combination", "DA_PPA", "-85.7", "-85.0", "D&A: intangibles de combinaciones (PPA)"),
    ("TO INCOME)", "DA_TOTAL", "-1019.4", "-965.1", "D&A total neta de subvenciones"),
    ("Additions to or reversals of provisions included in EBIT", "PROV_EBIT", "0.1", "3.3", "Provisiones en el EBIT"),
    ("TOTAL ADDITIONS TO OR REVERSALS OF PROVISIONS", "PROV_TOT", "-0.4", "2.6", "Provisiones: total dotaciones netas"),
    ("Earnout adjustments", "OOIE_EARN", "-0.2", "8.7", "OOIE: ajustes de earnout"),
    ("Net gain (loss) related to retirement of fixed assets", "OOIE_PLUSV", "25.7", "-1.5", "OOIE: resultado por bajas de inmovilizado"),
    ("OTHER OPERATING INCOME AND EXPENSES", "OOIE_TOT", "-3.1", "-18.5", "OOIE: total"),
    ("of which monetary items", "OOIE_MON", "-28.2", "-22.2", "OOIE: de los que monetarios"),
]:
    dos(U, 350, etq, idb, 2025, v25, 2024, v24, c)
# Arrendamientos (nota 6.3), PDF p.366: bloque 2024 (ocurrencia 1) y 2025 (ocurrencia 2); columnas ROU total y pasivo
for etq, idb, vals in [
    ("Increase related to business combinations", "LS_COMB", [("9.0", "9.6"), ("11.7", "12.8")]),
    ("New rights of use", "LS_NUEVO", [("145.7", "145.7"), ("183.9", "184.0")]),
    ("Remeasuring of rights of use", "LS_REEST", [("39.6", "39.7"), ("50.0", "50.0")]),
    ("Amortization", "LS_AMORT", [("-132.2", "0.0"), ("-149.5", "0.0")]),
    ("Impairment recognized", "LS_DETER", [("-0.4", "0.0"), ("-0.1", "0.0")]),
    ("Principal payments", "LS_PRINC", [("0.0", "-125.0"), ("0.0", "-148.3")]),
    ("Translation differences", "LS_FX", [("-5.5", "-6.3"), ("-1.8", "-1.8")]),
    ("Other movements/item-to-item transfers", "LS_OTROS", [("3.0", "4.2"), ("-1.2", "0.3")]),
]:
    for occ, (anio, (vrou, vpas)) in enumerate(zip((2024, 2025), vals), start=1):
        t(U, 366, etq, occ, [(-2, anio, f"{idb}_ROU_{anio}", vrou), (-1, anio, f"{idb}_PAS_{anio}", vpas)], f"Arrendamientos: {etq} (activo ROU / pasivo)")
t(U, 366, "AS AT JANUARY 1, 2024", 0, [(-2, 2023, "LS_SALDO_ROU_2023", "513.7"), (-1, 2023, "LS_SALDO_PAS_2023", "538.3")], "Arrendamientos: saldo inicial 2024 (ROU / pasivo)")
t(U, 366, "AS AT 12/31/2024", 0, [(-2, 2024, "LS_SALDO_ROU_2024", "572.8"), (-1, 2024, "LS_SALDO_PAS_2024", "606.2")], "Arrendamientos: saldo 31-dic-2024 (ROU / pasivo)")
t(U, 366, "AS AT 12/31/2025", 0, [(-2, 2025, "LS_SALDO_ROU_2025", "665.8"), (-1, 2025, "LS_SALDO_PAS_2025", "703.2")], "Arrendamientos: saldo 31-dic-2025 (ROU / pasivo)")
# Inmovilizado material (nota 6.4), PDF p.367: artículos en alquiler-mantenimiento (lino y equipos propios)
t(U, 367, "re:^\\s*Investments\\s", 1, [(-2, 2024, "PPE_INV_RM_2024", "628.8"), (-1, 2024, "PPE_INV_TOT_2024", "852.4")], "PP&E: inversiones (devengo) en artículos de alquiler-mantenimiento / total")
t(U, 367, "re:^\\s*Investments\\s", 2, [(-2, 2025, "PPE_INV_RM_2025", "635.0"), (-1, 2025, "PPE_INV_TOT_2025", "887.1")], "PP&E: inversiones (devengo) en artículos de alquiler-mantenimiento / total")
t(U, 367, "re:^\\s*Amortization\\s{2,}\\(", 1, [(-2, 2024, "PPE_AM_RM_2024", "-573.1"), (-1, 2024, "PPE_AM_TOT_2024", "-722.7")], "PP&E: amortización de artículos de alquiler-mantenimiento / total")
t(U, 367, "re:^\\s*Amortization\\s{2,}\\(", 2, [(-2, 2025, "PPE_AM_RM_2025", "-601.6"), (-1, 2025, "PPE_AM_TOT_2025", "-761.3")], "PP&E: amortización de artículos de alquiler-mantenimiento / total")
# Resultado financiero (nota 8.2), PDF p.379
for etq, idb, v25, v24, c in [
    ("at amortized cost", "FIN_INTDEU", "-122.4", "-124.1", "Gasto por intereses de deuda a coste amortizado"),
    ("Interest expense on lease liabilities", "FIN_INTLS", "-29.2", "-25.8", "Gasto por intereses de arrendamientos (devengo)"),
    ("Interest income using the effective interest rate method", "FIN_INGR", "17.5", "25.5", "Ingresos por intereses"),
    ("TOTAL NET INTEREST EXPENSE", "FIN_INTNET", "-134.1", "-124.3", "Gasto neto total por intereses"),
    ("Accretion expenses", "FIN_ACTUAL", "-3.8", "-8.8", "Gastos de actualización"),
    ("NET FINANCIAL INCOME (EXPENSE)", "FIN_TOT", "-137.1", "-130.4", "Resultado financiero neto"),
]:
    dos(U, 379, etq, idb, 2025, v25, 2024, v24, c)
# Deuda financiera neta (nota 8.5), PDF p.384
for etq, idb, v25, v24, c in [
    ("CONVERTIBLE BONDS", "DEU_OCEANE", "362.0", "352.3", "Deuda: OCEANE (componente de deuda)"),
    ("BORROWINGS AND FINANCIAL DEBT", "DEU_BRUTA", "3418.3", "3660.1", "Deuda financiera bruta (sin arrendamientos)"),
    ("CASH AND CASH EQUIVALENTS (ASSETS)", "DEU_CAJA", "398.1", "622.0", "Caja y equivalentes"),
    ("re:^\\s*NET DEBT\\s", "DEU_NETA", "3020.2", "3038.0", "Deuda financiera neta"),
]:
    dos(U, 384, etq, idb, 2025, v25, 2024, v24, c)
# Impuestos (nota 9), PDF p.392
for etq, idb, v25, v24, c in [
    ("Current taxes", "TAX_CORR", "147.2", "127.7", "Impuesto corriente"),
    ("re:^\\s*Deferred taxes\\s{2,}", "TAX_DIF", "-21.0", "0.6", "Impuesto diferido"),
    ("INCOME (LOSS) BEFORE TAX", "TAX_BAI", "492.9", "465.9", "Resultado antes de impuestos (nota 9)"),
    ("ACTUAL INCOME TAX EXPENSE", "TAX_REAL", "126.2", "128.3", "Gasto real por impuesto"),
    ("Effect of tax not based on net income", "TAX_CVAE", "3.7", "3.5", "Impuestos no basados en el resultado (CVAE, IRAP)"),
    ("re:Differences in tax rate\\s{2,}", "TAX_DTIPO", "-7.2", "-0.1", "Diferencias de tipo (incl. contribución excepcional francesa 2025)"),
    ("Permanent differences", "TAX_PERM", "5.6", "-12.1", "Diferencias permanentes"),
]:
    dos(U, 392, etq, idb, 2025, v25, 2024, v24, c)
t(U, 392, "Theoretical tax rate", 0, [(-2, 2025, "TAX_TEOR_2025", "25.83"), (-1, 2024, "TAX_TEOR_2024", "25.83")], "Tipo teórico de la matriz", "%")
# Intangibles (nota 6.2), PDF p.364: columnas marcas / relaciones con clientes / otros / total
t(U, 364, "Acquisitions through business combinations", 1, [(-3, 2024, "INT_RC_COMB_2024", "32.3")], "Relaciones con clientes: altas por combinaciones (2024 reexpresado)")
t(U, 364, "Acquisitions through business combinations", 2, [(-3, 2025, "INT_RC_COMB_2025", "3.7")], "Relaciones con clientes: altas por combinaciones")
t(U, 364, "re:^\\s*Amortization\\s", 1, [(-4, 2024, "INT_MARCA_AM_2024", "-1.1"), (-3, 2024, "INT_RC_AM_2024", "-83.9")], "Amortización de marcas / relaciones con clientes")
t(U, 364, "re:^\\s*Amortization\\s", 2, [(-4, 2025, "INT_MARCA_AM_2025", "-2.2"), (-3, 2025, "INT_RC_AM_2025", "-83.5")], "Amortización de marcas / relaciones con clientes")
t(U, 364, "NET CARRYING AMOUNT AS AT JANUARY 1, 2024", 0, [(-3, 2023, "INT_RC_VNC_2023", "414.9")], "Relaciones con clientes: valor neto a 1-ene-2024")
t(U, 364, "NET CARRYING AMOUNT AS AT DECEMBER 31, 2024", 0, [(-3, 2024, "INT_RC_VNC_2024", "351.6")], "Relaciones con clientes: valor neto a 31-dic-2024 (reexpresado)")
t(U, 364, "NET CARRYING AMOUNT AS AT DECEMBER 31, 2025", 0, [(-3, 2025, "INT_RC_VNC_2025", "275.1")], "Relaciones con clientes: valor neto a 31-dic-2025")
t(U, 364, "Gross value", 3, [(-3, 2025, "INT_RC_BRUTO_2025", "1444.5")], "Relaciones con clientes: valor bruto a 31-dic-2025")
t(U, 364, "Accumulated amortization and impairment of assets", 3, [(-3, 2025, "INT_RC_AMAC_2025", "-1169.4")], "Relaciones con clientes: amortización acumulada a 31-dic-2025")

# ---------------- DEU 2024 (2024 y 2023 reexpresado), francés ----------------
D = "DEU2024FR"
for etq, idb, v24, v23, c in [
    ("Produits de l'activité ordinaire", "IS_VENTAS", "4573.7", "4309.4", "Ventas"),
    ("Résultat opérationnel", "IS_EBIT", "596.4", "496.8", "Resultado operativo"),
    ("Résultat financier net", "IS_FIN", "-130.4", "-124.6", "Resultado financiero neto"),
    ("Résultat avant impôt", "IS_BAI", "466.0", "372.2", "Resultado antes de impuestos"),
    ("Charge d'impôt", "IS_IMP", "-128.3", "-110.3", "Gasto por impuesto"),
    ("re:^\\s*d'entreprises\\s{2,}", "IS_PPA", "-84.9", "-85.7", "Amortización de intangibles reconocidos en combinaciones (PPA)"),
    ("re:^\\s*RÉSULTAT NET\\s{2,}", "IS_BN", "337.8", "261.9", "Resultado neto"),
]:
    dos(D, 270, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, v24, v23, c in [
    ("re:^\\s*RÉSULTAT NET\\s{2,}", "CF_BN", "337.8", "261.9", "EFE: resultado neto"),
    ("Charge d'impôt", "CF_IMP", "128.3", "110.3", "EFE: gasto por impuesto"),
    ("Résultat financier net", "CF_FIN", "130.4", "124.6", "EFE: resultado financiero"),
    ("Paiements en actions", "CF_SBC", "27.1", "22.9", "EFE: pagos en acciones no monetarios"),
    ("Dotations nettes aux amortissements et provisions", "CF_DAP", "963.3", "886.0", "EFE: amortizaciones y provisiones"),
    ("Quote-part de subvention virée au compte de résultat", "CF_SUBV", "-0.9", "-0.5", "EFE: subvenciones imputadas"),
    ("Plus et moins-values de cession", "CF_PLUSV", "7.3", "4.3", "EFE: resultados por enajenación"),
    ("re:^\\s*sur la trésorerie\\s{2,}", "CF_EARN", "-9.3", "48.4", "EFE: ajustes de earnout y otros no monetarios"),
    ("re:^\\s*ET IMPÔT\\s", "CF_ANTES", "1584.0", "1457.9", "EFE: caja antes de costes financieros e impuestos"),
    ("Variation des stocks", "CF_EXIS", "-14.0", "12.3", "EFE: existencias"),
    ("Variation des clients, autres débiteurs et actifs sur contrats", "CF_CLI", "-15.8", "-66.6", "EFE: clientes"),
    ("Variation des autres actifs", "CF_OAC", "-3.5", "-1.4", "EFE: otros activos"),
    ("Variation des comptes fournisseurs et autres créditeurs", "CF_PROV", "10.6", "1.7", "EFE: proveedores"),
    ("Variation des passifs sur contrats et autres passifs", "CF_PCON", "21.3", "52.5", "EFE: pasivos de contrato y otros"),
    ("Variation des autres postes", "CF_OTRV", "-3.2", "-0.9", "EFE: otras variaciones"),
    ("Avantages du personnel", "CF_EMPL", "-2.3", "-3.5", "EFE: prestaciones a empleados"),
    ("Impôts versés", "CF_IMPPAG", "-124.9", "-126.4", "EFE: impuestos pagados"),
    ("PAR L'ACTIVITÉ", "CF_CFO", "1452.1", "1325.6", "EFE: CFO"),
    ("Décaissements liés aux acquisitions d'immobilisations incorporelles", "CF_CAPINT", "-26.6", "-26.8", "EFE: compras de intangibles"),
    ("Encaissements liés aux cessions d'immobilisations incorporelles", "CF_DESINT", "0.0", "0.1", "EFE: cobros por venta de intangibles"),
    ("Décaissements liés aux acquisitions d'immobilisations corporelles", "CF_CAPMAT", "-860.8", "-797.1", "EFE: compras de inmovilizado material"),
    ("Encaissements liés aux cessions d'immobilisations corporelles", "CF_DESMAT", "7.3", "2.8", "EFE: cobros por venta de inmovilizado material"),
    ("Acquisition de filiales, sous déduction de la trésorerie acquise", "CF_ADQ", "-183.3", "-82.1", "EFE: adquisiciones de filiales"),
    ("Subventions d'investissement", "CF_SUBVINV", "4.1", "0.3", "EFE: subvenciones de inversión"),
    ("Augmentation de capital", "CF_AMPL", "10.4", "7.9", "EFE: ampliaciones de capital"),
    ("Actions propres", "CF_AUTOC", "-2.2", "1.2", "EFE: acciones propias"),
    ("Dividendes et distributions mis en paiement", "CF_DIV", "-101.3", "-61.7", "EFE: dividendos"),
    ("Encaissements liés aux nouveaux emprunts", "CF_EMPR", "1207.8", "1194.8", "EFE: nuevos préstamos"),
    ("Remboursements d'emprunts", "CF_REEMB", "-1303.6", "-985.9", "EFE: devolución de préstamos"),
    ("Paiements de passifs locatifs (y compris intérêts sur passifs locatifs)", "CF_LEASE", "-150.8", "-130.8", "EFE: pagos de arrendamientos"),
    ("Intérêts financiers nets versés", "CF_INT", "-78.9", "-70.5", "EFE: intereses financieros netos pagados"),
    ("Autres flux liés aux opérations de financement", "CF_OFIN", "-4.8", "-1.4", "EFE: otros flujos de financiación"),
]:
    dos(D, 273, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, v24, v23, c in [
    ("EBITDA AJUSTÉ", "FCF_EBITDA", "1609.8", "1474.8", "APM: EBITDA ajustado"),
    ("Annulation des (plus) ou moins-values", "FCF_CANC", "2.5", "9.8", "APM: anulación de plusvalías y provisiones"),
    ("Éléments exceptionnels monétaires", "FCF_NOCOR", "-22.2", "-16.9", "APM: partidas monetarias excepcionales"),
    ("Charges sur paiements en actions (contributions sociales)", "FCF_SBCSOC", "-4.3", "-8.2", "APM: cargas sociales de pagos en acciones"),
    ("Frais financiers divers", "FCF_FINDIV", "-1.8", "-1.6", "APM: gastos financieros diversos"),
    ("Capacité d'autofinancement avant coût", "FCF_ANTES", "1584.0", "1457.9", "APM: caja antes de costes financieros e impuestos"),
    ("Investissements nets", "FCF_CAPNET", "-876.0", "-820.8", "APM: capex neto"),
    ("Variation du besoin en fonds de roulement", "FCF_BFR", "-6.9", "-5.9", "APM: circulante"),
    ("Intérêts financiers nets versés", "FCF_INT", "-78.9", "-70.5", "APM: intereses netos pagados"),
    ("Impôts versés", "FCF_IMP", "-124.9", "-126.4", "APM: impuestos pagados"),
    ("Paiements de passifs locatifs", "FCF_LEASE", "-150.8", "-130.8", "APM: pagos de arrendamientos"),
    ("FREE CASH FLOW", "FCF_FCF", "346.4", "303.6", "APM: free cash flow publicado"),
    ("Charges sur paiements en actions (IFRS 2)", "EBITA_SBC", "31.4", "31.1", "Gasto IFRS 2 total (tabla de resultado neto corriente)"),
]:
    dos(D, 259, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, v24, v23, c in [
    ("Achats de linge", "CAPX_LINO", "-594.3", "-584.3", "Capex: compras de lino"),
    ("Achats d'autres articles en location-entretien", "CAPX_OART", "-34.6", "-37.3", "Capex: otros artículos en alquiler-mantenimiento"),
    ("Autres acquisitions d'immobilisations corporelles et incorporelles", "CAPX_OTRO", "-258.6", "-202.3", "Capex: resto de inmovilizado"),
    ("Cessions d'actifs", "CAPX_CES", "7.3", "2.9", "Capex: cesiones de activos"),
    ("Subventions d'investissement", "CAPX_SUBV", "4.1", "0.3", "Capex: subvenciones de inversión"),
    ("DÉCAISSEMENTS/ENCAISSEMENTS LIÉS AUX IMMOBILISATIONS", "CAPX_NETO", "-876.0", "-820.8", "Capex neto"),
]:
    dos(D, 257, etq, idb + "_FR", 2024, v24, 2023, v23, c)
t(D, 253, "re:^\\s*TOTAL\\s{2,}", 0, [(-4, 2024, "CREC_ORG_2024", "5.2"), (-3, 2024, "CREC_EXT_2024", "1.2"), (-2, 2024, "CREC_FX_2024", "-0.3"), (-1, 2024, "CREC_PUB_2024", "6.1")], "Crecimiento de ventas: orgánico / externo / divisa / publicado", "%")
dos(D, 296, "incluses dans l'EBIT", "DA_EBIT_FR", 2024, "-876.8", 2023, "-791.7", "D&A incluida en el EBIT ajustado", occ=1)
for etq, idb, v24, v23, c in [
    ("Articles textiles en location-entretien", "DA_TEXT", "-537.6", "-482.1", "D&A: lino propio"),
    ("Autres articles en location-entretien", "DA_OART", "-35.3", "-32.7", "D&A: otros artículos propios en alquiler"),
    ("Autres immobilisations incorporelles et corporelles", "DA_OTRO", "-172.5", "-161.6", "D&A: resto de inmovilizado"),
    ("Actifs comptabilisés au titre du droit d'utilisation", "DA_ROU", "-132.2", "-115.8", "D&A: derechos de uso NIIF 16"),
    ("Quote-part de subvention virée au compte de résultat", "DA_SUBV", "0.9", "0.5", "D&A: subvenciones imputadas"),
    ("Pertes de valeur comptabilisées en autres produits et charges opérationnels", "DA_DETER", "-3.3", "-0.0", "D&A: deterioros en OOIE"),
    ("Dotations aux amortissements des incorporels reconnus dans un regroupement d'entreprises", "DA_PPA", "-84.9", "-85.7", "D&A: PPA"),
    ("AU COMPTE DE RÉSULTAT)", "DA_TOTAL", "-965.0", "-877.4", "D&A total neta de subvenciones"),
    ("TOTAL DES DOTATIONS OU REPRISES DE PROVISIONS", "PROV_TOT", "2.6", "-8.1", "Provisiones: total"),
    ("Ajustements de compléments de prix", "OOIE_EARN", "8.7", "-48.9", "OOIE: ajustes de earnout"),
    ("Plus ou moins-values liées aux sorties d'immobilisations", "OOIE_PLUSV", "-1.5", "-1.2", "OOIE: bajas de inmovilizado"),
    ("AUTRES PRODUITS ET CHARGES OPÉRATIONNELS", "OOIE_TOT", "-18.5", "-67.9", "OOIE: total"),
    ("dont éléments monétaires", "OOIE_MON", "-22.2", "-16.9", "OOIE: monetarios"),
]:
    dos(D, 296, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, (vr, vp) in [
    ("d'entreprises", "LS_COMB", ("1.5", "1.5")),
    ("Nouveaux droits d'utilisation", "LS_NUEVO", ("132.6", "132.6")),
    ("Réévaluation des droits d'utilisation", "LS_REEST", ("24.9", "24.9")),
    ("Amortissements de l'exercice", "LS_AMORT", ("-115.9", "0.0")),
    ("Paiements du principal", "LS_PRINC", ("0.0", "-111.0")),
]:
    t(D, 312, etq, 1, [(-2, 2023, f"{idb}_ROU_2023", vr), (-1, 2023, f"{idb}_PAS_2023", vp)], f"Arrendamientos 2023 (DEU 2024): {etq}")
t(D, 312, "AU 1ER JANVIER 2023", 0, [(-2, 2022, "LS_SALDO_ROU_2022", "466.9"), (-1, 2022, "LS_SALDO_PAS_2022", "485.4")], "Arrendamientos: saldo a 1-ene-2023")
t(D, 312, "AU 31 DÉCEMBRE 2023", 0, [(-2, 2023, "LS_SALDO_ROU_2023_FR", "513.7"), (-1, 2023, "LS_SALDO_PAS_2023_FR", "538.3")], "Arrendamientos: saldo a 31-dic-2023")
for etq, idb, v24, v23, c in [
    ("Charge d'intérêts sur passifs locatifs", "FIN_INTLS", "-25.8", "-19.8", "Gasto por intereses de arrendamientos (devengo)"),
    ("Charge d'intérêts sur emprunts", "FIN_INTDEU", "-124.1", "-109.3", "Intereses de deuda a coste amortizado"),
    ("Produits d'intérêts selon la méthode", "FIN_INGR", "25.5", "18.0", "Ingresos por intereses"),
    ("Charges de désactualisation", "FIN_ACTUAL", "-8.8", "-13.8", "Gastos de actualización"),
    ("RÉSULTAT FINANCIER NET", "FIN_TOT", "-130.4", "-124.6", "Resultado financiero neto"),
]:
    dos(D, 324, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, v24, v23, c in [
    ("OBLIGATIONS CONVERTIBLES", "DEU_OCEANE", "352.3", "343.1", "Deuda: OCEANE"),
    ("EMPRUNTS ET DETTES FINANCIÈRES", "DEU_BRUTA", "3660.1", "3690.7", "Deuda financiera bruta"),
    ("TRÉSORERIE ET ÉQUIVALENTS DE TRÉSORERIE (ACTIFS)", "DEU_CAJA", "622.1", "665.3", "Caja"),
    ("SOLDE ENDETTEMENT NET", "DEU_NETA", "3038.0", "3025.4", "Deuda financiera neta"),
]:
    dos(D, 329, etq, idb + "_FR", 2024, v24, 2023, v23, c)
for etq, idb, v24, v23, c in [
    ("Impôt courant des activités poursuivies", "TAX_CORR", "127.7", "120.3", "Impuesto corriente"),
    ("Impôt différé des activités poursuivies", "TAX_DIF", "0.6", "-10.1", "Impuesto diferido"),
    ("RÉSULTAT AVANT IMPÔT", "TAX_BAI", "466.0", "372.2", "Resultado antes de impuestos"),
    ("IMPÔT RÉEL", "TAX_REAL", "128.3", "110.3", "Gasto real por impuesto"),
    ("Incidence d'impôts dont la base diffère", "TAX_CVAE", "3.5", "4.6", "CVAE / IRAP"),
    ("compléments de prix non déductibles", "TAX_EARN", "0.8", "-15.8", "Earnout no deducible"),
    ("Différences permanentes", "TAX_PERM", "-12.1", "-12.2", "Diferencias permanentes"),
]:
    dos(D, 337, etq, idb + "_FR", 2024, v24, 2023, v23, c)
t(D, 310, "VALEUR NETTE COMPTABLE AU 1er JANVIER 2023", 0, [(-3, 2022, "INT_RC_VNC_2022", "471.5")], "Relaciones con clientes: valor neto a 1-ene-2023")
t(D, 310, "Acquisitions par voie de regroupements d'entreprises", 1, [(-3, 2023, "INT_RC_COMB_2023", "20.6")], "Relaciones con clientes: altas por combinaciones 2023")
# (O7) altas de 2024 tal como las publicó el DEU 2024 (edición anterior a la reexpresión del URD 2025: 32,3)
t(D, 310, "Acquisitions par voie de regroupements d'entreprises", 2, [(-3, 2024, "INT_RC_COMB_FR_2024", "18.0")],
  "Relaciones con clientes: altas por combinaciones 2024 en el DEU 2024 (edición anterior)")
t(D, 310, "Amortissements de l'exercice", 1, [(-3, 2023, "INT_RC_AM_2023", "-84.6")], "Relaciones con clientes: amortización 2023")
t(D, 310, "VALEUR NETTE COMPTABLE AU 31 DÉCEMBRE 2023", 0, [(-3, 2023, "INT_RC_VNC_2023_FR", "414.9")], "Relaciones con clientes: valor neto a 31-dic-2023")

# ---------------- URD 2023 (2023 original y 2022 reexpresado) ----------------
W = "URD2023"
for etq, idb, v23, v22, c in [
    ("Revenue", "IS_VENTAS", "4309.4", "3820.9", "Ventas"),
    ("Amortization of intangible assets recognized in a business combination", "IS_PPA", "-85.1", "-82.9", "PPA"),
    ("Goodwill impairment", "IS_DETFC", "0.0", "-58.7", "Deterioro de fondo de comercio"),
    ("re:^\\s*Operating income\\s{2,}", "IS_EBIT", "497.5", "369.0", "Resultado operativo"),
    ("Net financial income (expense)", "IS_FIN", "-124.6", "-86.7", "Resultado financiero"),
    ("Income (loss) before tax", "IS_BAI", "372.9", "282.3", "Resultado antes de impuestos"),
    ("re:^\\s*Tax\\s{2,}", "IS_IMP", "-110.4", "-79.7", "Gasto por impuesto"),
]:
    dos(W, 276, etq, idb + "_U23", 2023, v23, 2022, v22, c)
for etq, idb, v23, v22, c in [
    ("NET CASH FROM OPERATING ACTIVITIES", "CF_CFO", "1325.7", "1091.2", "EFE: CFO"),
    ("Share-based payments", "CF_SBC", "22.9", "20.3", "EFE: pagos en acciones"),
    ("Acquisition of intangible assets", "CF_CAPINT", "-26.8", "-26.5", "EFE: compras de intangibles"),
    ("Acquisition of property, plant and equipment", "CF_CAPMAT", "-797.1", "-673.3", "EFE: compras de inmovilizado material"),
    ("Acquisition of subsidiaries, net of cash acquired", "CF_ADQ", "-82.2", "-221.7", "EFE: adquisiciones"),
    ("Lease liability payments - principal", "CF_LSPRINC", "-111.0", "-101.5", "EFE: principal de arrendamientos (presentación 2023)"),
    ("Net interest paid (including interest on lease liabilities)", "CF_INTCONLS", "-90.2", "-72.9", "EFE: intereses netos pagados INCLUIDOS los de arrendamientos (presentación 2023)"),
    ("Tax paid", "CF_IMPPAG", "-126.4", "-100.1", "EFE: impuestos pagados"),
]:
    dos(W, 279, etq, idb + "_U23", 2023, v23, 2022, v22, c)
for etq, idb, v23, v22, c in [
    ("Linen purchases", "CAPX_LINO", "-584.3", "-518.8", "Capex: lino"),
    ("Purchases of other items for rental/laundry/maintenance services", "CAPX_OART", "-37.3", "-37.3", "Capex: otros artículos en alquiler"),
    ("Other acquisitions of property, plant and equipment and intangible assets", "CAPX_OTRO", "-202.3", "-143.7", "Capex: resto"),
    ("Asset disposals", "CAPX_CES", "2.9", "7.4", "Capex: cesiones"),
    ("OUTFLOWS/INFLOWS RELATING TO PROPERTY, PLANT AND EQUIPMENT AND INTANGIBLE ASSETS", "CAPX_NETO", "-820.8", "-691.9", "Capex neto"),
]:
    dos(W, 266, etq, idb + "_U23", 2023, v23, 2022, v22, c)
for etq, idb, v23, v22, c in [
    ("Cash flow before finance costs and tax", "FCF_ANTES", "1457.9", "1243.8", "APM: caja antes de costes financieros e impuestos"),
    ("Net capex", "FCF_CAPNET", "-820.8", "-691.9", "APM: capex neto"),
    ("Change in working capital requirement", "FCF_BFR", "-5.9", "-52.6", "APM: circulante"),
    ("Net interest paid (including interest on lease liabilities)", "FCF_INTCONLS", "-90.2", "-72.9", "APM: intereses incl. arrendamientos"),
    ("Tax paid", "FCF_IMP", "-126.4", "-100.1", "APM: impuestos pagados"),
    ("Lease liability payments", "FCF_LSPRINC", "-111.0", "-101.5", "APM: principal de arrendamientos"),
    ("FREE CASH FLOW (AFTER PAYMENT OF LEASE LIABILITIES)", "FCF_FCF", "303.6", "224.9", "APM: free cash flow"),
]:
    dos(W, 268, etq, idb + "_U23", 2023, v23, 2022, v22, c)
t(W, 261, "re:^\\s*TOTAL\\s{2,}", 0, [(-4, 2023, "CREC_ORG_2023", "11.8"), (-3, 2023, "CREC_EXT_2023", "1.8"), (-2, 2023, "CREC_FX_2023", "-0.8"), (-1, 2023, "CREC_PUB_2023", "12.8")], "Crecimiento de ventas 2023", "%")
for etq, idb, v23, v22, c in [
    ("Textile rental & maintenance items", "DA_TEXT", "-482.1", "-424.0", "D&A: lino propio"),
    ("Other leased items", "DA_OART", "-32.7", "-30.3", "D&A: otros artículos propios en alquiler"),
    ("Other property, plant and equipment and intangible assets", "DA_OTRO", "-161.6", "-158.6", "D&A: resto"),
    ("Right-of-use assets", "DA_ROU", "-115.8", "-103.7", "D&A: ROU"),
    ("Portion of grants transferred to income", "DA_SUBV", "0.5", "0.7", "D&A: subvenciones"),
    ("Depreciation and amortization included in Other operating income and expenses", "DA_DETER", "-0.0", "-0.1", "D&A en OOIE"),
    ("Amortization of intangible assets recognized in a business combination", "DA_PPA", "-85.1", "-82.9", "D&A: PPA"),
    ("TO INCOME)", "DA_TOTAL", "-876.8", "-799.0", "D&A total"),
]:
    dos(W, 301, etq, idb + "_U23", 2023, v23, 2022, v22, c)
for etq, idb, (vr, vp) in [
    ("New rights of use", "LS_NUEVO", ("90.4", "90.4")),
    ("Remeasuring of rights of use", "LS_REEST", ("19.7", "19.7")),
    ("Principal payments", "LS_PRINC", (None, "-101.5")),
]:
    cols = ([(-2, 2022, f"{idb}_ROU_2022", vr)] if vr else []) + [(-1, 2022, f"{idb}_PAS_2022", vp)]
    t(W, 321, etq, 1, cols, f"Arrendamientos 2022 (URD 2023, reexpresado): {etq}")
t(W, 321, "Depreciation & amortization / impairment", 1, [(-1, 2022, "LS_AMORT_ROU_2022", "-103.7")], "Arrendamientos 2022: amortización ROU")
for etq, idb, v23, v22, c in [
    ("Interest expense on lease liabilities", "FIN_INTLS", "-19.8", "-13.1", "Gasto por intereses de arrendamientos (devengo)"),
]:
    dos(W, 332, etq, idb + "_U23", 2023, v23, 2022, v22, c)

# ---------------- URD 2022 (2022 original y 2021 reexpresado) ----------------
X = "URD2022"
for etq, idb, v22, v21, c in [
    ("Revenue", "IS_VENTAS", "3820.9", "3048.3", "Ventas"),
    ("Amortization of intangible assets recognized in a business combination", "IS_PPA", "-80.1", "-81.1", "PPA"),
    ("Goodwill impairment", "IS_DETFC", "-58.7", "0.0", "Deterioro de fondo de comercio"),
    ("re:^\\s*Operating income\\s{2,}", "IS_EBIT", "371.8", "261.5", "Resultado operativo"),
    ("Net financial income (expense)", "IS_FIN", "-86.7", "-90.5", "Resultado financiero"),
    ("Income (loss) before tax", "IS_BAI", "285.1", "171.0", "Resultado antes de impuestos"),
    ("re:^\\s*Tax\\s{2,}", "IS_IMP", "-80.5", "-56.6", "Gasto por impuesto"),
]:
    dos(X, 258, etq, idb + "_U22", 2022, v22, 2021, v21, c)
for etq, idb, v22, v21, c in [
    ("NET CASH FLOWS FROM OPERATING ACTIVITIES", "CF_CFO", "1091.2", "961.6", "EFE: CFO"),
    ("Acquisition of intangible assets", "CF_CAPINT", "-26.5", "-21.1", "EFE: compras de intangibles"),
    ("Acquisition of property, plant and equipment", "CF_CAPMAT", "-673.3", "-552.8", "EFE: compras de inmovilizado material"),
    ("Acquisition of subsidiaries, net of cash acquired", "CF_ADQ", "-221.6", "-86.8", "EFE: adquisiciones"),
    ("Lease liability payments - principal", "CF_LSPRINC", "-101.5", "-89.4", "EFE: principal de arrendamientos"),
    ("Net interest paid (including interest on lease liabilities)", "CF_INTCONLS", "-72.9", "-74.6", "EFE: intereses netos pagados incl. arrendamientos"),
    ("Tax paid", "CF_IMPPAG", "-100.1", "-83.2", "EFE: impuestos pagados"),
]:
    dos(X, 261, etq, idb + "_U22", 2022, v22, 2021, v21, c)
for etq, idb, v22, v21, c in [
    ("Linen purchases", "CAPX_LINO", "-518.8", "-406.7", "Capex: lino"),
    ("Purchases of other items for rental/laundry/maintenance services", "CAPX_OART", "-37.3", "-32.6", "Capex: otros artículos en alquiler"),
    ("Other acquisitions of property, plant and equipment and intangible assets", "CAPX_OTRO", "-143.7", "-134.6", "Capex: resto"),
    ("Asset disposals", "CAPX_CES", "7.4", "3.8", "Capex: cesiones"),
    ("OUTFLOWS/INFLOWS RELATING TO PROPERTY, PLANT AND EQUIPMENT AND INTANGIBLE ASSETS", "CAPX_NETO", "-691.9", "-569.5", "Capex neto"),
]:
    dos(X, 247, etq, idb + "_U22", 2022, v22, 2021, v21, c)
for etq, idb, v22, v21, c in [
    ("Change in working capital requirement", "FCF_BFR", "-52.6", "10.1", "APM: circulante"),
    ("FREE CASH FLOW (AFTER PAYMENT OF LEASE LIABILITIES)", "FCF_FCF", "224.9", "228.1", "APM: free cash flow"),
]:
    dos(X, 250, etq, idb + "_U22", 2022, v22, 2021, v21, c)
t(X, 243, "re:^\\s*TOTAL\\s{2,}", 0, [(-4, 2022, "CREC_ORG_2022", "21.0"), (-3, 2022, "CREC_EXT_2022", "3.1"), (-2, 2022, "CREC_FX_2022", "1.2"), (-1, 2022, "CREC_PUB_2022", "25.3")], "Crecimiento de ventas 2022", "%")
for etq, idb, v22, v21, c, occ in [
    ("Textile rental, laundry and maintenance items", "DA_TEXT", "-424.0", "-386.9", "D&A: lino propio", 0),
    ("Other leased items", "DA_OART", "-30.3", "-28.5", "D&A: otros artículos propios en alquiler", 0),
    ("Other property, plant and equipment and intangible assets", "DA_OTRO", "-158.6", "-156.3", "D&A: resto", 0),
    ("Right-of-use assets", "DA_ROU", "-103.7", "-92.6", "D&A: ROU", 0),
    ("Portion of grants transferred to income", "DA_SUBV", "0.7", "0.6", "D&A: subvenciones", 0),
    ("included in other operating income and expenses", "DA_DETER", "-0.1", "0.0", "D&A en OOIE", 1),
    ("amortization of intangible assets recognized in a business combination", "DA_PPA", "-80.1", "-81.1", "D&A: PPA", 0),
    ("TO INCOME)", "DA_TOTAL", "-796.2", "-744.8", "D&A total", 0),
]:
    dos(X, 284, etq, idb + "_U22", 2022, v22, 2021, v21, c, occ=occ)
for etq, idb, vals in [
    ("Increase related to business combinations", "LS_COMB", [("1.7", "2.0"), ("21.7", "22.8")]),
    ("New rights of use", "LS_NUEVO", [("71.1", "71.1"), ("90.4", "90.4")]),
    ("Remeasuring of rights of use", "LS_REEST", [("20.8", "20.8"), ("19.7", "19.7")]),
]:
    for occ, (anio, (vr, vp)) in enumerate(zip((2021, 2022), vals), start=1):
        sufijo = "" if anio == 2021 else "_U22"
        t(X, 302, etq, occ, [(-2, anio, f"{idb}_ROU_{anio}{sufijo}", vr), (-1, anio, f"{idb}_PAS_{anio}{sufijo}", vp)], f"Arrendamientos (URD 2022): {etq}")
t(X, 302, "Depreciation & amortization / impairment", 1, [(-1, 2021, "LS_AMORT_ROU_2021", "-92.6")], "Arrendamientos 2021: amortización ROU")
t(X, 302, "Principal payments", 1, [(-1, 2021, "LS_PRINC_PAS_2021", "-89.4")], "Arrendamientos 2021: principal pagado")
for etq, idb, v22, v21, c in [
    ("Interest expense on lease liabilities", "FIN_INTLS", "-13.1", "-10.4", "Gasto por intereses de arrendamientos (devengo)"),
]:
    dos(X, 313, etq, idb + "_U22", 2022, v22, 2021, v21, c)

# Circulante y SBC del horizonte S2C (2021 del URD 2022; 2022 del URD 2023 reexpresado)
for etq, idb, v22, v21, c in [
    ("Share-based payments", "CF_SBC", "20.3", "24.4", "EFE: pagos en acciones no monetarios"),
    ("Change in inventories", "CF_EXIS", "-50.0", "1.0", "EFE: existencias"),
    ("Change in trade and other receivables and contract assets", "CF_CLI", "-119.3", "-76.8", "EFE: clientes"),
    ("Change in other assets", "CF_OAC", "0.3", "2.8", "EFE: otros activos"),
    ("Change in trade and other payables", "CF_PROV", "82.2", "35.3", "EFE: proveedores"),
    ("Change in contract liabilities and other liabilities", "CF_PCON", "35.7", "45.5", "EFE: pasivos de contrato y otros"),
    ("Other changes", "CF_OTRV", "-2.2", "0.1", "EFE: otras variaciones"),
    ("Employee benefits", "CF_EMPL", "0.7", "2.3", "EFE: prestaciones a empleados"),
]:
    dos(X, 261, etq, idb + "_U22", 2022, v22, 2021, v21, c)
dos(X, 287, "Equity-settled share-based payments", "SBC_N52_U22", 2022, "-22.3", 2021, "-28.0", "Nota 5.2: pagos en acciones liquidados con instrumentos de patrimonio")
for etq, idb, v23, v22, c in [
    ("Change in inventories", "CF_EXIS", "12.3", "-50.0", "EFE: existencias"),
    ("Change in trade and other receivables and contract assets", "CF_CLI", "-66.6", "-119.3", "EFE: clientes"),
    ("Change in other assets", "CF_OAC", "-1.4", "0.3", "EFE: otros activos"),
    ("Change in trade and other payables", "CF_PROV", "1.7", "82.2", "EFE: proveedores"),
    ("Change in contract liabilities and other liabilities", "CF_PCON", "52.5", "35.7", "EFE: pasivos de contrato y otros"),
    ("Other changes", "CF_OTRV", "-0.9", "-2.2", "EFE: otras variaciones"),
    ("Employee benefits", "CF_EMPL", "-3.5", "0.7", "EFE: prestaciones a empleados"),
]:
    dos(W, 279, etq, idb + "_U23", 2023, v23, 2022, v22, c)
for etq, idb, (vr, vp) in [("Écarts de conversion", "LS_FX", ("5.6", "5.9")), ("Autres mouvements", "LS_OTROS", ("-1.9", "-1.0"))]:
    t(D, 312, etq, 1, [(-2, 2023, f"{idb}_ROU_2023", vr), (-1, 2023, f"{idb}_PAS_2023", vp)], f"Arrendamientos 2023 (DEU 2024): {etq}")

# Impuesto diferido por naturaleza: efecto en resultados (posición −4: inicial, combinaciones, RESULTADO, ORI, divisa, final)
t(U, 393, "re:^\\s*Intangible assets\\s{2,}\\(", 0, [(-4, 2025, "TAXDIF_INT_2025", "17.5")], "Diferido: intangibles (ingreso por reversión del pasivo diferido)")
t(U, 393, "Right-of-use assets", 0, [(-4, 2025, "TAXDIF_ROU_2025", "-17.5")], "Diferido: derechos de uso")
t(U, 393, "Lease liabilities", 0, [(-4, 2025, "TAXDIF_LS_2025", "19.2")], "Diferido: pasivos por arrendamiento")
t(D, 338, "Immobilisations incorporelles", 0, [(-4, 2024, "TAXDIF_INT_2024", "20.3")], "Diferido: intangibles")
t(D, 338, "re:^\\s*d'utilisation\\s{2,}", 0, [(-4, 2024, "TAXDIF_ROU_2024", "-7.2")], "Diferido: derechos de uso")
t(D, 338, "Passifs locatifs", 0, [(-4, 2024, "TAXDIF_LS_2024", "9.5")], "Diferido: pasivos por arrendamiento")
t(W, 346, "re:^\\s*Intangible assets\\s{2,}\\(", 0, [(-4, 2023, "TAXDIF_INT_2023", "15.5")], "Diferido: intangibles (edición original 2023)")
t(W, 346, "Right-of-use assets*", 0, [(-4, 2023, "TAXDIF_ROU_2023", "-17.4")], "Diferido: derechos de uso (edición original 2023)")
t(W, 346, "Lease liabilities*", 0, [(-4, 2023, "TAXDIF_LS_2023", "17.0")], "Diferido: pasivos por arrendamiento (edición original 2023)")

# ---------------- URD 2021 ----------------
Y = "URD2021"
dos(Y, 226, "Revenue", "IS_VENTAS_U21", 2021, "3048.3", 2020, "2806.3", "Ventas (2020 = base de S2C)")
t(Y, 211, "re:^\\s*TOTAL\\s{2,}", 0, [(-2, 2021, "CREC_PUB_2021", "8.6"), (-1, 2021, "CREC_ORG_2021", "7.4")], "Crecimiento de ventas 2021: publicado / orgánico", "%")

t(U, 347, "Flat linen", 0, [(-1, 2025, "VENTAS_LINO_PLANO_2025", "2217.4")], "Ventas de lino plano 2025 (nota 4.2, total de segmentos)",
  nota="Tabla de un solo ejercicio: el título «2025» va encima de la tabla y la p.348 presenta 2024; control manual del ejercicio")
# Ventas en la información por segmentos (columna «Total»): contraste entre páginas de la cifra de la cuenta de resultados
t(U, 347, "re:^\\s*REVENUE\\s{2,}", 0, [(-1, 2025, "VENTAS_SEG_2025", "4796.8")], "Ventas 2025 en la nota 4.2 (total de segmentos)")
t(U, 345, "SEGMENT REVENUE", 0, [(-1, 2024, "VENTAS_SEG_2024", "4573.7")], "Ventas 2024 en la información por segmentos (total)")
t("DEU2024FR", 290, "Clients externes", 2, [(-1, 2023, "VENTAS_SEG_FR_2023", "4309.4")],
  "Ventas 2023 en la información por segmentos del DEU 2024 (clientes externos, total)")

# ---------------- Literales de texto (prosa) ----------------
TXT = [
    ("TXT_CAPEX_AMBOS", 2025, U, 312, "It therefore covers investments for both growth (new plants or to increase capacity) and maintenance (equipment replacement)", "La inversión industrial cubre crecimiento y mantenimiento; no se publica el reparto."),
    ("TXT_LINO_CRECIM", 2025, U, 312, "Growth investments thus make up a large percentage of this expenditure because of the initial outlay required to set up a new customer", "Parte grande del gasto en lino es inversión de crecimiento (dotación de clientes nuevos); sin importe."),
    ("TXT_BAJAS", 2025, U, 141, "customer attrition rates are monitored at the Executive", "La tasa de bajas se sigue internamente; no se publica."),
    ("TXT_VIDA_LINO", 2025, U, 367, "depreciated over a period of 18 months to five years", "Vida útil del lino y equipos propios en alquiler."),
    ("TXT_VIDA_RC", 2025, U, 364, "acquired customer contracts and relationships: 4 to 14 years", "Vida útil de las relaciones con clientes adquiridas."),
    ("TXT_OCEANE_CUPON", 2025, U, 380, "carry an annual coupon of 2.25%", "Cupón de la OCEANE 2029."),
    ("TXT_OCEANE_NOMINAL", 2025, U, 380, "€380.0 million", "Nominal de la OCEANE 2029."),
    ("TXT_PRECIO_2023", 2023, W, 261, "with a price effect of +9% on average during the year", "Efecto precio medio en 2023 dentro del crecimiento orgánico."),
    ("TXT_PRESENT_2023", 2023, W, 266, "broken down between interest (recorded as financial expenses) and principal payments (presented on a separate line)", "Presentación 2023: intereses de arrendamientos dentro de intereses pagados."),
    ("TXT_CONTRIB_EXC", 2025, U, 392, "(€4.9 million in 2025)", "Contribución excepcional francesa 2025 dentro de diferencias de tipo."),
    ("TXT_VOLUMEN_2025", 2025, U, 122, "driven by a price effect from residual inflation in 2025, and a volume effect", "Crecimiento orgánico 2025: efecto precio y efecto volumen (sin importes)."),
    ("TXT_VOLUMEN_2024", 2024, D, 121, "tirée par l'effet prix, en raison de l'inflation résiduelle en 2024, et par l'effet volume", "Crecimiento orgánico 2024: efecto precio y efecto volumen (sin importes)."),
    ("TXT_VOLUMEN_COSTES", 2025, U, 309, "in connection with the continued growth in volumes processed", "Costes de proceso 2025 al alza por crecimiento de volúmenes procesados."),
    # Revisión independiente n.º 1, O1: proporción publicada de mantenimiento del lino plano (factor de riesgo)
    ("TXT_LINO_2TERCIOS_2025", 2025, U, 137, "particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation", "Dos tercios de la inversión en lino plano mantienen el stock en circulación (factor de riesgo de la hostelería)."),
    ("TXT_LINO_2TERCIOS_2024", 2024, D, 135, "en particulier le linge plat dont les deux tiers assurent la maintenance du stock en circulation", "Ídem, DEU 2024."),
    ("TXT_LINO_2TERCIOS_2023", 2023, W, 239, "particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation", "Ídem, URD 2023."),
    ("TXT_LINO_2TERCIOS_2022", 2022, X, 221, "particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation", "Ídem, URD 2022."),
    ("TXT_LINO_2TERCIOS_2021", 2021, Y, 189, "particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation", "Ídem, URD 2021."),
    # O2: efecto precio en 2024–25 (sin cuantificar)
    ("TXT_PRECIO_2024_GRUPO", 2024, D, 252, "une dynamique de prix favorable en lien avec l'inflation du coût de la main-d'œuvre", "Efecto precio 2024 a nivel de grupo, sin cifra."),
    ("TXT_PRECIO_2025_LATAM", 2025, U, 307, "Price momentum is favorable, in line with labor cost inflation", "Efecto precio 2025 en Latinoamérica, sin cifra."),
    ("TXT_PRECIO_2025_UK", 2025, U, 307, "adjustments implemented in the region to offset cost inflation", "Ajustes de precio 2025 en Reino Unido e Irlanda, sin cifra."),
    # O5: la propia Elis cuenta el arrendamiento como renovación dentro de la inversión en sus pruebas de deterioro
    ("TXT_RENOV_ARR_2025", 2025, U, 368, "capital expenditure (including lease renewal)", "Flujo de las pruebas de deterioro: inversión que incluye la renovación de arrendamientos."),
    # Premisa (iv): arrendamientos fuera del ROU, registrados como gasto (evidencia contraria buscada)
    ("TXT_ARR_BAJO_VALOR_2025", 2025, U, 366, "leases of low-value assets totaling €2.0 million", "Arrendamientos de bajo valor registrados como gasto en 2025 (nota 6.3)."),
    ("TXT_ARR_CORTO_2025", 2025, U, 366, "short-term leases totaling €5.9 million", "Arrendamientos a corto plazo registrados como gasto en 2025 (nota 6.3)."),
    ("TXT_ARR_VARIABLE_2025", 2025, U, 366, "variable lease payments totaling €0.9 million", "Pagos variables de arrendamiento registrados como gasto en 2025 (nota 6.3)."),
    # O6: evidencia contra la D&A propia como caso central y señales de contención del capex
    ("TXT_PLAN_CLIMA_A", 2025, U, 369, "the Group's climate plan, with a level of investment greater than", "Hipótesis de deterioro: plan climático con inversión superior a… (frase partida entre columnas)."),
    ("TXT_PLAN_CLIMA_B", 2025, U, 369, "the amortization and depreciation historically recorded", "…la amortización históricamente registrada (continuación de la frase anterior)."),
    ("TXT_PLAN_CLIMA_FR", 2024, D, 315, "supérieur aux amortissements historiquement constatés", "Ídem, DEU 2024."),
    ("TXT_INVERSIONES_FUTURAS", 2025, U, 333, "include additional future investments", "Las hipótesis de deterioro incluyen inversiones futuras adicionales."),
    ("TXT_CAPEX_CONTROL", 2025, U, 122, "effective management of capital expenditure, particularly in linen, has kept depreciation under control", "Contención del capex de lino en 2025."),
    ("TXT_CAPEX_CONTENIDO", 2025, U, 122, "capex contained despite new workwear contracts and expenditure under the Climate plan", "Capex contenido en 2025 pese a contratos nuevos y al plan climático."),
    ("TXT_CAPEX_NORMAL", 2025, U, 312, "The Group's capital expenditure has returned to normal levels since 2024", "Capex normalizado desde 2024."),
    ("TXT_CAPEX_ESTABLE", 2025, U, 311, "They remained stable after the sharp increase in previous years", "Inversión neta estable tras el aumento de años anteriores."),
    # O7: altas de 2025 provisionales
    ("TXT_ALTAS_PROVIS", 2025, U, 340, "the amounts above are only provisional", "Contabilización provisional de las combinaciones de 2025."),
    # O8: datos sobre la cartera de clientes
    ("TXT_CONTRATOS_4A", 2025, U, 141, "contracts are usually valid for an initial four-year term", "Contratos con plazo inicial habitual de cuatro años."),
    ("TXT_PERDIDAS_2024", 2024, D, 121, "a permis de baisser le taux de pertes", "En 2024 bajó la tasa de pérdidas de clientes (sin cifra)."),
    # O9: partida puntual de 2025
    ("TXT_SEGUROS_2025", 2025, U, 309, "a high level of insurance benefits in 2025", "Indemnizaciones de seguros elevadas en 2025 (otros ingresos y gastos operativos)."),
    # O11: intereses y devengo no monetario de la OCEANE
    ("TXT_REFIN_TIPOS", 2025, U, 312, "refinancing transactions in 2024 and 2025 at higher interest rates", "Intereses pagados al alza por refinanciación a tipos mayores."),
    ("TXT_OCEANE_DEVENGO", 2025, U, 314, "-€9.7 million in 2025", "Revalorización no monetaria del componente de deuda de la OCEANE en 2025."),
]


def modo_anio(idf):
    """Modo de control del ejercicio de cada fila (ver verificar_cifras.py)."""
    if idf == "VENTAS_LINO_PLANO_2025" or idf.startswith("VENTAS_SEG_"):
        return "titulo"
    if idf.startswith("CREC_"):
        return "crecimiento"
    if idf.startswith("TAXDIF_"):
        return "max_cabecera"
    if "_SALDO_" in idf or idf.startswith("INT_RC_VNC"):
        return "saldo"
    if idf.startswith(("LS_", "PPE_", "INT_")):
        return "movimientos"
    return "dos_columnas"


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--fuentes", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    a = ap.parse_args()
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))["fuentes"]
    pdf = {s: a.raiz / f["archivo"] for s, f in fuentes.items()}
    for s, p in pdf.items():
        if V.sha256_file(p) != fuentes[s]["sha256"]:
            sys.exit(f"huella distinta: {s}")
    ejercicios = {f["ejercicio"] for f in fuentes.values()}
    filas, errores, ids, pendientes = [], [], set(), []
    for doc, pag, etq, occ, cols, concepto, unidad, nota in T:
        idioma = fuentes[doc]["idioma"]
        texto = V.texto_pagina(pdf[doc], pag)
        cand = V.lineas_con(texto, etq)
        if occ:
            cand = cand[occ - 1:occ]
        if not cand:
            errores.append(f"{doc} p{pag} «{etq}» occ{occ}: sin línea")
            continue
        lineas = texto.splitlines()
        toks_por_linea = [V.tokens_numericos(l, idioma) for _, l in cand]
        for pos, anio, idf, leido in cols:
            try:
                literales = {tk[pos] for tk in toks_por_linea}
            except IndexError:
                errores.append(f"{idf}: sin token en pos {pos}: {[l.strip()[:120] for l in cand]}")
                continue
            if len(literales) != 1:
                errores.append(f"{idf}: ambiguo {literales}")
                continue
            lit = literales.pop()
            v = V.valor(lit, idioma)
            if v is None or v != Fraction(leido):
                errores.append(f"{idf}: leído {leido} ≠ extraído {lit!r} en {doc} p{pag}")
                continue
            if idf in ids:
                errores.append(f"id repetido {idf}")
            ids.add(idf)
            modo = modo_anio(idf)
            e_doc = fuentes[doc]["ejercicio"]
            ey = max(anio, e_doc - 1) if modo == "saldo" else anio
            regla = V.regla_edicion(ey, modo, ejercicios)
            if e_doc > regla:
                errores.append(f"{idf}: publicación {e_doc} posterior a la que exige la regla ({regla})")
                continue
            fila = {"id": idf, "anio": anio, "concepto": concepto, "doc": doc, "pagina": pag, "tipo": "tabla",
                    "etiqueta": etq, "ocurrencia": occ, "pos": pos, "literal": lit, "valor_publicado": leido,
                    "unidad": unidad, "perimetro": V.PERIMETRO_GRUPO, "edicion": "vigente" if e_doc == regla else "anterior",
                    "nota": nota, "control_anio": modo}
            # la fila escrita no puede fallar en ninguna dimensión; lo que no se acredita automáticamente se lista
            r = V.comprobar_tabla(pdf[doc], {k: str(v) for k, v in fila.items()}, idioma, fuentes[doc], ejercicios)
            for k, dv in r["dimensiones"].items():
                if dv["estado"] == "PENDIENTE":
                    pendientes.append(f"{idf}: {k}: {dv['detalle']}")
                elif dv["estado"] != "OK":
                    errores.append(f"{idf}: {k} {dv['estado']}: {dv['detalle']}")
            filas.append(fila)
    for idf, anio, doc, pag, lit, nota in TXT:
        fila = {"id": idf, "anio": anio, "concepto": nota, "doc": doc, "pagina": pag, "tipo": "texto",
                "etiqueta": "", "ocurrencia": 0, "pos": 0, "literal": lit, "valor_publicado": "",
                "unidad": "", "perimetro": "", "edicion": "", "nota": nota, "control_anio": "texto"}
        r = V.comprobar_texto(pdf[doc], {k: str(v) for k, v in fila.items()}, fuentes[doc], ejercicios)
        malos = [f"{k} {dv['estado']}: {dv['detalle']}" for k, dv in r["dimensiones"].items() if dv["estado"] not in ("OK", "NO_APLICA", "PENDIENTE")]
        pendientes += [f"{idf}: {k}: {dv['detalle']}" for k, dv in r["dimensiones"].items() if dv["estado"] == "PENDIENTE"]
        if malos:
            errores.append(f"{idf}: {doc} p{pag}: " + "; ".join(malos))
            continue
        filas.append(fila)
    if errores:
        print("\n".join(errores))
        sys.exit(1)
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    with a.salida.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(filas[0].keys()), delimiter=";")
        w.writeheader()
        w.writerows(filas)
    print(f"{len(filas)} filas escritas en {a.salida}")
    if pendientes:
        print(f"{len(pendientes)} dimensiones sin acreditación automática (quedan PENDIENTE en verificar_cifras.py):")
        print("\n".join("  " + x for x in pendientes))


if __name__ == "__main__":
    main()
