# Informe financiero de la entrega 4.10 · Vidrala: N4 revisada, P3, N5–N8 y N10

**Qué es.** La parte financiera del encargo 4.10 (§4 y §5). Todo se ha calculado sobre copias identificadas del libro de referencia (`…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/Vidrala_v63_evaluada.xlsx`, que no se modifica). Ninguna convención se adopta: las alternativas van a la propuesta única (`propuestas/PROPUESTA_DECISIONES_4_10.md`) y los campos humanos quedan vacíos.

**Convenciones de lectura.**
- **[Dato]** es una cifra publicada, con su fuente.
- **[Derivación]** es un cálculo hecho con datos.
- **[Hipótesis]** es un supuesto, que no es una cota ni una convención adoptada.

**Unidades.** Las cifras van en millones de euros (mm) salvo que se diga otra cosa. Las fuentes publican en miles de euros, con perímetro consolidado y moneda EUR (los saldos de Encirc están convertidos desde la libra).

**Fuente principal: ES 2025.** Es la versión española de la información financiera consolidada de 2025, `contrastes/piloto_Vidrala_2025/fuentes/es_2308_descarga_2026-11-08/2308_es-informacion_financiera_consolidada_2025.pdf`:
- SHA-256 `29fd6a299d37270279195e8eb194820869a1bb2c513dd6a646963034698f14e7`;
- 372 páginas, descargada el 8-nov-2026;
- en la memoria, la página impresa es la página del PDF − 8.

Se prioriza la versión española. Donde la inglesa o el ESEF difieren, se dice.

**Referencia mecánica heredada, reproducida.** r = 0,09; probabilidades 0,2 / 0,6 / 0,2; k = 3 (experimental); caja 108,352; puente 160,784; N = 35,206.

| | MALO | NORMAL | BUENO | Ponderado | Precio de Sí |
|---|---|---|---|---|---|
| Valor (€/acción) | 53,670420 | 70,772197 | 86,488762 | 70,495154 | 65,688087 |

La copia sin cambios lo reproduce dentro de 5·10⁻⁷ (`variantes/variantes_4_10.json` → `identidades.base_reproduce_la_referencia`).

## 1. N4 revisada (§4.1 y §4.2)

**Otros activos financieros (10 entradas auxiliares).**
- **[Dato] La especificación vigente** tiene dos textos:
  - `prompts/historia_anio.md` dice «activos financieros corrientes que no son caja (depósitos a plazo, inversiones financieras temporales)»;
  - `prompts/metadatos_fase1.md` admite sumarlos a la caja «solo si la empresa mantiene una parte material de su liquidez en depósitos a plazo u otras inversiones financieras corrientes líquidas».
- **[Dato] El balance español de 2025** (ES 2025, pág. PDF 9, impresa 1) muestra instrumentos financieros derivados corrientes de 1,157 (2025) y 25,567 (2024).
- **[Dato] Los cuadres de la 4.9** dan derivados corrientes en 9 de los 10 años:

  | Año | 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
  |---|---|---|---|---|---|---|---|---|---|---|
  | Derivados corrientes | 2,777 | 3,568 | 8,623 | 5,646 | 1,378 | 24,010 | 1,114 | 0 | 25,567 | 1,157 |

  Ningún año tiene una línea de depósitos ni de inversiones financieras temporales.
- **[Interpretación] El cuadre prueba la ausencia de depósitos e inversiones temporales, no el cero de la categoría amplia.** La lectura literal («activos financieros corrientes que no son caja») incluiría los derivados e incluso, en sentido estricto de la NIIF 9, los deudores comerciales. Eso muestra que la intención de la especificación es la liquidez distinta del efectivo.
- **Definición explícita con la que se clasifica (lectura estrecha, propuesta como D-N4-OAF):**
  - incluye los depósitos a plazo y las inversiones financieras temporales líquidas que no sean equivalentes de efectivo;
  - excluye los derivados (su valor razonable no es liquidez del accionista, revierte con la partida cubierta y tiene contrapartida en pasivos derivados de 1,235 corrientes y 6,938 no corrientes en 2025, y en la reserva de coberturas), los deudores, los impuestos, otros activos operativos y los activos financieros no corrientes;
  - razón económica: la partida solo tiene sentido como ampliación posible de la caja.
- **Límite:** la composición de «Otros activos corrientes» (nota 13) solo se ha comprobado en 2024–2025 (IVA y otros conceptos); en 2016–2023 la clasificación se apoya en el rótulo de la línea.
- **No se redefine para conservar el cero ni se suma nada a la caja.** La referencia mantiene `caja_incluye_otros_activos_financieros = false`, así que la partida no tiene efecto en la valoración con ninguna de las dos lecturas.

