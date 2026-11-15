# Fase C · turno 1 · Vidrala, S.A. (VID) · base 31-dic-2025 · V6.4 experimental, motor B (ensayo 4.13)

Reviso las fases A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Los hechos salen de `datos_v63.md` (Historia, anclas), de `extracto_v63.md` ([ES, PDF p. n] y [CF_aaaa, PDF p. n]) y de lo que calcula la hoja (`resultados.json`, `precio.json`, `configuracion_v64_variantes.md`, 19 variantes calculadas). Uso como información las tres correcciones económicas de la 4.13 y su recálculo del crecimiento terminal. Lo que marco «cálculo mío» es una aproximación con el tornado (3,68 € de valor NORMAL por punto de margen) y con la pendiente de la escalera (0,43 € de precio de Sí por euro de valor MALO o NORMAL, 0,14 € por euro de BUENO). No es un recálculo del libro.

## 1. Una sola historia

**Lo que calcula la hoja.** Valor por acción 44,32 / 60,21 / 78,52 € (MALO / NORMAL / BUENO). Ponderado 60,70 €. Precio de Sí 56,02 € (P\*, sin tope del NORMAL). Precio 90,10 €: zona **caro**. 90,10 está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí); el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio). La regla antigua (C156) da 44,32.

- **Peso del terminal:** 41 / 48 / 54 %, todos bajo el 75 %. G16 no salta.
- **Semáforos:** margen en REVISAR en los tres escenarios (G5, justificado en la fase B) y f = −2,8 % en REVISAR, que es la razón del motor B. La cuota implícita no se calcula (C24 vacía): G17 no salta. El resto pasa.
- **Veredicto de la hoja:** «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: C13 mide el precio, no el negocio.
- **DCF inverso:** a 90,10 el precio descuenta un crecimiento de ventas del 14,2 % anual en los años 1–5 con el resto de mi NORMAL; al precio de Sí, −0,8 %. Mi NORMAL crece un 1,5 % y el BUENO un 3,5 %; la Historia da 2,9 % a tres años y 8,2 % a cinco, con el choque de precios de 2022 y la compra de Brasil (C45, C46). El precio supera el valor BUENO de la activa y de las 19 variantes (máximo 88,38, solo_N2).
- **Tornado (información, no criterio):** ROIC LP ±5 puntos 12,67 €; tasa ±1 punto 10,56 €; margen ±2 puntos 7,36 €; crecimiento ±2 puntos 3,52 €; S2C ±0,3 2,22 €; g ±0,5 puntos 0,19 €. La tasa no es la palanca más influyente.

**¿Cuentan la misma historia que `fase_a.md`?** Sí. Un fabricante maduro de un envase pesado, con un margen que sigue a la energía, un foso estrecho que la Historia sostiene y un precio que paga más que mi escenario bueno. Las fricciones que encuentro no cambian ni el cubo ni la zona:

1. **Rentabilidad marginal.** La hoja calcula 9,5 / 14,7 / 20,0 % porque aplica f = 1,165 al S2C (SR1) y el tipo N1. La fase B escribió ≈ 8,4 / 13 / 17,6 % con las bases heredadas, como le pide la sección 0. El salto del año 11 del NORMAL pasa de 4,0 a 5,7 puntos solo por la configuración.
2. **Crecimiento terminal (corrección 4.13 §2).** «ROIC terminal = r, luego crecer no crea valor» no vale. El motor descuenta la perpetuidad a r_op = 8,69 %, y el terminal carga además la reposición. Con g = 0 recalculado sobre copias, el crecimiento perpetuo de la activa aporta +0,61 / +0,88 / +6,52 € de valor y +1,57 € de precio de Sí. El 9 % de B18:C18 es la tasa del motor redondeada, 0,31 puntos por encima. No cambia ninguna palanca; cambia cómo escribo G8.
3. **El MALO bajo R1.** Su historia cuenta capex de hornos sin ventas, pero B16 no actúa (s2c_inerte) y ese capex solo entra por λ. A la vez, el terminal del MALO carga 15,8 mm al año de inversión para crecer con ventas bajo el máximo conservado. Cálculo mío: quitar esa carga sumaría ~1,09 € al precio de Sí; 20 mm más de capex al año en los años 1–5 restarían ~0,96 €. Se compensan.
4. **Perímetro del margen NORMAL.** Palancas!C15 = 0,18 sale de 2019–2025 (18,1 %), con Italia hasta 2022. La media de continuadas (N2, 18,55 %) llevaría a 0,185. Cálculo mío: precio de Sí de 56,02 a 56,81 (+1,4 %). No cambia cubo ni zona y queda bajo el 5 %: la dejo, con el cálculo escrito (v2.1).
5. **Mezcla de la reinversión.** El S2C NORMAL 0,9 viene de una reinversión de 2021–2025 que fue en un 52,6 % la fila 14 (circulante), inflada por la energía y por partidas que no son circulante comercial. Con R1, el circulante futuro es el 14,7 % de las ventas nuevas: cada euro nuevo pide ~0,81 € fijos tras f, frente a 0,53 € en la historia. No cambia SR1; decide cómo se comparan SR1 y SRF (punto 9).
6. **BUENO.** Con f rinde el 20,0 % por euro nuevo en los años 1–10, más que cualquier ROIC anual de la Historia (máximo 16,2 %). G7 no lo ve porque usa las bases heredadas. Lo sostienen la capacidad libre [ES, PDF p. 54 y p. 94] y Brasil [ES, PDF p. 107].
7. **«Otros» de 2025.** 43,1 mm sin explicar son 2,9 puntos del margen [ES, PDF p. 79]. Si no fueran recurrentes: NORMAL 0,17 y BUENO 0,19, ≈ −2,2 € de precio de Sí (cálculo mío), zona igual.
8. C27 = Expandiendo con escenarios que no expanden: la fase A ya lo explicó. G7, las referencias mecánicas y el valor sin crecimiento (58,19 €, sin P0) son lecturas de base parcial: solo contexto.
9. Las celdas de la fase C del libro son de la ejecución anterior. Las reescribo en el turno 2.

## 2. Desviaciones pendientes (G8)

La gramática deja dos saltos del año 11: NORMAL 5,7 puntos y BUENO 8,0. G5 lo justificó la fase B. G16 y G17 no están señalados.

