# Motor A · perímetro F1 · F1-IMPL 1 (4.15 · decisiones F1 del 17-nov-2026)

Libro `d2593777650f1d9d…` · declaración `2a7c641cea51b56a…` · 2026-11-17

**DIAGNÓSTICO F1 · el resultado del motor A no se usa para una conclusión: F1-2i, F1-K3b, F1-K3c, F1-LIBRO, F1-PARAM, F1-REGISTRO, V-F1a, V-F1g, V-F1i, V-F1j, V-F1k, V-F1l**

Estado propuesto: pendiente_de_datos · apto para dinero real: no.

## Guardas

| Id | Salta | Severidad | Efecto | Decisión | Detalle |
|---|---|---|---|---|---|
| F1-NORMA | no | — | — | generalidad | NIIF declarada; libro: IFRS (adoptadas por la Unión Europea) |
| F1-REGISTRO | sí | BLOQUEA | INCOMPLETO | E2 (registro de cada declaración) | norma_contable sin registro (fecha, persona, motivo) |
| V-F1e | no | — | — | (1a) | invariantes de E1 y signos declarados: conformes |
| F1-REGISTRO | sí | BLOQUEA | INCOMPLETO | E2 (registro de cada declaración) | perimetro_reinversion sin registro (fecha, persona, motivo): es una decisión, no la rellena el agente |
| V-F1b | no | — | — | (1a) | D&A ROU declarada en la ventana o C49 = 0 |
| V-F1a | sí | BLOQUEA | MODELO NO APLICABLE | (1a) | coste de arrendamiento contado dos veces en la proyección: D&A ROU de la ventana 397.5 > 0 y C49 = 128.1 > 0, con perímetro A0 (sin umbral adoptado: bloquea con cualquier importe) |
| V-F1m | no | — | — | (1a) | no salta |
| F1-M-SIM | no | — | — | (1a) · simétrica de V-F1m | no salta |
| F1-ROU-HISTORIA | no | — | — | (1a) | sin conflicto entre la ROU declarada y las filas 17 y 23 de la Historia |
| F1-2i | sí | BLOQUEA | MODELO NO APLICABLE | (2)(i) | perímetro A0_total con PPA 256.4 > 0 en la ventana: trata la amortización PPA como reposición, contra la política (2)(i) aprobada; la combinación no está cubierta por las decisiones (no se resuelve aquí) |
| V-F1l | sí | BLOQUEA | INCOMPLETO | (5a) | N1 exige el margen objetivo declarado sin esos ajustes (condición de 5a): sin declarar |
| F1-PARAM | sí | BLOQUEA | INCOMPLETO | (5a) opciones sin decidir | alcance de N1 a los ejercicios del τ fuera de la ventana sin decisión adoptada (declarados fuera de la ventana: [2021, 2022]); no se elige por omisión; se calculan las variantes · actualización financiera del earnout (N1 alcanza o no el BAI que da el tipo): sin decisión adoptada; o se declara expresamente que no existe (actualizacion_financiera_earnout_declarada: false) |
| V-F1j | sí | BLOQUEA | INCOMPLETO | (4b) | clasificación de las compras de sociedades pendiente (opción A de 4b, hasta M6) |
| V-F1i | sí | BLOQUEA | INCOMPLETO | (5b) | transición conocida con su tratamiento pendiente (sin importe ni horizonte la conclusión queda pendiente; nunca cero por defecto) |
| V-F1d | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1c | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1h | no | — | — | (2) | margen EBIT_NIIF16_PPA_constante coherente con A0_total |
| V-F1g | sí | BLOQUEA | MODELO NO APLICABLE | (4a) | perímetro de las palancas S2C sin declarar |
| V-F1k | sí | BLOQUEA | MODELO NO APLICABLE | (4a) | perímetro del ROIC del terminal sin declarar |
| F1-REPLICA | no | — | — | T1/T7 | la réplica A0 reproduce el libro (f, τ, m0, ancla y flujos): la capa F1 y el libro son el mismo motor |
| F1-K3a | no | — | — | K3 | caja base por dos vías: cada diferencia entre C70 y la fila 35 está explicada por una partida declarada |
| F1-K3b | sí | BLOQUEA | MODELO NO APLICABLE | K3 | alquiler contado dos veces en la proyección con el perímetro A0_total (debe contarse una vez) |
| F1-K3c | sí | BLOQUEA | INCOMPLETO | K3 | reinversión media de la ventana -81.200 < 0 con ventas que no bajan: D_X devuelve más amortización de la que el capex repuso · sin justificación |
| F1-LIBRO | sí | BLOQUEA | MODELO NO APLICABLE | (1a) · implantación | LÍMITE DECLARADO · el libro V6.3 calcula el perímetro A0 sin normalizar y sin términos explícitos; con A0_total y N1; flujos del perímetro declarado distintos de los del Motor en 33 celdas: su valor no corresponde a la declaración; la conclusión del motor A no se toma del libro; los flujos F1 son un diagnóstico |
| V-F1k (salto del terminal) | no | — | — | (4a) | /salto/ ≤ C179 en los tres escenarios: informa (no acredita coherencia) |
| V-F1f | no | — | — | (2) | {"PPA: media ÷ ventas medias (lo que devuelve f en A2)": 0.018743, "PPA: año base ÷ ventas del año base (lo que lleva m0)": 0.017866, "efecto de escala de la PPA en el flujo sin crecimiento de A2 (mm)": 4.206, "ROU: media ÷ ventas medias (lo que devuelve f en A1 y A2)": 0.029057, "ROU: año base ÷ ventas del año base (lo que lleva m0)": 0.031167, "efecto de escala de la ROU en el flujo sin crecimiento de A1 y A2 (mm)": -10.118, "años de agotamiento de la PPA al ritmo del año base (valor neto ÷ PPA)": 3.21} |

