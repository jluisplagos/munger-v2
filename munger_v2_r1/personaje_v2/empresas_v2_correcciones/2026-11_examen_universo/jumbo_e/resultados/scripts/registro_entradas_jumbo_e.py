#!/usr/bin/env python3
"""Registro de entradas de jumbo_e (examen): parte del registro de Mistral (rama mistral/examen-jumbo-entradas @ fced486) y lo adapta a
los valores y fuentes ACTUALES del expediente (correcciones r2/r3 de fase1_partes, recálculos de C40/C42/C96, declaración F1, textos de
las fases). Las entradas que cambian llevan como extractor «Claude orquestación»; las demás conservan a Mistral. Todas las comprobaciones
quedan «pendiente», sin revisor ni vínculo: el sellado es de un revisor independiente. No toca el libro, las fuentes ni las fases.
Uso: registro_entradas_jumbo_e.py CARPETA_EXPEDIENTE REGISTRO_MISTRAL.json SALIDA_CAMBIOS.json"""
import copy
import hashlib
import json
import os
import re
import sys

C, MISTRAL, SALIDA = sys.argv[1], sys.argv[2], sys.argv[3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402

EXT = "Claude orquestación"
HOY = "2026-11-19"
reg = json.load(open(MISTRAL, encoding="utf-8"))
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


def cambia(k, motivo):
    CAMBIOS.append({"celda": k, "motivo": motivo})


DOCS = {}
for e in reg["entradas"]:
    f = e.get("fuente") or {}
    if str(f.get("archivo") or "").startswith("texto/") and f["archivo"] not in DOCS:
        DOCS[f["archivo"]] = {"documento": f["documento"], "version": f["version"], "sha256": f["sha256"]}
for a, d in DOCS.items():
    assert sha(a) == d["sha256"], f"huella distinta: {a}"
AR25, H1 = "texto/jumbo-annual-report-fy2025.txt", "texto/jumbo-h1-2026-financial-results.txt"


def fuente(archivo, pag, ubicacion, concepto, columna, periodo, valor_fuente, cita, signo=1, unidad="euros", escala=1e-06,
           tratamiento="cifra tal como se publica", reexpresado="no aplica (ejercicio corriente del informe)"):
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
    cambia(k, motivo)


def aux(clave, valor, f, nota, ident="aux"):
    e = nueva(clave, ident, "dato_publicado", valor, fuente=f, comprobacion=comp(f"{f['archivo']} [PDF PAGE {f['pagina']}]", nota))
    poner(e, "auxiliar nuevo (orquestación): " + nota)
    return clave


def vm(k):
    return INST["celdas"][k]


# ---------------------------------------------------------------------------------------------- 1. J3 en 2019 (r2; REVISION punto 1)
A20 = "texto/jumbo-annual-report-fy2020.txt"
J3 = ("Cifra registrada tal como está impresa en la columna 01/01–31/12/2019 de AR2020 PDF p. 59. El emisor cruzó las etiquetas «Lease repayments» "
      "(es el INTERÉS) e «Interest paid for leases» (es el PRINCIPAL) también en esta columna (J3 extendido a 2019, correccion_fase1_partes_r2.json): "
      "prueba, nota de costes financieros AR2020 PDF p. 86, «Interest expense on lease liabilities … 1.488.678» (2019), igual al euro a la línea "
      "«Lease repayments»; el informe de transición (PDF p. 57) rotula bien; pago publicado entre paréntesis: signo −1 lo transforma en magnitud positiva del modelo")
k_int, k_lr, k_ipl = ("aux:jumbo-annual-report-fy2020_p59_interest_paid_2019_2019", "aux:jumbo-annual-report-fy2020_p59_lease_repayments_2019_2019",
                      "aux:jumbo-annual-report-fy2020_p59_interest_paid_for_leases_2019_2019")
for k, ident, concepto in ((k_lr, "aux_intereses", "Lease repayments 2019 (etiqueta del emisor; es el INTERÉS de arrendamientos: etiquetas cruzadas, J3)"),
                           (k_ipl, "aux_arrendamientos_principal", "Interest paid for leases 2019 (etiqueta del emisor; es el PRINCIPAL de arrendamientos: etiquetas cruzadas, J3)")):
    e = copy.deepcopy(por[k])
    e["id"], e["fuente"]["concepto"], e["fuente"]["tratamiento"] = ident, concepto, J3
    e["fuente"]["ubicacion"] = "estado de flujos de efectivo consolidado (actividades de financiación; columna 01/01–31/12/2019)"
    e["comprobacion"] = comp(f"{A20} [PDF PAGE 59]; nota de costes financieros {A20} [PDF PAGE 86]",
                             "Mismo dato y misma cita que Mistral; cambian el concepto y el tratamiento (J3 también en 2019, correccion_fase1_partes_r2.json)")
    poner(e, "concepto y tratamiento J3 en 2019 (correccion_fase1_partes_r2.json; REVISION.md punto 1)")
for k, origenes, formula, conc in (
        ("Historia!F15", [k_int, k_lr], f'round(o["{k_int}"]+o["{k_lr}"], 4)',
         "intereses 2019 = «Interest paid» (explotación) 7,124703 + «Lease repayments» (es el interés de arrendamientos, J3) 1,488677 = 8,61338 → 8,6134"),
        ("Historia!F16", [k_lr], f'round(o["{k_lr}"], 4)', "intereses en financiación 2019 = «Lease repayments» (es el interés de arrendamientos, J3) 1,488677 → 1,4887"),
        ("Historia!F17", [k_ipl], f'round(o["{k_ipl}"], 4)', "principal de arrendamientos 2019 = «Interest paid for leases» (es el principal, J3) 4,312789 → 4,3128")):
    e = copy.deepcopy(por[k])
    e["valor_modelo"] = vm(k)
    e["derivacion"] = {"origenes": origenes, "formula": formula, "conciliacion": conc, "unidad": "millones de euros"}
    e["comprobacion"] = comp(None, "Derivado actualizado al libro vigente: J3 en la columna 2019 de AR2020 p. 59 (correccion_fase1_partes_r2.json)")
    poner(e, f"valor {por[k]['valor_modelo']!r} → {vm(k)!r}: J3 en 2019 (correccion_fase1_partes_r2.json; REVISION.md punto 1)")

# ---------------------------------------------------------------------------------------------- 2. acciones: escala (REVISION punto 2)
k_acc = "aux:jumbo-annual-report-fy2025_p142_ordinary_registered_shares_2025"
e = copy.deepcopy(por[k_acc])
e["fuente"]["escala"] = 1e-06
e["fuente"]["unidad"] = "acciones"
e["fuente"]["tratamiento"] += "; acciones en unidades → millones de acciones (escala 1e-6)"
e["comprobacion"] = comp(f"{AR25} [PDF PAGE 142]", "Escala corregida a 1e-6 (REVISION.md punto 2): 134.365.561 acciones = 134,365561 millones; cifra y cita sin cambios")
poner(e, "escala 1 → 1e-6 (REVISION.md punto 2)")

# ---------------------------------------------------------------------------------------------- 3. ceros con la cita del expediente (r2/r3)
R2, R3 = "resultados/correccion_fase1_partes_r2.json", "resultados/correccion_fase1_partes_r3.json"
PARTES = {}
for anio in (2016, 2017, 2018, 2019, 2021, 2024):
    PARTES[anio] = json.load(open(os.path.join(C, "fase1_partes", f"AR_{anio}.json"), encoding="utf-8"))["partidas"]
TXT = {2016: "texto/jumbo-annual-report-fy2016-17.txt", 2017: "texto/jumbo-annual-report-fy2017-18.txt", 2018: "texto/jumbo-annual-report-fy2018-19.txt",
       2019: "texto/jumbo-annual-report-transition-2019.txt", 2021: "texto/jumbo-annual-report-fy2021.txt", 2024: "texto/jumbo-annual-report-fy2024.txt"}
CEROS = (("Historia!C16", 2016, "intereses_financiacion", R2), ("Historia!D16", 2017, "intereses_financiacion", R2),
         ("Historia!E16", 2018, "intereses_financiacion", R2), ("Historia!C17", 2016, "arrendamientos_principal", R3),
         ("Historia!E23", 2018, "arrendamientos", R3), ("Historia!F13", 2019, "adquisiciones", R3), ("Historia!H13", 2021, "adquisiciones", R3))
for k, anio, partida, rastro in CEROS:
    cero = PARTES[anio][partida]["cero"]
    assert vm(k) == 0, k
    e = copy.deepcopy(por[k])
    f = e.get("fuente") or {}
    e["clase"] = "no_aplicable"
    e["fuente"] = {}
    e["justificacion"] = (
        f"El libro guarda 0 por ausencia de la partida, no por una cifra impresa: {cero['motivo']} (fase1_partes/AR_{anio}.json → partidas.{partida}.cero, "
        f"cita del expediente en {TXT[anio]} [PDF PAGE {cero['pagina']}]: «{cero['cita']}»; cambio registrado en {rastro}). La cita anterior del registro "
        f"(«{str(f.get('cita'))[:90]}…») no probaba el cero (cita forzada, REVISION.md punto 4) y la página no imprime un guion ni un 0 de esta partida que "
        "pueda contrastarse como cero comprobado; se declara no aplicable con su justificación. En fase1_v63.json sigue como cero PENDIENTE DE VERIFICACIÓN "
        "(pendientes_verificacion): solo una decisión humana registrada lo confirma.")
    if anio == 2019:
        e["incidencia"] = ("El cero es del año natural 2019, pero el informe de transición solo cubre jul–dic 2019; la columna del año natural de AR2020 PDF p. 59 "
                           "imprime también «-» en la misma línea (REVISION_ORQUESTACION_R2.md).")
    e["comprobacion"] = comp(f"{TXT[anio]} [PDF PAGE {cero['pagina']}]", f"Cita y motivo del expediente ({rastro}); clase no_aplicable (cero por ausencia, sin cifra impresa)")
    poner(e, f"cita forzada sustituida por la del expediente ({rastro}); cero_comprobado → no_aplicable")

# SBC 2024 (K18): el libro guarda ahora 0 (fase1_partes/AR_2024.json, «cero» de AR2024 p. 48), como J18 y L18
sbc = PARTES[2024]["sbc"]["cero"]
e = copy.deepcopy(por["Historia!L18"])
e["celda"], e["valor_modelo"] = "Historia!K18", vm("Historia!K18")
cita_sbc = linea(TXT[2024], sbc["pagina"], sbc["cita"])
e["fuente"] = fuente(TXT[2024], sbc["pagina"], "informe de gobierno corporativo / remuneración del consejo", "sbc: declaración de ausencia en el informe",
                     "2024 (columna del ejercicio corriente)", "ejercicio 2024 (1-ene-2024 a 31-dic-2024)", 0, cita_sbc,
                     tratamiento="declaración textual de ausencia (sin guion ni 0 impreso en tabla)")
e["justificacion"] = (f"El libro guarda 0 y el informe declara textualmente la ausencia: «{cita_sbc}» ({TXT[2024]} [PDF PAGE {sbc['pagina']}]). Motivo fase1: "
                      f"{sbc['motivo']} Se declara no_aplicable (no cero_comprobado), como J18 y L18, porque la página no imprime un guion ni un 0 en tabla.")
e["comprobacion"] = comp(f"{TXT[2024]} [PDF PAGE {sbc['pagina']}]", "El libro vigente guarda 0 (antes vacío): misma regla que J18 y L18")
poner(e, "dato_ausente (vacío) → no_aplicable con 0 del libro vigente (fase1_partes/AR_2024.json)")

# ---------------------------------------------------------------------------------------------- 4. capa F1 (Historia 85–87)
decl = json.load(open(os.path.join(C, "motor_a_f1.json"), encoding="utf-8"))
pr = decl["perimetro_reinversion"]
poner(nueva("Historia!C85", "F1.perimetro_reinversion", "hipotesis", vm("Historia!C85"), ambito="calculo", hipotesis={
    "identificacion": "H-F1.perimetro_reinversion (motor_a_f1.json → perimetro_reinversion)",
    "fundamento": ("Decisión registrada de la persona responsable (motor_a_f1.json → perimetro_reinversion.registro: " + json.dumps(pr["registro"], ensure_ascii=False)
                   + "). Reinversión necesaria = amortización propia sin derechos de uso ni PPA (A2_propio), como hipótesis declarada, no como dato. Hecho que la "
                   "condiciona: Jumbo no publica el reparto del capex entre mantenimiento y crecimiento. El libro escribe C85 con f1_libro_v631.py aplicar."),
    "alternativas": "A0_total (toda la D&A de la fila 8 como reposición; celda vacía); A1_sin_ROU (sin la D&A de derechos de uso, con la PPA dentro); A3_estimado.",
    "limites": ("Hipótesis declarada, no dato publicado; una firma no la demuestra y no se adopta para dinero real. Con A2 la D_X (fila 88) exige D&A, ROU y PPA del "
                "año: solo 2021–2025 tienen serie declarada (filas 86–87). El personaje la presenta condicionada y con su sensibilidad (F1-A)."),
    "procedencia": "motor_a_f1.json → Historia!C85 del libro (f1_libro_v631.py aplicar)"},
    comprobacion=comp("motor_a_f1.json → perimetro_reinversion", "Configuración de la capa F1: hipótesis declarada por la persona; el revisor comprueba que la decisión citada es la vigente.")),
    "nueva entrada F1 (antes dato_ausente con la celda vacía)")
COLS = dict(zip("CDEFGHIJKL", range(2016, 2026)))
for c, y in COLS.items():
    if y < 2021:
        continue
    s = decl["series"]["da_rou"][str(y)]
    k = f"Historia!{c}86"
    cita = linea(s["archivo"], s["pagina"], s["literal"])
    vf = int(s["literal"].strip("()").replace(".", "")) * (-1 if s["literal"].startswith("(") else 1)
    poner(nueva(k, "F1.da_rou", "dato_publicado", vm(k), ambito="calculo", fuente=fuente(
        s["archivo"], s["pagina"], s["cuadro"], "amortización de derechos de uso del año (fila «- Additions» de la sección «Depreciation», columna «Total of leasehold fixed assets»)",
        f"{y} (movimiento del año; la columna es la clase de activo «Total of leasehold fixed assets»)", f"ejercicio {y} (1-ene-{y} a 31-dic-{y})", vf, cita, signo=-1,
        tratamiento=f"cargo publicado entre paréntesis en euros («{s['literal']}»); magnitud positiva en el modelo (signo −1) y euros → mm (escala 1e-6), como la declaración F1 "
                    f"(motor_a_f1.json → series.da_rou.{y})"),
        comprobacion=comp(f"{s['archivo']} [PDF PAGE {s['pagina']}]", f"Serie F1 da_rou {y} de motor_a_f1.json; cita = la línea completa de la página")),
        "nueva entrada F1 (antes dato_ausente con la celda vacía)")
    p = decl["series"]["da_ppa"][str(y)]
    k = f"Historia!{c}87"
    assert vm(k) == 0, k
    cz = p["cero_comprobado"]
    poner(nueva(k, "F1.da_ppa", "no_aplicable", vm(k), ambito="calculo", justificacion=(
        f"PPA {y} = 0 por lectura, sin cifra impresa: {cz['motivo']} (motor_a_f1.json → series.da_ppa.{y}; {p['archivo']} [PDF PAGE {p['pagina']}], «{cz['cita']}»). "
        "La página no imprime un guion ni un 0 de esta partida que pueda contrastarse como cero comprobado: se declara no aplicable (no hay intangibles de "
        "combinaciones de negocios que amortizar), pendiente del revisor."),
        comprobacion=comp(f"{p['archivo']} [PDF PAGE {p['pagina']}]", "Cero por lectura de la declaración F1 (F1-SERIES-CERO), pendiente de revisor")),
        "nueva entrada F1 (antes dato_ausente con la celda vacía)")

# ---------------------------------------------------------------------------------------------- 5. Análisis y filas sin resolver
k_ebitda25 = aux("aux:jumbo-annual-report-fy2025_p148_ebitda_2025", 435.659964, fuente(
    AR25, 148, "cuenta de resultados consolidada (EBITDA)", "Earnings before interest, taxes, depreciation and amortization (grupo)", "2025 (columna del grupo, ejercicio corriente)",
    "ejercicio 2025 (1-ene-2025 a 31-dic-2025)", 435659964, linea(AR25, 148, "435.659.964")), "EBITDA del grupo 2025 (AR2025 PDF p. 148)")
k_ebitda_h126 = aux("aux:jumbo-h1-2026-financial-results_p23_ebitda_2026h1", 169.927311, fuente(
    H1, 23, "cuenta de resultados consolidada del semestre (EBITDA)", "Earnings before interest, taxes, depreciation and amortization (grupo, H1 2026)",
    "1-ene–30-jun-2026 (columna del grupo)", "semestre 1-ene-2026 a 30-jun-2026", 169927311, linea(H1, 23, "169.927.311")), "EBITDA del grupo H1 2026 (H1 2026 PDF p. 23)")
k_ebitda_h125 = aux("aux:jumbo-h1-2026-financial-results_p23_ebitda_2025h1", 165.352664, fuente(
    H1, 23, "cuenta de resultados consolidada del semestre (EBITDA)", "Earnings before interest, taxes, depreciation and amortization (grupo, H1 2025)",
    "1-ene–30-jun-2025 (columna comparativa del grupo)", "semestre 1-ene-2025 a 30-jun-2025", 165352664, linea(H1, 23, "165.352.664"),
    reexpresado="columna comparativa del semestral H1 2026"), "EBITDA del grupo H1 2025 (H1 2026 PDF p. 23)")
k_caja_h1 = aux("aux:jumbo-h1-2026-financial-results_p25_cash_and_cash_equivalents_2026h1", 546.140091, fuente(
    H1, 25, "balance consolidado (H1 2026)", "Cash and cash equivalents al 30-jun-2026 (grupo)", "30/06/2026 (columna corriente del grupo)", "cierre 30-jun-2026",
    546140091, linea(H1, 25, "546.140.091")), "Caja del grupo a 30-jun-2026 (H1 2026 PDF p. 25), sin redondear (C53 guarda 546,14)")
k_lease_h1 = "aux:jumbo-h1-2026-financial-results_p57_total_lease_liabilities_2026h1"
assert k_lease_h1 in por
LTM = f'(o["{k_ebitda25}"]+o["{k_ebitda_h126}"]-o["{k_ebitda_h125}"])'

e = nueva("Análisis!C33", "juicio_C33", "derivado", vm("Análisis!C33"), ambito="juicio", derivacion={
    "origenes": [k_lease_h1, k_caja_h1, k_ebitda25, k_ebitda_h126, k_ebitda_h125],
    "formula": f'round((o["{k_lease_h1}"]-o["{k_caja_h1}"])/{LTM}, 4)',
    "conciliacion": "deuda neta ÷ EBITDA LTM = (préstamos 0 + arrendamientos 62,247015 − caja 546,140091) ÷ (435,659964 + 169,927311 − 165,352664) = −483,893076 ÷ 440,234611 = −1,09917 → −1,0992 (Control maestro fila 36)",
    "unidad": "x"}, comprobacion=comp(None, "Derivado de cifras publicadas del H1 2026 (p. 23, 25, 57) y AR2025 (p. 148); préstamos = 0 («neither the Company nor the Group has any borrowings»)"))
poner(e, "sin resolver en Mistral → derivado (REVISION.md, dudas resolubles)")

e = nueva("Análisis!C42", "juicio_C42", "derivado", vm("Análisis!C42"), ambito="juicio", derivacion={
    "origenes": ["Análisis!C41", k_lease_h1, k_caja_h1, k_ebitda25, k_ebitda_h126, k_ebitda_h125],
    "formula": f'(o["Análisis!C41"]+o["{k_lease_h1}"]-o["{k_caja_h1}"])/{LTM}',
    "conciliacion": ("EV ÷ EBITDA LTM = (capitalización C41 = 27,28 × 134,365561 = 3.665,49250408 + arrendamientos 62,247015 − caja 546,140091) ÷ 440,234611 = "
                     "3.181,59942808 ÷ 440,234611 = 7,227054 (recalculo_C42.json; entradas_r3.json)"), "unidad": "x"},
    incidencia=("Desalineación de fechas declarada en el expediente (Control maestro M42/N42): el precio del 17-nov-2026 es posterior al dividendo de 0,70 € "
                "(pagado el 28-jul-2026) y a la fecha ex del reparto extraordinario de 1,00 €, mientras la caja es la del 30-jun-2026: 7,441x / 7,746x con los "
                "ajustes; el valor no se ajusta (decisión pendiente). Depende de C41 (precio, lectura externa sin bytes): no puede quedar comprobado mientras C37 no lo esté."),
    comprobacion=comp(None, "Recalculado en jumbo_e con el precio activo (resultados/recalculo_C42.json, entradas_r3.json); Mistral lo dejó sin resolver con el valor de la etapa 1 (6,4458)"))
poner(e, "6,4458 (etapa 1) → 7,227054 (recalculo_C42.json; REVISION.md punto 3)")

k_vak = aux("aux:jumbo-annual-report-fy2025_p48_acciones_vakakis_2025", 22.339966, fuente(
    AR25, 48, "informe de gobierno corporativo: acciones de los miembros del consejo", "acciones de A.-E. Vakakis (indirectas)", "31/12/2025",
    "cierre 31-dic-2025", 22339966, linea(AR25, 48, "22.339.966"), unidad="acciones"), "acciones del consejo (Vakakis, indirectas) AR2025 PDF p. 48")
k_ath = aux("aux:jumbo-annual-report-fy2025_p48_acciones_athanasiou_2025", 0.00036, fuente(
    AR25, 48, "informe de gobierno corporativo: acciones de los miembros del consejo", "acciones de A. Athanasiou (directas)", "31/12/2025",
    "cierre 31-dic-2025", 360, linea(AR25, 48, "360 direct"), unidad="acciones"), "acciones del consejo (Athanasiou) AR2025 PDF p. 48")
k_ter = aux("aux:jumbo-annual-report-fy2025_p49_acciones_terzaki_2025", 0.002022, fuente(
    AR25, 49, "informe de gobierno corporativo: acciones de la alta dirección", "acciones de I. Terzaki (alta dirección)", "31/12/2025",
    "cierre 31-dic-2025", 2022, linea(AR25, 49, "Terzaki Ioanna"), unidad="acciones"), "acciones de la alta dirección (Terzaki) AR2025 PDF p. 49")
e = nueva("Análisis!C96", "juicio_C96", "derivado", vm("Análisis!C96"), ambito="juicio", derivacion={
    "origenes": [k_vak, k_ath, k_ter, k_acc], "formula": f'(o["{k_vak}"]+o["{k_ath}"]+o["{k_ter}"])/o["{k_acc}"]',
    "conciliacion": "% de insiders a 31-dic-2025 = (22.339.966 + 360 + 2.022) ÷ 134.365.561 = 0,166280 (entradas_r3.json; Control maestro fila 75)", "unidad": "proporción"},
    incidencia=("La cifra impresa del 16,42 % (AR2025 PDF p. 143) no es esta partida: es la sociedad del presidente; que esté calculada sobre 136.059.759 acciones es "
                "una inferencia aritmética (22.339.966 ÷ 136.059.759 = 16,419 %), no un dato publicado (REVISION_ORQUESTACION_R2.md)."),
    comprobacion=comp(None, "Recalculado en jumbo_e (entradas_r3.json): 0,1663 → 0,166280 sin redondear"))
poner(e, "sin resolver en Mistral (0,1663) → derivado 0,166280 (entradas_r3.json)")

# C40: misma definición que C46 (P-O1 c, J1, J2), con C76 como origen (la convención de reparto)
K = {n: f"aux:jumbo-annual-report-fy2025_p155_{n}_2025" for n in ("dividends_received", "interest_received")}
k_bon = "aux:jumbo-annual-report-fy2025_p179_corporate_bonds_2025"
k_c23, k_c24, k_c25 = ("aux:jumbo-annual-report-fy2024_p149_cash_and_cash_equivalents_2023", "aux:jumbo-annual-report-fy2025_p150_cash_and_cash_equivalents_2024",
                       "aux:jumbo-annual-report-fy2025_p150_cash_and_cash_equivalents_2025")
for x in list(K.values()) + [k_bon, k_c23, k_c24, k_c25]:
    assert x in por, x
JC = ("Dato de la valoración que depende de la convención de reparto de la caja sobrante (Análisis!C76, juicio de las fases) por las decisiones P-O1 (c), J1 y J2: "
      "los intereses cobrados que cuentan son los que no corresponden a la caja sumada en C76. No es un dato publicado; sus componentes sí lo son.")
INC76 = ("DESFASE: el valor del libro se calculó con C76 = 200 (s = 200 ÷ caja media 471,8284), pero el libro vigente tiene C76 = {c76} (fases); con la fórmula "
         "declarada y el C76 vigente sale {alt}. El expediente lo anticipaba («SI LA FASE B CAMBIA C76, hay que recalcular los intereses que entran»): "
         "decisión pendiente de la orquestación/persona responsable; aquí no se cambia el libro.{extra}")
c76 = vm("Análisis!C76")
e = copy.deepcopy(por["Análisis!C40"])
e.update(valor_modelo=vm("Análisis!C40"), justificacion_clase=JC, derivacion={
    "origenes": ["Historia!L11", "Historia!L12", "Historia!L16", "Historia!L17", K["dividends_received"], K["interest_received"], k_bon, k_c23, k_c24, k_c25, "Análisis!C76"],
    "formula": (f'o["Historia!L11"]-o["Historia!L12"]-o["Historia!L16"]-o["Historia!L17"]+o["{K["dividends_received"]}"]+o["{K["interest_received"]}"]'
                f'-o["Análisis!C76"]/round((o["{k_c23}"]+o["{k_c24}"]+o["{k_c25}"])/3, 4)*(o["{K["interest_received"]}"]-o["{k_bon}"])'),
    "conciliacion": ("FCF del accionista 2025 con la definición de C46 (entradas_r3.json): CFO 296,9129 − capex 38,384 − intereses de arrendamientos 2,3258 − principal 9,7272 "
                     "+ dividendos 1,8762 + intereses cobrados 9,91679 − s × (9,91679 − cupones 0,595058), s = C76 ÷ caja media 2023–2025 redondeada a 4 decimales (471,8284, como la nota "
                     "del expediente) = 254,317567 con C76 = 200"),
    "unidad": "millones de euros"})
vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else vm(o)) for o in e["derivacion"]["origenes"]}
e["incidencia"] = INC76.format(c76=c76, alt=round(float(VE._eval_formula_exacta(e["derivacion"]["formula"], vals)), 6), extra=(
    " Además, el libro guarda el importe sin redondear (254,31756701901787): con la regla de importes (U2) solo vale el exacto o un redondeo a 3 decimales, "
    "y el exacto de una división no es representable; aunque C76 vuelva a cuadrar, la comprobación exige que el expediente guarde C40 redondeado (p. ej. 254,318)."))
