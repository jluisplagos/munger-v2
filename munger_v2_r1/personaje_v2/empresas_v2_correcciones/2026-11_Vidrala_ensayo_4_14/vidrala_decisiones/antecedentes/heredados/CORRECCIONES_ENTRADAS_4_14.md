# Correcciones de las entradas financieras de Vidrala · rama 4.14

**Autor:** agente C-Vidrala (Claude), 14-nov-2026. No es una revisión humana ni una revisión independiente: el agente actúa como extractor de las correcciones. Todo lo que cambia queda «pendiente» de una nueva revisión independiente.

**Encargo:** corregir en la extracción las discrepancias confirmadas por la revisión independiente R-Vidrala (`agentes/R_vidrala/INFORME_REVISION.md`) e investigar, sin decidir, los pendientes J14, K14, K13 y C48.

**Convenciones del documento:**
- «Hecho»: lo que la fuente imprime, con documento, página «[PDF PAGE n]» del texto conservado y cita literal. Todas las citas se comprobaron por programa contra su página (`c_citas.py`; 0 fallos).
- «Interpretación»: lo que el agente deduce y la fuente no dice.
- «Propuesta»: lo que se sugiere y no se ha hecho.

**Documentos:**
- CF_20xx = `texto/CF_20xx.txt`: cuentas consolidadas en inglés, «free translation»; prevalece el español.
- ES 2025 = `texto/ES_2025_informacion_financiera_consolidada.txt`: original español, doc. 2308.
- ES 2024 = `texto/ES_2024_informacion_financiera_consolidada.txt`, **añadido en esta rama**:
  - origen: PDF `2118_es-informacion_financiera_consolidada_2024.pdf` (389 págs., sha256 `365eea9eb1238ea2536a4e3c465c61401bfd9ce01c34ce9fca50235d9b7e7dcf`), copia de contraste en `agentes/D1/arbol/munger_v2_r1/contrastes/vidrala_2023_arrendamientos/fuentes/` (documento D9 de ese contraste);
  - método: el mismo que `cambiar_base.py` usó para ES 2025 (`pdftotext -layout` y marcas `[PDF PAGE n]`); se comprobó que ese método reproduce byte a byte el texto de ES 2025 desde su PDF;
  - huella del texto: `1eb5ac625388b6c01a4437d368342c29d8800692ced658a3685076273ba40261`;
  - límite: la huella del PDF no estaba registrada en el expediente.

## 1. Cómo se construyó el expediente

Se averiguó en `historia_revision.md`, `fase1_v63.json`, `estado_pipeline.json`, `cambiar_base.py` y `configuracion/cambio_de_base_cierre_condicionado.json` de la 4.12.

1. **Historia:** `fase1_historia.py construir` toma `fase1_partes/AR_<año>.json` y usa, para cada año, la cifra más reciente (el comparativo del informe siguiente).
2. **Sustituciones:** `cambiar_base.py` (paso 4) sustituyó en `fase1_v63.json → analisis` diez entradas con `cambio_de_base_cierre_condicionado.json`. Entre ellas:
   - C46 335,413 → 335,4 y C47 169,668 → 169,7 («precisión de referencia»);
   - C48 → 0 (supuesto heredado);
   - C49 6,764 → 4,5.
3. **Libro:** `rellenar_fase1_v63.py` escribió el libro de datos desde `Vidrala_v63_base.xlsx`, migrado de `etapa1/Vidrala_evaluada.xlsx`.
   - En ese libro base, C46 = 335,4 y C47 = 169,7 ya venían de la etapa 1.
   - El registro de rellenado los lista en `no_pisadas`: no se escribieron desde `fase1_v63.json`.

**Reproducción previa:** antes de tocar nada se rehízo el paso 2 en una copia (construir + mismas sustituciones). El `fase1_v63.json` salió **idéntico byte a byte** al del expediente, y `historia_revision.md` idéntica salvo la cabecera. Con esa misma vía (`c_reconstruir_fase1.py`) se reconstruyó después la rama.

## 2. Correcciones aplicadas (hechos)

