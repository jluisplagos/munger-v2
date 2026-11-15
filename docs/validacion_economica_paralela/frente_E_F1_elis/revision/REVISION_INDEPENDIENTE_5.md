# Revisión independiente n.º 5 · frente E · F1 · Elis · lo afectado por C9 y C10

Fecha: 15-nov-2026. Material revisado: commit congelado `364129afd45ba2e54a1df4141fd50e97fd55ef6d` (C11) de la rama `auditoria/economica-f1-frente-e`. C11 solo añade a C10 (`95b37e6da22bd4d5adb55c3f09c729b8d4e409f1`) el registro de su hash (comprobado: `git diff 95b37e6 364129a` toca `ESTADO.md`, una línea de las respuestas y el manifiesto). Alcance: `git diff 97441770 364129a`, es decir, C9 (`c8764494…`) y C10. Bases de comparación: C8 (`97441770…`) y C9, cada una en su propio worktree.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit a15f706.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2).
2. **Las siete filas nuevas de C9 son correctas** en página, línea, columna, ejercicio, unidad, perímetro y edición. Las he leído con dos motores distintos de `pdftotext` y a la vista, sobre la página renderizada (§3). La afirmación [P] sobre las adquisiciones de 2021 (86,9 publicado, 86,8 reexpresado) es cierta, y el límite de R39 está bien declarado.
3. **El hueco de las columnas por país está bien descrito y bien corregido para las columnas por país** (§4). La corrección tiene tres defectos, ninguno con efecto en los datos reales:
   - **la columna «published» de las tablas de reexpresión pasa como OK en las seis dimensiones, con edición «vigente»**, y la columna «restated», que es la vigente, queda PENDIENTE. Son 589 cifras en las cinco publicaciones, entre ellas el 86,9 del propio ejemplo del autor (Q1);
   - la asignación «por orden» no mira la cabecera. En el balance del URD 2021 **acepta la cifra de 2020 como de 2021 y el saldo de apertura como de 2020, y rechaza las correctas** (Q2). Es anterior a C9, pero está en la función que C9 cambia y C9 no la cubre;
   - deja PENDIENTE 25 de 75 cifras legítimas de la columna de 2020 de los estados del URD 2021, según la anchura del número, y **rebaja de FALLO a PENDIENTE** esas mismas cifras cuando se declaran de otro ejercicio (Q3).
4. **P1, P3 y P4: corregidas. P5: corregida, con un resto. P2: corregida en parte** (§5). El caso que señaló la revisión n.º 4 queda PENDIENTE, pero dentro de los mismos bloques por país siguen pasando como del grupo 89 de 376 cifras en millones, entre ellas las obligaciones de Francia del URD 2023, que es el mismo caso en otra edición (Q4).
5. **Cobertura de la unidad y del perímetro (§6).** Los recuentos del autor son exactos: 223 / 151 / 4 / 31, y 13 páginas con 41 entradas sin identidad entre páginas. Los he derivado por otra vía, sin leer su contabilidad. Dos matices:
   - en cuatro de las cinco tablas de crecimiento, que están entre esas 13 páginas, **una fila de segmento pasa como del grupo**, también como crecimiento orgánico (Q5). Los datos reales proceden de la fila TOTAL y son correctos;
   - **cinco de las 151 entradas con solo identidad de su página sí mueven los valores de referencia** (D&A total y resultado antes de impuestos de 2021 y 2022, adquisiciones de 2023). Tres frases del material dicen lo contrario (Q6).
6. **Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales. Las siete objeciones nuevas son menores o de forma.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje de la sesión autora, recibido al crearse esta sesión. Lo trato como un encargo de revisión, no como una conclusión que confirmar: no doy por cierta ninguna descripción del autor sin comprobarla.

**Configuración.** Los valores que expone el entorno se dan en la respuesta de la sesión. Aquí no se escriben identificadores de modelo.

**Límites de la independencia:**
- **La sesión autora crea esta sesión y le encarga esta pasada. El alcance lo fija ella**, y el encargo da números de página.
- **Leo los informes de los revisores anteriores** (pasadas 1, 3 y 4) y sus scripts. Esta sesión es nueva: no es la que hizo esas pasadas y no conserva su contexto. Parto de sus informes, no de su memoria, y eso también me ancla en sus conclusiones.
- **La misma herramienta de extracción puede compartir errores con el autor.** Lo he reducido donde he podido:
  - las siete filas de C9, las entradas que contrastan y la afirmación sobre el 86,9 están leídas con pdfminer y con PDFium, no con `pdftotext`, y miradas en la página renderizada con PDFium;
  - las pruebas del verificador usan `pdftotext` por fuerza: es la entrada del propio verificador. Un error de extracción común a esas pruebas no se detectaría.
- Los contraejemplos se ejecutan con `verificar_cifras.py` del autor como proceso aparte. El barrido de §4 llama a sus funciones cargadas como módulo; la equivalencia con la ejecución oficial está comprobada en las 704 y 697 filas de tabla reales de C11 y C8, sin ninguna diferencia.
- Las candidatas a falso negativo y a falso positivo del barrido las elijo con criterios míos (alineación por el borde derecho, lista amplia de países). Son heurísticas: pueden dejar clases sin ver. Lo que no he mirado está en §9.

