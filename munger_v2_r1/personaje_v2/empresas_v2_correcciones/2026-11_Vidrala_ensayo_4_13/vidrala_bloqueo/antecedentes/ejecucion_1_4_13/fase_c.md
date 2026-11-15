# Fase C · turno 1 · Vidrala, S.A. (VID) · base económica 31-dic-2025 · V6.4 experimental, motor B · copia con protocolo «bloqueo_del_objetivo»

Regeneración 4.13 de la fase C de esta copia. Las fases A y B, las palancas, el libro evaluado y `precio.json` no cambian. Cambian tres cosas:
- las variantes calculadas: ahora son 19 y su formato es el de la 4.13;
- el contrato de cobertura por parámetro;
- tres interpretaciones económicas de la 4.12, que están corregidas (`CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`).

La fase C de la 4.12 es mía y la reviso como si fuera de otro: «intensively consider any evidence tending to disconfirm any hypothesis of his» (PCA p.528; HIM). Los hechos salen de:
- `datos_v63.md` (Historia y anclas);
- `extracto_v63.md` ([ES, PDF p. n] y [CF_aaaa, PDF p. n]);
- lo que calcula la hoja (`resultados.json`, `precio.json`, `configuracion_v64_variantes.md`).

Las cifras marcadas «cálculo mío» son aproximaciones con la sensibilidad del tornado o con la fórmula de la escalera (∂P\*/∂V NORMAL = 0,6 ÷ 1,4); no son recálculos del libro.

## 1. Una sola historia

**Lo que calcula la hoja.**
- Valor por acción: 44,32 € (MALO), 60,21 € (NORMAL) y 78,52 € (BUENO).
- Ponderado: 60,70 €. Precio de Sí: 56,02 € (P\*, sin tope del NORMAL).
- Precio: 90,10 €, en zona **caro**. Está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí). Dicho al revés, el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio).
- Regla antigua (C156): 44,32 €.
- Peso del terminal: 41 / 48 / 54 %, siempre por debajo del 75 %.

Los semáforos:
- margen en REVISAR en los tres escenarios (G5, justificado en la fase B);
- f = −2,8 % en REVISAR, que es la razón del motor B;
- cuota implícita sin calcular (C24 vacía);
- el resto pasa.

El estado técnico es «COMPLETO Y VÁLIDO». El libro lleva los textos de la fase C de la 4.12. La hoja dice «DESCARTADA POR FILTRO PABRAI» por C13 = No. Mi cubo es Vigilar, porque C13 mide el precio, no el negocio.

**DCF inverso.** A 90,10 € el mercado descuenta un crecimiento de ventas del 14,2 % anual en los años 1–5, con el resto de mi NORMAL. Al precio de Sí descuenta −0,8 %. Mi NORMAL crece un 1,5 % y el BUENO un 3,5 %. El precio supera el valor BUENO de las 19 variantes calculadas: el máximo es 88,38 €, en solo_N2.

¿Quién es el tonto? «For a security to be mispriced, someone else must be a damn fool» (TCI p.17; HIM). No hace falta que lo sea nadie. Con mi NORMAL, 90,10 € equivale a una tasa unos dos puntos más baja que la del motor (≈6,5 % frente a 8,69 %; cálculo mío) o a un margen que no vuelve a su ciclo. Yo no tengo esa alternativa: «it's your alternatives that matter. That's how we make all of our decisions» (PCA p.114; HIM).

**Tornado (información, no criterio).** Efecto de cada palanca sobre el valor NORMAL:
- ROIC LP ±5 puntos: 12,67 €;
- tasa ±1 punto: 10,56 €;
- margen ±2 puntos: 7,36 €;
- crecimiento ±2 puntos: 3,52 €;
- S2C ±0,3: 2,22 €;
- g ±0,5 puntos: 0,19 €.

El efecto del ROIC es asimétrico: hacia arriba pesa poco, porque la reinversión terminal es g ÷ ROIC con g = 2 %. La tasa no es la palanca más influyente.

**¿Cuentan la misma historia que la fase A?** Sí. Es un fabricante maduro de un envase pesado, con un margen que sigue a la energía y un foso estrecho que la Historia sostiene. El precio paga más que mi escenario bueno. Encuentro estas fricciones; ninguna cambia el cubo ni la zona:

1. **Rentabilidad marginal.** La hoja calcula 14,7 % (NORMAL), 20,0 % (BUENO) y 9,5 % (MALO), porque aplica f = 1,165 al S2C (SR1) y el tipo N1. La fase B escribió ≈13 %, ≈17,6 % y ≈8,4 % con las bases heredadas. El salto del año 11 del NORMAL (5,7 puntos) solo pasa de 5 por la configuración:
   - con las bases heredadas sería ≈4,0 puntos;
   - con SR2, que reestima también el ROIC terminal (0,09 × 1,165 ≈ 10,5 %), sería ≈4,2 (cálculo mío).

   Lo crea reestimar el S2C sin reestimar el ROIC.
2. **El MALO y su capex.** Su historia cuenta hornos sin ventas detrás. Pero con R1 la palanca B16 = 0,7 no actúa (aviso s2c_inerte), y ese capex solo entra por λ: 19,9 mm al año. Si fueran 20 mm más al año durante cinco años, el precio de Sí bajaría ~1,0 € (cálculo mío).
3. **Perímetro del margen NORMAL.** Palancas!C15 = 0,18 sale de 2019–2025 con Italia. Con continuadas (18,55 %) daría 0,185. El precio de Sí subiría ~0,8 € (+1,4 %), sin cambiar el cubo ni la zona y por debajo del 5 %. La dejo y la registro en `celdas_corregidas`.
4. **Mezcla de la reinversión.** El S2C NORMAL (0,9) copia C53. En la reinversión histórica de 2021–2025 el circulante fue el 52,6 % (278,8 de 530,0 mm). La configuración fija el circulante en el 14,7 % de las ventas nuevas. Por eso, en el modelo, cada euro de ventas nuevas pide 0,954 € con SR1, de los que 0,807 € son fijos; en la historia fueron 0,527 € fijos por euro (251,2 ÷ 476,8). En la activa no mueve nada, porque el NORMAL y el BUENO solo dependen del total. Sí explica por qué H y SRF dan otros valores (punto 9).
5. **ROIC terminal y tasa.** La fase B dice «sin exceso a perpetuidad» frente a r = 9 %. Pero el motor descuenta a r_op = 8,69 %. El crecimiento perpetuo aporta +0,61 / +0,88 / +6,52 € (MALO / NORMAL / BUENO) y +1,57 € de precio de Sí frente a g = 0 (recálculo de la orquestación). Es poco, pero no es neutral, y ningún texto lo dirá así.
6. **Textos de la fase C de la 4.12 que lleva el libro.** C104 habla de 14 variantes y ahora son 19, con el mismo rango del precio de Sí (51,29–65,72 €). Los reescribo en el turno 2; no tocan el valor.
7. **C27 = Expandiendo** convive con escenarios que no expanden el margen. La fase A ya lo explicó: hubo un escalón en 2016–2019 y desde entonces es ciclo.
8. **El valor sin crecimiento (58,19 €)** es una lectura con base parcial (sin P0). Solo sirve de contexto.

## 2. Desviaciones pendientes (G8)

La gramática deja dos desviaciones: el salto del año 11 del NORMAL (5,7 puntos) y el del BUENO (8,0). Las justifico; no muevo palancas.

- **NORMAL (convención).** En los años 1–10, cada euro nuevo rinde 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 %, junto al ROIC de cinco años (13,8 %, Historia C55). La escala regional sigue sirviendo al capital que se reinvierte dentro del plazo del modelo. Desde el año 11, el capital nuevo rinde la tasa (9 %). Como la del motor es 8,69 %, todavía crea algo de valor.

  La ventaja que pierdo es la de añadir capacidad nueva con retorno en exceso en un mercado maduro [ES, PDF p. 55], cuyo competidor más peligroso no conozco (extracto §9). El margen del 18 % sigue sobre el capital instalado. «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).

  El exceso sobre 5 puntos lo crea la configuración: con las bases heredadas o con SR2 el salto quedaría por debajo de 5. La convergencia hacia el coste de capital es un criterio, no una ley (MR; E2).
- **BUENO (fundamentada).** Cada euro nuevo rinde el 20,0 %:
  - llena hornos que no iban llenos: la empresa supone plena utilización en 2025 «aunque no haya sido el caso» [ES, PDF p. 54];
  - suma Brasil, con un 42,4 % de margen EBITDA [ES, PDF p. 107];
  - cierra Toro [ES, PDF p. 85].

  Esa ventaja es finita. En el año 11, el capital nuevo rinde el suelo de la meseta de 2018–2025 (11,9 %, 12,5 % y 12,2 %; Historia E33, I33 y J33). Lo que se pierde es el volumen sin capex, no la ventaja del capital instalado. Sigue por debajo de 2 × C55 (27,7 %). «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

