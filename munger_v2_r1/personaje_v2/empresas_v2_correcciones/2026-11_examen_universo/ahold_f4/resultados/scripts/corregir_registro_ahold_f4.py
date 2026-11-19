#!/usr/bin/env python3
"""ahold_f4 · correcciones del registro de entradas (verificacion_entradas.json, conservado de ahold_f3 por cambiar_base.py).
Extractor: «Claude orquestación». Cada entrada cambiada queda PENDIENTE (sin revisor ni vínculo): la revisará otro agente. Las demás no se tocan;
su sello sigue solo si `verificacion_entradas.py comprobar` mantiene su vínculo vigente (nada se reescribe a mano).
  1. A-Q3 (19-nov-2026): C24, C33, C40, C42 (derivados), C53 y C54 (datos publicados) con el informe del 3T 2026; auxiliares del 2T sin uso
     retirados y auxiliares del 3T añadidos (cada cifra leída aquí en su página de texto/ y comprobada); C31 y C34 (convenciones) con su
     fundamento comprobado con el 3T.
  2. A-NIC17: Historia C22 y D22 declaran la inclusión de los arrendamientos financieros NIC 17 (decisión «dejarla» de la persona responsable).
  3. G26, H26 y K26: campo «columna» = comparativo del informe N+1 (REVISION_SELLADO.md, segunda pasada).
  4. Encargo del coordinador (19-nov-2026): C57 = 0,0337 con el CSV oficial de la Bundesbank (WT1010, 13-nov-2026) y Palancas!C7 con la tabla de
     Damodaran (damodaran_margin.xls, fila 83), ambos conservados en fuentes_mercado/ (resultados/fuentes_mercado_ahold_f4.json).
Uso: python3 -I corregir_registro_ahold_f4.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO_CAMBIOS.json"""
import copy, hashlib, json, os, re, shutil, sys
C, ANT, REG = sys.argv[1:4]
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
shutil.copy2(p, os.path.join(ANT, "verificacion_entradas_conservado_de_ahold_f3.json"))
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
HOY, EXT = "2026-11-19", "Claude orquestación"
cambios = []
DEC = "decisión A-Q3 de la persona responsable (19-nov-2026, DECISIONES_PARA_EL_USUARIO.md, «19-nov-2026 (mañana)»)"


def pendiente(e, nota, antes=None):
    antes = copy.deepcopy(e) if antes is None else antes
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[{EXT}, {HOY}, ahold_f4] {nota} · Comprobación anterior (ahold_f3): {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}",
                         "vinculo": None}
    e["incidencia"] = None
    cambios.append({"celda": e["celda"], "antes": antes, "despues": copy.deepcopy(e)})


# ---------- texto/ del 3T: cada cifra se lee en su página
Q3 = "texto/AD_q3-2026-interim-report.txt"
SHA_Q3 = h(os.path.join(C, Q3))
assert SHA_Q3 == "2b3df57bb77e9d359d27b6ab9f44b8421ebc305fde3b9add0cce33c66f178e88"
TXT = open(os.path.join(C, Q3), encoding="utf-8").read()


def pagina(n):
    return re.search(r"\[PDF PAGE %d\]\n(.*?)(?=\n\[PDF PAGE |\Z)" % n, TXT, re.S).group(1)


def linea(n, etq):
    L = [l for l in pagina(n).split("\n") if l.strip().startswith(etq)]
    assert L, (n, etq)
    return re.sub(r"\s+", " ", L[0].strip())


def cifras(l):
    return [(-1 if x.startswith("(") else 1) * int(x.strip("()").replace(",", "")) for x in re.findall(r"\(?\d[\d,]*\)?", l)]


