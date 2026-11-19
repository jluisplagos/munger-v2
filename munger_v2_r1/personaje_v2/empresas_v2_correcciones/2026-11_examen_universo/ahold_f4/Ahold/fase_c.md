# Fase C · turno 1 · Ahold Delhaize (AD) · 2026-11-19 · motor A

Reviso A y B como si fueran de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM).

## 1. Una sola historia

Lo que dice la hoja con las 52 celdas: MALO 28,40 · NORMAL 35,76 · BUENO 44,05 · ponderado 35,95 (B78:D78, C83). Precio 36,05 € (C37). Escalera de `precio.json`: precio de Sí 33,79 (P\*, sin tope del NORMAL), zona **caro**. El precio está un 6,7 % por encima del precio de Sí (diferencia ÷ precio de Sí); dicho al revés, el precio de Sí está un 6,3 % por debajo del precio (diferencia ÷ precio). El precio del escenario MALO está un 21,2 % por debajo del precio (diferencia ÷ precio). Regla antigua (C156): 26,96.

La historia de `fase_a.md` es una cadena de comida madura, con caja estable y no creciente, un foso estrecho de escala local y el ahorro que se va al cliente. La hoja cuenta lo mismo:

- **Valor sin crecimiento 34,70 €**, el mismo en los tres escenarios. Pago 1,35 € por un crecimiento que en mi NORMAL vale 1,06 € (pagas ÷ vale 1,27). Casi todo el valor es la caja de hoy.
- **Peso del terminal**: 42 % / 51 % / 55 %. Pasa: nada del valor depende de un futuro lejano exagerado.
- **Salto del año 11**: MALO −0,04 puntos, NORMAL +4,0, BUENO +4,97. El capital nuevo pasa de rendir 14,0 % a 10 % en el NORMAL y de 17,0 % a 12 % en el BUENO. Es mi hipótesis: la escala local se erosiona con la inversión en precios. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). El BUENO queda justo bajo el aviso de 5 puntos. Comprobé que no se eligió por el umbral: Palancas!D16 es el S2C medio sin arrendamientos de 2025 (5,43) redondeado, y Palancas!D18 es la referencia mecánica y el máximo de 2–3 puntos a perpetuidad (MR pp. 62–63; E2).
- **DCF inverso**: el precio descuenta ≈ 3,3 % de crecimiento de ventas en los años 1–5 con el resto de mi NORMAL. Es más que mi 3 %, que el CAGR de tres años (2,0 %, Historia!C45) y que las comparables de 39 semanas de 2026 (1,4 % [Q3-26 PDF p. 3]). El precio de Sí corresponde a ≈ 0,7 %.
- **Tornado** (información, no criterio): manda el margen (±2 puntos → ±19,67 € en el NORMAL). Después vienen la tasa (±1 punto → 5,94 €) y el ROIC terminal (±5 puntos → 4,60 €). El S2C casi no mueve nada (0,25 €).
- **Semáforos**: todos pasan; la cuota implícita no se calcula porque C24 está vacía. D84 y D85 marcan poco margen y asimetría débil, coherentes con «caro».
- **A6** dice «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar porque C13 = No dice que el valor no se ve sin la hoja, no que el negocio falle. C11 y C12 son Sí y no hay descalificador.

Incoherencias anotadas. Ninguna exige mover palancas.

