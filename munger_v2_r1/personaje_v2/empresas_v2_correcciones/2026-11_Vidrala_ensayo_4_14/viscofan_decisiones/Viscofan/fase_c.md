# Viscofan, S.A. · fase C · turnos 1 y 2 · expediente de decisiones (rama 4.14 con D3 y E1) · 2026-11-14 · motor B · V6.4.1 experimental

Base económica: 31-dic-2025. Precio: 54,70 € del 3-nov-2026 (boletín de cotización de BME, PDF p. 3). Acciones: 45,993399 M en circulación a 31-dic-2025, por la decisión D3 de la persona responsable. Son fechas distintas: esto no es una actualización a 2026. Lo posterior a la base no apoya ningún juicio. «Historia» es la hoja de diez años de `datos_v63.md` (C = 2016 … L = 2025), con los datos corregidos de la rama. Reviso las fases A y B, que no cambian ninguna celda frente a la rama, como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Parto de la fase C de la rama 4.14 (copiada aquí como `fase_c.rama.json` y `fase_c.rama.md`). Conservo lo que sigue valiendo con las cifras nuevas y cambio solo lo que invalidan D3 y E1 (última sección).

## 1. Una sola historia

Lo que calcula la hoja: MALO 29,78 €, NORMAL 43,77 €, BUENO 57,95 €, ponderado 43,81 € (B78:D78, C83), frente a 54,70 €. El precio está por encima del NORMAL y del ponderado; solo el BUENO lo supera. Es la historia de la fase A: un buen negocio de nicho, con un foso estrecho, un margen que se ha estrechado y un precio sin margen de seguridad (C13 = No, C20 = Riesgo real alto).

- **Peso del terminal:** 49 % / 58 % / 63 %. Ninguno pasa del 75 %: no hay G16.
- **Salto del año 11:** 1,7 / 4,7 / 8,3 puntos. La rentabilidad marginal de los años 1–10 (9,7 %, 15,7 % y 20,3 %, con f = 1,1136 y t = 22,12 %) baja al ROIC terminal (8 %, 11 %, 12 %). Solo el BUENO pasa de 5 puntos (G8, punto 2). Sin f, los saltos serían 0,7 / 3,1 / 6,2 puntos: el BUENO pasa igual. D3 y E1 no mueven estas cifras.
- **DCF inverso:** con el margen, el S2C y el terminal del NORMAL, 54,70 € descuentan un 10,1 % anual de crecimiento de ventas en los años 1–5 (C86 = 0,1009). Es más que mi BUENO (7 %) y que la mejor racha de la década (5,8 % anual en 2016–2021 [cálculo, Historia ventas]). El precio de Sí descuenta un 2,0 %. Se paga por crecer 2,2 veces lo que vale el crecimiento del NORMAL (20,42 € frente a 9,48 €).
- **Tornado:** la palanca que más mueve el valor es la tasa de descuento (±1 punto: 9,90 €), con la r heredada. Es información, no criterio: el valor depende sobre todo de la rentabilidad exigida. Después vienen el margen (±2 puntos: 6,35 €) y el ROIC terminal (±5 puntos: 5,63 €).
- **Semáforos:** el margen queda por encima del Q3 del sector en los tres escenarios (G5, justificado). La r del 9,0 % queda bajo la r mínima del 9,5 % (heredada; se informa). Están las banderas D84–D86. La cuota implícita queda sin calcular (C24 vacía).
- **Veredicto de la hoja** (A6): «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: buen negocio sin valor claro al precio.
- **Estado:** INCOMPLETO solo por las tres predicciones (Palancas A38:A40), que se escriben en el turno 2. Evidencias INCOMPLETAS (datos 15 de 17; dos no verificables, Historia C23:L23 y C26:L26; punto 6). Sin bloqueo del valor.
- **Bases parciales:** G7 usa el tipo y el S2C de la Historia sin f; las referencias mecánicas del S2C se anclan en Configuración V6.4!B155 (1,0675) sin f. No las presento como comprobación del modelo experimental.

Lo que no cuadra a primera vista, y cómo lo resuelvo:

1. **El capital nuevo del NORMAL rinde más que el de la década.** Rinde un 15,7 % por euro nuevo en los años 1–10 (14,1 % sin f). La rentabilidad incremental fue de ≈9,0 % en 2016–2025 y de ≈7,4 % en 2021–2025, pero de ≈18,9 % en 2019–2025, saliendo del mínimo de margen [cálculo, Historia ebit y capital_invertido, t = 22,12 %]. No es una palanca mal derivada. La incremental fue baja porque el margen de toda la base cayó del 21,1 % al 16,4 % y el circulante subió 106,1 y 90,6 M€ en 2022–2023 (J14 corregido sin la variación de provisiones; CF_2024.txt, PDF p. 9). El NORMAL dice que el margen deja de caer; si sigue cayendo, es el MALO. Es la hipótesis que más condiciona (punto 8).
2. **La configuración ensancha el salto del año 11.** SR1 multiplica por f el S2C de los años y no toca el ROIC del terminal: 1,0 / 1,6 / 2,1 puntos del salto son de f. Las justificaciones de G8 de la fase B usaban las bases heredadas; valen las cifras de la hoja.
3. **El apoyo de B69 está mal casado con la frecuencia.** Llama «márgenes de MALO» a 2019, 2022 y 2023 (15,1–15,7 %), que están dentro del rango del NORMAL de C69, y ningún año llegó al 14 % del MALO (0 de 10). La probabilidad se sostiene por el mecanismo (repercusión parcial en 2022 y 2023 [CF_2022 p. 93; IA_2023 p. 246]) y por no castigar dos veces un margen que ya está bajo el mínimo observado. No es una palanca mal derivada. Con la fórmula de la escalera sobre los V de `precio.json` (`precio_de_si.py`, `p_estrella`): 0,25 / 0,6 / 0,15 da 38,19 € (−1,61 €, −4,0 %); 0,3 / 0,5 / 0,2 da 37,67 € (−5,3 %); 0,15 / 0,6 / 0,25 da 41,65 € (+1,85 €). La zona no cambia con ningún vector (tope del NORMAL, 43,77 €). No pido revisarla; para el objetivo es un límite (punto 9, D7).
4. **El FCF del NORMAL crece un 6,2 % anual y C25 = No.** Es mecánica: el crecimiento baja del 4,5 % al 2 % y con él la reinversión. Además es el flujo de la empresa, no el del accionista de la fila 35.
5. **El MALO vale menos que el valor sin crecimiento** (29,78 € frente a 34,28 €). Es coherente: el margen baja al 14 % y el ROIC terminal (0,08) queda 0,27 puntos bajo la tasa del motor (8,27 %, Diagnóstico V6 C15) por el redondeo. El efecto es pequeño (g = 1 %).
6. **Celdas de la fase C en el libro** (B101, B102, C104): son las de la etapa 1, con un precio de Sí de 25,1 € y un «0 %». Se reescriben en el turno 2.
7. **Recompras por encima de mi valor.** Fueron 94,0 M€ en 2025 (extracto: AR_2025 p. 144), con un precio medio diario de 59,47 € (p. 147). La nota 12.4 da el coste de las 1.599.709 acciones compradas: 93.752 miles de € (AR_2025.txt, PDF p. 83; el número de acciones también en PDF p. 143), ≈58,6 € por acción [cálculo]. Las dos cifras superan mi NORMAL (43,77 €). Absorben sobre todo el dividendo en acciones (nota de C28): C98 se queda en el borde, pero va a lo no numerable.
8. **Acciones: decisión D3 de la persona responsable (14-nov-2026), ya no pendiente.**
   - C55 = 45,993399 M, las acciones en circulación a 31-dic-2025: 46.500.000 emitidas − 506.601 propias (AR_2025.txt, PDF pp. 76, 83).
   - Sustituye a la media «diluida» de la nota 20.2 (45,479209 M), que contradice su definición porque queda por debajo de la básica (45,656226).
   - C41 = 54,70 € × 45,993399 M = 2.515,8 M€.
   - **Efecto medido** sobre la rama (`resultados/efecto_decisiones_viscofan.json`): el precio de Sí pasa de 40,30282 a 39,79819 € (−0,50462 €, −1,25 %). Por separado, el denominador con E fijo resta 0,45057 € y la capitalización 0,05466 €. La capitalización actúa por la r operativa (Diagnóstico V6 C15: 8,2603 % → 8,2677 %), y los dos efectos no suman exactamente el conjunto.
   - **Fechas distintas.** El precio es del 3-nov-2026 y las acciones son las de las cuentas de 2025: no es una actualización a 2026. La autocartera al 3-nov-2026 no consta. La última cifra oficial anterior al precio es la de 30-jun-2026: 46.000.000 emitidas tras la amortización de mayo de 2026 y 396.357 propias, 45,603643 M en circulación (`datos_v63.md` §2, evidencia de C41). No la adopto: D3 fija la base de 2025. Con ese divisor el precio de Sí subiría ≈+0,34 € por el solo denominador [estimación proporcional mía con E fijo: 39,79819 × 45,993399 ÷ 45,603643; no la calcula la hoja ni ninguna variante]. La hoja lo avisa: «Precio y acciones con fechas separadas más de 90 días (Palancas C45, C46)».
   - **Dilución potencial**, declarada aparte y no adoptada. El plan de incentivos 2025–2027 prevé hasta 315.000 acciones (incentivo objetivo) o 472.500 (máximo), que se entregan en el primer semestre de 2028. La nota no dice si se entregarán con autocartera o con acciones nuevas (AR_2025.txt, PDF pp. 129–130). Con ellas, el precio de Sí sería 39,52748 € (−0,27 €) o 39,39350 € (−0,40 €), siempre en caro.
   - No cambia mi conclusión: el precio está un 37,4 % por encima del precio de Sí (÷ precio de Sí).
