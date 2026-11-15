# Decisiones pendientes · revisión financiera del piloto Vidrala (entrega 4.3; revisado en la 4.3.1)

Nada de lo que sigue se ha aplicado. No se ha tocado `personaje_v2/empresas_v2/`: ni extracciones, ni `fase1_decisiones.json`, ni libros, ni fases. La numeración sigue la de las entregas anteriores:
- P1–P6 y PE1–PE7: piloto, `contrastes/piloto_Vidrala_2025/`;
- P7–P11 y PE8–PE13: entrega 4.2, `contrastes/vidrala_2023_arrendamientos/`.

Cada punto lleva su tipo:
- **corrección factual:** un dato que no coincide con su fuente;
- **hipótesis propuesta:** un supuesto con su fundamento y su límite, que entraría como estimación justificada o como hipótesis;
- **decisión humana:** reservada a la persona responsable.

## 1. Correcciones factuales

| # | Qué | Evidencia | Estado | Recomendación |
|---|---|---|---|---|
| **P1** (piloto) | Historia K14: −127,840 → **84,994** | ES24 p.14; ESEF; EN25 p.7 (comparativo) | Respaldada; **aplicación pendiente** | Aplicarla en un expediente nuevo con cualquier motor. Afecta a `f`, a las filas 30 y 31, al S2C de referencia (C53: 1,55 → 0,92) y a la cuenta del S2C de la fase B |
| **P8** (4.2) | Página de D&A en `AR_2024.json` (p.4 → p.7) | Texto nuevo de la 4.2 | Pendiente (tipo A; sin cambio de valor) | Incluirla en el mismo expediente nuevo |
| **P12** | Documentación: D&A afecta a la reinversión (C76), no al NOPAT (C75) | Fórmulas de Historia C75 y C76 | **Aplicada en esta entrega**, solo en dos documentos de la 4.2 (ver `ANEXO_REPRODUCIBLE.md`, §6) | — |
| **P13** | Cita de la plusvalía en `fase_a.md` («[CF_2025, PDF p.31, 64]») | EN25 p.31: «a gain of 50 million euros» | **Correcta**; no requiere acción | — |
| **P23** (4.3.1) | Control maestro, C37: el campo «periodo» dice «Cierre 09/10/2026», pero la fuente es una cotización intradía del 3-nov-2026 a las 10:13. La nota llama al precio «con derecho» | `datos_v63.json`; BORME 28-oct-2026 (período de asignación desde el día siguiente a la publicación) | Discrepancia documental. «Con derecho» queda contradicho por el BORME (interpretación sobre la fecha sin derecho; E2) | Corregirlo en el expediente nuevo cuando se obtengan E1 y E2 |
| **P24** (4.3.1) | Fase A, Palancas C47: «liberada 1×20 aprobada y no ejecutada a 9-oct… a ojo, un 3 %, dentro de la tolerancia del 5 %» | BORME: ejecutada (1.760.312 acciones nuevas) | El supuesto queda superado por un hecho. La liberada sola ya supone un 5 % | Volver a decidir C47 en la fase A con E1–E3 |

## 2. Hipótesis propuestas

Cada hipótesis se decide **por separado**. No se pide aceptar un conjunto.

