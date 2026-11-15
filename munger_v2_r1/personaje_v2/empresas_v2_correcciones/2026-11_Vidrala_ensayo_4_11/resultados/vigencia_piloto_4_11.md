# Vigencia del piloto 4.11 con el código final de la entrega

Comprobación solo en lectura, con las funciones que usan el pipeline y los generadores, después de las correcciones de la revisión interna.

- Expediente: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/Vidrala` · estado {'paso': 14, 'estado_analisis': 'concluido', 'auditoria': 'APROBADO'}.
- `cierre_v2.motivo_vigencia`: ninguno (el cierre sigue vigente).
- Selección de plantilla con `config_v2_v64_experimental.json`: conforme.
- Paso 12, variantes frente a `precio.json` (H10): corresponden.
- Celdas de configuración de los libros frente a `configuracion_economica.json`: iguales.
- Resumen registrado al publicar: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/resumen_v2.csv` (publicada). Con el código actual, una publicación nueva iría a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/resumen_v2_v64_experimental.csv` (H2).
- Archivos de `piloto/` examinados antes y después: 282 · ninguno cambió.

**Resultado: VIGENTE.**

**Nota.** Solo lectura. Las salidas del piloto (ficha, informe, entrada_v63.md, resumen) no se regeneran: ficha.py con el código actual escribiría una ficha de contenido distinto (los dos límites de R1, H12), y sustituir una ficha cerrada exige una auditoría nueva (Anexo D). Una ejecución nueva del piloto publicaría en el resumen del código actual.
