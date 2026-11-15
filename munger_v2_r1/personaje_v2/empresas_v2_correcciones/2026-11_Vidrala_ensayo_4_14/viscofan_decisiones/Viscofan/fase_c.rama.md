# Viscofan, S.A. · fase C · turnos 1 y 2 · rama 4.14 · 2026-11-14 · motor B · V6.4.1 experimental

Base económica: 31-dic-2025. Precio: 54,70 € del 3-nov-2026. Lo posterior a la base no apoya ningún juicio. «Historia» es la hoja de diez años de `datos_v63.md` (C = 2016 … L = 2025), con los datos corregidos de la rama (`CORRECCIONES_ENTRADAS_4_14.md`). Reviso las fases A y B, que no cambian ninguna celda frente a la 4.13, como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Parto de mi fase C de la 4.13 (`fase_c.4_13.json`, `fase_c.4_13.md`): conservo lo que sigue valiendo con las cifras nuevas y cambio lo que invalidan (última sección).

## 1. Una sola historia

Lo que calcula la hoja: MALO 30,15 €, NORMAL 44,32 €, BUENO 58,69 €, ponderado 44,36 € (B78:D78, C83), frente a 54,70 €. El precio está por encima del NORMAL y del ponderado; solo el BUENO lo supera. Es la historia de la fase A: buen negocio de nicho con un foso estrecho, un margen que se ha estrechado y un precio sin margen (C13 = No, C20 = Riesgo real alto).

- **Peso del terminal:** 49 % / 58 % / 63 %. Ninguno pasa del 75 %: no hay G16.
- **Salto del año 11:** 1,7 / 4,7 / 8,3 puntos. La rentabilidad marginal de los años 1–10 (9,7 %, 15,7 % y 20,3 %, con f = 1,1136 y t = 22,12 %) baja al ROIC terminal (8 %, 11 %, 12 %). Solo el BUENO pasa de 5 puntos (G8, punto 2). Sin f los saltos serían 0,7 / 3,1 / 6,2: el BUENO pasa igual.
- **DCF inverso:** con el margen, el S2C y el terminal del NORMAL, 54,70 € descuentan un 9,8 % anual de crecimiento de ventas en los años 1–5 (C86). Es más que mi BUENO (7 %) y que la mejor racha de la década (5,8 % anual en 2016–2021 [cálculo, Historia ventas]). El precio de Sí descuenta un 2,0 %. Se paga por crecer 2,1 veces lo que vale el crecimiento del NORMAL (19,99 € frente a 9,62 €).
- **Tornado:** la palanca que más mueve el valor es la tasa de descuento (±1 punto: 10,04 €), la r heredada. Es información, no criterio: el valor depende sobre todo de la rentabilidad exigida. Después, el margen (±2 puntos: 6,43 €) y el ROIC terminal (±5 puntos: 5,70 €).
- **Semáforos:** margen por encima del Q3 del sector en los tres escenarios (G5, justificado); r del 9,0 % bajo la r mínima del 9,5 % (heredada, se informa); banderas D84–D86. Cuota implícita sin calcular (C24 vacía).
- **Veredicto de la hoja** (A6): «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: buen negocio sin valor claro al precio.
- **Estado:** INCOMPLETO solo por las tres predicciones (turno 2); evidencias INCOMPLETAS (datos 15 de 17, con dos no verificables: Historia C23:L23 y C26:L26; punto 6). Sin bloqueo del valor.
- **Bases parciales:** G7 usa el tipo y el S2C de la Historia sin f; las referencias mecánicas del S2C se anclan en Configuración V6.4!B155 (1,0675) sin f. No las presento como comprobación del modelo experimental.

Lo que no cuadra a primera vista, y cómo lo resuelvo:

1. **El capital nuevo del NORMAL rinde más que el de la década.** 15,7 % por euro nuevo en los años 1–10 (14,1 % sin f), frente a una rentabilidad incremental de ≈9,0 % en 2016–2025 y ≈7,4 % en 2021–2025, pero ≈18,9 % en 2019–2025, saliendo del mínimo de margen [cálculo, Historia ebit y capital_invertido, t = 22,12 %]. No es una palanca mal derivada. La incremental fue baja porque el margen de toda la base cayó del 21,1 % al 16,4 % y el circulante subió 106,1 y 90,6 M€ en 2022–2023 (J14 corregido sin la variación de provisiones; CF_2024.txt, PDF p. 9). El NORMAL dice que el margen deja de caer; si sigue cayendo, es el MALO. Es la hipótesis que más condiciona (punto 8).
2. **La configuración ensancha el salto del año 11.** SR1 multiplica por f el S2C de los años y no toca el ROIC del terminal: 1,0 / 1,6 / 2,1 puntos del salto son de f. Las justificaciones de G8 de la fase B usaban las bases heredadas; valen las cifras de la hoja.
3. **El apoyo de B69 está mal casado con la frecuencia.** Llama «márgenes de MALO» a 2019, 2022 y 2023 (15,1–15,7 %), que están dentro del rango del NORMAL de C69, y ningún año llegó al 14 % del MALO (0 de 10). La probabilidad se sostiene por el mecanismo (repercusión parcial en 2022 y 2023 [CF_2022 p. 93; IA_2023 p. 246]) y por no castigar dos veces un margen que ya está bajo el mínimo observado. No es una palanca mal derivada. Con la fórmula de la escalera sobre los mismos V: 0,25 / 0,6 / 0,15 da 38,67 € (−4,0 %); 0,3 / 0,5 / 0,2, 38,15 € (−5,3 %); 0,15 / 0,6 / 0,25, 42,18 €. La zona no cambia con ningún vector (tope del NORMAL, 44,32 €). No pido revisarla; para el objetivo es un límite (punto 9, D7).
4. **El FCF del NORMAL crece un 6,2 % anual y C25 = No.** Mecánica: el crecimiento baja del 4,5 % al 2 % y con él la reinversión. Además es el flujo de la empresa, no el del accionista de la fila 35.
5. **El MALO vale menos que el valor sin crecimiento** (30,15 € frente a 34,71 €). Coherente: el margen baja al 14 % y el ROIC terminal (0,08) queda 0,26 puntos bajo la tasa del motor (8,26 %) por el redondeo. Efecto pequeño (g = 1 %).
6. **Celdas de la fase C en el libro** (B101, B102, C104): son las de la etapa 1, con un precio de Sí de 25,1 € y un «0 %». Se reescriben en el turno 2.
7. **Recompras por encima de mi valor.** 94,0 M€ en 2025 (extracto: AR_2025 p. 144), con un precio medio diario de 59,47 € (p. 147); 94,0 M€ ÷ 1.599.709 acciones compradas (AR_2025.txt, PDF p. 143) da ≈58,8 € [inferencia, si cubren las mismas compras]. Las dos cifras superan mi NORMAL. Absorben sobre todo el dividendo en acciones (nota de C28): C98 se queda en el borde, pero va a lo no numerable.
8. **Acciones (D3, decisión pendiente).** N = 45,479209 M es la media «diluida» publicada, que contradice su definición. Con la circulación a 31-dic-2025 el precio de Sí sería 39,85 € (−0,31 €, −0,77 %) con los datos de la rama, y 39,71 € (−0,449 €) sobre la activa de la 4.13 (`resultados/efecto_correcciones_viscofan.md` del ensayo 4.14); siempre en caro. No la adopto y no cambia mi conclusión: el precio está un 35,7 % por encima del precio de Sí (÷ precio de Sí).
9. **Tipo impositivo.** C52 (19,83 %) incluye el 10,1 % de 2025 por la activación de bases de EE. UU. (extracto: AR_2025 p. 142); la configuración usa 22,12 %.
10. **Datos corregidos de la rama.** Con A y B sin cambios, el precio de Sí pasa de 40,16401 a 40,30282 € (+0,13881 €): +0,13437 € por las pensiones netas (solo L25 entra en el puente: 14,878 M€ en lugar de 20,989 [AR_2025.txt, PDF pp. 87–88]) y +0,00444 € por el circulante. El puente baja de 279,9 a 273,8 M€. Cambian cifras, no el relato.

Las 52 celdas cuentan una sola historia. No pido mover ninguna palanca.

## 2. Desviaciones pendientes

`gramatica.md`: G8 en el BUENO (8,3 puntos) y las tres G5, ya justificadas en la fase B y que repito con sus hechos. No hay G16 (58 % de terminal en el NORMAL) ni G17 (C24 vacía).

**G8 · BUENO · fundamentada.** En los años 1–10 cada euro nuevo rinde un 20,3 % (1,3 × 1,1136 × 0,18 × (1 − 0,2212)) porque se juntan dos cosas que pasan una vez. Una: se llena capacidad construida o comprometida al cierre de 2025 (colágeno en EE. UU., plásticos en México, extrusión en Serbia; el 37 % de la inversión de 2025 fue a capacidad y quedan 52,0 M€ de compromisos; extracto: AR_2025 pp. 65, 143). Dos: el margen sube del 16,4 % al 18 % de 2020–2021 al repartir costes fijos, crecimiento por eficiencia, que es finito (GV p. 32; I1). Con las plantas llenas y el margen en su techo, el euro nuevo vuelve a pagar planta a coste completo: 12 %, el ROIC del peor año de la década (12,1 % en 2019, F33). En el año 11 no se pierde el foso (12 % sigue 3,7 puntos sobre la tasa del motor): se acaban la capacidad ya pagada y el recorrido del margen. Precedente propio en los dos sentidos: S2C de 1,57 en el ciclo de construir y llenar de 2016–2021 (era 1,70 antes de corregir el circulante de 2019–2020), y ≈18,9 % de rentabilidad incremental en 2019–2025 frente a ≈9,0 % en la década. Sin f el salto sería 6,2 puntos. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Lo contaré en la tesis; no cambio D18.

## 3. ¿Hay que mover palancas?

