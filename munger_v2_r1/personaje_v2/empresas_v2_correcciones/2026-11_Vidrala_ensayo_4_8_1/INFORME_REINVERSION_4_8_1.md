# Reinversión de Vidrala: reposición, crecimiento y circulante (R-F1 y R-F2)

**Qué es este documento:**
- es la respuesta de la entrega 4.8.1 a los puntos R-F1 y R-F2 del encargo;
- todas las cifras salen de `scripts/analisis_reinversion_4_8_1.py`, y sus salidas están en `financiero/rf_*`;
- es un modelo auxiliar: no cambia el libro de referencia, ni r, ni las probabilidades, ni los escenarios, ni k, ni la caja, ni el puente, ni las acciones;
- ningún valor es una medición del mantenimiento real, una previsión, una cota ni una comparación con la cotización;
- **P-M1 sigue abierta.**

**Cómo se reproduce:** `python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/scripts/analisis_reinversion_4_8_1.py`, desde `munger_v2_r1/`. Código 0 si se cumplen los ocho controles (el 7 y el 8 se describen juntos en el punto 7):
1. **Réplica de la 4.8.** El guion de la 4.8 se ejecuta sin cambios y sus siete salidas salen idénticas byte a byte. Esa ejecución reproduce a su vez la 4.7.1.
2. **Motor.** El motor nuevo reproduce las alternativas de la 4.8 que usa, con una diferencia menor de 1e-9: REF, P0, X41, P5x0, P1, P1b, P1a, P5 y P1s.
3. **Referencias externas.** Las cuatro referencias de R-F2 del encargo se reproducen a 7 decimales.
4. **Descomposición.** La de R-F2 cierra.
5. **Identidad del FCF.** Se cumple en cada fila anual y terminal.
6. **Crédito.** Solo aparece en la estructura del hueco.
7. **SRF.** Con Rh = 0, y por la misma vía de cálculo, reproduce S. Además, fila a fila, su inversión fija es la de S × (1 − Rh ÷ F). Son controles añadidos tras la auditoría interna y corregidos tras el control de vigencia (V-4).

**Convenciones del texto:**
- «Hecho» es un dato publicado o un resultado de cálculo reproducible.
- «Interpretación» es una lectura de esos hechos.
- «Propuesta» es una sugerencia para la persona responsable.
- Las cifras van en M€ y los valores por acción, en €.
- Δ es la diferencia con la referencia REF de la 4.7.1, que da 69,24 de ponderado y 64,26 de precio de Sí.

## 1. Resumen

**Hechos:**
- La estructura del hueco de la 4.8 (P1, P1b, P1a, P5 y P6) cuenta toda la inversión fija neta del modelo como crédito contra el requisito de reposición. En el NORMAL con λ = 1,15, el crédito cubre todo el requisito de los diez años, 196,1 de 196,1. Por eso P1 vale lo mismo que P0 en el NORMAL y el BUENO.
- Si la misma inversión **no** puede cumplir las dos funciones, el valor depende de la estructura. Con el mismo λ = 1,15, el ponderado va de 68,92 (hueco) a 61,63 (suma sin reestimar):
  - con el S2C reestimado da 62,47 o 63,66, según cómo se trate el ROIC del terminal;
  - con la inversión fija para crecer reestimada da 65,38.
- **R-F2.** Con el mismo requisito, los mismos impuestos y el mismo descuento, el crédito explica +12,47 de los −20,64 de X41, es decir, el 60,45 % de su caída en ponderado. La convención terminal de P5x0 explica otros −2,05 frente a ese contraste. La interacción entre los dos cambios es +0,10.
- La cifra de la 4.8, «el 51 % del efecto de X41 es doble cómputo», mezclaba los dos cambios. Se retira (§4).

**Interpretaciones:**
- La identidad del FCF solo garantiza que la regla del hueco no cobra dos veces la misma inversión **si** esa inversión cumple las dos funciones. No demuestra que las cumpla.
- Que el S2C histórico (C53) contenga inversión fija no identifica qué parte de ella repone y qué parte hace crecer.
- **Cuánto mantenimiento está ya cubierto es información insuficiente.** El dato que falta es el desglose de la inversión de 2021–2025 por naturaleza (Q-E1) y el calendario de hornos (Q-E2).