---

## 2. Reproducción (alcance 5)

Base 4.14 materializada desde el ZIP original de la Release (1.130.912.246 bytes, SHA-256 `bb51942c…b93e`) con `tools/base_414.py`: 6.798 de 6.798, `complete: true`. Libro `d2593777…92385`. Las cinco fuentes, con la huella de `fuentes.json`. Ejecución sobre una copia del worktree de 364129a.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 177 de 177 |
| CSV regenerado desde los PDF | Idéntico (SHA-256 `ebf7edf3…0c55`) |
| Verificador: 743 filas, 729 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON idéntico. Las 70 páginas exportadas, idénticas |
| `test_verificar_cifras`: 71/71 | Reproducido. Registro idéntico |
| Contraste: 280 comprobaciones (136 del libro, 115 de fuente con 114 residuos, 29 algebraicas), 0 fallidas, 409 entradas | Reproducido. Código 0. JSON y tabla idénticos |
| `test_contraste_residuos`: 18/18 | Reproducido. Registro idéntico |
| `cobertura_por_mutacion`: 521 filas, sin incoherencias | Reproducido. Salida idéntica: 374 por identidad, 4 solo libro, 23 sin detectar, 8 leídas sin efecto y 112 no usadas |
| Sondas: 704/704 en unidad y en perímetro | Reproducido. El JSON solo difiere en la etiqueta de versión que le pasé |
| Referencias de E9 sin cambios | C53 de A1, 2,445331695332; de A2, 1,612524303305. Todo `referencia_especificacion` es igual al de C8 |
| «Las filas anteriores no cambian de estado» | Cierto: las 736 filas comunes tienen el mismo estado y el mismo detalle en las seis dimensiones en C8, C9 y C11 |
| Scripts de los revisores n.º 3 y n.º 4 sobre C10 | Reproducidos. Cinco salidas idénticas a `resultados/*_sobre_C10.txt` |

`prueba_caja_no_nula.py` y su salida no cambian desde C4 (`git diff` vacío). No la he repetido. Fuera de la carpeta del frente E no cambia nada entre C8 y C11. Las copias de los informes y scripts de los revisores en la rama del autor son iguales a las de esta rama.

---

## 3. C9 · filas nuevas (alcance 1)

**Estado de los cambios de C9** (el detalle, en este apartado y en §4):

| Cambio de C9 | Estado | Dónde |
|---|---|---|
| Siete filas nuevas del CSV | Correctas en las siete dimensiones pedidas | §3 |
| Identidades R17, R39 y R40 de 2021–22 | Correctas (residuo 0,0 las cinco). Segundas presentaciones genuinas; R40 es una reproducción de la misma cuenta | §3 |
| Afirmación [P] sobre el 86,9 y límite de R39 | Cierta; límite bien declarado | §3 |
| Descripción del hueco de las columnas por país | Exacta | §4 |
| Corrección: `cabeceras_ajenas`, `palabra_de_cabecera_mas_cercana` y `pais_de_columna` | Correcta para las columnas por país; las sociedades quedan PENDIENTE, como se declara | §4 |
| Falsos negativos que quedan | Dos clases: columna «published» (Q1) y asignación por orden (Q2, anterior a C9) | §4, §7 |
| Falsos positivos nuevos | Una clase: marca «(a)» en la cabecera, con rebaja de FALLO a PENDIENTE (Q3) | §4, §7 |
| Casos nuevos de los dos tests | Reproducidos | §2 |

Prueba: `scripts_revisor_5/lectura_filas_c9.py` → `resultados_revisor_5/lectura_filas_c9.txt`. Lectura con pdfminer (palabras con su caja; la columna se identifica por la cabecera alineada con el número) y con PDFium (el rótulo va seguido de los mismos números en el mismo orden). 23 lecturas, ninguna diferencia. Las cinco tablas, además, vistas en la página renderizada.

| Fila | Página PDF (folio) | Línea y columna [P] | Ej. | Unidad y perímetro [P] | Edición | Veredicto |
|---|---|---|---|---|---|---|
| `TAX_CORR_U22_2021` | URD 2022 p.326 (324) | «Current taxes 93.4 · 81.4», columna «12/31/2021» | 2021 | «(In millions of euros)»; nota 9 de los estados consolidados | URD 2022, vigente para 2021 | Correcta |
| `TAX_DIF_U22_2021` | ídem | «Deferred taxes (12.9) · (24.8)», columna «12/31/2021» | 2021 | ídem | ídem | Correcta |
| `CF_ADQ_NOTA_U22_2021` | URD 2022 p.277 (275) | «Net cash flow (86.8) (19.0) …», primera columna, «12/31/2021»; las doce siguientes son países | 2021 | «(In millions of euros)»; total de la nota 2.4 | ídem | Correcta |
| `TAX_CORR_U23_2022` | URD 2023 p.345 (343) | «Current taxes 120.5 · 92.6», columna «2022 restated*» | 2022 | «(In millions of euros)»; nota 9 | URD 2023, vigente para 2022 | Correcta |
| `TAX_DIF_U23_2022` | ídem | «Deferred taxes (10.1) · (12.9)», columna «2022 restated*» | 2022 | ídem | ídem | Correcta |
| `CF_ADQ_NOTA_U23_2022` | URD 2023 p.294 (292) | «NET CASH FLOW (221.7) (25.7) …», primera columna, «2022 restated*»; las cinco siguientes son sociedades | 2022 | «(In millions of euros)»; total de la nota 2.4 | ídem | Correcta |
| `IS_VENTAS_MR_U21_2020` | URD 2021 p.213 (211) | «Revenue 3,048.3 · 2,806.3 · 242.0 · 8.6%», columna «2020 restated» | 2020 | «(In millions of euros)»; «Group results» | URD 2021, vigente para 2020 | Correcta |

