# Vidrala · contraste de los datos de 2023 y de los arrendamientos 2023–2025

**Fecha:** 8-nov-2026. **Paquete:** `munger_v2_r1`, entrega 4.2, construida sobre la 4.1. **Modelo:** Opus; Fable no se ha usado (motivo en `REGISTRO.md`).

**Alcance.** Este trabajo tiene dos objetivos acotados:
1. contrastar los cinco datos de 2023 que alimentan las medias de `Análisis` y el circulante de la ventana 2023–2025;
2. reunir evidencia sobre cómo se tratan los arrendamientos.

No se ha aplicado ninguna corrección, no se ha ejecutado `construir`, no se ha recalculado ningún libro y no se ha tocado ningún original, extracción, decisión, escenario ni código del sistema. Las réplicas aritméticas repiten las fórmulas del libro en memoria. **No son conclusiones de valoración.**

Este informe va acompañado de:
- `DOCUMENTOS_Y_FUENTES.md`;
- `ANEXO_REPRODUCIBLE.md`, que remite a `scripts/contraste_2023_arrendamientos.py`, con 45 comprobaciones;
- `PROPUESTAS_Y_PENDIENTES.md`;
- `REGISTRO.md`.

## 0. Comprobación inicial

- **Hecho.** El ZIP de la 4.1 tiene el SHA-256 `85198c54…806a8e213`, como indica el encargo.
- **Hecho.** Se revisaron `VERSION`, `REGISTRO_IMPLEMENTACION_H1-H3.md`, `REGISTRO_PILOTO.md` y el informe, el anexo, las fuentes y las propuestas de la 4.1.
- **Hecho.** La batería del piloto (35 comprobaciones) se reproduce sin diferencias, y los originales conservan su huella (verificación completa en `REGISTRO.md`).

## 1. Datos de 2023

| Partida (valor vigente, mm) | Resultado | Evidencia principal |
|---|---|---|
| **CFO 263,437** (Historia J11, media C46) | **Confirmado.** Mismo importe, signo, unidad (miles → mm) y ejercicio en el informe de 2023 y en el comparativo de 2024, en inglés y en español. En las dos presentaciones, beneficio + ajustes + circulante + intereses + impuestos da el total impreso | Inglés 2023 (doc. 1831) p. 7; inglés 2024 (doc. 2145) p. 7; español 2024 (doc. 2118) p. 14 |
| **Capex 151,700** (J12, media C47) | **Confirmado.** 143.848 + 7.852, que son pagos por adquisición de inmovilizado material e intangible (rótulo español). No hay cobros por ventas. Es el mismo en los dos informes | Las mismas páginas |
| **Aumento del circulante 78,805** (J14, entra en `f`) | **Pendiente.** La causa de la diferencia con 89,866 está documentada (ver abajo). El valor vigente reproduce fielmente el comparativo reexpresado, pero **no es solo variación del circulante**: incluye 11,061 de ajustes no monetarios de Italia trasladados a esa línea | Español 2024 p. 14 frente a inglés 2023 p. 7; nota de discontinuadas, inglés 2024 p. 35 |
| **Pago registrado como principal de arrendamientos 5,861** (J17, media C49) | **Confirmado como pago total** del pasivo por arrendamiento. **Discrepante con el rótulo «principal»** de la fila 17: el pago incluye intereses. El principal no está publicado | Nota 8: inglés 2023 p. 52, inglés 2024 p. 56, español 2024 p. 64 |
| **Interés devengado de arrendamientos 2,131** (aproximación heredada de C49) | **Confirmado como gasto devengado** («Accrued finance charges» y «Finance cost» de la nota 8). Su uso para obtener el principal sigue **sin acreditar** | Las mismas páginas |

**Recorrido.**
- Los cinco datos van de `AR_2024.json` («anterior», comparativo del informe siguiente) a `fase1_v63.json` y a Historia J11, J12, J14 y J17. `fase1_decisiones.json` no tiene ninguna decisión para ellos.
- C46 = 335,4 y C47 = 169,7 son las medias 2023–2025 de las filas 11 y 12.
- C49 = 4,5 procede de la herencia V5.3, no de la fila 17.

### Circulante de 2023: qué explica 89,866 frente a 78,805

