# Registro de la entrega 4.8.1 · auditorías nuevas (R-T1) y coherencia de la reinversión (R-F1, R-F2)

**Autoría y revisión.** Lo redactó Claude (Opus, esfuerzo alto) el 10-nov-2026. El encargo vigente es «Munger V2 — Encargo 4.8.1: auditorías nuevas y coherencia de la reinversión». ChatGPT revisará la entrega después.

**Procedencia de cada afirmación:**
- **[Claude]**: ejecutado o declarado por Claude en esta sesión;
- **[auditor]**: auditoría interna de Claude con contexto separado;
- **[vigencia]**: control de vigencia de las correcciones finales, también con contexto separado;
- **[revisión externa]**: lo que dice el encargo que obtuvo la revisión de la 4.8; no se ha vuelto a comprobar, salvo donde se indica;
- **[pendiente]**: sin hacer o sin comprobar.

Nada de esta entrega está comprobado externamente.

## 1. Partida

**Paquete:** `munger_v2_r1_entrega4.8_mantenimiento_y_estados.zip`, SHA-256 `6fc60aed…2fbca7c3f`. Es el ZIP que Claude entregó en la 4.8, en esta misma sesión.

**Verificación de partida [Claude].** Es la verificación final de la 4.8, hecha sobre ese mismo ZIP en una descompresión limpia, en la misma sesión:
- `verificar_paquete.sh completa` da PASA: manifiesto de 1.494 archivos, estados 28/28, resumen 45/45 y cierre 55/55;
- controles históricos con salida idéntica a la de referencia; el de la 4.8 da 36 de 36;
- P1 intacto.

La copia de trabajo de la 4.8.1 se descomprimió de ese ZIP, con su huella comprobada.

**Hallazgos externos reproducidos [Claude]:**
- **R-T1:** `reproducir_rt1.py`, con el código de la 4.8, da:
  - en CET: código 10;
  - en UTC: código 0, concluido/APROBADO;
  - con fechas renovadas: código 0, concluido/APROBADO.

  Salida en `reproduccion/rt1_con_codigo_4_8.txt`.
- **Batería de estados con las fechas renovadas:** 27/28, con `unzip -DD` del ZIP de la 4.8. Falla la subsanación de X-c, porque reutilizaba la auditoría (`reproduccion/test_estados_4_8_fechas_renovadas.txt`). Es el resultado de la revisión externa.
- **R-F2:** las cuatro referencias externas se reproducen a 7 decimales (`INFORME_REINVERSION_4_8_1.md` §2).

## 2. Trabajo hecho

