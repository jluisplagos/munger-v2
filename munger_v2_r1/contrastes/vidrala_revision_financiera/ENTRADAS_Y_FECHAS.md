# Entradas del motor B, fechas y alcance de la continuación (entrega 4.3.1, 9-nov-2026)

Este documento resuelve las precisiones 1 y 2 de la subsanación. Las cifras salen de dos scripts:
- `scripts/subsanacion_entradas_fechas.py` (43 comprobaciones);
- `scripts/revision_financiera_vidrala.py` (217, sin cambios).

**Regla de lectura.** Que una cifra esté en el libro no acredita que sirva para la valoración propuesta. Una hipótesis aceptada tampoco convierte un dato no comprobado en un hecho verificado. **No se escribe ninguna confirmación humana.**

## 1. Clases

| Clase | Significado |
|---|---|
| **L · localizada** | La cifra está en el libro o en el expediente; esta revisión no la ha contrastado con su fuente |
| **C · contrastada** | Cifra **y definición** comprobadas contra la fuente, para el uso que le da el motor |
| **D · derivada por convención** | Resulta de una fórmula o convención del sistema; su validez es la de la convención y la de sus entradas |
| **H · hipótesis pendiente** | Supuesto necesario sin respaldo suficiente; requiere decisión o evidencia |
| **A · ausente** | Falta el dato o la confirmación; no puede sustituirse por una afirmación |

Una entrada puede tener más de una clase. Por ejemplo, un importe puede estar contrastado (C) y usarse con un supuesto sobre su definición (H).

## 2. Clasificación de las entradas

Fecha de referencia del motor: el motor descuenta los flujos 1–10 con exponentes enteros desde el año base (2025). Su valor queda referido al **31-dic-2025** (script 4.3.1, §4).

| Entrada | Libro | Fecha del dato | Clase | Respaldo | Qué falta o qué se supone |
|---|---|---|---|---|---|
| L15 · intereses pagados | 20,8 | 2025 | **C** como intereses pagados | EN25 p.7; ESEF | Si incluyen intereses de arrendamientos (pregunta 2). Afecta a i |
| C63 · i | 0,0634 | 2025 sobre la deuda media de 2024–2025 | **D** (convención 4) | Fórmula del libro | Aproximación histórica. No recoge la deuda de 2026: emisión de 259,4 en el primer semestre (heredado, A) ni el coste de la deuda de Toro |
| L22 · deuda sin arrendamientos | 213,613 | 31-dic-2025 | **C** | EN25 p.3 y p.52 | — |
| L23 · arrendamientos | 49,3 | 31-dic-2025 | **C** | EN25 p.52 | — |
| L24 · caja | 108,352 | 31-dic-2025 | **C** como saldo · **H** como caja disponible | EN25 p.2 y p.7 | El dividendo a cuenta de 43,338 se aprobó el 19-dic-2025 y se pagó el 13-feb-2026 (EN25 p.64). Es un pasivo que no está en L22. Caja restringida: no examinada |
| L25 · «déficit neto de pensiones» | 6,223 | 31-dic-2025 | **C** como provisión de personal · **H** como déficit · **A** el déficit neto | EN25 p.71–72: «defined benefit plans and other obligations with employees» | Obligación menos activos del plan británico; parte de otras obligaciones. Usar 6,223 es una aproximación (≈0,2 % de C41) |
| L26 · minoritarios | 0 | 31-dic-2025 | **L** (cero heredado) · **A** la confirmación humana | Evidencia candidata: el balance no tiene línea de minoritarios (EN25 p.3) | La IA no confirma ceros. Pendiente de revisión humana, como P4 |
| C64 · D | 262,913 | 31-dic-2025 | **C** | L22 + L23 = préstamos del balance | — |
| C37 · precio | 87,9 | 3-nov-2026, 10:13 (intradía) | **L** · **A** la confirmación primaria | Control maestro: Bolsamanía, un solo proveedor | El campo «periodo» dice «Cierre 09/10/2026»: contradicción interna. La nota lo llama «con derecho», pero según el BORME (§3) el 3-nov-2026 cae dentro del período de asignación de la liberada, así que la cotización sería sin derecho (interpretación). Falta un cierre oficial y el calendario de la operación |
| C55 · acciones | 35,206 | 31-dic-2025 | **C** como acciones emitidas y media ponderada de 2025 · **H** como acciones a la fecha del precio · **A** las acciones en circulación el 3-nov-2026 | EN25 p.60, p.61 y p.76 | La convención 9 pide «las acciones vigentes en la fecha de valoración». Faltan la autocartera de 2026 (heredada ≈1,021 mm, no contrastada y mayor que el programa documentado de 350.000) y la liberada 1×20 (+5,0 %, hecho; fecha sin derecho por interpretación) |
| C41 · E | 3.094,6 | Mezcla: precio de 3-nov-2026 × acciones de 31-dic-2025 | **D** (C37 × C55) · **H** su idoneidad | Libro | El Control maestro calcula otra cifra (3.032,2 = 88,70 × 34,185). Con la liberada y la autocartera heredada, el número de acciones sería ≈35,89 (+1,96 %); sin autocartera de 2026, ≈36,94 (+4,93 %) |
| C52 · τ | 0,20032 | Media 2021–2025 | **D** | Fórmula del libro | 2021–2022 incluyen Italia (perímetro mixto; efecto pequeño) |
| `r_op` | 0,0869 | Mezcla (E de 3-nov-2026; D de 31-dic-2025; i de 2025) | **D** (convención 4: tasa personalizada, no coste de mercado) | Aritmética del libro | Con D a 30-jun-2026 (409,6, heredado) bajaría ≈15 pb; con las acciones tras la liberada y la autocartera heredada, ≈+0,5 pb. Es aritmética, no una valoración |
| r | 0,09 | — | Decisión humana | — | No se toca |
| V0 · ventas de 2025 | 1.465,16 | 2025 | **C** | EN25 p.4 | No incluye Toro (consolidada desde el 30-mar-2026, heredado) |

