# Elis · análisis de las entradas de la configuración experimental (Munger V2, entrega 4.14)

Base económica: 31-dic-2025. Millones de euros salvo que se diga otra cosa. Las cifras se han buscado en su página: 179 de 179 citas encontradas (tabla «Cifras comprobadas» al final), con el script `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/elis_config/analisis_configuracion_elis.py`. Documentos: URD 2021–2025 (el de 2024 está en francés) e informe semestral 2026. Para cada año se usa la edición más reciente que lo publica, la misma que usó la Historia (fase 1). Nada viene de Vidrala ni de Viscofan, y nada se adopta. Cada sección separa **Hechos** (lo que publica la empresa o se calcula directamente con ello), **Interpretación** y, donde toca, **Opciones** (sin elegir ninguna).

## N1 · tipo impositivo (perímetro: consolidado, actividades continuadas; período 2021–2025, el de la regla heredada)

**Hechos.** No hubo actividades interrumpidas en 2021–2025: el resultado de las interrumpidas es 0,0 en 2025 y 2024 (URD 2025, p. 324), en 2023 (URD 2024, p. 270) y en 2022 y 2021 (URD 2022, p. 258). El tipo teórico de la matriz es 28,41 % en 2021 y 25,83 % de 2022 a 2025. La empresa presenta la CVAE francesa (y el IRAP italiano) dentro del impuesto sobre beneficios, porque «meets the definition of income tax in paragraph 2 of IAS 12» (URD 2025, p. 333), y la saca aparte en la conciliación («Effect of tax not based on net income»). Convención del desglose: la diferencia es el impuesto teórico menos (el impuesto real − CVAE). Una partida positiva reduce el impuesto. El desglose cuadra con la diferencia con un error de ±0,1 (redondeo).

| Año | BAI | Impuesto real | CVAE/IRAP | Dif. de tipo | Permanentes (NIIF 2…) | Bases negativas / créditos | Deterioro del fondo de comercio | Complementos de precio | Otras (CVAE deducible…) | Fuente |
|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 171,0 | 56,6 | 5,7 | 12,2 | −12,2 | −6,0 | 0,0 | — | 3,7 | URD 2022 p. 326 |
| 2022 | 282,3 | 79,7 | 6,8 | 8,8 | −12,3 | 12,5 | −15,1 | 0,5 | 5,7 | URD 2023 p. 345 |
| 2023 | 372,2 | 110,3 | 4,6 | 0,0 | −12,2 | 14,8 | — | −15,8 | 3,6 | URD 2024 p. 337 |
| 2024 | 465,9 | 128,3 | 3,5 | −0,1 | −12,1 | 0,3 | — | 0,8 | 6,7 | URD 2025 p. 392 |
| 2025 | 492,9 | 126,2 | 3,7 | −7,2 (incl. −4,9 de contribución excepcional) | 5,6 | −0,2 | — | −0,2 | 6,8 | URD 2025 p. 392 |

| Año | Fila del tipo (Historia) = efectivo | Sin las partidas no recurrentes (A) | (A) y sin bases negativas (B) | Sin la CVAE (lectura) |
|---|---|---|---|---|
| 2021 | 33,10 % | 33,10 % | 29,59 % | 29,77 % |
| 2022 | 28,23 % | 23,06 % | 27,49 % | 25,82 % |
| 2023 | 29,63 % | 25,39 % | 29,37 % | 28,40 % |
| 2024 | 27,54 % | 27,71 % | 27,77 % | 26,79 % |
| 2025 | 25,60 % | 24,57 % | 24,53 % | 24,85 % |
| **Media 2021–2025** | **28,82 %** (regla heredada, C52) | **26,77 %** | **27,75 %** | 27,13 % |
| Media 2022–2025 (lectura) | 27,75 % | 25,18 % | 27,29 % | — |

(A) quita del impuesto el efecto de las partidas que la conciliación nombra y que no se repiten por su naturaleza: deterioro no deducible del fondo de comercio de Rusia (2022, −15,1), ajustes y actualización no deducibles de complementos de precio (2022 +0,5, 2023 −15,8, 2024 +0,8, 2025 −0,2) y contribución excepcional francesa (2025, −4,9, dentro de «diferencias de tipo»). La empresa dice que esa contribución no se aplica al grupo fiscal de Elis en 2026 (informe semestral 2026, p. 9). (B) quita además las partidas de bases negativas y créditos fiscales. Agregados 2021–2025 (Σ impuesto ÷ Σ BAI): efectivo 28,08 %; (A) 26,14 %. Si se calcula de otra forma, sumando al BAI las partidas no deducibles antes de impuestos (58,7 del fondo de comercio en 2022, impreso; 61,2 de complementos en 2023, derivado como 15,8 ÷ 25,83 %) en lugar de restarlas del impuesto, la media es 26,81 %. Tipo efectivo medio según la NIC 12 §86 publicado por la empresa: 25,6 % en 2025 y 27,5 % en 2024 (URD 2025, p. 393).

**Interpretación.** Qué distorsiona y por qué:
- 2021 tiene un tipo teórico distinto: 28,41 % frente al 25,83 % posterior, por la bajada del tipo francés. Por eso la media 2021–2025 mezcla dos regímenes; la media 2022–2025 es solo una lectura.
- El deterioro de Rusia de 2022 (58,7, no deducible) y la revaluación del complemento de precio de México en 2023 (−48,9 en el resultado operativo; la empresa dice que el tipo francés de 2023 quedó «fortement impacté» por esos ajustes, URD 2024, p. 338) suben el tipo de esos años por partidas que no se repiten.
- Las bases negativas mezclan signos: −6,0; +12,5; +14,8; +0,3; −0,2. Su efecto neto 2021–2025 baja el impuesto, sobre todo en 2022–2023.
- Las diferencias permanentes (sobre todo la NIIF 2 no deducible) restan unos −12 al año de 2021 a 2024 y cambian de signo en 2025 (+5,6). La empresa no explica el cambio más allá de la etiqueta. Son recurrentes mientras haya pagos en acciones.
- La CVAE (3,5–6,8 al año) está en el impuesto y no en el EBIT. Quitarla del tipo dejaría ese coste fuera del NOPAT. Por eso es solo una lectura, no una corrección.

## N2 · margen de partida

**Hechos.** El EBIT de la Historia es el «Operating income» de la cuenta de resultados (630,0 en 2025, derivado como BAI 492,9 + resultado financiero 137,1; la cuenta imprime 629,9). Incluye la amortización de intangibles de combinaciones de negocios, los gastos NIIF 2, los «otros ingresos y gastos operativos» (OOIE) y el deterioro del fondo de comercio. La empresa publica el «adjusted EBIT» (el EBITA ajustado del encargo), que excluye todo eso y además las «partidas financieras diversas» (comisiones bancarias). Así lo define el URD 2025, p. 344: «Adjusted EBIT is defined as net income (loss) before net financial income (loss), income tax, share in net income of equity-accounted companies, amortization of intangible assets recognized in a business combination, goodwill impairment losses, other operating income and expenses, miscellaneous financial items (bank fees recognized in operating income) and IFRS 2 expense (share-based payments)». La empresa clasifica en OOIE las partidas «unusual, abnormal or infrequent» (URD 2025, p. 350).

