# Fase C · turno 1 · Jumbo S.A. (BELA) · motor A · 2026-11-19

Reviso A y B como si fueran de otro: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM).

## 1. Una sola historia

Lo que calcula la hoja con mis 52 celdas: 25,88 / 37,23 / 45,44 € por acción (MALO / NORMAL / BUENO), ponderado 35,63 €, precio de Sí 32,38 € (P*, sin tope del NORMAL), regla antigua C156 = 25,88 €. Al precio de 27,28 € la zona es `cumple_regla_k`: el precio está un 15,7 % por debajo del precio de Sí (diferencia ÷ precio de Sí); el precio de Sí está un 18,7 % por encima del precio (diferencia ÷ precio). El precio está 1,40 € por encima del valor del MALO (5,1 % del precio).

La historia de la fase A es una tienda de precio bajo y surtido enorme, con diez años de margen EBIT entre el 24,8 % y el 33,4 % (Historia fila 29), sin deuda, cuyo riesgo es que las plataformas transfronterizas le quiten margen. La hoja cuenta lo mismo: el DCF inverso dice que el precio descuenta ventas que caen un 1,96 % al año con el resto del NORMAL (C86), y el valor sin crecimiento (28,12 €, margen de 2025 para siempre) está por encima del precio. En mi réplica del motor A (reproduce B78:D78 al céntimo), con el crecimiento del NORMAL el precio equivale a un margen objetivo de ≈ 22,5 %, por debajo del peor año de la serie. Lo que el mercado duda es el margen, no el crecimiento, y es justo lo que yo dudo.

Peso del terminal: 44 / 52 / 55 %, todos bajo el 75 %. Semáforos: margen sobre el Q3 del sector en los tres (G5, ya justificado en B), r bajo la r mínima, el resto en PASA; cuota implícita «—» por C24 vacío. Tornado: la tasa de descuento es la palanca que más mueve el valor (±1 punto ≈ ±6,06 € en el NORMAL). Lo digo en una línea: el valor depende sobre todo de la rentabilidad exigida. Con la r mínima de la hoja (10,19 %) y mis palancas, el precio de Sí sería ≈ 28,01 € y la zona seguiría en `cumple_regla_k`, con el precio un 2,6 % por debajo del precio de Sí (diferencia ÷ precio de Sí). La r es heredada (S-3): lo informo y no la toco.

Incoherencias que encontré (todas en `una_sola_historia.incoherencias`):

- **El cubo de A frente a la zona.** A dejó Vigilar porque el precio no daba un margen visible sin la hoja y remitió el precio de Sí a esta fase. C13 = No sigue siendo cierto (valor sin crecimiento ≈ precio), pero no es un descalificador: el cubo provisional cambia por el orden de mando. A6 dice DESCARTADA POR FILTRO PABRAI; mi cubo es otro y digo por qué.
- **C76 y J1.** La fase B bajó C76 de 200 a 160, pero C46, C40, C52 y f siguen calculados con s = 200 ÷ 471,83 (f es el mismo en `resultados.json`). Con s = 0,3391 entran 1,14 mm más al año; C40 ≈ 255,46 mm y FCF yield ≈ 6,97 %. Si pasa entero a f (±0,00093), el precio de Sí se mueve ±0,13 € (±0,4 %). Es una celda de datos: no la recalculo; la orquestación tiene que aplicar J1 antes del cierre.
- **S2C del MALO.** Con aperturas y más de 95 mm de centros [AR2025, PDF p. 25], el motor reinvierte en el MALO solo 129 mm en diez años (Δventas ÷ 1,0), sin sitio para el circulante (210 mm por 401 mm de ventas nuevas en 2022–2025, Historia filas 6 y 14). 0,75–0,8 cuadra mejor. Corregido a 0,75: precio de Sí ≈ 32,27 € (−0,3 %), misma zona y cubo. No es un error aritmético: es el extremo favorable del rango de B. Lo dejo (v2.1) y lo anoto.
- **Margen del MALO.** 0,27 está por encima de todos los años 2016–2020 (24,8–26,9 %). Con 0,25: MALO 24,33 €, precio de Sí ≈ 31,60 € (−2,4 %), misma zona. Juicio dentro del rango de B, no error.
- **FCF del año 1.** El del MALO (306,7 mm) supera al del NORMAL (291,7 mm): es la mecánica del motor, agrandada por el S2C del MALO.

