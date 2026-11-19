#!/usr/bin/env python3
"""zoetis_t2 · genera configuracion/cambio_zoetis_t2.json desde zoetis_t1d (que no se toca), por encargo del coordinador (19-nov-2026): segundo
tiempo de Zoetis, «el mismo expediente más el trimestre del 5-nov-2026». Fecha de análisis 5-nov-2026 (cierre del día de la publicación del T3).
Reutiliza literalmente lo vigente de zoetis_t1d (cambio_zoetis_t1d.json, fase1_metadatos.json) y cambia solo lo que trae el tercer trimestre:
LTM y balance a 30-sep-2026 (C24, C32, C33, C40, C42, C53, C54), precio y Treasury del 5-nov-2026 (C37, C57, C41) y la evidencia de C31, C34,
D4, C25, C27 y C76. Cada componente sale de texto/ (cifras_t3.py lo comprueba en su línea y página). Extractor: Claude orquestación.
Uso: python3 -I generar_cambio_zoetis_t2.py RAIZ_munger_v2_r1 DIR_TEXTO SALIDA.json
  DIR_TEXTO: carpeta con zoetis-10k-fy2025.txt (el de zoetis_t1d) y los textos del T3 hechos como los hará cambiar_base.py (pdftotext -layout con
  marcas [PDF PAGE n]) y html_a_texto.py; tras preparar, corregir_registro_zoetis_t2.py vuelve a comprobarlo todo en zoetis_t2/Zoetis/texto/."""
import copy, json, os, sys
from fractions import Fraction as F
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cifras_t3 as CT  # noqa: E402

RAIZ, DIRTX, SAL = sys.argv[1:4]
EX = "personaje_v2/empresas_v2_correcciones/2026-11_examen_universo"
T1D = os.path.join(RAIZ, EX, "zoetis_t1d")
T2 = os.path.join(RAIZ, EX, "zoetis_t2")
meta = json.load(open(os.path.join(T1D, "Zoetis", "fase1_metadatos.json"), encoding="utf-8"))
c1d = json.load(open(os.path.join(RAIZ, EX, "configuracion", "cambio_zoetis_t1d.json"), encoding="utf-8"))
tx = CT.Textos(DIRTX)
v, d = CT.calcular(tx)
assert tx.sha(CT.K25) == "4159130b8f53d35cb18c0617b2ac8f0e6405b1e5a808ce9014e6a6f0566a503a"
SHA_PDF = {"zoetis-10q-2026-q3.pdf": "f797be282a86905e29ea3d41573fba5a645f2db674fc7c0f26fb93c0f71242bf",
           "zoetis-3q2026-financial-results.pdf": "bac00765798eb16967fc509b4f1b8c1011d05664249b70d22737f9bc6135e05d",
           "zoetis-3q2026-press-release.html": "fe2c88a8d6e3b4cf14b2edfb75eb63a39244d9d20109ae32a97493db77aaeb77"}
import hashlib  # noqa: E402
for n, s in SHA_PDF.items():
    assert hashlib.sha256(open(os.path.join(T2, "fuentes_release", n), "rb").read()).hexdigest() == s, n


def es(x, dec=None):
    """Número en formato español (miles con punto, decimales con coma)."""
    if dec is None:
        s = f"{x:,}" if isinstance(x, int) else f"{x:,}"
    else:
        s = f"{x:,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


def pct(x, dec=1):
    return es(float(x) * 100, dec) + " %"


# --- mercado
PRECIO = F("82.11")
ACC = F("424.927535")
CAP = PRECIO * ACC
assert CAP == F("34890.79989885")
ACC_SEP, ACC_OCT = F("407.487227"), F("406.316147")
tx.frase(CT.Q3, 5, "424,927,535 shares outstanding at September 30, 2026, and December 31, 2025, respectively")
tx.frase(CT.Q3, 5, "407,487,227 and")
tx.frase(CT.Q3, 1, "As of October 30, 2026, there were 406,316,147 shares of common stock outstanding.")
EBITDA, ND = d["ebitda_ltm"], d["deuda_neta"]
C42 = (CAP + ND) / EBITDA
C42_SEP = (PRECIO * ACC_SEP + ND) / EBITDA
C42_REC = (CAP + ND) / d["ebitda_ltm_recast"]
assert f"{float(C42):.6f}" == "11.109987"
ZACC = ("DESALINEACIÓN DE FECHAS declarada (decisión Z-ACC de la persona responsable, 19-nov-2026: se mantienen las acciones al cierre del ejercicio, "
        "P-O2): precio del 5-nov-2026 × 424.927.535 acciones en circulación al 31-dic-2025 (10-K 2025 PDF p. 68), deuda y caja del balance del "
        "30-sep-2026 y EBITDA de los 12 meses a 30-sep-2026; con las 407.487.227 acciones del 30-sep-2026 (10-Q T3 2026 PDF p. 5) saldría "
        + es(float(C42_SEP), 2) + "x, y con las 406.316.147 de la portada del 10-Q T3 (30-oct-2026, PDF p. 1) "
        + es(float((PRECIO * ACC_OCT + ND) / EBITDA), 2) + "x.")
FYA = ("APROXIMACIÓN por la «Fiscal Year Alignment» (nota 2 del 10-Q T3 2026, PDF p. 10–11: desde el 1-ene-2026 las filiales no estadounidenses dejaron "
       "de declarar con un mes de desfase; el 9M-2025 del 10-Q está reexpresado y el 10-K 2025 todavía no): LTM al 30-sep-2026 = 2025 (10-K, base "
       "antigua) − 9M-2025 + 9M-2026 (10-Q T3 2026); la nota 2 da el 9M-2025 «As previously reported» para el BAI (2.599), los impuestos (529), el "
       "beneficio neto (2.070) y el CFO (2.011), que se usan, pero solo reexpresado para intereses (165), D&A (365), capex (462) y arrendamientos "
       "financieros (2): esas cuatro mezclan bases.")