No. Comprobé la aritmética de la fase B contra la Historia corregida: C45 = 1,39 % → B14 = 0,015; media del margen 2019–2025 = 16,44 % → C15 = 0,165; pendiente del margen de −0,5 puntos al año, que en cinco años desde el 16,4 % da ≈13,9 % → B15 = 0,14; CAGR de 2016–2021 del 5,8 %; S2C de 0,86 (2016–2019), 0,98 (2021–2025), 1,57 (2016–2021) y 1,18 (década); B155 = 1,0675 × 0,75 / 1 / 1,25 → 0,8 / 1,1 / 1,3. Todo cuadra; no hay perímetro ni dato equivocado. Registro en `celdas_corregidas` que revisé C62, C97 y C98 (fase A) y B69 y C15 (fase B), sin cambios. La duda de la fase A que no reescribo es un dato, no una palanca: el divisor de acciones (C55), que es la decisión pendiente D3.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** La etapa 1 dejó un precio de Sí de 25,1 € y un «0 %», que el libro aún muestra en B101, B102 y C104. Las celdas que heredan algo tienen motivo propio (C97 y C62 cambian con hechos; las g, con AR_2025 p. 181 e IA_2016 p. 42). También miré el anclaje en mi fase C de la 4.13. Cambio: ninguno en celdas; reescribo B101, B102 y C104 en el turno 2.
2. **Anclaje en el precio o en la fuente externa.** El NORMAL queda un 19,0 % bajo el precio (÷ precio). No usé Simply Wall St (118,26 €) ni el consenso (69,29 €). «Few psychological tendencies do more damage to correct thinking» (PCA p.579; HIM). Cambio: ninguno.
3. **Consistencia y compromiso.** Busqué qué rompería Vigilar: ningún vector de probabilidades (tope del NORMAL), ninguna de las dieciocho variantes (38,61–43,52 €, todas en caro). El paso a No depende de si la compresión del margen es estructural, y eso no lo sé. Con la 4.13, corregí lo que ya no vale en vez de defenderlo. Cambio: ninguno en celdas.
4. **Historia bonita / viento de cola atribuido a la empresa.** Del 4,5 % del NORMAL, unos 3 puntos son del nicho, 1–1,5 de precio y lo que reste de cuota. Cambio: la tesis lo dirá.
5. **Optimismo del BUENO frente a la tasa base.** 7 % anual (la mejor racha dio 5,8 %) y 20,3 % por euro nuevo (el mejor ROIC de la década fue 16,7 %); ≈32 % del mercado en valor en el año 10 si este crece un 3 % [cálculo]. Plausible, en el borde. Cambio: ninguno.
6. **Doble castigo del mismo riesgo.** La deuda solo la resta el motor B (puente de 273,8 M€); el margen está como gravedad, no además como frecuencia; la reposición puede contarse en parte dos veces en el terminal con SR1 (SR2: +0,58 €) (PA pp. 20–21; E6). En el objetivo no cuento dos veces la alternativa SR2 (punto 9). Cambio: anotado en el punto 9.
7. **Disponibilidad (lo vívido del extracto).** La «inflación sustancial» de las pieles (AR_2025 p. 436) frente a la fila 29: la pendiente existe desde 2016 y 2024–2025 están por encima de 2023. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad (guía de la dirección como hecho).** Ninguna palanca copia la guía de 2026; θ = 0,5 no es una medida, y la clasificación de la inversión por tipo que publica la empresa es evidencia, no una medición de la reposición. «will frequently be a lie» (TCI p.60; HIM). Cambio: θ condiciona el objetivo.
9. **¿El MALO es de verdad malo?** En margen sí (14 %, bajo el mínimo de la década; vale 30,15 €). No recoge perder cuota frente a un competidor que no sé nombrar. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: la tesis inversa lo contará.
10. **Lo no numerable que pesa y no está en las palancas.** Reparto por encima de la caja con deuda a un año, recompras a ≈59 €, un «extraordinario» repetido tres años, Danville, un competidor sin nombre, una cifra de acciones contradictoria y, a favor, compras de directivos. «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM). Cambio: tesis inversa, B222 y C98 en el borde.

## 5. Cubo y conclusión provisionales

