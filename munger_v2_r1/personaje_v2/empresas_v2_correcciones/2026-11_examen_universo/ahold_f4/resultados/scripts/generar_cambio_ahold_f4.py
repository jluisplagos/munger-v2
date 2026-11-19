#!/usr/bin/env python3
"""Genera configuracion/cambio_ahold_f4.json desde cambio_ahold_f3.json (que no se toca) con las decisiones A-Q3, A-NIC17 y Z-ACC del 19-nov-2026.
Las cifras se leen de texto/ (ahold_f3, conservado) y se comprueban antes de escribirlas."""
import copy, json, os, re, sys
from fractions import Fraction as F

BASE = "/home/user/e_work/wt_expedientes/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_examen_universo"
T = os.path.join(BASE, "ahold_f3/Ahold/texto")
f3 = json.load(open(os.path.join(BASE, "configuracion/cambio_ahold_f3.json"), encoding="utf-8"))
meta3 = json.load(open(os.path.join(BASE, "ahold_f3/Ahold/fase1_metadatos.json"), encoding="utf-8"))


def pag(f, n):
    t = open(os.path.join(T, f), encoding="utf-8").read()
    return re.search(r"\[PDF PAGE %d\]\n(.*?)(?=\n\[PDF PAGE |\Z)" % n, t, re.S).group(1)


def linea(f, n, etq):
    L = [l for l in pag(f, n).split("\n") if l.strip().startswith(etq)]
    assert L, (f, n, etq)
    return L[0]


def nums(l):
    out = []
    for x in re.findall(r"\(?-?[\d,]+\)?", l):
        if re.search(r"\d", x):
            v = int(x.strip("()").replace(",", ""))
            out.append(-v if x.startswith("(") else v)
    return out


Q3, A25 = "AD_q3-2026-interim-report.txt", "AD_annual-report-2025.txt"
q = {k: nums(linea(Q3, p, e))[-2:] for k, (p, e) in {
    "oi": (12, "Operating income"), "da": (16, "Depreciation, amortization and impairments"), "cfo": (16, "Net cash from operating activities"),
    "cap": (16, "Purchase of non-current assets"), "ip": (16, "Interest paid"), "ls": (16, "Repayment of lease liabilities"),
    "jv": (16, "Dividends received from joint ventures"), "ir": (16, "Interest and dividend received"),
    "lr": (16, "Lease payments received on lease receivables"), "cash": (14, "Cash and cash equivalents"),
    "eq": (14, "Equity attributable to common shareholders"), "jvi": (14, "Investments in joint ventures and associates")}.items()}
gd = nums(linea(Q3, 24, "Gross debt"))
assert gd == [19747, 19261, 18404]
assert "4,321             3,625               3,301" in pag(Q3, 24)
fy = {k: nums(linea(A25, 216, e))[-2] for k, e in {"cfo": "Net cash from operating activities", "cap": "Purchase of non-current assets", "ip": "Interest paid",
      "ls": "Repayment of lease liabilities", "jv": "Dividends received from joint ventures", "ir": "Interest received",
      "lr": "Lease payments received on lease receivables", "da": "Depreciation, amortization and impairments"}.items()}
fy["oi"] = nums(linea(A25, 212, "Operating income"))[-2]
assert fy == {"cfo": 6989, "cap": -2564, "ip": -261, "ls": -1944, "jv": 28, "ir": 130, "lr": 138, "da": 3733, "oi": 3542}, fy
assert q == {"oi": [2736, 2643], "da": [2739, 2773], "cfo": [4030, 4288], "cap": [-1898, -1805], "ip": [-196, -192], "ls": [-1473, -1461], "jv": [22, 28],
             "ir": [89, 91], "lr": [113, 104], "cash": [3559, 3605], "eq": [14375, 14195], "jvi": [254, 259]}, q
L = {k: fy[k] + q[k][0] - q[k][1] for k in fy}
C40 = sum(L[k] for k in ("cfo", "cap", "ip", "ls", "jv", "ir", "lr"))
EBITDA = L["oi"] + L["da"]
C53, C54, EQ, JVI = q["cash"][0], gd[0], q["eq"][0], q["jvi"][0]
C41 = F("36.05") * F("886.877259")
assert float(C41) == meta3["capitalizacion"]["valor"]
C42 = (C41 + C54 - C53 - JVI) / EBITDA
C33 = round(float(F(C54 - C53, EBITDA)), 4)
C24 = round(float(F(L["oi"], EQ + C54)), 3)
C41_sep = F("36.05") * F("865.173863")
C42_sep = (C41_sep + C54 - C53 - JVI) / EBITDA
assert (C40, EBITDA, C33, C24) == (2150, 7334, 2.2073, 0.107), (C40, EBITDA, C33, C24)
print({"C40": C40, "C42": float(C42), "C33": C33, "C24": C24, "C53": C53, "C54": C54, "EBITDA": EBITDA, "L": L, "C42_sep": float(C42_sep)})

