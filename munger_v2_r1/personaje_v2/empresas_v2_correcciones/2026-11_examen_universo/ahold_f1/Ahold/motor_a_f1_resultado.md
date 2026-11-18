# Motor A · perímetro F1 · F1-IMPL 1 (4.15 · decisiones F1 del 17-nov-2026)

Libro `d8b02a523d943b94…` · declaración `e431b19ffa4b3922…` · 2026-11-18

**motor A utilizable para una conclusión según F1 (condición necesaria, no suficiente; no apto para dinero real)**

Estado propuesto: — · apto para dinero real: no.

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
| V-F1g | no | — | — | (4a) | palancas S2C en el mismo perímetro (A2_propio) |
| V-F1k | no | — | — | (4a) | ROIC del terminal en el perímetro de las palancas (A2_propio) |
| F1-REPLICA | no | — | — | T1/T7 | la réplica A0 reproduce el libro (f, τ, m0, ancla y flujos): la capa F1 y el libro son el mismo motor |
| F1-K3a | no | — | — | K3 | caja base por dos vías: cada diferencia entre C70 y la fila 35 está explicada por una partida declarada |
| F1-K3b | no | — | — | K3 | alquiler contado una vez |
| F1-K3c | no | — | — | K3 | reinversión media 79.000 ≥ 0 (o ventas a la baja) |
| F1-LIBRO | no | — | — | (1a) · implantación | el libro V6.3.1 F1 calcula el perímetro declarado (A2_propio): f, ancla, D_X, series y 0 flujos del Motor coinciden con la capa |
| V-F1f | sí | INFORMA | INFORMA | (2) | {"PPA: media ÷ ventas medias (lo que devuelve f en A2)": 0.0002, "PPA: año base ÷ ventas del año base (lo que lleva m0)": 0.000195, "efecto de escala de la PPA en el flujo sin crecimiento de A2 (mm)": 0.44, "ROU: media ÷ ventas medias (lo que devuelve f en A1 y A2)": 0.015046, "ROU: año base ÷ ventas del año base (lo que lleva m0)": 0.015159, "efecto de escala de la ROU en el flujo sin crecimiento de A1 y A2 (mm)": -10.496, "años de agotamiento de la PPA al ritmo del año base (valor neto ÷ PPA)": 27.06} |
| F1-SERIES | no | — | — | (1a) · H12 · V631-2 | D&A de derechos de uso y PPA: cifra publicada con su signo, como cifra completa, en una página existente de una fuente del expediente con su huella; columna del ejercicio comprobada en 5 años, PENDIENTE en 3 (la aptitud por entradas sigue en «no») |

## Flujo sin crecimiento por perímetro (diagnóstico)

| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |
|---|---|---|---|---|
| A0_total | 0.018853521 | 1041.577 | +0.000 | None |
| A1_sin_ROU | 0.003807781 | 2431.081 | +1389.504 | 5.101651 |
| A2_propio | 0.003608107 | 2449.521 | +1407.944 | None |
| B_cota_capex | 0.004114686 | 2402.737 | +1361.161 | 6.266809 |

## K3 · perímetro declarado (A2_propio)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 1999.334 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 380.774 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -1.632 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -7.955 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | 79.000 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | 0.000 | explicada |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | 0.000 | explicada |
| **= flujo sin crecimiento** | **2449.521** | cuadra |

## K3 · perímetro A0 (lo que calcula el libro)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 1999.334 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 380.774 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -1.632 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -41.566 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | 79.000 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | -1356.333 | doble_computo |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | -18.000 | reposicion_no_monetaria |
| **= flujo sin crecimiento** | **1041.577** | cuadra |

Doble cómputo señalado por K3 en A0: 1374.333 mm de media en la ventana; 1407.944 a la escala del año base.

## (1b) Sensibilidad al peso del año base

```
{
 "convencion": "media de la ventana (referencia de ensayo y convención declarada; no es una estimación del peso futuro)",
 "pagos_media_%_ventas": 2.0344,
 "pagos_año_base_%_ventas": 2.105,
 "sensibilidad_pagos_mm (A0, A1 y A2)": -65.147,
 "sensibilidad_amortizacion_ROU_que_devuelve_f_mm (A1 y A2)": 10.496,
 "total_A1_A2_mm": -54.651
}
```

## Parámetros sin valor adoptado

- alcance_n1_ejercicios_tau: sin valor (N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada))
- n1_actualizacion_financiera_earnout: sin valor (N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada))
- umbral_v_f1a: sin valor (PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada))