e["comprobacion"] = comp(None, "Recalculado en jumbo_e (entradas_r3.json): 246,48 → 254,317567 con la definición de C46")
poner(e, "246,48 (etapa 1) → 254,317567 (entradas_r3.json; REVISION_ORQUESTACION_R2.md)")

e = copy.deepcopy(por["Análisis!C46"])
vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else vm(o)) for o in e["derivacion"]["origenes"]}
e["justificacion_clase"] = JC
e["incidencia"] = INC76.format(c76=c76, alt=round(float(VE._eval_formula_exacta(e["derivacion"]["formula"], vals)), 6), extra="")
e["comprobacion"] = comp(None, "Misma fórmula y orígenes que Mistral; se añade la justificación de clase (N2: depende de C76) y el desfase con el C76 vigente")
poner(e, "justificacion_clase (N2) e incidencia del desfase con C76 vigente")

# L14 e I17 (REVISION, dudas resolubles)
k_l14 = aux("aux:jumbo-annual-report-fy2025_p209_variacion_circulante_subtotal_2025", -61.158549, fuente(
    AR25, 209, "estado de flujos de la sociedad/grupo, ajustes de circulante (subtotal)", "subtotal de las variaciones del circulante (inventarios, cobros, otros activos corrientes, depósitos restringidos no corrientes y pasivos)",
    "2025 (columna del grupo, ejercicio corriente)", "ejercicio 2025 (1-ene-2025 a 31-dic-2025)", -61158549, linea(AR25, 209, "(61.158.549)"),
    tratamiento="subtotal publicado entre paréntesis (consume caja); la fórmula cambia el signo a la convención de la fila 14 (+ consume caja)"),
    "subtotal de circulante 2025 (AR2025 PDF p. 209)")
