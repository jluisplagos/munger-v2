# Zoetis Inc. (ZTS) · fase C · turno 1 · 5-nov-2026

## 1. Una sola historia

La historia de la fase A es una empresa de calidad de cartera cuya ventaja dura menos por franquicia de lo que leía la etapa 1, que crece poco sin el precio de 2023–2025 y que hoy no da margen. Lo que la hoja calcula con mis palancas cuenta esa historia.

- **Valores.** MALO 58,65 · NORMAL 80,06 · BUENO 106,17 · ponderado 78,62 (B78:D78, C83). Precio 82,11. El precio está un 4,4 % por encima del ponderado (diferencia ÷ ponderado): zona `caro` de `precio.json`. Precio de Sí 71,97 (P\*, sin tope del NORMAL). El precio de Sí está un 12,4 % por debajo del precio (diferencia ÷ precio); dicho al revés, el precio está un 14,1 % por encima del precio de Sí (diferencia ÷ precio de Sí). Regla antigua (C156) 58,65.
- **Sin crecimiento.** El negocio vale 64,97 por acción sin crecer. El precio paga 17,14 por el crecimiento y el crecimiento de mi NORMAL vale 15,09 (1,14 veces). En el MALO el crecimiento resta 6,31, porque el margen cae del 34,1 % de partida al 31 %.
- **DCF inverso.** Con las demás palancas del NORMAL, el precio descuenta un crecimiento de ventas del 3,66 % en los años 1–5 (C86). Mi NORMAL es 3,0 %, la historia de 2020–2025 7,2 % (C46) y la guía orgánica de 2026 negativa. El precio de Sí descuenta un 0,13 %. El mercado no pide un BUENO; pide algo más que mi NORMAL.
- **Peso del terminal.** 41 %, 52 % y 59 %: pasa en los tres. El valor no depende sobre todo del «para siempre».
- **Semáforos.** Margen en REVISAR en los tres, por el Q3 del sector (15,5 %), no por el máximo propio (37,8 %): G5 ya justificada. Tu r (9,0 %) por debajo de la r mínima (10,4 %): la r es heredada (S-3), lo informo y no la cambio. Cuota implícita sin lectura (C24 vacía). Lo demás pasa.
- **Tornado (información, no criterio).** La tasa de descuento mueve 14,16 USD el NORMAL con ±1 punto. El valor depende sobre todo de la r exigida (A5). Después ROIC terminal (8,19 con ±5 puntos) y crecimiento (6,42 con ±2 puntos).
- **Veredicto de la hoja.** A6 dice «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar porque lo entiendo, está en el borde de mi círculo, la calidad de cartera sigue y el precio no da margen.

Incoherencias que anoto (ninguna rompe la historia):

1. La fase A cita C55 como 27,7 %. La hoja da 23,6 %, con la I+D capitalizada; el 27,7 % es la media de 2021–2025 de la fila 33. C18 no cambia: las dos cifras casi doblan el 14,7 % del sector. La fase B ya usó el 23,6 %.
2. Acciones y precio en fechas distintas (A3). La hoja divide por 424,93 m (31-dic-2025) y a 30-sep-2026 hay 407,49 m [zoetis-10q-2026-q3.txt, PDF p. 5]. Con C76 = 0 la caja gastada en recompras no se suma en ninguna fecha, así que el valor por acción sale hasta ≈ 4 % bajo. Derivado: ponderado ≈ 82,0, precio de Sí ≈ 75,0. La zona seguiría en `caro` por 0,1 USD y el precio seguiría por encima del precio de Sí. Es una celda de datos: no la toco.
3. En el MALO las ventas caen y la hoja libera capital a S2C 0,8 (≈ 470 mm en diez años, derivado). La fase B dice que plantas e I+D no se venden con cada paciente perdido. Por eso el FCF del año 1 del MALO (2.532) es el más alto de los tres. Sin esa liberación, el MALO valdría ≈ 1 USD menos y el precio de Sí ≈ 0,5 USD menos.
4. **Dos palancas derivadas con generosidad, que calculo y dejo.**
   - `Palancas!C14 = 0,03`. Los componentes de la fase B dan un CAGR de 1,3–2,1 % (si los +3 a +4 puntos son brutos) o de 2,1–2,9 % (si son netos). Con la tabla del DCF inverso de la hoja: con 0,025 el NORMAL vale 78,56 y el precio de Sí ≈ 71,37 (−0,8 %); con 0,02, 77,10 y ≈ 70,78 (−1,6 %).
   - `Palancas!B14 = −0,01`. La cuenta de la fase B da ≈ −2 % anual; la fase B eligió un punto intermedio con el «las ventas dejan de crecer» de la fase A. Con −0,02 el precio de Sí bajaría ≈ 1,2–1,5 USD.
   - Las dos a la vez: ≈ 69,3–69,6 (≈ −3,5 %). Ni el cubo (Vigilar) ni la zona (`caro`) cambian, y el precio de Sí se mueve menos de un 5 %. No pido revisar palancas.
