# Informe del personaje · revisión financiera del piloto Vidrala (entrega 4.3, 8-nov-2026; armonizado en la 4.3.1, 9-nov-2026)

Este informe aplica el procedimiento de `personaje_v2/personaje_munger_v2.md` a las entradas financieras del piloto. Está escrito en tercera persona, como pide el encargo, aunque el personaje habla en primera persona en las fases.

Es un **expediente separado**: no modifica `fase_a.md`, `fase_b.md`, `fase_c.md`, `informe.md`, el libro ni ninguna decisión. Las cifras salen de dos scripts:
- `scripts/revision_financiera_vidrala.py`: 217 comprobaciones, todas cumplen; sin cambios en la 4.3.1;
- `scripts/subsanacion_entradas_fechas.py`: 43 comprobaciones, nuevo en la 4.3.1.

Las fórmulas están en `ANEXO_REPRODUCIBLE.md`. La clasificación de las entradas del motor B y el análisis de fechas están en `ENTRADAS_Y_FECHAS.md`. La relación entre cada precisión de la subsanación y su resolución está en `NOTA_SUBSANACION_4.3.1.md`.

Cada afirmación lleva su categoría:
- **[Hecho]**: comprobado en un documento o en el libro.
- **[Interpretación]**: lectura razonada de los hechos.
- **[Propuesta]**: recomendación pendiente de decisión.

Importes en millones de euros (mm) salvo que se indique otra cosa.

---

## 1. Diagnóstico en una página

**1. La `f = 0,0199` del libro es un artefacto.** [Hecho]
- El libro combina el CFO real de 2024 (362,516) con un circulante de 2024 que no sale del estado de flujos (−127,840, por la lectura errónea de «106,417)»; piloto, P1).
- Si se usa el circulante de 2024 del mismo estado (84,994), `f` pasa a **−0,0276**.
- El «✓ PASA» del semáforo y la frase de la fase A «f = 0,020 está en rango» descansan en ese error.

**2. Unas dos terceras partes de esa `f` negativa son la Italia vendida.** [Hecho e interpretación]
- Si el circulante sale del mismo estado que el CFO, se anula con él, y `f` mide NOPAT + D&A de continuadas frente al flujo antes de circulante del estado de flujos.
- Ese flujo incluye el beneficio de discontinuadas: 19,559 en 2023 y 60,065 en 2024. Los 60,065 son 9,518 de Italia en el primer semestre más **50,547 de plusvalía no monetaria**.
- En la ventana, eso pesa **−0,0178** de los −0,0276.
- Proyectar esa `f` como porcentaje de las ventas futuras sería proyectar como recurrentes el negocio vendido y su plusvalía.

**3. Con el perímetro de continuadas, `f` sigue siendo negativa: −0,009847, condicionada a los supuestos de T3.** [Hecho aritmético bajo supuestos]
- La cifra se reproduce exactamente, pero depende de dos supuestos:
  - **δ = 0.** Es una hipótesis: no se publica la parte de Italia en los intereses e impuestos pagados del grupo.
  - **El circulante de continuadas (85,978 en 2023 y 36,487 en 2024) es derivado**, un residuo, no una cifra publicada.
- La variante T3δ (−0,010747) toma esa parte igual a lo devengado por Italia. Es una **sensibilidad condicionada, no una cota** del pago. No hay ningún intervalo demostrado para `f` de T3.
- La revisión del problema de perímetro está hecha. Su cuantificación sigue con incertidumbre y su aplicación, pendiente.
- Lo que deja negativa esa `f` son partidas en las que el devengo y la caja no coinciden en el año:
  - **partidas no monetarias de continuadas: −0,0124**, sobre todo provisiones de derechos de emisión y deterioros; en 2023, también el resultado por puesta en equivalencia de Vidroporto;
  - **impuesto corriente no pagado en el año: −0,0064**: 18,2 en 2023 y 15,4 en 2025.
- Esas partidas superan a las fugas reales: **intereses netos pagados (+0,0086)** y **arrendamientos (C49, +0,0030)**.
- [Interpretación] **No está acreditado que esas diferencias se repitan, y tampoco está demostrado que no se repitan.** El personaje no las proyecta como perpetuas sin evidencia, porque su procedimiento pide investigar, no extrapolar, los «impuestos pagados que bajan como porcentaje del beneficio» y la «caja que no cuadra con el beneficio declarado» (PCA pp.390–392; HIM). Qué evidencia fundamentaría o descartaría una normalización: §3.6.

**4. La ventana 2023–2025 mezcla tres regímenes de financiación.** [Hecho]
- 2023: Vidroporto consolidada solo desde diciembre; intereses netos de 4,5.
- 2024: deuda alta y venta de Italia; intereses netos de 20,9.
- 2025: deuda baja; intereses netos de 13,3.
- Deuda con arrendamientos: 599,0 → 393,3 → 262,9. A 30-jun-2026, 409,6 según el contexto de Análisis C54.
- La convención 10 de la V6.3 dice: «si la financiación cambia mucho, usa el motor B».

