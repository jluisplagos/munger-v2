# Fase C · turno 1 · Vidrala, S.A. (VID) · base económica 31-dic-2025 · V6.4 experimental, motor B · copia con protocolo «bloqueo_del_objetivo»

Esta carpeta es la copia del cierre condicionado. Solo cambia el protocolo experimental del objetivo, que ahora es «bloqueo_del_objetivo». Ninguno de los dos protocolos está adoptado. Libros, palancas, variantes y `precio.json` son los mismos (lo he comprobado archivo por archivo). La fase C de aquel cierre es mi referencia, pero su aprobación está retirada y no vale aquí: la reviso como si fuera de otro. «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Los hechos salen de `datos_v63.md` (Historia, anclas), de `extracto_v63.md` ([ES, PDF p. n] y [CF_aaaa, PDF p. n]) y de lo que calcula la hoja (`resultados.json`, `precio.json`, `configuracion_v64_variantes.md`). Las cifras marcadas «cálculo mío» son aproximaciones con la sensibilidad del tornado o con la fórmula de la escalera; no son recálculos del libro.

## 1. Una sola historia

**Lo que calcula la hoja.** Valor por acción de 44,32 / 60,21 / 78,52 € (MALO / NORMAL / BUENO), ponderado de 60,70 €, precio de Sí de 56,02 € (P\*, sin tope del NORMAL) y precio de 90,10 €: zona **caro**. 90,10 está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí); dicho al revés, el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio). La regla antigua (C156) da 44,32. El peso del terminal es del 41 / 48 / 54 %, siempre por debajo del 75 %.

Los semáforos:
- margen en REVISAR en los tres escenarios (G5, justificado en la fase B: Vidrala está por encima del Q3 del sector todos los años);
- f = −2,8 % en REVISAR, que es la razón del motor B;
- cuota implícita sin calcular (C24 vacía);
- el resto pasa.

El estado técnico es «COMPLETO Y VÁLIDO», porque el libro de esta copia ya lleva las predicciones y los textos de la fase C del cierre condicionado. La hoja dice «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar, porque C13 mide el precio, no el negocio.

**DCF inverso.** A 90,10 el mercado descuenta un crecimiento de ventas del 14,2 % anual en los años 1–5, con el resto de mi NORMAL. Al precio de Sí descuenta −0,8 %. Mi NORMAL crece un 1,5 % y el BUENO un 3,5 %. El precio supera el valor BUENO de las 15 variantes calculadas (el máximo es 88,38, en solo_N2). De los 90,10 €, 31,91 pagan un crecimiento que en mi NORMAL vale 2,02 € (lectura sin la cartera P0).

¿Quién es el tonto? «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). No hace falta que lo sea nadie. Con mi NORMAL, 90,10 equivale a una tasa unos dos puntos más baja que la del motor (≈6,5 % frente a 8,69 %, cálculo mío aproximado) o a un margen que no vuelve a su ciclo. Yo no tengo esa alternativa: «it's your alternatives that matter. That's how we make all of our decisions» (PCA p.114; HIM).

**Tornado (información, no criterio).** Sobre el valor NORMAL, cada palanca mueve:

| Palanca | Variación | Efecto |
|---|---|---|
| ROIC LP | ±5 puntos | 12,67 € |
| Tasa | ±1 punto | 10,56 € |
| Margen | ±2 puntos | 7,36 € |
| Crecimiento | ±2 puntos | 3,52 € |
| S2C | ±0,3 | 2,22 € |
| g | ±0,5 puntos | 0,19 € |

El efecto del ROIC es asimétrico. Hacia abajo (4 %, cerca de g) es grande. Hacia arriba es pequeño, porque la reinversión terminal es g ÷ ROIC con g = 2 %: dos puntos más de ROIC NORMAL suben el valor NORMAL unos 1,6 € (cálculo mío). La tasa no es la palanca más influyente.

**¿Cuentan la misma historia que la fase A?** Sí. Es un fabricante maduro de un envase pesado, con un margen que sigue a la energía, un foso estrecho que la Historia sostiene y un precio que paga más que mi escenario bueno. Estas son las fricciones que encuentro; ninguna cambia el cubo ni la zona:

