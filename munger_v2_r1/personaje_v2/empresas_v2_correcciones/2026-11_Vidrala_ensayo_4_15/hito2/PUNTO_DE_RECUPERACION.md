# Punto de recuperación · 4.15 hito 2

Actualizado: 16-nov-2026, tras la séptima comprobación dirigida (X1, X2, X3 y X5 corregidos), rama `claude/hopeful-bardeen-qap6y0`.
Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente.

## Estado de las pruebas (hechos)

- Regresión completa de la candidata `45ff57c` → **RESULTADO GLOBAL: PASA** (`resultados/verificacion_completa_45ff57c.txt`) y
  reconstrucción de C48 con su código: 8 casos iguales (`resultados/reconstruccion_c48_45ff57c/`). **Pero** `45ff57c` llevaba la regresión
  X1 (ver abajo), que la batería no veía: ese PASA no vale para la candidata final.
- **Después** se corrigieron:
  - **X1** (`verificacion_entradas.py:542`): al aplicar W3 se sustituyó el apóstrofo ASCII por el tipográfico en el límite inicial de la
    cifra de `_lectura_cifra`, en vez de añadirlo: «Total 1'849,7» volvía a contener 849,7 (en el sentido de aceptar). Repuesto
    `(?<!\d['’])`. `verificacion_entradas.py` queda con SHA-256 `4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd`, el
    archivo exacto que la séptima comprobación ejecutó con las tres baterías, los registros reales y sus sondas (árbol `fix7`).
  - **X2** (`test_verificacion_entradas_415.py`, prueba «(V3, V7)» y «(V5)»): los casos de la cita completa con el valor cortado, dos
    controles, los de W4 y el mensaje de W5, tal como los propuso el revisor (el número de pruebas no cambia: 190).
  - **X5** (`fase1_historia.importe_completo`, ya en la 4.14, en el sentido de aceptar): el apóstrofo de miles, ASCII o tipográfico, es
    parte del número. Prueba nueva en `test_entrada_efectiva_415.py` (62 pruebas; mínimo de `verificar_paquete.sh`: 62). Las mutaciones
    (sin el cambio, solo delante, solo detrás, solo ASCII) la hacen fallar. **No revisado todavía por otro agente.**
  - **X3** (registro): `HITO_2_4_15.md` §1, §4, §5 (tabla, criterio y límites) y §8, `CONTINUIDAD.md`, `VERSION` y `PROMPT_NUEVA_VENTANA.md`.
- Baterías sobre el árbol corregido: entradas 4.15 **190/190**, entrada efectiva **62/62**, entradas 4.14 **33/33**, comprobadores
  **114/114**. Registros reales con el código corregido: diagnóstico idéntico byte a byte, inventario de signo igual, PDF reales (q12 B):
  244/244 y 225/225, 0 rechazos falsos.
- **Regresión completa y reconstrucción de C48 de la candidata final: pendientes** (no se dan por superadas).
- Control de la entrega 4.14: 29/35 (3 esperadas desde el hito 1; 3 por fechas que Git no conserva). No se da por superado.

## Revisiones independientes (Fable, esfuerzo máximo, agente distinto del autor, con aviso)

- Pasadas 1.ª a 6.ª: tabla de `HITO_2_4_15.md` §5 e informes en `revision_independiente/hito2/`.
- **Séptima comprobación dirigida** (`45ff57c`): `REVISION_FABLE_HITO2_SEPTIMA.md` (con `sondas7/` y `salidas7/`). **Es un borrador:** el
  agente terminó con un error 529 (API sobrecargada) antes de rellenar §9 (integridad del árbol congelado). El dictamen, X1–X5, las
  baterías sobre `fix7` (190/190, 61/61, 33/33) y las diez mutaciones de W1 con la batería entera (nueve detectadas; `v7c`, no, por X2)
  sí estaban terminados y constan en `salidas7/`. Dictamen: ACEPTABLE CON CORRECCIONES; pide corregir X1 y X2 antes de cerrar, corregir el
  registro (X3), declarar X4 y declarar o corregir X5. No pide otra revisión completa: basta una verificación mecánica por otro agente.

## Incidencias y requisitos pendientes (no cerrados)

- **Verificación mecánica de X1/X2** (`sondas7/verificar_correccion_x1.py`, tiene que decir «CONFORME») y **comprobación dirigida de X5**
  y de la corrección del registro (lista de X3), por un agente distinto del autor: pendientes.
- **Regresión completa** y **reconstrucción de C48** de la candidata final: pendientes.
- **H9 (parte abierta):** un relevo caducado vuelve siempre al paso 12; si cambian salidas de fases anteriores (fase_a/b/c, entrada
  efectiva) haría falta volver al paso que las consume. Propuesta sin aplicar (cambia el recorrido del pipeline).
- **U1:** no hay regla automática que acredite el significado económico de un derivado; lo acredita la revisión independiente de cada
  derivado al regenerar los registros.
- **U6 (a):** sin entrada_efectiva.json ni modo en los metadatos, el modo es «registrada» (visible en ficha e informe; el archivo está en el
  material auditado).
- **Regeneración y auditoría de los expedientes** Viscofan, Vidrala y Elis con extractor y revisor reales (sin firmas simuladas).
- **F1** (fuera de este frente, decisión y conciliación económica en otra tarea): el motor A no está validado.
- Límites declarados de `HITO_2_4_15.md` §5.
- Tras la verificación: manifiesto final y paquete de cambios comprobado sobre la base 4.14.

## Incidencia de ejecución

- 16-nov-2026: un reinicio del contenedor cortó la regresión completa y la cuarta comprobación de la candidata `7a6583b` antes de que
  terminaran; sus resultados se perdieron y no se dan por obtenidos. Se rehicieron las copias congeladas y se relanzaron desde cero.
- 16-nov-2026: la séptima comprobación terminó con «API Error: 529 Overloaded»; se conserva el borrador tal como quedó.

## Siguiente paso exacto

1. Regenerar el manifiesto y congelar una copia limpia de la candidata con X1, X2, X3 y X5.
2. En paralelo: (a) regresión completa (`bash verificar_paquete.sh completa`) y, al terminar, reconstrucción de C48 (LibreOffice, en
   secuencia); (b) verificación mecánica de X1/X2 y comprobación dirigida de X5 y del registro por un agente distinto del autor (Fable,
   esfuerzo máximo, sin LibreOffice).
3. Si todo pasa sin correcciones de código: nota final en `HITO_2_4_15.md`, manifiesto final, paquete de cambios comprobado sobre la base
   4.14, commit y push con el resumen para la revisión externa.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
