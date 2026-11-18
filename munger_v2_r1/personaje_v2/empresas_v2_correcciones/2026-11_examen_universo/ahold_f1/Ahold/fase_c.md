# Fase C · turno 1 · Koninklijke Ahold Delhaize N.V. (AD) · motor A

Fuentes: Historia fila n y Cnn son celdas de `datos_v63.md`; páginas de los informes como las cita `extracto_v63.md` (AR2025 PDF p. n; Q3-26 PDF p. n). Valores de la hoja de `resultados.json` y escalera de `precio.json`, leída, no recalculada. Las variantes que doy son mías: una réplica de la fórmula del motor A que reproduce B78:D78 al céntimo, con la escalera aplicada por el mismo método. No sustituyen al recálculo oficial.

## 1. Una sola historia

Lo que dice la hoja: MALO 22,99 €, NORMAL 26,12 €, BUENO 33,48 €, ponderado 26,44 €. Precio 36,05 €. Precio de Sí 25,29 € (sin tope del NORMAL). Zona caro. El precio está un 42,6 % por encima del precio de Sí (diferencia ÷ precio de Sí). El precio supera también el BUENO y el valor sin crecimiento (30,07 €). Semáforos: todos pasan. La cuota implícita no se calcula (C24 vacía). Peso del terminal: 40 %, 53 % y 59 %. Salto del año 11: −1,1, +0,8 y +1,3 puntos; ninguno pasa de 5. El tornado pone primero el margen (±2 puntos mueven el ponderado 18,63 €), después el ROIC a largo plazo (9,39 €) y la tasa (4,48 €). Es información, no criterio.

DCF inverso: la tabla no se puede usar. Con mis palancas, crecer destruye valor en el NORMAL. La rentabilidad marginal es 8,8 % bruta y 7,6 % neta de f [3,2 × (0,035 × 0,786 − 0,0036)], por debajo de r = 0,09. Ninguna tasa de crecimiento llega a 36,05. Con la fórmula del motor, el precio descuenta dos cosas posibles. Sin crecimiento y con r = 0,09: un margen IFRS del 4,5 % para siempre, por encima del máximo de diez años (C51 4,39 %). Con el margen de 2025 y sin crecimiento: un rendimiento del 7,5 %, por debajo de r y de la r mínima (7,86 %).

La historia grande es la de la fase A: un negocio duradero que no gana más que mi alternativa, a un precio que pide un margen que no ha tenido. Pero las cifras no la cuentan del todo igual. Hay ocho puntos:

1. **Perímetro.** El libro calcula el motor A en el perímetro A2_propio (Historia C85). Los pagos de arrendamiento están dentro de f (0,0036 frente a 0,0189 en A0). La reinversión es el capex propio menos la amortización propia, más el circulante y las compras (Historia filas 30–31). Pero D16 (3,6) se midió con el capital invertido de la fila 32, que incluye los pasivos por arrendamiento: 17.840 en 2017 y 25.568 en 2018, cuando entran 9.432 de arrendamientos (fila 23). El ancla de B16 (2,46 y 2,57 en 2018–2019) también lleva arrendamientos. B18:D18 salen de la fila 33 y de C54 (3,19), medidas con el mismo capital. Así el capital arrendado se cobra dos veces. La propia empresa separa los dos perímetros: Tesco Chequia y Eslovaquia vale 1.200 de valor empresa y 1.700 con arrendamientos (Q3-26 PDF p. 30). El 85 % de los locales es arrendado (AR2025 PDF p. 58).
2. **C14 frente a C16.** El NORMAL crece un 3 %: unos 2,5 puntos orgánicos y 0,5 de compras. El S2C de 3,2 sale de 2022–2025, años en que Profi aporta 2.867 de los 5.368 de ventas nuevas (53 %) y 1.239 de los 1.655 de reinversión (75 %) (Historia filas 6 y 31; AR2025 PDF p. 222). Cobra todo el crecimiento a la intensidad de una compra. Sin Profi la ventana da unos 6. Con la mezcla que cuenta C14 sale unos 4,7–4,8.
3. **El crecimiento.** Que crecer destruya valor depende de los puntos 1 y 2. Con un S2C de 4,7 en A2, la rentabilidad marginal neta sería de un 11 % y el crecimiento del NORMAL crearía algo de valor. El juicio de calidad de la fase A (C18 = No, medido con el capital total) no cambia. Lo que cambia es el motivo de no pagar por crecer.
4. **C8 = Último año.** La fase B dice que 2025 tuvo pocos cargos y pone el NORMAL en 3,5 %, por debajo del m0 de 3,84 %. El motor arranca, por tanto, del mejor año de la ventana. Con Media del ciclo, el precio de Sí bajaría un 0,9 %. Mantengo la celda porque la regla da Último año.
5. **f.** f se calibra con una ventana que incluye la devolución fiscal belga de +367 en 2023 (datos_v63 §2, Observación de C48 y C49). La fuga de 2025 sola es 0,0059 de las ventas: 2.784 de NOPAT menos 85 de reinversión propia menos 2.150 de flujo del accionista. Sin la devolución, la ventana da unos 0,005. Con esa f el precio de Sí bajaría un 8–13 %. Es un dato de la hoja: no lo cambio. Empuja en la dirección del No y de caro.
6. **La caja del MALO.** El año 1 del MALO da 2.328, más que cualquier flujo del accionista de la década (máximo 2.150, fila 35), porque con crecimiento 0 no reinvierte. Su daño está en el margen de los años 4–10 y en el terminal.
7. **D18 = 0,10.** Queda por encima del ROIC homogéneo más alto (9,8 % en 2022). El 11,5 % de 2017 se mide sin arrendamientos (fila 23 = 0) y no es comparable. Eso refuerza C18 = No.
8. **A6.** Dice descartada por el filtro Pabrai (C13). Mi No es por la calidad, no por el filtro.

