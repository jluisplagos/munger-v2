# Revisión independiente · estado

| Pasada | Material revisado | Resultado | Documentos |
|---|---|---|---|
| 1 | Commit C1, 96a69ca | 17 objeciones (3 materiales, 10 menores, 4 de forma). Ninguna invierte una conclusión material | [REVISION_INDEPENDIENTE_1.md](REVISION_INDEPENDIENTE_1.md), `scripts_revisor/` y `resultados_revisor/`: copia sin cambios, en las mismas rutas, del commit 47551a2 de la rama del revisor ([PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md)) |
| Contraste externo | Commit C2, 6fb9294 | Confirma O1 y O2 en los PDF; reproduce O3 con los mutantes del revisor | `docs/validacion_economica_paralela/revision_chatgpt_1/` de la rama `auditoria/economica-f1` (commit 5ce263a) |
| Respuesta del autor | C3 (eb77dea) y C4 | 16 objeciones aceptadas y corregidas; O3, aceptada y corregida con un matiz (cotas de redondeo por identidad en lugar de ±0,15). Ninguna rechazada | [RESPUESTAS_AUTOR_1.md](RESPUESTAS_AUTOR_1.md) |
| 2 | Commit C3, eb77dea | **Interrumpida sin resultado.** Se encargó a la sesión de revisión el 15-nov-2026 a las 19:22 UTC. La sesión del autor la interrumpió a las 19:25 UTC, cuando el revisor aún leía las diferencias, porque C3 iba a cambiar justo en O3. No produjo informe ni commit y **no cuenta como revisión** | — |
| 3 | Lo afectado por C3 y C4, sobre el commit congelado 1864c4e. Encargada el 15-nov-2026 a las 20:03 UTC; es la segunda revisión efectiva | **Hecha**, commit 11b999a (20:48 UTC). Resuelve O1, O2 y O4–O17; O3, parcialmente. Objeciones nuevas: N1 (material), N2–N5 (menores), N6–N8 (forma) | [REVISION_INDEPENDIENTE_3.md](REVISION_INDEPENDIENTE_3.md), `scripts_revisor_3/` y `resultados_revisor_3/`: copia sin cambios del commit 034301c ([PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md)) |
| 3, adenda | Sondas externas de un solo campo sobre eb77dea (`revision_chatgpt_1/seguimiento_eb77dea/`, commit e57239c de `auditoria/economica-f1`) y el commit C6 (f30c66c) | **Hecha**, commit 034301c (21:05 UTC). Las sondas se reproducen y las cifras del autor son exactas. Objeciones nuevas: N9 y N10 (menores) y contraejemplos de las heurísticas | §11 del mismo informe |
| Respuesta a la revisión n.º 3 | C7 | Las diez objeciones se aceptan y se corrigen | [RESPUESTAS_AUTOR_1.md](RESPUESTAS_AUTOR_1.md), segunda parte |
| 4 | Lo afectado por C7, sobre el commit congelado 97441770 (C8). Encargada el 15-nov-2026 hacia las 21:49 UTC | **Publicada** a las 22:04 UTC (a15f706, según los metadatos de la sesión de revisión). Pendiente de copiar, incorporar y responder | Se copiará sin cambios desde la rama del revisor |
| Cambios del autor tras el congelado | C9 | Segunda presentación de cinco entradas del ancla de S2C; hueco del verificador hallado por el autor (columna de un país con OK, también en C7 y C8) y corregido. **No revisados** | [RESPUESTAS_AUTOR_1.md](RESPUESTAS_AUTOR_1.md), tercera parte |
| 5 | Lo afectado por C9 y por la respuesta a la pasada 4, sobre un commit congelado | **Pendiente** | — |

**C4 = d2e585e91638c363682a000bdb416a4b865c6cce.** El commit 1864c4e solo cambia, respecto a C4, este archivo, la línea de C4 en RESPUESTAS_AUTOR_1.md y el manifiesto. Es el commit congelado sobre el que se encarga la pasada 3; su hash se da en el encargo y constará en el registro al incorporar el informe del revisor.

**C6 = f30c66c8651dba134b4e66fff9a08c2b50359b6c.** **C7 = 9869def325b8820e2ee25618107495a7a7b70229.** El commit siguiente solo cambia, respecto a C7, este archivo, la línea de C7 en RESPUESTAS_AUTOR_1.md y el manifiesto. Es el commit congelado sobre el que se encarga la pasada 4; su hash se da en el encargo y constará en el registro al incorporar el informe del revisor.

Las correcciones de C7 **no están revisadas** de forma independiente hasta que se incorpore la pasada 4. Los cambios de C9 tampoco: entran en la pasada 5. La configuración de cada pasada se registra en ../REGISTRO_CONFIGURACION.md.