DOC_Q3 = "Interim report Q3 2026 de Koninklijke Ahold Delhaize N.V. (informe interino oficial, 4-nov-2026)"
VER_Q3 = ("PDF oficial «pdf/AD_q3-2026-interim-report.pdf», sha256 39268b160a31c09d8fb1ae02efd9fef369e7ac64d310c5967bcefae420c64882 (pdf_DESCARGAS_2026.tsv: "
          "https://media.aholddelhaize.com/media/voehurnq/ahold-delhaize-q3-2026-interim-report.pdf, 2026-11-17); texto con marcas [PDF PAGE n]: "
          f"«{Q3}», sha256 {SHA_Q3}")
assert E["Análisis!C55"]["fuente"]["version"] == VER_Q3
UBIC = {12: "cuenta de resultados consolidada del informe interino", 14: "balance consolidado del informe interino",
        16: "estado consolidado de flujos de caja del informe interino", 24: "nota 12 Alternative performance measures (cuadro Net debt)"}


def fuente_q3(pag, etq, pos, concepto, columna, periodo, tratamiento="cifra publicada con su signo propio (los pagos figuran entre paréntesis); signo 1, sin transformación"):
    l = linea(pag, etq)
    v = cifras(l)[pos]
    return {"documento": DOC_Q3, "version": VER_Q3, "archivo": Q3, "sha256": SHA_Q3, "pagina": pag, "folio": pag, "ubicacion": UBIC[pag], "concepto": concepto,
            "columna": columna, "periodo": periodo, "unidad": "millones de euros", "escala": 1, "signo": 1, "tratamiento": tratamiento, "perimetro": "consolidado",
            "reexpresado": "no aplica (informe interino 2026; columnas del periodo publicado)", "valor_fuente": v, "cita": l}


COL = {-2: ("Q3 YTD 2026 (39 semanas cerradas el 27-sep-2026; tercera columna)", "39 semanas cerradas el 27-sep-2026"),
       -1: ("Q3 YTD 2025 (39 semanas cerradas el 28-sep-2025; cuarta columna, comparativa)", "39 semanas cerradas el 28-sep-2025")}
NUEVOS = {}   # clave → (página, etiqueta, posición, concepto)
for k, pag, etq, conc in (("cfo", 16, "Net cash from operating activities", "flujo neto de las actividades de explotación"),
                          ("capex", 16, "Purchase of non-current assets", "compra de activos no corrientes (capex bruto en caja)"),
                          ("intpaid", 16, "Interest paid", "intereses pagados (financiación)"),
                          ("lease", 16, "Repayment of lease liabilities", "pagos de pasivos por arrendamiento (principal + intereses, una sola línea)"),
                          ("dividends_jv", 16, "Dividends received from joint ventures", "dividendos cobrados de negocios conjuntos (inversión)"),
                          ("interest_dividend_received", 16, "Interest and dividend received",
                           "intereses y dividendos cobrados (inversión); la misma línea que el informe anual y el 2T rotulan «Interest received» (1S 2026 50 + 3T 39 = 89; 1S 2025 76 + 3T 15 = 91)"),
                          ("lease_receivables", 16, "Lease payments received on lease receivables", "cobros de arrendamientos financieros a cobrar (subarriendos; inversión)"),
                          ("operating_income", 12, "Operating income", "resultado operativo (IFRS)"),
                          ("da_impairments", 16, "Depreciation, amortization and impairments", "amortizaciones y deterioros (ajuste del estado de flujos)")):
    for pos, suf in ((-2, "ytd2026"), (-1, "ytd2025")):
        NUEVOS[f"aux:Q3-2026_p{pag}_{k}_{suf}"] = fuente_q3(pag, etq, pos, conc + f", {COL[pos][1]}", COL[pos][0], COL[pos][1])
