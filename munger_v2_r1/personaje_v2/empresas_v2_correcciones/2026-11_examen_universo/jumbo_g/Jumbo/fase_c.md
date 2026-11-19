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

# Turno 2 · Conclusión

## 9. Comprobación conjunta

No existe `comprobacion_conjunta.json` porque no procedía: la lista de hipótesis sin fundamento está vacía. `sobrevive = null`. Con la conclusión final `esperar`, `resultado = no_procede` (antes de la respuesta al contradictor era `sin_limitacion`, con `comprar`). No hay rango del precio de Sí bajo una combinación adversa. El único peldaño es el de `precio.json`.

## 10. Estado, cubo y acción

**`concluido` (provisional hasta la auditoría) · cubo Vigilar · `esperar`, con condición de negocio y sin precio objetivo.**

El turno 2 cerró en Sí · `comprar`. Tras la respuesta al contradictor (sección 17), la conclusión baja un escalón. La condición es esperar al informe anual de 2026: pasaría a comprar si el margen EBIT del grupo de 2026 es de al menos el 31,0 % y el margen bruto anual de al menos el 54,0 %. El precio objetivo es nulo porque la zona ya cumple la regla k.

El orden de mando del turno 1 sigue igual:

- sin bloqueo;
- sin límite del modelo;
- sin descalificadores;
- sin datos ausentes materiales;
- lista vacía de hipótesis sin fundamento;
- zona `cumple_regla_k`.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 33.42 · zona cumple_regla_k · precio de Sí ≤ 33.42 · precio esc. MALO 26.12 · ponderado 36.34 · fundamento no procede (conclusión no favorable)».

Lo que no es la conclusión, y José Luis debe pesar:

- **La regla k = 3 es una convención experimental (D11).** Con la regla antigua de la hoja (C156 = 26,12 €), el precio de 27,28 € quedaría por encima del precio de Sí.
- **La r del 9 % no es mía.** Es heredada, provisional según `alcance_v2.json` y menor que la r mínima (10,19 %), y es la palanca de mayor efecto del tornado.
- **No hay colchón.** El precio está solo un 4,4 % por encima del precio esc. MALO (diferencia ÷ precio esc. MALO), y el MALO no es un suelo.

De los dos errores, con Jumbo estoy más cerca de regatear: «We left a lot of money on the table through early fretting» (TCI p.79; HIM). Pero el otro está a la vista si me creo sin causa el margen de 2021–2025: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

C93 = Sí. Con g 0,02 y ROIC terminal 0,10, el terminal reinvierte un 20 % del beneficio operativo y pesa un 51 %.

C103 = No. Es un foso de escala en un canal que cambia.

## 11. Tesis (B101)

Jumbo es una tienda de precio bajo y surtido enorme: 89 hipermercados propios y 46 tiendas de socios. Compra directo en Asia a más de 200 proveedores y ha ganado un margen EBIT del 24,8–33,4 % durante diez años, frente a un Q3 del sector del 8,6 %.

No tiene deuda, reparte casi toda la caja y en Grecia vende más con las mismas 53 tiendas.

A 27,28 € el precio no paga nada por crecer (valor sin crecimiento 28,17 €) y descuenta ventas que caen un 1,7 % al año. Mi NORMAL vale 37,02 € y el MALO, con el margen de 2016–2020, 26,12 €.

El precio está por debajo del precio de Sí (33,42 €, k = 3). Pero el NORMAL y el BUENO cobran para siempre un margen que nació en 2021 sin causa explicada y que ya cede, y el tipo impositivo del motor es anterior a la subida de Chipre. Espero al margen de 2026 completo antes de comprar.

La conclusión depende además de una r heredada, provisional y por debajo de la r mínima.

## 12. Tesis inversa (B102)

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

- **El margen saltó sin causa explicada, y ya cede.** Pasó del 24,8–26,9 % al 31,7–33,4 % sin que ningún informe del expediente diga por qué. El margen bruto bajó del 55,61 % al 54,72 % [FY2025, PDF p. 15] y luego al 53,53 % en H1 2026 [H1 2026, PDF p. 7].
- **Las plataformas atacan la ventaja de compra.** Venden desde China lo mismo, barato y voluminoso [FY2025, PDF p. 23]. Si el cliente compra directo, la escala de compra deja de ser una ventaja, y el margen puede bajar por debajo de cualquier escenario.
- **El crecimiento se frena.** El beneficio de 2025 fue plano (Historia!K9:L9), Rumanía cayó un 6,50 % [H1 2026, PDF p. 6] y Grecia no tendrá tienda nueva en 2027 [H1 2026, PDF p. 17].
- **El inventario crece más que las ventas.** Subió un 19,0 % frente a ventas +7,2 % (C31). En un minorista eso anticipa rebajas.
- **Hay dependencia del presidente.** El bono caía si él o su familia dejaban el control [FY2022, PDF p. 57], y no hay plan de sucesión en el expediente.
- **El precio pasa la regla con poco margen.** Solo la pasa con r = 9 % y con k = 3. El mercado descuenta −1,7 % al año (C86) y puede estar viendo lo que yo no veo.

Quité de la tesis inversa de la etapa 1 tres hechos que no tienen fuente en este expediente: la edad del presidente, el voto de la remuneración y las ventas de su sociedad.

## 13. Predicciones (Palancas!A38:C40)

Las tres se comprueban con el informe anual de 2027 (fecha 2028-04-30). La probabilidad es la de que cada predicción se cumpla dado el NORMAL.