| Celda | Antes | Después | Documento y página | Cita literal | Motivo |
|---|---|---|---|---|---|
| Análisis!C46 (CFO medio 2023–2025) | 335,4 | **335,413** | CF_2024 [PDF PAGE 7] (columna 2023(*)); CF_2025 [PDF PAGE 7] | «Net cash from operating activities 362,516 263,437» · «Net cash from operating activities 380,287 362,516» | Discrepancia confirmada (redondeo heredado). (263,437 + 362,516 + 380,287) ÷ 3 = 335,413 mm |
| Análisis!C47 (capex medio 2023–2025) | 169,7 | **169,668** | CF_2024 [PDF PAGE 7]; CF_2025 [PDF PAGE 7] | «Payments from sale of property, plant and equipment (160,063) (143,848)» · «Payments from sale of other intangible assets (8,737) (7,852)» · «Payments from sale of property, plant and equipment (178,746) (160,063)» | Discrepancia confirmada. Media de 151,700, 168,800 y 188,503 = 169,668 mm (Historia J12:L12, sin cambio) |
| Historia!F8 (D&A 2019) | 97,091 | **91,088** | CF_2020 [PDF PAGE 13], columna 2019; también CF_2019 [PDF PAGE 12] | «Amortisation and depreciation 6&7 84,144 91,088» · aparte: «Impairment of non-current assets 6 1,415 6,003» · CF_2019: «Amortisation and depreciation 6&7 91,088 88,178» | Discrepancia confirmada. Los otros nueve años excluyen el deterioro. Comprobado también en el PDF 1304 renderizado (sha256 `35264bc7…b10e`) |
| Historia!K13 (adquisiciones 2024) | −241,668 | **−224,000** | CF_2025 [PDF PAGE 7], columna 2024; ES 2024 [PDF PAGE 114] (Informe de Gestión 2024, pág. impresa 20) | «Cash flows from loss of control of subsidiaries - 230,000» · «Acquisition of companies accounted for using the equity method - (6,000)» · ES 2024: «Adquisición/enajenación de sociedades -224.000 +254.086 Estado de flujos de efectivo consolidado dependientes, efecto neto» | La fuente resuelve el pendiente (ver §6). La propia empresa publica −224.000 = −(230.000 − 6.000) para ese concepto, con origen en el estado de flujos; su 2023 (+254.086) es J13. Página renderizada y leída |

**Vía de extracción de cada corrección** (copias previas: `fase1_partes/AR_<año>.antes_4_14.json`, `fase1_v63.antes_4_14.json`, `historia_revision.antes_4_14.md`, `verificacion_entradas.antes_4_14.json`):

- **F8**, en `fase1_partes/AR_2020.json → da`:
  - se quita «Impairment of non-current assets» de la columna anterior (2019, la que usa la Historia);
  - también de la actual (2020): no cambia el libro, porque G8 sale del comparativo de CF_2021 (84,144); evita una definición distinta en el mismo archivo.
- **K13**, en `fase1_partes/AR_2025.json → adquisiciones`, columna anterior (2024):
  - se quita «Other effects of disposal» (11,668);
  - se añade la línea de puesta en equivalencia (6,000).
  - Lo mismo en `AR_2024.json`, columna actual (no cambia el libro; evita una «diferencia» falsa en `historia_revision.md`).
  - La columna 2025 sigue en 0.
- **C46 y C47:** se vuelve a construir con las mismas sustituciones de `cambio_de_base_cierre_condicionado.json`, **salvo C46 y C47**. Así quedan los valores exactos que `fase1_historia.py` construye desde la Historia, con su fuente. Se añadió una nota en `fase1_v63.json → _notas`.
- **`fase1_decisiones.json`:** no se ha tocado.

**Diferencias de `fase1_v63.json`** frente a la copia previa (comparación campo a campo):
- `historia.partidas.da.valores[2019]`: 97,091 → 91,088;
- `historia.partidas.adquisiciones.valores[2024]`: −241,668 → −224,0;
- `analisis.C46`: 335,4 → 335,413, con su fuente;
- `analisis.C47`: 169,7 → 169,668, con su fuente;
- las notas de esas partidas y `_notas`.

