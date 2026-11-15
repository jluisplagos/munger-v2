# Registro de implementación · reparación H1–H3 de Munger v2

**Versión del paquete:** r1 · entrega 3.1 (continuidad; contiene las entregas 1 a 3) · 8-nov-2026.

> **Entrega 3.1 · continuidad.** Su punto de entrada es `CONTINUIDAD.md`, y una sesión nueva puede comprobar el estado sin depender de esta conversación. Cambios respecto a la entrega 3:
> - **Archivos nuevos:** `CONTINUIDAD.md`; `PROMPT_NUEVA_VENTANA.md` (el mensaje de arranque); `verificar_paquete.sh` (manifiesto, entorno y pruebas); `MANIFIESTO_SHA256.txt` (la huella de cada archivo); y `documentacion_reparacion/`, con el encargo inicial, el diagnóstico (informe, anexo, pruebas y resultados), el contrato y las instrucciones posteriores transcritas literalmente.
> - **Avisos de documento histórico:** `personaje_v2/ESTADO.md` lleva al principio un aviso que remite a `CONTINUIDAD.md`, y las tres copias de `documentacion_reparacion/` (informe, anexo y contrato) llevan notas de continuidad. `README_v2.md`, `PROMPT_CLAUDE_CODE.md` y `PROMPT_VENTANA_NUEVA.md` llevan un aviso de documento histórico.
> - **Prueba H3:** `comparacion_H3.json` deja de reescribirse al ejecutar las pruebas. El informe regenerado va a `pruebas/resultados_reparacion/` y una comprobación nueva verifica que coincide con el entregado (H3 pasa de 13 a 14 comprobaciones; total, 114). Además, el informe se ordena de forma determinista: antes dependía del orden de los conjuntos de Python, que cambia en cada ejecución. El `comparacion_H3.json` entregado se regeneró así; tiene los mismos elementos que en la entrega 3, en otro orden.
> - **Revisiones independientes y correcciones.** Dos agentes nuevos, sin contexto (Opus), verificaron el paquete partiendo solo del ZIP y del mensaje de arranque. En las dos, las pruebas y la integridad pasaron.
>   - **Primera revisión.** Encontró 15 puntos, todos corregidos:
>     1. el orden de la verificación, que ahora es una sola, completa, sobre una descompresión limpia;
>     2. el estado de la prueba de variabilidad, que estaba hecha el 3-nov;
>     3. «pasos 0–14»;
>     4. el contenido real de `kit_pipeline_munger/`;
>     5. los nombres de los textos de cada empresa y la excepción de Rational;
>     6. los efectos de las pruebas fuera de `pruebas/`;
>     7. qué expediente de Aarsleff es el vigente;
>     8. todo el cuerpo histórico de `ESTADO.md`, marcado como tal;
>     9. `.lo_perfil/` dentro del paquete;
>     10. el origen de cada decisión;
>     11. el pendiente S-4b;
>     12. los requisitos que faltaban en `LEEME_REPARACION_H1-H3.md`;
>     13. la anotación de las 13 o 14 comprobaciones de H3;
>     14. la nota del contrato sobre la regla de H2;
>     15. la nota de continuidad del informe del diagnóstico.
>   - **Segunda revisión.** Confirmó los 15 puntos y encontró más, también corregidos:
>     - la frase sobre los libros V5.3, porque hay además una copia y una V5.3 sintética;
>     - la nota del contrato, que ya incorpora P3;
>     - los avisos de histórico en `README_v2.md` y en los dos prompts antiguos;
>     - los efectos de las pruebas y la lista de contenido en `LEEME_REPARACION_H1-H3.md`;
>     - la mención de los resultados de la 3.1 en este registro;
>     - la coherencia de las notas de continuidad;
>     - el contenido de `diagnostico/`, que se detalla en la nota del anexo;
>     - la declaración expresa de la ampliación de la lista cerrada y del origen de I9;
>     - quién es «José Luis».
> - **`personaje_v2/.lo_perfil/`:** es un perfil de LibreOffice que se crea al ejecutar el pipeline (`config_v2.json` → `recalc.perfil`). Se había incluido por error en los ZIP de las entregas 2 y 3, con 35 archivos, y se retira; no es parte del sistema.
> - **Scripts de verificación:** `verificar_paquete.sh` y `pruebas/ejecutar_pruebas_reparacion.sh` fijan `PYTHONDONTWRITEBYTECODE=1`, para que no se cree `__pycache__` dentro del paquete. El registro del entorno va a un archivo temporal creado con `mktemp`.
> - **Código del sistema:** no cambia. `CAMBIOS_ARCHIVOS.txt` lo confirma: los archivos modificados de `personaje_v2/scripts/` son los mismos que en la entrega 3, con las mismas huellas.

