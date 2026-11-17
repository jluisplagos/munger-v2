# N1 · alcance en los ejercicios de τ · propuesta para decisión

**Fecha:** 17-nov-2026. **Estado:** propuesta para la persona responsable. **No adopta nada.**

- Responde a: «Justifica el alcance de N1 para todos los ejercicios utilizados en τ.»
- Se toman como dadas las decisiones registradas el 17-nov-2026:
  - (5a): regla N1, con N2 pendiente y sin deducir el 27,936;
  - E8.1: se mantiene el τ de proyección de cinco años. Con él, los ejercicios de τ son **2021–2025**.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933, E1/D3/E2/E6 y Elis en `pendiente_de_datos`.
- No se fija R ni ningún umbral. No cambian el CSV, las fuentes ni sus huellas.
- Ninguna opción se propone por su efecto en el valor. Donde lo hay, se dice en qué sentido.

Marcas: **[P]** publicado · **[D]** derivado · **[I]** interpretación · **[H]** hipótesis · **[Pol]** política · **[B]** búsqueda sin resultado · **[LECTURA]** cifra publicada leída en el PDF que no está en el CSV verificado.

Cifras: `resultados/n1_alcance_y_actualizacion.{json,md}`, de `scripts/n1_alcance_y_actualizacion.py`. 107 controles, ninguno fallido; 103 de 103 [LECTURA] y 19 de 19 pasajes en su página del PDF. Las páginas son páginas del PDF. Abreviaturas: URD21, URD22, URD23 y URD25 son los documentos de registro en inglés de 2021, 2022, 2023 y 2025; DEU24, el de 2024 en francés.

---

## 1. Respuesta corta

- **El alcance de N1 debe seguir a τ.** N1 cambia cómo se mide el tipo de un año: gasto por impuesto ÷ resultado antes de impuestos (BAI) sin el ajuste de earnout. El τ de proyección es la media de los cinco tipos de 2021–2025. Si la regla se aplica en unos años sí y en otros no a la misma partida, la media mezcla dos definiciones del tipo.
- **La regla tiene una premisa fiscal: que el ajuste no sea deducible.** Es el fundamento con el que se propuso (5a): «No son deducibles: tienen línea propia en la conciliación fiscal». Por eso N1 quita el ajuste del BAI y deja el gasto por impuesto como está. La premisa hay que comprobarla en cada año.
- **2022 la cumple** [P]: la misma línea de la misma nota que 2023–25, no monetaria, y con línea fiscal propia en la conciliación del impuesto. Dejarlo fuera sería incoherente.
- **2021 no la cumple con lo publicado. Esta es la razón real en contra de «todos los ejercicios».** El ajuste es de la misma naturaleza contable [P], pero:
  - no tiene línea fiscal propia [B];
  - la única indicación fiscal publicada va en contra: la medida neta de impuesto del URD 2021 atribuye a su línea casi todo el tipo teórico. Al tipo teórico, entre 2,4 y 3,0 de los 3,0 del ajuste llevan efecto fiscal [P][D];
  - un ajuste que lleva su impuesto apenas mueve el tipo: sin él, 0,3302; con él, 0,3310. La distorsión que N1 corrige no se da en ese año.
- **Propuesta: alcance 2022–2025** (opción B). Efecto frente a N1 solo en 2023–25: −0,302 en el flujo sin crecimiento y −0,339 en el año 11 NORMAL. Total frente al libro: −11,908 y −18,948. Solo se mueve el tipo; f y m0 no cambian [D].
- **El +0,416 y +0,466 de la propuesta de decisiones se reproduce,** pero supone que el ajuste de 2021 no fue deducible. Es una hipótesis [H] contraria a la única indicación publicada. Con el tratamiento que la indicación sostiene, extender a 2021 da −0,202 y −0,226: casi lo mismo que no tocarlo.
- Las tres opciones de alcance quedan por debajo del 0,15 % del FCF base. La elección es de coherencia y de evidencia, no de importe.

---

