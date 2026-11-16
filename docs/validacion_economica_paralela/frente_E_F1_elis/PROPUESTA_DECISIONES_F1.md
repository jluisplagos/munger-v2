# Propuesta de decisiones F1 · Elis · para aprobación

Fecha: 16-nov-2026. **Estado: propuesta. No adoptada ni implementada.**

- Elis sigue bloqueada para valoración (`pendiente_de_datos`) mientras falten datos o fundamento.
- No se adopta A1, A2 ni A1′, ni ningún valor de reinversión.
- Se conservan C48 = 108 y las decisiones E1, D3, E2 y E6.
- Ninguna recomendación se hace por su efecto en la valoración. Donde una opción lo mueve, se dice en qué sentido.

Marcas: **[P]** publicado · **[D]** derivado · **[I]** inferido · **[H]** hipótesis · **[Pol]** política (una decisión, no un dato) · **[DH]** decisión humana registrada.

Base:
- [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md), §3–§6 y §9–§10;
- [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md), E2–E5.

Las cifras son medias de 2023–25 o de la base 2025, como en el informe. No hay cifras nuevas: todas salen del informe, cuyas entradas han comprobado nueve revisiones independientes. **Las recomendaciones sí son nuevas y no están revisadas.**

---

## Resumen

| # | Cuestión | Recomendación | En qué se apoya | Decisión que necesito |
|---|---|---|---|---|
| 1 | Alternativa F1 y arrendamientos | **F1 (b): corregir la definición** del motor A, con perímetros declarados y controles (E2–E5). Arrendamiento: la amortización de los derechos de uso (ROU) sale de la reinversión; el FCF base, C48 y C49 no cambian. A1′, no. Donde salte un control, el caso no usa el motor A, como en (a) | Doble cómputo del arrendamiento [D], con una premisa [I] que es la práctica publicada de Elis [P] | Aprobar (b) con ese tratamiento, o mantener (a) |
| 2 | Intangibles adquiridos (PPA) | **La PPA no es un desembolso de reposición.** Reponer los clientes perdidos, adquiridos o no, forma parte de la reinversión necesaria (R). Margen con PPA constante. No se adopta el valor de R de A2 | No es caja [P]; en su mayor parte no es deducible [I]; la cartera se repuso orgánicamente en la ventana [P][I] | Aprobar esa política, tratar la PPA como reposición (A1) o modelizar las adquisiciones |
| 3 | Reinversión necesaria | **Conservar `pendiente_de_datos`.** El intervalo 736,0–867,2 solo mide lo que está en juego: no es una estimación ni una horquilla entre la que escoger | No se publica como importe [P]; la cota superior es una inferencia [I]; la inferior no es una cota y tiene evidencia publicada en contra [P][I] | Aprobar que siga pendiente, y decidir si se pide el dato y quién lo pide |
| 4 | Perímetros de reinversión, S2C y margen | **Un solo perímetro** para f, el ancla de S2C y el margen. Crecimiento proyectado y ancla de S2C, **los dos con adquisiciones**. Anclas numéricas pendientes de R | Matriz de coherencia de la especificación [D]; adquisiciones en todos los años [P]; reparto precio/volumen sin cuantificar [P] | Aprobar la regla y el perímetro del crecimiento: con adquisiciones u orgánico |

**Resultado del conjunto:** el motor A quedaría corregido en su definición, pero **Elis seguiría bloqueada**. Sin R no hay f, ni flujo de partida, ni ancla de S2C.

---

## 1. Alternativa F1 y tratamiento de los arrendamientos

**Recomendación: F1 (b), corregir la definición.** Política completa propuesta, para aprobar tal cual o con cambios:

> El motor A no supone que la amortización de los derechos de uso (NIIF 16) se reponga con inversión propia. La reinversión que calibra f se mide con un perímetro declarado (`perimetro_reinversion`) que excluye esa amortización. El mismo perímetro se usa en el ancla de S2C y en el margen proyectado. El FCF base (307,933), C48 = 108 y C49 = 128,1 no cambian. El perímetro `A0_total` (D&A total) solo se admite si no hay arrendamientos (D&A ROU = 0 y C49 = 0). Si falta un dato o una declaración que el perímetro exige, el caso queda «modelo no aplicable» o «incompleto» (controles V-F1a–h) y no se usa el motor A. Cada perímetro se registra con fecha, persona y motivo.

**Fundamento:**
- En la calibración el arrendamiento se cuenta una vez: los pagos, dentro del FCF base. En la proyección, dos: la amortización ROU dentro del margen y los pagos dentro de f [D].
- El exceso es de 139,4 en la base 2025 (2,9–3,1 % de las ventas). Es íntegro a crecimiento cero y en el terminal [D].
- La premisa, que el activo arrendado se repone con contratos nuevos cuyo coste son los pagos, es una inferencia [I]. Es exactamente la definición de flujo que usa Elis en sus pruebas de deterioro: «capital expenditure (including lease renewal)», sobre un EBITDA sin coste de arrendamiento [P: URD25 p.368; DEU24 p.314].

**Publicado, derivado, hipótesis:**
- [P] Pagos, amortización ROU, altas ROU no monetarias y práctica de las pruebas de deterioro.
- [D] El doble cómputo y su tamaño.
- [I] La premisa de reposición por contrato.
- [Pol] La elección de (b).

**Alternativas y consecuencias:**
- **(a) Declarar el límite** (supuesto vigente [S]): no hay doble cómputo porque no se usa el motor. Todos los casos con NIIF 16 quedan sin motor A.
- **(c) Juicio caso a caso:** sin una regla escrita no se puede auditar ni reproducir.
- **A1′ (FCF base sin el principal de arrendamientos):** es coherente en estado estacionario y es el esquema de Elis. Pero modifica C49 y la construcción registrada del FCF base (decisión del 10-nov-2026 y E6). Además, su variante de margen (después de arrendamientos) hoy no es admisible: contaría dos veces el interés de arrendamiento, 25,1 de media (N4).
- **Motor B** (f = 0 y el pasivo por arrendamientos restado): trata el arrendamiento de forma coherente. Tiene su propia incoherencia de perímetro en el coste de la deuda (C63), y la elección de motor es de la fase A.
- **Efecto en el valor:** frente a A0, la corrección sube el flujo 139,4 en la base 2025. No la recomiendo por eso, sino porque A0 es incoherente con NIIF 16 [D].

**Evidencia ausente:** por qué los pagos crecen más deprisa que las ventas (3,04 % → 3,30 % → 3,71 % de las ventas en 2023–25).
- f usa la media, 3,359 %. Con el porcentaje de 2025, el coste en la base 2025 sería 16,8 mayor.
- Esa evidencia impide proyectar con seguridad cuánto pesará el arrendamiento. Afecta igual a todas las alternativas.
- Propongo mantener la convención registrada, la media de la ventana, y declarar esa sensibilidad.

**Decisión que necesito:**
- (1a) Aprobar F1 (b) con la política del recuadro, o mantener (a).
- (1b) Mantener la media de la ventana para el peso del arrendamiento, con la sensibilidad de 16,8 declarada: sí o no.

---

## 2. Intangibles adquiridos (PPA)

**Recomendación, como política [Pol]:**
- La amortización de los intangibles adquiridos (PPA: 85,7 en 2025, de ellos 83,5 de relaciones con clientes y 2,2 de marcas) no se trata como un desembolso de reposición.
- Reponer los clientes perdidos, adquiridos u orgánicos, es parte de R por definición: según el informe, §9, R «incluye la reposición de clientes perdidos».
- Las compras de sociedades se tratan como inversión de crecimiento (cuestión 4).
- Perímetro del margen: `EBIT_NIIF16_PPA_constante`, la única combinación admisible hoy con esta política (E2).
- **No se adopta el valor de R que lleva A2 (la D&A propia).**