| Parte | Qué | Dónde |
|---|---|---|
| R-T1 · código | Solicitudes de auditoría identificables y persistentes, ligadas al material, conservadas en los relanzamientos. El paso 13 acepta `auditoria.md` solo si nombra la solicitud pendiente y, si aprueba, no es ninguna auditoría conocida del expediente, ni por su huella ni por su contenido sin formato; el registro persiste en `auditorias_conocidas.json`. Pedir una auditoría nueva retira el cierre vigente. Con una solicitud pendiente no cierran ni el paso 14, ni `ficha.py`, ni la vigencia. En los cierres de la 4.8.1, `auditoria.md` tiene que ser la respuesta registrada; en los anteriores, la de `cierre_vigente.json`. Las fechas no intervienen en el paso 13. H2 y la vinculación al material, sin cambios | `personaje_v2/scripts/pipeline.py` (`solicitud_auditoria_vigente`, `agente_auditoria`, paso 14) · `personaje_v2/scripts/cierre_v2.py` (§1b; comprobación de `auditoria_respuesta` en `motivo_rechazo_cierre`) · `personaje_v2/prompts/verificacion.md` · Anexo D (§ cierre y D.9) |
| R-T1 · pruebas | Batería nueva de 55 pruebas, obligatoria en `verificar_paquete.sh completa`, con mínimo 55 y su bloque antes del de estados. Fija ella misma los tres modos de fechas. Con el código de la 4.8, `reproduccion/test_auditorias_con_codigo_4_8.txt` (varios grupos se interrumpen al no encontrar ninguna solicitud) | `personaje_v2/pruebas/test_auditorias_v2.py` · `resultados/test_auditorias_v2_salida.txt` · `reproduccion/test_auditorias_con_codigo_4_8.txt` |
| R-T1 · mutaciones | 25 mutaciones del código de la reparación: la batería detecta las 25 | `scripts/mutar_rt1.py` · `reproduccion/mutaciones_rt1.txt` |
| R-T1 · integración | Control de integración del bloque nuevo: 13 de 13. Los de la 4.6.1, 4.7.1 y 4.8 siguen en 13 de 13; el de la 4.7, en 12 de 13, como en la 4.8 | `scripts/comprobar_integracion_verificador_481.py` |
| Simulador y prueba del resumen | El auditor sintético (`agentes_sinteticos.auditoria`) y el auditor simulado de la prueba 8 de `test_resumen_v2.py` escriben la línea de la solicitud vigente, como un auditor real. **No cambia ninguna expectativa** de las baterías anteriores: 114, 30, 28, 45 y 55 siguen igual | `personaje_v2/pruebas/agentes_sinteticos.py` · `personaje_v2/pruebas/test_resumen_v2.py` |
| R-F2 | Contraste 2 × 2 entre crédito y convención terminal, sin P0; efectos, interacción y reparto de Shapley; por escenario y con años y terminal por separado | `scripts/analisis_reinversion_4_8_1.py` · `financiero/rf2_credito_y_convencion.csv` · `INFORME_REINVERSION_4_8_1.md` §2 |
| R-F1 | Conciliación anual y terminal de reposición, crecimiento, circulante, crédito, inversión total y FCF. Cinco estructuras (H, S, SR1, SR2 y SRF) por siete requisitos (λ y θ), sin elegir ninguna, con el efecto de la convención de la amortización en cada celda y el Δ frente a P0; P1s revisado; afirmaciones de la 4.8 retiradas | `financiero/rf_conciliacion_anual_y_terminal.csv` (1.386 filas) · `rf1_alternativas.csv` · `rf_resultados.json` · `INFORME_REINVERSION_4_8_1.md` §3–§5 |
| Decisiones | D-N3b revisada, sin estructura por defecto; D-N3e, Q-T4 y Q-T5 nuevas; campos humanos vacíos | `financiero/decisiones_y_preguntas_4_8_1.json` |
| Control | `comprobar_entrega_4_8_1.py` | `scripts/`, `resultados/` |
| Documentación | VERSION, CONTINUIDAD, PROMPT, DECISIONES.md, Anexo D, cabeceras del código y LEEME de las baterías históricas | — |

## 3. Respuesta a R-T1

**El defecto [Claude, reproducido].** `Pipeline.agente` comparaba la fecha de `auditoria.md` con la anotada en `consumidos`.
- El campo de fecha DOS del ZIP guarda la hora local sin zona y con 2 s de resolución.
- Con `zipfile` de Python o con Info-ZIP `-X` (solo ese campo), leído en CET queda 0,21 s *antes* del consumo: se pide una auditoría nueva. Leído en UTC queda +3.599,8 s *después*. Con las fechas renovadas, también después. En los dos últimos casos se reutiliza la auditoría y se cierra.
- **Precisión (auditoría interna, Y-k):** el resultado depende de la herramienta.
  - Info-ZIP por defecto escribe además el campo UT, en tiempo universal: con él, CET y UTC dan la misma fecha.
  - Sin el campo UT, Info-ZIP redondea hacia arriba los segundos impares (+0,79 s): el código 4.8 habría aceptado la auditoría también en CET.
  - El código 4.8.1 no usa fechas, así que esto solo afecta a la explicación del defecto.

