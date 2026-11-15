# N3 · Inversión fija, circulante y mantenimiento · subsanación de la entrega 4.7.1

Redactado por Claude (Opus) el 10-nov-2026 como respuesta a la revisión independiente de la 4.7, §2. Es una declaración de Claude; nada está comprobado externamente por ChatGPT. Se distinguen **hechos publicados**, **cálculos derivados**, **hipótesis** y **decisiones humanas**.

**Qué sustituye.** Del informe de la 4.7 (`…/2026-11_Vidrala_ensayo_4_7/INFORME_FINANCIERO_N1_N3.md`), este documento sustituye la viñeta «Necesidades de caja» del §4.2 («Realizabilidad») y, en el §6, la mención a «la cobertura de los compromisos», una columna que la matriz ya no lleva. El resto del §4.2 sigue vigente, en particular:
- el circulante comercial, el 14,70 % de las ventas de 2025 (14,88 % en 2024);
- el activo fijo y la coherencia de la recuperación (que el §4 de este documento completa);
- el registro de la revisión de la regla;
- la advertencia de que el terminal reinvierte g ÷ ROIC desde el año 11 aunque en el MALO las ventas del año 10 sigan por debajo del máximo.

Ese informe se conserva intacto como antecedente; N1, N2, la matriz y los libros de propuesta no cambian. (Corregido tras la auditoría interna de Claude, N-c: la primera redacción decía «el §4.2 y la fila de “cálculos de caja” del §4.3», y esa fila no existe.)

**Aviso de alcance.** Las cifras son resultados mecánicos de un ensayo, sobre copias identificadas. No son una comparación válida con el precio de 87,9 del 3-nov-2026 ni una recomendación de compra o espera. Las sensibilidades de este documento son exploratorias: no son alternativas de la matriz ni cotas.

**Constantes.** r = 0,09; probabilidades 0,2 / 0,6 / 0,2; k = 3; caja 108,352 (sin volver a restar el dividendo de 43,338); puente 160,784. Nada de eso cambia.

## 1. Qué estaba mal y qué cambia

**El error (hecho, señalado por la revisión independiente).** La 4.7 calculaba la inversión bruta implícita como D&A + reinversión total. Con la descomposición que usa el propio análisis, la relación correcta es otra:

- reinversión total = inversión fija neta + variación del circulante;
- inversión bruta = D&A + inversión fija neta = D&A + reinversión total − variación del circulante.

En R1, año 1, toda la reinversión es circulante (−2,15434). La inversión bruta implícita es, por tanto, **132,948**, no 130,79366. En R0 es 118,82278, no 116,7.

**Qué no cambia (cálculo, con control en el script).**
- Los flujos de caja, los valores, la matriz de 27 combinaciones y la combinación recomendada son los de la 4.7. `analisis_n1_n3.py` lo comprueba frente a `…_4_7/financiero/matriz.csv`.
- La corrección es contable y revela qué supone la réplica. No cambia lo que calcula.

**Qué cambia en el modelo auxiliar (`scripts/analisis_n1_n3.py`).**
- Cada regla separa ahora la reinversión en variación del circulante e inversión fija neta.
- La inversión bruta implícita es D&A de 2025 (constante) + inversión fija neta.
- La hipótesis de mantenimiento se hace explícita (§3).
- Se añaden sensibilidades de mantenimiento y de capacidad (§4–§5), con su salida en `financiero/sensibilidades_n3.csv`.
- `financiero/matriz.csv` y `n3_anio_a_anio.csv` llevan las columnas nuevas. Se retira la columna «FCF1 MALO / compromisos», porque esa comparación no tenía sentido.

## 2. Descomposición por regla (cálculo derivado; MALO, año 1)

| Regla | Reinversión total | Variación del circulante | Inversión fija neta | Inversión bruta implícita | FCF |
|---|---|---|---|---|---|
| R0 (plantilla), T0·M0 | −16,27956 | −2,15434 | −14,12522 (desinversión) | 118,82278 | 207,494 |
| R1, T0·M0 | −2,15434 | −2,15434 | 0 | 132,94800 | 193,369 |
| R2, T0·M0 | 0 | 0 | 0 | 132,94800 | 191,215 |
| **R1, T1·M1 (recomendada)** | **−2,15434** | **−2,15434** | **0** | **132,94800** | **203,825** |

La serie completa de los diez años y de las cuatro reglas está en `financiero/n3_anio_a_anio.csv`.

**Qué supone R1 (interpretación).** Mientras las ventas caen y se recuperan por debajo del máximo, la inversión fija neta es cero. Si la reposición se aproxima por la amortización, la inversión bruta es exactamente la amortización. Por encima del máximo vuelve ΔV ÷ S2C, repartido entre circulante y fijo.

## 3. La hipótesis de mantenimiento: evidencia y límites

