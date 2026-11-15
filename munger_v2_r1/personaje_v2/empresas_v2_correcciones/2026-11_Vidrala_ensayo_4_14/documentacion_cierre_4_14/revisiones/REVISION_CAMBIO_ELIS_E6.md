# Revisión independiente del CAMBIO de base E6 de Elis (base 31-dic-2025)

- **Revisor:** RE6, Claude. Trabajo con un contexto separado del extractor. **No es una revisión humana.** Fecha: 14-nov-2026.
- **Objeto:** `/home/claude/trabajo_4_14/agentes/elis_E6/cambio_decisiones_elis_4_14.json`. No lo he modificado, ni ningún otro archivo de entrada.
- **Método:**
  - Primero contrasté las fuentes yo mismo. Solo después leí `EXTRACCION_ELIS_E6.md`.
  - Leí los textos con marcas `[PDF PAGE n]` del expediente de origen, `fuentes_2026/` y `fuentes_mercado/`.
  - Abrí con openpyxl en solo lectura `Elis_v63_datos.xlsx`, `Elis_v63_evaluada.xlsx` y `etapa1/Elis_evaluada.xlsx`.
  - Leí `cambiar_base.py` y `rellenar_fase1_v63.py` para saber qué columnas del Control maestro reescribe cada paso.
  - Simulé en memoria la evidencia activa final: Control maestro del libro de datos + evidencia del CAMBIO + lo que escribe la fase 1. No ejecuté `cambiar_base.py`, el pipeline ni LibreOffice.
- **Abreviaturas:**
  - Las páginas son siempre de PDF.
  - URD 2025 = `texto/Elis - 2025 Universal Registration Document.txt`. Su PDF tiene sha256 `04bfd087…cd62e` (coincide con `fuentes_pdf/HUELLAS_PDF.txt`) y el texto `0672b95d…`.
  - DEU 2024 = `texto/Elis_Document d'enregistrement universel_2024_FR.txt`.
  - URD 2023 = `texto/Elis_Universal Registration Document_2023_EN.txt`.

## Resultado

**DISCREPANCIA (menor; solo afecta a textos de evidencia).** **Todas las cifras del CAMBIO están verificadas**: acciones, capitalización, OCEANE, C48, dilución, las seis correcciones de pensiones, las nueve reexpresiones y las tres medias. Ninguna incorpora la conversión ni la recompra de 2026.

Hay dos restos de 2026 en evidencia activa que el CAMBIO no reescribe y que `textos_prohibidos` no detecta. No cambian ningún valor:

- **D1.** La columna I del Control maestro de C46, C47 y C50 (también la de C48) sigue diciendo «Informe anual auditado + NP». NP es la nota de prensa del primer semestre de 2026.
- **D2.** La N de C88 presenta como «Actual» múltiplos de base 30-jun-2026 y «pro forma».

Hay además puntos que no puedo comprobar o que tiene que confirmar la persona responsable (§8).

---

## 1. C55, C41 y C37: **VERIFICADO**

**C55 = 232,47681 M (`metadatos.acciones_diluidas`, fecha 2025-12-31).**

Hechos:
- URD 2025 p. 394, nota 10.1:
  - «NUMBER OF SHARES AS AT DECEMBER 31, 2025 232,848,588»
  - «Number of shares issued and fully paid up 232,848,588»
  - «Treasury shares 371,778»
- p. 439, cuadro de accionistas a 12/31/2025: «Treasury stock 371,778» y «TOTAL 232,848,588».
- p. 441: «Treasury shares held directly or indirectly as at December 31, 2025 371,778(b)», con «(b) O/w 131,550 for the liquidity agreement».

Cálculo: 232.848.588 − 371.778 = **232.476.810** = 232,47681 M.

Conciliaciones:
- **Historia del capital** (p. 437): 236.664.445 + 889.250 (Elis for All, 13-nov-2025) − 4.705.107 (amortización) = 232.848.588.
- **Dividendo propuesto** (p. 395): «€0.48 per share, or €111.6 million, based on the number of existing shares as at December 31, 2025 (excluding treasury shares)». 0,48 × 232.476.810 = 111,59 mm. Cuadra.
- **Autocartera:** 240.228 fuera del contrato de liquidez (6.560.820 − 6.320.592, p. 415) + 131.550 del contrato = 371.778.

