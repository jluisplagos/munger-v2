# Vidrala · fase C, turnos 1 y 2 (ensayo 4.10.1 · base económica 2025 · motor B)

Base: cierre del 31-dic-2025. Precio de 90,10 € con derecho al dividendo a cuenta, 35,182858 millones de acciones en circulación, puente de 160,784 (el dividendo a cuenta no se resta otra vez), r = 0,09, probabilidades 0,2 / 0,6 / 0,2 y k = 3 experimental. Precio, acciones y valor comparten fecha; no es un backtest y nada aquí es una recomendación. Importes en millones de euros (mm). Columnas de la Historia: C (2016) a L (2025). `ES_2025` es el informe español de 2025, como lo cita `extracto_v63.md`. Las sensibilidades salen de una réplica del motor B que reproduce la hoja al céntimo (53,66 / 72,74 / 86,44 y precio de Sí 66,52); no sustituyen a la hoja.

Reviso las fases A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

**Lo que calcula la hoja.**
- Valores por acción: MALO 53,66 · NORMAL 72,74 · BUENO 86,44 · ponderado (C83) 71,66. Valor sin crecimiento: 59,96.
- Escalera (`precio.json`): precio esc. MALO 53,66 · precio de Sí 66,52 (P\*, sin tope del NORMAL) · ponderado 71,66. Zona del precio de 90,10: **caro**. Distancias, sobre el precio: 26,2 % al precio de Sí y 40,4 % al MALO. Regla antigua (C156): 53,66.
- r operativa 0,087 (C15), por encima de la r mínima (0,0817).
- Peso del terminal: 41,7 / 52,6 / 57,0 %. Ninguno llega al 75 %.
- Salto del año 11: 1,8 / 2,3 / 4,0 puntos. Ninguno llega a 5.
- Flujo del año 1: 207,5 / 172,8 / 160,8. El del NORMAL cae dentro de los 140–180 mm que esperaba la fase A.
- Tornado: la tasa de descuento (±1 punto) mueve ±13,52 € el NORMAL; el margen ±2 puntos, ±7,99; el ROIC terminal ±5 puntos, ±7,52. El valor depende sobre todo de la rentabilidad exigida (aviso A5). Es información, no criterio.
- DCF inverso: con mis demás palancas del NORMAL, el precio de 90,10 descuenta un 9,2 % anual de crecimiento en los años 1–5 (C86). Es más que mi BUENO (3,5 %), más que el CAGR de 2020–2025 (8,2 %, que lleva Vidroporto y el salto de precio de 2022) y mucho más que el 1,3 % anual de Europa y Reino Unido sin Italia ni Brasil en 2022–2025. Dicho de otra forma: con mi NORMAL, el precio equivale a descontar a un 7,5 % en vez de a 0,087. Aquí la lectura es válida, porque precio y valor son del mismo día; no la leo como lo que espera el mercado.
- Veredicto de la hoja (A6): descartada por el filtro Pabrai, porque C13 = No. Mi cubo provisional es Vigilar: es el caso típico de la regla 4.

**¿Cuentan la misma historia que `fase_a.md`?** Sí. Las palancas siguen a las narrativas: el MALO baja juntos margen, ROIC y g; el BUENO no pide más de lo que la empresa ya hizo; el orden MALO ≤ NORMAL ≤ BUENO se cumple; la quiebra va vacía con 0,36 veces el EBITDA (C33). Encuentro cinco salvedades. Ninguna cambia la historia, la zona ni el cubo.

