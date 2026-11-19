#!/usr/bin/env python3
"""jumbo_g · antes de la auditoría (encargo del coordinador, 19-nov-2026):
 1) fuentes de mercado con los bytes que subió la persona responsable (RELEASE_FUENTES_EXAMEN_VERIFICACION.md del auxiliar, anexos 3 y 3 ter; copias del
    coordinador en DIR_PERSONA con SHA256SUMS): captura de Euronext Athens «Historical Data» del 17-nov-2026 (asset 766946296), CSV oficial de la Bundesbank
    WT1010 (asset 766892543) y margin.xls de Damodaran (asset 766892761). Se conservan byte a byte en Jumbo/fuentes_mercado/ y, como en ahold_f4 y zoetis_t1d,
    con una copia de texto con marca [PDF PAGE 1] que verificacion_entradas.py puede examinar (CSV y XLS con las mismas conversiones que
    ahold_f4/resultados/scripts/fuentes_mercado_ahold_f4.py; la imagen, con la transcripción de Claude orquestación, que el revisor contrasta con la imagen).
    Las fuentes anteriores (JUMBO_BELA_20261118.md y el extracto de mgnroc) se conservan sin cambios.
 2) registro: C37, C57 y Palancas!C7 pasan de lectura externa a fuente local; C41/C42 (dependen de C37) quedan pendientes de nuevo; C38 se marca
    «Dato no verificable» en el registro; hipótesis y convenciones con el texto vigente de las fases de jumbo_g (C76 = 150 de la fase B); C46/C40 solo llevarían
    una incidencia si su valor no correspondiera al C76 vigente (ya están recalculados con 150: recalculo_dependientes_Jumbo.json). Todo lo cambiado: extractor «Claude orquestación», pendiente, sin revisor ni vínculo. No se usa `sellar`.
Uso: python3 -I fuentes_mercado_y_registro_jumbo_g.py CARPETA_EMPRESA DIR_PERSONA DIR_XLRD RASTRO.json"""
import copy, hashlib, json, os, re, shutil, sys
C, PERS, XLRD, RASTRO = sys.argv[1:5]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402
FM = os.path.join(C, "fuentes_mercado")
HOY, EXT = "2026-11-19", "Claude orquestación"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
ESPERADO = {"Jumbo_BELA_2026-11-17_EuronextAthens.jpg": ("766946296", "c6f6a4b192248837f41c69e7132f28a9c5c29f663c92ae9d16ad41e946976693"),
            "bund_10y_WT1010.csv": ("766892543", "fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967"),
            "damodaran_margin.xls": ("766892761", "25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a")}
sumas = open(os.path.join(PERS, "SHA256SUMS"), encoding="utf-8").read()
for n, (_, s) in ESPERADO.items():
    assert h(os.path.join(PERS, n)) == s and f"{s}  {n}" in sumas, n
rastro = {"fecha": HOY, "guion": "resultados/scripts/fuentes_mercado_y_registro_jumbo_g.py",
          "release": "jluisplagos/munger-v2-evidencias-mistral, fuentes-examen-20261118 (anexos 3 y 3 ter de RELEASE_FUENTES_EXAMEN_VERIFICACION.md)",
          "copias": "/home/user/e_work/fuentes_examen/mercado_persona/ (SHA256SUMS del coordinador)", "archivos": [], "registro": {}}


def nuevo(nombre):
    p = os.path.join(FM, nombre)
    assert not os.path.exists(p), p
    return p


# ---------------------------------------------------------------------------------------------- 1a. precio: captura de Euronext Athens
JPG = nuevo("Jumbo_BELA_2026-11-17_EuronextAthens.jpg")
shutil.copy2(os.path.join(PERS, "Jumbo_BELA_2026-11-17_EuronextAthens.jpg"), JPG)
TXT_P = nuevo("Jumbo_BELA_2026-11-17_EuronextAthens_historical_data.txt")
open(TXT_P, "w", encoding="utf-8").write(
    "[PDF PAGE 1]\n"
    f"Transcripción (Claude orquestación, 19-nov-2026, leyendo la imagen) de la captura de pantalla {os.path.basename(JPG)} (sha256 {h(JPG)}), subida por la persona "
    "responsable a la Release fuentes-examen-20261118 (asset 766946296; RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 ter). Página de Euronext Athens "
    "(logotipo «EURONEXT | Athens»), sección «Historical Data». La imagen no muestra el nombre ni el código del instrumento: que es BELA (Jumbo S.A.) lo dicen el "
    "nombre del archivo, el anexo 3 ter y la lectura anterior de la persona (JUMBO_BELA_20261118.md). El revisor contrasta esta transcripción con la imagen.\n"
    "DATE\n"
    "11/18/2026 (fila plegada)\n"
    "11/17/2026 (fila desplegada):\n"
    "11/17/2026 | CLOSE 27.2800 | OPEN 27.0000 | HIGH 27.2800 | LOW 26.7200 | CHANGE +0.44% | VOLUME 369,577 | VALUE 9,980,364.1200\n"
    "TRADES (cortado en la imagen)\n")
