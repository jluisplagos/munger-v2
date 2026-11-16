# Especificación económica propuesta · F1 · motor A con NIIF 16 e intangibles adquiridos

Fecha: 15-nov-2026; revisada el 16-nov-2026 para que coincida con la revisión 3 de [PROPUESTA_DECISIONES_F1.md](PROPUESTA_DECISIONES_F1.md) (respuesta a la revisión de la propuesta, F1-P1 a P4, y correcciones V1–V11 de la revisión dirigida: E2–E6, E8 y E9). Autor: frente E. Estado: **propuesta, no adoptada ni implementada**.

**Corregida según V1–V11** de la revisión dirigida a P1–P4 (commit `8fcc7fd`; [revision/REVISION_PROPUESTA_P1_P4.md](revision/REVISION_PROPUESTA_P1_P4.md)). Detalle en [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md):
- V2: el ancla de E4 excluye lo que se cobra como término explícito; V-F1i, V-F1j y T15;
- V5: la amortización ROU en `perimetro_margen` y en E8.5;
- V6: el terminal usa la comparación del libro (Convenciones V6.3 §3); V-F1k;
- V7: fórmula de los términos explícitos en E3;
- V9: T8 y T15;
- V10: E2 y E4 coinciden con E5;
- V4: T16 declara su convención y su alcance.

Las correcciones no están revisadas todavía; se revisarán externamente solo en lo afectado.

Fundamento: [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md), `resultados/contraste_f1.json`, `resultados/copia_investigacion_f1.json` (copia de investigación, no entradas registradas) y `resultados/controles_sinteticos_f1.json` (ejemplos de política con importes ficticios).

## E0. Condiciones previas

1. Decisión F1 de la persona responsable con la política completa, (a), (b) o (c), según el informe, §10. **Esta especificación solo se aplica si la decisión es (b)**, o (c) con estas reglas como guía del juicio.
2. Implementación sobre una versión técnica fijada por commit del frente T, que se cita. Antes de implementar, comprobar que esa versión no cambia los datos o definiciones usados aquí: Historia filas 6–18, Análisis C46–C52, C57, C58, C70 y Motor. En `d1f1fa9` solo cambia la declaración del signo de los componentes de C48.
3. Conservar: E1, D3, E2 y E6 tal como están registradas; C48 = 108 con su derivación; C52 = 307,933. Expedientes nuevos, con el anterior conservado.
4. No elegir el perímetro por su efecto en el precio. El perímetro y la política PPA son decisiones (informe §10, puntos 2–4).

## E1. Entradas nuevas de la Historia (por año, columnas C–L)

| Fila nueva (propuesta) | Contenido | Fuente en Elis | Regla |
|---|---|---|---|
| D&A de derechos de uso (NIIF 16) | Amortización ROU del año (magnitud) | Nota 4.5 («Right-of-use assets») | Cifra publicada entre paréntesis: declarar `valor_fuente` negativo, `signo` −1 y `tratamiento` (R415-SIGNO). Vacío = desconocido; 0 solo si se verifica |
| Amortización de intangibles de combinaciones (PPA) | Amortización de lo adquirido (magnitud) | Nota 4.5 / cuenta de resultados | Ídem |
| Reinversión necesaria estimada (solo perímetro A3) | Estimación documentada por año, con rango, separada en R_propia (capex propio necesario, incluida la dotación a los clientes que sustituyen a los perdidos), R_compras (compras de cartera necesarias para mantener las ventas) y la inversión de transición de sostenimiento | No publicada (M1, M2, M6) | Exige fuente, método, rango y responsable; nunca se presenta como dato publicado |
| Inversión de transición (si se clasifica aparte; propuesta, 5b) | Importe por año, finalidad (sostenimiento permanente, sostenimiento u obligación temporal, crecimiento) y horizonte | No publicada (M1) | Sin importe u horizonte: vacío, que es desconocido, no cero |
| Ajustes de normalización (solo si se aprueba la regla N1; propuesta, 5a) | Por año: partida, importe original, fuente, regla fiscal y ubicación de su caja | Nota 4.6 (ajustes de earnout) | La fila del EBIT publicado no cambia; el ajuste va en una fila propia |

Opcional, para el diagnóstico: compras de lino y amortización de lino, y pagos totales de arrendamientos.

Invariantes: D&A ROU ≤ D&A total, PPA ≤ D&A total y D&A ROU + PPA ≤ D&A total (fila 8).

## E2. Parámetro declarado: perímetro de la reinversión necesaria

Nuevo parámetro de configuración del motor A, `perimetro_reinversion`, con estos valores admisibles:

| Valor | D_X,t (D&A que se supone repuesta con capex propio) | Uso |
|---|---|---|
| `A1_sin_ROU` | D&A total − D&A ROU | Arrendamientos coherentes; la PPA se trata como reposición monetaria |
| `A2_propio` | D&A total − D&A ROU − PPA | Arrendamientos coherentes; la PPA, no monetaria y sin reposición |
| `A3_estimado` | Reinversión necesaria estimada (E1) | Si hay dato o estimación documentada |
| `A0_total` | D&A total | **Solo** si D&A ROU = 0 y no hay pagos de arrendamientos en el FCF base (C49 = 0). Es la V6.3 actual |

El parámetro es una decisión: se registra con fecha, persona y motivo, como E1–E6. No lo rellena el agente.

**Parámetro declarado del perímetro del margen** (revisión independiente, O12): `perimetro_margen`, con estos valores admisibles:

| Valor | Significado |
|---|---|
| `EBIT_NIIF16_PPA_constante` | El margen objetivo incluye la PPA y la amortización ROU como **proporción constante de las ventas**, las mismas que devuelve f (la PPA en `A2_propio`; la ROU en `A1_sin_ROU` y `A2_propio`; en cada caso, media ÷ ventas medias de la ventana). No significa constante en euros. m0 es el margen real del año base, y en Elis los efectos de escala se declaran (`copia_investigacion_f1.json`): PPA, 1,7866 % en m0 frente a 1,8743 % en f, **+4,206**, que sube el flujo sin crecimiento de A2; ROU, 3,1167 % frente a 2,9057 %, **−10,118**, que baja el de A1 y A2; las dos en A2, −5,913. Los casos sintéticos P2g–P2i muestran que solo la proporción constante se anula en el flujo |
| `EBIT_NIIF16_PPA_decreciente` | El margen objetivo incluye una PPA que se agota según el valor neto publicado |
| `EBIT_NIIF16_sin_PPA` | El margen objetivo excluye la PPA |
| `margen_despues_de_arrendamientos` | El margen objetivo es posterior a los pagos de arrendamiento (EBITDAaL o similar) |

