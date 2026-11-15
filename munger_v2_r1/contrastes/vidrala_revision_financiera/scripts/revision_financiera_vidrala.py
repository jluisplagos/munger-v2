#!/usr/bin/env python3
"""Munger v2 · entrega 4.3 · revisión financiera del piloto Vidrala (solo lectura).

Qué hace:
  1. Comprueba la huella de las fuentes que usa (textos conservados en entregas anteriores y el ESEF 2025 completo).
  2. Comprueba cada cifra citada contra el texto de su página (etiqueta y cifra en la misma frase) y,
     para 2024 y 2025, contra los hechos etiquetados del ESEF 2025 completo.
  3. Lee los valores en caché de Vidrala_v63_evaluada.xlsx (Historia y Análisis) sin escribir nada.
  4. Construye la matriz de perímetro de la ventana 2023–2025.
  5. Descompone por año la diferencia que genera f y replica f con los tratamientos comparados.
  6. Comprueba la disponibilidad de las entradas del motor B.

No escribe en el paquete, no crea __pycache__ (ejecutar con «python3 -I») y no recalcula libros.
Las réplicas son aritmética reproducible: no son valoraciones ni acreditan las hipótesis.
Importes: miles de euros en las fuentes; millones (mm) en el sistema.
"""
import hashlib
import html
import os
import re
import sys
import zipfile

sys.dont_write_bytecode = True
import openpyxl  # noqa: E402

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
EXP = os.path.join(RAIZ, "personaje_v2", "empresas_v2", "Vidrala")
C42 = os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos")
C41 = os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025")
AQUI = os.path.join(RAIZ, "contrastes", "vidrala_revision_financiera")

FUENTES = {
    "ES24": (os.path.join(C42, "textos_nuevos", "CF_2024_ES_EXTRACCION_NUEVA.txt"),
             "39a91c9cc9c68f447d9227238a6cd90299774b48fb68ea6e622782fdb00b526d",
             "informe 2024, español (D9, doc. 2118); prevalece"),
    "EN24": (os.path.join(C42, "textos_nuevos", "CF_2024_EXTRACCION_NUEVA.txt"),
             "fd37a10ecd5933b3bd6fb9355923d07be1e0190caad98fc715abb1233f3b7f7f",
             "informe 2024, inglés (D7, doc. 2145)"),
    "EN23": (os.path.join(C42, "textos_nuevos", "CF_2023_EXTRACCION_NUEVA.txt"),
             "8fbc85ec5aa773c7129d86af84e11a9323eaa82b40d3090be66c5a0db44962b0",
             "informe 2023, inglés (D6, doc. 1831)"),
    "EN25": (os.path.join(C41, "fuentes", "texto_nuevo_CF_2025", "CF_2025_EXTRACCION_NUEVA.txt"),
             "ebfe0f35db7e30adf6ec381a610d30c4a56bc3ca59da24fe4c5af5b60aa6a4e4",
             "informe 2025, inglés (D1, doc. 2355)"),
}
ESEF = (os.path.join(AQUI, "fuentes", "esef_2025_completo", "2311_en-2025_esef_consolidated_information.zip"),
        "14264d1f0a07f1bc3c7273450e393ddbe0587855293b487447319dcd1c7bde90")

N_OK = 0
N_TOTAL = 0


def comprobar(nombre, cond, detalle=""):
    global N_OK, N_TOTAL
    N_TOTAL += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}" + (f" · {detalle}" if detalle else ""))
    return bool(cond)


