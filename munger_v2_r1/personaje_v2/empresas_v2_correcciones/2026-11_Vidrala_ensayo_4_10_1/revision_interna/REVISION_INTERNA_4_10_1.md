# Revisión interna independiente · entrega 4.10.1

**Qué es.** La revisión interna de los dos puntos principales del encargo 4.10.1 (§7): la preparación de T-1 y el expediente completo a base 2025. La hizo un agente de revisión de Claude que no participó en el trabajo, con contexto separado, el 11-nov-2026, entre las 23:13 y las 23:45. No es la revisión externa y no la sustituye.

**Objeto revisado.** Árbol de trabajo `munger_v2_r1/`, comparado con el ZIP de la 4.10 (SHA-256 `dab490a5…68363`, comprobado). El ejecutor siguió escribiendo durante la revisión: VERSION, CONTINUIDAD.md, PROMPT_NUEVA_VENTANA.md, registros vacíos, `comprobar_entrega_4_10_1.py`, `generar_cambios_y_manifiesto.py`, y retocó `comparar_con_C1.py` y `concordancia_2025.py`. **No cambió nada en `Vidrala/`, en la prueba ni en el código de producción** entre la instantánea inicial y la final de la revisión. Los objetos revisados tienen estas huellas:

| Objeto | SHA-256 |
|---|---|
| `personaje_v2/pruebas/test_trazabilidad_v2.py` (4.10 → 4.10.1) | `6e8649db…` → `bac433b4…` |
| `Vidrala/Vidrala_v63_evaluada.xlsx` (libro final) | `da053c79bdcffe14…` |
| `Vidrala/Vidrala_v63_datos.xlsx` | `d6c2518f7f5aedd2…` |
| `Vidrala/ficha.json` · `informe.md` · `auditoria.md` | `f2e2d74c…` · `5cc2a9fa…` · `6703c396…` |

---

## 0. Veredicto

| Punto | Veredicto |
|---|---|
| **1 · T-1** | **Correcto.** La corrección está solo en la prueba, sigue el orden pedido, no rebaja ninguna expectativa y es independiente de los bytes del Excel: la revisión lo **reprodujo con las propias pruebas en un entorno con bytes distintos**: 4.10, 73/74, con el mismo fallo que la revisión externa; 4.10.1, 78/78. Hay un hallazgo de severidad **baja** (H-3): las dos pruebas nuevas de reconstrucción pueden fallar en falso en un caso límite. |
| **2 · Expediente 2025** | **Recorrido legítimo y conclusión coherente** con el material y las reglas: concluido · Vigilar · esperar; ponderado 71,66; precio de Sí 66,52 frente a 90,10. El recálculo, la acreditación, las huellas, la auditoría nueva y la publicación aislada están bien. Hacen falta **correcciones documentales**: H-1 (**media**), restos de la capitalización y de la N antiguas en la evidencia del libro final, con una concordancia que afirma «ninguno»; y H-2 (**baja**), notas obsoletas en los metadatos activos que una regeneración repondría. Ninguna cambia un número ni la conclusión. |

---

## 1. Qué ejecutó la revisión y qué solo leyó

**Ejecutado por la revisión.** Siempre en secuencia, nunca dos procesos con LibreOffice a la vez, y con los temporales en el scratchpad de la revisión:

1. Huella del ZIP 4.10 (`dab490a5…`, coincide con el encargo), extracción a un temporal y `diff -rq` del árbol completo frente al ZIP.
2. `python3 -B pruebas/test_trazabilidad_v2.py` en el árbol de trabajo: **78/78, código 0; grupo L 11/11** (unos 2 min).
3. `python3 -I -B …/scripts/reproducir_T1.py`: código 0. La salida es **idéntica byte a byte** a `t1/reproducir_T1_salida.txt`.
4. **Reproducción independiente de T-1 con las pruebas reales.** Una copia de `verificar_todo.sh` en el scratchpad reempaqueta el libro tras incorporar las cachés y antes de acreditarlo (mismos miembros, otra fecha interna y otra compresión), como haría otro entorno. Se pasó con `--codigo` a la prueba de la 4.10 (sobre el árbol extraído del ZIP) y a la de la 4.10.1 (sobre el árbol de trabajo). Resultados en §2.5.
5. `comparar_con_C1.py --salida <scratchpad>` (versión actual): atribución, controles, valores y **huellas de las cuatro copias idénticos** a los archivados.
6. `concordancia_2025.py --libro --salida <scratchpad>`: CONCUERDA, idéntica a la archivada.
7. `validar_esquema.py` sobre fase_a, fase_b, fase_c (turno 2), ficha y ficha_provisional: los cinco VÁLIDO. `verify_quotes_v2.py` (Munger y Damodaran, páginas estrictas) sobre informe, fases y Observaciones: PASS.
8. Controles de producción en solo lectura:
   - `Pipeline.veredicto_auditoria(auditoria.md)` = APROBADO;
   - `cierre_v2.motivo_acreditacion_libro` = None;
   - `cierre_v2.motivo_vigencia(…, veredicto_auditoria)` = None.

   Una primera llamada de la revisión pasó la razón social como `empresa` y dio un falso «material cambió». Fue un error de uso de la revisión (el parámetro es el prefijo de los archivos), no un hallazgo.
9. `precio_de_si.p_estrella([53,6597; 72,7405; 86,4439], [0,2; 0,6; 0,2], 3)` = 66,5206; ponderado = 71,6650.
10. Comprobaciones con openpyxl (`data_only`):
    - etapa 1 original frente a la copia de ensayo;
    - libro final frente a la copia recalculada;
    - barrido de restos;
    - rastreo de las fórmulas que usan C57, C38, C15 y C17.
11. `pdftotext` del PDF español de 2025 (SHA-256 `29fd6a29…`, coincide con la configuración), págs. 9, 10, 11, 14, 17, 67 y 97.
12. Huellas: el material auditado (20/20), el inventario de heredados (75/75) y el de la preparación 1 (16/16).

**Solo leído:**
- el encargo;
- el informe T-1 y el del recorrido;
- la configuración;
- las fases, la ficha, el informe, la auditoría y los prompts;
- los scripts del ensayo y el código de producción afectado.

**No ejecutado:**
- `pipeline.py` y `verificar_todo.sh` sobre el expediente real;
- `verificar_paquete.sh`;
- `comprobar_entrega_4_10_1.py`, en curso por el ejecutor;
- el ZIP final.

**Limpieza.** La ejecución de `reproducir_T1.py` creó `personaje_v2/scripts/__pycache__/` (ver A-T1-1); la revisión lo borró. Al terminar, el árbol solo difiere de la instantánea inicial en los archivos del ejecutor citados arriba y en este informe.

---

## 2. Punto 1 · T-1 (grupo L de `test_trazabilidad_v2.py`)

### 2.1 El código de producción no cambia
`diff -rq` frente al ZIP de la 4.10:
- `personaje_v2/scripts/`, `kit_pipeline_munger/`, `v6/` (sin `__pycache__`), `esquema/` y `prompts/`: **idénticos**.
- Fuera del ensayo solo cambian `pruebas/test_trazabilidad_v2.py` y `verificar_paquete.sh`.
- Quedan además dos restos de ejecución que no estaban en el ZIP de la 4.10: `personaje_v2/.lo_perfil/` y `v6/scripts/__pycache__/`, este ya presente al empezar la revisión.

### 2.2 El orden pedido se cumple (`prueba_correspondencia`)
1. **Libro final acreditado.** `verificar_todo.sh` construye y acredita el libro antes de llamar a la función, y la prueba anterior del bucle exige `fin.sha256 == sha(ev)`.
2. **Fichas sintéticas antes de m0.** `fichas_sinteticas(c.d, final)` escribe las fichas de la **copia de la prueba** (en `TMP`) con la identidad del archivo, y solo después se calcula m0. No se toca ninguna ficha, auditoría ni cierre real.
3. **Precondición coherente.** `m0 is None` forma parte de las cuatro aserciones de rechazo.
4. **Mutaciones separadas.** Cada mutación se aplica en su propia copia:
   - ficha que registra otro libro → «registra otro libro»;
   - modificación posterior → «no es el libro acreditado»;
   - JSON ilegible → «no se puede acreditar»;
   - comprobante que nombra un libro ausente → «falta el libro acreditado».

Los diagnósticos exigidos coinciden con los textos de `cierre_v2.motivo_acreditacion_libro`, que no cambia.

