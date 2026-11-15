# Viscofan · reutilización de la extracción y de las fases A y B de la 4.12 (encargo 4.13 §9)

**Resultado: REUTILIZABLES.**

## Prompts generados (normalizada la ruta del expediente)

- `05_extraccion_v63.md`: igual salvo la ruta del expediente
- `06_fase_a.md`: igual salvo la ruta del expediente
- `08_fase_b.md`: igual salvo la ruta del expediente

## Libro de datos (salida de la fase 1) frente al de la 4.12, celda a celda

- Fecha de análisis: 2 celdas · evidencia de las celdas frescas (Control maestro G:N): 27 · «Configuración V6.4» (perímetro de la V6.4.1): 44 · etiquetas de versión de la plantilla: 7 · **otras: 0**

| Celda | Celda fresca | 4.12 | 4.13 |
|---|---|---|---|
| Control maestro!G38 | Análisis!C37 | Cierre 6-oct-2026 | cierre del 2026-11-03 |
| Control maestro!G41 | Análisis!C41 | 2026-11-03 | precio del 3-nov-2026 × acciones medias de 2025 |
| Control maestro!G52 | Análisis!C55 | 2025-12-31 | media ponderada del ejercicio 2025 (publicada como diluida) |
| Control maestro!G54 | Análisis!C57 | 7-oct-2026 | None |
| Control maestro!H41 | Análisis!C41 | mm | millones de EUR |
| Control maestro!H52 | Análisis!C55 | mm | millones de acciones |
| Control maestro!H54 | Análisis!C57 | % | None |
| Control maestro!I38 | Análisis!C37 | Mercado (secundaria: Bolsamanía, MarketScreener) | None |
| Control maestro!I41 | Análisis!C41 | Cálculo interno (precio de mercado × acciones de estados intermedios) | None |
| Control maestro!I52 | Análisis!C55 | Estados intermedios / cuentas anuales | None |
| Control maestro!I54 | Análisis!C57 | Mercado (secundaria) | None |
| Control maestro!J41 | Análisis!C41 | Precio 54,70 EUR x 45,479209 millones de acciones diluidas | Precio 54,70 EUR (cierre del 3-nov-2026) × 45,479209 millones (media ponderada «diluida» de 2025): fechas mezcladas, precio de 2026 y acciones medias de 2025 |
| Control maestro!J52 | Análisis!C55 | AR_2025, nota 20.2 Beneficio por acción diluido (nº medio ponderado de acciones en circulación, diluido) | AR_2025, nota 20.2: media ponderada «diluida» de acciones en circulación de 2025, la publicada (45,479209 millones). Contradice su propia definición: queda por  |
| Control maestro!K38 | Análisis!C37 | https://www.marketscreener.com/ | None |
| Control maestro!K41 | Análisis!C41 | Documento adjunto por el inversor | None |
| Control maestro!K52 | Análisis!C55 | Documento adjunto por el inversor | None |
| Control maestro!K54 | Análisis!C57 | https://tradingeconomics.com/germany/government-bond-yield | None |
| Control maestro!L38 | Análisis!C37 | — | None |
| Control maestro!L41 | Análisis!C41 | IF_1S26 (capital y autocartera) | None |
| Control maestro!L54 | Análisis!C57 | — | None |
| Control maestro!M38 | Análisis!C37 | Último cierre del mercado principal, en EUR (moneda de los flujos). Dos fuentes coinciden. | None |
| Control maestro!M41 | Análisis!C41 | 53,60 × 45,6036 mm acciones (46.000.000 emitidas − 396.357 autocartera, restada una sola vez) = 2.444,4. Una sola clase. | None |
| Control maestro!M52 | Análisis!C55 | Acciones en circulación netas de autocartera a 30-jun-2026 = 45,60 mm (base actual, coherente con C41). No se usa la diluida media FY25 como principal por la an | None |
| Control maestro!M54 | Análisis!C57 | Bund alemán 10 años (flujos en EUR) = 3,48%. Referencia; la r es decisión del inversor. | None |
| Control maestro!N41 | Análisis!C41 | Recompras jul–oct-2026 no verificadas: −0,5% a −1,5% de capitalización. La capitalización que publica la empresa usa 46,5 mm sin restar autocartera (solo contra | Con las acciones en circulación a 30-jun-2026 (45,604) sería 2.494,5; a 31-dic-2025 (45,993), 2.515,8. Solo contraste. |
| Control maestro!N52 | Análisis!C55 | Sens.: diluida media FY25 45,48; básica media FY25 45,66; + acciones objetivo ILP 2025–27 45,92 (máx. 46,08). Rango −0,7%/+1,0%. Confianza media-alta. | Sensibilidad de definición (no corrección): básica media 2025 45,656; en circulación 45,993 (31-dic-2025) y 45,604 (30-jun-2026); plan de incentivos 2025–2027 h |
| Control maestro!N54 | Análisis!C57 | Bono español 10 años 4,13%: spread ≈0,65 pp = riesgo país (no forma parte de la rf). Una sola fuente reciente: verificar con Bundesbank. Confianza media. | None |

## Sección 0 de datos_v63.md (configuración económica)

Cambia con la V6.4.1: f 1,0739 → 1,1127, D_hist 296,489 → 320,599, perímetro NIIF 16. Las palancas se eligen sin anticipar la configuración («no se anticipan en las palancas»). ¿Citan las salidas reutilizadas alguna de esas cifras o conceptos? `extracto_v63.md`: ninguno; `fase_a.json`: ninguno; `fase_a.md`: ninguno; `fase_b.json`: ninguno; `fase_b.md`: SR1, θ.

Líneas que mencionan la configuración (revisión de la orquestación: ninguna la usa para fijar una palanca; la de la fase B declara justo lo contrario):

- `fase_b.md`: «Base económica: 31-dic-2025. Ningún hecho de 2026 (1S26, guía, renovaciones posteriores al cierre) apoya una cifra. Documentos que cita el extracto: AR25 = AR_2025.txt, AR19 = AR_2019.txt, IA16, IA21, IA23 = IA_2016/2021/2023_es.txt, CF22 = CF_2022_compilacion.txt; páginas del PDF. «Historia» es la hoja de diez años (columnas C = 2016 … L = 2025; filas 28 crecimiento, 29 margen EBIT, 32 capital in»

## Fuentes

- `texto/`: mismos bytes
- `etapa1/`: mismos bytes

**Lectura.** Las fases reutilizadas son del 12-nov-2026 (sus archivos conservan esa fecha). Lo que cambia en sus entradas es la fecha de análisis y el texto de la evidencia de las cifras frescas, que ahora describe su concepto y sus fechas (4.13 §6). Las cifras no cambian. La plantilla V6.4.1 añade el perímetro de la inversión, que solo actúa en las bases de P-M1 (paso 10, después de la fase B). La fase C y la auditoría se hacen de nuevo con agentes reales.