## 2. Lo publicado, ejercicio por ejercicio

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Ajuste de earnout, nota 4.6 [P] | (3,0) | 2,4 | (48,9) | 8,7 | (0,2) |
| Fuente de la edición vigente | URD22 p.285 | URD23 p.302 | DEU24 p.296 | URD25 p.350 | URD25 p.350 |
| ¿En el CSV verificado? | Sí | Sí | Sí | Sí | Sí |
| Línea del estado de flujos que lo devuelve por no monetario | 2,9 [LECTURA: URD22 p.261] | (2,5) [LECTURA: URD23 p.279] | 48,4 | (9,3) | (0,1) |
| Línea fiscal propia en la conciliación del impuesto | **No hay** [B: URD21 p.290; URD22 p.326] | 0,5 [LECTURA: URD23 p.345] | (15,8) [P: DEU24 p.337] | 0,8 [LECTURA: URD25 p.392] | (0,2) [LECTURA: URD25 p.392] |
| (Ajuste − actualización) × tipo teórico [D] | −0,852, al 28,41 % | 0,620, al 25,83 % | −15,834 | 0,801 | −0,232 |
| ¿Cuadra con la línea publicada? | — | No con 2,4; sí con 2,1 | Sí | Sí | Sí |
| Otra indicación fiscal publicada | Medida neta de impuesto: **con efecto fiscal** [P][D] (§5) | — | — | — | — |
| Pagos de earnouts y aplazados | Dentro del importe pagado de la nota 2.4, sin fila propia [I] | Ídem [I] | Fila propia: 34,4 [P] | 93,9 [P] | 23,3 [P] |

Precisiones:
- **2021.** El URD 2021 presentaba una sola línea: «Costs related to acquisitions and earnout adjustments», (5,1) [LECTURA: URD21 p.253]. El URD 2022 la separa en costes de transacción, (2,1), y ajustes de earnout, (3,0): 2,1 + 3,0 = 5,1 [D]. La cifra separada solo existe en la edición vigente.
- **2022.** El URD 2022 daba 2,1; el URD 2023 lo reexpresa a 2,4. El total de la nota no cambia: (9,0) en las dos ediciones. El cálculo usa 2,4, por la regla de la edición vigente.
- **Línea del estado de flujos.** En el URD 2022 se llama «Other»; el URD 2023 la rotula «Earnout adjustments and other elements with no impact on cash flows». En los cinco años vale el ajuste de earnout con el signo contrario, salvo una diferencia de −0,1 a −0,6: los otros elementos sin efecto en caja [D].
- **Tipos teóricos** [LECTURA]: 28,41 % en 2021 (URD21 p.290; URD22 p.326) y 25,83 % en 2022–2024 (URD23 p.345; DEU24 p.337; URD25 p.392). El de 2025 está en el CSV.
- **Actualización del earnout de México:** 12,4 / 5,6 / 0,7 en 2023–25 y nada en 2022 («–» [LECTURA: URD23 p.267]). Se trata en [N1_ACTUALIZACION_EARNOUT_MEXICO.md](N1_ACTUALIZACION_EARNOUT_MEXICO.md).

---

## 3. ¿Son de la misma naturaleza contable que los de 2023–25?

Sí, en todo lo que la empresa publica.

- **Misma línea y misma nota** [P]: «Earnout adjustments», nota 4.6 «Other operating income and expenses», en los cinco ejercicios (URD22 p.285; URD23 p.302; DEU24 p.296, «Ajustements de compléments de prix»; URD25 p.350).
- **Misma política contable de la nota** [P]: «Items of material amounts that are unusual, abnormal or infrequent are disclosed separately in the income statement», con el mismo texto en el URD 2022, el URD 2023 y el URD 2025.
- **No monetarios al registrarse** [P][D]: el estado de flujos los devuelve en los cinco años (tabla del §2).
- **Mismo pasivo** [P]: la deuda ligada a adquisiciones figura a valor razonable, nivel 3, al cierre de 2021 y de 2022: 27,1 y 90,4 [LECTURA: URD22 p.320]. La técnica, flujos descontados, la describe el URD 2025 (p.386). El 27,1 incluye 1,2 de compromisos de recompra de minoritarios (6,5 + 19,3 + 1,2 = 27,0 [D]).
- **La suma de la nota cierra** [D]: las líneas de la nota 4.6 de 2021 suman (16,1), su total publicado; las de 2022 suman (9,1), frente a (9,0), dentro del redondeo de sus diez cifras.