DEC = ("decisión A-Q3 de la persona responsable (19-nov-2026; munger-v2-evidencias-mistral, coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md, "
       "sección «19-nov-2026 (mañana)»)")
LTM = "12 meses (52 semanas) a 27-sep-2026: ejercicio 2025 + 39 semanas de 2026 − 39 semanas de 2025 (informe del 3T 2026, publicado el 4-nov-2026)"
ZACC = ("Z-ACC (19-nov-2026): se mantienen las acciones al cierre del ejercicio (C55 = 886,877259 M a 28-dic-2025, P-O2 a) con el balance a 27-sep-2026, "
        "que ya descuenta 864 de recompras pagadas en 2026 (Q3-26 PDF p. 16; 23.847.837 acciones, 865.173.863 en circulación a 27-sep-2026, p. 21): "
        "desalineación de fechas declarada")

conf = copy.deepcopy(f3)
conf["_estado_del_archivo"] = (
    "Examen del personaje (19-nov-2026). Expediente nuevo ahold_f4 desde ahold_f3/Ahold (que no se toca), sobre la rama examen/expedientes-f1. POR QUÉ: "
    "las decisiones de la persona responsable del 19-nov-2026 (DECISIONES_PARA_EL_USUARIO.md, rama coordinacion/cierre-v2, «19-nov-2026 (mañana)»): "
    "A-Q3 mueve los doce últimos meses y el balance reciente del informe del 2T (28-jun-2026) al del 3T 2026 (27-sep-2026; publicado el 4-nov-2026, ya en texto/, "
    "antes del precio del 13-nov-2026, 36,05 €), y pide expediente nuevo con las fases repetidas; A-NIC17 deja la deuda 2016–2017 como se publicó (con "
    "arrendamientos financieros NIC 17) y la declara; Z-ACC mantiene las acciones al cierre (P-O2 a) y declara la desalineación de fechas en cada cifra afectada. "
    f"Entradas recalculadas con el 3T (cada componente comprobado en texto/ con su página): C24 = {C24} (ROCE antes de impuestos LTM, resultado operativo "
    f"3.542 + 2.736 − 2.643 = 3.635 ÷ capital empleado a 27-sep-2026 = patrimonio 14.375 + deuda bruta 19.747 = 34.122; antes 0,109), C33 = {C33} "
    f"(19.747 − 3.559 = 16.188 ÷ EBITDA LTM 7.334; antes 2,2153), C40 = {C40} (FCF LTM con la regla espejo P-O1 c; antes 2.096), C42 = {float(C42):.6f} "
    f"(antes 6,590310), C53 = {C53} (antes 3.196) y C54 = {C54} (antes 19.261); C31 («Sí») y C34 («No») comprobadas con el 3T sin cambio de valor, con su evidencia "
    "nueva; evidencia preparada de C25, C27 y C76 actualizada al 3T. Se conservan de ahold_f3: P-O1 (c) en C46/C48/C49, C47, C88, C96, P-O2 (a), P-FOSO (a), la serie "
    "intereses_arrendamiento y la declaración F1 (motor_a_f1.json), y el registro de entradas verificacion_entradas.json: los sellos que el programa mantenga "
    "vigentes siguen; las entradas cambiadas quedan pendientes (extractor «Claude orquestación»), con las discrepancias formales G26, H26 y K26 corregidas "
    "(REVISION_SELLADO.md). Tasa sin riesgo C57 = 0,0337 (Bund a 10 años de la Bundesbank, serie WT1010, 13-nov-2026; CSV oficial de la Release fuentes-examen-20261118 conservado en fuentes_mercado/; antes 0,0334 de Trading Economics) y Palancas!C7 con la tabla de Damodaran (damodaran_margin.xls de la misma Release) como fuente local, por encargo del coordinador del 19-nov-2026. Metadatos de acciones con «impreso» y «escala_impreso» (prompt de metadatos nuevo). Nada adoptado; tasa 9 % provisional; no apto para dinero real.")
conf["origen"] = "personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/ahold_f3/Ahold"
conf["destino"] = "personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/ahold_f4"
conf["base_economica"] = {"fecha": "2025-12-28", "descripcion": (
    "Ejercicio 2025 de Ahold Delhaize (52 semanas, cerrado el 28-dic-2025), la misma base y entradas del FCF base que ahold_f3 (P-O1 (c), P-O2 (a), P-FOSO (a)). "
    "Cambian solo las entradas de juicio LTM y de balance reciente, que pasan del informe del 2T (28-jun-2026) al del 3T (27-sep-2026) por la decisión A-Q3.")}
