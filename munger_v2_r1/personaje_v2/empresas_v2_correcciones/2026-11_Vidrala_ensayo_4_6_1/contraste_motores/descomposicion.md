# Descomposición del contraste de motores (entrega 4.5)

Aritmética de la hoja reproducida en Python (la réplica coincide con las cinco variantes recalculadas por LibreOffice al céntimo). Cada paso cambia una sola cosa. **No es una valoración ni un argumento para elegir motor.** Las palancas de la fase B, las probabilidades, V0, el margen de partida, el tipo y las acciones son comunes.

## Orden tasa → puente → f

| Paso | V NORMAL | Δ V NORMAL | Ponderado | Δ ponderado | Precio de Sí | Δ precio de Sí |
|---|---|---|---|---|---|---|
| B0 · motor B (ensayo) | 70.77 | — | 70.50 | — | 65.69 | — |
| tasa r_op 0.0869 → r 0.09 | 67.47 | -3.30 | 67.23 | -3.27 | 62.78 | -2.91 |
| sin restar pasivos netos (160.784 mm) | 72.04 | +4.57 | 71.79 | +4.57 | 67.34 | +4.57 |
| f 0 → -0.009847 (T3, condicionada) → estado = A2 | 78.01 | +5.97 | 77.67 | +5.88 | 72.87 | +5.52 |
| definición de f: T3 → T1 publicada (-0.027608) → estado = A1 | 88.78 | +10.77 | 88.27 | +10.60 | 82.82 | +9.96 |

## Orden f → puente → tasa

| Paso | V NORMAL | Δ V NORMAL | Ponderado | Δ ponderado | Precio de Sí | Δ precio de Sí |
|---|---|---|---|---|---|---|
| B0 · motor B (ensayo) | 70.77 | — | 70.50 | — | 65.69 | — |
| f 0 → -0.009847 (T3, condicionada) | 77.02 | +6.25 | 76.64 | +6.15 | 71.45 | +5.77 |
| sin restar pasivos netos (160.784 mm) | 81.59 | +4.57 | 81.21 | +4.57 | 76.02 | +4.57 |
| tasa r_op 0.0869 → r 0.09 → estado = A2 | 78.01 | -3.57 | 77.67 | -3.54 | 72.87 | -3.16 |
| definición de f: T3 → T1 publicada (-0.027608) → estado = A1 | 88.78 | +10.77 | 88.27 | +10.60 | 82.82 | +9.96 |

## C49 dentro del motor A con T3 (solo entra por f)

| Variante | f | Ponderado | Precio de Sí |
|---|---|---|---|
| A2 | -0.009847 | 77.67 | 72.87 |
| A2a | -0.008307 | 76.75 | 72.00 |
| A2b | -0.012860 | 79.47 | 74.55 |

Cómo entra la financiación en cada motor: en el B, por el puente (deuda + arrendamientos + pensiones + minoritarios − caja de 31-dic-2025) y por `r_op`; en el A, por `f` (que recoge, entre otras partidas, los intereses pagados) y por r. Un f negativo suma flujo cada año y para siempre.

En el motor B, C49 no entra en el valor (f = 0; los arrendamientos están en el puente como deuda contrastada).
