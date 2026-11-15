# N4 · Ceros pendientes de Vidrala (entrega 4.9)

**Qué es.** Es la investigación documental de los ceros que el expediente de referencia (`…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/`) tiene pendientes de verificación. Las prioridades son `Historia!L26` (minoritarios de 2025) y `Análisis!C48` (intereses pagados en financiación).

**Qué no es.**
- **No es una confirmación.** La IA no confirma ceros ni escribe `fase1_decisiones.json`: el pipeline sigue tratando las 38 entradas como pendientes, y en el libro siguen como «Dato no verificable».
- **No es un porcentaje de fiabilidad para invertir.**
- **No cambia la referencia.** El libro de referencia, las decisiones registradas y los criterios no cambian. `fase1_decisiones.json` conserva P1 y las decisiones y la regla preexistentes de deuda y arrendamientos; ninguna de las 38 entradas está registrada.

Base económica sin cambios: 31-dic-2025, motor B, r = 0,09, probabilidades 0,2/0,6/0,2, k = 3, caja 108,352, puente 160,784, 35,206 millones de acciones.

**Cómo se reproduce todo** (desde `munger_v2_r1/`, en este orden, con `S` una carpeta temporal vacía; `S=$(mktemp -d); mkdir $S/efectos`):
1. `python3 -I -B …/2026-11_Vidrala_ensayo_4_9/scripts/efectos_n4.py --salida $S/efectos`, que usa LibreOffice: no ejecutar en paralelo con otras pruebas;
2. `python3 -I -B …/scripts/n4_investigacion.py --salida $S --propuestas $S/prop`;
3. `python3 -I -B …/scripts/test_n4_comprobaciones.py`.

Sin `--salida`, los dos primeros **sobrescriben** las salidas entregadas. Estas son `n4/matriz_n4.json` y `.csv`, `n4/recuento_n4.json`, `n4/efectos/` y `propuestas/propuestas_n4_sin_firmar.json`. `comprobar_entrega_4_9.py` hace esta misma reproducción en temporales y compara con lo entregado.

## 1. Recuento real

**[Hecho] Son 38**, que es la cifra de `fase1_v63.json` → `pendientes_verificacion` y coincide con la del encargo.

| Partida | Fila de la Historia | Años pendientes | Entradas |
|---|---|---|---|
| Adquisiciones netas | 13 | 2018–2022 | 5 |
| Intereses pagados en financiación | 16 | 2016–2025 | 10 |
| Principal de arrendamientos | 17 | 2016 y 2018 | 2 |
| Pasivo por arrendamientos | 23 | 2016 | 1 |
| Minoritarios | 26 | 2016–2025 | 10 |
| Otros activos financieros corrientes | ninguna (auxiliar de la caja) | 2016–2025 | 10 |
| **Total** | | | **38** (28 con fila y 10 auxiliares) |

**Diferencias con otros recuentos, explicadas:**
- `ceros_heredados_H1.csv` tiene **39** entradas de Vidrala. La de más es la de `adquisiciones` en `AR_2023.json`, cuyo motivo es la columna 2022 («impreso '-'»). No se usa en la Historia: el CSV dice «no (lo sustituye el comparativo del informe siguiente)», y el valor de 2022 sale de `AR_2022.json`, que sí está entre las 38.
- La partida auxiliar `otros_activos_financieros` solo contaría en la caja si `fase1_metadatos.json` lo declarara, y declara `caja_incluye_otros_activos_financieros = false`. Por eso esas 10 entradas no tienen celda ni efecto en el modelo.
- `Análisis!C48` no es un cero propio: es la **media 2023–2025** de `intereses_financiacion`, que escribe la fase 1 (`fase1_historia.DEP_ANALISIS`), y hereda el estado de esos tres años.

## 2. Método (automatizado y reproducible)

Para cada entrada, `n4_investigacion.py` reconstruye la cadena **celda → `fase1_v63.json` y `AR_<año>.json` → `texto/CF_<año>.txt` → página del PDF oficial**, con la huella del PDF. No basta con que la cita exista: se comprueba que está en su página y, sobre todo, se **contrasta con la partida mediante un cuadre completo** del bloque del estado que contendría el dato, en las dos columnas:

| Partida | Cuadre que acredita el cero |
|---|---|
| Minoritarios | patrimonio atribuido a la dominante + total pasivo = total patrimonio neto y pasivo, **y** resultado del ejercicio = resultado atribuido a la dominante |
| Intereses en financiación | bloque de financiación: suma de líneas = total impreso, sin ninguna línea de intereses; y la línea de intereses pagados dentro de explotación |
| Adquisiciones | bloque de inversión: suma = total, sin importe del año en la línea de adquisiciones. Una línea con un solo importe se asigna a la columna con la que cuadran **las dos** columnas, y solo si esa asignación es única |
| Principal de arrendamientos | bloque de financiación sin línea de arrendamientos, más la norma aplicable (NIC 17 o NIIF 16) |
| Pasivo por arrendamientos | pasivos no corrientes y corrientes = sus subtotales, sin pasivo por arrendamientos, más la norma aplicable |
| Otros activos financieros | activo corriente = subtotal, sin inversiones financieras corrientes ni depósitos |

**Más comprobaciones:**
- **Unidad y moneda:** miles de euros en el estado, millones en la Historia.
- **Signo.**
- **Período y comparativa:** la columna comparativa del informe siguiente cuadra igual.
- **Perímetro:** Italia, como discontinuada en 2024, no afecta a estas partidas.
- **Prioridad documental:**
  - 2024 y 2025 se repiten en la **versión española**, que prevalece, y en el **ESEF 2025** oficial, que es en español.
  - De 2017 a 2022 solo se conserva la traducción inglesa: es una limitación declarada. 2023 se contrasta con la columna comparativa del informe español de 2024.
  - El texto de 2016 ya está en español.

**Condiciones generales de la clasificación** (`aplicar_condiciones_generales`; añadidas tras la auditoría interna, Z-4). Una entrada solo puede quedar en la clase 2 o en la 4 si se cumplen todas:
- la cita está en su página;
- la columna comparativa no contradice;
- la unidad (miles de euros) consta en el estado;
- **ningún rótulo del bloque queda sin reconocer.** La clasificación es **por exclusión**: cada línea con rótulo del bloque tiene que estar en una lista blanca de rótulos conocidos para esa partida. Una línea con otro rótulo («Finance costs paid», «Business combinations», «Short-term investments»…) no se interpreta: baja la entrada a la clase 3;
- **ninguna excepción de estructura** (añadidas tras el control de vigencia, V-4): una línea solo con importes y sin rótulo dentro del bloque que no sea el total impreso aparte, un segundo bloque con el mismo inicio en la página (por ejemplo, actividades interrumpidas) o un desglose «of which / de los cuales» en la página. La unidad se busca en la **cabecera** del estado (el texto anterior al bloque), no en toda la página, y una cabecera con «millions of euros» o «millones de euros» la contradice (otras formas, como «€ millions», no se reconocen). En el balance, una mención de intereses minoritarios en la página con alguno de los rótulos reconocidos («non-controlling», «minorit…», «participaciones no dominantes», «socios externos», «outside shareholders/interests») impide el cuadre. Las mismas excepciones se aplican al contraste con la versión española, que prevalece;
- una línea ilegible solo se tolera en la **columna comparativa**. En la del año, la entrada no se acepta aunque la suma cuadre.

Si falla alguna, la entrada pasa a la clase 3 con el motivo. Las clases 4 tampoco están fijadas: dependen de la norma por fecha (NIIF 16 desde 2019), de la ausencia de la línea en el bloque y, en 2018, de la nota de deuda y de la regla de `fase1_decisiones.json`. **En los datos reales, ningún rótulo queda sin reconocer y ninguna condición falla**, así que no cambia ninguna clase.

**Lo que la clasificación no examina** (límite declarado): el significado de los rótulos de la lista blanca más allá de su texto (un rótulo conocido que escondiera otro concepto en la memoria) y otras formas de desglose, unidad o rótulo que las probadas. El segundo control de vigencia (W-5) encontró once engaños sintéticos más que pasan: «thereof», «including», un espacio no separable o un homoglifo en el rótulo, un segundo bloque con otra cabecera, «€ millions», un rótulo de adquisición partido en dos líneas y minoritarios rotulados «other shareholders» o «intereses de terceros». **Ninguno aparece en los textos reales de Vidrala 2016–2025**, y no se han convertido en pruebas: quedan como requisito previo de cualquier activación de la propuesta de automatización. Por eso una clase 2 es una evidencia documental, no una confirmación, y la propuesta de automatización exige más pruebas antes de activarse.