**Fundamento:**
- No es salida de caja [P].
- En su mayor parte no es deducible: el ingreso fiscal diferido de los intangibles equivale al 18–24 % de su amortización [P][I].
- La cartera adquirida se agota. El valor neto de las relaciones con clientes es 275,1, frente a 83,5 de amortización al año: unos 3,3 años sin compras nuevas [P][D].
- En la ventana, el crecimiento orgánico, neto de clientes perdidos, fue positivo y con efecto volumen. La cartera se repuso con un coste que ya está en el EBIT y en el capex propio [P][I].
- Si R ya incluye reponer clientes, cargar además la PPA contaría esa reposición dos veces.

**Publicado, derivado, hipótesis:**
- [P] Composición, valor neto, vidas de 4 a 14 años, altas de 2025 provisionales y contratos de cuatro años.
- [D] El agotamiento.
- [I] La no deducibilidad y la reposición orgánica en la ventana.
- [H] La reposición futura.

**Alternativas y consecuencias:**
- **A1 (PPA como reposición en caja perpetua, unos 85,7 al año):** ningún dato publicado la sostiene. Con el mismo R, el flujo de partida es 89,9 menor que con la política recomendada.
- **Modelizar las adquisiciones** (compras recurrentes como salida de caja, con su PPA): más fiel a la realidad, pero exige los datos M2 y la decisión M3, y una estructura del motor que no existe.
- **PPA decreciente según el valor neto:** hoy no es admisible (E2).
- **Efecto en el valor:** con el mismo R, la política recomendada da más flujo que A1. No me apoyo en eso, sino en la definición de R y en la evidencia. Además, mientras R siga pendiente no produce ninguna valoración.

**Evidencia ausente:** M2, la tasa de bajas de clientes (en particular de los adquiridos) y el desembolso inicial por cliente nuevo. Impide:
- cuantificar la parte de R que repone clientes;
- confirmar la política para el futuro, porque la evidencia de la ventana es parcial.

**Decisión que necesito:** (2) Aprobar como política que la PPA no es reposición en caja, que reponer clientes perdidos va dentro de R y que el margen lleva PPA constante. O, en su lugar, tratar la PPA como reposición (A1), o pedir que se modelicen las adquisiciones, que requiere M2, M3 y un cambio de motor.

---

## 3. Reinversión necesaria (R)

**Recomendación:** conservar `pendiente_de_datos` para R y, con ella, para f, el flujo de partida y el ancla de S2C de Elis.

**No hay fundamento suficiente para una estimación documentada con rango que pueda usarse** (perímetro `A3_estimado`; el control V-F1d exige fuente, método, rango y responsable):
- la cota superior es una inferencia;
- la referencia inferior no es una cota;
- nada sitúa R dentro del intervalo.

**Lo que hay:**
- **[P] No se publica ningún reparto entre mantenimiento y crecimiento.** Solo se publica:
  - que dos tercios de la inversión en lino plano mantienen el stock en circulación. Es un texto fijo, sin importe;
  - que la inversión industrial y la de lino incluyen crecimiento.

  El lino plano supone el 46,2 % de las ventas, y la proporción no se puede extender a todo el lino: dos tercios de las compras de lino serían 396, frente a 565,1 de amortización.
- **[I] Cota superior: el capex propio (867,2 de media).** Elis creció en volumen, con apoyo publicado cualitativo para 2024 y 2025, sin cifra. Deja de valer si en 2025 hubo infrainversión. Hay señales de contención del capex, que la empresa presenta como normalización.
- **[I] Referencia inferior: la D&A propia (736,0).** No está demostrada, y hay evidencia publicada en contra de usarla como caso central:
  - con inflación, reponer a coste actual cuesta más que la amortización a coste histórico;
  - los planes de las pruebas de deterioro suponen una inversión superior a la amortización histórica, ligada al plan climático.
- **[D] La V6.3 supone R igual a la D&A total (954,0).** Es más que el capex propio de unos años en que la empresa crecía: incompatible con la historia [I].

