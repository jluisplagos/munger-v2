# Zoetis Inc. (ZTS) · fase C · turno 1 · motor A · r = 0,09

Fuentes abreviadas como en `fase_a.md`. Reviso la fase A y la B como si fueran de otro: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Las cifras marcadas «estimación auxiliar» salen de una réplica mía del motor A (en el scratchpad, fuera de esta carpeta) que reproduce B78:D78 (62,07 / 80,52 / 105,88) y el precio de Sí de `precio.json` (73,31) al céntimo; sirven para medir sensibilidades, no sustituyen a la hoja ni a la escalera.

## 1. Una sola historia

Lo que calcula la hoja: MALO 62,07, NORMAL 80,52, BUENO 105,88, ponderado 80,06. Precio 73,08. Precio de Sí 73,31 (sin tope del NORMAL), zona `cumple_regla_k`: el precio está un 0,3 % por debajo del precio de Sí (diferencia ÷ precio de Sí) y un 15,1 % por encima del precio del escenario MALO (diferencia ÷ precio). Peso del terminal 0,43 / 0,52 / 0,58. DCF inverso: el precio descuenta un 0,9 % anual de ventas en los años 1–5 con el resto del NORMAL; el valor sin crecimiento es 64,97 y pago 8,11 por un crecimiento que en mi NORMAL vale 15,55. Tornado: la tasa de descuento (±1 punto) mueve 14,29 por acción; el valor depende sobre todo de la r exigida, que es heredada (A5). Es información, no criterio.

La historia de la fase A se sostiene: una calidad de diez años cuya duración se pone a prueba, a un precio que no da margen a ojo. La hoja lo confirma con una precisión incómoda: el margen existe solo por la regla k = 3 y por 0,23 de colchón. A6 dice «DESCARTADA POR FILTRO PABRAI» por C13 = No; no es mi cubo, porque C13 dice que el valor no se ve sin modelos, no que el negocio sea malo.

Incoherencias revisadas (detalle en `fase_c.json`), ninguna obliga a mover palancas:

- La fase A cita `C55` como 27,7 %; es 23,6 % (con la I+D capitalizada, Historia fila 36). No cambia C18.
- B66 dice que el margen del MALO «vuelve hacia su media» y la fase B pone 0,32, por debajo. La cifra es más dura que la frase; el mecanismo (mezcla y rebajas [10-Q 2T26, PDF p. 35; conferencia 2T26, PDF p. 12]) es el mismo.
- B69 dice que la pérdida continua es «tan plausible» como la de una vez, pero le da 0,3 frente a 0,7. La frase exagera; la cifra se sostiene con lo medido: dermatología −10 puntos y Simparica Trio −1 [presentación 2T26, PDF p. 6–7].
- C17 = No frente a un NORMAL del ≈5 % desde 2027: por componentes (precio de 1–3 puntos, lanzamientos de 2–5; extracto, sección 4) no necesita viento, pero depende de que sigan los lanzamientos.
- Perímetro de la I+D: con C9 = Sí, `C53` cuenta la I+D neta como reinversión y los márgenes objetivo son EBIT publicado, así que la I+D neta del crecimiento pesa dos veces. Es convención de la plantilla («solo cambia las anclas»), no una palanca mal derivada; la mido igual: con S2C sin I+D (0,8 / 1,0 / 1,3) el precio de Sí pasaría a ≈74,12 (+1,1 %), misma zona y mismo cubo (estimación auxiliar). Cumple la regla v2.1 y va contra la tesis: no pido revisión.

## 2. Desviaciones pendientes

`gramatica.md` deja pendiente G8 en los tres escenarios; G16 no salta (peso del terminal ≤ 0,58) y G17 no se puede calcular (C24 vacía).

- **MALO (convención).** ROIC terminal = tasa del motor. El salto de 15,4 % a 9 % dice que en el año 11 se acaba la exclusividad efectiva, como con Draxxin (−66 % en EE. UU. [10-K 2025, PDF p. 42]). Con ventas planas apenas mueve el valor.
- **NORMAL (fundamentada).** De 22,4 %, el retorno de la cartera de hoy (22,8–25,5 % en 2021–25, Historia fila 36), a 11 %. Lo que se pierde es la ventaja de patente de Simparica y Apoquel (28 % de los ingresos [10-K 2025, PDF p. 44]). Lo que queda es la escala de vacunas, ganado e Internacional: 2 puntos sobre r, dentro de 2–3 como mucho (MR pp. 62–63; E2). «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). El año exacto del salto es convención del horizonte: por eso las fechas de exclusividad son un dato material (punto 6).
- **BUENO (fundamentada).** De 30,0 % a 12 %: los productos nuevos envejecen como los de hoy. El 30 % supera el máximo de la fila 36 (25,5 %); lo pesa una probabilidad de 0,2.

## 3. Palancas

