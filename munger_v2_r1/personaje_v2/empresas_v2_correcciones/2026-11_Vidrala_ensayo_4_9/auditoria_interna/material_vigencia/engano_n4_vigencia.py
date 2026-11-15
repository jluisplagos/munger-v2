#!/usr/bin/env python3
"""Control de vigencia 4.9 · Z-4: intentos de engañar la clasificación de n4_investigacion.py con estados SINTÉTICOS (identificados como
tales). Adapta /…/auditoria_interna/material_auditor/engano_n4.py a la clasificación ACTUAL de main(): se reproducen sus expresiones
(intereses: cuadre_actual + sin línea de intereses + «Interest paid» en explotación + sin rótulos no reconocidos; adquisiciones:
cuadre + sin adquisición del año + sin rótulos; otros activos financieros: cuadre + sin inversiones + sin rótulos) y después
aplicar_condiciones_generales() (cita en su página, unidad, comparativa, rótulos). Las páginas sintéticas llevan «(thousands of euros)»
para que la condición de unidad no rechace por sí sola los casos. Un caso ACEPTADO (clase 2) que debía rechazarse es un falso positivo.
Solo lectura; no escribe en la copia auditada.
Uso: python3 -I -B engano_n4_vigencia.py"""
import json
import sys

sys.dont_write_bytecode = True
sys.path.insert(0, "/home/claude/vigencia_4_9/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/scripts")
import n4_investigacion as N  # noqa: E402

R = []
UNI = "(sintético) Consolidated statement (thousands of euros)\n"


def condiciones(c, clase):
    e = {"clasificacion": clase, "cita_en_su_pagina": True, "comparativa_coherente": True, "comprobaciones": c, "explicacion": "", "valor_propuesto": 0.0}
    return N.aplicar_condiciones_generales(e)["clasificacion"]


def clase_intereses(texto):
    c = N.ch_financiacion(2020, {7: texto}, 7)
    ok = N.cuadre_actual(c["cuadre_financiacion"]) and not c["lineas_intereses_en_financiacion"] and bool(c["intereses_pagados_en_explotacion"]) and not c["rotulos_no_reconocidos"]
    return condiciones(c, 2 if ok else 3), c


def clase_adq(texto):
    c = N.ch_inversion(2020, {13: texto}, 13)
    cu = c["cuadre_inversion"]
    adq_actual = [l for l in c["linea_adquisiciones_un_importe"] if l["columna"] == "actual"] + c["linea_adquisiciones_dos_importes"]
    ok = cu.get("ok") and not adq_actual and not c["rotulos_no_reconocidos"]
    return condiciones(c, 2 if ok else 3), c


def clase_otros(texto):
    c = N.ch_activo_corriente(2020, {2: texto}, 2)
    cu = c["cuadre_activo_corriente"]
    ok = cu.get("ok") and not c["lineas_inversiones_financieras_corrientes"] and not c["rotulos_no_reconocidos"]
    return condiciones(c, 2 if ok else 3), c


def clase_minoritarios(bal, pyg):
    c = N.ch_minoritarios(2020, {3: UNI + bal, 4: pyg}, 3)
    ok = c["cuadre_balance"] and c["cuadre_resultado"]
    return condiciones(c, 2 if ok else 3), c


def caso(serie, nombre, clase_c, debia):
    clase, c = clase_c
    acepta = clase == 2
    R.append({"serie": serie, "caso": nombre, "clase": clase, "acepta": acepta, "debia_aceptar": debia})
    etiqueta = ("FALSO POSITIVO" if acepta and not debia else ("ok (rechaza)" if not acepta and not debia else ("ok (acepta)" if acepta else "rechazo inesperado")))
    print(f"{etiqueta} · [{serie}] {nombre} · clase {clase}")


EXP = UNI + """Cash flows from operating activities
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
INV = UNI + """Cash flows from investing activities
Acquisition of property, plant and equipment  (100)  (90)
{linea}
Net cash used in investing activities  (140)  (90)
"""
AC = UNI + """Current assets
Inventories  10  100  90
{linea}
Cash and cash equivalents  30  25
  150  130
