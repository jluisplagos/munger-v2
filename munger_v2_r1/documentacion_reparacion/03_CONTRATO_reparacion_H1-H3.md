> **Nota de continuidad (8-nov-2026, entrega 3.1).** Este es el contrato de reparación tal como se cerró a las 15:30 aprox. Incorpora además la corrección de las rutas de H3 (precisión P3, de las 15:35): `observaciones.C25` y `seis_preguntas.que_caja_espero`. Las instrucciones posteriores de la persona responsable del proyecto, transcritas literalmente en `04_INSTRUCCIONES_POSTERIORES.md`, **prevalecen sobre él**. En particular:
> - **H2:** la regla «cualquier punto FALLA → REPETIR», adoptada por la persona responsable a las 15:12, ya figura en este contrato (casos 2, 7 y 8). Después se añadió el cierre de la vía de los encabezados inválidos (15:48).
> - **Precisiones P1, P2 y P4:** se añadieron después de este contrato; P3 ya está aplicada en esta copia.
> - **Cierre de H1:** se añadieron los casos de reutilización A, B y C.
> - **Lista cerrada de archivos:** se amplió, de forma declarada, con `rellenar_fase1_v63.py` y `comprobar_entrada_v63.py`.
>
> El estado vigente está en `../CONTINUIDAD.md` y en `../REGISTRO_IMPLEMENTACION_H1-H3.md`.

# Munger v2 · Contrato de reparación H1–H3

Fecha: 8-nov-2026 (rutas de H3 corregidas el mismo día: `observaciones.C25`, `seis_preguntas.que_caja_espero`). Este documento fija los criterios de aceptación y la lista cerrada de archivos de la reparación. **No se ha cambiado nada del sistema**. Las columnas «Hoy» recogen resultados ejecutados con el código actual: `resultados/h1_*.json` y `resultados/h2_*.json` del paquete de diagnóstico.

**Orden de implementación: H2 → H1 → H3.** H3 necesita una auditoría nueva, que ya debe leerse con la regla de H2. H1 no interfiere con H3, porque H3 no vuelve a ejecutar la fase 1.

## 1. H1 · Comprobación de extracciones

**Reglas que se implementan**
- **R-a.** La `linea`, una vez normalizada, tiene que estar en la página citada. Se elimina la vía alternativa (líneas 119–122 de `fase1_historia.py`).
- **R-b.** El `impreso` tiene que figurar como importe completo, tanto en la línea como en la página. No basta con que aparezca dentro de otro número: tras normalizar, debe cumplirse el patrón `(?<![\d.,])IMPORTE(?![\d.,]*\d)`.
- **R-c.** Un `cero` sin `cita`, o cuya `cita` no aparezca literalmente en la página citada, se **rechaza**. Un `cero` cuya `cita` sí aparece queda **PENDIENTE**: nunca se da por comprobado.

**Tres resultados posibles:**
- **ACEPTADO:** sin errores y sin pendientes.
- **PENDIENTE:** sin errores, pero con uno o más ceros pendientes de verificación.
- **RECHAZADO:** con errores.

El control automático no distingue el caso 12 del caso 13. Comprueba que la cita existe en la página, pero no que se refiera a la partida. Por eso los dos acaban en PENDIENTE.