1. Las celdas de la fase C que hoy tiene el libro son de la etapa 1. C104 lleva un porcentaje de posición y un precio de Sí de otra escalera. B101 y B102 citan 33,14 €, 15,7 veces y un suelo de 23 €. Se reescriben en el turno 2.
2. **El MALO arranca alto.** El flujo del año 1 es 2.649. Supera el FCF base (2.312), el FCF LTM (2.150) y todo FCF del accionista de diez años (máximo 2.150). Es mecánica, no un error. El flujo sin crecimiento (2.770) parte del EBIT de 2025, 381 por encima de la media de la ventana (K3 de `motor_a_f1_resultado.md`). Con crecimiento 0 no hay reinversión. La caída viene después: 1.981 en el año 10.
3. **Tensión entre fases.** La fase A puso C8 = «Último año», como pide la regla. La fase B dice que 2025 tuvo pocos cargos. Con la media del ciclo (3,67 %), el valor bajaría ≈ 0,2–0,3 € por acción. Es menos de un 1 % del precio de Sí: ni cubo ni zona.
4. **Acciones y balance de fechas distintas** (Z-ACC, decisión registrada). Con las 865,174 M acciones de septiembre, y restando los 864 M€ que costó la recompra [Q3-26 PDF p. 16, 21], el precio de Sí sería ≈ 33,6 y el ponderado ≈ 35,9: sigue en caro y la acción no cambia (corregido tras la nota 1 del contradictor). Es un dato: no lo toco.
5. **De dónde sale el exceso de C18** (13,03 % frente a r). Es el ROIC de todo el capital (8,78 %, por debajo de r y del sector) apalancado con locales alquilados a ≈ 3,3 % antes de impuestos. La vara P-FOSO lo admite. Pero su duración depende de renovar unos 35.000 de prórrogas [AR2025 PDF p. 272]. Es coherente con dejar a perpetuidad 1 punto en el NORMAL y ninguno en el MALO.

## 2. Desviaciones pendientes

`gramatica.md` tras el recálculo no tiene ninguna desviación (G8, G16 y G17 no saltan) ni errores. Solo quedan dos avisos: P-FOSO, informativo, y A3, de fechas. `desviaciones_justificadas` queda vacía. El salto del NORMAL y del BUENO (4,0 y 4,97 puntos) lo contaré igual en la tesis: qué ventaja se pierde en el año 11.

## 3. ¿Hay que mover palancas?

No: `revisar_palancas = false`. Revisé la aritmética y el perímetro de cada palanca:

- **Margen.** MALO 3,4 % subyacente menos cargos = 3,0 %. NORMAL 4,0 − 0,4/0,5 = 0,035. BUENO 4,34 − 0,45 = 0,04. Las cuentas cuadran con los segmentos [AR2025 PDF p. 49] y con la serie de diez años [AR2025 PDF p. 64]. Los cargos se repiten: «If it happens every year like clockwork, what's so extraordinary about it?» (PCA p.119; HIM).
- **S2C.** El aviso P-FOSO dice que el MALO (3,8) queda más cerca de C54. Revisada la derivación, no está anclado en C54. Es la banda del ejercicio sobre el NORMAL del perímetro (0,75 × 5,1), con la comprobación de que el capital nuevo rinde r. Aunque fuera 5,1, el MALO no crece en los años 1–5 y cambiaría menos de 0,2 €. No es una palanca mal derivada.
- **ROIC terminal.** El MALO es igual a r, y eso no es un error de perímetro. El NORMAL (0,10) y el BUENO (0,12) quedan dentro de r + 0,03.
- **El resto.** g por debajo de rf y de r. Probabilidades de la lista y que suman 1. C22 = 0 argumentado, C76 = 0.

`celdas_corregidas` registra lo que revisé, sin cambiar valores: C18, Palancas!C8, Palancas!B16 y Palancas!C15.

## 4. Autocomprobación

La lista completa está en `fase_c.json`. Lo que más pesa:

- **Anclaje en la etapa 1.** Las tres g y las probabilidades acaban exactamente en los valores de la etapa 1. Los motivos son nuevos y el efecto es de ≤ 0,4 €.
- **Consistencia.** Probé las alternativas que más pesan, una a una:
  - probabilidades 0,3/0,6/0,1 → precio de Sí 32,14;
  - probabilidades 0,25/0,6/0,15 → 32,91;
  - probabilidades 0,1/0,6/0,3 → 35,76 (el tope del NORMAL);
  - margen NORMAL 0,04 (aproximación lineal con el tornado) → ≈ 35,9.

  En todas el precio sigue por encima del precio de Sí. Con el margen 0,04 y las acciones de septiembre, restando la caja de la recompra, sería ≈ 35,8: aún por debajo (corrijo el ≈ 36,8 de antes). Con el valor fechado al día del precio (O2), el margen 0,04 sí cruzaría el precio. La acción esperar es estrecha.
