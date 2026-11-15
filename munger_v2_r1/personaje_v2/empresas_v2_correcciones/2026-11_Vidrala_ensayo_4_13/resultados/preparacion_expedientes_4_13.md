# Preparación de los expedientes regenerados en la 4.13 (Hito 4)

## vidrala_condicionado
- `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/cierre_condicionado/Vidrala` → `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/vidrala_condicionado/Vidrala` (181 archivos, sin el perfil de LibreOffice).
- Cambio editorial en la configuración (huella económica igual: `e9bf4676b7fc7eb5…`): justificación de PM1.roic_terminal con la condición de Q-ROIC1 de la 4.9 y nota 4.13.
- Aprobación copiada: antecedente; la primera llamada la retira. Se sigue con `--desde 10` (variantes 4.13, fase C y auditoría nuevas).

## vidrala_bloqueo
- `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/cierre_bloqueo/Vidrala` → `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/vidrala_bloqueo/Vidrala` (183 archivos, sin el perfil de LibreOffice).
- Cambio editorial en la configuración (huella económica igual: `e9bf4676b7fc7eb5…`): justificación de PM1.roic_terminal con la condición de Q-ROIC1 de la 4.9 y nota 4.13.
- Aprobación copiada: antecedente; la primera llamada la retira. Se sigue con `--desde 10` (variantes 4.13, fase C y auditoría nuevas).

## viscofan
- Expediente nuevo `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/viscofan/Viscofan` (V6.4.1 experimental) con las entradas de partida de `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/viscofan/experimental/Viscofan`.
- Campos cambiados: fase1_v63.json: fecha_analisis, acciones_diluidas.fuente, capitalizacion.fuente, _notas; fase1_metadatos.json: fecha_analisis, acciones_diluidas.fuente, capitalizacion.fuente, _notas.
- Configuración: modo experimental · N1 0.221191 (escudo vinculado) · N2 vacío (Palancas C8) · R1 · P-M1 SR1 · Θ 0.5 · años Plana · terminal Proporcional a las ventas · perímetro NIIF 16 · cartera legado (altas [3.01, 1.633, 6.554, 6.419, 6.494]).
- Antecedentes para reutilizar (solo si sus entradas no cambian en lo económico): extracto_v63.md, fase_a.json, fase_a.md, fase_b.json, fase_b.md, datos_v63.md, entrada_v63.md, datos_v63.json.
- No se copia: libros, estado, fase C, auditoría, ficha, informe y resumen del 4.12 (el pipeline los genera de nuevo; la fase C y la auditoría, con agentes reales).