**Propuesta:**
- No elegir ninguna estructura por defecto.
- Mientras no haya respuesta a Q-E1 y Q-E2, presentar el abanico por requisito y estructura (§3.4), sin tomar el extremo que da más valor como central.
- La decisión es de la persona responsable: D-N3b revisada, en `financiero/decisiones_y_preguntas_4_8_1.json`.

## 2. R-F2: el crédito, separado del cambio de convención terminal

**El problema.** La comparación de la 4.8 entre X41 y P5x0 cambiaba dos cosas a la vez:
- el crédito: X41 no lo tiene y P5x0 sí;
- el requisito del terminal: 55,555 × (1 + g) en X41 y 55,555 × ventas₁₁ ÷ ventas₀ en P5x0.

**El diseño.** Es un 2 × 2, sin P0 en ninguna rama. Es igual en todos los casos:
- el requisito de los años 1–10, 55,555 cada año, que es el exceso de 2025 sobre la amortización total;
- impuestos, descuento, escenarios y probabilidades;
- caja, puente y acciones.

**Resultados (hechos):**

| Caso | Requisito del terminal | Crédito | V MALO | V NORMAL | V BUENO | Ponderado | Precio de Sí |
|---|---|---|---:|---:|---:|---:|---:|
| REF | — | — | 51,8059 | 69,7805 | 85,0758 | **69,2446731** | **64,2621768** |
| X41 (4.7.1) | 55,555 × (1 + g) | no | 32,5125 | 49,0340 | 63,4265 | **48,6081961** | **44,0094136** |
| X41c: X41 con el mismo requisito y crédito | 55,555 × (1 + g) | sí | 35,1489 | 62,2965 | 83,3742 | **61,0825280** | **53,6729333** |
| X41t: X41 con la convención de P5x0 | 55,555 × ventas₁₁ ÷ ventas₀ | no | 32,8692 | 46,7398 | 59,2144 | 46,4605972 | 42,5773468 |
| P5x0 (4.8) | 55,555 × ventas₁₁ ÷ ventas₀ | sí | 35,5057 | 60,0022 | 79,6628 | **59,0350469** | **52,3123793** |

**Las referencias externas se reproducen exactamente.** Las cuatro del encargo (REF, X41, X41c y P5x0) coinciden a 7 decimales; no hubo que ajustar ninguna entrada.

**Requisito del terminal por escenario:**

| Escenario | Convención de X41 | Convención de P5x0 |
|---|---:|---:|
| MALO | 56,11 | 53,89 |
| NORMAL | 56,67 | 69,08 |
| BUENO | 56,94 | 78,02 |

Las dos convenciones crecen con distinta base: la de X41 con (1 + g) sobre el nivel de 2025; la de P5x0, con las ventas del año 11 frente a las de 2025. En el NORMAL y el BUENO, la segunda es más exigente.

**Descomposición (hechos):**

| Efecto | Ponderado | Precio de Sí |
|---|---:|---:|
| Caída de X41 frente a REF | −20,6365 | −20,2528 |
| Crédito, con la convención de X41 (X41c − X41) | **+12,4743 (60,45 % de la caída)** | +9,6635 (47,71 %) |
| Crédito, con la convención de P5x0 (P5x0 − X41t) | +12,5744 | +9,7350 |
| Convención, sin crédito (X41t − X41) | −2,1476 | −1,4321 |
| Convención, con crédito (P5x0 − X41c) | **−2,0475** | −1,3606 |
| Interacción | +0,1001 | +0,0715 |
| Reparto de Shapley: crédito / convención (suman P5x0 − X41) | +12,5244 / −2,0975 (+10,4269) | +9,6993 / −1,3963 (+8,3030) |

**Dónde actúa cada efecto (hecho).**
- **El crédito** actúa en los años 1–10 del NORMAL y el BUENO, y en el terminal de los tres escenarios.
- **En los años 1–10 del MALO, el crédito no actúa.** Las ventas caen y la regla R1 no deja inversión fija neta que acreditar, así que el valor presente de esos años es igual en X41 y X41c (786,81).
- **La convención** solo actúa en el terminal.