**¿Son segundas presentaciones genuinas y del mismo concepto?** Sí, con un matiz.
- **R17.** La línea «Tax» de la cuenta de resultados remite a la nota 9, y la tabla de la nota abre con el impuesto corriente y el diferido, que suman el «actual tax expense» [P]. Mismo concepto, otra página. 2021: 81,4 − 24,8 − 56,6 = 0,0; 2022: 92,6 − 12,9 − 79,7 = 0,0 [D]. Observación: la tabla del URD 2022 rotula la columna «12/31/2021», sin «restated», pero sus cifras son las reexpresadas (resultado neto 114,4 y antes de impuestos 171,0; lo publicado fue 114,6 y 171,1) [P].
- **R39.** La línea del EFE remite a la nota 2.4, y el total de su tabla de flujos coincide con ella los dos años [P]. Mismo concepto, otra página.
- **R40.** Es la misma cifra, pero el informe de gestión dice de su tabla que muestra «certain line items from the income statement» [P]: es una reproducción de la cuenta de resultados, no una construcción independiente. Vale como segunda página con su propia cabecera y su propia declaración de unidades. Sería más fuerte la información por segmentos del mismo URD (p.247: los siete segmentos suman 2.806,3) [P] [I].

**La afirmación [P] sobre las adquisiciones de 2021: cierta.**
- Informe de gestión del URD 2022, p.247, bajo «2021 restated»: (86,9). El total de inversión de esa tabla es (655,4) [P].
- Tabla de reexpresión, p.271: «12/31/2021 published» (86,9), «IFRS 3» 0,1, «12/31/2021 restated» (86,8); total, (655,4), 0,1 y (655,3) [P].
- EFE, p.261: (86,8) y (655,3) [P].
- Añado: el URD 2021 publicó (86,9), tanto en el EFE (p.229) como en la nota 2.4 (p.242). El ajuste de 0,1 está en la columna de Irlanda: (13,5) en el URD 2021 y (13,4) en el URD 2022 [P]. La tabla del informe de gestión arrastra, pues, las cifras publicadas bajo una cabecera que dice «restated» [I].

**El límite de R39: bien declarado.** Con 86,9 en el EFE de 2021, el residuo es +0,1 y la cota 0,10: R39 no lo distingue [D]. El test del autor lo documenta y lo he reproducido (lo detectan dos comprobaciones del libro).

---

## 4. C9 · verificador (alcance 2)

Pruebas: `contraejemplos_5.py` (casos A, B y C, con el verificador de C8, C9 y C11 como proceso aparte), `clases_5.py` (recuento por clases, C8 y C11) y `barrido_tablas.py` (48.094 candidatas: cada token numérico de las 459 páginas del grupo, declarado del grupo con el ejercicio de la publicación y con el anterior).

**¿Está bien descrito el hueco?** Sí.
- Sobre C8, Bélgica (p.277, contigua al total) daba OK en las seis dimensiones (A1). Lo mismo «Germany & Luxembourg» en la tabla de 2020 del URD 2021 p.244 (A6).
- El hueco alcanzaba solo a la columna contigua al total. Las más alejadas ya quedaban PENDIENTE en C8 porque estaban a más de 14 caracteres de la columna del ejercicio (A3–A5). El autor lo describe así.

**¿Está bien corregido?** Para las columnas por país, sí.
- Las doce columnas de país de la p.277 dan FALLO en perímetro, también Letonia y Gran Bretaña, que no están en la lista de países (A3, A4). En el barrido, 846 candidatas pasan de OK a FALLO en perímetro por esta regla.
- Las sociedades quedan PENDIENTE (A8, A9), como declara el autor.
- Detalle de forma: el motivo nombra la columna por su palabra más próxima, y sale «Great» o «&».

**Falsos negativos: columnas ajenas que aún pasan.** Dos clases (Q1 y Q2).

| Caso | Fila real | C8 | C11 |
|---|---|---|---|
| B1 | URD 2022 p.271, adquisiciones de 2021, columna «12/31/2021 published»: (86,9) | OK | **OK en las seis** |
| B2 | La misma línea, columna «12/31/2021 restated»: (86,8), la vigente | PENDIENTE | PENDIENTE |
| B7 / B8 | URD 2025 p.334, PPA de 2024: «published» (84,9) / «restated» (85,0) | OK / PENDIENTE | **OK** / PENDIENTE |
| B9 / B10 | DEU 2024 p.283, adquisiciones de 2023: «publié» (82,2) / «retraité» (82,1) | OK / PENDIENTE | **OK** / PENDIENTE |
| B11 / B12 | URD 2023 p.289, adquisiciones de 2022: «reported» (221,6) / «restated» (221,7) | OK / PENDIENTE | **OK** / PENDIENTE |
| B13 | URD 2021 p.228, balance: activos no corrientes de **2020** (7.010,1) declarados **2021** | OK | **OK en las seis** |
| B14 | Ídem: saldo de apertura «01/01/2020 Adjusted» (7.198,9) declarado 2020 | OK | **OK en las seis** |
| B15 / B16 | Ídem: las cifras correctas de 2021 (7.065,5) y de 2020 (7.010,1) | FALLO | **FALLO** |
| B17 / B18 | URD 2025 p.366, vencimientos: total de flujos sin descontar (856,9) / valor en libros (703,2), declarados 2025 | OK / FALLO | **OK** / FALLO |

