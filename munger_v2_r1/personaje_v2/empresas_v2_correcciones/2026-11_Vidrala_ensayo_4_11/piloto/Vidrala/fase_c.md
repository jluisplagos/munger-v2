# Vidrala, S.A. (VID) · fase C · turno 1 · base económica 31-dic-2025

Hechos: `resultados.json` (libro recalculado, recálculo forzado comprobado), `precio.json`, `gramatica.md`, `configuracion_v64_variantes.md`, `datos_v63.md` y `extracto_v63.md` (ES_2025 y CF_2025, páginas del PDF). El libro lleva la configuración V6.4 de demostración (N1 22,05 %, N2 18,55 %, R1, P-M1 SR1 · Λ · λ 1,15 · P0). No está adoptada. Todas las cifras del libro y de la escalera la llevan dentro, y digo dónde pesa. Para medir lo que la tabla de variantes no trae uso una réplica mía del motor B, de solo lectura y fuera del paquete. Reproduce al céntimo los tres valores del libro y once de las trece variantes calculadas (todas salvo las dos de convención de la amortización). Sus cifras son estimaciones mías, no variantes calculadas, y de ellas no afirmo ninguna zona.

## 1. Una sola historia

**Lo que calcula la hoja.**
- Valor por acción: MALO 45,56 · NORMAL 61,93 · BUENO 81,74. Ponderado 62,62 (C83). Precio 90,10 (C37): zona `caro`.
- El precio está por encima del valor de mi BUENO.
- Valor sin crecimiento: 58,19 €. El crecimiento de mi NORMAL vale 3,74 €. El precio paga 31,91 € por crecer: 8,5 veces lo que vale.
- Peso del terminal: 41 / 50 / 56 % (PASA). El valor no cuelga del futuro lejano: es, sobre todo, el poder de ganancia actual.
- Salto del año 11: 0,5 / 5,7 / 8,0 puntos (Diagnóstico V6 C176:D178).
- DCF inverso (C86): con el resto de palancas del NORMAL, 90,10 € descuentan un 14,2 % anual de ventas en los años 1-5. Mi BUENO es del 4,5 %, C46 es del 8,2 % y el Q3 del sector, del 10,4 %. Al precio de Sí, el crecimiento descontado es de −0,03 %: pagar el precio de Sí es no pagar nada por crecer (57,74 frente a 58,19 sin crecimiento).
- Tornado (información, no criterio): ROIC a largo plazo ±5 puntos, 13,57 € (21,9 % del NORMAL); tasa ±1 punto, 11,22; margen ±2 puntos, 7,82; crecimiento, 3,70; S2C, 3,38; g, 0,20. El g casi no pesa porque el ROIC terminal del NORMAL está en la tasa: crecer a la tasa no crea valor.
- Semáforos: margen REVISAR en los tres (G5, justificado en la fase B: Vidrala está por encima del Q3 del sector todos los años desde 2016); f REVISAR (aviso A6, que es la razón del motor B). El resto, PASA. Cuota implícita «—» porque C24 está vacía.
- Múltiplos a mi NORMAL: PER 10,4, EV/EBITDA 5,5 y P/FCF 13,5. A precio de hoy: 15,1, 7,8 y 19,7.
- A6 dice «DESCARTADA POR FILTRO PABRAI · el valor no es claro sin modelos (C13)». Mi cubo es Vigilar porque C13 = No dice que el valor no es obvio a este precio, no que el negocio no pase los filtros (regla 17.4).

**¿Es la historia de la fase A?** Sí. La fase A dijo: buen negocio con un foso estrecho, cíclico por la energía, gestión que asigna bien y un precio que pide un crecimiento que un mercado maduro no promete. La hoja lo pone en cifras: el precio necesita un 14,2 % y mi NORMAL tiene un 2,5 %. El NORMAL es, casi entero, el negocio de hoy (58,19 + 3,74). Esto cuadra con C17 = No, C19 = No y C14 = Cíclica. La conclusión aguanta la configuración: en las trece variantes calculadas el precio supera al NORMAL (máximo 70,67) y al ponderado (máximo 71,77), y en diez de las trece supera también al BUENO (solo heredado, solo_N2 y solo_R1 lo dejan en 90,73-91,77). «once you put the price into the formula, it wasn't so clear anymore» (PCA p.201; HIM).