**La reparación**, en la parte que decidió Claude:
1. **Solicitud.** Al llegar al paso 13 sin una solicitud pendiente del material fijado, se registra una solicitud.
   - Su identificador es «SA-» y 16 cifras hexadecimales, que salen del SHA-256 de material, hora y 16 bytes aleatorios.
   - Se guarda en `estado_pipeline.json → solicitudes_auditoria`, que conserva todas, y en `solicitud_auditoria.json`; el prompt (`{SOLICITUD_AUDITORIA}`) y `ESPERANDO.md` la nombran.
   - Si el material cambia, la solicitud pendiente queda «sustituida».
2. **Respuesta.** `agente_auditoria` acepta `auditoria.md` solo si se cumplen dos condiciones:
   - una sola línea «Solicitud de auditoría: <id pendiente>»;
   - si aprueba según H2, no es ninguna auditoría **conocida**, ni por su huella SHA-256 ni por su contenido sin formato.

   **Cómo se quita el formato.** Se compara el multiconjunto de palabras del texto, sin la línea de solicitud: secuencias de letras y cifras, tras NFKC, sin tildes y con casefold. No cuentan el formato, el orden ni los cortes de línea; sí cuántas veces aparece cada palabra.

   **Son conocidas**, y se anotan al registrar cada solicitud en `estado_pipeline.json` y en `auditorias_conocidas.json`:
   - todo archivo de texto del expediente con forma de auditoría, con cualquier nombre y en cualquier subcarpeta;
   - la huella de `cierre_vigente.json`;
   - las respuestas ya aceptadas.

   Una REPETIR puede repetir contenido, porque no cierra nada.

   Si no se cumplen, no consume el archivo: sigue esperando (código 10), con el motivo en `ESPERANDO.md`, en la última línea y en `ultima_auditoria_no_aceptada`.
3. **Consumo.** Una respuesta aceptada deja la solicitud «respondida», con su huella, la huella de su contenido y su veredicto, y escribe `auditoria_respuesta`. Toda petición posterior es una solicitud nueva: una corrección por material distinto o una auditoría tras REPETIR.
4. **Cierre:**
   - **Al registrar una solicitud** con un cierre vigente, el cierre se archiva en la misma ejecución, con su retirada, y la aprobación se retira (Q-T5).
   - **Con una solicitud pendiente** no se cierra: lo impiden el paso 14, `ficha.py` y la vigencia (`motivo_rechazo_cierre`).
   - **En un cierre de la 4.8.1,** `auditoria.md` tiene que ser la respuesta registrada, por su contenido sin formato, y otra cualquiera lo deja sin vigencia.
   - **En un cierre anterior a la 4.8.1,** `auditoria.md` tiene que ser la que registra `cierre_vigente.json`, byte a byte.
5. **Lo que no cambia.**
   - `veredicto_auditoria`: su huella del código es la de la 4.7.1 y la 4.8.
   - La vinculación al material.
   - Los cierres anteriores a la 4.8.1, sin solicitud: se comprueban como antes y no reciben ninguna solicitud retroactiva. Solo se anota la huella de su auditoría ya consumida, para que no responda a una solicitud nueva.

**Aceptación [Claude]: `test_auditorias_v2.py`, 55/55.** Cubre los casos de aceptación del encargo y los que encontró la auditoría interna:

| Grupo | Qué prueba |
|---|---|
| A | Modos CET, UTC y renovadas: `--desde 13` directo pide una auditoría nueva |
| B | Los mismos tres modos, con el intento intermedio desde 14 |
| C | Relanzamientos repetidos: sin `--desde`, con `--desde 13`, con el informe antiguo con fecha reciente y futura, y con `--desde 14` pendiente, que se rechaza |
| D | Respuestas inválidas: informe antiguo reescrito o con la línea añadida y cambios de formato (espacios, puntuación, NFD, separadores, comillas, orden y corte de las líneas, sin tildes), auditoría histórica con otro nombre, solicitud ausente, equivocada o duplicada, material distinto e incumplimiento de H2 |
| E | Respuesta válida y cierre correcto en los tres modos; sustitución posterior por el informe antiguo, que se rechaza |
| H | Penúltima respuesta reutilizada; registro persistente sin el estado de las solicitudes ni las auditorías en disco; `ficha.py` con una solicitud pendiente; `--desde 13` sobre un cierre vigente; cambio de material con la solicitud pendiente; respuesta guardada con CRLF; REPETIR repetida; cierre anterior a la 4.8.1 con la auditoría sustituida |
| I | Auditorías históricas con mayúscula, con otra extensión, en una subcarpeta, en cp1252, en UTF-16 o con relleno de más de 2 MB; respuesta que no es UTF-8 válido; registro ilegible o con tipos inválidos (código 6) |
| F | Cierre histórico sin solicitudes |
| G | H2 idéntica |

**Observa en la primera ejecución:**
- código y última línea;
- estado, solicitud, prompt y `ESPERANDO.md`;
- ficha, informe y diagnóstico;
- fila e historial del resumen.

**Fuera de esta reparación,** como dice el encargo: Q-T1 a Q-T3 y el rediseño general del almacenamiento. Las salidas de los pasos 5–10 siguen con el criterio de fechas (Q-T4, preparada).

**Límite declarado.** El pipeline no puede probar que el auditor haya hecho de nuevo las dieciséis comprobaciones.
- **Lo que descarta:** la reutilización literal, o con otro formato, de cualquier auditoría conocida del expediente. Por formato se entienden las tildes, el orden y los cortes de línea, la puntuación y la forma Unicode.
- **Qué archivos se leen:** UTF-8, UTF-16 con BOM o cp1252, no binarios y de hasta 50 MB.
- **Lo que no detecta:**
  - una auditoría antigua a la que se cambian o añaden palabras;
  - una auditoría traída de fuera del expediente;
  - una corrección por material distinto que solo cambia la línea de material.
- **El revés:** una auditoría rehecha de verdad con un texto idéntico al de otra ya usada no se acepta (V-10).

Es una garantía de procedimiento, como la autoría humana de `fase1_decisiones.json`.

## 4. Fuentes públicas

En la 4.8.1 no se ha usado ninguna fuente nueva. R-F1 y R-F2 trabajan con los datos ya conservados y reproducidos en la 4.8: la réplica de la 4.8 sale idéntica byte a byte.

**Los PDF de la CNMV de la 4.8 (O1–O11) siguen sin conservarse.** El motivo, con precisión [Claude, 10-nov-2026, 19:27 CET]:
- desde el contenedor, `curl` a `www.cnmv.es` sigue recibiendo «CONNECT tunnel failed, response 403» del proxy;
- la lectura con el navegador del equipo de la persona responsable solo devuelve texto;
- traer los PDF exigiría pasar su contenido binario por la conversación o descargarlos en el equipo de la persona responsable, lo que requiere su permiso expreso y una carpeta conectada.

Las URL, las fechas y las huellas SHA-256 calculadas en la lectura están en `…_4_8/fuentes/fuentes_externas_pm1.json`: cualquier copia que se descargue después se puede comprobar con ellas. **Propuesta:** que la persona responsable las descargue, si quiere conservarlas.

## 5. Uso de Fable

**No se ha usado Fable en la 4.8.1.**
- **Motivo:** R-F2 es un recálculo con referencias externas exactas, y R-F1, un contraste de estructuras con todas las alternativas publicadas, sin seleccionar ninguna.
- **Revisión:** ya la cubren la auditoría interna y el control de vigencia (§6–§7).
- **Lo que no cambia:** la crítica de Fable de la 4.8 se conserva como registro (`…_4_8/CRITICA_FABLE_PM1.md`). Sus afirmaciones sobre el doble cómputo quedan matizadas en `INFORME_REINVERSION_4_8_1.md` §4.

## 6. Auditoría interna [auditor]

