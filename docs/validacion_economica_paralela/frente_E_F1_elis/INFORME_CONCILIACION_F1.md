# F1 · Elis · Conciliación económica, puente del FCF base al motor A y especificación propuesta (frente E)

Fecha: 15-nov-2026. Rama: `auditoria/economica-f1-frente-e`, creada desde `auditoria/economica-f1` (c029018).
**F1 sigue abierto.** Esta entrega cierra la conciliación de cifras y puentes con fuentes primarias y cálculos reproducibles. No cierra la decisión económica: la corrección de la plantilla necesita una decisión humana y datos que Elis no publica. No contiene valoraciones, precios objetivo ni recomendaciones de inversión. No se ha modificado código, libros ni datos de producción.

Marcas usadas en todo el informe:
**[P]** dato publicado (página PDF verificada) · **[D]** derivación aritmética de datos publicados o de fórmulas del libro · **[I]** interpretación económica · **[H]** hipótesis no verificable con la base · **[DH]** decisión humana registrada · **[S]** supuesto de la orquestación (no es decisión humana).

---

## 0. Resumen

1. **Base y evidencia.** Base 4.14 materializada desde el ZIP original y verificada (6.798/6.798 + manifiesto). Árbol del hito 4.15 (059f4f6) verificado con su propio manifiesto (7.004/7.004). El libro de Elis es idéntico en ambos (SHA-256 `d2593777…92385`). 683 cifras de cinco informes anuales de Elis verificadas contra los bytes de los PDF, con página, literal y signo; 10/10 contraejemplos rechazados (signo invertido, redondeo, página inexistente o equivocada, fuente ausente o con otra huella).
2. **Conciliación 2023–2025.** Todas las identidades cierran con residuos de ±0,1 de redondeo de la cifra impresa, salvo dos residuos explicados: 0,4 entre interés de arrendamientos de caja (29,6) y devengado (29,2) en 2025 y −0,2 en el free cash flow publicado de 2024 frente a sus componentes. Ninguno es material [D].
3. **FCF base 307,933** reproducido por dos vías independientes (CFO y free cash flow publicado menos SBC). **C48 = 108** se mantiene con su derivación: 82,933 de intereses financieros + 25,067 de interés implícito de caja de arrendamientos [D][DH E6].
4. **f = 4,168 %** se descompone exactamente en: pagos de arrendamientos 153,2 (principal 128,1 + interés de caja 25,1), intereses financieros 82,9, efectos fiscales −24,9 y otros −21,1. **Ni la amortización de derechos de uso ni la de intangibles adquiridos están dentro de f**: aparecen en la reinversión histórica (−81,2) [D].
5. **Motor A** reimplementado desde sus ecuaciones documentadas: reproduce los 30 flujos anuales, los 3 del año 11 y los 3 flujos sin crecimiento del libro con diferencias < 10⁻⁹ [D]. Su flujo sin crecimiento, 248,5, es el FCF base −59,4: +39,6 por el nivel del EBIT 2025, −8,0 por el cambio de tipo impositivo, −9,9 por escalar f a las ventas 2025 y −81,2 porque la proyección no reproduce la reinversión histórica [D].
6. **Arrendamientos: inconsistencia demostrada en la definición del modelo** [D]. En la calibración el coste de arrendamiento se cuenta una vez (los pagos); en la proyección se cuenta dos veces (amortización ROU dentro del margen y pagos completos dentro de f). El exceso equivale a la amortización ROU: 2,9–3,1 % de las ventas (139,4 en la base 2025 si se corrige f). Ocurre a crecimiento cero y en el terminal, y no depende del reparto entre reposición y crecimiento. Es un defecto de definición, no un error de datos. No se corrige aquí.
7. **Intangibles adquiridos: doble cómputo no demostrado.** La V6.3 los trata implícitamente como una reposición monetaria necesaria de 85,7 al año. Hechos publicados: la amortización no es salida de caja, se está agotando y no es deducible en caja. El valor neto de las relaciones con clientes es 275,1 frente a 83,5 de amortización anual, y el diferido de intangibles aporta 15,5/20,3/17,5. La tasa de bajas de clientes no se publica. Requiere una decisión de política [P][I][H].
8. **Reinversión necesaria frente a crecimiento: dato no publicado** en los URD 2021–2025 [P]. Se acota por inferencia, con premisas explícitas, entre la D&A propia (736,0 de media) y el capex propio (867,2). La V6.3 implica 954,0, por encima de lo que Elis invirtió mientras crecía [I]. Es material: el flujo de partida va de 339,8 a 477,8 según el reparto, frente a 248,5 en la V6.3 [D].
9. **Alternativas** A1, A1′, A2 y cota B calculadas, con sus consecuencias en f, el flujo de partida y el ancla de S2C. **Ninguna adoptada**. Especificación con reglas de control y criterios de prueba en [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md).
10. **Pendiente:** decisión F1 (a/b/c con política completa), política de intangibles adquiridos, dato o estimación documentada de la reinversión necesaria, perímetro de S2C. Dos observaciones de la plantilla quedan fuera de F1: la ventana del tipo impositivo y la escala de intereses sin endeudamiento nuevo. La conclusión de nivel de Elis sigue **pendiente_de_datos**.

---

## 1. Alcance, base y evidencia

| Elemento | Identificación | Comprobación |
|---|---|---|
| Base 4.14 | ZIP `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip`, 1.130.912.246 bytes, SHA-256 `bb51942c…b97b93e` | Descargado por la API REST de la Release (la descarga por GraphQL de `gh release download` está bloqueada en esta sesión); `tools/base_414.py materialize` + `verify`: 6.798/6.798, `complete:true` (`/home/user/e_work/inventario/`, fuera del repositorio) |
| Hito 4.15 | `revision/4.15-hito1` = `059f4f68dca7acf465b5f5b21de2dede84c885ff` | Binarios 4.14 copiados sin sobrescribir; `sha256sum -c` de su MANIFIESTO: 7.004 OK, 0 fallos, 0 archivos de más. No se ejecutó `base_414.py` sobre la 4.15 |
| Libro | `…_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx`, SHA-256 `d2593777650f…9c92385` | Idéntico en 4.14 y 4.15. Solo lectura de valores en caché con openpyxl |
| Fuentes | URD 2021, 2022, 2023 y 2025 (inglés) y DEU 2024 (francés) de `elis_decisiones/Elis/fuentes_pdf/` | SHA-256 de [datos/fuentes.json](datos/fuentes.json); coinciden con `HUELLAS_PDF.txt` y con los homónimos de `elis_motor_A` |
| Frente técnico | `claude/hopeful-bardeen-qap6y0`, observado en `d1f1fa9` (hito 2) y en `c0dcbd0` (15-nov, 17:25 UTC) | Hasta `d1f1fa9` solo añade a los componentes de C48 la cifra publicada con su signo (`valor_fuente` negativo, `signo` −1): no cambia valores, el 108,0 ni la plantilla V6.3. `bc48f9d`, `c554cc0` y `c0dcbd0` cambian el verificador de entradas, el pipeline y sus pruebas (U6, U7, H-P1/X2), sin tocar `v6/`, los datos de Elis ni `fase1_historia.py`. Sin cambios de datos o definiciones que afecten a F1. **Recomprobar al integrar** |

