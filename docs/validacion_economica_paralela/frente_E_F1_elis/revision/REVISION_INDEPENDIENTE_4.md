# Revisión independiente n.º 4 · frente E · F1 · Elis · lo afectado por C7

Fecha: 15-nov-2026. Material revisado: commit congelado `97441770f51761e28c089df7830d3de802bf87e9` (C8) de la rama `auditoria/economica-f1-frente-e`. C8 solo añade a C7 (`9869def325b8820e2ee25618107495a7a7b70229`) el registro de su hash. Bases de comparación: f30c66c (C6) y 1864c4e.

Se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit 034301c.

Marcas: **[P]** publicado (leído en el PDF) · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis.

Este documento no contiene valoraciones, precios, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna decisión pendiente. Se conservan C48 = 108 y E1/D3/E2/E6. No modifica el material del autor, el producto ni los libros.

Nota de nombres: las objeciones nuevas de esta pasada se numeran P1–P5, como pide el encargo. No son los contraejemplos «P1» y «P2a» de la adenda de la revisión n.º 3, a los que aquí me refiero por su contenido (ventas de Alemania, fila «Other»).

---

## 0. Resultado en breve

1. **Las cifras que declara el autor se reproducen todas**, con salidas idénticas byte a byte (§2).
2. **N2–N10: corregidas. N1: corregida en parte.**
   - En N1 queda corregido todo lo que señalé sobre el ejercicio, el modo declarado y el concepto de la columna, y el informe dice ya que OK significa «sin incoherencia detectada», no «acreditada».
   - Las reglas nuevas de unidad y de perímetro son listas de rótulos. Detectan los casos conocidos y dan OK por defecto a lo que no figura en la lista.
3. **Tres filas reales nuevas pasan como OK en todas las dimensiones** sobre el commit congelado (P1 y P2):
   - dos recuentos de acciones declarados en millones de euros (URD 2025 p.395);
   - las obligaciones de pensiones de Francia, 45,2, declaradas del grupo (URD 2025 p.356; el grupo son 414,4).
4. **Respuesta a la pregunta de la persona responsable (§6).** La unidad y el perímetro no quedan acreditados por las reglas del verificador. Solo los acredita, de forma indirecta, una identidad entre páginas o la comparación con el libro. De las 402 entradas usadas, eso cubre 211 y 9. Las 151 con identidad solo de su misma página tienen acreditada la coherencia interna de su tabla, no su unidad ni su perímetro (P3). Las 31 restantes no tienen segunda línea.
5. **Lo que el autor dice de mis scripts es cierto en los cuatro puntos** (§5). Uno de ellos es un defecto de mi script de la revisión n.º 3, que reconozco. No afecta a los resultados que publiqué entonces.
6. **Ninguna conclusión material cambia.** No he encontrado ningún error en los datos reales.

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje de la sesión autora del 15-nov-2026, 21:49 UTC. Lo trato como un encargo de revisión, no como una conclusión que confirmar. Actúo porque el encargo general del frente pide repetir la revisión independiente sobre lo corregido, y porque el trabajo queda dentro de mis límites: lectura del material del autor y escritura solo en esta rama.

**Configuración.** Los valores que expone el entorno al empezar y al terminar se dan en la respuesta de la sesión. Aquí no se escriben identificadores de modelo.

**Límites de la independencia:**
- Soy el mismo revisor de las pasadas n.º 1 y n.º 3. Conozco mis conclusiones anteriores.
- La sesión autora creó esta sesión y le encarga esta pasada. El alcance lo fija ella.
- El contexto de la sesión se resumió durante la pasada n.º 3. Trabajo con notas propias y solo cito lo que he vuelto a ejecutar o a leer en esta pasada.
- Leo los PDF con `pdftotext -layout`, como el autor. Un error de extracción común no se detectaría.
- **Presupuesto de contexto escaso.** He leído las diferencias entre f30c66c y el commit congelado, no los documentos enteros. Lo que dejé sin hacer está en §9.

