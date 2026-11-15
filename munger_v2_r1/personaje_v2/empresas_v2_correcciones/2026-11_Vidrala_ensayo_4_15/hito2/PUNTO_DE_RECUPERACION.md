# Punto de recuperación · 4.15 hito 2

Actualizado: 15/16-nov-2026, tras la regresión completa de la candidata `f3d15e8` (PASA), rama
`claude/hopeful-bardeen-qap6y0`. Aptitud: uso supervisado experimental; **no apto para dinero real**. F1 queda fuera de este frente.

## Estado de las pruebas (hechos)

- Última regresión completa conforme: candidata estable `92b2362` → **RESULTADO GLOBAL: PASA** (`resultados/verificacion_completa_estable_92b2362.txt`).
- Después se corrigieron N1–N10 de la segunda pasada. Regresión completa de esa candidata, `f3d15e8` (manifiesto 7207/7207, sin archivos de
  más): **RESULTADO GLOBAL: PASA**, código 0 (`resultados/verificacion_completa_f3d15e8.txt`). Reconstrucción de C48 con ese código
  (`resultados/reconstruccion_c48_f3d15e8/`): 8 casos iguales; C48 = 108 con y sin valores migrados.
- Baterías dirigidas sobre el árbol actual (sin LibreOffice): entradas 4.15 **173/173**, entrada efectiva **60/60**, entradas 4.14 33/33.
  Mínimos de `verificar_paquete.sh`: 173, 60 y 5 (relevo).
- Registros reales con el código actual: diagnóstico idéntico byte a byte al registrado; inventario de signo igual; las 469 entradas
  reales de Elis y Viscofan citadas contra su PDF: 0 rechazos falsos (sonda q12 de la tercera pasada del hito 1).
- Control de la entrega 4.14: 29/35 (3 esperadas desde el hito 1; 3 por fechas de archivo que Git no conserva). No se da por superado.

## Revisiones independientes (Fable, esfuerzo máximo, agente distinto del autor, con aviso)

- Primera pasada sobre `c2d2b96`: ACEPTABLE CON CORRECCIONES (H1 y H2 importantes; H3–H14 menores u observaciones),
  `revision_independiente/hito2/REVISION_FABLE_HITO2.md`. Corregidos en `d54ee13`: H1, H2, H4, H5, H6, H7 (salvo clases CSS), H8, H9 (en
  parte), H10, H14. Declarados como límites: H3, H7 (clases CSS y otros rechazos conservadores), H11 (en parte), H12.
- Segunda pasada (solo lo cambiado tras la primera) sobre `92b2362`: ACEPTABLE CON CORRECCIONES (H1 y H2 corregidos; N1–N11 menores u
  observaciones), `revision_independiente/hito2/REVISION_FABLE_HITO2_SEGUNDA.md`. Corregidos ahora: N1, N2, N3, N4, N5, N6, N9, N10, N11
  (auxiliares sin uso) y N7 en parte (pruebas de H1 en calcular_entrada, H9 con registro apto y mutaciones m12, m16, m17, m20, m22, m29 y
  H6 ±). Declarados: N8 (orden de orígenes en fórmulas anidadas; min(o, 0) dentro del límite U1), H3, H7 (clases CSS), H12 y m47.
- **Pendiente: comprobación independiente de lo cambiado tras la segunda pasada** (el revisor indicó que basta comprobar lo que se cambie).

## Incidencias y requisitos pendientes (no cerrados)

- **Comprobación independiente de las correcciones de la segunda pasada** (tercera pasada acotada, Fable, en curso sobre `f3d15e8`): pendiente.
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

1. Regenerar manifiesto y `CAMBIOS_ARCHIVOS.txt` sobre el árbol limpio (sin `.lo_perfil` ni `__pycache__`) y congelar una copia.
2. (Hecho: regresión completa de `f3d15e8`, PASA.) En curso: la comprobación independiente (Fable, esfuerzo máximo, otro agente, sin
   LibreOffice) solo de lo cambiado desde `92b2362`; su informe irá a `revision_independiente/hito2/REVISION_FABLE_HITO2_TERCERA.md`.
3. Si ambas pasan sin correcciones de código: documentación de cierre (`VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`,
   `HITO_2_4_15.md`), manifiesto final, paquete de cambios con `scripts/empaquetar_cambios_4_15.py` comprobado sobre la base 4.14, commit y
   push con el resumen para la revisión externa. Si piden cambios de código: corregir, revisar lo afectado y repetir la regresión.

Reproducción del entorno: `gh release download` no funciona aquí (GraphQL bloqueado); el ZIP se descarga con
`gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858`, y se materializa con
`python3 -I tools/base_414.py materialize --source <zip>` y `verify` (6798/6798).
