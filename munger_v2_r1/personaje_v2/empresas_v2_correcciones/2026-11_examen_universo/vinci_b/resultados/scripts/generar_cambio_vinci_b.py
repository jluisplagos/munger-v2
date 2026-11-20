#!/usr/bin/env python3
"""vinci_b · genera configuracion/cambio_vinci_b.json (encargo del coordinador, 20-nov-2026).
Parte de la receta del autor de la normalización del circulante (rama f1/circulante-normalizado,
2026-11_Vidrala_ensayo_4_15/f1_circulante/resultados/ensayo_vinci_b/cambio_vinci_b.propuesta.json), que es cambio_vinci.json con el origen
vinci/Vinci, el destino vinci_b, extracto_v63.md y motor_a_f1.json conservados y las 8 entradas `analisis` conservadas. Sobre ella cambia SOLO
los datos de mercado que el encargo pide, ahora con bytes oficiales (que se conservan en fuentes_mercado/ con su huella):
  - C57 = 3,47 % (Bundesbank, serie WT1010, fila 2026-10-09; bund_10y_WT1010.csv, asset 766892543, fef9498e…), antes 3,486 % de Investing (etapa 1);
  - C37 = 107,05 € sin cambio de valor, con la exportación de Euronext de la persona (VINCI_historical_price.xls, 78eee9c5…), antes «pendiente
    de verificación»; C41 sin cambio de valor (producto exacto), con la fuente del precio actualizada;
  - los textos que decían «pendiente de verificación» (fechas, alcance, D88, nota de los metadatos).
Comprueba las huellas de los archivos de la persona y las filas usadas antes de escribir.
Uso: python3 -I generar_cambio_vinci_b.py PROPUESTA.json DIR_MERCADO_PERSONA SALIDA.json"""
import copy, hashlib, json, os, sys
from fractions import Fraction as F

PROP, MP, SAL = sys.argv[1:4]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
assert h(os.path.join(MP, "bund_10y_WT1010.csv")) == "fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967"
assert h(os.path.join(MP, "VINCI_historical_price.xls")) == "78eee9c5d6b1e0402ab9bf8979a5f2d19c09acf3d861bca9e9427ebe305afb9d"
assert "\n2026-10-09,3.47,\n" in open(os.path.join(MP, "bund_10y_WT1010.csv"), encoding="utf-8-sig").read()
p = json.load(open(PROP, encoding="utf-8"))
c = copy.deepcopy(p)
ACC, PRECIO = F("555.967094"), F("107.05")
CAP = ACC * PRECIO
assert CAP == F("59516.2774127")

c["_estado_del_archivo"] = (p["_estado_del_archivo"] + " (vinci_b, Claude orquestación, 20-nov-2026) Además, datos de mercado con bytes oficiales "
    "(encargo del coordinador): C57 = 3,47 % (Bundesbank WT1010, 9-oct-2026; antes 3,486 % de Investing en la etapa 1) y C37 = 107,05 € "
    "verificado en la exportación de Euronext entregada por la persona (antes pendiente de verificación); fuentes en fuentes_mercado/ con huella. "
    "Generado por resultados/scripts/generar_cambio_vinci_b.py.")
c["fechas"]["publicacion_fuentes"] = (
    "Informes anuales 2016–2019, URD 2020–2025 y semestral a 30-jun-2026 de VINCI (FUENTES.tsv; Release fuentes-examen-20261118). Corte: fecha de "
    "análisis de la etapa 1 (Análisis!D4 = 2026-10-10); la información de los nueve meses de 2026 (22-oct-2026) queda fuera. Datos de mercado del "
    "9-oct-2026 con bytes: precio 107,05 € de la exportación oficial de Euronext «Historical Data» (VINCI_historical_price.xls, entregado por la "
    "persona responsable el 19-nov-2026, anexo 3 bis) y tasa sin riesgo 3,47 % del CSV oficial de la Bundesbank (Bund a 10 años, serie WT1010; "
    "Release fuentes-examen-20261118, asset 766892543); sector de Damodaran con damodaran_margin.xls (enero 2026, asset 766892761).")