## 2. Desviaciones pendientes

`gramatica.md` (tras el recálculo) no trae ninguna desviación: ni G8, ni G16, ni G17. Solo el aviso A3: precio del 13-nov-2026 y acciones del 28-dic-2025. Con las acciones del 3T el valor por acción subiría alrededor de un 3,6 % y la zona no cambiaría. No hay nada que justificar. Ningún escenario usa como ROIC terminal la tasa del motor; las separaciones del año 11 son hipótesis mías y van en la tesis.

## 3. Palancas: vuelta a la fase B

La aritmética de cada palanca cuadra. El error está en el perímetro, y v2.1 no me deja dejarlo como error prudente salvo que corregirlo mueva el precio de Sí menos de un 5 %.

| Variante (réplica del motor) | MALO | NORMAL | BUENO | Precio de Sí | Ponderado | Zona |
|---|---|---|---|---|---|---|
| Libro actual | 22,99 | 26,12 | 33,48 | 25,29 | 26,44 | caro |
| D16 = 6,9 | 22,99 | 26,12 | 37,59 | 25,70 (+1,6 %) | 27,05 | caro |
| D16 = 6,9 y D18 = 0,17 | 22,99 | 26,12 | 40,81 | 26,02 (+2,9 %) | 27,54 | caro |
| C16 = 4,8 y C18 = 0,12 | 22,99 | 30,10 | 33,48 | 26,88 (+6,3 %) | 28,83 | caro |
| C16 4,8 · C18 0,12 · D16 6,9 · D18 0,12–0,17 | 22,99 | 30,10 | 38,89–40,81 | 27,42–27,61 (+8–9 %) | 29,64–29,93 | caro |

Ni la zona ni el cubo cambian. El precio de Sí sí se mueve más de un 5 %. Por eso `revisar_palancas = true`. Las instrucciones (D16, B16, C16 y B18:D18, con sentido y motivo) están en el JSON. No toco ninguna celda. No pido cambiar crecimientos, márgenes, g, probabilidades, quiebra ni C76: revisé su derivación y es correcta. f y el FCF base son datos.

En `celdas_corregidas` registro lo que revisé, siempre con `despues = antes`. Revisé de la fase A C18, C62 y Palancas!C8. C18 lo revisé con lo que lo contradice: ROIC sin fondo de comercio de 12,9–13,5 % (C24), ROE de cinco años del 14,6 % y el 38,2 % de Albert Heijn. Se sostiene: con el capital total el negocio no supera r en diez años, y el ahorro se va al precio (AR2025 PDF p. 45). «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM). El ROIC del capital propio en A2 está apalancado por los arrendamientos: no prueba un foso.

## 4. Autocomprobación