`scripts/test_n4_comprobaciones.py` (**19 pruebas**) demuestra que las comprobaciones **rechazan**, con estados sintéticos (identificados como tales):
- una línea de intereses dentro de financiación;
- un bloque que no cuadra;
- un importe ilegible en la columna del año, aunque no descuadre la suma (en la comparativa se tolera y se declara);
- un interés no dominante;
- un resultado atribuido distinto;
- una adquisición en la columna del año;
- un depósito corriente;
- una cita fuera de su página;
- los 14 rótulos alternativos con los que la auditoría interna obtuvo falsos positivos: tres para intereses en financiación, cinco para adquisiciones y seis para activos financieros corrientes;
- los seis engaños estructurales del control de vigencia: intereses o una adquisición en una línea sin rótulo, un «of which» después del total, un segundo bloque de financiación, un estado en millones con «thousands of euros» en una nota y minoritarios incluidos en «Total liabilities»;
- cada condición general, por separado.

También comprueba que los casos reales favorables (L26 y C48 de 2025, y la errata comparativa de 2023) lo siguen siendo.

## 3. Resultado por partida

Clases (encargo §4.2): 1 cero publicado · 2 cero derivado por conciliación completa · 3 dato no publicado o evidencia insuficiente · 4 concepto no aplicable · 5 valor discrepante.

| Partida | Años | Clase | Resumen documental |
|---|---|---|---|
| Minoritarios (L26 y resto) | 2016–2025 | **2** (10) | Ningún balance tiene participaciones no dominantes, y los cuadres del balance y de la cuenta de resultados son completos en las dos columnas. En 2023, la comparativa del informe español de 2024 cuadra igual, pero con cifras reexpresadas (total pasivo 1.284.595 frente a 1.257.579 del texto inglés; el patrimonio atribuido coincide), y la explicación de la matriz lo dice. 2025: 1.412.878 + 901.354 = 2.314.232, y 209.341 = 209.341 (igual en el PDF español, p. 10–11; en el ESEF, `ProfitLoss` = `ProfitLossAttributableToOwnersOfParent` y no hay ningún hecho de intereses no dominantes). Las menciones a «non-controlling» o «minority» de la memoria se revisaron una a una y se describen con su contexto real de cada año: son de política contable (fondo de comercio) o de participaciones que el grupo **adquiere** en otras sociedades (Vidroporto, Envasados Eva y Glassco). En 2025, además, la tabla de sociedades dependientes de las cuentas consolidadas da todas las dependientes al 100 %; Envasados Eva (45 %) y Glassco (20 %) se integran por puesta en equivalencia |
| Intereses en financiación | 2016–2017 | **2** (2) | Los intereses pagados están en explotación; financiación cuadra sin línea de intereses |
| Intereses en financiación (C48 = 2023–2025) | 2018–2025 | **2 con reserva** (8) | Intereses de deudas: clase 2. Están en explotación (2025: «Interest paid (20.800)» / «Pagos de intereses (20.800)»; en el ESEF, solo `InterestPaidClassifiedAsOperatingActivities`, 20.800 y 32.100). Financiación cuadra sin intereses (2025: 2.626 + 219.500 − 1.294 − 125.259 − 227.266 − 51.833 = −183.526, también en español). **Reserva:** no consta en qué línea del estado de flujos están los intereses de arrendamientos (2018, NIC 17; desde 2019, NIIF 16): es una clase 3 en ese componente (§4). 2023: el comparativo 2022 del texto tiene la errata «112,5000»; el año 2023 cuadra y la errata se declara. 2023 también se contrasta con la columna comparativa del informe español de 2024 (financiación 69.826, sin intereses; «Pagos de intereses (12.320)») |
| Adquisiciones | 2018–2022 | **2** (5) | El bloque de inversión cuadra en las dos columnas sin importe de adquisición del año. 2018: la única línea, «Acquisition of a subsidiary … (235.233)», solo cuadra como comparativo de 2017. **Aviso:** en el texto inglés los rótulos de ese bloque están desplazados respecto de los importes; el cuadre no depende de los rótulos |
| Principal de arrendamientos | 2016 | **4** | Antes de la NIIF 16. Solo arrendamientos operativos (nota 3 f), cuyo pago está en el CFO. Concepto no aplicable |
| Principal de arrendamientos | 2018 | **4** | Antes de la NIIF 16. Hay un arrendamiento financiero de NIC 17 (nota 15, p. 57: «Finance Lease» 40.916 no corriente y «-» corriente, nacido en 2018). La **regla registrada** en `fase1_decisiones.json` («Arrendamientos = solo pasivos NIIF 16. Los arrendamientos financieros que no son NIIF 16 (leasing de maquinaria de dic-2018 …) van en deuda») lo lleva a la deuda (decisión registrada deuda 2018 = 433,767), así que su principal es de la deuda, no de la fila 17. Decisión escrita en el archivo, sin fecha ni firma: principal 2017 = 0 «antes de NIIF 16». Concepto no aplicable bajo esa regla |
| Pasivo por arrendamientos | 2016 | **4** | Antes de la NIIF 16. Los pasivos cuadran sin arrendamientos y no hay arrendamientos financieros. Concepto no aplicable |
| Otros activos financieros | 2016–2025 | **2** (10) | El activo corriente cuadra sin inversiones financieras corrientes ni depósitos (2025: 712.559; 2024 y 2025 también en la versión española, y 2023 en la comparativa del informe español de 2024, con el total reexpresado: 816.395 frente a 821.341). La partida no entra en el modelo |