**Incoherencias.** Ninguna pide mover palancas. Las anoto, con su cálculo:
- (a) **Magnitud del salto.** La fase B escribió «unos 4 puntos» en el NORMAL y «≈ 5-6» en el BUENO, con rentabilidades marginales de ≈ 13 % y ≈ 17,6 %. La hoja da 14,7 % y 20,0 %, con saltos de 5,7 y 8,0 puntos. La diferencia es de la configuración, no de las palancas: SR1 multiplica el S2C por f = 1,1649 (efectivo 1,048 y 1,281) y N1 pone t en 22,05 %. Las Observaciones de Palancas C16, D16, C18 y D18 llevan la cuenta en base V6.3. Lo resuelvo justificando G8 (punto 2). La tesis del turno 2 tiene que decirlo con las cifras de la hoja.
- (b) **La carga del MALO no está en los números.** La historia del MALO dice que la descarbonización pide capex sin ventas (B65 de la fase A; Palancas B16 de la fase B). Con R1 las ventas del MALO no vuelven nunca al nivel de 2025 (1.407 mm en el año 10 frente a 1.465). No hay inversión fija para crecer y el S2C del MALO no mueve el valor: con la réplica, 0,6, 0,7 y 0,8 dan los mismos 45,56 €. El único mantenimiento del MALO es el mismo λ que el del NORMAL. Sin el plan de capex no hay un hecho para la magnitud. Una cota: con el margen del MALO en el suelo de la fase B (13,5 %), el MALO vale 40,95 y el precio de Sí 55,77 (−3,4 %), en zona `caro`. Ni el cubo ni la zona cambian.
- (c) **Perímetro del margen del NORMAL (Palancas C15).** El 18 % sale de Historia G29:L29 (18,2 %), cuyo 2020-2022 lleva Italia. La media del ciclo 2020-2025 de continuadas es del 18,55 % (N2, `configuracion_economica.json`), que redondea a 0,185. Corregido: NORMAL 63,88, precio de Sí 58,58 (+1,45 %), ponderado 63,79, zona `caro`, cubo Vigilar. No cambia ni el cubo ni la zona y mueve el precio de Sí menos de un 5 %: la dejo (v2.1) y la registro en `celdas_corregidas`.
- (d) **C98 = Buena frente a su propio disparador.** La fase A escribió «Bajaría a Aceptable si recompran por encima del valor». Las 23.400 acciones propias de la base costaron 2,097 mm, unos 89,6 € cada una, y el programa de diciembre tiene un tope de 33 mm para 350.000 acciones, unos 94 € de media si se agotan los dos [CF_2025, PDF p. 61]. Ese precio está por encima de mi NORMAL y de mi BUENO, y del NORMAL de todas las variantes calculadas. El importe es pequeño (0,07 % de la capitalización), pero la señal no lo es. No reescribo la fase A. Lo anoto y va a la tesis inversa. Aceptable no es un descalificador y no impide esperar.
- (e) **Celdas heredadas de la fase C.** B101, B102, C93, C103 y C104 todavía llevan la etapa 1 con hechos posteriores a la base: Chile «desde el 30-mar-2026», 0,69x a 30-jun-2026, 88,7 €, y un porcentaje de posición en C104 que va contra D16. El turno 2 las reescribe; no se mantienen.
- (f) **La referencia del S2C mezcla perímetros.** C53 (0,916) mide 476,8 mm de ventas añadidas en 2020-2025, que incluyen Brasil y excluyen Italia, frente a solo 12,4 mm de compras netas (254,1 − 241,7, Historia fila 13). Además, su circulante de 2021-2025 (278,8 mm, fila 14) supera todo el circulante comercial de la base (215,4 mm, el 14,70 % de las ventas). Efecto acotado: con S2C del NORMAL de 0,8 a 1,2, el precio de Sí se mueve entre −0,62 % y +1,26 %. No es material.

## 2. Desviaciones pendientes