5. La base del margen es la media del ciclo (C8, 34,1 %) con un LTM del 35,3 %: los años 1–4 arrancan por debajo del margen actual. Es prudente y pequeño (≈ 0,3–0,4 USD por acción). C8 es de la fase A y su regla lo sostiene.
6. El salto del año 11 supera 5 puntos en los tres escenarios. Lo justifico en el punto 2.

## 2. Desviaciones pendientes (G8, salto del año 11)

G16 (peso del terminal) y G17 (cuota implícita) no saltan. G8 sí, en los tres escenarios.

- **MALO, 0,108 · convención.** El ROIC terminal es la tasa del motor (r = 0,09). Con él, crecer para siempre ni crea ni destruye valor (CV p. 13; E3). La rentabilidad marginal de los años 1–10 (19,8 %) apenas actúa, porque las ventas caen en los años 1–5. Lo que se pierde en el año 11 es la ventaja del capital nuevo: con competidores que entran con descuentos y con genéricos en franquicias que pesan el 42 %, el dólar reinvertido rinde lo que cuesta, como con Draxxin (−66 % [zoetis-10k-fy2025.txt, PDF p. 42]). El capital viejo sigue rindiendo por encima.
- **NORMAL, 0,104 · fundamentada.**
   - Años 1–10: cada dólar nuevo rinde 22,4 %, algo menos que el capital viejo (23,6 %), porque se vende con franquicias que aún tienen exclusividad.
   - Año 11: el capital nuevo rinde 12 %. Lo que se pierde son las exclusividades de hoy. Cada franquicia caduca: Draxxin −66 % y Rimadyl −39 % en EE. UU. tras los genéricos [zoetis-10k-fy2025.txt, PDF p. 25]. Dermatología ya pierde cuota ante marcas nuevas (≈ 96 % → ≈ 80 %).
   - Lo que queda es la escala de cartera, que sostiene un exceso pequeño sobre r (MR p. 63; E2), no el 22 % de un producto protegido. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **BUENO, 0,146 · fundamentada.**
   - Años 1–10: los lanzamientos se venden con la fuerza de ventas y las plantas que ya existen (29,6 % por dólar nuevo, el máximo de la fila 33).
   - Año 11: el capital nuevo converge a la media del sector (CV p. 10; E2), porque las exclusividades de 2026–2029 también caducan. Se pierde el sobreprecio del producto sin sustituto barato. Se conserva la capacidad de renovar cartera, que dio un ROIC de al menos 17,8 % cada año de 2016–2025.

## 3. ¿Hay que mover palancas?

No. No veo una incoherencia que no se resuelva con palabras. Las dos derivaciones generosas (C14 y B14) las he calculado: juntas mueven el precio de Sí ≈ 3,5 % sin cambiar cubo ni zona.