**No incluye acciones de la conversión de 2026:**
- Informe semestral 2026 (`fuentes_2026/texto/Elis_2026_half-year_financial_report_EN.txt`, p. 46): «Number of shares as at December 31, 2025 232,848,588» y «NUMBER OF SHARES AS AT JUNE 30, 2026 232,848,588».
- La conversión es del 7-oct-2026. Comunicado `fuentes_2026/Elis_OCEANE_2029_resultados_conversion.html`, sha256 `f6d6c27f…be7`, igual que `HUELLAS.txt`: «comprising 18,104,556 existing shares held in treasury and 5,465,000 new shares»; «share capital … now amounts to EUR 238,313,588».

Diferencias con otras cifras:
- No es la media diluida del BPA: 259.077.654, p. 395, que incluye «Effect of conversion of convertible bonds 23,355,764».
- **Observación menor:** la fuente de C55 cita «la amortización … del 23-dic-2025 (PDF p. 437)». El cuadro de la p. 437 imprime «11/23/2025». La fecha de diciembre está en las p. 394, 440 y 441. No afecta a ninguna cifra.

**C41 = 5.621,2892658 mm.** Cálculo: 24,18 × 232,47681 = 5.621,2892658. Exacto. Las fechas son distintas (precio del 4-nov-2026, acciones de 31-dic-2025) y se declaran. Contraste: p. 447, «232,848,588 24.26 5,648.9».

**C37 = 24,18 €, 4-nov-2026 (sin cambio).**
- `fuentes_mercado/Euronext_ELIS_historico_no_ajustado_20261114.txt`, sha256 `257d6668…` (coincide con `HUELLAS.txt`): «04/11/2026 23.80 24.32 23.68 24.18 24.18 354,998 8,578,726 24.1656».
- La captura `Euronext_ELIS_fila_04112026_cierre.png` muestra la fila resaltada con CLOSE 24.18.
- Que la persona responsable quiera el precio de 2026 en una base 2025 está en §8.

**Mecánica del pipeline:** `rellenar_fase1_v63.py` trata C37, C41, C55 y C57 como frescas: vacía G:N del Control maestro y escribe los textos nuevos. No quedan los textos antiguos («238.072.967», «240,69», «Twelve Data × 259,077654»).

## 2. OCEANE como deuda y C48: **VERIFICADO**. El desglose del cupón **NO ES COMPROBABLE**.

**Pasivo a 31-dic-2025:**
- URD 2025 p. 384, nota 8.5: «CONVERTIBLE BONDS 362.0 352.3», dentro de «BORROWINGS AND FINANCIAL DEBT 3,418.3».
- p. 383, vencimientos: «Convertible bonds 364.4 2.4 362.0».
- p. 314: «revaluation of the debt component of the convertible bond (… -€9.7 million in 2025)». 352,3 + 9,7 = 362,0.
- Pasivo = **362,0 a coste amortizado**. El total de 364,4 incluye los 2,4 que vencen en 2026. Que esos 2,4 sean interés devengado es una interpretación: 380 × 2,25 % × 100/365 ≈ 2,34.

**Presencia en el libro:**
- Historia!L22 = 3.418,3 (incluye la OCEANE). C54 = 3.418,3 + 703,2 = 4.121,5.
- No hay ninguna resta ni pro forma de la conversión en C33, C42, C53, C54, C41 ni C55.

**C48 = 108,0 (sin cambio; solo se reescribe N):**
- Intereses netos pagados: 70,5 (DEU 2024 p. 273, «Intérêts financiers nets versés (78,9) (70,5)»), 78,9 y 99,4 (URD 2025 p. 327, «Net interest paid (99.4) (78.9)»). Media 82,9333.
- Intereses de arrendamientos (pagos menos principal):
  - 130,8 − 111,0 = 19,8 (DEU 2024 p. 273 y p. 312, «Paiements du principal … (111,0)»)
  - 150,8 − 125,0 = 25,8
  - 177,9 − 148,3 = 29,6 (URD 2025 p. 327 y p. 366)
  - Media 25,0667.
- Suma: **108,000**.
- Cupón de la OCEANE: «annual coupon of 2.25%, payable annually and for the first time on September 22, 2023» (p. 380). 2,25 % × 380,0 = 8,55. La p. 377 da 8,6 al año.

