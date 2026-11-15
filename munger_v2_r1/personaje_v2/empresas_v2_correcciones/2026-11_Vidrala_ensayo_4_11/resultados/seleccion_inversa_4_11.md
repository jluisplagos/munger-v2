# Selección inversa sobre una copia de un expediente V6.3 cerrado (revisión interna H1, §5.1)

- Origen (no se toca): `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10_1/Vidrala`, estado {'paso': 14, 'estado_analisis': 'concluido', 'auditoria': 'APROBADO'}.
- A la copia se le añade una `configuracion_economica.json` válida (la del piloto) y se lanza el pipeline con `config_v2_v64_experimental.json`.
- Código de salida: **2** (esperado tras la corrección: 2).
- Última línea: «SELECCIÓN DE PLANTILLA DETENIDA: el expediente ya tiene Vidrala_v63_base.xlsx, Vidrala_v63_datos.xlsx, Vidrala_v63_evaluada.xlsx (paso 14) y no tiene plantilla_activa.json: se preparó con la V6.3 y esta ejecución selecciona V6.4 experimental (config_v2_v64_experimental.json); un expediente solo se ejecuta con su plantilla: para la V6.4, prepara un expediente nuevo (cambiar_base.py, o una carpeta c»
- Archivos nuevos: 0 [] · archivos cambiados: 0 [].
- `plantilla_activa.json` escrito: no · estado después: {'paso': 14, 'estado_analisis': 'concluido', 'auditoria': 'APROBADO'}.

**Resultado: CONFORME.**