SEP = ("September 27, 2026 (primera columna del balance)", "saldo a 27-sep-2026")
NUEVOS["aux:Q3-2026_p14_investments_jv_sep2026"] = fuente_q3(14, "Investments in joint ventures and associates", 0, "inversiones en negocios conjuntos y asociadas", *SEP, tratamiento="cifra tal como se publica")
NUEVOS["aux:Q3-2026_p14_equity_sep2026"] = fuente_q3(14, "Equity attributable to common shareholders", -2, "patrimonio atribuible a los accionistas comunes (nota 7; sin minoritarios)", *SEP, tratamiento="cifra tal como se publica")
ESPERADO = {"cfo_ytd2026": 4030, "cfo_ytd2025": 4288, "capex_ytd2026": -1898, "capex_ytd2025": -1805, "intpaid_ytd2026": -196, "intpaid_ytd2025": -192,
            "lease_ytd2026": -1473, "lease_ytd2025": -1461, "dividends_jv_ytd2026": 22, "dividends_jv_ytd2025": 28, "interest_dividend_received_ytd2026": 89,
            "interest_dividend_received_ytd2025": 91, "lease_receivables_ytd2026": 113, "lease_receivables_ytd2025": 104, "operating_income_ytd2026": 2736,
            "operating_income_ytd2025": 2643, "da_impairments_ytd2026": 2739, "da_impairments_ytd2025": 2773, "investments_jv_sep2026": 254, "equity_sep2026": 14375}
for k, f in NUEVOS.items():
    clave = re.sub(r"^aux:Q3-2026_p\d+_", "", k)
    assert f["valor_fuente"] == ESPERADO[clave], (k, f["valor_fuente"])
    e = {"celda": k, "id": "aux", "ambito": None, "uso": None, "material": True, "clase": "dato_publicado", "valor_modelo": f["valor_fuente"], "fuente": f,
         "derivacion": None, "hipotesis": None, "justificacion": None,
         "comprobacion": {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                          "nota": f"[{EXT}, {HOY}, ahold_f4] auxiliar nuevo del 3T 2026 ({DEC}); cita leída en la página {f['pagina']} de {Q3}", "vinculo": None},
         "incidencia": None}
    assert k not in E
    d["entradas"].append(e)
    E[k] = e
    cambios.append({"celda": k, "antes": None, "despues": copy.deepcopy(e)})
o = lambda k: f'o["{k}"]'  # noqa: E731
A = lambda k, s: f"aux:Q3-2026_p{16 if k not in ('operating_income',) else 12}_{k}_{s}"  # noqa: E731


def ltm(fy, k):
    return f'{o(fy)} + {o(A(k, "ytd2026"))} - {o(A(k, "ytd2025"))}'


EBIT_LTM = ltm("Historia!L7", "operating_income")
DA_LTM = ltm("Historia!L8", "da_impairments")
assert (E["Historia!L7"]["valor_modelo"], E["Historia!L8"]["valor_modelo"]) == (3542, 3733)
# ---------- C53 y C54 (datos publicados)
for celda, pag, etq, pos, conc, v_ant, v in (("Análisis!C53", 14, "Cash and cash equivalents", -2, "efectivo y equivalentes de efectivo (nota 8)", 3196, 3559),
                                             ("Análisis!C54", 24, "Gross debt", 0, "deuda bruta (gross debt): loans + lease liabilities + porción corriente de deuda y arrendamientos", 19261, 19747)):
    e = E[celda]
    assert e["valor_modelo"] == v_ant
    antes = copy.deepcopy(e)
    f = fuente_q3(pag, etq, pos, conc, "September 27, 2026 (primera columna)", "saldo a 27-sep-2026 (informe interino Q3 2026)", tratamiento="cifra tal como se publica")
    assert f["valor_fuente"] == v, (celda, f["valor_fuente"])
    f["tratamiento"] = ("cifra tal como se publica. Z-ACC (19-nov-2026): el balance a 27-sep-2026 ya descuenta las recompras de 2026 (864, Q3-26 PDF p. 16) y C55 "
                        "sigue con las acciones a 28-dic-2025 (P-O2 a): desalineación de fechas declarada")
    e["fuente"], e["valor_modelo"] = f, v
    pendiente(e, f"{DEC}: saldo del 3T (27-sep-2026) en lugar del 2T ({v_ant}); configuracion/cambio_ahold_f4.json", antes)
