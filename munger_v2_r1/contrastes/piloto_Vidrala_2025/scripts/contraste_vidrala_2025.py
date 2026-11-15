#!/usr/bin/env python3
"""Contraste acotado del piloto Vidrala 2025 (CFO, capex, arrendamientos, adquisiciones) · solo lectura.

Uso, desde la raíz munger_v2_r1/ del paquete:
    python3 -I contrastes/piloto_Vidrala_2025/scripts/contraste_vidrala_2025.py > /tmp/salida.txt
    diff /tmp/salida.txt contrastes/piloto_Vidrala_2025/resultados/contraste_salida.txt     (debe salir vacío)

Lee, sin modificar nada:
  - el texto nuevo CF_2025 (fuentes/texto_nuevo_CF_2025/), generado con personaje_v2/scripts/pdf_a_texto.py desde el PDF
    descargado el 8-nov-2026 (fuentes/en_2355_descarga_2026-11-08/);
  - el extracto de la versión española (fuentes/es_2308_extracto/), obtenido con pdf.js en el navegador;
  - el expediente original personaje_v2/empresas_v2/Vidrala/ (AR_2024.json, AR_2025.json, fase1_decisiones.json,
    fase1_v63.json, historia_revision.md y Vidrala_v63_evaluada.xlsx, con sus valores en caché).
Reproduce los cuadres del documento, sigue cada dato hasta el libro y replica la conciliación de f (Historia C74:C80).
Código de salida: 0 si todas las comprobaciones marcadas como CUMPLE dan el resultado esperado; 1 si alguna no.
No escribe archivos (PYTHONDONTWRITEBYTECODE implícito: sys.dont_write_bytecode).
"""
import json
import os
import re
import sys

sys.dont_write_bytecode = True
RAIZ = os.getcwd()
if not os.path.exists(os.path.join(RAIZ, "VERSION")):
    sys.exit("Ejecutar desde la raíz munger_v2_r1/ del paquete")
PIL = os.path.join(RAIZ, "contrastes", "piloto_Vidrala_2025")
EXP = os.path.join(RAIZ, "personaje_v2", "empresas_v2", "Vidrala")
sys.path.insert(0, os.path.join(RAIZ, "personaje_v2", "scripts"))
import fase1_historia as F  # noqa: E402  (se usa su numero(): así se reproduce exactamente la lectura del sistema)
import openpyxl  # noqa: E402

fallos = []


def comprobar(nombre, cond, detalle=""):
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}{(' · ' + detalle) if detalle else ''}")
    if not cond:
        fallos.append(nombre)


def paginas_pipeline(ruta):
    t = open(ruta, encoding="utf-8").read()
    partes = re.split(r"^\[PDF PAGE (\d+)\]\n", t, flags=re.M)
    return {int(partes[i]): partes[i + 1] for i in range(1, len(partes), 2)}


def num(tok):
    """Lectura estricta: exige paréntesis equilibrados; devuelve (valor, aviso)."""
    t = tok.strip()
    if t in ("-", "—"):
        return 0, None
    aviso = None
    if t.count("(") != t.count(")"):
        aviso = f"paréntesis desequilibrado en «{t}»"
    neg = t.startswith("(") or t.startswith("-") or t.endswith(")")
    d = t.strip("()- ").replace(",", "").replace(".", "")
    return (-int(d) if neg else int(d)), aviso


TOK = r"\(?-?[\d.,]+\)?|(?<!\w)-(?!\w)"


def fila(pag, inicio):
    """Primera línea de la página que empieza por `inicio`; devuelve (línea, [tokens numéricos de las dos columnas])."""
    for ln in pag.splitlines():
        if ln.strip().startswith(inicio):
            resto = ln.strip()[len(inicio):]
            toks = re.findall(TOK, resto)
            return ln.strip(), toks[-2:]
    raise KeyError(inicio)


def dos(pag, inicio):
    ln, toks = fila(pag, inicio)
    v = [num(t) for t in toks]
    return [x[0] for x in v], [x[1] for x in v if x[1]], ln, toks


