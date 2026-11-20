# Fase C · turno 1 (tras la vuelta a la fase B) · VINCI SA (DG) · motor B

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

   La acción `esperar` aguanta mientras el exceso sobre los 3.576 contables pase de ≈3,45 mil M. Los dividendos y los precios de compra de OMA y Edimburgo (4.159 para la parte ajena de solo dos filiales) apuntan por encima. El precio objetivo sí depende de esta hipótesis, y no hay otra vuelta a la fase B: lo marco como provisional.
2. **La vara de la reinversión.** El MALO rinde 7,5 %, por debajo de r pero por encima de la tasa del motor (6,41 %). En la hoja, su reinversión de los años 1–10 crea algo de valor, al revés de su historia. No es una palanca mal derivada, porque la tasa es convención de la plantilla. Con S2C 1,0 el MALO bajaría a ≈75,1 € y el precio de Sí a ≈95,7 € [cálculo]: la acción no cambia.
3. **«Cuánto pagas por crecer».** El valor sin crecimiento (103,58 €) lleva para siempre las autopistas y no resta a los minoritarios. Queda por encima del NORMAL, así que el «⚠» de la hoja no es una lectura del negocio.
4. **Zona en el filo.** El ponderado está a un céntimo del precio. Entre `caro` y `vigilar` la acción es la misma.

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

La duda que queda es de base (dividendos frente a resultado), no de cálculo. Va al fundamento material y marca el objetivo como provisional. En `celdas_corregidas` registro B15, C15, D15 y C16 con `despues = antes`.

## 4. Autocomprobación

Las diez tendencias están en `fase_c.json`. Destaco tres.

- **Anclaje.** El MALO coincide ahora con el «≈79 €» de la etapa 1, y el ponderado con el precio. Comprobé que las dos coincidencias salen de fórmulas con hechos de este expediente, no de esas cifras.
- **Consistencia.** La vuelta que pedí confirma mi Vigilar de la fase A. Reconozco la parte débil del recorte y la dejo como hipótesis sin base, sin darla por firme.
- **Lo no numerable.** Pesan sin celda la negociación política del fin de las autopistas, el litigio de la TEITLD y los bonos canjeables en ADP (semestral PDF p. 6), además de la duda sobre los minoritarios. «practically everybody (1) overweighs the stuff that can be numbered» (PCA pp.412–414; HIM).

## 5. Cubo y conclusión provisionales

Recorro el orden de mando:
1. Bloqueo: no hay; la gramática da código 0.
2. Límite del modelo: no hay.
3. Descalificadores: ninguno. La deuda está en 1,4 veces el Ebitda, con calificación A−, y las piezas las entiendo por partes: «It's not a competency if you don't know the edge of it» (TCI p.100; HIM). El borde es Cobra IS.
4. Datos ausentes materiales: ninguno.
5. Fundamento material: no limita una conclusión no favorable.
6. Zona: `caro`.

**Cubo provisional: Vigilar. Conclusión provisional: `esperar`**, con el precio de Sí (97,79 €) como objetivo. Ese objetivo es provisional porque lo condiciona el recorte por minoritarios (punto 7): ≈104,9 € con la mitad del recorte.

Es el caso de un negocio correcto, con un foso que caduca por contrato, a un precio que paga más que el escenario central. «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM).

## 6. Datos ausentes (S-19)

Revisé los trece datos uno a uno. Ninguno es material para `esperar` con precio objetivo, porque ninguno cambia la acción:
- **Evidencia de arrendamientos y ceros de 2016–2018:** no tocan el motor B ni las medias de 2021–2025, y los 2.849 de 2025 los confirma el extracto (PDF p. 396).
- **Subidas de peaje de ASF y Escota:** mueven entre −2,8 y +2,0 € [cálculo].
- **Flujos de fin de contrato:** mueven ≈4,2 €. Ambos quedan muy por debajo de los 9,26 € que separan el precio de Sí del precio.
- **Múltiplos de compra:** ya están medidos por el capital empleado por negocio y entran en la mezcla del S2C.
- **Mercado, I+D, tipo constante, dividendos regulados y calendario climático:** no mueven ninguna palanca en su redondeo.

`alguno_material = false`.

## 7. Fundamento material (D10)

Hay una hipótesis sin base: **Palancas!B15:D15, el tamaño del recorte por minoritarios.**
- La clase es fundamentada (confianza baja), pero ningún hecho acota el tamaño del recorte.
- No tiene alternativas defendibles (`hay_base = false`). Por arriba, nada prueba que 805 sea el flujo sostenible. Por abajo, los precios de compra llevan prima de control y no conozco la parte de Gatwick en los 3.576.

Las demás palancas, las probabilidades, la quiebra, el motor, la base del margen, el caso especial y las narrativas citan hechos.

Con `esperar`, el resultado es `no_procede` y no hago la comprobación conjunta: la sensibilidad del punto 1 ya da el rango del precio de Sí (≈97,8–104,9 € entre el recorte entero y la mitad). En el turno 2, C104 marcará el objetivo como provisional, condicionado a esta hipótesis.