| # | Hipótesis | Fundamento | Supuesto que añade | Límite y riesgo | Recomendación |
|---|---|---|---|---|---|
| **P14** | **Solo si se mantiene el motor A:** perímetro de continuadas para `f` (T3). C46 = 322,65; J14 = 85,978; K14 = 36,487 | CFO − explotación de Italia (ES24 p.43); FAC − discontinuadas (ES24 p.11 y p.14) | **δ = 0**, que es una hipótesis: no se publica la parte de Italia en los intereses e impuestos pagados | J14 y K14 serían derivadas (residuos), no publicadas. T3δ (−0,0009 de `f`) es una sensibilidad condicionada, no una cota. **`f` = −0,009847, condicionada**: proyecta partidas de devengo cuya recurrencia no está acreditada (ni descartada) | Solo como contraste; no como base (informe, §6.4) |
| **P15** | C49 con el motor A: 4,5 como **hipótesis pendiente**; 6,8 y 0 como sensibilidades | Nota 8: pagos y devengo (4.2) | Que el interés de arrendamientos esté en «Pagos de intereses» | Omisión o duplicación de hasta ≈2,3/año; `f` de −0,0129 a −0,0083 con T3 (sensibilidad, no intervalo demostrado) | Mantener la etiqueta de hipótesis. Con el motor B, C49 no se usa |
| **P16a** | Motor B: el puente a **31-dic-2025** para una ruta **exploratoria** (ruta A) | Saldos contrastados (EN25 p.2, p.3 y p.52) | Que el ejercicio no se compare con el precio de 3-nov-2026 | E de `r_op` y D4 son de 3-nov-2026: no es una valoración íntegramente referida a 2025 | Aceptable solo para la ruta A, con la nota de fechas |
| **P16b** | L25 = 6,223 como aproximación del déficit neto de pensiones | EN25 p.71–72 | Que «otras obligaciones con empleados» sea inmaterial o equivalente a deuda | ≈0,2 % de C41; definición más amplia que la fila | Aceptable como hipótesis declarada en la ruta A. Obtener el desglose de prestación definida para la ruta B (pregunta 11) |
| **P16c** | Caja disponible: L24 tal cual, o L24 menos el dividendo a cuenta comprometido (43,338) | EN25 p.64: aprobado el 19-dic-2025 y pagado el 13-feb-2026 | Que la caja del balance esté disponible para el accionista | 1,4 % de C41. Si no se resta, la ruta A incluye un dividendo ya repartido | Decisión de definición; el personaje se inclina por restarlo (interpretación), sin aplicarlo |
| **P16d** | i = C63 (intereses de 2025 ÷ deuda media de 2024–2025) | Fórmula del libro (convención 4) | Que el coste histórico represente el futuro | No recoge la emisión de 2026 ni la deuda de Toro; no se sabe si incluye intereses de arrendamientos | Aceptable en la ruta A como convención declarada |

## 3. Decisiones humanas (con la recomendación del personaje)

| # | Decisión | Opciones | Recomendación | Por qué y con qué límites |
|---|---|---|---|---|
| **P17** | **Motor** (C62, fase A) | a) motor A con T3 (P14); b) **motor B**; c) motor A sin cambios | **b)**, como justificación **metodológica** | `f` no puede representar fugas recurrentes con datos acreditados de esta ventana: perímetro, partidas de devengo y tres regímenes de financiación. Es lo que prevén la convención 10 y el personaje. **Límites:** el motor B no resuelve las fechas, las acciones, Toro, L25 ni L26, y añade `r_op`. **La 4.3.1 retira la afirmación de la 4.3 de que «no falta ninguna evidencia»** |
| **P18** | **Ruta** | Ruta A: reejecución exploratoria con base 2025. Ruta B: análisis comparable con el precio de noviembre de 2026 | Ruta A ejecutable con encargo y con P1, P17 y P16a–d decididas. Ruta B solo cuando exista la evidencia de P21 | La ruta A no permite decidir: no da un precio de Sí comparable, ni zona, ni cubo. Ver `RUTA_DE_CONTINUACION.md` |
| **P19** | **Preguntas a Relación con Inversores** (§4) | Enviarlas o no | Opcional en la ruta A. Las preguntas 10 y 11 son necesarias en la ruta B; las 1–9, para cerrar el motor A o normalizar | No se ha enviado ninguna |
| **P20** (= P11) | Añadir a `verificar_paquete.sh` los scripts de 45, 217 y 43 comprobaciones | Sí o no | Sí, en un encargo que permita tocar la herramienta de verificación | Hoy se ejecutan a mano (anexo, §1 y §7) |
| **P21** | **Encargar la obtención de la evidencia de la ruta B** | Sí o no | Sí, antes de cualquier conclusión de compra o espera | Lista exacta en §5 |
| **P22** | **Cómo tratar el tiempo** en la ruta B | a) llevar el valor de 31-dic-2025 a la fecha del precio, restando las distribuciones; b) rebasar en una fecha de 2026 | Sin recomendación hasta tener los datos | Es una decisión de método: el motor no admite un primer año parcial |
| — | **Salvaguarda de P17** | — | La elección del motor se fija antes de ver valores. Que el valor de un motor resulte más favorable no sirve de argumento | El encargo prohíbe usar el cambio de motor para ocultar una discrepancia o conseguir un resultado favorable |
| — | **Ceros pendientes** (L26, C48 y P4) | — | Revisión humana. La IA no confirma ceros ni escribe `fase1_decisiones.json` | Evidencia candidata: EN25 p.3 (minoritarios); ESEF (intereses en explotación) |

