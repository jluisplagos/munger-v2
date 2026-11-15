# Elis · extracción para el cambio de base E6 (base 31-dic-2025)

- **Quién:** extractor E6, agente Claude, 14-nov-2026. No es el revisor y no es una revisión humana.
- **Qué se ha hecho:** solo leer y preparar.
  - No se ha ejecutado `cambiar_base.py`, `pipeline.py` ni LibreOffice.
  - No se ha modificado nada dentro de `E414/elis_motor_A`.
  - Los libros se han leído con openpyxl en solo lectura: `Elis_v63_datos.xlsx`, `Elis_v63_evaluada.xlsx` y `etapa1/Elis_evaluada.xlsx`.
  - Scripts auxiliares (`python3 -B`) en el scratchpad: `…/scratchpad/pg.py` imprime páginas y `…/scratchpad/e6/hacer_cambio.py` genera el JSON.
- **Abreviaturas:**
  - PV = `/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2`.
  - E414 = `PV/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14`.
  - Expediente = `E414/elis_motor_A/Elis`.
  - «URD 2025» = `texto/Elis - 2025 Universal Registration Document.txt`, edición inglesa. Su PDF tiene sha256 `04bfd087…cd62e`.
  - Las páginas son siempre de **PDF**, con el folio impreso entre paréntesis.
- **Etiquetas:** cada apartado separa **Hechos** (cita literal), **Interpretación** y **Propuesta**.

---

## 0. Resumen de cifras propuestas

| Entrada | Libro actual | Propuesta (base 31-dic-2025) | Fuente |
|---|---|---|---|
| C55 acciones | 259,077654 (media ponderada del BPA diluido de 2025) | **232,476810** M en circulación = 232.848.588 − 371.778 | URD 2025 p. 394, 439, 441 |
| C41 capitalización | 6.264,5 | **5.621,2892658** = 24,18 × 232,47681 | derivada |
| C37 precio | 24,18 (4-nov-2026) | sin cambio | Euronext, histórico no ajustado |
| C48 intereses | 108,0 | **sin cambio** (incluye el cupón de la OCEANE, que es lo coherente con esta base) | DEU 2024 p. 273; URD 2025 p. 327, 366 |
| OCEANE como deuda (L22) | dentro de 3.418,3 | sin cambio: componente de deuda 362,0 (364,4 con el interés devengado) | URD 2025 p. 382–384 |
| I25:L25 pensiones | 50,7 / 78,3 / 104,1 / 79,7 | **47,4 / 74,9 / 91,6 / 67,1** | URD 2023 p. 307; DEU 2024 p. 301; URD 2025 p. 355 |
| C46 / C47 / C50 | 1.429,4 / 857,1 / 28,2 | sin cambio; solo se describen (no hay decisión) | — |
| Dilución potencial (aparte) | — | OCEANE 23.355.764; acciones de rendimiento 2.613.905 (hasta 3.136.686) | URD 2025 p. 380, 360, 361, 439 |

---

## 1. Acciones a 31-dic-2025 (C55)

### Hechos

**Acciones emitidas a 31-dic-2025: 232.848.588.**
- URD 2025 p. 394 (folio 392), nota 10.1 «Changes in share capital»:
  - «NUMBER OF SHARES AS AT DECEMBER 31, 2025 232,848,588»
  - «Number of shares issued and fully paid up 232,848,588»
  - «Treasury shares 371,778»
- URD 2025 p. 416, nota de la sociedad matriz: «As at December 31, 2025, share capital is divided into 232,848,588 fully paid-up common shares with a par value of €1.00 each.»
- URD 2025 p. 437 (folio 435), historia del capital: «AS AT 12/31/2025 232,848,588».
  - Movimientos de 2025: +889.250 por «Elis for All 2025» (13-nov-2025) y −4.705.107 por amortización de acciones propias.
  - Cuadra: 236.664.445 + 889.250 − 4.705.107 = 232.848.588.
  - El cuadro fecha la amortización el «11/23/2025». Las p. 394 y 440 dicen «December 23, 2025». Es una incoherencia de fecha dentro del documento; no cambia el número.

**Acciones propias a 31-dic-2025: 371.778.** Tres sitios del URD dan la misma cifra:
- p. 394: «Treasury shares 371,778».
- p. 439 (folio 437), cuadro de accionistas a 12/31/2025: «Treasury stock(h) 371,778 … 0.16» y «TOTAL 232,848,588». Nota (h): «O/w 131,550 held under the liquidity agreement».
- p. 441 (folio 439): «Treasury shares held directly or indirectly as at December 31, 2025 371,778(b)», con «(b) O/w 131,550 for the liquidity agreement».
- Contrato de liquidez, p. 394: «As at December 31, 2025, 131,550 securities and €2.8 million in liquidity are held under the liquidity agreement». La p. 440 da la misma cifra.

### Conciliación

| Concepto | Acciones |
|---|---|
| Emitidas a 31-dic-2025 | 232.848.588 |
| − Propias | 371.778 |
| — de ellas, contrato de liquidez | 131.550 |
| — de ellas, fuera del contrato | 240.228 |
| **= En circulación a 31-dic-2025** | **232.476.810** (232,476810 M) |

Comprobaciones independientes:
1. **Dividendo propuesto.** p. 395: «€0.48 per share, or €111.6 million, based on the number of existing shares as at December 31, 2025 (excluding treasury shares)».
   - 0,48 × 232.476.810 = 111,589 mm, que redondea a 111,6. Cuadra.
2. **Arrastre hasta 30-jun-2026** con el informe semestral (`fuentes_2026/texto/Elis_2026_half-year_financial_report_EN.txt`):
   - Datos de la p. 46: «bought back 17,787,422 shares», «delivered 1,229,349 shares»; contrato de liquidez del 1 al 8-ene-2026: compra de 48.667 y venta de 64.304.
   - Autocartera a 30-jun-2026, p. 14: «Treasury shares(d) 16,914,214».
   - 371.778 + 17.787.422 − 1.229.349 − (64.304 − 48.667) = 16.914.214. Cuadra exactamente.
   - La p. 46 habla de «the stock of 356,141 shares held outside of the liquidity agreement as at December 31». Esa cifra es 240.228 + 115.913 (las acciones del contrato al cerrarlo el 14-ene-2026). Es coherente.