**Base:** `munger_v2_paquete.zip`, SHA-256 `61c70800d0faa7c4a98888b7413820ec8041153e53484c32b0c549b26b6af87d`.

El paquete es una copia completa de la base con la reparación aplicada, así que no hace falta combinar parches. Los originales no se han tocado: los 489 archivos de `empresas_v2/` conservan el SHA-256 de la base, y dos pruebas lo comprueban.

| Parte | Estado |
|---|---|
| H2 · lector de auditorías | **Cerrada** en la entrega 2; confirmada por la revisión externa |
| H1 · comprobación de extracciones | **Cerrada**: entregas 2 y 3 (sección 2) |
| H3 · corrección de Aarsleff | **Ejecutada** (sección 3) |

**Modelos.** Opus ha sido el modelo principal. **Fable no se ha usado**, porque ninguna cuestión lo justificó: las tres incompatibilidades se resolvieron leyendo el código y con pruebas que se pueden reproducir. En H3 se usó un único agente adicional: el **agente de verificación** que el propio sistema prevé para el paso 13 (Opus, esfuerzo medio, sin contexto previo). Recibió el prompt generado por el pipeline y su resultado fue APROBADO, con los 16 puntos en PASA.

## 1. Precisiones del contrato

| # | Precisión | Estado |
|---|---|---|
| P1 | Ningún cero pendiente puede quedar «Rellenado y verificado» ni aprobarse en silencio, y hace falta una prueba del recorrido completo | Cumplida (entrega 2), ampliada a libros reutilizados y medias previas (sección 2). **Ampliación declarada de la lista cerrada del contrato:** se añadieron `scripts/rellenar_fase1_v63.py` (para marcar los ceros pendientes en el Excel) y `scripts/comprobar_entrada_v63.py`. Este último lo exigió la incompatibilidad I9, descubierta al implementar H1 en la entrega 2: el contrato llegaba hasta I8 |
| P2 | Confirmación por decisión humana registrada, sin que la IA la invente | Cumplida (entrega 2); la confirmación sobre un libro ya rellenado se cubre en la sección 2 |
| P3 | Rutas de H3: `observaciones.C25` y `seis_preguntas.que_caja_espero`; `celdas.C25` queda en «No» | Aplicada (sección 3) |
| P4 | ZIP completo, autocontenido y versionado | Aplicada: `LEEME_REPARACION_H1-H3.md`, este registro, `VERSION`, `CAMBIOS_ARCHIVOS.txt` y `personaje_v2/pruebas/ejecutar_pruebas_reparacion.sh` |

## 2. H1 · cierre (revisión externa de la entrega 2)

### 2.1 Reproducción con el código de la entrega 2
Se añadió la parte `test_comprobadores.py h1_reutilizacion`, con 16 comprobaciones iniciales. Con el código de la entrega 2 **fallaron 11** (salida en `pruebas/resultados_reparacion/entrega3_H1cierre_H3/test_reutilizacion_contra_entrega2.txt`):
- **Caso A, libro ya rellenado, con y sin `--sobrescribir`:** las filas de Historia de SBC y adquisiciones conservaban «Rellenado y verificado», y C50 también cuando no se usaba `--sobrescribir`.
- **Caso B, C50 en los metadatos:** la media no heredaba el pendiente.
- **Caso C, confirmación posterior:** las marcas de pendiente antiguas se conservaban, y una reutilización insegura no se rechazaba.

### 2.2 Corrección

**`scripts/fase1_historia.py`**
- `DEP_ANALISIS` define, para cada celda de datos de Análisis que depende de la Historia (C46–C50, C24, C26, C28 y C33), qué partidas usa y en qué ventana de años.
- `pendientes_celda` devuelve los años con cero pendiente dentro de esa ventana.
- `defecto_independiente` valida el respaldo de una fuente independiente: fuente con página, fecha, una persona y motivo.
- `construir` propaga el pendiente a **toda** celda dependiente, también a las que ya venían en los metadatos (caso B), salvo que lleven un respaldo independiente válido. Los respaldos inválidos se anotan en `historia_revision.md`, en «Fuentes independientes no aceptadas». Una sección nueva, «Celdas de Análisis que heredan el pendiente», lista las celdas afectadas.