### 2.3 Expectativas: ninguna se rebaja
- La aserción antigua toleraba que faltara la ficha provisional: `(not F or …)`. **La nueva exige el rechazo siempre** (es más estricta).
- La comprobación de huella sigue intacta y se refuerza con la de identidad estricta.
- La última prueba de L amplía su alcance a `2026-11_Vidrala_ensayo_4_10_*` con la misma lógica.
- La prueba de R-3 recibe la misma preparación. En la práctica no cambia nada, porque acredita sin cachés y el libro copiado ya es el que registran sus fichas.
- Los grupos B y M no cambian.
- El grupo L pasa de 7 a 11 casos: se conservan los 7 y se añaden 4 (comprobante ilegible, falta de correspondencia, reconstrucción inocua e identidad estricta). Total: 74 → 78.

### 2.4 `verificar_paquete.sh`
Exige `n_tot ≥ 78` y conserva el patrón de la línea final («N/M pruebas de trazabilidad de la 4.10 PASAN»), que la batería sigue imprimiendo.

### 2.5 Reproducción del fallo antiguo y de la independencia nueva
- **Script del ejecutor.** `reproducir_T1.py` reproduce el mecanismo con un «otro entorno» simulado, y lo declara simulado: libro final `fa874f1c…`, m0 antiguo «ficha.json registra otro libro evaluado (1020bb53…)», m0 nuevo None. La revisión lo reejecutó con el mismo resultado.
- **Reproducción de la revisión con las pruebas reales** (`--codigo` con el `verificar_todo.sh` perturbado):

| Perturbación del libro final | Prueba 4.10 (árbol del ZIP) | Prueba 4.10.1 (árbol de trabajo) |
|---|---|---|
| B: fecha 1999-12-31, compresión 9 (final `cee8fca7…`) | **73/74**: falla «una modificación posterior… invalidan la correspondencia» con «ficha.json registra otro libro evaluado (1020bb53…) que el acreditado (cee8fca7…)», como en la revisión externa | **78/78** |
| A: la misma fecha y compresión que usa `rezip_inocuo` (final `fa874f1c…`) | **73/74**, el mismo fallo | **76/78**: el caso corregido PASA; fallan las dos pruebas nuevas de reconstrucción (H-3) |

**Conclusión.** La preparación nueva no depende de recuperar el ZIP interno del Excel histórico, y la antigua falla en cuanto los bytes difieren.

### 2.6 Hallazgo de T-1
**H-3 · baja · `personaje_v2/pruebas/test_trazabilidad_v2.py`, `rezip_inocuo` y las dos pruebas nuevas de L.**

- **Causa.** `rezip_inocuo` es una transformación fija e idempotente: fecha 2001-02-03 04:05:06, `compresslevel=1`, `zipfile` de Python. Si el libro reconstruido ya tiene exactamente esa forma, el reempaquetado no cambia los bytes. Entonces `h5 != sha(orig)` es falso y la identidad estricta no puede rechazar, porque ambos archivos son iguales.
- **Prueba.** Con la perturbación A, la batería da 76/78: fallan «reconstrucción sintética con bytes distintos e inocuos…» e «identidad estricta…».
- **Gravedad.** En un entorno real es muy improbable. Pero T-1 trata precisamente de que la batería no dependa del entorno, y el fallo sería un falso negativo de la preparación, no del control.
- **Corrección propuesta (solo en la prueba).** Elegir parámetros que garanticen bytes distintos y conservar la aserción. Por ejemplo, una fecha distinta de la `date_time` de los miembros del original, o reintentar con otro nivel de compresión hasta que cambie la huella.

### 2.7 Avisos de T-1
- **A-T1-1 · `reproducir_T1.py`.**
  - No comprueba los códigos de retorno de `escribir_v63.py`, `verificar_todo.sh` ni `acreditar_libro.py`, ni que exista `acreditacion_libro.json`. Por sí sola, la línea «A … PASA» de «este entorno» no distingue «acreditado y coincide» de «sin comprobante». La batería sí lo acredita: incorporación de cachés PASA, acreditado `1020bb53…`.
  - Su docstring dice «escribe solo en un temporal», pero sus subprocesos (`verificar_todo.sh` llama a `python3` sin `-B`) crearon `personaje_v2/scripts/__pycache__/` con `celdas_v2`, `config_v2` y `v63_xml`. Conviene pasar `PYTHONDONTWRITEBYTECODE=1` en el entorno de los subprocesos.