1. **Rentabilidad marginal.** La fase B escribió ≈13 % (NORMAL), ≈17,6 % (BUENO) y ≈8,4 % (MALO) con las bases heredadas. La hoja calcula 14,7 %, 20,0 % y 9,5 %, porque aplica f = 1,165 al S2C (estructura SR1) y el tipo N1 (22,05 %). Las palancas están bien derivadas: la fase B tenía que elegirlas con la base V6.3. Pero el salto del año 11 del NORMAL (5,7 puntos) pasa de 5 solo por la configuración.
2. **El MALO y su capex.** Su historia cuenta hornos y electrificación sin ventas detrás. Con R1 y ventas por debajo del máximo conservado, B16 = 0,7 no actúa (aviso s2c_inerte), y ese capex solo entra por la reposición λ: 19,9 mm al año, igual en los tres escenarios. Por eso su FCF del año 1 (189,1 mm) supera al del NORMAL (178,0). Si fueran 20 mm más al año durante cinco años, el valor MALO bajaría ~2,2 € y el precio de Sí ~1,0 € (−1,8 %, cálculo mío). Ninguna palanca lo expresa.
3. **Perímetro del margen NORMAL.** Palancas!C15 = 0,18 sale de la media de 2019–2025 de la Historia (F29:L29), que incluye Italia hasta 2022. La media de continuadas de 2020–2025 es 18,55 % (N2), que redondeada da 0,185. Corregirla subiría el precio de Sí de 56,02 a ~56,81 € (+1,4 %, cálculo mío). No cambia el cubo ni la zona y queda bajo el 5 %, así que la dejo y la registro en `celdas_corregidas`. En sentido contrario empujan los 43,1 mm de «Otros» sin explicar.
4. **Los textos de fase C que lleva el libro** (B101, B102, C93, C103, C104, las predicciones, B222 y B223) son los del cierre condicionado. C104 dice «esperar: precio de Sí ≤ 56.02 … objetivo condicionado (provisional)», y B222 dice que la reposición «condiciona» el precio objetivo. Con el protocolo de esta copia, el objetivo no se emite y la acción queda sin fijar (punto 9), así que C104 no corresponde. Los reescribo en el turno 2. No tocan el valor.
5. **C27 = Expandiendo** convive con escenarios que no expanden el margen. La fase A lo explicó: hubo un escalón en 2016–2019 y desde entonces es ciclo. No la cambio.
6. **El valor sin crecimiento (58,19 €)** y «cuánto pagas por crecer» son lecturas con base parcial (sin la cartera P0). Solo sirven de contexto.

## 2. Desviaciones pendientes (G8)

La gramática deja dos desviaciones: el salto del año 11 del NORMAL (5,7 puntos) y el del BUENO (8,0). Las justifico; no muevo palancas.