e = nueva("Historia!L14", "h_circulante", "derivado", vm("Historia!L14"), ambito="calculo", derivacion={
    "origenes": [k_l14], "formula": f'round(-o["{k_l14}"], 4)',
    "conciliacion": "aumento del circulante 2025 = −(subtotal publicado (61.158.549)) = 61,158549 → 61,1585 (la suma de los componentes da 61,15855 por el redondeo de cada uno)", "unidad": "millones de euros"},
    incidencia="Incluye 1,45 mm de «Non-short-term restricted bank deposits» (REVISION.md, duda de significado de J14 para 2023: −9,6 mm).",
    comprobacion=comp(None, "Sin resolver en Mistral (empate de redondeo de los componentes); el subtotal publicado reproduce el libro"))
poner(e, "sin resolver en Mistral → derivado del subtotal publicado (REVISION.md)")
k_i17 = "aux:jumbo-annual-report-fy2023.conversion_p71_interest_paid_for_leases_etiqueta_del_emis_2022"
A23 = "texto/jumbo-annual-report-fy2023.conversion.txt"
e = copy.deepcopy(por["aux:jumbo-annual-report-fy2022.conversion_p68_interest_paid_for_leases_etiqueta_del_emis_2021"])
e.update(celda=k_i17, valor_modelo=7.03515)
e["fuente"] = dict(e["fuente"], documento=DOCS[A23]["documento"], version=DOCS[A23]["version"], archivo=A23, sha256=DOCS[A23]["sha256"], pagina=71,
                   columna="2022 (columna comparativa «anterior» del informe siguiente)", periodo="ejercicio 2022 (1-ene-2022 a 31-dic-2022)", valor_fuente=-7035150,
                   cita=linea(A23, 71, "Interest paid for leases"),
                   tratamiento=e["fuente"]["tratamiento"].replace("PDF p. 92", "PDF p. 95 (AR2023)"))
