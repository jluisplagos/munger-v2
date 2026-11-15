# Revisión independiente n.º 1 · frente E · conciliación económica F1 de Elis

Fecha: 15-nov-2026. Material revisado: rama `auditoria/economica-f1-frente-e`, commit `96a69ca10cbfd38bea9e6c54a9ef79b9a2eeea0d` (comprobado con `git rev-parse HEAD`). Carpeta `docs/validacion_economica_paralela/frente_E_F1_elis/`.

Esta revisión no modifica el material del autor ni el producto. No contiene valoraciones, precios objetivo ni recomendaciones de inversión, y no adopta ninguna política económica. Todas las páginas citadas son **páginas PDF** (1 = primera del archivo).

Marcas: **[P]** dato publicado que he leído en el PDF · **[D]** derivación aritmética · **[I]** interpretación · **[H]** hipótesis · **[DH]** decisión humana registrada.

Gravedad de las objeciones:
- **material**: afecta al contenido, a la etiqueta de evidencia o al alcance de una conclusión material, o a la suficiencia de un criterio de prueba. Pide corrección antes de dar esa conclusión por revisada.
- **menor**: matiz o debilidad que no cambia la conclusión.
- **forma**: errata o presentación.

---

## 0. Resultado en breve

1. **Las cifras y los cálculos del informe son correctos.** Los he recalculado por mi cuenta desde los PDF, antes de leer el informe, y coinciden: C46–C52, C48 = 108, f, flujo sin crecimiento, composición de f, descomposición del −81,2, réplica de los 33 flujos del motor A y alternativas. No he encontrado ninguna cifra atribuida a un concepto, año o edición equivocados.
2. **La conclusión sobre arrendamientos está fundada**: con el FCF base registrado y el margen NIIF 16, el motor A carga dos veces el coste de arrendamiento a crecimiento cero y en el terminal. Su alcance necesita un matiz (O4): en los años 1–10, y solo si la palanca S2C se anclara en C53, parte del exceso se devuelve.
3. **Dos afirmaciones sobre las fuentes son incorrectas** y afectan a la sección 6:
   - sí hay publicada una proporción parcial de mantenimiento del lino plano, «dos tercios», en los cinco informes (O1);
   - sí hay publicado un efecto precio y un efecto volumen para 2024 y 2025, sin cifra (O2).

   Ninguna de las dos cierra el dato que falta. La conclusión `pendiente_de_datos` se mantiene.
4. **Los scripts del autor reproducen sus resultados byte a byte, pero pueden pasar con datos incorrectos** (O3): una cifra tomada de la columna de otro año pasa las 680 y las 129 comprobaciones sin fallo. El criterio de prueba T12 de la especificación no es suficiente tal como está.
5. Se conservan C48 = 108 con su derivación y las decisiones E1/D3/E2/E6. El informe no declara aptitud para dinero real ni emite recomendaciones.

17 objeciones: 3 materiales, 10 menores y 4 de forma. Ninguna invierte una conclusión material del informe.

---

## 1. Configuración y límites de la independencia

| Elemento | Lo que me consta |
|---|---|
| Sesión | Sesión propia en la nube, `session_01W2RVAoVoXGDAhWhNdDb7w3`, creada el 15-nov-2026 a las 18:09 UTC, título «Revisión independiente F1 Elis (frente E)» |
| Modelo | Los metadatos de la sesión (`get_session`, consultados al empezar) exponen el modelo configurado y el que sirvió el turno, y coinciden entre sí. **No los transcribo en este archivo**: una regla del entorno de esta sesión impide escribir identificadores de modelo en artefactos del repositorio. Los doy en la respuesta final de la sesión, para que el autor o la persona responsable los registren |
| Esfuerzo | `effort_level` = `max` según los mismos metadatos |
| Contexto | Separado del autor. No he tenido acceso a su conversación ni a sus notas; solo al repositorio y al encargo de revisión |

Límites que deben constar:
- **La sesión de revisión fue creada y encargada por la sesión del autor.** Su `parent_session_id` es la sesión que firma el commit 96a69ca. El encargo fija el alcance (A–H) y da números de página, pero no contiene conclusiones del informe.
- Antes del recálculo leí el encargo y los documentos de contexto que el encargo indica. `F1_INICIO_CONCILIACION.md` ya contiene páginas, C46–C52 y el −81,2. La extracción de los PDF y la aritmética son mías.
- Leí `INFORME_CONCILIACION_F1.md` y `ESPECIFICACION_F1_PROPUESTA.md` **después** de terminar el recálculo del paso A.

---

## 2. Preparación y huellas comprobadas