| Año | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Margen EBIT (Historia) | 12,33 % | 5,30 % | 7,83 % | 10,21 % | 4,21 % | 8,58 % | 9,66 % | 11,53 % | 13,04 % | 13,13 % |

| Año | EBIT ajustado | Partidas financieras diversas | NIIF 2 | Amort. intangibles de combinaciones | OOIE | Deterioro del fondo de comercio | EBIT reconstruido (Historia) | Margen EBIT ajustado | Margen EBIT sin OOIE ni deterioro |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | 388,3 | 1,6 | 28,0 | 81,1 | 16,1 | 0,0 | 261,5 (261,5) | 12,74 % | 9,11 % |
| 2022 | 543,7 | 1,7 | 22,3 | 82,9 | 9,0 | 58,7 | 369,1 (369,0) | 14,23 % | 11,43 % |
| 2023 | 683,1 | 1,6 | 31,1 | 85,7 | 67,9 | 0,0 | 496,8 (496,8) | 15,85 % | 13,10 % |
| 2024 | 732,9 | 1,8 | 31,4 | 85,0 | 18,5 | 0,0 | 596,2 (596,3) | 16,02 % | 13,44 % |
| 2025 | 766,6 | 1,9 | 45,9 | 85,7 | 3,1 | 0,0 | 630,0 (630,0) | 15,98 % | 13,20 % |

- Regla heredada (Palancas C8 «Último año»): **13,13 %**. Media 2021–2025: 11,19 %. Media de diez años: 9,58 %; mínimo 4,21 % (2020), máximo 13,13 % (2025). Media 2021–2025 del margen ajustado: 14,96 %. Sin OOIE ni deterioro: 12,06 %. Sin OOIE, deterioro ni amortización de intangibles de combinaciones: 11,77 %; 13,60 %; 15,09 %; 15,30 %; 14,98 %.
- Diferencia entre el EBIT y el EBIT ajustado en 2025: 136,7 (2,85 puntos de margen) = NIIF 2 45,9 + intangibles de combinaciones 85,7 + OOIE 3,1 + partidas financieras diversas 1,9.
- Partidas que la empresa identifica, todas incluidas en el EBIT de la Historia:
  - OOIE de 2025: −3,1, neto de una plusvalía de +25,7 por bajas de inmovilizado y de costes de reestructuración (5,4), de cambio de sistemas (7,6), medioambientales (5,2) y otros (6,2).
  - OOIE de 2024: −18,5, con un complemento de precio de +8,7.
  - OOIE de 2023: −67,9, con −48,9 de complemento de precio de México.
  - Deterioro del fondo de comercio de Rusia en 2022: 58,7.
  - El resultado «headline» excluye también la NIIF 2 (45,9 en 2025), la actualización del complemento de México (0,7) y la contribución fiscal excepcional (4,9) (URD 2025, p. 313).

**Interpretación.** El margen de 2025 (13,13 %) es el máximo de la serie y el EBIT de 2025 lleva dentro OOIE casi nulos. Sin la plusvalía de +25,7, los OOIE de 2025 serían −28,8 (la empresa cifra en −28,2 sus partidas monetarias). La serie 2016–2020 tiene otro perímetro (compra de Berendsen en 2017: adquisiciones de 1.361,9) y la caída de 2020 (pandemia), así que la media de diez años mezcla regímenes distintos. Los OOIE tienen partidas que aparecen todos los años (reestructuración 5–7, sistemas, rehabilitación medioambiental): «no recurrente» es la clasificación de la empresa, no una comprobación. Los gastos NIIF 2 (22–46 al año) y la amortización de las relaciones con clientes (≈85 al año mientras sigan las adquisiciones) son costes recurrentes que el EBIT ajustado excluye. Usar el margen ajustado como N2 dejaría fuera unos 2,85 puntos de costes que se repiten.

## N3 · circulante comercial a 31-dic-2025 (balance, URD 2025, p. 326; ventas 2025: 4.796,8)

**Hechos.**

| Lectura | Existencias | Deudores | Acreedores | Circulante | ÷ ventas |
|---|---|---|---|---|---|
| A · líneas del balance (definición B29:B31) | 205,9 | 945,3 (comerciales y otras cuentas a cobrar) | 457,0 (comerciales y otras cuentas a pagar) | 694,2 | **14,47 %** |
| A2 · A sin proveedores de inmovilizado (47,7) | 205,9 | 945,3 | 409,3 | 741,9 | 15,47 % |
| B · solo comercial (notas 4.4 y 4.8) | 205,9 | 838,6 (clientes netos) | 392,2 (proveedores) | 652,3 | 13,60 % |
| C · A con activos (53,5) y pasivos (89,2) de contratos | 205,9 | 998,8 | 546,2 | 658,5 | 13,73 % |
| D · C con otros activos (26,0) y otros pasivos corrientes (529,4: personal 303,1, impuestos y otras deudas 206,6…) | 205,9 | 1.024,8 | 1.075,6 | 155,1 | 3,23 % |

Conciliación de las notas:
- Deudores (nota 4.4, p. 349): 945,3 = 838,6 de clientes netos + 106,7 de otras cuentas a cobrar.
- Acreedores (nota 4.8, p. 351): 457,0 = 392,2 de proveedores + 47,7 de proveedores de inmovilizado + 17,2 de otras cuentas a pagar.
- Existencias (nota 4.7, p. 351): 205,9, de las que 159,4 son mercaderías.

Misma lectura A a 31-dic-2024: (200,0 + 839,7 − 407,8) ÷ 4.573,7 = 13,82 %.

**Interpretación.** La lectura A sigue la definición de la plantilla y es la que corresponde a «Configuración V6.4» B29:B31. Las demás son lecturas de sensibilidad. Elis es intensiva en personal: sus pasivos con el personal (303,1) y fiscales (206,6) quedan fuera de la definición. Una regla R1 que libera circulante cuando caen las ventas los ignora, aunque en la práctica también bajarían. Los proveedores de inmovilizado (47,7) son deuda por capex, no circulante comercial. La política contable dice que los artículos de alquiler se registran primero como existencias y después se activan (nota 6.4, p. 367): parte de las existencias (materias primas 36,7, mercaderías 159,4) puede ser lino aún no puesto en servicio. Las cuentas no lo separan.

## Capex, amortización y adquisiciones 2021–2025, por bloques

**Hechos.** Los bloques son:
- (a) Artículos de alquiler propios (lino y ropa, más otros artículos de alquiler, mantenimiento y lavandería como aparatos de higiene). Es inmovilizado material propio de Elis: se activa y se amortiza (nota 6.4, «Rental & maintenance items»).
- (b) Resto del capex material e intangible.
- (c) Derechos de uso NIIF 16: activos que Elis arrienda («property, vehicles, machines, and other equipment», nota 6.3, p. 365).
- (d) Amortización de cada bloque (nota 4.5).
- (e) Adquisiciones de dependientes netas de caja (estado de flujos).

El capex de caja de (a) y (b) sale de la tabla de pagos de la sección 4.2.4. (a) + (b) coincide con la fila capex de la Historia, que suma los pagos brutos por intangibles e inmovilizado material del estado de flujos, sin restar cesiones (15,3 en 2025) ni subvenciones (0,2). (a) nunca se mezcla con (c).

