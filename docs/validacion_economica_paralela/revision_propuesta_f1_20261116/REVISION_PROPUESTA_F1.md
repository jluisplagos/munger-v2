# Revisión de la propuesta de decisiones F1/Elis

16-nov-2026. Material revisado: `auditoria/economica-f1-frente-e`, commit **`b83803cd1c42c52c6ced6a538f5ae03ef706a644`**, en particular `PROPUESTA_DECISIONES_F1.md` (SHA-256 `f2d8c8159f56ffdd5742b1926477683a609cdc44be0dfcb92fea43000131f795`). Se consultaron el informe, la especificación y las fuentes conservadas. Esta revisión no registra decisiones humanas ni modifica el motor.

## Dictamen

**No recomiendo aprobar en bloque la propuesta tal como está.** Es correcto corregir el doble cómputo de arrendamientos bajo las premisas documentadas, exigir coherencia de perímetros y mantener R y la valoración de Elis pendientes. Antes de adoptar la política completa, faltan precisiones que aseguren que ningún coste se omite o se paga dos veces.

La conclusión actual de bloqueo se conserva: no se ha encontrado una valoración de Elis que deba liberarse. Lo observado a continuación son huecos de definición de la **propuesta no implementada**, no fallos demostrados de una implementación nueva.

## Evidencia comprobada

- Manifiesto del frente E: **349/349** archivos conformes.
- Libro de referencia: SHA-256 `d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385`.
- Se ejecutó `scripts/contraste_f1.py` con el CSV, su verificación, el libro en lectura y el resultado ya conservado de caja no nula: **292 comprobaciones, 0 fallidas** (127 de fuente, 136 de libro, 29 algebraicas). Los JSON e informe regenerados son idénticos byte a byte a los publicados. Se utilizó el registro anterior de la prueba de caja; **no se ejecutó LibreOffice de nuevo**.
- Se verificaron huellas de los PDF consultados. Se examinaron, entre otras, URD2025 páginas PDF 122, 309, 364, 366, 368, 369, 393 y 141, y DEU2024FR p.337. La selección sirve a esta revisión concreta; no se afirma una nueva auditoría completa de las cinco publicaciones.
- La fuente confirma gasto del plan climático dentro del capex y planes con inversión superior a la amortización histórica (URD2025 p.122 y p.369). No publica en esos pasajes un importe separado del plan.
- Confirma PPA de clientes 83,5, marcas 2,2 y cartera neta de clientes 275,1 (p.364), pagos principales y nuevos derechos de uso (p.366), y monitorización de bajas de clientes sin tasa en el pasaje examinado (p.141).
- La práctica de deterioro de Elis usa un DCF de CGU con EBITDA, inversión incluida renovación de arrendamientos y WACC (p.368). Apoya contar el coste una sola vez; **no valida por sí sola todo el flujo al accionista del motor A**.

## F1-P1 · Una categoría de transición no puede dejar su caja fuera del modelo

La propuesta §5 recomienda inversión climática «fuera de R y del crecimiento», con importe y horizonte pendientes. Es admisible separar una categoría analítica; no está justificado concluir por su nombre que toda inversión climática es ajena a reposición o a conservar el negocio. Puede haber proyectos con finalidades distintas.

Falta especificar **dónde se resta el desembolso**, con qué horizonte y cómo se evita restarlo de nuevo si ya está en R, capex o margen. El motor actual usa f, inversión de crecimiento y terminal: una categoría sin término ni correspondencia de caja puede desaparecer a crecimiento cero.

Contraejemplo sintético, no estimación de Elis: EBITDA 100, capex propio de mantenimiento 20, pagos de arrendamiento 12 y transición necesaria adicional 7. Caja sostenible del escenario: **61**. Si los 7 se excluyen de R y del crecimiento sin otro cargo, el flujo proyectado ilustrativo queda **68**. Incluirlos una vez en R o como salida separada devuelve 61. Esto no significa que todo capex climático real sea perpetuo o de mantenimiento: exige clasificar y conservar su caja con evidencia.