## Flujo sin crecimiento por perímetro (diagnóstico)

| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |
|---|---|---|---|---|
| A0_total | 0.041681455 | 248.496 | +0.000 | 9.03951 |
| A1_sin_ROU | 0.012624225 | 387.878 | +139.382 | 2.445332 |
| A2_propio | -0.006118602 | 477.784 | +229.287 | 1.612524 |
| B_cota_capex | 0.022646228 | 339.805 | +91.308 | 2.651525 |

## K3 · perímetro declarado (A0_total)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 307.933 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 30.405 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -9.613 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -10.634 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | 136.767 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | -132.500 | doble_computo |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | -85.467 | reposicion_no_monetaria |
| **= flujo sin crecimiento** | **236.891** | cuadra |

## K3 · perímetro A0 (lo que calcula el libro)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 307.933 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 39.600 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | -7.965 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -9.872 | explicada |
| + inversión neta propia y circulante de la ventana (capex − D&A propia + circulante) | 136.767 | explicada |
| − amortización ROU que D_X devuelve como reposición, con los pagos de arrendamiento ya dentro del FCF base | -132.500 | doble_computo |
| − amortización PPA que D_X devuelve como reposición (no es caja: política (2)(i)) | -85.467 | reposicion_no_monetaria |
| **= flujo sin crecimiento** | **248.496** | cuadra |

Doble cómputo señalado por K3 en A0: 217.967 mm de media en la ventana; 229.287 a la escala del año base.

## (1b) Sensibilidad al peso del año base

```
{
 "convencion": "media de la ventana (referencia de ensayo y convención declarada; no es una estimación del peso futuro)",
 "pagos_media_%_ventas": 3.3589,
 "pagos_año_base_%_ventas": 3.7087,
 "sensibilidad_pagos_mm (A0, A1 y A2)": -16.778,
 "sensibilidad_amortizacion_ROU_que_devuelve_f_mm (A1 y A2)": 10.118,
 "total_A1_A2_mm": -6.66
}
```

## Parámetros sin valor adoptado

- alcance_n1_ejercicios_tau: sin valor (N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada))
- n1_actualizacion_financiera_earnout: sin valor (N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada))
- umbral_v_f1a: sin valor (PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada))