rastro["archivos"] += [{"archivo": os.path.relpath(JPG, C), "asset": "766946296", "sha256": h(JPG), "que": "captura de Euronext Athens «Historical Data» (anexo 3 ter)"},
                       {"archivo": os.path.relpath(TXT_P, C), "sha256": h(TXT_P), "que": "transcripción de la captura con marca [PDF PAGE 1]",
                        "fila_usada": "11/17/2026 | CLOSE 27.2800 (C37)"}]
# ---------------------------------------------------------------------------------------------- 1b. Bund: CSV oficial de la Bundesbank (como ahold_f4)
CSV = nuevo("Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv")
shutil.copy2(os.path.join(PERS, "bund_10y_WT1010.csv"), CSV)
out = []
for l in open(CSV, encoding="utf-8").read().split("\n"):
    if re.match(r"^\d{4}-\d{2}-\d{2},", l):
        l = l.replace(",", " ", 1)
        l = l[:-1] if l.endswith(",") else l
    out.append(l)
TXT_B = nuevo("Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt")
open(TXT_B, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + "\n".join(out))
assert "\n2026-11-17 3.35\n" in open(TXT_B, encoding="utf-8").read()
assert h(TXT_B) == "c236dfcc2229861ad1c32348bd3375b584fcb048ba72fcc2554791f67a9d63a4"  # la misma copia de texto que ahold_f4
rastro["archivos"] += [{"archivo": os.path.relpath(CSV, C), "asset": "766892543", "sha256": h(CSV), "que": "descarga cruda (CSV oficial de la Bundesbank)"},
                       {"archivo": os.path.relpath(TXT_B, C), "sha256": h(TXT_B), "que": "copia de texto con marca [PDF PAGE 1] (filas de datos con separador de espacio)",
                        "fila_usada": "2026-11-17 3.35 (fecha del precio, C37; C57)"}]
# ---------------------------------------------------------------------------------------------- 1c. Damodaran: margin.xls (como ahold_f4)
sys.path.insert(0, XLRD)
import xlrd  # noqa: E402
XLS = nuevo("Damodaran_margin_2026-01.xls")
shutil.copy2(os.path.join(PERS, "damodaran_margin.xls"), XLS)
b = xlrd.open_workbook(XLS)
s = b.sheet_by_name("Industry Averages")
fecha = xlrd.xldate_as_datetime(s.cell_value(0, 1), b.datemode).date().isoformat()


def celda(v):
    if isinstance(v, float) and v.is_integer():
        return str(int(v))
    return str(v)


filas = [f"fila {r + 1}: " + " | ".join(celda(v) for v in s.row_values(r)).rstrip(" |") for r in range(s.nrows)]
TXT_D = nuevo("Damodaran_margin_industry_averages_2026-01.txt")
open(TXT_D, "w", encoding="utf-8").write("[PDF PAGE 1]\n" + f"Hoja «Industry Averages» de Damodaran_margin_2026-01.xls (sha256 {h(XLS)}); "
                                         f"«Date updated» (B1, número de serie de Excel {celda(s.cell_value(0, 1))}) = {fecha}\n" + "\n".join(filas) + "\n")
assert h(TXT_D) == "fe11adc50fad7efa191d0c99a899703f2e73cb1242f79b60cf2d5dfcbc1360ab"  # la misma copia de texto que ahold_f4
fila_g = [r + 1 for r in range(s.nrows) if s.cell_value(r, 0) == "Retail (General)"]
assert fila_g == [82], fila_g
rastro["archivos"] += [{"archivo": os.path.relpath(XLS, C), "asset": "766892761", "sha256": h(XLS), "que": "descarga cruda (XLS de Damodaran, «Margins by industry», empresas de EE. UU.)"},
                       {"archivo": os.path.relpath(TXT_D, C), "sha256": h(TXT_D), "que": "copia de texto con marca [PDF PAGE 1] de la hoja «Industry Averages» (xlrd 2.0.1)",
                        "fila_usada": filas[81][:160], "fecha_datos": fecha}]
