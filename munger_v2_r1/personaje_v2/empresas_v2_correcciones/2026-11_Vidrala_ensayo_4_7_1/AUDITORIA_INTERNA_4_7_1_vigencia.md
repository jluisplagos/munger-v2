# Auditoría interna de Claude · control de vigencia de la entrega 4.7.1

Es un control de vigencia acotado, no una auditoría completa. Lo hace **el mismo auditor** que la auditoría interna (`AUDITORIA_INTERNA_4_7_1.md`): Claude, con un contexto separado del de la persona que preparó la entrega.

**No es independiente de esa auditoría**, porque revisa las correcciones de sus propios hallazgos. Tampoco es una revisión externa.

Se distinguen:
- **hechos comprobados por el auditor**, reproducidos con comandos o guiones propios;
- **interpretaciones**;
- **propuestas**.

Las propuestas no cambian criterios financieros, probabilidades, r, k, escenarios ni conclusiones. Las decisiones son de la persona responsable.

## Material auditado

- **Lista de huellas:** `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7_1/MATERIAL_VIGENCIA_4_7_1.txt`. SHA-256 `7863eb9188320e75969d14b5c954c2d9b431175b9666f5c73c9ee547ded88634`, 47 archivos.
- **`grep -v '^#' MATERIAL_VIGENCIA_4_7_1.txt | sha256sum -c` desde `munger_v2_r1/`:**
  - al principio (10-nov-2026, 10:58 UTC): **47 de 47 OK**;
  - al final (11:17 UTC): **47 de 47 OK**.
- **Estado del árbol real:**
  - El auditor tomó al principio las huellas de sus 1.452 archivos. Antes de escribir este informe comprobó que no había cambiado ninguno.
  - El informe anterior (`AUDITORIA_INTERNA_4_7_1.md`, `51748dcb…`) es idéntico al que escribió el auditor.
  - Respecto al árbol de la auditoría, solo cambian los archivos que declara el cierre técnico §5–§6. `analisis_n1_n3.py` y las salidas de `financiero/` no cambian, salvo `decisiones_propuestas_N1_N3.json`.
- **Copias de código:** `reproduccion/codigo_4_7/` coincide con el código del manifiesto 4.7. `reproduccion/codigo_auditado_4_7_1/` coincide con las huellas del primer cierre (`f7f28186…`, `62ac0c4e…`, `8e289606…`).
- **Dónde se ejecutó:** solo en copias nuevas del scratchpad, con `PYTHONDONTWRITEBYTECODE=1` y `-B`/`-I`:

  | Copia | Contenido |
  |---|---|
  | `aud471v` | código actual |
  | `aud471v_c47` | árbol actual con `cierre_v2.py`, `ficha.py`, `resumen.py` y `pipeline.py` de la 4.7 |
  | `aud471v_aud` | árbol actual con el código que vio la auditoría, más `pipeline.py` de la 4.7, que entonces no había cambiado |
  | `aud471v_ver` | copia limpia para el verificador |
  | `aud471v_mutF/*` | mutaciones |
  | `aud471v_cfg` | cambio de versión de la configuración |
  | `*_sch` | esquema roto a propósito |

  Los guiones del auditor están en `…/scratchpad/aud471_pruebas/` (`w1_variantes.py`, `w1_vigencia.py`, `mutaciones.py`). Las salidas, en `…/scratchpad/aud471v_out/`.
- **Escritura en el árbol:** el auditor no modificó nada del árbol real. Este informe es lo único que escribe en él.

## Qué se ejecutó