3. **Diferencia sin explicar en las cuentas de la sociedad matriz.** URD 2025 p. 415, nota 3.9:
   - «Number of treasury shares … 132,480» (inmovilizado financiero) y «… 240,228» (valores negociables), que suman 372.708.
   - Son **930 acciones más** que 371.778. La diferencia está en el bloque del contrato de liquidez: 184.855 + 3.114.060 − 3.166.435 = 132.480, frente a 184.390 + 3.114.060 − 3.166.900 = 131.550 de la p. 440.
   - No he encontrado la explicación. Es inmaterial: 930 × 24,18 ≈ 0,02 mm. Se usa 371.778, la cifra consolidada que aparece en tres sitios.

### Las emitidas a 31-dic-2025 no incluyen acciones de la conversión de 2026

- La última operación de capital de 2025 es la amortización de diciembre (p. 437).
- El informe semestral de 2026 (p. 46) da «Number of shares as at December 31, 2025 232,848,588» y «NUMBER OF SHARES AS AT JUNE 30, 2026 232,848,588».
- Comunicado del 7-oct-2026 (`fuentes_2026/Elis_OCEANE_2029_resultados_conversion.html`, sha256 `f6d6c27f…be7`, que coincide con `HUELLAS.txt`):
  - «…delivery of a total of 23,569,556 Elis shares …, comprising 18,104,556 existing shares held in treasury and 5,465,000 new shares»
  - «The share capital of the Company now amounts to EUR 238,313,588»
  - Cuadra: 232.848.588 + 5.465.000 = 238.313.588.
- Además, p. 439: «The 3,800 OCÉANE 2029 bonds … represent 23,355,764 underlying Elis shares». Son acciones potenciales, no emitidas.

### Diferencias con otras cifras del documento (interpretación)

URD 2025 p. 395, nota 10.3:
- «Weighted average number of shares 233,954,020» (2025)
- «Effect of conversion of convertible bonds 23,355,764»
- «Effect of contingently issuable shares 1,767,869»
- «Weighted average number of shares used for diluted EPS 259,077,654»
- La suma de los componentes da 259.077.653. Es una acción menos que la publicada, por redondeo de la propia tabla.

**Media básica 233.954.020 frente a 232.476.810 en circulación al cierre.**
- La media pondera en el tiempo las compras de 2025 (9.674.415 compradas y 3.166.900 vendidas, p. 441), las entregas, la ampliación del 13-nov y la amortización del 23-dic.
- El URD dice: «The weighted average numbers of shares take into account the withdrawal of 2,711,351 treasury shares in 2025» (p. 395).
- Aproximación: 236.664.445 − 2.711.351 = 233.953.094, a 926 de la cifra publicada. No he reconstruido la ponderación exacta.
- Es una media del ejercicio, no un saldo.

**Media diluida 259.077.654.**
- Es la básica media más las 23,36 M acciones potenciales de la OCEANE más 1,77 M contingentes.
- Con la OCEANE tratada como deuda (decisión E6), incluir esas 23,36 M en el denominador contaría la OCEANE dos veces.
- Además es una media, no las acciones a 31-dic-2025. Por eso no sirve como C55 en esta base.

**Otras cifras del documento:**
- Capitalización de la p. 447: «232,848,588 24.26 5,648.9» (emitidas × precio de cierre de 2025). Sobre las acciones en circulación serían 5.639,9.
- La «Number of shares, basic (C) 234.0 / diluted (D) 259.1» del resultado «headline» (p. 313) son las mismas medias redondeadas.

### Propuesta

- **C55 = 232,476810 M.** Va en `metadatos.acciones_diluidas` del CAMBIO, con fecha 2025-12-31.
- **C41 = 24,18 × 232,47681 = 5.621,2892658 mm.** Va en `metadatos.capitalizacion`, con fecha 2026-11-04. Mezcla precio de 2026 y acciones de 2025, y se declara así.

---

## 2. OCEANE 2029 a 31-dic-2025: pasivo y lugar en el libro

### Hechos (URD 2025)

**Nota 8.5, p. 384 (folio 382):**
- «CONVERTIBLE BONDS 362.0 352.3» (12/31/2025, 12/31/2024)
- «ACCRUED INTEREST 39.0 47.6»
- «BORROWINGS AND FINANCIAL DEBT 3,418.3 3,660.1»
- «NET DEBT 3,020.2»

**Variación de la deuda, p. 382:**
- «CONVERTIBLE BONDS 352.3 0.0 0.0 0.0 0.0 9.7 362.0»: el +9,7 es «Other changes».
- p. 314 lo explica: «Other changes include the revaluation of the debt component of the convertible bond (for -€9.2 million in 2024 and -€9.7 million in 2025)».

**Vencimientos, p. 383:**
- «Convertible bonds 364.4 2.4 362.0 0.0 0.0» (total; 2026; 2027).
- «The table above takes into account the redemption right of holders of 2029 convertible bonds as at September 22, 2027».

**Flujos contractuales, p. 377:**
- «Convertible bonds 364.4 0.0 8.6 0.0 8.6 380.0 8.6 … 380.0 25.7»: valor en libros a coste amortizado e intereses de 8,6 al año.

**Condiciones y contabilidad, p. 380:**
- «€380.0 million»; «annual coupon of 2.25%, payable annually and for the first time on September 22, 2023».
- «The fair value of the debt component of the 2029 OCÉANEs, presented in non-current liabilities, is equivalent to €328.3 million at inception».
- «The options component, presented in equity, was valued at €47.6 million».

**Valor razonable, p. 386:** «Convertible bonds – debt component 366.1» (2025) y «357.6» (2024). Es solo información; no es el importe del balance.