# ---------- derivados
C41 = E["Análisis!C41"]["valor_modelo"]
assert abs(C41 - 31971.92518695) < 1e-9


def derivado(celda, valor, origenes, formula, conciliacion, unidad, v_ant, nota):
    e = E[celda]
    assert abs(e["valor_modelo"] - v_ant) < 1e-9, (celda, e["valor_modelo"])
    antes = copy.deepcopy(e)
    e["valor_modelo"] = valor
    e["derivacion"] = {"origenes": origenes, "formula": formula, "conciliacion": conciliacion, "unidad": unidad}
    pendiente(e, nota, antes)


derivado("Análisis!C24", 0.107,
         ["Historia!L7", A("operating_income", "ytd2026"), A("operating_income", "ytd2025"), "aux:Q3-2026_p14_equity_sep2026", "Análisis!C54"],
         f'round(({EBIT_LTM}) / ({o("aux:Q3-2026_p14_equity_sep2026")} + {o("Análisis!C54")}), 3)',
         ("ROCE antes de impuestos IFRS con fondo de comercio, LTM a 27-sep-2026 (definición de la decisión del inversor del 28-oct-2026, Control maestro fila 29, M; "
          f"periodo de la {DEC}): resultado operativo LTM = 3.542 (2025, AR2025 PDF p. 212) + 2.736 − 2.643 (39 semanas de 2026 y de 2025, Q3-26 PDF p. 12) = 3.635 ÷ "
          "capital empleado a 27-sep-2026, la fecha del fin de los doce meses (y la de C53 y C54) = patrimonio atribuible 14.375 (Q3-26 PDF p. 14) + deuda bruta con "
          "arrendamientos 19.747 (C54, Q3-26 PDF p. 24) = 34.122 → 0,106530 → round(…, 3) = 0,107 = libro (redondeo de la etapa 1, declarado en la fórmula). Misma "
          "definición del denominador que en ahold_f3 (patrimonio + deuda + arrendamientos: a 28-dic-2025, 14.195 + 18.404 de deuda bruta, Q3-26 p. 24). Sensibilidad: "
          "con el capital a 28-dic-2025, 0,112; con la media 28-dic-2025/27-sep-2026, 0,109; neto de caja, 0,119."), None, 0.109,
         f"{DEC}: LTM al 3T con el denominador a 27-sep-2026, fecha documentada y coherente (resuelve la discrepancia del sellado: la fecha del denominador no estaba documentada)")
derivado("Análisis!C33", 2.2073,
         ["Análisis!C54", "Análisis!C53", "Historia!L7", A("operating_income", "ytd2026"), A("operating_income", "ytd2025"), "Historia!L8", A("da_impairments", "ytd2026"), A("da_impairments", "ytd2025")],
         f'round(({o("Análisis!C54")} - {o("Análisis!C53")}) / ({EBIT_LTM} + {DA_LTM}), 4)',
         ("Definición de la etapa 1 (Control maestro fila 36): (deuda bruta con arrendamientos − caja) ÷ EBITDA NIIF 16 con deterioros, LTM. Con el 3T (" + DEC + "): "
          "deuda bruta 19.747 (C54, Q3-26 PDF p. 24) − caja 3.559 (C53, Q3-26 p. 14) = 16.188 ÷ EBITDA LTM a 27-sep-2026: resultado operativo 3.542 (L7) + 2.736 − 2.643 "
          "(Q3-26 p. 12) = 3.635; amortizaciones y deterioros 3.733 (L8, flujos 2025) + 2.739 − 2.773 (Q3-26 p. 16) = 3.699; EBITDA 7.334. 16.188 ÷ 7.334 = 2,207254… → "
          "round(…, 4) = 2,2073 = libro. No usa acciones (Z-ACC no le afecta)."), None, 2.2153, f"{DEC}: deuda, caja y EBITDA LTM del 3T")
