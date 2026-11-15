# VISCOFAN · informe del revisor independiente (entradas financieras, 4.14)

Revisor: R-Viscofan (Claude, contexto separado del extractor; no es una revisión humana). Fecha: 14-nov-2026.
Registro revisado: `R_viscofan/Viscofan/verificacion_entradas.json` (copia `cp -a` del expediente del extractor). Solo se ha escrito el bloque `comprobacion` (revisor, fecha, resultado, fuente_examinada, nota). Se comprobó por programa que ningún otro campo cambió (tampoco `incidencia` ni `comprobacion.extractor`). Scripts del revisor: `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/R_viscofan/rv_*.py`.

## 1. Método

- El revisor abrió las 59 páginas citadas, agrupadas por fuente y página. En cada una leyó la cabecera de columnas (qué año ocupa cada columna), la unidad («Thousands of euros» / «Miles de euros»), el signo y la fila de cada entrada. También contrastó cada cifra con su concepto (`uso`/`concepto`).
- Renderizó y miró cinco páginas del PDF:
  - CF_2021 p. 8, que tiene los rótulos desplazados en el propio PDF;
  - CA_2023 p. 8;
  - CF_2024 p. 9;
  - AR_2020 p. 7 (estado de cambios en el patrimonio);
  - el boletín de BME p. 3.
- Los PDF de las cuentas proceden de `trabajo_4_12/.../viscofan/fuentes/pdf/`. Sus sha256 coinciden con los registrados.
- Derivados: el revisor recalculó cada fórmula y comprobó que representa lo que pide la fila y que la serie es homogénea entre años.
- Leyó las notas de pensiones (AR_2020 p. 61, CF_2021 p. 49, CF_2022 p. 61, CA_2023 p. 45, CF_2024 p. 67, AR_2025 p. 87) y las de deuda (AR_2019 p. 86, AR_2025 p. 98).
- Revisó las fórmulas del libro que usan las filas 13, 14, 22 y 25, con openpyxl en solo lectura, para estimar los efectos.
- El informe del extractor se leyó al final.

## 2. Recuento (334 entradas: 232 celdas y 102 «aux:»)

| Resultado | Entradas |
|---|---|
| verificado | 315 (incluye 43 hipótesis o convenciones revisadas solo como clasificación) |
| discrepancia | 19 |
| pendiente | 0 |

## 3. Discrepancias

Valor del libro frente al valor correcto según la fuente, con su ubicación. Efecto respecto del valor ponderado del libro, 44,22 €/acción, y del puente del motor B, −279,94 mm.

| Celda | Libro | Correcto según la fuente | Efecto |
|---|---|---|---|
| Historia!L25 (pensiones 2025) | 20,989 | **14,878**: prestación definida, AR_2025 p. 87, nota 13, col. 2025. La línea del balance suma 6,111 de «Other staff remuneration» | Entra en el puente (Historia!C65). Resta 6,111 mm de más; corregido, el valor sube ≈ **+0,13 €/acción** (44,22 → ≈44,36) |
| Historia!K25 (2024) | 19,145 | 16,498 (AR_2025 p. 87; CF_2024 p. 67) | Solo historia |
| Historia!J25 (2023) | 25,916 | 17,266 (CF_2024 p. 67; CA_2023 p. 45) | Solo historia |
| Historia!H25 (2021) | 29,133 | 24,779 (CF_2022 p. 61; CF_2021 p. 49) | Solo historia |
| Historia!G25 (2020) | 37,871 | 28,204 (AR_2020 p. 61; CF_2021 p. 49) | Solo historia |
| Historia!F25 (2019) | 33,294 | 29,995 (AR_2020 p. 61; AR_2019 p. 76) | Solo historia |
| Análisis!C55 (acciones) | 45,479209 | **Concepto distinto**: es la media ponderada *diluida* de 2025 (AR_2025 p. 119), menor que la básica (45,656,226), lo que contradice la NIC 33. La fila pide las acciones en una fecha. La única cifra a una fecha que da el expediente: 46,500,000 (p. 76) − 506,601 propias (p. 83) = **45,993399** a 31-dic-2025. No consta la cifra al 3-nov-2026 | Con 45,993399: valor ponderado ≈ **43,73 €** (−0,49 €, −1,1 %); con L25 corregida, ≈43,86 €. Decisión VISCOFAN-ACCIONES pendiente |
| Análisis!C41 (capitalización) | 2.487,7 | 54,70 × 45,479209 = 2.487,713 (redondeo de −0,013, inmaterial). Hereda además el problema de C55: con 45,993399 sería **2.515,84** | +28,1 mm. Afecta al peso de la financiación en B y a Palancas C47; efecto en r no cuantificado |
| Análisis!C47 | 77,5 | 77,533 (media de J12:L12) | FCF base del libro +0,033 mm |
| Análisis!C48 | 8,3 | 8,294 | FCF base −0,006 mm |
| Análisis!C49 | 5,5 | 5,547 (pago total por arrendamientos; no separa principal) | FCF base +0,047 mm |
| Análisis!C50 | 3,71 | 3,707 | FCF base −0,003 mm. Neto de C47–C50: +0,071 mm, inmaterial, y solo en el motor A, que no es el elegido |
| Historia!F14 (circulante 2019) | −12,134 | −6,135 (sin provisiones; es el subtotal publicado en AR_2019 p. 12; AR_2020 p. 8) | Motor A y reinversión histórica |
| Historia!G14 (2020) | 19,349 | 25,178 (CF_2021 p. 8, col. 2020) | Ídem |
| Historia!J14 (2023) | 83,032 | 90,646 (CF_2024 p. 9, col. 2023) | Ídem |
| Historia!K14 (2024) | 15,452 | 8,862 (AR_2025 p. 27, col. 2024) | Ídem |
| Historia!L14 (2025) | 53,222 | 49,933 (AR_2025 p. 27, col. 2025) | Ídem. Neto: Historia!C76 baja −0,755 mm/año; S2C 2021–25 pasa de 1,146 a ≈1,155. Sin efecto directo en el valor del motor B |
| Historia!D22 (deuda 2017) | 82,794 | 93,698 = 93.722 − derivados 24 (IA_2018 p. 104), con el criterio de 2016 y 2018–2025 (incluye «Otros pasivos financieros») | Solo capital invertido y ROIC de 2017. El puente usa L22 |
| Historia!G13 (adquisiciones 2020) | vacía | 0 (AR_2020 p. 8: «-» con los rótulos bien alineados; CF_2021 p. 8 imprime 0 con los rótulos desplazados) | Nulo: el libro usa N(G13) y B59 suma H13:L13 |