**Regla de edición** [D]: cada ejercicio se toma de la publicación más reciente que lo presenta, que es la regla de la Historia. 2025 y 2024 proceden del URD 2025; 2023 del DEU 2024 reexpresado; 2022 del URD 2023 reexpresado; 2021 del URD 2022 reexpresado. Las reexpresiones son pequeñas y proceden sobre todo de la contabilización definitiva de combinaciones: la PPA pasa de 80,1 a 82,9 en 2022, de 85,1 a 85,7 en 2023 y de 84,9 a 85,0 en 2024. Hay además un cambio de presentación: hasta el URD 2023 los intereses de arrendamientos iban dentro de «Net interest paid» (90,2 en 2023); desde el DEU 2024 van dentro de los pagos de arrendamientos (70,5 + 130,8) [P: URD23 p.266, p.279; DEU24 p.273].

**Evidencia reproducible.** Todas las rutas son relativas a esta carpeta.
- `datos/cifras_fuente.csv`: 683 cifras con documento, página PDF, etiqueta de línea, posición, literal impreso y valor con signo.
- `scripts/verificar_cifras.py`: comprueba huella, página, literal y signo sobre los PDF. `scripts/test_verificar_cifras.py` ejecuta 10 contraejemplos.
- `scripts/contraste_f1.py`: 129 comprobaciones aritméticas y de libro, todas OK. Resultados en `resultados/contraste_f1.{json,md}`.
- `resultados/tabla_conciliacion.md`: tabla de cifras con literal y página.
- `evidencias/paginas/`: texto de cada página citada, con la huella de su PDF.

---

## 2. Conciliación anual 2023–2025

La tabla completa, con literal impreso y página de cada cifra, está en [resultados/tabla_conciliacion.md](resultados/tabla_conciliacion.md). Resumen en millones de euros, con el signo convertido al uso del modelo:

| Partida | 2023 | 2024 | 2025 | Fuente (página PDF) |
|---|---|---|---|---|
| Ventas | 4.309,4 | 4.573,7 | 4.796,8 | DEU24 p.270; URD25 p.324 [P] |
| EBIT publicado (resultado operativo) | 496,8 | 596,3 | 629,9 | ídem [P] |
| EBIT de la Historia (BAI + financiero) | 496,8 | 596,3 | 630,0 | [D]; residuo 2025 de +0,1 por redondeo |
| D&A total neta (fila 8) | 877,4 | 965,1 | 1.019,4 | DEU24 p.296; URD25 p.350 [P] |
| · lino propio / otros artículos propios / resto | 482,1 / 32,7 / 161,6 | 537,6 / 35,3 / 172,5 | 565,1 / 36,3 / 183,6 | ídem [P] |
| · derechos de uso NIIF 16 | 115,8 | 132,2 | 149,5 | ídem [P] |
| · intangibles de combinaciones (PPA) | 85,7 | 85,0 | 85,7 | ídem [P] |
| · subvenciones (−) / deterioros (+) | 0,5 / 0,0 | 0,9 / 3,3 | 1,0 / 0,1 | ídem [P] |
| Provisiones: dotación neta | 8,1 | −2,6 | 0,4 | ídem [P] |
| Caja antes de financieros e impuestos | 1.457,9 | 1.584,0 | 1.661,3 | DEU24 p.273; URD25 p.327 [P] |
| Circulante (consumo +) | 5,9 | 6,9 | 4,0 | [P] APM; = −Σ líneas del EFE [D] |
| Impuestos pagados | 126,4 | 124,9 | 146,7 | [P] |
| CFO | 1.325,6 | 1.452,1 | 1.510,6 | [P] |
| Capex bruto (intangibles + material) | 823,9 | 887,4 | 890,2 | [P] |
| · lino / otros artículos / resto | 584,3 / 37,3 / 202,3 | 594,3 / 34,6 / 258,6 | 594,2 / 40,8 / 255,2 | DEU24 p.257; URD25 p.311 [P] |
| Cesiones + subvenciones de inversión | 2,9 + 0,3 | 7,3 + 4,1 | 15,3 + 0,2 | ídem [P] |
| Capex neto («Net capex», C47) | 820,8 | 876,0 | 874,7 | DEU24 p.259; URD25 p.314 [P] |
| Adquisiciones netas de caja (fila 13) | 82,1 | 183,3 | 117,6 | [P] |
| SBC no monetario (C50) / cargas sociales / IFRS 2 total | 22,9 / 8,2 / 31,1 | 27,1 / 4,3 / 31,4 | 34,7 / 11,2 / 45,9 | DEU24 p.259, p.273; URD25 p.314, p.327, p.345 [P]; suma exacta [D] |
| Pagos de arrendamientos (principal + intereses) | 130,8 | 150,8 | 177,9 | [P] |
| · principal (C49) | 111,0 | 125,0 | 148,3 | DEU24 p.312; URD25 p.366 [P] |
| · interés implícito de caja (pagos − principal) | 19,8 | 25,8 | 29,6 | [D] |
| · interés devengado (nota 8.2) | 19,8 | 25,8 | 29,2 | DEU24 p.324; URD25 p.379 [P] |
| Intereses financieros netos pagados (sin arrendamientos) | 70,5 | 78,9 | 99,4 | [P] |
| Gasto por impuesto / corriente / diferido | 110,3 / 120,3 / −10,1 | 128,3 / 127,7 / 0,6 | 126,2 / 147,2 / −21,0 | DEU24 p.337; URD25 p.392 [P] |
| Deuda financiera bruta / caja / neta | 3.690,7 / 665,3 / 3.025,4 | 3.660,1 / 622,0 / 3.038,0 | 3.418,3 / 398,1 / 3.020,2 | DEU24 p.329; URD25 p.384 [P] |
| Pasivo por arrendamientos | 538,3 | 606,2 | 703,2 | [P] |
| Free cash flow publicado (APM) | 303,6 | 346,3 | 358,6 | DEU24 p.259; URD25 p.314 [P] |

**Identidades y residuos** (cálculo exacto; `resultados/contraste_f1.md`, primera tabla) [D]:

| Identidad | 2023 | 2024 | 2025 | Explicación |
|---|---|---|---|---|
| EBIT → caja antes de financieros e impuestos (NI + impuesto + financiero + SBC + amortizaciones y provisiones + subvenciones + plusvalías + earnout) | 0,0 | 0,0 | +0,1 | Redondeo de líneas impresas |
| Caja antes − circulante − impuestos pagados = CFO | 0,0 | −0,1 | 0,0 | Redondeo |
| D&A: componentes = total | 0,0 | +0,1 (D&A en EBIT) | +0,1 (total) | Redondeo de componentes |
| Línea del EFE «amortizaciones y provisiones» = D&A total + subvención + provisiones | 0,0 | 0,0 | 0,0 | Exacta: 1.020,8 = 1.019,4 + 1,0 + 0,4. **No se sustituye 1.019,4 por 1.020,8**: la diferencia son subvenciones y provisiones |
| Capex bruto del EFE = lino + otros + resto | 0,0 | −0,1 | 0,0 | Redondeo |
| Capex neto = bruto − cesiones − subvenciones | +0,1 | 0,0 | 0,0 | 2023: 820,8 publicado frente a 820,7 de las líneas; ya registrado en C47 |
| FCF publicado = suma de sus componentes | +0,1 | **−0,2** | 0,0 | 2024: la tabla del URD 2025 imprime 346,3 (346,4 en el DEU 2024) frente a 346,5 de sus componentes. Redondeo y reexpresión; no afecta a C52, que se construye por la vía CFO |
| Interés de arrendamientos: caja − devengo | 0,0 | 0,0 | **+0,4** | Ver §5.4 |
| Movimiento del pasivo y del ROU | 0,0 | 0,0 / −0,1 | 0,0 | Redondeo |
| Impuesto corriente + diferido = gasto | −0,1 | 0,0 | 0,0 | Redondeo |
| Deuda bruta − caja = deuda neta | 0,0 | +0,1 | 0,0 | Caja 622,0 frente a 622,1 entre ediciones |

**Historia y Análisis frente a la fuente** [D]. Se contrastaron 72 celdas de Historia y todas coinciden exactamente con las cifras publicadas:
- 64 de filas: 6, 7, 8, 10, 11, 12, 13, 14, 15, 17 y 18 de 2021–2025, y 22, 23 y 24 de 2023–2025;
- G6 (ventas 2020);
- las anclas C52, C58, C70, C74–C76 y C79.
 Las celdas de Análisis C46–C52 coinciden con las medias publicadas redondeadas a tres decimales: el libro registra 1.429,433, 857,167 y 28,233 frente a las medias exactas 1.429,4333…, 857,1666… y 28,2333…. Por eso C52 vale 307,933 frente a 307,93333. El efecto en f es −7,3·10⁻⁸ y en los flujos ≤ 0,0006 mm. No es material, pero «exacto» en el registro significa redondeado a tres decimales; la especificación debe fijarlo (§E7 de la especificación).

---

## 3. Horizonte 2021–2025 (S2C)

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Ventas (2020: 2.806,3) | 3.048,3 | 3.820,9 | 4.309,4 | 4.573,7 | 4.796,8 |
| Crecimiento orgánico [P] | 7,4 % | 21,0 % | 11,8 % (efecto precio ≈ +9 %) | 5,2 % | 3,8 % |
| Capex bruto | 573,9 | 699,8 | 823,9 | 887,4 | 890,2 |
| · lino − amortización de lino | 19,8 | 94,8 | 102,2 | 56,7 | 29,1 |
| D&A total / ROU / PPA | 744,8 / 92,6 / 81,1 | 799,0 / 103,7 / 82,9 | 877,4 / 115,8 / 85,7 | 965,1 / 132,2 / 85,0 | 1.019,4 / 149,5 / 85,7 |
| D&A propia (total − ROU − PPA) | 571,1 | 612,4 | 675,9 | 747,9 | 784,2 |
| Circulante (consumo +) | −10,2 | 52,6 | 5,9 | 6,9 | 4,0 |
| Adquisiciones | 86,8 | 221,7 | 82,1 | 183,3 | 117,6 |
| Fila 30: capex − D&A total + circulante | −181,1 | −46,6 | −47,6 | −70,8 | −125,2 |
| Capex − D&A propia + circulante | −7,4 | 140,0 | 153,9 | 146,4 | 110,0 |

Fuentes [P]: URD21 p.211 y p.226; URD22 p.243, 247, 258, 261 y 284; URD23 p.261, 266, 276, 279 y 301; más las de 2023–2025.

- **C53 (S2C marginal de 5 años) = 9,04** [D]: (4.796,8 − 2.806,3) ÷ Σ₂₀₂₁₋₂₅ (capex − D&A total + circulante + adquisiciones) = 1.990,5 ÷ 220,2. Su denominador usa la D&A total, que incluye ROU y PPA sin contrapartida en el capex. Con el mismo cálculo y la D&A propia sale 1,61; sin ROU, 2,45 (§9) [D]. Las palancas S2C del expediente (1 / 1,2 / 1,5) no usan C53. La fase C las ancló en «la inversión propia sobre la amortización propia de 2024–25 (S2C ≈ 1,5)» (`elis_decisiones/Elis/fase_c.json`, desviación G7) [I]. **El perímetro de las palancas S2C (propio) no es el de f (D&A total).**
- **Ruptura de presentación en las filas 15/16** [P][D]: 2021 y 2022 incluyen los intereses de arrendamientos (74,6 y 72,9, «including interest on lease liabilities», URD22 p.261), mientras 2023–2025 los excluyen. No afecta a C48, que usa 2023–25 y suma el interés de caja de arrendamientos aparte, ni a C58. Sí afecta a la comparabilidad de la fila 35 de 2021–22 y debe declararse si se amplía la ventana.
- **Fila 18 de 2021** [P][D]: 28,0 procede de la nota 5.2 («Equity-settled share-based payments», URD22 p.287); el EFE da 24,4 (URD22 p.261). Los demás años usan el EFE. Fuera de la ventana de f; se declara como incoherencia de fuente de la fila.
- **El crecimiento orgánico de 2022–23 fue en buena parte precio** [P: «price effect of +9% on average», URD23 p.261]. Las anclas S2C calculadas sobre crecimiento orgánico nominal sobrestiman la productividad del capital en volumen [I].

---

## 4. Puente del FCF base 307,933 a f y al motor A

### 4.1 FCF base (Análisis C46–C52)

FCF base = CFO − capex neto − (intereses financieros + interés de caja de arrendamientos) − principal de arrendamientos − SBC no monetario, en media 2023–25 [DH 10-nov-2026 y E6; D]:

| Año | CFO | − capex neto | − intereses fin. | − interés arr. (caja) | − principal arr. | − SBC | = FCF base del año | Vía FCF publicado − SBC |
|---|---|---|---|---|---|---|---|---|
| 2023 | 1.325,6 | 820,8 | 70,5 | 19,8 | 111,0 | 22,9 | 280,6 | 280,7 |
| 2024 | 1.452,1 | 876,0 | 78,9 | 25,8 | 125,0 | 27,1 | 319,3 | 319,2 |
| 2025 | 1.510,6 | 874,7 | 99,4 | 29,6 | 148,3 | 34,7 | 323,9 | 323,9 |
| Media | 1.429,433 | 857,167 | 82,933 | 25,067 | 128,1 | 28,233 | **307,933** | 307,933 |

- **C48 = 108,0 = 82,933 + 25,067** [D]. Se mantiene. Sustituirlo por 82,933 dejaría sin restar 25,067 de pagos de arrendamientos (FCF base 333,0). Con el interés devengado en lugar del de caja sería 107,867. Ambas son variantes calculadas y **no adoptadas**: el FCF base es un concepto de caja y C48 está conciliado con E6 [DH].
- El cupón en caja de la OCEANE (2,25 % sobre 380,0, URD25 p.380 [P]) está dentro de los intereses pagados según el registro E6; el devengo no monetario del componente de deuda no está [DH E6]. No se cambia.
- FCF base = media del free cash flow publicado − media del SBC (336,167 − 28,233). Las dos vías coinciden en la media aunque por año difieran en ±0,1 [D].

### 4.2 f y su composición económica

Definición de la plantilla (Convenciones V6.3 §10; Historia C58 y filas 73–81) [P/D]:

f = [NOPAT medio − reinversión media − FCF base] ÷ ventas medias = [416,799 − (−81,2) − 307,933] ÷ 4.559,967 = 190,066 ÷ 4.559,967 = **0,041681455**

con NOPAT = EBIT × (1 − tipo efectivo de cada año, fila 10, 4 decimales) y reinversión = capex bruto − D&A total + circulante.

**Descomposición independiente** [D]. Sustituyendo las identidades del estado de flujos, f·ventas es exactamente la suma de estos componentes (comprobado por año y en media):

| Componente de f·ventas (media 2023–25) | mm | Naturaleza |
|---|---|---|
| Principal de arrendamientos | 128,100 | caja, financiación |
| Interés de arrendamientos (caja) | 25,067 | caja, financiación |
| Intereses financieros netos pagados | 82,933 | caja, financiación |
| Escudo fiscal del gasto financiero (−τ·financiero) | −35,976 | el NOPAT aplica τ al EBIT; el impuesto real descuenta el gasto financiero |
| Impuesto pagado − gasto por impuesto | +11,067 | caja frente a devengo; incluye la reversión no monetaria del diferido de intangibles (§7) |
| Redondeo de τ a 4 decimales | +0,009 | redondeo |
| Capex neto − bruto (cesiones y subvenciones) | −10,000 | la reinversión usa capex bruto; el FCF base, neto |
| Plusvalías por enajenación (no monetarias en el EBIT) | +3,833 | 2025: +23,1 (bajas de inmovilizado +25,7 en OOIE) |
| Earnout y otros no monetarios | −13,000 | 2023: −48,4 por la reestimación del earnout de México, cargo no monetario en el EBIT 2023 |
| Provisiones | −1,967 | dotación neta no monetaria |
| EBIT de la Historia − EBIT del EFE; residuos del EFE | 0,000 | redondeos que se compensan |
| **Total = Historia C79** | **190,066** | |

Consecuencias [D]:
- f es, en sustancia, **236,1 de financiación y arrendamientos, menos 24,9 de efectos fiscales y menos 21,1 de partidas de la ventana**. Ni la amortización ROU ni la PPA son componentes de f. El SBC no está en f para Elis: se resta en el FCF base y ya está en el EBIT, así que se compensa. Las adquisiciones tampoco: no están en el FCF base.
- La afirmación del hallazgo de 14-nov, «f incluye 85,7 de amortización de intangibles», es imprecisa [I]. La PPA no está en f. Está en el EBIT y se devolvía en la reinversión histórica. Su efecto en la proyección se analiza en §6.
- Dos partidas de la ventana proyectan como fuga permanente algo puntual [I]:
  - el componente de earnout y otros no monetarios (−13,0 de media, dominado por el cargo de −48,4 de 2023) baja f en 0,29 puntos de ventas;
  - las plusvalías netas de la ventana (+3,8 de media; +23,1 en 2025) la suben en 0,08 puntos.

  Además, la plusvalía de 2025 (+25,7 en OOIE) eleva m0 (13,13 %) unos 0,54 puntos. Son efectos de calibración documentados, no decisiones.

### 4.3 Motor A: réplica y flujo de partida

Ecuaciones de la V6.3 (Convenciones §1–§3), reimplementadas sin leer las fórmulas de las celdas. Coinciden con los 33 flujos (AU6:BD8), los 3 flujos del año 11 (BF6:BF8) y el flujo sin crecimiento (BL·r) con diferencias < 10⁻⁹ [D]:

- flujo_t = V_t·[m_t·(1 − τ) − f] − (V_t − V_{t−1}) ÷ S2C; terminal = V₁₀·(1+g)·[m_obj·(1 − τ)·(1 − g/ROIC) − f].
- V₀ = 4.796,8; m₀ = 630,0/4.796,8 = 13,134 %; τ = 28,82 % (media de 5 años de la fila 10); f = 4,168 %.
- **Flujo sin crecimiento F₀ = V₀·[m₀(1 − τ) − f] = 248,496.**

**Puente FCF base → F₀** [D]:

| Paso | mm |
|---|---|
| FCF base (C52) | 307,933 |
| + nivel del EBIT 2025 (630,0) frente a la media 2023–25 (574,367), al τ de 5 años | +39,600 |
| + τ de 5 años (28,82 %) frente al τ de cada año en la ventana (NOPAT 408,834 frente a 416,799) | −7,965 |
| − f aplicada a las ventas 2025 en lugar de las medias | −9,872 |
| + reinversión histórica media (C76) que la proyección no reproduce | −81,200 |
| **= F₀** | **248,496** |

**Puente F₀ → año 1** [D] (palancas del expediente, que son juicio de la fase C y no se discuten aquí):

