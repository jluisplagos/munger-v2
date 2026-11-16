# Punto de recuperación · 4.15 hito 2

Actualizado: 16-nov-2026, tras las correcciones de la tercera comprobación (T1–T10), rama `claude/hopeful-bardeen-qap6y0`.
Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente.

## Estado de las pruebas (hechos)

- Última regresión completa conforme: candidata `f3d15e8` → **RESULTADO GLOBAL: PASA** (`resultados/verificacion_completa_f3d15e8.txt`);
  reconstrucción de C48 con ese código: 8 casos iguales (`resultados/reconstruccion_c48_f3d15e8/`).
- **Después** se corrigieron T1–T4 y T6–T10 de la tercera comprobación (`verificacion_entradas.py`, `ficha.py`, `pipeline.py`) y una
  fragilidad de la batería 4.15 a medianoche: la **regresión completa de esta candidata está pendiente** (no se da por superada).
- Baterías dirigidas sobre el árbol actual (sin LibreOffice): entradas 4.15 **178/178**, entrada efectiva **61/61**, entradas 4.14 33/33.
  Mínimos de `verificar_paquete.sh`: 178, 61 y 5.
- Registros reales con el código actual: diagnóstico idéntico byte a byte; inventario de signo igual; PDF reales de Elis y Viscofan: 0
  rechazos falsos.
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
  T3, T4, T6, T7, T8, T9, T10 y T5 en parte (pruebas de N1, N3, N10, T1, T2, T4). **Pendiente: cuarta comprobación corta de lo cambiado.**

## Incidencias y requisitos pendientes (no cerrados)

- **Cuarta comprobación independiente corta** (T1–T4 y lo tocado) y **regresión completa** de la nueva candidata: pendientes.
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

1. Regenerar manifiesto y `CAMBIOS_ARCHIVOS.txt` sobre el árbol limpio y congelar una copia.
2. En paralelo: regresión completa (LibreOffice en secuencia) y cuarta comprobación independiente (Fable, esfuerzo máximo, otro agente,
   sin LibreOffice) solo de lo cambiado desde `f3d15e8`, con las sondas que indicó la tercera (r2, r4b, r5, r7, r7b, r8, n2, n11, n12, r10).
3. Si ambas pasan sin correcciones de código: actualizar `HITO_2_4_15.md` (§4–§5) con los resultados, manifiesto final, paquete de
   cambios comprobado sobre la base 4.14, commit y push con el resumen para la revisión externa.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
