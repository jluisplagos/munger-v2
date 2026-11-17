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

Cifras: `resultados/n1_alcance_y_actualizacion.{json,md}`, de `scripts/n1_alcance_y_actualizacion.py`. 98 controles, ninguno fallido; 93 de 93 [LECTURA] en su línea del PDF. Las páginas son páginas del PDF. Abreviaturas: URD21, URD22, URD23 y URD25 son los documentos de registro en inglés de 2021, 2022, 2023 y 2025; DEU24, el de 2024 en francés.

---

## 1. Respuesta corta

- **N1 cambia cómo se mide el tipo de un año:** gasto por impuesto ÷ resultado antes de impuestos (BAI) sin el ajuste de earnout. El τ de proyección es la media de los cinco tipos de 2021–2025 y multiplica a un margen que (5a) exige declarar sin esos ajustes. Aplicar N1 a tres de los cinco años deja en esa media dos definiciones del tipo. **El alcance coherente es el de τ: 2021–2025.**
- **Los ajustes de 2021 y 2022 son de la misma naturaleza que los de 2023–25** [P]: la misma línea de la misma nota, con la misma política contable, y no monetarios al registrarse.
- **Hay una razón real en contra, y afecta solo a 2021:** su tratamiento fiscal no está publicado [B]. La línea fiscal propia del earnout aparece en la conciliación del impuesto desde el ejercicio 2022. Aplicar a 2021 la parte fiscal de la regla («sin efecto en el gasto por impuesto») es una hipótesis [H].
- En 2022 la línea fiscal existe [P], con un matiz: cuadra con la cifra anterior a la reexpresión (2,1) y no con la vigente (2,4).
- **Efecto, con el τ de cinco años:** +0,416 en el flujo sin crecimiento y +0,466 en el año 11 NORMAL frente a N1 solo en 2023–25. Total frente al libro: −11,190 y −18,142. Solo se mueve el tipo; f y m0 no cambian [D].
- **Propuesta:** alcance 2021–2025 (opción A), con la regla fiscal de 2021 registrada como hipótesis y su sensibilidad a la vista. Si se exige una línea fiscal publicada para cada año ajustado, la alternativa es 2022–2025 (opción B).

---

## 2. Lo publicado, ejercicio por ejercicio

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Ajuste de earnout, nota 4.6 [P] | (3,0) | 2,4 | (48,9) | 8,7 | (0,2) |
| Fuente de la edición vigente | URD22 p.285 | URD23 p.302 | DEU24 p.296 | URD25 p.350 | URD25 p.350 |
| ¿En el CSV verificado? | Sí | Sí | Sí | Sí | Sí |
| Línea del estado de flujos que lo devuelve por no monetario | 2,9 [LECTURA: URD22 p.261] | (2,5) [LECTURA: URD23 p.279] | 48,4 | (9,3) | (0,1) |
| Línea fiscal propia en la conciliación del impuesto | No hay [B: URD21 p.290; URD22 p.326] | 0,5 [LECTURA: URD23 p.345] | (15,8) [P: DEU24 p.337] | 0,8 [LECTURA: URD25 p.392] | (0,2) [LECTURA: URD25 p.392] |
| (Ajuste − actualización) × tipo teórico [D] | −0,852, al 28,41 % | 0,620, al 25,83 % | −15,834 | 0,801 | −0,232 |
| ¿Cuadra con la línea publicada? | — | No con 2,4; sí con 2,1 | Sí | Sí | Sí |
| Pagos de earnouts y aplazados | Dentro del importe pagado de la nota 2.4, sin fila propia [I] | Ídem [I] | Fila propia: 34,4 [P] | 93,9 [P] | 23,3 [P] |

Precisiones:
- **2021.** El URD 2021 presentaba una sola línea: «Costs related to acquisitions and earnout adjustments», (5,1) [LECTURA: URD21 p.253]. El URD 2022 la separa en costes de transacción, (2,1), y ajustes de earnout, (3,0): 2,1 + 3,0 = 5,1 [D]. La cifra separada solo existe en la edición vigente.
- **2022.** El URD 2022 daba 2,1; el URD 2023 lo reexpresa a 2,4. El total de la nota no cambia: (9,0) en las dos ediciones. El cálculo usa 2,4, por la regla de la edición vigente.
- **Línea del estado de flujos.** En el URD 2022 se llama «Other»; el URD 2023 la rotula «Earnout adjustments and other elements with no impact on cash flows». En los cinco años vale el ajuste de earnout con el signo contrario, salvo una diferencia de −0,1 a −0,6: los otros elementos sin efecto en caja [D].
- **Tipos teóricos** [LECTURA]: 28,41 % en 2021 (URD22 p.326) y 25,83 % en 2022–2024 (URD23 p.345; DEU24 p.337; URD25 p.392). El de 2025 está en el CSV.
- **Actualización del earnout de México:** 12,4 / 5,6 / 0,7 en 2023–25 y nada en 2022 («–» [LECTURA: URD23 p.267]). Se trata en [N1_ACTUALIZACION_EARNOUT_MEXICO.md](N1_ACTUALIZACION_EARNOUT_MEXICO.md).