9. **Tipo impositivo.** C52 (19,83 %) incluye el 10,1 % de 2025, por la activación de bases de EE. UU. (extracto: AR_2025 p. 142); la configuración usa 22,12 %.
10. **Datos corregidos de la rama.** Con A y B sin cambios, la rama llevó el precio de Sí de 40,16401 a 40,30282 € (+0,13881 €). De ellos, +0,13437 € son de las pensiones netas: solo L25 entra en el puente, con 14,878 M€ en lugar de 20,989 (AR_2025.txt, PDF pp. 87–88). Los +0,00444 € restantes son del circulante. El puente baja de 279,9 a 273,8 M€ y D3 no lo toca. Sobre esa base, este expediente aplica D3 y E1: el precio de Sí pasa de 40,30282 a 39,79819 €. Cambian cifras, no el relato.
11. **E1, medias exactas.** C47–C50 pasan a 77,533 / 8,294 / 5,547 / 3,707 M€. El efecto en el precio de Sí es de 0,000 €, porque solo entran en el FCF del motor A (C52 pasa de 97,29 a 97,22 M€) y el motor es el B.
12. **El divisor en la identificación de la configuración.** La versión auditada de `configuracion_economica.json` → naturaleza terminaba en «N sigue en 45,479209 (VISCOFAN-ACCIONES)», y la sección 14 del informe y la ficha lo copiaban como divisor vigente. El divisor efectivo es Análisis!C55 = 45,993399 M (D3; `resultados.json`), el del libro, `precio.json` y todas mis cifras. La orquestación ya corrigió la frase (cambio editorial; la anterior queda en `configuracion_economica.antes_naturaleza_D3.json`). 45,479209 M es solo la media «diluida» que D3 sustituyó: aquí no figura como acciones activas. No es un fallo de palanca ni de celda de la fase A y no mueve ninguna cifra.
13. **C42 sigue con la capitalización anterior.** EV/EBITDA 9,47 y su evidencia (Control maestro J42; `datos_v63.md` §2) usan 2.487,7 M€ (× 45,479209 M). Con C41 = 2.515,8 M€ el EV sería 2.774,8 M€ y el múltiplo ≈9,57 [cálculo: (2.515,839 + 304,075 + 12,243 − 62,790 + 5,422) ÷ 289,990]. Es un dato de entrada: lo corrige quien escribe las entradas (`cambiar_base.py` o la fase 1), no esta fase. No entra en el motor B: no mueve el precio de Sí, la zona ni el cubo. La Observación de C13 de la fase A lo cita como contraste, y con 9,57 C13 = No se sostiene igual.

Las 52 celdas cuentan una sola historia. No pido mover ninguna palanca.

## 2. Desviaciones pendientes

`gramatica.md` da G8 en el BUENO (8,3 puntos) y las tres G5, ya justificadas en la fase B, que repito con sus hechos. No hay G16 (58 % de terminal en el NORMAL) ni G17 (C24 vacía). D3 y E1 no cambian ninguna de las cifras de estas comprobaciones.

**G8 · BUENO · fundamentada.** En los años 1–10, cada euro nuevo rinde un 20,3 % (1,3 × 1,1136 × 0,18 × (1 − 0,2212)) porque se juntan dos cosas que solo pasan una vez.
- Se llena capacidad construida o comprometida al cierre de 2025: colágeno en EE. UU., plásticos en México y extrusión en Serbia. El 37 % de la inversión de 2025 fue a capacidad y quedan 52,0 M€ de compromisos (extracto: AR_2025 pp. 65, 143).
- El margen sube del 16,4 % al 18 % de 2020–2021 al repartir costes fijos. Es crecimiento por eficiencia, y es finito (GV p. 32; I1).

Con las plantas llenas y el margen en su techo, el euro nuevo vuelve a pagar planta a coste completo: el 12 %, el ROIC del peor año de la década (12,1 % en 2019, F33). En el año 11 no se pierde el foso, porque el 12 % sigue 3,7 puntos sobre la tasa del motor (8,27 %). Lo que se acaba es la capacidad ya pagada y el recorrido del margen. Hay precedente propio en los dos sentidos: un S2C de 1,57 en el ciclo de construir y llenar de 2016–2021 (era 1,70 antes de corregir el circulante de 2019–2020), y una rentabilidad incremental de ≈18,9 % en 2019–2025 frente a ≈9,0 % en la década. Sin f, el salto sería de 6,2 puntos. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Lo contaré en la tesis; no cambio D18.