Combinaciones coherentes con `perimetro_reinversion`:
- `A2_propio` exige `EBIT_NIIF16_PPA_constante`, porque f devuelve la PPA entera de forma perpetua.
- **No admisibles por ahora** (revisión n.º 3, N4). Disparan V-F1h hasta que se especifiquen con su fórmula y su prueba:
  - `margen_despues_de_arrendamientos`: la variante A1′ solo quita de f el principal (C49), y el interés de arrendamiento sigue en C48. Con un margen posterior a los pagos se contaría dos veces: 25,067 de media, 26,4 en la base 2025, antes de impuestos. Quitarlo de C48 chocaría con E0.3. Una definición posible, no adoptada: calibrar f con el NOPAT calculado sobre el mismo margen que se proyecta y con la reinversión sin ROU;
  - `EBIT_NIIF16_PPA_decreciente` con `A2_propio`: devolver solo la PPA proyectada exige una f que cambie con el tiempo o un término **no monetario**, con su efecto fiscal nocional. Los términos explícitos de E3 son solo de caja (inversión) y no cubren este caso.
- Cualquier otra combinación dispara V-F1h.

**Matriz de coherencia de los tres perímetros** (revisión, O4 y O12). El margen objetivo, la reinversión que calibra f (E3) y el ancla de la palanca S2C (E4) deben describir el mismo tratamiento del arrendamiento y de la PPA:

| `perimetro_reinversion` | `perimetro_margen` coherente | f (E3) | Ancla de la palanca S2C (E4) | Si no casa |
|---|---|---|---|---|
| `A0_total` | EBIT NIIF 16 con PPA constante | Reinversión con D&A total | C53 con D&A total | V-F1a si hay arrendamientos, con cualquier importe (E5) |
| `A1_sin_ROU` | `EBIT_NIIF16_PPA_constante`: la PPA se trata como coste de reposición que persiste | Reinversión con D&A total − ROU | C53 con el mismo D_X | V-F1h (margen) o V-F1g (ancla) |
| `A2_propio` | `EBIT_NIIF16_PPA_constante` (con `…_decreciente`: no admisible por ahora) | Reinversión con D&A propia; f devuelve la PPA entera | C53 con D&A propia | V-F1h o V-F1g |
| `A3_estimado` | El que declare la estimación para la PPA; si no lo declara, el de `A2_propio` | Reinversión con la D_X estimada (E1) | C53 con la misma D_X | V-F1d (estimación incompleta), V-F1h o V-F1g |
| Cualquiera con `margen_despues_de_arrendamientos` | No admisible por ahora: A1′ deja el interés de arrendamiento en f (N4) | — | — | V-F1h |

En este expediente las palancas S2C (1 / 1,2 / 1,5) no se anclan en C53 sino en un perímetro propio (informe §3). Con cualquier perímetro de reinversión, la regla V-F1g bloquearía (E5).

**El terminal entra en la misma matriz** (revisión de la propuesta, P4). El terminal no usa S2C: reinvierte g∞/ROIC del NOPAT (E4). El ROIC de las palancas (Palancas fila 18) declara su perímetro (`perimetro_roic`), que debe ser el del ancla de S2C:
- NOPAT del perímetro del margen;
- capital de crecimiento con adquisiciones si el ancla las lleva;
- sin la ROU, porque el arrendamiento se paga en f;
- sin R, porque la reposición está en f.

Sin declaración, o con otro perímetro, salta V-F1k.

**Otras declaraciones** (propuesta, decisiones 2, 4b y 5b). Cada una se registra con fecha, persona y motivo, como E1–E6, y no la rellena el agente:

| Parámetro | Valores admisibles | Si falta |
|---|---|---|
| `clasificacion_compras` | `crecimiento_por_hipotesis` (hipótesis registrada, con su fundamento y su apoyo parcial: propuesta, 4b); `reposicion_con_importe` (por año: R_compras dentro de D_X, solo con `A3_estimado`; con `A1_sin_ROU` o `A2_propio`, término explícito de E3, fuera del ancla de E4); `pendiente` | V-F1j |
| `tratamiento_transicion` | `en_R` (sostenimiento permanente y proporcional a las ventas: en f crece con ellas); `termino_explicito` (importe por año y horizonte; término de E3, fuera del ancla de E4); `crecimiento` (amplía capacidad: dentro de la inversión de crecimiento y del ancla); `pendiente` | V-F1i |
| `perimetro_roic` | El mismo valor que el perímetro de las palancas S2C | V-F1k |

**Correspondencia de costes.** La tabla de la propuesta, §2, es parte de esta especificación: cada coste tiene un solo sitio en la ventana, en los años 1–10 y en el terminal. Los casos de `controles_sinteticos_f1.py` (T15) la comprueban, también a crecimiento cero.

## E3. Calibración de f

Misma ventana (C57) y mismas guardas que el C58 actual, sustituyendo la D&A total por D_X en la reinversión:

f = { Σ_w EBIT_t·(1 − τ_t) ⁄ n − Σ_w (capex_t − D_X,t + ΔWC_t) ⁄ n − FCF base } ÷ (Σ_w V_t ⁄ n)

