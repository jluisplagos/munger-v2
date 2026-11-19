# Plantilla V6.3.1 F1 del motor A

Escrita el 18-nov-2026 por el agente autor de la plantilla (Claude, Opus) en la rama `f1/plantilla-v631`, desde `f1/implantacion` @ `24e9a30`.
**Sin revisión independiente todavía**: la hará otro agente. Punto de control (guion, referencia, verificador y prueba A0) en `a4feae1`;
segunda mitad (selección, declaración en el libro, oráculo en `motor_a_f1.py`, validación A1/A2, sintético NIIF 16 y H10/H11/H12 de la
revisión de F1-IMPL) en los commits siguientes (§5–§8).

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** La V6.3, su referencia, sus ejemplos y los expedientes
hechos con ella **no cambian**.

## 1. Qué es y qué no es

**Hecho.** La V6.3.1 F1 es la V6.3 con un solo cambio de modelo: la amortización que f (Historia C58), el ancla de S2C (C53) y, a través
de f, el terminal del Motor tratan como reposición (D_X) se calcula con el **perímetro F1 de la reinversión** que declara la persona
(decisiones F1 del 17-nov-2026; E2–E4 de la especificación F1):

| Perímetro (Historia C85) | D_X por año (fila 88) | Igual que |
|---|---|---|
| vacío o `A0_total` | D&A total (fila 8) | la V6.3 |
| `A1_sin_ROU` | D&A total − D&A de derechos de uso (fila 86) | — |
| `A2_propio` | D&A total − D&A de derechos de uso − PPA (fila 87) | — |

Los identificadores son los de `personaje_v2/scripts/motor_a_f1.py` (`PERIMETROS`).

**Qué no es.** No elige ningún perímetro: vacío es A0, que es la V6.3. No calcula `A3_estimado` (R estimada), N1 ni los términos
explícitos (transición, compras): con ellos la capa F1 tiene que seguir bloqueando (`F1-LIBRO`). No cambia las series publicadas (fila 8,
FCF base, Análisis C46–C52) ni las entradas registradas.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `entregables/Plantilla_V6.3.1_F1.xlsx` | La plantilla. SHA-256 en `referencia/SHA256_entregables_V6.3.1_F1.txt` y en el manifiesto. **No va en Git** (los `.xlsx` están excluidos): se reconstruye desde la V6.3 de la base con `python3 -I scripts/construir_v631_f1.py ../entregables/Plantilla_V6.3.xlsx entregables/Plantilla_V6.3.1_F1.xlsx` y tiene que dar la misma huella. |
| `referencia/referencia_V6.3.1_F1.json` | Referencia de integridad nueva (regenerada con la C53 de la revisión, §8): 10.975 fórmulas, 5.140 celdas fijas, 52 validaciones, 13 partes del paquete (idénticas a las de la V6.3). |
| `scripts/construir_v631_f1.py` | La construye a partir de la V6.3, que no se modifica. Determinista: dos ejecuciones dan el mismo SHA-256. |
| `scripts/verificar_v631.py`, `generar_referencia.py`, `inventario_entradas.py`, `add_sliders.py` | Copias de los de la V6.3: `add_sliders.py` idéntico; en `verificar_v631.py` y `generar_referencia.py` cambia solo el docstring; el inventario añade Historia C85, C86:L87 y M85:S87. |
| `scripts/trasladar_entradas.py`, `comparar_libros.py` | Copias de las de la V6.4.1, adaptadas (sin hoja de configuración; todas las columnas; solo se excluyen las etiquetas de versión y la sección nueva). |
| `scripts/probar_v631_f1.py` | Pruebas `estructura` (sin LibreOffice) y `a0` (con LibreOffice). Resultados en `pruebas/`. |

## 3. Cambios de fórmula frente a la V6.3

- **Historia, sección nueva (filas 84–90).** C85 perímetro (lista de validación); C86:L86 D&A de derechos de uso y C87:L87 PPA por año
  (≥ 0; vacío = desconocido, no cero); M85:S87 sus fuentes; C88:L88 D_X; C89 perímetro efectivo («no reconocido» con un texto fuera de la
  lista: D_X y f quedan vacías); A90 nota.
