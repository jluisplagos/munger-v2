# Fase C · turno 1 · Vidrala, S.A. (VID) · base 31-dic-2025 · V6.4 experimental, motor B (expediente de decisiones de la rama 4.14)

Reviso las fases A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Parto del turno 1 de la fase C de la rama 4.14 (`vidrala/Vidrala/fase_c.json` y `fase_c.md`), copiado aquí como `fase_c.rama.json` y `fase_c.rama.md`. Conservo lo que E1, E4 y las reservas E2 y E3 no invalidan y cambio solo lo que sí invalidan.

Fuentes de los hechos:
- `datos_v63.md` de este expediente (Historia, anclas y sección 0 de la configuración);
- `extracto_v63.md`, reutilizado de la rama: [ES, PDF p. n] es ES 2025 (doc. 2308); [ES_2024, PDF p. n] es ES 2024 (doc. 2118); [CF_aaaa, PDF p. n] son las cuentas en inglés;
- lo que calcula la hoja: `resultados.json`, `precio.json`, `configuracion_v64_variantes.md` (19 variantes) y `contraste_objetivo_v64.md`;
- las decisiones y supuestos de entradas: `configuracion/cambio_decisiones_vidrala_4_14.json` y `hitos/decisiones/DECISIONES_ENTRADAS_4_14.md`;
- su efecto medido: `resultados/efecto_correcciones_vidrala.md`, en la carpeta del ensayo 4.14.

Lo que marco «cálculo mío» es una aproximación con el tornado (3,68 € de valor NORMAL por punto de margen) y con la pendiente de la escalera (`precio_de_si.p_estrella`: 0,4286 € de precio de Sí por euro de valor MALO o NORMAL y 0,1429 € por euro de BUENO). No es un recálculo del libro.

## Cambios frente a la rama

**Qué cambia en la entrada.** Las fases A y B no cambian ninguna celda frente a la rama. El libro cambia solo en Análisis C46–C48 (`cambio_decisiones_vidrala_4_14.json`; datos_v63.md §2):
- **E1, decisión de la persona responsable (14-nov-2026):** C46 = 335,413 y C47 = 169,668, las medias exactas de 2023–2025, en lugar de los redondeos de la etapa 1 (335,4 y 169,7).
- **E4, supuesto de la orquestación, no decisión:** C48 queda vacío como dato ausente declarado. Ningún ejercicio publica intereses en financiación; antes era un cero heredado. La persona responsable no contestó E4 y pidió seguir con un supuesto razonable y decirlo. El supuesto aplica su requisito de verificación (cero verificado ≠ dato ausente) y se puede revertir con una decisión explícita.
- **Consecuencia de E4:** el libro ya no calcula el FCF base (C52), f (Historia C58), el semáforo de f ni «Precio ÷ FCF base», y el motor A deja de ser calculable (V09, `entrada_v63.md`). El motor B no se ve afectado.

E2 y E3 no cambian el libro:
- **E2, decisión de la persona responsable:** K14 = 84,994, la cifra publicada, con reserva sobre si dentro está la plusvalía de Italia (50,547 mm). La alternativa exploratoria (≈ 34,447) no se adopta.
- **E3, supuesto de la orquestación:** la pareja A de 2023 (87,210; 78,805) sin cambios, con reserva por las partidas no monetarias de Italia (11,061).

**Precio de Sí: 56,00201 €, idéntico al de la rama.** E1 y E4 solo tocan el motor A. `precio.json` y los valores de `resultados.json` son los de la rama; `contraste_objetivo_v64.md` es idéntico y las 19 variantes también (solo cambia la huella del libro en `configuracion_v64_variantes.md`). La lista de datos ausentes tiene los mismos 39 datos; solo cambia la nota de C48.

**Lo que cambio, y por qué:**
1. **Semáforo de f y múltiplos (punto 1).** Ya no digo «f = −2,8 %, en REVISAR, es la razón del motor B». f no se calcula (fila 50: «—») y la hoja cuenta 5 REVISAR (D7) en lugar de 6. «Precio ÷ FCF base» tampoco se calcula. Lo sustituyo por un cálculo mío: con C46 − C47 − C49 = 161,245 mm, 19,7 veces (5,1 %); con la alternativa de C48, 158,991 mm, 19,9 veces (5,0 %).
2. **Una fricción nueva (punto 1, n.º 10):** E4. La reviso y no rompe la historia.
3. **Límite del modelo (punto 5).** Quito «FCF base positivo (161,2 mm, C52)». C52 no existe en este libro. Lo apoyo en lo que sí está: C46 − C47 − C49 = 161,245 mm (o 158,991 con la alternativa de C48) y la caja al accionista de 2023–2025 (105,9, 187,6 y 183,5 mm, Historia J35:L35). Sigue sin haber límite del modelo.
4. **C48 en los datos ausentes (punto 6).** Pasa de «cero heredado, decisión E4 que no adopto» a dato ausente declarado por el supuesto E4. El efecto sigue medido en 0,000 €. Ajusto también las entradas de las filas 16 y 17, que citaban C52.
5. **E2 y E3: de «decisiones pendientes que no adopto» a lo que son.** E2 es una decisión de la persona responsable, con reserva. E3 y E4 son supuestos de la orquestación, no decisiones. Lo digo en el punto 1 (n.º 5), en la autocomprobación (n.º 7), en los límites del juicio sobre el objetivo de PM1.estructura y PM1.parametro, y en el motivo del objetivo.
6. **La medida de E2 y E3.** La rama daba «+0,03 a +0,05 €» y «−0,006 a +0,010 €»: los dos Δ de `efecto_correcciones_vidrala.md`, ambos frente a la activa 4.13 (56,01809 €). Frente a este expediente (56,00201 €), con las correcciones de la rama ya dentro:
   - K14 ≈ 34,447 da 56,05107 €: **+0,049 €**. El «+0,033 €» del registro de decisiones es el Δ frente a la activa 4.13.
   - K14 ≈ 33,594 da 56,05198 €: +0,050 €.
   - La pareja B de 2023 da 56,01192 €: **+0,010 €**. El «−0,006 €» del registro es frente a la 4.13.
   - E4 con 2,254 mm y E1 con los redondeos: 0,000 €.

   Ninguna llega al criterio de 1,58 € ni cambia la zona.