| Predicción | Probabilidad | Por qué |
|---|---|---|
| Margen EBIT del grupo de 2027 ≥ 30,0 % | 0,75 | Pone a prueba la hipótesis de B222. El NORMAL da ≈ 31,7 % en 2027. |
| Ventas netas del grupo de 2027 ≥ 1.350 mm | 0,65 | El NORMAL da ≈ 1.372 mm. |
| El inventario de 2027 crece menos que las ventas de 2027 | 0,6 | Pone a prueba la señal de la tesis inversa. |

## 14. B222 y B223

**B222.** La hipótesis fundamentada de la que más depende la conclusión es que el margen de 2021–2025 dure frente a las plataformas (C15:D15, C18). El NORMAL y el BUENO lo cobran para siempre en el terminal. El salto está en el margen bruto: del 51,78 % de 2020 al 55,66 % de 2021 [FY2021, PDF p. 11].

**B223.** Los informes de 2016–2021 del expediente muestran el salto pero no su causa (O2 del contradictor), así que ya no lo resolverían. Lo resolverían dos cosas:

1. La pregunta a Relación con Inversores sobre la causa del salto del margen bruto de 2021.
2. El margen bruto y el margen EBIT de 2026 completo, el primer año con el derecho de aduana.

## 15. Qué me haría cambiar de cubo

- **A Sí:** que el informe anual de 2026 dé un margen EBIT de al menos el 31,0 % y un margen bruto de al menos el 54,0 %, con el precio aún por debajo de 33,42 €.
- **A No:** un margen EBIT por debajo del 28 % dos años seguidos, ventas griegas que caigan con la misma red, o deuda para centros o inmuebles.
- **A Demasiado difícil:** no poder explicar con los informes una caída en Grecia, una caja que pase a depender de socios, Balfin o inmuebles, o una compra grande no relacionada.

## 16. Comparación con la etapa 1

La etapa 1 decía Vigilar con un precio de Sí ≈ 19 € (estimado) a 24,72 €. Ahora también digo Vigilar, pero por otra razón. El precio, 27,28 €, ya está por debajo del precio de Sí, 33,42 €, y espero una condición de margen, no un precio. El negocio que veo es el mismo. Cambian tres cosas:

1. **La regla.** Con la convención k = 3 el precio pasa la regla de precio. Con la regla antigua de hoy (26,12 €) no la pasaría.
2. **El MALO.** Antes era un FCF que caía un 2 % al año, estimado en ≈ 19 €. Ahora es un margen que vuelve al 26 % y vale 26,12 €. Es más suave, y lo digo.
3. **El precio y la caja.** El precio sube a 27,28 € ya sin los repartos de 1,70 € por acción, y C76 pasa de 200 a 150.

La etapa 1 no se equivocó en el negocio. Lo que la separa de esta conclusión es una convención, un MALO menos duro y una condición de margen, y José Luis tiene que juzgar las tres cosas.

## 17. Respuesta al contradictor

Leí `OBJECIONES.json` y comprobé en `texto/` los hechos que cita:

- Chipre al 15 % desde el 1-ene-2026 [H1 2026, PDF p. 40].
- La frase sobre la presión de largo plazo de las plataformas [H1 2026, PDF p. 14].
- El margen bruto del 51,78 % en 2020 y del 55,66 % en 2021 [FY2021, PDF p. 11; FY2020, PDF p. 12].

| Objeción | Respuesta | Efecto |
|---|---|---|
| **O1 · tipo impositivo** (baja). El motor usa el tipo medio de 2021–2025 (Historia!C52 = 17,99 %). En 2025 el tipo fue del 18,93 % y en H1 2026 del 19,97 %, y Chipre sube al 15 % [H1 2026, PDF p. 40]. | **No rebatida.** El hecho es cierto y el sesgo va en su dirección. C52 es una celda de datos que no puedo cambiar, y no tengo ningún dato que lo contradiga. | A la baja. Según su réplica del motor, el precio de Sí pasa de 33,42 a 32,98 € (−0,44 €). Sola no cambia la zona. Cuenta para el escalón de bajada. |
| **O2 · margen para siempre** (baja). El terminal cobra sobre toda la base, para siempre, un margen que nació en 2021 sin causa en los informes y que ya cede. | **No rebatida.** Es la incoherencia que anoté en el turno 1 y resolví solo con palabras. El contradictor la cuantifica y comprueba que los informes de 2016–2021 no dan la causa del salto del margen bruto. Con eso cae el primer punto de mi B223, y no tengo un dato de la causa que lo rebata. | A la baja. El precio de Sí baja a 31,44 € si el terminal vuelve al 26 % (−1,98 €) y a ≈ 31,0 € sumando O1. Cuenta para el mismo escalón. |

Son dos objeciones válidas, no rebatidas, en la misma dirección. Con la regla de movimiento del orquestador (como mucho un escalón por dirección), la conclusión baja un escalón: de concluido · Sí · comprar a concluido · Vigilar · esperar, con una condición de negocio comprobable en el informe anual de 2026.

Con la regla de precio sola, la zona no cambiaría. El precio de Sí quedaría en ≈ 31,0 € según la réplica del contradictor, por encima del precio de 27,28 €, aunque el script no lo ha recalculado. La espera no sale de la escalera: sale de que la conclusión favorable descansaba en un margen terminal que la evidencia del expediente no explica.

Cambios en `fase_c.json`:

- cubo final, acción y condición;
- `fundamento_material.resultado` (`no_procede`) y `que_lo_resolveria`;
- C104, B101, B222 y B223, con las Observaciones de C104 y B101;
- insumos, herencia de C104, comparación con la etapa 1 y «a Sí»;
- las claves nuevas `respuesta_al_contradictor` y `respuesta_al_contradictor_efecto`.

Nada más cambia. El turno 1 conserva su conclusión provisional como registro.
