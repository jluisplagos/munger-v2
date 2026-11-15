# Revisión independiente n.º 3 · frente E · F1 · Elis · lo afectado desde 96a69ca

Fecha: 15-nov-2026. Material revisado: commit congelado `1864c4ec6239c1499d08a47c24a55b48d3585a45` de la rama `auditoria/economica-f1-frente-e`.
Esta revisión se publica en la rama `auditoria/economica-f1-frente-e-revision`, sobre el commit 47551a2 de la revisión n.º 1.

No hay revisión n.º 2: el encargo sobre eb77dea se interrumpió a los pocos minutos y no produjo nada. Nada de aquel intento se publica aquí.

**Adenda (§11).** El autor añadió después de la congelación el commit `f30c66c8651dba134b4e66fff9a08c2b50359b6c` y pidió revisarlo junto con las sondas externas de un solo campo. Está en §11, publicada en un segundo commit de esta rama.

Marcas: **[P]** dato publicado (leído en el PDF) · **[D]** derivación aritmética · **[I]** interpretación · **[H]** hipótesis · **[DH]** decisión humana registrada.

Este documento no contiene valoraciones, valores por acción, recomendaciones de inversión ni declaraciones de aptitud. No adopta ninguna política pendiente. No modifica el material del autor, el producto ni los libros.

---

## 0. Resultado en breve

1. **Reproducción.** Todas las salidas del autor se reproducen sobre una base 4.14 verificada (6.798/6.798). Son idénticas byte a byte a `resultados/`, salvo la prueba de LibreOffice, cuyos resultados numéricos son idénticos.
2. **Objeciones de la revisión n.º 1.** 16 quedan **resueltas** (O1, O2 y O4–O17). **O3 queda parcialmente resuelta.**
3. **O3, lo corregido.** Los mutantes de la revisión n.º 1 ya se rechazan. Los residuos se afirman con una cota de redondeo fundada. Una fuente sin huella da un diagnóstico controlado. Las identidades algebraicas están separadas de las pruebas de datos.
4. **O3, lo que queda (objeción nueva N1, material en el mismo sentido que O3, con alcance reducido).** El verificador sigue dando por buenas cifras incorrectas en configuraciones reproducibles:
   - una cifra de 2024 declarada de 2025, **en el modo por defecto**, si la tabla tiene una tercera columna;
   - una columna de otro ejercicio, si la fila declara otro modo de control;
   - un número de acciones o un importe por acción como millones de euros;
   - un margen de un segmento como dato del grupo;
   - otra columna u otra línea de la misma tabla.

   Dos de estos casos pasan también por el contraste y cambian cifras que el informe o la especificación citan: las partidas puntuales (+27,9 → +8,6) y el C53 de referencia de T2 y T3 (2,445 → 2,688).
5. **Lo que N1 no afecta.** No he encontrado ningún error en los datos reales. Las 36 filas añadidas desde 96a69ca están comprobadas en los PDF. f, el flujo sin crecimiento y los flujos de referencia quedan protegidos por los residuos y por el libro frente a errores mayores que la cota de redondeo.
6. **Recálculos.** Coinciden con el autor a 10⁻⁹ o mejor: f, flujo sin crecimiento y C53 de A0, A1, A2 y B; los flujos de los años 1–10 y del año 11 de A1 y A2; A3 con valores sintéticos, incluido el punto medio; los ratios fiscales; O4, O9 y O10.
7. **Otras objeciones nuevas.** Cuatro menores (N2–N5) y tres de forma (N6–N8). Están en §5.
8. **Ninguna conclusión material cambia.** La conclusión de nivel sigue `pendiente_de_datos`. Se conservan C48 = 108 y E1/D3/E2/E6.
9. **Adenda (§11).** Las dos sondas externas de un solo campo pasaban en eb77dea y se rechazan en 1864c4e y en f30c66c; las cifras del autor (0 de 671; 677 y 673 de 677; 677 y 677) son exactas. Esas sondas prueban que una etiqueta cambiada se detecta, no que la etiqueta correcta esté acreditada: cuatro contraejemplos reales más quedan en OK (ventas de Alemania o del segmento «Other» como grupo; recuentos de acciones como millones de euros). f30c66c no cambia ninguno de los resultados de N1–N3, añade un fallo propio en matrices con una celda vacía (N9, menor) y presenta las sondas como cobertura de la unidad y del perímetro (N10, menor).

---

## 1. Encargo, configuración y límites de la independencia

**Encargo.** Mensaje de la sesión del autor del 15-nov-2026, 20:03 UTC: revisar lo afectado desde 96a69ca sobre el commit congelado. Lo trato como un encargo de revisión, no como una conclusión que confirmar. Actúo porque el encargo general del frente pide repetir la revisión independiente sobre lo afectado por correcciones materiales, y porque el trabajo queda dentro de mis límites: lectura del material del autor y escritura solo en esta rama.

**Configuración.** Los valores que expone el entorno al empezar y al terminar se dan en la respuesta de la sesión. Aquí no se escriben identificadores de modelo. Al empezar esta pasada, los tres campos de modelo de los metadatos coincidían entre sí y el esfuerzo era el máximo.

**Límites de la independencia, que el lector debe pesar:**
- Esta sesión fue creada y encargada por la sesión del autor. El alcance lo fija el autor.
- Soy el mismo revisor de la pasada n.º 1. No es un contexto nuevo: conozco mis conclusiones anteriores.
- El contexto de la sesión se resumió automáticamente durante la pasada. Trabajé con notas propias y volví a ejecutar cada comprobación que cito; no cito de memoria ninguna cifra.
- Leo los PDF con `pdftotext -layout`, igual que el autor. Un error de extracción común a los dos no se detectaría. No he inspeccionado las páginas como imagen.

**Método.**
1. Reproduje las salidas del autor.
2. Lancé un primer lote de mutantes y la cobertura por mutación, leyendo solo el código de los scripts.
3. Leí enteros el informe, la especificación y las respuestas del commit congelado, y cotejé sus cifras con las salidas.
4. Hice el recálculo independiente y el resto de mutantes.

Durante el encargo interrumpido sobre eb77dea había leído ya las diferencias del informe y una versión anterior de las respuestas. Las conclusiones de este documento se apoyan en comprobaciones hechas sobre el commit congelado.

---

## 2. Reproducción (alcance d)

| Comprobación | Resultado |
|---|---|
| Commit congelado | `1864c4e` era la cabeza de la rama al empezar esta pasada, poco después de las 20:03 UTC. Cuatro commits del autor desde 96a69ca: 6fb9294, eb77dea, d2e585e y 1864c4e. Ninguno toca nada fuera de la carpeta del frente E. A las 20:10 UTC el autor añadió f30c66c, que se revisa en §11 |
| Mis archivos de la revisión n.º 1 | Los 14 son idénticos a los del commit 47551a2 (`git diff` vacío). Coincide con `revision/PROCEDENCIA_REVISOR.md` |
| Manifiesto del autor | `sha256sum -c MANIFIESTO_SHA256.txt`: 125 de 125 |
| Base 4.14 | ZIP original, SHA-256 `bb51942c…b97b93e`; `tools/base_414.py verify`: 6.798/6.798. Libro de Elis `d2593777…92385` |
| `verificar_cifras.py` | Código 2. 716 filas: 702 OK, 14 PENDIENTE, 0 FALLO. JSON, registro y 65 páginas exportadas idénticos |
| `test_verificar_cifras.py` | 39/39. Registro idéntico |
| `prueba_caja_no_nula.py` | LibreOffice 24.2.7.2, un solo proceso y nada más a la vez. Resultados numéricos idénticos. El libro original no cambia |
| `contraste_f1.py` | Código 0. 236 comprobaciones (72 de fuente, 136 del libro, 28 algebraicas), 0 fallidas. JSON, tabla y registro idénticos |
| `test_contraste_residuos.py` | 7/7. Registro idéntico |
| `tabla_conciliacion.py` y `especificacion_cifras.py` | Tabla idéntica. El CSV regenerado desde los PDF es idéntico a `datos/cifras_fuente.csv` |
| Mutantes de la revisión n.º 1 sobre el commit congelado | Mi script, sin cambios: M1 FALLO en ejercicio; M4 FALLO en ejercicio, unidad, edición y perímetro; M2 y M3 FALLO con motivo. Salida idéntica a `resultados/mutantes_revisor_sobre_C4.txt` del autor (`resultados_revisor_3/prueba_mutantes_rev1_sobre_commit_congelado.txt`) |

