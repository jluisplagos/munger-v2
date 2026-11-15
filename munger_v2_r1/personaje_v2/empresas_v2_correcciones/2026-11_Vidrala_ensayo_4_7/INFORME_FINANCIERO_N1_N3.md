# Validación financiera N1–N3 de Vidrala · entrega 4.7, bloque B

Redactado por Claude (Opus) el 9-nov-2026 y **revisado tras tres auditorías internas de Claude**: la primera (`AUDITORIA_INTERNA_4_7_primera.md`), la de control de las correcciones (`AUDITORIA_INTERNA_4_7_control.md`) y la final (`AUDITORIA_INTERNA_4_7_final.md`). Esa auditoría encontró dos debilidades de razonamiento en N1 (H-5, H-6) y un error de fuentes en N2 (H-4), además de imprecisiones menores. Lo que cambió se dice en cada apartado y se resume en el §9. Todo está **ejecutado o declarado por Claude**; nada está comprobado externamente por ChatGPT. Se distinguen en cada apartado **hechos publicados**, **cálculos derivados**, **hipótesis** y **decisiones humanas**.

**Aviso de alcance.** Los valores, ponderados y precios de Sí son resultados mecánicos de un ensayo, calculados sobre copias identificadas. No son una comparación válida con el precio de 87,9 del 3-nov-2026 ni una recomendación de compra o espera. La aprobación técnica no es una validación financiera. El libro de referencia, sus valores y el registro humano P1 no cambian: las alternativas son propuestas hasta que la persona responsable decida (`financiero/decisiones_propuestas_N1_N3.json`, sin rellenar).

**Constantes que no cambian.** r = 0,09; probabilidades 0,2 / 0,6 / 0,2; k = 3; palancas de la fase B; caja 108,352 (sin volver a restar el dividendo de 43,338); puente 160,784; 35,206 millones de acciones. Lo único que cambia de forma derivada es `r_op` (Diagnóstico V6!C15), porque su fórmula usa el tipo impositivo. Ese efecto se separa en el §2.4.

## 1. Método y trazabilidad

- **Fuentes.** Textos conservados del expediente de referencia (`2026-11_Vidrala_ensayo_4_6_1/Vidrala/texto/CF_AAAA.txt`), generados a partir de los PDF oficiales. No se ha usado ninguna fuente nueva.
- **Matriz de evidencia.** `scripts/analisis_n1_n3.py` vuelve a extraer **109 datos publicados**. Cada uno se busca por concepto y columna en su archivo y página PDF, y se compara **con su signo** con el valor registrado (paréntesis = negativo). Los 109 se reproducen.
  - Están en `financiero/evidencia.md` y `evidencia.json`.
  - De cada dato se anotan página impresa, período, perímetro, unidad, signo publicado y línea literal.
  - Si un dato no se reproduce, el script termina con código 1.
  - Antes de la auditoría se comparaban valores absolutos (H-15).
- **Réplica.** La réplica en Python del motor B se valida contra el libro de referencia antes de calcular nada: 53,6704 / 70,7722 / 86,4888, ponderado 70,4952, precio de Sí 65,6881 y `r_op` 0,0869221. La tolerancia es de 0,005 €; si falla, el script termina con código 1.
- **Fundamentos y su historia.**
  - Las alternativas de cada asunto y su fundamento están fijados en el diccionario `ALTERNATIVAS` del script. Hay tres por asunto, base incluida, y 27 combinaciones.
  - El fundamento de dos alternativas cambió después de calcular una primera matriz. El del N3 se revisó por coherencia antes de la auditoría (§4.2). El de T1 se revisó por la auditoría (§2.4).
  - Las formulaciones anteriores, con su script y su matriz, se conservan en `financiero/formulacion_inicial_N3/` y `financiero/formulacion_inicial_N1/`.
- **Libros de propuesta.** `scripts/propuesta_excel.py` recalcula dos copias identificadas del libro con LibreOffice, en recálculo forzado. En las dos, el libro coincide con la réplica (§5).

## 2. N1 · Tipo impositivo

### 2.1 Hechos publicados: conciliación completa (puntos sobre la base de cada conciliación)