- **NORMAL (convención).** En los años 1–10, cada euro nuevo rinde 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 %, junto al ROIC de cinco años (13,8 %, Historia C55). La escala regional, que ha sostenido diez años de ROIC por encima del sector (Historia fila 33; Palancas H18, 9,3 %, solo contexto), sigue sirviendo al capital que se reinvierte dentro del plazo del modelo. Desde el año 11, el capital nuevo rinde la tasa (9 %; la del motor es 8,69 %). La ventaja que pierdo es la de añadir capacidad nueva con retorno en exceso en un mercado maduro [ES, PDF p. 55], cuyo competidor más peligroso no conozco (extracto §9). El margen del 18 % sigue sobre el capital instalado. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Con las bases heredadas el salto sería ≈4,0 puntos; el resto lo crea f. La convergencia hacia el coste de capital es un criterio, no una ley (MR; E2).
- **BUENO (fundamentada).** Cada euro nuevo rinde 1,1 × 1,165 × 0,20 × (1 − 0,2205) = 20,0 % porque llena hornos que no iban llenos, suma Brasil y cierra Toro:
  - la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54], y el consumo fue inferior a lo previsto [ES, PDF p. 94];
  - Brasil tiene un 42,4 % de margen EBITDA [ES, PDF p. 107];
  - Toro está firmado, con el cierre condicionado [ES, PDF p. 85].

  Esa ventaja es finita. Con la capacidad libre usada y Toro integrado, el capital nuevo del año 11 rinde el suelo de la meseta de 2018–2025 (11,9 %, 12,5 % y 12,2 %; Historia E33, I33 y J33), tres puntos sobre r. Lo que se pierde en el año 11 es el volumen sin capex, no la ventaja del capital instalado. Sigue por debajo de 2 × C55 (27,7 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

G16 (peso del terminal) y G17 (cuota implícita) no están señalados.

## 3. ¿Hay que mover palancas?

No. Ninguna incoherencia exige números distintos:
- la del margen NORMAL es de perímetro, pero corregirla mueve el precio de Sí un 1,4 % sin cambiar el cubo ni la zona (lo dejo escrito con su cálculo, v2.1);
- la del MALO no tiene palanca que la exprese bajo R1;
- la de la rentabilidad marginal viene de la configuración.

`revisar_palancas = false`. En `celdas_corregidas` dejo Palancas!C15 y B16 con `despues = antes` y su motivo. De la fase A no encuentro ninguna celda que impida sostener la conclusión. El cambio de protocolo no afecta a ninguna palanca: no es un cambio económico.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Mantuve Vigilar, las opciones de B65:D65 y 0,2/0,6/0,2. El cubo lo sostiene la escalera nueva, no la herencia, y cambié lo que la Historia corregía: C62 pasa al motor B, C97 a Neutral y C76 queda vacía. Lo más heredado son las probabilidades. Con 0,25/0,6/0,15, la sustituta que dejó escrita la fase B, el precio de Sí bajaría a 54,10 € (−3,4 %, cálculo mío) y la zona seguiría «caro». Cambio: ninguno.
2. **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 90,10 € y de los 171,8 € de Simply Wall St (C38, posterior a la base). Cambio: ninguno; no bajo r ni subo el NORMAL para acercarme.
3. **Consistencia y compromiso.** La zona es «caro» en las 15 variantes y el precio supera el BUENO de todas. Para cumplir la regla a 90,10 haría falta un NORMAL por encima de 90, un 50 % sobre el mío.

   Además, esta copia hereda una fase C entera que es mi propia conclusión anterior. La revisé como de otro. Rehíce las cifras de materialidad con `configuracion_v64_variantes.md`, el ámbito de cada parámetro, el exceso de capex de 2021–2025 (739,0 frente a 509,6 mm, Historia filas 12 y 8), la escalera (56,02 € con 0,2/0,6/0,2 y 54,10 € con 0,25/0,6/0,15) y las páginas que cito.

   También miré la tentación contraria, la que crea este protocolo: marcar los PM1 como fundamentados para que el objetivo salga emitido, o declarar material el capex por destino para convertir el bloqueo en un dato ausente. Ninguna se sostiene, porque no hay hechos nuevos. Cambio: ninguno en palancas ni en materialidad; solo cambia lo que depende del protocolo.
4. **Historia bonita / viento de cola.** El margen de 2024–2025 coincide con la bajada del gas tras 2022 [ES, PDF p. 56]: es marea. El 42,4 % de Brasil se compró: Vidroporto ya daba 55,5 mm de EBITDA pro forma y costó unas 6,9 veces [ES, PDF p. 36–37]. Lo propio de Vidrala es la vuelta del margen de 2022 a 2024 y diez años de ROIC sobre el sector. Cambio: ninguno en palancas; en la tesis lo atribuiré así.
5. **Optimismo del BUENO frente a la tasa base.** Crece menos que la historia (3,5 % frente al 7,4 % con compras) y su ROIC terminal (12 %) queda bajo C55. Pero en los años 1–10 rinde el 20,0 % por euro nuevo, 1,45 veces C55, y la G7 no lo ve porque usa las bases heredadas (17,6 %). Ese 20 % pide hornos sin llenar que no puedo medir. Cambio: ninguno, porque el BUENO pesa ~0,14 € de precio de Sí por euro de valor; queda en incoherencias y en G8.
6. **Doble castigo.** El NORMAL está al 18 %, el MALO al 15 %, p(MALO) no sube, la quiebra está vacía y la r es la heredada, sin prima. La reposición está en SR1, y la fase B no rebajó S2C ni ROIC por lo mismo. g NORMAL al 2 % no castiga: mueve ±0,19 €. Cambio: ninguno.
7. **Disponibilidad.** Kristin, el cierre de Chile y las recompras de 2026 son posteriores a la base y quedan fuera. El apagón de 2025 la empresa lo da por no material [ES, PDF p. 78]. Los 43,1 mm de «Otros» los medí: como mucho ~0,66 puntos en la media del NORMAL y ~1,9 € de precio de Sí. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad.** El NORMAL (1,5 %) está junto a la proyección de la empresa (1,6 % [ES, PDF p. 55]) y usa su volumen del +1 %. Se sostiene sin la guía:
   - el orgánico de 2025 fue −5,4 % [ES, PDF p. 88];
   - C45 da un 2,9 % con Brasil dentro;
   - las bajadas de precio que supuso en 2023 se cumplieron en lo grueso [CF_2023, PDF p. 48].

   En contra: Iberia (~4,8 %) y Reino Unido (~10,3 %) crecieron en euros en 2020–2025, sobre todo por el precio de la energía. Cambio: ninguno, porque cada punto de crecimiento pesa menos de 1 € de precio de Sí.
9. **¿El MALO es de verdad malo?** Vale 44,32 €, la mitad del precio. Su margen del 15 % para siempre queda por debajo de todos los años salvo 2016, 2017 y 2022, y está un 24 % bajo el valor sin crecimiento. No es un NORMAL maquillado, aunque con R1 libera circulante y su capex de hornos solo entra por λ. Un MALO al 13,7 % de 2022 bajaría el precio de Sí ~2 €. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno.
10. **Lo no numerable.** La concentración de clientes sube: los diez mayores pasan de ~30 % (2019) a ~38 % (2024) y a «algo más del 35 %» (2025), y el percentil 50 baja de 27 a cerca de 20 clientes [CF_2019, PDF p. 67; CF_2024, PDF p. 45; ES, PDF p. 104]. El cliente tiene más poder para quedarse la mejora. Pesan también la cobertura del 69 % de la energía de 2026 [ES, PDF p. 101] y el CO2. Cambio: irá a la tesis inversa y a lo que me haría cambiar de cubo (turno 2).

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Sigo el orden de mando:
- **Bloqueo:** ninguno (gramática sin errores, valor no bloqueado).
- **Límite del modelo:** no (FCF base positivo, no es financiera, el motor B cuadra en las 15 variantes).
- **Descalificador mío:** ninguno (fase A, sección 3).
- **Dato ausente material:** ninguno (punto 6).
- **Fundamento material:** la lista D10 está vacía (punto 7) y con `esperar` no limita.
- **Zona:** caro.

Conclusión provisional: **esperar**, por precio. «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM). Aquí ni siquiera es maravillosa: es buena y cíclica.

