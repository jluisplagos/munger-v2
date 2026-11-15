# Matriz de coherencia · ventana 2023–2025 de Vidrala (entrega 4.3; armonizada en la 4.3.1)

Cada celda se ha comprobado con `scripts/revision_financiera_vidrala.py` (secciones 2, 3 y 5), contra el texto de la página citada y, para 2024 y 2025, contra el ESEF 2025 completo.

**Siglas de los documentos:**
- **ES24:** informe 2024, español, doc. 2118. Prevalece sobre la traducción.
- **EN23 · EN24 · EN25:** informes inglés de 2023 (doc. 1831), 2024 (doc. 2145) y 2025 (doc. 2355).
- **ESEF:** doc. 2311, conservado entero en `fuentes/esef_2025_completo/`.

**Perímetro:**
- **C:** operaciones continuadas.
- **C+I:** incluye Italia (discontinuada).
- **Cons.:** consolidado, que en 2025 equivale a continuadas.

**Estado:**
- **Documentada:** la cifra está en la fuente con la definición de la fila.
- **Discrepante:** el libro no coincide con la fuente.
- **Perímetro mixto:** la cifra es correcta, pero su perímetro no es el de las demás entradas con las que se combina.
- **Derivada:** cálculo con datos publicados y un residuo no publicado.
- **Hipótesis:** sin respaldo directo.

## 1. Entradas de la ventana (Historia, columnas J–L)

| Año | Entrada (fila) | Libro (mm) | Fuente | Perímetro | Definición | Estado | Canal hacia `f` |
|---|---|---|---|---|---|---|---|
| 2023 | Ventas (6) | 1.427,473 | ES24 p.11 (2023 reexpresado) | C | Ventas de la cuenta de resultados | Documentada | C74 (V) |
| 2023 | EBIT (7) | 267,508 | ES24 p.11 | C | Resultado de explotación | Documentada | C75 (NOPAT) |
| 2023 | D&A (8) | 87,21 | ES24 p.14 | C | Amortizaciones del estado de flujos | Documentada (la cita del expediente es p.4; P8) | **C76 (reinversión)** |
| 2023 | Tipo (10) | 0,204 | ES24 p.11: 54.813 ÷ 268.649 = 0,20403 | C | Impuesto ÷ BAI de continuadas, a cuatro decimales | Documentada | C75 |
| 2023 | CFO (11) | 263,437 | ES24 p.14 (= EN23 p.7) | **C+I** (Italia: +26,732 de explotación, ES24 p.43) | Flujo neto de explotación | Perímetro mixto | C46 → C70 |
| 2023 | Capex (12) | 151,7 | ES24 p.14: 143,848 + 7,852 | **C+I** (altas de Italia 4,315, EN23 p.30) | Pagos por inmovilizado material e intangible | Perímetro mixto (se anula en `f`) | C47 y C76 |
| 2023 | Circulante (14) | 78,805 | ES24 p.14 | **C+I** y 11,061 de ajustes no monetarios de Italia | «Efectivo generado por las operaciones», cambiado de signo | Perímetro mixto; coherente con su CFO | C76 |
| 2024 | Ventas (6) | 1.588,267 | ES24 p.11; ESEF | C (con un segmento «Italia» de 17,016, ES24 p.37) | Ventas | Documentada | C74 |
| 2024 | EBIT (7) | 331,008 | ES24 p.11; ESEF | C (segmento «Italia» con BAI de 2,139) | Resultado de explotación | Documentada | C75 |
| 2024 | D&A (8) | 117,72 | ES24 p.14; ESEF | C | Amortizaciones | Documentada (P8) | C76 |
| 2024 | Tipo (10) | 0,2143 | 64.968 ÷ 303.218 = 0,21426 | C | Impuesto ÷ BAI de continuadas | Documentada | C75 |
| 2024 | CFO (11) | 362,516 | ES24 p.14; ESEF | **C+I** (Italia: +11,558 de explotación) y el beneficio incluye 60,065 de discontinuadas | Flujo neto de explotación | Perímetro mixto | C46 → C70 |
| 2024 | Capex (12) | 168,8 | 160,063 + 8,737; ESEF | Puede incluir Italia del 1S (no publicado) | Pagos por inmovilizado | Perímetro dudoso (se anula en `f`) | C47 y C76 |
| 2024 | Circulante (14) | **−127,840** | Fuente: **84,994** (ES24 p.14) | **C+I**, con la reversión de la plusvalía (≈50,5) por eliminación | Ídem | **Discrepante** (P1, corrección factual) | C76 |
| 2025 | Ventas, EBIT, D&A y tipo | 1.465,16 · 292,068 · 132,948 · 0,2433 | EN25 p.4 y p.7; ESEF | Cons. = C | Ídem | Documentadas | C74, C75 y C76 |
| 2025 | CFO (11) | 380,287 | EN25 p.7; ESEF | Cons. | Ídem | Documentada | C46 |
| 2025 | Capex (12) | 188,503 | 178,746 + 9,757; ESEF | Cons. | Ídem | Documentada | C47 y C76 |
| 2025 | Circulante (14) | −0,799 | EN25 p.7 | Cons. | Ídem | Documentada | C76 |

