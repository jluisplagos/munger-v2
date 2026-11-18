# Ahold Delhaize · fase C · turno 1 · 2026-11-18

Páginas: AR2025, AR2024, Q2-26 y Q3-26 con la marca [PDF PAGE n] del texto, como en el extracto. «Historia» y las celdas Cnn de Historia son de `datos_v63.md`. Las cifras de la hoja son de `resultados.json` y la escalera es la de `precio.json`; no la recalculo. Para medir correcciones uso una réplica de la fórmula del motor que reproduce B78:D78 a cuatro decimales (28,0098 / 37,4807 / 44,2809). Reviso A y B como si fueran de otro: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM).

## 1. Una sola historia

Lo que la hoja calcula con mis 52 celdas:

- Valores por escenario: 28,01 / 37,48 / 44,28 €; ponderado 36,95 €; precio 36,05 €.
- Valor sin crecimiento: 34,70 € en los tres. El crecimiento vale −6,69 € en el MALO, +2,78 € en el NORMAL y +9,58 € en el BUENO.
- Rentabilidad marginal de los años 1-10: 5,9 % / 10,1 % / 12,4 %.
- Peso del terminal: 42 % / 52 % / 56 %.

La historia de la fase A se reconoce en esas cifras. Es un negocio cuyo retorno se parece a r. Crecer casi no crea valor. El valor depende de cuánto del ahorro se queda en casa: en el tornado, el margen a ±2 puntos mueve 18,80 €; el crecimiento, 0,91 €; el g, 0,16 €. Es la pregunta de Munger: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

Encuentro tres incoherencias.

**(a) Perímetro de las palancas frente al del motor. Es una palanca mal derivada y pido revisarla.**

- *El motor.* Reinvierte en el perímetro A2_propio (`motor_a_f1.json`). La reposición es la amortización propia, sin derechos de uso ni PPA. La amortización de los derechos de uso queda dentro del margen. La declaración pide «un solo perímetro para f, el ancla de S2C, el margen y el ROIC del terminal».
- *Las palancas de la fase B.* El S2C (2,5/3,2/3,5) sale de ventas ÷ capital invertido con el pasivo por arrendamientos (Historia!C54 = 3,19). El ROIC terminal (0,08/0,09/0,09) sale de la serie de ROIC con ese mismo capital (Historia!C55 = 8,8 %). El capital invertido salta de 17.840 a 25.568 mm en 2018 con la NIIF 16.
- *El efecto.* El local arrendado se cobra dos veces: su coste en el margen (1.400 mm de amortización de derechos de uso en 2025, AR2025 PDF p. 272) y su capital en la reinversión.
- *Dónde se ve.* El NORMAL reinvierte unos 721 mm al año para crecer un 2,5 %, y su flujo del año 1 cae a 2.142 mm. Pero la reinversión neta orgánica fue de 198, −46 y 85 mm en 2023-2025 (Historia).
- *Las cifras sin arrendamientos.* Ventas ÷ capital propio va de 3,89 (2018) a 5,43 (2025), y el ancla A1_sin_ROU de la capa F1 es 5,10. El ROIC sobre ese capital fue 15,8 %, 16,3 %, 13,3 %, 12,6 % y 16,1 % en 2021-2025.
- *Cuánto mueve.* Con la réplica:
  - solo el S2C a 3,9/5,4/5,7: precio de Sí 35,88 € (+4,3 %), zona vigilar;
  - S2C y ROIC a 0,13/0,15/0,15: precio de Sí 37,68 € (+9,6 %), y el precio pasa a cumple_regla_k.
- *Por qué la guarda no lo vio.* La guarda V-F1g se evaluó a las 12:36, antes de que existiera `fase_b.json` (12:47): comprobó la declaración, no las cifras.

Cambia la zona y mueve el precio de Sí más de un 5 %. No la dejo como error prudente.

**(b) El flujo base del motor no es la caja que cuenta la fase A.**

- *Las tres cifras.* El motor parte de 2.770 mm al año, que es el NOPAT de 2025 menos f × ventas. El FCF base es 2.312 mm (Análisis!C52) y la fase A habla de «unos 2.000 mm al accionista».
- *Lo que dice K3.* La conciliación de `motor_a_f1_resultado.md` lo explica con dos partidas: +381 mm por el EBIT de 2025 frente a la media de 2023-2025, y +79 mm de inversión neta.
- *De dónde salen los +381 mm.* Son sobre todo cargos. El EBIT IFRS quedó 758, 824 y 192 mm por debajo del subyacente en 2023-2025 (subyacente 3.604, 3.608 y 3.734, AR2025 PDF p. 42, 49).
- *Lo que falta en el flujo.* No hay ninguna partida explícita para los intereses de arrendamientos (465 mm en 2025, AR2025 PDF p. 227) ni para los intereses netos (C48 = 77). f = 0,00014 se calibró en una ventana en la que los cargos los compensaban.
- *Cuánto pesa.* Cada 100 mm de flujo son 1,25 € por acción.

