# Fase C · turno 1 (sobre el libro recalculado tras la corrección de la fase B) · Koninklijke Ahold Delhaize N.V. (AD) · motor A

Fuentes: Historia fila n y Cnn son celdas de `datos_v63.md`; las páginas de los informes son las de `extracto_v63.md` (AR2025 PDF p. n; Q3-26 PDF p. n). Los valores de la hoja vienen de `resultados.json` y la escalera de `precio.json`, que leo y no recalculo. Las variantes son mías. Las saco de una réplica de la fórmula del motor A, que reproduce B78:D78 al céntimo. Sirven para medir sensibilidades y no sustituyen al recálculo oficial. La vuelta C→B ya se usó: lo que siga abierto lo declaro aquí, no pido otra.

## 1. Una sola historia

**Lo que dice la hoja.** Valores: MALO 23,62 €, NORMAL 30,10 € y BUENO 38,89 €; ponderado 29,80 €. Precio 36,05 €. Precio de Sí 27,74 €. Zona caro. El precio está un 30,0 % por encima del precio de Sí (diferencia ÷ precio de Sí).

**Semáforos.** Pasan todos menos la fila 42 del BUENO: cada euro nuevo rendiría un 22 %, más del doble de C55.

**Terminal.** El peso del terminal es 41 %, 53 % y 54 %. El salto del año 11 es de +0,2, +1,2 y +9,7 puntos (aviso V16 en el BUENO).

**Tornado.** El margen es lo que más mueve (19,70 €), después la tasa (5,10 €) y el ROIC a largo plazo (2,68 €). Es información, no criterio.

**DCF inverso.** Ahora se puede usar. Con mi margen, mi S2C y mi ROIC del NORMAL, el precio descuenta un crecimiento de ventas del 11,3 % al año durante cinco años. La historia dice otra cosa: 4,3 % a cinco años con compras (C46) y 2,0 % a tres años (C45). Solo la fusión de 2017 y la inflación de 2022 pasaron de ese ritmo. Se pagan 5,98 € por encima del valor sin crecimiento (30,07 €) por un crecimiento que en el NORMAL vale 0,02 €.

La historia de la fase A se sostiene: es un negocio duradero que no gana más que mi alternativa sobre el capital total, y su precio pide algo que no ha hecho. Hay estas tensiones, resueltas o declaradas:

1. **Salto del BUENO (9,7 puntos).** La fase B lo justifica porque la competencia se lleva lo que dio la escala. Pero el motor mantiene el margen del 4,0 % para siempre. Lo que cambia en el año 11 es la intensidad de capital propio: de 6,9 a unos 3,8 euros de venta por euro. Mi lectura es que, a perpetuidad, el BUENO ya no puede crecer casi solo con tiendas arrendadas y compras baratas, y necesita el capital de un minorista sin foso. Es prudente y casi inmaterial: sin salto (D18 = 0,22), el precio de Sí sube un 1,1 %.
2. **C18 y D18 = 0,12, justo la tasa + 3 puntos.** La cifra sale del tope del criterio (MR; E2), no de un hecho de la empresa, y ese criterio piensa en el capital total. Lo declaro en el fundamento material (punto 7).
3. **Crecer ya no destruye valor.** En A2 la reinversión del NORMAL rinde un 13,2 %. El accionista gana más que r sobre su capital propio porque el arrendador pone las tiendas: el 85 % de los locales es arrendado (AR2025 PDF p. 58). Eso es apalancamiento con renta fija, no foso. C18 = No y el cubo no cambian. Cambia el motivo: el riesgo está en la renta que no baja en el MALO.
4. **C8 = Último año.** El motor arranca del mejor año de la ventana. Con Media del ciclo el precio de Sí bajaría un 0,8 %. La mantengo, porque la regla da Último año.
5. **f.** f se calibra con una ventana que incluye la devolución fiscal belga de 2023 (+367; datos_v63 §2). La fuga de 2025 sola es 0,0059 de las ventas: 2.784 − 85 − 2.150 (Historia filas 30 y 35). Con f entre 0,005 y 0,0059, el precio de Sí bajaría un 7–12 %. Es un dato: no lo cambio. Empuja hacia caro y No.
6. **La caja del MALO.** El año 1 da 2.328, más que cualquier flujo del accionista de la década (máximo 2.150), porque con crecimiento 0 no reinvierte. Su daño llega en los años 4–10 y en el terminal.
7. **Documentación de la fase B.** `fase_b.md` conserva las secciones de S2C y ROIC de la primera pasada. Manda la sección de la corrección, y las Observaciones del JSON están al día.
8. **El veredicto de A6.** A6 descarta por el filtro Pabrai (C13). Mi No es por la calidad.