**Interpretación:**
- El 60,45 % es lo que la estructura del hueco atribuye al crédito, **bajo la hipótesis de que la inversión fija para crecer también repone**. No es una medición del doble cómputo ni del mantenimiento real.
- En precio de Sí la fracción es menor, el 47,71 %, porque el MALO pesa más en la escalera y en el MALO el crédito casi no actúa.

## 3. R-F1: reposición, crecimiento y circulante

### 3.1 Qué se concilia y de dónde sale

Cada fila del año 1 al 10, y la del terminal (año 11), de `financiero/rf_conciliacion_anual_y_terminal.csv` lleva estas piezas:

| Pieza | Qué es | Origen |
|---|---|---|
| Reposición contable | Amortización que se repone: D&A de 2025 menos la cartera de clientes mientras dura (P0). En el terminal, proporcional a las ventas | Dato publicado (CF_2025 y nota de intangibles) y cálculo |
| Requisito de reposición adicional | Lo que haría falta invertir por encima de esa amortización para conservar la capacidad y la competitividad | **Hipótesis** (λ o θ, §3.3) |
| Inversión fija para crecer | ΔV ÷ S2C − Δcirculante (en el terminal, g ÷ ROIC × NOPAT − Δcirculante) | Cálculo del modelo con S2C y ROIC de la fase B |
| Crédito (misma inversión, dos funciones) | La parte del requisito que la estructura da por cubierta con la inversión para crecer | **Consecuencia de la estructura**, no una medición |
| Reposición adicional pagada | Requisito menos crédito | Cálculo |
| Circulante | ΔV × circulante ÷ ventas de 2025, con la regla R1 | Cálculo del modelo |
| Inversión fija bruta, inversión total y FCF | Reposición contable + inversión para crecer + reposición adicional pagada; inversión total = esa inversión + circulante; FCF = NOPAT + amortización − inversión fija bruta − Δcirculante | Cálculo (identidad comprobada en cada fila) |

**Datos de la Historia** (publicados, o cálculo de la plantilla con datos publicados):
- ΔV 2020–2025: 476,79;
- reinversión neta de 2021–2025 (Historia!H31:L31, el denominador de C53): 520,60. Se compone así (auditoría interna, Y-c):

  | Componente | Importe |
  |---|---:|
  | Inversión menos amortización | 229,38 |
  | Adquisiciones netas (Vidroporto en 2023 y venta de Italia en 2024) | 12,42 |
  | Aumento del circulante | 278,80 (53,6 %) |

  Por unidad de ΔV, el circulante histórico es 0,585 y el del modelo, 0,147. Medido frente a la amortización que se repone (sin la cartera, Σ 9,41), el denominador es 530,01. La inversión fija neta histórica frente a esa amortización, con las adquisiciones, es 251,21;
- C53: 0,9159;
- exceso de la inversión sobre la amortización que se repone, 2021–2025: 238,79 en total y 47,76 de media anual.

### 3.2 Cuándo una misma inversión cumple varias funciones y cuándo se suman

**Interpretación**, con ejemplos del sector:
- **Una sola inversión, dos funciones.** Ocurre cuando la reposición se hace con más capacidad o más eficiencia. Por ejemplo, la reconstrucción de un horno al final de su campaña con más toneladas por día: el mismo gasto repone el horno viejo y añade la capacidad que pide el crecimiento. Es lo que supone la estructura del hueco, y cabe en el vidrio hueco.
- **Dos necesidades que se suman.** Ocurre cuando el crecimiento exige capacidad nueva, como una línea o un horno adicional, además de reponer la existente. También cuando la reposición o la competitividad obligada (descarbonización, electrificación, normativa) no añade capacidad vendible. En esos casos, la inversión para crecer no reduce lo que hay que reponer.
- **Cuál de los dos casos se da** depende del plan de hornos y del desglose de la inversión, que no son públicos (Q-E1, Q-E2 y Q-E3). **Información insuficiente.**
- **El circulante** acompaña al crecimiento de las ventas y no repone nada. Ninguna estructura lo usa como crédito.

### 3.3 Las estructuras y los requisitos