| Caso | Entrada | Hoy | Tras la reparación | Regla |
|---|---|---|---|---|
| 1 | Página «Revenue 123»; capex 123 con la línea «Capital expenditure 123», que no existe | ACEPTADO | **RECHAZADO** | R-a |
| 2 | capex con la línea real «Revenue 123», de otra partida | ACEPTADO | ACEPTADO · limitación conocida L1 (concepto) | — |
| 3 | «123» dentro de «91234», con línea inexistente | ACEPTADO | **RECHAZADO** | R-a |
| 3b *(nuevo, ajuste A1)* | Línea real «Capital expenditure 91234»; impreso «123» | ACEPTADO | **RECHAZADO** | R-b |
| 4 | Cifra del ejercicio anterior declarada como actual | ACEPTADO | ACEPTADO · limitación conocida L2 (columna) | — |
| 5 | Página en miles declarada en millones | ACEPTADO | ACEPTADO · limitación conocida L3 (unidad) | — |
| 6 | Cobro con el signo invertido | ACEPTADO | ACEPTADO · limitación conocida L4 (signo) | — |
| 7 | `cero` sin `cita`, con una página que no menciona la partida | ACEPTADO | **RECHAZADO** | R-c |
| 7b *(nuevo, ajuste A1)* | `cero` con una `cita` que no está en la página | ACEPTADO | **RECHAZADO** | R-c |
| 8 | Número ausente de la página | RECHAZADO | RECHAZADO | — |
| 9 | Página inexistente | RECHAZADO | RECHAZADO | — |
| 10 | Línea y número presentes | ACEPTADO | ACEPTADO | — |
| 11 | `cero` con página inexistente | RECHAZADO | RECHAZADO | — |
| 12 *(nuevo)* | Cero de SBC con la cita «The Group has no share-based payment programmes», presente en la página | ACEPTADO | **PENDIENTE** | R-c |
| 13 *(nuevo)* | Cero de SBC con una cita auténtica sobre pensiones, presente en la página | ACEPTADO | **PENDIENTE**, igual que el 12 | R-c |

**Condiciones adicionales de aceptación de H1**
- En los casos 12 y 13 el valor se conserva como 0. El cero aparece en una sección de `historia_revision.md` que deja de llamarse «Ceros con evidencia» y pasa a llamarse «Ceros pendientes de verificación (cita sin contrastar)». La fuente de esa partida en la Historia incluye «cero pendiente de verificación».
- La orden `comprobar-anio` termina con código 0 e imprime una línea `PENDIENTE` por cada cero. `preparar` no vuelve a pedir el año por tener ceros pendientes: solo lo pide cuando hay errores.
- Un cero solo pasa a considerarse comprobado mediante una decisión humana registrada en `fase1_decisiones.json`, con el valor 0, la fuente y la fecha. Ese mecanismo ya existe en el sistema.

**Ceros existentes.** Hay 134 ceros en cinco expedientes (Aarsleff 21, Hermès 16, Nike 40, Vidrala 39, Viscofan 18; Rational 0). Ninguno lleva `cita`.
- Se conservan sin cambios en los expedientes originales, con los mismos valores en la Historia.
- `preparar` y `construir` no se vuelven a ejecutar sobre esos expedientes. Si se hiciera, R-c los rechazaría y `preparar` volvería a pedir la extracción de esos años.
- Se registran en un inventario nuevo, cada uno con la marca «pendiente de verificación (heredado, sin cita)».

**Revisión de rechazos reales, cuando haya documentos (texto/ o PDF)**
1. Se trabaja sobre una copia del expediente, con `texto/` añadido.
2. Se ejecuta `fase1_historia.py comprobar-anio <copia> <año>` para cada año. Es solo lectura. Nunca se usa `preparar`.
3. Cada rechazo se clasifica en uno de tres tipos:
   - **A, respaldo mal atribuido con cifra correcta:** se corrige `linea` o `cita` en una versión nueva de `AR_<año>.json`, sin tocar el valor.
   - **B, cifra incorrecta:** se fija con fuente en `fase1_decisiones.json` y se abre la evaluación de sus consecuencias en un expediente nuevo.
   - **C, no resoluble:** la cifra pasa a `null`, es decir, a desconocido, nunca a 0.
4. Cada cero heredado lo revisa una persona sobre la página citada: o se añade la `cita` y se registra la decisión, o se aplica el tipo C.
5. Solo se vuelve a extraer la partida y el año afectados, nunca el año completo.
6. Se ejecuta `construir` en la versión nueva, y la Historia debe salir idéntica salvo los cambios de tipo B y C.

## 2. H2 · Lectura de auditorías

**Regla.**
- Un punto es una línea con el formato `N. PASA` o `N. FALLA`, con marcas de markdown opcionales al principio, como admite el lector actual.
- Una auditoría es válida si cumple todas estas condiciones:
  - contiene los puntos 1 a 16, una sola vez cada uno;
  - no contiene puntos fuera de ese rango;
  - tiene una sola línea de veredicto, que dice exactamente APROBADO o REPETIR.