- La conciliación de las filas 73–81 debe mostrar D_X media y sus componentes. Recomendado: también la composición económica de f del informe, §4.2 (arrendamientos, intereses, impuesto, capex neto/bruto, partidas no monetarias), con su suma igual a C79.
- **Tratamiento fiscal.** El cambio de perímetro es antes de impuestos. Los efectos fiscales reales ya están en los impuestos pagados que calibran f; en Elis, el diferido de intangibles aporta 15,5/20,3/17,5 y el de NIIF 16 es casi neutro. No se añade ningún escudo fiscal adicional. Hay que declarar la limitación: el efecto fiscal se escala con las ventas aunque la PPA se agote.
- **Normalización: solo si se aprueba la regla N1** (propuesta, 5a). El 27,936 de `partidas_puntuales_en_flujo_sin_crecimiento` es un diagnóstico y no se deduce.
  - N1 saca los ajustes de earnout de la nota 4.6 del EBIT y del resultado antes de impuestos de su año, con el gasto por impuesto sin cambios, porque no son deducibles.
  - Se recalcula el tipo de ese año con la convención de la fila 10 (gasto ÷ BAI, 4 decimales) y, con él, el NOPAT de la ventana, f, el τ de 5 años y m0.
  - Los históricos no cambian: el ajuste va en su fila (E1).
  - **Alcance.** El texto aprobado dice si alcanza solo a la ventana 2023–25 o también a 2021–22, que solo entran en el τ de cinco años (ajustes (3,0) y 2,4 [LECTURA]: +0,416 en el flujo sin crecimiento). La propuesta lo deja como opción de (5a).
  - **Caja.** Los pagos de earnouts están en las adquisiciones, en inversión, fuera del FCF base [P: nota 2.4]. N1 es coherente solo si las compras se cobran como compras (propuesta, 4b o M6).
  - **Convención.** La cifra depende de la convención del τ de proyección (E8.1): −11,605 con la registrada de cinco años y −9,141 con la de la ventana. Se declara con ella.
  - **Actualización del earnout.** Es financiera y no deducible (12,4 / 5,6 / 0,7 [LECTURA]). No entra en N1 mientras sus cifras no estén en el CSV verificado; su efecto sería −0,790.
  - N2 (bajas de 2025 con seguros) no se aplica mientras su fiscalidad y su caja no estén identificadas.
  - Ninguna partida se normaliza por su etiqueta.
  - Valores de referencia condicionales: T16.
- **Estructura del flujo y términos explícitos** (revisión dirigida, V7). La estructura de las Convenciones §1–§3 no cambia, salvo los términos explícitos de caja que declaren `tratamiento_transicion = termino_explicito` o `clasificacion_compras = reposicion_con_importe` fuera de D_X:
  - años 1–10: flujo_t = V_t·[m_t(1−τ) − f] − ΔV_t/S2C − X_t;
  - año 11: V₁₀·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f] − X₁₁;
  - para una transición con importe T_t y horizonte H: X_t = T_t si t ≤ H, y 0 si t > H. X₁₁ = 0 si H ≤ 10. Una transición permanente no va como término sino en R, o se declara proporcional;
  - para compras de reposición proporcionales a las ventas, con proporción a: X_t = a·V_t y X₁₁ = a·V₁₁. Con importes por año documentados, esos importes;
  - X_t es inversión: no lleva efecto fiscal, como ΔV/S2C;
  - lo que se cobra en X sale del denominador del ancla de S2C (E4);
  - comprobación: casos V2b y V2g de `controles_sinteticos_f1.py`.

## E4. Ancla de S2C con el mismo perímetro

C53 = (V_L − V_G) ÷ Σ_{H..L} (capex − D_X + ΔWC + adquisiciones − X^v)

X^v es lo que, en los años del ancla, corresponde a desembolsos que la proyección cobra como términos explícitos de E3: la transición con `termino_explicito` y las compras de reposición fuera de D_X (revisión dirigida, V2). Lo que se cobra fuera de ΔV/S2C y no está en D_X sale del denominador. Si no, con crecimiento se cobra dos veces (casos V2a y V2f; corregidos en V2b y V2g). Lo que está en D_X ya queda fuera por la resta de D_X (V2c y V2h).

- Variante orgánica opcional, si se dispone del crecimiento orgánico publicado. **El crecimiento orgánico publicado es nominal e incluye precio** (informe §3, §6.2). La variante debe declararse como nominal o deflactarse con un efecto precio documentado; nunca se presenta como productividad en volumen.
- Las palancas S2C (Palancas B16:D16) deben declarar el perímetro con que se anclan. Si no coincide con `perimetro_reinversion`, salta V-F1g, que bloquea (E5).
- Con la palanca anclada en C53 y el perímetro `A0_total`, el exceso de arrendamientos de los años 1–10 disminuye con el crecimiento y se anula cerca del crecimiento histórico. A crecimiento cero y en el terminal persiste (informe §5.3). Por eso V-F1a no depende del ancla.
- Si se documentan compras de reposición, el denominador del ancla no las incluye: dentro de D_X, por la resta de D_X; como término explícito, por X^v. Contarlas en los dos sitios las cobra dos veces con crecimiento, aunque a crecimiento cero el caso parezca coherente (casos sintéticos P2c y V2f).

**Terminal.** Terminal = V₁₀·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f]. No usa S2C.
- La inversión de crecimiento del terminal es g∞/ROIC del NOPAT, antes de f. f persiste a perpetuidad, con todos los costes que contiene.
- **Comparación numérica: la del libro** (revisión dirigida, V6). Convenciones V6.3 §3: «En el año 11 la rentabilidad del capital pasa de S2C·m_obj·(1−τ) a ROIC; el salto se muestra en Diagnóstico V6, bloque 10, y avisa si supera C179». En Elis: `Diagnóstico V6`, filas 176–179; umbral C179 = 5 puntos, «ajustable». V-F1k usa esa comparación y ese umbral: AVISO si el salto lo supera, INFORMA si no. No se añade otra comparación ni otro umbral, y esta especificación no cambia el vigente.
- **Igualdad exacta (INFORMA).** El año 11 cobra exactamente la inversión de ΔV/S2C si ROIC = (1+g∞)·m_obj·(1−τ)·S2C, por el tiempo del motor. La fórmula del libro difiere solo en el factor (1+g∞): con un salto nulo según el libro, el año 11 cobra (1+g∞) veces ΔV/S2C (caso P4e). Se muestra como precisión, sin consecuencia propia.
- Con g∞ = 0, el terminal es V₁₀·[m_obj(1−τ) − f]: un coste recurrente que solo se cobre como crecimiento desaparece también aquí (casos P2a y P4c).
- En Elis, con las palancas actuales, la rentabilidad marginal del libro (fila 176) es 7,4739 % / 10,6770 % / 14,4140 % frente a un ROIC de 7 % / 10 % / 12 %. Los saltos son de −0,47, −0,68 y −2,41 puntos, por debajo del umbral, así que V-F1k informa. Con la igualdad exacta, el ROIC sería 7,55 % / 10,89 % / 14,77 %. La compatibilidad queda pendiente de R y del perímetro de las palancas (`copia_investigacion_f1.json`).

