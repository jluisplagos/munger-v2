# Elis SA · fase C, turno 1 · motor A · plantilla V6.3 · base 31-dic-2025

Millones de euros salvo que diga otra cosa. Fuentes como en las fases A y B: URD2025, DEU2024 (en francés; lo cito traducido), H1-2026, comunicado OCEANE; celdas de `datos_v63.md`, `resultados.json` y `precio.json`. Separo tres cosas: **hecho** (está en un documento o lo calcula la hoja), **interpretación** (mi lectura, con su cálculo) y **propuesta** (lo que pido a otro; no lo adopto). Las cifras «fuera de la hoja» salen de una réplica del motor A en Python que reproduce al céntimo B78:D78 (5,01 / 7,03 / 9,78), C83 (7,17) y el precio de Sí (6,56); el script queda en el directorio temporal de la sesión. Son interpretación, no sustituyen a la hoja.

## 1. Una sola historia

**Lo que dice la hoja (hechos).** Precio 24,18 € (C37). Escalera de `precio.json`: precio esc. MALO 5,01 €, precio de Sí 6,56 €, ponderado 7,17 €, BUENO 9,78 €; zona **caro**. El precio de Sí está un 72,9 % por debajo del precio (diferencia ÷ precio); el precio está un 268,8 % por encima del precio de Sí (diferencia ÷ precio de Sí). Regla antigua C156: 5,01 €. Valor sin crecimiento 10,66 €/acción; el crecimiento con la mejora de margen vale −5,38 / −3,27 / −0,37 € en MALO / NORMAL / BUENO. FCF del año 1: 139,3 / 75,3 / 89,0; del año 10: 131,5 / 214,6 / 286,9. Peso del terminal 0,50 / 0,66 / 0,65 (bajo el 75 %). Salto del año 11: 0,47 / 0,68 / 2,41 puntos (bajo 5). DCF inverso no utilizable (B193: «con tus palancas crecer destruye valor»). Tornado (información, no criterio): margen ±2 pts mueve el NORMAL ±3,29 €; ROIC ±5 pts, 2,78 €; S2C ±0,3, 1,43 €; tasa ±1 pt, 1,42 €. Veredicto A6: DESCARTADA POR FILTRO PABRAI (C13 = No); mi cubo es Vigilar porque el problema es el precio, no el negocio. Estado técnico INCOMPLETO por las tres predicciones (A38:A40): son celdas de la fase C que este turno no escribe (el prompt manda `celdas = null`); van en el turno 2.

**Incoherencias que encuentro.**

1. *La caja de la hoja no es la de la fase A.* La fase A cuenta «unos 308 mm al año como punto de partida, que crecen con el orgánico». La hoja hace caer el FCF del NORMAL a 75,3 en el año 1 y no vuelve a 214,6 hasta el año 10. Hecho de contraste: el FCF al accionista después de adquisiciones fue 215,2 / 150,4 / 220,4 en 2023–25 (Historia: FCF 297,3 / 333,7 / 338,0 menos adquisiciones 82,1 / 183,3 / 117,6; 2025 y 2024 en [URD2025, PDF p. 327]), con un crecimiento parecido al del NORMAL (2025: +3,8 % orgánico y +1,8 % de perímetro [URD2025, PDF p. 307]). El año 1 del NORMAL es la mitad del peor de esos tres años. No es la misma historia. La causa es el ancla f (punto 3), no una palanca.
2. *El semáforo y el motor miden distinto el mismo euro.* G7 lee una rentabilidad marginal del 10,7 % en el NORMAL (S2C 1,2 × 0,125 × 0,712). El motor resta además f × ventas a cada euro nuevo de ventas: (0,125 × 0,7118 − 0,0417) × 1,2 = 5,7 %, por debajo de r = 0,09 (cálculo propio con Historia C52 y C58). Por eso «crecer destruye valor» y el DCF inverso no aplica. La fase A cuenta lo contrario (foso estrecho, ROIC del capital nuevo orgánico por encima de r).
3. *La fase B infravalora su propio aviso.* Compara 248,6 con 308 «antes de reinvertir». Pero 308 (C52) ya va después de la inversión en artículos e inmovilizado propios por encima de su amortización (punto 3: +136,7 de media en 2023–25). El sesgo no es de 59 mm al año: está entre 59 y unos 229.
4. *Página de C55.* La tabla de acciones diluidas (259.077.654, con 23.355.764 por la conversión de las OCEANE) está en la **página 395 del PDF**, cuyo folio impreso es «393» (lo comprobé en el PDF y en el texto). La fase B cita bien «PDF p. 395»; la fase A escribe «PDF p. 393», que es el folio, no la página del PDF. `datos_v63.md` también da «393» como folio. El dato no cambia; cambia la referencia.
5. *Acciones y precio con fechas distintas (aviso A3).* C55 es la media diluida de 2025 y el precio es de noviembre de 2026; en octubre de 2026 el capital quedó en 238.313.588 acciones tras la conversión (comunicado OCEANE). El tratamiento de la OCEANE está pendiente (E6/D3): no lo adopto. Solo lo uso como prueba de robustez del punto 5.

