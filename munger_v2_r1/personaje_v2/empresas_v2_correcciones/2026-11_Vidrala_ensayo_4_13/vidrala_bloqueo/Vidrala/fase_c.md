# Fase C · turno 1 · Vidrala, S.A. (VID) · base económica 31-dic-2025 · V6.4 experimental (no adoptada)

Reviso las fases A y B como si fueran de otro: «consider any evidence tending to disconfirm any hypothesis» (PCA p.528; HIM). Los hechos salen de `extracto_v63.md` ([ES, PDF p. n], [CF_aaaa, PDF p. n]), de `datos_v63.md` (Historia, Análisis, Palancas), de `resultados.json`, de `precio.json` y de `configuracion_v64_variantes.md`. Los hechos posteriores a la base no cuentan. Damodaran va solo por documento y principio.

## 1. Una sola historia

La hoja da 44,32 / 60,21 / 78,52 € (MALO / NORMAL / BUENO), un ponderado de 60,70 € y un precio de Sí de 56,02 € (`precio.json`). El precio es 90,10 €: zona **caro**. Está por encima incluso del BUENO. El precio está un 60,8 % por encima del precio de Sí (diferencia ÷ precio de Sí); dicho al revés, el precio de Sí está un 37,8 % por debajo del precio (diferencia ÷ precio). El DCF inverso dice que 90,10 € descuenta un crecimiento de ventas del 14,2 % al año durante cinco años. Es cuatro veces mi BUENO (3,5 %) y cinco veces el CAGR de tres años (2,9 %, Historia C45).

Eso es lo que contaba `fase_a.md`: un fabricante de envases con un foso estrecho, un margen que se mueve con la energía y un precio que paga un margen junto a su máximo. Las 52 celdas cuentan esa historia. Peso del terminal: 40,7 % / 47,9 % / 54,3 %. La tabla del DCF inverso es monótona.

Siete incoherencias. Ninguna cambia el cubo ni la zona:

1. **S2C del MALO inerte.** La fase B eligió 0,7 para meter «capex sin ventas detrás». Con R1 y ventas que nunca pasan de 1.465 mm en los años 1–10, el S2C no actúa. Y con ventas que caen, ningún S2C podría expresar ese capex en este motor. Por eso el MALO no lleva ese canal. Lo mido así: cada 10 mm al año de capex sin ventas durante cinco años valen ≈ 1,1 € de V MALO y ≈ 0,5 € de precio de Sí. Es aritmética mía: P = (0,6 V_MALO + 0,6 V_NORMAL + 0,2 V_BUENO) ÷ 1,4 con mis probabilidades, y reproduce 56,02.
2. **El S2C del NORMAL y del BUENO sale de un ancla con el perímetro mezclado.** Historia C53 (0,916) divide 476,8 mm de ventas nuevas 2020→2025 entre la reinversión. Esas ventas incluyen +178 mm de Brasil y −72 mm de Italia. La reinversión solo lleva 12,4 mm netos de adquisiciones (la compra de Brasil menos la venta de Italia), y los 168 mm de deuda asumida no entran. Con el mismo perímetro (Península y Reino Unido, nota 4: +372,4 mm [CF_2021, PDF p. 30; ES, PDF p. 33]) frente a 508,2 mm de reinversión orgánica sale ≈ 0,73. Es una derivación de perímetro, no un error prudente. Calculo el efecto de corregirla: C16 y D16 en −0,15 restan ≈ 0,9 € de V NORMAL y ≈ 1,2 € de V BUENO, y ≈ 0,55 € de precio de Sí (−1,0 %). El MALO no se mueve porque es inerte. No cambia el cubo ni la zona y queda por debajo del 5 %: la dejo (v2.1).
3. **El margen del NORMAL tiene el perímetro mezclado al revés.** El 18 % es la media 2019–2025 (18,13 %, Historia F29:L29), con Italia en 2019–2022. Para 2020–2025, la configuración da 18,55 % con continuadas y la Historia 18,22 %. Con continuadas, el NORMAL redondearía a 0,185: ≈ +1,8 € de V NORMAL y ≈ +0,8 € de precio de Sí (+1,4 %). Va en sentido contrario al punto 2 y también queda por debajo del 5 %: la dejo.
4. **El salto del año 11 es mayor de lo que vio la fase B.** Con f, la rentabilidad marginal del NORMAL es 0,9 × 1,165 × 0,18 × (1 − 0,2205) = 14,7 % frente a un ROIC terminal del 9 % (5,7 puntos). Sin f serían 12,6 % y 3,6 puntos. La G8 del NORMAL existe por la configuración (§2).
5. **«El capital nuevo rinde la tasa» no hace neutral el crecimiento.** El motor descuenta a r_op 8,689 % (Diagnóstico V6!C15), no al 9 %, y con P-M1 el terminal carga además el requisito. El g perpetuo aporta +0,61 / +0,88 / +6,52 € en la activa (`resultados/crecimiento_terminal_vidrala.md`, que solo leo). La historia aguanta: en el NORMAL el crecimiento aporta poco.
6. **Lecturas con bases parciales.** El valor sin crecimiento (58,19 €) y «cuánto pagas por crecer» (15,8 veces) no llevan la cartera P0. G7 y las referencias mecánicas usan el tipo de la Historia y el S2C sin f. Las leo como lecturas, no como comprobación del modelo experimental (`datos_v63.md` §0).
7. **Textos de la ejecución anterior.** El libro evaluado lleva en C93, B101, B102, B222 y B223 los textos de la ejecución anterior de esta fase C. No los uso. El turno 2 escribe esas celdas.

