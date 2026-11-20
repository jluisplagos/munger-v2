#!/usr/bin/env python3
"""vinci_b · fuentes de mercado (encargo del coordinador, 20-nov-2026). Crea Vinci/fuentes_mercado/ (vinci/Vinci no tenía) con:
  1. lo que conservó el extractor Mistral (rama mistral/examen-vinci-entradas @ 737a8d8, resultados_examen/vinci/fuentes_mercado/), byte a byte y
     con las huellas de su HUELLAS.txt (se comprueban): histórico no ajustado de Euronext Paris, serie UMU de la Bundesbank, curva AAA del BCE y
     página mgnroc de Damodaran; su HUELLAS.txt encabeza el nuestro sin cambios;
  2. los archivos oficiales que subió o entregó la persona responsable (huellas comprobadas contra las publicadas), en bruto y con una copia de
     texto con la marca [PDF PAGE 1] que verificacion_entradas.py puede examinar:
     - bund_10y_WT1010.csv (Release fuentes-examen-20261118, asset 766892543): filas de datos con separador de espacio (como en ahold_f4);
     - damodaran_margin.xls (asset 766892761): hoja «Industry Averages» fila a fila, celdas separadas por « | » (xlrd 2.0.1; como en ahold_f4);
     - VINCI_historical_price.xls (exportación de Euronext entregada por la persona, anexo 3 bis): convertida a CSV con LibreOffice
       (soffice --convert-to csv; el guion se ejecuta bajo flock /home/user/e_work/libreoffice.lock) y conservada con las celdas separadas por « | ».
Añade las huellas a HUELLAS.txt y deja el rastro en RASTRO.json. No cambia ninguna cifra.
Uso: python3 -I fuentes_mercado_vinci_b.py CARPETA_EMPRESA DIR_MISTRAL DIR_PERSONA DIR_XLRD DIR_TRABAJO RASTRO.json"""
import csv, hashlib, io, json, os, re, shutil, subprocess, sys
C, MIS, DESC, XLRD, TRAB, RASTRO = sys.argv[1:7]
FM = os.path.join(C, "fuentes_mercado")
assert not os.path.exists(FM)
os.makedirs(FM)
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
ESPERADO = {"bund_10y_WT1010.csv": ("766892543", "fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967"),
            "damodaran_margin.xls": ("766892761", "25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a"),
            "VINCI_historical_price.xls": ("anexo 3 bis (entregado en el chat; copia del coordinador)", "78eee9c5d6b1e0402ab9bf8979a5f2d19c09acf3d861bca9e9427ebe305afb9d")}
for n, (_, s) in ESPERADO.items():
    assert h(os.path.join(DESC, n)) == s, n
rastro = {"fecha": "2026-11-20", "autor": "Claude orquestación", "guion": "resultados/scripts/fuentes_mercado_vinci_b.py",
          "release": "jluisplagos/munger-v2-evidencias-mistral, fuentes-examen-20261118; anexos 3 y 3 bis de coordinacion/cierre_v2/examen/RELEASE_FUENTES_EXAMEN_VERIFICACION.md",
          "archivos": []}
# --- 1. lo del extractor Mistral
hu_m = open(os.path.join(MIS, "HUELLAS.txt"), encoding="utf-8").read()
for bloque in re.findall(r"archivo: (\S+)\n  bytes: (\d+)\n  sha256: ([0-9a-f]{64})", hu_m):
    n, b, s = bloque
    src = os.path.join(MIS, n)
    assert h(src) == s and os.path.getsize(src) == int(b), n
    shutil.copy2(src, os.path.join(FM, n))
    rastro["archivos"].append({"archivo": f"fuentes_mercado/{n}", "sha256": s, "que": "conservado por el extractor Mistral (rama mistral/examen-vinci-entradas @ 737a8d8), sin cambios"})
assert len(rastro["archivos"]) == 4
# --- 2a. Bundesbank WT1010
crudo = os.path.join(FM, "Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv")
shutil.copy2(os.path.join(DESC, "bund_10y_WT1010.csv"), crudo)
out = []
for l in open(crudo, encoding="utf-8").read().split("\n"):
    if re.match(r"^\d{4}-\d{2}-\d{2},", l):
        l = l.replace(",", " ", 1)
        l = l[:-1] if l.endswith(",") else l
    out.append(l)
txt = os.path.join(FM, "Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt")
open(txt, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + "\n".join(out))
assert "\n2026-10-09 3.47\n" in open(txt, encoding="utf-8").read()
rastro["archivos"] += [{"archivo": "fuentes_mercado/" + os.path.basename(crudo), "asset": ESPERADO["bund_10y_WT1010.csv"][0], "sha256": h(crudo), "que": "descarga cruda (CSV oficial de la Bundesbank)"},
                       {"archivo": "fuentes_mercado/" + os.path.basename(txt), "sha256": h(txt), "que": "copia de texto con marca [PDF PAGE 1] (filas de datos con separador de espacio)",
                        "fila_usada": "2026-10-09 3.47 (fecha del precio, C37; C57)"}]