| | MALO | NORMAL | BUENO |
|---|---|---|---|
| F₀ | 248,496 | 248,496 | 248,496 |
| + NOPAT por ventas y margen del año 1 | −9,376 | +15,657 | +27,302 |
| − f sobre el aumento de ventas | −3,999 | −8,997 | −10,997 |
| − reinversión de crecimiento ΔV/S2C (S2C = 1 / 1,2 / 1,5) | −95,936 | −179,880 | −175,883 |
| = flujo del año 1 | 139,185 | 75,276 | 88,920 |

### 4.4 Qué es el −81,2

Descomposición exacta de la reinversión media C76 [D]:

| Bloque (media 2023–25) | mm |
|---|---|
| Lino: compras − amortización | +62,667 |
| Otros artículos propios en alquiler: compras − amortización | +2,800 |
| Resto de inmovilizado e intangibles: compras − amortización | +66,133 |
| Subvenciones (+) y deterioros (−) | −0,333 |
| Residuo de redondeo | −0,100 |
| Circulante | +5,600 |
| **Inversión neta propia + circulante** | **+136,767** |
| − amortización de derechos de uso NIIF 16 | −132,500 |
| − amortización de intangibles de combinaciones | −85,467 |
| **= C76** | **−81,200** |

El −81,2 es una identidad de las entradas. **Por sí solo no prueba un doble cómputo**: el mismo signo aparecería si Elis hubiera invertido por debajo de sus necesidades de reposición [I]. Lo que permite concluir es la naturaleza de cada bloque (§5 y §6), no el signo del total.

---

## 5. Arrendamientos

### 5.1 Bloques distintos que no se mezclan [P][D]

| Bloque | Qué es | Caja | No monetario | Dónde está en el libro |
|---|---|---|---|---|
| Lino y equipos propios en alquiler-mantenimiento | Inmovilizado material propio que Elis alquila a sus clientes; amortización de 18 meses a 5 años (URD25 p.367) | Compras de lino 584,3/594,3/594,2 y otros artículos 37,3/34,6/40,8 dentro de las compras de inmovilizado | Inversión devengada 621,6/628,8/635,0, que coincide con la de caja | Capex (fila 12) y D&A propia (fila 8) |
| Derechos de uso NIIF 16 (ROU) | Inmuebles, vehículos y equipos que Elis arrienda (nota 6.3) | Pagos 130,8/150,8/177,9 (financiación) | Altas 159,0/194,3/245,6 (nuevos, reestimaciones y combinaciones); amortización 115,8/132,2/149,5 | Fila 8 (amortización), fila 17 (principal), C48 (interés de caja), fila 23 (pasivo). Las altas no están en ninguna fila |

**El lino propio no es ROU** y no debe reclasificarse. Las altas ROU no son capex de caja y no deben sumarse al capex [P].

### 5.2 Dónde queda el coste de arrendamiento

| | Calibración (2023–25) | Proyección (base 2025) |
|---|---|---|
| Amortización ROU dentro del EBIT/NOPAT | −132,5 | −149,5 (dentro de m₀) |
| Devolución de la amortización ROU por la reinversión (− D&A total en C76) | +132,5 | 0 (ΔV/S2C no la devuelve) |
| Pagos de arrendamiento dentro del FCF base y de f | −153,2 | −161,1 (f·V₀) |
| **Coste de arrendamiento reconocido** | **−153,2 (una vez: los pagos)** | **−310,6 (dos veces)** |

### 5.3 Demostración (derivación) y su alcance

**Premisas:**
- (i) Las altas ROU no son salidas de caja: las financia el arrendador y aumentan el pasivo [P: URD25 p.366; estado de flujos sin capex ROU].
- (ii) El FCF base resta los pagos completos de arrendamiento (C48 + C49) [DH registrada].
- (iii) La proyección del motor es NOPAT − f·V − ΔV/S2C, sin ningún término que devuelva la amortización ROU [P: Convenciones V6.3; réplica exacta, §4.3].

**Conclusión** [D]. Con crecimiento cero (y en el valor terminal cuando g → 0), el flujo del motor es NOPAT − f·V: resta la amortización ROU dentro del margen y los pagos completos dentro de f. El coste económico de caja del arrendamiento para el accionista son los pagos; con pasivo constante, el principal se repone con nuevos contratos no monetarios. Por tanto el motor carga **de más, aproximadamente, la amortización ROU**:
- 2,906 % de las ventas en media 2023–25 y 3,117 % en 2025;
- 139,4 en la base 2025 si se corrige f con la media de la ventana;
- 43 % del FCF base.

La demostración sintética de `contraste_f1.py` lo confirma con números redondos: sin impuestos, sin crecimiento, EBITDA 100, capex propio = D&A propia = 20, ROU 10 y pagos 12. El FCF verdadero es 68 y la V6.3 da 58 [D].

**Alcance:**
- No depende del reparto entre reposición y crecimiento.
- No depende de la palanca S2C, porque se produce a crecimiento cero.
- No depende del margen objetivo, salvo que se definiera como margen después de pagos de arrendamiento. No es el caso: la fase C ancla los márgenes en el EBIT NIIF 16 publicado [I, `fase_c.json` G5].

Es un **defecto de definición** de la calibración de f en el motor A para empresas con NIIF 16 material, no un error de datos. **No cuantifica por sí solo el error de valor**: este depende también de §6 y de las palancas. **No autoriza una corrección**: corresponde a la decisión F1 [DH pendiente].

### 5.4 Interés de caja 29,6 frente a devengado 29,2

En 2023 y 2024 coinciden (19,8 y 25,8). En 2025 difieren en 0,4 [D]. Las notas publicadas no traen un puente: el movimiento del pasivo no muestra los intereses devengados por separado. Posibles causas no verificables [H]: interés devengado no pagado al cierre, efecto del tipo de cambio en las fechas de pago, modificaciones de contratos o el residuo de «otros movimientos» (0,3).

**Materialidad:** 0,133 en C48 (0,04 % del FCF base). **Tratamiento:** se conserva la cifra de caja, coherente con un FCF de caja, y se registra el residuo. No se intercambian los datos.

### 5.5 Pasivo por arrendamientos y deuda

En el motor A el pasivo por arrendamientos (703,2) no se resta: es coherente con un flujo al accionista que ya paga los arrendamientos dentro de f [D]. Entre 2022 y 2025 el pasivo creció de 485,4 a 703,2 por altas no monetarias superiores al principal [P]. Con f proporcional a las ventas, los pagos crecen con el negocio, lo que equivale a suponer que la cartera arrendada crece con él [I].

---

## 6. Intangibles adquiridos y reinversión necesaria frente a crecimiento

### 6.1 Búsqueda del desglose [P]

Se buscó en los cinco informes 2021–2025 y en el comunicado de resultados de 2025. Términos en inglés y francés: «maintenance capex», «growth capex», «replacement», «renewal», «churn», «attrition», «retention rate», «investissements de maintenance/de croissance», «renouvellement», «taux de perte». **No hay importes de reparto entre mantenimiento y crecimiento.** Lo publicado:

- La inversión industrial «covers investments for both growth (new plants or to increase capacity) and maintenance (equipment replacement)» (URD25 p.312; DEU24 p.258).
- Gasto en lino: «Growth investments thus make up a large percentage of this expenditure because of the initial outlay required to set up a new customer» (URD25 p.312). No da porcentaje.
- «customer attrition rates are monitored at the Executive Committee», pero la tasa no se publica (URD25 p.141).
- Capex por tipo de activo (lino, otros artículos, resto; URD25 p.311; DEU24 p.257; URD23 p.266; URD22 p.247). Es un desglose por activo, no por finalidad.
- Inversión neta del 18,2–19,2 % de las ventas; lino, 12,4 % (2025) y 13,0 % (2024) de las ventas (URD25 p.311).

Fuentes que podrían contenerlo y **no están en la base**: presentaciones de mercado de capitales, respuestas de Relación con Inversores (el expediente ya redactó la pregunta en `Diagnóstico V6!B223`) y transcripciones de presentaciones de resultados. Registrar su existencia no equivale a disponer de sus bytes.

### 6.2 Lo que se puede derivar e inferir

- **[D]** Inversión neta propia (capex − D&A propia + circulante): −7,4 / 140,0 / 153,9 / 146,4 / 110,0 en 2021–2025. En lino: 19,8 / 94,8 / 102,2 / 56,7 / 29,1. En 2025 el lino casi iguala su amortización y el resto del inmovilizado la supera en 71,6.
- **[I] Cota superior de la reinversión necesaria: el capex propio.** Elis creció en todos los ejercicios: orgánico de 3,8 % en 2025 y 5,2 % en 2024. Además declara que una parte grande del lino y parte de la inversión industrial son crecimiento. Por tanto, su reinversión necesaria para sostener las ventas fue menor que el capex propio (867,2 de media). Premisa: el crecimiento orgánico tuvo un componente de volumen, no solo de precio.
  - Evidencia cualitativa publicada, sin importes [P]: el crecimiento de 2025 fue «driven by a price effect from residual inflation in 2025, and a volume effect» (URD25 p.122) y el de 2024 «tirée par l'effet prix … et par l'effet volume» (DEU24 p.121). Los costes de proceso de 2025 subieron «in connection with the continued growth in volumes processed» (URD25 p.309).
  - En 2023 el efecto precio fue ≈ +9 % sobre el 11,8 % orgánico (URD23 p.261).
  - El reparto cuantitativo precio/volumen de 2024–25 no se publica.
- **[I] Referencia inferior: la D&A propia** (736,0 de media). No es una cota demostrada. Con inflación, reponer a coste actual cuesta más que la amortización a coste histórico, sobre todo en edificios y maquinaria de vida larga. El lino, con vidas de 18 meses a 5 años, se aproxima más a su amortización.
- **[D] La V6.3 implica una reinversión necesaria igual a la D&A total** (954,0 de media; 1.003,5 en la base 2025): 86,8 más que el capex propio medio mientras la empresa crecía. Con las premisas anteriores, esa hipótesis implícita es **incompatible con la historia publicada** [I].

### 6.3 Reposición económica de los intangibles adquiridos [P][D][I]

- **Composición [P].** La PPA de 85,7 (2025) son relaciones con clientes, 83,5, y marcas, 2,2 (URD25 p.364). Las relaciones con clientes se amortizan en 4–14 años (URD25 p.364; DEU24 p.310).
- **Agotamiento [P/D].** Valor neto de las relaciones con clientes: 471,5 (1-ene-2023) → 414,9 → 351,6 (reexpresado) → **275,1** (31-dic-2025). Las altas por combinaciones fueron pequeñas: 20,6 / 32,3 / 3,7. Sin compras nuevas, el ritmo actual de amortización no puede durar más de unos 3,3 años (275,1 ÷ 83,5) [D]. Bruto acumulado 1.444,5, del que 1.169,4 ya está amortizado: es sobre todo la cartera de compras anteriores.
- **Fiscalidad [P].** El diferido de intangibles aporta un ingreso de 15,5 / 20,3 / 17,5 en 2023–2025 (URD23 p.346; DEU24 p.338; URD25 p.393): la amortización de lo adquirido reduce el gasto por impuesto, pero no el impuesto de caja.
- **Interpretación [I].** Las relaciones adquiridas se consumen a medida que se van clientes. Elis las repone (a) orgánicamente, con coste comercial ya incluido en el EBIT y lino para clientes nuevos ya incluido en el capex propio, o (b) con nuevas adquisiciones, que son caja fuera del FCF base e incluidas en C53 a través de la fila 13. La amortización contable de lo adquirido no mide ninguna de las dos. Que no sea salida de caja **no demuestra** que la cartera se mantenga gratis. Lo que indica es que su coste de reposición está en el EBIT y en el capex, o en las compras, y no en la PPA.
- **Hipótesis implícita de la V6.3 [H].** Cargar la PPA de forma perpetua equivale a suponer una reposición monetaria igual a la PPA, unos 85,7 al año. No hay dato publicado que la sostenga ni que la refute: no se publica la tasa de bajas ni las bajas de clientes adquiridos. **Doble cómputo no demostrado. Requiere decisión de política** (§10).

### 6.4 Qué falta, cuánto pesa y qué impide concluir

| # | Dato que falta | Materialidad (flujo, base 2025) | Conclusión que bloquea |
|---|---|---|---|
| M1 | Reparto de la inversión propia entre reposición y crecimiento, por bloque (lino, otros artículos, industrial/TI) y año | Flujo de partida entre 339,8 (todo el capex es reposición) y 477,8 (reposición = D&A propia); intervalo de 138, el 45 % del FCF base | Nivel del flujo de partida del motor A y, con él, cualquier nivel de valor del motor A; anclaje de S2C |
| M2 | Tasa de bajas de clientes, en particular de los adquiridos, y desembolso inicial por cliente nuevo | Política PPA: 85,7 al año (28 % del FCF base); diferencia entre A1 y A2 en el flujo de partida: 89,9 | Si la PPA es un coste de reposición |
| M3 | Política de proyección: crecimiento orgánico frente a crecimiento con adquisiciones | Cambia el ancla de S2C: en A2, 1,61 con adquisiciones frente a 2,07–3,13 orgánico; en A1, 2,45 frente a 5,52–13,85 | Coherencia entre crecimiento proyectado, inversión y PPA |
| M4 | Puente caja/devengo del interés de arrendamientos de 2025 | 0,4 (0,04 % del FCF base) | Ninguna |
| M5 | Efecto precio y volumen del crecimiento orgánico 2024–25 | Anclas S2C orgánicas | Calibración de las palancas S2C, no de f |

