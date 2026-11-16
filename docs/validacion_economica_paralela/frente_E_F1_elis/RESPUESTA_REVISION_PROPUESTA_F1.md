# Respuesta a la revisión de la propuesta de decisiones F1 · P1–P4

Fecha: 16-nov-2026. Autor: frente E (sesión «Conciliación económica Elis/F1»).

- **Revisión respondida:** `REVISION_PROPUESTA_F1.md`, rama `auditoria/revision-propuesta-f1`, commit `1a071881c65a191056ca3c6b41a20a965825cf12`, leída sin fusionarla ni cambiar de rama.
- **Material que revisó:** la propuesta del commit `b83803cd1c42c52c6ced6a538f5ae03ef706a644` (SHA-256 `f2d8c815…f795`).
- **Esta respuesta:** está en el commit congelado `13f864f910bf0bb3e27007b23c13a8e957f1bfb7`.
- **Revisada** por la revisión dirigida a P1–P4 (commit `8fcc7fd`). Resultado: §7. **Sus correcciones V1–V11 se aplican después**, en la revisión 3 de la propuesta y en la especificación: [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md). Este documento conserva el texto revisado, con notas de corrección en los puntos afectados.

**Qué no hace.**
- No adopta ninguna decisión económica.
- No modifica la plantilla, los libros, los datos ni las fórmulas o cifras de valoración.
- No libera la valoración de Elis, que sigue en `pendiente_de_datos`.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y las decisiones E1, D3, E2 y E6.
- No se ha enviado ninguna comunicación a Relación con Inversores ni a terceros.

## 0. Resumen

Acepto las cuatro correcciones. No discrepo en el fondo de ninguna. Hay dos precisiones numéricas, en §5.4, y tres hallazgos del cálculo conjunto que la revisión pedía, en §4.

| | Qué faltaba | Qué cambia | Qué sigue pendiente |
|---|---|---|---|
| **P1** | La inversión climática quedaba como categoría «fuera de R y del crecimiento», sin línea de caja | (5b) clasifica por la finalidad documentada y cobra la caja una sola vez en la ventana, la proyección y el terminal, con horizonte. Sin importe ni horizonte, queda pendiente. Nunca cero por defecto ni perpetua por su nombre. Nuevo control V-F1i | Importe, horizonte y finalidad del plan climático (parte de M1) |
| **P2** | No se reconciliaban tres frases: «reponer clientes va en R», «su coste ya está en EBIT y capex» y «todas las compras son crecimiento» | Tabla de correspondencia de cada coste en la ventana, los años 1–10 y el terminal (propuesta, §2). Composición de R: R_propia + R_compras. La guarda compara cada parte con su propia caja. (4b) pasa a ser una hipótesis declarada, con su fundamento, su consecuencia a crecimiento cero y su sensibilidad. «PPA constante» quiere decir constante como proporción de las ventas | M2 (bajas de clientes) y el nuevo M6 (finalidad de las compras de sociedades) |
| **P3** | Se trataba el 27,936 como el efecto de una regla y se mezclaban 13,7 y ≈ 18,6 | Tabla de ajustes concretos, con fuente, importe original y normalizado, motivo, fiscalidad, caja y dependencias. Cálculo conjunto en una copia de investigación, sobre f, el tipo de cada año, el τ de 5 años, m0, los flujos y el terminal. El 27,936 se conserva como diagnóstico | N2 (bajas de 2025 con indemnizaciones de seguros): fiscalidad y ubicación de la caja. Actualización del earnout mexicano en el tipo |
| **P4** | No estaba fijado qué bloquea y qué solo avisa; aparecía un umbral del 0,5 %; faltaba el terminal; la media de los arrendamientos se presentaba como peso futuro | Columna de severidad en E5, la misma que en el texto de aprobación. V-F1a sin umbral adoptado. V-F1g pasa a bloquear. Nuevos V-F1i–l. El terminal entra en (4a): ROIC con el mismo perímetro que S2C, y compatibilidad calculada. (1b): la media es una referencia de ensayo, con la sensibilidad de 16,8 | El perímetro de las palancas S2C y ROIC de Elis, que no está declarado |

