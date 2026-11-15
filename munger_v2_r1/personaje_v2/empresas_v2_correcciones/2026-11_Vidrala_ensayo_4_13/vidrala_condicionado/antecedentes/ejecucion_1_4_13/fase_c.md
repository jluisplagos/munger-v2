# Fase C · turno 1 · Vidrala, S.A. (VID) · base económica 31-dic-2025 · V6.4 experimental, motor B (ensayo 4.13)

Reviso las fases A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Los hechos salen de `datos_v63.md` (Historia, anclas), de `extracto_v63.md` ([ES, PDF p. n] y [CF_aaaa, PDF p. n]) y de lo que calcula la hoja (`resultados.json`, `precio.json`, `configuracion_v64_variantes.md`, 19 variantes calculadas). Uso además, como información, las tres correcciones económicas de la 4.13 y su recálculo del crecimiento terminal. Los cálculos marcados «míos» son aproximaciones con el efecto del tornado (+3,68 € de valor NORMAL por punto de margen) y con la pendiente de la escalera (0,43 € de precio de Sí por euro de valor MALO o NORMAL, 0,14 € por euro de BUENO). No son recálculos del libro.

## 1. Una sola historia

**Lo que calcula la hoja.** Valor por acción 44,32 / 60,21 / 78,52 € (MALO / NORMAL / BUENO), ponderado 60,70 €, precio de Sí 56,02 € (P\*, sin tope del NORMAL), precio 90,10 €: zona **caro**. 90,10 está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí); el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio). La regla antigua (C156) da 44,32. Peso del terminal: 41 / 48 / 54 %, todo bajo el 75 %. Semáforos: margen en REVISAR en los tres escenarios (G5, justificado en la fase B) y f = −2,8 % en REVISAR, que es la razón del motor B. La cuota implícita no se calcula porque C24 está vacía. El resto pasa. El estado técnico sale COMPLETO porque el libro lleva todavía las predicciones del cierre de la 4.12. La hoja dice «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar, porque C13 mide el precio, no el negocio.

**DCF inverso.** A 90,10 el mercado descuenta un crecimiento de ventas del 14,2 % anual en los años 1–5 con el resto de mi NORMAL; al precio de Sí, −0,8 %. Mi NORMAL crece 1,5 % y el BUENO 3,5 %. El precio supera el valor BUENO de las 19 variantes (el máximo es 88,38, en solo_N2). «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). No hace falta que lo sea nadie: con mi NORMAL, 90,10 equivale a una tasa bastante más baja que la del motor. Yo no tengo esa alternativa: «it's your alternatives that matter. That's how we make all of our decisions» (PCA p.114; HIM).

**Tornado (información, no criterio).** Sobre el valor NORMAL: ROIC LP ±5 puntos 12,67 €; tasa ±1 punto 10,56 €; margen ±2 puntos 7,36 €; crecimiento ±2 puntos 3,52 €; S2C ±0,3 2,22 €; g ±0,5 puntos 0,19 €. El del ROIC es asimétrico: hacia abajo pesa mucho y hacia arriba poco, porque el terminal reinvierte g ÷ ROIC con g = 2 %. La tasa no es la palanca más influyente.

**¿Cuentan la misma historia que la fase A?** Sí. Es un fabricante maduro de un envase pesado, con un margen que sigue a la energía, un foso estrecho que la Historia sostiene y un precio que paga más que mi escenario bueno. Las fricciones que encuentro no cambian ni el cubo ni la zona:

1. **Rentabilidad marginal.** La hoja calcula 14,7 / 20,0 / 9,5 % porque aplica f = 1,165 al S2C (SR1) y el tipo N1. La fase B había escrito ≈13 / 17,6 / 8,4 % con las bases heredadas. Con SR1 esa cifra es el retorno del capital que crece, con la reposición cargada aparte; sobre toda la inversión nueva el retorno es menor. El salto del año 11 del NORMAL (5,7 puntos) solo pasa de 5 por la configuración.
2. **Crecimiento terminal (corrección 4.13).** La lectura de la 4.12, «el ROIC terminal es igual a r y por eso el crecimiento terminal no crea valor», no vale. El motor descuenta la perpetuidad a r_op = 8,69 %, no al 9 %, y el terminal carga además la reposición. Recalculado con g = 0, el crecimiento perpetuo de la activa aporta +0,61 / +0,88 / +6,52 € de valor y +1,57 € de precio de Sí. Desde el año 11 el capital nuevo rinde la r personal y el crecimiento aporta poco, pero no nada. No cambia ninguna palanca: cambia cómo escribo G8 y la tesis.
3. **El MALO.** Su historia cuenta capex de hornos sin ventas. Con R1 la palanca B16 no actúa (s2c_inerte) y ese capex solo entra por λ. Calculo yo que 20 mm más al año en los años 1–5 costarían ~1,0 € de precio de Sí. Al revés, el terminal del MALO carga 15,8 mm al año de inversión para crecer con ventas por debajo del máximo conservado: quitarla sumaría ~1,1 €. Los dos efectos se compensan casi enteros.
4. **Perímetro del margen NORMAL.** Palancas!C15 = 0,18 sale de la media de 2019–2025 (18,1 %), que lleva Italia hasta 2022. La media de continuadas (N2, 18,55 %) daría 0,185. Corregirla subiría el precio de Sí de 56,02 a ~56,81 (+1,4 %): no cambia cubo ni zona y queda bajo el 5 %. La dejo y la registro (v2.1).
5. **Mezcla de la reinversión.** El S2C NORMAL 0,9 viene de una reinversión de 2021–2025 que fue un 52,6 % circulante, empujado por el precio de la energía. Con R1, la reinversión futura es un 13,2 % circulante: cada euro de ventas nuevas pide 0,96 € fijos, frente a 0,53 € en la historia. En SR1 esto no cambia el valor; sí decide cómo se comparan H y SRF.
6. **Mantenimiento.** La fase C de la 4.12 eligió SR1 con dos inferencias que no se sostienen. La retiro (punto 9).
7. **Celdas pendientes.** B101, B102, C93, C103, C104, las predicciones y B222:B223 del libro son los textos de la 4.12 («14 variantes»; ahora son 19, con el mismo rango). Los reescribo en el turno 2.
8. C27 = Expandiendo convive con escenarios que no expanden el margen; la fase A ya lo explicó. El valor sin crecimiento (58,19 €) y «cuánto pagas por crecer» son lecturas con base parcial (sin P0): solo contexto.

## 2. Desviaciones pendientes (G8)

La gramática deja dos: el salto del año 11 del NORMAL (5,7 puntos) y el del BUENO (8,0). Los justifico sin mover palancas.

