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
- Perímetro de la I+D. *Corregido tras la nota (2) del contradictor.* En el turno 1 leí como I+D neta el exceso de la fila 31 sobre capex − D&A + circulante + adquisiciones, y de ahí saqué un doble cómputo. En realidad es la amortización de intangibles (149 / 141 / 128 en 2023–25 [10-K 2025, PDF p. 49 y 66]). No hay doble cómputo y retiro la estimación auxiliar de 74,12.

## 2. Desviaciones pendientes

`gramatica.md` deja pendiente G8 en los tres escenarios; G16 no salta (peso del terminal ≤ 0,58) y G17 no se puede calcular (C24 vacía).

- **MALO (convención).** ROIC terminal = tasa del motor. El salto de 15,4 % a 9 % dice que en el año 11 se acaba la exclusividad efectiva, como con Draxxin (−66 % en EE. UU. [10-K 2025, PDF p. 42]). Con ventas planas apenas mueve el valor.
- **NORMAL (fundamentada).** De 22,4 %, el retorno de la cartera de hoy (22,8–25,5 % en 2021–25, Historia fila 36), a 11 %. Lo que se pierde es la ventaja de patente de Simparica y Apoquel (28 % de los ingresos [10-K 2025, PDF p. 44]). Lo que queda es la escala de vacunas, ganado e Internacional: 2 puntos sobre r, dentro de 2–3 como mucho (MR pp. 62–63; E2). «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). El año exacto del salto es convención del horizonte: por eso las fechas de exclusividad son un dato material (punto 6).
- **BUENO (fundamentada).** De 30,0 % a 12 %: los productos nuevos envejecen como los de hoy. El 30 % supera el máximo de la fila 36 (25,5 %); lo pesa una probabilidad de 0,2.

## 3. Palancas

No pido revisión (`revisar_palancas = false`). Revisé la aritmética de la fase B (crecimientos compuestos, reinversión del BUENO ≈3.800, g ÷ ROIC ≈23 %, rentabilidades marginales, deuda neta ÷ EBITDA en el MALO ≈2,2x) y cuadra. El S2C se ancla en `C53`, no en `C54`. El ROIC terminal del MALO en r no se sube por el perímetro (sección 1 bis). No queda ninguna cuestión de perímetro: la de la I+D se retiró tras la nota del contradictor. Las dudas sobre celdas de la fase A (C18, B66) y de la B (B69, Palancas!C14, B16:D16) quedan en `celdas_corregidas` con `despues = antes`.

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

Lo que más condiciona es B69:C69 con Palancas!C18: que 2026 sea un escalón (NORMAL 0,5, ROIC terminal 0,11) y no una pendiente (MALO 0,3). Lo resolverían dos cosas. Primero, las fechas de exclusividad por producto y mercado. El resumen de patentes del 10-K 2025 [PDF p. 17] solo trae Draxxin, Excede/Naxcel y Cerenia, así que hay que preguntarlas a Relación con Inversores. Segundo, la cuota de dermatología y de Simparica Trio en el 3T26, junto con la del rival que la gana. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## 9. Configuración V6.4

No aplica: no hay `configuracion_economica.json` en la carpeta (plantilla V6.3.1 F1). `configuracion_v64 = null`.

## 10. Conclusión (turno 2)

No hay `comprobacion_conjunta.json`, porque no procedía: `sobrevive = null` y `resultado = no_procede`. El cierre es **`pendiente_de_datos` · Vigilar · acción `null`**, sin precio objetivo. El precio cumple la regla k = 3 por 0,23: el precio de Sí es 73,31, el precio esc. MALO 62,07, el ponderado 80,06 y la zona `cumple_regla_k`. Aun así no emito la conclusión favorable, porque faltan dos datos materiales: las fechas de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela, y el nombre y la cuota del rival de dermatología. El tamaño de la posición, también el cero, lo decide José Luis. La r (0,09) está por debajo de la r mínima (10,8 %). La palanca que más pesa es la tasa de descuento: el valor depende sobre todo de la r exigida. Confianza global: baja.

## 11. Tesis y tesis inversa