hu = os.path.join(FM, "HUELLAS.txt")
añadido = ["", "# --- Añadidas en jumbo_g por Claude orquestación (19-nov-2026; resultados/fuentes_mercado_y_registro_jumbo_g.json): captura de Euronext Athens del",
           "# 17-nov-2026 (asset 766946296, anexo 3 ter), CSV oficial de la Bundesbank (asset 766892543) y XLS de Damodaran (asset 766892761), subidos por la persona",
           "# responsable a la Release fuentes-examen-20261118; huellas comprobadas contra las publicadas. Los archivos anteriores se conservan sin cambios.", ""]
for a in rastro["archivos"]:
    añadido += [f"{a['sha256']}  fuentes_mercado/{os.path.basename(a['archivo'])}", f"#   contenido: {a['que']}" + (f"; {a['fila_usada']}" if a.get("fila_usada") else ""), ""]
open(hu, "a", encoding="utf-8").write("\n".join(añadido))
rastro["huellas_txt_sha256"] = h(hu)

# ---------------------------------------------------------------------------------------------- 2. registro
p = os.path.join(C, VE.REGISTRO)
rastro["registro"]["antes_sha256"] = h(p)
reg = json.load(open(p, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
INST = VE.universo(C)
EVID = VE.evidencia_libro(C)
cambios = []


def pendiente(e, nota, fuente_examinada=None):
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, jumbo_g] {nota} · Comprobación anterior: {c0.get('extractor')} / {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:300]}",
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "motivo": nota})


def fuente_local(archivo, documento, version, ubicacion, concepto, columna, periodo, unidad, escala, valor_fuente, cita, tratamiento, perimetro_j):
    return {"documento": documento, "version": version, "conservacion": "local", "archivo": archivo, "sha256": h(os.path.join(C, archivo)), "pagina": 1, "folio": None,
            "ubicacion": ubicacion, "concepto": concepto, "columna": columna, "periodo": periodo, "unidad": unidad, "escala": escala, "signo": 1,
            "tratamiento": tratamiento, "perimetro": "no aplica: dato de mercado", "perimetro_justificacion": perimetro_j, "reexpresado": "no aplica",
            "valor_fuente": valor_fuente, "cita": cita}


e = por["Análisis!C37"]
e["fuente"] = fuente_local(
    os.path.relpath(TXT_P, C), "Euronext Athens, «Historical Data» del instrumento (BELA, Jumbo S.A., ISIN GRS467003000), fila del 17-nov-2026",
    (f"captura de pantalla subida por la persona responsable a la Release fuentes-examen-20261118 (asset 766946296; anexo 3 ter), conservada byte a byte en "
     f"fuentes_mercado/{os.path.basename(JPG)}, sha256 {h(JPG)}; transcripción con marca [PDF PAGE 1] hecha por Claude orquestación leyendo la imagen, sha256 {h(TXT_P)} "
     "(el revisor la contrasta con la imagen). Sustituye la lectura externa (JUMBO_BELA_20261118.md, «Previous Close» leído el 18-nov, que se conserva)"),
    "cuadro «Historical Data», fila 11/17/2026 desplegada (OPEN 27.0000, HIGH 27.2800, LOW 26.7200, VOLUME 369,577)", "precio de cierre por acción (CLOSE) de la sesión del 17-nov-2026",
    "CLOSE de la fila 11/17/2026", "cierre de la sesión del 17-nov-2026", "EUR por acción", 1, 27.28, "11/17/2026 | CLOSE 27.2800",
    ("precio de cierre de la sesión del 17-nov-2026, sin transformación; posterior a la fecha ex (16-nov-2026) de la distribución extraordinaria de 1,00 €/acción: "
     "sin derecho a ella (Control maestro N38). Límite: la imagen no muestra el nombre ni el código del instrumento; la identificación como BELA se apoya en el "
     "nombre del archivo, el anexo 3 ter y la lectura anterior de la persona"),
    "el precio es de la acción de Jumbo S.A. en Euronext Athens; el perímetro contable no se aplica a un dato de mercado")
