# N1 · actualización del earnout de México · identificación previa a la decisión

**Fecha:** 17-nov-2026. **Estado:** propuesta para la persona responsable. **No adopta nada.**

- Responde a: «Antes de incluir la actualización de México, identifica su naturaleza contable, tratamiento fiscal y correspondencia con deuda y pagos, evitando duplicaciones.»
- Se toman como dadas las decisiones registradas el 17-nov-2026: (5a), regla N1 con N2 pendiente; E8.1, τ de proyección de cinco años; (4b), opción A.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933, E1/D3/E2/E6 y Elis en `pendiente_de_datos`. No cambian el CSV, las fuentes ni sus huellas.
- **Las opciones del final no se recomiendan por su efecto en la valoración.** El efecto se declara y se explica de dónde sale.

Marcas: **[P]** publicado · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis · **[Pol]** política · **[B]** búsqueda sin resultado · **[LECTURA]** cifra publicada leída en el PDF que no está en el CSV verificado.

Cifras: `resultados/n1_alcance_y_actualizacion.{json,md}`, de `scripts/n1_alcance_y_actualizacion.py`. Las páginas son páginas del PDF. URD22, URD23 y URD25 son los documentos de registro de 2022, 2023 y 2025 en inglés; DEU24, el de 2024 en francés. «Release» es la Release `fuentes-elis-e-20261117` del repositorio auxiliar: sus PDF tienen huella comprobada, pero no están entre las cinco fuentes del CSV verificado.

---

## 1. Respuesta corta

| Pregunta | Respuesta |
|---|---|
| ¿Qué es? | El **descuento financiero** del pasivo por el earnout de la compra de México (Lavartex, 2022): 12,4 / 5,6 / 0,7 en 2023–25 [P]. **No es la revaluación**, que va aparte en la nota 4.6 y es lo que N1 ya recoge. Las dos son variaciones del valor razonable del mismo pasivo [I] |
| ¿En qué línea está? | En el resultado financiero neto, dentro de «Accretion expenses» de la nota 8.2 [P]. **No está en el EBIT** |
| ¿Es deducible? | **No** [P]. La línea fiscal publicada es una sola para los ajustes y la actualización, y solo cuadra con las dos [D] |
| ¿Cuadra con el pasivo y los pagos? | Sí. Se añade al pasivo ligado a adquisiciones y se paga con él, dentro de «Acquisition of subsidiaries». Sin ella el pasivo no cierra: faltarían 12,3 / 6,4 / 0,7 [D] |
| ¿Está ya en otro sitio del motor? | **No** en C48, C49, el FCF base ni el coste de la deuda. Hoy solo entra por el BAI que da el tipo de la fila 10 [D] |
| ¿Hay riesgo de contarla dos veces? | En caja, no, ni incluyéndola ni dejándola fuera. Las duplicaciones posibles son de implementación y se enumeran en el §6 |

Lo que queda por decidir no es un hecho contable, fiscal ni de caja: es el alcance de la regla. Opciones en el §10, al final.

---

## 2. Naturaleza contable

- **Rótulo** [P]: «Accretion expense for the earnout pertaining to the acquisition in Mexico» (URD25 p.313; URD23 p.267); «Charge de désactualisation du complément de prix de l'acquisition réalisée au Mexique» (DEU24 p.259). Es la actualización de un pasivo descontado: el gasto por el paso del tiempo.
- **El pasivo se mide a valor razonable por flujos descontados** [P]: «Offsetting assets and debt related to acquisitions: discounted cash flows», nivel 3 (URD25 p.386).
- **Dos líneas para un mismo pasivo** [I]:
  - el cambio en los pagos esperados es la revaluación: nota 4.6, «Earnout adjustments», dentro del EBIT. En 2023, por la revisión al alza de las perspectivas del grupo comprado [P: URD23 p.302];
  - el paso del tiempo es la actualización: resultado financiero, fuera del EBIT.

  La empresa las junta en una sola línea de la conciliación del impuesto (§4).
