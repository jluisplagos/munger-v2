# F1 · inicio de conciliación económica de Elis (solo lectura)

Fecha: 15-nov-2026. **F1 sigue abierto.** Están comprobadas las cifras de ROU, intangibles adquiridos y pagos de arrendamientos y está localizado su recorrido por el libro. Eso prueba una diferencia de perímetros que merece conciliación; **no prueba por sí solo un doble cómputo económico definitivo**. No se propone una corrección de fórmulas ni un precio objetivo.

## Base, alcance y evidencia reproducible

Se leyó la copia completa inmutable 4.14 y se contrastó el libro correspondiente del Hito1 4.15 recibido. No se accedió al trabajo vivo de Claude, no se ejecutaron pipelines ni LibreOffice y no se guardó ningún libro.

Ruta abreviada `CASO`: `/workspace/work/revision414_runtime/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/`.

Libro: `CASO/Elis_v63_evaluada.xlsx`. SHA256 `d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385`. El libro equivalente de `/workspace/work/revision415_runtime/…/elis_decisiones/Elis/` tiene exactamente ese mismo SHA256. Esta comparación no identifica ni valida los cambios posteriores sin commit de Claude.

Fuentes primarias usadas, disponibles en el caso hermano `elis_motor_A/Elis/fuentes_pdf/`:

- `Elis - 2025 Universal Registration Document.pdf`, SHA256 `04bfd08724e768804e7110093d3ec2cf017a7e7fe2983bacd75656d3a95cd62e`.
- `Elis_Document d'enregistrement universel_2024_FR.pdf`, SHA256 `94e994f0de79cc588240f9866d263c4a5ae27fe3ccff83bc0b817eb91633c1e9`.

Todas las páginas citadas abajo son **páginas PDF**, no la numeración impresa. Se volvieron a extraer directamente de los PDF con `pdftotext`; no se confió solo en los textos heredados. Evidencia adjunta: `f1_fuentes_primarias.txt` (páginas pertinentes) y `f1_evidencias.json` (rutas, huellas, fórmulas leídas, cachés y tratamiento registrado de C47/C48). La réplica previa `revision414_financiera_A.json` se toma únicamente como comprobación matemática: declara `economic_F1_correction_validated=false`.

## Hechos comprobados y celdas implicadas

Millones de euros; ejercicio 2025 salvo indicación.

| Componente | Fuente primaria | Entrada / recorrido del libro | Qué queda probado |
|---|---|---|---|
| EBIT publicado 629,9; BAI 492,9; financiero 137,1 | URD2025 pp.324 y345 | `Historia!L7=630`; `L29=L7/L6`; `C48` margen último año | La Historia reconstruye 630,0 por BAI+financiero; diferencia de redondeo de 0,1 frente al EBIT impreso. No es el EBIT ajustado766,6. |
| D&A total neta de subvenciones1.019,4 | p.350, nota4.5 | `Historia!L8=1019,4`; entra en `L30`, `L31`, `C53` y `C58` | Incluye ROU149,5 e intangibles de combinaciones85,7, además de textil565,1, otros artículos36,3 y demás PP&E/intangibles183,6; subvenciones−1,0 y deterioro0,1. |
| CFO1.510,6 | p.327 | `Historia!L11`; `Análisis!C46=1429,433`, media2023–25 | Ya incluye impuestos de caja146,7 y cambios de circulante. Intereses financieros y pagos lease se presentan en financiación. |
| Capex bruto890,2 | p.327: intangibles26,2 + PP&E864,0 | `Historia!L12=890,2`; `L30=L12−L8+L14` | El capex de la Historia es bruto y no lleva altas ROU. |
| Capex neto874,7 | p.314 | `Análisis!C47=857,167`, media2023–25 de820,8/876,0/874,7 | La base FCF usa el «Net capex» publicado. No coincide con el capex bruto que calibra la reinversión histórica. El registro conserva el redondeo publicado2023:820,8 frente a820,7 derivado de líneas. |
| Pagos lease177,9 | p.327 | Su principal entra por `Historia!L17=148,3`; intereses implícitos entran en `Análisis!C48` | El pago completo no está incluido en el CFO. |
| Principal lease148,3; deuda lease703,2 | p.366, nota6.3 | `Historia!L17=148,3`; `L23=703,2`; `L32` incluye L23 | ROU amortizado149,5 es un concepto distinto del principal pagado148,3. Nuevos ROU183,9 y reestimaciones50,0 no son capex de caja. |
| Intereses financieros netos99,4 | p.327 | `Historia!L15=L16=99,4`; base `Análisis!C48=108` | Los99,4 excluyen intereses de leases, que van dentro de177,9. **Mantener C48=108 según el tratamiento registrado.** |
| Deuda financiera3.418,3; caja398,1 | pp.384 y327 | `Historia!L22`, `L24`; deuda lease separada en L23 | La deuda financiera excluye703,2 de lease. Su tratamiento debe ser coherente con el flujo al accionista y el régimen de deuda constante. |
| Compras de negocios117,6 | p.327 | `Historia!L13`; `L31=L30+L13` | No es capex propio ni alta ROU; sí afecta la reinversión total y el S2C histórico. |