## 2. Desviaciones pendientes

`gramatica.md` trae dos desviaciones del BUENO, las dos justificadas en el JSON con hechos:

- **G7: rentabilidad marginal de 21,7 %, más de 2 × C55.** C55 lleva los arrendamientos dentro y A2 no. En A2, el capital propio rindió un 14,8 % de media en 2021–2025. La ventana 2020–2025 (+17.616 de ventas con +2.552 de capital propio) es la más cargada de capital de las que da la Historia. Es estructura de financiación, no foso.
- **G8: salto de 9,7 puntos.** Es mi hipótesis de lo que se pierde en el año 11: la ligereza de capital, no el margen. Los arrendamientos se renuevan a renta de mercado y las compras se pagan a precio pleno; Profi apenas supera su prueba de deterioro (AR2025 PDF p. 238). El efecto es de +1,1 % como mucho.

El aviso A3 (fechas) sube el valor por acción en torno a un 3,6 % con las acciones del 3T y no cambia la zona. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).

## 3. Palancas

Comprobé la corrección de la fase B. Todo está en A2_propio y la aritmética cuadra: B16 = 62.791 ÷ 16.136 = 3,9; C16 = mezcla de 6,2 orgánico y 2,3 de Profi = 4,8; D16 = 17.616 ÷ 2.552 = 6,9. Los ROIC son 9,2 %, 13,2 % y 21,7 %, con los dos últimos topados en 0,12. El orden se mantiene y g < ROIC. No hay palancas mal derivadas: `revisar_palancas = false`.

| Variante (réplica) | Precio de Sí | Ponderado | Zona |
|---|---|---|---|
| Libro | 27,74 | 29,80 | caro |
| C18 = 0,09 / 0,13 | 27,23 / 27,85 | 29,04 / 29,97 | caro |
| D18 = 0,22 | 28,03 | 30,24 | caro |
| C16 = 3,2 y C18 = 0,08 (ventana entera) | 26,12 | 27,41 | caro |
| C15 = 0,04 (juicio, no error) | 29,71 | 32,75 | caro |
| Probabilidades 0,2/0,6/0,2 | 28,58 | 30,56 | caro |
| f = 0,005 / 0,0059 (dato) | 25,76 / 24,48 | 27,68 / 26,31 | caro |

En `celdas_corregidas` registro lo revisado con `despues = antes`. De la fase A: C18, C62 y Palancas!C8. De la fase B: B16:D18.

## 4. Autocomprobación

- **Anclaje en la etapa 1.** Revisé C18 = No con lo que lo contradice: ROIC sin fondo de comercio de 12,9–13,5 % y capital propio con un 14,8 %. Se sostiene. El exceso sobre r viene del arrendamiento.
- **Precio o fuente externa.** Los valores suben por el perímetro, no por acercarse al precio. El ponderado sigue un 17 % por debajo del precio (diferencia ÷ precio).
- **Consistencia y compromiso.** El NORMAL ya no destruye valor. Comprobé si eso tumba el No: no, pero cambia su motivo.
- **Viento de cola.** El 21,7 % del BUENO es en buena parte el arrendador, no mérito operativo.
- **Optimismo del BUENO.** El ROIC terminal no lleva el 21,7 % a perpetuidad y el BUENO pesa poco en el precio de Sí.
- **Doble castigo.** La doble cuenta del arrendamiento quedó corregida. Margen del NORMAL, MALO y probabilidades caen del mismo lado, cada uno con su hecho. Lo dejo para la tesis inversa.
- **Disponibilidad.** p(MALO) = 0,25 lo sostienen cuatro de diez años con un margen del 3,2 % o menos, no el trimestre de 2026. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM).
- **Autoridad.** Ninguna palanca copia la guía. Los S2C y ROIC salen de la Historia.
- **¿El MALO es malo?** En margen sí; en la caja de los años 1–3, no. Con la f de 2025 bajaría a unos 20,8 €. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** Hay 14.721 de arrendamientos sin descontar (AR2025 PDF p. 271). Justo lo que hace rendir al capital propio es lo que no baja en un mal año. Añado Profi, Tesco, los cambios en la dirección y la poca propiedad del consejo. Todo va a la tesis inversa y a B222.