## 3. ¿Hay que mover palancas?

No. Comprobé la aritmética de la fase B contra la Historia corregida, y todo cuadra:
- C45 = 1,39 % → B14 = 0,015.
- Media del margen de 2019–2025 = 16,44 % → C15 = 0,165.
- La pendiente del margen es de −0,5 puntos al año: en cinco años desde el 16,4 % da ≈13,9 % → B15 = 0,14.
- CAGR de 2016–2021: 5,8 %.
- S2C de 0,86 (2016–2019), 0,98 (2021–2025), 1,57 (2016–2021) y 1,18 (década).
- B155 = 1,0675 × 0,75 / 1 / 1,25 → 0,8 / 1,1 / 1,3.

No hay perímetro ni dato equivocado. Registro en `celdas_corregidas` que revisé C62, C97 y C98 (fase A) y B69 y C15 (fase B), sin cambios. El divisor de acciones (C55) ya no es una duda que deje anotada: lo fija la decisión D3, que es un dato, no una palanca. Lo que queda abierto es fecha y dilución, y lo declaro en el punto 1.8 y en el 9.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** La etapa 1 dejó un precio de Sí de 25,1 € y un «0 %», que el libro aún muestra en B101, B102 y C104. Las celdas que heredan algo tienen motivo propio: C97 y C62 cambian con hechos, y las g con AR_2025 p. 181 e IA_2016 p. 42. También miré el anclaje en la fase C de la rama: la conservo solo donde sigue valiendo con D3 y E1. Cambio: ninguno en celdas; reescribo B101, B102 y C104 en el turno 2.
2. **Anclaje en el precio o en la fuente externa.** El NORMAL queda un 20,0 % bajo el precio y el ponderado un 19,9 % (÷ precio). No usé Simply Wall St (118,26 €) ni el consenso (69,29 €). «Few psychological tendencies do more damage to correct thinking» (PCA p.579; HIM). Cambio: ninguno.
3. **Consistencia y compromiso.** Busqué qué rompería Vigilar: no lo rompe ningún vector de probabilidades (tope del NORMAL) ni ninguna de las dieciocho variantes (38,13–42,98 €, todas en caro). El paso a No depende de si la compresión del margen es estructural, y eso no lo sé. Con la rama: no defiendo lo que D3 invalida y corrijo su cifra de −0,31 €. Cambio: ninguno en celdas.
4. **Historia bonita / viento de cola atribuido a la empresa.** Del 4,5 % del NORMAL, unos 3 puntos son del nicho, 1–1,5 de precio y lo que reste de cuota. Cambio: la tesis lo dirá.
5. **Optimismo del BUENO frente a la tasa base.** El BUENO pide un 7 % anual (la mejor racha dio un 5,8 %) y un 20,3 % por euro nuevo (el mejor ROIC de la década fue un 16,7 %). En el año 10 sería ≈32 % del mercado en valor si este crece un 3 % [cálculo]. Plausible, en el borde. Cambio: ninguno.
6. **Doble castigo del mismo riesgo.** La deuda solo la resta el motor B (puente de 273,8 M€). El margen está como gravedad, no además como frecuencia. Con SR1, la reposición puede contarse en parte dos veces en el terminal (SR2: +0,57 €) (PA pp. 20–21; E6). En el objetivo no cuento dos veces la alternativa SR2 (punto 9). Cambio: anotado en el punto 9.
7. **Disponibilidad (lo vívido del extracto).** Contrasté la «inflación sustancial» de las pieles (AR_2025 p. 436) con la fila 29: la pendiente existe desde 2016, y 2024–2025 están por encima de 2023. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad (guía de la dirección como hecho).** Ninguna palanca copia la guía de 2026. θ = 0,5 no es una medida, y la clasificación de la inversión por tipo que publica la empresa es evidencia, no una medición de la reposición. «will frequently be a lie» (TCI p.60; HIM). Cambio: θ condiciona el objetivo.
9. **¿El MALO es de verdad malo?** En margen, sí: 14 %, bajo el mínimo de la década, y vale 29,78 €. No recoge perder cuota frente a un competidor que no sé nombrar. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: la tesis inversa lo contará.
10. **Lo no numerable que pesa y no está en las palancas.** Pesan:
    - el reparto por encima de la caja con deuda a un año;
    - las recompras a ≈59 €;
    - un «extraordinario» repetido tres años;
    - Danville;
    - un competidor sin nombre;
    - una media de acciones «diluida» publicada que contradice su definición (ya no es el divisor, por D3);
    - una dilución potencial del plan 2025–2027 que no está en el divisor;
    - y, a favor, las compras de directivos.

    «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM). Cambio: va a la tesis inversa y a B222; C98 queda en el borde; la dilución se declara aparte (39,53 / 39,39 €).

## 5. Cubo y conclusión provisionales