| Elemento | Resultado |
|---|---|
| ZIP de la Release base-4.14 | Descargado por la API REST en una carpeta nueva y vacía, al primer intento, sin errores de red. 1.130.912.246 bytes. SHA-256 `bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e`. Coinciden |
| Materialización | Worktree de `origin/main` (`d69d4837f0e99ce30f38d3461f15cceee9a58730`) fuera del repositorio. `tools/base_414.py materialize`: 1.008 archivos recuperados. `verify`: 6.798/6.798, `complete: true`, código 0 |
| Libro | `…/elis_decisiones/Elis/Elis_v63_evaluada.xlsx`, SHA-256 `d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385`. Coincide. Solo lectura |
| PDF | Los 10 PDF de `elis_decisiones/Elis/fuentes_pdf/` coinciden con `HUELLAS_PDF.txt`. Los cinco usados por el autor coinciden con `datos/fuentes.json`: URD 2021 `e2d316b3…`, URD 2022 `98c0012c…`, URD 2023 `8aac7004…`, DEU 2024 `94e994f0…`, URD 2025 `04bfd087…` |
| Herramientas | pdftotext 24.02.0 (poppler), Python 3.13.18 con `-I`, openpyxl 3.1.5. Mis scripts están en `revision/scripts_revisor/`, en una carpeta distinta de los datos |

No he reproducido, porque el encargo no lo pide: el manifiesto del hito 4.15 (7.004 archivos), el estado de la rama del frente técnico (`d1f1fa9`) ni la búsqueda en el comunicado de resultados de 2025.

---

## 3. Objeciones

### Materiales

#### O1 · material · §6.1, §0 punto 8, §6.4 (M1) · hay una proporción publicada de mantenimiento que el informe no encontró

**Qué dice el informe.** «No hay importes de reparto entre mantenimiento y crecimiento» y, sobre el lino, «No da porcentaje». El resumen concluye «dato no publicado en los URD 2021–2025 [P]».

**Evidencia.** Los cinco informes repiten, en el factor de riesgo de la hostelería, esta frase [P]:

> «investments in linen are automatically impacted, particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation, which is greatly reduced in the event of a downturn»

- URD 2025 p.137; URD 2023 p.239; URD 2022 p.221; URD 2021 p.189.
- DEU 2024 p.135: «en particulier le linge plat dont les deux tiers assurent la maintenance du stock en circulation».

Es una proporción de mantenimiento publicada. La búsqueda del autor no la encontró.

**Límites de ese dato**, que impiden usarlo para cerrar M1:
- Se refiere solo al lino plano. El lino plano fue el 46,2 % de las ventas de 2025 (2.217,4 de 4.796,8; URD 2025 p.347) [P][D]. Las compras de lino no se publican separadas entre lino plano y ropa de trabajo.
- «Mantenimiento del stock en circulación» no es lo mismo que la reinversión necesaria para sostener las ventas: no incluye la dotación inicial de clientes nuevos que sustituyen a los perdidos [I].
- No da importes y es un texto fijo, idéntico al menos desde el URD 2020 (p.133).
- No se puede extender mecánicamente a todo el lino: dos tercios de las compras de lino de 2025 serían 396, por debajo de su amortización, 565,1. Es una ilustración del límite, no una estimación [D].

**Además**, la carpeta de fuentes contiene los documentos de 2016 a 2020, que el informe no dice haber buscado. Los he buscado con términos equivalentes en inglés y francés: no contienen importes de reparto. El Registration Document 2017 (p.52) describe el capex de mantenimiento solo de forma cualitativa. Los de 2018 (p.155) y 2019 (p.84 y p.146) mencionan mejoras de retención y de bajas, sin tasa.

**Corrección propuesta.**
- Citar la frase como [P] en §6.1, con sus límites.
- Cambiar el punto 8 del resumen a «no publicado como importe; hay publicada una proporción parcial y cualitativa para el lino plano».
- Añadirla a M1 como evidencia que una estimación documentada (perímetro `A3_estimado`) debería considerar.
- Declarar el alcance real de la búsqueda (documentos y términos).

La conclusión `pendiente_de_datos` no cambia.

#### O2 · material · §6.2, §3, §6.4 (M5) · el efecto precio y el efecto volumen de 2024 y 2025 sí están publicados

**Qué dice el informe.** «Para 2024–25 no hay un efecto precio publicado en las páginas revisadas». La existencia de un componente de volumen se presenta como premisa sin evidencia para esos años. M5 lo lista como dato que falta.

**Evidencia [P].**

| Documento y página | Texto |
|---|---|
| DEU 2024 p.121 | «Cette nouvelle performance est tirée par l'effet prix, en raison de l'inflation résiduelle en 2024, et par l'effet volume» |
| DEU 2024 p.252 | «une dynamique de prix favorable en lien avec l'inflation du coût de la main-d'œuvre» |
| DEU 2024 p.253 | Francia y Alemania, «bonne dynamique de prix»; Reino Unido, «effet prix favorable»; Latinoamérica, «effet prix conforme à l'inflation» |
| URD 2025 p.122 | «driven by a price effect from residual inflation in 2025, and a volume effect» |
| URD 2025 p.307–308 | Latinoamérica, «Price momentum is favorable, in line with labor cost inflation»; Reino Unido, «adjustments implemented in the region to offset cost inflation» |
| URD 2025 p.309 | «continued growth in volumes processed»; «volume growth and cost inflation» |

Dos de estas páginas están entre las evidencias exportadas por el propio autor: `evidencias/paginas/DEU2024FR_p253.txt` y `URD2025_p307.txt`. La frase del informe es, por tanto, incorrecta incluso limitada a «las páginas revisadas».