- **Solo existe en 2023–2025** [P]:

  | | 2022 | 2023 | 2024 | 2025 | 1.er semestre de 2026 |
  |---|---|---|---|---|---|
  | Actualización del earnout de México | – | 12,4 | 5,6 | 0,7 | – |
  | Fuente | [LECTURA: URD23 p.267] | DEU24 p.259 | URD25 p.313 | URD25 p.313 | [LECTURA: Release, comunicado del 1.er semestre de 2026, p.5] |

  El earnout se liquidó en 2024 y 2025 [P: URD25 p.352]. No es una partida que continúe.
- **No es un devengo mecánico** [D][I]. En el primer semestre de 2024 fue 7,8 [LECTURA: Release, comunicado del 1.er semestre de 2025, p.6] y en el año, 5,6: en el segundo semestre fue **−2,2**. Se recalcula con el pasivo. En ese primer semestre el earnout de México se había revaluado al alza unos 25 millones [P: mismo comunicado, p.5], y el año cerró con un abono neto de 8,7.
- **Política contable específica:** no la he encontrado publicada [B]. La nota 2.2 (combinaciones de negocios) y la nota 4.6 no describen la medición posterior del earnout. El reparto entre revaluación y actualización es la presentación de la empresa.

---

## 3. En qué línea está

| Estado | Dónde | 2023 | 2024 | 2025 | Fuente |
|---|---|---|---|---|---|
| Cuenta de resultados | Resultado financiero neto | (124,6) | (130,4) | (137,1) | [P] DEU24 p.270; URD25 p.324 |
| Nota 8.2 | «Accretion expenses» / «Charges de désactualisation» | (13,8) | (8,8) | (3,8) | [P] DEU24 p.324; URD25 p.379 |
| · de ellos, earnout de México | Tabla del resultado neto corriente | 12,4 | 5,6 | 0,7 | [P] DEU24 p.259; URD25 p.313 |
| · resto | Otras actualizaciones | 1,4 | 3,2 | 3,1 | [D] |
| EBIT | **No está** | — | — | — | [D]: EBIT de la Historia = BAI + resultado financiero |

Precisiones:
- **La cifra de México no es una línea de la nota 8.2.** La nota da el total de «Accretion expenses» y la nombra en su texto [P: URD23 p.332; DEU24 p.324; URD25 p.379]. El importe sale de la tabla que concilia el resultado neto con el resultado neto corriente, una medida alternativa de rendimiento. El cuadre fiscal del §4 la corrobora.
- **El resto** es, por el rótulo que tenía esa línea en el URD 2022, la actualización de provisiones y pensiones: «Interest expense on provisions and retirement benefits», (0,3) en 2022 [LECTURA: URD22 p.313; URD23 p.332] [I].
- **Estado de flujos** [P: URD25 p.327]: el resultado financiero se añade entero para llegar a la caja antes de costes financieros e impuestos; los intereses pagados van aparte, en financiación. La actualización no es caja al registrarse.
- **Balance** [P]: «Deferred consideration payable on acquisitions», en otros pasivos corrientes (nota 4.9) y no corrientes (nota 8.7).
- **Deuda financiera neta** [P: URD25 p.384]: la nota 8.5 no tiene ninguna línea de adquisiciones ni de earnout. El pasivo por earnout no está en la deuda financiera.

---

## 4. Tratamiento fiscal

**No es deducible** [P]. Tres indicios publicados y un cuadre:

1. **La línea de la conciliación del impuesto** se llama «Adjustments and accretion of non-deductible earnouts» / «Ajustements et désactualisation de compléments de prix non déductibles», y remite a la nota 4.6 [P: URD23 p.345; DEU24 p.337; URD25 p.392].
2. **Cuadra solo con las dos partidas** [D], al tipo teórico del 25,83 %:

   | | 2023 | 2024 | 2025 |
   |---|---|---|---|
   | Ajuste de earnout (nota 4.6) | (48,9) | 8,7 | (0,2) |
   | Actualización | (12,4) | (5,6) | (0,7) |
   | Solo el ajuste × 25,83 % | −12,631 | 2,247 | −0,052 |
   | Ajuste y actualización × 25,83 % | −15,834 | 0,801 | −0,232 |
   | Línea fiscal publicada | (15,8) | 0,8 | (0,2) |
   | ¿Cuadra solo con el ajuste? | No | No | No |
   | ¿Cuadra con los dos? | Sí | Sí | Sí |

   La cota de redondeo es 0,076. La línea de 2023 está en el CSV verificado; las de 2024 y 2025 de la edición vigente son [LECTURA: URD25 p.392].
