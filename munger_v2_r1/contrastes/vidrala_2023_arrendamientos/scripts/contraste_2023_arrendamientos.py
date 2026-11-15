#!/usr/bin/env python3
"""Contraste de los datos de 2023 y de los arrendamientos 2023–2025 de Vidrala (entrega 4.2) · solo lectura.

Uso, desde la raíz munger_v2_r1/ del paquete:
    python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py > /tmp/salida.txt
    diff /tmp/salida.txt contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt     (debe salir vacío)

Lee, sin modificar nada:
  - textos nuevos generados con personaje_v2/scripts/pdf_a_texto.py desde los PDF oficiales descargados el 8-nov-2026:
    CF_2023 (EN, doc. 1831), CF_2024 (EN, doc. 2145) y CF_2024_ES (ES, doc. 2118; prevalece);
  - el texto nuevo CF_2025 del piloto (contrastes/piloto_Vidrala_2025/fuentes/texto_nuevo_CF_2025/);
  - los hechos numéricos del ESEF consolidado 2025 (doc. 2311), extraídos en el navegador (fuentes/esef_2311_extracto/);
  - el expediente original personaje_v2/empresas_v2/Vidrala/ (AR_2023, AR_2024, fase1_decisiones, fase1_v63,
    historia_revision.md y Vidrala_v63_evaluada.xlsx con sus valores en caché).
Las réplicas aritméticas no recalculan ni modifican el libro: repiten sus fórmulas sobre copias en memoria.
Código de salida: 0 si todas las comprobaciones marcadas CUMPLE dan el resultado esperado; 1 si alguna no.
"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True
RAIZ = os.getcwd()
if not os.path.exists(os.path.join(RAIZ, "VERSION")):
    sys.exit("Ejecutar desde la raíz munger_v2_r1/ del paquete")
AQ = os.path.join(RAIZ, "contrastes", "vidrala_2023_arrendamientos")
PIL = os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025")
EXP = os.path.join(RAIZ, "personaje_v2", "empresas_v2", "Vidrala")
sys.path.insert(0, os.path.join(RAIZ, "personaje_v2", "scripts"))
import fase1_historia as F  # noqa: E402
import openpyxl  # noqa: E402

fallos = []


def comprobar(nombre, cond, detalle=""):
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}{(' · ' + detalle) if detalle else ''}")
    if not cond:
        fallos.append(nombre)


def paginas(ruta):
    t = open(ruta, encoding="utf-8").read()
    p = re.split(r"^\[PDF PAGE (\d+)\]\n", t, flags=re.M)
    return {int(p[i]): p[i + 1] for i in range(1, len(p), 2)}


def num(tok):
    t = tok.strip()
    if t in ("-", "—"):
        return 0
    neg = t.startswith("(") or t.startswith("-") or t.endswith(")")
    d = re.sub(r"[()\-\s.,]", "", t)
    return -int(d) if neg else int(d)


TOK = r"\(?-?\d{1,3}(?:[.,]\d{3})*\)?|(?<![\w(])-(?![\w)])"


def dos(pag, inicio, n=2, contiene=False):
    """Últimos n importes de la primera línea de la página que empieza por `inicio` seguido de espacios e importe
    (o que lo contiene, con contiene=True)."""
    for ln in pag.splitlines():
        s = ln.strip()
        if contiene and inicio in s:
            toks = re.findall(TOK, s[s.index(inicio) + len(inicio):])
            return [num(t) for t in toks[-n:]], s
        if not contiene and s.startswith(inicio) and re.match(r"\s+(\(Note \d+\)\s+)?[\d(\-—]", s[len(inicio):] + " "):
            toks = re.findall(TOK, s[len(inicio):])
            return [num(t) for t in toks[-n:]], s
    raise KeyError(inicio)


def miles(x):
    return f"{x:,}".replace(",", ".")


P23 = paginas(os.path.join(AQ, "textos_nuevos", "CF_2023_EXTRACCION_NUEVA.txt"))
P24 = paginas(os.path.join(AQ, "textos_nuevos", "CF_2024_EXTRACCION_NUEVA.txt"))
E24 = paginas(os.path.join(AQ, "textos_nuevos", "CF_2024_ES_EXTRACCION_NUEVA.txt"))
P25 = paginas(os.path.join(PIL, "fuentes", "texto_nuevo_CF_2025", "CF_2025_EXTRACCION_NUEVA.txt"))
AR = {a: json.load(open(os.path.join(EXP, "fase1_partes", f"AR_{a}.json"), encoding="utf-8")) for a in (2023, 2024)}
DEC = json.load(open(os.path.join(EXP, "fase1_decisiones.json"), encoding="utf-8"))
F63 = json.load(open(os.path.join(EXP, "fase1_v63.json"), encoding="utf-8"))
REV = open(os.path.join(EXP, "historia_revision.md"), encoding="utf-8").read()
ESEF = json.load(open(os.path.join(AQ, "fuentes", "esef_2311_extracto", "esef_2025_hechos_numericos.json"), encoding="utf-8"))
XL = os.path.join(EXP, "Vidrala_v63_evaluada.xlsx")
wf, wv = openpyxl.load_workbook(XL), openpyxl.load_workbook(XL, data_only=True)
H, AN = wv["Historia"], wv["Análisis"]
hist = F63["historia"]["partidas"]
idx = {a: i for i, a in enumerate(F63["historia"]["anios"])}

print("CONTRASTE · DATOS DE 2023 Y ARRENDAMIENTOS 2023–2025 DE VIDRALA · salida reproducible (miles de euros salvo mm)")
print("=" * 104)

# ------------------------------------------------------------------------------------------------ 0 correspondencia
print("\n0 · CORRESPONDENCIA ENTRE AR_2023/AR_2024.json Y LOS TEXTOS NUEVOS (espacios normalizados)")
for a, PP in ((2023, P23), (2024, P24)):
    tot = ok = 0
    malas = []
    for k, v in AR[a]["partidas"].items():
        for lado in ("actual", "anterior"):
            for c in F.componentes(v.get(lado)):
                tot += 1
                if F.norm(c["linea"]) in F.norm(PP.get(c["pagina"], "")):
                    ok += 1
                else:
                    otras = [p for p, x in PP.items() if F.norm(c["linea"]) in F.norm(x)]
                    malas.append((k, lado, c["pagina"], otras))
    print(f"  AR_{a}.json → CF_{a}_EXTRACCION_NUEVA.txt: {ok} de {tot} líneas en su página; fuera de su página: {malas}")
    exactas = sum(any(c["linea"] == ln.strip() for ln in PP.get(c["pagina"], "").splitlines())
                  for v in AR[a]["partidas"].values() for lado in ("actual", "anterior") for c in F.componentes(v.get(lado)))
    print(f"  AR_{a}.json: líneas idénticas carácter a carácter (sin normalizar espacios): {exactas} de {tot}")
comprobar("AR_2023: todas las líneas citadas están en su página del texto nuevo", True if all(
    F.norm(c["linea"]) in F.norm(P23.get(c["pagina"], "")) for v in AR[2023]["partidas"].values()
    for lado in ("actual", "anterior") for c in F.componentes(v.get(lado))) else False)
da24 = [c for lado in ("actual", "anterior") for c in AR[2024]["partidas"]["da"][lado]]
comprobar("AR_2024: las dos líneas de D&A se citan en la p.4 pero están en la p.7 (cifra correcta, página mal atribuida)",
          all(F.norm(c["linea"]) not in F.norm(P24[4]) and F.norm(c["linea"]) in F.norm(P24[7]) for c in da24))

# ------------------------------------------------------------------------------------------------ 1 estados de flujos
AJ_EN23 = ["Amortisation and depreciation", "Impairment of non-current assets", "(Reversal of) impairment losses on trade receivables",
           "(Reversal of) impairment losses on inventories", "Exchange (gains) / losses", "Changes in provisions",
           "Government grants recognised in the income statement", "Finance income", "Finance costs", "Income tax "]
AJ_ES = ["Amortizaciones", "Pérdidas por deterioro de activos no corrientes", "Pérdidas (Reversiones) por deterioro de valor de deudores comerciales",
         "Pérdidas (Reversiones) por deterioro de valor de existencias", "(Ingresos) / Gastos por diferencias de cambio",
         "Variaciones de provisiones", "Imputación de subvenciones oficiales a resultados", "Ingresos financieros", "Gastos financieros",
         "Impuesto sobre las ganancias"]
CC_EN = ["Inventories", "Trade and other receivables", "Trade and other payables", "Other current liabilities", "of foreign operations"]
CC_ES = ["Existencias", "Deudores comerciales y otras cuentas a cobrar", "Acreedores comerciales y otras cuentas a pagar",
         "Otros activos y pasivos corrientes y no corrientes", None]


def bloque(pag, aj, cc, ben, sub_cc, ip, ir, tp, cfo, col):
    a = {x: dos(pag, x)[0][col] for x in aj}
    c = {}
    for x in cc:
        if x is None:  # línea de conversión en ES: los importes van en una línea aparte
            ln = [ln for ln in pag.splitlines() if re.fullmatch(r"\s*\(?[\d.]+\)?\s+\(?[\d.]+\)?\s*", ln)
                  and "Efecto de las diferencias" in pag.split(ln)[0][-300:]][0]
            c["conversión"] = [num(t) for t in re.findall(TOK, ln)][col]
        else:
            c[x] = dos(pag, x)[0][col]
    sub_aj_ln = [ln for ln in pag.splitlines() if re.fullmatch(r"\s*[\d.,]+\s+[\d.,]+\s*", ln)][0]
    sub_aj = [num(t) for t in re.findall(TOK, sub_aj_ln)][col]
    return dict(beneficio=dos(pag, ben)[0][col], ajustes=a, suma_aj=sum(a.values()), sub_aj=sub_aj, circ=c,
                suma_cc=sum(c.values()), sub_cc=dos(pag, sub_cc)[0][col], ip=dos(pag, ip)[0][col], ir=dos(pag, ir)[0][col],
                tp=dos(pag, tp)[0][col], cfo=dos(pag, cfo)[0][col])


print("\n1 · CFO Y CIRCULANTE DE 2023")
own = bloque(P23[7], AJ_EN23, CC_EN, "Profit for the year", "Cash used in operating activities", "Interest paid",
             "Interest received", "Income tax paid", "Net cash from operating activities", 0)
re_en = bloque(P24[7], AJ_EN23, CC_EN, "Profit for the year   ", "Cash used in operating activities", "Interest paid",
               "Interest received", "Income tax paid", "Net cash from operating activities", 1)
re_es = bloque(E24[14], AJ_ES, CC_ES, "Beneficio del ejercicio   ", "Efectivo generado por las operaciones", "Pagos de intereses",
               "Cobros de intereses", "Pagos por impuestos sobre las ganancias", "Efectivo neto generado por las actividades de explotación", 1)
for nom, b, cuadra in (("informe 2023 (EN, doc.1831, PDF p.7), columna 2023", own, True),
                       ("informe 2024 (EN, doc.2145, PDF p.7), columna 2023 reexpresada", re_en, False),
                       ("informe 2024 (ES, doc.2118, PDF p.14), columna 2023 reexpresada", re_es, True)):
    print(f"  · {nom}")
    if cuadra:
        comprobar("    suma de los 10 ajustes = subtotal impreso", b["suma_aj"] == b["sub_aj"], f"{miles(b['suma_aj'])} frente a {miles(b['sub_aj'])}")
    else:
        comprobar("    HALLAZGO EN EL DOCUMENTO: la suma de los 10 ajustes NO coincide con el subtotal impreso", b["suma_aj"] != b["sub_aj"],
                  f"{miles(b['suma_aj'])} frente a {miles(b['sub_aj'])}")
    comprobar("    suma de las 5 líneas de circulante = subtotal impreso", b["suma_cc"] == b["sub_cc"], f"{miles(b['suma_cc'])} = {miles(b['sub_cc'])}")
    calc = b["beneficio"] + b["sub_aj"] + b["sub_cc"] + b["ip"] + b["ir"] + b["tp"]
    comprobar("    beneficio + ajustes + circulante + intereses + impuestos = CFO impreso", calc == b["cfo"],
              f"{miles(b['beneficio'])} + {miles(b['sub_aj'])} + ({miles(b['sub_cc'])}) + ({miles(b['ip'])}) + {miles(b['ir'])} + ({miles(b['tp'])}) = {miles(calc)}")
# diferencias EN frente a ES en la columna reexpresada
dif_en_es = {AJ_EN23[i]: (re_en["ajustes"][AJ_EN23[i]], re_es["ajustes"][AJ_ES[i]]) for i in range(10)
             if re_en["ajustes"][AJ_EN23[i]] != re_es["ajustes"][AJ_ES[i]]}
print(f"  líneas de ajustes 2023 reexpresadas que difieren entre EN y ES (EN, ES): {dif_en_es}")
own22 = {x: dos(P23[7], x)[0][1] for x in AJ_EN23}
comprobar("las tres líneas EN que difieren repiten la columna 2022 del informe 2023",
          all(dif_en_es[k][0] == own22[k] for k in dif_en_es) and len(dif_en_es) == 3, f"{ {k: own22[k] for k in dif_en_es} }")
# diferencias informe 2023 frente a reexpresión (ES, que prevalece)
d = {AJ_EN23[i]: re_es["ajustes"][AJ_ES[i]] - own["ajustes"][AJ_EN23[i]] for i in range(10)}
d = {k: v for k, v in d.items() if v}
print(f"  reexpresado (ES) − informe 2023, por línea de ajustes: {d} · total {miles(sum(d.values()))}")
d_cc = re_es["circ"]["Otros activos y pasivos corrientes y no corrientes"] - own["circ"]["Other current liabilities"]
comprobar("la caída de los ajustes (−11.061) se compensa exactamente en «Otros activos y pasivos…» (+11.061); el resto del circulante no cambia",
          sum(d.values()) == -11061 and d_cc == 11061 and all(re_es["circ"][CC_ES[i]] == own["circ"][CC_EN[i]] for i in (0, 1, 2)),
          f"Δ ajustes {miles(sum(d.values()))} · Δ «Otros…» {miles(d_cc)} · circulante {miles(own['sub_cc'])} → {miles(re_es['sub_cc'])}")
p35 = P24[35]
it = {k: dos(p35, k, 1)[0][0] for k in ("Amortisation cost", "Impairment of non-current assets", "Finance cost", "Income Tax", "Other incomes")}
print(f"  nota de operaciones discontinuadas (EN 2024, PDF p.35), Italia 2023: {it}")
comprobar("las diferencias de amortización, deterioro, gasto financiero e impuesto coinciden con la cuenta de Italia 2023 de la p.35",
          d["Amortisation and depreciation"] == it["Amortisation cost"] and d["Impairment of non-current assets"] == it["Impairment of non-current assets"]
          and d["Finance costs"] == it["Finance cost"] and d["Income tax "] == it["Income Tax"],
          f"amortización {d['Amortisation and depreciation']} / {it['Amortisation cost']} · deterioro {d['Impairment of non-current assets']} / "
          f"{it['Impairment of non-current assets']} · gasto fin. {d['Finance costs']} / {it['Finance cost']} · impuesto {d['Income tax ']} / {it['Income Tax']}")
print(f"  subvenciones: Δ {d.get('Government grants recognised in the income statement')} frente a «Other incomes» de Italia {it['Other incomes']} "
      f"(diferencia de 1, sin explicación en el documento); deudores: Δ {d.get('(Reversal of) impairment losses on trade receivables')} sin línea propia en la p.35")
fl = re.sub(r"\s+", " ", p35)
m = re.search(r"Operating activities ([\d,]+) ([\d,]+) Investing activities ([\d,]+) \(([\d,]+)\)", fl)
print(f"  flujos de operaciones discontinuadas (p.35): explotación 2024 {m.group(1)} · 2023 {m.group(2)}; inversión 2024 {m.group(3)} · 2023 ({m.group(4)})")
comprobar("historia_revision.md registra 89,866 (informe 2023) frente a 78,805 (comparativo 2024) y aplica el más reciente",
          "**circulante_lineas 2023**: informe 2023 = 89.866 · comparativo del informe 2024 = 78.805" in REV)
comprobar("no hay decisiones registradas para cfo, capex, circulante ni arrendamientos de 2023",
          not any(k in DEC and "2023" in DEC[k] for k in ("cfo", "capex", "circulante_lineas", "arrendamientos_principal")))

print("\n2 · CAPEX DE 2023")
cx_own = [dos(P23[7], x)[0][0] for x in ("Payments from sale of property, plant and equipment", "Payments from sale of other intangible assets")]
cx_es = [dos(E24[14], x)[0][1] for x in ("Pagos por la adquisición de inmovilizado material", "Pagos por la adquisición de activos intangibles")]
comprobar("informe 2023 (EN) y comparativo 2024 (ES, «Pagos por la adquisición…») coinciden: 143.848 + 7.852",
          cx_own == cx_es == [-143848, -7852], f"{cx_own} · {cx_es}")
comprobar("capex 2023 del sistema = 151,700 mm y Historia J12 = 151,7", abs(hist["capex"]["valores"][idx[2023]] - 151.7) < 1e-9 and H["J12"].value == 151.7)
comprobar("CFO 2023: 263.437 en los tres textos y en Historia J11", own["cfo"] == re_en["cfo"] == re_es["cfo"] == 263437 and H["J11"].value == 263.437)

# ------------------------------------------------------------------------------------------------ 3 arrendamientos
print("\n3 · ARRENDAMIENTOS · nota 8 de los informes 2023 (p.52), 2024 (EN p.56, ES p.64) y 2025 (p.52)")
mov = {}
for nom, pag, col, lab in (("2022 (inf.2023)", P23[52], 1, "en"), ("2023 (inf.2023)", P23[52], 0, "en"), ("2023 (inf.2024)", P24[56], 1, "en"),
                           ("2024 (inf.2024)", P24[56], 0, "en"), ("2024 (inf.2024 ES)", E24[64], 0, "es"), ("2023 (inf.2024 ES)", E24[64], 1, "es"),
                           ("2025 (inf.2025)", P25[52], 0, "en")):
    if lab == "en":
        ks = ["Initial balance", "Additions due to business combinations", "Additions", "Accrued finance charges", "Payments", "Others",
              "Translation differences", "Final balance at 12/31"]
        kd = "leases of low-value items"
    else:
        ks = ["Saldo inicial", "Altas por combinaciones de negocio", "Adiciones", "Gastos financieros devengados", "Pagos", "Otros",
              "Diferencias conversión", "Saldo final a 31/12"]
        kd = "valor"  # rótulo partido en tres líneas: «Gastos relacionados / con arrendamientos / … de poco valor»
    v = {}
    for k in ks:
        try:
            v[k] = dos(pag, k)[0][col]
        except (KeyError, IndexError):
            v[k] = 0
    try:
        v["dup"] = dos(pag, kd)[0][col]
    except (KeyError, IndexError):
        v["dup"] = None
    vals = list(v.values())
    calc = sum(vals[:7])
    mov[nom] = v
    comprobar(f"{nom}: inicial + altas + devengo + pagos + otros + conversión = final", calc == vals[7],
              f"pagos {miles(vals[4])} · devengado {miles(vals[3])} · final {miles(vals[7])}")
    comprobar(f"{nom}: «gastos de arrendamientos a corto plazo y de poco valor» = −pagos", v["dup"] == -vals[4], f"{v['dup']}")
pagos = {2023: mov["2023 (inf.2024)"]["Payments"], 2024: mov["2024 (inf.2024)"]["Payments"], 2025: mov["2025 (inf.2025)"]["Payments"]}
devs = {2023: mov["2023 (inf.2024)"]["Accrued finance charges"], 2024: mov["2024 (inf.2024)"]["Accrued finance charges"],
        2025: mov["2025 (inf.2025)"]["Accrued finance charges"]}
comprobar("pago 2023 = −5.861 y devengo 2023 = 2.131 en los informes 2023 y 2024 (EN y ES)",
          mov["2023 (inf.2023)"]["Payments"] == mov["2023 (inf.2024)"]["Payments"] == mov["2023 (inf.2024 ES)"]["Pagos"] == -5861
          and mov["2023 (inf.2023)"]["Accrued finance charges"] == mov["2023 (inf.2024 ES)"]["Gastos financieros devengados"] == 2131)
fin = {}
for a, PP, p in ((2023, P23, 7), (2024, P24, 7), (2025, P25, 7)):
    lns = PP[p].splitlines()
    i0 = next(i for i, x in enumerate(lns) if x.strip() == "Cash flows from financing activities")
    i1 = next(i for i, x in enumerate(lns) if "Net cash from/(used in) financing activities" in x)
    bl = [x.strip() for x in lns[i0 + 1:i1] if x.strip()]
    fin[a] = bl
    comprobar(f"{a}: el bloque de financiación no tiene línea de arrendamientos ni de intereses",
              not any(re.search(r"(?i)lease|interest", x) for x in bl))
deuda = {}
for a, PP, p in ((2023, P23, 7), (2024, P24, 7), (2025, P25, 7)):
    s = 0
    for x in fin[a]:
        if re.search(r"(?i)loans and borrowings|other debts", x):
            toks = re.findall(r"\(?\d{1,3}(?:,\d{3})+\)?", x)  # primer importe con separador de miles = ejercicio corriente
            s += num(toks[0])
    deuda[a] = s
print(f"  línea 2022 del informe 2023 impresa como «{[x for x in fin[2023] if 'Proceeds' in x][0].split()[-1]}» (errata del documento; no afecta a 2023)")
ias = {2024: (P24[72], ["Current loans and borrowings", "Non-current loans and borrowings"]),
       2025: (P25[67], ["Current loans and borrowings", "Non-current loans and borrowings"]),
       2023: (P23[67], ["Current loans and borrowings", "Non-current loans and borrowings"])}
for a, (pag, ks) in ias.items():
    filas = []
    for k in ks:
        ln = next(x for x in pag.splitlines() if x.strip().startswith(k))
        filas.append([num(t) for t in re.findall(TOK, ln[ln.index(k) + len(k):])])
    ini = sum(f[0] for f in filas)
    fin_ = sum(f[-1] for f in filas)
    caja = sum(f[1] for f in filas)
    print(f"  {a}: flujos de deuda del estado de flujos {miles(deuda[a])} · variación del saldo de préstamos (incl. arrendamientos) {miles(fin_ - ini)} · "
          f"«cash flows» de la tabla NIC 7 {miles(caja)}")
comprobar("2024 y 2025: los flujos de deuda del estado de flujos igualan la variación total del saldo (incluidos movimientos no monetarios)",
          deuda[2024] == -205736 and deuda[2025] == -130399)
comprobar("2023: los flujos de deuda del estado de flujos (107.377) no igualan ni la variación del saldo ni los «cash flows» NIC 7", deuda[2023] == 107377)
nombres = {h["name"] for h in ESEF["hechos_numericos"]}
lease_tags = sorted(n for n in nombres if re.search(r"(?i)lease", n))
comprobar("ESEF 2025: ninguna etiqueta numérica de arrendamientos (todo el texto de notas va en bloques)", lease_tags == [], f"{len(nombres)} conceptos, {len(ESEF['hechos_numericos'])} hechos")
ip = [h for h in ESEF["hechos_numericos"] if h["name"] == "ifrs-full:InterestPaidClassifiedAsOperatingActivities"]
comprobar("ESEF 2025: «Pagos de intereses» etiquetado como InterestPaidClassifiedAsOperatingActivities (20.800 / 32.100)",
          sorted(h["texto"] for h in ip) == ["20.800", "32.100"])
fin_tags = sorted({(h["name"], h["texto"]) for h in ESEF["hechos_numericos"] if h["contextRef"] == "c-3" and
                   re.search(r"Borrowings|OtrasDeudas|EntidadesDeCredito", h["name"])})
print(f"  ESEF 2025, financiación 2025: {fin_tags}")
print(f"  pagos totales de arrendamientos (nota 8) 2023–2025: {pagos} · gasto devengado: {devs}")
b24 = re.search(r"monthly amortization payments of ([\d,.]+) thousand euros \(([\d,.]+) thousand British pounds\)", re.sub(r"\s+", " ", P24[75]))
b25 = re.search(r"monthly instalments of EUR ([\d,.]+) thousand \(GBP ([\d,.]+) thousand\).{0,400}?compared with GBP ([\d,.]+) thousand in 2024",
                re.sub(r"\s+", " ", P25[69]))
comprobar("arrendamiento de Bristol (5 %, cuotas mensuales hasta feb-2034): informe 2024 p.75 = 466 miles € (387 miles £) al mes",
          b24 is not None and b24.groups() == ("466", "387"), f"{b24.groups() if b24 else None}")
comprobar("HALLAZGO EN EL DOCUMENTO: el informe 2025 (p.69) atribuye a 2024 una cuota de 354 miles £, no 387", b25 is not None and b25.group(3) == "354",
          f"{b25.groups() if b25 else None}")
print(f"  orden de magnitud (aritmética, no evidencia de principal): 466 × 12 = {miles(466 * 12)} frente a pagos 2024 {miles(-pagos[2024])}; "
      f"554 × 12 = {miles(554 * 12)} frente a pagos 2025 {miles(-pagos[2025])}")

# ------------------------------------------------------------------------------------------------ 4 recorrido y réplicas
print("\n4 · RECORRIDO HASTA EL LIBRO Y RÉPLICAS ARITMÉTICAS (sin recalcular el libro)")
for k, r in (("cfo", 11), ("capex", 12), ("circulante", 14), ("arrendamientos_principal", 17), ("da", 8)):
    fu = [x for x in hist[k]["fuente"].split("; ") if x.startswith("2023 ")]
    print(f"  {k}: fase1_v63 2023 = {hist[k]['valores'][idx[2023]]} · Historia J{r} = {H.cell(r, 10).value} · fuente: {fu[0] if fu else '—'}")
print(f"  Análisis C46 {AN['C46'].value} · C47 {AN['C47'].value} · C48 {AN['C48'].value} · C49 {AN['C49'].value} · C50 {AN['C50'].value} · C52 {AN['C52'].value}")
win = H["C57"].value
cols = list(range(13 - win, 13))
V = [H.cell(6, c).value for c in cols]
E = [H.cell(7, c).value for c in cols]
DA = [H.cell(8, c).value for c in cols]
T = [H.cell(10, c).value for c in cols]
CX = [H.cell(12, c).value for c in cols]
CI = [H.cell(14, c).value for c in cols]


def f_de(circ, fcf):
    c74 = sum(V) / win
    c75 = sum(e * (1 - t) for e, t in zip(E, T)) / win
    c76 = sum(x - d_ + ci for x, d_, ci in zip(CX, DA, circ)) / win
    return c76, (c75 - c76) - fcf, ((c75 - c76) - fcf) / c74


base = f_de(CI, H["C70"].value)
comprobar("la réplica reproduce la f del libro", abs(base[2] - H["C58"].value) < 1e-12, f"{base[2]:.6f}")
print("  Entradas constantes en todas las réplicas: ventas, EBIT, tipo y D&A 2023–2025 (Historia J–L 6, 7, 8, 10), capex (fila 12),")
print("  ventana C57 = 3. Solo cambia lo que indica cada línea.")
esc = [("libro (2023 = 78,805 · 2024 = −127,840)", CI, H["C70"].value),
       ("2024 corregido a 84,994; 2023 = 78,805", [CI[0], 84.994, CI[2]], H["C70"].value),
       ("2024 corregido a 84,994; 2023 = 89,866 (presentación del informe 2023)", [89.866, 84.994, CI[2]], H["C70"].value),
       ("2024 sin corregir; 2023 = 89,866", [89.866, CI[1], CI[2]], H["C70"].value)]
for nom, ci, fcf in esc:
    c76, c79, fx = f_de(ci, fcf)
    print(f"  réplica · {nom}: C76 {c76:.4f} · C79 {c79:.4f} · f {fx:.6f}")
c46 = sum(hist["cfo"]["valores"][idx[a]] for a in (2023, 2024, 2025)) / 3
c47 = sum(hist["capex"]["valores"][idx[a]] for a in (2023, 2024, 2025)) / 3
comprobar("C46 y C47 son las medias 2023–2025 de CFO y capex (redondeadas a un decimal)", round(c46, 1) == AN["C46"].value and round(c47, 1) == AN["C47"].value,
          f"{c46:.4f} · {c47:.4f}")
m_pagos = sum(-pagos[a] for a in pagos) / 3000
m_dif = sum(-pagos[a] - devs[a] for a in pagos) / 3000
print(f"  arrendamientos (sensibilidad condicionada, no límites): media de pagos totales {m_pagos:.4f} · media de pagos − devengado {m_dif:.4f} (C49 = {AN['C49'].value})")
for c49 in (round(m_dif, 1), round(m_pagos, 1), 0.0):
    fcf = AN["C46"].value - AN["C47"].value - AN["C48"].value - c49 - AN["C50"].value
    _, _, fx = f_de(CI, fcf)
    print(f"    C49 = {c49}: FCF base {fcf:.1f} · f (circulante del libro) {fx:.6f}")

print("\n" + "=" * 104)
print(f"RESULTADO: {'todas las comprobaciones esperadas se cumplen' if not fallos else 'NO se cumplen: ' + '; '.join(fallos)}")
sys.exit(1 if fallos else 0)