## 5. Cubo y conclusión provisionales

Sigo el orden de mando:

- **Bloqueo:** no hay. La gramática da cero errores y el estado INCOMPLETO solo se debe a las predicciones.
- **Límite del modelo:** no hay.
- **Calidad:** el retorno del capital total no supera mi alternativa en diez años y el ahorro se lo queda el cliente. Lo evalué y no cumple: «We have three baskets: in, out, and too tough» (TCI p.13; HIM).
- **Datos ausentes:** ninguno es material.
- **Fundamento:** no procede, porque la conclusión no es favorable.
- **Zona:** caro en todas mis variantes.

**Cubo provisional: No. Conclusión provisional: descartar.**

## 6. Datos ausentes (S-19)

Revisé los 29 datos y ninguno es material (`alguno_material = false`):

- Los ceros pendientes no tocan las anclas de cinco años. Los de 2016–2017 hacen no comparable el ROIC de 2017, y eso refuerza C18 = No.
- Los minoritarios no entran en el motor A.
- Mercado, cuotas, competidores, I+D, regulación y online no mueven el NORMAL ni la zona.
- Profi, Tesco, el capex por destino y el reparto entre precio y volumen afectan al S2C y al crecimiento. En el tornado, el S2C mueve 0,28 € y el crecimiento 1,21 €.
- Calificaciones, covenant y ciberataque no cambian la quiebra, con deuda neta/EBITDA de 2,2 y liquidez de 3.115 más 1.500.
- Insiders y firmantes: la gestión se juzga por diez años de historial.

## 7. Fundamento material (D10)

No hay ninguna celda técnica ni sin juicio propio, y todas las Observaciones citan hechos. Declaro dos hipótesis porque su cifra sale de un umbral, no de un hecho:

- **Palancas!C18 = 0,12**, alternativa 0,09–0,13. El suelo es comprar al ritmo de 2022–2025 (fila 31); el techo, la rentabilidad A2 del propio NORMAL.
- **Palancas!D18 = 0,12**, alternativa 0,12–0,22. El suelo es el retorno del NORMAL; el techo, la reinversión A2 del BUENO sin salto.

El efecto sobre el precio de Sí va de −1,8 % a +1,1 %. `resultado = no_procede`. No hago la comprobación conjunta (`sobrevive = null`).

## 8. Lo que más condiciona

Lo que más condiciona es Palancas!C18, aunque solo mueve el precio de Sí entre 27,23 € y 27,85 €. La conclusión descartar descansa en Análisis!C18 = No, que es una hipótesis fundamentada.

Lo resolverían dos datos:

- la reinversión neta propia y las compras de 2016–2022 (Historia filas 30–31), junto con la amortización de derechos de uso, para medir en A2 el S2C y el ROIC de diez años;
- las ventas y el resultado de Tesco Chequia y Eslovaquia.

## 9. Turno 2 · comprobación conjunta, estado y conclusión

**Nota:** las secciones 9 a 15 recogen el cierre antes de responder al contradictor (No · descartar). Mandan la sección 16 y `fase_c.json`: Vigilar · esperar, con objetivo provisional.

No existe `comprobacion_conjunta.json`: con una conclusión no favorable no procedía. `sobrevive = null` y `resultado = no_procede`.

Cierre: **estado concluido (provisional hasta la auditoría) · cubo No · acción descartar**. No hay precio objetivo.

C104: «Pendiente de decisión de cartera · conclusión del personaje: descartar (No) · zona caro · precio de Sí ≤ 27.74 · precio esc. MALO 23.62 · ponderado 29.80 · fundamento no procede (conclusión no favorable)». La escalera sale de `precio.json`. El tamaño de la posición es de José Luis.

Insumos para esa decisión:
- precio 36,05 €;
- el precio de Sí está un 23,1 % por debajo del precio, y el precio esc. MALO un 34,5 % por debajo (diferencia ÷ precio);
- r 0,09 frente a una r mínima de 0,0786;
- ningún dato ausente material;
- la palanca más influyente, solo como información, es el margen.

## 10. Tesis (B101)