**Coherencia:** la OCEANE es deuda, sus acciones no están en C55 y su cupón está en el coste. No hay doble cómputo.

**No comprobable:** que el cupón esté dentro de «Net interest paid». El estado de flujos no lo desglosa; la p. 312 solo dice «financial interest (net of financial income)». La inferencia es razonable, pero no es un dato publicado.

**Observaciones:**
- `fase1_v63.json` seguirá teniendo C48 = 82,933, calculado desde la Historia. El libro conservará 108,0, porque la etapa 1 no lo vacía y la fase 1 no pisa ese valor. Es lo mismo que en el origen.
- La M de C48 (texto de la etapa 1) cita «LTM 85,2» como alternativa descartada. No cambia el valor.

## 3. Dilución potencial: **VERIFICADO**. Las cifras son correctas, no entra en el caso base y no se cuenta dos veces.

**OCEANE 2029:**
- p. 380: «These 3,800 2029 OCÉANEs represented 23,355,764 underlying shares … as at December 31, 2025 … 6,146.2538 shares per bond».
- 3.800 × 6.146,2538 = 23.355.764,4. La p. 439 da la misma cifra.

**Acciones de rendimiento:**
- p. 360, «Number of rights outstanding as at 12/31/2025»: 0 + 388.960 + 0 + 954.339 + 29.250 + 16.730 + 1.207.746 + 16.880 = **2.613.905**. La p. 439 da «2,613,905 rights».
- Máximo con el 120 % (p. 361 (d)): 3.136.686.

**Escenarios:** 232.476.810 + 23.355.764 = 255.832.574. Con las acciones de rendimiento, 258.446.479.

**Dónde queda declarada:**
- Fuente de C55, que pasa a la J del Control maestro.
- `alcance.aviso`.
- `nota_metadatos`, que menciona la OCEANE pero no las acciones de rendimiento.

**No se suma a C55.** La variante «si se convierte» quita a la vez el cupón (108,0 − 8,55 = 99,45) y la deuda. Es correcta.

**Observación:** el tratamiento de las 2,61 M acciones de rendimiento queda abierto en `propuesta_dilucion_potencial_no_incorporada`, una clave que ningún script lee. En el caso base actúan de hecho como coste a través de la SBC (C50, con C51 = Sí) y no entran en el denominador. Ningún texto activo lo dice expresamente.

## 4. Pensiones: `correcciones_fase1_partes` y `nota_partida`: **VERIFICADO**

Comprobé lo siguiente:
- El `esperado` es lo que hay ahora en `fase1_partes` del origen.
- La `linea` es una subcadena literal de su `[PDF PAGE n]`.
- El `impreso` nuevo está en esa línea.
- (1) − (2) cuadra.

| Archivo · lado | Esperado (origen) | Nuevo | Página | Comprobación |
|---|---|---|---|---|
| AR_2023 · actual | 78.3 ✓ | 74.9 | URD 2023 p. 307 | 443,4 − 368,5 = 74,9 |
| AR_2023 · anterior | 50.7 ✓ | 47.4 | URD 2023 p. 307 | 410,7 − 363,3 = 47,4 |
| AR_2024 · actual | 104,1 ✓ | 91,6 | DEU 2024 p. 301 | 447,8 − 356,2 = 91,6 |
| AR_2024 · anterior | 78,3 ✓ | 74,9 | DEU 2024 p. 301 | 443,4 − 368,5 = 74,9 |
| AR_2025 · actual | 79.7 ✓ | 67.1 | URD 2025 p. 355 | 414,4 − 347,3 = 67,1 |
| AR_2025 · anterior | 104.1 ✓ | 91.6 | URD 2025 p. 355 | 447,8 − 356,2 = 91,6 |

Líneas literales de la nota 5.3:
- «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) = (1) − (2) … 67.1 91.6»
- «Other long-term benefits (4) 12.6 12.5»
- «LIABILITIES (ASSETS) RELATED TO LONG-TERM EMPLOYEE BENEFITS (5)=(3)+(4) 79.7 104.1»

Los «Other long-term benefits» que citan los `motivo` coinciden: 3,3, 3,5, 12,5 y 12,6.