- **APROBADO** exige una auditoría válida, los 16 puntos con PASA y el veredicto escrito APROBADO. En cualquier otro caso, REPETIR.
- Si la palabra FALLA aparece en el texto de un punto que está en PASA, también da REPETIR. Es la interpretación prudente que ya aplican el código y el prompt actuales (ajuste A2).

| Caso | Entrada | Hoy | Tras la reparación |
|---|---|---|---|
| 1 | Solo «Veredicto: APROBADO» | APROBADO | **REPETIR** |
| 2 | «8. FALLA · hecho material inventado» + APROBADO | APROBADO | **REPETIR** |
| 3a / 3b / 3c | FALLA en el punto 1, 11 o 16 + APROBADO | REPETIR | REPETIR |
| 4 / 5 / 6 | Texto vacío · «APROBADO con reservas» · dos veredictos | REPETIR | REPETIR |
| 7 | 16 puntos, FALLA en el 8, APROBADO | APROBADO | **REPETIR** |
| 8 | 16 puntos, FALLA en los 11 puntos no bloqueantes, APROBADO | APROBADO | **REPETIR** |
| 9 | 16 puntos, todos PASA, APROBADO | APROBADO | APROBADO |
| 10 *(nuevo)* | 16 puntos con el 5 duplicado | APROBADO | **REPETIR** |
| 11 *(nuevo)* | 15 puntos: falta el 12 | APROBADO | **REPETIR** |
| 12 *(nuevo)* | 16 puntos, todos PASA, veredicto REPETIR | REPETIR | REPETIR |
| 13 *(nuevo)* | 16 puntos PASA; el 7 incluye «Aviso: …» | APROBADO | APROBADO |
| 14 *(nuevo)* | 16 puntos PASA; el 6 contiene la palabra «FALLA» en su texto | APROBADO | **REPETIR** (A2) |
| Reales (6) | Auditorías de Aarsleff, Hermès, Nike, Rational, Vidrala y Viscofan | APROBADO | APROBADO, con SHA-256 idéntico antes y después |

**Condiciones adicionales de aceptación de H2**
- `test_pipeline_sintetico.py` da **30/30** con el generador actualizado. Los nombres de las 30 comprobaciones son los mismos antes y después. Los casos nuevos van en un archivo de pruebas aparte, sin quitar ninguno de los existentes.
- La regla aparece con las mismas palabras en el código, en `prompts/verificacion.md`, en el Anexo D §D.9, en `DECISIONES.md` y en `ESTADO.md`. La búsqueda de «FALLA en 1, 4, 11, 12 o 16» como **única** condición de REPETIR no devuelve ningún resultado.
- El prompt indica que una observación no bloqueante se escribe como «PASA … Aviso: …» y que cualquier FALLA obliga a escribir «Veredicto: REPETIR».

## 3. H3 · Corrección de Aarsleff

**Ubicación del expediente nuevo:** `personaje_v2/empresas_v2_correcciones/2026-11_H3/Aarsleff/`. El original no se toca.

**Correcciones de texto (las cinco, literales)**

| Archivo de origen | Campo | Cambio |
|---|---|---|
| `fase_a.json` | `observaciones.C25` (`celdas.C25` permanece en «No») | «cuatro años negativos de diez» → «cinco años negativos de diez» |
| `fase_a.json` | `herencia.C25.evidencia_y_razonamiento` | El mismo cambio |
| `fase_a.json` | `seis_preguntas.que_caja_espero` | «con cuatro años negativos» → «con cinco años negativos» |
| `fase_a.md` | Líneas 49 y 99 | «Cuatro años negativos de diez» y «con cuatro años negativos» → «Cinco…» y «cinco…» |
| `fase_c.json` | `celdas.B102` | «con cuatro años negativos» → «con cinco años negativos» |

**Regeneración.** Se usa el modo de agentes simulados que ya tiene el pipeline: `pipeline.py <nuevo> --agentes-simulados <DIR> --reiniciar`. Ese DIR contiene las salidas originales de los agentes:
- `extracto_v63.md` y `fase_b.json`, sin cambios;
- `fase_a.json` corregido;
- `fase_c.json` corregido, copiado como `fase_c.turno1.json` y como `fase_c.turno2.json`;
- **sin `auditoria.md`**, para que el pipeline se detenga en el paso 13 y pida una auditoría nueva.