**5. La justificación del motor A ya no se sostiene.** [Interpretación] Sus dos apoyos eran:
- «f = 0,020 está en rango»: es el artefacto del punto 1;
- «los intereses son pequeños frente al flujo»: es cierto, pero no basta, porque lo que mueve `f` no son los intereses.

**6. Recomendación del personaje, en tres niveles separados** (§6). [Propuesta]
- **Método:** el motor B sigue siendo el preferente (C62 = «No · financiación cambia mucho»). La razón es metodológica: `f` no puede representar fugas recurrentes con los datos acreditados de la ventana, y la financiación cambia mucho dentro de ella. Cambiar de motor **no resuelve** las fechas, las acciones, Toro, L25, L26 ni el carácter de `r_op`.
- **Reejecución exploratoria:** los datos bastan para una reejecución con base 2025 (ruta A), con condiciones declaradas. Su resultado no puede compararse con el precio del 3-nov-2026.
- **Valoración comparable con el precio:** la evidencia **no basta** (ruta B). Faltan las acciones a la fecha del precio, el cierre oficial y la fecha sin derecho de la liberada, los saldos de 2026, Toro y las distribuciones de 2026.

**[Corrección de la 4.3]** La 4.3 afirmaba que «no falta ninguna evidencia» para el motor B y que no quedaba ninguna conclusión impedida por sus entradas. La afirmación era demasiado amplia y se retira (§5.2, §7 y `ENTRADAS_Y_FECHAS.md`).

**7. Hallazgo colateral, material para la fase B.** [Hecho]
- La misma corrección P1 cambia la referencia mecánica del S2C marginal (Historia C53) de **1,55 a 0,92**.
- La cuenta con la que la fase B justificó el S2C del NORMAL (≈1,0) usaba una reinversión orgánica de 295 mm que contiene el error. Con P1 serían 508 mm y la cuenta daría ≈0,59.
- El S2C es una palanca y no se recalcula aquí. Pero su apoyo factual cambia, y la fase B tiene que volver a decidirlo con cualquier motor.

---

## 2. Cómo se ha aplicado el procedimiento del personaje

**Qué se ha hecho:**
- Se ha leído entero `personaje_munger_v2.md`.
- Se han usado las reglas que aplican a esta revisión:
  - las cuatro clases de supuesto (§9);
  - lo heredado es hipótesis y no hecho (§13): el «f = 0,020» de la fase A se revisa como hipótesis;
  - qué buscar en las notas: la caja que no cuadra con el beneficio, los impuestos pagados que bajan y los cargos «extraordinarios» (§3);
  - el motor como hipótesis material (§14);
  - los estados y el orden de mando (§15).
- Se han releído, sin modificarlas, las partes pertinentes de:
  - **fase A:** motor, gestión, «qué caja espero»;
  - **fase B:** S2C, C76 y C44;
  - **fase C:** el S2C medido «por mal camino», la base de 161,2 y la lista de hipótesis.

**Qué no se ha hecho:**
- No se ha recalculado ninguna celda de datos, no se ha cambiado la base del FCF en el libro y no se ha ejecutado `construir`.
- No se han tocado r, las probabilidades ni los escenarios.
- No se ha calculado ninguna valoración con ningún motor.
- Las réplicas de `f` son aritmética de las fórmulas del libro. **No son valoraciones ni acreditan las hipótesis.**

---

## 3. La cadena, eslabón a eslabón

### 3.1 Datos históricos y su perímetro

La matriz completa está en `MATRIZ_DE_COHERENCIA.md`. En resumen:

| Entrada (fila de Historia) | 2023 | 2024 | 2025 | Entra en |
|---|---|---|---|---|
| Ventas (6), EBIT (7), tipo (10) | Continuadas (reexpresado) | Continuadas* | Consolidado = continuadas | C74 (V); C75 (NOPAT) |
| D&A (8) | Continuadas | Continuadas | Consolidado | **C76 (reinversión)**, no NOPAT |
| CFO (11) | **Incluye Italia** (+26,732 de explotación) | **Incluye Italia** (+11,558) y la plusvalía en el beneficio | Consolidado | C46 → C52 → C70 (FCF base) |
| Capex (12) | Incluye Italia (altas de Italia: 4,315) | Puede incluir Italia del 1S (no publicado) | Consolidado | C47 y C76 (se anulan en `f`) |
| Circulante (14) | Incluye 11,061 de ajustes no monetarios de Italia | **Libro −127,840: error**; fuente 84,994, que incluye la reversión de la plusvalía | Consolidado | C76 |