**Efecto en la Historia:**
- `fase1_historia.py` toma el comparativo del informe siguiente (fuentes de Historia!M25).
- I25 = AR_2023 anterior → 47,4; J25 = AR_2024 anterior → 74,9; K25 = AR_2025 anterior → 91,6; L25 = AR_2025 actual → 67,1.
- Coincide con las discrepancias I25:L25 de `verificacion_entradas.json`.

**`nota_partida`:** está en las tres correcciones «actual» (una por archivo) con las cifras de la línea (3). Sustituye la nota errónea «pasivo 93.2 menos activo 13.5». `cambiar_base.py` la aplica (`d["partidas"][partida]["nota"]`).

**Observación, fuera de I25:L25:**
- El DEU 2022 (p. 289) imprime «NET VALUE OF DEFINED BENEFIT PLAN LIABILITY (ASSET) (3) – (1) = (2) 50.7 54.0», sin línea de «Other long-term benefits».
- Su 50,7 de 2022 es la línea (5) del URD 2023 (47,4 + 3,3).
- Por eso es posible que H25 (2021, 54,0) y los años anteriores sigan con el concepto que incluye otros beneficios, y que la serie se rompa entre H25 e I25.
- No lo he podido comprobar y la decisión no lo pide (§8).

## 5. Entradas de `analisis`: **VERIFICADO** en valores, fórmulas, periodos, páginas y citas. **DISCREPANCIA D1** en la evidencia.

| Celda | Valor CAMBIO | Recalculado | Periodo | Página y cita comprobadas |
|---|---|---|---|---|
| C24 | 0,097 | 766,6 ÷ ((3.598,1 + 3.660,1 + 606,2) + (3.812,5 + 3.418,3 + 703,2))/2 = 766,6 ÷ 7.899,2 = 0,09705 | ejercicio 2025 | p. 315 «ADJUSTED EBIT (I) 766.6 732.9»; p. 326 «TOTAL EQUITY 3,812.5 3,598.1»; p. 384 «3,418.3 3,660.1»; p. 366 703,2 / 606,2. La definición (capital bruto medio) es la de la etapa 1 |
| C31 | Sí | 838,6/771,0 = +8,77 % frente a 4.796,8/4.573,7 = +4,88 %; existencias +2,95 % | dic-25 frente a dic-24 | p. 349 «TRADE RECEIVABLES AND NOTES RECEIVABLE 838.6 771.0»; p. 324; p. 326; p. 340 (17,4); p. 310 («mechanical effect of the increase in revenue throughout 2025») |
| C33 | 2,22 | (3.418,3 + 703,2 − 341,5) ÷ 1.700,1 = 2,2234; caja no restringida 398,1 − 45,8 − 8,0 − 2,8 = 341,5 | 31-dic-2025 | p. 383 (45,8; 8,0; 2,8), p. 384, p. 366, p. 314 «ADJUSTED EBITDA 1,700.1». Con caja total 2,19x ✓ |
| C34 | No | 341,5 ÷ 800,5 = 0,43x (caja total 0,50x) | 31-dic-2025 | p. 384 «Of which maturing in less than one year 800.5»; RCF «€900.0 million» sin disponer → 1,55x ✓ |
| C40 | 323,9 | 1.510,6 − 874,7 − 99,4 − 177,9 − 34,7 = 323,9; FCF 358,6 ✓ | ejercicio 2025 | p. 327 (CFO, leases, intereses, «Share-based payments 34.7»); p. 314 «Net capex (874.7)», «FREE CASH FLOW 358.6» |
| C42 | 5,53 | (5.621,2893 + 3.780,0) ÷ 1.700,1 = 5,5298 | precio 2026 × acciones y deuda 2025 (declarado) | p. 314, 366, 383, 384 |
| C53 | 398,1 | — | 31-dic-2025 | p. 383 «CASH AND CASH EQUIVALENTS (ASSETS) 398.1 622.0» (296,3 + 101,7) |
| C54 | 4.121,5 | 3.418,3 + 703,2 | 31-dic-2025 | p. 384; p. 366 «AS AT 12/31/2025 … 703.2» |
| C76 | 0 (solo evidencia) | — | 31-dic-2025 | p. 383–384: caja 398,1 < deuda a corto 800,5 < bruta 3.418,3 |
| C46 | 1.429,433 | (1.325,6 + 1.452,1 + 1.510,6)/3 = 1.429,4333 | 2023–2025 | DEU 2024 p. 273 «FLUX NETS … ACTIVITÉ 1 452,1 1 325,6»; URD 2025 p. 327 |
| C47 | 857,167 | (820,8 + 876,0 + 874,7)/3 = 857,1667 (con las líneas del estado de flujos, 857,133) | 2023–2025 | DEU 2024 p. 259 «Investissements nets(b) (876,0) (820,8)»; URD 2025 p. 314 |
| C50 | 28,233 | (22,9 + 27,1 + 34,7)/3 = 28,2333 | 2023–2025 | DEU 2024 p. 273 «Paiements en actions 27,1 22,9»; URD 2025 p. 327 |

