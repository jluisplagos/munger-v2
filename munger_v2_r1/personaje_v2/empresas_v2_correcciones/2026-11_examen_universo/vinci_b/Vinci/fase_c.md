# Fase C · turno 1 (tras la vuelta a la fase B; corrección 1 de la auditoría) · VINCI SA (DG) · motor B

**Corrección 1 (auditoría REPETIR).** Corrijo cuatro cosas:
- **Rango de B15:D15 (punto 5).** Evalúo el rango defendible entero y ya no presento «esperar con 97,79 €» como conclusión sostenida.
- **§7 y §8 (punto 5).** Los alineo con `fase_c.json`: `hay_base = true`, frontera de ≈2,1 mil M.
- **Insiders (punto 9).** Anoto la evidencia de la URD que no había usado: C97 y la etapa 1.
- **Datos ausentes (aviso del punto 16).** Mido su materialidad también contra la conclusión favorable y el objetivo.

Las secciones de conclusión del turno 2 (antes §9–§13) se reescribirán en el turno 2. Allí corregiré la cita del punto 6, que debe ir como (TCI p.95; HIM), y la frase sobre los insiders de la v1. La respuesta al contradictor se conserva, salvo lo que corrige la auditoría.

La fase B ya usó la única vuelta: en este turno no pido otra (`revisar_palancas = false`). Cambió B15:D15 de 0,095 / 0,10 / 0,105 a 0,085 / 0,09 / 0,10, por los minoritarios, y C16 de 1,7 a 1,5, por la mezcla de la reinversión.

Libro recalculado, con p = 0,25 / 0,6 / 0,15:
- MALO 79,28 €
- NORMAL 101,75 €
- BUENO 174,47 €
- ponderado 107,04 €

Escalera (`precio.json`):
- precio de Sí: 97,79 €, sin tope del NORMAL;
- precio del escenario MALO: 79,28 €;
- zona: `caro`.

El precio de 107,05 € está un 9,5 % por encima del precio de Sí (9,26 ÷ 97,79; denominador: el precio de Sí). Dicho al revés, el precio de Sí está un 8,7 % por debajo del precio (9,26 ÷ 107,05; denominador: el precio). La regla antigua (C156) da 79,28 €.

Lo reviso como si fuera de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

**Lo que coincide.**
- Los semáforos de las filas 40–44 y 47 pasan.
- El peso del terminal es 0,60 / 0,68 / 0,72.
- El salto del año 11 es de 1,5 / 2,2 / 5,6 puntos.
- La rentabilidad marginal del NORMAL es 9,2 %, y el valor de su crecimiento, −1,8 € por acción. La historia NORMAL de la fase A ya cuenta lo mismo que la hoja: crecer reinvirtiendo en torno a r sin crear mucho valor.
- Mi réplica del motor B reproduce los nuevos B78:D78 al céntimo.
- El recorte por minoritarios está bien hecho: cada −0,001 de margen resta ≈811 / 975 / 1.293 M, y la fase B aplicó −0,008 / −0,008 / −0,007 para excesos de ≈6,5 / 7,9 / 8,8 mil M.
- El S2C 1,5 sale de la mezcla de 2023–2025: 77 % compras al 6,9 % de Airports y 23 % propio al 16,1 % de Energy Solutions, ≈9 % [cálculo].
- La fase A dijo Vigilar y que a 107,05 € no veía margen. Ahora el libro dice lo mismo.

**El DCF inverso.** El precio descuenta ≈5,4 % de crecimiento de ventas en los años 1–5 (C86). El NORMAL pone el 4 % (2,5 % orgánico + 1,5 % de compras), y el orgánico de 2025 fue del 2,6 % (URD 2025 PDF p. 130). El precio pide más que mi escenario central.

**El tornado** (información): ±1 punto de tasa mueve ±45,5 €; ±2 puntos de margen, ±35,1 €. El valor depende sobre todo de la rentabilidad exigida (r heredada, 9 %, por debajo de la r mínima de 9,08 %).

**Lo que no cuenta la misma historia.**