- **G8 NORMAL, 5,7 puntos (convención).** El ROIC terminal está en la tasa del motor (0,09 frente a 8,69 %). En el año 11 se pierde el exceso del capital nuevo, no el del instalado. En los años 1-10 cada euro reinvertido rinde un 14,7 %. Es el rendimiento de crecer con precio, Toro y algo de volumen sobre hornos ya instalados, cerca del ROIC medio de cinco años (13,8 %, C55) y del ~15 % que da el histórico de crecimiento con SR1 (C53 × f × m0 × (1 − t)). Desde el año 11 el capital nuevo rinde la tasa, porque el foso es estrecho (C18 = Sí, confianza baja). No sé quién me mata: los informes no nombran competidores y hablaban de una «cuota de mercado estable» sin cifra [CF_2025, PDF p. 31; CF_2019, PDF p. 69]. Y la descarbonización obliga a rehacer los hornos desde 2026 [CF_2025, PDF p. 65], con tecnología que los competidores también compran. El margen del 18 % sigue sobre el capital instalado. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **G8 BUENO, 8,0 puntos (fundamentada).** En los años 1-10 se rinde un 20,0 % (S2C efectivo 1,281, margen del 20 %), y desde el año 11, un 12 %. Mi hipótesis: el crecimiento del BUENO llena primero capacidad que en 2025 no iba llena («aunque no fuera así» [CF_2025, PDF p. 48]) y la de Toro (145.000 t [CF_2025, PDF p. 78]), con Brasil al 42,4 % de margen EBITDA [ES_2025, PDF p. 107]. Así, cada euro nuevo rinde como el capital añadido entre 2016 y 2025: el NOPAT pasó de 74,7 a 221,0 mm sobre 770 mm de capital añadido, un 19 % (Historia filas 7, 10 y 32). Agotada esa holgura, los hornos nuevos rinden como el peor año de la meseta 2018-2025 (11,9 % en 2018 y 12,2 % en 2023, fila 33). La ventaja dura, pero se estrecha a 3 puntos sobre r (MR; E2). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).
- **G16:** no salta (50 % en el NORMAL). **G17:** no se calcula, porque C24 está vacía y no hay cifra primaria de mercado. El BUENO, al 4,5 % con Toro, no necesita más mercado del que crece.

## 3. Palancas

