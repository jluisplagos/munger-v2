# Revisión independiente · estado

| Pasada | Material revisado | Resultado | Documentos |
|---|---|---|---|
| 1 | Commit C1, 96a69ca | 17 objeciones (3 materiales, 10 menores, 4 de forma). Ninguna invierte una conclusión material | [REVISION_INDEPENDIENTE_1.md](REVISION_INDEPENDIENTE_1.md), `scripts_revisor/` y `resultados_revisor/`: copia sin cambios, en las mismas rutas, del commit 47551a2 de la rama del revisor ([PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md)) |
| Contraste externo | Commit C2, 6fb9294 | Confirma O1 y O2 en los PDF; reproduce O3 con los mutantes del revisor | `docs/validacion_economica_paralela/revision_chatgpt_1/` de la rama `auditoria/economica-f1` (commit 5ce263a) |
| Respuesta del autor | C3 (eb77dea) y C4 | 16 objeciones aceptadas y corregidas; O3, aceptada y corregida con un matiz (cotas de redondeo por identidad en lugar de ±0,15). Ninguna rechazada | [RESPUESTAS_AUTOR_1.md](RESPUESTAS_AUTOR_1.md) |
| 2 | Commit C3, eb77dea | **Interrumpida sin resultado.** Se encargó a la sesión de revisión el 15-nov-2026 a las 19:22 UTC. La sesión del autor la interrumpió a las 19:25 UTC, cuando el revisor aún leía las diferencias, porque C3 iba a cambiar justo en O3. No produjo informe ni commit y **no cuenta como revisión** | — |
| 3 | Lo afectado por C3 y C4, sobre el commit congelado 1864c4e. Encargada el 15-nov-2026 a las 20:03 UTC; es la segunda revisión efectiva | **En curso** | Se copiará sin cambios desde la rama del revisor, con su procedencia |
| 3, adenda | Sondas externas de un solo campo sobre eb77dea (`revision_chatgpt_1/seguimiento_eb77dea/`, commit e57239c de `auditoria/economica-f1`) y el commit C6, que solo añade la columna de la matriz por segmentos para el perímetro, tres casos de test y `sondas_metadatos.py` con sus resultados | **Pendiente**: se añade a la pasada 3 sin reiniciarla | Ídem |

**C4 = d2e585e91638c363682a000bdb416a4b865c6cce.** El commit 1864c4e solo cambia, respecto a C4, este archivo, la línea de C4 en RESPUESTAS_AUTOR_1.md y el manifiesto. Es el commit congelado sobre el que se encarga la pasada 3; su hash se da en el encargo y constará en el registro al incorporar el informe del revisor.

Mientras la pasada 3 no conste, las correcciones posteriores a 96a69ca **no están revisadas** de forma independiente. La configuración de cada pasada se registra en ../REGISTRO_CONFIGURACION.md.