- **A-T1-2.** En los casos sintéticos de L, `verificar_todo.sh` termina en 1, igual en la 4.10 y en la 4.10.1; la prueba solo exige el código 0 de la preparación. Es anterior y ajeno a T-1.
- **A-T1-3.** Para el ZIP final hay que excluir `personaje_v2/.lo_perfil/` y `v6/scripts/__pycache__/`, que no estaban en el de la 4.10.

---

## 3. Punto 2 · Expediente completo a base 2025

### 3.1 Entradas 2025: valores y fuentes correctos
Comprobado en el PDF español de 2025, con su huella:

| Dato | Valor | Fuente |
|---|---|---|
| Precio de cierre de 2025 | 90,10 € | pág. 97 |
| Acciones emitidas y propias | 35.206.258 y 23.400 | pág. 67 |
| PN 2025 y 2024 | 1.412,878 y 1.309,830 | pág. 10 |
| Pasivos financieros | 196,080 + 66,833 = 262,913 | pág. 10 |
| Caja | 108,352 | pág. 9 |
| EBIT, D&A, BAI e impuesto | 292,068; 132,948; 276,661; 67,320 (24,33 %) | pág. 11 |
| CFO y capex | 380,287; 178,746 + 9,757 = 188,503 | pág. 14 |
| Formulación de las cuentas | 24-feb-2026 | pág. 17 |

**Valores derivados que cuadran:**
- N = 35,182858 y E = 3.169,9755058;
- puente: 262,913 + 6,223 − 108,352 = 160,784, sin restar otra vez el dividendo;
- C24 = 0,1394 (capital empleado medio 1.585,244);
- C33 = 0,364, C34 = 1,62 y C42 = 7,822.

**Coherencia del dividendo.** El extracto dice que el dividendo a cuenta se pagó el 13-feb-2026. Eso es coherente con «con derecho» a 31-dic-2025 y con no restarlo en el puente.

**Fechas separadas.** La fecha económica, la del precio y las acciones (Palancas C45 y C46 = 2025-12-31), la de publicación y la de ejecución (D4 = 2026-11-11) están separadas. Las predicciones vencen el 31-mar-2028, a 16,6 meses de D4.

**Configuración.** Es reproducible y está separada de `fase1_decisiones.json`, que no cambia. Las extracciones AR (`fase1_partes/`), los `texto/CF_*` y los textos de la etapa 1 conservan sus bytes. El caso principal mantiene C46 = 335,4, C47 = 169,7, C48 = 0 y C49 = 4,5 como supuesto heredado, sin sustituirlo por 6,764.

### 3.2 Preparación 2 (reexpresión a 31-dic-2025): legítima, bien hecha y declarada
- **Legítima.** `rellenar_fase1_v63.py` no pisa un valor migrado, y esa regla de producción no cambia. Por eso la reexpresión actúa en la entrada: una copia de la etapa 1 sin esos valores, con los de 2025 por la ruta real (`fase1_v63.json`, o derivados de la Historia en C33). No hay parche del libro de salida ni cambio de código.
- **Bien hecha:**
  - el original queda en `antecedentes/etapa1_original/` (`6aed2116…`, el mismo de todos los expedientes anteriores);
  - la copia (`d8c78658…`) solo cambia `sheet1.xml` y `sheet4.xml`;
  - la revisión comprobó **107 celdas distintas**: las 7 de Análisis más 10 filas × 10 columnas de Control maestro (filas 20, 29, 34, 36, 37, 38, 42, 50, 51 y 54), sin ninguna otra diferencia.
- **Declarada:** en `reexpresion_2025.md`, en la configuración y en el informe del recorrido. La preparación 1 está archivada con su inventario (16/16).
- **Extracto reutilizado.** El de la preparación 1 se conserva; la revisión confirmó que no contiene 409,6; 0,69; 109,4; 7,68; 30-jun-2026; 1S2026; 87,9; 88,7; 259,4 ni LTM. Sus menciones de 2026 vienen del informe anual de 2025 y están identificadas como guía o hechos posteriores.
- **Residuos como valores:** ninguno en las celdas de datos. En textos sí quedan (§3.3).