- **NORMAL (convención).** En los años 1–10 cada euro nuevo de crecimiento rinde 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 %, junto al ROIC de cinco años (13,8 %, Historia C55). La escala regional sigue sirviendo al capital que crece mientras dura el modelo. Desde el año 11 el capital nuevo rinde el 9 %: es la r personal, 0,31 puntos sobre la tasa a la que descuenta el motor (8,69 %, Diagnóstico V6!C15). Lo que pierdo es el exceso de retorno de poner capacidad nueva en un mercado maduro [ES, PDF p. 55] cuyo competidor más peligroso no conozco (extracto §9). El margen del 18 % sigue sobre el capital instalado y el crecimiento perpetuo aporta todavía +0,88 € al valor NORMAL. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Con las bases heredadas el salto sería ≈4,0 puntos: el resto lo pone f. La convergencia hacia el coste de capital es un criterio, no una ley (MR; E2).
- **BUENO (fundamentada).** Cada euro nuevo rinde 1,1 × 1,165 × 0,20 × (1 − 0,2205) = 20,0 % porque llena hornos que no iban llenos: la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54] y el consumo fue inferior a lo previsto [ES, PDF p. 94]. Además suma Brasil, con un 42,4 % de margen EBITDA [ES, PDF p. 107], y cierra Toro [ES, PDF p. 85]. Esa ventaja se agota: cuando se usa la capacidad libre, el capital nuevo rinde el suelo de la meseta de 2018–2025 (Historia E33, I33, J33), tres puntos sobre r. Sigue por debajo de 2 × C55 (27,7 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

G16 y G17 no están señalados.

## 3. ¿Hay que mover palancas?

No. La incoherencia del margen NORMAL es de perímetro, pero corregirla mueve el precio de Sí un 1,4 % sin cambiar cubo ni zona (lo dejo escrito con su cálculo). La del MALO no tiene palanca que la exprese bajo R1. La de la rentabilidad marginal es de la configuración. La del crecimiento terminal es de lectura, no de cifra. `revisar_palancas = false`. En `celdas_corregidas` dejo Palancas!C15, B16 y C18 con `despues = antes` y su motivo. En la fase A no encuentro ninguna celda que impida sostener la conclusión.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Mantuve Vigilar, B65:D65 y 0,2/0,6/0,2. El cubo lo sostiene la escalera, no la herencia. Con 0,25/0,6/0,15 el precio de Sí bajaría a 54,10 (−3,4 %) y la zona seguiría «caro». El otro ancla es mi fase C de la 4.12: de ella reutilicé la revisión de datos ausentes después de comprobarla, pero no la evaluación del mantenimiento. Cambio: retiro SR1 y bajo la confianza de PM1.roic_terminal.
2. **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 90,10 y del 171,8 de Simply Wall St (C38, posterior a la base). Cambio: ninguno.
3. **Consistencia y compromiso.** En la 4.12 defendí SR1 y sus dos apoyos han caído. Busqué otros y no los tengo, así que lo honesto es soltarla: «People get to believing the plan because they created it» (AIWTK p.86; HIM). El cubo no depende de esto. Para cumplir la regla a 90,10 haría falta, como mínimo, un NORMAL de 90,10, y con MALO y BUENO fijos un NORMAL de unos 147 €. Cambio: estructura más coherente = null.
4. **Historia bonita / viento de cola.** El margen de 2024–2025 coincide con la bajada del gas [ES, PDF p. 56]: es marea. El 42,4 % de Brasil se compró [ES, PDF p. 36–37]. El crecimiento de 2020–2025 en euros (Iberia ~4,8 % anual, Reino Unido ~10,3 %) es sobre todo precio. Cambio: ninguno en palancas; la tesis lo atribuirá así.
5. **Optimismo del BUENO.** Crece menos que la historia, pero en los años 1–10 rinde el 20,0 % por euro nuevo, 1,45 veces C55, y la G7 no lo ve porque usa las bases heredadas. Pesa ~0,14 € de precio de Sí por euro de valor. Cambio: ninguno.
6. **Doble castigo.** NORMAL al 18 %, MALO al 15 %, p(MALO) sin subir, quiebra vacía y r sin prima. La reposición está en SR1 y la fase B no la descontó en el S2C ni en el ROIC. En el MALO, la carga terminal de R1 y el capex que no se ve se compensan. La estructura S sí contaría la reposición dos veces, pero no es la activa. Cambio: ninguno.
7. **Disponibilidad.** Kristin, Chile y las recompras de 2026 quedan fuera de la base; el apagón de 2025 la empresa lo da por no material [ES, PDF p. 78]. En el peor caso, los «Otros» costarían ~2,1 € de precio de Sí. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad.** El NORMAL (1,5 %) está junto a la proyección de la empresa (1,6 % [ES, PDF p. 55]), pero lo sostienen hechos sin la guía: ventas orgánicas del −5,4 % [ES, PDF p. 88] y C45 = 2,9 %. Que un capex del 8 % de las ventas basta para mantener [CF_2019, PDF p. 44] es un supuesto del vendedor: no lo uso para acotar la reposición. Cambio: ninguno.
9. **¿El MALO es de verdad malo?** Vale 44,32 €, la mitad del precio, con un margen del 15 % para siempre, por debajo de todos los años salvo 2016, 2017 y 2022. Un MALO al 13,7 % bajaría el precio de Sí ~1,5 €. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno.
10. **Lo no numerable.** La concentración de clientes sube [CF_2019, PDF p. 67; CF_2024, PDF p. 45; ES, PDF p. 104]. Pesan también la cobertura de energía de 2026 [ES, PDF p. 101] y el CO2. Hay además algo que ninguna celda recoge: si reconstruir un horno añade capacidad. Cambio: irá a la tesis inversa y a B223 en el turno 2.

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Sigo el orden de mando. **Bloqueo:** ninguno. **Límite del modelo:** no hay (FCF base positivo, no es financiera, el motor B cuadra en las 19 variantes). **Descalificador mío:** ninguno. **Dato ausente material:** ninguno. **Fundamento material:** la lista D10 está vacía. **Zona:** caro. Conclusión provisional: **esperar**, con el precio de Sí (56,02) como objetivo condicionado por la reposición (punto 9). «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM). Aquí ni siquiera es maravillosa: es buena y cíclica.

## 6. Datos ausentes (S-19)

Reviso uno a uno los 30 datos, que son los mismos de la 4.12. Ninguno es material para esperar con objetivo. Los seis de evidencia de la Historia no tocan el valor del motor B o el extracto confirma su cifra en la base (arrendamientos de 49,3 mm, minoritarios cero [ES, PDF p. 72 y p. 10]). Los que más pesan:

- **Cuota y competidores.** Es lo que me llevaría a No o a Demasiado difícil. No deja el objetivo sin base: los márgenes salen de diez años que ya incluyen un choque de energía completo, y el precio supera todos los BUENO calculados.
- **«Otros» ingresos.** En el peor caso costarían ~2,1 € de precio de Sí (−3,7 %). Aparecen en los dos años: «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM).
- **Capex por destino, capacidad por planta y utilización.** Es lo que fundaría la reposición y separaría H de SR1. Lo trato como hipótesis de la configuración sin fundamento suficiente, no como dato que bloquee. Ningún requisito lleva el precio de Sí por encima de 63,11 €.
- **Ingresos diferidos.** Cuadran: 41,117 − 23,115 = 18,002 mm de créditos fiscales [ES, PDF p. 10 y p. 71].

`alguno_material = false`.

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B: palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas. Todas son «fundamentada» o «convención» y citan hechos en el apoyo. Ninguna narrativa es genérica. C97 es «técnico», pero no es una hipótesis material del valor. Miré con lupa B69:D69 (convención argumentada; la alternativa mueve −3,4 %), B16 (no actúa), D16 (0,3 menos ≈ −0,4 €), D66 y C18 (la corrección 4.13 cambia su lectura, no su cifra). Ninguna entra en la lista.

La lista queda vacía. Con `esperar`, `resultado = no_procede`, la comprobación conjunta no procede y `sobrevive = null`. Los parámetros experimentales sin fundamento no entran en D10 con `esperar`: condicionan el objetivo.

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis de la que más depende la conclusión es **Palancas!C15**: que el 18 % del NORMAL sea la media de un ciclo que vuelve y no un nivel nuevo. Es lo que decide quién se queda la mejora: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM). Lo resolverían la serie de precio y de coste de energía por tonelada y segmento de 2019–2025, las cláusulas de traslado y la explicación de los 43,1 mm de «Otros». El objetivo lo condiciona además la reposición de hornos.

## 9. Configuración V6.4 experimental

**Variantes.** Las 19 calculadas dan «caro», con un precio de Sí de 51,29 a 65,72 € (la activa, 56,02). Es una tabla de sensibilidad, no un intervalo de confianza.

**Parámetros** (cobertura · base · Δ del precio de Sí):
- **N1 tipo** (variación conjunta necesaria · calculada · +1,75 € sin N1). La media de 2023–2025 da 22,05 %; lo compruebo. Fundamentado, no material. **N1 escudo** (contraste aislado · −0,08 €): convención inmaterial.
- **N2** (aislado · −0,94 €). Es el margen de partida, no mi objetivo. La Historia de 2020–2025 con Italia da 18,2 %. Fundamentado, no material.
- **N3 regla R1** (variación conjunta necesaria con «sin P-M1» · calculada). Su efecto propio, por diferencia de dos pares calculados, es −1,36 €, solo en el MALO. La juzgo con fundamento suficiente: un horno no devuelve caja cuando caen las ventas, y R0 libera capital fijo (aviso en sus tres variantes). Discrepa de la «hipótesis» de la configuración; resuelto en el JSON. **N3 circulante** (14,70 %, 14,9 % en 2024; solo variación conjunta · juicio económico): no material.
- **PM1.estructura** (aislada · calculada): S −0,50 · SR2 +1,06 · SRF +2,41 · H +5,35 · sin requisito +7,10 €. No es material para la acción y sí para el objetivo. Técnico, sin fundamento suficiente.
- **PM1.familia** (solo variación conjunta · juicio económico). Θ no se calcula y quitar toda P-M1 no mide la familia. Cualquier requisito es ≥ 0, y sin requisito el precio de Sí es 63,11 €: no puede cambiar la acción. Material para el objetivo y sin fundamento. Es la única hipótesis que condiciona el objetivo sin quedar cubierta por el ámbito calculado.
- **PM1.parametro λ** (aislado · calculada): de +2,37 € (1,10) a −4,73 € (1,25). Material para el objetivo y sin fundamento. Si todo el exceso fijo fuera reposición, λ ≈ 1,46, fuera del rango.
- **Convenciones** de años (−0,13 €) y de terminal (+0,40 €), y **cartera P0** (−0,54 €): no materiales y fundadas.
- **PM1.roic_terminal** (SR2 · variación conjunta necesaria · +1,06 €): no material. Q-ROIC1 sigue abierta. Si un ROIC es neto de reposición, encaja con SR1; si se midió sobre una inversión que la incluye, con SR2 (corrección 4.13 §1). La fase B eligió el ROIC sobre la base de la V6.3, la misma del S2C que SR1 ya reestima, y eso apunta a SR2. En contra, la amortización a coste histórico infla el NOPAT. Bajo la confianza a baja (discrepancia resuelta).