Versiones: pdftotext 24.02.0, Python 3.13.18, openpyxl 3.1.5.

**Filas nuevas del CSV.** Desde 96a69ca hay 36 filas nuevas: 27 hasta eb77dea y 9 en d2e585e [P].
- Las 27 primeras son 26 citas de texto y las ventas de lino plano (2.217,4; URD 2025 p.347). Las citas proceden casi todas de las páginas que di en la revisión n.º 1; su presencia literal en la página la comprueba el verificador, que he reproducido. La cifra de lino plano la he leído en el PDF.
- Las 9 últimas las he leído en los PDF en esta pasada:
  - `IS_PPA_FR_2024` y `IS_PPA_FR_2023`: (84,9) y (85,7), DEU 2024 p.270;
  - `INT_RC_COMB_FR_2024`: 18,0, DEU 2024 p.310;
  - `VENTAS_SEG_2025`, `VENTAS_SEG_2024` y `VENTAS_SEG_FR_2023`: 4.796,8 (URD 2025 p.347), 4.573,7 (p.345) y 4.309,4 (DEU 2024 p.290);
  - tres textos del URD 2025 p.366: arrendamientos de bajo valor 2,0, a corto plazo 5,9 y pagos variables 0,9.

---

## 3. Estado de las objeciones de la revisión n.º 1

| Objeción | Estado | Motivo |
|---|---|---|
| O1 · dos tercios del lino plano | **Resuelta** | §6.1 cita la frase con sus páginas y sus cuatro límites. §0.8 y M1 (a–d) están reescritos. El alcance de la búsqueda está declarado. La proporción no se usa como porcentaje del capex total ni como reposición suficiente. Detalle en §3.1 |
| O2 · precio y volumen de 2024–25 | **Resuelta** | §3, §6.2 y M5 separan la existencia publicada [P] de la cuantificación ausente. E4 declara nominal la variante orgánica de C53 |
| O3 · los scripts podían pasar con datos incorrectos | **Parcialmente resuelta** | Lo que señalé está corregido. Quedan huecos nuevos del mismo tipo, con prueba: N1, N2 y N3. Detalle en §3.2 |
| O4 · alcance según el ancla de S2C | **Resuelta** | §5.3 (alcance), nota ¹ de §5.2, §0.6 y E4. Recalculado: 81,3 y 129,6; 517,6 y 496,6; 11,3 % |
| O5 · premisa de arrendamientos | **Resuelta** | Premisa (iv) numerada y marcada [I]; conclusión «[D, condicionada a la premisa iv]»; cita de la nota 6.5. La evidencia contraria se buscó; yo tampoco la encuentro (§6.3). Matiz de forma en §0.6 (N8b) |
| O6 · evidencia contra la D&A propia como caso central | **Resuelta** | §6.2 cita el plan climático, las inversiones futuras adicionales y la contención del capex. §9 y §10.6 dejan el plan climático pendiente de definición |
| O7 · fiscalidad y agotamiento | **Resuelta** | «Mayoritariamente no deducible [I]»; altas de 2025 provisionales; matiz del agotamiento. Ratios recalculados: 18,3 %, 24,2 % y 21,0 %. Sus entradas no tienen segunda línea de comprobación (N2) |
| O8 · crecimiento orgánico y PPA | **Resuelta** | §6.3 lo enlaza como evidencia parcial, cita los contratos de cuatro años y la bajada de la tasa de pérdidas, y explica la compensación numérica |
| O9 · partidas puntuales | **Resuelta** | +27,9 recalculado (+13,7 − 4,0 + 18,3). Consta en §0.8, M1, §9, E8.4 y E9. Una de sus entradas no tiene segunda línea (N2, mutante H1) |
| O10 · tendencia de los arrendamientos | **Resuelta** | Tabla de §5.5 y nota ³ de §9. Recalculado: 161,1 frente a 177,9; 10,1 sin devolver |
| O11 · deuda constante | **Resuelta** | §8 recoge los cuatro límites. Recalculado: 41 %; 87,2 |
| O12 · perímetro del margen; V-F1a | **Resuelta** | Los cuatro puntos pedidos están en E2, E4 y E5. La matriz de coherencia añadida tiene dos imprecisiones nuevas (N4) |
| O13 · referencias de flujos y prueba de A3 | **Resuelta** | T2 y T3 fijan los años 1–10 y el año 11 de A1 y A2. T3b prueba A3 con valores sintéticos. Todo recalculado. T3b no fija el ancla ni los flujos de A3 (N5) |
| O14 · «33 flujos» | **Resuelta** | §4.3: 30 flujos anuales más 3 del año 11 |
| O15 · identidad del exceso de caja | **Resuelta** | (BL − M)·r, comprobada con C76 = 0, 250 y −80 en una copia recalculada. Reproducido por mí |
| O16 · README, nombre del caso, `KeyError` | **Resuelta** | README por clases; caso renombrado; fallo con motivo «no declara SHA-256» |
| O17 · nota de §5.2 | **Resuelta** | Nota ² con el exceso exacto, 139,4 |

### 3.1 O1 y O2: evidencia contraria buscada

**O1.**
- Las cinco citas están en las páginas dadas [P]: URD 2025 p.137, URD 2023 p.239, URD 2022 p.221, URD 2021 p.189 y DEU 2024 p.135. La frase figura también en el URD 2020 (p.133) y no en el de 2019. «Texto fijo desde al menos el URD 2020» es correcto.
- El autor declara haber buscado también en los documentos de 2026 de la carpeta `fuentes_2026/`. He extraído esos PDF y he comprobado sus dos citas [P]: «new client wins outpacing churn» (presentación del primer semestre de 2026, p.6) y «lower churn» (p.12). He buscado en ellos reparto entre mantenimiento y crecimiento: no hay importes ni tasas.
- **La proporción no se usa indebidamente.** No entra en ningún cálculo de los scripts. Los 396 (dos tercios de las compras de lino de 2025) aparecen solo como ilustración del límite. T3b la excluye de forma expresa. M1 mantiene abiertos el importe del lino plano, la proporción del resto del capex, la reposición de clientes perdidos y la base de la estimación.

**O2.** Las citas de precio y de volumen son las que di en la revisión n.º 1, en las mismas páginas. El texto ya no presenta el efecto volumen como premisa sin apoyo, y tampoco presenta el reparto como cuantificado: M5 pide la cuantificación, no la existencia. En 2023 solo se publica el efecto precio (≈ +9 %); el volumen de ese año es una derivación [D], y §6.3 lo dice bien («efecto volumen positivo publicado en 2024 y 2025»).

### 3.2 O3: qué está corregido y qué queda

**Corregido y comprobado por mí:**
- `verificar_cifras.py` comprueba cinco dimensiones y deja cada una en OK, PENDIENTE o FALLO. Los 14 PENDIENTE son correctos: la tabla de arrendamientos del URD 2022 p.302 no imprime la unidad [P].
- M1 y M4 de la revisión n.º 1 se rechazan en su dimensión. M2 y M3 fallan con motivo.
- Los 71 residuos se afirman. La cota de cada uno es la suma, para cada cifra impresa, de |coeficiente| × media unidad de su última cifra. Es una cota fundada en la precisión y en el número de cifras agregadas, no una tolerancia global.
- La única excepción es R13 de 2025, fijada en +0,4 ± 0,15.
- Las 28 identidades algebraicas están marcadas como tales y no cuentan como prueba de datos.
- La regla de edición de las tablas de un solo ejercicio es correcta: el movimiento de impuestos diferidos solo lo presenta la publicación del propio ejercicio [P: URD 2025 p.393; DEU 2024 p.338; URD 2023 p.346].