G16 (peso del terminal) y G17 (cuota implícita) no están señalados.

## 3. ¿Hay que mover palancas?

No. Ninguna incoherencia exige números distintos:
- la del margen NORMAL es de perímetro, y corregirla mueve el precio de Sí un 1,4 % sin cambiar el cubo ni la zona (calculado, v2.1);
- la del MALO no tiene palanca que la exprese bajo R1;
- la de la rentabilidad marginal y la mezcla de la reinversión vienen de la configuración, que la fase B no debía anticipar.

`revisar_palancas = false`. En `celdas_corregidas` dejo Palancas!C15 y B16 con `despues = antes` y su motivo. De la fase A no encuentro ninguna celda que impida sostener la conclusión.

## 4. Autocomprobación

1. **Anclaje en la etapa 1.** Mantuve Vigilar y 0,2/0,6/0,2, y cambié lo que la Historia corregía: C62 pasa al motor B, C97 a Neutral y C76 queda vacía. Con 0,25/0,6/0,15, el precio de Sí bajaría a 54,10 € (cálculo mío), y la zona seguiría en «caro». Cambio: ninguno.
2. **Anclaje en el precio o en la fuente externa.** Mis valores quedan muy por debajo de 90,10 € y de los 171,8 € de Simply Wall St. No bajo r ni subo el NORMAL. Cambio: ninguno.
3. **Consistencia y compromiso.** Esta regeneración hereda mi propia fase C de la 4.12, con tres interpretaciones ya corregidas.
   - Su mantenimiento elegía SR1 con dos inferencias que no prueban nada: que el exceso de 2025 descarta H (en H un año sin crecimiento paga todo el requisito) y que SRF quita «más de lo que muestra la historia» (compara cocientes con denominadores distintos).
   - En Q-ROIC1 la condición estaba invertida.
   - Además, el 9 % terminal no hace neutral el crecimiento.

   Cambio: el mantenimiento queda sin estructura más coherente, y PM1.roic_terminal pasa a fundamento insuficiente, con confianza baja. La conclusión no cambia, porque no dependía de esas inferencias. Miré también la tentación que crea el bloqueo: marcar los PM1 como fundamentados, o convertir el capex por destino en dato ausente material. No hay hechos nuevos que la sostengan.
4. **Historia bonita / viento de cola.** El margen de 2024–2025 coincide con el gas a la baja [ES, PDF p. 56]: es marea. Brasil se compró [ES, PDF p. 36–37]. Lo propio de Vidrala es la vuelta del margen de 2022 a 2024 y diez años de ROIC por encima del sector. Cambio: ninguno en palancas.
5. **Optimismo del BUENO frente a la tasa base.** En los años 1–10 rinde el 20,0 % por euro nuevo; con λ = 1,25 rendiría el 22,5 % (cálculo mío). Pide hornos sin llenar que no puedo medir. Cambio: ninguno, porque sigue bajo 2 × C55 y pesa ~0,14 € de precio de Sí por euro de valor.
6. **Doble castigo.** En la activa no encuentro el mismo riesgo en dos sitios. La estructura S sí castigaría dos veces, porque suma el requisito sobre un S2C que ya lleva la reposición histórica; la uso como argumento contra S. Cambio: ninguno.
7. **Disponibilidad.** Lo posterior a la base queda fuera. Los 43,1 mm de «Otros» pesan como mucho ~1,9 € de precio de Sí. Lo vívido de la renovación de hornos de 2025 no decide la estructura del requisito. «An idea or a fact is not worth more merely because it is easily available to you» (PCA p.587; HIM). Cambio: 2025 deja de contar como prueba contra H.
8. **Autoridad.** El NORMAL (1,5 %) está junto a la proyección de la empresa (1,6 % [ES, PDF p. 55]), pero se sostiene sin ella:
   - el orgánico de 2025 fue −5,4 % [ES, PDF p. 88];
   - C45 da un 2,9 %;
   - las bajadas de precio que supuso en 2023 se cumplieron en lo grueso [CF_2023, PDF p. 48].

   La otra autoridad es la configuración, que eligió SR1 para la demostración. No lo tomo como prueba. Cambio: SR1 queda como activa del ensayo, no como elección mía.