CLASE = ("[Clase: convención · aproximación declarada (no es un derivado exacto: en el registro de entradas es «convencion» con su justificacion_clase, "
         "como en zoetis_t1d)]")
T2N = "(zoetis_t2, segundo tiempo, Claude orquestación, 19-nov-2026)"
EBITDA_TXT = (f"BAI (3.360 − 2.599 + 2.353 = {es(int(d['bai_ltm']))}) + gasto por intereses (222 − 165 + 185 = {es(int(d['int_ltm']))}) + D&A "
              f"(487 − 365 + 357 = {es(int(d['da_ltm']))}) = {es(int(EBITDA))} (EBIT = BAI + intereses = {es(int(d['ebit_ltm']))})")
PAG_EBITDA = "10-K 2025 PDF p. 66 y 70; 10-Q T3 2026 PDF p. 3, 5, 8 y 10"
K_T3 = "Release fuentes-examen-20261118 (zoetis-10q-2026-q3.pdf, sha256 f797be28…42bf); texto/zoetis-10q-2026-q3.txt"
analisis = {}


def entrada(c, valor, fuente, pagina, periodo, unidad, naturaleza, fecha, derivacion, G, I, J, N, H=None):
    ev = {"G": G, "I": I, "J": J, "K": K_T3, "L": pagina, "M": fuente, "N": N}
    if H:
        ev["H"] = H
    analisis[c] = {"valor": (int(valor) if valor.denominator == 1 else float(valor)) if isinstance(valor, F) else valor, "fuente": fuente, "pagina": pagina, "periodo": periodo, "unidad": unidad,
                   "vaciar_en_etapa1": True, "naturaleza": naturaleza, "fecha": fecha, "derivacion": derivacion, "evidencia": ev}


APROX = "aproximación declarada por la «Fiscal Year Alignment» (convención de la orquestación; no derivado exacto)"
# C33
m33 = (f"Deuda neta ÷ EBITDA LTM = (deuda 750 + 8.299 = 9.049 − caja 1.333, 10-Q T3 2026 p. 5) ÷ EBITDA LTM a 30-sep-2026 = {EBITDA_TXT} = "
       f"{es(int(ND))} ÷ {es(int(EBITDA))} = {es(float(d['C33']), 6)}")
entrada("C33", d["C33"], m33, PAG_EBITDA, "deuda neta a 30-sep-2026; EBITDA LTM a 30-sep-2026", "x", APROX, "2026-09-30",
        "LTM = 2025 (10-K, base antigua) − 9M-2025 + 9M-2026 (10-Q T3 2026)",
        "Deuda neta a 30-sep-2026 · EBITDA LTM a 30-sep-2026", "10-Q 3T26 y 10-K 2025 (primaria) · cálculo derivado (aproximación declarada)",
        "Zoetis 10-Q 3T26 (balance p. 5, resultados p. 3, flujos p. 8, nota 2 p. 10); Zoetis · Informe anual 2025 (10-K FY2025, p. 66 y 70)",
        f"{CLASE} {T2N} Recalculado con el 10-Q del T3 2026 (el valor del primer tiempo, con el 2T, está en la tabla de vigencia del extracto y en antecedentes/evidencia_anterior.json). {FYA} Con el 9M-2025 "
        f"todo reexpresado (BAI 2.571) sale {es(float(d['C33_recast']), 2)}x. La deuda incluye ahora la porción corriente (750: el bono del 3,000 % "
        f"vence el 12-sep-2027, 10-Q T3 PDF p. 44); sin arrendamientos (el 10-Q no los desglosa en el balance). Covenant: deuda neta consolidada ÷ "
        f"EBITDA ≤ 3,50 a 1, cumplido a 30-sep-2026 (10-Q T3 PDF p. 42; la empresa no publica su propio cálculo). Sin acciones ni precio: no le afecta "
        f"la desalineación de C41 y C42.")
# C40
m40 = (f"FCF LTM a 30-sep-2026 = CFO (2.904 − 2.011 «as previously reported» + 1.880 = {es(int(d['cfo_ltm']))}) − capex (621 − 462 + 334 = "
       f"{es(int(d['capex_ltm']))}) − intereses fuera del CFO 0 (US GAAP) − principal de arrendamientos financieros (2 − 2 + 1 = {es(int(d['fl_ltm']))}; "
       f"10-Q T3 p. 8) = {es(int(d['fcf_ltm']))}")
entrada("C40", d["fcf_ltm"], m40, "10-K 2025 PDF p. 70 y 89; 10-Q T3 2026 PDF p. 8 y 11", "12 meses a 30-sep-2026", "mm", APROX, "2026-09-30",
        "LTM = 2025 (10-K, base antigua) − 9M-2025 + 9M-2026 (10-Q T3 2026)", "LTM a 30-sep-2026", "10-K 2025 y 10-Q 3T26 (primaria) · cálculo derivado (aproximación declarada)",
        "Zoetis 10-Q 3T26 (flujos p. 8, nota 2 p. 11); Zoetis · Informe anual 2025 (10-K FY2025, p. 70 y 89)",
        f"{CLASE} {T2N} Recalculado con el 10-Q del T3 2026 (el valor del primer tiempo, con el 2T, está en la tabla de vigencia del extracto y en antecedentes/evidencia_anterior.json). {FYA} Todo reexpresado (CFO 9M-2025 2.056) "
        f"sale {es(int(d['fcf_ltm_recast']))}. P-O1 (c) no cambia nada con US GAAP (cobros dentro del CFO). Sin acciones ni precio: no le afecta la "
        f"desalineación de C41 y C42.")