conf["fechas"] = dict(f3["fechas"], publicacion_fuentes=(
    "Informes anuales 2016–2025 de Ahold Delhaize e informes interinos del 2T (5-ago-2026) y del 3T 2026 (4-nov-2026), páginas oficiales del emisor "
    "(pdf_DESCARGAS_2026.tsv; huellas en INDICE_FUENTES.csv del repositorio auxiliar). LTM y balance reciente: 3T 2026 (27-sep-2026). Precio 13-nov-2026 "
    "(Euronext, fuentes_mercado/); tasa sin riesgo del 13-nov-2026 (Bundesbank, serie WT1010, fuentes_mercado/)."))
conf["conservar"] = list(f3["conservar"]) + ["fuentes_mercado", "verificacion_entradas.json"]
ac = copy.deepcopy(meta3["acciones_diluidas"])
ac["impreso"], ac["escala_impreso"] = "886,877,259", "unidades"
assert "December 28, 2025: 886,877,259" in " ".join(pag(Q3, 21).split())
TSR = {"valor": 0.0337, "fecha": "2026-11-13",
       "fuente": ("Deutsche Bundesbank, serie diaria BBSSY.D.REN.EUR.A630.000000WT1010.A «Daily yield of the current 10 year federal bond» (rendimiento del Bund "
                  "a 10 años de referencia), fila del 2026-11-13, la fecha del precio (C37): 3,37 % → 0,0337. CSV oficial subido por la persona responsable a la Release "
                  "fuentes-examen-20261118 del repositorio auxiliar (asset 766892543, bund_10y_WT1010.csv, SHA-256 fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967; "
                  "última actualización de la serie 2026-11-18 12:31:26), conservado en fuentes_mercado/ con su huella. Sustituye la lectura de Trading Economics de la "
                  "etapa de metadatos (3,34 %, «cierre de octubre», sin fuente conservada). Bund = bono sin riesgo de impago en EUR."),
       "pagina": "fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt, fila 2026-11-13",
       "periodo": "2026-11-13 (fecha del precio)", "unidad": "proporción"}
conf["metadatos"] = {"acciones_diluidas": ac, "tasa_sin_riesgo": TSR}
conf["notas_que_se_retiran"] = [r"C42, C53 y C54 siguen a 28-jun-2026 como en la etapa 1", r"^Tasa sin riesgo: último dato verificable del Bund a 10 años es de finales de octubre de 2026"]
conf["nota_metadatos"] = (
    "(ahold_f4, 19-nov-2026) Decisiones de la persona responsable: A-Q3: las entradas de juicio LTM y de balance reciente (C24, C33, C40, C42, C53, C54; "
    "comprobadas C31 y C34) salen del informe del 3T 2026 (27-sep-2026, publicado el 4-nov-2026, antes del precio del 13-nov-2026); LTM = 2025 + 39 semanas de 2026 − 39 "
    "semanas de 2025. Z-ACC: P-O2 (a) se mantiene (acciones en circulación a 28-dic-2025, 886,877259 M, AR2025 PDF p. 244 y Q3-2026 PDF p. 21; capitalización = "
    "36,05 € × esas acciones = 31.971,9 mm); el balance a 27-sep-2026 ya descuenta las recompras de 2026 (864 pagados; 865.173.863 acciones en circulación a "
    "27-sep-2026, Q3-2026 PDF p. 21): la desalineación de fechas se declara en C40, C41, C42, C53 y C54 (con las acciones a 27-sep-2026, EV/EBITDA "
    f"{float(C42_sep):.3f}x en lugar de {float(C42):.3f}x). A-NIC17: la deuda 2016–2017 (Historia C22 y D22) se deja como se publicó, con los arrendamientos "
    "financieros NIC 17 (2016: 1.761 + 199; 2017: 1.430 + 177), declarado; sin doble cuenta (C23 y D23 = 0, sin NIIF 16). Dilución potencial (≈ 4 M de acciones "
    "condicionales) no incluida. Tasa sin riesgo (C57): 3,37 % del Bund a 10 años de la Bundesbank (serie WT1010) el 13-nov-2026, fecha del precio (fuentes_mercado/, CSV oficial de la Release fuentes-examen-20261118); sustituye el 3,34 % de Trading Economics. (P-O1 (c)) C46, C48 y C49 llevan los cobros que Ahold presenta en inversión (dividendos de negocios conjuntos, intereses cobrados "
    "y cobros de subarriendos), con su cálculo declarado.")
