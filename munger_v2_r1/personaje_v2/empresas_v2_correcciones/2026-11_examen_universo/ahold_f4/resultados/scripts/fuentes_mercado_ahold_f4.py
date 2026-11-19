#!/usr/bin/env python3
"""ahold_f4 · fuentes de mercado nuevas (encargo del coordinador, 19-nov-2026): CSV oficial de la Bundesbank (Bund a 10 años, serie
BBSSY.D.REN.EUR.A630.000000WT1010.A) y tabla de márgenes de Damodaran (damodaran_margin.xls), subidos por la persona responsable a la Release
fuentes-examen-20261118 del repositorio auxiliar (assets 766892543 y 766892761). Comprueba las huellas, conserva la descarga cruda byte a byte y,
como las demás fuentes de mercado, una copia de texto con la marca [PDF PAGE 1] que verificacion_entradas.py puede examinar (CSV: filas de datos
con separador de espacio, como Bundesbank_UMU…; XLS: la hoja «Industry Averages» fila a fila, celdas separadas por « | »). Añade las huellas a
HUELLAS.txt y deja el rastro en resultados/fuentes_mercado_ahold_f4.json.
Uso: python3 -I fuentes_mercado_ahold_f4.py CARPETA_EMPRESA DIR_DESCARGAS DIR_XLRD RASTRO.json"""
import datetime as dt, hashlib, json, os, re, shutil, sys
C, DESC, XLRD, RASTRO = sys.argv[1:5]
FM = os.path.join(C, "fuentes_mercado")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
ESPERADO = {"bund_10y_WT1010.csv": ("766892543", "fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967"),
            "damodaran_margin.xls": ("766892761", "25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a")}
for n, (_, s) in ESPERADO.items():
    assert h(os.path.join(DESC, n)) == s, n
rastro = {"fecha": "2026-11-19", "guion": os.path.abspath(__file__), "release": "jluisplagos/munger-v2-evidencias-mistral, fuentes-examen-20261118",
          "descarga": "gh api -H 'Accept: application/octet-stream' repos/jluisplagos/munger-v2-evidencias-mistral/releases/assets/<asset>", "archivos": []}
# --- Bundesbank
crudo = os.path.join(FM, "Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv")
shutil.copy2(os.path.join(DESC, "bund_10y_WT1010.csv"), crudo)
lin = open(crudo, encoding="utf-8").read().split("\n")
out = []
for l in lin:
    if re.match(r"^\d{4}-\d{2}-\d{2},", l):
        l = l.replace(",", " ", 1)
        l = l[:-1] if l.endswith(",") else l
    out.append(l)
txt = os.path.join(FM, "Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt")
open(txt, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + "\n".join(out))
assert "\n2026-11-13 3.37\n" in open(txt, encoding="utf-8").read()
rastro["archivos"].append({"archivo": os.path.relpath(crudo, C), "asset": ESPERADO["bund_10y_WT1010.csv"][0], "sha256": h(crudo), "que": "descarga cruda (CSV oficial de la Bundesbank)"})
rastro["archivos"].append({"archivo": os.path.relpath(txt, C), "sha256": h(txt), "que": "copia de texto con marca [PDF PAGE 1] (filas de datos con separador de espacio)",
                           "fila_usada": "2026-11-13 3.37 (fecha del precio, C37)"})
# --- Damodaran
sys.path.insert(0, XLRD)
import xlrd  # noqa: E402
crudo_d = os.path.join(FM, "Damodaran_margin_2026-01.xls")
shutil.copy2(os.path.join(DESC, "damodaran_margin.xls"), crudo_d)
b = xlrd.open_workbook(crudo_d)
s = b.sheet_by_name("Industry Averages")
fecha = xlrd.xldate_as_datetime(s.cell_value(0, 1), b.datemode).date().isoformat()


def celda(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


filas = [f"fila {r + 1}: " + " | ".join(celda(v) for v in s.row_values(r)).rstrip(" |") for r in range(s.nrows)]
txt_d = os.path.join(FM, "Damodaran_margin_industry_averages_2026-01.txt")
open(txt_d, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + f"Hoja «Industry Averages» de Damodaran_margin_2026-01.xls (sha256 {h(crudo_d)}); "
                                         f"«Date updated» (B1, número de serie de Excel {celda(s.cell_value(0, 1))}) = {fecha}\n" + "\n".join(filas) + "\n")
fila_g = [r + 1 for r in range(s.nrows) if s.cell_value(r, 0) == "Retail (Grocery and Food)"]
assert fila_g == [83], fila_g
rastro["archivos"].append({"archivo": os.path.relpath(crudo_d, C), "asset": ESPERADO["damodaran_margin.xls"][0], "sha256": h(crudo_d), "que": "descarga cruda (XLS de Damodaran, «Margins by industry», empresas de EE. UU.)"})
rastro["archivos"].append({"archivo": os.path.relpath(txt_d, C), "sha256": h(txt_d), "que": "copia de texto con marca [PDF PAGE 1] de la hoja «Industry Averages» (xlrd 2.0.1)",
                           "fila_usada": f"fila {fila_g[0]}: {filas[fila_g[0] - 1][:160]}", "fecha_datos": fecha})
hu = os.path.join(FM, "HUELLAS.txt")
añadido = ["", "--- Añadidas en ahold_f4 por Claude orquestación (19-nov-2026; resultados/fuentes_mercado_ahold_f4.json): CSV y XLS oficiales de la Release",
           "fuentes-examen-20261118 (assets 766892543 y 766892761), subidos por la persona responsable; huellas comprobadas contra las publicadas.", ""]
for a in rastro["archivos"]:
    añadido += [f"archivo: {os.path.basename(a['archivo'])}", f"  sha256: {a['sha256']}", f"  contenido: {a['que']}" + (f"; {a['fila_usada']}" if a.get("fila_usada") else ""), ""]
open(hu, "a", encoding="utf-8").write("\n".join(añadido))
rastro["huellas_txt_sha256"] = h(hu)
json.dump(rastro, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rastro, ensure_ascii=False, indent=1))