**Quién, cuándo y qué revisó.**
- **Revisor:** un agente de Claude (Opus) con contexto separado, del 10-nov-2026, de 19:41 a 19:57 CET.
- **Seguimiento [Claude]:** dejó constancia de su avance en un archivo de progreso, revisado durante la ejecución.
- **Material:** `MATERIAL_AUDITORIA_4_8_1.txt`, 47 archivos, SHA-256 `4315129b…5ee55f20`.
- **Límite:** no ejecutó nada que use LibreOffice.
- **Informe:** `AUDITORIA_INTERNA_4_8_1.md`.

**Hallazgos y qué se hizo [Claude]:**

| Hallazgo | Clase | Corrección |
|---|---|---|
| Y-a: formato del informe antiguo aceptado | bloqueante | La huella de contenido aplica NFKC y casefold y conserva solo letras y cifras. Pruebas nuevas: puntuación, NFD, separadores y comillas. Mutación M10. El detector de casi duplicados que proponía el auditor **no** se adoptó: bloquearía correcciones legítimas, como reescribir solo la línea de material que pide el propio pipeline. El límite se declara (§3) |
| Y-b: auditoría histórica con otro nombre | bloqueante | Se anotan como conocidas todas las auditorías del expediente: carpeta, `historial_cierres/`, `cierre_vigente.json` y respuestas. Registro persistente `auditorias_conocidas.json`. Pruebas: auditoría histórica con otro nombre, penúltima respuesta y registro sin el estado ni los archivos. Mutaciones M11 y M12 |
| Y-c: den no neutral | importante | Composición de den publicada (§3.1 del informe). Nueva estructura SRF, con la variante del auditor; da sus mismas cifras (65,38 / 59,95 con λ = 1,15 y 62,10 / 55,36 con θ = 1). f corregido con den medido frente a la amortización que se repone (530,01). El auditor citaba 1,1442 con λ = 1,15 en su informe final tal como se devolvió a la sesión. Ese texto no se conserva íntegro en el árbol: la transcripción es condensada. Con esta definición sale 1,1649, y no se ha reconstruido cómo obtuvo su cifra (V-6) |
| Y-d: salto del terminal | importante | Variante continua, con los años proporcionales a las ventas, y su efecto en cada celda («Δ conv.»). Se matiza «coherentes» en el informe y en D-N3b. La reposición de los años 1–10 se reclasifica como convención |
| Y-e: retiradas de la 4.8 sin marcar | importante | Marcadas en CONTINUIDAD 0f y 0g y en DECISIONES, entrada de la 4.8 |
| Y-f: la documentación prometía de más | importante | El código cubre ahora Y-a, Y-b, Y-g e Y-h. Las afirmaciones se ajustan a lo que se comprueba, con los límites declarados (Anexo D y §3) |
| Y-g: cierre anterior con la auditoría sustituida | menor | Se compara con `cierre_vigente.json`. Prueba y mutación M15 |
| Y-h: solicitud pendiente sin efecto en la vigencia ni en `ficha.py` | menor | Pedir una auditoría nueva archiva el cierre vigente. `motivo_rechazo_cierre` rechaza con una solicitud pendiente. Pruebas y mutaciones M13 y M14. Queda para decisión humana como Q-T5 |
| Y-i: CRLF anulaba una respuesta | menor | La respuesta registrada se compara por contenido sin formato. Prueba y mutación M16 |
| Y-j: huecos de la batería | menor | Se añaden 13 pruebas (de 30 a 43) y 8 mutaciones (M10–M17); M6 se retira porque su comprobación ya no existe. Quedan 16 |
| Y-k: explicación de las fechas | menor | Precisada (§3) |
| Y-l: marcadores y salidas sin escribir | menor | Se completan antes del empaquetado y se comprueban en la verificación final (§10) |
| Y-m: Δ frente a REF mezclaba P0 | menor | Columna Δ frente a P0 en §3.4 y en `rf1_alternativas.csv` |