C40_OR = []
partes = []
for k, fy in (("cfo", "aux:AR2025_p216_cfo_fy2025"), ("capex", "aux:AR2025_p216_capex_fy2025"), ("intpaid", "aux:AR2025_p216_intpaid_fy2025"),
              ("lease", "aux:AR2025_p216_lease_fy2025"), ("dividends_jv", "aux:AD_annual-report-2025_p216_dividends_received_from_joint_ventures_2025"),
              ("interest_dividend_received", "aux:AD_annual-report-2025_p216_interest_received_2025"),
              ("lease_receivables", "aux:AD_annual-report-2025_p216_lease_payments_received_on_lease_receivables_2025")):
    assert fy in E, fy
    C40_OR += [A(k, "ytd2026"), fy, A(k, "ytd2025")]
    partes.append(f'{o(A(k, "ytd2026"))} + {o(fy)} - {o(A(k, "ytd2025"))}')
derivado("Análisis!C40", 2150, C40_OR, " + ".join(partes),
         ("FCF LTM a 27-sep-2026 con la regla espejo (P-O1 c), misma definición que la caja base (" + DEC + "): 39 semanas de 2026 + 2025 − 39 semanas de 2025 de cada "
          "partida (Q3-26 PDF p. 16; AR2025 PDF p. 216): CFO 4.030 + 6.989 − 4.288 = 6.731; capex −1.898 − 2.564 + 1.805 = −2.657; intereses pagados −196 − 261 + 192 = −265; "
          "pagos de arrendamientos −1.473 − 1.944 + 1.461 = −1.956; dividendos de negocios conjuntos 22 + 28 − 28 = 22; intereses (y dividendos) cobrados 89 + 130 − 91 = 128; "
          "cobros de subarriendos 113 + 138 − 104 = 147 → 2.150 = libro. Los gastos van con su signo publicado (negativos), los cobros en positivo. El 3T rotula «Interest and "
          "dividend received» la línea que el informe anual llama «Interest received» (misma serie: 1S 50 + 3T 39 = 89). Z-ACC: FCF yield con C41 (acciones a 28-dic-2025) "
          "6,72 %; con las acciones a 27-sep-2026, 6,89 % (desalineación declarada)."), "millones de euros", 2096, f"{DEC}: FCF LTM al 3T (antes 2.096, LTM al 2T)")
derivado("Análisis!C42", 47905.92518695 / 7334,
         ["Análisis!C41", "Análisis!C54", "Análisis!C53", "aux:Q3-2026_p14_investments_jv_sep2026", "Historia!L7", A("operating_income", "ytd2026"), A("operating_income", "ytd2025"),
          "Historia!L8", A("da_impairments", "ytd2026"), A("da_impairments", "ytd2025")],
         f'({o("Análisis!C41")} + {o("Análisis!C54")} - {o("Análisis!C53")} - {o("aux:Q3-2026_p14_investments_jv_sep2026")}) / ({EBIT_LTM} + {DA_LTM})',
         ("EV ÷ EBITDA LTM = (C41 31.971,925 + deuda bruta C54 19.747 − caja C53 3.559 − negocios conjuntos 254, Q3-26 PDF p. 14) ÷ (3.542 + 2.736 − 2.643 + 3.733 + 2.739 − "
          "2.773 = 7.334) = 47.905,925 ÷ 7.334 = 6,532032 (" + DEC + "; misma definición que C33). Z-ACC: C41 usa las acciones a 28-dic-2025 (P-O2 a) y el balance es a "
          "27-sep-2026, después de 864 de recompras: con las 865,173863 M acciones a 27-sep-2026 (Q3-26 PDF p. 21) saldría 6,425350 (desalineación declarada)."), "x",
         6.590309595552951, f"{DEC}: EV con el balance del 3T y EBITDA LTM al 3T (resuelve la vigencia que declaraba la incidencia)")
