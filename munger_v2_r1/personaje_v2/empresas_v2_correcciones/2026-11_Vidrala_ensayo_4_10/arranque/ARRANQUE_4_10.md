# Arranque de la entrega 4.10 (11-nov-2026)

**Base:** `munger_v2_r1_entrega4.9_integridad_auditoria_y_N4.zip`, recibida con el nombre `munger_v2_r1_entrega4_9_integridad_auditoria_y_N4.zip` (guion bajo en lugar de punto). El contenido es el mismo.

**Comprobado al empezar** (encargo §2: no se repitió la tanda histórica como ceremonia de arranque):
- **Tamaño:** 115.641.984 bytes.
- **SHA-256:** `8a48158996a955a0ad1a1e54080f0b1b73729fe3750d75b1457b2514cc552ea5`, igual al del encargo y al del `.sha256` adjunto.
- **CRC:** `unzip -t`, sin errores en las 1.981 entradas.
- **VERSION:** «munger_v2 · r1 · entrega 4.9 …».
- **Manifiesto:** 1.733 archivos.
  - Extracción limpia con `unzip`: 0 modificados, 0 ausentes, 0 de más. Se conserva sin escritura.
  - Extracción de trabajo con `unzip`: igual, e idéntica a la limpia.
  - Extracción con Python `zipfile` predeterminado: 0 modificados, **1 ausente** (`…/2026-11_Vidrala_ensayo_4_9/auditoria_interna/material_vigencia_2/ejecuciones/n4_paginas_reales_engaños.txt`) y **1 de más** (el mismo nombre como `enga├▒os.txt`).
- **Referencias críticas:** el libro de referencia, `…_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx`, reproduce la referencia mecánica (`variantes/variantes_4_10.json`, variante «base»).

**Causa de la incidencia** (comprobada leyendo el ZIP con `zipfile`): esa entrada guarda su nombre con bytes UTF-8, pero con el bit 11 de los indicadores a 0 y sin campo extra Unicode (0x7075). Es la única entrada con un nombre no ASCII.

**Qué se hace con ella:**
- El ZIP original no se modifica y el archivo de la 4.9 no se renombra.
- Se trabaja sobre la extracción con `unzip`, que recupera el nombre.
- El productor del ZIP nuevo se corrige (`scripts/empaquetar_zip.py`; `INFORME_CORRECCIONES_TECNICAS_4_10.md` §3.1).

**Verificación completa del árbol 4.9** (una vez, antes de este encargo, en la conversación de arranque):
- `verificar_paquete.sh completa`: PASA, código 0.
- Controles históricos: idénticos a sus referencias; 4.9 con 39 de 39.