"""

# ---------- A. los 16 casos de la auditoría anterior, con la clasificación actual ----------
S = "anteriores"
caso(S, "control favorable: financiación limpia", clase_intereses(EXP + FIN), True)
caso(S, "intereses en financiación «Finance costs paid»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Finance costs paid  (3)  (2)\nDividends paid  (7)  (7)")), False)
caso(S, "intereses en financiación «Gastos financieros pagados»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Gastos financieros pagados  (3)  (2)\nDividends paid  (7)  (7)")), False)
caso(S, "«Interest paid» a «-» y «Borrowing costs paid» en financiación",
     clase_intereses(EXP.replace("Interest paid  (5)  (4)", "Interest paid  -  (4)") + FIN.replace("Dividends paid  (10)  (9)", "Borrowing costs paid  (3)  (2)\nDividends paid  (7)  (7)")), False)
caso(S, "importe ilegible en la columna del año («Other financing payments 0,00»)", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Dividends paid  (10)  (9)\nOther financing payments  0,00  -")), False)
for rot in ("Acquisition of businesses, net of cash acquired  (40)  -", "Business combinations, net of cash acquired  (40)  -", "Purchase of subsidiaries  (40)  -",
            "Adquisición de negocios, neta de la caja adquirida  (40)  -", "Combinaciones de negocios  (40)  -"):
    caso(S, f"adquisición con el rótulo «{rot.split('  ')[0]}»", clase_adq(INV.format(linea=rot)), False)
caso(S, "control: «Acquisition of a subsidiary» con importe en el año", clase_adq(INV.format(linea="Acquisition of a subsidiary, net of the cash acquired  (40)  -")), False)
for rot in ("Short-term investments  20  15", "Current financial assets  20  15", "Marketable securities  20  15", "Imposiciones a corto plazo  20  15",
            "Inversiones a corto plazo  20  15", "Activos financieros corrientes  20  15"):
    caso(S, f"activo financiero corriente «{rot.split('  ')[0]}»", clase_otros(AC.format(linea=rot)), False)

# ---------- B. engaños nuevos (rótulos y estructuras) ----------
S = "nuevos"
# B1. el importe de los intereses en una línea SIN rótulo dentro del bloque (la lista blanca ignora las líneas sin letras; el cuadre la suma)
caso(S, "B1 intereses en financiación en una línea solo con importes (sin rótulo)", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "(3)  (2)\nDividends paid  (7)  (7)")), False)
# B2. «de los cuales intereses» DESPUÉS de la línea de total (fuera del bloque que se examina)
caso(S, "B2 «of which: interest paid» después del total de financiación", clase_intereses(EXP + FIN + "Of which: interest paid included in payments of loans  (3)  (2)\n"), False)
# B3. dos bloques de financiación en la página (actividades continuadas e interrumpidas): intereses en el segundo
caso(S, "B3 segundo bloque de financiación (actividades interrumpidas) con intereses", clase_intereses(EXP + FIN + "Discontinued operations\n" + FIN.replace("Dividends paid  (10)  (9)", "Interest paid  (3)  (2)\nDividends paid  (7)  (7)")), False)
# B4. estado en MILLONES con una mención suelta de «thousands of euros» en la página (la unidad se busca en toda la página)
caso(S, "B4 estado en millones con «thousands of euros» en una nota al pie", clase_intereses(EXP.replace("(thousands of euros)", "(millions of euros)") + FIN + "Note: comparative figures in thousands of euros were restated.\n"), False)
# B5. adquisición del año en una línea solo con importes (rótulo desplazado, como el aviso del texto inglés de 2018)
caso(S, "B5 adquisición del año en una línea solo con importes", clase_adq(INV.format(linea="(40)  -")), False)
# B6. depósito corriente en una línea solo con importes
caso(S, "B6 depósito corriente en una línea solo con importes", clase_otros(AC.format(linea="20  15")), False)
# B7. rótulo con un homoglifo cirílico («Intеrest paid», е = U+0435) dentro de financiación
caso(S, "B7 «Intеrest paid» con homoglifo cirílico en financiación", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Intеrest paid  (3)  (2)\nDividends paid  (7)  (7)")), False)
# B8. rótulo de la lista blanca seguido de una línea de continuación con el concepto («Dividends paid» / «and interest»)
caso(S, "B8 «Dividends paid and» + continuación «interest on borrowings»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Dividends paid and\ninterest on borrowings  (10)  (9)")), False)
# B9. rótulo de la lista blanca con una llamada a nota que contiene la palabra («Dividends paid (incl. interest, note 12)»)
caso(S, "B9 «Dividends paid (incl. finance costs)»", clase_intereses(EXP + FIN.replace("Dividends paid  (10)  (9)", "Dividends paid (incl. finance costs)  (10)  (9)")), False)
# B10. minoritarios rotulados «Outside shareholders' interests» (fuera de la expresión de menciones): el cuadre del balance debe rechazar
bal = "Equity attributed to equity holders of the Parent  1,000  900\nOutside shareholders' interests  50  40\nTotal liabilities  500  450\nTotal equity and liabilities  1,550  1,390\n"
pyg = "Profit for the year from continuing operations  100  90\nProfit for the year  100  90\nProfit for the year attributable to equity holders of the Parent  100  90\n"
caso(S, "B10 «Outside shareholders' interests» en el balance", clase_minoritarios(bal, pyg), False)
# B11. «Total liabilities» que ya incluye los minoritarios (cuadra; el rótulo no se examina con lista blanca)
bal2 = "Equity attributed to equity holders of the Parent  1,000  900\nTotal liabilities  550  490\nTotal equity and liabilities  1,550  1,390\nOutside shareholders' interests included in liabilities  50  40\n"
caso(S, "B11 minoritarios dentro de «Total liabilities» y desglosados aparte", clase_minoritarios(bal2, pyg), False)
# B12. control favorable de minoritarios
bal3 = "Equity attributed to equity holders of the Parent  1,000  900\nTotal liabilities  500  450\nTotal equity and liabilities  1,500  1,350\n"
caso(S, "B12 control favorable de minoritarios", clase_minoritarios(bal3, pyg), True)

fp = [r for r in R if r["acepta"] and not r["debia_aceptar"]]
for s in ("anteriores", "nuevos"):
    deb = [r for r in R if r["serie"] == s and not r["debia_aceptar"]]
    print(f"[{s}] {sum(1 for r in deb if not r['acepta'])} rechazados de {len(deb)} que debían rechazarse; falsos positivos: {[r['caso'] for r in deb if r['acepta']]}")
ctrl = [r for r in R if r["debia_aceptar"]]
print(f"controles favorables aceptados: {sum(r['acepta'] for r in ctrl)} de {len(ctrl)}")
json.dump(R, open("/home/claude/vigencia_4_9/tmp/ejecuciones/engano_n4_vigencia.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
