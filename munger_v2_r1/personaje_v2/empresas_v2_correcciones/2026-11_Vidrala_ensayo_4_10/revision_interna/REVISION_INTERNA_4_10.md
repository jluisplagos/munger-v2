# Revisión interna de la entrega 4.10 (Claude, contexto separado)

**Qué es.** La revisión interna que pide el encargo 4.10 §8 y §9, hecha por una instancia de Claude (Opus 5.5) con un contexto separado, que no participó en el trabajo. Es **interna** y distinta de la revisión externa posterior de ChatGPT. No corrige el material: describe hallazgos y propone correcciones.

**Convenciones.** **[Hecho]** = comprobado en esta revisión (archivo, línea, cifra o ejecución). **[Interpretación]** = lectura del revisor. **[Propuesta]** = corrección sugerida, sin aplicar. Gravedad: **bloqueante** (impide entregar), **importante** (debe corregirse o decidirse antes de dar la entrega por cerrada), **menor** (corrección de coherencia o de redacción).

## 1. Alcance y material

- **Material revisado:** el árbol extraído con `unzip` del ZIP candidato, `/home/claude/w410/zip_c1/comprobacion/extraccion_unzip/munger_v2_r1/`, copiado antes de ejecutar nada en `/home/claude/w410/revision_interna/arbol/`. Todo lo ejecutado se ejecutó sobre la copia.
- **Material fijado:** `/home/claude/w410/revision_interna/MATERIAL_REVISION_4_10.txt`, con el SHA-256 de los 48 archivos revisados a fondo, al empezar (16:41 UTC) y al terminar. **[Hecho]** Los 48 coinciden al principio y al final, en el origen y en la copia.
- **Contexto (no es material de esta revisión):** el ZIP candidato `munger_v2_r1_entrega4.10_consolidacion_financiera_y_trazabilidad.zip` tiene SHA-256 `450ef3d6927825f351b12fb118a3b67b679f2c1f7718f12eb97e0938a18b933f` (122.681.895 bytes). **[Hecho]** Su único nombre no ASCII (`…/n4_paginas_reales_engaños.txt`) lleva el bit UTF-8, y su lista de archivos es exactamente la del `MANIFIESTO_SHA256.txt` de la 4.10 (leído con `zipfile`, sin extraer).
- **Criterio:** el encargo 4.10 completo (adjunto `adb06dfb-attachment.txt`).
- **Fuera de alcance:** `REGISTRO_ENTREGA_4.10.md` y `resultados/LEEME_BATERIAS_HISTORICAS.md`, que siguen provisionales (vacíos), no se cuentan como hallazgo.

## 2. Qué se ejecutó (comandos y resultados reales)

Todo con Python 3 sobre la copia y `TMPDIR` en el directorio temporal de la sesión. Las salidas están en `/home/claude/w410/revision_interna/salidas/`.