**Falsos positivos: filas legítimas que quedan PENDIENTE** (Q3).

| Caso | Fila real | C8 | C11 |
|---|---|---|---|
| C1 | URD 2021 p.226, resultado antes de impuestos de 2020: 29,7 | OK | **PENDIENTE** («bajo la cabecera «(a)»») |
| C3 | Ídem, resultado neto de 2020: 2,7 | OK | **PENDIENTE** |
| C4 | Control: ventas de 2020, 2.806,3 (número ancho) | OK | OK |
| C2 | El 29,7 declarado 2021: ejercicio equivocado | **FALLO** | **PENDIENTE** |
| C5 / C6 | URD 2021 p.229, pagos en acciones de 2020 (12,9): declarado 2020 / declarado 2021 | OK / FALLO | **PENDIENTE / PENDIENTE** |

Las demás transiciones de OK a PENDIENTE del barrido son tablas con varias medidas bajo una misma fecha (valor en libros y valor razonable, bruto y deterioro) o con columnas que no son ejercicios (variación del patrimonio, vencimientos). Ahí PENDIENTE es razonable [I].

---

## 5. C10 · respuestas a P1–P5 (alcance 3)

| Objeción | Estado | Prueba |
|---|---|---|
| P1 · recuento sin rótulo de recuento | **Corregida** | D1 y D2 quedan PENDIENTE y el control D3, FALLO. En las cinco publicaciones hay 238 enteros de seis cifras o más en páginas del grupo: 23 daban OK en unidad en C8 y **ninguno en C11** (`clases_5.txt`, N). Los 23 son recuentos de acciones [P] |
| P2 · bloque de un país bajo su título | **Corregida en parte** | E1 queda PENDIENTE. Pero en los mismos bloques siguen pasando 89 de 376 cifras en millones y 83 de 209 porcentajes (E2–E7; `clases_5.txt`, P). Q4 |
| P3 · la identidad de la misma página | **Corregida** | `cobertura_entradas` dice qué acredita cada clase, marca cada entrada y lista las 13 páginas. Recuento propio idéntico (§6). Tres frases quedan más fuertes que su prueba (Q6) |
| P4 · el caso de los pagos en 178,0 | **Corregida** | El test separa las clases: 1 comprobación de fuente y 41 del libro. Informe §1 y respuestas, alineados |
| P5 · dos frases absolutas | **Corregida, con un resto** | Las dos frases señaladas están matizadas. La misma frase absoluta sigue en la tabla de N1 de las respuestas (fila «B1, B2»), y C10 añade otras dos sobre el título (Q4, Q7) |

**P1 · ¿demasiado amplio o demasiado estrecho?** En estas cinco publicaciones, ni lo uno ni lo otro [D]:
- *Amplio.* No marca ningún importe legítimo. Los 23 tokens que pasan de OK a PENDIENTE están en 12 líneas, todas de acciones: los efectos de dilución de las cinco ediciones, la autocartera del URD 2021 («Treasury shares (a) 117,289») y, en la edición francesa, «Nombre moyen pondéré d'actions 235 896 652», que en C8 pasaba porque la lista busca «nombre d» (D4). Los importes legítimos en millones sin decimales que hay (tablas de sensibilidad del deterioro, hasta 3.272) tienen cuatro cifras y no se marcan (D6).
- *Estrecho.* Entre las candidatas del barrido que quedan OK en todas las dimensiones no hay ningún recuento de menos de seis cifras: los que hay caen por el rótulo, por la declaración de otra unidad o porque su página no declara unidad.
- *Tablas francesas.* El separador de miles con espacio y la coma decimal se tratan bien (D4).
- *Límite.* Fuera de estas publicaciones el criterio no protege de recuentos de menos de seis cifras (plantilla, centros) ni de magnitudes con decimales que no son importes (años, ratios). Y se evalúa antes que la declaración de unidades: un entero largo de una tabla en otra unidad quedaría PENDIENTE y no FALLO. No hay ningún caso real en las páginas del grupo (0 transiciones de FALLO a PENDIENTE en unidad). Conviene decirlo en T14 [I].

**P2.** Lo que encuentro está en Q4. El positivo del autor (total por países, 67,1, bajo «INFORMATION BY REGION») sigue en OK (E19).

---

## 6. Cobertura de la unidad y del perímetro (alcance 4)