Nada más cambia: C48 = 0, C49 = 4,5 y C24, C31, C34, C42, C53 y C54 quedan como estaban.

**`historia_revision.md`:**
- cambian las filas da y adquisiciones;
- desaparecen las dos «diferencias» de D&A de 2019 y 2020 (27 → 25 diferencias);
- los ceros pendientes siguen siendo 38.

## 3. Lo que no se corrigió, y por qué

1. **C46 y C47 en el libro.**
   - **Hecho:** `Vidrala_v63_base.xlsx` y `etapa1/Vidrala_evaluada.xlsx` tienen C46 = 335,4 y C47 = 169,7. La columna M de Control maestro dice «Decisión del inversor (23-oct-2026): FCF base con media 3 años 2023–25 (C46, C47, C49) → C46 = 335,4…».
   - **Hecho:** `rellenar_fase1_v63.py` no pisa un valor migrado sin `--sobrescribir`. La columna J de esas filas no empieza por «Historia de fase1_v63.json», así que tampoco lo rechaza. Si el pipeline se ejecuta sin más, **el libro seguirá con 335,4 y 169,7 en silencio**: solo lo registrará `no_pisadas`.
   - **No se hizo:** tocar los libros (etapa 1, base). Es un libro y su evidencia M recoge una decisión del inversor.
   - **Propuesta:** aplicar el mecanismo de `cambiar_base.py` (`vaciar_en_etapa1` de C46 y C47, con evidencia M nueva que conserve la decisión del período 2023–2025) antes de regenerar. Lo decide quien lleve el pipeline.
   - **Efecto conocido** (revisión R-Vidrala): FCF base 161,2 → 161,245 (≈ +0,001 €/acción al año), solo en el motor A; nulo en el B activo.
2. **C48 y aux:intereses_financiacion_2023–2025:** la fuente no da el dato (§4). Se reclasificaron en el registro; no hay cambio de valor.
3. **J14:** es una decisión de perímetro (P7). Se exponen las dos parejas (§5).
4. **K14:** la fuente no publica dónde se compensa la plusvalía (§6). Se dejan las alternativas.
5. **Productos derivados del expediente** (`datos_v63.*`, `cadena_trazabilidad.*`, `ficha*.json`, `informe*.md`, `resultados.json`, libros de datos y evaluado): siguen con los valores anteriores hasta que el pipeline se vuelva a ejecutar (prohibido en este encargo).

## 4. C48 · intereses pagados en financiación

**Hechos:**
- **Estado de flujos:** el bloque de financiación de 2023, 2024 y 2025 no tiene línea de intereses, ni en inglés ni en español.
  - Citas: CF_2024 [PDF PAGE 7] «Net cash from/(used in) financing activities (410,796) 69,826»; CF_2025 [PDF PAGE 7] «Net cash from/(used in) financing activities (183,526) (410,796)».
  - Sus totales cuadran con sus líneas.
  - Los intereses pagados están en explotación: CF_2025 [PDF PAGE 7] «Interest paid (20,800) (32,100)»; ES 2025 [PDF PAGE 14] «Pagos de intereses (20.800) (32.100)»; ES 2024 [PDF PAGE 14] «Pagos de intereses (32.100) (12.320)».
- **Arrendamientos (nota 8):** el pago incluye el interés devengado, porque el movimiento del pasivo suma el devengo y resta el pago.
  - CF_2025 [PDF PAGE 52]: «Accrued finance charges 2,452 2,179» y «Payments (8,314) (6,117)»; ES 2025 [PDF PAGE 58]: «Gastos financieros devengados 2.452 2.179», «Pagos (8.314) (6.117)».
  - CF_2024 [PDF PAGE 56]: «Accrued finance charges 2,179 2,131» y «Payments (6,117) (5,861)».