M1 y M2 son materiales y no se pueden resolver con la base. **Se conserva `pendiente_de_datos` para la conclusión de nivel**, como ya hace el expediente.

---

## 7. Impuestos

| | 2023 | 2024 | 2025 | Fuente |
|---|---|---|---|---|
| τ de la fila 10 (gasto ÷ BAI, 4 decimales) | 29,63 % | 27,54 % | 25,60 % | [D] de DEU24 p.270; URD25 p.324 |
| Impuesto nocional τ·EBIT (dentro del NOPAT) | 147,2 | 164,2 | 161,3 | [D] |
| Gasto por impuesto | 110,3 | 128,3 | 126,2 | [P] |
| · diferencia = escudo del gasto financiero τ·financiero | 36,9 | 35,9 | 35,1 | [D] |
| Corriente / diferido | 120,3 / −10,1 | 127,7 / 0,6 | 147,2 / −21,0 | [P] DEU24 p.337; URD25 p.392 |
| · diferido por intangibles (ingreso no monetario) | 15,5 | 20,3 | 17,5 | [P] URD23 p.346 (edición original); DEU24 p.338; URD25 p.393 |
| · diferido de ROU + pasivos por arrendamiento | −0,4 | 2,3 | 1,7 | [P] ídem |
| Impuestos pagados | 126,4 | 124,9 | 146,7 | [P] |
| Pagado − nocional (componente fiscal de f) | −20,8 | −39,3 | −14,6 | [D] |
| Partidas especiales | earnout no deducible: +15,8 de impuesto | — | contribución excepcional francesa: 4,9 | [P] DEU24 p.337; URD25 p.392 |
| CVAE/IRAP incluidos en el gasto | 4,6 | 3,5 | 3,7 | [P] |

- No se toma el gasto (126,2) por el impuesto de caja (146,7). f recoge, como fuga, la diferencia entre el impuesto pagado y el nocional [D].
- **Tratamiento fiscal de los ajustes ROU y PPA.** Las alternativas de §9 cambian un concepto de caja antes de impuestos: el perímetro de la reinversión. La identidad de calibración se mantiene exacta y no necesita un ajuste fiscal adicional. Los efectos fiscales reales ya están en los impuestos pagados que calibran f: la no deducibilidad en caja de la PPA y el efecto casi neutro de NIIF 16 [D].
  - **Limitación [I]:** en la proyección esos efectos se escalan con las ventas, aunque la PPA se agote. El escudo nocional τ·PPA dentro del NOPAT es 25,4 / 23,4 / 21,9 y queda compensado en la historia por el diferido de intangibles.
- **Observación fuera de F1 [D]:** f se calibra con el τ de cada año (media efectiva ponderada ≈ 27,4 %) y la proyección aplica el τ de 5 años (28,82 %, que incluye el 33,1 % de 2021). Efecto en la base: −8,0 al año. Es una convención (Convenciones §4 y C52), no un error. Si se revisa, debe decidirse expresamente.

---

## 8. Financiación y flujo al accionista

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Free cash flow publicado | 303,6 | 346,3 | 358,6 |
| FCF base del año (después de SBC) | 280,6 | 319,3 | 323,9 |
| Adquisiciones | 82,1 | 183,3 | 117,6 |
| Dividendos | 61,7 | 101,3 | 105,1 |
| Recompras − ampliaciones | −9,1 | −8,2 | 139,0 |
| Emisión neta de deuda (EFE) | +208,9 | −95,8 | −210,6 |
| Deuda financiera neta al cierre | 3.025,4 | 3.038,0 | 3.020,2 |
| Pasivo por arrendamientos al cierre | 538,3 | 606,2 | 703,2 |
| OCEANE (componente de deuda) | 343,1 | 352,3 | 362,0 |

Fuentes [P]: DEU24 p.259, 273 y 329; URD25 p.314, 327 y 384. El puente publicado de la deuda neta cierra en 2025 (FCF 358,6 − adquisiciones 117,6 − deuda adquirida 9,1 − otros flujos 12,7 − dividendos 105,1 − capital y acciones propias 139,0 + otros 42,7 = 17,8 de reducción) y en 2024 con un residuo de 0,1 [D].

- **Deuda constante [D/I].** El FCF base resta intereses pero no amortizaciones ni nuevas emisiones de deuda financiera: equivale a un flujo al accionista con la deuda refinanciada. La deuda neta fue estable en 2023–25 (3.025 → 3.038 → 3.020), lo que es coherente con esa lectura histórica.
- **Observación fuera de F1 [D][I].** En la proyección, f escala los intereses con las ventas (1,82 % de las ventas) sin el endeudamiento nuevo que haría falta para que la deuda creciera con el negocio. En el año 1:
  - los intereses adicionales son 1,7 / 3,9 / 4,8 (MALO / NORMAL / BUENO);
  - si la deuda neta se mantuviera en el 63 % de las ventas, el endeudamiento neto omitido sería 60,4 / 135,9 / 166,1.

  La plantilla lo declara («supone que escala con el negocio»). Es una convención con sesgo prudente cuya revisión es económica y no forma parte de F1.
- Acciones, SBC y OCEANE se mantienen según E6 [DH]: acciones en circulación a 31-dic-2025, OCEANE como deuda y sin acciones de conversión. El SBC se resta como coste (C50), y la dilución potencial de la OCEANE y de las acciones de rendimiento se identifica aparte, sin contarla dos veces.

---

## 9. Definiciones económicas y alternativas coherentes (ninguna adoptada)

**Definiciones propuestas:**
- **Reinversión necesaria (R):** inversión propia anual para sostener las ventas a volumen constante. Incluye la reposición de clientes perdidos.
- **Inversión de crecimiento:** capex propio − R + circulante.
- **D&A propia:** D&A total − ROU − PPA.
- **Perímetro de la reinversión:** el conjunto de D&A que se supone repuesto con capex propio. Debe ser el mismo en la calibración de f, en el ancla de S2C y en la proyección.