| Año | (a) Lino | (a) Otros artículos | (a) Total, caja | (a) Altas, nota 6.4 | (b) Resto del capex | Capex = Historia | (c) Nuevos derechos de uso | (c) Reestimaciones | (c) Por combinaciones | Principal de arrendamientos |
|---|---|---|---|---|---|---|---|---|---|---|
| 2021 | 406,7 | 32,6 | 439,3 | 441,9 | 134,6 | 573,9 | 71,1 | 20,8 | 1,7 | 89,4 |
| 2022 | 518,8 | 37,3 | 556,1 | 556,1 | 143,7 | 699,8 | 90,4 | 19,7 | 21,7 | 101,5 |
| 2023 | 584,3 | 37,3 | 621,6 | 621,6 | 202,3 | 823,9 | 132,6 | 24,9 | 1,5 | 111,0 |
| 2024 | 594,3 | 34,6 | 628,9 | 628,8 | 258,6 | 887,4 (suma 887,5) | 145,7 | 39,6 | 9,0 | 125,0 |
| 2025 | **594,2** | **40,8** | **635,0** | 635,0 | **255,2** | 890,2 | **183,9** | 50,0 | 11,7 | 148,3 |
| Σ | 2.698,3 | 182,6 | 2.880,9 | 2.883,4 | 994,4 | 3.875,2 | 623,7 | 155,0 | 45,6 | 575,2 |

| Año | (d) Lino | (d) Otros artículos | (d) Resto | (d) Derechos de uso | Subvenciones | Deterioro en OOIE | (d) Intangibles de combinaciones (de ellos, relaciones con clientes) | D&A total = Historia | (e) Adquisiciones |
|---|---|---|---|---|---|---|---|---|---|
| 2021 | 386,9 | 28,5 | 156,3 | 92,6 | −0,6 | 0,0 | 81,1 (78,2) | 744,8 | 86,8 |
| 2022 | 424,0 | 30,3 | 158,6 | 103,7 | −0,7 | 0,1 | 82,9 (80,9) | 799,0 | 221,7 |
| 2023 | 482,1 | 32,7 | 161,6 | 115,8 | −0,5 | 0,0 | 85,7 (84,6) | 877,4 | 82,1 |
| 2024 | 537,6 | 35,3 | 172,5 | 132,2 | −0,9 | 3,3 | 85,0 (83,9) | 965,1 | 183,3 |
| 2025 | **565,1** | **36,3** | **183,6** | **149,5** | −1,0 | 0,1 | **85,7 (83,5)** | 1.019,4 | 117,6 |
| Σ | 2.395,7 | 163,1 | 832,6 | 593,8 | −3,7 | 3,5 | 420,4 (411,1) | 4.405,7 | 691,5 |

Diferencias por bloque (inversión − amortización):
- (a): 23,9; 101,8; 106,8; 56,0; 33,6. Σ 322,1; razón 1,126. En 2025, 635,0 frente a 601,4 (razón 1,056).
- (b): −21,7; −14,9; 40,7; 86,1; 71,6. Σ 161,8.
- (c), solo nuevos: −21,5; −13,3; 16,8; 13,5; 34,4. Σ 29,9. Con las reestimaciones: Σ 184,9.
- Intangibles de combinaciones: 420,4 amortizados frente a 165,7 de altas de relaciones con clientes por combinaciones (21,1; 88,0; 20,6; 32,3; 3,7).

Capex ÷ D&A de la Historia: 0,77; 0,88; 0,94; 0,92; 0,87 (diez años: 0,88). Ventas 2021→2025: +57,36 %; 2020→2025: +70,93 %. Las compras de lino son el 12,4 % de los ingresos en 2025 y el 13,0 % en 2024 (p. 311). La empresa dice que el capex «has returned to normal levels since 2024» (p. 312).

**Interpretación.** La D&A de la Historia (1.019,4 en 2025) tiene cuatro capas:
- la de los activos que se reponen con capex (lino y otros artículos 601,4; resto 183,6);
- la de los derechos de uso (149,5, el 14,7 %), que se repone con nuevos arrendamientos y no con capex;
- la de las relaciones con clientes y marcas de combinaciones (85,7, el 8,4 %), que solo se reponen con adquisiciones;
- subvenciones y deterioros, que son menores.

Por eso el capex de la Historia está por debajo de la D&A todos los años (Σ −530,5), aunque los dos bloques que se reponen con capex superan su amortización (+322,1 y +161,8).

## Bases históricas de «Configuración V6.4»

Se calculan con las fórmulas de la plantilla, las mismas que `replica_independiente_v641.py`, sobre la Historia de 2021–2025:
- D_hist = Σ (capex − D&A + adquisiciones + circulante) + cartera + altas;
- exceso = Σ (capex − D&A) + cartera + altas;
- F_hist = exceso + Σ adquisiciones;
- A (B63) = Σ D&A − cartera;
- S2C histórico = (ventas 2025 − ventas 2020) ÷ D_hist (C53 con «Caja»; B155 con NIIF 16).

Σ circulante 2021–2025 = 59,2; Δventas 2020→2025 = 1.990,5; D&A₀ (B54) = 1.019,4; Σ adquisiciones (B59) = 691,5; 1 ÷ NWC (lectura A) = 6,910.

| Perímetro · cartera | Altas (B153) | Cartera (B56) | D_hist (B57) | Exceso (B60) | Exceso medio (B61) | F_hist (B62) | A (B63) | S2C histórico | λ máx. con f definida | λ máx. SRF |
|---|---|---|---|---|---|---|---|---|---|---|
| Caja · legado | 0 | 0 | 220,2 | **−530,5** | −106,1 | 161,0 | 4.405,7 | **9,040** (C53) | 1,0500 | 1,0365 |
| NIIF 16 (solo nuevos derechos) · legado | 623,7 | 0 | 843,9 | 93,2 | 18,64 | 784,7 | 4.405,7 | 2,359 | 1,1915 | 1,1781 |
| NIIF 16 (nuevos + reestimaciones) · legado | 778,7 | 0 | 998,9 | 248,2 | 49,64 | 939,7 | 4.405,7 | 1,993 | 1,2267 | 1,2133 |
| Caja · P0 (relaciones con clientes) | 0 | 411,1 | 631,3 | −119,4 | −23,88 | 572,1 | 3.994,6 | 3,153 | 1,1580 | 1,1432 |
| NIIF 16 (nuevos) · P0 | 623,7 | 411,1 | 1.255,0 | 504,3 | 100,86 | 1.195,8 | 3.994,6 | 1,586 | 1,3142 | 1,2994 |
| NIIF 16 (nuevos + reestimaciones) · P0 | 778,7 | 411,1 | 1.410,0 | 659,3 | 131,86 | 1.350,8 | 3.994,6 | 1,412 | 1,3530 | 1,3382 |

Familia Θ (Rh = θ × exceso; nivel anual = θ × exceso medio):