| Comando (en copias) | Resultado |
|---|---|
| `test_resumen_v2.py`, código actual | **45/45** |
| La misma batería con el código 4.7 | **35/45**. Fallan las 3 de W-1 y 7 de las 8 nuevas; pasa la 29, de conservación |
| La misma batería con el código auditado | **36/45**. Fallan la 23 (W-g), la 25 (aviso de W-d) y las 26a, 26b, 27, 28, 30, 31 y 32 |
| Siete mutaciones del código actual (`mutaciones.py`), cada una con la batería | Cada mutación hace fallar al menos una prueba (detalle en «Comprobaciones sin hallazgo») |
| `bash verificar_paquete.sh completa`, copia limpia, 7 min 10 s | Pasan entorno, piloto, comprobadores 114/114, sintético 30/30, nombres de la línea de base, resumen 45/45 y cierre 55/55. **Falla el manifiesto**: sigue siendo el de la 4.7 (C-c). Global: FALLA (1 bloque) |
| `comprobar_entrega_4_7_1.py` | **41 de 44**. Ver X-f |
| `w1_variantes.py` S1–S16, código actual, comparado con la salida del código auditado | W-a, W-b y W-e a W-g, resueltos (detalle abajo) |
| `w1_vigencia.py` V1–V4, con los tres códigos | V1: `terminar()`. V2: ejecución normal, sustitución en el pipeline e historial. V3: W-f con una publicación vigente legítima. V4: fechas, V-2 y empresa |
| `pipeline.py --desde 2` sin `fase1_v63.json` ni `texto/` (actual y auditado) | Ver X-a |
| `pipeline.py --desde 14` con `version_config` 0.2.2 → 0.2.3 | Ver X-b |
| `pipeline.py --desde 14` con el esquema de la ficha roto a propósito (actual y auditado) | Ver X-c |
| Cotejo de las cifras nuevas del N3 con `CF_2025.txt` y con la Historia | Ver N-b y X-e |

## Estado de los hallazgos de la auditoría

| Id | Gravedad en la auditoría | Estado |
|---|---|---|
| W-a | bloqueante | **Resuelto** |
| W-b | menor | **Resuelto** |
| W-c | importante | **Resuelto** |
| W-d | menor | **Resuelto como se documenta** |
| W-e | importante | **Resuelto**, con efectos nuevos (X-a, X-b, X-c) |
| W-f | menor | **Resuelto** |
| W-g | menor | **Resuelto** |
| N-a | menor | **Resuelto** |
| N-b | menor | **Resuelto en lo sustancial** (precisión en X-e) |
| N-c | menor | **Resuelto** |
| C-a | menor | **Resuelto** |
| C-b | menor | **Resuelto** |
| C-c | menor | **Pendiente**, declarado: es del empaquetado |

**W-a · bloqueante → resuelto.** Con el código actual (hecho comprobado):
- **Ruta de W-1 (S7, S8 y S14):** se retiran en la primera llamada:
  - las filas reescritas, con `87.90`, `65.6880873204157` (lo que deja LibreOffice) o coma decimal;
  - la ficha editada tras el cierre en un expediente sin archivo previo.
- **Pipeline configurado (S15):** se retira en la primera llamada, con código 4.
- **`resumen.py` sin ficha (S13):** se retira el destino recibido.
- **Fila de la ficha vigente:** se conserva (S5 y prueba 29, con «11/03/26» y los números de la hoja), igual que la fila idéntica de otra empresa (S6) y la de otra fecha (21b y V4).

**W-b · menor → resuelto.** S4 y prueba 30: con el registro ilegible, la ruta de W-1 devuelve 5, retira el predeterminado y no toca el registro.

**W-c · importante → resuelto.**
- Las pruebas 23 y 24 comprueban de inmediato:
  - las dos filas y los dos historiales;
  - el archivo de las salidas;
  - `estado_pipeline` (sin cierre, sin aprobación y con `cierres_archivados` = número de carpetas);
  - el registro, con el material, y el reintento.
- Las pruebas 26–32 cubren W-a (cuatro variantes y la conservación), W-b, W-f y W-e.
- Todas son sustantivas: cada corrección hace fallar al menos una prueba cuando se revierte (mutaciones). Las afirmaciones del cierre técnico sobre 45, 35 y 36 coinciden con las ejecuciones.

**W-d · menor → resuelto como se documenta.**
- `ficha.py` devuelve 0 con «AVISO: … la ficha nueva NO es vigente…» (S9).
- El Anexo D documenta el 0 y el 4 dentro del pipeline.
- El cambio de código sigue siendo decisión de la persona responsable.

**W-e · importante → resuelto.** S16 y prueba 32, sustitución dentro del pipeline:
- código 4, «CIERRE RECHAZADO», sin «FIN · estado concluido»;
- sin ficha ni informe;
- `estado_pipeline` con `None`/`None`/paso 13 y `cierres_archivados` = 3 = carpetas;
- filas retiradas.

Efectos nuevos de la corrección: X-a, X-b y X-c.

**W-f · menor → resuelto.**
- S12 y prueba 31: la fila restaurada en un destino registrado como «retirada» se vuelve a retirar.
- V3a: una publicación vigente registrada en el predeterminado **no** se vuelve a retirar en cinco llamadas: `resumen.py` al predeterminado y a otro destino, `informe.py`, `ficha.py` y el pipeline. Todas devuelven 0 y el historial no cambia (1 → 1).