- **Fila 30** (y con ella la 31): `capex − D_X + circulante`. Con A0, D_X es el valor de la fila 8: la misma operación.
- **C58 (f), C76 (conciliación de f) y C53 (ancla de S2C):** `=IF($C$89="A0_total", <fórmula literal de la V6.3>, <fórmula con D_X>)`.
  Con A1/A2: la reinversión es la de la fila 30; f exige D_X en todos los años de la ventana (vacío ≠ 0) y el ancla, los cinco años H–L
  de **todo** el denominador: capex (fila 12), adquisiciones (13), circulante (14) y D_X (88), con 0 explícito si no los hubo (E4, confirmado
  por la revisión de la V6.3.1; la V6.3 admite tres años y cuenta los vacíos de las filas 13 y 14 como 0, y su rama A0 no cambia).
- **Motor E205 (validación V05 del motor A):** al final, tres causas nuevas, que solo pueden saltar con A1/A2 o con un texto no reconocido:
  perímetro no reconocido (INV), D_X vacía en la ventana (INC) y D&A de derechos de uso + PPA mayor que la D&A total (INV).
- **Etiquetas de versión:** Panel A1, Análisis A1, Guía V6 A1 y Control maestro A3.

## 4. Pruebas ejecutadas (hechos)

| Orden (desde `v6/v631_f1/scripts/`) | Resultado literal |
|---|---|
| `python3 -I probar_v631_f1.py estructura` | `21/21 comprobaciones V6.3.1 F1 (estructura) PASAN` |
| `flock /home/user/e_work/libreoffice.lock python3 -I probar_v631_f1.py a0 <carpeta nueva fuera del repo>` | `22/22 comprobaciones V6.3.1 F1 (a0) PASAN` |

- *estructura*: reconstrucción con el mismo SHA-256; la V6.3 sin cambios; la referencia nueva difiere de la de la V6.3 exactamente en las
  celdas del §3 (ninguna fórmula o celda fija de la V6.3 quitada; formato condicional, nombres y partes del paquete idénticos); con A0,
  C53, C58 y C76 contienen literalmente la fórmula de la V6.3; el verificador nuevo acepta la plantilla y rechaza una mutación de D_X
  (C88 = C8); el de la V6.3 rechaza la V6.3.1.
- *a0*: libro de Elis (`Elis_v63_evaluada.xlsx`, d2593777…, el que concilió el frente E) y los tres ejemplos de la V6.3 (Empresa X, ABB,
  Hermès). Las entradas se trasladan a la V6.3 y a la V6.3.1 por la misma vía y los dos libros se recalculan con LibreOffice: con el
  perímetro **vacío** y con **`A0_total`** escrito, **0 celdas distintas** de 39.846 en las once hojas, con **igualdad exacta**
  (tolerancia 0), excluidas solo las cuatro etiquetas de versión y la sección nueva. Además: el libro V6.3.1 con las entradas es ÍNTEGRO
  frente a su referencia; con A0, D_X = D&A; el libro de Elis tal cual, recalculado, coincide con la V6.3 con sus entradas trasladadas
  (el traslado es fiel); los orígenes no cambian.

## 5. Uso en el pipeline (hechos)

- **Selección explícita:** `personaje_v2/config_v2_v631_f1.json` (= `config_v2.json` salvo la plantilla, `version_config` y el resumen
  `resumen_v2_v631_f1.csv`). Nunca es la de por defecto. `seleccion_plantilla.py`: `V631 = "V6.3.1 F1"`, `es_v631`, `registra`. Con la
  V6.3.1 la primera ejecución escribe `plantilla_activa.json` (como la V6.4); un expediente V6.3.1 no se ejecuta con la V6.3 ni con la V6.4,
  uno V6.3 ya empezado no se ejecuta con la V6.3.1, y una `configuracion_economica.json` se rechaza. `cierre_v2.nombre_resumen` y
  `ficha.esquema.json` conocen la versión; `ficha.py` no escribe el bloque de configuración económica para la V6.3.1 y añade
  `motor_a_f1.libro_v631_f1`.
- **Declaración al libro:** `personaje_v2/scripts/f1_libro_v631.py aplicar` escribe en Historia C85 el perímetro (solo `A0_total`,
  `A1_sin_ROU`, `A2_propio`; con `A3_estimado` o sin declarar queda vacío = A0), en C86:L87 las magnitudes de las series (signo ×
  valor_fuente, con la misma lectura que la capa; una entrada inválida queda vacía) y en M85:M87 la procedencia. Reescribe siempre las
  tres filas. El pipeline lo llama en el **paso 2**, tras `rellenar_fase1_v63.py`, solo con la V6.3.1.