- **Perímetro (sección 1 bis).** El S2C está anclado en el marginal propio (C53 = 0,81, ancla A2_propio), no en C54: no está mal derivado. El ROIC terminal del MALO igual a r no es un efecto del perímetro y no pido subirlo.
- **Vara del foso.** Con US GAAP la medida del accionista pagado el alquiler no es aplicable. C18 se juzga solo frente al sector.
- **Celdas de la fase A.** Registro C18 y C8 en `celdas_corregidas` con el valor igual.
- **Límite del modelo.** No aplica: el motor A valora a esta empresa.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Las celdas mantenidas nombran su evidencia. La fase B cambió B69 y D69 contra la etapa 1. Mi precio de Sí (71,97) no se parece al suyo (≈ 49). Nada que cambiar.
2. **Anclaje en el precio o en la fuente externa.** El ponderado queda cerca del precio, y lo miré. Las desviaciones del NORMAL salen de componentes y ninguna cita el precio, Simply Wall St ni los analistas. El DCF inverso (3,66 %) está por encima de mi NORMAL: anclarme al precio me habría llevado a subirlo.
3. **Consistencia y compromiso.** El cubo Vigilar no necesitó palancas torcidas: C13 = No ya llevaba ahí, y la fase B subió el MALO y bajó el BUENO. Encontré la cita equivocada de C55 en C18 y la corrijo sin cambiar el valor.
4. **Historia bonita / viento de cola.** Parte del margen de 2023–2025 fue precio del nicho. Pero el NORMAL (0,35) se apoya en el suelo de 2021 (34,9 %), un año con 1 punto de precio y 14 de volumen y lanzamientos (extracto §4).
5. **Optimismo del BUENO frente a la tasa base.** El BUENO crece menos que la historia, no pasa del margen máximo y converge al sector. Su rentabilidad marginal (29,6 %) está, eso sí, en el máximo propio. Con un S2C de 0,8 el precio de Sí bajaría ≈ 0,3 USD.
6. **Doble castigo del mismo riesgo.** La erosión está en la severidad y en la probabilidad del MALO, que son dos cosas distintas. No está en la r, ni en la quiebra, ni en el g del MALO (PA p. 20; E6).
7. **Disponibilidad (lo vívido del extracto).** El NORMAL al 3 % pesa mucho dos trimestres de 2026. Con 0,04 el precio de Sí sería ≈ 73,3 y con 0,02 ≈ 70,8. La acción no cambia. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).
8. **Autoridad (guía de la dirección como hecho).** El año 1 coincide con la guía, pero lo sostienen nueve meses publicados. Las aprobaciones guiadas solo entran en el BUENO, con probabilidad 0,15.
9. **¿El MALO es de verdad malo?** Es real pero no lo peor. Supone la mitad de Draxxin en Simparica y Apoquel (≈ −33 %), cerca de Rimadyl (−39 %). Fuera quedan un Draxxin entero en las cuatro grandes, un problema de seguridad probado y el margen de 2016. Con un Draxxin entero (≈ 50 USD) el precio de Sí bajaría a ≈ 67,6. El precio del MALO no es un suelo. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
10. **Lo no numerable que pesa y no está en las palancas.** La demanda colectiva sobre seguridad y cuota de cuatro productos, la salida del director financiero, la recompra con deuda a ≈ 134 USD, el poder del canal, la caída de visitas, el ERP nuevo y la ciencia del pipeline. Va a la tesis inversa y a «qué me haría cambiar de cubo» en el turno 2.

## 5. Cubo y conclusión provisionales

Recorro el orden de mando:

- Bloqueo: no hay (gramática sin errores; B252 y B254 falsos).
- Límite del modelo: no.
- Descalificador: ninguno de la sección 2 aplica (fase A).
- Dato ausente material: ninguno (punto 6).
- Fundamento material: la lista está vacía (punto 7).
- Zona: `caro`.

**Cubo provisional Vigilar. Conclusión provisional esperar.** El precio de Sí (71,97) es el objetivo que leerá el turno 2. El error que tengo más cerca es pagar cualquier cosa por la calidad pasada: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 6. Datos ausentes (S-19)

Reviso los 57 uno a uno. Ninguno es material para sostener `esperar` con el precio de Sí como objetivo. Hay tres grupos:

- **Ceros pendientes de verificar.** Con US GAAP los ceros de intereses en financiación son lo que pide la norma, y los de arrendamientos y minoritarios mueven el FCF o el ROIC décimas.
- **Hechos del T3 volcados por error como «no encontrado».** Son hechos, no ausencias, y los uso. Entre ellos están las 407,49 m acciones de la incoherencia 2.
- **Ausencias reales.** Ninguna mueve una palanca ni la acción.

La que más pesa es la de las **fechas de pérdida de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela**. No la declaro material por cuatro razones:

- El 10-K da su lista de expiraciones de patentes clave recientes y próximas, y solo están Draxxin, Excede y Cerenia [zoetis-10k-fy2025.txt, PDF p. 17] (extracto §8).
- La erosión de 2026 viene de marcas nuevas con descuentos, que es el mecanismo del MALO.
- El MALO ya supone una pérdida parecida a la de Rimadyl.
- Con un MALO peor (Draxxin entero) el precio de Sí bajaría a ≈ 67,6, y con p(MALO) 0,3 a ≈ 69,7. El precio actual sigue por encima y la acción no cambia.

Si una fecha cae antes de 2031, el MALO se queda corto. Por eso es el dato de B223.

## 7. Fundamento material (D10)

Recorrí las hipótesis materiales: las palancas de los tres escenarios, g, probabilidades, quiebra y recuperación, C76, C44, motor, base del margen, caso especial y narrativas. Todas están en clase fundamentada o convención, con hechos de la Historia o de los extractos. No hay ninguna «sin juicio propio» ni «técnico». Las narrativas tienen mecanismo y «qué lo pararía» propios.

`hipotesis_sin_fundamento` queda vacía. La conclusión provisional no es favorable, así que el resultado es `no_procede` y no hago la comprobación conjunta.

La más débil, aunque fundamentada, es el ROIC terminal del NORMAL (0,12): sale del punto medio entre r y la media del sector, con hechos que dicen que el foso existe pero no cuánto dura.

## 8. Lo que más condiciona y qué lo resolvería

- **Hipótesis que más condiciona:** `Palancas!C18`, el ROIC terminal del NORMAL. De él depende que el salto del año 11 cuente bien cuánto dura la ventaja de las cuatro grandes franquicias.
- **Qué lo resolvería:** las fechas de expiración de patentes y de exclusividad de datos de Simparica Trio, Apoquel, Cytopoint y Librela en EE. UU. y la UE, pedidas a Relación con Inversores o buscadas en el registro de patentes y exclusividades de la FDA para medicamentos veterinarios (Green Book). Junto con las cuotas Kynetec de dermatología y de Simparica Trio de los cuatro próximos trimestres.

## 9. Comprobación conjunta (turno 2)

No hay `comprobacion_conjunta.json`: la lista de hipótesis sin fundamento está vacía y la conclusión no es favorable. `sobrevive` queda en `null` y el resultado sigue en `no_procede`. No hay un rango calculado del precio de Sí; las sensibilidades del turno 1 son derivadas, no las calculó la hoja.

## 10. Conclusión

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 71,97 (precio de Sí de `precio.json`).**

- **Por qué esperar.** El precio (82,11) está en la zona `caro`: 4,4 % por encima del ponderado (diferencia ÷ ponderado) y 14,1 % por encima del precio de Sí (diferencia ÷ precio de Sí).
- **Insumos para José Luis.**
   - Precio del MALO: 58,65, que no es un suelo.
   - Regla antigua (C156): 58,65.
   - Crecimiento implícito: el precio descuenta 3,66 % y el precio de Sí 0,13 %.
   - r = 0,09 frente a una r mínima de 0,104; el valor depende sobre todo de la r exigida.
   - Datos ausentes materiales: ninguno. Descalificadores: ninguno aplica.
- **Tamaño.** No escribo ningún tamaño de posición: es de José Luis.

`C93` = Sí: g 0,025, bajo la tasa sin riesgo (CV p. 5; E1). Con un ROIC terminal de 0,12 exige reinvertir ≈ 21 % del NOPAT (CV p. 12; I2), y el negocio lo paga. `C103` = No: el foso hay que renovarlo cada década. «if you can buy a few great companies then you can sit on your ass» (PCA pp.85–86; HIM) no describe este negocio.