| Línea (clase) | 2021 | 2022 | 2023 ¹ | 2024 | 2025 |
|---|---|---|---|---|---|
| Fuente | CF_2021, PDF p. 49 | CF_2022, p. 51 | CF_2024, p. 61 (comparativo) | CF_2025, p. 57 (comparativo) | CF_2025, p. 57 |
| Base (resultado antes de impuestos) | 172,514 | 187,748 | 287,493 ¹ | 303,218 | 276,661 |
| Al tipo de cada país (recurrente) | +22,42 | +23,29 | +23,89 | +32,96 ² | +24,27 |
| Deducciones del año (recurrente) | −4,33 | −5,27 | −1,03 | −1,06 | −0,83 |
| Diferencias permanentes (recurrente) | −3,34 | −0,60 | −3,36 | −9,27 ² | −2,09 |
| Otros ajustes (naturaleza no publicada) | −1,63 | +0,56 | +0,06 | −1,20 | +1,93 |
| Ajustes de ejercicios anteriores (no recurrente) | −1,19 | −0,10 | −0,01 | −0,01 | −0,02 |
| Cambio de tipo (no recurrente) | +3,19 | — | — | — | — |
| Reducción o aumento de pasivos diferidos (no recurrente, signo variable) | +0,73 | +0,26 | −0,49 | — | +1,06 |
| **Gasto (cuadra con el estado)** | 27,357 | 34,062 | 54,813 | 64,968 | 67,320 |
| **Tipo efectivo sobre el resultado de continuadas** | **15,86 %** | **18,14 %** | **20,40 %** ¹ | **21,43 %** | **24,33 %** |
| Corriente / pagado (mm) | 15,878 / 27,800 | 23,599 / 8,600 | 63,249 ³ / 45,021 ³ | 65,376 / 70,100 | 56,136 / 40,757 |

¹ **2023.** El informe de 2024 trae una conciliación comparativa que termina en el gasto reexpresado sin Italia (54,813), pero mantiene la base publicada de 287,493 y cambia «otros ajustes» de (530) a 185. La reexpresión es parcial. El tipo efectivo usa el resultado reexpresado de continuadas, 268,649 (CF_2024, p. 4); los puntos de la tabla usan la base de la conciliación.
² **2024.** «The permanent differences primarily correspond to the exemption associated with the capital gain from the sale of the Italian subsidiary» (CF_2024, PDF p. 61). **Interpretación** (no lo dice el texto, auditoría de control C-8): la plusvalía entra en la línea del tipo de cada país (+32,96 frente a ≈ 24 los demás años) y su exención en las diferencias permanentes, y las dos se compensan en el gasto (H-5); así, el 21,43 % de 2024 no estaría rebajado por la exención neta. Es coherente con que la plusvalía consolidada, 50 mm, figure en el resultado de operaciones interrumpidas, fuera de la base de 303,218 (CF_2024, PDF p. 34).
³ Perímetro publicado de 2023, con Italia.

Las 31 líneas de importe forman parte de la matriz de evidencia (claves `conc_*`), y cada conciliación cuadra con su gasto.

### 2.2 Reconstrucción del 20,0 %

- **Hecho:** los tipos de la Historia (fila 10, H10:L10) son exactamente gasto ÷ resultado antes de impuestos de cada año.
- **Cálculo:** su media 2021–2025 es 0,20033, frente a Historia!C52 = 0,20032 en la hoja; la diferencia es de redondeo.

Componentes, según la tabla:
- **2021 y 2022:** perímetro con Italia y deducciones del año de 4,3 y 5,3 puntos, frente a 0,8–1,1 en 2023–2025.
- **2021:** además, un ajuste por cambio de tipo de +3,2 puntos y ajustes de ejercicios anteriores de −1,2.
- **Tipo de cada país:** sube de 22,4 % en 2021 a 24,3 % en 2025, sin contar 2024. El informe no desglosa las causas; la mezcla de países es la explicación más directa, pero no está acreditada en los textos conservados (se retira la afirmación sobre el Reino Unido y Brasil, H-11).

### 2.3 Gasto, corriente, diferido y pagado

- **Hecho, 2025:** gasto 67,320 = corriente 56,136 + diferido 11,184. El diferido sale sobre todo del aumento del pasivo por amortización acelerada: «Expense for increase of deferred tax liabilities 14,624» (CF_2025, PDF p. 56).
- **Hecho:** el pagado de 2025 es 40,757.
- **Cálculo:** pagado ÷ resultado antes de impuestos = 16,1 / 4,6 / 15,7 / 23,1 / 14,7 %, con una media del 14,8 %. Es muy irregular porque depende del calendario de pagos fraccionados y devoluciones.
- **Interpretación:**
  - El NOPAT de la plantilla grava el EBIT con un tipo sobre el gasto, el devengado, y eso es lo coherente con el resto del motor.
  - El aplazamiento por amortización acelerada dura mientras la inversión supere a la amortización. No es una rebaja permanente y no entra en ninguna alternativa ni en el terminal.
  - El pagado no es una norma utilizable.

