# Ahold Delhaize (AD) · fase C · turno 1 · 2026-11-19

## 1. Una sola historia

Lo que calcula la hoja con mis 52 celdas (resultados.json, precio.json):

- Valor por acción MALO 28,47 · NORMAL 40,68 · BUENO 50,44; ponderado 40,19 (C83). Precio 36,05 (C37, 13-nov-2026). Precio de Sí 36,84, que es P\* porque queda por debajo del NORMAL. Zona `cumple_regla_k`. El precio está 0,79 € por debajo del precio de Sí: un 2,2 % del precio (diferencia ÷ precio). El precio del escenario MALO está un 21 % por debajo del precio (diferencia ÷ precio). La regla antigua (C156) da 28,47.
- DCF inverso: con el resto del NORMAL, el precio actual descuenta un crecimiento de ventas del −1,25 % anual en los años 1–5 y el precio de Sí uno del −0,45 %. La tabla es monótona (B193 pasa) y el tope del NORMAL no actúa.
- Peso del terminal: 42 % / 51 % / 56 %. No salta G16 ni el semáforo de la fila 44.
- Salto del año 11: 1,8 / 6,0 / 7,1 puntos. La rentabilidad marginal es 10,8 % / 16,0 % / 19,1 % y el ROIC terminal 0,09 / 0,10 / 0,12. G8 salta en el NORMAL y en el BUENO (punto 2).
- Valor sin crecimiento: 34,70 en los tres escenarios. Pago 1,35 por crecer y el crecimiento del NORMAL vale 5,98. En el MALO el crecimiento destruye 6,23 porque el margen baja al 3 %.
- Tornado, solo como información: el margen (±2 puntos) mueve 19,67 €, el 48 % del ponderado. Le siguen la tasa (±1 punto) con 6,80, el ROIC terminal (±5 puntos) con 5,26, el crecimiento con 2,57, g con 0,49 y el S2C con 0,25. La tasa no es la palanca más influyente: no hay aviso A5.
- Estado técnico INCOMPLETO solo porque faltan las predicciones de la fase C, sin bloqueo (B252 y B254 falsos). El veredicto de la hoja (A6) es «DESCARTADA POR FILTRO PABRAI» por C13 = No. La lectura de precio de la hoja (B267) es «asimetría débil». Ni el veredicto ni esa lectura son mi decisión.

¿Cuentan la misma historia que la fase A? En lo grande, sí. Es un supermercado maduro con un foso local estrecho. El ahorro se va al cliente y el margen ronda el 4 %. El valor depende casi entero del margen y de cuánto dura un exceso pequeño sobre r. Pero la fase A cerró con «el precio no da margen hoy» (C13 = No, unas 15,3 veces el FCF frente a una mediana de 12,5). La hoja dice ahora que el precio cumple la regla k por 0,79 €. Ese colchón es más pequeño que cada una de estas incertidumbres:

1. **Probabilidades (B69:D69).** La fase B mantiene 0,2/0,6/0,2 y dice que las colas pesan parecido. Para la cola mala cuenta años de margen NIIF ≤ 3,2 % (2016, 2020, 2023, 2024: cuatro de diez). Para la buena cuenta años de margen subyacente ≥ 4,4 %. Son medidas distintas. El margen objetivo del BUENO (4,5 %) es NIIF, y en NIIF nunca se ha alcanzado (máximo 4,39 %, C51). Medida igual a los dos lados, la serie no sostiene la simetría. La propia Observación de B69 dice «cuatro de diez» y lo deja en 0,2. Lo que queda en pie es la convención y el argumento de no contar dos veces el riesgo (PA; E6, extendido como convención del ejercicio). Por eso va a `hipotesis_sin_fundamento` (punto 7). Con 0,25/0,6/0,15 el precio de Sí sería 35,55 y con 0,3/0,6/0,1 sería 34,42. Los dos quedan por debajo del precio.
2. **Margen NORMAL (C15 = 0,04).** Lo sostienen hechos NIIF: el margen de 2025 (3,84 %, C48) y la media de 2021–2025 (3,78 %) redondean a 0,04. Es fundamentado. Pero la fase A dijo que los cargos se repiten y son gasto: «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM). Si resto al subyacente actual (4,0 %, Q3-2026 p. 3) la media de cargos de 2021–2025, que es la diferencia entre el subyacente (AR2025 p. 64) y el NIIF de la fila 29, unos 0,38 puntos, sale 3,62 %. Eso redondea a 0,035. La cifra está a 0,13 puntos de la frontera de redondeo (3,75 %). El apoyo «el subyacente está en 4,0 %» no añade nada a un objetivo NIIF. Se resuelve con palabras: la celda se queda, pero es la hipótesis fundamentada de la que más depende la zona.
3. **La caja de partida del motor (dato, no palanca).** El flujo sin crecimiento es 2.770 (motor_a_f1_resultado.md, K3): el FCF base de C52 (2.312, media de 2023–2025) más el nivel del EBIT de 2025 y la reinversión de la ventana. La nota de C46 y C47 en datos_v63 dice que esa ventana incluye la devolución fiscal belga de +367 de 2023. El pago de unos 380 de 2021 queda fuera de la ventana. La calibración de f trata como permanentes unos 122 al año que no se repiten. A perpetuidad sin crecimiento son unos 1,5 € por acción en los tres escenarios, el doble del colchón. No recalculo celdas de datos ni cambio la base del FCF: lo digo aquí y en la ficha. La ventana es la que fijó la orquestación (C57 = 3).
4. **El precio.** 36,05 viene de una fuente secundaria (Trivano, 13-nov-2026) y está pendiente de fuente oficial (alcance_v2.json). El 30 de octubre cotizaba a 32,75. Un precio oficial por encima de 36,84 cambia la zona.

No veo ninguna palanca mal derivada. La aritmética de la rentabilidad marginal coincide con la hoja. El S2C está anclado en el perímetro propio y no en C54. El ROIC terminal del MALO igual a r no es un error de perímetro. Dos lecturas que no son incoherencias. El semáforo de la fila 42 marca el BUENO («19 %, más del doble de su historia») porque compara con 2 × C55, que es de todo el capital. Con F1 en A2_propio manda G7 con 2 × 14,82 % = 29,6 %, y no salta (datos_v63 §1 bis, límite declarado). Y la fase B atribuye 1,8 puntos del salto del año 11 a la medida (intereses de arrendamiento). No me apoyo en eso: justifico el salto entero como hipótesis de pérdida de ventaja.

No pido revisar palancas. Lo de las probabilidades no es un error de cálculo: es una convención sin un hecho que la sostenga, y el procedimiento para eso es D10. Lo del margen se sostiene con hechos NIIF. Lo de la caja es un dato. Ninguna de las tres cosas se arregla moviendo otra palanca: compensar un dato con una palanca sería maquillar.

## 2. Desviaciones pendientes (gramática tras el recálculo)