\* La cuenta de 2024 de continuadas incluye un segmento «Italia» con ventas de 17,016 y BAI de 2,139 (ES24 p.37), cuya naturaleza no explican los documentos. Pesa un 1,1 % de las ventas. Es la pregunta 7 de `DECISIONES_PENDIENTES.md`.

**[Hecho]** Ventas, EBIT, D&A y tipo de 2023 se han contrastado ya línea a línea en la cuenta reexpresada (ES24 p.11 y p.14). Con eso se cierra PE11.

**[Hecho] La venta de Italia** se formalizó el 4-jul-2024 por 230 mm.
- La plusvalía es de 50 mm (ES24 p.42; EN25 p.31; también en el ESEF 2025, versión española).
- Las diferencias permanentes del impuesto de 2024 (−28,095) son «principalmente» la exención de esa plusvalía (ES24 p.69).
- Ninguna línea de ajustes del estado de flujos de 2024 revierte la plusvalía. Los ajustes son solo de continuadas: amortización 117,720 e impuesto 64,968.
- [Interpretación] Por eliminación, la reversión está en «Otros activos y pasivos corrientes y no corrientes» (−106,417), la misma línea cuyo paréntesis perdido originó P1. El ESEF la etiqueta como `AdjustmentsForIncreaseDecreaseInOtherOperatingPayables` y no la desglosa.
- Esta interpretación no cambia ninguna réplica: el tratamiento de continuadas resta la plusvalía del flujo antes de circulante, esté donde esté su reversión.

### 3.2 NOPAT y reinversión

**[Hecho, corrección de documentación pedida por el encargo]**
- **NOPAT (C75)** = media de EBIT × (1 − t): depende de la fila 7 y de la fila 10.
- **D&A** entra en la **reinversión (C76)** = media de (capex − D&A + circulante), **no en el NOPAT**.
- La entrega 4.2 decía que el perímetro de la columna 2023 «afecta a f (NOPAT medio y reinversión media de C75 y C76)» y anotaba D&A como «C76, NOPAT y reinversión». Se ha corregido en esos documentos, con nota de la entrega 4.3.

**[Hecho] Identidad comprobada** (sin residuo, en `ANEXO_REPRODUCIBLE.md`, §2):

`f·V = media(NOPAT + D&A − (CFO + circulante)) + C48 + C49 + C50 + redondeos de C46 y C47`

Tres consecuencias:
1. **El capex se anula.** La fila 12 y C47 entran con signo opuesto, así que la composición del capex no altera `f`. Sí altera el nivel del FCF base.
2. **El circulante solo importa emparejado con el CFO.** Si los dos salen del mismo estado, su suma es el flujo antes de circulante (FAC) = beneficio + ajustes + intereses cobrados − intereses pagados − impuestos pagados. Por eso elegir entre 78,805 y 89,866 en 2023 no es la cuestión: cada cifra va con su propia presentación del estado de flujos. La pregunta P7 de la 4.2 queda absorbida aquí.
3. **La diferencia anual se descompone sin residuo** en cuatro partes: discontinuadas, partidas no monetarias de continuadas (X), impuestos y intereses netos.

### 3.3 FCF base y flujo implícito: ¿definiciones y periodos compatibles?

**[Hecho] No lo son.**
- El FCF base (C52 = 161,2) parte de CFO y capex consolidados con Italia en 2023 y 2024.
- El flujo implícito (C77) parte de EBIT, tipo y D&A de continuadas.
- Coinciden en los años (2023–2025), no en el perímetro.
- Es el riesgo que la réplica independiente de la V6.2 dejó escrito: «f absorbería una diferencia de perímetro además de las fugas reales, y proyectarla como % constante de ventas no estaría justificado» (`v6/docs/Replica_independiente_V6_2.md`).

**[Hecho] El flujo de inversión de Italia no es su capex.**
- Las «Investments» de Italia en 2023 (altas de inmovilizado material e intangible) fueron 4,315 (EN23 p.30). Su flujo de inversión fue −28,371 (ES24 p.43).
- Restarlo como capex habría quitado ≈24 mm de más.
- El capex de Italia del primer semestre de 2024 no se publica.
- Conclusión: **el FCF base de continuadas no es determinable con evidencia**. Una réplica condicionada, que toma las altas de 2023 como capex y 0 en 2024, da ≈149,9 frente a 161,2. No es un dato.
- [Interpretación] La fase A («qué caja espero») y la fase C (D66) razonan sobre una base de 161,2. Su orden de magnitud no cambia, pero su perímetro sí.

### 3.4 Conciliación de `f`: qué hay dentro

Medias de la ventana 2023–2025 (mm/año) y peso en `f` (÷ 1.493,6 de ventas medias):