7. **Fundamento material (punto 7).** Anoto lo que las fases A y B reescribieron (apoyos que leían C52 y f) y la reserva E2/E3 en el apoyo del S2C (C53 = 0,886 con K14 publicado; ≈ 0,978 si la plusvalía estuviera dentro). Ninguna hipótesis pierde el fundamento. La lista D10 sigue vacía.
8. **Autocomprobación, n.º 1 y 3.** El ancla y el compromiso ya no son con la 4.13, sino con la fase C de la rama, que tienta copiar entera porque el precio de Sí es el mismo.

**Lo que no cambia:**
- el cubo provisional (Vigilar) y la conclusión (esperar);
- `alguno_material = false` y la lista D10 vacía (`no_procede`);
- `revisar_palancas = false` y las dos celdas revisadas (C15 y B16);
- las dos justificaciones de G8, con los mismos hechos;
- los doce parámetros de la configuración, con su `juicio_objetivo` y el contraste copiado de `contraste_objetivo_v64.json` (comprobado: idéntico);
- el criterio de materialidad del objetivo: 1,58 €, `juicio_propio_del_agente`; no hay ninguna política adoptada y D1 sigue pendiente;
- los cuatro condicionantes del objetivo y el tratamiento (`objetivo_condicionado`);
- el mantenimiento (ninguna estructura más coherente) y los avisos de dominio (ninguno material).

## Cambios de la rama frente a la 4.13 (registro heredado)

Se conserva como estaba en la fase C de la rama. Lo que dice de C48 («cero heredado») y de E1–E4 («decisiones que no adopto») es el estado de la rama; el de este expediente está en la sección anterior.

**Lo que cambió en la entrada.** Las fases A y B no cambian ninguna celda. La rama corrige dos datos de la Historia (`CORRECCIONES_ENTRADAS_4_14.md` §2):
- **D&A de 2019 (F8):** de 97,091 a 91,088, sin el deterioro [CF_2020, PDF p. 13];
- **adquisiciones de 2024 (K13):** de −241,668 a −224,000, la cifra que publica la propia empresa [ES_2024, PDF p. 114].

K13 entra en D_hist, que pasa de 530,0 a 547,7 mm, y con él f, que baja de 1,1649 a 1,1587. El precio de Sí pasa de 56,01809 a 56,00201 €, solo por ese efecto mecánico, medido y reproducido (`efecto_correcciones_vidrala.md`). F8 no mueve el valor: 2019 está fuera de la ventana.

**Cifras que actualizó, sin cambiar ningún juicio:**
- Valores de 44,32 / 60,21 / 78,52 a 44,32 / 60,19 / 78,48 €; ponderado de 60,70 a 60,67 €.
- Rentabilidad marginal de 9,53 / 14,71 / 19,98 % a 9,48 / 14,63 / 19,87 %; salto del año 11 de 5,71 a 5,63 puntos (NORMAL) y de 7,98 a 7,87 (BUENO).
- DCF inverso: el precio descuenta un 14,3 % de crecimiento (antes 14,2 %).
- S2C marginal (C53): de 0,916 a 0,886. La circulante pesa el 50,9 % de la reinversión (antes 52,6 %). Cada euro de ventas nuevas pidió 0,56 € de inversión fija (antes 0,53).
- Capex sobre amortización desde 2017: de 1,15 a 1,74 veces (antes 1,10 a 1,74, por la D&A de 2019).
- f deja de estar definida en λ = 2,09 (antes 2,06). Con todo el exceso como reposición, f ≈ 1,72 (antes 1,76).
- Rango de las variantes: de 51,26 a 65,72 € (antes 51,29 a 65,72).

**Fuente nueva: ES 2024.** Hechos que usa:
- en 2024 las ventas a divisa constante y perímetro comparable crecieron un 0,2 % y el EBITDA un 10,5 % [ES_2024, PDF p. 97 y p. 98];
- el consumo de materias primas fue plano en 2024–2025 [ES_2024, PDF p. 214; ES, PDF p. 195];
- los covenants de 2024 se cumplían (0,55x y 18,80x) [ES_2024, PDF p. 81–82];
- la guía de 2024 para 2025 fue cualitativa salvo el dividendo, que se cumplió [ES_2024, PDF p. 101–102; ES, PDF p. 95];
- la concentración de clientes de 2024 se cita en [ES_2024, PDF p. 110], en lugar de CF_2024 p. 45.

**Datos ausentes.** La lista pasó de 30 a 39; ninguno nuevo es material.

**Juicios que cambiaron (contrato 4.14).** El juicio sobre el objetivo se separa del juicio sobre la acción, con un criterio declarado de 1,58 € de precio de Sí (juicio propio, no política; D1 pendiente):
- **PM1.roic_terminal** pasó de «no material para el objetivo» a **no determinada**, y condiciona el objetivo. La 4.13 lo excluyó sin comparación.
- **N1.tipo** pasó a material para el objetivo (+1,75 > 1,58). No condiciona, porque tiene fundamento suficiente.
- Los condicionantes del objetivo pasaron de tres a cuatro: PM1.estructura, PM1.familia, PM1.parametro y PM1.roic_terminal. El tratamiento no cambió: objetivo condicionado.

## 1. Una sola historia

**Lo que calcula la hoja.**
- Valor por acción: 44,32 / 60,19 / 78,48 € (MALO / NORMAL / BUENO). Ponderado: 60,67 €.
- Precio de Sí: 56,00 € (P\*, sin tope del NORMAL). Precio: 90,10 €, zona **caro**.
- Distancias: 90,10 está un 60,9 % por encima del precio de Sí (diferencia ÷ precio de Sí). El precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio).
- La regla antigua (C156) da 44,32.

**Peso del terminal:** 41 / 48 / 54 %, todos bajo el 75 %. G16 no salta.

**Semáforos:**
- el margen está en REVISAR en los tres escenarios (G5, justificado en la fase B);
- f (fugas al accionista, fila 50) sale «—»: no se calcula porque C48 está vacío como dato ausente (E4; datos_v63.md §3, C58 = —). En la rama era −2,8 %, en REVISAR. Por eso la hoja cuenta 5 REVISAR (D7) y no 6. La fase A ya no lo usa como apoyo del motor B;
- la cuota implícita no se calcula (C24 vacía), así que G17 no salta;
- el resto pasa.

El estado técnico es INCOMPLETO solo porque faltan las tres predicciones (Palancas A38:A40), que escribe el turno 2.