# --- 2b. Damodaran margin.xls
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
fila_e = [r + 1 for r in range(s.nrows) if s.cell_value(r, 0) == "Engineering/Construction"]
assert fila_e == [39], fila_e
rastro["archivos"] += [{"archivo": "fuentes_mercado/" + os.path.basename(crudo_d), "asset": ESPERADO["damodaran_margin.xls"][0], "sha256": h(crudo_d), "que": "descarga cruda (XLS de Damodaran, «Margins by industry», empresas de EE. UU.)"},
                       {"archivo": "fuentes_mercado/" + os.path.basename(txt_d), "sha256": h(txt_d), "que": "copia de texto con marca [PDF PAGE 1] de la hoja «Industry Averages» (xlrd 2.0.1)",
                        "fila_usada": filas[fila_e[0] - 1][:200], "fecha_datos": fecha}]
# --- 2c. Euronext (exportación de la persona), con LibreOffice
crudo_e = os.path.join(FM, "VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.xls")
shutil.copy2(os.path.join(DESC, "VINCI_historical_price.xls"), crudo_e)
conv = os.path.join(TRAB, "conv_euronext")
os.makedirs(conv, exist_ok=True)
perfil = os.path.join(TRAB, "perfil_lo")
r = subprocess.run(["soffice", f"-env:UserInstallation=file://{perfil}", "--headless", "--convert-to", "csv:Text - txt - csv (StarCalc):44,34,76,1",
                    "--outdir", conv, crudo_e], capture_output=True, text=True, timeout=300)
ver = subprocess.run(["soffice", f"-env:UserInstallation=file://{perfil}", "--version"], capture_output=True, text=True, timeout=120).stdout.strip().split(" 420")[0]
assert ver.startswith("LibreOffice "), ver
csvp = os.path.join(conv, os.path.splitext(os.path.basename(crudo_e))[0] + ".csv")
assert r.returncode == 0 and os.path.exists(csvp), (r.stdout, r.stderr)
lineas = [" | ".join(f).rstrip(" |") for f in csv.reader(io.StringIO(open(csvp, encoding="utf-8").read()))]
txt_e = os.path.join(FM, "VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.txt")
cab = (f"Exportación de Euronext «Historical Data» de VINCI (FR0000125486) entregada por la persona responsable (VINCI_historical_price.xls, sha256 "
       f"{h(crudo_e)}), convertida a texto con {ver} (soffice --headless --convert-to csv, bajo flock); celdas separadas por « | »; ninguna cifra cambia")
open(txt_e, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + cab + "\n" + "\n".join(lineas) + "\n")
usada = [l for l in lineas if l.startswith("2026-10-09 |")]
assert usada == ["2026-10-09 | 107.8 | 108.1 | 106.75 | 107.05 | 107.05 | 776381 | 5046 | 83208577 | 107.1749"], usada
assert lineas[3].startswith("Date | Open | High | Low | Last | Close"), lineas[:4]
rastro["archivos"] += [{"archivo": "fuentes_mercado/" + os.path.basename(crudo_e), "origen": ESPERADO["VINCI_historical_price.xls"][0], "sha256": h(crudo_e),
                        "que": "exportación cruda de Euronext «Historical Data» (XLS) entregada por la persona responsable"},
                       {"archivo": "fuentes_mercado/" + os.path.basename(txt_e), "sha256": h(txt_e),
                        "que": "copia de texto con marca [PDF PAGE 1] (LibreOffice --convert-to csv, bajo flock; celdas separadas por « | »)",
                        "fila_usada": usada[0] + " (C37: Close)", "libreoffice": ver}]
# --- HUELLAS.txt
hu = os.path.join(FM, "HUELLAS.txt")
añadido = ["", "--- Añadidas en vinci_b por Claude orquestación (20-nov-2026; resultados/fuentes_mercado_vinci_b.json): CSV y XLS oficiales de la Release",
           "fuentes-examen-20261118 (assets 766892543 y 766892761), subidos por la persona responsable, y la exportación de Euronext entregada por la",
           "persona (anexo 3 bis); huellas comprobadas contra las publicadas. Los cuatro archivos de arriba (extractor Mistral) se conservan sin cambios.", ""]
for a in rastro["archivos"][4:]:
    añadido += [f"archivo: {os.path.basename(a['archivo'])}", f"  sha256: {a['sha256']}", f"  contenido: {a['que']}" + (f"; {a['fila_usada']}" if a.get("fila_usada") else ""), ""]
open(hu, "w", encoding="utf-8").write(hu_m.rstrip("\n") + "\n" + "\n".join(añadido))
rastro["huellas_txt_sha256"] = h(hu)
json.dump(rastro, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(rastro, ensure_ascii=False, indent=1))