**Consecuencias.**
- La premisa de la cota superior (el crecimiento orgánico tuvo un componente de volumen) **tiene apoyo publicado** para 2024 y 2025. Refuerza la inferencia del informe.
- El crecimiento orgánico de 2024–25 (5,2 % y 3,8 %) tampoco fue solo volumen. Las anclas S2C orgánicas sobrestiman la productividad en volumen también en esos años, no solo en 2022–23.
- Lo que falta es la **cuantificación** del efecto precio de 2024–25 a nivel de grupo, no su existencia.

**Corrección propuesta.** Reescribir el párrafo de §6.2, citar estas páginas y redefinir M5 como «cuantificación no publicada».

#### O3 · material · especificación E9 (T12), informe §1 y §13 · los scripts pueden pasar con datos incorrectos

**Qué he comprobado.** `verificar_cifras.py` comprueba huella, página, etiqueta, posición, literal y signo. El informe lo describe bien. Lo que **no** comprueba es que la posición corresponda al ejercicio declarado, ni la unidad, el perímetro o la edición: son campos declarados.

**Contraejemplo reproducible** (`scripts_revisor/prueba_mutantes.py`, salida en `resultados_revisor/prueba_mutantes.txt`):

| Mutación | `verificar_cifras.py` | `contraste_f1.py` | Efecto |
|---|---|---|---|
| M1: `DA_ROU_2025` toma el literal «(132.2)» de la columna de 2024 y se declara 2025 | 680/680, código 0 | 129/129, código 0 | Los residuos R6 y R16 de 2025 pasan de 0,0 a ±17,3. El flujo de referencia de A1 pasa de 387,878 a 381,812 y el de A2 de 477,784 a 471,718 |
| M4: año 2031, unidad «mm EUR» para un porcentaje, perímetro «segmento Francia» | 680/680, código 0 | 129/129, código 0 | Ninguno: los campos no se usan |
| M2: fuente sin campo `sha256` | Aborta con `KeyError` | — | No acepta, pero no informa del motivo |
| M3: `sha256` vacío | Rechaza | — | Correcto |

**Por qué pasa M1.**
- Las identidades R1–R19 se calculan y se muestran, pero no se afirman con una tolerancia: un residuo de 17,3 no hace fallar el script.
- Unas 13 de las 129 comprobaciones son identidades algebraicas que se cumplen con cualquier dato: la descomposición de f (4), la de la reinversión (1), los puentes (4) y el caso sintético (4). He desarrollado la suma de componentes de f: se reduce idénticamente a la definición. La descomposición de la reinversión lleva un término de «residuo de redondeo» que absorbe cualquier diferencia.
- Las comprobaciones sensibles a los datos son las que comparan con el libro: 72 celdas de Historia, 6 de Análisis y 36 del motor, que dependen de las mismas entradas, más la doble vía del FCF base y C53. No cubren los componentes de la D&A, el capex por tipo, las notas de arrendamientos (salvo el principal y el pasivo final), el impuesto corriente y diferido ni los intangibles.
- El caso «columna de otro ejercicio» de `test_verificar_cifras.py` solo cambia la posición y deja el literal. Detecta una discrepancia entre posición y literal, no una columna equivocada.

**Los datos del autor están bien.** Lo he comprobado por otra vía (§4, confirmación 11). La objeción es de suficiencia de la herramienta y del criterio de prueba.

**Corrección propuesta.**
- Afirmar R1–R19 con tolerancia: ±0,15 por defecto y excepciones declaradas, que hoy serían el −0,2 del FCF de 2024 y el +0,4 del interés de arrendamientos de 2025.
- Comprobar el ejercicio contra la cabecera de la tabla. `scripts_revisor/comprobacion_columnas.py` lo hace para las tablas de dos columnas.
- Añadir M1 como contraejemplo del test, y un caso de fuente sin huella con mensaje claro.
- En T12, distinguir comprobaciones contra el libro de identidades algebraicas, y exigir residuos dentro de tolerancia además del código de salida.

### Menores

#### O4 · menor · §5.2, §5.3, §0 punto 6 · alcance de la demostración: en los años 1–10 el exceso depende del ancla de S2C

**Qué dice el informe.** «No depende de la palanca S2C, porque se produce a crecimiento cero». La tabla de §5.2 pone «0 (ΔV/S2C no la devuelve)» en la proyección.

**Lectura alternativa que he buscado y encontrado.** La plantilla ancla la palanca S2C en C53, que se calcula con el mismo perímetro que f: D&A total. Si la palanca fuera C53 = 9,04 y el crecimiento el histórico, ΔV/S2C reproduce la reinversión neta histórica, que ya lleva restadas la amortización ROU y la PPA. En esa senda no hay doble cómputo: la plantilla es coherente consigo misma **solo** en su senda histórica.

**Cuantificación [D]** (`resultados_revisor/sensibilidades_revision.txt`): con el ancla propia de cada perímetro y las palancas del escenario NORMAL,