- **NORMAL (convención).** En los años 1–10 cada euro nuevo rinde 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 %, junto al ROIC de cinco años (13,8 %, Historia C55). Desde el año 11 rinde el 9 %. Lo que se pierde es el exceso de retorno de poner capacidad nueva en un mercado maduro [ES, PDF p. 55] cuyo competidor más peligroso no conozco (extracto §9). El margen del 18 % sigue sobre el capital instalado y el crecimiento perpetuo aún aporta +0,88 €. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). La convergencia al coste de capital es un criterio, no una ley (MR; E2).
- **BUENO (fundamentada).** Cada euro nuevo rinde 1,1 × 1,165 × 0,20 × (1 − 0,2205) = 20,0 % porque llena hornos que no iban llenos: la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54]. Suma Brasil al 42,4 % de margen EBITDA [ES, PDF p. 107] y Toro [ES, PDF p. 85]. Agotada la capacidad libre, el capital nuevo rinde el 12 %, el suelo de la meseta de 2018–2025 (Historia E33, I33, J33). Sigue bajo 2 × C55 (27,7 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

## 3. ¿Hay que mover palancas?

No. La única palanca con un defecto de derivación es C15 (perímetro), y corregirla mueve el precio de Sí un 1,4 % sin cambiar cubo ni zona. La del MALO no tiene palanca que la exprese bajo R1. La de la rentabilidad marginal es de la configuración. La del crecimiento terminal es de lectura, no de cifra. Comprobé las cuentas por componentes de B14:D14 (−1,56 / 1,5 / 3,56 %) y los topes de D18 (mín(C55, C56 + 0,03) = 0,12): cuadran. `revisar_palancas = false`. En `celdas_corregidas` dejo C15 y B16 con `despues = antes` y su motivo. No veo ninguna celda de la fase A que impida sostener la conclusión.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Vigilar, B65:D65 y 0,2/0,6/0,2 se mantienen por la escalera, no por la herencia. Con 0,25/0,6/0,15 el precio de Sí baja a 54,10 (−3,4 %) y la zona sigue «caro». No reutilizo la elección de SR1 de la 4.12 ni los textos de la fase C anterior. Cambio: estructura más coherente = null.
2. **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 90,10 y del 171,8 de Simply Wall St (C38, posterior a la base). Miré también el ancla a la baja: el NORMAL al 18 % frente al 19,8 % de 2023–2025 lo sostienen el ciclo y las bajadas de 2026 [ES, PDF p. 54]. Cambio: ninguno.
3. **Consistencia y compromiso.** Para cumplir la regla a 90,10 haría falta subir los tres valores 34 €: unos 9 puntos más de margen en cada escenario, un NORMAL del 27 % que nunca se ha visto (máximo 20,8 %). El cubo no depende de un ajuste fino. Mi compromiso con SR1 (4.12) se queda sin apoyos. «People get to believing the plan because they created it» (AIWTK p.86; HIM). Cambio: retiro SR1; PM1.roic_terminal con confianza baja.
4. **Historia bonita / viento de cola.** El margen de 2024–2025 coincide con el gas a la baja [ES, PDF p. 56]: es marea. Brasil se compró [ES, PDF p. 36–37]. Las ventas en euros de 2020–2025 crecen sobre todo por precio (orgánico −5,4 % en 2025 [ES, PDF p. 88]). De la empresa es lo que la Historia muestra: ROIC sobre el sector diez años y margen mínimo del 12,0 %. Cambio: ninguno en palancas; la tesis lo atribuirá así.
5. **Optimismo del BUENO.** Crece y gana margen menos que su historia, pero con f rinde el 20,0 % por euro nuevo, y necesita capacidad libre que no puedo medir. Pesa 0,14 € por euro de valor. Cambio: ninguno; anotado en la incoherencia 6 y en G8.
6. **Doble castigo.** NORMAL al 18 %, MALO al 15 %, p(MALO) sin subir, quiebra vacía, r sin prima. La reposición está en SR1 y la fase B no la descontó en el S2C ni en el ROIC. S sí la contaría dos veces, pero no es la activa. Cambio: ninguno.
7. **Disponibilidad.** Kristin (posterior a la base), el apagón de 2025 (no material según la empresa [ES, PDF p. 78]), la deuda a CDI y Chile no mueven ninguna cifra salvo Toro en el BUENO. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad.** El volumen +1 % del NORMAL es el supuesto de deterioro de la empresa [ES, PDF p. 54] y el 1,5 % queda junto a su proyección (1,6 % [ES, PDF p. 55]). Es donde más me apoyo en el vendedor. Lo contrastan el orgánico de 2025 y C45; con volumen 0 el precio de Sí bajaría ~0,75 €. El «8 % de las ventas basta» [CF_2019, PDF p. 44] no lo uso para acotar la reposición. Cambio: ninguno; lo declaro.
9. **¿El MALO es de verdad malo?** 44,32 €, un 51 % bajo el precio: margen del 15 % para siempre, por debajo de todos los años desde 2018 salvo 2022, y ventas −1,5 % al año. El 13,7 % de 2022 para siempre restaría ~1,6 € de precio de Sí. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno.
10. **Lo no numerable.** La concentración de clientes sube [CF_2019, PDF p. 67; CF_2024, PDF p. 45; ES, PDF p. 104]. Pesan la cobertura de energía de 2026–2027 [ES, PDF p. 101], el CO2 sin cuota publicada, los competidores sin nombre y si reconstruir un horno añade capacidad. Cambio: irá a la tesis inversa, a B222 y a «qué me haría cambiar de cubo» en el turno 2.

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Orden de mando. **Bloqueo:** ninguno (gramática con código 0). **Límite del modelo:** no hay (FCF base positivo, no es financiera, el motor B cuadra en las 19 variantes). **Descalificador mío:** ninguno; el más cercano es la macro de la energía y la divisa, que la fase A descartó con la Historia del ciclo completo. **Dato ausente material:** ninguno (punto 6). **Fundamento material:** la lista D10 está vacía (punto 7). **Zona:** caro. Conclusión provisional: **esperar**, con el precio de Sí (56,02) como objetivo condicionado por la reposición (punto 9). «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM). Aquí ni siquiera es maravillosa: es buena y cíclica.