**Lo que queda** está en N1 (primera línea), N2 (segunda línea) y N3 (enlace entre las dos).

---

## 4. Estado de los requisitos del contraste externo

Numeración mía sobre los documentos `REVISION.md` y `PROMPT_PARA_AUTOR.md` del contraste externo hecho sobre 6fb9294 (rama `auditoria/economica-f1`, commit 5ce263a; la ruta de la carpeta está en `revision/RESPUESTAS_AUTOR_1.md` del autor).

| Requisito | Estado | Motivo |
|---|---|---|
| RE1 · O1 con páginas y límites; no convertir los dos tercios en porcentaje de todo el capex ni en reposición suficiente; alcance de la búsqueda y datos pendientes | **Cumplido** | §3.1 |
| RE2 · O2: registrar la corrección de 6fb9294; existencia publicada frente a cuantificación ausente | **Cumplido** | §3.1 |
| RE3 · comprobar ejercicio, unidad, perímetro y edición, o dejarlos explícitamente pendientes; las identidades algebraicas no sustituyen el contraste de entradas | **Parcialmente cumplido** | Las cinco dimensiones existen y las algebraicas están separadas. Pero hay configuraciones en que la dimensión queda en OK sin estar acreditada, en lugar de PENDIENTE (N1) |
| RE4 · residuos con tolerancias fundadas en precisión, unidad y agregación, no globales; las excepciones −0,2 y +0,4 no absorben errores nuevos | **Cumplido, con dos matices de forma** | Cota por identidad. El −0,2 queda dentro de su cota (0,35). El +0,4 está fijado. Matices: un error de hasta 0,15 en sus cifras sí pasa, y R16 de 2023 pasa por igualdad (N6) |
| RE5 · fuente sin `sha256`: diagnóstico controlado | **Cumplido** | Caso del test y mi mutante M2 |
| RE6 · mutantes conjuntos de posición y literal, año, unidad, perímetro y edición; conservar los positivos y las pruebas existentes | **Parcialmente cumplido** | Los mutantes del test existen y las pruebas anteriores se conservan. Pero otros mutantes conjuntos de las mismas cinco clases no se detectan (N1: F1, A1, A2, A4, H1, B1, B2, C1, D1, D2, H5) |
| RE7 · resto de objeciones: S2C, premisas de arrendamientos, evidencia contraria, partidas puntuales, fiscalidad y PPA, perímetro del margen y su coherencia con la reinversión y S2C | **Cumplido** | §3. La matriz de coherencia tiene dos imprecisiones (N4) |
| RE8 · referencias de los flujos anuales y terminales de A1 y A2; pruebas de A3_estimado | **Cumplido** | Recalculado (§6.1). A3 no tiene referencia de ancla ni de flujos (N5) |
| RE9 · identidad con exceso de caja, probada con caja no nula | **Cumplido** | Reproducido con LibreOffice |
| RE10 · commit congelado; respuesta a O1–O17; C48 = 108 y E1/D3/E2/E6; producto sin tocar; ninguna alternativa elegida; sin aptitud | **Cumplido** | §2, §7 y §8 |

---

## 5. Objeciones nuevas

### N1 · material (resto de O3, alcance reducido) · `verificar_cifras.py`; informe §0.1 y §1; especificación T12 y T14 · el verificador sigue dando OK a cifras incorrectas

**Qué dice el material.** «716 cifras […] verificadas […] en cinco dimensiones […] 702 quedan acreditadas en todas» (§0.1). T14 propone que la verificación de entradas del frente técnico rechace «los mismos contraejemplos» que el test del autor.

**Prueba reproducible.** `scripts_revisor_3/prueba_mutantes_3.py` y `prueba_mutantes_3b.py`; salidas en `resultados_revisor_3/`. Los scripts del autor se ejecutan sin cambios sobre copias mutadas del CSV. «5 dim. OK» significa que la fila mutada queda en OK en las cinco dimensiones.

| Id | Mutación | Verificador | Contraste | Efecto |
|---|---|---|---|---|
| F1 | Tabla con tercera columna «Change» (URD 2025 p.308: «TOTAL 1,700.1 1,609.8 +5.6%»). El total de **2024**, 1.609,8, se declara de **2025** en el modo por defecto | 5 dim. OK | — (fila nueva, no usada) | Falso negativo del ejercicio sin tocar el modo |
| F2, F3 | Los totales **correctos** de esa tabla: 1.700,1 como 2025 y 1.609,8 como 2024 | FALLO en ejercicio | — | Falsos positivos: «la columna es de 2025, no de 2024» |
| A1, A2 | M1 de la revisión n.º 1, declarando el modo «crecimiento» o «max_cabecera» | 5 dim. OK | Código 1: R6 y R16 de 2025 | La segunda línea lo detecta |
| A4 | Cifra de la edición anterior (DEU 2024, 596,4) declarada vigente, con el modo «crecimiento» | 5 dim. OK | Código 0 | Sin efecto numérico: el valor es el mismo. La edición no queda acreditada |
| H1 | `OOIE_PLUSV_2025` toma «(1.5)» de la columna de 2024, con el modo «crecimiento» | 5 dim. OK | Código 0 | Las partidas puntuales pasan de **+27,9 a +8,6** |
| B1, B2 | Número de acciones (234,0) e importe por acción (2,00) del URD 2025 p.313, declarados en millones de euros | 5 dim. OK | — | Falso negativo de la unidad |
| C1 | Margen de EBITDA de Francia, «As a % of revenue 41.9%» (URD 2025 p.308), declarado del grupo | 5 dim. OK | — | Falso negativo del perímetro |
| D1 | `TAXDIF_INT_2025` toma «(0.9)», la columna de combinaciones, en vez de 17,5 | 5 dim. OK | Código 0 | El ratio fiscal de 2025 pasa de 21,0 % a −1,1 % |
| D2 | `CREC_ORG_2025` toma «+1.8%», el crecimiento externo, en vez de +3,8 % | 5 dim. OK | Código 0 | S2C orgánico de A1: 5,52 → 4,92 |
| H5 | `DA_ROU_U23_2022` toma «(30.3)», la línea «Other leased items» de la misma tabla | 5 dim. OK | Código 0 | C53 de referencia de T2: **2,445 → 2,688**; de T3: 1,613 → 1,714 |
| K0, A5, E1 (controles) | M1 en el modo por defecto; edición anterior declarada vigente; tabla de 2024 declarada 2025 en el modo «titulo» | FALLO en su dimensión | — | Se detectan, como debe ser |

**Por qué pasa** [D, leído en el código]:
- **Ejercicio, modo por defecto.** El control es posicional: supone que los dos últimos números de la línea son los dos ejercicios de la cabecera. No alinea la posición del número con la columna del año. Con una tercera columna, la posición −2 es el ejercicio anterior y el verificador la toma por el corriente.
- **Modo declarado.** `control_anio` es un campo de la fila que gobierna el control del ejercicio y el de la edición, y no se valida contra la forma de la tabla. Los modos «crecimiento» y «max_cabecera» solo comprueban el ejercicio más reciente de la cabecera, cualquiera que sea la columna. El truco alcanza solo a filas declaradas del ejercicio más reciente de su tabla.
- **Unidad.** Vale la declaración más próxima por encima de la línea, sea o no de su tabla y se aplique o no a esa línea. Las declaraciones que no son de millones, miles o miles de millones de euros («(In euros)», «(In number of people)») se ignoran y la búsqueda sigue hacia arriba.
- **Perímetro.** Solo conoce los segmentos por el rótulo exacto de la línea o por la matriz de columnas. Una sublínea bajo el rótulo de un segmento pasa como grupo.
- **Columna y línea.** El concepto no es una dimensión. Fuera del modo por defecto, el control del ejercicio no mira la columna (131 filas); solo la matriz por segmentos exige la columna «Total». La etiqueta de la línea es siempre un dato declarado.