3. **En la tabla del resultado neto corriente del URD 2023**, cinco partidas llevan la llamada «(a) Net of tax effect». La actualización no la lleva, como tampoco el deterioro del fondo de comercio, que no es deducible [P: URD23 p.267].
4. **El tipo efectivo de Francia** en 2023 fue del 50,0 %, «heavily impacted by non-deductible earnout adjustments» [P][LECTURA: URD23 p.346; el mismo texto en DEU24 p.338]. El texto habla de los ajustes; sitúa el gasto en la jurisdicción francesa.

Consecuencia para el motor [D]: la actualización baja el BAI y no baja el gasto por impuesto. El tipo de la fila 10 (gasto ÷ BAI) sube: en 2023, 0,2619 con ella dentro del BAI y 0,2544 sin ella, una vez aplicada N1.

---

## 5. Correspondencia con el pasivo y con los pagos

**Conciliación del pasivo ligado a adquisiciones** (valor razonable, nivel 3; todas las compras, no solo México) [D]:

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Saldo inicial | 90,5 | 118,2 | 23,9 |
| + Altas por las compras del año (precio − desembolso) | n. d. | +1,9 | +11,4 |
| + Revaluación (nota 4.6) | +48,9 | −8,7 | +0,2 |
| + **Actualización** (resultado financiero) | **+12,4** | **+5,6** | **+0,7** |
| − Pagos de earnouts y aplazados (nota 2.4) | −34,4 | −93,9 | −23,3 |
| = Saldo calculado | 117,4 | 23,1 | 12,9 |
| Saldo final publicado | 117,3 | 23,9 | 12,9 |
| Residuo | −0,1 | +0,8 | 0,0 |
| Cota de redondeo | 0,25 | 0,35 | 0,35 |
| **Residuo si se quita la actualización** | **12,3** | **6,4** | **0,7** |

Fuentes y ediciones:
- **Saldos** [LECTURA]: «Debt related to acquisitions» de la jerarquía de valor razonable (URD23 p.339; DEU24 p.331; URD25 p.386). Coinciden con la suma del pasivo corriente y el no corriente (URD23 p.304 y p.340; DEU24 p.298 y p.332; URD25 p.352 y p.387), con 0,1 de redondeo.
- **Revaluación, actualización y pagos:** filas verificadas del CSV.
- **Altas** [LECTURA]: precio de adquisición menos desembolso del año (URD25 p.340–342). En 2023 no se puede determinar: el desembolso de las «otras adquisiciones» supera su precio.
- **2023** usa el cierre del URD 2023. El DEU 2024 lo reexpresa a 118,2; con él el residuo es +0,8.
- **2024** usa el URD 2025. Con el DEU 2024 (cierre 23,5; precio provisional), el residuo es el mismo, +0,8.

Lectura:
- **2023 y 2025 cierran dentro del redondeo.** 2024 deja +0,8 sin explicar por el redondeo: diferencias de conversión y otros movimientos que no se publican por separado [B].
- **Sin la actualización, ningún año cierra.** La actualización se añadió a este pasivo y se pagó con él.
- No hay una tabla publicada del movimiento del pasivo por earnout: la conciliación es una derivación.

**Lavartex, del pendiente en la compra a los pagos** (columnas por sociedad, [LECTURA]):