En orden de mando:
- **Bloqueo:** no hay (0 errores; el estado INCOMPLETO solo espera las predicciones).
- **Límite del modelo:** no hay.
- **Descalificadores:** ninguno (fase A, sección 3).
- **Dato ausente material:** ninguno (punto 6).
- **Fundamento material:** lista D10 vacía (punto 7).
- **Zona:** caro. 54,70 € está por encima del ponderado (43,81 €). Precio de Sí: 39,80 € (P\*; el tope del NORMAL no actúa). El precio de Sí está un 27,2 % por debajo del precio (÷ precio), y el precio, un 37,4 % por encima del precio de Sí (÷ precio de Sí). Regla antigua (C156): 29,78 €.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`, con precio de Sí ≤ 39,80 €**, objetivo condicionado por la configuración (punto 9). «We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). La escalera es una convención experimental (k = 3). Ni la dilución potencial ni el perímetro cambian la conclusión.

## 6. Datos ausentes (S-19)

Revisé los 27 uno a uno (JSON), los mismos de la rama. Ninguno es material para `esperar` con precio objetivo.
- **Los cinco de la rama:** los ceros de 2016–2018 del pasivo por arrendamientos (antes de la NIIF 16, con los arrendamientos NIC 17 ya en la deuda), del principal de arrendamientos y de la SBC (solo cuentan en el motor A, que usa 2023–2025: C49 = 5,547 y C50 = 3,707 M€, exactos por E1), y los minoritarios de 2019–2022 (el balance de 2021 y 2022 no tiene la línea: CF_2021.txt, PDF p. 3; CF_2022_compilacion.txt, PDF p. 20). El puente usa los saldos de 2025 (L23 = 12,243 y L26 = 5,422 M€), documentados. Dejan las evidencias en «INCOMPLETAS», que se informa.
- **Los que más se acercan a ser materiales:** los competidores y la descomposición de volumen, precio y mezcla, que serían materiales para un `comprar` que dependiera del BUENO o de excluir un MALO de pérdida de cuota; y los covenants, el rating y la renovación de la deuda. C22 = 0 se sostiene con 0,87x EBITDA, 155,3 M€ de líneas libres y sin impagos (AR_2025 pp. 98, 122).
- **Operaciones de directivos:** no son un dato ausente; la evidencia de fase 1 las tiene (Control maestro fila 76).
- **Plan de capex de 2026:** no fundaría θ. Lo que acota θ es el desglose histórico por tipo, que está en el paquete para 2021, 2022, 2023 y 2025. θ es una hipótesis sin fundamento suficiente, no un dato ausente.
- **Fuera de `datos_ausentes.json`:** la autocartera al 3-nov-2026 y la forma de entrega del plan de incentivos no se pueden saber con lo publicado. Las trato como límites declarados de D3 (punto 1.8), no como datos de esta lista.

## 7. Fundamento material (D10)

Recorrí B14:D16, B18:D18, B68:D69, C22, C23, C24, C76, C44, C62, C6, C8 y B65:D66, con las Observaciones de la fase B (B155 = 1,07; tramos del S2C 0,86, 0,98, 1,57 y 1,18). Ninguna celda es «sin juicio propio» ni «técnico», y todas citan hechos con celda o página. Las seis narrativas tienen mecanismo y «qué lo pararía» con hechos propios (extracto: AR_2025 pp. 436, 139, 65, 66, 140, 399). B69 tiene un apoyo de frecuencia mal casado (punto 1.3), pero su mecanismo está en los hechos.

**Lista vacía.** Con conclusión no favorable: `resultado = no_procede`, sin comprobación conjunta y `sobrevive` en null. Los parámetros de la configuración sin fundamento suficiente condicionan el objetivo por el protocolo (punto 9), no por esta lista. D3 y E1 son datos, no hipótesis.

## 8. La hipótesis que más condiciona y qué la resolvería

Por juicio, no por el tornado: **Palancas!C15, que el margen del NORMAL deje de comprimirse en el 16,5 %.** La década muestra 21,1 % → 16,4 %; los siete últimos años, 15,1–18,0 % sin tendencia. Si la compresión es estructural, el NORMAL es el MALO y el cubo es No. «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

**Qué la resolvería:** la descomposición de la variación de ventas y de margen en volumen, precio y mezcla y coste de pieles, por tecnología y región. No se publica (extracto: AR_2025 p. 139) y se pide a Relación con Inversores. Como comprobación, el margen EBIT de 2026 y 2027 frente a la inflación de pieles.

## 9. Configuración V6.4.1 (experimental, no adoptada)

Dieciocho variantes calculadas, todas en caro: precio de Sí de 38,13 € (θ = 1) a 42,98 € (heredado).

**Dos juicios separados.** Para la **acción**, ninguna variante calculada cambia la zona: ningún parámetro es material para la acción. Para el **objetivo** (contrato 4.14), juzgo cada parámetro con su contraste mecánico (`contraste_objetivo_v64.md`, filas nuevas copiadas tal cual en el JSON), lo que ese contraste no cubre y un criterio declarado.

**Criterio (juicio propio, no política: `juicio_propio_del_agente`).** Llamo material para el objetivo a un desplazamiento atribuible del precio de Sí de 1 € o más (≈2,5 % de 39,80 €). No hay ninguna política de materialidad adoptada (D1 pendiente). La razón sale de este expediente. Un solo paso de la lista de probabilidades (0,05 entre las colas) mueve el precio de Sí −1,61 € o +1,85 € [cálculo exacto con `precio_de_si.py` sobre los V de `precio.json`]. Y en esa palanca ya discreparon dos agentes en Viscofan (DECISIONES_PENDIENTES_4_14.md §2.7). Por debajo de 1 €, el número es más preciso de lo que sé. «Better roughly right than precisely wrong» (PCA p.451; HIM). Es el mismo criterio de la rama, y las cifras de D3 y E1 no exigen cambiarlo: ningún contraste atribuible cruza 1 € (el más cercano por debajo, «Caja», queda en +0,65 €). Cuando un parámetro sin fundamento suficiente mueve el precio de Sí y lo juzgo no material, digo con qué lo comparo.

| Parámetro | Contraste atribuible (Δ precio de Sí) | Fundamento | Objetivo: material · base | ¿Condiciona? |
|---|---|---|---|---|
| N1.tipo | activa_sin_N1 +1,51 € | sí | sí · juicio | no (fundado) |
| N1.escudo | escudo_alternativo −0,06 € | sí | no · juicio | no |
| N3.regla | solo_N1 y activa_R0_sin_PM1 +1,67 € | no | no · juicio, comparado con activa_sin_PM1 (+1,67 €: todo es de P-M1) | no |
| N3.circulante | ninguno (solo conjuntas) | sí | no · juicio | no |
| PM1.estructura | H +1,67 · S −0,62 · SRF +1,91 · SR2 +0,57 € | no | sí · juicio | **sí** |
| PM1.familia | ninguno: Λ sin calcular | no | no determinada | **sí** |
| PM1.parametro | θ = 0 +1,67 · θ = 1 −1,67 € | no | sí · juicio | **sí** |
| PM1.convencion_anios | −0,17 € | no | no · juicio, comparado con un paso de probabilidades (1,61 €) | no |
| PM1.convencion_terminal | +0,37 € | sí | no · juicio | no |
| PM1.roic_terminal | estructura_SR2 +0,57 € | no | no · juicio, comparado con PM1.estructura (2,53 €, que ya condiciona) | no |
| PM1.cartera | ninguno (solo heredado) | sí | no · juicio (≈0,03 €) | no |
| PM1.perimetro | «Caja» +0,65 € (1,31 € con θ = 1) | sí | no · juicio | no |

Lo que cambia la lectura de cada uno:

- **N1.tipo** (conjunta necesaria con su escudo): +1,51 €. Es material para el objetivo y está fundado (conciliaciones del impuesto; activación de 18,0 M€ en 2025, extracto: AR_2025 p. 142): no condiciona.
- **N3.regla:** el +1,67 € es de quitar P-M1. R0 y R1 sin P-M1 dan lo mismo al céntimo (41,4698 €), porque con ventas que no caen en ningún escenario R1 no actúa. No tiene fundamento (en 2024 el circulante subió 8,9 M€ con las ventas a la baja, Historia K14 corregido), pero su parte propia del contraste es 0,00 €. Límite: R0 con P-M1 no está especificado.
- **PM1.estructura:** S 39,18 · SR1 39,80 · SR2 40,37 · H 41,47 · SRF 41,71 €. Material y sin fundamento: **condiciona**.
- **PM1.familia:** ninguna variante calcula Λ; λ no se observa. Es inmaterial para la acción: haría falta subir el precio de Sí 14,90 €, casi nueve veces el efecto entero de P-M1. Para el objetivo es **no determinada**: condiciona y no está cubierta por el ámbito.
- **PM1.parametro:** θ = 0 da 41,47 € y θ = 1 da 38,13 €. Material y sin fundamento: **condiciona**.
  - La empresa publica el desglose de su inversión por tipo, y el paquete lo tiene para 2021 (IA_2021_es.txt, PDF p. 213), 2022 (CF_2022_compilacion.txt, PDF p. 202), 2023 (IA_2023_es.txt, PDF p. 250) y 2025 (AR_2025.txt, PDF p. 143).
  - En los cuatro años, lo que no es capacidad queda por debajo de la D&A: 55,3 / 70,3 / 70,3 / 54,8 M€ frente a 72,3 / 78,1 / 83,7 / 85,2 M€ [cálculo]. Apunta a θ bajo, es decir, a un objetivo por encima del activo.
  - No lo fundamenta: «capacidad y maquinaria» puede incluir maquinaria de reposición (solo 2025 dice «aimed at increasing capacity»), la D&A es a coste histórico, 2024 no está en un documento conservado y aceptar el método es una decisión pendiente (D2, D5).
- **PM1.convencion_anios:** −0,17 €. Le doy confianza baja frente a la media de la configuración: la razón de «Plana» no aplica sin ventas a la baja, y la D&A fue el 6,8 % de las ventas en 2016 y en 2025. No tiene fundamento, pero mueve una décima parte de un paso de probabilidades y depende de θ: no material.
- **PM1.convencion_terminal:** +0,37 €. Fundada en el estado estable (CV p. 13; I2). No material.
- **PM1.roic_terminal:** +0,57 €. Le doy confianza baja frente a la media: B18:D18 se anclaron en ROIC sobre todo el capital (Historia fila 33), la lectura en la que Q-ROIC1 pide SR2. Su único contraste es la variante estructura_SR2, una de las estructuras de PM1.estructura, que ya condiciona: nombrarlo aparte contaría dos veces la misma alternativa. No material.
- **PM1.perimetro:** «Caja» da +0,65 €. NIIF 16 es el perímetro coherente con el motor B, y la propia empresa define su CapEx con los derechos de uso (AR_2025.txt, PDF p. 275). Fundado; su efecto solo existe a través de θ. La elección formal es humana (D4).

**Mantenimiento.** La reposición no supera de forma visible a la amortización: el exceso de la década está en los años de capacidad nueva; en 2024, sin crecimiento, la inversión quedó por debajo; en los cuatro años con desglose, lo que no fue capacidad quedó bajo la D&A. No hay hornos. Chequia es reposición pura, pero posterior a la base. Por estructuras:
- S cuenta dos veces el exceso que ya está en el S2C.
- SRF quita ≈0,17 € por euro de crecimiento, el doble del exceso histórico por euro (≈0,096), porque aplica la proporción de reposición a un fijo futuro 1,8 veces el histórico.
- SR1 quita ≈0,093 €.
- Por Q-ROIC1, SR2 es más coherente que SR1.
- H no queda excluida.

El desglose por tipo no separa H de SR2: `estructura_mas_coherente = null`, nada adoptado. D3 y E1 no cambian ninguna base de P-M1.

**Avisos de dominio.** Solo el factor de reestimación (lectura): f = 1,1136 en la activa y de 1,0000 a 1,2562 en las variantes, sin cambios. En el extremo θ = 1 (38,13 €), el NORMAL rendiría un 17,8 % por euro nuevo, el doble de la incremental de la década. Lo digo, pero su incertidumbre es la de θ y no la cuento dos veces. No es material.

**Objetivo.** Protocolo `objetivo_condicionado` (el que declara la configuración; es un ensayo, no una adopción). Lo condicionan PM1.estructura, PM1.familia y PM1.parametro. Ninguno es material para la acción y las dieciocho variantes quedan en caro: la acción se sostiene en el ámbito y el precio de Sí (39,80 €) se emite en el turno 2 como objetivo condicionado. El rango (38,13–42,98 €) es una tabla de sensibilidad, no un intervalo de confianza, y no cubre la familia Λ.

**D3 aplicada: lo que declaro aparte.**
- **Fechas distintas.** El precio es del 3-nov-2026 y las acciones de 31-dic-2025. No es una actualización a 2026: la autocartera de la fecha del precio no consta. La última cifra oficial anterior al precio (30-jun-2026: 46.000.000 emitidas y 396.357 propias, 45,603643 M en circulación; `datos_v63.md` §2) no se adopta ni la calcula ninguna variante: por el solo denominador subiría el precio de Sí ≈+0,34 € [estimación proporcional mía], por debajo de mi criterio de 1 €.
- **Dilución potencial**, no adoptada: 39,53 € con el incentivo objetivo y 39,39 € con el máximo (−0,27 / −0,40 €), fuera de las variantes. Está por debajo de mi criterio de 1 €, así que no la cuento como condicionante del objetivo, pero quien use el objetivo debe saber que, si el plan se entrega con acciones nuevas, el objetivo baja en esa cuantía.

**Límites del objetivo que vienen de decisiones pendientes** (no las adopto; las nombro porque mueven el objetivo o su uso):

- **D7 · probabilidades.** Un paso de la lista mueve el precio de Sí −1,61 / +1,85 €, por encima de mi criterio, y ninguna variante lo contrasta. B69 tiene fundamento (punto 1.3), así que no entra en D10, pero el objetivo no es más preciso que eso.
- **D4 · perímetro** (+0,65 € con «Caja») y **D5 · N1 y θ** (θ ya condiciona).
- **D2 · delimitación de P-M1 y protocolo.** Si la persona responsable decide que la incertidumbre de P-M1 no está delimitada, el objetivo se bloquearía (abstención), aunque la acción «no comprar a 54,70 €» se sostiene en todo el rango calculado.
- **D1 · política de materialidad:** no existe; mi criterio de 1 € es juicio propio.
- **D8 · uso.** La recomendación pendiente es mantener la entrega como experimental y supervisada, no apta para dinero real mientras sigan abiertas D1 y D2. Quien decida con dinero real debe saberlo: este objetivo es condicional y experimental.

## Cambios frente a la rama

Base: `fase_c.rama.json` y `fase_c.rama.md`, copias exactas de la fase C de la rama 4.14 (`…/viscofan/Viscofan`, sin tocar; SHA-256 `3e48cb09…` y `f38d7823…`). Las fases A y B no cambian ninguna celda frente a la rama; cambian los datos C41, C55 y C47–C50 por las decisiones D3 y E1, y con ellos `resultados.json`, `precio.json`, las variantes y el contraste.

**Se conservan los juicios que siguen valiendo:**
- cubo Vigilar y `esperar`;
- lista D10 vacía e hipótesis que más condiciona (C15);
- ningún dato ausente material (los mismos 27);
- las mismas tres hipótesis que condicionan el objetivo y el protocolo `objetivo_condicionado`;
- para cada parámetro, clase, confianza, fundamento, cobertura, ámbito, base y materialidad, para la acción y para el objetivo, y las contradicciones revisadas;
- el criterio de 1 € como `juicio_propio_del_agente`, sin cambios porque ningún contraste atribuible lo cruza.

**Cambia por D3 (decisión de la persona responsable; ya no es una decisión pendiente):**

1. C55 = 45,993399 M en circulación a 31-dic-2025 y C41 = 2.515,8 M€. El precio de Sí pasa de 40,30282 a 39,79819 € (−0,50462 €). Por separado, el denominador resta 0,45057 € y la capitalización 0,05466 €, por la r operativa (8,2603 % → 8,2677 %) (`resultados/efecto_decisiones_viscofan.json`).
2. Se declaran aparte las fechas distintas y la dilución potencial del plan 2025–2027: 39,52748 € (objetivo) y 39,39350 € (máximo), con su fuente (AR_2025.txt, PDF pp. 129–130). No se adopta.
3. Se reescriben los textos que trataban D3 como pendiente: punto 1.8 de la historia; el límite de acciones de cada `juicio_objetivo`; las autocomprobaciones 1, 3 y 10; el motivo del objetivo y el punto 3. D3 sale de la lista de límites por decisiones pendientes.
4. Corrijo una cifra de la rama. Decía «−0,31 €, −0,77 % con los datos de esta rama», pero −0,31 € era la diferencia frente a la activa de la 4.13, no frente a la rama (DECISIONES_ENTRADAS_4_14.md, fila E5). Frente a la rama, el denominador solo movía −0,45057 €.

**Cambia por E1:**

5. C47–C50 pasan a 77,533 / 8,294 / 5,547 / 3,707 M€. Efecto en el precio de Sí: 0,000 € (solo motor A). C52 pasa de 97,29 a 97,22 M€. Se actualizan los textos de Historia C17:L17 y C18:L18 en la revisión de datos ausentes.

**Cambia por las cifras nuevas (efecto mecánico, no juicio):**

6. Valores:

   | Cifra | Rama | Ahora |
   |---|---|---|
   | MALO | 30,15 € | 29,78 € |
   | NORMAL | 44,32 € | 43,77 € |
   | BUENO | 58,69 € | 57,95 € |
   | Ponderado | 44,36 € | 43,81 € |
   | Precio de Sí | 40,30 € | 39,80 € |
   | Valor sin crecimiento | 34,71 € | 34,28 € |
   | Valor del crecimiento del MALO | −4,55 € | −4,50 € |
   | Lo que se paga por crecer | 19,99 € | 20,42 € |
   | Lo que vale el crecimiento del NORMAL | 9,62 € | 9,48 € |
   | Veces | 2,1 | 2,2 |
   | DCF inverso | 9,8 % | 10,1 % |
   | Tasa del motor | 8,26 % | 8,27 % |

   Tornado: 10,04 → 9,90; 6,43 → 6,35; 5,70 → 5,63; 3,60 → 3,55; 2,54 → 2,52; 1,12 → 1,10 €. El peso del terminal, el salto del año 11, f y el puente (273,8 M€) no cambian.
7. Distancias:
   - el precio de Sí, del 26,3 % al 27,2 % por debajo del precio (÷ precio);
   - el precio, del 35,7 % al 37,4 % por encima del precio de Sí (÷ precio de Sí) y del 23,3 % al 24,9 % por encima del ponderado (÷ ponderado);
   - el NORMAL, del 19,0 % al 20,0 % por debajo del precio, y el ponderado, del 18,9 % al 19,9 % (÷ precio).
8. Probabilidades: un paso de la lista pasa de −1,63 / +1,88 € a −1,61 / +1,85 €. Los vectores dan 38,19 € (antes 38,67), 37,67 € (antes 38,15) y 41,65 € (antes 42,18). La comparación por un paso pasa de 1,6279 a 1,6068 €.
9. Variantes y contraste: copio exactamente las filas nuevas de `contraste_objetivo_v64.md` en cada `juicio_objetivo`.
   - Rango: de 38,61–43,52 € a 38,13–42,98 €.
   - Estructuras: S 39,18, SR2 40,37, H 41,47 y SRF 41,71 €.
   - θ = 0 da 41,47 € y θ = 1 da 38,13 €; «Caja», 40,45 €.
   - Δ: N1.tipo +1,51 (antes +1,53); N3.regla, H y θ ±1,67 (antes ±1,69); SRF +1,91; S −0,62; SR2 +0,57; «Caja» +0,65; terminal +0,37 €.
   - El recorrido de las estructuras pasa de 2,5633 a 2,5318 €, y la comparación de N3.regla, de 1,6932 a 1,6717 €.
   - La zona sigue siendo caro en las dieciocho.
10. Los puntos 1 a 9 son los del turno 1. Las secciones 10 a 16 son las del turno 2 (comprobación conjunta, C104, tesis, predicciones, B222:B223, cambio de cubo, comparación con la etapa 1).

## 10. Turno 2 · comprobación conjunta y conclusión

El turno 2 cierra la decisión del turno 1 y no reabre sus juicios. `configuracion_v64` queda como la dejó el turno 1, con el `juicio_objetivo` de cada parámetro intacto; también la lista D10, los datos ausentes y las celdas revisadas. La copia exacta está en `fase_c.turno1.json`.

**Comprobación conjunta:** no se ejecutó. No existe `comprobacion_conjunta.json` y la conclusión provisional no es favorable. `sobrevive = null`, `resultado = no_procede`.

**Estado: `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 39,80 € (condicionado, provisional).** Es lo que corresponde al tratamiento `objetivo_condicionado` del protocolo de `configuracion_economica.json`.
- Lo condicionan PM1.estructura, PM1.familia y PM1.parametro; ninguno es material para la acción.
- Las dieciocho variantes calculadas quedan en caro, con un precio de Sí de 38,13 a 42,98 €. Ese rango es una tabla de sensibilidad de las variantes calculadas: no es un intervalo de confianza ni una robustez frente a hipótesis no exploradas, y no cubre la familia Λ.
- Sin datos ausentes materiales, sin descalificadores y con la lista D10 vacía.