| | A0 (S2C 9,04) | A1 (S2C 2,445) | A2 (S2C 1,613) |
|---|---|---|---|
| Flujo sin crecimiento | 248,5 | 387,9 | 477,8 |
| Flujo del año 1 (crecimiento 4,5 %) | 231,3 | 312,5 | 360,9 |
| Brecha frente a A0 a crecimiento cero | — | 139,4 | 229,3 |
| Brecha frente a A0 en el año 1 | — | 81,3 | 129,6 |
| Aumento de ventas que anula la brecha | — | 517,6 (10,8 %) | 496,6 (10,4 %) |

Como referencia, las ventas crecieron de 2020 a 2025 un 11,3 % anual compuesto, 398,1 al año de media. La brecha se anula, por tanto, con un crecimiento del orden del histórico, no exactamente en él: f se calibra con 2023–25 y C53 con 2021–25.

**Lo que no cambia.**
- A crecimiento cero y en el terminal, que reinvierte con g/ROIC y no con S2C, el exceso es íntegro.
- En este expediente las palancas S2C (1 / 1,2 / 1,5) no usan C53 sino un perímetro propio, como dice el informe en §3. El exceso se aplica entero en todos los años.

**Matiz propuesto.** Decir en §5.3 que la independencia de S2C vale para el flujo sin crecimiento y el terminal. Añadir que, con la palanca anclada en C53, el exceso de los años 1–10 decrece con el crecimiento y se anula cerca del histórico. Poner una nota en la celda «0» de §5.2.

#### O5 · menor · §5.3, §9 (A1′) · premisa económica implícita y evidencia publicada no citada

La conclusión de §5.3 lleva la marca [D], pero descansa también en una premisa económica que no está numerada: el activo arrendado se repone con nuevos arrendamientos cuyo coste son los pagos, de modo que la amortización ROU no exige además un desembolso [I]. La premisa es sólida, pero conviene enunciarla como (iv) y marcar la conclusión como [D] condicionada a ella.

Hay apoyo publicado que el informe no cita. En sus pruebas de deterioro, que incluyen NIIF 16, la propia Elis define el flujo como [P]:

> «adjusted EBITDA […] +/− change in WC − income tax at standard rate − capital expenditure (including lease renewal)»

URD 2025 p.368; DEU 2024 p.314 («y compris de renouvellement des contrats de location»); URD 2023 p.322; URD 2022 p.303.

Es decir, la empresa cuenta el arrendamiento una sola vez, como renovación dentro de la inversión y sobre un EBITDA sin coste de arrendamiento. Es el mismo esquema que la alternativa A1′. Propongo citarlo en §5.3 y en la fila de evidencia de A1′.

#### O6 · menor · §6.2 · la referencia inferior (D&A propia) tiene evidencia publicada en contra como caso central, y hay señales de contención del capex en 2025

El informe ya dice que la D&A propia «no es una cota demostrada». Falta citar lo publicado:

- Hipótesis de los planes de negocio de las pruebas de deterioro [P]: «the Group's climate plan, with a level of investment greater than the amortization and depreciation historically recorded» (URD 2025 p.369; DEU 2024 p.315; URD 2023 p.322). La nota 1.3 lo repite: las hipótesis de deterioro «include additional future investments» (URD 2025 p.333). La empresa planifica invertir por encima de la amortización histórica. Es evidencia contra tomar A2 como caso central.
- Contención del capex en 2025 [P]: «effective management of capital expenditure, particularly in linen, has kept depreciation under control» y «capex contained despite new workwear contracts and expenditure under the Climate plan» (URD 2025 p.122). También «The Group's capital expenditure has returned to normal levels since 2024» (p.312) y «They remained stable after the sharp increase in previous years» (p.311).
- La inversión neta en lino cae de 102,2 a 56,7 y a 29,1 en 2023–2025 [D], con compras planas (594,3 y 594,2) y amortización creciente (537,6 y 565,1).

Estas señales no demuestran infrainversión: la empresa las presenta como eficiencia y normalización tras 2022–23. Pero son la evidencia pertinente para la pregunta y deben constar. Si hubiera infrainversión en 2025, la cota superior no valdría para ese año. El plan climático es además un tercer tipo de inversión, ni reposición ni crecimiento de ventas, que la definición de §9 no contempla.

#### O7 · menor · §6.3, §0 punto 7 · etiquetas de la fiscalidad y del agotamiento de las relaciones con clientes

1. **«No es deducible en caja» no es un hecho publicado.** El resumen lo lista entre los «hechos publicados». Lo publicado es el ingreso por impuesto diferido de la fila «Intangible assets»: 15,5 / 20,3 / 17,5 [P]. Que la amortización de lo adquirido no reduzca el impuesto de caja es una inferencia [I], bien apoyada: el ingreso equivale al 18,3 %, 24,2 % y 21,0 % de la amortización de las relaciones con clientes (84,6 / 83,9 / 83,5) [D], cerca de los tipos nominales de los países. La fila incluye además marcas y otros intangibles, y hay una fila aparte de fondo de comercio con amortización fiscal. Lo correcto es «mayoritariamente no deducible [I]».
2. **Las altas de 2025 (3,7) son provisionales** [P]: «the initial accounting for some of the business combinations is incomplete […] the amounts above are only provisional» (URD 2025 p.340). Hay un precedente dentro de la misma serie: las altas de 2024 eran 18,0 en el DEU 2024 (p.310) y son 32,3 reexpresadas en el URD 2025 (p.364). La nota 1.4 (p.333) atribuye la reexpresión a tres compras del último trimestre de 2024: «recognition of customer relationships, using the earnings method». El informe marca 351,6 como reexpresado, pero presenta el 3,7 sin esa salvedad.
3. **«Se está agotando»** es correcto como aritmética: 275,1 ÷ 83,5 = 3,3 años sin compras nuevas [D]. Conviene añadir que la amortización no caerá de golpe, porque las vidas van de 4 a 14 años, y que las compras siguen reponiendo cartera a un ritmo de 20–32 al año.