- **G8 · NORMAL (6,0 puntos).** En los años 1–10, cada euro propio nuevo (reformas, centros de distribución, automatización) rinde como el capital propio de hoy. Son 5,1 × 0,04 × (1 − 0,214) = 16,0 %, frente al 16,15 % sin arrendamientos de 2025 y el 14,82 % de media (§1 bis). La densidad local aguanta: Albert Heijn lleva siete años ganando cuota (AR2025 p. 50) y Food Lion 53 trimestres de comparables positivas (AR2025 p. 43). Desde el año 11 el exceso sobre el capital nuevo se estrecha a un punto sobre r. El ahorro se reinvierte entero en precio (1.294 en 2025 y 1.354 en 2024, AR2025 p. 45), hay 1.000 M$ comprometidos en precios hasta 2028 (AR2025 p. 22) y la presión de los competidores de descuento se intensificó (AR2025 p. 69, 77). El retorno pagado todo el alquiler ya bajó al 10,67 % en 2024 (§1 bis). La plantilla hace caer la ventaja de golpe en el año 11; en la realidad sería gradual. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **G8 · BUENO (7,1 puntos).** En los años 1–10 el BUENO se queda parte del ahorro: marca propia por encima del 40 % (Q2-2026 p. 4) y Europa del 3,3 % al 3,8 % de margen subyacente en 2023–2025 (AR2025 p. 49). Son 5,4 × 0,045 × 0,786 = 19,1 %. Después, el exceso a perpetuidad no pasa de tres puntos sobre r (MR; E2). El pico de 2021–2022 (14,2–14,8 % pagado el alquiler, con márgenes NIIF del 4,3–4,4 %) bajó al 10,7–11,5 % en cuanto el margen volvió al 3,1–3,2 % (§1 bis; fila 29). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

G16 y G17 no aparecen: el peso del terminal está por debajo del 75 % y la cuota implícita no se calcula porque C24 está vacía.

## 3. Palancas

`revisar_palancas = false`. No cambio ninguna celda. Reviso C18 (foso), C62 (motor), C15 (margen NORMAL) y B69:D69, y en `celdas_corregidas` dejo después = antes con el motivo. C18 sigue en Sí, estrecho, con la vara P-FOSO: 13,03 % de media frente a r, y el peor año 10,67 %.

## 4. Autocomprobación

Está en el JSON, una entrada por tendencia. Lo que cambia: B69:D69 pasa a la lista de hipótesis sin fundamento (por las tendencias 1, 4 y 5), y C15 y la caja de partida quedan escritos como lo que más condiciona la zona (por las tendencias 8 y 10). Ninguna palanca se mueve. Antídoto: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM).

## 5. Cubo y conclusión provisionales

En el orden de mando, no hay bloqueo (0 errores y 0 límites en la gramática, B252 y B254 falsos). No hay límite del modelo: el motor A vale con F1 en A2_propio, aunque F1-SERIES siga pendiente en tres años de la serie de amortización (motor_a_f1_resultado.md). No tengo descalificador (fase A, sección 3). Ningún dato ausente es material (punto 6). Llego al fundamento material con la zona en `cumple_regla_k`. Por el orden de mando, la conclusión provisional es **`comprar`** y el cubo provisional **Sí**. Es la regla, no mi lectura del negocio: un Sí por 0,79 € no resiste la primera duda razonable, y las de arriba ya son cuatro. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM). La comprobación conjunta decide.

## 6. Datos ausentes (S-19)

Reviso los 29, uno a uno, en el JSON. Ninguno es material para la conclusión favorable. Los dos ceros pendientes de verificación tienen apoyo en el extracto. Los arrendamientos de 2016–2017 son anteriores a la NIIF 16, y ninguna ancla de las palancas usa esos años. Los minoritarios son cero en resultados (AR2025 p. 212, 213) y en el balance del 3T de 2026 (Q3-2026 p. 14). Lo que más pesa son los competidores no nombrados y la definición de la cuota. Pero su efecto ya está en la serie de márgenes que ancla el MALO: 3,1–3,2 % NIIF en 2023–2024 con la presión intensificada (AR2025 p. 69, 77). Además, el borde del círculo ya está declarado en C12. Lo que me impide concluir no es un dato ausente: es fundamento (punto 7).

## 7. Fundamento material (D10)

La única hipótesis material sin fundamento suficiente es **B69:D69**: la convención 0,2/0,6/0,2 con un argumento que mezcla medidas. Las demás palancas citan hechos de la empresa que sostienen la cifra: la fila 28, la fila 29, la §1 bis y las páginas de los informes. También las narrativas (mecanismo y «qué lo pararía» con páginas), C8, C62, la quiebra y C76.