1. **La base del recorte por minoritarios.** La fase B capitaliza 805 de dividendos a r − g. Pero son dividendos, no resultado. El valor contable de los minoritarios bajó de 4.085 a 3.576 mientras cobraban 805 y 902 (URD 2025 PDF p. 358, 399). Eso apunta a que cobran más de lo que ganan, y entonces el recorte sería menor. Lo calculé con la réplica [cálculo]:
   - con medio recorte (0,09 / 0,095 / 0,10), el precio de Sí sería ≈104,9 € y la zona `vigilar`;
   - sin recorte, 113,3 € y `cumple_regla_k`.

   La frontera de la acción es un exceso de ≈2,1 mil M sobre los 3.576 contables, calculado con los márgenes equivalentes exactos (0,093 / 0,098 / 0,107) y C16 1,5 [cálculo]. El ≈3,45 mil M que di antes salía de márgenes ya redondeados. La nota 23.5 (texto/vinci-urd-2025.txt PDF p. 399) da 1,1 / 1,7 / 2,1 mil M, justo alrededor de esa frontera. Lo desarrollo en el punto 6 de esta lista.
2. **La vara de la reinversión.** El MALO rinde 7,5 %, por debajo de r pero por encima de la tasa del motor (6,41 %). En la hoja, su reinversión de los años 1–10 crea algo de valor, al revés de su historia. No es una palanca mal derivada, porque la tasa es convención de la plantilla. Con S2C 1,0 el MALO bajaría a ≈75,1 € y el precio de Sí a ≈95,7 € [cálculo]: la acción no cambia.
3. **«Cuánto pagas por crecer».** El valor sin crecimiento (103,58 €) lleva para siempre las autopistas y no resta a los minoritarios. Queda por encima del NORMAL, así que el «⚠» de la hoja no es una lectura del negocio.
4. **Zona en el filo.** El ponderado está a un céntimo del precio. Además, esa zona descansa sobre un B15:D15 que queda fuera de su rango defendible (punto 6): no la leo como conclusión.
5. **Tras el contradictor.** Hay tres datos mal medidos:
   - el recorte por minoritarios capitaliza dividendos que son 2,2 veces el resultado (PDF p. 356, 358, 399);
   - el t de Historia C52 incluye 388 M de diferidos sin caja de 2021 (texto/vinci-urd-2021.txt PDF p. 67);
   - el coste de la deuda de C63 es neto de lo que rinde la caja (PDF p. 138, 356).

   C52 y C63 son celdas de datos, y la vuelta a la fase B ya se gastó.
6. **El rango defendible entero de B15:D15 (corrección 1).** El rango es 0,0878–0,093 / 0,0936–0,098 / 0,1037–0,107, y el libro (0,085 / 0,09 / 0,10) queda por debajo de sus dos límites. Con la réplica [cálculo]:
   - en el límite bajo, el precio de Sí es ≈103,2 € (C16 1,5) o ≈102,5 € (C16 1,4), zona `vigilar`;
   - con el redondeo de la hoja (0,09 / 0,095 / 0,105), ≈106,1 / 105,4 €, zona `vigilar`;
   - en el límite alto, ≈110,9 / 110,1 €, zona `cumple_regla_k`;
   - con O2 mínima y O3 al 4,4 %, ≈100,2–100,9 € en el límite bajo y ≈107,7–108,4 € en el alto, todavía por encima de 107,05 €.

   Dentro del rango que yo mismo doy por defendible, la acción cambia. El objetivo del libro (97,79 €) queda fuera del rango de precio de Sí (≈100–111 €). La palanca es de la fase B, está mal derivada por su base y no admite otra vuelta. Un error no se aprueba con una explicación (D17): no sostengo «esperar con 97,79 €».
7. **Insiders: C97, celda de la fase A (corrección 1).** La URD 2025 (texto/vinci-urd-2025.txt PDF p. 180, §4.4.2) registra las operaciones de 2025: Huillard vendió 29.365 acciones, Labeyrie (CFO) 52.038 y Bertocco Trindade compró 1.000, el mínimo estatutario de la consejera (§4.4.1). La URD 2024 (PDF p. 181, §4.3.2) registra que en 2024 vendieron Huillard (41.999), Coppey (29.691) y Labeyrie (60.162).
   - Solo hay año, no fechas: no puedo situarlas en la ventana de 12 meses anterior al 10-oct-2026 (solo el último trimestre de 2025 cae dentro). El semestral de 2026 no trae operaciones.
   - El patrón es de ventas anuales de los directivos: con esa evidencia, C97 estaría más cerca de «Vendiendo» que de «Neutral». En la fase A dije que no había operaciones porque no estaban en mis entradas, pero estaban en los textos de la carpeta.
   - No reescribo C97: va a `celdas_corregidas` con `despues = antes`.
   - Efecto: no es un descalificador. Huillard conserva 336.616 acciones (URD 2025 PDF p. 148), C98 = Aceptable no cambia y ninguna palanca depende de C97. Resta confianza en la alineación de la dirección y va a la tesis inversa. Por sí sola no impide una conclusión favorable.

