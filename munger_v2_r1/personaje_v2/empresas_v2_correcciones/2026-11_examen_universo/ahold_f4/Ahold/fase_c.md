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
4. **Acciones y balance de fechas distintas** (Z-ACC, decisión registrada). Con las 865,174 M acciones de septiembre, los valores por acción subirían ≈ 2,5 %. La zona pasaría de caro a vigilar y la acción no cambia. Es un dato: no lo toco.
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

  En todas el precio sigue por encima del precio de Sí. Pero el margen 0,04 junto con las acciones de septiembre daría ≈ 36,8 y la zona cumple_regla_k. La acción esperar es estrecha.
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
