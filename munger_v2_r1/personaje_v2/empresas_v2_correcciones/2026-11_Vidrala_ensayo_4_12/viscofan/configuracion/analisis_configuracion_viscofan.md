# Viscofan · análisis propio de las entradas de la configuración experimental (encargo 4.12 §8)

Base económica 31-dic-2025. Todas las cifras se han buscado en su página (61 de 61 encontradas; tabla al final). Millones de euros salvo que se diga otra cosa. Nada de esto viene de Vidrala; nada se adopta.

## N1 · tipo impositivo (perímetro: actividades continuadas, consolidado; período: 2021–2025, el de la regla heredada)

| Año | Fila del tipo (Historia) | Efectivo (conciliación) | Sin activaciones de bases negativas | Además sin ajustes de años anteriores |
|---|---|---|---|---|
| 2021 | 24.61 % | 24.61 % | 24.61 % | 24.62 % |
| 2022 | 24.14 % | 24.14 % | 24.14 % | 25.06 % |
| 2023 | 16.54 % | 16.54 % | 16.54 % | 20.45 % |
| 2024 | 23.79 % | 23.79 % | 24.99 % | 21.65 % |
| 2025 | 10.09 % | 10.09 % | 20.31 % | 21.51 % |
| **Media** | **19.83 %** (C52, regla heredada) | 19.83 % | **22.12 %** | 22.66 % |

La fila del tipo de la Historia (fase 1) va redondeada a 4 decimales; C52 es su media 2021–2025. Las activaciones de bases imponibles negativas (Estados Unidos: 18,009 en 2025 y 2,493 en 2024) son la causa que da la empresa del 10,1 % de 2025; los ajustes de ejercicios anteriores mezclan signos (−0,011; −1,700; −6,602; +6,905; −2,122) y su media es pequeña. La deducción de 2023 por las subvenciones de ICMS en Brasil no está cuantificada por separado: no se ajusta.
Agregado 2021–2025 (Σ impuesto ÷ Σ resultado antes de impuestos): sin activaciones 22.28 %; además sin ajustes 22.66 %. El activo por impuesto diferido de las bases negativas (26,731 a 31-dic-2025) no entra en el motor B.

## N2 · margen de partida

| Año | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|---|
| Margen EBIT | 21.12 % | 19.90 % | 18.61 % | 15.33 % | 17.86 % | 17.99 % | 15.74 % | 15.07 % | 16.74 % | 16.36 % |

Regla heredada (Palancas C8 «Último año»): 16.36 %. Media 2021–2025: 16.38 %. Diez años (C49): 17.47 %; mínimo 15.07 %, máximo 21.12 %. La regla heredada (Palancas C8 «Último año») da el margen de 2025; el ciclo 2021–2025 da prácticamente lo mismo. En 2025 no hay partidas no recurrentes identificadas de importe material en el resultado de explotación (deterioro y enajenaciones +0,648) y la empresa dice que los cambios de perímetro no tuvieron efecto material en el EBITDA (0,0 p.p.). Las adquisiciones de 2024 y 2025 (Brasil) son 7,213 y 8,948.

## N3 · circulante comercial

- 2025 (balance, p. 21–22): existencias 386,859 + deudores 321,044 − acreedores 103,388 = 604.515 sobre ventas 1251.983 → **48.28 %**.
- 2024 (mismas líneas): 48.04 %. Solo comercial (notas 9 y 14): 46.79 %.
- Conciliación: 321,044 = deudores comerciales 289,733 + administraciones públicas 24,783 + periodificaciones 6,528 (nota 9, p. 70); 103,388 = acreedores comerciales 90,766 + administraciones públicas 12,622 (nota 14, p. 95). Se usan las líneas del balance (como la definición B29:B31 de la plantilla); la lectura solo comercial de las notas baja la razón en 1,5 puntos.

## Capex, amortización y adquisiciones (2021–2025)