**Tesis (B101).** Zoetis vende medicinas, vacunas y diagnóstico para animales, y en diez años ha llevado el margen EBIT del 28,5 % al 37,8 % (Historia fila 29). Leo que su ventaja es de cartera: patentes renovadas con I+D y una escala en vacunas, ganado e Internacional que no depende de ninguna patente. En 2026 la parte de patente tropieza: dermatología pierde 10 puntos de cuota [presentación 2T26, PDF p. 6]. El precio descuenta menos crecimiento que mi NORMAL (0,9 % en los años 1–5, C86). Pero la tesis se apoya en dos datos que no tengo.

**Tesis inversa (B102).** El foso es una suma de exclusividades que caducan, y ya han empezado a caducar:

- Draxxin perdió un 66 % tras su genérico [10-K 2025, PDF p. 42], y Cerenia y Convenia ya tienen genéricos.
- La cuota de dermatología cae 5 puntos en un trimestre.
- Las dos primeras franquicias suman el 28 % de los ingresos y no se conoce la fecha en que pierden la exclusividad [10-K 2025, PDF p. 44].
- El margen se hizo con precio mientras bajaban las visitas, y ahora se devuelve en rebajas [conferencia 2T26, PDF p. 3, 12 y 16].
- La dirección recompró con deuda a ≈134 y ≈124 justo antes del tropiezo (Historia fila 22).
- El IRS reclama unos 450, en recurso, que el motor no resta [10-Q 2T26, PDF p. 16; 10-K 2025, PDF p. 84].
- El convertible al 0,25 % vence en 2029 [10-K 2025, PDF p. 59], y su refinanciación tampoco está en el valor.

Si llegan genéricos a Simparica Trio o Apoquel antes de 2030, el MALO vale ≈55 (estimación auxiliar) y a 73,08 se pierde una cuarta parte. Un colchón de 0,23 no es margen de seguridad, y con las objeciones del contradictor ni siquiera es colchón.

## 12. Predicciones (dado el NORMAL)

1. La cuota de dermatología en EE. UU. en el T3 2027 será del 80 % o más. Fecha: 2027-11-15. Probabilidad: 0,6.
2. En 2027 el crecimiento orgánico operativo será de al menos +2 %. Fecha: 2028-02-29. Probabilidad: 0,65.
3. El margen EBIT de 2027 estará entre el 33 % y el 37 %. Fecha: 2028-02-29. Probabilidad: 0,65.

Las tres separan el escalón del NORMAL de la pendiente del MALO.

## 13. Qué cambiaría el cubo

- **A Sí:** que las exclusividades duren más allá de 2030, que el rival esté identificado y que la cuota de dermatología se mantenga en el 80 % o más en el T3 y el T4 de 2026, con un precio de Sí que, recalculado con las cuatro correcciones del contradictor, quede claramente por encima del precio.
- **A No:** que 2027 vuelva a ser negativo en orgánico y que Simparica Trio empiece a caer.
- **A Demasiado difícil:** que las exclusividades venzan antes de 2030 y que el valor pase a depender de la ciencia del riñón y la oncología.

## 14. Comparación con la etapa 1

Los dos análisis dan Vigilar, pero por motivos distintos. En la etapa 1 era Vigilar por precio, con un precio de Sí de ≈49 estimado sin escalera. En la v2 es Vigilar por falta de datos: el precio cumple la regla k = 3 (73,31). La diferencia está sobre todo en el MALO. El de la etapa 1 tenía un FCF que caía un 2 % al año; el de la v2 tiene ventas planas con un margen del 32 % y vale 62,07. Si las exclusividades vencen antes de 2030, el MALO v2 baja a ≈55 y se acerca al de la etapa 1. La etapa 1 acertaba en la tesis inversa pero no conocía la causa; la v2 tiene la causa medida y le faltan las fechas. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## 15. Checklist de la fase C

He comprobado lo siguiente:

- Las 68 celdas cuentan una sola historia, con las incoherencias del punto 1.
- La autocomprobación tiene contenido en las diez tendencias.
- Están revisados los 26 datos ausentes, y dos son materiales.
- La lista de hipótesis sin fundamento está vacía, y digo qué revisé para llegar a eso.
- No hubo combinación conjunta, porque un dato material la bloquea antes.
- El estado (`pendiente_de_datos`), el cubo (Vigilar) y la acción (`null`) son coherentes con la sección 15.
- C104 no lleva ningún porcentaje y su etiqueta es «pendiente de datos».
- Las predicciones son tres, falsables, sobre el negocio y dentro de la ventana de 12–24 meses.
- La tesis inversa está apoyada en hechos y B222/B223 son concretos.
- La comparación con la etapa 1 y lo que cambiaría el cubo están escritos.
- Cada cita lleva libro y página.

## 16. Respuesta al contradictor

He leído `OBJECIONES.json` y he comprobado las citas en `texto/`. Las cifras son estimaciones auxiliares: salen de mi réplica del motor A y, para O4 y el conjunto, de las cuentas del contradictor. No son precio.json.

| Objeción | Respuesta | Efecto |
|---|---|---|
| **O1** (baja). Reclamación del IRS de unos 450, sin intereses ni sanciones, en recurso [10-Q 2T26, PDF p. 16; 10-K 2025, PDF p. 84] | **No rebatida.** La provisión no tiene cifra y no evita la salida de caja; el motor A no resta ese pasivo. Mi turno 2 la quitó de B102 diciendo que no estaba en mis entradas, y era un error. | Precio de Sí 72,78 si se cuenta como coste esperado al 50 % y 72,25 si se pierde entera. Vuelve a B102. Cuenta para el escalón a la baja. |
| **O2** (baja). Intereses de la deuda nueva: 296 esperados frente a 276,7 de media en 2023–25 [10-K 2025, PDF p. 86; Historia fila 15]; convertible al 0,25 % con vencimiento en 2029 [10-K 2025, PDF p. 59] | **No rebatida.** El gasto por intereses sube un 15 % en el semestre [10-Q 2T26, PDF p. 29] y la caja que genera intereses ha bajado (Análisis!C53). | 72,91 en el caso mínimo, que es un hecho, y 71,44 en el central, que es un juicio sobre la refinanciación. Cuenta para el escalón a la baja. |
| **O3** (baja). Tipo impositivo: 20,4 % en 2025 y en el semestre de 2026, frente a t = 0,1997 en la proyección [10-K 2025, PDF p. 50; 10-Q 2T26, PDF p. 32] | **No rebatida.** He comprobado que f sale del tipo de cada año de 2023–25 (275,3 ÷ 27.267). | 72,92 con el 20,36 % y 72,78 con el 20,5 %. Cuenta para el escalón a la baja. |
| **O4** (sube). Fecha de la valoración y acciones: 414,15 M a 30-jun-2026 [10-Q 2T26, PDF p. 5]; repartos del semestre [10-Q 2T26, PDF p. 8]; aviso V28 de la hoja | **No rebatida.** La cuenta ya resta los repartos pagados; si acaso es prudente. | 75,71, o 75,39 si solo se actualizan las acciones. Cuenta para el escalón al alza. Sola no cambia el cubo: la rama de genéricos se queda en ≈71,1. |

**Regla de movimiento.** O1, O2 y O3 dan un escalón a la baja y O4 uno al alza: se compensan.

**Conclusión final, sin cambio:** `pendiente_de_datos` · Vigilar · acción `null`, sin precio objetivo. Lo que cambia es el motivo. Con las cuatro correcciones, el precio de Sí central queda en ≈72,6–72,7, por debajo de 73,08, y su rango (≈70–74,3) contiene el precio. El Vigilar es ahora por datos **y** por precio: aunque lleguen las fechas de exclusividad y el rival, habrá que recalcular antes de hablar de compra.

**Notas del contradictor:**

- **(2)** Tiene razón: no hay doble cómputo de la I+D. Corrijo la incoherencia 5, los motivos de B16:D16 y la autocomprobación.
- **(3)** El 10-K no da las fechas de Simparica Trio, Apoquel, Cytopoint ni Librela. Corrijo B223.
- **(4)** Rimadyl cayó un 39 % tras los genéricos [10-K 2025, PDF p. 25]. Suaviza la rama de genéricos, pero no fija ninguna fecha.
- **(1)** y **(5)** no piden cambios.