**Documentos revisados (sin implementar nada):**
- [PROPUESTA_DECISIONES_F1.md](PROPUESTA_DECISIONES_F1.md), con la tabla única de las decisiones (1a)–(5b);
- [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md): E2–E6, E8 y E9;
- precisiones en [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md): §4.2, §6.4 y §9.

## 1. Evidencia ejecutada

Desde `scripts/`, sobre el árbol materializado de la base 4.14 y el libro de Elis `d2593777…92385`, leído en solo lectura.

```bash
python3 -I controles_sinteticos_f1.py --salida ../resultados/controles_sinteticos_f1.json
```

```bash
python3 -I copia_investigacion_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro "$LIBRO" --contraste ../resultados/contraste_f1.json --salida ../resultados/copia_investigacion_f1.json --informe ../resultados/copia_investigacion_f1.md
```

```bash
python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro "$LIBRO" --caja-no-nula ../resultados/caja_no_nula.json --salida ../resultados/contraste_f1.json --informe ../resultados/contraste_f1.md
```

| Script | Resultado | Salida |
|---|---|---|
| `controles_sinteticos_f1.py` (nuevo) | Código 0. 22 casos: 8 coherentes y 14 incoherencias ilustradas, cada uno con el resultado esperado. Los 9 casos del revisor se reproducen exactamente. El motor sintético coincide con `motor_a` en tres casos de prueba. **Corrección V10:** esos tres casos tenían crecimiento y margen constantes y no recorrían la senda de `motor_a`. Desde las correcciones, el script tiene 32 casos y coincide con `motor_a` también con crecimiento y margen variables e impuestos | `resultados/controles_sinteticos_f1.{json,log}` |
| `copia_investigacion_f1.py` (nuevo) | Código 0. 43 controles, ninguno fallido. Sin ajustes, reproduce f (Historia!C58), el τ de 5 años (C52), el flujo sin crecimiento 248,496395342656, los 33 flujos del libro, el FCF base registrado (Historia!C70), C48 = 108, el diagnóstico 13,675 / −4,032 / 18,293 / 27,936 y la sensibilidad de arrendamientos de la revisión. La variación de cada escenario es idéntica en A0, A1 y A2 | `resultados/copia_investigacion_f1.{json,md}` |
| `contraste_f1.py` (sin cambios) | Se ha vuelto a ejecutar: 292 comprobaciones, 0 fallidas; salidas idénticas byte a byte | `resultados/contraste_f1.{json,md}` |

Los controles sintéticos usan importes ficticios: son ejemplos de política, no datos de Elis. La copia de investigación usa solo cifras verificadas y las mismas funciones del contraste. No cambia el CSV, la verificación, el libro ni ninguna entrada registrada.

## 2. F1-P1 · Inversión climática

**Acepto.** Una categoría separada no puede dejar su caja fuera del modelo. El nombre no decide si la inversión es mantenimiento, crecimiento o una obligación temporal.

**Corrección.** La decisión (5b) pasa a decir:
- La inversión de transición se clasifica por su **finalidad documentada**:
  - **sostenimiento** (necesaria para mantener las ventas a volumen constante): dentro de R, si es permanente, o como término explícito con su importe y su horizonte, si es temporal;
  - **crecimiento**, si amplía la capacidad de ventas: inversión de crecimiento;
  - **obligación temporal** (por ejemplo, adaptar plantas a una norma): término explícito con importe y horizonte.
- En la ventana, su caja ya está dentro del capex propio y del FCF base. En los años 1–10 y en el terminal se cobra una sola vez, en el lugar que corresponda a su clasificación.
- Sin importe u horizonte suficiente, la conclusión afectada queda pendiente. No se supone cero ni se elimina por su categoría.
- Nuevo control V-F1i (bloquea):
  - transición declarada sin finalidad, importe u horizonte;
  - transición cobrada dos veces, o ninguna.

Detalle en la propuesta, §5, y en la especificación, E2 y E5.