---

## 2. Reproducción (alcance 5)

Sobre un worktree del commit congelado y la base 4.14 verificada. Libro `d2593777…92385`.

| Cifra declarada | Resultado |
|---|---|
| Manifiesto | 154 de 154 |
| Verificador: 736 filas, 722 OK, 14 PENDIENTE, 0 FALLO | Reproducido. Código 2. JSON idéntico |
| `test_verificar_cifras`: 63/63 | Reproducido. Registro idéntico |
| Contraste: 275 comprobaciones (136 del libro, 110 de fuente con 109 residuos, 29 algebraicas), 0 fallidas, 402 entradas | Reproducido. Código 0. JSON y tabla idénticos |
| Cobertura: 211 / 151 / 9 / 31 | Reproducido |
| `test_contraste_residuos`: 14/14 | Reproducido. Registro idéntico |
| Mutación: 362 por identidad, 9 solo libro, 23 sin detectar, 8 leídas sin efecto, 112 no usadas | Reproducido. Salida idéntica (el script agrupa las dos últimas en 120) |
| Ninguna de las 23 cambia la referencia; 5 de las 9 de la Historia sí | Reproducido. Las cinco: impuesto y adquisiciones de 2021 y 2022 y ventas de 2020 |
| Referencias de E9 sin cambios | C53 de A1, 2,445331695332; de A2, 1,612524303305. f y flujo sin crecimiento, iguales |

`prueba_caja_no_nula.py` y su salida no cambian desde 1864c4e (`git diff` vacío). No he repetido la prueba con LibreOffice; vale la reproducción de la pasada n.º 3.

Fuera de la carpeta del frente E no cambia nada entre f30c66c y el commit congelado. Mis archivos de la revisión n.º 3 están copiados sin cambios en la rama del autor.

---

## 3. Estado de N1–N10 (alcance 1)

Pruebas: mis scripts de la revisión n.º 3, sin cambios, sobre el commit congelado (salidas idénticas a `resultados/revisor3_*_sobre_C7.txt` del autor), y `scripts_revisor_4/contraejemplos_4.py`.

| Objeción | Estado | Prueba y motivo |
|---|---|---|
| N1 · el verificador daba OK a cifras incorrectas | **Corregida en parte** | Corregido: el ejercicio en tablas con tercera columna (F1 FALLO; F2 y F3, los valores correctos, OK); el modo declarado (A1, A2, A4 y H1, FALLO); el concepto de la columna (D1 y D2, FALLO en la dimensión nueva); los casos concretos de unidad y perímetro (B1, B2 y C1, FALLO); la otra línea de la misma tabla la detecta el contraste (H5: R25 y R16 de 2022); el informe dice qué significa OK. **Queda:** las reglas de unidad y perímetro son listas de rótulos, y filas reales fuera de la lista pasan como OK (P1 y P2) |
| N2 · entradas sin segunda línea | **Corregida** | 109 residuos. `cobertura_entradas` clasifica las 402 entradas, con una aserción de completitud. La mutación coincide con la clasificación. Quedan declaradas 31 sin segunda línea y 5 que cambian la referencia con la Historia como única segunda línea. Mis casos C1 y C2 confirman ese residuo: una línea equivocada en dos de las 31 pasa las dos líneas de defensa y cambia el ratio fiscal de 2025 (21,0 % → −21,0 %) y las partidas puntuales (+27,9 → +9,4), sin tocar la referencia |
| N3 · verificación de otro CSV | **Corregida** | El contraste se niega: «la verificación no corresponde a este CSV» (H2) |
| N4 · dos combinaciones de E2 sin fórmula | **Corregida** | Retiradas de las admisibles; disparan V-F1h. La vía posible queda descrita sin adoptarla |
| N5 · A3 sin ancla ni flujos | **Corregida** | `A3_estimado_sintetico` da C53 y flujos. Los tres C53 coinciden con los que calculé en la revisión n.º 3 |
| N6 · residuos: afirmaciones más fuertes que la prueba | **Corregida**, con una imprecisión nueva de forma | §0.2 y §5.4 dicen el límite de 0,15. R16 de 2023 está en la tabla de §2 con su causa. La imprecisión nueva es P4 |
| N7 · «359 entradas» | **Corregida** | §1: 402 leídas; 394 con efecto y 8 sin efecto |
| N8 · varios | **Corregida** | (a) OK definido; (b) §0.6 remite al esquema de A1′; (c) 13 positivos, 1 PENDIENTE y 49 contraejemplos; (d) desvíos del año 11 en T2 y T3; (e) corregida en C6; (f) regla de los saldos y R26–R28 |
| N9 · columna de la matriz contada desde la derecha | **Corregida** | La columna se asigna por posición horizontal. Con una celda vacía: el margen de Francia declarado «Europa central», FALLO, y declarado «Francia», OK; lo mismo con el margen de EBIT de Europa del Sur (casos E1–E4) |
| N10 · las sondas presentadas como cobertura | **Corregida** | §1, T12 y las respuestas dicen qué miden. Los contraejemplos de la adenda están en el test y en T14. La frase inexacta está corregida |