e.pop("lectura_externa", None)
e["incidencia"] = "La captura no muestra el nombre del instrumento (ver «tratamiento»); el revisor confirma la identificación con el anexo 3 ter."
pendiente(e, "lectura externa → fuente local: captura de Euronext Athens del 17-nov-2026 (Release, asset 766946296, anexo 3 ter)", os.path.relpath(JPG, C))
e = por["Análisis!C57"]
e["fuente"] = fuente_local(
    os.path.relpath(TXT_B, C), "Deutsche Bundesbank, serie diaria BBSSY.D.REN.EUR.A630.000000WT1010.A «Daily yield of the current 10 year federal bond» (Bund a 10 años de referencia)",
    (f"CSV oficial subido por la persona responsable a la Release fuentes-examen-20261118 (asset 766892543, bund_10y_WT1010.csv; última actualización de la serie "
     f"2026-11-18), descarga cruda conservada byte a byte en fuentes_mercado/{os.path.basename(CSV)}, sha256 {h(CSV)} (la huella publicada, anexo 3); conservada como texto "
     f"con marca [PDF PAGE 1] y separador de espacio en las filas de datos (la misma copia que ahold_f4), sha256 {h(TXT_B)}"),
    "tabla de la serie diaria (cabecera con la definición de la serie), fila del 2026-11-17", "rendimiento del Bund a 10 años de referencia, en % diario",
    "2026-11-17 (fecha del precio, C37 y Palancas!C45)", "2026-11-17", "percent", 0.01, 3.35, "2026-11-17 3.35",
    ("rendimiento diario publicado en %; escala 0,01 lo pasa a proporción (3,35 % = 0,0335). Misma fecha que el precio (17-nov-2026). Sustituye las lecturas de "
     "terceros de los metadatos (Trading Economics, Ideal-investisseur), que coincidían"),
    "la tasa sin riesgo es un dato de mercado del bono de referencia en EUR; el perímetro contable no se aplica")
e.pop("lectura_externa", None)
pendiente(e, "lectura externa → fuente local: CSV oficial de la Bundesbank WT1010 (Release, asset 766892543, anexo 3)", os.path.relpath(CSV, C))
e = por["Palancas!C7"]
e["fuente"] = fuente_local(
    os.path.relpath(TXT_D, C), f"Damodaran (NYU Stern), «Margins by industry» (margin.xls), hoja «Industry Averages», empresas de EE. UU., «Date updated» {fecha}",
    (f"XLS subido por la persona responsable a la Release fuentes-examen-20261118 (asset 766892761, damodaran_margin.xls), descarga cruda conservada byte a byte en "
     f"fuentes_mercado/{os.path.basename(XLS)}, sha256 {h(XLS)} (la huella publicada, anexo 3); hoja «Industry Averages» conservada como texto con marca [PDF PAGE 1], una "
     f"línea por fila («fila n: celda | celda …», xlrd 2.0.1; la misma copia que ahold_f4), sha256 {h(TXT_D)}"),
    "hoja «Industry Averages», fila 82 (columna A «Industry Name»)", "sector de Damodaran asignado a Jumbo", "Industry Name (columna A), fila 82 de la hoja",
    f"clasificación de los datos de enero de 2026 («Date updated» {fecha})", "texto", 1, "Retail (General)", "fila 82: Retail (General) | 23",
    ("etiqueta de industria tal como figura en la tabla (23 empresas en esa fila, las mismas que la fila de mgnroc.html del extracto anterior, que se conserva). "
     "Limitación: la tabla es de empresas de EE. UU. y Jumbo es una minorista griega; la tabla europea o de mercados emergentes de Damodaran no está en el expediente"),
    "la clasificación sectorial es un dato externo al perímetro contable del grupo")
e.pop("lectura_externa", None)
pendiente(e, "lectura externa → fuente local: margin.xls de Damodaran (Release, asset 766892761, anexo 3)", os.path.relpath(XLS, C))
for k in ("Análisis!C41", "Análisis!C42"):
    pendiente(por[k], "sin cambio de fórmula ni de valor; su origen C37 pasa a fuente local (la huella de sus orígenes cambia): revisar de nuevo")