**W-g · menor → resuelto.**
- La fila retirada dice «APROBADO del material 74b94f8072dd58c1». El historial y el registro llevan el material.
- Interpretación: según el código, si hay varias fichas archivadas con la misma fecha, se nombra la más reciente, que puede no ser la que publicó la fila. Solo afecta a la trazabilidad.

**N-a · menor → resuelto.**
- Se retira «Es inversión de renovación, no de ampliación». Queda «*sobre todo* (primarily): no excluye…».
- La vida útil de 8–16 años se presenta como contable, no como duración de una campaña, también en el §4.
- La interpretación se marca como tal.

**N-b · menor → resuelto en lo sustancial.**
- Hay «**Límites en el otro sentido**»:
  - 7,913 de amortización de intangibles en 2025, de los que 4,492 son de cartera de clientes (p. 46, comprobado);
  - el salto de perímetro de 87,21 a 117,72 y 132,948;
  - 2020 con Italia.
- El §6 y D-N3b dicen que «=D&A» es la opción de mayor valor.
- Queda una precisión (X-e).

**N-c · menor → resuelto.**
- «Qué sustituye» nombra la viñeta «Necesidades de caja» del §4.2 y la frase del §6.
- Declara vigente el resto del §4.2, incluidas las cifras de circulante y la advertencia sobre el terminal.

**C-a · menor → resuelto.**
- El control reejecuta la batería del resumen en copias con los tres códigos (`ejecutar_baterias_4_7_1.py --solo-comprobar`). Compara huellas, estado de cada prueba y línea final.
- Ejecuta la conservación y una variante de W-a.
- Calcula los niveles desde la evidencia.
- Las salidas de cierre y del sintético siguen siendo [constata], pero llevan en su cabecera las huellas del código y `verificar_paquete.sh completa` las reejecuta.

**C-b · menor → resuelto.** La cabecera del control de integración habla de la batería del resumen con mínimo 45: 13 de 13.

**C-c · menor → pendiente (declarado).**
- `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` siguen siendo los de la 4.7, y `REGISTRO_ENTREGA_4.7.1.md` no existe.
- El verificador falla en el bloque del manifiesto, con 8 modificados y los archivos nuevos.
- El control lo señala (2 de sus 3 incumplimientos). Hay que resolverlo antes de entregar.

## Hallazgos nuevos

### X-a · menor · `adoptar_archivo` borra el estado final de una terminación no cerrada

**Hecho comprobado por el auditor.** Escenario: una copia aprobada, sin `fase1_v63.json` ni `texto/` (fuera del material), ejecutada con `pipeline.py --desde 2`.

| | Código actual | Código auditado |
|---|---|---|
| Mensaje final | «FIN · estado pendiente_de_datos», seguido de **«estado final: None · paso 2»** | «estado final: pendiente_de_datos» |
| Código de salida | 0 | 0 |
| `estado_pipeline.json` | `estado_analisis` `None`, `auditoria` `None`, 2 cierres archivados | `estado_analisis` `pendiente_de_datos`, `auditoria` `APROBADO` caducada (persiste tras la segunda ejecución), 1 cierre (un archivo sin registrar) |
| `ficha.json` y fila del resumen | `pendiente_de_datos` | `pendiente_de_datos` |

- Con el código actual, la segunda ejecución deja `pendiente_de_datos`.
- Lo mismo se reproduce llamando a `Pipeline.terminar()` directamente (V1).

**Interpretación.**
- `archivar_salidas` pone a `None` el estado del disco al archivar la ficha cerrada anterior, y `adoptar_archivo` copia ese `None` encima del estado que la propia `terminar()` acababa de fijar.
- Es mejor que antes en lo que importa: no queda ninguna aprobación caducada. Pero el pipeline termina con un estado incoherente con la ficha durante una ejecución.

**Propuesta.** Al adoptar, conservar el `estado_analisis` no cerrado que fijó `terminar()`, o volver a fijarlo después; adoptar solo la auditoría, el paso y los cierres. Añadir una prueba con el escenario de arriba.

### X-b · menor · Rehacer el paso 14 de un expediente aprobado exige ya una auditoría nueva si la ficha cambia, aunque solo sea por un metadato

**Hecho comprobado por el auditor.** En una copia con `version_config` 0.2.2 → 0.2.3 en `config_v2.json`, sin tocar nada del material:
- `pipeline.py --desde 14` sobre el expediente aprobado archiva la ficha y el informe (`02` y `03`) y termina con código 4.
- El relanzamiento sin `--desde` queda esperando una auditoría (código 10, V2d).

