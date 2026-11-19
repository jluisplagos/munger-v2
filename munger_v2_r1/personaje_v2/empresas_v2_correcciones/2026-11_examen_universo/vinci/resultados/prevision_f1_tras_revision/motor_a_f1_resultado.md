# Motor A · perímetro F1 · F1-IMPL 2 (4.15 · decisiones F1 del 17-nov-2026 · US GAAP, ASC 842: D-US1, D-US2, D-US2 bis y D-WM del 18-nov-2026 · cierre de la revisión R2 · margen de partida según Palancas C8, 19-nov-2026)

Libro `64623058d3020f5d…` · declaración `fc7d02a4b4583d6d…` · 2026-11-19

**DIAGNÓSTICO F1 · el resultado del motor A no se usa para una conclusión: F1-K3c**

Estado propuesto: pendiente_de_datos · apto para dinero real: no.

## Guardas

| Id | Salta | Severidad | Efecto | Decisión | Detalle |
|---|---|---|---|---|---|
| F1-NORMA | no | — | — | generalidad | NIIF declarada; libro: IFRS |
| V-F1e | no | — | — | (1a) | invariantes de E1 y signos declarados: conformes |
| V-F1b | no | — | — | (1a) | D&A ROU declarada en la ventana o C49 = 0 |
| V-F1a | no | — | — | (1a) | no aplica: el perímetro no es A0 |
| V-F1m | no | — | — | (1a) | no aplica: el perímetro no es A0 |
| F1-M-SIM | no | — | — | (1a) · simétrica de V-F1m | no salta |
| F1-ROU-HISTORIA | no | — | — | (1a) | sin conflicto entre la ROU declarada y las filas 17 y 23 de la Historia |
| F1-2i | no | — | — | (2)(i) | el perímetro no trata la PPA como reposición |
| V-F1l | no | — | — | (5a) | sin ajustes de normalización (el diagnóstico se muestra como diagnóstico) |
| V-F1j | no | — | — | (4b) | compras: crecimiento_por_hipotesis |
| V-F1i | no | — | — | (5b) | sin transición conocida |
| V-F1d | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1c | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1h | no | — | — | (2) | margen EBIT_NIIF16_PPA_constante coherente con A2_propio |
| V-F1g | no | — | — | (4a) | perímetro declarado de las palancas S2C = perímetro de la reinversión (A2_propio): compara etiquetas de la declaración, no cifras; los valores, en «V-F1g (valores)» (P-FOSO, D3) |
| V-F1k | no | — | — | (4a) | perímetro declarado del ROIC del terminal = el de las palancas S2C (A2_propio): compara etiquetas de la declaración, no cifras; los valores, en «V-F1k (valores)» (P-FOSO, D3) |
| F1-REPLICA | no | — | — | T1/T7 | la réplica A0 reproduce el libro (f, τ, m0 = Historia!C48, ancla y flujos): la capa F1 y el libro son el mismo motor |
| F1-K3a | no | — | — | K3 | caja base por dos vías: cada diferencia entre C70 y la fila 35 está explicada por una partida declarada |
| F1-K3b | no | — | — | K3 | alquiler contado una vez |
| F1-K3c | sí | BLOQUEA | INCOMPLETO | K3 | reinversión media de la ventana -1514.333 < 0 con ventas que no bajan: D_X devuelve más amortización de la que el capex repuso · sin justificación |
| F1-LIBRO | no | — | — | (1a) · implantación | el libro V6.3.1 F1 calcula el perímetro declarado (A2_propio): f, ancla, D_X, series y 0 flujos del Motor coinciden con la capa |
| F1-INTERESES-ARR | no | — | — | P-FOSO · C1 | series.intereses_arrendamiento: comprobada |
| V-F1g (valores) | no | — | — | (4a) · P-FOSO | perímetro A2_propio declarado; aún sin palancas (antes de la fase B): las cifras de B16:D16 y B18:D18 no se han medido frente a las medidas del perímetro; se miden cuando existen (gramática tras la fase B y capa F1 en el paso 12) |
| V-F1k (valores) | no | — | — | (4a) · P-FOSO | perímetro A2_propio declarado; aún sin palancas (antes de la fase B): las cifras de B16:D16 y B18:D18 no se han medido frente a las medidas del perímetro; se miden cuando existen (gramática tras la fase B y capa F1 en el paso 12) |
| V-F1f | sí | INFORMA | INFORMA | (2) | {"PPA: media ÷ ventas medias (lo que devuelve f en A2)": 0.001274, "PPA: año base ÷ ventas del año base (lo que lleva m0)": 0.000509, "efecto de escala de la PPA en el flujo sin crecimiento de A2 (mm)": 57.044, "ROU: media ÷ ventas medias (lo que devuelve f en A1 y A2)": 0.010225, "ROU: año base ÷ ventas del año base (lo que lleva m0)": 0.010952, "efecto de escala de la ROU en el flujo sin crecimiento de A1 y A2 (mm)": -54.221} |
| F1-SERIES-CERO | sí | AVISO | PENDIENTE | (1a) · F1-SERIES-ESCALA | CERO SIN CIFRA IMPRESA, PENDIENTE DE REVISOR (no comprobado: el programa solo ha visto que la frase está en la página; no bloquea F1-SERIES y la aptitud por entradas sigue en «no»): series.da_ppa.2021: motivo «PPA de 2021 = 0 por LECTURA, pendiente de revisor: la única amortización de intangibles de combinaciones que VINCI publica por separado es la de Cobra IS, y Cobra IS se adquirió el último día del ejercicio (frase citada, nota A.1 del URD 2021); la nota 4.3 de 2021 (PDF p. 156) no menciona ninguna am»; cita (p. 150 de 'URD2021') «After announcing the agreement on 1 April 2021, VINCI completed its acquisition of ACS’s energy business (Cobra IS) on 31 December 2021.» |
| F1-SERIES | no | — | — | (1a) · H12 · V631-2 | D&A de derechos de uso y PPA: cifra publicada con su signo, como cifra completa, en una página existente de una fuente del expediente con su huella; columna del ejercicio comprobada en 0 años, PENDIENTE en 10 (la aptitud por entradas sigue en «no») |

## Flujo sin crecimiento por perímetro (diagnóstico)

| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |
|---|---|---|---|---|
| A0_total | 0.056397725 | 2158.246 | +0.000 | 21.872385 |
| A1_sin_ROU | 0.046172672 | 2921.025 | +762.779 | 6.452376 |
| A2_propio | 0.044898609 | 3016.069 | +857.823 | 5.959529 |
| B_cota_capex | 0.052928926 | 2417.015 | +258.769 | 9.096578 |

## K3 · perímetro declarado (A2_propio)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 4419.333 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 424.636 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -182.807 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -130.760 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | -1514.333 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | 0.000 | explicada |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | 0.000 | explicada |
| **= flujo sin crecimiento** | **3016.069** | cuadra |

## K3 · perímetro A0 (lo que calcula el libro)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 4419.333 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 424.636 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -182.807 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -164.249 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | -1514.333 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | -733.000 | doble_computo |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | -91.333 | reposicion_no_monetaria |
| **= flujo sin crecimiento** | **2158.246** | cuadra |

Doble cómputo señalado por K3 en A0: 824.333 mm de media en la ventana; 857.823 a la escala del año base.

## Parámetros sin valor adoptado

- alcance_n1_ejercicios_tau: sin valor (N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada))
- n1_actualizacion_financiera_earnout: sin valor (N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada))
- umbral_v_f1a: sin valor (PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada))