e["comprobacion"] = comp(f"{A23} [PDF PAGE 71]", "Principal de arrendamientos 2022 (etiqueta cruzada J3), comparativo de AR2023")
poner(e, "auxiliar nuevo (orquestación): principal 2022 (J3) de AR2023 p. 71")
e = nueva("Historia!I17", "juicio_h17", "derivado", vm("Historia!I17"), ambito="juicio", derivacion={
    "origenes": [k_i17], "formula": f'round(o["{k_i17}"], 4)',
    "conciliacion": "principal de arrendamientos 2022 = «Interest paid for leases» (J3) 7.035.150 € = 7,03515 mm", "unidad": "millones de euros"},
    incidencia=("EMPATE DE REDONDEO: la cifra publicada es 7,03515 mm; ROUND de la hoja (mitad lejos de cero) da 7,0352 y el libro guarda 7,0351 (redondeo binario del "
                "generador): diferencia de 50 €. Con la regla de importes (U2) no es el exacto ni un redondeo a 3 decimales: el revisor verá la discrepancia; "
                "corregirla exige regenerar la Historia, no cambiar la cifra publicada."),
    comprobacion=comp(None, "Sin resolver en Mistral; se registra la derivación real con la incidencia del redondeo"))
poner(e, "sin resolver en Mistral → derivado con incidencia de redondeo (REVISION.md)")


