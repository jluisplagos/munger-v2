# Contraste independiente F1 · Elis · resultados calculados

Generado por `scripts/contraste_f1.py`. Comprobaciones: 186 (algebraica: 13, fuente: 58, libro: 115), fallidas: 0. Libro contrastado: sí, SHA-256 d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385. Millones de euros salvo indicación.

### Residuos de las conciliaciones anuales (0 = cuadra exactamente; ±0,1 = redondeo de la cifra impresa)

| Identidad | 2023 | 2024 | 2025 |
|---|---|---|---|
| R1 EBIT publicado − (BAI + resultado financiero) | 0.000 | 0.000 | -0.100 |
| R2 EBIT del EFE (BN+impuesto+financiero) − EBIT publicado | 0.000 | 0.100 | 0.000 |
| R3 caja antes de financieros e impuestos − suma de sus líneas | 0.000 | 0.000 | 0.100 |
| R4 CFO − (caja antes − circulante − impuestos pagados) | 0.000 | -0.100 | 0.000 |
| R5 circulante APM − circulante de las líneas del EFE | 0.000 | 0.000 | 0.000 |
| R6 D&A en EBIT − suma de componentes | 0.000 | 0.100 | 0.000 |
| R7 D&A total − (D&A en EBIT + deterioro + PPA) | 0.000 | 0.000 | 0.100 |
| R8 línea EFE amortizaciones y provisiones − (D&A total + subvención + provisiones) | 0.000 | 0.000 | 0.000 |
| R9 capex bruto EFE − capex por tipo (lino + otros artículos + resto) | 0.000 | -0.100 | 0.000 |
| R10 capex neto APM − (capex bruto EFE − cesiones − subvenciones) | 0.100 | 0.000 | 0.000 |
| R11 FCF publicado − suma de sus componentes | 0.100 | -0.200 | 0.000 |
| R12 FCF publicado − (CFO − capex neto − intereses − pagos de arrendamientos) | 0.100 | -0.100 | 0.000 |
| R13 interés implícito de caja (pagos − principal) − gasto devengado | 0.000 | 0.000 | 0.400 |
| R14 pasivo por arrendamiento: final − (inicial + altas − principal + divisa + otros) | 0.000 | 0.000 | 0.000 |
| R15 activo ROU: final − (inicial + altas − amortización − deterioro + divisa + otros) | 0.000 | -0.100 | 0.000 |
| R16 amortización ROU (nota 4.5) − amortización del movimiento de ROU | -0.100 | 0.000 | 0.000 |
| R17 impuesto corriente + diferido − gasto por impuesto | -0.100 | 0.000 | 0.000 |
| R18 SBC no monetario + cargas sociales − gasto IFRS 2 total | 0.000 | 0.000 | 0.000 |
| R19 deuda bruta − caja − deuda neta | 0.000 | 0.100 | 0.000 |

### FCF base por año y media (C46–C52)

| Concepto | 2023 | 2024 | 2025 |
|---|---|---|---|
| CFO | 1 325.600 | 1 452.100 | 1 510.600 |
| capex_neto | 820.800 | 876.000 | 874.700 |
| int_fin | 70.500 | 78.900 | 99.400 |
| int_arr_caja | 19.800 | 25.800 | 29.600 |
| principal_arr | 111.000 | 125.000 | 148.300 |
| sbc | 22.900 | 27.100 | 34.700 |
| fcf_base_via_cfo | 280.600 | 319.300 | 323.900 |
| fcf_base_via_apm | 280.700 | 319.200 | 323.900 |

### Composición económica de las fugas f·ventas (media 2023–25 y por año)