### 2.4 Alternativas, efecto y recomendación

| Alternativa | Tipo | Fundamento | Ponderado (M0·R0) | Precio de Sí (M0·R0) |
|---|---|---|---|---|
| **T0** base | 20,03 % | media del efectivo 2021–2025 (C52): incluye 2021–2022, con Italia, deducciones de 4–5 puntos y el cambio de tipo de 2021 | 70,50 | 65,69 |
| **T1** propuesta | 22,05 % | media del tipo efectivo 2023–2025 del perímetro de continuadas, con **todas** las líneas de la conciliación | 68,56 (−1,93) | 63,92 (−1,77) |
| **T2** adversa | 24,33 % | último año de una serie que sube (20,4 → 21,4 → 24,3 %), con +1,9 puntos de otros ajustes sin acreditar y +1,1 de diferidos | 66,38 (−4,11) | 61,92 (−3,77) |

- **Por qué T1** (criterio simétrico):
  - Usa los tres años del perímetro actual y no elige líneas de la conciliación: entran tal como ocurrieron.
  - Según la interpretación de la nota ², la plusvalía de Italia de 2024 no lo distorsiona, porque su exención la compensa.
- **Robustez** (cálculo derivado):
  - sin las líneas no recurrentes (ejercicios anteriores, cambios de tipo y diferidos de signo variable), la media sería 21,88 %, con 20,93 / 21,43 / 23,29 % por año;
  - quitando además los «otros ajustes», cuya naturaleza no se publica, sería 21,62 %;
  - si no se acepta la interpretación de 2024 y se excluye ese año, sería 22,37 % (2023 y 2025), con −0,30 de ponderado y −0,28 de precio de Sí frente a T1 (auditoría final, F-9, calculado con la réplica);
  - las variantes de robustez quedan a los dos lados de T1, que no es la más favorable de ellas.
- **Formulación anterior, descartada tras la auditoría** (H-5, H-6):
  - T1 = tipo de cada país 2025 (24,27 %) − deducciones medias 2023–2025 (0,97 pp) = 23,30 %.
  - Excluía las diferencias permanentes, negativas los cinco años, y rechazaba el 22,0 % con un argumento (la exención de 2024) que contradecía la propia nota ².
  - La revisión **sube** el valor: en la combinación recomendada, el ponderado pasa de 68,04 a 69,24 y el precio de Sí de 63,15 a 64,26. Se hace por el criterio, no por el resultado; T2 sigue en la matriz como sensibilidad adversa.
- **Cálculo derivado:** de los −1,93 del ponderado (T0 → T1), −2,04 vienen del NOPAT y del terminal y +0,11 de `r_op`, que baja de 0,086922 a 0,086822.
  - Ese efecto sobre `r_op` sale de la fórmula de la hoja, no de un cambio de r.
- **Elasticidad** (en T1·M1·R1): +1 punto de tipo mueve el ponderado −0,97 y el precio de Sí −0,89.
- **Propuesta:** T1 = 22,05 % para el NOPAT de los años 1–10 y para el terminal.
- **Incertidumbre residual, en los dos sentidos:**
  - **al alza:** la serie sube, y 2025 (24,3 %) podría ser la nueva norma. Es la T2; su efecto frente a T1 es de ≈ −2,2 en el ponderado;
  - **a la baja:** los «otros ajustes» y los diferidos de 2025 (+3,0 pp) podrían no repetirse (21,6–21,9 %);
  - **la lectura de 2024:** sin ese año, 22,37 %;
  - **ni 20,0 ni 22,0 ni 24,3 % son normas automáticas:** T1 es una medición con criterio declarado.
- **Decisión humana pendiente:** D-N1.

## 3. N2 · Margen de partida

### 3.1 Años y perímetros dentro de la media del ciclo (Historia!C49 = 16,86 %)

