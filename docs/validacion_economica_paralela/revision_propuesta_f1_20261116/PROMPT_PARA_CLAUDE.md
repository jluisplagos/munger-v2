# Munger V2 · reconciliar la propuesta de decisiones F1/Elis antes de aprobarla

Continúa en la sesión **Conciliación económica Elis/F1**, repositorio `jluisplagos/munger-v2`, rama `auditoria/economica-f1-frente-e`. La propuesta revisada es la de `b83803cd1c42c52c6ced6a538f5ae03ef706a644`. Si tu rama ha avanzado, conserva lo nuevo y contrasta si ya resuelve estos puntos; no restaures una versión antigua.

La revisión externa está en la rama `auditoria/revision-propuesta-f1`, directorio `docs/validacion_economica_paralela/revision_propuesta_f1_20261116/`. Recupera esa rama y lee `REVISION_PROPUESTA_F1.md`, `comprobaciones_sinteticas.json` y las pruebas/procedencias asociadas, sin fusionarla ni cambiar tu rama. El archivo `sondas_economicas.py` es investigación sintética, no una implementación del producto ni estimación de costes de Elis.

## Objeto y autorización

Reconciliar la **propuesta y su especificación**, para que la persona responsable pueda decidir sobre una política completa y comprensible. **Este encargo no adopta las decisiones económicas ni autoriza modificar la plantilla o liberar la valoración de Elis.** Continúan vigentes C48=108, C49, FCF base=307,933 y E1/D3/E2/E6. R, f y la conclusión afectada siguen pendientes mientras falte fundamento.

La revisión externa reprodujo los 349 archivos del manifiesto y las 292 comprobaciones del contraste, con salidas idénticas. No se encarga repetir una auditoría general de cifras ni investigar empresas nuevas.

## Correcciones concretas

1. **F1-P1 · inversión climática:** una categoría separada no puede quedar fuera de toda salida de caja. Revisa la recomendación (5b): clasificar según la finalidad documentada y mostrar dónde se cobra cada desembolso en la ventana, proyección y terminal, una sola vez. Si no hay importe/rango suficiente, pendiente; no asumir cero. No adoptar por el nombre que toda inversión climática es ajena al mantenimiento o que sea perpetua.
2. **F1-P2 · reposición de clientes y adquisiciones:** distingue gasto comercial ya incluido en EBIT, inversión propia necesaria, compra de cartera para sostener ventas y compra para crecimiento. Ningún euro puede omitirse ni cobrarse dos veces. Reconciliar «reponer clientes va en R», «su coste ya está en EBIT/capex» y «todas las compras son crecimiento». Si no hay desglose, decláralo y conserva el bloqueo; no inventes una tasa de bajas o R. Precisa el perímetro de R y las guardas que comparan R con capex. Explica si PPA constante significa euros o proporción de ventas, su relación con f y qué se sabe frente a qué se supone.
3. **F1-P3 · normalización:** 27,936 es el diagnóstico del cálculo actual, no un ajuste universal aprobado. Presenta los ajustes concretos propuestos con fuente, original/normalizado, motivo, fiscalidad y dependencias. No combines los 13,7 de earnout sin efecto fiscal con los ≈18,6 con efecto fiscal y un total sin reconciliar. Calcula conjuntamente lo que pueda calcularse en una copia de investigación; si falta un dato o política, pendiente. Conserva los históricos y las entradas registradas. La etiqueta «no recurrente» no sustituye la justificación económica ni la consideración de gastos relacionados.
4. **F1-P4 · coherencia completa:** sincroniza el texto de aprobación y E2–E5 sobre qué bloquea y qué solo avisa. No adoptes el umbral propuesto de 0,5 % sin decisión. Incluye el significado y compatibilidad del ROIC y los costes en el terminal, que no usa S2C. La media histórica de pagos de arrendamiento puede ser referencia de ensayo con sensibilidad 16,8; no presentarla como peso futuro identificado. No hace falta elegir ahora otro punto.

## Entregables y cierre

- `RESPUESTA_REVISION_PROPUESTA_F1.md`: respuesta a P1–P4, con lo corregido, evidencia y lo que siga pendiente. Si discrepas, argumento y ejemplo reproducible.
- `PROPUESTA_DECISIONES_F1.md` revisada y `ESPECIFICACION_F1_PROPUESTA.md` coherente con ella, **sin implementar**.
- Una tabla única de las decisiones (1a), (1b), (2), (3a), (3b), (4a), (4b), (5a), (5b): recomendación, dato/derivación/hipótesis/política, condición de aplicación, carencia y texto exacto que se pide aprobar. No pedir elegir una cifra para sustituir evidencia ausente.
- Extiende los controles sintéticos solo en lo necesario para comprobar correspondencia de caja, crecimiento cero, coste ya incluido en EBIT, adquisiciones de reposición y tratamiento terminal. Son ejemplos de política, no datos de Elis. Registra comandos y salidas reales.
- Actualiza manifiesto y recuperación; commit congelado y push. Concluye. No ampliar a Mistral, Qwen, otra empresa o una nueva auditoría general.

## Modelos, esfuerzo y trabajo independiente

Opus con esfuerzo alto para coordinación, redacción y cambios. Usa herramientas deterministas para cálculos y huellas. Reserva Fable con esfuerzo máximo para **una revisión económica independiente dirigida a P1–P4** si cambian justificaciones materiales, sobre el commit congelado y en contexto separado; avisa antes. Las tareas administrativas pueden usar menos esfuerzo. Registra solo la configuración realmente disponible, respetando las reglas del entorno.

No encadenes pasadas automáticas. Si esa revisión encuentra una carencia de datos o de política, documenta el bloqueo y termina; no inventes una solución para obtener aprobación. Las observaciones U1–U6 de la revisión 9 del verificador pueden tratarse como trabajo independiente ya abierto, pero no son evidencia de aprobación económica de esta propuesta. No cambies cifras o fórmulas de valoración en este encargo.

No envíes comunicaciones a Relación con Inversores ni a terceros. Puedes preparar preguntas concretas o identificar fuentes públicas recuperables; su envío no está autorizado por este encargo.