---

## 3. ¿Son de la misma naturaleza que los de 2023–25?

Sí, en todo lo que la empresa publica.

- **Misma línea y misma nota** [P]: «Earnout adjustments», nota 4.6 «Other operating income and expenses», en los cinco ejercicios (URD22 p.285; URD23 p.302; DEU24 p.296, «Ajustements de compléments de prix»; URD25 p.350).
- **Misma política contable de la nota** [P]: «Items of material amounts that are unusual, abnormal or infrequent are disclosed separately in the income statement», con el mismo texto en el URD 2022, el URD 2023 y el URD 2025.
- **No monetarios al registrarse** [P][D]: el estado de flujos los devuelve en los cinco años (tabla del §2).
- **Mismo pasivo** [P]: la deuda ligada a adquisiciones se mide a valor razonable, nivel 3, por flujos descontados, y existía al cierre de 2021 y de 2022: 27,1 y 90,4 [LECTURA: URD22 p.320]. El 27,1 incluye 1,2 de compromisos de recompra de minoritarios (6,5 + 19,3 + 1,2 = 27,0 [D]).
- **La suma de la nota cierra** [D]: las líneas de la nota 4.6 de 2021 suman (16,1), su total publicado; las de 2022 suman (9,1), frente a (9,0), dentro del redondeo de sus diez cifras.

Lo que no está publicado [B]:
- a qué adquisiciones corresponden los ajustes de 2021 y de 2022. Los de 2023 son «principalmente» de la compra de México [P: URD23 p.302];
- una fila propia de pagos de earnouts en 2021 y 2022. La nota 2.4 de esos años da el importe pagado por país. Ese importe incluye pagos de compras de años anteriores [I]: en 2021 se pagaron 9,4 en Brasil por compras cuyo precio fue 1,4; en 2022 se pagaron 7,8 en Rusia, donde no hubo ninguna compra ese año y quedaban 9,7 pendientes de 2021 [LECTURA, columnas por país: URD22 p.275 y p.277]. Eso sitúa los pagos aplazados dentro de las adquisiciones; no identifica cuáles son earnouts.

---

## 4. ¿Su registro sigue la misma regla?

N1 exige una fila de ajuste por año con su fuente, su regla fiscal y la ubicación de su caja (especificación, E1; control V-F1l). La fila del EBIT publicado no cambia.

| Requisito | 2021 | 2022 | 2023–25 |
|---|---|---|---|
| Partida e importe con fuente | (3,0) [P]; fila verificada | 2,4 [P]; fila verificada. 2,1 en la edición anterior | [P]; filas verificadas |
| Regla fiscal: no deducible, gasto sin cambios | **Sin línea fiscal propia [B].** Por identidad de naturaleza, [H] | Línea propia: 0,5 [P]. Cuadra con 2,1 y no con 2,4 | Línea propia [P]. Cuadra con el ajuste y la actualización |
| Ubicación de la caja: adquisiciones, fuera del FCF base | Importe pagado de la nota 2.4 [I] | Ídem [I] | Fila propia de la nota 2.4 [P] |

Conclusión:
- **2022** cumple los tres requisitos, con dos matices declarados: la línea fiscal no cuadra con la cifra reexpresada, y la caja se sitúa por inferencia.
- **2021** cumple el primero. El segundo no está publicado. El tercero es una inferencia.

---

## 5. Por qué el alcance debe ser el de τ

1. **El tipo se aplica a una base y debe medirse sobre la misma base** [D].
   - En la proyección, el NOPAT es margen × (1 − τ). El margen se declara sin ajustes de earnout: es una condición de (5a), y m0 sale del EBIT de 2025 sin el ajuste.
   - El tipo que lo multiplica debe medirse sobre un resultado sin esos ajustes en **todos** los años que lo forman.
