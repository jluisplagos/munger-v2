# Revisión interna · entrega 4.12 (validación supervisada, cierre de la integración y contraste con Viscofan)

**Qué es.** Revisión **interna** de Claude. No es la revisión externa ni la sustituye. La hace un agente revisor (Claude, modelo de la misma familia que los que construyeron y auditaron el trabajo) en un contexto separado, sin haber participado en el trabajo.

**Fecha y hora.** 12 de noviembre de 2026, de 23:10 a 23:30 (hora de la consola, CET).

**Objeto.** El árbol `/home/claude/trabajo_4_12/munger_v2_r1`, comparado donde hacía falta con la 4.11 intacta (`/home/claude/base_4_11/munger_v2_r1`). Rutas relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/` salvo que se diga otra cosa.

**Cómo se trabajó.** Solo lectura del árbol. Los tres expedientes se copiaron a los temporales del revisor y allí se ejecutaron scripts que solo leen (`objetivo_v64.py`, funciones de `entradas_economicas.py` y `dominios_v64.py`) y lecturas con openpyxl. No se ejecutó el pipeline, ni LibreOffice, ni ninguna batería. No se usó internet. Los marcadores pendientes del informe integrado ([VERIFICACION_FINAL], [REVISION_INTERNA], [CONTROLES_REPETIDOS] y FALLOS_REVISION) no se cuentan como hallazgos.

## 1. Veredicto en breve

| Gravedad | Número | Hallazgos |
|---|---|---|
| Bloqueante | 0 | — |
| Importante | 5 | R1–R5 |
| Menor | 4 | R6–R9 |
| Observación | 5 | R10–R14 |

Ningún hallazgo cambia una cifra de valoración, un estado ni un veredicto de los tres expedientes. Las aprobaciones vigentes corresponden al material auditado y a las salidas oficiales. Los cinco hallazgos importantes son afirmaciones que el material no sostiene tal como están escritas: dos en el informe integrado (fechas de Vidrala; quién decide el tratamiento del objetivo), dos en las salidas de los expedientes (cobertura del ámbito; cadena de trazabilidad de Viscofan) y una en el código y los documentos (la instantánea de «entradas económicas» no cubre una fila que mueve el valor).

## 2. Hallazgos

### R1 · Importante · La instantánea de entradas económicas y la cadena de trazabilidad no cubren las adquisiciones de la Historia (fila 13), que mueven el valor en el modo experimental

**Evidencia.**
- `personaje_v2/scripts/entradas_economicas.py`, líneas 85–100: la instantánea son las 58 entradas de la relación de la V6.3 más las celdas de entrada de «Configuración V6.4». La fila 13 de la Historia (adquisiciones netas) no está en esa relación.
- Libro `cierre_condicionado/Vidrala/Vidrala_v63_evaluada.xlsx`, hoja «Configuración V6.4»: `B55 = SUM(Historia!H31:L31)`, con `Historia!L31 = L30 + N(L13)`; `B57` (D_hist) `= B55 + B56`; `B59 = SUM(Historia!H13:L13)`; `B62` (F_hist) `= B60 + B59`; `B72` (f) `= B57 / (B57 − B71)`. Por tanto `Historia!H13:L13` entra en D_hist y en F_hist, y con ellas en el factor f de SR1 y SR2 y en f_fija de SRF. Valores: Vidrala Σ H13:L13 = 12,418 (0; 0; 254,086; −241,668; 0); Viscofan 16,161.
- Reproducción: un rastreo estático de precedentes de `Análisis!B78:D78` y `C83` con openpyxl (script `traza.py` en los temporales del revisor) alcanza 838 celdas de entrada, de las que 630 no están en la instantánea. Casi todas son rótulos, tablas fijas o ramas de otros motores. Las que importan aquí son `Historia!C13:L13`.
- `cierre_condicionado/Vidrala/verificacion_trazabilidad.txt`: 3 avisos de cero pendiente (C48, C23:L23, C26:L26). La línea de estado del informe enumera 6 causas de «datos de etapa 1 incompletos». Las tres que faltan en la cadena son `Historia!C13:L13`, `C16:L16` y `C17:L17`, porque `trazabilidad_v64.py` (línea 99) solo recorre la relación. De las tres, `C13:L13` («Adquisiciones netas: cero pendiente de verificación», años 2018–2022) es la que entra en el valor.
- La fase C de Vidrala sí lo vio y lo midió (`fase_c.json → revision_datos_ausentes`, entrada `evidencia Historia!C13:L13`: afecta a «D_hist de la configuración (530,0 mm)»; efecto estimado por el agente, menos de 0,5 € en el precio de Sí; no material).

**Consecuencia.**
- No se sostienen tal como están escritas: «instantánea de las 216 entradas económicas» como correspondencia de las variantes (informe integrado, línea 59; README de la V6.4 §9), «0 de 216 entradas económicas distintas» y «Datos: ninguno (216 entradas iguales)» como prueba de que los datos no cambian (líneas 76 y 96), y la cadena «fuente → … → conclusión» con «un dato desconocido nunca se convierte en cero» (línea 61).
- En los hechos de esta entrega no hay diferencia: el revisor comprobó que la fila 13 de Vidrala es igual en el piloto 4.11 y en el cierre nuevo, y que las entradas de la instantánea de Viscofan solo difieren del origen en las 14 celdas de configuración y en `Palancas!B15`.
- Riesgo que queda en el código: un cambio en `Historia!H13:L13` posterior al paso 10 se trataría como editorial. El paso 12 lo detectaría por el vector de la activa cuando la estructura activa usa f o f_fija; no lo detectaría si la activa es S o H, y las variantes SR1, SR2 y SRF quedarían desactualizadas.
- La cadena de trazabilidad de Vidrala no avisa del cero pendiente que sí entra en el cálculo experimental.

### R2 · Importante · El informe integrado dice que los dos expedientes usan precios de noviembre de 2026; el de Vidrala usa el cierre del 31 de diciembre de 2025

**Evidencia.**
- `INFORME_INTEGRACION_4_12.md`, línea 303: «los dos expedientes combinan cuentas de 2025 con precios de noviembre de 2026»; línea 322 (L10): «fechas mixtas (cuentas de 2025, precio de noviembre de 2026)».
- `cierre_condicionado/Vidrala/fase1_metadatos.json → precio`: 90,10 €, fecha 2025-12-31 («La cotización de la acción cerró 2025 en 90,10 euros», cuentas de 2025, PDF p. 97; «no contrastada con el boletín de BME»). `cadena_trazabilidad.md`, línea 5: «precio 2025-12-31». Fecha de análisis: 2026-11-12.
- Viscofan sí usa un precio de noviembre de 2026 (54,70 €, 3-nov-2026).

**Consecuencia.** La descripción de fechas del informe es falsa para Vidrala. El encargo exige separar fechas. Además, «esperar por precio» y «precio de Sí 56,02 € frente a 90,10 €» (línea 13) comparan con un precio de diez meses y medio antes de la fecha de análisis, y el informe no lo dice en ningún sitio donde da la cifra. Los expedientes de Vidrala sí lo declaran («base económica 31-dic-2025»).

### R3 · Importante · «Hipótesis no cubiertas por el ámbito calculado: ninguna» es una afirmación casi vacía, y en Vidrala es incorrecta para la familia de P-M1

**Evidencia.**
- `personaje_v2/scripts/objetivo_v64.py`, líneas 155–167 (`cubiertas`): una hipótesis cuenta como cubierta si cualquier escenario la lista entre sus `parametros_variados`. La variante «heredado» lista todos los parámetros activos (`configuracion_economica.parametros_variados`, línea 248, compara celdas), así que ningún parámetro de la configuración puede salir nunca como no cubierto. Por lo mismo, `material_para_accion = null` («no determinada») no puede darse.
- Vidrala, `PM1.familia` (una de las tres hipótesis que condicionan el objetivo): las cinco variantes de su ámbito (heredado, solo_N1, solo_N2, solo_R1, activa_sin_PM1) quitan el requisito entero; ninguna calcula la familia Θ. La propia fase C lo escribe: «Sin variante que la aísle (Θ no se calcula: θ no observado)» (`fase_c.json → configuracion_v64.parametros[PM1.familia].materialidad`).
- Salidas: `ficha.json → objetivo.hipotesis_no_cubiertas_por_el_ambito = []` en los tres expedientes; `informe.md`, línea 253 (Vidrala, las dos copias) y 242 (Viscofan): «No cubiertas por el ámbito calculado: ninguna». Reproducción: `python3 -B scripts/objetivo_v64.py <copia del expediente>`.
- Caso menor del mismo origen: en Viscofan el ámbito de `PM1.cartera` es `[heredado]`, pero la activa ya tiene cartera «legado», igual que el heredado. La variante figura como si la variara porque la celda pasa de vacía a «Legado»; económicamente no la varía.

**Consecuencia.** Afecta a la afirmación «ámbito exacto» del encargo §4 y a la lectura del rango 51,29–65,72 € de Vidrala: el rango no refleja la alternativa de familia, aunque las salidas digan que ninguna hipótesis condicionante queda sin cubrir. No cambia el tratamiento del objetivo ni la zona. `ambito_aislado_por_parametro` (ficha) sí da el dato correcto (vacío para la familia), pero el informe no lo usa.

### R4 · Importante · En la cadena de trazabilidad de Viscofan, el precio, la capitalización y las acciones llevan fechas y transformaciones que contradicen el valor, y la cadena da «0 avisos»

**Evidencia.** `viscofan/experimental/Viscofan/cadena_trazabilidad.md`, líneas 9–11 (y `cadena_trazabilidad.json`, tres primeras entradas):
- `D-precio`: fuente «cierre del 2026-11-03 (54,70 EUR)», pero período «Cierre 6-oct-2026».
- `D-capitalizacion`: valor 2.487,7 y fuente «54,70 × 45,479209», pero transformación «53,60 × 45,6036 mm acciones … = 2.444,4» y página «IF_1S26».
- `C-acciones`: valor 45,479209 con fuente «media ponderada diluida de 2025», pero criterio «acciones en circulación a 30-jun-2026 = 45,60 mm … No se usa la diluida media FY25 como principal» y «acciones vigentes en la fecha de valoración (no la media del ejercicio)».
- `verificacion_trazabilidad.txt`: «69 entradas · 0 avisos · PASS». La ficha sí lleva el aviso A3 del libro («precio y acciones con fechas separadas más de 90 días»).
- El documento IF_1S26 (semestral de 2026, posterior a la base) no está entre las doce publicaciones conservadas.

Son textos de evidencia heredados del expediente de origen (Control maestro), que no se actualizaron cuando cambió el valor. `trazabilidad_v64.py` los copia y solo comprueba que las fechas no falten.

**Consecuencia.** La lectura del precio del segundo expediente no se puede seguir sin contradicciones hasta su fuente, y el control que debía avisar no avisa. Efecto numérico acotado: usar 45,60 millones de acciones en vez de 45,48 bajaría los valores por acción un 0,27 % (unos 0,1 € en el precio de Sí; cálculo del revisor, no recalculado en el libro). La capitalización combina el precio del 3-nov-2026 con la media diluida de 2025. La afirmación del informe integrado sobre la cadena («fechas separadas y avisos de … fecha», línea 61) es más fuerte que lo que la herramienta comprueba.

### R5 · Importante · El tratamiento del objetivo y la protección de la compra dependen de dos juicios del agente que nada contrasta, y los documentos de la entrega no coinciden sobre qué hipótesis carecen de fundamento

**Evidencia.**
- `objetivo_v64.py`, línea 103: condiciona el objetivo un parámetro con `material_para_objetivo = true` y `fundamento_suficiente = false`. `pipeline.coherencia_v64` (líneas 1284–1425) exige que los dos campos sean booleanos y comprueba el ámbito y la acción, pero no los contrasta con nada: ni con la clase que declara la propia configuración (`configuracion_economica.json → trazabilidad`), ni con los efectos calculados. El prompt lo dice («tu juicio con las cifras; no hay umbral adoptado», `prompts/fase_c_turno1.md`, línea 28). Con «comprar», la exigencia de D10 solo alcanza a los parámetros que el agente marca con `fundamento_suficiente = false`; `prompts/verificacion.md` (punto 11) tampoco pide al auditor revisar los `true`.
- Juicios distintos sobre la misma regla: la configuración clasifica `N3.regla` (R1) como «hipótesis»; la fase C de Vidrala la da por «fundamentada · fundamento suficiente» (efecto aislado −1,36 €) y la de Viscofan por «técnico · sin fundamento» (efecto 0). En Viscofan, `PM1.familia` es «hipótesis · confianza baja» en la configuración y «fundamentada» para la fase C.
- `REVISION_ECONOMICA_VIDRALA_4_12.md`, línea 108: el objetivo «depende de hipótesis sin fundamento suficiente (λ, la estructura, la cartera P0, R1 y los tipos y márgenes normalizados)». El expediente, en cambio, da fundamento suficiente a la cartera, a R1, a N1 y a N2, y solo condicionan el objetivo PM1.estructura, PM1.familia y PM1.parametro. El apartado 7 de esa revisión («coincidencias y diferencias») no recoge esta diferencia.
- `INFORME_INTEGRACION_4_12.md`, línea 50: «Calcula el tratamiento y la decisión que corresponde; la fase C no lo elige».

**Consecuencia.** La frase del informe es cierta solo a medias: el tratamiento es mecánico a partir de dos banderas que elige la fase C. Si un agente marca todo como fundado o como no material, el objetivo sale emitido sin condiciones y una compra queda fuera de D10 sin que ninguna regla lo detecte. En los tres expedientes no cambia nada (acción «esperar», lista de condicionantes razonada), pero la lista de hipótesis que las salidas presentan como condicionantes depende de ese juicio, y dos documentos de la entrega dan listas distintas para Vidrala. Es una laguna no declarada como tal en la tabla de limitaciones.

### R6 · Menor · En Viscofan, θ = 0,5 funciona como central en las salidas aunque se declare «sin central»

**Evidencia.** `viscofan/CONTRASTE_VISCOFAN_4_12.md`, línea 55: «θ = 0,5 solo como punto de cálculo, sin central económica». Con el protocolo «objetivo_condicionado», el expediente emite 39,29 € como precio objetivo (línea de estado, `ficha.decision.precio_objetivo`, `ficha.objetivo.precio_objetivo_emitido` y columna del resumen), que es el valor de θ = 0,5. La fase C lee «θ en el extremo bajo de [0, 1]» (`configuracion_v64.mantenimiento`); con θ = 0 el precio de Sí es 40,35 €.

**Consecuencia.** La cifra emitida es la del punto medio, no la de una lectura fundada. Está marcada como condicionada y provisional, con su rango (38,22–41,81 €), así que la consecuencia es de presentación: ±1,07 € sobre la cifra emitida.

### R7 · Menor · Los avisos de dominio solo se calculan para la variante activa; el README dice que avisan «en una variante calculada»

**Evidencia.** `personaje_v2/scripts/variantes_configuracion_v64.py`, línea 154: `DOM.avisos(… "activa.xlsx", res_act)`. README de la V6.4, línea 268: «`dominios_v64.py` lo avisa cuando ocurre en una variante calculada». El revisor aplicó `dominios_v64.avisos` a los 28 libros de variantes (solo lectura): en Viscofan no hay ningún aviso activo en ninguna, como dice el contraste; en Vidrala, el extremo inferior del rango (λ = 1,25; 51,29 €) lleva f = 1,309, que ninguna salida muestra (solo se muestra f = 1,165 de la activa).

**Consecuencia.** El rango calculado puede incluir variantes fuera de dominio sin aviso. En esta entrega no ocurre con la inversión fija negativa. La frase del README no describe lo que hace el código.

### R8 · Menor · L13 califica de «sesgo pequeño» el efecto de los derechos de uso sin calcularlo

**Evidencia.** `INFORME_INTEGRACION_4_12.md`, línea 325 (L13): «Sesgo pequeño en el requisito». En Viscofan la amortización de derechos de uso suma 27,1 M€ en 2021–2025 frente a un exceso de 40,8 M€ (`analisis_configuracion_viscofan.md`): el exceso sobre la amortización que se repone con capex sería 67,9 M€, un 66 % mayor. Ninguna variante lo calcula.

**Consecuencia.** Estimación lineal del revisor, no recalculada en el libro: con ese exceso, el precio de Sí bajaría unos 0,7 € con θ = 0,5 y unos 1,4 € más con θ = 1, es decir, por debajo del extremo inferior del rango declarado (38,22 €). La zona no cambia. «Pequeño» no está respaldado por una cifra.

### R9 · Menor · Los documentos de la entrega no recogen que en Viscofan la r usada está por debajo de la r mínima de la hoja y es la palanca más influyente

**Evidencia.** `viscofan/experimental/Viscofan/ficha.json → avisos`: A2 («tu r (9,0 %) < r mínima (9,5 %)»), A5 («la palanca más influyente del tornado es la tasa de descuento») y A3 (fechas de precio y acciones separadas más de 90 días). `precio.json → aviso_tasa_descuento_mas_influyente = true`. El informe integrado y el contraste no lo mencionan; L5 habla de «r = 0,09 en Vidrala» y dice que ninguna variante mueve r.

**Consecuencia.** Laguna en la tabla de limitaciones: «la zona no cambia» en Viscofan no cubre la variable que más mueve el valor. Con una r mayor el valor baja, así que «caro» no está en riesgo por este lado.

### R10 · Observación · Las baterías completas no se han ejecutado todavía sobre el código final

**Evidencia.** `REGISTRO_PRUEBAS_4_12.md`: A–G completa, 120/120 a las 21:00–21:14; después solo F (35/35) y G (14/14). `ficha.py`, `informe.py` y `resumen.py` se editaron a las 22:43–22:44 y `pipeline.py` a las 22:49. El grupo E (vigencia en las primeras llamadas de pipeline, ficha, informe y resumen), los grupos A–D y las seis baterías V6.3 no se han repetido desde entonces. El informe integrado (líneas 10 y 244) da como hecho «123 pruebas … en la verificación final sobre una copia limpia».

**Consecuencia.** Esas frases, y «las salidas V6.3 y V6.4 heredadas no cambian», solo quedarán sostenidas si la verificación final pasa. Está anunciado como pendiente; se deja constancia de qué grupos son los que faltan.

### R11 · Observación · Los avisos de las auditorías no son fallos reales

- «15 variantes» (sección 14) frente a «14 escenarios» (rango): son coherentes (15 con la activa, 14 sin ella), pero la sección 14 no lo explica. El informe integrado mezcla las dos cifras igual (líneas 88 y 114).
- Etiqueta «valor calculado condicional» en la línea de estado: con `objetivo_condicionado` la línea da «precio de Sí» y «precio objetivo (condicionado, provisional …)» por separado, sin la etiqueta literal; la ficha, la sección 14 y el resumen sí separan los dos campos. Con `objetivo_bloqueado` la etiqueta está y no hay precio emitido.
- `verificacion_integridad.txt` sobre el libro antes de las cachés: es el diseño de la 4.10; el libro auditado lo acreditan `verificacion_libro_final.txt` y `acreditacion_libro.json`, cuyas huellas el revisor comprobó.

### R12 · Observación · Restos del original en la copia `cierre_bloqueo/Vidrala` que no dan vigencia a nada

- `configuracion_v64_variantes.json` es idéntico byte a byte al del original (variantes reutilizadas) y su campo `configuracion_economica_sha256` es la huella de la configuración del original (`bd092502…`), no la de la copia (`2abd044a…`). El pipeline compara la huella económica, que sí coincide.
- `entrada_v63.json` (material auditado) y los `resultados.json` de las variantes guardan rutas de `cierre_condicionado/`.
- `publicaciones_resumen.json` comparte `registro_id` con el original; sus entradas están reubicadas y apuntan solo al resumen de la copia.
- En `cierre_condicionado/Vidrala/publicaciones_resumen.json` la entrada «publicada» conserva un `retirada_motivo` de la retirada anterior.

Ninguno hace vigente una aprobación del original: la aprobación heredada está en `historial_cierres/01_47e1c83dc70a3d86` con su `RETIRADA.json`, y su huella figura en `auditorias_conocidas.json`.

### R13 · Observación · No queda claro si la fase A de Viscofan recibió la fase A del expediente heredado

**Evidencia.** `viscofan/CONTRASTE_VISCOFAN_4_12.md`, línea 68: «Las fases de juicio recibieron como referencia de solo lectura las del expediente heredado». El registro de avance solo lo dice de las fases B y C. El expediente heredado ya había elegido el motor B.

**Consecuencia.** Si la fase A vio esa elección, «motor B por los hechos» tiene un ancla que el documento no declara. El prompt generado (`prompts_generados/06_fase_a.md`) y `fase_a.md` no citan el heredado, y el razonamiento se apoya en cifras de la Historia y del extracto. El revisor no puede comprobar qué recibió el agente.

### R14 · Observación · «186 celdas contrastadas» aparece en el §9.3 como hecho contrastado con fuentes sin su salvedad

El contraste busca dígitos en la publicación del ejercicio («encontrar los dígitos no prueba que hablen de esa partida», `contraste_cifras_historia.md`). El contraste de Viscofan lo dice; el §9.3 del informe integrado (línea 266) lo lista entre lo «contrastado con fuentes» sin esa salvedad. El recuento (186, 15 y 9) es correcto.

## 3. Lo que se comprobó sin encontrar problemas

**Vigencia y correspondencia de las salidas (punto 1).**
- En los tres expedientes, las 24 huellas de `material_auditoria.json` coinciden con los archivos; `cierre_vigente.json` coincide con `ficha.json`, `informe.md` y `auditoria.md`; cada auditoría responde a su solicitud y a su material (SA-2427fb9cd6e753fe / 5025f54d0c143062; SA-8da4a78afc939a43 / f7a0ba07431707e3; SA-e8c8384c2e565c23 / 0dee970f14c042d4).
- La ficha y el informe oficiales solo difieren de los provisionales auditados en la marca provisional y en el bloque de cierre.
- Las salidas oficiales son posteriores a la última edición del código (pipeline.py 22:49:03; `--desde 13` a las 22:49:52 y 22:49:53; Viscofan, pasos 10–13 a las 22:58–22:59).
- La copia de bloqueo archivó la aprobación del original en su primera llamada (22:04:26) y no reutilizó ninguna: las auditorías anteriores están en `auditorias_conocidas.json` y la no consumida se conserva aparte con su huella (`3eb4908c…`).
- En `pipeline.py`, la vigencia va antes del rechazo de la selección y `SEL.registrar` después; en `informe.py` y `resumen.py` la vigencia va antes de `SEL.resolver`, y en `ficha.py` el rechazo llega después de retirar.

**Objetivo y materialidad (punto 3).** `objetivo_v64.evaluar` sobre las copias reproduce el tratamiento, el estado, la acción, el precio objetivo, el ámbito y el rango de las tres fichas. Con bloqueo no hay precio emitido en ninguna salida. El rango lleva siempre «no es un intervalo de confianza». Ninguna salida presenta nada como adoptado.

**Cifras (puntos 4 y 6).** Coinciden con `precio.json` y con las tablas de variantes todas las cifras comprobadas del informe integrado, de la revisión económica, de la comparación de protocolos y del contraste: valores por escenario, ponderados, precios de Sí, rangos, efectos de S, SR2, SRF, H y sin P-M1, convenciones, N1, N2 y R1, 37,1 % y 30,8 % con su denominador, separación de cambios (−1,724 €; −1,245 € y −2,518 €), pesos del terminal, rentabilidades marginales, salto del requisito y dominios (λ = 2,06, 1,50, 1,1413 y 1,7355; 1 ÷ NWC = 2,071).

**Viscofan (punto 5).** Nada trasladado de Vidrala: las entradas económicas del expediente nuevo difieren del origen solo en las 14 celdas de configuración y en `Palancas!B15`; N1 (22,12 %), el circulante (48,28 %) y las bases salen de cifras propias que el revisor recalculó. N1 tiene perímetro y período; N2 vacío está razonado. Las combinaciones no definidas se declaran. Doce publicaciones con huella; ninguna otra edición se llama «original recuperado» ni lleva el nombre de la fuente de la fase 1. La sección 0 anterior a la fase A está corregida en `volcar_datos_v63.py`.

**Aptitud de uso (puntos 6 y 7).** La ficha, la sección 1 del informe y el resumen dicen «experimental», separada de la auditoría. El informe integrado, la propuesta (sin firmar), la guía y el contraste no atribuyen aptitud general ni permiten decisiones con dinero real. Los archivos de las seis baterías V6.3 son idénticos a los de la 4.11 (en `pruebas/` solo cambian `test_integracion_v64.py` y `agentes_sinteticos.py`).

## 4. Límites de esta revisión

- **No se ejecutó nada que escriba en el árbol ni que recalcule.** Sin pipeline, sin LibreOffice y sin baterías: los resultados de las pruebas, de las réplicas, del control de palancas y de la reproducción del heredado se toman de sus registros.
- **La vigencia no se probó en vivo.** Las copias de los expedientes conservan en `publicaciones_resumen.json` la ruta absoluta del resumen real; una retirada provocada en la copia podía escribir en el árbol, así que no se intentó. Se revisó el código y los registros.
- **Código leído en parte.** Completos: `objetivo_v64.py`, `entradas_economicas.py`, `trazabilidad_v64.py`, `dominios_v64.py`, `seleccion_plantilla.py`, `variantes_configuracion_v64.py`. En parte: `pipeline.py` (función principal, coherencia V6.4 y correspondencia de variantes), `configuracion_economica.py`, `ficha.py`, `informe.py` y `resumen.py`. No leídos: `cierre_v2.py` (salvo las referencias al registro), `comprobacion_conjunta.py` y las baterías de pruebas.
- **Fuentes.** No se abrieron los PDF ni se comprobaron las páginas citadas (61 de 61, 186 celdas): se revisó la coherencia de los inventarios y de los recuentos.
- **Juicios de los agentes.** No se rehicieron las fases A, B y C ni las auditorías; se revisó su coherencia con las reglas y entre expedientes.
- **Documentos leídos por encima.** `GUIA_RECORRIDO_SUPERVISADO.md`, Anexo D §D.13 y `propuesta_humana_4_12.json` (solo búsquedas dirigidas).
- **Estimaciones propias.** Las cifras de R4 y R8 marcadas como cálculo del revisor son aproximaciones, no recálculos del libro.
- **Misma familia de modelos.** El revisor comparte los posibles errores comunes de quienes construyeron y auditaron el trabajo.

## 5. Huellas SHA-256 de los archivos principales revisados

**Documentos de la entrega**

| Archivo | SHA-256 |
|---|---|
| `INFORME_INTEGRACION_4_12.md` (con los marcadores pendientes) | `eb4ab4902aa81670a38807177a4f84218f1c74db047d72253e466d08ab87a53d` |
| `REGISTRO_AVANCE_4_12.md` | `03b1a72dce4ecc10b3a54a26f4f168b484decfdc77644a3077422edb7bded7bc` |
| `REGISTRO_PRUEBAS_4_12.md` | `67a7d634f68ee1dfea4ab20d8208b6980e49b8e9400cb59aa478c426a6562b00` |
| `REVISION_ECONOMICA_VIDRALA_4_12.md` | `0da776c9bbb9449e1f9fbd9db7422bf71d3dc02d0c8c85b807fa2eea049a4286` |
| `COMPARACION_PROTOCOLOS_4_12.md` | `b7e4962eff6f4d04e411c23cfb03b21778aaf691736a7912c3ca77b75bc5b326` |
| `viscofan/CONTRASTE_VISCOFAN_4_12.md` | `b0a0973bfebb2907551b0cfae7ac439c7a795f01e3c86a9f2853ff565c42d259` |
| `propuestas/PROPUESTA_HUMANA_4_12.md` | `2e344485cb17fda1c3f5824a21d6ad5a8fdaf2e6c8d88de55d835a09c16fef48` |
| `viscofan/configuracion/analisis_configuracion_viscofan.md` | `5ea54f1ceee6d3783290e18d69394ce90ea7bbc0479b49dc035abe3e39e23e7e` |
| `viscofan/configuracion/configuracion_economica_viscofan_experimental.json` | `6030330c79abd672cf7db788b632595cf0fbabe6b204924545f5f70c5f1f9abc` |
| `viscofan/fuentes/inventario_fuentes_viscofan.md` | `9ad3954ab9fa490f5428700c7fc3dabacf7b308914e1efef08a44f6f94aa225b` |
| `revision_interna/ENCARGO_REVISION_INTERNA_4_12.md` | `8afa4790fc3385b35619c1bd08cb561d6f36f82e6eee956ca0df982c197ac5b6` |
| `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` | `435c12e3fb55a434576c89d683d34a9db072e568a3829a1de4b4cd24f13b6db3` |
| `personaje_v2/ANEXO_D_salidas_y_formatos.md` | `28128cf0679f4cae1271bda61984f526e59a9ef3c8a76cc38458e7db0cb7ffd3` |
| `v6/v64_experimental/docs/README_V6.4_experimental.md` | `8d4283ccd39be2e246824ec0a78e8cbd56c3c766261da495f9cc43a2f3f504d1` |

**Expedientes**

| Archivo | `cierre_condicionado/Vidrala` | `cierre_bloqueo/Vidrala` | `viscofan/experimental/Viscofan` |
|---|---|---|---|
| `ficha.json` | `a353182ef9e1cd48…` | `adba528556de44ec…` | `fd951b2528a3a1b3…` |
| `informe.md` | `199bf44d66c8fbbd…` | `d9ae363c42d66d60…` | `5a7b7a1512dd1b76…` |
| `auditoria.md` | `833ee26a0958751d…` | `ca140080e3d5f223…` | `5cc5ba1fc61c203b…` |
| `fase_c.json` | `4332ba9b3b2e1939…` | `91a6f0d4cda6dd56…` | `5986b127f2637d1d…` |
| `material_auditoria.json` | `dff6a7c563680b8e…` | `b40b75e67acffc90…` | `0b96feb4f92d417e…` |
| `configuracion_economica.json` | `bd092502a40cf27b…` | `2abd044a21b9863d…` | `73a9f23dc963b36a…` |
| `configuracion_v64_variantes.json` | `dab33cb4fbccb143…` | `dab33cb4fbccb143…` | `55d9dbb2c7faf112…` |
| `cadena_trazabilidad.json` | `02a01eb93c021dc7…` | `e49429dbc5ba3545…` | `0a30a4fda0fe70a5…` |
| `precio.json` | `ff1438f5cdf48ee4…` | `ff1438f5cdf48ee4…` | `46446a661f0c6d4b…` |
| libro evaluado (`*_v63_evaluada.xlsx`) | `0f87bdc9c2817a49…` | `0a6e41800078f1f5…` | `33cf616b3ac6d571…` |
| `resumen_v2_v64_experimental.csv` (junto al expediente) | `d9ca1e03b373c262…` | `2f8a3ba14aa962ba…` | `70d5d7dc12367a65…` |

Las huellas completas de `ficha.json`, `informe.md` y `auditoria.md` son las que registra el `cierre_vigente.json` de cada expediente, que el revisor comprobó contra los archivos.

**Código y prompts (`personaje_v2/`)**

| Archivo | SHA-256 |
|---|---|
| `scripts/pipeline.py` | `5b082b064b38c755dc04025bb9c8c628f6e03845a9583d7f0d7264e7f8e221df` |
| `scripts/cierre_v2.py` | `5d5a252ec2e85ff870aa94bdee8bc20fbb9443be94d110233edce022482ccaa7` |
| `scripts/seleccion_plantilla.py` | `5e5968eb230810caa70d6e71ec0748f261f1fc2fdd92061271856a0c174daa42` |
| `scripts/ficha.py` | `d269982e9692d92d99fa59988b11ee330c3a082298d6ce1a67a25c108c35b84e` |
| `scripts/informe.py` | `7d180262c999f7ddadd53c0ab6ba6caffddf13660818b54e7ebcb58bebaf9426` |
| `scripts/resumen.py` | `c3057e5025fda7d4e5e001ce4e6e15b78345fc80d4fbe89cc80c8163df5a5dd5` |
| `scripts/objetivo_v64.py` | `40d240b21a6e881f637341c57b174a00f49be529619cfa3147663d0a3bd432b7` |
| `scripts/trazabilidad_v64.py` | `9c97c639aec39747b114fe5153a59829696ed1ecd9becd5a20edf0abbc67fd5c` |
| `scripts/entradas_economicas.py` | `f2f0ea239b2e79920d03cbe80cc1d3b0d216f358b111c7013c708632088b95e2` |
| `scripts/dominios_v64.py` | `cc561771bc9bc05fd190a525fc9daa54c0a8c2604b2314386142ea7bf49de942` |
| `scripts/comprobacion_conjunta.py` | `32163155a9d7d3048ea525ef8839d5c4214d93915906d269c18955491b3760e8` |
| `scripts/configuracion_economica.py` | `bd7871ccad8120d59a78473d0581d674563714b54be26703f45da77d895c998b` |
| `scripts/variantes_configuracion_v64.py` | `34ff146d0fbc6126ed04cdc4eb2d0fbb9c3b1f638796cea464c28fae035fa0d5` |
| `scripts/volcar_datos_v63.py` | `b84772757ba742e3ca06eceb7c76bd840f92eb7774f6fd7eccf2919a842739a9` |
| `prompts/verificacion.md` | `d9ea1d3f967ef017abbed940b619f1346fd498d78c9798ddc7f96570d9c4222c` |
| `prompts/fase_c_turno1.md` | `46913d53f12e29b137cc3069a996717d8cd14016be0b1a7ce46ca0f85f21a0be` |