**`scripts/rellenar_fase1_v63.py`**
- Las filas de Historia se reclasifican **siempre** con la Historia actual (casos A y C). La nota «[H1]» se sustituye por «H1 resuelto» cuando el cero queda confirmado.
- Las celdas dependientes se revisan aunque ya tengan valor:
  - **Con un cero pendiente en su ventana:** pasan a «Dato no verificable» y conservan su valor; la nota dice qué valor daría la Historia actual y que solo `--sobrescribir` lo aplica. Así ocurre también con los valores heredados de la etapa 1.
  - **Si antes estaban pendientes:** vuelven a «Rellenado y verificado» solo si su valor coincide con el de la Historia actual. El estado cambia; el valor, no.
  - **Si no se puede resolver con seguridad** (una celda pendiente, o derivada de la Historia, cuyo valor no coincide): **se rechaza con el código 5** sin escribir el libro, y hay que regenerar desde el libro base o usar `--sobrescribir`.
- La reclasificación IFRS de C48 y C49 también reconoce una celda que una pasada anterior dejó pendiente.

### 2.3 Criterios de la revisión

| Criterio | Prueba (`h1_reutilizacion`, salvo indicación) | Resultado |
|---|---|---|
| Un dato que depende de un cero pendiente no conserva la etiqueta «verificado» por estar ya relleno | Caso A sin y con `--sobrescribir`; caso A con un valor de la etapa 1 | Cumplido |
| El pendiente se propaga a las medias que ya existían | Caso B (C50 en los metadatos) y tabla de dependencias (parte `h1`, 10 casos) | Cumplido |
| Una fuente independiente no queda validada solo por declararla | Caso B: con respaldo válido no hereda el pendiente; declarada sin respaldo, firmada por un agente o sin página, sigue pendiente | Cumplido |
| Tras la confirmación solo cambian las evidencias afectadas | Caso C: SBC y C50 pasan a verificado, adquisiciones 2017 sigue pendiente y las demás celdas no cambian | Cumplido |
| Los cambios de estado no modifican valores en silencio | Caso C: ningún valor cambia; caso A: sin `--sobrescribir` el valor se conserva y la nota lo explica | Cumplido |
| Una reutilización no soportada se rechaza de forma expresa | Caso C sin soporte: código 5, sin libro de salida, con aviso de regenerar; con `--sobrescribir`, regeneración correcta | Cumplido |
| Se mantienen las 82 comprobaciones anteriores y las 30 del pipeline | Regresión final (sección 4) | Cumplido |

## 3. H3 · expediente corregido de Aarsleff

**Ubicación:** `personaje_v2/empresas_v2_correcciones/2026-11_H3/Aarsleff/`. Las salidas de agente registradas están en `…/agentes_registrados/`, la comparación en `…/comparacion_H3.json` y el resumen regenerado en `…/resumen_v2.csv`. El procedimiento completo está en `…/Aarsleff/CORRECCION_H3.md`.

**Correcciones (P3).** Se cambió «cuatro» por «cinco» en estos sitios, sin reformatear los archivos:
- `fase_a.json`: `seis_preguntas.que_caja_espero`, `herencia.C25.evidencia_y_razonamiento` y `observaciones.C25`;
- `fase_a.md`: líneas 49 y 99;
- `fase_c.json`: `celdas.B102`.

`celdas.C25` sigue siendo «No». La comparación de rutas JSON confirma que no cambia ninguna otra.

**Regeneración.** Se ejecutó `pipeline.py … --agentes-simulados agentes_registrados`. El pipeline llegó al paso 13 sin pedir otro agente (incompatibilidad I7 del contrato, confirmada) y por el camino `verificar_todo.sh` dio PASS. En el paso 13 hizo la auditoría nueva el agente de verificación (I8): 16 puntos en PASA y veredicto APROBADO. Al relanzarlo, el pipeline terminó: paso 14, `concluido`, auditoría APROBADO. Se borraron `recalc/` y `.lo_perfil/`, como en el expediente original.