print("CONTRASTE ACOTADO · VIDRALA 2025 · salida reproducible (miles de euros salvo que se indique mm)")
print("=" * 100)

# ---------------------------------------------------------------------------------------------------------- fuentes
P = paginas_pipeline(os.path.join(PIL, "fuentes", "texto_nuevo_CF_2025", "CF_2025_EXTRACCION_NUEVA.txt"))
ES = open(os.path.join(PIL, "fuentes", "es_2308_extracto", "extracto_pdfjs_paginas_14_y_58.txt"), encoding="utf-8").read()
AR25 = json.load(open(os.path.join(EXP, "fase1_partes", "AR_2025.json"), encoding="utf-8"))
AR24 = json.load(open(os.path.join(EXP, "fase1_partes", "AR_2024.json"), encoding="utf-8"))
DEC = json.load(open(os.path.join(EXP, "fase1_decisiones.json"), encoding="utf-8"))
F63 = json.load(open(os.path.join(EXP, "fase1_v63.json"), encoding="utf-8"))
REV = open(os.path.join(EXP, "historia_revision.md"), encoding="utf-8").read()
XL = os.path.join(EXP, "Vidrala_v63_evaluada.xlsx")
wf = openpyxl.load_workbook(XL, data_only=False)
wv = openpyxl.load_workbook(XL, data_only=True)

print("\n0 · CORRESPONDENCIA ENTRE AR_2025.json Y EL TEXTO NUEVO")
tot = ok = 0
for k, v in AR25["partidas"].items():
    for lado in ("actual", "anterior"):
        for c in F.componentes(v.get(lado)):
            tot += 1
            ok += any(c["linea"] == ln.strip() for ln in P[c["pagina"]].splitlines())
comprobar("cada «linea» de AR_2025.json está, carácter a carácter, en su página del texto nuevo", ok == tot, f"{ok} de {tot}")
print(f"  páginas del texto nuevo: {len(P)} · archivo citado en AR_2025.json: {AR25['archivo']} · unidad: {AR25['unidad']}")

p7 = P[7]
COLS = ("2025", "2024")

# ---------------------------------------------------------------------------------------------------------- 4.1 CFO
print("\n4.1 · CFO · estado de flujos consolidado, PDF p.7 (versión inglesa) y PDF p.14 (versión española)")
AJ = ["Amortisation and depreciation", "Impairment of non-current assets", "(Reversal of) impairment losses on trade receivables",
      "(Reversal of) impairment losses on inventories", "Exchange (gains) / losses", "Changes in provisions",
      "Government grants recognised in the income statement", "Finance income", "Finance costs", "Income tax "]
CC = ["Inventories", "Trade and other receivables", "Trade and other payables", "Other current liabilities", "of foreign operations"]
beneficio, _, _, _ = dos(p7, "Profit for the year   ")
aj = [dos(p7, x) for x in AJ]
suma_aj = [sum(a[0][i] for a in aj) for i in range(2)]
sub_aj = [num(t)[0] for t in re.findall(TOK, next(ln for ln in p7.splitlines() if re.fullmatch(r"\s*224,195\s+240,195\s*", ln)))]
cc = [dos(p7, x) for x in CC]
avisos = [a for c in cc for a in c[1]]
suma_cc = [sum(c[0][i] for c in cc) for i in range(2)]
sub_cc, _, _, _ = dos(p7, "Cash used in operating activities")
ip, _, _, _ = dos(p7, "Interest paid")
ir, _, _, _ = dos(p7, "Interest received")
tp, _, _, _ = dos(p7, "Income tax paid")
cfo, _, _, _ = dos(p7, "Net cash from operating activities")
for i, a in enumerate(COLS):
    comprobar(f"{a}: suma de los 10 ajustes = subtotal impreso sin rótulo", suma_aj[i] == sub_aj[i], f"{suma_aj[i]:,} = {sub_aj[i]:,}")
    comprobar(f"{a}: suma de las 5 líneas de circulante (lectura estricta) = «Cash used in operating activities»",
              suma_cc[i] == sub_cc[i], f"{suma_cc[i]:,} = {sub_cc[i]:,}")
    calc = beneficio[i] + sub_aj[i] + sub_cc[i] + ip[i] + ir[i] + tp[i]
    comprobar(f"{a}: beneficio + ajustes + circulante + intereses pagados + intereses cobrados + impuestos pagados = CFO impreso",
              calc == cfo[i], f"{beneficio[i]:,} + {sub_aj[i]:,} + {sub_cc[i]:,} + ({ip[i]:,}) + {ir[i]:,} + ({tp[i]:,}) = {calc:,} · impreso {cfo[i]:,}")