conf["analisis_que_se_conservan"] = {
    "C46": "entrada de ahold_f3 (P-O1 (c), cálculo declarado; cambio_ahold_po1_po2.json) sin cambio: el FCF base sigue con la media 2023–2025 de los ejercicios cerrados; A-Q3 solo mueve las cifras LTM y de balance reciente",
    "C47": "entrada de ahold_f3 (media exacta 2023–2025, precedente E1) sin cambio",
    "C48": "entrada de ahold_f3 (P-O1 (c), cálculo declarado) sin cambio",
    "C49": "entrada de ahold_f3 (P-O1 (c), cálculo declarado) sin cambio",
    "C88": "entrada de ahold_f3 (resultados/recalculo_C40_C42_C88.json: mediana 2019–2025 de capitalización de cierre ÷ FCF con la regla espejo, ejercicios cerrados) sin cambio: no usa el 2T",
    "C96": "entrada de ahold_f3 (resultados/entradas_r3.json: insiders a 28-dic-2025 ÷ acciones a 28-dic-2025, P-O2 a) sin cambio: no usa el 2T"}
conf["analisis_que_se_descartan"] = {}

ev = {}
# ---------- C24
ev["C24"] = {
    "valor": C24,
    "fuente": (f"ROCE antes de impuestos IFRS con fondo de comercio, LTM a 27-sep-2026 ({DEC}; definición de la decisión del inversor del 28-oct-2026, Control maestro "
               "fila 29, M): resultado operativo LTM = 3.542 (AR2025 PDF p. 212) + 2.736 − 2.643 (Q3-26 PDF p. 12, Q3 YTD 2026 y 2025) = 3.635 ÷ capital empleado a "
               "27-sep-2026, la misma fecha que el fin de los doce meses = patrimonio atribuible 14.375 (Q3-26 PDF p. 14) + deuda bruta con arrendamientos 19.747 "
               f"(C54, Q3-26 PDF p. 24) = 34.122 → 0,106530 → {C24} (redondeo a 3 decimales de la etapa 1)"),
    "pagina": "AR2025 PDF p. 212; Q3-26 PDF p. 12, 14 y 24",
    "periodo": "resultado operativo LTM a 27-sep-2026 ÷ capital empleado a 27-sep-2026",
    "unidad": "%", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "derivado de datos publicados (definición de la etapa 1; periodo de A-Q3)",
    "derivacion": "round((EBIT 2025 + resultado operativo 39 semanas 2026 − 39 semanas 2025) ÷ (patrimonio + deuda bruta con arrendamientos a 27-sep-2026), 3)",
    "evidencia": {
        "I": "Cálculo derivado sobre estados auditados 2025 + intermedio Q3-26 (A-Q3)",
        "N": ("[Clase: derivado de datos publicados] (ahold_f4, A-Q3 de la persona responsable, 19-nov-2026) Recalculado con el 3T: 3.635 ÷ 34.122 = 0,1065 → 0,107 "
              "(antes 0,109 con el 2T). La decisión del inversor del 28-oct-2026 (M) fija la definición; su «10,9 %» y su «→ C24 = 0.109» son las cifras del 2T, "
              "sustituidas. Fecha del denominador: 27-sep-2026, el fin de los doce meses y la fecha de C53 y C54. Sensibilidad con otras fechas del capital: a a "
              "28-dic-2025 (14.195 + 18.404 = 32.599) → 0,112; media de 28-dic-2025 y 27-sep-2026 → 0,109; neto de caja (− 3.559) → 0,119. Contexto de la etapa 1: "
              "media ROIC 2021–25 9,0 % IFRS / 9,9 % subyacente; sin fondo de comercio 12,9–13,5 %; WACC de las pruebas de deterioro (EE. UU. 6,7 %, NL 5,0 %) no es "
              "el coste del capital propio. Confianza en la cifra: alta; en la definición: media.")}}