9. **¿El MALO es de verdad malo?** Vale 44,32 €, la mitad del precio, con un margen del 15 % para siempre. Su alivio es R1: libera circulante y su capex sin ventas solo entra por λ. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM). Cambio: ninguno.
10. **Lo no numerable.** La concentración de clientes sube [CF_2019, PDF p. 67; CF_2024, PDF p. 45; ES, PDF p. 104]. Pesan también la cobertura del 69 % de la energía de 2026 [ES, PDF p. 101] y el CO2. Ninguna celda recoge si cada reconstrucción de horno añade capacidad, que es lo que separa H de SR1. Cambio: va a la tesis inversa y a la información que falta de PM1.estructura.

## 5. Cubo y conclusión provisionales: Vigilar · esperar

Sigo el orden de mando:
- **Bloqueo:** ninguno.
- **Límite del modelo:** no; el motor B cuadra en las 19 variantes.
- **Descalificador mío:** ninguno.
- **Dato ausente material:** ninguno (punto 6).
- **Fundamento material:** la lista D10 está vacía (punto 7).
- **Zona:** caro.

Conclusión provisional: **esperar**, por precio. «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; TCI p.17; HIM). Aquí ni siquiera es maravillosa: es buena y cíclica.

El protocolo de esta copia hace con esa conclusión lo que dice el punto 9. El precio de Sí depende de la reposición de hornos, que no tiene fundamento suficiente, y con «bloqueo_del_objetivo» ese objetivo no se emite. En el turno 2 el expediente quedará en `pendiente_de_datos` · Vigilar · sin acción, y 56,02 € será un valor calculado condicional.

## 6. Datos ausentes (S-19)

Reviso los 30 datos de `datos_ausentes.json`. Ninguno es material para esperar con objetivo. Lo que más pesa:

- **Cuota y competidores.** Es el hueco mayor, pero no deja el objetivo sin base. Los márgenes salen de diez años propios que ya contienen un choque de energía completo, y el precio supera todos los BUENO calculados.
- **«Otros» ingresos (43,1 mm [ES, PDF p. 79]).** En el peor caso, el precio de Sí bajaría ~1,9 € (−3,3 %). Aparecen los dos años, así que una parte es recurrente.
- **Capex por destino, capacidad por planta y utilización.** No son materiales como datos ausentes: con todas las estructuras y con λ de 1,10 a 1,25 la zona es «caro». Lo que dejan sin fundamento es una hipótesis económica, la reposición de hornos. La registro una sola vez, en PM1 (punto 9).
- **Ingresos diferidos.** Cuadran: 41,117 − 23,115 = 18,002 mm de créditos fiscales [ES, PDF p. 10 y p. 71].

`alguno_material = false`.

## 7. Fundamento material (D10)

Revisé todas las hipótesis materiales de A y B: palancas, probabilidades, quiebra, C76, C44, motor, C6, C8 y las narrativas. Todas son «fundamentada» o «convención» con hechos en el apoyo, y ninguna narrativa es genérica. Miré con lupa las más débiles y ninguna entra en la lista:
- **B69:D69:** convención argumentada, con la fila 29;
- **B16:** inerte con R1;
- **D16:** ±0,3 mueve ~0,4 €;
- **D66:** el BUENO pesa poco.

La lista queda vacía. Con `esperar`, `resultado = no_procede`, la comprobación conjunta no procede y `sobrevive = null`. Los parámetros experimentales sin fundamento no entran en D10 con `esperar`: condicionan el objetivo por el protocolo.

## 8. Lo que más condiciona y qué lo resolvería

Con la lista vacía, la hipótesis de la que más depende la conclusión es **Palancas!C15**: que el 18 % del NORMAL es la media de un ciclo que vuelve, no un nivel nuevo. «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

Lo resolvería la serie de 2019–2025 de precio y coste de energía por tonelada en cada segmento, con las cláusulas de traslado, y la explicación de los 43,1 mm de «Otros». El estado del expediente, en esta copia, lo decide la reposición de hornos.

## 9. Configuración V6.4 experimental