**Alternativas y consecuencias:**
- **Estimación con rango (`A3_estimado`):** solo con evidencia operativa con fuente, método, rango y responsable. Hoy no la hay.
- **Usar un extremo:**
  - R igual al capex propio (cota B, flujo de partida 339,8) no es una alternativa: supone crecimiento sin inversión;
  - R igual a la D&A propia (A2, 477,8) tiene evidencia en contra como caso central.
- **Un punto intermedio:** convertiría la falta del dato en una cifra a escoger. No lo propongo.
- **Lo que está en juego:** el flujo de partida va de 339,8 a 477,8, una diferencia de 138, el 45 % del FCF base. Los dos extremos llevan +27,9 de partidas puntuales.

**Evidencia ausente: M1**, el reparto por bloque y año:
- lino plano, resto del lino, otros artículos, inversión industrial y TI, y plan climático;
- la parte de la dotación a clientes nuevos que repone clientes perdidos;
- la fecha y la base de la proporción de los dos tercios.

Sin M1 no se puede fijar R ni, con ella, el nivel del flujo ni ningún valor del motor A para Elis.

**Decisión que necesito:**
- (3a) Aprobar que R siga en `pendiente_de_datos`, con el intervalo 736,0–867,2 solo como medida de materialidad.
- (3b) Si quieres desbloquear Elis: decidir si se pide el dato a Relación con Inversores, u otra fuente, y quién lo pide. La pregunta ya está redactada en `Diagnóstico V6!B223`. Esa gestión es tuya; yo no puedo hacerla.

---

## 4. Perímetros coherentes de reinversión, S2C y margen

**Recomendación:**
- **(i) Un solo perímetro**, declarado, para la reinversión que calibra f, el ancla de S2C y el margen proyectado. Es la matriz de E2; los controles V-F1g y V-F1h avisan si no casan. Con las recomendaciones 1 a 3: D_X igual a R (pendiente) y margen EBIT NIIF 16 con PPA constante.
- **(ii) Crecimiento proyectado y ancla de S2C, los dos con adquisiciones:**
  - Elis compra sociedades todos los años (de 82,1 a 221,7 al año en 2021–25 [P]);
  - esas compras reponen y amplían la cartera, y generan la PPA;
  - su caja no está en el FCF base: con adquisiciones en los dos lados se paga dentro de la inversión de crecimiento, lo que casa con la cuestión 2.
- **(iii) Ancla numérica de S2C pendiente**, porque depende de R.
  - Las palancas actuales (1 / 1,2 / 1,5) se anclaron en un perímetro propio (≈ 1,5) y no en C53.
  - C53 vale 9,04 y usa la D&A total [D].

**Fundamento:**
- La especificación exige que los tres perímetros describan el mismo tratamiento del arrendamiento y de la PPA (revisión, O4 y O12) [D].
- El crecimiento orgánico publicado incluye precio todos los años (en 2023, unos 9 de sus 11,8 puntos), y el reparto solo se cuantifica para 2023 [P]. Un ancla orgánica nominal sobrestima la productividad del capital en volumen [I].

**Alternativas y consecuencias:**
- **Orgánico en los dos lados** (sin adquisiciones en el ancla ni en el crecimiento): es coherente si el crecimiento proyectado es orgánico, pero exige M5, el reparto entre precio y volumen.
  - Da anclas más altas: en el perímetro de A2, 2,07–3,13 frente a 1,61.
  - Es la opción más favorable para el valor. No la recomiendo sin M5.
- **Mezclar** (ancla con adquisiciones y crecimiento orgánico, o al revés): incoherente.

**Evidencia ausente:**
- R (M1), para calcular el ancla;
- M5, para un ancla orgánica en volumen;
- M3 (orgánico o con adquisiciones) no es un dato, es una decisión.

**Decisión que necesito:**
- (4a) Aprobar la regla de un solo perímetro.
- (4b) Declarar el crecimiento proyectado de Elis como total, con adquisiciones, y el ancla de S2C con adquisiciones. O bien orgánico en los dos lados, condicionado a M5.

