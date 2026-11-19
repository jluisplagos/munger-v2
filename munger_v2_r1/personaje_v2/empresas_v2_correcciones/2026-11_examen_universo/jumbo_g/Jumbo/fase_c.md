# Fase C · turno 1 · Jumbo S.A. (BELA) · motor A · 2026-11-19

## 1. Una sola historia

Lo que la hoja calcula con mis 52 celdas: MALO 26,12 €, NORMAL 37,02 €, BUENO 44,52 €, ponderado 36,34 € (C83). Peso del «para siempre» 45 % / 51 % / 55 %: ninguno pasa del 75 %. Semáforos: el margen en «⚠ REVISAR» en los tres escenarios porque supera el Q3 del sector (8,6 %), no su máximo propio (33,4 %), y G5 ya está justificada; r = 9,0 % por debajo de la r mínima (10,2 %); el resto pasa. El estado técnico es INCOMPLETO solo por las predicciones, que son del turno 2.

El DCF inverso dice que el precio de 27,28 € descuenta ventas que caen un 1,7 % al año en los años 1–5 con mis demás palancas del NORMAL; el precio de Sí descuenta +3,15 %, menos que mi NORMAL (+5,5 %). El valor sin crecimiento (28,17 €) ya supera el precio: el precio no paga nada por crecer. El mercado ve una empresa que encoge. «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM): o se equivoca el mercado con las plataformas, o me equivoco yo con la duración del margen.

El tornado es información: la tasa de descuento es la palanca de mayor efecto (±1 punto: 6,01 €, el 16 % del NORMAL), después el ROIC a largo plazo (4,51 €) y el crecimiento (3,44 €). El valor depende sobre todo de la rentabilidad exigida, y esa r (9 %) es heredada, provisional según `alcance_v2.json` y menor que la r mínima. Una caída igual del 18,4 % en los tres valores llevaría el precio de Sí al precio actual. No la cambio (S-3), pero lo digo.

La hoja dice «DESCARTADA POR FILTRO PABRAI» (A6). Ese filtro lee C13; mi cubo lo decide el orden de mando.

Incoherencias que encontré, y cómo quedan:

- **C13.** La fase A dijo que, sin crecimiento, el FCF sobre la capitalización sin caja (≈ 7,5 %) queda bajo r. Ese FCF ya paga la reinversión con la que la empresa creció un 7,2 %. La hoja da 28,17 € sin crecimiento, un 3 % sobre el precio. Un 3 % no es un margen claro: «if there is a big whirlpool you don't want to miss it with 20 feet» (AIWTK p.53; HIM). C13 sigue en No; cambio el argumento, no la celda.
- **Duración de la ventaja.** La fase A habla de «una ventaja de años, no de décadas». El motor, en cambio, mantiene para siempre el margen del año 10 sobre las tiendas ya abiertas; el ROIC a largo plazo solo afecta al capital nuevo. Lo que se pierde en el año 11 es el exceso de rentabilidad del capital nuevo, no el margen de la base. La tesis tendrá que decirlo así. Un margen por debajo del nivel de 2016–2020 no está en ningún escenario: va a la tesis inversa.
- **Aviso P-FOSO.** El S2C del MALO (1,1) se parece a C54 (1,115), pero no está anclado en él: sale de la medida marginal propia de 2021–2025 (401 mm de ventas nuevas con 356,9 mm de reinversión neta, Historia!H6, L6, I31:L31). No hay error de perímetro.
- **S2C del NORMAL.** La fase B quita los ~75 mm de tiendas que ya alquilaba y además Patras. Pero VESO MARE es uno de los tres inmuebles de 2025 (~25 mm [FY2025, PDF p. 21]) y entra en los 75 mm: quitarlo dos veces daría 1,48. Quitando solo los 75 mm sale 1,42, o algo menos si parte cayó en 2021. Redondeado, 1,4: la celda no cambia, ni el cubo, ni la zona. Como pide F1-B, señalo que Herald Hellas 2 sustituyó un alquiler de una tienda que ya funcionaba: contarla como crecimiento baja un poco C53.
- **Grecia.** Las fases A y B la llaman madura. Con 53 hipermercados a fin de 2023 y a mitad de 2026 [FY2023, PDF p. 10; H1 2026, PDF p. 7], sus ventas crecieron +6,10 %, +8,63 % y +7,08 % en 2024, 2025 y H1 2026 [FY2024, PDF p. 13; FY2025, PDF p. 14; H1 2026, PDF p. 6]. Sin las ventas a socios, un 6,4 % en 2025 (segmento [FY2025, PDF p. 175 y p. 176]). Madura en tiendas no es madura en ventas. Las comparables del NORMAL (+2,5–3 %) son prudentes. Es juicio, en sentido conservador: no lo pido corregir.
- **Inventario.** Creció un 19,0 % en 2025 frente a ventas +7,2 % (días de inventario 203 frente a 187; nota de C31), y el circulante absorbió 50,6 y 61,2 mm en 2024–2025. Si es compra anticipada [FY2025, PDF p. 22], no pasa nada; si no rota, el MALO llega por rebajas. Va a la tesis inversa y a una predicción.
- **Textos de la etapa 1.** B101, B102 y C104 siguen en el libro con un precio de Sí de ≈ 19 € y un tamaño de posición en C104, que D16 no admite. Se reescriben en el turno 2, sin los hechos de la etapa 1 que no tienen fuente en este expediente.