- **Historia bonita.** Parte del exceso es la financiación barata de los locales, no foso.
- **¿El MALO es malo?** En su estado estable sí: subyacente ≈ 3,4 %, por debajo de cualquier año desde 2016. Pero sus primeros años llevan más caja que la observada, y no incluye un deterioro, una compra cara ni alquileres más caros. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Doble castigo.** La renta está en la r heredada y en el MALO, no en la quiebra ni en las probabilidades (PA pp. 20–21; E6).

## 5. Cubo y conclusión provisionales

En orden de mando:

1. Bloqueo: ninguno (gramática sin errores; el estado técnico solo espera las predicciones).
2. Límite del modelo: ninguno.
3. Descalificadores: ninguno (fase A).
4. Dato ausente material: ninguno (punto 6).
5. Fundamento material: lista vacía (punto 7).
6. Zona: caro.

**Cubo Vigilar · conclusión `esperar`**, con el precio de Sí de 33,79 € como objetivo. Estoy más cerca del error de pagar la estabilidad como calidad: «is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM).

## 6. Datos ausentes (S-19)

Revisé los 29 datos uno a uno. **Ninguno es material** para esperar con precio objetivo:

- **Los dos ceros pendientes de verificación** (arrendamientos 2016–2017 y minoritarios) no entran en ninguna cifra de la escalera. El requisito del pipeline para LISTO·PROVISIONAL sigue siendo una decisión humana.
- **Lo que pesaría sobre una conclusión favorable** a un precio cercano al de Sí: competidores, cuotas, margen por marca y el múltiplo de Tesco Chequia y Eslovaquia. Lo dejo dicho; no cambia esperar.

`alguno_material = false`.

## 7. Fundamento material (D10)

`hipotesis_sin_fundamento` está vacía:

- Ninguna palanca, probabilidad, quiebra, C76 ni C44 es de clase «técnico» o «sin juicio propio».
- Las de convención (B16, B69:D69 y C23) citan hechos.
- Las narrativas tienen mecanismo y «qué lo pararía» con páginas.
- C97 es técnico, pero no es una hipótesis de valoración (Anexo B §B.6).

Con conclusión no favorable, `resultado = no_procede` y no hago la comprobación conjunta.

## 8. Hipótesis que más condiciona

**Palancas!C15**, el margen NORMAL de 0,035: un subyacente del 4,0 % menos 0,4–0,5 puntos de cargos que se repiten.

- Media de la diferencia entre subyacente e IFRS: 0,52 puntos en diez años y 0,38 en 2021–2025. La mediana es ≈ 0,29.
- Con la media, el IFRS redondea a 0,035. Para llegar a 0,04 los cargos tendrían que quedarse por debajo de 0,25 puntos de media, y ninguna media de cinco años ha bajado de 0,38.
- Con 0,04, el precio de Sí sería ≈ 35,9, todavía por debajo de 36,05.

**Qué lo resolvería**: la diferencia entre el resultado subyacente y el IFRS de 2026 en el informe anual 2026 (3-mar-2027), con el margen de EE. UU. del 4T y las holguras de deterioro de Stop & Shop, Giant y Profi.

## 9. Turno 2 · comprobación conjunta y conclusión

No hay `comprobacion_conjunta.json`, porque con una conclusión no favorable no procede: `sobrevive = null` y `resultado = no_procede`.

**Estado `concluido` (provisional hasta la auditoría) · cubo Vigilar · acción `esperar` · precio objetivo 33,79 €** (precio de Sí de `precio.json`).

C104: «Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 33.79 · zona caro · precio de Sí ≤ 33.79 · precio esc. MALO 28.40 · ponderado 35.95 · fundamento no procede (conclusión no favorable)». El tamaño de la posición lo decide el inversor (D16).

C93 = Sí. Un g del 2 % con un ROIC terminal de 0,10 pide reinvertir el 20 % del resultado, por debajo del capex de hoy, y el terminal pesa un 51 %. «If a thing can't go on forever, it will eventually stop» (PCA p.416; HIM).