**Un efecto de la corrección encontrado al volver a ejecutar las baterías [Claude].**
- **Qué pasó.** Con la primera versión de Y-a, la prueba de agotamiento de correcciones de `test_cierre_v2.py` (54/55) y dos de `test_pipeline_sintetico.py` (28/30) fallaron. El auditor sintético escribe una REPETIR idéntica en cada vuelta, y se rechazaba como ya usada.
- **Corrección.** La regla de reutilización se aplica solo a las respuestas que aprueban, porque una REPETIR no puede cerrar nada.
- **Prueba y mutación:** se añadió la prueba «REPETIR repetida» y la mutación M17.
- **Expectativas:** las de las baterías anteriores no se tocaron.

## 7. Control de vigencia [vigencia]

**Quién, cuándo y qué revisó.**
- **Revisor:** un agente de Claude (Opus) con contexto separado, del 10-nov-2026, de unos 15 minutos.
- **Seguimiento [Claude]:** dejó constancia de su avance en un archivo de progreso, revisado durante la ejecución.
- **Material:** `MATERIAL_VIGENCIA_4_8_1.txt`, 36 archivos, SHA-256 `d69532a5…2d5f102c6`.
- **Límite:** no ejecutó nada que use LibreOffice.
- **Informe:** `AUDITORIA_INTERNA_4_8_1_vigencia.md`.

**Qué concluyó sobre los hallazgos de la auditoría:**
- **resueltos:** Y-c, Y-d, Y-g, Y-h, Y-i, Y-k e Y-m;
- **resueltos en parte:** Y-a, Y-b, Y-e, Y-f e Y-j;
- **pendiente declarado:** Y-l.

**Hallazgos nuevos y qué se hizo [Claude]:**

| Hallazgo | Clase | Corrección |
|---|---|---|
| V-1: reordenar líneas o quitar tildes seguía acreditando una aprobación | importante | La huella de contenido no depende del orden (conjunto de líneas) ni de las tildes. Pruebas: línea de material al principio, puntos en orden inverso y sin tildes. Mutaciones M18 y M19 |
| V-2: auditorías históricas que no se llaman `auditoria*.md` | importante | Se anota todo archivo de texto del expediente con forma de auditoría, con cualquier nombre y en cualquier subcarpeta. Pruebas: mayúscula, `.bak` y subcarpeta. Mutación M20 |
| V-3: cifras y textos desfasados | menor | Corregidos: «las cinco», 61,63–65,38, 1.386 filas y la docstring del guion |
| V-4: control de SRF tautológico | menor | Ahora va por `kw_estructura("SRF", 0)` y se añade un control fila a fila |
| V-5: ROIC y S2C de SRF no efectivos | menor | Columnas `s2c_efectivo` y `roic_efectivo` en el CSV. El ROIC efectivo del terminal se publica en el informe §3.6, con la implicación de θ alto |
| V-6: cifra 1,1442 no transcrita | menor | Se repone en la transcripción de la auditoría (Y-c), que ahora se declara condensada. **Documentado, no comprobable:** el informe original no se conserva íntegro |
| V-7: la opción «no» de Q-T5 estaba mal descrita | menor | Reescrita con todo lo que implicaría; Q-T5 añadida a §9 |
| V-8: documentación desalineada | menor | LEEME a 50/50; Anexo D y DECISIONES («no puede acreditar una aprobación»; la REPETIR, aparte); docstrings de `pipeline.py` |
| V-9: registro ilegible sin mensaje | menor | Código 6 y «REGISTRO DE AUDITORÍAS ILEGIBLE». Prueba y mutación M21 |
| V-10: una auditoría rehecha con el mismo texto se rechaza | menor | Documentado como límite (Anexo D y §3). No se cambia el comportamiento: contar la repetición como corrección fallida es una decisión de gobierno, preparada como Q-T6 |
| Y-e (residuo): «contiene doble cómputo» sin matiz | — | Marcado como retirado en DECISIONES y en CONTINUIDAD |

