#!/usr/bin/env python3
"""Registro de entradas de ahold_f3 (examen): parte del registro de Mistral completado por el extractor complementario
(munger-v2-evidencias-mistral, coordinacion/cierre-v2 @ 33d5f2d, coordinacion/cierre_v2/examen/ahold/registro/verificacion_entradas.json) y lo
adapta a los valores y fuentes ACTUALES del expediente: P-O2 (a) en C55/C41 y P-O1 (c) en C46/C48/C49 (heredados de ahold_f2), C40/C42/C88/C96
recalculados en ahold_f3 (resultados/recalculo_C40_C42_C88.json, entradas_r3.json) e hipótesis con el texto vigente de las fases. Las entradas
que cambian llevan como extractor «Claude orquestación»; las demás conservan su extractor. Todas las comprobaciones quedan «pendiente», sin
revisor ni vínculo. No toca el libro, las fuentes ni las fases.
Uso: registro_entradas_ahold_f3.py CARPETA_EXPEDIENTE REGISTRO_ORIGEN.json SALIDA_CAMBIOS.json"""
import copy
import hashlib
import json
import os
import re
import sys

C, ORIGEN, SALIDA = sys.argv[1], sys.argv[2], sys.argv[3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402

EXT = "Claude orquestación"
HOY = "2026-11-19"
reg = json.load(open(ORIGEN, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
INST = VE.universo(C)
EVID = VE.evidencia_libro(C)
CAMBIOS = []


def sha(p):
    return hashlib.sha256(open(os.path.join(C, p), "rb").read()).hexdigest()


def pagina(archivo, n):
    t = open(os.path.join(C, archivo), encoding="utf-8").read()
    m = re.search(r"\[PDF PAGE %d\]" % n, t)
    fin = re.search(r"\[PDF PAGE \d+\]", t[m.end():])
    return t[m.end(): m.end() + fin.start()] if fin else t[m.end():]


def linea(archivo, n, contiene):
    ls = [l for l in pagina(archivo, n).split("\n") if contiene in l]
    if len(ls) != 1:
        raise SystemExit(f"{archivo} p.{n}: {len(ls)} líneas con {contiene!r}")
    return ls[0].strip()


def comp(fuente_examinada, nota):
    return {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada, "nota": nota, "vinculo": None}


DOCS = {}
for e in reg["entradas"]:
    f = e.get("fuente") or {}
    if str(f.get("archivo") or "").startswith("texto/") and f["archivo"] not in DOCS:
        DOCS[f["archivo"]] = {"documento": f["documento"], "version": f["version"], "sha256": f["sha256"]}
Q3 = "texto/AD_q3-2026-interim-report.txt"
DOCS[Q3] = {"documento": "Interim report Q3 2026 de Koninklijke Ahold Delhaize N.V. (informe interino oficial, 4-nov-2026)",
            "version": (f"PDF oficial «pdf/AD_q3-2026-interim-report.pdf», sha256 {sha('pdf/AD_q3-2026-interim-report.pdf')} (pdf_DESCARGAS_2026.tsv: "
                        "https://media.aholddelhaize.com/media/voehurnq/ahold-delhaize-q3-2026-interim-report.pdf, 2026-11-17); texto con marcas [PDF PAGE n]: "
                        f"«{Q3}», sha256 {sha(Q3)}"), "sha256": sha(Q3)}
for a, d in DOCS.items():
    assert sha(a) == d["sha256"], f"huella distinta: {a}"
AR = {y: f"texto/AD_annual-report-{y}.txt" for y in range(2016, 2026)}
Q2 = "texto/AD_q2-2026-interim-report.txt"


def fuente(archivo, pag, ubicacion, concepto, columna, periodo, valor_fuente, cita, signo=1, unidad="millones de euros", escala=1,
           tratamiento="cifra tal como se publica; signo 1, sin transformación", reexpresado="no aplica (ejercicio corriente del informe)"):
    d = DOCS[archivo]
    return {"documento": d["documento"], "version": d["version"], "archivo": archivo, "sha256": d["sha256"], "pagina": pag, "folio": None,
            "ubicacion": ubicacion, "concepto": concepto, "columna": columna, "periodo": periodo, "unidad": unidad, "escala": escala, "signo": signo,
            "tratamiento": tratamiento, "perimetro": "consolidado", "reexpresado": reexpresado, "valor_fuente": valor_fuente, "cita": cita}


def nueva(celda, ident, clase, valor, ambito=None, **kw):
    e = {"celda": celda, "id": ident, "ambito": ambito, "uso": None, "material": True, "clase": clase, "valor_modelo": valor, "fuente": {},
         "derivacion": None, "hipotesis": None, "justificacion": None, "comprobacion": None, "incidencia": None}
    e.update(kw)
    return e


def poner(e, motivo):
    k = e["celda"]
    if k in por:
        reg["entradas"][reg["entradas"].index(por[k])] = e
    else:
        reg["entradas"].append(e)
    por[k] = e
    CAMBIOS.append({"celda": k, "motivo": motivo})


def quitar(k, motivo):
    reg["entradas"].remove(por.pop(k))
    CAMBIOS.append({"celda": k, "motivo": "retirada: " + motivo})


def aux(clave, valor, f, nota, ident="aux"):
    poner(nueva(clave, ident, "dato_publicado", valor, fuente=f, comprobacion=comp(f"{f['archivo']} [PDF PAGE {f['pagina']}]", nota)), "auxiliar nuevo (orquestación): " + nota)
    return clave


def vm(k):
    return INST["celdas"][k]


def derivado(k, origenes, formula, conciliacion, unidad, nota, motivo, **kw):
    e = copy.deepcopy(por[k]) if k in por else nueva(k, INST["ids"].get(k), "derivado", None, ambito=INST["ambito"].get(k))
    e.update(clase="derivado", valor_modelo=vm(k), fuente={}, hipotesis=None, justificacion=None,
             derivacion={"origenes": origenes, "formula": formula, "conciliacion": conciliacion, "unidad": unidad}, comprobacion=comp(None, nota))
    e.pop("justificacion_clase", None)
    e.update(kw)
    poner(e, motivo)


# ---------------------------------------------------------------------------------------------- 1. P-O2 (a): C55 y C41 (REVISION punto 1)
cita55 = "The number of outstanding common shares as of September 27, 2026, was 865,173,863 (December 28, 2025: 886,877,259)."
assert VE._norm_txt(cita55) in VE._norm_txt(pagina(Q3, 21))  # la frase ocupa dos líneas de la página: el paréntesis que abre está en la primera
e = copy.deepcopy(por["Análisis!C55"])
e["valor_modelo"] = vm("Análisis!C55")
e["fuente"] = fuente(Q3, 21, "nota de acciones en circulación del informe interino Q3 2026", "acciones ordinarias EN CIRCULACIÓN a 28-dic-2025 (cierre del ejercicio base)",
                     "December 28, 2025 (cifra comparativa del texto)", "a 28-dic-2025", 886877259, cita55, unidad="acciones", escala=1e-06,
                     tratamiento=("acciones en circulación al cierre del ejercicio base (decisión P-O2 (a)); unidades → millones de acciones (escala 1e-6). La frase completa: "
                                  "«The number of outstanding common shares as of September 27, 2026, was 865,173,863 (December 28, 2025: 886,877,259)»; AR2025 PDF p. 244 "
                                  "da 886,877 en miles (891,188 emitidas − 4,311 en autocartera)"))
e["comprobacion"] = comp(f"{Q3} [PDF PAGE 21]", "P-O2 (a): acciones en circulación a 28-dic-2025 (fase1_v63.json → acciones_diluidas), no la media diluida de 2025 (905)")
poner(e, "905 (media diluida) → 886,877259 (P-O2 a; REVISION.md punto 1)")
e = copy.deepcopy(por["Análisis!C41"])
e["valor_modelo"] = vm("Análisis!C41")
e["derivacion"] = dict(e["derivacion"], conciliacion="capitalización = precio C37 36,05 € (13-nov-2026) × acciones en circulación C55 886,877259 M (28-dic-2025, P-O2 a) = 31.971,92518695 = libro")
e["comprobacion"] = comp(None, "Misma fórmula; arrastre de C55 (P-O2 a)")
poner(e, "32.625,25 → 31.971,925 (arrastre de C55; REVISION.md punto 1)")

# ---------------------------------------------------------------------------------------------- 2. P-O1 (c): cobros (regla espejo)
COBROS = {"dividendos": ("Dividends received from joint ventures", "dividends_received_from_joint_ventures", "dividendos cobrados de negocios conjuntos"),
          "intereses": ("Interest received", "interest_received", "intereses cobrados"),
          "subarriendos": ("Lease payments received on lease receivables", "lease_payments_received_on_lease_receivables", "cobros de subarriendos (arrendamientos por cobrar)")}
FUENTE_ANIO = {2019: (AR[2020], 149), 2020: (AR[2021], 184), 2021: (AR[2022], 194), 2022: (AR[2023], 204), 2023: (AR[2024], 263), 2024: (AR[2025], 216), 2025: (AR[2025], 216)}
VALORES = {2019: (36, 56, 94), 2020: (16, 24, 99), 2021: (28, 16, 103), 2022: (38, 56, 115), 2023: (22, 160, 117), 2024: (22, 196, 125), 2025: (28, 130, 138)}
AUXC = {}
for y, (arch, pag) in FUENTE_ANIO.items():
    for i, (n, (literal, slug, desc)) in enumerate(COBROS.items()):
        v = VALORES[y][i]
        corriente = (y == 2025) or arch == AR.get(y)
        k = f"aux:{os.path.basename(arch)[:-4]}_p{pag}_{slug}_{y}"
        cita = linea(arch, pag, literal)
        AUXC[(y, n)] = aux(k, v, fuente(arch, pag, "estado de flujos de efectivo consolidado (actividades de inversión)", f"{literal} ({desc})",
                                        f"{y} (" + ("columna del ejercicio corriente" if corriente else "columna comparativa del informe siguiente") + ")",
                                        f"ejercicio {y}", v, cita, reexpresado="no aplica (ejercicio corriente del informe)" if corriente else
                                        "columna comparativa del informe siguiente (la misma fuente que la Historia)"),
                           f"{desc} {y} (P-O1 c, regla espejo; {os.path.basename(arch)} PDF p. {pag})")
CFO = {2023: "aux:AD_annual-report-2024_p263_net_cash_from_operating_activities_2023", 2024: "aux:AD_annual-report-2025_p216_net_cash_from_operating_activities_2024",
       2025: "aux:AD_annual-report-2025_p216_net_cash_from_operating_activities_2025"}
IP = {2023: "aux:AD_annual-report-2024_p263_interest_paid_2023", 2024: "aux:AD_annual-report-2025_p216_interest_paid_2024", 2025: "aux:AD_annual-report-2025_p216_interest_paid_2025"}
RL = {2023: "aux:AD_annual-report-2024_p263_repayment_of_lease_liabilities_2023", 2024: "aux:AD_annual-report-2025_p216_repayment_of_lease_liabilities_2024",
      2025: "aux:AD_annual-report-2025_p216_repayment_of_lease_liabilities_2025"}
for x in list(CFO.values()) + list(IP.values()) + list(RL.values()):
    assert x in por, x
P_O1 = "Decisión P-O1 (c) «regla espejo» (18-nov-2026): si se resta lo que se paga, se suma lo que se cobra por lo mismo; fase1_v63.json → analisis.{c}.calculo"
for c, base, comp_, signo, txt in (("C46", CFO, "dividendos", "+", "CFO + dividendos de negocios conjuntos"), ("C48", IP, "intereses", "-", "intereses pagados − intereses cobrados"),
                                   ("C49", RL, "subarriendos", "-", "pagos de arrendamientos − cobros de subarriendos")):
    ori = [o for y in (2023, 2024, 2025) for o in (base[y], AUXC[(y, comp_)])]
    formula = "(" + " + ".join(f'(o["{base[y]}"] {signo} o["{AUXC[(y, comp_)]}"])' for y in (2023, 2024, 2025)) + ") / 3"
    vals = " + ".join(f"({por[base[y]]['valor_modelo']} {signo} {VALORES[y][['dividendos', 'intereses', 'subarriendos'].index(comp_)]})" for y in (2023, 2024, 2025))
    derivado(f"Análisis!{c}", ori, formula, f"media 2023–2025 de {txt} = [{vals}] / 3 → libro {vm('Análisis!' + c)} ({P_O1.format(c=c)})", "millones de euros",
             "P-O1 (c) heredado de ahold_f2 (cambio_ahold_po1_po2.json): se añaden los cobros de cada año (AR2024 p. 263, AR2025 p. 216)",
             f"{por['Análisis!' + c]['valor_modelo']} → {vm('Análisis!' + c)} (P-O1 c; REVISION.md punto 2)")

# ---------------------------------------------------------------------------------------------- 3. C40, C42, C88 y C96 (recalculo_C40_C42_C88.json, entradas_r3.json)
Q2C = {}
for n, (literal, slug, desc) in COBROS.items():
    cita = linea(Q2, 15, literal)
    nums = [int(x) for x in re.findall(r"\b\d+\b", cita)]
    hy26, hy25 = nums[-2], nums[-1]
    Q2C[(n, 2026)] = aux(f"aux:Q2-2026_p15_{slug}_hy2026", hy26, fuente(Q2, 15, "estado de flujos consolidado del informe interino (actividades de inversión)",
                         f"{literal} ({desc}), primer semestre 2026", "HY 2026 (semestre cerrado el 28-jun-2026; tercera columna)", "semestre cerrado el 28-jun-2026", hy26, cita),
                         f"{desc} 1S-2026 (Q2-26 PDF p. 15)")
    Q2C[(n, 2025)] = aux(f"aux:Q2-2026_p15_{slug}_hy2025", hy25, fuente(Q2, 15, "estado de flujos consolidado del informe interino (actividades de inversión)",
                         f"{literal} ({desc}), primer semestre 2025", "HY 2025 (semestre comparativo; cuarta columna)", "semestre cerrado el 29-jun-2025", hy25, cita,
                         reexpresado="columna comparativa del informe interino"), f"{desc} 1S-2025 (Q2-26 PDF p. 15)")
e40 = por["Análisis!C40"]
ori = list(e40["derivacion"]["origenes"])
form = e40["derivacion"]["formula"]
for n in COBROS:
    ori += [Q2C[(n, 2026)], AUXC[(2025, n)], Q2C[(n, 2025)]]
    form += f' + o["{Q2C[(n, 2026)]}"] + o["{AUXC[(2025, n)]}"] - o["{Q2C[(n, 2025)]}"]'
derivado("Análisis!C40", ori, form,
         ("FCF LTM a 28-jun-2026 con la regla espejo (P-O1 c): 1S-2026 + 2025 − 1S-2025 de cada partida: CFO 6.598 − capex 2.566 − intereses pagados 271 − pagos de "
          "arrendamientos 1.940 (= 1.821 de la etapa 1) + dividendos de negocios conjuntos 27 + intereses cobrados 104 + cobros de subarriendos 144 = 2.096 = libro "
          "(recalculo_C40_C42_C88.json). Los gastos van con su signo publicado (negativos), los cobros en positivo."), "millones de euros",
         "Recalculado en ahold_f3 (recalculo_C40_C42_C88.json; REVISION_ORQUESTACION_R2.md, C)", "1.821 → 2.096 (P-O1 c; recalculo_C40_C42_C88.json)")
LTM = ('(o["Historia!L7"] + o["aux:Q2-2026_p11_operating_income_hy2026"] - o["aux:Q2-2026_p11_operating_income_hy2025"] + o["Historia!L8"] + '
       'o["aux:Q2-2026_p15_da_impairments_hy2026"] - o["aux:Q2-2026_p15_da_impairments_hy2025"])')
derivado("Análisis!C42", ["Análisis!C41", "Análisis!C54", "Análisis!C53", "aux:Q2-2026_p13_investments_jv_hy2026", "Historia!L7", "aux:Q2-2026_p11_operating_income_hy2026",
                          "aux:Q2-2026_p11_operating_income_hy2025", "Historia!L8", "aux:Q2-2026_p15_da_impairments_hy2026", "aux:Q2-2026_p15_da_impairments_hy2025"],
         f'(o["Análisis!C41"] + o["Análisis!C54"] - o["Análisis!C53"] - o["aux:Q2-2026_p13_investments_jv_hy2026"]) / {LTM}',
         ("EV ÷ EBITDA LTM = (C41 31.971,925 + deuda bruta C54 19.261 − caja C53 3.196 − negocios conjuntos 244) ÷ (3.542 + 1.760 − 1.741 + 3.733 + 1.828 − 1.870 = 7.252) "
          "= 47.792,925 ÷ 7.252 = 6,590310 (recalculo_C40_C42_C88.json; misma definición que C33)"), "x",
         "Recalculado en ahold_f3 con C41 vigente (la capitalización de la etapa 1, 28.626, sin fuente, se retira)",
         "6,129 → 6,590310 (recalculo_C40_C42_C88.json; REVISION.md punto 3)",
         incidencia=("Vigencia (REVISION_ORQUESTACION_R2.md, duda D): el informe Q3 2026 (4-nov-2026) está en texto/ y es anterior al precio (13-nov-2026); con el Q3 "
                     "sale ≈ 6,53x (≈ 6,43x con las acciones a 27-sep-2026). La deuda bruta de 19.261 (C54) está en Q2-26 PDF p. 23. El expediente no lo ha decidido; "
                     "depende de C41 (precio C37, fuente de mercado conservada)."))
quitar("aux:etapa1_capitalizacion_oct2026", "C42 ya no usa la capitalización de la etapa 1 sin fuente (recalculo_C40_C42_C88.json → no_tocado)")
CAP = {y: f"aux:AD_annual-report-2025_p65_market_capitalization_{y}" for y in range(2019, 2026)}
COL = dict(zip(range(2016, 2026), "CDEFGHIJKL"))
for y in range(2019, 2026):
    k = f"aux:pfcf_{y}"
    c = COL[y]
    ori = [CAP[y], f"Historia!{c}11", f"Historia!{c}12", f"Historia!{c}16", f"Historia!{c}17"] + [AUXC[(y, n)] for n in COBROS]
    den = (f'o["Historia!{c}11"] - o["Historia!{c}12"] - o["Historia!{c}16"] - o["Historia!{c}17"] + '
           + " + ".join(f'o["{AUXC[(y, n)]}"]' for n in COBROS))
    vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else vm(o)) for o in ori}
    fcf = vals[f"Historia!{c}11"] - vals[f"Historia!{c}12"] - vals[f"Historia!{c}16"] - vals[f"Historia!{c}17"] + sum(vals[AUXC[(y, n)]] for n in COBROS)
    e = copy.deepcopy(por[k])
    e.update(valor_modelo=vals[CAP[y]] / fcf, derivacion={"origenes": ori, "formula": f'o["{CAP[y]}"] / ({den})', "unidad": "x",
             "conciliacion": f"P/FCF {y} con la regla espejo (P-O1 c): capitalización de cierre {vals[CAP[y]]} ÷ FCF {fcf} (CFO − capex − intereses − arrendamientos + dividendos de "
                             f"negocios conjuntos + intereses cobrados + cobros de subarriendos) = {vals[CAP[y]] / fcf:.6f} (recalculo_C40_C42_C88.json → p_fcf_por_anio)"},
             comprobacion=comp(None, "Recalculado con la regla espejo (recalculo_C40_C42_C88.json); antes, definición de la fila 52 de la etapa 1"))
    poner(e, f"P/FCF {y} con la regla espejo (recalculo_C40_C42_C88.json)")
e = copy.deepcopy(por["Análisis!C88"])
e["valor_modelo"] = vm("Análisis!C88")
f88 = e["derivacion"]["formula"]
assert f88.startswith("round(") and f88.endswith(", 1)")
e["derivacion"] = dict(e["derivacion"], formula=f88[len("round("):-len(", 1)")], unidad="x",
                       conciliacion=("Mediana de los 7 P/FCF de cierre 2019–2025 con la regla espejo (red de ordenación min/max: el contrato no tiene mediana) = "
                                     "12,491503 (2024: 28.668 ÷ 2.295) = libro, sin redondear (recalculo_C40_C42_C88.json)"))
e["comprobacion"] = comp(None, "Recalculado en ahold_f3 (recalculo_C40_C42_C88.json): 14,7 → 12,4915; misma red de ordenación que el registro de origen, sin el redondeo a 1 decimal")
poner(e, "14,7 → 12,491503 (recalculo_C40_C42_C88.json)")
A25 = AR[2025]
k_mb = aux("aux:AD_annual-report-2025_p199_acciones_management_board_2025", 0.556165, fuente(
    A25, 199, "informe de remuneración: acciones del Management Board", "acciones de los miembros del Management Board (total)", "a 28-dic-2025", "a 28-dic-2025",
    556165, linea(A25, 199, "556,165"), unidad="acciones", escala=1e-06), "acciones del Management Board (AR2025 PDF p. 199)")
k_adr = aux("aux:AD_annual-report-2025_p199_adr_muller_2025", 0.009579, fuente(
    A25, 199, "informe de remuneración: nota 2 de la tabla de acciones del Management Board", "acciones de F. Muller en ADR (además del total)", "a 28-dic-2025", "a 28-dic-2025",
    9579, linea(A25, 199, "9,579"), unidad="acciones", escala=1e-06), "ADR de F. Muller (AR2025 PDF p. 199, nota 2)")
k_weir = aux("aux:AD_annual-report-2025_p209_acciones_weir_2025", 0.001, fuente(
    A25, 209, "informe de remuneración del Supervisory Board, nota 3", "acciones de H. Weir (único miembro del Supervisory Board con acciones)", "a 28-dic-2025", "a 28-dic-2025",
    1000, linea(A25, 209, "Helen Weir held 1,000"), unidad="acciones", escala=1e-06), "acciones del Supervisory Board (AR2025 PDF p. 209)")
derivado("Análisis!C96", [k_mb, k_adr, k_weir, "Análisis!C55"], f'(o["{k_mb}"] + o["{k_adr}"] + o["{k_weir}"]) / o["Análisis!C55"]',
         "% de insiders a 28-dic-2025 = (556.165 + 9.579 + 1.000) ÷ 886.877.259 = 0,000639 (entradas_r3.json)", "proporción",
         "Recalculado en ahold_f3 (entradas_r3.json): la etapa 1 (0,0007) usaba notificaciones AFM sin fuente en el expediente",
         "convención 0,0007 (etapa 1) → derivado 0,000639 (entradas_r3.json)",
         incidencia="No incluye al Comité Ejecutivo fuera del Management Board (entradas_r3.json).")

# ---------------------------------------------------------------------------------------------- 4. hipótesis: el texto VIGENTE de las fases
FASES = {}
for f_ in ("A", "B", "C"):
    p_ = os.path.join(C, f"celdas_{f_}.json")
    if os.path.exists(p_):
        for kk in json.load(open(p_, encoding="utf-8")):
            if "!" in kk:
                FASES[kk.replace("'", "")] = f_
for k in list(por):
    e = por[k]
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
    if h0.get("fundamento") == fund and e.get("clase") == clase and VE._igual_exacto(e.get("valor_modelo"), vm(k)):
        continue  # sin cambios en la fase: se conserva la entrada del extractor complementario
    ref = re.search(r"(Referencia mecánica:.*?)(?=\s*Apoyo:|\s*Lo sustituiría:|$)", n, re.S)
    sust = re.search(r"(Lo sustituiría:.*)$", n, re.S)
    rango = re.search(r"(Rango[^.]*?\d[^.]*?)\.(?:\s|$)", n)
    fase = FASES.get(k)
    proc = f"Control maestro!N{ev.get('fila')} del libro (Ahold_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e = copy.deepcopy(e)
    e["clase"], e["valor_modelo"] = clase, vm(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")), "fundamento": fund,
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    e["comprobacion"] = comp(proc, f"Fundamento, alternativas y límites copiados del texto vigente de la fase (Control maestro!N{ev.get('fila')}, ahold_f3); clase «{clase}» "
                                   f"según la clase que declara la fase («{clase_decl}»). No se juzga su acierto.")
    poner(e, "hipótesis: texto vigente de la fase en ahold_f3" + (f" (valor {antes!r} → {vm(k)!r})" if not VE._igual_exacto(antes, vm(k)) else ""))

# ---------------------------------------------------------------------------------------------- cabecera y escritura
for e in reg["entradas"]:
    if not e["celda"].startswith("aux:"):
        assert VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(e["celda"])) or e.get("valor_modelo") == INST["celdas"].get(e["celda"]), e["celda"]
    c_ = e.get("comprobacion") or {}
    assert c_.get("resultado") == "pendiente" and c_.get("revisor") is None and not c_.get("vinculo"), e["celda"]
reg["libro"] = os.path.basename(VE.libro_de(C))
reg["huella_entradas_economicas"] = INST["huella"]
reg["extractor_orquestacion"] = EXT
reg["fecha_orquestacion"] = HOY
reg["nota_de_la_orquestacion"] = (
    f"Adaptado el {HOY} por {EXT} al expediente ahold_f3: parte del registro de Mistral completado por el extractor complementario (coordinacion/cierre-v2 @ 33d5f2d) "
    "y aplica, solo donde el expediente ya lo recoge, las correcciones de la revisión del registro (coordinacion/cierre_v2/examen/ahold/revision_registro/): P-O2 (a) en "
    "C55/C41, P-O1 (c) en C46/C48/C49 y los recálculos de C40/C42/C88/C96 (resultados/recalculo_C40_C42_C88.json, entradas_r3.json); retira el auxiliar de la "
    "capitalización de la etapa 1 y actualiza las hipótesis al texto vigente de las fases. Fuentes de mercado de Mistral (mistral/examen-ahold-entradas @ 9a06d4a) "
    "copiadas en fuentes_mercado/ con sus huellas. Todas las comprobaciones quedan «pendiente», sin revisor ni vínculo. Lista de cambios: resultados/registro_entradas_ahold_f3.json.")
json.dump(reg, open(os.path.join(C, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
vistos = {}
for x in CAMBIOS:
    vistos[x["celda"]] = x["motivo"]
json.dump({"fecha": HOY, "autor": EXT + " (agente de implementación; sin firma humana)", "guion": "resultados/scripts/registro_entradas_ahold_f3.py",
           "origen": "munger-v2-evidencias-mistral, coordinacion/cierre-v2 @ 33d5f2d, coordinacion/cierre_v2/examen/ahold/registro/verificacion_entradas.json",
           "registro_origen_sha256": hashlib.sha256(open(ORIGEN, "rb").read()).hexdigest(),
           "registro_sha256": hashlib.sha256(open(os.path.join(C, VE.REGISTRO), "rb").read()).hexdigest(),
           "entradas": len(reg["entradas"]), "universo": INST["n"], "cambiadas": len(vistos),
           "cambiadas_universo": sum(1 for k in vistos if not k.startswith("aux:")), "cambiadas_auxiliares": sum(1 for k in vistos if k.startswith("aux:")),
           "cambios": [{"celda": k, "motivo": v} for k, v in vistos.items()]},
          open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("entradas", len(reg["entradas"]), "cambiadas", len(vistos))
