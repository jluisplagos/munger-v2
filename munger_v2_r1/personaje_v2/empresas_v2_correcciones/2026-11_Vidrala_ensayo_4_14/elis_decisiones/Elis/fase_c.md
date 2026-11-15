# Elis SA · fase C, turno 1 · motor A · plantilla V6.3 · base 31-dic-2025

Millones de euros salvo que diga otra cosa. Base económica 31-dic-2025 (decisión E6 de la persona responsable): 232,48 m acciones en circulación a esa fecha (Análisis C55), la OCEANE 2029 como deuda con su cupón en C48 y ninguna operación de 2026 incorporada, ni en parte. **No es una valoración actualizada a 2026.** El precio (24,18 €) es del 4-nov-2026: en cada comparación con el precio digo que las fechas son distintas. Fuentes como en las fases A y B: URD2025, DEU2024 (en francés; lo cito traducido), URD2023 y anteriores; los informes de 2026 no son apoyo. «Historia C55» es el ROIC medio de cinco años y «Análisis C55», las acciones. Separo tres cosas: **hecho** (está en un documento o lo calcula la hoja), **interpretación** (mi lectura, con su cálculo) y **propuesta o supuesto** (de otro; no lo adopto). Las cifras «fuera de la hoja» salen de una réplica del motor A en Python que reproduce al céntimo B78:D78 (5,58 / 7,82 / 10,89), C83 (7,99) y el precio de Sí (7,30); el script queda en el directorio temporal de la sesión. Son interpretación, no sustituyen a la hoja.

**Supuesto F1 (de la orquestación, no de la persona responsable).** El motor A cuenta dos veces los arrendamientos NIIF 16 y los intangibles adquiridos en el ancla f (hallazgo F1). Mientras la persona responsable no responda rige la opción (a): el motor A queda «no validado para casos con NIIF 16» y **su precio de Sí en Elis no es una conclusión utilizable**. No cambio por ello la elección del motor ni los criterios del personaje.

## 1. Una sola historia

**Lo que dice la hoja (hechos).**
- Precio 24,18 € (C37, 4-nov-2026) frente a acciones de 31-dic-2025.
- Escalera de `precio.json`: precio esc. MALO 5,58 €, precio de Sí 7,30 €, ponderado 7,99 €, BUENO 10,89 €; zona **caro**. El precio de Sí está un 69,8 % por debajo del precio (diferencia ÷ precio); el precio está un 231,1 % por encima del precio de Sí (diferencia ÷ precio de Sí). Regla antigua C156: 5,58 €. Por el supuesto F1, la escalera se lee como zona, no como objetivo.
- Valor sin crecimiento 11,88 €/acción; el crecimiento con la mejora de margen vale −6,00 / −3,64 / −0,41 € en MALO / NORMAL / BUENO.
- FCF del año 1: 139,2 / 75,3 / 88,9; del año 10: 131,5 / 214,5 / 286,8.
- Peso del terminal 0,50 / 0,66 / 0,65 (bajo el 75 %). Salto del año 11: 0,47 / 0,68 / 2,41 puntos (bajo 5).
- DCF inverso no utilizable (B193: «con tus palancas crecer destruye valor»).
- Tornado (información, no criterio): margen ±2 pts mueve el NORMAL ±3,67 €; ROIC ±5 pts, 3,10 €; S2C ±0,3, 1,59 €; tasa ±1 pt, 1,59 €.
- Veredicto A6: DESCARTADA POR FILTRO PABRAI (C13 = No); mi cubo es Vigilar porque el problema es el precio, no el negocio.
- Estado técnico INCOMPLETO por las tres predicciones (A38:A40): son celdas del turno 2.

**Efectos separados de E6 (hechos del cálculo; efectos mecánicos con las fases anteriores fijas, `efecto_decisiones_elis_E6.md`).** Partiendo del precio de Sí anterior (6,55634 €):

| Efecto | Δ precio de Sí |
|---|---|
| Denominador (Análisis C55 = 232,48 m) | +0,75020 € |
| Capitalización (C41) | 0 |
| Pensiones I25:L25 | 0 (el motor A no las resta) |
| Medias exactas C46, C47, C50 (supuesto de la orquestación, precedente E1; no es decisión de la persona responsable para Elis) | −0,00402 € |
| Entradas reexpresadas a 2025 | 0 |
| Todo | 6,55634 → 7,30206 €, igual al precio de Sí de este expediente |

La dilución potencial **no está incorporada** y se declara aparte: −0,14650 € la conversión de la OCEANE; −0,08119 / −0,09721 € las acciones de rendimiento (vivas / al 120 %).

**Incoherencias que encuentro.**