**Estructuras.** Ninguna se ha elegido; las cinco son hipótesis condicionadas:
- **H** (regla del hueco, la de la 4.8). Crédito de toda la inversión fija para crecer contra el requisito, en los diez años y en el terminal. Es coherente si la inversión para crecer también repone (§3.2, primer caso).
- **S** (suma sin reestimar). Requisito completo más la inversión para crecer con el S2C y el ROIC de la fase B. Es coherente si el S2C de la fase B no contiene el exceso histórico de reposición. **Interpretación:** con un S2C de la fase B (0,90 / 0,90 / 1,00) próximo a C53 (0,916), que sí lo contiene por construcción, S tiende a cobrar dos veces ese exceso.
- **SR1** (suma con el S2C reestimado):
  - el S2C de los diez años se multiplica por f = den ÷ (den − Rh), donde Rh es la parte de la reinversión histórica que la **misma** hipótesis atribuye a la reposición;
  - el ROIC del terminal no cambia;
  - el requisito sigue también en el terminal, sin crédito.
- **SRF** (inversión fija reestimada; la propuso la auditoría interna, Y-c).
  - **Qué hace.** La inversión **fija** para crecer, en los años y en el terminal, se multiplica por 1 − Rh ÷ 251,21. El circulante no se toca y el requisito va completo.
  - **Por qué hace falta.** El 53,6 % de den es circulante, y SR1 y SR2 reparten Rh también sobre él. Por eso SR1 y SR2 descontaminan la inversión fija menos de lo que implica su propia hipótesis.
  - **Qué no se decide aquí.** Si la reposición histórica se repartió así es igual de condicionado que en las demás estructuras.
- **SR2.** Como SR1, pero el ROIC del terminal también se multiplica por f, de modo que la reinversión para crecer se descontamina igual en los diez años (ΔV ÷ S2C) y en el terminal (g ÷ ROIC). Por qué se distingue de SR1: en la plantilla, el S2C de los diez años y el ROIC_lp del terminal son parámetros distintos de la fase B. Si el ROIC_lp ya mide el rendimiento de la inversión para crecer, vale SR1; si se fijó con la misma historia que el S2C, vale SR2. **Información insuficiente:** la fase B no lo dice.

**Requisitos (hipótesis):**
- **Familia Λ:** (λ − 1) × (amortización − cartera), con λ = 1,10 / 1,15 / 1,25: el desfase de inflación de la 4.8, `INFORME_PM1.md` §3. Su Rh histórico es Σ 2021–2025 de (λ − 1) × (amortización − cartera): 50,0 / 75,0 / 125,1. Su f vale 1,104 / 1,165 / 1,309, con den medido, como Rh, frente a la amortización que se repone. La primera versión daba 1,106 / 1,168 / 1,316 con den = 520,60 (Y-c). Su factor en SRF vale 0,801 / 0,701 / 0,502.
- **Familia Θ:** θ × 47,76 M€/año, donde θ es la fracción del exceso 2021–2025 que fue reposición o competitividad y no crecimiento. Se usa θ = 0,25 / 0,50 / 0,75 / 1. **θ no es un dato observado: no se usa ninguna proporción como si lo fuera.** θ = 1 es P5 de la 4.8. Su Rh es θ × 238,79, y su f vale 1,127 / 1,291 / 1,510 / 1,820 (en la primera versión, 1,130 / 1,298 / 1,524 / 1,847). Su factor en SRF vale 0,762 / 0,525 / 0,287 / 0,049.
- P0, la cartera no repuesta, se aplica en toda la familia, como en P1 y P5 de la 4.8.
- **Convenciones (auditoría interna, Y-d).** Las convenciones son las de la 4.8:
  - en los años 1–10, la amortización y el nivel θ quedan **planos** en el valor de 2025, que es una convención del motor y no un dato;
  - en el terminal, ambos pasan a ser **proporcionales a las ventas**.

  Por eso hay un salto en el año 11 (§3.5). §2 solo lo medía para el nivel de X41 sin P0. Ahora cada celda de §3.4 lleva además el efecto de una convención continua, con el requisito proporcional a las ventas también en los años 1–10: es la tabla de «Δ conv.».

  El auditor midió otra variante, la del terminal plano × (1 + g): +0,77 en S·L1.15 y +1,84 en S·T1.00. No se adopta ninguna convención: las dos son tan convencionales como la de la 4.8.

