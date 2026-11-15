# Fase C · turno 1 · Vidrala, S.A. (VID) · base económica 31-dic-2025 · V6.4 experimental, motor B

Reviso las fases A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Hechos de `datos_v63.md` (Historia, anclas), de `extracto_v63.md` ([ES, PDF p. n] y [CF_aaaa, PDF p. n]) y de lo que calcula la hoja (`resultados.json`, `precio.json`, `configuracion_v64_variantes.md`). Los cálculos marcados «míos» son aproximaciones con la sensibilidad del tornado o con la fórmula de la escalera; no son recálculos del libro.

## 1. Una sola historia

**Lo que calcula la hoja.** Valor por acción 44,32 / 60,21 / 78,52 € (MALO / NORMAL / BUENO), ponderado 60,70 €, precio de Sí 56,02 € (P\*, sin tope del NORMAL), precio 90,10 €: zona **caro**. 90,10 está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí); el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio). La regla antigua (C156) da 44,32. Peso del terminal: 41 / 48 / 54 %, todos por debajo del 75 %. Semáforos: margen en REVISAR en los tres escenarios (G5, justificado en la fase B: Vidrala está por encima del Q3 del sector todos los años), f = −2,8 % en REVISAR (es la razón del motor B), cuota implícita sin calcular (C24 vacía); el resto pasa. Estado técnico INCOMPLETO solo por las predicciones, que son del turno 2. La hoja dice «DESCARTADA POR FILTRO PABRAI» por C13 = No; mi cubo es Vigilar porque C13 mide el precio, no el negocio.

**DCF inverso.** A 90,10 el mercado descuenta un crecimiento de ventas del 14,2 % anual en los años 1–5 con el resto de mi NORMAL; al precio de Sí, −0,8 %. Mi NORMAL crece 1,5 % y el BUENO 3,5 %. El precio supera el valor BUENO de las 15 variantes calculadas (máximo 88,38, solo_N2). Lo que paga el precio: 31,91 € por un crecimiento que en mi NORMAL vale 2,02 € (lectura sin la cartera P0). ¿Quién es el tonto? «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). No hace falta que lo sea nadie: con mi NORMAL, 90,10 equivale a una tasa unos dos puntos más baja que la del motor (≈6,5 % frente a 8,69 %, cálculo mío aproximado) o a un margen que no vuelve a su ciclo. Yo no tengo esa alternativa: «it's your alternatives that matter. That's how we make all of our decisions» (PCA p.114; HIM).

**Tornado (información, no criterio).** Sobre el valor NORMAL: ROIC LP ±5 puntos 12,67 €; tasa ±1 punto 10,56 €; margen ±2 puntos 7,36 €; crecimiento ±2 puntos 3,52 €; S2C ±0,3 2,22 €; g ±0,5 puntos 0,19 €. El del ROIC es asimétrico: hacia abajo (4 %, cerca de g) es grande; hacia arriba es pequeño, porque la reinversión terminal es g ÷ ROIC con g = 2 %: dos puntos más de ROIC NORMAL suben el valor NORMAL unos 1,6 € (cálculo mío). La tasa no es la palanca más influyente.

**¿Cuentan la misma historia que la fase A?** Sí. Un fabricante maduro de un envase pesado, con un margen que sigue a la energía, un foso estrecho que la Historia sostiene y un precio que paga más que mi escenario bueno. Las fricciones que encuentro, ninguna de las cuales cambia el cubo ni la zona:

1. **Rentabilidad marginal.** La fase B escribió ≈13 % (NORMAL), ≈17,6 % (BUENO) y ≈8,4 % (MALO) con las bases heredadas; la hoja calcula 14,7 %, 20,0 % y 9,5 % porque aplica f = 1,165 al S2C (estructura SR1) y el tipo N1 (22,05 %). Las palancas están bien derivadas (la fase B tenía que elegirlas con la base V6.3), pero el salto del año 11 del NORMAL (5,7 puntos) solo pasa de 5 por la configuración.
2. **El MALO y su capex.** Su historia cuenta hornos y electrificación sin ventas detrás. Con R1 y ventas por debajo del máximo conservado, B16 = 0,7 no actúa (aviso s2c_inerte) y ese capex solo entra por la reposición λ (19,9 mm al año, igual en los tres escenarios); por eso su FCF del año 1 (189,1 mm) supera al del NORMAL (178,0). Si fueran 20 mm más al año durante cinco años, el valor MALO bajaría ~2,2 € y el precio de Sí ~1,0 € (−1,8 %, cálculo mío). Ninguna palanca lo expresa.
3. **Perímetro del margen NORMAL.** Palancas!C15 = 0,18 sale de la media de 2019–2025 de la Historia (F29:L29), que lleva Italia hasta 2022; la media de continuadas 2020–2025 es 18,55 % (N2), que redondeada da 0,185. Corregirla subiría el precio de Sí de 56,02 a ~56,81 (+1,4 %, cálculo mío): no cambia cubo ni zona y queda bajo el 5 %, así que la dejo y la registro en `celdas_corregidas`. En sentido contrario empujan los 43,1 mm de «Otros» sin explicar.
4. **B101, B102, C93 y C104** del libro son todavía los textos de la etapa 1, con hechos posteriores a la base (30-jun-2026, 88,7 €, Chile desde el 30-mar-2026). Los reescribo en el turno 2.
5. **C27 = Expandiendo** convive con escenarios que no expanden el margen; la fase A lo explicó (escalón de 2016–2019, ciclo después). No la cambio.
6. **El valor sin crecimiento (58,19 €)** y «cuánto pagas por crecer» son lecturas con base parcial (sin la cartera P0): solo contexto.

## 2. Desviaciones pendientes (G8)

La gramática deja dos: el salto del año 11 del NORMAL (5,7 puntos) y del BUENO (8,0). Las justifico; no muevo palancas.

