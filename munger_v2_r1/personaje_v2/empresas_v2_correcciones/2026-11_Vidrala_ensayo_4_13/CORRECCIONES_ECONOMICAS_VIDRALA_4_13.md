# Vidrala · corrección de tres interpretaciones económicas (encargo 4.13 §8)

**Qué es.** Este documento corrige tres explicaciones de la entrega 4.12. Los documentos de la 4.12 no se modifican: son el historial, y aquí se dice qué frase deja de valer y por qué. No cambia ningún parámetro, ninguna palanca ni ninguna elección para que las cuentas cuadren con la corrección. Ninguna elección pendiente se da por firmada.

**Fuentes.**
- Expediente `…_4_12/cierre_condicionado/Vidrala` (libro evaluado, `resultados.json`, `configuracion_v64_variantes.json` y `fase_c.json`).
- `…_4_9/PRECISION_ROIC_4_9.md`.
- `resultados/crecimiento_terminal_vidrala.md`: seis recálculos nuevos con LibreOffice, sobre copias.

Cifras en millones de euros, salvo los € por acción. Se marca qué es hecho comprobado, qué es interpretación y qué es propuesta.

## 1. Q-ROIC1: qué ROIC hace coherente cada estructura

**Lo que dijo la 4.12.**
- `REVISION_ECONOMICA_VIDRALA_4_12.md` §1: «Si ese ROIC ya era neto de reposición (la pregunta Q-ROIC1, sin decidir), sobra hasta 1,06 € (SR2)».
- `INFORME_INTEGRACION_4_12.md`, «Revisión económica»: «si el ROIC de la fase B ya era neto de reposición, sobra hasta 1,06 € (SR2)».

**La definición original (hecho).** `PRECISION_ROIC_4_9.md` distingue dos lecturas del ROIC a largo plazo de la fase B:
- neto de la reposición: rendimiento de la inversión que excede el mantenimiento;
- sobre una inversión que ya la incluye.

Y asocia cada una a una estructura:
- si es lo primero, «la combinación coherente con la suma es la que **no** reestima el ROIC del terminal» (SR1);
- si es lo segundo, «la combinación coherente es la que **lo** reestima» (SR2).

**La corrección.** La frase de la 4.12 invierte esa condición.
- Un ROIC neto de reposición mide el rendimiento del capital que crece. P-M1 carga aparte el requisito de reposición. Conservar ese ROIC y sumar el requisito (SR1) no cuenta nada dos veces.
- Si el ROIC se midió sobre una inversión total contaminada por el mantenimiento, ese ROIC ya descuenta la reposición. Cargar además el requisito la contaría dos veces. Entonces hay que reestimarlo (SR2: ROIC × f). Ahí está el «sobra hasta 1,06 €» (precio de Sí de SR2, 57,08 €, frente a 56,02 € de la activa).

**Qué mide cada ROIC.**
- **ROIC de la fase B (9 % / 9 % / 12 %).** Lo fija la fase B. En el MALO y el NORMAL es la tasa por convención; en el BUENO viene de la meseta histórica, medida con la amortización a coste histórico.
- **ROIC × f de SR2 (≈ 10,5 % en el NORMAL).** Es el mismo ROIC reexpresado sobre la inversión neta de la parte que repone (f = D_hist ÷ (D_hist − Rh) = 530,0 ÷ 455,0 = 1,165).

**Lo que no cambia.** No se elige SR1 ni SR2. Ni la autoridad de la definición de la 4.9 ni el valor que da cada una deciden la elección. La pregunta Q-ROIC1 sigue abierta: hay que saber cómo se pensó el ROIC de la fase B.

## 2. ROIC terminal del 9 % y tasa de descuento

**Lo que dijo la 4.12.** `REVISION_ECONOMICA_VIDRALA_4_12.md` §2: «En la perpetuidad rinde el 9 %, igual que r, así que el crecimiento terminal no crea valor».

