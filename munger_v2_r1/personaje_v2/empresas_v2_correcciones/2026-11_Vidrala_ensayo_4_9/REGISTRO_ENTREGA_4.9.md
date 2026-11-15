# Registro de la entrega 4.9 · integridad de la auditoría vigente (R-V1) e investigación N4 de Vidrala

**Encargo:** «Munger V2 — Encargo 4.9», recibido el 11-nov-2026, posterior a la revisión independiente de la 4.8.1 (ChatGPT).
**Base:** `munger_v2_r1_entrega4.8.1_auditorias_y_reinversion.zip`, SHA-256 `bfbbbf2c6b6aad3e8e31a6e20d09cf048795278cd52aeaef938a5b460ddbfdfa`.

**Quién hizo qué:**
- **Ejecución principal:** Claude (Opus).
- **Auditorías internas:** Claude con contexto separado: una auditoría (§6) y dos controles de vigencia (§7 y §7 bis). No son una revisión externa.
- **Revisión externa:** la hará ChatGPT, posterior y fuera de esta entrega.

## 1. Partida

**Verificación de arranque** (descompresión `verif_4_8_1`, conservada con sus registros):
- huella del ZIP coincidente;
- `verificar_paquete.sh completa`: PASA, código 0;
- controles históricos con los resultados previstos para el árbol 4.8.1 y salidas idénticas a sus referencias;
- manifiesto intacto.

**Descompresión de trabajo nueva** del mismo ZIP: huella, versión 4.8.1 y manifiesto comprobados (1.539 archivos; 0 modificados, 0 ausentes, 0 de más) antes de cambiar nada. La tanda de arranque no se repitió.

## 2. Qué se hizo

| Parte | Qué | Dónde |
|---|---|---|
| R-V1 | Reproducción con el código 4.8.1 (24/100); reparación (funciones A y B separadas, huella fiel, transformaciones inocuas, compatibilidad), más Z-1 y Z-2 de la auditoría interna y V-1 a V-3 y W-1 a W-4 de los controles de vigencia; batería nueva de 103, obligatoria; 31 mutaciones, todas detectadas | `INFORME_RV1_4_9.md` · `reproduccion/` · `personaje_v2/pruebas/test_integridad_auditoria_v2.py` |
| N4 | 38 entradas investigadas con cuadres completos, versión española y ESEF; clasificación por exclusión con condiciones generales; dependencias; efectos por recálculo en copias identificadas; excepciones de estructura; matriz; propuestas sin firmar; 19 pruebas contra falsos positivos | `INFORME_N4_4_9.md` · `n4/` · `propuestas/` |
| ROIC | Corrección de la afirmación de la 4.8.1: la justificación sí consta; no se elige estructura | `PRECISION_ROIC_4_9.md` |
| Automatización | Propuesta de política futura, sin activar | `PROPUESTA_AUTOMATIZACION_4_9.md` |
| Continuidad | `CONTINUIDAD.md` (§1 resumida y cronológica, §2 con la verificación vigente y con dónde escriben las pruebas, §4 en orden, §9 numerada de forma coherente), `PROMPT_NUEVA_VENTANA.md`, `VERSION` y el LEEME de controles históricos de la 4.9. Copias de las versiones 4.8.1 en `reproduccion/` | raíz · `resultados/LEEME_BATERIAS_HISTORICAS.md` |

## 3. Archivos cambiados respecto a la 4.8.1