**Evidencia.** Casos sintéticos P1a–P1e de `controles_sinteticos_f1.py`, a crecimiento cero. Ventana: capex 27, del que 7 es transición; FCF base 61.

| Caso | Motor | Caja | Qué muestra |
|---|---|---|---|
| P1a · plan temporal (5 años) cargado en R | 61 en todos los años | 61 en los años 1–5; 68 en los años 6–10 y en el terminal | Cargarlo en R lo hace perpetuo y lo cobra de más después del plan |
| P1b · plan temporal con R = 20 y término explícito en los años 1–5 | = caja | = | Coherente, si el importe y el horizonte están documentados |
| P1c · inversión permanente con término limitado a 5 años | 68 en los años 6–10 y en el terminal | 61 | Un horizonte no documentado la omite |
| P1d · en R y además como término | 54 | 61 | La cobra dos veces |
| P1e · clasificada como crecimiento | 68 | 61 | A crecimiento cero desaparece, igual que si se excluyera |

**Elis.**
- En la ventana, el gasto del plan está dentro del capex propio [P: «capex contained despite new workwear contracts and expenditure under the Climate plan», URD25 p.122]. Por tanto, también está dentro del FCF base y de la cota superior de R.
- Los planes de las pruebas de deterioro suponen una inversión superior a la amortización histórica [P: URD25 p.369]. No se publica un importe separado ni un horizonte.
- Por eso no puede clasificarse. Como R ya está pendiente, esto no añade un bloqueo nuevo, pero la estimación de R tendrá que declarar el tratamiento de la transición (V-F1d).
- **Pendiente:** importe, horizonte y finalidad del plan, dentro de M1.

## 3. F1-P2 · Reposición de clientes, adquisiciones y «PPA constante»

**Acepto.** Las tres frases describen tres desembolsos distintos y una hipótesis.

**Reconciliación.**
- El coste de conservar y reponer clientes tiene hasta tres componentes de caja:
  - **(a) Gasto comercial corriente.** Está en el EBITDA, el EBIT y el FCF base. En la proyección queda en el margen. **No se añade a R.**
  - **(b) Inversión propia para los clientes que sustituyen a los perdidos.** Es el lino y el equipo de arranque: «initial outlay required to set up a new customer» [P: URD25 p.312]. Está en el capex propio y forma parte de **R_propia**, porque hace falta para mantener las ventas a volumen constante.
  - **(c) Compras de cartera que reponen ventas perdidas,** si las hay. Están fuera del FCF base. Van en **R_compras** o en un término explícito proporcional a las ventas, **nunca solo como crecimiento**: con ΔV = 0 desaparecerían.
- Qué cubre cada frase:
  - «Reponer clientes va en R» se refiere a (b) y, si existe, a (c).
  - «Su coste ya está en el EBIT y el capex» describe la ventana: (a) y (b) están pagados dentro del EBIT y del capex. Por eso la PPA, que no es caja, no es un coste de reposición adicional.
  - «Todas las compras son crecimiento» es la hipótesis (c) = 0. **Es una hipótesis, no un dato.** Se declara con su fundamento y su consecuencia en (4b).
- **Perímetro de R:** R = R_propia + R_compras, más la transición que se clasifique como sostenimiento.
- **Guarda V-F1c:** compara R_propia con el capex propio y R_compras con las compras, **no R total con el capex propio**. El caso sintético lo muestra: R = 29 (20 propia + 9 de compras de cartera), con capex propio 20.
  - La guarda anterior daría alarma de infrainversión, sin que la haya.
  - La propuesta no la da.
  - Salida: `guarda_R_frente_a_capex` de `controles_sinteticos_f1.json`.

