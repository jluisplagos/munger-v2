#!/usr/bin/env python3
"""zoetis_t1d · fuentes de mercado con bytes oficiales (encargo del coordinador, 19-nov-2026): CSV oficial del Tesoro de EE. UU. (Daily Treasury Par Yield Curve
Rates 2026) y tabla de márgenes de Damodaran (damodaran_margin.xls), subidos por la persona responsable a la Release fuentes-examen-20261118 del repositorio
auxiliar (assets 766892834 y 766892761; anexo 3 de RELEASE_FUENTES_EXAMEN_VERIFICACION.md). Comprueba las huellas publicadas, conserva la descarga cruda byte a
byte y, como en ahold_f4 (resultados/scripts/fuentes_mercado_ahold_f4.py), una copia de texto con la marca [PDF PAGE 1] que verificacion_entradas.py puede
examinar (CSV: cada fila con sus celdas separadas por « | », sin tocar ninguna cifra; XLS: la hoja «Industry Averages» fila a fila, xlrd 2.0.1). Los archivos
de zoetis_t1c (transcripciones del extractor) se conservan sin cambios. Añade las huellas a HUELLAS.txt y deja el rastro en RASTRO.json.
Añadido (encargo del coordinador, 19-nov-2026): la captura de investor.zoetis.com «Historical Stock Quote» del 8-oct-2026 entregada por la persona responsable
(RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 ter; copia del coordinador en DIR_CAPTURA con SHA256SUMS), byte a byte, y su transcripción con marca [PDF PAGE 1]
hecha por Claude orquestación leyendo la imagen (la comprueba el revisor contra la imagen).
Uso: python3 -I fuentes_mercado_zoetis_t1d.py CARPETA_EMPRESA DIR_DESCARGAS DIR_XLRD RASTRO.json DIR_CAPTURA"""
import csv, hashlib, io, json, os, shutil, sys
C, DESC, XLRD, RASTRO, CAPT = sys.argv[1:6]
FM = os.path.join(C, "fuentes_mercado")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
ESPERADO = {"us_treasury_par_yield_2026.csv": ("766892834", "0707733bdc20fce9a21a1063c5b99dbfd3456acabb216f73e6d6b798f511243d"),
            "damodaran_margin.xls": ("766892761", "25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a")}
for n, (_, s) in ESPERADO.items():
    assert h(os.path.join(DESC, n)) == s, n
rastro = {"fecha": "2026-11-19", "guion": os.path.relpath(os.path.abspath(__file__), os.path.dirname(os.path.abspath(C))),
          "release": "jluisplagos/munger-v2-evidencias-mistral, fuentes-examen-20261118 (anexo 3)",
          "descarga": "gh api -H 'Accept: application/octet-stream' repos/jluisplagos/munger-v2-evidencias-mistral/releases/assets/<asset>", "archivos": []}
# --- Tesoro de EE. UU.
crudo = os.path.join(FM, "US_Treasury_par_yield_2026_Release_766892834.csv")
assert not os.path.exists(crudo)
shutil.copy2(os.path.join(DESC, "us_treasury_par_yield_2026.csv"), crudo)
filas = list(csv.reader(io.StringIO(open(crudo, encoding="utf-8").read())))
cab = filas[0]
assert cab[0] == "Date" and cab[12] == "10 Yr", cab
txt = os.path.join(FM, "US_Treasury_par_yield_2026_Release_766892834.txt")
lineas = [" | ".join(f) for f in filas]
open(txt, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + f"U.S. Department of the Treasury, Daily Treasury Par Yield Curve Rates 2026: copia de texto de {os.path.basename(crudo)} "
                                       f"(sha256 {h(crudo)}), una línea por fila del CSV con sus celdas separadas por « | »\n" + "\n".join(lineas) + "\n")
fila = [l for l in lineas if l.startswith("10/08/2026 |")]
assert len(fila) == 1 and fila[0].split(" | ")[12] == "5.22", fila
rastro["archivos"].append({"archivo": os.path.relpath(crudo, C), "asset": ESPERADO["us_treasury_par_yield_2026.csv"][0], "sha256": h(crudo), "que": "descarga cruda (CSV oficial del Tesoro de EE. UU.)"})
rastro["archivos"].append({"archivo": os.path.relpath(txt, C), "sha256": h(txt), "que": "copia de texto con marca [PDF PAGE 1] (celdas separadas por « | »)",
                           "fila_usada": fila[0] + " (columna 13 «10 Yr» = 5.22; C57)"})
# --- Damodaran
sys.path.insert(0, XLRD)
import xlrd  # noqa: E402
crudo_d = os.path.join(FM, "Damodaran_margin_2026-01_Release_766892761.xls")
assert not os.path.exists(crudo_d)
shutil.copy2(os.path.join(DESC, "damodaran_margin.xls"), crudo_d)
b = xlrd.open_workbook(crudo_d)
s = b.sheet_by_name("Industry Averages")
fecha = xlrd.xldate_as_datetime(s.cell_value(0, 1), b.datemode).date().isoformat()