| Componente | mm/año | `f` | Naturaleza |
|---|---|---|---|
| Discontinuadas: Italia y plusvalía | −26,54 | −0,0178 | **Perímetro.** Que no se repite es un hecho: el negocio está vendido y la plusvalía es de una sola vez |
| X: provisiones (11,5), deterioros (5,8), subvenciones (−2,6), puesta en equivalencia (2,2) y otros | −18,59 | −0,0124 | **Devengo.** No monetario en el año. Dónde y cuándo va su caja no está acreditado; su recurrencia, tampoco, ni en un sentido ni en otro |
| Impuestos: corriente no pagado en el año | −9,63 | −0,0064 | **Calendario (interpretación).** 18,2 en 2023, −4,7 en 2024 y 15,4 en 2025. Que se revierta no está acreditado; que se repita, tampoco |
| Impuestos: diferido y ajustes | −0,78 | −0,0005 | **Devengo** (2025: +11,2 por amortización acelerada) |
| Impuestos: devengado − t·EBIT | −3,16 | −0,0021 | **Escudo fiscal de la financiación** y redondeo de t |
| Intereses netos pagados | +12,91 | +0,0086 | **Fuga real** al acreedor |
| C49, arrendamientos (4,5) | +4,50 | +0,0030 | **Fuga real**, en cuantía hipotética |
| Redondeos de C46 y C47 | +0,05 | +0,0000 | Técnico |
| **Total = T1** | **−41,24** | **−0,0276** | |

Por año (g + C49, sobre las ventas de cada año):

| Año | Con T1 | Con perímetro de continuadas (T3, condicionada) |
|---|---|---|
| 2023 | −0,026 | −0,013 |
| 2024 | −0,041 | −0,003 |
| 2025 | −0,014 | −0,014 |

**[Hecho]** El año con perímetro limpio (2025) tampoco da una `f` positiva con T3: el impuesto pagado (40,8) quedó muy por debajo del corriente (56,1) y del devengado (67,3).

**[Interpretación]** Cambiar la ventana no resuelve nada, y no se propone hacerlo.

### 3.5 Uso en las proyecciones

**[Hecho]** En el motor A, el flujo anual es `V_t·[m_t·(1−τ) − f] − ΔV/S2C`, y el terminal resta `f` también (Convenciones V6.3).

- Una `f` negativa **suma** caja al accionista cada año, en proporción a las ventas y a perpetuidad.
- El FCF base solo influye en el valor a través de `f`. Además alimenta el DCF inverso (C86) y los ratios de contexto (FCF yield y precio ÷ FCF).

**[Interpretación] Qué se proyectaría con cada tratamiento:**
- **T1:** el beneficio de un negocio vendido y una plusvalía de una sola vez. Que no se repiten es un hecho.
- **T3:** que, en proporción a las ventas y para siempre, la empresa pagará menos impuesto del que devenga y sus partidas no monetarias superarán a su caja.

Esa segunda proyección no está acreditada. Tampoco está demostrado lo contrario. Con estos documentos, el personaje no puede fundamentarla en ningún sentido: en las cuatro clases de §9 sería un supuesto «sin juicio propio».

### 3.6 Recurrencia de los impuestos y las provisiones: qué se sabe y qué falta

| | Impuestos (corriente no pagado; diferido) | Partidas no monetarias (sobre todo provisiones de derechos de emisión) |
|---|---|---|
| **Comprobado** | Corriente, pagado y devengado de 2023–2025 (ES24 p.69; EN25 p.56; script 217, §6). Medias: corriente no pagado 9,63/año; diferido y ajustes 0,78/año | Líneas de ajuste de 2023–2025 (ES24 p.14; EN25 p.7). Movimiento de la provisión de 2025: cargo 49,5 y «pagos» de 50,7, que son entregas de derechos (EN25 p.71–72) |
| **Interpretación del personaje** | Parece sobre todo calendario de pagos. El diferido de 2025 (11,2) apunta a la amortización acelerada | El coste devengado de CO₂ se liquida entregando derechos (gratuitos o comprados). La caja de los comprados puede estar en el capex de intangibles o en el circulante |
| **Evidencia que fundamentaría una normalización** (tratarlo como no recurrente) | Saldos de impuesto a cobrar y a pagar de 2023–2025 que muestren la reversión; calendario de pagos fraccionados; una serie de 2016–2022 en la que el pagado converja con el corriente | Una serie plurianual en la que el ajuste por provisiones oscile alrededor de cero; separación de derechos gratuitos y comprados y dónde va la caja de los comprados |
| **Evidencia que la descartaría** (tratarlo como recurrente) | Pagado sistemáticamente por debajo del corriente durante muchos años, o diferido creciente por inversión sostenida | Ajuste positivo persistente sin una salida de caja equivalente en otra línea |
| **Dónde está** | Informes anuales de 2016–2022 (no conservados en el paquete) y notas fiscales; pregunta 8 | Notas de provisiones e intangibles de varios años; pregunta 9 nueva |