**Modificados:**
- `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `verificar_paquete.sh`, al que se añade el bloque obligatorio de la batería de integridad;
- `personaje_v2/scripts/cierre_v2.py` y `personaje_v2/scripts/pipeline.py`;
- `personaje_v2/scripts/ficha.py`, `personaje_v2/scripts/informe.py` y `personaje_v2/scripts/resumen.py`, que leen el estado y la ficha con una función local tolerante (Z-2 y V-1);
- `personaje_v2/ANEXO_D_salidas_y_formatos.md` y `personaje_v2/DECISIONES.md`;
- `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`.

**Nuevos:** `personaje_v2/pruebas/test_integridad_auditoria_v2.py` y el expediente `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/`.

**Intactos:** ningún original, expediente anterior, libro de referencia ni decisión registrada se ha modificado. `fase1_decisiones.json` de la referencia conserva su huella de la 4.8.1. Lo comprueba `scripts/comprobar_entrega_4_9.py`.

## 4. Decisiones técnicas tomadas (pendientes de revisión humana)

- **Transformaciones inocuas** (D-RV1a): BOM, CRLF/CR, saltos finales y NFC/NFD. Los espacios al final de línea **no** se admiten, porque en Markdown dos espacios finales son un salto de línea.
- **Cierres de la 4.8.1 sin huella fiel** (D-RV1b): solo por bytes exactos.
- **Sin registro de la respuesta aprobada, no se cierra** (Z-1): hace falta una auditoría nueva, en vez de atribuir la huella del archivo actual.
- **Archivos de control ilegibles o `auditoria.md` no UTF-8** (Z-2): retiran la aprobación; con `estado_pipeline.json` ilegible, `pipeline.py` termina con el código nuevo 6 (o 5 si queda una retirada pendiente).
- **N4, clasificación por exclusión** (Z-4): un rótulo fuera de la lista blanca de la partida, una cita fuera de su página, una comparativa que contradice, la unidad no localizada o un ilegible en la columna del año bajan la entrada a la clase 3.
- **N4, intereses de 2018–2025:** clase 2 con una reserva en el componente de arrendamientos, que es una clase 3 en ese componente, en lugar de bajar toda la entrada a clase 3.
- **N4, principal de arrendamientos de 2018:** clase 4 (no aplicable), por la regla ya registrada en `fase1_decisiones.json` («Arrendamientos = solo pasivos NIIF 16 …»). La primera versión de la matriz la clasificaba como 3 sin tener en cuenta esa regla. Se corrigió al leer `fase1_decisiones.json` completo, que además de P1 contiene una regla y decisiones anteriores sobre deuda y arrendamientos, sin fecha ni firma.

## 5. Modelos

Opus en todo el procedimiento. **Fable no se usó.** El trabajo era sobre todo de comprobación reproducible (código, cuadres y recálculo), con criterios fijados por el encargo, y una crítica de razonamiento con Fable no aportaba bastante frente a su coste. No hubo subagentes de ejecución. La auditoría interna y los dos controles de vigencia usaron tres agentes distintos con contexto separado, del mismo modelo (Opus).

## 6. Auditoría interna

**Quién y sobre qué.** Un agente de Claude (Opus) con contexto separado, que no participó en el trabajo, sobre una copia propia del árbol. El material fijado es `MATERIAL_AUDITORIA_4_9.txt` (54 huellas; SHA-256 `be02e0f86b035e183d1910118e1477bdaa4dd5ab1ba6bf2f36880b703eabf598`). El informe está en `AUDITORIA_INTERNA_4_9.md`, con una nota de conservación al principio, y los scripts y salidas del auditor en `auditoria_interna/material_auditor/`. No es una revisión externa.

**Incidencias de la propia auditoría:**
- el auditor ejecutó `test_n4_comprobaciones.py` sin `-B` y regeneró un `.pyc` que estaba en el material (lo declara él mismo, §0);
- ejecutó `test_estados_v2.py`, que usa LibreOffice, quizá a la vez que otra tarea con LibreOffice (Z-9). Ese resultado (28/28) coincide con el de las verificaciones de Claude, antes y después.

**Hallazgos y tratamiento** (las cifras de la auditoría son las del material fijado: 63 pruebas, 15 mutaciones, 24/61 y 12 pruebas de N4):

| Hallazgo | Gravedad | Tratamiento | Dónde se comprueba |
|---|---|---|---|
| **Z-1.** Sin registro de la respuesta aprobada (`cierre_vigente.json` borrado en un cierre de la 4.6.1, cierre de la 4.6, o de la 4.9 sin estado ni `cierre_vigente.json`), `ficha.py` volvía a cerrar con cualquier APROBADO y le atribuía la huella actual. Anterior a la 4.9 | Bloqueante | **Corregido.** `motivo_rechazo_cierre`: sin `auditoria_respuesta` ni `cierre_vigente.json` con huella, no hay cierre: hace falta una auditoría nueva | Grupo H (6 casos), mutación M21. Con el código 4.8.1, los 6 fallan |
| **Z-2.** Un `auditoria.md` no UTF-8 o un archivo de control ilegible rompían las vías con traza (código 1) y la aprobación seguía publicada; la rama «no es UTF-8» era inalcanzable | Bloqueante | **Corregido.** Lectura de bytes y decodificación explícita; `leer_json_control` en `cierre_v2.py`, `ficha.py` y `resumen.py`; `pipeline.py` retira primero y termina con código 6 (o 5) | Grupo H (9 casos), mutaciones M22 y M23. Con el código 4.8.1, los 9 fallan |
| **Z-3.** La batería no fijaba los límites de la lista cerrada (NFKC, caracteres de formato, NBSP, separadores) ni la rama de huella fiel sin estado | Importante | **Corregido.** Pruebas unitarias de esos límites en el grupo G; caso «sin estado y en CRLF» (H) | Mutaciones M16–M20 |
| **Z-4.** La cita, la comparativa y la unidad no intervenían en la clasificación; clases 4 fijadas en el código; tolerancia a erratas sin distinguir columna; 15 de 16 falsos positivos por rótulos alternativos | Importante | **Corregido.** `aplicar_condiciones_generales`; clasificación por exclusión con listas blancas; clase 4 condicionada a la norma por fecha y a la ausencia de la línea; ilegibles solo tolerados en la comparativa. En los datos reales no cambia ninguna clase | `test_n4_comprobaciones.py`: 16/16 tras esta corrección, con los 14 rótulos del auditor; 19/19 en el paquete final (§7) |
| **Z-5.** Las decisiones de 2017–2018 se llamaban «precedentes humanos» sin fecha ni firma | Importante | **Corregido.** «Decisiones escritas en `fase1_decisiones.json`, sin fecha ni firma» en `CONTINUIDAD.md`, `DECISIONES.md`, los informes, la propuesta y la matriz (campo `registro_en_fase1_decisiones`); D-N4-na pide confirmarlas si se quiere apoyarse en ellas | `comprobar_entrega_4_9.py` (cobertura) |
| **Z-6.** `f`, el paso REVISAR→PASA y el precio de Sí no estaban en las salidas | Menor | **Corregido.** `efectos_n4.py` lee Diagnóstico V6!C12 y C50 y calcula `precio_de_si.p_estrella` con los tres valores recalculados | `n4/efectos/efectos_n4.json`; `comprobar_entrega_4_9.py` |
| **Z-7.** Faltaban los contrastes españoles de 2023 y de otros activos 2024–2025; explicación de minoritarios fija; sin la tabla de dependientes; sin la discrepancia de la nota 8 | Menor | **Corregido.** Contrastes añadidos (2023 con la comparativa del informe español de 2024); explicación con las menciones reales de cada año y la tabla de dependientes de 2025; la discrepancia de la nota 8 en `INFORME_N4_4_9.md` §4 y §6 | `n4/matriz_n4.json` |
| **Z-8.** Remisiones a archivos que no existían | Menor | **Corregido** en el paquete final: el registro, el LEEME y la primera auditoría ya estaban en el candidato; el control de vigencia y la salida de referencia del control de la 4.9 se añadieron después de ese control (§7 y §8) | `comprobar_entrega_4_9.py` (existencia) |
| **Z-9.** Comandos que sobrescriben salidas o escriben `__pycache__`; `.pyc` en el material; `test_estados_v2.py` usa LibreOffice; `.lo_perfil/` en el árbol | Menor | **Corregido.** Comandos con `--salida` a temporales y `python3 -I -B`; §2 de `CONTINUIDAD.md` dice qué pruebas usan LibreOffice; el paquete se construye sin `__pycache__` ni archivos de perfiles de LibreOffice; solo quedan los directorios vacíos que ya traía el ZIP de la 4.8.1 (§7, V-6). `MATERIAL_AUDITORIA_4_9.txt` se conserva tal como se auditó | Manifiesto de la verificación final (§8) |
| **Z-10.** Comas del mensaje de arranque, cabecera del verificador, tachado en el Anexo D, título de §9 y lista de archivos de `INFORME_RV1_4_9.md` | Menor | **Corregido.** El mensaje de arranque enumera las entregas en una lista | — |

## 7. Control de vigencia de las correcciones

**Quién y sobre qué.** Otro agente de Claude (Opus) con contexto separado, sobre una descompresión del paquete candidato, sin usar LibreOffice. El material fijado es `MATERIAL_VIGENCIA_4_9.txt` (101 huellas; SHA-256 `479cf703d00b57f4a315729635dfff7ecc9dfb7ce41e25e711da735f561be9e3`), igual al principio y al final; el auditor no cambió ningún archivo de su copia. Informe en `AUDITORIA_INTERNA_4_9_vigencia.md`, y sus scripts y salidas en `auditoria_interna/material_vigencia/`.

**Vigencia de Z-1 a Z-10:** vigentes Z-1, Z-3, Z-5 y Z-6; vigentes con reservas las otras seis; ninguna no vigente.

**Hallazgos nuevos y tratamiento:**

| Hallazgo | Gravedad | Tratamiento | Dónde se comprueba |
|---|---|---|---|
| **V-1.** `material_auditoria.json` o `ficha.json` ilegibles: traza y código 1 en las cuatro vías, con la aprobación publicada | Importante | **Corregido.** `material_auditoria.json` ilegible o sin «id» y «archivos» es motivo de retirada; una `ficha.json` ilegible ya no es «sin salida cerrada»: se archiva y se retira la aprobación (en la primera corrección, `ficha.py` volvía a escribir la ficha oficial; véase W-2 en §7 bis) | Grupo I (8 casos), mutaciones M24 y M26. El segundo control de vigencia (W-2) mostró que la reescritura de la ficha por `ficha.py` dejaba un registro más débil: se cambió para que no vuelva a cerrar (§7 bis) |
| **V-2.** JSON válido que no es un objeto, estructura interna errónea, estado o `auditoria.md` como carpetas | Menor | **Corregido.** `leer_json_control` exige un objeto; `_motivo_estructura` valida `solicitudes_auditoria`, `auditoria_respuesta` y `material_auditoria.json`; `pipeline.py` captura también `OSError` y valida el tipo del estado; la lectura de `auditoria.md` trata `OSError` como motivo | Grupo I (7 casos), mutaciones M25 y M28 |
| **V-3.** Sin estado, `ficha.py` reescribía `cierre_vigente.json` sin la solicitud ni la huella fiel | Menor | **Corregido.** `registrar_cierre` conserva la solicitud, la huella fiel y la huella de bytes de la respuesta aceptada | Grupo I (1 caso), mutación M27 |
| **V-4.** N4: seis engaños estructurales pasaban la clasificación por exclusión | Menor | **Corregido en lo probado y declarado el resto.** Excepciones de estructura (líneas sin rótulo, segundo bloque, «of which»), unidad en la cabecera del estado y «outside shareholders» en el balance. En los datos reales no cambia ninguna clase. El límite queda en `INFORME_N4_4_9.md` §2 y en `CONTINUIDAD.md` §8 | `test_n4_comprobaciones.py` 19/19 |
| **V-5.** Contradicción sobre 2023 en el informe; «igual» en minoritarios 2023 con cifras reexpresadas; sin contraste de otros activos 2023 | Menor | **Corregido.** Texto de 2023 armonizado; la explicación declara la reexpresión; contraste de otros activos 2023 con la comparativa española de 2024 (816.395 frente a 821.341) | `n4/matriz_n4.json` |
| **V-6.** Carpeta `.lo_perfil/` vacía; duraciones distintas; uso sin `-B`; texto de la tabla antes/después | Menor | **Corregido**, salvo la carpeta: son directorios vacíos que ya traía el ZIP de la 4.8.1 en `pruebas/sintetico/EmpresaX_cero_pendiente/` (no son archivos ni están en el manifiesto) y se conservan como estaban. Las duraciones se fijan con las observadas en §8 | — |
| **V-7.** El registro daba por existentes archivos posteriores; el límite de la reescritura coordinada exigía más archivos de los necesarios | Menor | **Corregido.** Z-8 se redacta con el orden real; el límite dice que bastan dos archivos | `INFORME_RV1_4_9.md` §5; `CONTINUIDAD.md` §8 |

**Una consecuencia que el control de vigencia no vio y que apareció en la verificación del candidato.** La corrección de Z-1 hace que el control de la 4.6 dé 23 de 24 (§8). Está declarada en `INFORME_RV1_4_9.md` §5 y queda como decisión D-RV1c.

**Además, en la misma verificación:** al cambiar `ficha.py` y `resumen.py`, la primera versión dependía de una función nueva de `cierre_v2.py`, y las reproducciones de la 4.8.1 que combinan el código de la 4.8 con esos scripts fallaban (25 de 30 en vez de 28 de 30). Se corrigió con una función local en cada script.

**Segundo control de vigencia.** Como las correcciones de V-1 a V-7 son posteriores al control, otro agente con contexto separado las revisó sobre el paquete final candidato (§7 bis).

## 7 bis. Segundo control de vigencia

**Quién y sobre qué.** Un tercer agente de Claude (Opus) con contexto separado, sobre una descompresión del paquete candidato 2. El material fijado es `MATERIAL_VIGENCIA_2_4_9.txt` (150 huellas; SHA-256 `b2fac6fd13dceae9a9e2faf20db9151d38a8dcec0dad81449465e03fec2e6046`), igual al principio y al final. Informe en `AUDITORIA_INTERNA_4_9_vigencia_2.md`; scripts y salidas en `auditoria_interna/material_vigencia_2/`.

**Incidencia: se incumplió la regla de LibreOffice.** A las 12:36, en un ataque, el auditor ejecutó `pipeline.py` sin `--desde` sobre una copia sin `estado_pipeline.json`. El pipeline empezó en el paso 0 y arrancó LibreOffice unos 30 segundos (lo declara él mismo y deja la lista de archivos creados en su `.lo_perfil/`). **En ese momento estaba en curso la verificación de Claude sobre el candidato 2 (12:28–12:38)**, con su propio LibreOffice y otro perfil. Esa verificación dio PASA, pero no se usa como resultado de referencia: la verificación final (§8) se repite en secuencia, sin ninguna otra tarea en marcha.

**Vigencia de V-1 a V-7:** V-5 vigente; las otras seis, vigentes con reservas; ninguna no vigente.

**Hallazgos nuevos y tratamiento** (todos menores; ninguno cambia un dato real):

| Hallazgo | Tratamiento | Dónde se comprueba |
|---|---|---|
| **W-1.** Ficha con «cierre» que no es un objeto o solicitud sin «id»: traza con la aprobación publicada. Tipos erróneos de `historial`, `cierres_archivados` o `paso`: traza después de retirar. Accesos que ya existían en la 4.8.1 | **Corregido.** `leer_ficha_control` exige que «cierre» sea un objeto; `_motivo_estructura` exige «id» en las solicitudes y los tipos de esos tres campos; `pipeline.py` trata esos errores como un estado ilegible (código 6, después de retirar); `archivar_salidas` no actualiza un estado con esos tipos erróneos | Grupo I (5 casos), mutación M29 |
| **W-2.** `ficha.py` sobre una ficha ilegible volvía a cerrar (código 0) con un registro más débil o con una ficha que no era vigente | **Corregido.** `ficha.py` archiva la ficha ilegible, retira la aprobación y no vuelve a cerrar: hace falta una auditoría nueva | Grupo I (2 casos, con y sin estado; también la llamada siguiente de `informe.py`), mutación M30 |
| **W-3.** `auditoria.md` sin permiso de lectura interrumpía el archivado antes de retirar las filas | **Corregido** leyendo el código: la copia es opcional y `RETIRADA.json` dice que no se pudo hacer. **No probado:** la batería se ejecuta como superusuario | `INFORME_RV1_4_9.md` §5 |
| **W-4.** Un `material_auditado` con «../» sacaba el archivo de la retirada del expediente (anterior a la 4.9) | **Corregido.** El nombre de la carpeta se limpia | Grupo I (1 caso), mutación M31 |
| **W-5.** N4: once engaños sintéticos más pasan; dos frases del informe decían más de lo que hace el código; el contraste español no aplicaba las excepciones de estructura | **En parte.** Las frases se corrigieron y el contraste español aplica ya las excepciones (sin cambios en los datos reales). Los once engaños **no se han convertido en pruebas ni se rechazan**: quedan como límite declarado (`INFORME_N4_4_9.md` §2) y como requisito previo de la automatización | `test_n4_comprobaciones.py` 19/19 |
| **W-6.** Restos documentales (límite con tres archivos, fila Z-9 frente a §7, frase general sobre archivos ilegibles, descripción del caso de la ficha, «16/16» de Z-4) | **Corregido** | — |

**Lo que no se ha hecho:** los tratamientos de W-1 a W-6 no los ha revisado un cuarto control independiente. Los ha comprobado Claude con la batería (103/103), las mutaciones (31 de 31) y la verificación final (§8). Queda para la revisión externa.

## 8. Verificación final

Todas las ejecuciones de esta sección las hizo Claude, en secuencia y sin ninguna otra tarea con LibreOffice en marcha.

**Candidatos anteriores.** La verificación del candidato 1 descubrió dos problemas que se corrigieron (la consecuencia de Z-1 sobre el control de la 4.6 y la dependencia de `ficha.py` y `resumen.py` de una función nueva; §7). La del candidato 2 coincidió con la incidencia de LibreOffice del segundo control (§7 bis) y no se usa como referencia.

**Paquete candidato 3** (el contenido final, salvo este apartado, la salida de referencia del control de la 4.9 y una corrección del propio control; descompresión limpia, 11-nov-2026, de 13:34 a 14:03):
- `bash verificar_paquete.sh completa`: **PASA**, código 0, en 9 minutos y 10 segundos. Manifiesto: 1.732 archivos, 0 modificados, 0 ausentes, 0 de más. Entorno: PASA. Piloto: 35 comprobaciones CUMPLEN y salida idéntica. `test_comprobadores.py` 114/114; `test_pipeline_sintetico.py` 30/30; integridad 103/103; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55.
- Controles de las entregas, en el orden del LEEME y **con salidas idénticas a sus referencias**: 4.2 (45), 4.3 (217 de 217), 4.3.1 (43 de 43), 4.4 (72 de 72), 4.5 (60 de 60), 4.6 (23 de 24, por Z-1), 4.6.1 (23 de 23), comparación de baterías de la 4.8.1 («HAY DIFERENCIAS», de huellas), 4.7 (45 de 49), 4.7.1 (38 de 44), 4.8 (32 de 36), comparación de baterías de la 4.8 («HAY DIFERENCIAS»), 4.8.1 (27 de 30).
- `comprobar_entrega_4_9.py`: **38 de 39**. El caso que no cumplía era un **error del propio control**, no del paquete: al actualizar el número de mutaciones (de 28 a 31) con un reemplazo de texto, se cambió también el «28» de «28 con fila en la Historia» del recuento de N4. El recuento real sigue siendo 28 con fila y 10 auxiliares. Se corrigió el control.

**Paquete candidato 4** (el candidato 3 con el control corregido): `comprobar_entrega_4_9.py` sobre una descompresión limpia: **39 de 39**, código 0 (8 reejecutan, 17 recalculan y 14 solo constatan). Su salida es la referencia `resultados/comprobar_entrega_4_9_salida.txt`.

**ZIP final.** Es el candidato 4 con este apartado y esa salida de referencia añadidos, y `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` regenerados. Su verificación completa, sobre otra descompresión limpia y posterior a este registro, no puede figurar dentro del propio ZIP: se entrega aparte, junto al ZIP, en `munger_v2_r1_entrega4.9_integridad_auditoria_y_N4.VERIFICACION.txt`.

## 9. Límites, carencias y pendientes

- **R-V1:** no es un clasificador de significado, ni detecta una reescritura coordinada de `auditoria.md` y los registros que la acreditan (bastan dos archivos; `INFORME_RV1_4_9.md` §5). Solo se validan los campos de los archivos de control que lee el cierre; el caso de permisos (W-3) no se puede probar como superusuario. Q-T4 sigue fuera.
- **N4:**
  - la línea del estado de flujos en la que están los intereses de arrendamientos no se publica (reserva de 8 entradas; ligada a P3 y C49);
  - de 2017 a 2022 solo se conserva la traducción inglesa (2023 se contrasta con la comparativa del informe español de 2024);
  - la discrepancia documental de la nota 8 de 2025 (pagos de arrendamientos iguales a los gastos a corto plazo), ya registrada en la 4.2, sigue sin resolver;
  - ningún cero está confirmado.
- **Pendientes de decisión:** `propuestas/decisiones_y_preguntas_4_9.json` y `CONTINUIDAD.md` §9.8.
