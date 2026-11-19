#!/usr/bin/env python3
"""zoetis_t1d · genera configuracion/cambio_zoetis_t1d.json desde zoetis_t1c (que no se toca), por encargo del coordinador (19-nov-2026).
Reutiliza literalmente los textos vigentes de zoetis_t1c (entradas_r3.json, fase1_metadatos.json) y cambia solo lo que el encargo pide.
Uso: python3 -I generar_cambio_zoetis_t1d.py RAIZ_munger_v2_r1 SALIDA.json"""
import copy, json, os, sys
from fractions import Fraction as F

RAIZ, SAL = sys.argv[1:3]
EX = "personaje_v2/empresas_v2_correcciones/2026-11_examen_universo"
T1C = os.path.join(RAIZ, EX, "zoetis_t1c")
meta = json.load(open(os.path.join(T1C, "Zoetis", "fase1_metadatos.json"), encoding="utf-8"))
r3 = json.load(open(os.path.join(T1C, "resultados", "entradas_r3.json"), encoding="utf-8"))["declarar"]
c1c = json.load(open(os.path.join(RAIZ, EX, "configuracion", "cambio_zoetis_t1c.json"), encoding="utf-8"))

ACC = F("424.927535")
PRECIO = F("73.08")
CAP = PRECIO * ACC                      # 31.053,7042578 exacto
assert CAP == F("31053.7042578")
EV = CAP + 9048 - 1476
C42 = float(EV / 3992)                  # 9,675777619689379
C42_JUN = float((PRECIO * F("414.154046") + 7572) / 3992)
assert abs(meta["analisis"]["C33"]["valor"] - 7572 / 3992) < 1e-15 and meta["analisis"]["C40"]["valor"] == 2363

import openpyxl  # noqa: E402
_cm = openpyxl.load_workbook(os.path.join(T1C, "Zoetis", "etapa1", "Zoetis_evaluada.xlsx"), data_only=True)["Control maestro"]
_f = [r for r in range(17, 83) if _cm[f"B{r}"].value == "Análisis!C38"]
assert len(_f) == 1 and _cm[f"F{_f[0]}"].value == "Rellenado y verificado"
N_C38 = _cm[f"N{_f[0]}"].value
assert N_C38.startswith("Captura previa: 202,45")
assert _cm["F5"].value.startswith("Pendiente de inversor: media FY23–25") and _cm["D90"].value.startswith("C46, C47, C50 y C51 pendientes de inversor")
CLASE_ANT = "[Clase: derivado de datos publicados, aproximado]"
CLASE = ("[Clase: convención · aproximación declarada (no es un derivado exacto: en el registro de entradas es «convencion» con su justificacion_clase, "
         "como C24; zoetis_t1d, sellado del registro de zoetis_t1c)]")
ZACC = ("DESALINEACIÓN DE FECHAS declarada (decisión Z-ACC de la persona responsable, 19-nov-2026: se mantienen las acciones al cierre del ejercicio, P-O2): "
        "precio del 8-oct-2026 × 424.927.535 acciones en circulación al 31-dic-2025 (10-K 2025 PDF p. 68), deuda y caja del balance del 30-jun-2026 y "
        "EBITDA de los 12 meses a 30-jun-2026; con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 PDF p. 5) saldría " + f"{C42_JUN:.2f}".replace(".", ",") + "x.")


def n_nuevo(c, extra):
    n = r3[c]["N"]
    assert n.startswith(CLASE_ANT), c
    return CLASE + n[len(CLASE_ANT):] + " " + extra


M42 = ("EV ÷ EBITDA TTM = (C41 31.053,7042578 = 73,08 × 424,927535 (valor exacto, sin redondear las acciones) + deuda 9.048 − caja 1.476 (10-Q T2 2026 p. 5)) "
       "÷ EBITDA TTM a 30-jun-2026 = BAI (3.360 − 1.712 + 1.624 = 3.272) + gasto por intereses (222 − 107 + 123 = 238) + D&A (487 − 243 + 238 = 482) = 3.992 "
       "(EBIT = BAI + intereses) = 38.625,7042578 ÷ 3.992 = 9,675778")