Ninguna obliga a mover palancas: `revisar_palancas = false`.

## 2. Desviaciones pendientes

Solo queda G8 (salto del año 11): 0,145 / 0,262 / 0,326. G16 y G17 no aparecen (peso del terminal ≤ 55 %; cuota sin C24). Las justifico una por escenario:

- **MALO (convención).** El ROIC terminal es la tasa del motor. En los años 1–10 el capital nuevo rinde 1,1 × 0,26 × 0,82 ≈ 0,235 porque las tiendas nuevas usan la compra directa y la logística que ya existen. Desde el año 11 las plataformas y el dólar se han quedado la ventaja: el capital nuevo rinde lo que cuesta, cerca del neutro (8,83 %). Las tiendas abiertas conservan el 26 %.
- **NORMAL (fundamentada).** 1,4 × 0,315 × 0,82 ≈ 0,362 en los años 1–10, con aperturas fuera de Grecia y socios que ponen su capital [H1 2026, PDF p. 19]. Desde el año 11 se acaba el sitio: Grecia (58 % de las ventas [FY2025, PDF p. 17]) no abre en 2027 [H1 2026, PDF p. 17] y Rumanía habrá agotado, aun cumpliendo la guía, su objetivo de duplicarse [FY2025, PDF p. 26]. Lo que queda va a pop-ups, tienda en línea y socios lejanos, sin ventaja demostrada: un punto sobre r.
- **BUENO (fundamentada).** 1,7 × 0,32 × 0,82 ≈ 0,446, con más peso de los socios. Desde el año 11, 3 puntos sobre el coste, el máximo del criterio a perpetuidad (MR; E2), porque la vara P-FOSO está sin comprobar.

«The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).

## 3. Palancas

No pido moverlas. Revisé las que podían estar mal derivadas: la aritmética del S2C (1,12 sin ajustes; 1,42 sin las tiendas compradas, redondeo 1,4), el perímetro del MALO (no anclado en C54), C76 (546,14 − 94,06 − 134,37 − 5,7 − 95 − 66,4 = 150,6) y los 95 mm de centros. Estos no están en el S2C de 2022–2025, así que no se cuentan dos veces. Aunque lo estuvieran, valdrían 0,71 € por acción en los tres escenarios: +2,1 % sobre el precio de Sí, sin cambio de zona. En `celdas_corregidas` dejo C13, C18, B16, C16 y C76 con `despues = antes` y el motivo.

## 4. Autocomprobación

Lo detallado está en el JSON; aquí lo que pesa.

- **Anclaje en la etapa 1.** Las g y las probabilidades siguen iguales que en la etapa 1, con hechos propios: no las muevo. Lo que queda de la etapa 1 son los textos de B101, B102 y C104: se reescriben.
- **Anclaje en el precio o la fuente externa.** El precio de Sí (33,42 €) cae cerca de Simply Wall St (33,04 €). Ninguna Observación usa C38. Lo tomo como casualidad, no como ancla.
- **Consistencia.** El cubo provisional pasa de Vigilar a Sí. La fase A lo dejó condicionado a la escalera, y las palancas van por debajo de sus referencias, no por encima.
- **Historia bonita.** El salto de margen de 2021 llega tras la pandemia y con dos años de inflación; el extracto no da la causa: «carefully examine each past success, looking for accidental, non causative factors» (PCA pp.548–549; HIM). Es la hipótesis que más condiciona.
- **BUENO.** No necesita un margen ni un ROIC que no hayan existido. Leyendo la fórmula del Anexo C con los valores de `precio.json`, aunque valiera lo mismo que el NORMAL, P* quedaría en ≈ 32,35 €.
- **Doble castigo.** No lo encuentro (PA; E6).
- **Disponibilidad.** Lo vívido (Rumanía −6,50 %, plataformas, flete) empujó a la prudencia; la fila menos vívida es Grecia creciendo con las mismas tiendas.
- **Autoridad.** La superficie de la guía cuadra con lo ocurrido (+1,9 % al año). La guía de centros entra como coste.
- **¿El MALO es malo?** Vale 26,12 €, un 4,2 % bajo el precio (diferencia ÷ precio). Es malo dentro de la historia de la empresa, pero las plataformas no existían en 2016–2020 y el margen puede bajar más. Leyendo la misma fórmula, el precio seguiría bajo P* mientras el MALO valiera más de ≈ 11,8 €. La conclusión depende del NORMAL, no de lo hondo del MALO. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** El peso del presidente y accionista principal (el bono caía si él o su familia dejaban el control [FY2022, PDF p. 57]), sin plan de sucesión ni remuneración en el expediente; el 70 % del producto viene de Asia [FY2025, PDF p. 24], y un corte del suministro sería un salto, no un MALO de margen; y el inventario.