C103 = No. El margen es del 4 % sin poder de precio y todo el capital rinde por debajo de r.

## 10. Tesis (B101)

1. Ahold Delhaize vende comida en 9.551 tiendas de EE. UU. y Europa. Convierte un margen subyacente del 4,0 % en unos 2.300 de caja base al año y la devuelve casi entera al accionista [AR2025 PDF p. 42, 56].
2. Su ventaja es la escala local: Albert Heijn tiene el 38,2 % de cuota y Food Lion lleva 53 trimestres de comparables positivas [AR2025 PDF p. 43, 50]. El capital del accionista, pagado todo el alquiler, rinde un 13,03 % frente a mi 9 %.
3. Pero el ahorro se va al cliente y el resultado subyacente está plano desde 2022 [AR2025 PDF p. 45, 49]. En mi NORMAL el capital nuevo rinde un 14 % hasta el año 10 y un 10 % después.
4. La acción vale 28,40 / 35,76 / 44,05 €, con un precio de Sí de 33,79 €.
5. A 36,05 € pago algo más de lo que vale seguir como hoy sin crecer: 34,70 € en la hoja, ≈ 33,1 € sin la devolución fiscal belga de 2023. Me gusta el negocio, no el precio, y espero.

## 11. Tesis inversa (B102)

El No se defiende con las cifras de la propia empresa:

1. **El retorno es en parte prestado del casero.** Todo el capital rinde un 8,78 % (Historia!C55), menos que r y que el sector. El 13 % del accionista sale de alquilar el 85 % de los locales a ≈ 3,3 %, con unos 35.000 de prórrogas por renovar [AR2025 PDF p. 58, 272].
2. **No hay poder de precio.** El ahorro se fue al precio y el subyacente bajó del 4,4 % al 4,0 % [AR2025 PDF p. 45, 64]. EE. UU. va del 4,7 % al 4,3 %, con comparables del 0,5 % en el 3T 2026 [Q3-26 PDF p. 3, 7].
3. **La caja no crece.** El FCF sin circulante bajó de 2.149 a 1.725 LTM y la guía de 2026 es de unos 2.100 (extracto §0; Q3-26 PDF p. 2).
4. **Los cargos se repiten.** Hubo 643 en 2024, y las holguras de deterioro son de 1–2 % en Stop & Shop y Giant y mínima en Profi [AR2025 PDF p. 46, 238].
5. **Se compra sin cifras.** Tesco Chequia y Eslovaquia no tiene múltiplo publicado, y la recompra de 2026 se hizo a 35,41 € de media [Q3-26 PDF p. 21, 30].

Mi MALO no es un suelo. Lo que me impide firmar el No es que la escala local y el BBB+ aguantan bastante mala gestión.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

## 12. Predicciones (dado el NORMAL, todas a 2028-03-31)

1. **Margen subyacente del Grupo de 2027 entre el 3,8 % y el 4,2 %.** Probabilidad 0,7.
2. **Comparables sin gasolina del Grupo de 2027 entre el 0,5 % y el 3,5 %.** Probabilidad 0,7.
3. **Diferencia entre el resultado subyacente y el NIIF de 2027 de al menos 0,2 puntos de ventas.** Probabilidad 0,55. Pone a prueba la hipótesis de B222.

## 13. Incertidumbre pendiente (B222/B223)

**B222.** Es el margen NORMAL de 0,035 (Palancas!C15):

- Con 0,04, el precio de Sí sería ≈ 35,9.
- El objetivo de 33,79 tiene dos sesgos mecánicos que no rebato (sección 16). Con los dos corregidos, el precio de Sí queda en ≈ 32,5–33,0, y en ≈ 35,3 con el margen 0,04: siempre por debajo de 36,05.

**B223.** Lo resolvería el informe anual 2026, con la conciliación del resultado subyacente con el NIIF y las holguras de deterioro. Y una pregunta a Relación con Inversores: qué parte de los cargos es recurrente y cuándo se renuevan los arrendamientos.