`fase_a.md`, `fase_b.md` y `fase_c.md` se colocan a mano en la carpeta nueva, `fase_a.md` ya corregido. `etapa1/` y los archivos `fase1_*`, incluidos `fase1_v63.json` y `fase1_partes/`, se copian sin cambios byte a byte. La fase 1 no se vuelve a ejecutar.

**Criterios de aceptación de H3**
1. **Sin restos de la afirmación.** En los textos y en las celdas del Excel del expediente nuevo, estas dos búsquedas no devuelven nada:
   - `(?i)\b(cuatro|4|four)\s+(años|ejercicios|years)\b[^.;]{0,60}negativ`
   - `(?i)negativ[^.;]{0,40}\b(cuatro|4)\s+(de|en)\s+(diez|10)\b`

   Quedan **excluidos y deben conservarse**:
   - «Cuatro de cinco años planos o negativos» y «cuatro planos o negativos», que se refieren al crecimiento del escenario MALO (Palancas!B14 y `fase_b`);
   - los textos heredados de la etapa 1 en `datos_v63.md`: «tres años negativos en once» y «FCF negativo en FY20/21–21/22». Usan otra definición de FCF y son copia literal de la etapa anterior.
2. **Propagación completa.** Para cada archivo, el número de apariciones de «cinco años negativos» en el expediente nuevo es igual al de «cuatro años negativos» en el original: 27 apariciones en 13 archivos, incluidas `Análisis!B102` y `Control maestro!N30`.
3. **Controles aprobados.**
   - `verificar_todo.sh`: PASS (integridad ÍNTEGRO, celdas PASS, gramática con código 0, citas PASS, estado del libro LISTO · PROVISIONAL, caché ÍNTEGRO).
   - `comprobar_celdas_v2.py`: PASS con 64 celdas.
   - `validar_esquema.py` de la ficha: VÁLIDO.
   - Auditoría nueva: APROBADO según la regla de H2.
4. **Comparación anterior/posterior completa,** con un informe de diferencias escrito por un script:
   - En el Excel se comparan todas las hojas y todas las celdas, tanto valores recalculados como fórmulas. Las únicas diferencias de contenido admitidas son `Análisis!B102` y `Control maestro!N30`.
   - En los JSON y en el Markdown, las únicas diferencias de contenido admitidas son el cambio de «cuatro» por «cinco» en las frases de la serie y la auditoría nueva.
5. **Contenido que se conserva sin cambios:**
   - las filas 5–35 de la Historia, con sus valores y fórmulas;
   - `fase1_v63.json`;
   - B65:D69, la hoja Palancas, C46–C56 y todas las hipótesis numéricas;
   - `precio.json`: precio de Sí 450,5719, ponderado 502,3637 y escenario MALO 346,988;
   - las cifras de `resultados.json`;
   - `Análisis!D4`, la fecha de la ficha y las fechas de las predicciones;
   - cubo Vigilar y acción esperar;
   - **C25 = No**.
6. **Diferencias técnicas.** Se aceptan y se declaran como técnicas, no como cambios de contenido:
   - marcas de tiempo, rutas absolutas, `historial` y `consumidos` de `estado_pipeline.json`, y las anotaciones «agente simulado»;
   - metadatos del ZIP del xlsx (docProps y orden interno) y los hashes que dependen de ellos;
   - las carpetas `recalc/` y del perfil de LibreOffice;
   - rutas y fechas en `verificacion_*.txt`;
   - `prompts_generados/13_verificacion.md`;
   - diferencias numéricas de 1e-9 o menos, si aparecieran tras el recálculo.

   Cualquier otra diferencia es un cambio de contenido y la entrega no se acepta.
7. **Original intacto.** El manifiesto SHA-256 de `empresas_v2/` (las seis carpetas y `resumen_v2.csv`) es idéntico antes y después.
8. **Registro.** `CORRECCION_H3.md`, dentro del expediente nuevo, recoge las cinco correcciones con su texto anterior y posterior, el motivo y la referencia al diagnóstico.