**Reservas, no aplicabilidad y recuento revisado.**

| Evidencia | Entradas | Cuáles |
|---|---|---|
| Completa | 18 | adquisiciones 2018–2022 (5), minoritarios 2016–2025 (10), intereses en financiación 2016–2017 (2), otros activos financieros 2023 (1, cero con las dos lecturas) |
| Parcial | 8 | intereses en financiación 2018–2025: el componente de deuda está acreditado (se paga en explotación); el de arrendamientos no lo está (no se publica en qué línea de flujos se pagan; NIC 17 financiero en 2018) |
| Depende de la definición | 9 | otros activos financieros 2016–2022 y 2024–2025: cero con la lectura estrecha; con la amplia, los derivados de la tabla |
| No aplicable | 3 | NIIF 16 en 2016 (principal y pasivo) y principal de 2018. No son ceros publicados; el de 2018 depende de la regla que lleva el arrendamiento financiero NIC 17 a deuda, escrita en `fase1_decisiones.json` sin fecha ni firma, que no se atribuye a ninguna persona |

- **El total sigue siendo 38.** Los «35 respaldados» de la 4.9 no eran una cuota: ahora son 18 completas, 8 parciales y 9 dependientes de una definición.
- **Ninguna está confirmada:** los campos humanos están vacíos. Una firma no sustituye el dato que falta en las 8 parciales.
- **Dependencia.** Las 28 entradas con fila alimentan Historia C5:L26; las 10 auxiliares quedan fuera mientras no entren en la caja.
- **Archivos:** `n4/matriz_n4_4_10.json` y `.csv`, generados por `scripts/n4_revision.py` a partir de la matriz de la 4.9, que no se reescribe.

## 2. CFO, C48 y C49 conjuntamente (P3, §4.3)

**[Dato] Movimiento del pasivo por arrendamiento (nota 8):**

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Pagos totales (P+I) | 5,861 | 6,117 | 8,314 |
| Gasto financiero devengado | 2,131 | 2,179 | 2,452 |

- Fuente de 2025: ES 2025, pág. PDF 58 (impresa 50). Las de 2023 y 2024 son las de la 4.2.
- **[Dato] El estado de flujos de 2025** (pág. PDF 14, impresa 6):
  - en explotación tiene «Pagos de intereses (20.800)»;
  - en financiación no tiene ninguna línea de arrendamientos. Los pagos de arrendamientos están dentro de otras líneas de deuda; la nota 14(k), pág. PDF 68, dice que la NIIF 16 «supone un aumento de 49 millones de euros en el epígrafe "Deudas con entidades de crédito"».
- **[Derivación] Medias de 2023–2025:**
  - P+I = 6,764;
  - I = 2,254;
  - P = 4,510 (solo si el interés pagado es igual al devengado), que coincide con C49 = 4,5 de la referencia.
- **Lo desconocido, exactamente:**
  - en qué línea del estado de flujos se paga el interés de los arrendamientos (en «Pagos de intereses» de explotación o en financiación, junto con el principal);
  - si el interés pagado es igual al devengado.

  Es la pregunta Q-N4a, que no se envía.

**Las tres situaciones:**

| Situación | Representación | Resultado |
|---|---|---|
| A · I dentro del CFO | C48 = 0 y C49 = P | Es la referencia. C49 = P+I restaría I dos veces, aunque C48 = 0 |
| B · I en financiación | C48 = I y C49 = P, o C48 = 0 y C49 = P+I | Las dos representaciones dan una única resta equivalente. En las variantes, C48 = 2,254 con C49 = 4,5, frente a C48 = 0 con C49 = 4,5 + 2,254 = 6,754; con P = 4,510, P+I sería 6,764, y la diferencia de 0,010 es el redondeo de C49 = 4,5: FCF base 158,946 (−2,254) y `f` −0,026099 (−0,027608 en la referencia). La comprobación aparte da el mismo FCF, la misma `f` y la misma valoración (`P3_B1_igual_B2`) |
| Sin acreditar | — | Se conservan A y B como alternativas condicionadas |