## E5. Reglas de control

**Severidad** (la misma que en el texto de aprobación de la propuesta; revisión de la propuesta, P4):
- **BLOQUEA:** el resultado del motor A no se usa para una conclusión. Puede calcularse y mostrarse como diagnóstico, rotulado con el control que salta.
- **AVISO:** se muestra, no bloquea y no acredita coherencia.
- **INFORMA:** información para quien decide.

| Id | Condición | Severidad | Efecto |
|---|---|---|---|
| V-F1a | Motor A, Σ D&A ROU > 0 en la ventana, C49 > 0 y perímetro `A0_total` | **BLOQUEA**, con cualquier importe. **No se adopta umbral de materialidad**: el 0,5 % de la versión anterior no se adopta. Un umbral, si se quiere, es una decisión aparte, y esta especificación no propone ninguna cifra | **MODELO NO APLICABLE** («coste de arrendamiento contado dos veces en la proyección»), no «datos inválidos»: los datos son correctos y la incoherencia es de definición (revisión, O12) |
| V-F1b | Motor A, C49 > 0 y fila de D&A ROU vacía en algún año de la ventana | **BLOQUEA** | **INCOMPLETO** (vacío ≠ 0) |
| V-F1c | R_propia media > capex propio medio, o R_compras media > compras medias, en la ventana. **No se compara R total con el capex propio**: R puede superar el capex propio sin infrainversión si incluye compras de cartera (caso sintético `guarda_R_frente_a_capex`) | **AVISO** con justificación obligatoria (hipótesis de infrainversión documentada); sin ella, **BLOQUEA** | Sin justificación, la entrada pasa a «hipótesis pendiente» |
| V-F1d | `A3_estimado` sin fuente, método, rango o responsable, o sin declarar cómo trata la reposición de clientes (R_propia, R_compras) y la inversión de transición | **BLOQUEA** | **INCOMPLETO** |
| V-F1e | Invariantes de E1 incumplidos o signos sin declarar | **BLOQUEA** | **DATOS INVÁLIDOS** |
| V-F1f | `A2_propio` con PPA > 0, o `A1_sin_ROU` / `A2_propio` con D&A ROU > 0 | **INFORMA** | Valor neto de los intangibles adquiridos ÷ PPA (años de agotamiento al ritmo actual); si las altas del último ejercicio son provisionales; efectos de escala de la PPA y de la amortización ROU (proporción en m0 frente a la que devuelve f) y su sentido |
| V-F1g | Perímetro declarado de las palancas S2C ≠ `perimetro_reinversion`, o sin declarar | **BLOQUEA** (antes AVISO) | **MODELO NO APLICABLE** para una conclusión; se muestra la diferencia de anclas S2C entre perímetros |
| V-F1h | `perimetro_margen` incompatible con `perimetro_reinversion` (E2) | **BLOQUEA** | **MODELO NO APLICABLE** hasta que se declare una combinación coherente |
| V-F1i | `tratamiento_transicion` sin declarar o `pendiente` cuando hay una transición conocida, publicada o documentada aunque sin importe; `termino_explicito` sin importe u horizonte; transición cobrada dos veces (en R y como término, o como término y también en el denominador del ancla de S2C) o ninguna | **BLOQUEA** | **INCOMPLETO** o **MODELO NO APLICABLE**. Nunca cero por defecto |
| V-F1j | `clasificacion_compras` sin declarar o `pendiente`; `reposicion_con_importe` sin importe por año; compras de reposición cobradas en R, o como término explícito, y también en el denominador del ancla de S2C | **BLOQUEA** | **INCOMPLETO** o **MODELO NO APLICABLE** |
| V-F1k | `perimetro_roic` sin declarar o distinto del de las palancas S2C | **BLOQUEA** el perímetro. Comparación numérica del bloque 10 del libro (Convenciones V6.3 §3): **AVISO** si el salto supera `Diagnóstico V6!C179`, el umbral vigente del libro, que esta especificación no cambia; **INFORMA** si no. La igualdad exacta con (1+g∞), **INFORMA** | **MODELO NO APLICABLE** para una conclusión si falta el perímetro. Se muestran la rentabilidad marginal, el ROIC, los dos saltos y la diferencia de inversión del año 11 |
| V-F1l | Un ajuste de normalización sin fuente, regla fiscal o ubicación de su caja; o la deducción del diagnóstico de partidas puntuales como si fuera un ajuste | **BLOQUEA** | **INCOMPLETO**. Sin regla aprobada, el diagnóstico se muestra como tal |

## E6. Presentación en el diagnóstico

- Puente FCF base → flujo sin crecimiento, en cinco líneas (informe §4.3): nivel del EBIT, cambio de tipo, escala de f, reinversión histórica y resultado.
- Tabla «Dónde queda el coste de arrendamiento» (informe §5.2).
- La salida debe decir que el perímetro es una **decisión** y que el reparto entre reposición y crecimiento **no está publicado** cuando así sea. La conclusión de nivel se mantiene como `pendiente_de_datos` mientras M1 esté abierto, salvo que la persona responsable registre otra política.
- Tabla de correspondencia de costes (propuesta, §2), con el sitio de cada coste en la ventana, los años 1–10 y el terminal, y los controles que saltan con su severidad.
- Estado de la normalización: el diagnóstico de partidas puntuales, rotulado como diagnóstico, y los ajustes aprobados, cada uno con su fuente, su regla fiscal y su efecto en f, en el τ de 5 años, en m0 y en el terminal.
- Los avisos nunca se presentan como prueba de coherencia.

## E7. Redondeo de las entradas registradas

C46, C47 y C50 se registran con tres decimales, no con su media exacta. El efecto es −7,3·10⁻⁸ en f y ≤ 0,0006 mm en los flujos.

Hay dos opciones; hay que elegir y declarar una:
- (i) mantener «redondeo: 3» y llamarlo redondeo, no «valor exacto», en el registro;
- (ii) guardar la media exacta.