**Múltiplos:** PER 15,1 y EV ÷ EBITDA 7,8. «Precio ÷ FCF base» no se calcula (C52 vacío por E4). Cálculo mío con C46 − C47 − C49 = 161,245 mm: la capitalización (3.170 mm, C41) son 19,7 veces (rentabilidad del 5,1 %). Con la alternativa de C48 (158,991 mm), 19,9 veces (5,0 %).

**Veredicto de la hoja:** «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar: C13 mide el precio, no el negocio.

**DCF inverso.** A 90,10 € el precio descuenta un crecimiento de ventas del 14,3 % anual en los años 1–5 con el resto de mi NORMAL; al precio de Sí, −0,8 %. Mi NORMAL crece un 1,5 % y el BUENO un 3,5 %. La Historia da un 2,9 % a tres años y un 8,2 % a cinco, con el choque de precios de 2022 y la compra de Brasil (C45, C46). El precio supera el valor BUENO de la activa y de las 19 variantes (máximo 88,38 €, solo_N2).

**Tornado** (información, no criterio): ROIC LP ±5 puntos 12,67 €; tasa ±1 punto 10,56 €; margen ±2 puntos 7,36 €; crecimiento ±2 puntos 3,49 €; S2C ±0,3 2,23 €; g ±0,5 puntos 0,18 €.

**¿Cuentan la misma historia que `fase_a.md`?** Sí: un fabricante maduro de un envase pesado, con un margen que sigue a la energía, un foso estrecho que la Historia sostiene y un precio que paga más que mi escenario bueno. Las fricciones que encuentro no cambian ni el cubo ni la zona:

1. **Rentabilidad marginal.** La hoja calcula 9,48 / 14,63 / 19,87 % porque aplica f = 1,1587 al S2C (SR1) y el tipo N1. La fase B escribió ≈ 8,4 / 13 / 17,6 % con las bases heredadas, como le pide la sección 0. Solo por la configuración, el salto del año 11 del NORMAL pasa de 4,0 a 5,6 puntos.
2. **Crecimiento terminal** (corrección 4.13 §2). «ROIC terminal = r, luego crecer no crea valor» no vale: el motor descuenta a r_op = 8,689 % y el terminal carga la reposición. En la 4.13 se midió +0,88 € de valor NORMAL y +1,57 € de precio de Sí (`2026-11_Vidrala_ensayo_4_13/resultados/crecimiento_terminal_vidrala.md`). No está recalculado ni en la rama ni aquí. Los datos corregidos de la rama mueven el NORMAL 0,02 € y E1/E4 no lo mueven, así que leo el orden de magnitud como vigente (inferencia).
3. **El MALO bajo R1.** Su historia cuenta capex de hornos sin ventas, pero B16 no actúa (s2c_inerte) y ese capex solo entra por λ. A la vez, el terminal del MALO carga 15,8 mm al año. Se compensan (~1,09 € y ~0,96 €; cálculo mío de la 4.13, que los datos no tocan).
4. **Perímetro del margen NORMAL.** C15 = 0,18 sale de 2019–2025, con Italia hasta 2022; la media de continuadas (N2, 18,55 %) llevaría a 0,185. Cálculo mío: el precio de Sí iría de 56,00 a 56,79 (+1,4 %). No cambia cubo ni zona y queda bajo el 5 %: la dejo, con el cálculo escrito (v2.1).
5. **Mezcla de la reinversión.** El 50,9 % de la reinversión de 2021–2025 fue circulante (fila 14), con partidas que no son circulante comercial. En 2024 está la línea «Otros activos y pasivos corrientes y no corrientes» (106.417) [ES, PDF p. 14], que pudo absorber la plusvalía de Italia.
   - Sobre K14 hay una **decisión de la persona responsable (E2):** se mantiene el 84,994 publicado, con reserva sobre si dentro están los 50,547 mm de la plusvalía (60,065 de discontinuadas [ES_2024, PDF p. 37] menos 9,518 del semestre [ES, PDF p. 38]).
   - Si lo estuvieran, el circulante de 2021–2025 bajaría de 278,8 a 228,3 mm y su peso al 45,9 % de una D_hist de 497,1 mm (cálculo mío con la fila 14). El precio de Sí iría a 56,05 €, +0,049 € frente a este expediente (`efecto_correcciones_vidrala.md`).
   - Con R1, cada euro nuevo pide ~0,81 € fijos tras f, frente a 0,56 € en la historia. La mezcla histórica sigue lejos del 14,70 % de R1 con o sin la plusvalía.
6. **BUENO.** Con f rinde el 19,9 % por euro nuevo, más que cualquier ROIC anual de la Historia (máximo 16,2 %). G7 no lo ve. Lo sostienen la capacidad libre [ES, PDF p. 54 y p. 94] y Brasil [ES, PDF p. 107].
7. **«Otros» de 2025.** Son 43,1 mm sin explicar, 2,9 puntos del margen [ES, PDF p. 79]. Si no fueran recurrentes: ≈ −2,2 € de precio de Sí (cálculo mío). La zona no cambia.
8. **Lecturas de base parcial.** C27 = Expandiendo ya lo explicó la fase A. G7, las referencias mecánicas y el valor sin crecimiento (58,19 €) son lecturas de base parcial.
9. **Celdas de la fase C en el libro.** Las del libro de este expediente, como las de la rama, son las de la etapa 1: C104 trae un porcentaje de posición, que D16 no admite. Las reescribo en el turno 2.
10. **E4 (supuesto de la orquestación, no decisión).** Con C48 vacío, el libro no calcula C52, f, su semáforo ni «Precio ÷ FCF base», y el motor A no es calculable (V09). No rompe la historia:
    - el motor B lo eligió la fase A por el régimen de financiación, no por la calculabilidad (`fase_a.md` §13, punto 4);
    - las fases A y B miden ahora la caja con lo que sí está: C46 − C47 − C49 = 335,413 − 169,668 − 4,5 = 161,245 mm (E1), o 158,991 con la alternativa de C48 de 2,254 mm, y la caja al accionista de 2023–2025, 159,0 mm de media (Historia J35:L35);
    - E1 no cambia ninguna cifra que use la historia: 161,245 redondea a los 161,2 de la rama.

## 2. Desviaciones pendientes (G8)

`gramatica.md` deja dos saltos del año 11 sin justificar: NORMAL 0,056 y BUENO 0,079. Son las mismas cifras que en la rama (`resultados.json` → salto_anio_11: 0,0563 y 0,0787). La tesis del turno 2 los contará. Aquí los justifico con hechos.