Prueba: `cobertura_propia.py` → `resultados_revisor_5/cobertura_propia.txt`. El autor clasifica cada entrada con la contabilidad interna del contraste, y su prueba de mutación no distingue «entre páginas» de «misma página»: en las dos falla «una identidad de fuente». Yo derivo la clase del comportamiento, sin leer esa contabilidad:
- muto cada entrada y anoto qué residuos fallan;
- un residuo es «entre páginas» si las entradas que lo hacen fallar están en dos páginas o más del CSV, y «de una página» si están en una. De los 114 residuos salen 76 y 38, con las mismas páginas que declara el autor en los 114;
- la clase de una entrada es la del mejor residuo que su mutación hace fallar.

| Declarado por el autor | Recuento propio | ¿Coincide? |
|---|---|---|
| 223 con identidad entre páginas | 223 | Sí, entrada por entrada |
| 151 solo de su página | 151 | Sí |
| 4 solo con la Historia del libro | 4 | Sí |
| 31 sin segunda línea | 31 (23 cambian alguna salida sin que nada falle; 8 se leen sin efecto) | Sí |
| 13 de 52 páginas sin identidad entre páginas, con 41 entradas, 25 de ellas con solo identidad de su página | 13, 41 y 25; las mismas páginas y las mismas entradas | Sí |
| Ninguna de las 41 cambia la referencia | 0 de 41 | Sí |
| Ninguna de las 31 ni de las 4 cambia la referencia | 0 de 31 y 0 de 4 | Sí |

**¿Hay entradas cuya unidad o perímetro se presenten como acreditados sin serlo?** En los recuentos, no. En tres frases, sí (Q6):
- 97 entradas mueven la referencia. 92 tienen identidad entre páginas. **Cinco solo la tienen de su página:** `DA_TOTAL_U22_2021`, `DA_TOTAL_U23_2022`, `IS_BAI_U22_2021`, `IS_BAI_U23_2022` y `CF_ADQ_FR_2023`. La tabla del autor las clasifica bien; lo que falla es el texto.
- Atenuante [I]: las cinco están en páginas que sí tienen otras entradas contrastadas entre páginas, de la misma tabla. Su tabla está anclada; la cifra, no.
- Una de las 223 descansa en una contraparte PENDIENTE: `DA_ROU_U22_2021` solo tiene R16 de 2021, frente a `LS_AMORT_ROU_2021`. Está declarado.

**Las 13 páginas.** El autor las presenta como cobertura pendiente, no acreditada, y eso es exacto. Añado una prueba de por qué importa y una vía para cerrarlas en parte:
- En cuatro de las cinco tablas de crecimiento, una fila de segmento declarada del grupo queda OK en las seis dimensiones (Q5). Las entradas reales proceden de la fila TOTAL, que el literal y la etiqueta fijan: son correctas [P].
- El crecimiento publicado se puede contrastar entre páginas con las ventas de las cuentas de resultados [D]:

  | Ejercicio | Ventas / ventas del año anterior | Publicado | Residuo | Cota |
  |---|---|---|---|---|
  | 2021 | 3.048,3 / 2.806,3 → 8,623 % | 8,6 % | −0,023 | 0,054 |
  | 2022 | 3.820,9 / 3.048,3 → 25,345 % | 25,3 % | −0,045 | 0,054 |
  | 2023 | 4.309,4 / 3.820,9 → 12,785 % | 12,8 % | +0,015 | 0,053 |
  | 2024 | 4.573,7 / 4.309,4 → 6,133 % | 6,1 % | −0,033 | 0,052 |
  | 2025 | 4.796,8 / 4.573,7 → 4,878 % | 4,9 % | +0,022 | 0,052 |

  Las cinco cierran. Con esa identidad, `CREC_PUB` quedaría contrastada entre páginas, las cinco páginas de crecimiento dejarían de estar sin ancla, y una fila de segmento rompería la identidad (el Reino Unido e Irlanda de 2021 publica 19,4 %).

---

## 7. Objeciones nuevas

Todas las filas existen en el PDF [P]. Ninguna afecta a una fila real del CSV.

### Q1 · menor · `verificar_cifras.py`, ejercicio y edición · la columna «published» pasa como edición vigente

- **Prueba.** `contraejemplos_5.txt`, B1–B12; `clases_5.txt`, R. En las tablas de reexpresión de la nota 1.4 de las cinco publicaciones (URD 2021 p.236–239, URD 2022 p.268–271, URD 2023 p.286–289, DEU 2024 p.280–283 y URD 2025 p.334–337):
  - 589 cifras de la columna «published», «reported» o «publié», declaradas del ejercicio comparativo y con edición «vigente»: **589 OK en las seis dimensiones**;
  - las 589 de la columna «restated» o «retraité», que son las vigentes: 589 PENDIENTE.
- **Causa** [D]. «published», «reported» y «publié» están en la lista de calificadores, así que no cuentan como cabecera ajena. Y de dos columnas del mismo año la cabecera solo guarda la de más a la izquierda, que es la publicada. La dimensión de edición mira el pie de la página, no la columna.
- **Por qué importa.** Es el caso que el propio informe describe en §2: una cifra publicada antes de la reexpresión, impresa en la publicación vigente. El verificador le pone «edición vigente (2022) para 2021». La segunda línea solo la detecta si la diferencia supera la cota, y en adquisiciones es de 0,1 (2021, 2022 y 2023).
- **Corrección propuesta.** Tratar esas palabras como marca de edición anterior: FALLO en edición si la fila se declara vigente. Reconocer por separado las dos columnas del mismo año, de modo que la reexpresada pueda quedar OK. Añadir B1, B2 y B7–B12 al test y a T14, y nombrar esta clase entre los límites de las respuestas.