1. **Margen de partida (C8).** C8 = Media del ciclo hace que los tres escenarios arranquen en Historia C49 = 16,9 %. Esa media mezcla perímetros: Italia en 2016–2022, 2016–2018 con otra base industrial y Brasil solo desde diciembre de 2023. Las historias de la fase A parten del 19,9 % de 2025 (L29). En el NORMAL la hoja dibuja un margen que sube del 16,9 al 18,5 %; la historia dice que baja del 19,9 % hacia el 18,5 % con las bajadas de precio de 2026 [ES_2025, PDF p. 54]. Con m0 = 18,1 % el precio de Sí sube un 1,1 %; con 18,6 %, un 1,5 %; con 19,9 %, un 2,7 %. Es un sesgo conservador que sale de una regla correcta, no una palanca mal derivada.
2. **MALO con capital liberado.** Con ventas que caen, el motor libera unos 16 mm al año en los años 1–5. Por eso el flujo del año 1 del MALO (207,5) supera al del NORMAL y a la caja de 2025 (183,5, L35). La historia dice lo contrario: en 2025 las ventas bajaron 123,1 mm, el capital invertido solo 35,6 y la reinversión orgánica fue de +54,8 (Historia K6:L6, K32:L32 y L30). Sin esa liberación el MALO vale 51,67 y el precio de Sí baja un 1,3 %. La plantilla no tiene palanca para eso.
3. **Tipo impositivo.** Historia C52 = 20,0 % es la media de 2021–2025 de una serie que sube cada año: 15,9 %, 18,1 %, 20,4 %, 21,4 % y 24,3 % (H10:L10). Ni la fase A ni la B lo examinaron. Con el tipo de 2023–2025 (22,0 %) el precio de Sí baja un 2,7 %; con el de 2025, un 5,7 % (62,71), y la zona sigue en caro. En sentido contrario, los impuestos pagados de 2025 quedaron unos 26,6 mm por debajo del gasto (Control maestro, C40). No es una palanca: es una celda de datos de la plantilla que la fase C no cambia y que la fase B no puede corregir. Es la sensibilidad de datos más grande que encuentro y la dejo visible para la persona responsable.
4. **Celdas heredadas en el libro.** C93, B101, B102, C103 y C104 siguen con texto de la etapa 1: Chile desde marzo de 2026, deuda a 30-jun-2026, el precio de Sí antiguo y un porcentaje de posición. Son del turno 2.
5. **Texto de 2026 en Observaciones de datos** (C28, C32, C40, C41, C46, C47, C50 y C55) y C38 (Simply Wall St, 08-oct-2026). Sus valores son de la base 2025 o no entran en el motor; no uso ese texto.

**Hechos posteriores.** Toro, la tormenta Kristin y las operaciones de 2026 no entran en el balance, el perímetro ni las cifras de partida. Para escala: Kristin serían 0,28–0,43 € por acción sin seguro [ES_2025, PDF p. 85]; Toro, unos 77 mm de valor de empresa, del orden del 2–3 % de la capitalización.

**Variante de precisión.** C46:C47 = 335,4 / 169,7 frente a 335,413 / 169,668 no cambia ningún valor del motor B: solo entran en el FCF base del motor A.

## 2. Desviaciones pendientes

`gramatica.md` (tras el recálculo) da código 0. G8, G16 y G17 no saltan: el salto del año 11 máximo es de 4,0 puntos, el peso del terminal del NORMAL es del 52,6 % y la cuota implícita no se calcula sin C24. Lo único marcado es G5 en los tres escenarios, que la fase B justificó. Lo revisé como si fuera de otro y vuelvo a justificarlo con mis palabras en `desviaciones_justificadas`:
- **Contra qué se mide.** El Q3 (9,4 %) es el de un sector de envases en general. Vidrala está por encima los diez años, también en su mínimo (12,0 % en 2016, C50) y en el valle de 2022 (13,7 %).
- **El NORMAL** es la media del ciclo 2019–2025: comprobé el 18,1 % publicado y el 18,6 % sin Italia.
- **El BUENO** es el margen de 2025 mantenido, por debajo del máximo de 2024 (20,8 %).
- **Quién se queda la mejora:** el cliente en el MALO, repartida en el NORMAL y la empresa en la eficiencia propia en el BUENO, con confianza baja: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

El salto del año 11 no es un fallo; es la hipótesis de pérdida de ventaja que irá en la tesis. En el NORMAL, el capital nuevo deja de rendir el 13,3 % y se queda en dos puntos sobre r, porque no sé quién me mata. En el BUENO, la mezcla de Brasil y la eficiencia de los hornos no duran para siempre y el terminal conserva el ROIC de los peores años desde 2018 (Historia fila 33). «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).

## 3. ¿Hay que mover palancas?