Con el código auditado, el pipeline volvía a cerrar, con el estado sobrescrito que motivó W-e.

**Interpretación.**
- Es la aplicación coherente de la regla de la 4.6.1: una ficha cerrada no se sustituye en silencio. Además, el material auditado incluye `ficha_provisional.json`, con sus versiones.
- Pero la consecuencia no está declarada: la próxima entrega que suba una versión de la configuración obligará a reauditar cada expediente aprobado que se relance.
- Es el sentido conservador.

**Propuesta.** Declararlo en el Anexo D y que la persona responsable decida si las diferencias solo de metadatos (`versiones`) deben contar como sustitución.

### X-c · menor · El fallo de esquema en el paso 14 termina ahora en un estado mixto

**Hecho comprobado por el auditor.** Con `esquema/ficha.esquema.json` roto a propósito (un campo obligatorio inexistente) y `--desde 14`:

| | Código actual | Código auditado |
|---|---|---|
| Código de salida | **4**: «CIERRE RECHAZADO» con el motivo de `informe.py` («auditoria = None»), que no es la causa | 0 |
| `estado_pipeline.json` | `no_entregable`, paso **13** | `no_entregable`/`APROBADO` |
| `ficha.json` | ninguna: la `no_entregable` también se archiva | `no_entregable` **con `cierre`** |
| Fila del resumen | retirada | «no_entregable / APROBADO» |

**Interpretación.**
- La causa es anterior a la 4.7.1: `ficha.py` pone `cierre` siempre que `paso == 14`, sea cual sea el estado.
- Lo actual es conservador, mejor que publicar «no_entregable / APROBADO». Pero el mensaje y el estado son incoherentes: dice que «vuelve al paso 13» y conserva `no_entregable`.
- Es una ruta de fallo de implementación, poco frecuente.

**Propuesta.** Escribir `cierre` solo cuando el estado lo admite, distinguir el fallo de esquema en la comprobación del paso 14 y añadir una prueba.

### X-d · menor · Márgenes de la detección por fecha y de la exclusión

**Hecho comprobado por el auditor (V3, V4).**
1. **Fecha ambigua.** Una fila de **otro** expediente de la misma empresa con «11/03/2026» (11 de marzo) se retira al invalidar este, cuya fecha es el 3 de noviembre, porque se admiten día/mes y mes/día.
   - Es el sentido conservador.
   - El Anexo D dice que «la regla V-2 protege así las filas de otros expedientes» y no menciona esta excepción.
2. **Formatos no leídos.** Con «3-Nov-26», «03-nov-2026» o «2026.11.03», la fila propia caducada no se retira.
   - Lo cubre el límite residual declarado («ya no se pueda leer como fecha»).
   - Pero el Anexo D afirma en general que la fecha «se lee también en los formatos que deja una hoja de cálculo».
3. **Fila vigente redondeada.** Con `65.69` o `70.50`, la exclusión falla y la fila se retira.
   - Con el pipeline por defecto se vuelve a publicar (V3b).
   - Con el resumen configurado en otro CSV, el predeterminado se queda «SIN APROBACIÓN VIGENTE» aunque la aprobación sea vigente (V3c).
   - El Anexo D dice que «`resumen.py` la vuelve a publicar», y eso solo ocurre si `resumen.py` escribe en ese CSV.
4. **Empresa en otra grafía.** Una fila con la empresa en mayúsculas no se reconoce. Es anterior a la 4.7.1.

**Interpretación.** Ninguno crea ni deja una aprobación indebida fuera del límite declarado: (1) y (3) retiran de más; (2) está declarado. Son precisiones de la documentación.

**Propuesta.** En el Anexo D:
- enumerar los formatos de fecha que se leen;
- mencionar la ambigüedad día/mes frente a V-2;
- matizar la nueva publicación.

### X-e · menor · Precisión de N-b y redacción

**Hecho comprobado por el auditor.**
- El informe da «en 2024, 4,768 de amortización de derechos de uso (nota del lector en la Historia, fila 8)». La cifra es correcta para 2024 (CF_2025, PDF p. 52, columna comparativa).
- Pero la amortización que usa la hipótesis es la de 2025, y en 2025 esa partida es **6,760** (misma página), en el texto conservado.
- En el §6, la «Advertencia explícita» repite dos veces la misma idea (que la sensibilidad del MALO acompañe siempre a R1).

