#!/usr/bin/env python3
"""zoetis_t1d · tabla de vigencia de las cifras heredadas de la etapa 1, al principio de extracto_v63.md (encargo del coordinador, 19-nov-2026, lección de
la revisión de ahold_f4: coordinacion/cierre_v2/examen/revisiones/expedientes_f1/REVISION_AHOLD_F4.md, hallazgos 1 y 2, en el repositorio auxiliar).
No toca los textos heredados (sección 6 de datos_v63.md, etapa1/Zoetis_respuesta.md, Control maestro N): añade un bloque registrado «0. Vigencia …» entre la
cabecera y la sección 1 del extracto conservado de zoetis_t1c (el original va a antecedentes/). Cada cifra vigente sale de fase1_v63.json del expediente o
de las fuentes que se citan; el guion comprueba las que puede. Rastro (y textos de Control maestro neutralizados o no) en RASTRO.json.
Uso: python3 -I vigencia_extracto_t1d.py CARPETA_EMPRESA CARPETA_ANTECEDENTES RASTRO.json"""
import hashlib, json, os, shutil, sys
from fractions import Fraction as F
C, ANT, RASTRO = sys.argv[1:4]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
ex = os.path.join(C, "extracto_v63.md")
orig = os.path.join(ANT, "extracto_v63_conservado_de_zoetis_t1c.md")
assert not os.path.exists(orig)
f1 = json.load(open(os.path.join(C, "fase1_v63.json"), encoding="utf-8"))
an = {k: (v["valor"] if isinstance(v, dict) else v) for k, v in f1["analisis"].items()}
P = f1["historia"]["partidas"]
anios = f1["historia"]["anios"]
ventas, ebit = P["ventas"]["valores"], P["ebit"]["valores"]
cap, acc = F(repr(f1["capitalizacion"]["valor"])), F(repr(f1["acciones_diluidas"]["valor"]))
assert cap == F("73.08") * acc and acc == F("424.927535")
c52 = F(repr(an["C46"])) - F(repr(an["C47"])) - F(repr(an["C48"])) - F(repr(an["C49"])) - F(repr(an["C50"]))
assert c52 == F("1994.001"), c52
dn = 9048 - 1476
ebit_ttm = (3360 - 1712 + 1624) + (222 - 107 + 123)
assert ebit_ttm == 3510 and ebit_ttm + (487 - 243 + 238) == 3992
assert abs(an["C42"] - float((cap + dn) / 3992)) < 1e-15 and an["C40"] == 2363 and abs(an["C33"] - dn / 3992) < 1e-15
coma = lambda x, d: f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")  # noqa: E731
margen = " · ".join(f"{a} {coma(100 * e / v, 1)} %" for a, e, v in zip(anios, ebit, ventas))
assert ebit[-1] == 3582 and ventas[-1] == 9467