- **Oráculo (`motor_a_f1.py`, cambio aislado en `_libro_v631`, `_replica_v631`, `_f_vacia_v631` y cuatro líneas en `evaluar`):** con un libro
  V6.3.1, `F1-LIBRO` deja de bloquear solo si el perímetro efectivo (C89) es el declarado, las series del libro son las declaradas (vacío
  ≠ 0), D_X, f (10⁻¹²), el ancla (10⁻⁹) y los flujos del Motor (tantos como escenarios con palancas tenga la capa: 33 en el paso 12, 0 en el
  paso 7) coinciden con la capa, y no hay N1 ni términos explícitos. Cualquier diferencia bloquea. La réplica (`F1-REPLICA`) contrasta
  en un libro A1/A2 las ecuaciones con la D_X del propio libro y D_X con sus filas 8, 86 y 87. Con un libro V6.3 nada cambia (`F1-LIBRO`
  límite declarado). Si la declaración cambia después del paso 2, el libro deja de corresponder y la capa bloquea (P8).
- **A3_estimado** no lo calcula el libro: sin estimación la capa termina en `pendiente_de_datos` (V-F1d); con estimación, `F1-LIBRO` bloquea
  (`no_entregable · límite del modelo`). Tampoco N1 ni los términos explícitos.

## 6. Correcciones H10, H11 y H12 de la revisión de F1-IMPL (en `motor_a_f1.py`)

- **H10 · términos explícitos, vacío no es cero** (`_terminos_incompletos`): compras de reposición con importes por año exigen los años
  1–10 y el 11 (o la proporción de las ventas); con `ancla_s2c_excluye_terminos`, los importes históricos H–L (X^v, 0 explícito); la
  transición como término, sus importes históricos H–L. El año 11 cobra el importe declarado (antes, 0) y X^v usa los importes históricos
  de las compras. Los términos siguen bloqueados por `F1-LIBRO` (no están en el libro).
- **H11:** `F1-C49` y `F1-ROU-HISTORIA` ya estaban (primera ronda). Se añade el registro obligatorio de «sin transición conocida».
  No se hizo el registro de la normalización (resto de H9: N1 sigue bloqueado por `F1-PARAM`).
- **H12 · `F1-SERIES`** (`_guarda_fuentes_series`, como T9): para cada año de la D&A de derechos de uso y de la PPA, la cifra publicada
  (`literal`, p. ej. «(149,5)») tiene que ser `valor_fuente` con su signo, y la fuente (`archivo`: texto con marcas «[PDF PAGE n]» dentro del
  expediente, o un PDF con `archivo_texto`) tiene que existir, tener la página citada y contener esa cifra en ella. Vacío o no examinable →
  INCOMPLETO; signo o cifra distintos, página inexistente o cifra ausente → DATOS INVÁLIDOS. `evaluar(..., carpeta=None)` no examina y
  bloquea; el CLI y el pipeline pasan la carpeta. BLOQUEA si nada más bloquea; si otra guarda ya bloquea, AVISA y no cambia el estado.
  **No es la verificación de entradas** (sin revisor, sello ni contraste con el PDF): las series siguen fuera del universo de
  `verificacion_entradas.py`.
- Para estas pruebas se ajustaron `test_motor_a_f1.py` (las series sintéticas llevan `literal` y `archivo`; tres casos pasan la carpeta con
  una fuente sintética; el caso de transición lleva sus importes históricos) y `prueba_pipeline_f1.py` (la fuente sintética de las series).

## 7. Pruebas de la segunda mitad (hechos; resultados literales)

