# Viscofan · fase C · turnos 1 y 2 (corrección por auditoría) · 2026-11-13 · motor B · V6.4.1 experimental

Base económica: 31-dic-2025. Precio de 54,70 € del 3-nov-2026: no es una valoración a cierre de 2025 ni un backtest. Ningún hecho de 2026 (1S26, guía, recompra de 2026, renovaciones tras el cierre) apoya un juicio. «Historia» es la hoja de diez años de `datos_v63.md` (columnas C = 2016 … L = 2025). Las fases A y B son las de la 4.12, sin cambios; las reviso como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

Lo que calcula la hoja: MALO 30,04 €, NORMAL 44,18 €, BUENO 59,22 €, ponderado 42,90 € (B78:D78, C83), frente a 54,70 €. El precio está por encima del NORMAL y del ponderado; solo el BUENO lo supera. Es la historia de la fase A: buen negocio de nicho, foso que la Historia confirma pero que rinde cada vez menos en margen, y un precio sin margen (C13 = No, C20 = Riesgo real alto).

- **Peso del terminal:** 48 % / 58 % / 62 %. Ninguno pasa del 75 %: no hay G16.
- **Salto del año 11:** 2,9 / 4,7 / 9,8 puntos. La rentabilidad marginal de los años 1–10 (10,9 %, 15,7 % y 21,8 %, con f = 1,1127 y el tipo de N1) baja al ROIC terminal (8 %, 11 % y 12 %). Solo el BUENO pasa de 5 puntos (G8, punto 2); el NORMAL queda justo por debajo. Parte del salto es de la configuración: sin f serían 1,8 / 3,1 / 7,6 puntos.
- **DCF inverso:** con el margen, el S2C y el terminal del NORMAL, 54,70 € descuentan un crecimiento de ventas del 9,8 % anual en los años 1–5 (C86). Es más que mi BUENO (7 %) y que la mejor racha de la década (5,8 % anual en 2016–2021 [cálculo Historia C28:H28]). El precio de Sí descuenta un 0,9 %. Lo que se paga por crecer es 2,1 veces lo que vale el crecimiento del NORMAL (20,13 € frente a 9,61 €).
- **Tornado:** la palanca que más mueve el valor es la tasa de descuento (±1 punto: 10,04 €), la r heredada. Es información, no criterio: el valor depende sobre todo de la rentabilidad exigida. Después vienen el margen objetivo (±2 puntos: 6,43 €) y el ROIC terminal (±5 puntos: 5,70 €).
- **Semáforos:** margen por encima del Q3 del sector en los tres escenarios (G5, justificado en la fase B); r del 9,0 % por debajo de la r mínima del 9,5 % (heredada, se informa); banderas D84–D86. Lo demás pasa. Cuota implícita sin calcular: C24 está vacía.
- **Veredicto de la hoja** (A6): «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: el caso típico de buen negocio sin margen claro en el precio.
- **Bases parciales:** G7 y las referencias mecánicas usan el tipo de la Historia (19,8 %) y el S2C sin f. No las presento como comprobación del modelo experimental. La cartera es «legado»: el valor sin crecimiento (34,57 €) no tiene el límite de P0.

Lo que no cuadra a primera vista, y cómo lo resuelvo:

1. **La rentabilidad del capital nuevo del NORMAL frente a la de la década.** El NORMAL rinde un 15,7 % por euro nuevo; sin f sería un 14,1 %, cerca de C55 (14,3 %). En la Historia, el NOPAT creció unos 39 M€ para 436 M€ de capital nuevo en 2016–2025 (≈9,0 %) y 24 M€ para 319 M€ en 2021–2025 (≈7,4 %) [cálculo filas ebit y capital_invertido, t = 22,12 %]. No es una palanca mal derivada: el S2C es C53 redondeado y el margen es el de 2025. La rentabilidad incremental fue baja porque el margen de toda la base cayó del 21,1 % al 16,4 % y el circulante subió 106,1 y 83,0 M€ en 2022–2023. El NORMAL dice que el margen deja de caer; si sigue cayendo, es el MALO. Se resuelve con palabras, pero es la hipótesis de la que más depende el precio de Sí (punto 8).
2. **El FCF del NORMAL crece un 6,2 % anual y C25 = No.** Es mecánica: el crecimiento baja del 4,5 % al 2 % y con él la reinversión. C25 mira un pasado con el circulante de 2022–2023 y el capex de 115,6 M€ de 2022.
3. **p(MALO) = 0,25 con un MALO más duro que el heredado.** La Observación de B69 dice que el MALO «ya ocurrió en tres de siete años» (F29, I29, J29: 15,3 %, 15,7 % y 15,1 %), pero el MALO de este expediente lleva el margen al 14 % y ningún año de la década estuvo ahí (0 de 10). El 0,25 se sostiene por el mecanismo en marcha al cierre de 2025 (materias primas +11,1 % con ventas +4,0 %, extracto AR25 p. 23; pieles y aranceles, p. 436; mezcla, p. 139), no por la frecuencia. Lo calculé con la fórmula de la escalera: con 0,2 / 0,6 / 0,2 el precio de Sí sería 40,27 €, un 4,3 % más; la zona sigue en caro y el cubo en Vigilar. Menos de un 5 %: no pido revisarla y lo dejo en `celdas_corregidas` (B69, sin cambio).
4. **El tipo impositivo.** C52 (19,8 %) incluye el 10,1 % de 2025 por la activación de bases negativas en EE. UU. (18,0 M€; extracto AR25 p. 142). Lo corrige la configuración: N1 = 22,12 %, −1,45 € en el precio de Sí (activa_sin_N1 frente a la activa).
5. **Acciones y fechas.** El motor B resta la deuda del 31-dic-2025 y divide por N = 45,479209 millones, la media «diluida» de 2025, que contradice su propia definición: queda por debajo de la básica (45,656226) con el mismo numerador (nota 20, AR_2025 PDF p. 119). No es la cifra de la fecha del puente (45,993399 en circulación a 31-dic-2025) ni la del precio. La elección es humana y está pendiente (VISCOFAN-ACCIONES); no la tomo. En el libro de la 4.12, las alternativas mueven el precio de Sí entre −0,11 y −0,49 € (hasta −1,3 %), todas en caro; aquí no están calculadas y, por proporción, serían del mismo orden. No afecta a mi conclusión: el precio está un 41,7 % por encima del precio de Sí (÷ precio de Sí). La evidencia de C61 usa esa misma media; con la básica la serie también baja desde 46,60 M en 2016, así que C61 se sostiene.
6. **Mi lectura de la 4.12 sobre la inversión mezclaba perímetros.** Escribí que en 2023–2025 los pagos por inmovilizado fueron 0,90–0,94 veces la amortización. Esa amortización incluye la de los derechos de uso (27,1 M€ en 2021–2025) y el capex no incluye sus altas (24,1 M€). Con el perímetro coherente con el motor B (NIIF 16) son 1,00 / 0,97 / 1,02 veces; solo con activos propios, 0,98 / 0,96 / 1,01. La reposición sigue sin superar de forma visible a la amortización, pero «por debajo» pasa a «igual».
7. **El ROIC terminal y la estructura activa.** B18:D18 se anclaron en ROIC contables sobre todo el capital (fila 33, F33, H18). Con esa medida, sumar el requisito y dejar el ROIC sin cambio (SR1) es la combinación de un ROIC neto de reposición, que no es como se midió (Q-ROIC1). Síntoma: SR1 sube el S2C de los años por f y no toca el terminal, y el salto del año 11 se ensancha ≈1,6 puntos en el NORMAL y ≈2,2 en el BUENO. Es un parámetro de la configuración, no una celda de A o B: no pido cambiarlo; lo evalúo en el punto 9 (SR2: +0,52 €).
8. **Recompras por encima del valor.** En 2025 se recompraron 94,0 M€ (extracto AR25 p. 144), un año en que la acción cotizó a una media diaria de 59,47 € (p. 147). 59,47 € no es el precio medio de la recompra, que no está en mis entradas; una aproximación (94,0 M€ ÷ 1.599.709 acciones propias compradas en 2025, conciliación de acciones de la 4.13) da ≈58,8 €, si las dos cifras cubren las mismas compras. Cualquiera de las dos está por encima de mi NORMAL (44,18 €). El modelo no lo recoge; va a lo no numerable.
9. **C97 (insiders) contradice la evidencia de fase 1.** La fase A puso «Neutral» como supuesto técnico porque no veía operaciones de directivos, y en el turno 1 lo repetí como dato «no hallado». La evidencia de fase 1 sí las tiene (Control maestro fila 76; CNMV, art. 19 MAR; 7-oct-2025 a 7-oct-2026): 10 compras en mercado (≈21,9 mil acciones, ≈1,19 M€) de 6 personas (CEO, COO, 2 consejeros y 2 vinculadas) frente a 1 venta de 700 acciones; las 22 operaciones restantes son scrip a 0 €. **Lo que se puede fechar:** la ventana empieza dentro de 2025 y acaba después de la base; de los nueve números de registro, siete empiezan por 2025 y dos por 2026, que leo como año de registro (inferencia). **Lo que no:** la fecha de cada operación y qué compras, venta o scrip lleva cada notificación, así que no sé cuántas de las 10 compras ni cuánto de los ≈1,19 M€ son anteriores al 31-dic-2025. Con la regla de C97 (12 meses, hechos de fase 1) la evidencia apunta a «Comprando». La celda es de la fase A: no la reescribo; va en `celdas_corregidas` sin cambio. **Efecto:** ninguno en la escalera ni en la conclusión, porque C97 no entra en ninguna palanca. Las compras suman un 0,05 % de la capitalización [cálculo sobre C41] a ≈54 € de media [cálculo]: una señal a favor de la alineación de la dirección, no un argumento de valor.

Las 52 celdas cuentan una sola historia. No pido mover ninguna palanca.