# datos de juicio de texto o con operaciones que el contrato no admite: convención con su justificación de clase (N2)
def conv(k, just, alternativas, limites):
    ev = EVID.get(k) or {}
    fund = " · ".join(f"Control maestro!{c}{ev.get('fila')}: {ev[c]}" for c in ("L", "M", "N") if ev.get(c))
    poner(nueva(k, por[k].get("id") or f"juicio_{k.split('!')[1]}", "convencion", vm(k), ambito="juicio", justificacion_clase=just, hipotesis={
        "identificacion": "V-" + k.split("!")[1], "fundamento": "Cálculo o clasificación de la etapa 1, tal como lo documenta el libro: " + fund,
        "alternativas": alternativas, "limites": limites, "procedencia": f"Control maestro!L–N{ev.get('fila')} del libro (Jumbo_v63_evaluada.xlsx)"},
        comprobacion=comp(f"Control maestro fila {ev.get('fila')} del libro", "Sin resolver en Mistral; se registra como dato tratado como convención (se lista aparte)")),
        "sin resolver en Mistral → convencion con justificacion_clase")


conv("Análisis!C28", "Etiqueta de texto (Dilución / Recompra / Estable) que la etapa 1 deriva de las acciones diluidas medias 2020→2025 (AR2025 p. 181) con un umbral; no es una cifra publicada.",
     "Con un umbral de ±2 % sería «Estable» (Control maestro N33).", "Informativa, no es aviso; depende del umbral de la regla.")