## 8. Lo que más condiciona y lo que lo resolvería

**Hipótesis:** el tamaño del recorte por minoritarios en B15:D15, que mueve el objetivo entre ≈97,8 y ≈104,9 €. Solo cambiaría la acción si el exceso bajara de ≈3,45 mil M.

**Lo resolvería:** la nota de intereses minoritarios del URD 2025: resultado neto, dividendos, deuda neta y flujo de London Gatwick, Edimburgo y OMA atribuidos a los minoritarios en 2023–2025. Con eso, el recorte se calcula sobre el resultado y no sobre los dividendos.

## 9. Turno 2 · conclusión

No hay `comprobacion_conjunta.json`, porque con `esperar` no procedía: `sobrevive = null`.

**Estado `concluido`, provisional hasta la auditoría. Cubo Vigilar. Acción `esperar`, con precio objetivo 97,79 €**, el precio de Sí de `precio.json`.

El objetivo es provisional porque lo condiciona el recorte por minoritarios de B15:D15. Con medio recorte sería de ≈104,9 € [cálculo]. Es una sensibilidad condicional, no un intervalo de confianza.

`fundamento_material.resultado = no_procede`. C104 lleva «fundamento no procede (conclusión no favorable)» y la marca del objetivo provisional, sin ningún porcentaje: el tamaño de la posición es de José Luis.

Insumos para la decisión de cartera:
- zona `caro`;
- el precio está un 9,5 % por encima del precio de Sí (denominador: el precio de Sí) y un 35 % por encima del MALO (denominador: el MALO);
- r 9 % frente a una r mínima de 9,08 %;
- palanca más influyente: la tasa de descuento;
- datos ausentes materiales: ninguno.

Lo digo con sus palabras: no lo compraría «at the prices then prevailing» (PCA p.267; HIM). Y sin prisa: «Missing out on some opportunity never bothers us» (TCI p.57; HIM).

## 10. Tesis y tesis inversa

**Tesis (B101).** VINCI cobra peajes y tasas por infraestructuras sin sustituto cercano y vende servicios con poco capital (FCF de 7.010 M€, deuda neta de 1,4 veces el Ebitda, A−). Su mejor activo vuelve al Estado entre 2032 y 2036, y lo que compra para sustituirlo rinde ≈7 % después de impuestos. Una parte del flujo de los aeropuertos es de sus socios (805 M€ de dividendos en 2025). A 107,05 € el precio pide un 5,4 % de crecimiento de ventas al año, más que mi caso central. Espero, con un precio de Sí de 97,79 € todavía provisional.

**Tesis inversa (B102).** Defiendo el No con cinco hechos:
1. La joya se gasta: las autopistas dan 3.311 de Ebit y 2,6 mil M de FCF y vuelven al Estado.
2. El Estado cobra antes del final: TEITLD y una contribución excepcional repetida.
3. La parte del accionista es menor de lo que parece: minoritarios, circulante y pagos en acciones.
4. El capital se asigna caro: compras sin múltiplos publicados, Cobra IS con FCF negativo y recompras por encima del precio.
5. El precio ya está en el ponderado.

Es el negocio en el que «all the excess cash must be reinvested» (PCA p.110; HIM) para no encoger.

**C93 = Sí.** Un g del 2 % < rf con reposición a ≈7 % (lo que rinde hoy lo comprado) es sostenible, con un salto de 2,2 puntos y un peso del terminal de 0,68. **C103 = No**: el activo principal caduca por contrato.

## 11. Predicciones (dado el NORMAL)

Las tres se comprueban el 2028-03-31, con el informe anual 2027:
1. **Ventas de Energy Solutions en 2027 ≥ 32.000 M€** (29.612 en 2025). Probabilidad: 0,65.
2. **ROCE del grupo en 2027 entre el 9,0 % y el 11,5 %** (10,7 % en 2025). Probabilidad: 0,7.
3. **Ingresos de VINCI Autoroutes en 2027 ≤ 7.100 M€** (6.733 en 2025). Probabilidad: 0,75.

## 12. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo del precio de Sí, con la nota de minoritarios resolviendo B222 y con fundamento para la compra (D10).
- **A No:** compras a retornos por debajo de la tasa del motor, deterioros en Cobra IS o en aeropuertos, o una carga fiscal permanente que lleve el resto del grupo por debajo del 8 % de margen.
- **A Demasiado difícil:** que el valor pase a depender de la negociación política del fin de las autopistas o del EPC de Cobra IS.

## 13. Comparación con la etapa 1

El cubo es el mismo: Vigilar. El precio de Sí pasa de ≈79 € a 97,79 €.

La diferencia está en la regla, no en la valoración. La regla antigua (mín(MALO, 0,75 × ponderado)) da en este libro 79,28 € (C156), casi lo mismo que la v1. La v2 aplica la escalera k = 3 (D11) a tres escenarios calculados por la hoja, y descuenta la parte de los socios de los aeropuertos, que la v1 no restaba.