«We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). No escribo ningún tamaño de posición (D16): es de José Luis.

**Datos aplicados y fechas.** D3 y E1 son decisiones de la persona responsable, aplicadas como datos. C55 son las acciones en circulación a 31-dic-2025 y el precio es del 3-nov-2026: son fechas distintas, así que no es una actualización a 2026. La última cifra oficial anterior al precio (30-jun-2026: 45,603643 M en circulación) se cita y no se adopta. La dilución potencial del plan 2025–2027 se declara aparte y no se adopta: 39,53 € (incentivo objetivo) o 39,39 € (máximo) (AR_2025.txt, PDF pp. 129–130).

**Para quien decida con dinero real:** el objetivo es experimental y condicional. Lo limitan, además, decisiones pendientes que no adopto:
- D7: un paso de la lista de probabilidades mueve el precio de Sí −1,61 / +1,85 €;
- D4: +0,65 € con «Caja»;
- D2: si P-M1 no se acepta como delimitada, el objetivo se bloquearía;
- D8: la recomendación pendiente es no usar esta entrega para dinero real mientras D1 y D2 sigan abiertas.

**C104:** Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 39.80 · zona caro · precio de Sí ≤ 39.80 · precio esc. MALO 29.78 · ponderado 43.81 · fundamento no procede (conclusión no favorable) · objetivo condicionado (provisional): lo condicionan la estructura del mantenimiento, θ y la familia de P-M1 de la configuración experimental (la familia, sin calcular); rango del precio de Sí en las variantes calculadas 38.13 a 42.98, dieciocho variantes, todas en caro; acciones en circulación a 31-dic-2025 (D3) y precio del 3-nov-2026: fechas distintas