Lo que cambia frente al cierre condicionado es lo que el protocolo hace con esa conclusión (punto 9). El precio de Sí depende de la reposición de hornos, que no tiene fundamento suficiente, y con «bloqueo_del_objetivo» ese objetivo no se emite. En el turno 2 el expediente quedará en `pendiente_de_datos` · Vigilar · sin acción · sin precio objetivo, y 56,02 € será un valor calculado condicional, no un objetivo. Lo que sostengo no cambia: a 90,10 € no compraría, y lo que falta para fijar el precio al que sí está nombrado (punto 9).

## 6. Datos ausentes (S-19)

Reviso los 30 de `datos_ausentes.json`; ninguno es material para esperar con objetivo. Los seis de evidencia de la Historia no tocan el valor del motor B o están confirmados en la base por el extracto: arrendamientos de 49,3 mm y minoritarios cero [ES, PDF p. 72 y p. 10]. Lo que más pesa:

- **Cuota y competidores.** Es el hueco mayor y lo que me llevaría a No o a Demasiado difícil, pero no deja el objetivo sin base. Los márgenes de los tres escenarios salen de diez años propios que ya contienen la respuesta de la competencia a un choque de energía completo (13,7 % en 2022, 20,8 % en 2024). Además, el NORMAL no da retorno en exceso al capital nuevo desde el año 11, y el precio supera todos los BUENO calculados.
- **«Otros» ingresos (43,1 mm en 2025 y 26,2 en 2024 [ES, PDF p. 79]).** En el peor caso, si todo fuera no recurrente, el precio de Sí bajaría ~1,9 € (−3,3 %). Aparece los dos años, así que algo es recurrente. «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM) vale también al revés.
- **Capex por destino.** Lo reviso como dato ausente y, por S-19, no es material: la acción no depende de él, porque con λ de 1,10 a 1,25 y todas las estructuras la zona es «caro». La incertidumbre que deja es otra cosa, una hipótesis económica: la reposición de hornos. La registro una sola vez, en la configuración (PM1, punto 9), donde aparece como información que falta. Qué pasa con el objetivo por esa hipótesis lo decide el protocolo, no esta revisión. He precisado la redacción frente al cierre condicionado.
- **Ingresos diferidos.** La diferencia cuadra: 41,117 − 23,115 = 18,002 mm, que son los créditos fiscales por inversiones que incluye el epígrafe [ES, PDF p. 10 y p. 71].

