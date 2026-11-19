# Zoetis Inc. (ZTS) · fase C · turno 1

## 1. Una sola historia

La hoja, con mis 52 celdas, da MALO 57,20 · NORMAL 81,65 · BUENO 124,61 · ponderado 82,91 (resultados.json). La escalera de precio.json: precio esc. MALO 57,20 · precio de Sí 73,27 · ponderado 82,91 · zona `cumple_regla_k`. El precio (73,08) está un 0,26 % por debajo del precio de Sí (diferencia ÷ precio de Sí). El precio esc. MALO está un 21,7 % por debajo del precio (diferencia ÷ precio).

Lo que cuenta la hoja cuadra con la fase A: un negocio de márgenes altos que crece poco en el NORMAL (3,5 %) y cuyo valor depende de cuánto dura la ventaja. Peso del terminal 49 %, 57 % y 65 %: todos bajo el 75 %. El ROIC terminal está en la tasa del motor en el MALO y el NORMAL, así que el valor lejano apenas depende de g. El DCF inverso: el precio descuenta ≈1,3 % de crecimiento de ventas en 2026–30 con el resto del NORMAL (C86 = 0,0126). Es una historia entre mi MALO (0 %) y mi NORMAL (3,5 %). La guía de 2026 ((3) %–(1) % orgánico) es guía, no hecho. El tornado dice que manda el ROIC a largo plazo: ±5 puntos mueven 42,13 USD el NORMAL. Es información, no criterio. Pero coincide con lo que declaré no saber: cuánto duran Simparica y Apoquel.

Incoherencias (ninguna pide mover palancas):
- La fase A atribuye a Historia!C55 un 27,7 % que «dobla» al sector. C55 es 0,236 (media 2021–25 del ROIC con la I+D capitalizada). Frente al sector (0,147) es 1,6 veces. No cambia C18 = No: con US GAAP no hay vara F1 (datos_v63 §1 bis) y C55 solo se compara con el sector. La fase B ya usó 0,236.
- C93 heredada se apoya en un ROIC de ≈27 %. Mi terminal NORMAL usa 0,08 y g 0,025: reinvierte ≈31 % del beneficio operativo. Se re-decide en el turno 2.
- B101, B102 y C104 heredadas citan ≈49 USD y un «0 %». La escalera vigente es otra y D16 prohíbe el porcentaje. Se reescriben en el turno 2.
- La zona invitaría a comprar; A6 dice «DESCARTADA POR FILTRO PABRAI · fuera del círculo (C12)». Mi cubo es Demasiado difícil por el descalificador. La zona es el último criterio.
- El MALO tiene más FCF en el año 1 (2.519) que el NORMAL (2.255) y que 2025 (≈2.196, derivado). Con crecimiento 0 el motor no pide reinversión neta. Es la identidad del motor, no un error. Supone que mantener las ventas planas no consume capital.
- La hoja resta los pasivos netos de 31-dic-2025 (6.779) con las acciones de esa fecha. La pareja es coherente; con junio de 2026 el NORMAL cambiaría ≈0,1 USD (derivado).

La zona es frágil (aproximaciones mías con el valor terminal de resultados.json; el método reproduce el −42,13 del tornado). Con el ROIC del BUENO en 0,11, el precio de Sí sería ≈72,92. Con el MALO y el NORMAL en la tasa exacta (0,0757) en vez de 0,08, ≈72,66. En los dos casos la zona sería `vigilar`. El BUENO aporta el 71 % de la ganancia esperada al precio de Sí. La zona aquí no informa de nada.

## 2. Desviaciones pendientes

Solo G8 (salto del año 11). No hay G16 (peso del terminal bajo el 75 %) ni G17 (sin C24).

- **MALO, 6,4 puntos.** Rentabilidad marginal 0,6 × 0,30 × (1 − 0,1997) ≈ 14,4 % → ROIC terminal 0,08 (tasa del motor redondeada). Supongo que la erosión de hoy en dermatología y Simparica Trio alcanza a toda la cartera de compañía, como alcanzó a Draxxin (−66 %, 10-K 2025 PDF p. 42). El capital nuevo solo gana su coste. Convención del caso neutro.
- **NORMAL, 13,8 puntos.** 0,8 × 0,34 × (1 − 0,1997) ≈ 21,8 % → 0,08. En los años 1–10 crece sobre franquicias con exclusividad y capacidad pagada. En el año 11 supongo que las de hoy (Simparica y Apoquel, el 28 % de los ingresos, 10-K 2025 PDF p. 44) han perdido la exclusividad o han sido igualadas. No conozco sus fechas: el año 11 es el horizonte del modelo. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Convención.
- **BUENO, 17,6 puntos.** 1,0 × 0,37 × (1 − 0,1997) ≈ 29,6 % → 0,12. Lo lanzado en 2026–30 (Lenivia y Portela, 10-K 2025 PDF p. 12) conserva parte de su exclusividad: tres puntos sobre C56, el exceso a perpetuidad que el criterio admite como mucho (MR pp. 62–63; E2). Frente a la tasa del motor son 4,4 puntos. Fundamentada.

