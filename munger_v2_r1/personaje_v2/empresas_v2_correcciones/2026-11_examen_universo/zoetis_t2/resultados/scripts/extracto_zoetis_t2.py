#!/usr/bin/env python3
"""zoetis_t2 · extracto_v63.md del segundo tiempo (relevo de extracción del paso 5, registrado; no de juicio). Autor: «Claude orquestación».
Parte del extracto conservado de zoetis_t1d (que queda en antecedentes/) y:
  (a) cambia la cabecera (fecha de análisis 5-nov-2026 y fuentes del T3);
  (b) sustituye el bloque «## 0.» por la tabla de vigencia al 5-nov-2026: cifra de la etapa 1 o del primer tiempo (zoetis_t1d) → valor vigente →
      celda → fuente, con la evidencia preparada de C25, C27 y C76 (columna M del Control maestro, que volcar_datos_v63.py no vuelca);
  (c) añade al principio de la sección 5 la guía 2026 del 5-nov-2026 frente a la del 6-ago-2026;
  (d) añade la sección «## 10.» con el tercer trimestre (resultados, segmentos, caja, financiación, demanda colectiva del 10-Q T2 p. 23 y su
      estado en el 10-Q T3 p. 24, lo no encontrado).
Las secciones 1–9 del primer tiempo no se reescriben (son el estado al 9-oct-2026); el bloque 0 dice que manda la sección 10 donde la actualiza.
Cada cifra del T3 se comprueba aquí en texto/ antes de escribirla: frases literales de frases_t3_extracto.txt y cifras de cifras_t3.py.
Uso (desde zoetis_t2/): python3 -I resultados/scripts/extracto_zoetis_t2.py Zoetis antecedentes resultados/extracto_zoetis_t2.json"""
import hashlib, json, os, shutil, sys
from fractions import Fraction as F
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import cifras_t3 as CT  # noqa: E402
C, ANT, REG = (os.path.abspath(x) for x in sys.argv[1:4])
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
ex = os.path.join(C, "extracto_v63.md")
viejo = open(ex, encoding="utf-8").read()
assert viejo.startswith("# Extracto V6.3 · Zoetis Inc. (ZTS) · corte 9-oct-2026"), viejo[:80]
copia = os.path.join(ANT, "extracto_v63_conservado_de_zoetis_t1d.md")
assert not os.path.exists(copia)
shutil.copy2(ex, copia)
tx = CT.Textos(os.path.join(C, "texto"))
v, d = CT.calcular(tx)
n_fr = 0
for l in open(os.path.join(AQUI, "frases_t3_extracto.txt"), encoding="utf-8"):
    if l.strip():
        a, n, f = l.rstrip("\n").split("|", 2)
        tx.frase(a, int(n), f)
        n_fr += 1
cm = json.load(open(os.path.join(os.path.dirname(os.path.dirname(C)), "configuracion", "cambio_zoetis_t2.json"), encoding="utf-8"))
EV = cm["evidencia"]
CAP = F("82.11") * F("424.927535")
FCFB = F("1994.001")


def es(x, dec=0):
    s = f"{float(x):,.{dec}f}"
    return s.replace(",", "§").replace(".", ",").replace("§", ".")


Q, P, R, Q2 = "zoetis-10q-2026-q3.txt", "zoetis-3q2026-financial-results.txt", "zoetis-3q2026-press-release.txt", "zoetis-10q-2026-q2.txt"
# (a) cabecera
i_fuentes = viejo.index("\n\nFuentes:")
i_0 = viejo.index("## 0. Vigencia")
i_1 = viejo.index("## 1. Mercado y cuota")
cab = ("# Extracto V6.3 · Zoetis Inc. (ZTS) · segundo tiempo: fecha de análisis 5-nov-2026\n\n"
       "Fuentes: 10-K 2016–2025, 10-Q del T1, T2 y T3 de 2026, documentos de resultados del T2 2026 publicados el 6-ago-2026 (comunicado, "
       "zoetis-2q2026-press-release.txt, texto de una página HTML; presentación, zoetis-2q2026-financial-results.txt; transcripción de la conferencia, "
       "zoetis-2q2026-earnings-call.txt) y documentos de resultados del T3 2026 publicados el 5-nov-2026 (comunicado, zoetis-3q2026-press-release.txt, "
       "texto de una página HTML; presentación, zoetis-3q2026-financial-results.txt) (carpeta texto/). No hay transcripción de la conferencia del T3 en "
       "las fuentes. Nada publicado después del 5-nov-2026. Las secciones 1 a 9 son las del primer tiempo (estado al 9-oct-2026, sin cambios); la "
       "sección 10 añade el tercer trimestre y la sección 5 empieza con la guía del 5-nov-2026: donde la sección 10 o la tabla de vigencia actualizan "
       "una cifra anterior, mandan ellas. Cifras en millones de dólares salvo indicación. En lo que sale de los documentos de resultados del T2 2026, "
       "las frases entre «» marcadas «(paráfrasis traducida)» son traducciones de la orquestación, no citas literales. «PDF p.» es la marca `[PDF PAGE n]` "
       "del texto. Los 10-K 2020–2024 vienen de OCR: toda cifra de esos años que se cita aquí cuadra con su total (suma de segmentos, de especies o de "
       "viñetas de crecimiento) en la misma página; cuando solo hay una página, se dice. A partir del 1-ene-2026 las filiales no estadounidenses dejaron "
       "de declarar con un mes de desfase (Fiscal Year Alignment); las cifras de 2025 de los 10-Q de 2026 están reexpresadas y no coinciden con las del "
       "10-K 2025, que la empresa reexpresará cuando lo presente como comparativo [zoetis-10q-2026-q2.txt, PDF p. 29; zoetis-10q-2026-q3.txt, PDF p. 10].")