**C48 no es una incidencia:** el registro `datos_v63.json → control_maestro.filas.45.N` documenta108,0 =82,933 de intereses financieros netos medios2023–25 +25,067 de intereses lease implícitos medios. Estos últimos son la diferencia entre pagos completos y principal:19,8/25,8/29,6. Los pagos2023 se contrastaron con URD2024 p.273 y el principal111,0 con p.312. Por tanto C48 junto con C49=128,1 resta el pago completo medio de leases153,167 y los intereses financieros82,933. Sustituir108 por82,933 dejaría sin restar25,067.

En2025,177,9−148,3=29,6 de interés lease implícito de caja. El gasto devengado publicado es29,2 (URD2025 p.379, nota8.2). La diferencia0,4 requiere puente de caja/devengo; no deben intercambiarse los dos datos.

**Lino propio y ROU son bloques distintos:** la nota6.4 p.367 activa artículos propios destinados a alquiler y los amortiza entre18meses y5años; sus compras están en PP&E. La nota6.3 trata activos arrendados por Elis. No debe reclasificarse el lino como ROU.

## El punto exacto que debe conciliar F1

La lectura de la fórmula de `Historia!C58` da, sin sus guardas de integridad:

`f = {media[EBIT×(1−tipo) − (capex bruto − D&A total + aumento WC)] − FCFbase} / ventas medias`.

La ventana es **2023–25** (`Historia!C57=3`, columnas J:L), mientras que el tipo proyectado de `Historia!C52=28,82%` es la media2021–25. `Historia!C70` toma `Análisis!C52=307,933`, construido como:

`1429,433 − 857,167 − 108 − 128,1 − 28,233 = 307,933`.

En las filas de Motor A, `Motor!L6=Historia!C58` y `K6` recoge el tipo. El flujo anual (`AU6` en año1, hasta `BD6`) tiene la estructura `ventas×[margen EBIT×(1−tipo)−f]−aumento ventas/S2C`. El terminal `BF6` conserva la fuga `f`. Por tanto la discrepancia de perímetros puede propagarse por todo el horizonte; que la fórmula se reproduzca no valida su interpretación económica.

Un control algebraico ya concreto, **sin cambiar datos ni valorar la empresa**, es:

- Ventas medias2023–25:4.559,9667; NOPAT histórico medio calculado con el tipo de cada año:416,79905.
- Reinversión orgánica media que usa C58: `867,1667−953,9667+5,6 = −81,2`.
- Flujo histórico anterior a f:497,99905; `f=0,04168145527`; fuga monetaria media190,06605.
- Identidad resultante: `NOPATmedio−f×ventasmedias =226,733 =FCFbase307,933+(−81,2)`.

Esto demuestra que el término de caja antes del crecimiento del motor, evaluado con esas medias, **no coincide automáticamente con el FCF ancla**. Es una identidad de las entradas actuales, no una prueba suficiente de error ni el flujo de un escenario real. El−81,2 combina D&A, capex y WC: no puede atribuirse íntegramente a ROU149,5 o a intangibles85,7 de un solo año. También cambian las bases fiscal, temporal, bruta/neta y de margen.