**Hechos:**
- **El informe de 2023 cuadra.** Ajustes 169.475 y circulante −89.866 llevan a un CFO de 263.437.
- **El comparativo reexpresado del informe de 2024, en español (que prevalece), también cuadra.** Ajustes 158.414 y circulante −78.805 llevan al **mismo** CFO, 263.437.
- **Diferencias línea a línea en los ajustes** (reexpresado − original): amortización −10.655, deterioro −333, deudores −690, subvenciones +3.388, gastos financieros −3.486 e impuesto +715. Suman **−11.061**.
- **Compensación en el circulante.** «Otros activos y pasivos corrientes y no corrientes» pasa de +36.138 a +47.199, es decir, **+11.061**. Las otras cuatro líneas no cambian.
- **Coincidencia con la nota de Italia.** La nota 2(b) dice que el estado de flujos de 2023 se reexpresa por la venta del segmento de Italia. La cuenta de resultados de Italia en 2023 (p. 35) recoge amortización 10.655, deterioro 333, gasto financiero 3.486, impuesto +715 y otros ingresos 3.387, que coinciden con las diferencias anteriores. Las subvenciones difieren en 1 de los «otros ingresos» de Italia, sin explicación en el documento. Los 690 de deudores no tienen línea propia en esa nota.
- **Flujos de Italia en 2023:** explotación +26.732 e inversión −28.371. Ambos están dentro de los totales consolidados.

**Interpretación.**
- La reexpresión sacó del bloque de ajustes las partidas no monetarias de Italia, pero mantuvo el beneficio total, que incluye a Italia. Para que el CFO no cambiara, el importe se llevó a la línea «Otros activos y pasivos…».
- En consecuencia, 78,805 no mide solo la variación del circulante, y 89,866 sí lo hace pero con el perímetro que incluye a Italia.
- El documento no publica la variación del circulante solo de las operaciones continuadas.

**Discrepancia de traducción.** En el informe inglés de 2024, la columna de 2023 reexpresada no cuadra: sus ajustes suman 130.444 frente a 158.414. Tres líneas (provisiones, subvenciones y gastos financieros) repiten las cifras de 2022 del informe de 2023. La versión española, que prevalece, es correcta.

**Perímetro de la columna 2023 de la Historia** (interpretación con base en hechos). La Historia mezcla dos perímetros:
- ventas, EBIT y D&A de 2023 vienen del comparativo reexpresado, solo con operaciones continuadas (D&A 87,21 frente a 97,865 del informe de 2023);
- CFO y capex incluyen a Italia;
- el circulante incluye la reclasificación de 11,061.

Esto afecta a `f` por canales distintos (corregido en la entrega 4.3; antes decía «NOPAT medio y reinversión media de C75 y C76», como si D&A afectara al NOPAT): las ventas, a las ventas medias (C74); el EBIT y el tipo, al NOPAT (C75 = media de EBIT × (1 − t)); D&A, capex y circulante, a la reinversión (C76); CFO y capex, al FCF base (C46, C47 → C70). Es materia de la revisión financiera (`contrastes/vidrala_revision_financiera/`).

## 2. Arrendamientos 2023–2025

| Año | Pago total (nota 8) | Interés devengado | Movimiento del pasivo |
|---|---|---|---|
| 2023 | 5.861 | 2.131 | cuadra (2.346 + 46.123 + 643 + 2.131 − 5.861 = 45.382) |
| 2024 | 6.117 | 2.179 | cuadra |
| 2025 | 8.314 | 2.452 | cuadra |