**Cobertura de las 38** (documental, no confirmación ni fiabilidad):
- **investigadas:** 38;
- **respaldadas (clase 2):** 35, de ellas **8 con reserva** (componente de arrendamientos de los intereses 2018–2025);
- **no aplicables (clase 4):** 3 (arrendamientos NIIF 16 de 2016, principal y pasivo, y principal de 2018), con decisiones para 2017–2018 escritas en `fase1_decisiones.json`, aunque sin fecha ni firma (§7);
- **sin evidencia suficiente (clase 3):** 0 en la entrada completa (la reserva de los 8 intereses es una clase 3 en un componente: §4);
- **discrepantes (clase 5):** 0;
- **cero publicado explícitamente (clase 1):** ninguno. En todos los casos el informe no imprime el cero: se deduce del cuadre.

## 4. C48: devengo, pago y clasificación

- **Gasto financiero devengado.** «Finance costs», por ejemplo 31.001 en 2025. No es un pago ni entra en C48.
- **Intereses efectivamente pagados.** En 2023–2025, 12.320, 32.100 y 20.800 (media 21,74 mm). Están dentro del CFO (Análisis!C46 = 335,4 ya los descuenta).
- **Clasificación.** Explotación (estado de flujos inglés y español; ESEF). La parte en financiación de los intereses de deudas es 0.
- **Que se paguen intereses no obliga a que C48 sea positivo.** C48 solo debe recoger intereses pagados que el CFO no haya descontado. El contraejemplo calculado lo muestra: poner C48 = 21,74 resta dos veces los mismos intereses (FCF base 161,2 → 139,46), mueve `f` de −2,76 % a −1,31 % y convierte el aviso «⚠ REVISAR» del control de rango de `f` en un **«✓ PASA» falso**. No es una alternativa.
- **Arrendamientos (componente separado).** Los pagos de arrendamientos (nota 8: 5.861, 6.117 y 8.314) incluyen intereses (devengados 2.131, 2.179 y 2.452). **Aviso documental:** esas mismas tres cifras aparecen, idénticas, como «Expenses related to short-term leases…» en la misma nota (CF_2025.txt, l. 2937). Es la discrepancia que ya registró la 4.2, y no está resuelta. No consta en qué línea del estado de flujos están (4.2, `INFORME_2023_Y_ARRENDAMIENTOS.md`: «No consta»). Lo que conviene a C48 depende de la decisión pendiente sobre C49 (P3):
  - **Si C49 recoge el pago total** (6,764, el valor de `fase1_v63.json`), los intereses de arrendamientos ya se restan ahí: **C48 tiene que seguir en 0**, porque sumarlos sería un doble cómputo.
  - **Si C49 = 4,5** (principal estimado, el valor del libro) y esos intereses se pagaran dentro de financiación, faltaría restar unos 2,254 mm. Es una **hipótesis**, no una cota: FCF base 158,95 y `f` −2,61 %.
  - **Si se pagan dentro de «Interest paid»**, como sugiere la NIIF 16.50 b) con la política de la empresa (inferencia normativa, no dato publicado), ya están en el CFO y C48 = 0.