---

## 4. Cambios de C7 que no responden a una objeción (alcance 2)

- **(a) R5 de 2021–22.** Correcta. El circulante del APM es 10,1 en 2021 (URD 2022 p.250) y (52,6) en 2022 (URD 2023 p.268) [P]. Frente a las líneas del EFE deja residuos de +0,1 y 0,0, con cota 0,40 [D]. Es un contraste entre páginas.
- **(b) `cobertura_entradas`.** Se construye al final y `contraste_f1.py` exige que su conjunto sea igual al de entradas usadas. La mutación no encuentra ninguna entrada con efecto fuera de la tabla.
- **(c) `scripts/cobertura_por_mutacion.py`.** Es mi script con el cambio que declara: la verificación falsa se liga a cada CSV mutado (huella, literal y valor). Añade además una comparación con `cobertura_entradas`, que su cabecera describe. La medida es la misma que la mía.
- **(d) Casos nuevos de `test_contraste_residuos.py`.** Reproducidos, 14/14. Mi repetición independiente de H3a–H3c y H4 da lo mismo (casos D1–D4). El recuento «42» del caso de los pagos necesita un matiz (P4).

---

## 5. Lo que el autor dice de mis scripts sobre C7 (alcance 3)

| Afirmación del autor | Veredicto |
|---|---|
| (a) H3a–H3c y H4 de `prueba_mutantes_3b.py` leen un `k.json` anterior | **Cierta.** Es un defecto de mi script: todos los casos comparten una carpeta temporal y, si el contraste se niega a calcular, se lee la salida del caso anterior (H5). En 1864c4e y en f30c66c el contraste calculaba siempre, así que los resultados que publiqué en la revisión n.º 3 son correctos. `contraejemplos_4.py` usa una carpeta por caso |
| (b) Mi `cobertura_por_mutacion.py` aborta en 514 de 514 | **Cierta.** Entrega la verificación del CSV original y la barrera de N3 la rechaza |
| (c) Los positivos de `sondas_revisor.py` (fila «Other» y margen de Francia con su perímetro correcto) fallan en ejercicio | **Cierta.** Su perímetro queda OK; falla el modo, porque mis identificadores nuevos no están en la lista cerrada |
| (d) Los dos casos de la matriz del URD 2021 quedan PENDIENTE en perímetro | **Cierta.** El total del grupo de esa matriz queda OK en perímetro y PENDIENTE en columna |