## 2. Desviaciones pendientes

Queda solo G8 en el BUENO: 5,6 puntos, ya justificada por la fase B y que repito con hechos (clase fundamentada).

En los años 1–10, el capital nuevo del BUENO rinde 15,6 % por dos razones:
- Energy Solutions vende 29,6 mil M con 9,5 mil M de capital, ≈16 % después de impuestos (URD 2025 PDF p. 134, 136, 141);
- las tarifas aprobadas suben ventas sobre activos ya construidos: OMA a inflación + 6,9 % y la segunda pista de Gatwick (PDF p. 132).

En el año 11, sin foso (C18 = No), la competencia y el precio de las concesiones nuevas lo llevan a r + 1. Solo lo sostienen los aeropuertos en plena propiedad y las concesiones largas (PDF p. 382).

«The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM): aquí, diez años. Va en la tesis.

G16 y G17 no están pendientes.

## 3. Mover palancas

No pido otra vuelta: el pipeline solo admite una, y otra terminaría en `no_entregable`.

Revisé las palancas nuevas y ninguna está mal derivada:
- el recorte y el S2C cuadran con su aritmética;
- el orden MALO ≤ NORMAL ≤ BUENO se mantiene;
- los redondeos van al múltiplo de 0,005 más cercano.

La aritmética cuadra, pero la base no: tras el contradictor y la auditoría (corrección 1), B15:D15 queda fuera de su rango defendible. Es una palanca mal derivada, la vuelta ya se gastó y no puedo corregirla. Corregirla cambia la zona y mueve el precio de Sí más de un 5 %, así que no puedo dejarla como si nada: va al fundamento material (punto 7). En `celdas_corregidas` registro B15, C15, D15, C16 y C97 con `despues = antes`.

## 4. Autocomprobación

Las diez tendencias están en `fase_c.json`. Destaco tres.

- **Anclaje.** El MALO coincide ahora con el «≈79 €» de la etapa 1, y el ponderado con el precio. Comprobé que las dos coincidencias salen de fórmulas con hechos de este expediente, no de esas cifras.
- **Consistencia.** La vuelta que pedí confirmaba mi Vigilar de la fase A. Con el rango defendible entero ya no lo confirma: no presento «esperar con 97,79 €» como conclusión sostenida.
- **Lo no numerable.** Pesan sin celda la negociación política del fin de las autopistas, el litigio de la TEITLD y los bonos canjeables en ADP (semestral PDF p. 6), además de la duda sobre los minoritarios. «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM).

## 5. Cubo y conclusión provisionales

Recorro el orden de mando:
1. Bloqueo: no hay; la gramática da código 0.
2. Límite del modelo: no hay.
3. Descalificadores: ninguno. La deuda está en 1,4 veces el Ebitda, con calificación A−, y las piezas las entiendo por partes: «It's not a competency if you don't know the edge of it» (TCI p.100; HIM). El borde es Cobra IS.
4. Datos ausentes materiales: ninguno (punto 6).
5. Fundamento material: B15:D15 está fuera de su rango defendible. Dentro del rango, la parte alta cumple la regla de precio, así que la conclusión favorable es una candidata real y se somete a D10 (punto 7).
6. Zona del libro: `caro`, pero descansa sobre el B15:D15 mal derivado.

**Cubo provisional: Vigilar. Conclusión provisional: `comprar`**, solo como candidata de la parte alta del rango, sometida a la comprobación conjunta. No hay compra ni objetivo mientras D10 no lo resuelva. Si la combinación no sobrevive, el turno 2 cerrará sin conclusión.

Es el caso de un negocio correcto, con un foso que caduca por contrato, a un precio que paga más que el escenario central. «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM).

## 6. Datos ausentes (S-19)