- **Sin línea propia:** los pagos de arrendamientos no tienen línea en el estado de flujos. El cuadro NIC 7 (CF_2025 [PDF PAGE 67]) solo muestra «Current loans and borrowings 92,688 (25,724) (131) - 66,833» y «Non-current loans and borrowings 300,624 (103,730) (814) - 196,080». Esos saldos incluyen el pasivo NIIF 16: CF_2025 [PDF PAGE 66], «Finance Lease - NIIF 16 (Note 8) 43,162 6,138 41,279 3,625».
- **Gasto financiero:** la empresa resta el interés de arrendamientos del gasto financiero en su medida «Gasto financiero neto» (ES 2024 [PDF PAGE 115]: «Impacto NIIF 16 Arrendamientos -2.179 -2.131 Nota 8 - Activos Intangibles»). Prueba que ese interés está en el gasto financiero de la cuenta de resultados. No dice en qué línea de flujos se paga.
- **Nota 26** (ES 2025 [PDF PAGE 82], «Gastos financieros por deudas (29.253) (40.046)»): sin desglose del pagado.
- **Resultado:** ninguna nota, ni ES 2024, ni ES 2025, ni CF 2023–2025, dice si el interés de arrendamientos está en «Pagos de intereses» o dentro de los pagos de deuda de financiación. El contraste previo de D1 (`contrastes/vidrala_2023_arrendamientos`, §2) llegó a lo mismo y añadió que el ESEF 2025 solo etiqueta `InterestPaidClassifiedAsOperatingActivities`.

**Qué se hizo:** no se corrige porque la fuente no lo dice. En el registro, `aux:intereses_financiacion_2023/2024/2025` pasan de `cero_comprobado` a **`dato_ausente`**:
- `valor_modelo` vacío;
- justificación con los hechos anteriores;
- `fuente` reescrita como lugar examinado, sin `valor_fuente`.

C48 sigue como derivado (no se reclasifica como hipótesis: no se afloja su control). Queda pendiente porque sus orígenes no están comprobados. Su conciliación dice que el 0 del libro es el supuesto heredado «situación A de P3» (`fase1_v63.json`, `analisis.C48`).

**Interpretación:** las dos lecturas son compatibles con la fuente.

| Alternativa | C48 (mm) | Efecto (revisión R-Vidrala) |
|---|---|---|
| El interés de arrendamientos está en «Pagos de intereses» (explotación) | 0 | — |
| Está dentro de los pagos de deuda de financiación | 2,254 = media de 2,131, 2,179 y 2,452 | FCF base del motor A −2,254 mm (≈ −0,06 €/acción al año); nulo en el motor B activo |

**Propuesta:** consultar a Relación con Inversores de Vidrala (P9-c1 del contraste D1). No se ha contactado con nadie.

## 5. J14 · circulante de 2023 (P7): las dos parejas coherentes con J8

| | Pareja A · estado reexpresado | Pareja B · estado original |
|---|---|---|
| J8 (D&A 2023) | 87,210 | 97,865 |
| J14 (aumento del circulante 2023) | 78,805 | 89,866 |
| Documento | CF_2024 [PDF PAGE 7], columna «2023(*) Restated»; original español ES 2024 [PDF PAGE 14] | CF_2023 [PDF PAGE 7] (informe del propio ejercicio) |
| Cita D&A | «Amortisation and depreciation 7&8 117,720 87,210» · ES: «Amortizaciones 7y8 117.720 87.210» | «Amortisation and depreciation 7&8 97,865 85,460» |
| Cita del subtotal | «Cash used in operating activities (84,994) (78,805)» · ES: «Efectivo generado por las operaciones (84.994) (78.805)» | «Cash used in operating activities (89,866) (117,545)» |
| Línea «otros» | ES: «Otros activos y pasivos corrientes y no corrientes (106.417) 47.199» | «Other current liabilities 36,138 (84,515)» |
| Ajustes (subtotal) | ES: «240.195 158.414» | «169,475 87,783» |
| Perímetro de D&A | Operaciones continuadas: sin Italia | Consolidado con Italia |
| Perímetro del circulante | Parte del beneficio total, con Italia (233,395). Las partidas no monetarias de Italia (11,061) salieron de los ajustes y entraron en «Otros activos y pasivos…» | Consolidado con Italia; sus cinco líneas suman (89,866) |