**Alcance, para no exagerar:**
- **No he encontrado ningún error en los datos reales.** En la revisión n.º 1 comprobé por otra vía las 680 filas de entonces, y ahora las 36 nuevas. En los datos reales:
  - los 18 «crecimiento» son porcentajes y los 9 «max_cabecera» son las tablas de impuestos diferidos;
  - ninguna de las 546 filas del modo por defecto procede de una tabla con una tercera columna a la derecha. 458 tienen dos números tras el rótulo y 88 tienen tres, y en las 88 el primero es la referencia de la nota (`scripts_revisor_3/comprobacion_tokens.py`).
- **f, el flujo sin crecimiento y los flujos de referencia están protegidos** por la segunda línea (N2 dice hasta dónde).
- La objeción es de suficiencia del criterio de prueba, como O3. La gravedad «material» se refiere a T12 y T14: si la verificación de entradas del producto copiara este diseño, aceptaría F1, y los contraejemplos que T14 traslada al frente técnico son un conjunto incompleto.

**Corrección propuesta.**
1. Alinear el ejercicio con la columna de la cabecera por posición horizontal, o exigir en el modo por defecto que la línea tenga exactamente dos números detrás del rótulo; en otro caso, PENDIENTE.
2. Validar el modo declarado contra la tabla: «crecimiento» solo con literal en porcentaje; «max_cabecera» solo con fechas de apertura y cierre; o una lista cerrada de identificadores por modo, con su prueba.
3. Unidad: exigir que no haya otra cabecera de tabla entre la declaración y la línea, y dejar PENDIENTE las líneas de importes por acción o de recuentos.
4. Perímetro: PENDIENTE para sublíneas situadas bajo un rótulo de segmento.
5. Decir en §0.1 y §1 que OK significa «sin incoherencia detectada por las reglas automáticas», no «acreditada». El concepto de la línea y de la columna lo acreditan una lectura independiente o una identidad.
6. Añadir estos mutantes al test y a T14.

### N2 · menor · `contraste_f1.py`; informe §0.2; especificación E9 y T12 · 54 entradas con efecto no tienen ninguna comprobación de segunda línea

**Qué dice el material.** «71 de las 72 entradas clave de la ventana quedan contrastadas por una identidad entre páginas» (§0.2). Es cierto para las 17 magnitudes que el script llama clave. No dice qué pasa con las demás.

**Prueba reproducible.** `scripts_revisor_3/cobertura_por_mutacion.py`. Altera en +3,0 cada una de las 499 filas de tabla de la edición vigente y ejecuta el contraste del autor con el verificador saltado, como hace su propio test.

| Clase | Entradas |
|---|---|
| Falla alguna identidad de fuente | 226 |
| Solo fallan comprobaciones contra el libro | 40 |
| **Cambia alguna salida y no falla nada** | **54** |
| Ninguna salida cambia | 179 |

Las 54 sin detectar:
- **4 que fijan el C53 de referencia de T2 y T3:** amortización ROU y PPA de 2021 y 2022;
- 16 de la tabla de impuestos: el diferido por intangibles, ROU y pasivos (9), la amortización y el valor neto de las relaciones con clientes (4) y CVAE/IRAP (3). Sostienen el «mayoritariamente no deducible [I]»;
- 5 de crecimiento orgánico (anclas S2C orgánicas);
- 1 de partidas puntuales (`OOIE_PLUSV_2025`);
- 18 de la tabla de financiación;
- 10 del horizonte 2021–22: capex por tipo, amortización de lino e interés devengado de arrendamientos.

**He comprobado por mi cuenta las cuatro primeras** con identidades que el propio CSV permite y el contraste no afirma [P][D]:
- componentes de la D&A frente al total: residuo 0,0 en 2021 (744,8) y −0,1 en 2022 (799,0);
- segunda presentación de la amortización ROU en el movimiento de arrendamientos: 92,6 (URD 2022 p.302) y 103,7 (URD 2023 p.321);
- segunda presentación de la PPA en la cuenta de resultados: 81,1 (URD 2022 p.258) y 82,9 (URD 2023 p.276).

Los datos están bien. Falta que el script lo afirme.

**Corrección propuesta.** Afirmar R6, R7, R16 y R22 también para 2021 y 2022. Listar en la tabla de cobertura todas las entradas con efecto y sin comprobación, no solo las clave. Decir en los límites de E9 de qué entradas depende el C53 de referencia.

Nota de recuento: el autor declara 363 entradas usadas, que son las solicitadas por el cálculo. Con efecto en alguna salida o comprobación hay 320.

### N3 · menor · `contraste_f1.py` · acepta una verificación que no corresponde al CSV

`contraste_f1.py` recibe el CSV y la verificación por separado y solo cruza el identificador y el estado de cada fila. Si el CSV cambia después de verificar, el cálculo sigue.

**Prueba** (mutante H2): se cambia `DA_ROU_U23_2022` de −103,7 a −93,7 en el CSV y se entrega la verificación original. Código 0, y el C53 de referencia de A1 pasa de 2,445 a 2,476.

**Corrección propuesta.** Guardar en la verificación las huellas del CSV y de `fuentes.json`, y exigir que coincidan; o comparar el literal y el valor de cada fila.

### N4 · menor · especificación E2, matriz de coherencia · dos combinaciones mal definidas

**(a) Fila «`margen_despues_de_arrendamientos`».** Remite a «la variante A1′ del informe» como f «sin pagos de arrendamiento». Pero A1′ solo quita el principal (C49). El interés de arrendamiento sigue dentro de C48 y, por tanto, de f [D]: 25,067 de media, el 0,55 % de las ventas, 26,4 en la base 2025, antes de impuestos (`resultados_revisor_3/recalculo_3.txt`, punto 9). Con un margen posterior a los pagos, ese interés se contaría dos veces. Quitarlo de C48 choca con E0.3, que conserva C48 = 108 [DH].

Hay una vía que no toca ninguna entrada registrada [D]: calibrar f con el NOPAT calculado sobre el mismo margen que se proyecta y con la reinversión sin ROU. Por la identidad de calibración, el flujo sin crecimiento reproduce entonces el FCF base más la inversión neta propia de la historia, cualquiera que sea la definición del margen. La especificación no da esa fórmula ni una prueba.

**(b) `EBIT_NIIF16_PPA_decreciente` con `A2_propio`.** La matriz dice que «f devuelve solo la PPA proyectada». Eso exige una f que cambie con el tiempo o un término aparte, y E3 dice «sin cambios en la estructura del flujo ni del terminal». No hay fórmula ni prueba.

**Corrección propuesta.** Definir las dos combinaciones con su fórmula y su criterio de prueba, o retirarlas de las admisibles y dejarlas en V-F1h. No es el caso de este expediente: la fase C ancla los márgenes en el EBIT NIIF 16 publicado.

### N5 · menor · especificación T3b · A3_estimado no tiene referencia de ancla ni de flujos

T3b fija f y el flujo sin crecimiento de tres casos sintéticos. E4 exige que el ancla C53 use la misma D_X, y T2 y T3 fijan además los flujos de los años 1–11 «para detectar una implementación que cambie f en un término y no en otro». En A3 falta lo mismo: una implementación que aplicara la D_X estimada a f pero no al ancla ni al terminal pasaría T3b.

Los C53 que corresponden a los tres casos son 2,651525243106, 1,612524303305 y 2,005440531963 [D] (`recalculo_3.txt`, punto 4).