La hoja dice «DESCARTADA POR FILTRO PABRAI» (A6) por C13 = No. Mi cubo es Vigilar porque C13 = No mide el precio, no el negocio. Tornado (información, no criterio): ROIC ±5 puntos mueve 12,67 €, la tasa ±1 punto 10,56 € y el margen ±2 puntos 7,36 € de V NORMAL. La tasa de descuento no es la palanca que más pesa.

## 2. Desviaciones pendientes

`gramatica.md` (motor B, código 0): 0 errores y 0 límites del modelo. Las tres G5 están justificadas en la fase B. Quedan dos G8, que justifico en `desviaciones_justificadas`. G16 y G17 no aparecen: el peso del terminal está por debajo del 75 % y no hay cuota implícita sin C24.

- **G8 NORMAL (5,7 puntos; convención con hechos).** En los años 1–10 el capital nuevo rinde 14,7 %, junto al ROIC de cinco años (13,8 %, C55). Desde el año 11 rinde la tasa. El mercado es maduro [ES, PDF p. 55], el consumo está por debajo de lo previsto y la capacidad se ajusta [ES, PDF p. 94], y Vidrala ya rindió la tasa en 2016–2017 (9,4 %, Historia C33:D33). En el año 11 se pierde la ventaja sobre el capital nuevo, no sobre el instalado. Es la convergencia como criterio (MR; E2): «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM).
- **G8 BUENO (8,0 puntos; fundamentada).** Cada euro nuevo rinde 20,0 % mientras el volumen llena capacidad que en 2025 no estaba llena [ES, PDF p. 54] y Brasil (42,4 % de margen EBITDA [ES, PDF p. 107]) y Chile crecen. Cuando se acaba la capacidad libre, el capital nuevo vuelve al suelo de la meseta 2018–2025 (11,9–12,5 %, Historia E33, I33, J33). Sin G7: el 20,0 % queda por debajo de 2 × C55 = 27,7 %. «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM).

## 3. Palancas

No pido volver a la fase B (`revisar_palancas = false`). Las dos derivaciones de perímetro (§1, puntos 2 y 3) van en sentidos opuestos. Su efecto neto es de unos +0,3 € de precio de Sí, cada una queda por debajo del 5 % y ninguna cambia el cubo ni la zona. El S2C del MALO no se arregla moviéndolo. Lo registro en `celdas_corregidas` con `despues = antes`: Palancas!B16, C16, D16 y C15. No veo ninguna celda de la fase A mal puesta.