| Año | Capex | D&A | de ella, derechos de uso | Capex − D&A | Capex − D&A sin derechos de uso | Capex ÷ D&A | Adquisiciones |
|---|---|---|---|---|---|---|---|
| 2021 | 95.779 | 72.281 | 5.123 | 23.498 | 28.621 | 1.33 | 0.000 |
| 2022 | 115.566 | 78.148 | 5.289 | 37.418 | 42.707 | 1.48 | 0.000 |
| 2023 | 77.126 | 83.713 | 5.293 | -6.587 | -1.294 | 0.92 | 0.000 |
| 2024 | 75.027 | 83.794 | 5.843 | -8.767 | -2.924 | 0.90 | 7.213 |
| 2025 | 80.447 | 85.196 | 5.503 | -4.749 | 0.754 | 0.94 | 8.948 |

Capex ÷ D&A en diez años: 1.16; ventas 2021→2025: +29.17 %. La D&A de la Historia incluye la amortización de los derechos de uso (5,1–5,8 al año), que se repone con arrendamientos (financiación) y no con capex: la plantilla no la separa, así que el «exceso histórico» de la familia Θ (Σ capex − D&A) queda 27,1 por debajo del exceso sobre la amortización que se repone con capex, y la base de la familia Λ (D&A₀) incluye 5,5 que no se reponen con capex. Es un límite de definición de la plantilla, no se corrige en la configuración.

## Bases históricas de «Configuración V6.4» (fórmulas de la plantilla; cartera legado)

B54_DA0 85.196; B55_reinversion_neta 296.489; B56_cartera 0.000; B57_D_hist 296.489; B58_capex_menos_da 40.813; B59_adquisiciones 16.161; B60_exceso 40.813; B61_exceso_medio 8.163; B62_F_hist 56.974; B63_amortizacion_que_se_repone 403.132. S2C histórico (C53) 1.1462.

| θ | Rh | f (SR1, SR2) | f_fija (SRF) | nivel anual |
|---|---|---|---|---|
| 0.0 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| 0.25 | 10.203 | 1.0356 | 0.8209 | 2.041 |
| 0.5 | 20.406 | 1.0739 | 0.6418 | 4.081 |
| 0.75 | 30.610 | 1.1151 | 0.4627 | 6.122 |
| 1.0 | 40.813 | 1.1596 | 0.2837 | 8.163 |

| λ | Rh | f (SR1, SR2) | f_fija (SRF) | requisito anual |
|---|---|---|---|---|
| 1.0 | 0.000 | 1.0000 | 1.0000 | 0.000 |
| 1.05 | 20.157 | 1.0729 | 0.6462 | 4.260 |
| 1.1 | 40.313 | 1.1574 | 0.2924 | 8.520 |
| 1.14 | 56.438 | 1.2351 | 0.0094 | 11.927 |
| 1.15 | 60.470 | 1.2562 | -0.0614 (fuera de [0, 1]: SRF no definida) | 12.779 |
| 1.25 | 100.783 | 1.5150 | -0.7689 (fuera de [0, 1]: SRF no definida) | 21.299 |
| 1.5 | 201.566 | 3.1235 | -2.5379 (fuera de [0, 1]: SRF no definida) | 42.598 |

**Dominios.** Con Λ, SRF deja de estar definida por encima de λ = 1.1413 y f por encima de λ = 1.7355. Con Θ, todo θ en [0, 1] está definido. La inversión fija para crecer de R1 sería negativa si S2C × f > 1 ÷ NWC = 2.071 (S2C > 1.929 con θ = 0,5; > 1.786 con θ = 1).

**Cartera.** cartera de clientes de la combinación de negocios de Brasil: inmaterial (≈0,11 al año); sin cartera identificada en 2021–2024 en esta revisión, la ausencia no confirma ceros: no se usa P0.

## Cifras comprobadas