Ninguna de estas incoherencias pide mover palancas: cada una mueve el precio de Sí menos de un 5 % y no cambia la zona ni el cubo. Juntas (margen 0,25, S2C 0,75 y f en contra), el precio de Sí quedaría en ≈ 31,37 € y la zona seguiría igual.

## 2. Desviaciones pendientes

Solo queda G8, el salto del año 11, en los tres escenarios (0,131 / 0,241 / 0,313). G16 y G17 no saltan (peso del terminal bajo el 75 %; sin cifra de mercado no hay cuota implícita). Lo justifico con lo que pierde la empresa en el año 11, sin cambiar la clase de ninguna palanca:

- **MALO** (0,22 → 0,09, convención): el ROIC terminal es la tasa del motor. El capital nuevo de los años 1–10 abre las últimas tiendas de un formato que funciona. En el año 11 ya no quedan sitios donde abrir y la escala de compra se ha ido al cliente. El capital nuevo solo defiende ventas que crecen al 1 %.
- **NORMAL** (0,34 → 0,10, fundamentada): en los años 1–10 el dinero nuevo va a Rumanía, Chipre, Bulgaria, socios y logística, y rinde como el viejo (ROIC sin arrendamientos 28,93 %, sección 1 bis). En el año 11 la red está hecha y el 2 % es solo precio. El margen del capital existente sigue en el terminal. Lo que se acaba es reinvertir a retornos extraordinarios: «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **BUENO** (0,43 → 0,12, fundamentada): el crecimiento sin capital propio de los socios y de Balfin [H1 2026, PDF p. 19] se agota cuando esos mercados maduran. Además, Balfin gestionará su propia cadena desde China [H1 2026, PDF p. 18]. Queda r + 3 puntos, el máximo que admito con C18 = Sí (MR p. 63; E2).

## 3. Palancas

No pido volver a la fase B (`revisar_palancas = false`). No he encontrado ninguna palanca con aritmética, perímetro o dato equivocado que cambie el cubo, la zona o el precio de Sí en un 5 % o más. El S2C del MALO no está anclado en C54: la fase B lo contrasta con el S2C medio sin arrendamientos (1,186). El ROIC terminal del MALO igual a r no es un efecto del perímetro que haya que corregir. En `celdas_corregidas` dejo C76, B16 y B15 de la fase B y C13 de la fase A con `despues = antes` y el motivo.

## 4. Autocomprobación

Va entera en el JSON. Lo que cambió: el cubo provisional, por consistencia y compromiso. Mantener Vigilar habría sido no desdecirme de la fase A, inventando una condición de espera que el MALO ya modela. Lo que pesa sin cambiar nada:

- el MALO está en el lado suave. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM);
- el precio de Sí coincide con las cifras externas (33,04 € de C38, 32,24 € de los analistas), y lo trato como sospecha, no como apoyo;
- el NORMAL atribuye a la empresa el escalón de margen de 2021;
- la única guía que sube el valor es duplicar Rumanía, en el BUENO. «A projection prepared by… an executive trying to justify a particular course of action will frequently be a lie» (TCI p.60; HIM).

Calculé el efecto de cada uno y ninguno cambia la zona.

## 5. Cubo y conclusión provisional

Orden de mando:

1. No hay bloqueo: el estado técnico INCOMPLETO solo pide las predicciones del turno 2.
2. No hay límite del modelo.
3. No hay descalificador: el más cercano es el cambio de canal, y no me impide juzgar.
4. No hay dato ausente material (punto 6).
5. La lista de hipótesis sin fundamento está vacía (punto 7).
6. Solo entonces, la zona: `cumple_regla_k`.

Cubo provisional **Sí**, conclusión provisional **comprar**. Cumplir la regla de precio no es una garantía: el precio de Sí es una convención experimental con k = 3, el MALO no es un suelo y la r está por debajo de la mínima. «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). El que vende a 27,28 € cree que el margen vuelve por debajo del 25 %. Puede tener razón. Por eso B222 nombrará ese margen.