### 3.3 Restos de la base anterior: hallazgos

**H-1 · media · libro final activo `Vidrala_v63_evaluada.xlsx` (y su volcado `datos_v63.json/md`), filas 41 y 52 de Control maestro; afirmación «Residuos…: ninguno» de `resultados/concordancia_2025*.md` y del informe del recorrido (§1, «sin residuos de la base anterior»).**

Las filas de evidencia de C41 (capitalización) y C55 (acciones) tienen la fuente J actualizada (4.10.1), pero las columnas M y N siguen siendo, **byte a byte, las de la etapa 1 y la 4.6.1**:

| Celda | Texto | Contradice |
|---|---|---|
| M41 | «88,70 × 34,185 mm (35,206 emitidas − ≈1,021 autocartera, restada una vez) = 3.032,2 mm.» | C41 = 3.169,9755058 |
| N41 | autocartera de informes semanales de 2026; «3.029,7»; «proveedor 3.122,8» | C41 = 3.169,9755058 |
| M52 | «35,206 − ≈1,021 = 34,185 mm» | C55 = 35,182858 |
| N52 | «si se ejecuta la liberada 2026, ≈35,89 mm» | C55 = 35,182858 |

- **Qué es.** Es la capitalización antigua presentada como cálculo de la celda que hoy vale otra cosa, sin identificar en el libro.
- **Dónde se menciona.** La fase A y el informe del recorrido (§4) solo dicen, de forma genérica, que «las Observaciones o documentos de … C41 … y C55 conservan menciones de 2026 como contexto».
- **Por qué no lo detecta la concordancia.** `concordancia_2025.py` solo busca textos de 2026 en las filas reexpresadas (`filas_rx`) y en las columnas G, J, L y N.
- **Efecto numérico:** ninguno. Son textos y el motor usa los valores.
- **Por qué exige corrección.** El criterio 2 de §6 pide «ausencia … de la capitalización antigua como datos del caso», y la concordancia lo da por cumplido sin haberlo comprobado en esas filas.
- **Corrección mínima:**
  - ampliar el barrido de la concordancia a todas las filas de evidencia de las celdas que fija la configuración (20, 38, 41, 52 y 54) y a las columnas M y N;
  - identificar M41, N41, M52 y N52 por celda como restos de la etapa 1;
  - corregir el «ninguno» y la frase del informe del recorrido.
- **Corrección completa** (para el mecanismo general de cambio de base): incluir M y N de las filas 41 y 52 en la copia de la etapa 1. Obligaría a regenerar el libro, el material y la auditoría.

**H-2 · baja · `Vidrala/fase1_metadatos.json` y `Vidrala/fase1_v63.json` (`_notas`), con su ruta `scripts/preparar_ensayo_2025.py`.**
- **Qué queda.** Dos notas de la 4.6.1 contradicen los valores activos:
  - «Rentabilidad del bono: Trading Economics 2 nov 2026 … no se obtuvo dato del 3 nov.»;
  - «Acciones: … se usa el promedio ponderado/emitidas 35,206 M (autocartera de 23.400 acciones ignorada por inmaterial).»
- **Por qué se repondrían.** `preparar_ensayo_2025.py` solo filtra la nota que contiene «Bolsamanía», así que una regeneración las volvería a poner. Eso es justo lo que §4.2 pide evitar para N 35,206 y la rf de noviembre de 2026.
- **Alcance.** No llegan al libro ni a las salidas.
- **Corrección:** filtrarlas o marcarlas como antecedente en la ruta, y que la concordancia busque también en `_notas`.

### 3.4 Antecedentes, estado propio y nada heredado: bien
- **Heredados de la 4.6.1** en `antecedentes/heredados_4_6_1/`: 75 archivos, todos iguales al original y sin ninguno sin inventariar, con fases, celdas, libros, resultados, `precio.json`, gramática, referencias, material, auditorías, cierres, `historial_cierres` y estado.
- **Expedientes anteriores.** Todos, incluida la 4.10, conservan sus bytes frente al ZIP; ningún registro de publicaciones ajeno cambió.
- **`estado_pipeline.json` propio.** Inicio a las 21:53:40, contadores a 0 y una sola solicitud (la nueva). `auditorias_conocidas.json` solo registra la auditoría nueva, que no coincide con ninguna auditoría del árbol.
- **Reinicio de la preparación 2.** El estado de la preparación 1 (paso 6, contadores a 0, solo el extracto consumido) está archivado: recrear el estado no eludió ningún límite (ver A-6).