**Hipótesis (explícita desde la 4.7.1).** La plantilla y la réplica suponen que la inversión de reposición, la necesaria para conservar la capacidad, es igual a la amortización. Lo suponen en los tres escenarios, no solo en el MALO: el NOPAT ya descuenta la amortización y el flujo de caja solo resta la reinversión neta (ΔV ÷ S2C).

**Hechos publicados** (textos conservados del expediente de referencia):

| Año | Ventas | Inversión (inmovilizado material + inmaterial) | Amortización | Inversión ÷ amortización | Fuente |
|---|---|---|---|---|---|
| 2020 | −2,2 % | 134,248 | 84,144 | 1,60 | CF_2020, PDF p. 13, estado de flujos |
| 2024 | +11,3 % | 168,800 | 117,720 | 1,43 | CF_2025, p. 7, comparativo |
| 2025 | −7,8 % | 188,503 | 132,948 | 1,42 | CF_2025, p. 7 |

- **Historia del libro de referencia** (filas 12 y 8, 2016–2025): inversión ÷ amortización = 0,73 · 1,16 · 1,15 · 1,10 · 1,60 · 1,27 · 1,41 · 1,74 · 1,43 · 1,42. Desde 2017 la inversión supera a la amortización todos los años, también en los dos años con ventas en caída (2020 y 2025).
- **Destino de la inversión:** «The main additions in 2025 and the prior year correspond to the investments made primarily in the renewal of furnaces» en España, Portugal y el Reino Unido (CF_2025, PDF p. 44). El texto dice *sobre todo* (primarily): no excluye ampliación, eficiencia ni descarbonización.
- **Vida útil** contable de «furnaces, installations, and production machinery»: 8–16 años (CF_2025, p. 14). Es una vida útil contable, no la duración de una campaña de horno; los textos conservados no dan esa duración ni un calendario de reconstrucciones.
- **Descarbonización:** subvenciones PERTE de 10,298 y 6,316 mm para inversiones en la descarbonización de hornos «from 2026 onwards» (CF_2025, p. 65). Hay además un plan de autogeneración renovable (p. 37).
- **Compromisos** de compra de instalaciones y maquinaria: 66,610 mm al cierre de 2025, frente a 9,622 en 2024 (p. 45).
- **Gasto de reparación y mantenimiento** de 2025: 41,854 mm (p. 74). Es gasto corriente, ya incluido en el EBIT; no es inversión.

**Interpretación.**
- Que la inversión supere a la amortización incluso con ventas en caída, y que se destine sobre todo a renovar hornos, indica que la amortización puede **quedarse corta** como medida de la reposición. Que buena parte sea renovación es una interpretación del «primarily» de la p. 44, no un dato.
- La amortización es de coste histórico. Renovar a precios actuales, y descarbonizar, cuesta más.
- Pero los textos conservados **no separan** reposición, eficiencia, descarbonización y crecimiento dentro de la inversión. Una parte del exceso puede ser voluntaria o de crecimiento. 2025 incluye además daños por el apagón de abril (p. 72), cuyo coste no se cuantifica en inversión.
- **Límites en el otro sentido** (añadidos tras la auditoría interna, N-b). La amortización también contiene partidas que no son reposición de capacidad:
  - en 2025, 7,913 mm de amortización de intangibles, de los que 4,492 son de la cartera de clientes adquirida (CF_2025, p. 46);
  - en 2024, 4,768 de amortización de derechos de uso (nota del lector en la Historia, fila 8).

  Además, la amortización salta de 87,21 (2023) a 117,72 (2024) y 132,948 (2025) con los cambios de perímetro (Brasil desde noviembre de 2023; Italia fuera desde 2024), así que la ratio de un año mezcla perímetros. La fila de 2020 de la tabla es la publicada entonces, con Italia; las de 2024 y 2025 son de continuadas. Nada de esto cambia cifras, ni permite fijar una cifra de reposición.
- **Límite:** el exceso de 2025 (55,555 mm, +41,8 % de la amortización) **no prueba** que deba repetirse ni es una cota. Tampoco lo es el de 2020 (+59,5 %). Comparar la inversión implícita del año 1 con los compromisos de 66,6 mm solo dice que estos caben en ella; no valida las necesidades futuras de caja.

## 4. La recuperación de capacidad

**Hipótesis de R1.** La capacidad que no se desinvierte queda disponible para la recuperación. Eso exige que, durante la caída, se siga invirtiendo al menos en reposición. Si un horno llega al final de su vida útil y no se reconstruye, la capacidad se pierde, y recuperarla exigiría inversión fija nueva. (La vida útil contable es de 8–16 años; la duración real de las campañas no está en los textos conservados.)