1. *La caja de la hoja no es la de la fase A.* La fase A cuenta «unos 307,9 mm al año como punto de partida (C52), que crecen con el orgánico». La hoja hace caer el FCF del NORMAL a 75,3 en el año 1 y no vuelve a 214,5 hasta el año 10. Hecho de contraste: el FCF al accionista después de adquisiciones fue 215,2 / 150,4 / 220,4 en 2023–25 (Historia: FCF 297,3 / 333,7 / 338,0 menos adquisiciones 82,1 / 183,3 / 117,6; 2025 y 2024 en [URD2025, PDF p. 327]), con un crecimiento parecido al del NORMAL (2025: +3,8 % orgánico [URD2025, PDF p. 307]). El año 1 del NORMAL es la mitad del peor de esos tres años. La causa es el ancla f (punto 3, hallazgo F1), no una palanca.
2. *El semáforo y el motor miden distinto el mismo euro.* G7 lee una rentabilidad marginal del 10,7 % en el NORMAL (S2C 1,2 × 0,125 × 0,712). El motor resta además f × ventas a cada euro nuevo de ventas: (0,125 × 0,7118 − 0,0417) × 1,2 = 5,7 %, por debajo de r = 0,09 (cálculo propio con Historia C52 y C58). Por eso «crecer destruye valor» y el DCF inverso no aplica. La fase A cuenta lo contrario (foso estrecho, ROIC del capital nuevo orgánico por encima de r).
3. *La fase B infravalora su propio aviso.* Compara 248,5 con 307,9 «antes de cobrar ninguna reinversión». Pero C52 ya va después de la inversión en artículos e inmovilizado propios por encima de su amortización (+136,7 de media en 2023–25). El sesgo no es de 59 mm al año: está entre 59,4 y unos 229.
4. *Acciones y precio con fechas distintas (aviso A3).* Análisis C55 son las acciones en circulación a 31-dic-2025 y el precio es de noviembre de 2026. La dilución potencial (23,36 m de la OCEANE; 2,61–3,14 m de acciones de rendimiento [URD2025, PDF p. 360, 380]) no está en el denominador y sesga al alza el valor por acción, en las cifras de arriba. No la compenso con nada.
5. *C48 puede cambiar sin decisión (riesgo declarado por el revisor independiente).* El libro conserva C48 = 108,0 de la etapa 1 (intereses netos 82,93 más 25,07 de intereses de arrendamientos, la definición de la fase A). `fase1_v63.json` reconstruye 82,933, sin los intereses de arrendamientos. Si el libro se regenerara desde cero, C48 bajaría sin decisión: C52 pasaría a 333,0 y el precio de Sí del libro a ≈8,98 € (réplica del motor; ponderado 9,76 €; zona caro). No sería una corrección: dejaría de restar el coste completo de los arrendamientos.
6. *Las celdas de cierre del libro son de la etapa 1.* B101, B102 y C104 aún dicen ≈23 % sobre el capital tangible, recompra de 2026 a ≈26,3 €, 17,6x la caja LTM, «la compraría cerca de 15 €» y un tamaño de posición con «Watchlist». Contradicen la base E6 y D16. Son celdas del turno 2, que las reescribe.
7. *Cita incompleta en la fase B (observación del revisor independiente de las entradas).* En Palancas!C14, el rango orgánico de 2016–19 «2,4–3,3 %» solo cita el URD 2019, que respalda el 3,3 % de 2019 [URD2019, PDF p. 145]. El 2,4 % de 2017 está en [RD2017, PDF p. 187], que la fase B cita en el MALO pero no ahí. Lo comprobé en los dos textos: el dato es correcto y la palanca (0,045) no cambia. No pido revisar palancas; es una referencia que falta, y en mis textos la pongo completa.

La incoherencia de página de C55 del expediente anterior desaparece: la fase A cita ahora la página 395 del PDF para la media diluida y la 394 para las acciones en circulación. Con las siete restantes, `una_sola_historia.coherente = false`. Ninguna se resuelve con palabras, y ninguna moviendo palancas (punto 3).

## 2. Desviaciones de la gramática

`gramatica.md` no deja G8, G16 ni G17 pendientes: el salto del año 11 queda bajo 5 puntos, el peso del terminal bajo el 75 % y la cuota no se calcula (C24 de Palancas vacía). Quedan G5 (BUENO) y G7 (NORMAL y BUENO), que la fase B justificó. Las reviso como si fueran de otro:

- **G5 · BUENO 0,135.** El «máximo histórico» de 13,13 % lleva +25,7 de plusvalía por bajas de inmovilizado [URD2025, PDF p. 350]; sin ella, 2025 da 12,6 %. El BUENO sube 0,9 puntos en cinco años. Mecanismo, escala local: Francia gana 22,3 % de EBIT ajustado y Reino Unido 9,7 % [URD2025, PDF p. 344]; Alemania, +450 pb de EBITDA en 2024 [DEU2024, PDF p. 254]. La mejora se la queda Elis en los clientes pequeños [URD2025, PDF p. 50]; en Sanidad, el cliente. La sostengo.
- **G7 · NORMAL 10,7 %** frente a 2 × 4,7 % (Historia C55). Historia C55 mide el capital total, con un fondo de comercio del 42,2 % del activo (C32). El ROCE publicado, que también lleva el goodwill posterior a la LBO, da 14,7 % antes de impuestos [URD2025, PDF p. 315], ≈10,5 % después (cálculo de la fase B). El ancla orgánica (S2C ≈1,5 en 2024–25: 397,9 de ventas orgánicas nuevas por 258,2 de inversión propia neta, 1,54) sale de [URD2025, PDF p. 311, 350, 367]. La sostengo con una reserva, que llevo al punto 7: depende de que el capital orgánico rinda más que el total. Y recuerdo la incoherencia 2: en el motor ese euro rinde 5,7 %, no 10,7 %.
- **G7 · BUENO 14,4 %.** Aquí cambia lo que sé. La evidencia de C24 reexpresada a 2025 (ROCE 9,7 % sobre capital empleado bruto) ya no trae el ≈23 % del capital tangible con el que el expediente anterior lo contrastaba. El 14,4 % queda por encima del ≈10,5 % del ROCE publicado y descansa solo en llenar las plantas de 2025 [URD2025, PDF p. 19] con poco capital nuevo. Además, el S2C de 3,1 de 2021–25 en que se apoya es el que la propia fase B descarta para el NORMAL por la reapertura y el precio de 2022–23. Lo sostengo con confianza baja porque calculé qué pasa si está mal (punto 3).

## 3. ¿Hay que mover palancas? El sesgo del flujo de partida

