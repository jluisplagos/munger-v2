#!/usr/bin/env python3
"""zoetis_t2 · registro de entradas (verificacion_entradas.json, versión sellada y comprometida de zoetis_t1d, 897db35, igual en dfc0a2c) puesto al día con el segundo tiempo:
LTM y balance a 30-sep-2026 (10-Q T3 2026), precio y Treasury del 5-nov-2026. Extractor: «Claude orquestación». Cada entrada cambiada o nueva queda
PENDIENTE (sin revisor ni vínculo) para otro agente; las demás no se tocan y conservan su sello solo si `verificacion_entradas.py comprobar`
mantiene su vínculo vigente (nada se reescribe a mano). Los auxiliares nuevos salen de cifras_t3.py, que comprueba cada cifra en su línea y página
de texto/; las citas son esas líneas. Las entradas de las celdas que escriben las fases (C25, C27, C51, C56, C61, C62, C76, Palancas…) no se tocan:
las rehacen las fases del segundo tiempo y su registro se pone al día después, como en zoetis_t1d.
Uso: python3 -I corregir_registro_zoetis_t2.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO_CAMBIOS.json"""
import copy, datetime as dt, hashlib, json, os, shutil, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cifras_t3 as CT  # noqa: E402
C, ANT, REG = (os.path.abspath(x) for x in sys.argv[1:4])
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
cons = os.path.join(ANT, "verificacion_entradas_conservado_de_zoetis_t1d.json")
assert not os.path.exists(cons)
shutil.copy2(p, cons)
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
HOY = "2026-11-19"
cambios = []
tx = CT.Textos(os.path.join(C, "texto"))
v, dd = CT.calcular(tx)
SHA_Q3T = tx.sha(CT.Q3)
assert SHA_Q3T == "ddcd22703ceef1da78f5bc57015671e10c0eac411cee79f3710f98e0f777e70b"
for k, (aid, val) in CT.AUX_10K.items():
    assert E[aid]["valor_modelo"] == val and E[aid]["comprobacion"]["resultado"] == "verificado", aid


def pendiente(e, nota, nueva=False):
    antes = None if nueva else copy.deepcopy(e)
    c0 = (e.get("comprobacion") or {}) if not nueva else {}
    e["comprobacion"] = {"extractor": "Claude orquestación", "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[Claude orquestación, {HOY}, zoetis_t2] {nota}"
                         + ("" if nueva else f" · Comprobación anterior (zoetis_t1d): {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}"),
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "antes": antes, "despues": copy.deepcopy(e)})


UBIC = {3: "cuenta de resultados del 10-Q (Condensed Consolidated Statements of Income)", 5: "balance del 10-Q (Condensed Consolidated Balance Sheets)",
        8: "estado de flujos del 10-Q (Condensed Consolidated Statements of Cash Flows)", 10: "nota 2 del 10-Q, «Fiscal Year Alignment» (cambios en los resultados)",
        11: "nota 2 del 10-Q, «Fiscal Year Alignment» (cambios en el estado de flujos)"}
NEG = {"q3_p8_capex_9m2026", "q3_p8_capex_9m2025"}


def fuente_q3(k):
    a, n, pref, i, val, concepto, columna, periodo, reexp = CT.COMP[k]
    linea = tx.linea(a, n, pref, i, val).strip()
    signo = -1 if k in NEG else 1
    return {"documento": "Form 10-Q del tercer trimestre de 2026 de Zoetis Inc. (estados financieros consolidados interinos del tercer trimestre de 2026)",
            "version": ("PDF oficial «zoetis-10q-2026-q3.pdf», sha256 f797be282a86905e29ea3d41573fba5a645f2db674fc7c0f26fb93c0f71242bf (Release fuentes-examen-20261118 "
                        "del repositorio auxiliar jluisplagos/munger-v2-evidencias-mistral, descargado el 2026-11-19 y verificado contra RELEASE_FUENTES_EXAMEN_SHA256SUMS "
                        f"y FUENTES.tsv); texto extraído con marcas [PDF PAGE n] por cambiar_base.py (pdftotext -layout): «texto/{CT.Q3}», sha256 {SHA_Q3T}"),
            "archivo": f"texto/{CT.Q3}", "sha256": SHA_Q3T, "pagina": n, "folio": None, "ubicacion": UBIC[n], "concepto": concepto, "columna": columna, "periodo": periodo,
            "unidad": "mm", "escala": 1, "signo": signo,
            "tratamiento": ("pago publicado entre paréntesis: signo −1 lo transforma en magnitud positiva del modelo" if signo == -1 else "cifra tal como se publica; signo 1, sin transformación"),
            "perimetro": "consolidado", "reexpresado": reexp, "valor_fuente": int(val), "cita": linea}