Lo que no está publicado [B]:
- a qué adquisiciones corresponden los ajustes de 2021 y de 2022. Los de 2023 son «principalmente» de la compra de México [P: URD23 p.302];
- una fila propia de pagos de earnouts en 2021 y 2022. La nota 2.4 de esos años da el importe pagado por país. Ese importe incluye pagos de compras de años anteriores [I]: en 2021 se pagaron 9,4 en Brasil por compras cuyo precio fue 1,4; en 2022 se pagaron 7,8 en Rusia, donde no hubo ninguna compra ese año y quedaban 9,7 pendientes de 2021 [LECTURA, columnas por país: URD22 p.275 y p.277]. Eso sitúa los pagos aplazados dentro de las adquisiciones; no identifica cuáles son earnouts.

**La naturaleza contable no decide la fiscal.** La línea de la conciliación del impuesto se llama «Adjustments and accretion of **non-deductible** earnouts» [P]. El propio nombre admite que haya ajustes de earnout deducibles.

---

## 4. ¿Su registro sigue la misma regla?

N1 exige una fila de ajuste por año con su fuente, su regla fiscal y la ubicación de su caja (especificación, E1; control V-F1l). La fila del EBIT publicado no cambia.

| Requisito | 2021 | 2022 | 2023–25 |
|---|---|---|---|
| Partida e importe con fuente | (3,0) [P]; fila verificada | 2,4 [P]; fila verificada. 2,1 en la edición anterior | [P]; filas verificadas |
| Regla fiscal: no deducible, gasto sin cambios | **No se sostiene.** Sin línea fiscal propia [B]; la medida neta de impuesto le atribuye efecto fiscal [P][D] | Línea propia: 0,5 [P]. Cuadra con 2,1 y no con 2,4 | Línea propia [P]. Cuadra con el ajuste y la actualización |
| Ubicación de la caja: adquisiciones, fuera del FCF base | Importe pagado de la nota 2.4 [I] | Ídem [I] | Fila propia de la nota 2.4 [P] |

Conclusión:
- **2022** cumple los tres requisitos, con dos matices declarados: la línea fiscal no cuadra con la cifra reexpresada, y la caja se sitúa por inferencia.
- **2021** cumple el primero. El tercero es una inferencia. **El segundo no se cumple con lo publicado:** la regla fiscal de su fila sería una hipótesis, no un dato.

---

## 5. La indicación fiscal de 2021

**No hay línea fiscal propia** [B]. Ni el URD 2021 (p.290) ni el URD 2022 (p.326) separan el earnout en la conciliación del impuesto de 2021. La línea la crea el URD 2023, que la da para 2023 y 2022. Para 2021 no se ha publicado nunca.

**Lo único publicado es la medida «net income from ordinary operations» del URD 2021** (p.217), que presenta cada partida «net of tax effect»:

| | Bruto (nota 4.6) | Neto de impuesto | Efecto fiscal implícito | Tipo teórico del año |
|---|---|---|---|---|
| 2021 · costes de adquisición y ajustes de earnout | 5,1 | 3,7 | 1,4, el 27,5 % | 28,41 % |
| 2021 · reestructuración | 6,4 | 4,8 | 25,0 % | 28,41 % |
| 2020 · costes de adquisición y ajustes de earnout | 5,7 | 4,6 | 19,3 % | 32,02 % |
| 2023 · nota 4.6 entera, con (48,9) de earnout | 67,9 | 64,6 | 4,9 % | 25,83 % |

Todas son [LECTURA]: URD21 p.217, p.253 y p.290; URD23 p.267 y p.302; DEU24 p.337.

Lectura [D][I]:
- **La medida no aplica un tipo único; mide el efecto fiscal de cada partida.**
  - Da porcentajes distintos por partida y por año. En la reestructuración de 2021, el 25,0 %: con el redondeo de sus dos cifras, entre el 23,6 % y el 26,4 %, por debajo del tipo teórico.
  - En 2023 deja casi sin efecto fiscal una nota dominada por un earnout no deducible.
- **En 2021 el ajuste de earnout lleva efecto fiscal.**
  - Si los costes de transacción (2,1) llevaran el tipo teórico entero, aportarían 0,60 del 1,4. Los 0,80 restantes solo pueden venir del ajuste de earnout: equivalen a 2,8 de sus 3,0. Con el redondeo de las cifras impresas, entre 2,4 y 3,0.
  - Sin efecto fiscal en el earnout, el neto publicado sería 4,5 y no 3,7.
  - Para que el ajuste no llevara ningún efecto fiscal, los costes de transacción tendrían que soportar un 66,7 % de impuesto (un 60,5 % como mínimo, con el redondeo). Ningún tipo del impuesto llega ahí.