Con estas incoherencias, `una_sola_historia.coherente = false`. Ninguna se resuelve con palabras, y ninguna se resuelve moviendo palancas (punto 3).

## 2. Desviaciones de la gramática

`gramatica.md` no deja G8, G16 ni G17 pendientes: el salto del año 11 queda bajo 5 puntos, el peso del terminal bajo el 75 % y la cuota no se calcula (C24 vacía). Quedan G5 (BUENO) y G7 (NORMAL y BUENO), que la fase B justificó. Las reviso como si fueran de otro:

- **G5 · BUENO 0,135.** El «máximo histórico» de 13,13 % lleva +25,7 de plusvalía por bajas de inmovilizado [URD2025, PDF p. 350]; sin ella, 2025 da 12,6 %. El BUENO sube 0,9 puntos en cinco años. Mecanismo, escala local: Francia gana 22,3 % de EBIT ajustado y Reino Unido 9,7 % [URD2025, PDF p. 344]; Alemania, +450 pb de EBITDA en 2024 [DEU2024, PDF p. 254]. La mejora se la queda Elis en los clientes pequeños [URD2025, PDF p. 50]; en Sanidad, el cliente. La sostengo.
- **G7 · NORMAL y BUENO.** Son 10,7 % y 14,4 % frente a 2 × 4,7 % (C55). C55 mide el capital total, con un fondo de comercio del 42,2 % del activo (C32); el capital tangible rinde ≈23 % antes de impuestos (C24). El ancla orgánica (S2C ≈1,5 en 2024–25) sale de la inversión propia por encima de la amortización propia [URD2025, PDF p. 311, 350, 367]. La sostengo con una reserva, que llevo al punto 7: depende de que el capital orgánico rinda más que el total, y la propia fase B dice que no lo pudo fundamentar del todo. Y recuerdo la incoherencia 2: en el motor ese euro rinde 5,7 %, no 10,7 %.

## 3. ¿Hay que mover palancas? El sesgo del flujo de partida

**Hechos.**
- f = 0,0416668 (Historia C58) se calibra con la reinversión orgánica de la Historia: −47,6 / −70,8 / −125,2 en 2023–25 (capex − D&A + circulante). Lo reproduzco: (NOPAT medio con el tipo de cada año − reinversión media − C52) ÷ ventas medias = 0,0417.
- La D&A de esos años incluye la amortización de los **derechos de uso NIIF 16**: 115,8 / 132,2 / 149,5. También la de los **intangibles de combinaciones**: 85,7 / 84,9 / 85,7 [DEU2024, PDF p. 296; URD2025, PDF p. 350]. Los derechos de uso son inmuebles, vehículos y equipos que Elis **arrienda**. Sus altas (183,9 en 2025) no son caja, y su coste en caja son los pagos del arrendamiento (177,9 con intereses en 2025 [URD2025, PDF p. 327]; principal 148,3 [URD2025, PDF p. 366]). C52 ya los resta (C48, C49). El lino y los artículos que Elis **alquila a sus clientes** son inmovilizado propio, se pagan con capex de caja (635,0 en 2025 [URD2025, PDF p. 367]) y se amortizan en 18 meses a 5 años [URD2025, PDF p. 367]. No los mezclo.
- Quitadas esas dos amortizaciones, la inversión en activos propios por encima de su amortización (con circulante) fue +153,9 / +146,3 / +110,0, de media 136,7 (cálculo propio con las cifras anteriores).
- El motor arranca, a crecimiento cero, en 4.796,8 × (0,131338 × 0,7118 − 0,0416668) = 248,6. Es lo mismo que el FCF histórico más la reinversión histórica, que es negativa: el motor resta los 81 mm de «reinversión negativa» en vez de sumar los 136,7 de inversión propia que ya van dentro de C52.
- La empresa dice que las inversiones de crecimiento son una gran parte del gasto en lino, por el desembolso inicial de cada cliente nuevo, y que el capex industrial cubre crecimiento y reposición de equipos [URD2025, PDF p. 312]. No publica el reparto (extracto §9; `datos_ausentes.json`).