**Hechos.**
- La r personal es el 9 %.
- El motor B descuenta la perpetuidad a **r_op = 8,689151674 %** (Diagnóstico V6 C15). Se calcula con las entradas y no cambia aquí.
- El terminal del motor B con P-M1 carga además un requisito de reposición que crece con las ventas (convención terminal «proporcional a las ventas»).
- Valor que aporta el crecimiento perpetuo: el caso menos el mismo caso con g = 0 en los tres escenarios. Son recálculos sobre copias (`resultados/crecimiento_terminal_vidrala.md`), € por acción:

| Configuración | Δ V MALO | Δ V NORMAL | Δ V BUENO | Δ ponderado | Δ precio de Sí |
|---|---|---|---|---|---|
| activa (SR1 · Λ 1,15 · P0) | +0,61 | +0,88 | +6,52 | +1,95 | +1,57 |
| SR2 | +1,02 | +2,31 | +8,41 | +3,27 | +2,63 |
| heredado (V6.3 efectiva; r_op 8,698969 %) | +0,37 | +2,01 | +8,47 | +2,97 | +2,23 |

La activa reproduce el expediente: precio de Sí 56,02 € y ponderado 60,70 €.

**La corrección.**
- La igualdad «ROIC terminal 9 % = r 9 %» no demuestra que el crecimiento sea neutral en el motor B, porque se descuenta a r_op, que es menor que el 9 %.
- Con las configuraciones calculadas, el crecimiento perpetuo aporta valor en los tres escenarios. En el MALO y el NORMAL aporta poco.
- Tampoco vale la conclusión contraria («P-M1 introduce inversión adicional, luego el crecimiento destruye valor»). En la activa el efecto es menor que en SR2 o en el heredado, pero sigue siendo positivo.

**Interpretación.** La discontinuidad del año 11 que describe la 4.12 §2 se sostiene como hecho: la rentabilidad marginal implícita de los años 1–10 (14,7 % en el NORMAL) queda por encima del ROIC terminal (9 %). La frase «el crecimiento terminal no crea valor» se sustituye por las cifras de la tabla.

La r personal sigue en el 9 % y nada de esto cambia una palanca.

## 3. «Capex mayor que la amortización sin crecimiento» no excluye H

**Lo que dijo la 4.12.** En la fase C de `cierre_condicionado` y `cierre_bloqueo`, `configuracion_v64.mantenimiento`, que es un juicio del agente:
- «H no encaja (acredita la reposición contra la inversión para crecer, y en 2025 el exceso se dio sin crecer)»;
- «SR1 quita del crecimiento exactamente el exceso histórico por euro de ventas añadido (75,0 ÷ 476,8 = 0,157 €); SRF, al reestimar solo la inversión fija, quita unos 0,29 € por euro, más de lo que muestra la historia».

**Por qué el primer argumento no excluye H (hecho de la especificación).**
- En H, el requisito de cada año se acredita contra la inversión fija para crecer de ese año: crédito = min(requisito, inversión fija para crecer).
- En un año sin crecimiento, la inversión fija para crecer es 0, así que el crédito es min(requisito, 0) = 0 y el año paga **todo** el requisito.
- Un año como 2025 (ventas −7,8 %, −5,4 % orgánicas; capex − D&A = 55,6) es compatible con H tanto como con SR1. Por sí solo no selecciona SR1.

**Lo que distinguiría H de SR1 (interpretación).** Los años **con** crecimiento:
- en H, la reposición y el crecimiento se solapan, y la inversión del año se acerca al máximo de las dos;
- en S y SR1, se suman.

Los años de 2021 a 2024 crecieron (+9,7 %, +24,1 %, +6,1 % y +11,3 %), con capex − D&A de 23,5, 34,7, 64,5 y 51,1 y con aumentos de circulante grandes en 2022–2024. Las cuentas no separan la inversión fija para crecer de la reposición, así que con las fuentes disponibles no se puede decidir.

**Por qué la comparación SR1/SRF necesita la mezcla de fijo y circulante (hechos; denominadores explícitos).**