# ---------- C33
ev["C33"] = {
    "valor": C33,
    "fuente": (f"Deuda neta ÷ EBITDA LTM a 27-sep-2026 ({DEC}): (deuda bruta con arrendamientos 19.747, C54, Q3-26 PDF p. 24 − caja 3.559, C53, Q3-26 PDF p. 14) = "
               "16.188 ÷ EBITDA LTM (resultado operativo 3.542 + 2.736 − 2.643 = 3.635; amortizaciones y deterioros del estado de flujos 3.733 + 2.739 − 2.773 = 3.699) "
               f"= 7.334 → 2,207254 → {C33} (redondeo a 4 decimales de la etapa 1)"),
    "pagina": "Q3-26 PDF p. 12, 14, 16 y 24; AR2025 PDF p. 212 y 216",
    "periodo": "deuda y caja a 27-sep-2026; EBITDA LTM a 27-sep-2026",
    "unidad": "x", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "derivado de datos publicados (definición de la etapa 1; periodo de A-Q3)",
    "derivacion": "round((C54 − C53) ÷ (EBIT LTM + amortizaciones y deterioros LTM), 4)",
    "evidencia": {
        "I": "Intermedio Q3-26 + AR2025 (cálculo derivado; A-Q3)",
        "M": "NIIF 16 coherente: (deuda bruta con arrendamientos 19.747 − caja 3.559) = 16.188 ÷ EBITDA LTM a 27-sep-2026 7.334 (resultado operativo 3.635 + amortizaciones y deterioros 3.699) = 2,2073x. Sin híbridos ni preferentes.",
        "N": ("[Clase: derivado de datos publicados] (ahold_f4, A-Q3, 19-nov-2026) Recalculado con el 3T (antes 2,2153 con el 2T). Con el 3T: definición de la empresa "
              "(deuda neta 16.087, que resta también depósitos 15 y el fondo de bonos 86; Q3-26 PDF p. 24) ÷ 7.334 = 2,19x; sin la caja restringida (36): 2,21x; "
              "balance y EBITDA de 2025 ((18.404 − 3.605) ÷ (3.542 + 3.733)): 2,03x. Las demás sensibilidades de la etapa 1 (estrés, sin arrendamientos) eran del 2T y se "
              "retiran. Covenant 5,5:1 solo si el rating baja de BBB/Baa2 (AR2025 p. 54-55). No usa acciones: Z-ACC no le afecta. Confianza alta.")}}
# ---------- C40
ev["C40"] = {
    "valor": C40,
    "fuente": (f"FCF LTM a 27-sep-2026 con la regla espejo (P-O1 c), misma definición que la caja base ({DEC}): CFO 6.731 − capex 2.657 − intereses pagados 265 − "
               f"pagos de arrendamientos 1.956 + dividendos de negocios conjuntos 22 + intereses y dividendos cobrados 128 + cobros de subarriendos 147 = {C40}; cada "
               "partida LTM = 2025 (AR2025 PDF p. 216) + 39 semanas de 2026 − 39 semanas de 2025 (Q3-26 PDF p. 16)"),
    "pagina": "Q3-26 PDF p. 16; AR2025 PDF p. 216",
    "periodo": "12 meses a 27-sep-2026",
    "unidad": "mm", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "derivado de datos publicados (P-O1 c; periodo de A-Q3)",
    "derivacion": "Σ (2025 + Q3 YTD 2026 − Q3 YTD 2025) de CFO, capex, intereses pagados, pagos de arrendamientos, dividendos de negocios conjuntos, intereses cobrados y cobros de subarriendos",
    "evidencia": {
        "I": "Cálculo derivado (estados de flujos AR2025 + intermedio Q3-26)",
        "M": (f"FCF LTM a 27-sep-2026 con la regla espejo (P-O1 c), misma definición que la caja base: CFO 6.731 − capex 2.657 − intereses pagados 265 − pagos de "
              f"arrendamientos 1.956 (= 1.853 sin la regla espejo) + dividendos de negocios conjuntos 22 + intereses y dividendos cobrados 128 + cobros de subarriendos 147 = {C40}; "
              "cada partida LTM = 2025 + 39 semanas de 2026 − 39 semanas de 2025"),
        "N": ("[Clase: derivado de datos publicados] (ahold_f4, A-Q3, 19-nov-2026) Recalculado con el 3T (antes 2.096 con el 2T); sin la regla espejo saldría 1.853. "
              "C76 = 0, así que los intereses cobrados entran (salvaguarda de P-O1). El 3T rotula «Interest and dividend received» la línea que el informe anual y el "
              "2T llaman «Interest received»: es la misma serie (1S 2026 50 + 3T 39 = 89; 1S 2025 76 + 3T 15 = 91) e incluye dividendos de activos financieros, que la "
              "regla espejo también suma. La definición de FCF de la empresa (Q3-26 PDF p. 24) suma además las desinversiones de activos. " + ZACC +
              f": FCF yield con C41 (acciones a 28-dic-2025) {C40 / float(C41):.2%}; con las acciones a 27-sep-2026 (31.189,5 mm) {C40 / float(C41_sep):.2%}. "
              "Semana 53 de 2026 fuera del LTM.")}}