| | Importe | Fuente |
|---|---|---|
| Precio de adquisición, a valor razonable en la compra | 220,2 | URD23 p.294 |
| Pagado en 2022 | 148,0 | URD23 p.294 |
| Pendiente en la compra | 72,2 | [D] |
| Pagos de 2023, 2024 y 2025 | 31,4 + 83,2 + 19,7 = 134,3 | DEU24 p.288; URD25 p.342 y p.341 |
| Pendiente + revaluación neta de 2023–25 (40,4) + actualización (18,7) | 131,3 | [D] |
| Residuo frente a los pagos | 3,0 | [D] |
| Residuo si se quita la actualización | 21,7 | [D] |

- La revaluación neta es la de toda la nota 4.6, que es «principalmente» de México [P]. El residuo de 3,0 recoge la conversión, los ajustes de 2022 y lo que no sea de México [B].
- **La actualización es el 13,9 % de lo pagado por el earnout de Lavartex.** Su caja está dentro de esos pagos.
- **Los pagos están en las adquisiciones, fuera del FCF base** [P]:
  - nota 2.4, fila «Earnouts and deferred consideration»: 34,4 / 93,9 / 23,3 (filas verificadas);
  - «settlement of the second installment and the balance of the Mexican earnout in 2024 and 2025» (URD25 p.352);
  - presentaciones de resultados: la línea «Acquisitions of subsidiaries, net of cash acquired» incluye «a €83m earn-out payment for the Mexican acquisition» en 2024, y el último, de 20 millones, en 2025 [Release: presentación de resultados de 2024, p.29; de 2025, p.29].

---

## 6. Dónde está ya en el motor, y qué se podría contar dos veces

| Elemento | ¿Lleva la actualización? | Evidencia |
|---|---|---|
| EBIT, m0 y margen proyectado | No | Es resultado financiero [P] |
| Tipo de la fila 10 de 2023–25 (gasto ÷ BAI) | **Sí. Es el único sitio** | El BAI va después del resultado financiero [D] |
| f | Solo a través de ese tipo, en el NOPAT de la ventana | f es un residuo [D] |
| τ de cinco años | Sí, por los tipos de 2023–25 | [D] |
| **C48 = 108** | **No** | C48 usa los intereses netos **pagados**: 70,5 / 78,9 / 99,4. La empresa publica la conciliación entre el resultado financiero y los intereses pagados: la actualización del earnout está solo en el lado de resultados, (5,6) de (130,4) en 2024 y (0,7) de (137,1) en 2025, y no en la salida de caja, (78,9) y (99,4) [P: Release, presentación de 2024, p.52; de 2025, p.51]. Para 2023 no hay esa tabla entre las fuentes: [I] |
| **C49 = 128,1** | **No** | Es el principal de los arrendamientos |
| **FCF base = 307,933** | **No** | El CFO parte de añadir el resultado financiero entero; el pago del earnout está en inversión [P: URD25 p.327] |
| **Coste de la deuda** (Historia C63; motor B, no activo en Elis) | **No** | Usa los intereses pagados y la deuda con arrendamientos. El pasivo por earnout no está en la deuda financiera [P: URD25 p.384] ni en los arrendamientos |
| Deuda o pasivos que el motor resta | No | El motor A no resta deuda. El pasivo por earnout tampoco se resta: 12,9 al cierre de 2025, de otras compras; el de México está liquidado |
| Adquisiciones (Historia, fila 13) | **Su caja, sí** | Los pagos de earnout están dentro de 82,1 / 183,3 / 117,6. Entran en el ancla de S2C si el ancla lleva adquisiciones |

**Duplicaciones.**
- **En caja no hay doble cómputo con ninguna de las dos opciones.** La actualización no se cobra como coste en ningún término de caja del motor. Su caja está en las adquisiciones, que el motor cobrará según se decida en (4b) o con M6.
- **Lo que sí la contaría dos veces**, y hay que excluir en cualquier implementación:
  1. sumarla a C48 como si fuera un interés: su caja ya está en las adquisiciones;
  2. restarla del EBIT: no está en el EBIT;
  3. ajustar a la vez el BAI y el gasto por impuesto con la línea fiscal (15,8 en 2023): la regla toca el BAI y deja el gasto como está;
  4. tomar el total de «Accretion expenses» (13,8 / 8,8 / 3,8) en lugar de la cifra de México: el resto no es earnout.
