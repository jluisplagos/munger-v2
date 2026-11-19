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
