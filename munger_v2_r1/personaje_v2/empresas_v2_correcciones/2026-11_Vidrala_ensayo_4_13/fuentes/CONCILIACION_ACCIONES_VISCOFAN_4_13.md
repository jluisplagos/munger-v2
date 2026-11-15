# Viscofan · conciliación del número de acciones (encargo 4.13 §6)

**Qué es.** Este documento concilia las cifras de acciones de Viscofan en sus definiciones, fechas, unidades y operaciones de capital. Usa la publicación conservada en el paquete y dos fuentes oficiales consultadas el 13-nov-2026.

No elige ninguna cifra. Las alternativas se comparan en `resultados/alternativas_acciones_viscofan.md`. El expediente sigue con la cifra que usaba (45,479209 millones) hasta que la persona responsable decida otra cosa (propuesta, decisión VISCOFAN-ACCIONES).

Todo lo que sigue son hechos comprobados en las fuentes citadas, salvo lo marcado como interpretación.

## 1. Fuentes

| Fuente | Qué es | Conservación |
|---|---|---|
| `viscofan/fuentes/pdf/AR_2025.pdf` (SHA-256 `e997bc7d07392b5d50226a9ad18839897c9e705c46a81d8acbc51174f638b83c`) | Informe anual consolidado 2025 (inglés), 470 páginas | En el paquete (4.12) |
| BORME-C-2026-738 (12-mar-2026) | Convocatoria de la junta ordinaria de 2026 (punto quinto: reducción por amortización de 500.000 acciones propias) | Consulta textual: https://boe.es/borme/dias/2026/03/12/pdfs/BORME-C-2026-738.pdf |
| BORME-C-2026-1603 (28-abr-2026) | Anuncio de la reducción de capital ejecutada | Consulta textual: https://boe.es/borme/dias/2026/04/28/pdfs/BORME-C-2026-1603.pdf |
| BORME-C-2026-3155 (2-jun-2026) | Aumento liberado (Viscofan Retribución Flexible) con reducción simultánea por amortización de acciones propias | Consulta textual: https://www.boe.es/borme/dias/2026/06/02/pdfs/BORME-C-2026-3155.pdf |
| CNMV, informe financiero del primer semestre de 2026 (registro del 29-jul-2026), anexo | Estados intermedios consolidados a 30-jun-2026 | Consulta textual: https://www.cnmv.es/portal/aldia/detalleifialdia.aspx?nreg=2026107196 |

**Conservación.** La consola no llega a boe.es ni a cnmv.es, así que esos PDF se leyeron con la herramienta de consulta web y no se conservan sus bytes. Quedan los localizadores y las cifras literales. Si la persona responsable deja los PDF en la carpeta conectada, se pueden conservar con su huella, como los informes anuales en la 4.12.

## 2. Lo que dice cada fuente

**AR 2025, nota 20 (página PDF 119, impresa 99).**

| | 2025 | 2024 |
|---|---|---|
| 20.1 Básico · media ponderada de acciones en circulación | 45.656.226 | 45.548.368 |
| = acciones medias (46.500.000) + efecto de la autocartera | −843.774 | −951.632 |
| Numerador: beneficio atribuido de las operaciones continuadas (miles €) | 159.917 | 157.019 |
| BPA básico (€) | 3,50 | 3,45 |
| 20.2 Diluido · «Weighted average number of ordinary shares outstanding» | 45.479.209 | 45.699.511 |
| Mismo numerador (miles €) | 159.917 | 157.019 |
| BPA diluido (€; la línea lleva por error la etiqueta «Basic») | 3,52 | 3,44 |

Comprobación aritmética: 159.917 ÷ 45.656,226 = 3,5026 → 3,50; 159.917 ÷ 45.479,209 = 3,5163 → 3,52; 157.019 ÷ 45.548,368 = 3,4473 → 3,45; 157.019 ÷ 45.699,511 = 3,4359 → 3,44.

**La contradicción.** La nota 20.2 dice que el diluido «incorpora el efecto del plan de acciones del grupo» (nota 22.3), que añade acciones potenciales.
- En 2024 lo cumple: el diluido supera al básico en 151.143 acciones.
- En 2025 el diluido queda 177.017 acciones POR DEBAJO del básico, con el mismo numerador, y su BPA (3,52) supera al básico (3,50). Con la definición que da la propia nota, eso no es posible.
- La nota no lo explica, y no se ha encontrado otra edición de la nota 20 de 2025: el informe semestral de 2026 no trae el BPA.

**Interpretación:** es una errata o un cálculo con otra base, y no se puede resolver con las fuentes disponibles.

**AR 2025, capital y autocartera.**
- Página PDF 76, impresa 56: 46.500.000 acciones de 0,70 € a 31-dic-2025.
- Nota 12.4, página PDF 83, impresa 63: 506.601 acciones propias a 31-dic-2025 (1,09 % de los votos).
- El movimiento de 2025 cuadra exactamente: 690.795 al inicio + 1.599.709 compradas − 12.351 y 145.318 entregadas (planes) − 795.636 y − 898.098 entregadas en los dividendos flexibles + 33.432 y 34.068 recibidas = 506.601.
- En circulación a 31-dic-2025: 46.500.000 − 506.601 = **45.993.399**.