Límites de esta indicación:
- es una medida alternativa de rendimiento, no la nota del impuesto;
- la empresa pudo calcular ese efecto fiscal con una simplificación, y no con el tratamiento real de la partida [H]. En contra de esa lectura: la misma línea llevó en 2020 un 19,3 %, frente a un tipo teórico del 32,02 %; la medida no aplicaba el tipo entero por defecto [I];
- la línea mezcla costes de transacción y ajustes de earnout. El reparto exacto depende del tipo de cada país, que no se publica; el sentido no depende de él;
- no dice por qué el ajuste de 2021 llevaría impuesto y los de 2022–25 no. Las adquisiciones a las que corresponde no están publicadas [B].

**No es concluyente. Pero es lo único publicado, y apunta en contra de aplicar a 2021 una regla «sin efecto fiscal».**

---

## 6. Por qué el alcance debe seguir a τ, y hasta dónde

1. **El tipo se aplica a una base y debe medirse sobre la misma base** [D].
   - En la proyección, el NOPAT es margen × (1 − τ). El margen se declara sin ajustes de earnout: es una condición de (5a), y m0 sale del EBIT de 2025 sin el ajuste.
   - El tipo que lo multiplica no debe llevar la distorsión de esos ajustes en ninguno de los años que lo forman.
2. **La distorsión solo existe si el ajuste no es deducible** [D].
   - Un ajuste no deducible mueve el BAI y no el gasto: el tipo cambia. Es lo que N1 corrige.
   - Un ajuste que lleva su impuesto mueve los dos: el tipo casi no cambia. En 2021, 0,3310 con el ajuste dentro y 0,3302 sin él y sin su impuesto.
3. **Por eso el alcance coherente son los ejercicios de τ con un ajuste no deducible.**
   - Con N1 en 2023–25 y no en 2022, la media mezclaría tres tipos medidos sin la distorsión y uno con ella: **eso sí sería incoherente.**
   - Dejar 2021 como está no lo es: con lo publicado, su tipo no lleva esa distorsión.
4. **Cada uso de la regla alcanza a los años que entran en ese uso** [D].
   - El EBIT de 2021 y 2022 no entra en f ni en m0: la ventana de calibración es 2023–25. Para el EBIT, el alcance es la ventana.
   - El tipo de 2021 y 2022 sí entra en τ. Para el tipo, el alcance son los años de τ.
   - El script lo comprueba: en todos los escenarios, f y m0 son idénticos a los de N1 en 2023–25, y la variación es exactamente −V₀·m0·Δτ.
5. **La regla se aprobó por la naturaleza de la partida, no por su tamaño ni por su signo** [Pol, (5a)]. El ajuste de 2022 es un abono pequeño: se incluye igual.
6. **Si cambia la convención de τ, el alcance la sigue.** Con el τ de la ventana (convención no adoptada), 2021 y 2022 no entrarían en ningún cálculo y la cuestión desaparecería.

---

## 7. Matices y límites

1. **En 2022 la línea fiscal cuadra con 2,1 y no con 2,4** [D].
   - 2,4 × 25,83 % = 0,620, frente a 0,5 publicado: residuo −0,120, mayor que la cota de redondeo (0,063). Con 2,1, 0,542: cuadra.
   - Lecturas posibles [H]: el comparativo fiscal no se actualizó con la reexpresión, o una parte del ajuste, del orden de 0,5, tributa.
   - Si tributara la parte que la línea no cubre, el tipo de 2022 sería 0,2843 en lugar de 0,2847, y el efecto de la opción B, −0,252 en lugar de −0,302. No cambia la conclusión.
2. **Extender N1 no deja el τ de cinco años «normalizado»** [D]. Solo hace uniforme la regla del earnout.
   - En los años de τ hay otras partidas no deducibles que N1 no toca. La mayor es el deterioro del fondo de comercio de 2022: 58,7, con línea fiscal propia de (15,1) [LECTURA: URD23 p.345].
   - Mueve el tipo de 2022 de 0,2337 a 0,2823: 0,0097 en el τ de cinco años, unos 6,1 en el flujo sin crecimiento. El alcance de N1 mueve 0,0005.
   - **No se propone normalizarla:** (5a) aprobó que ninguna otra partida se normaliza, y la convención de τ es E8.1. Se declara para que el alcance de N1 no se lea como una depuración del tipo.
