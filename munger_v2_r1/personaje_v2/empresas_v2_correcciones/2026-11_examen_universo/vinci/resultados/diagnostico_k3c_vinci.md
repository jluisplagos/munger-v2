# VINCI · F1-K3c: el circulante en la reinversión (diagnóstico para la decisión de la persona responsable)

19-nov-2026. Orquestación; cifras de la capa F1 (`motor_a_f1.py`, A2_propio) sobre el libro de datos del expediente (`resultados/prevision_f1_tras_revision/`). Nada adoptado; no apto para dinero real. La justificación declarada que convertía F1-K3c en aviso se ha **retirado** (decisión del coordinador retirada tras la revisión independiente del montaje, `coordinacion/cierre_v2/examen/revisiones/vinci_montaje/REVISION.md` §3): F1-K3c vuelve a **BLOQUEAR** hasta que decida la persona.

## El problema
La capa calibra f = (NOPAT medio − reinversión media − C70) ÷ ventas medias de la ventana 2023–2025 (`motor_a_f1.py`, `calcular`; Historia C58), con reinversión = capex − D_X + circulante (fila 30).
- C70 = C52 = 4.419,333 EXCLUYE la entrada de circulante (decisión del inversor de la etapa 1, Control maestro M43: CFO 11.380 − circulante 2.090).
- La fila 30 la INCLUYE (fila 14: −1.463 / −2.311 / −2.496, media −2.090; URD 2024 PDF p. 336, URD 2025 PDF p. 358). Sin ella, capex − D_X = +329 / +876 / +522 (media +575,667).
- Resultado: el circulante sale dos veces en sentido contrario. f absorbe 2.090 ÷ 71.686,667 = 2,9 puntos de ventas como fuga permanente; la proyección equivale a una salida de circulante de ≈ 2.090/año (ni la entrada histórica ni el cero de M43).

Datos comunes: NOPAT medio 6.123,631; ventas medias 71.686,667; ventas 2025 (V0) 74.599; m0 = 0,125524; τ de proyección 0,32022.

## Opciones y efecto calculado (misma fórmula de la capa)

| Opción | C52 / C70 | reinversión media | f | flujo sin crecimiento (año base) | ancla S2C (E4, 2021–2025) |
|---|---|---|---|---|---|
| Estado actual = (c) | 4.419,333 | −1.514,333 | 4,490 % | 3.016,1 | 5,960 |
| (a) circulante 0 en la fila 14 de la ventana 2023–2025 | 4.419,333 | +575,667 | 1,574 % | 5.191,0 (+2.174,9; +72 %) | 5,960 si el ajuste no entra en el ancla; 2,720 si entra en 2023–2025; 2,323 si entra en 2021–2025 |
| (b) circulante en C46 (revoca M43) | 6.509,333 (C46 = 11.417,333) | −1.514,333 | 1,574 % | 5.191,0 (+2.174,9) | 5,960 |
| (c) mantenerlo, hipótesis conservadora declarada | 4.419,333 | −1.514,333 | 4,490 % | 3.016,1 | 5,960 |

Ancla: (V_2025 − V_2020) ÷ Σ 2021–2025 (capex − D_X + circulante + adquisiciones) = 31.365 ÷ 5.263; sin el circulante de 2023–2025, ÷ 11.533; sin el de 2021–2025, ÷ 13.504. Un ancla menor exige más reinversión por euro de crecimiento.

Lectura: (a) y (b) dan la misma f y el mismo flujo sin crecimiento (los dos tratan el circulante igual en la caja base y en la reinversión); difieren en la caja base que se enseña (C52 4.419 frente a 6.509, con el C40 coherente: 4.132 frente a 6.628), en lo que dice de la decisión M43 y en el ancla. (c) es más prudente (−2.175 mm/año de flujo sin crecimiento frente a a/b), pero incoherente con M43 si no se declara como hipótesis: supone una salida permanente de circulante de ≈ 2.090/año. Rasgo económico de fondo: VINCI tiene un circulante negativo estructural (anticipos de construcción y energía; entradas de 10,5 mil millones en 2016–2025 según la revisión), que solo se revierte si la contratación se contrae.

## Qué haría falta para cada una sin trucos
- **(a)** No se puede hacer hoy con NIIF: la reinversión de la capa (`WC_de`) y la del libro V6.3.1 (fila 30, C58 y C53) toman la fila 14 tal cual; el único ajuste declarado del circulante es el de US GAAP (`con_ajuste`, `retira_de_14`), y ni siquiera ese lo calcula el libro (F1-LIBRO bloquea). Corregir la fila 14 a 0 en la Historia (p. ej. con `fase1_decisiones.json`) NO vale: la fila 14 es la cifra publicada y alimenta otros cálculos; sería cambiar una fuente para legitimar un resultado. Haría falta en el PRODUCTO: (1) un campo declarado en `motor_a_f1.json` (p. ej. `normalizacion_circulante`: años, importe por año = −fila 14, motivo con la decisión M43 y su registro de la persona) que `WC_de` aplique también con NIIF; (2) una fila nueva del libro V6.3.1 (como las 86–88) con el circulante normalizado, escrita por `f1_libro_v631.py aplicar`, usada por la fila 30, C58 y C53, con su referencia, su verificador y la prueba de igualdad A0 regenerados (plantilla nueva → expediente nuevo); (3) decidir si el ajuste entra también en el ancla de S2C (2021–2025) y cómo lo tratan K3a y K3c; (4) pruebas con mutaciones y revisión independiente.
- **(b)** Solo el expediente: la persona revoca M43; C46 = media 2023–2025 de CFO + dividendos de no consolidadas = 11.417,333 (cálculo declarado, la misma vía que hoy sin el término de la fila 14), C40 coherente 6.628; expediente nuevo con `cambiar_base.py` (o el mismo con una corrección registrada) y relanzar desde el paso 2. Con (b), K3c NO deja de saltar: la reinversión sigue en −1.514,333 con ventas al alza, así que K3c BLOQUEA igual y haría falta además una justificación, esta vez coherente (la caja base sí cuenta el circulante y la reinversión también: una sola vez).
- **(c)** Solo el expediente: la persona declara la hipótesis (salida de circulante de ≈ 2.090/año en la proyección, con su cota +2.175 mm/año de flujo sin crecimiento frente a a/b) y su texto entra en `justificacion_reinversion_negativa` como decisión de la persona; F1-K3c queda en aviso.

Pregunta formulada al usuario por el coordinador: V-CIRC (auxiliar, f2e8312). Este diagnóstico no la contesta.