En orden de mando. **Bloqueo:** no hay (0 errores; el estado INCOMPLETO solo espera las predicciones). **Límite del modelo:** no hay. **Descalificadores:** ninguno (fase A, sección 3). **Dato ausente material:** ninguno (punto 6). **Fundamento material:** lista D10 vacía (punto 7). **Zona:** caro. 54,70 € está por encima del ponderado (44,36 €). Precio de Sí 40,30 € (P\*; el tope del NORMAL no actúa): el precio de Sí está un 26,3 % por debajo del precio (÷ precio) y el precio un 35,7 % por encima del precio de Sí (÷ precio de Sí). Regla antigua (C156): 30,15 €.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`, con precio de Sí ≤ 40,30 €**, objetivo condicionado por la configuración (punto 9). «We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). La escalera es una convención experimental (k = 3). Ni las acciones ni el perímetro cambian la conclusión.

## 6. Datos ausentes (S-19)

Revisé los 27 uno a uno (JSON). Ninguno es material para `esperar` con precio objetivo. Los cinco nuevos de la rama: los ceros de 2016–2018 del pasivo por arrendamientos (antes de la NIIF 16, con los arrendamientos NIC 17 ya en la deuda), del principal de arrendamientos y de la SBC (solo el motor A, que usa 2023–2025), y los minoritarios de 2019–2022 (sin línea en el balance de 2021 y 2022: CF_2021.txt, PDF p. 3; CF_2022_compilacion.txt, PDF p. 20). El puente usa los saldos de 2025 (L23 = 12,243 y L26 = 5,422 M€), documentados. Dejan las evidencias en «INCOMPLETAS», que se informa. Los que más se acercan a ser materiales siguen siendo los de la 4.13: los competidores y la descomposición de volumen, precio y mezcla (serían materiales para un `comprar` que dependiera del BUENO o de excluir un MALO de pérdida de cuota); los covenants, el rating y la renovación de la deuda (C22 = 0 se sostiene con 0,87x EBITDA, 155,3 M€ de líneas libres y sin impagos, AR_2025 pp. 98, 122). Las operaciones de directivos no son un dato ausente: la evidencia de fase 1 las tiene (Control maestro fila 76). El plan de capex de 2026 no fundaría θ: lo que lo acota es el desglose histórico por tipo, que está en el paquete para 2021, 2022, 2023 y 2025, y θ es una hipótesis sin fundamento suficiente, no un dato ausente.

## 7. Fundamento material (D10)

Recorrí B14:D16, B18:D18, B68:D69, C22, C23, C24, C76, C44, C62, C6, C8 y B65:D66 con las Observaciones que la fase B actualizó a la Historia corregida (B155 = 1,07; tramos del S2C 0,86, 0,98, 1,57 y 1,18). Ninguna es «sin juicio propio» ni «técnico»; todas citan hechos con celda o página. Las seis narrativas tienen mecanismo y «qué lo pararía» con hechos propios (extracto: AR_2025 pp. 436, 139, 65, 66, 140, 399). B69 tiene un apoyo de frecuencia mal casado (punto 1.3), pero su mecanismo está en los hechos. **Lista vacía.** Conclusión no favorable: `resultado = no_procede`, sin comprobación conjunta, `sobrevive` en null. Los parámetros de la configuración sin fundamento suficiente condicionan el objetivo por el protocolo (punto 9), no por esta lista.

## 8. La hipótesis que más condiciona y qué la resolvería

Por juicio, no por el tornado: **Palancas!C15, el margen del NORMAL deja de comprimirse en el 16,5 %.** La década muestra 21,1 % → 16,4 %; los siete últimos años, 15,1–18,0 % sin tendencia. Si la compresión es estructural, el NORMAL es el MALO y el cubo es No. «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

**Qué la resolvería:** la descomposición de la variación de ventas y de margen en volumen, precio y mezcla y coste de pieles, por tecnología y región, que no se publica (extracto: AR_2025 p. 139), pedida a Relación con Inversores; y el margen EBIT de 2026 y 2027 frente a la inflación de pieles.

## 9. Configuración V6.4.1 (experimental, no adoptada)

Dieciocho variantes calculadas, todas en caro: precio de Sí de 38,61 € (θ = 1) a 43,52 € (heredado).

**Dos juicios separados.** Para la **acción**, ninguna variante calculada cambia la zona: ningún parámetro es material para la acción. Para el **objetivo** (contrato 4.14), juzgo cada parámetro con su contraste mecánico (`contraste_objetivo_v64.md`, copiado tal cual en el JSON), lo que ese contraste no cubre y un criterio declarado.

**Criterio (juicio propio, no política).** Llamo material para el objetivo a un desplazamiento atribuible del precio de Sí de 1 € o más (≈2,5 % de 40,30 €). No hay ninguna política de materialidad adoptada (D1 pendiente). La razón sale de este expediente: un solo paso de la lista de probabilidades (0,05 entre las colas) mueve el precio de Sí −1,63 € o +1,88 € [cálculo exacto con `precio_de_si.py` sobre los V de `precio.json`], y en esa palanca ya discreparon dos agentes de este mismo expediente (DECISIONES_PENDIENTES_4_14.md §2.7). Por debajo de 1 € el número es más preciso de lo que sé. «Better roughly right than precisely wrong» (PCA p.451; HIM). Cuando un parámetro sin fundamento suficiente mueve el precio de Sí y lo juzgo no material, digo con qué lo comparo.

| Parámetro | Contraste atribuible (Δ precio de Sí) | Fundamento | Objetivo: material · base | ¿Condiciona? |
|---|---|---|---|---|
| N1.tipo | activa_sin_N1 +1,53 € | sí | sí · juicio | no (fundado) |
| N1.escudo | escudo_alternativo −0,06 € | sí | no · juicio | no |
| N3.regla | solo_N1 y activa_R0_sin_PM1 +1,69 € | no | no · juicio, comparado con activa_sin_PM1 (+1,69 €: todo es de P-M1) | no |
| N3.circulante | ninguno (solo conjuntas) | sí | no · juicio | no |
| PM1.estructura | H +1,69 · S −0,63 · SRF +1,93 · SR2 +0,58 € | no | sí · juicio | **sí** |
| PM1.familia | ninguno: Λ sin calcular | no | no determinada | **sí** |
| PM1.parametro | θ = 0 +1,69 · θ = 1 −1,69 € | no | sí · juicio | **sí** |
| PM1.convencion_anios | −0,17 € | no | no · juicio, comparado con un paso de probabilidades (1,63 €) | no |
| PM1.convencion_terminal | +0,38 € | sí | no · juicio | no |
| PM1.roic_terminal | estructura_SR2 +0,58 € | no | no · juicio, comparado con PM1.estructura (2,56 €, que ya condiciona) | no |
| PM1.cartera | ninguno (solo heredado) | sí | no · juicio (≈0,03 €) | no |
| PM1.perimetro | «Caja» +0,66 € (1,32 € con θ = 1) | sí | no · juicio | no |

Lo que cambia la lectura de cada uno:

- **N1.tipo** (conjunta necesaria con su escudo): +1,53 €. Material para el objetivo y fundado (conciliaciones del impuesto; activación de 18,0 M€ en 2025, extracto: AR_2025 p. 142): no condiciona.
- **N3.regla:** el +1,69 € es de quitar P-M1. R0 y R1 sin P-M1 dan lo mismo al céntimo (41,9960 €), porque con ventas que no caen en ningún escenario R1 no actúa. Sin fundamento (en 2024 el circulante subió 8,9 M€ con las ventas a la baja, Historia K14 corregido), pero su parte propia del contraste es 0,00 €. Límite: R0 con P-M1 no está especificado.
- **PM1.estructura:** S 39,67 · SR1 40,30 · SR2 40,88 · H 42,00 · SRF 42,24 €. Material y sin fundamento: **condiciona**.
- **PM1.familia:** ninguna variante calcula Λ; λ no se observa. Inmaterial para la acción (haría falta subir el precio de Sí 14,40 €, unas ocho veces y media el efecto entero de P-M1); objetivo **no determinado**: condiciona y no está cubierta por el ámbito.
- **PM1.parametro:** θ = 0 42,00 € · θ = 1 38,61 €. Material y sin fundamento: **condiciona**. Evidencia nueva frente a la 4.13: la empresa publica el desglose de su inversión por tipo y el paquete lo tiene para 2021 (IA_2021_es.txt, PDF p. 213), 2022 (CF_2022_compilacion.txt, PDF p. 202), 2023 (IA_2023_es.txt, PDF p. 250) y 2025 (AR_2025.txt, PDF p. 143). En los cuatro años, lo que no es capacidad queda por debajo de la D&A (55,3 / 70,3 / 70,3 / 54,8 M€ frente a 72,3 / 78,1 / 83,7 / 85,2 M€ [cálculo]): apunta a θ bajo, es decir, a un objetivo por encima del activo. No lo fundamenta: «capacidad y maquinaria» puede incluir maquinaria de reposición (solo 2025 dice «aimed at increasing capacity»), la D&A es a coste histórico, 2024 no está en un documento conservado, y aceptar el método es una decisión pendiente (D2, D5).
- **PM1.convencion_anios:** −0,17 €. Confianza baja frente a la media de la configuración (la razón de «Plana» no aplica sin ventas a la baja; la D&A fue el 6,8 % de las ventas en 2016 y en 2025). Sin fundamento, pero una décima parte de un paso de probabilidades y dependiente de θ: no material.
- **PM1.convencion_terminal:** +0,38 €. Fundada en el estado estable (CV p. 13; I2). No material.
- **PM1.roic_terminal:** +0,58 €. Confianza baja frente a la media: B18:D18 se anclaron en ROIC sobre todo el capital (Historia fila 33), la lectura en la que Q-ROIC1 pide SR2. Su único contraste es la variante estructura_SR2, que es una de las estructuras de PM1.estructura, ya condicionante: nombrarlo aparte contaría dos veces la misma alternativa. No material.
- **PM1.perimetro:** «Caja» +0,66 €. NIIF 16 es el coherente con el motor B, y la propia empresa define su CapEx con los derechos de uso (AR_2025.txt, PDF p. 275). Fundado; su efecto solo existe a través de θ. La elección formal es humana (D4).

**Mantenimiento.** La reposición no supera de forma visible a la amortización: el exceso de la década está en los años de capacidad nueva; en 2024, sin crecimiento, la inversión quedó por debajo; en los cuatro años con desglose, lo que no fue capacidad quedó bajo la D&A. No hay hornos. Chequia es reposición pura, pero posterior a la base. Estructuras: S cuenta dos veces el exceso que ya está en el S2C; SRF quita ≈0,17 € por euro de crecimiento, el doble del exceso histórico por euro (≈0,096), porque aplica la proporción de reposición a un fijo futuro 1,8 veces el histórico; SR1 quita ≈0,093 €; por Q-ROIC1, SR2 es más coherente que SR1; H no queda excluida. El desglose por tipo no separa H de SR2: `estructura_mas_coherente = null`, nada adoptado.

**Avisos de dominio.** Solo el factor de reestimación (lectura): f = 1,1136 en la activa y de 1,0000 a 1,2562 en las variantes. En el extremo θ = 1 el NORMAL rendiría un 17,8 % por euro nuevo, el doble de la incremental de la década: lo digo, pero su incertidumbre es la de θ y no lo cuento dos veces. No es material.

**Objetivo.** Protocolo `objetivo_condicionado` (el que declara la configuración; ensayo, no adopción). Condicionan PM1.estructura, PM1.familia y PM1.parametro; ninguno es material para la acción y las dieciocho variantes quedan en caro: la acción se sostiene en el ámbito y el precio de Sí (40,30 €) se emite en el turno 2 como objetivo condicionado. El rango (38,61–43,52 €) es una tabla de sensibilidad, no un intervalo de confianza, y no cubre la familia Λ.

**Límites del objetivo que vienen de decisiones pendientes** (no las adopto; las nombro porque mueven el objetivo o su uso):

- **D7 · probabilidades.** Un paso de la lista mueve el precio de Sí −1,63 / +1,88 €, por encima de mi criterio, y ninguna variante lo contrasta. B69 tiene fundamento (punto 1.3), así que no entra en D10, pero el objetivo no es más preciso que eso.
- **D3 · acciones.** −0,31 € con la circulación a 31-dic-2025 y los datos de la rama (39,85 €); −0,449 € sobre la activa de la 4.13. Por debajo de mi criterio, pero el divisor actual descansa en una cifra que su propia fuente contradice.
- **D4 · perímetro** (+0,66 € con «Caja») y **D5 · N1 y θ** (θ ya condiciona).
- **D2 · delimitación de P-M1 y protocolo.** Si la persona responsable decide que la incertidumbre de P-M1 no está delimitada, el objetivo se bloquearía (abstención), aunque la acción «no comprar a 54,70 €» se sostiene en todo el rango calculado.
- **D1 · política de materialidad:** no existe; mi criterio de 1 € es juicio propio.
- **D8 · uso.** La recomendación pendiente es mantener la entrega como experimental y supervisada, no apta para dinero real mientras sigan abiertas D1 y D2. Quien decida con dinero real debe saberlo: este objetivo es condicional y experimental.

## Cambios frente a la 4.13

Base: `fase_c.4_13.json` y `fase_c.4_13.md` (copias exactas de la fase C cerrada de la 4.13). Las fases A y B no cambian ninguna celda; cambian los datos (`CORRECCIONES_ENTRADAS_4_14.md`), las variantes y el contraste (`configuracion_v64_variantes.md`, `contraste_objetivo_v64.md`) y el contrato del juicio sobre el objetivo (4.14). Los juicios de la 4.13 que siguen valiendo se conservan: cubo Vigilar, `esperar`, lista D10 vacía, hipótesis que más condiciona (C15), ningún dato ausente material, las mismas tres hipótesis que condicionan el objetivo, protocolo `objetivo_condicionado`, clases, confianzas y contradicciones revisadas.

**Cambia por los datos corregidos (efecto mecánico, no juicio):**

1. Valores: MALO 30,02 → 30,15; NORMAL 44,18 → 44,32; BUENO 58,55 → 58,69; ponderado 44,22 → 44,36; precio de Sí 40,16 → 40,30 €; valor sin crecimiento 34,57 → 34,71 €; puente 279,9 → 273,8 M€. Causa: pensiones netas en L25 (resultados/efecto_correcciones_viscofan.md, reproducido al céntimo: 40,30282).
2. Distancias: el precio pasa de un 36,2 % a un 35,7 % por encima del precio de Sí (÷ precio de Sí) y de un 23,7 % a un 23,3 % por encima del ponderado; el precio de Sí, de un 26,6 % a un 26,3 % por debajo del precio (÷ precio).
3. Rango de las variantes: 38,47–43,39 → 38,61–43,52 €; estructuras S 39,54 → 39,67, SR2 40,74 → 40,88, H 41,86 → 42,00, SRF 42,10 → 42,24 €; θ = 0 41,86 → 42,00 y θ = 1 38,47 → 38,61 €; «Caja» 40,83 → 40,96 €. Los Δ frente a la activa apenas cambian (por ejemplo, N1.tipo +1,53 y SR2 +0,58 €).
4. f 1,1127 → 1,1136 (D_hist 320,6 → 318,3 M€ por el circulante corregido); rango de f 1,0000–1,2539 → 1,0000–1,2562; rentabilidad marginal del NORMAL en θ = 1, 17,7 % → 17,8 %; SR1 quita ≈0,093 € por euro de crecimiento (≈0,092); fijo del 25,5 % de la reinversión (25,3 %).
5. Circulante de 2023 106,1 y 83,0 → 106,1 y 90,6 M€; circulante de 2024 +15,5 → +8,9 M€ (N3.regla); S2C de 2016–2021 1,70 → 1,57 (G8) y tramos de la fase B 0,86 / 0,98 / 1,18.
6. Vectores de probabilidades: 38,54 → 38,67 € (0,25/0,6/0,15) y 38,01 → 38,15 € (0,3/0,5/0,2); tope del NORMAL 44,18 → 44,32 €.
7. Acciones (D3): la cifra nueva es −0,31 € con los datos de la rama (−0,449 € sobre la activa de la 4.13); la 4.13 daba un intervalo de 39,66 a 40,05 € sobre su activa.
8. Datos ausentes: 22 → 27; los cinco nuevos (Historia C17:L17, C18:L18, C23:L23, C26:L26 y minoritarios de 2021–2022) no son materiales (punto 6).

**Cambia porque la 4.13 decía algo que no era exacto:**

9. La 4.13 decía que del desglose de la inversión por destino «solo consta 2025». El paquete tiene también 2021, 2022 y 2023 (IA_2021_es.txt, PDF p. 213; CF_2022_compilacion.txt, PDF p. 202; IA_2023_es.txt, PDF p. 250; comprobado en `texto/`). Cambian la información que falta de PM1.estructura y PM1.parametro, la revisión del plan de capex, el mantenimiento y la información no disponible del objetivo. θ sigue sin fundamento suficiente, pero la evidencia apunta a θ bajo.

**Cambia por el contrato 4.14 (nuevo y obligatorio):**

10. Cada parámetro lleva `juicio_objetivo`, separado del juicio sobre la acción, con el contraste copiado, límites, base, criterio, comparación y razonamiento propios.
11. El criterio de la 4.13 («del orden de 1 €») se declara como **juicio propio del agente** con su razón (`juicio_propio_del_agente`), no como umbral. Por eso N1.tipo, PM1.estructura y PM1.parametro pasan de base «calculada» a «juicio_economico» en el objetivo (lo material lo decide mi criterio, no el cálculo). Ningún parámetro cambia de lado.
12. Los tres parámetros sin fundamento suficiente que juzgo no materiales y cuyo contraste mueve el precio de Sí llevan su comparación: N3.regla con activa_sin_PM1 (+1,69 €: toda la diferencia es de P-M1), PM1.convencion_anios con un paso de probabilidades (1,63 €) y PM1.roic_terminal con PM1.estructura (2,56 €, que ya condiciona). La 4.13 los excluía con una inferencia sin comparación.
13. Se añaden los límites del objetivo que vienen de decisiones pendientes (D7, D3, D4, D5, D2, D1, D8), que la 4.13 no nombraba como tales (salvo acciones y perímetro).

## 10. Turno 2 · comprobación conjunta y conclusión

El turno 2 cierra la decisión del turno 1 y no reabre sus juicios: `configuracion_v64` (con el `juicio_objetivo` de cada parámetro), la lista D10, los datos ausentes y las celdas revisadas quedan como los dejó el turno 1 (copia exacta en `fase_c.turno1.json`).

**Comprobación conjunta:** no se ejecutó (no existe `comprobacion_conjunta.json`; la conclusión provisional no es favorable). `sobrevive = null`, `resultado = no_procede`.

**Estado: `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 40,30 € (condicionado, provisional).** Es lo que corresponde al tratamiento `objetivo_condicionado` del protocolo de `configuracion_economica.json`: lo condicionan PM1.estructura, PM1.familia y PM1.parametro, ninguno material para la acción, y las dieciocho variantes calculadas quedan en caro (precio de Sí de 38,61 a 43,52 €). Ese rango es una tabla de sensibilidad de las variantes calculadas: no es un intervalo de confianza ni una robustez frente a hipótesis no exploradas, y no cubre la familia Λ. Sin datos ausentes materiales, sin descalificadores y con la lista D10 vacía. «We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). No escribo ningún tamaño de posición (D16): es de José Luis.