## 2. Entradas agregadas de `Análisis` y de `Historia`

| Celda | Libro | Qué es | Perímetro | Estado | Tratamiento coherente propuesto |
|---|---|---|---|---|---|
| C46 | 335,4 | Media del CFO 2023–2025 | C+I en 2023–2024 | Perímetro mixto | **Motor A:** 322,65 = media de (CFO − explotación de Italia), con CFO y nota 5. **Motor B:** sin uso en el valor |
| C47 | 169,7 | Media del capex | C+I en 2023 (y quizá 2024) | Perímetro mixto | **Motor A:** no determinable con evidencia; `f` no depende de C47 si la fila 12 se mantiene igual. **Motor B:** sin uso en el valor |
| C48 | 0 | Intereses en financiación | — | Cero heredado. Evidencia candidata: intereses pagados en explotación (EN25 p.7; ESEF). La IA no confirma el cero (piloto, P4) | Sin cambio |
| C49 | 4,5 | Arrendamientos (principal) | — | **Hipótesis pendiente** = media de (pagos − interés devengado) | **Motor A:** 4,5 con recorrido de 0 a 6,8. **Motor B:** sin uso; los arrendamientos van como deuda (L23) |
| C50 | 0 | SBC | — | Cero heredado, no contrastado en esta revisión | Sin cambio |
| C52 → C70 | 161,2 | FCF base | Mixto | Perímetro mixto | **Motor A:** el nivel de continuadas no es determinable (réplica condicionada ≈149,9). **Motor B:** sin uso en el valor |
| C57 | 3 | Ventana | — | Convención | Sin cambio (§3 del informe) |
| C58 | 0,0199 | `f` | Mixto y con P1 | **Artefacto** | **Motor A:** −0,009847, condicionada a los supuestos de T3 (δ = 0 es una hipótesis; circulante derivado, no publicado). Es la variante más coherente del motor A, solo como contraste. **Motor B:** 0 por construcción |
| C53 | 1,549 | S2C marginal de referencia | G6 con Italia; J31 con Brasil; K31 con P1 y el cobro de Italia | Discrepante (por P1) y de perímetro mixto | Con P1: 0,916. Sigue mezclando perímetros: es una referencia para la fase B, no un dato |

## 3. Entradas del motor B y de la lectura de precio (revisado en la 4.3.1)

Clases: **L** localizada, **C** contrastada (cifra y definición), **D** derivada por convención, **H** hipótesis pendiente, **A** dato o confirmación ausente. La tabla completa, con fechas, está en `ENTRADAS_Y_FECHAS.md`, §2.