## 5. Dependencias y efecto material (copias identificadas, recálculo forzado)

El grafo de fórmulas (`scripts/dependencias_v63.py`) muestra que **todas** las entradas alcanzan formalmente las salidas, a través de la regla de tipos de Historia C5:L26 (`Motor!E234`), que actúa como puerta del estado técnico. Esa es una dependencia **formal**. La **numérica** se mide recalculando con LibreOffice copias identificadas con +1 mm (`scripts/efectos_n4.py`; el recálculo de la base reproduce exactamente 53,670 / 70,772 / 86,489, el ponderado 70,495 y el puente 160,784). Todas las cifras de esta sección y de la §4 están en `n4/efectos/efectos_n4.json`: los tres escenarios y el ponderado, el FCF base (Análisis!C52), `f` (Diagnóstico V6!C12), el texto del control de rango de `f` (Diagnóstico V6!C50) y el precio de Sí, que se calcula con `precio_de_si.p_estrella` (k = 3) sobre los tres valores recalculados:

| Grupo | Efecto por +1 mm | ¿Material para la valoración? |
|---|---|---|
| **L26** (minoritarios 2025) | Puente +1. MALO, NORMAL, BUENO, ponderado y **precio de Sí: −0,0284 € por acción** (= 1/35,206) | **Sí, por unidad.** Con el valor documentado (0), el efecto es **nulo** |
| C26:K26 (minoritarios 2016–2024) | ninguno | No |
| **C48** | FCF base −1; `f`, su control de rango, precio/FCF y el disparador de quiebra de `referencias_mecanicas.py` | **No** para la valoración del motor B (B78:D78 y C83 no cambian). Sí para el diagnóstico de `f` |
| Fila 16 (2016–2025, sin tocar C48) | ninguno | No: C48 es un valor escrito por la fase 1, no una fórmula |
| E13:I13, C17 y E17, C23 | ninguno | No |

## 6. Carencias y decisiones pendientes

**Carencias documentales:**
1. **Intereses de arrendamientos.** No se publica su línea en el estado de flujos. Hace falta consultarlo (Vidrala) o resolverlo como convención en P3. No se ha enviado ninguna consulta (encargo §10).
2. **2017–2022 solo en inglés.** No se conservan las versiones españolas, que prevalecen. Los cuadres se hicieron en la traducción oficial. 2023 se contrasta con la columna comparativa del informe español de 2024.
3. **Nota 8 de 2025.** Las cifras de pagos de arrendamientos coinciden con las de gastos de arrendamientos a corto plazo (§4). Discrepancia documental ya registrada en la 4.2, sin resolver.

**Decisiones de la persona responsable** (en `propuestas/propuestas_n4_sin_firmar.json`, agrupadas por partida y clase, sin firmar):
- **Clase 2 (35 entradas en 4 grupos):** registrar o no los ceros con la fuente del cuadre, en `fase1_decisiones.json`, con valor, fuente con página, fecha y persona.
- **Clase 4 (3 entradas):** extender a 2016 (principal y pasivo) y al principal de 2018 la representación como 0 que ya escriben en `fase1_decisiones.json` las decisiones de 2017–2018 y la regla «Arrendamientos = solo pasivos NIIF 16», o dejarlas vacías (= desconocido). Esas decisiones no tienen fecha ni firma: si la persona responsable quiere apoyarse en ellas, conviene que las confirme también.
- **P3 (C49), ligada a la reserva de C48:** qué recoge C49.

## 7. Decisiones preexistentes en `fase1_decisiones.json` (contexto)

`fase1_decisiones.json` de la referencia contiene, además de P1 (circulante 2024, firmado), una regla y decisiones anteriores **sin fecha ni firma** en el archivo. `DECISIONES.md` (3-nov-2026, «Segunda empresa real: Vidrala») las recoge entre los trabajos de la sesión de construcción de la fase 1, sin atribuirlas a la persona responsable; no consta quién las tomó:
- la regla «Arrendamientos = solo pasivos NIIF 16»;
- deuda 2018–2022;
- arrendamientos 2017–2022;
- principal de arrendamientos 2017.

Ninguna corresponde a las 38 entradas. Explican que en 2018 el arrendamiento financiero (40.916) esté en la deuda (E22 = 433,767) y E23 = 0: no hay doble cómputo. La 4.9 no las cambia ni las valora.