### 3.4 Resultados (hechos de cálculo; todos son hipótesis condicionadas)

Ponderado (Δ frente a P0) y precio de Sí. Todas las alternativas de R-F1 llevan P0 (+0,49 frente a REF). Así se separa el efecto del requisito del de la cartera (Y-m). REF da 69,24 / 64,26 y P0, 69,73 / 64,75.

| Requisito | H (hueco) | S (suma) | SR1 (S2C reestimado) | SR2 (S2C y ROIC reestimados) | SRF (inversión fija reestimada) |
|---|---|---|---|---|---|
| λ = 1,10 | 69,25 (−0,48) · 63,72 | 64,33 (−5,40) · 59,61 | 64,89 (−4,85) · 60,01 | 65,68 (−4,05) · 60,66 | 66,83 (−2,90) · 61,55 |
| λ = 1,15 | 68,92 (−0,82) · 63,00 | 61,63 (−8,11) · 57,04 | 62,47 (−7,27) · 57,64 | 63,66 (−6,08) · 58,61 | 65,38 (−4,35) · 59,95 |
| λ = 1,25 | 67,78 (−1,96) · 60,90 | 56,23 (−13,51) · 51,90 | 57,62 (−12,11) · 52,90 | 59,61 (−10,13) · 54,52 | 62,48 (−7,25) · 56,75 |
| θ = 0,25 | 69,29 (−0,44) · 63,81 | 64,84 (−4,90) · 60,09 | 65,50 (−4,23) · 60,57 | 66,45 (−3,28) · 61,34 | 67,83 (−1,91) · 62,40 |
| θ = 0,50 | 68,63 (−1,10) · 62,39 | 59,94 (−9,79) · 55,43 | 61,27 (−8,46) · 56,38 | 63,17 (−6,57) · 57,93 | 65,92 (−3,82) · 60,06 |
| θ = 0,75 | 66,86 (−2,87) · 59,97 | 55,04 (−14,69) · 50,77 | 57,04 (−12,69) · 52,20 | 59,89 (−9,85) · 54,52 | 64,01 (−5,73) · 57,71 |
| θ = 1 (P5) | 62,71 (−7,03) · 55,83 | 50,15 (−19,59) · 46,11 | 52,81 (−16,92) · 48,01 | 56,60 (−13,13) · 51,10 | 62,10 (−7,63) · 55,36 |

**Δ conv.** es el efecto en el ponderado de la convención continua (§3.3). Es igual en S, SR1, SR2 y SRF:

| Requisito | H | S, SR1, SR2 y SRF |
|---|---:|---:|
| λ = 1,10 | +0,02 | −0,22 |
| λ = 1,15 | +0,03 | −0,33 |
| λ = 1,25 | −0,34 | −0,55 |
| θ = 0,25 | +0,02 | −0,20 |
| θ = 0,50 | +0,03 | −0,40 |
| θ = 0,75 | −0,39 | −0,59 |
| θ = 1 | −0,77 | −0,79 |

**Valores por escenario, pesos del terminal y demás detalles:** en `financiero/rf1_alternativas.csv` y en `financiero/rf_salida.txt`.

**Interpretaciones:**
- Con cualquier requisito, H da el valor más alto y S el más bajo; SR1, SR2 y SRF quedan entre los dos.
- **SRF da más que SR1 y SR2.** Cuál de las tres descontaminaciones vale depende de cómo se reparta la reposición histórica entre inversión fija y circulante. Es una convención no observada, igual de condicionada (Y-c).
- **La convención de los años pesa menos que la estructura.** Va de −0,8 a +0,03 puntos.
- Con λ = 1,15, el abanico entre estructuras (61,6–68,9) es más ancho que el que da λ dentro de H en la 4.8 (67,8–69,3).
- **La incertidumbre principal de P-M1 no es λ: es qué parte de la inversión para crecer repone.** Es la misma pregunta que Q-E1.

### 3.5 Conciliación de un caso (NORMAL, λ = 1,15)

Hechos de cálculo, en M€; la fuente es `rf_conciliacion_anual_y_terminal.csv`.