#### O8 · menor · §6.3, §6.4 (M2), §9 · el crecimiento orgánico neto de bajas es evidencia sobre la PPA; hechos publicados no citados

**Coherencia interna.** §6.2 usa el crecimiento orgánico positivo para acotar la reinversión necesaria por debajo del capex propio. §6.3 dice de la reposición monetaria de la PPA que «no hay dato publicado que la sostenga ni que la refute». Pero el crecimiento orgánico se mide sobre las ventas totales, netas de clientes perdidos, adquiridos o no. Fue positivo todos los años y con efecto volumen positivo publicado en 2024 y 2025 (O2). Eso indica que, en la ventana, la cartera se repuso orgánicamente, con un coste que ya está en el EBIT y en el capex propio [I]. Es evidencia parcial contra la hipótesis de reposición monetaria igual a la PPA. No la refuta para el futuro, que es una hipótesis de proyección.

**Hechos publicados relevantes para M2 que el informe no cita [P].**
- «contracts are usually valid for an initial four-year term», con renovación automática y penalización por rescisión de casi todo el valor residual (URD 2025 p.141).
- En 2024, la calidad del servicio «a permis de baisser le taux de pertes» (DEU 2024 p.121).

La tasa sigue sin publicarse.

**Lectura de compensación que he examinado.** El nivel de A0 coincide casi exactamente con «todo el capex propio es reposición y además hay que reponer la PPA con caja»: 339,8 − 89,9 = 249,9 frente a 248,5. La causa es que el capex menos la D&A propia (131,2) es casi igual a la amortización ROU (132,5). Bajo esa lectura el nivel de la V6.3 no estaría sesgado, pero es una compensación numérica de dos efectos, no ausencia de doble cómputo, y la contradice la evidencia anterior.

No propongo cambiar la conclusión «requiere decisión de política». Propongo enlazar ambas secciones y citar estos hechos.

#### O9 · menor · §0 punto 8, §6.4 (M1), §9 · el intervalo 339,8–477,8 hereda partidas puntuales que el propio informe identifica

§4.2 identifica tres efectos de calibración y da sus magnitudes en puntos, pero no las suma ni las traslada al intervalo. En millones, sobre la base 2025 [D]:

| Partida | Efecto en el flujo sin crecimiento |
|---|---|
| Earnout de 2023 dentro de f (−13,0 de media) | +13,7 |
| Plusvalías netas de la ventana dentro de f (+3,8 de media) | −4,0 |
| Plusvalía de 25,7 dentro del margen de partida de 2025 | +18,3 |
| **Efecto neto en todos los perímetros** | **+27,9** |

Si además se cuenta que el earnout no deducible eleva el tipo de 2023, el efecto del earnout sube a 18,6. La fuente relaciona la partida de 2025 con indemnizaciones de seguros: «a high level of insurance benefits in 2025» (URD 2025 p.309) [P].

El efecto es común a todos los perímetros, así que no altera las diferencias entre alternativas, pero es el 20 % de la anchura del intervalo (138). Propongo añadir la salvedad allí donde se cite el intervalo y en los valores de referencia de la especificación, que la heredan.

#### O10 · menor · §5.5, §9 · «coherente con los arrendamientos» necesita una salvedad sobre la tendencia

[P][D] Los pagos de arrendamiento crecen más deprisa que las ventas:

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Pagos ÷ ventas | 3,04 % | 3,30 % | 3,71 % |
| Amortización ROU ÷ ventas | 2,69 % | 2,89 % | 3,12 % |
| Variación del pasivo | +10,9 % | +12,6 % | +16,0 % |
| Variación de las ventas | +12,8 % | +6,1 % | +4,9 % |

- f aplica la media, 3,359 % de las ventas. Sobre las ventas de 2025 son 161,1, frente a 177,9 pagados: 16,8 menos.
- En A1 y A2 el margen de partida lleva la amortización ROU de 2025 (149,5) y f devuelve la media escalada (139,4): quedan 10,1 sin devolver.
- El informe dice en §5.5 que f supone que la cartera arrendada crece con el negocio. No dice que en la ventana creció bastante más.

No es un defecto de las alternativas: es una limitación de proyectar una razón constante. Debe declararse al calificarlas de coherentes.

#### O11 · menor · §8 · la conclusión de deuda constante está fundada, con cuatro límites

La lectura es correcta para la deuda financiera neta: 3.025,4 → 3.038,0 → 3.020,2 [P]. Límites que el informe no dice:

1. **Los arrendamientos no están en base de deuda constante.** El FCF base resta su principal (128,1) y no acredita las altas no monetarias (159,0 / 194,3 / 245,6). La financiación se trata de forma asimétrica: deuda financiera renovada, arrendamientos amortizados. Es legítimo, pero es el origen de F1 y la razón de que A1′ sea la variante simétrica.
2. **Deuda constante no es interés constante.** Con deuda neta plana, los intereses netos pagados subieron un 41 %, de 70,5 a 99,4, por la refinanciación a tipos más altos y el reembolso anticipado del bono de 2026 (URD 2025 p.312) [P]. f usa la media, 82,9, que escalada a 2025 son 87,2, por debajo del último dato.
3. **La estabilidad es de la deuda neta.** La bruta bajó de 3.690,7 a 3.418,3 y la caja de 665,3 a 398,1 [P].
4. **El devengo no monetario de la OCEANE** (9,7 en 2025; URD 2025 p.314) aumenta el pasivo sin caja. No está en C48 por la decisión E6, que no se discute, pero significa que ese pasivo no es constante.

La observación del informe sobre intereses proporcionales a las ventas sin endeudamiento nuevo es correcta. He reproducido 60,4 / 135,9 / 166,1.

#### O12 · menor · especificación E2–E5 · falta controlar el perímetro del margen; estado y umbral de V-F1a

1. **Perímetro del margen.** La especificación obliga a declarar el perímetro de la palanca S2C (E4), pero no el del margen objetivo. A2 devuelve la PPA dentro de f de forma perpetua (1,87 % de las ventas). Solo es coherente si el margen objetivo incluye una PPA de ese orden. Si la PPA se agota y el margen objetivo sigue al EBIT publicado, el motor devolvería un coste que ya no carga. E3 solo declara la limitación fiscal. Propongo un parámetro declarado de perímetro del margen (EBIT NIIF 16 con PPA; con PPA constante o decreciente) y un aviso si no casa con `perimetro_reinversion`. Lo mismo vale para un margen definido después de pagos de arrendamiento, que el informe menciona en §5.3 pero la especificación no controla.
2. **V-F1a** asigna «DATOS INVÁLIDOS» a una incoherencia de definición del modelo. Los datos no son inválidos. En la escala de las Convenciones (§12) encaja mejor «MODELO NO APLICABLE» o un estado propio. Tampoco tiene umbral de materialidad: un caso del motor A con arrendamientos mínimos quedaría bloqueado y pendiente de una decisión humana de perímetro.
3. **El aviso de E4** (perímetro de S2C distinto) no tiene identificador en la tabla E5 y la prueba T8 no lo cubre.
4. **La variante orgánica de C53** usa crecimiento orgánico nominal, que incluye precio (O2). Debe declararse o deflactarse.

#### O13 · menor · especificación E9 · faltan valores de referencia para detectar una implementación parcial

T2 y T3 solo fijan f, el flujo sin crecimiento y C53 para A1 y A2. Los flujos de los años 1–11 solo tienen referencia en A0 (`A0_flujos_libro`). Una implementación que cambiara f en el flujo sin crecimiento pero no en el terminal pasaría T2 y T3. Propongo:

- añadir los flujos de los años 1–10 y del año 11 de A1 y A2 con las palancas actuales, como contraste de implementación y sin valores por acción;
- una prueba para `A3_estimado`;
- la corrección de T12 de O3.

### Forma

#### O14 · forma · §4.3

«Coinciden con los 33 flujos (AU6:BD8), los 3 flujos del año 11 (BF6:BF8)». El rango AU6:BD8 tiene 30 flujos. Son 30 + 3 = 33, como dice el resumen.

#### O15 · forma · `scripts/contraste_f1.py`

La comprobación «Motor!BL·r − exceso de caja = flujo sin crecimiento» calcula `BL·r − C76`. La celda BL es F₀/r + C76, así que lo correcto es `(BL − C76)·r`. Hoy pasa porque C76 = 0. Fallaría sin motivo en un caso con exceso de caja.

#### O16 · forma · README y `scripts/test_verificar_cifras.py`

- El README llama a las 129 comprobaciones «cálculo independiente contra la fuente y el libro». Conviene separar las que comparan con el libro de las identidades algebraicas (O3).
- El caso «columna de otro ejercicio» debería llamarse «posición distinta con el mismo literal».
- Una fuente sin campo `sha256` aborta con `KeyError`. Mejor un fallo con mensaje.

#### O17 · forma · §5.2

La columna de proyección suma la amortización ROU de 2025 (149,5), antes de impuestos, con los pagos medios escalados (161,1). El total de −310,6 no es literalmente lo que resta el flujo. El exceso exacto, que el informe da bien en §5.3, es 139,4: la amortización ROU media escalada, antes de impuestos, porque el impuesto real ya está dentro de f. Basta una nota al pie.

---

## 4. Confirmaciones independientes

Lo que recalculé por mi cuenta y coincidió. Los cálculos están en `scripts_revisor/` y sus salidas en `resultados_revisor/`.