| Año | Margen de la Historia | Perímetro y fuente del segmento | Sin Italia | Sin Italia ni Brasil |
|---|---|---|---|---|
| 2016 | 12,03 % | con Italia, sin Santos Barosa (adquirida en 2017); Italia sin segmento propio | sin dato | — |
| 2017 | 14,24 % | con Italia; los informes 2017 y 2018 solo dan «Continental Europe» | sin dato | — |
| 2018 | 15,39 % | con Italia: EBIT ≈ 0,92 sobre 53,9 (1,7 %), CF_2019, p. 39 | 16,21 % | 16,21 % |
| 2019 | 17,56 % | con Italia: ≈ 2,72 sobre 62,7 (4,3 %), CF_2019, p. 38 | 18,44 % | 18,44 % |
| 2020 | 19,66 % | con Italia: ≈ 11,08 sobre 72,3 (15,3 %), CF_2020, p. 39 | 20,00 % | 20,00 % |
| 2021 | 16,47 % | con Italia: ≈ 4,60 sobre 83,9 (5,5 %), CF_2021, p. 30 | 17,39 % | 17,39 % |
| 2022 | 13,69 % | con Italia: ≈ 6,02 sobre 106,0 (5,7 %), CF_2022, p. 30 | 14,38 % | 14,38 % |
| 2023 | 18,74 % | reexpresado sin Italia; Brasil desde noviembre: ≈ 6,86 sobre 19,1 (35,8 %), CF_2024, p. 30 | 18,74 % | 18,51 % |
| 2024 | 20,84 % | continuadas; Brasil ≈ 65,65 sobre 199,9 (32,8 %); Italia residual 17,0 de ingresos | 20,84 % | 19,15 % |
| 2025 | 19,93 % | continuadas; Brasil ≈ 53,87 sobre 178,3 (30,2 %), CF_2025, p. 27 | 19,93 % | 18,51 % |

**Notas a la tabla.**
- El EBIT de los segmentos es un **cálculo derivado**: resultado antes de impuestos + gastos − ingresos financieros, con su signo (en Italia 2018–2019 los ingresos financieros se publican entre paréntesis), y en Brasil 2023 − 5,607 de valor razonable. Es la misma identidad que reproduce el EBIT consolidado de la Historia (2025: 276,661 + 31,001 − 15,101 − 493 = 292,068).
- Italia 2023, interrumpida: ≈ 22,33 sobre 131,3 (17,0 %).
- La versión anterior de este informe decía que no había EBIT de Italia en 2018–2019. Era falso: CF_2019, p. 38–39, trae la cuenta por segmentos de los dos años (auditoría interna, H-4).

### 3.2 La afirmación de fase_c.md

fase_c.md (línea 112) afirma: «Una media del perímetro de 2025 con los mismos años no puede quedar por debajo» del 16,9 %. **No queda demostrada.** Sería cierta solo si se cumplieran tres condiciones que los textos conservados no acreditan:
1. que el margen de Italia fuera inferior al del grupo también en 2016–2017, para los que no hay segmento propio (en 2018–2022 lo es todos los años);
2. que Santos Barosa, que falta en 2016, no tuviera un margen inferior al 12,0 % del grupo ese año;
3. que Brasil, que en el perímetro de 2025 habría que añadir a todos los años, tuviera antes de 2023 márgenes no inferiores a los del grupo. No hay datos pro forma.

Lo que sí está medido apunta en la misma dirección. Italia rinde menos que el grupo en 2018–2023, y quitarla eleva cada año de 2018 a 2022. Brasil rinde más que el grupo en 2023–2025.

**Consecuencia:** el intervalo 16,9–19,9 % de la fase C se describe solo como una **sensibilidad condicional**, no como límites. Con T0·R0, el precio de Sí va de 65,69 a 67,46 (+2,7 %); el libro lo reproduce (§5).

### 3.3 Efectos de perímetro, ciclo y estructura (cálculos derivados)

- **Perímetro, Italia:** quitar Italia donde se conoce (2018–2022), con la ventana 2016–2025, sube la media de 16,86 a 17,22 % (**+0,36 pp**).
- **Ciclo, ventana:** quitar 2016–2019 (años de margen bajo, previos a Santos Barosa y a la mejora) lleva la media de 17,22 a 18,55 % (**+1,33 pp**). 2022, con la crisis energética (14,4 %), queda dentro: la ventana no excluye el año malo del ciclo reciente.
- **Estructura, Brasil:** dentro de M1, Brasil aporta **+0,56 pp** (M1 = 18,55 % frente a M1b = 17,99 %, el grupo sin Italia ni Brasil). Es un efecto de composición y queda en la base de partida, porque V0 incluye Brasil.

### 3.4 Alternativas y recomendación