**Para quien decida con dinero real:** el objetivo es experimental y condicional. Lo limitan, además, decisiones pendientes que no adopto: D7 (un paso de la lista de probabilidades mueve el precio de Sí −1,63 / +1,88 €), D3 (39,85 € con las acciones en circulación a 31-dic-2025), D4 (+0,66 € con «Caja»), D2 (si P-M1 no se acepta como delimitada, el objetivo se bloquearía) y D8 (la recomendación pendiente es no usar esta entrega para dinero real mientras D1 y D2 sigan abiertas).

**C104:** Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 40.30 · zona caro · precio de Sí ≤ 40.30 · precio esc. MALO 30.15 · ponderado 44.36 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional): lo condicionan la estructura del mantenimiento, θ y la familia de P-M1 de la configuración experimental (la familia, sin calcular); rango del precio de Sí en las variantes calculadas 38.61 a 43.52, dieciocho variantes, todas en caro

**C93 = Sí.** El g del NORMAL (2 %) con un ROIC terminal del 11 % reinvierte el 18 % del NOPAT (CV p. 13; I2); el salto del año 11 del NORMAL es de 4,7 puntos y el terminal pesa el 58 %. **C103 = No:** ROIC del 12,1 % al 16,7 % con un margen que se estrecha; no es un negocio que se tiene sin mirar el precio.