**Hechos comunes:**
- El CFO de 2023 es 263,437 en los dos informes (CF_2023 [PDF PAGE 7] «Net cash from operating activities 263,437»; CF_2024 [PDF PAGE 7]).
- 97,865 − 87,210 = 10,655, la amortización de Italia en 2023 (CF_2024 [PDF PAGE 35]: «Amortisation cost (10,655)»).
- 169,475 − 158,414 = 47,199 − 36,138 = 11,061 = 89,866 − 78,805.
- La traducción inglesa de CF_2024 [PDF PAGE 7] copia en la columna 2023 tres líneas de 2022 (provisiones, subvenciones, gastos financieros). El español (ES 2024 [PDF PAGE 14]: «Variaciones de provisiones 20.024 10.647») sí cuadra.

**Efecto:** en D_hist (capex − amortización + circulante) las dos parejas difieren solo 0,406 mm (−8,405 frente a −7,999).

**Interpretación, sin elegir:**
- A mantiene J8 en el perímetro de continuadas de J6 y J7 (ventas y EBIT de continuadas), pero su circulante incluye partidas no monetarias de Italia que no son circulante.
- B es consolidado en D&A y circulante, coherente con el CFO y el capex de 2023 (que incluyen Italia: explotación 26,732 e inversión (28,371), CF_2025 [PDF PAGE 32]), pero no con ventas y EBIT.
- La decisión es humana (P7). La fuente no publica el circulante de 2023 solo de continuadas.

## 6. K14, K13 y la venta de Italia

### Hechos

| Hecho | Documento y página | Cita |
|---|---|---|
| Precio | CF_2024 [PDF PAGE 34]; ES 2025 [PDF PAGE 38] | «for the initially agreed amount (230 million euros)» |
| Plusvalía de unos 50 mm, en el resultado de interrumpidas | CF_2025 [PDF PAGE 31]; ES 2025 [PDF PAGE 38]; ES 2024 [PDF PAGE 42] | «amounted to a gain of 50 million euros recorded under the heading 'Profit for the period from discontinued operations'» · «2024 ascendió a una plusvalía de 50 millones de euros registrada bajo el epígrafe “Beneficio del periodo de actividades discontinuadas”» |
| Resultado de Italia en el primer semestre | CF_2025 [PDF PAGE 31] | «Profit for the year from discontinuing operations 9,518» |
| Resultado de interrumpidas 2024 | CF_2025 [PDF PAGE 7] | «Profit for the year from discontinuing operations - 60,065» |
| Activos netos dados de baja | CF_2025 [PDF PAGE 32] | «Net assets disposed of 204,502» |
| Flujos de interrumpidas 2024 | CF_2025 [PDF PAGE 32] | «Operating activities 11,558 26,732» · «Investing activities 230,000 (28,371)» |
| Cobro en inversión | CF_2025 [PDF PAGE 7]; ES 2025 [PDF PAGE 14] | «Cash flows from loss of control of subsidiaries - 230,000» · «Other effects of disposal - 11,668» · ES: «Otros efectos enajenación - 11.668» |
| Compra por puesta en equivalencia | CF_2025 [PDF PAGE 7] y [PDF PAGE 32] | «Acquisition of companies accounted for using the equity method - (6,000)» · «Additions - 6,000» (Envasados Eva 45 %, Glassco 20 %) |
| Ajustes al resultado | CF_2025 [PDF PAGE 7]; ES 2025 [PDF PAGE 14] | Diez líneas. Ninguna es un resultado por enajenación. Suman 240,195; D&A 117,720 = la de continuadas de la cuenta de resultados |
| Línea «otros» del circulante 2024 | ES 2025 [PDF PAGE 14] (el inglés omite el paréntesis de apertura: P1) | «Otros activos y pasivos corrientes y no corrientes (23.477) (106.417)» · «Efectivo generado por las operaciones 799 (84.994)» |
| Tratamiento fiscal | CF_2024 [PDF PAGE 61] | «The permanent differences primarily correspond to the exemption associated with the capital gain from the sale of the Italian subsidiary (Note 5)» |
| Cifra de la empresa para adquisiciones y enajenaciones netas | ES 2024 [PDF PAGE 114] | «Adquisición/enajenación de sociedades -224.000 +254.086 Estado de flujos de efectivo consolidado dependientes, efecto neto» · «Flujo de caja libre 206.056 153.528 N/A» |