## 3. Palancas

No pido revisión. No veo ninguna palanca mal derivada: comprobé la aritmética del crecimiento (MALO ≈0 %, NORMAL ≈3,6 %, BUENO ≈6,5 % con sus supuestos), el margen medio (0,34), la media de 2023–25 (0,37) y los S2C de Historia. D18 = 0,12 mide el exceso contra C56, como la referencia v2.1 y G4. Contra la tasa del motor es mayor. Es una convención declarada, no un error de aritmética, perímetro ni dato. Lo calculo igual: con 0,11 el precio de Sí bajaría ≈0,5 % y la zona pasaría a `vigilar`. No cambian ni el cubo ni la conclusión. Queda en `celdas_corregidas` con después = antes, junto a C12 y C18.

## 4. Autocomprobación

Las diez tendencias están en el JSON. Lo que más pesa:
- **Anclaje en el precio**: el precio de Sí queda a 0,19 USD del precio. Las palancas se fijaron antes del recálculo y subir el MALO a 0,3 bajó el precio de Sí. La cercanía es casual.
- **Optimismo del BUENO**: el BUENO sostiene la zona (71 % de la ganancia esperada). Su ROIC terminal es 4,4 puntos sobre la tasa del motor.
- **¿El MALO es malo?** Es real, pero no es un precipicio. No incluye que Simparica y Apoquel caigan como Draxxin (≈18 % de los ingresos, derivado). «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). El precio esc. MALO no es un suelo.
- **Disponibilidad**: el MALO 0,3 descansa en dos trimestres. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).

Ningún hallazgo cambia una palanca. Todos van a la tesis inversa del turno 2.

## 5. Cubo y conclusión provisionales

Orden de mando: no hay bloqueo (gramática sin errores). No hay límite del modelo. Hay un descalificador de la fase A: no sé juzgar si el foso dura. Las franquicias que deciden el valor pierden cuota frente a moléculas de otros mientras siguen protegidas (dermatología −10 puntos, pres. T2 2026 PDF p. 6). Juzgar si la I+D las sustituye es ciencia que no sé juzgar. «I do not understand whether or not their moats will last» (AIWTK p.131; HIM). Con un descalificador, la conclusión es `demasiado_dificil` aunque la zona sea `cumple_regla_k`.

**Cubo provisional: Demasiado difícil. Conclusión provisional: `demasiado_dificil`.** «We have three baskets: in, out, and too tough. We have to have a special insight, or we'll put it in the 'too tough' basket» (TCI p.13; HIM). No es un No: no lo evalué malo.

## 6. Datos ausentes (S-19)

Reviso los 26 datos uno a uno en el JSON. Dos son materiales para una conclusión favorable: las fechas de pérdida de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela, y la cuota y la identidad del competidor que gana la cuota de dermatología. Sin ellos no podría sostener `comprar` ni un precio objetivo. `alguno_material = true`. No afectan a `demasiado_dificil`, que va antes en el orden de mando (sección 15). Aun con esos datos, el descalificador sigue en pie: la erosión de 2026 ocurre bajo patente, y quién gana depende de una ciencia que no sé juzgar. Los otros 24 no tocan ninguna conclusión. Los arrendamientos y los minoritarios mueven céntimos. Los ceros de intereses son lo esperado con US GAAP. El capex mueve el S2C en décimas. China es el 2 % de los ingresos.

## 7. Fundamento material (D10)

La lista `hipotesis_sin_fundamento` está vacía. Ninguna palanca, probabilidad, quiebra, C76 ni C44 tiene clase «sin juicio propio» ni «técnico». Todas citan hechos en su apoyo. Las narrativas B65:D66 tienen mecanismo y «qué lo pararía» con hechos. La conclusión no es favorable: `resultado = no_procede`. No hago la comprobación conjunta.

## 8. La hipótesis que más condiciona

Análisis!C12 y su traducción en Palancas!B18:D18: cuánto duran Simparica y Apoquel frente a competidores que ya les quitan cuota. Ningún documento de hoy lo resuelve solo. Reabrirían el análisis tres cosas. Las fechas de exclusividad de las cuatro franquicias: el 10-K 2025 PDF p. 17 solo las da para Excede y Cerenia, así que hay que preguntarlas a Relación con Inversores. El nombre y el producto del competidor que gana cuota en dermatología. Y dos o tres trimestres de cuota estable de dermatología y Simparica Trio en clínicas de EE. UU., con precio realizado positivo (presentaciones del T3 2026 al T2 2027).