No pido revisión. Ninguna palanca está mal derivada por aritmética ni por dato. La única derivada sobre un perímetro mixto es C15 (c): corregirla mueve el precio de Sí un +1,45 % y no cambia ni cubo ni zona. Las alternativas de la fase B, palanca a palanca, mueven el precio de Sí menos de un 5 %. Las de mayor efecto: probabilidades 0,3/0,5/0,2 → −4,4 % y 0,15/0,6/0,25 → +4,0 %; MALO al 13,5 % → −3,4 %; NORMAL al 17 % o al 19 % → ∓2,9 %. Con todas a la vez en el lado malo (S2C del MALO 0,6, S2C del BUENO 1,0, ROIC del BUENO 0,11, margen del NORMAL 0,17 y 0,25/0,6/0,15), el precio de Sí queda en 53,93 (−6,6 %), en zona `caro`. Lo que de verdad mueve el objetivo no son mis palancas, es la configuración (punto 9).

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Su precio de Sí (~48 €) se parece a mi MALO (45,56), pero el mío sale de 15 % de margen, −1 % de crecimiento y la configuración, no de su cifra. Lo heredado de la fase C (B101, B102, C104) lleva hechos de 2026 y un porcentaje de posición en C104. Cambio: en el turno 2 reescribo B101, B102 y C104 con la base y sin porcentaje, y decido de nuevo C93 y C103 con el salto y el peso del terminal.
2. **Anclaje en el precio o en la fuente externa.** Mis valores (45,6-81,7) están lejos de 90,10 y de los 171,8 de Simply Wall St (C38). Si algo, me anclé a la baja: el 18 % del NORMAL frente al 18,55 % de continuadas. SR1 es la estructura de la demostración: la comparé con H, S, SR2 y SRF usando la reinversión histórica, no porque venga dada. Cambio: C15 en `celdas_corregidas` con su cálculo (+1,45 %).
3. **Consistencia y compromiso.** Vigilar no depende de ajustes: la zona es `caro` en las trece variantes. Pero C98 = Buena se quedó, y el disparador que la propia fase A escribió se cumple con las cifras de la hoja: recompras a ~89,6 € con el NORMAL en 61,93 (d). Cambio: C98 a incoherencias y a `celdas_corregidas` (sin reescribirla). La tesis inversa del turno 2 lo recoge.
4. **Historia bonita / viento de cola.** El margen de 2023-2025 que usa mi BUENO lleva dos regalos. Uno, la energía a la baja. Otro, 19,8 mm más de «otros ingresos» que en 2024, sin explicar (47,966 frente a 28,187 [CF_2025, PDF p. 73]): unos 1,4 puntos de margen. Brasil se compró ya con su margen. Cambio: ninguno en las palancas. Con el BUENO al 19 %, el precio de Sí baja a 57,07 (−1,2 %). Lo digo en la tesis.
5. **Optimismo del BUENO frente a la tasa base.** Un 4,5 % de crecimiento con Toro está por debajo del Q3 y no pide más mercado. Pero su rentabilidad marginal del 20,0 % supera el ~15 % del histórico de crecimiento, y descansa en una capacidad sobrante que no está medida. El 12 % a perpetuidad ya es el tope de 3 puntos sobre r. Cambio: Palancas D16 pasa a la lista de hipótesis sin base. Su efecto es pequeño (1,0 → −0,24 %).
6. **Doble castigo del mismo riesgo.** La r no lleva prima de quiebra, C22 está vacía y p(MALO) no sube por el margen alto, que ya está en el NORMAL. El punto más cercano está en la configuración: SR1 cobra la reposición aparte y deja el ROIC terminal sin cambiar. Si el 0,12 del BUENO ya fuera neto de reposición, la contaría dos veces. SR2 lo mide: +1,13 € (+1,95 %). Cambio: ninguno. Lo informo en el punto 9.
7. **Disponibilidad (lo vívido del extracto).** La tormenta Kristin (10-15 mm) es posterior a la base y no está en ninguna cifra. El apagón ibérico del 28-abr-2025 la empresa lo da por no material [CF_2025, PDF p. 72]. Los 551 kt de CO2 no mueven ninguna palanca. Margen y ROIC salen de las filas 29 y 33 de la Historia. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: ninguno.
8. **Autoridad (guía de la dirección como hecho).** Tres palancas coinciden con supuestos de la prueba de deterioro de la dirección: el volumen del +1 % del NORMAL, el g del 2 % (la inflación que ella supone) y las bajadas de precio de 2026 [CF_2025, PDF p. 48 y 49]. Mi NORMAL sin Toro (1,6 %) es justo su CAGR proyectado. No tengo una serie de volumen independiente. «an executive trying to justify a particular course of action will frequently be a lie» (TCI p.60; HIM). Aquí la guía va en el sentido prudente, pero sigue siendo guía. Cambio: ninguno en las cifras (NORMAL al 1,5 % → −1,26 %). En la tesis la declaro como guía.
9. **¿El MALO es de verdad malo?** Vale un 26 % menos que el NORMAL y un 22 % menos que el valor sin crecimiento: no es cosmético. Pero le falta la carga de la descarbonización (b) y no tiene una pérdida estructural de volumen frente a otros envases. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno en las palancas, porque no hay un hecho para la magnitud. La cota (−3,4 %) va a la tesis inversa.
10. **Lo no numerable que pesa y no está en las palancas.** Recompras por encima de mi valor, insiders sin hechos (C97 técnico), un déficit de pensiones británico sin cifra, el camino del coste del CO2 y si el vidrio en Iberia y Reino Unido es un sector racional. Cambio: van a la tesis inversa, a qué me haría cambiar de cubo y a B222 en el turno 2.

Antídoto general: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Lo que más contradice mi tesis es (d): la dirección compra a 90 €, y lo que sabe del negocio vale más que mi lectura de sus cuentas. A favor de mi lectura está que, si el precio está mal, alguien se equivoca. «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). Aquí ese alguien puede ser quien lee 2024-2025 como permanentes, o yo con λ y el ROIC en la tasa. El precio de hoy solo lo alcanza el BUENO de la V6.3 efectiva (90,73): el mercado paga mi mejor historia sin el coste de reposición.