**No pido `revisar_palancas`.** Comprobé la aritmética, el perímetro y el dato de cada palanca:
- Crecimiento del NORMAL: Europa y Reino Unido pasan de 1.240,6 mm (2022) a 1.289,0 (2025), un 1,3 % anual; con volumen ≈1 % y precio que baja en 2026 y luego sigue al coste sale ≈2 %.
- BUENO: 0,88 × (0 % en 2026 y ≈4 % después) + 0,12 × ≈5,5 % da ≈3,5 %.
- Margen: la dilución de Italia es de 0,80 / 0,44 / 1,04 / 0,84 puntos en 2019–2022; la media sin ella, 18,57 %. El MALO sin Italia en 2022, 14,5 %.
- S2C: C54 = 0,93; Δventas ÷ Δcapital 2016–2025 = 0,90; 2021 = 1,02 y 2024 = 0,99.
- Rentabilidades marginales: 10,8 / 13,3 / 16,0 %.

No encuentro ninguna palanca mal derivada. Los dos límites que encuentro no son de la fase B:
- **C8** es de la fase A y su efecto sale de una celda de datos.
- **La liberación de capital del MALO** no tiene representación en la plantilla.

Corregir cualquiera de los dos mueve el precio de Sí menos de un 5 % (+2,7 % y −1,3 %) y no cambia ni la zona ni el cubo. Lo mismo vale para todo movimiento dentro de los rangos de la fase B, uno a uno (el mayor, el margen del MALO, ±2,0 %; subir el MALO a 0,25 de probabilidad, −2,2 %) y todos a la vez: la combinación pesimista da un precio de Sí de 60,1 y la optimista, con m0 = 19,9 %, 77,9 con un ponderado de 83,1. Las dos quedan en caro. El tipo impositivo (−5,7 % con el de 2025) no es una palanca: no se arregla volviendo a la fase B. La única vuelta C → B queda sin usar. En `celdas_corregidas` dejo C8, B16, C15, C62 y B69 con `despues = antes` y el motivo.

## 4. Autocomprobación

- **Anclaje en la etapa 1.** g y probabilidades repiten las cifras de la etapa 1, pero con hechos de 2025 y sin Chile; el precio de Sí no se parece (≈48 € frente a 66,52). Leí la fase C del antecedente 4.6.1 sin copiarla: tenía otro precio (87,90 €), las acciones emitidas y citas del texto inglés. «the new ideas were not accepted because they were inconsistent with old ideas in place» (PCA p.526; HIM).
- **Anclaje en el precio o en la fuente externa.** Ninguna palanca usa 90,10, C38 ni objetivos de analistas. Que el precio supere incluso mi BUENO (D86) no me lleva a subirlo: con todo en el extremo optimista de la fase B el ponderado llega a 83,1. La distancia la explica la tasa, no unas palancas tímidas. «Few psychological tendencies do more damage to correct thinking» (PCA p.579; HIM).
- **Consistencia y compromiso.** El cubo y el motor se fijaron antes de ver valores; las desviaciones de la fase B van en los dos sentidos y la zona sobrevive a moverlas todas a la vez.
- **Historia bonita / viento de cola.** Parte del margen de 2023–2025 es el desfase del ciclo de energía [CF_2022.txt, PDF p. 45], no foso. El NORMAL no lo extrapola; el BUENO lo mantiene con confianza baja y peso 0,2. C17 = No.
- **Optimismo del BUENO frente a la tasa base.** Margen y ROIC del BUENO no superan lo que ya hizo la empresa; en diez años solo 2024 tuvo un margen igual o superior al del BUENO y solo 2022 uno inferior al del MALO desde 2018. 0,2 / 0,6 / 0,2 cae dentro de esas frecuencias. «What a man wishes, that also will he believe» (PCA p.564; HIM).
- **Doble castigo del mismo riesgo.** Uno pequeño y mecánico: el margen en lo alto del ciclo está en el objetivo del NORMAL y otra vez en el arranque desde C49 (hasta +2,7 % si se quitara). Sin prima de quiebra en r ni en C22; el dividendo no se cuenta dos veces.
- **Disponibilidad.** Kristin, Toro, el apagón y la reestructuración no se extrapolan; mandan las diez filas de la Historia. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).
- **Autoridad.** Volumen, IPC y perpetuidad vienen de las pruebas de deterioro y van como hipótesis de la empresa; sin el volumen el precio de Sí baja un 1,2 %. «A projection prepared by… an executive trying to justify a particular course of action will frequently be a lie» (TCI p.60; HIM).
- **¿El MALO es de verdad malo?** En margen y retorno, sí; tiene el maquillaje del capital liberado. Con el valle de 2022 para siempre y sin liberación valdría 47,58 (precio de Sí −3,9 %). «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** Quién me mata, la sustitución del vidrio, el coste del CO2 y de la descarbonización, los insiders sin verificar, Toro y la tendencia del tipo impositivo. Va a B102 y a B222 en el turno 2.