**Hechos.**
- f = 0,0416815 (Historia C58) se calibra con la reinversión orgánica de la Historia: −47,6 / −70,8 / −125,2 en 2023–25 (capex − D&A + circulante). Lo reproduzco: (NOPAT medio con el tipo de cada año 416,8 − reinversión media −81,2 − C52 307,9) ÷ ventas medias 4.560,0 = 0,0417.
- La D&A de esos años incluye la amortización de los **derechos de uso NIIF 16** (115,8 / 132,2 / 149,5) y la de los **intangibles de combinaciones** (85,7 / 84,9 / 85,7) [DEU2024, PDF p. 296; URD2025, PDF p. 350]. Los derechos de uso son inmuebles, vehículos y equipos que Elis **arrienda**. Sus altas (183,9 en 2025) no son caja, y su coste en caja son los pagos del arrendamiento (177,9 con intereses en 2025 [URD2025, PDF p. 327]; principal 148,3 [URD2025, PDF p. 366]). C52 ya los resta (C48, C49). El lino y los artículos que Elis **alquila a sus clientes** son inmovilizado propio, se pagan con capex de caja (635,0 en 2025 [URD2025, PDF p. 367]) y se amortizan en 18 meses a 5 años [URD2025, PDF p. 367]. No los mezclo.
- Quitadas esas dos amortizaciones, la inversión en activos propios por encima de su amortización (con circulante) fue +153,9 / +146,3 / +110,0, de media 136,7 (cálculo propio).
- El motor arranca, a crecimiento cero, en 4.796,8 × (0,131338 × 0,7118 − 0,0416815) = 248,5: resta los 81 mm de «reinversión negativa» en vez de sumar los 136,7 de inversión propia que ya van dentro de C52.
- La empresa dice que las inversiones de crecimiento son una gran parte del gasto en lino y que el capex industrial cubre crecimiento y reposición de equipos [URD2025, PDF p. 312]. No publica el reparto (extracto §9; `datos_ausentes.json`).

**Interpretación (es el hallazgo F1).** El motor A cuenta dos veces dos cosas.
- *Los arrendamientos:* una vez dentro del margen, como amortización del derecho de uso, y otra dentro de f, como pago. Damodaran pide tratarlos como un compromiso, una sola vez: «Operating lease commitments look very much like debt commitments insofar as firms as contractually obligated to make them» (MR p. 31; E8).
- *Las compras:* una vez dentro de f, porque a crecimiento cero el motor supone un capex igual a toda la D&A, incluida la de los intangibles comprados, que el capex nunca repone. Y otra en el S2C, que cobra el crecimiento comprado, lo que es **correcto** porque C52 no las resta.

**Cuánto pesa (fuera de la hoja; mismas palancas, 232,48 m acciones, solo cambia f):**

| Lectura de f | f | FCF de partida | MALO / NORMAL / BUENO (€) | Ponderado (€) | Precio de Sí (€) | FCF año 1 NORMAL | Zona a 24,18 € (4-nov-2026) |
|---|---|---|---|---|---|---|---|
| Hoja (C58) | 0,0417 | 248,5 | 5,58 / 7,82 / 10,89 | 7,99 | 7,30 | 75,3 | caro |
| Partida = C52 (todo el exceso propio es reposición) | 0,0293 | 307,9 | 8,82 / 11,90 / 15,43 | 11,99 | 11,08 | 137,4 | caro |
| Sin la amortización NIIF 16 | 0,0126 | 387,9 | 13,18 / 17,37 / 21,53 | 17,37 | 16,17 | 220,9 | caro |
| Sin NIIF 16 ni intangibles comprados (todo el exceso propio es crecimiento) | −0,0061 | 477,7 | 18,08 / 23,53 / 28,40 | 23,42 | 21,89 | 314,8 | caro |

La primera fila corregida es un suelo: a crecimiento cero el capex no superaría el de hoy, que ya financia un orgánico del 3,8 %. La última es un techo: supone que todo el capex propio por encima de su amortización es crecimiento, cuando una parte es reposición [URD2025, PDF p. 312]. Contraste con los hechos: el FCF del año 1 del NORMAL cae entre los 150,4–220,4 observados después de adquisiciones solo entre la segunda y la tercera fila. Leo que el valor defendible está más cerca de 11–16 € que de 7,30 €, sin poder fijarlo.

Al otro lado va la dilución potencial: en el techo, la conversión de la OCEANE (23,36 m acciones más, sin su cupón de 8,55 en C48) bajaría el ponderado a 21,83 € y el precio de Sí a 20,41 €; las acciones de rendimiento al 120 %, a 23,10 € y 21,60 €. No la incorporo (E6).

**¿Es defendible el resultado o es un límite del modelo?** El *nivel* (7,30 / 7,99 / 11,88 €) no es una estimación económica defendible del valor: es el artefacto F1, en una empresa cuya D&A lleva 149,5 de derechos de uso y 85,7 de intangibles comprados (el 23 % de la D&A de 2025). Por el supuesto (a) de F1, el precio de Sí del motor A no es una conclusión utilizable. **No** es L1, L2 ni L3: C52 = 307,9 > 0, C43 = No aplica, C6 = Ninguno, C62 = Sí. El motor B tampoco lo arregla sin decidir el perímetro de la reinversión, y cambiar el motor no es mío: la fase A eligió A por la financiación y el supuesto F1 no cambia esa elección. `limite_del_modelo.aplica = false`, y trato el sesgo como lo que es para la conclusión: decide el objetivo, no la acción.

**¿Revisar palancas?** No. El sesgo está en un dato de la hoja (C58) y en la estructura del motor, no en una palanca mal derivada. Revisé las anclas de la fase B y cuadran: margen del NORMAL 12,6 % subyacente = (630 − 25,7) ÷ 4.796,8; S2C orgánico ≈1,5 (1,54); comprado entre 0,65 en caja y 0,89 al precio; crecimiento 3,0 % orgánico + 1,5 % comprado. Compensar el sesgo subiendo el margen o el S2C sería mover palancas para cuadrar un número.

**Las dos palancas dudosas del BUENO (D16 = 1,5 y D18 = 0,12).** Perdieron el contraste del capital tangible, pero no están mal derivadas: la aritmética y el perímetro cuadran y lo que falta es fundamento. Calculo igualmente lo que exige la regla para dejarlas:

| Cambio | Precio de Sí hoja | Δ | Precio de Sí techo | Δ | Zona / cubo |
|---|---|---|---|---|---|
| D18 = 0,10 | 7,19 € | −1,5 % | — | — | caro / Vigilar |
| D16 = 1,2 | 7,13 € | −2,3 % | — | — | caro / Vigilar |
| D16 = 1,2 y D18 = 0,10 | 7,01 € | −4,0 % | 21,60 € | −1,3 % | caro / Vigilar |