## 14. Qué me haría cambiar de cubo

- **A Sí.** Un precio por debajo de 33,79 € con los hechos iguales. O, sin que baje el precio, dos años de cargos por debajo de 0,25 puntos. Antes pediría competidores, el múltiplo de Tesco y el margen de EE. UU. de 2026.
- **A No.** Cualquiera de estas: el ROIC propio por debajo de r dos años; el subyacente por debajo del 3,5 % dos años; un deterioro con cierres de tiendas; renovaciones de alquiler que se coman el diferencial; o una compra grande sin múltiplo.
- **A Demasiado difícil.** Que el online cambie la economía de la tienda hasta no poder juzgar la densidad, o que el control de precios se extienda a otros mercados del grupo.

## 15. Comparación con la etapa 1

El cubo es el mismo, Vigilar, por la misma razón. El precio de Sí pasa de 23,13 € a 33,79 € por dos causas:

- **Las entradas.** Con mis palancas y el FCF base de 2.312, la regla antigua da hoy 26,96 € (C156).
- **La regla.** La escalera k = 3 da 33,79 € con los mismos valores.

Además, mi MALO (28,40) es menos duro que el de la etapa 1 (23,13). Con las dos, el precio del día queda por encima del precio de Sí.

## 16. Respuesta al contradictor

| Objeción | Respuesta | Efecto |
|---|---|---|
| **O1 (baja).** El FCF base 2023–2025 lleva la devolución fiscal belga de 367 de 2023; f la absorbe y el precio de Sí sale ≈ 2,0 € alto. | **No rebatida.** El propio expediente lo declara en C46 y C47: incluye la devolución fiscal belga, +367 en 2023 (datos_v63 §2). La empresa lo confirma (Bélgica, 367: AR2023 PDF p. 220) y lo trata como un cobro incidental (AR2024 PDF p. 52). Devuelve un pago de 2021, fuera de la ventana: no es caja repetible. No encuentro en la ventana una salida que lo compense. | Un escalón hacia abajo. El objetivo de 33,79 queda ≈ 2,0 € alto (≈ 31,7–31,8). Zona caro. No cambio C52 ni `precio.json`: normalizar el FCF base es una decisión humana. Ajusto el texto de B101, B222, B223 y los insumos. |
| **O2 (sube).** El valor está fechado a 28-dic-2025 y el precio es del 13-nov-2026; llevado a la fecha del precio y restando los dividendos de 2026, el precio de Sí sube 0,9–1,4 €. | **No rebatida.** C55 dice que la valoración no está actualizada a 2026 (datos_v63 §2). Entre las dos fechas se pagaron 0,73 y 0,51 € (Q3-26 PDF p. 21). Lo único que podría oponer, la guía de FCF de 2026 de unos 2.100 (Q3-26 PDF p. 2), ya está en su extremo bajo. | Un escalón hacia arriba. El objetivo queda 0,9–1,4 € bajo (≈ 34,7–35,2) y la zona pasaría a vigilar; el precio sigue por encima del precio de Sí. Con el margen 0,04 cruzaría el precio (≈ 37,4). No cambio `precio.json`: la fecha es una convención del motor. |
| Nota 1 (no es objeción). Mi cuenta de Z-ACC olvidaba los 864 M€ de la recompra. | **Aceptada.** | La corrijo: precio de Sí ≈ 33,6 y ponderado ≈ 35,9, zona caro; con el margen 0,04, ≈ 35,8. |

**Regla de movimiento.** Hay dos objeciones válidas no rebatidas, una en cada dirección. El escalón hacia abajo (O1) y el escalón hacia arriba (O2) se compensan, así que la conclusión no se mueve.

**Conclusión final:**

- Estado `concluido` (provisional hasta la auditoría), cubo Vigilar, acción `esperar`.
- Precio objetivo: 33,79 €, el de `precio.json`. Lleva dos sesgos mecánicos declarados; con los dos corregidos queda en ≈ 32,5–33,0 €, con un ponderado de ≈ 34,8–35,2 €.
- Los dos valores quedan por debajo del precio de 36,05 €.