Ahold Delhaize vende comida en 9.551 tiendas (AR2025 PDF p. 58) y deja unos 2.000 millones al año para el accionista (C52), que reparte casi enteros (AR2025 PDF p. 56). Su escala local defiende la cuota, no el retorno. El margen IFRS va del 2,9 % al 4,4 % en diez años (fila 29). El ahorro de 1.294 vuelve al precio (AR2025 PDF p. 45). El ROIC del capital total, un 8,8 % (C55), no supera mi alternativa. El accionista rinde más sobre su capital propio porque el 85 % de los locales es arrendado: eso es renta fija, no foso. A 36,05 €, el precio pide un 11,3 % de crecimiento anual durante cinco años (C86), y queda por encima del ponderado (29,80 €) y del precio de Sí (27,74 €). No: descartar.

## 11. Tesis inversa (B102)

Mi cubo es No, así que la inversa defiende el lado contrario: el error de omisión.

1. Sin fondo de comercio el ROIC es del 12,9–13,5 % (C24), y el capital propio rindió un 14,8 % en 2021–2025 (Historia filas 7, 23 y 32).
2. Albert Heijn tiene el 38,2 % de cuota (AR2025 PDF p. 50) y Food Lion lleva 53 trimestres en positivo (AR2025 PDF p. 43).
3. La caja vuelve al dueño y hay un 29 % menos de acciones desde 2017 (fila 20).
4. La r es heredada: con la r mínima, el ROIC total la supera.
5. El BUENO (38,89 €) ya supera el precio.

No me basta. El retorno de más es apalancamiento con renta fija, el margen no ha subido en diez años y el precio exige un crecimiento que la empresa no ha tenido sin comprar. «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 12. Predicciones (dado el NORMAL)

1. El margen subyacente del Grupo en 2027 estará entre el 3,7 % y el 4,2 %. Fecha: 2028-03-31. Probabilidad: 0,7.
2. Las comparables sin gasolina del Grupo en 2027 crecerán entre el 0,5 % y el 3,5 %. Fecha: 2028-03-31. Probabilidad: 0,7.
3. La caja de explotación de 2027, menos capex, arrendamientos e intereses pagados, estará entre 1.700 y 2.400 millones. Fecha: 2028-03-31. Probabilidad: 0,65.

Las tres son del negocio y se pueden comprobar con el informe anual de 2027.

## 13. C93, C103, B222 y B223

- **C93 = Sí, se mantiene.** El g del 2 % es C45. Con un ROIC de 0,12 exige reinvertir alrededor del 17 % del resultado. El salto del NORMAL es de +1,2 puntos y el terminal pesa un 53 %.
- **C103 = No, se mantiene.** Es un negocio que hay que vigilar.
- **B222.** La hipótesis que más condiciona es Palancas!C18 (y D18): el ROIC terminal está en el tope de la tasa + 3 puntos. Mueve el precio de Sí entre 27,23 € y 27,85 €.
- **B223.** La resolverían las notas de flujos y de inmovilizado de 2016–2022 (para Historia filas 30–31 en A2), y una pregunta a Relación con Inversores por las ventas, el resultado y los arrendamientos de Tesco Chequia y Eslovaquia.

## 14. Qué me haría cambiar de cubo

- **A Vigilar, y solo después a Sí:** tres años de ROIC del capital total por encima de r, con el margen subyacente sobre el 4,4 % y el ahorro retenido.
- **Para reforzar el No:** un margen subyacente bajo el 3,8 % dos años seguidos, o un nuevo deterioro de Profi o de Stop & Shop (AR2025 PDF p. 238).
- **A Demasiado difícil:** que el precio y el surtido se decidan fuera de sus canales (AR2025 PDF p. 69), o que las compras hagan del grupo algo cuyo retorno no pueda medir.

## 15. Comparación con la etapa 1

| | Cubo | Precio de Sí | Precio de entonces |
|---|---|---|---|
| Etapa 1 (v1) | Vigilar | 23,13 € (mín(MALO, 0,75 × ponderado)) | 33,14 € |
| Ahora (v2) | No | 27,74 € (escalera k = 3, motor A en A2_propio) | 36,05 € |

El cubo difiere porque la etapa 1 llamó foso a la cuota y a la densidad. La Historia de diez años da un ROIC del capital total por debajo de r, y el ahorro se lo queda el cliente. El precio de Sí es más alto porque las tiendas arrendadas se pagan dentro de f y la regla es otra. Las dos versiones coinciden en lo esencial: a precio de mercado no hay margen. La etapa 1 acertó al ver la estructura rígida; se equivocó, creo, al llamar foso a una ventaja que no da retorno.

Confianza global: media.

## 16. Respuesta al contradictor