| Año | Estructura | Requisito | Inversión para crecer | Crédito | Reposición adicional pagada | Inversión total | FCF |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | H | 19,3 | 28,3 | 19,3 | 0,0 | 161,0 | 186,7 |
| 1 | S | 19,3 | 28,3 | 0,0 | 19,3 | 180,3 | 167,4 |
| 1 | SR1 = SR2 | 19,3 | 23,6 | 0,0 | 19,3 | 175,7 | 172,0 |
| 1 | SRF | 19,3 | 19,8 | 0,0 | 19,3 | 171,8 | 175,9 |
| 10 | H | 19,9 | 33,8 | 19,9 | 0,0 | 171,9 | 211,7 |
| 10 | S | 19,9 | 33,8 | 0,0 | 19,9 | 191,8 | 191,7 |
| 10 | SR1 = SR2 | 19,9 | 28,3 | 0,0 | 19,9 | 186,3 | 197,2 |
| 10 | SRF | 19,9 | 23,7 | 0,0 | 19,9 | 181,7 | 201,8 |
| terminal | H | 24,8 | 41,2 | 24,8 | 0,0 | 211,8 | 209,1 |
| terminal | S y SR1 | 24,8 | 41,2 | 0,0 | 24,8 | 236,6 | 184,3 |
| terminal | SR2 | 24,8 | 34,6 | 0,0 | 24,8 | 230,0 | 190,9 |
| terminal | SRF | 24,8 | 28,9 | 0,0 | 24,8 | 224,3 | 196,6 |

**Suma de los diez años (hechos):**

| Estructura | Inversión total | Requisito | Inversión para crecer | Crédito |
|---|---:|---:|---:|---:|
| H | 1.664,1 | 196,1 | 309,3 | 196,1 |
| S | 1.860,3 | 196,1 | 309,3 | 0 |
| SR1 y SR2 | 1.809,8 | 196,1 | 258,9 | 0 |
| SRF | 1.767,9 | 196,1 | 216,9 | 0 |
| REF | 1.686,0 | — | — | — |

REF no lleva ni P0 ni requisito adicional.

**El salto del terminal (hecho, convención heredada de la 4.8).** La amortización pasa de 132,9 (año 10, constante desde 2025) a 165,3 (terminal, proporcional a las ventas). Con ella, el requisito λ pasa de 19,9 a 24,8, y el θ = 1, de 47,8 a 59,4. No es un error de cálculo, pero sí una discontinuidad de convención: Fable la señaló en la 4.8 (crítica, M4) y la auditoría interna de la 4.8.1, en Y-d. Su efecto está cuantificado en §3.4 (Δ conv.). Esta discontinuidad la tienen **todas** las estructuras, también SR1, SR2 y SRF.

**Necesidades de caja en el MALO (hechos).** Las ventas caen y no hay inversión para crecer, así que las cinco estructuras coinciden en los años 1–10:

| Requisito | FCF del año 1 | Mínimo | Suma de los años 1–5 |
|---|---:|---:|---:|
| REF | 203,8 | 161,5 | 921,1 |
| λ = 1,15 | 189,0 | 141,6 | 846,6 |
| θ = 1 | 160,6 | 113,8 | 704,2 |

Las estructuras solo se separan en el terminal del MALO, donde g = 1 % y sí hay inversión para crecer.

### 3.6 S2C y ROIC del terminal, revisados juntos

**Interpretación:**
- **La regla del hueco** (H) trata la inversión para crecer de los diez años (ΔV ÷ S2C) y la del terminal (g ÷ ROIC) como capaces de reponer. Es coherente consigo misma, pero esa capacidad es una hipótesis.
- **Las estructuras que suman** necesitan, para ser coherentes, descontar del S2C la parte de la reinversión histórica que su propia hipótesis llama reposición: SR1 y SR2. Si no, la cuentan dos veces: S.
- **Para el terminal** caben dos lecturas del ROIC_lp:
  - SR1: no cambia, porque ya mide la inversión para crecer;
  - SR2: se descontamina con el mismo factor que el S2C.
  La diferencia es de 1,2 puntos con λ = 1,15 y de 3,8 con θ = 1. **Información insuficiente:** falta cómo se fijó el ROIC_lp en la fase B.