2. **Con N1 solo en la ventana, la media mezcla dos definiciones** [D].
   - Tres tipos (2023–25) quedarían medidos sobre el BAI sin ajustes de earnout y dos (2021–22) sobre el BAI con ellos.
   - El resultado no sería el tipo de ninguna definición.
3. **Cada uso de la regla alcanza a los años que entran en ese uso** [D].
   - El EBIT de 2021 y 2022 no entra en f ni en m0: la ventana de calibración es 2023–25. Para el EBIT, el alcance es la ventana.
   - El tipo de 2021 y 2022 sí entra en τ. Para el tipo, el alcance son los cinco años.
   - El script lo comprueba: en todos los escenarios, f y m0 son idénticos a los de N1 en 2023–25, y la variación es exactamente −V₀·m0·Δτ.
4. **La regla se aprobó por la naturaleza de la partida** [Pol, (5a)].
   - El año de 2021 es un cargo y el de 2022 un abono. Aplicar la regla según el año, el signo o el tamaño sería elegirla por su efecto.
5. **Si cambia la convención de τ, el alcance la sigue.** Con el τ de la ventana (convención no adoptada), 2021 y 2022 no entrarían en ningún cálculo y la cuestión desaparecería.

---

## 6. Razones en contra encontradas

1. **2021 no tiene línea fiscal publicada** [B]. Es la única razón de fondo.
   - Ni el URD 2021 (p.290) ni el URD 2022 (p.326) separan el earnout en la conciliación del impuesto de 2021. Si no fue deducible, su efecto (0,852) estaría dentro de «Permanent differences», (12,2) [I].
   - Lo mismo pasaba con 2022 en el URD 2022. La línea propia la crea el URD 2023, que la da también para 2022. Para 2021 no se ha publicado nunca.
   - **Indicio publicado en contra, débil** [P][I]: la medida «net income from ordinary operations» del URD 2021 presenta los costes de adquisición y ajustes de earnout de 2021 netos de impuesto: 3,7 frente a 5,1 (URD21 p.217). Es el resultado de aplicar el 28,41 % a toda la línea (3,651); sin efecto fiscal en el earnout saldría 4,503 [D].
   - Por qué es débil: en 2021 esa medida aplica el tipo teórico a la nota 4.6 entera, 11,5 frente a 16,1, un 28,6 % [LECTURA: URD22 p.249]. Es una convención general, no un análisis partida a partida. En 2023 la misma medida ya no la aplica: 64,6 frente a 67,9, un 4,9 % [LECTURA: URD23 p.267].
   - Lo que está en juego [D]: si el ajuste de 2021 llevara impuesto al tipo teórico, el tipo de 2021 sería 0,3302 en lugar de 0,3253, y el efecto del alcance pasaría de +0,416 a −0,202.
2. **En 2022 la línea fiscal cuadra con 2,1 y no con 2,4** [D].
   - 2,4 × 25,83 % = 0,620, frente a 0,5 publicado: residuo −0,120, mayor que la cota de redondeo (0,063). Con 2,1, 0,542: cuadra.
   - Lecturas posibles [H]: el comparativo fiscal no se actualizó con la reexpresión, o una parte del ajuste (0,3 a 0,5) tributa.
   - Si tributara la parte que la línea no cubre, el tipo de 2022 sería 0,2843 en lugar de 0,2847, y el efecto del alcance, +0,466 en lugar de +0,416. No cambia la conclusión.
3. **Extender N1 no deja el τ de cinco años «normalizado»** [D]. Solo hace uniforme la regla del earnout.
   - En los años de τ hay otras partidas no deducibles que N1 no toca. La mayor es el deterioro del fondo de comercio de 2022: 58,7, con línea fiscal propia de (15,1) [LECTURA: URD23 p.345].
   - Mueve el tipo de 2022 de 0,2337 a 0,2823: 0,0097 en el τ de cinco años, unos 6,1 en el flujo sin crecimiento. El alcance de N1 mueve 0,0007.
   - **No se propone normalizarla:** (5a) aprobó que ninguna otra partida se normaliza, y la convención de τ es E8.1. Se declara para que el alcance de N1 no se lea como una depuración del tipo.
4. **La caja de 2021–22 se sitúa por inferencia** [I] (§3).
5. **Las dos cifras nuevas no tienen identidad entre páginas.** Están verificadas en el CSV, sin incoherencia detectada. Su segunda línea es la suma de su propia nota y la línea del estado de flujos, que son [LECTURA].

Ninguna de estas razones se refiere a la naturaleza de la partida. La primera es una carencia de evidencia fiscal en un año; las demás son matices y límites.

---

