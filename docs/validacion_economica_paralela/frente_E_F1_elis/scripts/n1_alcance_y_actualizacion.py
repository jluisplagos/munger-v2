"""N1 · alcance en los ejercicios de τ y actualización del earnout de México · F1 · Elis. Solo lectura.

Cálculo de apoyo de dos propuestas para decisión (N1_ALCANCE_EJERCICIOS_TAU.md y N1_ACTUALIZACION_EARNOUT_MEXICO.md).
No adopta nada, no es una entrada registrada ni una valoración: Elis sigue en pendiente_de_datos. No cambia el CSV,
la verificación, el libro ni las fuentes.

Usa las funciones de `contraste_f1.py` (`Fuente`, `datos_anio`, `motor_a`, `leer_libro`) y las mismas ecuaciones que
`copia_investigacion_f1.py` (tipo de la fila 10 con 4 decimales, f, τ de proyección, m0 y motor A). Los cálculos solo
toman filas verificadas del CSV (sin FALLO, edición vigente, grupo, mm EUR). Lo que no está en el CSV va rotulado
[LECTURA], con documento, página, rótulo, literal y posición; con --raiz (árbol munger_v2_r1 materializado) y --release
(carpeta con los PDF de la Release `fuentes-elis-e-20261117` del repositorio auxiliar) el script comprueba la huella de
cada PDF y que cada literal está en su línea de la página (pdftotext -layout). Esa comprobación NO es la verificación
de seis dimensiones de `verificar_cifras.py`: una [LECTURA] no es una fila verificada.

Parte A · alcance de N1: con el τ registrado de cinco años (E8.1), los ajustes de earnout de 2021 y 2022 solo entran
  en τ. Escenarios: N1 en 2023–25; en 2021–25; solo con 2021; solo con 2022; y 2021 con efecto fiscal al tipo teórico.
  Conciliación de la línea fiscal publicada de cada año y suma de la nota 4.6.
Parte B · actualización del earnout de México: línea fiscal con y sin ella; conciliación del pasivo ligado a
  adquisiciones (saldo inicial, altas, revaluación, actualización, pagos, saldo final); puente de Lavartex;
  conciliación publicada entre el resultado financiero y los intereses pagados; efecto de sacarla del resultado antes
  de impuestos que da el tipo.

Uso:
  python3 -I n1_alcance_y_actualizacion.py --cifras ../datos/cifras_fuente.csv \
     --verificacion ../resultados/verificacion_cifras.json --libro <ruta>/Elis_v63_evaluada.xlsx \
     --copia ../resultados/copia_investigacion_f1.json --salida ../resultados/n1_alcance_y_actualizacion.json \
     --informe ../resultados/n1_alcance_y_actualizacion.md [--raiz <ruta>/munger_v2_r1] [--release <carpeta>]
Termina con 1 si un control falla o si una [LECTURA] comprobada no está en su página.
"""
import argparse
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import unicodedata
from fractions import Fraction as Fr
from pathlib import Path

_spec = importlib.util.spec_from_file_location("contraste_f1", Path(__file__).with_name("contraste_f1.py"))
C = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(C)
VENT, HOR = C.VENTANA, C.HORIZONTE

# Release `fuentes-elis-e-20261117` (repositorio auxiliar, SHA256SUMS del índice de la Release)
RELEASE = {
    "REL_FY2024_PRES": ("fy2024_presentacion_en.pdf", "d733b56d6fd25e538d945da6434a0c90a4579fd291550558d2ff786cb2ec4e7d"),
    "REL_FY2025_PRES": ("fy2025_presentacion_en.pdf", "b3642606567cb4d9082e007843670e1fab6d46fab4dd466badfda92648c06786"),
    "REL_H1_2025_COM": ("h1_2025_comunicado_fr.pdf", "1347fc21135ebd6ad5705853f87e489ceee68e864c172b0e2aec4a1a702c9779"),
    "REL_H1_2026_COM": ("h1_2026_comunicado_en.pdf", "5a84458c26fc5b060f5e45e631139436d3a65592e7b676cc29b68ecc44579cb4"),
}