- **Lo que deja cada opción en el tipo** [D]: si se queda en el BAI, el tipo conserva el rastro de una partida no deducible cuya caja se cuenta en las adquisiciones; si se saca, no. De los 15,834 de impuesto nocional de 2023, N1 quita 12,631; los otros 3,203 son de la actualización.

---

## 7. Efecto de incluirla (se declara; no es criterio)

Perímetro `A0_total`; idéntico en los demás. τ de cinco años. Año 11: MALO / NORMAL / BUENO.

| | Tipo de 2023 / 2024 / 2025 | τ de cinco años | Frente al libro: flujo sin crecimiento · año 11 | Frente a N1 en 2023–25 |
|---|---|---|---|---|
| N1 en 2023–25 | 0,2619 / 0,2806 / 0,2559 | 0,28234 | −11,605 · −15,433 / −18,609 / −19,976 | — |
| N1 en 2023–25 con la actualización | 0,2544 / 0,2772 / 0,2556 | 0,28010 | −12,396 · −16,910 / −20,270 / −21,668 | −0,790 · −1,476 / −1,661 / −1,692 |
| N1 en 2022–25 (opción B del alcance) | 0,2619 / 0,2806 / 0,2559 | 0,28282 | −11,908 · −15,681 / −18,948 / −20,371 | −0,302 · −0,248 / −0,339 / −0,395 |
| N1 en 2022–25 con la actualización | 0,2544 / 0,2772 / 0,2556 | 0,28058 | −12,698 · −17,157 / −20,609 / −22,064 | −1,093 · −1,724 / −2,000 / −2,088 |

**El efecto propio de la actualización es el mismo con cualquier alcance de N1:** −0,790 en el flujo sin crecimiento y −1,661 en el año 11 NORMAL. La actualización no existe en 2021 ni en 2022, así que los dos efectos se suman ([N1_ALCANCE_EJERCICIOS_TAU.md](N1_ALCANCE_EJERCICIOS_TAU.md)).

De dónde sale el −0,790 [D]:
- el tipo de la ventana baja, el NOPAT de la ventana sube y f, que es un residuo, sube: **−2,202**;
- el τ de cinco años baja y el NOPAT proyectado sube: **+1,412**;
- la suma no es cero porque el tipo se promedia en tres años dentro de f y en cinco en la proyección.

**El signo depende de esa convención.** Con el τ de la ventana (no adoptado; E8.1 mantiene cinco años), incluirla daría +0,151 en el flujo sin crecimiento y −0,606 en el año 11 NORMAL. Por eso el efecto no sirve para decidir: mide la convención de τ, no la partida.

---

## 8. Qué está verificado, qué es [LECTURA] y qué no valida

- **En el CSV verificado** (todas OK en sus seis dimensiones):
  - la actualización: `FIN_ACTMEX_FR_2023`, `FIN_ACTMEX_2024`, `FIN_ACTMEX_2025`;
  - el total de «Accretion expenses»: `FIN_ACTUAL_*`;
  - los ajustes de earnout: `OOIE_EARN_*`;
  - los pagos: `ADQ_EARNDIF_*`;
  - la línea fiscal de 2023: `TAX_EARN_FR_2023`.
- **[LECTURA]**, comprobadas por el script en su línea del PDF, pero no verificadas en seis dimensiones:
  - los saldos del pasivo y sus dos líneas de balance;
  - los precios y desembolsos de las compras;
  - las columnas de Lavartex, que son de una sociedad y no del grupo;
  - las líneas fiscales de 2024 y 2025 del URD 2025;
  - las cifras de la Release: la conciliación entre el resultado financiero y los intereses pagados, y los semestres.