e = por["Análisis!C38"]
if "no verificable" not in str(e.get("incidencia") or "").lower():
    e["incidencia"] = ("«Dato no verificable»: valor intrínseco de terceros (Simply Wall St) sin bytes ni captura en el expediente; es contexto, no dato verificado. "
                       "El libro sigue marcándolo «Rellenado y verificado» (Control maestro F39, evidencia de la etapa 1): cambiar esa marca exige tocar la etapa 1 y "
                       "regenerar el libro que consumieron las fases; decisión de la orquestación.")
    pendiente(e, "marcado «Dato no verificable» en el registro (tercero sin bytes)")
c76 = INST["celdas"]["Análisis!C76"]
for k in ("Análisis!C46", "Análisis!C40"):
    e = por[k]
    d = e["derivacion"]
    vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else INST["celdas"][o]) for o in d["origenes"]}
    alt_ex = VE._eval_formula_exacta(d["formula"], vals)
    if VE._importe_libro_exacto(alt_ex, INST["celdas"][k]):
        continue  # ya recalculado con el C76 vigente (resultados/recalculo_dependientes_Jumbo.json): nada que señalar
    alt = float(alt_ex)
    e["incidencia"] = (f"DESFASE: el valor del libro ({INST['celdas'][k]}) se calculó con C76 = 160 (hipótesis de la fase B de jumbo_e); la fase B de jumbo_g fija "
                       f"C76 = {c76} y con la fórmula declarada sale {alt:.6f}. Decisión pendiente de la orquestación; aquí no se cambia el libro.")
    pendiente(e, f"incidencia del desfase con C76 = {c76} (fase B de jumbo_g)")
# hipótesis y convenciones: texto vigente de las fases
FASES = {}
for f_ in ("A", "B", "C"):
    p_ = os.path.join(C, f"celdas_{f_}.json")
    if os.path.exists(p_):
        for kk in json.load(open(p_, encoding="utf-8")):
            if "!" in kk:
                FASES[kk.replace("'", "")] = f_
hip = []
for k, e in por.items():
    if k.startswith("aux:") or INST["tipos"].get(k) != "hipótesis" or k == "Historia!C85":
        continue
    ev = EVID.get(k) or {}
    n = str(ev.get("N") or "")
    m_cl = re.match(r"\[Clase: ([^\]]+)\] \[Confianza: ([^\]]+)\]", n)
    if not m_cl:
        raise SystemExit(f"{k}: sin texto de fase en Control maestro N")
    clase_decl, conf = m_cl.group(1), m_cl.group(2)
    clase = "convencion" if clase_decl.startswith("convenci") else "hipotesis"
    fund = n + (f" [Evidencia preparada, Control maestro!M{ev['fila']}: {ev['M']}]" if ev.get("M") else "")
    h0 = e.get("hipotesis") or {}
    if h0.get("fundamento") == fund and e.get("clase") == clase and VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(k)):
        continue
    ref = re.search(r"(Referencia mecánica:.*?)(?=\s*Apoyo:|\s*Lo sustituiría:|$)", n, re.S)
    sust = re.search(r"(Lo sustituiría:.*)$", n, re.S)
    rango = re.search(r"(Rango[^.]*?\d[^.]*?)\.(?:\s|$)", n)
    fase = FASES.get(k)
    proc = f"Control maestro!N{ev.get('fila')} del libro (Jumbo_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e["clase"], e["valor_modelo"] = clase, INST["celdas"].get(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")), "fundamento": fund,
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    pendiente(e, f"texto vigente de la fase en jumbo_g (Control maestro!N{ev.get('fila')}); clase «{clase}» según la fase («{clase_decl}»)"
                 + (f"; valor {antes!r} → {e['valor_modelo']!r}" if not VE._igual_exacto(antes, e["valor_modelo"]) else ""), proc)
    hip.append(k)
reg["nota_jumbo_g_mercado_e_hipotesis"] = (f"{HOY}, {EXT}: C37, C57 y Palancas!C7 con los bytes de la persona responsable (Release, anexos 3 y 3 ter; fuentes_mercado/), "
                                           "C41/C42 de nuevo pendientes, C38 «Dato no verificable», hipótesis con el texto vigente de las fases de jumbo_g. "
                                           "Rastro: resultados/fuentes_mercado_y_registro_jumbo_g.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
rastro["registro"].update(despues_sha256=h(p), cambiadas=len({c["celda"] for c in cambios}), hipotesis_actualizadas=hip, cambios=cambios)
json.dump(rastro, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", rastro["registro"]["cambiadas"], "hipótesis", len(hip))