| Componente | Media | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| pagos_arrendamientos_principal | 128.100 | 111.000 | 125.000 | 148.300 |
| pagos_arrendamientos_interes_caja | 25.067 | 19.800 | 25.800 | 29.600 |
| intereses_financieros_netos_pagados | 82.933 | 70.500 | 78.900 | 99.400 |
| impuesto: escudo del gasto financiero (−τ·financiero) | -35.976 | -36.919 | -35.912 | -35.098 |
| impuesto: caja − devengo (pagado − gasto) | 11.067 | 16.100 | -3.400 | 20.500 |
| impuesto: redondeo de τ a 4 decimales (gasto − τ·BAI) | 0.009 | 0.017 | -0.009 | 0.018 |
| capex neto − bruto (cesiones, subvenciones) | -10.000 | -3.100 | -11.400 | -15.500 |
| plusvalías por enajenación (no monetarias en EBIT) | 3.833 | -4.300 | -7.300 | 23.100 |
| earnout y otros no monetarios | -13.000 | -48.400 | 9.300 | 0.100 |
| provisiones (D&A total − línea de amortizaciones y provisiones − subvención) | -1.967 | -8.100 | 2.600 | -0.400 |
| EBIT de la Historia − EBIT del EFE | 0.000 | 0.000 | -0.100 | 0.100 |
| residuos de redondeo del EFE publicado (−R3 − R4) | 0.000 | 0.000 | 0.100 | -0.100 |
| TOTAL = C79 | 190.066 | 116.598 | 183.579 | 270.020 |

### Puente FCF base → flujo sin crecimiento del motor A (base 2025)

| Paso | mm |
|---|---|
| FCF base (C52 registrado) | 307.933 |
| + nivel del EBIT 2025 frente a la media 2023–25, al τ de 5 años | 39.600 |
| + cambio de tipo: τ de 5 años frente a τ de cada año en la ventana | -7.965 |
| − f aplicada a las ventas 2025 frente a las ventas medias | -9.872 |
| + reinversión histórica media que el motor no proyecta (C76) | -81.200 |
| = flujo sin crecimiento del motor (V0·[m0(1−τ) − f]) | 248.496 |

### Descomposición de la reinversión media 2023–25 (C76)

| Bloque | mm |
|---|---|
| lino: compras − amortización | 62.667 |
| otros artículos en alquiler: compras − amortización | 2.800 |
| resto de inmovilizado e intangibles: compras − amortización | 66.133 |
| subvenciones imputadas (+) y deterioros (−) | -0.333 |
| residuo de redondeo (capex EFE − por tipo; D&A total − componentes) | -0.100 |
| circulante | 5.600 |
| − amortización de derechos de uso NIIF 16 | -132.500 |
| − amortización de intangibles de combinaciones (PPA) | -85.467 |
| TOTAL = C76 | -81.200 |

### Puente flujo sin crecimiento → año 1 · MALO

| Paso | mm |
|---|---|
| flujo sin crecimiento | 248.496 |
| + NOPAT adicional por ventas y margen del año 1 | -9.376 |
| − f sobre el aumento de ventas | -3.999 |
| − reinversión de crecimiento ΔV/S2C | -95.936 |
| = flujo del año 1 | 139.185 |

### Puente flujo sin crecimiento → año 1 · NORMAL

| Paso | mm |
|---|---|
| flujo sin crecimiento | 248.496 |
| + NOPAT adicional por ventas y margen del año 1 | 15.657 |
| − f sobre el aumento de ventas | -8.997 |
| − reinversión de crecimiento ΔV/S2C | -179.880 |
| = flujo del año 1 | 75.276 |

### Puente flujo sin crecimiento → año 1 · BUENO

| Paso | mm |
|---|---|
| flujo sin crecimiento | 248.496 |
| + NOPAT adicional por ventas y margen del año 1 | 27.302 |
| − f sobre el aumento de ventas | -10.997 |
| − reinversión de crecimiento ΔV/S2C | -175.883 |
| = flujo del año 1 | 88.920 |

### Arrendamientos por año