**Corrección necesaria:** documentar la correspondencia de categorías y términos, tanto en la ventana como en años proyectados y terminal. Una salida material sin importe o rango defendible sigue pendiente; ni cero ni desaparición por categoría. La decisión (5b) puede crear una clasificación de trabajo, pero no autorizar esa omisión.

## F1-P2 · Precisar qué reposición se paga en EBIT, R y adquisiciones

La propuesta §2 dice que reponer clientes perdidos está en R; su fundamento dice que el coste comercial ya está en EBIT y en capex propio. §4 declara todas las compras de sociedades como crecimiento. El informe §6.3 admite que la reposición puede hacerse orgánicamente o con adquisiciones. Es necesario reconciliar estas frases antes de adoptarlas.

1. **Gasto comercial corriente:** si está en el EBIT proyectado, no añadirlo otra vez a R. R debe identificar inversión/desembolsos adicionales que no estén ya cobrados por otra vía. No confundir «coste económico de conservar clientes» con «todo ese coste pertenece a capex/R».
2. **Adquisiciones:** «total frente a orgánico» no resuelve por sí mismo cuánto repone una cartera y cuánto amplía ventas. Si una compra fuera necesaria para mantener ventas, no puede desaparecer al hacerse ΔV = 0. Si se adopta como hipótesis que todas las compras futuras son crecimiento, declararla y fundamentarla; no elevarla a dato por haber compras todos los años.
3. **PPA:** su amortización no es caja ni demuestra un coste de reposición del mismo importe. Tampoco demuestra que el cliente se mantenga gratis. La propuesta puede separar ambos conceptos, pero necesita una correspondencia de los desembolsos reales y una hipótesis de proyección explícita. La evidencia histórica parcial no identifica su cuantía futura.

Ejemplos sintéticos ejecutados:

- Si EBITDA 100 ya incluye gasto comercial 5, añadir otros 5 a R reduce indebidamente el flujo de 68 a 63.
- Si una compra de cartera 9 fuera necesaria para conservar ventas, tratarla solo mediante ΔV/S2C deja 68 donde el escenario exige 59. Incluirla una sola vez en la reposición o en un término de caja explícito resuelve ese caso.
- En ese segundo ejemplo R total puede ser 29 con capex propio 20, sin que haya infrainversión: incluye una compra de cartera. Por tanto, el significado de R y el denominador usado en sus guardas deben coincidir. No se pide adoptar ese perímetro en Elis sin datos.

**Corrección necesaria:** una correspondencia de cada coste entre margen, R, crecimiento/adquisiciones y flujos, sin omisiones ni doble cargo. Separar política propuesta, evidencia publicada y carencias M1/M2. Aclarar «PPA constante»: el término de f se escala con ventas; constante en euros y constante como proporción no son la misma hipótesis.

## F1-P3 · La normalización requiere una regla y un cálculo completos

Se reproduce **27,936** como diagnóstico de las partidas de la ventana en el cálculo actual: +13,675 de earnout y otros en f, −4,032 de plusvalías en f y +18,293 de plusvalía en m0. Es una descomposición del cálculo conservado, **no prueba que aprobar una normalización produzca exactamente −27,936** con cualquier política fiscal.

La propuesta también cita ≈18,6 para el earnout con su efecto fiscal, frente a 13,7 sin él. Si se cambian numerador/denominador del tipo efectivo, f o m0, el resultado debe recalcularse conjuntamente con una regla fiscal explícita. La fuente francesa confirma complementos de precio no deducibles (DEU2024FR p.337); no corresponde mezclar ambas sensibilidades y deducir una constante sin puente.

Además, una etiqueta de «no recurrente» publicada no basta por sí sola para demostrar que el efecto económico no se repetirá. Si se normalizan seguros, bajas de activos y adquisiciones, explicar la relación con los desembolsos y las reposiciones correspondientes y aplicar la regla de forma simétrica. No se exige una investigación genérica nueva: identificar los ajustes concretos propuestos y lo que los datos permiten afirmar.

