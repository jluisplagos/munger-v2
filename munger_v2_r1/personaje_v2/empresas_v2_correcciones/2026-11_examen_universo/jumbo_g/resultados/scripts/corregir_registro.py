#!/usr/bin/env python3
"""jumbo_g · correcciones del registro de entradas (verificacion_entradas.json, conservado de jumbo_e) que pide el sellado
(munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/jumbo/revision_registro/REVISION_SELLADO.md @ 787ad6f). Extractor: «Claude orquestación».
Cada entrada corregida queda PENDIENTE (sin revisor ni vínculo): la revisará otro agente. Las demás no se tocan; su sello sigue solo si
`verificacion_entradas.py comprobar` mantiene su vínculo vigente (nada se reescribe a mano).
Uso: python3 -I corregir_registro.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO_CAMBIOS.json"""
import copy, datetime as dt, hashlib, json, os, shutil, sys
C, ANT, REG = sys.argv[1:4]
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
shutil.copy2(p, os.path.join(ANT, "verificacion_entradas_conservado_de_jumbo_e.json"))
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
HOY = "2026-11-19"
cambios = []


def pendiente(e, nota):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": "Claude orquestación", "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[Claude orquestación, {HOY}, jumbo_g] {nota} · Comprobación anterior (jumbo_e): {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}",
                         "vinculo": None}
    e["incidencia"] = None
    cambios.append({"celda": e["celda"], "antes": antes, "despues": copy.deepcopy(e)})


# 1) C46 y C40 con C76 = 160
e = E["Análisis!C46"]; e["valor_modelo"] = 317.617
e["derivacion"]["conciliacion"] = ("C46 = media 2023–2025 de [CFO + dividendos cobrados de la cartera cotizada + intereses cobrados − s × (intereses cobrados − cupones de bonos)], con s = C76 × 3 ÷ "
    "Σ caja 2023–2025 = 160 × 3 ÷ 1.415,485114 = 0,339106 (decisiones P-O1 (c), J1 y J2; C76 = 160, hipótesis vigente de la fase B de jumbo_e). CFO 323,918862 / 300,687098 / 296,912917; "
    "dividendos 0,133043 / 0,828384 / 1,8762; intereses cobrados 18,490712 / 13,791382 / 9,91679; cupones 0,595837 / 0,594641 / 0,595058; caja 434,000394 / 444,815962 / 536,668758. "
    "Resultado 317,616988 → libro 317,617 (redondeo a 3 decimales admitido en importe). Mientras el libro no tenga C76 = 160 (lo fija la fase B) la fórmula no reproduce el libro.")
pendiente(e, "valor recalculado con C76 = 160 (discrepancia del sellado de jumbo_e: el libro usaba C76 = 200); configuracion/cambio_jumbo_g.json")
e = E["Análisis!C40"]; e["valor_modelo"] = 255.108
e["derivacion"]["conciliacion"] = ("FCF del accionista 2025 con la definición de C46: CFO 296,9129 − capex 38,384 − intereses de arrendamientos 2,3258 − principal 9,7272 + dividendos 1,8762 + intereses cobrados "
    "9,91679 − C76 ÷ round(caja media, 4) × (9,91679 − cupones 0,595058), con C76 = 160 (hipótesis vigente de la fase B de jumbo_e) y caja media 471,8284 → 255,107832; libro 255,108 "
    "(redondeo a 3 decimales admitido en importe). Mientras el libro no tenga C76 = 160 la fórmula no lo reproduce.")