1. **Estados de flujos 2023–2025.** Transcripción propia de URD 2025 p.327 y DEU 2024 p.273. Mismos residuos que el autor: +0,1 en la caja antes de financieros de 2025 y −0,1 en el CFO de 2024.
2. **Notas.** Nota 4.5 (URD 2025 p.350; DEU 2024 p.296), nota 6.3 (p.366; p.312), nota 8.2 (p.379; p.324), nota 9 (p.392–393; p.337–338), tabla de free cash flow (p.314; p.259), cuenta de resultados (p.324) y segmentos (p.344–345).
3. **C46–C52.** 1.429,4333 / 857,1667 / 108,0 / 128,1 / 28,2333 → 307,9333. El libro los registra con tres decimales.
4. **C48 = 108,0** = 82,933 de intereses financieros netos + 25,067 de interés implícito de caja de arrendamientos (19,8 / 25,8 / 29,6). El devengado es 19,8 / 25,8 / 29,2: mismo residuo de +0,4 en 2025.
5. **f.** 0,04168138 con medias exactas; el libro da 0,0416814553. La diferencia, 7,3·10⁻⁸, es el redondeo de las entradas, como dice el informe.
6. **Flujo sin crecimiento:** 248,496.
7. **Composición de f·ventas.** Mi descomposición, en siete bloques, suma 190,066: pagos de arrendamiento 153,167; intereses financieros 82,933; SBC +28,233 y −28,233; impuesto pagado menos nocional −24,901; capex bruto menos neto −10,0; otros no monetarios −11,133. Equivale a la del autor. Confirmo que ni la amortización ROU ni la PPA son componentes de f.
8. **Descomposición del −81,2.** Capex menos D&A de activos propios +132,367; ROU −132,5; PPA −85,467; deterioros −1,133; redondeo −0,067; circulante +5,6.
9. **Puente a 248,496.** Por una vía distinta de la del autor: escala +15,993, margen y tipo +9,987, reinversión escalada −85,417. Mismo total.
10. **Motor A.** Réplica propia desde las Convenciones: los 30 flujos de los años 1–10 y los 3 del año 11 coinciden con el libro, con diferencia máxima de 6,5·10⁻¹³.
11. **Cifras del CSV.**
    - Año de la columna comprobado automáticamente contra la cabecera en 545 filas de dos columnas: todas coinciden.
    - Las 5 señaladas por mi script son columnas de porcentaje de crecimiento, revisadas a mano y correctas.
    - Las 130 restantes (110 de tablas de movimientos y otras posiciones, 10 saldos y 10 de texto) las revisé contra la línea del PDF que casa con cada fila. En las tablas de movimientos comprobé además el bloque de cada año leyendo la página entera: URD 2025 p.364, 366, 367 y 393; DEU 2024 p.310, 312 y 338; URD 2023 p.321 y 346; URD 2022 p.302.
    - Páginas leídas directamente: URD 2025 p.122, 137, 141, 307–309, 311–314, 324, 327, 333, 340, 344–345, 347, 350, 363–370, 379–380, 392–393; DEU 2024 p.121, 135, 252–253, 257, 259, 273, 296, 310, 312, 314–315, 324, 337–338; URD 2023 p.261, 321, 346; URD 2022 p.261, 284, 302; URD 2021 p.211. El resto de las páginas citadas por el autor las contrasté por la línea extraída, no por lectura completa.
12. **Horizonte 2021–2025 y S2C.** C53 = 9,04; 2,445 sin ROU; 1,613 con D&A propia; anclas orgánicas 2,07 / 3,13 y 5,52 / 13,85.
13. **Alternativas.** A1: f = 1,262 %, 387,9. A1′: 1,359 %, 383,2. A2: −0,612 %, 477,8. B: 2,265 %, 339,8. Dos variantes mías que mueven el ajuste al margen en lugar de a f dan 383,5 y 469,3: son coherentes con las del autor.
14. **Impuestos y financiación.** Tipos 29,63 / 27,54 / 25,60 %; nocional 147,2 / 164,2 / 161,3; pagado menos nocional −20,8 / −39,3 / −14,6; puente de la deuda neta de 2025 (17,8) y de 2024 (residuo 0,1).
15. **Scripts del autor sobre mi materialización.** `verificar_cifras.py` 680/680; `test_verificar_cifras.py` 10/10; `contraste_f1.py` 129/129; `tabla_conciliacion.py`. Las cinco salidas son **idénticas byte a byte** a `resultados/`, las 49 páginas a `evidencias/paginas/` y el CSV regenerado con `especificacion_cifras.py` a `datos/cifras_fuente.csv`.
16. **Conservación y límites (H).**
    - C48 = 108 y su derivación se conservan (informe §4.1; especificación E0 y T10).
    - E1, D3, E2 y E6 se conservan y no se vuelven a pedir (§10).
    - No hay valoraciones, precios ni recomendaciones, y no se declara aptitud para dinero real (§0, §13).
    - El commit 96a69ca solo toca la carpeta del frente E: 66 archivos, ninguno fuera.

---

## 5. Lecturas alternativas buscadas (¿hay alguna sin doble cómputo?)