**Mantenimiento.** *¿La reposición supera la amortización?* En dirección, sí. El capex supera a la amortización todos los años desde 2017; en 2021–2025 fueron 739,0 frente a 509,6 mm (Historia filas 8 y 12). El exceso aparece también en los dos años sin crecimiento: 50,1 mm en 2020 y 55,6 en 2025, con la renovación de hornos como destino principal [ES, PDF p. 50]. Siguen en uso 627 mm de activos totalmente amortizados [ES, PDF p. 51] y los hornos duran hasta 15 años [ES, PDF p. 168]. En contra: el calendario de hornos [ES, PDF p. 180], la descarbonización [ES, PDF p. 173], Brasil y el supuesto del 8 % de 2019. La magnitud no la mido.

*¿Qué estructura?* No hay base para nombrar una. **S** es la menos coherente: cuenta dos veces lo que ya está en C53. **H** no queda excluida por 2025, porque en un año sin crecimiento también paga todo el requisito. Para distinguirla de SR1 harían falta años con crecimiento de volumen, y el crecimiento de 2021–2024 fue precio y la compra de Brasil. Además, H supone que reconstruir un horno añade la capacidad que pide el crecimiento, y no hay dato de eso. **SR1 frente a SRF** depende de la mezcla: quitan el 14,2 % del total y el 29,9 % de lo fijo, con denominadores distintos, y la mezcla futura no es la histórica. **SR1 frente a SR2** es Q-ROIC1. `estructura_mas_coherente = null`, `adoptada = false`. «When you don't know and you don't have any special competence, don't be afraid to say so» (PCA p.272; HIM).

**Avisos de dominio.** Ninguno es material. El factor de reestimación (f = 1,165; 1,000–1,309 en las variantes) explica G8, pero con λ ≈ 1,46 f perdería sentido. El terminal de R1 y s2c_inerte se compensan (~1 € cada uno). inversion_fija_para_crecer_negativa solo aparece con R0 (solo_N1, solo_N2, activa_R0_sin_PM1), que forman el extremo superior del rango, el menos creíble. Las lecturas con bases parciales (G7, referencias mecánicas, valor sin crecimiento sin P0) no comprueban el modelo experimental.

**Objetivo (provisional; lo cierra el turno 2).** Protocolo `objetivo_condicionado`. Condicionan el objetivo PM1.estructura, PM1.familia y PM1.parametro. La acción se sostiene en las 19 variantes y ningún condicionante es material para la acción. Tratamiento: **objetivo_condicionado**, con 56,02 € como objetivo condicionado. «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 10. Turno 2 · conclusión

**Comprobación conjunta:** no se ejecutó porque no procedía con `esperar`. No hay `comprobacion_conjunta.json`, así que `sobrevive` queda `null` y `resultado = no_procede`.

**Estado: concluido (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 56,02 €, condicionado.** No hay bloqueo, límite del modelo, descalificador ni dato ausente material, y la lista D10 está vacía; la zona es «caro». Con el protocolo experimental `objetivo_condicionado`, el precio de Sí se emite como objetivo condicionado a la reposición de hornos (PM1.estructura, PM1.familia y PM1.parametro). Es posible porque la acción se sostiene en las 19 variantes calculadas: precio de Sí de 51,29 a 65,72 €, todas «caro». Ese rango es el de la tabla de variantes: no es un intervalo de confianza ni cubre hipótesis no exploradas. PM1.familia no tiene contraste aislado. Que no pueda cambiar la acción es un juicio, apoyado en la cota del caso sin requisito (63,11 €). C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 56.02 · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional) …». La posición es de José Luis. «If you wait, I think you'll get your price» (DR p.29; AUTHOR).