`alguno_material = false`. El `pendiente_de_datos` del turno 2 vendrá del protocolo del objetivo, no de un dato de esta lista.

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B: palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas. Todas son «fundamentada» o «convención» con hechos en el apoyo. Ninguna narrativa es genérica: cada una tiene mecanismo, dueño de la mejora y «qué lo pararía» con páginas. Miré con lupa las más débiles y no las incluyo, por esto:

- **B69:D69 (0,2/0,6/0,2):** es una convención argumentada (no contar dos veces el pico de margen) con hechos de la fila 29. La alternativa escrita (0,25/0,6/0,15) mueve el precio de Sí un −3,4 %.
- **B16 (S2C MALO):** no actúa con R1. Su efecto es nulo; no es material.
- **D16 (S2C BUENO 1,1):** la magnitud sale de la banda del ejercicio y Toro (0,91) va en contra. Pero un S2C BUENO 0,3 más bajo mueve el precio de Sí ~0,4 €: no es material.
- **D66 (la empresa se queda la mejora en Brasil y Chile):** la apoya el margen de Brasil de 2024–2025, no la estructura competitiva, que no conozco. El BUENO mueve poco el precio de Sí.

La lista queda vacía. Con `esperar`, `resultado = no_procede`, la comprobación conjunta no procede y `sobrevive = null`. Los parámetros experimentales sin fundamento suficiente no entran en D10 con `esperar`: condicionan el objetivo por el protocolo (punto 9).

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis fundamentada de la que más depende la conclusión, a mi juicio, es **Palancas!C15: el 18 % del NORMAL es la media de un ciclo que vuelve, no un nivel nuevo**. Es la diferencia entre mi lectura y la del precio, y decide quién se queda la mejora: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM). Dos puntos más (el nivel de 2024–2025) subirían el precio de Sí a ~59,2 € (cálculo mío), todavía lejos de 90,10.

Lo resolvería la serie de 2019–2025 de precio medio y de coste de energía por tonelada en cada segmento, con las cláusulas de traslado de los contratos (pregunta a Relación con Inversores), y la explicación de los 43,1 mm de «Otros». El estado del expediente en esta copia no lo decide C15: lo decide la reposición de hornos (punto 9).

## 9. Configuración V6.4 experimental

**Variantes.** Las 15 calculadas dan «caro», con un precio de Sí de 51,29 a 65,72 € (la activa, 56,02 €). La tabla no es un intervalo de confianza ni prueba robustez frente a hipótesis no exploradas.

**Parámetros** (Δ del precio de Sí con su variante):
- **N1 tipo** (22,05 %, media de 2023–2025 de la fila de tipo impositivo: 20,4 / 21,4 / 24,3 %; lo compruebo) y escudo vinculado: −1,71 € frente al heredado. Fundamentado; no material.
- **N2** (m0 18,55 %): +0,97 €. Fundamentado; no material. Es el margen de partida, no mi objetivo.
- **N3 regla R1:** −1,36 €, solo en el MALO. Va del lado prudente y encaja con hornos específicos que se conservan [ES, PDF p. 168 y p. 94]. El circulante, 14,70 % de las ventas, lo recalculo con el balance [ES, PDF p. 9 y p. 10] y cuadra.
- **PM1.estructura** (SR1): −7,10 € frente a sin requisito. Por estructura, el precio de Sí es S 55,52 · SR1 56,02 · SR2 57,08 · SRF 58,43 · H 61,37.
- **PM1.familia** (Λ): no se aísla; P-M1 entero resta 6,61 €.
- **PM1.parametro** (λ 1,15): de +2,37 € (λ 1,10) a −4,73 € (λ 1,25).

  Estos tres son técnicos, de confianza baja, materiales para el objetivo y **sin fundamento suficiente**: falta el desglose del capex por destino y el coste de reponer hoy un horno frente a su coste histórico.
- Las convenciones de años (−0,13 €) y de terminal (+0,40 €), el ROIC terminal (SR2, +1,06 €) y la cartera P0 (+0,49 €) no son materiales.
- Ninguno es material para la acción: todas las variantes que los varían dan «caro».

**Mantenimiento.** La reposición supera la amortización:
- el capex ha sido de 1,10 veces la amortización o más todos los años desde 2017, y de 1,45 veces en 2021–2025 (739,0 frente a 509,6 mm, Historia filas 12 y 8);
- en 2025 fue de 1,42 veces, con ventas orgánicas −5,4 % y la renovación de hornos como destino principal [ES, PDF p. 50];
- hay 627 mm de inmovilizado amortizado en uso [ES, PDF p. 51].