AUX_USADOS = ["q3_p3_bai_9m2026", "q3_p10_bai_9m2025_prev", "q3_p3_interest_expense_9m2026", "q3_p3_interest_expense_9m2025", "q3_p8_da_9m2026", "q3_p8_da_9m2025",
              "q3_p3_taxes_9m2026", "q3_p10_taxes_9m2025_prev", "q3_p8_cfo_9m2026", "q3_p11_cfo_9m2025_prev", "q3_p8_capex_9m2026", "q3_p8_capex_9m2025",
              "q3_p8_finance_leases_9m2026", "q3_p8_finance_leases_9m2025", "q3_p5_cash_2026-09-30", "q3_p5_current_ltd_2026-09-30", "q3_p5_long_term_debt_2026-09-30",
              "q3_p5_goodwill_2026-09-30", "q3_p5_total_assets_2026-09-30", "q3_p5_total_equity_2026-09-30"]
A = {}
for k in AUX_USADOS:
    aid = CT.aux_id(k)
    assert aid not in E, aid
    f = fuente_q3(k)
    e = {"celda": aid, "id": "aux", "ambito": None, "uso": None, "material": True, "clase": "dato_publicado", "valor_modelo": f["signo"] * f["valor_fuente"],
         "fuente": f, "derivacion": None, "hipotesis": None, "justificacion": None, "comprobacion": None, "incidencia": None}
    d["entradas"].append(e); E[aid] = e; A[k] = aid
    pendiente(e, f"auxiliar nuevo del 10-Q T3 2026: {f['concepto']} ({f['columna']}), PDF p. {f['pagina']}", nueva=True)
K10 = {k: x[0] for k, x in CT.AUX_10K.items()}
o = lambda x: f'o["{x}"]'  # noqa: E731
BAI = f'({o(K10["bai_2025"])} - {o(A["q3_p10_bai_9m2025_prev"])} + {o(A["q3_p3_bai_9m2026"])})'
INT = f'({o(K10["interest_2025"])} - {o(A["q3_p3_interest_expense_9m2025"])} + {o(A["q3_p3_interest_expense_9m2026"])})'
DA = f'({o(K10["da_2025"])} - {o(A["q3_p8_da_9m2025"])} + {o(A["q3_p8_da_9m2026"])})'
TAX = f'({o(K10["taxes_2025"])} - {o(A["q3_p10_taxes_9m2025_prev"])} + {o(A["q3_p3_taxes_9m2026"])})'
DEUDA = f'({o(A["q3_p5_current_ltd_2026-09-30"])} + {o(A["q3_p5_long_term_debt_2026-09-30"])})'
CAJA = o(A["q3_p5_cash_2026-09-30"])
ORI_EBITDA = [K10["bai_2025"], A["q3_p10_bai_9m2025_prev"], A["q3_p3_bai_9m2026"], K10["interest_2025"], A["q3_p3_interest_expense_9m2025"],
              A["q3_p3_interest_expense_9m2026"], K10["da_2025"], A["q3_p8_da_9m2025"], A["q3_p8_da_9m2026"]]