## 11. Tesis (B101)

Viscofan es el mayor fabricante de envolturas para embutidos y el único con todas las tecnologías (extracto: AR_2025 p. 180), con un ROIC de entre el 12,1 % y el 16,7 % en diez años (Historia fila 33) y una cuota que subió del 30 % al 41 % entre los productores de envoltura a medida en 2015-2022 (AR_2019 p. 121; CF_2022 p. 182). Es un buen negocio, no uno extraordinario: las ventas crecieron un 71 % en la década, pero el margen EBIT bajó del 21,1 % al 16,4 % (fila 29), el capital nuevo rindió en torno a un 9 % y el FCF al accionista de 2025 (93,8 M€) quedó por debajo del de 2019 (108,5 M€; fila 35), mientras la deuda sube para repartir más de lo que genera (AR_2025 p. 144). Con mis tres escenarios (30,15 / 44,32 / 58,69 €) el precio de 54,70 € está por encima del NORMAL y del ponderado (44,36 €) y descuenta un crecimiento de ventas del 9,8 % anual, más que mi BUENO (C86). Vigilar: espero a un precio de Sí de 40,30 €, objetivo condicionado por las hipótesis de mantenimiento de la configuración experimental (de 38,61 a 43,52 € en las dieciocho variantes calculadas, todas en caro). La frontera con No es una sola: si la compresión del margen es estructural.