# C42
m42 = (f"EV ÷ EBITDA LTM = (C41 {es(float(CAP), 8)} = 82,11 × 424,927535 (valor exacto, sin redondear las acciones) + deuda 9.049 − caja 1.333 "
       f"(10-Q T3 2026 p. 5)) ÷ EBITDA LTM a 30-sep-2026 = {EBITDA_TXT} = {es(float(CAP + ND), 8)} ÷ {es(int(EBITDA))} = {es(float(C42), 6)}")
entrada("C42", C42, m42, PAG_EBITDA + "; Análisis C41", "EV con precio del 5-nov-2026 y balance a 30-sep-2026; EBITDA LTM a 30-sep-2026", "x", APROX,
        "2026-09-30", "LTM = 2025 (10-K, base antigua) − 9M-2025 + 9M-2026 (10-Q T3 2026) ; EV con C41 = C37 × C55 exactos",
        "EV con precio 5-nov-2026 y balance 30-sep-2026 · EBITDA LTM a 30-sep-2026", "10-Q 3T26 y 10-K 2025 (primaria) · cálculo derivado (aproximación declarada)",
        "Zoetis 10-Q 3T26 (balance p. 5); Zoetis · Informe anual 2025 (10-K FY2025)",
        f"{CLASE} {T2N} Recalculado con el 10-Q del T3 2026 y el precio del 5-nov-2026 "
        f"(el valor del primer tiempo, con el 2T, está en la tabla de vigencia del extracto y en antecedentes/evidencia_anterior.json). {FYA} Con el 9M-2025 todo reexpresado (BAI 2.571) ≈ {es(float(C42_REC), 2)}x. {ZACC}")
# C24
m24 = (f"ROIC DESPUÉS de impuestos (no ROCE), con goodwill, definición de la etapa 1 (NOPAT = EBIT × (1 − tipo efectivo GAAP); capital invertido = "
       f"patrimonio + deuda financiera − caja) con el LTM a 30-sep-2026: EBIT LTM {es(int(d['ebit_ltm']))} (= BAI {es(int(d['bai_ltm']))} + intereses "
       f"{es(int(d['int_ltm']))}) × (1 − impuestos LTM 687 − 529 + 470 = {es(int(d['tax_ltm']))} ÷ BAI {es(int(d['bai_ltm']))} = {pct(d['t_ltm'], 3)}) = "
       f"NOPAT {es(float(d['nopat_ltm']), 4)} ÷ capital invertido a 30-sep-2026 (patrimonio 3.303 + deuda 9.049 − caja 1.333 = {es(int(d['capital_sep']))}) "
       f"= {es(float(d['C24']), 6)} (valor exacto del cociente, sin redondear)")
entrada("C24", d["C24"], m24, "10-K 2025 PDF p. 66; 10-Q T3 2026 PDF p. 3, 5 y 10", "NOPAT LTM a 30-sep-2026 ÷ capital invertido a 30-sep-2026", "%",
        APROX, "2026-09-30", "NOPAT LTM (2025 − 9M-2025 + 9M-2026) ÷ (patrimonio + deuda − caja) a 30-sep-2026",
        "LTM a 30-sep-2026 (capital invertido a 30-sep-2026)", "10-Q 3T26 y 10-K 2025 (primaria) · cálculo derivado (aproximación declarada)",
        "Zoetis 10-Q 3T26 (resultados p. 3, balance p. 5, nota 2 p. 10); Zoetis · Informe anual 2025 (10-K FY2025, p. 66)",
        f"{CLASE} {T2N} Sustituye al 26,6 % de la etapa 1 (doce meses al 2T 2026, con EBIT derivado 3.463 y capital medio de junio de 2025 y de 2026), que zoetis_t1d "
        f"conservaba como convención no reproducible (su fórmula y el 10-Q del T2 2025 no están en el expediente). El 10-Q del T3 no publica el balance "
        f"del 30-sep-2025, así que no hay capital medio de doce meses: se toma el capital al fin de los doce meses (la fecha de C53 y C54, como en "
        f"ahold_f4). Sensibilidades: capital medio 31-dic-2025 (reexpresado: 3.415 + 9.042 − 2.450 = 10.007, 10-Q T3 p. 5) y 30-sep-2026 → "
        f"{pct(d['C24_medio'])}; restando también las inversiones a corto (200) → {pct(d['C24_sin_sti'])}. {FYA} El LTM incluye cargos de 9M-2026 que "
        f"la empresa trata como no recurrentes: 142 de reestructuración (con 11 de deterioros) y 78 de deterioro de I+D en curso de PetMedix (10-Q T3 PDF p. 3, 15 y 39). Pasa igual con «Compounder» ≥ 15 % y con «Calidad» ≥ 12 %.",
        H="% (decimal)")
# C32
m32 = (f"Literal: goodwill 2.888 ÷ activo total 15.088 (10-Q T3 2026 p. 5, 30-sep-2026) = {es(float(d['C32']), 6)} (cociente exacto, sin redondear: "
       f"la etapa 1 guardaba el redondeo a 3 decimales)")
entrada("C32", d["C32"], m32, "10-Q T3 2026 PDF p. 5 y 20", "saldo a 30-sep-2026", "%", "derivado de datos publicados (cociente exacto)", "2026-09-30",
        "goodwill ÷ activo total a 30-sep-2026", "30-sep-2026", "10-Q 3T26 (primaria)", "Zoetis 10-Q 3T26 (balance p. 5; nota 11 de goodwill, p. 20)",
        f"{T2N} Recalculado con el balance del 30-sep-2026 (antes 0,184 = round(2.771 ÷ 15.077, 3) a 30-jun-2026). El goodwill sube 114 por la "
        f"compra de VitalRADS (107) y el tipo de cambio (7) (10-Q T3 PDF p. 20); sigue por debajo del umbral del 20 % (a 0,9 puntos). Deterioro: el 10-Q "
        f"del T3 no informa de la prueba anual de goodwill; sí de 78 de deterioro de I+D en curso de PetMedix (intangible, no goodwill; PDF p. 15). "
        f"Goodwill + intangibles: (2.888 + 850) ÷ 15.088 = {pct(F(2888 + 850, 15088))}.", H="% (decimal)")