## 2. Desviaciones pendientes

`gramatica.md` deja una sin justificar: **G8 en el BUENO** (9,8 puntos). No hay G16 (el terminal pesa el 58 % en el NORMAL) ni G17 (C24 vacía). Las tres G5 están justificadas en la fase B.

**G8 · BUENO · fundamentada.** En los años 1–10 cada euro nuevo rinde un 21,8 % (1,4 × 1,1127 × 0,18 × (1 − 0,2212)) porque se juntan dos cosas que solo ocurren una vez. Una: se llena capacidad ya pagada o en marcha al cierre de 2025 (colágeno en EE. UU., plásticos en México, extrusión en Serbia; extracto AR25 p. 65; el 37 % de la inversión de 2025 fue a capacidad, p. 143). Dos: el margen sube del 16,4 % al 18,0 % al repartir costes fijos. Es crecimiento por eficiencia y es finito (GV p. 32; I1). Cuando el margen llega al techo de 2020–2021 (G29, H29) y las plantas están llenas, el euro nuevo vuelve a pagar planta a coste completo y rinde lo que rindió el capital en el peor año de la década: 12,1 % en 2019 (F33). En el año 11 no se pierde el foso: se acaban la capacidad ociosa ya pagada y el recorrido del margen. El 12 % sigue 3,7 puntos por encima de la tasa del motor (8,3 %). Unos 2,2 de los 9,8 puntos los pone f; con la base de la V6.3 el salto sería de 7,6. Tengo precedente propio en las dos direcciones: en 2019–2025, saliendo del mínimo de margen, el capital incremental rindió ≈18,9 %; en 2016–2025, ≈9,0 %. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). No cambio la clase ni la cifra de D18; lo contaré en la tesis.

## 3. ¿Hay que mover palancas?

No. Comprobé la aritmética de la fase B contra la Historia: pendiente del margen de 2016–2025 de −0,49 puntos por año (cinco años desde el 16,4 % dan el 13,9 %, B15 = 0,14); crecimiento medio de 2017–2025 sin 2022 del 4,18 %; CAGR de 2016–2021 del 5,8 %; mercado en valor +2,18 % anual en 2016–2025; S2C de 2,03 (2016–2021), 0,89 (2021–2025) y 1,19 (2016–2025). Todo cuadra. No encuentro perímetro ni dato equivocado en las palancas. El único apoyo flojo es la frecuencia de B69: corregir la probabilidad movería el precio de Sí un 4,3 % sin cambiar zona ni cubo. En `celdas_corregidas` registro que revisé C62, C18 y C61 de la fase A y B69 de la fase B, y que las mantengo.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** La etapa 1 dejó Vigilar con precio de Sí de 25,1 € y un C104 con un porcentaje. Revisé las g heredadas: tienen argumento propio. Miré también como hipótesis mi fase C de la 4.12 sobre las mismas cuentas: elegía SR1 y leía la inversión de 2023–2025 por debajo de la amortización. Las dos cosas no aguantan (Q-ROIC1 y perímetro). Y acepté sin comprobarlo el «no consta» de la fase A sobre los directivos (C97), cuando la fila 76 del Control maestro recoge 10 compras y 1 venta notificadas a la CNMV. Cambio: estructura más coherente sin elegir, ratios corregidas, C97 anotada como incoherencia de la fase A y el dato de directivos fuera de «no hallado»; en el turno 2 reescribo B101, B102 y C104.
2. **Anclaje en el precio o en la fuente externa.** El NORMAL queda un 19,2 % por debajo del precio (÷ precio). Las probabilidades se movieron hacia el MALO. No usé el valor de Simply Wall St (118,26 €, C38) ni el consenso. Cambio: ninguno.
3. **Consistencia y compromiso.** El cubo se decidió en la fase A. El precio descuenta un 9,8 % de crecimiento, más que mi BUENO, y ninguna de las dieciocho variantes sale de caro. Cambio: ninguno en celdas.
4. **Historia bonita / viento de cola atribuido a la empresa.** Del 4,5 % del NORMAL, unos 3 puntos son del nicho (mercado del 2–4 % en volumen, extracto AR25 p. 181; tripa animal de la mitad del mercado al 44 %, IA16 p. 42 e IA23 p. 146), un punto es precio que sigue al coste y medio punto es cuota. Cambio: la tesis dirá que el crecimiento es sobre todo del nicho.
5. **Optimismo del BUENO frente a la tasa base.** El BUENO pide un 7 % (la mejor racha dio un 5,8 %) y un 21,8 % por euro nuevo, más que el mejor ROIC de la década (16,7 %); unos 2,2 puntos los pone f. Sus ventas del año 10 serían ≈32 % del mercado si este creciera un 3 % anual, frente a ≈24,5 % hoy. Plausible, en el borde, y menos probable que el MALO. Cambio: ninguno; lo llamo la historia menos probada.
6. **Doble castigo del mismo riesgo.** La deuda solo la resta el motor B. El margen está como gravedad (14 %) y como frecuencia (0,25), medida aparte (+4,3 % con 0,2). La reposición puede contarse en parte dos veces en el terminal si el ROIC contable se mantiene y se suma el requisito (SR1); SR2 lo evita (+0,52 €). Una quiebra sobre un riesgo que ya está en el MALO sería contarlo dos veces (PA pp. 20–21; E6). Cambio: anotado en el punto 9.
7. **Disponibilidad (lo vívido del extracto).** Lo vívido son la «inflación sustancial» de las pieles y las coberturas superadas (extracto AR25 p. 436). Lo contrasté con la fila 29: la pendiente existe desde 2016 y 2024–2025 están por encima de 2023. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad (guía de la dirección como hecho).** No copié la guía de 2026: el NORMAL es un 4,5 %. La cuota (30 % → 41 %) es una estimación de la empresa; C18 se sostiene con el ROIC de las cuentas. Tampoco tomo la configuración como autoridad: θ = 0,5 es el punto medio del dominio. «will frequently be a lie» (TCI p.60; HIM). Cambio: la tesis lo dirá.
9. **¿El MALO es de verdad malo?** Sí. Lleva el margen al 14 %, por debajo del mínimo de la década (15,1 %), con el ROIC terminal en la tasa: vale 30,04 €, menos que el valor sin crecimiento (34,57 €). No cubre perder cuota o volumen; por eso no es un suelo. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: la tesis inversa contará la pérdida de cuota.
10. **Lo no numerable que pesa y no está en las palancas.** El reparto por encima de la caja con deuda a corto y las recompras de 94,0 M€ en un año en que la acción cotizó a una media diaria de 59,47 € (extracto AR25 pp. 144, 147); las «acusaciones en Danville» sin desenlace (p. 150); un competidor que no sé nombrar (p. 399); una cifra de acciones publicada que contradice su definición; y, a favor, las compras de directivos de la ventana 7-oct-2025 a 7-oct-2026 (Control maestro fila 76). «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM). Cambio: tesis inversa, B222 y C98; las acciones quedan como decisión pendiente.

