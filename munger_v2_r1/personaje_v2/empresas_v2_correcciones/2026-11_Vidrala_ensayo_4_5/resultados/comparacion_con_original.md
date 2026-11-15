# Comparación con el expediente original · Vidrala (entrega 4.5)

Original: `personaje_v2/empresas_v2/Vidrala/` (ejecución anterior, motor A, circulante de 2024 sin P1). Ensayo: `2026-11_Vidrala_ensayo_4_5/Vidrala/`. Generado por `scripts/comparar_con_original.py`. Los resultados son **mecánicos**; ninguna de las dos columnas es una valoración comparable con el precio.

## 1. Entradas (Historia de fase1_v63.json)

| Partida | Año | Original | Ensayo |
|---|---|---|---|
| circulante | 2024 | -127.84 | 84.994 |

Diferencias de valor: 1. Metadatos distintos: ninguno. Ceros pendientes de verificación en el ensayo: 38 (el original no los marcaba: se construyó antes de la reparación H1).

## 2. Celdas de juicio (68) en el libro evaluado

| Celda | Fase | Original | Ensayo |
|---|---|---|---|
| Análisis!C19 | A | Sí | No |
| Análisis!C62 | A | Sí | No · financiación cambia mucho |
| Análisis!B66 | A | La energía más barata se traslada al cliente por las fórmulas de precio mientras el vol… | La energía más barata y una demanda europea débil se van al cliente vía precio: Vidrala… |
| Análisis!C66 | A | Volumen casi plano en mercados maduros y precio que sigue al coste con retraso: el marg… | Volumen al ritmo de un mercado maduro y precio que sigue al coste por fórmulas contract… |
| Análisis!D66 | A | Brasil y Chile crecen en euros y se acercan a la rentabilidad del grupo, y en Europa la… | Brasil crece en volumen y precio y gana peso en la mezcla, su deuda en reales se amorti… |
| Análisis!B68 | B | 0.015 | 0.01 |
| Análisis!C76 | B | 0 | (vacía) |
| Análisis!C97 | A | Comprando | Neutral |
| Análisis!B101 | C | Vidrala fabrica envases de vidrio para alimentación y bebidas en Iberia y Europa occide… | Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil para client… |
| Análisis!B102 | C | El vidrio es un envase poco diferenciado que sale de 21 hornos que no se pueden parar [… | El margen de 2023–2025 no es foso, es el desfase de un ciclo de coste: la energía bajó … |
| Análisis!C104 | C | Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 54… | Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 65… |
| Palancas!C14 | B | 0.03 | 0.02 |
| Palancas!D14 | B | 0.055 | 0.035 |
| Palancas!B15 | B | 0.14 | 0.15 |
| Palancas!C15 | B | 0.17 | 0.18 |
| Palancas!D15 | B | 0.19 | 0.2 |
| Palancas!B16 | B | 0.8 | 0.9 |
| Palancas!C16 | B | 1 | 0.9 |
| Palancas!D16 | B | 1.3 | 1 |
| Palancas!D18 | B | 0.14 | 0.12 |
| Palancas!C22 | B | 0 | (vacía) |
| Palancas!C23 | B | 0 | (vacía) |
| Palancas!A38 | C | Las ventas consolidadas de Vidrala del ejercicio 2027 (cuenta de resultados de las cuen… | Margen EBIT consolidado de 2027 (resultado de explotación ÷ ingresos ordinarios de las … |
| Palancas!A39 | C | El margen EBIT consolidado de 2027 (resultado de explotación contable ÷ ventas de la cu… | Ingresos ordinarios del segmento Vidrala Europe en 2027 entre 680 y 790 mm (714,9 mm en… |
| Palancas!A40 | C | La deuda neta según la definición de la propia empresa (sin NIIF 16) a 31-dic-2027 será… | Pagos por inmovilizado material e intangible del estado de flujos consolidado de 2027 p… |
| Palancas!B38 | C | 2028-04-30 00:00:00 | 2028-03-31 00:00:00 |
| Palancas!B39 | C | 2028-04-30 00:00:00 | 2028-03-31 00:00:00 |
| Palancas!B40 | C | 2028-04-30 00:00:00 | 2028-03-31 00:00:00 |
| Palancas!C38 | C | 0.65 | 0.7 |
| Palancas!C39 | C | 0.6 | 0.75 |
| Diagnóstico V6!B222 | C | B69:D69, la probabilidad del escenario MALO (0,2 por convención, rango defendible 0,2–0… | Palancas C8 (base del margen = Media del ciclo): la hoja parte de un margen del 16,9 % … |
| Diagnóstico V6!B223 | C | Las cuentas anuales consolidadas y el informe de resultados de 2026 de Vidrala (margen … | Cuenta de resultados de operaciones continuadas reexpresada sin Italia para 2019–2022 (… |

Iguales: 36. Distintas: 32. (Las iguales no prueban que se heredaran: las fases del ensayo las decidieron de nuevo; ver sus Observaciones.)

## 3. Historia: celdas numéricas distintas (libros evaluados recalculados)

| Celda | Original | Ensayo |
|---|---|---|
| K14 | -127.84 | 84.994 |
| K30 | -76.76 | 136.074 |
| K31 | -318.428 | -105.594 |
| C53 | 1.54922 | 0.915854 |
| C58 | 0.0198902 | -0.0276078 |
| C76 | 40.4303 | 111.375 |
| C77 | 190.909 | 119.964 |
| C79 | 29.7087 | -41.2359 |
| C80 | 0.0198902 | -0.0276078 |

## 4. Estados y resultados mecánicos

| Concepto | Original | Ensayo |
|---|---|---|
| Estado del análisis | concluido | concluido |
| Auditoría | APROBADO | APROBADO |
| Motor (C62) | A | B |
| f (Historia C58) | 0.0198902 | -0.0276078 |
| Tasa de descuento del motor | 0.09 | 0.0869221 |
| r (C56) | 0.09 | 0.09 |
| Pasivos netos del puente (C16, motor B) | — | 160.784 |
| Valor por acción MALO | 43.7994 | 53.6704 |
| Valor por acción NORMAL | 57.8682 | 70.7722 |
| Valor por acción BUENO | 77.6934 | 86.4888 |
| Probabilidades | [0.2, 0.6, 0.2] | [0.2, 0.6, 0.2] |
| Ponderado (mecánico) | 59.0195 | 70.4952 |
| Precio de Sí (mecánico) | 54.6709 | 65.6881 |
| Zona (mecánica) | caro | caro |
| Precio de la hoja (C37) | 87.9 | 87.9 |
| Cubo | Vigilar | Vigilar |
| Estado del libro | LISTO · PROVISIONAL (23 estimaciones justificadas) | NO LISTO · evidencias incompletas (2 pendientes) · cálculo completo |
| Estado de las evidencias | PROVISIONAL · 23 estimación(es) justificada(s) · documentadas 19 de 19 · hipótesis conf… | INCOMPLETAS · datos 15 de 17 · hipótesis confirmadas 0 de 22 · 22 estimaciones · 2 no v… |
| Análisis!C104 | Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 54… | Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 65… |

Los valores del original y del ensayo no son comparables entre sí como valoraciones: cambian el dato de 2024 (P1), el motor, las palancas decididas de nuevo y la fecha de referencia del valor (motor B: 31-dic-2025, con derecho al dividendo a cuenta).