| Perímetro · cartera | θ = 0,5: f (SR1, SR2) · f_fija (SRF) · nivel | θ = 1: f · f_fija · nivel |
|---|---|---|
| Caja · legado | exceso < 0: requisito negativo, no definido | no definido |
| NIIF 16 (nuevos) · legado | 1,0584 · 0,9406 · 9,32 | 1,1242 · 0,8812 · 18,64 |
| NIIF 16 (nuevos + reestimaciones) · legado | 1,1419 · 0,8679 · 24,82 | 1,3306 · 0,7359 · 49,64 |
| Caja · P0 | exceso < 0: no definido | no definido |
| NIIF 16 (nuevos) · P0 | 1,2514 · 0,7891 · 50,43 | 1,6718 · 0,5783 · 100,86 |
| NIIF 16 (nuevos + reestimaciones) · P0 | 1,3051 · 0,7560 · 65,93 | 1,8782 · 0,5119 · 131,86 |

**Dominios (hechos de la especificación con estas bases).** Con «Caja» el exceso es negativo, así que la familia Θ da un requisito a ventas constantes negativo para todo θ > 0, que la plantilla rechaza («el requisito a ventas constantes es negativo»). Solo θ = 0 (sin requisito) queda definido. Con Λ y «Caja», f deja de estar definida por encima de λ = 1,0500 y SRF por encima de λ = 1,0365. La inversión fija para crecer de R1 es negativa cuando S2C × f > 1 ÷ NWC = 6,910. Con «Caja», el S2C histórico (C53 = 9,040) ya supera ese umbral con f = 1. La plantilla aplica un tope a la palanca del S2C (rentabilidad marginal ≤ 2 × ROIC histórico C55); este análisis no ha calculado C55. Con NIIF 16 el S2C histórico (B155) queda entre 1,41 y 2,36, y con θ = 1 el producto S2C × f vale 2,65 en las cuatro filas NIIF 16: es Δventas ÷ (Σ adquisiciones + Σ circulante) = 1.990,5 ÷ 750,7, sea cual sea la lectura de altas o de cartera. Está por debajo del umbral.

## Datos para P-M1 (opciones; ninguna elegida)

**Hechos sobre la cartera de activos de alquiler:**
- Vida útil: «items related to rental & maintenance service agreements (textiles, equipment, and other leased items) are initially recognized as inventories and are then capitalized and depreciated over a period of 18 months to five years» (nota 6.4, p. 367).
- Saldos a 31-dic-2025: valor neto 1.037,7, amortización del año 601,6 (valor neto ÷ amortización = 1,72 años) y valor bruto 2.550,4. El bruto era 3.096,5 un año antes (bruto ÷ inversión anual = 4,0 años). La tabla da solo movimientos netos, así que la bajada del bruto no se ve como partida.
- Inversión ÷ amortización en 2021–2025: 1,058; 1,224; 1,207; 1,098; 1,056 (Σ 1,126).
- La empresa dice que el gasto en lino «varies according to the level of activity and the schedule for providing linen to the Group’s customers», y que «Growth investments thus make up a large percentage of this expenditure because of the initial outlay required to set up a new customer» (p. 312). Del capex industrial dice que cubre «both growth (new plants or to increase capacity) and maintenance (equipment replacement)».

Ninguna cifra separa la reposición del crecimiento.

**Hechos sobre los derechos de uso:**
- Vehículos: 123,8 de los 183,9 nuevos de 2025.
- Amortización 149,5; pagos de principal 148,3; pagos con intereses 177,9 (flujos, p. 327); pasivo 703,2 (p. 366).
- Altas 2021–2025 por la lectura: solo nuevos [71,1; 90,4; 132,6; 145,7; 183,9] = 623,7. Nuevos + reestimaciones [91,9; 110,1; 157,5; 185,3; 233,9] = 778,7. Por combinaciones [1,7; 21,7; 1,5; 9,0; 11,7] = 45,6. Las de combinaciones llegan con las adquisiciones, cuya caja ya está en la fila de adquisiciones.

**Hechos sobre la cartera de clientes (para P0):**
- Relaciones con clientes de combinaciones: amortización [78,2; 80,9; 84,6; 83,9; 83,5] = 411,1; valor neto a 31-dic-2025 de 275,1; vida de 4 a 14 años (nota 6.2, p. 364).
- La línea completa de intangibles de combinaciones, con marcas, es [81,1; 82,9; 85,7; 85,0; 85,7] = 420,4.
- P0 cumple la condición de la plantilla: 275,1 ≤ 10 × 83,5. La cartera se agotaría en unos 3,3 años (83,5; 83,5; 83,5; 24,6; 0…).

**Opciones de perímetro de la inversión:**
- **«Caja»**: capex de caja frente a toda la D&A. Consecuencias: Θ queda indefinida (exceso −530,5), Λ queda en un dominio de λ < 1,05 (SRF < 1,0365) y el S2C histórico C53 vale 9,04, por encima de 1 ÷ NWC. La D&A que compara incluye 593,8 de derechos de uso y 420,4 de intangibles de combinaciones que el capex no repone.
- **«NIIF 16»**: capex + altas de derechos de uso frente a toda la D&A. Consecuencias: con solo los nuevos, el exceso es 93,2 y Θ está definida en todo [0, 1] (f ≤ 1,124); con las reestimaciones, el exceso es 248,2 (f ≤ 1,331). Es coherente con que el motor B trata los arrendamientos como capital y como deuda (Historia: pasivo 703,2; principal 148,3), y su NOPAT ya descuenta la amortización de los derechos de uso. La plantilla admite una serie de cinco altas; qué se cuenta como alta (con o sin reestimaciones) es una decisión de definición, y en Elis las reestimaciones son materiales (155,0).

**Opciones de estructura y familia (con NIIF 16):**
- **Sin requisito adicional.**
- **Θ** (θ no observado; dominio [0, 1]) con SR1, SR2 o SRF: todas definidas en todo θ con las dos lecturas de altas y con legado o P0. Las cifras de f y f_fija están en la tabla de la familia Θ.
- **Λ** (λ no observado): SR1 y SR2 definidas hasta λ = 1,19–1,35 y SRF hasta 1,18–1,34, según las altas y la cartera.
- Para Λ, la evidencia más cercana a un λ observado es la razón inversión ÷ amortización de los activos que se reponen con capex: 1,126 en los artículos de alquiler; 1,143 en el capex total frente a la D&A sin derechos de uso ni intangibles de combinaciones; 1,021 en capex + nuevos derechos frente a toda la D&A. Estas razones mezclan reposición y crecimiento (ventas +57 % en el período): no son λ.

**Opciones de cartera:**
- **Legado.** La amortización de las relaciones con clientes cuenta como amortización que se repone.
- **P0.** No se repone con capex, con importes que constan sin ceros. Consecuencia: el exceso sube en 411,1 y A baja a 3.994,6. Interpretación: en Elis esa cartera se repone, si acaso, con adquisiciones (165,7 de altas por combinaciones frente a 411,1 amortizados).

## Hechos que pueden poner en duda la aplicabilidad del motor B (los decide la fase A)

