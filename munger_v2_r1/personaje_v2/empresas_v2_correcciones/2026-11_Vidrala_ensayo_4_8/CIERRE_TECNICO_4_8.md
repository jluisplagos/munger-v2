# Cierre técnico de la entrega 4.8 · coherencia de estados X-a y X-c

Redactado por Claude (Opus) el 10-nov-2026 para el encargo 4.8, §4. Es una declaración de Claude: lo que está ejecutado se indica con el archivo de salida que lo prueba; nada de este documento está comprobado externamente.

## 1. Qué fallaba (hechos reproducidos con el código 4.7.1)

Salida completa: `reproduccion/reproduccion_xa_xc_codigo_4_7_1.txt` (guion `scripts/reproducir_xa_xc.py`, que trabaja en temporales y no modifica ni el árbol ni el expediente de referencia).

**X-a** (reproducido también por la revisión externa de la 4.7.1). Copia del expediente aprobado de la 4.6.1 con su resumen, sin `fase1_v63.json` ni `texto/`, y una sola ejecución de `pipeline.py COPIA --desde 2`:

| Observación | Código 4.7.1 |
|---|---|
| Código de salida | 0 |
| Última línea | «estado final: None · paso 2» |
| `estado_pipeline.json` | `estado_analisis = None`, `auditoria = None`, paso 2 |
| `ficha.json` y fila del resumen | `pendiente_de_datos` |
| `diagnostico.json` | `pendiente_de_datos` (estado del diagnóstico distinto del del pipeline) |
| Aprobación caducada | retirada y archivada (esto ya estaba bien) |

**Causa.** `ficha.py` archiva la ficha cerrada anterior y deja en el disco el estado sin cierre (`None`); `Pipeline.adoptar_archivo()` copiaba ese `None` encima del estado que `terminar()` acababa de fijar.

**X-c** (declarado por el auditor interno de la 4.7.1; no reproducido externamente). Código con `esquema/ficha.esquema.json` roto a propósito (un campo obligatorio inexistente), copia del mismo expediente y una sola ejecución de `--desde 14`:

| Observación | Código 4.7.1 |
|---|---|
| Código de salida | **4**, «CIERRE RECHAZADO» |
| Motivo del rechazo | el de `informe.py` («auditoria = None»), que no es la causa |
| `estado_pipeline.json` | `no_entregable`, paso **13** |
| `ficha.json` | ninguna; en el archivo, una ficha **`no_entregable` con `cierre`** |
| Fila del resumen | «SIN APROBACIÓN VIGENTE» |

**Causa.** `ficha.py` escribía `cierre` siempre que el pipeline estuviera en el paso 14, también en `no_entregable`. `informe.py` encontraba esa ficha «cerrada» sin aprobación registrada, la archivaba, y el pipeline lo interpretaba como un rechazo del cierre.

## 2. Qué cambia (código)

| Archivo | Cambio |
|---|---|
| `personaje_v2/scripts/pipeline.py` | `salidas_finales(cierre=…)`: `False` desde `terminar()` (terminaciones que no pasan por la auditoría), `True` en el paso 14. `adoptar_archivo(conservar_estado=…)`: en una terminación que no cierra adopta la auditoría retirada, los cierres archivados y el historial, pero **conserva el estado y el paso** de la memoria (X-a). En el paso 14, el archivo sigue mandando (W-e de la 4.7.1, sin cambios). Fallo de esquema de la ficha: el «estado previsto» del diagnóstico es el que se pidió escribir; con `cierre=True` el análisis queda en `no_entregable`, paso 14, el diagnóstico dice «continuar desde el paso 13» con auditoría nueva y el pipeline termina con **código 0** y «FIN · estado no_entregable · fallo_de_implementacion…», no con «CIERRE RECHAZADO» (X-c). La aprobación se retira **después** del archivo, para que `cierres_archivados` conserve «APROBADO» como auditoría registrada del cierre archivado. La última línea, en todo estado distinto de `concluido`, añade la causa y el paso desde el que se continúa (de `diagnostico.json`). Documentación de los códigos. |
| `personaje_v2/scripts/ficha.py` | `cierre` solo si el estado no es `no_entregable` (X-c) y, cuando hay material auditado, solo si el estado es el que propuso `ficha_provisional.json`; `--estado concluido` con otro estado propuesto termina con código 3 (Z-f de la auditoría interna). |
| `personaje_v2/pruebas/test_estados_v2.py` | Batería nueva de 28 pruebas (§3). |
| `verificar_paquete.sh` | La batería nueva es obligatoria en `completa` (al menos 28 pruebas, todas en PASA). Su bloque va **antes** del del resumen, para que los controles de integración de la 4.6.1, la 4.7 y la 4.7.1, que extraen sus bloques por posición, sigan extrayendo los mismos (Z-e). |
| `personaje_v2/ANEXO_D_salidas_y_formatos.md` | Comportamiento de X-a y X-c y precisiones de X-d (§5). |

