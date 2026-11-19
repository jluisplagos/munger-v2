#!/usr/bin/env python3
"""Registro de entradas de zoetis_t1c (examen): parte del registro de Mistral (rama mistral/examen-zoetis-entradas @ 790a8f0) y lo adapta a
los valores y fuentes ACTUALES del expediente: correcciones de fase1_partes (r1: filas 22/23 con solo arrendamientos financieros, L17; r2: signo
de los intereses en el EBIT, adquisiciones de 2017 y 2023, citas de los ceros de las filas 16/17/23), C33/C40/C42 recalculados (entradas_r3.json),
C41 sin redondear (capitalizacion_C41_r3.json), capa F1 e hipótesis con el texto de las fases. Las entradas que cambian llevan como extractor
«Claude orquestación»; las demás conservan a Mistral. Todas las comprobaciones quedan «pendiente», sin revisor ni vínculo. No toca el libro, las
fuentes ni las fases.
Uso: registro_entradas_zoetis_t1c.py CARPETA_EXPEDIENTE REGISTRO_MISTRAL.json SALIDA_CAMBIOS.json"""
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


def referenciados(entradas):
    return {str(o) for e in entradas if e.get("clase") == "derivado" for o in ((e.get("derivacion") or {}).get("origenes") or [])}


REF0 = referenciados(reg["entradas"])


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
for a, d in DOCS.items():
    assert sha(a) == d["sha256"], f"huella distinta: {a}"
K = {y: f"texto/zoetis-10k-fy{y}.txt" for y in range(2016, 2026)}
Q2 = "texto/zoetis-10q-2026-q2.txt"