En contra, en 2019 la empresa suponía que un capex del 8 % de las ventas bastaba para mantener y crecer [CF_2019, PDF p. 44], por debajo de su amortización de entonces; pero es un supuesto del vendedor.

La magnitud no la mido. λ = 1,15 es un tercio del exceso histórico (75,0 de 229,4 mm); todo el exceso daría λ ≈ 1,46. La estructura más coherente es **SR1**, con confianza baja:
- H no encaja: en 2025 el exceso se dio sin crecer;
- S cuenta dos veces, porque C53 ya lleva el exceso;
- SR1 quita del crecimiento justo el exceso histórico por euro de ventas añadido (75,0 ÷ 476,8 = 0,157 €);
- SRF quita unos 0,29 € por euro, más de lo que muestra la historia;
- SR2 corrige un ROIC que en el NORMAL es una convención.

No se adopta nada.

**Avisos de dominio.**
- **Factor de reestimación** (f = 1,165; deja de estar definido en λ ≈ 2,06): explica la G8 del NORMAL. No es material.
- **Terminal R1 sin máximo conservado:** el MALO carga 15,8 mm de inversión para crecer al 1 % con ventas bajo el máximo. Es prudente y no es material.
- **S2C inerte en el MALO:** es la incoherencia 2 del punto 1, ~1,0 € de precio de Sí. No es material.

Las lecturas con bases parciales (G7, referencias mecánicas, valor sin crecimiento sin P0) no las presento como comprobación del modelo experimental. Rehecha con f y N1, la rentabilidad marginal del BUENO es del 20,0 %, frente a 2 × C55 = 27,7 %.

**Objetivo (protocolo `bloqueo_del_objetivo`, ensayo).** Espero por precio. Lo condicionan PM1.estructura, PM1.familia y PM1.parametro, y la lista D10 está vacía. Ningún aviso de dominio es material y ningún dato ausente es material.

La acción se sostiene en las 14 variantes del ámbito (todas «caro», precio de Sí de 51,29 a 65,72 €). Este protocolo no se conforma con eso: no emite un objetivo que depende de información material no disponible. El tratamiento es **objetivo_bloqueado**, con origen `protocolo_de_bloqueo`. Lo que corresponde en el turno 2 es `pendiente_de_datos` · Vigilar · sin acción · sin precio objetivo, con 56,02 € como valor calculado condicional.

La información que falta:
- el desglose del capex de 2021–2025 y de 2026 en adelante por destino (reposición de hornos, crecimiento y descarbonización);
- el coste de reconstruir hoy un horno frente a su coste histórico;
- la utilización y las toneladas fundidas por segmento.

«Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## Cambios frente a la fase C del cierre condicionado

1. **`configuracion_v64.objetivo`:** el protocolo pasa a `bloqueo_del_objetivo`; el tratamiento, a `objetivo_bloqueado`, con origen `protocolo_de_bloqueo`; y el motivo, reescrito. Se conservan las hipótesis que condicionan, la información no disponible, el ámbito (14 variantes) y `accion_sostenida_en_ambito = true`. Es lo único que dicta el protocolo; `objetivo_v64.py` (solo lectura) da el mismo tratamiento y el mismo estado esperado.
2. **Incoherencia 4 de `una_sola_historia` y último semáforo de `lo_que_dice_la_hoja`.** Antes decían que el libro llevaba los textos de la etapa 1 y que el estado técnico era INCOMPLETO. En esta copia el libro lleva los textos de la fase C del cierre condicionado (C104 con «objetivo condicionado»), que ya no corresponden, y el estado es «COMPLETO Y VÁLIDO». Es un hecho de la copia, no un juicio nuevo.
3. **Revisión de datos ausentes, entrada del capex de 2026 por destino:** sigue siendo no material. Solo precisé la redacción, como pedía el aviso del punto 16 de la auditoría anterior: es un dato ausente no material por S-19, y la hipótesis sin fundamento (PM1) se registra aparte y una sola vez.
4. **Autocomprobación, «consistencia y compromiso»:** añadí la revisión de la fase C heredada y de la tentación que crea este protocolo. Las otras nueve entradas no cambian.
5. **Evaluación de PM1.estructura:** una frase sobre su papel con este protocolo. La materialidad, el fundamento y el ámbito no cambian.
6. **No cambio ningún otro juicio:** ni palancas, ni `celdas_corregidas`, ni las desviaciones G8, ni D10 (lista vacía), ni la materialidad de los parámetros, ni el mantenimiento (SR1), ni los avisos de dominio, ni el cubo provisional (Vigilar), ni la conclusión provisional (esperar). Los campos del turno 2 van a `null` (`escalera` y `confianza_global` también, porque son del cierre).