## 3. Hecho nuevo: la ampliación liberada de 2026

**[Hecho]** BORME núm. 208, 28-oct-2026, anuncio 5696. Se conserva en `fuentes/borme_2026_5696/`, con su huella.
- Vidrala ejecuta el acuerdo de la junta del 29-abr-2026: **1.760.312 acciones nuevas**, una por cada veinte antiguas.
- El período de asignación dura catorce días naturales «desde el día siguiente al de la publicación del anuncio» en el BORME y en la web de la sociedad.
- Tienen derecho los titulares al cierre del día anterior a ese inicio.
- 1.760.312 × 20 = 35.206.240: coincide, salvo 18 acciones de redondeo, con las 35.206.258 emitidas a 31-dic-2025. El capital no se había reducido por amortización de autocartera antes de la operación.

**[Interpretación]**
- Si la web publicó el mismo día, el período va del **29-oct al 11-nov-2026**, y el precio del 3-nov-2026 es un **precio sin derecho**.
- Comparar ese precio con un valor por acción calculado con 35,206 millones de acciones (antes de la liberada) sobrestima el valor por acción frente al precio. Según la autocartera, el exceso va de ≈2,0 % a ≈4,9 %.
- La fase A (Palancas C47) daba la liberada por «no ejecutada a 9-oct» y calculaba el efecto «a ojo, un 3 %, dentro de la tolerancia del 5 %». El BORME supera ese supuesto: la operación se ejecutó antes de la fecha del precio, y la parte de la liberada (5 %) ya alcanza la tolerancia por sí sola.
- Confirmarlo exige el calendario oficial: hecho relevante o documento informativo. Ninguno está conservado.

## 4. Ruta A · reejecución exploratoria con base 2025

**Qué es.** Expediente nuevo con P1 aplicada y el motor elegido, con todos los saldos a 31-dic-2025. Como el motor descuenta desde el año base, su valor está referido a esa fecha.

**Fechas que no son de 31-dic-2025 y deben declararse:**
- C37 = 87,9 y, por tanto, C41 = E de `r_op`: 3-nov-2026.
- C53 y C54: 30-jun-2026; solo contexto, no entran.
- La fecha de análisis (D4): 3-nov-2026.

Mientras se conserven esos parámetros, **el ejercicio no es una valoración íntegramente referida al cierre de 2025**. Para que lo fuera haría falta el precio de cierre de 31-dic-2025 (ausente) para E. El efecto de E en `r_op` es pequeño, pero existe.

**Qué permite comprobar:**
- la coherencia interna del expediente con P1;
- si las palancas de la fase B se sostienen con la referencia S2C corregida;
- cómo responde el valor a la elección del motor (A con T3 frente a B) sobre la misma base;
- qué peso tienen L25, L26 y C49 en cada motor;
- si los avisos de la gramática desaparecen o cambian.

**Qué queda fuera de su alcance:**
- **No permite comparar el valor con el precio del 3-nov-2026.**
- Por tanto, no da un precio de Sí comparable, ni una zona, ni un margen de seguridad, ni un cubo para decidir.
- Tampoco dice nada sobre Toro, los dividendos y recompras de 2026, la liberada ni la deuda de 2026.

**Requisitos para ejecutarla:**
- **Decisiones humanas:** P1; el motor; que la ruta es exploratoria. Con el motor B, además, el tratamiento de L25 y de la caja comprometida.
- **Confirmaciones pendientes:** L26 y C48 siguen como ceros pendientes. El sistema los marca y el resultado queda provisional.