ORI_DN = [A["q3_p5_current_ltd_2026-09-30"], A["q3_p5_long_term_debt_2026-09-30"], A["q3_p5_cash_2026-09-30"]]
FYA = ("El LTM a 30-sep-2026 se forma con 2025 del 10-K (base anterior a la «Fiscal Year Alignment») − 9M-2025 + 9M-2026 del 10-Q del T3 2026 (base nueva); "
       "la nota 2 da el 9M-2025 «As previously reported» para el BAI (2.599), los impuestos (529) y el CFO (2.011), que se usan, pero solo reexpresado "
       "para intereses (165), D&A (365), capex (462) y arrendamientos financieros (2): esos cuatro mezclan bases (10-Q T3 2026 PDF p. 3, 8, 10 y 11)")
JCL = ("{c} es una aproximación declarada, no un derivado exacto del concepto: " + FYA + ". Se registra como convención con su fundamento (como en "
       "zoetis_t1d); la fórmula de «derivacion» solo documenta la aproximación.")
ZACC = ("Desalineación de fechas declarada (decisión Z-ACC de la persona responsable, 19-nov-2026: se mantienen las acciones al cierre del ejercicio, P-O2): "
        "precio del 5-nov-2026 × acciones en circulación al 31-dic-2025")
conf = json.load(open(os.path.join(os.path.dirname(os.path.dirname(C)), "configuracion", "cambio_zoetis_t2.json"), encoding="utf-8"))
AN = conf["analisis"]


def convencion(celda, valor, origenes, formula, unidad, concil, alt, lim):
    c = celda.split("!")[1]
    e = E[celda]
    e["clase"] = "convencion"; e["valor_modelo"] = valor; e["fuente"] = {}
    e["derivacion"] = {"origenes": origenes, "formula": formula, "unidad": unidad, "conciliacion": "APROXIMACIÓN (documental): " + concil}
    e["hipotesis"] = {"identificacion": "V-" + c, "fundamento": f"{c} = {valor!r}: {concil} {FYA}.", "alternativas": alt, "limites": lim,
                      "procedencia": f"configuracion/cambio_zoetis_t2.json (analisis {c}); Control maestro G–N de la fila de {c}; resultados/scripts/cifras_t3.py"}
    e["justificacion"] = None
    e["justificacion_clase"] = JCL.format(c=c)
    e["incidencia"] = "APROXIMACIÓN declarada (Fiscal Year Alignment): " + FYA + "."
    assert AN[c]["valor"] == valor, c
    pendiente(e, f"{c} recalculado con el 10-Q T3 2026 (LTM y balance a 30-sep-2026); configuracion/cambio_zoetis_t2.json")


# C33
convencion("Análisis!C33", float(dd["C33"]), ORI_DN + ORI_EBITDA, f"({DEUDA} - {CAJA}) / ({BAI} + {INT} + {DA})", "x",
           "deuda neta ÷ EBITDA LTM = (750 + 8.299 − 1.333) ÷ (3.360 − 2.599 + 2.353 + 222 − 165 + 185 + 487 − 365 + 357 = 3.835) = 7.716 ÷ 3.835 = 2,011995",
           f"Con el 9M-2025 todo reexpresado (BAI 2.571) ≈ {float(dd['C33_recast']):.2f}x; con el 10-K 2025 reexpresado (la empresa dice que lo reexpresará al presentarlo como comparativo) se podría rehacer en una sola base.",
           "Mezcla bases (ver justificacion_clase). Sin acciones ni precio: no le afecta la desalineación de C41/C42 (deuda neta del 30-sep-2026 y EBITDA de 12 meses a esa fecha).")
# C40
ORI40 = [K10["cfo_2025"], A["q3_p11_cfo_9m2025_prev"], A["q3_p8_cfo_9m2026"], K10["capex_2025"], A["q3_p8_capex_9m2025"], A["q3_p8_capex_9m2026"],
         K10["fl_2025"], A["q3_p8_finance_leases_9m2025"], A["q3_p8_finance_leases_9m2026"]]