assert viejo[:i_fuentes].count("\n") == 0
# (b) bloque 0
pct = lambda x, dec=1: es(float(x) * 100, dec) + " %"  # noqa: E731
filas = [
    ("Fecha de análisis (D4)", "9-oct-2026 (primer tiempo; datos al T2, 30-jun-2026)", "5-nov-2026 (cierre del día de la publicación del T3); LTM y balance a 30-sep-2026", "Análisis!D4", "10-Q T3 2026 (presentado el 5-nov-2026)"),
    ("Precio (C37)", "73,08 USD (cierre del 8-oct-2026; etapa 1 y primer tiempo)", "82,11 USD, cierre del 5-nov-2026 (6-nov: 79,40; 4-nov: 89,20)", "Análisis!C37",
     "fuentes_mercado/Zoetis_IR_XNYS_ZTS_historico_acciones_20261118_mistral_examen_zoetis_t2.txt (tabla de investor.zoetis.com transcrita por Mistral; FALTA captura o CSV original); la transcripción heredada da el mismo cierre"),
    ("Tasa sin riesgo (C57)", "5,22 % (Treasury a 10 años del 8-oct-2026)", "4,84 % (Treasury a 10 años del 5-nov-2026)", "Análisis!C57", "fuentes_mercado/US_Treasury_par_yield_2026_Release_766892834.txt, fila 11/05/2026 (CSV oficial, asset 766892834)"),
    ("Capitalización (C41)", "30.198 mm (etapa 1, acciones de la portada del 10-Q T2); 31.053,7042578 = 73,08 × 424,927535 (primer tiempo)",
     f"{es(CAP, 8)} mm = 82,11 × 424,927535, producto exacto; con las 407.487.227 acciones del 30-sep-2026 sería 33.458,8", "Análisis!C41",
     "C37 × C55; P-O2 y Z-ACC: acciones al cierre del ejercicio con precio del 5-nov-2026, desalineación de fechas declarada [zoetis-10q-2026-q3.txt, PDF p. 5]"),
    ("Acciones (C55)", "417,7 m (media diluida del 2T26, etapa 1); 424,927535 m (primer tiempo)", "424,927535 m sin cambio (P-O2); últimas publicadas, solo informativas: 407.487.227 a 30-sep-2026 y 406.316.147 a 30-oct-2026", "Análisis!C55",
     "10-K 2025 PDF p. 68; [zoetis-10q-2026-q3.txt, PDF p. 5 y 1]"),
    ("Caja (C53)", "1.476 (30-jun-2026)", "1.333 (30-sep-2026; incluye 2 restringida); inversiones a corto 200 aparte", "Análisis!C53", "[zoetis-10q-2026-q3.txt, PDF p. 5]"),
    ("Deuda (C54)", "9.048 (30-jun-2026, sin porción corriente)", "9.049 = porción corriente 750 (bono del 3,000 % que vence el 12-sep-2027) + deuda a largo 8.299", "Análisis!C54", "[zoetis-10q-2026-q3.txt, PDF p. 5 y 44]"),
    ("Deuda neta", "7.575 (etapa 1); 7.572 (30-jun-2026, primer tiempo)", f"7.716 = 9.049 − 1.333 (30-sep-2026); {es(F(7716) / F('424.927535'), 2)} USD/acción con C55", "C54 − C53", "[zoetis-10q-2026-q3.txt, PDF p. 5]"),
    ("EBIT y EBITDA de doce meses", "EBIT 3.463 (etapa 1); EBIT 3.510 y EBITDA 3.992 (TTM a 30-jun-2026, primer tiempo)",
     f"EBIT {es(d['ebit_ltm'])} = BAI {es(d['bai_ltm'])} + intereses {es(d['int_ltm'])}; EBITDA {es(d['ebitda_ltm'])} con D&A {es(d['da_ltm'])} (LTM a 30-sep-2026)",
     "(dentro de C24, C33 y C42)", "10-K 2025 PDF p. 66 y 70; [zoetis-10q-2026-q3.txt, PDF p. 3, 8 y 10] (LTM = 2025 − 9M-2025 + 9M-2026; BAI y CFO de 9M-2025 «as previously reported»)"),
    ("Deuda neta ÷ EBITDA (C33)", "1,92x (etapa 1); 1,8968x (primer tiempo)", f"{es(d['C33'], 6)}x (aproximación declarada; con el 9M-2025 todo reexpresado {es(d['C33_recast'], 2)}x)", "Análisis!C33", "fila anterior; Fiscal Year Alignment: mezcla bases"),
    ("EV/EBITDA (C42)", "9,57x (etapa 1); 9,675778x (primer tiempo)", f"{es((CAP + 7716) / d['ebitda_ltm'], 6)}x = (C41 + 7.716) ÷ {es(d['ebitda_ltm'])} (con las acciones del 30-sep-2026, 10,74x; todo reexpresado ≈ 11,03x)", "Análisis!C42",
     "C41 exacto y el LTM de C33; desalineación de fechas declarada (Z-ACC): precio 5-nov-2026, acciones 31-dic-2025, balance 30-sep-2026"),
    ("FCF de doce meses (C40)", "2.365 (etapa 1); 2.363 (TTM a 30-jun-2026, primer tiempo)", f"{es(d['fcf_ltm'])} = CFO {es(d['cfo_ltm'])} − capex {es(d['capex_ltm'])} − principal de arrendamientos financieros {es(d['fl_ltm'])} (todo reexpresado {es(d['fcf_ltm_recast'])})", "Análisis!C40",
     "10-K 2025 PDF p. 70 y 89; [zoetis-10q-2026-q3.txt, PDF p. 8 y 11]"),
    ("Rendimiento FCF de doce meses (C40 ÷ C41)", "7,61 % (primer tiempo)", f"{pct(d['fcf_ltm'] / CAP, 2)}", "C40 ÷ C41", "derivado de las filas anteriores"),
    ("FCF base (C52) y su rendimiento", "1.994,001 mm; 6,42 % sobre la capitalización del primer tiempo", f"1.994,001 mm sin cambio (FY2023–2025); {pct(FCFB / CAP, 2)} sobre C41", "Análisis!C52 (fórmula)", "C46–C50 sin cambio (10-K 2025)"),
    ("ROIC (C24)", "26,6 % (etapa 1, TTM a 30-jun-2026; convención no reproducible en el primer tiempo)",
     f"{pct(d['C24'], 2)} = NOPAT LTM {es(d['nopat_ltm'], 1)} ÷ capital invertido a 30-sep-2026 11.019 (capital medio dic-25/sep-26: {pct(d['C24_medio'])}; sin inversiones a corto: {pct(d['C24_sin_sti'])})", "Análisis!C24",
     "10-K 2025 PDF p. 66; [zoetis-10q-2026-q3.txt, PDF p. 3, 5 y 10]; el 10-Q T3 no publica el balance del 30-sep-2025"),
    ("Goodwill ÷ activo (C32)", "18,4 % (0,184 redondeado, 30-jun-2026)", f"{pct(d['C32'], 2)} = 2.888 ÷ 15.088 (exacto); +107 por VitalRADS", "Análisis!C32", "[zoetis-10q-2026-q3.txt, PDF p. 5 y 20]"),
    ("Cobros/inventario frente a ingresos (C31)", "«Sí» (inventario +5,5 % interanual al 30-jun-2026)", "«Sí» sin cambio: inventario +160 y cobros +337 en doce meses (variaciones del estado de flujos) frente a ingresos de 9M +0,4 %", "Análisis!C31", "10-K 2025 PDF p. 70; [zoetis-10q-2026-q3.txt, PDF p. 3, 5 y 8]"),
    ("Caja frente a deuda a corto (C34)", "«Sí» (sin deuda a corto a 30-jun-2026)", "«Sí» sin cambio: 1.331 de caja no restringida frente a 750 a corto = 1,77x", "Análisis!C34", "[zoetis-10q-2026-q3.txt, PDF p. 5 y 42]"),
    ("CFO ÷ beneficio neto (C26)", "1,058 (FY2021–2025); «TTM 1,10» (etapa 1)", f"1,058 sin cambio (FY2021–2025); LTM a 30-sep-2026, solo contexto: {es(d['cfo_ltm'] / d['ni_ltm'], 3)} = {es(d['cfo_ltm'])} ÷ {es(d['ni_ltm'])}", "Análisis!C26", "10-K 2025 PDF p. 66 y 70; [zoetis-10q-2026-q3.txt, PDF p. 3, 8, 10 y 11]"),
    ("Acciones medias diluidas (C28, C60)", "«Recompra»; 2T23→2T26 −3,37 %/año (etapa 1)", "«Recompra» y −1,50 %/año (FY2020–2025) sin cambio; 9M-2026 417,3 m frente a 445,6 m en 9M-2025 (−6,4 %)", "Análisis!C28, C60", "[zoetis-10q-2026-q3.txt, PDF p. 3]"),
    ("Margen EBIT", "2025: 37,8 % (Historia)", f"LTM a 30-sep-2026: {pct(d['ebit_ltm'] / d['revenue_ltm'])} (EBIT {es(d['ebit_ltm'])} ÷ ingresos {es(d['revenue_ltm'])}); 9M-2026 con 142 de reestructuración y 78 de deterioro de I+D en curso", "(evidencia de C27)", "[zoetis-10q-2026-q3.txt, PDF p. 3, 10 y 15]"),
    ("Guía 2026", "6-ago-2026: ingresos 9.120–9.320; orgánico (3)%–(1)%; BPA ajustado 6,15–6,25 (primer tiempo; «−3 % a −1 %» de la etapa 1)", "5-nov-2026: ingresos 9.220–9.320; orgánico (2)%–(1)%; BPA ajustado 6,25–6,35; beneficio neto ajustado 2.600–2.640 (guía de la dirección, no hecho)", "—",
     "sección 5 de este extracto [zoetis-3q2026-press-release.txt, PDF p. 1; zoetis-3q2026-financial-results.txt, PDF p. 16 y 18]"),
    ("Escenarios y precio de Sí", "malo ≈48,7–49 USD, normal ≈90,9–91, bueno ≈120,2, ponderado ≈88,3 (etapa 1); los del primer tiempo los calculó el libro con el precio de 73,08", "sin cifra vigente: los calcula el libro (precio_de_si.py) tras las fases del segundo tiempo", "Análisis (escenarios)", "—"),
    ("Valor intrínseco externo (C38) y P/FCF histórico (C88)", "197,36 USD (Simply Wall St) y 47,1x (Digrin)", "sin valor vigente verificado: «Dato no verificable» (terceros sin bytes), como en el primer tiempo", "Análisis!C38, C88", "registro de entradas (lecturas externas)"),
]
for fila in filas:
    assert len(fila) == 5 and all(isinstance(x, str) for x in fila), fila
