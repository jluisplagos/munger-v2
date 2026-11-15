#!/usr/bin/env python3
"""Pruebas de las comprobaciones de N4 contra falsos positivos (entrega 4.9). Sin LibreOffice; solo lectura.

Uso: python3 -I -B test_n4_comprobaciones.py

Cada prueba construye un estado financiero sintético (identificado como tal) que NO debe acreditar un cero —una línea de intereses
dentro de financiación, un bloque que no cuadra, un interés no dominante, un resultado atribuido distinto, una adquisición en la
columna del año, un depósito corriente, una errata en la columna del año— y comprueba que la función correspondiente lo rechaza.
Después comprueba, sobre los textos reales, que los casos favorables lo siguen siendo (L26 y C48 de 2025).
"""
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import n4_investigacion as N  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append(bool(ok))
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))


FIN_OK = """(sintético)
Cash flows from operating activities
Profit for the year  100  90
Interest paid  (5)  (4)
Net cash from operating activities  150  140
Cash flows from financing activities
Proceeds from loans and borrowings  16  20  10
Payments of loans and borrowings  (30)  (12)
Dividends paid  (10)  (9)
Net cash from/(used in) financing activities  (20)  (11)
"""


def main():
    # 1. lectura de importes
    paso("importes: paréntesis = negativo, «-» = 0, separadores de millar, errata ilegible = None",
         N.valor("(1.234)") == -1234 and N.valor("1,234,567") == 1234567 and N.valor("-") == 0 and N.valor("112,5000") is None and N.valor("13") == 13)
    # 2. financiación favorable sintética
    c = N.ch_financiacion(2025, {7: FIN_OK}, 7)
    paso("financiación sintética que cuadra, sin intereses dentro y con «Interest paid» en explotación: se acepta",
         c["cuadre_financiacion"]["ok"] and not c["lineas_intereses_en_financiacion"] and c["intereses_pagados_en_explotacion"])
    # 3. una línea de intereses dentro de financiación
    t = FIN_OK.replace("Dividends paid  (10)  (9)", "Interest paid on borrowings  (3)  (2)\nDividends paid  (7)  (7)")
    c = N.ch_financiacion(2025, {7: t}, 7)
    paso("línea de intereses dentro de financiación: se detecta (no acredita el cero)", c["lineas_intereses_en_financiacion"] != [], str(c["lineas_intereses_en_financiacion"]))
    # 4. financiación que no cuadra (falta una línea)
    t = FIN_OK.replace("Dividends paid  (10)  (9)\n", "")
    c = N.ch_financiacion(2025, {7: t}, 7)
    paso("bloque de financiación que no cuadra: no se acepta", not N.cuadre_actual(c["cuadre_financiacion"]), str(c["cuadre_financiacion"].get("total")))
    # 5. errata en la columna DEL AÑO que NO descuadra la suma (el ilegible cuenta 0): no se acepta; en la comparativa, sí (auditoría interna, Z-4)
    t = FIN_OK.replace("Dividends paid  (10)  (9)", "Dividends paid  (10)  (9)\nOther financing payments  0,00  -")
    c = N.ch_financiacion(2025, {7: t}, 7)
    t2 = FIN_OK.replace("Proceeds from loans and borrowings  16  20  10", "Proceeds from loans and borrowings  16  20  1,00")
    c2 = N.ch_financiacion(2025, {7: t2}, 7)
    paso("importe ilegible en la columna del año, aunque la suma cuadre: no se acepta; el mismo en la columna comparativa: se tolera y se declara",
         c["cuadre_financiacion"]["actual_cuadra"] and not N.cuadre_actual(c["cuadre_financiacion"]) and N.cuadre_actual(c2["cuadre_financiacion"]) and c2["cuadre_financiacion"]["ilegibles"][0]["columna"] == "anterior")
    # 6. minoritarios: balance con interés no dominante
    bal = """(sintético)
Equity attributed to equity holders of the Parent  1,000  900
Non-controlling interests  50  40
Total liabilities  500  450
Total equity and liabilities  1,550  1,390
"""
    pyg = """Profit for the year from continuing operations  100  90
Profit for the year  100  90
Profit for the year attributable to equity holders of the Parent  100  90
"""
    c = N.ch_minoritarios(2025, {3: bal, 4: pyg}, 3)
    paso("balance con intereses no dominantes: el cuadre atribuido + pasivo ≠ total lo rechaza", not c["cuadre_balance"], str((c["patrimonio_atribuido"], c["total_pasivo"], c["total_pn_y_pasivo"])))
    # 7. minoritarios: resultado atribuido distinto
    bal2 = bal.replace("Non-controlling interests  50  40\n", "").replace("1,550  1,390", "1,500  1,350")
    c = N.ch_minoritarios(2025, {3: bal2, 4: pyg.replace("attributable to equity holders of the Parent  100  90", "attributable to equity holders of the Parent  95  90")}, 3)
    paso("resultado atribuido a la dominante ≠ resultado del ejercicio: se rechaza aunque el balance cuadre", c["cuadre_balance"] and not c["cuadre_resultado"])
    # 8. adquisiciones: importe en la columna del año
    inv = """(sintético)
Cash flows from investing activities
Acquisition of property, plant and equipment  (100)  (90)
Acquisition of a subsidiary, net of the cash acquired  (40)
Net cash used in investing activities  (140)  (90)
"""
    c = N.ch_inversion(2020, {13: inv}, 13)
    act = [l for l in c["linea_adquisiciones_un_importe"] if l["columna"] == "actual"]
    paso("adquisición con un solo importe que cuadra en la columna del año: se detecta como importe del año", c["cuadre_inversion"]["ok"] and act != [], str(c["linea_adquisiciones_un_importe"]))
    # 9. activo corriente con un depósito
    ac = """(sintético)
Current assets
Inventories  10  100  90
Short-term deposits  20  15
Cash and cash equivalents  30  25
  150  130
"""
    c = N.ch_activo_corriente(2020, {2: ac}, 2)
    paso("activo corriente con depósitos a corto plazo: se detecta (no acredita el cero de otros activos financieros)", c["lineas_inversiones_financieras_corrientes"] != [])
    # 10. cita que no está en su página
    paso("una cita que no está en su página no se da por contrastada", not N.cita_en_pagina("Interest paid (20,800) (32,100)", "Interest paid (20,801) (32,100)"))
    # 10b. listas blancas: rótulos alternativos que esconderían el concepto (casos de la auditoría interna, Z-4)
    otros_fin = ("Finance costs paid", "Gastos financieros pagados", "Borrowing costs paid")
    r = [N.ch_financiacion(2025, {7: FIN_OK.replace("Dividends paid  (10)  (9)", f"{x}  (3)  (2)\nDividends paid  (7)  (7)")}, 7)["rotulos_no_reconocidos"] for x in otros_fin]
    paso("intereses en financiación con otro rótulo («Finance costs paid», «Gastos financieros pagados», «Borrowing costs paid»): rótulo no reconocido, no se acepta", all(r), str(r))
    inv = "(sintético)\nCash flows from investing activities\nAcquisition of property, plant and equipment  (100)  (90)\n{l}\nNet cash used in investing activities  (140)  (90)\n"
    otros_inv = ("Acquisition of businesses, net of cash acquired", "Business combinations, net of cash acquired", "Purchase of subsidiaries", "Adquisición de negocios, neta de la caja adquirida", "Combinaciones de negocios")
    r = [N.ch_inversion(2020, {13: inv.format(l=f"{x}  (40)  -")}, 13)["rotulos_no_reconocidos"] for x in otros_inv]
    paso("adquisición del año con otro rótulo (cinco variantes): rótulo no reconocido, no se acepta", all(r), str(r))
    ac = "(sintético)\nCurrent assets\nInventories  10  100  90\n{l}  20  15\nCash and cash equivalents  30  25\n  150  130\n"
    otros_ac = ("Short-term investments", "Current financial assets", "Marketable securities", "Imposiciones a corto plazo", "Inversiones a corto plazo", "Activos financieros corrientes")
    r = [N.ch_activo_corriente(2020, {2: ac.format(l=x)}, 2)["rotulos_no_reconocidos"] for x in otros_ac]
    paso("activo financiero corriente con otro rótulo (seis variantes): rótulo no reconocido, no se acepta", all(r), str(r))
    # 10c. condiciones generales de la clasificación: cita, unidad, comparativa y rótulos
    base = {"clasificacion": 2, "cita_en_su_pagina": True, "comparativa_coherente": True, "comprobaciones": {"unidad": True, "rotulos_no_reconocidos": []}, "explicacion": "x", "valor_propuesto": 0.0}
    casos = [dict(base, cita_en_su_pagina=False), dict(base, comparativa_coherente=False), dict(base, comprobaciones={"unidad": False, "rotulos_no_reconocidos": []}),
             dict(base, comprobaciones={"unidad": True, "rotulos_no_reconocidos": ["Finance costs paid"]}), dict(base, clasificacion=4)]
    res = [N.aplicar_condiciones_generales(json.loads(json.dumps(x)))["clasificacion"] for x in casos]
    ok_base = N.aplicar_condiciones_generales(json.loads(json.dumps(base)))["clasificacion"] == 2 and N.aplicar_condiciones_generales(json.loads(json.dumps(dict(base, comparativa_coherente=None))))["clasificacion"] == 2
    paso("clasificación: una cita fuera de su página, una comparativa que contradice, la unidad no localizada o un rótulo no reconocido bajan la entrada a la clase 3 (también una clase 4 sin cita)",
         res[:4] == [3, 3, 3, 3] and N.aplicar_condiciones_generales(dict(json.loads(json.dumps(base)), clasificacion=4, cita_en_su_pagina=False))["clasificacion"] == 3 and ok_base, str(res))
    # 10d. engaños estructurales del control de vigencia de la 4.9 (V-4): lo que no se examina línea a línea pasa a excepción
    exc = lambda c: c["excepciones_estructura"]  # noqa: E731
    b1 = N.ch_financiacion(2025, {7: FIN_OK.replace("Dividends paid  (10)  (9)", "(3)  (2)\nDividends paid  (7)  (7)")}, 7)
    b2 = N.ch_financiacion(2025, {7: FIN_OK + "Of which: interest paid included in payments of loans  (3)  (2)\n"}, 7)
    b3 = N.ch_financiacion(2025, {7: FIN_OK + "Discontinued operations\n" + FIN_OK.split("Cash flows from financing activities")[1].join(["Cash flows from financing activities", ""]).replace("Dividends paid  (10)  (9)", "Interest paid  (3)  (2)\nDividends paid  (7)  (7)")}, 7)
    inv5 = "(sintético)\nCash flows from investing activities\nAcquisition of property, plant and equipment  (100)  (90)\n(40)  -\nNet cash used in investing activities  (140)  (90)\n"
    b5 = N.ch_inversion(2020, {13: inv5}, 13)
    paso("línea solo con importes dentro del bloque (intereses o adquisición sin rótulo), desglose «of which» después del total y segundo bloque de financiación en la página: excepciones de estructura, no se aceptan",
         all(exc(x) for x in (b1, b2, b3, b5)), str([exc(x) for x in (b1, b2, b3, b5)]))
    b4 = N.ch_financiacion(2025, {7: "(millions of euros)\n" + FIN_OK + "Note: comparative figures in thousands of euros were restated.\n"}, 7)
    b4ok = N.ch_financiacion(2025, {7: "(thousands of euros)\n" + FIN_OK}, 7)
    paso("unidad: una cabecera en millones con «thousands of euros» en una nota al pie no acredita la unidad; la cabecera en miles, sí",
         b4["unidad"] is False and b4ok["unidad"] is True and not exc(b4ok))
    bal11 = "(sintético)\nEquity attributed to equity holders of the Parent  1,000  900\nTotal liabilities  550  490\nTotal equity and liabilities  1,550  1,390\nOutside shareholders' interests included in liabilities  50  40\n"
    c11 = N.ch_minoritarios(2025, {3: bal11, 4: pyg}, 3)
    paso("minoritarios incluidos en «Total liabilities» y desglosados aparte («Outside shareholders' interests»): el cuadre del balance lo rechaza", not c11["cuadre_balance"])
    # 11. casos reales favorables (texto oficial de 2025)
    P = N.paginas_txt(2025)
    cm = N.ch_minoritarios(2025, P, 3)
    cf = N.ch_financiacion(2025, P, 7)
    paso("real 2025: minoritarios (L26) cuadran balance y resultado; financiación (C48) cuadra sin intereses y con «Interest paid» en explotación; unidad en la cabecera y sin excepciones de estructura",
         cm["cuadre_balance"] and cm["cuadre_resultado"] and cf["cuadre_financiacion"]["ok"] and not cf["lineas_intereses_en_financiacion"] and cf["intereses_pagados_en_explotacion"]
         and cm["unidad"] and cf["unidad"] and not cm["excepciones_estructura"] and not cf["excepciones_estructura"])
    # 12. real 2023: errata en la comparativa tolerada solo en la comparativa
    cf = N.ch_financiacion(2023, N.paginas_txt(2023), 7)
    paso("real 2023: la errata «112,5000» está en la columna comparativa; el año cuadra y se declara la errata",
         N.cuadre_actual(cf["cuadre_financiacion"]) and not cf["cuadre_financiacion"]["ok"] and cf["cuadre_financiacion"]["ilegibles"])
    n = sum(R)
    print(f"\n{n}/{len(R)} pruebas de las comprobaciones N4 PASAN")
    sys.exit(0 if n == len(R) else 1)


if __name__ == "__main__":
    main()