# C53, C54
entrada("C53", 1333, "1.333 (balance a 30-sep-2026; incluye 2 de caja restringida, nota (b)). Inversiones a corto plazo aparte: 200.",
        "10-Q T3 2026 PDF p. 5", "saldo a 30-sep-2026 (10-Q 3T26)", "mm", "dato publicado", "2026-09-30", "cifra tal como se publica",
        "30-sep-2026", "10-Q 3T26 (primaria)", "Zoetis 10-Q 3T26 (balance p. 5)",
        f"{T2N} Antes 1.476 (30-jun-2026). 31-dic-2025: 2.312 en el 10-K / 2.450 reexpresado en el 10-Q (FYA). La caja baja 1.117 en nueve meses: "
        f"recompras pagadas 1.690 y dividendos 666 frente a un CFO de 1.880 (10-Q T3 PDF p. 8). Sin dividendos a pagar en el balance del 30-sep-2026 "
        f"(«—», p. 5).")
entrada("C54", 9049, "9.049 = porción corriente de la deuda a largo 750 + deuda a largo plazo contable 8.299 (balance a 30-sep-2026); sin préstamos a corto; sin arrendamientos.",
        "10-Q T3 2026 PDF p. 5 y 17", "saldo a 30-sep-2026 (10-Q 3T26)", "mm", "derivado de datos publicados (suma de dos líneas del balance)", "2026-09-30",
        "porción corriente + deuda a largo plazo (contables)", "30-sep-2026", "10-Q 3T26 (primaria)", "Zoetis 10-Q 3T26 (balance p. 5; deuda p. 17 y 44)",
        f"{T2N} Antes 9.048 (30-jun-2026, sin porción corriente). El bono de 750 al 3,000 % (vence el 12-sep-2027) pasa a corriente (10-Q T3 PDF p. 44). "
        f"Nominal 9.150 sin cambios (11 emisiones, PDF p. 44); valor razonable de la deuda a largo 8.115 (PDF p. 17). Con arrendamientos operativos "
        f"(no corrientes 188, p. 5; los corrientes no se desglosan en el 10-Q) sería mayor. Vencimientos: 2027 750 · 2028 1.350 · 2029 2.000 "
        f"(convertible al 0,25 %, conversión ≈148,20 USD) · 2030 750 · después 4.300 (PDF p. 44).")