## 5. Cubo y conclusión provisionales

En orden de mando:
1. Bloqueo: ninguno (0 errores; G8 queda justificado).
2. Límite del modelo: no.
3. Descalificadores: ninguno (fase A). La hoja no añade ninguno: reinversión del 23 % en el año 1 y deuda de 0,36x.
4. Dato ausente material: ninguno (punto 6).
5. Fundamento material: cuatro hipótesis sin base. Condicionan el objetivo, no la acción.
6. Zona: `caro`.

**Cubo Vigilar · conclusión esperar.** El precio de Sí es 57,74. Es provisional: lo condicionan la configuración de demostración (P-M1) y las hipótesis del punto 7. Con la V6.3 efectiva sería 66,02. En las variantes calculadas va de 57,03 a 67,00. Distancias:
- 90,10 está un 56,04 % por encima del precio de Sí (diferencia ÷ precio de Sí). El precio de Sí está un 35,91 % por debajo del precio (diferencia ÷ precio).
- Frente a 66,02 (heredado): un 36,48 % por encima (÷ 66,02); 66,02 está un 26,73 % por debajo (÷ precio).
- El precio del escenario MALO (45,56) está un 49,43 % por debajo del precio (÷ precio).

«We just said that we wouldn't buy it or recommend that our friends buy it at the prices then prevailing» (PCA p.267; HIM). El error más cercano sigue siendo pagar cualquier cosa: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 6. Datos ausentes (S-19)

Reviso los veintisiete. **Ninguno es material** para esperar con precio objetivo:
- Las seis evidencias pendientes no tocan el motor B: los arrendamientos van dentro de C64 de todos modos; no hay minoritarios porque todas las dependientes son al 100 % [CF_2025, PDF p. 9 y 4]; C48 e intereses solo cuentan para el motor A o para f; los ceros de compras de 2021-2022 solo moverían el factor del S2C de SR1 si escondieran una compra, y el estado de flujos de esos años solo trae inmovilizado.
- Los de mercado, cuota y competidores tocan C18 y el ROIC. Serían materiales para un Sí, no para esperar a un precio por encima de mi NORMAL en todas las variantes (ROIC del NORMAL en 0,11 → +1,47 %).
- Los de precio, volumen y absorción tocan el margen y el crecimiento: ∓2,9 % y ∓1,3 % del precio de Sí.
- Capacidad y utilización tocan el S2C del BUENO (±0,4 %).
- El capex previsto (descarbonización) toca la carga del MALO y el mantenimiento (P-M1). La acción no depende de él (zona `caro` en las trece variantes). Deja provisional el objetivo y forma parte de lo que lo resolvería (punto 8).
- Rating, covenants y pensiones tocan C22 y los pasivos netos. Con 0,36x y 258 mm sin disponer no hay disparador. Un déficit de 50 mm restaría 1,42 € (−2,5 %).

`alguno_material = false`.

## 7. Fundamento material (D10)

Hipótesis sin fundamento suficiente:
- **Palancas B16 (S2C del MALO 0,7).** La magnitud es la de la banda y, con R1, no mueve el valor. Sin base.
- **Palancas D16 (S2C del BUENO 1,1).** La magnitud es la de la banda y no hay utilización publicada. Sin base para el techo.
- **B69:D69 (0,2 / 0,6 / 0,2).** Es una convención argumentada. Diez años con un solo choque de energía no dan la frecuencia de un régimen permanente. Sin base.
- **Configuración V6.4 · P-M1 (SR1 · Λ · λ 1,15).** Es un supuesto técnico de la demostración. Los hechos dan el sentido (la reposición supera la amortización) pero no la magnitud. Sin base.

El ROIC del NORMAL en la tasa no entra en la lista. Es la palanca que más pesa en el tornado, pero tiene hechos para su sentido (foso estrecho, ningún competidor conocido, hornos por rehacer). Su alternativa de 0,11 mueve el precio de Sí un +1,47 %.