- **NORMAL (convención).** En los años 1–10 cada euro nuevo rinde 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 %, junto al ROIC de cinco años (13,8 %, Historia C55): la escala regional, que ha sostenido diez años de ROIC por encima del sector (Historia fila 33; Palancas H18, 9,3 %, solo contexto), sigue sirviendo al capital que se reinvierte dentro del plazo del modelo. Desde el año 11 el capital nuevo rinde la tasa (9 %; tasa del motor 8,69 %): la ventaja que pierdo es la de poner capacidad nueva con retorno en exceso en un mercado maduro [ES, PDF p. 55] cuyo competidor más peligroso no conozco (extracto §9). El margen del 18 % sigue sobre el capital instalado. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Con las bases heredadas el salto sería ≈4,0 puntos: el resto lo crea f. Convergencia hacia el coste de capital como criterio, no como ley (MR; E2).
- **BUENO (fundamentada).** 1,1 × 1,165 × 0,20 × (1 − 0,2205) = 20,0 % por euro nuevo porque llena hornos que no iban llenos (la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54]; consumo inferior a lo previsto [ES, PDF p. 94]), suma Brasil al 42,4 % de margen EBITDA [ES, PDF p. 107] y cierra Toro [ES, PDF p. 85]. Esa ventaja es finita: con la capacidad libre usada y Toro integrado, el capital nuevo del año 11 rinde el suelo de la meseta de 2018–2025 (11,9 %, 12,5 %, 12,2 %; Historia E33, I33, J33), tres puntos sobre r. Lo que se pierde en el año 11 es el volumen sin capex, no la ventaja del capital instalado. Sigue por debajo de 2 × C55 (27,7 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

G16 (peso del terminal) y G17 (cuota implícita) no están señalados.

## 3. ¿Hay que mover palancas?

No. Ninguna incoherencia exige números distintos: la del margen NORMAL es de perímetro, pero corregirla mueve el precio de Sí un 1,4 % sin cambiar cubo ni zona (lo dejo escrito con su cálculo, v2.1); la del MALO no tiene palanca que la exprese bajo R1; la de la rentabilidad marginal es de la configuración. `revisar_palancas = false`. En `celdas_corregidas` dejo Palancas!C15 y B16 con `despues = antes` y su motivo. De la fase A no encuentro ninguna celda que impida sostener la conclusión.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Mantuve Vigilar, las opciones de B65:D65 y 0,2/0,6/0,2. El cubo lo sostiene la escalera nueva, no la herencia, y cambié lo que la Historia corregía (C62 a motor B, C97 a Neutral, C76 vacía). Lo más heredado son las probabilidades: con 0,25/0,6/0,15, la sustituta que dejó escrita la fase B, el precio de Sí bajaría a 54,10 (−3,4 %, cálculo mío) y la zona seguiría «caro». Cambio: ninguno.
2. **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 90,10 y del 171,8 de Simply Wall St (C38, posterior a la base). Cambio: ninguno; no bajo r ni subo el NORMAL para acercarme.
3. **Consistencia y compromiso.** La zona es «caro» en las 15 variantes y el precio supera el BUENO de todas; para cumplir la regla a 90,10 haría falta un NORMAL por encima de 90, un 50 % sobre el mío. El cubo no depende de cómo afiné las cifras. Cambio: ninguno.
4. **Historia bonita / viento de cola.** El margen de 2024–2025 coincide con el gas a la baja tras 2022 [ES, PDF p. 56]: es marea. El 42,4 % de Brasil se compró: Vidroporto ya daba 55,5 mm de EBITDA pro forma y costó unas 6,9 veces [ES, PDF p. 36–37]. Lo propio de Vidrala es la vuelta de 2022 a 2024 y diez años de ROIC sobre el sector. Cambio: ninguno en palancas; en la tesis lo atribuiré así.
5. **Optimismo del BUENO frente a la tasa base.** Crece menos que la historia (3,5 % frente al 7,4 % con compras) y su ROIC terminal (12 %) queda bajo C55, pero en los años 1–10 rinde el 20,0 % por euro nuevo, 1,45 veces C55, y la G7 no lo ve porque usa las bases heredadas (17,6 %). Ese 20 % pide hornos sin llenar que no puedo medir. Cambio: ninguno (pesa ~0,14 € de precio de Sí por euro de valor); queda en incoherencias y en G8.
6. **Doble castigo.** NORMAL al 18 %, MALO al 15 %, p(MALO) sin subir, quiebra vacía, r heredada sin prima; la reposición está en SR1 y la fase B no rebajó S2C ni ROIC por lo mismo. g NORMAL al 2 % no castiga: mueve ±0,19 €. Cambio: ninguno.
7. **Disponibilidad.** Kristin, el cierre de Chile y las recompras de 2026 son posteriores a la base y quedan fuera; el apagón de 2025 la empresa lo da por no material [ES, PDF p. 78]. Los 43,1 mm de «Otros» los medí: como mucho ~0,66 puntos en la media del NORMAL y ~1,9 € de precio de Sí. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad.** El NORMAL (1,5 %) está junto a la proyección de la empresa (1,6 % [ES, PDF p. 55]) y usa su volumen del +1 %. Lo sostiene sin la guía: orgánico −5,4 % en 2025 [ES, PDF p. 88], C45 = 2,9 % con Brasil dentro y bajadas de precio supuestas en 2023 que se cumplieron en lo grueso [CF_2023, PDF p. 48]. En contra: Iberia (~4,8 %) y Reino Unido (~10,3 %) crecieron en euros en 2020–2025, sobre todo por precio de la energía. Cambio: ninguno; el crecimiento pesa menos de 1 € de precio de Sí por punto.
9. **¿El MALO es de verdad malo?** 44,32 €, la mitad del precio; margen del 15 % para siempre, por debajo de todos los años salvo 2016, 2017 y 2022; un 24 % bajo el valor sin crecimiento. No es un NORMAL maquillado, aunque con R1 libera circulante y su capex de hornos solo entra por λ. Un MALO al 13,7 % de 2022 bajaría el precio de Sí ~2 €. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno.
10. **Lo no numerable.** La concentración de clientes sube: los diez mayores de ~30 % (2019) a ~38 % (2024) y «algo más del 35 %» (2025), y el percentil 50 de 27 a cerca de 20 clientes [CF_2019, PDF p. 67; CF_2024, PDF p. 45; ES, PDF p. 104]. Más poder del cliente para quedarse la mejora. Pesan también la cobertura del 69 % de la energía de 2026 [ES, PDF p. 101] y el CO2. Cambio: irá a la tesis inversa y a lo que me haría cambiar de cubo (turno 2).

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Orden de mando. **Bloqueo:** ninguno (gramática sin errores, valor no bloqueado). **Límite del modelo:** no (FCF base positivo, no financiera; el motor B cuadra en las 15 variantes). **Descalificador mío:** ninguno (fase A, sección 3). **Dato ausente material:** ninguno (punto 6). **Fundamento material:** la lista D10 está vacía (punto 7) y con `esperar` no limita. **Zona:** caro. Conclusión provisional: **esperar**, con el precio de Sí (56,02) como objetivo, que la configuración experimental condiciona (punto 9). «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM). Aquí ni siquiera es maravillosa: es buena y cíclica.

## 6. Datos ausentes (S-19)

