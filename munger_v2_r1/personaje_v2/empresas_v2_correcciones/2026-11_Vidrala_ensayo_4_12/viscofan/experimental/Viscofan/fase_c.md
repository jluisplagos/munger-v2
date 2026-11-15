# Viscofan · fase C · turnos 1 y 2 · 2026-11-12 · motor B · V6.4 experimental

Base económica: 31-dic-2025. Precio de 54,70 € del 3-nov-2026: no es una valoración a cierre de 2025 ni un backtest. Ningún hecho de 2026 (1S26, guía, programa de recompra de 2026, renovaciones tras el cierre) apoya un juicio. «Historia» es la hoja de diez años de `datos_v63.md` (columnas C = 2016 … L = 2025).

## 1. Una sola historia

Leo las 52 celdas de A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

Lo que calcula la hoja: MALO 30,69 €, NORMAL 44,85 €, BUENO 60,00 €, ponderado 43,59 € (B78:D78, C83), frente a 54,70 €. El precio está por encima del NORMAL y del ponderado; solo el BUENO lo supera. Es la historia de la fase A: buen negocio de nicho, foso que la Historia confirma pero que rinde cada vez menos en margen, y un precio sin margen (C13 = No, C20 = Riesgo real alto).

- **Peso del terminal:** 48 % / 59 % / 62 %. Ninguno pasa del 75 %: no hay G16.
- **Salto del año 11:** 2,5 / 4,2 / 9,1 puntos. La rentabilidad marginal de los años 1–10 (10,5 %, 15,2 % y 21,1 %, ya con f = 1,074 y el tipo de N1) baja al ROIC terminal (8 %, 11 % y 12 %). Solo el BUENO pasa de 5 puntos: es G8 y lo justifico en el punto 2.
- **DCF inverso:** con el margen, el S2C y el terminal del NORMAL, 54,70 € descuentan un crecimiento de ventas del 9,6 % anual en los años 1–5 (C86). Es más que mi BUENO (7 %) y que la mejor racha de la década (5,8 % anual en 2016–2021 [cálculo Historia C28:H28]). El precio de Sí descuenta un 0,9 %. Lo que se paga por crecer es 2,0 veces lo que vale el crecimiento del NORMAL (19,49 € frente a 9,64 €).
- **Tornado:** la palanca que más mueve el valor es la tasa de descuento (±1 punto: 10,21 €), que es la r heredada. Es información, no criterio: el valor depende sobre todo de la rentabilidad exigida. Después vienen el margen objetivo (±2 puntos: 6,43 €) y el ROIC terminal (±5 puntos: 5,70 €).
- **Semáforos:** margen por encima del Q3 del sector en los tres escenarios (G5, justificado en la fase B); r del 9,0 % por debajo de la r mínima del 9,5 % (heredada, se informa); banderas D84–D86 de poco margen y crecimiento implícito por encima del BUENO. Crecimiento, ROIC marginal, ROIC terminal, peso del terminal, S2C medio, orden de escenarios, tipo y motor, y f pasan. Cuota implícita sin calcular: C24 está vacía.
- **Veredicto de la hoja** (A6): «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: el caso típico de buen negocio sin margen claro en el precio.
- **Bases parciales:** G7 y las referencias mecánicas usan el tipo de la Historia (19,8 %) y el S2C sin f. No las presento como comprobación del modelo experimental. La cartera es «legado» (sin P0): el valor sin crecimiento (35,21 €) no tiene ese límite.

Lo que no cuadra a primera vista, y cómo lo resuelvo:

1. **La rentabilidad del capital nuevo del NORMAL frente a la de la década.** El NORMAL rinde un 15,2 % por euro nuevo. En la Historia, el NOPAT creció unos 39 M€ para 436 M€ de capital nuevo en 2016–2025 (≈9,0 %) y 24 M€ para 319 M€ en 2021–2025 (≈7,4 %) [cálculo filas ebit y capital_invertido, t = 22,12 %]. No es una palanca mal derivada: el S2C es el de la Historia (C53, 1,15) y el margen es el de 2025 (16,4 %). La rentabilidad incremental fue baja porque el margen de toda la base cayó del 21,1 % al 16,4 % y porque el circulante subió 106,1 y 83,0 M€ en 2022–2023. El NORMAL dice que el margen deja de caer; si sigue cayendo, es el MALO, que ya lleva el S2C de 2021–2025 (0,9). Se resuelve con palabras, pero es la hipótesis de la que más depende el precio de Sí (punto 8).
2. **El FCF del NORMAL crece un 6,2 % anual y C25 = No.** Es mecánica: el crecimiento baja del 4,5 % al 2 % y con él la reinversión. C25 mira el pasado, que lleva el circulante de 2022–2023 y el capex de 115,6 M€ de 2022. Coherente si no se repite ese choque, que es justo el MALO.
3. **p(MALO) = 0,25 con un MALO más duro que el heredado.** La Observación de B69 dice que el MALO «ya ocurrió en tres de siete años» (F29, I29, J29: 15,3 %, 15,7 % y 15,1 %). Esos años eran el MALO del expediente heredado (vuelta al mínimo, 15 %). El de este expediente lleva el margen al 14 % por la pendiente de la década (B15), y ningún año de la década estuvo en el 14 % o por debajo (0 de 10). El 0,25 se sostiene por el mecanismo en marcha al cierre de 2025 (materias primas +11,1 % con ventas +4,0 %, extracto AR25 p. 23; pieles y aranceles, p. 436; mezcla, p. 139) y por la pendiente de la fila 29, no por la frecuencia. Lo calculé: con 0,2 / 0,6 / 0,2 el precio de Sí sería 40,95 €, un 4,2 % más; la zona sigue en caro y el cubo en Vigilar. Menos de un 5 %: no pido revisarla y lo dejo escrito en `celdas_corregidas` (B69, sin cambio).
4. **El tipo impositivo.** C52 (19,8 %) incluye el 10,1 % de 2025 por la activación de bases negativas en EE. UU. (18,0 M€; extracto AR25 p. 142). Aquí lo corrige la configuración: N1 = 22,12 % en el NOPAT. La nota que el expediente heredado dejó abierta («≈3 % optimista») queda resuelta con hechos: −1,45 € en el precio de Sí.
5. **Deuda y acciones en la misma fecha.** El motor B resta 279,9 M€ del cierre de 2025 y divide por las acciones diluidas de 2025: coherente. Lo que el modelo no recoge es que en 2025 se recompraron 94,0 M€ (extracto AR25 p. 144) con la acción a una media de 59,47 € (p. 147), por encima de mi NORMAL: para quien se queda, eso resta valor.

Las 52 celdas cuentan una sola historia. No pido mover ninguna palanca.

## 2. Desviaciones pendientes

`gramatica.md` deja una sin justificar: **G8 en el BUENO** (salto de 9,1 puntos). No hay G16 (el terminal pesa el 59 % en el NORMAL) ni G17 (C24 vacía). Las tres G5 están justificadas en la fase B.

**G8 · BUENO · fundamentada.** En los años 1–10 cada euro nuevo rinde un 21,1 % (1,4 × 1,074 × 0,18 × (1 − 0,221)) porque se juntan dos cosas que solo ocurren una vez. Una: se llena capacidad ya pagada o en marcha al cierre de 2025 (colágeno en EE. UU., plásticos en México, extrusión en Serbia; extracto AR25 p. 65; el 37 % de la inversión de 2025 fue a capacidad, p. 143). Dos: el margen sube del 16,4 % al 18,0 % al repartir costes fijos. Es crecimiento por eficiencia y es finito (GV p. 32; I1). Cuando el margen llega al techo de 2020–2021 (G29, H29) y las plantas están llenas, el euro nuevo vuelve a pagar planta nueva a coste completo y rinde lo que rindió el capital en el peor año de la década: 12,1 % en 2019 (F33). En el año 11 no se pierde el foso: se acaban la capacidad ociosa ya pagada y el recorrido del margen. El 12 % sigue 3,7 puntos por encima de la tasa del motor (8,3 %). Tengo precedente propio en las dos direcciones: en 2019–2025, saliendo del mínimo de margen, el capital incremental rindió ≈18,9 %; en 2016–2025, ≈9,0 % [cálculo Historia]. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). No cambio la clase ni la cifra de D18. Lo contaré en la tesis.