**Propuesta.** Citar 6,760 de 2025 con su fuente primaria (además o en lugar de la de 2024) y quitar la repetición. No cambia ningún cálculo.

### X-f · menor · Recuento declarado del control

**Hecho comprobado por el auditor.**
- El encargo declara 40 de 44, con cuatro incumplimientos esperados, entre ellos «el material de ese control».
- Con el material ya fijado, el control da **41 de 44**. Solo fallan este informe, VERSION/CONTINUIDAD/PROMPT y el registro.
- La cabecera del control dice «unos 4 minutos»; en la copia tardó 1 min 13 s.

**Propuesta.** Actualizar la cifra declarada. No es un defecto del control.

## Comprobaciones sin hallazgo

- **Secuencia de §1 (S1) y reintentos:** igual que en la auditoría, y ahora con el material en la fila, el historial y el registro.
- **Variantes de la auditoría (S2, S3, S5, S6, S9–S11):** sin regresiones frente al código auditado.
- **Ejecución normal sin sustitución (V2a, V2b):** `--desde 14` con la configuración por defecto (dos veces) y con resumen configurado.
  - Código 0, concluido/APROBADO.
  - Sin archivos nuevos ni historial duplicado: los duplicados del historial son los mismos antes y después (17 → 17); en V2c no aumentan con la sustitución.
- **Falsos positivos de la detección por fecha.**
  - No se retira una fila legítima de la ficha vigente: ni idéntica (S5) ni reescrita por una hoja de cálculo (prueba 29, V3b con «03/11/2026»).
  - La exclusión exige los nueve campos de contenido dentro de la tolerancia y la fecha. Por eso ni la tolerancia de 10⁻⁶ ni la ambigüedad de fechas pueden conservar una fila que presente valores distintos de los de la ficha vigente (lectura del código y V3/V4). La salvedad es la de X-d (1 y 3), que retira de más.
- **Mutaciones**, todas detectadas por la batería:

  | Mutación | Resultado | Pruebas que fallan |
  |---|---|---|
  | Sin exclusión de la vigente | 41/45 | 29, 31 y dos de copia |
  | Sin tolerancia | 44/45 | 29 |
  | Solo fecha ISO | 42/45 | 26a, 27 y 28 |
  | Sin el rechazo del paso 14 | 44/45 | 32 |
  | Sin `adoptar_archivo` | 44/45 | 32 |
  | Sin W-f | 44/45 | 31 |
  | Detección por contenido con tolerancia | 44/45 | 26b |
- **N3.**
  - El control regenera byte a byte las 8 salidas.
  - `analisis_n1_n3.py`, la matriz, los CSV y la evidencia no han cambiado desde la auditoría.
  - D-N1 y D-N2 son iguales a la 4.7.
  - D-N3 y D-N3b siguen sin `decision`, `fecha` ni `confirmado_por`.
  - No cambia ninguna constante, probabilidad, r ni k. Se mantienen los avisos de no comparabilidad con 87,9 y de que no es una recomendación.
- **Integridad:** originales, la carpeta 4.7 y P1 intactos (control, apartado 1: 1.400 archivos, los 489 originales y la carpeta 4.7 completa).
- **`comprobar_entrega_4_7_1.py`**, versión nueva.
  - Es sustantivo: reejecuta tres baterías en copias con las huellas del código, una conservación y una variante de W-a; calcula los niveles desde la evidencia; y comprueba el veredicto de cada informe con el resultado esperado.
  - Sus 3 incumplimientos actuales corresponden a lo pendiente.

## Veredicto

**Sin hallazgos bloqueantes**. Todos los hallazgos de la auditoría interna, del W-a al C-b, quedan resueltos, comprobados con reproducciones propias y con pruebas que fallan cuando se revierte cada corrección. C-c (empaquetado) queda pendiente y declarado, y hay que completarlo antes de entregar.

Hay seis hallazgos nuevos menores. Los más útiles de atender:
- X-a: `adoptar_archivo` borra el estado de una terminación no cerrada durante una ejecución;
- X-b: relanzar el paso 14 de un expediente aprobado tras un cambio solo de metadatos exige una auditoría nueva, y no está declarado;
- X-c: el fallo de esquema en el paso 14 deja un estado mixto.

Los demás (X-d a X-f) son precisiones de documentación y de cifras. Ninguno crea ni deja publicada una aprobación indebida.