### Interpretación

- El pasivo a 31-dic-2025 es el **componente de deuda a coste amortizado: 362,0 mm**.
- Más **2,4** que vencen en 2026, dentro de la línea «Accrued interest» 39,0. Total **364,4**. Es previsiblemente el cupón devengado desde el 22-sep: 380 × 2,25 % × 100/365 ≈ 2,34. La nota no lo desglosa.
- No es el nominal (380,0) ni el valor razonable (366,1).
- El componente de patrimonio (47,6 al inicio) no es deuda.

### En el libro

- **Historia!L22 = 3.418,3** («Deuda financiera», fila 22): es «BORROWINGS AND FINANCIAL DEBT» de la p. 384. Incluye los 362,0 de la OCEANE y su interés devengado.
- Historia!C64 = 4.121,5 = L22 + L23 (703,2 de arrendamientos).
- El registro de verificación (`Historia!L22`) lo da como verificado y anota «Incluye la OCEANE 2029 (CONVERTIBLE BONDS 362,0 …; 364,4 con intereses)».
- **El libro ya tiene la OCEANE como deuda, por 362,0 (364,4 con el devengado), en L22.** No hace falta cambiar nada.
- El motor A no resta la deuda: lo dice la celda Análisis C54, «El motor A no la resta». Allí la OCEANE actúa solo a través de los intereses (C48).
- Análisis!C54 = 4.816,9 viene de la etapa 1 y es a 30-jun-2026. Ver §8.

### Propuesta

- Sin cambio en la deuda.

---

## 3. C48 (intereses): composición y coherencia con la base

### Hechos (reproducción)

| Año | «Net interest paid» (Historia fila 15) | Pagos de arrendamientos con intereses | Principal de arrendamientos | Intereses de arrendamientos |
|---|---|---|---|---|
| 2023 | 70,5 (DEU 2024 p. 273: «Intérêts financiers nets versés (78,9) (70,5)») | 130,8 (p. 273) | 111,0 (DEU 2024 p. 312: «Paiements du principal … (111,0)») | 19,8 |
| 2024 | 78,9 (URD 2025 p. 327) | 150,8 (p. 327) | 125,0 (URD 2025 p. 366) | 25,8 |
| 2025 | 99,4 (URD 2025 p. 327: «Net interest paid (99.4) (78.9)») | 177,9 (p. 327: «Lease liability payments (including interest on lease liabilities) (177.9) (150.8)») | 148,3 (p. 366: «Principal payments … (148.3)») | 29,6 |

- Media de los intereses netos: (70,5 + 78,9 + 99,4) / 3 = **82,933**.
- Media de los intereses de arrendamientos: (19,8 + 25,8 + 29,6) / 3 = **25,067**.
- **C48 = 108,000**, igual que el libro (108).
- Es la fórmula de `derivacion` del registro y la decisión del inversor del 10-nov-2026 (Control maestro, fila 45).

### ¿Incluye el cupón de la OCEANE?

- **Hecho:** el cupón en efectivo es 2,25 % × 380,0 = **8,55 mm al año**. Se paga el 22-sep desde 2023 (p. 380), y el cuadro de la p. 377 da 8,6 al año.
- **Hecho:** el estado de flujos (p. 327) no lo desglosa. La explicación del URD (p. 312) habla de «financial interest (net of financial income)».
- **Interpretación:**
  - Lo más probable es que el cupón esté dentro de «Net interest paid» en 2023, 2024 y 2025: es interés financiero en efectivo y no figura en otra línea.
  - En C48 serían unos 8,55 de los 108,0 (≈ 2,8 % del FCF base de 308,0).
  - El devengo no monetario del componente de deuda (9,7 en 2025) no es caja y no está en C48.
  - El «Interest expense related to convertible bonds (net of tax) 12.6» de la p. 395 es el ajuste contable del BPA diluido (cupón más devengo, neto de impuestos). No es un flujo de caja.

### Coherencia con la base 2025

- Con la OCEANE como deuda y **sin** sus acciones en el denominador, su cupón es un coste del accionista. **Mantenerlo en C48 es lo coherente**, y el libro ya lo hace así.
- El doble cómputo que señalaba la revisión (cupón dentro de C48 y además las acciones de conversión en C55) desaparece al pasar C55 a 232,48 M.

### Propuesta

- **C48 sin cambio de valor.**
- En el CAMBIO, `evidencia["Análisis!C48"].N` deja escrita esta conciliación en la copia de ensayo de la etapa 1. Es la fila 45 del Control maestro, una fila de dato.
- El texto actual de esa celda, «Si ya están dentro de CFO, clasificar No aplicable…», pasa a antecedentes.

---

## 4. Dilución potencial (aparte; NO entra en el caso base)

### Hechos

**OCEANE 2029, situación a 31-dic-2025** (p. 380):
- «These 3,800 2029 OCÉANEs represented 23,355,764 underlying shares of the Company as at December 31, 2025. This number of shares takes into account the last adjustment of the conversion ratio set at 6,146.2538 shares per bond, from May 28, 2025».
- Cálculo: 3.800 × 6.146,2538 = 23.355.764,4.
- Precio de conversión: 16,27 €.
- p. 439: «The potentially dilutive effect of the OCÉANE 2029 bonds was approximately 10.03% of the Company’s share capital as at December 31, 2025». Cálculo: 23.355.764 / 232.848.588 = 10,03 %.

**OCEANE 2029, conversión real (posterior a la base; no se aplica)**, según el comunicado del 7-oct-2026:
- Relación «6,256.8564 Elis shares per Bond», ajustada «effective May 28, 2026» (informe semestral, p. 15).
- «3,767 Bonds … 99.13%».
- Entrega de 23.569.556 acciones: 18.104.556 propias y 5.465.000 nuevas. Capital resultante: 238.313.588.
- «The remaining 33 Bonds … will be redeemed in cash on October 13, 2026 … aggregate redemption amount of €3,304,271.85».

