# Revisión independiente de las entradas financieras de Vidrala (4.14)

**Revisor:** revisor independiente R-Vidrala (Claude, contexto separado del extractor). **No es una revisión humana.** Fecha: 14-nov-2026.

- **Registro revisado (copia):** `/home/claude/trabajo_4_14/agentes/R_vidrala/Vidrala/verificacion_entradas.json`.
- **Qué se cambió:** solo el bloque `comprobacion` de cada entrada; el campo `extractor` se conserva. Además se añadió la `incidencia` de la hipótesis Análisis!C49, como permite el encargo. No se tocó ningún otro campo ni el registro del extractor.
- **Scripts:** `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/R_vidrala/`. Solo sirven para mostrar páginas y volcar las notas. Cada nota recoge lo que el revisor leyó en la página.

## 1. Recuento

| Resultado | Celdas del universo (226) | Auxiliares (119) | Total (345) |
|---|---|---|---|
| verificado | 219 (175 datos + 44 hipótesis/convenciones) | 116 | 335 |
| discrepancia | 3 | 0 | 3 |
| pendiente | 4 | 3 | 7 |

Se abrieron las 61 páginas citadas, todas ellas.

## 2. Discrepancias

| Celda | Libro | Valor correcto según la fuente | Ubicación | Efecto |
|---|---|---|---|---|
| Análisis!C46 (CFO medio) | 335,4 | **335,413** = (263,437 + 362,516 + 380,287) ÷ 3 | CF_2024 p.7 (columna 2023(*)); CF_2025 p.7 | +0,013 mm en el FCF base, solo motor A. **Nulo en el motor B activo.** |
| Análisis!C47 (capex medio) | 169,7 | **169,668** = media de 151,700, 168,800 y 188,503 | CF_2024 p.7; CF_2025 p.7 | +0,032 mm en el FCF base (C46 y C47 juntos: 161,2 → 161,245; unos 0,001 €/acción al año), solo motor A. **Nulo en B.** |
| Historia!F8 (D&A 2019) | 97,091 | **91,088**: solo «Amortisation and depreciation»; el deterioro de 6,003 va en línea aparte, y los otros nueve años lo excluyen | CF_2020 p.13, columna 2019 (también CF_2019 p.12 y CF_2020 p.10) | −6,003 mm. 2019 queda fuera de la ventana del FCF base y de la de D_hist (2021–2025). **Sin efecto en el valor.** |

## 3. Pendientes (con motivo)

1. **Análisis!C48 y aux:intereses_financiacion_2023/2024/2025: el cero se infiere, no está impreso.**
   - **Qué hay en la fuente:** el bloque de financiación no tiene línea de intereses. Así es en el texto inglés y en el original español: ES 2025 p.14 y ES 2024, doc. 2118, p.14. Su total cuadra con sus líneas. El ESEF 2025 solo etiqueta `InterestPaidClassifiedAsOperatingActivities`.
   - **Por qué queda pendiente:** los pagos por arrendamientos van dentro de los flujos de «loans and borrowings» (cuadro NIC 7, CF_2025 p.67). La fuente no dice si su interés (2,131, 2,179 y 2,452 miles) está en «Interest paid» o en financiación.
   - **Efecto posible:** C48 sería 2,254 mm; el FCF base del motor A bajaría 2,254 mm, unos −0,06 €/acción al año. Nulo en B.
   - **Incidencia de clasificación:** ver §4.
2. **Historia!J14 (circulante 2023 = 78,805): perímetro, P7.**
   - **La cifra está bien leída:** se comprobó en el PDF renderizado y en el español de 2024.
   - **La diferencia del extractor se confirma, con matiz:** la reexpresión llevó 11,061 de partidas no monetarias de Italia a «Otros activos y pasivos corrientes y no corrientes». El original consolidado es (89,866), en CF_2023 p.7.
   - **El matiz:** corregir J14 sola sería incoherente con J8 (87,210, de continuadas). Las parejas coherentes son (87,210; 78,805) y (97,865; 89,866), y en D_hist difieren solo 0,41 mm. La decisión es humana.
   - **Hallazgo nuevo:** en la traducción inglesa de CF_2024 p.7, tres líneas de ajustes de 2023 están copiadas de 2022 y no suman 158,414. El español sí cuadra.
3. **Historia!K14 (circulante 2024 = 84,994): el concepto está contaminado (hallazgo nuevo).**
   - **P1 confirmado:** el español imprime (106.417).
   - **El problema:** el beneficio de 2024 incluye una plusvalía de unos 50 mm por la venta de Italia (CF_2025 p.31), y ninguna línea de ajustes la elimina. Lo previsible es que esté dentro de «Otros activos y pasivos…» (−106,417).
   - **Si es así:** unos 50 mm de la cifra no son circulante. Se trata de una inferencia del revisor; la fuente no publica el circulante limpio.
   - **Efecto:** la fila entra en D_hist de la V6.4. Restando 50 mm, f pasaría de 1,165 a unos 1,185. Cota grosera: hasta unos −0,8 €/acción en B; no está recalculado.