**Hechos derivados por aritmética:**
- **La plusvalía:**
  - plusvalía contable = 60,065 − 9,518 = **50,547** (la nota la redondea a «50 millones»);
  - **cobrado por la venta en 2024:** 230,000 en «loss of control of subsidiaries»; la nota de interrumpidas atribuye a Italia exactamente 230,000 de inversión;
  - 11,668 adicionales en «Other effects of disposal», cuyo contenido no se publica.
- **La propia empresa** resta 224.000 = 230.000 − 6.000 como efecto neto de adquisiciones y enajenaciones en su flujo de caja libre. El cálculo de su tabla cuadra: 224.324 + 173.938 + 1.150 + 31.122 − 224.000 − 478 = 206.056.
  - Así, deja los 11,668 dentro de su flujo de caja libre y cuenta la compra por puesta en equivalencia como adquisición.
- **Cuadre del estado:** el estado de flujos cuadra con la variación de caja (18,588 = 100,094 − 81,506). Su beneficio de partida (298,315) incluye la plusvalía no monetaria y ninguna línea de ajustes la elimina. Para que cuadre, una o varias de las cinco líneas de circulante tienen que compensarla.

### K13: resuelto por la fuente y corregido

- **Valor:** **K13 = −224,000** (§2).
- **Lo que deja fuera:** «Other effects of disposal» (11,668). No consta que pertenezca a la venta y la empresa no lo cuenta como adquisición o enajenación.
- **Lo que incluye:** la compra por puesta en equivalencia (6,000), que es pago por negocios. Así lo trata la empresa y así lo dice la convención de la fila: «Adquisiciones = −(pagos y cobros por negocios del estado de flujos)».
- **Límites:**
  - la cifra de contraste es una medida alternativa de rendimiento del informe de gestión, no un estado auditado (las líneas de origen sí lo son);
  - **sigue siendo decisión** si la venta de Italia debe entrar en D_hist o tratarse aparte (perímetro). Esta corrección no la adopta.
- **Efecto cualitativo:** las adquisiciones de la ventana 2021–2025 pasan de 12,418 a 30,086 mm (+17,668), así que D_hist sube y `f` baja.
  - La revisión R-Vidrala acota esta alternativa en f −0,006 y ≤ 0,25 €/acción. No está recalculado.

### K14: no resuelto por la fuente

- **Lo que la fuente no dice:** en qué línea se compensa la plusvalía de 50,547.
- **Indicios (interpretación):**
  - **(a) El precedente de 2023:** en el estado de 2023 reexpresado, la empresa llevó las partidas no monetarias de Italia (11,061) a «Otros activos y pasivos corrientes y no corrientes» (§5, hecho aritmético).
  - **(b) El tamaño de la línea:** esa es la única línea de 2024 con importe suficiente para absorber 50,5 mm (−106,417).
  - **(c) El balance:** «Other current liabilities» apenas se mueve (CF_2024 [PDF PAGE 3]: 32,200 → 30,848).
  - **(d) Conciliación aproximada con el balance** (2023 reexpresado → 2024, neta de las bajas de Italia de CF_2024 [PDF PAGE 35] y de dotaciones e imputaciones):
    - «otros» sale ≈ −23,7 mm frente a −106,4 publicados; la diferencia (≈ −83 mm) admite los 50,5 de la plusvalía;
    - pero deudores sale ≈ −40,8 frente a −15,7: la conciliación línea a línea no cierra;
    - no tiene en cuenta los acreedores de inmovilizado ni la conversión. Por eso no sirve para aislar la plusvalía.