P7 (circulante de 2023, 4.2) queda **superada**. La elección entre 78,805 y 89,866 no era la cuestión: cada cifra va emparejada con su presentación del CFO, y el circulante se anula con él (informe, §3.2).
- **Con el motor A**, el valor más coherente es el derivado de continuadas (P14, condicionado).
- **Con el motor B**, la fila 14 no entra en el valor; solo en las filas 30 y 31 y en las referencias de la fase B.

## 4. Preguntas redactadas para Vidrala (no enviadas)

| # | Pregunta | Qué decisión resolvería |
|---|---|---|
| 1 | ¿En qué líneas del estado de flujos consolidado de 2023, 2024 y 2025 se presentan los pagos por arrendamientos NIIF 16, separando principal e intereses? | C49 con el motor A (4,5, 6,8 o 0); P15 |
| 2 | ¿La línea «Pagos de intereses» (explotación) incluye los intereses de los pasivos por arrendamiento? | La diferencia entre 4,5 y 6,8 |
| 3 | En la nota 8 (2022–2025), la línea «Gastos por arrendamientos a corto plazo y de poco valor» repite el importe de los pagos del pasivo. ¿Es un error de presentación o hay un gasto adicional dentro del resultado de explotación? | El riesgo de duplicación con los dos motores (pequeño) |
| 4 | ¿En qué línea de explotación del estado de flujos de 2024 se revierte la plusvalía de la venta de Vidrala Italia (≈50 mm)? ¿Qué otros importes de Italia contiene «Otros activos y pasivos corrientes y no corrientes» (−106.417 miles)? | Confirma la interpretación por eliminación (informe, §3.1). No cambia ninguna réplica |
| 5 | ¿Cuál es la composición del flujo de inversión de las actividades interrumpidas de 2023 (−28.371 miles), frente a unas inversiones de Italia de 4.315 miles? ¿Cuál fue el capex de Italia en el primer semestre de 2024? | C47 y el FCF base de continuadas (solo con el motor A o para contexto) |
| 6 | ¿Qué parte de «Pagos de intereses» y «Pagos por impuestos sobre las ganancias» de 2023 y del primer semestre de 2024 corresponde a Vidrala Italia? | δ de P14 |
| 7 | ¿Qué actividad recoge el segmento «Italia» dentro de las operaciones continuadas de 2024 (ventas de 17.016 miles; BAI de 2.139 miles) y continúa en 2025? | El perímetro de las ventas y el EBIT de 2024 (≈1 %) |
| 8 | ¿A qué se debe la diferencia entre el impuesto corriente y el pagado (2023: 63.249 frente a 45.021; 2025: 56.136 frente a 40.757 miles): calendario de pagos fraccionados, devoluciones o créditos fiscales? | Si el componente fiscal de `f` es recurrente (solo con el motor A) |
| 9 | En la provisión de derechos de emisión, ¿qué parte de los derechos entregados fue gratuita y qué parte comprada? ¿En qué línea del estado de flujos van los pagos por compra de derechos (inversión en intangibles o explotación)? | Si las partidas no monetarias (X) que mueven `f` se repiten o se revierten (informe, §3.6) |
| 10 | Cristalerías Toro: ¿precio final, deuda asumida, pago aplazado (importe y calendario) y cuentas de 2025 y del primer semestre de 2026 (ventas, EBIT, D&A y capex)? | Perímetro de la base y puente de la ruta B |
| 11 | Plan británico de prestación definida a 31-dic-2025 y a 30-jun-2026: ¿obligación, activos del plan y otras obligaciones con empleados incluidas en la provisión de personal? | L25 (P16b) |