La conclusión provisional no es favorable, así que `resultado = no_procede`. No pido la comprobación conjunta: es opcional, el rango del precio de Sí ya lo dan las variantes y mis alternativas, y ninguna de las cuatro hipótesis tiene sus dos extremos atados a hechos. Con esperar y hipótesis sin base, el turno 2 marca el precio objetivo como provisional en C104, con P-M1 como la hipótesis que lo condiciona.

## 8. Lo que más condiciona y qué lo resolvería

**Hipótesis que más condiciona: cuánto supera la reposición de los hornos a su amortización** (P-M1, λ = 1,15 de demostración):
- Sin requisito, el precio de Sí sube un +11,5 % (64,37).
- Entre estructuras va de 57,03 (S) a 63,11 (H).
- Con λ de 1,10 o 1,25 (réplica) sería 60,12 o 53,00.

**Qué lo resolvería:**
- El desglose del capex de 2021-2025 y del plan 2026-2030 entre renovación de hornos, capacidad nueva y descarbonización.
- El coste de reconstruir un horno frente a la amortización del que sustituye. Es una pregunta a Relación con Inversores: la nota de inmovilizado [CF_2025, PDF p. 43-45] no lo separa.
- La decisión D-N3b sobre P-M1, que es de la persona responsable, no mía.

## 9. Configuración V6.4 (demostración, no adoptada)

Efectos aislados (tabla de variantes, precio de Sí; en las trece la zona es `caro`):
- **N1, tipo** (solo_N1 frente a heredado): −1,79 € (−2,7 %). Es fundamentada: el tipo de la Historia lleva 2021-2022 con Italia.
- **N1, escudo**: no está aislado en la tabla. Con la réplica, −0,08 €.
- **N2, margen de partida** (solo_N2): +0,98 € (+1,5 %).
- **N3, regla R1** (solo_R1): −0,81 € (−1,2 %). Solo actúa en el MALO, y además deja inerte el S2C del MALO.
- **P0, cartera no repuesta**: +0,49 €.
- **P-M1 sin requisito** frente a la activa: −6,63 € (−10,3 %).
- **Estructuras**: H 63,11 · SRF 60,46 · SR2 58,87 · SR1 57,74 · S 57,03.
- **Convenciones de la amortización**: años −0,26 €; terminal +0,64 €.

Solo la estructura P-M1 y su magnitud (familia y λ) son materiales para el objetivo. Ningún parámetro lo es para la acción.

**Mantenimiento.** La reposición supera la amortización:
- El capex fue ≥ 1,10 veces la amortización todos los años desde 2017, y 1,45 veces en 2021-2025 (739,0 frente a 509,6 mm, Historia filas 8 y 12).
- Eso, con un volumen plano o a la baja (orgánico −5,4 % en 2025 [ES_2025, PDF p. 90]).
- La renovación de hornos es el destino principal [CF_2025, PDF p. 43 y 44].
- Hay 66,6 mm de maquinaria comprometida [CF_2025, PDF p. 45] y descarbonización desde 2026 [CF_2025, PDF p. 65].

La magnitud no la mido. λ = 1,15 es el 33 % del exceso histórico (75,0 de 229,4 mm). Si todo el exceso fuera reposición, λ sería ≈ 1,46.

Estructura:
- **H** no encaja: supone que la reposición viaja con el crecimiento, y en 2025 el capex fue 1,42 veces la amortización con ventas orgánicas a la baja.
- **S** cuenta dos veces: C53 ya lleva el exceso.
- **SR1** quita exactamente el exceso histórico por euro de ventas añadido (75,0 ÷ 476,8 = 0,157 €). **SRF** quita 0,288 €, más de lo que muestra la historia. **SR2** corrige un ROIC que en el NORMAL es convención y en el BUENO está medido en bruto.

La más coherente con los hechos es **SR1**, con confianza baja; SR2 queda a +1,95 %, no material. No la adopto: la estructura pesa menos que λ, y λ es técnico.

## 10. Conclusión (turno 2)