**¿Alguna defensa de C7 deja sin medir algo que mis pruebas medían?** No, con dos observaciones:
- La barrera de N3 impide saltarse el verificador con una verificación antigua. La medida de la segunda línea se recupera ligando la verificación falsa al CSV mutado, como hacen el autor y mis casos D. Eso muestra también qué es la barrera: un control de integridad contra el descuido, no contra una verificación fabricada.
- La lista cerrada de modos se decide por el **prefijo del identificador** (`modo_admitido`), y el identificador es también un campo declarado. He comprobado que no abre un atajo: una fila con un prefijo de otro modo necesita además una regla de columna para su concepto y, si no la tiene, queda PENDIENTE. La consecuencia es de diseño: una fila nueva de una tabla que no sea de dos ejercicios no puede quedar OK sin tocar las listas del verificador.

---

## 6. Cobertura de la unidad y del perímetro (alcance 4)

**Pregunta.** Los mutantes de un solo campo ya se rechazan. ¿Están acreditados esos campos por otra vía independiente y trazable, o queda cobertura pendiente?

**Respuesta.** Queda cobertura pendiente, y el informe ya lo dice en términos generales. Concreto aquí cuánta y dónde.

| Vía | ¿Independiente de lo declarado? | ¿Trazable? | Qué acredita | Qué no |
|---|---|---|---|---|
| Reglas de unidad del verificador | Sí: lee el PDF | Sí, fila a fila | Que el literal lleva «%» o no; que la declaración más próxima dice millones; que el rótulo no está en una lista de recuentos, importes por acción, márgenes, días o años | Que una línea sin esas señales esté en millones (P1) |
| Reglas de perímetro del verificador | Sí | Sí | Que la página es de estados consolidados; que la fila no lleva rótulo de segmento ni de país, ni es sublínea de un segmento, ni columna de segmento en una matriz | Que la tabla sea del grupo (P2) |
| Identidad entre páginas | Sí: otra presentación de la cifra | Sí: `residuos_con_cota` | De forma indirecta, la unidad y el perímetro: una cifra de otra unidad o de otro perímetro rompería la identidad | — |
| Identidad de la misma página | Sí | Sí | La coherencia interna de la tabla | La unidad y el perímetro de la tabla entera (P3) |
| Historia del libro | A medias: es otra transcripción de las mismas publicaciones | Sí | El número, salvo error común a las dos lecturas | Lo mismo |

**Cuánta cobertura** [D], sobre `cobertura_entradas` del commit congelado:
- 211 entradas con identidad entre páginas: unidad y perímetro acreditados de forma indirecta;
- 151 con identidad solo de su página. De ellas, 126 están en páginas donde otra entrada sí tiene contraste entre páginas, y 25 en páginas sin ninguno;
- 9 solo con la Historia del libro;
- 31 sin segunda línea.

De las 47 páginas de fuente con entradas usadas, **14 no tienen ninguna entrada contrastada entre páginas.** En ellas hay 42 entradas (25, 15 y 2 de las clases anteriores): las cuatro tablas de crecimiento, las dos de deuda neta, las tres de impuestos diferidos y otras cinco páginas sueltas. En esas tablas la unidad y el perímetro descansan en las reglas del verificador y en la lectura. En mi lectura de las pasadas n.º 1 y n.º 3 son del grupo y están en la unidad declarada [I]; no las he vuelto a leer una a una en esta pasada.

**«OK = sin incoherencia detectada, no acreditada».** Está dicho en el informe (§0.1 y §1), en T12, en el README y en las respuestas. Falta en dos lugares, por redacción (P5).

---

## 7. Objeciones nuevas

Prueba de todas: `scripts_revisor_4/contraejemplos_4.py`, salida en `resultados_revisor_4/contraejemplos_4.txt`. Las filas existen en el PDF [P].

### P1 · menor · `verificar_cifras.py`, unidad · la lista de rótulos no monetarios deja pasar otros recuentos de la misma tabla

- **Prueba.** En la tabla del beneficio por acción (URD 2025 p.395), bajo «(In millions of euros)»:
  - «Effect of conversion of convertible bonds 23,355,764», declarado «mm EUR»: **OK en todas las dimensiones**;
  - «Effect of contingently issuable shares 1,767,869»: **OK**;
  - control: «Weighted average number of shares 233,954,020»: FALLO en unidad.
