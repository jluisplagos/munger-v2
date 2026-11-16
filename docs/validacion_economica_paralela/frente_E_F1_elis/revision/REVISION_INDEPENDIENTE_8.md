# Revisión independiente n.º 8 · frente E · F1 · Elis · lo afectado por C16

Fecha: 16-nov-2026. Material revisado: commit congelado `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` (C17) de la rama `auditoria/economica-f1-frente-e`. C17 solo añade a C16 (`66d01b8fc21b277efdae938170cc64815705962e`) el registro de su hash (comprobado: `git diff 66d01b8 863ddde` toca `ESTADO.md`, la línea de C16 en las respuestas y el manifiesto). Alcance: `git diff f1dd6c5 66d01b8`, es decir, la respuesta a S1–S7 (36 archivos), en dos commits: `559828e` (verificador y test) y `66d01b8`. Entre los dos, `verificar_cifras.py` solo gana tres líneas en su cabecera. Base de comparación, en su propio worktree: C15 (`c96d544…`), que tiene el código de C14. La copia de la revisión n.º 7 que incorpora `f1dd6c5` es idéntica a lo publicado en esta rama (informe, scripts y salidas).

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit d192cab.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2). El verificador de C14 y el de C16 dan el mismo resultado sobre las 752 filas reales.
2. **Los scripts de las revisiones n.º 6 y 7 sobre C16**, vueltos a ejecutar sin cambios: 11 de las 12 salidas que guarda el autor son idénticas. La duodécima, `reproduccion_7`, difiere en dos líneas: la guardada dice «Manifiesto: 243 de 251» y sobre el congelado da 274 de 274 (T8 e).
3. **Las 346 aceptaciones nuevas** que declara el autor existen y salen todas de la regla de S1 (fecha del saldo en el rótulo). **341 son cifras legítimas de saldos**: ejercicio, unidad, perímetro y edición correctos [P][D]. **Cinco no son cifras**: dos veces el día de la fecha («31»), dos veces la pestaña del capítulo («6») y una vez el año de una fecha en una línea de prosa. En mi barrido, que recorre también los años sueltos, son 411: las mismas 341 y 70 tokens que no son cifras (§4.3).
4. **En ninguna fila de tabla de las cinco publicaciones la fecha del rótulo da un ejercicio equivocado** [P][D]. Las 76 filas con cifras aceptadas las he leído además con PDFium: el rótulo lleva esa fecha en las 76.
5. **La regla de S1 sí acepta cosas que no debe o deja de aceptar lo que debe** (§7):
   - **T1.** Da OK en las seis dimensiones a un saldo de una tabla con columnas por concepto sin que nada compruebe la columna: la dimensión «columna» queda NO_APLICA con el motivo «la columna es el ejercicio». 331 de las 341 están en filas de dos a doce columnas. La cifra de la columna «Vehicles» pasa con un identificador genérico, sea cual sea el concepto que la fila diga declarar; con el identificador de saldo, la misma cifra falla en «columna».
   - **T2.** Se dispara en 355 líneas: 157 son filas de saldo, 71 son recuentos con fecha y 127 no son ni lo uno ni lo otro (prosa, títulos, sumarios, cabeceras). En estas últimas solo quedan OK los años de la propia fecha; ninguna cifra. Y da el ejercicio a cualquier token de la línea.
   - **T3.** No reconoce cinco de los diez saldos de cierre del estado de cambios en el patrimonio (rótulo partido tras el día o en tres líneas): quedan PENDIENTE. En dos de ellos, una cifra era OK en C14. T14 cita esos saldos entre lo que debe aceptarse.
6. **S2 frente a rótulos de otras filas** (T5): la función toma por rótulo cualquier línea contigua de una sola celda, sin límite de longitud. En seis líneas cambia el perímetro por un párrafo de prosa o por la leyenda de un organigrama. No crea ninguna aceptación en las seis dimensiones y no hace fallar ninguna cifra legítima.
7. **S4 queda con un resto** (T4): en el DEU 2024 p.315 las dos últimas filas de la tabla del WACC por país conservan el perímetro OK (18 cifras).
8. **Las dos decisiones propias de C16 se sostienen** (§5): declarar S7 d como límite es prudente y está declarado, aunque el motivo inexacto retiene tablas en tres publicaciones y los documentos lo sitúan en una; retirar un argumento de la decisión (b) es correcto y no cambia su coste (176 cifras legítimas). El argumento retirado sigue escrito en T14 y en la sexta parte de las respuestas (T8 a).
9. **Contraste** (§6): `detecta_desde_unidades` es exacto en las 246 entradas, comprobado como caja negra con 1.458 ejecuciones. Las frases de S6 están corregidas, salvo E9: su lista sigue citando R36 de 2021–22, en la que no interviene ninguna de las 97 entradas (T7 c).
10. **Objeciones nuevas: T1–T4 (menores) y T5–T8 (forma). Ninguna afecta a las 752 filas reales. Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje recibido al crearse esta sesión, entregado como aviso automático y no tecleado por una persona en ella. Lo trato como un encargo de revisión, no como una conclusión que confirmar: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Aquí no se escriben identificadores de modelo. Quien encarga puede leer la configuración de esta sesión en sus metadatos.

**Límites de la independencia:**
- **Quien encarga fija el alcance** y señala qué mirar: las 346 aceptaciones, la prosa, los rótulos con fechas que no son el saldo, las columnas que no son del grupo, la regla de S2 y las dos decisiones.
- **He leído la revisión n.º 7 entera y he usado sus scripts y los de la n.º 6** para comprobar las salidas guardadas. Esta sesión es nueva y no conserva el contexto de ninguna pasada, pero parte de sus informes y de su universo de casos.
- **La herramienta de extracción es en parte común.** Mi barrido usa `pdftotext` por fuerza: es la entrada del verificador. Lo he reducido así:
  - las 76 filas de saldo aceptadas están leídas con PDFium, un motor distinto (`lectura_saldos_8.py`);
  - los encabezados que pierde la regla de S5 están clasificados por tipografía con MuPDF;
  - cuatro páginas de los casos nuevos están vistas en la página renderizada: DEU 2024 p.274 y p.315, URD 2025 p.366 y URD 2022 p.350;
  - un error de extracción común a `pdftotext` y a mis lecturas de página con esa herramienta no se detectaría.
- **Mis clases son un filtro, no una verdad.** «Fila de saldo», «recuento con fecha» y «otra» salen de expresiones mías. He leído las 127 líneas de la clase «otra», las 88 líneas con aceptaciones nuevas, la cabecera de la tabla en las 40 páginas con cifras aceptadas, las líneas en las que una fila deja de ser OK y aquellas en las que el perímetro pasa a FALLO. No he mirado las 154.476 candidatas una a una.
- **Los identificadores de sondeo de los demás modos son míos.** Fijan el modo por su prefijo, como hace el verificador; no son filas del autor.
- Mi barrido llama a `comprobar_tabla`, la función que la ejecución oficial usa para cada fila. Equivalencia comprobada en las 713 filas de tabla reales de C14 y de C16: ninguna dimensión distinta. Restringido al universo del barrido de la revisión n.º 6, da sus mismos recuentos: dos arneses escritos por separado coinciden.

---

## 2. Reproducción (alcance 1)