**Corrección necesaria:** propuesta de ajustes con original, normalizado, fuente, motivo, tratamiento fiscal y dependencias; calcular su efecto conjunto en una copia de investigación, conservando datos históricos y decisiones registradas. Si no puede calcularse aún, el impacto final queda pendiente, sin reemplazarlo por el diagnóstico 27,936.

## F1-P4 · Sincronizar controles, supuestos y terminal

- **Arrendamientos, decisión 1b:** la media escalada da ≈161,120 frente a 177,9 pagados en 2025: diferencia **16,780**. Ambos hechos se reproducen. Elegir la media sigue siendo una hipótesis/convención; no demuestra el peso futuro de arrendamientos. Puede conservarse como referencia de ensayo, con sensibilidad y límites. No hace falta elegir un nuevo punto para cerrar esta revisión.
- **Controles:** el texto de aprobación sugiere que los casos que no cumplen controles no usan motor A, pero E5 mantiene avisos en V-F1g (ancla de otro perímetro) y propone un umbral de 0,5 % en V-F1a. Antes de adoptar la política, fijar qué bloquea, qué informa y cómo se trata una incoherencia material. **Esta revisión no adopta ese umbral.** Un aviso no debe presentarse como prueba de coherencia.
- **Terminal:** el motor reinvierte por g/ROIC, además de f, y no por S2C. La coherencia de margen/f/S2C debe extenderse al tratamiento de los costes y al significado de ROIC en el terminal. No se pide estimar un ROIC nuevo sin fuente; documentar la compatibilidad o dejar la conclusión afectada pendiente. Los ejemplos a crecimiento cero son controles útiles también para detectar costes recurrentes que desaparezcan en el terminal.

## Recomendación sobre las nueve decisiones solicitadas

| ID | Recomendación del revisor; no es decisión humana registrada |
|---|---|
| 1a | A favor de preparar la corrección de definición (b), conservando FCF base/C48/C49; precisar P1–P4 antes de adoptar la política completa. Mantener el bloqueo del motor para el uso no validado. |
| 1b | Media como referencia de ensayo con sensibilidad; no presentarla como coste futuro identificado. |
| 2 | Separar PPA no monetaria de reposición económica; adopción de su política y margen pendiente de la correspondencia de costes e hipótesis explícitas de P2. |
| 3a | **Mantener R y la valoración de Elis pendientes**. 736,0–867,2 no es una horquilla validada de elección. |
| 3b | Obtener el dato o una estimación documentada si se quiere desbloquear Elis. Se puede preparar la solicitud o investigar fuentes públicas; esta revisión no envía mensajes ni encarga una gestión externa al usuario. |
| 4a | A favor de la coherencia de perímetros, incluyendo el tratamiento terminal. |
| 4b | No adoptar todavía «todas las adquisiciones son crecimiento»: distinguir política y mantenimiento/reposición o demostrar que la restricción elegida es pertinente. |
| 5a | A favor de estudiar normalización documentada y simétrica; no adoptar la deducción automática de 27,936 sin la regla y el cálculo de P3. |
| 5b | Categoría analítica separada, si resulta útil, **con su caja siempre identificada**; no excluir costes materiales del modelo por su etiqueta. |

Estas recomendaciones no aprueban A1, A2, A1′, un valor de R o una valoración. La ausencia de M1/M2 impide cerrar Elis; no exige dejar sin terminar el mecanismo general ni declarar pendientes a expedientes independientes que sí cumplan su propia validación.

## Continuación finita

`PROMPT_PARA_CLAUDE.md` contiene el encargo completo para reconciliar la propuesta y la especificación, con las ilustraciones sintéticas. No ordena implementar decisiones sin aprobación, no repite la auditoría general del verificador y no abre ciclos recursivos. Se conservan los trabajos válidos y se revisará después únicamente lo modificado y sus dependencias.
