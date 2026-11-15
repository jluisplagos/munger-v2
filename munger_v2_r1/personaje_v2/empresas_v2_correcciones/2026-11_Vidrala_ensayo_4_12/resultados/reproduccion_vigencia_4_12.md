# Reproducción del fallo de vigencia (encargo 4.12 §3) · código de `/home/claude/trabajo_4_12/munger_v2_r1`

- Copia aislada de `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto` (el original no se toca), con el resumen y el registro de publicaciones reubicados en la copia.
- Alteración: configuracion_economica.json: PM1.lambda = 0.9 (inválida). Llamada: pipeline.py COPIA --config config_v2_v64_experimental.json (primera llamada, sin MUNGER_CONFIG).
- Código de salida: **2**.
- Salida:
```
APROBACIÓN RETIRADA ANTES DE DETENER LA LLAMADA: el material cambió después de la auditoría (configuracion_economica.json): la aprobación no vale para la versión nueva · salidas oficiales archivadas en historial_cierres/01_6dd711561fd92f12
SELECCIÓN DE PLANTILLA DETENIDA: configuracion_economica.json no es válida: PM1.lambda: número ≥ 1
```
- Después: estado {'paso': 13, 'estado_analisis': None, 'auditoria': None} · ficha oficial archivada · antecedentes ['01_6dd711561fd92f12'].
- Fila del resumen: ['SIN APROBACIÓN VIGENTE · cierre anterior (APROBADO del material 6dd711561fd92f12'].
- Archivos cambiados: 7 · nuevos: 6.

**Aprobación del material anterior retirada: sí.**