- **NORMAL (convención).** En los años 1–10 cada euro nuevo rinde 0,9 × 1,1587 × 0,18 × (1 − 0,2205) = 14,6 %, junto al ROIC de cinco años (13,8 %, Historia C55). Desde el año 11 rinde el 9 %, la tasa del motor (8,69 %) redondeada.
  - Lo que se pierde es el exceso de retorno de poner capacidad nueva en un mercado que la empresa llama «estable, madura y razonablemente predecible» [ES, PDF p. 55], con competidores que solo nombra como «cinco principales» [ES_2024, PDF p. 128].
  - El margen del 18 % sigue sobre el capital instalado.
  - «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). La convergencia al coste de capital es un criterio, no una ley (MR; E2).
- **BUENO (fundamentada).** Cada euro nuevo rinde 1,1 × 1,1587 × 0,20 × (1 − 0,2205) = 19,9 %, porque llena hornos que no iban llenos: la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54].
  - Suma Brasil, con un 42,4 % de margen EBITDA [ES, PDF p. 107], y Toro [ES, PDF p. 85].
  - Agotada la capacidad libre, el capital nuevo rinde el 12 %, el suelo de la meseta de 2018–2025 (Historia E33, I33, J33), por debajo de 2 × C55 (27,7 %).
  - «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

## 3. ¿Hay que mover palancas?

No.
- La única palanca con un defecto de derivación es C15 (perímetro). Corregirla mueve el precio de Sí un 1,4 % sin cambiar cubo ni zona.
- Ni las correcciones de la rama ni E1–E4 tocan ninguna palanca. La reserva E2 afecta al apoyo de B16:D16 (C53 = 0,886, ≈ 0,978 con la plusvalía dentro), pero en el sentido de subir la referencia: el 0,9 queda del lado del menor valor (`fase_b.md`).
- La del MALO no tiene palanca que la exprese bajo R1. La de la rentabilidad marginal es de la configuración.

`revisar_palancas = false`. En `celdas_corregidas` dejo C15 y B16 con `despues = antes`.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** La alternativa de la etapa 1 (0,25/0,6/0,15) da un precio de Sí de 54,08 (−3,4 %), también en «caro». El otro ancla es la fase C de la rama, con el mismo precio de Sí (56,00201 €), que tienta a copiarla entera. Rehago lo que E1, E4 y las reservas E2/E3 tocan: lo que se apoyaba en C52, en f y en «Precio ÷ FCF base», y E2–E4 descritas como decisiones pendientes con el Δ frente a la 4.13.
2. **Anclaje en el precio.** Mis valores quedan muy por debajo de 90,10 y del 171,8 de Simply Wall St (C38, posterior a la base). El ancla a la baja (NORMAL al 18 %) la sostienen el ciclo y las bajadas de 2026 [ES, PDF p. 54].
3. **Consistencia y compromiso.** Para cumplir la regla a 90,10 haría falta subir los tres valores 34,1 €, un NORMAL del ~27 % que nunca se ha visto. Con la fase C de la rama, lo que más tentaba conservar era «FCF base positivo (161,2 mm, C52)» como prueba de que no hay límite del modelo; C52 no existe aquí y lo sustituyo por C46 − C47 − C49 y la fila 35. «People get to believing the plan because they created it» (AIWTK p.86; HIM).
4. **Historia bonita.** El margen de 2024–2025 es gas a la baja [ES, PDF p. 56]. En 2024 el EBITDA creció un 10,5 % con ventas comparables del +0,2 % [ES_2024, PDF p. 97 y p. 98]: es margen, no volumen. Brasil se compró [ES, PDF p. 36–37].
5. **Optimismo del BUENO.** Con f rinde el 19,9 % por euro nuevo y necesita capacidad libre que no puedo medir. Pesa 0,143 € por euro.
6. **Doble castigo.** No encuentro el mismo riesgo en dos sitios. S lo contaría dos veces, pero no es la activa.
7. **Disponibilidad.** Kristin, el apagón y la plusvalía de Italia en el circulante son vívidos. Sobre la plusvalía, la persona responsable decidió mantener K14 publicado, con reserva (E2). Su alternativa exploratoria (≈ 34,447), que no se adopta, da 56,05 €: +0,049 € frente a este expediente, +0,033 € frente a la activa 4.13. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).
8. **Autoridad.** El volumen +1 % es supuesto de la empresa [ES, PDF p. 54; CF_2019, PDF p. 44]. Lo contrastan el orgánico −5,4 % [ES, PDF p. 88] y las materias primas planas en 2024–2025 (3.162.770 y 3.162.197 t [ES_2024, PDF p. 214; ES, PDF p. 195]). Con volumen 0, ~−0,75 € de precio de Sí.
9. **¿El MALO es de verdad malo?** 44,32 €, un 50,8 % bajo el precio: margen del 15 % para siempre. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
10. **Lo no numerable.** Clientes del ~30 % (2019) al ~38 % (2024) y «algo más del 35 %» en 2025 [CF_2019, PDF p. 67; ES_2024, PDF p. 110; ES, PDF p. 104]. A eso se suman las coberturas de energía [ES, PDF p. 101], el CO2, los competidores sin nombre y el tipo medio de la deuda contradictorio [ES_2024, PDF p. 83; ES, PDF p. 75].

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Orden de mando:
- **Bloqueo:** ninguno; la gramática no tiene errores.
- **Límite del modelo:** no hay.
  - C52 no se calcula (E4) y el motor A no es calculable, pero el motor B lo eligió la fase A por la financiación.
  - La caja de la base es positiva con las dos medidas que sí tengo: C46 − C47 − C49 = 161,245 mm (158,991 con la alternativa de C48) y la caja al accionista de 2023–2025 (105,9, 187,6 y 183,5 mm, Historia J35:L35).
  - La empresa no es financiera y el motor B cuadra en las 19 variantes.
- **Descalificador mío:** ninguno.
- **Dato ausente material:** ninguno (punto 6).
- **Fundamento material:** la lista D10 está vacía (punto 7).
- **Zona:** caro.

Conclusión provisional: **esperar**, con el precio de Sí (56,00 €) como objetivo condicionado por la reposición de hornos y por el ROIC terminal (punto 9). «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM).

## 6. Datos ausentes (S-19)

Reviso uno a uno los 39 datos, los mismos que en la rama. Ninguno es material para esperar con objetivo: `alguno_material = false`. Lo que cambia y lo que conviene recordar:

- **C48 (intereses en financiación).** Ya no es un cero heredado: es dato ausente declarado por el supuesto E4 de la orquestación, no por una decisión. Ningún ejercicio de 2023–2025 publica la línea y ninguna nota dice dónde va el interés de arrendamientos (datos_v63.md §2, C48). Con 0 o con 2,254 mm el precio de Sí es 56,00201 € (0,000 €; solo motor A). El motor B no lo usa.
- **Intereses en financiación de la Historia (fila 16).** Solo afectan a la caja al accionista de la fila 35, que es contexto: con 2,254 mm al año en 2023–2025, su media bajaría de 159,0 a unos 156,7 mm (`fase_a.md` §13, punto 3). C52 no se calcula con o sin estos ceros.
- **Adquisiciones (fila 13).** Si los ceros de 2021–2022 escondieran 53 mm, el efecto sería ~−0,3 €.
- **«Otros efectos enajenación» (11,668 mm).** Quedan fuera de K13; incluirlos movería centésimas.
- **Covenants.** Los indicadores ya están (0,55x y 18,80x en 2024 [ES_2024, PDF p. 81–82]); faltan los umbrales. Con la deuda en 0,2x EBITDA [ES, PDF p. 93], no hay disparador.
- **Pensiones del Reino Unido.** La provisión es de 6,2 mm y los movimientos actuariales son pequeños [ES, PDF p. 70 y p. 77–78]. Cada 10 mm restarían 0,28 €.
- **Tipo medio de 2024, gas de 2024 e inversiones de 2023 por área.** Ninguna palanca los usa.
- **Múltiplos de las operaciones.** Vidroporto y Italia ~6,9 veces EBITDA [ES, PDF p. 36–38; ES_2024, PDF p. 112]; Toro ~6,4 [ES, PDF p. 85].
- **Capex por destino, capacidad, toneladas y taxonomía de 2025.** Informan una hipótesis sin fundamento suficiente que ya condiciona el objetivo. No son un dato que bloquee: sin ningún requisito, el precio de Sí sería 63,11 €.
- **«Otros» ingresos.** El peor caso es ≈ −2,2 €. Se repiten en 2024 y 2025 [ES, PDF p. 79; ES_2024, PDF p. 87]: «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM).

E2 y E3 no son datos ausentes: son reservas sobre cifras publicadas (K14 y la pareja A de 2023), una decidida y otra supuesta, que se tratan en los puntos 1 y 9.

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B, que no cambian ninguna celda frente a la rama (ni la rama frente a la 4.13): palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas.
- Todas son «fundamentada» o «convención» y citan hechos.
- C97 es «técnico», pero no es una hipótesis material del valor.
- Miré con lupa B69:D69 (−3,4 % con la alternativa), B16 (no actúa), D16 y C15 (+1,4 %).
- Frente a la rama, las fases A y B solo reescriben los apoyos que leían C52 y f: C13, C20, C25, C51, C62 y Palancas C43 en la A; C22:C23 y C44 en la B. Ahora miden con C46 − C47 − C49 = 161,245 mm y con la fila 35.
- Añaden la reserva E2/E3 al apoyo de B16:D16: C53 = 0,886 con K14 publicado, ≈ 0,978 si la plusvalía estuviera dentro. Eso subiría la referencia y el valor, así que el 0,9 queda del lado del menor valor. Ninguna pierde el fundamento.

La lista queda vacía. Con `esperar`, el resultado es `no_procede`, sin comprobación conjunta y con `sobrevive = null`. Los parámetros experimentales sin fundamento suficiente condicionan el objetivo, no van a D10.

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis fundamentada de la que más depende la conclusión, a mi juicio, es **Palancas!C15**: que el 18 % del NORMAL sea la media de un ciclo de energía que vuelve. «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

Lo resolverían:
- el precio medio y el coste de energía por tonelada y segmento de 2019–2025;
- las cláusulas de traslado;
- el desglose de los 43,1 mm de «Otros» [ES, PDF p. 79].

## 9. Configuración V6.4 experimental

**Variantes.** Las 19 calculadas dan «caro», con un precio de Sí de 51,26 a 65,72 € (activa 56,00; amplitud 14,46 €). Son las mismas que en la rama. Es una tabla de sensibilidad, no un intervalo de confianza. `zona_igual_en_variantes_calculadas = true` solo para esa tabla.

**Criterio para el objetivo (contrato 4.14).** El juicio sobre el objetivo es distinto del de la acción. Para separar lo material uso un criterio propio, que **es juicio mío y no una política** (`juicio_propio_del_agente`; no hay ninguna adoptada y D1 está pendiente): **1,58 € de precio de Sí** (2,8 %).
- Es lo que mueve un punto de margen NORMAL: tornado 7,36 € por 2 puntos × 0,4286.
- Es la incertidumbre que ya acepto en C15, la palanca fundamentada de la que más depende el objetivo (perímetro +0,5 puntos; «Otros» −1 punto).
- Con él, la base es siempre `juicio_economico`, nunca `calculada`.
- Para un parámetro sin fundamento que juzgue no material, declaro con qué lo comparo. Si no puedo, la base es `no_determinada` y condiciona el objetivo.
- Copio el contraste de `contraste_objetivo_v64.json` (el mismo de `contraste_objetivo_v64.md`) tal cual en cada `juicio_objetivo`. Es idéntico al de la rama.

**Parámetros** (cobertura · base para la acción / para el objetivo · contraste atribuible del precio de Sí):

| Parámetro | Cobertura | Acción | Objetivo | Contraste atribuible | ¿Fundamento? | ¿Condiciona? |
|---|---|---|---|---|---|---|
| N1.tipo | conjunta necesaria | no (calculada) | **material** (juicio) | +1,75 | sí | no |
| N1.escudo | aislado | no (calculada) | no (juicio) | −0,08 | sí | no |
| N2.margen | aislado | no (calculada) | no (juicio) | −0,94 | sí | no |
| N3.regla | conjunta necesaria | no (calculada) | no (juicio) | +7,98, de los que 6,62 son quitar P-M1; R1 frente a R0: 1,36 | sí | no |
| N3.circulante | conjunta | no (juicio) | no (juicio) | sin contraste atribuible; cálculo mío < 0,01 | sí | no |
| PM1.estructura | aislado | no (calculada) | **material** (juicio) | −0,48 a +7,11 | no | **sí** |
| PM1.familia | conjunta | no (juicio) | **material** (juicio) | sin contraste atribuible; cota +7,11 | no | **sí** |
| PM1.parametro | aislado | no (calculada) | **material** (juicio) | +2,37 / −4,74 | no | **sí** |
| PM1.convencion_anios | aislado | no (calculada) | no (juicio) | −0,13 | sí | no |
| PM1.convencion_terminal | aislado | no (calculada) | no (juicio) | +0,40 | sí | no |
| PM1.roic_terminal | conjunta necesaria | no (calculada) | **no determinada** | +1,02 a λ 1,15 | no | **sí** |
| PM1.cartera | aislado | no (calculada) | no (juicio) | −0,55 | sí | no |