## 6. Datos ausentes (S-19)

Reviso los 25 de `datos_ausentes.json` y ninguno es material para la conclusión favorable (`alguno_material = false`):

- **Los ceros pendientes de verificación** (adquisiciones, intereses y principal de arrendamientos, pasivo por arrendamientos y minoritarios) son de ejercicios anteriores a la NIIF 16 o de años que no entran en las anclas.
- **La SBC** está tapada por tres hechos: no hay plan de acciones, el estado de flujos no tiene ajuste por pagos en acciones y el BPA básico es igual al diluido.
- **Mercado, cuota y competidores** afinarían el MALO y el BUENO. Lo que decide el valor, el margen, tiene diez años de hechos.
- **Las ventas comparables** faltan, pero las acotan la red estable de 89 tiendas en H1 2026 y las ventas un 4,4 % arriba [H1 2026, PDF p. 7 y p. 37].
- **El capex por destino, el coste de los centros, la inversión por tienda y el capital en Balfin** mueven el S2C. Dentro de los rangos de B, el precio de Sí queda entre ≈ 31,56 y 32,27 € y la zona no cambia.
- **Las guías, el rating, el capital regulatorio y la cartera de pedidos** no tocan ninguna celda.

## 7. Fundamento material (D10)

Recorrí las hipótesis materiales del Anexo B §B.6 (B14:D16, B18:D18, B68:D69, C22, C23, C76, C44, C62, C8, C6 y B65:D66):

- ninguna es «sin juicio propio» ni «técnico»;
- todas las fundamentadas o de convención citan hechos con celda o página;
- las narrativas tienen mecanismo, dueño de la mejora y freno con hechos del extracto.

La lista `hipotesis_sin_fundamento` queda vacía y el resultado es `sin_limitacion`. No procede la comprobación conjunta: no hay ninguna hipótesis que combinar. Las sensibilidades de los puntos 1 y 4 son información mía, no una comprobación del script. Sobre la vara del foso: no me apoyo en el ROIC del capital propio pagado el alquiler (NO COMPROBADO). C18 = Sí se sostiene con diez años de margen frente al sector, y ningún ROIC terminal pasa de r + 3 puntos.

## 8. La hipótesis que más condiciona

`Palancas!C15`, el margen objetivo del NORMAL (0,32): que la franja de 2021–2025 aguante diez años con el margen bruto bajando (55,61 → 54,72 → 53,53 % [AR2025, PDF p. 15; H1 2026, PDF p. 7]). La elijo por juicio, no por el tornado: el precio equivale a un margen de ≈ 22,5 %. Lo resolvería el informe anual de 2026, con el margen bruto y el margen EBIT del grupo y el resultado de Rumanía. Lo completaría una pregunta a Relación con Inversores por las ventas comparables por país de 2024 a 2026.

# Fase C · turno 2 · conclusión

## 9. Comprobación conjunta y estado

No existe `comprobacion_conjunta.json`: con la lista de hipótesis sin fundamento vacía no procedía, y `sobrevive` queda `null`. El fundamento es `sin_limitacion`.

El orden de mando no cambia: no hay bloqueo, límite del modelo, descalificador ni dato ausente material, y la zona es `cumple_regla_k`. Antes del contradictor: concluido · Sí · comprar. **Tras la respuesta al contradictor (sección 15): estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción esperar**, con precio objetivo de 32,38 € y una condición que no es de precio.

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 32.38 · zona cumple_regla_k · precio de Sí ≤ 32.38 · precio esc. MALO 25.88 · ponderado 35.63 · fundamento no procede (conclusión no favorable)». El tamaño de la posición lo decide José Luis.

Lo que esta conclusión no es: no es una garantía. El precio de Sí sale de una convención k = 3 cuya suficiencia no está demostrada. El MALO no es un suelo: el precio está solo 1,40 € por encima de su valor, y mi MALO está en el lado suave. La r heredada está por debajo de la mínima de la hoja: con la r mínima, el precio de Sí bajaría a ≈ 28,01 €. Queda pendiente para la orquestación recalcular C46, C40, C52 y f por J1 (±0,13 € en el precio de Sí).

## 10. Tesis (B101)