**Fundamento de la hipótesis (4b) en Elis:**
- [P] El crecimiento orgánico fue positivo todos los años de 2021–2025: 7,4 %, 21,0 %, 11,8 %, 5,2 % y 3,8 %.
- [P] Tuvo efecto volumen publicado en 2024 y 2025, sin cifra. En 2023, unos 9 de los 11,8 puntos fueron de precio.
- [I] El crecimiento orgánico se mide sobre la cartera existente, neta de los clientes perdidos, también los de sociedades compradas en años anteriores. Que fuera positivo en volumen indica que, en la ventana, las bajas se repusieron sin compras, y que las compras añadieron ventas (crecimiento externo del 1,2 % al 3,1 % al año en 2022–2025).
  - **Corrección V1 (material):** la definición publicada solo excluye las adquisiciones «importantes», de más de 5,0 millones de ingresos en Francia y de 3,0 en los demás países (URD25 p.313; DEU24 p.259; URD23 p.267). Las compras pequeñas, con un flujo neto de 31,5 al año de media en 2023–25, están dentro del crecimiento orgánico. Lo publicado permite decir «sin compras importantes», no «las bajas se repusieron sin compras». La propuesta, revisión 3, (4b), ya no recomienda aprobar la hipótesis: la deja como opción B.
- Es una evidencia parcial de la ventana. Para el futuro, es una hipótesis.

**Consecuencia y sensibilidad de la hipótesis.**
- A crecimiento cero no se compra nada.
- Si una parte de las compras fuera de reposición, cada millón anual bajaría el flujo sostenible en un millón: en todos los años y en el terminal.
- Si la hipótesis no se aprueba, hace falta conocer la finalidad de las compras. Es el nuevo dato **M6**, y sin él el caso queda bloqueado (V-F1j).

**Evidencia sintética** (`controles_sinteticos_f1.py`):

| Caso | Resultado |
|---|---|
| P2a · compras de reposición del 9 % solo como crecimiento, con el ancla calculada con todas las compras | A crecimiento 0 faltan 9. Al 5 % histórico casi se compensa (diferencia máxima 0,73). Al 10 % se cobra de más (−21,0). La compensación no es correspondencia |
| P2b · en R (R = 29) y ancla sin ellas | Coherente al 0, al 5 y al 10 % y en el terminal |
| P2c · en R y además en el ancla | A crecimiento cero, coherente (59). Con crecimiento, las cobra dos veces (−14,7). **La prueba a crecimiento cero no basta** |
| P2d · como término explícito proporcional a las ventas | Coherente |
| P2e · compras solo de crecimiento | Coherente, también a crecimiento cero: es el caso que supone (4b) |
| P2f · gasto comercial en el EBIT y también en R | Cobrado dos veces en todos los años |

**«PPA constante».**
- **Significa constante como proporción de las ventas**, la misma que devuelve f. No constante en euros.
- En el motor, f es una proporción de las ventas por construcción, y el margen objetivo también lo es. La PPA, que no es caja, solo se anula en el flujo si el margen la lleva en la misma proporción que f devuelve.
- Casos sintéticos:
  - P2g · misma proporción: coherente con cualquier crecimiento;
  - P2h · PPA fija en euros en el margen frente a f proporcional: sobrestima el flujo en 0,05·V_t − 5, cada vez más;
  - P2i · PPA que se agota sin compras: sobrestima hasta 5. Es la razón por la que `EBIT_NIIF16_PPA_decreciente` con A2 no es admisible (E2).
- **En Elis** (`copia_investigacion_f1.md`):
  - f devuelve en A2 la proporción media de la ventana, el 1,8743 % de las ventas (89,906 sobre las de 2025);
  - m0 lleva la PPA real de 2025, el 1,7866 % (85,7);
  - la diferencia, 4,206 en la base 2025, es un efecto de escala de la definición y se declara.
- **Qué se sabe y qué se supone:**
  - [P] la PPA de 2025 es 85,7, con una cartera neta de 275,1 y vidas de 4–14 años;
  - [D] sin compras nuevas, se agotaría en unos 3,3 años al ritmo actual;
  - [H] la proporción constante es una convención del perímetro: no hay dato que diga cómo evolucionará la PPA en euros.

**Pendiente:** M2 (tasa de bajas y desembolso por cliente nuevo) y M6. Sin ellos, la parte de R que repone clientes no se puede cuantificar.