## 5. Cubo y conclusión provisionales

Orden de mando:
1. **Bloqueo:** no hay. Gramática con código 0; el estado técnico es INCOMPLETO solo por las predicciones, que son del turno 2.
2. **Límite del modelo:** no hay. El motor B cumple sus condiciones.
3. **Descalificador:** ninguno. Revisé los nueve de la fase A. El más cercano sigue siendo el de la macro y la energía, y no aplica: el valor depende del traslado al precio, que es del negocio. La deuda es de 0,36 veces el EBITDA.
4. **Dato ausente material:** ninguno (§6).
5. **Fundamento material:** una hipótesis, acotada con hechos (§7).
6. **Zona:** caro, a un 26,2 % del precio de Sí.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`.** Lo entiendo, está en mi círculo con el borde nombrado, tiene un foso estrecho y una gestión de fiar, y al precio de cierre no lo veo barato: «we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). El precio objetivo es el precio de Sí, 66,52. Como la única hipótesis de la lista tiene base, D10 no lo marca como provisional. Lo que más puede moverlo es el tipo impositivo (hasta 62,71). De los dos errores opuestos sigo teniendo más cerca pagar por un margen de lo alto del ciclo: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 6. Datos ausentes (S-19)

Reviso los 39 datos de `datos_ausentes.json` uno a uno; el detalle está en el JSON. Ninguno es material para sostener `esperar` con un precio de Sí de 66,52: el que más lo mueve es el margen por segmento de 2016–2023, que resolvería C8 (de 0 a +2,7 %, al alza). Los tres abiertos que el encargo no permite cerrar:
- **P3** (C48 = 0, C49 = 4,5, supuesto heredado y no un principal acreditado): **materialidad nula para esta conclusión.** No entran en el valor del motor B (f = 0 en el motor; el FCF base solo lo usa el motor A). C63 sale de los intereses totales de la fila 15, que el estado de flujos lleva en explotación sin línea de intereses ni de arrendamientos en financiación [ES_2025, PDF p. 14]. Aun si los 2,452 de intereses de arrendamientos [ES_2025, PDF p. 58] estuvieran fuera de esa fila, el precio de Sí bajaría un 0,7 %. No lo declaro resuelto.
- **N4** (minoritarios L26 = 0 y los demás ceros): **materialidad baja.** Cada millón de minoritarios resta 0,028 € por acción; harían falta unos 117 mm para mover el precio de Sí un 5 %, y el balance no tiene línea de participaciones no dominantes [ES_2025, PDF p. 10]. Los ceros de adquisiciones, intereses en financiación y principal antiguo solo tocan referencias y series de contexto. No confirmo ningún cero ni activo su verificación.
- **Provisión de personal** (L25 = 6,223, que entra como pensiones): **materialidad baja.** Toda ella son 0,18 € por acción (0,27 %). Sobre el doble cómputo, la limitación es esta. El motor B no proyecta desde el CFO sino desde el EBIT, así que el hecho de que las aportaciones vayan en el CFO no prueba nada. Si parte de la provisión son retribuciones devengadas cuyo gasto ya está en el EBIT, restarla en el puente la cuenta dos veces; si es déficit de prestación definida, restarla es correcto. Sin desglose no lo separo; el error posible está acotado por la provisión entera.

Los que el extracto no encontró (volúmenes, cuotas, competidores, capacidad, capex plurianual) bajan la confianza en C18 y en el NORMAL, pero no mueven el precio de Sí fuera de los rangos ya calculados. `alguno_material = false`.

## 7. Fundamento material (D10)

Recorrí las hipótesis materiales:
- las cinco palancas en los tres escenarios, todas fundamentadas con hechos;
- las probabilidades, convención con argumento propio y con hechos; las crucé con las frecuencias observadas;
- la quiebra y su recuperación, C76 y C44;
- el motor, C6 y C8;
- las seis celdas de narrativa.

Ninguna tiene clase «sin juicio propio» ni «técnico», y todas citan hechos. Las narrativas nombran mecanismo, dueño de la mejora y qué lo pararía con páginas; la parte más débil es la lectura del BUENO de que las fórmulas trasladan la energía y no la eficiencia propia, declarada como lectura y con confianza baja.

Una hipótesis queda sin fundamento en su consecuencia numérica: **Palancas C8**. La regla está bien elegida (UD; E5), pero fija un margen de partida del 16,9 % que ningún hecho del perímetro de 2025 sostiene. Tiene base para acotarse:
- **Suelo, 16,9 % (C49).** Las dos correcciones de perímetro que puedo medir la suben: sin Italia, +0,4 a +1,0 puntos en 2019–2022 [CF_2019.txt, PDF p. 38], [CF_2021.txt, PDF p. 30] y [CF_2023.txt, PDF p. 29]; con Brasil, el segmento de más margen [ES_2025, PDF p. 107].
- **Techo, 19,9 % (L29).** Es el único año homogéneo; partir de más exigiría un margen que sube con las bajadas de precio que supone la empresa para 2026 [ES_2025, PDF p. 54].

Su efecto va de 0 a +2,7 % del precio de Sí. Con conclusión no favorable, `resultado = no_procede`. No hago la comprobación conjunta: es opcional y la hipótesis no es una celda numérica de las fases A o B. `sobrevive = null`.

## 8. Hipótesis que más condiciona y qué la resolvería

**Palancas C8**, la base del margen. La resolvería el EBIT o el EBITDA por segmento de 2019–2023 o una cuenta de continuadas sin Italia para 2019–2022, para calcular una media de ciclo del perímetro de 2025. La empresa solo publica el EBITDA por segmento de 2024 y 2025 [ES_2025, PDF p. 107] y solo reexpresó 2023 [CF_2024.txt, PDF p. 30]. Es una pregunta a Relación con Inversores.

**De las fundamentadas**, la que más pesa en mi juicio es el margen del NORMAL: cuánto del ahorro de energía se va al cliente en 2026–2027. **De los datos**, el tipo impositivo, que no es hipótesis mía pero mueve el precio de Sí más que cualquier palanca dentro de su rango. «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 9. Conclusión (turno 2)

No existe `comprobacion_conjunta.json`: el turno 1 la dio como `no_procede`, así que `sobrevive = null` y `resultado = no_procede`.

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 66,52.** Sale del mapa cerrado de la sección 15:
- no hay bloqueo, límite del modelo ni descalificador;
- no hay dato ausente material (S-19);
- la conclusión no es favorable, así que D10 no la limita;
- la zona es `caro`, así que no hace falta una condición que no sea de precio.

Como la única hipótesis de la lista (C8) tiene base, el precio objetivo no queda marcado como provisional por D10.

Qué significa aquí: el precio de Sí es un valor a 31-dic-2025, con derecho al dividendo a cuenta y sobre las acciones en circulación, comparado con el precio de cierre del mismo día. No es un backtest ni una recomendación, y el tamaño de la posición es de José Luis.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 66.52 · zona caro · precio de Sí ≤ 66.52 · precio esc. MALO 53.66 · ponderado 71.66 · fundamento no procede (conclusión no favorable)».

Quedan para la persona responsable, sin firmarlas yo:
- el tipo impositivo de la hoja (Historia C52 = 20,0 % frente al 24,3 % de 2025: el precio de Sí bajaría a 62,71);
- la carencia de C8 (de 0 a +2,7 %);
- el límite de traducción del MALO (−1,3 %).

P3, N4 y la provisión de personal siguen abiertos, con materialidad nula o baja para esta conclusión (§6).

**C93 = Sí.** La g del NORMAL (0,02) está por debajo de rf y de la r operativa. La reinversión terminal es de ≈18 % del beneficio operativo, el salto del año 11 de 2,3 puntos y el peso del terminal del 52,6 %. «If a thing can't go on forever, it will eventually stop» (PCA p.416; HIM).

**C103 = No.** Es una cíclica con foso estrecho: margen del 13,7 al 20,8 % con la energía (Historia fila 29) y ROIC de solo 4,8 puntos de media sobre r (C55).

## 10. Tesis (B101)

Vidrala fabrica envases de vidrio para alimentación y bebidas en la Península, Reino Unido e Irlanda y Brasil, para clientes diversificados: los diez primeros son algo más del 35 % de las ventas y ninguno pasa del 10 % [ES_2025, PDF p. 104]. Traslada el coste de la energía al precio con retraso: el margen EBIT cayó al 13,7 % en 2022 y volvió al 18,7–20,8 % en 2023–2025 (Historia fila 29). Rinde por encima de su capital, con un ROIC de al menos el 11,9 % cada año desde 2018 (fila 33), y a 31-dic-2025 debía poco: 0,36 veces el EBITDA con arrendamientos (C33). Toro (Chile) y la tormenta Kristin son hechos posteriores que no entran en las cifras [ES_2025, PDF p. 85]. Leo un foso estrecho de escala regional y un margen de 2025 que la propia empresa supone que bajará con los precios de 2026 [ES_2025, PDF p. 54]: mi NORMAL es la media del ciclo 2019–2025 (18,5 %), y en el año 11 el capital nuevo pasa de rendir un 13,3 % a dos puntos sobre r. El motor B da 53,66 / 72,74 / 86,44 € por acción y un precio de Sí de 66,52, frente a un cierre de 90,10 que pedía un 9,2 % anual de crecimiento (C86). Vigilar.

## 11. Tesis inversa (B102)

La defiendo contra mí, con los hechos que más daño le hacen:
- **No hay foso demostrado.** Ningún informe nombra a un competidor con cuota (extracto §9). El ROIC medio solo supera a r en 4,8 puntos (C55). El margen supera al Q3 del sector porque ese sector es el de envases en general (Palancas I15).
- **El margen de 2023–2025 es en buena parte ciclo.** La propia empresa lo explicaba por el desfase entre subidas de precio y normalización de la energía [CF_2022.txt, PDF p. 45], y ya supone bajadas de precio en 2026 [ES_2025, PDF p. 54]. Con el NORMAL en la media de diez años (16,9 %, C49), el valor pierde unos 6,4 € por acción.
- **El volumen no crece.** Vidrala Europe baja de 799,7 a 714,9 mm en 2023–2025 [CF_2024.txt, PDF p. 30] y [ES_2025, PDF p. 33].
- **La reinversión no da tregua.** Capex de 188,5 frente a 132,9 de amortización (L12 y L8) y compromisos de 66,6 mm [ES_2025, PDF p. 51]. En 2025 el capital invertido apenas bajó con las ventas (K32:L32), así que mi MALO, que libera capital, es más amable que la realidad.
- **La caja de 2025 está inflada y el modelo es generoso con el fisco.** El impuesto pagado quedó unos 26,6 mm por debajo del gasto (Control maestro, C40) y hay 43,1 mm de «Otros» ingresos sin detalle [ES_2025, PDF p. 79]. La hoja grava el EBIT al 20,0 % (C52) cuando el tipo de 2025 fue del 24,3 % (L10): solo eso resta un 5,7 % al precio de Sí.
- **Divisa, Brasil y Toro.** Casi la mitad de las ventas está en libra y real [ES_2025, PDF p. 103], y Brasil carga 18,9 mm de gastos financieros [ES_2025, PDF p. 33]. Toro llega después del cierre, condicionada a un ajuste organizativo [ES_2025, PDF p. 85].
- **El valor depende sobre todo de la tasa**, no de algo que yo sepa del negocio.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 12. Predicciones (dado el NORMAL; fecha de análisis 11-nov-2026)

1. Margen EBIT consolidado de 2027 (resultado de explotación ÷ ventas de las cuentas consolidadas de 2027) entre el 16,0 % y el 20,5 %, ambos incluidos; fue el 19,9 % en 2025. Fecha 2028-03-31 · probabilidad 0,7.
2. Ventas y prestación de servicios del segmento Vidrala Europe en 2027 entre 680 y 770 mm, según la nota de segmentos; fueron 714,9 en 2025. Fecha 2028-03-31 · probabilidad 0,75.
3. Pagos por inmovilizado material e intangible del estado de flujos consolidado de 2027 por encima de la amortización consolidada del mismo año; en 2025, 188,5 frente a 132,9. Fecha 2028-03-31 · probabilidad 0,8.

Las tres son sobre el negocio y se comprueban con cuentas publicadas. Su fecha cae dentro de la ventana de 12–24 meses. Son la autopsia de este análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

**B222.** Palancas C8: la hoja arranca los tres escenarios en un margen del 16,9 % (C49) que ningún hecho del perímetro de 2025 sostiene. Acotado entre 16,9 y 19,9 %, mueve el precio de Sí de 0 a +2,7 % sin cambiar zona ni cubo. Queda además, para la persona responsable, el tipo impositivo de la hoja (−5,7 %).

**B223.** El EBIT o el EBITDA por segmento de 2019–2023, o una cuenta de continuadas reexpresada sin Italia para 2019–2022. Es una pregunta a Relación con Inversores.

## 13. Qué me haría cambiar de cubo

- **A Sí:**
  - un precio igual o inferior a 66,52 con el negocio igual: margen EBIT de 2026–2027 en torno al 18 % o más sin choque de energía y ROIC por encima del 11 %;
  - y, antes de comprar, cuotas o competidores publicados que no muestren pérdidas.
- **A No:**
  - margen EBIT por debajo de su media de diez años (16,9 %) dos años seguidos sin choque de costes;
  - pérdidas de cuota;
  - ROIC por debajo de r con el perímetro de 2025;
  - Toro o Brasil pidiendo capital sin retorno con la deuda por encima de 2 veces el EBITDA.
- **A Demasiado difícil:**
  - que el valor pase a depender de Sudamérica más que de Europa;
  - evidencia de sustitución del vidrio que no sé medir;
  - una descarbonización cuya rentabilidad no pueda estimar.

## 14. Comparación con la etapa 1

El cubo coincide (Vigilar), y por la misma razón: un buen negocio cíclico con foso estrecho, que no se ve barato sin la hoja (C13 = No).

El precio de Sí no es comparable:
- **Etapa 1 (≈48, estimado):** salía del motor A con un FCF base de 161 mm que mezcla perímetros, de datos de 2026 (Chile, saldos a 30-jun-2026) y de la regla antigua mín(malo, ¾ del ponderado).
- **V6.3 (66,52):** sale del motor B con base de 31-dic-2025, palancas fundamentadas y la escalera k = 3. Con la regla antigua sobre estos valores saldría 53,66 (C156).

Herencia de las celdas de la fase C:
- **C93 y C103** se mantienen, con la evidencia nueva de la Historia y del libro.
- **B101 y B102** se reescriben sin hechos de 2026.
- **C104** cambia por definición (D16): ningún porcentaje de posición.

La diferencia es de método y de datos, no de juicio sobre el negocio.

## 15. Checklist de la fase C (sección 17)

- Las 68 respuestas cuentan una sola historia, con cinco salvedades cuantificadas (§1).
- Autocomprobación con contenido (§4).
- Los 39 datos ausentes revisados (§6).
- Lista de hipótesis completa, con su acotación (§7).
- Estado, cubo y acción coherentes con la sección 15.
- C104 sin porcentaje.
- Tres predicciones falsables sobre el negocio, con fecha y probabilidad.
- Tesis inversa con hechos.
- B222 y B223 concretos.
- Comparación con la etapa 1.
- Qué me haría cambiar de cubo.
- Ninguna cita sin libro y página.