- **No valida:**
  - que los 12,4 / 5,6 / 0,7 sean solo descuento financiero: es lo que dice el rótulo, y la cifra del segundo semestre de 2024 muestra que se recalcula con el pasivo;
  - la causa del residuo de 2024 (+0,8) ni la del de Lavartex (3,0);
  - la ausencia de la actualización en los intereses pagados de 2023, que es una inferencia;
  - ninguna valoración de Elis: R sigue pendiente y (4b) también.
- Este documento no está revisado por un contexto distinto del autor.


---

## 9. Reproducción

La de [N1_ALCANCE_EJERCICIOS_TAU.md](N1_ALCANCE_EJERCICIOS_TAU.md), §12: el mismo script calcula las dos partes (107 controles, ninguno fallido). Controles de esta parte:
- las cifras de la propuesta de decisiones, §5.1: −12,396 · −20,270 y −0,790 · −1,661;
- la línea fiscal de 2023, 2024 y 2025 con y sin la actualización;
- el cierre del pasivo en 2023 y 2025;
- la suma de la conciliación publicada del resultado financiero y su igualdad con los intereses pagados del estado de flujos;
- la tabla de la deuda financiera neta, sin líneas de adquisiciones ni de earnout.

---

## 10. Opciones

**Opción I · incluirla.**

> «N1 alcanza también a la actualización del earnout de México de 2023, 2024 y 2025 (12,4 / 5,6 / 0,7): se saca del resultado antes de impuestos que da el tipo de su año, sin tocar el EBIT ni el gasto por impuesto, con su fila de registro. No se extiende a ninguna otra partida financiera.»

Qué implica:
- **El tipo queda sin ninguna partida de la línea fiscal del earnout no deducible.** La regla cubre lo mismo que la línea publicada, que es conjunta, y las dos variaciones del mismo pasivo.
- **Cambia la naturaleza de la regla aprobada.** (5a) habla de «los ajustes de earnout de la nota 4.6», que están en el EBIT. La actualización no está en la nota 4.6 ni en el EBIT: sería una regla solo sobre el tipo. Hay que acotarla, como hace el texto, para que no se lea como permiso para depurar el tipo de otras partidas no deducibles.
- **m0 y el margen no cambian.** Cambian los tipos de 2023–25 y, por ellos, f (a través del NOPAT de la ventana) y el τ de cinco años.
- **Datos:** las tres cifras ya están en el CSV verificado. Habría que pasar al CSV las líneas fiscales de 2024 y 2025 de la edición vigente. Se aplica V-F1l: fuente, regla fiscal y ubicación de la caja.
- **Implementación:** con las cuatro exclusiones del §6.

**Opción II · no incluirla.**

> «N1 se limita a los ajustes de earnout de la nota 4.6. La actualización del earnout de México se queda en el resultado antes de impuestos que da el tipo; se declara que el tipo de 2023–25 la lleva dentro. Cualquier depuración del tipo se decide con la convención de τ (E8.1).»

Qué implica:
- **N1 no toca nada fuera del EBIT.** El texto aprobado de (5a) no cambia.
- **Se conserva la convención general del tipo:** gasto ÷ BAI, con todo el resultado financiero dentro, igual para todas las empresas.
- **La línea fiscal publicada queda neutralizada a medias:** el tipo de 2023 es 0,2619 en lugar de 0,2544.
- **No omite ninguna caja ni la cuenta dos veces.**
- **Datos:** ninguno nuevo.

**Criterios que no dependen del efecto:**

| Criterio | Apunta a |
|---|---|
| Que el tipo no lleve ninguna partida del earnout no deducible, porque la evidencia fiscal es una sola línea | I |
| Que revaluación y actualización, dos líneas del mismo pasivo, reciban el mismo trato | I |
| Que N1 siga siendo una normalización del EBIT, con el alcance que ya se aprobó | II |
| Que la convención del tipo sea la misma en todas las empresas y sus excepciones se decidan juntas en E8.1 | II |
| Evitar duplicaciones en caja | Indiferente: no las hay en ninguna de las dos |

Los hechos identificados no dan ninguna razón contable, fiscal ni de caja para excluirla, y tampoco obligan a incluirla. La elección es sobre el alcance de la regla.