| Concepto | Cifra | Denominador |
|---|---|---|
| Reinversión histórica H–L (D_hist) | 530,0 | — |
| · de la cual, fija: capex − D&A + adquisiciones netas + cartera (F_hist) | 251,2 (47,4 %) | D_hist |
| · de la cual, circulante: Historia fila 14 | 278,8 (52,6 %) | D_hist |
| Parte atribuida a reposición (Rh = 0,15 × 500,2) | 75,0 | — |
| Rh sobre la reinversión total (lo que quita SR1) | 14,2 % | D_hist |
| Rh sobre la reinversión fija (lo que quita SRF: 1 − f_fija) | 29,9 % | F_hist |
| Reinversión futura por euro de ventas nuevas en el NORMAL (1 ÷ S2C 0,9) | 1,111 € | € de ventas |
| · de la cual, circulante (NWC efectivo) | 0,147 € (13,2 %) | € de ventas |
| · de la cual, fija | 0,964 € (86,8 %) | € de ventas |
| Lo que quita SR1 por euro de ventas nuevas (1,111 − 1,111 ÷ 1,165) | 0,157 € | € de ventas |
| Lo que quita SRF por euro de ventas nuevas (29,9 % × 0,964) | 0,288 € | € de ventas |

**Interpretación.**
- En la historia, SR1 y SRF quitan lo mismo: Rh = 75,0.
- En el futuro difieren porque la mezcla cambia. En la historia, el circulante es el 52,6 % de la reinversión; en las palancas futuras es el 13,2 %.
- SRF aplica la proporción que tuvo la reposición dentro de la inversión fija histórica a una inversión futura que es casi toda fija. Por eso quita más por euro de ventas nuevas.
- Que eso sea «más de lo que muestra la historia» depende de cuál de las dos mezclas describa mejor la reposición futura. Es una hipótesis sobre la mezcla, no un hecho:
  - si la reposición acompaña a la inversión fija, SRF es la coherente;
  - si acompaña a la reinversión total, lo es SR1.
- El «0,29 € por euro» de la fase C es correcto como € por euro de ventas futuras (0,288). Pero se comparó con 0,157, que en la historia es un cociente sobre las ventas de 2020–2025 y en el futuro sale de otra mezcla. Por eso los dos porcentajes de partida (14,2 % y 29,9 %) tienen denominadores distintos.

**Efecto separado de las estructuras**, de las variantes ya calculadas del expediente (precio de Sí, €):

| Estructura | Precio de Sí | Δ frente a la activa (SR1) |
|---|---|---|
| H | 61,37 | +5,35 |
| SRF | 58,43 | +2,41 |
| SR2 | 57,08 | +1,06 |
| SR1 (activa) | 56,02 | 0 |
| S | 55,52 | −0,50 |

Las cinco quedan en «caro».

## 4. Qué se revisa y qué no

- **Fase C de Vidrala.** «La más coherente es SR1» se apoyaba en dos inferencias: H descartado por 2025, y SRF descartado por quitar «más de lo que muestra la historia». Ninguna de las dos se sostiene como prueba. Al regenerar la fase C (Hito 4), el agente recibe esta corrección como información. La elección de la estructura sigue siendo su juicio, con su evidencia; la estructura activa de la configuración no se cambia para que coincida.
- **Configuración del expediente.** La justificación activa de `PM1.estructura` («SR1 se elige para la DEMOSTRACIÓN porque ejercita el factor f, D_hist con la cartera y P0») no depende de esas inferencias y sigue valiendo. La de `PM1.roic_terminal` dice que Q-ROIC1 está sin decidir y que SR2 se calcula como variante; también sigue valiendo. En los expedientes nuevos, su texto recoge la condición correcta del §1.
- **Ninguna palanca cambia** con estas correcciones. Si un juicio deja de sostenerse, su efecto se ve en las variantes ya calculadas: SR1 frente a H, SRF y SR2.
- **Pendiente (propuesta, sin firma):**
  - Q-ROIC1: cómo se pensó el ROIC de la fase B;
  - la mezcla futura de fijo y circulante que acompaña a la reposición (SR1 frente a SRF);
  - el solapamiento de reposición y crecimiento en los años con crecimiento (H frente a S y SR1).

Las tres van en el grupo 2 de decisiones de la propuesta (elecciones económicas por empresa).
