# Munger v2 · paquete de reparación H1–H3 · r1 · entrega 3.1 (continuidad)

> **Para continuar en una ventana nueva hay que leer primero `CONTINUIDAD.md` y usar `PROMPT_NUEVA_VENTANA.md`.** La verificación completa se hace con `bash verificar_paquete.sh completa` desde esta carpeta.

## Qué contiene
Es el paquete `munger_v2_paquete.zip` completo, con las reparaciones H2, H1 y H3 ya aplicadas. Se puede usar tal cual, en lugar del original, sin combinar parches.
- `REGISTRO_IMPLEMENTACION_H1-H3.md`: precisiones del contrato, cambios, pruebas, incompatibilidades y pendientes.
- `CAMBIOS_ARCHIVOS.txt`: lista generada de los archivos añadidos o modificados respecto a la base, con su SHA-256 antes y después. El resto de archivos son idénticos a la base, byte a byte.
- `VERSION`: identificador de la entrega.
- `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `verificar_paquete.sh`: punto de entrada, mensaje de arranque y verificación para una sesión nueva.
- `MANIFIESTO_SHA256.txt`: huella de cada archivo del paquete, que `verificar_paquete.sh` comprueba.
- `documentacion_reparacion/`: encargo inicial, diagnóstico, contrato e instrucciones posteriores (literales).

## Cómo comprobarlo
Requisitos: los mismos del proyecto (`bash personaje_v2/scripts/comprobar_entorno.sh`), es decir, Python 3 con openpyxl, lxml, pypdf y jsonschema, LibreOffice y pdftotext.

Desde la carpeta `personaje_v2/`:
```
bash pruebas/ejecutar_pruebas_reparacion.sh            # todas (≈ 4–5 min con LibreOffice)
bash pruebas/ejecutar_pruebas_reparacion.sh rapidas    # solo test_comprobadores.py: H2, H1 (con recorrido y reutilización) y H3 (≈ 1 min)
```
Las salidas se guardan en `personaje_v2/pruebas/resultados_reparacion/`. El script devuelve el código 0 si todo pasa.
Las pruebas escriben en el árbol: carpetas en `personaje_v2/pruebas/sintetico/` (como siempre ha hecho el proyecto), salidas en `personaje_v2/pruebas/` y el perfil de LibreOffice en `personaje_v2/.lo_perfil/`. Después de ejecutarlas, la comprobación del manifiesto daría archivos «de más». Por eso conviene ejecutarlas sobre una descompresión limpia y no repetirlas en la misma carpeta (véase `CONTINUIDAD.md`, sección 2).

## Qué cambia en el uso
- **Auditoría (H2):** el pipeline solo acepta APROBADO si `auditoria.md` trae los 16 puntos, cada uno una sola vez y todos en PASA, sin la palabra «FALLA» en ninguna parte, y con una única línea `Veredicto: APROBADO`. Una observación que no impide aprobar se escribe dentro de un punto en PASA, precedida de «Aviso:». El prompt de verificación ya lo indica.
- **Auditoría (cierre de H2):** ninguna otra línea puede tener forma de encabezado. Por ejemplo, «17. PENDIENTE», «100. PASA» u «8) PASA» dan REPETIR.
- **Extracción (H1):** cada `linea` tiene que estar en su página y cada importe tiene que aparecer completo. Cada cero lleva una `cita` literal de la página y queda **pendiente de verificación**. En el libro, ese cero y todo lo que depende de él aparecen como «Dato no verificable», y la fase C tiene que revisarlos.
- **Confirmar un cero:** solo puede hacerlo una persona, escribiendo en `fase1_decisiones.json` de la empresa una entrada como esta:
  `{"sbc": {"2025": {"valor_mm": 0, "fuente": "AR_2025.txt p. 41: «…»", "fecha": "2026-11-08", "confirmado_por": "<nombre de la persona>"}}}`
  Después se vuelven a ejecutar `fase1_historia.py construir` y el pipeline. Ningún agente ni script escribe ese archivo.
- **Reutilizar un libro ya rellenado (cierre de H1):** `rellenar_fase1_v63.py` reclasifica siempre las filas de Historia. Las celdas que dependen de un cero pendiente pasan a «Dato no verificable» sin cambiar su valor; solo `--sobrescribir` cambia el valor. Si una celda no puede actualizarse con seguridad, el script termina con el **código 5** y no escribe el libro; entonces hay que regenerar desde el libro base `<E>_v63_base.xlsx` o repetir con `--sobrescribir`.
- **Fuente independiente de una media o ratio:** para que no herede el pendiente de la Historia, su entrada en `fase1_metadatos.json` tiene que llevar `"independiente": {"fuente": "… p. N …", "fecha": "AAAA-MM-DD", "confirmado_por": "<persona>", "motivo": "…"}`.
- **Aarsleff corregido (H3):** el expediente nuevo está en `personaje_v2/empresas_v2_correcciones/2026-11_H3/Aarsleff/` (cinco años negativos y auditoría nueva APROBADO). `CORRECCION_H3.md` explica qué se cambió y cómo, y `../comparacion_H3.json` recoge la comparación completa con el original. El original `empresas_v2/Aarsleff/` se conserva sin cambios.
- **Las seis empresas analizadas no cambian.** Sus auditorías siguen leyéndose como APROBADO. Sus 134 ceros heredados están inventariados en `personaje_v2/empresas_v2_correcciones/ceros_heredados_H1.csv`, pendientes de verificación. No hay que volver a construir esos expedientes.

## Estado
H2 y H1 están cerradas y H3 está ejecutada; todas tienen pruebas. No queda ninguna parte del contrato pendiente. La sección 7 del registro recoge lo que queda fuera del alcance.