- **Efecto en la valoración del motor B: nulo** en los tres escenarios, el ponderado y el precio de Sí. Cambian el FCF base y `f`, que sigue negativa («⚠ REVISAR»).
- **Los intereses de deuda pagados en explotación de 2023–2025** (media 21,740) ya están en el CFO y no se añaden a C48 (contraejemplo de doble cómputo de la 4.9).
- **Ni 4,5 ni 6,764 se adoptan** como solución de C49. Los 2,254 son devengos usados como hipótesis.
- **La discrepancia de la nota 8 sigue visible.** «Gastos relacionados con arrendamientos corrientes y de poco valor» repite exactamente los pagos (8,314 y 6,117; ES 2025, pág. PDF 58). Está registrada desde la 4.2 y sigue sin resolverse documentalmente.

## 3. N5 · pensiones y obligaciones de personal

- **[Dato] Provisión «Personal»:** 6,223 a 31-dic-2025 y 6,053 a 31-dic-2024 (nota 19, ES 2025, pág. PDF 77, impresa 69).
  - Recoge «planes de prestaciones definidas y otras obligaciones con empleados» (pág. PDF 78).
  - El plan de prestación definida es el británico de Encirc (pensión y cobertura médica posterior a la jubilación). Lo valora un actuario independiente según la NIC 19.
  - La pérdida actuarial en el otro resultado global fue de −0,163 en 2025 y −0,241 en 2024 (nota 14(m)(ii), pág. PDF 70).
- **[Dato] No se publican por separado** la obligación por prestaciones definidas, los activos del plan, el déficit o superávit neto ni las otras obligaciones: tampoco en la versión inglesa, y el ESEF solo trae un bloque de texto, sin cifras etiquetadas.
- **[Interpretación] Qué es el 6,223 de L25.** Es el pasivo neto reconocido, antes de impuestos: el déficit del plan, si no hay límite del activo, más otras obligaciones. «Déficit neto de pensiones» describe una parte, no el total.
- **En el puente** entra como max(0; L25); con un superávit, el puente no lo sumaría como caja.
- **No hay doble cómputo con la deuda:** D = 262,913 son los pasivos financieros, y las provisiones son otra línea del balance (64,180 en total, de los que 46,366 son derechos de emisión).
- **En los flujos,** las aportaciones al plan van en explotación (gasto de personal), así que el stock se resta una vez.
- **Alternativas** (no se pone 0 por falta de desglose):

  | Alternativa | Qué supone | Efecto |
  |---|---|---|
  | Referencia | 6,223 bruto | — |
  | [Hipótesis] neto de un impuesto del 25 % (tipo general británico) | 4,667 | +0,0442 €/acción en todos los valores (identidad ΔV = −ΔL25/N comprobada) |
  | Solo el componente de prestación definida | No separable con las fuentes publicadas | Condicionado; no se calcula |

## 4. N6 · fecha de E y tasa operativa

- **r = 0,09 se conserva.** La fórmula de r_op, Diagnóstico V6!C15, se ha comprobado aparte en cuatro variantes con 10⁻¹² de error: r_op = (r·E + i·(1−τ)·D)/(E+D).
- **D** = 262,913: pasivos financieros corrientes y no corrientes a 31-dic-2025 (196,080 + 66,833), con 49,3 de arrendamientos NIIF 16 (balance, pág. PDF 10).
- **i** = 0,063393: intereses pagados de 2025 (20,8) ÷ la media de deuda más arrendamientos de 2024 y 2025 ((393,312 + 262,913)/2).
- **τ** = 0,20032: media del tipo efectivo de 2021 a 2025 (Historia H10:L10).
- **[Dato] Precio de cierre de 2025:** 90,10 €, con «una capitalización bursátil de 3.172 millones de euros» sobre las acciones emitidas (Informe de gestión de 2025, «Evolución bursátil», ES 2025, pág. PDF 97).
  - Es la base corporativa de 31-dic-2025, sin ajuste por la ampliación liberada de 2026.
  - **Límite:** el dato procede del informe financiero anual que la empresa deposita en la CNMV; no se ha contrastado con el boletín de cotización de BME, que no se encontró en una búsqueda web.
- **La referencia mezcla fechas:** E = 87,90 (3-nov-2026) × 35,206 = 3.094,6.

| Variante | E | r_op | Ponderado | Precio de Sí | Efecto en el ponderado |
|---|---|---|---|---|---|
| N6, solo la fecha de E | 90,10 × 35,206258 = 3.172,084 | 0,086992 (+0,000070) | 70,418140 | 65,619563 | −0,077 |
| [Alternativa estructural] τ del escudo = tipo efectivo de 2025 (0,2433) | como N6 | 0,086783 | 70,649950 | 65,825805 | +0,232 respecto a N6 |

- La alternativa de τ no es representable con celdas de valor, porque la plantilla usa el mismo τ en el motor y en r_op. Se sustituye la fórmula de C15 en una copia que no es íntegra.
- **No se ha adoptado** T1 ni T2, ni ninguna estimación WACC.
- **g < r_op se cumple** en todas las variantes (el g máximo es 0,025).

