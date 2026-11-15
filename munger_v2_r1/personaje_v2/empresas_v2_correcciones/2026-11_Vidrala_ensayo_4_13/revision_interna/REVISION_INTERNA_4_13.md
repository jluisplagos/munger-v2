# Revisión interna · entrega 4.13 (fiabilidad del motor B y conciliación económica)

**Qué es.** Revisión **interna** de Claude, hecha por un agente en contexto separado que no participó en el trabajo. **No es la revisión externa ni la sustituye.** Objeto: el código y el material de `/home/claude/trabajo_4_13/munger_v2_r1` tal como estaban el 13-nov-2026 entre las 14:27 y las 14:50.

**Cómo se hizo.**
- Solo lectura del árbol. La única escritura en él es este informe.
- Las pruebas se ejecutaron sobre una copia parcial del árbol en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna_4_13/` (`arbol/`, con `python3 -B` y `soffice` sustituido por un ejecutable que falla: no se lanzó LibreOffice ni el pipeline sobre los expedientes reales).
- Scripts del revisor, en esa carpeta: `scripts/fuzz_tipos.py`, `scripts/sonda_p2.py`, `scripts/caso_no_entregable.py`, `scripts/copia_exp.py`; salidas en `out/`.

**Límites de esta revisión (hechos).**
- No se recalculó ningún libro: las cifras de los libros recalculados (precio de Sí, variantes, alternativas de N, g = 0) se han contrastado entre archivos y con aritmética, no con un recálculo propio.
- El grupo F de la batería no se pudo reproducir (necesita LibreOffice). Los grupos A, B, C, D, G y H no se ejecutaron. El grupo E sí: 28 de 28 con el código final.
- La conciliación de acciones con BORME y CNMV no se pudo contrastar (sin internet; sus PDF no están en el paquete).
- **Incidencia del propio revisor.** A las 14:31 la primera tanda de pruebas llenó el disco durante unos dos minutos (1.300 copias del piloto en la carpeta temporal). Se liberó enseguida. Comprobado después: ningún archivo del árbol tiene fecha posterior a las 14:28, salvo este informe; los 3.796 archivos del manifiesto de la 4.12 siguen presentes. Si en ese intervalo otro proceso intentó escribir en el mismo volumen, pudo fallar: conviene que la orquestación lo tenga en cuenta.

## Resumen por gravedad

| Gravedad | Nº | Hallazgos |
|---|---|---|
| Bloqueante | 1 | R1 |
| Importante | 6 | R2, R3, R4, R5, R6, R7 |
| Menor | 6 | R8, R9, R10, R11, R12, R13 |
| Observación | 5 | R14, R15, R16, R17, R18 |

| Id | Gravedad | Título |
|---|---|---|
| R1 | Bloqueante | `ficha.py` sigue leyendo el material antes de la vigencia: con un JSON roto en nueve archivos del material, o con `ficha.json` de otra estructura, la primera llamada termina en excepción y la aprobación sigue publicada |
| R2 | Importante | La retirada no está protegida frente a tipos anidados en los archivos de control: un elemento mal formado en el registro de publicaciones deja la fila APROBADO y el estado concluido · APROBADO, sin «retirada pendiente» visible |
| R3 | Importante | Regresión del §4: tras una fase C con objetivo emitido, condicionado o bloqueado, una terminación en `no_entregable` no puede escribir su ficha, su informe ni su fila |
| R4 | Importante | La materialidad para el objetivo no tiene «no determinada» ni base: un parámetro sin contraste puede declararse no material para el objetivo, y el objetivo sale «emitido» sin condición |
| R5 | Importante | La configuración auditada de Viscofan (NIIF 16) conserva dos cifras de la base «Caja»: el exceso «observado» de 40,813 y la cota λ = 1,1413 de SRF |
| R6 | Importante | El perímetro NIIF 16 no llega a la palanca S2C: f se calcula con la base nueva y el S2C de la fase B reutilizada sigue anclado en la base «Caja» (interpretación económica) |
| R7 | Importante | Viscofan: queda evidencia activa del 6-oct-2026 y de 53,60 × 45,6036 en el Control maestro, y la conciliación atribuye a la etapa 1 una N que la etapa 1 no usó |
| R8 | Menor | Las fichas oficiales de la 4.13 declaran la aptitud de uso de la 4.12 |
| R9 | Menor | Ámbito de las pruebas: el grupo E se ejecutó antes de las últimas ediciones del código que prueba; el registro cuenta 16 pruebas nuevas y hay 15; ninguna prueba cubre R1, R2 ni R3 |
| R10 | Menor | Las alternativas de N de Viscofan están calculadas sobre el libro de la 4.12 (39,29), no sobre la activa de la 4.13 (38,62) |
| R11 | Menor | Conciliación de arrendamientos: la línea citada de las frases de altas está desplazada en una |
| R12 | Menor | `configuracion_economica.validar` acepta `Infinity` y `NaN` en varios números |
| R13 | Menor | Quedan seis carpetas `__pycache__` en el árbol |
| R14 | Observación | La «variación conjunta necesaria» permite una materialidad «calculada»: correcto según el encargo, con un matiz que conviene declarar |
| R15 | Observación | Campos redundantes de `cierre_vigente.json` que no se comprueban |
| R16 | Observación | `mismo_importe` y los medios céntimos |
| R17 | Observación | `en_la_activa = false` en un grupo de avisos que sí se lee en la activa |
| R18 | Observación | Fecha de un promedio escrita como fecha de un saldo |

---

## R1 · `ficha.py` lee el material antes de la vigencia (bloqueante)

**Hechos comprobados.**
- `personaje_v2/scripts/ficha.py`, líneas 48–50 y 88–92: `cargar()` hace `json.load` sin protección de `fase_a.json`, `fase_b.json`, `fase_c.json`, `resultados.json`, `precio.json`, `referencias_mecanicas.json`, `gramatica.json`, `comprobacion_conjunta.json`, `entrada_v63.json`, `datos_v63.json`, `datos_ausentes.json` y `diagnostico.json`, **antes** del bloque de vigencia (línea 95 en adelante).
- Línea 118: `CIE.motivo_rechazo_cierre(...)` se llama sin protección. Solo `motivo_vigencia` está protegida (`cierre_v2.py`, 663–671).
- Prueba 1 (piloto cerrado de la 4.11, copias aisladas, primera llamada de cada vía; `out/fuzz_raiz.json`, 440 llamadas): con el archivo truncado a la mitad, `ficha.py` termina con `json.decoder.JSONDecodeError`, código 1, y quedan **concluido · APROBADO, la ficha cerrada, `cierre_vigente.json` y la fila APROBADO** en los nueve casos: `fase_a.json`, `fase_b.json`, `fase_c.json`, `datos_ausentes.json`, `entrada_v63.json`, `referencias_mecanicas.json`, `resultados.json`, `precio.json` y `gramatica.json`. Las otras tres vías (pipeline, informe y resumen) retiran bien.
- Prueba 2 (copia del expediente final `vidrala_condicionado`): `fase_c.json` truncado → `ficha.py` → `JSONDecodeError`, código 1; después: `concluido APROBADO`, ficha y cierre presentes, fila APROBADO. Una llamada posterior al pipeline sí retira.
- Prueba 3 (copia del expediente final `viscofan` y del piloto): `ficha.json` con `"hashes": "x"` → `ficha.py` → `AttributeError: 'str' object has no attribute 'get'` en `cierre_v2.py:470` (`motivo_acreditacion_libro`), llamado desde `cierre_v2.py:429` y `ficha.py:118`. La aprobación sigue. Las otras tres vías retiran («la vigencia no se puede comprobar…»).

**Cómo se reproduce.** Copia aislada del expediente con las publicaciones reubicadas (como `test_integracion_v64.copia_piloto`); truncar `fase_c.json`; `python3 -B personaje_v2/scripts/ficha.py COPIA`.

**Consecuencia.** El §3 del encargo pide una guarda «que no dependa de interpretar correctamente el archivo alterado», en la **primera** llamada de las cuatro vías, y dice que no basta capturar los ejemplos aislados. En una de las cuatro vías la guarda sigue dependiendo de leer bien el material. La frase del registro «todas las alteraciones del material retiran la aprobación en la primera llamada» vale para las 25 alteraciones de `sonda_tipos.py`, no para el patrón. Es el mismo defecto que encontró la revisión externa (excepción antes de la vigencia, con la aprobación publicada), por otra puerta.

**Qué haría falta.** En `ficha.py`, comprobar la vigencia antes de cualquier lectura del material (o leerlo con una función que convierta el fallo en motivo), y pasar `motivo_rechazo_cierre` por la misma protección que `motivo_vigencia`. Añadir al grupo E «JSON roto» para **cada** archivo de `MATERIAL_FIJO` y un tipo anidado en `ficha.json`, en las cuatro vías.

## R2 · La retirada no está protegida frente a tipos anidados en los archivos de control (importante)

**Hechos comprobados.**
- `cierre_v2.py`: `archivar_salidas` (748–806), `retirar_publicaciones` (993–1020), `_propias` (917–950), `_retirar_en` (975–990) y `retiradas_pendientes` (1142–1147) interpretan el registro de publicaciones y el estado sin validar sus elementos y fuera de toda protección. `_cargar` (855–859) solo comprueba que `publicaciones` sea una lista.
- `archivar_salidas` mueve primero la ficha, el informe y el cierre al historial y después retira las publicaciones y actualiza el estado: un fallo a mitad deja la retirada a medias.
- Prueba A (copia del expediente final de Viscofan): θ de 0,5 a 0,6 en `configuracion_economica.json` (material alterado) **y** un elemento `null` añadido a `publicaciones` (la entrada válida «publicada» sigue ahí). `pipeline.py … --hasta 8` → `AttributeError` en `cierre_v2.py:923`, código 1. Después: ficha y cierre archivados, **`estado_pipeline.json` sigue en concluido · APROBADO y la fila del CSV sigue en APROBADO**. La segunda llamada falla igual: la aprobación publicada no se retira nunca y no aparece «RETIRADA PENDIENTE» (código 5).
- Prueba B (piloto 4.11; λ = 1,25 más el registro alterado; cuatro vías): con `publicaciones = [null]` o con la entrada sin `csv` (`KeyError: 'csv'`), las cuatro vías terminan con excepción, estado APROBADO y fila APROBADO.
- Prueba C (λ = 1,25 más `estado_pipeline.json` con `paso`, `historial` o `cierres_archivados` a `null`): las cuatro vías terminan con `TypeError` o `AttributeError` (`cierre_v2.py:798–803`); la fila queda «SIN APROBACIÓN VIGENTE», pero `estado_pipeline.json` sigue en concluido · APROBADO.
- Prueba D (material intacto; `out/fuzz_anidado.json`, 1.740 llamadas): con `publicaciones = ["x"]`, `[null]`, `[{}]` o `[{"estado": "publicada"}]`, las vías terminan con excepción y código 1, no con el código 5 que el diseño prevé para un registro ilegible. Aquí la aprobación sigue siendo legítima (el material no cambió).

**Consecuencia.** Hacen falta dos alteraciones (material y archivo de control), así que no es el caso de una sola alteración del §3. Pero el encargo pide ensayar «estructuras anidadas incorrectas en las entradas y archivos de control afectados» y que, si un destino no es actualizable, quede «retirada pendiente visible y sin continuar como aprobado». La prueba nueva del grupo E solo cubre el registro y el estado como lista en la raíz. Con un elemento mal formado, un resumen publicado conserva APROBADO de un material que ya no es el auditado.

**Qué haría falta.** Un plano estructural para `publicaciones_resumen.json` (elementos objeto con `csv`, `empresa`, `expediente` y `estado` de texto) y para los campos de `estado_pipeline.json` que la retirada actualiza; tratar un elemento mal formado como registro ilegible (código 5, retirando lo que se conoce); proteger la retirada entera y actualizar el estado aunque falle la retirada de un destino.

## R3 · Una terminación en `no_entregable` después de la fase C ya no puede escribir sus salidas (importante)

**Hechos comprobados.**
- `objetivo_v64.bloque_ficha` (444–499) fija `estado_del_objetivo` con el tratamiento de la fase C, sea cual sea el estado que se escribe. `contradicciones_salida` (413–423) exige que un objetivo «emitido» o «emitido_condicionado» coincida con `decision.precio_objetivo`, y que uno «bloqueado» vaya con un estado pendiente.
- `ficha.py`, 290–294: con cualquier contradicción no escribe la ficha (código 3), también la oficial de un estado `no_entregable`, que no lleva decisión.
- Prueba 1: copia de `vidrala_condicionado`; `ficha.py COPIA --estado no_entregable --provisional` → «CONTRADICCIÓN en la decisión: objetivo emitido_condicionado None y decision.precio_objetivo None: tienen que coincidir (dos decimales). No se escribe la ficha». Igual con `--estado pendiente_de_investigacion`.
- Prueba 2 (`scripts/caso_no_entregable.py`): copia de `vidrala_condicionado` puesta en el paso 12 sin cierre; `Pipeline.terminar("no_entregable", …)` como hace `pipeline.py:928` cuando `verificar_todo.sh` falla. Resultado: `ficha.py … → 3`, `validar_esquema.py → 2 · no existe ficha.json`, `informe.py → 3`, `resumen.py → 3`; el pipeline registra «aviso: ficha.json (no_entregable) tampoco cumple su esquema», que no es la causa; queda `estado no_entregable`, `ficha_valida: False`, `resumen_pendiente: True`, sin ficha, sin informe y sin fila del estado final.
- Las terminaciones afectadas son todas las posteriores a una fase C con esos tratamientos: `pipeline.py` 834–849, 905–928, 977, 984, 1041, 1051 y 1717. El caso «sin protocolo» (827) no se ve afectado, porque su estado del objetivo no es «emitido».

**Consecuencia.** No deja ninguna aprobación falsa: es del lado seguro. Pero el estado final `no_entregable` deja de publicarse con su ficha y su fila (criterio 7 † y D17), el diagnóstico del registro es engañoso y `resumen_pendiente` no se resuelve nunca. Es una regresión del §4 que la batería no cubre. En la 4.13 habría ocurrido, por ejemplo, si la segunda auditoría de Viscofan hubiera agotado las correcciones.

**Qué haría falta.** Que el bloque del objetivo de una salida que no es la de la fase C (estado `no_entregable` o forzado por el pipeline) diga que no se emite nada, o que `contradicciones_salida` no exija la igualdad cuando el estado no es `concluido` y no hay objetivo emitido. Añadir la prueba: fase C concluida con objetivo condicionado y otra con bloqueo, y terminación en `no_entregable`.

## R4 · La materialidad para el objetivo no tiene «no determinada» ni base (importante)

**Hechos comprobados.**
- `pipeline.py`, 1335–1337: `material_para_objetivo` es un booleano obligatorio. `_coherencia_cobertura_413` (1459–1498) solo aplica el contrato de cobertura a `material_para_accion`.
- Ninguna comprobación mecánica cruza `material_para_objetivo` con los contrastes calculados (para la acción sí: 1483–1486).
- Prueba (`scripts/sonda_p2.py`, caso `no_fundados_no_materiales_objetivo`): en la fase C real de `vidrala_condicionado`, poner `material_para_objetivo = false` en los parámetros sin fundamento suficiente (PM1.estructura tiene contrastes aislados de −0,50 a +7,10 € de precio de Sí; PM1.parametro, de −4,73 a +2,37 €) y actualizar el bloque con el propio evaluador → `coherencia_fase_c` **ACEPTA** con el tratamiento `objetivo_emitido`: objetivo sin condición y sin marca provisional.
- Caso real: `viscofan/Viscofan/fase_c.json`, PM1.familia: cobertura `variacion_conjunta` (ningún contraste), `fundamento_suficiente = false`, `material_para_objetivo = false`. No entra en `hipotesis_que_condicionan` y la ficha da `hipotesis_no_cubiertas_por_el_ambito = []`. En Vidrala, el mismo parámetro, con la misma cobertura, se declaró material para el objetivo y aparece como no cubierto.

**Interpretación.** El agente de Viscofan lo razona como juicio y lo dice en sus inferencias (un λ de hasta ≈ 1,16 daría un requisito dentro del rango de θ). No es un error del agente: es que el contrato no le pide marcar ese juicio ni le deja decir «no determinada».

**Consecuencia.** El §5 pide representar como no determinado lo que no tiene contraste, «sin convertirlo en falso». Eso se cumple para la acción y no para el objetivo. El objetivo de Viscofan (38,62 €) se presenta «condicionado a PM1.estructura y PM1.parametro», con el rango 36,88–41,81 y sin hipótesis no cubiertas, aunque la familia Λ no se ha calculado. Que un objetivo salga condicionado o emitido depende de un booleano que nada contrasta.

**Qué haría falta.** Extender el contrato a `material_para_objetivo`: admitir `null`, pedir su base (calculada, juicio económico o no determinada) y comprobar que no sea `false` «calculada» cuando un contraste aislado mueve el precio de Sí al redondeo declarado. Y decidir, sin umbral, cómo entra en `hipotesis_que_condicionan` un parámetro sin fundamento cuya materialidad para el objetivo no está determinada.

## R5 · La configuración auditada de Viscofan conserva cifras de la base «Caja» (importante)

**Hechos comprobados.**
- `viscofan/Viscofan/configuracion_economica.json`, campo `naturaleza` (material auditado; se repite en el informe): «P-M1: SR1 con la familia Θ porque su base es el exceso de capex sobre D&A OBSERVADO en 2021–2025 (40,813)…» y «La familia Λ no se declara: λ no se observa y, con las bases de Viscofan, SRF solo estaría definida hasta λ = 1,1413 (combinación no definida en esta configuración)».
- El perímetro activo del expediente es NIIF 16: exceso 64,923 y F_hist 81,084 (`resultados.json`, `dominios_perimetro.md`).
- 1,1413 = 1 + 56,974 ÷ 403,132, con el F_hist de «Caja». Con NIIF 16 la cota es 1 + 81,084 ÷ 403,132 = 1,2011. Lo dice el propio `viscofan/resultados/dominios_perimetro.md`: «La cota de la 4.12 (λ ≤ 1,1413 para SRF) era de la base Caja y no se traslada a la de NIIF 16».
- El registro ya recoge el aviso de la auditoría sobre el 40,813. El de la cota no consta.

**Consecuencia.** El §7 dice: «No se trasladará una cota numérica de la base antigua a otra base como si fuera evidencia económica». Aquí la cota antigua está en el material auditado y es, además, el motivo declarado para no declarar la familia Λ, que es la razón de que PM1.familia no tenga contraste (R4).

**Qué haría falta.** Corregir el texto de `naturaleza` (exceso 64,923 con NIIF 16; cota 1,2011, o quitarla). Es material auditado: el cambio retira la aprobación y pide auditoría nueva. Si no se corrige, declararlo como contradicción conocida en el informe de la entrega.

## R6 · El perímetro NIIF 16 no llega a la palanca S2C (importante; interpretación económica)

**Hechos comprobados.**
- La V6.4.1 cambia B55 y B58 de «Configuración V6.4» (`construir_v641_experimental.py`): las altas entran en D_hist, el exceso, F_hist, Rh, f, f_fija, el requisito anual y el terminal. Historia C53 (S2C marginal, Δventas ÷ Σ H31:L31) no cambia. La celda nueva B155 («S2C histórico de referencia con el perímetro») es informativa: ninguna fórmula la usa.
- Viscofan: C53 = 1,146 (base «Caja», 296,489) y B155 = 1,060 (base NIIF 16, 320,599); f = 320,599 ÷ (320,599 − 32,4615) = 1,1127.
- Las palancas S2C de la fase B (0,9 / 1,1 / 1,4) son las de la 4.12, reutilizadas, iguales a sus referencias mecánicas, que salen de C53 (`referencias_mecanicas.py`). `fase_b.json` justifica el NORMAL con «el S2C marginal de la década es 1,15 (C53)».
- El informe muestra «S2C histórico de referencia 1.06». La fase C no lo menciona (búsqueda en `fase_c.json`).

**Interpretación.** El factor f corrige el S2C histórico para quitarle la parte de reposición: ΔV ÷ (D − Rh) = (ΔV ÷ D) × f, con la **misma** D en los dos factores. En la activa de Viscofan, f usa la D de NIIF 16 y el S2C se eligió sobre la D de «Caja». El S2C efectivo de los años 1–10 queda en torno a un 8 % por encima del que resulta de llevar el perímetro a las dos piezas (320,599 ÷ 296,489 = 1,081), es decir, con menos inversión para crecer. El sentido probable es que el precio de Sí «NIIF 16» (38,62) esté algo alto frente a una propagación completa; el tamaño no se ha calculado (haría falta LibreOffice). La fase B cita también el crecimiento del capital invertido (fila 32, que sí incluye arrendamientos), así que el anclaje no es solo C53: por eso es interpretación y no hecho.

**Consecuencia.** El §7 pide propagar la alternativa a «D_hist, F_hist, Rh, f/f_fija, S2C, requisito anual y terminal». El S2C solo recibe una celda de lectura. La activa «NIIF 16 completo» mezcla perímetros en el producto S2C × f, sin declararlo en la fase C ni en los límites de la ficha. La justificación de la reutilización de la fase B («las palancas se eligen sin anticipar la configuración») es cierta, pero es justo lo que deja el S2C en la base anterior.

**Qué haría falta.** Declararlo como límite del caso NIIF 16 y, si se quiere resuelto, una variante con el S2C reexpresado sobre B155 (o una fase B que vea la referencia con el perímetro), con su efecto separado. No elegir por el valor.

## R7 · Viscofan: evidencia activa que contradice las entradas, y origen de N (importante)

**Hechos comprobados** (libros `Viscofan_v63_datos.xlsx` y `Viscofan_v63_evaluada.xlsx` del expediente final, hoja «Control maestro», leídos con openpyxl).
- Fila 42 (Análisis!C42, EV / EBITDA): G42 = «EV a 6-oct-2026 / deuda 30-jun-26 · EBITDA LTM jun-26»; M42 = «EV 2.766,6 = capitalización 2.444,4 + DFN…». Análisis!C42 = 9,9, calculado con esa capitalización. Las entradas activas son precio 54,70 del 3-nov-2026 (C37) y capitalización 2.487,7 (C41).
- D88 (lista de comprobación de períodos): «…C60 2020→25; precio 6-oct-26…».
- `rellenar_fase1_v63.py:52`: `FRESCAS` solo cubre C37, C41, C55 y C57. Las filas 42 y 88 vienen del libro base de la etapa 1 y nadie las reescribe.
- `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`, §3, dice de 45,479209: «la que usa el modelo desde la fase 1 de la etapa 1». Pero `viscofan/Viscofan/etapa1/Viscofan_evaluada.xlsx`, Análisis!C55 = 45,6 (C37 = 53,6; C41 = 2.444,4), y el texto de la etapa 1, conservado en `evidencias_sustituidas` y en el libro base (Control maestro M52), dice: «Acciones en circulación netas de autocartera a 30-jun-2026 = 45,60 mm (base actual, coherente con C41). No se usa la diluida media FY25 como principal por la anomalía NIC 33».
- El puente del motor B resta Historia C64 + C65 − C66 (Diagnóstico V6 C16 = 279,939), con saldos del 31-dic-2025 (Historia L22 = 304,075; L23 = 12,243).

**Consecuencia.**
- El §6 pide limpiar del Control maestro la evidencia activa que contradice las entradas. Quedan una fecha (6-oct-2026) y una cifra (2.444,4 = 53,60 × 45,6036), con un C42 calculado con ellas. No afectan al valor del motor B; sí a la afirmación del registro de que esos textos «desaparecen» (desaparecen de las cuatro filas frescas, no del libro).
- La N del modelo (media «diluida» de 2025) no viene de la etapa 1: la introdujo la fase 1 del pipeline V2 en sustitución de una cifra que la etapa 1 había elegido de forma expresa y que había descartado la diluida por la misma anomalía. La conciliación no lo dice, y eso es información pertinente para la decisión VISCOFAN-ACCIONES.

**Qué haría falta.** Corregir la frase de la conciliación y añadir el antecedente de la etapa 1. Para las filas 42 y 88: o se extiende la sustitución de evidencia a las celdas derivadas del precio y de N (C42 y la lista de períodos), o se declaran como evidencia heredada no actualizada. Cambiar el libro retira la aprobación.

## R8 · Las fichas de la 4.13 declaran la aptitud de uso de la 4.12 (menor)

**Hechos.** `ficha.py:35–45`: `APTITUD_V64` tiene `"version": "4.12"` y `"evaluacion": "informe integrado de la entrega 4.12 (…INFORME_INTEGRACION_4_12.md…)"`. Las tres `ficha.json` finales lo llevan así.

**Consecuencia.** Las salidas oficiales de la 4.13 citan como evaluación de aptitud un documento de otra entrega. Ojo al corregirlo: cambia el contenido de la ficha; una llamada a `ficha.py` sobre los expedientes ya cerrados produciría una ficha distinta y archivaría la aprobación (comprobado con el piloto de la 4.11, cuya ficha es de otra versión del código). Hoy los tres expedientes son idempotentes (ver «Qué está bien»).

**Qué haría falta.** Decidir antes de empaquetar: o se actualiza la constante y se cierran de nuevo los tres expedientes, o se deja y se declara.

## R9 · Ámbito de las pruebas (menor)

**Hechos.**
- El registro sitúa el grupo E (pruebas de tipos) entre las 11:55 y las 12:02. Después se editaron archivos que ese grupo prueba: `cierre_v2.py` (12:29), `seleccion_plantilla.py` (12:34), `configuracion_economica.py` (12:38), `pipeline.py` y `ficha.py` (12:45) e `informe.py` (12:47). El último resultado guardado (`pruebas/_v64/resultados_integracion_v64.json`, 13:15) solo tiene C, G y H (52). `test_integracion_v64.py` se modificó a las 13:16:01, después de ese resultado.
- El revisor ejecutó el grupo E con el código final, en su copia: **28 de 28 PASAN**.
- El registro dice «16 pruebas nuevas» en el grupo E; en el código son 15 (14 de `TIPOS_413` y una de estado y registro como lista).
- Ninguna prueba cubre R1 (JSON roto en el material con `ficha.py`), R2 (elementos del registro) ni R3 (`no_entregable` con objetivo).

**Consecuencia.** El registro no afirma una ronda completa (queda para el Hito 5) y es coherente con lo ejecutado, salvo el recuento. El informe final debería distinguir lo ejecutado con el código final de lo ejecutado antes.

## R10 · Alternativas de N calculadas sobre el libro de la 4.12 (menor)

**Hechos.** `resultados/alternativas_acciones_viscofan.md` dice «Reproducción del caso activo: sí (39,28770…)» y calcula sobre copias del libro evaluado de la 4.12 (perímetro «Caja»). La activa de la 4.13 es 38,616 (NIIF 16). El «E fijo» es 2.487,700, cuando 54,70 × 45,479209 = 2.487,713.

**Consecuencia.** Las diferencias relativas (≈ 1 %) siguen valiendo como orden de magnitud; los niveles de la tabla no son los del expediente final, y el documento no lo dice.

## R11 · Línea citada de las altas (menor)

**Hechos.** `resultados/conciliacion_arrendamientos_viscofan.md` cita `AR_2025.txt · 2373` y `CF_2021.txt · 2317` para las frases de altas; están en las líneas 2374 y 2318 (`grep -n "Additions to right-of-use"`). Las cifras leídas son correctas (6.494 y 6.419; 3.010 y 2.007). Las líneas de las tablas sí coinciden.

## R12 · `validar` acepta `Infinity` y `NaN` (menor)

**Hechos.** `configuracion_economica.validar`: `PM1.lambda = Infinity` pasa (`_num(x) and x >= 1`); `NaN` pasa en `cartera_anual`, `cartera_vnc` y `cartera_historica`. Probado con λ = Infinity en el piloto: las cuatro vías retiran la aprobación y el pipeline termina en `no_entregable` («no aplicable»). Resultado seguro, por una vía que no es la validación.

## R13 · `__pycache__` en el árbol (menor)

**Hechos.** Hay seis: `v6/scripts/`, `v6/v64_experimental/scripts/`, `v6/v641_experimental/scripts/`, `personaje_v2/scripts/`, `personaje_v2/pruebas/` y `…_4_13/scripts/` (este, de `replica_independiente_v641.py`, que declara que no deja `.pyc`). No están en el manifiesto de la 4.12. Hay que excluirlos del paquete.

## R14 · Variación conjunta necesaria y materialidad «calculada» (observación)

**Hechos.** `vinculados_necesarios` (`objetivo_v64.py:73–89`) liga PM1.estructura ↔ PM1.roic_terminal, N1.tipo → N1.escudo y N3.regla → N3.circulante más todos los PM1 activos cuando hay requisito o P0. Son los vínculos que impone `validar` (SR2 ↔ ROIC × f; R0 + P-M1 sin especificar); no se han visto ampliaciones para dar cobertura. «Sin requisito adicional» cuenta como contraste aislado de PM1.estructura porque solo cambia B36.

**Interpretación.** Con N3.regla, el contraste necesario (`activa_R0_sin_PM1`) cambia a la vez toda P-M1. Las fases C lo resuelven bien, por diferencia de dos pares calculados (−1,36 € en Vidrala; 0,00 en Viscofan). El contrato no lo exige: aceptaría «calculada» con la sola invariancia de la variante conjunta. Conviene decirlo en la guía.

## R15 · Campos de `cierre_vigente.json` que no se comprueban (observación)

**Hechos** (`out/fuzz_anidado.json`). Con `auditoria_sha256`, `solicitud`, `auditoria_fiel`, `estado_analisis` o `informe_sha256` cambiados a `null`, lista, texto u objeto, la aprobación sigue en pipeline, informe y resumen (con el estado del pipeline presente, la respuesta registrada manda). Con `informe_sha256` vacío deja de comprobarse que `informe.md` sea el registrado (`cierre_v2.py:711`). No es material auditado.

## R16 · `mismo_importe` y los medios céntimos (observación)

**Hechos.** `round(float(x), 2)` redondea el valor binario: un precio de Sí que termine en medio céntimo puede dar un céntimo menos que el redondeo a mano. El error iría del lado del rechazo (pide corrección), no de la aceptación. Con 56,018 y 38,616 no ocurre.

## R17 · `en_la_activa` en las lecturas sin umbral (observación)

**Hechos.** `dominios_v64.agrupar`: `en_la_activa` solo mira los avisos activos. El grupo `factor_de_reestimacion` de los tres expedientes sale con `en_la_activa: false` y, a la vez, «afecta: valor de la activa», porque la activa está entre sus lecturas.

## R18 · Fecha de un promedio (observación)

**Hechos.** `fase1_v63.json → acciones_diluidas.fecha = 2025-12-31` para una media ponderada del ejercicio. El campo `periodo` lo aclara.

---

## Respuestas breves a los puntos de atención

1. **§3.** Quedan lecturas anteriores a la vigencia en `ficha.py` (R1). Una alteración de tipo puede dejar la aprobación vigente en la primera llamada de `ficha.py` (`ficha.json` con `hashes` de otro tipo, R1) y, con dos alteraciones, en las cuatro vías (R2). El material intacto con la selección equivocada se sigue rechazando sin tocar nada (grupo E, ejecutado por el revisor).
2. **§4.** No se ha encontrado ninguna combinación contradictoria que la coherencia de la fase C acepte (23 combinaciones en `sonda_p2.py`; el contraejemplo externo con bloqueo se rechaza; sin protocolo, el pipeline no entrega). Una `decision` que no es un objeto da `AttributeError` en `coherencia_fase_c`; no se ha comprobado si el esquema la detiene siempre antes. Las transiciones legítimas siguen aceptadas (provisional comprar o descartar → final esperar condicionado). S-19, la compra en zona «caro» y el bloqueo con acción nula se conservan. Efecto no deseado: R3.
3. **§5.** Los vínculos necesarios son los de la configuración (R14). «No determinada» no se convierte en «no material» para la acción; para el objetivo, sí puede (R4). Los juicios económicos se presentan como juicio, con evidencia e inferencias, en las tres fases C. No hay umbral. No toda hipótesis va a D10 (lista vacía, `no_procede`, con esperar y con el bloqueo). Los avisos de las variantes llegan agrupados, con «afecta» y «conclusiones», a la fase C, a la ficha y al informe.
4. **§6.** Queda evidencia activa contradictoria fuera de las cuatro celdas frescas (R7) y en la configuración (R5). N se presenta con su concepto real en `fase1_v63.json`, `fase1_metadatos.json` y el Control maestro (filas 41 y 52). En la herencia de la fase A reutilizada (22 celdas) no se ha encontrado otro caso como C97 con una búsqueda de frases de ausencia contrastadas con el Control maestro; es una búsqueda, no una auditoría completa.
5. **§7.** El perímetro NIIF 16 es coherente con el puente, el NOPAT, el capital y los pagos, y no se ha visto doble cómputo (Historia fila 31 no contiene altas). La propagación al S2C es parcial (R6). La V6.4, sus expedientes y sus huellas se conservan. Se trasladó una cota de la base anterior en el texto de la configuración (R5). La réplica no importa nada de la plantilla ni lee fórmulas; su definición del perímetro es de la misma autoría que la plantilla.
6. **§8.** La condición de Q-ROIC1 es la de la 4.9 (`PRECISION_ROIC_4_9.md`, líneas 17 y 32–33). La lectura de r_op frente a la r personal es correcta y no cae en la contraria. La tabla de H y de la mezcla fijo/circulante cuadra con sus denominadores (530,0 = 251,2 + 278,8; 75,0 ÷ 530,0 = 14,2 %; 75,0 ÷ 251,2 = 29,9 %; 0,157 y 0,288 € por euro). Las fases C nuevas no eligen estructura y no se apoyan en las inferencias corregidas.
7. **Expedientes.** Estados y auditorías acordes al material (ver abajo). Ninguna aprobación antigua vigente ni reutilizada.

## Qué está bien (solo lo comprobado)

- **Preservación.** Los 3.796 archivos del manifiesto de la 4.12 existen; 23 cambian, todos de código, esquemas, prompts o pruebas. La V6.4, su referencia y los expedientes anteriores conservan sus bytes.
- **Plantilla V6.4.1.** Reconstruida desde la V6.4 en la copia del revisor: mismo SHA-256 (`ad685573…`). Verificador: ÍNTEGRO, 0 fallos, en la plantilla y en los tres libros evaluados finales.
- **Huellas.** La huella económica de las configuraciones de la 4.11 y la 4.12, calculada con el código de la 4.13, es la guardada (`e9bf4676…`, `9161a3f5…`).
- **Expedientes finales.** En los tres, `motivo_vigencia` no da motivo; el material actual es el fijado; la auditoría es APROBADO según H2 y nombra su solicitud y su material; estados: `vidrala_condicionado` concluido · APROBADO (795e4ff5ad2ff161), `vidrala_bloqueo` pendiente_de_datos · APROBADO (8a3db1f6c7bdfb95), `viscofan` concluido · APROBADO (c76627e1181d2041). En copias aisladas, `ficha.py`, `informe.py` y `resumen.py` a mano no cambian ni un byte de la ficha, el informe, el estado, el cierre ni el CSV.
- **Aprobaciones antiguas.** Las de la 4.12 están archivadas en `historial_cierres/04_*`; sus auditorías, apartadas en `antecedentes/`, constan en `auditorias_conocidas.json` y no son la `auditoria.md` actual. La auditoría REPETIR de Viscofan está conservada.
- **§3, lo corregido.** Raíz nula, lista, número o texto en 18 archivos JSON (los 15 del material, más `ficha.json`, `cierre_vigente.json` y `material_auditoria.json`): en las 288 primeras llamadas (18 × 4 tipos × 4 vías) la aprobación se retira sin excepción. Registro de publicaciones roto o de otro tipo en la raíz: código 5 con la retirada pendiente visible en 20 de 20. Campos anidados de `configuracion_economica.json` (`lambda_rango` con un texto, `trazabilidad` como lista, `estructura` numérica, `N1.valor = NaN`): retirada en las cuatro vías. Grupo E: 28 de 28.
- **§4.** El contraejemplo externo se rechaza; objetivo distinto del precio de Sí a dos decimales (56,10) se rechaza y 56,018 se acepta.
- **Comparación 4.12 → 4.13.** Vidrala: misma valoración (56,018 y 60,697). Viscofan: la variante «Caja» da 39,2877008705, igual que la 4.12; la diferencia de la activa, −0,6715 €, es la del perímetro.
- **Aritmética de las conciliaciones.** Acciones: 46.500.000 − 506.601 = 45.993.399; el movimiento de autocartera de 2025 cuadra; BPA 3,50 y 3,52. Arrendamientos: altas 24,110 y amortización 27,051; las cifras leídas coinciden con el texto.