print(f"  avisos de lectura en la versión inglesa: {avisos}")
m = re.search(r"Otros activos y pasivos corrientes y no corrientes \| \(23\.477\) \| \(106\.417\)", ES)
comprobar("versión española (prevalece): «Otros activos y pasivos corrientes y no corrientes» 2024 impreso «(106.417)», negativo", bool(m))
from collections import Counter  # noqa: E402
_n = lambda x: x.replace(",", "").replace(".", "").replace("(", "-").replace(")", "")  # noqa: E731
_en = Counter(map(_n, re.findall(r"\(?\d{1,3}(?:,\d{3})+\)?|\b\d{3}\b", p7)))
_es = Counter(map(_n, re.findall(r"\(?\d{1,3}(?:\.\d{3})+\)?|\b\d{3}\b", ES.split("=== PDF p.58")[0])))
comprobar("estado de flujos EN (PDF p.7) y ES (PDF p.14): mismas cifras salvo el signo de 106.417 en 2024",
          (_en - _es) == Counter({"106417": 1}) and (_es - _en) == Counter({"-106417": 1}),
          f"solo EN {dict(_en - _es)} · solo ES {dict(_es - _en)}")
lectura_sistema = F.numero("106,417)")
comprobar("el lector del sistema (fase1_historia.numero) convierte «106,417)» en +106.417 (signo perdido)", lectura_sistema == 106417.0,
          f"numero('106,417)') = {lectura_sistema:,.0f}")
comp24 = [c for c in AR25["partidas"]["circulante_lineas"]["anterior"] if c["concepto"] == "Other current liabilities"][0]
print(f"  AR_2025.json, circulante_lineas.anterior: impreso «{comp24['impreso']}», signo {comp24.get('signo', '(no declarado → 1)')}")
print(f"  AR_2025.json, nota: «{AR25['partidas']['circulante_lineas']['nota'][:150]}…»")
sis24 = -sum(F.numero(c["impreso"]) * c.get("signo", 1) for c in AR25["partidas"]["circulante_lineas"]["anterior"]) / 1000
print(f"  circulante 2024 que construye el sistema desde AR_2025.json = −(suma) = {sis24:.3f} mm")
v24 = -F.numero(AR24["partidas"]["circulante_lineas"]["actual"][0]["impreso"]) / 1000
print(f"  circulante 2024 desde AR_2024.json (informe 2024, subtotal impreso «{AR24['partidas']['circulante_lineas']['actual'][0]['impreso']}») = {v24:.3f} mm")
comprobar("historia_revision.md registra la diferencia 84,994 frente a −127,84 y aplica el comparativo más reciente",
          "**circulante_lineas 2024**: informe 2024 = 84.994 · comparativo del informe 2025 = -127.84" in REV)
comprobar("no hay decisión registrada para circulante_lineas en fase1_decisiones.json", "circulante_lineas" not in DEC and "circulante" not in DEC)
hist = F63["historia"]["partidas"]
idx = {a: i for i, a in enumerate(F63["historia"]["anios"])}
print(f"  fase1_v63.json: cfo 2024/2025 = {hist['cfo']['valores'][idx[2024]]} / {hist['cfo']['valores'][idx[2025]]} · "
      f"circulante 2024/2025 = {hist['circulante']['valores'][idx[2024]]} / {hist['circulante']['valores'][idx[2025]]}")