**Acciones de rendimiento (planes 19–25)**, nota 5.4, p. 360, fila «Number of rights outstanding as at 12/31/2025»:
- Derechos vivos por plan: 0 / 388.960 / 0 / 954.339 / 29.250 / 16.730 / 1.207.746 / 16.880.
- Total: **2.613.905**, la misma cifra que da la p. 439: «2,613,905 rights likely to result in the issue of 2,613,905 new shares».
- Límite máximo, p. 361 (d): «the number of vested shares may not exceed 120% of the shares granted». Con ese límite el máximo sería 3.136.686. Los planes 17, 19 y 20 se consolidaron al 120 % (p. 361 (e)).
- Entrega, p. 439: «all performance shares whose plans expired in 2025 were delivered using existing shares acquired under the current share buyback program, and it is planned to renew this delivery operation in 2026».

**Dilución total y otros instrumentos:**
- p. 439: «The overall potentially dilutive effect … approximately 11.15%». Cálculo: (23.355.764 + 2.613.905) / 232.848.588 = 11,15 %.
- p. 439: «No other securities give access to the Company’s share capital».
- En el BPA diluido, las acciones contingentes ponderadas son 1.767.869 (p. 395).

### Cómo se calcularía, sin contarla dos veces (propuesta de método, no calculada con el motor)

Acciones en cada escenario:

| Escenario | Acciones |
|---|---|
| Caso base (decisión E6) | 232.476.810 |
| Con la conversión de la OCEANE | 232.476.810 + 23.355.764 = 255.832.574 |
| Con la conversión y las acciones de rendimiento | 258.446.479 (258.969.260 con el 120 %) |

**Conversión de la OCEANE.** Se calcularía como variante, en una copia del libro y nunca en el caso base, cambiando a la vez:
- C55 = 255,832574.
- C48 sin el cupón: 108,0 − 8,55 = 99,45. Es antes de impuestos: el URD no publica el efecto fiscal del cupón en caja.
- En el motor B, la deuda sin 362,0 (y sin los 2,4 devengados).

Lo que no puede hacerse es sumar las acciones manteniendo el cupón o la deuda: eso es justo lo que hacía el libro actual.

**Acciones de rendimiento.** Hay dos vías, y no se suman:
- añadirlas al denominador, o
- tratarlas como coste. C50 ya resta la SBC (28,2), que es el gasto NIIF 2 de los planes, incluidos parcialmente los vivos.

Contar a la vez las 2,61 M en el denominador y toda la SBC duplicaría, en parte, el coste de los derechos ya concedidos. Además, si se entregan con acciones recompradas, la dilución se convierte en una salida de caja que el FCF no recoge. La elección queda para la persona responsable.

**Orden de magnitud, solo interpretación:** la conversión añade un 10,05 % de acciones y quita unos 8,55 de 308,0 de FCF base (≈ 2,8 % antes de impuestos). El efecto exacto en el valor solo lo da el motor, y no lo he ejecutado.

---

## 5. Pensiones I25:L25

### Hechos (citas literales, cuadro «FUNDED STATUS OF EMPLOYEE BENEFIT OBLIGATION» de la nota 5.3)

| Celda | Año | Libro: línea (5) | Correcto: línea (3) | Página y cita literal de la línea (3) | (1) − (2) |
|---|---|---|---|---|---|
| I25 | 2022 | 50,7 | **47,4** | URD 2023 (`Elis_Universal Registration Document_2023_EN.txt`) p. 307, columna 12/31/2022: «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) = (1) − (2) 74.9 47.4» | 410,7 − 363,3 = 47,4 |
| J25 | 2023 | 78,3 | **74,9** | DEU 2024 (`Elis_Document d'enregistrement universel_2024_FR.txt`) p. 301, columna 31/12/2023: «VALEUR NETTE DU PASSIF (ACTIF) RELATIF AUX RÉGIMES À PRESTATIONS DÉFINIES (3) = (1) - (2) 91,6 74,9» | 443,4 − 368,5 = 74,9 |
| K25 | 2024 | 104,1 | **91,6** | URD 2025 p. 355 (folio 353), columna 12/31/2024: «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) = (1) − (2) 67.1 91.6» | 447,8 − 356,2 = 91,6 |
| L25 | 2025 | 79,7 | **67,1** | URD 2025 p. 355, columna 12/31/2025: misma línea | 414,4 − 347,3 = 67,1 |

En las mismas páginas:
- Línea (4) «Other long-term benefits»: 3,3 (2022), 3,5 (2023), 12,5 (2024) y 12,6 (2025).
- Línea (5): «LIABILITIES (ASSETS) RELATED TO LONG-TERM EMPLOYEE BENEFITS (5)=(3)+(4) 79.7 104.1» (p. 355) y «… 78.3 50.7» (URD 2023 p. 307).
- El cuadro de movimientos de la p. 355 cuadra con la línea (3): «AS AT 12/31/2024 447.8 356.2 91.6» y «AS AT 12/31/2025 414.4 347.3 67.1».
- URD 2023 p. 307: «AS AT 12/31/2022 410.7 363.3 47.4» y «AS AT 12/31/2023 443.4 368.5 74.9».
- En todos los casos coinciden con la propuesta de la revisión.

### Qué línea tomaba el libro y por qué estaba mal

- Los `fase1_partes` (AR_2023, AR_2024 y AR_2025) citan la línea **(5) = (3) + (4)**, que es lo que suma el balance: pasivos por beneficios a empleados menos activos. Ejemplo: 93,2 − 13,5 = 79,7.
- `fase1_historia.py` toma para cada año el comparativo del informe siguiente: I25 sale de AR_2023 «anterior», J25 de AR_2024 «anterior», K25 de AR_2025 «anterior» y L25 de AR_2025 «actual».
- La fila 25 del libro pide «Posición neta (obligación − activos del plan)», que es la línea (3). La (5) añade otros beneficios a largo plazo que no son el déficit del plan.
- Interpretación: esos otros beneficios son también un pasivo con carácter de deuda, pero la etiqueta de la fila no los cubre. Si se quisieran recoger, irían en otra partida.
- 2016–2021 (C25:H25) ya son la línea (3), según la revisión. El URD 2022 (p. 289) imprimió para 2022 «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) – (1) = (2) 50.7 54.0», con obligaciones de 414,2. El URD 2023 lo reexpresa en 47,4 + 3,3.