Reviso los 30 de `datos_ausentes.json`; ninguno es material para esperar con objetivo. Los seis de evidencia de la Historia no tocan el valor del motor B o están confirmados en la base por el extracto (arrendamientos de 49,3 mm, minoritarios cero [ES, PDF p. 72 y p. 10]). Lo que más pesa:

- **Cuota y competidores.** Es el hueco mayor y lo que me llevaría a No o a Demasiado difícil, pero no deja el objetivo sin base: los márgenes de los tres escenarios salen de diez años propios que ya contienen la respuesta de la competencia a un choque de energía completo (13,7 % en 2022, 20,8 % en 2024), el NORMAL no da retorno en exceso al capital nuevo desde el año 11 y el precio supera todos los BUENO calculados.
- **«Otros» ingresos (43,1 mm en 2025, 26,2 en 2024 [ES, PDF p. 79]).** En el peor caso (todo no recurrente) el precio de Sí bajaría ~1,9 € (−3,3 %); aparece los dos años, así que algo es recurrente. «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM) vale también al revés.
- **Capex por destino.** Es la información que fundaría la reposición; la trato como hipótesis sin fundamento suficiente en la configuración (punto 9), no como dato que bloquee: la acción no depende de él.
- **Ingresos diferidos.** La diferencia cuadra: 41,117 − 23,115 = 18,002 mm, los créditos fiscales por inversiones que el epígrafe incluye [ES, PDF p. 10 y p. 71].

`alguno_material = false`.

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B (palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas). Todas son «fundamentada» o «convención» con hechos en el apoyo; ninguna narrativa es genérica (cada una tiene mecanismo, dueño de la mejora y «qué lo pararía» con páginas). Miré con lupa las más débiles y no las incluyo, por esto:

- **B69:D69 (0,2/0,6/0,2):** convención argumentada (no contar dos veces el pico de margen) con hechos de la fila 29; la alternativa escrita (0,25/0,6/0,15) mueve el precio de Sí −3,4 %.
- **B16 (S2C MALO):** no actúa con R1; efecto nulo, no es material.
- **D16 (S2C BUENO 1,1):** la magnitud sale de la banda del ejercicio y Toro (0,91) va en contra; pero un S2C BUENO 0,3 más bajo mueve el precio de Sí ~0,4 €: no es material.
- **D66 (la empresa se queda la mejora en Brasil y Chile):** lo apoya el margen de Brasil de 2024–2025, no la estructura competitiva, que no conozco; el BUENO mueve poco el precio de Sí.

Lista vacía. Con `esperar`, `resultado = no_procede` y la comprobación conjunta no procede (`sobrevive = null`). Los parámetros experimentales sin fundamento suficiente no entran en D10 con `esperar`; condicionan el objetivo por el protocolo (punto 9).

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis fundamentada de la que más depende la conclusión, a mi juicio, es **Palancas!C15: el 18 % del NORMAL es la media de un ciclo que vuelve, no un nivel nuevo**. Es la diferencia entre mi lectura y la del precio, y la que decide quién se queda la mejora: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM). Dos puntos más (el nivel de 2024–2025) subirían el precio de Sí a ~59,2 € (cálculo mío), lejos aún de 90,10. Lo resolvería: la serie 2019–2025 de precio medio y de coste de energía por tonelada por segmento, con las cláusulas de traslado de los contratos (pregunta a Relación con Inversores), y la explicación de los 43,1 mm de «Otros».

## 9. Configuración V6.4 experimental

**Variantes.** Las 15 calculadas dan «caro» (precio de Sí de 51,29 a 65,72; la activa, 56,02). La tabla no es un intervalo de confianza ni prueba robustez frente a hipótesis no exploradas.

**Parámetros** (Δ del precio de Sí con su variante):
- N1 tipo (22,05 %, media 2023–2025 de la fila de tipo impositivo: 20,4 / 21,4 / 24,3 %; lo compruebo) y escudo vinculado: −1,71 € frente al heredado. Fundamentado; no material.
- N2 (m0 18,55 %): +0,97 €. Fundamentado; no material. Es margen de partida, no mi objetivo.
- N3 regla R1: −1,36 €, solo en el MALO; va del lado prudente y encaja con hornos específicos que se conservan [ES, PDF p. 168 y p. 94]. Circulante 14,70 % de las ventas: lo recalculo con el balance [ES, PDF p. 9 y p. 10] y cuadra.
- **PM1.estructura** (SR1): −7,10 € frente a sin requisito; S 55,52 · SR1 56,02 · SR2 57,08 · SRF 58,43 · H 61,37. **PM1.familia** (Λ): no se aísla; P-M1 entero, −6,61 €. **PM1.parametro** (λ 1,15): de +2,37 € (1,10) a −4,73 € (1,25). Los tres son técnicos, de confianza baja, materiales para el objetivo y **sin fundamento suficiente**: falta el desglose del capex por destino y el coste de reponer un horno hoy frente a su coste histórico.
- Convenciones de años (−0,13 €) y de terminal (+0,40 €), ROIC terminal (SR2, +1,06 €) y cartera P0 (+0,49 €): no materiales.
- Ninguno es material para la acción: todas las variantes que los varían dan «caro».

