# Prueba de traspaso de la 4.14 (encargo de cierre §10)

**Qué es.** La evidencia de la prueba con un agente receptor sin historial. El agente recibió solo el ZIP candidato (SHA-256 `f9f888e3…4f5a24`) y el mensaje de arranque, más una segunda tarea: elegir un relevo real pendiente del paquete, resolverlo con el procedimiento del paquete y reanudar el pipeline. El mensaje literal está en `PROMPT_DEL_AGENTE_RECEPTOR.md`.

**Resultado** (hechos; detalle en `INFORME_TRASPASO.md`):
- **Arranque.** El SHA-256 del ZIP coincide. `bash verificar_paquete.sh completa` da PASA con código 0 (20:24–21:00, `_logs/verificacion_completa.txt`). El control de la 4.14 da 35/35.
- **Controles históricos.** Mismos resultados que `resultados/LEEME_CONTROLES_HISTORICOS_4_14.md`. Ese LEEME no iba en la candidata; va en la final.
- **Relevo.** `elis_motor_A/Elis`, paso 13 (auditoría), se resolvió en una copia hermana, `elis_motor_A_relevo_traspaso/`, para no tocar el expediente anterior.
  - La solicitud pendiente estaba caducada (INCIDENCIAS I19).
  - Con `--desde 12` se emitió la solicitud SA-21babb1dd24901d1. El agente receptor la respondió con APROBADO, y el pipeline se reanudó hasta el paso 14 (`pendiente_de_datos`).
  - Los registros están en `relevo/`. Las salidas que escribió el relevo están en `salidas_copia_relevo/`: auditoría, estado, ficha, informe, material, solicitud y verificaciones.
- **Dificultades de la documentación.** Se recogen en INCIDENCIAS I18–I20 y se corrigen en la final; las que tocan código se declaran con propuesta.

**Límites.**
- **La auditoría del relevo no es independiente.** La hizo el mismo agente receptor, que no podía lanzar un agente nuevo. Prueba que el procedimiento se puede seguir con la documentación del paquete, no la calidad de una auditoría de contexto separado.
- **El expediente del relevo no tiene valor económico.** Está sustituido por `elis_decisiones` y su precio de Sí no es utilizable (F1).
- **La copia completa del relevo no se incluye.** Sus demás archivos son los de `elis_motor_A/Elis` y se reproducen copiándolo y ejecutando los comandos de `relevo/`.