3. **La caja de 2021–22 se sitúa por inferencia** [I] (§3).
4. **Las dos cifras de 2021 y 2022 no tienen identidad entre páginas.** Están verificadas en el CSV, sin incoherencia detectada. Su segunda línea es la suma de su propia nota y la línea del estado de flujos, que son [LECTURA].

---

## 8. Efecto recalculado

Perímetro `A0_total`; la variación es idéntica en `A1_sin_ROU` y `A2_propio`. τ de proyección de cinco años. Año 11: MALO / NORMAL / BUENO.

| Alcance | Tipo de 2021 · 2022 | τ de cinco años | Frente al libro: flujo sin crecimiento · año 11 | Frente a N1 en 2023–25: flujo · año 11 |
|---|---|---|---|---|
| Libro, sin ajustes | 0,3310 · 0,2823 | 0,28820 | — | — |
| **C** · N1 en 2023–25 | 0,3310 · 0,2823 | 0,28234 | −11,605 · −15,433 / −18,609 / −19,976 | — |
| **B** · N1 en 2022–25 (propuesta) | 0,3310 · 0,2847 | 0,28282 | −11,908 · −15,681 / −18,948 / −20,371 | −0,302 · −0,248 / −0,339 / −0,395 |
| **A′** · N1 en 2021–25, con 2021 gravado al 28,41 % [LECTURA] | 0,3302 · 0,2847 | 0,28266 | −11,807 · −15,599 / −18,835 / −20,240 | −0,202 · −0,165 / −0,226 / −0,264 |
| **A** · N1 en 2021–25, todos sin efecto fiscal | 0,3253 · 0,2847 | 0,28168 | −11,190 · −15,093 / −18,142 / −19,433 | +0,416 · +0,341 / +0,466 / +0,543 |
| Descomposición: 2023–25 y 2021 sin efecto fiscal | 0,3253 · 0,2823 | 0,28120 | −10,887 · −14,845 / −17,803 / −19,037 | +0,718 · +0,588 / +0,806 / +0,939 |
| Sensibilidad de B: en 2022 tributa lo que la línea fiscal no cubre [LECTURA] | 0,3310 · 0,2843 | 0,28274 | −11,858 · −15,640 / −18,891 / −20,305 | −0,252 · −0,206 / −0,283 / −0,329 |

Lectura:
- **El +0,416 de la propuesta de decisiones se reproduce** y se descompone: +0,718 de 2021 y −0,302 de 2022 [D]. Todo el signo positivo viene de tratar 2021 como no deducible.
- **B y A′ dan casi lo mismo:** −0,302 y −0,202. Quitar del BAI un gasto que lleva su impuesto apenas cambia el tipo.
- En valor absoluto, B, A′ y A quedan entre el 0,07 % y el 0,14 % del FCF base. **Es pequeño en cualquier caso.**

Controles de reproducción:
- el libro: f, τ de cinco años, flujo sin crecimiento y los tres flujos del año 11;
- las cifras de la propuesta de decisiones, §5.1: −11,605 · −18,609; −11,190 · −18,142; +0,416 · +0,466;
- la salida ya contrastada de `copia_investigacion_f1.py`, cifra a cifra.

---

## 9. Qué está en el CSV verificado y qué sería [LECTURA] nueva

**El cálculo de B, A y C solo usa filas verificadas del CSV** (762 filas: 748 OK, 14 PENDIENTE, 0 FALLO; todas las de aquí, OK en sus seis dimensiones). A′ usa además el tipo teórico de 2021, que es [LECTURA].

| Cifra | Filas |
|---|---|
| Ajustes de earnout de 2021–2025 | `OOIE_EARN_U22_2021`, `OOIE_EARN_U23_2022`, `OOIE_EARN_FR_2023`, `OOIE_EARN_2024`, `OOIE_EARN_2025` |
| BAI y gasto por impuesto de 2021–2025 | `IS_BAI_*` e `IS_IMP_*` de cada edición vigente |
| Línea fiscal del earnout de 2023 | `TAX_EARN_FR_2023` |
| Tipo teórico de 2025 | `TAX_TEOR_2025` |
| Solo identidad entre ediciones, sin entrar en el cálculo | `OOIE_EARN_U22_2022` (2,1) y `TAX_EARN_FR_2024` (0,8) |

