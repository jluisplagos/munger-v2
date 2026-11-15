# Comparación homogénea · heredado frente a experimental (mismas entradas y palancas)

Precio 90.1 · zona activa caro · huella de las entradas económicas `ef796fea2af329f2…`.

- **Heredado (V6.3 efectiva):** ponderado 69.04 · precio de Sí 64.75 · zona caro.
- **Activa:** ponderado 60.70 · precio de Sí 56.02 · zona caro.
- **Diferencia total (activa − heredado):** ponderado -8.34 · precio de Sí -8.73. De ella, P-M1 (con la cartera) frente a la activa sin P-M1: ponderado -6.80 · precio de Sí -6.61; el resto es de N1, N2 y R1 juntos.

| Variante | Lectura | Ponderado | Precio de Sí | Zona | Δ pond. vs heredado | Δ Sí vs heredado | Δ Sí vs activa |
|---|---|---|---|---|---|---|---|
| heredado | V6.3 efectiva (modo heredado) sobre el mismo libro | 69.04 | 64.75 | caro | 0.00 | 0.00 | 8.73 |
| solo_N1 | solo N1 (tipo normalizado), lo demás heredado | 67.17 | 63.04 | caro | -1.87 | -1.71 | 7.02 |
| solo_N2 | solo N2 (margen de partida), lo demás heredado | 70.02 | 65.72 | caro | 0.98 | 0.97 | 9.70 |
| solo_R1 | solo R1 (reinversión con capacidad conservada), lo demás heredado | 68.41 | 63.40 | caro | -0.63 | -1.36 | 7.38 |
| activa_sin_PM1 | la activa sin P-M1 (N1, N2 y R1 juntos) | 67.50 | 62.63 | caro | -1.54 | -2.13 | 6.61 |
| activa_solo_P0 | la activa sin requisito adicional, con P0 | 67.99 | 63.11 | caro | -1.05 | -1.64 | 7.10 |
| activa | configuración activa del expediente | 60.70 | 56.02 | caro | -8.34 | -8.73 | 0.00 |
| estructura_H | misma configuración con la estructura H (entradas compatibles) | 67.17 | 61.37 | caro | -1.87 | -3.38 | 5.35 |
| estructura_S | misma configuración con la estructura S (entradas compatibles) | 60.00 | 55.52 | caro | -9.04 | -9.23 | -0.50 |
| estructura_SR2 | misma configuración con la estructura SR2 (entradas compatibles) | 62.02 | 57.08 | caro | -7.02 | -7.68 | 1.06 |
| estructura_SRF | misma configuración con la estructura SRF (entradas compatibles) | 63.77 | 58.43 | caro | -5.27 | -6.32 | 2.41 |
| parametro_minimo | estructura activa con λ = 1.1 (extremo del rango declarado) | 63.13 | 58.38 | caro | -5.91 | -6.37 | 2.37 |
| parametro_maximo | estructura activa con λ = 1.25 (extremo del rango declarado) | 55.84 | 51.29 | caro | -13.20 | -13.47 | -4.73 |
| convencion_anios_alternativa | estructura activa con los años «Proporcional a las ventas» | 60.43 | 55.89 | caro | -8.61 | -8.86 | -0.13 |
| convencion_terminal_alternativa | estructura activa con el terminal «Crece con g» | 61.35 | 56.42 | caro | -7.69 | -8.33 | 0.40 |

Todas las variantes usan las mismas entradas y las mismas palancas (copias del libro evaluado; huella de las entradas económicas en `mismas_entradas`). Los efectos aislados no son aditivos (interactúan); el rango de esta tabla no es un intervalo de confianza ni cubre hipótesis no exploradas.