1. Jumbo es un minorista de precio bajo y surtido enorme que compra directo, sobre todo en Asia [AR2025, PDF p. 24], con diez años de margen EBIT entre el 24,8 % y el 33,4 % (Historia fila 29) y sin préstamos [H1 2026, PDF p. 9].
2. El foso es la escala de compra y el formato. Cuánto dura frente a las plataformas es la pregunta abierta, con el margen bruto bajando del 55,61 % al 53,53 %.
3. La dirección devuelve la caja y recompró a 25,42 €.
4. A 27,28 € el precio no paga crecimiento (valor sin crecimiento 28,12 €) y queda bajo el precio de Sí de 32,38 €.
5. Esperar (sección 15): la regla se cumple, pero tres hechos que mis escenarios no recogían bajan los tres valores y la dejan en el filo con la r mínima.

## 11. Tesis inversa (B102)

El precio se sostiene solo con el margen, y el margen baja:

- **Margen.** El margen bruto pasa del 55,61 % al 54,72 % y al 53,53 %, y el EBITDA del 36,77 % al 35,34 % [AR2025, PDF p. 15; H1 2026, PDF p. 7]. Mientras, crecen plataformas que la empresa acusa de romper la igualdad de condiciones [AR2025, PDF p. 23].
- **El escalón de 2021.** El salto de margen de 2021 llegó con la salida de la pandemia (Historia fila 29). Si el margen vuelve al 25 %, el MALO valdría ≈ 24,3 €, un 11 % bajo el precio.
- **Crecimiento.** Se frena: beneficio de 2025 plano (fila 9), Rumanía −6,50 % en ventas [H1 2026, PDF p. 6], Grecia sin apertura en 2027 [H1 2026, PDF p. 17] y guías incumplidas [AR2025, PDF p. 58].
- **Dependencia de China.** El 70 % del producto viene de Asia, sobre todo de China [AR2025, PDF p. 24], y Balfin montará su propia cadena desde allí [H1 2026, PDF p. 18].
- **Caja de la base favorecida.** El capex de 2025 quedó bajo la amortización (filas 12 y 8), el inventario sube un 19 % (C31) y vienen más de 95 mm en centros [AR2025, PDF p. 25].
- **Convenciones.** La compra depende de dos: la r bajo la mínima y la regla k = 3. Con la regla antigua (C156 = 25,88 €), el precio de 27,28 € no daría para comprar.

Es el nivel que pide «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM). Lo que me hace mantener la compra pese a todo: incluso con margen 0,25, S2C 0,75 y f en contra a la vez, el precio de Sí quedaría en ≈ 31,37 € (mi réplica del motor). Y el precio actual equivale a un margen de ≈ 22,5 % con el crecimiento del NORMAL, por debajo del peor año de la serie.

## 12. Predicciones (dado el NORMAL)

| Predicción | Fecha de comprobación | Probabilidad | Por qué |
|---|---|---|---|
| Margen EBIT del grupo de 2027 ≥ 30 % | 2028-04-30 (informe anual de 2027) | 0,75 | Ningún año de 2021–2025 bajó del 31,7 % |
| Ventas netas de 2027 > 1.330 mm | 2028-04-30 | 0,75 | Equivale a ≈ +3,9 % al año frente al ≈ +6 % de enero–agosto de 2026 [H1 2026, PDF p. 67] |
| Al menos 92 hipermercados propios a 30.06.2028 | 2028-09-30 (semestral de H1 2028) | 0,7 | Las guías de aperturas se han incumplido [H1 2026, PDF p. 17] |

## 13. Qué me haría cambiar de cubo

- **De nuevo a Sí:** cumplirse la condición (margen EBIT de 2026 del 31 % o más y margen bruto del 54 % o más) con la escalera corregida todavía en cumple_regla_k.
- **A No:** un margen EBIT bajo el 30 % dos años sin causa transitoria, deuda nueva, o capital propio en Balfin, Canadá o los pop-ups sin retorno publicado.
- **A Demasiado difícil:** un margen que pase a moverse con el dólar, el flete o los aranceles, o ventas que caigan sin que pueda separar las plataformas del consumo.

## 14. Comparación con la etapa 1