## 4. F1-P3 · Normalización

**Acepto.** El 27,936 es una descomposición del cálculo conservado, no el efecto de aprobar una regla. Tres hallazgos del cálculo conjunto lo confirman.

1. **El «≈ 18,6» no se puede sumar a nada.** Es solo la parte de f del ajuste del earnout de 2023 con tipo recalculado (−18,648). Omite que el mismo ajuste baja el tipo de 2023 y, con él, el τ de 5 años de la proyección (+4,334). El efecto conjunto de ese ajuste es −14,314. La cifra procedía de la revisión n.º 1, O9, y la propuesta la repitió sin cálculo.
2. **El diagnóstico no corresponde a ninguna regla concreta:**
   - toma las líneas del estado de flujos de los tres años, que incluyen otros elementos no monetarios y las pérdidas ordinarias por bajas fuera de la nota 4.6 (3,1 / 5,8 / 2,6 [D]: la línea del estado de flujos menos la de la nota);
   - quita de f la partida antes de impuestos, mientras que normalizar el EBIT la quita después de impuestos;
   - lleva la plusvalía de 2025 a m0, pero no la quita del NOPAT de 2025 que calibra f.
3. **La etiqueta «no recurrente» no basta.**
   - La nota 4.6 presenta como «inhabituales, anormales o poco frecuentes» partidas que se repiten todos los años: reestructuración, cambio de sistemas, rehabilitación ambiental y litigios. Sus elementos monetarios suman 16,9 / 22,2 / 28,2 y su caja está en el FCF base.
   - Aplicar la regla literal de la propuesta anterior a toda la nota da −20,057 en el flujo sin crecimiento y −32,803 en el terminal NORMAL. El coste se traslada del margen a f. Es un contraejemplo, no una propuesta.

**Ajustes concretos** (propuesta, §5.1; cifras de `copia_investigacion_f1.md`, perímetro A0; la variación es la misma en A1 y A2):

| Ajuste | Fuente | Original → normalizado | Motivo | Fiscalidad | Caja y dependencias | Efecto conjunto en el flujo sin crecimiento y en el terminal NORMAL |
|---|---|---|---|---|---|---|
| **N1** · ajustes de earnout de 2023–25 | Nota 4.6: −48,9 / +8,7 / −0,2 (DEU24 p.296; URD25 p.350). En 2023, revaluación del complemento de precio de México (DEU24 p.296) | EBIT y BAI del año → sin el ajuste | Revaluación del precio de una adquisición, no coste de explotación. No monetaria al reconocerse: el estado de flujos la añade de vuelta. Se trata simétricamente en los tres años | No deducible [P]: la línea fiscal de 2023, 15,8, es 25,83 % × (48,9 + 12,4 de actualización) [D]; en 2024, 0,8, y en 2025, 0,2 (URD25 p.392). **Corrección V10:** con su signo, (15,8) en 2023, 0,8 en 2024 y (0,2) en 2025; 2024 es de sentido contrario. Regla: gasto por impuesto sin cambios y tipo del año recalculado | El pago está fuera del FCF base [I]: la línea del pago no se ha identificado en las páginas examinadas. **Corrección V3:** está publicado [P]. La nota 2.4 separa «Earnouts and deferred consideration» dentro de «Acquisition of subsidiaries, net of cash acquired»: 34,4 / 93,9 / 23,3 (DEU24 p.288; URD25 p.342 y p.341). El de México se liquidó en 2024 y 2025 (URD25 p.352). Coherente con (4b), porque el coste de las compras se cobra como compras. m_obj debe declararse sin estos ajustes | **−11,605** y −18,609, con la regla publicada. Con el tipo fijo: −9,765 y −14,598 |
| **N2** · resultado por bajas de 2025, con indemnizaciones de seguros | Nota 4.6: +25,7 (URD25 p.350); «a high level of insurance benefits in 2025» (URD25 p.309). Que las dos cosas sean la misma partida es una inferencia [I] | EBIT 2025 y m0 → sin la plusvalía | Suceso extraordinario [I] | No publicada. Tres hipótesis: tipo fijo, tipo teórico del 25,83 % y no gravada | La caja cobrada no está identificada: los cobros por bajas de 2025 son 15,3, menos que la plusvalía de 23,1 del estado de flujos. Tampoco lo está la reposición de los activos dados de baja. Una normalización simétrica tendría que ajustar también el FCF base registrado (E6), y eso no se puede calcular | Parcial, sin la simetría de caja: −10,305 a −11,598 y +9,9 a +12,3. El terminal **sube**, porque solo baja f. **Pendiente** |
| No se proponen | El resto de la nota 4.6 y las pérdidas ordinarias por bajas | — | Recurrentes; su caja está en el FCF base | — | Normalizarlas las trasladaría a f (contraejemplo) | — |