**C93 = Sí.** El g del NORMAL (2 %) con un ROIC terminal del 11 % reinvierte el 18 % del NOPAT (CV p. 13; I2). El salto del año 11 del NORMAL es de 4,7 puntos y el terminal pesa el 58 %.

**C103 = No.** ROIC del 12,1 % al 16,7 % con un margen que se estrecha: no es un negocio que se tiene sin mirar el precio.

## 11. Tesis (B101)

Viscofan es el mayor fabricante de envolturas para embutidos y el único con todas las tecnologías (extracto: AR_2025 p. 180), con un ROIC de entre el 12,1 % y el 16,7 % en diez años (Historia fila 33) y una cuota que subió del 30 % al 41 % entre los productores de envoltura a medida en 2015-2022 (AR_2019 p. 121; CF_2022 p. 182). Es un buen negocio, no uno extraordinario: las ventas crecieron un 71 % en la década, pero el margen EBIT bajó del 21,1 % al 16,4 % (fila 29), el capital nuevo rindió en torno a un 9 % (filas 7 y 32) y el FCF al accionista de 2025 (93,8 M€) quedó por debajo del de 2019 (108,5 M€; fila 35), mientras la deuda sube para repartir más de lo que genera (AR_2025 p. 144). Con mis tres escenarios (29,78 / 43,77 / 57,95 €) el precio de 54,70 € del 3-nov-2026 está por encima del NORMAL y del ponderado (43,81 €) y descuenta un crecimiento de ventas del 10,1 % anual, más que mi BUENO (C86). Vigilar: espero a un precio de Sí de 39,80 €, con las acciones en circulación a 31-dic-2025 (D3), objetivo condicionado por las hipótesis de mantenimiento de la configuración experimental (de 38,13 a 42,98 € en las dieciocho variantes calculadas, todas en caro). La frontera con No es una sola: si la compresión del margen es estructural.