**Interpretación.** El motor A cuenta dos veces dos cosas.
- *Los arrendamientos:* una vez dentro del margen, como amortización del derecho de uso, y otra dentro de f, como pago. Damodaran pide tratarlos como un compromiso, una sola vez: «Operating lease commitments look very much like debt commitments insofar as firms as contractually obligated to make them» (MR p. 31; E8).
- *Las compras:* una vez dentro de f, porque a crecimiento cero el motor supone un capex igual a toda la D&A, incluida la de los intangibles comprados, que el capex nunca repone. Y otra en el S2C, que cobra el crecimiento comprado.

Cobrar las compras en el S2C es **correcto**: C52 no las resta y costaron 138,3 al año en 2021–25 (Historia). Lo que sobra es la amortización de los intangibles comprados que va dentro de f. Hay que distinguir esto del aviso tal como lo formula la fase B.

**Cuánto pesa (fuera de la hoja; mismas palancas, solo cambia f):**

| Lectura de f | f | FCF de partida | MALO / NORMAL / BUENO (€) | Ponderado (€) | Precio de Sí (€) | FCF año 1 NORMAL | Zona a 24,18 € |
|---|---|---|---|---|---|---|---|
| Hoja (C58) | 0,0417 | 248,6 | 5,01 / 7,03 / 9,78 | 7,17 | 6,56 | 75,3 | caro |
| Partida = C52 (todo el exceso propio es reposición) | 0,0293 | 308,0 | 7,92 / 10,68 / 13,85 | 10,76 | 9,95 | 137,5 | caro |
| Sin la amortización NIIF 16 | 0,0126 | 387,9 | 11,83 / 15,59 / 19,33 | 15,59 | 14,52 | 221,0 | caro |
| Sin NIIF 16 ni intangibles comprados (todo el exceso propio es crecimiento) | −0,0061 | 477,8 | 16,23 / 21,12 / 25,49 | 21,02 | 19,65 | 314,9 | caro |

La primera fila corregida es un suelo: a crecimiento cero el capex no superaría el de hoy, que ya financia un orgánico del 3,8 %. La última es un techo: supone que todo el capex propio por encima de su amortización es crecimiento, cuando una parte es reposición [URD2025, PDF p. 312] y el lino se amortiza a coste histórico. Contraste con los hechos: el FCF del año 1 del NORMAL cae entre los 150,4–220,4 observados después de adquisiciones solo entre la segunda y la tercera fila. Leo que el valor defendible está más cerca de 10–15 € que de 6,56 €, sin poder fijarlo.

**¿Es defendible el resultado o es un límite del modelo?** El *nivel* (6,56 / 7,17 / 10,66 €) no es una estimación económica defendible del valor. Es un artefacto de calibración del motor A en una empresa cuya D&A lleva 149,5 de derechos de uso y 85,7 de intangibles comprados (el 23 % de la D&A de 2025). Es un límite del modelo en sentido económico. **No** es L1, L2 ni L3: C52 = 308 > 0, C43 = No aplica, C6 = Ninguno, C62 = Sí. El motor B tampoco lo arregla sin decidir el perímetro de la reinversión, y la fase A ya mostró que con «Caja» sale −530,5. Declarar L3 tiraría una lectura de zona que es robusta. Por eso `limite_del_modelo.aplica = false`, y trato el sesgo como lo que es para la conclusión: decide el objetivo, no la acción.