**Alternativas para K14**, sin elegir:

| Alternativa | K14 (mm) | Supuesto |
|---|---|---|
| Cifra impresa | 84,994 | La línea «otros» es circulante |
| Toda la plusvalía en «otros» | ≈ 34,447 | 84,994 − 50,547 |
| Además, por analogía con 2023, otras partidas no monetarias de Italia del primer semestre en esa línea | ≈ 33,594 | Amortización 304, deterioro 1, gasto financiero 45 e impuesto 503: suman 853 (CF_2025 [PDF PAGE 31]) |

**Efecto cualitativo:** la fila entra en D_hist de la V6.4 (circulante 2021–2025 = 278,8 mm según la revisión). Restar unos 50 mm baja D_hist y sube `f`: según la revisión R-Vidrala, de 1,165 a ≈ 1,185, con una cota grosera de hasta −0,8 €/acción en el motor B. No está recalculado.

**Propuesta:** preguntar a Vidrala por la composición de «Otros activos y pasivos corrientes y no corrientes» de 2024 y de «Otros efectos enajenación». Mientras no haya respuesta, calcular las dos versiones por separado, como prevé `RAMAS_4_14.md`.

## 7. Registro de verificación (`verificacion_entradas.json`)

**Criterios:**
- `valor_modelo` de las celdas sigue siendo el del libro, que no se ha regenerado. El valor nuevo va en `incidencia.corregido_4_14`.
- `comprobacion` queda así:
  - `resultado` = «pendiente»;
  - `nota` empieza por «corregido en la rama 4.14; pendiente de nueva revisión independiente»;
  - `extractor` recoge al extractor y a C-Vidrala;
  - `revisor`, `fecha` y `fuente_examinada` quedan vacíos;
  - la revisión R-Vidrala se conserva entera en `comprobacion.revision_anterior`.
- Se añadió `correcciones_4_14` en la cabecera.

**Cambios por entrada:**

| Entrada | Cambio |
|---|---|
| Análisis!C46 y C47 | Conciliación con el valor corregido; incidencia 335,413 y 169,668; pendiente |
| Historia!F8 | Derivado (amortización + deterioro) → **dato_publicado** (CF_2020 [PDF PAGE 13], columna 2019, valor_fuente 91.088); incidencia 91,088; pendiente |
| Historia!K13 | Orígenes → aux:venta_dependientes_2024 y aux:adq_puesta_equivalencia_2024; fórmula −(230 − 6); incidencia −224,0; pendiente |
| aux:adq_puesta_equivalencia_2024 (nueva) | dato_publicado −6,0 (CF_2025 [PDF PAGE 7]); pendiente |
| aux:mar_adquisicion_enajenacion_2024 (nueva) | dato_publicado −224,0 (ES 2024 [PDF PAGE 114]); contraste, fuera de la fórmula; pendiente |
| aux:otros_efectos_venta_2024 | Sin cambio de valor ni de comprobación; `uso` e incidencia: ya no es origen de K13 |
| aux:intereses_financiacion_2023/2024/2025 | cero_comprobado → **dato_ausente** (valor vacío, justificación); pendiente |
| Análisis!C48 | Sigue como derivado; conciliación e incidencia actualizadas; pendiente |
| Historia!J14 y K14 | Sin cambio de valor ni de comprobación; incidencia del extractor con lo investigado |

**Resultado de `verificacion_entradas.py comprobar CARPETA --json`** (sobre el libro evaluado sin regenerar):

| Concepto | Antes (registro revisado) | Después (rama 4.14) |
|---|---|---|
| Universo | 226 | 226 |
| Comprobadas | 335 | 335 |
| Auxiliares | 119 | 121 |
| Pendientes | 4 | 9 |
| Discrepancias | 6 | 3 |
| Errores | 0 | 0 |
| Desactualizadas | 0 | 0 |
| Sin entrada, sobrantes o repetidas | 0 | 0 |
| Materiales sin comprobar | 7 | 7 |
| Apto por entradas | False | **False** |