conv("Análisis!C31", "Veredicto de texto («No») de una comparación de crecimientos (inventario y cobros frente a ventas) decidida por el inversor (comparación semestral); no es una cifra publicada.",
     "La comparación anual (inventario +19,0 % frente a ventas +7,2 %) daría BANDERA (Control maestro N34).", "Depende del período de comparación elegido (decisión del inversor del 11-oct-2026).")
conv("Análisis!C34", "Veredicto de texto («Sí») de la comparación caja no restringida (546,14) frente a deuda financiera a corto (0); no es una cifra publicada.",
     "Con los arrendamientos a corto (9,44) la cobertura es 57,9x (Control maestro M37).", "Depende de qué se cuente como deuda a corto; los restringidos (9,66) quedan fuera de la caja.")
conv("Análisis!C60", "Tasa de crecimiento compuesto de las acciones diluidas (136,06 → 134,37 mm, AR2025 p. 181): exige una raíz, que el contrato de fórmulas no admite; no es una cifra publicada.",
     "Con 3 años (2022→2025): −0,42 %/año (Control maestro N55).", "Cálculo a mano, no reproducible por la máquina; el revisor lo recalcula.")
ev32 = EVID.get("Análisis!C32") or {}
poner(nueva("Análisis!C32", "juicio_C32", "no_aplicable", vm("Análisis!C32"), ambito="juicio", justificacion=(
    f"Goodwill ÷ activo total = 0 porque el balance del grupo no tiene fondo de comercio (AR2025 PDF p. 150; H1 2026 PDF p. 25): no hay cifra de goodwill impresa que "
    f"contrastar. Control maestro M{ev32.get('fila')}: {ev32.get('M')} La compra de HERALD 2 (2025) dio una ganancia por compra ventajosa, no fondo de comercio (AR2025 PDF p. 189)."),
    comprobacion=comp("texto/jumbo-annual-report-fy2025.txt [PDF PAGE 150]; [PDF PAGE 189]", "Sin resolver en Mistral; cero por ausencia de la partida")),
    "sin resolver en Mistral → no_aplicable (sin fondo de comercio)")