### Efecto

- Historia!C65 (pensiones + minoritarios, último año) pasa de 79,7 a 67,1.
- **Motor A: ningún efecto directo en el valor.** C65 entra en Diagnóstico V6 C16, que solo usa el motor B, y en los múltiplos EV de Diagnóstico V6 B63/B64/D63/D64, que son informativos.
- La hipótesis de Palancas C23 cita «pensiones netas de 79,7»; con la corrección son 67,1.

### Propuesta y límite del formato

- `cambiar_base.py` **no tiene clave para la Historia**. Su ESQUEMA solo admite metadatos, `analisis` y evidencia, y la Historia la reconstruye `fase1_historia.py construir` desde `fase1_partes/` y `fase1_decisiones.json`.
- El origen no tiene `fase1_decisiones.json` y no se puede modificar.
- El JSON lleva la corrección en `propuesta_historia`, una clave que ningún script lee, con dos mecanismos. No elijo entre ellos:
  - **A.** La persona responsable escribe `fase1_decisiones.json` con el contenido propuesto. Ese archivo solo puede escribirlo una persona, según la cabecera de `fase1_historia.py`.
  - **B.** Se corrigen las entradas de pensiones de `fase1_partes`.
- En los dos casos el archivo tiene que estar en el destino antes de `construir`. Hay dos formas:
  - Añadirlo después de `preparar` y repetir `construir`. Con `analisis` vacío no se pierde ninguna sustitución; solo la nota «(cambio de base…)» de `fase1_v63.json`.
  - Ampliar `cambiar_base.py`.

---

## 6. Medias C46, C47 y C50 (solo descripción)

| Celda | Libro | Media exacta de los orígenes del registro (`derivacion.formula`) | Diferencia |
|---|---|---|---|
| C46 | 1.429,4 | (1.325,6 + 1.452,1 + 1.510,6) / 3 = **1.429,4333**. Fuentes: «Net cash from operating activities», DEU 2024 p. 273 y URD 2025 p. 327 | −0,033 |
| C47 | 857,1 | (820,8 + 876,0 + 874,7) / 3 = **857,1667**. Fuentes: «Net capex» publicado, DEU 2024 p. 259 («Investissements nets (876,0) (820,8)») y URD 2025 p. 314 («Net capex (874.7) (876.0)») | −0,067 |
| C50 | 28,2 | (22,9 + 27,1 + 34,7) / 3 = **28,2333**. Fuentes: DEU 2024 p. 273 («Paiements en actions 27,1 22,9») y URD 2025 p. 327 («Share-based payments 34.7 27.1») | −0,033 |

**El caso de C47.** Hay dos medias netas posibles:
- **Con el «Net capex» publicado:** 857,167, que redondeado a un decimal da 857,2.
- **Con las líneas del estado de flujos:** 857,133.
  - 2023: 26,8 + 797,1 − 0,1 − 2,8 − 0,3 = 820,7 (DEU 2024 p. 273), frente a 820,8 publicado.
  - 2024: 26,6 + 860,8 − 0,0 − 7,3 − 4,1 = 876,0.
  - 2025: 26,2 + 864,0 − 0,0 − 15,3 − 0,2 = 874,7 (URD 2025 p. 327).
- El 857,1 del libro es el redondeo de esta segunda media, no de la del registro.
- El capex **neto** es una elección del inversor (10-nov-2026, Control maestro fila 44). La Historia, fila 12, es bruta (823,9 / 887,4 / 890,2; media 867,167). La construcción automática de `fase1_v63.json` daría 867,167 si la etapa 1 no trajera el valor.
- No decido entre ninguna de estas opciones.

**Efecto en el FCF base:**
- Con el libro: 1.429,4 − 857,1 − 108,0 − 128,1 − 28,2 = 308,0.
- Con valores exactos: 307,933 (C47 = 857,167) o 307,967 (C47 = 857,133).

**En el JSON:** van en `propuesta_medias_pendiente_de_decision`, clave que no se aplica. `analisis` queda vacío, porque no hay decisión para Elis.

---

## 7. Precio C37 (sin cambio)

- **C37 = 24,18 €**, cierre del **4-nov-2026** (Palancas C45 = 2026-11-04).
- Fuente: histórico **no ajustado** de Euronext para ELIS (FR0012435121-XPAR), `fuentes_mercado/Euronext_ELIS_historico_no_ajustado_20261114.txt` (sha256 `257d6668…a1e671`), fila «04/11/2026 23.80 24.32 23.68 24.18 24.18 354,998 8,578,726 24.1656» (columna CLOSE).
- Hay capturas de esa fila (`Euronext_ELIS_fila_04112026_*.{jpg,png}`).
- La revisión lo da por verificado.
- El CAMBIO no toca `metadatos.precio`. Las fechas son distintas: precio de 2026 y acciones de 2025, y se declaran.

---

## 8. Hallazgo fuera del encargo: entradas de la etapa 1 con datos de 2026 (sin aplicar)

La decisión E6 pide «no aplicar parcialmente la conversión o la recompra». Varias celdas de Análisis vienen de la etapa 1 con datos de 2026, según la columna G del Control maestro del libro de datos. En el JSON están en `propuesta_entradas_2026_fuera_de_alcance` y no se aplican.

**C33 = 2,33**: «30-jun-26 pro forma conversión OCEANE (7-oct-26)». Aplica la conversión.
- A 31-dic-2025: (3.418,3 + 703,2 − 341,5) / 1.700,1 = **2,22**.
- Caja no restringida: 398,1 − 45,8 (Latinoamérica) − 8,0 (Rusia) − 2,8 (contrato de liquidez) = 341,5, todo de la p. 383.
- EBITDA ajustado: «ADJUSTED EBITDA 1,700.1» (p. 314).