## 4. Lista cerrada de archivos

### Alcance obligatorio

| # | Archivo | Cambio previsto | Motivo | Prueba que lo valida |
|---|---|---|---|---|
| 1 | `personaje_v2/scripts/fase1_historia.py` | `comprobar_anio`: R-a, R-b y R-c, y un parámetro opcional `pendientes` (lista) que recoge los ceros pendientes, sin cambiar lo que devuelve a quienes la llaman. `construir`: la sección pasa a llamarse «Ceros pendientes de verificación» y la fuente de la partida queda marcada. Orden `comprobar-anio`: imprime los pendientes y termina con código 0 | H1 | Casos H1 1–13, incluidos 3b y 7b |
| 2 | `personaje_v2/scripts/pipeline.py` | `veredicto_auditoria` con la regla de H2, y su docstring | H2 | Casos H2 1–14 y las 6 auditorías reales |
| 3 | `personaje_v2/pruebas/agentes_sinteticos.py` | `auditoria()` escribe 16 puntos. La variante REPETIR lleva FALLA en el punto 1 y «Veredicto: REPETIR» | H2: la versión actual, de un solo punto, depende del fallo | `test_pipeline_sintetico.py` 30/30, con los mismos nombres de comprobación |
| 4 | `personaje_v2/pruebas/test_comprobadores.py` *(nuevo)* | Los casos H1 y H2 de este contrato. Las auditorías reales se leen sin modificarlas | H1 y H2 | Termina con código 0; SHA-256 de las auditorías reales sin cambios |
| 5 | `personaje_v2/prompts/historia_anio.md` | `cita` obligatoria en cada `cero`. Describir exactamente lo que comprueba el script y retirar la afirmación de la línea 53. Explicar que un cero con cita queda pendiente | H1 | Los casos 12 y 13 usan el formato del ejemplo del prompt; revisión de texto |
| 6 | `personaje_v2/prompts/verificacion.md` | Sección «Veredicto»: cualquier FALLA obliga a REPETIR; una observación no bloqueante se escribe como «PASA … Aviso: …» | H2 | Casos 13 y 14; búsqueda de la regla antigua |
| 7 | `personaje_v2/ANEXO_D_salidas_y_formatos.md` | §D.9, última frase: la misma regla | H2 | Búsqueda de la regla antigua |
| 8 | `personaje_v2/DECISIONES.md` | Entradas fechadas: regla de auditoría (sustituye a la del 2-nov) y ceros pendientes | H1 y H2 | Revisión de texto |
| 9 | `personaje_v2/ESTADO.md` | Líneas 29 y 75 (regla del lector) y constancia de la reparación | H1 y H2 | Búsqueda de la regla antigua |
| 10 | `personaje_v2/empresas_v2_correcciones/2026-11_H3/Aarsleff/` *(nuevo)* | `fase_a.json`, `fase_a.md` y `fase_c.json` corregidos; `CORRECCION_H3.md`; regenerados: libro evaluado, `celdas_A.json`, `celdas_C.json`, `citas_fase_a.*`, `citas_fase_c.*`, `datos_v63.*`, `resultados.json`, `observaciones_para_citas.md`, `verificacion_*.txt`, `ficha.json`, `informe.md`, `estado_pipeline.json`; `auditoria.md` nueva | H3 | Criterios H3 1–8 |
| 11 | `personaje_v2/empresas_v2_correcciones/2026-11_H3/resumen_v2.csv` *(nuevo, generado)* | Fila de Aarsleff regenerada | Lo escribe `resumen.py` en la carpeta superior del expediente | El `resumen_v2.csv` original conserva su SHA-256; la fila nueva solo difiere en campos técnicos |
| 12 | `personaje_v2/empresas_v2_correcciones/ceros_heredados_H1.csv` *(nuevo)* | Inventario de los 134 ceros sin `cita`: empresa, año, partida, motivo, página y estado | H1: conservación de los ceros existentes | Recuento de 134, que coincide con los `AR_*.json` |