**¿Revisar palancas?** No. El sesgo está en un dato de la hoja (C58) y en la estructura del motor, no en una palanca mal derivada. Revisé las anclas de la fase B y cuadran:
- margen del NORMAL: 12,6 % subyacente = (630 − 25,7) ÷ 4.796,8;
- S2C orgánico: ≈1,5 (con la inversión propia de caja de 2024–25, 256,3 por cálculo propio, y las ventas orgánicas nuevas que da la fase B, 397,9, me sale 1,55);
- comprado: entre 0,65 en caja y 0,89 al precio;
- crecimiento: 3,0 % orgánico + 1,5 % comprado.

Compensar el sesgo subiendo el margen o el S2C sería mover palancas para cuadrar un número: las palancas dejarían de decir lo que dicen sus hechos. `revisar_palancas = false`.

**Propuesta (no adoptada; para la persona responsable).** Que el ancla f del motor A se calcule sin la amortización de derechos de uso NIIF 16, ya pagados dentro de f, y sin la de intangibles de combinaciones. Y que el reparto del capex propio entre reposición y crecimiento se pida a Relación con Inversores. No es una política ni una decisión registrada.

## 4. Autocomprobación

Diez tendencias en `fase_c.json`. Lo que más cambió mi lectura:
- *Doble castigo.* El motor castiga dos veces el coste de los arrendamientos. No es un riesgo contado dos veces; es un coste.
- *Consistencia.* Me preguntaba si la corrección del sesgo podía sacar a Elis de «caro» y darme una excusa para reabrir la fase A. No puede: el techo del ponderado es 21,02 €.
- *Anclaje en la etapa 1.* Su precio de Sí era ≈15 € (C104 de la etapa 1). Cae dentro de mi rango, pero no lo uso como objetivo: los límites salen de C52 y de las notas de D&A.

## 5. Cubo y conclusión provisionales

Orden de mando:
- **Bloqueo:** ninguno (gramática código 0, B252 y B254 falsos; INCOMPLETO solo por las predicciones del turno 2).
- **Límite del modelo:** no en el sentido de L1–L3 (punto 3).
- **Descalificador:** ninguno (fase A §3).
- **Dato ausente material:** sí, el reparto del capex entre reposición y crecimiento (punto 6). Decide dónde cae el precio de Sí entre ≈9,95 € y ≈19,65 € (cálculo propio). Es material para «esperar con precio objetivo».

**¿«Caro» se sostiene aunque se corrija el sesgo?** Sí.
- Con la corrección más generosa, el ponderado es 21,02 € y el precio de Sí 19,65 €, ambos bajo 24,18 €. El precio de Sí está un 18,7 % por debajo del precio (diferencia ÷ precio).
- Sin adoptar ningún tratamiento de la OCEANE, si dividiera entre las 238,31 m acciones de octubre de 2026 en vez de 259,08 m, el techo subiría a ≈22,85 €. Sigue bajo el precio, y sin restar la deuda extra de la recompra de 2026.
- A r = 0,09 (heredada), el precio pide que los 308 de C52 crezcan ≈3,9 % al año para siempre sin más reinversión: g = (0,09 × 6.264,5 − 308) ÷ (6.264,5 + 308), cálculo propio. Eso está por encima de la tasa sin riesgo del 3,29 % (C57) (CV p. 5; E1).
- Solo juntando la corrección más generosa con una r de 0,08, por debajo de la r mínima de la hoja (0,0885), el ponderado llegaría a 24,79 €. No cambio r.

«I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; HIM).

**Cubo provisional Vigilar · conclusión provisional `esperar`.** Como hay un dato ausente material para el objetivo, el turno 2 cierra sin conclusión: estado propuesto `pendiente_de_datos`, cubo Vigilar, sin acción y sin precio objetivo. La zona `caro` se informa como zona. El otro error, regatear, también está cerca: si se leyera 6,56 € como objetivo, se dejaría pasar un buen negocio por un artefacto. «We left a lot of money on the table through early fretting» (TCI p.79; HIM).

## 6. Datos ausentes (S-19)