**Criterios** (prueba `test_comprobadores.py h3`: 13 comprobaciones en la entrega 3 y 14 en la 3.1, por la comprobación de que el informe regenerado coincide con el entregado; pasan todas):
1. **Variantes de la frase:** las dos expresiones regulares del contrato no encuentran ninguna en los textos ni en las celdas, aparte de `CORRECCION_H3.md`, que cita la frase antigua a propósito. Las frases excluidas se conservan: el crecimiento del escenario MALO y los textos heredados de la etapa 1.
2. **Propagación:** 13 archivos; las 27 apariciones de «cuatro» pasan a 27 de «cinco», archivo por archivo.
3. **Controles:** `verificar_todo.sh` PASS, celdas PASS (64), esquema de la ficha VÁLIDO, citas PASS e integridad ÍNTEGRO. La auditoría nueva da APROBADO con la regla de H2.
4. **Excel:** se compararon las cuatro hojas de cálculo celda a celda (17.159 celdas en el libro evaluado, tanto fórmulas como valores guardados). Solo cambian `Análisis!B102` y `Control maestro!N30`, y en ambas el único cambio es la frase. La única diferencia técnica es `Control maestro!L5`, la fecha de revisión que escribe el relleno.
5. **JSON y textos:** ninguna diferencia de contenido. Las técnicas se aceptan solo con una regla explícita (rutas absolutas, SHA-256 de un libro, fecha L5) o porque el archivo está en una lista declarada y comprobada. Hay dos casos de esa lista que conviene detallar:
   - `conciliacion.json`: solo cambian rutas;
   - `fase1.registro.json`: `n_celdas` pasa de 444 a 445 porque el relleno corregido vacía también la columna J de una fila «No aplicable», que ya estaba vacía.

   Todas las diferencias técnicas quedan registradas en `comparacion_H3.json`.
6. **Contenido conservado:**
   - `fase1_v63.json`, idéntico byte a byte;
   - `precio.json`, idéntico: precio de Sí 450,57, ponderado 502,36, escenario MALO 346,99, zona caro;
   - en la ficha: fecha, cubo Vigilar, estado, precio, escalera, decisión (esperar), predicciones y motor;
   - C25 = No, tanto en la fase A como en el Excel.
7. **El original y todo `empresas_v2/` siguen idénticos a la base.**
8. **`CORRECCION_H3.md`** recoge las cinco correcciones.

**Lo que H3 no cambia.** Los 21 ceros heredados de Aarsleff siguen sin cita, igual que en el original, porque la fase 1 no se volvió a ejecutar. Ya figuran en el inventario `ceros_heredados_H1.csv`.

## 4. Pruebas y resultados (entrega 3)

Se ejecutaron el 8-nov-2026 con `bash pruebas/ejecutar_pruebas_reparacion.sh` sobre una copia del árbol final (Python 3.13.18, LibreOffice 24.2.7.2). Las salidas están en `personaje_v2/pruebas/resultados_reparacion/entrega3_H1cierre_H3/`.

| Prueba | Resultado | Código |
|---|---|---|
| `test_comprobadores.py`, todas las partes: H2 39 · H1 23 · recorrido 21 · reutilización 17 · H3 13 (entrega 3; 14 en la 3.1, véase la nota inicial) | **113/113 PASAN** (114/114 en la 3.1): se mantienen las 82 de la entrega 2 y se añaden 31 | 0 |
| `test_pipeline_sintetico.py` | **30/30 PASAN**, con los mismos 30 nombres que la línea de base v2.2 | 0 |
| `h1_reutilizacion` contra el código de la entrega 2 (reproducción) | 5/16; fallan los casos A, B y C | 1 |
| Prueba H3 ejecutada desde otra carpeta (que el paquete funcione en cualquier ubicación) | 13/13 | 0 |

En la primera regresión final falló 1 de 113 comprobaciones. La regla técnica de H3 solo reconocía las rutas absolutas de la carpeta donde se había generado el expediente, y no las de una copia en otra ubicación. Se generalizó la regla y la regresión completa se repitió con 113/113.

## 5. Cambios por archivo (entregas 1 a 3)