## 7. Efecto recalculado

Perímetro `A0_total`; la variación es idéntica en `A1_sin_ROU` y `A2_propio`. τ de proyección de cinco años. Año 11: MALO / NORMAL / BUENO.

| Alcance | Tipo de 2021 · 2022 | τ de cinco años | Frente al libro: flujo sin crecimiento · año 11 | Frente a N1 en 2023–25: flujo · año 11 |
|---|---|---|---|---|
| Libro, sin ajustes | 0,3310 · 0,2823 | 0,28820 | — | — |
| **C** · N1 en 2023–25 | 0,3310 · 0,2823 | 0,28234 | −11,605 · −15,433 / −18,609 / −19,976 | — |
| **A** · N1 en 2021–25, sin efecto fiscal | 0,3253 · 0,2847 | 0,28168 | −11,190 · −15,093 / −18,142 / −19,433 | +0,416 · +0,341 / +0,466 / +0,543 |
| **B** · N1 en 2022–25 | 0,3310 · 0,2847 | 0,28282 | −11,908 · −15,681 / −18,948 / −20,371 | −0,302 · −0,248 / −0,339 / −0,395 |
| Descomposición: 2023–25 y 2021 | 0,3253 · 0,2823 | 0,28120 | −10,887 · −14,845 / −17,803 / −19,037 | +0,718 · +0,588 / +0,806 / +0,939 |
| Sensibilidad de A: 2021 gravado al 28,41 % [LECTURA] | 0,3302 · 0,2847 | 0,28266 | −11,807 · −15,599 / −18,835 / −20,240 | −0,202 · −0,165 / −0,226 / −0,264 |
| Sensibilidad de A: en 2022 tributa lo que la línea fiscal no cubre [LECTURA] | 0,3253 · 0,2843 | 0,28160 | −11,139 · −15,052 / −18,086 / −19,367 | +0,466 · +0,382 / +0,523 / +0,609 |

Lectura:
- El +0,416 de la propuesta se reproduce y se descompone: +0,718 de 2021 y −0,302 de 2022 [D].
- El signo del conjunto depende del tratamiento fiscal de 2021: +0,416 sin efecto fiscal y −0,202 con él.
- Todas las variantes quedan entre −0,302 y +0,718, el 0,1–0,2 % del FCF base. **Es pequeño en cualquier caso: la elección es de coherencia y de evidencia, no de importe.**
- Tratar 2021 como gravado equivale casi a no aplicarle N1: −0,202 frente a −0,302. Quitar del BAI un gasto que lleva su impuesto apenas cambia el tipo.

Controles de reproducción:
- el libro: f, τ de cinco años, flujo sin crecimiento y los tres flujos del año 11;
- las cifras de la propuesta, §5.1: −11,605 · −18,609; −11,190 · −18,142; +0,416 · +0,466;
- la salida ya contrastada de `copia_investigacion_f1.py`, cifra a cifra.

---

## 8. Qué está en el CSV verificado y qué sería [LECTURA] nueva

**El cálculo de A, B y C solo usa filas verificadas del CSV** (762 filas: 748 OK, 14 PENDIENTE, 0 FALLO; todas las de aquí, OK en sus seis dimensiones):

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
| Línea fiscal del earnout de 2022: 0,5 | URD23 p.345 | Regla fiscal de 2022 | **Sí**, si se aprueba A o B: es la evidencia que V-F1l pide registrar |
| Línea fiscal de 2024 y 2025, edición vigente: 0,8 y (0,2) | URD25 p.392 | Regla fiscal de 2024–25; hoy el CSV tiene la de 2024 como edición anterior y no tiene la de 2025 | **Sí**: afecta a la regla ya aprobada |
| Tipos teóricos de 2021–2024: 28,41 % y 25,83 % | URD22 p.326; URD23 p.345; DEU24 p.337; URD25 p.392 | Cuadre de la línea fiscal; el de 2021 entra en una sensibilidad | Sí, si el cuadre se registra como control |
| Línea no monetaria del estado de flujos de 2021 y 2022: 2,9 y (2,5) | URD22 p.261; URD23 p.279 | Segunda línea de los ajustes de 2021–22 | Recomendable |
| Total de la nota 4.6 de 2021 y 2022 y sus líneas | URD22 p.285; URD23 p.302 | Suma de la nota | Recomendable |
| Línea conjunta de 2021: (5,1); medidas netas de impuesto: 3,7; 11,5; 7,0; 64,6 | URD21 p.253 y p.217; URD22 p.249; URD23 p.267 | Indicio fiscal de 2021 | No hace falta: es evidencia de contexto |
| Actualización de 2022: «–»; gastos de actualización de 2022: (0,3) | URD23 p.267 y p.332; URD22 p.313 | Que en 2022 no hubo actualización del earnout | Sí, si se incluye la actualización |
| Deterioro de 2022, línea fiscal: (15,1) | URD23 p.345 | Límite declarado | No |
| Pasivo de 2021–22 y pagos por país | URD22 p.275, p.277, p.286, p.320 y p.321 | Ubicación de la caja | Los pagos por país no son del perímetro del grupo: seguirían [LECTURA] |