Los efectos por acción son una aproximación lineal (valor total ≈ 44,22 × 45,479 = 2.011,2 mm). No se recalculó el libro.

## 4. Pendientes

Ninguna.

## 5. Incidencias de clasificación

No se encontró ningún dato publicado disfrazado de hipótesis o convención.

- **B11 (N1.tipo)**: está bien derivado (22,119 %, recalculado), pero contiene un juicio de normalización: quita solo las activaciones de bases negativas.
- **Ceros sin cifra impresa** (C23, D23, E23, H26, I26): son ceros inferidos, por la NIIF 16 no vigente o por la ausencia de la línea con cuadre aritmético. No son ceros publicados. El revisor los da por buenos y lo dice en la nota.

## 6. Las 18 diferencias del extractor

El revisor las confirma todas con su propia lectura:

- pensiones F25–H25 y J25–L25;
- circulante F14, G14 y J14–L14;
- D22;
- G13;
- redondeos C41 y C47–C50.

Discrepa de la clasificación del extractor en dos puntos:

1. **C55**: el extractor lo trata como observación. El revisor lo marca como discrepancia, por el concepto (media frente a fecha) y por la cifra incoherente.
2. **C41**: además del redondeo, hereda el problema de C55.

La ubicación correcta de G13 es AR_2020 p. 8. CF_2021 p. 8 tiene los rótulos desplazados en el propio PDF.

## 7. Análisis!C37 (precio)

Verificado. En el boletín de la Bolsa de Madrid del martes 03-nov-2026, p. 3 (texto y PDF renderizado, sha256 23335f63… igual al registrado), la fila «MC VIS VISCOFAN» da:

- Cierre (Closing): **54,7000**;
- Mínimo 54,50 y Máximo 55,30;
- CMP 54,8454.

Sin red, el revisor acredita el contenido del PDF conservado, no su descarga.

## 8. Comprobador (sobre la copia del revisor)

- universo 232; 102 auxiliares;
- **310 «comprobadas»**: la cifra incluye los «aux:», de ahí el texto «310 de 232»;
- 23 discrepancias;
- 1 pendiente (C41: su origen C55 está en discrepancia);
- 0 errores, 0 desactualizadas, 0 sin entrada, sobrantes o repetidas;
- 24 materiales sin comprobar;
- **apto_por_entradas = False**.

Las 23 discrepancias son las 18 del revisor (sin C41) más cinco automáticas: C23, D23, F26, G26 e I26, porque «la cita no contiene 0». El revisor las verificó: F26 y G26 imprimen «-», y C23, D23 e I26 son ceros por ausencia. Seguirán bloqueando mientras el contrato del comprobador no admita «-» ni los ceros inferidos.

El comprobador también deja pasar H26 por dígitos que no son el saldo: la cita es un movimiento («Transactions with non-controlling interests 0»).

## 9. Límites de la revisión

- No se rehízo la extracción del texto de todas las páginas desde el PDF. Solo se renderizaron las cinco de §1; el resto se leyó en el texto extraído, con alineación clara.
- No se comprobó la reexpresión por NIC 12 que el extractor cita (CF_2024 p. 25). Las cifras de 2022 usadas coinciden con las originales de CF_2022.
- Hipótesis y convenciones:
  - se revisaron solo como clasificación;
  - su valor no se juzga;
  - no se abrieron todas las páginas que cita su fundamento.
- Los efectos en €/acción son estimaciones lineales, sin recalcular el libro. El efecto de C41 en la r operativa no se cuantificó.
- No consta en el expediente el número de acciones a la fecha del precio (3-nov-2026).