## 6. Datos ausentes (S-19)

Reviso uno a uno los 30 datos. Ninguno es material para esperar con objetivo. `alguno_material = false`.

- **Evidencia de la Historia (seis).** Las cifras que usa el motor B en la base las confirma el extracto (arrendamientos 49,3 mm, minoritarios cero [ES, PDF p. 72, p. 109 y p. 10]). Los intereses solo tocan el motor A. Los ceros de adquisiciones de 2021–2022 sí entran en D_hist: si escondieran 53 mm, el S2C histórico bajaría de 0,92 a ~0,83 y f a ~1,148, unos 0,3 € de precio de Sí.
- **Cuota y competidores.** Es lo que me llevaría a No o a Demasiado difícil. No deja el objetivo sin base: los márgenes salen de diez años con un choque de energía completo y el precio supera todos los BUENO calculados.
- **«Otros» ingresos.** En el peor caso ≈ −2,2 € de precio de Sí. Aparecen en los dos años: «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM).
- **Capex por destino, capacidad por planta y utilización.** Fundarían la reposición y separarían H de SR1. Son información de una hipótesis sin fundamento suficiente, no un dato que bloquee: sin ningún requisito el precio de Sí sería 63,11 €.
- **Ingresos diferidos.** Cuadran: 41,117 − 23,115 = 18,002 mm de créditos fiscales [ES, PDF p. 10 y p. 71].

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B: palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas. Todas son «fundamentada» o «convención» y citan hechos en el apoyo. Ninguna narrativa es genérica. C97 es «técnico», pero no es una hipótesis material del valor. Miré con lupa B69:D69 (convención argumentada; la alternativa mueve −3,4 %), B16 (no actúa), D16 y C15 (perímetro, +1,4 %). Ninguna entra.

La lista queda vacía. Con `esperar`, `resultado = no_procede`, la comprobación conjunta no procede y `sobrevive = null`. Los parámetros experimentales sin fundamento suficiente no van a D10 con `esperar`: condicionan el objetivo.

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis fundamentada de la que más depende la conclusión, a mi juicio y no por el tornado, es **Palancas!C15**: que el 18 % del NORMAL sea la media de un ciclo de energía que vuelve y no un nivel nuevo. Decide quién se queda la mejora: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM). Lo resolverían la serie de precio medio y de coste de energía por tonelada y segmento de 2019–2025, las cláusulas de traslado de los contratos y el desglose de los 43,1 mm de «Otros» (pregunta a Relación con Inversores). El objetivo lo condiciona además la reposición de hornos.

## 9. Configuración V6.4 experimental

**Variantes.** Las 19 calculadas dan «caro», con un precio de Sí de 51,29 a 65,72 € (activa 56,02). Es una tabla de sensibilidad, no un intervalo de confianza. `zona_igual_en_variantes_calculadas = true` solo para esa tabla.

**Parámetros** (cobertura · base para la acción / para el objetivo · Δ del precio de Sí). Las bases para el objetivo siguen la regla de la revisión interna: «calculada» solo con contraste; si un contraste mueve el precio de Sí a dos decimales y lo juzgo no material, es juicio económico.