c["metadatos"] = {
    "precio": {
        "valor": 107.05, "moneda_cotizacion": "EUR", "fecha": "2026-10-09", "fx": None, "fx_fecha": None,
        "fuente": ("Cierre de VINCI (FR0000125486, Euronext Paris) del 9-oct-2026 = 107,05 €, de la exportación oficial de Euronext «Historical Data» "
                   "(del 2024-11-20 al 2026-11-18) entregada por la persona responsable el 19-nov-2026 (VINCI_historical_price.xls, SHA-256 "
                   "78eee9c5d6b1e0402ab9bf8979a5f2d19c09acf3d861bca9e9427ebe305afb9d; RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 bis): fila "
                   "«2026-10-09 | 107.8 | 108.1 | 106.75 | 107.05 | 107.05» (apertura 107,80; máximo 108,10; mínimo 106,75; último y cierre 107,05). "
                   "Bytes conservados en fuentes_mercado/VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.xls con una copia "
                   "de texto (LibreOffice). Coincide con el precio de la etapa 1 y con el histórico no ajustado de Euronext que conservó el extractor "
                   "Mistral (fuentes_mercado/Euronext_DG_FR0000125486_XPAR_historico_NO_AJUSTADO_2026-01-02_a_2026-11-19.txt). El cierre lleva el "
                   "dividendo a cuenta de 1,10 € (fecha ex 13-oct-2026, según la etapa 1). Cierre del día, sin hora intradía."),
        "nota": "precio de cierre del 9-oct-2026 (fecha de análisis 2026-10-10), comprobado en la exportación oficial de Euronext entregada por la persona"},
    "capitalizacion": {
        "valor": float(CAP), "fecha": "2026-10-09",
        "fuente": ("107,05 € (cierre del 9-oct-2026, exportación oficial de Euronext) × 555,967094 millones de acciones en circulación a 31-dic-2025 "
                   "(P-O2 (a)) = 59.516,2774127 mm, producto exacto. La etapa 1 daba 59.043 con las 551.548.982 acciones a 30-sep-2026. Desalineación "
                   "de fechas declarada (Z-ACC): precio del 9-oct-2026 y acciones al cierre del ejercicio."),
        "pagina": "derivado (acciones: URD 2025 PDF p. 346)", "periodo": "precio del 9-oct-2026 × acciones a 31-dic-2025", "unidad": "millones de EUR"},
    "tasa_sin_riesgo": {
        "valor": 0.0347, "fecha": "2026-10-09",
        "fuente": ("Deutsche Bundesbank, serie diaria BBSSY.D.REN.EUR.A630.000000WT1010.A «Daily yield of the current 10 year federal bond» (Bund "
                   "alemán a 10 años de referencia; Alemania, AAA; moneda del modelo EUR), fila del 2026-10-09, la fecha del precio (C37): 3,47 % → "
                   "0,0347. CSV oficial subido por la persona responsable a la Release fuentes-examen-20261118 del repositorio auxiliar (asset "
                   "766892543, bund_10y_WT1010.csv, SHA-256 fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967; última actualización "
                   "de la serie 2026-11-18 12:31:26), conservado en fuentes_mercado/ con su huella. Sustituye el 3,486 % de la etapa 1 (Investing.com, "
                   "sin bytes conservados). Contraste (no es la serie elegida): la rentabilidad de 9 a 10 años de la Bundesbank (UMU) da 3,46 % y la "
                   "curva AAA del BCE 3,5112 % ese día (conservadas por el extractor Mistral). El OAT francés no se usa: su prima la suma la plantilla "
                   "en «Riesgo país»."),
        "pagina": "fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt, fila 2026-10-09",
        "periodo": "2026-10-09 (fecha del precio)", "unidad": "proporción"},
}
c["notas_que_se_retiran"] = ["^Fecha de análisis = la de la etapa 1 \\(Análisis!D4 = 2026-10-10\\); fuentes posteriores"]
c["nota_metadatos"] = ("(vinci_b, 20-nov-2026) Fecha de análisis = la de la etapa 1 (Análisis!D4 = 2026-10-10); fuentes posteriores (nueve meses de "
                       "2026, 22-oct-2026) fuera del expediente. Precio (107,05 €) y tasa sin riesgo (3,47 %) son cierres del 9-oct-2026 con bytes "
                       "oficiales en fuentes_mercado/: exportación de Euronext entregada por la persona y CSV de la Bundesbank (serie WT1010). El "
                       "sector de Damodaran (Engineering/Construction) se contrasta con damodaran_margin.xls (enero 2026, Release, asset 766892761).")
c["control_maestro_textos"]["D88"] = ("Medias del DCF: FY2023–2025 (C46–C50). Balance a 30/06/2026 y LTM a 30/06/2026 en C33, C40, C42, C53 y C54 "
                                      "(etapa 1); precio 09/10/2026 (Euronext, exportación oficial) y Bund a 10 años del mismo día (Bundesbank WT1010); "
                                      "acciones en circulación a 31/12/2025 (C55 = 555,967094 M, P-O2 a).")
av = p["alcance"]["aviso"]
viejo = "Precio y tasa sin riesgo de la etapa 1, pendientes de verificación."
assert viejo in av
c["alcance"]["aviso"] = av.replace(viejo, "Precio 107,05 € (Euronext, exportación oficial) y tasa sin riesgo 3,47 % (Bundesbank WT1010) del 9-oct-2026, con bytes en fuentes_mercado/.")
c["alcance"]["fecha"] = "2026-11-20"
c["alcance"]["fuente"] = p["alcance"]["fuente"] + " V-CIRC (a) y V-ANCLA (a) (19-nov-2026); anexos 3 y 3 bis de RELEASE_FUENTES_EXAMEN_VERIFICACION.md (datos de mercado)."
c["textos_prohibidos"] = p["textos_prohibidos"] + ["según la etapa 1 \\(Investing", "etapa 1, pendiente de verificación", "pendiente de verificación en Euronext",
                                                   "pendientes de verificación en fuente oficial", "Precio y tasa sin riesgo de la etapa 1"]
json.dump(c, open(SAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
open(SAL, "a").write("\n")
print("escrito", SAL)