| Concepto | 2023 | 2024 | 2025 |
|---|---|---|---|
| pagos_totales_caja | 130.800 | 150.800 | 177.900 |
| principal | 111.000 | 125.000 | 148.300 |
| interes_implicito_caja | 19.800 | 25.800 | 29.600 |
| interes_devengado_nota_8_2 | 19.800 | 25.800 | 29.200 |
| diferencia_caja_devengo | 0.000 | 0.000 | 0.400 |
| amortizacion_ROU | 115.800 | 132.200 | 149.500 |
| altas_no_monetarias_ROU (nuevas + reestimaciones + combinaciones) | 159.000 | 194.300 | 245.600 |
| pasivo_final | 538.300 | 606.200 | 703.200 |
| variacion_pasivo | 52.900 | 67.900 | 97.000 |
| amortizacion_ROU_sobre_ventas_% | 2.687 | 2.890 | 3.117 |
| pagos_sobre_ventas_% | 3.035 | 3.297 | 3.709 |

### Dónde queda el coste de arrendamiento

| Elemento | mm |
|---|---|
| calibración: amortización ROU dentro del EBIT (NOPAT) | -132.500 |
| calibración: amortización ROU devuelta por la reinversión (− D&A total) | 132.500 |
| calibración: pagos de arrendamiento dentro del FCF base (C48 + C49) | -153.167 |
| calibración: coste neto de arrendamiento reconocido en la historia | -153.167 |
| proyección (base 2025): amortización ROU dentro de m0 | -149.500 |
| proyección (base 2025): pagos de arrendamiento dentro de f·V0 | -161.122 |
| proyección: devolución de la amortización ROU por la reinversión | 0.000 |
| proyección (base 2025): coste de arrendamiento total cargado | -310.622 |

### Alternativas de perímetro de la reinversión necesaria (consecuencias calculadas; ninguna adoptada)

| Magnitud | A0 V6.3 actual | A1 sin derechos de uso | A2 perímetro propio | B cota | A1′ arrendamientos como deuda renovada |
|---|---|---|---|---|---|
| reinversion_necesaria_media_2023_25 | 953.967 | 821.467 | 736.000 | 867.167 | 953.967 |
| inversion_neta_de_crecimiento_media (capex − necesaria + circulante) | -81.200 | 51.300 | 136.767 | 5.600 | -81.200 |
| fugas_f_por_ventas_mm | 190.066 | 57.566 | -27.901 | 103.266 | 61.966 |
| f | 0.042 | 0.013 | -0.006 | 0.023 | 0.014 |
| flujo_sin_crecimiento_base_2025 | 248.496 | 387.878 | 477.784 | 339.805 | 383.250 |
| diferencia_frente_a_A0 | 0.000 | 139.382 | 229.287 | 91.308 | 134.753 |
| reinversion_necesaria_implicita_en_proyeccion_base_2025 | 1 003.513 | 864.132 | 774.226 | 912.205 | 1 003.513 |
| necesaria_menos_capex_medio_2023_25 | 86.800 | -45.700 | -131.167 | 0.000 | 86.800 |
| S2C_total_2021_25 (ΔV 2020→2025 ÷ Σ reinversión + adquisiciones) | 9.040 | 2.445 | 1.613 | 2.651 |  |
| S2C_organico_2023_25 (Σ crecimiento orgánico ÷ Σ inversión neta propia) |  | 5.515 | 2.069 | 50.521 |  |
| S2C_organico_2021_25 |  | 13.850 | 3.125 | 28.658 |  |

### Palanca S2C anclada en el C53 de cada perímetro (escenario NORMAL; revisión O4)

| Magnitud | A0 | A1 | A2 |
|---|---|---|---|
| S2C_ancla_C53 | 9.040 | 2.445 | 1.613 |
| f | 0.042 | 0.013 | -0.006 |
| flujo_sin_crecimiento | 248.496 | 387.878 | 477.784 |
| flujo_año_1_NORMAL_con_S2C_ancla | 231.277 | 312.538 | 360.899 |
| brecha_frente_a_A0_sin_crecimiento |  | 139.382 | 229.287 |
| brecha_frente_a_A0_año_1 |  | 81.260 | 129.622 |
| aumento_de_ventas_que_anula_la_brecha |  | 517.648 | 496.594 |

### Partidas puntuales dentro del flujo sin crecimiento (revisión O9)