| Id | Concepto | Ejercicio | Cifra | Fuente |
|---|---|---|---|---|
| T25_bai | resultado antes de impuestos de continuadas | 2025 | «176,254» | AR_2025.txt, PDF p. 109 |
| T25_gasto | gasto por impuesto | 2025 | «17,784» | AR_2025.txt, PDF p. 109 |
| T25_bin | activación de bases imponibles negativas | 2025 | «-18,009» | AR_2025.txt, PDF p. 109 |
| T25_ant | ajustes de ejercicios anteriores y otros | 2025 | «-2,122» | AR_2025.txt, PDF p. 109 |
| T24_bai | resultado antes de impuestos de continuadas | 2024 | «206,438» | AR_2025.txt, PDF p. 109 |
| T24_gasto | gasto por impuesto | 2024 | «49,105» | AR_2025.txt, PDF p. 109 |
| T24_bin | activación de bases imponibles negativas | 2024 | «-2,493» | AR_2025.txt, PDF p. 109 |
| T24_ant | ajustes de ejercicios anteriores y otros | 2024 | «6,905» | AR_2025.txt, PDF p. 109 |
| T25_tipo_navarra | tipo de Navarra de la conciliación | 2025 | «Tax rate at 28%» | AR_2025.txt, PDF p. 109 |
| T25_causa | causa del 10,1 % según la empresa | 2025 | «tax bases in the US worth €18.0 million» | AR_2025.txt, PDF p. 142 |
| T25_10_1 | tipo efectivo de 2025 según la empresa | 2025 | «effective tax rate of 10.1%» | AR_2025.txt, PDF p. 142 |
| T25_impacto | impacto de la activación en resultados | 2025 | «18,009 thousand euros (2,493 thousand euros in 2024)» | AR_2025.txt, PDF p. 108 |
| T25_activo_bin | activo por impuesto diferido por bases imponibles negativas | 2025 | «€26,731 thousand» | AR_2025.txt, PDF p. 105 |
| T23_bai | resultado antes de impuestos de continuadas | 2023 | «168,906» | CF_2024.txt, PDF p. 85 |
| T23_gasto | gasto por impuesto | 2023 | «27,944» | CF_2024.txt, PDF p. 85 |
| T23_ded | deducciones generadas o aplicadas | 2023 | «-12,259» | CF_2024.txt, PDF p. 85 |
| T23_ant | ajustes de ejercicios anteriores y otros | 2023 | «-6,602» | CF_2024.txt, PDF p. 85 |
| T24_ant_cf24 | ajustes de ejercicios anteriores y otros (edición 2024, sin separar las bases negativas) | 2024 | «4,412» | CF_2024.txt, PDF p. 85 |
| T23_icms | deducción de subvenciones de ICMS en Brasil (2023) | 2023 | «subvenciones de ICMS» | CA_2023_es.txt, PDF p. 122 |
| T22_bai | resultado antes de impuestos de continuadas | 2022 | «183,789» | CF_2022_compilacion.txt, PDF p. 74 |
| T22_gasto | gasto por impuesto | 2022 | «44,359» | CF_2022_compilacion.txt, PDF p. 74 |
| T22_ant | ajustes de ejercicios anteriores y otros | 2022 | «-1,700» | CF_2022_compilacion.txt, PDF p. 74 |
| T21_bai | resultado antes de impuestos de continuadas | 2021 | «176,420» | CF_2022_compilacion.txt, PDF p. 74 |
| T21_gasto | gasto por impuesto | 2021 | «43,423» | CF_2022_compilacion.txt, PDF p. 74 |
| T21_ant | ajustes de ejercicios anteriores y otros | 2021 | «-11» | CF_2022_compilacion.txt, PDF p. 74 |
| P25_continuadas | resultado de continuadas = resultado del ejercicio | 2025 | «Profit for the year from continuing operations 158,470 157,333» | AR_2025.txt, PDF p. 23 |
| P23_continuadas | resultado de continuadas = resultado del ejercicio (2024 y 2023) | 2024 | «157,333 140,962» | CF_2024.txt, PDF p. 4 |
| P25_perimetro | cambios de perímetro sin efecto material en el EBITDA según la empresa | 2025 | «changes having no material impact (0.0» | AR_2025.txt, PDF p. 142 |
| P25_deterioro | deterioro y resultado por enajenación de inmovilizado | 2025 | «Impairment and gain/loss on disposal of fixed assets 648» | AR_2025.txt, PDF p. 23 |
| C25_ventas | ventas y prestación de servicios | 2025 | «1,251,983» | AR_2025.txt, PDF p. 23 |
| C24_ventas | ventas y prestación de servicios | 2024 | «1,203,994» | AR_2025.txt, PDF p. 23 |
| C25_exist | existencias (balance) | 2025 | «386,859» | AR_2025.txt, PDF p. 21 |
| C24_exist | existencias (balance) | 2024 | «398,954» | AR_2025.txt, PDF p. 21 |
| C25_deud | deudores comerciales y otras cuentas a cobrar (balance) | 2025 | «321,044» | AR_2025.txt, PDF p. 21 |
| C24_deud | deudores comerciales y otras cuentas a cobrar (balance) | 2024 | «305,643» | AR_2025.txt, PDF p. 21 |
| C25_acre | acreedores comerciales y otras cuentas a pagar (balance) | 2025 | «103,388» | AR_2025.txt, PDF p. 22 |
| C24_acre | acreedores comerciales y otras cuentas a pagar (balance) | 2024 | «126,164» | AR_2025.txt, PDF p. 22 |
| C25_deud_com | total deudores comerciales (nota 9) | 2025 | «Total trade debtors 289,733 279,146» | AR_2025.txt, PDF p. 70 |
| C25_deud_aapp | administraciones públicas deudoras (nota 9) | 2025 | «Public authorities receivable 24,783 20,886» | AR_2025.txt, PDF p. 70 |
| C25_deud_perio | periodificaciones (nota 9) | 2025 | «Accruals 6,528 5,611» | AR_2025.txt, PDF p. 70 |
| C25_acre_com | acreedores comerciales (nota 14) | 2025 | «Trade creditors 90,766 113,091» | AR_2025.txt, PDF p. 95 |
| C25_acre_aapp | administraciones públicas acreedoras (nota 14) | 2025 | «Payables to public authorities 12,622 13,073» | AR_2025.txt, PDF p. 95 |
| A25_intang | amortización de intangibles | 2025 | «-5,737 -4,587» | AR_2025.txt, PDF p. 23 |
| A25_mat | amortización del inmovilizado material | 2025 | «-73,956 -73,364» | AR_2025.txt, PDF p. 23 |
| A25_rou | amortización de derechos de uso | 2025 | «-5,503 -5,843» | AR_2025.txt, PDF p. 23 |
| A25_total | amortización total (flujos) | 2025 | «85,196 83,794» | AR_2025.txt, PDF p. 27 |
| K25_capex | pagos por inmovilizado material e intangible | 2025 | «-80,447 -75,027» | AR_2025.txt, PDF p. 27 |
| K25_adq | adquisición de dependientes neta de caja | 2025 | «-8,948 -7,213» | AR_2025.txt, PDF p. 27 |
| L25_arr | pagos por arrendamientos (derechos de uso) | 2025 | «-5,503 -5,843» | AR_2025.txt, PDF p. 28 |
| A23_intang | amortización de intangibles (2024 y 2023) | 2023 | «-4,587 -4,792» | CF_2024.txt, PDF p. 4 |
| A23_mat | amortización del inmovilizado material (2024 y 2023) | 2023 | «-73,364 -73,628» | CF_2024.txt, PDF p. 4 |
| A23_rou | amortización de derechos de uso (2024 y 2023) | 2023 | «-5,843 -5,293» | CF_2024.txt, PDF p. 4 |
| K23_capex | pagos por inmovilizado (2024 y 2023) | 2023 | «-75,027 -77,126» | CF_2024.txt, PDF p. 9 |
| L23_arr | pagos por arrendamientos (2024 y 2023) | 2023 | «-5,843 -5,296» | CF_2024.txt, PDF p. 9 |
| A22_intang | amortización de intangibles (2022 y 2021) | 2022 | «−4.782 −4.345» | CF_2022_compilacion.txt, PDF p. 21 |
| A22_mat | amortización del inmovilizado material (2022 y 2021) | 2022 | «−68.076 −62.813» | CF_2022_compilacion.txt, PDF p. 21 |
| A22_rou | amortización de derechos de uso (2022 y 2021) | 2022 | «−5.289 −5.123» | CF_2022_compilacion.txt, PDF p. 21 |
| K22_capex | pagos por inmovilizado (2022 y 2021) | 2022 | «−115.566 −95.779» | CF_2022_compilacion.txt, PDF p. 25 |
| L22_arr | pagos por arrendamientos (2022 y 2021) | 2022 | «−5.289 −5.123» | CF_2022_compilacion.txt, PDF p. 25 |
| Q25_cartera | altas de cartera de clientes de la combinación de negocios | 2025 | «customer portfolio (1,294 thousand euros)» | AR_2025.txt, PDF p. 33 |
| Q25_vida | vidas útiles de cartera, marca y know-how | 2025 | «useful lives of 12, 8 and 10 years» | AR_2025.txt, PDF p. 33 |