Revisé los trece datos uno a uno, frente a la conclusión favorable y frente al precio objetivo (aviso del punto 16). Ninguno es material:
- **Evidencia de arrendamientos y ceros de 2016–2018:** no tocan el motor B ni las medias de 2021–2025, y los 2.849 de 2025 los confirma el extracto (PDF p. 396).
- **Subidas de peaje de ASF y Escota:** mueven entre −2,8 y +2,0 € [cálculo].
- **Flujos de fin de contrato:** mueven ≈4,2 €, dentro de límites atados a hechos (2,7–3,0 mil M). Ambos pesan menos que el rango de ≈8 € que abre B15:D15, que es lo que decide.
- **Múltiplos de compra:** ya están medidos por el capital empleado por negocio y entran en la mezcla del S2C.
- **Mercado, I+D, tipo constante, dividendos regulados y calendario climático:** no mueven ninguna palanca en su redondeo.

`alguno_material = false`.

## 7. Fundamento material (D10)

Hay una hipótesis sin fundamento suficiente en el libro: **Palancas!B15:D15, el recorte por minoritarios.** Capitaliza 805 de dividendos (PDF p. 358) cuando el resultado atribuido fue 372 M (PDF p. 356, 138), 338 M en las tres filiales (nota 23.5, PDF p. 399).

Sí tiene alternativas defendibles (`hay_base = true`), con los dos límites atados a hechos de VINCI:
- **Límite bajo del margen** (recorte mayor): los precios que VINCI pagó por el control, con prima de control: Gatwick 3.080 por el 50,01 % (texto/vinci-annual-report-2019.txt PDF p. 302), OMA 1.169 por el 29,99 % (URD 2023 PDF p. 170) y Edimburgo 1.431 por el 50,01 % (URD 2025 PDF p. 370). Dan un exceso de 4.254 M y márgenes de 0,0878 / 0,0936 / 0,1037.
- **Límite alto** (sin recorte): la caja libre atribuida a los minoritarios, ≈207 M (nota 23.5), apenas llega a su valor contable. Márgenes de 0,093 / 0,098 / 0,107.

Las demás palancas, las probabilidades, la quiebra, el motor, la base del margen, el caso especial y las narrativas citan hechos.

Con `comprar` candidata y la hipótesis acotada, **procede la comprobación conjunta**. Va una sola combinación en el extremo adverso del rango, con el redondeo de la hoja:
- B15 = 0,09, C15 = 0,095 y D15 = 0,105;
- C16 = 1,4, porque el S2C del NORMAL baja con el margen por la regla de la fase B (0,09 ÷ (0,095 × 0,68) = 1,39).

El orden de los escenarios se mantiene. Historia C52 y C63 (O2, O3) no pueden entrar: son celdas de datos. `sobrevive` lo dirá el script, y lo dejo en `null`. Mi réplica anticipa un precio de Sí de ≈105,4 € y zona `vigilar`, pero eso lo decide la copia recalculada, no yo.

## 8. Lo que más condiciona y lo que lo resolvería

**Hipótesis:** el recorte por minoritarios de B15:D15, fuera de su rango defendible. Dentro del rango, el precio de Sí va de ≈102,5 a ≈110,9 € y la acción cambia en una frontera de ≈2,1 mil M de exceso. Historia C52 y C63 mueven además ≈+4,0 y ≈−5,9 €.

**Lo resolvería:**
- rehacer B15:D15 en un ciclo nuevo con el resultado atribuido de la nota 23.5 (URD 2025 PDF p. 399: 144 / 143 / 51 M en Gatwick, OMA y Edimburgo) y recalcular el libro y la escalera;
- que la persona responsable decida sobre las celdas de datos C52 (URD 2021 PDF p. 67) y C63 (URD 2025 PDF p. 138, 356).

## Respuesta al contradictor

He comprobado las tres objeciones en los textos de la carpeta y con mi réplica del motor, que reproduce el libro al céntimo.