Lo que pide explicación:

- **N1.tipo.** +1,75 supera el criterio, así que es material para el objetivo. No lo condiciona porque tiene fundamento: el tipo de 2023–2025 (22,05 %) es el del perímetro actual, y la alternativa (C52 de la Historia, 20,03 %, con 2021–2022 e Italia) es la menos defendible y la favorable.
- **N3.regla.** El contraste atribuible mueve +7,98 €, pero 6,62 de ellos son quitar P-M1 (activa_sin_PM1). R0 frente a R1 es +1,36 €, bajo el criterio, y R0 está fuera del dominio (aviso inversion_fija_para_crecer_negativa). El límite: R0 con P-M1 no está especificado y la descomposición supone que no hay interacción. Discrepa de la «hipótesis» de la configuración; resuelto en el JSON sin decidir D-N3.
- **PM1.familia.** Θ no se calcula. θ = 0 coincide con no tener requisito (+7,11). θ = 1 trata como reposición los 229,4 mm de exceso, más del triple del Rh de λ 1,15 (75,0), y llevaría el objetivo por debajo de 51,26. Es material por juicio, sin contraste atribuible.
- **PM1.roic_terminal.** A λ 1,15 mueve +1,02 €, bajo el criterio. Su efecto entra por ROIC × f, y f − 1 va de 0,159 (activa) a 0,296 (λ 1,25). Mi aproximación lineal lo lleva a ~1,9 €, por encima del criterio, pero no está calculado. λ es otra hipótesis sin fundamento, así que no puedo declarar con qué comparación queda acotado en su ámbito. Lo dejo **no determinado**: condiciona el objetivo. Q-ROIC1 sigue abierta. Discrepa de la confianza media de la configuración; la resuelvo en el JSON.
- **Entradas: decisiones y supuestos** (`DECISIONES_ENTRADAS_4_14.md`; `efecto_correcciones_vidrala.md`). Las alternativas se miden frente a este expediente (56,00201 €):
  - **E1** (decisión): medias exactas de C46–C47; los redondeos darían 0,000 €.
  - **E2** (decisión, con reserva): K14 = 84,994 publicado. La alternativa exploratoria ≈ 34,447, no adoptada, da +0,049 € (+0,033 € frente a la activa 4.13, la cifra del registro).
  - **E3** (supuesto de la orquestación): pareja A de 2023; la pareja B da +0,010 € (−0,006 € frente a la 4.13).
  - **E4** (supuesto de la orquestación): C48 dato ausente; con 2,254 mm, 0,000 €.

  Ninguna es material con el criterio declarado ni condiciona el objetivo. Anoto E2 y E3 como límites de PM1.estructura y PM1.parametro, porque mueven D_hist y f y solo están medidas en la activa.

**Mantenimiento.** *¿La reposición supera la amortización?* En dirección, sí; en magnitud, no lo sé.
- El capex supera la amortización todos los años desde 2017 (1,15 a 1,74 veces). En 2021–2025 fueron 739,0 frente a 509,6 mm.
- El exceso aparece también en los años sin crecimiento: 50,1 mm en 2020 y 55,6 en 2025. En 2025, la renovación de hornos fue el destino principal [ES, PDF p. 50] y el consumo de materias primas fue plano [ES_2024, PDF p. 214; ES, PDF p. 195].
- Siguen en uso 627 mm de activos totalmente amortizados [ES, PDF p. 51] y los hornos duran hasta 15 años [ES, PDF p. 168].
- En contra de atribuirlo todo a la reposición: el calendario de hornos [ES, PDF p. 180], la descarbonización [ES, PDF p. 173], Brasil y el 8 % de 2019 [CF_2019, PDF p. 44]. λ = 1,15 atribuye 75,0 de los 229,4 mm de exceso.

*¿Qué estructura?* No hay base para nombrar una.
- **S** es la menos coherente.
- **H** no queda excluida: la distinguirían los años con crecimiento y saber si reconstruir un horno añade capacidad.
- **SR1 frente a SRF** depende de la mezcla: la histórica fue un 50,9 % circulante (45,9 % si la plusvalía de Italia estuviera dentro de K14); la futura, 13–15 %.
- **SR1 frente a SR2** es Q-ROIC1.

`estructura_mas_coherente = null`, `adoptada = false`. «When you don't know and you don't have any special competence, don't be afraid to say so» (PCA p.272; HIM).

**Avisos de dominio.** Ninguno es material.
- f = 1,1587 en la activa (el factor de reestimación del S2C, no las fugas al accionista) deja de estar definida en λ = 2,09. Explica G8 y condiciona el objetivo a través de λ, la estructura y el ROIC terminal, que ya son condicionantes. Con λ ≈ 1,46, f sería ≈ 1,72 y el S2C NORMAL reestimado ≈ 1,55: perdería sentido.
- El terminal de R1 y s2c_inerte se compensan (~1 € cada uno).
- inversion_fija_para_crecer_negativa solo aparece con R0, en el extremo superior del rango, el menos creíble.
- Las lecturas de base parcial no comprueban el modelo experimental.

**Objetivo.** Protocolo `objetivo_condicionado`.
- Condicionan el objetivo PM1.estructura, PM1.familia, PM1.parametro y PM1.roic_terminal.
- La acción se sostiene en las 19 variantes y ningún condicionante es material para la acción.
- Tratamiento: **objetivo_condicionado**, con 56,00 € como objetivo condicionado (provisional).

Este tratamiento sale del protocolo declarado en `configuracion_economica.json`. No es una delimitación de P-M1: esa es la decisión D2, pendiente, y para Vidrala su propuesta es abstenerse del objetivo. Las decisiones E1 y E2 son de entradas y no adoptan ninguna configuración ni criterio. Con dinero real, el objetivo no es una cifra firme. «Better roughly right than precisely wrong» (PCA p.451; HIM).

# Fase C · turno 2 · conclusión, celdas y predicciones