No es una palanca y no la toco. Es una celda de datos y la conciliación propia del modelo A con arrendamientos, que la capa F1 declara «condición necesaria, no suficiente». Empuja en sentido contrario a (a).

**(c) La zona es frágil en los dos sentidos.** El precio está a 1,66 € del precio de Sí.

- El perímetro de (a) lo sube hasta un 9,6 %.
- Un margen NORMAL de 0,035, con los cargos de 2023-2025 tratados como gasto recurrente, lo baja un 5,9 % y deja la zona en caro.
- La duda de (b) lo baja 1,25 € por cada 100 mm.

La conclusión no se apoya en la zona. Esto no cambia el cubo, pero la escalera debe llegar al turno 2 con las palancas en el perímetro del motor.

**Lo que no es incoherencia.**

- *Salto del año 11 (ninguno llega a 5 puntos; no hay G8).*
  - BUENO, +3,4 puntos: cada euro nuevo rinde 12,4 % en los años 1-10 y vuelve a r en el año 11. Es la ventaja que se pierde cuando los competidores igualan precios, coherente con C18 = No: «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).
  - MALO, −2,1 puntos: el capital comprometido rinde 5,9 % en los años 1-10, y el terminal reinvierte al 8 %, que es lo que la empresa ganó con márgenes del 3,1-3,2 % (7,9 % y 7,4 % en 2023-2024, Historia fila 33). Con B18 = 0,06 el precio de Sí bajaría un 0,7 %: no cambia nada.
- *Peso del terminal:* 52 % en el NORMAL, lejos del 75 %; no hay G16.
- *Cuota implícita:* «—», porque C24 está vacía; no hay G17.
- *DCF inverso.* C86 = −1,2 %, pero la tabla es casi plana: 33,59 € con −10 % y 38,15 € con +4 %. Con rentabilidad marginal ≈ r, crecer no crea valor. Lo que el precio descuenta es el margen: 36,05 € equivale a un margen NORMAL del 3,85 % (el 3,84 % de 2025 sostenido), y el precio de Sí, a uno del 3,67 %.

## 2. Desviaciones pendientes

`gramatica.md` no deja G8, G16 ni G17: las cifras no las disparan. La única desviación es G5 BUENO, ya justificada en la fase B, y la reviso.

- *Margen.* 0,045 es el redondeo de volver al 4,39 % y 4,33 % de 2021-2022.
- *Mecanismo.* Escala y mezcla en Europa: de 3,3 % a 3,8 % en 2023-2025 (AR2025 PDF p. 49) y 4,0 % en el 3T de 2026. Marca propia por encima del 40 % (Q2-26 PDF p. 4). Online rentable (AR2025 PDF p. 44).
- *Quién se queda la mejora.* La empresa, solo si los competidores no igualan cada bajada. Por eso p(BUENO) = 0,2, igual que la frecuencia observada.
- *Lo que añado.* Parte de la mejora europea de 2026 es un impuesto belga menor y las sinergias de Rumanía (Q3-26 PDF p. 7, 8). Es una razón más para la confianza baja, no para subir el margen.

## 3. Palancas a revisar

Pido `revisar_palancas = true`, una sola vuelta. Las dos van al alza, al perímetro A2_propio:

- **Palancas!B16:D16.** Ventas ÷ capital propio sin arrendamientos.
- **Palancas!B18:D18.** ROIC sobre ese capital. Si sale por encima de r + 3 puntos, G4 se justifica como efecto del perímetro, no como foso. C18 = No se mantiene, porque el ROIC con todo el capital (8,8 %) es la medida económica: el accionista también soporta la renta del 85 % de locales arrendados (AR2025 PDF p. 58).

No toco nada más. `celdas_corregidas` deja todo con `despues = antes`.

Revisé C15 por los cargos: 0,04 sale de la media IFRS de cinco años (3,78 %) y del 3,84 % de 2025, no de un error de derivación. Lo dejo como fragilidad declarada. «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM): en dos de cinco años no fue como un reloj, y en 2025 bajó a 192 mm.