# ---------------------------------------------------------------------------------------------------------- 4.2 capex
print("\n4.2 · Capex · PDF p.7 (EN) y PDF p.14 (ES)")
ln_ppe, toks_ppe = fila(p7, "Payments from sale of property, plant and equipment")
ppe = [num(t)[0] for t in toks_ppe]
lns = p7.splitlines()
i_int = next(i for i, ln in enumerate(lns) if ln.strip() == "Payments from sale of other intangible assets")
intg = [num(t)[0] for t in re.findall(TOK, lns[i_int + 1])]
print(f"  EN rótulo 1: «Payments from sale of property, plant and equipment» → {toks_ppe}")
print(f"  EN rótulo 2: «Payments from sale of other intangible assets» (sin cifras en su línea); línea siguiente: «{lns[i_int + 1].strip()}»")
comprobar("ES: «Pagos por la adquisición de inmovilizado material | (178.746) | (160.063)»",
          "Pagos por la adquisición de inmovilizado material | (178.746) | (160.063)" in ES)
comprobar("ES: «Pagos por la adquisición de activos intangibles | (9.757) | (8.737)»",
          "Pagos por la adquisición de activos intangibles | (9.757) | (8.737)" in ES)
comprobar("ES: no hay línea de cobros por venta de inmovilizado en inversión", "venta de inmovilizado" not in ES.lower())
inv_lineas = ["Payments from sale of property, plant and equipment", "Acquisition of companies accounted for using the equity method",
              "Cash flows from loss of control of subsidiaries", "Other effects of disposal"]
inv = [fila(p7, x) for x in inv_lineas]
inv_v = [[num(t)[0] for t in x[1]] for x in inv]
tot_inv, _, _, _ = dos(p7, "Net cash used in investing activities")
for i, a in enumerate(COLS):
    s = sum(v[i] for v in inv_v) + intg[i]
    comprobar(f"{a}: suma de las líneas de inversión = total impreso", s == tot_inv[i], f"{s:,} = {tot_inv[i]:,}")
capex_sis = [hist["capex"]["valores"][idx[a]] for a in (2025, 2024)]
for i, a in enumerate(COLS):
    comprobar(f"{a}: capex del sistema = −(PP&E + intangibles) / 1000", abs(capex_sis[i] - (-(ppe[i] + intg[i]) / 1000)) < 1e-9,
              f"{capex_sis[i]} = −({ppe[i]:,} + {intg[i]:,})/1000")

# ---------------------------------------------------------------------------------------------------------- 4.3 arrendamientos
print("\n4.3 · Arrendamientos · nota 8, PDF p.52 (EN) y PDF p.58 (ES); nota 16, PDF p.66–68; estado de flujos p.7")
p52 = P[52]
mov = {k: dos(p52, k)[0] for k in ("Initial balance", "Additions", "Accrued finance charges", "Payments", "Others",
                                     "Translation differences", "Final balance at 12/31")}
for i, a in enumerate(COLS):
    calc = sum(mov[k][i] for k in ("Initial balance", "Additions", "Accrued finance charges", "Payments", "Others", "Translation differences"))
    comprobar(f"{a}: movimiento del pasivo por arrendamiento cuadra (inicial + altas + gasto devengado + pagos + otros + conversión = final)",
              calc == mov["Final balance at 12/31"][i], f"{calc:,} = {mov['Final balance at 12/31'][i]:,}")
corto, _, _, _ = dos(p52, "leases of low-value items")
comprobar("HALLAZGO EN EL DOCUMENTO (EN): «Expenses related to short-term leases…» repite exactamente los pagos 8,314 / 6,117",
          corto == [-x for x in mov["Payments"]], f"{corto} frente a pagos {mov['Payments']}")
comprobar("HALLAZGO EN EL DOCUMENTO (ES): «Gastos relacionados con arrendamientos corrientes y de poco valor | 8.314 | 6.117»",
          "corrientes y de poco valor | 8.314 | 6.117" in ES)