Alternativas defendibles, cada límite atado a un hecho:

- **p(MALO) ∈ [0,2; 0,3].** Suelo 0,2: dos de diez ejercicios (2023 y 2024) tuvieron el mecanismo del MALO, con inversión en precios y costes por encima de la inflación minorista (AR2025 p. 18, 45). En esos años el margen NIIF estuvo al nivel del MALO (3,21 % y 3,12 %, fila 29). Techo 0,3: añado 2016, con un margen NIIF del 3,19 % y el subyacente más bajo de la serie (3,8 %, AR2025 p. 64). No cuento 2020: su NIIF del 2,93 % se debe a cargos de 1,9 puntos en el año de subyacente récord (4,8 %), y no fue una compresión de margen.
- **p(BUENO) ∈ [0,1; 0,2].** Techo 0,2: dos de diez ejercicios (2021 y 2022) tuvieron un margen NIIF al nivel del BUENO (4,39 % y 4,33 %). Suelo 0,1: esos dos años son anteriores al compromiso de 1.000 M$ en precios de 2025–2028 (AR2025 p. 22), que cubre al menos tres de los cinco años del horizonte y empuja contra el mecanismo del BUENO. Desde entonces el ahorro se ha ido entero a precio (AR2025 p. 45).
- **p(NORMAL)** es el resto: [0,5; 0,7].

Todas tienen base, así que la comprobación conjunta procede, con una sola combinación: **B69 = 0,3 · C69 = 0,6 · D69 = 0,1**. La historia adversa es que la inversión en precios de 2025–2028 y la presión de descuento hacen más frecuentes los años como 2023–2024 y menos los de 2021–2022. Lo que gana el MALO lo pierde el BUENO, y el NORMAL se queda con el 60 %. No toco la severidad, la r ni la quiebra: el riesgo se cuenta una vez, en la probabilidad. Los tres valores están en la lista y suman 1. El BUENO no supera al MALO. Por mi cuenta aritmética con los valores actuales, el precio de Sí bajaría a unos 34,4 y el ponderado a unos 38,0. Con el precio de 36,05 la zona sería `vigilar`. Lo confirma o no el script: `sobrevive = null` hasta el turno 2.

## 8. Lo que más condiciona y qué lo resolvería

La hipótesis que más condiciona es **B69:D69**. La resolverían los márgenes NIIF y subyacente de 2026 y 2027, con el desglose de deterioros y reestructuración y el destino del ahorro de Save for Our Customers. Están en el informe anual de 2026 (3-mar-2027; resultados el 17-feb-2027, Q3-2026 p. 31) y en el de 2027. Si con la inversión en precios en marcha el margen NIIF se queda en el 3,8 % o más durante dos ejercicios, la cola mala pierde peso. Si vuelve al 3,1–3,2 %, la gana. La pregunta a Relación con Inversores: qué parte del ahorro acumulado de 5.000 M de 2025–2028 (AR2025 p. 22) está prevista para el margen y qué parte para el precio. Aparte, y sin que sea mi hipótesis, la conclusión depende de dos cosas que no son palancas. Una es la caja de partida: una ventana del FCF base sin la devolución fiscal belga, o de cinco años, en la que el pago de 2021 y la devolución de 2023 se compensan. La otra es el precio con fuente oficial.

# Turno 2 · 2026-11-19

## 9. Comprobación conjunta y conclusión