def sha(ruta):
    h = hashlib.sha256()
    with open(ruta, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def paginas(ruta):
    t = open(ruta, encoding="utf-8").read()
    p = re.split(r"^\[PDF PAGE (\d+)\]\n", t, flags=re.M)
    return {int(p[i]): re.sub(r"\s+", " ", p[i + 1]) for i in range(1, len(p), 2)}


def num(tok):
    """Cifra entera en miles: «(1.478)», «1,588,267», «-». Los separadores de miles se eliminan."""
    t = tok.strip()
    if t in ("-", "—"):
        return 0
    neg = t.startswith("(") or t.endswith(")")
    t = t.strip("()").replace(".", "").replace(",", "")
    return -int(t) if neg else int(t)


def miles(x):
    return f"{x:,.0f}".replace(",", ".")


def mm(x, d=3):
    s = f"{x + 0.0:,.{d}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


TXT = {}


def cita(doc, pag, etiqueta, *tokens, ventana=420):
    """Devuelve True si en la página aparece la etiqueta seguida, en ese orden y dentro de la ventana,
    de los tokens indicados (cifras tal como se imprimen)."""
    texto = TXT[doc][pag]
    for m in re.finditer(etiqueta, texto, flags=re.I):
        trozo = texto[m.end(): m.end() + ventana]
        pos, ok = 0, True
        for tk in tokens:
            mt = re.search(r"(?<![\d.,])" + re.escape(tk) + r"(?![\d])", trozo[pos:])
            if not mt:
                ok = False
                break
            pos += mt.end()
        if ok:
            return True
    return False


def V(doc, pag, etiqueta, *tokens, nombre=None, ventana=420):
    """Comprueba la cita y devuelve el valor numérico de los tokens (miles)."""
    ok = cita(doc, pag, etiqueta, *tokens, ventana=ventana)
    comprobar(nombre or f"{doc} p.{pag} «{etiqueta}» {' · '.join(tokens)}", ok)
    vals = [num(t) for t in tokens]
    return vals if len(vals) > 1 else vals[0]


# ───────────────────────────────────────────────────────────────────────────────────────────────
print("REVISIÓN FINANCIERA DEL PILOTO VIDRALA · entrega 4.3 · script de solo lectura")
print("=" * 100)
print("\n1. HUELLAS DE LAS FUENTES")
for k, (ruta, h, desc) in FUENTES.items():
    comprobar(f"{k} = {desc}: SHA-256 {h[:12]}…", os.path.exists(ruta) and sha(ruta) == h)
    TXT[k] = paginas(ruta)
comprobar(f"ESEF 2025 completo (doc. 2311): SHA-256 {ESEF[1][:12]}…, 35.979.149 bytes",
          sha(ESEF[0]) == ESEF[1] and os.path.getsize(ESEF[0]) == 35979149)

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n2. CIFRAS CITADAS (etiqueta y cifra en la misma frase de la página indicada)")
D = {2023: {}, 2024: {}, 2025: {}}

print("  2.1 Cuenta de resultados de operaciones continuadas · 2024 y 2023 reexpresado (ES24 p.11)")
D[2024]["ventas"], D[2023]["ventas"] = V("ES24", 11, r"Ventas", "1.588.267", "1.427.473")
D[2024]["ebit"], D[2023]["ebit"] = V("ES24", 11, r"Ganancia pérdida por actividades de explotación", "331.008", "267.508")
D[2024]["fin_ing_pl"], D[2023]["fin_ing_pl"] = V("ES24", 11, r"Ingresos financieros", "14.267", "8.483")
D[2024]["fin_gas_pl"], D[2023]["fin_gas_pl"] = V("ES24", 11, r"Gastos financieros", "(42.551)", "(12.949)")
D[2024]["equiv"], D[2023]["equiv"] = V("ES24", 11, r"sociedades puestas", "494", "5.607")
D[2024]["bai"], D[2023]["bai"] = V("ES24", 11, r"Beneficio antes de impuestos de actividades", "303.218", "268.649")
D[2024]["imp"], D[2023]["imp"] = V("ES24", 11, r"Gasto por impuesto sobre las ganancias", "(64.968)", "(54.813)")
D[2024]["ben_c"], D[2023]["ben_c"] = V("ES24", 11, r"Beneficio del ejercicio de actividades continuadas", "238.250", "213.836")
D[2024]["disc"], D[2023]["disc"] = V("ES24", 11, r"Beneficio del ejercicio de actividades discontinuadas", "60.065", "19.559")

print("  2.2 Estado de flujos 2024 y 2023 reexpresado (ES24 p.14)")
p14 = [("amort", r"Amortizaciones", "117.720", "87.210"),
       ("det_anc", r"deterioro de activos no corrientes", "5.231", "5.659"),
       ("det_deu", r"deterioro de valor de deudores comerciales", "1.182", "(1.478)"),
       ("det_exi", r"deterioro de valor de existencias", "3.052", "1.213"),
       ("dif_cam", r"Gastos por diferencias de cambio", "2.245", "(131)"),
       ("prov", r"Variaciones de provisiones", "20.024", "10.647"),
       ("subv", r"subvenciones oficiales a resultados", "(266)", "(4.116)"),
       ("fin_ing_aj", r"Ingresos financieros", "(14.267)", "(8.352)"),
       ("fin_gas_aj", r"Gastos financieros", "40.306", "12.949"),
       ("imp_aj", r"Impuesto sobre las ganancias", "64.968", "54.813")]
for clave, et, a24, a23 in p14:
    D[2024][clave], D[2023][clave] = V("ES24", 14, et, a24, a23)
D[2024]["ajustes"], D[2023]["ajustes"] = V("ES24", 14, r"Impuesto sobre las ganancias 10 64\.968 54\.813", "240.195", "158.414",
                                            nombre="ES24 p.14 total de ajustes 240.195 · 158.414")
D[2024]["otros_ap"], D[2023]["otros_ap"] = V("ES24", 14, r"Otros activos y pasivos corrientes y no corrientes", "(106.417)", "47.199")
D[2024]["circ_cf"], D[2023]["circ_cf"] = V("ES24", 14, r"Efectivo generado por las operaciones", "(84.994)", "(78.805)")
D[2024]["int_pag"], D[2023]["int_pag"] = V("ES24", 14, r"Pagos de intereses", "(32.100)", "(12.320)")
D[2024]["int_cob"], D[2023]["int_cob"] = V("ES24", 14, r"Cobros de intereses", "11.200", "7.774")
D[2024]["imp_pag"], D[2023]["imp_pag"] = V("ES24", 14, r"Pagos por impuestos sobre las ganancias", "(70.100)", "(45.021)")
D[2024]["cfo"], D[2023]["cfo"] = V("ES24", 14, r"Efectivo neto generado por las actividades de explotación", "362.516", "263.437")
D[2024]["capex_m"], D[2023]["capex_m"] = V("ES24", 14, r"adquisición de inmovilizado material", "(160.063)", "(143.848)")
D[2024]["capex_i"], D[2023]["capex_i"] = V("ES24", 14, r"adquisición de activos intangibles", "(8.737)", "(7.852)")
D[2024]["ben_tot"], D[2023]["ben_tot"] = V("ES24", 14, r"operaciones discontinuadas 60\.065 19\.559 Beneficio del ejercicio", "298.315", "233.395",
                                            nombre="ES24 p.14 Beneficio del ejercicio 298.315 · 233.395")
venta_italia = V("ES24", 14, r"Flujos de efectivo procedentes pérdida de control de dependientes", "230.000")
otros_enaj = V("ES24", 14, r"Otros efectos enajenación", "11.668")

print("  2.3 Italia: venta, plusvalía, primer semestre de 2024, 2023 y flujos (ES24 p.42–43; EN25 p.31)")
comprobar("ES24 p.42: «asciende a una plusvalía de 50 millones de euros» en «Beneficio del periodo de actividades discontinuadas»",
          cita("ES24", 42, r"asciende a una plusvalía de", "50") and "actividades discontinuadas" in TXT["ES24"][42])
comprobar("EN25 p.31 (cita de fase_a.md): «amounted to a gain of 50 million euros»", "amounted to a gain of 50 million euros" in TXT["EN25"][31])
ita24 = {"ventas": V("ES24", 42, r"desglose: Miles de € Ventas", "43.646"),
         "amort": V("ES24", 42, r"Gastos por amortización", "(304)"),
         "fin": V("ES24", 42, r"Gastos financieros", "(45)"),
         "bai": V("ES24", 42, r"BENEFICIO ANTES DE IMPUESTOS DE ACTIVIDADES DISCONTINUADAS", "10.020"),
         "imp": V("ES24", 42, r"Gasto por impuesto sobre las ganancias", "(503)"),
         "ben": V("ES24", 42, r"BENEFICIO DEL PERIODO DE ACTIVIDADES DISCONTINUADAS", "9.518")}
ita23 = {"ventas": V("ES24", 43, r"siguiente detalle: Miles de € Ventas", "131.292"),
         "amort": V("ES24", 43, r"Gastos por amortización", "(10.655)"),
         "fin": V("ES24", 43, r"Gastos financieros", "(3.486)"),
         "bai": V("ES24", 43, r"BENEFICIO ANTES DE IMPUESTOS", "18.844"),
         "imp": V("ES24", 43, r"Gasto por impuesto sobre las ganancias", "715"),
         "ben": V("ES24", 43, r"BENEFICIO DEL PERIODO", "19.559")}
ita_op24, ita_op23 = V("ES24", 43, r"Actividades de explotación", "11.558", "26.732")
ita_inv24, ita_inv23 = V("ES24", 43, r"Actividades de inversión", "230.000", "(28.371)")
seg_ita24 = {"ventas": V("ES24", 37, r"Ventas y prestación de servicios", "742.267", "17.016")[1],
             "amort": V("ES24", 37, r"Gastos por amortización", "(51.196)", "(1.822)")[1],
             "bai": V("ES24", 37, r"Beneficio antes de impuestos de actividades continuadas", "163.853", "2.139")[1]}
comprobar("ES24 p.69: las diferencias permanentes (28.095) son «principalmente» la exención de la plusvalía de Italia",
          cita("ES24", 69, r"Diferencias permanentes", "(28.095)") and "exención asociada por la plusvalía" in TXT["ES24"][69])
inv_geo23 = V("EN23", 30, r"Italy 229,277 52,430", "4,315", nombre="EN23 p.30 «Investments» de Italia 2023 (altas de inmovilizado material e intangible): 4,315")
comprobar("EN24 p.31: Italia 2023 (*) reexpresado con inversiones 4,315 y sin fila de 2024", cita("EN24", 31, r"Italy - - -", "229,277", "52,430", "4,315"))

print("  2.3b Impuesto corriente del ejercicio (ES24 p.69; EN25 p.56)")
D[2024]["imp_corr"], D[2023]["imp_corr"] = V("ES24", 69, r"Impuesto corriente del ejercicio", "65.376", "63.249")
D[2025]["imp_corr"], _c24 = V("EN25", 56, r"Current tax", "56,136", "65,376")
comprobar("El impuesto corriente de 2024 coincide en los informes de 2024 y 2025 (65.376)", _c24 == D[2024]["imp_corr"])
print("  2.4 Ejercicio 2025 (EN25 p.4 y p.7) y 2023 según su propio informe (EN23 p.4 y p.7)")
D[2025]["ventas"] = V("EN25", 4, r"Revenues 4 & 22", "1,465,160")
D[2025]["ebit"] = V("EN25", 4, r"Profit loss from operating activities", "292,068")
D[2025]["fin_ing_pl"] = V("EN25", 4, r"Finance income 26", "15,101")
D[2025]["fin_gas_pl"] = V("EN25", 4, r"Finance costs 26", "(31,001)")
D[2025]["equiv"] = V("EN25", 4, r"accounted for using the equity", "493")
D[2025]["bai"] = V("EN25", 4, r"Profit before income tax from continuing operations", "276,661")
D[2025]["imp"] = V("EN25", 4, r"Income tax expense 10", "(67,320)")
D[2025]["ben_c"] = V("EN25", 4, r"Profit for the year from continuing operations", "209,341")
D[2025]["disc"] = 0
comprobar("EN25 p.4: el beneficio de actividades discontinuadas de 2025 es «-»", cita("EN25", 4, r"Profit for the year from discontinuing operations", "-", "60,065"))
p7 = [("amort", r"Amortisation and depreciation 7&8", "132,948"), ("det_anc", r"Impairment of non-current assets 7&8", "2,362"),
      ("det_deu", r"impairment losses on trade receivables", "(1,228)"), ("det_exi", r"impairment losses on inventories 11", "1,280"),
      ("dif_cam", r"Exchange \(gains\) / losses 26", "-"), ("prov", r"Changes in provisions", "3,829"),
      ("subv", r"Government grants recognised in the income statement 22", "(3,453)"), ("fin_ing_aj", r"Finance income 26", "(9,864)"),
      ("fin_gas_aj", r"Finance costs 26", "31,001"), ("imp_aj", r"Income tax 10", "67,320"),
      ("int_pag", r"Interest paid", "(20,800)"), ("int_cob", r"Interest received", "7,509"),
      ("imp_pag", r"Income tax paid", "(40,757)"), ("cfo", r"Net cash from operating activities", "380,287"),
      ("capex_m", r"Payments from sale of property, plant and equipment", "(178,746)"),
      ("capex_i", r"Payments from sale of other intangible assets", "(9,757)")]
for clave, et, tk in p7:
    D[2025][clave] = V("EN25", 7, et, tk)
D[2025]["ajustes"] = V("EN25", 7, r"Income tax 10 67,320", "224,195", nombre="EN25 p.7 total de ajustes 224,195")
D[2025]["circ_cf"] = V("EN25", 7, r"Cash used in operating activities", "799")
D[2025]["ben_tot"] = V("EN25", 7, r"discontinuing operations - 60,065 Profit for the year", "209,341", nombre="EN25 p.7 Profit for the year 209,341")
own23 = {"ventas": V("EN23", 4, r"Revenues 4 & 22", "1,558,765"), "ebit": V("EN23", 4, r"Profit loss from operating activities", "289,838"),
         "amort": V("EN23", 4, r"Amortisation and depreciation 7&8", "(97,865)"), "imp": V("EN23", 4, r"Income tax expense 10", "(54,098)"),
         "bai": V("EN23", 4, r"Profit before income tax from continuing operations", "287,493"),
         "ajustes": V("EN23", 7, r"Income tax 10 54,098", "169,475", nombre="EN23 p.7 total de ajustes 169,475"),
         "cfo": V("EN23", 7, r"Net cash from operating activities", "263,437")}

comprobar("EN25 p.29: Vidroporto aportó en 2023 ventas de 19,147 (desde la compra) frente a 154,969 si se hubiera comprado el 1 de enero",
          cita("EN25", 29, r"amounting to EUR", "19,147") and cita("EN25", 29, r"would have amounted to EUR", "154,969"))
print("  2.5 Cuadres internos de cada estado de flujos")
for y in (2023, 2024, 2025):
    d = D[y]
    lineas = sum(d[k] for k in ("amort", "det_anc", "det_deu", "det_exi", "dif_cam", "prov", "subv", "fin_ing_aj", "fin_gas_aj", "imp_aj"))
    comprobar(f"{y}: suma de las líneas de ajuste = total impreso ({miles(d['ajustes'])})", lineas == d["ajustes"])
    comprobar(f"{y}: beneficio continuadas + discontinuadas = beneficio del ejercicio ({miles(d['ben_tot'])})", d["ben_c"] + d["disc"] == d["ben_tot"])
    cfo = d["ben_tot"] + d["ajustes"] + d["circ_cf"] + d["int_pag"] + d["int_cob"] + d["imp_pag"]
    comprobar(f"{y}: beneficio + ajustes + circulante + intereses + impuestos = CFO impreso ({miles(d['cfo'])})", cfo == d["cfo"])
    ebit_recalc = d["bai"] - d["fin_ing_pl"] - d["fin_gas_pl"] - d["equiv"]
    comprobar(f"{y}: BAI − resultado financiero − puesta en equivalencia = EBIT ({miles(d['ebit'])})", ebit_recalc == d["ebit"])
comprobar("Italia 1S 2024: 43.646 + 775 − 2.667 − 20.862 − 5.013 − 304 − 1 − 5.508 − 45 = 10.021 ≈ BAI 10.020 (redondeo de 1)",
          abs(43646 + 775 - 2667 - 20862 - 5013 - 304 - 1 - 5508 - 45 - ita24["bai"]) <= 1)
comprobar("Italia 1S 2024: 10.020 − 503 = 9.518 (redondeo de 1)", abs(ita24["bai"] + ita24["imp"] - ita24["ben"]) <= 1)
plusvalia = D[2024]["disc"] - ita24["ben"]
comprobar(f"Discontinuadas 2024 = 60.065 = 9.518 (Italia 1S) + {miles(plusvalia)} (plusvalía; la nota la redondea a «50 millones»)",
          abs(plusvalia - 50000) < 1000, f"{miles(plusvalia)} miles")
ebit_ita23 = ita23["bai"] - ita23["fin"]
comprobar("EN23 propio 2023: EBIT 289.838 = continuadas reexpresado 267.508 + EBIT de Italia 22.330 (BAI 18.844 + gasto financiero 3.486)",
          own23["ebit"] == D[2023]["ebit"] + ebit_ita23, f"EBIT de Italia 2023 {miles(ebit_ita23)}")
comprobar("EN23 propio 2023: ventas 1.558.765 = continuadas 1.427.473 + Italia 131.292", own23["ventas"] == D[2023]["ventas"] + ita23["ventas"])
comprobar("Ajustes 2023: propio 169.475 − reexpresado 158.414 = 11.061 (ajustes no monetarios de Italia, entrega 4.2)",
          own23["ajustes"] - D[2023]["ajustes"] == 11061)

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n3. CONTRASTE CON EL ESEF 2025 COMPLETO (hechos etiquetados sin dimensión; 2025 y comparativo 2024)")
z = zipfile.ZipFile(ESEF[0])
xh = [n for n in z.namelist() if n.endswith(".xhtml")]
comprobar("El ZIP del ESEF tiene 9 miembros y un único informe XHTML", len(z.namelist()) == 9 and len(xh) == 1, xh[0] if xh else "")
x = z.read(xh[0]).decode("utf-8")
ctx = {}
for m in re.finditer(r'<xbrli:context id="([^"]+)">(.*?)</xbrli:context>', x, re.S):
    b = m.group(2)
    if "segment" in b:
        continue
    p = re.search(r"<xbrli:startDate>([^<]+)</xbrli:startDate>\s*<xbrli:endDate>([^<]+)", b)
    i = re.search(r"<xbrli:instant>([^<]+)", b)
    ctx[m.group(1)] = (p.group(2)[:4] if p else i.group(1)[:4], "D" if p else "I")
hechos = {}
for m in re.finditer(r"<ix:nonFraction([^>]*)>(.*?)</ix:nonFraction>", x, re.S):
    a = dict(re.findall(r'([\w:]+)="([^"]*)"', m.group(1)))
    c = ctx.get(a.get("contextRef"))
    if not c:
        continue
    txt = re.sub(r"<[^>]+>", "", m.group(2)).strip()
    val = 0 if txt in ("-", "") else float(txt.replace(".", "").replace(",", "."))
    if a.get("sign") == "-":
        val = -val
    hechos.setdefault((a["name"], c[0], c[1]), set()).add(val)
print(f"  Hechos numéricos sin dimensión leídos: {sum(len(v) for v in hechos.values())} (conceptos y periodos: {len(hechos)})")
texto_esef = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", x)))


def esef(concepto, anio, esperado, signo=1, tipo="D"):
    vals = hechos.get(("ifrs-full:" + concepto, str(anio), tipo), set())
    return comprobar(f"ESEF {concepto} {anio} = {miles(esperado)}", (signo * esperado) in vals or esperado in vals, f"etiquetado {sorted(vals)}")


for y in (2024, 2025):
    d = D[y]
    esef("Revenue", y, d["ventas"])
    esef("ProfitLossFromOperatingActivities", y, d["ebit"])
    esef("DepreciationAndAmortisationExpense", y, d["amort"])
    esef("ProfitLossBeforeTax", y, d["bai"])
    esef("IncomeTaxExpenseContinuingOperations", y, -d["imp"])
    esef("ProfitLossFromContinuingOperations", y, d["ben_c"])
    esef("ProfitLoss", y, d["ben_tot"])
    esef("AdjustmentsForReconcileProfitLoss", y, d["ajustes"])
    esef("AdjustmentsForProvisions", y, d["prov"])
    esef("InterestPaidClassifiedAsOperatingActivities", y, -d["int_pag"])
    esef("InterestReceivedClassifiedAsOperatingActivities", y, d["int_cob"])
    esef("IncomeTaxesPaidRefundClassifiedAsOperatingActivities", y, -d["imp_pag"])
    esef("CashFlowsFromUsedInOperatingActivities", y, d["cfo"])
    esef("PurchaseOfPropertyPlantAndEquipmentClassifiedAsInvestingActivities", y, -d["capex_m"])
    esef("PurchaseOfIntangibleAssetsClassifiedAsInvestingActivities", y, -d["capex_i"])
esef("ProfitLossFromDiscontinuedOperations", 2024, D[2024]["disc"])
esef("AdjustmentsForIncreaseDecreaseInOtherOperatingPayables", 2024, D[2024]["otros_ap"], signo=1)
comprobar("ESEF: ningún concepto etiquetado identifica la plusvalía de Italia ni su reversión en el estado de flujos",
          not any(re.search(r"(?i)gain.*dispos|disposal.*gain|GainsLossesOnDisposalOfInvestments", k[0]) for k in hechos))
comprobar("ESEF (texto, versión española que prevalece): «ascendió a una plusvalía de 50 millones de euros» y el resultado del primer semestre de Italia «9.518 miles»",
          "ascendió a una plusvalía de 50 millones de euros" in texto_esef and "ascendió a 9.518 miles de euros" in texto_esef)
comprobar("ESEF (texto): el beneficio de 2025 se compara «en perímetro comparable, es decir, ajustado por la contribución de Italia a resultados de 2024 y por la plusvalía contable»",
          "ajustado por la contribución de Italia a resultados de 2024 y por la plusvalía contable" in texto_esef)

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n4. VALORES EN CACHÉ DEL LIBRO (Vidrala_v63_evaluada.xlsx, solo lectura)")
XL = os.path.join(EXP, "Vidrala_v63_evaluada.xlsx")
huella_libro = sha(XL)
wv = openpyxl.load_workbook(XL, data_only=True)
H, AN = wv["Historia"], wv["Análisis"]
COL = {2023: 10, 2024: 11, 2025: 12}
FILAS = {"ventas": 6, "ebit": 7, "da": 8, "tipo": 10, "cfo": 11, "capex": 12, "adq": 13, "circ": 14, "int_hist": 15, "arr_hist": 17}
L = {y: {k: H.cell(r, c).value for k, r in FILAS.items()} for y, c in COL.items()}
for y in COL:
    print(f"  {y}: " + " · ".join(f"{k} {L[y][k]}" for k in FILAS))
C = {k: H[k].value for k in ("C57", "C58", "C70", "C74", "C75", "C76", "C77", "C78", "C79", "C52", "C63", "C64", "C65", "C66")}
A = {k: AN[k].value for k in ("C46", "C47", "C48", "C49", "C50", "C51", "C52", "C41")}
print("  Historia: " + " · ".join(f"{k} {v}" for k, v in C.items()))
print("  Análisis: " + " · ".join(f"{k} {v}" for k, v in A.items()))
comprobar("Motor activo A (Diagnóstico V6 C5) y f del motor = Historia C58", wv["Diagnóstico V6"]["C5"].value == "A" and wv["Diagnóstico V6"]["C12"].value == C["C58"])
comprobar("Semáforo de f (Diagnóstico V6 C50, rango −0,02 a 0,05) en «✓ PASA» con el libro", str(wv["Diagnóstico V6"]["C50"].value).startswith("✓ PASA"))

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n5. MATRIZ DE PERÍMETRO (libro frente a fuente; C = continuadas; C+I = incluye Italia)")


def igual(a, b, tol=0.0005):
    return a is not None and b is not None and abs(a - b) <= tol


ts = {y: -D[y]["imp"] / D[y]["bai"] for y in D}
filas_m = []
for y in (2023, 2024, 2025):
    d, l = D[y], L[y]
    capex = -(d["capex_m"] + d["capex_i"]) / 1000
    filas_m += [
        (y, "ventas (6)", l["ventas"], d["ventas"] / 1000, "C" if y < 2025 else "C = consolidado",
         "ES24 p.11" if y < 2025 else "EN25 p.4", igual(l["ventas"], d["ventas"] / 1000)),
        (y, "EBIT (7)", l["ebit"], d["ebit"] / 1000, "C" if y < 2025 else "C = consolidado", "ES24 p.11" if y < 2025 else "EN25 p.4",
         igual(l["ebit"], d["ebit"] / 1000)),
        (y, "D&A (8)", l["da"], d["amort"] / 1000, "C" if y < 2025 else "C = consolidado", "ES24 p.14" if y < 2025 else "EN25 p.7",
         igual(l["da"], d["amort"] / 1000)),
        (y, "tipo (10)", l["tipo"], ts[y], "C (impuesto ÷ BAI de continuadas)", "ES24 p.11" if y < 2025 else "EN25 p.4",
         igual(l["tipo"], round(ts[y], 4), 1e-9)),
        (y, "CFO (11)", l["cfo"], d["cfo"] / 1000, "C+I" if y < 2025 else "C = consolidado", "ES24 p.14" if y < 2025 else "EN25 p.7",
         igual(l["cfo"], d["cfo"] / 1000)),
        (y, "capex (12)", l["capex"], capex, "C+I" if y < 2025 else "C = consolidado", "ES24 p.14" if y < 2025 else "EN25 p.7",
         igual(l["capex"], capex, 0.051)),
        (y, "circulante (14)", l["circ"], -d["circ_cf"] / 1000, "C+I y partidas no monetarias" if y < 2025 else "C = consolidado",
         "ES24 p.14" if y < 2025 else "EN25 p.7", igual(l["circ"], -d["circ_cf"] / 1000)),
    ]
for y, k, libro, fuente, per, fu, ok in filas_m:
    comprobar(f"{y} {k}: libro {libro} · fuente {mm(fuente, 4)} · perímetro {per} · {fu}", ok if k != "circulante (14)" or y != 2024 else not ok,
              "NO coincide: es la corrección P1 (fuente 84,994)" if (k == "circulante (14)" and y == 2024) else "")
comprobar("Capex 2024 del libro 168,8 = 160,063 + 8,737 redondeado a un decimal (168,800)", L[2024]["capex"] == 168.8)

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n6. DESCOMPOSICIÓN DE LA DIFERENCIA QUE GENERA f (por año, mm)")
print("""  Identidad (Historia C74–C80 y Análisis C52, ventana C57 = 3):
     f·V = media(NOPAT − (capex − D&A + circ)) − (C46 − C47 − C48 − C49 − C50)
         = media(NOPAT + D&A − (CFO + circ)) + C48 + C49 + C50 + (C47 − media capex) − (C46 − media CFO)
  El capex se anula (solo queda el redondeo de C47). D&A entra en la reinversión (C76), no en el NOPAT (C75 = EBIT·(1 − t)).
  Si el circulante y el CFO salen del mismo estado de flujos, CFO + circ = flujo antes de circulante (FAC):
     FAC = beneficio del ejercicio + ajustes + intereses cobrados − intereses pagados − impuestos pagados
  y la diferencia anual g = NOPAT + D&A − FAC se descompone, sin residuo, en:
     g = − discontinuadas − X + (impuestos pagados − t·EBIT) + (intereses pagados − intereses cobrados)
  con X = (beneficio de continuadas + ajustes) − (EBIT + D&A): partidas no monetarias y resultado no operativo de continuadas.""")
V_ = {y: L[y]["ventas"] for y in D}
R = {}
for y in (2023, 2024, 2025):
    d, l = D[y], L[y]
    t = l["tipo"]
    nopat = l["ebit"] * (1 - t)
    fac = (d["ben_tot"] + d["ajustes"] + d["int_cob"] + d["int_pag"] + d["imp_pag"]) / 1000
    comprobar(f"{y}: FAC {mm(fac)} = CFO {mm(d['cfo'] / 1000)} + circulante del mismo estado {mm(-d['circ_cf'] / 1000)}",
              abs(fac - (d["cfo"] - d["circ_cf"]) / 1000) < 1e-9)
    disc = d["disc"] / 1000
    X = (d["ben_c"] + d["ajustes"]) / 1000 - (l["ebit"] + l["da"])
    imp_gap = -d["imp_pag"] / 1000 - t * l["ebit"]
    imp_tim = (-d["imp_pag"] + d["imp"]) / 1000
    imp_acc = -d["imp"] / 1000 - t * l["ebit"]
    neti = (-d["int_pag"] - d["int_cob"]) / 1000
    g = nopat + l["da"] - fac
    comprobar(f"{y}: g = −disc − X + (imp. pagados − t·EBIT) + intereses netos pagados (sin residuo)", abs(g - (-disc - X + imp_gap + neti)) < 1e-9)
    Xl = {"provisiones": d["prov"], "deterioros": d["det_anc"] + d["det_deu"] + d["det_exi"], "subvenciones": d["subv"],
          "dif. cambio": d["dif_cam"], "puesta en equivalencia": d["equiv"],
          "ingresos fin. (cuenta − ajuste)": d["fin_ing_pl"] + d["fin_ing_aj"], "gastos fin. (ajuste − cuenta)": d["fin_gas_aj"] + d["fin_gas_pl"]}
    comprobar(f"{y}: X = suma de sus líneas ({mm(X)})", abs(sum(Xl.values()) / 1000 - X) < 0.0015)
    R[y] = dict(nopat=nopat, da=l["da"], fac=fac, g=g, disc=disc, X=X, imp_gap=imp_gap, imp_tim=imp_tim, imp_acc=imp_acc, neti=neti, Xl=Xl, t=t)
    print(f"  {y}: NOPAT {mm(nopat)} + D&A {mm(l['da'])} − FAC {mm(fac)} = g {mm(g)}")
    print(f"        −discontinuadas {mm(-disc)} · −X {mm(-X)} · impuestos pagados − t·EBIT {mm(imp_gap)} "
          f"(pagado − devengado {mm((-d['imp_pag'] + d['imp']) / 1000)}; devengado − t·EBIT {mm(imp_acc)}) · intereses netos pagados {mm(neti)}")
    print(f"        impuesto: devengado {mm(-d['imp'] / 1000)} · corriente {mm(d['imp_corr'] / 1000)} · pagado {mm(-d['imp_pag'] / 1000)} → "
          f"corriente − pagado {mm((d['imp_corr'] + d['imp_pag']) / 1000)} · devengado − corriente (diferido y ajustes) {mm((-d['imp'] - d['imp_corr']) / 1000)}")
    print("        X por líneas: " + " · ".join(f"{k} {mm(v / 1000)}" for k, v in Xl.items()))
Vm = sum(V_.values()) / 3
red = (A["C47"] - sum(L[y]["capex"] for y in D) / 3) - (A["C46"] - sum(L[y]["cfo"] for y in D) / 3)
print(f"  Ventas medias {mm(Vm, 4)} · redondeo de C46 y C47 a un decimal: {mm(red, 5)} mm (≈ {red / Vm:.6f} de f)")
print("  Medias de la ventana y su peso en f (mm/año ÷ ventas medias):")
comp = [("discontinuadas (Italia y plusvalía)", -sum(R[y]["disc"] for y in D) / 3),
        ("X (partidas no monetarias y no operativas)", -sum(R[y]["X"] for y in D) / 3),
        ("impuestos: pagado − devengado", sum((R[y]["imp_gap"] - R[y]["imp_acc"]) for y in D) / 3),
        ("impuestos: devengado − t·EBIT (escudo y redondeo de t)", sum(R[y]["imp_acc"] for y in D) / 3),
        ("intereses netos pagados", sum(R[y]["neti"] for y in D) / 3),
        ("C49 arrendamientos (hipótesis vigente 4,5)", A["C49"]), ("C48 + C50", A["C48"] + A["C50"]),
        ("redondeo de C46 y C47", red)]
for k, v in comp:
    print(f"    {k:55s} {mm(v):>9s} mm · {v / Vm:+.6f}")
f_T1 = sum(v for _, v in comp) / Vm
tim = sum((D[y]["imp_corr"] + D[y]["imp_pag"]) / 1000 for y in D) / 3
dif = sum((-D[y]["imp"] - D[y]["imp_corr"]) / 1000 for y in D) / 3
print(f"    de «pagado − devengado»: corriente no pagado en el año {mm(-tim)} mm · diferido y ajustes {mm(-dif)} mm")
comprobar("Pagado − devengado = −(corriente − pagado) − (devengado − corriente)",
          abs(sum((R[y]["imp_gap"] - R[y]["imp_acc"]) for y in D) / 3 - (-tim - dif)) < 1e-9)
print(f"    {'f con circulante y CFO del mismo estado (T1)':55s} {'':>9s}    · {f_T1:+.6f}")

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n7. RÉPLICAS DE f POR TRATAMIENTO (fórmulas de Historia C74:C80 y Análisis C52; constantes salvo lo indicado)")


def f_de(circ, c46, c47=None, c49=None, capex=None, anos=(2023, 2024, 2025)):
    c47 = A["C47"] if c47 is None else c47
    c49 = A["C49"] if c49 is None else c49
    capex = {y: L[y]["capex"] for y in D} if capex is None else capex
    n = len(anos)
    vm = sum(L[y]["ventas"] for y in anos) / n
    c75 = sum(L[y]["ebit"] * (1 - L[y]["tipo"]) for y in anos) / n
    c76 = sum(capex[y] - L[y]["da"] + circ[y] for y in anos) / n
    c70 = c46 - c47 - A["C48"] - c49 - A["C50"]
    c79 = c75 - c76 - c70
    return c79 / vm, c70, c76, c79


circ_libro = {y: L[y]["circ"] for y in D}
circ_P1 = {**circ_libro, 2024: 84.994}
circ_P1b = {**circ_P1, 2023: 89.866}
f0 = f_de(circ_libro, A["C46"])
comprobar(f"T0 libro: f = {f0[0]:.6f} = Historia C58", abs(f0[0] - C["C58"]) < 1e-12)
T = {"T0 libro (K14 = −127,840, no procede del estado de flujos)": f0,
     "T1 corrección factual P1 (K14 = 84,994; J14 = 78,805)": f_de(circ_P1, A["C46"]),
     "T2 T1 y J14 = 89,866 (presentación del informe 2023)": f_de(circ_P1b, A["C46"])}
comprobar("T1 = suma de componentes de la sección 6", abs(T["T1 corrección factual P1 (K14 = 84,994; J14 = 78,805)"][0] - f_T1) < 1e-12)
# T3: perímetro de continuadas. CFO_c = CFO − flujo de explotación de Italia (nota 5); FAC_c = FAC − discontinuadas.
cfo_c = {2023: L[2023]["cfo"] - ita_op23 / 1000, 2024: L[2024]["cfo"] - ita_op24 / 1000, 2025: L[2025]["cfo"]}
fac_c = {y: R[y]["fac"] - R[y]["disc"] for y in D}
circ_c = {y: fac_c[y] - cfo_c[y] for y in D}
c46_c = sum(cfo_c.values()) / 3
print(f"  CFO de continuadas (CFO − explotación de Italia, nota 5): " + " · ".join(f"{y} {mm(v)}" for y, v in cfo_c.items()) + f" · media {mm(c46_c, 4)}")
print(f"  FAC de continuadas (FAC − discontinuadas): " + " · ".join(f"{y} {mm(v)}" for y, v in fac_c.items()))
print(f"  Circulante derivado de continuadas (FAC_c − CFO_c; no publicado, residuo): " + " · ".join(f"{y} {mm(v)}" for y, v in circ_c.items()))
comprobar("Circulante derivado 2024 = 84,994 − plusvalía + (explotación de Italia − beneficio de Italia 1S)",
          abs(circ_c[2024] - (84.994 - plusvalia / 1000 + (ita_op24 - ita24["ben"]) / 1000)) < 1e-9)
T["T3 perímetro de continuadas (preferente si se mantiene el motor A)"] = f_de(circ_c, c46_c)
# δ: parte de Italia en intereses e impuestos pagados (no publicada); cota con su devengo
delta = {2023: (-ita23["fin"]) / 1000 + max(0, -ita23["imp"]) / 1000, 2024: (-ita24["fin"] - ita24["imp"]) / 1000, 2025: 0.0}
circ_cd = {y: circ_c[y] + delta[y] for y in D}
T["T3δ T3 con la parte de Italia en intereses e impuestos pagados aproximada por su devengo (hipótesis)"] = f_de(circ_cd, c46_c)
T["T3a T3 con C49 = 6,8 (sensibilidad condicionada)"] = f_de(circ_c, c46_c, c49=6.8)
T["T3b T3 con C49 = 0 (sensibilidad condicionada)"] = f_de(circ_c, c46_c, c49=0.0)
# T4: normalización estructural (hipótesis): impuestos pagados = devengados, X = 0, sin discontinuadas.
g_s = {y: R[y]["imp_acc"] + R[y]["neti"] for y in D}
f_s = (sum(g_s.values()) / 3 + A["C49"] + A["C48"] + A["C50"]) / Vm
T["T4 normalización (hipótesis): solo intereses netos pagados, escudo fiscal devengado y C49"] = (f_s, None, None, f_s * Vm)
for k, (fx, c70, c76, c79) in T.items():
    marca = "*" if k.startswith("T3") else ""
    extra = f" · C70{marca} {mm(c70, 4)} · C76 {mm(c76, 4)}" if c70 is not None else ""
    print(f"  {k}: f = {fx:+.6f}{extra} · C79 {mm(c79, 4)} · semáforo {'PASA' if -0.02 <= fx <= 0.05 else 'REVISAR'}")
print("  * En T3, C70 combina CFO de continuadas con el capex consolidado de la fila 12: no es un FCF base con significado propio; f no depende de él (ver abajo).")
comprobar("T1 reproduce la réplica A de la entrega 4.2 (−0,027608)", abs(T["T1 corrección factual P1 (K14 = 84,994; J14 = 78,805)"][0] - (-0.027608)) < 5e-7)
comprobar("T2 reproduce la réplica B de la entrega 4.2 (−0,030076)", abs(T["T2 T1 y J14 = 89,866 (presentación del informe 2023)"][0] - (-0.030076)) < 5e-7)
f3 = T["T3 perímetro de continuadas (preferente si se mantiene el motor A)"][0]
media_cfo = sum(L[y]["cfo"] for y in D) / 3
comprobar("T3 − T1 = (media de las discontinuadas + redondeo de C46 que T1 arrastra) ÷ ventas medias",
          abs(f3 - (f_T1 + (sum(R[y]["disc"] for y in D) / 3 + (A["C46"] - media_cfo)) / Vm)) < 1e-12)
comprobar("f no depende del capex si la fila 12 y C47 cambian lo mismo (+10 mm cada año y en C47)",
          abs(f_de(circ_c, c46_c, c47=A["C47"] + 10, capex={y: L[y]["capex"] + 10 for y in D})[0] - f3) < 1e-12)
comprobar("Con el perímetro de continuadas f sigue siendo negativa", f3 < 0)
print("  Por año, (g + C49) ÷ ventas del año, con T1 y con el perímetro de continuadas (T3):")
for y in D:
    print(f"    {y}: T1 g {mm(R[y]['g'])} → {(R[y]['g'] + A['C49']) / V_[y]:+.6f} · T3 g_c {mm(R[y]['g'] + R[y]['disc'])} → {(R[y]['g'] + R[y]['disc'] + A['C49']) / V_[y]:+.6f}")
print("  Diagnóstico de ventana (no es una propuesta de cambiar C57):")
for anos in ((2024, 2025), (2025,)):
    fx = f_de(circ_c, sum(cfo_c[y] for y in anos) / len(anos), c47=sum(L[y]["capex"] for y in anos) / len(anos), anos=anos)[0]
    print(f"    perímetro de continuadas, ventana {anos}: f = {fx:+.6f}")
comprobar("Ni la ventana 2024–2025 ni 2025 solo dan una f positiva con el perímetro de continuadas",
          all(f_de(circ_c, sum(cfo_c[y] for y in a) / len(a), c47=sum(L[y]["capex"] for y in a) / len(a), anos=a)[0] < 0 for a in ((2024, 2025), (2025,))))

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n8. COMPOSICIÓN DEL FLUJO DE INVERSIÓN DE ITALIA Y FCF BASE DE CONTINUADAS")
print(f"  2023: flujo de inversión de Italia {mm(ita_inv23 / 1000)}; «Investments» de Italia (altas, devengo) {mm(inv_geo23 / 1000)}; "
      f"diferencia no explicada por los documentos {mm((-ita_inv23 - inv_geo23) / 1000)}")
comprobar("El flujo de inversión de Italia 2023 no es su capex: las altas de Italia (4,315) son el 15 % del flujo (28,371)", inv_geo23 / -ita_inv23 < 0.2)
print(f"  2024: flujo de inversión de Italia {mm(ita_inv24 / 1000)} = cobro de la venta {mm(venta_italia / 1000)}; capex del primer semestre no publicado.")
print(f"  C46 de continuadas {mm(c46_c, 4)} (evidencia: CFO y nota 5). C47 de continuadas no determinable con evidencia (capex de Italia 1S 2024 no publicado;"
      f" en 2023 solo hay altas por devengo).")
c47_h = (L[2023]["capex"] - inv_geo23 / 1000 + L[2024]["capex"] + L[2025]["capex"]) / 3
print(f"  Réplica condicionada (hipótesis: capex de Italia 2023 ≈ sus altas 4,315; 1S 2024 = 0): C47 {mm(c47_h, 4)} → FCF base {mm(c46_c - c47_h - A['C49'], 4)} "
      f"frente a 161,2 (no es una valoración ni un dato).")

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n9. ARRENDAMIENTOS: QUÉ MIDEN 4,5 Y 6,8 (nota 8; entrega 4.2) Y EFECTO EN f")
pagos = {2023: 5861, 2024: 6117, 2025: 8314}
interes = {2023: 2131, 2024: 2179, 2025: 2452}
m_pagos = sum(pagos.values()) / 3000
m_princ = sum(pagos[y] - interes[y] for y in pagos) / 3000
comprobar(f"Media de pagos totales 2023–2025 = {mm(m_pagos, 4)} → 6,8 a un decimal", round(m_pagos, 1) == 6.8)
comprobar(f"Media de (pagos − interés devengado) = {mm(m_princ, 4)} → 4,5 a un decimal (C49 vigente, heredado de la V5.3)", round(m_princ, 1) == 4.5)
comprobar("Fila 17 de Historia (J17:L17) = pagos totales de la nota 8, no principal", [L[y]["arr_hist"] for y in D] == [5.861, 6.117, 8.314])
print(f"  Efecto en f de cada 1 mm de C49: {1 / Vm:+.6f}. Recorrido 0 → 6,8: {6.8 / Vm:+.6f}.")

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n10. ENTRADAS DEL MOTOR B (último ejercicio, 31-dic-2025) Y SU RESPALDO")
deuda_tot = V("EN25", 3, r"Non-current liabilities Deferred income 15 41,117 8,291 Loans and borrowings 16", "196,080", nombre="EN25 p.3 préstamos no corrientes 196,080")
deuda_cor = V("EN25", 3, r"Current liabilities Loans and borrowings 16", "66,833")
caja = V("EN25", 2, r"Cash and cash equivalents", "108,352")
arr = V("EN25", 52, r"Final balance at 12/31", "49,300")
pers = V("EN25", 71, r"At 31 December 2025", "46,366", "6,223", nombre="EN25 p.71 provisión de personal 6,223 a 31-dic-2025")
V("EN25", 71, r"Charge against profit or loss", "46,366", "1,463", "1,697", "49,526", nombre="EN25 p.71 provisiones 2025: cargo 49,526 (derechos de emisión 46,366)")
V("EN25", 71, r"Payments", "(50,699)", "(50,699)", nombre="EN25 p.71 provisiones 2025: «Payments» (entregas de derechos) 50,699")
comprobar("EN25 p.72: la provisión de derechos de emisión recoge «the estimated surrender of emission allowances»", "estimated surrender of emission allowances" in TXT["EN25"][72])
comprobar("Historia L22 + L23 = préstamos del balance (196,080 + 66,833 = 262,913), arrendamientos incluidos", abs(H["L22"].value + H["L23"].value - (deuda_tot + deuda_cor) / 1000) < 1e-9)
comprobar("Historia L23 = pasivo por arrendamientos de la nota 8 (49,300)", H["L23"].value == arr / 1000)
comprobar("Historia L24 = caja del balance (108,352)", H["L24"].value == caja / 1000)
comprobar("Historia L15 = intereses pagados 2025 (20,8)", H["L15"].value == -D[2025]["int_pag"] / 1000)
comprobar("Historia L25 (6,223) = provisión «Personnel», que incluye planes de prestación definida «y otras obligaciones con empleados» (definición más amplia que la fila)",
          H["L25"].value == pers[1] / 1000 and "defined benefit plans and other obligations with employees" in TXT["EN25"][72])
comprobar("Historia L26 = 0 (cero heredado) y el balance de 2025 no presenta línea de minoritarios: evidencia candidata para la revisión humana; la IA no confirma el cero",
          H["L26"].value == 0 and "Equity attributed to equity holders of the Parent" in TXT["EN25"][3] and not re.search(r"(?i)non-controlling|minority", TXT["EN25"][3]))
comprobar("Historia C63 = L15 ÷ media(K22 + K23, L22 + L23)", abs(C["C63"] - H["L15"].value / ((H["K22"].value + H["K23"].value + H["L22"].value + H["L23"].value) / 2)) < 1e-12,
          f"{C['C63']:.6f}")
r_inv = AN["C56"].value
r_op = A["C41"] and (r_inv * A["C41"] / (A["C41"] + C["C64"]) + C["C63"] * (1 - C["C52"]) * C["C64"] / (A["C41"] + C["C64"]))
print(f"  r operativa que daría la convención 4 con los datos del libro (r = Análisis C56 = {r_inv}, sin cambiarla): {r_op:.6f}. Es aritmética de la fórmula, no una valoración.")
print("  Fechas: el puente del motor B usa saldos a 31-dic-2025; Análisis C53 y C54 (30-jun-2026: caja 109,4; deuda 409,6) son contexto y no entran.")

# ───────────────────────────────────────────────────────────────────────────────────────────────
print("\n11. OTRA ENTRADA MATERIAL AFECTADA POR P1: S2C MARGINAL DE REFERENCIA (Historia C53, referencia mecánica de la fase B)")
cols = {2021: 8, 2022: 9, 2023: 10, 2024: 11, 2025: 12}
fila31 = {y: H.cell(31, c).value for y, c in cols.items()}
num53 = H["L6"].value - H["G6"].value
comprobar(f"Historia C53 del libro = (L6 − G6) ÷ SUMA(H31:L31) = {mm(num53)} ÷ {mm(sum(fila31.values()))}", abs(H["C53"].value - num53 / sum(fila31.values())) < 1e-12,
          f"{H['C53'].value:.4f}")
k31_p1 = L[2024]["capex"] - L[2024]["da"] + 84.994 + L[2024]["adq"]
suma_p1 = sum(fila31.values()) - fila31[2024] + k31_p1
print(f"  Con K14 = 84,994: K31 {mm(fila31[2024])} → {mm(k31_p1)}; SUMA(H31:L31) {mm(sum(fila31.values()))} → {mm(suma_p1)}; C53 {H['C53'].value:.4f} → {num53 / suma_p1:.4f}")
print("  Perímetro de C53: G6 (2020) incluye Italia y L6 (2025) no; J31 incluye la compra de Vidroporto (254,086) y K31 el cobro de Italia (−241,668).")
fila30 = {y: H.cell(30, c).value for y, c in cols.items()}
s30 = sum(fila30.values())
s30_p1 = s30 - fila30[2024] + (L[2024]["capex"] - L[2024]["da"] + 84.994)
s30_c = s30 - fila30[2023] - fila30[2024] + (L[2023]["capex"] - L[2023]["da"] + circ_c[2023]) + (L[2024]["capex"] - L[2024]["da"] + circ_c[2024])
ventas_sin_br = num53 - 178.267
print(f"  Cuenta de la fase B (fase_b.md: «295 mm de reinversión orgánica, H30:L30, para ≈300 mm de ventas sin Brasil» → ≈1,0):")
print(f"    ventas 2025 − 2020 − Brasil 2025 = {mm(ventas_sin_br)} · SUMA(H30:L30) libro {mm(s30)} → {ventas_sin_br / s30:.2f} · con P1 {mm(s30_p1)} → {ventas_sin_br / s30_p1:.2f}"
      f" · con el circulante derivado de continuadas en 2023–2024 {mm(s30_c)} → {ventas_sin_br / s30_c:.2f}")
comprobar("La reinversión orgánica que sostenía el S2C del NORMAL (≈295 mm) lleva dentro el error de K14", abs(s30 - 295.3) < 0.5)
comprobar("P1 baja la referencia S2C de la fase B por debajo de 1 (la fase B decidió 1,0 en el NORMAL frente a una referencia de 1,5)", num53 / suma_p1 < 1)

print("\n12. INTEGRIDAD")
comprobar("El libro no ha cambiado durante la ejecución", sha(XL) == huella_libro, huella_libro[:12] + "…")
print(f"\nRESULTADO: {N_OK} de {N_TOTAL} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_TOTAL else 1)