### 3.5 Fases A, B y C: revisadas, no copiadas
| Fase | Textos largos idénticos a la 4.6.1 | Citas a ES_2025 (ensayo / 4.6.1) |
|---|---|---|
| A | 21 de 132 (etiquetas de descalificadores y citas literales de la etapa 1 en `herencia.*.etapa1`) | 175 / 0 |
| B | 2 de 104 | 126 / 0 |
| C | 27 de 262 (nombres de sesgos y de datos) | 100 / 0 |

- **Fase A.** Detectó los siete datos de 2026, el motivo de la preparación 2.
- **Fase B.** Justifica cada palanca con hechos de 2025.
- **Fase C.** Hizo dos turnos, reescribió en el segundo B101, B102 y C104 sin datos de 2026, y redecidió C93 y C103.

### 3.6 Recálculo, escalera, acreditación y correspondencia de huellas: bien
- **Recálculo forzado:** `resultados.json` sale de `recalc/`, sin fallos.
- **Valores por acción.** Coinciden con valor_final/N: 1.887,90 / 2.559,22 / 3.041,34 ÷ 35,182858.
- **r_op = 0,08699, recalculada** con la fórmula vigente: (r·E + kd·(1−t)·D)/(E+D). No se impone 0,09.
- **Escalera.** P* = 66,5206 (reproducido aparte), ponderado 71,6650, zona caro.
- **Libro final.** Las cachés del libro final coinciden con la copia recalculada en las **16.411** celdas con valor. La cadena es `73f06584…` (antes de las cachés, ÍNTEGRO) → `da053c79…` (final, ÍNTEGRO). El comprobante nombra ese archivo y `motivo_acreditacion_libro` = None.
- **Correspondencias:**
  - ficha: `libro_evaluado` = `da053c79…` y `libro_entrada` = `d6c2518f…`;
  - material `e60b272b654aeece`: 20/20 huellas actuales, con ambos libros, el comprobante y la ficha y el informe provisionales;
  - `cierre_vigente.json`: ficha `f2e2d74c…`, informe `5cc2a9fa…`, auditoría `6703c396…` y solicitud SA-433ea31c3f7fc4bd;
  - resumen: 90,1 / 53,66 / 66,52 / 71,66 · caro · esperar · APROBADO.

### 3.7 Auditoría, cierre y publicación: bien
- **Auditoría.** Se identifica como **interna** en su primera línea. Tiene 16 puntos, todos en PASA y con contenido material: repitió las citas, comparó la herencia por script y revisó la mecánica. Contiene «Solicitud de auditoría: SA-433ea31c3f7fc4bd», «Material auditado: e60b272b654aeece» y un solo «Veredicto: APROBADO».
- **Vigencia.** `veredicto_auditoria` y `motivo_vigencia` la dan por vigente.
- **Publicación.** Solo en `2026-11_Vidrala_ensayo_4_10_1/resumen_v2.csv`, y `Vidrala/publicaciones_resumen.json` registra ese único destino, con el material auditado.
- **Campos humanos.** Los de las propuestas siguen vacíos (`decision`, `fecha` y `decidido_por` a null).

### 3.8 P3, N4, provisión de personal y N1–N3/P-M1: bien
Ninguno se declara resuelto ni se confirma un cero. La fase C evalúa la materialidad con cifras que cuadran:

| Abierto | Materialidad evaluada | Comprobación |
|---|---|---|
| N4 | 0,028 €/acción por cada millón; harían falta unos 117 mm para mover el precio de Sí un 5 % | 3,33 ÷ 0,0284 |
| Provisión de personal | 0,18 €/acción, el 0,27 % | 6,223/N |
| P3 | nula en el motor B; −0,7 % en el peor caso, por C63 | — |

**Doble cómputo.** La fase C explica bien su límite: el motor B proyecta desde el EBIT, así que que las aportaciones vayan en el CFO no prueba nada.