La copia de prueba con B69 = 0,3, C69 = 0,6 y D69 = 0,1 se recalculó con recálculo forzado y no dio errores de gramática (comprobacion_conjunta.json). Los valores por escenario no cambian (28,47 / 40,68 / 50,44). El ponderado baja a 37,99 y el precio de Sí a 34,42. El precio actual, 36,05, queda en la zona `vigilar`: **`sobrevive = false`**. La conclusión favorable depende de unas probabilidades que no puedo sostener con hechos. Por el orden de mando, en el turno 2 la conclusión fue **`pendiente_de_investigacion` · cubo Vigilar · sin acción**. Tras la respuesta al contradictor (sección 14), O1 no rebatida la baja un escalón: **`concluido` · Vigilar · `esperar`**, con una condición que no es de precio. La condición es que la caja de partida se mida sin la devolución fiscal belga de 2023 (AR2023 p. 232) y que la escalera resultante siga dejando el precio por debajo del precio de Sí. El resultado es `fundamento_material.resultado = no_procede` y el precio objetivo es null, porque precio.json da `cumple_regla_k`. El rango del precio de Sí entre la combinación adversa y las palancas centrales es 34,42–36,84. No es un intervalo de confianza: es lo que dan los rangos que encontré defendibles.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 36.84 · zona cumple_regla_k · precio de Sí ≤ 36.84 · precio esc. MALO 28.47 · ponderado 40.19 · fundamento no procede (conclusión no favorable)». El tamaño de la posición, incluido el cero, es de José Luis.

C93 = Sí. g = 2 % es la de un supermercado maduro y reinvierte el 20 % con un ROIC de 0,10. El terminal pesa el 51 %. El salto del año 11 es mi hipótesis escrita. C103 = No: no es un negocio para no vender nunca, con un margen del 3,8 %, un ROIC de todo el capital por debajo del sector y marcas en reparación.

## 10. Tesis

Ahold Delhaize vende comida a 77 millones de clientes por semana con un margen NIIF del 3,84 % y reparte unos 2.000 millones al año. Su foso es la densidad local: estrecho pero real con la vara del accionista (13,0 % pagado el alquiler frente a r 9 %), y sin ventaja frente al sector con todo el capital (8,8 % frente a 10,1 %). El ahorro se va al cliente, así que el valor depende de que el margen aguante en torno al 4 % y de cuánto dura un punto de exceso sobre r. El precio cumple la regla por 0,79 €. Con unas probabilidades más cargadas al MALO, que los hechos defienden igual de bien, deja de cumplirla. Dos ejercicios con la inversión en precios en marcha dirán qué cola pesa más.

## 11. Tesis inversa

No hay poder de precio: 1.354 y 1.294 de ahorro reinvertidos en precio (AR2025 p. 45), 1.000 M$ más hasta 2028 (AR2025 p. 22), y el subyacente ha bajado del 4,4 % al 4,0 % (AR2025 p. 64). Con todo el capital no gana más que el sector (Historia!C55 frente a Palancas!H18), y el retorno pagado el alquiler cayó al 10,7 % en 2024. La caja no crece: la guía de 2026 es de unos 2.100 tras 2.600 (Q3-2026 p. 2, 9), y la base de la valoración lleva dentro una devolución fiscal belga que no se repite. La estructura es rígida: 85 % arrendado, 11.974 de pasivo y unos 35.000 en prórrogas (AR2025 p. 58, 271, 272). Las holguras de deterioro son justas (AR2025 p. 238), llega una compra de unos 1.700 con arrendamientos (Q3-2026 p. 30) y la deuda neta sube a 16.087 (Q3-2026 p. 24). Además, el precio paga 15,3 veces el FCF frente a una mediana de 12,5 (C40, C88). Si el margen vuelve al 3,1–3,2 %, el valor se acerca a 28,47. Lo que me impide firmar el No es la cuota del 38,2 % (AR2025 p. 50), la red y una deuda que no mata (AR2025 p. 55).

## 12. Predicciones (dado el NORMAL)

1. Margen operativo NIIF del Grupo de 2027 ≥ 3,5 % (informe anual 2027; comprobación el 2028-03-31; probabilidad 0,75).
2. Ventas comparables sin gasolina del Grupo de 2027 entre el 0,5 % y el 3,5 % (2028-03-31; 0,7).
3. Flujo de caja libre de 2027 con la definición de la empresa ≥ 2.000 millones (2028-03-31; 0,65).