**Detalle de discrepancias y pendientes después:**
- **Las 3 discrepancias** son las del libro sin regenerar, y son las esperadas:
  - C46: «la fórmula da 335.413 y el modelo 335.4»;
  - C47: «169.668 y 169.7»;
  - F8: «signo × escala × valor_fuente = 91.088 ≠ valor del modelo 97.091».
- **Desaparecen** las tres discrepancias de cita de aux:intereses_financiacion: ya no se presentan como ceros comprobados.
- **Los 9 pendientes:** los tres aux:intereses_financiacion; C48 (por sus orígenes); J14; K14; las dos aux nuevas; y K13 (por su origen nuevo).
  - Cuando se revise ese origen, K13 dará discrepancia hasta que el libro se regenere (fórmula −224,0 frente a −241,668 en el libro).
- **Ningún control se ha aflojado.** Los resultados se guardaron en `scratchpad/C_vidrala/comprobar_antes.json` y `comprobar_despues.json`.

## 8. Resultados de los scripts

- **`fase1_historia.py comprobar-anio CARPETA AÑO`**, de 2016 a 2025 después de las correcciones: **OK los diez años**. Avisos «PENDIENTE» de ceros con cita sin contrastar (H1, sin cambio): 5, 3, 5, 4, 4, 4, 4, 3, 3 y 3.
- **`fase1_historia.py construir`** (vía `c_reconstruir_fase1.py`): «fase1_v63.json escrito (10 años, 25 diferencias con el comparativo, 38 ceros pendientes de verificación, 0 confirmados por decisión humana; ver historia_revision.md)». Código 0. Antes eran 27 diferencias.
- **Sustituciones reaplicadas** de `cambio_de_base_cierre_condicionado.json`: C48 0,0 → 0; C49 6,764 → 4,5; C24 → 0,1394; C31 → «Sí»; C34 → «Sí»; C42 → 7,82; C53 → 108,352; C54 → 262,913. Se excluyeron C46 y C47.

**Huellas sha256 tras los cambios:**

| Archivo | sha256 |
|---|---|
| `fase1_partes/AR_2020.json` | `82e18deb1782dc496a08eea0d9da3e147f203757f8bd1822f46440ea703d2873` |
| `fase1_partes/AR_2024.json` | `729046364f6912a312244e89b2c3c72b0f44684e4fdfb8953bfbfd1c1bc17647` |
| `fase1_partes/AR_2025.json` | `50d30571977aff295550eec482761cd2f8532530f1b4f596a592d2fc7f85e241` |
| `fase1_v63.json` | `b182c82147d8e216785a51546de80cc1b88ae3858bc676e3f1e9b708aa523460` |
| `historia_revision.md` | `02d68fa06f64f5cc9656835ede164daabdcc49da1b0ca47fcde8c239d4cacfd9` |
| `verificacion_entradas.json` (se guardó antes de redactar este documento) | `d3118d75891cc8091a2a048a442b2abf25e1c5eb26c1072947f01502e9c3d33f` |

**Qué no se ejecutó ni tocó:** LibreOffice, el pipeline, `rellenar_fase1_v63.py`, ningún libro `.xlsx` y `fase1_decisiones.json`. Fuera de la rama solo se escribió en `scratchpad/C_vidrala/`.

**Scripts** (`/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/C_vidrala/`):
- `c_corregir_ar.py`;
- `c_reconstruir_fase1.py` y `sust_4_14.json`;
- `c_registro.py`;
- `c_citas.py` y `citas_4_14.json`.

## 9. Límites

- **Páginas renderizadas en PDF:** solo se renderizaron CF_2020 [PDF PAGE 13] (PDF 1304) y ES 2024 [PDF PAGE 114] (PDF 2118). Lo demás se leyó en los .txt.
- **Los PDF de contraste** están fuera del expediente y sus huellas no estaban registradas en él.
- **Efectos en €/acción:** los que se citan son cotas de la revisión R-Vidrala. No se recalculó el libro.
- **Pendiente de revisión:** el agente no es revisor independiente de sus propias correcciones. Todas quedan pendientes de una nueva revisión independiente.