# ---------- C42
ev["C42"] = {
    "valor": float(C42),
    "fuente": (f"EV/EBITDA = (C41 31.971,925 + C54 19.747 − C53 3.559 − negocios conjuntos 254, Q3-26 PDF p. 14) ÷ EBITDA LTM a 27-sep-2026 (3.542 + 2.736 − 2.643 + "
               f"3.733 + 2.739 − 2.773 = 7.334) = 47.905,925 ÷ 7.334 = {float(C42):.6f} ({DEC})"),
    "pagina": "Q3-26 PDF p. 12, 14, 16 y 24; AR2025 PDF p. 212 y 216; Análisis C41, C53 y C54",
    "periodo": "EV con precio del 13-nov-2026, acciones a 28-dic-2025 y balance a 27-sep-2026; EBITDA LTM a 27-sep-2026",
    "unidad": "x", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "derivado de datos publicados (periodo de A-Q3; acciones de P-O2 a, desalineación declarada por Z-ACC)",
    "derivacion": "(C41 + C54 − C53 − inversiones en negocios conjuntos) ÷ (EBIT LTM + amortizaciones y deterioros LTM)",
    "evidencia": {
        "G": "EV: precio 13-nov-2026 × acciones 28-dic-2025 + deuda y caja 27-sep-2026 · EBITDA LTM a 27-sep-2026",
        "J": "Q3-26; AR2025; Análisis C41, C53 y C54",
        "M": f"EV/EBITDA = (C41 31.971,925 + C54 19.747 − C53 3.559 − negocios conjuntos 254) ÷ EBITDA LTM 7.334 = 47.905,925 ÷ 7.334 = {float(C42):.6f}",
        "N": ("[Clase: derivado de datos publicados] (ahold_f4, A-Q3, 19-nov-2026) Recalculado con el 3T (antes 6,590310 con el 2T). " + ZACC +
              f": con las acciones a 27-sep-2026 (36,05 × 865,173863 = 31.189,518) saldría {float(C42_sep):.6f}. Misma definición de EBITDA que C33.")}}
# ---------- C53 / C54
ev["C53"] = {
    "valor": C53,
    "fuente": f"Caja y equivalentes a 27-sep-2026, balance consolidado del informe del 3T 2026 ({DEC}): «Cash and cash equivalents 8 3,559 3,605»",
    "pagina": "Q3-26 PDF p. 14", "periodo": "saldo a 27-sep-2026", "unidad": "mm", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "dato publicado (A-Q3)",
    "evidencia": {
        "G": "27-sep-2026", "J": "Informe Q3 2026", "L": "Q3-26 PDF p. 14",
        "M": "Caja y equivalentes 3.559 a 27-sep-2026 (28-dic-2025: 3.605). Incluye 36 de caja restringida y 1.176 de cash pool nocional, compensado por un importe igual en la deuda a corto (Q3-26 PDF p. 21 y 24).",
        "N": ("(ahold_f4, A-Q3, 19-nov-2026) Antes 3.196 (2T). " + ZACC + ". El dividendo a cuenta de 0,51 € se pagó el 27-ago-2026 (Q3-26 PDF p. 21), "
              "antes del balance. Confianza alta.")}}
ev["C54"] = {
    "valor": C54,
    "fuente": f"Deuda bruta con arrendamientos a 27-sep-2026, cuadro «Net debt» de la nota 12 del informe del 3T 2026 ({DEC}): «Gross debt 19,747 19,261 18,404»",
    "pagina": "Q3-26 PDF p. 24", "periodo": "saldo a 27-sep-2026", "unidad": "mm", "vaciar_en_etapa1": True, "fecha": "2026-09-27",
    "naturaleza": "dato publicado (A-Q3)",
    "evidencia": {
        "G": "27-sep-2026", "J": "Informe Q3 2026", "L": "Q3-26 PDF p. 24", "I": "Conciliación de deuda neta del intermedio (nota 12)",
        "M": "Deuda bruta con arrendamientos 19.747 (préstamos no corrientes 4.854 + arrendamientos no corrientes 10.572 + deuda a corto y porción corriente de deuda y arrendamientos 4.321), Q3-26 PDF p. 24. Incluye 1.176 de cash pool compensado en la caja. Solo contexto.",
        "N": ("(ahold_f4, A-Q3, 19-nov-2026) Antes 19.261 (2T). La porción corriente de los arrendamientos no se publica en el 3T (a 28-dic-2025 era 1.448, AR2025). "
              + ZACC + ". Confianza alta.")}}
conf["analisis"] = ev
for k, d in ev.items():
    assert d.get("vaciar_en_etapa1") and d.get("evidencia")