## 11. Tesis (B101)

Zoetis vende medicinas, vacunas y diagnósticos para animales, sobre todo para perros y gatos, con márgenes del 35–38 % y un ROIC de al menos 17,8 % durante diez años. Su foso es escala y una cartera que hay que renovar. Cada franquicia caduca (Draxxin −66 %, Rimadyl −39 %), y dermatología ya pierde cuota ante marcas nuevas. Mi escenario central crece al 3 % sin el precio de 2023–2025. Con 0,25/0,6/0,15 el ponderado (78,62) queda por debajo del precio. La miraría a 71,97 o menos.

## 12. Tesis inversa (B102)

1. **El foso caduca.** Es una suma de exclusividades que caducan, y la concentración sube: cinco productos eran el 37 % de los ingresos en 2023 y el 42 % en 2025.
2. **El crecimiento era precio.** En 2023–2025 el crecimiento fue precio con visitas a la baja, y el precio ya resta. Dermatología cae un 16 % y ha perdido unos 16 puntos de cuota en poco más de un año.
3. **El MALO puede quedarse corto.** Si Simparica y Apoquel siguen el camino de Draxxin, las ventas caen más que en mi MALO y su valor baja hacia ≈ 50.
4. **La dirección.** Subió la deuda para recomprar a ≈ 134 USD, reparte más de lo que genera y tiene encima una demanda que alega que ocultó la caída de la demanda.
5. **El precio.** A 82,11 se paga más por crecer de lo que vale mi NORMAL (17,14 frente a 15,09), y hasta el valor del MALO hay casi un 29 % de caída.

## 13. Predicciones (dado el NORMAL)

1. La cuota de dermatología canina en EE. UU. (Kynetec) que publique la presentación del T3 de 2027 será ≥ 75 %. Se comprueba el 2027-11-30. Probabilidad 0,6.
2. Los ingresos de 2027 del 10-K FY2027 estarán entre 9.250 y 9.900 mm. Se comprueba el 2028-03-15. Probabilidad 0,65.
3. El margen EBIT de 2027 del 10-K FY2027 será ≥ 33,5 %. Se comprueba el 2028-03-15. Probabilidad 0,7.

**B222.** `Palancas!C18`, el ROIC terminal del NORMAL: cuánto dura la ventaja de las cuatro grandes franquicias.

**B223.** Las fechas de patentes y de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela, que pediría a Relación con Inversores o buscaría en el Green Book de la FDA, y las cuotas Kynetec de los próximos cuatro trimestres.

## 14. Qué me haría cambiar de cubo

- **A Sí:** que el precio baje de 71,97 y que las fechas de exclusividad sean posteriores a 2031, o que la cuota de dermatología se mantenga estable durante 2027.
- **A No:** que se prueben las alegaciones de la demanda, que la deuda pase de 3x EBITDA para recomprar, o que Simparica Trio caiga por debajo del 18 % de cuota con el margen bruto de EE. UU. bajo el 80 %.
- **A Demasiado difícil:** que Simparica Trio o Apoquel pierdan la exclusividad antes de 2030 y el valor pase a depender del pipeline, o que no pueda conseguir nunca las fechas.

## 15. Comparación con la etapa 1

El cubo es el mismo, Vigilar, y por la misma razón: un buen negocio sin margen al precio. El precio de Sí sube de ≈ 49 a 71,97 por tres motivos:

1. **El método.** La etapa 1 usaba la regla antigua; hoy esa regla daría 58,65.
2. **El MALO.** El mío es más suave que el de la etapa 1 (58,65 frente a ≈ 48,7). Lo digo sin rodeos: supone media Draxxin, no Draxxin entero.
3. **El NORMAL.** Crece al 3 % sin precio, frente al 5 % con precio de la etapa 1.

También cambian C17 (de Sí a No), C27 (de Expandiendo a Estable) y p(MALO) (de 0,2 a 0,25). El precio pasó de 73,08 a 82,11.