| Orden | Resultado |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_v631_f1.py` (selección, aplicación, oráculo; sin LibreOffice) | `21/21 pruebas V6.3.1 F1 (sin LibreOffice) PASAN` |
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1.py` | `155/155 pruebas del motor A F1 (4.15) PASAN` (142 + 13 de H10/H11/H12) |
| `flock … python3 -I v6/v631_f1/scripts/probar_v631_f1.py f1 <carpeta nueva>` | `32/32 comprobaciones V6.3.1 F1 (f1) PASAN` (`pruebas/resultado_f1.md`) |
| `flock … python3 -B v6/v631_f1/scripts/prueba_pipeline_v631.py` | `6/6 pruebas de la V6.3.1 F1 en el pipeline PASAN` (`pruebas/resultado_pipeline_v631.txt`) |
| `flock … python3 -B …/f1_impl/scripts/prueba_pipeline_f1.py` (desde `personaje_v2/`) | `7/7 pruebas del gancho F1 del pipeline PASAN` (`pruebas/resultado_prueba_pipeline_f1.txt`) |
| `flock … bash verificar_paquete.sh completa` sobre una copia limpia de `f4be12b` (manifiesto 7811 archivos) | `RESULTADO GLOBAL: PASA`, código 0 (`pruebas/verificacion_completa_f4be12b.txt`): motor A F1 155/155, gancho 7/7, V6.4 199/199, cierre 55/55, resumen 45/45, sintética con los nombres de la línea de base… |

- *f1*: Elis con A1 y A2 recalculado por LibreOffice: f, C53 y los 33 flujos = E9 de `datos/elis_cifras_f1.json` (f 0,0126242253232846 y
  −0,00611860174416477; C53 2,4453316953317 y 1,61252430330525; desviación máxima de los flujos 1,0·10⁻¹²); año 11 A1 − A0 = 205,363093;
  capa = libro; `F1-REPLICA`, `F1-LIBRO` y `F1-SERIES` no saltan (las series con las páginas del texto del expediente de Elis, solo
  lectura). Vacío ≠ 0 (ROU 2024 o PPA 2025 vacías → f vacía, V05 INCOMPLETO, capa en `pendiente_de_datos`; ROU 2021 vacía → f igual y
  C53 vacía). C85 no reconocido → V05 DATOS INVÁLIDOS. Bloquea si el libro no corresponde (otro perímetro, otra serie, libro V6.3).
  Sintético NIIF 16 pesado (Empresa X: D&A de derechos de uso 75 % de la D&A con su principal en el FCF base, PPA 15 %): libro = capa en
  A0, A1 y A2 e identidades de f y C53 con los valores del libro.
- *pipeline*: P6 empresa sintética con arrendamientos y A1 declarado con la V6.3.1 → `plantilla_activa.json` V6.3.1, F1 utilizable,
  gancho en los pasos 7 y 12, `concluido`, resumen en `resumen_v2_v631_f1.csv`; P7 la misma con la V6.3 → paso 7 `no_entregable ·
  límite del modelo` (`F1-LIBRO`); P8 declaración cambiada y `--desde 7` → `F1-LIBRO` bloquea.

## 8. Primera ronda de revisión independiente de la V6.3.1 (`4928fc9`, CORRECCIONES acotadas) y lo que se corrigió

| Hallazgo | Corrección | Prueba |
|---|---|---|
| V631-1 · R2-1 abierto: `--reiniciar --desde 13` con el resultado F1 borrado llegaba a `concluido` | `pipeline.py` rechaza `--reiniciar` junto con `--desde` (código 2), después de retirar una aprobación que ya no corresponde al material; al reanudar con `--desde ≥ 7` sin el motor en el estado, lo repone desde `fase_a.json`; `vigencia()` toma el motor de `fase_a.json` y «motor desconocido» con F1 exigido no es «no es el A» | `prueba_pipeline_v631.py` P9 (R21a, R21b, R21c); `test_v631_f1.py` (vigencia y rechazo) |
| V631-2 · `F1-SERIES` aceptaba subcadenas, otro ejercicio y fuentes sin huella | la cifra se busca como cifra completa; con `fila`, en esa línea y en la columna cuyo encabezado de ejercicio (alineado en el texto con marcas) es el año; `fuentes_series` liga cada `documento` a un `archivo` **dentro de la carpeta del expediente** con su `sha256` (y `archivo_texto`/`sha256_texto` para un PDF); sin `fila` o sin encabezado alineado, la columna queda **pendiente** (no bloquea F1; la aptitud por entradas la bloquea el universo, V631-3) | `test_motor_a_f1.py` «V631-2» (8); `probar_v631_f1.py f1`: E1 sobre el texto real de Elis, y las 10 cifras de Elis con la columna comprobada |
| V631-3 · la huella y la aptitud por entradas no veían las filas 85–87 | `entradas_economicas.instantanea` incluye Historia C85 y C86:L87 en los libros V6.3.1 (marca de A84): A1 y A2 tienen huellas distintas, y las celdas entran en el universo de `verificacion_entradas.py`, así que sin su verificación la aptitud por entradas es «no». Los libros V6.3 y V6.4 no cambian de huella | `test_v631_f1.py` «V631-3» (3) |
| E4 y V631-5 · ancla con A1/A2 | C53 (rama A1/A2) exige las filas 12, 13, 14 y 88 numéricas en H–L; la capa también (para todos los perímetros) | `probar_v631_f1.py f1` (circulante de 2021 vacío) |
| V631-4 · con A0 el oráculo bloqueaba donde la V6.3 no | con A0, C53 se contrasta solo si la capa lo calcula | `probar_v631_f1.py f1` (capex de 2021 vacío) |
| V631-8 (P6) | P6 exige `concluido` | `prueba_pipeline_v631.py` |