convencion("Análisis!C40", int(dd["fcf_ltm"]), ORI40,
           f'({o(ORI40[0])} - {o(ORI40[1])} + {o(ORI40[2])}) - ({o(ORI40[3])} - {o(ORI40[4])} + {o(ORI40[5])}) - ({o(ORI40[6])} - {o(ORI40[7])} + {o(ORI40[8])})', "mm",
           "FCF LTM = CFO (2.904 − 2.011 + 1.880 = 2.773) − capex (621 − 462 + 334 = 493) − principal de arrendamientos financieros (2 − 2 + 1 = 1) = 2.279",
           f"Todo reexpresado (CFO 9M-2025 2.056) sale {int(dd['fcf_ltm_recast'])}; Mistral (contraste) da 2.235 = CFO reexpresado − capex, sin arrendamientos financieros.",
           "Mezcla bases (ver justificacion_clase). Sin acciones ni precio: no le afecta la desalineación de C41/C42 (12 meses a 30-sep-2026).")
# C42
PRECIO, ACC = F("82.11"), F("424.927535")
C42 = float((PRECIO * ACC + dd["deuda_neta"]) / dd["ebitda_ltm"])
convencion("Análisis!C42", C42, ["Análisis!C41"] + ORI_DN + ORI_EBITDA, f'({o("Análisis!C41")} + {DEUDA} - {CAJA}) / ({BAI} + {INT} + {DA})', "x",
           "EV ÷ EBITDA LTM = (C41 34.890,79989885 + 9.049 − 1.333) ÷ 3.835 = 11,109987. " + ZACC + "; balance del 30-sep-2026 y EBITDA de 12 meses a esa fecha.",
           f"Con el 9M-2025 todo reexpresado ≈ 11,03x; con las 407.487.227 acciones del 30-sep-2026 (10-Q T3 2026 PDF p. 5) 10,74x.",
           "Mezcla bases (ver justificacion_clase). " + ZACC + ". Depende de C41 y de C37 (transcripción del 5-nov-2026, pendiente de revisor; falta captura o CSV).")
# C24
ORI24 = ORI_EBITDA[:6] + [K10["taxes_2025"], A["q3_p10_taxes_9m2025_prev"], A["q3_p3_taxes_9m2026"], A["q3_p5_total_equity_2026-09-30"]] + ORI_DN
convencion("Análisis!C24", float(dd["C24"]), ORI24, f'({BAI} + {INT}) * (1 - {TAX} / {BAI}) / ({o(A["q3_p5_total_equity_2026-09-30"])} + {DEUDA} - {CAJA})', None,
           "ROIC después de impuestos (definición de la etapa 1) = EBIT LTM (3.114 + 242 = 3.356) × (1 − impuestos LTM 628 ÷ BAI LTM 3.114) ÷ capital invertido a "
           "30-sep-2026 (patrimonio 3.303 + deuda 9.049 − caja 1.333 = 11.019) = 2.679,1959 ÷ 11.019 = 0,243143 (exacto)",
           "Capital medio 31-dic-2025 (reexpresado, 10.007) y 30-sep-2026 → 25,5 %; restando las inversiones a corto (200) → 24,8 %; la etapa 1 (26,6 %) usaba capital medio jun-25/jun-26 con el 10-Q del T2 2025, que no está en el expediente.",
           "Mezcla bases (ver justificacion_clase); el capital es el del fin de los doce meses porque el 10-Q del T3 no publica el balance del 30-sep-2025 (como en ahold_f4).")
E["Análisis!C24"]["hipotesis"]["procedencia"] += "; sustituye la convención no reproducible de zoetis_t1d (0,266 de la etapa 1)"
# C32: derivado exacto
e = E["Análisis!C32"]
e["valor_modelo"] = float(dd["C32"]); e["fuente"] = {}
e["derivacion"] = {"origenes": [A["q3_p5_goodwill_2026-09-30"], A["q3_p5_total_assets_2026-09-30"]],
                   "formula": f'{o(A["q3_p5_goodwill_2026-09-30"])} / {o(A["q3_p5_total_assets_2026-09-30"])}',
                   "conciliacion": "goodwill / activo total a 30-sep-2026 = 2.888 / 15.088 = 0,1914103923647932 exacto = libro (sin el round(…, 3) de zoetis_t1d)", "unidad": None}