**C42 = 5,66**: «EV pro forma oct-26». Aplica la conversión y depende de C41.
- A 31-dic-2025, con la C41 nueva: (5.621,3 + 3.780,0) / 1.700,1 = **5,53**.

**C53 = 446,6 y C54 = 4.816,9**: son de 30-jun-2026, después de la recompra.
- A 31-dic-2025: 398,1 (p. 383–384) y 4.121,5 (3.418,3 + 703,2).
- El motor A no resta C54. C76 = 0.

**C24, C31, C34, C40 y C76:** su periodo es LTM jun-26, H1-26 o 30-jun-26. C34 da también la cifra a diciembre de 2025: 0,43x, con el mismo «No».

Si se reexpresan, el JSON propone dos textos prohibidos adicionales: «pro forma conversión OCEANE» y «238\.072\.967». **No los he puesto activos**: con C33 y C42 sin reexpresar, `comprobar` daría «QUEDAN RESTOS».

---

## 9. Efectos separados (mecánicos, con todo lo demás igual; no ejecutados con el motor)

En el libro evaluado:
- **Valor por acción:** Panel K24 = (Motor BI7 − BL7) / C55. Hoy da −3,265 €.
- **Lo que se paga en el NORMAL:** C37 − BL7 / C55. Hoy da 13,52 €.
- BI y BL no dependen de C41 ni de C55 en el motor A. Lo he comprobado leyendo las fórmulas de Motor BI, BL, BO y M.

| Efecto | Cambio | Valor por acción (K24) | «Pagas en el NORMAL» |
|---|---|---|---|
| C55: 259,077654 → 232,47681 | ×1,114424 (+11,44 %) | −3,265 → −3,639 (×1,1144) | 13,52 → 12,30 |
| C41: 6.264,5 → 5.621,3 | −10,27 % | 0 en el motor A (solo conciliación y diagnóstico) | — |
| C48 | sin cambio | 0 | 0 |
| Pensiones I25:L25 | L25 −12,6 | 0 en el motor A; motor B +12,6 mm de patrimonio | — |
| Medias (si se adoptaran) | FCF base −0,03 a −0,07 | ≈0 (no calculado) | — |

Las fases B y C y la auditoría pueden cambiar hipótesis al ver la nueva base. Estas cifras no sustituyen el recálculo.

---

## 10. El archivo CAMBIO propuesto

Ruta: `/home/claude/trabajo_4_14/agentes/elis_E6/cambio_decisiones_elis_4_14.propuesta.json`. `python3 -m json.tool` lo valida.

**Origen y destino:**
- `origen`: `…/elis_motor_A/Elis`. `destino`: `…/elis_decisiones`.
- `etapa1/` tiene un solo libro (`Elis_evaluada.xlsx`), como exige `preparar`.

**Qué se conserva:** `conservar` = etapa1, texto, fase1_partes, fase1_fuentes.json, fuentes_mercado, fuentes_pdf, fuentes_2026 y verificacion_entradas.json. Este último quedará desactualizado en C55, C41 e I25:L25 hasta su nueva revisión, igual que en Viscofan.

**Metadatos que cambian:** solo acciones y capitalización.
- `acciones_diluidas`: valor, fecha, fuente con página, periodo, unidad y `literal` (va a la columna M del Control maestro).
- `capitalizacion`: valor, fecha, fuente, periodo y unidad.
- `rellenar_fase1_v63.py` los escribe siempre, con su evidencia.

**Notas:**
- `nota_metadatos` resume la base y los hechos posteriores que no se aplican.
- `notas_que_se_retiran` retira 4 notas de la base anterior: «Acciones: la base es…», «Hecho posterior… conversión…», «La etapa 1 usó 240,69…» y «ATENCIÓN… acciones diluidas medias…». He comprobado que los cuatro patrones casan con las notas 3, 4, 6 y 12 de `fase1_metadatos.json`.

**`analisis` y descartes:**
- `analisis` = {}: no cambia ninguna celda de dato.
- `analisis_que_se_descartan` = {}: `construir` reproducirá C46–C50 del origen sin cambios, porque las partes son las mismas.

**Evidencia:** `evidencia` escribe la columna N de C48 (§3).

**Textos prohibidos:** 3 patrones, que son los textos antiguos de C55, C41 y de la nota 4. He comprobado que casan con los metadatos antiguos, que no casan con los textos nuevos y que no aparecen en el Control maestro de la etapa 1.

**Alcance:** `alcance` tiene tipo `ensayo_exploratorio`, aviso y fuente, y dice que no es una valoración a 2026. `configuracion_economica` = null, porque es la V6.3.

**Claves que ningún script lee:** `propuesta_historia` (I25:L25), `propuesta_medias_pendiente_de_decision`, `propuesta_dilucion_potencial_no_incorporada` y `propuesta_entradas_2026_fuera_de_alcance`.
- Si se prefiere un CAMBIO sin claves ajenas al ESQUEMA, pueden quitarse sin efecto en `preparar`.
- La ruta definitiva que cita `alcance.fuente` (`E414/configuracion/cambio_decisiones_elis_4_14.json`) es la que le daría la orquestación; aquí no se ha creado.

---

## 11. Lo que no he podido comprobar

- **Diferencia de 930 acciones propias** entre las cuentas consolidadas y las de la sociedad matriz (p. 415): sin explicar.
- **La media básica 233.954.020** no la he reconstruido exactamente: queda a 926 acciones con la aproximación de la p. 395.
- **El cupón de la OCEANE dentro de «Net interest paid»** es una inferencia. El estado de flujos no lo desglosa. Su efecto fiscal en caja no se publica.
- **El desglose de los 2,4** de la OCEANE en 2026 (p. 383) como interés devengado es una interpretación.
- **No he ejecutado el motor.** Los efectos del §9 son mecánicos, con todo lo demás igual, y el de la dilución potencial no está calculado.
- **No he renderizado PDF.** He trabajado con el texto extraído. La revisión ya renderizó las p. 355 y 395 del URD 2025.
- **`fuentes_2026/Elis_OCEANE_2029_ajuste_ratio.html` no existe.** La relación 6.256,8564 la he tomado del comunicado del 7-oct y del informe semestral, p. 15.
- **Una incoherencia del informe semestral de 2026** que no afecta a la base: la p. 46 da «Treasury shares 0» a 30-jun-2026 y la p. 14 da 16.914.214.