## 12. Tesis inversa (B102)

Defiendo el No. Viscofan transforma pieles bovinas, celulosa y gas en un insumo industrial y no ha sabido trasladar sus costes: el margen EBIT cayó del 21,1 % de 2016 al 15,1 % de 2023 (Historia fila 29), las subidas de precio solo compensaron en parte en 2022 y 2023 (extracto: CF_2022 p. 93; IA_2023 p. 246) y en 2025 la mezcla de precios bajó con volumen récord (AR_2025 p. 139): la cuota se puede estar pagando con precio, frente a competidores que ni siquiera sé nombrar (AR_2025 p. 399). En diez años el capital invertido creció 436 M€ y el beneficio operativo después de impuestos 39 M€, un 9 % sobre el capital nuevo, tan cerca de la r que crecer apenas crea valor, y el FCF al accionista de 2025 (93,8 M€) es menor que el de 2019 (108,5 M€; Historia filas 32 y 35). Mientras, reparte más de lo que genera: 145,1 M€ en 2025 frente a 93,8 M€ de FCF, con un dividendo «extraordinario» repetido tres años y recompras de 94,0 M€ en un año con una cotización media de 59,47 € (AR_2025 pp. 144, 147), por encima de lo que creo que vale; la deuda financiera pasó de 116,8 a 304,1 M€ en 2021-2025 (fila 22), con 227,4 M€ de deuda bancaria a un año (AR_2025 p. 98). La inversión en EE. UU. dio resultados negativos durante años (AR_2025 p. 66), Danville arrastra avisos de las agencias ambientales desde 2020 (p. 94) y la última compra, Pet Mania, se frenó por un arancel (p. 140). Si el margen sigue la pendiente de la década, mi MALO (29,78 €) es el caso central y 54,70 € pagan un 84 % más que él.

Lo que no puedo defender del No: que la deuda mate a la empresa (0,87x EBITDA, 155,3 M€ de líneas libres; AR_2025 pp. 98, 122) o que la cuota esté cayendo.

## 13. Predicciones (dado el NORMAL)

1. Las ventas consolidadas de 2027 que publique Viscofan en su informe anual de 2027 estarán entre 1.300 y 1.420 M€ (1.252,0 M€ en 2025). Fecha 2028-03-31; probabilidad 0,65.
2. El margen de explotación de 2027 (resultado de explotación ÷ ventas consolidadas del informe anual de 2027) estará entre el 15,5 % y el 17,5 % (16,4 % en 2025). Fecha 2028-03-31; probabilidad 0,65.
3. La deuda bancaria neta a 31-dic-2027, con la definición de la empresa, no superará 1,5 veces el EBITDA de 2027 (206,1 M€ sobre 290,0 M€ de EBITDA, 0,71 veces, a 31-dic-2025). Fecha 2028-03-31; probabilidad 0,7.

Las tres fechas caen entre 12 y 24 meses después de Análisis!D4 (2026-11-14). Las probabilidades son de que cada predicción se cumpla dado el NORMAL, no la del escenario.

## 14. Incertidumbre pendiente (B222 · B223)

Lista D10 vacía: la hipótesis fundamentada de la que más depende la conclusión es Palancas!C15, que el margen EBIT del NORMAL deje de comprimirse en el 16,5 % (media de 2019-2025) en vez de seguir la pendiente de la década (del 21,1 % al 16,4 %, Historia fila 29). Si la compresión es estructural, el NORMAL es el MALO y el cubo es No. El objetivo lo condicionan además tres hipótesis de la configuración experimental sin fundamento suficiente: la estructura del mantenimiento, θ (qué parte del exceso de inversión de 2021-2025 fue reposición) y la familia de P-M1, que ninguna variante calcula.

Lo que la resolvería:
- La descomposición de la variación de ventas y de margen de 2023-2025 en volumen, precio y mezcla y coste de pieles, por tecnología y región. El informe anual no la publica (solo «mezcla de precios ligeramente inferior», AR_2025 p. 139): pregunta a Relación con Inversores.
- Para el objetivo, qué parte de la inversión de 2021-2024 clasificada como «capacidad y maquinaria» sustituyó capacidad existente, y el desglose por tipo de 2024 en un documento conservado. Los de 2021, 2022, 2023 y 2025 ya están en el paquete (IA_2021_es.txt, PDF p. 213; CF_2022_compilacion.txt, PDF p. 202; IA_2023_es.txt, PDF p. 250; AR_2025.txt, PDF p. 143).
- La vida útil y la antigüedad media de las líneas de extrusión, conversión y cogeneración (pregunta a Relación con Inversores).

## 15. Qué me haría cambiar de cubo