Corregirlas no cambia ni el cubo ni la zona y mueve el precio de Sí menos de un 5 %. La rentabilidad marginal del BUENO seguiría sobre 2 × Historia C55 incluso con D16 = 1,2 (11,5 %). `revisar_palancas = false`; D16 y D18 quedan en la lista de hipótesis sin fundamento (punto 7).

**Propuesta y supuesto (no adoptados por mí).** F1 está registrado con tres opciones; la orquestación aplica la (a) mientras no responda la persona responsable, y deja pendiente la (b): calcular el ancla f sin la amortización de derechos de uso NIIF 16, ya pagados dentro de f, y sin la de intangibles de combinaciones. El reparto del capex propio entre reposición y crecimiento habría que pedirlo a Relación con Inversores.

## 4. Autocomprobación

Diez tendencias en `fase_c.json`. Lo que más cambió mi lectura:
- *Consistencia.* La corrección del sesgo no saca a Elis de «caro» a r = 0,09, pero la holgura ya no es amplia: el techo del ponderado es 23,42 € frente a 24,18 € (fechas distintas), 23,97 € con la r mínima.
- *Optimismo del BUENO.* D16 y D18 perdieron su contraste; las dejo porque su efecto es menor del 5 % y no cambia la zona, y lo digo.
- *Doble castigo.* El motor castiga dos veces el coste de los arrendamientos (F1). No es un riesgo contado dos veces; es un coste. La dilución no incorporada empuja al otro lado.

## 5. Cubo y conclusión provisionales

Orden de mando:
- **Bloqueo:** ninguno (gramática código 0, B252 y B254 falsos; INCOMPLETO solo por las predicciones del turno 2).
- **Límite del modelo:** no en el sentido de L1–L3 (punto 3). Rige el supuesto F1: el precio de Sí del motor A no es utilizable como conclusión.
- **Descalificador:** ninguno (fase A §3).
- **Dato ausente material:** sí, el reparto del capex entre reposición y crecimiento (punto 6). Decide dónde cae el precio de Sí entre ≈11,08 € y ≈21,89 € (cálculo propio). Es material para «esperar con precio objetivo».

**¿«Caro» se sostiene aunque se corrija el sesgo?** Sí, pero con menos holgura que en el expediente anterior. Todas las comparaciones son entre un precio del 4-nov-2026 y una base del 31-dic-2025.
- Con la corrección más generosa, el ponderado es 23,42 € y el precio de Sí 21,89 €, ambos bajo 24,18 €. El precio está un 3,2 % por encima de ese ponderado (diferencia ÷ ponderado); el precio de Sí está un 9,5 % por debajo del precio (diferencia ÷ precio).
- Con la r mínima de la hoja (0,0885), el ponderado del techo sería 23,97 €: aún bajo el precio, por 0,21 €.
- Solo juntando la corrección más generosa con r = 0,08, por debajo de la r mínima, el precio de Sí llegaría a 25,65 € (cumple_regla_k). No cambio r.
- La dilución potencial que E6 deja fuera bajaría el techo (21,83 € de ponderado con la conversión de la OCEANE).
- A r = 0,09, el precio pide que los 307,9 de C52 crezcan ≈3,3 % al año para siempre sin más reinversión: g = (0,09 × 5.621,3 − 307,9) ÷ (5.621,3 + 307,9), cálculo propio. Apenas por encima de la tasa sin riesgo del 3,29 % (C57) (CV p. 5; E1).

«I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; HIM).

**Cubo provisional Vigilar · conclusión provisional `esperar`.** Como hay un dato ausente material para el objetivo, el turno 2 cierra sin conclusión: estado propuesto `pendiente_de_datos`, cubo Vigilar, sin acción y sin precio objetivo. La zona `caro` se informa como zona. El precio de Sí del motor A (7,30 €) no se presenta como objetivo ni como conclusión utilizable (supuesto F1), y el rango corregido tampoco: es interpretación de una réplica. El otro error, regatear, también está cerca: si se leyera 7,30 € como objetivo, se dejaría pasar un buen negocio por un artefacto. «We left a lot of money on the table through early fretting» (TCI p.79; HIM).

## 6. Datos ausentes (S-19)

Reviso los 21 de `datos_ausentes.json` en `fase_c.json`. Uno es material: el **reparto del capex entre mantenimiento y crecimiento**. Duplica el rango del objetivo (≈11,08 € a ≈21,89 €) y no se acota sin él. Los demás no lo son:
- los ceros NIIF 16 de 2016–2018 no entran en C52, f, Historia C55 ni el S2C, que usan 2019 en adelante;
- el cumplimiento de la guía 2026 no es evaluable en la base 31-dic-2025 y ninguna palanca depende de él;
- los datos de mercado, competidores, bajas, precio y volumen, márgenes por línea, capacidad, cartera, contratos públicos y coste de la deuda afectan a celdas de juicio o a la tesis, pero no a la acción ni de forma material al objetivo frente al anterior.

Cada uno lleva su motivo en el JSON. `alguno_material = true`.

## 7. Fundamento material (D10)

Dos hipótesis sin fundamento suficiente:
1. **Análisis!C62 con Historia!C58 (hallazgo F1).** La hipótesis es que el motor A, con este f, reproduce el flujo de partida de Elis. Los hechos lo contradicen: 248,5 frente a 307,9–477,7. Hay base para acotar el FCF de partida. Suelo, C52 = 307,9, de flujos publicados. Techo, 477,7: el arranque del motor más la amortización NIIF 16 y la de intangibles comprados [DEU2024, PDF p. 296; URD2025, PDF p. 350]. La razón de cada lado está en el punto 3. El punto exacto lo decide el dato ausente del punto 6.
2. **Palancas!C16, D16, C18, D18.** Dependen de que el capital orgánico rinda más que el total (C18). La fase B no lo pudo fundamentar del todo, y con la base E6 perdió el contraste del capital tangible. Ahora solo hay hechos para los suelos: S2C del NORMAL 1,0 y ROIC del NORMAL 0,09, con el ROCE publicado después de impuestos (≈10,5 % [URD2025, PDF p. 315]) y las compras al 5–7 % [URD2025, PDF p. 340, 342]. Ningún hecho publicado acota los techos. Por eso `hay_base = false`: haría falta el rendimiento del capital orgánico sin goodwill, por país o por planta. Su efecto está acotado (punto 3) y no cambia la zona.