- **N1 tipo** (variación conjunta necesaria · calculada / juicio · +1,75 € sin N1). La media de 2023–2025 da 22,05 %; el tipo de la Historia mete 2021–2022 con Italia. Con fundamento; no material para ninguno de los dos.
- **N1 escudo** (aislado · calculada / juicio · −0,08 €). Convención inmaterial.
- **N2** (aislado · calculada / juicio · −0,94 €). Margen de partida de continuadas, no mi objetivo. Con fundamento; no material.
- **N3 regla R1** (variación conjunta necesaria · calculada / juicio · −1,35 € de efecto propio, por diferencia de dos pares calculados; solo en el MALO). La juzgo con fundamento suficiente: un horno no devuelve caja cuando caen las ventas y R0 libera capital fijo (aviso en sus tres variantes). Discrepa de la «hipótesis» de la configuración; resuelto en el JSON sin decidir D-N3.
- **N3 circulante** (solo variación conjunta · juicio / juicio). 14,70 % en 2025 y 14,88 % en 2024. Con R1 solo pesa en lo que se libera al caer las ventas. No material.
- **PM1.estructura** (aislada · calculada / calculada): S −0,50 · SR2 +1,06 · SRF +2,41 · H +5,35 · sin requisito +7,10 €. No material para la acción; material para el objetivo. Técnico, sin fundamento suficiente.
- **PM1.familia** (solo variación conjunta · juicio / juicio). Θ no se calcula y quitar toda P-M1 no mide la familia. Ningún requisito no negativo sube el precio de Sí sobre 63,11 €, y el capex supera la amortización desde 2017: no puede cambiar la acción. Material para el objetivo y sin fundamento. Es la única condicionante que el ámbito calculado no cubre.
- **PM1.parametro λ** (aislado · calculada / calculada): +2,37 € (1,10) a −4,73 € (1,25). Material para el objetivo y sin fundamento. Si todo el exceso fijo de 2021–2025 fuera reposición, λ ≈ 1,46: el rango puede quedarse corto por arriba.
- **Convenciones** de años (−0,13 €) y de terminal (+0,40 €), y **cartera P0** (−0,54 €): con fundamento; no materiales (juicio, porque mueven el precio de Sí a dos decimales).
- **PM1.roic_terminal** (SR2 · variación conjunta necesaria · calculada / juicio · +1,06 €). Q-ROIC1 sigue abierta (corrección 4.13 §1): ROIC neto de reposición → SR1; medido sobre una inversión que la incluye → SR2. El 9 % es convención sin base de medición; el 12 % del BUENO sale del ROIC histórico sobre todo el capital, y SR1 reestima el S2C elegido con la misma base. Apunta a SR2 sin decidir. Sin fundamento suficiente, confianza baja (discrepancia resuelta). No material para el objetivo: su alternativa está dentro de la hipótesis de estructura, que ya lo condiciona.

**Mantenimiento.** *¿La reposición supera la amortización?* En dirección, sí; en magnitud, no lo sé.
- El capex supera la amortización todos los años desde 2017 (1,10 a 1,74 veces). En 2021–2025 fueron 739,0 frente a 509,6 mm (Historia filas 8 y 12).
- El exceso aparece también en los años sin crecimiento: 50,1 mm en 2020 y 55,6 en 2025, con la renovación de hornos como destino principal de 2025 [ES, PDF p. 50].
- Siguen en uso 627 mm de activos totalmente amortizados [ES, PDF p. 51] y los hornos duran hasta 15 años [ES, PDF p. 168]: reconstruir uno hoy cuesta más que su coste histórico.
- En contra de atribuirlo todo a la reposición: el calendario de hornos [ES, PDF p. 180], la descarbonización [ES, PDF p. 173], Brasil y el supuesto del 8 % de 2019. λ = 1,15 atribuye 75,0 de los 229,4 mm de exceso.

*¿Qué estructura?* No hay base para nombrar una.
- **S** es la menos coherente: el S2C histórico ya lleva el exceso de capex en el denominador y S lo carga otra vez.
- **H** no queda excluida por 2025: en un año sin crecimiento también paga todo el requisito. La distinguirían los años con crecimiento y saber si reconstruir un horno añade capacidad; 2021–2024 crecieron sobre todo por precio y por Brasil, y no hay toneladas.
- **SR1 frente a SRF** depende de la mezcla: quitan el 14,2 % de la reinversión total y el 29,9 % de la fija, con denominadores distintos, y la mezcla futura (13–15 % circulante) no es la histórica (52,6 %). Si la reposición acompaña a la inversión fija, SRF; si a la total, SR1. Es hipótesis, no hecho.
- **SR1 frente a SR2** es Q-ROIC1.

`estructura_mas_coherente = null`, `adoptada = false`. «When you don't know and you don't have any special competence, don't be afraid to say so» (PCA p.272; HIM).