fin_ini = lns.index(next(ln for ln in lns if ln.strip() == "Cash flows from financing activities"))
fin_fin = lns.index(next(ln for ln in lns if "Net cash from/(used in) financing activities" in ln))
bloque_fin = [ln.strip() for ln in lns[fin_ini + 1:fin_fin] if ln.strip()]
comprobar("el bloque de financiación (p.7) no tiene línea propia de arrendamientos ni de intereses",
          not any(re.search(r"lease|interest", ln, re.I) for ln in bloque_fin), " | ".join(x.split("  ")[0] for x in bloque_fin))
fin_v = [[num(t)[0] for t in re.findall(TOK, ln.split("  ", 1)[1] if "  " in ln else "")[-2:]] for ln in bloque_fin]
deuda_cf = [sum(v[i] for v, ln in zip(fin_v, bloque_fin) if re.search(r"loans and borrowings|other debts", ln)) for i in range(2)]
p66 = P[66]
tot16 = [num(t)[0] for t in re.findall(TOK, next(ln for ln in p66.splitlines() if re.fullmatch(r"\s*196,080\s+66,833\s+300,624\s+92,688\s*", ln)))]
var_saldo = (tot16[0] + tot16[1]) - (tot16[2] + tot16[3])
print(f"  flujos de deuda en financiación 2025 (cobros y pagos de préstamos y otras deudas) = {deuda_cf[0]:,}; "
      f"variación del saldo de la nota 16 (incluye arrendamientos NIIF 16 y «Finance Lease - Others») = {var_saldo:,}")
p67 = P[67]
ias7 = [num(t)[0] for t in re.findall(TOK, next(ln for ln in p67.splitlines() if "Current loans and borrowings" in ln))]
ias7b = [num(t)[0] for t in re.findall(TOK, next(ln for ln in p67.splitlines() if "Non-current loans and borrowings" in ln))]
print(f"  conciliación NIC 7 (p.67), préstamos corrientes: {ias7} · no corrientes: {ias7b} (columna «Other» vacía para préstamos)")
comprobar("NIC 7: flujos + conversión de préstamos = variación total del saldo de la nota 16 (no aparecen altas, devengos ni «Otros» de arrendamientos)",
          ias7[1] + ias7[2] + ias7b[1] + ias7b[2] == var_saldo, f"{ias7[1] + ias7b[1]:,} + ({ias7[2] + ias7b[2]:,}) = {var_saldo:,}")
ar_pri = AR25["partidas"]["arrendamientos_principal"]
print(f"  AR_2025.json arrendamientos_principal: actual «{ar_pri['actual'][0]['impreso']}», anterior «{ar_pri['anterior'][0]['impreso']}» · nota: «{ar_pri['nota']}»")
pagos = {a: hist["arrendamientos_principal"]["valores"][idx[a]] for a in (2023, 2024, 2025)}
print(f"  fase1_v63.json arrendamientos_principal 2023–2025 = {pagos} (pagos totales de la nota 8, no principal)")
dev = {2025: mov["Accrued finance charges"][0] / 1000, 2024: mov["Accrued finance charges"][1] / 1000}
n24 = F63["historia"]["partidas"]["arrendamientos_principal"]["nota"]
m23 = re.search(r"intereses 2,179 / 2,131", n24)
dev[2023] = 2.131 if m23 else None
print(f"  gasto financiero devengado de arrendamientos: 2025 {dev[2025]} · 2024 {dev[2024]} (p.52) · 2023 {dev[2023]} "
      f"(solo consta en la nota del lector 2024 de fase1_v63.json; CF_2024 no está en el paquete)")
med_pagos = round(sum(pagos.values()) / 3, 4)
med_dif = round(sum(pagos[a] - dev[a] for a in pagos) / 3, 4)
print(f"  media 2023–2025 de pagos totales = {med_pagos} · media de (pagos − devengado) = {med_dif}")
an = wv["Análisis"]
comprobar("Análisis C49 = 4,5 coincide con la media de (pagos − gasto devengado), no con la de pagos totales",
          round(med_dif, 1) == an["C49"].value and round(med_pagos, 1) != an["C49"].value, f"C49 = {an['C49'].value}")