**Conjunto N1 + N2:** de −22,060 a −23,353, frente al diagnóstico de −27,936. Solo es un cálculo parcial, porque N2 está pendiente.

**Recomendación revisada para (5a):**
- no deducir el 27,936;
- aprobar, si se quiere normalizar, solo la regla N1, con su fiscalidad publicada y su condición (4b);
- mantener N2 pendiente;
- no normalizar nada por su etiqueta.

La alternativa es no normalizar y declarar el diagnóstico. Los históricos y las entradas registradas no cambian: la normalización sería una fila de ajustes con fuente y regla (especificación, E1 y E3).

**Límite declarado de N1.**
- La actualización del complemento de precio de México está en el resultado financiero: 12,4 en 2023 y 5,6 en 2024 [P: DEU24 p.259]. No es deducible y también eleva el tipo de esos años.
- No se calcula, porque esas cifras no están en el CSV verificado y la de 2025 no se publica por separado (URD25 p.379 solo dice que bajó).
  - **Corrección V3:** la de 2025 sí se publica: 0,7 (URD25 p.313). Con 12,4 / 5,6 / 0,7, la línea fiscal cuadra los tres años al 25,83 %. Su efecto, si la regla fiscal la alcanzara, es −0,790 en el flujo sin crecimiento. Está calculado como [LECTURA] en `copia_investigacion_f1.md`.

## 5. F1-P4 · Coherencia completa

**5.1 Qué bloquea y qué avisa.**
- **Acepto.** El texto de aprobación y E5 usan ahora la misma columna de severidad:
  - **BLOQUEA:** el resultado del motor A no se usa para una conclusión; puede calcularse y mostrarse como diagnóstico, rotulado;
  - **AVISO:** se muestra, no bloquea y no acredita coherencia;
  - **INFORMA:** información.
- **V-F1a.** **No se adopta el umbral del 0,5 %.** Mientras no se decida un umbral, bloquea con cualquier importe. Fijar un umbral sería una decisión aparte, y no propongo ninguna cifra.
- **V-F1g** (ancla de S2C de otro perímetro o sin declarar) pasa de aviso a **BLOQUEA**. Con anclas tan distintas (9,04 en A0 frente a 1,61 en A2), un aviso no puede presentarse como coherencia.
- **V-F1c** es un aviso con justificación obligatoria; sin la justificación, bloquea.
- Controles nuevos:
  - V-F1i: transición;
  - V-F1j: clasificación de las compras;
  - V-F1k: perímetro del ROIC del terminal;
  - V-F1l: ajustes de normalización sin fuente, regla fiscal o caja.

**5.2 Terminal.**
- El terminal no usa S2C. Reinvierte g∞/ROIC del NOPAT, antes de f: V₁₀·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f].
- **Significado del ROIC** compatible con la propuesta: el rendimiento de la inversión nueva, medido sobre el NOPAT del mismo perímetro del margen y sobre el capital de crecimiento del mismo perímetro que el ancla de S2C. Por eso:
  - con adquisiciones, si (4b) lo está;
  - sin la ROU, porque el arrendamiento se paga dentro de f;
  - sin R, porque la reposición está en f.