def celda(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


filas_d = [f"fila {r + 1}: " + " | ".join(celda(v) for v in s.row_values(r)).rstrip(" |") for r in range(s.nrows)]
txt_d = os.path.join(FM, "Damodaran_margin_industry_averages_2026-01_Release_766892761.txt")
open(txt_d, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + f"Hoja «Industry Averages» de {os.path.basename(crudo_d)} (sha256 {h(crudo_d)}); "
                                         f"«Date updated» (B1, número de serie de Excel {celda(s.cell_value(0, 1))}) = {fecha}\n" + "\n".join(filas_d) + "\n")
fila_g = [r + 1 for r in range(s.nrows) if s.cell_value(r, 0) == "Drugs (Pharmaceutical)"]
assert len(fila_g) == 1, fila_g
rastro["archivos"].append({"archivo": os.path.relpath(crudo_d, C), "asset": ESPERADO["damodaran_margin.xls"][0], "sha256": h(crudo_d), "que": "descarga cruda (XLS de Damodaran, «Margins by industry», empresas de EE. UU.)"})
rastro["archivos"].append({"archivo": os.path.relpath(txt_d, C), "sha256": h(txt_d), "que": "copia de texto con marca [PDF PAGE 1] de la hoja «Industry Averages» (xlrd 2.0.1)",
                           "fila_usada": filas_d[fila_g[0] - 1][:200], "fila": fila_g[0], "fecha_datos": fecha})
# --- captura del precio (investor.zoetis.com)
PNG_SHA = "c1871f7e80e1f46015912a0cc585292bc9186e2fad95db5d8ef98bbe632c1530"
src = os.path.join(CAPT, "Zoetis_ZTS_2026-10-08_chat.png")
assert h(src) == PNG_SHA and f"{PNG_SHA}  Zoetis_ZTS_2026-10-08_chat.png" in open(os.path.join(CAPT, "SHA256SUMS"), encoding="utf-8").read()
png = os.path.join(FM, "Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.png")
assert not os.path.exists(png)
shutil.copy2(src, png)
txt_p = os.path.join(FM, "Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.txt")
open(txt_p, "w", encoding="utf-8").write(
    "[PDF PAGE 1]\n"
    f"Transcripción (Claude orquestación, 19-nov-2026, leyendo la imagen) de la captura de pantalla {os.path.basename(png)} (sha256 {PNG_SHA}), entregada por la persona "
    "responsable el 19-nov-2026 (RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 ter). Página: https://investor.zoetis.com/stock-information/default.aspx#stock-historical "
    "(Zoetis Inc. - Stock Information). Sección «Historical Stock Quote». El revisor la contrasta con la imagen.\n"
    "Lookup Date: 2026 Oct 8\n"
    "Day's Open $71.36 | Closing Price $73.08\n"
    "Intraday Low $71.15 | Intraday High $73.75\n"
    "Volume 6,176,469\n")
rastro["archivos"].append({"archivo": os.path.relpath(png, C), "sha256": h(png), "que": "captura de investor.zoetis.com «Historical Stock Quote», 2026-Oct-8 (anexo 3 ter; copia del coordinador Zoetis_ZTS_2026-10-08_chat.png)"})
rastro["archivos"].append({"archivo": os.path.relpath(txt_p, C), "sha256": h(txt_p), "que": "transcripción de la captura con marca [PDF PAGE 1]", "fila_usada": "Closing Price $73.08 (Lookup Date 2026 Oct 8; C37)"})
hu = os.path.join(FM, "HUELLAS.txt")
añadido = ["", "--- Añadidas en zoetis_t1d por Claude orquestación (19-nov-2026; resultados/fuentes_mercado_zoetis_t1d.json): CSV y XLS oficiales de la Release",
           "fuentes-examen-20261118 (assets 766892834 y 766892761, anexo 3), subidos por la persona responsable, y captura del precio del 8-oct-2026 (anexo 3 ter); huellas comprobadas contra las publicadas.",
           "Los archivos anteriores (transcripciones o extractos del extractor) se conservan sin cambios.", ""]
for a in rastro["archivos"]:
    añadido += [f"archivo: {os.path.basename(a['archivo'])}", f"  sha256: {a['sha256']}", f"  contenido: {a['que']}" + (f"; {a['fila_usada']}" if a.get("fila_usada") else ""), ""]
open(hu, "a", encoding="utf-8").write("\n".join(añadido))
rastro["huellas_txt_sha256"] = h(hu)
json.dump(rastro, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rastro, ensure_ascii=False, indent=1))