**Avisos de dominio.** Ninguno es material.
- *En la activa:* el factor de reestimación (f = 1,165; deja de estar definido en λ = 2,06) explica G8 y condiciona el objetivo a través de λ y de la estructura, ya condicionantes. Con λ ≈ 1,46, f sería ≈ 1,76 y perdería sentido. El terminal de R1 y s2c_inerte se compensan (~1 € cada uno).
- *En las variantes:* inversion_fija_para_crecer_negativa solo aparece con R0 (solo_N1, solo_N2, activa_R0_sin_PM1), que forman el extremo superior del rango, el menos creíble. El factor de reestimación se lee en la activa y en diez variantes (f de 1,000 a 1,309): afecta al valor de la activa y al extremo inferior (parametro_maximo, 51,29 €) sin salir del dominio. Los dos avisos de R1 desplazan la activa y el rango de forma uniforme.
- Las lecturas con bases parciales (G7, referencias mecánicas, valor sin crecimiento sin P0) no comprueban el modelo experimental.

**Objetivo.** Protocolo `objetivo_condicionado`. Condicionan el objetivo PM1.estructura, PM1.familia y PM1.parametro. La acción se sostiene en las 19 variantes y ningún condicionante es material para la acción. No hubo comprobación conjunta. Tratamiento: **objetivo_condicionado**, con 56,02 € como objetivo condicionado (provisional). «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 10. Turno 2 · conclusión

**Comprobación conjunta:** no se ejecutó porque no procedía con `esperar`. No existe `comprobacion_conjunta.json`, así que `sobrevive = null` y `resultado = no_procede`.

**Estado: concluido (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 56,02 €, condicionado.**
- No hay bloqueo, límite del modelo, descalificador ni dato ausente material.
- La lista D10 está vacía.
- La zona es «caro».
- Con el protocolo `objetivo_condicionado`, el precio de Sí se emite como objetivo condicionado a la reposición de hornos. Es posible porque la acción se sostiene en las 19 variantes calculadas (precio de Sí de 51,29 a 65,72 €, todas «caro»). Ese rango es el de la tabla de variantes: no es un intervalo de confianza ni cubre hipótesis no exploradas. PM1.familia no tiene contraste aislado.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 56.02 · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional) …». La posición es de José Luis. «If you wait, I think you'll get your price» (DR p.29; AUTHOR).

**C93 = Sí.** g es el 2 %, bajo la tasa sin riesgo (2,85 %). El terminal reinvierte el 22 % del NOPAT más la reposición y pesa el 48 % del valor. Desde el año 11 el capital nuevo rinde el 9 %: crecer aporta poco, pero no nada (+0,88 € de valor NORMAL). **C103 = No:** es cíclica, con margen ligado a la energía y foso estrecho; es propiedad del negocio.

**Insumos para José Luis:** precio 90,10 €; zona caro; precio de Sí 56,02 € (37,83 % por debajo del precio, sobre el precio); precio del escenario MALO 44,32 € (no es un suelo de valor); ponderado 60,70 €; r = 0,09 frente a una r mínima de 0,0817; palanca más influyente del tornado, el ROIC a largo plazo (información). Confianza global: media.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil. Ningún cliente pasa del 10 % de las ventas [ES, PDF p. 104] y lleva diez años con ROIC sobre el sector (13,8 % frente a 9,3 %; Historia C55, Palancas H18). Leo que gana por fabricar cerca del cliente y trasladar la energía con retraso: 13,7 % de margen en 2022 y 20,8 % en 2024 (Historia I29, K29). Pero el 19,9 % de 2025 está junto al máximo, con 43,1 mm de «Otros» sin explicar [ES, PDF p. 79] y bajadas de precio supuestas para 2026 [ES, PDF p. 54]. A 90,10 € pago más que mi BUENO (78,52 €): el precio descuenta un 14,2 % anual de crecimiento de ventas. Espero hasta 56,02 €, un objetivo condicionado a la reposición de hornos.