conf["evidencia"] = {
    "Análisis!C31": {
        "G": "12 meses a 27-sep-2026 (variaciones del estado de flujos) · ventas: 39 semanas de 2026",
        "I": "Intermedio Q3-26 (estado de flujos) + AR2025 (A-Q3)", "J": "Informe Q3 2026; AR2025", "L": "Q3-26 PDF p. 3 y 16; AR2025 PDF p. 216",
        "N": ("(ahold_f4, A-Q3 de la persona responsable, 19-nov-2026) Comprobado con el 3T; el valor «Sí» no cambia. El 3T no publica el balance de sep-2025, así que la "
              "comparación interanual del 2T de la etapa 1 no se repite; se usan las variaciones del estado de flujos (sin divisa ni adquisiciones), 2025 + 39 semanas "
              "de 2026 − 39 semanas de 2025: cobros y otros activos corrientes −91 + 83 − 128 = −136 (aumentan 136, ≈ +4,7 % sobre 2.904 = 2.659 + 381 − 136 a "
              "27-sep-2026) e inventario −158 − 42 + 258 = +58 (bajan 58, ≈ −1,2 %), frente a ventas +1,9 % a tipo constante en las 39 semanas (Q3-26 PDF p. 3). Lectura "
              "literal de la decisión del inversor («cobros o inventario», M): «Sí»; económica (inventario): «No». La línea de cobros incluye otros activos corrientes; "
              "aproximación declarada. Confianza media.")},
    "Análisis!C34": {
        "G": "27-sep-2026 (balance del 3T 2026)",
        "I": "Intermedio Q3-26 (balance y deuda neta; A-Q3)", "J": "Informe Q3 2026; AR2025", "L": "Q3-26 PDF p. 14, 16, 21 y 24",
        "N": ("(ahold_f4, A-Q3, 19-nov-2026) Comprobado con el 3T; el valor «No» no cambia. Con el criterio de la decisión del inversor (M: deuda a corto con los "
              "arrendamientos corrientes): caja 3.559 (p. 14) ÷ préstamos a corto y porción corriente de deuda y arrendamientos 4.321 (p. 24) = 0,82x → «No» (con el 2T, "
              "0,87x). Sin el cash pool nocional de 1.176, que está en los dos lados (p. 21 y 24): 2.383 ÷ 3.145 = 0,76x. Sin arrendamientos corrientes (no publicados en "
              "el 3T; 1.448 a 28-dic-2025, estimación): caja no restringida 3.523 ÷ ≈ 2.873 ≈ 1,2x («Sí» en la lectura sin arrendamientos, que la decisión descartó). "
              "La deuda a corto sube de 3.301 (28-dic-2025) a 4.321, con 1.292 de aumento neto de préstamos a corto en 39 semanas (p. 16). Confianza media-alta.")},
    "Análisis!C25": {
        "M": ("Evidencia (pkg_FIN): FCF del accionista sin circulante 1.136 (2021) → 2.149 (2022) → 2.041 → 2.059 → 1.911 (2025) → 1.725 (LTM a 27-sep-2026, 3T 2026: "
              "FCF sin la regla espejo 1.853 − circulante 128; A-Q3, ahold_f4; con el 2T era 1.813): escalón en 2022 y meseta. Crecimiento 2021–25: +12,4%/año sin ajustar "
              "frente a ~3% normalizado; 2022–25 plano o negativo. Definición de la empresa: 1.618 → 2.600 (2021–25); guía de 2026 actualizada el 4-nov-2026: unos 2.100 "
              "(Q3-26). Por acción crece por las recompras.")},
    "Análisis!C27": {
        "M": ("Evidencia (pkg_OPS): margen operativo subyacente (la métrica menos distorsionada) 4,0–4,4% desde 2018 (sin el 4,8% de 2020); 4,04% en 2024–25 y 4,07% LTM a "
              "27-sep-2026 (3.734, AR2025 PDF p. 42, + 2.748 − 2.740 = 3.742 ÷ ventas 92.352 + 68.529 − 68.862 = 92.019; Q3-26 PDF p. 3 y 25; A-Q3, ahold_f4; con el 2T era 4,08%). "
              "Pendiente 2021–25: −0,10 pp/año; margen bruto 27,36 → 26,54%; EBITDA subyacente 8,4 → 7,9%. Interpretación: \"Estable\" como base; \"Comprimiendo\" como "
              "alternativa conservadora.")},
    "Análisis!C76": {
        "G": "27-sep-2026", "I": "Balance intermedio Q3-26 (evidencia preparada; A-Q3)", "J": "Q3-26; pkg_BAL", "L": "Q3-26 PDF p. 14, 21 y 24",
        "M": ("Evidencia (3T 2026, ahold_f4, A-Q3): caja 3.559; restringida 36; cash pool nocional 1.176 compensado por un importe igual en la deuda a corto; deuda neta "
              "con arrendamientos 16.188 (19.747 − 3.559; la de la empresa, que resta también depósitos y el fondo de bonos, 16.087). Caja sin restringida ni cash pool "
              "≈ 2.347, menor que la deuda a corto sin el cash pool (3.145). Recomendación de la etapa 1 (hecha con el 2T): vacío (= 0). Decide el inversor.")}}