**Pruebas de esta ronda (resultados literales; plantilla reconstruida `eaece01a…`, porque cambió C53):** `test_v631_f1.py` `28/28 … PASAN` ·
`test_motor_a_f1.py` `163/163 … PASAN` · `probar_v631_f1.py estructura` `21/21 … PASAN` · `flock … probar_v631_f1.py a0` `22/22 … PASAN`
(0 celdas distintas, igualdad exacta) · `flock … probar_v631_f1.py f1` `35/35 … PASAN` · `flock … prueba_pipeline_v631.py` `9/9 … PASAN` ·
`flock … prueba_pipeline_f1.py` `7/7 … PASAN`. `flock … bash verificar_paquete.sh completa` sobre una copia limpia de `0917de9`: `RESULTADO GLOBAL: PASA`, código 0
(`pruebas/verificacion_completa_0917de9.txt`).

**No corregido (declarado):** V631-6 (el oráculo contrasta valores en caché: en el pipeline lo cubren el recálculo forzado y
`verificar_v631.py` en el paso 12; a mano sobre un libro de origen desconocido, no); V631-7 (rótulos de A30/A76; la nota de A90 explica
D_X); el rótulo F1 «utilizable» que conserva la ficha del control 2 de V631-8; las tres pruebas nuevas siguen sin registrar en
`verificar_paquete.sh`; el tercer caso del §2 de la revisión (una fila 8 que ya excluye la ROU: A1 la restaría dos veces) no tiene guarda
propia (lo cubre solo la verificación de la fila 8 y de las series).

## 8 bis. US GAAP (18-nov-2026) · la plantilla no cambia

**Hecho.** La reparación F1 · US GAAP (`personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_usgaap/F1_USGAAP.md`) no toca
la plantilla, su referencia ni su verificador (`eaece01a…`): los expedientes V6.3.1 en curso siguen ejecutándose con sus huellas.
- Con US GAAP, `f1_libro_v631.py aplicar` escribe en la **fila 86** la amortización de derechos de uso que está dentro de la fila 8: la de
  los arrendamientos financieros (`da_rou`) más la de los operativos declarada dentro de la fila 8 (`da_rou_operativo`). No lleva la de los
  financieros tratados como deuda (D-WM) ni la declarada fuera de la fila 8. Con NIIF, nada cambia.
- El libro **calcula tal cual** los tramos no publicados (D-US1) o fuera de las filas, la amortización operativa dentro de la fila 8 y los
  dos tramos dentro de la fila 14 (D-US2 bis: su valor cuenta el coste contable; la capa enseña cuánto cambiaría contando los pagos).
- Lo que el libro **no** calcula con US GAAP: retirar del circulante el importe de **un solo** tramo del arrendamiento operativo que esté
  dentro de la fila 14 (la capa lo calcula y `F1-LIBRO` bloquea) y excluir del puente del motor B el pasivo por arrendamiento operativo
  (`F1-US-PUENTE`).
- Una declaración mal formada no hace fallar `aplicar`: la serie se lee como vacía y la capa lo dice en el paso 7 (`F1-DECLARACION`). Una
  nota de texto dentro de `series`, en una clave que no es el nombre de una serie, se admite y no cambia ninguna celda (cierre de la ronda 2).