## 5. N7 · acciones

- **[Dato] Emitidas a 31-dic-2025:** 35.206.258 (nota 14(k), ES 2025, pág. PDF 67, impresa 59), tras la ampliación liberada 1×20 ejecutada el 23-oct-2025.
- **[Dato] Autocartera:** 23.400 acciones (2,097 de coste).
- **[Derivación] En circulación:** 35.182.858.
  - Lo confirma un dato independiente: el dividendo a cuenta de 43.338.244,48 € (propuesta de distribución, pág. PDF 71) ÷ 1,2318 € = 35.182.858.
- **[Dato] Medias anuales, que son otro concepto:** promedio ponderado básico de 35.206 miles (pág. PDF 82). La versión inglesa da 35.205.947. No hay instrumentos dilutivos.
- **No se mezclan** la liberada ni la autocartera de 2026.

| Variante | Qué cambia | Efecto en el ponderado | Comprobación |
|---|---|---|---|
| Efecto puro del denominador | N = 35,182858 con E fija | +0,0463 | V·N/N' comprobada aparte |
| Efecto conjunto | N y E = 90,10 × 35,182858 = 3.169,976 | −0,0287 frente a la referencia | — |

## 6. N8 · derecho al dividendo a cuenta

**Conciliación caja / obligación / distribución, registrada una sola vez.**
- **[Dato] Acuerdo y pago:** el Consejo del 19-dic-2025 acordó 1,2318 € por acción, 43,338 en total, pagados el 13-feb-2026 (nota 14(n), pág. PDF 70).
- **[Dato] Obligación:** a 31-dic-2025 figura como pasivo, «Accionistas por dividendos» 43,338 (nota 17, pág. PDF 76), y está restado del patrimonio.
- **[Interpretación] Caja:** la caja de 108,352 todavía lo contiene.
- **Valoración con derecho** (la referencia): caja 108,352 y puente 160,784, sin tocar.
- **Valoración sin derecho:** la obligación se resta una vez en el puente.
  - En la copia, el vehículo es `Historia!L26`, una celda de valor que en la valoración solo entra por el puente. Mueve además los múltiplos informativos EV/ventas y EV/EBITDA de Diagnóstico V6, que no intervienen en los valores. No son minoritarios: los minoritarios siguen en 0.
  - Valoración operativa, E, r_op, escenarios y N quedan fijos.
  - [Comprobado aparte] V_sin_derecho = V_con_derecho − 43,338/35,206 = −1,230983 €/acción en los tres escenarios, el ponderado y el precio de Sí. El precio de Sí es una media ponderada por tramos, así que se desplaza igual.
- **[Dato] El complementario no se resta en ninguna variante:** 16.490.205,54 € (≈ 0,4687 € por acción en circulación; pág. PDF 71) estaban todavía propuestos a la junta y no eran una obligación al cierre. No se simula su traslado a 2026.
- **Otro contraste, no la identidad pura:** con E y N de 31-dic-2025 (C2), el efecto es −1,231793 = −43,338/35,182858.

## 7. N10 · probabilidades y colas

- **[Dato] Fundamento registrado** (fase B de la referencia, `palancas.probabilidades`):
  - 0,2 / 0,6 / 0,2 es una «convención», con confianza media;
  - el MALO no se sube porque «el riesgo de que el margen alto de 2025 no dure ya está en el NORMAL (18 % frente a 19,9 %) y en el margen de partida»;
  - se apoya en el rango de márgenes de 2016–2025 (12,0–20,8 %) y en un único valle;
  - lo cambiaría a 0,25 un 2026 con un margen inferior al 17 %.
- **[Interpretación] Una frecuencia anual de márgenes no identifica por sí sola probabilidades de trayectorias de diez años.** El fundamento cubre la dimensión margen/energía y apenas las demás:
  - ventas (−1 % / 2 % / 3,5 %);
  - capital (S2C 0,9 / 0,9 / 1,0);
  - mantenimiento: P-M1 abierta, con la reposición igual a la amortización en todos los escenarios;
  - ejecución (Brasil y hornos).
- **Cambiar los pesos** (los mismos tres valores; [Hipótesis] etiquetadas, sin fundamento propio de su precisión):

  | Pesos | Ponderado | Precio de Sí |
  |---|---|---|
  | 0,2 / 0,6 / 0,2 (referencia) | 70,50 | 65,69 |
  | 0,3 / 0,5 / 0,2 | 68,78 | 63,12 |
  | 0,4 / 0,5 / 0,1 | 65,50 | 60,24 |
  | 0,25 / 0,5 / 0,25 | 70,43 | 64,84 |
  | 1/3 cada uno | 70,31 | 63,65 |
  | 0,1 / 0,6 / 0,3 | 73,78 | 70,43 |