**[Hecho]** No se elige otra cifra de `f`. T4 (+0,0095) es solo un contraste que supone la normalización; no es una propuesta.

---

## 4. Arrendamientos

**[Hecho] Qué miden las cifras en juego.**
- **4,5** = media de (pagos − interés devengado) de 2023–2025 = 4,51. Es la hipótesis de que los pagos incluyen intereses y el principal es el resto.
- **6,8** = media de los pagos totales = 6,76.
- **La fila 17 de Historia** recoge pagos totales, no principal.
- No se publican el principal ni el interés pagado, y ninguna línea del estado de flujos se identifica como de arrendamientos.
- «Pagos de intereses» está etiquetado como intereses pagados de explotación en el ESEF 2025.
- Las líneas de deuda de financiación de 2024 y 2025 suman la variación del saldo de préstamos con arrendamientos incluidos (entrega 4.2). Es un indicio de que el flujo de los arrendamientos está dentro de esas líneas, no una acreditación.

**Evaluación de cada tratamiento con el motor A:**

| C49 | Evidencia | Supuesto adicional | Riesgo | Efecto en `f` (sobre T3) |
|---|---|---|---|---|
| 4,5 (vigente) | Pagos y devengo de la nota 8 | Que el interés de arrendamientos esté en «Pagos de intereses» (explotación) y el principal en financiación | Omisión de ≈2,3/año si el interés también va en financiación | −0,0098 (T3, condicionada) |
| 6,8 | Pagos de la nota 8 | Que todo el pago (principal e interés) vaya en financiación | Duplicación de ≈2,3/año si el interés ya está en explotación | −0,0083 |
| 0 | Repetición de los pagos como «gasto a corto plazo» en la nota 8 | Que los pagos estén dentro del CFO | Omisión de 4,5–6,8/año si están en financiación; contradice el indicio de la NIC 7 | −0,0129 |

**[Propuesta]**
- **Con el motor B (preferente) no hace falta C49.** El pasivo por arrendamientos (49,3; nota 8; incluido en Historia L22 + L23 = préstamos del balance) se resta como deuda. Con la NIIF 16, el EBIT va después de amortizar el derecho de uso y antes del interés, así que restar el pasivo no duplica nada.
  - Riesgo residual: si la línea de la nota 8 que repite los pagos como gasto a corto plazo fuera un gasto real, habría una duplicación pequeña en el EBIT. La pregunta 3 lo resolvería.
- **Con el motor A no se puede recomendar ninguna cifra con evidencia.** Se mantiene 4,5 como **hipótesis pendiente**. Las tres cifras dan, con T3, entre −0,0129 y −0,0083 de `f`. No es un intervalo demostrado: es la sensibilidad a tres supuestos de clasificación, todos bajo los supuestos de T3. Con ninguna de ellas cambia el signo, así que los arrendamientos no son lo que bloquea.

**[Hecho] Conclusión impedida mientras dure la incertidumbre:** no puede afirmarse que el FCF base y `f` estén libres de una omisión o una duplicación de hasta ≈2,3 mm/año (entre 4,5 y 6,8), ni de hasta 4,5 si los pagos estuvieran en el CFO. Tampoco puede presentarse C49 como dato.

Las preguntas 1–3 de `DECISIONES_PENDIENTES.md` resolverían esto. No se ha enviado ninguna.

---

## 5. Adecuación del motor

### 5.1 Motor A: por qué deja de sostenerse

La fase A lo justificó así (`fase_a.md`, «Gestión»): «la financiación sube con cada compra y vuelve a niveles bajos… los intereses son pequeños frente al flujo y f = 0,020 está en rango». Con la evidencia nueva:

- **«f = 0,020 está en rango».** [Hecho] Es el artefacto de P1. Con el dato corregido, −0,0276 está fuera de rango: la gramática daría el aviso A6 («la fase A revisa el FCF base y considera el motor B»). Con el perímetro de continuadas (T3, condicionada), −0,0098 está dentro del rango, pero es negativa por partidas que no son fugas y cuya recurrencia no está acreditada (§3.4 y §3.6).
- **«La financiación sube y vuelve a bajar».** [Hecho] Es exactamente un patrón de financiación que cambia mucho. Ocurre dentro de la misma ventana con la que se calibra `f`: compra de Vidroporto en diciembre de 2023, venta de Italia y dividendo extraordinario en 2024, desapalancamiento hasta 0,36 × EBITDA en 2025 y nueva deuda en 2026 (Toro y recompras).
- **«Los intereses son pequeños frente al flujo».** [Hecho] Lo son: +0,0086 de `f`. Pero las partidas que mueven `f` son tres o cuatro veces mayores y no son financiación.
- **[Interpretación] La plantilla no tiene una celda para normalizar `f`.**
  - C43 y C44 solo actúan con un FCF base ≤ 0.
  - Para que `f` del motor A recogiera solo las fugas reales habría que escribir en las celdas de datos de CFO o de circulante valores que no son los publicados. El personaje no lo hace: «nunca recalculo celdas de datos ni cambio la base del FCF».
  - La normalización T4 (+0,0095: solo intereses netos con su escudo fiscal y C49) existe solo como contraste aritmético en el anexo.