- Prueba sobre el libro real recalculado: `f1_usgaap/scripts/probar_libro_v631_usgaap.py` (16 comprobaciones).

## 9. Preguntas para el revisor y límites

1. **E4 con A1/A2:** confirmado por la revisión (cinco años H–L de todo el denominador; aplicado en §8).
2. `F1-SERIES` solo cubre la D&A de derechos de uso y la PPA (no `pagos_arrendamiento`, que solo da la sensibilidad (1b)); avisa sin cambiar
   el estado cuando otra guarda ya bloquea. La columna se comprueba por alineación en el texto «-layout»: una tabla con otra maquetación la
   deja pendiente (no la inventa). Una fuente fabricada dentro del expediente con su huella pasa `F1-SERIES`: la cubre la verificación de
   entradas (revisor y sello), que sigue siendo condición de la aptitud.
3. La PPA declarada a cero no tiene contraste en la Historia (no hay fila): `F1-SERIES` exige su cifra, su página y su columna, nada más.
4. Fuera de alcance: D_X y sus series en el control de evidencias del libro (Control maestro); el resto de H9 (registro y alcance de N1);
   `test_v631_f1.py`, `probar_v631_f1.py` y `prueba_pipeline_v631.py` no están registrados en `verificar_paquete.sh`.
5. **No comprobado:** Excel real (todo el recálculo es LibreOffice); `regresion_elis_f1.py` no se volvió a ejecutar (escribe en los
   resultados de F1-IMPL).

## 10. `F1-SERIES` con escala y ceros sin cifra (18-nov-2026, rama `f1/series-escala`)

**Hecho.** El examen de Jumbo (`2026-11_examen_universo/jumbo_d`) no tenía salida honrada en `F1-SERIES`: Jumbo publica en euros enteros
(el modelo trabaja en millones) y su PPA es cero sin cifra impresa (no hay intangibles de combinaciones). La revisión de `f1/usgaap` (R1-2)
encontró el mismo hueco con un cero impreso como «—» (10-K de Zoetis). Cambio en `motor_a_f1.py` (`leer_serie`, `_guarda_fuentes_series`
y las funciones nuevas `_escala_serie`, `_clase_cero` y `_cero_en_pagina`):
- `escala` opcional en cada año de una serie: «unidades», «miles» o «millones» (sin ella, la del modelo: el comportamiento anterior).
  `valor_fuente` sigue en la escala del modelo y tiene que ser **exactamente** la cifra de `literal` convertida; la cifra impresa sigue
  buscándose literal, completa, en su fila y su columna. Otro valor de `escala` → DATOS INVÁLIDOS (también en `leer_serie`: V-F1e).
- Cero impreso sin dígitos (`literal` «—», «–», «-» o «nil», `valor_fuente` 0): exige `fila`; la marca, aislada y después de la etiqueta,
  en esa línea y en la columna del ejercicio. Sin encabezado alineado queda PENDIENTE, como una cifra.
- Cero sin cifra impresa: `cero_comprobado` {`motivo`, `cita`}, sin `literal` y con `valor_fuente` 0. La cita tiene que estar literal en la
  página citada (espacios y mayúsculas aparte), con al menos 8 palabras y sin importes. El programa comprueba la cita, **no** que pruebe la
  inexistencia: queda PENDIENTE de revisor (no bloquea F1; la aptitud por entradas sigue en «no»). Amplía el límite 3 de este §9.
- Nada más se relaja. Batería `personaje_v2/pruebas/test_f1_series_escala.py` (55 pruebas, registrada en `verificar_paquete.sh` en los
  dos modos; con el código anterior pasan 12 de 55: las que comprueban que lo que bloqueaba sigue bloqueando).

**Ronda 2 (revisión independiente, `coordinacion/cierre_v2/examen/revisiones/f1_series_escala/REVISION.md`).**
- *Hallazgo A (cero impreso):* una marca solo es la celda del ejercicio si a su derecha no quedan letras (no es parte de la etiqueta:
  «Finance lease - principal», «Financing cash flows – finance leases» del 10-K de Zoetis) y no la sigue, con un espacio como mucho, una
  cifra o un paréntesis (no es el signo de «- 7»). Si no queda ninguna, DATOS INVÁLIDOS.