comprobar("Análisis C48 (intereses en financiación) = 0", an["C48"].value == 0)
print(f"  Historia L17 (rotulada «Principal de arrendamientos») = {wv['Historia']['L17'].value}")

# ---------------------------------------------------------------------------------------------------------- 4.4 adquisiciones
print("\n4.4 · Adquisiciones y desinversiones · PDF p.7 (EN) y PDF p.14 (ES)")
for x, v in zip(inv_lineas[1:], inv_v[1:]):
    print(f"  EN «{x}»: 2025 {v[0]:,} · 2024 {v[1]:,}")
ln_acq = next(ln.strip() for ln in lns if ln.strip().startswith("Acquisition of a subsidiary"))
comprobar("EN «Acquisition of a subsidiary, net of cash acquired» sin importes en ningún año", re.findall(r"\d", ln_acq) == [], f"«{ln_acq}»")
comprobar("ES «Otros efectos enajenación | - | 11.668» (enajenación = venta)", "Otros efectos enajenación | - | 11.668" in ES)
comprobar("ES «Flujos de efectivo procedentes pérdida de control de dependientes | - | 230.000»",
          "procedentes pérdida de control de dependientes | - | 230.000" in ES)
ital = re.search(r"On 4 July 2024, the effective sale of the Italian subsidiary Vidrala Italia took place", "\n".join(P.values()).replace("\n", " "))
comprobar("la memoria sitúa la venta de Vidrala Italia el 4-jul-2024", bool(ital))
adq_sis = {a: hist["adquisiciones"]["valores"][idx[a]] for a in (2024, 2025)}
comprobar("adquisiciones del sistema = −(suma impresa de negocios dependientes): 2024 = −(230,000 + 11,668)/1000; 2025 = 0",
          abs(adq_sis[2024] - (-(230000 + 11668) / 1000)) < 1e-9 and adq_sis[2025] == 0, f"{adq_sis}")
print("  la compra de participadas por puesta en equivalencia (6,000 en 2024) queda fuera: convención «negocios/dependientes» (prompts/historia_anio.md)")

# ---------------------------------------------------------------------------------------------------------- libro
print("\n5 · DATO EFECTIVO EN EL LIBRO (Vidrala_v63_evaluada.xlsx, valores en caché) Y USO EN EL CÁLCULO")
h, hf = wv["Historia"], wf["Historia"]
for r in (11, 12, 13, 14, 15, 16, 17, 35):
    print(f"  Historia fila {r:>2} «{hf.cell(r, 1).value}»: 2023 {h.cell(r, 10).value} · 2024 {h.cell(r, 11).value} · 2025 {h.cell(r, 12).value}")
for c in ("C46", "C47", "C48", "C49", "C50", "C52"):
    print(f"  Análisis {c} «{wf['Análisis'][c].offset(column=-2).value}»: {an[c].value}")

REF = re.compile(r"(?:(?:'[^']+'|[A-Za-zÁ-ú]+)!)?\$?([A-Z]{1,2})\$?(\d+)(?::\$?([A-Z]{1,2})\$?(\d+))?")


def usos(celdas_hist):
    """Fórmulas del libro que leen alguna de las celdas de Historia dadas ({(col, fila)}); devuelve [(hoja, celda)]."""
    def colnum(c):
        n = 0
        for ch in c:
            n = n * 26 + ord(ch) - 64
        return n
    out = []
    for ws in wf.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value
                if not (isinstance(v, str) and v.startswith("=")):
                    continue
                for m in REF.finditer(v):
                    txt = m.group(0)
                    hoja = txt.split("!")[0].strip("'") if "!" in txt else ws.title
                    if hoja != "Historia":
                        continue
                    c1, r1 = colnum(m.group(1)), int(m.group(2))
                    c2, r2 = (colnum(m.group(3)), int(m.group(4))) if m.group(3) else (c1, r1)
                    if any(c1 <= cc <= c2 and r1 <= rr <= r2 for cc, rr in celdas_hist):
                        out.append((ws.title, c.coordinate))
                        break
    return sorted(set(out))