La conclusión provisional no es favorable: `resultado = no_procede` y no hago la comprobación conjunta. Además, el script solo puede mover celdas de A y B, y lo que manda aquí es C58, un dato.

## 8. Lo que más condiciona y qué lo resolvería

**Hipótesis que más condiciona:** el flujo de partida del motor A (Análisis!C62 con Historia!C58): 248,5 frente a 307,9–477,7.

**Qué lo resolvería:**
- el reparto del capex de 2023–25 entre reposición y crecimiento, para el lino, los otros artículos de alquiler y el resto del inmovilizado: pregunta a Relación con Inversores, o la nota del URD si la publicara;
- una decisión de la persona responsable sobre F1: la corrección (b) de la definición de f (pendiente; hoy rige el supuesto (a) de la orquestación).

Sin las dos cosas, el objetivo no es fiable. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

**Limitaciones que dejo dichas:** el riesgo de C48 (incoherencia 5) puede mover el precio de Sí del libro a ≈8,98 € sin decisión si el libro se regenera; las medias exactas de C46, C47 y C50 son un supuesto de la orquestación con precedente E1, no una decisión para Elis (−0,00402 €); la dilución potencial está fuera de la base.

## 9. Configuración V6.4

No aplica: no hay `configuracion_economica.json` en el expediente.

# Turno 2 · conclusión, celdas y predicciones

No hay `comprobacion_conjunta.json` en el expediente (el turno 1 no la pidió: conclusión no favorable), así que `sobrevive = null`. Del turno 1 no cambio nada: ni las incoherencias, ni la revisión de datos ausentes, ni las dos hipótesis sin fundamento. Mantengo el supuesto F1 de la orquestación: el precio de Sí del motor A no se presenta como objetivo ni como conclusión utilizable. Toda comparación con el precio (24,18 €, 4-nov-2026) es contra una base del 31-dic-2025: fechas distintas. Ninguna operación de 2026 entra en la base (E6).

## 10. Conclusión

El orden de mando es el de la sección 15:
- **Bloqueo:** ninguno.
- **Límite del modelo:** no en el sentido de L1–L3; rige el supuesto F1.
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

Escalera de `precio.json` (hecho; convención experimental, D11): precio esc. MALO 5,58 €, precio de Sí 7,30 €, ponderado 7,99 €, precio 24,18 € (4-nov-2026), zona **caro**. La informo como zona. **No es un precio objetivo** ni una conclusión utilizable: hereda el ancla f del motor A (hallazgo F1). La réplica del motor fuera de la hoja (interpretación, turno 1) lo situaría entre ≈11,08 € y ≈21,89 €, según el reparto del capex que Elis no publica [URD2025, PDF p. 312]. La zona es caro en todo ese rango, con poca holgura en el techo. El precio del escenario MALO no es un suelo de valor.

C104: «Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de datos: Historia!C58 dentro de Análisis!C62, reparto del capex entre reposición y crecimiento; motor A no validado con NIIF 16, F1) · zona caro · precio de Sí ≤ 7.30 · precio esc. MALO 5.58 · ponderado 7.99 · fundamento pendiente de datos». No lleva ningún porcentaje. La decisión de cartera es de José Luis (D16).

Insumos para esa decisión:
- precio 24,18 € (4-nov-2026; base 31-dic-2025);
- distancias desde el precio: −69,8 % hasta el precio de Sí y −76,9 % hasta el precio esc. MALO (diferencia ÷ precio, `precio.json`);
- r = 0,09, por encima de la r mínima de 0,0885;
- un dato ausente material, el reparto del capex;
- la dilución potencial no incorporada (−0,15 € la OCEANE; −0,08 / −0,10 € las acciones de rendimiento, sobre el precio de Sí del libro);
- descalificadores revisados: los nueve de la fase A, ninguno aplica;
- la palanca más influyente del tornado es el margen (±2 pts), como información, no como criterio.

## 11. Tesis (B101)

1. Elis alquila y mantiene lino plano, ropa de trabajo y equipos de higiene a unos 400.000 clientes en 31 países [URD2025, PDF p. 6]. Sus contratos suelen tener un plazo inicial de cuatro años [URD2025, PDF p. 141]. Gana por densidad local: margen EBIT ajustado del 22,3 % en Francia frente al 9,7 % en Reino Unido [URD2025, PDF p. 344].
2. El negocio es estable:
   - orgánico del 2,4–3,8 % en los años normales [RD2017, PDF p. 187; URD2025, PDF p. 307];
   - margen EBIT ajustado plano en 15,85–16,02 % en 2023–25 [DEU2024, PDF p. 291; URD2025, PDF p. 345];
   - caja libre positiva todos los años desde 2018, también en 2020 (197,3 mm, Historia).
3. Sobre el capital total rinde un 4,7 % de media en 2021–25 (Historia C55), por debajo de r = 0,09. El fondo de comercio es el 42,2 % del activo (Historia C32): el valor de las compras se lo cobraron los vendedores.
4. La hoja da 7,99 € de ponderado y 7,30 € de precio de Sí, pero el ancla f cuenta dos veces los arrendamientos NIIF 16 y los intangibles comprados: ese precio no es utilizable (F1). Fuera de la hoja iría de ≈11,08 € a ≈21,89 €, según el reparto del capex.
5. A 24,18 € (4-nov-2026, fecha distinta de la base) está cara en todo ese rango. La vigilo, sin precio objetivo hasta tener ese dato.

## 12. Tesis inversa (B102)