- *Hallazgo B (escala):* con `escala` declarada, la página tiene que declarar esa escala en un encabezado (lista cerrada `MARCAS_ESCALA`:
  «(in millions)», «(amounts in Euro)», «in thousands of euros», «€000», «EUR m», «en miles de euros»…; la prosa con una cifra en medio
  no cuenta). Otra escala → DATOS INVÁLIDOS; sin encabezado reconocible, o con varias escalas, la escala queda PENDIENTE («declarada y NO
  comprobada»). Sin `escala` no se contrasta nada (el comportamiento anterior). En Jumbo las cuatro páginas dicen «(amounts in Euro)».
- *Cero comprobado, visible:* **antes un cero sin cifra impresa dejaba F1-SERIES en INCOMPLETO; ahora no la bloquea.** No hay vía para que
  un revisor lo cierre dentro de la capa: queda siempre pendiente y, para que nadie lo lea como comprobado, cada año sale en un aviso propio,
  `F1-SERIES-CERO` (AVISO, PENDIENTE), con su motivo y su cita, que aparece en la tabla de guardas de `motor_a_f1_resultado.md` y en los
  avisos del bloque `motor_a_f1` de la ficha. La aptitud por entradas sigue en «no».
- La batería pasa a 74 pruebas (13 nuevas fallan con el código de la ronda 1), con un caso US: con la capa de `f1/usgaap`, la línea de
  Zoetis en `pagos_arr_financiero_principal`; sin ella, la misma línea en `da_ppa`.
- Jumbo (copia de comprobación): la frase de AR2025 p. 189 solo se usa para 2025; para 2021–2024 no prueba nada (es de octubre de 2025) y
  esos años siguen sin cero declarado (INCOMPLETO) hasta que la persona responsable decida.

**Retoques tras la ronda 2 (`REVISION_R2.md`, conforme con límites).**
- *Límite 2:* «All amounts in euros (thousands)» ya no se lee como «unidades» (el patrón admite un paréntesis antes de «thousands»,
  «millions» o «'000»): declarado «unidades» queda PENDIENTE y declarado «miles» ya no se rechaza (queda PENDIENTE: «(thousands)» solo no
  es una marca de la lista).
- *Límite 1:* la escala se busca en el **bloque de la tabla** de la cifra, no en toda la página: desde la línea de la cifra (la que lleva
  también la `fila`; la primera si hay varias) hacia arriba hasta dos líneas en blanco seguidas o el principio de la página
  (`_escala_de_tabla`). Lo que va debajo (otra tabla «(in thousands)», como en la sonda R1 del revisor) no cuenta. **Límite que queda:**
  una página de continuación cuyo encabezado quedó en la página anterior no tiene marca en el bloque y la escala queda PENDIENTE; y si
  dos tablas van seguidas sin dos líneas en blanco entre ellas, la marca de la de arriba entra en el bloque de la de abajo (p. ej., la
  sonda R1 del revisor con la tabla «(in thousands)» encima, y no debajo, de la de arrendamientos sin encabezado propio daría un falso
  «comprobado» con «miles»). En Jumbo las cinco cifras siguen con la escala comprobada.
- *Detalle menor:* con la escala pendiente, el año ya no cuenta además como columna comprobada; la columna se sigue examinando (otra
  columna → DATOS INVÁLIDOS).
- Batería: 80 pruebas (6 nuevas, que fallan con el código de la ronda 2).

## 11. Normalización del circulante (19-nov-2026) · la V6.3.1 no cambia

**Hecho.** La normalización declarada del circulante de la reinversión (decisión V-CIRC (a); `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_circulante/F1_CIRCULANTE.md`)
no está en la V6.3.1 F1: la plantilla, su referencia, su verificador (`eaece01a…`) y los expedientes hechos con ella no cambian. Con la normalización
declarada y un libro V6.3.1, la capa bloquea con F1-LIBRO (límite declarado). Se calcula en la plantilla hermana **V6.3.2 F1** (`v6/v632_f1/`,
`config_v2_v632_f1.json`), que sin normalización es exactamente la V6.3.1 (0 celdas distintas de 39.950 con las mismas entradas). `f1_libro_v631.py
aplicar` escribe en un libro V6.3.1 las mismas 24 celdas de antes.