**N1–N3 y P-M1.** El código no cambia y no se integran.

### 3.9 Comparación con C1 y variante de precisión: la atribución es correcta
La reejecución de la revisión reproduce byte a byte las copias y la tabla:

| Variante | Resultado |
|---|---|
| C1_control (referencia + C41/C55) | 70,4665 / 65,6645: reproduce C1 |
| ensayo con las palancas de C1 | **exactamente C1** |

**Atribución:**
- entrada y convención = 0;
- juicio = +1,997 en el NORMAL, +1,198 en el ponderado y +0,856 en el precio de Sí, todo por Palancas!C15 (0,18 → 0,185);
- precisión de C46/C47 = 0: el FCF base pasa de 161,2 a 161,245, pero el motor B no lo usa.

**Matiz.** «Entrada» también absorbe que los juicios de la fase A con efecto en el valor (Palancas C5–C10, C62) coinciden con C1: ninguna de esas celdas aparece entre las 21 distintas.

### 3.10 Conclusión: coherente
- **Regla aplicada.** C11 = Sí, C12 = Sí y C13 = No, por lo que la hoja dice «DESCARTADA POR FILTRO PABRAI». Es el «caso típico» de la regla 4 del personaje: escribe Vigilar con el precio de Sí.
- **Combinación admitida.** Concluido, esperar y `no_procede` es una combinación que admite `FUNDAMENTO_C104`.
- **NO LISTO admitido.** «NO LISTO · evidencias incompletas (2 no verificables)» está admitido con la fase C escrita.
- **Lo que se señalaba como posible omisión está tratado:**
  - **Tipo impositivo.** `Historia!C52` no es un 20 % fijo: es la fórmula de la plantilla, la media 2021–2025 del tipo efectivo (20,03 %). La sensibilidad al 24,33 % de 2025 se calcula (62,71, −5,7 %) y se eleva como decisión humana (D-TAU-HOJA). No cambia ni la zona ni la acción.
  - **Base del margen C8.** La regla está fundamentada, pero su cifra no (C49 = 16,9 % mezcla perímetros). Se acota entre 16,9 % y 19,9 %, con un efecto de 0 a +2,7 %, y se propone pedir los datos por segmento (D-C8-MARGEN).
- Ningún extremo de ambas sensibilidades acerca el precio de Sí a 90,10.

### 3.11 Avisos y límites del expediente (no exigen corrección en esta entrega)
- **A-1 · dónde interviene la rf (§4.2.3), documentado a medias.** El informe del recorrido solo dice que la rf «no mueve la valoración». La revisión encontró que la rf (C57) interviene en cuatro sitios:
  - la r mínima (`Diagnóstico V6!C17` = rf + Riesgo país C3 + Palancas D34 → C18, PASA);
  - el texto de D57;
  - las **referencias mecánicas de g**;
  - la regla G3 de la gramática.

  Con rf = 0,0285, la referencia del BUENO es mín(0,03; 0,03; 0,0285) = 0,0285, que `ajustar_lista` redondea al valor más cercano: **0,03, por encima de la rf**, contra la orientación E1. Es comportamiento de producción conforme al Anexo B («ajustado a la lista»), y con la rf de la 4.6.1 (0,0329) no se manifestaba. La fase B lo vio y eligió 0,025, así que no tiene efecto. Convendría documentarlo y proponer redondear hacia abajo cuando el tope sea la rf; sería un cambio de producción, fuera de esta entrega.
- **A-2 · rf no verificable.** El PDF del Bundesbank no se conservó (declarado), así que la rf de 2,85 % no se puede verificar desde el paquete. La revisión tampoco la consultó.
- **A-3 · fase A activa revisada, no hecha desde cero.** Es una revisión dirigida de la fase A de la preparación 1, del mismo ensayo: 115 de 132 textos iguales, 16 cambiados en las celdas reexpresadas y 1 añadido. Está declarado («revisada sobre el libro de la preparación 2») y es proporcionado al cambio de entradas.
- **A-4 · prompt del extractor.** El prompt de extracción de la preparación 1 le dio al extractor el `datos_v63.md` con los datos de 2026 («no lo repitas»). El extracto resultante está limpio (§3.2).
- **A-5 · coincidencia de las palancas con la 4.6.1.**
  - Coinciden 11 de 12 valores y desviaciones; solo cambia el margen del NORMAL. Las referencias mecánicas son las mismas.
  - La fase B no recibió la fase B de la 4.6.1. Pero el extracto dice que «reutilizó hechos» comprobados de la 4.6.1, y la fase C leyó la fase C del antecedente («sin copiarla», declarado).
  - Los textos son nuevos y la convergencia es plausible. La autocomprobación solo trata el anclaje frente a la etapa 1, no frente a las palancas de la 4.6.1; queda como observación para la revisión externa.