4. **Historia!K13 (adquisiciones 2024 = −241,668): tratamiento.**
   - **Las cifras son correctas:** 230,000, 11,668 y (6,000).
   - **Lo que no está acreditado:** la nota de interrumpidas atribuye a Italia solo 230,000 de flujos de inversión, así que no consta que los 11,668 pertenezcan a la venta. Además, se excluyen 6,000 de participaciones por puesta en equivalencia.
   - **Alternativas:** −230,000, −224,000 o −235,668.
   - **Efecto:** entra en D_hist; f bajaría entre 0,004 y 0,006. Cota grosera: hasta unos 0,25 €/acción; no está recalculado.

## 4. Incidencias de clasificación

- **aux:intereses_financiacion_2023–2025:** no son «cero_comprobado». La cita es el total de financiación y no tiene ningún «0» ni «-». Es un cero por conciliación (derivado) o un dato ausente. Por eso el comprobador los marca como discrepancia de cita.
- **Análisis!C49 (4,5, hipótesis):** en la práctica es un derivado. En la nota 8, el pago incluye el interés devengado, como muestra el movimiento del saldo, así que principal ≈ pago − interés = **4,510**. La diferencia con el libro es −0,010 mm, inmaterial. Se registró la incidencia.
- **Campo `uso` incompleto:**
  - Las filas 8, 12, 13 y 14 de la Historia (2021–2025) entran en D_hist del motor B experimental: D_hist = capex − amortización 229,4 + adquisiciones 12,4 + cartera 9,4 + circulante 278,8 (fase_c.json).
  - El `uso` de las filas 8, 12 y 14 dice «motor A».
- **Perímetro mezclado dentro de D_hist (observación):** el capex y el CFO de 2023–2024 incluyen Italia, mientras que la D&A de 2023–2024 es de continuadas.
- **Sin hipótesis ni convenciones que sean datos publicados disfrazados,** salvo C49. H23 y C50 están bien clasificadas.

## 5. Valoración de las diferencias que declara el extractor

| Celda | Valoración del revisor |
|---|---|
| C46 y C47 | Confirmadas: son redondeos heredados, inmateriales. |
| F8 | Confirmada. |
| C48 | De acuerdo con dejarla pendiente. Además, el cero de sus orígenes está mal clasificado. |
| C49 y C50 | De acuerdo. A C49 le añade la incidencia de clasificación. |
| J14 (P7) | Confirmada. Pero corregirla requiere mover J8 en la misma decisión. |
| P1 (K14) | Correcto en signo, aunque el concepto es dudoso (§3). |
| I14 | Confirmada, incluida la errata 132,341 de CF_2022. |
| G23 | Confirmada la errata del rótulo. |
| B46–B48 | Confirmados: los ceros están impresos. |
| K13 | Confirmada la duda. Además, la nota de interrumpidas no respalda los 11,668. |

**Análisis!C37 (precio 90,10):**
- **Qué dice la fuente:** ES 2025 p.97 dice «La cotización de la acción cerró 2025 en 90,10 euros» y el cuadro da «Cotización a cierre del periodo · 2025 · 90,10». Se comprobó en el PDF renderizado.
- **Fecha:** coincide con la que declara el modelo, 2025-12-31.
- **Resultado:** verificado, con dos límites:
  - es una fuente secundaria, no el boletín de BME (D-N6);
  - la celda se rotula «Precio actual», pero la ejecución es de 2026-11-12. Un precio posterior exigiría otro número de acciones, porque hay una ampliación liberada de 2026.

**Otras observaciones (no cambian valores):**
- En 2022, los movimientos de «Personnel» suman 222 frente a un saldo impreso de 262. Se usa el saldo impreso, que cuadra con el balance.
- La nota 8 repite los pagos de arrendamiento como «gasto de arrendamientos a corto plazo».

## 6. Resumen del comprobador (sobre la copia del revisor)

| Concepto | Resultado |
|---|---|
| Universo | 226 |
| Comprobadas | 335 (incluye las 44 hipótesis y convenciones) |
| Auxiliares | 119 |
| Pendientes | 4: C48 (por su origen), J14, K14 y K13 |
| Discrepancias | 6: C46, C47, F8 y las tres citas sin cero de aux:intereses_financiacion |
| Errores | 0 |
| Desactualizadas | 0 |
| Sin entrada, sobrantes o repetidas | 0 |
| Materiales sin comprobar | 7 |
| Apto por entradas | **False** |

## 7. Límites

- **PDF:** no hay PDF en el expediente. Se renderizaron copias que están en `/home/claude/trabajo_4_14/agentes/D1/arbol/munger_v2_r1/…`. Sus huellas no figuran en el expediente; su texto coincidió con los .txt en las páginas contrastadas.
- **Páginas renderizadas:**
  - CF_2018 p.13;
  - CF_2019 p.12;
  - CF_2022 p.30;
  - CF_2024 p.7;
  - ES 2025 p.97.
- **Resto de 2016–2022:** se revisó solo sobre los .txt. La alineación de columnas se contrastó con totales y sumas de líneas.
- **Versiones españolas:** no se dispuso de las de 2016–2023.
- **Efectos en €/acción:** no se recalculó el libro (estaba prohibido), así que los efectos de §3 en B son cotas groseras.
- **Alcance de la revisión de hipótesis:** no se auditó el juicio económico de las hipótesis; solo su naturaleza.