assert es((CAP + 7716) / d["ebitda_ltm"], 6) == "11,109987"
tabla = "\n".join("| " + " | ".join(f) + " |" for f in filas)
bloque0 = f"""## 0. Vigencia al 5-nov-2026 de las cifras heredadas de la etapa 1 y del primer tiempo (zoetis_t2, Claude orquestación, 19-nov-2026)

Los textos heredados de la etapa 1 (sección 6 de `datos_v63.md`, `etapa1/Zoetis_respuesta.md`, observaciones del Control maestro) y las secciones 1 a 9 de este extracto (primer tiempo, 9-oct-2026) **no se han tocado** y citan cifras que hoy valen otra cosa. Esta tabla da, para cada una, el valor vigente al 5-nov-2026 (segundo tiempo), su celda y su fuente. Manda la columna «vigente al 5-nov-2026». Bloque de la orquestación (rastro: `resultados/extracto_zoetis_t2.json`): cada cifra del T3 se comprobó en texto/ antes de escribirla.

| Cifra | Etapa 1 o primer tiempo (zoetis_t1d) | Vigente al 5-nov-2026 | Celda | Fuente |
|---|---|---|---|---|
{tabla}

Se conserva del primer tiempo:
- Minoritarios (Historia fila 26): 2022 y 2023 impresos «(2)» y «(6)» (patrimonio negativo de minoritarios) → 0 (decisión Z-MIN de la persona, 19-nov-2026); 2018 = 0 («—» impreso en el 10-K 2018 PDF p. 73). El balance del 30-sep-2026 imprime «—» [zoetis-10q-2026-q3.txt, PDF p. 5].
- Reparto geográfico de la r mínima (Palancas A28:B33; decisión Z-R, 19-nov-2026: se deja y se anota): «Región · Asia» incluye «Other emerging markets» (913 mm, que no son solo Asia) y «Región · Australia & New Zealand» incluye «Other developed markets» (641 mm) y «Contract manufacturing & human health» (116 mm): las etiquetas del modelo no son las del informe [zoetis-10k-fy2025.txt, PDF p. 77].
- C24, C33, C40 y C42 son aproximaciones declaradas (LTM con la «Fiscal Year Alignment»: la nota 2 del 10-Q T3 da el 9M-2025 «as previously reported» para el BAI, los impuestos y el CFO, pero no para intereses, D&A, capex ni arrendamientos financieros [zoetis-10q-2026-q3.txt, PDF p. 10–11]), no derivados exactos.

Evidencia preparada para las celdas de las fases (columna M del Control maestro; datos, no juicio):
- C25 (¿el FCF crece de forma sostenida?): {EV['Análisis!C25']['M']}
- C27 (evolución de los márgenes): {EV['Análisis!C27']['M']}
- C76 (exceso de caja; lo decide la fase B): {EV['Análisis!C76']['M']}

"""
# (c) guía al principio de la sección 5
i5 = viejo.index("## 5. Guía y objetivos de la dirección\n\nTodo lo de esta sección es guía o intención, no hecho.\n")
fin5 = i5 + len("## 5. Guía y objetivos de la dirección\n\nTodo lo de esta sección es guía o intención, no hecho.\n")
guia = """
- **Guía anual de 2026 vigente: la del 5-nov-2026** (guía; tipos de cambio del 20-oct-2026), que «estrecha» los ingresos y «sube» el BPA ajustado frente a la del 6-ago-2026 (la del punto siguiente) [zoetis-3q2026-press-release.txt, PDF p. 1; zoetis-3q2026-financial-results.txt, PDF p. 16 y 18]:
  - Ingresos: 9.220 a 9.320 (antes 9.120 a 9.320); crecimiento orgánico operativo (2)% a (1)% (antes (3)% a (1)%).
  - Coste de ventas ajustado: ≈ 29,0 % de los ingresos (sin cambio). SG&A ajustado 2.340 a 2.370 (antes 2.330 a 2.380). I+D ajustada 705 a 715 (antes 720 a 730). Intereses y otros ajustados ≈ 215 (sin cambio). Tipo impositivo sobre el resultado ajustado ≈ 20 % (antes ≈ 20,5 %).
  - Beneficio neto ajustado 2.600 a 2.640 (antes 2.570 a 2.620); crecimiento orgánico operativo (7)% a (5)% (antes (9)% a (5)%). Beneficio neto reportado 2.300 a 2.340.
  - BPA diluido ajustado 6,25 a 6,35 (antes 6,15 a 6,25); reportado 5,50 a 5,60 (antes 5,55 a 5,65). Partidas significativas y costes de adquisiciones y ventas ≈ 210 (antes ≈ 150).
  - Lo que dice la dirección del trimestre: «Our third-quarter performance was in line with our expectations» [zoetis-3q2026-press-release.txt, PDF p. 1]. No hay transcripción de la conferencia del T3 en las fuentes: los supuestos de la guía del 5-nov-2026 no se conocen más allá del comunicado y la presentación.
  - Lanzamientos que la empresa espera (guía): aprobación de Cytopoint de acción prolongada en EE. UU. en el T4 de 2026 y aprobación de Simparica Duo antes de fin de año («ahead of schedule») [zoetis-3q2026-financial-results.txt, PDF p. 10 y 11].
- La guía siguiente es la del primer tiempo, **sustituida** por la del 5-nov-2026:"""
# (d) sección 10
s10 = f"""

## 10. Segundo tiempo: tercer trimestre de 2026 (10-Q, comunicado y presentación del 5-nov-2026)

Hechos publicados hasta el 5-nov-2026; donde actualizan una cifra de las secciones 1 a 9, mandan estos.

### 10.1 Ingresos, segmentos y precio

- Ingresos del T3 2026: 2.391 frente a 2.422 (−1 % reportado, −2 % operativo, −1 % orgánico operativo); nueve meses 7.121 frente a 7.094 (plano reportado, −1 % operativo) [zoetis-10q-2026-q3.txt, PDF p. 3 y 29; zoetis-3q2026-financial-results.txt, PDF p. 8]. El 9M-2025 está reexpresado (FYA); «as previously reported» 7.080 [zoetis-10q-2026-q3.txt, PDF p. 10].
- Componentes del crecimiento operativo del T3 (aproximados): volumen de franquicias clave −1 %; precio −1 % («lower net price realization»); venta de MFA −1 %; otros productos en línea +1 % [zoetis-10q-2026-q3.txt, PDF p. 29–30]. Nueve meses: franquicias clave −2 %, otros en línea +1 % [zoetis-10q-2026-q3.txt, PDF p. 30]. La presentación lo resume como «0% Volume | (1)% Price» orgánico [zoetis-3q2026-financial-results.txt, PDF p. 3].
- Segmentos del T3: EE. UU. 1.246 frente a 1.322 (−6 %): animal de compañía 980 frente a 1.069 (−8 %), ganado 266 frente a 253 (+5 %); Internacional 1.116 frente a 1.074 (+4 %; +3 % operativo; +4 % orgánico) [zoetis-10q-2026-q3.txt, PDF p. 33; zoetis-3q2026-financial-results.txt, PDF p. 8]. Nueve meses: EE. UU. 3.602 frente a 3.861 (−7 %; compañía 2.889 frente a 3.218, −10 %); Internacional 3.438 frente a 3.144 (+9 %; +5 % operativo), ayudado por los cambios operativos de la FYA [zoetis-10q-2026-q3.txt, PDF p. 33 y 36].
- Causa que da la empresa en EE. UU. animal de compañía: «softer end-market demand and an increasingly competitive landscape»; presión competitiva y sensibilidad al precio en dermatología, genéricos de Convenia y Cerenia y menores ventas de vacunas y Librela, compensado en parte por diagnóstico [zoetis-10q-2026-q3.txt, PDF p. 35].
- Margen bruto por segmento: T3 EE. UU. 82,2 % frente a 83,2 %; Internacional 68,9 % frente a 68,2 %; nueve meses EE. UU. 82,5 % frente a 83,7 %, Internacional 70,3 % frente a 69,5 % [zoetis-10q-2026-q3.txt, PDF p. 34–35]. Resultado de segmento del T3: EE. UU. 830 frente a 899; Internacional 600 frente a 563 [zoetis-10q-2026-q3.txt, PDF p. 34].
- Franquicias del T3 (orgánico operativo): dermatología clave 396 frente a 469 (−16 %); anticuerpos para el dolor artrósico 137 frente a 134 (+2 %; caninos 96, −3 %; felinos 41, +17 %); diagnóstico de compañía 122 frente a 108 (+13 %); franquicia Simparica 358 frente a 351 (+1 %), Simparica Trio 293 frente a 280 (+4 %) [zoetis-3q2026-financial-results.txt, PDF p. 19].
- Cuotas que publica la empresa (Kynetec, canal de clínica, pacientes caninos): la pérdida de cuota en dermatología en EE. UU. se frenó a 4 puntos en el T3 frente a 7 en el T2; cuota actual ≈ 80 %; Simparica Trio ≈ 23 % de cuota mientras las visitas por pulgas, garrapatas y gusano del corazón cayeron ≈ 11 % [zoetis-3q2026-financial-results.txt, PDF p. 4 y 10].
- Por país (T3, orgánico operativo): China +14 %, Alemania −15 %, Japón −18 %, Reino Unido −4 % [zoetis-3q2026-financial-results.txt, PDF p. 20]. EE. UU. nueve meses 3.602 frente a 3.861; China 186 frente a 173 [zoetis-10q-2026-q3.txt, PDF p. 12].
- Moneda: ≈ 45 % de los ingresos de nueve meses en divisas y ≈ 55 % en dólares; el cambio sumó ≈ 1 % [zoetis-10q-2026-q3.txt, PDF p. 28].

### 10.2 Resultados, márgenes y partidas no recurrentes

- Beneficio neto del T3 591 frente a 721 (−18 %); nueve meses 1.883 frente a 2.049; BPA diluido 1,44 frente a 1,63 (nueve meses 4,51 frente a 4,60) [zoetis-10q-2026-q3.txt, PDF p. 3]. Ajustado: 720 frente a 754 (nueve meses 2.147 frente a 2.178); BPA ajustado 1,75 frente a 1,70 (nueve meses 5,14 frente a 4,89) [zoetis-10q-2026-q3.txt, PDF p. 38].
- Partidas significativas antes de impuestos de nueve meses: 241 (reestructuración y programa de costes 125; deterioros 89; transformación de procesos 18) frente a 62 [zoetis-10q-2026-q3.txt, PDF p. 39]; reestructuración en la cuenta de resultados 142 frente a 34 [zoetis-10q-2026-q3.txt, PDF p. 3]; deterioro de I+D en curso de PetMedix 78 en «Other (income)/deductions» [zoetis-10q-2026-q3.txt, PDF p. 15]. Ingresos por intereses 54 frente a 69 [zoetis-10q-2026-q3.txt, PDF p. 15].
- Coste de ventas: 29,2 % de los ingresos en el T3 frente a 28,8 %; 28,3 % frente a 27,9 % en nueve meses. Margen antes de impuestos de nueve meses 33 % frente a 36 %. Tipo efectivo 20,0 % frente a 20,3 % [zoetis-10q-2026-q3.txt, PDF p. 29]. Margen bruto ajustado del T3 71,0 % frente a 71,3 % [zoetis-3q2026-financial-results.txt, PDF p. 9]. I+D de nueve meses 527 frente a 503 [zoetis-10q-2026-q3.txt, PDF p. 3].
- Doce meses a 30-sep-2026 (LTM = 2025 − 9M-2025 + 9M-2026, aproximación por la FYA): ingresos {es(d['revenue_ltm'])}, BAI {es(d['bai_ltm'])}, EBIT {es(d['ebit_ltm'])}, EBITDA {es(d['ebitda_ltm'])}, beneficio neto {es(d['ni_ltm'])}, CFO {es(d['cfo_ltm'])}, capex {es(d['capex_ltm'])} [zoetis-10k-fy2025.txt, PDF p. 66 y 70; zoetis-10q-2026-q3.txt, PDF p. 3, 8, 10 y 11].

### 10.3 Caja, capex e inversión

- Nueve meses: CFO 1.880 frente a 2.056; capex 334 frente a 462; adquisiciones 155 (VitalRADS) frente a 10; compra de inversiones 210 [zoetis-10q-2026-q3.txt, PDF p. 8]. La presentación: ≈ 525 de I+D y ≈ 335 de capex en el año hasta septiembre [zoetis-3q2026-financial-results.txt, PDF p. 15].
- VitalRADS (teleradiología veterinaria), comprada en el T3, sin impacto material (precio no publicado); añade 107 de goodwill [zoetis-10q-2026-q3.txt, PDF p. 14 y 20]. Neogen (genómica animal): cierre esperado a principios de 2027, con las revisiones de la competencia de Australia y Nueva Zelanda en curso [zoetis-10q-2026-q3.txt, PDF p. 14].
- Sistema: en el T3 empezó a usar partes de un ERP nuevo, que sustituirá sus sistemas financieros en varios años [zoetis-10q-2026-q3.txt, PDF p. 46].

### 10.4 Financiación y retornos al accionista

- Balance a 30-sep-2026: caja 1.333 (2 restringida), inversiones a corto 200, porción corriente de la deuda 750, deuda a largo 8.299, patrimonio 3.303, sin dividendos a pagar; pasivos por arrendamiento operativo no corrientes 188 [zoetis-10q-2026-q3.txt, PDF p. 5]. Valor razonable de la deuda a largo 8.115 [zoetis-10q-2026-q3.txt, PDF p. 17]. El bono de 750 al 3,000 % vence el 12-sep-2027 [zoetis-10q-2026-q3.txt, PDF p. 44].
- Covenant (deuda neta ÷ EBITDA ≤ 3,50 a 1) cumplido a 30-sep-2026; la línea de crédito de 1.250, sin disponer, se prorrogó hasta el 27-ago-2031; otras líneas 46 sin disponer [zoetis-10q-2026-q3.txt, PDF p. 42]. Rating sin cambios: Moody's A3 estable (última acción enero de 2025); S&P BBB+ estable (abril de 2025) [zoetis-10q-2026-q3.txt, PDF p. 44].
- Recompras de nueve meses: 17,7 millones de acciones por 1.659 (sin 16 de impuesto especial); quedan 770 del programa de 6.000 [zoetis-10q-2026-q3.txt, PDF p. 44]; en el T3, 6.685.325 acciones a un precio medio de 74,77 USD [zoetis-10q-2026-q3.txt, PDF p. 47]. Pagadas en efectivo: recompras 1.690 y dividendos 666 [zoetis-10q-2026-q3.txt, PDF p. 8]; dividendos declarados por acción 1,060 en nueve meses [zoetis-10q-2026-q3.txt, PDF p. 3]. La empresa: 2.400 devueltos al accionista en el año y «Expected to maintain or grow dividend» (guía) [zoetis-3q2026-financial-results.txt, PDF p. 15].
- Acciones en circulación: 407.487.227 a 30-sep-2026 y 406.316.147 a 30-oct-2026 [zoetis-10q-2026-q3.txt, PDF p. 5 y 1]; media diluida del T3 411,6 millones [zoetis-10q-2026-q3.txt, PDF p. 3].

### 10.5 Demanda colectiva de accionistas (hecho; resultado incierto)

- El 27-may-2026 se presentó en Nueva York una demanda colectiva de valores contra la empresa y algunos directivos (City of Ann Arbor Retiree Health Care Benefit Plan & Trust v. Zoetis Inc., S.D.N.Y.), por compradores entre el 14-ene-2025 y el 6-may-2026, por declaraciones supuestamente falsas o engañosas sobre la seguridad, la posición competitiva y la cuota de Librela, Simparica Trio, Apoquel y Cytopoint; pide daños sin cuantificar [zoetis-10q-2026-q2.txt, PDF p. 23].
- Sigue en el 10-Q del T3: el 23-oct-2026 los demandantes principales presentaron una demanda modificada que añade a quienes operaron con opciones, nombra a la consejera delegada, al ex director financiero y al director comercial, y alega además un plan para ocultar la caída de la demanda de esos productos; está en fase inicial y la empresa aún no ha contestado. Las demandas derivadas de junio de 2026 están acumuladas en dos tribunales (S.D.N.Y. 1:26-cv-04709 y D.N.J. 2:26-cv-07479) [zoetis-10q-2026-q3.txt, PDF p. 24]. Ningún documento da un importe estimado de pérdida.
- Dirección: con la salida del director financiero en agosto de 2026, la consejera delegada pasó a ser la máxima responsable de las decisiones operativas (CODM) desde el 17-ago-2026 [zoetis-10q-2026-q3.txt, PDF p. 24].

### 10.6 Lo que no encontré en el tercer trimestre

- Transcripción de la conferencia de resultados del T3 (no está en las fuentes) y, con ella, los supuestos de la guía del 5-nov-2026 y el precio esperado para el año.
- Balance del 30-sep-2025 (el 10-Q del T3 no lo publica): no hay comparación interanual de balance (C24, C31).
- 10-K 2025 reexpresado por la FYA (la empresa lo reexpresará al presentarlo como comparativo) [zoetis-10q-2026-q3.txt, PDF p. 10]: el LTM mezcla bases.
- Resultado de la prueba anual de deterioro del goodwill de 2026.
- Precio de VitalRADS y de la genómica de Neogen.
- Arrendamientos corrientes y financieros a 30-sep-2026 (el balance del 10-Q no los desglosa).
- Guía de capex de 2026.
"""
nuevo = cab + "\n\n" + bloque0 + viejo[i_1:fin5] + guia + viejo[fin5:].rstrip("\n") + "\n" + s10
# comprobación: las secciones 1–9 del primer tiempo siguen enteras (solo se intercala la guía al principio de la 5)
assert nuevo.replace(guia, "", 1).find(viejo[i_1:].rstrip("\n")) > 0
open(ex, "w", encoding="utf-8").write(nuevo)
json.dump({"fecha": "2026-11-19", "autor": "Claude orquestación", "guion": "resultados/scripts/extracto_zoetis_t2.py", "antes_sha256": h(copia), "despues_sha256": h(ex),
           "antes": os.path.relpath(copia, os.path.dirname(C)), "frases_comprobadas_en_texto": n_fr, "filas_de_vigencia": len(filas),
           "cambios": ["cabecera (fecha de análisis y fuentes)", "bloque 0 sustituido (vigencia al 5-nov-2026 y evidencia preparada de C25, C27 y C76)",
                       "sección 5: guía del 5-nov-2026 al principio; la del 6-ago-2026 queda como sustituida", "sección 10 nueva (tercer trimestre)"],
           "secciones_1_a_9": "sin cambios (se intercala la guía del 5-nov-2026 al principio de la sección 5)"},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("extracto escrito:", h(ex), "frases comprobadas", n_fr, "filas", len(filas))