### Q2 · menor · `verificar_cifras.py`, ejercicio · la asignación «por orden» acepta la columna equivocada y rechaza la correcta

- **Prueba.** B13–B19. El balance del URD 2021 (p.228) tiene tres columnas de saldo: «12/31/2021», «12/31/2020 Restated (a)» y «01/01/2020 Adjusted (a)».
  - En las filas sin referencia a nota hay tres números y la cabecera da tres columnas reconocidas («Notes», 2021 y 2020, porque los dos «2020» cuentan una vez). Se asignan por orden: el saldo de 2021 a «Notes», el de 2020 a 2021 y el de apertura a 2020.
  - Resultado: 7.010,1 (2020) declarado 2021, OK; 7.198,9 (apertura) declarado 2020, OK; las dos declaraciones correctas, FALLO.
  - Lo mismo, con otra forma, en las tablas de vencimientos de los arrendamientos (URD 2025 p.366, DEU 2024 p.312, URD 2023 p.321): el total de flujos sin descontar pasa como el ejercicio y el valor en libros da FALLO.
- **Alcance.** Existe ya en C8: no lo introduce C9. Lo traigo porque C9 corrige esta función y solo añade la comprobación de cabeceras ajenas a la rama de alineación. Ninguna fila real procede de esas tablas. De las nuevas, es la más seria: no es una señal que falta, es un veredicto invertido en un estado principal.
- **Corrección propuesta.** No asignar por orden sin comprobar la alineación de cada número con su cabecera; si no coinciden, PENDIENTE. Contar como columnas distintas dos fechas distintas del mismo año. Añadir B13–B18 al test y a T14.

### Q3 · menor · `verificar_cifras.py`, ejercicio (C9) · una marca de nota en la cabecera deja PENDIENTE cifras legítimas y rebaja de FALLO a PENDIENTE las de otro ejercicio

- **Prueba.** C1–C6; `clases_5.txt`, S. Cuenta de resultados, resultado global y EFE del URD 2021 (p.226, 227 y 229), columna «12/31/2020 restated (a)», 75 cifras:
  - declaradas 2020: 75 OK en C8; **50 OK y 25 PENDIENTE en C11**. Depende de la anchura del número: con tres caracteres quedan PENDIENTE 14 de 19; con seis o más, ninguna;
  - las mismas declaradas 2021: 75 FALLO en C8; **50 FALLO y 25 PENDIENTE en C11**.
  - En el barrido completo, 2.112 candidatas con el ejercicio equivocado pasan de FALLO a PENDIENTE; en 954 la cabecera del otro ejercicio está alineada sobre el número.
- **Causa** [D]. La marca «(a)» no está entre los calificadores (sí «(1)» y «*»), y la comprobación de cabeceras ajenas va antes que la del ejercicio. Si «(a)» queda más cerca del centro del número que el «2020» de la fecha, la fila sale PENDIENTE sin llegar a comparar el año.
- **Por qué importa.** `contraste_f1.py` se niega a calcular con un FALLO, pero calcula con una PENDIENTE y termina con código 2. Para estas filas, C9 debilita la corrección de N1 que la revisión n.º 4 dio por buena.
- **Corrección propuesta.** Agrupar las palabras de cabecera en celdas y no tratar como ajena la que está en la celda de la columna reconocida; añadir las llamadas con letra a los calificadores; si la columna reconocida más próxima es de otro ejercicio, mantener FALLO. Añadir C1, C2 y C5 al test.

### Q4 · menor · `verificar_cifras.py`, perímetro (P2) · el criterio de título deja pasar la mayor parte de lo que hay bajo un título de país

- **Prueba.** E1–E7, E18; `clases_5.txt`, P. Bloques «X – DETAILS» y «DÉTAIL POUR X» de la nota de pensiones de las cinco publicaciones:
  - cifras en millones: 376. OK en C8, 293; **OK en C11, 89** (URD 2023, 32; URD 2025, 22; DEU 2024, 21; URD 2022, 14);
  - porcentajes: 209. OK en C8, 202; OK en C11, 83.
  - Ejemplos que quedan OK en las seis dimensiones: obligaciones de **Francia** de 2022, 40,1, en el URD 2023 p.308 (el grupo, 410,7 en la p.307): es el caso B1 de la revisión n.º 4 en otra edición; activos del plan del **Reino Unido**, 243,5, y de Irlanda, 24,2 (URD 2025 p.358 y p.357; el grupo, 347,3); obligaciones de Irlanda con el título en la página anterior (URD 2022 p.291); tasa de descuento de Francia en el mismo bloque del caso B1 (URD 2025 p.356).
  - Falso positivo: el total de clientes y activos por contratos del **grupo**, 824,1 (DEU 2024 p.321), queda PENDIENTE porque una línea de prosa por encima nombra el Reino Unido.