El turno 1 queda arriba sin cambios y en `fase_c.turno1.json`. No reabro sus juicios. En particular, conservo tal cual los parámetros de `configuracion_v64` con su `juicio_objetivo` y el bloque `objetivo`, porque la conclusión no cambió. Parto del turno 2 de la rama (en `fase_c.rama.json` y `fase_c.rama.md`) y cambio lo que E1 y E4 invalidan: lo que se apoyaba en el FCF base (C52), que este libro no calcula, y la fecha de análisis (Análisis D4 = 2026-11-14 aquí, 2026-11-12 en la rama).

## 10. Comprobación conjunta

No existe `comprobacion_conjunta.json`. La lista D10 está vacía y la conclusión provisional es `esperar`, así que la comprobación no procedía.
- `sobrevive` queda en `null`.
- `fundamento_material.resultado` sigue en `no_procede`.
- No hay escalera bajo ninguna combinación que informar.

## 11. Conclusión: concluido (provisional hasta la auditoría) · Vigilar · esperar

Orden de mando (sección 15), sin cambios desde el turno 1:
- sin bloqueo ni límite del modelo;
- ningún descalificador;
- ningún dato ausente material (`alguno_material = false`);
- lista D10 vacía;
- zona **caro**: 90,10 € frente a un ponderado de 60,67 €.

La conclusión sale así:
- **Acción:** `esperar`.
- **Precio objetivo:** 56,00 €, el `precio_si` de `precio.json` (56,002005…) redondeado a dos decimales.
- **Tratamiento** (protocolo `objetivo_condicionado`): `objetivo_condicionado`. Es un objetivo **condicionado y provisional**.
  - Lo condicionan PM1.estructura, PM1.familia, PM1.parametro y PM1.roic_terminal. Ninguno tiene fundamento suficiente.
  - La acción se sostiene en las 19 variantes calculadas, que dan todas «caro».
- **Rango del precio de Sí:** de 51,26 € (λ 1,25) a 65,72 € (solo_N2). Es una tabla de sensibilidad, no un intervalo de confianza. Tampoco prueba robustez frente a hipótesis que no se exploraron.
- **Etiqueta de C104** (tabla cerrada del Anexo D §D.6): «fundamento no procede (conclusión no favorable)».
- **Entradas.** E1 (medias exactas de C46–C47) y E2 (K14 = 84,994 publicado, con reserva sobre la plusvalía de Italia) son decisiones de la persona responsable. E3 (pareja A de 2023, con reserva) y E4 (C48 dato ausente) son supuestos de la orquestación, no decisiones. Frente a este expediente (56,00201 €):
  - la alternativa de E2 (K14 ≈ 34,447) da 56,05107 €: +0,049 €;
  - la pareja B de E3 da 56,01192 €: +0,010 €;
  - E1 con los redondeos y E4 con C48 = 2,254 mm: 0,000 €.

  Son los casos «con todas las correcciones» de `resultados/efecto_correcciones_vidrala.md`. Los +0,033 y −0,006 € del registro de decisiones se miden frente a la activa 4.13. Ninguna llega al criterio de 1,58 € ni cambia la zona.

La hoja dice en B258: «DESCARTADA POR FILTRO PABRAI», por C13 = No. Mi cubo es Vigilar porque C13 mide el precio, no el negocio. «An orangutan could figure out that the stock is selling miles above the value» (DR pp.220–221; HIM).

**Insumos para la decisión de cartera.** El tamaño de la posición lo decide José Luis (D16).

| Insumo | Valor |
|---|---|
| Precio | 90,10 € |
| Precio de Sí | 56,00 € (37,84 % por debajo del precio, sobre el precio; el precio queda un 60,89 % por encima, sobre el precio de Sí) |
| Precio del escenario MALO | 44,32 € (50,81 % por debajo del precio) |
| Ponderado | 60,67 € |
| r y r mínima | 0,09 y 0,0817 |
| Datos ausentes materiales | ninguno |

Descalificadores que miré:
- **Macro** (energía y divisa): es el más cercano. No aplica porque la Historia trae el ciclo completo: 13,7 % de margen en 2022 y 20,8 % en 2024 (I29, K29). Una depreciación del 5 % de la libra o del real resta un 1,5 % o un 0,8 % al beneficio [ES, PDF p. 103].
- **Deuda:** 0,36x EBITDA (C33), con 258 mm disponibles [ES, PDF p. 75 y p. 105].
- **Capex de hornos:** fue 1,42 veces la amortización en 2025 (Historia L12, L8). El FCF base (C52) no se calcula aquí (E4), pero la caja de la base es positiva con lo que sí está: C46 − C47 − C49 = 335,413 − 169,668 − 4,5 = 161,245 mm (datos_v63.md §2), y la caja al accionista fue de 105,9, 187,6 y 183,5 mm en 2023–2025 (Historia J35:L35).
- **Cambio tecnológico:** la electrificación es capex y coste [ES, PDF p. 173], no sustitución.

La palanca más influyente del tornado es el ROIC de largo plazo. Es información, no criterio.

## 12. Tesis (B101)

Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil. Ningún cliente supera el 10 % de las ventas [ES, PDF p. 104]. Lleva diez años con un ROIC por encima del sector: 13,8 % de media en cinco años frente al 9,3 % (Historia C55, Palancas H18).

Leo que gana por fabricar cerca del cliente y trasladar la energía al precio con retraso. El margen operativo cayó al 13,7 % en 2022 y volvió al 20,8 % en 2024 (I29, K29). Pero el 19,9 % de 2025 está junto al máximo, y tres cosas lo hacen frágil:
- el gas va a la baja;
- hay 43,1 mm de «Otros» sin explicar [ES, PDF p. 79];
- la empresa supone bajadas de precio en 2026 [ES, PDF p. 54].

Mi NORMAL deja el margen en la media del ciclo, el 18 %. En los años 1–10 cada euro nuevo rinde el 14,6 %; desde el año 11, el 9 %, apenas sobre la tasa del motor (8,69 %). Este es el salto G8 que justifiqué en el punto 2. Por eso crecer aporta poco.

A 90,10 € pago más que mi escenario BUENO (78,48 €). Ese precio descuenta un crecimiento de ventas del 14,3 % anual durante cinco años; mi NORMAL (60,19 €) crece un 1,5 %.

Vigilar: espero hasta 56,00 €. Es un objetivo condicionado a la reposición de hornos y al ROIC del terminal.

## 13. Tesis inversa (B102): el No, defendido mejor que un bajista

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