| Partida | mm |
|---|---|
| earnout y otros no monetarios dentro de f | 13.675 |
| plusvalías netas de la ventana dentro de f | -4.032 |
| resultado por bajas de inmovilizado 2025 (+25,7 en OOIE) dentro de m0, después de τ | 18.293 |
| efecto neto común a todos los perímetros | 27.936 |

### Tendencia de los arrendamientos frente a la razón constante de f (revisión O10)

| Magnitud | mm |
|---|---|
| pagos_medios_escalados_a_2025 (f) | 161.122 |
| pagos_2025 | 177.900 |
| diferencia_pagos_2025_menos_escalados | 16.778 |
| amortizacion_ROU_2025_en_m0 | 149.500 |
| amortizacion_ROU_media_escalada_devuelta_en_A1_A2 | 139.382 |
| ROU_2025_no_devuelta_en_A1_A2 | 10.118 |

### Materialidad (porcentaje sobre las ventas del mismo período: medias 2023–25 o 2025)

| Partida | mm | % FCF base (C52) | % ventas del período |
|---|---|---|---|
| amortización ROU media 2023–25 | 132.500 | 43.030 | 2.906 |
| amortización ROU 2025 | 149.500 | 48.550 | 3.117 |
| amortización PPA media 2023–25 | 85.467 | 27.750 | 1.874 |
| amortización PPA 2025 | 85.700 | 27.830 | 1.787 |
| capex bruto − D&A propia media 2023–25 | 131.167 | 42.600 | 2.876 |
| capex bruto − D&A propia 2025 | 106.000 | 34.420 | 2.210 |
| D&A total − capex bruto media 2023–25 | 86.800 | 28.190 | 1.904 |

### Impuestos

| Concepto | 2023 | 2024 | 2025 |
|---|---|---|---|
| tau_fila10 | 0.296 | 0.275 | 0.256 |
| EBIT_historia | 496.800 | 596.300 | 630.000 |
| impuesto_nocional_tau_EBIT | 147.202 | 164.221 | 161.280 |
| gasto_por_impuesto | 110.300 | 128.300 | 126.200 |
| corriente | 120.300 | 127.700 | 147.200 |
| diferido | -10.100 | 0.600 | -21.000 |
| pagado | 126.400 | 124.900 | 146.700 |
| escudo_gasto_financiero_tau_fin | 36.919 | 35.912 | 35.098 |
| CVAE_IRAP_incluido | 4.600 | 3.500 | 3.700 |
| pagado_menos_nocional | -20.802 | -39.321 | -14.580 |
| diferido_intangibles_(ingreso; PPA no deducible en caja) | 15.500 | 20.300 | 17.500 |
| diferido_ROU_+_pasivos_arrendamiento | -0.400 | 2.300 | 1.700 |
| tau_por_PPA_(escudo nocional dentro del NOPAT) | 25.393 | 23.409 | 21.939 |

### Demostración sintética (τ = 0, sin crecimiento): flujo del motor frente al FCF verdadero

| Magnitud | solo arrendamientos | arrendamientos y PPA |
|---|---|---|
| FCF verdadero | 68.000 | 68.000 |
| motor sin crecimiento · A0 (D&A total) | 58.000 | 53.000 |
| motor sin crecimiento · A1 (sin ROU) | 68.000 | 63.000 |
| motor sin crecimiento · A2 (propia) | 68.000 | 68.000 |

### Financiación y accionista

| Concepto | 2023 | 2024 | 2025 |
|---|---|---|---|
| FCF publicado | 303.600 | 346.300 | 358.600 |
| FCF base del año (vía CFO) | 280.600 | 319.300 | 323.900 |
| adquisiciones | 82.100 | 183.300 | 117.600 |
| dividendos | 61.700 | 101.300 | 105.100 |
| recompras netas de ampliaciones | -9.100 | -8.200 | 139.000 |
| emisión neta de deuda (EFE) | 208.900 | -95.800 | -210.600 |
| deuda financiera neta final | 3 025.400 | 3 038.000 | 3 020.200 |
| pasivo por arrendamientos final | 538.300 | 606.200 | 703.200 |
| OCEANE (componente de deuda) | 343.100 | 352.300 | 362.000 |