def fuente(archivo, pag, ubicacion, concepto, columna, periodo, valor_fuente, cita, signo=1, unidad="mm", escala=1,
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


def aux(clave, valor, f, nota, ident="aux", clase="dato_publicado"):
    poner(nueva(clave, ident, clase, valor, fuente=f, comprobacion=comp(f"{f['archivo']} [PDF PAGE {f['pagina']}]", nota)), "auxiliar nuevo (orquestación): " + nota)
    return clave


def vm(k):
    return INST["celdas"][k]


def editar(k, motivo, nota, **campos):
    e = copy.deepcopy(por[k])
    e.update(campos)
    if not k.startswith("aux:"):
        e["valor_modelo"] = vm(k)
    e["comprobacion"] = comp((e.get("comprobacion") or {}).get("fuente_examinada"), nota)
    poner(e, motivo)
    return e


COL = dict(zip(range(2016, 2026), "CDEFGHIJKL"))

# ---------------------------------------------------------------------------------------------- 1. EBIT = BAI + gasto por intereses (r2)
for y, c in COL.items():
    k = f"Historia!{c}7"
    d = por[k]["derivacion"]
    k_int = next(o for o in d["origenes"] if "interest_expense" in o)
    f = dict(por[k_int]["fuente"], signo=1, tratamiento=(
        "«Interest expense, net of capitalized interest» se imprime en positivo, como coste dentro de «Costs and expenses»: EBIT = BAI + gasto por intereses "
        "(signo +1; correccion_fase1_partes_r2.json, REVISION.md punto 1)"))
    editar(k_int, "signo −1 → +1: el gasto por intereses se suma al BAI (correccion_fase1_partes_r2.json)", "Misma cifra y cita; signo corregido (REVISION.md punto 1)",
           valor_modelo=abs(por[k_int]["valor_modelo"]), fuente=f)
    editar(k, f"EBIT {por[k]['valor_modelo']} → {vm(k)} (BAI + intereses; correccion_fase1_partes_r2.json)", "Misma fórmula; el auxiliar de intereses lleva ahora signo +1",
           derivacion=dict(d, conciliacion=f"EBIT {y} = BAI + gasto por intereses neto (impreso en positivo dentro de «Costs and expenses») = {vm(k)}"))

# ---------------------------------------------------------------------------------------------- 2. deuda y arrendamientos financieros (r1)
FIN = {2023: ("aux:zoetis-10k-fy2024_p86_finance_lease_liabilities_current_2023_2023", "aux:zoetis-10k-fy2024_p86_finance_lease_liabilities_noncurrent_2023_2023"),
       2024: ("aux:zoetis-10k-fy2025_p89_finance_lease_liabilities_current_2024", "aux:zoetis-10k-fy2025_p89_finance_lease_liabilities_noncurrent_2024"),
       2025: ("aux:zoetis-10k-fy2025_p89_finance_lease_liabilities_current_2025", "aux:zoetis-10k-fy2025_p89_finance_lease_liabilities_noncurrent_2025")}
for y, (a, b) in FIN.items():
    c = COL[y]
    d = por[f"Historia!{c}22"]["derivacion"]
    ori = [o for o in d["origenes"] if o not in (a, b)]
    editar(f"Historia!{c}22", f"deuda {por['Historia!' + c + '22']['valor_modelo']} → {vm('Historia!' + c + '22')}: sin el pasivo por arrendamientos financieros (correccion_fase1_partes.json)",
           "La fila 22 deja de contar los arrendamientos financieros, que pasan a la fila 23 (F1-US-PUENTE)",
           derivacion=dict(d, origenes=ori, formula=" + ".join(f'o["{o}"]' for o in ori),
                           conciliacion=f"deuda financiera {y} sin arrendamientos financieros (que van a la fila 23) = {vm('Historia!' + c + '22')}"))
    d23 = por[f"Historia!{c}23"].get("derivacion") or {}
    editar(f"Historia!{c}23", f"arrendamientos {por['Historia!' + c + '23']['valor_modelo']} → {vm('Historia!' + c + '23')}: solo el pasivo por arrendamientos financieros (correccion_fase1_partes.json)",
           "US GAAP: la fila 23 lleva solo el pasivo por arrendamientos financieros (el operativo no es deuda del puente; F1-US-PUENTE)",
           clase="derivado", fuente={}, derivacion={"origenes": [a, b], "formula": f'o["{a}"] + o["{b}"]', "unidad": "mm",
                                                      "conciliacion": f"pasivo por arrendamientos financieros {y} = corriente + no corriente = {vm('Historia!' + c + '23')}"})

# ---------------------------------------------------------------------------------------------- 3. ceros de las filas 16, 17 y 23 (r1/r2) y C48
PARTES = {y: json.load(open(os.path.join(C, "fase1_partes", f"AR_{y}.json"), encoding="utf-8"))["partidas"] for y in range(2016, 2026)}
RASTRO = "resultados/correccion_fase1_partes_r2.json (y correccion_fase1_partes.json para la fila 23 de 2019–2021)"


def no_aplicable_por_cero(k, y, partida):
    cero = PARTES[y][partida]["cero"]
    assert vm(k) == 0, k
    f0 = por[k].get("fuente") or {}
    e = copy.deepcopy(por[k])
    e.update(clase="no_aplicable", fuente={}, derivacion=None, valor_modelo=vm(k), justificacion=(
        f"El libro guarda 0 por ausencia de la partida, no por una cifra impresa: {cero['motivo']} (fase1_partes/AR_{y}.json → partidas.{partida}.cero; cita del "
        f"expediente en {K[y]} [PDF PAGE {cero['pagina']}]: «{cero['cita']}»; {RASTRO}). La cita anterior del registro («{str(f0.get('cita'))[:80]}…») no probaba el "
        "cero (REVISION.md punto 5) y la página no imprime un guion ni un 0 de esta partida que pueda contrastarse como cero comprobado: se declara no aplicable "
        "con su justificación. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN."))
    e["comprobacion"] = comp(f"{K[y]} [PDF PAGE {cero['pagina']}]", "Cita y motivo del expediente (cero por ausencia, sin cifra impresa): no_aplicable")
    poner(e, f"{por[k]['clase']} → no_aplicable con el motivo y la cita del expediente (r1/r2)")


for y, c in COL.items():
    no_aplicable_por_cero(f"Historia!{c}16", y, "intereses_financiacion")
for y in range(2016, 2022):
    no_aplicable_por_cero(f"Historia!{COL[y]}17", y, "arrendamientos_principal")
    no_aplicable_por_cero(f"Historia!{COL[y]}23", y, "arrendamientos")
# 2022 (I23): el 10-K 2023 imprime «—» en la columna de 2022 del pasivo por arrendamientos financieros
ant = PARTES[2023]["arrendamientos"]["anterior"][0]
editar("Historia!I23", "229 (operativos) → 0: «—» impreso del pasivo por arrendamientos financieros 2022 (correccion_fase1_partes.json)",
       "Cero comprobado con el «—» de la columna 2022 del 10-K 2023 (fase1_partes/AR_2023.json → arrendamientos.anterior)",
       clase="cero_comprobado", derivacion=None, fuente=fuente(K[2023], ant["pagina"], "nota de arrendamientos (información suplementaria del balance)",
                                                               "Finance lease liabilities - current (pasivo por arrendamientos financieros; impreso «—» en 2022)",
                                                               "2022 (columna comparativa del 10-K 2023)", "a 31-dic-2022", 0, linea(K[2023], ant["pagina"], "Finance lease liabilities - current"),
                                                               reexpresado="columna comparativa del informe siguiente",
                                                               tratamiento="cero impreso como «—»: sin arrendamientos financieros en 2022 (solo operativos: 10-K 2022 PDF p. 70)"))
# C48 = media de la fila 16 (0): no aplicable con US GAAP; se retiran sus tres auxiliares con citas sin relación
c16 = PARTES[2025]["intereses_financiacion"]["cero"]
e = copy.deepcopy(por["Análisis!C48"])
e.update(clase="no_aplicable", derivacion=None, fuente={}, valor_modelo=vm("Análisis!C48"), justificacion=(
    f"C48 = media 2023–2025 de los intereses pagados en financiación = 0 porque con US GAAP (ASC 230) los intereses pagados van en el flujo de explotación (dentro "
    f"del CFO de C46) y la sección de financiación no tiene línea de intereses: {c16['motivo']} ({K[2025]} [PDF PAGE {c16['pagina']}], «{c16['cita']}»). Los tres "
    "auxiliares del registro de Mistral citaban «Principal payments on long-term debt…», que no prueba el cero (REVISION.md, duda C48): se retiran."))
e["comprobacion"] = comp(f"{K[2025]} [PDF PAGE {c16['pagina']}]", "Cero por ausencia de la partida con US GAAP (filas 16 de la Historia, no aplicables)")
poner(e, "derivado de 3 ceros con citas sin relación → no_aplicable (US GAAP)")
# C49: el cero de 2023 con la línea correcta de su misma página
k49 = "aux:zoetis-10k-fy2025_p89_principal_arrendamientos_financieros_2023"
editar(k49, "cita forzada → «Financing cash flows – finance leases 2 1 —» (columna 2023 = «—»)", "La línea correcta está en la misma página (REVISION.md punto 5)",
       fuente=dict(por[k49]["fuente"], cita=linea(K[2025], 89, "Financing cash flows – finance leases"), ubicacion="nota de arrendamientos (información suplementaria de flujos)",
                   tratamiento="cero impreso como «—» en la columna 2023 de «Financing cash flows – finance leases»"))

# ---------------------------------------------------------------------------------------------- 4. adquisiciones (r2) y L17 (r1)
k_np = "aux:zoetis-10k-fy2018_p75_net_proceeds_from_sales_of_assets_2017"
d = por["Historia!D13"]["derivacion"]
k_oa = "aux:zoetis-10k-fy2018_p75_other_acquisitions_2017"
editar("Historia!D13", "119 → 82: «Net proceeds from sales of assets» son ventas de activos, no de negocios (correccion_fase1_partes_r2.json)",
       "Solo «Other acquisitions (82)» (10-K 2018 p. 75)", derivacion=dict(d, origenes=[k_oa], formula=f'-o["{k_oa}"]',
                                                                        conciliacion="adquisiciones netas 2017 = −(Other acquisitions (82)) = 82; los 37 de ventas de activos no se restan ni se suman"))
k_pb = "aux:zoetis-10k-fy2024_p68_proceeds_from_sale_of_businesses_net_of_cash_s_2023"
editar(k_pb, "signo −1 → +1: cobro por venta de negocios impreso en positivo (correccion_fase1_partes_r2.json)", "Misma cifra y cita; signo corregido (REVISION.md punto 2)",
       valor_modelo=96, fuente=dict(por[k_pb]["fuente"], signo=1, tratamiento="cobro impreso en positivo; resta de las adquisiciones (signo +1, como en 2025)"))
editar("Historia!J13", "251 → 59 (155 − 96; correccion_fase1_partes_r2.json)", "Misma fórmula; el cobro por venta de negocios lleva ahora signo +1",
       derivacion=dict(por["Historia!J13"]["derivacion"], conciliacion="adquisiciones netas 2023 = −(Acquisitions (155) + Proceeds from sale of businesses 96) = 59"))
e = copy.deepcopy(por["Historia!K17"])
e["celda"], e["valor_modelo"] = "Historia!L17", vm("Historia!L17")
e["fuente"] = dict(e["fuente"], columna="2025 (columna del ejercicio corriente)", periodo="ejercicio 2025", valor_fuente=2, reexpresado="no aplica (ejercicio corriente del informe)")
e["comprobacion"] = comp(f"{K[2025]} [PDF PAGE 89]", "Principal de arrendamientos financieros 2025 publicado (correccion_fase1_partes.json; REVISION.md punto 4)")
e["incidencia"] = "La ubicación del pago en el estado de flujos no se publica (REVISION_ORQUESTACION.md, L17)."
poner(e, "dato_ausente (vacío) → dato_publicado 2 (correccion_fase1_partes.json)")

# ---------------------------------------------------------------------------------------------- 5. capa F1 (Historia 85–87)
decl = json.load(open(os.path.join(C, "motor_a_f1.json"), encoding="utf-8"))
poner(nueva("Historia!C85", "F1.perimetro_reinversion", "hipotesis", vm("Historia!C85"), ambito="calculo", hipotesis={
    "identificacion": "H-F1.perimetro_reinversion (motor_a_f1.json → perimetro_reinversion)",
    "fundamento": ("Decisión registrada de la persona responsable (motor_a_f1.json → perimetro_reinversion.registro: " + json.dumps(decl["perimetro_reinversion"]["registro"], ensure_ascii=False)
                   + "). Reinversión necesaria = amortización propia sin derechos de uso ni PPA (A2_propio), como hipótesis declarada, no como dato. Zoetis no publica el reparto "
                   "del capex entre mantenimiento y crecimiento. El libro escribe C85 con f1_libro_v631.py aplicar."),
    "alternativas": "A0_total (toda la D&A de la fila 8 como reposición; celda vacía); A1_sin_ROU; A3_estimado.",
    "limites": ("Hipótesis declarada, no dato publicado; una firma no la demuestra y no se adopta para dinero real. La PPA de Zoetis («Purchase accounting adjustments: "
                "Amortization and depreciation») incluye depreciación de activos fijos revalorizados: es una cota superior (REVISION_ORQUESTACION.md). En el paso 12 "
                "del 19-nov-2026 la evaluación F1 bloqueó el motor A (F1-LIBRO, F1-REPLICA: motor_a_f1_resultado.md)."),
    "procedencia": "motor_a_f1.json → Historia!C85 del libro (f1_libro_v631.py aplicar)"},
    comprobacion=comp("motor_a_f1.json → perimetro_reinversion", "Configuración de la capa F1: hipótesis declarada por la persona")), "nueva entrada F1")
for y in range(2021, 2026):
    c = COL[y]
    s = decl["series"]["da_rou"][str(y)]
    k = f"Historia!{c}86"
    if s.get("cero_comprobado"):
        cz = s["cero_comprobado"]
        assert vm(k) == 0
        poner(nueva(k, "F1.da_rou", "no_aplicable", vm(k), ambito="calculo", justificacion=(
            f"Sin arrendamientos financieros en {y}: {cz.get('motivo') or ''} ({s['archivo']} [PDF PAGE {s['pagina']}], «{cz['cita']}»; motor_a_f1.json → series.da_rou.{y}). "
            "No hay amortización de derechos de uso de arrendamientos financieros que contar; la página no imprime un guion ni un 0 de la partida."),
            comprobacion=comp(f"{s['archivo']} [PDF PAGE {s['pagina']}]", "Cero por lectura de la declaración F1, pendiente de revisor")), "nueva entrada F1")
    else:
        cita = linea(s["archivo"], s["pagina"], s["fila"])
        poner(nueva(k, "F1.da_rou", "dato_publicado", vm(k), ambito="calculo", fuente=fuente(
            s["archivo"], s["pagina"], "nota de arrendamientos: «Supplemental Income Statement information for finance leases»",
            f"{s['fila']} (amortización del derecho de uso de los arrendamientos FINANCIEROS)", f"{y} ({s['columna']})", f"ejercicio {y}", s["valor_fuente"], cita,
            reexpresado="no aplica" if y == 2025 else "columna comparativa del 10-K 2025"),
            comprobacion=comp(f"{s['archivo']} [PDF PAGE {s['pagina']}]", f"Serie F1 da_rou {y} de motor_a_f1.json; {s.get('nota', '')[:200]}")), "nueva entrada F1")
    p = decl["series"]["da_ppa"][str(y)]
    k = f"Historia!{c}87"
    poner(nueva(k, "F1.da_ppa", "dato_publicado", vm(k), ambito="calculo", fuente=fuente(
        p["archivo"], p["pagina"], "conciliación del beneficio ajustado (non-GAAP): «Purchase accounting adjustments»", f"{p['fila']} (ajustes de la contabilidad de compras: amortización y depreciación)",
        f"{y} ({p['columna']})", f"ejercicio {y}", p["valor_fuente"], linea(p["archivo"], p["pagina"], p["fila"]),
        reexpresado="no aplica" if (y == 2025 or (y == 2022 and "2022" in p["archivo"])) else "columna comparativa del informe"),
        incidencia="Cota superior de la PPA: incluye depreciación por la revalorización de activos fijos adquiridos y compras de activos netos (REVISION_ORQUESTACION.md, PPA).",
        comprobacion=comp(f"{p['archivo']} [PDF PAGE {p['pagina']}]", f"Serie F1 da_ppa {y} de motor_a_f1.json")), "nueva entrada F1")

# ---------------------------------------------------------------------------------------------- 6. Análisis (entradas_r3.json, capitalizacion_C41_r3.json)
editar("Análisis!C41", "31.053,7 → 31.053,73824 sin redondear (capitalizacion_C41_r3.json)", "C37 × C55 sin redondear",
       derivacion=dict(por["Análisis!C41"]["derivacion"], formula='o["Análisis!C37"] * o["Análisis!C55"]',
                       conciliacion="capitalización = 73,08 × 424,928 (C55 del libro, redondeado a 3 decimales) = 31.053,73824 = libro (capitalizacion_C41_r3.json)"),
       incidencia=("REVISION_ORQUESTACION_R2.md (X, pendiente en el expediente): C55 del libro es 424,928 (redondeo de 424,927535); con la cifra exacta, C41 = "
                   "31.053,704. La corrección corresponde al expediente, no al registro."))


def a(clave, archivo, pag, contiene, valor, columna, periodo, concepto, ubic, signo=1, reex="no aplica (período corriente del informe)", trat=None):
    cita = linea(archivo, pag, contiene)
    vf = valor * signo
    return aux(clave, valor, fuente(archivo, pag, ubic, concepto, columna, periodo, vf, cita, signo=signo, reexpresado=reex,
                                    tratamiento=trat or ("pago publicado entre paréntesis: signo −1 lo transforma en magnitud positiva del modelo" if signo == -1 else
                                                         "cifra tal como se publica; signo 1, sin transformación")),
               f"{concepto} ({os.path.basename(archivo)} PDF p. {pag}, {columna})")


QR = "6M-2025 reexpresado por la «Fiscal Year Alignment» (10-Q T2 2026 p. 10–11)"
BAI25 = a("aux:zoetis-10k-fy2025_p66_bai_2025", K[2025], 66, "Income before provision for taxes on income", 3360, "2025", "ejercicio 2025", "Income before provision for taxes on income", "cuenta de resultados")
INT25 = a("aux:zoetis-10k-fy2025_p66_interest_expense_2025_ttm", K[2025], 66, "Interest expense, net of capitalized interest", 222, "2025", "ejercicio 2025", "Interest expense, net of capitalized interest", "cuenta de resultados")
DA25 = a("aux:zoetis-10k-fy2025_p70_depreciation_and_amortization_2025", K[2025], 70, "Depreciation and amortization expense", 487, "2025", "ejercicio 2025", "Depreciation and amortization expense", "estado de flujos")
BAI_6M26 = a("aux:zoetis-10q-2026-q2_p3_bai_6m2026", Q2, 3, "Income before provision for taxes on income", 1624, "seis meses 2026", "1-ene a 30-jun-2026", "Income before provision for taxes on income", "cuenta de resultados del 10-Q")
INT_6M26 = a("aux:zoetis-10q-2026-q2_p3_interest_expense_6m2026", Q2, 3, "Interest expense, net of capitalized interest", 123, "seis meses 2026", "1-ene a 30-jun-2026", "Interest expense, net of capitalized interest", "cuenta de resultados del 10-Q")
INT_6M25 = a("aux:zoetis-10q-2026-q2_p3_interest_expense_6m2025", Q2, 3, "Interest expense, net of capitalized interest", 107, "seis meses 2025 (reexpresado)", "1-ene a 30-jun-2025", "Interest expense, net of capitalized interest", "cuenta de resultados del 10-Q", reex=QR)
BAI_6M25 = a("aux:zoetis-10q-2026-q2_p10_bai_6m2025_as_previously_reported", Q2, 10, "Income before provision for taxes on income", 1712, "seis meses 2025 «As previously reported»", "1-ene a 30-jun-2025", "Income before provision for taxes on income (as previously reported)", "nota de la «Fiscal Year Alignment» del 10-Q", reex="base antigua («As previously reported»), la del 10-K 2025")
DA_6M26 = a("aux:zoetis-10q-2026-q2_p8_depreciation_and_amortization_6m2026", Q2, 8, "Depreciation and amortization expense", 238, "seis meses 2026", "1-ene a 30-jun-2026", "Depreciation and amortization expense", "estado de flujos del 10-Q")
DA_6M25 = a("aux:zoetis-10q-2026-q2_p8_depreciation_and_amortization_6m2025", Q2, 8, "Depreciation and amortization expense", 243, "seis meses 2025 (reexpresado)", "1-ene a 30-jun-2025", "Depreciation and amortization expense", "estado de flujos del 10-Q", reex=QR)
DEUDA = a("aux:zoetis-10q-2026-q2_p5_long_term_debt_2026-06-30", Q2, 5, "Long-term debt, net of discount and issuance costs", 9048, "30-jun-2026", "a 30-jun-2026", "Long-term debt, net of discount and issuance costs", "balance del 10-Q")
CAJA = a("aux:zoetis-10q-2026-q2_p5_cash_2026-06-30", Q2, 5, "Cash and cash equivalents(b)", 1476, "30-jun-2026", "a 30-jun-2026", "Cash and cash equivalents", "balance del 10-Q")
CFO25 = "aux:zoetis-10k-fy2025_p70_cfo_10k2025_2025"
CFO_6M26 = a("aux:zoetis-10q-2026-q2_p8_cfo_6m2026", Q2, 8, "Net cash provided by operating activities", 1056, "seis meses 2026", "1-ene a 30-jun-2026", "Net cash provided by operating activities", "estado de flujos del 10-Q")
CFO_6M25 = a("aux:zoetis-10q-2026-q2_p11_cfo_6m2025_as_previously_reported", Q2, 11, "Net cash provided by operating activities", 1073, "seis meses 2025 «As previously reported»", "1-ene a 30-jun-2025", "Net cash provided by operating activities (as previously reported)", "nota de la «Fiscal Year Alignment» del 10-Q", reex="base antigua («As previously reported»), la del 10-K 2025")
CAPEX25 = "aux:zoetis-10k-fy2025_p70_capex_10k2025_2025"
CAPEX_6M26 = a("aux:zoetis-10q-2026-q2_p8_capex_6m2026", Q2, 8, "(227)", 227, "seis meses 2026", "1-ene a 30-jun-2026", "Capital expenditures", "estado de flujos del 10-Q", signo=-1)
CAPEX_6M25 = a("aux:zoetis-10q-2026-q2_p8_capex_6m2025", Q2, 8, "(227)", 324, "seis meses 2025 (reexpresado)", "1-ene a 30-jun-2025", "Capital expenditures", "estado de flujos del 10-Q", signo=-1, reex=QR)
FL25 = "aux:zoetis-10k-fy2025_p89_principal_arrendamientos_financieros_2025"
FL_6M25 = a("aux:zoetis-10q-2026-q2_p8_finance_leases_6m2025", Q2, 8, "Financing cash flows - finance leases", 2, "seis meses 2025", "1-ene a 30-jun-2025", "Financing cash flows - finance leases (principal)", "información suplementaria de flujos del 10-Q", reex=QR)
k = "aux:zoetis-10q-2026-q2_p8_finance_leases_6m2026"
aux(k, 0, fuente(Q2, 8, "información suplementaria de flujos del 10-Q", "Financing cash flows - finance leases (principal), impreso «—»", "seis meses 2026", "1-ene a 30-jun-2026",
                 0, linea(Q2, 8, "Financing cash flows - finance leases"), tratamiento="cero impreso como «—»"), "principal de arrendamientos financieros 6M-2026 (10-Q PDF p. 8, «—»)",
    clase="cero_comprobado")
FL_6M26 = k
for x in (CFO25, CAPEX25, FL25):
    assert x in por, x
EBITDA = (f'(o["{BAI25}"] - o["{BAI_6M25}"] + o["{BAI_6M26}"] + o["{INT25}"] - o["{INT_6M25}"] + o["{INT_6M26}"] + o["{DA25}"] - o["{DA_6M25}"] + o["{DA_6M26}"])')
ORI_E = [BAI25, BAI_6M25, BAI_6M26, INT25, INT_6M25, INT_6M26, DA25, DA_6M25, DA_6M26]
APROX = ("APROXIMACIÓN declarada en el expediente (entradas_r3.json): TTM = 2025 (10-K, base antigua) − 6M-2025 + 6M-2026; el 10-Q da el 6M-2025 «as previously reported» "
         "para el BAI y el CFO, que se usan, pero solo reexpresado para intereses, D&A y capex: esos tres mezclan bases.")
e = nueva("Análisis!C33", "juicio_C33", "derivado", vm("Análisis!C33"), ambito="juicio", derivacion={
    "origenes": [DEUDA, CAJA] + ORI_E, "formula": f'(o["{DEUDA}"] - o["{CAJA}"]) / {EBITDA}', "unidad": "x",
    "conciliacion": "deuda neta ÷ EBITDA TTM = (9.048 − 1.476) ÷ (3.360 − 1.712 + 1.624 + 222 − 107 + 123 + 487 − 243 + 238 = 3.992) = 1,896794 (entradas_r3.json)"},
    incidencia=APROX, comprobacion=comp(None, "Recalculado en zoetis_t1c (entradas_r3.json); Mistral lo dejó sin resolver"))
poner(e, "sin resolver en Mistral → derivado (entradas_r3.json)")
e = nueva("Análisis!C42", "juicio_C42", "derivado", vm("Análisis!C42"), ambito="juicio", derivacion={
    "origenes": ["Análisis!C41", DEUDA, CAJA] + ORI_E, "formula": f'(o["Análisis!C41"] + o["{DEUDA}"] - o["{CAJA}"]) / {EBITDA}', "unidad": "x",
    "conciliacion": "EV ÷ EBITDA TTM = (C41 31.053,73824 + 9.048 − 1.476) ÷ 3.992 = 9,675786 (entradas_r3.json)"},
    incidencia=APROX + (" Desalineación de fechas (REVISION_ORQUESTACION_R2.md, D): el balance es del 30-jun-2026 y C41 usa las acciones del 31-dic-2025; con las "
                        "414.154.046 acciones a 30-jun-2026 (10-Q p. 5) saldría ≈ 9,48x. Depende de C41 (C37, fuente de mercado conservada)."),
    comprobacion=comp(None, "Recalculado en zoetis_t1c (entradas_r3.json); Mistral lo dejó sin resolver"))
poner(e, "sin resolver en Mistral → derivado (entradas_r3.json)")
e = nueva("Análisis!C40", "juicio_C40", "derivado", vm("Análisis!C40"), ambito="juicio", derivacion={
    "origenes": [CFO25, CFO_6M25, CFO_6M26, CAPEX25, CAPEX_6M25, CAPEX_6M26, FL25, FL_6M25, FL_6M26],
    "formula": (f'(o["{CFO25}"] - o["{CFO_6M25}"] + o["{CFO_6M26}"]) - (o["{CAPEX25}"] - o["{CAPEX_6M25}"] + o["{CAPEX_6M26}"]) - '
                f'(o["{FL25}"] - o["{FL_6M25}"] + o["{FL_6M26}"])'), "unidad": "mm",
    "conciliacion": "FCF TTM = CFO (2.904 − 1.073 + 1.056 = 2.887) − capex (621 − 324 + 227 = 524) − principal de arrendamientos financieros (2 − 2 + 0 = 0) = 2.363 (entradas_r3.json)"},
    incidencia=APROX, comprobacion=comp(None, "Recalculado en zoetis_t1c (entradas_r3.json); Mistral lo dejó sin resolver"))
poner(e, "sin resolver en Mistral → derivado (entradas_r3.json)")
# C26 = Σ CFO ÷ Σ beneficio neto 2021–2025 (Historia)
fila_cfo = 11
fila_bn = 9
cols = [COL[y] for y in range(2021, 2026)]
s_cfo = sum(vm(f"Historia!{c}{fila_cfo}") for c in cols)
s_bn = sum(vm(f"Historia!{c}{fila_bn}") for c in cols)
assert (s_cfo, s_bn) == (12335, 11654), (s_cfo, s_bn)
ori = [f"Historia!{c}{fila_cfo}" for c in cols] + [f"Historia!{c}{fila_bn}" for c in cols]
e = nueva("Análisis!C26", "juicio_C26", "derivado", vm("Análisis!C26"), ambito="juicio", derivacion={
    "origenes": ori, "formula": "round((" + " + ".join(f'o["{o}"]' for o in ori[:5]) + ") / (" + " + ".join(f'o["{o}"]' for o in ori[5:]) + "), 3)", "unidad": "x",
    "conciliacion": "Σ CFO 2021–2025 12.335 ÷ Σ beneficio neto 2021–2025 11.654 = 1,05843 → 1,058 (Control maestro fila 30; REVISION.md)"},
    comprobacion=comp(None, "Sin resolver en Mistral; derivado de la Historia (REVISION.md: «se puede registrar ya como derivado»)"))
poner(e, "sin resolver en Mistral → derivado de la Historia")


def conv(k, just, alternativas, limites):
    ev = EVID.get(k) or {}
    fund = " · ".join(f"Control maestro!{c}{ev.get('fila')}: {ev[c]}" for c in ("L", "M", "N") if ev.get(c))
    poner(nueva(k, por[k].get("id") or f"juicio_{k.split('!')[1]}", "convencion", vm(k), ambito="juicio", justificacion_clase=just, hipotesis={
        "identificacion": "V-" + k.split("!")[1], "fundamento": "Cálculo de la etapa 1, tal como lo documenta el libro: " + fund, "alternativas": alternativas,
        "limites": limites, "procedencia": f"Control maestro!L–N{ev.get('fila')} del libro (Zoetis_v63_evaluada.xlsx)"},
        comprobacion=comp(f"Control maestro fila {ev.get('fila')} del libro", "Sin resolver en Mistral; dato tratado como convención (se lista aparte)")),
        "sin resolver en Mistral → convencion con justificacion_clase")


conv("Análisis!C24", "ROIC después de impuestos de la etapa 1 (TTM a jun-2026, con EBIT derivado 3.463 y capital medio jun-25/jun-26): su fórmula y el 10-Q del T2 2025 que usa no están en el expediente; con lo conservado sale ≈ 26,2–26,9 % (REVISION.md), no exacto.",
     "Con el EBIT corregido (BAI + intereses) y el capital del expediente: ≈ 26,2–26,9 % según se resten o no las inversiones a corto (REVISION.md).",
     "No reproducible por la máquina con las fuentes del expediente; usa el EBIT con el signo de los intereses anterior a la corrección r2.")
conv("Análisis!C60", "Tasa de crecimiento compuesto de las acciones medias diluidas ((443,835 / 478,569)^(1/5) − 1): exige una raíz, que el contrato de fórmulas no admite; no es una cifra publicada.",
     "FY22→25: −1,92 %/año (Control maestro M28).", "Cálculo a mano (REVISION.md lo reproduce exacto: −1,50 %); el revisor lo recalcula.")
ev88 = EVID.get("Análisis!C88") or {}
editar("Análisis!C88", "incidencia: «Dato no verificable» del expediente (entradas_r3.json)", "Lectura externa de Mistral sin cambios; se añade la marca del expediente",
       incidencia=f"El expediente lo marca «{ev88.get('F')}» (entradas_r3.json): {str(ev88.get('N'))[:600]}")

# ---------------------------------------------------------------------------------------------- 7. hipótesis: el texto de las fases
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
        raise SystemExit(f"{k}: sin texto de fase en Control maestro N: {n[:80]!r}")
    clase_decl, conf = m_cl.group(1), m_cl.group(2)
    clase = "convencion" if clase_decl.startswith("convenci") else "hipotesis"
    ref = re.search(r"(Referencia mecánica:.*?)(?=\s*Apoyo:|\s*Lo sustituiría:|$)", n, re.S)
    sust = re.search(r"(Lo sustituiría:.*)$", n, re.S)
    rango = re.search(r"(Rango[^.]*?\d[^.]*?)\.(?:\s|$)", n)
    fase = FASES.get(k)
    proc = f"Control maestro!N{ev.get('fila')} del libro (Zoetis_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e = copy.deepcopy(e)
    e["clase"], e["valor_modelo"] = clase, vm(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")),
        "fundamento": n + (f" [Evidencia preparada, Control maestro!M{ev['fila']}: {ev['M']}]" if ev.get("M") else ""),
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    e["comprobacion"] = comp(proc, f"Fundamento, alternativas y límites copiados del texto de la fase (Control maestro!N{ev.get('fila')}); clase «{clase}» según la clase "
                                   f"que declara la fase («{clase_decl}»). No se juzga su acierto.")
    poner(e, "hipótesis: texto de la fase" + (f" (valor {antes!r} → {vm(k)!r})" if not VE._igual_exacto(antes, vm(k)) else ""))

# ---------------------------------------------------------------------------------------------- auxiliares que quedan sin uso por estos cambios
ref1 = referenciados(reg["entradas"])
for k in [x for x in list(por) if x.startswith("aux:") and x in REF0 and x not in ref1]:
    reg["entradas"].remove(por.pop(k))
    CAMBIOS.append({"celda": k, "motivo": "retirada: auxiliar que ya no es origen de ninguna entrada tras las correcciones del expediente"})

# ---------------------------------------------------------------------------------------------- cabecera y escritura
for e in reg["entradas"]:
    if not e["celda"].startswith("aux:"):
        assert VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(e["celda"])) or e.get("valor_modelo") == INST["celdas"].get(e["celda"]), e["celda"]
    c_ = e.get("comprobacion") or {}
    assert c_.get("resultado") == "pendiente" and c_.get("revisor") is None and not c_.get("vinculo"), e["celda"]
reg["libro"] = os.path.basename(VE.libro_de(C))
reg["huella_entradas_economicas"] = INST["huella"]
reg["extractor_complementario"] = EXT
reg["fecha_extraccion_complementaria"] = HOY
reg["nota_del_extractor_complementario"] = (
    f"Adaptado el {HOY} por {EXT} al expediente zoetis_t1c: parte del registro de Mistral (mistral/examen-zoetis-entradas @ 790a8f0) y aplica, solo donde el "
    "expediente ya lo recoge, las correcciones de la revisión del registro (coordinacion/cierre_v2/examen/zoetis/revision_registro/) y de la orquestación "
    "(resultados/: correccion_fase1_partes r1/r2, entradas_r3, capitalizacion_C41_r3, declaración F1). Las hipótesis llevan el texto que escribieron las fases "
    "(Control maestro N). Fuentes de mercado de Mistral copiadas en fuentes_mercado/ con sus huellas. Todas las comprobaciones quedan «pendiente», sin revisor "
    "ni vínculo. Lista de cambios: resultados/registro_entradas_zoetis_t1c.json.")
json.dump(reg, open(os.path.join(C, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
vistos = {}
for x in CAMBIOS:
    vistos[x["celda"]] = x["motivo"]
json.dump({"fecha": HOY, "autor": EXT + " (agente de implementación; sin firma humana)", "guion": "resultados/scripts/registro_entradas_zoetis_t1c.py",
           "origen": "munger-v2-evidencias-mistral, mistral/examen-zoetis-entradas @ 790a8f0, resultados_examen/zoetis/verificacion_entradas.json",
           "registro_mistral_sha256": hashlib.sha256(open(ORIGEN, "rb").read()).hexdigest(),
           "registro_sha256": hashlib.sha256(open(os.path.join(C, VE.REGISTRO), "rb").read()).hexdigest(),
           "entradas": len(reg["entradas"]), "universo": INST["n"], "cambiadas": len(vistos),
           "cambiadas_universo": sum(1 for k in vistos if not k.startswith("aux:")), "cambiadas_auxiliares": sum(1 for k in vistos if k.startswith("aux:")),
           "cambios": [{"celda": k, "motivo": v} for k, v in vistos.items()]},
          open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("entradas", len(reg["entradas"]), "cambiadas", len(vistos))