Ambas son admisibles. Lo que no se admite es presentar un redondeo como exacto.

## E8. Fuera de F1 (observaciones para una revisión económica separada; no implementar con F1)

1. Ventana del tipo: f se calibra con τ por año y la proyección usa τ de 5 años. Efecto en Elis: −8,0 en el flujo de partida. Además, mueve la cifra de N1 entre −11,605 (cinco años) y −9,141 (ventana) (revisión dirigida, V4).
2. Intereses proporcionales a las ventas sin endeudamiento nuevo. Efecto en Elis en el año 1: endeudamiento omitido de 60,4 a 166,1 si la deuda neta se mantuviera en el 63 % de las ventas.
3. Motor B, C63: intereses sin arrendamientos ÷ deuda con arrendamientos.
4. Partidas puntuales dentro de la ventana de f: earnout de 2023 y plusvalía de 2025, con +27,9 en el flujo sin crecimiento de Elis, común a todos los perímetros (informe §4.2). Ese +27,9 es un diagnóstico, no el efecto de una regla. La propuesta, decisión 5a, trae ajustes concretos con regla fiscal: N1, con −11,605 en el flujo sin crecimiento con la convención registrada del τ (−9,141 con la de la ventana; E8.1), y N2, pendiente. Si se aprueba N1, se aplica con F1 (E3, T16). **Los valores de referencia de T1–T3b no están normalizados.**
5. Tendencia de los arrendamientos: pagos y amortización ROU crecieron más deprisa que las ventas (informe §5.5). Una razón constante no lo proyecta. Propuesta, decisión 1b: la media es una referencia de ensayo. Sensibilidad con el peso de 2025, por partes:
   - los pagos, −16,778 (A0, A1 y A2);
   - la amortización ROU que devuelve f, +10,118 (A1 y A2);
   - en total, −6,660 en A1 y A2.
6. Inversión del plan climático (propuesta, 5b; E2, `tratamiento_transicion`; V-F1i): se clasifica por su finalidad documentada y su caja se cobra una sola vez. Importe, horizonte y finalidad: pendientes (M1).

## E9. Criterios de prueba

Tolerancia 10⁻⁹ salvo indicación. Los valores de referencia están en `resultados/contraste_f1.json → referencia_especificacion` y proceden de cifras verificadas contra los PDF.

**Límites de los valores de referencia.** Son valores de prueba de una implementación, no estimaciones económicas:
- se calculan con los datos, las palancas y la convención de redondeo actuales (E7). Si cambia cualquiera de ellos, hay que recalcularlos con `contraste_f1.py`;
- incluyen las partidas puntuales de la ventana sin normalizar, +27,9 en el flujo sin crecimiento (E8.4);
- los flujos de A1 y A2 usan las palancas S2C actuales, que no están ancladas en el perímetro de cada alternativa (V-F1g);
- los de `A3_estimado` usan estimaciones sintéticas de D_X, que no son datos de Elis;
- el C53 de referencia depende de las entradas del horizonte 2021–2025: ventas de 2020 y 2025, capex, D&A total, ROU y PPA, circulante, adquisiciones e impuesto de cada año. Desde C12 todas tienen una identidad entre páginas. Las 97 entradas que mueven la referencia intervienen en estas identidades entre páginas: R5, R8, R16, R17, R22, R34 y R39–R42 en 2021–22, y R5, R8–R13, R16–R18, R20–R24, R31 y R37 en 2023–25 (véase `cobertura_entradas`; la lista sale de `sondas_8.py`, sección 3, del revisor n.º 8, que lo comprueba desplazando cada entrada. Precisión de C16, revisión n.º 7, S6 e: la lista citaba también R25 y R35 de 2021–22, que son de la misma página, y R23 de 2021–22, en la que no interviene ninguna de las 97. Precisión de C18, revisión n.º 8, T7 c: citaba además R36 de 2021–22, en la que tampoco interviene ninguna, y para 2023–25 solo nombraba R24 y R42, y en R42 de esos años no interviene ninguna). La clase es por pertenencia: lo que una identidad entre páginas acredita es el número salvo un error dentro del intervalo que no detecta, que se da para cada entrada (`errores_sin_deteccion_entre_paginas`; revisión n.º 6, R6). Para las 97, el mayor error que ninguna identidad entre páginas detecta va de 0,1 a 0,5; un error igual a ese umbral no se detecta. Hasta C11 esta frase decía «desde C9», pero cinco de ellas solo tenían identidad de su página (revisión n.º 5, Q6). La prueba de mutación lo comprueba para todas las clases (`resultados/cobertura_por_mutacion.txt`). Límite declarado: la cifra publicada de las adquisiciones de 2021 antes de la reexpresión (86,9) y la reexpresada (86,8) difieren en 0,1, dentro de la cota de R39, así que ninguna identidad las distingue. Antes de C7, la amortización ROU y la PPA de 2021–22 solo estaban comprobadas por lectura (revisión n.º 3, N2);
- no son valores por acción ni sirven para elegir un perímetro.