### 5.2 Motor B: adecuación y estado de sus entradas

**[Hecho]** El motor B:
- usa `f = 0`;
- descuenta a `r_op`;
- resta deuda + arrendamientos + pensiones + minoritarios − caja del último ejercicio (31-dic-2025);
- descuenta con exponentes enteros desde el año base, así que su valor queda referido al 31-dic-2025.

La clasificación completa está en `ENTRADAS_Y_FECHAS.md`, §2. Clases: L localizada, C contrastada, D derivada por convención, H hipótesis pendiente, A ausente.

| Entrada | Libro | Clase | Nota |
|---|---|---|---|
| L22 · L23 · C64 | 213,613 · 49,3 · 262,913 | C | Préstamos del balance (EN25 p.3) y nota 8 |
| L24 · caja | 108,352 | C como saldo · H como caja disponible | El dividendo a cuenta de 43,338, aprobado el 19-dic-2025 y pagado el 13-feb-2026, no está en L22 |
| L25 · pensiones | 6,223 | C como provisión de personal · H como déficit · A el déficit neto | La provisión incluye «otras obligaciones con empleados»; no se tiene la obligación menos los activos del plan |
| L26 · minoritarios | 0 | L · A la confirmación humana | La IA no confirma ceros |
| L15 · C63 | 20,8 · 0,0634 | C · D | i es una aproximación histórica de 2025; no recoge la deuda de 2026 ni si los intereses incluyen los de arrendamientos |
| C37 · C55 · C41 | 87,9 · 35,206 · 3.094,6 | L · C (acciones de 2025) · D con fechas mezcladas · A el cierre oficial y las acciones a la fecha del precio | El precio es intradía, de una fuente secundaria, y probablemente sin derecho tras la liberada 1×20 (BORME, 28-oct-2026) |
| `r_op` | 0,0869 | D (convención 4) | Tasa personalizada, no coste de mercado. E es de 3-nov-2026, D de 31-dic-2025 e i de 2025 |

[Hecho] Con esas celdas y r = 0,09 (sin cambiarla), la fórmula de la convención 4 da `r_op` ≈ 0,0869. Es aritmética, no una valoración. Con D a 30-jun-2026 (heredado) bajaría ≈15 pb.

**[Interpretación] Por qué el motor B es metodológicamente más adecuado para Vidrala hoy:**
1. **No necesita calibrar nada con la ventana.** El perímetro, el calendario fiscal y las provisiones dejan de entrar en el valor por `f`.
2. **El negocio y el puente tienen el mismo perímetro a 31-dic-2025.** V0 son las ventas de 2025 y el puente son los saldos de esa fecha: sin Italia, con Brasil completo y sin Toro en ninguno de los dos lados. Esa coherencia es solo a 31-dic-2025; no se extiende a la fecha del precio.
3. **Los arrendamientos se tratan como deuda contrastada.** Eso elimina la incertidumbre de C49 en la valoración (§4).
4. **Es lo que prevén la convención 10 y el personaje.** Este último dice: «si solo cambia mucho la financiación → motor B», con la cita «Three things ruin people: drugs, liquor, and leverage» (TCI p.68; HIM) aplicada a la deuda que mata. Esta no es deuda que mata (0,36 × EBITDA en 2025): es deuda que cambia.

**[Interpretación] Lo que el motor B no resuelve y lo que añade:**
- **No resuelve el desfase de fechas.**
  - El valor queda referido al 31-dic-2025 y el precio es del 3-nov-2026. Entre medias hay 10 meses de rendimiento, 59,8 mm de dividendos, recompras, la liberada 1×20, Toro, la nueva deuda y Kristin.
  - Sus efectos tienen signos opuestos y no pueden sumarse sin datos (`ENTRADAS_Y_FECHAS.md`, §5).
  - El motor A tiene el mismo desfase, escondido en `f` y en el puente de caja.
- **No resuelve** las acciones a la fecha del precio, el déficit neto de pensiones ni la confirmación de L26.
- **Añade** una tasa personalizada (`r_op`, convención 4) con E y D de fechas distintas y una i histórica que incluye deuda brasileña cara.