| Lectura | Resultado |
|---|---|
| Palanca S2C anclada en C53 y crecimiento histórico | Sin doble cómputo solo en esa senda. A crecimiento cero y en el terminal persiste (O4) |
| Margen objetivo definido después de pagos de arrendamiento | No es el caso: `fase_c.json` ancla los márgenes en el margen EBIT de la Historia (630,0 ÷ 4.796,8), que es EBIT NIIF 16. Comprobado en el expediente |
| Arrendamientos como deuda renovada (NIIF 16 pura) | El duplicado pasa a ser el principal en lugar de la amortización ROU. Sigue habiendo doble cómputo con el FCF base registrado |
| Reinversión definida sobre capital invertido, con altas ROU como inversión no monetaria | El flujo sigue restando la amortización ROU y los pagos |
| Reposición propia por encima de la D&A propia, por inflación | Compensa numéricamente como máximo 131,2 de los 218 (ROU + PPA), porque la reposición no puede superar el capex si hubo crecimiento en volumen. Es compensación, no ausencia de doble cómputo |
| Todo el capex es reposición y además la PPA se repone con caja | Reproduce el nivel de A0 por coincidencia numérica (O8). Contradicha por el crecimiento orgánico neto de bajas |
| Exceso de caja sumado y a la vez su rendimiento en los intereses netos | No aplica: `Análisis!C76` = 0 |

Conclusión: no he encontrado ninguna lectura razonable de la plantilla, de las palancas del expediente o del FCF base registrado bajo la que el coste de arrendamiento se cuente una sola vez a crecimiento cero y en el terminal.

---

## 6. Conclusión sobre las conclusiones materiales

| Conclusión del informe | Veredicto | Límites |
|---|---|---|
| Conciliación 2023–2025 y residuos | **Fundada.** Confirmada de forma independiente | — |
| FCF base 307,933 y C48 = 108 | **Fundada** | Decisiones registradas; no revisadas como política |
| f = 4,168 % y su composición; ROU y PPA no están en f | **Fundada** | — |
| Réplica del motor A y puente a 248,5 | **Fundada** | El flujo de partida lleva unos +28 de partidas puntuales (O9) |
| Arrendamientos: doble coste a crecimiento cero y en el terminal, defecto de definición | **Fundada** | Alcance en los años 1–10 (O4); premisa económica explícita y evidencia adicional (O5); tendencia de los pagos (O10) |
| Intangibles adquiridos: doble cómputo no demostrado, requiere política | **Fundada como posición prudente** | Etiquetas y salvedades (O7); la evidencia publicada se inclina contra la reposición monetaria en la ventana, sin demostrarlo (O8) |
| Reinversión necesaria frente a crecimiento: dato no publicado | **Parcialmente incorrecta en su formulación** | Hay una proporción parcial publicada (O1) y efectos precio y volumen publicados (O2). La consecuencia, `pendiente_de_datos`, se mantiene |
| Cotas 339,8–477,8 | **Aritmética correcta; premisas razonables** | La premisa de volumen tiene apoyo publicado (O2); la referencia inferior tiene evidencia en contra como caso central (O6); partidas puntuales (O9) |
| Impuestos: no hace falta ajuste fiscal adicional en la calibración | **Fundada** | La limitación en la proyección es mayor que la fiscal: afecta a la devolución de la PPA entera (O12) |
| Financiación: deuda constante | **Fundada con límites** | O11 |
| Alternativas A1, A1′, A2 y cota B | **Coherentes; ninguna elegida por su resultado** | A1′ tiene apoyo publicado no citado (O5); falta el perímetro del margen (O12) |
| Especificación y criterios de prueba | **Verificables, pero no suficientes** | O3, O12, O13 |

**Sobre el conjunto.** El trabajo es cuidadoso y sus cifras son fiables. Las tres objeciones materiales no invierten ninguna conclusión: dos corrigen afirmaciones sobre lo que las fuentes publican y una señala que las pruebas automáticas no bastan para detectar un dato mal periodificado. F1 sigue abierto por las razones que el informe da: hace falta la decisión de la persona responsable y un dato, o una estimación documentada, que Elis no publica como importe.

Esta revisión no declara aptitud para dinero real, no valida ningún precio y no sustituye la integración, la réplica ni la auditoría del material final.

---

## 7. Reproducción de esta revisión

Con un árbol `munger_v2_r1` materializado y los cinco PDF convertidos a texto paginado (`pdftotext -layout <pdf> <carpeta_txt>/<SLUG>.txt`, con los nombres `URD2021`, `URD2022`, `URD2023`, `DEU2024FR` y `URD2025`):

```bash
cd docs/validacion_economica_paralela/frente_E_F1_elis/revision/scripts_revisor
LIBRO=<ruta>/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
python3 -I recalculo_independiente.py "$LIBRO"
python3 -I replica_motor_A.py "$LIBRO"
python3 -I comprobacion_columnas.py ../../datos/cifras_fuente.csv <carpeta_txt>
python3 -I sensibilidades_revision.py
python3 -I prueba_mutantes.py --raiz <ruta>/munger_v2_r1 --autor ../.. --libro "$LIBRO"
```

`pag.py`, `busca.py` y `libro_dump.py` son utilidades de lectura: página de un texto paginado, búsqueda con número de página y volcado de celdas en solo lectura. `prueba_mutantes.py` escribe sus copias mutadas en una carpeta temporal y no toca el material del autor.