No hay `comprobacion_conjunta.json`: `sobrevive = null`. La conclusión no es favorable, así que `resultado = no_procede`.

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción esperar · precio objetivo 57,74.**
- El precio objetivo es el precio de Sí de `precio.json`.
- Es provisional: lo condiciona la reposición P-M1 de la configuración V6.4 de demostración, no adoptada. Con la V6.3 efectiva sería 66,02; en las variantes calculadas, de 57,03 a 67,00.
- 90,10 está un 56,04 % por encima del precio de Sí (diferencia ÷ precio de Sí). El precio de Sí está un 35,91 % por debajo del precio (diferencia ÷ precio).
- Ningún dato ausente es material. Ningún descalificador aplica.
- r = 9 % frente a una r mínima del 8,17 %. La palanca más influyente es el ROIC a largo plazo (información, no criterio).

Celdas de cierre:
- **C104:** «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 57.74 · zona caro · precio de Sí ≤ 57.74 · precio esc. MALO 45.56 · ponderado 62.62 · fundamento no procede (conclusión no favorable) · precio objetivo provisional: lo condiciona la reposición P-M1 de la configuración V6.4 de demostración, no adoptada (con la V6.3 efectiva sería 66.02)». Sin porcentajes: el tamaño de la posición es de José Luis.
- **C93 = Sí (mantiene).** El peso del terminal es del 50 % y el salto del año 11 es de convención. Con el ROIC terminal en la tasa, el g del 2 % casi no pesa (0,20 € en el tornado). Es un mercado maduro [CF_2025, PDF p. 48-49]. «If a thing can't go on forever, it will eventually stop» (PCA p.416; HIM).
- **C103 = No (mantiene).** El margen sigue a la energía (Historia fila 29), el foso es estrecho y los hornos se rehacen cada campaña. No es una empresa para guardar sin mirar.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en nueve centros de España, Portugal, Reino Unido, Irlanda y Brasil, sin ningún cliente por encima del 10 % de las ventas [ES_2025, PDF p. 98 y 104; CF_2025, PDF p. 29 y 34]. Gana dinero por dos cosas:
- traslada la energía al precio con retraso: margen EBIT del 19,7 % en 2020, 13,7 % en 2022 y 20,8 % en 2024 (Historia fila 29);
- opera con poca deuda (0,36x EBITDA, C33).

Su ROIC de cinco años es del 13,8 % (C55) frente a r = 9 %. Leo un foso estrecho: supongo que se mantiene sobre los hornos instalados, pero no sobre el capital nuevo a partir del año 11. A 90,10 € el precio pide un 14,2 % anual de crecimiento de ventas durante cinco años (C86) y está por encima de mi BUENO (81,74): no hay margen de seguridad. El precio de Sí, 57,74 €, es casi el valor sin crecimiento (58,19). Es provisional, porque depende de cuánto cuesta reponer los hornos por encima de su amortización.

**Tesis inversa (B102).** Defiendo el No con los hechos que más daño hacen:
- **Hornos que se rehacen cada campaña.** El capex fue 1,45 veces la amortización en 2021-2025 (Historia filas 8 y 12), con ventas orgánicas que cayeron un 5,4 % en 2025 [ES_2025, PDF p. 90]. La descarbonización empieza en 2026 sin capex publicado [CF_2025, PDF p. 65]. Leo que parte del beneficio contable es reposición que no se ve.
- **Un margen prestado.** El 19,9 % de 2025 (Historia C48) es energía barata que la empresa supone que irá al cliente [CF_2025, PDF p. 48], más 19,8 mm de «otros ingresos» sin explicar [CF_2025, PDF p. 73].
- **No crece por unidades.** El crecimiento de diez años es precio y compras (Historia filas 13 y 28), en un mercado que ella misma llama maduro.
- **La caja no cuadra y la dirección paga caro.** f = −2,76 % (C58). La dirección recompra a ~89,6 € [CF_2025, PDF p. 61], por encima de cualquier NORMAL que calculo, mientras se va a Brasil y Chile con un real que cayó un 20 % en 2024 [ES_2025, PDF p. 106].
- **No sé quién me mata** [CF_2025, PDF p. 31]. Si el foso no existe, la acción vale el negocio de hoy: unos 58 € o menos.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 12. Predicciones (Palancas A38:C40)

Todas con fecha de comprobación 2028-03-31, dentro de la ventana de 12-24 meses desde D4 (2026-11-12). La probabilidad de cada una está calculada dado el NORMAL.