- **SRF** aplica la misma lógica solo a la inversión fija, en los diez años y en el terminal. Su ROIC efectivo del terminal en el NORMAL, calculado como g × NOPAT ÷ reinversión para crecer, es más alto que el 0,110 de la fase B:

  | Requisito | ROIC efectivo |
  |---|---:|
  | λ = 1,10 | 0,134 |
  | λ = 1,15 | 0,150 |
  | λ = 1,25 | 0,197 |
  | θ = 0,25 | 0,139 |
  | θ = 0,50 | 0,190 |
  | θ = 0,75 | 0,299 |
  | θ = 1 | 0,701 |

  **Interpretación:** SRF con θ alto supone que el crecimiento apenas necesita inversión fija, también a perpetuidad. Es una implicación poco verosímil y condiciona esas celdas (control de vigencia, V-5). Las columnas `s2c_efectivo` y `roic_efectivo` del CSV dan las cifras por fila.

### 3.7 P1s revisado

**Hecho.** El P1s de la 4.8 (66,88 / 61,54) combinaba dos estructuras:
- **años 1–10:** la estructura SR1, con el S2C reestimado y el requisito explícito sin crédito;
- **terminal:** la estructura H, con el crédito de la inversión para crecer y el ROIC sin cambio.

En el terminal del NORMAL, el requisito (24,8) quedaba cubierto entero por el crédito.

**Interpretación:** la combinación es incoherente. Los diez años suponen que la inversión para crecer **no** repone, y el terminal, que **sí**.

**Corrección:**
- P1s sale de las propuestas;
- en su lugar quedan SR1·λ1,15 (62,47 / 57,64), SR2·λ1,15 (63,66 / 58,61) y SRF·λ1,15 (65,38 / 59,95). Son coherentes en cuanto al crédito: no lo tienen ni en los diez años ni en el terminal. **No** lo son en la convención de la amortización: la plana de los años 1–10 y la proporcional del terminal (§3.5) siguen, como en todas las estructuras;
- el valor de la 4.8 se conserva en las tablas solo como «P1s_4_8».
- Que P1s existiera no lo validaba: era un contraste, y su terminal no era coherente con sus diez años.

## 4. Afirmaciones de la 4.8 que se retiran

La 4.8 se conserva intacta: es un expediente anterior. Estas afirmaciones dejan de ser vigentes, y su sustituta es la de este informe:

| Dónde (4.8) | Afirmación retirada | Qué dice ahora |
|---|---|---|
| `INFORME_PM1.md` §1 (punto 2), §5.2, §6 (filas X41 y P5x0) y §7 (fila X41) | «Unos 309 de los 555 M€ […] ya los pagaba la inversión fija neta del modelo»; «En torno a la mitad (≈ 51 %) de su efecto es doble cómputo»; «P5x0 solo sirve para medir el doble cómputo de X41»; «No es una alternativa coherente» | 309,3 es lo que la estructura H **acredita** en el NORMAL, no un mantenimiento demostrado. El 51 % mezclaba crédito y convención terminal. Con el contraste puro (§2), el crédito explica el 60,45 % de la caída de X41 **bajo la hipótesis H**. Si la inversión para crecer no repone, X41 no tiene doble cómputo en el sentido de la 4.8. X41 queda como sensibilidad de la 4.7.1, con su estructura (S, sin crédito) y su convención (1 + g) declaradas |
| `INFORME_PM1.md` §1 (punto 3), §5.1 y §5.2 | «Las alternativas coherentes (con la regla del hueco, que no cobra dos veces)»; «la reposición implícita es D&A + inversión fija neta»; «Añadir encima un mantenimiento fijo cobra dos veces la parte que el modelo ya reinvierte» | Son ciertas **solo bajo la hipótesis H**: que la inversión para crecer también repone. Coherentes son también S, si el S2C de la fase B no contiene el exceso, y SR1 y SR2. El rango «69,7–62,7» de la 4.8 era el de H y P0, no el de las alternativas coherentes (§3.4) |
| `INFORME_PM1.md` §7 y D-N3b | P1 (λ = 1,15 con el hueco) como «hipótesis condicionada (central)» | Con λ = 1,15, H es la estructura que da **más** valor (68,92, frente a 61,63–65,38 en las que suman). No se propone como central por defecto (§1) |
| `INFORME_PM1.md` §8 (veredicto de la crítica) y `CRITICA_FABLE_PM1.md` | «la regla del hueco es correcta como identidad y el doble cómputo de X41 existe»; 63 % o 51 % de doble cómputo | La identidad del FCF es correcta, pero no demuestra la suficiencia económica del hueco (§1). El documento de la crítica se conserva como registro de lo que dijo |
| `scripts/analisis_pm1.py` (clases de X41 y P5x0; salidas «X41: inversión adicional que ya estaba pagada…» y «parte […] que es doble cómputo ≈ 51 %») | Las mismas | El guion de la 4.8 no se modifica, porque es material conservado y su réplica sirve de control. Sus salidas con esas frases ya no son vigentes |
| `decisiones_y_preguntas_4_8.json`, D-N3b | P1 (hueco) como hipótesis central | La sustituye D-N3b revisada en `financiero/decisiones_y_preguntas_4_8_1.json`: ninguna estructura por defecto |
| `VERSION`, `CONTINUIDAD.md` y `DECISIONES.md` de la 4.8 | «alternativas coherentes entre 69,7 y 62,7 […] frente al −20,6 con doble cómputo» | Lo corrigen el `VERSION`, el `CONTINUIDAD.md` y la entrada de `DECISIONES.md` de la 4.8.1 |