assert AN["C32"]["valor"] == e["valor_modelo"]
pendiente(e, "C32 con el balance del 30-sep-2026 (10-Q T3 p. 5), cociente exacto")
# C53: dato publicado
e = E["Análisis!C53"]
f = copy.deepcopy(E[A["q3_p5_cash_2026-09-30"]]["fuente"])
f.update({"ubicacion": "balance consolidado (Condensed Consolidated Balance Sheets)", "periodo": "saldo a 30-sep-2026 (10-Q 3T26)", "folio": 3,
          "tratamiento": "cifra tal como se publica (incluye 2 de caja restringida, nota (b) del balance); inversiones a corto (200) aparte"})
e["valor_modelo"] = 1333; e["fuente"] = f
pendiente(e, "C53 = caja a 30-sep-2026 (10-Q T3 p. 5)")
# C54: derivado (porción corriente + deuda a largo)
e = E["Análisis!C54"]
e["clase"] = "derivado"; e["valor_modelo"] = 9049; e["fuente"] = {}
e["derivacion"] = {"origenes": [A["q3_p5_current_ltd_2026-09-30"], A["q3_p5_long_term_debt_2026-09-30"]], "formula": DEUDA,
                   "conciliacion": "deuda financiera a 30-sep-2026 = porción corriente 750 + deuda a largo plazo 8.299 = 9.049 = libro; sin préstamos a corto ni arrendamientos (como en zoetis_t1d)",
                   "unidad": "mm"}
pendiente(e, "C54 = 750 + 8.299 (10-Q T3 p. 5): de dato publicado a derivado (dos líneas del balance)")
# C31 y C34: convenciones con el fundamento del T3 (valor sin cambio)
e = E["Análisis!C31"]
assert e["valor_modelo"] == "Sí"
e["hipotesis"] = {"fundamento": ("Respuesta «Sí» (comprobada con el T3 2026): el 10-Q del T3 no publica el balance del 30-sep-2025; con las variaciones del estado de "
                                 "flujos (10-K 2025 p. 70 y 10-Q T3 p. 8: 2025 − 9M-2025 + 9M-2026) el inventario aumenta 160 (≈ +6,7 %, hasta 2.536) y los cobros 337 "
                                 "(≈ +24,9 %, hasta 1.692, 10-Q T3 p. 5) en doce meses, frente a ingresos de nueve meses +0,4 % reportados y −1 % operativos (10-Q T3 p. 3 y 29)."),
                  "alternativas": "«No» si se atribuye el aumento de cobros solo al calendario de ventas y cobros (la empresa: días de cobro dentro de 45–75, 10-Q T3 p. 42).",
                  "limites": "Juicio sobre datos publicados; las variaciones del estado de flujos mezclan el 2025 del 10-K con el 9M-2025 reexpresado (aproximación)."}
pendiente(e, "C31: fundamento con el T3 2026, valor sin cambio")
e = E["Análisis!C34"]
assert e["valor_modelo"] == "Sí"
e["hipotesis"] = {"fundamento": ("Respuesta «Sí» (comprobada con el T3 2026): caja no restringida 1.331 (1.333 − 2) frente a deuda a corto 750 (porción corriente del bono "
                                 "del 3,000 % que vence el 12-sep-2027) a 30-sep-2026 = 1,77x (10-Q T3 2026 PDF p. 5 y 44); revolving de 1.250 sin disponer, prorrogado hasta "
                                 "el 27-ago-2031 (p. 42)."),
                  "alternativas": "Con las inversiones a corto (200), 2,04x; «No» solo si se exigiera cubrir también los pasivos corrientes no financieros.",
                  "limites": "Juicio de la fase sobre el balance publicado."}