Estas comprobaciones de sensibilidad no recalculan ni sustituyen la escalera del script; la escalera sigue siendo la de `precio.json`.

## 5. Cubo y conclusión provisionales

Sigo el orden de mando:

- **Bloqueo:** ninguno (gramática con 0 errores; B252 y B254 falsos).
- **Límite del modelo:** ninguno (motor A, FCF base positivo, financiación estable).
- **Descalificadores:** ninguno. El cambio de canal es la frontera, pero lo puedo juzgar con hechos: Grecia vende más con las mismas tiendas y el margen EBIT de 2025 fue 31,8 %.
- **Datos ausentes:** ninguno material (punto 6).
- **Fundamento material:** lista vacía (punto 7).
- **Zona:** `cumple_regla_k`. El precio está un 18,4 % por debajo del precio de Sí (diferencia ÷ precio de Sí), y el precio de Sí un 22,5 % por encima del precio (diferencia ÷ precio).

**Cubo provisional Sí; conclusión provisional `comprar`.** Dos condiciones lo hacen frágil. Primera, la r: es heredada, provisional y menor que la r mínima, y es la palanca de mayor efecto. Segunda, la duración del margen de 2021–2025. La escalera es una convención (D11) y no mide riesgo.

## 6. Datos ausentes (S-19)

Revisé los 25 datos de `datos_ausentes.json`, uno a uno, y ninguno es material: `alguno_material = false`.

- **SBC de C50 y Historia fila 18.** El estado de flujos no tiene ajuste por pagos en acciones, el BPA básico es igual al diluido y las acciones no se diluyeron. Para mover el precio de Sí un 5 % haría falta una SBC de unos 13 mm al año, que habría dejado rastro en esas tres cifras.
- **Ceros de 2016–2018 (intereses, principal y pasivo por arrendamientos).** Son anteriores a la NIIF 16 y no entran en ninguna palanca.
- **Adquisiciones.** Solo 2021 entra en C53.
- **Minoritarios.** Solo restan en el motor B.
- **Datos que el extracto no encontró.** Mercado, cuota, competidores, comparables, elasticidad, capex por destino, inversión por tienda, Balfin y centros afinarían una palanca o la tesis inversa, pero ninguno puede llevar el precio por encima del precio de Sí. Para dos tengo sustituto parcial. La cuota y las comparables se aproximan con Grecia: misma red y ventas al alza. El tamaño del BUENO casi no pesa: aunque el BUENO valiera lo mismo que el NORMAL, P* quedaría en ≈ 32,35 €.
- **Resto.** Rating, ratios de capital, cartera de pedidos y guía no afectan a ninguna celda de juicio. El cruce de etiquetas no cambia la suma que usa el FCF base.

## 7. Fundamento material (D10)

Recorrí las hipótesis materiales: B14:D16, B18:D18, B68:D68, B69:D69, C22, C23, C76, C44, C62, C8, C6 y las narrativas B65:D66.

- **Palancas, g, C76 y C6:** todas con clase fundamentada y hechos de la Historia o del extracto.
- **Probabilidades:** convención argumentada con hechos (banda de margen de diez años, un solo año de caída, socios que se retrasan).
- **Quiebra, C8 y C44:** convención con hechos.
- **Narrativas:** con mecanismo, dueño de la mejora y «qué lo pararía» propios de Jumbo.
- **C97 técnico:** no es hipótesis material de §B.6.

La lista `hipotesis_sin_fundamento` está vacía y D10 no limita la conclusión. `resultado = sin_limitacion`; la comprobación conjunta no procede (`procede = false`, `sobrevive = null`).

## 8. Lo que más condiciona y qué lo resolvería

**La hipótesis fundamentada de la que más depende la conclusión es `Palancas!C15` (con D15 y C18).** Supone que el margen EBIT de 2021–2025 (31,7–33,4 %) dura frente a las plataformas, aunque nadie ha explicado por qué subió desde el 24,8–26,9 % de 2016–2020.

**Lo resolverían tres cosas:**

1. La cuenta de resultados por naturaleza y el margen bruto de los informes de 2016 a 2021, para separar compra, precio y apalancamiento operativo.
2. Preguntar a Relación con Inversores qué parte del salto atribuyen a la compra directa y qué parte al precio.
3. El margen bruto y el margen EBIT de 2026 completo, el primer año con el derecho de aduana de 3 € [H1 2026, PDF p. 14].