## 4. Autocomprobación

Las diez tendencias están en el JSON. Las que cambian algo:

- **Consistencia y compromiso.** Todas las desviaciones de la fase B fueron a la baja. La evidencia contraria existe, es el perímetro, y la pido aunque favorezca comprar.
- **Doble castigo del mismo riesgo.** Es el mismo hallazgo visto desde el otro lado: el local arrendado cobrado en el margen y en la reinversión.
- **Autoridad.** El margen NORMAL de 0,04 coincide con la guía subyacente de la dirección. Sale de la Historia, pero solo si los cargos de 2025 son los normales.
- **Anclaje en el precio.** Los valores están cerca del precio, pero por la gramática (ROIC ≈ r), no por anclaje.
- **¿El MALO es de verdad malo?** El MALO es real y ya pasó dos años: «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** La rigidez de la renta (14.721 mm de pagos sin descontar y unos 35.000 mm más en prórrogas, AR2025 PDF p. 271, 272) y la recompra de 2026 a 35,41 € (Q3-26 PDF p. 21), casi a mi ponderado, no están en ninguna palanca. Van a B102.

## 5. Cubo y conclusión provisionales: No · descartar

Sigo el orden de mando:

1. *Bloqueo:* no hay. La gramática da 0 errores y el estado técnico solo espera las predicciones del turno 2.
2. *Límite del modelo:* no hay. El motor A sigue siendo el adecuado; la duda F1 es de cálculo, no de elección.
3. *Descalificador mío:* sí. No pasa el segundo filtro. El ROIC con todo el capital es 8,8 % frente a r = 0,09, el ahorro va al precio y la hoja lo confirma: rentabilidad marginal 10,1 % en el NORMAL y un crecimiento que vale 2,78 €. Es el No de la sección 7 («lo evalué y no cumple»), con el descalificador del negocio que reinvierte con retorno mediocre a medias.

Con eso la conclusión es `descartar`, sea cual sea la zona. Hoy la zona es «vigilar»:

- el precio está un 4,8 % por encima del precio de Sí (diferencia ÷ precio de Sí);
- el precio de Sí está un 4,6 % por debajo del precio (÷ precio).

Si tras la revisión el precio quedara en cumple_regla_k, la conclusión seguiría siendo descartar. Cumplir la regla de precio no hace bueno el negocio: «it's not worth an infinite price» (TCI p.29; HIM) tiene su reverso, y un negocio de retorno igual a r a su valor no deja nada.

## 6. Datos ausentes (S-19)

Los 29 datos están revisados uno a uno y ninguno es material: `alguno_material = false`.

- Los dos ceros pendientes de verificación (arrendamientos de 2016-2017, antes de la NIIF 16, y minoritarios, que el informe da como cero) no tocan ninguna ancla que use.
- Lo que falta sobre cuota, competidores, margen por marca y precio, volumen y mezcla sería imprescindible para un Sí. Para descartar no lo es, porque el No sale del retorno del grupo.

## 7. Fundamento material (D10)

La lista recoge dos hipótesis: S2C (B16:D16) y ROIC terminal (B18:D18). Las dos son fundamentadas con hechos, pero de otro perímetro.

Los rangos tienen base:

- S2C: MALO 2,5-3,9, NORMAL 3,2-5,4, BUENO 3,5-5,7.
- ROIC: MALO 0,08-0,13, NORMAL y BUENO 0,09-0,16.

En los dos, el límite bajo es el capital con arrendamientos y el alto, el capital propio de la Historia. Con conclusión no favorable, el resultado es `no_procede` y no hago comprobación conjunta. El resto de celdas materiales (motor, caso especial, base del margen, narrativas, probabilidades, quiebra, C76) son fundamentadas o de convención con hechos citados.

## 8. Lo que más condiciona y lo que lo resolvería

Lo que más condiciona es Palancas!B18:D18: su perímetro decide si el precio queda en vigilar o en cumple_regla_k. No condiciona el descarte, que descansa en C18.

Lo resolverían dos datos:

- el importe en libros de los derechos de uso y de la PPA al cierre de 2021-2025 (notas de arrendamientos e intangibles), para medir S2C y ROIC sin aproximar;
- la conciliación propia del motor A con arrendamientos: dónde entran los 465 mm de intereses de arrendamientos y si f, calibrada con 758 y 824 mm de cargos, vale para un año base con 192.