pendiente(e, "valor recalculado con C76 = 160 (discrepancia del sellado de jumbo_e); configuracion/cambio_jumbo_g.json")
# 2) ceros con cita que no probaba el cero → no_aplicable con su justificación (precedente: Historia!C16, sellado en jumbo_e)
NA = {
 "Historia!D13": "El libro guarda 0 por ausencia de la partida, no por una cifra impresa: el bloque de inversión del estado de flujos consolidado de 2017/18 (texto/jumbo-annual-report-fy2017-18.txt [PDF PAGE 47]) no tiene ninguna línea de compra ni de venta de negocios (fase1_partes/AR_2017.json → partidas.adquisiciones.cero). La página no imprime un guion ni un 0 de esta partida que pueda contrastarse como cero comprobado. La cita anterior («Investments in financial assets available for sale … 8.000.000») era una inversión financiera y no probaba el cero (REVISION_SELLADO.md). En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN: solo una decisión humana registrada lo confirma.",
 "Historia!D17": "El libro guarda 0 por ausencia de la partida: ejercicio 2017/18, anterior a la NIIF 16 (aplicada por el grupo desde el 1-jul-2019); el bloque de financiación del estado de flujos consolidado (texto/jumbo-annual-report-fy2017-18.txt [PDF PAGE 47]: dividendos, devolución de capital, dividendo a cuenta, préstamos obtenidos y devueltos) no tiene ninguna línea de pagos de arrendamientos financieros NIC 17 (fase1_partes/AR_2017.json → partidas.arrendamientos_principal.cero). La página no imprime un guion ni un 0 de esta partida. La cita anterior (una carta de garantía de 8,0 mm) no probaba el cero. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN.",
 "Historia!E17": "El libro guarda 0 por ausencia de la partida: ejercicio 2018/19, anterior a la NIIF 16 (1-jul-2019); el bloque de financiación del estado de flujos consolidado (texto/jumbo-annual-report-fy2018-19.txt [PDF PAGE 48]: dividendos, dividendo a cuenta, préstamos obtenidos, costes del bono, préstamos devueltos) no tiene ninguna línea de pagos de arrendamientos financieros NIC 17 (fase1_partes/AR_2018.json → partidas.arrendamientos_principal.cero). La página no imprime un guion ni un 0 de esta partida. La cita anterior (una carta de garantía de 7,5 mm) no probaba el cero. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN.",
 "Historia!C23": "El libro guarda 0 por ausencia de la partida: ejercicio 2016/17, anterior a la NIIF 16; no hay pasivo por arrendamientos en el balance y el bloque de financiación del estado de flujos (texto/jumbo-annual-report-fy2016-17.txt [PDF PAGE 46]) no tiene ninguna línea de pagos de arrendamientos financieros NIC 17; los compromisos son sobre todo arrendamientos operativos ([PDF PAGE 93]; fase1_partes/AR_2016.json → partidas.arrendamientos.cero). La página no imprime un guion ni un 0 de esta partida. La cita anterior («Other liabilities …», ajuste de la nota 5.30) no probaba el cero. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN.",
 "Historia!D23": "El libro guarda 0 por ausencia de la partida: ejercicio 2017/18, anterior a la NIIF 16; no hay pasivo por arrendamientos en el balance y el bloque de financiación del estado de flujos (texto/jumbo-annual-report-fy2017-18.txt [PDF PAGE 47]) no tiene ninguna línea de pagos de arrendamientos financieros NIC 17; los compromisos son sobre todo arrendamientos operativos ([PDF PAGE 94]; fase1_partes/AR_2017.json → partidas.arrendamientos.cero). La página no imprime un guion ni un 0 de esta partida. La cita anterior (una carta de garantía de 8,0 mm) no probaba el cero. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN."}
for c, j in NA.items():
    e = E[c]; assert e["valor_modelo"] == 0
    e["clase"] = "no_aplicable"; e["fuente"] = {}; e["justificacion"] = j
    pendiente(e, "cero con cita que no lo probaba → no_aplicable con su justificación (REVISION_SELLADO.md; precedente Historia!C16)")