**Variantes.** Las 19 variantes dan «caro», con un precio de Sí de 51,29 a 65,72 € (activa: 56,02 €). La tabla no es un intervalo de confianza. No refleja la familia del requisito, porque Θ no se calcula.

**Cobertura y materialidad.** Las cifras son el Δ del precio de Sí frente a la activa.

| Parámetro | Cobertura | Base | Cifra | Material para la acción | Material para el objetivo | Fundamento suficiente |
|---|---|---|---|---|---|---|
| N1.tipo | conjunta necesaria | calculada | −1,75 € | no | no | sí |
| N1.escudo | aislada | calculada | −0,08 € | no | no | sí |
| N2.margen | aislada | calculada | +0,94 € | no | no | sí |
| N3.regla | conjunta necesaria | calculada | −1,36 €, solo en el MALO | no | no | sí |
| N3.circulante | conjunta | juicio | — | no | no | sí |
| PM1.estructura | aislada | calculada | de −0,50 (S) a +5,35 (H); +7,10 sin requisito | no | sí | no |
| PM1.familia | conjunta | juicio | P-M1 entero: −6,61 € | no | sí | no |
| PM1.parametro | aislada | calculada | +2,37 (λ 1,10) / −4,73 (λ 1,25) | no | sí | no |
| PM1.convencion_anios | aislada | calculada | −0,13 € | no | no | sí |
| PM1.convencion_terminal | aislada | calculada | +0,40 € | no | no | sí |
| PM1.roic_terminal | conjunta necesaria (SR2) | calculada | +1,06 € | no | no | no |
| PM1.cartera | aislada | calculada | +0,54 € por P0 | no | no | sí |

Las dos materialidades de juicio son estas:
- **N3.circulante:** es un dato recalculado [ES, PDF p. 9 y p. 10]. Solo fija el circulante que libera el MALO, unos 3 mm al año, y su peso es de unos 0,3 € (cálculo mío).
- **PM1.familia:** un requisito no negativo, en cualquier familia, no puede subir el valor por encima del caso sin requisito (62,63 €, caro). Un requisito negativo lo contradice la historia: el capex ha sido de 1,10 veces la amortización o más todos los años desde 2017.

Dos contradicciones con la configuración, revisadas:
- **N3.regla:** la configuración la llama hipótesis y yo le doy fundamento suficiente. En los dos años de caída de ventas (2020 y 2025), la reinversión neta orgánica fue positiva (41,0 y 54,8 mm): no se liberó capital fijo. Lo que no se demuestra, que la capacidad conservada sirva después, solo afecta al MALO y en sentido prudente.
- **PM1.roic_terminal:** la configuración le da confianza media y yo, baja, porque Q-ROIC1 sigue abierta.

La invariancia de la acción vale solo para las variantes calculadas.

**Q-ROIC1, con la condición corregida.** SR1 es coherente si mi ROIC terminal es neto de reposición; SR2, si se midió sobre una inversión que ya la incluye. La fase B lo eligió con la base V6.3, sin rebajarlo por la reposición (fase_b.md; datos_v63.md §0).
- En el BUENO (12 %) es el suelo del ROIC histórico, medido sobre un capital que acumula el exceso de capex y con la amortización a coste histórico. Apunta a SR2.
- En el NORMAL y el MALO (9 %) es la convención de que el capital nuevo rinde la tasa, no una medida. La condición no decide.

«Sin cambio» no tiene fundamento suficiente, pero no es material: +1,06 € (+1,9 %).

**Mantenimiento.** ¿La reposición supera la amortización? Probablemente sí, aunque no está medida:
- el capex ha sido de 1,10 veces la amortización o más todos los años desde 2017, y de 1,45 veces en 2021–2025 (739,0 frente a 509,6 mm; Historia filas 12 y 8);
- en 2025 fue de 1,42 veces, con ventas orgánicas −5,4 % y la renovación de hornos como destino principal [ES, PDF p. 50; p. 88];
- hay 627 mm de inmovilizado amortizado en uso [ES, PDF p. 51]. Corta en los dos sentidos: las vidas económicas son más largas que las contables, pero la reposición es a coste corriente.

En contra, en 2019 la empresa suponía que un capex del 8 % de las ventas bastaba [CF_2019, PDF p. 44]. Parte del exceso puede ser Brasil [ES, PDF p. 128] o descarbonización. λ = 1,15 es un tercio del exceso; todo el exceso daría λ ≈ 1,46.

