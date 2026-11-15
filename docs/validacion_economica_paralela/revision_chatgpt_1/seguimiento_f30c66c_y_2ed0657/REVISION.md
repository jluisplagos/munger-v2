# Seguimiento de ambos frentes

Versiones examinadas: económico f30c66c8651dba134b4e66fff9a08c2b50359b6c; técnico 2ed065769f6f6c52f27ac960f3d37ca05703d9c3. Ningún cambio del producto realizado por esta revisión.

## Económico: mejoras comprobadas

El autor añadió control separado de literal, ejercicio, unidad, perímetro y edición, y cotas de redondeo por identidad. Repetí42/42 casos de verificar_cifras y7/7 de residuos, con el resultado esperado. El último caso de residuos documenta que un error dentro de la precisión publicada puede no detectarse: no se interpreta como detección universal de cualquier error.

Repetí las dos sondas externas de un solo campo sobre las716 filas actuales. Cambiar la unidad de CREC_ORG_2025 de% a mmEUR ahora produceFALLO en unidad y código1; cambiar el perímetro de IS_VENTAS_2025 de grupoElis a segmentoFrancia produceFALLO en perímetro y código1. El rechazo ya no depende de mezclar esas mutaciones con un año falso.

Verificación completa ejecutada:716 filas,702OK,14PENDIENTE,0FALLO; código2. Los14 pendientes de unidad no impresa se conservan visibles, no se cuentan comoOK. El contraste usa363 entradas y ninguna pendiente.

Repetí el cálculo de contraste:236 comprobaciones,0fallidas (136libro,72fuente,28algebraicas). Los18 contrastes de caja no nula usan los resultados recalculados aportados por el autor, no una ejecución propia nueva de LibreOffice. Las identidades algebraicas no se presentan como prueba independiente de la veracidad de entradas.

La revisión efectiva del revisor sobre las correcciones sigue en curso según ESTADO.md; la pasada interrumpida no se cuenta. La adenda de f30c66c está pendiente de esa revisión. F1 continúa abierto: estos resultados no adoptan una política económica ni validan el modelo final para invertir.

## Técnico: mejoras comprobadas

El árbol reconstruido en nuestra copia desechable coincide con7113entradas del manifiesto;0ausentes/alteradas. Se conserva la base14 y no se modifica el entorno de Claude.

Las sondas propias tienen control positivo apto y rechazan página999999, fuente local ausente, página/cita negativas con valor_fuente positivo y la variante con cita recortada para ocultar el signo negativo. El último caso eraH1 de la revisión técnica y ahora produce discrepancia R415-SIGNO.

El commitd54ee13 también endurece las pruebas deH2 (una afirmación falsa de aptitud en el informe podía pasar). El autor aporta mutaciones que ahora se detectan; no repetí aquí esas baterías completas ni la regresión global. La revisión técnica recibida era sobre una candidata anterior; su aceptación condicionada no acredita automáticamente los cambios posteriores. Antes del cierre debe constar la revisión de lo afectado y la regresión de la candidata final, sin trasladar elPASA de una versión previa.

## Continuación

Los dos hallazgos de unidad/perímetro señalados externamente ya se rechazan en estos casos. No se añade un nuevo encargo ni se reinician las tareas. Corresponde dejar concluir las revisiones pendientes y fijar loscommits de cierre. Después: especificación económica, decisiones materiales con fundamento, integración, expedientes regenerados y auditoría final. Las conclusiones de esta nota están limitadas a las versiones y pruebas indicadas.