**[Propuesta] Salvaguarda contra la elección por resultado.**
- La recomendación del motor se fija **ahora**, por adecuación, **antes** de conocer ningún valor. Esta revisión no ha calculado ninguno.
- En la reejecución, el expediente debe presentar el motor elegido y, como contraste, el otro, con la diferencia explicada.
- Si el resultado del motor B fuera más favorable, eso no puede usarse como argumento, ni en un sentido ni en otro.
- El cambio de motor no oculta ninguna discrepancia: P1, el perímetro, C49, las fechas y las acciones siguen documentados y abiertos en `DECISIONES_PENDIENTES.md`.
- El cambio de motor tampoco se presenta como solución de esas incertidumbres.

---

## 6. Recomendación y alternativas (revisada en la 4.3.1)

La recomendación se separa en tres niveles. Cada uno tiene su propio alcance. **Ninguno pide que se acepten a la vez supuestos que todavía no están bien delimitados.**

### 6.1 Justificación metodológica del motor B (se mantiene)

**[Propuesta] Motor B** (C62 = «No · financiación cambia mucho»). Se mantiene por estas razones:
- `f` no puede representar fugas recurrentes con los datos acreditados de la ventana: perímetro, partidas de devengo con recurrencia no acreditada y tres regímenes de financiación (§3–§5.1).
- La convención 10 y el personaje prevén el motor B cuando la financiación cambia mucho.
- La plantilla no permite normalizar `f` sin escribir datos no publicados.

**Condiciones:**
- aplicar P1 (corrección factual) con cualquier motor;
- fijar la elección antes de ver ningún valor;
- presentar el motor A con T3 como contraste, con la diferencia explicada.

**Límites:**
- el motor B elimina `f` y C49 del valor, pero **no resuelve** las fechas, las acciones, Toro, L25 ni L26;
- añade una tasa personalizada (`r_op`).

La razón es de adecuación del método. **No** es que la evidencia del motor B sea completa.

### 6.2 Suficiencia de datos para una reejecución exploratoria (ruta A)

**[Interpretación] Suficiente, con condiciones declaradas** (`ENTRADAS_Y_FECHAS.md`, §4):
- el valor queda referido al 31-dic-2025;
- E, en `r_op`, y la fecha de análisis son de 3-nov-2026: el ejercicio no es una valoración íntegramente referida al cierre de 2025;
- L26 y C48 siguen como ceros pendientes de confirmación humana;
- L25 es una aproximación;
- en el motor A, T3 depende de δ = 0 y de un circulante derivado.

**Para qué sirve:** comprobar la coherencia del expediente corregido, la respuesta de las palancas de la fase B a la referencia S2C corregida y la diferencia entre motores.

**Para qué no sirve:** comparar con el precio del 3-nov-2026, ni dar un precio de Sí comparable, una zona, un margen o un cubo para decidir.

### 6.3 Suficiencia de evidencia para una valoración comparable con el precio (ruta B)

**[Hecho] Insuficiente.** Faltan:
1. el cierre oficial del 3-nov-2026 y el calendario de la liberada 1×20, que fija si el precio es sin derecho;
2. las acciones en circulación a esa fecha: autocartera de 2026 y acciones tras la liberada;
3. saldos de deuda, arrendamientos, caja, pensiones y otras obligaciones cercanos a la fecha del precio, con la deuda asumida y el pago aplazado de Toro;
4. las cuentas y el precio final de Toro, si la base lo incluye;
5. los dividendos y recompras de 2026;
6. el efecto neto de Kristin;
7. una decisión de método sobre el tiempo: llevar el valor de 2025 a la fecha del precio o rebasar en 2026.

Mientras falten, el signo neto del desfase no se conoce (`ENTRADAS_Y_FECHAS.md`, §5).

### 6.4 Alternativas

| Alternativa | Estado | Motivo |
|---|---|---|
| **Motor A con perímetro de continuadas (T3: `f` = −0,009847, condicionada)** | **Se mantiene como contraste, no como base** | Es la versión más coherente del motor A con los datos disponibles. Depende de δ = 0 (hipótesis) y de un circulante derivado (no publicado). Proyecta como perpetuas partidas de devengo cuya recurrencia no está acreditada. Para usarla habría que llevar al expediente, como estimaciones justificadas, C46 = 322,65, J14 = 85,978 y K14 = 36,487 |
| Motor A con T4 (`f` = +0,0095, normalizada) | Solo como contraste en el anexo | Supone una normalización sin la evidencia de §3.6. No se puede introducir sin escribir datos no publicados y depende del nivel futuro de los intereses |
| T1 (P1 sin perímetro: −0,0276) | Descartada como base de `f` | Proyecta el negocio vendido y la plusvalía |
| T2 (P1 y J14 = 89,866: −0,0301) | Descartada | Añade a la mezcla los ajustes no monetarios de Italia |
| T0 (libro: +0,0199) | Descartada | Error de dato (P1) |
| Restar al capex el flujo de inversión de Italia | Descartada | Las altas de Italia (4,3) son el 15 % de ese flujo (28,4) |
| Perímetro consolidado con Italia en toda la ventana | Descartada | Representa un negocio que la empresa ya no tiene |
| Cambiar la ventana (C57) | No se propone | 2025 y 2024–2025 también dan `f` negativa con T3 (−0,0144 y −0,0086, condicionadas). No hay razón de representatividad que lo justifique |