¿Qué estructura es la más coherente? **No hay base para nombrar una** (`estructura_mas_coherente = null`):
- **S** es la menos coherente: suma el requisito sin reestimar un S2C (C53) que ya lleva la reposición histórica.
- **H frente a SR1:** 2025 no las separa. Las separarían los años con crecimiento, pero en 2021–2024 el crecimiento fue sobre todo precio (+24,1 % en 2022 con el margen a la baja), que pide circulante, y las cuentas no separan la inversión fija para crecer. Con H, el NORMAL y el BUENO valen lo mismo que sin requisito (67,52 y 86,43 €): solo paga el MALO.
- **SR1 frente a SRF:** SR1 quita 0,157 € por euro de ventas nuevas (el 14,2 % de la reinversión total). SRF quita 0,288 € (el 29,9 % de la fija), porque el modelo agranda la parte fija de la reinversión futura (86,8 % con S2C 0,9, frente al 47,4 % histórico). Que la reposición acompañe a la reinversión total o a la fija es una hipótesis, no un hecho.
- **SR1 frente a SR2:** es Q-ROIC1.

Precio de Sí por estructura: H 61,37 · SRF 58,43 · SR2 57,08 · SR1 56,02 (activa, de la demostración) · S 55,52 €. Todas en «caro». No se adopta nada.

**Avisos de dominio.** Ninguno es material:
- **Factor de reestimación** (f = 1,165; de 1,00 a 1,31 en las variantes): explica la G8 del NORMAL. En el extremo inferior (λ 1,25) la rentabilidad marginal del NORMAL es del 16,5 %, todavía bajo 2 × C55.
- **Terminal R1 sin máximo conservado:** el MALO carga de 11,1 a 16,3 mm. Va del lado prudente.
- **S2C inerte en el MALO:** ~1,0 € de precio de Sí.
- **Inversión fija para crecer negativa:** solo en solo_N1, solo_N2 y activa_R0_sin_PM1, que llevan R0 y cuyo MALO libera unos 31 mm al año de capital fijo. Afecta al extremo superior del rango (65,72 €). Dentro del dominio, el máximo es 64,75 € (heredado). Las tres dan «caro».

Las lecturas con bases parciales (G7, referencias mecánicas, valor sin crecimiento sin P0) no las presento como comprobación del modelo experimental.

**Objetivo (protocolo `bloqueo_del_objetivo`, ensayo).** Espero por precio. Lo condicionan PM1.estructura, PM1.familia y PM1.parametro. La lista D10 está vacía, y ningún aviso ni dato ausente es material. La acción se sostiene en las 19 variantes. Aun así, este protocolo no emite un objetivo que depende de información no disponible: el tratamiento es **objetivo_bloqueado**, con origen `protocolo_de_bloqueo`.

La información que falta:
- el desglose del capex por destino;
- el coste de reconstruir hoy un horno;
- la capacidad que añade cada reconstrucción, la utilización y las toneladas;
- la inversión fija que acompañó al crecimiento de 2021–2024.

«Knowing what you don't know is more useful than being brilliant» (TCI p.15; HIM).

## Cambios frente a la fase C de la 4.12

1. **Mantenimiento:** `estructura_mas_coherente` pasa de SR1 a `null`. Retiro los dos argumentos corregidos (H y 2025; SRF y «más de lo que muestra la historia») y añado la mezcla de la reinversión y Q-ROIC1.
2. **PM1.roic_terminal:** `fundamento_suficiente` pasa a false, con confianza baja y la condición de Q-ROIC1 ya corregida. No es material.
3. **Contrato 4.13:** cobertura, base de la materialidad, evidencia, hechos, inferencias y contradicciones en los 12 parámetros. Las cifras de materialidad salen ahora de los contrastes aislados (N1 −1,75; N2 +0,94; P0 +0,54 €).
4. **Avisos de las variantes:** cuatro grupos, entre ellos la inversión fija negativa en las variantes con R0.
5. **Textos:** la G8 del NORMAL y las incoherencias ya no dicen que el ROIC del 9 % hace neutral el crecimiento; hay una incoherencia nueva sobre la mezcla de la reinversión.
6. **Sin cambios:** palancas, `celdas_corregidas`, datos ausentes (salvo el recuento de variantes), D10, cubo y conclusión provisionales, y tratamiento del objetivo.