assert f"{C42:.6f}" == "9.675778"
N42 = n_nuevo("C42", ZACC + " En zoetis_t1c salía 0,000008x más alto (C41 calculado con las acciones redondeadas a tres decimales).")
N33 = n_nuevo("C33", "Sin acciones ni precio: no le afecta la desalineación de C41 y C42 (deuda neta del 30-jun-2026 y EBITDA de 12 meses a esa fecha).")
N40 = n_nuevo("C40", "Sin acciones ni precio: no le afecta la desalineación de C41 y C42 (12 meses a 30-jun-2026).")

analisis = {}
for c, valor, m_, n_ in (("C42", C42, M42, N42), ("C33", meta["analisis"]["C33"]["valor"], r3["C33"]["M"], N33), ("C40", 2363, r3["C40"]["M"], N40)):
    analisis[c] = {"valor": valor, "fuente": m_, "pagina": r3[c]["L"], "periodo": r3[c]["periodo"], "unidad": r3[c]["unidad"], "vaciar_en_etapa1": True,
                   "naturaleza": "aproximación declarada por la «Fiscal Year Alignment» (convención de la orquestación; no derivado exacto)",
                   "fecha": "2026-06-30",
                   "derivacion": "TTM = 2025 (10-K, base antigua) − 6M-2025 + 6M-2026 (10-Q T2 2026)" + (" ; EV con C41 = C37 × C55 exactos" if c == "C42" else ""),
                   "evidencia": {"L": r3[c]["L"], "M": m_, "N": n_}}

acciones = {
    "valor": float(ACC), "unidad": "millones de acciones", "impreso": "424,927,535", "escala_impreso": "unidades", "fecha": "2025-12-31", "pagina": 68,
    "fuente": ("Balance consolidado del 10-K FY2025 (PDF p. 68): «Common stock, $0.01 par value: 6,000,000,000 authorized, 501,891,243 and 501,891,243 shares issued; "
               "424,927,535 and 448,473,073 shares outstanding at December 31, 2025 and 2024» → 424.927.535 acciones en circulación al 31-dic-2025 (emitidas menos "
               "76.963.708 de autocartera) = 424,927535 millones, valor exacto (un número de acciones no es un importe: no se redondea). No se suma dilución "
               "(sin «dilucion»): las opciones/RSU antidilutivas no son materiales y el 10-K no publica dilución al cierre; las notas convertibles (precio de "
               "conversión ≈148,20 USD, con capped calls) están muy fuera de dinero frente a 73,08 USD. Cifra de cierre del ejercicio, no media ponderada "
               "(P-O2; Z-ACC, 19-nov-2026: se mantiene y la desalineación con el precio del 8-oct-2026 se declara en cada cifra que las combina)."),
}
precio = dict(meta["precio"])
assert precio["valor"] == 73.08 and precio["fecha"] == "2026-10-08"
precio["fuente"] = ("Cierre del 8-oct-2026 en NYSE (ZTS) = 73,08 USD, de la página oficial de la empresa: investor.zoetis.com, «Stock Information» → «Historical "
                    "Stock Quote», Lookup Date 2026 Oct 8: Day's Open $71.36, Closing Price $73.08, Intraday Low $71.15, Intraday High $73.75, Volume 6,176,469. "
                    "Bytes: captura de pantalla entregada por la persona responsable el 19-nov-2026 (RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 ter; SHA-256 c1871f7e80e1f46015912a0cc585292bc9186e2fad95db5d8ef98bbe632c1530), "
                    "conservada en fuentes_mercado/Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.png con su transcripción. Cierre del día, sin hora intradía. "
                    "Sustituye a stockanalysis.com y MarketBeat (terceros) como fuente.")
assert meta["acciones_diluidas"]["pagina"] == 68 and abs(meta["acciones_diluidas"]["valor"] - 424.928) < 1e-12
capitalizacion = {
    "valor": float(CAP), "fecha": "2026-10-08",
    "fuente": ("Precio de cierre 73,08 USD (8-oct-2026; investor.zoetis.com, «Historical Stock Quote», captura conservada en fuentes_mercado/) × 424,927535 millones de acciones en circulación al 31-dic-2025 = 31.053,7042578 millones de USD, "
               "producto exacto (sin redondear las acciones ni el resultado). DESALINEACIÓN DE FECHAS declarada (Z-ACC, 19-nov-2026): precio del 8-oct-2026 "
               "y acciones al cierre del ejercicio (P-O2); con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 p. 5) sería 30.266,37768168. "
               "(zoetis_t1d: en zoetis_t1c la capitalización se calculó con las acciones redondeadas a tres decimales, 0,034 mm más.)"),
}
tasa = {
    "valor": 0.0522,
    "fuente": ("Treasury de EE. UU. a 10 años, Daily Treasury Par Yield Curve Rates del Departamento del Tesoro, cierre del 8-oct-2026: 5,22 % (fila «10/08/2026», "
               "columna «10 Yr»). Bytes: CSV oficial us_treasury_par_yield_2026.csv subido por la persona responsable a la Release fuentes-examen-20261118 "
               "(asset 766892834, SHA-256 0707733bdc20fce9a21a1063c5b99dbfd3456acabb216f73e6d6b798f511243d), conservado en "
               "fuentes_mercado/US_Treasury_par_yield_2026_Release_766892834.csv. Moneda del modelo USD; el Treasury se toma como libre de riesgo de impago."),
}
assert meta["tasa_sin_riesgo"]["valor"] == 0.0522