# C88: el expediente lo declara ahora «Dato no verificable»
e = copy.deepcopy(por["Análisis!C88"])
ev88 = EVID.get("Análisis!C88") or {}
e["incidencia"] = f"El expediente lo marca «{ev88.get('F')}» (entradas_r3.json): {ev88.get('N')}"
e["comprobacion"] = dict(e["comprobacion"], extractor=EXT, fecha=HOY, nota="Lectura externa de Mistral sin cambios; se añade la marca del expediente («Dato no verificable», entradas_r3.json)")
poner(e, "incidencia: «Dato no verificable» del expediente (entradas_r3.json)")

# ---------------------------------------------------------------------------------------------- 6. hipótesis: el texto de las fases
FASES = {}
for f_ in ("A", "B", "C"):
    p_ = os.path.join(C, f"celdas_{f_}.json")
    if os.path.exists(p_):
        d_ = json.load(open(p_, encoding="utf-8"))
        for x in (d_ if isinstance(d_, list) else d_.get("celdas") or d_.get("cambios") or []):
            if isinstance(x, dict) and x.get("celda"):
                FASES[str(x["celda"]).replace("'", "")] = f_
        if isinstance(d_, dict):
            for kk in d_:
                if "!" in kk:
                    FASES[kk.replace("'", "")] = f_