| Alternativa | Margen | Fundamento | Ponderado (T1·R1) | Precio de Sí (T1·R1) |
|---|---|---|---|---|
| **M0** base | 16,86 % | media 2016–2025 (C49) | 68,28 | 63,31 |
| **M1** propuesta | 18,55 % | media 2020–2025 en perímetro de continuadas | 69,24 | 64,26 |
| **M2** | 19,93 % | 2025 (C8 = «Último año», representable en la plantilla) | 70,03 | 65,04 |

- **Elasticidad:** +1 pp de margen de partida mueve el ponderado +0,57 y el precio de Sí +0,56.
- **Sensibilidades complementarias, fuera de la matriz:**
  - M1b = 17,99 % da un ponderado de 68,93 (−0,32) y un precio de Sí de 63,95 (−0,31);
  - la ventana 2018–2025 sin Italia, 18,24 %, ya posible con los datos de 2018–2019, quedaría en ≈ −0,18 de ponderado (cálculo por elasticidad).
- **Propuesta:** M1 (18,55 %).
  - Mantiene la regla «media del ciclo» que la fase C eligió para una cíclica y corrige el error de perímetro medible (Italia).
  - Usa seis años que contienen un año malo (2022) y dos buenos (2020, 2024).
  - No se propone M2: un solo año, y la empresa supone rebajas de precio en 2026 («price decreases are assumed for 2026 in Vidrala Europe and Encirc», CF_2025, PDF p. 48).
- **Incertidumbre:** la de la ventana (2020–2025 o 2018–2025: −0,31 pp) y la de Brasil (−0,56 pp si se excluyera).
- **Decisión humana pendiente:** D-N2.

## 4. N3 · El MALO y la reinversión con ventas que caen

### 4.1 Reconstrucción año a año (T0·M0, la base)

Archivo completo, con T1·M1 y las tres reglas, en `financiero/n3_anio_a_anio.csv`.

| Año | Ventas | NOPAT | Reinversión R0 | FCF R0 | Reinversión R1 | FCF R1 | FCF R2 |
|---|---|---|---|---|---|---|---|
| 1 | 1.450,5 | 191,2 | −16,3 | 207,5 | −2,2 | 193,4 | 191,2 |
| 2 | 1.436,0 | 185,0 | −16,1 | 201,2 | −2,1 | 187,2 | 185,0 |
| 3 | 1.421,6 | 179,0 | −16,0 | 194,9 | −2,1 | 181,1 | 179,0 |
| 4 | 1.407,4 | 173,0 | −15,8 | 188,8 | −2,1 | 175,1 | 173,0 |
| 5 | 1.393,4 | 167,1 | −15,6 | 182,8 | −2,1 | 169,2 | 167,1 |
| 6 | 1.385,0 | 166,1 | −9,3 | 175,4 | −1,2 | 167,4 | 166,1 |
| 7 | 1.382,2 | 165,8 | −3,1 | 168,9 | −0,4 | 166,2 | 165,8 |
| 8 | 1.385,0 | 166,1 | +3,1 | 163,1 | +0,4 | 165,7 | 166,1 |
| 9 | 1.393,3 | 167,1 | +9,2 | 157,9 | +1,2 | 165,9 | 167,1 |
| 10 | 1.407,2 | 168,8 | +15,5 | 153,3 | +2,0 | 166,8 | 168,8 |

- **Capital liberado en diez años:** R0 92,2 mm; R1 12,2 mm; R2 0.
- **NORMAL, año 1:** ventas 1.494,5, NOPAT 204,2, reinversión +32,6, FCF 171,6.

**Los ≈ 16 mm** son V0 × |g1| ÷ S2C = 1.465,16 × 0,01 ÷ 0,9 = 16,28. La plantilla aplica ΔV ÷ S2C también cuando ΔV es negativo, de modo que cada euro de ventas perdido devuelve 1,11 € de capital.

**Por qué el FCF1 del MALO supera al del NORMAL** (207,5 frente a 171,6, +35,9). Se descompone así:
- ΔNOPAT de −12,96;
- Δreinversión de −48,84: el NORMAL reinvierte 32,6 para crecer y el MALO libera 16,3.

Aun sin liberar nada (R2), el MALO del año 1 (191,2) supera al NORMAL, porque no reinvierte para crecer. Esa parte es coherente. Lo discutible es solo la liberación.

### 4.2 Realizabilidad