### 6.5 Fases que habría que volver a ejecutar (con cualquier ruta)

- **A**, para justificar C62 y revisar «qué caja espero» con el perímetro de continuadas y con las fechas declaradas.
- **B**, para volver a decidir el S2C con la referencia corregida (0,92). Con el motor B, además, comprobar g < `r_op` y ROIC a largo plazo > g.
- **C**, para la comprobación conjunta. En la ruta A, sin cubo de decisión.

---

## 7. Qué conclusiones quedan impedidas

1. **Ninguna valoración del motor A del libro puede leerse como sostenida.**
   - Su `f` procede de un error de dato.
   - Con el dato corregido, contiene un negocio vendido.
   - Con T3, contiene partidas de devengo cuya recurrencia no está acreditada, y depende de δ = 0 y de un circulante derivado.
   - [Interpretación] El cubo provisional Vigilar de la fase C se apoyaba en un precio de Sí calculado con esa `f`. En lo financiero debe leerse como **pendiente de investigación**, aunque el juicio cualitativo de la fase A no cambia.
2. **Con el motor A no puede afirmarse** el nivel del FCF base de continuadas (capex de Italia), ni el valor de C49 (§4), ni un intervalo demostrado para `f`.
3. **Con el motor B, en la ruta A:** no puede compararse el valor con el precio del 3-nov-2026 ni presentarse el ejercicio como una valoración íntegramente referida al cierre de 2025, porque E es de 2026. L25 y L26 siguen sin confirmar.
4. **En cualquier motor, mientras falte la evidencia de §6.3:** ningún precio de Sí, zona, margen ni cubo comparable con el precio del 3-nov-2026.
5. **Sea cual sea el motor, el S2C del NORMAL tiene que volver a decidirse**, porque su apoyo factual contenía P1 (§1, punto 7).

---

## 8. Otras entradas materiales no contrastadas (no se dan por verificadas por venir de la herencia)

| Entrada | Problema | Efecto |
|---|---|---|
| Historia 2016–2022 (columnas C–I) | Consolidadas con Italia, no reexpresadas | Media de márgenes de diez años (C49 → m0, porque C8 = «Media del ciclo»), mínimo y máximo (C50 y C51), CAGR (C45 y C46), S2C (C53), ROIC medio (C55) y tipo medio de cinco años (C52 → τ). El margen de Italia en 2023 (17,0 %) se parece al del grupo, así que el efecto en m0 probablemente es pequeño (interpretación) |
| EBIT 2025 | Incluye 13,668 de costes de reestructuración de Reino Unido (EN25 p.28), y «Other income» sube a 47,966 (Reino Unido 33,291) sin explicación examinada | Margen del último año y base de la palanca de margen. Es un cargo «extraordinario» que el procedimiento manda tratar como gasto si se repite (PCA p.119; HIM) |
| Segmento «Italia» dentro de continuadas 2024 | Ventas 17,016, D&A 1,822 y BAI 2,139 (ES24 p.37), sin explicación | Perímetro de las ventas y el EBIT de 2024 (≈1 %) |
| Filas 30 y 31 (reinversión) | Contienen P1, la compra de Vidroporto (J31) y el cobro de Italia (K31) | Referencia S2C y la cuenta de la fase B (§1, punto 7) |
| Pensiones (L25) | Provisión de personal con una definición más amplia | Motor B, pequeño |
| C37, C41, C55 y fechas | Precio intradía de una fuente secundaria. Acciones de 31-dic-2025 frente a precio de 3-nov-2026, probablemente sin derecho tras la liberada 1×20 (BORME). Autocartera de 2026 heredada y no contrastada | Lectura de precio en cualquier motor; peso de E en `r_op`. Detalle en `ENTRADAS_Y_FECHAS.md` |
| Tipo (fila 10) | Redondeado a cuatro decimales | Inmaterial (≈0,001 mm) |

---

## 9. Qué no cambia

- El juicio cualitativo de la fase A no depende de `f`: negocio, círculo con su borde, foso estrecho, gestión con reservas y descalificadores.
- r = 0,09, las probabilidades, los escenarios y las palancas no se han tocado. Las palancas se volverán a decidir en la fase B si la persona responsable lo decide (§6.5).
- **[Hecho]** La cita de la plusvalía en `fase_a.md` («[CF_2025, PDF p.31, 64]») es correcta: EN25 p.31 dice «amounted to a gain of 50 million euros». En el resumen de trabajo anterior constaba como no encontrada; queda resuelto.
- H1–H3 sigue cerrado. El recuento 3.215/3.211 sigue fuera del encargo.