**Correcciones posteriores a la auditoría interna** (`AUDITORIA_INTERNA_4_8.md`), todas en `pipeline.py` salvo la de `ficha.py` (arriba):
- **Z-a.** Si `resumen.py` no puede publicar la fila del estado final (retirada pendiente, código 5), queda `resumen_pendiente = true`. La ejecución siguiente, sin `--desde` y con las retiradas ya completas, vuelve a publicarla. Con el código 4.7.1 esa vía funcionaba solo por accidente: el estado quedaba en `None` y se rehacía el paso 2.
- **Z-f.** `salidas_finales` no conserva un estado final si, en esa misma llamada, un generador archivó la ficha y no queda `ficha.json`. Si `ficha.py` simplemente no llegó a escribirla, el estado se conserva (V-b del control de vigencia).
- **V-a (bloqueante del control de vigencia).** La última línea nueva fallaba con `IndexError` (código 1) cuando la ejecución terminaba sin estado final (por ejemplo, con `--hasta`). Ahora solo añade la causa si hay un diagnóstico del mismo estado final, y lee su primera línea de forma segura. `test_comprobadores.py` vuelve a registrar «pipeline --hasta 2 código 0».
- **Z-g.** El FIN del historial toma la causa del diagnóstico cuando la ficha no cumplió su esquema. Si el estado ya era `no_entregable`, se anota también el fallo de esquema.
- **Z-h.** Al reanudar con `--desde` desde un estado final distinto de `concluido`, su diagnóstico pasa a `.anterior`.

**Lo que no cambia.**
- La regla H2 (`Pipeline.veredicto_auditoria`): su código fuente es idéntico al de la 4.7.1 (prueba F de la batería).
- La retirada de la aprobación caducada, el archivo en `historial_cierres/`, el registro de destinos del resumen y el código 4 de la sustitución de una ficha dentro del paso 14 (W-e).
- `cierre_v2.py`, `informe.py`, `resumen.py`.
- Ningún criterio financiero, expediente histórico ni original.

**Decisión de diseño declarada (código de salida de X-c).** Se usa el código 0 porque `no_entregable` es un estado final con sus salidas y así terminan todas las demás vías de `fallo_de_implementacion` (p. ej., la auditoría en REPETIR tras agotar las correcciones; `test_pipeline_sintetico.py`, pruebas 13). La causa queda en el estado, el diagnóstico y la última línea. Si la persona responsable prefiere un código distinto para «fallo de implementación al cerrar», es un cambio acotado (pregunta Q-T1 de `financiero/decisiones_y_preguntas_4_8.json`).

## 3. Pruebas (primera salida, estados y archivos; no solo códigos)

`personaje_v2/pruebas/test_estados_v2.py` tiene 28 pruebas, tarda unos 9 s y no usa LibreOffice. Trabaja sobre copias del expediente aprobado de la 4.6.1:

| Grupo | Pruebas | Qué observa |
|---|---|---|
| A · falta de datos tras un cierre previo (X-a) | 10 | código y última línea; `estado_pipeline.json`; ficha sin cierre; informe; diagnóstico; resumen e historial del resumen; archivo; segunda ejecución sin cambios; retirada pendiente (código 5) y relanzamiento con el destino recuperado (Z-a); `terminar()` directo |
| B · fallo de esquema al cerrar (X-c) | 8 | código 0 sin «CIERRE RECHAZADO»; estado y paso; ninguna ficha `no_entregable` con `cierre`; diagnóstico con la causa y «desde el 13»; resumen; historial conservado; subsanación (`--desde 13` pide auditoría nueva, no reutiliza la archivada y deja el diagnóstico anterior como `.anterior`, Z-h); `ficha.py` directo |
| C · estados tempranos legítimos | 5 | expediente sin etapa 1 ni cierre previo; fallo de migración tras un cierre previo (`no_entregable` en el paso 1); parada sin estado final con `--hasta` (V-a); `ficha.py` sin poder escribir la ficha por un `alcance_v2.json` ilegible (V-b) |
| D · cierre válido sin cambios | 2 | relanzamiento sin `--desde` (salidas idénticas); `--desde 14` (concluido · APROBADO, sin archivos nuevos) |
| E · rechazo de material modificado | 2 | código 4, salidas archivadas, fila «SIN APROBACIÓN VIGENTE» (4.6.1, sin cambios) |
| F · regla H2 | 1 | `veredicto_auditoria` idéntica a la de la 4.7.1 |