Reviso los 21 de `datos_ausentes.json` en `fase_c.json`. Uno es material: el **reparto del capex entre mantenimiento y crecimiento**. Duplica el rango del objetivo (≈9,95 € a ≈19,65 €) y no se acota sin él. Los demás no lo son:
- los ceros NIIF 16 de 2016–2018 no entran en C52, f, C55 ni el S2C, que usan 2019 en adelante;
- los datos de mercado, competidores, bajas, precio y volumen, márgenes por línea, capacidad, cartera, contratos públicos, coste de la deuda y guía de 2026 afectan a celdas de juicio o a la tesis, pero no a la acción ni de forma material al objetivo frente al anterior.

Cada uno lleva su motivo en el JSON. `alguno_material = true`.

## 7. Fundamento material (D10)

Dos hipótesis sin fundamento suficiente:
1. **Análisis!C62 con Historia!C58.** La hipótesis es que el motor A, con este f, reproduce el flujo de partida de Elis. Los hechos lo contradicen: 248,6 frente a 308–478. Base para acotar el FCF de partida: sí. Suelo, C52 = 308, de flujos publicados. Techo, 477,8: C52 más la amortización NIIF 16 y la de intangibles comprados [DEU2024, PDF p. 296; URD2025, PDF p. 350], con la razón de cada lado en el punto 3. El punto exacto lo decide el dato ausente del punto 6.
2. **Palancas!C16, D16, C18, D18.** Dependen de que el capital orgánico rinda más que el total (C18). La fase B no lo pudo fundamentar del todo. Rango: S2C del NORMAL entre 1,0 y 1,2; ROIC del NORMAL entre 0,09 y 0,11. Los límites salen de las compras al 5–7 % después de impuestos (cálculo de la fase B con [URD2025, PDF p. 340, 342]), del ancla orgánica de 2024–25 y del ROIC incremental de C24.

La conclusión provisional no es favorable: `resultado = no_procede` y no hago la comprobación conjunta. Además, el script solo puede mover celdas de A y B, y lo que manda aquí es C58, un dato.

## 8. Lo que más condiciona y qué lo resolvería

**Hipótesis que más condiciona:** el flujo de partida del motor A (Análisis!C62 con Historia!C58): 248,6 frente a 308–478.

**Qué lo resolvería:**
- el reparto del capex de 2023–25 entre reposición y crecimiento, para el lino, los otros artículos de alquiler y el resto del inmovilizado: pregunta a Relación con Inversores, o la nota del URD si la publicara;
- una decisión de la persona responsable sobre cómo trata el ancla f la amortización de derechos de uso NIIF 16 y de intangibles de combinaciones (propuesta, no adoptada).

Sin las dos cosas, el objetivo no es fiable. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## 9. Configuración V6.4

No aplica: no hay `configuracion_economica.json` en el expediente.


# Turno 2 · conclusión, celdas y predicciones

Abreviaturas nuevas: H1-2026 = informe financiero semestral de 2026 (en inglés); Com-RA2025 = comunicado de resultados anuales de 2025 (11-mar-2026); DdR2016 = Document de référence 2016; RD2017 = Registration Document 2017. No hay `comprobacion_conjunta.json` en el expediente (el turno 1 no la pidió: conclusión no favorable), así que `sobrevive = null`. Del turno 1 no cambio nada: ni las incoherencias, ni la revisión de datos ausentes, ni las dos hipótesis sin fundamento, ni la propuesta sobre el ancla f, que sigue siendo una propuesta para la persona responsable y no está adoptada. Tampoco adopto ningún tratamiento de la OCEANE (E6/D3).

## 10. Conclusión

El orden de mando es el de la sección 15:
- **Bloqueo:** ninguno.
- **Límite del modelo:** no en el sentido de L1–L3.
- **Descalificador:** ninguno.
- **Dato ausente material:** sí. El turno 1 declaró material el reparto del capex entre reposición y crecimiento (`alguno_material = true`, S-19), y ese dato manda sobre la zona.

| Campo | Valor |
|---|---|
| `estado_analisis` | `pendiente_de_datos` |
| Cubo | **Vigilar** |
| Acción | ninguna (`null`) |
| Precio objetivo | ninguno (`null`) |
| `fundamento_material.resultado` | `no_procede` |
| Etiqueta de C104 | «fundamento pendiente de datos» |