**Tras estas correcciones** [Claude]:
- batería de auditorías 50/50;
- mutaciones 20 de 20;
- las demás baterías, vueltas a ejecutar después (§10).

## 7b. Tercera revisión [tercera]

**Quién, cuándo y qué revisó.**
- **Revisor:** un agente de Claude (Opus) con contexto separado, del 10-nov-2026, de 21:05 a 21:15 CET.
- **Seguimiento [Claude]:** dejó constancia de su avance en un archivo de progreso, revisado durante la ejecución.
- **Material:** `MATERIAL_VIGENCIA2_4_8_1.txt`, 20 archivos.
- **Límite:** no ejecutó nada que use LibreOffice.
- **Informe:** `AUDITORIA_INTERNA_4_8_1_tercera.md`.

**Qué concluyó sobre los hallazgos del control de vigencia:**
- **resueltos:** V-1 a V-5, V-7 y V-9 (este último, con un residuo);
- **en parte:** V-6 y V-8;
- **resuelto como documentación:** V-10.

**Hallazgos nuevos y qué se hizo [Claude]:**

| Hallazgo | Clase | Corrección |
|---|---|---|
| W-1: volver a cortar las líneas acreditaba una aprobación | importante | La huella es el multiconjunto de palabras de todo el texto, sin depender de los cortes de línea. Prueba: líneas cortadas a 170 columnas, el ancho con el que H2 sigue dando APROBADO; con cortes más estrechos, H2 da REPETIR, que no cierra. Mutación M22 |
| W-2: cp1252, UTF-16 y relleno de más de 2 MB | menor | Se lee UTF-8, UTF-16 con BOM o cp1252; se descartan solo los binarios; el límite pasa a 50 MB. Pruebas para los tres casos. Mutación M24 |
| W-3: respuesta que no es UTF-8, y registro con tipos inválidos | menor | No se consume; el pipeline sigue esperando, con el motivo. El registro valida sus tipos (código 6). Pruebas y mutaciones M25 y M26 |
| W-4: salidas desfasadas | menor | Se regeneran (§10) |
| W-5: restos de documentación | menor | Textos con «corregidos o documentados»; «multiconjunto de palabras»; «no puede acreditar una aprobación» en la nota, en `cierre_v2.py` y en `pipeline.py`; límite completo en CONTINUIDAD y DECISIONES. Mutación M23 (solo la carpeta y `historial_cierres/`) |

**Después de esta revisión:**
- **Resultados [Claude]:** batería de auditorías 55/55 y mutaciones 25 de 25 (§10).
- **No hubo una cuarta revisión independiente.** Las correcciones de W-1 a W-5 las cubren:
  - sus pruebas y sus mutaciones;
  - las baterías completas;
  - la verificación final sobre una descompresión limpia (§10).

## 8. Controles históricos

Los resultados esperados sobre este árbol, y por qué, están en `resultados/LEEME_BATERIAS_HISTORICAS.md`.

## 9. Incertidumbres y decisiones pendientes

- **P-M1 sigue abierta.** Qué parte de la inversión para crecer repone es **información insuficiente** (Q-E1 a Q-E3).
- **Abanico.** Hasta que se responda, el abanico por requisito y estructura es el de `INFORME_REINVERSION_4_8_1.md` §3.4. Ningún extremo es una cota.
- **Decisiones**, con los campos humanos vacíos:
  - D-N3b revisada, D-N3e, Q-T4, Q-T5 y Q-T6: en `financiero/decisiones_y_preguntas_4_8_1.json`;
  - D-N3c, D-N3d, Q-T1 a Q-T3 y Q-E1 a Q-E7, de la 4.8: sin cambios;
  - D-N1 a D-N3, de la 4.7.1: sin cambios.
- **Siguiente fase identificada: N4**, no iniciada. Consiste en investigar los 38 ceros pendientes de Vidrala, empezando por L26 y C48, con evidencia y una propuesta por partida. La IA no confirma ceros.

## 10. Verificación final