**Medias con tres decimales:** es la precisión del precedente E1 (Viscofan y Vidrala usan 3 decimales en sus CAMBIO) y la de `fase1_historia.py`. Cada media dice expresamente «SUPUESTO DE LA ORQUESTACIÓN … NO es una decisión de la persona responsable para Elis». Correcto.

**`textos_prohibidos` (13):**
- Cada patrón casa con algún texto antiguo (metadatos o Control maestro de la etapa 1).
- Ninguno casa con los textos nuevos del CAMBIO (metadatos, nota, análisis, evidencia, alcance, partes).
- Las 4 `notas_que_se_retiran` casan con una nota cada una.
- Mi simulación de la evidencia activa final (filas 17–82 y 107–175; G:M en filas de juicio y E:N en filas de dato) da **0 restos**.
- Fuera de la evidencia activa, y solo informativos: Control maestro F5 y D88 («LTM jun-26»).

**DISCREPANCIA D1:**
- En la etapa 1, la columna I («Tipo de fuente») del Control maestro de C46 (fila 43), C47 (44) y C50 (48) dice «Informe anual auditado + NP». También la de C48 (45). NP es la nota de prensa del primer semestre de 2026; la J de la etapa 1 era «…; NP H1-26».
- El CAMBIO solo reescribe M y N de esas filas, y la fase 1 no escribe I cuando hay fuente (`etiquetar`).
- El resto de 2026 queda en la evidencia activa de entradas reexpresadas, aunque sus valores sean ya solo de informes anuales.
- Lo esperado: declarar I = «Informe anual auditado + cálculo derivado» (o «Informe anual auditado») en `analisis.C46/C47/C50.evidencia` y en `evidencia["Análisis!C48"]`.

**Observación sobre C42:** es «fresca» en `rellenar_fase1_v63.py`. La fase 1 vacía G:N y solo escribe J, L, G y H, así que la evidencia I, K, M y N que declara el CAMBIO para C42 se perderá. No deja restos: J lleva todo el cálculo y sus fechas. Pero esa evidencia declarada no llegará al libro.

## 6. Otras entradas con datos de 2026 o pro forma: **VERIFICADO** en valores, con la **DISCREPANCIA D2** en un texto.

**Con datos de 2026 en el valor.** Son de mercado o de terceros, no operaciones societarias de 2026:
- **C37:** precio del 4-nov-2026.
- **C57:** tasa sin riesgo del 4-nov-2026.
- **C38:** 29,45 €, valor razonable de Simply Wall St del 10-jun-2026. Entra en C39 y C87 solo como contraste.
- **C97:** «Neutral», ventas de directivos de nov-2025 a nov-2026. Es una fila de juicio; en el Motor solo se comprueba que esté rellena.
- **D4:** fecha real de ejecución.
- Ninguna aplica la conversión ni la recompra. Si son admisibles en una base 2025 está en §8.

**Con contexto de 2026, sin efecto en el valor:**
- **C28 = «Emite» y C60 = 0,0109:** usan FY22→FY25. Los textos M, N y J mencionan la conversión del 7-oct-26 y «NP H1-26».
- **C32 = 0,422:** a dic-25. M da también jun-26 (41,0 %).
- **C48 y C49:** M cita LTM como alternativa.
- **D4:** M dice «Último periodo publicado: H1 2026».
- **Filas de juicio** cuya N reescriben las fases: C13, C25, C61, C62, B66 (que cita «1.181,7»), B67, C66, D65, D66, C98.
- C26, C88 (valor 14,6, mediana de cierres de 2019–2025) y C96 son de 2025 o anteriores.