# 3) años: cita de la cabecera de columnas
FY1819 = dict(E["Historia!E17"]["antes_fuente"]) if False else None
src = {c: copy.deepcopy(E[c]["fuente"]) for c in ("Historia!D5", "Historia!F5", "Historia!G5", "Historia!I5")}
ANIOS = {
 "Historia!D5": ("texto/jumbo-annual-report-fy2018-19.txt", 11, "operating activities of € 64,14 mil in 2018/2019 from € 94,84 mil in 2017/2018. Cash and cash equivalent", "Historia!D5",
                 "2017 = ejercicio 2017/18 («2017/2018», el anterior al 2018/2019 del informe); el libro rotula cada ejercicio de julio a junio con el año en que empieza (convención de la fase 1)", "ejercicio 2017/18 (1-jul-2017 a 30-jun-2018)"),
 "Historia!E5": ("texto/jumbo-annual-report-fy2018-19.txt", 11, "operating activities of € 64,14 mil in 2018/2019 from € 94,84 mil in 2017/2018. Cash and cash equivalent", "Historia!D5",
                 "2018 = ejercicio 2018/19 («2018/2019», el del informe; el informe de transición lo da como comparativo con la cabecera «30/06/2019»); el libro rotula el ejercicio de julio a junio con el año en que empieza (convención de la fase 1)", "ejercicio 2018/19 (1-jul-2018 a 30-jun-2019)"),
 "Historia!F5": ("texto/jumbo-annual-report-fy2020.txt", 16, "31/12/2020      31/12/2019      31/12/2019       31/12/2020     31/12/2019    31/12/2019", "Historia!F5",
                 "2019 = año natural 2019 (segunda columna, «01/01/2019- 31/12/2019», del cuadro del EBITDA del grupo del informe 2020, J-T bis; la tercera «31/12/2019» es el periodo de transición)", "año natural 2019 (1-ene-2019 a 31-dic-2019)"),
 "Historia!G5": ("texto/jumbo-annual-report-fy2021.txt", 14, "31/12/2021       31/12/2020        31/12/2021        31/12/2020", "Historia!G5",
                 "2020 = ejercicio cerrado el 31/12/2020 (columna comparativa del informe 2021)", "ejercicio 2020 (1-ene-2020 a 31-dic-2020)"),
 "Historia!I5": ("texto/jumbo-annual-report-fy2023.conversion.txt", 14, "31/12/2023         31/12/2022    31/12/2023    31/12/2022", "Historia!I5",
                 "2022 = ejercicio cerrado el 31/12/2022 (columna comparativa del informe 2023)", "ejercicio 2022 (1-ene-2022 a 31-dic-2022)")}
for c, (arch, pg, cita, base, col, per) in ANIOS.items():
    e = E[c]; f = copy.deepcopy(src[base])
    assert f["archivo"] == arch, (c, f["archivo"], arch)
    f.update({"pagina": pg, "folio": None, "valor_fuente": e["valor_modelo"], "ubicacion": "informe de gestión (cifras del ejercicio)" if pg == 11 else "cabecera de columnas del cuadro del grupo", "columna": col, "periodo": per, "cita": cita,
              "concepto": f"año de la columna {e['valor_modelo']}", "reexpresado": "cabecera de columnas (sin cifra que reexpresar)"})
    e["fuente"] = f
    pendiente(e, "la cita anterior salía de dígitos sueltos o de otro periodo (REVISION_SELLADO.md); ahora es la cabecera de columnas del estado financiero")
# 4) justificaciones desactualizadas
for fila, serie in (("86", "F1.da_rou (amortización de derechos de uso)"), ("87", "F1.da_ppa (amortización de intangibles de combinaciones)")):
    for col, anio in zip("CDEFG", range(2016, 2021)):
        e = E[f"Historia!{col}{fila}"]; assert e["clase"] == "dato_ausente" and e["valor_modelo"] is None
        e["justificacion"] = (f"Celda vacía en el libro (vacío no es cero). motor_a_f1.json declara C85 = A2_propio y la serie {serie} solo para 2021–2025 (H{fila}:L{fila}): la ventana de f "
                              f"(2023–2025) y los cinco años del ancla de S2C (2021–2025). {anio} no lo usa ningún cálculo del perímetro F1, así que no se declara; fase1_v63.json no declara cálculo para Historia!{col}{fila}.")
        pendiente(e, "justificación desactualizada («el motor no declaró la serie»): la serie está declarada para 2021–2025 (REVISION_SELLADO.md)")
e = E["Análisis!C50"]
e["justificacion"] = ("C50 = media 2023–2025 de SBC = 0 (cálculo declarado en cambio_jumbo_c.json C50). Los informes 2023, 2024 y 2025 declaran textualmente que no hay opciones ni plan de entrega de acciones "
                      "(texto/jumbo-annual-report-fy2023.conversion.txt [PDF PAGE 43], texto/jumbo-annual-report-fy2024.txt [PDF PAGE 48] y texto/jumbo-annual-report-fy2025.txt [PDF PAGE 51]: «No options have been granted and no share disposal plan is in place»); las páginas no imprimen guion ni 0 en tabla. "
                      "Historia fila 18: J18, K18 y L18 son no_aplicable con esas frases (K18 lleva el cero desde jumbo_d, resultados/declaracion_f1_jumbo_d.json). El libro guarda 0.")