- **Causa** [D]. La regla rechaza los rótulos de una lista («number of», «per share», «as a % of»…). Las dos primeras líneas son acciones, pero su rótulo no dice «number of».
- **Alcance.** Ninguna fila real está en ese caso. El límite está declarado en §1 del informe. Importa para T14, que traslada al frente técnico una lista de casos, no un criterio.
- **Corrección propuesta.** Añadir un criterio que no dependa del rótulo: en una tabla de millones con un decimal, dejar PENDIENTE un número sin decimales de seis cifras o más, o cualquier línea cuyo formato no sea el de la tabla. Incluir los dos casos en el test y en T14.

### P2 · menor · `verificar_cifras.py`, perímetro · un bloque por país con rótulos genéricos pasa como grupo

- **Prueba.** La nota de pensiones «Information by region» (URD 2025 p.356) tiene un bloque por país, con el país en un título y rótulos genéricos en las filas. «TOTAL VALUE OF DEFINED BENEFIT PLAN OBLIGATIONS (1) 45.2» es el total de **Francia**; el del grupo es 414,4 (p.355). Declarado del grupo: **OK en todas las dimensiones**. Controles: la fila «United Kingdom» de la tabla por países de esa página y las ventas de Alemania, FALLO en perímetro.
- **Causa** [D]. El perímetro se reconoce por la página y por el rótulo de la fila. Un título de país o de segmento por encima de la tabla no cuenta.
- **Alcance.** Ninguna fila real está en ese caso. Es el límite que §1 declara («una cifra de otro perímetro sin ninguna de esas señales no se detectaría»), ahora con un ejemplo real.
- **Corrección propuesta.** Dejar PENDIENTE el perímetro cuando entre el título de la sección y la tabla haya un título que sea un país o un segmento, o cuando el mismo rótulo aparezca en la página anterior con otro valor. Incluir el caso en el test y en T14.

### P3 · menor · informe §0.2 y §1; `cobertura_entradas` · la identidad de la misma página no acredita la unidad ni el perímetro

- **Qué dice el material.** Presenta cuatro clases de cobertura. La segunda, «solo identidad de la misma página» (151 entradas), figura como segunda línea sin matiz.
- **Por qué importa** [D]. Una suma de componentes dentro de una tabla cuadra igual si toda la tabla es de otro perímetro o de otra unidad: el bloque de Francia de P2 cuadra internamente. Para la unidad y el perímetro, la segunda línea que cuenta es la de entre páginas.
- **Prueba.** §6: 14 de las 47 páginas no tienen ninguna entrada contrastada entre páginas; 25 de las 151 están en ellas.
- **Corrección propuesta.** Decir en §0.2 y en §1 qué acredita cada clase. Añadir a `cobertura_entradas` si la página de cada entrada tiene alguna identidad entre páginas, y listar las 14 que no.

### P4 · forma · respuestas (N6) y `test_contraste_residuos.py` · el caso de los pagos en 178,0

- Las respuestas dicen que a ese caso «no lo detecta ninguna identidad» y que «hace fallar 42 comprobaciones contra el libro».
- Lo que ocurre [D]: R13 no lo detecta, pero sí una comprobación de fuente, la doble vía del FCF base. Las 42 del test son esa y 41 del libro. Con la copia recalculada (`--caja-no-nula`) son 1 y 50 (caso D3).
- Corrección: «ningún residuo lo detecta; lo detectan la doble vía del FCF base y 41 comprobaciones del libro».

### P5 · forma · informe §1 y respuestas (N1 y N10) · dos frases absolutas

- §1: «Las líneas de recuentos, importes por acción, márgenes, años o euros no pueden ser "mm EUR"». Vale para las líneas cuyo rótulo está en la lista (P1).
- Respuestas, N10: «los que eran OK quedan ahora en FALLO». Vale para esos casos, no para su clase (P1 y P2).
- El párrafo de límites de §1 ya lo matiza. Basta alinear estas dos frases con él.

---