**Corrección propuesta.** Añadir a T3b el C53 y los flujos de los años 1–11 de al menos el caso del punto medio, generados por `contraste_f1.py`.

### N6 · forma · informe §0.2, §2 y §5.4; respuestas a O3 · dos afirmaciones sobre los residuos más fuertes que la prueba

1. «Si cambia cualquiera de ellas […], la comprobación falla» (§5.4) y «un error nuevo en cualquiera de sus tres cifras la hace fallar» (respuestas). Solo falla si el error neto supera 0,15. Con el gasto devengado en 29,3 o en 29,1 en lugar de 29,2, R13 pasa y el contraste termina con código 0 (mutantes H3a y H3b). Es el límite de detección que el propio test del autor documenta para otra cifra; basta decirlo igual aquí.
2. R16 de 2023 vale −0,1 y su cota es 0,10: pasa por igualdad. La causa es que la amortización ROU de 2023 se imprime dos veces con valores distintos [P]: 115,8 en la nota 4.5 (DEU 2024 p.296) y 115,9 en el movimiento de arrendamientos (p.312; 48,2 + 64,1 + 3,6). La tabla de residuos de §2 no muestra este residuo, que es el único que agota su cota. E1 fija la nota 4.5 como fuente, así que las referencias están bien definidas.

### N7 · forma · informe §1 · recuento que no coincide con la salida

§1 dice que el contraste usa «359 entradas». `resultados/contraste_f1.log` y las respuestas del autor dicen 363.

### N8 · forma · varios

- **(a)** §0.1, «acreditadas en todas»: ver N1, corrección 5.
- **(b)** §0.6, «respaldada por la propia práctica de Elis». La nota 6.5 respalda que el arrendamiento se cuente una sola vez, como renovación dentro de la inversión: el esquema de A1′. No respalda literalmente que «el coste son los pagos». §5.3 ya lo matiza bien; el resumen puede decir lo mismo.
- **(c)** «Rechaza 32 contraejemplos» (§0.1 y README). Uno de los 32 es el control manual justificado, cuyo resultado esperado es PENDIENTE, no un rechazo.
- **(d)** El «control negativo» del año 11 es una identidad algebraica: pasaría también si la diferencia fuera cero. Los desvíos que detectaría la referencia son 166,6 / 205,4 / 223,9 en A1 y 274,1 / 337,8 / 368,3 en A2 [D] (`recalculo_3.txt`, punto 3). Conviene dar esas cifras en T2 y T3.
- **(e)** `revision/ESTADO.md` dice que el commit congelado «solo cambia este archivo y el manifiesto» respecto a C4. Cambia también una línea de `RESPUESTAS_AUTOR_1.md`. El autor lo corrige en f30c66c.
- **(f)** La regla de edición de los saldos da por vigentes dos publicaciones para la misma fecha: el cierre de 2023 del DEU 2024 y la apertura de 2024 del URD 2025. Hoy los valores coinciden (513,7 y 538,3) [P]. Conviene declarar cuál prevalece si difirieran.

---

## 6. Recálculos y evidencia contraria (alcance b)

### 6.1 Recálculos

`scripts_revisor_3/recalculo_3.py` usa las cifras que transcribí de los PDF en la revisión n.º 1 y una réplica propia del motor, con aritmética exacta. No usa el CSV ni el código del autor. Salida en `resultados_revisor_3/recalculo_3.txt`.

| Magnitud | Revisor | Autor |
|---|---|---|
| f de A0 / A1 / A2 / B | 0,041681455274 / 0,012624225323 / −0,006118601744 / 0,022646228408 | Igual |
| Flujo sin crecimiento de A0 / A1 / A2 / B | 248,496395342656 / 387,878115969269 / 477,783708846410 / 339,804571572014 | Igual |
| C53 de A0 / A1 / A2 / B | 9,039509536785 / 2,445331695332 / 1,612524303305 / 2,651525243106 | Igual |
| Año 11 de A1 (MALO / NORMAL / BUENO) | 294,942490201187 / 413,845194930899 / 488,862107627977 | Igual |
| Año 11 de A2 | 402,413237593105 / 546,310847791079 / 633,271006526708 | Igual |
| Años 1–10 de A1 y A2, los tres escenarios | — | Diferencia máxima 5·10⁻¹³ |
| A3 sintético, punto medio: f y flujo sin crecimiento | 0,008263813332 y 408,794140209212 | Igual |
| O4: flujo del año 1 con S2C = C53 (A0 / A1 / A2) | 231,277 / 312,537 / 360,899 | Igual |
| O4: aumento de ventas que anula la brecha (A1 / A2) | 517,648 / 496,594 | Igual |
| O9: partidas puntuales | +13,675 − 4,032 + 18,293 = +27,936 | Igual |
| O10: pagos escalados; diferencia con 2025; ROU sin devolver | 161,122; 16,778; 10,118 | Igual |
| O7: diferido de intangibles ÷ amortización de relaciones con clientes | 18,3 % / 24,2 % / 21,0 % | Igual |

**Control negativo de la implementación parcial** [D]. Con la f nueva en los años 1–10 y la f de A0 en el terminal, el año 11 queda en el valor de A0 (128,3 / 208,5 / 265,0) y se desvía de la referencia en 166,6 a 368,3. Con la f de A0 en los años y la nueva en el terminal, el año 1 se desvía en 142,2 a 241,9. Ningún desvío es cero.

**A3 con valores sintéticos** [D]. f es lineal en la media de D_X de la ventana: f = f de A0 − (D&A total media − D_X media) ÷ ventas medias. Lo he comprobado también con una D_X no uniforme. Por eso el punto medio de la D_X da el punto medio exacto de f y del flujo.

**Ratios fiscales de O7** [P][D]. 15,5 ÷ 84,6; 20,3 ÷ 83,9; 17,5 ÷ 83,5. Numeradores leídos en URD 2023 p.346, DEU 2024 p.338 y URD 2025 p.393; denominadores en DEU 2024 p.310 y URD 2025 p.364. El ratio de 2024 combina el diferido de la edición original con la amortización reexpresada; con la amortización original (83,8) sigue siendo 24,2 %.

### 6.2 Caja no nula (O15)

Reproducida con un solo proceso de LibreOffice. Con Análisis!C76 = 0, 250 y −80, Motor!M6:M8 = C76 y (Motor!BL − Motor!M)·r = 248,496395342656 en los tres escenarios. La identidad anterior se desviaría en −227,5 y +72,8.

### 6.3 Premisa (iv) de §5.3: evidencia contraria buscada por el revisor

La premisa fallaría si reponer el activo arrendado exigiera caja propia además de los pagos. He buscado tres cosas:

1. **Pagos iniciales fuera del pasivo.** Si parte de las altas de ROU se pagara al contado, las altas del activo superarían a las del pasivo. No ocurre [P][D]: los contratos nuevos suman 132,6 / 145,7 / 183,9 en el activo y 132,6 / 145,7 / 184,0 en el pasivo (DEU 2024 p.312; URD 2025 p.366).
2. **Política contable.** El URD 2025 (p.365) admite en el coste del ROU los costes directos iniciales y los pagos anticipados, y en el pasivo el precio de una opción de compra. Es la norma general; no publica importes. La igualdad anterior indica que no son materiales [I].
3. **Términos de búsqueda** en el URD 2025: mejoras en locales arrendados, opción de compra, venta con arrendamiento posterior, desmantelamiento, incentivos, períodos sin renta. Solo aparece la política de la p.365.

No encuentro evidencia publicada contra la premisa (iv) en las cinco fuentes verificadas. La conclusión del autor, «[D, condicionada a la premisa iv]», está bien marcada.