| Pregunta | Respuesta y evidencia | Estado |
|---|---|---|
| ¿Los pagos del movimiento del pasivo permiten identificar el principal? | **No.** El movimiento suma el gasto devengado aparte y resta el pago, así que el pago incluye intereses. No se publica el principal ni el interés pagado | No acreditado |
| ¿El interés pagado coincide con el devengado? | **No hay evidencia directa.** Indicio (interpretación): el arrendamiento principal, Bristol, se paga en cuotas mensuales al 5 % (466 miles € al mes según el informe de 2024; 554 en 2025), lo que hace pensar que el interés se liquida dentro del año | No acreditado |
| ¿Los intereses de arrendamientos están dentro de los intereses pagados de explotación? | **No consta.** Las notas no lo dicen. El ESEF 2025 etiqueta el total de «Pagos de intereses» como `InterestPaidClassifiedAsOperatingActivities`, sin desglose | No determinable |
| ¿Dónde está el principal en el estado de flujos? | **No hay línea propia** en ningún año, y el ESEF no tiene ninguna etiqueta de arrendamientos. En 2024 y 2025, los flujos de deuda del estado de flujos (−205.736 y −130.399) igualan **la variación total del saldo** de la nota 16, que incluye los arrendamientos y sus movimientos no monetarios. En 2023 no ocurre así (107.377 frente a 275.495) | No determinable. Hay indicios de que van dentro de las líneas de deuda |
| ¿La deducción de C49 podría duplicar un pago ya incluido en el CFO? | **Sí, en dos escenarios no descartables:** (a) si el interés de arrendamientos está en «Interest paid», restar el pago total lo duplica; C49 = 4,5 lo evita solo si el pagado es igual al devengado; (b) si 8.314, 6.117 y 5.861 fueran en realidad gastos de arrendamientos a corto plazo (operativos, ya dentro del CFO), cualquier deducción en C49 los duplicaría | No determinable |
| ¿Hay explicación documentada de la repetición de importes? | **No.** La repetición es **sistemática:** en 2022, 2023, 2024 y 2025 (613, 5.861, 6.117 y 8.314), en inglés y en español. Interpretación: es probablemente un error de redacción de la tabla de resultados de la nota 8. Lo apoyan dos cosas: el movimiento del pasivo cuadra cada año, y las cuotas de Bristol (466 × 12 = 5.592 en 2024; 554 × 12 = 6.648 en 2025) son coherentes en magnitud con los pagos. No es prueba | No resuelto |

**Resultado: pendiente.** Ni el principal, ni el interés pagado, ni la clasificación de los pagos de arrendamientos están acreditados.

**Discrepancia documental adicional.** El informe de 2025 atribuye a 2024 una cuota de Bristol de 354 miles £; el de 2024 decía 387.

## 3. Réplicas aritméticas (sin recalcular el libro)

- **Entradas constantes:** ventas, EBIT, tipo y D&A de 2023–2025, capex y la ventana C57 = 3.
- **Entrada que cambia:** solo la indicada en cada fila.

| Escenario del circulante (2023; 2024) | C76 reinversión media | C79 fugas | `f` |
|---|---|---|---|
| Libro (78,805; −127,840) | 40,430 | 29,709 | 0,019890 |
| 78,805; 84,994 (corrección respaldada de 2024) | 111,375 | −41,236 | −0,027608 |
| 89,866; 84,994 | 115,062 | −44,923 | −0,030076 |
| 89,866; −127,840 | 44,117 | 26,022 | 0,017422 |

- **Medias de CFO y capex (C46 y C47):** no cambian. Sus datos de 2023 se confirman.
- **C49 (sensibilidad condicionada, no límites).**
  - Con 4,5: FCF base 161,2.
  - Con 6,8, si el pago total queda fuera del CFO: 158,9.
  - Con 0, si los pagos ya estuvieran en el CFO: 165,7.
  - Ninguno de los tres valores está acreditado.
- **Interpretación.** El circulante de 2023 desplaza `f` unas 0,0025 en cualquiera de los dos casos del de 2024. El signo de `f` lo decide sobre todo la corrección de 2024.

## 4. Qué queda preparado para la revisión financiera y qué sigue abierto

**Preparado (hechos con fuente).**
- CFO y capex de 2023 confirmados.
- La causa de la diferencia del circulante de 2023, documentada línea a línea.
- La columna española de 2023, que cuadra, y el error de la inglesa.
- Los flujos de Italia en 2023.
- Pagos y devengos de arrendamientos de 2022 a 2025, con sus movimientos cuadrados.
- La ausencia de etiquetas y líneas de arrendamientos.
- El resultado de las réplicas.

**Abierto:**
- qué valor de circulante de 2023 representa la variación del circulante con el perímetro de la ventana; el documento no publica la de las operaciones continuadas;
- la coherencia de perímetro de la columna 2023 (continuadas frente a consolidado) y su efecto en `f`;
- el principal, el interés pagado y la clasificación de los arrendamientos;
- ventas, EBIT y tipo de 2023, que no se han contrastado en este encargo;
- la conveniencia de proyectar una `f` negativa, que corresponde a la persona responsable.