# [LECTURA]: clave → (valor, documento, página PDF, rótulo, ocurrencia, desplazamiento de línea, posición, literal, perímetro)
# rótulo «re:…» es una expresión regular sobre la línea; posición entre las celdas numéricas de la línea (negativa = desde el final).
G, S = "grupo", "sociedad"
LECTURAS = {
    # --- parte A · línea fiscal, tipos teóricos y presentaciones de 2021–22
    "fiscal_earnout_2022": ("0.5", "URD2023", 345, "Adjustments and accretion of non-deductible earnouts", 0, 0, -1, "0.5", G),
    "fiscal_earnout_2023_ed_anterior": ("-15.8", "URD2023", 345, "Adjustments and accretion of non-deductible earnouts", 0, 0, -2, "(15.8)", G),
    "fiscal_earnout_2024": ("0.8", "URD2025", 392, "Adjustments and accretion of non-deductible earnouts", 0, 0, -1, "0.8", G),
    "fiscal_earnout_2025": ("-0.2", "URD2025", 392, "Adjustments and accretion of non-deductible earnouts", 0, 0, -2, "(0.2)", G),
    "tipo_teorico_2021": ("28.41", "URD2022", 326, "Theoretical tax rate", 0, 0, -1, "28.41%", G),
    "tipo_teorico_2022": ("25.83", "URD2023", 345, "Theoretical tax rate", 0, 0, -1, "25.83%", G),
    "tipo_teorico_2023": ("25.83", "DEU2024FR", 337, "Taux théorique", 0, 0, -1, "25,83%", G),
    "tipo_teorico_2024": ("25.83", "URD2025", 392, "Theoretical tax rate", 0, 0, -1, "25.83%", G),
    "ooie_costes_y_earnout_2021_URD21": ("-5.1", "URD2021", 253, "Costs related to acquisitions and earnout adjustments", 0, 0, -2, "(5.1)", G),
    "apm_costes_y_earnout_2021_neto_de_impuesto": ("3.7", "URD2021", 217, "Costs related to acquisitions and earnout adjustments(a)", 0, 0, -2, "3.7", G),
    "ooie_costes_de_transaccion_2021": ("-2.1", "URD2022", 285, "Acquisition-related transaction costs", 0, 0, -1, "(2.1)", G),
    "ooie_total_2021": ("-16.1", "URD2022", 285, "OTHER OPERATING INCOME AND EXPENSES", 0, 0, -1, "(16.1)", G),
    "ooie_total_2022": ("-9.0", "URD2023", 302, "OTHER OPERATING INCOME AND EXPENSES", 0, 0, -1, "(9.0)", G),
    "apm_ooie_2021_neto_de_impuesto": ("11.5", "URD2022", 249, "Other operating income and expenses(a)", 0, 0, -1, "11.5", G),
    "apm_ooie_2022_neto_de_impuesto": ("7.0", "URD2023", 267, "Other operating income and expenses(a)", 0, 0, -1, "7.0", G),
    "apm_ooie_2023_neto_de_impuesto": ("64.6", "URD2023", 267, "Other operating income and expenses(a)", 0, 0, -2, "64.6", G),
    "ooie_total_2023_URD23": ("-67.9", "URD2023", 302, "OTHER OPERATING INCOME AND EXPENSES", 0, 0, -2, "(67.9)", G),
    "actualizacion_earnout_2022": ("0", "URD2023", 267, "Accretion expense for the earnout pertaining to the acquisition in Mexico", 0, 0, -1, "-", G),
    "actualizacion_earnout_2023_URD23": ("12.4", "URD2023", 267, "Accretion expense for the earnout pertaining to the acquisition in Mexico", 0, 0, -2, "12.4", G),
    "gastos_de_actualizacion_2022": ("-0.3", "URD2023", 332, "Accretion expenses", 0, 0, -1, "(0.3)", G),
    "intereses_de_provisiones_2022_URD22": ("-0.3", "URD2022", 313, "Interest expense on provisions and retirement benefits", 0, 0, -2, "(0.3)", G),
    "fiscal_deterioro_fondo_de_comercio_2022": ("-15.1", "URD2023", 345, "Goodwill impairment", 0, 0, -1, "(15.1)", G),
    "efe_otros_sin_efecto_en_caja_2021": ("2.9", "URD2022", 261, r"re:^Other\s{2,}", 0, 0, -1, "2.9", G),
    "efe_earnout_y_otros_sin_efecto_en_caja_2022": ("-2.5", "URD2023", 279, "Earnout adjustments and other elements with no impact on cash flows", 0, 0, -1, "(2.5)", G),
    # pasivo ligado a adquisiciones y pagos de 2021–22 (la nota 2.4 de esos años no tiene fila propia de earnouts)
    "deuda_adquisiciones_2022_ed_anterior": ("90.4", "URD2022", 320, "Debt related to acquisitions", 0, 0, 0, "90.4", G),
    "deuda_adquisiciones_2021": ("27.1", "URD2022", 320, "Debt related to acquisitions", 1, 0, 0, "27.1", G),
    "aplazado_corriente_2021": ("6.5", "URD2022", 286, "Deferred consideration payable on acquisitions", 0, 0, -1, "6.5", G),
    "aplazado_no_corriente_2021": ("19.3", "URD2022", 321, "Deferred consideration payable on acquisitions", 0, 0, -1, "19.3", G),
    "recompra_de_minoritarios_2021": ("1.2", "URD2022", 286, "Liability for repurchase commitments to non-controlling interests", 0, 0, -1, "1.2", G),
    "compras_2021_precio_brasil": ("1.4", "URD2022", 277, "PURCHASE PRICE", 0, 0, 2, "1.4", S),
    "compras_2021_pagado_brasil": ("-9.4", "URD2022", 277, "Amount paid", 0, 0, 2, "(9.4)", S),
    "compras_2021_precio_rusia": ("15.4", "URD2022", 277, "PURCHASE PRICE", 0, 0, -2, "15.4", S),
    "compras_2021_pagado_rusia": ("-5.7", "URD2022", 277, "Amount paid", 0, 0, -2, "(5.7)", S),
    "compras_2022_pagado_rusia": ("-7.8", "URD2022", 275, r"re:^Russia\s{2,}", 0, 0, 1, "(7.8)", S),
    # --- parte B · pasivo ligado a adquisiciones (valor razonable, nivel 3) y sus dos líneas de balance
    "deuda_adquisiciones_2025": ("12.9", "URD2025", 386, "Debt related to acquisitions", 0, 0, 0, "12.9", G),
    "deuda_adquisiciones_2024": ("23.9", "URD2025", 386, "Debt related to acquisitions", 1, 0, 0, "23.9", G),
    "deuda_adquisiciones_2024_ed_anterior": ("23.5", "DEU2024FR", 331, "Dettes liées aux acquisitions", 0, 0, 0, "23,5", G),
    "deuda_adquisiciones_2023": ("118.2", "DEU2024FR", 331, "Dettes liées aux acquisitions", 1, 0, 0, "118,2", G),
    "deuda_adquisiciones_2023_ed_anterior": ("117.3", "URD2023", 339, "Debt related to acquisitions", 0, 0, 0, "117.3", G),
    "deuda_adquisiciones_2022": ("90.5", "URD2023", 339, "Debt related to acquisitions", 1, 0, 0, "90.5", G),
    "aplazado_corriente_2025": ("0.6", "URD2025", 352, "Deferred consideration payable on acquisitions", 0, 0, -2, "0.6", G),
    "aplazado_corriente_2024": ("19.4", "URD2025", 352, "Deferred consideration payable on acquisitions", 0, 0, -1, "19.4", G),
    "aplazado_no_corriente_2025": ("12.3", "URD2025", 387, "Deferred consideration payable on acquisitions", 0, 0, -2, "12.3", G),
    "aplazado_no_corriente_2024": ("4.5", "URD2025", 387, "Deferred consideration payable on acquisitions", 0, 0, -1, "4.5", G),
    "aplazado_corriente_2024_ed_anterior": ("19.1", "DEU2024FR", 298, "Dette liée aux paiements différés relatifs aux acquisitions", 0, 0, -2, "19,1", G),
    "aplazado_corriente_2023": ("86.2", "DEU2024FR", 298, "Dette liée aux paiements différés relatifs aux acquisitions", 0, 0, -1, "86,2", G),
    "aplazado_no_corriente_2024_ed_anterior": ("4.4", "DEU2024FR", 332, "Dette liée aux paiements différés relatifs aux acquisitions", 0, 0, -2, "4,4", G),
    "aplazado_no_corriente_2023": ("31.9", "DEU2024FR", 332, "Dette liée aux paiements différés relatifs aux acquisitions", 0, 0, -1, "31,9", G),
    "aplazado_corriente_2023_ed_anterior": ("86.0", "URD2023", 304, "Deferred consideration payable on acquisitions", 0, 0, -2, "86.0", G),
    "aplazado_corriente_2022": ("33.5", "URD2023", 304, "Deferred consideration payable on acquisitions", 0, 0, -1, "33.5", G),
    "aplazado_no_corriente_2023_ed_anterior": ("31.3", "URD2023", 340, "Deferred consideration payable on acquisitions", 0, 0, -2, "31.3", G),
    "aplazado_no_corriente_2022": ("57.1", "URD2023", 340, "Deferred consideration payable on acquisitions", 0, 0, -1, "57.1", G),
    # altas por las compras del año: precio de adquisición − desembolso del año (nota 2.4, columna del total)
    "precio_compras_2025": ("124.0", "URD2025", 340, "PURCHASE PRICE", 0, 0, 0, "124.0", G),
    "desembolso_compras_2025": ("-112.6", "URD2025", 341, r"re:^for the acquisition\s{2,}", 0, 0, 0, "(112.6)", G),
    "precio_compras_2024": ("96.7", "URD2025", 342, "PURCHASE PRICE", 0, 0, 0, "96.7", G),
    "desembolso_compras_2024": ("-94.8", "URD2025", 342, r"re:Cash outflows for the acquisition\s{2,}", 0, 0, 0, "(94.8)", G),
    "precio_compras_2024_ed_anterior": ("96.3", "DEU2024FR", 286, "PRIX D'ACQUISITION", 0, 0, 0, "96,3", G),
    "precio_compras_2023": ("51.0", "DEU2024FR", 288, "PRIX D'ACQUISITION", 0, 0, 0, "51,0", G),
    "desembolso_compras_2023": ("-53.4", "DEU2024FR", 288, "Sorties de trésorerie effectuées pour l'acquisition", 0, 0, 0, "(53,4)", G),
    # columnas por sociedad (Lavartex) y «otras adquisiciones»: no son del perímetro del grupo
    "lavartex_precio_de_adquisicion": ("220.2", "URD2023", 294, "PURCHASE PRICE", 0, 0, -2, "220.2", S),
    "lavartex_pagado_2022": ("-148.0", "URD2023", 294, "Amount paid", 0, 0, -2, "(148.0)", S),
    "lavartex_pago_2023": ("-31.4", "DEU2024FR", 288, "Compléments de prix et paiements différés", 0, 0, -2, "(31,4)", S),
    "lavartex_pago_2024": ("-83.2", "URD2025", 342, "Earnouts and deferred consideration", 0, 0, -2, "(83.2)", S),
    "lavartex_pago_2025": ("-19.7", "URD2025", 341, r"re:^consideration\s{2,}", 0, 0, -2, "(19.7)", S),
    "otras_pago_aplazado_2023": ("-3.0", "DEU2024FR", 288, "Compléments de prix et paiements différés", 0, 0, -1, "(3,0)", S),
    "otras_pago_aplazado_2024": ("-10.7", "URD2025", 342, "Earnouts and deferred consideration", 0, 0, -1, "(10.7)", S),
    "otras_pago_aplazado_2025": ("-3.6", "URD2025", 341, r"re:^consideration\s{2,}", 0, 0, -1, "(3.6)", S),
    # --- Release: conciliación publicada del resultado financiero con los intereses pagados, y semestre
    "rel_2024_intereses_deuda_caja": ("-101.5", "REL_FY2024_PRES", 52, "Financial debt interests (cash)", 0, 0, 0, "(101.5)", G),
    "rel_2024_intereses_cobrados_caja": ("25.4", "REL_FY2024_PRES", 52, "Investment interests received (cash)", 0, 0, 0, "25.4", G),
    "rel_2024_comisiones_caja": ("-2.8", "REL_FY2024_PRES", 52, "Recurring fees (cash)", 0, 0, 0, "(2.8)", G),
    "rel_2024_intereses_arrendamientos": ("-25.8", "REL_FY2024_PRES", 52, "Leasing debt interests", 0, 0, 0, "(25.8)", G),
    "rel_2024_ajuste_devengo": ("-5.1", "REL_FY2024_PRES", 52, "Adjustment accrued / non accrued interests", 0, 0, 0, "(5.1)", G),
    "rel_2024_nocional_oceane": ("-9.2", "REL_FY2024_PRES", 52, "Notional interests (OCEANE)", 0, 0, 0, "(9.2)", G),
    "rel_2024_costes_de_emision": ("-5.1", "REL_FY2024_PRES", 52, "Amortization of issuing costs", 0, 0, 0, "(5.1)", G),
    "rel_2024_actualizacion_earnout": ("-5.6", "REL_FY2024_PRES", 52, "Accretion expense for the earnout pertaining to the", 0, 1, 0, "(5.6)", G),
    "rel_2024_otros": ("-0.7", "REL_FY2024_PRES", 52, "Other (including FX) & change in fair value of derivatives", 0, 0, 0, "(0.7)", G),
    "rel_2024_cargo_en_resultados": ("-130.4", "REL_FY2024_PRES", 52, "P&L charge", 0, 0, 0, "(130.4)", G),
    "rel_2024_salida_de_caja": ("-78.9", "REL_FY2024_PRES", 52, "P&L charge", 0, 0, -1, "(78.9)", G),
    "rel_2025_intereses_deuda_caja": ("-114.3", "REL_FY2025_PRES", 51, "Financial debt interests (cash)", 0, 0, 0, "(114.3)", G),
    "rel_2025_intereses_cobrados_caja": ("17.5", "REL_FY2025_PRES", 51, "Investment interests received (cash)", 0, 0, 0, "17.5", G),
    "rel_2025_comisiones_caja": ("-2.5", "REL_FY2025_PRES", 51, "Recurring fees (cash)", 0, 0, 0, "(2.5)", G),
    "rel_2025_intereses_arrendamientos": ("-29.2", "REL_FY2025_PRES", 51, "Leasing debt interests (cash)", 0, 0, 0, "(29.2)", G),
    "rel_2025_ajuste_devengo": ("9.2", "REL_FY2025_PRES", 51, "Adjustment accrued / non accrued interests", 0, 0, 0, "9.2", G),
    "rel_2025_nocional_oceane": ("-9.7", "REL_FY2025_PRES", 51, "Notional interests (OCEANE)", 0, 0, 0, "(9.7)", G),
    "rel_2025_costes_de_emision": ("-5.0", "REL_FY2025_PRES", 51, "Amortization of issuing costs", 0, 0, 0, "(5.0)", G),
    "rel_2025_actualizacion_earnout": ("-0.7", "REL_FY2025_PRES", 51, "Accretion expense for the earnout pertaining", 0, 1, 0, "(0.7)", G),
    "rel_2025_otros": ("-2.3", "REL_FY2025_PRES", 51, "Other (including FX) & change in fair value", 0, 1, 0, "(2.3)", G),
    "rel_2025_otros_caja": ("0.0", "REL_FY2025_PRES", 51, "Other (including FX) & change in fair value", 0, 1, -1, "0.0", G),
    "rel_2025_cargo_en_resultados": ("-137.1", "REL_FY2025_PRES", 51, "P&L charge", 0, 0, 0, "(137.1)", G),
    "rel_2025_salida_de_caja": ("-99.4", "REL_FY2025_PRES", 51, "P&L charge", 0, 0, -1, "(99.4)", G),
    "rel_actualizacion_earnout_S1_2025": ("0.7", "REL_H1_2025_COM", 6, "Charge de désactualisation du complément de prix de l'acquisition réalisée", 0, 1, -2, "0,7", G),
    "rel_actualizacion_earnout_S1_2024": ("7.8", "REL_H1_2025_COM", 6, "Charge de désactualisation du complément de prix de l'acquisition réalisée", 0, 1, -1, "7,8", G),
    "rel_actualizacion_earnout_S1_2026": ("0", "REL_H1_2026_COM", 5, "Accretion expense linked to the earn-out of the Mexican acquisition", 0, 0, -2, "-", G),
}