## 3. ¿Hay que mover palancas?

No. Comprobé la aritmética de la fase B contra la Historia: pendiente del margen de 2016–2025 de −0,49 puntos por año (cinco años desde el 16,4 % dan el 13,9 %, B15 = 0,14); crecimiento medio de 2017–2025 sin 2022 del 4,18 %; CAGR de 2016–2021 del 5,8 %; mercado en valor +2,18 % anual en 2016–2025; S2C de 2,03 (2016–2021) y 0,89 (2021–2025). Todo cuadra. El S2C del NORMAL (1,1) es C53 = 1,146 redondeado a 0,1. No encuentro perímetro ni dato equivocado. La fase B no rebajó el S2C por la reposición porque ya la aplica la configuración: no hay doble cuenta. El único apoyo flojo es la frecuencia que cita B69 (punto 1.3): corregir la probabilidad movería el precio de Sí un 4,2 % sin cambiar zona ni cubo. En `celdas_corregidas` registro que revisé C62 y C18 de la fase A y B69 de la fase B, y que las mantengo.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** La etapa 1 dejó Vigilar con precio de Sí de 25,1 € y un C104 con un porcentaje. Revisé las g heredadas: la del MALO casi no mueve el valor (ROIC terminal = tasa) y la del NORMAL tiene argumento propio (mercado en valor +2,2 % anual; sustitución que se agota). Cambio: ninguno en palancas; en el turno 2 reescribo B101, B102 y C104, que llevan hechos de 2T26 y un porcentaje que D16 prohíbe.
2. **Anclaje en el precio o en la fuente externa.** Los valores no se acercan a 54,70 €: el NORMAL queda un 18 % por debajo (÷ precio). Las probabilidades se movieron hacia el MALO. No usé el valor de Simply Wall St (118,26 €, C38) ni el consenso. Cambio: ninguno.
3. **Consistencia y compromiso.** El cubo se decidió en la fase A, antes de los números. El precio descuenta un 9,6 % de crecimiento, más que mi BUENO, y ninguna de las doce variantes de la configuración sale de caro. No ajusté palancas para que saliera. Cambio: ninguno.
4. **Historia bonita / viento de cola atribuido a la empresa.** Del 4,5 % del NORMAL, unos 3 puntos son del nicho (mercado del 2–4 % en volumen, extracto AR25 p. 181; tripa animal de la mitad del mercado al 44 %, IA16 p. 42 e IA23 p. 146), un punto es precio que sigue al coste y medio punto es cuota. Cambio: la tesis dirá que el crecimiento es sobre todo del nicho.
5. **Optimismo del BUENO frente a la tasa base.** El BUENO pide un 7 % de crecimiento (la mejor racha dio un 5,8 %) y un 21,1 % por euro nuevo, más que el mejor ROIC de la década (16,7 %). Sus ventas del año 10 serían ≈32 % del mercado si este creciera un 3 % anual, frente a ≈24,5 % hoy. Plausible, en el borde, y menos probable que el MALO. Cambio: ninguno; lo llamo la historia menos probada.
6. **Doble castigo del mismo riesgo.** La deuda solo la resta el motor B: no está en la r, ni en la quiebra (0, con dos disparadores argumentados), ni en la probabilidad. El margen está como gravedad (14 %) y como frecuencia (0,25); la frecuencia citada en B69 no es la del MALO de este expediente, y lo medí (+4,2 % con 0,2). Una quiebra sobre un riesgo que ya está en el MALO sería contarlo dos veces (PA pp. 20–21; E6). Cambio: ninguno en celdas; anotado en B69.
7. **Disponibilidad (lo vívido del extracto).** Lo vívido son la «inflación sustancial» de las pieles y las coberturas superadas (extracto AR25 p. 436). Lo contrasté con la fila 29: la pendiente existe desde 2016 y 2024–2025 (16,7 % y 16,4 %) están por encima de 2023. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad (guía de la dirección como hecho).** No copié la guía de 2026: el NORMAL es un 4,5 %. Beat'30 no tiene cifras. Pero la cuota (30 % → 41 %) es una estimación de la empresa; C18 se sostiene igual con el ROIC de las cuentas (fila 33). «will frequently be a lie» (TCI p.60; HIM). Cambio: la tesis dirá que la cuota es estimación de la dirección.
9. **¿El MALO es de verdad malo?** Sí. Lleva el margen al 14 %, por debajo del mínimo de la década (15,1 %), con el ROIC terminal en la tasa: vale 30,69 €, menos que el valor sin crecimiento (35,21 €). No cubre perder cuota o volumen; por eso no es un suelo. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: la tesis inversa contará la pérdida de cuota.
10. **Lo no numerable que pesa y no está en las palancas.** El reparto por encima de la caja con deuda a corto, incluidas recompras de 94,0 M€ en 2025 a una media de 59,47 € (extracto AR25 pp. 144, 147); las «acusaciones en Danville» sin desenlace (p. 150); un competidor que no sé nombrar (p. 399). «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM). Cambio: van a la tesis inversa, a B222 y a C98 como evidencia.