filas = [
 ("Capitalización (C41)", "30.198 mm (C13); 30.198,4 = 73,08 × 413,223602 (acciones de la portada del 10-Q, 31-jul-2026; Control maestro de la etapa 1)",
  f"{coma(float(cap), 7)} mm = 73,08 × 424,927535, producto exacto", "Análisis!C41",
  "fase1_metadatos.json (capitalizacion); acciones: 10-K 2025 PDF p. 68. P-O2 y Z-ACC (19-nov-2026): acciones al cierre del ejercicio con precio del 8-oct-2026, desalineación de fechas declarada; con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 PDF p. 5) sería 30.266,4"),
 ("Acciones (C55)", "417,7 m (media ponderada diluida del 2T26; respuesta.md §1 y Control maestro); 413,2 en portada (31-jul-2026)",
  "424,927535 m, exactas (424.927.535 acciones en circulación a 31-dic-2025, sin dilución)", "Análisis!C55",
  "10-K 2025 PDF p. 68 (balance); comprobado contra la cifra impresa por fase1_historia.py (historia_revision.md, «Acciones de los metadatos»)"),
 ("FCF base (C52)", "1.995 mm (C13, C25, B67, B69; respuesta.md §1); «≈2.000 mm» (respuesta.md §3)",
  f"{coma(float(c52), 3)} mm = C46 2.736,667 − C47 669,333 − C48 0 − C49 1,000 − C50 72,333 (con C51 = Sí, que decide la fase A)", "Análisis!C52 (fórmula)",
  "C46, C47, C49 y C50: cálculo declarado sobre el 10-K 2025 PDF p. 70 y 89 (fase1_v63.json); C48 = 0 (US GAAP)"),
 ("Rendimiento FCF base ÷ capitalización", "≈6,6 % (C13)", f"{coma(100 * float(c52 / cap), 2)} %", "C52 ÷ C41", "derivado de las dos filas anteriores"),
 ("Deuda neta", "7.575 mm (C13, C62, C76; respuesta.md §1); «≈18 USD/acción»",
  f"7.572 mm = deuda 9.048 − caja 1.476 (30-jun-2026); {coma(dn / float(acc), 2)} USD/acción con C55", "C54 − C53", "10-Q T2 2026 PDF p. 5"),
 ("Deuda neta ÷ EBITDA (C33)", "1,92x (C20; C33 de la etapa 1)", f"{coma(an['C33'], 4)}x (aproximación declarada; todo reexpresado ≈ 1,88x)", "Análisis!C33",
  "TTM = 2025 (10-K) − 6M-2025 + 6M-2026 (10-Q T2 2026 PDF p. 3, 5, 8 y 10); «Fiscal Year Alignment»: mezcla bases (convención/aproximación, no derivado exacto)"),
 ("EBIT TTM a 30-jun-2026", "3.463 mm (EBIT derivado de la etapa 1, Control maestro M29, fundamento de C24)",
  "3.510 mm = BAI 3.272 + gasto por intereses 238 (EBIT = BAI + intereses: el signo de los intereses se corrigió desde zoetis_t1b); EBITDA 3.992 con D&A 482",
  "(dentro de C33 y C42)", "10-K 2025 PDF p. 66 y 70; 10-Q T2 2026 PDF p. 3, 8 y 10"),
 ("EV/EBITDA (C42)", "9,57x (C42 de la etapa 1, con capitalización 30.198)",
  f"{coma(an['C42'], 6)}x = (C41 + 7.572) ÷ 3.992 (aproximación declarada; con las acciones del 30-jun-2026, 9,48x; todo reexpresado ≈ 9,61x)", "Análisis!C42",
  "C41 exacto y el TTM de C33; desalineación de fechas declarada (Z-ACC): precio 8-oct-2026, acciones 31-dic-2025, balance 30-jun-2026"),
 ("FCF TTM (C40)", "2.365 mm (C25; C40 de la etapa 1, con el capex del 10-Q del T2 2025, que no está en el expediente)",
  "2.363 mm = CFO 2.887 − capex 524 − principal de arrendamientos financieros 0 (aproximación declarada; todo reexpresado 2.316)", "Análisis!C40",
  "10-K 2025 PDF p. 70 y 89; 10-Q T2 2026 PDF p. 8 y 11"),
 ("ROIC (C24)", "26,6 % (C14, C24), ≈27 % (C93), 26–30 % (B101; respuesta.md §6)",
  "C24 = 0,266 conservado como convención NO reproducible con el expediente (F «Dato no verificable»): con el EBIT corregido y el capital del expediente sale ≈ 26,2–26,9 %",
  "Análisis!C24", "registro de entradas (Análisis!C24, justificacion_clase); su fórmula y el 10-Q del T2 2025 no están en el expediente"),
 ("Margen EBIT (Historia, EBIT = BAI + intereses)", "la etapa 1 no cita el margen EBIT en cifras («márgenes crecientes», C14; el margen antes de impuestos 28,7 % → 35,5 % de C27 no depende del EBIT y no cambia)",
  margen, "Historia (ventas y ebit)", "fase1_v63.json (Historia construida por fase1_historia.py)"),
 ("C46 / C47 / C50", "2.736,7 / 669,3 / 72,3 (C51: «SBC media FY23–25 de 72,3 mm»)", "2.736,667 / 669,333 / 72,333 (valores exactos, cálculo declarado)",
  "Análisis!C46, C47, C50", "10-K 2025 PDF p. 70 (precedente E1: exactos en lugar de redondeos)"),
 ("C48 / C49", "C48 «vacía» (C62; Control maestro M45) y C49 vacía (= 0)", "C48 = 0 (US GAAP: intereses pagados dentro del CFO; cero pendiente H1) · C49 = 1,000 (principal de arrendamientos financieros — / 1 / 2)",
  "Análisis!C48, C49", "10-K 2025 PDF p. 70 y 89"),
 ("P/FCF histórico (C88)", "mediana 47,1x (C68), «47x» (B102), 66,4x en 2021 (C98)",
  "sin valor vigente verificado: C88 = 47,1 es «Dato no verificable» (Digrin, tercero sin bytes en el expediente; su FCF es CFO − capex)", "Análisis!C88",
  "registro de entradas (lectura externa, no comprobada)"),
 ("Valor intrínseco externo (C38)", "197,36 USD (Simply Wall St; Control maestro de la etapa 1)",
  "sin valor vigente verificado: C38 pasa a «Dato no verificable» en zoetis_t1d (tercero sin bytes); solo contexto", "Análisis!C38", "registro de entradas (lectura externa)"),
 ("Escenarios y precio de Sí", "malo ≈48,7–49 USD, normal ≈90,9–91, bueno ≈120,2, ponderado ≈88,3; precio de Sí ≈49 USD; capitalización ≈20.200 (C13, C20, C104, B101, B102; respuesta.md §1, §6 y §7)",
  "sin cifra vigente: son estimaciones de la etapa 1 hechas sin la hoja; las calcula el libro (precio_de_si.py) tras la fase B con las palancas de este expediente", "Análisis (escenarios)", "—"),
 ("Guía orgánica 2026", "«guía orgánica negativa para 2026 (datos)» (C13), «−3 % a −1 %» (C31, B102; respuesta.md §2)",
  "misma cifra, ahora con fuente en el expediente: crecimiento orgánico operativo (3)%–(1)% (guía de la dirección, no hecho), comunicado y presentación de resultados del T2 2026 publicados el 6-ago-2026",
  "—", "sección 5 de este extracto (decisión de la persona del 18-nov-2026: incluir la guía)"),
 ("Precio (C37) y tasa sin riesgo (C57)", "73,08 USD; Treasury a 10 años 5,22 %", "sin cambio de valor, ahora con bytes: 73,08 USD = «Closing Price $73.08» de investor.zoetis.com («Historical Stock Quote», 2026-Oct-8; captura de la persona, anexo 3 ter), en vez de stockanalysis/MarketBeat; 5,22 % del CSV oficial del Tesoro (Release, asset 766892834)",
  "Análisis!C37, C57", "fuentes_mercado/ (Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.png y .txt; US_Treasury_par_yield_2026_Release_766892834.csv y .txt)"),
]
L = ["## 0. Vigencia de las cifras heredadas de la etapa 1 (zoetis_t1d, Claude orquestación, 19-nov-2026)", "",
     "Los textos heredados de la etapa 1 (sección 6 de `datos_v63.md`, `etapa1/Zoetis_respuesta.md`, observaciones del Control maestro) **no se han tocado** y "
     "citan cifras que hoy valen otra cosa. Esta tabla da, para cada una, el valor vigente del expediente, su celda y su fuente. Manda la columna «vigente». "
     "Bloque añadido por la orquestación al extracto conservado de zoetis_t1c (rastro: `resultados/vigencia_extracto_t1d.json`); no es extracción nueva de las fuentes.", "",
     "| Cifra | Etapa 1 (dónde la cita) | Vigente | Celda | Fuente |", "|---|---|---|---|---|"]