**Un matiz, que no es evidencia contraria.**
- [P, fuera de las cinco fuentes y posterior a la fecha base] El informe semestral de 2026 (p.10) dice que el grupo «also benefits from a rent-free period on its new headquarters, running until December 2028».
- [P] Las altas de derechos de uso de inmuebles fueron 57,1 en 2025, frente a 10,4 en 2024 y 26,9 en 2023 (URD 2025 p.366; DEU 2024 p.312). El URD 2025 menciona el traslado de la sede (p.13), pero no el período sin renta.
- [I] Si esa sede forma parte del alta de 2025, sus pagos quedan por debajo de su coste hasta 2028. El importe no se publica. No contradice la premisa (iv), que trata de un desembolso adicional a los pagos y no de su calendario. Sí refuerza el límite que el autor declara en §5.5: la razón de pagos sobre ventas de la ventana puede quedarse corta. Conviene citarlo allí.

---

## 7. Textos cambiados (alcance c)

**Informe.** He leído el informe congelado entero y he cotejado con las salidas o recalculado las cifras de las secciones cambiadas. Coinciden:
- §0 y §1: 716 filas; 702 / 14 / 0; 39 casos (7 + 32); 7 casos; 236 = 136 + 72 + 28; 18 comprobaciones de la copia recalculada; 71 residuos; 71 de 72 entradas clave. La única discrepancia es el 359 de N7.
- §2, tabla de residuos: coincide con `residuos_con_cota`, salvo la omisión de R16 de 2023 (N6). La explicación de la deuda neta de 2024 es correcta: caja 622,1 en el DEU 2024 (p.329) y 622,0 en el URD 2025.
- §4.3, §5.2, §5.3 y §5.4: 139,4; 229,3; 81,3; 129,6; 517,6; 496,6; 11,3 %.
- §6.1, §6.2, §6.3 y §6.4: 46,2 %; 396; 867,2; 736,0; 954,0; 1.003,5; 86,8; 3,3 años; 138; 45 %; 28 %; 89,9.
- §7 y §8: impuesto nocional, escudo, pagado menos nocional, 25,4 / 23,4 / 21,9, 1,87 %, 41 %, 87,2, 1,82 %, 63 %.
- §12 y §13: el estado de la revisión y los comandos son exactos; los he ejecutado.

**Marcas de evidencia.** No encuentro ningún [P] que sea solo [I] en los textos cambiados. La fiscalidad de la PPA está ahora como [I]. La premisa (iv) está como [I] y su conclusión como [D] condicionada. Los matices están en N6 y N8.

**Especificación.** E2 (N4), E4, E5, E8 y E9 leídos. T2, T3, T3b y T13 recalculados. T12 describe bien las salidas actuales. T14 hereda el límite de N1.

**Respuestas del autor y estado.** Las 17 respuestas describen cambios que existen en el commit congelado. Las pruebas que citan existen y dan lo que dicen. Imprecisiones: N6 (1), N7 y N8 (e).

**Clasificación de las afirmaciones centrales, tal como quedan:**

| Afirmación | Clase | ¿Bien marcada? |
|---|---|---|
| Cifras de 2021–2025 y sus páginas | [P] | Sí |
| FCF base 307,933; f = 4,168 %; puentes; réplica del motor | [D] | Sí |
| Dos tercios del lino plano mantienen el stock en circulación | [P], parcial y sin importes | Sí |
| Efecto precio y efecto volumen en 2024 y 2025 | [P] la existencia; no publicada la cuantía | Sí |
| El coste de arrendamiento se cuenta dos veces a crecimiento cero y en el terminal | [D], condicionada a la premisa (iv) [I] | Sí |
| La amortización de lo adquirido es mayoritariamente no deducible | [I] apoyada en [P][D] | Sí |
| La cartera se repuso orgánicamente en la ventana | [I]; evidencia parcial | Sí |
| Reposición monetaria igual a la PPA | [H] implícita de la V6.3 | Sí |
| Reinversión necesaria entre la D&A propia y el capex propio | [I] con premisas; no es dato | Sí |
| Elección de perímetro, política de la PPA, F1 (a/b/c) | [DH] pendiente | Sí; no se adopta ninguna |
| C48 = 108; E1, D3, E2 y E6 | [DH] registradas | Se conservan |

---

## 8. Conclusión sobre las conclusiones materiales

| Conclusión del informe | ¿Cambia con esta revisión? |
|---|---|
| La conciliación 2023–2025 y el FCF base 307,933 son correctos | No. Reproducidos; las filas nuevas están comprobadas en los PDF |
| C48 = 108 se mantiene con su derivación | No |
| El motor A cuenta dos veces el coste de arrendamiento a crecimiento cero y en el terminal, bajo la premisa (iv) | No. No encuentro evidencia contraria |
| El doble cómputo de los intangibles adquiridos no está demostrado y requiere una decisión de política | No |
| La reinversión necesaria no está publicada como importe; el nivel sigue `pendiente_de_datos` | No |
| Ninguna alternativa se adopta | No |

**Lo que sí cambia** es el valor que debe darse a las herramientas como prueba. Un código de salida correcto y «702 OK» no acreditan por sí solos el ejercicio, la unidad, el perímetro ni el concepto de una cifra (N1). Cuatro entradas que fijan valores de referencia de la especificación solo están comprobadas por lectura (N2). Esto debe corregirse antes de usar T12 y T14 como criterio de aceptación.

---

## 9. No comprobado

- **Reglas V-F1a a V-F1h y pruebas T8 y T14.** Están especificadas, no implementadas. No se pueden ejecutar.
- **Árbol del hito 4.15 y rama del frente técnico.** No he repetido la verificación del manifiesto 4.15 ni he revisado los commits técnicos que §1 del informe describe. Motivo: quedan fuera de lo afectado.
- **Ausencia de datos en los documentos de 2016–2020 y de 2026.** He comprobado las citas del autor y he buscado por términos. No he leído esos documentos enteros.
- **Lectura visual de los PDF.** Todo se apoya en `pdftotext -layout`, como en el material del autor.
- **Las 28 identidades algebraicas, una a una.** He derivado de nuevo las que sostienen T3b y el control del año 11. Las demás se cumplen por construcción y no prueban datos.
- **Configuración de la sesión del autor.** No es verificable desde esta sesión.
- **Regeneración del libro y de los expedientes.** No se ha hecho ni correspondía. Solo se recalculó una copia temporal para O15.
- **Versión eb77dea.** Solo he ejecutado sobre ella las sondas de §11. No he repetido su reproducción completa.

---

## 10. Reproducción de esta revisión

Con un árbol `munger_v2_r1` materializado y verificado, y un worktree del commit congelado del autor:

```bash
AUTOR=<worktree de 1864c4e>/docs/validacion_economica_paralela/frente_E_F1_elis
RAIZ=<ruta>/munger_v2_r1
LIBRO=$RAIZ/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
cd revision/scripts_revisor_3
python3 -I prueba_mutantes_3.py  --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
python3 -I prueba_mutantes_3b.py --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
python3 -I cobertura_por_mutacion.py --autor "$AUTOR" --libro "$LIBRO"
python3 -I recalculo_3.py --autor-json "$AUTOR/resultados/contraste_f1.json"
python3 -I comprobacion_tokens.py --autor "$AUTOR"
# adenda: un worktree por versión del autor (eb77dea, 1864c4e, f30c66c)
python3 -I sondas_revisor.py --raiz "$RAIZ" --libro "$LIBRO" --version eb77dea=<carpeta> --version 1864c4e="$AUTOR" --version f30c66c=<carpeta>
python3 -I ../scripts_revisor/prueba_mutantes.py --raiz "$RAIZ" --autor "$AUTOR" --libro "$LIBRO"
```

Los scripts no escriben en la carpeta del autor: trabajan con copias en una carpeta temporal. Las salidas están en `revision/resultados_revisor_3/`:

| Archivo | Contenido |
|---|---|
| `prueba_mutantes_3.txt` | Mutantes K0, A1, A2, A4, A5, B1, B2, C1, D1, D2, E1 y F1–F3 |
| `prueba_mutantes_3b.txt` | Mutantes H1, H2, H3a–c, H4 y H5 |
| `comprobacion_tokens.txt` | Números tras el rótulo en las 546 filas reales del modo por defecto |
| `cobertura_por_mutacion.txt` | Clase de cada una de las 499 entradas de la edición vigente |
| `recalculo_3.txt` | Recálculo independiente y comparación con las referencias del autor |
| `sondas_revisor.txt` | Adenda: sondas de un solo campo en las tres versiones, equivalencia con una sonda por fila y contraejemplos P1, P2a, P2b, U1, U2 y X1–X5 |
| `prueba_mutantes_3_sobre_f30c66c.txt` y `prueba_mutantes_3b_sobre_f30c66c.txt` | Adenda: los mutantes de N1–N3 sobre f30c66c. Mismo resultado que sobre 1864c4e |
| `prueba_mutantes_rev1_sobre_commit_congelado.txt` | Mutantes de la revisión n.º 1 sobre el commit congelado |

---

## 11. Adenda: sondas externas de un solo campo y commit f30c66c del autor

Esta sección responde a la adenda que la sesión del autor envió el 15-nov-2026 a las 20:11 UTC. La leí a las 20:49 UTC, con el informe principal ya publicado (commit 11b999a). Las secciones anteriores no cambian, salvo tres retoques que remiten aquí: la primera fila de §2, N8 (e) y las listas de §9 y §10.

### 11.1 Material añadido y reproducción

- **Evidencia externa**, leída: carpeta `seguimiento_eb77dea/` del contraste externo (rama `auditoria/economica-f1`, commit e57239c2482ed02cae3b4a7236d89aef1f6a773c). Sostiene que, sobre eb77dea y con los años correctos, dos mutaciones separadas pasaban con código 0 y 707/707: la unidad de `CREC_ORG_2025` y el perímetro de `IS_VENTAS_2025`.
- **Commit del autor posterior a la congelación:** f30c66c. Respecto a 1864c4e cambia 14 archivos, todos del frente E:
  - `verificar_cifras.py`: función `columna_de_matriz` y su uso en el perímetro;
  - `test_verificar_cifras.py`: 42 casos (8 positivos y 34 contraejemplos);
  - `sondas_metadatos.py` con tres salidas, y `mutantes_revisor_sobre_C6.txt`;
  - informe (§0.1 y §1), especificación (T12 y T14), README, estado, respuestas y manifiesto.
- **Reproducido sobre f30c66c:** verificador (código 2, salida idéntica), test 42/42 (registro idéntico), contraste (código 0, JSON idéntico), test de residuos 7/7, manifiesto 130 de 130, mis mutantes de la revisión n.º 1 (salida idéntica a su registro) y su `sondas_metadatos.py` (677/677 y 677/677).
- **Mis mutantes de N1–N3 sobre f30c66c** dan exactamente el mismo resultado que sobre 1864c4e. **N1, N2 y N3 valen igual para f30c66c.**

### 11.2 Las sondas, reproducidas (encargo a)

Script propio: `scripts_revisor_3/sondas_revisor.py`. Ejecuta el verificador de cada versión sobre el CSV de esa versión. Salida en `resultados_revisor_3/sondas_revisor.txt`.

| Versión | Sonda de unidad (`CREC_ORG_2025`) | Sonda de perímetro (`IS_VENTAS_2025`) | Unidad cambiada en cada fila de tabla | Perímetro cambiado en cada fila de tabla |
|---|---|---|---|---|
| eb77dea | Pasa: código 0, 707/707 | Pasa: código 0, 707/707 | 0 de 671 detectadas | 0 de 671 |
| 1864c4e | Rechazada, en unidad | Rechazada, en perímetro | 677 de 677 | 673 de 677 |
| f30c66c | Rechazada, en unidad | Rechazada, en perímetro | 677 de 677 | 677 de 677 |

- **Las cifras del autor son exactas.** Las 4 filas sin detectar en 1864c4e son los totales de matriz `VENTAS_LINO_PLANO_2025`, `VENTAS_SEG_2025`, `VENTAS_SEG_2024` y `VENTAS_SEG_FR_2023`, que quedaban PENDIENTE.
- **La extensión del autor equivale a una sonda por fila.** Cambiar todas las filas a la vez da, en cada fila, el mismo estado que cambiar solo media tabla (0 diferencias en las tres versiones y en los dos campos) y que evaluar la fila sola en su propio CSV (0 diferencias en una muestra de 40 filas por versión y campo). Coincide con el código: cada fila se evalúa con su línea, su página y constantes.

**Qué prueban estas sondas y qué no** [D, leído en el código]. Cambian la etiqueta declarada y dejan la cifra intacta. Prueban que una etiqueta cambiada se detecta. No prueban que la etiqueta correcta esté acreditada:
- **Unidad.** La sonda cambia «mm EUR» por «%», o al revés. En las 677 detecciones decide el signo «%» del literal: 657 son «unidad % para un literal sin %» y 20, «unidad mm EUR para un literal en porcentaje». La regla que debería acreditar los millones, la declaración de unidades de la tabla, no decide ninguna.
- **Perímetro.** La sonda declara «segmento Francia» en filas del grupo. La delata que el rótulo de la línea no es «France» o que la columna de la matriz es el total. No prueba el caso contrario, que es el que importa para los cálculos: una cifra de un segmento o de un país declarada del grupo.

### 11.3 Dictamen campo por campo (encargo b)

| Campo | Versión | Vía que lo acredita | ¿Independiente de lo declarado? | ¿Trazable fila a fila? | Cobertura |
|---|---|---|---|---|---|
| Unidad | eb77dea | Ninguna: es un campo declarado que nadie lee | — | — | Sin cobertura |
| Unidad | 1864c4e y f30c66c (iguales) | El PDF, con dos reglas: (1) el signo «%» del literal; (2) la declaración de unidades reconocida más próxima por encima de la línea | Sí | Sí: dimensión `unidad` de `verificacion_cifras.json`, con la línea de la declaración | (1) distingue un porcentaje de un importe. (2) acredita «millones de euros» solo si esa declaración se aplica a la línea. Las 14 filas PENDIENTE son correctas. Quedan en OK los contraejemplos U1, U2, B1 y B2 |
| Perímetro | eb77dea | Ninguna | — | — | Sin cobertura |
| Perímetro | 1864c4e | El PDF: la cabecera de la página; el rótulo de la línea, si es un segmento; en una matriz, la última columna si la cabecera acaba en «Total». Un segmento declarado en una matriz queda PENDIENTE | Sí | Sí: dimensión `perimetro` | Acredita la página, no la tabla. Quedan en OK P1, P2a y C1 |
| Perímetro | f30c66c | Lo anterior. En una matriz, además, la columna del token: comprueba el orden de las ocho cabeceras y cuenta la posición desde la derecha | Sí | Sí | Lo anterior. Acredita también columnas de segmento, con el fallo de N9 |

**Contraejemplos de las heurísticas.** Son filas nuevas cuya cifra existe en el PDF [P]; «OK» significa OK en las cinco dimensiones.