Escalera de `precio.json` (hecho; convención experimental, D11): precio esc. MALO 5,01 €, precio de Sí 6,56 €, ponderado 7,17 €, precio 24,18 €, zona **caro**. La informo como zona. **No es un precio objetivo.** El precio de Sí de la hoja hereda el sesgo del ancla f (Historia C58). La réplica del motor fuera de la hoja (interpretación, turno 1) lo situaría entre ≈9,95 € y ≈19,65 €, según el reparto del capex que Elis no publica [URD2025, PDF p. 312]. La zona es caro en todo ese rango. El precio del escenario MALO no es un suelo de valor.

C104: «Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de datos: Historia!C58 dentro de Análisis!C62, reparto del capex entre reposición y crecimiento) · zona caro · precio de Sí ≤ 6.56 · precio esc. MALO 5.01 · ponderado 7.17 · fundamento pendiente de datos». No lleva ningún porcentaje. La decisión de cartera es de José Luis (D16).

Insumos para esa decisión:
- precio 24,18 €;
- distancias desde el precio: −72,9 % hasta el precio de Sí y −79,3 % hasta el precio esc. MALO (diferencia ÷ precio, `precio.json`);
- r = 0,09, por encima de la r mínima de 0,0885;
- un dato ausente material, el reparto del capex;
- descalificadores revisados: los nueve de la fase A, ninguno aplica;
- la palanca más influyente del tornado es el margen (±2 pts), como información, no como criterio.

## 11. Tesis (B101)

1. Elis alquila y mantiene lino plano, ropa de trabajo y equipos de higiene a unos 400.000 clientes en 31 países [URD2025, PDF p. 6]. Sus contratos suelen tener un plazo inicial de cuatro años [URD2025, PDF p. 141]. Gana por densidad local: margen EBIT ajustado del 22,3 % en Francia frente al 9,7 % en Reino Unido [URD2025, PDF p. 344].
2. El negocio es estable:
   - orgánico del 2,4–3,8 % en los años normales [RD2017, PDF p. 187; URD2025, PDF p. 307];
   - +3,2 % en el primer semestre de 2026 [H1-2026, PDF p. 5];
   - caja libre positiva todos los años desde 2018, también en 2020 (197,3 mm, Historia).
3. Sobre el capital total rinde un 4,7 % de media en 2021–25 (Historia C55), por debajo de r = 0,09. El fondo de comercio es el 42,2 % del activo (Historia C32): el valor de las compras se lo cobraron los vendedores.
4. La hoja da 7,17 € de ponderado y 6,56 € de precio de Sí. Pero el ancla f cuenta dos veces los arrendamientos NIIF 16 y los intangibles comprados. Fuera de la hoja, el precio de Sí iría de ≈9,95 € a ≈19,65 €, según el reparto del capex.
5. A 24,18 € está cara en todo ese rango. La vigilo, sin precio objetivo hasta tener ese dato.

## 12. Tesis inversa (B102)

La defiendo como la defendería quien quisiera el No.

- **Capex.** Elis invierte cada año el 18–19 % de sus ventas para crecer un 3–4 % orgánico: 18,7 / 18,1 / 19,0 / 19,2 / 18,2 % en 2021–25 [URD2022, PDF p. 247; URD2023, PDF p. 265; DEU2024, PDF p. 257; URD2025, PDF p. 311] y 19,5 % en el primer semestre de 2026 [H1-2026, PDF p. 10]. No dice cuánto de eso es reposición [URD2025, PDF p. 312]. Si casi todo lo es, al accionista le quedan los 308 mm de C52, y el precio de Sí corregido no pasa de ≈9,95 €, menos de la mitad del precio.
- **Rentabilidad.** Sobre el capital total rinde un 4,7 % (Historia C55), con un fondo de comercio del 42,2 % del activo. En 2025 cerró 22 compras más [URD2025, PDF p. 13] sin publicar a qué múltiplo.
- **Recompra y deuda.** En 2026 recompró 17,8 m de acciones a 26,25 € de media [H1-2026, PDF p. 46], por encima de los 24,18 € de hoy. El apalancamiento subió de 1,75x a 2,09x [H1-2026, PDF p. 11].
- **Directivos.** El Presidente del Directorio vendió 75.000 acciones a 24,53 € el 30-ene-2026 [URD2025, PDF p. 442].
- **Clientes y riesgos.**
  - México perdió volumen tras una licitación pública [H1-2026, PDF p. 5].
  - Brasil, el 5,7 % de las ventas [URD2025, PDF p. 346], tiene investigaciones por sobornos y riesgo de veto a contratos públicos [URD2025, PDF p. 373–374].
  - La tasa de bajas no se publica [URD2025, PDF p. 141].
  - Unas 60 lavanderías quedarían en estrés hídrico alto con +4 °C [URD2025, PDF p. 143].