**No se modifican:** las seis carpetas de `empresas_v2/` ni su `resumen_v2.csv`; `v6/`; `kit_pipeline_munger/`; `Rational/fase1_partes/consolidar.py`; los demás scripts, esquemas, anexos y el personaje.

### Opcional (fuera del alcance obligatorio)

| # | Archivo | Cambio | Motivo |
|---|---|---|---|
| O1 | `personaje_v2/prompts/verificacion.md`, punto 5 | Recontar con Bash todo recuento atribuido a una fila de la Historia | El error de H3 no lo detectó la auditoría |
| O2 | `personaje_v2/scripts/fase1_historia.py` y la fase C | Llevar los ceros pendientes a `datos_ausentes.json` para que se revise su materialidad (S-19) | Haría más visibles los pendientes; cambia el proceso de la fase C |

## 5. Incompatibilidades con la implementación actual y solución mínima

| # | Incompatibilidad | Solución mínima |
|---|---|---|
| I1 | `comprobar_anio` solo devuelve una lista de errores, y sus cuatro usos (`preparar`, en dos sitios; `construir`; la línea de órdenes) tratan una lista vacía como «correcto». No existe un estado PENDIENTE | Parámetro opcional `pendientes`: quien no lo pase ve el comportamiento de siempre, y `construir` y la línea de órdenes lo usan para registrar los pendientes. Sin cambiar el tipo devuelto |
| I2 | Los 134 ceros existentes no tienen `cita`. Con R-c, `preparar` y `construir` los rechazarían y volverían a pedir la extracción de esos años | No volver a ejecutar `preparar` ni `construir` sobre expedientes existentes, inventariar los ceros y revisarlos según el procedimiento de la sección 1 |
| I3 | `historia_revision.md` titula «Ceros con evidencia» lo que no está contrastado | Cambiar el título por «Ceros pendientes de verificación (cita sin contrastar)» |
| I4 | La regla de H2 contradice la decisión registrada del 2-nov (DECISIONES.md), el Anexo D §D.9, `prompts/verificacion.md`, `ESTADO.md` y el docstring | Actualizar los cinco a la vez que el código (archivos 2 y 6–9) |
| I5 | El generador sintético escribe una auditoría de un solo punto («1. PASA · mecánica\n…»); con la regla nueva, los escenarios que esperan APROBADO fallarían | Archivo 3: 16 puntos. Las 30 comprobaciones no cambian |
| I6 | El pipeline nombra los archivos por la carpeta (`<carpeta>_v63_evaluada.xlsx`) y `resumen.py` escribe en el `resumen_v2.csv` de la carpeta superior. Una carpeta «Aarsleff_r1» rompería los nombres, y otra dentro de `empresas_v2/` modificaría el resumen original | Carpeta `Aarsleff` dentro de otra carpeta superior, `empresas_v2_correcciones/2026-11_H3/` |
| I7 | El pipeline no tiene un modo de regeneración sin agentes, y solo se conserva el `fase_c.json` final, no el del turno 1 | Usar `--agentes-simulados` con las salidas guardadas. Comprobación previa ya hecha: el `fase_c.json` final pasa el esquema del turno 1 y el del turno 2 (`resultados/contrato_validar_turno*.txt`). Queda por confirmar en la ejecución que el pipeline llega al paso 13 sin pedir otro agente |
| I8 | Reutilizar el `auditoria.md` original aprobaría en silencio un texto que la auditoría no vio | No poner `auditoria.md` en el DIR simulado: el pipeline pide en el paso 13 una auditoría nueva (agente de verificación ya previsto en el sistema) |
| A1 | El caso 3 se rechaza por R-a, no por R-b, así que R-b quedaría sin prueba. Del mismo modo, R-c tiene dos formas de fallar y el caso 7 solo cubre una | Añadir el caso 3b (línea real con el número dentro de otro) y el 7b (cita ausente de la página) |
| A2 | Los criterios no dicen qué hacer con la palabra FALLA dentro de un punto en PASA | REPETIR (caso 14), como hacen hoy el código y el prompt. Si se prefiere leer solo la primera palabra, solo cambia el caso 14 |