## 4. Autocomprobación

Lo que miré en cada tendencia (detalle en el JSON):

- **Anclaje en la etapa 1.** El Vigilar sale de ahora. El precio supera el BUENO y también el ponderado del modo heredado (69,04 €).
- **Precio o fuente externa.** Ningún escenario se acerca a 90,10 € ni al Fair Value ajeno (171,8 €, C38, de fecha posterior a la base).
- **Consistencia.** Encontré las dos derivaciones de perímetro. Las escribo en vez de esconderlas.
- **Historia bonita.** La vuelta del margen de 2022 a 2024 es en parte energía. El 19,9 % de 2025 lleva 43,1 mm de «Otros» sin explicar [ES, PDF p. 79], 2,9 puntos de margen.
- **Optimismo del BUENO.** El BUENO pide a la vez Chile, el real y retener el ahorro de energía. Con f es más rentable de lo que vio la fase B (20,0 % frente a 17,1 %).
- **Doble castigo.** No lo hay: el pico de margen está en el NORMAL y el MALO, no en la probabilidad ni en la r.
- **Disponibilidad.** Los hechos posteriores a la base quedan fuera. Para el mantenimiento uso las diez filas de la Historia, no el relato.
- **Autoridad.** El volumen +1 % es un supuesto del vendedor [ES, PDF p. 54] que contrasta la Historia: «will frequently be a lie» (TCI p.60; HIM).
- **¿El MALO es malo?** Sí: vale la mitad del precio. Pero no es el peor caso: le falta el capex sin ventas. «We don't think because it's never happened that it won't» (AIWTK p.55; HIM).
- **Lo no numerable.** Competidores, sustitución del vidrio, CO2, concentración de clientes al alza (~30 % → ~38 % [CF_2019, PDF p. 67; CF_2024, PDF p. 45]) y Chile.

## 5. Cubo provisional y conclusión provisional: Vigilar · esperar

En orden de mando:

1. Bloqueo: no hay (0 errores).
2. Límite del modelo: no hay.
3. Descalificadores: ninguno. La deuda neta es 0,36x EBITDA (C33) y hay 258 mm disponibles [ES, PDF p. 75].
4. Dato ausente material: ninguno (§6).
5. Fundamento material: la lista D10 está vacía (§7).
6. Zona: caro.

Por tanto, **Vigilar · esperar**. El precio objetivo sería el precio de Sí (56,02 €). Con el protocolo declarado no se emite (§9). «If you wait, I think you'll get your price» (DR p.29; AUTHOR).

## 6. Datos ausentes (S-19)

Reviso los 30 datos de `datos_ausentes.json`, uno a uno. Ninguno es material para sostener `esperar` ni un precio objetivo: `alguno_material = false`. Los que más se acercan:

- **«Otros» ingresos (43,1 mm).** Si no se repitieran, estimo ≈ −1,6 € de precio de Sí, por debajo de mi criterio y lejos de la acción. Lo pido para B223.
- **Competidores y cuota.** Es el mayor hueco cualitativo. Pero el objetivo no paga foso más allá del año 10, y diez años de ROIC y margen por encima del sector sostienen los años 1–10. Sería lo primero que pediría antes de una compra.
- **Capex 2026+ por destino.** Lo que P-M1 necesita lo trato como hipótesis sin fundamento suficiente (§9). Contarlo también como dato ausente sería contar dos veces la misma carencia.
- **Ceros de adquisiciones de 2021–2022.** Si la participación inicial en Vidroporto se pagó antes de 2023, C53 bajaría a ≈ 0,83. Es el mismo sentido que el punto 2 del §1 y no cambia nada.

Un hallazgo: la «conciliación no encontrada» de los ingresos diferidos sí cuadra con el extracto. 23.115 + 18.002 = 41.117 [ES, PDF p. 51, p. 10 y p. 71].