- **Causa** [D]. La regla solo mira por encima de la línea de unidades, hasta 15 líneas, y se queda con la primera línea corta sin cifras. No ve el título cuando:
  - el bloque tiene varias tablas y la segunda o la tercera están a más de 15 líneas;
  - el título quedó en la página anterior;
  - la fila está por encima de la línea de unidades (la tabla de hipótesis, en porcentaje);
  - entre el título y la tabla hay prosa de más de 60 caracteres por línea (URD 2023 p.308).

  Además, si la declaración de unidades va sola en su línea, el resto «()» se toma como título y la búsqueda termina ahí. Comprobado con la función sobre líneas construidas; no he encontrado una página real.
- **Frases más fuertes que la prueba.** Informe §1: «una tabla cuyo título más próximo nombra un país […] deja el perímetro del grupo PENDIENTE». T14: «no se acepta como del grupo». Respuestas, P2: «Límite: no se detecta un bloque de otro perímetro sin título ni rótulo que lo nombre». El bloque de Francia del URD 2023 tiene título y no se detecta.
- **Corrección propuesta.** Seguir el bloque, no la tabla: desde un título que nombra un país o un segmento hasta el siguiente título del mismo nivel, también a través del salto de página, y para todas las filas, lleven o no declaración de unidades. Exigir que el título sea una línea propia, no prosa. Añadir E2–E7 y E18 al test y a T14, y alinear las tres frases.

### Q5 · menor · `verificar_cifras.py`, perímetro · filas de segmento, de país o de UGE que no están en las listas pasan como grupo, también en las tablas que el autor usa

- **Prueba.** E8–E17; `clases_5.txt`, G.
  - Tablas de crecimiento del informe de gestión: en cuatro de las cinco publicaciones pasan como del grupo, en ventas y en crecimiento orgánico, las filas «Scandinavia and Eastern Europe» y «United Kingdom and Ireland» (URD 2021 p.211), «Eastern Europe» y «and Ireland» (rótulo partido, URD 2022 p.243), «Ireland» (URD 2023 p.261) y «de l'Est» y «Royaume-Uni et Irlande» (DEU 2024 p.253). En el URD 2025 p.307, ninguna.
  - Fondo de comercio de la UGE Francia, 1.442,9 (URD 2025 p.363): OK. «République d'Irlande (Eire)», 109,3 (DEU 2024 p.292): OK; la fila «France» de esa tabla, FALLO.
- **Causa** [D]. El rótulo se compara literalmente con la lista: no casa «and» por «&», «et» por «&», la segunda línea de un rótulo partido, un prefijo («CGU») ni «République d'Irlande».
- **Por qué importa.** Las cuatro tablas de crecimiento están entre las 13 páginas sin identidad entre páginas, donde el informe dice que el perímetro descansa en estas reglas. R32, que es de la misma página, cuadra igual con una fila de segmento entera. `CREC_ORG_2021` no tiene ninguna segunda línea.
- **Corrección propuesta.** Un criterio de estructura en lugar de más rótulos: en una tabla con fila TOTAL, las filas que la preceden no son del grupo. Normalizar los rótulos y unir los partidos. Añadir la identidad entre páginas del crecimiento publicado (§6). Añadir E8, E9, E11–E13, E15 y E16 al test y a T14.

### Q6 · menor · especificación E9, punto de recuperación y respuestas · tres frases sobre la referencia más fuertes que su prueba

- **Qué dice el material.**
  - E9: el C53 de referencia depende, entre otras, de la «D&A total» y las adquisiciones de cada año, y «desde C9 todas tienen una identidad entre páginas».
  - `PUNTO_DE_RECUPERACION.md` §3.2 y respuestas, «Lo que queda abierto tras C10»: tras listar las 41 entradas de las 13 páginas, las 151 con solo identidad de su página y las 31 y 4, «ninguna de ellas cambia la referencia de la especificación».
- **Prueba.** `cobertura_propia.txt`. Cinco de las 151 mueven `referencia_especificacion`: `DA_TOTAL_U22_2021` y `DA_TOTAL_U23_2022` (solo R25, de su página), `IS_BAI_U22_2021` e `IS_BAI_U23_2022` (solo R35) y `CF_ADQ_FR_2023` (solo R29). `cobertura_entradas` del autor las clasifica así; `cobertura_por_mutacion.py` no mira esa clase.
- **Corrección propuesta.**
  - Corregir las tres frases: valen para las 41, las 31 y las 4, no para las 151.
  - Dar a esas cinco una identidad entre páginas. Para dos pares basta con páginas ya citadas: el resultado antes de impuestos de la nota 9 es 171,0 en el URD 2022 p.326 y 282,3 en el URD 2023 p.345, iguales a los de la cuenta de resultados [P]; las adquisiciones de 2023 reexpresadas, (82,1), están en el DEU 2024 p.283 [P]. Para la D&A total de 2021–22 sirve la identidad que ya se usa en 2023–25 con la línea del EFE.
  - Hacer que `cobertura_por_mutacion.py` informe del efecto en la referencia también para «solo misma página».

### Q7 · forma · varios