# Pasajes de texto: todos los fragmentos deben estar en la página (texto normalizado).
PASAJES = [
    ("nota 4.6: política contable de las partidas (2021, 2022, 2023 y 2025)", "URD2022", 285,
     ["Items of material amounts that are unusual, abnormal or infrequent are disclosed separately in the income statement"]),
    ("nota 4.6 de 2023: la misma política", "URD2023", 302,
     ["Items of material amounts that are unusual, abnormal or infrequent are disclosed separately in the income statement"]),
    ("nota 4.6 de 2025: la misma política; ajustes de earnout fuera de las partidas monetarias", "URD2025", 350,
     ["Items of material amounts that are unusual, abnormal or infrequent are disclosed separately in the income statement",
      "of which monetary items", "of which earnout adjustments"]),
    ("revaluación del earnout de México en 2023", "URD2023", 302,
     ["revaluation of the earnout pertaining to the", "acquisition carried out in Mexico in 2022"]),
    ("tipo efectivo de Francia en 2023, por ajustes de earnout no deducibles", "URD2023", 346,
     ["heavily impacted by non-deductible earnout adjustments"]),
    ("lo mismo en el DEU 2024", "DEU2024FR", 338, ["par les ajustements de compléments de prix", "non déductibles fiscalement"]),
    ("la línea fiscal remite a la nota 4.6", "URD2023", 345, ["(**) See Note 4.6."]),
    ("actualización del earnout de México en el resultado financiero, 2023", "URD2023", 332,
     ["affected by the accretion expense of the earnout pertaining to the acquisition carried out in Mexico in"]),
    ("lo mismo en 2024", "DEU2024FR", 324, ["désactualisation du complément de prix de l'acquisition réalisée"]),
    ("lo mismo en 2025", "URD2025", 379, ["decrease in the accretion expense of the earnout pertaining to the", "acquisition carried out in Mexico in 2022"]),
    ("el pasivo ligado a adquisiciones se mide a valor razonable por flujos descontados", "URD2025", 386,
     ["Offsetting assets and debt related to acquisitions: discounted"]),
    ("liquidación del earnout de México en 2024 y 2025", "URD2025", 352,
     ["settlement of the second installment and the balance of the Mexican earnout in 2024 and"]),
    ("reestimación al alza en 2023 y pago en 2024", "DEU2024FR", 298, ["estimation à la hausse de l'earn-out mexicain en 2023 puis son"]),
    ("la deuda financiera neta no incluye el pasivo por earnout", "URD2025", 384,
     ["BORROWINGS AND FINANCIAL DEBT", "CASH AND CASH EQUIVALENTS (ASSETS)", "NET DEBT"]),
    ("estado de flujos: el resultado financiero se añade entero y los intereses pagados van aparte", "URD2025", 327,
     ["Net financial income (expense)", "CASH FLOW BEFORE FINANCE COSTS AND TAX", "Acquisition of subsidiaries, net of cash acquired", "Net interest paid"]),
    ("Release · pago del earnout de México dentro de las adquisiciones, 2024", "REL_FY2024_PRES", 29,
     ["€83m earn-out payment for the", "will be paid in 2025 (c. €20m)"]),
    ("Release · último pago en 2025", "REL_FY2025_PRES", 29, ["acquisitions paid in 2025 ( €20m vs. €83m in 2024)"]),
    ("Release · baja de la actualización por el pago del último earnout (S1 2025)", "REL_H1_2025_COM", 5,
     ["conséquence du paiement du dernier earn-out relatif à l'acquisition mexicaine de 2022"]),
    ("Release · revaluación de 2024 en el primer semestre (unos 25 millones) y carácter no deducible", "REL_H1_2025_COM", 5,
     ["environ 25 millions d'euros", "non déductibles fiscalement"]),
]
# Páginas en las que NO debe aparecer una línea fiscal propia del earnout (búsqueda sin resultado, [B])
SIN_LINEA = [("conciliación fiscal de 2021 en el URD 2022", "URD2022", 326), ("conciliación fiscal de 2021 en el URD 2021", "URD2021", 290)]

NUM = re.compile(r"^\(?[+\-–−]?\d[\d.,]*\)?%?$|^[–\-−]$")


def f6(x, n=6):
    return C.f6(x, n)


def _norm(s):
    s = unicodedata.normalize("NFKC", s).replace("’", "'").replace("‘", "'")
    return s


def _plano(s):
    return re.sub(r"\s+", " ", _norm(s)).strip()


class Paginas:
    """Texto de una página con pdftotext -layout; comprueba la huella del PDF la primera vez que lo abre."""

    def __init__(self, raiz, fuentes, release):
        self.raiz, self.release = raiz, release
        self.fu = json.loads(Path(fuentes).read_text(encoding="utf-8"))["fuentes"]
        self.cache, self.huellas = {}, {}

    def disponible(self, doc):
        return (self.release is not None) if doc in RELEASE else (self.raiz is not None)

    def ruta(self, doc):
        if doc in RELEASE:
            return Path(self.release) / RELEASE[doc][0], RELEASE[doc][1]
        return Path(self.raiz) / self.fu[doc]["archivo"], self.fu[doc]["sha256"]

    def lineas(self, doc, pag):
        if (doc, pag) not in self.cache:
            ruta, sha = self.ruta(doc)
            if doc not in self.huellas:
                self.huellas[doc] = hashlib.sha256(ruta.read_bytes()).hexdigest() == sha
            out = subprocess.run(["pdftotext", "-layout", "-f", str(pag), "-l", str(pag), str(ruta), "-"],
                                 capture_output=True, text=True, check=True).stdout
            self.cache[(doc, pag)] = [_norm(x) for x in out.splitlines()]
        return self.cache[(doc, pag)]


def celdas_numericas(texto):
    return [c for c in re.split(r"\s{2,}", texto.strip()) if NUM.match(c)]


def buscar(lineas, rotulo, ocurrencia, desplazamiento):
    """Devuelve (índice, resto de la línea tras el rótulo) de la ocurrencia pedida entre las líneas con el rótulo y, en la
    línea de datos (la del rótulo más el desplazamiento), al menos una celda numérica."""
    hallados = []
    for i, ln in enumerate(lineas):
        if rotulo.startswith("re:"):
            m = re.search(rotulo[3:], ln)
            fin = m.end() if m else None
        else:
            p = ln.find(_norm(rotulo))
            fin = p + len(_norm(rotulo)) if p >= 0 else None
        if fin is None:
            continue
        j = i + desplazamiento
        if not 0 <= j < len(lineas):
            continue
        resto = lineas[j][fin:] if desplazamiento == 0 else lineas[j]
        if celdas_numericas(resto):
            hallados.append((j, resto))
    return hallados[ocurrencia] if len(hallados) > ocurrencia else None


def valor_del_literal(lit):
    """Valor de un literal impreso: paréntesis = negativo; coma decimal (francés) o punto con coma de millares (inglés); «-» = 0."""
    if lit in ("-", "–", "−"):
        return Fr(0)
    x = lit.strip("()%")
    x = x.replace(",", ".") if re.fullmatch(r"\d+,\d+", x) else x.replace(",", "")
    return (-1 if lit.startswith("(") else 1) * Fr(x)


def comprobar_lecturas(P):
    res, fallan = {}, []
    for k, (v, doc, pag, rot, oc, des, pos, lit, per) in LECTURAS.items():
        r = {"valor": v, "doc": doc, "pagina_pdf": pag, "rotulo": rot[3:] if rot.startswith("re:") else rot,
             "posicion": pos, "literal": lit, "perimetro": per, "valor_igual_al_literal": Fr(v) == valor_del_literal(lit),
             "comprobada": P.disponible(doc)}
        if not r["valor_igual_al_literal"]:
            fallan.append(k)
        if r["comprobada"]:
            h = buscar(P.lineas(doc, pag), rot, oc, des)
            cel = celdas_numericas(h[1]) if h else []
            r["linea"] = _plano(P.lineas(doc, pag)[h[0]]) if h else None
            r["en_su_linea"] = bool(h) and -len(cel) <= pos < len(cel) and cel[pos] == lit
            if not r["en_su_linea"] and k not in fallan:
                fallan.append(k)
        res[k] = r
    pas = []
    for nombre, doc, pag, frs in PASAJES:
        r = {"pasaje": nombre, "doc": doc, "pagina_pdf": pag, "fragmentos": frs, "comprobado": P.disponible(doc)}
        if r["comprobado"]:
            texto = _plano("\n".join(P.lineas(doc, pag)))
            r["encontrado"] = all(_plano(x) in texto for x in frs)
            if not r["encontrado"]:
                fallan.append(nombre)
        pas.append(r)
    sin = []
    for nombre, doc, pag in SIN_LINEA:
        r = {"busqueda": nombre, "doc": doc, "pagina_pdf": pag, "comprobado": P.disponible(doc)}
        if r["comprobado"]:
            texto = _plano("\n".join(P.lineas(doc, pag))).lower()
            r["tiene_la_conciliacion"] = "theoretical tax expense" in texto and "permanent differences" in texto
            r["sin_linea_de_earnout"] = "earnout" not in texto and "earn-out" not in texto
            if not (r["tiene_la_conciliacion"] and r["sin_linea_de_earnout"]):
                fallan.append(nombre)
        sin.append(r)
    return res, pas, sin, fallan