pendiente(e, "C34: fundamento con el balance del 30-sep-2026, valor sin cambio")
# C37: precio del 5-nov-2026 (transcripción de Mistral)
nm = "Zoetis_IR_XNYS_ZTS_historico_acciones_20261118_mistral_examen_zoetis_t2.txt"
fm = os.path.join(C, "fuentes_mercado", nm)
e = E["Análisis!C37"]
e["valor_modelo"] = 82.11
e["fuente"].update({
    "documento": "Página oficial de la empresa (Zoetis Investor Relations), «Stock Information», tabla «XNYS:ZTS historical stock data»",
    "version": (f"transcripción de la tabla hecha por el extractor Mistral (mistral-large-4-0) el 2026-11-18 (web_fetch de https://investor.zoetis.com/stock-information/default.aspx), "
                f"conservada en su rama mistral/examen-zoetis-t2 (resultados_examen/zoetis_t2/fuentes_mercado/, huella publicada en su HUELLAS.txt) y copiada byte a byte en "
                f"fuentes_mercado/{nm}, sha256 {h(fm)}. FALTA una captura o un CSV original de la página: solo hay transcripción"),
    "archivo": f"fuentes_mercado/{nm}", "sha256": h(fm), "pagina": 1, "folio": None,
    "ubicacion": "tabla «Stock Date | Stock Price», filas de noviembre de 2026", "concepto": "precio de cierre por acción (XNYS: ZTS) de la sesión del 5-nov-2026",
    "columna": "Stock Price (fila November 05, 2026)", "periodo": "cierre de la sesión del 5-nov-2026",
    "tratamiento": ("precio de cierre (no ajustado) de la sesión del 5-nov-2026, el día de la publicación del T3, sin transformación. La transcripción del extractor "
                    "heredada de zoetis_t1d (Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt, sha256 7a8d45f2…ad) da el mismo cierre. La página de la bolsa "
                    "(nyse.com) bloquea el acceso automatizado; se usa la página oficial de la empresa."),
    "valor_fuente": 82.11, "cita": "November 05, 2026 | $82.11"})
assert "November 05, 2026 | $82.11" in open(fm, encoding="utf-8").read().split("\n")
e["incidencia"] = "Solo transcripción del extractor (sin captura ni CSV original de la página): pendiente de revisor; si se exige captura, la tiene que aportar la persona."
pendiente(e, "C37 = cierre del 5-nov-2026 (segundo tiempo), transcripción de Mistral conservada con su huella; falta captura o CSV original")
# C41
e = E["Análisis!C41"]
assert PRECIO * ACC == F("34890.79989885")
e["valor_modelo"] = 34890.79989885
e["derivacion"]["conciliacion"] = ("capitalización = C37 82,11 × C55 424,927535 = 34.890,79989885 exacto = libro (sin redondear las acciones ni el resultado). " + ZACC +
                                    "; con las 407.487.227 acciones del 30-sep-2026 (10-Q T3 2026 PDF p. 5) sería 33.458,77620897 y con las 406.316.147 del 30-oct-2026 "
                                    "(portada del 10-Q T3) 33.362,61883017. C37: transcripción de investor.zoetis.com del 5-nov-2026 (falta captura o CSV).")
e["incidencia"] = "C37 sale de una transcripción del extractor (5-nov-2026), pendiente de revisor."
pendiente(e, "C41 = C37 × C55 exactos con el precio del 5-nov-2026; Z-ACC declarada")
# C55 (valor sin cambio; texto de la desalineación con la fecha nueva)
e = E["Análisis!C55"]
assert "precio del 8-oct-2026 × acciones" in e["fuente"]["tratamiento"]
e["fuente"]["tratamiento"] = e["fuente"]["tratamiento"].replace("precio del 8-oct-2026 × acciones", "precio del 5-nov-2026 × acciones") + (
    " (zoetis_t2) Últimas cifras tras el cierre, no usadas: 407.487.227 a 30-sep-2026 (10-Q T3 p. 5) y 406.316.147 a 30-oct-2026 (portada del 10-Q T3).")