## 7. Fundamento material (D10)

`hipotesis_sin_fundamento` queda vacía. En la fase B ninguna palanca, probabilidad, quiebra, C76 ni C44 es «técnico» ni «sin juicio propio», y todas las Observaciones citan hechos con celda o página. Motor (C62), caso especial (C6) y base del margen (C8) son fundamentadas con hechos. Las tres narrativas de la fase A nombran mecanismo, dueño de la mejora y qué las pararía, con páginas.

Las derivaciones de perímetro del §1 son defectos de derivación con fundamento, no hipótesis sin él. Con `esperar` el resultado es `no_procede`. No hago la comprobación conjunta: no hay hipótesis que combinar.

## 8. Lo que más condiciona y qué lo resolvería

Con la lista D10 vacía, la hipótesis fundamentada de la que más depende la conclusión, a mi juicio, es **Palancas!C15**. Supone que el 18 % del NORMAL es la media de un ciclo de energía que vuelve y no un nivel nuevo. La empresa ya supone bajadas de precio en 2026 [ES, PDF p. 54] con el gas de 39,9 a 23,3 €/MWh [ES, PDF p. 56]: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

Lo resolvería esto:

- precio medio y coste de energía por tonelada por segmento en 2019–2025;
- las cláusulas de traslado de los contratos;
- el desglose de los 43,1 mm de «Otros» [ES, PDF p. 79].

El objetivo depende además de P-M1 (§9), y eso es lo que lo deja sin emitir.

## 9. Configuración V6.4 (modo experimental; demostración, no adoptada)

**Criterios.**

- **Acción.** Para cambiarla, el precio de Sí tendría que pasar de 90,10 €, es decir +34,08 €. Las 19 variantes calculadas quedan en caro: precio de Sí 51,29–65,72 €, ponderado 55,84–70,02 €. Por eso ningún parámetro es material para la acción. La base es calculada donde hay contraste aislado o variación conjunta necesaria. Es juicio en N3.circulante y PM1.familia, que solo cambian con todo lo demás.
- **Objetivo.** No hay umbral adoptado. Mi juicio: es material un efecto de 1,5 € o más (≈ 2,7 % de 56,02). Es algo más que un paso de redondeo de la palanca más gruesa (ROIC 0,01 ≈ 1,1 € de precio de Sí; tornado como información y dP/dV NORMAL = 0,6 ÷ 1,4). Que la acción no cambie en estas variantes no prueba que un parámetro sea inmaterial: el rango es una sensibilidad condicional.

**Parámetros** (cobertura comprobada con `objetivo_v64.cobertura`):

| Parámetro | Cobertura | Contraste (Δ precio de Sí) | Acción | Objetivo | Fundamento |
|---|---|---|---|---|---|
| N1.tipo | conjunta necesaria | activa_sin_N1 +1,75 € | no (calc.) | **sí** (calc.) | sí |
| N1.escudo | aislado | −0,08 € | no (calc.) | no (juicio) | sí |
| N2.margen | aislado | −0,94 € | no (calc.) | no (juicio) | sí |
| N3.regla | conjunta necesaria | +7,96 € con P-M1; propio de R1 −1,36 € | no (calc.) | no (juicio) | sí |
| N3.circulante | conjunta | sin contraste propio | no (juicio) | no (juicio) | sí |
| PM1.estructura | aislado | H +5,35; SRF +2,41; SR2 +1,06; S −0,50; sin requisito +7,10 € | no (calc.) | **sí** (calc.) | **no** |
| PM1.familia | conjunta | sin contraste propio | no (juicio) | **sí** (juicio) | **no** |
| PM1.parametro | aislado | λ 1,10 +2,37; λ 1,25 −4,73 € | no (calc.) | **sí** (calc.) | **no** |
| PM1.convencion_anios | aislado | −0,13 € | no (calc.) | no (juicio) | sí |
| PM1.convencion_terminal | aislado | +0,40 € | no (calc.) | no (juicio) | sí |
| PM1.roic_terminal | conjunta necesaria | SR2 +1,06 € | no (calc.) | no (juicio) | **no** |
| PM1.cartera | aislado | −0,54 € | no (calc.) | no (juicio) | sí |