No se ha añadido ninguna fila al CSV en esta entrega: pasar cifras al CSV es un bloque propio, con su verificación y su revisión.

---

## 9. Opciones y texto que se pediría aprobar

| Opción | Alcance | Qué supone | Efecto frente a N1 en 2023–25 |
|---|---|---|---|
| **A** (propuesta) | 2021–2025: todos los ejercicios de τ | Una sola definición del tipo. La regla fiscal de 2021 es una hipótesis [H] | +0,416 · +0,466 |
| **B** | 2022–2025: los ejercicios con línea fiscal publicada | Evidencia fiscal publicada en todos los años ajustados. El tipo de 2021 conserva dentro un ajuste de (3,0) | −0,302 · −0,339 |
| **C** | 2023–2025: la ventana | El τ de cinco años promedia dos años sin normalizar; hay que declararlo | — |

Por qué A y no B: la regla se define por la naturaleza de la partida, que está publicada en los cinco años, y lo que falta en 2021 es una línea de desglose que la empresa no publicaba entonces para ningún año. Por qué B podría preferirse: es la única opción en la que cada año ajustado tiene su regla fiscal publicada.

**Texto A:**

> «El alcance de N1 son todos los ejercicios que entran en el τ de proyección: con la convención registrada de cinco años, 2021–2025. Los ajustes de earnout de la nota 4.6 de 2021, (3,0), y de 2022, 2,4, se sacan del resultado antes de impuestos de su año, sin efecto en el gasto por impuesto, con su fila de registro. La regla fiscal de 2021 se registra como hipótesis, porque su línea fiscal no está publicada, con su sensibilidad declarada. Si cambia la convención de τ (E8.1), el alcance la sigue.»

**Texto B:**

> «El alcance de N1 son los ejercicios de τ con línea fiscal publicada del earnout: 2022–2025. El ajuste de 2021, (3,0), queda identificado y sin aplicar mientras no se acredite su tratamiento fiscal; se declara que el tipo de 2021 lo lleva dentro.»

**Texto C:**

> «El alcance de N1 es la ventana 2023–2025. Se declara que el τ de cinco años promedia 2021 y 2022 sin normalizar.»

Con cualquiera de los tres:
- el margen objetivo se declara sin ajustes de earnout, como ya exige (5a);
- no cambian los históricos ni las entradas registradas: cada ajuste va en su fila;
- la cifra depende de la convención de τ y se declara con ella.

---

## 10. Qué no valida

- No aplica N1 ni cambia ninguna entrada: es una propuesta de alcance.
- No acredita el tratamiento fiscal de 2021.
- No normaliza el τ de cinco años de otras partidas (§6, punto 3).
- No decide si la actualización del earnout entra en la regla: es el documento hermano.
- No libera la valoración de Elis: R sigue pendiente, y N1 requiere además la clasificación de las compras ((4b), opción A: pendiente hasta M6).
- Las [LECTURA] no son filas verificadas.
- Autor y revisor deben ser contextos distintos: este documento no está revisado.

---

## 11. Reproducción

Desde `scripts/`, con el árbol `munger_v2_r1` materializado y los PDF de la Release `fuentes-elis-e-20261117` del repositorio auxiliar:

    python3 -I n1_alcance_y_actualizacion.py --cifras ../datos/cifras_fuente.csv \
        --verificacion ../resultados/verificacion_cifras.json --libro <ruta>/Elis_v63_evaluada.xlsx \
        --copia ../resultados/copia_investigacion_f1.json \
        --salida ../resultados/n1_alcance_y_actualizacion.json --informe ../resultados/n1_alcance_y_actualizacion.md \
        --raiz <ruta>/munger_v2_r1 --release <carpeta de la Release>

Sin `--raiz` ni `--release`, el script calcula igual y deja las [LECTURA] sin comprobar. Termina con 1 si un control falla o si una [LECTURA] no está en su línea.