for k in list(por):
    e = por[k]
    if e.get("clase") not in ("hipotesis", "convencion") or k.startswith("aux:") or INST["tipos"].get(k) != "hipótesis" or k == "Historia!C85":
        continue
    ev = EVID.get(k) or {}
    n = str(ev.get("N") or "")
    m_cl = re.match(r"\[Clase: ([^\]]+)\] \[Confianza: ([^\]]+)\]", n)
    if not m_cl:
        if (e.get("hipotesis") or {}).get("fundamento"):
            continue  # convención de Mistral ya completa (p. ej. Control maestro!J4)
        raise SystemExit(f"{k}: sin texto de fase en Control maestro N")
    clase_decl, conf = m_cl.group(1), m_cl.group(2)
    clase = "convencion" if clase_decl.startswith("convenci") else "hipotesis"
    ref = re.search(r"(Referencia mecánica:.*?)(?=\s*Apoyo:|\s*Lo sustituiría:|$)", n, re.S)
    sust = re.search(r"(Lo sustituiría:.*)$", n, re.S)
    rango = re.search(r"(Rango[^.]*?\d[^.]*?)\.(?:\s|$)", n)
    fase = FASES.get(k)
    proc = f"Control maestro!N{ev.get('fila')} del libro (Jumbo_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = (e.get("clase"), e.get("valor_modelo"))
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
    poner(e, "hipótesis: texto de la fase" + (f" (valor {antes[1]!r} → {vm(k)!r})" if antes[1] != vm(k) else ""))

# ---------------------------------------------------------------------------------------------- cabecera y escritura
assert all(e.get("valor_modelo") == INST["celdas"].get(e["celda"]) or VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(e["celda"]))
           for e in reg["entradas"] if not e["celda"].startswith("aux:")), "valores desfasados"
for e in reg["entradas"]:
    c_ = e.get("comprobacion") or {}
    assert c_.get("resultado") == "pendiente" and c_.get("revisor") is None and not c_.get("vinculo"), e["celda"]
reg["libro"] = os.path.basename(VE.libro_de(C))
reg["huella_entradas_economicas"] = INST["huella"]
reg["extractor_complementario"] = EXT
reg["fecha_extraccion_complementaria"] = HOY
reg["nota_del_extractor_complementario"] = (
    f"Adaptado el {HOY} por {EXT} al expediente jumbo_e: parte del registro de Mistral (mistral/examen-jumbo-entradas @ fced486) y aplica, solo donde el "
    "expediente ya lo recoge, las correcciones de la revisión del registro (coordinacion/cierre_v2/examen/jumbo/revision_registro/) y de la orquestación "
    "(resultados/: correccion_fase1_partes_r2/r3, recalculo_C42, entradas_r3, declaración F1). Las hipótesis llevan el texto que escribieron las fases "
    "(Control maestro N). Las entradas cambiadas declaran como extractor «Claude orquestación»; todas las comprobaciones quedan «pendiente», sin revisor ni "
    "vínculo: el sellado es de un revisor independiente. Lista de cambios: resultados/registro_entradas_jumbo_e.json.")
json.dump(reg, open(os.path.join(C, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
vistos = {}
for x in CAMBIOS:
    vistos[x["celda"]] = x["motivo"]
json.dump({"fecha": HOY, "autor": EXT + " (agente de implementación; sin firma humana)", "guion": "resultados/scripts/registro_entradas_jumbo_e.py",
           "origen": "munger-v2-evidencias-mistral, mistral/examen-jumbo-entradas @ fced486, resultados_examen/jumbo/verificacion_entradas.json",
           "registro_mistral_sha256": hashlib.sha256(open(MISTRAL, "rb").read()).hexdigest(),
           "registro_sha256": hashlib.sha256(open(os.path.join(C, VE.REGISTRO), "rb").read()).hexdigest(),
           "entradas": len(reg["entradas"]), "universo": INST["n"], "cambiadas": len(vistos),
           "cambiadas_universo": sum(1 for k in vistos if not k.startswith("aux:")), "cambiadas_auxiliares": sum(1 for k in vistos if k.startswith("aux:")),
           "cambios": [{"celda": k, "motivo": v} for k, v in vistos.items()]},
          open(SALIDA, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("entradas", len(reg["entradas"]), "cambiadas", len(vistos))