## 10. Turno 2 · conclusión

**Comprobación conjunta.** No se ejecutó: no procedía con `esperar`. No existe `comprobacion_conjunta.json`, así que `sobrevive` queda `null` y `resultado = no_procede`.

**Estado: pendiente de datos · cubo Vigilar · sin acción · sin precio objetivo.**
- No hay bloqueo, ni límite del modelo, ni descalificador.
- Ningún dato de `datos_ausentes.json` es material (S-19) y la lista D10 está vacía.
- La zona es «caro» y la conclusión provisional era esperar por precio.

Lo que me impide cerrar es el objetivo. El precio de Sí calculado (56,02 €) depende de la reposición de hornos (PM1.estructura, PM1.familia y PM1.parametro), que no tiene fundamento suficiente. Con el protocolo experimental «bloqueo_del_objetivo» (ensayo, no adoptado), un objetivo así no se emite: tratamiento `objetivo_bloqueado`, origen `protocolo_de_bloqueo`. `objetivo_v64.py` (solo lectura) da el mismo tratamiento y el mismo estado esperado.

La acción se sostiene en las 19 variantes calculadas: todas «caro», con un precio de Sí de 51,29 a 65,72 € (51,29–64,75 € dentro del dominio declarado). Ese rango es el de la tabla de variantes, no un intervalo de confianza, y no refleja la familia del requisito. A 90,10 € no compraría, pero no digo a qué precio sí mientras falte el capex por destino.

C104: «Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de datos: objetivo bloqueado por el protocolo experimental; …) · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento pendiente de datos · 56.02 es valor calculado condicional, no objetivo; …». La posición es de José Luis.

C93 = Sí. g es del 2 %, por debajo de la tasa sin riesgo (2,85 %); la reinversión terminal es g ÷ ROIC = 22 % con ROIC 0,09, más el requisito de reposición; el peso del terminal es del 48 %. El salto del año 11 es la convención del capital nuevo a la tasa. El crecimiento perpetuo aporta poco, pero no es neutral: +0,88 € en el NORMAL.

C103 = No. Es cíclica, con un margen ligado a la energía y un foso estrecho: es una propiedad del negocio.

## 11. Tesis y tesis inversa

**Tesis (B101).** Vidrala fabrica envases de vidrio en Iberia, Reino Unido e Irlanda y Brasil, con clientes repartidos (ninguno por encima del 10 % [ES, PDF p. 104]) y diez años de ROIC por encima del sector (13,8 % frente al 9,3 %; Historia C55, Palancas H18). Leo que gana porque fabrica cerca del cliente y traslada la energía con retraso: el margen cayó al 13,7 % en 2022 y volvió al 20,8 % en 2024 (Historia I29, K29). El 19,9 % de 2025 está junto al máximo, con el gas a la baja, y la empresa supone bajadas de precio en 2026 [ES, PDF p. 54]. A 90,10 € pago más que mi BUENO (78,52 €). Vigilar sin conclusión: el precio de Sí que calculo (56,02 €) depende de una reposición que no puedo fundar, y no lo doy como objetivo.

**Tesis inversa (B102).** Defiendo el No con hechos:
- es un producto poco diferenciado en un mercado maduro [ES, PDF p. 55], con consumo inferior a lo previsto y capacidad que se adapta [ES, PDF p. 94], y ventas orgánicas −5,4 % [ES, PDF p. 88];
- el margen es energía barata camino del cliente [ES, PDF p. 54 y p. 56], con 2,9 puntos de «Otros» que nadie explica [ES, PDF p. 79];
- los hornos se comen la caja: capex de 1,42 veces la amortización con ventas a la baja (Historia L12 y L8), 627 mm amortizados en uso y 66,6 mm comprometidos [ES, PDF p. 51];
- los clientes ganan fuerza: los diez mayores pasan de ~30 % a ~38 % en 2019–2024 [CF_2019, PDF p. 67; CF_2024, PDF p. 45];
- el crecimiento se busca donde no hay foso probado: el real cayó un 20 % en 2024, la deuda va a CDI y Toro venía con plan de ajuste [ES, PDF p. 106, p. 105 y p. 85];
- en 2016–2017 el ROIC era la tasa (Historia C33:D33);
- no hay ningún competidor con nombre.

«I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Los dos errores.** Sigo más cerca de pagar cualquier cosa por calidad: el precio paga más que mi mejor escenario en las 19 variantes. «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