La defiendo como la defendería quien quisiera el No.

- **Capex.** Elis invierte cada año el 18–19 % de sus ventas para crecer un 3–4 % orgánico: 18,7 / 18,1 / 19,0 / 19,2 / 18,2 % en 2021–25 [URD2022, PDF p. 247; URD2023, PDF p. 265; DEU2024, PDF p. 257; URD2025, PDF p. 311]. No dice cuánto de eso es reposición [URD2025, PDF p. 312]. Si casi todo lo es, al accionista le quedan los 307,9 mm de C52, y el precio de Sí corregido no pasa de ≈11,08 €, menos de la mitad del precio.
- **Rentabilidad.** Sobre el capital total rinde un 4,7 % (Historia C55), con un fondo de comercio del 42,2 % del activo. En 2025 cerró 22 compras más [URD2025, PDF p. 13] sin publicar a qué múltiplo.
- **Deuda y recompra.** La caja no cubre la deuda a un año (C34 = No: 398,1 frente a 800,5 [URD2025, PDF p. 383]). El URD 2025 anuncia una recompra de hasta 500 mm para 2026, financiada en parte con un bono de 600 mm al 3,875 % [URD2025, PDF p. 315, 402]; su ejecución es posterior a la base y no la incorporo.
- **Directivos.** El Presidente del Directorio vendió 75.000 acciones a 24,53 € el 30-ene-2026 [URD2025, PDF p. 442].
- **Clientes y riesgos.**
  - La disciplina de precios costó contratos en Reino Unido (2023) y Alemania (2025) [URD2023, PDF p. 261; URD2025, PDF p. 141].
  - Brasil, el 5,7 % de las ventas [URD2025, PDF p. 346], tiene investigaciones por sobornos y riesgo de veto a contratos públicos [URD2025, PDF p. 373–374].
  - La tasa de bajas no se publica [URD2025, PDF p. 141].
  - Unas 60 lavanderías quedarían en estrés hídrico alto con +4 °C [URD2025, PDF p. 143].
- **Precio.** A 24,18 € (4-nov-2026, sobre acciones de 31-dic-2025), el precio pide que los 307,9 mm crezcan ≈3,3 % al año para siempre sin más reinversión (cálculo propio, turno 1), por encima de la tasa sin riesgo (C57). Supera el ponderado más generoso fuera de la hoja (≈23,42 €), y la base no descuenta la dilución potencial de la OCEANE y de las acciones de rendimiento [URD2025, PDF p. 360, 380].

**Lo que la tesis inversa no rompe:** la densidad local y la caja de 2020. Por eso el cubo es Vigilar y no No. «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 13. Las otras celdas de la fase C

- **C93 = Sí (mantiene).** La g del NORMAL es 0,02 (C68), por debajo de la tasa sin riesgo (C57) y del orgánico de los años normales. El salto del año 11 es de 0,68 puntos y el peso del terminal 0,66, ambos bajo sus umbrales. El sesgo del ancla f afecta al nivel del flujo, no a que esa g sea sostenible.
- **C103 = No (mantiene).** «Nunca vender» es una propiedad del negocio, no de si se compra. Este negocio no compone solo: rinde un 4,7 % sobre el capital total y depende de comprar bien y de renovar contratos de cuatro años. «if you can buy a few great companies then you can sit on your ass» (PCA pp.85–86; TCI p.105; HIM).
- **B222.** Análisis!C62 con Historia!C58: que el motor A reproduce el flujo de partida (hallazgo F1). Arranca en 248,5 mm frente a C52 = 307,9; la D&A que calibra f lleva 149,5 de derechos de uso y 85,7 de intangibles de combinaciones [URD2025, PDF p. 350].
- **B223.** Lo que la resolvería, dos cosas:
  1. Una pregunta a Relación con Inversores: de la inversión neta de 2023–25 (874,7 mm en 2025, de ellos lino 594,2, otros artículos 40,8 y otro inmovilizado 255,2 [URD2025, PDF p. 311]), ¿qué parte fue dotación de clientes nuevos y capacidad, y qué parte reposición?
  2. La decisión de la persona responsable sobre F1: la corrección (b) del ancla f (pendiente; hoy rige el supuesto (a)).

## 14. Predicciones (Palancas A38:C40)

Son sobre el negocio, falsables con lo que Elis publica, y todas se comprueban el **2028-03-31**, dentro de la ventana de 12–24 meses desde D4 = 2026-11-14. Las cuentas consolidadas de 2025 se aprobaron en el Directorio del 10-mar-2026 [URD2025, PDF p. 330]. Cada probabilidad es la de que se cumpla esa predicción si se da el escenario NORMAL. Solo uso hechos hasta la base de 2025.

| # | Predicción | Probabilidad | Fundamento |
|---|---|---|---|
| 1 | Orgánico de 2027 entre el 2,0 % y el 4,5 % | 0,7 | NORMAL: 3,0 % orgánico (Palancas C14 = 0,045 con 1,5 % comprado). Publicado: 2,7 % en 2016 [DdR2016, PDF p. 150], 2,4 % en 2017 [RD2017, PDF p. 187], 3,3 % en 2019 [URD2019, PDF p. 145], 3,8 % en 2025 [URD2025, PDF p. 307]. 2024 quedó por encima, con 5,2 % [DEU2024, PDF p. 253]. |
| 2 | Margen EBIT ajustado de 2027 entre el 15,5 % y el 16,8 % | 0,7 | NORMAL: margen plano (C66). Publicado: 15,85 / 16,02 / 15,98 % en 2023–25 [DEU2024, PDF p. 291; URD2025, PDF p. 345]. La cobertura de electricidad de 2027 (≈63 %) es menor que la de 2026 (93 %) [URD2025, PDF p. 378]. |
| 3 | Inversión neta de 2027 entre el 17,0 % y el 19,5 % de las ventas | 0,75 | Publicado: 18,1–19,2 % en 2021–25 [URD2022, PDF p. 247; URD2023, PDF p. 265; DEU2024, PDF p. 257; URD2025, PDF p. 311]; «20 %» en 2019 [URD2019, PDF p. 150]. |