## 12. Tesis inversa (B102)

Defiendo el No. Viscofan transforma pieles bovinas, celulosa y gas en un insumo industrial y no ha sabido trasladar sus costes: el margen EBIT cayó del 21,1 % de 2016 al 15,1 % de 2023 (Historia fila 29), las subidas de precio solo compensaron en parte en 2022 y 2023 (extracto: CF_2022 p. 93; IA_2023 p. 246) y en 2025 la mezcla de precios bajó con volumen récord (AR_2025 p. 139): la cuota se puede estar pagando con precio, frente a competidores que ni siquiera sé nombrar (AR_2025 p. 399). En diez años el capital invertido creció 436 M€ y el beneficio operativo después de impuestos 39 M€, un 9 % sobre el capital nuevo, tan cerca de la r que crecer apenas crea valor, y el FCF al accionista de 2025 (93,8 M€) es menor que el de 2019 (108,5 M€; Historia filas 32 y 35). Mientras, reparte más de lo que genera: 145,1 M€ en 2025 frente a 93,8 M€ de FCF, con un dividendo «extraordinario» repetido tres años y recompras de 94,0 M€ en un año con una cotización media de 59,47 € (AR_2025 pp. 144, 147), por encima de lo que creo que vale; la deuda financiera pasó de 116,8 a 304,1 M€ en 2021-2025 (fila 22), con 227,4 M€ de deuda bancaria a un año (AR_2025 p. 98). La inversión en EE. UU. dio resultados negativos durante años (AR_2025 p. 66), Danville arrastra avisos de las agencias ambientales (p. 94) y la última compra, Pet Mania, se frenó por un arancel (p. 140). Si el margen sigue la pendiente de la década, mi MALO (30,15 €) es el caso central y 54,70 € pagan un 81 % más que él.

Lo que no puedo defender del No: que la deuda mate a la empresa (0,87x EBITDA, 155,3 M€ de líneas libres; AR_2025 pp. 98, 122) o que la cuota esté cayendo.

## 13. Predicciones (dado el NORMAL)

1. Las ventas consolidadas de 2027 que publique Viscofan en su informe anual de 2027 estarán entre 1.300 y 1.420 M€ (1.252,0 M€ en 2025). Fecha 2028-03-31; probabilidad 0.65.
2. El margen de explotación de 2027 (resultado de explotación ÷ ventas consolidadas del informe anual de 2027) estará entre el 15,5 % y el 17,5 % (16,4 % en 2025). Fecha 2028-03-31; probabilidad 0.65.
3. La deuda bancaria neta a 31-dic-2027, con la definición de la empresa, no superará 1,5 veces el EBITDA de 2027 (206,1 M€ sobre 290,0 M€ de EBITDA, 0,71 veces, a 31-dic-2025). Fecha 2028-03-31; probabilidad 0.7.

Las tres fechas caen entre 12 y 24 meses después de Análisis!D4 (2026-11-13). Las probabilidades son de que cada predicción se cumpla dado el NORMAL, no la del escenario.

## 14. Incertidumbre pendiente (B222 · B223)