## 5. Ruta B · análisis comparable con el precio de noviembre de 2026

**Consecuencia económica del desfase.** No es solo una salvedad. Si se compara un valor a 31-dic-2025 con un precio de 3-nov-2026, cada componente mueve la comparación en un sentido. Los porcentajes se expresan sobre C41, no sobre el valor del modelo, que no se ha calculado.

| Componente | Sentido sobre el valor por acción frente al precio | Orden de magnitud | Estado del dato |
|---|---|---|---|
| **Tiempo** (307 días) | El valor a 31-dic-2025 no incluye el rendimiento de 10 meses: lo **infravalora** a la fecha del precio | (1 + r)^(307/365) − 1 = 7,5 % del valor del negocio antes de distribuciones | Aritmética de la convención |
| **Dividendos de 2026** | El valor a 31-dic-2025 incluye 59,8 mm que el comprador del 3-nov ya no recibe: lo **sobrevalora** | 1,9 % de C41 (1,70 €/acción) | 43,338 hecho; 16,490 propuesto (EN25 p.65); pago del 15-jul heredado |
| **Liberada 1×20** | Con un precio sin derecho y acciones de antes de la liberada, el valor por acción se **sobrevalora** | +2,0 % a +4,9 % de acciones | Hecho (BORME) e interpretación (fecha sin derecho) |
| **Recompras de 2026** | Cambian la caja y las acciones. Son neutras solo si se compra al valor intrínseco | ≈1,02 mm de acciones; 52,7 mm en el primer semestre | Heredado, no contrastado; contradice el programa documentado de 350.000 |
| **Toro** | El precio lo incluye; la base de 2025 no incluye ni sus flujos ni su coste. Es neutro solo si se compró a su valor, y tiene un plan de ajuste | VE ≈77 mm = 2,5 % de C41; ventas ≈4,8 % de V0 | VE estimado (EN25 p.78); precio final, deuda asumida y pago aplazado ausentes |
| **Deuda neta de 2026** | +145,6 mm en el primer semestre: distribuciones, Toro, circulante y flujo del semestre. Su lectura depende del desglose | 4,7 % de C41 | Heredado (semestral 1S2026, doc. 2487, no conservado) |
| **Borrasca Kristin** | Coste de 2026, mitigado por seguros y ayudas | 10–15 mm antes de seguros = 0,3–0,5 % de C41 | Hecho posterior (EN25 p.78); efecto neto ausente |

**[Interpretación]** Los componentes tienen signos opuestos y el mayor, el tiempo, va en sentido contrario a los otros. **No puede saberse si el desfase favorece o perjudica la comparación** sin los datos de la columna «Estado». Por eso la ruta A no sirve para decidir, y la ruta B no puede ejecutarse todavía.

**Conciliaciones necesarias para la ruta B:**
1. **Perímetro y base de proyección.** Decidir si la base incluye Toro. Si la incluye, hacen falta sus cuentas (ventas, EBIT, D&A, capex y circulante) y el coste del plan de ajuste. Además, separar el efecto de Kristin del margen recurrente.
2. **Deuda, arrendamientos, caja y otras obligaciones** a una fecha próxima al precio: el semestral de 2026, conservado y contrastado, o una fecha posterior si existe. Incluye la deuda asumida y el pago aplazado de Toro, los dividendos a pagar, las pensiones (déficit neto), los derivados y la naturaleza del *confirming* (39,2, heredado).
3. **Adquisiciones:** precio final de Toro, forma de pago y deuda asumida.
4. **Recompras, dividendos y acciones:** autocartera al 3-nov-2026 (informes de la CNMV), programa o programas vigentes, dividendos pagados en 2026 y acciones emitidas tras la liberada.
5. **Precio y capitalización:** cierre oficial del 3-nov-2026 y calendario de la liberada. Después, capitalización = precio × acciones en circulación con la misma base (sin derecho y tras la liberada).
6. **Tiempo.** El motor no admite un primer año parcial. Hay dos opciones, y elegir entre ellas es una **decisión de método**:
   - llevar el valor de 31-dic-2025 a la fecha del precio, restando las distribuciones del período;
   - rebasar el ejercicio en una fecha de 2026, con su propia base.

**Qué conclusiones impide su ausencia:** cualquier lectura de precio frente a valor (precio de Sí, zona, margen y cubo), la recomendación de compra o espera y la comparación con la fuente externa (C38).

**Fuentes primero.** Las fuentes conservadas no contienen nada de 2026, salvo los hechos posteriores del informe 2025 (Toro, Kristin y el dividendo) y el BORME conservado ahora. El semestral de 2026 está identificado por URL en el Control maestro, pero no se ha descargado porque esta subsanación no es la actualización de 2026.