Base 4.14 materializada desde el ZIP original de la Release (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`, en un worktree de `main`: 6.798 de 6.798, `complete: true`. Libro `d2593777…92385`. Las cinco fuentes, con la huella de `fuentes.json`. Ejecución sobre una copia de la carpeta del worktree de C17. Prueba: `reproduccion_8.py` → `resultados_revisor_8/reproduccion_8.txt`.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 274 de 274 |
| CSV regenerado desde los PDF | Idéntico (752 filas: 713 de tabla y 39 de texto; SHA-256 `3f9ae6e6…1331`) |
| Verificador: 752 filas, 738 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON y registro idénticos. Las 73 páginas exportadas, idénticas. Las 14 PENDIENTE, del URD 2022 p.302 |
| «Salida idéntica byte a byte a la de C14» | Cierto. El verificador de C14 sobre el mismo CSV da un JSON idéntico al de C16 y al que guarda C15: ninguna de las 752 filas cambia en ningún campo |
| `test_verificar_cifras`: 117/117 | Reproducido. Registro idéntico. Composición: 23 OK, 23 PENDIENTE y 71 FALLO esperados |
| Contraste: 292 comprobaciones (136 del libro, 127 de fuente, 29 algebraicas), 0 fallidas, 419 entradas | Reproducido. Código 0. JSON, tabla y registro idénticos |
| `test_contraste_residuos`: 24/24 | Reproducido. Registro idéntico |
| `cobertura_por_mutacion`: 530 filas, sin incoherencias | Reproducido. Salida idéntica: 386 por identidad, 2 solo libro, 23 sin detectar y 119 no usadas |
| Sondas: 713/713 en unidad y en perímetro | Reproducido. JSON idéntico |
| Referencias de E9 sin cambios | Todo `referencia_especificacion` es igual en C15 y en C17 (C53 de A1, 2,445331695332; de A2, 1,612524303305). Entre los dos JSON del contraste solo cambia `cobertura_entradas`: el campo nuevo `detecta_desde_unidades` de cada entrada y su recuento |
| Scripts de las revisiones n.º 6 y 7 sobre C16 | Vueltos a ejecutar (`relanzar_revisores_6_7.sh` → `comparacion_6_7.txt`). 11 salidas idénticas a `resultados/revisor6_*_sobre_C16.txt` y `revisor7_*_sobre_C16.txt`. `reproduccion_7`: dos líneas distintas, las del manifiesto (la comparación cuenta cuatro, dos por versión; T8 e) |
| «Scripts de los revisores n.º 1 a 5: mismas salidas que sobre C14, salvo `clases_5`» | No los he vuelto a ejecutar. He comparado las salidas que guarda el autor sobre C14 y sobre C16, igualada la etiqueta de versión: ocho son iguales; `clases_5` difiere en 6 líneas, como dice; **`barrido_tablas` difiere en 220 líneas**, y eso no se dice (T7 f) |

`prueba_caja_no_nula.py` y sus dos salidas no cambian desde C4 (`git diff d2e585e 863ddde` vacío para los tres archivos). No la he repetido: no he usado LibreOffice.

---

## 3. Estado de S1–S7 (alcance 2)

Los casos A–E son los de la revisión n.º 7 (`contraejemplos_7` sobre C16, reproducido). Los casos T son los míos (`contraejemplos_8.txt`): el verificador oficial de C14 y de C16, como proceso aparte.

| Objeción | Estado | Prueba |
|---|---|---|
| S1 · el año del título de la tabla contaba como columna | **Corregida en sus casos, con tres efectos nuevos** | Lo que declara el autor es exacto: A1, A3, A5, A6, A7 y A12, de FALLO a OK; A10, de PENDIENTE a OK; A2, A4, A16 y A17, de PENDIENTE a FALLO; A8 y A9, de OK a FALLO; A13–A15, A18 y E2 ya solo fallan en edición. El título ya no entra en la cabecera de los diez estados: salen 15 líneas de continuación, y las 15 son continuaciones de un título (`clases_8.txt`, M). Efectos nuevos: T1, T2 y T3 |
| S2 · cifra en una línea sin rótulo | **Corregida**, con una observación | B1–B4, FALLO de perímetro; B5 y B6, FALLO; B7, OK. Declarada de su segmento, la fila pasa a OK (T6c). La función toma más de lo que debe: T5 |
| S3 · la pestaña del capítulo ocupaba el lugar del rótulo | **Corregida** | C1 y C2, FALLO. De las 19 líneas de las páginas del grupo con cifras tras la pestaña, cambian tres: «CGU France» y dos filas de saldo (`clases_8.txt`, I). Sin efecto en las demás |
| S4 · tabla con una columna por país y sin unidades | **Corregida en cuatro publicaciones; resto en el DEU 2024** | D1–D5, PENDIENTE. 283 tokens pasan de OK a PENDIENTE en cinco páginas, todas de la tabla del WACC por país; ninguna tabla del grupo queda retenida. En el DEU 2024 p.315, 18 cifras conservan el perímetro OK (T4) |
| S5 · la regla del encabezado numerado tomaba prosa | **Corregida en los casos citados**, con un resto | Las nueve líneas de las páginas del grupo que dejan de ser encabezado son texto por tipografía. Quedan 14 de 409 que no son títulos, y fuera de las páginas del grupo dejan de serlo nueve títulos verdaderos (T6). Ningún estado cambia por ello |
| S6 · frases más fuertes que su prueba | **(a), (b), (c), (d), (f), (g) y (h), corregidas; (e), en parte** | Precisadas en su sitio. `detecta_desde_unidades`, exacto (§6). En E9 queda R36 de 2021–22 (T7 c) |
| S7 · varios | **(c) y (e), corregidas; (a) y (b), reconocidas; (d), declarada** | (c) La cabecera dice seis dimensiones, pero no describe la regla nueva de la fila (T8 c). (e) El motivo de D6 es ahora «France». (d): §5 a |

---

## 4. Verificador (alcance 2)

### 4.1 Método

- **Barrido propio** (`barrido_8.py`). Todos los tokens numéricos de todas las líneas de las 2.026 páginas de los cinco PDF: con rótulo o sin él, del grupo o no, prosa y años sueltos incluidos. Son 22.324 líneas y 51.492 tokens; 27.198 en las 459 páginas del grupo. Cada token se declara de cuatro maneras:
  - **G**, cifra del grupo de dos columnas, con el ejercicio de la publicación, el anterior y el segundo anterior, y la edición que la regla exige: 154.476 candidatas, evaluadas con `comprobar_tabla` de C14 y de C16;
  - **M**, los demás modos de control del ejercicio (`max_cabecera`, `movimientos`, `saldo`, `titulo` y `crecimiento`), con 15 identificadores de sondeo que fijan también la columna esperada. Los barridos anteriores no los recorrían. El ejercicio, la columna y la edición se piden a las funciones que `comprobar_tabla` usa; uno de cada 25 tokens se evalúa además con `comprobar_tabla` entera: 175.194 evaluaciones de muestra, ninguna distinta;
  - **S**, el perímetro declarado de cada uno de los siete segmentos, con `comprobar_perimetro` de las dos versiones;
  - **R**, lo que las funciones nuevas leen en cada línea: el ejercicio del rótulo, los rótulos contiguos, el rótulo con y sin la pestaña y la cabecera de países.
- **Clases** (`clases_8.py` → `clases_8.txt`, secciones A–N).
- **Contraejemplos** con el verificador oficial como proceso aparte (`contraejemplos_8.py`, 25 casos).
- **Lecturas con otro motor**: PDFium para las filas de saldo aceptadas (`lectura_saldos_8.py`) y MuPDF para la tipografía de los encabezados (`clases_8.txt`, K).

### 4.2 Transiciones entre C14 y C16 (candidatas G, todas las páginas)

| Transición de la fila | Candidatas | Lectura [D] |
|---|---|---|
| No OK → OK | 411 | 401 desde PENDIENTE y 10 desde FALLO. Todas en páginas del grupo y todas por la regla de S1: §4.3 |
| OK → FALLO | 10 | Seis por la regla de S1, declaradas con otro ejercicio: A8 y A9 y cuatro años sueltos. Cuatro de perímetro: «CGU France» (S3) y la fila de Escandinavia (S2). **Ninguna es una cifra legítima** |
| OK → PENDIENTE | 37 | 35 movimientos del estado de cambios en el patrimonio, en la columna que quedaba bajo el año del título, y **dos saldos de cierre del DEU 2024** (T3). Son cifras legítimas que C14 aceptaba por coincidencia con el año del título. La respuesta no las cuenta |
| PENDIENTE → FALLO | 1.072 | 1.018 por la regla de S1, declaradas con un ejercicio que no es el de la fecha del rótulo. 26 de unidad: la pestaña ante una línea de prosa con «employees» o «Number of» (S3). 16 de perímetro: las correcciones de S2 y S3 y las líneas de T5. 12 de ejercicio sin la regla, en dos tablas de indicadores y dos líneas de prosa fuera de las páginas del grupo |
| FALLO → PENDIENTE | 271 | 172 por la regla de S1: el ejercicio pasa a OK y la fila sigue PENDIENTE por la unidad o el perímetro (151 en recuentos con fecha, casi todos de planes de acciones; 20 en epígrafes «Main offices…»; una en una fila de saldo). 99 sin la regla: 96 en los estados de cambios en el patrimonio, donde sin el año del título no hay columna de ejercicio, y 3 en una línea de sumario y otra de una tabla de referencias |
| OK → OK | 5.529 | — |

OK en las seis dimensiones: 5.576 en C14 y 5.940 en C16.

Por dimensión: ejercicio, 3.035 cambios; perímetro, 885 (36 de OK a FALLO y 849 de OK a PENDIENTE); unidad, 39. De los cambios de ejercicio, 2.772 vienen de la regla de la fila y 263 no: 229 en los estados de cambios en el patrimonio y 34 en nueve líneas de tablas de indicadores, encabezados, un sumario y prosa (cinco candidatas en páginas del grupo), donde cambia la zona de cabecera. Ninguno de los 263 acaba en una fila OK (`consultas_8.txt`, Q2 y Q3; `clases_8.txt`, G y M).

En el universo del barrido de la revisión n.º 6 (líneas con rótulo, sin años sueltos: 124.887 candidatas) mi arnés da sus mismas transiciones: 6 y 340 a OK, 3 de OK a FALLO, 37 de OK a PENDIENTE, 811 de PENDIENTE a FALLO y 247 de FALLO a PENDIENTE (`clases_8.txt`, A).

### 4.3 Las aceptaciones nuevas

Las 411 tienen el ejercicio por «saldo de AAAA (fecha en el rótulo de la fila)» y es la única dimensión que cambia (`clases_8.txt`, B).

| Clase del token | Candidatas | En el universo de la revisión n.º 6 |
|---|---|---|
| Cifra de una fila de saldo | 341 | 341 |
| Año de la fecha del propio rótulo, en una fila de saldo o en la cabecera de una tabla | 62 | — |
| Año de la fecha en una línea de prosa o de título | 4 | 1 («2023)») |
| Día de la fecha («31» de «DECEMBER, 31 2022») | 2 | 2 |
| Pestaña del capítulo («6») | 2 | 2 |
| **Total** | **411** | **346** |

**Las 341 son legítimas** [P][D]:
- están en 76 líneas de 40 páginas (`consultas_8.txt`, Q1): los saldos de apertura y de cierre de los estados de cambios en el patrimonio y los de las tablas de movimientos de intangibles, inmovilizado, derechos de uso, provisiones, pensiones, deterioro de clientes y reservas de cobertura. Es lo que dice el autor;
- la fecha del rótulo es la del saldo en las 76: leídas con PDFium, el rótulo que precede a las cifras lleva esa fecha y da el mismo ejercicio (`lectura_saldos_8.txt`);
- las cabeceras de esas tablas son conceptos del grupo (componentes del patrimonio, clases de activo, categorías de provisión); ninguna es una columna por país, por sociedad ni por marca. He leído la cabecera de la tabla en las 40 páginas;
- la unidad es la declarada por la tabla y la edición, la que exige la regla. Las 341 son saldos a 31 de diciembre: 163 del ejercicio de la publicación y 178 del anterior. Un saldo a 1 de enero cuenta como cierre del ejercicio anterior, igual que en el modo `saldo`; en estas tablas es el segundo ejercicio anterior, que la regla de edición no admite;
- ninguna fila con la fecha en el rótulo está en una tabla cuyas columnas sean ejercicios: no hay conflicto entre la fila y la columna en estas publicaciones. En las 103 líneas en que C14 decidía el ejercicio de una fila así por una columna reconocida, esa «columna» era el año del título (estados de cambios en el patrimonio), el año de concesión de un plan de acciones, una cabecera ajena o el propio año del rótulo (`consultas_8.txt`, Q4).

**Los 70 tokens que no son cifras** quedan OK en las seis dimensiones como millones de euros del grupo: «31» como 31,0, «6» como 6,0, «2021» como 2.021,0 (T2a–T2e). Nadie los declararía; muestran a qué da el ejercicio la regla.

### 4.4 Por regla

**S1, título numerado y su continuación.** Actúa en los diez estados de cambios en el patrimonio y en cinco títulos más; las 15 líneas que salen son continuaciones de un título. La zona de cabecera cambia en 1.252 líneas (815 en páginas del grupo), casi siempre porque ya no incluye lo que queda por encima de un encabezado numerado. Fuera de los estados de cambios en el patrimonio, el cambio de la zona mueve el ejercicio de 34 candidatas en nueve líneas (§4.2): ninguna es una cifra de una tabla del grupo y ninguna queda OK. Sin objeción.

**S1, fecha del saldo en el rótulo.** `anio_de_saldo_en_rotulo` da un ejercicio en 355 líneas (189 en páginas del grupo; `clases_8.txt`, C):

| Clase de línea | Líneas | En páginas del grupo |
|---|---|---|
| Fila de saldo | 157 | 127 |
| Recuento o dato con fecha (planes de acciones, capital, autocartera) | 71 | 34 |
| Otra: prosa, título, sumario o cabecera | 127 | 28 |

- En las filas de saldo y en los recuentos con fecha el ejercicio es el de la fecha [P]. En los planes de acciones la columna es el año de concesión y la fila, la fecha del saldo: lo que dice el autor es cierto.
- La regla no mira la columna ni la posición del token: T1 y T2.
- No reconoce la mitad de los cierres del estado de cambios en el patrimonio: T3.

**S2, rótulo de las líneas contiguas.** `rotulos_sin_rotulo` devuelve algún rótulo en 2.015 líneas (327 en páginas del grupo). En 33 de las del grupo la línea tiene dos tokens o más. Efectos: las dos correcciones (Escandinavia y «CGU France») y seis asociaciones que no son el rótulo de la fila (T5).

**S3, pestaña del margen.** `rotulo` cambia en 706 líneas (167 en páginas del grupo). 649 solo llevan la pestaña; 57 llevan además cifras, 19 de ellas en páginas del grupo. En esas 19 la regla hace lo que dice: cambia el estado de tres («CGU France» y dos filas de saldo que ahora tienen rótulo) y deja igual las otras 16. Fuera de las páginas del grupo cambia una de 38. Sin objeción.

**S4, cabecera de países y rótulo partido.** `cabecera_de_paises` actúa en las cinco tablas del WACC por país y en tres organigramas fuera de las páginas del grupo. Mi lectura de las cabeceras con dos países o más en celdas cortas no encuentra ninguna otra tabla que conserve el perímetro OK, salvo las dos filas de T4 (`clases_8.txt`, J). La excepción de la columna «Total» o «Group» no tiene ningún caso real: no está probada.

**S5, encabezado numerado en prosa.** De 418 a 409 líneas en las páginas del grupo, y de 1.012 a 982 en las demás. Resto: T6.

**Los demás modos (M).** Ninguna fila pasa a OK en ningún modo. Las filas OK son las mismas en C14 y en C16 con los 11 identificadores de `max_cabecera`, `movimientos`, `saldo` y `titulo`; con los de `crecimiento` baja una, la del segmento de Escandinavia (S2). Hay diferencias de columna o de ejercicio en 21 líneas: cuatro pies de página, cinco encabezados numerados, cuatro líneas de prosa, las dos líneas de cabecera de una tabla del grupo (URD 2023 p.304) y seis líneas de tablas fuera de las páginas del grupo (`clases_8.txt`, N).

### 4.5 Los scripts de las revisiones n.º 6 y 7 sobre C16

Las salidas que guarda el autor son las que dan los scripts (§2). Lo que la séptima parte dice de ellas es exacto en estos puntos, que he comprobado en las salidas:
- `contraejemplos_6`: los 48 casos tienen el mismo estado y el mismo motivo en C14 y en C16;
- clase E del revisor n.º 6: de 13 a 11;
- `barrido_7`: ninguna aceptación nueva en sus líneas sin rótulo; `sondas_umbral_7`: 246 de 246;
- `contraejemplos_7`: los 40 casos, como se describe en S1–S4 (tabla de §3).

Dos cosas que esas salidas no muestran, por construcción:
- los dos barridos excluyen los años sueltos y declaran cada token solo como cifra del grupo de dos columnas;
- la clase D de la revisión n.º 6 lista las 346 por rótulo. El primero de la lista, del DEU 2024 p.257, es «d'euros (contre 902,3 millions d'euros»: una línea de prosa (T7 a).

---

## 5. Las decisiones propias de C16 (alcance 3)

### (a) S7 d declarado como límite y no corregido

**Se sostiene como elección prudente, y está declarada.** El autor dice que corregir el motivo dejaría el perímetro de esas tablas en OK, porque la regla de grupos no las ve. Es cierto [D]: la tabla de las hipótesis por marca no tiene ejercicios en la cabecera ni nombra ningún país.

- **Qué cuesta** [P][D] (`clases_8.txt`, L; `consultas_8.txt`, Q8):
  - el motivo inexacto no está solo en el URD 2022 p.305. La tabla de hipótesis por marca queda retenida por el título de la tabla anterior también en el URD 2021 p.272 («Switzerland», 9 tokens) y en el URD 2023 p.324 («Sweden», 14 tokens: los 9 de la tabla y los 5 de la línea de cabecera de la tabla siguiente). En el URD 2022 p.305 son 44: los 9 de la tabla por marca y los 35 de la tabla de sensibilidad;
  - la retención es accidental: depende de que delante haya una tabla con título de país. En el URD 2025 y en el DEU 2024 la tabla por marca lleva dos fechas por marca y la retiene la regla de grupos, con su propio motivo;
  - el resultado no es uniforme. La tabla de sensibilidad de la marca Elis queda PENDIENTE entera en el URD 2022; en las otras cuatro publicaciones sus filas de datos conservan el perímetro OK, y en tres de ellas solo queda retenida su línea de cabecera;
  - en los tres URD, las 336 candidatas bajo el epígrafe de las marcas siguen PENDIENTE en ejercicio: su cabecera no tiene columnas de ejercicio. Corregir el motivo no crearía hoy ninguna aceptación; la crearía si más adelante se acreditara el ejercicio de esas tablas.
- **Redacción.** El informe §1 y la séptima parte dicen que la regla de grupos «no ve» la tabla de las marcas de los URD 2021–2023 y sitúan el motivo inexacto solo en el URD 2022 p.305. Se lee como si en los URD 2021 y 2023 el perímetro de esa tabla quedara en OK. No es así: queda PENDIENTE por el mismo motivo inexacto, como ya decía la revisión n.º 7 (§5 a) (T8 d).

### (b) Retirada de un argumento de la decisión (b) de C14

**Se sostiene.** El argumento retirado («la columna de una firma es un desglose por firma, no el total del grupo») es de concepto y no de perímetro, como decía la revisión n.º 7. Queda el otro: el verificador no distingue la columna de una firma auditora de la de una marca. Es cierto y basta para una elección conservadora.

- **Qué cuesta** [D]: lo mismo que antes. En mi barrido, 218 candidatas tienen el perímetro como único impedimento por la regla de grupos (`consultas_8.txt`, Q9): 176 de las cinco tablas de honorarios, que son cifras legítimas del grupo; 40 de las tablas por marca del DEU 2024 y del URD 2025 y de la línea de porcentajes que las sigue, retenidas con razón; y dos números de pie de página. Ninguna fila real está en esas tablas.
- **La retirada no ha llegado a todos los sitios** (T8 a): T14 sigue diciendo que «la columna del grupo no es la del grupo consolidado» para «una marca, una firma auditora», y la sexta parte, R2, conserva la frase sin la nota de precisión que sí llevan las demás.

---

## 6. Contraste (alcance 4)

Prueba: `sondas_8.py` → `sondas_8.txt`. Ejecuta `contraste_f1.py` del autor, sin cambios, con una sola entrada desplazada y la verificación falsa hecha corresponder con cada CSV, como en `cobertura_por_mutacion.py`. No usa sus coeficientes ni sus intervalos.

- **`detecta_desde_unidades`: exacto en las 246 entradas** [D]. Con el número de unidades declarado fallan los dos sentidos; con cualquier número menor, alguno no falla. 1.458 ejecuciones. El recuento, 5, 112, 69, 17, 33 y 10, coincide. La fórmula usa fracciones exactas y trunca: una entrada con el umbral en un número entero de unidades da el siguiente, como debe.
- **«Por encima de ±0,1»** [D]. En las doce entradas de ventas (cuenta de resultados, información por segmentos e informe de gestión, de 2020 a 2025), ±0,1 no hace fallar ningún residuo entre páginas y ±0,2 hace fallar R23 o R40. La frase es exacta en el informe §0.2 y §2 y en la sexta parte.
- **Tramos y recuento nuevo** [D]. «El mayor error que no se detecta» (145, 99 y 2) y «se detecta desde» (5, 112, 69, 17, 33 y 10) están bien distinguidos en el informe §0.2 y en la nota del JSON.
- **E9** [D]. Las entradas que mueven la referencia son 97, todas contrastadas entre páginas, y su mayor error sin detección va de 0,10 a 0,50: la frase nueva es exacta. La lista de identidades no lo es del todo (T7 c).

---

## 7. Objeciones nuevas

Todas las filas existen en el PDF [P]. Ninguna afecta a una fila real del CSV: la salida de las 752 es idéntica en C14 y en C16.

### T1 · menor · `verificar_cifras.py`, ejercicio y columna (S1, efecto nuevo) · un saldo de una tabla con columnas por concepto queda OK sin que nada compruebe la columna

- **Qué ocurre** [P][D]. La regla de S1 da el ejercicio por el rótulo «sea cual sea su columna», y lo hace en el modo `dos_columnas`. En ese modo la dimensión «columna» devuelve NO_APLICA con el motivo «la columna es el ejercicio: se comprueba en «ejercicio»». Para estas filas no es cierto: el ejercicio ha salido de la fila y la columna es un concepto (clase de activo, componente del patrimonio) que nadie mira.
- **Prueba.** `contraejemplos_8.txt`, T1a–T1e; `clases_8.txt`, D.

  | Cifra [P] | Declaración | C14 | C16 |
  |---|---|---|---|
  | URD 2025 p.366 · derechos de uso a 31-12-2024, columna «Vehicles» (237,4) | identificador genérico | PENDIENTE | **OK en las seis dimensiones** |
  | la misma cifra | identificador de saldo de derechos de uso (columna esperada: «Total») | FALLO de columna | FALLO de columna |
  | el total de esa fila (572,8) | identificador de saldo | OK | OK |
  | URD 2022 p.262 · patrimonio a 31-12-2021, columna «Non-controlling interests» (0,7) | identificador genérico | PENDIENTE | **OK en las seis dimensiones** |
  | URD 2025 p.367 · inmovilizado a 31-12-2024, columna «Vehicles» (13,0) | identificador genérico | PENDIENTE | **OK en las seis dimensiones** |

  De las 341 cifras aceptadas, las 341 tienen «columna» en NO_APLICA y 331 están en filas de dos a doce columnas.
- **Causa** [D]. Antes de C16 una fila de estas tablas no podía quedar OK con un identificador genérico: sin columnas de ejercicio, el ejercicio quedaba PENDIENTE. La regla nueva acredita el ejercicio y deja sin dueño la columna. En el modo `saldo`, un concepto sin columna esperada queda PENDIENTE en «columna»; aquí queda NO_APLICA.
- **Por qué importa.**
  - Son justo las tablas para las que existe la dimensión «columna». La cabecera del verificador, añadida en C16, dice que en ellas «la cabecera de la columna del token debe ser la del concepto declarado».
  - La lista cerrada de modos por concepto existe, dice el código, para que «un modo declarado no [pueda] saltarse el control de la columna o de la edición». Un identificador nuevo que no empiece por un prefijo conocido entra por `dos_columnas` y, en estas filas, se salta el de la columna.
  - T14 pasa la regla al frente técnico sin este límite.
- **Atenuantes.** Ninguna fila real usa este camino. El concepto de la línea ya era una declaración, y OK significa «sin incoherencia detectada».
- **Corrección propuesta.** Cuando el ejercicio sale del rótulo, «columna» no debe quedar NO_APLICA: PENDIENTE si el concepto no tiene columna esperada y la fila tiene más de una columna de datos. O limitar la regla a los conceptos con columna declarada. Añadir T1a y T1b al test y a T14.

### T2 · menor · `verificar_cifras.py`, ejercicio (S1, efecto nuevo) · la regla se dispara en líneas que no son filas de saldo y da el ejercicio a tokens que no son cifras

- **Qué ocurre** [P][D]. La regla pide dos cosas al rótulo unido: una de las palabras «balance», «solde», «as at» o «au», y una fecha completa. No pide que la línea sea una fila de tabla, ni que el token esté fuera del rótulo.
- **Prueba.** `clases_8.txt`, B y C; `contraejemplos_8.txt`, T2a–T2e y T4.
  - **(a) Líneas que no son filas de saldo: 127 de 355**, 28 en páginas del grupo. Son los epígrafes «Main offices and positions held as at December 31, 2021» y sus equivalentes (81), las continuaciones de título de los estados de cambios en el patrimonio (10), seis entradas de sumario y treinta líneas de prosa, de título y de cabecera (`consultas_8.txt`, Q5).
    - Cuatro candidatas quedan OK en las seis dimensiones, las cuatro el año de la propia fecha: DEU 2024 p.257 («…902,3 millions d'euros au 31 décembre 2023)»), p.277 («au 1er janvier 2024», un título de apartado, aceptado como 2023) y p.323, y URD 2025 p.393.
    - Los otros 12 tokens que no son un año (pestañas del margen, números de página de un sumario, «Note 9») quedan con el ejercicio OK y la fila PENDIENTE: solo los retiene que la página no declara la unidad.
  - **(b) Tokens del propio rótulo.** En las filas de saldo, el año, el día de la fecha y la pestaña del margen reciben el ejercicio como cualquier cifra: 66 candidatas OK en las seis dimensiones.
  - **(c) La fecha del rótulo de la fila anterior.** Si un rótulo de dos líneas lleva las cifras en la primera y la fecha en la segunda, la segunda queda sin cifras y se une al rótulo de la fila **siguiente**. Caso real [P]: URD 2022 p.350, tres filas. «Number of rights outstanding» recibe «as at 12/31/2022», que es la continuación de «Number of rights lapsed or forfeited»; esta, que es la dueña de la fecha, no la recibe. Aquí las filas son todas de la misma fecha y el ejercicio acierta. Con un saldo de apertura seguido de los movimientos del ejercicio, los movimientos pasarían como del ejercicio anterior [H]. No he encontrado ese caso.
- **Por qué importa.** El autor describe las 346 como «todas filas de saldo con la fecha en el rótulo». Una es prosa y cuatro no son cifras (T7 a). Un porcentaje al final de una línea de prosa de una página del grupo con una fecha en su celda quedaría OK en las seis dimensiones: la unidad se acredita por el propio literal [H]. En estas cinco publicaciones no hay ninguno.
- **Corrección propuesta.** Exigir que el rótulo sea la primera celda de una línea de dos celdas o más y que el token esté a su derecha; que el rótulo sea solo la fórmula del saldo y la fecha, con «restated», «retraité» o una llamada, y no una frase; y no unir a una fila una línea de fecha que es la continuación de la anterior. Añadir T2c, T2e y T4b al test.

### T3 · menor · `verificar_cifras.py`, ejercicio (S1, resto) · la regla no reconoce la mitad de los saldos de cierre del estado de cambios en el patrimonio

- **Qué ocurre** [P]. `rotulo_multilinea` solo une las líneas de encima que no tienen cifras. Una línea de rótulo que termina en un número cuenta como línea con cifras:
  - «SOLDE AU 31» / «DÉCEMBRE 2024»: la primera termina en «31» y no se une (DEU 2024 p.274; visto en la página);
  - «BALANCE AS AT» / «DECEMBER 31, 2021» / «(RESTATED)»: las cifras van en la tercera línea, y la segunda termina en el año.
- **Prueba.** `clases_8.txt`, E; `contraejemplos_8.txt`, T3a–T3f.

  | Estado | Saldo de apertura | Saldo de cierre |
  |---|---|---|
  | URD 2021 p.230 · p.231 | reconocido · reconocido | reconocido · **no** |
  | URD 2022 p.262 · p.263 | reconocido · reconocido | reconocido · **no** |
  | URD 2023 p.280 · p.281 | reconocido · reconocido | reconocido · reconocido |
  | DEU 2024 p.274 · p.275 | reconocido · reconocido | **no** · **no** |
  | URD 2025 p.328 · p.329 | reconocido · reconocido | reconocido · **no** |

  Son cinco filas y 60 cifras legítimas, PENDIENTE con su propio ejercicio. Dos de ellas, las del DEU 2024 (capital a 31-12-2024 y a 31-12-2023), eran OK en C14 por el año del título y pasan a PENDIENTE (T3a, T3b).
- **Por qué importa.**
  - T14 dice que el frente técnico «debe aceptar sus veintitrés positivos reales, entre ellos […] los saldos de apertura y de cierre del estado de cambios en el patrimonio declarados con su ejercicio». En el test son dos casos, A1 (una apertura) y A10 (un cierre), los dos del URD 2022 p.262. Leída como regla, la frase no se cumple: el verificador del autor no acepta la mitad de los cierres.
  - El informe §1 dice «aunque esté partido». Depende de por dónde lo parta `pdftotext`.
  - La respuesta no menciona las 37 candidatas que pasan de OK a PENDIENTE: 35 movimientos y estos dos saldos.
- **Atenuante.** PENDIENTE no acredita nada: es el lado prudente.
- **Corrección propuesta.** Unir también la línea de encima que termina en el día o en el año de la fecha cuando es de una sola celda y no lleva más cifras. Añadir T3a y T3c al test. O declarar el límite en el informe y en T14 y ajustar la frase de T14 a lo que se cumple.

### T4 · menor · `verificar_cifras.py`, perímetro (S4, resto) · en el DEU 2024 p.315 las dos últimas filas de la tabla del WACC por país conservan el perímetro OK

- **Qué ocurre** [P]. La tabla tiene una columna por país («France · Allemagne · Brésil · Danemark · Espagne · Grande-Bretagne · Mexique · Pays-Bas · Suède»; vista en la página). Sus dos últimas filas llevan el rótulo en dos líneas: «TAUX D'ACTUALISATION AVANT» / «IMPÔT 2024 (APPROXIMATION)» y «Taux d'actualisation avant impôt» / «2023 (approximation)».
- **Prueba.** `contraejemplos_8.txt`, T5a–T5d; `clases_8.txt`, J. Las 18 cifras de esas dos filas quedan con el perímetro OK, en C14 y en C16. Las otras 99 de la tabla pasan a PENDIENTE (T5c). La misma fila del URD 2025 p.369 queda PENDIENTE (T5d).
- **Causa** [D]. `cabecera_de_paises` sube desde la fila y se detiene en un título. «TAUX D'ACTUALISATION AVANT» va en mayúsculas, sin cifras y en línea propia: `es_titulo` la toma por título. En inglés la primera línea lleva el año («PRE-TAX DISCOUNT RATE 2021») y no cuenta como título; por eso D5 pasa.
- **Por qué importa.** Poco: la fila sigue PENDIENTE en ejercicio, como en S4. Pero el informe §1 y T14 dicen sin excepción que esa tabla «deja el perímetro PENDIENTE», y el test solo cubre los URD.
- **Corrección propuesta.** No cortar la búsqueda en una línea que es la primera del rótulo de una fila (misma sangría que los rótulos y con una fila de datos justo debajo), o seguir subiendo mientras queden filas de datos por encima. Añadir T5a al test.

### T5 · forma · `verificar_cifras.py`, perímetro (S2) · el rótulo de las líneas contiguas toma líneas que no son el rótulo de la fila

- **Prueba.** `clases_8.txt`, H; `contraejemplos_8.txt`, T6a–T6c.
  - **Prosa** [P]. En tres páginas (DEU 2024 p.253, URD 2022 p.243 y URD 2023 p.261) la pestaña del capítulo queda sola en una línea junto a un párrafo. La función toma el párrafo por rótulo, y como nombra la Unión Europea el perímetro falla: «la línea «adopted by the European Union. Audit procedures have been performed…» es de una jurisdicción». El token es la pestaña, no una cifra.
  - **Leyenda** [P]. En los organigramas (URD 2022 p.376, DEU 2024 p.391 y URD 2025 p.449) la línea «100% · ELIS COLOMBIA» queda junto a la leyenda de colores («France», «Latin America»). En el URD 2022, declarada del segmento Francia, pasa de FALLO a perímetro OK (T6b); en los otros dos pasa a OK declarada de Latinoamérica: el segmento es el suyo, pero quien lo acredita es la leyenda. La fila queda PENDIENTE: el ejercicio no se acredita.
  - **Sin efecto** [D]. En las páginas del grupo la función devuelve rótulos en 327 líneas; 33 llevan dos tokens o más. En casi todas el «rótulo» es prosa de la columna vecina de un sumario o el rótulo de otra fila («− Matthieu Lecharny» recibe «Number of working beneficiaries»). Entre C14 y C16 solo cambia el estado de tres, y solo el de una por esta regla: la fila de Escandinavia (`consultas_8.txt`, Q6).
- **Causa** [D]. `rotulos_sin_rotulo` acepta hasta tres líneas por arriba y tres por abajo de una sola celda y sin cifras, sin límite de longitud ni de sangría: 1.276 de las 2.015 líneas en que actúa reciben algún «rótulo» de más de 45 caracteres. `rotulo_multilinea` corta en 45. Además trata como línea sin rótulo la que empieza por un guion («− Matthieu Lecharny»).
- **Por qué importa** [I]. Hoy, nada en los datos: ninguna cifra legítima falla y ninguna candidata queda OK por ello. La clase es la de siempre: una línea vecina que la rejilla pone donde iría el rótulo.
- **Corrección propuesta.** Acotar las líneas contiguas a 45 caracteres y a la sangría de la columna de rótulos, y no aplicar la regla a una línea que solo lleva la pestaña.

### T6 · forma · `verificar_cifras.py`, perímetro (S5, resto) · el criterio de la puntuación deja prosa dentro y títulos fuera

- **Prueba.** `clases_8.txt`, K, con la tipografía de MuPDF; clase F del revisor n.º 7 sobre C16.
  - De las 409 líneas que C16 toma por encabezado en las páginas del grupo, 14 no son títulos: 12 entradas de sumario y dos líneas de prosa sin comillas ni puntuación final («Note 7.2 to the consolidated financial statements summarizes the», URD 2021 p.300; «Note 4.6 to the Group's consolidated financial statements for the», URD 2023 p.264).
  - Fuera de las páginas del grupo, nueve títulos verdaderos (14 y 16 puntos, negrita) dejan de serlo: ocho que se parten tras una coma («3.7 REPORT BY ONE OF THE STATUTORY AUDITORS,») y uno con comillas («NOTE 6 ENGAGEMENTS FINANCIERS ET « HORS-BILAN »», DEU 2024 p.369).
- **Por qué importa** [I]. Ningún estado cambia: en esas páginas el perímetro ya queda PENDIENTE por la cabecera de la página. Es un criterio de puntuación, no de título.
- **Corrección propuesta.** Rechazar también «Note N to the…», y admitir la coma final cuando la línea siguiente continúa el título. O declararlo como límite.

### T7 · forma · respuestas (séptima parte), informe §1, E9, T14 y punto de recuperación · frases más fuertes que su prueba o recuentos inexactos

- (a) **Séptima parte, informe §1 y punto de recuperación §2:** las 346 aceptaciones son todas «filas de saldo con la fecha en el rótulo». Son 341 cifras de saldos; una es el año de una línea de prosa y cuatro son el día de la fecha o la pestaña del margen (§4.3). La propia salida que se cita (`revisor6_clases_6_sobre_C16.txt`, D) empieza por la línea de prosa. Con los años sueltos, que ese barrido excluye, son 411.
- (b) **Séptima parte:** «Otras 99 pasan de FALLO a OK en ejercicio sin quedar OK en la fila». Las 99 son todas las que pasan de FALLO a OK en ejercicio en las páginas del grupo (`revisor6_clases_6_sobre_C16.txt`, A). Seis de ellas sí quedan OK en la fila y están entre las 346; las otras son 93. Y 208 más pasan de PENDIENTE a OK en ejercicio sin quedar OK (548 menos 340), que no se cuentan. De las 65 con la cabecera de otro ejercicio, 63 son de los planes de acciones y dos, de la tabla del número de acciones (URD 2021 p.291).
- (c) **E9:** la lista corregida de identidades de las 97 entradas sigue citando **R36 de 2021–22**. Ninguna de las 97 interviene en ella: sus entradas son el CFO, el capex neto, los intereses, el principal y el free cash flow de esos años, que no mueven la referencia (`sondas_8.txt`, 3; también en la salida del revisor n.º 7). Es el mismo defecto que S6 e señaló en R23. Y para 2023–25 la lista nombra dos identidades de las 18 en que intervienen. La conclusión no cambia: las 97 tienen identidad entre páginas.
- (d) **T14 e informe §1:** «debe aceptar […] los saldos de apertura y de cierre del estado de cambios en el patrimonio» y «aunque esté partido» (T3).
- (e) **T14 e informe §1:** la tabla con una columna por país y sin unidades «deja el perímetro PENDIENTE» (T4).
- (f) **Séptima parte, tabla de resultados:** «Scripts de los revisores n.º 1 a 5: mismas salidas que sobre C14, salvo `clases_5`». `revisor5_barrido_tablas_sobre_C16.txt` difiere de la de C14 en 220 líneas una vez igualada la etiqueta: 400 candidatas más y 310 más en OK. Es el efecto de la regla de S1 y de la pestaña en ese barrido, y es lo esperable, pero no se dice.
- (g) **Séptima parte, tabla de resultados:** «`reproduccion_7.py`: todas las cifras y salidas, idénticas». La salida guardada dice «Manifiesto: 243 de 251 […] código 1» (T8 e).
- **Corrección propuesta.** Ajustar cada frase a lo que su prueba cubre.

### T8 · forma · varios

- (a) **El argumento retirado sigue escrito.** T14: «la columna del grupo no es la del grupo consolidado» para «una marca, una firma auditora». Sexta parte, R2: «Además, la columna de una firma es un desglose por firma, no el total del grupo», sin nota de precisión.
- (b) `PUNTO_DE_RECUPERACION.md`, §5, paso 4: manda leer «las partes quinta y sexta» de las respuestas. La vigente es la séptima; la frase no cambia desde C15.
- (c) La cabecera de `verificar_cifras.py` describe `dos_columnas` solo por la columna del token. No dice que, desde C16, una fila con la fecha de un saldo en el rótulo toma el ejercicio de la fila. Tampoco recoge en «perimetro» la regla de S2.
- (d) Informe §1 y séptima parte: el motivo inexacto, atribuido solo al URD 2022 p.305. Retiene también la tabla por marca de los URD 2021 y 2023 (§5 a).
- (e) `resultados/revisor7_reproduccion_7_sobre_C16.txt` no es la salida del script sobre el congelado. Dice 243 de 251: se generó sobre un árbol anterior, con 251 entradas en el manifiesto y ocho huellas que no coincidían [I]. Sobre C17 da 274 de 274; el resto de la salida es idéntico.
- (f) `REGISTRO_CONFIGURACION.md`: la fila de la copia de la revisión n.º 7 dice «comprueba la copia blob a blob», en presente y sin el recuento ni el commit que dan las filas anteriores («16/16 blobs iguales a los de 9711f04»). La copia es idéntica: 15 de 15 archivos iguales a los de d192cab.

---

## 8. Coherencia entre documentos (alcance 5)

He leído la séptima parte de las respuestas y las precisiones de C16 en la quinta y la sexta, el informe (§0, §1, §2, §12 y §13), la especificación (E9, T12 y T14), el README, `ESTADO.md`, `REGISTRO_CONFIGURACION.md` y `PUNTO_DE_RECUPERACION.md`.

- **Recuentos.** Coinciden entre sí y con las salidas: 752 = 713 + 39; 738, 14 y 0; 117 = 23 + 23 + 71, y los 23 PENDIENTE que desglosa el informe §0.1 suman (1 + 1 + 2 + 6 + 11 + 2); 292 = 136 + 127 + 29; 126 residuos (88 entre páginas y 38 de la misma página); 419 = 246 + 140 + 2 + 31; 8 de 55 páginas, con 24 entradas; 24 casos; 530 = 386 + 2 + 23 + 8 + 111; 713/713; 97; umbrales 145, 99, 2 y 0; `detecta_desde_unidades` 5, 112, 69, 17, 33 y 10. Los nueve casos nuevos del test son dos positivos (A1 y A10), dos PENDIENTE (D1 y D5) y cinco contraejemplos (A8, A9, B1, B3 y C1).
- **Hashes y alcance.** C16 y C17, bien registrados. El congelado solo añade el hash. El alcance del punto de recuperación, `git diff f1dd6c5 C16`, es el del encargo.
- **Estado y registro.** Describen bien la pasada 7 y C16, y dejan esta pasada pendiente.
- **Reproducción (§13).** Los comandos funcionan tal como están escritos.
- **Afirmaciones comprobadas y ciertas:**
  - «las 752 filas reales no cambian» y «la salida del verificador es idéntica byte a byte»;
  - lo que se dice de los casos A–E del revisor n.º 7 y de los F–I del n.º 6 sobre C16;
  - «los saldos del estado de cambios en el patrimonio de las cinco publicaciones» y de las siete clases de tablas de movimientos;
  - «las cuatro que pasan de OK a FALLO en ejercicio son saldos cuya fecha en el rótulo no es la del ejercicio declarado»;
  - en los planes de acciones, «la fecha del saldo da el ejercicio de la cifra y la columna es el año de concesión»;
  - «las dos filas reales en una línea así («5 · Linen purchases») no cambian»;
  - el coste de la decisión (b): 176 cifras;
  - `detecta_desde_unidades`, «por encima de ±0,1» y «de 0,1 a 0,5» en E9.
- **Afirmaciones más fuertes que su prueba:** las de T7.
- **T14.** Recoge las reglas nuevas con sus casos. Le faltan los límites de T1 a T4, que son de esas reglas, y conserva el argumento retirado.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo su premisa, los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**Sobre el verificador** [I]. C16 corrige bien lo que se le señaló: los casos A–D de la revisión n.º 7 quedan como se pidió (los E son los límites declarados), y las reglas de S3 y de S4 no tienen efectos fuera de su objeto. La regla de la fila con fecha es de otra clase que las anteriores: no retiene, acredita. Es la primera que da el ejercicio sin mirar la cabecera, y por eso abre lo que la cabecera cerraba por accidente: 341 cifras legítimas, y con ellas la columna sin comprobar y las líneas que no son filas. Sus fallos van en los dos sentidos previsibles de una regla sobre el texto del rótulo: se dispara donde hay una fecha y no hay saldo, y no se dispara donde hay saldo y la rejilla parte la fecha. Lo que sostiene las cifras reales sigue siendo la segunda línea: las identidades entre páginas y la Historia.

**No comprobado en esta pasada:**
- Lo que no cambia entre C15 y C17, salvo lo que hizo falta para reproducir.
- Los §3 a §11 del informe y el resto de la especificación: no cambian en el alcance.
- La prueba de caja no nula con LibreOffice: no cambia desde C4 y no la he repetido.
- Los scripts de las revisiones n.º 1 a 5 sobre C16: no los he vuelto a ejecutar; solo he comparado las salidas guardadas.
- Las candidatas del barrido una a una. He leído las líneas que digo en §1.
- Con el perímetro de un segmento solo he evaluado la dimensión de perímetro, no las seis, salvo en T6b y T6c.
- Clases de error que mis filtros no señalan. Mi lectura de cabeceras por país usa la rejilla de `pdftotext`.
- La excepción «Total» o «Group» de `cabecera_de_paises`: sin caso real.
- Cuántas tablas retiene el título corto de una tabla anterior más allá de las de las marcas (S7 d).
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

Hacen falta PyMuPDF, que el entorno no trae (`pip install --target <carpeta> pymupdf`, y esa carpeta se pasa con `--pylibs`), pypdfium2 y, para los scripts de la revisión n.º 6, pdfplumber. Versiones usadas: Python 3.13, poppler 24.02 (`pdftotext`, `pdftoppm`), PyMuPDF 2.1 (MuPDF 1.28.6), pypdfium2 5.13.0 y pdfplumber 0.11.10 (pdfminer 20260107).

```bash
B=docs/validacion_economica_paralela/frente_E_F1_elis
C15=<worktree de c96d544>/$B ; C17=<worktree de 863ddde>/$B
RAIZ=<ruta>/munger_v2_r1 ; LIBS=<carpeta con pymupdf> ; W=<carpeta de trabajo>
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
cd revision/scripts_revisor_8
python3 -I -B reproduccion_8.py --raiz "$RAIZ" --autor "$C17" --c14 "$C15" --trabajo "$W/repro8"
python3 -I -B barrido_8.py --raiz "$RAIZ" --c14 "$C15" --c16 "$C17" --todas "$W/todas8.jsonl.gz" --salida ../resultados_revisor_8/barrido_8.txt
python3 -I -B clases_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c14 "$C15" --c16 "$C17" --pylibs "$LIBS"
python3 -I -B consultas_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c14 "$C15" --c16 "$C17"
python3 -I -B contraejemplos_8.py --raiz "$RAIZ" --version C14="$C15" --version C16="$C17"
python3 -I -B lectura_saldos_8.py --todas "$W/todas8.jsonl.gz" --raiz "$RAIZ" --c16 "$C17"
python3 -I -B sondas_8.py --autor "$C17" --libro "$LIBRO"
./relanzar_revisores_6_7.sh "$RAIZ" "$C15" "$C17" <ruta>/$B/revision "$LIBS" "$W/rev67"
```

Los scripts que no llevan `--salida` escriben por la salida estándar; cada uno se guardó en el archivo de su nombre. `reproduccion_8.py` deja su salida en la carpeta de trabajo. El barrido tarda unos 15 minutos con cuatro procesos; las sondas, unos 10; los scripts de las revisiones n.º 6 y 7, unos 25.

Salidas en `revision/resultados_revisor_8/`:

| Archivo | Contenido |
|---|---|
| `reproduccion_8.txt` | Manifiesto, CSV regenerado, cadena del §13 y sondas frente a las salidas del autor; el verificador de C14 sobre el mismo CSV; la referencia de E9 en C15 y en C17 y el campo nuevo del contraste |
| `barrido_8.txt` | 51.492 tokens de las 2.026 páginas: equivalencia con la ejecución oficial; transiciones C14 → C16 de las 154.476 candidatas del grupo; los demás modos; el perímetro por segmento |
| `clases_8.txt` | Cruce con el barrido de la revisión n.º 6 (A); aceptaciones nuevas (B); líneas de la regla de S1 (C); la columna (D); saldos del estado de cambios en el patrimonio (E); fecha de la fila anterior (F); transiciones por motivo (G); S2 (H); S3 (I); S4 (J); S5 con tipografía (K); decisión (b) y S7 d (L); zona de cabecera (M); los demás modos (N) |
| `consultas_8.txt` | Desgloses que el informe cita y `clases_8.py` no imprime: líneas y páginas de las aceptaciones (Q1); transiciones de la fila por dimensión (Q2); cambios de ejercicio sin la regla de la fila (Q3); la regla frente a las columnas que C14 reconocía (Q4); tipos de las líneas que no son saldos (Q5); S2 en líneas de dos tokens o más (Q6); cambios de unidad (Q7); el epígrafe de las marcas en las cinco publicaciones (Q8); decisión (b) (Q9); el ejercicio en el universo de la revisión n.º 6 (Q10) |
| `contraejemplos_8.txt` | 25 casos sobre filas reales con el verificador oficial de C14 y de C16: T1 (columna), T2 (tokens que no son cifras), T3 (cierres no reconocidos), T4 (fecha de la fila anterior), T5 (resto de S4) y T6 (rótulos contiguos) |
| `lectura_saldos_8.txt` | Las 88 líneas con aceptaciones nuevas leídas con PDFium: rótulo, fecha y ejercicio frente a la regla del autor |
| `sondas_8.txt` | `detecta_desde_unidades` de las 246 entradas como caja negra; ±0,1 y ±0,2 en las ventas; las 97 entradas que mueven la referencia y sus identidades |
| `comparacion_6_7.txt` | Las 12 salidas de los scripts de las revisiones n.º 6 y 7 sobre C16 frente a las guardadas; las salidas guardadas de las revisiones n.º 1 a 5 sobre C14 frente a sobre C16 |

`arnes8.py` es el módulo común; `consultas_8.py` importa de `clases_8.py` sus clases de línea. Los casos de `contraejemplos_8.py` se numeran por bloque (T1 a T6) y no coinciden uno a uno con las objeciones: sus bloques T4, T5 y T6 son las objeciones T2 c, T4 y T5. El barrido completo (un archivo comprimido) no se guarda en el repositorio: se regenera con los comandos de arriba. Tampoco se guardan las salidas de los scripts de las revisiones n.º 6 y 7 sobre este commit: son idénticas a las que guarda el autor, salvo las dos líneas de `reproduccion_7`.

Algunas comprobaciones están hechas con órdenes sueltas y no con estos scripts: las diferencias entre commits (`git diff`); la lectura de páginas con `pdftotext -layout`, entre ellas la de la cabecera de la tabla en las 40 páginas con cifras aceptadas; la vista de cuatro páginas renderizadas con `pdftoppm`; la tabla de estados de los 40 casos de `contraejemplos_7` y de los 48 de `contraejemplos_6` en las salidas guardadas; las citas de los documentos del autor (`grep`); y tres recuentos menores sobre el barrido: las 336 candidatas bajo el epígrafe de las marcas en los tres URD, las dimensiones que retienen las 172 filas de §4.2 y la ausencia de saldos a 1 de enero entre las aceptadas.