- **A Sí:** un precio igual o inferior al precio de Sí (≤ 39,80 €, condicionado por la configuración) con el negocio intacto: margen EBIT de 2026 y 2027 en el 16 % o más con volumen al alza, cuota ganada con producto según el desglose de ventas, deuda bancaria neta por debajo de 1,5 veces el EBITDA, y saber quién es el competidor que más daño puede hacer (AR_2025 p. 399 no lo nombra). Antes de comprar, la comprobación conjunta tendría que superar las hipótesis de la configuración sin fundamento suficiente (estructura, θ, familia) y habría que revisar la lista D10 para esa compra.
- **A No:** que la compresión del margen sea estructural: un margen EBIT por debajo del 15 % dos años seguidos con volumen récord, o un desglose que muestre la cuota pagada con precio. También la deuda neta por encima de 1,5 veces el EBITDA por pagar al accionista (C98 pasaría a Dudosa) o una adquisición grande fuera del negocio.
- **A Demasiado difícil:** que el valor pase a depender de predecir el coste de las pieles bovinas o del dólar porque la empresa deja de repercutirlos (el descalificador de materias primas; AR_2025 p. 436), que un sustituto cambie el volumen del mercado de envolturas (riesgo citado sin cuantificar, AR_2025 p. 399) o que Danville se convierta en una contingencia que no pueda estimar (AR_2025 p. 94).

**Condiciones de revisión del precio de Sí.**
- **Al alza:** el margen EBIT publicado de 2026 y 2027 en el 16,5 % o más con volumen al alza, un desglose de ventas que muestre la cuota ganada con producto, o documentación de que la inversión de 2021–2024 clasificada como «capacidad y maquinaria» fue crecimiento (θ bajo: 41,47 € en la variante θ = 0).
- **A la baja:** margen EBIT por debajo del 15 % con volumen récord, deuda bancaria neta por encima de 1,5 veces el EBITDA por el reparto, o documentación de que el exceso de 2021–2022 fue sobre todo reposición (θ alto: 38,13 € en la variante θ = 1). La dilución del plan 2025–2027, si se entregara con acciones nuevas, lo llevaría a 39,53 / 39,39 €.

## 16. Comparación con la etapa 1

Cubo v1 Vigilar con precio de Sí de 25,1 €; cubo v2 Vigilar con precio de Sí de 39,80 €. El cubo coincide: buen negocio de nicho, en el círculo, a un precio sin margen. El precio de Sí sube por cuatro cosas, y ninguna es que el negocio haya mejorado:
1. **La regla.** La v1 tomaba mín(MALO, 0,75 × ponderado); la v2 usa la escalera de k = 3 con tope en el NORMAL. Con la regla antigua sobre los valores de la v2 saldrían 29,78 € (C156).
2. **El motor.** La v1 proyectaba con el motor A un FCF base de 97 M€ y un MALO de caja plana (25,1 €; `etapa1/Viscofan_respuesta.md`). La v2 valora la operación con el motor B y resta la deuda de la base (puente de 273,8 M€); su MALO (29,78 €) es una compresión del margen al 14 %.
3. **La base y el precio.** La v1 mezclaba datos de 2026 (1S26, deuda de junio) y un precio de 53,6 €. La v2 usa el cierre de 2025, con los datos corregidos de la rama, y 54,70 € del 3-nov-2026.
4. **El divisor.** La v1 dividía entre 45,6 M de acciones diluidas. La v2 usa 45,993399 M en circulación a 31-dic-2025 (D3), que baja el precio de Sí 0,50 € frente a la rama (40,30 → 39,80 €).

La v1 no tenía la Historia de diez años: ahora C27 = Comprimiendo y C25 = No se sostienen con filas, y C97 pasa de Neutral (sin registro) a Comprando con la evidencia de fase 1 (Control maestro fila 76). La v1 escribió un porcentaje de posición en C104; la v2 no lo hace.

Frente al turno 2 de la rama (`fase_c.rama.json`), la conclusión es la misma: Vigilar, `esperar`, objetivo condicionado por las mismas tres hipótesis. Cambian solo las cifras por D3 y E1:
- precio de Sí 40,30 → 39,80 €;
- MALO 30,15 → 29,78 €;
- ponderado 44,36 → 43,81 €;
- rango 38,61–43,52 → 38,13–42,98 €;
- θ = 0 / θ = 1: 42,00 / 38,61 → 41,47 / 38,13 €;
- DCF inverso 9,8 → 10,1 %.

D3 sale de los límites pendientes porque ya es una decisión aplicada. La fecha de análisis es la de este expediente (2026-11-14).

El error que tengo más cerca sigue siendo pagar por calidad: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM). El contrario existe: si 2022-2023 fue un ciclo y 2024-2025 la recuperación, esperar a 40 € sería «early fretting» (TCI p.79; HIM). Confianza global: media.

## Cambios frente a la versión auditada (SA-5560fe3438e5febb)

Base: `fase_c.json` y `fase_c.md` auditados (material 53644d4b827d31a0, veredicto REPETIR). Cambio solo lo que pide la auditoría; los juicios, el cubo, la conclusión, la lista D10, los datos ausentes y los demás `juicio_objetivo` quedan como estaban.

1. Punto 10: nueva incoherencia (JSON y §1.12) y frase en `configuracion_v64.observaciones`: el divisor efectivo es C55 = 45,993399 M (D3); la frase «N sigue en 45,479209» de la naturaleza de la configuración la corrigió la orquestación; nada de esta fase presenta 45,479209 M como acciones activas.
2. Aviso del punto 5: nueva incoherencia (JSON y §1.13): C42 = 9,47 usa la capitalización de 2.487,7 M€; con D3 sería ≈9,57; dato de entrada que no reescribo; no mueve el precio de Sí.
3. Aviso del punto 11: `PM1.convencion_terminal` → `juicio_objetivo.comparado_con.valor_eur` de 1,6279 a 1,6068 (39,7982 − 38,1914 €, recalculado con `p_estrella`).
4. Aviso del punto 8: coste medio de las 1.599.709 acciones propias de ≈58,8 € a ≈58,6 € (93.752 miles de €, nota 12.4, AR_2025.txt, PDF p. 83; el número de acciones también en PDF p. 143), en §1.7 y en la incoherencia de las recompras; deja de ser una inferencia sobre dos cifras distintas.
5. Aviso del punto 9: la limitación de fechas de D3 dice también la última cifra oficial antes del precio (30-jun-2026: 46.000.000 emitidas y 396.357 propias = 45,603643 M), sin adoptarla y con su efecto estimado (≈+0,34 € por el solo denominador, no calculado en la hoja), en la incoherencia de las acciones, en el límite de acciones de los doce `juicio_objetivo` y en §1.8, §9 y §10.
6. Turno 1 de la corrección entregado con `turno: 1` (copia exacta en `fase_c.turno1.json`; el turno 1 anterior queda en `fase_c.turno1.anterior_SA-5560.json`).
7. Turno 2: `turno: 2`; no existe `comprobacion_conjunta.json`, así que `sobrevive = null` y `resultado = no_procede`; estado, cubo, acción, precio objetivo, las 16 celdas, sus Observaciones, `herencia`, `comparacion_etapa_1`, `cambiaria_de_cubo` y `configuracion_v64.objetivo` quedan como en la versión auditada: las correcciones no cambian ninguna cifra de la escalera ni la conclusión.
8. Turno 2: `insumos_decision_cartera.fundamento` añade a la limitación de fechas de D3 la última cifra oficial antes del precio (30-jun-2026: 45,603643 M en circulación), citada y no adoptada, como en el turno 1 (aviso del punto 9).