Notas:

- **N1.tipo.** 22,05 % es la media 2023–2025 de la Historia (J10:L10). Es material para el objetivo, pero fundado: no lo condiciona.
- **N3.regla.** La configuración la llama hipótesis; yo la doy por fundada. En 2020 y 2025, con ventas a la baja, el capex superó a la amortización en 50,1 y 55,6 mm y solo se liberó circulante. Además, 2025 no fue a plena utilización [ES, PDF p. 54].
- **PM1.roic_terminal.** Bajo la confianza a baja. Q-ROIC1 sigue abierta y mi fase B eligió sobre la base de la V6.3 sin decir si su ROIC era neto o bruto de reposición. Queda sin fundamento, pero su contraste (1,06 €) no llega a mi criterio: no condiciona el objetivo.
- **PM1.familia.** Ninguna variante calcula Θ y no la cubre ningún contraste aislado. La juzgo material para el objetivo porque fija el tamaño de un requisito que vale 7,10 €. No es material para la acción: haría falta reponer a ≈ 40 % de la amortización.

**Mantenimiento.** ¿Supera la reposición a la amortización? Probablemente sí a coste corriente, pero no está medido.

- A favor:
  - el capex superó a la amortización en nueve de diez años (1,45 veces en 2021–2025), también en 2020 y 2025, años sin crecimiento;
  - las altas de 2025 son «principalmente» renovación de hornos [ES, PDF p. 50];
  - los hornos viven hasta 15 años [ES, PDF p. 168].
- En contra:
  - 627 mm de inmovilizado totalmente amortizado sigue en uso [ES, PDF p. 51];
  - la empresa suponía en 2019 un capex del 8 % de las ventas, por debajo de la amortización de entonces [CF_2019, PDF p. 44];
  - parte de cada reconstrucción es mejora: electrificación del 25 % en los hornos nuevos [ES, PDF p. 173].

¿Qué estructura es más coherente? **Ninguna con base** (`estructura_mas_coherente = null`, `adoptada = false`).

- S es la menos coherente si el S2C histórico ya contiene reposición, pero no queda excluida.
- H y SR1 solo se distinguen en años de crecimiento de capacidad. El crecimiento de 2021–2024 fue precio y perímetro.
- SR1 frente a SRF depende de la mezcla futura de fijo y circulante: 52,6 % de circulante en la historia frente a 13,2 % en las palancas.
- SR1 frente a SR2 depende de Q-ROIC1.

Retiro los dos argumentos de la fase C anterior: H descartada por 2025, y SRF que quita «más de lo que muestra la historia». No se sostienen como prueba (CORRECCIONES §3). «Just because you express the depreciation rate in neat numbers doesn't make it anything you really know» (PCA pp.167–168; HIM).

**Avisos de dominio.** Ninguno es material:

- `factor_de_reestimacion`: f 1,165, lejos de 2,06. Las rentabilidades reestimadas siguen en la banda del ROIC histórico.
- `terminal_r1_sin_maximo_conservado`: prudente, ≈ 0,5 € de precio de Sí.
- `s2c_inerte`: §1, punto 1.

En las variantes:

- `inversion_fija_para_crecer_negativa` sobrestima el extremo superior del rango: solo_N2, activa_R0_sin_PM1 y solo_N1, con R0, liberan ≈ 181 mm de capital fijo en el MALO, contra lo que pasó en 2020 y 2025.
- El factor llega a 1,309 en el extremo inferior (λ 1,25), aún definido.