Objeciones de `coordinacion/cierre_v2/examen/contradictor/ahold/OBJECIONES.json`. Las cifras salen de mi réplica del motor, que reproduce el libro al céntimo; no son el recálculo oficial.

| Objeción | Respuesta | Dato | Efecto |
|---|---|---|---|
| O1 · al flujo del accionista le faltan cobros | **No rebatida.** Posible defecto de entrada o de plantilla | El estado de flujos de 2025 (AR2025 PDF p. 216) presenta en inversión los intereses cobrados (130; 196 en 2024), los cobros de subarriendos (138; 125) y los dividendos de negocios conjuntos (28; 22). La Historia fila 35, C52 y f no los suman, y sí restan los intereses pagados y todos los pagos de arrendamiento | Con f = 0,0015–0,0027 el precio de Sí queda entre 28,97 y 30,73 €. Mi incoherencia 5 del turno 1 tenía el signo equivocado. Zona caro. Cuenta para el movimiento |
| O2 · acciones de 2025 con precio de 2026 | **No rebatida.** Posible defecto de entrada o de plantilla | 865,17 millones de acciones a 27-sep-2026 (Q3-26 PDF p. 21), frente a 905 en C55. Las recompras de 2026 salieron de una caja que el motor no resta; aun así, llevando el valor a noviembre de 2026 y restando lo repartido, el efecto sigue al alza (+4–5 %) | Precio de Sí 28,94 € por sí sola; con O1, 30,23–32,07 € (ponderado 32,47–34,44 €). Zona caro. Cuenta para el movimiento |
| O3 · la prueba del foso cruza perímetros | **No rebatida** | Intereses de arrendamiento: 465 (AR2025 PDF p. 227). Tasas de deterioro después de impuestos: 5,0–6,7 % (AR2025 PDF p. 238). Con pesos de mercado, el coste del capital total es de un 7,1 % (cálculo mío), y el ROIC total (8,8 %, C55) lo supera. El 13–15 % del capital propio está medido después de pagar la renta, así que no basta con llamarlo apalancamiento | Análisis!C18 debería ser Sí (foso estrecho). No reescribo la celda. Es lo que lleva el cubo a Vigilar |
| O4 · margen del NORMAL y p(MALO) apoyados en cargos puntuales | **Rebatida** | El NORMAL usa el diferencial de 2021–2025 (0,4 puntos), que no incluye el cargo de pensiones de 2020 (Observación de Palancas!C15; AR2025 PDF p. 64). Con el redondeo del ejercicio (múltiplos de 0,005), tanto 3,6 % como 3,67 % se escriben 0,035; 0,036 y 0,0367 no son valores admitidos. p(MALO) se apoya en motivos estructurales (Observación de B69). Sin 2020, quedan 3 de 10 años con margen bajo | Ninguno. Saco 2020 del recuento |

**Regla de movimiento.** O1, O2 y O3 son válidas y no las rebato. Todas van al alza, así que la conclusión sube un escalón y solo uno: de **No · descartar** a **Vigilar · esperar**.

**Conclusión antes:** concluido · No · descartar · precio de Sí 27,74 €.

**Conclusión después:** concluido (provisional hasta la auditoría) · Vigilar · esperar · precio objetivo 27,74 €, el de `precio.json`. El objetivo es provisional: el libro tiene dos posibles defectos de entrada (O1 y O2). Si una persona los confirma y el pipeline recalcula, mi réplica deja el precio de Sí en 30,23–32,07 €. La zona seguiría en caro (precio 36,05 € frente a un ponderado de 32,47–34,44 €).

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 27.74 · zona caro · precio de Sí ≤ 27.74 · precio esc. MALO 23.62 · ponderado 29.80 · fundamento no procede (conclusión no favorable) · objetivo provisional: posible defecto de entrada en el flujo del accionista (O1) y en las acciones (O2)».

**Celdas que reescribí:** B101 (tesis de Vigilar con foso estrecho), B102 (ahora defiende el No: ahorro al cliente, renta fija, holguras de deterioro, guía de 2026 y deuda), C104, B222 y B223. También cambié la decisión, los insumos, la herencia, la comparación con la etapa 1 y qué cambiaría el cubo. C93, C103, las predicciones, las palancas y el libro no cambian; no relanzo el pipeline.

**Comparación con la etapa 1.** Ahora coincido en el cubo (Vigilar). La razón es distinta: el ROIC del capital total supera el coste del capital total, no la cuota. El precio de Sí también es otro: 27,74 € frente a 23,13 €, por el método y el perímetro.