| Id | Prueba | Resultado esperado |
|---|---|---|
| T1 | Elis, perímetro `A0_total` (comparación, con V-F1a desactivada solo en la prueba) | f = 0,041681455273796; flujo sin crecimiento = 248,496395342656; flujos MALO/NORMAL/BUENO de los años 1–11 = los del libro actual (`A0_flujos_libro`); C53 = 9,039509536785 |
| T2 | Elis, `A1_sin_ROU` | f = 0,012624225323285; flujo sin crecimiento = 387,878115969269; C53 = 2,445331695332. Flujos MALO/NORMAL/BUENO con las palancas actuales: los años 1–10 y el año 11 terminal = `A1_A2_flujos_detalle.A1` (año 11: 294,942490201187 / 413,845194930899 / 488,862107627977). Detecta una implementación que cambie f en un término y no en otro (revisión, O13). Control negativo: si el terminal conserva la f de A0, el año 11 se desvía en V₁₀·(1+g)·(f_A0 − f_A1): 166,6 / 205,4 / 223,9 (`desvio_anio_11_implementacion_parcial`) |
| T3 | Elis, `A2_propio` | f = −0,006118601744165; flujo sin crecimiento = 477,783708846410; C53 = 1,612524303305. Años 1–10 y año 11 terminal = `A1_A2_flujos_detalle.A2` (año 11: 402,413237593105 / 546,310847791079 / 633,271006526708). Mismo control negativo del terminal: desvíos de 274,1 / 337,8 / 368,3 |
| T3b | `A3_estimado` con estimaciones **sintéticas** de D_X, que no son datos de Elis (`A3_estimado_sintetico`) | (a) D_X = capex propio en cada año: reproduce la cota B, f = 0,022646228408102 y flujo sin crecimiento = 339,804571572014. (b) D_X = D&A propia: reproduce A2. (c) D_X = (capex propio + D&A propia)/2: f = 0,008263813331969 y flujo sin crecimiento = 408,794140209212, el punto medio exacto de A2 y B, porque f es lineal en la D_X media. (d) Sin fuente, método, rango o responsable de la estimación, dispara V-F1d. No se usa la proporción de dos tercios del lino plano: es parcial y no es una proporción del capex total (informe §6.1). (e) Para cada caso, el C53 con la misma D_X (2,651525243106 / 1,612524303305 / 2,005440531963) y los flujos de los años 1–10 y del año 11 con las palancas actuales (`A3_estimado_sintetico.*.flujos_palancas_actuales`). Así se detecta una implementación que aplique la D_X a f pero no al ancla ni al terminal (revisión n.º 3, N5) |
| T4 | Identidad de calibración | Para cualquier perímetro, f·ventas medias = NOPAT medio − reinversión media − FCF base. En A0, la suma de los componentes del informe §4.2 = f·ventas con medias exactas (190,065713333…); con las entradas registradas de C46/C47/C50, C79 = 190,066046666667. La diferencia, 0,000333, es el redondeo de E7 |
| T5 | Caso sintético solo con arrendamientos (τ = 0, sin crecimiento: EBITDA 100; capex propio = D&A propia = 20; ROU 10; pagos 12 = 10 + 2) | FCF verdadero 68; A1 y A2 dan 68; A0 da 58 (prueba negativa que documenta el defecto) |
| T6 | Caso sintético con PPA 5 sin reposición | A2 = 68; A1 = 63; A0 = 53 |
| T7 | Sin NIIF 16 ni PPA (ROU = PPA = 0, C49 = 0) | Los cuatro perímetros dan el mismo resultado que la V6.3. Los casos de referencia del motor A de `v6/pruebas/resultados_v63.json` no cambian |
| T8 | Reglas V-F1a…V-F1l, con su severidad (E5) | Cada una dispara su efecto con un caso positivo y no se dispara con su caso negativo. Una regla BLOQUEA impide que el resultado se use para una conclusión, y uno de AVISO o INFORMA no lo impide. V-F1a bloquea con cualquier importe mientras no haya un umbral decidido. V-F1c no se dispara con R = 29 (20 propia + 9 de compras de cartera) y capex propio 20. Sí se dispara con R_propia 25 frente a capex propio 20, y con R_compras 9 frente a compras 5 (`guardas_V_F1c`). V-F1k avisa solo por encima de C179 |
| T9 | Signos | D&A ROU y PPA publicados «(149.5)»/«(85.7)» se aceptan con `valor_fuente` negativo, `signo` −1 y `tratamiento`. La magnitud positiva sin esa declaración se rechaza (coherente con R415-SIGNO) |
| T10 | Invariantes de Elis | C46–C52, C48 = 108, C70 = 307,933, acciones, OCEANE y decisiones E1/D3/E2/E6 sin cambios. Solo cambian f (C58), C53, los flujos del motor y lo que dependa de ellos |
| T11 | Motor B (Viscofan, Vidrala) | Sin cambios en resultados de valoración (f = 0). Si cambia C53, solo cambian semáforos de diagnóstico, y se documenta |
| T12 | Reproducción independiente (revisión, O3; contraste externo; revisión n.º 3, N1–N3 y N10) | Sobre el material regenerado y por separado:<br>(a) `verificar_cifras.py`: 0 FALLO en las 752 filas y en cada una de las seis dimensiones (literal, ejercicio, columna, unidad, perímetro, edición). Las PENDIENTE deben ser solo las listadas en su salida, con su motivo: hoy 14, de URD 2022 p.302, sin unidad ni cabecera de columnas localizables, y una sola se usa, como contraparte. OK significa «sin incoherencia detectada por las reglas», no «acreditada». `test_verificar_cifras.py` 136/136: 23 positivos reales, 36 PENDIENTE esperados y 77 contraejemplos detectados en su dimensión, incluidos los de las revisiones n.º 1, n.º 3 y su adenda, n.º 4 a 8 y la columna de un país (C9); y 9/9 comprobaciones directas de funciones del verificador (revisión n.º 8). `sondas_metadatos.py`: 0 etiquetas cambiadas sin detectar. Mide la detección de etiquetas cambiadas, no la de cifras de otra unidad o de otro perímetro con una etiqueta verosímil;<br>(b) `contraste_f1.py`: se niega a calcular con una verificación de otro CSV. 0 fallos en cada clase y ninguna entrada usada con dimensión PENDIENTE. Los 126 residuos, dentro de su cota de redondeo calculada por cifra; la única excepción es la diferencia de concepto fijada de 2025 (+0,4 ± 0,15), con su límite de detección declarado. Las entradas usadas sin segunda línea deben estar listadas (`cobertura_entradas.sin_comprobacion`): hoy 31, ninguna con efecto en estos valores de referencia. Deben listarse también las páginas sin ninguna identidad entre páginas (`cobertura_entradas.paginas_sin_identidad_entre_paginas`, hoy 8 con 24 entradas): en ellas la unidad y el perímetro no están acreditados por una segunda línea. Ninguna entrada que mueva estos valores de referencia puede quedar sin identidad entre páginas (`cobertura_por_mutacion.py`). `test_contraste_residuos.py` 24/24. `cobertura_por_mutacion.py`: ninguna entrada declarada con una comprobación que la mutación no haga fallar, ni ninguna usada sin declarar. Las identidades algebraicas documentan, no prueban;<br>(c) la réplica del motor coincide con los flujos del libro regenerado.<br>Ni el código de salida 0 ni el número de comprobaciones bastan por sí solos |
| T13 | Exceso de caja distinto de cero (revisión, O15) | En una copia del libro recalculada con Análisis!C76 = 250 y = −80 (`prueba_caja_no_nula.py`): Motor!M6:M8 = C76 y (Motor!BL − Motor!M)·r = 248,496395342656 en los tres escenarios. Control negativo: la identidad anterior, BL·r − C76, se desvía en C76·(r − 1), que es −227,5 con 250 y +72,8 con −80 |
| T14 | Verificación de entradas del frente técnico | Debe rechazar los mismos contraejemplos que `test_verificar_cifras.py`, en la dimensión correspondiente:<br>· página inexistente o equivocada; fuente ausente, sin huella o con otra huella; redondeo; signo; posición distinta con el mismo literal;<br>· columna, bloque o saldo de otro ejercicio, también en una tabla con una tercera columna (F1);<br>· modo de control no admitido para el concepto (A1, A2, A4, H1);<br>· columna de otro concepto (D1, D2, activo frente a pasivo);<br>· recuentos e importes por acción como millones de euros (B1, B2, U1, U2);<br>· segmento, sublínea de un segmento, país o fila «Other» como grupo (C1, P1, P2a);<br>· edición no vigente;<br>· columna de una matriz con una celda vacía (N9);<br>· columna de un país en una tabla con columnas por país, y columna de una sociedad que no se asigna al ejercicio (C9);<br>· **criterio de formato**: un entero de seis cifras o más declarado en millones de euros queda PENDIENTE aunque su rótulo no sea de la lista (revisión n.º 4, P1: efectos de dilución en acciones);<br>· **criterio de título**: una fila bajo un título de bloque que nombra un país o un segmento queda PENDIENTE como del grupo. El título se busca hasta el principio de la página y al final de la anterior (revisiones n.º 4, P2, y n.º 5, Q4: bloques de pensiones de Francia, Irlanda y Reino Unido, en inglés y en francés);<br>· columna «published», «reported» o «publié» de una tabla de reexpresión declarada vigente: FALLO en edición; la «restated», OK (revisión n.º 5, Q1);<br>· columna de apertura («01/01/AAAA») y dos fechas del mismo año (revisión n.º 5, Q2). **Límite** (revisión n.º 6, R1): con columnas distintas para cada aparición del año, la cuenta de columnas puede igualar a la de números por accidente. Por eso la asignación por orden exige que cada número esté alineado con su columna (URD 2022 p.302: F13 y F14, PENDIENTE);<br>· **grupos de columnas**: si la cabecera repite los mismos ejercicios en cada grupo (una marca, una firma auditora), perímetro PENDIENTE: el verificador no distingue la columna de una firma auditora, cuyos honorarios paga el grupo, de la de una marca (revisión n.º 6, R1: F9; también los honorarios por firma, G2 y G4. Precisión de C18, revisión n.º 8, T8 a: esta línea decía que «la columna del grupo no es la del grupo consolidado», un argumento de concepto que se retiró en C16);<br>· **filas de una jurisdicción, una región o el desglose de un país** («› of which Ireland», «European Union (excluding France)», «Hors Union européenne»), con el rótulo unido aunque ocupe varias líneas: FALLO como del grupo; el TOTAL de esa tabla, OK (revisión n.º 6, R1: F1, F4 y F7);<br>· **encabezado numerado** de nota o de apartado («NOTE 13 …», «5.4 …»): cuenta como título y corta la búsqueda (revisión n.º 6, R2: G9);<br>· **cifra bajo una cabecera ajena**: FALLO solo si la columna de otro ejercicio está alineada con ella (5,5 caracteres o menos); si no, PENDIENTE (revisión n.º 6, R3: G6, el valor en libros bajo «Valeur comptable»);<br>· **título corto de la tabla** (de una sola celda, encima de su cabecera) que nombra un país, y cabecera con tres países o más sin ninguna columna reconocida: perímetro PENDIENTE (revisión n.º 6, R4: H1 y H2);<br>· filas de UGE con el prefijo «CGU» o «UGT» en la tabla del fondo de comercio (revisión n.º 6, R5: I12 e I14);<br>· **título numerado de la tabla y su continuación** («6.1.5 Consolidated statement of changes in equity / as at December 31, 2022»): no son cabecera de columnas (revisión n.º 7, S1);<br>· **fila de saldo con la fecha en el rótulo** (revisiones n.º 7, S1, y n.º 8, T1–T3): el rótulo es la primera celda de una línea con más celdas y solo dice la fórmula del saldo y la fecha, con «restated», «retraité», «published» o una llamada; puede estar partido en las líneas de encima, también tras el día o en tres líneas («SOLDE AU 31 / DÉCEMBRE 2024»; «BALANCE AS AT / DECEMBER 31, 2021 / (RESTATED)»), y se unen las justas para que lleve la fórmula y la fecha, sin absorber la cabecera de columna ni la línea de unidades de encima («Cash flow hedges» / «BALANCE AS AT JANUARY 1, 2021»). Los recuentos con fecha («Number of shares as at…», «Rights vested as at…») no son saldos y no toman el ejercicio de la fecha. Para los tokens a la derecha del rótulo, el ejercicio es el de esa fecha: OK si coincide con el declarado y FALLO si no (A8, A9, T3a declarado 2023). Si la fila tiene varias columnas de datos, la columna es un concepto que el modo «dos_columnas» no declara: «columna» PENDIENTE (A1, A10, T1a, T3a, T3c: ejercicio OK y fila PENDIENTE; con el identificador de saldo de los derechos de uso, la columna «Vehicles» es FALLO y la «Total», OK: T1b, T1c). Con una sola columna de datos, OK (deterioro de clientes, URD 2022 p.284). No toman el ejercicio de la fecha los tokens del propio rótulo (el día, el año, la pestaña), las líneas de prosa ni los títulos con fecha (T2a, T2b, T2c, T2e), ni una fila bajo la línea que continúa el rótulo de la fila anterior (T4b). Un año suelto dentro del rótulo de texto de la fila, o el día de la fecha de ese rótulo, no es una cifra en ningún modo: ejercicio PENDIENTE, aunque quede alineado con la columna de un ejercicio (el «2024» de «AU 31 DÉCEMBRE 2024», DEU 2024 p.295, declarado 2023). **Límites:** la unión depende de por dónde parta `pdftotext` el rótulo; una fila cuyo rótulo sea solo «Balance» o «Solde», sin fecha propia, bajo una línea de fecha que continúa la fila anterior y no empieza en minúscula, tomaría esa fecha;<br>· **línea de cifras sin rótulo**: toma el de las líneas de rótulo contiguas, de una sola celda, sin cifras, de 45 caracteres o menos y en el margen izquierdo; un segmento así no pasa como grupo (revisión n.º 7, S2: B1 y B3). No toma una línea de prosa ni la leyenda de un organigrama, y no se aplica a una línea que empieza por la pestaña del capítulo ni a un rótulo con viñeta («− Matthieu Lecharny») (revisión n.º 8, T5: T6a y T6b);<br>· **pestaña del capítulo en el margen** al principio de la línea: no es el rótulo (revisión n.º 7, S3: C1);<br>· **tabla con una columna por país sin declaración de unidades ni de ejercicios**: perímetro PENDIENTE, también en las filas cuyo rótulo empieza por una línea en mayúsculas; la primera línea de un rótulo partido no es la cabecera de ejercicios ni corta la búsqueda de la cabecera por países (revisión n.º 7, S4: D1 y D5; revisión n.º 8, T4: T5a y T5b). La excepción de la columna bajo una celda «Total» o «Group» no tiene caso real en las cinco publicaciones: se prueba con dos líneas sintéticas;<br>· **encabezado numerado en prosa** (con comillas, con puntuación final o con «Note N to the…»): no es título; en mayúsculas sí lo es, con comillas o con una coma final si la línea de debajo continúa el título (revisiones n.º 7, S5, y n.º 8, T6). **Límites:** un título en minúsculas partido tras una coma no cuenta como título, y una entrada de sumario sí;<br>· llamada con letra («(a)») en la cabecera: no deja PENDIENTE la cifra legítima ni rebaja a PENDIENTE la de otro ejercicio (revisión n.º 5, Q3);<br>· rótulos de segmento con «and», «et» o «CGU», o partidos en dos líneas (revisión n.º 5, Q5).<br>Estos criterios y las listas de rótulos detectan señales conocidas; no acreditan la unidad ni el perímetro (E9, T12).<br>Debe aceptar sus veintitrés positivos reales, entre ellos F2, F3, P2b, X2, el total de la nota de combinaciones de negocio, el total por países de la nota de pensiones, la columna «restated», el total del grupo bajo prosa que nombra un país, el impuesto total del grupo de la tabla por jurisdicción, el total de los derechos de uso con el identificador de saldo y el saldo de apertura de una tabla de una sola columna con la fecha en el rótulo. Los saldos del estado de cambios en el patrimonio declarados con su ejercicio y un identificador genérico deben quedar con el ejercicio OK y la columna PENDIENTE (precisión de C18, revisión n.º 8, T1 y T7 d: hasta C16 esta frase los contaba entre los positivos, y el verificador no reconocía la mitad de los cierres). Responde a los huecos de la revisión externa del hito 4.15 y de la revisión n.º 3 |
| T15 | Correspondencia de caja (revisión de la propuesta, P1–P4; revisión dirigida, V2 y V9) | `controles_sinteticos_f1.py`: 32 casos con importes ficticios, cada uno con su resultado esperado en los años 1–10 y en el año 11, también a crecimiento cero. Son 14 coherentes y 18 incoherencias ilustradas; 23 tienen crecimiento y 8 calculan el ancla de S2C con la fórmula de E4 desde una ventana con crecimiento:<br>· transición (P1a–e a crecimiento cero; V2a–e con crecimiento: término explícito dentro y fuera del ancla, en R proporcional y fija en euros, transición de crecimiento);<br>· compras de reposición (P2a–d; V2f–h: término explícito dentro y fuera del ancla, y en R);<br>· gasto comercial (P2f); «PPA constante» (P2g–i);<br>· terminal con g/ROIC (P4a–d), la fórmula del libro (P4e) y la senda de `motor_a` (P4f).<br>Además: tres guardas V-F1c (una no salta y dos sí) y un caso fiscal sintético de N1 con caja conocida y tres convenciones del tipo. Reproduce los 9 casos de la revisión externa. El motor sintético coincide exactamente con `motor_a` sin términos explícitos, con crecimiento distinto en los años 1–5 y 6–10, margen de m0 a m_obj e impuestos (4 juegos), pero no se compara con él cuando hay términos explícitos, que `motor_a` no tiene. Una implementación debe dar, con las mismas entradas, el mismo resultado que el motor sintético en los casos coherentes y detectar con sus controles cada incoherencia ilustrada |
| T16 | Normalización N1, **solo si se aprueba** (propuesta, 5a) | Elis, perímetro A0, ajustes de earnout de la nota 4.6 (−48,9 / +8,7 / −0,2) sin efecto fiscal, solo en la ventana y **con la convención registrada del τ de proyección de cinco años**: τ 2023/2024/2025 = 0,2619 / 0,2806 / 0,2559; τ de 5 años = 0,28234; m0 = 0,131379; f = 0,044900433; flujo sin crecimiento = 236,891 (−11,605 frente a T1); variación del año 11 NORMAL −18,609. La variación es la misma en A1 y A2 (`copia_investigacion_f1.json`; tolerancia 10⁻⁹ en f y 10⁻³ en los flujos). **Los valores dependen de la convención y del alcance aprobados** (V4):<br>· con el τ de la ventana: −9,141 y −15,848;<br>· si N1 alcanza también a 2021–22: −11,190 y −18,142 [LECTURA].<br>Se recalculan con `copia_investigacion_f1.py` para el texto aprobado. Control negativo: deducir el diagnóstico 27,936 no reproduce estos valores y dispara V-F1l |

## E10. Lo que esta especificación no decide

- El perímetro ni la política de la PPA.
- La clasificación de las compras de sociedades, el tratamiento de la inversión de transición, la normalización ni un umbral de materialidad.
- El valor de la reinversión necesaria.
- La validez del motor A para Elis.
- Ningún precio ni recomendación.

Tras implementarla hay que repetir la réplica, regenerar los expedientes del motor A y auditar el material final con un auditor de contexto separado.