# --- evidencia de las filas que no cambian de valor (C31, C34, D4) y evidencia preparada (C25, C27, C76)
ventas_9m = (v["q3_p3_revenue_9m2026"] / v["q3_p3_revenue_9m2025_recast"] - 1)
inv_ini, ar_ini = 2536 - d["inv_ltm_aumento"], 1692 - d["ar_ltm_aumento"]
evid = {
    "Análisis!D4": {"M": "Fecha del análisis: 5-nov-2026 (cierre del día en que se publicó el T3; segundo tiempo). Último periodo publicado: 10-Q 3T26 (cierre 30-sep-2026, presentado el 5-nov-2026). Métricas actuales: LTM a 30-sep-2026.",
                    "N": "Cambio contable: desde 1-ene-2026 Zoetis eliminó el desfase de un mes de las filiales no estadounidenses (Fiscal Year Alignment, retrospectivo; 10-Q T3 2026 nota 2, PDF p. 10–11). LTM principal = FY25 (10-K) − 9M25 «as previously reported» (donde la nota 2 lo da) + 9M26. (zoetis_t2: sustituye el texto del primer tiempo, que fechaba el análisis el 9-oct-2026 con los datos del 2T.)"},
    "Análisis!C31": {"G": "LTM a 30-sep-2026 (variaciones del estado de flujos) · ingresos: 9M-2026 frente a 9M-2025", "I": "10-Q 3T26 (estado de flujos y balance) + 10-K 2025",
                     "M": (f"Sí (comprobado con el T3 2026): inventario 2.536 y cobros 1.692 a 30-sep-2026 (10-Q T3 p. 5); en doce meses (variaciones del estado "
                           f"de flujos) el inventario aumenta {es(int(d['inv_ltm_aumento']))} y los cobros {es(int(d['ar_ltm_aumento']))}, frente a ingresos de "
                           f"nueve meses +{pct(ventas_9m)} reportados (−1 % operativos)."),
                     "J": "Zoetis 10-Q 3T26 (p. 3, 5 y 8); Zoetis · Informe anual 2025 (p. 70)", "K": K_T3, "L": "10-Q T3 2026 PDF p. 3, 5 y 8; 10-K 2025 PDF p. 70",
                     "N": (f"{T2N} Comprobado con el T3; el valor «Sí» no cambia. El 10-Q del T3 no publica el balance del 30-sep-2025, así que la comparación "
                           f"interanual del 2T de la etapa 1 no se repite; se usan las variaciones del estado de flujos (sin divisa ni adquisiciones), 2025 + "
                           f"9M-2026 − 9M-2025 (aproximación: el 9M-2025 está reexpresado): inventario 199 − 182 + 143 = {es(int(d['inv_ltm_aumento']))} de aumento "
                           f"(≈ {pct(d['inv_ltm_aumento'] / inv_ini)} sobre {es(int(inv_ini))} → 2.536 a 30-sep-2026) y cobros 236 − 190 + 291 = "
                           f"{es(int(d['ar_ltm_aumento']))} (≈ {pct(d['ar_ltm_aumento'] / ar_ini)} → 1.692), frente a ingresos de 9M +{pct(ventas_9m)} reportados "
                           f"y −1 % operativos (10-Q T3 PDF p. 3 y 29). La empresa atribuye el aumento de cobros al calendario de ventas y cobros, con los días "
                           f"de cobro dentro de 45–75 (PDF p. 40 y 42). Confianza media.")},
    "Análisis!C34": {"G": "30-sep-2026 (balance del 3T 2026)", "I": "10-Q 3T26 (primaria)", "J": "Zoetis 10-Q 3T26 (balance p. 5; liquidez p. 42)", "K": K_T3,
                     "L": "10-Q T3 2026 PDF p. 5 y 42",
                     "M": "Sí. Caja no restringida 1.331 (1.333 − 2 restringida) frente a deuda financiera a corto 750 (porción corriente del bono del 3,000 % que vence el 12-sep-2027; sin papel comercial ni préstamos).",
                     "N": (f"{T2N} Comprobado con el T3; el valor «Sí» no cambia: 1.331 ÷ 750 = {es(float(F(1331, 750)), 2)}x (con las inversiones a corto de "
                           f"200, {es(float(F(1531, 750)), 2)}x). Con el 2T no había deuda a corto (la etapa 1 preveía 1,96x al pasar el bono a corriente). "
                           f"Revolving de 1.250 sin disponer, prorrogado en agosto de 2026 hasta el 27-ago-2031; otras líneas 46 sin disponer (PDF p. 42). "
                           f"Confianza alta.")},
    "Análisis!C25": {"M": (f"Evidencia (Claude orquestación, zoetis_t2, 3T 2026): FCF = CFO − capex 1.736 (2021) → 1.326 (2022) → 1.621 (2023) → 2.298 "
                           f"(2024) → 2.283 (2025) (Historia) → {es(int(d['cfo_ltm'] - d['capex_ltm']))} LTM a 30-sep-2026 (CFO 2.773 − capex 493; todo "
                           f"reexpresado 2.235; 10-Q T3 PDF p. 8 y 11). 9M-2026: CFO 1.880 frente a 2.056 reexpresado (−8,6 %) y capex 334 frente a 462 "
                           f"(PDF p. 8). Por acción ayuda la recompra (acciones medias diluidas 9M 417,3 frente a 445,6, PDF p. 3).")},
    "Análisis!C27": {"M": (f"Evidencia (Claude orquestación, zoetis_t2, 3T 2026): margen EBIT (BAI + intereses) 34,9 % (2021), 35,6 %, 37,2 %, 36,3 %, "
                           f"37,8 % (2025) (Historia) → {pct(d['ebit_ltm'] / d['revenue_ltm'])} LTM a 30-sep-2026 (3.356 ÷ ingresos 9.467 − 7.080 + 7.121 = "
                           f"9.508; 10-Q T3 PDF p. 3 y 10). 9M-2026: margen antes de impuestos 33 % frente a 36 %; coste de ventas 28,3 % frente a 27,9 % "
                           f"de los ingresos (PDF p. 29); incluye 142 de reestructuración y 78 de deterioro de I+D en curso (PDF p. 3 y 15). Margen bruto "
                           f"ajustado T3 71,0 % frente a 71,3 % (presentación del T3, PDF p. 9).")},
    "Análisis!C76": {"G": "30-sep-2026", "I": "10-Q 3T26 (evidencia preparada)", "J": "Zoetis 10-Q 3T26 (balance p. 5; adquisiciones p. 14)", "K": K_T3,
                     "L": "10-Q T3 2026 PDF p. 5, 8 y 14",
                     "M": ("Evidencia (Claude orquestación, zoetis_t2, 3T 2026): caja 1.333 (+200 de inversiones a corto en depósitos a plazo); restringida 2; "
                           "sin dividendos a pagar en el balance del 30-sep-2026; deuda 9.049, con 750 a corto (bono de sep-2027): deuda neta 7.716. Neogen "
                           "(genómica animal): cierre esperado a principios de 2027, precio no publicado en el 10-Q (PDF p. 14). Nada es claramente sobrante; "
                           "recomendación de la etapa 1 (hecha con el 2T): vacío (= 0). Decide el inversor.")},
}
# --- metadatos
precio = {
    "valor": float(PRECIO), "moneda_cotizacion": "USD", "fecha": "2026-11-05", "fx": None, "fx_fecha": None,
    "fuente": ("Cierre del 5-nov-2026 en NYSE (ZTS) = 82,11 USD, de la página oficial de la empresa: investor.zoetis.com, «Stock Information», tabla "
               "«XNYS:ZTS historical stock data», fila «November 05, 2026 | $82.11» (6-nov-2026: $79.4; 4-nov-2026: $89.2). Bytes: SOLO TRANSCRIPCIÓN "
               "del extractor Mistral (rama mistral/examen-zoetis-t2, resultados_examen/zoetis_t2/fuentes_mercado/, leída el 18-nov-2026), conservada en "
               "fuentes_mercado/Zoetis_IR_XNYS_ZTS_historico_acciones_20261118_mistral_examen_zoetis_t2.txt con su huella (1eee36e6…08de, la que "
               "publica su HUELLAS.txt); FALTA una captura o un CSV original de la página (la del primer tiempo sí tenía captura de la persona). La "
               "transcripción del extractor heredada de zoetis_t1d (Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt, 7a8d45f2…ad) da el mismo "
               "cierre. Cierre del día de la publicación del T3 (resultados antes de la apertura), sin hora intradía.")}