- **Cambiar la historia de un escenario** ([Hipótesis], recalculada; no son pesos): un MALO adverso coherente, con ventas −2 % y un margen del 12 % (el mínimo de la serie), sin tocar NORMAL, BUENO, probabilidades ni r.
  - El MALO pasa de 53,67 a 43,97. Con los pesos de referencia, el ponderado queda en 68,56 y el precio de Sí en 61,53.
  - Con 0,3 / 0,5 / 0,2, el ponderado es 65,88 y el precio de Sí 57,66.
  - El mantenimiento adverso de la 4.7.1 (+41,8 % de la amortización, solo en el MALO: precio de Sí 55,99) es otra dimensión. No se suma aquí: la plantilla no la representa y P-M1 sigue abierta.
- **Se mantienen** la suma 1, k = 3 experimental y las restricciones del sistema. No se ajusta nada para obtener «Sí».

## 8. Resultados combinados

| Variante | MALO | NORMAL | BUENO | Ponderado | Precio de Sí | r_op | Puente | FCF base | f |
|---|---|---|---|---|---|---|---|---|---|
| Referencia | 53,6704 | 70,7722 | 86,4888 | 70,4952 | 65,6881 | 0,086922 | 160,784 | 161,200 | −0,0276 |
| C1 · 31-dic-2025 con derecho (N6 + N7) | 53,6597 | 70,7430 | 86,4438 | 70,4665 | 65,6645 | 0,086990 | 160,784 | 161,200 | −0,0276 |
| C2 · C1 sin derecho | 52,4279 | 69,5112 | 85,2121 | 69,2347 | 64,4328 | 0,086990 | 204,122 | 161,200 | −0,0276 |

- **Interacciones.** En C1, la fecha de E sube r_op y baja los valores (−0,077), y el denominador los sube (+0,046). El neto (−0,029) no se atribuye a una sola causa.
- **C2 suma el efecto del dividendo con N** = 35,182858.
- **P3, N5 y τ no entran en C1** porque son alternativas condicionadas o hipótesis: se ven aisladas en la tabla completa (`variantes/variantes_4_10.csv` y `.json`, con celdas, procedencia, r, r_op, N, puente, FCF, `f`, estado técnico y avisos).
- **Estado técnico:** «COMPLETO Y VÁLIDO» en todas; el control de `f` dice «⚠ REVISAR». En la copia estructural de τ, que no es íntegra, ese estado lo calcula la hoja y no refleja la sustitución de la fórmula (campo `aviso`).
- **No son comparables con el precio de noviembre de 2026,** que queda fuera del encargo.

**Copia exploratoria combinada** (`copia_combinada/`):
- es el libro C1 con sus cachés y su comprobante externo (`acreditacion_libro.json`), con veredicto ÍNTEGRO;
- su libro de entrada es coherente con C1: el de datos de la referencia, con C41 y C55 de C1;
- pasó la verificación de integridad y la acreditación, no `verificar_todo.sh` completo, porque no es un expediente con fases;
- se reproduce con `scripts/variantes_4_10.py`.

**Expediente exploratorio** (`expediente_exploratorio/Vidrala/`): una copia del de la 4.6.1 con E y N de C1 en `fase1_v63.json` y el alcance declarado.
- El pipeline, ejecutado desde el paso 2, archivó la aprobación heredada al primer paso («el material cambió … la aprobación no vale para la versión nueva»).
- Rellenó y comprobó la entrada (pasos 2–4) y se detuvo en el paso 5 con el código 10, esperando al agente de extracción. **Es su estado legítimo.**
- Los pasos 5–10 son juicios del personaje y el paso 13 es la auditoría.
- **[Interpretación] Por qué no se siguió.** Es una decisión de alcance, no algo que impongan los datos: la fase C compararía la escalera con el precio de noviembre de 2026, y actualizar la oportunidad frente a 87,90 € queda fuera de este encargo. Las entradas de C1 son, además, propuestas sin adoptar.
- El libro evaluado, `resultados.json` y los demás archivos posteriores al paso 4 siguen siendo los de la 4.6.1 hasta que se ejecuten los pasos 5–12 (`expediente_exploratorio/LEEME.md`).
- No hay ningún LISTO, concluido ni APROBADO forzado.