## 13. Incertidumbre pendiente, qué cambiaría el cubo y etapa 1

B222 son las probabilidades B69:D69. B223 son los márgenes NIIF y subyacente de 2026–2027 con el desglose de cargos y del ahorro (resultados del 17-feb-2027 e informe anual 2026 del 3-mar-2027, Q3-2026 p. 31), más la pregunta a Relación con Inversores sobre cuánto de los 5.000 M de ahorro va al margen.

- A Sí: dos años de margen NIIF del 3,8 % o más con el ahorro retenido en parte, una caja de partida sin la devolución belga que siga cumpliendo la regla y un precio de fuente oficial.
- A No: el retorno pagado el alquiler por debajo de r dos años, un margen NIIF por debajo del 3,0 % o deterioros grandes en Profi, Stop & Shop o Giant Food.
- A Demasiado difícil: compras que cambien el perímetro hasta que la Historia deje de describir el negocio, o una competencia de descuento que haga el margen imposible de acotar con lo que se publica.

La etapa 1 fue Vigilar con un precio de Sí de unos 23 €, su suelo de FCF a −2 % anual, con un FCF de 1.821 y un precio de 33,14. La V6.3 llega a Vigilar con un precio de Sí de 36,84 por la regla espejo (C40 = 2.096), las palancas y la escalera k = 3. El motivo también cambia. La etapa 1 decía «está por encima de mi suelo». Yo digo que el precio cumple la regla, pero que la conclusión depende de unas probabilidades sin hecho que las sostenga. Del diagnóstico cualitativo de la etapa 1 conservo lo que la evidencia sostiene: no hay poder de precio, la estructura es rígida y el foso es estrecho.

## 14. Respuesta al contradictor

| Objeción | Respuesta | Dato | Efecto |
|---|---|---|---|
| O1 (baja). La caja de partida lleva la devolución fiscal belga de 382 de 2023 y, sin ella, el precio de Sí central es 34,75 (35,28 a 33,56) | **No rebatida**. El hecho es cierto y yo mismo lo señalé en el turno 1 | AR2023 p. 232 (cuenta a cobrar de 382, recuperada en mayo de 2023); nota de C46 en datos_v63 §2 | Un escalón a la baja: de «pendiente de investigación» a «concluido · Vigilar · esperar», con una condición que no es de precio. No baja a No |
| O2 (sube). Llevar el valor a la fecha del precio sube el precio de Sí entre 1,0 y 1,5 € | **Rebatida**. Es actualizar la valoración a 2026, y eso contradice la decisión humana P-O2 (a). La versión «al revés», que deflacta el precio, es la misma actualización | datos_v63 §2, nota de C55: «no es una valoración actualizada a 2026»; la escalera es la de precio.json | Ninguno. El desfase queda como aviso A3 para José Luis |
| O3 (sube). 2016 no es comparable: con 2016 ajustado, el techo de p(MALO) es 0,2 y la combinación adversa da 36,15 | **Rebatida en su dirección**. Acepto el hecho: mi techo de 0,3 se apoyaba en 2016 y mi §6 se contradecía. Pero la empresa no publica un 2016 reexpresado. Con los ocho años comparables, 2018–2025, el MALO pesa 2/8 = 0,25 y la combinación adversa 0,25 / 0,65 / 0,1 da 35,23, por debajo de 36,05 | AR2025 p. 64 (cifras anteriores a 2018 no comparables por la NIIF 16); Historia fila 29 | Ninguno al alza. Queda anotado que el techo corregido es 0,25 |

Regla de movimiento: solo O1 es válida y no está rebatida, así que la conclusión baja un escalón. La conclusión final es **concluido · Vigilar · esperar**, sin precio objetivo porque precio.json da `cumple_regla_k`. La condición es la de arriba más los márgenes NIIF de 2026–2027, que acoten B69:D69. «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM).