conf = {
    "tipo": "cambio_de_base", "version_formato": 1, "empresa": "Zoetis",
    "_estado_del_archivo": (
        "Examen del personaje (19-nov-2026), Zoetis primer tiempo. Expediente nuevo zoetis_t1d desde zoetis_t1c/Zoetis (que no se toca), sobre la rama "
        "examen/expedientes-f1 (cabeza ≥ 6242bda: código con las acciones exactas de los metadatos, producto/minoritarios-acciones, y con los minoritarios "
        "impresos en negativo → 0 con aviso, producto/minoritarios-cero; revisiones coordinacion/cierre_v2/examen/revisiones/{minoritarios_acciones,"
        "minoritarios_cero}/REVISION.md del repositorio auxiliar, conformes). POR QUÉ un expediente nuevo: (1) el sellado del registro de entradas de "
        "zoetis_t1c (coordinacion/cierre_v2/examen/zoetis/revision_registro/REVISION_SELLADO.md, 4743cb0) confirma discrepancias que cambian valores del "
        "libro: C55 guardaba 424,928 (redondeo de 424.927.535 acciones) y C41 = 73,08 × 424,928 = 31.053,73824; ahora C55 = 424,927535 exacto (metadatos con "
        "«impreso» y «escala_impreso», sin dilución) y C41 = C37 × C55 = 31.053,7042578 sin redondear, y C42 = 9,675778 con ese C41; Historia I26 y J26 "
        "(minoritarios impresos (2) y (6)) pasan de +2 y +6 a 0 por la decisión Z-MIN (código integrado); Historia E26 pasa de vacío a 0, el «—» impreso en "
        "el 10-K 2018 (PDF p. 73), con una corrección registrada de fase1_partes/AR_2018.json; (2) decisiones de la persona responsable del 19-nov-2026 "
        "(DECISIONES_PARA_EL_USUARIO.md): Z-ACC (se mantienen las acciones al cierre, P-O2, y se declara la desalineación de fechas en C41 y C42), Z-R (la "
        "agrupación geográfica de Palancas A31/B31 y A33/B33 se deja y se anota la diferencia con las etiquetas del informe) y Z-MIN; (3) datos de mercado "
        "con bytes de la Release fuentes-examen-20261118 (anexo 3): C57 = 5,22 % del CSV oficial del Tesoro (asset 766892834) y Palancas!C7 de "
        "damodaran_margin.xls (asset 766892761), conservados en fuentes_mercado/ con su huella. C37 = 73,08 USD con la captura de "
        "investor.zoetis.com («Historical Stock Quote», 2026-Oct-8) entregada por la persona (anexo 3 ter), conservada en fuentes_mercado/ con su huella, en vez de stockanalysis/MarketBeat. C33, C40 y C42 se registran "
        "como convención/aproximación declarada por la «Fiscal Year Alignment» (no como derivado exacto); C33 y C40 conservan su valor. Se conserva todo lo "
        "demás vigente de zoetis_t1c: US GAAP, D-US1, fila 23 solo con arrendamientos financieros, EBIT = BAI + intereses, guía del 6-ago-2026, PPA como cota "
        "superior, C46/C47/C49/C50 con su cálculo declarado, C48 = 0, motor_a_f1.json, extracto_v63.md (mismas fuentes) y el registro "
        "verificacion_entradas.json, cuyas entradas corregidas por «Claude orquestación» quedan PENDIENTES de otro revisor (las selladas que no cambian "
        "conservan su sello solo si el programa mantiene vigente su vínculo). Tasa 9 % provisional. Nada adoptado; no apto para dinero real."),
    "origen": f"{EX}/zoetis_t1c/Zoetis",
    "destino": f"{EX}/zoetis_t1d",
    "base_economica": {"fecha": "2025-12-31", "descripcion": (
        "Ejercicio 2025 de Zoetis (cerrado el 31-dic-2025), la misma base, fuentes y entradas declaradas que zoetis_t1c (primer tiempo: nada publicado después "
        "del 9-oct-2026). Cambios: C55 exacto (424,927535), C41 = C37 × C55 sin redondear, C42 con ese C41, minoritarios 2022–2023 a 0 (Z-MIN) y 2018 = 0 "
        "(«—» impreso), y C37, C57 y Palancas!C7 con bytes oficiales (captura de investor.zoetis.com y Release).")},
    "fechas": {"ejecucion": "2026-10-09", "precio": "2026-10-08", "acciones": "2025-12-31",
               "publicacion_fuentes": c1c["fechas"]["publicacion_fuentes"] + (
                   " Datos de mercado (19-nov-2026, Release fuentes-examen-20261118, anexo 3): CSV oficial del Tesoro de EE. UU. (curva par diaria 2026, asset "
                   "766892834) y damodaran_margin.xls (enero 2026, asset 766892761), subidos por la persona responsable; precio: captura de investor.zoetis.com «Historical Stock Quote» del 8-oct-2026 entregada por la persona (anexo 3 ter).")},
    "conservar": ["etapa1", "texto", "fase1_partes", "fase1_fuentes.json", "pdf", "FUENTES.tsv", "fase1_listas.md", "extracto_v63.md", "motor_a_f1.json",
                  "fuentes_mercado", "verificacion_entradas.json"],
    "fuentes_adicionales": [],
    "metadatos": {"precio": precio, "acciones_diluidas": acciones, "capitalizacion": capitalizacion, "tasa_sin_riesgo": tasa},
    "notas_que_se_retiran": [r"^La hora de cierre del precio y del Treasury no figura en las fuentes", r"^Las cifras de la etapa 1 \(p\. ej\. precio 73,08\) no se copiaron"],
    "nota_metadatos": (
        "(zoetis_t1d, 19-nov-2026) La hora de cierre del precio y del Treasury no figura en las fuentes (cierre del día). El Treasury a 10 años (5,22 % el "
        "8-oct-2026) se contrasta ahora con el CSV oficial del Tesoro subido por la persona responsable a la Release fuentes-examen-20261118 (asset 766892834, "
        "conservado en fuentes_mercado/ con su huella). El precio 73,08 USD (cierre del 8-oct-2026) sale de la página oficial de la empresa (investor.zoetis.com, "
        "«Historical Stock Quote»): captura entregada por la persona responsable (anexo 3 ter), conservada en fuentes_mercado/ con su huella; no se copió de "
        "la etapa 1 (coincide con ella). Z-ACC: acciones al cierre del ejercicio (P-O2) con precio del 8-oct-2026, desalineación declarada en C41 y C42. "
        "Z-R (19-nov-2026): se deja la agrupación geográfica de la r mínima; «Región · Asia» incluye «Other emerging markets» (913 mm, que no son solo Asia) y "
        "«Región · Australia & New Zealand» incluye «Other developed markets» (641 mm) y «Contract manufacturing & human health» (116 mm): las etiquetas del "
        "modelo no son las del informe (10-K 2025 PDF p. 77)."),
    "analisis": analisis,
    "analisis_que_se_conservan": {
        c: f"entrada de zoetis_t1c sin cambio (cambio_zoetis_t1.json → cambio_zoetis_t1c.json): las acciones exactas, los minoritarios y los datos de mercado no cambian {c}"
        for c in ("C46", "C47", "C49", "C50")},
    "analisis_que_se_descartan": {},
    "evidencia": {"Análisis!C38": {"F": "Dato no verificable", "N": (
        "NO VERIFICABLE (zoetis_t1d, 19-nov-2026): valor intrínseco de un tercero (Simply Wall St) sin bytes en el expediente; lectura externa que el "
        "registro de entradas no cuenta como comprobada (REVISION_SELLADO.md de zoetis_t1c). Solo contexto, no dato. Texto de la etapa 1: " + N_C38)}},
    "control_maestro_textos": {
        "F5": ("FY2023–FY2025 (media de 3 años) en C46, C47 y C50 (decisión del inversor del 18-oct-2026, Control maestro M43, M44 y M48); TTM a 30-jun-2026 "
               "solo en C33, C40 y C42 (aproximación declarada por la «Fiscal Year Alignment»). (zoetis_t1d: sustituye el texto de la etapa 1 «Pendiente de "
               "inversor: media FY23–25 / media FY21–25 / TTM a 30-jun-2026».)"),
        "D90": ("C46 = 2.736,667, C47 = 669,333 y C50 = 72,333 (media FY23–25, cálculo declarado); C48 = 0 (US GAAP: intereses pagados dentro del CFO; cero "
                "de la Historia pendiente de verificación H1) y C49 = 1,000 (principal de arrendamientos financieros —/1/2, 10-K 2025 PDF p. 89); C51 la decide "
                "la fase A. (zoetis_t1d: sustituye el texto de la etapa 1 «C46, C47, C50 y C51 pendientes de inversor; C48 y C49 vacíos (US GAAP; inmaterial)».)")},
    "textos_prohibidos": [r"31[.,]?053[.,]73824", r"9[.,]675786", r"73,08 × 424,928\b", r"424,928 \(C55", r"stockanalysis\.com \(historial de ZTS", r"MarketBeat \(https"],
    "alcance": None,
    "configuracion_economica": None,
    "entrada_efectiva": {"modo": "estricta", "motivo": "expediente nuevo de la 4.15 (modo por defecto)"},
}
al = copy.deepcopy(c1c["alcance"])
al["aviso"] = (
    "EXAMEN DEL PERSONAJE · ZOETIS (caso del examen: primer tiempo, información hasta el 9-oct-2026, precio de cierre del 8-oct de la etapa 1) · plantilla "
    "V6.3.1 F1 (config_v2_v631_f1.json) con el código de examen/expedientes-f1 (acciones exactas de los metadatos; minoritarios impresos en negativo → 0, "
    "Z-MIN). Expediente zoetis_t1d (cambio_zoetis_t1d.json) desde zoetis_t1c, y antes zoetis_t1b. Etapa 1 de la persona responsable (Zoetis_evaluada.xlsx "
    "c33f17d1…5093, Zoetis_respuesta.md 7f29de8e…d0a1). Fuentes oficiales con huella en la Release fuentes-examen-20261118 (FUENTES.tsv): Form 10-K "
    "2016–2025, Form 10-Q del T1 y del T2 de 2026 y, por decisión de la persona responsable (18-nov-2026), comunicado, presentación y conferencia de resultados "
    "del T2 2026 publicados el 6-ago-2026, con la guía 2026 revisada (guía de la dirección, no hecho); nada publicado después del 9-oct-2026 entra. US GAAP: "
    "F1 con D-US1 y D-US2 (D-WM no aplica). Fila 23 solo con arrendamientos financieros; fila 17 de 2025 = 2. C46/C47/C50 exactas con cálculo declarado; "
    "C49 = 1,0; C48 = 0. P-O1 (c). P-O2 (a) y Z-ACC: 424,927535 M acciones a 31-dic-2025 (exactas), precio del 8-oct-2026 y desalineación declarada en C41 "
    "(31.053,7042578) y C42. C33, C40 y C42: aproximación declarada por la «Fiscal Year Alignment». Z-R: agrupación geográfica de la r mínima sin cambios, con la "
    "diferencia anotada. Minoritarios 2022–2023 impresos (2) y (6) → 0 (Z-MIN). Tasa sin riesgo 5,22 % del CSV oficial del Tesoro (Release, anexo 3). Precio "
    "73,08 USD: captura de investor.zoetis.com del 8-oct-2026 conservada en fuentes_mercado/ (anexo 3 ter). Tasa 9 % provisional, sin decidir. Nada adoptado; no apto "
    "para dinero real.")
al["fuente"] = al["fuente"] + (" · configuracion/cambio_zoetis_t1d.json; DECISIONES_PARA_EL_USUARIO.md, «19-nov-2026 (mañana)»: Z-ACC, Z-R, Z-MIN; "
                               "examen/zoetis/revision_registro/REVISION_SELLADO.md; examen/revisiones/{minoritarios_acciones,minoritarios_cero}/REVISION.md; "
                               "RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexos 3 y 3 bis.")
al["fecha"] = "2026-11-19"
conf["alcance"] = al
json.dump(conf, open(SAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("C41", float(CAP), "C42", C42, "C42 con acciones de junio", C42_JUN)
print(M42)