# ---------- auxiliares del 2T sin uso
usados = {str(x) for e in d["entradas"] for x in ((e.get("derivacion") or {}).get("origenes") or [])}
for k in [k for k in E if k.startswith("aux:Q2-2026_")]:
    assert k not in usados, k
    cambios.append({"celda": k, "antes": copy.deepcopy(E[k]), "despues": None, "motivo": "auxiliar del 2T sin uso: C24, C33, C40 y C42 se derivan del 3T (A-Q3)"})
    d["entradas"] = [x for x in d["entradas"] if x["celda"] != k]
    del E[k]
# ---------- C31 y C34 (convenciones con valor)
for celda, fund in (("Análisis!C31", (
        "Etiqueta de juicio de la etapa 1 («Sí», decisión del inversor del 28-oct-2026: lectura literal de «cobros o inventario»), comprobada con el 3T 2026 (" + DEC + "): el 3T no "
        "publica el balance de sep-2025, así que se usan las variaciones del estado de flujos (sin divisa ni adquisiciones), 2025 + 39 semanas de 2026 − 39 semanas de 2025 "
        "(AR2025 PDF p. 216; Q3-26 PDF p. 16): cobros y otros activos corrientes −91 + 83 − 128 = −136 (aumentan 136, ≈ +4,7 %), inventario −158 − 42 + 258 = +58 (bajan 58, "
        "≈ −1,2 %), frente a ventas +1,9 % a tipo constante en 39 semanas (Q3-26 PDF p. 3): literal «Sí», económica (inventario) «No». Aproximación declarada (la línea de cobros "
        "incluye otros activos corrientes). La etiqueta no es una cifra de fuente.")),
        ("Análisis!C34", (
        "Etiqueta de juicio de la etapa 1 («No», decisión del inversor del 28-oct-2026: deuda a corto con los arrendamientos corrientes), comprobada con el 3T 2026 (" + DEC + "): "
        "caja 3.559 (Q3-26 PDF p. 14) ÷ préstamos a corto y porción corriente de deuda y arrendamientos 4.321 (Q3-26 PDF p. 24) = 0,82x → «No» (0,87x con el 2T). Sin el cash "
        "pool nocional de 1.176 en los dos lados (p. 21 y 24): 0,76x. Sin los arrendamientos corrientes (no publicados en el 3T; 1.448 a 28-dic-2025, estimación) ≈ 1,2x, "
        "lectura que la decisión descartó. La etiqueta no es una cifra de fuente."))):
    e = E[celda]
    antes = copy.deepcopy(e)
    e["hipotesis"]["fundamento"] = fund
    e["hipotesis"]["procedencia"] = "Control maestro del libro (fila de la celda, G:N reescritas en ahold_f4 con el 3T; M = decisión del inversor del 28-oct-2026, conservada) y datos_v63.md"
    pendiente(e, f"fundamento comprobado con el 3T ({DEC}); valor sin cambio", antes)
# ---------- A-NIC17
for celda, anio, nic in (("Historia!C22", 2016, "1.761 + 199"), ("Historia!D22", 2017, "1.430 + 177")):
    e = E[celda]
    antes = copy.deepcopy(e)
    e["derivacion"]["conciliacion"] += (f" · Decisión A-NIC17 de la persona responsable (19-nov-2026, DECISIONES_PARA_EL_USUARIO.md, «19-nov-2026 (mañana)»: «dejarla»): la deuda "
                                        f"{anio} se deja como se publicó, con los arrendamientos financieros NIC 17 ({nic}), aunque la fila 22 del libro se rotule «sin arrendamientos»: "
                                        "antes de la NIIF 16 no hay pasivo por arrendamientos separado y no hay doble cuenta (Historia C23/D23 = 0, no_aplicable, AR2025 PDF p. 65). "
                                        "Declarado aquí y en fase1_metadatos.json (_notas, ahold_f4).")
    pendiente(e, "A-NIC17: inclusión de los arrendamientos financieros NIC 17 declarada (decisión de la persona responsable); deja de ser discrepancia si el revisor la acepta como declarada", antes)