La tercera es la autopsia del dato material. Con el orgánico dentro de la banda de la primera, leo que una inversión por encima del 19,5 % apuntaría a más reposición, y por tanto a la parte baja del rango corregido. «comparing predictions with outcomes» (PCA p.606; AIWTK p.162; HIM).

## 15. Qué me haría cambiar de cubo

- **A Sí:** tres cosas a la vez.
  1. El reparto del capex y una decisión sobre F1, que den un precio de Sí con fundamento.
  2. Un precio de mercado por debajo de ese precio de Sí (zona cumple_regla_k o bajo_malo), comparado en la misma fecha que la base o con la base actualizada, sin descalificador nuevo.
  3. Fundamento para Palancas C16 y C18 (retorno del capital orgánico por país o por planta), o una comprobación conjunta superada.
- **A No:** cualquiera de estos hechos.
  - Margen EBIT ajustado bajo el 15 % dos años seguidos sin causa cíclica.
  - Orgánico bajo el 2 % dos años, con pérdidas de contratos como las de Reino Unido y Alemania.
  - Una sanción o un veto amplio en Brasil [URD2025, PDF p. 373–374].
  - Recompras repetidas con deuda que lleven el apalancamiento por encima de 2,5x (1,75x a 31-dic-2025 [URD2025, PDF p. 314]).
- **A Demasiado difícil:** si Relación con Inversores confirma que no sigue el reparto y ninguna nota permite acotarlo. El precio de Sí quedaría en un rango que se duplica, sin dato que lo cierre. También si los procesos de Brasil crecieran hasta no poder acotar su efecto.

Condiciones de revisión:
- **Al alza:** reparto del capex con la mayor parte como crecimiento (hacia ≈21,89 €), la corrección (b) de F1, orgánico sostenido por encima del 4 %, margen ajustado por encima del 16,8 %, o una caída del precio de mercado. Ninguna de ellas emite por sí sola un precio objetivo.
- **A la baja:** casi todo el capex como reposición (≈11,08 €), margen ajustado bajo el 15,5 %, orgánico bajo el 2 %, apalancamiento por encima de 2,5x, Brasil, o la dilución potencial incorporada a la base.

## 16. Comparación con la etapa 1

**Cubo:** igual, Watchlist en la v1 y Vigilar en la v2, y por la misma razón: el precio, no el negocio.

**Precio de Sí:**
- La v1 estimaba ≈15 € como el menor entre su escenario malo y tres cuartos de su ponderado. Usaba FCF base 308, r 0,09 y 240,69 m de acciones.
- La v2 usa la escalera k = 3 sobre los tres escenarios del motor A, con 232,48 m acciones en circulación a 31-dic-2025 (Análisis!C55 [URD2025, PDF p. 394], base E6). Da 7,30 €.

La diferencia grande no es de juicio sino de motor, por el ancla f (F1). El rango corregido fuera de la hoja (≈11,08–21,89 €) contiene los 15 € de la v1, pero no los valida. La v2 no emite precio objetivo, mientras que la v1 lo daba sin tener el reparto del capex.

**Las cinco celdas heredadas:**
- C93 y C103 se mantienen, con evidencia nueva.
- B101 y B102 se reescriben con la Historia, las notas de D&A y la base 31-dic-2025. Quito el ≈23 % del capital tangible, todo lo de 2026 y lo que solo constaba en un agregador secundario.
- C104 cambia porque la V6.3 la define de otro modo: sin tamaño de posición y con otra escalera.

**Confianza global: media.** La zona y el cubo se sostienen en todo el rango corregido, con poca holgura en el techo; el objetivo no está determinado. «Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## Cambios frente al expediente anterior (elis_motor_A)