## 12. Predicciones (dado el NORMAL; autopsia el 31-mar-2028)

1. **Margen operativo de 2027 entre el 16 % y el 20 %.** Probabilidad 0,7: cinco de los siete años de 2019–2025 cayeron ahí (Historia F29:L29).
2. **Ventas orgánicas de 2027 entre −2 % y +4 % frente a 2026.** Probabilidad 0,65: el NORMAL crece un 1,5 %, pero el precio de la energía ha movido mucho las ventas (Historia fila 28).
3. **Capex de 2027 por encima de 1,2 veces la amortización.** Probabilidad 0,7. Pone a prueba la reposición, que es lo que bloquea el objetivo: seis de los últimos nueve años lo superaron (Historia filas 8 y 12), y 2025 tuvo menos hornos que 2024 [ES, PDF p. 180].

Son la autopsia del análisis: «comparing predictions with outcomes» (PCA p.606; HIM).

## 13. Qué me haría cambiar de cubo

- **A Sí:** un precio por debajo de 56,02 € sin que cambie el negocio y con la reposición fundada por el desglose del capex. Por debajo de 51,29 € la zona cumpliría la regla en las 19 variantes, pero la compra seguiría exigiendo que los PM1 entren en la comprobación conjunta y la superen.
- **A No:** un margen bajo el 14 % sin choque de energía; dos años más de capex por encima de 1,4 veces la amortización con ventas planas y el ROIC hacia la tasa; o datos de cuota que muestren pérdida.
- **A Demasiado difícil:** que el valor pase a depender de Brasil y Chile, con su divisa y su deuda; un exceso de capacidad duradero de los competidores; o una sustitución del vidrio que no sepa juzgar.

B222 nombra Palancas!C15 (el 18 % del NORMAL como media de un ciclo que vuelve) y la reposición de hornos (Configuración V6.4!B36:B38), que es lo que deja el expediente sin conclusión; la activa SR1 es de demostración y no hay estructura más coherente con las fuentes.

B223 pide a Relación con Inversores:
- el desglose del capex por destino, con el coste de reconstruir hoy un horno, la capacidad que añade cada reconstrucción, la inversión fija que acompañó al crecimiento de 2021–2024 y la utilización por segmento (esto desbloquearía el objetivo);
- el precio y el coste de energía por tonelada en cada segmento, con las cláusulas de traslado;
- el desglose de los 43,1 mm de «Otros».

## 14. Comparación con la etapa 1

El cubo es el mismo, Vigilar, y por la misma razón; el cierre no.
- **Cierre:** la etapa 1 concluía esperar hacia ~48 €; aquí el precio de Sí calculado es 56,02 €, pero no se emite como objetivo, y el expediente queda pendiente de datos.
- **Regla:** se pasa del mínimo del MALO y ¾ del ponderado a la escalera k = 3, que queda por encima del MALO (44,32).
- **Modelo:** motor B con palancas.
- **Configuración experimental:** resta 8,73 € frente al modo heredado (64,75) por la reposición, el tipo y R1.

Mi NORMAL (60,21 €) está por debajo del valor normal de la etapa 1 (~74 €): el margen va a la media del ciclo y el capital nuevo rinde la tasa desde el año 11. La etapa 1 usaba hechos posteriores a la base; yo no. Mantengo C93 y C103 y reescribo B101, B102 y C104 (este sin porcentaje).

## Cambios del turno 2 frente a la 4.12

1. **Recuento:** C104, B222, `escalera`, `insumos_decision_cartera.fundamento`, `cambiaria_de_cubo.a_si` y la herencia de C104 pasan de 14 a 19 variantes calculadas (mismo rango, 51,29–65,72), con el máximo dentro del dominio (64,75).
2. **Estructura:** B222, B223, `decision.condiciones_revision` y la Observación de A40 ya no dan SR1 como elegida; B223 pide además la capacidad por reconstrucción y la inversión fija del crecimiento de 2021–2024.
3. **C93:** su Observación y su herencia dicen que el crecimiento perpetuo aporta poco pero no es neutral (r_op 8,69 %).
4. **Sin cambios:** estado, cubo, acción nula, tratamiento del objetivo, B101, B102, C103, las tres predicciones con sus fechas y probabilidades, `confianza_global` (media) y todo el turno 1 salvo `turno`.