**Sensibilidad** (cálculo, regla `circulante_sin_capacidad`, que coincide con la formulación inicial del R1 conservada en la 4.7; el script lo comprueba): la recuperación paga ΔV ÷ S2C completo.
- En T1·M1, el ponderado pasa de 69,24 a 69,18 (−0,06) y el precio de Sí de 64,26 a 64,13 (−0,13).
- El efecto es pequeño porque en el MALO las ventas solo se recuperan un 1,8 % desde el mínimo en los años 8–10.

## 5. Sensibilidades exploratorias de mantenimiento (T1·M1·R1)

**Cómo se calculan.** El mantenimiento adicional, x × amortización de 2025, se resta del flujo de caja de cada año y del terminal, donde crece a g. No se le asigna efecto fiscal, lo que es conservador.

**Niveles.** x = 20,9 % y 41,8 %, la mitad y el total del exceso de 2025. No son cotas ni previsiones. Las diferencias (Δ) se calculan frente a la propuesta con los valores sin redondear.

| Mantenimiento | Alcance | V MALO / NORMAL / BUENO | Ponderado (Δ) | Precio de Sí (Δ) | FCF1 MALO | FCF mín. MALO | Inversión bruta año 1 MALO |
|---|---|---|---|---|---|---|---|
| = amortización (R1, la propuesta) | — | 51,81 / 69,78 / 85,08 | 69,24 | 64,26 | 203,8 | 161,5 | 132,9 |
| +20,9 % | solo MALO | 42,16 / 69,78 / 85,08 | 67,32 (−1,93) | 60,13 (−4,13) | 176,0 | 133,7 | 160,7 |
| +41,8 % | solo MALO | 32,51 / 69,78 / 85,08 | 65,39 (−3,86) | 55,99 (−8,27) | 148,3 | 106,0 | 188,5 |
| +20,9 % | todos los escenarios | 42,16 / 59,41 / 74,25 | 58,93 (−10,32) | 54,14 (−10,13) | 176,0 | 133,7 | 160,7 |
| +41,8 % | todos los escenarios | 32,51 / 49,03 / 63,43 | 48,61 (−20,64) | 44,01 (−20,25) | 148,3 | 106,0 | 188,5 |

Las variantes «sin capacidad» y las mismas sensibilidades sobre la base T0·M0 están en `financiero/salida.txt` y `sensibilidades_n3.csv`.

**Lectura** (interpretación):
1. **Solo MALO.** Responde a la pregunta del N3: si en el escenario adverso la reposición supera a la amortización, el MALO baja mucho. Como el MALO marca la escalera (k = 3), el precio de Sí cae más que el ponderado.
2. **Todos los escenarios.** Es una hipótesis de la plantilla entera, no del N3. Su efecto es de un orden mayor que cualquiera de N1–N3. No se adopta: se registra como **pendiente nuevo** (§7).

## 6. Recomendación revisada sobre D-N3 (propuesta; la decisión es de la persona responsable)

- **La regla de liberación R1 se mantiene propuesta:** solo se libera el circulante y la capacidad se conserva. Responde a la composición del balance y a lo observado en 2025.
- **Condición explícita:** R1 lleva implícita una reposición igual a la amortización. Adoptar R1 no es adoptar esa hipótesis.
- La evidencia apunta a que la reposición podría ser mayor, pero **no permite fijar cuánto**, y también hay partidas de la amortización que no son reposición (§3). Por eso Claude no propone ninguna cifra de mantenimiento.
- **Advertencia explícita:** de las tres opciones de D-N3b, «=D&A» es la de **mayor valor**. Claude la propone de forma provisional porque no hay cuantificación para otra, no porque la evidencia la respalde. Por eso la sensibilidad del MALO tiene que acompañar siempre a cualquier resultado con R1. Propone mostrar siempre, junto a cualquier resultado con R1, la sensibilidad de mantenimiento del MALO, y obtener la separación entre reposición y crecimiento de la inversión, que no está en los textos conservados.
- El archivo de decisiones actualizado está en `financiero/decisiones_propuestas_N1_N3.json`. D-N1 y D-N2 son las de la 4.7; D-N3 queda reescrita y hay una pregunta nueva, D-N3b, sobre la hipótesis de mantenimiento. Las cuatro están sin rellenar (`decision`, `fecha` y `confirmado_por` vacíos).

## 7. Pendientes que añade la 4.7.1

- **P-M1 · hipótesis de mantenimiento de la plantilla** (reposición = amortización en todos los escenarios). Tiene un efecto potencial de hasta unos −20 puntos de ponderado con el exceso de 2025. Necesita datos de reposición frente a crecimiento y de reconstrucciones de hornos programadas (presentaciones a inversores o informe de gestión), que no están en los textos conservados.
- **Validación del calendario de campañas de hornos** frente a la vida útil declarada, para la sensibilidad de capacidad.
- **Pendientes que siguen abiertos:** N4, N9, N10, P-N1 y P-N2, igual que en la 4.7.