## 5. Clasificación de las conclusiones

| Conclusión | Clase |
|---|---|
| Las cuatro referencias externas de R-F2 se reproducen con las mismas entradas, fórmulas y convenciones | **Respaldado** (cálculo reproducible) |
| Con el mismo requisito, el crédito explica +12,47 de ponderado (60,45 % de la caída de X41) y la convención terminal −2,05 frente al contraste, con una interacción de +0,10 | **Respaldado** como resultado del modelo; **condicionado** a la hipótesis H en cuanto a su significado |
| La amortización de la cartera no se repone (P0) | Respaldado con alcance y límites (4.8; sin cambios) |
| La reposición es igual a la amortización (REF) | Sin respaldo (4.8; sin cambios) |
| La inversión para crecer del modelo también repone (H) | **Hipótesis condicionada** |
| El S2C de la fase B no contiene el exceso histórico (S) | **Hipótesis condicionada**, poco compatible con S2C ≈ C53 |
| S2C reestimado con el ROIC sin cambio o reestimado (SR1 y SR2), e inversión fija reestimada (SRF) | **Hipótesis condicionadas.** El reparto de la reposición histórica entre inversión fija y circulante no se observa |
| Amortización y nivel θ planos en los años 1–10 y proporcionales a las ventas en el terminal | **Convención** (de la 4.8), con su efecto cuantificado (Δ conv.) |
| Valor de λ y de θ | **Información insuficiente.** Falta el desglose de la inversión de 2021–2025 por naturaleza y segmento (Q-E1), el calendario y la capacidad de los hornos (Q-E2), la obligatoriedad de las reconstrucciones (Q-E3) y la capacidad y la producción (Q-E4) |
| Cuánto mantenimiento está ya cubierto por la inversión para crecer | **Información insuficiente** (los mismos datos) |
| Cómo se fijó el ROIC_lp de la fase B (SR1 frente a SR2) | **Información insuficiente.** Falta la justificación de ese parámetro en la fase B |

## 6. Qué queda pendiente

- **P-M1 sigue abierta.**
- **Abanico.** Mientras no se responda a Q-E1 y Q-E2, el abanico de §3.4 es la información disponible:
  - en la familia Λ, de 56,2 a 69,3 de ponderado;
  - en la familia Θ, de 50,2 a 69,3;
  - P0 solo da 69,7.
  Ningún extremo es una cota, y no se ha elegido ninguna estructura.
- **Decisiones y preguntas.** Están en `financiero/decisiones_y_preguntas_4_8_1.json`, con los campos humanos vacíos:
  - D-N3b revisada;
  - D-N3e: SR1 frente a SR2;
  - Q-T4: el criterio de fechas para las salidas de los pasos 5–10;
  - Q-T5: si pedir una auditoría nueva retira el cierre vigente;
  - Q-T6: si una aprobación con el contenido de otra ya usada cuenta como corrección fallida;
  - D-N3e incluye ahora SRF.
  Las preguntas a la empresa se prepararon y no se han enviado.