## 10. Turno 2 · conclusión

**Comprobación conjunta.** No se ejecutó, porque no procedía con `esperar`. No hay `comprobacion_conjunta.json`, así que `sobrevive` queda `null` y `resultado = no_procede`.

**Estado: pendiente de datos · cubo Vigilar · sin acción · sin precio objetivo.**
- No hay bloqueo, ni límite del modelo, ni descalificador.
- Ningún dato de `datos_ausentes.json` es material (S-19) y la lista D10 está vacía.
- La zona es «caro» y la conclusión provisional era esperar por precio.

Lo que me impide cerrar es el objetivo. El precio de Sí calculado (56,02 €) depende de la reposición de hornos (PM1.estructura, PM1.familia y PM1.parametro), que no tiene fundamento suficiente. Con el protocolo experimental «bloqueo_del_objetivo» (ensayo, no adoptado), un objetivo así no se emite. El tratamiento es `objetivo_bloqueado`, con origen `protocolo_de_bloqueo`.

La acción se sostiene en las 14 variantes calculadas: todas «caro», con un precio de Sí de 51,29 a 65,72 €. Ese rango es el de la tabla de variantes, no un intervalo de confianza, y no cubre hipótesis no exploradas. Este protocolo no se conforma con eso: a 90,10 € no compraría, pero no digo a qué precio sí mientras falte el capex por destino.

C104: «Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de datos: objetivo bloqueado por el protocolo experimental; …) · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento pendiente de datos · 56.02 es valor calculado condicional, no objetivo; …». La posición es de José Luis. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

C93 = Sí. g es del 2 %, por debajo de la tasa sin riesgo (2,85 %); la reinversión terminal es del 22 % con ROIC 0,09; el peso del terminal es del 48 %. El salto del año 11 es la convención del capital nuevo a la tasa.

C103 = No. Es cíclica, con un margen ligado a la energía y un foso estrecho: es una propiedad del negocio.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil, con clientes repartidos (ninguno por encima del 10 % [ES, PDF p. 104]) y diez años de ROIC por encima del sector (13,8 % frente al 9,3 %; Historia C55, Palancas H18). Leo que gana porque fabrica cerca del cliente y traslada la energía con retraso: el margen cayó al 13,7 % en 2022 y volvió al 20,8 % en 2024 (Historia I29, K29). El 19,9 % de 2025 está junto al máximo, con el gas a la baja, y la empresa supone bajadas de precio en 2026 [ES, PDF p. 54]. Mi NORMAL lo deja en el 18 %, y desde el año 11 el capital nuevo rinde la tasa. A 90,10 € pago más que mi BUENO (78,52 €). Vigilar sin conclusión: el precio de Sí que calculo (56,02 €) depende de una reposición que no puedo fundar, y no lo doy como objetivo.

**Tesis inversa (B102).** Defiendo el No con hechos:
- es un producto poco diferenciado en un mercado maduro [ES, PDF p. 55], con consumo inferior a lo previsto y capacidad que se adapta [ES, PDF p. 94], y ventas orgánicas −5,4 % [ES, PDF p. 88];
- el margen es energía barata camino del cliente [ES, PDF p. 54 y p. 56], con 2,9 puntos de «Otros» que nadie explica [ES, PDF p. 79];
- los hornos se comen la caja: capex de 1,42 veces la amortización con ventas a la baja (Historia L12 y L8), 627 mm amortizados en uso y 66,6 mm comprometidos [ES, PDF p. 51];
- los clientes ganan fuerza: los diez mayores pasan de ~30 % a ~38 % en 2019–2024 [CF_2019, PDF p. 67; CF_2024, PDF p. 45];
- el crecimiento se busca donde no hay foso probado: el real cayó un 20 % en 2024, la deuda va a CDI y Toro venía con plan de ajuste [ES, PDF p. 106, p. 105 y p. 85];
- en 2016–2017 el ROIC era la tasa (Historia C33:D33);
- no hay ningún competidor con nombre.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Los dos errores.** Sigo más cerca de pagar cualquier cosa por calidad: el precio paga más que mi mejor escenario. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 12. Predicciones (dado el NORMAL; autopsia el 31-mar-2028)