---

## 5. Dependencias materiales

| Dependencia | Qué es | Peso | Recomendación | Decisión |
|---|---|---|---|---|
| **Partidas puntuales** | Dentro de la ventana de calibración [P][D]: el earnout de México (cargo no monetario de −48,4 en 2023: +13,7 en f, unos 18,6 con su efecto fiscal), las plusvalías (−4,0 en f) y la plusvalía de 2025, con indemnizaciones de seguros (+18,3 en el margen inicial, m0) | +27,9 en el flujo sin crecimiento de la base 2025, igual en todas las alternativas | Una regla escrita: sacar de la ventana de calibración (f y m0) las partidas que la fuente publica como no recurrentes, con su importe, y declararlo. Efecto: −27,9 en el flujo (menos favorable) | (5a) Aprobar la regla, o mantener la calibración sin normalizar y declarar su efecto |
| **Inversión del plan climático** | Ni reposición ni crecimiento de ventas [I]. Está dentro del capex propio de la ventana, sin importe separado [P: «expenditure under the Climate plan», URD25 p.122]. Los planes de deterioro suponen por ella una inversión superior a la amortización histórica [P: URD25 p.369] | Sin importe publicado | Una categoría propia («inversión de transición»), fuera de R y del crecimiento, con su importe y su horizonte cuando se publiquen o se obtengan. Hasta entonces, pendiente. Como está dentro del capex propio, este sigue siendo cota superior de R | (5b) Aprobar la categoría propia, sin importe |
| **Peso del arrendamiento** | Pagos ÷ ventas en aumento (cuestión 1) | 16,8 en la base 2025 | Media de la ventana, con la sensibilidad declarada | (1b) |
| **Precio frente a volumen** | El reparto del crecimiento orgánico de 2024–25 no se cuantifica (M5) | Anclas de S2C orgánicas | Solo importa si el crecimiento proyectado es orgánico (cuestión 4) | Ninguna aparte |
| **Fuera de F1** (informe, §7–§8) | Ventana del tipo impositivo y escala de intereses sin endeudamiento nuevo | — | Revisión económica aparte | Ninguna ahora |

---

## 6. Coherencia del conjunto

- **Arrendamiento:** se cuenta una vez en la calibración y en la proyección (1). El FCF base, C48 = 108 y C49 no cambian, así que E6 se conserva. E1, D3 y E2 no se tocan.
- **PPA y R:** la PPA no se carga como reposición (2), y reponer clientes queda dentro de R (3). No hay doble cómputo ni hueco, siempre que R, cuando se conozca, incluya esa reposición. Es una condición de la estimación de R, no algo que añadir después.
- **Margen:** con PPA constante, la única combinación admisible con (2).
- **Perímetros:** f, el ancla de S2C y el margen usan el mismo (4). Las adquisiciones van en el ancla y en el crecimiento, no en R.
- **Bloqueo:** con R pendiente (3), f, el flujo de partida y el ancla de S2C de Elis siguen pendientes, y el control V-F1d la deja «incompleta». **Ninguna recomendación desbloquea una valoración.**
- **Sentido del valor de cada recomendación:**
  - la 1 sube el flujo frente a A0, porque corrige un error demostrado;
  - la 2 lo sube frente a A1, con el mismo R;
  - la 3 no da ninguna cifra;
  - la 4 baja el ancla frente a la orgánica;
  - la regla de partidas puntuales baja el flujo 27,9;
  - el peso del arrendamiento se declara.

  No van todas en el mismo sentido, y ninguna se apoya en su efecto.

**Qué no se adopta:** A1, A2 ni A1′ con su valor de R; ningún valor de R; ninguna valoración de Elis.

**Después de tu decisión (no iniciado):**
1. Registrar cada decisión con fecha, persona y motivo, como E1–E6.
2. Aplicarlas en la especificación y en el motor, con sus pruebas.
3. Encargar una revisión independiente de lo que cambie.

Mientras R falte, Elis sigue en `pendiente_de_datos`.