- **Precio.** A 24,18 €, el precio pide que los 308 mm crezcan ≈3,9 % al año para siempre sin más reinversión (cálculo propio, turno 1). Eso está por encima de la tasa sin riesgo (C57). El precio supera incluso el ponderado más generoso fuera de la hoja (≈21,02 €).

**Lo que la tesis inversa no rompe:** la densidad local y la caja de 2020. Por eso el cubo es Vigilar y no No. «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 13. Las otras celdas de la fase C

- **C93 = Sí (mantiene).** La g del NORMAL es 0,02 (C68), por debajo de la tasa sin riesgo (C57) y del orgánico de los años normales. El salto del año 11 es de 0,68 puntos y el peso del terminal 0,66, ambos bajo sus umbrales. El sesgo del ancla f afecta al nivel del flujo, no a que esa g sea sostenible.
- **C103 = No (mantiene).** «Nunca vender» es una propiedad del negocio, no de si se compra. Este negocio no compone solo: rinde un 4,7 % sobre el capital total y depende de comprar bien y de renovar contratos de cuatro años. «if you can buy a few great companies then you can sit on your ass» (PCA pp.85–86; TCI p.105; HIM).
- **B222.** La hipótesis que más condiciona: Análisis!C62 con Historia!C58, es decir, que el motor A reproduce el flujo de partida. Arranca en 248,6 mm frente a C52 = 308. Además, la D&A que calibra f lleva 149,5 de derechos de uso y 85,7 de intangibles de combinaciones [URD2025, PDF p. 350].
- **B223.** Lo que la resolvería, dos cosas:
  1. Una pregunta a Relación con Inversores: de la inversión neta de 2023–25 (874,7 mm en 2025, de ellos lino 594,2, otros artículos 40,8 y otro inmovilizado 255,2 [URD2025, PDF p. 311]), ¿qué parte fue dotación de clientes nuevos y capacidad, y qué parte reposición?
  2. La decisión de la persona responsable sobre el ancla f (propuesta, no adoptada).

## 14. Predicciones (Palancas A38:C40)

Son sobre el negocio, falsables con lo que Elis publica, y todas se comprueban el **2028-03-31**. Esa fecha cae en la ventana de 12–24 meses desde D4 = 2026-11-14. Elis publicó los resultados anuales de 2025 el 11-mar-2026 [Com-RA2025, PDF p. 1]. Cada probabilidad es la de que se cumpla esa predicción si se da el escenario NORMAL.

| # | Predicción | Probabilidad | Fundamento |
|---|---|---|---|
| 1 | Orgánico de 2027 entre el 2,0 % y el 4,5 % | 0,7 | NORMAL: 3,0 % orgánico (Palancas C14 = 0,045 con 1,5 % comprado). Publicado: 2,7 % en 2016 [DdR2016, PDF p. 150], 2,4 % en 2017 [RD2017, PDF p. 187], 3,8 % en 2025 [URD2025, PDF p. 307] y 3,2 % en el primer semestre de 2026, con contratos nuevos en récord y pérdida de volumen en México [H1-2026, PDF p. 5]. 2024 quedó por encima, con 5,2 % [DEU2024, PDF p. 253]. |
| 2 | Margen EBIT ajustado de 2027 entre el 15,5 % y el 16,8 % | 0,7 | NORMAL: margen plano (C66). Publicado: 15,9 / 16,0 / 16,0 % en 2023–25 [DEU2024, PDF p. 291; URD2025, PDF p. 345, 307] y 15,1 % en el primer semestre de 2026, igual que un año antes [H1-2026, PDF p. 5]. La cobertura de electricidad de 2027 (≈63 %) es menor que la de 2026 (93 %) [URD2025, PDF p. 378]. |
| 3 | Inversión neta de 2027 entre el 17,0 % y el 19,5 % de las ventas | 0,75 | Publicado: 18,1–19,2 % en 2021–25 [URD2022, PDF p. 247; URD2023, PDF p. 265; DEU2024, PDF p. 257; URD2025, PDF p. 311]; «20 %» en 2019 [URD2019, PDF p. 150]; 19,5 % en el primer semestre de 2026 [H1-2026, PDF p. 10]. Uso la serie, no la guía de ≈18 %. |