**Quién y cuándo [Claude]:** 10-nov-2026, de 21:50 a 22:58 CET, en el contenedor de trabajo. LibreOffice siempre en secuencia.

### 10.1 Sobre el árbol montado

El árbol del paquete se montó desde el ZIP 4.8 intacto (SHA-256 `6fc60aed…7c3f`), más los 12 archivos declarados y el expediente `…_4_8_1/`. Así no entran restos de pruebas. Se ejecutó todo sobre una copia:

| Qué | Resultado |
|---|---|
| `ejecutar_pruebas_reparacion.sh` | 114/114 y 30/30, PASA |
| Solicitudes de auditoría | 55/55 |
| Estados | 28/28 |
| Resumen | 45/45 |
| Cierre | 55/55 |
| Controles 4.2 a 4.6.1 | Completos |
| 4.7, 4.7.1 y 4.8 | 45 de 49, 38 de 44 y 33 de 36, por diseño (`resultados/LEEME_BATERIAS_HISTORICAS.md`) |
| Baterías del resumen de la 4.7.1 | Coinciden (versión de la 4.8.1); la versión de la 4.8 da «HAY DIFERENCIAS», por diseño |
| `comprobar_entrega_4_8_1.py` | **30 de 30** |

Sus salidas son las de `resultados/`.

**Corrección del LEEME en este paso.** El control de la 4.8 da 33 de 36, no 34. Con el manifiesto regenerado, su comprobación «respecto a la 4.7.1 solo cambian los archivos declarados» ve también los archivos que cambia la 4.8.1 (`verificacion.md`, `agentes_sinteticos.py`, `test_resumen_v2.py` y `cierre_v2.py`). Es una consecuencia de las huellas, no una regresión. El LEEME lo dice así, y la batería de auditorías pasa allí de 50/50 a 55/55.

### 10.2 Sobre descompresiones limpias de un ZIP candidato

El ZIP candidato difería del final solo en este apartado, en `CAMBIOS_ARCHIVOS.txt` y en el manifiesto.

**Fechas renovadas (`unzip -DD`) y TZ=UTC:**
- `bash verificar_paquete.sh completa`: **RESULTADO GLOBAL: PASA**, código 0, en 8 min 43 s;
- manifiesto: 1.539 archivos, sin modificados, ausentes ni de más;
- piloto: 35;
- 114/114 y 30/30;
- auditorías: 55/55;
- estados: 28/28;
- resumen: 45/45;
- cierre: 55/55.

**Después, en la misma descompresión**, los controles históricos, uno detrás de otro. Todos dan una salida **idéntica byte a byte** a su referencia:
- 4.2, 4.3, 4.3.1, 4.4, 4.5, 4.6 y 4.6.1: completos;
- 4.7: 45 de 49;
- 4.7.1: 38 de 44;
- 4.8: 33 de 36;
- comparación de las baterías de la 4.7.1, versión de la 4.8: «HAY DIFERENCIAS»;
- comparación, versión de la 4.8.1: coinciden;
- **4.8.1: 30 de 30.**

**Fechas del ZIP descomprimidas en CET (TZ=Europe/Madrid) y en UTC (TZ=UTC)**, con una hora de diferencia en la fecha de los archivos:
- solicitudes de auditoría: 55/55 en los dos modos;
- estados: 28/28 en los dos modos.

**Conservación:**
- en los tres modos, después de las pruebas, ningún archivo del manifiesto está modificado ni ausente;
- los archivos de más son solo los de trabajo de las pruebas que ya documenta `CONTINUIDAD.md` §2: el perfil de LibreOffice y las salidas de `personaje_v2/pruebas/`;
- P1 conserva su huella (`b4e47afc…c445a4`).

### 10.3 Sobre el ZIP final

Se repite en el ZIP final, en una descompresión limpia con fechas renovadas y TZ=UTC, `bash verificar_paquete.sh completa`. El resultado consta en la hoja de continuidad que acompaña a la entrega, porque no puede ir dentro del propio ZIP.