No pido revisión (`revisar_palancas = false`). Revisé la aritmética de la fase B (crecimientos compuestos, reinversión del BUENO ≈3.800, g ÷ ROIC ≈23 %, rentabilidades marginales, deuda neta ÷ EBITDA en el MALO ≈2,2x) y cuadra. El S2C se ancla en `C53`, no en `C54`. El ROIC terminal del MALO en r no se sube por el perímetro (sección 1 bis). La única cuestión de perímetro es la de la I+D, ya medida arriba. Las dudas sobre celdas de la fase A (C18, B66) y de la B (B69, Palancas!C14, B16:D16) quedan en `celdas_corregidas` con `despues = antes`.

## 4. Autocomprobación

Diez entradas en `fase_c.json`. Lo que encontré:

- **Anclaje en el precio.** El precio de Sí cae a 0,23 del precio. No encuentro el ancla: ninguna palanca cita el precio, las recompras ni el valor de Simply Wall St. Pero la zona depende de céntimos.
- **¿El MALO es de verdad malo?** El MALO no recoge una pérdida de exclusividad de Simparica Trio y Apoquel. Con lo que la propia fase B daría en ese caso, el precio de Sí bajaría a ≈69,1 (estimación auxiliar). «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Optimismo del BUENO.** El BUENO también sostiene la zona por céntimos: con un ROIC terminal de 0,10 pasaría a `vigilar`.
- **Consistencia.** No mantengo el Vigilar de la fase A por coherencia. La conclusión provisional es la que da el orden de mando hasta la zona.
- **Disponibilidad.** La «tendencia de varios años» de las visitas es una paráfrasis de la conferencia sin cifra, y sobre ella descansa C17. La anoto como punto débil.

## 5. Cubo y conclusión provisionales

No hay bloqueo: la gramática no tiene errores y el estado técnico solo espera las predicciones. Tampoco hay límite del modelo. No aplico ningún descalificador: el más cercano, el cambio que no me deja juzgar si el foso dura, se resuelve con datos concretos y no con ciencia que no entiendo. Hasta aquí, la zona da **comprar**. Pero un dato ausente material va antes que la zona (punto 6), así que la conclusión favorable no se emite. **Cubo provisional: Vigilar.** Cierre previsto: `pendiente_de_datos`, acción `null`. Con 0,23 de colchón vale lo que Munger dice de los puntos pequeños: no se arriesga lo que uno tiene «for tiny, little, incremental advantages» (AIWTK p.104; HIM).

## 6. Datos ausentes (S-19)

He revisado los 26 datos de `datos_ausentes.json`. Dos son materiales para la conclusión favorable:

- **Fechas de pérdida de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela.** Deciden si un genérico como el de Draxxin cae dentro de los diez años explícitos. Si cae, el MALO pasa a ser el caso central y la zona a `vigilar`. Si no, el ROIC de 0,11 y el NORMAL se sostienen. La fase A ya hacía depender C12 de este dato.
- **Quién es el rival de dermatología y qué cuota tiene.** Decide si la pérdida de 2026 es un escalón o una pendiente, es decir, B69:C69. Con 0,4 / 0,4 / 0,2 el precio de Sí bajaría a ≈71,0 (estimación auxiliar). «I think it's important to know which competitor is most likely to do you in» (AIWTK p.131; HIM).

Los otros 24 no son materiales, cada uno por su motivo. Los ceros pendientes de verificación son clasificaciones US GAAP o partidas que no existían. El tamaño de mercado, el capex, las adquisiciones, el rating, el covenant, China y la alineación fiscal son pequeños frente a la conclusión o ya tienen otra cifra que los acota. `alguno_material = true`.

## 7. Fundamento material (D10)

Ninguna hipótesis material entra en la lista de la sección 14. Revisé las cinco palancas en los tres escenarios, B69:D69, C22:C23, C76, C44, C62, C8, C6 y las narrativas B65:D66. Todas son de clase fundamentada o de convención con hechos citados en el apoyo. Ninguna es «sin juicio propio» ni «técnico» (C97 es técnico, pero no es una hipótesis material). Ninguna narrativa es genérica. `hipotesis_sin_fundamento = []`. Como la conclusión favorable ya la bloquea un dato ausente, `resultado = no_procede`: no hago comprobación conjunta y `sobrevive` queda en `null`.

## 8. Lo que más condiciona y qué lo resolvería

Lo que más condiciona es B69:C69 con Palancas!C18: que 2026 sea un escalón (NORMAL 0,5, ROIC terminal 0,11) y no una pendiente (MALO 0,3). Lo resolverían dos cosas. Primero, las fechas de exclusividad por producto y mercado, de la sección de propiedad intelectual del 10-K 2025 o preguntando a Relación con Inversores. Segundo, la cuota de dermatología y de Simparica Trio en el 3T26, junto con la del rival que la gana. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## 9. Configuración V6.4

No aplica: no hay `configuracion_economica.json` en la carpeta (plantilla V6.3.1 F1). `configuracion_v64 = null`.