conf["control_maestro_textos"] = {
    "F5": "3 años FY2023–2025 (decisión del inversor de la etapa 1, 28-oct-2026; C46–C50 con cálculo declarado); LTM y balance reciente a 27-sep-2026 (3T 2026, A-Q3)",
    "D88": ("Medias del DCF: FY2023–2025 (C46–C50). LTM a 27-sep-2026 (2025 + 39 semanas de 2026 − 39 semanas de 2025, informe del 3T del 4-nov-2026; A-Q3) en C24, C33, "
            "C40 y C42; balance a 27-sep-2026 en C53 y C54; precio 13-nov-2026 (C37); acciones en circulación a 28-dic-2025 (C55 = 886,877259 M, P-O2 a): "
            f"desalineación de fechas declarada en C40, C41, C42, C53 y C54 (Z-ACC; con las acciones a 27-sep-2026, EV/EBITDA {float(C42_sep):.2f}x).")}
# los dos primeros patrones de ahold_f3 se afinan para no contar las citas entre comillas « » con que las entradas P-O1 (c) conservadas
# dicen qué decisión sustituyen (filas 43, 45 y 46 del Control maestro); siguen detectando el texto activo de la decisión anterior
PROH_F3 = {"no se suman \\(sensibilidad\\)": r"no se suman \(sensibilidad\)(?!»)", "solo como sensibilidad": r"intereses recibidos[^»]{0,40}solo como sensibilidad(?!»)"}
assert set(PROH_F3) <= set(f3["textos_prohibidos"]), f3["textos_prohibidos"]
conf["textos_prohibidos"] = [PROH_F3.get(x, x) for x in f3["textos_prohibidos"]] + [
    r"FCF LTM a 28-jun-2026", r"7\.252", r"16\.065", r"1\.813 \(LTM\)", r"4,08% LTM", r"6\.590310", r"6,590310 \(", r"Gross debt 19,261",
    r"C42, C53 y C54 siguen a 28-jun-2026", r"LTM a 28-jun-2026", r"Deuda: 28-jun-2026", r"3,34 % a cierre de octubre de 2026"]
conf["alcance"] = dict(f3["alcance"])
conf["alcance"]["aviso"] = (
    "EXAMEN DEL PERSONAJE · AHOLD DELHAIZE (caso F1, arrendamientos) · expediente ahold_f4 · plantilla V6.3.1 F1 con el código de examen/expedientes-f1. Mismas "
    "entradas del FCF base que ahold_f3: P-O1 (c) «regla espejo» (C46 + dividendos de negocios conjuntos; C48 intereses netos; C49 alquileres netos de subarriendos; "
    "SALVAGUARDA: si C76 suma caja, sus intereses salen de C48), P-O2 (a) (acciones en circulación a 28-dic-2025, 886,877 M) y P-FOSO (a) (serie de intereses de "
    "arrendamiento 2021–2025 para la vara del foso en A2_propio). Nuevo (19-nov-2026): A-Q3: LTM y balance reciente del informe del 3T 2026 (27-sep-2026; publicado el "
    f"4-nov-2026): C24 {C24}, C33 {C33}, C40 {C40}, C42 {float(C42):.4f}, C53 {C53}, C54 {C54}; Z-ACC: acciones al cierre de 2025 con el balance de sep-2026 "
    "(desalineación declarada en C40–C42, C53, C54); A-NIC17: deuda 2016–2017 con arrendamientos financieros NIC 17, declarada. Ejercicio 2025 cerrado el 28-dic-2025. "
    "Tasa 9 % provisional, sin decidir. Precio 36,05 € (13-nov-2026); tasa sin riesgo 3,37 % (Bundesbank WT1010, 13-nov-2026). Nada adoptado; no apto para dinero real.")
conf["alcance"]["fuente"] = (f3["alcance"]["fuente"] + " · DECISIONES_PARA_EL_USUARIO.md (coordinacion/cierre-v2), «19-nov-2026 (mañana)»: A-Q3, A-NIC17 y Z-ACC; "
                             "examen/ahold/revision_registro/REVISION_SELLADO.md; configuracion/cambio_ahold_f4.json.")
conf["alcance"]["fecha"] = "2026-11-19"
orden = ["tipo", "version_formato", "empresa", "_estado_del_archivo", "origen", "destino", "base_economica", "fechas", "conservar", "fuentes_adicionales", "metadatos",
         "notas_que_se_retiran", "nota_metadatos", "analisis", "analisis_que_se_conservan", "analisis_que_se_descartan", "evidencia", "control_maestro_textos",
         "textos_prohibidos", "alcance", "configuracion_economica", "entrada_efectiva"]
assert set(orden) == set(conf), set(conf) ^ set(orden)
out = os.path.join(BASE, "configuracion/cambio_ahold_f4.json")
if os.path.exists(out) and "--forzar" not in sys.argv:
    raise SystemExit(f"ya existe {out}")
json.dump({k: conf[k] for k in orden}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("escrito", out)