- **Circulante comercial**, hecho: existencias 252,454 + deudores 315,821 − acreedores 352,841 = 215,434 mm, el **14,70 %** de las ventas de 2025 (CF_2025, PDF p. 2–3). En 2024 era el 14,88 %. Es lo que puede liberarse si caen las ventas.
- **Activo fijo.** Hecho: en 2025 las ventas bajaron 123,1 mm y aun así la inversión (188,5) superó a la amortización (132,9) (Historia, filas 8 y 12). Hecho: los compromisos de compra de instalaciones y maquinaria suben de 9,622 a 66,610 mm (CF_2025, PDF p. 45). Interpretación: la planta no se desinvierte cuando cae la demanda; queda capacidad ociosa.
- **Necesidades de caja.** Cálculo: la inversión bruta implícita del MALO en el año 1 es la amortización de 2025 más la reinversión neta, 132,9 − 16,3 = 116,7 (R0), 130,8 (R1) o 132,9 (R2). Cubre los 66,6 mm comprometidos con cualquiera de las tres reglas, y el FCF1 del MALO (191–207 en la base, 202–218 con T1·M1) también.
  - Los compromisos no hacen irrealizable ninguna regla. Lo que hace poco realista la R0 es su supuesto de desinversión simétrica.
  - El dividendo de 43,338 no se vuelve a restar de la caja.
- **Coherencia de la recuperación** (fundamento de R1 y R2). Si el capital fijo no se libera al caer las ventas, la recuperación hasta el máximo ya alcanzado no exige inversión fija nueva: con R1 solo se repone el circulante, con R2 nada, y por encima del máximo, ΔV ÷ S2C. En el MALO las ventas no vuelven al nivel de 2025 en diez años.
- **Registro de la revisión.** La primera formulación del script aplicaba la asimetría solo al caer y cobraba ΔV ÷ S2C completo en la recuperación.
  - Con T1 = 23,30 % y M1, R1 daba ponderado 67,97 y precio de Sí 63,02; la regla revisada da 68,04 y 63,15 (valor MALO 50,64 → 50,95).
  - La regla se cambió después de calcular esa primera matriz y antes de redactar las conclusiones. El motivo es que la primera cobraba reinversión fija por un capital que nunca se liberó, una incoherencia interna, no el valor resultante.
  - Se conservan el script y la matriz de entonces en `financiero/formulacion_inicial_N3/`. La auditoría interna la juzgó justificada (H-14).
- **Fuera del alcance:** el terminal mantiene la fórmula de la plantilla, con reinversión g ÷ ROIC desde el año 11, aunque en el MALO las ventas del año 10 sigan por debajo del máximo. Queda como incertidumbre menor.

### 4.3 Alternativas y recomendación

| Alternativa | Regla | Ponderado (T1·M1) | Precio de Sí (T1·M1) | V MALO |
|---|---|---|---|---|
| **R0** base | liberación simétrica ΔV ÷ S2C (la plantilla) | 69,53 | 64,87 | 53,22 |
| **R1** propuesta | al caer, solo se libera el circulante (14,70 %); en la recuperación hasta el máximo anterior solo se repone el circulante | 69,24 | 64,26 | 51,81 |
| **R2** adversa | sin liberación; en la recuperación hasta el máximo anterior, sin reinversión | 69,20 | 64,17 | 51,59 |

- **Propuesta:** R1.
  - Responde a la composición del balance: solo el circulante es líquido.
  - Concuerda con la historia de la fase C («La historia dice que la reinversión no baja», fase_c.md, línea 22) y con lo ocurrido en 2025.
  - No baja el MALO por bajarlo: la diferencia con R0 es solo la liberación de capital fijo que no se observa.
  - Efecto sobre la combinación T1·M1: ponderado −0,28 y precio de Sí −0,61. Solo cambia el MALO, que pesa el 20 % y además marca la escalera.
- **Representabilidad:** la plantilla no puede representar R1 ni R2, porque la reinversión es ΔV ÷ S2C en las dos direcciones. Quedan en el modelo auxiliar.
- **Decisión humana pendiente:** D-N3.

## 5. Libros de propuesta (Excel)

`scripts/propuesta_excel.py` genera dos copias identificadas en `financiero/propuesta_excel/`, más la salida y la comparación celda a celda.