**Serían [LECTURA] nuevas.** El script las comprueba en su línea del PDF (huella, rótulo, literal y posición). Esa comprobación no es la verificación de seis dimensiones.

| [LECTURA] | Fuente | Para qué | ¿Pasarla al CSV? |
|---|---|---|---|
| Línea fiscal del earnout de 2022: 0,5 | URD23 p.345 | Regla fiscal de 2022 | **Sí**, si se aprueba B, A′ o A: es la evidencia que V-F1l pide registrar |
| Línea fiscal de 2024 y 2025, edición vigente: 0,8 y (0,2) | URD25 p.392 | Regla fiscal de 2024–25. Hoy el CSV tiene la de 2024 como edición anterior y no tiene la de 2025 | **Sí**, con cualquier alcance: es la evidencia fiscal de la regla ya aprobada |
| Medida neta de impuesto de 2021: 3,7 y 4,8; sus brutos: (5,1) y (6,4). La misma línea en 2020: 4,6 y (5,7) | URD21 p.217 y p.253 | Indicación fiscal de 2021 | **Sí**, si la decisión se apoya en ella: es la razón de dejar 2021 fuera, o de gravarlo |
| Tipos teóricos de 2020–2024: 32,02 %, 28,41 % y 25,83 % | URD21 p.290; URD22 p.326; URD23 p.345; DEU24 p.337; URD25 p.392 | Cuadre de la línea fiscal y lectura de la indicación de 2021. El de 2021 entra en el cálculo de A′ | Sí, si el cuadre se registra como control. El de 2021, **obligado** si se aprueba A′ |
| Línea no monetaria del estado de flujos de 2021 y 2022: 2,9 y (2,5) | URD22 p.261; URD23 p.279 | Segunda línea de los ajustes de 2021–22 | Recomendable |
| Total de la nota 4.6 de 2021 y 2022 y sus líneas; costes de transacción de 2021: (2,1) | URD22 p.285; URD23 p.302 | Suma de la nota; reparto de la línea conjunta de 2021 | Recomendable |
| Medida neta de impuesto de la nota entera: 11,5 (2021), 7,0 (2022) y 64,6 (2023) | URD22 p.249; URD23 p.267 | Contexto de la indicación | No hace falta |
| Actualización de 2022: «–»; gastos de actualización de 2022: (0,3) | URD23 p.267 y p.332; URD22 p.313 | Que en 2022 no hubo actualización del earnout | Sí, si se incluye la actualización |
| Deterioro de 2022, línea fiscal: (15,1) | URD23 p.345 | Límite declarado | No |
| Pasivo de 2021–22 y pagos por país | URD22 p.275, p.277, p.286, p.320 y p.321 | Ubicación de la caja | Los pagos por país no son del perímetro del grupo: seguirían [LECTURA] |

No se ha añadido ninguna fila al CSV en esta entrega: pasar cifras al CSV es un bloque propio, con su verificación y su revisión.

---

## 10. Opciones y texto que se pediría aprobar

| Opción | Alcance | Qué supone | Efecto frente a N1 en 2023–25 |
|---|---|---|---|
| **B** (propuesta) | 2022–2025: los ejercicios de τ con un ajuste no deducible según lo publicado | El tipo queda sin la distorsión del earnout no deducible en los cinco años. El ajuste de 2021 queda identificado y sin aplicar | −0,302 · −0,339 |
| **A′** | 2021–2025, con el ajuste de 2021 gravado al tipo teórico | La base queda uniforme también en 2021. Añade una regla fiscal distinta para un año, apoyada en una medida alternativa de rendimiento y en una cifra [LECTURA] | −0,202 · −0,226 |
| **A** | 2021–2025, todos sin efecto fiscal | Una sola regla. Para 2021 es una hipótesis contraria a la única indicación publicada | +0,416 · +0,466 |
| **C** | 2023–2025: la ventana | Deja en el τ de cinco años la distorsión de 2022; hay que declararlo | — |