| | Predicción | Probabilidad | Qué comprueba |
|---|---|---|---|
| 1 | Margen EBIT consolidado de 2027 entre el 16 % y el 20 % | 0,65 | La meseta frente a la mejora que se va al cliente |
| 2 | Pagos por inversiones de 2027 de al menos 1,2 veces la amortización de 2027 | 0,75 | La hipótesis que más condiciona el precio de Sí (P-M1) |
| 3 | Variación de ventas de 2027 a divisa constante y perímetro comparable entre −2 % y +4 % | 0,6 | El volumen del NORMAL, que coincide con la guía |

«comparing predictions with outcomes» (PCA p.606; HIM).

## 13. Qué me haría cambiar de cubo

- **A Sí.** Un precio por debajo de 57,74 con el negocio igual y las hipótesis sin base acotadas. O, a un precio algo mayor, tres cosas a la vez: datos de cuota que muestren un sector racional, una reposición cercana a la amortización (precio de Sí hacia 64) y un margen EBIT de al menos el 18 % en 2026-2027 pese a las bajadas de precio.
- **A No.** Cualquiera de estas: un margen de vuelta al 13,7-16,5 % de 2021-2022 sin choque de energía; compras en Latinoamérica que pidan capital sin retorno; o recompras por encima del valor junto con lo anterior.
- **A Demasiado difícil.** Cualquiera de estas: que el valor pase a depender más del real, el peso chileno y la libra que de Iberia; que f resulte ser caja que no entiendo; o que la descarbonización cambie los hornos de forma que no pueda juzgar si la ventaja de coste sobrevive.

## 14. Comparación con la etapa 1

El cubo es el mismo: Vigilar. El precio de Sí sube de ~48 € a 57,74 sobre todo por la regla:
- La v1 tomaba el mínimo entre su MALO y ¾ de su ponderado, sobre el crecimiento del FCF, a 88,7 € y con datos de 30-jun-2026.
- La v2 aplica la escalera k = 3, con el motor B y base 31-dic-2025.
- Con la regla antigua, la v2 daría 45,56 (C156): los dos MALO se parecen.

Las diferencias de fondo están en los otros escenarios:
- Mi NORMAL (61,93) queda por debajo del de la v1 (~74): pongo el ROIC terminal en la tasa y la configuración de demostración cobra la reposición (con la V6.3 efectiva sería 69,67).
- Mi BUENO (81,74 frente a ~113) no extrapola un 8 % anual de caja.

La v1 acertaba en lo esencial: un margen junto al máximo, energía que va al cliente y ningún margen de seguridad. La v2 corrige C27, C62 y C97, retira los hechos posteriores a la base y quita el porcentaje de posición de C104.

## 15. Incertidumbre pendiente (B222 · B223)

- **B222:** cuánto supera la reposición de los hornos a su amortización (P-M1, λ = 1,15, de demostración). Condiciona el precio objetivo: 57,74 con la activa, 64,37 sin requisito y de 57,03 a 63,11 entre estructuras. No condiciona la acción. Le siguen las probabilidades y el S2C del BUENO.
- **B223:** el desglose del capex de 2021-2025 y del plan 2026-2030 entre renovación de hornos, capacidad y descarbonización, con el coste de reconstruir un horno frente a su amortización. Es una pregunta a Relación con Inversores: la nota de inmovilizado [CF_2025, PDF p. 43-45] no lo separa. Y falta la decisión D-N3b, que es de la persona responsable.

## 16. Checklist de la fase C

- Una sola historia con la hoja: sí. Las seis incoherencias están anotadas y ninguna mueve el cubo ni la zona.
- Autocomprobación con contenido: diez entradas.
- Datos ausentes revisados: los 27.
- Lista de hipótesis sin fundamento: completa (4), con su limitación.
- Combinación: no procede.
- Estado, cubo y acción: coherentes con la sección 15.
- C104: sin porcentaje.
- Tres predicciones falsables sobre el negocio, con fecha y probabilidad.
- Tesis inversa con hechos.
- B222 y B223: concretos.
- Comparación con la etapa 1: honesta.
- Qué me haría cambiar de cubo: dicho.
- Citas con libro y página. Configuración V6.4 evaluada y no adoptada.