**Resultados [Claude].**

| Ejecución | Resultado | Salida |
|---|---|---|
| Batería nueva, código 4.8 | 28/28 | `resultados/test_estados_v2_salida.txt` |
| Batería nueva, código 4.7.1 | 17/28: fallan las 11 de X-a (incluida la vía del código 5) y de X-c (incluido el diagnóstico de la subsanación) | `reproduccion/test_estados_con_codigo_4_7_1.txt` |
| Mutaciones (cada corrección revertida por separado) | ver tabla siguiente | `reproduccion/mutaciones_test_estados.txt` |
| Reproducción con el código 4.8 | X-a y X-c coherentes en la primera ejecución | `reproduccion/reproduccion_xa_xc_codigo_4_8.txt` |
| `test_cierre_v2.py` (55), `test_resumen_v2.py` (45), `test_comprobadores.py` (114) y `test_pipeline_sintetico.py` (30), con el código final | ver `resultados/` y `LEEME_BATERIAS_HISTORICAS.md` | `resultados/` |

| Mutación | Corrección revertida | Resultado |
|---|---|---|
| M1 | `adoptar_archivo` | 24/28 |
| M3 | FIN del paso 14 | 26/28 |
| M4 | última línea | 26/28 |
| M5 | «estado previsto» | 27/28 |
| M6 | republicación del resumen (Z-a) | 27/28 |
| M7 | última línea sin estado (V-a) | 27/28 |
| M8 | defensa de Z-f sin condición (V-b) | 27/28 |
| M9 | diagnóstico a `.anterior` (Z-h) | 27/28 |
| M2b | las dos defensas de `ficha.py` | 22/28 |

**Mutantes equivalentes (Z-j).** No las detecta ninguna prueba porque el código tiene defensas redundantes:
- **M2**, quitar solo la exclusión de `no_entregable` en `ficha.py`, da 28/28: la condición de Z-f, que exige el estado propuesto, también la excluye.
- Las cuatro de la auditoría (`auditoria = None` tras el fallo de esquema, paso 14 forzado, segunda adopción sin conservar, `conservar = True`) tampoco se detectan: `archivar_salidas` ya retira la aprobación y no toca un `no_entregable`.

Ninguna expectativa anterior se ha cambiado.

## 4. Límites que siguen

- **X-b** (relanzar el paso 14 tras un cambio solo de metadatos exige una auditoría nueva) y **W-d** (`ficha.py` directo sustituye una ficha cerrada con código 0 y un aviso) quedan como estaban.
- Si el estado ya era `no_entregable` y además la ficha no cumple su esquema, el fallo solo consta en el historial y en `ficha_valida = false`, no en el diagnóstico (Z-g). Es anterior a la 4.8. Son decisiones de la persona responsable: Q-T2 y Q-T3.
- Los límites declarados del resumen (CSV compartido, copia del expediente solo en otro árbol, registro y respaldo borrados, punto de montaje vacío, traslado del expediente solo, filas sin registrar cuya fecha cambió o no se lee, expedientes cerrados antes de la 4.6.1) siguen en el Anexo D. No se ha rediseñado el almacenamiento ni se han revisado otros expedientes.
- La batería usa el expediente de Vidrala de la 4.6.1 y un expediente vacío. No prueba fallos de esquema en otros estados finales distintos de los cubiertos, aunque el código los trata igual (rama `cierre=False`).

## 5. Precisiones documentales hechas en el Anexo D

- **X-a y X-c.** Comportamiento nuevo, códigos y vía de subsanación.
- **X-d:**
  - qué formatos de fecha se leen y cuáles no («3-Nov-26», «03-nov-2026», «2026.11.03»);
  - la excepción de V-2 con una fecha ambigua día/mes;
  - la fila vigente redondeada solo se vuelve a publicar en el CSV en que escribe `resumen.py`.
- **X-e y X-f** son de documentos históricos de la 4.7.1, que no se modifican. Se corrigen en `INFORME_PM1.md` §2 y en `REGISTRO_ENTREGA_4.8.md` §6.