acciones = copy.deepcopy(meta["acciones_diluidas"])
assert acciones["valor"] == 424.927535 and acciones["impreso"] == "424,927,535"
acciones["fuente"] = acciones["fuente"].replace("muy fuera de dinero frente a 73,08 USD", "muy fuera de dinero frente a 82,11 USD").replace(
    "la desalineación con el precio del 8-oct-2026 se declara", "la desalineación con el precio del 5-nov-2026 se declara") + (
    " (zoetis_t2) El 10-Q del T3 2026 imprime 407.487.227 acciones en circulación a 30-sep-2026 (PDF p. 5) y la portada 406.316.147 a 30-oct-2026 "
    "(PDF p. 1); no se usan (P-O2).")
assert "82,11" in acciones["fuente"] and "5-nov-2026" in acciones["fuente"]
capitalizacion = {
    "valor": float(CAP), "fecha": "2026-11-05",
    "fuente": ("Precio de cierre 82,11 USD (5-nov-2026; investor.zoetis.com, tabla «XNYS:ZTS historical stock data», transcripción conservada en "
               "fuentes_mercado/) × 424,927535 millones de acciones en circulación al 31-dic-2025 = 34.890,79989885 millones de USD, producto exacto (sin "
               "redondear las acciones ni el resultado). DESALINEACIÓN DE FECHAS declarada (Z-ACC, 19-nov-2026): precio del 5-nov-2026 y acciones al "
               f"cierre del ejercicio (P-O2); con las 407.487.227 acciones del 30-sep-2026 (10-Q T3 2026 p. 5) sería {es(float(PRECIO * ACC_SEP), 8)}, y con "
               f"las 406.316.147 del 30-oct-2026 (portada del 10-Q T3) {es(float(PRECIO * ACC_OCT), 8)}.")}
assert abs(float(PRECIO * ACC_SEP) - 33458.77620897) < 1e-6
tx_t = open(os.path.join(T1D, "Zoetis", "fuentes_mercado", "US_Treasury_par_yield_2026_Release_766892834.txt"), encoding="utf-8").read()
fila_t = [l for l in tx_t.split("\n") if l.startswith("11/05/2026 |")]
assert len(fila_t) == 1 and fila_t[0].split(" | ")[12] == "4.84", fila_t
tasa = {
    "valor": 0.0484,
    "fuente": ("Treasury de EE. UU. a 10 años, Daily Treasury Par Yield Curve Rates del Departamento del Tesoro, cierre del 5-nov-2026: 4,84 % (fila "
               "«11/05/2026», columna «10 Yr»). Bytes: CSV oficial us_treasury_par_yield_2026.csv subido por la persona responsable a la Release "
               "fuentes-examen-20261118 (asset 766892834, SHA-256 0707733bdc20fce9a21a1063c5b99dbfd3456acabb216f73e6d6b798f511243d), conservado en "
               "fuentes_mercado/US_Treasury_par_yield_2026_Release_766892834.csv (heredado de zoetis_t1d) con su copia de texto. Coincide con el "
               "extracto de Mistral (4,84 %; 6-nov 4,86 %). Moneda del modelo USD; el Treasury se toma como libre de riesgo de impago.")}
FECHA_PUB = (c1d["fechas"]["publicacion_fuentes"].replace("Corte del primer tiempo: nada publicado después del 9-oct-2026; fecha de análisis = 2026-10-09 (corte), como en zoetis_t1.", "")
             + " SEGUNDO TIEMPO (zoetis_t2, encargo del coordinador del 19-nov-2026): Form 10-Q del T3 2026 (presentado el 5-nov-2026), comunicado y "
               "presentación de resultados del T3 2026 (5-nov-2026), con la guía 2026 actualizada (Release fuentes-examen-20261118; RELEASE_FUENTES_EXAMEN_"
               "VERIFICACION.md: «segundo tiempo = comunicado y presentación del T3 (5-nov-2026) + 10-Q T3»). Nada publicado después del 5-nov-2026; fecha "
               "de análisis = 2026-11-05. Precio del 5-nov-2026 (investor.zoetis.com, transcripción de Mistral; falta captura o CSV) y Treasury del "
               "5-nov-2026 (CSV oficial del Tesoro, asset 766892834).")
assert "9-oct-2026; fecha de análisis" not in FECHA_PUB
fuentes_ad = [
    {"pdf": f"{EX}/zoetis_t2/fuentes_release/zoetis-10q-2026-q3.pdf", "sha256": SHA_PDF["zoetis-10q-2026-q3.pdf"], "texto": "texto/zoetis-10q-2026-q3.txt"},
    {"pdf": f"{EX}/zoetis_t2/fuentes_release/zoetis-3q2026-financial-results.pdf", "sha256": SHA_PDF["zoetis-3q2026-financial-results.pdf"], "texto": "texto/zoetis-3q2026-financial-results.txt"},
]
NOTA_META = (
    "(zoetis_t2, 19-nov-2026) Segundo tiempo: la información usada es la publicada hasta el 5-nov-2026 (10-Q, comunicado y presentación del T3 2026); "
    "precio y tasa son cierres del 5-nov-2026. fecha_analisis = 2026-11-05. La hora de cierre del precio y del Treasury no figura en las fuentes (cierre "
    "del día). El Treasury a 10 años (4,84 %) sale del CSV oficial del Tesoro de la Release (asset 766892834). El precio 82,11 USD sale de la tabla "
    "«XNYS:ZTS historical stock data» de investor.zoetis.com en la transcripción conservada por Mistral (falta una captura o un CSV original). Z-ACC: "
    "acciones al cierre del ejercicio (P-O2) con precio del 5-nov-2026, desalineación declarada en C41 y C42; últimas cifras publicadas tras el cierre, "
    "solo informativas: 407.487.227 acciones a 30-sep-2026 (10-Q T3 p. 5) y 406.316.147 a 30-oct-2026 (portada del 10-Q T3); con 407,5 millones la "
    "capitalización sería ≈ 33.459 mm USD. Z-R (19-nov-2026): se deja la agrupación geográfica de la r mínima; «Región · Asia» incluye «Other emerging "
    "markets» (913 mm, que no son solo Asia) y «Región · Australia & New Zealand» incluye «Other developed markets» (641 mm) y «Contract manufacturing & "
    "human health» (116 mm): las etiquetas del modelo no son las del informe (10-K 2025 PDF p. 77).")