### Horizonte 2021–2025 (S2C)

| Concepto | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| ventas | 3 048.300 | 3 820.900 | 4 309.400 | 4 573.700 | 4 796.800 |
| crecimiento_organico_% | 7.400 | 21.000 | 11.800 | 5.200 | 3.800 |
| capex_bruto | 573.900 | 699.800 | 823.900 | 887.400 | 890.200 |
| lino | 406.700 | 518.800 | 584.300 | 594.300 | 594.200 |
| otros_articulos | 32.600 | 37.300 | 37.300 | 34.600 | 40.800 |
| resto | 134.600 | 143.700 | 202.300 | 258.600 | 255.200 |
| D&A_total | 744.800 | 799.000 | 877.400 | 965.100 | 1 019.400 |
| D&A_ROU | 92.600 | 103.700 | 115.800 | 132.200 | 149.500 |
| D&A_PPA | 81.100 | 82.900 | 85.700 | 85.000 | 85.700 |
| D&A_propia | 571.100 | 612.400 | 675.900 | 747.900 | 784.200 |
| circulante | -10.200 | 52.600 | 5.900 | 6.900 | 4.000 |
| adquisiciones | 86.800 | 221.700 | 82.100 | 183.300 | 117.600 |
| fila30_capex−D&A+circulante | -181.100 | -46.600 | -47.600 | -70.800 | -125.200 |
| capex−D&A_propia+circulante | -7.400 | 140.000 | 153.900 | 146.400 | 110.000 |
| lino_compras−amortizacion | 19.800 | 94.800 | 102.200 | 56.700 | 29.100 |

### Comprobaciones