# ---------- G26, H26, K26: campo «columna»
for celda, col in (("Historia!G26", "2020 (segunda columna, comparativa: 53 semanas cerradas el 3-ene-2021, de la cuenta de resultados del informe 2021)"),
                   ("Historia!H26", "2021 (segunda columna, comparativa: 52 semanas cerradas el 2-ene-2022, de la cuenta de resultados del informe 2022)"),
                   ("Historia!K26", "2024 (segunda columna, comparativa: 52 semanas cerradas el 29-dic-2024, de la cuenta de resultados del informe 2025)")):
    e = E[celda]
    antes = copy.deepcopy(e)
    assert "columna del ejercicio corriente" in e["fuente"]["columna"]
    e["fuente"]["columna"] = col
    pendiente(e, "campo «columna» corregido al comparativo del informe N+1 (REVISION_SELLADO.md, segunda pasada: discrepancia formal)", antes)
# ---------- C57 y Palancas!C7 (fuentes de mercado nuevas)
FM = os.path.join(C, "fuentes_mercado")
bb = "fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt"
e = E["Análisis!C57"]
antes = copy.deepcopy(e)
assert e["valor_modelo"] == 0.0334
e["valor_modelo"] = 0.0337
e["fuente"] = {
    "documento": "Deutsche Bundesbank, serie diaria BBSSY.D.REN.EUR.A630.000000WT1010.A «Daily yield of the current 10 year federal bond» (Bund a 10 años de referencia)",
    "version": ("CSV oficial subido por la persona responsable a la Release fuentes-examen-20261118 de jluisplagos/munger-v2-evidencias-mistral (asset 766892543, "
                "bund_10y_WT1010.csv; última actualización de la serie 2026-11-18 12:31:26), descarga cruda conservada byte a byte en "
                "fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv, sha256 fef9498ea765b89547cebb222ab8720e91c84113c8caca74a676e21e5e571967 (la huella "
                "publicada); conservada como texto con marca [PDF PAGE 1] y separador de espacio en las filas de datos, sha256 " + h(os.path.join(C, bb))),
    "archivo": bb, "sha256": h(os.path.join(C, bb)), "pagina": 1, "folio": None,
    "ubicacion": "tabla de la serie diaria (cabecera con la definición de la serie), fila del 2026-11-13",
    "concepto": "rendimiento del Bund a 10 años de referencia, en % diario",
    "columna": "2026-11-13 (fecha del precio, C37 y Palancas!C45)", "periodo": "2026-11-13", "unidad": "percent", "escala": 0.01, "signo": 1,
    "tratamiento": ("rendimiento diario publicado en %; escala 0,01 lo pasa a proporción (3,37 % = 0,0337). Misma fecha que el precio (13-nov-2026). Sustituye la lectura de "
                    "Trading Economics de los metadatos (3,34 %, «cierre de octubre», sin fuente conservada) y la fila del 2026-11-17 de la serie UMU 9–10 años (3,34 %) que "
                    "citaba el registro de ahold_f3; la serie UMU da 3,36 % el 13-nov (fuentes_mercado/, conservada)"),
    "perimetro": "no aplica: dato de mercado (bono soberano alemán de referencia en EUR)",
    "perimetro_justificacion": "la tasa sin riesgo es un dato de mercado del bono de referencia en EUR; el perímetro contable no se aplica",
    "reexpresado": "no aplica", "valor_fuente": 3.37, "cita": "2026-11-13 3.37"}
pendiente(e, "C57 = 0,0337 con el CSV oficial de la Bundesbank (WT1010, 13-nov-2026), por encargo del coordinador del 19-nov-2026; resultados/fuentes_mercado_ahold_f4.json", antes)
dm = "fuentes_mercado/Damodaran_margin_industry_averages_2026-01.txt"
e = E["Palancas!C7"]
antes = copy.deepcopy(e)
assert e["valor_modelo"] == "Retail (Grocery and Food)"
f = e["fuente"]
for k in ("conservacion", "lectura_externa"):
    f.pop(k, None)