La etapa 1 decía Vigilar a 24,72 €, con un precio de Sí de ≈ 19 € (regla antigua, estimado). La v2 dijo Sí a 27,28 €, con 32,38 €, y tras el contradictor queda en Vigilar (esperar), con el mismo precio de Sí. La mayor parte de la diferencia es la regla: con la regla antigua la v2 daría 25,88 € y no compraría. El resto:

- un MALO más suave (EBIT 0,27 frente a un EBITDA hacia el 25–28 %);
- probabilidades que restan (0,25 / 0,6 / 0,15);
- C76 de 160 con el precio ya sin el 1,00 € extraordinario.

Lo digo sin blandura: el cambio de cubo depende sobre todo de la convención de precio del ejercicio, no de un hecho nuevo del negocio. Y de los dos errores opuestos, el que tengo más cerca sigue siendo pagar por una calidad cuya duración no puedo medir: «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; HIM). Aquí la prima es pequeña: el precio no paga crecimiento.

## 15. Respuesta al contradictor

Comprobé en los textos los tres hechos que cita y reproduje sus cuentas con mi réplica del motor (que reproduce B78:D78). Las tres objeciones son válidas y ninguna queda rebatida; solo rebato los extremos altos de O1 y O3.

| Objeción | Respuesta | Dato | Efecto |
|---|---|---|---|
| O1 · el tipo impositivo de 2025–2026 es mayor que el de C52 (0,17988) | no rebatida (rebato solo el extremo alto) | Tipo de 2025: 18,93 % [AR2025, PDF p. 148], con Pilar II de 2,20 mm [AR2025, PDF p. 180]. El 19,97 % de H1 2026 no es anual: H1 2025 dio 19,77 % frente al 18,93 % del año [H1 2026, PDF p. 23] | Precio de Sí 32,00 € (−0,38 €); la zona no cambia |
| O2 · f lleva un 2023 atípico | no rebatida | Caja inicial de 802,9 mm repartida en dividendos (400,98 mm) y bono (200,39 mm); intereses de 18,49 mm e impuesto pagado bajo el devengado [AR2024, PDF p. 154] | f de 2024–2025 con J1: 32,20 € (−0,18 € neto); la zona no cambia |
| O3 · el MALO no paga los centros de distribución | no rebatida (rebato solo la cota alta) | Más de 95 mm en tres años [AR2025, PDF p. 25], frente a 37,4 mm de reinversión del MALO en los años 1–3. La cota alta exagera: Rumanía abrió Timisoara en 2025 [AR2025, PDF p. 21] con 7,09 mm de altas en todo el país [H1 2026, PDF p. 38] | MALO 25,48 €, precio de Sí 32,18 € (−0,20 €); la zona no cambia |
| Conjunto | regla de movimiento | Combinación suave: precio de Sí ≈ 31,64 €; dura: ≈ 30,96 €. Valor sin crecimiento ≈ 27,3–27,7 €; con la r mínima, ≈ 27,35 € | Un escalón a la baja: de comprar (Sí) a esperar (Vigilar) |

Tres objeciones válidas no rebatidas, las tres a la baja: un solo escalón, el máximo por dirección. La zona sigue en `cumple_regla_k` con r = 0,09 y k = 3. Lo que cambia es la holgura:

- el valor sin crecimiento queda casi en el precio;
- con la r mínima de la hoja, la regla queda a siete céntimos del precio;
- el MALO se aleja más de un suelo.

El aviso contrario del contradictor (la fecha de valoración, de +0,5 a +2,1 €) no lo cuento como rebatida: no está calculado en el expediente.

**Conclusión final: concluido · Vigilar · esperar.** Precio objetivo: precio de Sí ≤ 32,38 € (`precio.json`). Como el precio ya cumple la regla, la espera tiene una condición que no es de precio. Hacen falta dos cosas:

- que el informe anual de 2026 publique un margen EBIT del grupo del 31 % o más y un margen bruto del 54 % o más;
- que se corrijan, sin errores, el tipo impositivo (Historia C52), f sin 2023 y con J1 (Historia C58) y los centros en el MALO (Palancas!B16, vuelta a la fase B).

`fundamento_material.resultado = no_procede`; la lista de hipótesis sin fundamento sigue vacía.