| | A0 · V6.3 actual | A1 · sin ROU | A1′ · arrendamientos como deuda renovada | A2 · perímetro propio | B · cota |
|---|---|---|---|---|---|
| Reinversión necesaria supuesta | D&A total | D&A total − ROU | D&A total; FCF base sin principal | D&A propia | Capex propio |
| R media 2023–25 | 954,0 | 821,5 | 954,0 | 736,0 | 867,2 |
| R − capex medio | **+86,8** | −45,7 | +86,8 | −131,2 | 0 |
| f | 4,168 % | 1,262 % | 1,359 % | −0,612 % | 2,265 % |
| Flujo sin crecimiento (base 2025) | 248,5 | 387,9 | 383,2 | 477,8 | 339,8 |
| S2C total 2021–25 (con adquisiciones) | 9,04 | 2,45 | — | 1,61 | 2,65 |
| S2C orgánico 2023–25 / 2021–25 | no definido | 5,52 / 13,85 | — | 2,07 / 3,13 | no significativo |
| Coherencia con los arrendamientos | **No** (§5.3) | Sí | Sí, en estado estacionario (principal ≈ amortización ROU) | Sí | Sí |
| Tratamiento de la PPA | Reposición monetaria implícita | Reposición monetaria implícita | Reposición monetaria implícita | No monetaria, sin reposición | Incluida en el capex observado |
| Evidencia | Hipótesis implícita contraria a la historia (R > capex) [I] | Lease: [D]; PPA: [H] | Lease: [D]; cambia una entrada registrada | Lease: [D]; PPA: [I]/[H]; R = D&A propia: [H] | Cota: [I] |
| Límites | Doble coste de arrendamiento | Mantiene la hipótesis PPA | Sustituye el principal de caja (128,1) por la amortización ROU (132,5); **modifica C49, registrado: requiere decisión** | Si la reposición a coste actual supera la D&A propia, sobrestima el flujo | No es una alternativa: supone crecimiento sin inversión |

Fuente: `resultados/contraste_f1.md`, tabla «Alternativas».

Lectura [I], sin adoptar nada:
- A0 es incoherente con la mecánica de NIIF 16 y su reinversión implícita supera lo invertido.
- A1 y A2 corrigen el arrendamiento y difieren solo en la política de la PPA.
- A1′ es coherente, pero toca la construcción registrada del FCF base.
- El intervalo B–A2 refleja la falta del dato M1.
- **Motor B como vía alternativa:** con f = 0 y el pasivo por arrendamientos restado, trata los arrendamientos de forma coherente, porque en estado estacionario las altas ROU equivalen a la amortización ROU. Mantiene la misma cuestión de la PPA y una incoherencia propia de perímetro en el coste de la deuda: C63 divide intereses sin arrendamientos entre deuda con arrendamientos. La elección de motor (C62 = Sí) es de la fase A y no se cambia aquí.

**Ninguna alternativa se elige por su efecto en el resultado.** La elección depende de la decisión F1 y de los datos M1–M3.

---

## 10. Hipótesis, incertidumbres y decisiones

**Decisiones humanas registradas que se conservan** [DH]: E1 (valores exactos en Viscofan/Vidrala), D3 (acciones de Viscofan), E2 (K14 de Vidrala) y E6 (Elis: base coherente a 31-dic-2025, acciones en circulación, OCEANE como deuda sin acciones de conversión, C48 conciliado, dilución aparte). No se vuelven a pedir y este informe no altera ninguna. La construcción del FCF base (media 2023–25, capex neto, C48 = 82,9 + 25,1) procede de la decisión del inversor del 10-nov-2026 registrada en C47/C48.

**Supuestos de la orquestación que siguen vigentes** [S]: F1 opción (a), es decir, motor A «no validado para casos con NIIF 16» y precio de Sí no utilizable. Medias de C46/C47/C50 registradas con tres decimales.

**Decisiones pendientes** (de la persona responsable; no se adoptan por obtener números):
1. **F1:** (a) declarar el límite y no usar el motor A en esos casos; (b) corregir la definición; (c) juicio caso a caso. Debe redactarse la política completa, no solo la letra. `CONTINUIDAD.md` §9.19 abrevia (c) como «excluir»; este informe no lo resuelve.
2. Si (b): **política de arrendamientos**. Para que el motor A sea coherente, el perímetro debe excluir la amortización ROU (A1/A2) o el FCF base debe excluir el principal (A1′, que modifica C49).
3. Si (b): **política de intangibles adquiridos** (A1 frente a A2, o modelización explícita de adquisiciones). Requiere M2 y M3.
4. Si (b): **reinversión necesaria**: dato (M1) o estimación documentada con rango, evidencia operativa y responsable. Si no existe, se mantiene `pendiente_de_datos`.
5. **Perímetro de S2C** coherente con el anterior. El ancla C53 y las palancas deben declarar el mismo perímetro.
6. Observaciones de la plantilla fuera de F1 (§7 y §8): ventana del tipo impositivo y escala de intereses sin endeudamiento nuevo. Requieren revisión económica propia.

**Incertidumbres que no se pueden acotar con la base:** M1 y M2 (§6.4). La conclusión afectada, el nivel del flujo y del valor del motor A para Elis, **queda pendiente**.

---

## 11. Especificación propuesta y criterios de prueba

Ver [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md). Es una propuesta para que el frente técnico la implemente sobre una versión técnica fijada, después de la decisión F1. Incluye entradas nuevas de la Historia, parámetro declarado de perímetro, calibración de f y de S2C con ese perímetro, reglas de control, presentación del puente y criterios de prueba con valores de referencia de este informe.

## 12. Revisión independiente

Estado y documentos en [revision/](revision/). La revisión debe hacerla un agente distinto del autor, con contexto separado (Fable 5.2, esfuerzo máximo según el encargo). La configuración real que exponga el entorno se registra en [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md). Mientras no conste el informe del revisor con sus objeciones y respuestas, **la revisión independiente queda pendiente**.

## 13. Reproducción

Desde esta carpeta, con un árbol `munger_v2_r1` materializado (base 4.14 o hito 4.15; mismos binarios), Python 3.10+, pdftotext/pdfinfo (poppler) y openpyxl:

```bash
cd scripts
python3 -I verificar_cifras.py --raiz <ruta>/munger_v2_r1 --datos ../datos/cifras_fuente.csv --fuentes ../datos/fuentes.json --salida ../resultados/verificacion_cifras.json --exportar-paginas ../evidencias/paginas
python3 -I test_verificar_cifras.py --raiz <ruta>/munger_v2_r1
python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro <ruta>/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx --salida ../resultados/contraste_f1.json --informe ../resultados/contraste_f1.md
python3 -I tabla_conciliacion.py --cifras ../datos/cifras_fuente.csv --salida ../resultados/tabla_conciliacion.md
```

`especificacion_cifras.py` regenera el CSV desde los PDF y se detiene si una lectura del autor no coincide con el literal impreso.

**Lo que este informe no hace:** no valora la empresa, no emite precio objetivo ni recomendación, no cambia la plantilla, no regenera expedientes, no declara aptitud para dinero real y no sustituye la integración, réplica y auditoría del material final, que se comprobarán después.