def suma_de_la_nota(P, doc, pag, inicio, total, pos):
    """Suma de las líneas de una tabla entre el rótulo inicial y el del total (misma página), en la columna pedida."""
    ls = P.lineas(doc, pag)
    i0 = next(i for i, x in enumerate(ls) if _norm(inicio) in x and celdas_numericas(x[x.find(_norm(inicio)) + len(inicio):]))
    i1 = next(i for i, x in enumerate(ls) if i > i0 and _norm(total) in x)
    def valor(c):
        if c in ("-", "–", "−"):
            return Fr(0)
        neg = c.startswith("(")
        return (-1 if neg else 1) * Fr(c.strip("()").replace(",", ""))
    filas = []
    for x in ls[i0:i1]:
        cel = celdas_numericas(re.sub(r"^\s*\S.*?\s{2,}", "  ", x, count=1)) if re.search(r"\S\s{2,}\S", x) else []
        if len(cel) >= 2:
            filas.append((_plano(x), valor(cel[pos])))
    tot = valor(celdas_numericas(ls[i1][ls[i1].find(_norm(total)) + len(total):])[pos])
    return {"doc": doc, "pagina_pdf": pag, "lineas": len(filas), "suma": f6(sum(v for _, v in filas), 1), "total_publicado": f6(tot, 1),
            "residuo": f6(sum(v for _, v in filas) - tot, 1), "cota_de_redondeo": f6(Fr(5, 100) * (len(filas) + 1), 2),
            "dentro_de_la_cota": abs(sum(v for _, v in filas) - tot) <= Fr(5, 100) * (len(filas) + 1)}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--cifras", required=True, type=Path)
    ap.add_argument("--verificacion", required=True, type=Path)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--copia", type=Path, help="resultados/copia_investigacion_f1.json (cifras ya contrastadas, para el control)")
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--informe", required=True, type=Path)
    ap.add_argument("--raiz", type=Path, help="árbol munger_v2_r1 materializado: comprueba las [LECTURA] en los PDF")
    ap.add_argument("--release", type=Path, help="carpeta con los PDF de la Release fuentes-elis-e-20261117")
    ap.add_argument("--fuentes", type=Path, default=Path(__file__).resolve().parent.parent / "datos" / "fuentes.json")
    a = ap.parse_args()
    F = C.Fuente(a.cifras, a.verificacion)
    A = {y: C.datos_anio(F, y) for y in HOR}
    L = C.leer_libro(a.libro)
    controles, errores = [], []

    def control(nombre, calc, ref, tol=Fr(0)):
        ok = abs(Fr(str(calc)) - Fr(str(ref))) <= tol
        controles.append({"control": nombre, "calculado": f6(calc, 9), "referencia": f6(ref, 9), "ok": ok})
        if not ok:
            errores.append(nombre)

    def avg(fn):
        return sum(fn(A[y]) for y in VENT) / 3

    LV = {k: Fr(v[0]) for k, v in LECTURAS.items()}
    S_avg, V0 = avg(lambda d: d["ventas"]), A[2025]["ventas"]
    r3 = lambda x: Fr(round(x, 3)).limit_denominator(1000)   # noqa: E731  convención «redondeo: 3» del registro
    C48 = avg(lambda d: d["int"]) + avg(lambda d: d["leasepay"] - d["ls_princ"])
    C49 = avg(lambda d: d["ls_princ"])
    C52 = r3(avg(lambda d: d["cfo"])) - r3(avg(lambda d: d["capnet"])) - C48 - C49 - r3(avg(lambda d: d["sbc"]))
    control("FCF base registrado (Historia!C70) = 307,933", C52, Fr(L["Historia!C70"]), Fr(1, 10 ** 9))
    control("C48 = 108", C48, Fr(108))
    control("C49 = 128,1", C49, Fr("128.1"))
    pal = {}
    for nombre, col in (("MALO", "B"), ("NORMAL", "C"), ("BUENO", "D")):
        pal[nombre] = {k: Fr(str(L[f"{h}!{col}{n}"])) for k, h, n in [("g15", "Palancas", 14), ("m_obj", "Palancas", 15),
                                                                         ("s2c", "Palancas", 16), ("roic", "Palancas", 18),
                                                                         ("g_inf", "Análisis", 68)]}
    PER = {"A0": lambda d: d["da_total"], "A1": lambda d: d["da_total"] - d["da_rou"], "A2": lambda d: d["d_own"]}
    t_teor = F.pct("TAX_TEOR_2025") / 100       # 25,83 %: tipo teórico de la matriz (URD 2025 p.392)

    def calcular(aj, aj_bai=None, tau_proy="cinco_años"):
        """aj: {año: [(ΔEBIT, tipo del efecto fiscal o None)]}. None = sin efecto en el gasto por impuesto (regla N1);
        un tipo t = el ajuste lleva su impuesto a ese tipo (gasto += t·ΔEBIT). aj_bai: {año: ΔBAI} sin cambio del EBIT ni
        del gasto (partida financiera no deducible). Mismas ecuaciones que copia_investigacion_f1.py."""
        aj_bai = aj_bai or {}
        tau, ebit = {}, {}
        for y in HOR:
            d = A[y]
            dE = sum((x for x, _ in aj.get(y, [])), Fr(0))
            dB = aj_bai.get(y, Fr(0))
            ebit[y] = d["ebit_h"] + dE
            if not aj.get(y) and not dB:
                tau[y] = d["tau"]                       # fila 10 registrada, sin cambios
            else:
                imp = d["imp"] + sum((t * x for x, t in aj.get(y, []) if t is not None), Fr(0))
                tau[y] = Fr(round(imp / (d["bai"] + dE + dB), 4)).limit_denominator(10 ** 4)   # fila 10: 4 decimales
        nopat = sum(ebit[y] * (1 - tau[y]) for y in VENT) / 3
        taup = sum(tau[y] for y in HOR) / 5 if tau_proy == "cinco_años" else sum(tau[y] for y in VENT) / 3
        m0 = ebit[2025] / V0
        out = {"tau": tau, "taup": taup, "m0": m0, "nopat": nopat, "per": {}}
        for k, DX in PER.items():
            f = (nopat - avg(lambda d: d["capex"] - DX(d) + d["dwc"]) - C52) / S_avg
            out["per"][k] = {"f": f, "F0": V0 * (m0 * (1 - taup) - f), "esc": {n: C.motor_a(V0, m0, taup, f, **p) for n, p in pal.items()}}
        return out

    def variacion(r, b):
        """Variación frente a b; comprueba que es la misma en A0, A1 y A2."""
        d0 = r["per"]["A0"]["F0"] - b["per"]["A0"]["F0"]
        d11 = [r["per"]["A0"]["esc"][n]["flujo_11"] - b["per"]["A0"]["esc"][n]["flujo_11"] for n in pal]
        for k in ("A1", "A2"):
            if r["per"][k]["F0"] - b["per"][k]["F0"] != d0 or \
               [r["per"][k]["esc"][n]["flujo_11"] - b["per"][k]["esc"][n]["flujo_11"] for n in pal] != d11:
                errores.append("variación distinta entre perímetros")
        return d0, d11

    def fila(nombre, r, b_libro, b_n1):
        d0, d11 = variacion(r, b_libro)
        e0, e11 = variacion(r, b_n1)
        return {"escenario": nombre, "tau_2021_2025": [f6(r["tau"][y], 4) for y in HOR], "tau_de_proyeccion": f6(r["taup"], 6),
                "m0": f6(r["m0"], 6), "f_A0": f6(r["per"]["A0"]["f"], 9),
                "flujo_sin_crecimiento_A0": f6(r["per"]["A0"]["F0"], 3),
                "variacion_frente_al_libro": {"flujo_sin_crecimiento": f6(d0, 3), "año_11_MALO_NORMAL_BUENO": [f6(x, 3) for x in d11]},
                "variacion_frente_a_N1_2023_25": {"flujo_sin_crecimiento": f6(e0, 3), "año_11_MALO_NORMAL_BUENO": [f6(x, 3) for x in e11]}}

    earn = {2021: F("OOIE_EARN_U22_2021"), 2022: F("OOIE_EARN_U23_2022"), 2023: A[2023]["ooie_earn"], 2024: A[2024]["ooie_earn"],
            2025: A[2025]["ooie_earn"]}                       # nota 4.6, con su signo (cargo negativo)
    act = {2023: F("FIN_ACTMEX_FR_2023"), 2024: F("FIN_ACTMEX_2024"), 2025: F("FIN_ACTMEX_2025")}   # gasto (positivo)
    n1 = lambda años, tipos=None: {y: [(-earn[y], (tipos or {}).get(y))] for y in años}   # noqa: E731

    base = calcular({})
    control("f A0 sin ajustes = Historia!C58", base["per"]["A0"]["f"], Fr(L["Historia!C58"]), Fr(1, 10 ** 12))
    control("τ de 5 años = Historia!C52", base["taup"], Fr(str(L["Historia!C52"])), Fr(1, 10 ** 12))
    control("flujo sin crecimiento A0 = referencia de E9 (248,496395342656)", base["per"]["A0"]["F0"], Fr("248.496395342656"), Fr(1, 10 ** 9))
    for fl, n in ((6, "MALO"), (7, "NORMAL"), (8, "BUENO")):
        control(f"Motor!BF{fl} sin ajustes = libro", base["per"]["A0"]["esc"][n]["flujo_11"], Fr(L[f"Motor!BF{fl}"]), Fr(1, 10 ** 9))

    # ------------------------------------------------------------------ parte A · alcance de N1
    t21 = LV["tipo_teorico_2021"] / 100
    # 2022: tipo efectivo del ajuste si la línea fiscal publicada (0,5) mide todo lo que no tributa: (t·ajuste − línea) ÷ ajuste
    t22 = (LV["tipo_teorico_2022"] / 100 * earn[2022] - LV["fiscal_earnout_2022"]) / earn[2022]
    R = {"C · N1 en 2023–25 (solo la ventana)": calcular(n1(VENT)),
         "A · N1 en 2021–25 (todos los ejercicios de τ), sin efecto fiscal": calcular(n1(HOR)),
         "B · N1 en 2022–25 (los ejercicios con línea fiscal publicada; sin 2021)": calcular(n1((2022,) + VENT)),
         "descomposición · N1 en 2023–25 y 2021 (sin 2022)": calcular(n1((2021,) + VENT)),
         "sensibilidad de A · el ajuste de 2021 gravado al tipo teórico de 2021 [LECTURA: 28,41 %]": calcular(n1(HOR, {2021: t21})),
         "sensibilidad de A · en 2022 tributa la parte que la línea fiscal no cubre [LECTURA: 0,5]": calcular(n1(HOR, {2022: t22}))}
    b_n1 = R["C · N1 en 2023–25 (solo la ventana)"]
    tabla_A = [fila("Sin ajustes (libro)", base, base, b_n1)] + [fila(k, v, base, b_n1) for k, v in R.items()]
    ext = R["A · N1 en 2021–25 (todos los ejercicios de τ), sin efecto fiscal"]
    # los ajustes de 2021–22 no tocan el EBIT de la ventana, m0 ni f: solo el τ de proyección
    for k, v in R.items():
        control(f"f (A0) igual que con N1 en 2023–25: {k}", v["per"]["A0"]["f"], b_n1["per"]["A0"]["f"])
        control(f"m0 igual que con N1 en 2023–25: {k}", v["m0"], b_n1["m0"])
    d0, d11 = variacion(ext, b_n1)
    control("alcance 2021–22: variación del flujo sin crecimiento = −V0·m0·Δτ (solo el tipo)", d0, -V0 * b_n1["m0"] * (ext["taup"] - b_n1["taup"]))
    control("propuesta §5.1: N1 en 2023–25, flujo sin crecimiento −11,605", variacion(b_n1, base)[0], Fr("-11.605"), Fr(6, 10 ** 4))
    control("propuesta §5.1: N1 en 2023–25, año 11 NORMAL −18,609", variacion(b_n1, base)[1][1], Fr("-18.609"), Fr(6, 10 ** 4))
    control("propuesta §5.1: con 2021–22, flujo sin crecimiento −11,190", variacion(ext, base)[0], Fr("-11.190"), Fr(6, 10 ** 4))
    control("propuesta §5.1: con 2021–22, año 11 NORMAL −18,142", variacion(ext, base)[1][1], Fr("-18.142"), Fr(6, 10 ** 4))
    control("propuesta §5.1: diferencia de alcance +0,416 en el flujo sin crecimiento", d0, Fr("0.416"), Fr(6, 10 ** 4))
    control("propuesta §5.1: diferencia de alcance +0,466 en el año 11 NORMAL", d11[1], Fr("0.466"), Fr(6, 10 ** 4))

    # línea fiscal publicada frente a (ajuste − actualización) × tipo teórico; cota = redondeo de las cifras impresas
    tipo = {2021: LV["tipo_teorico_2021"] / 100, 2022: LV["tipo_teorico_2022"] / 100, 2023: LV["tipo_teorico_2023"] / 100,
            2024: LV["tipo_teorico_2024"] / 100, 2025: t_teor}
    linea = {2022: LV["fiscal_earnout_2022"], 2023: F("TAX_EARN_FR_2023"), 2024: LV["fiscal_earnout_2024"], 2025: LV["fiscal_earnout_2025"]}
    control("línea fiscal de 2023: URD 2023 p.345 (edición anterior) = DEU 2024 p.337 (fila verificada)", LV["fiscal_earnout_2023_ed_anterior"], linea[2023])
    control("línea fiscal de 2024: URD 2025 p.392 = DEU 2024 p.337 (fila verificada, edición anterior)", linea[2024], F.v["TAX_EARN_FR_2024"])
    control("tipo teórico de 2024 [LECTURA] = el de 2025 (fila verificada)", tipo[2024], t_teor)
    eps = Fr(5, 100)
    fiscal = {}
    for y in HOR:
        ac = act.get(y, Fr(0))
        con, sin = tipo[y] * (earn[y] - ac), tipo[y] * earn[y]
        r = {"ajuste_de_earnout_nota_4_6": f6(earn[y], 1), "actualizacion_del_earnout": f6(ac, 1), "tipo_teorico_pct": f6(100 * tipo[y], 2),
             "impuesto_nocional_del_ajuste": f6(sin, 3), "impuesto_nocional_de_ajuste_y_actualizacion": f6(con, 3)}
        if y in linea:
            cota_sin, cota_con = eps + tipo[y] * eps, eps + tipo[y] * eps * (2 if y in act else 1)
            r |= {"linea_fiscal_publicada": f6(linea[y], 1),
                  "residuo_solo_con_el_ajuste": f6(linea[y] - sin, 3), "cuadra_solo_con_el_ajuste": abs(linea[y] - sin) <= cota_sin,
                  "residuo_con_ajuste_y_actualizacion": f6(linea[y] - con, 3), "cuadra_con_ajuste_y_actualizacion": abs(linea[y] - con) <= cota_con,
                  "cota_de_redondeo": f6(cota_con, 3)}
        else:
            r["linea_fiscal_publicada"] = None
        fiscal[str(y)] = r
    e22a = F.v["OOIE_EARN_U22_2022"]                          # 2,1: edición anterior; solo identidad, no entra en el cálculo
    fiscal["2022"] |= {"ajuste_antes_de_la_reexpresion": f6(e22a, 1), "impuesto_nocional_con_la_cifra_anterior": f6(tipo[2022] * e22a, 3),
                       "residuo_con_la_cifra_anterior": f6(linea[2022] - tipo[2022] * e22a, 3),
                       "cuadra_con_la_cifra_anterior": abs(linea[2022] - tipo[2022] * e22a) <= eps + tipo[2022] * eps}
    for y in VENT:
        control(f"línea fiscal de {y} = (ajuste − actualización) × tipo teórico, dentro de la cota de redondeo",
                int(fiscal[str(y)]["cuadra_con_ajuste_y_actualizacion"]), 1)
        control(f"línea fiscal de {y}: sin la actualización NO cuadra", int(fiscal[str(y)]["cuadra_solo_con_el_ajuste"]), 0)
    control("línea fiscal de 2022: con la cifra reexpresada (2,4) NO cuadra dentro de la cota", int(fiscal["2022"]["cuadra_solo_con_el_ajuste"]), 0)
    control("línea fiscal de 2022: con la cifra anterior a la reexpresión (2,1) cuadra", int(fiscal["2022"]["cuadra_con_la_cifra_anterior"]), 1)

    # estado de flujos: la línea que devuelve los ajustes de earnout (no monetarios) frente al ajuste de la nota 4.6, con signo contrario
    efe = {2021: LV["efe_otros_sin_efecto_en_caja_2021"], 2022: LV["efe_earnout_y_otros_sin_efecto_en_caja_2022"],
           2023: A[2023]["earn"], 2024: A[2024]["earn"], 2025: A[2025]["earn"]}
    no_monetario = {str(y): {"linea_del_estado_de_flujos": f6(efe[y], 1), "ajuste_de_earnout_con_signo_contrario": f6(-earn[y], 1),
                             "diferencia (otros elementos sin efecto en caja)": f6(efe[y] + earn[y], 1)} for y in HOR}
    for y in HOR:
        control(f"{y}: la línea no monetaria del estado de flujos devuelve el ajuste de earnout (diferencia ≤ 0,65: otros elementos)",
                int(abs(efe[y] + earn[y]) <= Fr(65, 100)), 1)

    # 2021–22: el pasivo existe y los pagos aplazados están dentro del importe pagado de la nota 2.4 (sin fila propia)
    control("cierre de 2021: pasivo a valor razonable = aplazado corriente + no corriente + recompra de minoritarios (cota 0,2)",
            LV["aplazado_corriente_2021"] + LV["aplazado_no_corriente_2021"] + LV["recompra_de_minoritarios_2021"], LV["deuda_adquisiciones_2021"], Fr(2, 10))
    caja_21_22 = {"pasivo_ligado_a_adquisiciones (valor razonable, nivel 3)": {"cierre_2021": f6(LV["deuda_adquisiciones_2021"], 1),
                                                                                "cierre_2022 (URD 2022)": f6(LV["deuda_adquisiciones_2022_ed_anterior"], 1),
                                                                                "cierre_2022 (URD 2023, reexpresado)": f6(LV["deuda_adquisiciones_2022"], 1)},
                  "2021 · Brasil": {"precio_de_las_compras_del_año": f6(LV["compras_2021_precio_brasil"], 1), "pagado_en_el_año": f6(-LV["compras_2021_pagado_brasil"], 1),
                                    "pagado_de_más_sobre_el_precio": f6(-LV["compras_2021_pagado_brasil"] - LV["compras_2021_precio_brasil"], 1)},
                  "2021 · Rusia": {"precio_de_las_compras_del_año": f6(LV["compras_2021_precio_rusia"], 1), "pagado_en_el_año": f6(-LV["compras_2021_pagado_rusia"], 1),
                                   "pendiente_al_cierre": f6(LV["compras_2021_precio_rusia"] + LV["compras_2021_pagado_rusia"], 1)},
                  "2022 · Rusia (sin compra en 2022)": {"pagado_en_el_año": f6(-LV["compras_2022_pagado_rusia"], 1)},
                  "nota": "columnas por país: muestran que el importe pagado de la nota 2.4 incluye pagos de compras de años anteriores; no identifican earnouts"}

    # presentación de 2021 neta de impuesto (medida alternativa de rendimiento): efecto fiscal implícito
    bruto21, neto21 = -LV["ooie_costes_y_earnout_2021_URD21"], LV["apm_costes_y_earnout_2021_neto_de_impuesto"]
    control("2021: costes de transacción (2,1) + ajustes de earnout (3,0) = línea conjunta del URD 2021 (5,1)",
            -LV["ooie_costes_de_transaccion_2021"] - earn[2021], bruto21)
    apm = {"2021 · costes de adquisición y ajustes de earnout": {
               "bruto": f6(bruto21, 1), "neto_de_impuesto_publicado": f6(neto21, 1), "efecto_fiscal_implicito": f6(bruto21 - neto21, 1),
               "neto_si_todo_lleva_el_tipo_teorico": f6(bruto21 * (1 - tipo[2021]), 3),
               "neto_si_el_ajuste_de_earnout_no_lleva_efecto_fiscal": f6(bruto21 + tipo[2021] * LV["ooie_costes_de_transaccion_2021"], 3)},
           "2021 · nota 4.6 entera": {"bruto": f6(-LV["ooie_total_2021"], 1), "neto_de_impuesto_publicado": f6(LV["apm_ooie_2021_neto_de_impuesto"], 1),
                                       "efecto_fiscal_implicito_pct": f6(100 * (1 - LV["apm_ooie_2021_neto_de_impuesto"] / -LV["ooie_total_2021"]), 1)},
           "2022 · nota 4.6 entera": {"bruto": f6(-LV["ooie_total_2022"], 1), "neto_de_impuesto_publicado": f6(LV["apm_ooie_2022_neto_de_impuesto"], 1),
                                       "efecto_fiscal_implicito_pct": f6(100 * (1 - LV["apm_ooie_2022_neto_de_impuesto"] / -LV["ooie_total_2022"]), 1)},
           "2023 · nota 4.6 entera": {"bruto": f6(-LV["ooie_total_2023_URD23"], 1), "neto_de_impuesto_publicado": f6(LV["apm_ooie_2023_neto_de_impuesto"], 1),
                                       "efecto_fiscal_implicito_pct": f6(100 * (1 - LV["apm_ooie_2023_neto_de_impuesto"] / -LV["ooie_total_2023_URD23"]), 1)}}
    control("2021: el neto publicado (3,7) es el de aplicar el tipo teórico a toda la línea (5,1), con redondeo",
            int(abs(bruto21 * (1 - tipo[2021]) - neto21) <= eps + eps), 1)
    control("2021: el neto publicado (3,7) NO es el de un ajuste de earnout sin efecto fiscal (4,5)",
            int(abs(bruto21 + tipo[2021] * LV["ooie_costes_de_transaccion_2021"] - neto21) <= eps + eps), 0)

    # límite declarado (no es una propuesta): otra partida no deducible de un año de τ, mucho mayor que el alcance de N1
    det22 = -F("IS_DETFC_U23_2022")
    tau22_sin_det = Fr(round(A[2022]["imp"] / (A[2022]["bai"] + det22), 4)).limit_denominator(10 ** 4)
    limite = {"partida": "deterioro del fondo de comercio de 2022 (no deducible; línea fiscal propia)",
              "importe": f6(det22, 1), "linea_fiscal_publicada": f6(LV["fiscal_deterioro_fondo_de_comercio_2022"], 1),
              "importe_por_tipo_teorico": f6(tipo[2022] * det22, 3),
              "tau_2022_registrado": f6(A[2022]["tau"], 4), "tau_2022_sin_la_partida_en_el_BAI": f6(tau22_sin_det, 4),
              "efecto_en_el_tau_de_cinco_años": f6((tau22_sin_det - A[2022]["tau"]) / 5, 6),
              "equivalente_en_el_flujo_sin_crecimiento": f6(-V0 * b_n1["m0"] * (tau22_sin_det - A[2022]["tau"]) / 5, 3),
              "efecto_del_alcance_de_N1_en_el_tau_de_cinco_años": f6(ext["taup"] - b_n1["taup"], 6),
              "nota": "N1 no la alcanza; (5a) aprobó que ninguna otra partida se normaliza. Solo mide que el τ de cinco años no queda "
                      "«normalizado» por extender N1"}

    # ------------------------------------------------------------------ parte B · actualización del earnout de México
    con_act = calcular(n1(VENT), aj_bai={y: act[y] for y in VENT})
    con_act_ext = calcular(n1(HOR), aj_bai={y: act[y] for y in VENT})
    n1_v, act_v = calcular(n1(VENT), tau_proy="ventana"), calcular(n1(VENT), aj_bai={y: act[y] for y in VENT}, tau_proy="ventana")
    tabla_B = [fila("N1 en 2023–25, sin la actualización", b_n1, base, b_n1),
               fila("N1 en 2023–25, con la actualización fuera del BAI que da el tipo", con_act, base, b_n1),
               fila("N1 en 2021–25, sin la actualización", ext, base, b_n1),
               fila("N1 en 2021–25, con la actualización fuera del BAI que da el tipo", con_act_ext, base, b_n1)]
    dB0, dB11 = variacion(con_act, b_n1)
    control("propuesta §5.1: con la actualización, flujo sin crecimiento −12,396", variacion(con_act, base)[0], Fr("-12.396"), Fr(6, 10 ** 4))
    control("propuesta §5.1: con la actualización, año 11 NORMAL −20,270", variacion(con_act, base)[1][1], Fr("-20.270"), Fr(6, 10 ** 4))
    control("propuesta §5.1: efecto de la actualización −0,790 en el flujo sin crecimiento", dB0, Fr("-0.790"), Fr(6, 10 ** 4))
    control("propuesta §5.1: efecto de la actualización −1,661 en el año 11 NORMAL", dB11[1], Fr("-1.661"), Fr(6, 10 ** 4))
    control("la actualización no cambia el EBIT de la ventana ni m0", con_act["m0"], b_n1["m0"])
    # las mismas cifras en la salida ya contrastada de copia_investigacion_f1.py (si se da --copia)
    if a.copia:
        CP = json.loads(a.copia.read_text(encoding="utf-8"))
        e3, dep = CP["P3_normalizacion"]["escenarios"], CP["V3_V4_de_que_depende_N1"]["escenarios"]
        ref_n1 = e3["N1 · ajustes de earnout 2023–25, no deducibles"]
        ref_act = next(v for k, v in dep.items() if k.startswith("N1 + actualización del earnout"))
        ref_ext = next(v for k, v in dep.items() if k.startswith("N1 + ajustes de earnout de 2021–22"))
        for nombre, r, ref_tau, ref_f0, ref_11 in (
                ("N1 en 2023–25", b_n1, ref_n1["tau_5_anios"], ref_n1["variacion_flujo_sin_crecimiento"], ref_n1["variacion_terminal_MALO_NORMAL_BUENO"]),
                ("N1 en 2021–25", ext, ref_ext["tau_de_proyeccion"], ref_ext["variacion_flujo_sin_crecimiento"], ref_ext["variacion_año_11_MALO_NORMAL_BUENO"]),
                ("N1 + actualización", con_act, ref_act["tau_de_proyeccion"], ref_act["variacion_flujo_sin_crecimiento"], ref_act["variacion_año_11_MALO_NORMAL_BUENO"])):
            v0, v11 = variacion(r, base)
            control(f"copia de investigación: {nombre}, τ de proyección", f6(r["taup"], 6), ref_tau)
            control(f"copia de investigación: {nombre}, variación del flujo sin crecimiento", f6(v0, 3), ref_f0)
            for n, x, y in zip(pal, v11, ref_11):
                control(f"copia de investigación: {nombre}, variación del año 11 {n}", f6(x, 3), y)
        control("copia de investigación: f (A0) con N1 en 2023–25", f6(b_n1["per"]["A0"]["f"], 9), ref_n1["f_A0"])
    # descomposición: la parte de f (ventana, 1/3 por año) y la del τ de proyección (1/5 por año)
    parte_f = -V0 * (con_act["per"]["A0"]["f"] - b_n1["per"]["A0"]["f"])
    parte_t = -V0 * b_n1["m0"] * (con_act["taup"] - b_n1["taup"])
    control("efecto de la actualización = parte de f + parte del τ de proyección", dB0, parte_f + parte_t)
    mecanismo = {"parte_de_f (el NOPAT de la ventana sube y f, que es un residuo, sube)": f6(parte_f, 3),
                 "parte_del_tau_de_cinco_años (el tipo proyectado baja)": f6(parte_t, 3), "suma": f6(dB0, 3),
                 "con_el_tau_de_la_ventana (convención NO adoptada; E8.1 mantiene cinco años)": {
                     "flujo_sin_crecimiento": f6(variacion(act_v, n1_v)[0], 3), "año_11_NORMAL": f6(variacion(act_v, n1_v)[1][1], 3)},
                 "nota": "el signo y el tamaño salen de promediar el tipo en tres años dentro de f y en cinco en la proyección"}
    # dónde está: dentro de «Accretion expenses» del resultado financiero (filas verificadas), no en el EBIT
    actual_tot = {2023: -F("FIN_ACTUAL_FR_2023"), 2024: -F("FIN_ACTUAL_2024"), 2025: -F("FIN_ACTUAL_2025")}
    donde = {str(y): {"gastos_de_actualizacion_nota_8_2": f6(actual_tot[y], 1), "de_ellos_earnout_de_Mexico": f6(act[y], 1),
                      "resto": f6(actual_tot[y] - act[y], 1), "resultado_financiero_neto": f6(-A[y]["fin"], 1),
                      "EBIT_de_la_Historia (BAI + financiero)": f6(A[y]["ebit_h"], 1)} for y in VENT}
    for y in VENT:
        control(f"{y}: la actualización del earnout cabe en «Accretion expenses» de la nota 8.2", int(Fr(0) <= act[y] <= actual_tot[y]), 1)
    # conciliación del pasivo ligado a adquisiciones
    pagos = {2023: -F("ADQ_EARNDIF_FR_2023"), 2024: -F("ADQ_EARNDIF_2024"), 2025: -F("ADQ_EARNDIF_2025")}
    def cuadre(y, ini, fin, altas, n_cifras, nota):
        calc = ini + (altas or 0) - earn[y] + act[y] - pagos[y]          # un cargo de earnout (negativo) sube el pasivo
        return {"saldo_inicial": f6(ini, 1), "altas_por_compras_del_año (precio − desembolso)": None if altas is None else f6(altas, 1),
                "revaluacion (nota 4.6; + sube el pasivo)": f6(-earn[y], 1), "actualizacion (resultado financiero)": f6(act[y], 1),
                "pagos (nota 2.4, earnouts y pagos aplazados)": f6(-pagos[y], 1), "saldo_calculado": f6(calc, 1), "saldo_final_publicado": f6(fin, 1),
                "residuo (publicado − calculado)": f6(fin - calc, 1), "cota_de_redondeo": f6(eps * n_cifras, 2),
                "dentro_de_la_cota": abs(fin - calc) <= eps * n_cifras, "residuo_si_se_quita_la_actualizacion": f6(fin - calc + act[y], 1), "nota": nota}
    alt25 = LV["precio_compras_2025"] + LV["desembolso_compras_2025"]
    alt24, alt24a = LV["precio_compras_2024"] + LV["desembolso_compras_2024"], LV["precio_compras_2024_ed_anterior"] + LV["desembolso_compras_2024"]
    pasivo = {
        "2023 · con el cierre del URD 2023": cuadre(2023, LV["deuda_adquisiciones_2022"], LV["deuda_adquisiciones_2023_ed_anterior"], None, 5,
                                                    "altas de 2023 no determinables: el desembolso de las «otras adquisiciones» supera su precio"),
        "2023 · con el cierre reexpresado del DEU 2024": cuadre(2023, LV["deuda_adquisiciones_2022"], LV["deuda_adquisiciones_2023"], None, 5,
                                                                "el cierre de 2023 se reexpresó +0,9 entre ediciones"),
        "2024 · con el DEU 2024 (precio provisional)": cuadre(2024, LV["deuda_adquisiciones_2023"], LV["deuda_adquisiciones_2024_ed_anterior"], alt24a, 7,
                                                              "residuo no explicado por el redondeo: conversión y otros movimientos, no publicados"),
        "2024 · con el URD 2025 (precio definitivo y cierre reexpresado)": cuadre(2024, LV["deuda_adquisiciones_2023"], LV["deuda_adquisiciones_2024"], alt24, 7,
                                                                                  "ídem"),
        "2025 · URD 2025": cuadre(2025, LV["deuda_adquisiciones_2024"], LV["deuda_adquisiciones_2025"], alt25, 7, "cierra exactamente"),
    }
    control("pasivo ligado a adquisiciones 2025: saldo final = inicial + altas + revaluación + actualización − pagos",
            int(pasivo["2025 · URD 2025"]["dentro_de_la_cota"]), 1)
    control("pasivo ligado a adquisiciones 2023 (URD 2023): cierra dentro de la cota", int(pasivo["2023 · con el cierre del URD 2023"]["dentro_de_la_cota"]), 1)
    for y, (c, nc, tot) in {"2025": ("aplazado_corriente_2025", "aplazado_no_corriente_2025", "deuda_adquisiciones_2025"),
                            "2024": ("aplazado_corriente_2024", "aplazado_no_corriente_2024", "deuda_adquisiciones_2024"),
                            "2024 (DEU 2024)": ("aplazado_corriente_2024_ed_anterior", "aplazado_no_corriente_2024_ed_anterior", "deuda_adquisiciones_2024_ed_anterior"),
                            "2023 (DEU 2024)": ("aplazado_corriente_2023", "aplazado_no_corriente_2023", "deuda_adquisiciones_2023"),
                            "2023 (URD 2023)": ("aplazado_corriente_2023_ed_anterior", "aplazado_no_corriente_2023_ed_anterior", "deuda_adquisiciones_2023_ed_anterior"),
                            "2022 (URD 2023)": ("aplazado_corriente_2022", "aplazado_no_corriente_2022", "deuda_adquisiciones_2022")}.items():
        control(f"cierre de {y}: pasivo a valor razonable = aplazado corriente + no corriente (cota 0,15)", LV[c] + LV[nc], LV[tot], Fr(15, 100))
    # Lavartex: del pasivo inicial a los pagos (columnas por sociedad)
    lav_ini = LV["lavartex_precio_de_adquisicion"] + LV["lavartex_pagado_2022"]
    lav_pag = -(LV["lavartex_pago_2023"] + LV["lavartex_pago_2024"] + LV["lavartex_pago_2025"])
    act_tot, rev_tot = sum(act.values()), -sum(earn[y] for y in VENT)
    lavartex = {"precio_de_adquisicion (valor razonable en la fecha de compra)": f6(LV["lavartex_precio_de_adquisicion"], 1),
                "pagado_en_2022": f6(-LV["lavartex_pagado_2022"], 1), "pendiente_en_la_compra (precio − pagado)": f6(lav_ini, 1),
                "pagos_2023_2024_2025": [f6(-LV[f"lavartex_pago_{y}"], 1) for y in VENT], "pagos_2023_25": f6(lav_pag, 1),
                "actualizacion_2023_25": f6(act_tot, 1), "revaluacion_neta_2023_25 (toda la nota 4.6; «principalmente» México)": f6(rev_tot, 1),
                "pendiente + revaluación + actualización": f6(lav_ini + rev_tot + act_tot, 1),
                "residuo_frente_a_los_pagos": f6(lav_pag - (lav_ini + rev_tot + act_tot), 1),
                "residuo_si_se_quita_la_actualizacion": f6(lav_pag - (lav_ini + rev_tot), 1),
                "actualizacion_sobre_los_pagos_pct": f6(100 * act_tot / lav_pag, 1),
                "nota": "el residuo recoge la conversión, los ajustes de 2022 y la parte de los ajustes que no es de México; no se publica"}
    for y in VENT:
        control(f"{y}: pagos de earnouts y aplazados (fila verificada) = Lavartex + otras adquisiciones [LECTURA]", pagos[y],
                -(LV[f"lavartex_pago_{y}"] + LV[f"otras_pago_aplazado_{y}"]), eps * 3)
    # conciliación publicada por la empresa: resultado financiero frente a intereses pagados (Release)
    concil = {}
    for y, cf_int in ((2024, A[2024]["int"]), (2025, A[2025]["int"])):
        p = f"rel_{y}_"
        caja = [LV[p + k] for k in ("intereses_deuda_caja", "intereses_cobrados_caja", "comisiones_caja")] + ([LV[p + "otros_caja"]] if y == 2025 else [])
        resto = [LV[p + k] for k in ("intereses_arrendamientos", "ajuste_devengo", "nocional_oceane", "costes_de_emision", "actualizacion_earnout", "otros")]
        concil[str(y)] = {"partidas_de_caja (en los dos lados)": f6(sum(caja), 1), "partidas_solo_de_resultados": f6(sum(resto), 1),
                          "de_ellas_actualizacion_del_earnout_de_Mexico": f6(LV[p + "actualizacion_earnout"], 1),
                          "cargo_en_resultados_publicado": f6(LV[p + "cargo_en_resultados"], 1), "suma": f6(sum(caja) + sum(resto), 1),
                          "salida_de_caja_publicada": f6(LV[p + "salida_de_caja"], 1), "intereses_netos_pagados_del_EFE (fila verificada)": f6(-cf_int, 1)}
        control(f"{y}: conciliación publicada, cargo en resultados = suma de sus partidas (cota 0,5)", sum(caja) + sum(resto), LV[p + "cargo_en_resultados"], Fr(1, 2))
        control(f"{y}: conciliación publicada, salida de caja = partidas de caja (cota 0,2), sin la actualización", sum(caja), LV[p + "salida_de_caja"], Fr(2, 10))
        control(f"{y}: salida de caja de la conciliación = intereses netos pagados del EFE (componente de C48)", -LV[p + "salida_de_caja"], cf_int)
        control(f"{y}: cargo en resultados de la conciliación = resultado financiero neto", -LV[p + "cargo_en_resultados"], A[y]["fin"])
        control(f"{y}: actualización del earnout en la conciliación = fila verificada", -LV[p + "actualizacion_earnout"], act[y])
    semestre = {"actualizacion_S1_2024 [LECTURA, Release]": f6(LV["rel_actualizacion_earnout_S1_2024"], 1), "actualizacion_2024 (fila verificada)": f6(act[2024], 1),
                "actualizacion_S2_2024 (derivada)": f6(act[2024] - LV["rel_actualizacion_earnout_S1_2024"], 1),
                "actualizacion_S1_2025 [LECTURA, Release]": f6(LV["rel_actualizacion_earnout_S1_2025"], 1), "actualizacion_2025 (fila verificada)": f6(act[2025], 1),
                "actualizacion_S2_2025 (derivada)": f6(act[2025] - LV["rel_actualizacion_earnout_S1_2025"], 1),
                "actualizacion_S1_2026 [LECTURA, Release; impresa «-»]": f6(LV["rel_actualizacion_earnout_S1_2026"], 1)}

    # ------------------------------------------------------------------ comprobación de las [LECTURA] en los PDF
    P = Paginas(a.raiz, a.fuentes, a.release)
    lect, pasajes, sin_linea, fallan = comprobar_lecturas(P)
    if fallan:
        errores.append(f"lecturas con el valor distinto de su literal, o no encontradas en su línea o en su página: {fallan}")
    notas46 = None
    if a.raiz:
        notas46 = {"2021 (URD 2022 p.285)": suma_de_la_nota(P, "URD2022", 285, "Acquisition-related transaction costs", "OTHER OPERATING INCOME AND EXPENSES", -1),
                   "2022 (URD 2023 p.302)": suma_de_la_nota(P, "URD2023", 302, "Acquisition-related transaction costs", "OTHER OPERATING INCOME AND EXPENSES", -1)}
        for k, v in notas46.items():
            control(f"nota 4.6 de {k}: la suma de sus líneas da el total dentro de la cota", int(v["dentro_de_la_cota"]), 1)
        # la línea de la actualización no lleva la llamada «(a) Net of tax effect» y las demás sí (URD 2023 p.267)
        ls = P.lineas("URD2023", 267)
        act_ln = next(x for x in ls if "Accretion expense for the earnout pertaining to the acquisition in Mexico" in x)
        otras = [x for x in ls if "(a)" in x and celdas_numericas(x.split("(a)", 1)[1])]
        marca = {"linea_de_la_actualizacion_sin_la_llamada_(a)": "(a)" not in act_ln, "lineas_con_la_llamada_(a)": len(otras),
                 "nota_al_pie": any("(a) Net of tax effect." in x for x in ls)}
        control("URD 2023 p.267: la actualización no lleva la llamada «neto de efecto fiscal» y las otras cinco líneas sí",
                int(marca["linea_de_la_actualizacion_sin_la_llamada_(a)"] and marca["lineas_con_la_llamada_(a)"] == 5 and marca["nota_al_pie"]), 1)
        # la tabla de la deuda financiera neta (nota 8.5) no tiene ninguna línea de adquisiciones ni de earnout
        ls = P.lineas("URD2025", 384)
        i0 = next(i for i, x in enumerate(ls) if "Net financial debt" in x)
        i1 = next(i for i, x in enumerate(ls) if i > i0 and x.strip().startswith("NET DEBT"))
        tabla_dn = _plano(" ".join(ls[i0:i1 + 1])).lower()
        deuda_neta = {"lineas_de_la_tabla": i1 - i0, "sin_linea_de_adquisiciones_ni_de_earnout": not any(w in tabla_dn for w in ("acquisition", "earnout", "consideration"))}
        control("URD 2025 p.384: la deuda financiera neta no tiene ninguna línea de adquisiciones ni de earnout",
                int(deuda_neta["sin_linea_de_adquisiciones_ni_de_earnout"]), 1)
    else:
        marca = deuda_neta = None
    if not all(P.huellas.values()):
        errores.append(f"huella de PDF distinta: {[d for d, ok in P.huellas.items() if not ok]}")

    usadas = ["OOIE_EARN_U22_2021", "OOIE_EARN_U23_2022", "OOIE_EARN_FR_2023", "OOIE_EARN_2024", "OOIE_EARN_2025",
              "IS_BAI_U22_2021", "IS_BAI_U23_2022", "IS_BAI_FR_2023", "IS_BAI_2024", "IS_BAI_2025",
              "IS_IMP_U22_2021", "IS_IMP_U23_2022", "IS_IMP_FR_2023", "IS_IMP_2024", "IS_IMP_2025",
              "FIN_ACTMEX_FR_2023", "FIN_ACTMEX_2024", "FIN_ACTMEX_2025", "FIN_ACTUAL_FR_2023", "FIN_ACTUAL_2024", "FIN_ACTUAL_2025",
              "TAX_EARN_FR_2023", "TAX_TEOR_2025", "ADQ_EARNDIF_FR_2023", "ADQ_EARNDIF_2024", "ADQ_EARNDIF_2025", "IS_DETFC_U23_2022"]
    filas_csv = {i: {"referencia": F.ref[i], "valor": f6(F.v[i], 2), "estado": F.meta[i]["estado"], "edicion": F.meta[i]["edicion"]} for i in usadas}
    filas_csv |= {i: {"referencia": F.ref[i], "valor": f6(F.v[i], 2), "estado": F.meta[i]["estado"], "edicion": F.meta[i]["edicion"],
                      "uso": "solo identidad entre ediciones; no entra en ningún cálculo"} for i in ("OOIE_EARN_U22_2022", "TAX_EARN_FR_2024")}
    res = {"naturaleza": "cálculo de apoyo de dos propuestas para decisión; no adopta nada, no es una entrada registrada ni una valoración; "
                         "Elis sigue en pendiente_de_datos",
           "huella_libro": L["sha256"], "controles": controles,
           "A_alcance_de_N1": {"escenarios": tabla_A, "linea_fiscal_por_año": fiscal, "no_monetario_en_el_estado_de_flujos": no_monetario,
                               "pasivo_y_pagos_de_2021_22": caja_21_22,
                               "presentacion_neta_de_impuesto": apm,
                               "suma_de_la_nota_4_6": notas46, "limite_declarado": limite},
           "B_actualizacion_del_earnout": {"escenarios": tabla_B, "mecanismo": mecanismo, "donde_esta": donde, "pasivo_ligado_a_adquisiciones": pasivo,
                                           "lavartex": lavartex, "conciliacion_financiero_intereses_pagados": concil, "semestres": semestre,
                                           "llamada_neto_de_efecto_fiscal": marca, "tabla_de_la_deuda_financiera_neta": deuda_neta},
           "filas_verificadas_del_CSV": filas_csv,
           "lecturas": {"nota": "[LECTURA]: cifra publicada leída en el PDF que NO está en el CSV verificado. La comprobación de esta tabla "
                                "(huella del PDF, rótulo, literal y posición en la línea) no es la verificación de seis dimensiones",
                        "cifras": lect, "pasajes": pasajes, "busquedas_sin_resultado": sin_linea,
                        "huellas_pdf": {d: ok for d, ok in sorted(P.huellas.items())}},
           "resumen": {"controles": len(controles), "fallidos": [c["control"] for c in controles if not c["ok"]], "errores": errores,
                       "lecturas": len(lect), "lecturas_comprobadas_en_su_linea": sum(1 for v in lect.values() if v.get("en_su_linea")),
                       "pasajes": len(pasajes), "pasajes_encontrados": sum(1 for v in pasajes if v.get("encontrado")),
                       "busquedas_sin_resultado_confirmadas": sum(1 for v in sin_linea if v.get("sin_linea_de_earnout"))}}
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    def t(filas):
        out = ["| Escenario | τ 2021 / 2022 / 2023 / 2024 / 2025 | τ de proyección | f (A0) | Flujo sin crecimiento | Frente al libro: flujo · año 11 M / N / B | Frente a N1 2023–25: flujo · año 11 M / N / B |",
               "|---|---|---|---|---|---|---|"]
        for x in filas:
            vl, vn = x["variacion_frente_al_libro"], x["variacion_frente_a_N1_2023_25"]
            out.append(f"| {x['escenario']} | {' / '.join(str(v) for v in x['tau_2021_2025'])} | {x['tau_de_proyeccion']} | {x['f_A0']} | "
                       f"{x['flujo_sin_crecimiento_A0']} | {vl['flujo_sin_crecimiento']} · {' / '.join(str(v) for v in vl['año_11_MALO_NORMAL_BUENO'])} | "
                       f"{vn['flujo_sin_crecimiento']} · {' / '.join(str(v) for v in vn['año_11_MALO_NORMAL_BUENO'])} |")
        return out
    md = ["# N1 · alcance en los ejercicios de τ y actualización del earnout de México (cálculo de apoyo)", "",
          "Generado por `scripts/n1_alcance_y_actualizacion.py`. **No adopta nada: no es una entrada registrada ni una valoración.** "
          "Elis sigue en `pendiente_de_datos`. Mismas funciones que `contraste_f1.py`; los cálculos solo usan filas verificadas del CSV, "
          "salvo el escenario rotulado [LECTURA].", "",
          f"Controles: {len(controles)}, fallidos: {len(res['resumen']['fallidos'])}. [LECTURA]: {res['resumen']['lecturas_comprobadas_en_su_linea']} de "
          f"{len(lect)} en su línea del PDF; pasajes: {res['resumen']['pasajes_encontrados']} de {len(pasajes)}; búsquedas sin resultado confirmadas: "
          f"{res['resumen']['busquedas_sin_resultado_confirmadas']} de {len(sin_linea)}; huellas de los PDF: "
          f"{'todas iguales a las declaradas' if P.huellas and all(P.huellas.values()) else 'no comprobadas o alguna distinta'}.", "",
          "## A · Alcance de N1 (perímetro A0_total; la variación es la misma en A1_sin_ROU y A2_propio)", ""] + t(tabla_A) + ["",
          "### Línea fiscal publicada frente a (ajuste − actualización) × tipo teórico", "",
          "| Año | Ajuste de earnout | Actualización | Tipo teórico | Solo el ajuste | Ajuste y actualización | Línea publicada | ¿Cuadra solo con el ajuste? | ¿Y con la actualización? |",
          "|---|---|---|---|---|---|---|---|---|"]
    for y in HOR:
        x = fiscal[str(y)]
        md.append(f"| {y} | {x['ajuste_de_earnout_nota_4_6']} | {x['actualizacion_del_earnout']} | {x['tipo_teorico_pct']} % | {x['impuesto_nocional_del_ajuste']} | "
                  f"{x['impuesto_nocional_de_ajuste_y_actualizacion']} | {x['linea_fiscal_publicada'] if x['linea_fiscal_publicada'] is not None else 'no hay línea'} | "
                  f"{'—' if x['linea_fiscal_publicada'] is None else ('sí' if x['cuadra_solo_con_el_ajuste'] else 'no')} | "
                  f"{'—' if x['linea_fiscal_publicada'] is None else ('sí' if x['cuadra_con_ajuste_y_actualizacion'] else 'no')} |")
    md += ["", f"2022: con la cifra anterior a la reexpresión ({fiscal['2022']['ajuste_antes_de_la_reexpresion']}), "
               f"{fiscal['2022']['impuesto_nocional_con_la_cifra_anterior']}: {'cuadra' if fiscal['2022']['cuadra_con_la_cifra_anterior'] else 'no cuadra'}.", "",
           "### Estado de flujos: línea que devuelve los ajustes de earnout (no monetarios)", "",
           "| Año | Línea del estado de flujos | Ajuste de earnout con signo contrario | Diferencia (otros elementos sin efecto en caja) |", "|---|---|---|---|"] + \
          [f"| {y} | {v['linea_del_estado_de_flujos']} | {v['ajuste_de_earnout_con_signo_contrario']} | {v['diferencia (otros elementos sin efecto en caja)']} |"
           for y, v in no_monetario.items()] + \
          ["", "### Pasivo y pagos de 2021–22 (la nota 2.4 de esos años no tiene fila propia de earnouts)", ""] + \
          [f"- {k}: {v}" for k, v in caja_21_22.items()] + \
          ["", "### Presentación neta de impuesto de 2021–2023 (medida alternativa de rendimiento)", ""] + \
          [f"- {k}: " + "; ".join(f"{kk}: {vv}" for kk, vv in v.items()) for k, v in apm.items()] + \
          ["", "### Límite declarado (no es una propuesta)", ""] + [f"- {k}: {v}" for k, v in limite.items()] + \
          ["", "## B · Actualización del earnout de México", ""] + t(tabla_B) + ["", "### Mecanismo del efecto", ""] + \
          [f"- {k}: {v}" for k, v in mecanismo.items()] + ["", "### Conciliación del pasivo ligado a adquisiciones (valor razonable, nivel 3)", "",
           "| Año y edición | Inicial | Altas | Revaluación | Actualización | Pagos | Calculado | Publicado | Residuo | Cota | Residuo sin la actualización |",
           "|---|---|---|---|---|---|---|---|---|---|---|"]
    for k, v in pasivo.items():
        w = list(v.values())
        md.append(f"| {k} | {w[0]} | {'n. d.' if w[1] is None else w[1]} | {w[2]} | {w[3]} | {w[4]} | {w[5]} | {w[6]} | {w[7]} | {w[8]} | {w[10]} |")
    md += ["", "### Lavartex: del pendiente en la compra a los pagos (columnas por sociedad, [LECTURA])", ""] + [f"- {k}: {v}" for k, v in lavartex.items()] + \
          ["", "### Conciliación publicada entre el resultado financiero y los intereses pagados (Release)", ""] + \
          [f"- {y}: " + "; ".join(f"{k}: {v}" for k, v in c.items()) for y, c in concil.items()] + \
          ["", "### Semestres", ""] + [f"- {k}: {v}" for k, v in semestre.items()] + \
          ["", "### Dónde está la actualización", ""] + [f"- {y}: " + "; ".join(f"{k}: {v}" for k, v in c.items()) for y, c in donde.items()]
    a.informe.write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    return 1 if errores else 0


if __name__ == "__main__":
    sys.exit(main())
