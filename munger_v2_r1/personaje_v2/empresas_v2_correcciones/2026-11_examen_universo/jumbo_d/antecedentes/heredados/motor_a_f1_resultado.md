# Motor A · perímetro F1 · F1-IMPL 1 (4.15 · decisiones F1 del 17-nov-2026)

Libro `44bffd9645b2895c…` · declaración `44136fa355b3678a…` · 2026-11-18

**DIAGNÓSTICO F1 · el resultado del motor A no se usa para una conclusión: F1-K3a, F1-NORMA, F1-PERIMETRO, V-F1b, V-F1g, V-F1h, V-F1i, V-F1j, V-F1k**

Estado propuesto: pendiente_de_datos · apto para dinero real: no.

## Guardas

| Id | Salta | Severidad | Efecto | Decisión | Detalle |
|---|---|---|---|---|---|
| F1-NORMA | sí | BLOQUEA | INCOMPLETO | generalidad | norma contable sin declarar en la declaración F1 (entrada obligatoria) |
| V-F1e | no | — | — | (1a) | invariantes de E1 y signos declarados: conformes |
| F1-PERIMETRO | sí | BLOQUEA | INCOMPLETO | (1a) | perimetro_reinversion sin declarar |
| V-F1b | sí | BLOQUEA | INCOMPLETO | (1a) | C49 = 8.569 > 0 y D&A ROU vacía en [2023, 2024, 2025]: vacío no es cero |
| V-F1a | no | — | — | (1a) | no aplica: el perímetro no es A0 |
| V-F1m | no | — | — | (1a) | no aplica: el perímetro no es A0 |
| F1-M-SIM | no | — | — | (1a) · simétrica de V-F1m | no salta |
| F1-ROU-HISTORIA | no | — | — | (1a) | sin conflicto entre la ROU declarada y las filas 17 y 23 de la Historia |
| F1-2i | no | — | — | (2)(i) | el perímetro no trata la PPA como reposición |
| V-F1l | no | — | — | (5a) | sin ajustes de normalización (el diagnóstico se muestra como diagnóstico) |
| V-F1j | sí | BLOQUEA | INCOMPLETO | (4b) | clasificación de las compras de sociedades sin declarar |
| V-F1i | sí | BLOQUEA | INCOMPLETO | (5b) | sin declarar si hay una inversión de transición conocida (publicada o documentada) |
| V-F1d | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1c | no | — | — | (3a) | no aplica: el perímetro no es A3_estimado |
| V-F1h | sí | BLOQUEA | MODELO NO APLICABLE | (2) | perimetro_margen sin declarar |
| V-F1g | sí | BLOQUEA | MODELO NO APLICABLE | (4a) | perímetro de las palancas S2C sin declarar |
| V-F1k | sí | BLOQUEA | MODELO NO APLICABLE | (4a) | perímetro del ROIC del terminal sin declarar |
| F1-REPLICA | no | — | — | T1/T7 | la réplica A0 reproduce el libro (f, τ, m0, ancla y flujos): la capa F1 y el libro son el mismo motor |
| F1-K3a | sí | BLOQUEA | DATOS INVÁLIDOS | K3 | caja base por dos vías: faltan Análisis C46–C52 o las filas 11, 12, 16, 17 o 18 de la ventana: no se puede descomponer la diferencia; diferencia total sin explicar: +9.301933 |
| F1-LIBRO | no | — | — | (1a) · implantación | el libro V6.3.1 F1 calcula el perímetro declarado (None): f, ancla, D_X, series y 0 flujos del Motor coinciden con la capa |
| V-F1f | no | — | — | (2) | sin series para los efectos de escala |
| F1-SERIES | no | — | — | (1a) · H12 · V631-2 | D&A de derechos de uso y PPA: cifra publicada con su signo, como cifra completa, en una página existente de una fuente del expediente con su huella; columna del ejercicio comprobada en 0 años |

## Flujo sin crecimiento por perímetro (diagnóstico)

| Perímetro | f | Flujo sin crecimiento | Frente a A0 | Ancla S2C (E4) |
|---|---|---|---|---|
| A0_total | 0.004129830 | 316.818 | +0.000 | 1.965673 |
| B_cota_capex | 0.024499970 | 291.704 | -25.114 | 3.601553 |

## K3 · perímetro A0 (lo que calcula el libro)

| Partida | mm | Clase |
|---|---|---|
| FCF base que calibra f (Historia C70, entrada registrada) | 241.454 | caja |
| + nivel del EBIT del año base frente a la media de la ventana, al τ de proyección | 10.922 | explicada |
| + τ de proyección frente al τ de cada año de la ventana | 1.164 | explicada |
| − f aplicada a las ventas del año base en lugar de las medias | -0.323 | explicada |
| + reinversión de la ventana que la proyección sin crecimiento no repite (capex − D_X + circulante; D&A ROU o PPA sin declarar) | 63.601 | sin_desglose |
| **= flujo sin crecimiento** | **316.818** | cuadra |

Doble cómputo señalado por K3 en A0: 0.000 mm de media en la ventana; 0.000 a la escala del año base.

## Parámetros sin valor adoptado

- alcance_n1_ejercicios_tau: sin valor (N1_ALCANCE_EJERCICIOS_TAU.md (propuesta, no adoptada))
- n1_actualizacion_financiera_earnout: sin valor (N1_ACTUALIZACION_EARNOUT_MEXICO.md (propuesta, no adoptada))
- umbral_v_f1a: sin valor (PROPUESTA_UMBRAL_V-F1a.md (propuesta, no adoptada))