Lista D10 vacía: la hipótesis fundamentada de la que más depende la conclusión es Palancas!C15, que el margen EBIT del NORMAL deje de comprimirse en el 16,5 % (media de 2019-2025) en vez de seguir la pendiente de la década (del 21,1 % al 16,4 %, Historia fila 29). Si la compresión es estructural, el NORMAL es el MALO y el cubo es No. El objetivo lo condicionan además tres hipótesis de la configuración experimental sin fundamento suficiente: la estructura del mantenimiento, θ (qué parte del exceso de inversión de 2021-2025 fue reposición) y la familia de P-M1, que ninguna variante calcula.

La descomposición de la variación de ventas y de margen de 2023-2025 en volumen, precio y mezcla y coste de pieles, por tecnología y región, que el informe anual no publica (solo «mezcla de precios ligeramente inferior», AR_2025 p. 139): pregunta a Relación con Inversores. Para el objetivo: qué parte de la inversión de 2021-2024 clasificada como «capacidad y maquinaria» sustituyó capacidad existente y el desglose por tipo de 2024 en un documento conservado (2021, 2022, 2023 y 2025 ya están en el paquete: IA_2021_es.txt, PDF p. 213; CF_2022_compilacion.txt, PDF p. 202; IA_2023_es.txt, PDF p. 250; AR_2025.txt, PDF p. 143), y la vida útil y antigüedad media de las líneas de extrusión, conversión y cogeneración (pregunta a Relación con Inversores).

## 15. Qué me haría cambiar de cubo

- **A Sí:** un precio igual o inferior al precio de Sí (≤ 40,30 €, condicionado por la configuración) con el negocio intacto: margen EBIT de 2026 y 2027 en el 16 % o más con volumen al alza, cuota ganada con producto según el desglose de ventas, deuda bancaria neta por debajo de 1,5 veces el EBITDA, y saber quién es el competidor que más daño puede hacer (AR_2025 p. 399 no lo nombra). Antes de comprar, la comprobación conjunta tendría que superar las hipótesis de la configuración sin fundamento suficiente (estructura, θ, familia) y la lista D10 tendría que revisarse para esa compra.
- **A No:** que la compresión del margen sea estructural: un margen EBIT por debajo del 15 % dos años seguidos con volumen récord, o un desglose que muestre la cuota pagada con precio; también la deuda neta por encima de 1,5 veces el EBITDA por pagar al accionista (C98 pasaría a Dudosa) o una adquisición grande fuera del negocio.
- **A Demasiado difícil:** que el valor pase a depender de predecir el coste de las pieles bovinas o del dólar porque la empresa deja de repercutirlos (el descalificador de materias primas; AR_2025 p. 436), que un sustituto cambie el volumen del mercado de envolturas (riesgo citado sin cuantificar, AR_2025 p. 399) o que Danville se convierta en una contingencia que no pueda estimar (AR_2025 p. 94).

Condiciones de revisión del precio de Sí. Al alza: el margen EBIT publicado de 2026 y 2027 en el 16,5 % o más con volumen al alza, un desglose de ventas que muestre la cuota ganada con producto, o documentación de que la inversión de 2021–2024 clasificada como «capacidad y maquinaria» fue crecimiento (θ bajo: 42,00 € en la variante θ = 0). A la baja: margen EBIT por debajo del 15 % con volumen récord, deuda bancaria neta por encima de 1,5 veces el EBITDA por el reparto, o documentación de que el exceso de 2021–2022 fue sobre todo reposición (θ alto: 38,61 € en la variante θ = 1).

## 16. Comparación con la etapa 1

Cubo v1 Vigilar con precio de Sí de 25,1 €; cubo v2 Vigilar con precio de Sí de 40,30 €. El cubo coincide: buen negocio de nicho, en el círculo, a un precio sin margen. El precio de Sí sube por tres cosas, ninguna de las cuales es que el negocio haya mejorado. (1) La regla: la v1 tomaba mín(MALO, 0,75 × ponderado); la v2 usa la escalera de k = 3 con tope en el NORMAL; con la regla antigua sobre los valores de la v2 saldrían 30,15 € (C156). (2) El motor: la v1 proyectaba con el motor A un FCF base de 97 M€ y un MALO de caja plana (25,1 €; `etapa1/Viscofan_respuesta.md`); la v2 valora la operación con el motor B y resta la deuda de la base (puente de 273,8 M€), y su MALO (30,15 €) es una compresión del margen al 14 %. (3) La base y el precio: la v1 mezclaba datos de 2026 (1S26, deuda de junio) y un precio de 53,6 €; la v2 usa el cierre de 2025, con los datos corregidos de la rama, y 54,70 €. La v1 no tenía la Historia de diez años: ahora C27 = Comprimiendo y C25 = No se sostienen con filas, y C97 pasa de Neutral (sin registro) a Comprando con la evidencia de fase 1 (Control maestro fila 76). La v1 escribió un porcentaje de posición en C104; la v2 no lo hace.

Frente a la fase C cerrada de la 4.13 (`fase_c.4_13.json`): misma conclusión (Vigilar, `esperar`, objetivo condicionado por las mismas tres hipótesis); cambian solo las cifras por los datos corregidos (precio de Sí 40,16 → 40,30 €, MALO 30,02 → 30,15 €, ponderado 44,22 → 44,36 €, rango 38,47–43,39 → 38,61–43,52 €), el FCF al accionista de 2019 frente a 2025 se escribe con sus cifras (108,5 y 93,8 M€) en lugar de «no crece desde 2019», porque 2024 fue de 143,2 M€ (Historia fila 35), y B223 ya no pide el desglose por tipo de 2021–2023, que está en el paquete, sino la parte de «capacidad y maquinaria» que fue reposición y el de 2024.

El error que tengo más cerca sigue siendo pagar por calidad: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM). El contrario existe: si 2022-2023 fue un ciclo y 2024-2025 la recuperación, esperar a 40 € sería «early fretting» (TCI p.79; HIM). Confianza global: media.