Las cifras de la v1 (FCF base 4.382 y 567,06 M de acciones) no están vigentes. Sus ventas de directivos no están en mis entradas.

## Respuesta al contradictor

He comprobado las tres objeciones en los textos de la carpeta y con mi réplica del motor, que reproduce el libro al céntimo.

| Objeción | Respuesta | Efecto |
|---|---|---|
| **O1 · sube** · los socios de los aeropuertos cobran más del doble de lo que ganan | **No rebatida.** La nota 23.5 da un resultado atribuido de 144 / 143 / 51 M en Gatwick, OMA y Edimburgo (texto/vinci-urd-2025.txt PDF p. 399). En el grupo son 372 M (410 en 2024; PDF p. 356, 138), frente a 805 M de dividendos (PDF p. 358). El dato que di por ausente estaba en los textos de la carpeta, aunque no en el extracto. Mi frontera de ≈3,45 mil M salía de márgenes ya redondeados; con los equivalentes exactos es ≈2,1 mil M [cálculo]. Incluso con los precios de compra, que llevan prima de control (Gatwick 3.080 por el 50,01 %, texto/vinci-annual-report-2019.txt PDF p. 302), el recorte del libro es demasiado grande. | Precio de Sí de 97,79 a ≈105,4 € (márgenes 0,09 / 0,095 / 0,105 y S2C 1,4) o ≈107,5 € sin redondear; ≈102,5 € en el extremo de los precios de compra [cálculo]. **Un escalón al alza.** |
| **O2 · sube** · el tipo impositivo «para siempre» incluye un apunte sin caja | **Rebatida en parte.** La historia NORMAL deja los impuestos especiales como coste (fase_a.md §8), y la empresa espera en 2026 una carga de la misma magnitud que la de 2025 (texto/vinci-urd-2025.txt PDF p. 143; 323 M en el semestre, semestral PDF p. 12): la contribución de 2025 no se quita. **No rebatida en lo de 2021:** los 388 M de diferidos de Gatwick tuvieron impacto nulo en caja (texto/vinci-urd-2021.txt PDF p. 67) y pesan en Historia C52, una celda de datos que no cambio. | Versión mínima (t = 0,2999): precio de Sí ≈101,8 € (+4,0) [cálculo]. Al alza, en el mismo escalón que O1: como mucho uno por dirección. |
| **O3 · baja** · la caja cuenta dos veces en la tasa del motor | **No rebatida.** La deuda bruta costó 1.760 M y la caja rindió 513 M (texto/vinci-urd-2025.txt PDF p. 356). El tipo medio de la deuda bruta a largo plazo fue del 4,4 % (PDF p. 138). Historia C63 (3,69 %) usa Net interest paid, neto de lo cobrado (datos_v63 §3, fila «intereses»), mientras el motor resta la caja entera. La financiación nueva al 3,2 % (semestral PDF p. 6) incluye bonos canjeables al 0,75 %, y el coste medio del semestre fue del 4,5 % (misma página): no la rebate. | Con un coste de la deuda del 4,4 %: precio de Sí ≈91,9 € (−5,9) [cálculo]. **Un escalón a la baja.** |

**Las tres juntas.** Con O1, O2 en su versión mínima y O3 al 4,4 %, el precio de Sí queda en ≈103,0–105,1 € y la zona en `vigilar` [cálculo]. Con O3 al 4,83 % baja a ≈101,4–103,5 €, y con O1 en su extremo adverso, a ≈100,2 €. En ninguna combinación el precio (107,05 €) queda por debajo del precio de Sí.

**Regla de movimiento.** Hay un escalón al alza (O1 y O2) y uno a la baja (O3): se compensan. **Conclusión final: `concluido` (provisional hasta la auditoría) · Vigilar · `esperar`.**

El precio objetivo oficial sigue siendo el precio de Sí de `precio.json` (97,79 €), porque el libro no se ha recalculado. Queda marcado como provisional. Con las objeciones no rebatidas sería de ≈103–105 €: es una sensibilidad condicional, no un intervalo de confianza.

**Cambios en `fase_c.json`.**
- Nuevo bloque `respuesta_contradictor`.
- Una incoherencia nueva.
- La hipótesis de B15:D15 pasa a tener base. Rango por margen: MALO 0,0878–0,093, NORMAL 0,0936–0,098 y BUENO 0,1037–0,107. El libro queda por debajo de los dos límites.
- Actualizados `hipotesis_que_mas_condiciona`, `que_lo_resolveria`, B222, B223, C104 con su Observación, la condición de revisión al alza, el fundamento de los insumos, el rango de la escalera y el paso a Sí.

Lo demás no cambia.

**Lo que resolvería todo.** Rehacer B15:D15 con la nota 23.5 en un ciclo nuevo. Y que la persona responsable decida sobre las celdas de datos Historia C52 (tipo impositivo) y C63 (coste de la deuda), y después recalcular el libro.
