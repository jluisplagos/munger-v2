# Reproducción del fallo de vigencia (encargo 4.12 §3) · código de `/home/claude/base_4_11/munger_v2_r1`

- Copia aislada de `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto` (el original no se toca), con el resumen y el registro de publicaciones reubicados en la copia.
- Alteración: configuracion_economica.json: PM1.lambda = 0.9 (inválida). Llamada: pipeline.py COPIA --config config_v2_v64_experimental.json (primera llamada, sin MUNGER_CONFIG).
- Código de salida: **2**.
- Salida:
```
SELECCIÓN DE PLANTILLA DETENIDA: configuracion_economica.json no es válida: PM1.lambda: número ≥ 1
```
- Después: estado {'paso': 14, 'estado_analisis': 'concluido', 'auditoria': 'APROBADO'} · ficha oficial presente · antecedentes [].
- Fila del resumen: ['APROBADO'].
- Archivos cambiados: 0 · nuevos: 0.

**Aprobación del material anterior retirada: NO (sigue constando como vigente).**