**Tesis inversa (B102).** El No, con hechos:
- Producto poco diferenciado en un mercado maduro [ES, PDF p. 55], con consumo por debajo de lo previsto [ES, PDF p. 94] y ventas orgánicas del −5,4 % [ES, PDF p. 88].
- Margen que es energía barata camino del cliente [ES, PDF p. 54 y p. 56], con 2,9 puntos de «Otros» que nadie explica [ES, PDF p. 79].
- Hornos que se comen la caja: capex sobre la amortización desde 2017 y 1,42 veces en 2025 con ventas a la baja (Historia L12, L8); 627 mm de activos amortizados en uso [ES, PDF p. 51]; mi modelo solo carga como reposición un tercio del exceso de 2021–2025.
- Clientes que ganan fuerza [CF_2019, PDF p. 67; CF_2024, PDF p. 45].
- Crecimiento donde el foso no está probado [ES, PDF p. 106, p. 105 y p. 85].
- Un ROIC que en 2016–2017 era la tasa (Historia C33:D33) y ningún competidor con nombre (extracto §9).

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Los dos errores.** El que tengo más cerca es pagar cualquier cosa por calidad: el precio paga más que mi mejor escenario. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 12. Predicciones (dado el NORMAL; autopsia el 30-abr-2028)

1. El margen operativo de 2027 queda entre el 16 % y el 20 %. Probabilidad 0,7: cinco de los siete años de 2019–2025 cayeron en esa banda (Historia F29:L29).
2. La variación orgánica de las ventas de 2027 queda entre −2 % y +4 %. Probabilidad 0,65: el NORMAL crece un 1,5 %, pero la energía ha movido mucho las ventas (Historia fila 28).
3. Los pagos por inmovilizado de 2027 superan 1,2 veces la amortización. Probabilidad 0,7: seis de los nueve años de 2017–2025 lo superaron (Historia filas 8 y 12), aunque el calendario de hornos puede dejar un año por debajo [ES, PDF p. 180]. Pone a prueba la reposición, sin distinguir entre estructuras.

La fecha deja tiempo para las cuentas de 2027: las de 2024 se aprobaron en abril de 2025 [ES, PDF p. 70]. Son la autopsia de este análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 13. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo de 56,02 € sin que cambie el negocio. El umbral subiría con un capex desglosado que sitúe la reposición cerca de la amortización (λ 1,10: 58,38 €), con la prueba de que reconstruir un horno añade capacidad (H: 61,37 €) o con un margen de 2026–2027 del 18 % o más con energía normal.
- **A No:** un margen por debajo del 14 % sin choque de energía; dos años más de capex por encima de 1,4 veces la amortización con ventas planas; datos de cuota que muestren pérdida; o los diez mayores clientes por encima del 40 % con margen a la baja.
- **A Demasiado difícil:** que el valor pase a depender de Brasil y Chile; un exceso de capacidad duradero en los competidores; o una sustitución del vidrio que no sepa juzgar.

**B222:** el 18 % del NORMAL como media de un ciclo que vuelve (Palancas!C15), más la reposición, que condiciona el objetivo sin base para elegir estructura. **B223:** precio y coste de energía por tonelada y segmento de 2019–2025, cláusulas de traslado, desglose de los «Otros» y del capex por destino, coste de reconstruir hoy un horno, toneladas que añade cada reconstrucción y serie de toneladas vendidas (preguntas a Relación con Inversores).

## 14. Comparación con la etapa 1

Mismo cubo, Vigilar, y por la misma razón. El precio de Sí pasa de ~48 € a 56,02 € por tres cambios:
- La regla: la escalera k = 3 sustituye al mínimo entre el MALO y ¾ del ponderado.
- El modelo: motor B con palancas.
- La configuración experimental: resta 8,73 € frente al modo heredado (64,75 €), sobre todo por la reposición.

Mi NORMAL (60,21 €) queda por debajo del valor normal de la etapa 1 (~74 €): el margen va a la media del ciclo y el capital nuevo rinde la tasa desde el año 11. La etapa 1 usaba hechos posteriores a la base; yo no. Mantengo C93 y C103 y reescribo B101, B102 y C104, este último sin porcentaje.