Además, la fila `Historia!35` usa `CFO−capex bruto−interés financiero−principal lease−SBC`. En2025 da338,0. El FCF de caja con capex neto y pago completo lease da323,9: `1510,6−874,7−99,4−177,9−34,7`. La diferencia14,1 se explica exactamente por `−15,5` de capex bruto/neto y `+29,6` de interés lease omitido en la fila35. **No comparar la fila35 con el ancla como si sus definiciones fueran iguales.** Tampoco implica que C48 sea incorrecta.

## Qué encargar ahora, separado de R415-SIGNO / U2–U5 / I20

Encargo económico F1, cerrado a Elis base31-dic-2025, ventana2023–25, con anexo2021–25 para S2C y reinversión. Entregable: una tabla de conciliación anual con fuente/página, definición, caja/devengo, impuestos, signo y destino en el libro; residuo cuantificado y explicado. Sin cambios de fórmula hasta cerrar el puente.

1. **EBIT→caja operativa:** partir del EBIT publicado y reconciliar D&A por bloques, SBC, provisiones, plusvalías, earnouts y otros ajustes hasta CFO. En2025 el estado de flujos parte de resultado366,6, impuesto126,2 y financiero137,1; imprime caja antes de finanzas e impuestos1.661,3, circulante−4,0 e impuestos de caja−146,7 para llegar a1.510,6. Las sumas con cifras impresas presentan redondeos de0,1. No sustituir D&A1.019,4 por D&A+provisiones1.020,8 sin puente.
2. **Fiscal:** explicar uso de tipo sobre EBIT frente a impuestos corrientes/diferidos y caja; separar escudo financiero, diferencias permanentes, CVAE y extraordinarios. No dar por equivalente126,2 de gasto a146,7 de caja. Los ajustes a la amortización adquirida o ROU deben llevar su tratamiento fiscal explícito.
3. **Lease:** escoger y justificar un tratamiento económico coherente para ROU, pagos/principal/interés, altas/reestimaciones y deuda. Mantener separadas altas no monetarias y pagos. Demostrar que una única obligación económica queda recogida una vez entre EBIT, reinversión, f y deuda.
4. **Intangibles adquiridos:** reconciliar85,7 de amortización con la política de adquisiciones, altas y posible reposición económica de cartera. Que la amortización no sea salida de caja no demuestra que el negocio conserve clientes gratuitamente ni que toda compra futura sea crecimiento. Distinguir consolidación adquirida de crecimiento orgánico.
5. **Reinversión:** reconciliar capex bruto/neto, cobros de activos/subvenciones, lino propio, resto PP&E/intangibles, altas ROU y compras de negocios. Determinar qué repone capacidad/clientes y qué añade crecimiento; alinear ese perímetro con S2C y con el margen de partida. Mantener separadas la falta de desglose y una eventual corrección del ancla.
6. **Financiación y accionista:** comprobar que el flujo después de intereses supone deuda constante y qué ocurre con principal financiero, leases, OCEANE, caja, SBC y acciones. Conservar el tratamiento registrado de C48 y de la OCEANE; cualquier alternativa debe mostrar el puente completo de numerador y denominador.

## Hipótesis y datos todavía faltantes

- **Hipótesis por probar:** f más EBIT proyectado puede volver a cargar el coste económico de leases o de intangibles adquiridos. Las cifras y el recorrido existen; la duplicación y su importe neto no están demostrados. Las afirmaciones definitivas heredadas en `elis_motor_A/Elis/celdas_C.json` no sustituyen ese puente.
- **Dato no identificado en las páginas revisadas:** desglose cuantitativo de capex entre mantenimiento y crecimiento, por bloque y año. URD2025 p.312 dice expresamente que la inversión industrial cubre ambos y que una parte grande del lino corresponde a dotar clientes nuevos; no asigna importes. Eso no autoriza un porcentaje estimado como hecho ni prueba que el dato no exista en otra comunicación.
- Faltan el puente íntegro2023–25 de impuestos y partidas no monetarias, el residuo caja/devengo de leases, y una regla verificable de reinversión para mantener cartera y capacidad. Si no hay desglose publicado, hace falta estimación documentada con rango, evidencia operacional y responsable; la incertidumbre debe conservarse.
- El inicio permite abrir el encargo anterior de inmediato y mantener los controles técnicos en paralelo. **No habilita inversión con dinero real, modificación del libro ni una conclusión económica definitiva de F1.**