| Celda | Libro | Fecha | Fuente | Clase |
|---|---|---|---|---|
| L22 | 213,613 | 31-dic-2025 | EN25 p.3: préstamos 196,080 + 66,833 = 262,913, arrendamientos incluidos; menos L23 | C |
| L23 | 49,3 | 31-dic-2025 | EN25 p.52, nota 8 | C |
| L24 | 108,352 | 31-dic-2025 | EN25 p.2 y p.7; ESEF | C como saldo · H como caja disponible (dividendo a cuenta de 43,338 aprobado el 19-dic-2025 y pagado el 13-feb-2026, EN25 p.64) |
| L25 | 6,223 | 31-dic-2025 | EN25 p.71: provisión «Personnel» (prestación definida «y otras obligaciones con empleados», p.72) | C como provisión · H como «déficit neto de pensiones» · A el déficit neto |
| L26 | 0 | 31-dic-2025 | EN25 p.3: el balance no presenta línea de minoritarios | L (cero heredado) · A la confirmación humana (la IA no confirma ceros) |
| L15 · C63 | 20,8 · 0,0634 | 2025 | EN25 p.7; ESEF; fórmula del libro | C (intereses pagados) · D (i, aproximación histórica, convención 4) |
| C64 | 262,913 | 31-dic-2025 | L22 + L23 | C |
| C37 | 87,9 | 3-nov-2026, intradía | Control maestro: Bolsamanía, un solo proveedor | L · A el cierre oficial y el estado con o sin derecho |
| C55 | 35,206 | 31-dic-2025 | EN25 p.60 y p.76 | C para 2025 · H para la fecha del precio · A las acciones en circulación a 3-nov-2026 |
| C41 | 3.094,6 | Mezcla | C37 × C55 | D · H su idoneidad (fechas y acciones de bases distintas) |
| `r_op` | 0,0869 | Mezcla | Convención 4 | D (tasa personalizada; E de 2026, D de 2025) |

## 4. Ajustes: cuáles se calculan con evidencia y cuáles exigirían hipótesis

| Ajuste | Con evidencia | Cálculo | Hipótesis que quedaría |
|---|---|---|---|
| Circulante de 2024 del mismo estado que su CFO (P1) | **Sí** | 84,994 (ES24 p.14) | Ninguna |
| Discontinuadas fuera del flujo antes de circulante | **Sí** | 19,559 (2023) y 60,065 (2024); ES24 p.11 y p.14 | Ninguna |
| Plusvalía dentro de las discontinuadas de 2024 | **Sí** | 60,065 − 9,518 = 50,547 (nota: «50 millones») | Ninguna |
| CFO de continuadas | **Sí** | CFO − explotación de Italia (26,732; 11,558; ES24 p.43) | Que la explotación de Italia de la nota 5 sea la parte exacta de Italia en el CFO consolidado (es la definición de NIIF 5) |
| Circulante de continuadas | **No publicado** | Derivado (residuo, no cifra publicada): 85,978 (2023) y 36,487 (2024) | **δ = 0 (hipótesis):** la parte de Italia en los intereses e impuestos pagados del grupo no se publica. La sensibilidad condicionada T3δ (δ igual a lo devengado por Italia) da −0,0009 de `f`. No es una cota del pago |
| Capex de continuadas | **No** | — | El capex de Italia en caja de 2023 (solo hay altas por devengo: 4,315) y el del 1S 2024 (no publicado) |
| Normalizar impuestos y partidas no monetarias | **No** | T4 (contraste) | Que el impuesto corriente no pagado y las provisiones no se repitan (recurrencia no acreditada, pero tampoco descartada; evidencia necesaria en el informe, §3.6). Que los intereses futuros sean los de la ventana |
| Arrendamientos (C49) | **No** | 4,5 · 6,8 · 0 | La clasificación de los pagos (preguntas 1–3) |

## 5. Comparabilidad histórica tras la venta de Italia

- **2016–2022 (columnas C–I):** consolidadas con Italia y sin reexpresar. Ninguna de estas columnas entra en `f` (C57 = 3). Sí entran en la media de márgenes (m0), en los CAGR, en el S2C de referencia, en el ROIC medio y en τ (cinco años: 2021–2025).
- **2023:** continuadas en la cuenta de resultados; estado de flujos con Italia. Brasil solo desde el 4-dic-2023: ventas de 19,1 frente a 155,0 pro forma (EN25 p.29).
- **2024:** continuadas en la cuenta de resultados, con un segmento «Italia» pequeño. Estado de flujos con Italia en el primer semestre y con la plusvalía.
- **2025:** primer año con perímetro homogéneo (sin Italia y con Brasil completo). Toro entra en 2026 (consolidada desde el 30-mar-2026, según el Control maestro heredado).
- **2026, hasta la fecha del precio:** Toro, dividendos, recompras, la liberada 1×20, la nueva deuda y Kristin. Ninguno entra en la base 2025 (`ENTRADAS_Y_FECHAS.md`, §5).