## 5. Evidencia que necesita la ruta B (P21)

Son fuentes públicas o de la empresa por obtener, conservar y contrastar. No son consultas que haya que enviar.

| # | Evidencia | Para qué | Estado |
|---|---|---|---|
| E1 | Cierre oficial de Vidrala del 3-nov-2026 (BME) | C37: sustituir la cotización intradía de una fuente secundaria | Ausente |
| E2 | Calendario de la liberada 1×20 de 2026: hecho relevante u «otra información relevante» de la CNMV, o documento informativo | Confirmar que el 3-nov-2026 cotizaba sin derecho | Ausente. El BORME (conservado) fija el período por referencia a la publicación |
| E3 | Autocartera y programas de recompra de 2026 (comunicaciones a la CNMV) | Acciones en circulación a la fecha del precio. La heredada (≈1,021 mm) no cabe en el programa documentado de 350.000 | Ausente |
| E4 | Informe financiero semestral 1S2026 (doc. 2487, identificado en el Control maestro) | Deuda, arrendamientos, caja, pensiones, Toro, dividendos y recompras a 30-jun-2026 | Identificado, no conservado ni contrastado |
| E5 | Información posterior al semestre, si se publica (por ejemplo, del tercer trimestre de 2026) | Acercar el puente a la fecha del precio | Sin examinar |
| E6 | Toro: precio, deuda asumida, pago aplazado y cuentas | Perímetro y puente | Pregunta 10 |
| E7 | Efecto neto de Kristin (seguros y ayudas) | Separar lo extraordinario del margen | Sin examinar |

## 6. Estado de los pendientes anteriores

| # | Pendiente | Estado tras esta entrega |
|---|---|---|
| PE1 | Efecto en los valores, el precio de Sí y el cubo | **Sigue abierto.** Lo resuelve la reejecución (P18) |
| PE2 · PE10 | Principal y clasificación de los arrendamientos | **Siguen abiertos**, pero no bloquean con el motor B (P15 y P17) |
| PE3 | Identidad byte a byte del `CF_2025.txt` original | Sigue abierto, fuera de este encargo |
| PE4 · PE11 | Datos de 2023 de las medias; ventas, EBIT y tipo de 2023 línea a línea | **Cerrados**: ES24 p.11 y p.14 (script, sección 2) |
| PE5 | Diferencias de circulante entre informe y comparativo (2022, 2023) | La de 2023 queda explicada y absorbida (P7 superada). La de 2022 no entra en la ventana |
| PE6 · P10 | Discrepancias de los documentos | Siguen como notas |
| **PE7** | Revisión financiera de una `f` negativa | **Hecha** (este expediente). Las decisiones pasan a P14–P17 |
| PE8 · PE9 | Perímetro de la columna 2023 | **Cerrados** (matriz de coherencia) |
| PE12 | Traducción inglesa de 2023 | Sigue abierto; irrelevante para las decisiones |
| PE13 | ESEF 2025 completo | **Cerrado**: conservado en `fuentes/esef_2025_completo/` y usado por el script |
| P2 | Detección del signo perdido en `numero()` | Sigue pendiente (requiere encargo de código) |
| P3 · P9 | Arrendamientos | Sustituidas por P15 y P17 |
| P4 | Cero heredado de `intereses_financiacion` 2025 | Sigue pendiente de revisión humana. La IA no confirma ceros; lo mismo vale para L26 (minoritarios) |
| P5 · P6 | Notas de los lectores; participadas | Siguen pendientes |