**Objetivo (protocolo «bloqueo_del_objetivo», ensayo).** Lo condicionan PM1.estructura, PM1.familia y PM1.parametro: son materiales para el objetivo y no tienen fundamento suficiente. PM1.familia no está cubierta por el ámbito. La acción se sostiene en las 19 variantes. Tratamiento: `objetivo_bloqueado`, origen `protocolo_de_bloqueo`. Queda pendiente_de_datos, cubo Vigilar, acción null y sin precio objetivo. El valor calculado condicional es 56,02 €, dentro de un rango calculado de 51,29–65,72 € que no es un intervalo de confianza.

Información que lo desbloquearía:

- capex de 2021–2025 por destino (reposición, capacidad, descarbonización);
- coste de reconstruir hoy un horno frente a su coste histórico;
- capacidad añadida por cada reconstrucción y utilización por segmento.

## 10. Turno 2 · cierre

**Comprobación conjunta.** No existe `comprobacion_conjunta.json`: no se ejecutó porque la conclusión no es favorable y la lista D10 está vacía. `sobrevive = null` y `resultado = no_procede`. El ámbito del objetivo son solo las 19 variantes calculadas.

**Estado, cubo y acción.** Cierro en **pendiente_de_datos · Vigilar · acción null · sin precio objetivo**. El camino es este:

- La conclusión provisional es esperar, con el precio por encima del precio de Sí.
- El objetivo lo condicionan PM1.estructura, PM1.familia y PM1.parametro, que son materiales para el objetivo y no tienen fundamento suficiente.
- El protocolo declarado es «bloqueo_del_objetivo» (ensayo, no adoptado). Por eso el tratamiento es `objetivo_bloqueado`, con origen `protocolo_de_bloqueo`.

No es un dato ausente de S-19 (`alguno_material = false`): es la lectura del protocolo. La etiqueta de C104 es «pendiente de datos» (tabla cerrada del Anexo D §D.6).

C104: «Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de datos: objetivo bloqueado…) · zona caro · precio de Sí ≤ 56.02 · precio esc. MALO 44.32 · ponderado 60.70 · fundamento pendiente de datos». Lleva el rango calculado (51,29–65,72 €) y dice que no es un intervalo de confianza. No escribo ningún tamaño de posición: es de José Luis.

Distancias, con su denominador:

- 90,10 € está un 60,84 por ciento por encima de 56,02 € (diferencia ÷ precio de Sí).
- 56,02 € está un 37,83 por ciento por debajo de 90,10 € (diferencia ÷ precio).

El MALO (44,32 €) no es un suelo de valor.

**C93 = Sí.** El g del NORMAL (0,02) está por debajo de la tasa sin riesgo (2,85 %) y de r_op (8,69 %). Con un ROIC terminal del 9 %, reinvierte el 22 % del NOPAT. El terminal pesa el 47,9 %. El salto del año 11 es la pérdida de ventaja que escribo en la tesis, no un g alto.

**C103 = No.** Es un negocio cíclico, con foso estrecho y que reinvierte mucho para mantenerse.

**Tesis (B101).** Vidrala gana porque fabrica cerca del cliente y traslada la energía con retraso. Diez años de ROIC por encima del sector lo muestran (13,8 % de media en cinco años, Historia C55). Pero 90,10 € paga más que mi BUENO (78,52 €) y un 14,2 % de crecimiento anual de ventas. La espera se sostiene en todas las variantes calculadas. El precio de Sí (56,02 €; 51,29–65,72 € en las variantes) depende de una reposición de hornos que no puedo medir, así que no lo emito como objetivo.

**Tesis inversa (B102).** Defiendo el No con estos hechos:

- El mercado es maduro y en 2025 las ventas orgánicas cayeron un 5,4 % [ES, PDF p. 55, p. 94 y p. 88].
- El 19,9 % de margen de 2025 lleva 2,9 puntos de «Otros» ingresos sin explicar [ES, PDF p. 79], y la energía barata se irá al cliente [ES, PDF p. 54 y p. 56].
- Reinvierte para quedarse donde está: el capex fue 1,42 veces la amortización sin crecer (Historia L12, L8), hay 627 mm de activos amortizados por reponer [ES, PDF p. 51] y la descarbonización pide más [ES, PDF p. 168 y p. 77].
- Con el mismo perímetro, cada euro de ventas nuevas pidió ≈ 1,4 € de reinversión.
- El FCF fue negativo en 2022 (Historia I35) y el ROIC de 2016–2017 estuvo en la tasa (Historia C33:D33).
- La concentración de clientes sube: los diez mayores pasaron del ~30 % al ~38 % de las ventas [CF_2019, PDF p. 67; CF_2024, PDF p. 45].
- Crece fuera de Europa, donde el riesgo es mayor: real −20 % en 2024, deuda a CDI y Chile condicionado [ES, PDF p. 106, p. 105 y p. 85].
- Y no sé quién me mata [extracto §9]. «I'm not entitled to have an opinion unless I can state the arguments against my position better than the people who are in opposition» (PCA pp.467–468; HIM).

**Predicciones** (comprobación el 2028-03-31, unos 16 meses después de Análisis!D4; probabilidad dado el NORMAL):

1. Margen operativo de 2027 entre el 16,5 % y el 20,5 % (0,7).
2. Ventas consolidadas de 2027 entre 1.400 y 1.650 mm (0,75).
3. Capex de 2027 por encima de 1,2 veces la amortización (0,7). Esta pone a prueba la hipótesis de P-M1.

**B222 / B223.**

- B222: con la lista D10 vacía, la hipótesis fundamentada que más condiciona es Palancas!C15. Además, el objetivo queda bloqueado por P-M1 (Configuración V6.4!B36, B37 y B38).
- B223: precio y coste de energía por tonelada y segmento, cláusulas de traslado y desglose de los 43,1 mm de «Otros»; y, para P-M1, capex de 2021–2025 por destino, coste de reconstruir un horno frente a su coste histórico y capacidad añadida por cada reconstrucción.

**Qué me haría cambiar de cubo.**

- A Sí: P-M1 fundada y un precio por debajo del precio de Sí que resulte, sin cambio en el negocio y sin pérdida de cuota.
- A No: un margen por debajo del 14 % sin choque de energía, un ROIC por debajo de r dos años seguidos, o unos «Otros» no recurrentes con el margen subyacente cayendo.
- A Demasiado difícil: que el valor pase a depender de Brasil, Chile y sus divisas, que aparezca un exceso de capacidad duradero, o que la sustitución del vidrio se vea en los volúmenes.

**Comparación con la etapa 1.**

- Coincide el cubo: Vigilar en las dos, y por la misma razón.
- El precio de Sí pasa de ~48 € a 56,02 € (calculado, no emitido). Lo explican tres cambios:
  - la regla: escalera k = 3 frente a mín(MALO, ¾ ponderado);
  - el motor: B con palancas, con un NORMAL de 60,21 € frente a ~74 €;
  - la base: 31-dic-2025, sin Chile ni datos de 2026.
- La configuración experimental resta 8,73 € de precio de Sí frente al modo heredado.
- Cambia el cierre: la etapa 1 esperaba hacia 48 €; yo no emito objetivo.

De los dos errores, sigo más cerca de pagar cualquier cosa por calidad: «Since it's so obvious that investing in great companies works, it gets horribly overdone» (PCA p.214; HIM).

**Checklist (sección 17).**

- Las 68 celdas cuentan una sola historia, con siete incoherencias anotadas.
- La autocomprobación tiene diez entradas con contenido.
- Revisé los 30 datos ausentes.
- La lista D10 está vacía y lo justifico.
- Estado, cubo y acción siguen el mapa cerrado.
- C104 no lleva ningún porcentaje.
- Las tres predicciones son falsables, con fecha y probabilidad.
- La tesis inversa va con hechos.
- B222 y B223 son concretos.
- Comparo con la etapa 1 y digo qué me haría cambiar de cubo.
- Cada hecho lleva celda o página; lo demás va como juicio.

Confianza global: media. La acción es robusta en todas las variantes; el foso tiene confianza baja y P-M1 no tiene fundamento.