## 5. Cubo y conclusión provisionales

En orden de mando. **Bloqueo:** no hay (0 errores de gramática; el estado técnico INCOMPLETO solo espera las predicciones del turno 2). **Límite del modelo:** no hay; el motor B calcula los tres escenarios y la configuración es válida. **Descalificadores:** ninguno aplica (fase A, sección 3). **Dato ausente material:** ninguno (punto 6). **Fundamento material:** la lista D10 está vacía (punto 7). **Zona:** caro. 54,70 € está por encima del ponderado (42,90 €). El precio de Sí es 38,62 € (P\*; el tope del NORMAL no actúa): el precio de Sí está un 29,4 % por debajo del precio (÷ precio), y el precio, un 41,7 % por encima del precio de Sí (÷ precio de Sí). La regla antigua de la hoja (C156) da 30,04 €.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`, con precio de Sí ≤ 38,62 €**, objetivo condicionado por la configuración (punto 9). «We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). La escalera es una convención experimental (k = 3) y la zona no mide el riesgo. Ni la cifra de acciones ni el perímetro cambian esta conclusión.

## 6. Datos ausentes (S-19)

Revisé los 22 datos de `datos_ausentes.json` uno a uno (detalle en el JSON). Ninguno es material para `esperar` con precio objetivo. Los que más se acercan:
- **Competidores, cuota desde 2022, desglose de volumen, precio y mezcla, y margen por segmento o región.** Afectan a por qué cayó el margen y a cuánto dura. Pero la escalera usa el margen consolidado y los tres escenarios cubren el 14–18 %, con el MALO por debajo del mínimo de la serie y un 0,25. Serían materiales para un `comprar` que dependiera del BUENO; no para esperar a 38,62 €.
- **Covenants, rating y calendario de renovación.** Afectan a C22 = 0. Con datos del cierre de 2025: 0,87 veces el EBITDA, EBIT 23 veces los intereses, 155,3 M€ de líneas libres (extracto AR25 p. 98) y sin impagos (p. 122).
- **Compras y ventas de directivos.** No es un dato ausente: el extracto no lo encontró, pero la evidencia de fase 1 lo tiene (Control maestro fila 76: 10 compras y 1 venta, 7-oct-2025 a 7-oct-2026). Falta solo fechar cada operación frente a la base. Contradice C97 (punto 1.9) y no es material para esperar: no entra en ninguna palanca ni en la escalera.
- **Plan de capex de 2026.** Lo que fundaría θ es el desglose del capex de 2021–2024, no un plan futuro, y θ es una hipótesis sin fundamento suficiente (punto 9), no un dato ausente.

## 7. Fundamento material (D10)

Recorrí B14:D16, B18:D18, B68:D69, C22, C23, C76, C44, C62, C8, C6 y B65:D66. Ninguna es de clase «sin juicio propio» ni «técnico», y todas las Observaciones citan hechos con celda de la Historia o página del extracto. Las seis narrativas tienen mecanismo y «qué lo pararía» con hechos de esta empresa (pieles, extracto AR25 p. 436; mezcla, p. 139; capacidad, p. 65; EE. UU., pp. 66, 140; sustitutos, p. 399). Las palancas que coinciden con su referencia (C15, B16, C16, D16, B18, D18) tienen su propio hecho y un rango acotado por la Historia. B69 tiene un apoyo de frecuencia mal casado (punto 1.3), pero su mecanismo sí está en los hechos. C97 (técnico, y contradicha por la evidencia de fase 1, punto 1.9) y C56 (r heredada) no son hipótesis materiales de §B.6; C55 es un dato con una elección de definición pendiente. **Lista vacía.**

La conclusión provisional no es favorable: `resultado = no_procede`, sin comprobación conjunta y con `sobrevive` en null. Los parámetros de la configuración sin fundamento suficiente no entran en esta lista con `esperar` (solo con `comprar`): condicionan el objetivo por el protocolo del punto 9.

## 8. La hipótesis que más condiciona y qué la resolvería

La lista está vacía, así que la nombro por juicio y no por el tornado: **C15 y C18 del NORMAL: el margen deja de erosionarse en el 16,5 % y el capital nuevo rinde un 11 % a perpetuidad.** La década muestra un margen del 21,1 % al 16,4 % y una rentabilidad incremental de ≈9 % (≈7,4 % en 2021–2025), mientras el NORMAL rinde un 15,7 % por euro nuevo en los años 1–10. «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

**Qué la resolvería:** el desglose de la variación de ventas y de margen en volumen, precio, mezcla y coste de pieles por tecnología, que no se publica (extracto AR25 p. 139); se pide a Relación con Inversores. Y el margen EBIT consolidado del informe anual de 2026: si es de al menos el 16 % con las pieles caras, confirma el NORMAL; si baja del 15 %, lo desplaza hacia el MALO.

## 9. Configuración V6.4.1 (experimental, no adoptada)

Doce parámetros activos (N2 vacío por elección de la configuración). Las dieciocho variantes calculadas quedan en **caro** (precio de Sí 36,88–41,81 €, ponderado 41,16–46,26 €): `zona_igual_en_variantes_calculadas = true`, solo para esa tabla. Ningún parámetro es material para la acción: para cambiarla, el precio de Sí tendría que pasar de 54,70 € (+42 %), y el mayor efecto calculado de un parámetro es de 1,74 €.

| Parámetro | Cobertura · base | Efecto en el precio de Sí | Fundamento suficiente | Material para el objetivo |
|---|---|---|---|---|
| N1.tipo (22,12 %) | conjunta necesaria · calculada | −1,45 € (−3,6 %) | sí: activación de 18,0 M€ (extracto AR25 p. 142) | sí, pero fundado: no condiciona |
| N1.escudo | aislado · calculada | −0,06 € | sí (convención) | no |
| N3.regla (R1) | conjunta necesaria · calculada | 0,00: las ventas no caen | no (sin año que la pruebe), pero inerte | no |
| N3.circulante (48,28 %) | conjunta · juicio | inerte con R1 | sí (balance de 2025) | no |
| PM1.estructura (SR1) | aislado · calculada | S −0,51 · SR2 +0,52 · SRF +1,68 · H +1,74 | no | sí |
| PM1.familia (Θ) | conjunta · juicio | sin variante con requisito | no: los hechos no distinguen Θ de Λ | no (juicio: λ ≤ 1,16 cae dentro del rango de θ) |
| PM1.parametro (θ = 0,5) | aislado · calculada | θ = 0: +1,74 · θ = 1: −1,74 | no: punto medio sin central | sí |
| PM1.convencion_anios | aislado · calculada | −0,15 € | sí (convención) | no |
| PM1.convencion_terminal | aislado · calculada | +0,32 € | sí (convención) | no |
| PM1.roic_terminal | conjunta necesaria · calculada | SR2 +0,52 € | no: Q-ROIC1 abierta | no: dentro del rango de la estructura |
| PM1.cartera (legado) | conjunta · juicio | ≈0,11 M€ al año | sí (inmaterial) | no |
| PM1.perimetro (NIIF 16) | aislado · calculada | Caja +0,67 € (+1,34 € con θ = 1) | sí: coherente con el motor B | sí, pero fundado: no condiciona |

Como juicio, sin umbral adoptado, llamo material para el objetivo a lo que lo mueve en torno a 1 € (≈2,5 % del precio de Sí) o más en alguna de sus variantes. Revisé las discrepancias con la configuración: en N3.regla y PM1.roic_terminal mi confianza (baja) es menor que la suya (media), por las razones del JSON; en las demás no hay.

**Perímetro.** NIIF 16 es el coherente con cómo trata el motor B los arrendamientos: el capital invertido los incluye (2025: 927,6 + 304,1 + 12,2 − 62,8 = 1.181,2 M€), el puente resta su pasivo (C64) y el EBIT ya descuenta su amortización. «Caja» mete esa amortización en la D&A y deja fuera las altas que la reponen (24,1 frente a 27,1 M€ en 2021–2025). La elección formal sigue siendo humana (VISCOFAN-PERIMETRO).

**Mantenimiento.** ¿Supera la reposición a la amortización? Con los hechos del cierre de 2025, no se ve. El exceso de la década se concentra en años de capacidad nueva (2021–2022: colágeno en cinco países, celulósica en Danville; extracto IA21 p. 210, CA23 p. 98). En 2023–2025, con NIIF 16, la inversión fue 1,00 / 0,97 / 1,02 veces la amortización con ventas casi planas; en 2024, sin crecimiento, quedó por debajo. En 2025, de 84,1 M€, 53,2 M€ no fueron capacidad, menos que la amortización de los activos propios (79,7 M€; extracto AR25 p. 143). No hay hornos: son líneas de extrusión y conversión y la cogeneración, sin vida útil publicada. Chequia sería reposición pura, pero es posterior a la base. Lectura: θ en el extremo bajo, donde todas las estructuras coinciden (40,35 €). **Estructura más coherente: ninguna con base suficiente (null).** S y SR1 son las menos coherentes con cómo se fijaron las palancas (Q-ROIC1: con un ROIC contable, la coherente es SR2). H no queda excluida: un año sin crecimiento paga todo el requisito en H, y en 2021–2022 la capacidad nueva incluyó renovación tecnológica, donde reposición y crecimiento se solapan. SR1 frente a SRF depende de la mezcla: el circulante fue el 75 % de la reinversión de 2021–2025 y es el 59 % de la futura por euro de ventas en el NORMAL; SRF quita 0,171 € por euro de ventas nuevas y SR1 0,092 €, frente a 0,096 € de la historia. `adoptada = false`.

**Avisos de dominio.** Solo el factor de reestimación, en la activa y en las variantes (lectura sin umbral, f de 1,0000 a 1,2539). En la activa lleva el S2C efectivo a 1,00 / 1,22 / 1,56. En el extremo inferior (θ = 1, 36,88 €) el capital nuevo del NORMAL rendiría un 17,7 %, el doble que la década, y su salto del año 11 pasaría de 5 puntos: ese extremo es menos coherente con los hechos que θ = 0. Depende de θ, que ya condiciona el objetivo: no material por sí solo, lo digo en el diagnóstico.

**Objetivo (protocolo `objetivo_condicionado`, ensayo).** Esperar por precio, con dos condicionantes: PM1.estructura y PM1.parametro. La acción se sostiene en todo el ámbito calculado (las dieciocho variantes, todas en caro). Tratamiento: `objetivo_condicionado`: cierro `concluido · Vigilar · esperar` con el precio de Sí de 38,62 € como objetivo condicionado a esas dos hipótesis (punto 11). Las estructuras que encuentro más coherentes (SR2, H, SRF) y el extremo bajo de θ dan entre 39,14 y 40,35 €: el objetivo activo está en la parte baja del rango calculado. Información que falta: el desglose por año y destino de la inversión de 2021–2024, cómo se pensó el ROIC de la fase B y la vida útil de las líneas frente a su amortización. «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 10. Turno 2 · comprobación conjunta

No existe `comprobacion_conjunta.json`: con conclusión `esperar` y lista D10 vacía no procedía. `sobrevive` queda en null y `resultado` en `no_procede`. El único rango del precio de Sí que informo es el de las dieciocho variantes calculadas de la configuración (36,88–41,81 €, todas en caro): una tabla de sensibilidad, no un intervalo de confianza, y no cubre hipótesis no exploradas (la familia Λ no tiene variante con requisito).

## 11. Conclusión

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 38,62 €** (precio de Sí de `precio.json`), **condicionado (provisional)** a PM1.estructura y PM1.parametro de la configuración V6.4.1 (tratamiento `objetivo_condicionado`, protocolo de ensayo). En orden de mando: no hay bloqueo, límite del modelo, descalificador, dato ausente material ni hipótesis de A o B sin fundamento. Manda la zona, `caro`: 54,70 € está por encima del ponderado (42,90 €) y del NORMAL (44,18 €). La escalera es convención experimental (k = 3). El precio del MALO (30,04 €) no es un suelo. Dos elecciones humanas siguen pendientes y no las tomo: la cifra de acciones (VISCOFAN-ACCIONES) y el perímetro (VISCOFAN-PERIMETRO); ninguna cambia la zona.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 38.62 · zona caro · precio de Sí ≤ 38.62 · precio esc. MALO 30.04 · ponderado 42.9 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional) a PM1.estructura y PM1.parametro de la configuración V6.4.1 · rango calculado del precio de Sí 36.88–41.81 en 18 variantes (tabla de sensibilidad, no intervalo de confianza)». La decisión de cartera es de José Luis.

El veredicto de la hoja (A6, «DESCARTADA POR FILTRO PABRAI») y mi cubo difieren por C13 = No: la hoja descarta lo que no es barato a ojo; yo vigilo un buen negocio que entiendo a un precio sin margen.

C93 = Sí. El g del NORMAL (2 %) se sostiene: el terminal reinvierte el 18 % del NOPAT a un ROIC del 11 %, el salto del año 11 es de 4,7 puntos y el terminal pesa el 58 %. C103 = No: el foso existe pero rinde cada vez menos (margen del 21,1 % al 16,4 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

## 12. Tesis (B101)

Viscofan fabrica envolturas para embutidos en 22 plantas para más de 1.700 clientes, ninguno por encima del 10 % de las ventas (extracto AR25 pp. 121, 137), y su ROIC no bajó del 12,1 % en diez años (Historia fila 33): es un buen negocio de nicho con un foso de escala y proceso. El foso rinde menos que antes: el margen EBIT pasó del 21,1 % al 16,4 % mientras la cuota que estima la propia empresa subía del 30 % al 41 % (extracto AR19 p. 121, CF22 p. 182), y el crecimiento es sobre todo del nicho (AR25 p. 181). Mi NORMAL vale 44,18 €, con el MALO en 30,04 € y el BUENO en 59,22 €; en el BUENO, el salto del año 11 (9,8 puntos) es mi hipótesis de que la capacidad ociosa ya pagada y el recorrido del margen se agotan y el capital nuevo vuelve a rendir el 12 % del peor año (F33). A 54,70 € el precio descuenta un 9,8 % de crecimiento anual de las ventas (C86), más que mi BUENO, y la empresa reparte por encima de su caja con deuda a corto (AR25 pp. 98, 144), aunque sus directivos compraron ≈1,19 M€ en mercado entre el 7-oct-2025 y el 7-oct-2026 (CNMV, Control maestro fila 76), en parte después de la base. Vigilar: esperar a 38,62 €, objetivo condicionado a la estructura del mantenimiento y a θ (36,88–41,81 € en las variantes calculadas).

## 13. Tesis inversa (B102)

Defiendo el No con hechos.

- **Costes que no controla.** El consumo de materias primas pasó de 370,5 a 411,6 M€ en 2025 con las ventas un 4,0 % arriba (extracto AR25 p. 23); las pieles europeas sufren «inflación sustancial» y las coberturas de dólar fueron superadas (p. 436).
- **Cuota pagada con precio.** La cuota sube, pero el margen cayó 4,7 puntos en diez años (Historia C29, L29) y en 2025 la mezcla fue inferior con volumen récord (p. 139).
- **El capital nuevo apenas rinde su coste.** 436 M€ de capital nuevo en 2016–2025 para unos 39 M€ de NOPAT: ≈9 %, frente a una tasa del motor del 8,3 %, y ≈7,4 % en 2021–2025 [cálculo Historia].
- **Reparte más caja de la que genera.** La caja libre al accionista no crece desde 2019 (Historia fila 35). Aun así pagó 145,1 M€ al accionista en 2025, 94,0 M€ en recompras en un año en que la acción cotizó a una media diaria de 59,47 € (pp. 144, 147), por encima de mi NORMAL, y la deuda pasó de 116,8 a 304,1 M€, con 227,4 M€ de bancos a un año (p. 98).
- **Lo que no sé.** Quién es el competidor que gana y en qué quedó Danville (p. 150). Pet Mania perdió actividad por un arancel (p. 140).
- **El precio frente al MALO.** Si el margen sigue la pendiente hasta el 14 %, la hoja da 30,04 € (B78) y el mercado paga un 82 % más. Y ese MALO aún no recoge perder cuota.

## 14. Predicciones (dado el NORMAL)

1. Ventas consolidadas de 2027 entre 1.330 y 1.450 M€ · 2028-03-31 · 0,65.
2. Margen EBIT consolidado de 2027 entre el 15,5 % y el 17,5 % · 2028-03-31 · 0,6.
3. Pagos por adquisición de inmovilizado de 2027 de no más de 1,3 veces la amortización total del ejercicio · 2028-03-31 · 0,65.

Las tres son sobre el negocio y se comprueban con el informe anual de 2027. La tercera se mide con la definición de caja (pagos frente a toda la amortización), la misma con la que se calcula su probabilidad. Son la autopsia de este análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 15. B222, B223 y qué me haría cambiar de cubo

- **B222:** la hipótesis fundamentada de la que más depende el precio de Sí: el margen deja de erosionarse en el 16,5 % (C15) y el capital nuevo rinde un 11 % (C18). El objetivo queda además condicionado por la estructura del mantenimiento y θ (hasta ±1,74 €).
- **B223:** el desglose de volumen, precio, mezcla y coste de pieles por tecnología (Relación con Inversores) y el margen EBIT del informe anual de 2026 (≥ 16 % confirma el NORMAL; < 15 % lo desplaza al MALO); para θ y la estructura, el desglose por año y destino de los pagos por inmovilizado y de las altas de derechos de uso de 2021–2024 (como el de 2025, extracto AR25 p. 143) y la respuesta a Q-ROIC1.
- **A Sí:** un precio de 38,62 € o menos con el NORMAL intacto, o un margen de al menos el 17,5 % dos años con cuota publicada al alza; antes, resolver estructura y θ.
- **Insiders (C97).** La fase A dejó Neutral como técnico; la evidencia de fase 1 (Control maestro fila 76) recoge compradores netos en la ventana 7-oct-2025 a 7-oct-2026. No la reescribo; no mueve la escalera ni el cubo. Ventas netas de directivos en el registro de la CNMV de 2026–2027 sí pesarían hacia No en la confianza.
- **A No:** margen por debajo del 15 % dos años con ventas planas; deuda neta por encima de 2,5 veces el EBITDA para seguir pagando al accionista; o que Danville revele un problema de integridad.
- **A Demasiado difícil:** que la caída del margen venga de un sustituto tecnológico que no pueda juzgar (p. 399), o una compra grande fuera del nicho.

## 16. Comparación con la etapa 1

Coinciden el cubo (Vigilar) y la razón: precio sin margen. El precio de Sí sube de 25,1 € a 38,62 € por cuatro cambios:

- **Motor.** La etapa 1 valoró el FCF al accionista sin restar deuda; yo valoro con el motor B y resto 279,9 M€.
- **MALO.** El suyo era caja plana; el mío lleva el margen al 14 %, y vale 30,04 €.
- **Regla.** La suya era mín(MALO, 0,75 × ponderado), que en esta hoja daría 30,04 € (C156); la mía es la escalera k = 3.
- **Configuración V6.4.1.** Tipo sin activaciones fiscales (−1,45 €) y reposición con SR1, θ = 0,5 y perímetro NIIF 16 (−1,74 €): −3,19 € frente a la V6.3 efectiva (41,81 €).

La etapa 1 acertó en que el precio descuenta más crecimiento del que la empresa ha dado. Se equivocó al usar como hechos datos de 2T26, posteriores a la base, y al poner un tamaño de posición, que no me corresponde.

## Cambios frente al expediente de la 4.12

- Valores por escenario 30,69 / 44,85 / 60,00 € → 30,04 / 44,18 / 59,22 €; ponderado 43,59 → 42,90 €; precio de Sí 39,29 → 38,62 €. Motivo: el perímetro de la inversión pasa de Caja a NIIF 16 (plantilla V6.4.1): el exceso histórico sube de 40,8 M€ (perímetro Caja) a 64,9 M€ (NIIF 16) y f de 1,074 a 1,113. El caso de la 4.12 es ahora la variante `perimetro_alternativo` (39,29 €).
- Salto del año 11: 2,5 / 4,2 / 9,1 → 2,9 / 4,7 / 9,8 puntos. Motivo: f más alto en los años 1–10 con el ROIC terminal sin reestimar.
- DCF inverso: 9,6 % → 9,8 %; cuánto pagas por crecer 2,0 → 2,1 veces. Motivo: valores más bajos con el mismo precio.
- Estructura más coherente: SR1 → ninguna con base suficiente (null). Motivo: Q-ROIC1 (con ROIC contables, la coherente es SR2), H no excluida por invertir sin crecer, y SR1 frente a SRF depende de la mezcla de fijo y circulante.
- Ratios de inversión de 2023–2025: 0,90–0,94 → 1,00 / 0,97 / 1,02 veces la amortización. Motivo: la comparación anterior mezclaba perímetros.
- PM1.familia y PM1.roic_terminal: de «fundamento suficiente» a «sin fundamento suficiente», no materiales para el objetivo. Motivo: los hechos no distinguen Θ de Λ, y el ROIC terminal sin cambio solo es coherente con un ROIC neto de reposición.
- Nuevo: PM1.perimetro (NIIF 16, fundado; Caja +0,67 €) y la cifra de acciones como decisión pendiente (VISCOFAN-ACCIONES; N contradictoria, alternativas en caro).
- Precio objetivo: 39,29 € → 38,62 €, condicionado (provisional) a PM1.estructura y PM1.parametro; rango calculado 38,22–41,81 € en 12 variantes → 36,88–41,81 € en 18.
- Corrección por auditoría: C97 (Neutral, fase A) queda anotada como contradicha por la evidencia de fase 1 (Control maestro fila 76: 10 compras y 1 venta de directivos, 7-oct-2025 a 7-oct-2026; siete registros de 2025 y dos de 2026, sin poder fechar cada operación frente a la base); el dato de directivos deja de ser «no hallado». Sin efecto en la escalera ni en la conclusión.
- Corrección por auditoría: 59,47 € es la media diaria de la cotización de 2025, no el precio de la recompra (no publicado; ≈58,8 € aproximado con 1.599.709 acciones propias compradas).
- Sin cambio: cubo Vigilar, conclusión `esperar`, lista D10 vacía, ningún dato ausente material, G8 en el BUENO con el mismo mecanismo, hipótesis que más condiciona (C15 y C18 del NORMAL) y qué la resolvería.
