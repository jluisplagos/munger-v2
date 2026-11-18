# Regresión F1 de Elis sobre una copia del expediente

Copia: `<copia fuera del repositorio>` (fuera del repositorio) · libro `d2593777650f1d9d…`

**39 de 39 comprobaciones pasan.**

| Comprobación | Resultado | Detalle |
|---|---|---|
| réplica: la capa F1 reproduce el libro en A0 (f, τ, m0, ancla y 33 flujos) | PASA | {"f": 0.041681455273796, "C58": 0.041681455273796, "ancla": 9.039509536785, "C53": 9.039509536785, "flujos_contrastados": 33, "conforme": true, "perimetro_replicado": "A0"} |
| E9 A0: f, flujo sin crecimiento y C53 | PASA | f 0.041681455273796 · F0 248.496395343 · C53 9.039509536785 |
| E9 A1: f, flujo sin crecimiento y C53 | PASA | f 0.012624225323285 · F0 387.878115969 · C53 2.445331695332 |
| E9 A2: f, flujo sin crecimiento y C53 | PASA | f -0.006118601744165 · F0 477.783708846 · C53 1.612524303305 |
| E9 B: f, flujo sin crecimiento y C53 | PASA | f 0.022646228408102 · F0 339.804571572 · C53 2.651525243106 |
| E9 A1: flujos de los años 1–10 y año 11 con las palancas actuales | PASA | desviación máxima 0.00e+00 |
| E9 A2: flujos de los años 1–10 y año 11 con las palancas actuales | PASA | desviación máxima 0.00e+00 |
| E9 T1: flujos A0 = los del libro | PASA | desviación máxima 0.00e+00 |
| (1a) flujo corregido frente a A0 en la base 2025: +139,4 | PASA | +139.381721 |
| V-F1a salta con el libro tal cual (A0 con ROU y C49 > 0) | PASA |  |
| K3 en A0: puente cuadrado y doble cómputo del arrendamiento señalado (132,5 de media; 139,4 a la escala de 2025) | PASA | {"doble_computo": 139.381721, "reposicion_no_monetaria": 89.905593} |
| K3 en A2: sin doble cómputo (partidas sin explicar: ninguna) | PASA |  |
| K3a: caja base por dos vías conforme (307,933 frente a 323,000; −25,067 de C48 y +10,0 de C47 declarados) | PASA | {"C70": 307.933, "media_fila_35": 323.0, "diferencia": -15.067, "componentes": {"C46": -0.000333, "C47": 9.999667, "C48": -25.066667, "C49": 0.0, "C50": 0.000333, "C70": 0.0}, "explicado": {"C48": -25.067, "C47": 10.0},  |
| K3b/K3c con el libro tal cual (A0): alquiler contado dos veces y reinversión media −81,2: bloquean | PASA |  |
| K3b con las decisiones (A3: f devuelve la ROU, pagos en el FCF base): alquiler contado una vez | PASA |  |
| T16: N1 en A0 (τ 0,2619/0,2806/0,2559; τ5 0,28234; m0 0,131379; f 0,044900433; flujo 236,891) | PASA | f 0.044900432751701 · F0 236.890936177 · τ {'2023': 0.2619, '2024': 0.2806, '2025': 0.2559} · τ5 0.28234 |
| T16: −11,605 (solo ventana) y variantes sin decidir −11,190 (2021–22) y −12,396 (actualización) | PASA | {"N1 solo en la ventana, sin la actualización financiera": -11.605459, "N1 también en los ejercicios del τ fuera de la ventana": -11.189527, "N1 con la actualización financiera fuera del BAI que da el tipo": -12.395744,  |
| T16: variación del año 11 NORMAL −18,609 | PASA | -18.608670 |
| T16: con N1 sin decidir sus opciones, F1-PARAM bloquea y F1-LIBRO también (el libro no normaliza) | PASA |  |
| Elis sigue en pendiente_de_datos: estado del expediente sin cambios | PASA |  |
| Elis: la evaluación F1 con las decisiones propone pendiente_de_datos (código 3) | PASA | DIAGNÓSTICO F1 · el resultado del motor A no se usa para una conclusión: F1-LIBRO, F1-PARAM, F1-PERIMETRO, F1-REGISTRO, V-F1d, V-F1g, V-F1i, V-F1j, V-F1k, V-F1l |
| Elis con las decisiones: V-F1d bloquea | PASA | A3_estimado sin estimación de la reinversión necesaria (R sigue en pendiente_de_datos: 3a, 3b (iv)) |
| Elis con las decisiones: V-F1j bloquea | PASA | clasificación de las compras de sociedades pendiente (opción A de 4b, hasta M6) |
| Elis con las decisiones: V-F1i bloquea | PASA | transición conocida con su tratamiento pendiente (sin importe ni horizonte la conclusión queda pendiente; nunca cero por defecto) |
| Elis con las decisiones: V-F1g bloquea | PASA | perímetro de las palancas S2C sin declarar |
| Elis con las decisiones: V-F1k bloquea | PASA | perímetro del ROIC del terminal sin declarar |
| Elis con las decisiones: F1-PARAM bloquea | PASA | alcance de N1 a los ejercicios del τ fuera de la ventana sin decisión adoptada (declarados fuera de la ventana: [2021, 2022]); no se elige por omisión; se calcu |
| Elis con las decisiones: F1-LIBRO bloquea | PASA | LÍMITE DECLARADO · el libro V6.3 calcula el perímetro A0 sin normalizar y sin términos explícitos; con A3_estimado y N1: su valor no corresponde a la declaració |
| Elis con las decisiones: V-F1l bloquea | PASA | N1 exige el margen objetivo declarado sin esos ajustes (condición de 5a): sin declarar |
| Elis con las decisiones: V-F1a no salta (el perímetro no es A0) | PASA |  |
| invariantes: C48 = 108, C49 = 128,1, C70 = 307,933 | PASA |  |
| (1b) sensibilidad: pagos −16,8; ROU +10,1; total −6,7 | PASA | {"convencion": "media de la ventana (referencia de ensayo y convención declarada; no es una estimación del peso futuro)", "pagos_media_%_ventas": 3.3589, "pagos_año_base_%_ventas": 3.7087, "sensibilidad_pagos_mm (A0, A1  |
| V-F1f informa (escala PPA +4,206; ROU −10,118) con el perímetro A2 · aquí se muestra como diagnóstico | PASA | {"PPA: media ÷ ventas medias (lo que devuelve f en A2)": 0.018743, "PPA: año base ÷ ventas del año base (lo que lleva m0)": 0.017866, "efecto de escala de la PPA en el flujo sin crecimiento de A2 (mm) |
| V-F1k (bloque 10): saltos +0,47/+0,68/+2,41 puntos ≤ C179: no avisa | PASA |  |
| ficha provisional de la copia: bloque motor_a_f1 presente, no utilizable, estado pendiente_de_datos | PASA | código 0 · OK: ficha_provisional.json · estado propuesto pendiente_de_datos · cubo Vigilar · acción None  |
| la ficha provisional cumple su esquema | PASA | VÁLIDO · ficha_provisional.json contra ficha.esquema.json |
| informe provisional de la copia: línea «Motor A · F1» | PASA | código 0  |
| el libro de la copia no cambia | PASA |  |
| el expediente original no cambia (huellas de todos sus archivos) | PASA |  |

## Comparación de los resultados F1 de Elis antes y después de F1 · US GAAP (mismo libro y mismas declaraciones)

- elis_T16_A0_con_N1_motor_a_f1_resultado.json: IGUAL (sin version, fecha ni rutas)
- elis_decisiones_17nov_motor_a_f1_resultado.json: IGUAL (sin version, fecha ni rutas)
- elis_libro_tal_cual_A0_motor_a_f1_resultado.json: IGUAL (sin version, fecha ni rutas)
- regresion_elis_f1.json: IGUAL (sin version, fecha ni rutas)