- (a) Informe §0.11: dice que la revisión de lo corregido «está pendiente». §12 dice que las pasadas 3 y 4 están hechas y que lo pendiente es C9 y C10.
- (b) `PUNTO_DE_RECUPERACION.md`: «hacia las 22:45 UTC». El commit que lo contiene es de las 22:27:44 UTC.
- (c) Respuestas, tabla de N1, fila «B1, B2»: sigue la frase absoluta que P5 pidió matizar.
- (d) Respuestas, C9, «Límite que queda»: solo nombra las columnas por sociedad. Faltan las de Q1 y Q2.
- (e) README, fila del test: falta una coma entre «revisión n.º 3» y «las columnas por país».
- (f) El motivo del FALLO de perímetro nombra la columna como «Great» o «&».

---

## 8. Coherencia entre documentos (alcance 6)

He leído las partes tercera y cuarta de las respuestas, el informe (§0, §1, §2, §3, §12 y §13), la especificación (E9, T12 y T14, por sus diferencias), el README, `ESTADO.md`, `REGISTRO_CONFIGURACION.md` y `PUNTO_DE_RECUPERACION.md`.

- **Recuentos.** Coinciden entre sí y con las salidas: 743 = 704 + 39; 729, 14 y 0; 71 = 15 + 5 + 51; 280 = 136 + 115 + 29; 114 residuos; 409 = 223 + 151 + 4 + 31; 13 de 52 páginas, 41 entradas y 25; 18 casos; 521 = 374 + 4 + 23 + 8 + 112; 704/704. No queda ningún recuento de C8 en los documentos principales.
- **Las 13 páginas.** «Las tablas de crecimiento, las de deuda neta y las de impuestos diferidos y cuatro páginas sueltas» suma 13 si la tabla de 2021 se cuenta como suelta (4 + 2 + 3 + 4). Coherente.
- **Estado y registro.** Describen bien C9, C10 y la pasada 4, y dejan esta pasada pendiente.
- **Cronología de C9.** El autor dice que halló el hueco hacia las 22:05 UTC sin haber leído el informe de la revisión n.º 4 (22:04 UTC), y que git no puede acreditar el orden. No lo puedo comprobar. La revisión n.º 4 no señala ese hueco, así que la cuestión no tiene consecuencia.
- **Afirmaciones más fuertes que su prueba:** las de Q4 (tres frases sobre el criterio de título) y las de Q6 (tres frases sobre la referencia). No encuentro otras en lo leído.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo su premisa, los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**No comprobado en esta pasada:**
- Lo que no cambia entre C8 y C11, salvo lo que hizo falta para reproducir.
- Los §4 a §11 del informe y el resto de la especificación: no cambian en el alcance.
- La prueba de caja no nula con LibreOffice: no cambia desde C4 y no la he repetido.
- La D&A total de 2021 y 2022 en una segunda página. Las otras tres entradas de Q6 sí las he leído.
- Las candidatas del barrido una a una: he revisado las clases y un ejemplo de cada una, no las 48.094.
- Clases de falso negativo que mis heurísticas no señalan. El barrido no es exhaustivo.
- Las páginas fuera de las que el verificador acepta como del grupo, y las filas de prosa.
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

```bash
B=docs/validacion_economica_paralela/frente_E_F1_elis
C8=<worktree de 9744177>/$B ; C9=<worktree de c876449>/$B ; C11=<worktree de 364129a>/$B
RAIZ=<ruta>/munger_v2_r1
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
cd revision/scripts_revisor_5
python3 -I lectura_filas_c9.py --raiz "$RAIZ" --autor "$C11"                              # pdfplumber y pypdfium2
python3 -I contraejemplos_5.py --raiz "$RAIZ" --version C8="$C8" --version C9="$C9" --version C11="$C11"
python3 -I clases_5.py --raiz "$RAIZ" --anterior C8="$C8" --nueva C11="$C11"
python3 -I barrido_tablas.py --raiz "$RAIZ" --nueva "$C11" --anterior "$C8" --salida ../resultados_revisor_5
python3 -I cobertura_propia.py --autor "$C11" --libro "$LIBRO"
```

Salidas en `revision/resultados_revisor_5/`:

| Archivo | Contenido |
|---|---|
| `lectura_filas_c9.txt` | Las siete filas, las cinco entradas que contrastan y la afirmación sobre el 86,9, leídas con pdfminer y PDFium; identidades R17, R39 y R40 con fracciones exactas |
| `contraejemplos_5.txt` | Casos A (columnas por país), B (columnas que aún pasan), C (falsos positivos y FALLO → PENDIENTE), D (P1) y E (P2 y perímetro), con el verificador de C8, C9 y C11 |
| `clases_5.txt` | Recuento por clases con la ejecución oficial de C8 y C11: tablas de reexpresión, bloques por país, tablas de crecimiento, estados del URD 2021 y enteros largos |
| `barrido_tablas.txt` | 48.094 candidatas de las 459 páginas del grupo: transiciones de estado entre C8 y C11 y candidatas a falso negativo y a falso positivo (listas recortadas a 40 por clase) |
| `cobertura_propia.txt` | Clase de cada entrada derivada por mutación, páginas sin identidad entre páginas y efecto en la referencia |

`arnes.py` es el módulo común de los scripts. No se guardan aquí las salidas de los scripts de los revisores anteriores sobre este commit: son idénticas a las que el autor guarda en `resultados/*_sobre_C10.txt`.