## 5. Cubo y conclusión provisionales

En orden de mando. **Bloqueo:** no hay (0 errores de gramática; el estado técnico INCOMPLETO solo espera las predicciones del turno 2). **Límite del modelo:** no hay; el motor B calcula los tres escenarios y la configuración es válida. **Descalificadores:** ninguno aplica (fase A, sección 3). **Dato ausente material:** ninguno (punto 6). **Fundamento material:** la lista D10 está vacía (punto 7). **Zona:** caro. 54,70 € está por encima del ponderado (43,59 €). El precio de Sí es 39,29 € (P\*; el tope del NORMAL no actúa): el precio de Sí está un 28,2 % por debajo del precio (÷ precio), y el precio, un 39,2 % por encima del precio de Sí (÷ precio de Sí). La regla antigua de la hoja (C156) da 30,69 €.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`, con precio de Sí ≤ 39,29 €**, objetivo condicionado por la configuración (punto 9). «We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). La escalera es una convención experimental (k = 3) y la zona no mide el riesgo.

## 6. Datos ausentes (S-19)

Revisé los 22 datos de `datos_ausentes.json` uno a uno (detalle en el JSON). Ninguno es material para `esperar` con precio objetivo. Los que más se acercan:
- **Competidores, cuota desde 2022, desglose de volumen, precio y mezcla, y margen por segmento o región.** Afectan a por qué cayó el margen y a cuánto dura. Pero la escalera usa el margen consolidado y los tres escenarios cubren el 14–18 %, con el MALO por debajo del mínimo de la serie y un 0,25. Serían materiales para un `comprar` que dependiera del BUENO; no para esperar a 39,29 €.
- **Covenants, rating y calendario de renovación.** Afectan a C22 = 0. Con datos del cierre de 2025: 0,87 veces el EBITDA, EBIT 23 veces los intereses, 155,3 M€ de líneas libres (extracto AR25 p. 98) y sin impagos (p. 122). No uso lo que la empresa dice haber renovado tras el cierre.
- **Plan de capex de 2026.** Lo que fundaría θ es el desglose del capex de 2021–2024, no un plan futuro, y θ es una hipótesis sin fundamento suficiente (punto 9), no un dato ausente.
- **Danville y New Jersey sin contrastar.** El informe de 2023 dice que esas líneas arrancaron en 2023 (extracto IA23 p. 131); la capacidad del BUENO se apoya en los proyectos de 2025 (AR25 p. 65). No mueve ninguna celda.

## 7. Fundamento material (D10)

Recorrí B14:D16, B18:D18, B68:D69, C22, C23, C76, C44, C62, C8, C6 y B65:D66. Ninguna es de clase «sin juicio propio» ni «técnico» y todas las Observaciones citan hechos con celda de la Historia o página del extracto. Las seis narrativas tienen mecanismo y «qué lo pararía» con hechos de esta empresa (pieles, extracto AR25 p. 436; mezcla, p. 139; capacidad, p. 65; EE. UU., pp. 66, 140; sustitutos, p. 399). Miré con más cuidado las palancas que coinciden con su referencia (C15, B16, C16, D16, B18, D18): cada una tiene su propio hecho y un rango acotado por la Historia. B69 tiene un apoyo de frecuencia mal casado (punto 1.3), pero su mecanismo sí está en los hechos. C97 (técnico) y C56 (r heredada, S-3) no son hipótesis materiales de §B.6. **Lista vacía.**

La conclusión provisional no es favorable: `resultado = no_procede`, sin comprobación conjunta y con `sobrevive` en null. Los dos parámetros de la configuración sin fundamento suficiente (estructura y θ) no entran en esta lista con `esperar` (solo con `comprar`, 4.12): condicionan el objetivo por el protocolo del punto 9.

## 8. La hipótesis que más condiciona y qué la resolvería

La lista está vacía, así que la nombro por juicio y no por el tornado: **C15 y C18 del NORMAL: el margen deja de erosionarse en el 16,5 % y el capital nuevo rinde un 11 % a perpetuidad.** La década muestra un margen del 21,1 % al 16,4 % y una rentabilidad incremental de ≈9 % (≈7,4 % en 2021–2025). «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

**Qué la resolvería:** el desglose de la variación de ventas y de margen en volumen, precio, mezcla y coste de pieles por tecnología, que no se publica (extracto AR25 p. 139); se pide a Relación con Inversores. Y el margen EBIT consolidado del informe anual de 2026: si es de al menos el 16 % con las pieles caras, confirma el NORMAL; si baja del 15 %, lo desplaza hacia el MALO.

## 9. Configuración V6.4 (experimental, no adoptada)

Once parámetros activos (N2 vacío por elección de la configuración). Las doce variantes calculadas quedan en **caro** (precio de Sí 38,22–41,81 €, ponderado 42,52–46,26 €): `zona_igual_en_variantes_calculadas = true`, solo para esa tabla. Ningún parámetro es material para la acción.

| Parámetro | Efecto calculado en el precio de Sí | Fundamento suficiente | Material para el objetivo |
|---|---|---|---|
| N1.tipo (22,12 %) | −1,45 € aislado (−3,5 %) | sí: activación de 18,0 M€ en 2025 (extracto AR25 p. 142) | sí, pero fundado: no condiciona |
| N1.escudo | sin variante aislada; por mecanismo ≈0 | sí (convención) | no |
| N3.regla (R1) | 0,00: las ventas no caen en ningún escenario | no (sin año que la pruebe), pero inerte | no |
| N3.circulante (48,28 %) | 0,00 con R1 inerte | sí (balance de 2025) | no |
| PM1.estructura (SR1) | S −0,35 · SR2 +0,36 · H +1,07 · SRF +1,61 | no: P-M1 abierta | sí |
| PM1.familia (Θ) | ninguna variante cambia solo la familia | sí: exceso observado de 40,8 M€ | no |
| PM1.parametro (θ = 0,5) | θ = 0: +1,07 · θ = 1: −1,07 | no: punto medio sin central | sí |
| PM1.convencion_anios | −0,09 | sí (convención) | no |
| PM1.convencion_terminal | +0,20 | sí (convención) | no |
| PM1.roic_terminal | SR2 +0,36 | sí: B18:D18 ya son después de amortización | no |
| PM1.cartera (legado) | solo en heredado; ≈0,11 M€ al año | sí (inmaterial) | no |

Como juicio, sin umbral adoptado, llamo material para el objetivo a lo que lo mueve en torno a 1 € o más en sus variantes. N1 lo mueve, pero está fundado en hechos.

**Mantenimiento.** ¿Supera la reposición a la amortización? Con los hechos del cierre de 2025, no se ve. Los pagos por inmovilizado fueron 1,16 veces la amortización en la década, pero el exceso se concentra en 2016–2018 y 2021–2022, años de capacidad nueva (colágeno, celulósica en Danville; extracto IA21 p. 210, CA23 p. 98). En 2023–2025 quedaron en 0,90–0,94 veces. En 2025, de 84,1 M€, 30,9 M€ fueron capacidad y 53,2 M€ medio ambiente, mejoras y ordinarias (extracto AR25 p. 143): menos que la amortización de activos propios (≈79,7 M€). No hay hornos: son líneas de extrusión y conversión y la cogeneración, sin vida útil publicada. El traslado de Chequia sería reposición, pero se ejecuta después de la base. Lectura: θ en el extremo bajo, y SR1 como estructura más coherente con cómo están medidos C53 y la fila 33. `adoptada = false`.

**Avisos de dominio.** Solo el factor de reestimación (lectura sin umbral): f = 1,074 lleva el S2C efectivo a 0,97 / 1,18 / 1,50, dentro de los rangos de la fase B. Depende de θ, que ya condiciona el objetivo: no material por sí solo, lo digo en el diagnóstico.

**Objetivo (protocolo `objetivo_condicionado`, ensayo).** Esperar por precio, con dos condicionantes: PM1.estructura y PM1.parametro. La acción se sostiene en todo el ámbito calculado (las doce variantes, todas en caro). Tratamiento: `objetivo_condicionado`. En el turno 2 cerraré `concluido · Vigilar · esperar` con el precio de Sí de 39,29 € como objetivo condicionado a esas dos hipótesis. Información que falta: el desglose por año y destino del capex de 2021–2024 y la vida útil de las líneas frente a su amortización. «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 10. Turno 2 · comprobación conjunta

No existe `comprobacion_conjunta.json`: con conclusión `esperar` y lista D10 vacía no procedía. `sobrevive` queda en null y `resultado` en `no_procede`. El único rango del precio de Sí que informo es el de las doce variantes calculadas de la configuración (38,22–41,81 €, todas en caro): una tabla de sensibilidad, no un intervalo de confianza.

## 11. Conclusión

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 39,29 €** (precio de Sí de `precio.json`), **condicionado (provisional)** a PM1.estructura y PM1.parametro de la configuración V6.4 (tratamiento `objetivo_condicionado`, protocolo de ensayo). En orden de mando: no hay bloqueo, límite del modelo, descalificador, dato ausente material ni hipótesis de A o B sin fundamento. Manda la zona, `caro`: 54,70 € está por encima del ponderado (43,59 €) y del NORMAL (44,85 €). La escalera es convención experimental (k = 3). El precio del MALO (30,69 €) no es un suelo.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 39.29 · zona caro · precio de Sí ≤ 39.29 · precio esc. MALO 30.69 · ponderado 43.59 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional) a PM1.estructura y PM1.parametro de la configuración V6.4 · rango calculado del precio de Sí 38.22–41.81 en 12 variantes (tabla de sensibilidad, no intervalo de confianza)». La decisión de cartera es de José Luis.

El veredicto de la hoja (A6, «DESCARTADA POR FILTRO PABRAI») y mi cubo difieren por C13 = No: la hoja descarta lo que no es barato a ojo; yo vigilo un buen negocio que entiendo a un precio sin margen.

C93 = Sí. El g del NORMAL (2 %) se sostiene: el terminal reinvierte el 18 % del NOPAT a un ROIC del 11 %, el salto del año 11 es de 4,2 puntos y el terminal pesa el 59 %. C103 = No: el foso existe pero rinde cada vez menos (margen del 21,1 % al 16,4 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

## 12. Tesis (B101)

Viscofan fabrica envolturas para embutidos en 22 plantas para más de 1.700 clientes, ninguno por encima del 10 % de las ventas (extracto AR25 pp. 121, 137), y su ROIC no bajó del 12,1 % en diez años (Historia fila 33): es un buen negocio de nicho con un foso de escala y proceso. El foso rinde menos que antes: el margen EBIT pasó del 21,1 % al 16,4 % mientras la cuota que estima la propia empresa subía del 30 % al 41 % (extracto AR19 p. 121, CF22 p. 182), y el crecimiento es sobre todo del nicho (AR25 p. 181). Mi NORMAL vale 44,85 €, con el MALO en 30,69 € y el BUENO en 60,00 €; en el BUENO, el salto del año 11 (9,1 puntos) es mi hipótesis de que la capacidad ociosa ya pagada y el recorrido del margen se agotan y el capital nuevo vuelve a rendir el 12 % del peor año (F33). A 54,70 € el precio descuenta un 9,6 % de crecimiento anual de las ventas (C86), más que mi BUENO, y la empresa reparte por encima de su caja con deuda a corto (AR25 pp. 98, 144). Vigilar: esperar a 39,29 €, objetivo condicionado a la estructura del mantenimiento y a θ (38,22–41,81 € en las variantes calculadas).

## 13. Tesis inversa (B102)

Defiendo el No con hechos.

- **Costes que no controla.** El consumo de materias primas pasó de 370,5 a 411,6 M€ en 2025 con las ventas un 4,0 % arriba (extracto AR25 p. 23); las pieles europeas sufren «inflación sustancial» y las coberturas de dólar fueron superadas (p. 436).
- **Cuota pagada con precio.** La cuota sube, pero el margen cayó 4,7 puntos en diez años (Historia C29, L29) y en 2025 la mezcla fue inferior con volumen récord (p. 139).
- **El capital nuevo apenas rinde su coste.** 436 M€ de capital nuevo en 2016–2025 para unos 39 M€ de NOPAT: ≈9 %, frente a una tasa del motor del 8,3 %, y ≈7,4 % en 2021–2025 [cálculo Historia].
- **Reparte más caja de la que genera.** La caja libre al accionista no crece desde 2019 (Historia fila 35). Aun así pagó 145,1 M€ al accionista en 2025, 94,0 M€ en recompras con la acción a una media de 59,47 € (pp. 144, 147), y la deuda pasó de 116,8 a 304,1 M€, con 227,4 M€ de bancos a un año (p. 98).
- **Lo que no sé.** Quién es el competidor que gana y en qué quedó Danville (p. 150). Pet Mania perdió actividad por un arancel (p. 140).
- **El precio frente al MALO.** Si el margen sigue la pendiente hasta el 14 %, la hoja da 30,69 € (B78) y el mercado paga un 78 % más. Y ese MALO aún no recoge perder cuota.

## 14. Predicciones (dado el NORMAL)

1. Ventas de 2027 entre 1.330 y 1.450 M€ · 2028-03-31 · 0,65.
2. Margen EBIT de 2027 entre el 15,5 % y el 17,5 % · 2028-03-31 · 0,6.
3. Pagos por inmovilizado de 2027 de no más de 1,3 veces la amortización · 2028-03-31 · 0,65.

Las tres son sobre el negocio y se comprueban con el informe anual de 2027. Son la autopsia de este análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 15. B222, B223 y qué me haría cambiar de cubo

- **B222:** la hipótesis fundamentada de la que más depende el precio de Sí: el margen deja de erosionarse en el 16,5 % (C15) y el capital nuevo rinde un 11 % (C18). El objetivo queda además condicionado por la estructura del mantenimiento y θ (±1–1,6 €).
- **B223:** el desglose de volumen, precio, mezcla y coste de pieles por tecnología (Relación con Inversores) y el margen EBIT del informe anual de 2026 (≥ 16 % confirma el NORMAL; < 15 % lo desplaza al MALO); para θ, el desglose por año y destino de los pagos por inmovilizado de 2021–2024 (como el de 2025, extracto AR25 p. 143).
- **A Sí:** un precio de 39,29 € o menos con el NORMAL intacto, o un margen de al menos el 17,5 % dos años con cuota publicada al alza.
- **A No:** margen por debajo del 15 % dos años con ventas planas; deuda neta por encima de 2,5 veces el EBITDA para seguir pagando al accionista; o que Danville revele un problema de integridad.
- **A Demasiado difícil:** que la caída del margen venga de un sustituto tecnológico que no pueda juzgar (p. 399), o una compra grande fuera del nicho.

## 16. Comparación con la etapa 1

Coinciden el cubo (Vigilar) y la razón: precio sin margen. El precio de Sí sube de 25,1 € a 39,29 € por cuatro cambios:

- **Motor.** La etapa 1 valoró el FCF al accionista sin restar deuda; yo valoro con el motor B y resto 279,9 M€.
- **MALO.** El suyo era caja plana; el mío lleva el margen al 14 %, y vale 30,69 €.
- **Regla.** La suya era mín(MALO, 0,75 × ponderado), que en esta hoja daría 30,69 € (C156); la mía es la escalera k = 3.
- **Configuración V6.4.** Tipo sin activaciones fiscales y reposición con SR1 y θ = 0,5: −2,52 € frente a la V6.3 efectiva (41,81 €).

La etapa 1 acertó en que el precio descuenta más crecimiento del que la empresa ha dado. Se equivocó al usar como hechos datos de 2T26, posteriores a la base, y al poner un tamaño de posición, que no me corresponde.

## Cambios frente al expediente heredado

- Valores por escenario 35,39 / 47,56 / 63,33 € → 30,69 / 44,85 / 60,00 €; ponderado 46,88 → 43,59 €; precio de Sí 43,05 → 39,29 €. Motivo: B15 pasa de 0,15 a 0,14 en la fase B de este expediente (pendiente de −0,49 puntos por año, Historia fila 29): la variante «heredado» (V6.3 efectiva con estas palancas) da 41,81 €. El resto (−2,52 €) es la configuración: N1 (−1,45 €) y SR1 con θ = 0,5 (−1,07 €).
- Tipo impositivo: de nota abierta («≈3 % optimista») a corregido por N1 = 22,12 %. Motivo: activación de bases negativas de 18,0 M€ en 2025 (extracto AR25 p. 142).
- Salto del año 11: 2,8 / 3,6 / 8,2 → 2,5 / 4,2 / 9,1 puntos. Motivo: la hoja calcula ahora con f = 1,074 y t = 22,12 %, y el margen del MALO es del 14 %.
- DCF inverso: 8,2 % → 9,6 %; precio de Sí descontando 1,7 % → 0,9 %; cuánto pagas por crecer 1,7 → 2,0 veces. Motivo: valores más bajos con el mismo precio.
- Nueva incoherencia anotada en B69: la frecuencia que la apoya (años del 15,1–15,7 %) no es la del MALO del 14 % (0 de 10 años). Motivo: cambió el MALO, no la probabilidad; con 0,2 el precio de Sí subiría un 4,2 %, sin cambiar la zona.
- Datos ausentes: 21 → 22. Motivo: nueva entrada «Danville y New Jersey sin contrastar»; no es material (extracto IA23 p. 131; AR25 p. 65).
- Deuda: 1,13 veces (jun-2026) → 0,87 veces el EBITDA (dic-2025), y fuera la nota de covenants de 1S26. Motivo: lo posterior a la base no es base.
- Recompras: fuera el programa de hasta 150 M€ de 2026; entran las de 94,0 M€ de 2025 (extracto AR25 p. 144). Motivo: base al 31-dic-2025.
- ¿El MALO es malo?: ahora baja del mínimo de la serie (14 % frente a 15,1 %) y vale 30,69 €, menos que el valor sin crecimiento (35,21 €). Motivo: B15 de este expediente.
- Nuevo: evaluación de la configuración V6.4. El objetivo queda condicionado por PM1.estructura y PM1.parametro (tratamiento `objetivo_condicionado`). El expediente heredado no tenía configuración ni protocolo.
- Precio objetivo: 43,05 € → 39,29 €, ahora condicionado (provisional) a PM1.estructura y PM1.parametro; C104 lleva «fundamento no procede (conclusión no favorable)» en lugar de «fundamento lista vacía». Motivo: valores del punto anterior; protocolo `objetivo_condicionado` de la configuración, y la etiqueta la fija la tabla cerrada del Anexo D §D.6 (esperar · no_procede).
- Predicción 3 (capex ≤ 1,3 veces la amortización): probabilidad 0,7 → 0,65. Motivo: cuatro de diez años la pasaron (Historia filas capex y da) y los compromisos de 52,0 M€ incluyen Chequia (extracto AR25 p. 143).
- Apoyo de C39: el heredado decía «cinco de siete años» en la banda del 15,5–17,5 %; son tres (2022, 2024, 2025; Historia F29:L29). Motivo: recuento corregido; la probabilidad (0,6) se mantiene porque es dado el NORMAL.
- C104 y descalificadores: la deuda a 0,87 veces el EBITDA de dic-2025 (antes 1,13 veces, de jun-2026). Motivo: base al 31-dic-2025.
- Sin cambio: cubo Vigilar, conclusión `esperar`, lista D10 vacía, G8 en el BUENO con el mismo mecanismo, hipótesis que más condiciona (C15 y C18 del NORMAL) y qué la resolvería.