- **Compatibilidad:** el terminal cobra la misma inversión de crecimiento que ΔV/S2C si ROIC = (1+g∞)·m_obj·(1−τ)·S2C. Casos sintéticos:
  - P4a: con ese ROIC, coherente;
  - P4b: un ROIC medido solo sobre el capital propio, mientras el crecimiento incluye compras, cobra la mitad de la inversión del terminal.
- **Palancas del libro de Elis:**

| Escenario | ROIC | ROIC que reproduce S2C | S2C implícita en el ROIC | Inversión del terminal con ROIC − con S2C |
|---|---|---|---|---|
| MALO | 7 % | 7,55 % | 0,93 frente a 1 | +4,45 |
| NORMAL | 10 % | 10,89 % | 1,10 frente a 1,2 | +10,28 |
| BUENO | 12 % | 14,77 % | 1,22 frente a 1,5 | +28,96 |

  - El ROIC de las palancas cobra en el terminal algo más de inversión de crecimiento que su propia S2C.
  - Que difieran no es un error en sí, porque las palancas pueden suponer otra intensidad de capital a perpetuidad. Pero debe declararse (V-F1k informa).
  - **El perímetro de las palancas no está declarado,** y su ancla depende de R. La compatibilidad del terminal de Elis queda **pendiente** con R.
  - No se estima ningún ROIC nuevo.

**5.3 Crecimiento cero en el terminal.**
- Con g∞ = 0, el terminal es V·[m_obj(1−τ) − f]. Un coste recurrente que solo se cobre como crecimiento desaparece también del terminal: casos P2a y P4c.
- Todos los casos sintéticos dan el terminal y los años 1–10, no solo el año de partida.
- Un coste cobrado de más tampoco desaparece en el terminal: casos P1a y P4d.

**5.4 Arrendamientos (1b).**
- **Acepto.** La media de la ventana, el 3,3589 % de las ventas, es una referencia de ensayo y la convención registrada. No es un peso futuro identificado.
- Sensibilidad con el peso de 2025 (3,7087 %): el flujo sin crecimiento sería **16,778** menor.
- **Precisión numérica:** el texto de la revisión dice «≈ 161,120» y «16,780», pero su propio JSON da 161,121763 y 16,778237, que reproduzco con las cifras verificadas. La propuesta redondea a 16,8.
- No se elige otro punto.

**5.5 Otra precisión.** Los efectos fiscales de las partidas normalizadas cambian el τ de 5 años y, con él, todos los años proyectados y el terminal. Por eso la propuesta da el efecto de cada ajuste también en el terminal, no solo en el flujo sin crecimiento.

## 6. Lo que sigue pendiente

| Carencia | Qué impide | Quién decide o aporta |
|---|---|---|
| M1: reparto de la inversión propia por bloque y año, con el plan climático (importe, horizonte y finalidad) | R, f, el flujo de partida y el ancla de S2C de Elis; la clasificación de la transición | Dato o estimación documentada (3b) |
| M2: tasa de bajas de clientes y desembolso por cliente nuevo | La parte de R que repone clientes | Dato (3b) |
| M6 (nuevo): finalidad de las compras de sociedades, reposición o ampliación | Sustituir la hipótesis (4b) por un dato | Dato (3b), o aprobar la hipótesis (4b) |
| N2: fiscalidad de la plusvalía de 2025, ubicación de la indemnización cobrada y reposición de los activos | La normalización de N2 y el efecto final conjunto | Dato; sin él, N2 sigue pendiente |
| Actualización del earnout mexicano en el tipo de 2023–25 | Completar la regla fiscal de N1 | Verificar las cifras (DEU24 p.259) y la de 2025 |
| Perímetro de las palancas S2C y ROIC de Elis | V-F1g y V-F1k | Fase C, con R conocido |
| Umbral de materialidad de V-F1a | Solo si se quiere uno; mientras tanto, bloquea con cualquier importe | Persona responsable |