**DISCREPANCIA D2:**
- La N de C88 (fila 73, fila de dato, evidencia activa) dice: «Actual 17,6x (base 30-jun, homogénea con el histórico) / 19,3x (pro forma) sobre FCF LTM».
- Presenta como actuales múltiplos de base 30-jun-2026 y pro forma de la conversión.
- No la detecta ningún patrón: «pro forma conversión OCEANE» no casa con «(pro forma)».
- No cambia el valor, que es una mediana histórica.
- Lo esperado: reescribir esa N (en `evidencia["Análisis!C88"]`) sin el múltiplo «actual» de 2026, o marcarlo como hecho posterior no aplicado, o añadir un patrón prohibido.

## 7. Coherencia con la decisión: **VERIFICADO** (base 2025; no se presenta como actualización a 2026)

- `base_economica`, `alcance.aviso` y `nota_metadatos` dicen literalmente que no es una valoración actualizada a 2026 y que no se recogen la recompra ni la conversión.
- Recompra y conversión de 2026 en el CAMBIO:
  - Solo aparecen como hechos posteriores informativos.
  - Sus cifras están comprobadas: 17.787.422 acciones por 466,8 mm (p. 46 del semestral); 16.914.214 propias (p. 14); 99,13 %; 23.569.556 acciones; 238.313.588; 3.304.271,85 €.
  - Ninguna se aplica, ni entera ni en parte.
- La OCEANE es deuda (362,0), su cupón está en C48 y sus acciones no están en C55. La dilución está identificada aparte.
- Las pensiones están corregidas.
- Las medias se declaran como supuesto de la orquestación, no como decisión.

**Observaciones:**
- `conservar` incluye `etapa1/`, que contiene `Elis_respuesta.md` (240,69 M de acciones, LTM, «19,3x pro forma», «1.181,7»). `volcar_datos_v63.py` lo pasa a las fases como bloque HEREDADO (hipótesis), junto con las N de juicio de la etapa 1. El CAMBIO no puede impedir que una fase recoja ese razonamiento de 2026. Conviene que la orquestación lo advierta a las fases.
- `verificacion_entradas.json` se conserva, como en los precedentes. Quedará no vigente en las celdas cambiadas hasta su nueva revisión.
- Formato de las cifras en los textos: «232.476810 millones» y «5621.2892658 mm» mezclan separadores y pueden leerse mal. Los campos `valor` son numéricos y correctos.

## 8. No comprobable o pendiente de la persona responsable

1. **El cupón de la OCEANE dentro de «Net interest paid» (2023–2025):** no está desglosado en el URD (p. 327 y p. 312). Es una inferencia.
2. **Los 2,4 que vencen en 2026** (p. 383) como interés devengado: es una interpretación, aunque cuadra con 380 × 2,25 % × 100/365 ≈ 2,34.
3. **Precio y fecha en una base 2025:** la decisión no dice qué precio usar. El CAMBIO conserva el del 4-nov-2026 (24,18), y con él la tasa sin riesgo, C38 y C97 de 2026, con las fechas declaradas. La alternativa sería el cierre de 31-dic-2025, 24,26 € (URD 2025 p. 447 y 441). Lo tiene que confirmar la persona responsable.
4. **Pensiones H25 y anteriores:** posible ruptura de concepto (§4). Está fuera de I25:L25 y no lo he podido comprobar con el DEU 2022.
5. **Diferencia de 930 acciones propias** entre la sociedad matriz (p. 415: 132.480 + 240.228 = 372.708) y el consolidado (371.778). Sin explicación en las fuentes. Es inmaterial: 0,0004 % de C55.
6. **Ejecución real:** no he ejecutado `cambiar_base.py`, el pipeline ni LibreOffice. Lo que digo de la fase 1 (C42 fresca, columna I no reescrita) sale de leer el código, no de ejecutarlo.

---

## Confirmación de D1 y D2 (CAMBIO corregido por la orquestación; RE6, 14-nov-2026)