- **Anclaje en la etapa 1.** Vigilé el riesgo contrario: cambiar el foso solo por llevar la contraria. Lo revisé con la evidencia en contra y se mantiene. El No no depende de los 0,2 puntos entre el ROIC y r.
- **Precio o fuente externa.** Simply Wall St da 61,27 € y los analistas 37,55 €; mis valores están lejos de los dos. Los cambios que pido salen del perímetro, no del precio. Corregidos, el ponderado sigue por debajo de 36,05.
- **Consistencia y compromiso.** Todas las palancas quedan por debajo de su referencia. Ese patrón es sospechoso en quien ya decidió No. Lo busqué y encontré dos errores que empujan hacia abajo (el perímetro y la mezcla de C16). Pido revisarlos.
- **Viento de cola.** El 2022 (+15,1 %) y buena parte del +4,3 % de cinco años son inflación, tipo de cambio y Profi. El NORMAL ya los separa.
- **Optimismo del BUENO.** El BUENO pide un 4,0 % sostenido, cuando la media de tres años más alta fue 3,98 %, y un ROIC del 10 %, por encima del 9,8 % homogéneo. D18 se revisa por el perímetro.
- **Doble castigo.** La doble cuenta literal es el capital arrendado, que está en f y otra vez en el S2C y el ROIC. Es la lógica de (PA, E6) aplicada al capital, convención del ejercicio. Además, el margen del NORMAL, el MALO y las probabilidades caen del mismo lado. Cada uno tiene su hecho. Con 0,2/0,6/0,2 el precio de Sí sería 25,83 € (+2,1 %). Lo dejo para la tesis inversa.
- **Disponibilidad.** p(MALO) = 0,25 no descansa en un trimestre de 2026: cuatro de los diez años tuvieron un margen IFRS del 3,2 % o menos (fila 29). «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).
- **Autoridad.** El NORMAL coincide con la guía (en torno al 4 % subyacente), pero sale de la banda de diez años (AR2025 PDF p. 64). La guía solo sirve de techo del BUENO.
- **¿El MALO es malo?** En margen y ROIC, sí. En la caja de los años 1–3, no. Y no recoge la renta fija ni la deuda neta que sube (16.087, Q3-26 PDF p. 24). «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** Hay 14.721 de pagos de arrendamiento sin descontar (AR2025 PDF p. 271), que f trata como proporcionales a las ventas. Profi supera su prueba de deterioro por poco (AR2025 PDF p. 238). Viene otra compra (Tesco). Hay transiciones en la dirección sin motivo publicado. Va a la tesis inversa y a B222.

## 5. Cubo y conclusión provisionales

Sigo el orden. No hay bloqueo: la gramática da cero errores, y el estado INCOMPLETO solo se debe a las predicciones. No hay límite del modelo: el motor A es utilizable según F1. Hay un juicio de calidad que no se cumple: el retorno del capital total no supera mi alternativa en diez años y el ahorro se lo queda el cliente. No es un descalificador de la sección 2, sino lo que sale de la evaluación: «We have three baskets: in, out, and too tough» (TCI p.13; HIM). Ningún dato ausente es material. El fundamento no procede, porque la conclusión no es favorable. La zona es caro, y lo sigue siendo en todas mis variantes.

**Cubo provisional: No. Conclusión provisional: descartar.** La revisión de palancas puede subir el precio de Sí un 8–9 %, pero no lo acerca al precio: el ponderado más alto de mis variantes (29,93 €) queda un 17 % por debajo de 36,05 (diferencia ÷ precio).

## 6. Datos ausentes (S-19)

Reviso los 29 datos de `datos_ausentes.json`. Ninguno es material: `alguno_material = false`. Los dos ceros pendientes de verificación no tocan las anclas de cinco años. Los de 2016–2017 hacen no comparable el ROIC de 2017, y eso refuerza C18 = No. Los minoritarios no entran en el motor A. Tamaño de mercado, cuotas, competidores, I+D, regulación y online: ninguno mueve una palanca del NORMAL ni la zona. El BUENO es de margen, no de cuota. Profi, Tesco, el capex por destino y el desglose de precio y volumen afectan al S2C y al crecimiento, que en el tornado mueven 0,65 € y 0,43 €. Lo que sí falta para el S2C (la reinversión A2 de diez años) lo pido a la fase B con la Historia. Calificaciones de 2026, covenant y ciberataque: con deuda neta/EBITDA de 2,2, BBB+/Baa1 a cierre de 2025 y 3.115 de liquidez más 1.500 sin disponer, ninguno cambia la quiebra. Insiders y firmantes: la gestión se juzga por diez años de historial. La conclusión descartar no depende de ninguno.

## 7. Fundamento material (D10)

Ninguna palanca, probabilidad, quiebra ni C76 tiene clase técnico o sin juicio propio. Todas las Observaciones citan hechos y las narrativas tienen mecanismo y freno concretos. Pero dos grupos se apoyan en hechos de otro perímetro: Palancas!D16 y Palancas!B18:D18. Los incluyo en la lista con sus rangos, cada límite atado a una celda de la Historia o a una página:

- D16: entre 3,2 (el NORMAL en A2) y 6,9 (2020–2025 sin arrendamientos).
- ROIC: MALO 0,06–0,12, NORMAL 0,08–0,13, BUENO 0,10–0,17.

Como la conclusión no es favorable, `resultado = no_procede` y no hago la comprobación conjunta. `sobrevive = null`.

## 8. Lo que más condiciona

De la lista, lo que más condiciona es Palancas!B18:D18, sobre todo C18 (ROIC a largo plazo del NORMAL) junto con C16: hasta +6 % del precio de Sí, sin cambiar ni la zona ni el cubo. La conclusión descartar descansa en Análisis!C18 = No, que es fundamentada.

Lo resolvería:
- la reinversión neta propia y las compras de 2016–2022 (Historia filas 30 y 31, hoy solo 2023–2025) y la amortización de derechos de uso de esos años, para medir en A2 el S2C y el ROIC de diez años;
- las ventas y el resultado de Tesco Chequia y Eslovaquia.

«The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