**Mantenimiento.** La reposición supera la amortización: capex de 1,10 veces la amortización o más todos los años desde 2017 y de 1,45 veces en 2021–2025 (739,0 frente a 509,6 mm, Historia filas 8 y 12); en 2025, 1,42 veces con ventas orgánicas −5,4 % y con la renovación de hornos como destino principal [ES, PDF p. 50]; 627 mm de inmovilizado amortizado en uso [ES, PDF p. 51]. En contra, la empresa suponía en 2019 que un capex del 8 % de las ventas bastaba para mantener y crecer [CF_2019, PDF p. 44], por debajo de su amortización de entonces: es supuesto del vendedor. La magnitud no la mido: λ = 1,15 es un tercio del exceso histórico (75,0 de 229,4 mm); todo el exceso daría λ ≈ 1,46. Estructura más coherente: **SR1**, con confianza baja. H no encaja (en 2025 el exceso se dio sin crecer); S cuenta dos veces (C53 ya lleva el exceso); SR1 quita del crecimiento justo el exceso histórico por euro de ventas añadido (75,0 ÷ 476,8 = 0,157 €); SRF quita unos 0,29 € por euro, más de lo que muestra la historia; SR2 corrige un ROIC que en el NORMAL es convención. No se adopta nada.

**Avisos de dominio.** Factor de reestimación (f = 1,165; deja de estar definido en λ ≈ 2,06): explica G8 del NORMAL; no material. Terminal R1 sin máximo conservado: el MALO carga 15,8 mm de inversión para crecer al 1 % con ventas bajo el máximo; prudente; no material. S2C inerte en el MALO: la incoherencia 2 del punto 1, ~1,0 € de precio de Sí; no material. Las lecturas con bases parciales (G7, referencias mecánicas, valor sin crecimiento sin P0) no las presento como comprobación del modelo experimental; rehecha con f y N1, la rentabilidad marginal del BUENO es 20,0 % frente a 2 × C55 = 27,7 %.

**Objetivo (protocolo `objetivo_condicionado`, ensayo).** Esperar por precio; lo condicionan PM1.estructura, PM1.familia y PM1.parametro; la acción se sostiene en las 14 variantes del ámbito: tratamiento **objetivo_condicionado**, con el precio de Sí (56,02) como objetivo condicionado. «Better roughly right than precisely wrong» (PCA p.451; HIM).

## 10. Turno 2 · conclusión

**Comprobación conjunta:** no se ejecutó (no procedía con `esperar`); no hay `comprobacion_conjunta.json` y `sobrevive` queda `null`. `resultado = no_procede`.

**Estado: concluido (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 56,02 €, condicionado.** Sin bloqueo, sin límite del modelo, sin descalificador, sin dato ausente material y con la lista D10 vacía; la zona es «caro». Con el protocolo experimental `objetivo_condicionado` el precio de Sí se emite como objetivo condicionado a la reposición de hornos (PM1.estructura, PM1.familia y PM1.parametro), porque la acción se sostiene en las 14 variantes calculadas (precio de Sí de 51,29 a 65,72, todas «caro»). Ese rango es el de la tabla de variantes: no es un intervalo de confianza ni cubre hipótesis no exploradas. C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 56.02 · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional) …». La posición es de José Luis. «If you wait, I think you'll get your price» (DR p.29; AUTHOR).