- OK · [fuente] residuo R1 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R2 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R3 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R4 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R5 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R6 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R7 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R8 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R9 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R10 2023 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R11 2023 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R12 2023 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R13 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R14 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R15 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R16 2023 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R17 2023 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R18 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R19 2023 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R1 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R2 2024 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R3 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R4 2024 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R5 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R6 2024 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R7 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R8 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R9 2024 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R10 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R11 2024 dentro de tolerancia: -0.2 frente a 0.0 (dif. -0.2; tol. 0.25)
- OK · [fuente] residuo R12 2024 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R13 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R14 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R15 2024 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R16 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R17 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R18 2024 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R19 2024 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R1 2025 dentro de tolerancia: -0.1 frente a 0.0 (dif. -0.1; tol. 0.15)
- OK · [fuente] residuo R2 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R3 2025 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R4 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R5 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R6 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R7 2025 dentro de tolerancia: 0.1 frente a 0.0 (dif. 0.1; tol. 0.15)
- OK · [fuente] residuo R8 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R9 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R10 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R11 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R12 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R13 2025 dentro de tolerancia: 0.4 frente a 0.0 (dif. 0.4; tol. 0.45)
- OK · [fuente] residuo R14 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R15 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R16 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R17 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R18 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] residuo R19 2025 dentro de tolerancia: 0.0 frente a 0.0 (dif. 0.0; tol. 0.15)
- OK · [fuente] C52 vía CFO = vía FCF publicado − SBC: 307.933333 frente a 307.933333 (dif. 0.0; tol. 0.0)
- OK · [libro] Análisis!C46 libro = fuente (exacto a 3 decimales registrados): 1429.433333 frente a 1429.433 (dif. 0.000333333; tol. 0.001)
- OK · [libro] Análisis!C47 libro = fuente (exacto a 3 decimales registrados): 857.166667 frente a 857.167 (dif. -0.000333333; tol. 0.001)
- OK · [libro] Análisis!C48 libro = fuente (exacto a 3 decimales registrados): 108.0 frente a 108.0 (dif. 0.0; tol. 0.001)
- OK · [libro] Análisis!C49 libro = fuente (exacto a 3 decimales registrados): 128.1 frente a 128.1 (dif. 0.0; tol. 0.001)
- OK · [libro] Análisis!C50 libro = fuente (exacto a 3 decimales registrados): 28.233333 frente a 28.233 (dif. 0.000333333; tol. 0.001)
- OK · [libro] Análisis!C52 libro = fuente (exacto a 3 decimales registrados): 307.933333 frente a 307.933 (dif. 0.000333333; tol. 0.001)
- OK · [libro] Historia!H6 (2021) libro = fuente: 3048.3 frente a 3048.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H7 (2021) libro = fuente: 261.5 frente a 261.5 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H8 (2021) libro = fuente: 744.8 frente a 744.8 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H10 (2021) libro = fuente: 0.331 frente a 0.331 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H11 (2021) libro = fuente: 961.6 frente a 961.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H12 (2021) libro = fuente: 573.9 frente a 573.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H13 (2021) libro = fuente: 86.8 frente a 86.8 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H14 (2021) libro = fuente: -10.2 frente a -10.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H17 (2021) libro = fuente: 89.4 frente a 89.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H18 (2021) libro = fuente: 28.0 frente a 28.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!H15 (2021) libro = fuente: 74.6 frente a 74.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I6 (2022) libro = fuente: 3820.9 frente a 3820.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I7 (2022) libro = fuente: 369.0 frente a 369.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I8 (2022) libro = fuente: 799.0 frente a 799.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I10 (2022) libro = fuente: 0.2823 frente a 0.2823 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I11 (2022) libro = fuente: 1091.2 frente a 1091.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I12 (2022) libro = fuente: 699.8 frente a 699.8 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I13 (2022) libro = fuente: 221.7 frente a 221.7 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I14 (2022) libro = fuente: 52.6 frente a 52.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I17 (2022) libro = fuente: 101.5 frente a 101.5 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I18 (2022) libro = fuente: 20.3 frente a 20.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!I15 (2022) libro = fuente: 72.9 frente a 72.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J6 (2023) libro = fuente: 4309.4 frente a 4309.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J7 (2023) libro = fuente: 496.8 frente a 496.8 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J8 (2023) libro = fuente: 877.4 frente a 877.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J10 (2023) libro = fuente: 0.2963 frente a 0.2963 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J11 (2023) libro = fuente: 1325.6 frente a 1325.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J12 (2023) libro = fuente: 823.9 frente a 823.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J13 (2023) libro = fuente: 82.1 frente a 82.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J14 (2023) libro = fuente: 5.9 frente a 5.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J17 (2023) libro = fuente: 111.0 frente a 111.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J18 (2023) libro = fuente: 22.9 frente a 22.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J15 (2023) libro = fuente: 70.5 frente a 70.5 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J22 (2023) libro = fuente: 3690.7 frente a 3690.7 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J23 (2023) libro = fuente: 538.3 frente a 538.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!J24 (2023) libro = fuente: 665.3 frente a 665.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K6 (2024) libro = fuente: 4573.7 frente a 4573.7 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K7 (2024) libro = fuente: 596.3 frente a 596.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K8 (2024) libro = fuente: 965.1 frente a 965.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K10 (2024) libro = fuente: 0.2754 frente a 0.2754 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K11 (2024) libro = fuente: 1452.1 frente a 1452.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K12 (2024) libro = fuente: 887.4 frente a 887.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K13 (2024) libro = fuente: 183.3 frente a 183.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K14 (2024) libro = fuente: 6.9 frente a 6.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K17 (2024) libro = fuente: 125.0 frente a 125.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K18 (2024) libro = fuente: 27.1 frente a 27.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K15 (2024) libro = fuente: 78.9 frente a 78.9 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K22 (2024) libro = fuente: 3660.1 frente a 3660.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K23 (2024) libro = fuente: 606.2 frente a 606.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!K24 (2024) libro = fuente: 622.0 frente a 622.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L6 (2025) libro = fuente: 4796.8 frente a 4796.8 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L7 (2025) libro = fuente: 630.0 frente a 630.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L8 (2025) libro = fuente: 1019.4 frente a 1019.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L10 (2025) libro = fuente: 0.256 frente a 0.256 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L11 (2025) libro = fuente: 1510.6 frente a 1510.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L12 (2025) libro = fuente: 890.2 frente a 890.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L13 (2025) libro = fuente: 117.6 frente a 117.6 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L14 (2025) libro = fuente: 4.0 frente a 4.0 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L17 (2025) libro = fuente: 148.3 frente a 148.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L18 (2025) libro = fuente: 34.7 frente a 34.7 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L15 (2025) libro = fuente: 99.4 frente a 99.4 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L22 (2025) libro = fuente: 3418.3 frente a 3418.3 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L23 (2025) libro = fuente: 703.2 frente a 703.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!L24 (2025) libro = fuente: 398.1 frente a 398.1 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!G6 (2020) libro = fuente: 2806.3 frente a 2806.3 (dif. 0.0; tol. 0.0)
- OK · [algebraica] descomposición económica de f·ventas 2023 = definición de la plantilla: 116.59816 frente a 116.59816 (dif. 0.0; tol. 0.0)
- OK · [algebraica] descomposición económica de f·ventas 2024 = definición de la plantilla: 183.57898 frente a 183.57898 (dif. 0.0; tol. 0.0)
- OK · [algebraica] descomposición económica de f·ventas 2025 = definición de la plantilla: 270.02 frente a 270.02 (dif. 0.0; tol. 0.0)
- OK · [algebraica] descomposición media de f·ventas = C79: 190.065713 frente a 190.065713 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!C74 libro = cálculo independiente: 4559.966667 frente a 4559.966667 (dif. -0.0; tol. 0.0)
- OK · [libro] Historia!C75 libro = cálculo independiente: 416.799047 frente a 416.799047 (dif. -0.0; tol. 0.0)
- OK · [libro] Historia!C76 libro = cálculo independiente: -81.2 frente a -81.2 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!C70 libro = cálculo independiente: 307.933 frente a 307.933 (dif. 0.0; tol. 0.0)
- OK · [libro] Historia!C79 libro = cálculo independiente: 190.066047 frente a 190.066047 (dif. -0.0; tol. 0.0)
- OK · [libro] Historia!C58 libro = cálculo independiente: 0.041681 frente a 0.041681 (dif. -0.0; tol. 0.0)
- OK · [libro] Historia!C52 (τ 5 años) libro = fuente: 0.2882 frente a 0.2882 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AU6 flujo año 1 MALO: réplica = libro: 139.185426 frente a 139.185426 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AV6 flujo año 2 MALO: réplica = libro: 123.25734 frente a 123.25734 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AW6 flujo año 3 MALO: réplica = libro: 106.636456 frente a 106.636456 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AX6 flujo año 4 MALO: réplica = libro: 89.301434 frente a 89.301434 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!AY6 flujo año 5 MALO: réplica = libro: 71.230357 frente a 71.230357 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AZ6 flujo año 6 MALO: réplica = libro: 82.896924 frente a 82.896924 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BA6 flujo año 7 MALO: réplica = libro: 94.815385 frente a 94.815385 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BB6 flujo año 8 MALO: réplica = libro: 106.925568 frente a 106.925568 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BC6 flujo año 9 MALO: réplica = libro: 119.163966 frente a 119.163966 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BD6 flujo año 10 MALO: réplica = libro: 131.464272 frente a 131.464272 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BF6 flujo año 11 MALO: réplica = libro: 128.3293 frente a 128.3293 (dif. 0.0; tol. 0.0)
- OK · [libro] (Motor!BL6 − exceso de caja)·r = flujo sin crecimiento MALO: 248.496395 frente a 248.496395 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AU7 flujo año 1 NORMAL: réplica = libro: 75.276241 frente a 75.276241 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!AV7 flujo año 2 NORMAL: réplica = libro: 73.937667 frente a 73.937667 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AW7 flujo año 3 NORMAL: réplica = libro: 72.326187 frente a 72.326187 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!AX7 flujo año 4 NORMAL: réplica = libro: 70.41995 frente a 70.41995 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AY7 flujo año 5 NORMAL: réplica = libro: 68.195692 frente a 68.195692 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!AZ7 flujo año 6 NORMAL: réplica = libro: 94.757991 frente a 94.757991 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BA7 flujo año 7 NORMAL: réplica = libro: 122.981544 frente a 122.981544 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BB7 flujo año 8 NORMAL: réplica = libro: 152.574294 frente a 152.574294 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BC7 flujo año 9 NORMAL: réplica = libro: 183.198571 frente a 183.198571 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BD7 flujo año 10 NORMAL: réplica = libro: 214.476759 frente a 214.476759 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!BF7 flujo año 11 NORMAL: réplica = libro: 208.482102 frente a 208.482102 (dif. -0.0; tol. 0.0)
- OK · [libro] (Motor!BL7 − exceso de caja)·r = flujo sin crecimiento NORMAL: 248.496395 frente a 248.496395 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AU8 flujo año 1 BUENO: réplica = libro: 88.919565 frente a 88.919565 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!AV8 flujo año 2 BUENO: réplica = libro: 96.593795 frente a 96.593795 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AW8 flujo año 3 BUENO: réplica = libro: 104.843208 frente a 104.843208 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AX8 flujo año 4 BUENO: réplica = libro: 113.707861 frente a 113.707861 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AY8 flujo año 5 BUENO: réplica = libro: 123.230475 frente a 123.230475 (dif. 0.0; tol. 0.0)
- OK · [libro] Motor!AZ8 flujo año 6 BUENO: réplica = libro: 153.038344 frente a 153.038344 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BA8 flujo año 7 BUENO: réplica = libro: 184.695896 frente a 184.695896 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BB8 flujo año 8 BUENO: réplica = libro: 217.835316 frente a 217.835316 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BC8 flujo año 9 BUENO: réplica = libro: 252.025025 frente a 252.025025 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BD8 flujo año 10 BUENO: réplica = libro: 286.777628 frente a 286.777628 (dif. -0.0; tol. 0.0)
- OK · [libro] Motor!BF8 flujo año 11 BUENO: réplica = libro: 264.983257 frente a 264.983257 (dif. 0.0; tol. 0.0)
- OK · [libro] (Motor!BL8 − exceso de caja)·r = flujo sin crecimiento BUENO: 248.496395 frente a 248.496395 (dif. 0.0; tol. 0.0)
- OK · [algebraica] puente FCF base → flujo sin crecimiento: 248.496395 frente a 248.496395 (dif. 0.0; tol. 0.0)
- OK · [algebraica] descomposición de la reinversión media = C76: -81.2 frente a -81.2 (dif. 0.0; tol. 0.0)
- OK · [algebraica] puente flujo sin crecimiento → año 1 MALO: 139.185426 frente a 139.185426 (dif. 0.0; tol. 0.0)
- OK · [algebraica] puente flujo sin crecimiento → año 1 NORMAL: 75.276241 frente a 75.276241 (dif. 0.0; tol. 0.0)
- OK · [algebraica] puente flujo sin crecimiento → año 1 BUENO: 88.919565 frente a 88.919565 (dif. 0.0; tol. 0.0)
- OK · [libro] S2C total A0 = Historia!C53: 9.0395 frente a 9.03951 (dif. -9.537e-06; tol. 0.0001)
- OK · [algebraica] sintético solo arrendamientos: A2 reproduce el FCF verdadero: 68.0 frente a 68.0 (dif. 0.0; tol. 0.0)
- OK · [algebraica] sintético solo arrendamientos: A0 queda por debajo en ROU + PPA: 10.0 frente a 10.0 (dif. 0.0; tol. 0.0)
- OK · [algebraica] sintético arrendamientos y PPA: A2 reproduce el FCF verdadero: 68.0 frente a 68.0 (dif. 0.0; tol. 0.0)
- OK · [algebraica] sintético arrendamientos y PPA: A0 queda por debajo en ROU + PPA: 15.0 frente a 15.0 (dif. 0.0; tol. 0.0)
