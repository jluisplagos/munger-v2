# Punto de recuperación · 4.15 hito 2

Actualizado: 16-nov-2026, al cerrar el bloque técnico (código de `0a0020b`; después solo texto del registro), rama
`claude/hopeful-bardeen-qap6y0`. Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente.

## Estado de las pruebas (hechos)

- **Candidata final del código: `0a0020b`** (X1, X2 y X5 corregidos tras la séptima comprobación; `verificacion_entradas.py` SHA-256
  `4b00aa2a42ae45743ef4f31669faad36a7effb81affe828fd4975a2ca98c86cd`).
- Regresión completa de `0a0020b` (copia limpia, `bash verificar_paquete.sh completa`): **RESULTADO GLOBAL: PASA**, código 0
  (`resultados/verificacion_completa_0a0020b.txt`): manifiesto, entorno, piloto (35 CUMPLEN), comprobadores 114/114, sintética 30/30, H5
  59/59, juicio 27/27, entradas 4.14 33/33, entradas 4.15 190/190, entrada efectiva 62/62, relevo caducado 5/5, integración V6.4 199/199,
  trazabilidad 78/78, integridad 103/103, auditorías 55/55, estados 28/28, resumen 45/45, cierre 55/55.
- Reconstrucción de C48 con ese código: 8 casos, tabla idéntica a la de `45ff57c` (`resultados/reconstruccion_c48_0a0020b/`).
- Registros reales: diagnóstico idéntico byte a byte, inventario de signo igual, PDF reales (q12 B) 244/244 y 225/225, 0 rechazos falsos
  (reproducido por el autor y por la octava comprobación).
- Baterías dirigidas previas al commit: `resultados/baterias_tras_septima.txt`.
- La `45ff57c` también pasaba la regresión completa, pero llevaba la regresión X1, que la batería no veía: ese PASA no vale para la final.
- Control de la entrega 4.14: 29/35 (3 esperadas desde el hito 1; 3 por fechas que Git no conserva). No se da por superado.

## Revisiones independientes (Fable, esfuerzo máximo, agente distinto del autor, con aviso)

- Pasadas 1.ª a 6.ª: tabla de `HITO_2_4_15.md` §5 e informes en `revision_independiente/hito2/`.
- **Séptima** (`45ff57c`, borrador por un error 529 de la API): ACEPTABLE CON CORRECCIONES; X1 y X2 (código y pruebas), X3 (registro),
  X4 (declarar), X5 (permisivo, ya en la 4.14). Corregidos X1, X2, X3 y X5; X4 declarado.
- **Octava** (`0a0020b`, `REVISION_FABLE_HITO2_OCTAVA.md`, `sondas8/`, `salidas8/`): ACEPTABLE CON CORRECCIONES, **solo de declaración**;
  sin cambios de código ni otra pasada. Verificación mecánica de X1/X2: CONFORME. X5 conforme. Y1, Y2 y Y4 declarados después en el
  registro (solo texto); Y3 (dos controles más en la prueba de X5) no aplicado: opcional y prudente. La octava no ejecutó las partes de
  `test_comprobadores.py` que lanzan LibreOffice (el 114/114 consta en la regresión completa).

## Incidencias y requisitos pendientes (no cerrados)

- **H9 (parte abierta):** un relevo caducado vuelve siempre al paso 12; si cambian salidas de fases anteriores (fase_a/b/c, entrada
  efectiva) haría falta volver al paso que las consume. Propuesta sin aplicar (cambia el recorrido del pipeline).
- **U1:** no hay regla automática que acredite el significado económico de un derivado; lo acredita la revisión independiente de cada
  derivado al regenerar los registros.
- **U6 (a):** sin entrada_efectiva.json ni modo en los metadatos, el modo es «registrada» (visible en ficha e informe; el archivo está en el
  material auditado).
- **Regeneración y auditoría de los expedientes** Viscofan, Vidrala y Elis con extractor y revisor reales (sin firmas simuladas).
- **F1** (fuera de este frente, decisión y conciliación económica en otra tarea): el motor A no está validado.
- Límites declarados de `HITO_2_4_15.md` §5; Y3 opcional.
- Control de la entrega 4.14: 29/35.

## Incidencias de ejecución

- 16-nov-2026: un reinicio del contenedor cortó la regresión completa y la cuarta comprobación de `7a6583b`; se relanzaron desde cero.
- 16-nov-2026: la séptima comprobación terminó con «API Error: 529 Overloaded»; se conserva el borrador tal como quedó.

## Siguiente paso exacto

1. Revisión externa del hito 2 sobre esta rama (o sobre el paquete de cambios frente a la base 4.14 que describe `HITO_2_4_15.md` §6).
2. Lo que decida la persona responsable sobre: F1 (otra tarea), regeneración de expedientes con extractor y revisor reales, e I19/H9.
   Este frente no inicia ninguno por su cuenta.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