---

## 12. Versión final del CAMBIO

**Archivo:** `/home/claude/trabajo_4_14/agentes/elis_E6/cambio_decisiones_elis_4_14.json`.
- Lo valida `python3 -m json.tool`.
- La propuesta anterior se conserva en `cambio_decisiones_elis_4_14.propuesta.json`.
- Lo genera `…/scratchpad/e6/hacer_cambio_final.py` a partir de la propuesta.

**Qué no he ejecutado:** `cambiar_base.py`, `pipeline.py` ni LibreOffice. No he tocado `E414/elis_motor_A`.

**Ensayo en una copia del scratchpad:** `…/scratchpad/e6/sim/Elis`, con `texto/` enlazado en solo lectura. En la copia:
- he aplicado las correcciones de `fase1_partes`;
- he ejecutado `fase1_historia.py comprobar-anio` y `construir`;
- he simulado la evidencia final del Control maestro (§12.6).

### 12.1 Pensiones: `correcciones_fase1_partes` (sustituye a `propuesta_historia`, que se ha quitado)

- Seis correcciones, todas con `partida` = "pensiones" e `indice` = 0.
- En cada una, la línea nueva es la línea (3) literal del texto, comprobada en su `[PDF PAGE n]`.
- `fase1_partes` ya estaba en `conservar`.

| Archivo · lado | Esperado (impreso actual) | Nuevo impreso | Página PDF | Línea del texto (línea del .txt) |
|---|---|---|---|---|
| AR_2023 · actual | 78.3 | 74.9 | 307 | «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) = (1) − (2) … 74.9 … 47.4» (URD 2023, l. 19594) |
| AR_2023 · anterior | 50.7 | 47.4 | 307 | la misma |
| AR_2024 · actual | 104,1 | 91,6 | 301 | «VALEUR NETTE DU PASSIF (ACTIF) RELATIF AUX RÉGIMES À PRESTATIONS DÉFINIES (3) = (1) - (2) … 91,6 … 74,9» (DEU 2024, l. 19002) |
| AR_2024 · anterior | 78,3 | 74,9 | 301 | la misma |
| AR_2025 · actual | 79.7 | 67.1 | 355 | «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) = (1) − (2) … 67.1 … 91.6» (URD 2025, l. 25148) |
| AR_2025 · anterior | 104.1 | 91.6 | 355 | la misma |

Resultado en la copia:
- `comprobar_anio` de 2023, 2024 y 2025 no da ningún error: cada número está en su línea y en su página.
- `construir` termina con rc 0.
- Historia fila 25 = 64,8 / 83,7 / 81,5 / 87,1 / 74,8 / 54,0 / **47,4 / 74,9 / 91,6 / 67,1**.
- Ninguna otra partida de la Historia cambia.

**Límite:** la «nota» de los lectores de la partida, que pasa a Historia!M25, sigue diciendo «Neto (Note 5.3…): pasivo 93.2 menos activo 13.5 del balance». El mecanismo solo corrige la entrada, no esa nota. Es texto, no cifra del modelo.

### 12.2 Acciones, capitalización y C48 (como en la propuesta)

- **C55 = 232,476810** (`metadatos.acciones_diluidas`, fecha 2025-12-31). Fuente: URD 2025 PDF p. 394, 439 y 441 (§1).
- **C41 = 5.621,2892658** (`metadatos.capitalizacion`). Es 24,18 € (4-nov-2026) × C55, con fechas distintas declaradas.
- **C48 = 108,0, sin cambio.** La conciliación con la base 2025 queda escrita en `evidencia["Análisis!C48"].N`.
- Precio y tasa sin riesgo: sin cambio.
- Notas retiradas y nota de metadatos: las del §10.

### 12.3 Reexpresión a 31-dic-2025 (decisión E6)

- Todas van en `analisis` con valor, fuente, página, periodo, unidad, `vaciar_en_etapa1: true` y evidencia nueva del Control maestro.
- Columnas de evidencia que escribe el CAMBIO: G, I, K, M y N. La fase 1 escribe además F, J, L, G y H desde la entrada.
- C42 es «fresca» en `rellenar_fase1_v63.py`: la fase 1 vacía G:N y escribe J, L, G y H.
- La columna K pasa a ser la copia local del URD 2025 en lugar del enlace al comunicado del primer semestre de 2026.