| Libro | Cambio frente a la referencia | Representación | Libro recalculado | Réplica | Celdas distintas |
|---|---|---|---|---|---|
| `PROPUESTA_M2_ultimo_anio.xlsx` | Palancas!C8 = «Último año» | entrada propia de la plantilla, escrita con `escribir_v63.py` | V 55,3774 / 72,5801 / 88,3487; ponderado 72,2933; precio de Sí 67,4602 | T0·M2·R0: coincide | 1 entrada |
| `PROPUESTA_T1_M1.xlsx` | Diagnóstico V6!C11 = 0,220541 (antes `=Historia!$C$52`); Diagnóstico V6!C10 = 0,185467 (antes la fórmula de C8) | sustitución de dos fórmulas intermedias, **solo en la copia de propuesta** | V 53,2198 / 69,7806 / 85,0759; ponderado 69,5275; precio de Sí 64,8682; `r_op` 0,086822 | T1·M1·R0: coincide (diferencias ≤ 0,0001 € por el redondeo a seis decimales de las celdas) | 2 celdas |

- **Primer intento, registrado y descartado:** sustituir Historia!C52 y C49 por valores. La regla V39 del Motor lo bloquea, porque Historia!C52 es una celda de salida protegida («ha sido sobrescrita con un valor: restaura la fórmula»), y la hoja no da valor.
- **Lo que se hizo:** en su lugar se sustituyen las celdas intermedias que consume el motor (Motor D·, K·, y `r_op`). Así **se elude, de forma declarada, la protección de la plantilla un nivel más abajo**; no se respeta. Historia, sus fórmulas y los hechos publicados quedan intactos.
- **Consumidores que siguen leyendo Historia**, sin entrar en el valor:
  - Diagnóstico V6!B176:D176 (comparación de anclas), Motor E218 y E236 (V39), que leen Historia!C52;
  - Palancas!F15 («media propia»), que lee Historia!C49 y sigue mostrando 16,86 % en la propuesta.
- **Aviso en los archivos de precio.** Los `precio.json` de las propuestas llevan un campo `aviso`. Dice que la zona, las distancias y `g_impl` frente a 87,9 no son una comparación válida ni una recomendación.
- **La propuesta B no es una V6.3 íntegra.** Para llevar T1 o M1 a un libro oficial haría falta una entrada de plantilla, tipo normalizado o margen de partida manual, o que la persona responsable decida otra vía. Es una **propuesta de cambio de plantilla**, no aplicada.
- **R1** no tiene representación en la plantilla. La combinación recomendada completa, T1·M1·R1, solo existe en el modelo auxiliar.

## 6. Matriz conjunta (27 combinaciones)

La matriz completa está en `financiero/matriz.md` y `matriz.csv`. Por cada combinación da:
- los valores MALO, NORMAL y BUENO, el ponderado y el precio de Sí mecánico;
- el peso del terminal, el FCF inicial y el mínimo;
- el capital liberado, la reinversión y el FCF de los años 1–5 del MALO;
- la cobertura de los compromisos y las diferencias frente a la base.

**Clases.** Las 15 combinaciones con T0 o M0 son **sensibilidades mecánicas**, porque contienen una medición de la base con error de perímetro. Las 12 con T1/T2 y M1/M2 son **hipótesis coherentes**, y una de ellas es la recomendada.

| Combinación | V MALO / NORMAL / BUENO | Ponderado (Δ) | Precio de Sí (Δ) | Peso terminal NORMAL | FCF1 MALO / NORMAL | FCF mín. MALO | Clase |
|---|---|---|---|---|---|---|---|
| T0·M0·R0 (base) | 53,67 / 70,77 / 86,49 | 70,50 | 65,69 | 0,525 | 207,5 / 171,6 | 153,3 | base |
| T1·M0·R0 (solo N1) | 52,31 / 68,81 / 84,08 | 68,56 (−1,93) | 63,92 (−1,77) | 0,527 | 202,7 / 166,5 | 149,1 | sensibilidad |
| T0·M1·R0 (solo N2) | 54,61 / 71,77 / 87,51 | 71,48 (+0,99) | 66,66 (+0,97) | 0,518 | 223,2 / 187,8 | 153,3 | sensibilidad |
| T0·M0·R1 (solo N3) | 52,26 / 70,77 / 86,49 | 70,21 (−0,28) | 65,08 (−0,61) | 0,525 | 193,4 / 171,6 | 165,7 | sensibilidad |
| **T1·M1·R1 (recomendada)** | **51,81 / 69,78 / 85,08** | **69,24 (−1,25)** | **64,26 (−1,43)** | **0,520** | **203,8 / 182,2** | **161,5** | **hipótesis coherente recomendada** |
| T1·M2·R0 (máximo coherente) | 53,97 / 70,58 / 85,89 | 70,32 (−0,18) | 65,65 (−0,04) | 0,514 | 230,5 / 195,1 | 149,1 | hipótesis coherente |
| T2·M1·R2 (mínimo coherente) | 50,02 / 67,54 / 82,32 | 66,99 (−3,50) | 62,14 (−3,55) | 0,522 | 195,8 / 175,9 | 156,9 | hipótesis coherente |

