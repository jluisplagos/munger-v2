# Punto de recuperación · 4.15 hito 2

Actualizado: 15-nov-2026, tras el commit `878be1a` de la rama `claude/hopeful-bardeen-qap6y0` (creada desde `revision/4.15-hito1`).
Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente (se concilia en otra tarea).

## Estado de las pruebas (hechos)

Candidata estable `92b2362` (manifiesto 7113/7113, sin archivos de más), `bash verificar_paquete.sh completa`:
**RESULTADO GLOBAL: PASA**, código 0 (`resultados/verificacion_completa_estable_92b2362.txt`):
manifiesto, entorno, piloto (35 CUMPLEN); comprobadores 114/114; sintética 30/30 (nombres de la línea de base); H5 59/59; juicio 27/27;
entradas 4.14 33/33; entradas 4.15 **159/159**; entrada efectiva **58/58**; relevo caducado **5/5** (nueva); integración V6.4 199/199;
trazabilidad 78/78; integridad 103/103; auditorías 55/55; estados 28/28; resumen 45/45; cierre 55/55.

Otras evidencias en `resultados/`:
- reconstrucción de C48 con el código estable (`reconstruccion_c48_estable/`): 8 casos iguales al hito 1; C48 = 108 con y sin valores
  migrados, precio de Sí con diferencia 0;
- registros reales: diagnóstico de los tres expedientes finales e inventario de signo de los 7 registros, sin cambios frente al hito 1;
- mutaciones de H2 detectadas tras la corrección (`mutaciones_H2_tras_correccion.txt`);
- regresión de la primera candidata `c2d2b96`: FALLA en 5 bloques (`verificacion_completa_candidata_c2d2b96_FALLA.txt`), corregida
  (I20 ya no cambia salidas históricas; prueba I1 de cierre ajustada a I19) y repetida (`repeticion_cinco_baterias.txt`).
- Control de la entrega 4.14 sobre este árbol: 29/35. Tres son las esperadas desde el hito 1 (registros sin vínculos); las otras tres
  comprueban fechas de archivos que un clon Git no conserva (contenido idéntico al manifiesto 4.14). No es un fallo del código, pero no
  se da por superado.

## Revisiones independientes (Fable, esfuerzo máximo, agente distinto del autor, con aviso)

- Primera pasada sobre `c2d2b96`: ACEPTABLE CON CORRECCIONES (H1 y H2 importantes; H3–H14 menores u observaciones),
  `revision_independiente/hito2/REVISION_FABLE_HITO2.md`. Corregidos en `d54ee13`: H1, H2, H4, H5, H6, H7 (salvo clases CSS), H8, H9 (en
  parte), H10, H14. Declarados como límites: H3, H7 (clases CSS y otros rechazos conservadores), H11 (en parte), H12.
- **Segunda pasada (solo lo cambiado tras la primera) sobre `92b2362`: EN CURSO**, sin LibreOffice. Su informe irá a
  `revision_independiente/hito2/REVISION_FABLE_HITO2_SEGUNDA.md`.

## Incidencias y requisitos pendientes (no cerrados)

- **Segunda pasada de revisión**: pendiente de su dictamen. Si pide cambios de código, hay que corregir, revisar lo afectado y repetir la
  regresión completa sobre la nueva candidata.
- **H9 (parte abierta):** un relevo caducado vuelve siempre al paso 12; si cambian salidas de fases anteriores (fase_a/b/c, entrada
  efectiva) haría falta volver al paso que las consume. Propuesta sin aplicar (cambia el recorrido del pipeline).
- **U1:** no hay regla automática que acredite el significado económico de un derivado; lo acredita la revisión independiente de cada
  derivado al regenerar los registros.
- **U6 (a):** sin entrada_efectiva.json ni modo en los metadatos, el modo es «registrada» (visible en ficha e informe; el archivo está en el
  material auditado).
- **Regeneración y auditoría de los expedientes** Viscofan, Vidrala y Elis con extractor y revisor reales (sin firmas simuladas).
- **F1** (fuera de este frente, decisión y conciliación económica en otra tarea): el motor A no está validado.
- **Documentación de cierre del hito:** `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` (sigue siendo el de la 4.14) y
  `HITO_2_4_15.md` (borrador) por actualizar con los resultados finales; después, manifiesto y paquete de cambios.

## Siguiente paso exacto

1. Leer el dictamen de la segunda pasada y copiar su informe y sondas a `revision_independiente/hito2/`.
2. Si hay correcciones de código: aplicarlas con pruebas, revisión independiente de lo afectado y regresión completa sobre una copia
   limpia (sin `.lo_perfil` ni `__pycache__`; manifiesto regenerado antes).
3. Si no las hay: actualizar `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `HITO_2_4_15.md`; regenerar manifiesto y
   `CAMBIOS_ARCHIVOS.txt`; preparar el paquete de cambios con `scripts/empaquetar_cambios_4_15.py` (base 4.14) y comprobarlo sobre la base
   materializada; commit y push con el resumen para la revisión externa.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