conf = {
    "tipo": "cambio_de_base", "version_formato": 1, "empresa": "Zoetis",
    "_estado_del_archivo": (
        "Examen del personaje (19-nov-2026), Zoetis SEGUNDO TIEMPO («el mismo expediente más el trimestre del 5-nov-2026»). Expediente nuevo zoetis_t2 "
        "desde zoetis_t1d/Zoetis (que no se toca) en la rama examen/expedientes-f1. POR QUÉ un expediente nuevo: el segundo tiempo cambia la fecha de "
        "análisis (9-oct → 5-nov-2026, cierre del día de la publicación del T3), las fuentes (se añaden el Form 10-Q del T3 2026 y el comunicado y la "
        "presentación de resultados del T3 del 5-nov-2026, de la Release fuentes-examen-20261118, huellas f797be28…, fe2c88a8… y bac00765… comprobadas "
        "contra RELEASE_FUENTES_EXAMEN_SHA256SUMS) y por tanto las entradas de los doce últimos meses y del balance reciente, el precio y la tasa sin "
        "riesgo, y repite las fases: no puede hacerse sobre zoetis_t1d sin perder su primer tiempo. Entradas recalculadas con el T3 (cada componente "
        "comprobado en texto/ con su página por resultados/scripts/cifras_t3.py): LTM al 30-sep-2026 = 10-K 2025 + 9M-2026 − 9M-2025, con el 9M-2025 "
        "«As previously reported» de la nota 2 donde existe (BAI, impuestos, beneficio neto, CFO) y reexpresado donde no (intereses, D&A, capex, "
        f"arrendamientos financieros): aproximación declarada por la «Fiscal Year Alignment». C33 = {es(float(d['C33']), 6)} (antes 1,896794), C40 = "
        f"{es(int(d['fcf_ltm']))} (antes 2.363), C42 = {es(float(C42), 6)} (antes 9,675778), C24 = {es(float(d['C24']), 6)} (ROIC LTM con capital a "
        f"30-sep-2026; antes 0,266 de la etapa 1, no reproducible), C32 = {es(float(d['C32']), 6)} exacto (antes 0,184 redondeado), C53 = 1.333 (antes "
        "1.476) y C54 = 9.049 (antes 9.048; incluye ahora 750 a corto); C31 («Sí») y C34 («Sí») comprobadas con el T3 sin cambio de valor; D4 y la "
        "evidencia preparada de C25, C27 y C76 al T3. Mercado: C37 = 82,11 USD (cierre del 5-nov-2026, tabla de investor.zoetis.com en la transcripción "
        "conservada por Mistral, huella comprobada; falta captura o CSV original), C41 = C37 × C55 = 34.890,79989885 exacto, C57 = 4,84 % (CSV oficial "
        "del Tesoro, asset 766892834, fila 11/05/2026). C55 = 424,927535 sin cambio (P-O2) y desalineación declarada (Z-ACC). Se conserva todo lo demás "
        "vigente de zoetis_t1d: US GAAP, D-US1, fila 23 solo con arrendamientos financieros, EBIT = BAI + intereses, minoritarios negativos a 0 con aviso "
        "(Z-MIN), Z-R, PPA como cota superior, C46/C47/C49/C50 con su cálculo declarado (FY2023–2025), C48 = 0, motor_a_f1.json, las decisiones de la "
        "persona (DECISIONES_PARA_EL_USUARIO.md) y el registro verificacion_entradas.json en su versión sellada y comprometida de zoetis_t1d (897db35, «registros "
        "definitivos»; igual en dfc0a2c, auditoría aprobada del primer tiempo): las entradas que cambian quedan pendientes (extractor «Claude orquestación»), "
        "las selladas que no cambian conservan su sello solo si el programa mantiene vigente su vínculo. El extracto (extracto_v63.md) se pone al día con "
        "la tabla de vigencia y el T3 (guía del 5-nov-2026, demanda colectiva). Tasa 9 % provisional. Nada adoptado; no apto para dinero real."),
    "origen": f"{EX}/zoetis_t1d/Zoetis",
    "destino": f"{EX}/zoetis_t2",
    "base_economica": {"fecha": "2025-12-31", "descripcion": (
        "Ejercicio 2025 de Zoetis (cerrado el 31-dic-2025) para el FCF base (FY2023–2025, sin cambios), con el SEGUNDO TIEMPO del examen: información "
        "hasta el 5-nov-2026 (10-Q, comunicado y presentación del T3 2026). Cambian los doce últimos meses y el balance reciente (30-sep-2026: C24, C32, "
        "C33, C40, C42, C53, C54), el precio (82,11 USD del 5-nov-2026), la capitalización (C37 × C55 exactos) y la tasa sin riesgo (4,84 %).")},
    "fechas": {"ejecucion": "2026-11-05", "precio": "2026-11-05", "acciones": "2025-12-31", "publicacion_fuentes": FECHA_PUB},
    "conservar": c1d["conservar"],
    "fuentes_adicionales": fuentes_ad,
    "metadatos": {"precio": precio, "acciones_diluidas": acciones, "capitalizacion": capitalizacion, "tasa_sin_riesgo": tasa},
    "notas_que_se_retiran": [r"^Primer tiempo: la información usada es la publicada hasta el 9-oct-2026",
                             r"^Últimas cifras publicadas tras el cierre, solo informativas: 422\.127\.709",
                             r"^Diferencia relevante: con 414,2 millones",
                             r"^\(zoetis_t1d, 19-nov-2026\) La hora de cierre del precio y del Treasury"],
    "nota_metadatos": NOTA_META,
    "analisis": analisis,
    "analisis_que_se_conservan": {c: (f"entrada de zoetis_t1d sin cambio (media FY2023–2025 del 10-K 2025, cálculo declarado): el T3 de 2026 y los datos "
                                      f"de mercado del 5-nov-2026 no cambian {c}") for c in ("C46", "C47", "C49", "C50")},
    "analisis_que_se_descartan": {},
    "evidencia": dict(evid, **{"Análisis!C38": c1d["evidencia"]["Análisis!C38"]}),
    "control_maestro_textos": {
        "F5": ("FY2023–FY2025 (media de 3 años) en C46, C47 y C50 (decisión del inversor del 18-oct-2026, Control maestro M43, M44 y M48); LTM a "
               "30-sep-2026 en C24, C33, C40 y C42 (aproximación declarada por la «Fiscal Year Alignment») y balance a 30-sep-2026 en C32, C53 y C54 "
               "(10-Q T3 2026); precio del 5-nov-2026 (C37) y acciones a 31-dic-2025 (C55, P-O2): desalineación declarada (Z-ACC). (zoetis_t2: "
               "sustituye el texto del primer tiempo, con los doce meses al 30-jun-2026.)"),
        "D90": c1d["control_maestro_textos"]["D90"],
        "D88": ("LTM a 30-sep-2026 = FY25 (10-K) − 9M25 «as previously reported» donde la nota 2 lo da (BAI, impuestos, beneficio neto y CFO) + 9M26 "
                "(10-Q 3T26); intereses, D&A, capex y arrendamientos financieros de 9M25 solo reexpresados (aproximación declarada). Balance a "
                "30-sep-2026. Precio 5-nov-2026. Fiscal Year Alignment documentada (10-Q T3 2026, nota 2, PDF p. 10–11; el FY2025 aún no está "
                "reexpresado). (zoetis_t2: sustituye el texto del primer tiempo, con los datos del 2T y el precio del 8-oct-2026.)")},
    "textos_prohibidos": [r"31[.,]?053[.,]70", r"9[.,]675778", r"1[.,]896794", r"TTM a 30-jun-2026", r"\b3\.992\b", r"73,08 USD", r"5,22 %",
                          r"9\.048 = deuda", r"1\.476 \(balance", r"jun-25 10\.123"],
    "alcance": None, "configuracion_economica": None,
    "entrada_efectiva": {"modo": "estricta", "motivo": "expediente nuevo de la 4.15 (modo por defecto)"},
}
al = copy.deepcopy(c1d["alcance"])
al["aviso"] = (
    "EXAMEN DEL PERSONAJE · ZOETIS (caso del examen: SEGUNDO TIEMPO, información hasta el 5-nov-2026, precio de cierre del 5-nov-2026) · plantilla V6.3.1 "
    "F1 (config_v2_v631_f1.json) con el código de examen/expedientes-f1. Expediente zoetis_t2 (cambio_zoetis_t2.json) desde zoetis_t1d (primer tiempo), "
    "y antes zoetis_t1c y zoetis_t1b. Etapa 1 de la persona responsable (Zoetis_evaluada.xlsx c33f17d1…5093, Zoetis_respuesta.md 7f29de8e…d0a1). "
    "Fuentes oficiales con huella en la Release fuentes-examen-20261118 (FUENTES.tsv): Form 10-K 2016–2025, Form 10-Q del T1, T2 y T3 de 2026, "
    "comunicado, presentación y conferencia de resultados del T2 2026 (6-ago-2026) y comunicado y presentación de resultados del T3 2026 (5-nov-2026), "
    "con la guía 2026 actualizada el 5-nov-2026 (guía de la dirección, no hecho); nada publicado después del 5-nov-2026 entra. US GAAP: F1 con D-US1 y "
    "D-US2 (D-WM no aplica). Fila 23 solo con arrendamientos financieros. C46/C47/C50 exactas con cálculo declarado (FY2023–2025); C49 = 1,0; C48 = 0. "
    "P-O1 (c). P-O2 (a) y Z-ACC: 424,927535 M acciones a 31-dic-2025 (exactas), precio del 5-nov-2026 y desalineación declarada en C41 "
    "(34.890,79989885) y C42. C24, C33, C40 y C42: LTM a 30-sep-2026, aproximación declarada por la «Fiscal Year Alignment». Z-R: agrupación geográfica "
    "de la r mínima sin cambios, con la diferencia anotada. Minoritarios 2022–2023 impresos (2) y (6) → 0 (Z-MIN). Tasa sin riesgo 4,84 % del CSV oficial "
    "del Tesoro (Release, anexo 3). Precio 82,11 USD: tabla de investor.zoetis.com en la transcripción de Mistral conservada en fuentes_mercado/ (falta "
    "captura o CSV original). Tasa 9 % provisional, sin decidir. Nada adoptado; no apto para dinero real.")
al["fuente"] = al["fuente"] + (" · configuracion/cambio_zoetis_t2.json (segundo tiempo, encargo del coordinador del 19-nov-2026); "
                               "RELEASE_FUENTES_EXAMEN_VERIFICACION.md (separación por fecha: segundo tiempo = 10-Q, comunicado y presentación del T3 2026).")
al["fecha"] = "2026-11-19"
conf["alcance"] = al
json.dump(conf, open(SAL, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps({c: x["valor"] for c, x in analisis.items()}, ensure_ascii=False))
print("C41", float(CAP), "C42 acciones sep", float(C42_SEP), "C42 recast", float(C42_REC))
