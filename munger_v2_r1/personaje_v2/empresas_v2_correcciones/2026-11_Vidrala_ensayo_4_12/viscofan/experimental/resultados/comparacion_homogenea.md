# Comparación homogénea · heredado frente a experimental (mismas entradas y palancas)

Precio 54.7 · zona activa caro · huella de las entradas económicas `7bff0b2e361fc235…`.

- **Heredado (V6.3 efectiva):** ponderado 46.26 · precio de Sí 41.81 · zona caro.
- **Activa:** ponderado 43.59 · precio de Sí 39.29 · zona caro.
- **Diferencia total (activa − heredado):** ponderado -2.67 · precio de Sí -2.52. De ella, P-M1 (con la cartera) frente a la activa sin P-M1: ponderado -1.06 · precio de Sí -1.07; el resto es de N1, N2 y R1 juntos.

| Variante | Lectura | Ponderado | Precio de Sí | Zona | Δ pond. vs heredado | Δ Sí vs heredado | Δ Sí vs activa |
|---|---|---|---|---|---|---|---|
| heredado | V6.3 efectiva (modo heredado) sobre el mismo libro | 46.26 | 41.81 | caro | 0.00 | 0.00 | 2.52 |
| solo_N1 | solo N1 (tipo normalizado), lo demás heredado | 44.65 | 40.35 | caro | -1.61 | -1.45 | 1.07 |
| solo_R1 | solo R1 (reinversión con capacidad conservada), lo demás heredado | 46.26 | 41.81 | caro | 0.00 | 0.00 | 2.52 |
| activa_sin_PM1 | la activa sin P-M1 (N1, N2 y R1 juntos) | 44.65 | 40.35 | caro | -1.61 | -1.45 | 1.07 |
| activa | configuración activa del expediente | 43.59 | 39.29 | caro | -2.67 | -2.52 | 0.00 |
| estructura_H | misma configuración con la estructura H (entradas compatibles) | 44.65 | 40.35 | caro | -1.61 | -1.45 | 1.07 |
| estructura_S | misma configuración con la estructura S (entradas compatibles) | 43.14 | 38.94 | caro | -3.12 | -2.87 | -0.35 |
| estructura_SR2 | misma configuración con la estructura SR2 (entradas compatibles) | 44.03 | 39.64 | caro | -2.23 | -2.16 | 0.36 |
| estructura_SRF | misma configuración con la estructura SRF (entradas compatibles) | 45.56 | 40.90 | caro | -0.70 | -0.91 | 1.61 |
| parametro_minimo | estructura activa con θ = 0.0 (extremo del rango declarado) | 44.65 | 40.35 | caro | -1.61 | -1.45 | 1.07 |
| parametro_maximo | estructura activa con θ = 1.0 (extremo del rango declarado) | 42.52 | 38.22 | caro | -3.74 | -3.58 | -1.07 |
| convencion_anios_alternativa | estructura activa con los años «Proporcional a las ventas» | 43.46 | 39.20 | caro | -2.80 | -2.61 | -0.09 |
| convencion_terminal_alternativa | estructura activa con el terminal «Crece con g» | 43.86 | 39.49 | caro | -2.40 | -2.32 | 0.20 |

Todas las variantes usan las mismas entradas y las mismas palancas (copias del libro evaluado; huella de las entradas económicas en `mismas_entradas`). Los efectos aislados no son aditivos (interactúan); el rango de esta tabla no es un intervalo de confianza ni cubre hipótesis no exploradas.