## 8. Coherencia entre documentos (alcance 6)

He cotejado las líneas cambiadas del informe (§0, §1, §2, §5.4 y §12), de la especificación (E2, E9, T2, T3, T12 y T14) y del estado, y la segunda parte de las respuestas.

- **Recuentos.** Coinciden entre sí y con las salidas: 736, 722, 14 y 0; 63 = 13 + 1 + 49; 275 = 136 + 110 + 29; 109 residuos; 402; 211, 151, 9 y 31; 14 casos; 514 = 362 + 9 + 23 + 8 + 112.
- **PENDIENTE usada como contraparte.** `LS_AMORT_ROU_2021` (unidad no impresa) es la contraparte de R16 de 2021 y el contraste termina con código 0. Está declarado en §0.1, en §1, en T12 y en las respuestas. Observación: esa identidad da segunda línea a la amortización ROU de 2021 con una cifra cuya unidad no está acreditada; la cubre también R25 de 2021, de la misma página.
- **Estado.** `ESTADO.md` describe bien las pasadas y deja la n.º 4 pendiente.
- **Afirmaciones más fuertes que su prueba:** P3, P4 y P5. No encuentro otras en lo leído.

---

## 9. Conclusiones materiales y lo no comprobado

**Conclusiones materiales.** Ninguna cambia: la conciliación y el FCF base, C48 = 108, el doble cómputo del arrendamiento bajo la premisa (iv), los intangibles adquiridos pendientes de política, la reinversión necesaria no publicada como importe y `pendiente_de_datos`. Las decisiones económicas siguen pendientes de la persona responsable.

**No comprobado en esta pasada:**
- Los documentos enteros: solo las diferencias entre f30c66c y el commit congelado.
- Las 20 filas nuevas del CSV una a una en los PDF, salvo las dos del circulante del APM. Las cubre el verificador reproducido y, en su mayoría, una identidad nueva.
- Los flujos de los años 1–11 de A3 sintético: no los he recalculado. Sí coinciden f, el flujo sin crecimiento y C53.
- La prueba de caja no nula con LibreOffice: no cambia desde 1864c4e y no la he repetido.
- Las reglas V-F1a a V-F1h y T8 y T14: especificadas, no implementadas.
- El código nuevo del verificador línea a línea: he leído las líneas añadidas y lo he probado con mutantes. No he buscado falsos positivos más allá de comprobar que los datos reales no cambian de estado.
- El árbol del hito 4.15 y la rama del frente técnico.

---

## 10. Reproducción de esta revisión

```bash
AUTOR=<worktree de 9744177>/docs/validacion_economica_paralela/frente_E_F1_elis
RAIZ=<ruta>/munger_v2_r1
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
python3 -I revision/scripts_revisor_4/contraejemplos_4.py --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
python3 -I revision/scripts_revisor_4/paginas_sin_ancla.py --contraste "$AUTOR/resultados/contraste_f1.json"
# scripts de la revisión n.º 3, sin cambios, sobre el mismo commit
python3 -I revision/scripts_revisor_3/prueba_mutantes_3.py  --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
python3 -I revision/scripts_revisor_3/prueba_mutantes_3b.py --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
python3 -I revision/scripts_revisor_3/sondas_revisor.py --raiz "$RAIZ" --libro "$LIBRO" --version C7="$AUTOR"
```

Salidas en `revision/resultados_revisor_4/`:

| Archivo | Contenido |
|---|---|
| `contraejemplos_4.txt` | Casos A1–A3 (unidad), B1–B3 (perímetro), C1–C2 (línea equivocada sin segunda línea), D1–D4 (diferencia fijada) y E1–E4 (matriz con celda vacía) |
| `paginas_sin_ancla.txt` | Páginas de fuente sin ninguna entrada contrastada entre páginas |

Las salidas de mis scripts de la revisión n.º 3 sobre este commit son idénticas a las que el autor guarda en `resultados/revisor3_*_sobre_C7.txt`; no las duplico.