for etiqueta, filas in (("fila 13 (adquisiciones)", [13]), ("fila 14 (circulante)", [14]), ("fila 17 (arrendamientos)", [17]),
                        ("fila 35 (FCF histórico)", [35]), ("C53 (S2C marginal)", None), ("C58 (f)", None)):
    celdas = {(c, r) for r in filas for c in range(3, 13)} if filas else {(3, int(etiqueta[1:3]))}
    u = usos(celdas)
    print(f"  fórmulas que leen Historia {etiqueta}: {len(u)} → {', '.join(f'{a}!{b}' for a, b in u[:12])}{' …' if len(u) > 12 else ''}")
dg = wv["Diagnóstico V6"]
comprobar("motor activo = A y f del motor (Motor L6) = Historia C58", dg["C5"].value == "A" and abs(wv["Motor"]["L6"].value - h["C58"].value) < 1e-15,
          f"Diagnóstico V6 C5 = {dg['C5'].value} · C58 = {h['C58'].value}")
# réplica de la conciliación de f (Historia C74:C80), ventana C57 = 3 → columnas J, K, L (2023–2025)
win = h["C57"].value
cols = list(range(13 - win, 13))
V = [h.cell(6, c).value for c in cols]
E = [h.cell(7, c).value for c in cols]
DA = [h.cell(8, c).value for c in cols]
T = [h.cell(10, c).value for c in cols]
CX = [h.cell(12, c).value for c in cols]
CI = [h.cell(14, c).value for c in cols]
fcf = h["C70"].value


def f_de(circ, fcf_base):
    c74 = sum(V) / win
    c75 = sum(e * (1 - t) for e, t in zip(E, T)) / win
    c76 = sum(x - d + ci for x, d, ci in zip(CX, DA, circ)) / win
    return c74, c75, c76, c75 - c76, (c75 - c76) - fcf_base, ((c75 - c76) - fcf_base) / c74


c74, c75, c76, c77, c79, f0 = f_de(CI, fcf)
comprobar("la réplica de C74:C80 reproduce la f del libro", abs(f0 - h["C58"].value) < 1e-12,
          f"réplica {f0:.10f} · libro {h['C58'].value:.10f} · C76 {c76:.4f} · C79 {c79:.4f}")
CIc = list(CI)
CIc[cols.index(11)] = v24  # 2024 = columna K
c74b, c75b, c76b, c77b, c79b, f1 = f_de(CIc, fcf)
print(f"  con el circulante 2024 = {v24} (en lugar de {CI[cols.index(11)]}): C76 {c76:.4f} → {c76b:.4f} · C79 {c79:.4f} → {c79b:.4f} · "
      f"f {f0:.6f} → {f1:.6f} (variación {f1 - f0:+.6f})")
for alt in (med_pagos,):
    fcf_alt = an["C46"].value - an["C47"].value - an["C48"].value - round(alt, 1) - an["C50"].value
    _, _, _, _, _, f2 = f_de(CI, fcf_alt)
    print(f"  sensibilidad arrendamientos: con C49 = media de pagos totales ({round(alt, 1)}) el FCF base sería {fcf_alt:.1f} "
          f"(libro {an['C52'].value}) y f {f0:.6f} → {f2:.6f} (variación {f2 - f0:+.6f})")
r31 = [h.cell(31, c).value for c in range(8, 13)]
s2c0 = (h["L6"].value - h["G6"].value) / sum(r31)
s2c1 = (h["L6"].value - h["G6"].value) / (sum(r31) + (v24 - CI[cols.index(11)]))
comprobar("réplica de S2C marginal (Historia C53)", abs(s2c0 - h["C53"].value) < 1e-12, f"{s2c0:.6f}")
print(f"  S2C marginal con el circulante 2024 corregido: {s2c0:.4f} → {s2c1:.4f} (Palancas F16: solo referencia visual; ninguna fórmula del motor la usa)")

print("\n" + "=" * 100)
print(f"RESULTADO: {'todas las comprobaciones esperadas se cumplen' if not fallos else 'NO se cumplen: ' + '; '.join(fallos)}")
sys.exit(1 if fallos else 0)