- Encabezado: base 31-dic-2025 (decisión E6), no es una valoración actualizada a 2026, precio del 4-nov-2026 con fechas distintas declaradas en cada comparación; los informes de 2026 (H1-2026, comunicado de la OCEANE) dejan de ser fuente; «Historia C55» (ROIC) se separa de «Análisis C55» (acciones).
- Supuesto F1 añadido en el encabezado, en `lo_que_dice_la_hoja.motor_A_F1`, en el punto 3, en `limite_del_modelo`, en la conclusión, en C62 de `celdas_corregidas` y en «qué lo resolvería»: el precio de Sí del motor A no es una conclusión utilizable; la elección del motor y los criterios no cambian. La antigua «propuesta» sobre el ancla f pasa a ser la opción (b) pendiente de F1.
- Escalera y hoja: precio de Sí 6,56 → 7,30 €, ponderado 7,17 → 7,99 €, precio esc. MALO 5,01 → 5,58 €, BUENO 9,78 → 10,89 €, distancias 72,9 % → 69,8 % (÷ precio) y 268,8 % → 231,1 % (÷ precio de Sí), valor sin crecimiento 10,66 → 11,88 €, valor del crecimiento y tornado recalculados; f 0,0416668 → 0,0416815, arranque 248,6 → 248,5, C52 308 → 307,9.
- Nuevo bloque `efectos_separados_E6` con los efectos mecánicos (+0,75020 / 0 / 0 / −0,00402 / 0; todo 7,30206 €) y la dilución potencial no incorporada (−0,14650; −0,08119 / −0,09721 €).
- Réplica del motor rehecha con 232,48 m acciones: rango corregido del precio de Sí 9,95–19,65 → 11,08–21,89 €; ponderado 10,76–21,02 → 11,99–23,42 €; partida 308,0–477,8 → 307,9–477,7.
- Robustez de la zona: se retira la prueba con 238,31 m acciones de octubre de 2026 (posterior a la base); se añaden el techo con la r mínima (23,97 €), el techo con r = 0,08 (cumple_regla_k, no aplicado) y la dilución sobre el techo; la holgura de «caro» en el techo pasa a ser pequeña (3,2 % sobre el ponderado).
- DCF inverso propio: g implícito ≈3,9 % → ≈3,3 % con 5.621,3 mm de capitalización (antes 6.264,5), apenas sobre C57.
- Incoherencia 4 anterior (página de C55) retirada: la fase A ya cita la página 395 del PDF.
- Incoherencia 5 anterior (C55 media diluida y conversión de 2026; tratamiento pendiente E6/D3) sustituida por las fechas distintas y la dilución potencial no incorporada.
- Incoherencias nuevas: el riesgo de C48 (108,0 en el libro frente a 82,933 en `fase1_v63.json`; ≈8,98 € si se regenerara), las celdas de cierre del libro, que siguen siendo de la etapa 1, y la cita incompleta del orgánico 2016–19 en Palancas!C14 de la fase B (falta [RD2017, PDF p. 187] para el 2,4 %; sin efecto en la palanca).
- Datos ausentes «crecimiento del mercado» y «efecto precio y volumen»: el rango 2,4–3,3 % lleva ahora sus dos fuentes ([RD2017, PDF p. 187] y [URD2019, PDF p. 145]).
- G7 NORMAL: retirado el ≈23 % del capital tangible de C24; apoyo en el ROCE publicado (14,7 % antes de impuestos, ≈10,5 % después) y en C32.
- G7 BUENO: retirado el contraste del capital tangible; se mantiene con confianza baja tras calcular que D16 = 1,2 y D18 = 0,10 mueven el precio de Sí −4,0 % (hoja) y −1,3 % (techo) sin cambiar zona ni cubo; `revisar_palancas` sigue en false.
- `celdas_corregidas`: añadidas Palancas!D16 y D18 (revisadas, sin cambio, con el cálculo).
- Hipótesis sin fundamento 2 (C16, D16, C18, D18): `hay_base` pasa de true a false y `rango` a null, porque el techo se apoyaba en el ROIC incremental y el capital tangible de la antigua evidencia de C24.
- Autocomprobación: anclaje en la etapa 1 (rango nuevo y umbral de la fase A de ≈16,6 €), anclaje en el precio (g ≈3,3 %), consistencia (holgura pequeña), optimismo del BUENO (D16 y D18), disponibilidad (la recompra de 2026 a 26,25 € pasa a ser la recompra anunciada en el URD 2025; Brasil ≈0,28 € por acción), autoridad (guía 2026 del URD 2025), MALO (5,58 €) y lo no numerable (dilución en lugar del tratamiento pendiente de la OCEANE).
- Datos ausentes: el dato de la guía 2026 cambia de redacción y se revisa de nuevo; se actualizan los motivos del reparto del capex (rango 11,08–21,89 €), la tasa de bajas, los contratos públicos, Palancas!C24, el efecto precio y volumen (sin H1-2026) y el coste de la deuda (bono de mar-2026 como hecho posterior publicado en el URD 2025).
- Sin cambios: el cubo provisional (Vigilar), la conclusión provisional (`esperar`), `alguno_material = true`, el dato material (reparto del capex), las dos hipótesis sin fundamento, `resultado = no_procede`, `limite_del_modelo.aplica = false`, G5 BUENO, el motor A y C18.

### Turno 2

- Escalera, C104, B222, decisión e insumos con los números nuevos de `precio.json` (7,30 / 5,58 / 7,99 €; distancias 69,8 % y 76,9 % ÷ precio) en lugar de 6,56 / 5,01 / 7,17 €.
- Supuesto F1 añadido en la escalera, los insumos, C104 («motor A no validado con NIIF 16, F1» dentro de la lista de pendiente de datos), su observación, B101, B222, B223, `comparacion_etapa_1` y `cambiaria_de_cubo`; la «propuesta del turno 1» sobre el ancla f pasa a ser la corrección (b) de F1, pendiente.
- Fechas distintas declaradas en la escalera, los insumos (`fecha_precio`, `fecha_base`), B101, B102, la observación de C104 y la condición «a Sí».
- Rango corregido fuera de la hoja 9,95–19,65 → 11,08–21,89 € y techo del ponderado 21,02 → 23,42 € en todos los textos.
- B101 reescrita: sin el +3,2 % de H1-2026; añadido el margen EBIT ajustado plano de 2023–25.
- B102 reescrita: sin la recompra de 2026 a 26,25 €, el 2,09x de junio de 2026 ni México (H1-2026); añadidos C34 a 31-dic-2025, la recompra y el bono anunciados en el URD 2025, las pérdidas de contratos de Reino Unido y Alemania y la dilución potencial; 308 → 307,9 y g implícito ≈3,9 % → ≈3,3 %.
- Predicciones (valores, fechas y probabilidades sin cambio): quitados los apoyos de H1-2026 (3,2 %, 15,1 %, 19,5 % y la guía de ≈18 %); añadidos 2019 (3,3 % [URD2019, PDF p. 145]) y los salarios fijados por el Estado en Latinoamérica [URD2025, PDF p. 308]; la fecha de publicación se apoya en la aprobación de las cuentas de 2025 del 10-mar-2026 [URD2025, PDF p. 330] en lugar del comunicado de resultados de 2026.
- Herencia: B101 y B102 explican la retirada del capital tangible y de lo de 2026; C104 añade F1; `etapa1` sin cambios.
- `comparacion_etapa_1`: precio de Sí v2 6,56 → 7,30 € con 232,48 m acciones en circulación (antes 259,08 m medias diluidas).
- `cambiaria_de_cubo` y condiciones de revisión: apalancamiento de referencia 1,75x a 31-dic-2025 (antes 2,09x de junio de 2026); pérdidas de contratos de Reino Unido y Alemania en lugar de México; la dilución incorporada como condición a la baja.
- Insumos: nueva línea de dilución potencial no incorporada; descalificadores de gestión y deuda sin cifras de 2026.
- Sin cambios: estado `pendiente_de_datos`, cubo Vigilar, acción y precio objetivo `null`, `resultado = no_procede`, `sobrevive = null`, C93 = Sí, C103 = No, confianza global media y todo el turno 1.