- **Qué he comparado:** el CAMBIO actual frente a `cambio_decisiones_elis_4_14.antes_revision_RE6.json`, campo a campo. Solo cambian 10 campos:
  - la nueva clave `_revision`;
  - la columna I de C46, C47 y C50 (en `analisis.*.evidencia`);
  - la columna I de C48 y C49 (en `evidencia`);
  - la N de C88 (en `evidencia`);
  - tres patrones nuevos en `textos_prohibidos`.
- **Lo que no cambia:** ningún valor, ninguna fuente, ningún metadato, ninguna corrección de pensiones ni ninguna nota.
- **D1: CORREGIDA.**
  - Las filas 43 (C46), 44 (C47), 45 (C48), 46 (C49) y 48 (C50) pasan a tener I = «Informe anual auditado (URD 2025; DEU 2024; URD 2023), ejercicios 2023–2025 · (E6, base 31-dic-2025: sin la nota de prensa del primer semestre de 2026)».
  - Confirmo que la fila 46 (C49) también tenía «+ NP»; está bien añadirla.
  - Las cinco filas existen en el Control maestro de la etapa 1 y la columna I es una columna permitida.
- **D2: CORREGIDA.**
  - La N de la fila 73 (C88) conserva los datos históricos de la etapa 1: «Sin 2020: 16,0x media / 14,7x mediana; 2021–25 14,5x / 14,6x. Es contexto, no juez.».
  - Retira los múltiplos «actuales» de base 30-jun-2026 y pro forma, y lo declara.
  - El valor de C88 no cambia.
- **Patrones nuevos (`Actual 17,6x`, `19,3x \(pro forma\)`, `auditado \+ NP`):**
  - En la etapa 1 y en el libro de datos solo casan con I43, I44, I45, I46, I48 y N73, que ahora se reescriben.
  - No casan con ningún texto nuevo del CAMBIO.
  - No casan con ninguna nota que quede en `fase1_metadatos.json` ni en `fase1_v63.json`.
- **Simulación repetida** (libro de datos + evidencia del CAMBIO + lo que escribe la fase 1, incluidas las celdas «frescas»; filas 17–82 y 107–175; G:M en juicio y E:N en dato), con los 16 patrones: **0 restos**. Fuera de la evidencia activa solo quedan los dos informativos ya conocidos (F5 y D88).
- **Precio (4-nov-2026 con acciones de 2025):** se aplica el mismo criterio que en Viscofan. Allí el CAMBIO se basa en la decisión D3 de la persona responsable y declara que el precio es del 3-nov-2026 y las fechas son distintas. El CAMBIO de Elis lo declara igual. Lo saco de «pendiente» y lo dejo como criterio declarado, porque la orquestación lo ha extendido a Elis.

**Discrepancia menor que introduce la corrección de D1:**
- El texto de I atribuye las cifras también al «URD 2023». Las medias usan el comparativo reexpresado del DEU 2024 para 2023, como citan las propias fuentes del CAMBIO.
- El URD 2023 (p. 279) da otras cifras para 2023:
  - «NET CASH FROM OPERATING ACTIVITIES 1,325.7» frente a 1.325,6;
  - «Net interest paid (including interest on lease liabilities) (90.2)», un concepto distinto del 70,5 que usa C48.
- Para C48 en particular el URD 2023 no es fuente.
- Lo esperado: quitar «URD 2023» del texto de I, o aclarar que es el informe original y que las cifras de 2023 son el comparativo del DEU 2024.
- No afecta a ningún valor ni deja restos de 2026.

**Resultado tras la confirmación:**
- D1 y D2 quedan corregidas y la simulación da 0 restos.
- El resultado se mantiene en **«discrepancia»** solo por la atribución del URD 2023 en la columna I, que es textual.

**Confirmación final (RE6, 14-nov-2026): VERIFICADO.** La columna I de C46, C47, C48, C49 y C50 dice ahora «Informe anual auditado: URD 2025 (ejercicios 2025 y 2024) y DEU 2024 (comparativo de 2023)…» y coincide con las fuentes. 2024 y 2025 salen del URD 2025: p. 327, 314 y 366. 2023 sale del comparativo «2023 retraité» del DEU 2024: p. 273, 259 y 312. Ningún valor, metadato ni corrección cambia, y la simulación sigue en 0 restos con los 16 patrones. El CAMBIO queda verificado.