- **Recorrido de las 12 hipótesis coherentes:** ponderado 66,99–70,32, precio de Sí 62,14–65,65.
- **Peso de cada asunto:** N1 (≈ −1,9 de ponderado) y N2 (≈ +1,0) se compensan en parte. N3 es menor (≈ −0,3), pero es el que más corrige la forma del MALO.
- **Tolerancias:** el script verifica la réplica con 0,005 €. Los dos libros de propuesta coinciden con la réplica dentro de esa tolerancia.

## 7. Recomendaciones (propuestas; las decisiones son de la persona responsable)

| Asunto | Propuesta | Efecto aislado sobre la base (ponderado / precio de Sí) | Dónde decidir |
|---|---|---|---|
| N1 | T1 = 22,05 % para el NOPAT y el terminal; T2 (24,33 %) como sensibilidad adversa | −1,93 / −1,77 | D-N1 |
| N2 | M1 = 18,55 %; describir 16,9–19,9 % solo como sensibilidad condicional | +0,99 / +0,97 | D-N2 |
| N3 | R1: liberación solo del circulante, capacidad conservada | −0,28 / −0,61 | D-N3 |
| Conjunta | T1·M1·R1 | −1,25 / −1,43 | las tres |
| Plantilla | añadir entradas para tipo normalizado y margen de partida manual, y una regla de reinversión asimétrica | — | propuesta de cambio de plantilla, no aplicada |

## 8. Estado de los demás pendientes (sin cambios)

- **N4:** los 38 ceros pendientes (L26, C48); la IA no confirma ceros. **N9:** ruta B (E1–E7). **N10:** probabilidades. **P-N1:** los dos sentidos de «conclusión favorable». **P-N2:** la huella de `verificacion_integridad.txt`. Todos siguen abiertos, igual que en la 4.6.1.
- **Nuevos de la 4.7:**
  - el segmento de Italia de 2016–2017 (en 2018–2019 está);
  - el margen de Santos Barosa en 2016;
  - el pro forma de Brasil antes de 2023;
  - la naturaleza de los «otros ajustes» y de las diferencias permanentes recurrentes de la conciliación fiscal;
  - el terminal del MALO con capacidad ociosa.

## 9. Cambios tras la auditoría interna de Claude

| Hallazgo | Qué cambia |
|---|---|
| H-4 (importante) | Italia 2018–2019 añadida a la evidencia y a los cálculos. Perímetro +0,36 pp (antes +0,19), ventana +1,33 pp (antes +1,50), media de 10 años 17,22 % (antes 17,05 %). M1 y la conclusión de §3.2 no cambian; la condición 1 se reduce a 2016–2017 |
| H-5 y H-6 (importantes) | Conciliación completa en la tabla y en la evidencia. T1 pasa de 23,30 % (selección asimétrica) a 22,05 % (todas las líneas), con robustez de 21,6–21,9 % e incertidumbre en los dos sentidos. Fundamento de T2 reescrito. La formulación anterior se conserva |
| H-11, H-12 | Retirada la afirmación sin fuente sobre el Reino Unido y Brasil; nota ¹ corregida (la conciliación comparativa de 2023 existe y es parcialmente reexpresada) |
| H-13 | Redacción: la protección V39 se elude de forma declarada; se añade Palancas!F15; aviso en los `precio.json` de propuesta |
| H-14 | Redacción del §1 y del §4.2; descripción completa de R1 en D-N3 |
| H-15 | La evidencia se compara con signo |
| F-9 (auditoría final) | Efecto de la sensibilidad sin 2024 calculado con la réplica (−0,30 / −0,28) |
| C-7, C-8, C-11 (auditoría de control) | Patrón de «cambio de tipo» restringido a la línea de la conciliación y columna publicada anotada en la evidencia; la compensación de 2024 rotulada como interpretación, con la p. 34 y la sensibilidad sin 2024 (22,37 %); cabecera del script alineada con el §1 |