Por qué B:
- aplica la regla donde su premisa está publicada y no la aplica donde la única indicación publicada la contradice;
- solo usa filas verificadas del CSV;
- A′ llega casi al mismo número con una regla más y con una estimación (que los 3,0 enteros tributaron al tipo teórico);
- A sería preferible solo si se acreditara que el ajuste de 2021 no fue deducible;
- no se elige por su efecto: frente a N1 en la ventana, B baja el flujo 0,302 y A lo sube 0,416. La diferencia entre ambas es el tratamiento fiscal de 2021, no el importe.

**Texto B:**

> «El alcance de N1 son los ejercicios que entran en el τ de proyección y tienen un ajuste de earnout no deducible según lo publicado: con la convención registrada de cinco años, 2022–2025. El ajuste de 2022, 2,4, se saca del EBIT y del resultado antes de impuestos de su año, sin efecto en el gasto por impuesto, con su fila de registro. El de 2021, (3,0), queda identificado y sin aplicar: su línea fiscal no está publicada y la única indicación publicada le atribuye efecto fiscal. Si se acredita su tratamiento fiscal, o si cambia la convención de τ (E8.1), el alcance se revisa.»

**Texto A′:**

> «El alcance de N1 son todos los ejercicios de τ: 2021–2025. El ajuste de 2022 se saca sin efecto en el gasto por impuesto. El de 2021 se saca con su efecto fiscal al tipo teórico de 2021, por la indicación de la medida neta de impuesto del URD 2021.»

**Texto A:**

> «El alcance de N1 son todos los ejercicios de τ: 2021–2025, todos sin efecto en el gasto por impuesto. La regla fiscal de 2021 se registra como hipótesis, con la indicación publicada en contra y su sensibilidad declaradas.»

**Texto C:**

> «El alcance de N1 es la ventana 2023–2025. Se declara que el τ de cinco años lleva dentro el ajuste no deducible de 2022.»

Con cualquiera de los cuatro:
- el margen objetivo se declara sin ajustes de earnout, como ya exige (5a);
- no cambian los históricos ni las entradas registradas: cada ajuste va en su fila;
- la cifra depende de la convención de τ y se declara con ella.

Qué cambiaría en la especificación (no se cambia en esta entrega):
- **E1, alcance:** el texto aprobado sustituye a «solo a la ventana o también a 2021–22».
- **Caso T16.** Hoy da los valores de C: τ de cinco años 0,28234; flujo sin crecimiento 236,891. Con B: tipo de 2022 = 0,2847; τ de cinco años = 0,28282; flujo sin crecimiento = 236,588 (−11,908 frente a T1); año 11 NORMAL −18,948. m0 = 0,131379 y f = 0,044900433 no cambian.
- **V-F1l:** con B, el ajuste de 2021 no es un ajuste aplicado. Se registra como partida identificada, con el motivo por el que no se aplica.

---

## 11. Qué no valida

- No aplica N1 ni cambia ninguna entrada: es una propuesta de alcance.
- **No acredita el tratamiento fiscal de 2021.** La indicación es una medida alternativa de rendimiento y no es concluyente.
- No explica por qué la línea fiscal de 2022 cuadra con 2,1 y no con 2,4.
- No normaliza el τ de cinco años de otras partidas (§7, punto 2).
- No decide si la actualización del earnout entra en la regla: es el documento hermano.
- No libera la valoración de Elis: R sigue pendiente, y N1 requiere además la clasificación de las compras, que la decisión (4b) deja pendiente hasta M6.
- Las [LECTURA] no son filas verificadas.
- Este documento no está revisado por un contexto distinto del autor.

---

## 12. Reproducción

Desde `scripts/`, con el árbol `munger_v2_r1` materializado y los PDF de la Release `fuentes-elis-e-20261117` del repositorio auxiliar:

    python3 -I n1_alcance_y_actualizacion.py --cifras ../datos/cifras_fuente.csv \
        --verificacion ../resultados/verificacion_cifras.json --libro <ruta>/Elis_v63_evaluada.xlsx \
        --copia ../resultados/copia_investigacion_f1.json \
        --salida ../resultados/n1_alcance_y_actualizacion.json --informe ../resultados/n1_alcance_y_actualizacion.md \
        --raiz <ruta>/munger_v2_r1 --release <carpeta de la Release>

Sin `--raiz` ni `--release`, el script calcula igual y deja las [LECTURA] sin comprobar. Termina con 1 si un control falla o si una [LECTURA] no está en su línea.