f.update({
    "documento": "Damodaran (NYU Stern), «Margins by industry» (margin.xls), hoja «Industry Averages», empresas de EE. UU., «Date updated» 2026-01-05",
    "version": ("XLS subido por la persona responsable a la Release fuentes-examen-20261118 de jluisplagos/munger-v2-evidencias-mistral (asset 766892761, damodaran_margin.xls), "
                "descarga cruda conservada byte a byte en fuentes_mercado/Damodaran_margin_2026-01.xls, sha256 25b04fce9740d9a471d50e176bf55aa6b7608cd0621b00072508a20e7c35ed7a "
                "(la huella publicada); hoja «Industry Averages» conservada como texto con marca [PDF PAGE 1], una línea por fila («fila n: celda | celda …», xlrd 2.0.1), "
                "sha256 " + h(os.path.join(C, dm))),
    "archivo": dm, "sha256": h(os.path.join(C, dm)), "pagina": 1, "folio": None,
    "ubicacion": "hoja «Industry Averages», fila 83 (columna A «Industry Name»)", "columna": "Industry Name (columna A), fila 83 de la hoja",
    "periodo": "clasificación de los datos de enero de 2026 («Date updated» 2026-01-05)",
    "tratamiento": "etiqueta de industria tal como figura en la tabla (15 empresas en esa fila); la tabla es de empresas de EE. UU. (celda F3 «US companies»)",
    "cita": "fila 83: Retail (Grocery and Food) | 15"})
pendiente(e, "lectura externa → fuente local: tabla de Damodaran de la Release (fila 83), por encargo del coordinador del 19-nov-2026; resultados/fuentes_mercado_ahold_f4.json", antes)
# ---------- cabecera del registro
fmc = d.get("fuentes_mercado") or {}
fmc.setdefault("contenido", {})
for n, que in (("Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.csv", "CSV oficial de la Bundesbank, serie WT1010 (Bund a 10 años de referencia), descarga cruda (Release fuentes-examen-20261118, asset 766892543)"),
               ("Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt", "la misma serie como texto con marca [PDF PAGE 1]; fila usada por C57: 2026-11-13 3.37"),
               ("Damodaran_margin_2026-01.xls", "XLS de Damodaran «Margins by industry», descarga cruda (Release fuentes-examen-20261118, asset 766892761)"),
               ("Damodaran_margin_industry_averages_2026-01.txt", "hoja «Industry Averages» como texto con marca [PDF PAGE 1]; fila usada por Palancas!C7: fila 83")):
    fmc["contenido"][n] = {"que": que, "sha256": h(os.path.join(FM, n))}
d["fuentes_mercado"] = fmc
d["nota_de_la_orquestacion"] = str(d.get("nota_de_la_orquestacion") or "") + (
    f" (ahold_f4, {HOY}) Registro conservado de ahold_f3 por cambiar_base.py; {EXT} cambió {len(cambios)} entradas (resultados/registro_cambios_ahold_f4.json): A-Q3 (C24, C33, "
    "C40, C42, C53, C54 con el 3T; auxiliares del 2T sin uso retirados y del 3T añadidos; C31 y C34 comprobadas), A-NIC17 (C22, D22), columna de G26/H26/K26, C57 "
    "(Bundesbank WT1010) y Palancas!C7 (Damodaran, fuente local). Quedan pendientes de otro revisor.")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": os.path.abspath(__file__), "registro_antes_sha256": h(os.path.join(ANT, "verificacion_entradas_conservado_de_ahold_f3.json")),
           "registro_despues_sha256": h(p), "entradas_cambiadas": [x["celda"] for x in cambios], "cambios": cambios}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("cambiadas", len(cambios))