| Heurística | Contraejemplo | 1864c4e | f30c66c |
|---|---|---|---|
| Tabla de otro perímetro, sin rótulos de segmento, en una página consolidada | **P1.** Ventas de Alemania, 621,2, de la tabla por países de la nota 3.3 (URD 2025 p.346), declaradas del grupo | **OK** | **OK** |
| Segmento fuera de una matriz de ocho columnas | **P2a.** Ventas del segmento «Other», 35,6 (URD 2025 p.307), declaradas del grupo. **P2b.** La misma cifra con su perímetro correcto. **C1** (N1): margen de Francia como grupo | P2a **OK**; P2b FALLO; C1 **OK** | Igual |
| Línea o tabla en otra unidad bajo una declaración de millones | **U1.** Número medio de acciones, 233.954.020 (URD 2025 p.395), bajo «(In millions of euros)». **U2.** Acciones suscritas, 889.250 (p.362): hereda la declaración que lleva el rótulo de la línea anterior. **B1, B2** (N1) | **OK** | **OK** |
| Matriz con orden de cabeceras no canónico | **X3–X5.** URD 2021 p.247: France, UK & Ireland, Central Europe, Scandinavia & Eastern Europe, Southern Europe, Latin America | Segmento declarado: FALLO o PENDIENTE; total del grupo: OK | Los dos segmentos, PENDIENTE; total, OK. Es el comportamiento prudente: **no es objeción** |
| Matriz con una celda vacía (no pedida; encontrada al revisar f30c66c) | **X1, X2.** «Adjusted EBITDA margin» (URD 2025 p.344), sin cifra en la columna de eliminaciones | X1 FALLO; X2 PENDIENTE | **X1 OK; X2 FALLO** (N9) |

Notas:
- P2a usa el modo «crecimiento» porque la línea tiene seis números; el ejercicio es el correcto. P2b muestra el reverso: la declaración correcta se rechaza, de modo que la única forma de registrar esa cifra en OK es con el perímetro equivocado.
- No he encontrado en las páginas de grupo del URD 2025 una tabla entera sin declaración de unidades debajo de otra de millones y con cabecera de dos ejercicios. Los casos reales son líneas en otra unidad dentro de una tabla de millones (U1, B1, B2) y tablas que llevan la unidad en el rótulo de cada línea (U2). La tabla de plantilla de la p.353 declara «(In number of people)»: el verificador ignora esa declaración y la deja PENDIENTE, que es lo correcto, porque no hay otra por encima.
- En el DEU 2024 (p.293–294) la cabecera «Autres secteurs» está partida en dos líneas y el orden tampoco se acredita. Probado con una sonda sobre la p.293: f30c66c deja PENDIENTE una columna declarada «segmento Francia».

### 11.4 Lo que acreditan las magnitudes y lo que acreditan las etiquetas (encargo c)

- **Etiquetas** (unidad y perímetro; también ejercicio y edición). Son declaraciones del CSV. Las contrasta con el PDF solo el verificador, con las reglas y los límites de §11.3. Una mutación solo de etiqueta no cambia ningún cálculo.
- **Barrera de `contraste_f1.py`.** Aborta si la etiqueta declarada de una entrada usada no es la que pide el cálculo. Lo he comprobado con las dos sondas y el verificador saltado: código 1 y ningún informe, en 1864c4e y en f30c66c. Esta barrera compara lo declarado con lo esperado; no lee el PDF.
- **Magnitudes.** Las acreditan el libro (136 comprobaciones) y los residuos (71). Acreditan que el número cuadra con otra presentación. De forma indirecta acreditan también su unidad y su perímetro: una cifra en miles, por acción o de un segmento rompería la identidad.
- **Alcance de esa vía indirecta.** Solo las entradas con identidad o con libro. De las 320 con efecto, 226 tienen identidad de fuente, 40 solo libro y **54 ninguna** (N2). En esas 54, la unidad y el perímetro descansan en las reglas del verificador y en la lectura independiente.

### 11.5 Objeciones nuevas de la adenda

**N9 · menor · f30c66c, `columna_de_matriz` · con una celda vacía acredita el segmento equivocado y rechaza el correcto.**
- La función comprueba que las ocho cabeceras estén en el orden de Elis. Después obtiene la columna del token **contando desde la derecha**, no por su posición horizontal. Si la línea tiene una celda vacía, las columnas situadas a su izquierda se desplazan una posición.
- Prueba (X1, X2): la línea «Adjusted EBITDA margin» de la matriz del URD 2025 p.344 tiene siete números, porque la columna de eliminaciones va vacía. El margen de Francia, 41,9 %, declarado «segmento Europa central», queda **OK**. Declarado «segmento Francia», que es lo correcto, queda **FALLO**. En 1864c4e el primero era FALLO y el segundo PENDIENTE.
- Los textos de f30c66c dicen que la columna se identifica «por el orden horizontal de las ocho cabeceras». Es inexacto: el orden se comprueba; la columna se cuenta.
- Alcance: ninguna fila real declara un segmento. Las 4 filas reales de matriz son totales, en la última posición, donde el recuento acierta.
- Corrección propuesta: asignar la columna por la posición horizontal del token respecto a las cabeceras, o exigir ocho números en la línea y dejar PENDIENTE las demás.

**N10 · menor · textos de f30c66c: respuestas («Sondas externas…»), informe §1 y especificación T12 · las sondas se presentan como cobertura de la unidad y del perímetro.**
1. T12 añade como criterio «0 mutaciones de unidad o de perímetro sin detectar». Ese criterio se cumple y aun así P1, P2a, U1, U2, B1, B2 y C1 quedan en OK (§11.2 y §11.3). Debe decirse qué mide: etiquetas cambiadas, no cifras de otra unidad o de otro perímetro con una etiqueta verosímil.
2. Las respuestas dicen, sobre el límite del perímetro: «Ninguna de las filas usadas está en ese caso: todas tienen su segunda presentación o su comparación con el libro». La primera parte coincide con mi lectura de los datos reales. La segunda no es exacta: 54 entradas con efecto no tienen ni una ni otra (N2).
3. A favor: f30c66c declara por primera vez tres límites en §1 y en las respuestas (perímetro por cabecera de página; unidad por la declaración más próxima; segmento solo por el rótulo fuera de las matrices). Es la dirección correcta. Falta que las filas afectadas por esos límites queden PENDIENTE y no OK, y que los contraejemplos entren en el test y en T14.

### 11.6 Estado de los requisitos de la carpeta externa (encargo d)

| Requisito de `seguimiento_eb77dea/` | Estado | Motivo |
|---|---|---|
| Las dos mutaciones separadas no deben pasar | **Resuelto** | Se rechazan en 1864c4e y en f30c66c, cada una en su dimensión. Reproducido |
| Comprobar si la unidad está acreditada por otra vía independiente, trazable y vigente, o dejar esa cobertura expresamente pendiente | **Parcialmente resuelto** | La vía es el PDF: independiente de lo declarado y trazable. Acredita porcentaje frente a importe; no acredita «millones» cuando la declaración más próxima no se aplica a la línea. El límite está declarado en f30c66c, pero las filas quedan OK y no PENDIENTE (U1, U2, B1, B2) |
| Lo mismo para el perímetro | **Parcialmente resuelto** | La vía es el PDF: independiente y trazable. Acredita la página, el rótulo de segmento y la columna «Total» de una matriz; no acredita la tabla. El límite está declarado, pero las filas quedan OK (P1, P2a, C1). f30c66c añade el fallo de N9 |
| No dar por cerrado O3 solo porque se rechace el mutante compuesto M4 | **Resuelto** | El autor no lo cierra por M4: prueba cada campo por separado. Con todo, O3 sigue parcialmente resuelta por N1 |
| La suficiencia de la evidencia requiere una revisión sobre el commit que se fije | **Resuelto con esta revisión** | 1864c4e en §1–§10 y f30c66c en esta adenda |
| F1 sigue abierto; sin implementación ni valoración con dinero real | **Cumplido** | Ningún documento del autor ni este lo alteran |

### 11.7 Efecto en el resto de este informe

- **Estados.** O3 sigue parcialmente resuelta. RE3 y RE6 siguen parcialmente cumplidos. Lo demás no cambia.
- **Objeciones anteriores en f30c66c.** N1, N2 y N3 persisten sin cambios. N7 persiste: §1 sigue diciendo «359 entradas». N8 (e) está corregida. N8 (c) pasa a «8 positivos y 34 contraejemplos», con el mismo matiz.
- **Conclusiones materiales.** Ninguna cambia.