L += [f"| {a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in filas]
L += ["", "Otras correcciones de zoetis_t1d que la etapa 1 no cita:",
      "- Minoritarios (Historia fila 26): 2022 y 2023 impresos «(2)» y «(6)» (patrimonio negativo de minoritarios) → 0 (decisión Z-MIN de la persona, 19-nov-2026; cifra impresa en `historia_revision.md`); 2018 = 0 («—» impreso en el 10-K 2018 PDF p. 73), antes vacío.",
      "- Reparto geográfico de la r mínima (Palancas A28:B33; decisión Z-R, 19-nov-2026: se deja y se anota): «Región · Asia» incluye «Other emerging markets» (913 mm, que no son solo Asia) y «Región · Australia & New Zealand» incluye «Other developed markets» (641 mm) y «Contract manufacturing & human health» (116 mm): las etiquetas del modelo no son las del informe [zoetis-10k-fy2025.txt, PDF p. 77].",
      "- C33, C40 y C42 son aproximaciones declaradas (TTM con la «Fiscal Year Alignment»), no derivados exactos.", ""]
bloque = "\n".join(L) + "\n"
t = open(ex, encoding="utf-8").read()
i = t.index("\n## 1. Mercado y cuota")
shutil.copy2(ex, orig)
open(ex, "w", encoding="utf-8").write(t[:i + 1] + bloque + t[i + 1:])
# textos del Control maestro: neutralizados (en la copia de ensayo por cambiar_base.py o por control_maestro_textos) y los que no se tocan, con el motivo
import openpyxl  # noqa: E402
cm0 = openpyxl.load_workbook(os.path.join(ANT, "etapa1_original", "Zoetis_evaluada.xlsx"), data_only=True)["Control maestro"]
fila = lambda b: [r for r in range(17, 83) if cm0[f"B{r}"].value == b][0]  # noqa: E731
textos = {
 "neutralizados": [
  {"celda": "Control maestro!F5", "antes": cm0["F5"].value, "como": "control_maestro_textos (cambio_zoetis_t1d.json → fase1_v63.json → rellenar_fase1_v63.py)", "motivo": "el período de las medias ya está decidido (FY23–25)"},
  {"celda": "Control maestro!D90", "antes": cm0["D90"].value, "como": "control_maestro_textos", "motivo": "C46/C47/C50 están decididas y C48/C49 ya no están vacías"},
  {"celda": f"Control maestro!F{fila('Análisis!C38')} y N{fila('Análisis!C38')} (Análisis!C38)", "antes": {"F": cm0[f"F{fila('Análisis!C38')}"].value, "N": cm0[f"N{fila('Análisis!C38')}"].value},
   "como": "evidencia de cambio_zoetis_t1d.json (copia de ensayo; el anterior también en antecedentes/evidencia_anterior.json)", "motivo": "tercero sin bytes: «Dato no verificable»"}],
 "ya_neutralizados_por_el_producto": [
  {"celda": f"Control maestro!G/L/M/N{fila('Análisis!C41')} (C41) y G/L/M/N{fila('Análisis!C55')} (C55)", "antes": {"C41_M": cm0[f"M{fila('Análisis!C41')}"].value, "C55_M": cm0[f"M{fila('Análisis!C55')}"].value},
   "motivo": "rellenar_fase1_v63.py escribe la evidencia de los metadatos (precio × acciones al 31-dic-2025) y vacía M y N en el libro de datos (comprobado en zoetis_t1c); no llegan a datos_v63.md"},
  {"celda": f"Control maestro!N{fila('Análisis!C88')} (C88)", "motivo": "«Dato no verificable» desde zoetis_t1c (copia de ensayo heredada)"}],
 "no_neutralizados": [
  {"celda": f"Control maestro!M{fila('Análisis!C48')} (C48)", "texto": cm0[f"M{fila('Análisis!C48')}"].value,
   "motivo": "«Celda vacía» describe la etapa 1; el tratamiento (intereses dentro del CFO, US GAAP) no contradice ninguna decisión y C48 = 0 lo da la Historia. La fila de evidencia forma parte del vínculo sellado de Análisis!C48 (verificado): reescribirla retiraría ese sello. La columna M no se vuelca a datos_v63.md; la tabla de vigencia lo aclara"},
  {"celda": f"Control maestro!M{fila('Análisis!C24')} (C24)", "motivo": "es la procedencia documentada de la convención C24 (EBIT 3.463 de la etapa 1); se conserva y la tabla da el EBIT vigente (3.510)"},
  {"celda": "Control maestro!B47 (fila CONTROL «Otros pagos relacionados con leases fuera de CFO»)", "texto": cm0["M47"].value, "motivo": "coherente con US GAAP y D-US1; no contradice ninguna decisión vigente"}]}
json.dump({"fecha": "2026-11-19", "guion": "resultados/scripts/vigencia_extracto_t1d.py", "extracto_antes_sha256": h(orig), "extracto_despues_sha256": h(ex),
           "bloque": bloque, "textos_control_maestro": textos}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print(bloque)