| Comando | Resultado |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_trazabilidad_v2.py --json …` | **68/68**, código 0, 28 s |
| `python3 -B pruebas/test_integridad_auditoria_v2.py` | **103/103**, código 0, 16 s |
| `python3 -B pruebas/test_auditorias_v2.py` | **55/55**, código 0, 40 s |
| `python3 -B pruebas/test_resumen_v2.py` | **45/45**, código 0, 29 s (**arrancó LibreOffice**: ver §6, incidencia) |
| `python3 -I -B …_4_10/scripts/n4_revision.py --salida <temporal>` | código 0. `matriz_n4_4_10.json` y `.csv` **idénticos byte a byte** a los entregados. Recuento 18 / 8 / 9 / 3, total 38 |
| `scripts/identidades_propias.py` (propio, aritmética independiente sobre `variantes_4_10.json`) | ver §3.2: las identidades se cumplen con errores ≤ 10⁻¹³ |
| `scripts/referencias_celda*.py` (propios, openpyxl, sin recalcular) | lectores de `Historia!L26`, `Historia!C65` y `Diagnóstico V6!C15` en el libro de referencia |
| `scripts/ataques_revision.py` (propio, 5 ataques) con el código 4.10 y con el de la 4.9 (`--codigo …/codigo_4_9`) | ver §3.1 y R-1, R-3 |
| `scripts/ataque_a6.py` (propio) | `cierre_vigente.json` ilegible o carpeta, con una ficha sin marcadores: **retirado** (código 3) |
| `scripts/conservacion.py` (propio): `MANIFIESTO_4_9.txt` y `MANIFIESTO_SHA256.txt` frente al árbol | ver §3.6 |
| `pdftotext -layout` sobre ES 2025 (SHA-256 `29fd6a29…f14e7`, 372 páginas), págs. PDF 9, 10, 14, 58, 66, 67, 70, 71, 76, 77, 78, 82 y 97 | ver §3.2 |

**No se ejecutó** (restricción de esta revisión): `verificar_paquete.sh`, `test_comprobadores.py`, `test_pipeline_sintetico.py`, `test_estados_v2.py`, `test_cierre_v2.py`, `recalc.sh`, `soffice`, `variantes_4_10.py`, `comprobar_entrega_4_10.py` ni los controles históricos.

## 3. Comprobaciones por bloque

### 3.1 Correcciones técnicas (§3.2–§3.4)

**[Hecho] §3.2, lectura común.**
- `cierre_v2.motivo_rechazo_cierre` (líneas 361–370) usa `texto_fiel(datos)` antes de `veredicto(txt)` (H2), del lector de material (`motivo_auditoria_no_corresponde`, `id_en_auditoria`) y del lector de solicitud (`motivo_respuesta_no_aceptada` → `lineas_solicitud`).
- El paso 13 de `pipeline.py` (líneas 338–343) también usa `CIE.texto_fiel`. Antes usaba `decode("utf-8-sig")`: el defecto estaba solo en el cierre y la vigencia.
- `texto_fiel` hace solo lo declarado: BOM, CRLF/CR, saltos finales y NFC. Las huellas de bytes (`sha_archivo`, `resp["sha256"]`) siguen sobre los bytes reales. El legado sin huella fiel compara bytes exactos (línea 195, en `motivo_respuesta_no_aceptada`, y la rama `auditoria_sha256` de 4.8.1).
- **`Pipeline.veredicto_auditoria` queda intacto:** el diff de `pipeline.py` frente a la 4.9 solo tiene dos bloques (líneas 299 y 338–343), ninguno en H2.
- **[Interpretación]** Aplicar NFC antes de H2 solo puede hacerla más estricta: un encabezado como «8 CRÍTICO» en NFD no casaba con `[A-ZÁÉÍÓÚÑ]{4,}` y en NFC sí casa. No se ha encontrado ningún caso en que NFC convierta un REPETIR en APROBADO.

**[Hecho] §3.3, ficha sin marcadores.**
- `cierre_registrado` (línea 572) = `os.path.lexists(cierre_vigente.json)`.
- La nueva rama de `motivo_vigencia` (líneas 615–627) retira si la ficha falta o no es la registrada, y si `cierre_vigente.json` es ilegible.
- `archivar_salidas` (línea 689) trata ese caso como cerrado y retira también sin empresa.
- `ficha.py` (línea 81), `informe.py` (línea 74), `resumen.py` (línea 51) y `pipeline.py` (línea 299) usan la misma condición, y `resumen.py` ya no escribe filas sin empresa.
- El ataque A6 (`cierre_vigente.json` con JSON roto o convertido en carpeta) se retira con código 3.
- **Hueco:** la detección depende de ese único archivo (R-1).

**[Hecho] §3.4, acreditación del libro.**
- `verificar_todo.sh` llama a `acreditar_libro.py` después de la incorporación de cachés y exige `verificacion_libro_final.txt` y `acreditacion_libro.json`.
- El libro no lleva su propio hash: no hay referencia circular.
- `MATERIAL_FIJO.extend` (línea 435) incorpora el comprobante al material. En los expedientes anteriores no existe ese archivo, así que su identificador de material no cambia.
- A5 (comprobante eliminado después de un cierre que lo tenía en el material): **retirado** por cambio de material. A4 (comprobante que acredita el libro de datos): **detectado** por la ficha.
- **Huecos menores:** R-3.

**[Hecho] Pruebas frente a los defectos originales.**
- `tecnico/reproduccion/trazabilidad_con_codigo_4_9.txt` da 26/64. Fallan:
  - 26 del grupo B: 5 + 16 + 4 + 1, como declara el informe;
  - 10 del grupo M: 8 + 1 + 1;
  - 2 del grupo L: 1 y la excepción.
- Con el código 4.10, esta revisión obtuvo **68/68**.
- Los casos legítimos se conservan: el estado temprano sin cierre, el BOM aceptado y las cuatro vías vigentes.

**[Hecho] Ataques propios con el código 4.10** (`salidas/ataques_revision.txt`):

| Ataque | Resultado |
|---|---|
| A1 · ambos marcadores eliminados + `cierre_vigente.json` eliminado (`resumen.py`, `informe.py`, `ficha.py`) | **NO detectado**: fila `pendiente_de_datos / APROBADO`, código 0 |
| A2 · ficha `{}` + `cierre_vigente.json` eliminado | `resumen.py`: sin fila sin empresa (mejora frente a la 4.9). Tras `ficha.py --estado pendiente_de_datos`: **fila `pendiente_de_datos / APROBADO`** |
| A3 · comprobante con SHA-256 correcto y veredicto «NO ÍNTEGRO» | **aceptado** por `motivo_acreditacion_libro` |
| A4 · comprobante del libro de datos | detectado (la ficha registra otro libro) |
| A4b · igual, sin `hashes.libro_evaluado` en las fichas | **aceptado** por la función (el material lo cubre aparte) |
| A5 · comprobante eliminado después del cierre | detectado (el material cambió) |
| A6 · `cierre_vigente.json` ilegible o carpeta, con la ficha sin marcadores | detectado (código 3) |

Con el código de la 4.9, A1 da el mismo resultado (el defecto es heredado), y A2 además publicaba una fila sin empresa con APROBADO.

### 3.2 Financiero

**[Hecho] Cifras contra el PDF español de 2025** (`pdftotext -layout`, página del PDF):

| Cifra | Página | Resultado |
|---|---|---|
| Cierre a 90,10 € y capitalización de 3.172 millones | 97 | coincide |
| 35.206.258 acciones; 23.400 propias (2.097 miles); liberada 1×20 el 23-oct-2025 | 67 | coincide (la tabla de la nota 14(k) llama «en circulación» a las 35.206.258) |
| Dividendo a cuenta de 1,2318 €, 43.338 miles, pagado el 13-feb-2026 | 70 | coincide |
| Propuesta de distribución: 43.338.244,48 y complementario 16.490.205,54 | 71 | coincide |
| «Accionistas por dividendos» 43.338 (2024: 37.547), nota 17 | 76 | coincide |
| Provisión «Personal» 6.223 (2024: 6.053); total de provisiones 64.180; derechos de emisión 46.366 | 77 | coincide |
| Composición de la provisión «Personal» | 78 | coincide |
| Arrendamientos: gasto devengado 2.452 / 2.179, pagos (8.314) / (6.117) y «corrientes y de poco valor» 8.314 / 6.117, la discrepancia visible | 58 | coincide |
| Derivados corrientes 1.157 / 25.567 | 9 | coincide |
| Pasivos derivados 6.938 no corrientes y 1.235 corrientes; pasivos financieros 196.080 + 66.833 = 262,913 (2024: 300.624 + 92.688 = 393,312) | 10 | coincide |
| «Pagos de intereses» (20.800), en explotación | 14 | coincide |
| Promedio ponderado de 35.206 miles | 82 | coincide |
| Nota 13, «Otros activos corrientes» de 2025 y 2024: solo administraciones públicas (IVA y otros conceptos) | 66 | coincide |

- 43.338.244,48 ÷ 1,2318 = 35.182.858,0 (comprobado).
- i = 20,8 ÷ ((393,312 + 262,913)/2) = 0,0633929. Es el heredado, igual en todas las variantes.

**[Hecho] Identidades con aritmética propia** (`salidas/identidades_propias.txt`):

| Identidad | Resultado |
|---|---|
| La base reproduce la referencia del encargo | diferencias ≤ 4·10⁻⁷ |
| Ponderado = Σ p·V en las 12 variantes | error ≤ 4,3·10⁻¹⁴ |
| N6, r_op = (r·E + i(1−τ)·D)/(E+D) en base, N6, N7 conjunto y C1 | error ≤ 4·10⁻¹⁷ |
| E de N6 = 90,10 × 35,206258 = 3.172,0838 | coincide |
| E de C1 = 90,10 × 35,182858 = 3.169,9755 | coincide |
| τ alternativa, con 0,2433 en el escudo | 0,086782998227, que es el valor sustituido en C15 |
| N7 puro, V·N/N′ − V′ | ≤ 6,4·10⁻¹⁴ |
| N8, V_sin − (V_con − 43,338/35,206) en los tres escenarios, el ponderado y el precio de Sí | ≤ 7,1·10⁻¹⁴ (−1,2309834) |
| N8, puente | 204,122 = 160,784 + 43,338, con la caja, r_op, E y N fijos |
| C2 − (C1 − 43,338/35,182858) | ≤ 8,5·10⁻¹⁴ (−1,2317931) |
| N5, ΔV + ΔL25/N, con L25 = 6,223 × 0,75 = 4,66725 | ≤ 5,6·10⁻¹⁴ (+0,0441899) |
| P3, B1 = B2 en valoración, FCF y `f` | ΔFCF = −2,254 y ΔV = 0. **B2 usa C49 = 6,754**, no 6,764 (R-4) |
| Precio de Sí de la referencia, a mano por tramos | 65,6881 |
| Precio de Sí del MALO adverso | 61,5318 |
| Sensibilidad 0,1/0,6/0,3 | 70,4259 |
| g < r_op en las 12 variantes | se cumple |

- La caja es 108,352 en todas las variantes: no se suma nada a la caja.
- r = 0,09, g = 0,01 / 0,02 / 0,025, probabilidades 0,2 / 0,6 / 0,2 y k = 3 en todas.
- Solo cambian las celdas declaradas en `celdas` y `sustituciones_estructurales`.
- Las cifras del informe financiero y de la propuesta coinciden con el JSON, salvo R-4.

**[Hecho] El vehículo del dividendo, `Historia!L26`, es la fila «Minoritarios»** («Intereses no dominantes»).
- Entra en `Historia!C65` («Pensiones + minoritarios»), que alimenta el puente (`Diagnóstico V6!C16`) y también `Diagnóstico V6!B63`, `D63`, `B64` y `D64` (EV ÷ ventas y EV ÷ EBITDA).
- Para la valoración es puro, porque la identidad se cumple. La frase «solo entra en el puente» es inexacta (R-5).

**[Hecho] La alternativa de τ** está etiquetada como «alternativa (estructural)», con la fórmula de C15 sustituida por un valor y τ del motor sin cambios (0,20032). Su `estado_tecnico` dice «COMPLETO Y VÁLIDO» (R-6).

### 3.3 N4 revisada

- **[Hecho]** La matriz de la 4.9 tiene 35 entradas de clase 2 y 3 de clase 4. Con las reglas de `n4_revision.py`:
  - **completas, 18:** adquisiciones 5, minoritarios 10, intereses 2016–2017 2, y otros activos financieros de 2023 1 (derivados 0);
  - **parciales, 8:** intereses de 2018–2025;
  - **dependientes de la definición, 9:** otros activos financieros con derivados distintos de 0;
  - **no aplicables, 3.**

  El recuento sale de la clasificación revisada; no hay ninguna cuota.
- **[Hecho]** Los 38 campos `registro` y los 10 de `decisiones_4_10.json` tienen `decision`, `fecha` y `confirmado_por` / `decidido_por` a `null`.
- **[Interpretación]** La definición de otros activos financieros es honesta:
  - la lectura estrecha se presenta como propuesta (D-N4-OAF), no como adoptada;
  - las 9 entradas con derivados no se cuentan como completas;
  - no se suma nada a la caja.

  Un límite: la composición de «Otros activos corrientes» (nota 13) solo se ha visto para 2024–2025 (R-9).

### 3.4 Copia combinada y expediente exploratorio

**[Hecho] Copia combinada.**
- `copia_combinada/Vidrala_v63_evaluada.xlsx` tiene SHA-256 `68512df4…8449`, igual a `acreditacion_libro.json → archivo_final`, con veredicto ÍNTEGRO y cachés incorporadas.
- El prefijo verificado antes de las cachés (`d2d4a909…`) es el de `variantes/copias/COPIA_EXPLORATORIA_C1_…xlsx`.
- C41 = 3.169,975506, C55 = 35,182858 y la caché de C83 = 70,466507, que es el ponderado de C1.
- **Es la acreditada.** Pero su «libro de entrada» no es el de C1 (R-2).

**[Hecho] Expediente exploratorio.**
- `estado_pipeline.json`: paso 5, esperando `5:extracto_v63.md`; `auditoria` null, `auditoria_respuesta` null y `estado_analisis` null; `solicitudes_auditoria` [].
- La aprobación de la 4.6.1 se archivó en `historial_cierres/02_74b94f8072dd58c1/` («el material cambió … alcance_v2.json»).
- **No se hereda ninguna aprobación.** Una reanudación pediría una solicitud nueva y anotaría las auditorías existentes como conocidas (`auditorias_del_expediente`).
- Conserva artefactos de la 4.6.1 sin regenerar (R-7).

### 3.5 Documentación

**[Hecho]** `VERSION`, `CONTINUIDAD.md` §1–§2, `PROMPT_NUEVA_VENTANA.md`, `DECISIONES.md` (nuevo bloque del 11-nov) y `verificar_paquete.sh` (bloque nuevo de trazabilidad, obligatorio en «completa», umbral ≥ 68) son coherentes entre sí y con los archivos en:
- los recuentos 68 / 103 / 55 / 28 / 45 / 55 / 114 / 30 / 35;
- el 26/64 con el código de la 4.9;
- N4 18 / 8 / 9 / 3;
- 90,10, 35.182.858 y −43,338/N;
- el expediente detenido en el paso 5.

**Entregables del §9:**

| Entregable | Situación |
|---|---|
| Informe financiero | presente |
| Tabla CSV/JSON con configuraciones (`celdas`) | presente |
| Matriz y propuestas N4 | presente |
| Copias, entradas, scripts y diagnóstico | presente |
| Informe técnico con antes y después | presente |
| Propuesta única | presente |
| Especificación | presente |
| `CAMBIOS_ARCHIVOS.txt` y manifiesto | presente |
| Registro de cambios 4.9 → 4.10 con huellas antes y después | pendiente del REGISTRO provisional |

`CAMBIOS_ARCHIVOS.txt` compara con la base original de 676 archivos, no con la 4.9. La relación 4.9 → 4.10 con huellas (§9) solo puede salir de `reproduccion/MANIFIESTO_4_9.txt` frente al manifiesto nuevo, y debería figurar en el REGISTRO (ver §3.6).

**Afirmaciones de ejecución.** No se ha encontrado ninguna afirmación de que algo se ejecutó que no se pueda comprobar, salvo la del arranque (§5, «no comprobado»). Los resultados «esperados» de `CONTINUIDAD.md` §2 están formulados como expectativas.

### 3.6 Conservación

**[Hecho]** Comparación de `reproduccion/MANIFIESTO_4_9.txt` (1.733 entradas) con el árbol: 0 ausentes y **12 cambiados**:
- `CAMBIOS_ARCHIVOS.txt`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `VERSION` y `verificar_paquete.sh`;
- `personaje_v2/DECISIONES.md`;
- `cierre_v2.py`, `ficha.py`, `informe.py`, `pipeline.py`, `resumen.py` y `verificar_todo.sh`.

Todos son scripts o documentación vigente, con motivo declarado.

- Ningún original, expediente anterior, fuente ni archivo de decisiones cambió. En particular, `prompts/historia_anio.md` y `fase1_decisiones.json` no cambian.
- Los 169 archivos nuevos están en el expediente 4.10, salvo `pruebas/test_trazabilidad_v2.py` y `scripts/acreditar_libro.py`, ambos declarados.
- Frente al manifiesto 4.10, el árbol de la revisión da 0 modificados y 0 ausentes. Tiene 44 adicionales, todos artefactos que crearon las pruebas de esta revisión: 35 en `personaje_v2/.lo_perfil/` y 9 `.pyc`.

## 4. Hallazgos

### R-1 · importante · Una ficha sin marcadores, con `cierre_vigente.json` eliminado, vuelve a publicar `pendiente_de_datos / APROBADO`

- **[Hecho] Ataque A1** (`salidas/ataques_revision.txt`).
  - Sobre un cierre 4.10 válido (código 0, fila concluido/APROBADO), se quitan «cierre» y el estado concluido de `ficha.json` y se borra `cierre_vigente.json`.
  - `resumen.py`, `informe.py` y `ficha.py --estado pendiente_de_datos` terminan con código 0 y dejan la fila `Vidrala, S.A. · pendiente_de_datos · APROBADO`.
  - `estado_pipeline.json` sigue con `auditoria = APROBADO` y `estado_analisis = concluido`, y `auditoria_respuesta` sigue registrada.
- **[Hecho] A2.** Con `{}`, `resumen.py` ya no publica una fila sin empresa, pero tras `ficha.py --estado pendiente_de_datos` aparece la misma fila incoherente.
- **[Hecho] Es heredado:** con el código de la 4.9 da exactamente lo mismo.
- **Causa:**
  - `cierre_registrado` (`cierre_v2.py`, línea 572) solo mira `cierre_vigente.json`, aunque el estado del pipeline y `publicaciones_resumen.json` registran el cierre;
  - `resumen.py` (línea 87) copia `pipe.get("auditoria")` en `verificacion` también para una ficha no cerrada.
- **[Interpretación]**
  - El encargo exige la «ausencia de aprobaciones incoherentes» y cita esa misma salida (`pendiente_de_datos / APROBADO`).
  - En la 4.9 ya se protegía el borrado de `cierre_vigente.json` con una ficha cerrada, así que no es la «reescritura coherente» que declara el límite del informe técnico: el estado sigue diciendo APROBADO.
- **[Propuesta]**
  1. En `resumen.py`, no escribir `verificacion = APROBADO` si la ficha no está cerrada y vigente. No hay ningún caso legítimo de una ficha sin «cierre» con APROBADO: el estado temprano legítimo tiene `auditoria = None` tras archivar.
  2. Ampliar «cierre registrado» a `estado_pipeline.json` con `auditoria == "APROBADO"` o `auditoria_respuesta`, y a una entrada viva en `publicaciones_resumen.json` de este expediente.
  3. Añadir A1 y A2 al grupo M de `test_trazabilidad_v2.py`, en las cuatro vías.

### R-2 · importante · El «libro de entrada» acreditado de la copia combinada no es el de C1; no hay ninguna pareja coherente de C1

- **[Hecho]** `copia_combinada/acreditacion_libro.json → libro_entrada` es `Vidrala_v63_datos.xlsx`, con SHA-256 `b3b7f941…f2e2`. Es el de datos de la 4.6.1, copiado por `variantes_4_10.py`, línea 164, con C41 = 3.094,6 y C55 = 35,206.
- **[Hecho]** El evaluado acreditado tiene C41 = 3.169,975506 y C55 = 35,182858.
- **[Hecho]** `verificar_todo.sh` no se ejecutó sobre la copia combinada: en ella solo están `verificacion_integridad.txt` y `verificacion_libro_final.txt`, y faltan las verificaciones de celdas, esquemas, estado del libro y C86.
- **[Hecho]** El expediente exploratorio tiene la otra mitad: datos de C1 (`fb2b99dc…`, C41 = 3.169,975506) y el evaluado de la 4.6.1 (`1020bb53…`).
- **[Interpretación]**
  - El §3.4 pide distinguir «libro de entrada, libro evaluado y archivo final», y el §6, una copia combinada «identificada y reproducible».
  - El comprobante identifica como entrada un libro que no contiene las entradas de C1.
  - No afecta a ningún valor ni a ninguna aprobación, pero es un registro de trazabilidad engañoso, precisamente en la pieza nueva de P-N2.
- **[Propuesta]**
  - Usar como entrada de la copia combinada el libro de datos con C41 y C55 de C1 (el del expediente exploratorio sirve, si se confirma que solo difiere en esas celdas), o anotar en el comprobante que la copia se obtuvo sobre el evaluado de la referencia y no tiene libro de entrada propio.
  - Decir en `INFORME_FINANCIERO_4_10.md` §8 que la copia no pasó por `verificar_todo.sh` completo, o ejecutarlo.

### R-3 · menor · `motivo_acreditacion_libro` no exige el veredicto del comprobante ni que acredite el libro evaluado

- **[Hecho] A3.** `acreditar_libro.py` escribe el comprobante también cuando la verificación final falla (línea 56, antes de calcular `ok` en la 57), y `motivo_acreditacion_libro` (`cierre_v2.py`, líneas 438–462) no lee `archivo_final.veredicto`. Un comprobante «NO ÍNTEGRO» con el SHA-256 correcto se acepta.
- **[Hecho] A4b.** La función acepta cualquier `.xlsx` del expediente (línea 448) si las fichas no tienen `hashes.libro_evaluado`.
- **[Interpretación]** Hoy lo mitigan el paso 12 (un FAIL de `verificar_todo.sh` termina en `no_entregable`) y el material fijado. Es una defensa en profundidad que falta.
- **[Propuesta]** Exigir `veredicto` que empiece por «ÍNTEGRO» y `archivo == f"{empresa}_v63_evaluada.xlsx"` (o el evaluado del material), con dos pruebas en el grupo L.

### R-4 · menor (corregir antes de la firma) · Cifras de la propuesta: P3 alternativa B y efecto de τ

- **[Hecho]** `PROPUESTA_DECISIONES_4_10.md`, línea 67, y `decisiones_4_10.json` (D-P3) dicen: «C48 = 2,254 con C49 = 4,5, o C48 = 0 con C49 = 6,764, **que son equivalentes**».
  - No lo son: 2,254 + 4,5 = 6,754.
  - La variante calculada `P3_B2` usa C49 = 6,754, con P = 4,5 de la referencia; 6,764 es P+I con P = 4,510.
  - El informe financiero no muestra el 6,754.
- **[Hecho]** La propuesta, línea 74 (B4), dice «+0,232 en P» para τ = 0,2433. Es el efecto respecto a A2/N6. Respecto a la referencia, que es la base que la propuesta declara para todos los efectos, es +0,155 (`delta_ponderado` 0,154796).
- **[Propuesta]** Escribir la alternativa B con un solo P (4,5 → 6,754, o 4,51 → 6,764 con C48 = 2,254 y C49 = 4,51) y dar el efecto de τ con su base explícita.

### R-5 · menor · El vehículo del dividendo es la fila «Minoritarios» y también mueve los múltiplos EV

- **[Hecho]** `Historia!A26` dice «Minoritarios». Además de en el puente, L26 entra en `Diagnóstico V6!B63/D63` (EV ÷ ventas) y `B64/D64` (EV ÷ EBITDA), a través de `Historia!C65`.
  - `INFORME_FINANCIERO_4_10.md`, línea 159, y la descripción de N8 en el JSON dicen «solo entra en el puente».
  - Los múltiplos que cambian no se registran en las variantes.
- **[Interpretación]** La identidad de valoración no se ve afectada, y el uso está declarado («no son minoritarios»). Pero en la copia, la celda etiquetada «Minoritarios» vale 43,338.
- **[Propuesta]**
  - Corregir la frase y registrar los diagnósticos afectados en N8 y C2.
  - Añadir a `ESPECIFICACION_INTEGRACION_4_10.md` §2 una partida propia para obligaciones de distribución devengadas en el puente.

### R-6 · menor · La copia «no íntegra» de τ aparece como «COMPLETO Y VÁLIDO»

- **[Hecho]** `N6_E_2025_tau_2025` tiene la fórmula de `Diagnóstico V6!C15` sustituida por 0,086782998227, y su descripción dice «copia estructural, no íntegra».
- **[Hecho]** El CSV y el JSON le dan `estado_tecnico = COMPLETO Y VÁLIDO`, y el informe, línea 205, dice «Estado técnico en todas: COMPLETO Y VÁLIDO» sin excepción. No consta ninguna verificación de integridad de esa copia.
- **[Propuesta]** Añadir un aviso en esa fila («estado técnico de la hoja; la copia no pasa la verificación de integridad por la sustitución estructural») y matizar la frase del §8.

### R-7 · menor · Expediente exploratorio: artefactos de la 4.6.1 sin marcar y el motivo de no seguir

- **[Hecho]** Siguen siendo los de la 4.6.1, con la aprobación ya archivada:
  - `Vidrala_v63_evaluada.xlsx` (`1020bb53…`, con E = 3.094,6 y N = 35,206);
  - `resultados.json`, `precio.json`, `ficha_provisional.json`, `informe_provisional.md`, `material_auditoria.json` (material `74b94f…`) y `auditoria.md`;
  - `LEEME_ANTES_DE_CONTINUAR.md`, que es el de la 4.6.1 y describe que «el paso 14 escribió `ficha.json`, `informe.md` y `cierre_vigente.json`».

  Solo `alcance_v2.json` explica que es C1.
- **[Interpretación]**
  - El estado del paso 5, esperando, es legítimo: no se fuerza nada ni se hereda ninguna aprobación.
  - Pero «Es su estado legítimo» (informe, línea 214) presenta como impuesto por los datos lo que es una decisión de alcance: la entrada está completa («0 bloqueantes»), y los pasos 5–9 no dependen del precio.
  - El motivo dado (la fase C compararía con 87,90 €, fuera del encargo) es razonable y está declarado como interpretación.
- **[Propuesta]**
  - Añadir en el expediente un `LEEME_4_10.md` que diga qué archivos son anteriores a C1 y no deben leerse como resultados de C1.
  - Formular la parada como decisión de alcance pendiente: si se encarga, ejecutar los pasos 5–14 con una auditoría nueva.

### R-8 · menor · `test_resumen_v2.py` arranca LibreOffice y la documentación no lo dice

- **[Hecho]** Su última prueba («estado temprano sin auditoría», `test_resumen_v2.py`, línea 556) ejecuta el pipeline de una empresa sintética desde el principio: pasos 1–3 con `recalc.sh` y `soffice`.
  - En esta revisión creó `personaje_v2/.lo_perfil/` (35 archivos) entre las 16:43:30 y las 16:43:37 UTC.
  - `CONTINUIDAD.md`, línea 52, enumera las pruebas que arrancan LibreOffice sin incluirla.
  - El docstring de `test_resumen_v2.py` («sin LibreOffice» para las copias) es ambiguo.
- **[Propuesta]**
  - Añadir `test_resumen_v2.py` a esa lista de `CONTINUIDAD.md`.
  - Precisar el docstring y, en las instrucciones a revisores, no clasificarla como batería sin LibreOffice.

### R-9 · menor · Otros activos financieros: «Otros activos corrientes» solo se ha visto para 2024–2025

- **[Hecho]** La nota 13 (ES 2025, pág. PDF 66) muestra que «Otros activos corrientes» de 2025 y 2024 son solo administraciones públicas.
- **[Hecho]** La 4.10 clasifica los otros activos financieros con las líneas del balance y no cita esa nota para 2016–2023, cuando la partida llegó a 40,863 en 2022.
- **[Propuesta]** Citar la composición de la nota de cada año antes del registro humano de las 9 y de la de 2023, o declarar el límite en la matriz.

## 5. Lo que no se pudo comprobar

- Los valores de las 12 variantes salen de recálculos con LibreOffice que esta revisión no repitió (`variantes_4_10.py` está prohibido aquí). Las copias de `variantes/copias/` no llevan cachés. Se comprobó la aritmética entre los valores publicados, no su recálculo.
- La copia combinada: no se ejecutó `verificar_v63` ni `add_cached_values`. Solo se leyeron sus valores en caché y se recalcularon sus huellas.
- No se ejecutaron ni `verificar_paquete.sh completa`, ni las baterías con LibreOffice (114, 30, 28 y 55), ni los controles históricos, ni `comprobar_entrega_4_10.py`.
- No se comprobó la verificación completa del árbol 4.9 que `arranque/ARRANQUE_4_10.md` da por PASA («en la conversación de arranque»): no hay ninguna salida conservada en el árbol.
- No se ejecutó el caso «`ficha.json` ausente con cierre registrado». Por lectura del código, `resumen.py` sin ficha retira las publicaciones, pero deja `estado_pipeline.json` y `cierre_vigente.json`, y la retirada completa ocurre en `ficha.py` o en el paso 14.
- No se revisaron en profundidad la extracción del ZIP con los dos lectores (`empaquetar_zip.py --comprobar`), las versiones inglesa y ESEF, ni el contraste del precio con BME.
- El fundamento económico de N10 se revisó como coherencia de lo declarado, no como juicio de inversión.

## 6. Incidencia de esta revisión

- **[Hecho]** La restricción de no arrancar LibreOffice se incumplió sin querer. `test_resumen_v2.py`, permitido en las instrucciones de la revisión, arrancó `soffice` durante unos 7 segundos (16:43:30–16:43:37 UTC), mientras otra verificación con LibreOffice podía estar en curso.
- Usó un perfil propio, en la copia (`/home/claude/w410/revision_interna/arbol/personaje_v2/.lo_perfil/`), distinto del de cualquier otro árbol. No queda ningún proceso `soffice` de esta revisión.
- **[Hecho]** El árbol de origen no contiene `.lo_perfil` y sus 48 archivos revisados conservan sus huellas.
- **[Propuesta]** Revisar si la otra verificación con LibreOffice registró alguna anomalía entre las 16:43 y las 16:44 UTC, y repetir solo el bloque afectado si la hubo.