La tercera es la autopsia del dato material. Con el orgánico dentro de la banda de la primera, leo que una inversión por encima del 19,5 % apuntaría a más reposición, y por tanto a la parte baja del rango corregido. «comparing predictions with outcomes» (PCA p.606; AIWTK p.162; HIM).

## 15. Qué me haría cambiar de cubo

- **A Sí:** tres cosas a la vez.
  1. El reparto del capex y una decisión sobre el ancla f, que den un precio de Sí con fundamento.
  2. Un precio de mercado por debajo de ese precio de Sí (zona cumple_regla_k o bajo_malo), sin descalificador nuevo.
  3. Fundamento para Palancas C16 y C18 (retorno del capital orgánico por país o por planta), o una comprobación conjunta superada.
- **A No:** cualquiera de estos hechos.
  - Margen EBIT ajustado bajo el 15 % dos años seguidos sin causa cíclica.
  - Orgánico bajo el 2 % dos años, con pérdidas de contratos como la de México.
  - Una sanción o un veto amplio en Brasil [URD2025, PDF p. 373–374].
  - Recompras repetidas con deuda que lleven el apalancamiento por encima de 2,5x (2,09x en junio de 2026 [H1-2026, PDF p. 11]).
- **A Demasiado difícil:** si Relación con Inversores confirma que no sigue el reparto y ninguna nota permite acotarlo. El precio de Sí quedaría en un rango que se duplica, sin dato que lo cierre. También si los procesos de Brasil crecieran hasta no poder acotar su efecto.

Condiciones de revisión:
- **Al alza:** reparto del capex con la mayor parte como crecimiento (hacia ≈19,65 €), orgánico sostenido por encima del 4 %, margen ajustado por encima del 16,8 %, o una caída del precio de mercado. Ninguna de ellas emite por sí sola un precio objetivo.
- **A la baja:** casi todo el capex como reposición (≈9,95 €), margen ajustado bajo el 15,5 %, orgánico bajo el 2 %, apalancamiento por encima de 2,5x, o Brasil.

## 16. Comparación con la etapa 1

**Cubo:** igual, Watchlist en la v1 y Vigilar en la v2, y por la misma razón: el precio, no el negocio.

**Precio de Sí:**
- La v1 estimaba ≈15 € como el menor entre su escenario malo y tres cuartos de su ponderado. Usaba FCF base 308, r 0,09 y 240,69 m de acciones.
- La v2 usa la escalera k = 3 sobre los tres escenarios del motor A, con 259,08 m de acciones diluidas (Análisis!C55, [URD2025, PDF p. 395], folio impreso 393). Da 6,56 €.

La diferencia grande no es de juicio sino de motor, por el ancla f. El rango corregido fuera de la hoja (≈9,95–19,65 €) contiene los 15 € de la v1, pero no los valida. Hay otra diferencia: la v2 no emite precio objetivo, mientras que la v1 lo daba sin tener el reparto del capex.

**Las cinco celdas heredadas:**
- C93 y C103 se mantienen, con evidencia nueva.
- B101 y B102 se reescriben con la Historia, las notas de D&A y el H1-2026. Quito de la tesis inversa lo que solo constaba en un agregador secundario.
- C104 cambia porque la V6.3 la define de otro modo: sin tamaño de posición y con otra escalera.

**Confianza global: media.** La zona y el cubo son robustos en todo el rango corregido; el objetivo no está determinado. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).