1. **Margen operativo de 2027 entre el 16 % y el 20 %.** Probabilidad 0,7: cinco de los siete años de 2019–2025 cayeron ahí (Historia F29:L29).
2. **Ventas orgánicas de 2027 entre −2 % y +4 % frente a 2026.** Probabilidad 0,65: el NORMAL crece un 1,5 %, pero el precio de la energía ha movido mucho las ventas (Historia fila 28).
3. **Capex de 2027 por encima de 1,2 veces la amortización.** Probabilidad 0,7. Pone a prueba la reposición, que es lo que bloquea el objetivo: seis de los últimos nueve años lo superaron (Historia filas 8 y 12), y 2025 tuvo menos hornos que 2024 [ES, PDF p. 180].

Son la autopsia del análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 13. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo de 56,02 € sin que cambie el negocio y con la reposición fundada por el desglose del capex. Por debajo de 51,29 € la zona cumpliría la regla en todas las variantes calculadas, pero la compra seguiría exigiendo que los PM1 entren en la comprobación conjunta y la superen.
- **A No:** un margen bajo el 14 % sin choque de energía; dos años más de capex por encima de 1,4 veces la amortización con ventas planas y el ROIC hacia la tasa; o datos de cuota que muestren pérdida.
- **A Demasiado difícil:** que el valor pase a depender de Brasil y Chile, con su divisa y su deuda; un exceso de capacidad duradero de los competidores; o una sustitución del vidrio que no sepa juzgar.

B222 nombra Palancas!C15 (el 18 % del NORMAL como media de un ciclo que vuelve), la hipótesis fundamentada de la que más depende la acción, y la reposición de hornos (Configuración V6.4!B36:B38), que es lo que deja el expediente sin conclusión.

B223 pide a Relación con Inversores:
- el desglose del capex de 2021–2025 y de 2026 en adelante por destino, con el coste de reconstruir hoy un horno y la utilización por segmento (esto desbloquearía el objetivo);
- el precio y el coste de energía por tonelada en cada segmento, con las cláusulas de traslado;
- el desglose de los 43,1 mm de «Otros».

## 14. Comparación con la etapa 1

El cubo es el mismo, Vigilar, y por la misma razón; el cierre no.
- **Cierre:** la etapa 1 concluía esperar hacia ~48 €; aquí el precio de Sí calculado es 56,02 €, pero no se emite como objetivo, y el expediente queda pendiente de datos.
- **Regla:** se pasa del mínimo del MALO y ¾ del ponderado a la escalera k = 3, que queda por encima del MALO (44,32).
- **Modelo:** motor B con palancas.
- **Configuración experimental:** resta 8,73 € frente al modo heredado (64,75) por la reposición, el tipo y R1.

Mi NORMAL (60,21 €) está por debajo del valor normal de la etapa 1 (~74 €): el margen va a la media del ciclo y el capital nuevo rinde la tasa desde el año 11. La etapa 1 usaba hechos posteriores a la base; yo no. Mantengo C93 y C103 y reescribo B101, B102 y C104 (este sin porcentaje).

## Cambios del turno 2 frente al cierre condicionado

1. **Estado y decisión:** `estado_analisis = pendiente_de_datos`, cubo Vigilar, `decision.accion` y `precio_objetivo` = `null`. Antes era `concluido · esperar · 56,02`. Es lo que corresponde a `objetivo_bloqueado` con origen `protocolo_de_bloqueo`; `objetivo_v64.py` (solo lectura) da lo mismo.
2. **C104:** «sin conclusión (pendiente de datos: objetivo bloqueado …)», con la etiqueta «fundamento pendiente de datos» y 56,02 como valor calculado condicional. B101 termina sin objetivo. B222 y B223 nombran la reposición como lo que deja el expediente sin conclusión y el capex por destino como lo que lo desbloquearía. Se reescriben con ellos sus Observaciones (C104, B101) y su herencia (C104, B101).
3. **Insumos y condiciones:** `insumos_decision_cartera.fundamento`, `decision.condiciones_revision`, `cambiaria_de_cubo.a_si`, `comparacion_etapa_1.por_que_difieren` y la nota de `escalera` se reescriben con el mismo motivo.
4. **Sin cambios:** C93, C103, B102, las tres predicciones con sus fechas y probabilidades, el resto de Observaciones y de la herencia, `confianza_global` (media) y todo el turno 1.