- **A-6 · redacción sobre los contadores.** «Contadores: no se reiniciaron» es impreciso: el estado se recreó en la preparación 2 y el de la preparación 1, con todo a 0, quedó archivado. Ningún límite se eludió.
- **A-7 · precio objetivo por acción de 2025.** `decision.precio_objetivo` = 66,52 es por acción de 2025, antes de la liberada de 2026 de 1 por cada 20. La ficha dice «valor a 31-dic-2025» en `cambiaria_de_cubo`, pero no junto al precio objetivo. Compararlo con cotizaciones de 2026 exige ajustarlo.
- **A-8 · marca de la copia de la etapa 1.** La copia conserva el nombre `etapa1/Vidrala_evaluada.xlsx` sin ninguna marca en la carpeta; sí está documentada en la configuración y en `reexpresion_2025.md`.
- **A-9 · redacción de D-TAU-HOJA.** Dice que C52 es «la media de la serie», pero es `AVERAGE(H10:L10)`, la de 2021–2025.
- **A-10 · celdas residuales menores:**
  - las filas 20, 38 y 54 de Control maestro quedan con G (periodo) vacío; la fecha del precio está en N38;
  - D4 sigue escrita como texto (aviso V31, heredado);
  - C38 (Simply Wall St, 08-oct-2026) solo alimenta C39 y C87, informativos, y se presenta como contexto posterior no usado.
- **A-11 · huellas en el texto del informe.** `informe.md` no las repite; se liga por `cierre_vigente.json`, que es el diseño de producción.
- **A-12 · pendiente del ejecutor.** No forma parte de los dos puntos revisados: VERSION, CONTINUIDAD, CAMBIOS, el manifiesto, `comprobar_entrega_4_10_1.py`, los registros y el ZIP estaban en curso o sin actualizar durante la revisión. `comparar_con_C1.py` no borra su directorio temporal.

---

## 4. Resumen de hallazgos que exigen corrección

| Id | Severidad | Archivo | Prueba | Corrección |
|---|---|---|---|---|
| H-1 | media | `Vidrala/Vidrala_v63_evaluada.xlsx`, Control maestro M41, N41, M52 y N52 (y `datos_v63.*`); `resultados/concordancia_2025*.md`; `INFORME_RECORRIDO_4_10_1.md` §1 | M41 «88,70 × 34,185 … = 3.032,2 mm» frente a C41 = 3.169,9755058; M52 «34,185 mm» frente a C55 = 35,182858; la concordancia dice «ninguno» porque no explora esas filas | ampliar el barrido (filas 20, 38, 41, 52 y 54; columnas M y N); identificar los restos por celda; corregir las afirmaciones. Lo ideal, en el mecanismo general, es limpiarlas en la copia de la etapa 1 |
| H-2 | baja | `Vidrala/fase1_metadatos.json`, `Vidrala/fase1_v63.json` (`_notas`); `scripts/preparar_ensayo_2025.py` | notas «Trading Economics 2 nov 2026» y «35,206 M … autocartera ignorada»; el filtro solo quita «Bolsamanía» | filtrarlas o marcarlas en la ruta; que la concordancia mire `_notas` |
| H-3 | baja | `personaje_v2/pruebas/test_trazabilidad_v2.py` (`rezip_inocuo` y las dos pruebas nuevas) | con un libro final que ya tiene la forma de `rezip_inocuo`, la batería da 76/78 (§2.5, perturbación A) | garantizar bytes distintos (otra fecha u otra compresión si coinciden) sin rebajar la aserción |

Ninguno afecta a los valores (71,66 / 66,52 / 53,66), al estado (concluido), al cubo (Vigilar) ni a la acción (esperar).