C93 = Sí: g del 2 % bajo la tasa sin riesgo (2,85 %), reinversión terminal del 22 % con ROIC 0,09, peso del terminal del 48 %; el salto del año 11 es la convención del capital nuevo a la tasa. C103 = No: cíclica, con margen ligado a la energía y foso estrecho; es propiedad del negocio.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil, con clientes repartidos (ninguno por encima del 10 % [ES, PDF p. 104]) y diez años de ROIC por encima del sector (13,8 % frente al 9,3 %; Historia C55, Palancas H18). Leo que gana porque fabrica cerca del cliente y traslada la energía con retraso: el margen cayó al 13,7 % en 2022 y volvió al 20,8 % en 2024 (Historia I29, K29). El 19,9 % de 2025 está junto al máximo con el gas a la baja y la empresa supone bajadas de precio en 2026 [ES, PDF p. 54]: mi NORMAL lo deja en el 18 % y desde el año 11 el capital nuevo rinde la tasa. A 90,10 € pago más que mi BUENO (78,52 €). Espero hasta 56,02 €, un objetivo condicionado a la reposición de hornos.

**Tesis inversa (B102).** El No, con hechos: producto poco diferenciado en un mercado maduro [ES, PDF p. 55], consumo inferior a lo previsto y capacidad que se adapta [ES, PDF p. 94], ventas orgánicas −5,4 % [ES, PDF p. 88]; un margen que es energía barata camino del cliente [ES, PDF p. 54 y p. 56], con 2,9 puntos de «Otros» que nadie explica [ES, PDF p. 79]; hornos que se comen la caja (capex de 1,42 veces la amortización con ventas a la baja, Historia L12 y L8; 627 mm amortizados en uso y 66,6 mm comprometidos [ES, PDF p. 51]); clientes que ganan fuerza (diez mayores de ~30 % a ~38 % en 2019–2024 [CF_2019, PDF p. 67; CF_2024, PDF p. 45]); crecimiento buscado donde no hay foso probado (real −20 % en 2024, deuda a CDI, Toro con plan de ajuste [ES, PDF p. 106, p. 105 y p. 85]); un ROIC que en 2016–2017 era la tasa (Historia C33:D33); y ningún competidor con nombre. «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Los dos errores.** Sigo más cerca de pagar cualquier cosa por calidad: el precio paga más que mi mejor escenario. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 12. Predicciones (dado el NORMAL; autopsia el 31-mar-2028)

1. Margen operativo de 2027 entre el 16 % y el 20 %. Probabilidad 0,7: cinco de siete años de 2019–2025 cayeron ahí (Historia F29:L29).
2. Ventas orgánicas de 2027 entre −2 % y +4 % frente a 2026. Probabilidad 0,65: el NORMAL crece 1,5 %, pero el precio de la energía ha movido mucho las ventas (Historia fila 28).
3. Capex de 2027 por encima de 1,2 veces la amortización. Probabilidad 0,7: pone a prueba la reposición (seis de los últimos nueve años lo superaron, Historia filas 8 y 12; 2025 tuvo menos hornos que 2024 [ES, PDF p. 180]).

Son la autopsia del análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 13. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo de 56,02 € sin que cambie el negocio; el umbral subiría con un capex desglosado que sitúe la reposición cerca de la amortización o con un margen de 2026–2027 del 18 % o más con las bajadas de precio aplicadas.
- **A No:** margen bajo el 14 % sin choque de energía; dos años más de capex por encima de 1,4 veces la amortización con ventas planas y ROIC hacia la tasa; datos de cuota que muestren pérdida.
- **A Demasiado difícil:** que el valor pase a depender de Brasil y Chile, con su divisa y su deuda; exceso de capacidad duradero de competidores; sustitución del vidrio que no sepa juzgar.

B222: el 18 % del NORMAL como media de un ciclo que vuelve (Palancas!C15), y la reposición que condiciona el objetivo. B223: precio y coste de energía por tonelada por segmento en 2019–2025, cláusulas de traslado, desglose de los 43,1 mm de «Otros» y del capex por destino, con el coste de reconstruir hoy un horno (Relación con Inversores).

## 14. Comparación con la etapa 1

Mismo cubo, Vigilar, y por la misma razón. El precio de Sí pasa de ~48 € a 56,02 €. La regla cambia: el mínimo del MALO y ¾ del ponderado pasa a la escalera k = 3, que queda por encima del MALO (44,32). El modelo cambia: motor B con palancas. Y la configuración experimental resta 8,73 € frente al modo heredado (64,75) por la reposición, el tipo y R1. Mi NORMAL (60,21 €) está por debajo del valor normal de la etapa 1 (~74 €): el margen va a la media del ciclo y el capital nuevo rinde la tasa desde el año 11. La etapa 1 usaba hechos posteriores a la base (Chile desde marzo de 2026, deuda de junio de 2026, 88,7 €); yo no. Mantengo C93 y C103; reescribo B101, B102 y C104 (este sin porcentaje).