| Archivo | Cambio | Parte |
|---|---|---|
| `scripts/pipeline.py` | `veredicto_auditoria` estricto: 16 puntos en PASA, ningún FALLA, ningún encabezado inválido | H2 |
| `pruebas/agentes_sinteticos.py` | Auditoría sintética de 16 puntos | H2 |
| `prompts/verificacion.md`, `ANEXO_D_salidas_y_formatos.md` | Regla de lectura de la auditoría y «Aviso:» | H2 |
| `scripts/fase1_historia.py` | R-a, R-b y R-c; estado PENDIENTE; confirmación humana; propagación a la Historia y a toda celda dependiente (`DEP_ANALISIS`); respaldo independiente explícito; secciones de `historia_revision.md` | H1 |
| `scripts/rellenar_fase1_v63.py` | «Dato no verificable» [H1] en filas y celdas dependientes; reutilización segura (reclasificación, cambio de estado sin tocar valores, rechazo con código 5) | H1 |
| `scripts/comprobar_entrada_v63.py` | Lista las filas con «[H1]» que la plantilla no cuenta | H1 |
| `prompts/historia_anio.md` | `cita` obligatoria, el cero queda pendiente, prohibido escribir decisiones | H1 |
| `empresas_v2_correcciones/ceros_heredados_H1.csv` | Inventario de los 134 ceros heredados | H1 |
| `empresas_v2_correcciones/2026-11_H3/` | Expediente corregido de Aarsleff, salidas de agente registradas, comparación y resumen | H3 |
| `DECISIONES.md`, `ESTADO.md` | Entradas del 8-nov-2026 (H2, H1, cierre de H1 y H3) | Todas |
| `pruebas/test_comprobadores.py`, `ejecutar_pruebas_reparacion.sh`, `linea_base/` | Pruebas (partes `h2`, `h1`, `h1_recorrido`, `h1_reutilizacion` y `h3`), ejecutor y líneas de base | Todas |

La lista completa, con el SHA-256 de cada archivo antes y después, está en `CAMBIOS_ARCHIVOS.txt`.

## 6. Incompatibilidades y limitaciones declaradas

| # | Asunto | Tratamiento |
|---|---|---|
| I9 | El inventario de evidencias de la plantilla no cuenta varias filas de la Historia | `comprobar_entrada_v63.py` las lista para la revisión obligatoria de la fase C. Limitación de la plantilla, que no se modifica: si el cero pendiente solo afecta a esas filas, el estado del libro puede seguir siendo LISTO · PROVISIONAL |
| — | Reutilizar un libro con valores que no coinciden con la Historia actual | No está soportado: se rechaza con el código 5 y se pide regenerar. Es intencionado |
| — | Autoría humana de `fase1_decisiones.json` y de los respaldos `independiente` | El código no puede probarla. Exige los campos, rechaza los nombres de agentes o modelos, ningún script escribe esos datos y el prompt lo prohíbe: es una garantía de procedimiento, declarada |
| L1–L4 | El control no valida concepto, columna, unidad ni signo | Fuera del alcance de esta reparación (contrato) |

## 7. Pendientes
- **Fuera del alcance de la reparación:** las 3.211 cifras extraídas y los 134 ceros heredados siguen pendientes de verificación hasta que haya `texto/` o PDF; la revisión debe seguir el procedimiento del contrato. Los lotes de la etapa anterior y la base de datos siguen sin examinar.
- No queda ninguna parte del contrato H1–H3 pendiente.

## 8. Pruebas de la entrega 3.1
Se ejecutaron sobre una copia del árbol final antes de empaquetarlo. Las salidas están en `personaje_v2/pruebas/resultados_reparacion/entrega3_1_continuidad/`.
- `test_comprobadores.py`: **114/114** (H2 39, H1 23, recorrido 21, reutilización 17, H3 14).
- `test_pipeline_sintetico.py`: **30/30**, con los mismos nombres que la línea de base.
- `comparacion_H3.json` regenerado: idéntico byte a byte al entregado.

Después de empaquetar, `verificar_paquete.sh completa` sobre una descompresión limpia del ZIP dio «RESULTADO GLOBAL: PASA» (manifiesto, entorno, 114/114 y 30/30), Las dos revisiones independientes reprodujeron ese mismo resultado por su cuenta, sobre versiones anteriores del ZIP de la 3.1 con el mismo código; las correcciones que siguieron a cada revisión solo cambiaron documentación. La verificación final se repitió sobre el ZIP definitivo. Que el paquete funcione en cualquier ubicación queda demostrado así: cada una de esas verificaciones se hizo en una carpeta distinta de aquella en la que se generó.

**Archivos de salida no conservados.** La primera regresión de la entrega 3, en la que falló 1 de 113 comprobaciones, y la prueba de H3 desde otra carpeta (13/13) no tienen archivo de salida conservado.