| Celda | Etapa 1 (periodo) | Valor a 31-dic-2025 / 2025 | Cálculo y fuente (URD 2025, PDF) |
|---|---|---|---|
| C24 | 0,098 (LTM jun-26) | **0,097** | EBIT ajustado 766,6 (p. 315) ÷ capital empleado bruto medio dic-24/dic-25 7.899,2. Patrimonio 3.598,1 / 3.812,5 (p. 326), deuda 3.660,1 / 3.418,3 (p. 384), arrendamientos 606,2 / 703,2 (p. 366) = 9,705 %. Se conserva la definición del inversor del 10-nov-2026 |
| C31 | Sí (H1-26) | **Sí** | Cuentas a cobrar comerciales 838,6 frente a 771,0, +8,8 % (p. 349). Ingresos 4.796,8 frente a 4.573,7, +4,9 % (p. 324). Existencias +3,0 % (p. 326). 17,4 de perímetro (p. 340) |
| C33 | 2,33 (pro forma conversión) | **2,22** (2,2234) | (3.418,3 + 703,2 − 341,5) ÷ 1.700,1. Caja no restringida = 398,1 − 45,8 − 8,0 − 2,8 (p. 383); EBITDA ajustado (p. 314) |
| C34 | No (30-jun-26) | **No** (0,43x) | 341,5 ÷ 800,5 (p. 383–384). Con la caja total, 0,50x |
| C40 | 264,5 (LTM jun-26) | **323,9** | 1.510,6 − 874,7 − 99,4 − 177,9 − 34,7 (p. 327 y 314). El FCF publicado por Elis es 358,6, menos la SBC de 34,7 |
| C42 | 5,66 (EV pro forma oct-26) | **5,53** (5,5299) | (5.621,2893 + 3.780,0) ÷ 1.700,1. Precio del 4-nov-2026 con balance de 2025, declarado |
| C53 | 446,6 (30-jun-26) | **398,1** | p. 383–384 |
| C54 | 4.816,9 (30-jun-26) | **4.121,5** | 3.418,3 (p. 384) + 703,2 (p. 366) |
| C76 | 0 (30-jun-26) | **0, sin cambio de valor** | Solo `evidencia` (G, I, J, K, L, M, N). C76 es una fila de juicio y no es una celda de dato admitida por la fase 1 |

Todas tienen cifra de 31-dic-2025 o del ejercicio 2025 en las fuentes conservadas: **no queda ninguna sin reexpresar**.

### 12.4 Medias: supuesto de la orquestación (precedente E1), no decisión de la persona responsable

Van en `analisis` con `vaciar_en_etapa1` y evidencia M/N, como en Viscofan y Vidrala. El texto de cada una dice expresamente «SUPUESTO DE LA ORQUESTACIÓN … NO es una decisión de la persona responsable para Elis».

| Celda | Valor | Cálculo y fuente |
|---|---|---|
| C46 | **1.429,433** | (1.325,6 + 1.452,1 + 1.510,6) / 3. DEU 2024 p. 273; URD 2025 p. 327 |
| C47 | **857,167** | Media del «Net capex» publicado, (820,8 + 876,0 + 874,7) / 3. DEU 2024 p. 259; URD 2025 p. 314. Es la fórmula de derivación del registro |
| C50 | **28,233** | (22,9 + 27,1 + 34,7) / 3. DEU 2024 p. 273; URD 2025 p. 327 |

Sobre C47:
- Con las líneas del estado de flujos la media sería 857,133, porque en 2023 da 820,7 frente a los 820,8 publicados.
- Esa diferencia es de redondeo de la propia empresa. No se usa porque el concepto elegido por el inversor es el «Net capex» publicado.

Con estos valores y C48 y C49 sin cambio, el FCF base queda en 307,933.

### 12.5 Guardián de `analisis` del origen

- El `fase1_v63.json` del origen tiene C46 a C50.
- En la reconstrucción de la copia:
  - C46, C47 y C50 se declaran en el CAMBIO.
  - C48 (82,933) y C49 (128,1) salen **iguales**: no hace falta declararlos.
- `analisis_que_se_descartan` = {}.
- Las celdas de la etapa 1 que no se declaran no las toca `construir`. Siguen como valores migrados del libro, entre ellas C48 = 108,0.

### 12.6 Textos prohibidos activos (13) y simulación

**Los tres de la base anterior:**
- «Es la media ponderada del ejercicio 2025 (no un saldo a 31-dic-2025)»
- «× 259,077654 millones de acciones (media ponderada diluida de 2025»
- «Las acciones de la conversión ya estaban contadas en la base diluida»

**Los diez de 2026, que solo aparecían en la evidencia antigua de las celdas reexpresadas:**
- «pro forma conversión OCEANE»
- «238\.072\.967»
- «LTM jun-26»
- «globenewswire\.com/news-release/2026/07/29»
- «446,6»
- «4\.816,9»
- «1\.181,7»
- «4\.117,0»
- «bono de mar-26»
- «recompra de julio»

**Resultado de la simulación** (evidencia de la etapa 1, más la del CAMBIO, más lo que escribe la fase 1; filas activas 17–82 y 107–175; columnas que revisa `comprobar`):
- **0 restos.**
- Tampoco hay ninguno en las notas de `fase1_metadatos.json` ni de `fase1_v63.json`.

**Descartado: «NP H1-26».** Casaba con Análisis!C28, columna J («…; NP H1-26»). C28 no se reexpresa: su valor, «Emite», ya usa ejercicios cerrados FY22→FY25. Con ese patrón activo, `comprobar` fallaría.

### 12.7 Lo que queda (limitaciones declaradas)

- **Restos fuera de la evidencia revisada.** «LTM jun-26» aparece en la cabecera del Control maestro (F5, «Periodo usado en medias DCF») y en la lista de comprobación (fila 88). Ninguna de las dos es evidencia activa, así que `comprobar` solo informa. El CAMBIO no puede reescribirlas: haría falta `control_maestro_textos` en la fase 1.
- **Contexto de 2026 en celdas que no se reexpresan.** Sus valores no dependen de la conversión ni de la recompra:
  - C28 y C60: el texto menciona la conversión del 7-oct-26 como hecho posterior.
  - C38: contraste SWS del 10-jun-2026.
  - C97: ventas de directivos de nov-2025 a nov-2026; es una fila de juicio.
  - D4, M: «Último periodo publicado: H1 2026».
  - B66, N: cita 1.181,7 de deuda a corto de jun-26. Es una fila de juicio y su N la reescriben las fases.
- **Nota de lectores de pensiones** (§12.1).
- **El registro de verificación** (`verificacion_entradas.json`, conservado) queda desactualizado en todas las celdas cambiadas hasta su nueva revisión.
- **Los efectos en el valor** son los mecánicos del §9 para C55. El de las medias es pequeño: FCF base −0,067 mm. Las reexpresiones de C24, C31, C33, C34, C40, C42, C53 y C54 no entran en el valor del motor A, que solo usa C46–C50, C55 y C76. Sí cambian los diagnósticos y los umbrales. No lo he calculado con el motor.