**Preguntas preparadas, no enviadas** (su envío no está autorizado por este encargo):
1. Reparto del capex de 2023–25 entre mantenimiento y crecimiento, por tipo de activo, y la base y la fecha de los «dos tercios» del lino plano.
2. Importe, calendario y finalidad del capex del plan climático, y qué parte es necesaria para seguir operando.
3. Tasa de bajas de clientes y desembolso inicial por cliente nuevo.
4. Qué parte de las compras de sociedades de 2021–25 repuso cartera perdida.
5. Dónde se cobraron en 2025 las indemnizaciones de seguros, su tratamiento fiscal y el capex de reposición de los activos dados de baja.

Fuentes públicas que podrían contenerlas y no están en la base: presentaciones de mercado de capitales, transcripciones de las presentaciones de resultados y respuestas publicadas de Relación con Inversores. La pregunta de M1 ya está redactada en `Diagnóstico V6!B223`.

**Revisión.** Las justificaciones materiales cambian en P1–P4. Por eso el encargo prevé una revisión económica independiente, dirigida a P1–P4, sobre el commit congelado y en un contexto separado. Su resultado se registra en `revision/ESTADO.md`. Si encuentra una carencia de datos o de política, se documenta el bloqueo y se termina, sin más pasadas.

## 7. Resultado de la revisión dirigida a P1–P4

Revisión independiente, en una sesión nueva con contexto propio, sobre el commit congelado `13f864f`. Commit `8fcc7fd` de la rama `auditoria/economica-f1-frente-e-revision`; copia sin cambios en [revision/REVISION_PROPUESTA_P1_P4.md](revision/REVISION_PROPUESTA_P1_P4.md).

**Reproducción:**
- materializó la base 4.14 (6.798 de 6.798) y el manifiesto (356 de 356);
- los tres scripts dan salidas idénticas byte a byte;
- recalculó N1 sin importar código del autor: −11,605 y −18,609, y coinciden 108 valores y 89 celdas del libro.

| | Veredicto | Objeción principal |
|---|---|---|
| P1 | Resuelto en parte | V2: lo que se cobra como término explícito sigue en el denominador del ancla de S2C; con crecimiento se cobra dos veces. Los casos P1 son todos a crecimiento cero |
| P2 | Resuelto en parte | V1 (material): el crecimiento orgánico publicado solo excluye las adquisiciones «importantes»; las pequeñas (31,5 al año, el 10,2 % del FCF base) están dentro. El §3 de esta respuesta describe mal ese fundamento |
| P3 | Resuelto | V3: la caja del earnout (nota 2.4) y la actualización de 2025 (0,7) están publicadas. V4: el −11,6 depende de la convención del τ de cinco años (−9,1 con el de la ventana) y de qué se hace con 2021–22 |
| P4 | Resuelto en parte | V10: E2 y E4 aún dicen «aviso» y «materiales» contra E5. V6: el terminal duplica, con otra fórmula, la comparación que el libro ya tiene (Convenciones V6.3 §3; `Diagnóstico V6`, filas 176–179). V5: el 16,8 es solo la parte de los pagos |

Las demás:
- V7: E3 dice «sin cambios en la estructura del flujo» frente a los términos explícitos;
- V8: la cota de R;
- V9: casos sintéticos con el ancla a mano;
- V11: textos de aprobación.

**Estado: aplicadas después de esta respuesta**, por encargo de la persona responsable: [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md). Lo que sigue describe la situación al incorporar la revisión.

**Situación al incorporarla: no aplicadas.**
- Este encargo preveía una sola pasada: si la revisión encuentra una carencia de datos o de política, se documenta y se termina.
- Aplicar V1–V11 cambiaría la propuesta revisada y exigiría revisar lo afectado; decide la persona responsable.
- Comparto las once objeciones. No veo motivo para discrepar de ninguna.

**Carencias que bloquean y no son defectos** (su §10):
- M1;
- M2;
- M6, ahora concretado en la finalidad de las compras pequeñas y en el crecimiento orgánico sin ellas;
- N2;
- el perímetro de las palancas S2C y ROIC de Elis;
- la convención del tipo de proyección;
- qué hacer con el umbral de V-F1a y con el del aviso del terminal que ya tiene el libro.

Elis sigue en `pendiente_de_datos`.