**C93 = Sí.** g es el 2 %, por debajo de la tasa sin riesgo (2,85 %). La reinversión terminal es el 22 % del NOPAT más la reposición, y el peso del terminal es el 48 %. Desde el año 11 el capital nuevo rinde la r personal, 0,31 puntos sobre la tasa del motor: crecer aporta poco, pero no nada (+0,88 € de valor NORMAL). **C103 = No:** es cíclica, con un margen ligado a la energía y un foso estrecho; es una propiedad del negocio.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil. Ningún cliente pasa del 10 % de las ventas [ES, PDF p. 104] y lleva diez años con un ROIC por encima del sector (13,8 % frente a 9,3 %; Historia C55, Palancas H18). Leo que gana porque fabrica cerca del cliente y traslada la energía con retraso: el margen bajó al 13,7 % en 2022 y volvió al 20,8 % en 2024 (Historia I29, K29). El 19,9 % de 2025 está junto al máximo y la empresa supone bajadas de precio en 2026 [ES, PDF p. 54]. Mi NORMAL lo deja en el 18 %, y desde el año 11 el capital nuevo rinde la r personal. A 90,10 € pago más que mi BUENO (78,52 €). Espero hasta 56,02 €, un objetivo condicionado a la reposición de hornos.

**Tesis inversa (B102).** El No, con hechos:
- Un producto poco diferenciado en un mercado maduro [ES, PDF p. 55], con consumo por debajo de lo previsto [ES, PDF p. 94] y ventas orgánicas del −5,4 % [ES, PDF p. 88].
- Un margen que es energía barata camino del cliente [ES, PDF p. 54 y p. 56], con 2,9 puntos de «Otros» que nadie explica [ES, PDF p. 79].
- Hornos que se comen la caja: capex de 1,42 veces la amortización con ventas a la baja (Historia L12 y L8), y mi requisito solo carga un tercio del exceso de 2021–2025.
- Clientes que ganan fuerza [CF_2019, PDF p. 67; CF_2024, PDF p. 45].
- Crecimiento buscado donde no hay foso probado [ES, PDF p. 106, p. 105 y p. 85].
- Un ROIC que en 2016–2017 era la tasa (Historia C33:D33), y ningún competidor con nombre.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Los dos errores.** El que tengo más cerca es pagar cualquier cosa por calidad: el precio paga más que mi mejor escenario. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 12. Predicciones (dado el NORMAL; autopsia el 31-mar-2028)

1. El margen operativo de 2027 queda entre el 16 % y el 20 %. Probabilidad 0,7: cinco de los siete años de 2019–2025 cayeron en esa banda (Historia F29:L29).
2. Las ventas orgánicas de 2027 varían entre −2 % y +4 %. Probabilidad 0,65: el NORMAL crece un 1,5 %, pero el precio de la energía ha movido mucho las ventas (Historia fila 28).
3. El capex de 2027 supera 1,2 veces la amortización. Probabilidad 0,7: seis de los últimos nueve años lo superaron (Historia filas 8 y 12), aunque el calendario de hornos puede dejar un año por debajo [ES, PDF p. 180]. Pone a prueba la reposición, pero no distingue entre estructuras.

## 13. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo de 56,02 € sin que cambie el negocio. El umbral subiría con un capex desglosado que sitúe la reposición cerca de la amortización, con la prueba de que reconstruir un horno añade capacidad (H: +5,35 €) o con un margen de 2026–2027 del 18 % o más.
- **A No:** un margen por debajo del 14 % sin choque de energía; dos años más de capex por encima de 1,4 veces la amortización con ventas planas; o datos de cuota que muestren pérdida.
- **A Demasiado difícil:** que el valor pase a depender de Brasil y Chile; un exceso de capacidad duradero en los competidores; o una sustitución del vidrio que no sepa juzgar.

B222: el 18 % del NORMAL como media de un ciclo que vuelve (Palancas!C15), más la reposición, que condiciona el objetivo sin base para elegir entre H, SR1 y SRF. B223: precio y coste de energía por tonelada y segmento de 2019–2025, cláusulas de traslado, desglose de los «Otros» y del capex por destino, coste de reconstruir hoy un horno, toneladas que añade cada reconstrucción y serie de toneladas vendidas (preguntas a Relación con Inversores).

## 14. Comparación con la etapa 1

Mismo cubo, Vigilar, y por la misma razón. El precio de Sí pasa de ~48 € a 56,02 €, por tres cambios:
- La regla: la escalera k = 3 sustituye al mínimo entre el MALO y ¾ del ponderado.
- El modelo: motor B con palancas.
- La configuración experimental: resta 8,73 € frente al modo heredado (64,75 €).

Mi NORMAL (60,21 €) queda por debajo del valor normal de la etapa 1 (~74 €): el margen va a la media del ciclo y el capital nuevo rinde la r personal desde el año 11. La etapa 1 usaba hechos posteriores a la base; yo no. Mantengo C93 y C103 y reescribo B101, B102 y C104, este último sin porcentaje.