pendiente(e, "justificación desactualizada («fy2024 p. ?», «K18 dato_ausente»): K18 es no_aplicable con AR2024 PDF p. 48 (REVISION_SELLADO.md)")

# 5) I17 y L14 con el redondeo exacto de la Historia (redondeo_exacto/REVISION.md, C2)
e = E["Historia!I17"]; assert abs(e["valor_modelo"] - 7.0351) < 1e-12
e["valor_modelo"] = 7.0352
e["derivacion"]["conciliacion"] = "principal de arrendamientos 2022 = «Interest paid for leases» (J3) 7.035.150 € = 7,03515 mm → ROUND(…, 4) de la hoja (mitad lejos de cero) = 7,0352; el libro anterior guardaba 7,0351 por el redondeo binario de fase1_historia.py, ya corregido (producto/redondeo-exacto)"
pendiente(e, "valor 7,0352 con el redondeo exacto de la Historia (código de examen/expedientes-f1 @ 6c0e678); la fórmula round(…, 4) ya lo reproduce")
e = E["Historia!L14"]; assert abs(e["valor_modelo"] - 61.1585) < 1e-12
sub = E["aux:jumbo-annual-report-fy2025_p209_variacion_circulante_subtotal_2025"]
PRE = "aux:jumbo-annual-report-fy2025_p209_"
NOMBRES = ["increase_decrease_in_inventories_2025", "increase_decrease_in_trade_and_other_recei_2025", "increase_decrease_in_other_current_assets_2025",
           "non_short_term_restricted_bank_deposits_2025", "increase_decrease_in_liabilities_excluding_2025"]
nuevas = [E[PRE + n] for n in NOMBRES]   # componentes ya registrados (y sellados en jumbo_e): no se duplican ni se tocan
assert [round(a["valor_modelo"], 6) for a in nuevas] == [-49.62744, 1.798445, -19.492757, 1.45, 4.713202], [a["valor_modelo"] for a in nuevas]
d["entradas"] = [x for x in d["entradas"] if x["celda"] != sub["celda"]]
cambios.append({"celda": sub["celda"], "antes": copy.deepcopy(sub), "despues": None, "motivo": "sin uso: L14 ya no se deriva del subtotal impreso"})
e["derivacion"] = {"origenes": [a["celda"] for a in nuevas],
                   "formula": "round(-(" + " + ".join(f'o["{a["celda"]}"]' for a in nuevas) + "), 4)",
                   "conciliacion": ("aumento del circulante 2025 = −(suma de las cinco líneas de variación del circulante de la nota 5.30, AR2025 PDF p. 209) = −((49.627.440) + 1.798.445 + (19.492.757) + 1.450.000 + 4.713.202) "
                                    "= 61.158.550 € = 61,15855 mm → ROUND(…, 4) = 61,1586 (regla del producto: fase1_historia.py suma las líneas, nunca el subtotal). El subtotal impreso es (61.158.549): 1 € menos por el redondeo del emisor. "
                                    "Incluye 1,45 mm de depósitos restringidos no corrientes."),
                   "unidad": "millones de euros"}
e["valor_modelo"] = 61.1586
pendiente(e, "L14 = 61,1586 derivado de las cinco líneas (regla del producto), no del subtotal (redondeo_exacto/REVISION.md, C2)")
d["nota_del_extractor"] = str(d.get("nota_del_extractor") or "") + f" (jumbo_g, {HOY}) Registro conservado de jumbo_e; Claude orquestación corrigió {len(cambios)} entradas que pedía el sellado (resultados/registro_cambios_jumbo_g.json): quedan pendientes de otro revisor."
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": os.path.abspath(__file__), "registro_antes_sha256": h(os.path.join(ANT, "verificacion_entradas_conservado_de_jumbo_e.json")), "registro_despues_sha256": h(p),
           "entradas_corregidas": [x["celda"] for x in cambios], "cambios": cambios}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("corregidas", len(cambios))