| Objeción | Respuesta | Efecto |
|---|---|---|
| **O1 · sube** · los socios de los aeropuertos cobran más del doble de lo que ganan | **No rebatida.** La nota 23.5 da un resultado atribuido de 144 / 143 / 51 M en Gatwick, OMA y Edimburgo (texto/vinci-urd-2025.txt PDF p. 399). En el grupo son 372 M (410 en 2024; PDF p. 356, 138), frente a 805 M de dividendos (PDF p. 358). El dato que di por ausente estaba en los textos de la carpeta, aunque no en el extracto. Mi frontera de ≈3,45 mil M salía de márgenes ya redondeados; con los equivalentes exactos es ≈2,1 mil M [cálculo]. Incluso con los precios de compra, que llevan prima de control (Gatwick 3.080 por el 50,01 %, texto/vinci-annual-report-2019.txt PDF p. 302), el recorte del libro es demasiado grande. | Precio de Sí de 97,79 a ≈105,4 € (márgenes 0,09 / 0,095 / 0,105 y S2C 1,4) o ≈107,5 € sin redondear; ≈102,5 € en el extremo de los precios de compra [cálculo]. **Un escalón al alza.** |
| **O2 · sube** · el tipo impositivo «para siempre» incluye un apunte sin caja | **Rebatida en parte.** La historia NORMAL deja los impuestos especiales como coste (fase_a.md §8), y la empresa espera en 2026 una carga de la misma magnitud que la de 2025 (texto/vinci-urd-2025.txt PDF p. 143; 323 M en el semestre, semestral PDF p. 12): la contribución de 2025 no se quita. **No rebatida en lo de 2021:** los 388 M de diferidos de Gatwick tuvieron impacto nulo en caja (texto/vinci-urd-2021.txt PDF p. 67) y pesan en Historia C52, una celda de datos que no cambio. | Versión mínima (t = 0,2999): precio de Sí ≈101,8 € (+4,0) [cálculo]. Al alza, en el mismo escalón que O1: como mucho uno por dirección. |
| **O3 · baja** · la caja cuenta dos veces en la tasa del motor | **No rebatida.** La deuda bruta costó 1.760 M y la caja rindió 513 M (texto/vinci-urd-2025.txt PDF p. 356). El tipo medio de la deuda bruta a largo plazo fue del 4,4 % (PDF p. 138). Historia C63 (3,69 %) usa Net interest paid, neto de lo cobrado (datos_v63 §3, fila «intereses»), mientras el motor resta la caja entera. La financiación nueva al 3,2 % (semestral PDF p. 6) incluye bonos canjeables al 0,75 %, y el coste medio del semestre fue del 4,5 % (misma página): no la rebate. | Con un coste de la deuda del 4,4 %: precio de Sí ≈91,9 € (−5,9) [cálculo]. **Un escalón a la baja.** |

**Las tres juntas.** Con O1, O2 en su versión mínima y O3 al 4,4 %, el precio de Sí queda en ≈103,0–105,1 € y la zona en `vigilar` [cálculo]. Con O3 al 4,83 % baja a ≈101,4–103,5 €, y con O1 en su extremo adverso, a ≈100,2 €. Corrección 1: eso solo vale para las combinaciones elegidas. En el límite alto del rango defendible de B15:D15, aun con O2 y O3, el precio de Sí es ≈107,7–108,4 € y la regla de precio se cumple: dentro del rango, la acción sí cambia.

**Regla de movimiento.** Hay un escalón al alza (O1 y O2) y uno a la baja (O3): se compensan. Pero la auditoría (punto 5) muestra que la acción no está determinada dentro del rango defendible, y que el objetivo de 97,79 € queda fuera de él.

**Conclusión tras la corrección 1:** ya no es «concluido · Vigilar · esperar». Es una conclusión provisional `comprar` (candidata), con cubo provisional Vigilar, que se somete a la comprobación conjunta. La conclusión la fija el turno 2.

El precio de Sí del libro (97,79 €) queda fuera del rango que doy por defendible, así que no lo emito como objetivo.

**Cambios en `fase_c.json`.**
- Nuevo bloque `respuesta_contradictor`.
- Una incoherencia nueva.
- La hipótesis de B15:D15 pasa a tener base. Rango por margen: MALO 0,0878–0,093, NORMAL 0,0936–0,098 y BUENO 0,1037–0,107. El libro queda por debajo de los dos límites.
- Actualizados `hipotesis_que_mas_condiciona`, `que_lo_resolveria`, B222, B223, C104 con su Observación, la condición de revisión al alza, el fundamento de los insumos, el rango de la escalera y el paso a Sí.

Lo demás no cambia.

**Lo que resolvería todo.** Rehacer B15:D15 con la nota 23.5 en un ciclo nuevo. Y que la persona responsable decida sobre las celdas de datos Historia C52 (tipo impositivo) y C63 (coste de la deuda), y después recalcular el libro.