1. El capex de la Historia es menor que la D&A en nueve de los diez años (todos menos 2017; razón de diez años: 0,88), con ventas que crecen. La razón es de definición (la D&A incluye derechos de uso e intangibles de combinaciones), pero con el perímetro «Caja» deja la reinversión neta en 220,2 y la familia Θ sin definir.
2. El S2C histórico con «Caja» (C53 = 9,04) parte de 2020, el año más bajo de la pandemia (ventas 2.806,3 frente a 3.281,8 en 2019), y supera el umbral 1 ÷ NWC (6,91): con R1, la inversión fija para crecer saldría negativa salvo que el tope de la palanca la recorte.
3. Crecimiento por adquisiciones. Fueron 691,5 en 2021–2025 y 1.361,9 en 2017 (Berendsen). La serie de diez años cambia de perímetro: margen EBIT de 5,30 % en 2017 y de 4,21 % en 2020.
4. Activos de alquiler de vida corta (18 meses a 5 años; valor neto ≈ 1,7 años de amortización). Son el 59 % de la D&A de 2025 y el 71 % del capex, y la empresa dice que buena parte de ese gasto es crecimiento (puesta en marcha de clientes). θ y λ no se observan, y el resultado puede depender mucho de ellos.
5. Los arrendamientos son materiales (pasivo 703,2; pagos con intereses de 177,9 frente a un flujo de caja libre de 358,6 según la empresa, p. 314).
6. Lo que queda fuera de la definición del circulante es grande: pasivos de personal y fiscales de 509,7, frente a un circulante de 694,2.
7. Hechos posteriores al cierre que no se mezclan con la base (fase 1): recompra de 17.787.422 acciones en el primer semestre de 2026 y conversión de las OCEANE 2029 (octubre de 2026). Afectan a las acciones, no a estas entradas.

## Cifras comprobadas

Cita literal tal como figura en la página (espacios normalizados; los números de la cita son los publicados, con su signo y su formato). Página = marca «[PDF PAGE n]» del texto del documento.

