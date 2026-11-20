- fase_c.una_sola_historia.incoherencias[0]: Minoritarios (resuelta en parte): tras la vuelta, B15:D15 restan el exceso del valor de los minoritarios de Gatwick, Edimburgo y OMA sobre su valor contable (−0,008 / −0,008 / −0,007). Ese exceso es 805 ÷ (r − g) − 3.576, unos 6,5 / 7,9 / 8,8 mil M. Lo que queda abierto es la base: 805 son dividendos, no resultado, y el valor contable de los minoritarios baja de 4.085 a 3.576 mientras cobran 805 (URD 2025 PDF p. 358, 399). Eso sugiere que los dividendos superan su resultado, y entonces el recorte sería menor. Con medio recorte (0,09 / 0,095 / 0,10) el precio de Sí sería ≈104,9 € y la zona `vigilar`; sin recorte, 113,3 € y `cumple_regla_k` [cálculo, réplica que reproduce B78:D78]. La acción `esperar` solo cambia si el exceso baja de ≈3,45 mil M; el precio objetivo, en cambio, depende de esta hipótesis. No admite otra vuelta a la fase B: marca el objetivo como provisional.
- fase_c.una_sola_historia.incoherencias[1]: Vara de la reinversión (sigue): el MALO rinde 7,5 % en los años 1–10, por debajo de r (9 %) pero por encima de la tasa del motor (6,41 %, Diagnóstico V6!C15). En la hoja, su reinversión crea algo de valor en esos años, al revés de su historia; solo su terminal (6 % < 6,41 %) destruye valor. No es una palanca mal derivada: la tasa es convención de la plantilla y r es heredada. Pero el MALO es más suave que sus palabras: con S2C 1,0 bajaría a ≈75,1 € y el precio de Sí a ≈95,7 € [cálculo], sin cambiar la acción.
- fase_c.una_sola_historia.incoherencias[2]: Lectura «cuánto pagas por crecer»: el valor sin crecimiento (103,58 €) aplica para siempre el margen de partida (10,69 %), con las autopistas dentro y sin restar a los minoritarios. Queda por encima del NORMAL (101,75 €). El «⚠ pagas por un crecimiento que no añade valor» de la hoja compara con una base que no cuenta la historia del expediente: no es un suelo.
- fase_c.una_sola_historia.incoherencias[3]: Zona en el filo: el ponderado (107,04) queda a un céntimo del precio (107,05), así que la frontera entre `caro` y `vigilar` la decide el redondeo. Las dos zonas llevan a la misma acción (`esperar`): no leo nada en la etiqueta.
- fase_c.lo_que_dice_la_hoja.valores.zona: caro
- fase_c.lo_que_dice_la_hoja.cambios_tras_la_vuelta: B15:D15 0,095 / 0,10 / 0,105 → 0,085 / 0,09 / 0,10 (minoritarios) y C16 1,7 → 1,5 (mezcla de la reinversión). Valores 93,87 / 122,34 / 186,10 → 79,28 / 101,75 / 174,47 €; precio de Sí 114,48 → 97,79 €; zona cumple_regla_k → caro.
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[0]: filas 40–44 (crecimiento, margen, ROIC marginal frente a su historia, ROIC a largo plazo, peso del para siempre): ✓ PASA en los tres escenarios; fila 47 (orden de los escenarios): ✓ PASA
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[1]: fila 45, cuota implícita: «—» (sin C24)
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[2]: fila 48: ⚠ REVISAR · r 9,0 % < r mínima 9,08 % (r heredada; se informa, no se toca)
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[3]: V11 AVISO Regulada: el modelo no recoge el marco regulatorio ni la base de activos; V16 AVISO salto del año 11 > 5 puntos (BUENO)
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[4]: cuánto pagas por crecer: ⚠ REVISAR (valor del crecimiento del NORMAL −1,83 €): ver incoherencias
- fase_c.lo_que_dice_la_hoja.semaforos_relevantes[5]: estado técnico INCOMPLETO solo por las tres predicciones (turno 2); lectura del precio B267 «sin margen: tu DCF no da colchón»; veredicto de la hoja «DESCARTADA POR FILTRO PABRAI» (C13 = No): no es mi decisión
- fase_c.lo_que_dice_la_hoja.salto_anio_11.explicacion: La rentabilidad marginal de los años 1–10 (S2C × margen × (1 − t)) es 7,5 % / 9,2 % / 15,6 %, frente a un ROIC terminal de 6 % / 7 % / 10 %. En MALO y NORMAL la transición es suave: el NORMAL ya reinvierte en torno a r y en el año 11 baja al retorno del sector. En el BUENO, el salto de 5,6 puntos es la pérdida de la ventaja de Energy Solutions y de las tarifas aprobadas (G8). El terminal del MALO (6 %) queda por debajo de la tasa del motor: su crecimiento perpetuo destruye valor, como dice su historia.
- fase_c.lo_que_dice_la_hoja.dcf_inverso: Con las demás palancas del NORMAL, 107,05 € descuentan un crecimiento de ventas del ≈5,4 % al año en los años 1–5 (C86 = 0,0535). El NORMAL pone el 4 % (2,5 % orgánico + 1,5 % de compras) y el orgánico de 2025 fue del 2,6 % (URD 2025 PDF p. 130). El precio pide algo más que el NORMAL. El precio de Sí equivale a ≈2,9 % (g implícito de precio.json).
- fase_c.lo_que_dice_la_hoja.palanca_mas_influyente: Tasa de descuento (±1 pt)
- fase_c.lo_que_dice_la_hoja.tornado: ±1 punto de tasa mueve ±45,5 € (45 %); ±2 puntos de margen, ±35,1 €; ±5 puntos de ROIC terminal, ±17,0 €; ±2 puntos de crecimiento, ±8,0 €; ±0,3 de S2C, ±6,5 €; ±0,5 puntos de g, ±2,7 €. El valor depende sobre todo de la rentabilidad exigida (r heredada) y del margen equivalente, que ahora lleva dentro el recorte por minoritarios.
- fase_c.lo_que_dice_la_hoja.comprobacion_del_escalon: Mi réplica del motor B reproduce los nuevos B78:D78 al céntimo (79,28 / 101,75 / 174,47). El escalón de las autopistas no cambia en esta vuelta. Antes del recorte, el equivalente seguía coherente con la suma de partes: 0,093–0,095 / 0,100–0,102 / 0,107–0,108 [cálculo]. Cada −0,001 de margen resta ≈811 / 975 / 1.293 M, igual que antes, porque el efecto del margen no depende del S2C.
- fase_c.lo_que_dice_la_hoja.sensibilidad_minoritarios: Precio de Sí según el recorte por minoritarios, con el resto de palancas igual y C16 = 1,5 [cálculo]: recorte entero (libro) 97,79 € (`caro`); medio recorte (0,09 / 0,095 / 0,10) 104,94 € (`vigilar`); solo NORMAL a 0,095, 101,29 € (`vigilar`); sin recorte (0,095 / 0,10 / 0,105) 113,26 € (`cumple_regla_k`). Un exceso de ≈3,45 mil M sobre los 3.576 contables es la frontera de la acción.
- fase_c.lo_que_dice_la_hoja.distancias: El precio está un 9,5 % por encima del precio de Sí (9,26 ÷ 97,79, con el precio de Sí como denominador). El precio de Sí está un 8,7 % por debajo del precio (9,26 ÷ 107,05, con el precio como denominador). El precio está un 35,0 % por encima del precio del escenario MALO (27,77 ÷ 79,28).
- fase_c.lo_que_dice_la_hoja.nota: el tornado es información, no criterio
- fase_c.desviaciones_justificadas[0].comprobacion: G8
- fase_c.desviaciones_justificadas[0].escenario: BUENO
- fase_c.desviaciones_justificadas[0].justificacion: En los años 1–10 del BUENO el capital nuevo rinde 15,6 % después de impuestos (2,3 × 0,10 × (1 − 0,32)) porque el crecimiento lo llevan Energy Solutions, que vende 29,6 mil M con 9,5 mil M de capital (≈16 % después de impuestos), y subidas de tarifa aprobadas sobre activos ya construidos (OMA, inflación + 6,9 % en 2026–2030; segunda pista de Gatwick). En el año 11 esa ventaja se pierde: sin foso (C18 = No), la competencia en servicios y el precio de mercado de las concesiones nuevas llevan el retorno a r + 1 punto (10 %), que solo sostienen los aeropuertos en plena propiedad y las concesiones largas. El salto de 5,6 puntos es esa hipótesis de duración (diez años, no para siempre) y va en la tesis.
- fase_c.desviaciones_justificadas[0].hechos[0]: Energy Solutions: Ebit 2.250 (7,6 %) sobre ventas 29.612 (URD 2025 PDF p. 134, 136) y capital empleado 9,5 mil M (PDF p. 141)
- fase_c.desviaciones_justificadas[0].hechos[1]: OMA: tarifas «reference inflation rate plus 6.9%» 2026–2030; Gatwick: segunda pista aprobada, hasta 80 M de pasajeros (URD 2025 PDF p. 132)
- fase_c.desviaciones_justificadas[0].hechos[2]: Airports: Ebit 2.459 sobre 24,1 mil M de capital empleado (≈6,9 % después de impuestos) (URD 2025 PDF p. 136, 141); Gatwick y Edimburgo en plena propiedad; concesiones aeroportuarias hasta 2045–2062 (PDF p. 382)
- fase_c.desviaciones_justificadas[0].hechos[3]: Análisis!C18 = No; salto del año 11 BUENO 0,0563 (Diagnóstico V6, bloque 10): 0,1563 frente a 0,10
- fase_c.desviaciones_justificadas[0].clase: fundamentada
- fase_c.autocomprobacion[0].sesgo: anclaje en la etapa 1
- fase_c.autocomprobacion[0].hallazgo: Tras la vuelta, el MALO y la regla antigua valen 79,28 €, casi el «≈79 €» de la etapa 1. Comprobé que no viene de ahí: el MALO sale del equivalente de 0,093–0,094 menos 0,008 de minoritarios (805 ÷ (0,09 − 0,01) − 3.576) y del S2C 1,3, todos con hechos de este expediente. La etapa 1 llamaba a ese 79 € precio de Sí; aquí es el MALO, que no es un suelo (D11).
- fase_c.autocomprobacion[0].cambio: ninguno en palancas; en el turno 2 B101, B102 y C104 se reescriben sin el 79 € heredado ni su porcentaje
- fase_c.autocomprobacion[1].sesgo: anclaje en el precio o en la fuente externa
- fase_c.autocomprobacion[1].hallazgo: El ponderado (107,04) queda a un céntimo del precio (107,05). Miré si la fase B eligió las cifras por su efecto: el recorte sale de 805 ÷ (r − g) − 3.576 con la g de cada escenario, y el NORMAL de 0,090–0,093 se redondea a 0,09, que es el múltiplo de 0,005 más cercano a su centro. Con 0,095 el ponderado sería 112,3 y la acción la misma. El Fair Value ajeno (111,79) no entra en nada.
- fase_c.autocomprobacion[1].cambio: ninguno; no leo nada en «caro» frente a «vigilar»: las dos zonas dan la misma acción
- fase_c.autocomprobacion[2].sesgo: consistencia y compromiso
- fase_c.autocomprobacion[2].hallazgo: Pedí la vuelta a la fase B y ahora la zona confirma mi Vigilar de la fase A. Revisé si empujé hacia ahí: el recorte por minoritarios sale de hechos (805–902 de dividendos y 3.576 de valor contable) y el de C16 de la mezcla de compras y crecimiento propio. La parte dudosa del recorte la reconozco: si los dividendos superan el resultado de los minoritarios, el precio de Sí sube hasta ≈105 € [cálculo].
- fase_c.autocomprobacion[2].cambio: marco el precio objetivo como provisional, condicionado a los minoritarios, en lugar de darlo por firme
- fase_c.autocomprobacion[3].sesgo: historia bonita / viento de cola atribuido a la empresa
- fase_c.autocomprobacion[3].hallazgo: El BUENO (15,6 % de rentabilidad marginal) lo llevan Energy Solutions con poco capital (2.250 de Ebit sobre 9,5 mil M, URD 2025 PDF p. 136, 141) y las tarifas aprobadas: electrificación y centros de datos son viento del sector (C17 = Sí), no foso (C18 = No). El NORMAL ya no lo lleva: rinde 9,2 % y su crecimiento vale −1,8 € por acción.
- fase_c.autocomprobacion[3].cambio: lo digo en G8: esa ventaja se pierde en el año 11; ninguna palanca cambia
- fase_c.autocomprobacion[4].sesgo: optimismo del BUENO frente a la tasa base
- fase_c.autocomprobacion[4].hallazgo: El BUENO necesita el resto del grupo al 10 % de margen (8,5 % en 2024 y 8,9 % en 2025 sin Autoroutes [cálculo, URD 2025 PDF p. 134, 136]) y un ROIC terminal del 10 % frente al 6,9 % que rinde hoy Airports; vale 174,47 € (+63 %). Tiene probabilidad 0,15, menor que el MALO, y es el único escenario por encima del precio.
- fase_c.autocomprobacion[4].cambio: ninguno: queda bajo el máximo histórico del grupo (C51) y su peso es pequeño; lo dejo escrito como el supuesto más optimista
- fase_c.autocomprobacion[5].sesgo: doble castigo del mismo riesgo
- fase_c.autocomprobacion[5].hallazgo: Tras la vuelta, el NORMAL baja por dos cosas: los minoritarios (un derecho de terceros sobre los flujos) y el S2C (el retorno del capital nuevo). Son mecanismos distintos. El MALO lleva el mismo mecanismo en margen, S2C, ROIC terminal, g y p(MALO) = 0,25, sin quiebra (0) y con r heredada (PA; E6). El recorte por minoritarios no se repite en ninguna otra celda.
- fase_c.autocomprobacion[5].cambio: ninguno: no veo el mismo riesgo contado dos veces
- fase_c.autocomprobacion[6].sesgo: disponibilidad (lo vívido del extracto)
- fase_c.autocomprobacion[6].hallazgo: Los datos vívidos del semestre (tráfico −2,9 %, Construcción al 2,2 %; semestral PDF p. 7, 10) y la pista de Gatwick orientan MALO y BUENO. La Historia de diez filas muestra un margen de 10,8 % a 12,6 % con un solo bache (2020: 5,7 %; 2021: 9,0 %); los márgenes equivalentes 0,085–0,10 llevan dentro el escalón y los minoritarios, no un deterioro del negocio.
- fase_c.autocomprobacion[6].cambio: ninguno: lo vívido no lleva ninguna palanca más allá de la Historia
- fase_c.autocomprobacion[7].sesgo: autoridad (guía de la dirección como hecho)
- fase_c.autocomprobacion[7].hallazgo: El 7 % de Energy Solutions del BUENO coincide con la guía de «un dígito medio-alto» (URD 2025 PDF p. 144), pero se apoya en lo real (+6,8 % en el semestre y cartera de 69,8 a 76,8 mil M; semestral PDF p. 9, 16). La guía de 6 mil M de FCF y la de ventas no entran en ninguna palanca.
- fase_c.autocomprobacion[7].cambio: ninguno: ninguna palanca copia la guía
- fase_c.autocomprobacion[8].sesgo: ¿el MALO es de verdad malo?
- fase_c.autocomprobacion[8].hallazgo: Ahora el MALO vale 79,28 € (−26 % del precio). Su rentabilidad marginal (7,5 %) queda por debajo de r, pero todavía por encima de la tasa del motor (6,41 %), así que su reinversión de los años 1–10 crea algo de valor en la hoja. Con un S2C de 1,0 el MALO bajaría a ≈75,1 € y el precio de Sí a ≈95,7 € [cálculo]. Tampoco recoge un año como 2020.
- fase_c.autocomprobacion[8].cambio: lo anoto como incoherencia; no cambia la acción y no admite otra vuelta a la fase B
- fase_c.autocomprobacion[9].sesgo: lo no numerable que pesa y no está en las palancas
- fase_c.autocomprobacion[9].hallazgo: Fuera de las palancas quedan: (1) la negociación política del fin de las autopistas (prórroga a cambio de inversión, o más impuestos); (2) el litigio de la TEITLD; (3) la participación en ADP con bonos canjeables (semestral PDF p. 6); (4) si los dividendos a minoritarios son sostenibles. Los minoritarios ya están en el margen, como estimación.
- fase_c.autocomprobacion[9].cambio: (1)–(3) van a fase_c.md para B102 y las condiciones de revisión del turno 2; (4) a B222/B223
- fase_c.limite_del_modelo.porque: El escalón de las autopistas y la parte de los minoritarios caben en las palancas sin incoherencias mecánicas. La gramática da código 0 y la réplica reproduce el libro. Lo que queda es una hipótesis sin base sobre el valor de los minoritarios, no un motor que no pueda valorar la empresa.
- fase_c.cubo_provisional: Vigilar
- fase_c.conclusion_provisional: esperar
- fase_c.revision_datos_ausentes.revisados[0].dato: evidencia Historia!C23:L23
- fase_c.revision_datos_ausentes.revisados[0].que_falta: documento y clasificación verificables del pasivo por arrendamientos (fila 23)
- fase_c.revision_datos_ausentes.revisados[0].conclusion_afectada: pasivos netos del motor B (Historia C64 = 39.561 incluye 2.849 de arrendamientos) y vara del foso de la sección 1 bis (capital propio = capital invertido − arrendamientos)
- fase_c.revision_datos_ausentes.revisados[0].porque: la cifra que pesa, 2.849 a 31-dic-2025, la confirma el extracto (URD 2025 PDF p. 396: 737 a menos de un año, 795, 700 y 617), y 2.983 a 30-jun-2026 (semestral PDF p. 55); los años 2019–2024 solo entran en las medias de C54–C55 y en el ROIC propio, donde los arrendamientos son el 4–5 % del capital: ni el valor ni C18 cambian de forma apreciable
- fase_c.revision_datos_ausentes.revisados[1].dato: evidencia Historia!C16:L16
- fase_c.revision_datos_ausentes.revisados[1].que_falta: contraste con la partida de los ceros de intereses de arrendamiento en financiación de 2016–2018
- fase_c.revision_datos_ausentes.revisados[1].conclusion_afectada: ninguna celda de juicio: C48 (89,333) es la media de 2023–2025 (67 / 91 / 110) y la vara del foso usa 2021–2025; el motor B no usa la fila 16
- fase_c.revision_datos_ausentes.revisados[1].porque: los tres ceros son anteriores a la NIIF 16 (aplicable desde 2019) y en VINCI los intereses de la deuda van en explotación; aunque no fueran cero, no tocan C52, ni el motor B, ni la tabla de la sección 1 bis, que empiezan en 2021 o 2023
- fase_c.revision_datos_ausentes.revisados[2].dato: evidencia Historia!C17:L17
- fase_c.revision_datos_ausentes.revisados[2].que_falta: contraste con la partida de los ceros de principal de arrendamientos de 2016–2018
- fase_c.revision_datos_ausentes.revisados[2].conclusion_afectada: ninguna celda de juicio: C49 (675,333) es la media de 2023–2025 (611 / 654 / 761) y f (C58) se mide en 2021–2025
- fase_c.revision_datos_ausentes.revisados[2].porque: son ceros anteriores a la NIIF 16, cuando los arrendamientos financieros estaban dentro de la deuda bruta; solo afectarían a la serie antigua de FCF al accionista (fila 35), que no decide ninguna palanca del motor B ni el FCF base
- fase_c.revision_datos_ausentes.revisados[3].dato: Palancas!C24
- fase_c.revision_datos_ausentes.revisados[3].que_falta: tamaño del mercado en el año 10 con cifra de fuente primaria
- fase_c.revision_datos_ausentes.revisados[3].conclusion_afectada: Palancas!C24 (vacía) y la comprobación de cuota implícita G17, que la hoja no calcula («—» en la fila 45)
- fase_c.revision_datos_ausentes.revisados[3].porque: las ventas del BUENO (124.913 en el año 10) se apoyan en componentes con hechos de VINCI (cartera de 76,8 mil M y 14 meses de actividad, semestral PDF p. 16; concesiones con kilómetros y fechas, URD 2025 PDF p. 382), no en una cuota; el techo de mercado solo serviría de contraste por inversión
- fase_c.revision_datos_ausentes.revisados[4].dato: extracto_v63: Tamaño del mercado, crecimiento del mercado y cuota de mercado en euros o en porcentaje (solo la comparación de kilómetros de red en Francia).
- fase_c.revision_datos_ausentes.revisados[4].que_falta: tamaño, crecimiento y cuota de mercado de cada negocio
- fase_c.revision_datos_ausentes.revisados[4].conclusion_afectada: crecimiento de ventas B14:D14 y C24; viento de cola C17
- fase_c.revision_datos_ausentes.revisados[4].porque: el crecimiento se razonó por negocio con el orgánico publicado (2,6 % en 2025, 1,3 % en el semestre; URD 2025 PDF p. 130, semestral PDF p. 7) y la cartera; en autopistas la red es fija (4.443 km frente a 2.560 de Eiffage, PDF p. 12) y el crecimiento es tarifa y tráfico: la cuota no movería ninguna palanca de forma que cambie la zona
- fase_c.revision_datos_ausentes.revisados[5].dato: extracto_v63: Gasto de investigación y desarrollo (importe y % de ventas).
- fase_c.revision_datos_ausentes.revisados[5].que_falta: gasto de I+D
- fase_c.revision_datos_ausentes.revisados[5].conclusion_afectada: Palancas!C9 (No) y C10 (vacía)
- fase_c.revision_datos_ausentes.revisados[5].porque: VINCI es concesiones, servicios de energía y obra (C6 = Regulada, no Intangibles) y las cuentas no publican un gasto de I+D reconocido; capitalizar la I+D solo se pide con Intangibles o I+D > 5 % de ventas, y nada en el extracto sugiere ese peso
- fase_c.revision_datos_ausentes.revisados[6].dato: extracto_v63: Subidas anuales de peaje de ASF y Escota en porcentaje.
- fase_c.revision_datos_ausentes.revisados[6].que_falta: ley de tarifas anual de ASF y Escota
- fase_c.revision_datos_ausentes.revisados[6].conclusion_afectada: caja de las autopistas dentro del margen equivalente B15:D15 (crecimiento ≈1,5 % supuesto en la fase B)
- fase_c.revision_datos_ausentes.revisados[6].porque: ASF y Escota son el 72 % de los ingresos de Autoroutes (URD 2025 PDF p. 12) y la ley de Cofiroute (83 % de la inflación, PDF p. 143) da el orden de magnitud; con la réplica, llevar ese crecimiento de 1,5 % a 0 % o a 2,5 % mueve el valor de la caja de las autopistas entre −2,8 y +2,0 € por acción [cálculo], frente a 9,26 € entre el precio de Sí (97,79) y el precio: no cambia la acción y queda dentro de lo que ya mueve la hipótesis de los minoritarios, que marca el objetivo como provisional
- fase_c.revision_datos_ausentes.revisados[7].dato: extracto_v63: Ingresos por pasajero o tasas aeroportuarias por aeropuerto.
- fase_c.revision_datos_ausentes.revisados[7].que_falta: ingresos por pasajero y tasas por aeropuerto
- fase_c.revision_datos_ausentes.revisados[7].conclusion_afectada: BUENO (D14, D15) y crecimiento del NORMAL en aeropuertos
- fase_c.revision_datos_ausentes.revisados[7].porque: VINCI Airports es el 6,4 % de las ventas (4.796 de 74.599, URD 2025 PDF p. 134) con margen Ebit del 51,3 % ya publicado; el plan de OMA (inflación + 6,9 %, PDF p. 132) y los pasajeros (334 M; estables en el semestre) bastan para las palancas de grupo: el desglose por aeropuerto afinaría el BUENO, que pesa 0,15
- fase_c.revision_datos_ausentes.revisados[8].dato: extracto_v63: Deuda, flujos y obligaciones de fin de contrato concesión por concesión (solo VINCI Autoroutes y VINCI Airports agregados).
- fase_c.revision_datos_ausentes.revisados[8].que_falta: deuda, flujos y obligaciones de restitución por concesión
- fase_c.revision_datos_ausentes.revisados[8].conclusion_afectada: valor de la caja de las autopistas en el margen equivalente B15:D15 y pasivos netos
- fase_c.revision_datos_ausentes.revisados[8].porque: la deuda de las concesiones ya está entera en los pasivos netos (Autoroutes 15.001, PDF p. 141); los pesos y fechas de cada red están publicados (ASF 58 % en 2036, Cofiroute 25 % en 2034, Escota 14 % en 2032; PDF p. 12, 382) y la caja anual queda acotada entre el FCF publicado de Autoroutes (2,6 mil M después de financiación, PDF p. 140) y ≈3,0 mil M antes de ella; el rango 2,7–3,0 mueve ≈4,2 € por acción, menos que los 9,26 € que separan el precio de Sí del precio, y el MALO ya usa 2,7
- fase_c.revision_datos_ausentes.revisados[9].dato: extracto_v63: Múltiplos de compra de las adquisiciones.
- fase_c.revision_datos_ausentes.revisados[9].que_falta: múltiplos pagados en Gatwick, OMA, Edimburgo, Northwest Parkway y Cobra IS
- fase_c.revision_datos_ausentes.revisados[9].conclusion_afectada: S2C B16:C16, ROIC terminal B18:C18 y probabilidades B69/D69
- fase_c.revision_datos_ausentes.revisados[9].porque: el retorno sobre lo pagado ya lo mide el capital empleado por negocio, que lleva el precio de compra (Airports 2.459 de Ebit sobre 24,1 mil M, Cobra IS 644 sobre 5,3 mil M; URD 2025 PDF p. 136, 141), y los importes pagados están publicados (PDF p. 370; URD 2023 PDF p. 170): el múltiplo afinaría la vara, no cambiaría el lado de r en el que caen las compras
- fase_c.revision_datos_ausentes.revisados[10].dato: extracto_v63: Márgenes por segmento a tipo de cambio constante.
- fase_c.revision_datos_ausentes.revisados[10].que_falta: márgenes por segmento a tipo constante
- fase_c.revision_datos_ausentes.revisados[10].conclusion_afectada: margen B15:D15 (margen del resto del grupo)
- fase_c.revision_datos_ausentes.revisados[10].porque: el efecto del tipo de cambio en ventas fue −1,0 % en 2025 (URD 2025 PDF p. 130) y los márgenes por segmento se publican en euros corrientes en dos años (PDF p. 136): el tipo constante no movería el margen del resto (8,5–8,9 %) en el redondeo de 0,005
- fase_c.revision_datos_ausentes.revisados[11].dato: extracto_v63: Límites regulatorios a la distribución de dividendos.
- fase_c.revision_datos_ausentes.revisados[11].que_falta: restricciones a subir caja de concesiones y filiales a VINCI SA
- fase_c.revision_datos_ausentes.revisados[11].conclusion_afectada: ninguna celda de juicio directamente; lectura de la caja del accionista junto con los minoritarios
- fase_c.revision_datos_ausentes.revisados[11].porque: los ratios de las financiaciones se cumplen (URD 2025 PDF p. 405), fuera de Concesiones hay caja neta (+1.718, +3.801 y +4.530 en holdings, PDF p. 141) y VINCI paga 5,00 € por acción (PDF p. 142); la caja que no es del accionista son los minoritarios, que la fase B ya resta del margen y que trato aparte como hipótesis sin base, no la regulación
- fase_c.revision_datos_ausentes.revisados[12].dato: extracto_v63: Calendario anual de la inversión del plan climático 2026–2030.
- fase_c.revision_datos_ausentes.revisados[12].que_falta: calendario anual del capex del plan climático
- fase_c.revision_datos_ausentes.revisados[12].conclusion_afectada: ninguna celda de juicio: S2C B16:D16 en el margen
- fase_c.revision_datos_ausentes.revisados[12].porque: son «over €1.5 billion» en cinco años (URD 2025 PDF p. 231), ≈0,3 mil M al año frente a un capex de 3.873 (Historia L12) y financiados con los recursos de los negocios: su reparto por años no mueve la reinversión del motor en el redondeo de 0,1
- fase_c.fundamento_material.hipotesis_sin_fundamento[0].celda: Palancas!B15:D15
- fase_c.fundamento_material.hipotesis_sin_fundamento[0].hipotesis: el recorte por minoritarios (−0,008 / −0,008 / −0,007) supone que su parte de Gatwick, Edimburgo y OMA vale 805 ÷ (r − g), es decir, que los 805 de dividendos de 2025 son el flujo sostenible de los minoritarios
- fase_c.fundamento_material.hipotesis_sin_fundamento[0].clase: fundamentada, con confianza baja, según la fase B; el tamaño del recorte no tiene ningún hecho que lo acote
- fase_c.fundamento_material.hipotesis_sin_fundamento[0].porque_sin_fundamento: 805 son dividendos, no el resultado atribuido. El valor contable de los minoritarios baja de 4.085 a 3.576 (URD 2025 PDF p. 399) mientras cobran 805 y 902 (PDF p. 358), lo que apunta a dividendos por encima del resultado. La propia Observación de C15 dice que con el resultado atribuido el NORMAL iría hacia 0,095. El precio de Sí pasa de 97,79 a ≈104,9 € con medio recorte [cálculo]
- fase_c.fundamento_material.hipotesis_sin_fundamento[0].alternativas_defendibles.evidencia: No puedo atar los dos límites a hechos. Por arriba, el recorte de la fase B ya usa el menor de los dos años de dividendos, pero no hay hecho que diga que el flujo sostenible de los minoritarios sea tan alto. Por abajo, los precios de compra (OMA 1.169 por el 29,99 %, URD 2023 PDF p. 170; Edimburgo 1.431 por el 50,01 %, URD 2025 PDF p. 370) implican 4.159 para la parte ajena de dos de las tres filiales. Pero llevan prima de control, son de 2022 y 2024, y no conozco qué parte de los 3.576 es de Gatwick. Haría falta la nota de intereses minoritarios del URD 2025: resultado neto, dividendos, deuda neta y flujo atribuidos a los minoritarios de London Gatwick, Edimburgo y OMA.
- fase_c.fundamento_material.resultado: no_procede
- fase_c.fundamento_material.hipotesis_que_mas_condiciona: Palancas!B15:D15: tamaño del recorte por minoritarios (805 de dividendos capitalizados a r − g frente a 3.576 contables). Condiciona el precio objetivo (97,79 € con el recorte entero, ≈104,9 € con la mitad) y, solo si el exceso bajara de ≈3,45 mil M, la acción
- fase_c.fundamento_material.que_lo_resolveria: URD 2025, nota de intereses minoritarios: resultado neto, dividendos, deuda neta y flujo de caja de London Gatwick, Edimburgo y OMA atribuidos a los minoritarios en 2023–2025 (o el resultado neto atribuido a minoritarios del grupo), para sustituir los dividendos por el resultado en el recorte de B15:D15
- fase_c.celdas_corregidas.Palancas!B15.motivo: revisada tras la vuelta: incluye el recorte por minoritarios (−0,008) con base en dividendos; se mantiene, con el objetivo marcado como provisional
- fase_c.celdas_corregidas.Palancas!C15.motivo: revisada tras la vuelta: 0,098–0,101 menos 0,008 de minoritarios, redondeado a 0,09; se mantiene, con la duda dividendos frente a resultado en hipotesis_sin_fundamento
- fase_c.celdas_corregidas.Palancas!D15.motivo: revisada tras la vuelta: 0,105–0,108 menos 0,007, redondeado a 0,10; se mantiene
- fase_c.celdas_corregidas.Palancas!C16.motivo: revisada tras la vuelta: mezcla 77 % compras al 6,9 % y 23 % propio al 16,1 % ≈ 9 %, con rentabilidad marginal 9,2 %, coherente con la historia NORMAL; se mantiene
- fase_c.estado_analisis: concluido
- fase_c.cubo_final: Vigilar
- fase_c.escalera.de: precio.json
- fase_c.escalera.zona: caro
- fase_c.escalera.rango_precio_de_si_por_minoritarios: ≈97,8 (recorte entero, libro) a ≈104,9 € (medio recorte) [cálculo, réplica]; sensibilidad condicional, no intervalo de confianza
- fase_c.decision.accion: esperar
- fase_c.decision.condiciones_revision.al_alza: Que la nota de minoritarios del URD muestre un resultado atribuido menor que los dividendos (recorte menor: precio de Sí hacia 105 €); una prórroga o compensación de alguna autopista francesa; compras de 2026 (Safeway, A154–A120, All for One) con retornos publicados por encima de r.
- fase_c.decision.condiciones_revision.a_la_baja: Una tercera carga fiscal francesa sobre las concesiones o la contribución excepcional hecha permanente; deterioros en Cobra IS (goodwill 4.156) o en aeropuertos; tráfico de autopistas y pasajeros a la baja en 2026–2027; compras grandes a retornos por debajo del 7 % después de impuestos.
- fase_c.insumos_decision_cartera.zona: caro
- fase_c.insumos_decision_cartera.fundamento: no procede (conclusión no favorable); precio objetivo provisional, condicionado al recorte por minoritarios de Palancas!B15:D15 (hipótesis sin base)
- fase_c.insumos_decision_cartera.descalificadores_considerados[0]: deuda que puede matar en un mal año: no (deuda neta 1,4 veces el Ebitda, A−/A3, liquidez 22,0 mil M; URD 2025 PDF p. 141, 405)
- fase_c.insumos_decision_cartera.descalificadores_considerados[1]: demasiadas piezas móviles / conglomerado (aviso A4): no; lo entiendo por partes y lo decisivo son pocas variables; el borde es Cobra IS
- fase_c.insumos_decision_cartera.descalificadores_considerados[2]: reinvertir toda la caja para mantenerse con retornos mediocres: riesgo tras 2036, no hoy (dividendo de 5,00 € y recompras; PDF p. 141–142)
- fase_c.insumos_decision_cartera.descalificadores_considerados[3]: valor que depende de prever macro o tipos: no; depende de contratos con fecha y del retorno de la reinversión
- fase_c.insumos_decision_cartera.descalificadores_considerados[4]: gestión en la que no confío: no (C98 = Aceptable)
- fase_c.insumos_decision_cartera.palanca_mas_influyente: Tasa de descuento (±1 pt)
- fase_c.herencia.C93.etapa1: No lo sé
- fase_c.herencia.C93.decision: cambia
- fase_c.herencia.C93.motivo: evidencia_nueva
- fase_c.herencia.C93.evidencia_y_razonamiento: La etapa 1 no sabía a qué retorno se reponían las concesiones. El capital empleado por negocio (URD 2025 PDF p. 136, 141) da 6,9 % (Airports) y 8,3 % (Cobra IS) después de impuestos: un ROIC terminal del 7 % con g 0,02 < rf queda dentro de lo observado, con salto del año 11 de 2,2 puntos y peso del terminal 0,68.
- fase_c.herencia.B101.etapa1: VINCI cobra peajes y tasas por infraestructuras que nadie puede duplicar y vende servicios de energía y obra con poco capital. La caja es real: FCF de 3.179 a 7.010 M€ entre 2018 y 2025, deuda neta de 1,4 veces el Ebitda y calificación A−. Pero entre el 35 % y el 38 % del beneficio y del FCF viene de autopistas francesas que vuelven gratis al Estado entre 2032 y 2036, y ese Estado ya ha creado dos impuestos nuevos que le afectan. El valor depende de reinvertir esa caja por encima del 9 %, y el ROCE del grupo ha estado entre el 9 % y el 11 %. A 107 € pago más o menos el escenario normal; compraría hacia 79 €.
- fase_c.herencia.B101.decision: cambia
- fase_c.herencia.B101.motivo: evidencia_nueva
- fase_c.herencia.B101.evidencia_y_razonamiento: Mantiene el núcleo (caja real, autopistas que vencen, Estado que grava), pero el «compraría hacia 79 €» era una estimación sin la hoja con 4.382 de FCF base y 567,06 M de acciones (extracto §0); ahora el libro valora tres historias, resta el exceso de los minoritarios (805 de dividendos, PDF p. 358) y la escalera da 97,79 €.
- fase_c.herencia.B102.etapa1: El argumento del No, lo mejor que sé hacerlo: (1) la joya es un activo que se gasta; VINCI Autoroutes es el 35 % del Ebit y el 38 % del FCF, y sus concesiones principales (ASF, Escota y Cofiroute) se devuelven sin compensación en 2032-2036, y para seguir igual VINCI tiene que comprar su futuro en concesiones nuevas a precios de mercado, y VINCI Airports rinde hoy ≈10 % antes de impuestos sobre su capital empleado [cálculo]. (2) La contraparte es un Estado con déficit que ya creó la TEITLD en 2024 (la empresa la considera contraria a las cláusulas de neutralidad fiscal de los contratos) y una contribución excepcional en 2025 que repite en 2026; lo extraordinario que se repite es gasto. (3) El FCF publicado de 7.010 está inflado para el accionista: +2.496 de circulante que la propia empresa llama excepcional, 805 de dividendos a minoritarios, 567 de pagos en acciones; la guía de 2026 es de unos 6.000. (4) Cobra IS añade piezas que no controlo: EPC al 45 % de sus ventas, renovables con riesgo de precio eléctrico, FCF de −365, goodwill de 4.156 sin deterioro y una compra de campos de petróleo que acabó en revisión estratégica. (5) Los incentivos premian BPA ajustado y Ebitda ajustado por circulante, cifras que se pueden mover con cobros de fin de año; el bonus sale al 98 % del máximo, los directivos venden todos los años y el TSR quedó 47,8 puntos por detrás de su índice en 2023-2025. A 107 € el precio ya descuenta el caso normal, así que cualquier error va contra mí.
- fase_c.herencia.B102.decision: cambia
- fase_c.herencia.B102.motivo: evidencia_nueva
- fase_c.herencia.B102.evidencia_y_razonamiento: Conservo sus argumentos de vencimiento, fiscalidad, Cobra IS y circulante, con cifras vigentes; quito los que mis entradas no sostienen (ventas de directivos, que no están en el expediente) y añado el retorno de lo comprado (6,9–8,3 %), los minoritarios y el DCF inverso del libro (5,4 %).
- fase_c.herencia.C103.etapa1: No
- fase_c.herencia.C103.decision: mantiene
- fase_c.herencia.C103.motivo: misma_evidencia
- fase_c.herencia.C103.evidencia_y_razonamiento: Revisados los vencimientos (URD 2025 PDF p. 382) y el retorno de lo que sustituye a las autopistas: el activo principal caduca por contrato y el futuro se compra a precio de mercado; «nunca vender» no es una propiedad de este negocio.
- fase_c.herencia.C104.etapa1: 0% · Watchlist · precio de Sí ≈ 79 €
- fase_c.herencia.C104.decision: cambia
- fase_c.herencia.C104.motivo: definicion_o_medicion_distinta
- fase_c.herencia.C104.evidencia_y_razonamiento: La V6.3 prohíbe el porcentaje de posición (D16) y fija la etiqueta de la sección 15 con la escalera k = 3 de precio.json; el ≈79 € de la etapa 1 aplicaba la regla mín(MALO, 0,75 × ponderado), que en este libro (C156) da 79,28.
- fase_c.comparacion_etapa_1.cubo_v1: Vigilar
- fase_c.comparacion_etapa_1.cubo_v2: Vigilar
- fase_c.comparacion_etapa_1.por_que_difieren: El cubo coincide: buen negocio con un foso que caduca por contrato, a un precio sin margen. El precio de Sí difiere por la regla y no por la valoración: la etapa 1 usaba mín(MALO, 0,75 × ponderado), y esa misma regla en este libro da 79,28 € (C156), casi su ≈79 €; la v2 aplica la escalera k = 3 (D11) a tres escenarios calculados por la hoja, que da 97,79 €. Las cifras de la v1 (FCF base 4.382, 567,06 M de acciones, sin hoja) no están vigentes (extracto §0). La v2 añade lo que la v1 no restaba: la parte de Gatwick, Edimburgo y OMA que es de sus socios. La v1 decía insiders «Vendiendo» con datos que no están en mis entradas; la v2 no lo usa.
- fase_c.celdas.C93: Sí
- fase_c.celdas.C103: No
- fase_c.celdas.C104: Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 97.79 · zona caro · precio de Sí ≤ 97.79 · precio esc. MALO 79.28 · ponderado 107.04 · fundamento no procede (conclusión no favorable) · objetivo provisional: depende del recorte por minoritarios de Palancas!B15:D15 (con medio recorte el precio de Sí sería de unos 105)
- fase_c.celdas.B101: VINCI cobra peajes y tasas por autopistas y aeropuertos sin sustituto cercano y vende servicios de energía y obra con poco capital: FCF de 7.010 M€ en 2025, deuda neta de 1,4 veces el Ebitda y calificación A− (URD 2025 PDF p. 139, 141). Su mejor activo, las autopistas francesas (3.311 de 9.558 M€ de Ebit), vuelve al Estado entre 2032 y 2036, y lo que compra para sustituirlo rinde cerca del 7 % después de impuestos (Airports 6,9 %, Cobra IS 8,3 % [cálculo, PDF p. 136, 141]). Además, una parte del flujo de Gatwick, Edimburgo y OMA es de sus socios, que cobraron 805 M€ de dividendos en 2025 (PDF p. 358). Con mis tres escenarios vale 79 / 102 / 174 € y a 107,05 € el precio pide un crecimiento de ventas del 5,4 % al año, más que mi caso central del 4 %. Es un negocio correcto con un foso con fecha: espero, con un precio de Sí de 97,79 € que es provisional mientras no conozca el resultado de los minoritarios.
- fase_c.celdas.B102: El argumento del No, mejor de lo que lo haría un bajista: (1) la joya se gasta: VINCI Autoroutes da 3.311 de los 9.558 M€ de Ebit y 2,6 mil M de FCF (URD 2025 PDF p. 136, 140) y ASF, Escota y Cofiroute vuelven al Estado en 2032–2036 (PDF p. 382); lo que compra para sustituirlas rinde menos que r: Airports 6,9 % y Cobra IS 8,3 % después de impuestos [cálculo, PDF p. 136, 141]. (2) La contraparte cobra antes del final: TEITLD de 284 desde 2024 (URD 2024 PDF p. 134) y contribución excepcional de 449 en 2025, repetida en 2026 (URD 2025 PDF p. 138, 143). (3) Lo del accionista es menos de lo que parece: 805 M€ de dividendos a minoritarios frente a 3.576 de valor contable (PDF p. 358, 399), y el FCF publicado lleva +2.496 de circulante y 567 de pagos en acciones (Historia L14, L18). (4) Asigna mal el capital caro: 21.371 de compras en diez años sin múltiplos publicados (Historia fila 13; PDF p. 370), Cobra IS con FCF de −365 y goodwill de 4.156 (PDF p. 140; Análisis C32), y recompras a 119,11 € y 125,80 €, por encima del precio (PDF p. 141; semestral PDF p. 15). (5) El precio ya está en el ponderado (107,04) y pide un 5,4 % de crecimiento de ventas con un orgánico del 1,3 % en el semestre y tráfico −2,9 % (semestral PDF p. 7): es el negocio en que «all the excess cash must be reinvested» (PCA p.110; HIM) para no encoger, y para eso no hace falta vigilarlo.
- fase_c.celdas.Diagnóstico V6!B222: Tamaño del recorte por minoritarios en Palancas!B15:D15 (−0,008 / −0,008 / −0,007): capitaliza los 805 M€ de dividendos de 2025 a r − g frente a 3.576 de valor contable, pero el contable baja de 4.085 a 3.576 y los dividendos pueden superar el resultado atribuido; con medio recorte el precio de Sí pasaría de 97,79 a unos 105 € (objetivo provisional).
- fase_c.celdas.Diagnóstico V6!B223: URD 2025, nota de intereses minoritarios (información resumida de filiales con minoritarios materiales): resultado neto, dividendos, deuda neta y flujo de London Gatwick, Edimburgo y OMA atribuidos a los minoritarios en 2023–2025; si no está, pregunta a Relación con Inversores por el resultado neto atribuido a minoritarios por filiales.
- fase_c.celdas.Palancas!A38: Las ventas de Energy Solutions (VINCI Energies más Cobra IS) del ejercicio 2027 publicadas por VINCI son de al menos 32.000 M€ (29.612 en 2025).
- fase_c.celdas.Palancas!B38: 2028-03-31
- fase_c.celdas.Palancas!A39: El ROCE del grupo que VINCI publica para el ejercicio 2027 queda entre el 9,0 % y el 11,5 % (10,7 % en 2025 y 11,4 % en 2024).
- fase_c.celdas.Palancas!B39: 2028-03-31
- fase_c.celdas.Palancas!A40: Los ingresos de VINCI Autoroutes del ejercicio 2027 no superan 7.100 M€ (6.733 en 2025).
- fase_c.celdas.Palancas!B40: 2028-03-31
- fase_c.cambiaria_de_cubo.a_si: Un precio por debajo del precio de Sí (97,79 €, o el que resulte cuando la nota de minoritarios fije el recorte) con los hechos intactos, y la nota de minoritarios del URD resolviendo la hipótesis de B222; para comprar haría falta además que la conclusión favorable tuviera fundamento (D10).
- fase_c.cambiaria_de_cubo.a_no: Que el valor del NORMAL quede por debajo del precio sin margen posible por hechos nuevos: compras de 2026–2027 a retornos por debajo de la tasa del motor, deterioros en Cobra IS o aeropuertos, o una carga fiscal francesa permanente que lleve el margen del resto del grupo por debajo del 8 %.
- fase_c.cambiaria_de_cubo.a_demasiado_dificil: Que el valor pase a depender de la negociación política del fin de las autopistas después de 2036 (prórrogas a cambio de inversión, rescate anticipado) o de las pérdidas del EPC de Cobra IS, variables que no sé juzgar.
- fase_c.observaciones.Palancas!A38: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: 29.612 en 2025 (URD 2025 PDF p. 134), +6,8 % en el primer semestre de 2026 y cartera de 69,8 a 76,8 mil M (semestral PDF p. 9, 16); 32.000 exige ≈4 % al año, el ritmo del NORMAL del grupo (Palancas C14). Falsable con el informe anual 2027 (segmentos).
Lo sustituiría: ventas por debajo de 31.000 me moverían el NORMAL hacia el MALO; por encima de 34.000, hacia el BUENO.
- fase_c.observaciones.Palancas!B38: [Clase: convención] [Confianza: alta]
Hereda: nueva en V6.3.
Apoyo: 2028-03-31, a unos 18 meses de la fecha de análisis (Análisis D4 = 2026-10-10), dentro de la ventana de 12–24 meses; VINCI publica el informe anual del ejercicio en febrero o marzo del año siguiente (URD 2025, cuentas de 2025).
Lo sustituiría: un cambio en el calendario de publicación de VINCI.
- fase_c.observaciones.Palancas!C38: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: 0.65 es la probabilidad de que la predicción 1 se cumpla dado el escenario NORMAL (no la probabilidad del escenario): el NORMAL la cumple con su centro y la banda deja margen para un año flojo como el semestre de 2026 (semestral PDF p. 7, 9).
Lo sustituiría: los datos del ejercicio 2026, que dirán si la senda del NORMAL se sostiene.
- fase_c.observaciones.Palancas!A39: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: ROCE 10,7 % en 2025 y 11,4 % en 2024 (URD 2025 PDF p. 142); el NORMAL reinvierte en torno a r (rentabilidad marginal 9,2 %, Palancas C16) y las autopistas siguen dentro hasta 2032: el ROCE no debería salir de esa banda. Falsable con el informe anual 2027.
Lo sustituiría: un ROCE por encima del 11,5 % con compras grandes me haría revisar el S2C del NORMAL al alza; por debajo del 9 %, hacia el MALO.
- fase_c.observaciones.Palancas!B39: [Clase: convención] [Confianza: alta]
Hereda: nueva en V6.3.
Apoyo: 2028-03-31, a unos 18 meses de la fecha de análisis (Análisis D4 = 2026-10-10), dentro de la ventana de 12–24 meses; VINCI publica el informe anual del ejercicio en febrero o marzo del año siguiente (URD 2025, cuentas de 2025).
Lo sustituiría: un cambio en el calendario de publicación de VINCI.
- fase_c.observaciones.Palancas!C39: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: 0.7 es la probabilidad de que la predicción 2 se cumpla dado el escenario NORMAL (no la probabilidad del escenario): el NORMAL la cumple con su centro y la banda deja margen para un año flojo como el semestre de 2026 (semestral PDF p. 7, 9).
Lo sustituiría: los datos del ejercicio 2026, que dirán si la senda del NORMAL se sostiene.
- fase_c.observaciones.Palancas!A40: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: 6.733 en 2025 (URD 2025 PDF p. 134), tráfico −2,9 % y ingresos −0,7 % en el primer semestre de 2026 (semestral PDF p. 7) y subidas de peaje contractuales (Cofiroute al 83 % de la referencia, PDF p. 143): el NORMAL no espera crecimiento real de la red. Falsable con el informe anual 2027.
Lo sustituiría: ingresos por encima de 7.100 (tráfico al alza o una adenda con subidas) me harían revisar al alza la caja de las autopistas del margen equivalente.
- fase_c.observaciones.Palancas!B40: [Clase: convención] [Confianza: alta]
Hereda: nueva en V6.3.
Apoyo: 2028-03-31, a unos 18 meses de la fecha de análisis (Análisis D4 = 2026-10-10), dentro de la ventana de 12–24 meses; VINCI publica el informe anual del ejercicio en febrero o marzo del año siguiente (URD 2025, cuentas de 2025).
Lo sustituiría: un cambio en el calendario de publicación de VINCI.
- fase_c.observaciones.Palancas!C40: [Clase: fundamentada] [Confianza: media]
Hereda: nueva en V6.3.
Apoyo: 0.75 es la probabilidad de que la predicción 3 se cumpla dado el escenario NORMAL (no la probabilidad del escenario): el NORMAL la cumple con su centro y la banda deja margen para un año flojo como el semestre de 2026 (semestral PDF p. 7, 9).
Lo sustituiría: los datos del ejercicio 2026, que dirán si la senda del NORMAL se sostiene.
- fase_c.observaciones.C93: [Clase: fundamentada] [Confianza: media]
Hereda: No lo sé → cambia (evidencia_nueva): el capital empleado por negocio y la vara de la sección 1 bis permiten juzgar la reposición.
Apoyo: g NORMAL 0,02 < rf 0,0347 (C57); ROIC terminal 7 % > tasa del motor 6,41 % y dentro de lo que rinde hoy lo que VINCI compra (Airports 6,9 %, Cobra IS 8,3 % después de impuestos [cálculo, URD 2025 PDF p. 136, 141]); reinvierte g ÷ ROIC ≈ 29 % del NOPAT; salto del año 11 de 2,2 puntos y peso del terminal 0,68 (< 0,75). Crecer un 2 % con la inflación de Europa reponiendo concesiones a ≈7 % es sostenible; lo que no lo sería es crecer más.
Lo sustituiría: compras de 2026–2027 (Safeway, All for One) a retornos por debajo del 6 %, hacia No lo sé.
- fase_c.observaciones.C103: [Clase: fundamentada] [Confianza: alta]
Hereda: No → mantiene (misma_evidencia): el activo principal caduca por contrato.
Apoyo: ASF 2036, Cofiroute 2034 y Escota 2032 vuelven al Estado (URD 2025 PDF p. 382) y para seguir igual VINCI tiene que comprar su futuro a precios de mercado (Airports 6,9 % después de impuestos [cálculo]). No es la empresa en la que «you can sit on your ass» (PCA pp.85–86; HIM).
Lo sustituiría: prórrogas largas de las autopistas o un historial de compras que rindan por encima de r de forma sostenida.
- fase_c.observaciones.C104: [Clase: convención] [Confianza: alta]
Hereda: 0% · Watchlist · precio de Sí ≈ 79 € → cambia (definicion_o_medicion_distinta): sin porcentaje de posición (D16) y con la escalera k = 3 del libro, no la regla mín(MALO, 0,75 × ponderado).
Apoyo: precio.json: precio de Sí 97,79, MALO 79,28, ponderado 107,04, zona caro; la regla antigua (C156) da 79,28. El objetivo es provisional: lo condiciona el recorte por minoritarios (B222). El tamaño es de José Luis.
Lo sustituiría: la nota de minoritarios del URD (B223), que fijaría el recorte y el precio de Sí; un precio por debajo del precio de Sí con los hechos intactos.
- fase_c.observaciones.B101: [Clase: fundamentada] [Confianza: media]
Hereda: tesis de la etapa 1 («… compraría hacia 79 €») → cambia (evidencia_nueva): el libro valora las tres historias y la parte de los minoritarios.
Apoyo: FCF 7.010 y deuda neta 1,4× (URD 2025 PDF p. 139, 141); Ebit por negocio (PDF p. 136); vencimientos (PDF p. 382); dividendos a minoritarios 805 (PDF p. 358); B78:D78 y C86 del libro; precio.json.
Lo sustituiría: una prórroga de las autopistas, la nota de minoritarios o compras que rindan por encima de r.
- fase_c.observaciones.B102: [Clase: fundamentada] [Confianza: media]
Hereda: tesis inversa de la etapa 1 → cambia (evidencia_nueva): mantiene sus puntos de vencimiento y fiscalidad y añade los minoritarios, el retorno de lo comprado y el DCF inverso.
Apoyo: URD 2025 PDF p. 136, 138, 140, 141, 143, 358, 370, 382, 399; URD 2024 PDF p. 134; semestral PDF p. 7, 15; Historia filas 13, 14 y 18; Análisis C32; C86.
Lo sustituiría: compras con retornos publicados por encima de r o una compensación del Estado al final de las concesiones.
- fase_c.confianza_global: media