- **Producto y mercado.** Es un producto poco diferenciado en un mercado que la propia empresa llama maduro [ES, PDF p. 55]. El consumo fue inferior a lo previsto y la capacidad se adapta a él [ES, PDF p. 94]. Las ventas orgánicas cayeron un 5,4 % en 2025 [ES, PDF p. 88] y las materias primas consumidas fueron planas en 2024–2025 [ES_2024, PDF p. 214; ES, PDF p. 195].
- **Margen.** El 19,9 % de 2025 es energía barata camino del cliente. La empresa supone bajadas de precio en 2026 [ES, PDF p. 54] y un gas que pasa de 39,9 a 23,3 €/MWh en 2029 [ES, PDF p. 56]. Además, 2,9 puntos son «Otros» sin explicar [ES, PDF p. 79].
- **Hornos.** El capex supera a la amortización todos los años desde 2017: 1,42 veces en 2025, con ventas a la baja (Historia L12, L8). Siguen en uso 627 mm de activos ya amortizados [ES, PDF p. 51] y la descarbonización empieza en 2026 [ES, PDF p. 72 y p. 173]. Mi modelo carga como reposición 75,0 de los 229,4 mm de exceso.
- **Clientes.** Los diez mayores pasaron del ~30 % de las ventas en 2019 al ~38 % en 2024. En 2025 son algo más del 35 % [CF_2019, PDF p. 67; ES_2024, PDF p. 110; ES, PDF p. 104].
- **Brasil y Chile.** El real se devaluó un 20 % en 2024 [ES, PDF p. 106] y la deuda brasileña paga a CDI [ES, PDF p. 105]. La compra de Chile está condicionada a un plan de ajuste [ES, PDF p. 85].
- **Foso.** El ROIC fue la tasa en 2016–2017 (9,4 %, Historia C33:D33). La empresa solo habla de sus «cinco principales competidores», sin nombres [ES_2024, PDF p. 128].

## 14. Predicciones (Palancas A38:C40)

Las tres vencen el 2028-04-30, a unos 17,5 meses de D4 (2026-11-14). Las cuentas se aprueban en abril [ES, PDF p. 70]. La probabilidad de cada una es la de que se cumpla dado el NORMAL.

| | Predicción | Probabilidad | Base |
|---|---|---|---|
| 1 | El margen operativo de 2027 queda entre el 16 % y el 20 % | 0,7 | 5 de los 7 años de 2019–2025 cayeron en esa banda (F29:L29) |
| 2 | La variación orgánica de las ventas de 2027 queda entre −2 % y +4 % | 0,65 | La energía ha movido mucho las ventas (fila 28: −7,8 % en 2025 y +24,1 % en 2022) |
| 3 | Los pagos por inmovilizado de 2027 superan 1,2 veces la amortización | 0,7 | 6 de los 9 años de 2017–2025 lo cumplieron (filas 8 y 12) |

## 15. Lo que más condiciona (B222) y qué lo resolvería (B223)

Con la lista D10 vacía, lo que más condiciona la conclusión, a mi juicio, es **Palancas!C15**: que el margen del 18 % sea la media de un ciclo que vuelve. El objetivo lo condicionan además la reposición de hornos y el ROIC del terminal.

Lo resolverían, preguntando a Relación con Inversores:
- precio y coste de energía por tonelada y segmento;
- cláusulas de traslado de la energía;
- desglose de los «Otros»;
- capex por destino;
- coste de reconstruir un horno y toneladas que añade cada reconstrucción.

Queda además Q-ROIC1, abierta: cómo se mide el ROIC de largo plazo.

## 16. Qué cambiaría el cubo

- **A Sí.**
  - Un precio por debajo de 56,00 € sin que cambie el negocio.
  - El umbral subiría con un capex desglosado: λ 1,10 lo lleva a 58,37 € y la estructura H a 61,37 €.
  - También con un margen de 2026–2027 del 18 % o más con energía normal.
  - Ninguno de esos hechos, por sí solo, lo lleva a 90,10 €.
- **A No.**
  - Un margen por debajo del 14 % sin choque de energía.
  - Dos años más de capex por encima de 1,4 veces la amortización con ventas planas.
  - Pérdida de cuota.
  - Los diez mayores clientes por encima del 40 % con el margen a la baja.
- **A Demasiado difícil.**
  - Que el valor dependa sobre todo de Brasil y Chile.
  - Exceso de capacidad duradero en el sector.
  - Una sustitución del vidrio que no sepa juzgar.

## 17. Comparación con la etapa 1

Las dos etapas llegan al mismo cubo, Vigilar, por la misma razón: buen negocio, cíclico, sin margen de seguridad al precio. «Missing out on some opportunity never bothers us» (TCI p.57; HIM).

Lo que cambia es el precio de Sí: de ~48 € a 56,00 €. Hay tres causas, y ninguna es una opinión nueva sobre la empresa:
- **La regla.** La etapa 1 tomaba el menor entre el MALO (≈ 48 €) y ¾ del ponderado (≈ 57 €) (`etapa1/Vidrala_respuesta.md`). La escalera k = 3 queda por encima del MALO (44,32 €).
- **El modelo.** El motor B trabaja con palancas en lugar del crecimiento del FCF base de 161 mm de la etapa 1. En este libro C52 ni siquiera se calcula (E4).
- **La configuración experimental.** Resta 8,75 € frente al modo heredado (64,75 €, variante «heredado» de `configuracion_v64_variantes.md`).

Mi NORMAL (60,19 €) queda por debajo del valor normal de la etapa 1 (~74 €).

La etapa 1 usaba hechos posteriores a la base: Chile desde el 30-mar-2026, la deuda a 30-jun-2026 y 88,7 €. Yo no los uso.

## 18. Checklist de la fase C (sección 17)

- Una sola historia, coherente con la hoja (punto 1).
- Autocomprobación con contenido (punto 4).
- Los 39 datos ausentes revisados (punto 6).
- Lista D10 completa y vacía; comprobación conjunta: no procede.
- Estado, cubo y acción según la sección 15 y la tabla del objetivo (§D.13).
- C104 sin porcentaje y con la etiqueta de fundamento de la tabla cerrada.
- Tres predicciones sobre el negocio, falsables, con fecha y probabilidad.
- Tesis inversa con hechos.
- B222 y B223 concretos.
- Comparación honesta con la etapa 1 y qué cambiaría el cubo.
- Citas con libro y página. Los hechos llevan su celda o página; lo demás va como juicio, con «leo» o «cálculo mío».