**AR 2025, nota 22.3.** Plan de incentivos 2025–2027: hasta 315.000 acciones (objetivo) o 472.500 (máximo), que se entregarán en el primer semestre de 2028. Es dilución potencial; la nota no dice si se entregarán de la autocartera o con acciones nuevas.

**BORME y CNMV (2026).**
- **Reducción de 500.000 acciones propias.** Son las compradas en el programa de recompra del 25-nov-2025 al 24-feb-2026. La aprobó la junta del 24-abr-2026 y quedó inscrita el 11-may-2026: el capital pasa a 32.200.000 € y **46.000.000 acciones**.
- **Junio de 2026.** Aumento liberado de 1.001.717 acciones nuevas con amortización simultánea de 1.001.717 acciones propias, «para evitar la dilución». Las acciones emitidas siguen siendo 46.000.000.
- **Autocartera a 30-jun-2026:** 396.357 acciones (0,86 % de los votos). En circulación a esa fecha: 46.000.000 − 396.357 = **45.603.643**.
- **3-nov-2026 (fecha del precio):** no hay cifra oficial de autocartera. Entre junio y noviembre puede haber compras o entregas.

## 3. Conceptos que no deben mezclarse

| Concepto | Cifra (millones) | Fecha o período | Uso propio |
|---|---|---|---|
| Media ponderada básica (denominador del BPA) | 45,656226 | promedio de 2025 | resultado por acción de 2025 |
| Media ponderada «diluida» publicada (contradictoria) | 45,479209 | promedio de 2025 | la que usa el modelo desde la fase 1 del pipeline V2 (no la eligió la etapa 1; ver el antecedente bajo esta tabla) |
| Acciones en circulación (emitidas − autocartera) | 45,993399 | 31-dic-2025, fecha de las cuentas | valor por acción a la fecha de las cuentas |
| Acciones en circulación | 45,603643 | 30-jun-2026, última cifra oficial antes del precio | valor por acción cerca de la fecha del precio |
| Dilución potencial del plan 2025–2027 | hasta 0,315 (objetivo) o 0,4725 (máximo) | entrega en 2028 | ajuste por dilución, si se adopta una política |

**Antecedente de la etapa 1 (corrección de la revisión interna R7).** La etapa 1 no usó 45,479209. Su libro evaluado (`viscofan/Viscofan/etapa1/Viscofan_evaluada.xlsx`) tiene Análisis!C55 = 45,6, C37 = 53,6 y C41 = 2.444,4. Su evidencia, conservada en el registro de la fase 1 (`evidencias_sustituidas`) y en el libro base (Control maestro, fila de C55), dice: «Acciones en circulación netas de autocartera a 30-jun-2026 = 45,60 mm (base actual, coherente con C41). No se usa la diluida media FY25 como principal por la anomalía NIC 33». La media «diluida» la introdujo la fase 1 del pipeline V2 (`fase1_metadatos.json`, `acciones_diluidas`), en lugar de una cifra que la etapa 1 había elegido de forma expresa y que había descartado la diluida por la misma anomalía. Es un hecho pertinente para la decisión VISCOFAN-ACCIONES; no decide nada por sí solo.

**Interpretación:**
- Para un valor por acción comparable con un precio, lo coherente es el número de acciones con derecho al valor en la fecha del precio, más la dilución potencial que se decida contar. Un promedio del año sirve para el BPA, no para dividir un valor.
- Ninguna cifra disponible corresponde al 3-nov-2026. Las candidatas mezclan fechas: las cuentas son de 2025 y el precio, de noviembre de 2026.

## 4. Qué se hace y qué no

- **No se sustituye N automáticamente.** El expediente sigue con 45,479209, ahora descrito con su concepto real: la media «diluida» publicada de 2025, contradictoria con su propia definición.
- **Se comparan las alternativas identificadas**, calculadas sobre copias del libro evaluado con LibreOffice, con E fijo y con E = 54,70 × N: `resultados/alternativas_acciones_viscofan.md`. Son sensibilidades de definición con fechas mezcladas, no correcciones ni valoraciones actualizadas.
- **Se corrige la evidencia activa** que contradecía las entradas (§6 del encargo):
  - la vía generativa: `rellenar_fase1_v63.py` sustituye entera la evidencia de las cifras frescas y guarda la anterior en el registro de la fase 1;
  - las entradas del expediente nuevo: `fase1_v63.json` y `fase1_metadatos.json` describen el concepto, el período y las otras cifras;
  - el resultado en el libro, celda a celda frente al de la 4.12: tabla de `viscofan/resultados/reutilizacion_4_12.md`.
- **Elección pendiente:** VISCOFAN-ACCIONES en la propuesta, con firmas vacías.
