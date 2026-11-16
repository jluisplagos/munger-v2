# Punto de recuperación · 4.15 hito 2

Actualizado: 16-nov-2026, tras las correcciones de la sexta comprobación (W1, W3–W5), rama `claude/hopeful-bardeen-qap6y0`.
Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente.

## Estado de las pruebas (hechos)

- Última regresión completa conforme: candidata `8196522` → **RESULTADO GLOBAL: PASA** (`resultados/verificacion_completa_8196522.txt`);
  reconstrucción de C48 con ese código: 8 casos iguales (`resultados/reconstruccion_c48_8196522/`).
- **Después** se corrigieron W3 (apóstrofo tipográfico, en el sentido de aceptar), W4 (apóstrofo en los límites de la cita), W5 (mensaje
  del máximo) y las pruebas de W1; se actualizaron `HITO_2_4_15.md` (pruebas, revisiones y límites declarados), `CONTINUIDAD.md` y
  `PROMPT_NUEVA_VENTANA.md`: **regresión completa de esta candidata pendiente** (no se da por superada).
- Baterías dirigidas sobre el árbol actual: entradas 4.15 **190/190**, entrada efectiva **61/61**, entradas 4.14 33/33. Mínimos: 190, 61 y 5.
- Registros reales: diagnóstico idéntico byte a byte; inventario de signo igual; PDF reales: 0 rechazos falsos.
- Control de la entrega 4.14: 29/35 (3 esperadas desde el hito 1; 3 por fechas que Git no conserva). No se da por superado.

## Revisiones independientes (Fable, esfuerzo máximo, agente distinto del autor, con aviso)

- Primera pasada sobre `c2d2b96`: ACEPTABLE CON CORRECCIONES (H1 y H2 importantes; H3–H14 menores u observaciones),
  `revision_independiente/hito2/REVISION_FABLE_HITO2.md`. Corregidos en `d54ee13`: H1, H2, H4, H5, H6, H7 (salvo clases CSS), H8, H9 (en
  parte), H10, H14. Declarados como límites: H3, H7 (clases CSS y otros rechazos conservadores), H11 (en parte), H12.
- Segunda pasada (solo lo cambiado tras la primera) sobre `92b2362`: ACEPTABLE CON CORRECCIONES (H1 y H2 corregidos; N1–N11 menores u
  observaciones), `revision_independiente/hito2/REVISION_FABLE_HITO2_SEGUNDA.md`. Corregidos ahora: N1, N2, N3, N4, N5, N6, N9, N10, N11
  (auxiliares sin uso) y N7 en parte (pruebas de H1 en calcular_entrada, H9 con registro apto y mutaciones m12, m16, m17, m20, m22, m29 y
  H6 ±). Declarados: N8 (orden de orígenes en fórmulas anidadas; min(o, 0) dentro del límite U1), H3, H7 (clases CSS), H12 y m47.
- Tercera comprobación (solo lo cambiado, `f3d15e8`): ACEPTABLE CON CORRECCIONES; pidió otra pasada corta por T1 (U7) y T3 (XHTML y
  códecs), que abrían huecos hacia lo permisivo, T2 (discrepancias falsas) y T4 (`REVISION_FABLE_HITO2_TERCERA.md`). Corregidos: T1, T2,
  T3, T4, T6, T7, T8, T9, T10 y T5 en parte (pruebas de N1, N3, N10, T1, T2, T4).
- Cuarta comprobación corta (`7a6583b`): ACEPTABLE CON CORRECCIONES (menores; T1–T4 corregidos; Q1 a corregir; Q2 pruebas; Q3–Q6
  observaciones), `REVISION_FABLE_HITO2_CUARTA.md`. Corregidos: Q1, Q3, Q4 y las pruebas de Q2 (T7 con registro apto, T3 en negativo,
  erratas dobles, coste, N3 con la cifra ausente en el documento). Declarados en el docstring y en el registro: los pendientes prudentes de
  T4, T8 y Q3, Q5 (erratas que fallan en cerrado) y los restos de Q6. Comprobación dirigida
  (`876bfc2`): ACEPTABLE CON CORRECCIONES, sin cambios de código exigidos; V1, V2 (en el sentido de aceptar), V3, V5–V7 y pruebas (V4)
  (`REVISION_FABLE_HITO2_QUINTA.md`). No se dejan como límites los que aceptan: corregidos V1, V2, V3, V5, V7 y las pruebas de V4; V6
  (pendientes prudentes) declarado en el docstring. Comprobación dirigida de V1–V7
  (`8196522`, 6.ª pasada): ACEPTABLE CON CORRECCIONES, sin cambios de código exigidos ni otra pasada (`REVISION_FABLE_HITO2_SEXTA.md`):
  W1 (pruebas que no fijaban V2 y V5) y W2–W6 a declarar; solo W3 iba en el sentido de aceptar. Corregidos W1, W3, W4 y W5; W2 y W6
  declarados en `HITO_2_4_15.md`. **Pendiente: comprobación dirigida de minutos de W1 y W3–W5 por otro agente** (e3, e7, e9, d7, las tres
  baterías y el diagnóstico).

## Incidencias y requisitos pendientes (no cerrados)

- **Comprobación dirigida de W1 y W3–W5** (otro agente) y **regresión completa** de la nueva candidata: pendientes.
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

## Incidencia de ejecución

- 16-nov-2026: un reinicio del contenedor cortó la regresión completa y la cuarta comprobación de la candidata `7a6583b` antes de que
  terminaran; sus resultados se perdieron y no se dan por obtenidos. Tras el reinicio, el árbol de trabajo seguía conforme (7321/7321) y la
  rama en `7a6583b`; se rehicieron las copias congeladas y se relanzaron los dos trabajos desde cero.

## Siguiente paso exacto

1. Regenerar manifiesto y congelar una copia limpia.
2. En paralelo: regresión completa y comprobación dirigida de W1 y W3–W5 por un agente distinto del autor (Fable, esfuerzo máximo, sin
   LibreOffice).
3. Si ambas pasan sin correcciones de código: reconstrucción de C48 con el código final, nota final en `HITO_2_4_15.md`, manifiesto
   final, paquete de cambios comprobado sobre la base 4.14, commit y push con el resumen para la revisión externa.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