pendiente(e, "C55 sin cambio de valor; desalineación con el precio del 5-nov-2026")
# C57
tt = os.path.join(C, "fuentes_mercado", "US_Treasury_par_yield_2026_Release_766892834.txt")
fila = [l for l in open(tt, encoding="utf-8").read().split("\n") if l.startswith("11/05/2026 |")]
assert len(fila) == 1 and fila[0].split(" | ")[12] == "4.84"
e = E["Análisis!C57"]
assert e["fuente"]["sha256"] == h(tt)
e["valor_modelo"] = 0.0484
e["fuente"].update({"ubicacion": "tabla de la curva par diaria 2026 (cabecera «Date | 1 Mo | … | 10 Yr | 20 Yr | 30 Yr»), fila 11/05/2026", "periodo": "cierre del 5-nov-2026",
                    "valor_fuente": 4.84, "cita": fila[0],
                    "tratamiento": "tasa publicada en porcentaje; escala 0,01 la pasa a tanto por uno del modelo (4,84 % → 0,0484). Misma fecha que el precio (5-nov-2026)."})
pendiente(e, "C57 = Treasury a 10 años del 5-nov-2026 del CSV oficial (asset 766892834), fila 11/05/2026")
# Palancas!C45: fecha del precio (serial de Excel)
e = E["Palancas!C45"]
serial = (dt.date(2026, 11, 5) - dt.date(1899, 12, 30)).days
assert e["valor_modelo"] == 46303 and serial == 46331
e["valor_modelo"] = serial
e["hipotesis"]["fundamento"] = (f"Fecha del precio usado en el análisis: fila «November 05, 2026 | $82.11» de la tabla XNYS:ZTS historical stock data de la página oficial de "
                                f"la empresa (investor.zoetis.com), archivo fuentes_mercado/{nm}, [PDF PAGE 1], sha256 {h(fm)}. El libro guarda esa fecha como serial de "
                                f"Excel {serial} = 2026-11-05 (calendario Excel 1900).")
e["hipotesis"]["limites"] = e["hipotesis"]["limites"].replace("46303 = 2026-10-08", f"{serial} = 2026-11-05")
e["justificacion_clase"] = e["justificacion_clase"].replace("46303 = 2026-10-08", f"{serial} = 2026-11-05")
pendiente(e, "Palancas!C45 = 2026-11-05 (fecha del precio del segundo tiempo)")
# fuentes de mercado y nota
d["fuentes_mercado"]["contenido"][nm] = {"que": ("transcripción de la tabla «XNYS:ZTS historical stock data» de investor.zoetis.com hecha por Mistral el 18-nov-2026 (rama "
                                                 "mistral/examen-zoetis-t2); fila usada «November 05, 2026 | $82.11» (C37). Falta captura o CSV original. (zoetis_t2)"), "sha256": h(fm)}
d["nota_del_extractor_complementario"] = str(d.get("nota_del_extractor_complementario") or "") + (
    f" (zoetis_t2, {HOY}) Segundo tiempo: registro sellado y comprometido de zoetis_t1d (897db35, «registros definitivos»; igual en dfc0a2c, auditoría aprobada del primer tiempo); Claude orquestación corrigió o añadió {len(cambios)} entradas "
    "(resultados/registro_cambios_zoetis_t2.json: LTM y balance a 30-sep-2026, precio y Treasury del 5-nov-2026): quedan pendientes de otro revisor. "
    "Las entradas de las celdas de las fases se pondrán al día tras las fases del segundo tiempo.")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": "resultados/scripts/corregir_registro_zoetis_t2.py", "registro_antes_sha256": h(cons), "registro_despues_sha256": h(p),
           "entradas_corregidas": [x["celda"] for x in cambios], "cambios": cambios}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("corregidas o añadidas", len(cambios), [x["celda"] for x in cambios])