| Id | Cifra (concepto) | Ejercicio | Documento | Página | Cita |
|---|---|---|---|---|---|
| T25_bai | resultado antes de impuestos (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «INCOME (LOSS) BEFORE TAX 492.9 465.9» |
| T25_cont | resultado de actividades continuadas = resultado neto (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Net income (loss) from continuing operations 366.6 337.7» |
| T25_teo | tipo teórico de la matriz (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Theoretical tax rate 25.83% 25.83%» |
| T25_real | gasto por impuesto real (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «ACTUAL INCOME TAX EXPENSE 126.2 128.3» |
| T25_cvae | efecto de impuestos no basados en el resultado (CVAE, IRAP) (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Effect of tax not based on net income (CVAE in France, IRAP in Italy) 3.7 3.5» |
| T25_tasa | diferencias de tipo (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Differences in tax rate (7.2) (0.1)» |
| T25_perm | diferencias permanentes (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Permanent differences (including non-deductible IFRS 2 expenses in 2024) 5.6 (12.1)» |
| T25_bin | bases negativas / créditos fiscales (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Utilization of previously unrecognized tax losses/(Unrecognized tax loss carryforwards)/Tax credits (0.2) 0.3» |
| T25_earn | ajustes de complementos de precio no deducibles (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Adjustments and accretion of non-deductible earnouts (0.2) 0.8» |
| T25_otras | otras diferencias (CVAE deducible…) (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «Other differences (deductible CVAE, etc.) 6.8 6.7» |
| T25_contrib | contribución excepcional francesa en «diferencias de tipo» | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 392] | «exceptional contribution on the profits of large French companies (€4.9 million in 2025)» |
| T25_ias12 | tipo efectivo medio NIC 12 §86 (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 393] | «TOTAL 492.9 126.2 25.6% 465.9 128.3 27.5%» |
| T25_bases | bases negativas sin activo diferido | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 393] | «€51.0 million (base) for which no deferred tax assets had been» |
| T25_cvae_nic12 | la CVAE se trata como impuesto sobre beneficios | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 333] | «meets the definition of income tax in paragraph 2 of IAS 12» |
| T26_contrib | la contribución excepcional no se aplica en 2026 | 2026 | Elis_2026_half-year_financial_report_EN.txt | [PDF PAGE 9] | «apply to the Elis tax group in 2026» |
| T23_bai | resultado antes de impuestos (2024 y 2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «RÉSULTAT AVANT IMPÔT 466,0 372,2» |
| T23_teo | tipo teórico (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «Taux théorique 25,83% 25,83%» |
| T23_real | impuesto real (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «IMPÔT RÉEL 128,3 110,3» |
| T23_cvae | CVAE / IRAP (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «(CVAE en France, IRAP en Italie) 3,5 4,6» |
| T23_tasa | diferencias de tipo (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «Différences de taux d'impôt (0,1) (0,0)» |
| T23_perm | diferencias permanentes (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «Différences permanentes (dont charges IFRS 2 non déductibles) (12,1) (12,2)» |
| T23_bin | bases negativas / créditos (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «Crédits d'impôts 0,3 14,8» |
| T23_earn | complementos de precio no deducibles (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «non déductibles* 0,8 (15,8)» |
| T23_otras | otras diferencias (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 337] | «Autres différences (CVAE déductible…) 6,7 3,6» |
| T23_mexico | causa del tipo francés de 2023 | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 338] | «par les ajustements de compléments de prix» |
| T22_bai | resultado antes de impuestos (2023 y 2022 reexpresado) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «INCOME (LOSS) BEFORE TAX 372.9 282.3» |
| T22_real | impuesto real (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «ACTUAL TAX EXPENSE 110.4 79.7» |
| T22_cvae | CVAE / IRAP (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «(CVAE in France, IRAP in Italy) 4.6 6.8» |
| T22_tasa | diferencias de tipo (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «Differences in tax rate (0.0) 8.8» |
| T22_perm | diferencias permanentes (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «Permanent differences (including non-deductible IFRS 2 expenses) (12.2) (12.3)» |
| T22_bin | bases negativas / créditos (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «Tax credits 14.8 12.5» |
| T22_gw | deterioro del fondo de comercio (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «Goodwill impairment (0.0) (15.1)» |
| T22_earn | complementos de precio no deducibles (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «earnouts** (15.8) 0.5» |
| T22_otras | otras diferencias (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 345] | «Other differences (deductible CVAE, etc.) 3.6 5.7» |
| T21_bai | resultado antes de impuestos (2022 y 2021 reexpresado) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Income (loss) before tax 285.1 171.0» |
| T21_teo | tipo teórico (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Theoretical tax rate 25.83% 28.41%» |
| T21_real | impuesto real (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «ACTUAL TAX EXPENSE 80.5 56.6» |
| T21_cvae | CVAE / IRAP (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Effect of tax not based on net income(a) 6.8 5.7» |
| T21_tasa | diferencias de tipo y operaciones a tipo reducido (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Tax rate differences and transactions taxed at reduced rates 9.3 12.2» |
| T21_perm | diferencias permanentes (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Permanent differences (including non-deductible IFRS 2 expenses) (11.7) (12.2)» |
| T21_bin | bases negativas (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «(Unrecognized tax loss carryforwards) 11.8 (6.0)» |
| T21_otras | otras diferencias (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 326] | «Other differences (deductible CVAE, etc.) 5.7 3.7» |
| P25_rev | ingresos (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 324] | «Revenue 3.1/4.1/4.2 4,796.8 4,573.7» |
| P25_ebit | resultado de explotación (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 324] | «Operating income 3.2 629.9 596.3» |
| P25_fin | resultado financiero (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 324] | «Net financial income (expense) 8.2 (137.1) (130.4)» |
| P25_disc | actividades interrumpidas (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 324] | «Net income (loss) from discontinued operations 0.0 0.0» |
| P25_adj | EBIT ajustado (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 345] | «ADJUSTED EBIT 766.6 732.9 Miscellaneous financial items (1.9) (1.8)» |
| P25_ooie | otros ingresos y gastos operativos (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 345] | «Other operating income and expenses 4.6 (3.1) (18.5)» |
| P25_sbc | gasto NIIF 2 (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 345] | «Expenses related to share-based payments 5.2 (45.9) (31.4)» |
| P25_ppa | amortización de intangibles de combinaciones (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 345] | «Amortization of intangible assets recognized in a business combination 6.2 (85.7) (85.0)» |
| P25_oi | resultado de explotación en la conciliación (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 345] | «OPERATING INCOME 629.9 596.3» |
| P25_def | definición del EBIT ajustado | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 344] | «Adjusted EBIT is defined as net income (loss) before net financial» |
| P25_hl_niif2 | partidas que la empresa excluye del resultado «headline»: NIIF 2 (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 313] | «Expenses related to share-based payments (IFRS 2) 45.9 31.4» |
| P25_hl_contrib | partidas excluidas del «headline»: contribución excepcional (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 313] | «Exceptional contribution - French corporate income tax 4.9 0.0» |
| P25_retiro | plusvalía por bajas de inmovilizado en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Net gain (loss) related to retirement of fixed assets 25.7 (1.5)» |
| P25_reestr | costes de reestructuración en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Restructuring costs (5.4) (7.3)» |
| P25_earn | ajustes de complementos de precio en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Earnout adjustments (0.2) 8.7» |
| P25_ooie_def | criterio de la empresa para OOIE | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Items of material amounts that are unusual, abnormal or infrequent are disclosed separately» |
| P23_rev | ingresos (2024 y 2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 270] | «Produits de l'activité ordinaire 3.1/4.1/4.2 4 573,7 4 309,4» |
| P23_adj | EBIT ajustado 2023 (reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 291] | «(20,3) 683,1» |
| P23_misc | conciliación 2023: partidas financieras diversas, OOIE, NIIF 2 | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 291] | «Frais financiers divers (1,6) Autres produits et charges opérationnels 4.6 (67,9) Charges sur paiements en actions 5.2 (31,1)» |
| P23_ppa | conciliación 2023: amortización de intangibles de combinaciones y resultado de explotación | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 291] | «un regroupement d'entreprises 6.2 (85,7) RÉSULTAT OPÉRATIONNEL 496,8» |
| P23_earn | ajustes de complementos de precio en OOIE (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 296] | «Ajustements de compléments de prix 8,7 (48,9)» |
| P22_rev | ingresos (2023 y 2022 reexpresado) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 263] | «REVENUE 4,309.4 3,820.9» |
| P22_adj | EBIT ajustado 2022 (reexpresado) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 297] | «(17.2) 543.7 Adjusted EBIT margin 21.1% 9.8% 18.1% 7.7% 15.5% 8.7% 14.2% Miscellaneous financial items (1.7)» |
| P22_sbc | conciliación 2022: NIIF 2, intangibles de combinaciones, OOIE, deterioro del fondo de comercio | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 297] | «payments (22.3) Amortization of intangible assets recognized in a business combination (82.9) Other operating income and expenses (9.0) Goodwill impairment (58.7) OPERATING INCOME 369.0» |
| P22_gw | deterioro del fondo de comercio de Rusia | 2022 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 246] | «In Russia, the Group recorded a goodwill impairment loss of» |
| P21_rev | ingresos (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 258] | «Revenue 3.1/4.1/4.2 3,820.9 3,048.3» |
| P21_adj | EBIT ajustado 2021 (reexpresado) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 280] | «(13.0) 388.3» |
| P21_sbc | gasto NIIF 2 en la conciliación (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 280] | «26.5 28.0» |
| P21_ppa | amortización de intangibles de combinaciones (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 258] | «Amortization of intangible assets recognized in a business combination 4.5 (80.1) (81.1)» |
| P21_ooie | OOIE (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 258] | «Other operating income and expenses 4.6 (9.0) (16.1)» |
| P21_ebit | resultado de explotación (2022 y 2021 reexpresado) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 258] | «Operating income 371.8 261.5» |
| P20_rev | ingresos (2021 y 2020) | 2020 | Elis_URD_2021_EN.txt | [PDF PAGE 213] | «Revenue 3,048.3 2,806.3» |
| P25_ooie_mon | partidas monetarias dentro de OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «of which monetary items (28.2) (22.2)» |
| P25_ooie_it | costes de cambio de sistemas en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Non-capitalizable costs related to the change of main IT systems (7.6) (5.2)» |
| P25_ooie_env | rehabilitación medioambiental en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «costs net of changes in provisions (5.2) (2.6)» |
| P25_ooie_otr | otros en OOIE (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Other (6.2) (1.4)» |
| P25_fcf | flujo de caja libre según la empresa (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 314] | «FREE CASH FLOW 358.6 346.3» |
| P19_rev | ingresos (2020 y 2019) | 2019 | Elis - 2020 Universal Registration Document.txt | [PDF PAGE 157] | «Revenue 2,806.3 3,281.8» |
| P17_adq | adquisición de dependientes neta de caja de 2017 (comparativo) | 2017 | Elis - 2018 Registration document.txt | [PDF PAGE 169] | «(1,362.9)» |
| T23_mexico2 | el tipo francés de 2023 quedó muy afectado | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 338] | «fortement impacté au cours de l’exercice 2023 par les ajustements de compléments de prix» |
| C25_mp | materias primas dentro de existencias (nota 4.7) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 351] | «Raw materials, supplies 36.7 37.3» |
| H26_recompra | recompra del primer semestre de 2026 | 2026 | Elis_2026_half-year_financial_report_EN.txt | [PDF PAGE 46] | «bought back 17,787,422 shares for €466.8 million» |
| C25_exist | existencias (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Inventories 4.7 205.9 200.0» |
| C25_cact | activos de contratos (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Contract assets 4.3 53.5 53.1» |
| C25_deud | deudores comerciales y otras cuentas a cobrar (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Trade and other receivables 4.4 945.3 839.7» |
| C25_oact | otros activos corrientes (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Other assets 4.9 26.0 27.6» |
| C25_acre | acreedores comerciales y otras cuentas a pagar (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Trade and other payables 4.8 457.0 407.8» |
| C25_cpas | pasivos de contratos (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Contract liabilities 4.3 89.2 86.5» |
| C25_opas | otros pasivos corrientes (balance) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 326] | «Other liabilities 4.9 529.4 483.1» |
| C25_cli | clientes y efectos a cobrar netos (nota 4.4) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 349] | «TRADE RECEIVABLES AND NOTES RECEIVABLE 838.6 771.0» |
| C25_otrcob | otras cuentas a cobrar (nota 4.4) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 349] | «Other receivables 106.7 68.7» |
| C25_prov | proveedores (nota 4.8) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 351] | «Trade payables 392.2 364.7» |
| C25_provinm | proveedores de inmovilizado (nota 4.8) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 351] | «Trade payables (fixed assets) 47.7 24.6» |
| C25_otrpag | otras cuentas a pagar (nota 4.8) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 351] | «Other payables 17.2 18.4» |
| C25_merc | mercaderías dentro de existencias (nota 4.7) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 351] | «Goods for resale 159.4 153.1» |
| C25_personal | pasivos con el personal (nota 4.9) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 352] | «Payroll-related liabilities 303.1 278.6» |
| C25_fiscal | pasivos fiscales y otras deudas (nota 4.9) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 352] | «Tax liabilities and other debt 206.6 169.8» |
| K25 | capex de caja: lino, otros artículos de alquiler, resto (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 311] | «Linen purchases (594.2) (594.3) Purchases of other items for rental/laundry/maintenance services (40.8) (34.6) Other acquisitions of property, plant and equipment and intangible assets (255.2) (258.6)» |
| K25_pct | compras de lino sobre ingresos (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 311] | «consolidated financial statements) represented 12.4% of revenue» |
| K25_flujos | pagos por intangibles y por inmovilizado material (flujos, 2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 327] | «Acquisition of intangible assets (26.2) (26.6) Proceeds from disposal of intangible assets 0.0 0.0 Acquisition of property, plant and equipment (864.0) (860.8)» |
| K23 | capex de caja (2024 y 2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 257] | «Achats de linge (594,3) (584,3) Achats d’autres articles en location-entretien (34,6) (37,3) Autres acquisitions d’immobilisations corporelles et incorporelles (258,6) (202,3)» |
| K22 | capex de caja (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 266] | «Linen purchases (584.3) (518.8) Purchases of other items for rental/laundry/maintenance services (37.3) (37.3) Other acquisitions of property, plant and equipment and intangible assets (202.3) (143.7)» |
| K21 | capex de caja (2022 y 2021 reexpresado) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 247] | «Linen purchases (518.8) (406.7) Purchases of other items for rental/laundry/maintenance services (37.3) (32.6) Other acquisitions of property, plant and equipment and intangible assets (143.7) (134.6)» |
| K25_pct24 | compras de lino sobre ingresos en 2024 | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 311] | «in 2025 (compared with 13.0% in 2024)» |
| K25_crec | la empresa: el gasto en lino es en gran parte inversión de crecimiento | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «Growth investments thus make up a» |
| K25_crec2 | (continuación de la frase anterior) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «large percentage of this expenditure because of the initial» |
| K25_crec3 | (continuación de la frase anterior) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «outlay required to set up a new customer» |
| K25_lino_act | el gasto en lino varía con la actividad | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «expenditure on linen, which varies according to the level of» |
| K25_mant | el capex industrial cubre crecimiento y mantenimiento | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «maintenance (equipment replacement)» |
| K25_normal | capex en niveles normales desde 2024 | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 312] | «capital expenditure has returned to normal» |
| A25 | amortización por bloques (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «Textile rental & maintenance items (565.1) (537.6) › Other rental & maintenance items (36.3) (35.3) › Other property, plant and equipment and intangible assets (183.6) (172.5) › Right-of-use assets (149.5) (132.2) › Portion of grants transferred to income 1.0 0.9 Impairment losses recognized in Other operating income and expenses (0.1) (3.3) Amortization of intangible assets recognized in a business combination (85.7) (85.0)» |
| A25_tot | amortización total (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 350] | «TO INCOME) (1,019.4) (965.1)» |
| A23 | amortización por bloques (2024 y 2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 296] | «Articles textiles en location-entretien (537,6) (482,1) › Autres articles en location-entretien (35,3) (32,7) › Autres immobilisations incorporelles et corporelles (172,5) (161,6) › Actifs comptabilisés au titre du droit d'utilisation (132,2) (115,8) › Quote-part de subvention virée au compte de résultat 0,9 0,5 Pertes de valeur comptabilisées en autres produits et charges opérationnels (3,3) (0,0) Dotations aux amortissements des incorporels reconnus dans un regroupement d'entreprises (84,9) (85,7)» |
| A23_tot | amortización total (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 296] | «AU COMPTE DE RÉSULTAT) (965,0) (877,4)» |
| A22 | amortización por bloques (2023 y 2022 reexpresado) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 301] | «Textile rental & maintenance items (482.1) (424.0) › Other leased items (32.7) (30.3) › Other property, plant and equipment and intangible assets (161.6) (158.6) › Right-of-use assets (115.8) (103.7) › Portion of grants transferred to income 0.5 0.7 Depreciation and amortization included in Other operating income and expenses (0.0) (0.1) Amortization of intangible assets recognized in a business combination (85.1) (82.9)» |
| A22_tot | amortización total (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 301] | «TO INCOME) (876.8) (799.0)» |
| A21 | amortización por bloques (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 284] | «Textile rental, laundry and maintenance items (424.0) (386.9) Other leased items (30.3) (28.5) Other property, plant and equipment and intangible assets (158.6) (156.3) Right-of-use assets (103.7) (92.6) Portion of grants transferred to income 0.7 0.6 › included in other operating income and expenses (0.1) 0.0 › amortization of intangible assets recognized in a business combination (80.1) (81.1)» |
| A21_tot | amortización total (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 284] | «TO INCOME) (796.2) (744.8)» |
| L25_inv | inversiones en inmovilizado material; columna de artículos de alquiler (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Investments 61.6 3.0 187.6 635.0 887.1» |
| L24_inv | inversiones en inmovilizado material (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Investments 32.9 2.8 187.9 628.8 852.4» |
| L25_am | amortización del inmovilizado material; artículos de alquiler (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Amortization (36.1) (5.1) (118.5) (601.6) (761.3)» |
| L24_am | amortización del inmovilizado material (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Amortization (34.0) (5.6) (110.1) (573.1) (722.7)» |
| L25_vnc | valor neto contable a 31-dic-2025; artículos de alquiler | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «NET CARRYING AMOUNT AS AT DECEMBER 31, 2025 687.4 12.4 778.2 1,037.7 2,515.7» |
| L25_bruto | valor bruto a 31-dic-2025; artículos de alquiler | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Gross value 1,168.9 117.8 2,249.0 2,550.4 6,086.1» |
| L24_bruto | valor bruto a 31-dic-2024; artículos de alquiler | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «Gross value 1,055.4 129.6 2,078.6 3,096.5 6,360.1» |
| L24_vnc | valor neto contable a 31-dic-2024; artículos de alquiler | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «NET CARRYING AMOUNT AS AT DECEMBER 31, 2024 640.3 13.0 701.0 1,000.8 2,355.0» |
| L25_vida | vida útil de los artículos de alquiler | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «and depreciated over a period of 18 months to five years» |
| L25_exist | los artículos se registran primero como existencias | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 367] | «recognized as inventories and are then capitalized» |
| L23_inv | inversiones en inmovilizado material (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 313] | «Investissements 41,2 3,4 136,4 621,6 802,6» |
| L23_am | amortización del inmovilizado material (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 313] | «Amortissements de l'exercice (30,7) (6,7) (102,5) (514,8) (654,7)» |
| L22_inv | inversiones en inmovilizado material (2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 319] | «Investments 24.8 3.0 100.1 556.1 684.0» |
| L22_am | amortización del inmovilizado material (2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 319] | «Depreciation (30.2) (8.1) (101.4) (454.3) (594.0)» |
| L21_inv | inversiones en inmovilizado material (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 300] | «Investments 17.2 1.0 95.0 441.9 555.1» |
| L21_am | amortización del inmovilizado material (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 300] | «Depreciation (30.9) (8.5) (99.3) (415.5) (554.2)» |
| R25_tipo | qué arrienda Elis (derechos de uso) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 365] | «lease agreements for a variety of assets including property, vehicles, machines, and other equipment» |
| R25_bc | derechos de uso por combinaciones (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Increase related to business combinations 6.8 1.5 3.4 11.7 12.8» |
| R25_new | nuevos derechos de uso (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «New rights of use 57.1 123.8 2.9 183.9 184.0» |
| R25_rem | reestimaciones de derechos de uso (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Remeasuring of rights of use 42.4 7.1 0.5 50.0 50.0» |
| R25_am | amortización de derechos de uso (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Amortization (54.4) (91.5) (3.6) (149.5) 0.0» |
| R25_pp | pagos de principal (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Principal payments 0.0 0.0 0.0 0.0 (148.3)» |
| R25_fin | derechos de uso y pasivo a 31-dic-2025 | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «AS AT 12/31/2025 376.9 275.6 13.4 665.8 703.2» |
| R24_bc | derechos de uso por combinaciones (2024 reexpresado) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Increase related to business combinations 3.5 0.2 5.3 9.0 9.6» |
| R24_new | nuevos derechos de uso (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «New rights of use 10.4 132.0 3.3 145.7 145.7» |
| R24_rem | reestimaciones (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Remeasuring of rights of use 39.7 0.0 (0.0) 39.6 39.7» |
| R24_am | amortización de derechos de uso (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Amortization (50.0) (79.1) (3.1) (132.2) 0.0» |
| R24_pp | pagos de principal (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 366] | «Principal payments 0.0 0.0 0.0 0.0 (125.0)» |
| R23_bc | derechos de uso por combinaciones (2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 312] | «d'entreprises 1,1 0,3 0,0 1,5 1,5» |
| R23_new | nuevos derechos de uso (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 312] | «Nouveaux droits d'utilisation 26,9 103,4 2,3 132,6 132,6» |
| R23_rem | reestimaciones (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 312] | «Réévaluation des droits d'utilisation 22,1 2,3 0,6 24,9 24,9» |
| R23_am | amortización de derechos de uso (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 312] | «Amortissements de l'exercice (48,2) (64,1) (3,6) (115,9) 0,0» |
| R22_bc | derechos de uso por combinaciones (2022) | 2022 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Increase related to business combinations 18.0 2.3 1.4 21.7 22.8» |
| R22_new | nuevos derechos de uso (2022) | 2022 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «New rights of use 15.6 71.8 3.1 90.4 90.4» |
| R22_rem | reestimaciones (2022) | 2022 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Remeasuring of rights of use 19.0 1.4 (0.7) 19.7 19.7» |
| R22_am | amortización de derechos de uso (2022) | 2022 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Depreciation & amortization / impairment (45.1) (55.0) (3.6) (103.7)» |
| R21_bc | derechos de uso por combinaciones (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Increase related to business combinations 0.6 0.7 0.4 1.7 2.0» |
| R21_new | nuevos derechos de uso (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «New rights of use 17.7 50.8 2.6 71.1 71.1» |
| R21_rem | reestimaciones (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Remeasuring of rights of use 14.3 6.2 0.3 20.8 20.8» |
| R21_am | amortización de derechos de uso (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 302] | «Depreciation & amortization / impairment (41.3) (47.8) (3.5) (92.6)» |
| R23_pp | pagos de principal (2023 y 2022) | 2023 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 279] | «Lease liability payments - principal 6.4 (111.0) (101.5)» |
| R21_pp | pagos de principal (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 261] | «Lease liability payments - principal 6.4 (101.5) (89.4)» |
| R25_pagos | pagos por arrendamientos con intereses (flujos, 2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 327] | «Lease liability payments (including interest on lease liabilities) (177.9) (150.8)» |
| Q25_adq | adquisición de dependientes neta de caja (2025 y 2024) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 327] | «Acquisition of subsidiaries, net of cash acquired 2.4 (117.6) (183.3)» |
| Q23_adq | adquisición de filiales neta de caja (2024 y 2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 273] | «Acquisition de filiales, sous déduction de la trésorerie acquise 2.4 (183,3) (82,1)» |
| Q22_adq | adquisición de dependientes neta de caja (2023 y 2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 279] | «Acquisition of subsidiaries, net of cash acquired 2.4 (82.2) (221.7)» |
| Q21_adq | adquisición de dependientes neta de caja (2022 y 2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 261] | «Acquisition of subsidiaries, net of cash acquired 2.4 (221.6) (86.8)» |
| Q25_vida | vida útil de las relaciones con clientes adquiridas | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «acquired customer contracts and relationships: 4 to 14 years» |
| Q25_cr_bc | altas por combinaciones; columna relaciones con clientes (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «Acquisitions through business combinations 0.4 3.7 0.7 4.8» |
| Q25_cr_am | amortización; columna relaciones con clientes (2025) | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «Amortization (2.2) (83.5) (23.7) (109.4)» |
| Q25_cr_vnc | valor neto a 31-dic-2025; relaciones con clientes | 2025 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «NET CARRYING AMOUNT AS AT DECEMBER 31, 2025 209.8 275.1 88.7 573.6» |
| Q24_cr_bc | altas por combinaciones; relaciones con clientes (2024 reexpresado) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «Acquisitions through business combinations 1.1 32.3 0.6 34.0» |
| Q24_cr_am | amortización; relaciones con clientes (2024) | 2024 | Elis - 2025 Universal Registration Document.txt | [PDF PAGE 364] | «Amortization (1.1) (83.9) (22.7) (107.7)» |
| Q23_cr_bc | altas por combinaciones; relaciones con clientes (2023 reexpresado) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 310] | «Acquisitions par voie de regroupements d'entreprises 0,0 20,6 0,0 20,7» |
| Q23_cr_am | amortización; relaciones con clientes (2023) | 2023 | Elis_Document d'enregistrement universel_2024_FR.txt | [PDF PAGE 310] | «Amortissements de l'exercice (1,2) (84,6) (21,6) (107,4)» |
| Q22_cr_bc | altas por combinaciones; relaciones con clientes (2022 reexpresado) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 317] | «Acquisitions through business combinations 3.9 88.0 0.1 91.9» |
| Q22_cr_am | amortización; relaciones con clientes (2022) | 2022 | Elis_Universal Registration Document_2023_EN.txt | [PDF PAGE 317] | «Depreciation (2.0) (80.9) (18.9) (101.9)» |
| Q21_cr_bc | altas por combinaciones; relaciones con clientes (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 299] | «Acquisitions through business combinations - 21.1 0.7 21.8» |
| Q21_cr_am | amortización; relaciones con clientes (2021) | 2021 | Elis - 2022 Universal Registration Document.txt | [PDF PAGE 299] | «Depreciation (3.0) (78.2) (17.5) (98.7)» |
