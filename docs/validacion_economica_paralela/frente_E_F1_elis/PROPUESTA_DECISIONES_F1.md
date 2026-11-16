# Propuesta de decisiones F1 · Elis · para aprobación

Fecha: 16-nov-2026, revisión 3. **Estado: propuesta. No adoptada ni implementada.**

- Elis sigue bloqueada para valoración (`pendiente_de_datos`) mientras falten datos o fundamento.
- No se adopta A1, A2 ni A1′, ni ningún valor de reinversión.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y las decisiones E1, D3, E2 y E6.
- Ninguna recomendación se hace por su efecto en la valoración. Donde una opción lo mueve, se dice en qué sentido.

**Historial.**
- La revisión 1 (`b83803c`) la revisó la revisión externa `1a07188` (F1-P1 a P4).
- La revisión 2 (`13f864f`) la revisó la revisión dirigida `8fcc7fd`: [revision/REVISION_PROPUESTA_P1_P4.md](revision/REVISION_PROPUESTA_P1_P4.md).
- **Esta revisión 3 aplica sus correcciones V1–V11.** Qué cambia, dónde y con qué prueba: [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md).
- Esta versión no está revisada todavía; se revisará externamente solo en lo afectado.
- La especificación coherente con ella está en [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md), E2–E6, E8 y E9.

Marcas: **[P]** publicado · **[D]** derivado · **[I]** inferido · **[H]** hipótesis · **[Pol]** política (una decisión, no un dato) · **[B]** resultado de una búsqueda: lo que no se ha encontrado publicado · **[LECTURA]** cifra publicada leída en el PDF que no está en el CSV verificado · **[DH]** decisión humana registrada.

Cifras:
- las del informe ([INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md)), medias de 2023–25 o base 2025;
- las nuevas salen de dos scripts:
  - `resultados/copia_investigacion_f1.md`, una copia de investigación con cifras verificadas, que no es una entrada registrada ni una valoración. Las [LECTURA] llevan documento, página y literal, y el script comprueba que están en su página del PDF;
  - `resultados/controles_sinteticos_f1.json`, ejemplos de política con importes ficticios, que no son datos de Elis.
- «Año 11» es el flujo del año 11 del motor, el del terminal; no es un valor terminal.

---

## Tabla única de decisiones

| ID | Recomendación | Naturaleza | Condición de aplicación | Carencia | Texto exacto que se pide aprobar |
|---|---|---|---|---|---|
| **1a** | F1 (b) en lo que toca a los arrendamientos: el perímetro de la reinversión que calibra f excluye la amortización de los derechos de uso (ROU). FCF base, C48 y C49 sin cambios. `A0_total` solo sin arrendamientos | Doble cómputo [D]; premisa de reposición por contrato [I], que es la práctica publicada de Elis en sus pruebas de deterioro [P]; elección de (b) [Pol] | Solo la definición del motor. Los demás controles y la regla de un solo perímetro se aprueban con su decisión: ver la columna «Controles» de la tabla de severidad. Elis sigue bloqueada por R (3a) | Ninguna para la corrección del arrendamiento. La tendencia de los pagos, en (1b) | «Apruebo F1 (b) en lo que toca a los arrendamientos: el perímetro de la reinversión que calibra f excluye la amortización de los derechos de uso; el FCF base (307,933), C48 = 108 y C49 = 128,1 no cambian; `A0_total` solo se admite sin arrendamientos; se aplican V-F1a, V-F1b y V-F1e con la severidad de E5. No fija R ni libera la valoración de Elis.» |
| **1b** | La media 2023–25 del arrendamiento es solo una referencia de ensayo y la convención registrada, **no un peso futuro identificado**. Sensibilidad con el peso de 2025, por partes: pagos, −16,8 en el flujo sin crecimiento (A0, A1 y A2); amortización ROU que devuelve f, +10,1 (A1 y A2); suma en A1 y A2, **−6,7** | Pagos, amortización y ventas [P]; sensibilidad [D]; uso de la media [H] | Valores de prueba y diagnósticos. En una valoración, el peso proyectado es una hipótesis declarada | Por qué los pagos crecen más deprisa que las ventas: 3,04 % → 3,30 % → 3,71 % | «Apruebo que la media 2023–25 de los pagos y de la amortización de los derechos de uso se use como referencia de ensayo y convención declarada, con su sensibilidad a la vista (−16,8 de los pagos; +10,1 de la amortización en A1 y A2; −6,7 en total en A1 y A2); no la apruebo como estimación del peso futuro.» |
| **2** | La PPA no es un desembolso de reposición. El coste de conservar y reponer clientes se cobra una sola vez, donde está: el gasto comercial, en el margen; la inversión propia para los clientes que sustituyen a los perdidos, en R; las compras de cartera necesarias, si se documentan, en R o como término explícito. El margen lleva la PPA y la amortización ROU **como proporción constante de las ventas**, la misma que devuelve f | PPA no monetaria [P]; mayoritariamente no deducible [I]; en la ventana, las ventas se sostuvieron sin compras importantes [P][I] (el efecto de las compras pequeñas está dentro del crecimiento orgánico); proyección [H]; correspondencia [Pol] | Tabla de correspondencia del §2 sin omisiones ni dobles cargos en los costes que tocan estas decisiones. R, cuando exista, declara cómo incluye la reposición. Controles V-F1f y V-F1h | M2: tasa de bajas y desembolso por cliente nuevo. En Elis, efectos de escala declarados: la PPA, +4,2, sube el flujo de A2; la ROU, −10,1, baja el de A1 y A2 | «Apruebo como política: (i) la amortización PPA no se trata como desembolso de reposición; (ii) el gasto comercial corriente queda en el margen y no se añade a R; (iii) la inversión propia para sustituir clientes perdidos forma parte de R; (iv) las compras de cartera necesarias para mantener las ventas, si se documentan, se cobran en R o como término explícito, nunca solo como crecimiento; (v) el margen proyectado lleva la PPA y la amortización de los derechos de uso como proporción constante de las ventas, la misma que devuelve f, con sus efectos de escala declarados; se aplican V-F1f y V-F1h.» |
| **3a** | R sigue en `pendiente_de_datos`. Perímetro: R = R_propia + R_compras (+ transición de sostenimiento). La guarda compara cada parte con su caja. El intervalo 736,0–867,2 es de R_propia más la transición y solo mide la materialidad bajo (4b) | Reparto no publicado [B]; cota superior [I]; la referencia inferior no es una cota y tiene evidencia publicada en contra [I][P] | Controles V-F1c y V-F1d | M1: reparto por bloque y año, con el plan climático. Si las compras no son solo de crecimiento, R_compras, que está fuera del capex propio, se añade a R | «Apruebo que R siga en `pendiente_de_datos`, con el perímetro del §3; que el intervalo 736,0–867,2 solo mida la materialidad de R_propia más la transición; y que se apliquen V-F1c y V-F1d con la severidad de E5.» |
| **3b** | Elegir cómo se intenta obtener M1, M2, M6 y los datos del plan climático. Las preguntas están preparadas; su envío no lo autoriza este encargo | Gestión [Pol] | — | M1, M2, M6 y el plan climático | «Para M1, M2, M6 y el plan climático elijo una o varias de estas vías: (i) pedir el dato a Relación con Inversores, por quien yo designe; (ii) buscar en fuentes públicas que no están en la base (presentaciones de mercado de capitales, transcripciones de resultados); (iii) encargar una estimación documentada con las exigencias de V-F1d; (iv) mantener el bloqueo. Mientras no haya dato o estimación documentada, R sigue pendiente.» |
| **4a** | Un solo perímetro declarado para la reinversión que calibra f, el ancla de S2C, el margen proyectado **y el ROIC del terminal**. Si no casan, el caso no se usa para una conclusión. La comparación numérica del terminal es la que el libro ya tiene (Convenciones V6.3 §3; `Diagnóstico V6`, bloque 10), con su umbral; no se añade otra | Matriz de coherencia [D]; regla [Pol] | Las palancas de S2C y de ROIC declaran su perímetro. Controles V-F1g y V-F1k | Anclas numéricas pendientes de R. En Elis, las palancas no declaran perímetro | «Apruebo que f, el ancla de S2C, el margen proyectado y el ROIC del terminal usen un solo perímetro declarado, y que un caso cuyos perímetros no casan no se use para una conclusión; se aplican V-F1g y V-F1k con la severidad de E5, y la comparación del terminal es la del bloque 10 del libro, con su umbral vigente.» |
| **4b** | **No fijar todavía la clasificación de las compras de sociedades.** El apoyo publicado de la hipótesis «las compras son crecimiento» es parcial. El crecimiento orgánico solo excluye las compras importantes; las pequeñas están dentro (31,5 al año de media en 2023–25, el 10,2 % del FCF base). Mientras falte M6, V-F1j bloquea. La hipótesis queda como alternativa declarada | Definición del crecimiento orgánico y crecimiento orgánico positivo [P]; ventas sostenidas sin compras importantes en la ventana [I]; finalidad de las compras pequeñas, no publicada [B]; futuro [H] | Con (2)(iv): las compras de reposición que se documenten van a R o a un término explícito | M6: finalidad de las compras pequeñas y crecimiento orgánico sin ellas. M5: precio frente a volumen | Opción A: «Mantengo pendiente la clasificación de las compras de sociedades hasta conocer M6; V-F1j bloquea.» Opción B: «Apruebo como hipótesis declarada, no como dato, que las compras de sociedades de Elis son inversión de crecimiento, sabiendo que su apoyo publicado es parcial (las compras pequeñas están dentro del crecimiento orgánico); el crecimiento proyectado y el ancla de S2C se miden con adquisiciones; a crecimiento cero no se compra nada; cada millón anual de compras que fuera de reposición bajaría el flujo sostenible en un millón; se revisa si se obtiene M6.» |
| **5a** | No deducir el 27,936, que es un diagnóstico. Normalizar solo con ajustes concretos y regla fiscal. **N1:** los ajustes de earnout sin efecto fiscal; con la convención registrada del τ de cinco años, −11,6 en el flujo sin crecimiento y −18,6 en el año 11 NORMAL; con el τ de la ventana, −9,1. **N2:** las bajas de 2025 con seguros, pendiente. El resto de la nota 4.6 no se normaliza | Partidas [P]; no deducibilidad del earnout [P]; pago del earnout en las adquisiciones, fuera del FCF base [P]; vínculo entre las bajas y los seguros [I]; regla y alcance [Pol] | N1 con la clasificación de las compras que se decida (4b o M6) y con m_obj declarado sin esos ajustes. No cambia los históricos ni las entradas registradas: fila de ajustes con fuente y regla. Control V-F1l | N2: fiscalidad, caja cobrada y reposición de los activos. La actualización del earnout y los ajustes de 2021–22, publicados pero fuera del CSV verificado | «Apruebo la regla N1: los ajustes de earnout de la nota 4.6 se sacan del EBIT y del resultado antes de impuestos de su año, sin efecto en el gasto por impuesto, con su registro, [solo en la ventana 2023–25 / también en 2021–22, que solo entran en el τ de cinco años]. Su efecto depende de la convención del τ de proyección (E8.1) y se declara con ella. N2 queda pendiente. Ninguna otra partida se normaliza por su etiqueta. El 27,936 se conserva como diagnóstico. Se aplica V-F1l.» Alternativa: «Mantengo la calibración sin normalizar y declaro su diagnóstico.» |
| **5b** | La inversión de transición (plan climático) se clasifica por su **finalidad documentada**, con su caja cobrada una sola vez en la ventana, los años 1–10 y el año 11. Si se cobra como término explícito, sale del denominador del ancla de S2C. Sin importe u horizonte, la conclusión afectada queda pendiente. Nunca cero por defecto ni perpetua por su nombre | Gasto del plan dentro del capex [P]; planes de deterioro con inversión superior a la amortización histórica [P]; clasificación [Pol] | Forma parte de la estimación de R (V-F1d). Control V-F1i | Importe, horizonte y finalidad del plan (M1) | «Apruebo que la inversión de transición se clasifique por su finalidad documentada, con su caja cobrada una sola vez en la ventana, los años 1–10 y el año 11, fuera del ancla de S2C cuando se cobre como término explícito, y que sin importe u horizonte la conclusión afectada quede pendiente; se aplica V-F1i.» |

**Resultado del conjunto.**
- El motor A quedaría corregido en su definición, pero **Elis seguiría bloqueada**: sin R no hay f, ni flujo de partida, ni ancla de S2C, ni compatibilidad del terminal.
- Ninguna decisión pide elegir una cifra para sustituir evidencia ausente. Lo que queda abierto se ofrece como opción explícita:
  - las dos opciones de (4b);
  - el alcance de N1 en (5a);
  - las vías de (3b).

### Severidad de los controles (E5)

| Severidad | Qué significa | Controles |
|---|---|---|
| **BLOQUEA** | El resultado del motor A no se usa para una conclusión. Puede calcularse y mostrarse como diagnóstico, rotulado | V-F1a (sin umbral adoptado: con cualquier importe), V-F1b, V-F1d, V-F1e, V-F1g, V-F1h, V-F1i, V-F1j, V-F1k (perímetro sin declarar o distinto), V-F1l; V-F1c sin justificación |
| **AVISO** | Se muestra, no bloquea y no acredita coherencia | V-F1c con justificación documentada; V-F1k cuando el salto del terminal supera el umbral del libro (`Diagnóstico V6!C179`, hoy 5 puntos, ajustable), como ya hace el bloque 10 |
| **INFORMA** | Información para quien decide | V-F1f (agotamiento de la PPA y efectos de escala de la PPA y de la ROU); V-F1k (comparación del terminal por debajo del umbral, y la igualdad exacta con el factor (1+g∞)) |

**Qué decisión aprueba cada control:**
- (1a): V-F1a, V-F1b y V-F1e;
- (2): V-F1f y V-F1h;
- (3a): V-F1c y V-F1d;
- (4a): V-F1g y V-F1k;
- (4b) o M6: V-F1j;
- (5a): V-F1l;
- (5b): V-F1i.

Un umbral de materialidad para V-F1a sería una decisión aparte. No propongo ninguna cifra; el 0,5 % de la versión 1 no se adopta. El umbral del terminal es el que el libro ya tiene, y esta propuesta no lo cambia.

---

## 1. Alternativa F1 y arrendamientos (1a, 1b)

**Política propuesta (1a):**

> El motor A no supone que la amortización de los derechos de uso (NIIF 16) se reponga con inversión propia. La reinversión que calibra f se mide con un perímetro declarado (`perimetro_reinversion`) que excluye esa amortización. El FCF base (307,933), C48 = 108 y C49 = 128,1 no cambian. `A0_total` (D&A total) solo se admite sin arrendamientos (D&A ROU = 0 y C49 = 0). V-F1a, V-F1b y V-F1e se aplican con la severidad de E5. Cada perímetro se registra con fecha, persona y motivo.

La regla de un solo perímetro (f, ancla de S2C, margen y ROIC del terminal) es la decisión (4a); los demás controles van con su decisión (tabla de severidad).

**Fundamento:**
- En la calibración, el arrendamiento se cuenta una vez: los pagos están dentro del FCF base. En la proyección se cuenta dos veces: la amortización ROU en el margen y los pagos en f [D].
- El exceso es de 139,4 en la base 2025 y es íntegro a crecimiento cero y en el año 11 [D]. Casos sintéticos: arrendamiento una vez, 68; A0, 58 en todos los años y en el año 11 (P4d).
- La premisa es que el activo arrendado se repone con contratos nuevos, cuyo coste son los pagos [I]. Es la definición de flujo de las pruebas de deterioro de Elis: «capital expenditure (including lease renewal)», sobre un EBITDA sin coste de arrendamiento [P: URD25 p.368; DEU24 p.314]. Esa práctica apoya contar el coste una vez; no valida por sí sola todo el flujo al accionista del motor A.

**Alternativas y consecuencias:**
- **(a) Declarar el límite** (supuesto vigente): todos los casos con NIIF 16 quedan sin motor A.
- **(c) Juicio caso a caso:** sin regla escrita, no se puede auditar ni reproducir.
- **A1′ (FCF base sin el principal):** cambia C49 y la construcción registrada del FCF base (decisión del 10-nov-2026 y E6); su variante de margen después de arrendamientos contaría dos veces el interés de arrendamiento, 25,1 de media.
- **Motor B:** tiene su propia incoherencia de perímetro en el coste de la deuda (C63); la elección de motor es de la fase A.
- **Efecto en el valor:** frente a A0, la corrección sube el flujo 139,4 en la base 2025. No la recomiendo por eso, sino porque A0 es incoherente con NIIF 16.

**Peso del arrendamiento (1b).** f aplica la media de la ventana a dos cosas: los pagos (3,3589 % de las ventas) y, en A1 y A2, la amortización ROU que devuelve (2,9057 %). m0 lleva la amortización ROU real de 2025 (3,1167 %).

| Con el peso de 2025 en… | A0 | A1 y A2 |
|---|---|---|
| los pagos (3,7087 %) | −16,778 | −16,778 |
| la amortización ROU que devuelve f | — | +10,118 |
| **las dos cosas** | **−16,778** | **−6,660** |

Fuente: `copia_investigacion_f1.md`; coincide con la revisión dirigida. La media es una referencia de ensayo y una convención, no un dato del peso futuro. No se elige otro punto.

---

## 2. Correspondencia de costes: PPA, reposición de clientes y adquisiciones (2, 4b)

**Dónde se cobra cada coste.** De los costes que tocan estas decisiones, ninguno se omite ni se cobra dos veces, tampoco a crecimiento cero. Impuestos e intereses quedan fuera de F1 (E8). Las cesiones y subvenciones, las provisiones y el SBC están en f (informe, §4.2) y estas decisiones no los cambian.

| Coste o desembolso | Ventana (calibración) | Años 1–10 | Año 11 | No admitido |
|---|---|---|---|---|
| Pagos de arrendamiento | FCF base (C48 y C49) | En f, proporcional a las ventas | En f | Cobrar además la amortización ROU como reposición (A0) |
| Amortización ROU | EBIT (no es caja) | En el margen, como proporción constante; se devuelve en f al excluirla de D_X | Igual | Tratarla como reposición |
| Gasto comercial corriente | EBIT y FCF base | En el margen | En el margen | Añadirlo a R (caso P2f) |
| Capex propio necesario, incluida la dotación a los clientes que sustituyen a los perdidos | FCF base (capex) | R_propia, en f | R_propia, en f | Excluirlo de R o cobrarlo también como crecimiento |
| Compras de cartera necesarias para mantener las ventas, si se documentan | Fuera del FCF base | R_compras, en f (solo con `A3_estimado`), o término explícito, **fuera del denominador del ancla** | Igual | Cobrarlas solo como crecimiento (P2a, P4c) o también en el ancla (P2c, V2f) |
| Compras de crecimiento, con sus gastos de transacción | Fuera del FCF base; los gastos de transacción, en el EBIT | ΔV/S2C, con el ancla con adquisiciones; los gastos de transacción quedan en el margen | g∞/ROIC, con el ROIC con adquisiciones | Contarlas en R. Los gastos de transacción, 1,5 / 5,2 / 2,4, se siguen cobrando a crecimiento cero: es pequeño y prudente |
| PPA | EBIT (no es caja) | En el margen, como proporción constante; devuelta en f (A2) | Igual | Cobrarla como reposición (A1) sin dato; PPA en euros o decreciente con A2 (P2h, P2i) |
| Inversión de transición | Dentro del capex propio y del FCF base | Según su finalidad (§5.2): en R, proporcional a las ventas; término explícito con importe y horizonte, fuera del ancla; o crecimiento, dentro del ancla | En R: en f. Término explícito: solo si es permanente. Crecimiento: g∞/ROIC | Excluirla de toda salida; cero por defecto; perpetua por su nombre (P1a–P1e); término explícito dentro del ancla (V2a) |
| Ajustes normalizados (N1) | Fuera del EBIT y del BAI de su año, sin efecto fiscal. Su caja está en las adquisiciones [P] | — | — | Deducir el diagnóstico 27,936 |
| Partidas recurrentes de la nota 4.6 | EBIT y FCF base | En el margen; m_obj se declara con ellas | Igual | Normalizarlas por su etiqueta |
| Inversión de crecimiento propia y circulante | FCF base | ΔV/S2C | g∞/ROIC | — |

**Reposición de clientes.** El coste de conservar y reponer clientes tiene hasta tres partes de caja:
- **(a) Gasto comercial:** en el margen, no en R.
- **(b) Inversión propia para los clientes nuevos que sustituyen a los perdidos:** en R_propia. Es el «initial outlay required to set up a new customer» [P: URD25 p.312].
- **(c) Compras de cartera que reponen ventas perdidas:** en R_compras o en un término explícito.

«Reponer clientes va en R» se refiere a (b) y, si existe, a (c). «Su coste ya está en el EBIT y el capex» describe la ventana: (a) y (b) están pagados ahí, y por eso la PPA no es un coste adicional. Que no haya (c) es la hipótesis de (4b), cuyo apoyo es parcial (abajo).

**PPA y amortización ROU (2).**
- [P] La PPA de 2025, 85,7, son relaciones con clientes (83,5) y marcas (2,2). Vidas de 4 a 14 años; cartera neta de 275,1; altas de 2025 provisionales.
- [D] Sin compras nuevas, la cartera se agotaría en unos 3,3 años al ritmo actual.
- [I] No es caja y en su mayor parte no es deducible: el ingreso fiscal diferido de los intangibles equivale al 18–24 % de su amortización.
- **«Constante» significa constante como proporción de las ventas.** f es una proporción de las ventas por construcción. Una partida que no es caja solo se anula en el flujo si el margen la lleva en la misma proporción que f devuelve (P2g). En euros, fija o agotándose, no casa (P2h y P2i). Vale para la PPA y para la amortización ROU, que f también devuelve en A1 y A2.
- **Efectos de escala en Elis** (`copia_investigacion_f1.md`; la proporción constante es una convención [H]):

| | Lo que devuelve f (media de la ventana) | Lo que lleva m0 (2025) | Diferencia sobre las ventas de 2025 | Sentido |
|---|---|---|---|---|
| PPA (A2) | 1,8743 % · 89,906 | 1,7866 % · 85,7 | +4,206 | Sube el flujo sin crecimiento de A2 |
| Amortización ROU (A1 y A2) | 2,9057 % · 139,382 | 3,1167 % · 149,5 | −10,118 | Baja el flujo sin crecimiento de A1 y A2 |
| **Las dos, en A2** | | | **−5,913** | Lo baja |

**Alternativas:**
- **A1 (PPA como reposición en caja perpetua, unos 85,7 al año):** ningún dato publicado la sostiene. Con el mismo R, el flujo de partida es 89,9 menor.
- **Modelizar las adquisiciones** como salida de caja, con su PPA: exige M2, M6 y otra estructura del motor.
- **Efecto en el valor:** con el mismo R, la política recomendada da más flujo que A1. Mientras R siga pendiente, no produce ninguna valoración.

**Compras de sociedades (4b).**
- **Lo publicado:**
  - [P] La definición: el crecimiento orgánico «is calculated excluding (i) the impacts of changes in the scope of consolidation of "major acquisitions" and "major disposals" […]». Son «major» las sociedades con más de 5,0 millones de ingresos anuales en Francia y de 3,0 en los demás países (URD25 p.313; la misma definición en DEU24 p.259 y URD23 p.267). **El efecto de las compras pequeñas está dentro del crecimiento orgánico publicado.** El crecimiento externo publicado es solo el de las importantes.
  - [P] Crecimiento orgánico positivo todos los años de 2021–2025: 7,4 %, 21,0 %, 11,8 %, 5,2 % y 3,8 %. Tuvo efecto volumen publicado en 2024 y 2025, sin cifra; en 2023, unos 9 de los 11,8 puntos fueron de precio. Crecimiento externo: 3,1 / 1,8 / 1,2 / 1,8 % en 2022–2025.
  - [P][LECTURA] Composición de las adquisiciones netas del estado de flujos (nota 2.4; DEU24 p.288; URD25 p.342 y p.341):

    | | 2023 | 2024 | 2025 | Media |
    |---|---|---|---|---|
    | Adquisiciones netas | 82,1 | 183,3 | 117,6 | 127,7 |
    | de ellas, earnouts y pagos aplazados | 34,4 | 93,9 | 23,3 | 50,5 |
    | de ellos, Lavartex (México, comprada en 2022) | 31,4 | 83,2 | 19,7 | 44,8 |
    | flujo neto de las «otras adquisiciones» | 35,3 | 22,0 | 37,3 | 31,5 |

    Ingresos anuales de las «otras adquisiciones»: 9,1 en 2024 (9 compras) y 19,8 en 2025 (16 compras) (URD25 p.341 y p.339). La empresa las describe así: «These bolt-on acquisitions help to consolidate the Group's position in these various countries and/or to pursue the development of its pest control services» (URD25 p.339).
- **Lo que se infiere [I]:** en la ventana, las ventas se sostuvieron **sin compras importantes**.
- **Lo que no se sabe [B]:**
  - si las bajas se repusieron sin compras;
  - qué parte del efecto volumen procede de las compras pequeñas;
  - si estas reponen o amplían cartera («consolidar la posición» puede ser cualquiera de las dos).
- **Consecuencia de la hipótesis «las compras son crecimiento»:** a crecimiento cero no se compra nada.
- **Sensibilidad:** cada millón anual de compras que fuera de reposición bajaría el flujo sostenible en un millón, también en el año 11 (caso P2a y revisión dirigida, S2d). Importes publicados de referencia, que no son cifras que elegir para R_compras:
  - 31,5 de media para las «otras adquisiciones», que por definición están dentro del crecimiento orgánico;
  - 127,7 para todas. Es una referencia extrema con evidencia en contra: 134,3 de los 383,0 de la ventana son pagos aplazados de una compra de 2022.
- **Recomendación:** no fijar todavía la clasificación (opción A). La hipótesis queda como alternativa declarada (opción B), con su apoyo parcial.
- **Lo observable:** la condición de revisión de la versión anterior («si el crecimiento orgánico en volumen deja de ser positivo») no se puede observar con lo publicado: no hay cifra de volumen, y el orgánico incluye esas compras. Se sustituye por «si se obtiene M6».
- **Ancla con adquisiciones o sin ellas:**
  - orgánica en los dos lados: exige M5 y da anclas más altas (en A2, de 2,07 a 3,13, frente a 1,61). Es la opción más favorable para el valor, y no la recomiendo sin M5;
  - mezclar los dos lados es incoherente.

---

## 3. Reinversión necesaria (3a, 3b)

**Recomendación:** R sigue en `pendiente_de_datos` y, con ella, f, el flujo de partida, el ancla de S2C y la compatibilidad del terminal de Elis.

**Perímetro de R:**
- R = **R_propia** + **R_compras** + la inversión de transición que se clasifique como sostenimiento (5b);
- R_propia: el capex propio necesario para sostener las ventas a volumen constante, incluida la dotación a los clientes que sustituyen a los perdidos;
- R_compras: las compras de cartera necesarias para mantener las ventas. Cero si se aprueba la opción B de (4b). Solo cabe en D_X con el perímetro `A3_estimado`; con `A1_sin_ROU` o `A2_propio` iría como término explícito, fuera del ancla (E3 y E4);
- R no incluye el gasto comercial, que está en el margen.

**Guarda (V-F1c):** R_propia frente al capex propio, y R_compras frente a las compras. Con R = 29 = 20 + 9 y capex propio 20, la guarda anterior dispara sin infrainversión y la propuesta no. Salta si R_propia supera el capex propio o R_compras las compras (`controles_sinteticos_f1.json`, `guardas_V_F1c`).

**No hay fundamento suficiente para una estimación con rango que pueda usarse** (`A3_estimado`; V-F1d exige fuente, método, rango, responsable y el tratamiento de la reposición de clientes y de la transición):
- **[B]** La búsqueda (informe, §6.1) no encontró ningún reparto publicado entre mantenimiento y crecimiento.
  - Solo hay un texto fijo, sin importe: dos tercios de la inversión en lino plano mantienen el stock en circulación [P].
  - El lino plano es el 46,2 % de las ventas, y la proporción no puede extenderse a todo el lino: dos tercios de sus compras serían 396, frente a 565,1 de amortización.
- **[I] Cota superior de R_propia más la transición: el capex propio, 867,2 de media.** Elis creció en volumen, con apoyo publicado cualitativo en 2024 y 2025. La cota incluye la transición, que está dentro del capex. No acota R_compras, que está fuera del capex. Dejaría de valer si en 2025 hubo infrainversión; hay señales de contención del capex que la empresa presenta como normalización.
- **[I] Referencia inferior: la D&A propia, 736,0.** No es una cota, y hay evidencia publicada en contra de tomarla como caso central:
  - con inflación, reponer cuesta más que la amortización a coste histórico;
  - los planes de deterioro suponen una inversión superior a la amortización histórica [P: URD25 p.369].
- **[D]** La V6.3 supone R igual a la D&A total, 954,0: más que el capex propio de unos años en que la empresa crecía.

**Alternativas:**
- Usar un extremo:
  - capex propio (cota B, flujo de partida 339,8): supone crecimiento sin inversión;
  - D&A propia (A2, 477,8): tiene evidencia en contra como caso central.
- Un punto intermedio convertiría la falta del dato en una cifra a escoger. No lo propongo.
- **Lo que está en juego:**
  - bajo la opción B de (4b), de 339,8 a 477,8 en el flujo de partida: 138, el 45 % del FCF base;
  - si alguna compra fuera de reposición, R_compras se añadiría a eso (media de las adquisiciones, 127,7; capex propio más adquisiciones, 994,8 [D]);
  - los extremos llevan las partidas de la ventana sin normalizar (§5.1).

**Evidencia ausente:**
- **M1:** reparto por bloque y año (lino plano, resto del lino, otros artículos, industrial y TI, plan climático con su importe, horizonte y finalidad); la base y la fecha de los dos tercios;
- **M2:** la parte de la dotación a clientes nuevos que repone clientes perdidos;
- **M6:** la finalidad de las compras pequeñas y el crecimiento orgánico sin ellas.

**Preguntas preparadas, no enviadas** (respuesta a la revisión de la propuesta, §6, y RESPUESTA_CORRECCIONES_V1_V11, V1): reparto del capex; plan climático; bajas de clientes y desembolso por cliente nuevo; finalidad de las compras pequeñas; indemnizaciones de seguros de 2025. La de M1 ya está redactada en `Diagnóstico V6!B223`. La vía es la decisión (3b).

---

## 4. Perímetros coherentes: f, S2C, margen y terminal (4a, 4b)

**Recomendación (4a):** un solo perímetro declarado para:
- la reinversión que calibra f;
- el ancla de S2C de los años 1–10;
- el margen proyectado;
- el ROIC del terminal.

Si no casan, el caso no se usa para una conclusión: V-F1g, V-F1h y V-F1k bloquean.

**El ancla de S2C solo cuenta inversión de crecimiento.** Lo que se cobra fuera de ΔV/S2C y no está en D_X (una transición o unas compras de reposición cobradas como término explícito) sale de su denominador. Si no, con crecimiento se cobra dos veces:
- casos V2a y V2f, con el ancla calculada con la fórmula anterior;
- casos V2b y V2g, coherentes con la corregida (E4).

**El terminal no usa S2C.** Reinvierte g∞/ROIC del NOPAT, antes de f: V₁₀·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f].
- El ROIC compatible con esta propuesta es el rendimiento de la inversión nueva, medido:
  - sobre el NOPAT del perímetro del margen;
  - sobre el capital de crecimiento del perímetro del ancla de S2C: con adquisiciones si así se decide; sin la ROU, porque el arrendamiento se paga en f; y sin R, porque la reposición está en f.
- **Comparación numérica: la del libro.** Convenciones V6.3 §3: «En el año 11 la rentabilidad del capital pasa de S2C·m_obj·(1−τ) a ROIC; el salto se muestra en Diagnóstico V6, bloque 10, y avisa si supera C179». Esta propuesta no añade otra comparación ni otro umbral.
- **Igualdad exacta.** El año 11 cobra exactamente ΔV/S2C si ROIC = (1+g∞)·m_obj·(1−τ)·S2C. La fórmula del libro difiere solo en el factor (1+g∞): con un salto nulo según el libro, el año 11 cobra (1+g∞) veces ΔV/S2C (caso P4e). Se informa como precisión, sin consecuencia propia.

**Palancas actuales de Elis** (`copia_investigacion_f1.md`; libro, `Diagnóstico V6`, filas 176–179; sin estimar ningún ROIC nuevo):

| | ROIC (fila 177) | Rentabilidad marginal del libro (fila 176) | Salto del libro, puntos | Salto con la igualdad exacta, puntos | Inversión del año 11 con ROIC − con S2C |
|---|---|---|---|---|---|
| MALO | 7 % | 7,4739 % | −0,47 | −0,55 | +4,45 |
| NORMAL | 10 % | 10,6770 % | −0,68 | −0,89 | +10,28 |
| BUENO | 12 % | 14,4140 % | −2,41 | −2,77 | +28,96 |

- Los tres saltos están por debajo del umbral del libro (5 puntos): V-F1k informa.
- El ROIC de las palancas cobra en el año 11 algo más de inversión que su propia S2C.
- Las palancas S2C (1 / 1,2 / 1,5) se anclaron en un perímetro propio (≈ 1,5), no en C53; el C53 de A0 es 9,04. Su perímetro no está declarado y depende de R: **compatibilidad del terminal pendiente.**

**Fundamento:**
- La especificación exige que los perímetros describan el mismo tratamiento del arrendamiento, de la PPA y de las compras [D].
- El crecimiento orgánico publicado incluye precio todos los años y el efecto de las compras pequeñas [P]. Un ancla orgánica nominal sobrestima la productividad del capital en volumen [I].

---

## 5. Dependencias: normalización, inversión de transición y otras

### 5.1 Partidas de la ventana (5a)

El **27,936** es un diagnóstico del cálculo actual:
- +13,675 de earnout y otros no monetarios dentro de f;
- −4,032 de plusvalías dentro de f;
- +18,293 de la plusvalía de 2025 dentro de m0.

No es el efecto de ninguna regla, por tres razones:
- toma las líneas del estado de flujos de los tres años, que incluyen otros elementos no monetarios y las pérdidas ordinarias por bajas;
- las quita de f antes de impuestos;
- no quita la plusvalía de 2025 del NOPAT que calibra f.

**Ajustes concretos** (perímetro A0; la variación es idéntica en A1 y A2):

| Ajuste | Fuente | Original → normalizado | Motivo | Fiscalidad | Caja y dependencias | Flujo sin crecimiento · año 11 NORMAL |
|---|---|---|---|---|---|---|
| **N1** · ajustes de earnout 2023–25 | Nota 4.6: −48,9 / +8,7 / −0,2 [P: DEU24 p.296; URD25 p.350]. En 2023, revaluación por la revisión al alza de las perspectivas de la compra de México [P: DEU24 p.296; URD23 p.302] | Sin el ajuste, en el EBIT y el BAI de su año | Revaluación del precio de adquisiciones, no coste de explotación; no monetaria al reconocerse; simétrica en los tres años | No deducible [P]. Línea propia de la conciliación fiscal: (15,8) en 2023, 0,8 en 2024 y (0,2) en 2025 (DEU24 p.337; URD25 p.392). Cuadra los tres años al 25,83 % con la actualización: −15,834 / +0,801 / −0,232 [D]. Regla: gasto sin cambios, tipo recalculado | Pagos de earnouts y aplazados dentro de «Acquisition of subsidiaries, net of cash acquired», en inversión, fuera del FCF base [P: nota 2.4, DEU24 p.288; URD25 p.342 y p.341]. México liquidado en 2024 y 2025 [P: URD25 p.352]. Requiere que las compras se cobren como compras (4b o M6) y m_obj sin estos ajustes | **−11,605 · −18,609** con el τ registrado de cinco años; −9,141 · −15,848 con el de la ventana. Con el tipo fijo: −9,765 · −14,598 (cinco años) y −9,763 (ventana) |
| **N2** · bajas de 2025 con seguros | Nota 4.6: +25,7 [P: URD25 p.350]; «insurance benefits» [P: p.309]; que sean la misma partida es [I] | Sin la plusvalía, en el EBIT de 2025 y en m0 | Suceso extraordinario [I] | No publicada: tres hipótesis | Caja no identificada (cobros por bajas 15,3 < plusvalía 23,1); reposición de los activos no identificada; la simetría tocaría el FCF base registrado | De −10,305 a −11,598 · de +9,9 a +12,3, parcial. **Pendiente** |
| No se proponen | Resto de la nota 4.6 (reestructuración, sistemas, medio ambiente, litigios); pérdidas ordinarias por bajas | — | Recurrentes; su caja está en el FCF base | — | Normalizarlas las pasaría a f: la nota entera da −20,057 · −32,803 | — |

**Conjunto N1 + N2:** de −22,060 a −23,353, con la convención registrada; parcial, porque N2 está pendiente.

**El «≈ 18,6» de la revisión 1** era solo la parte de f del ajuste de 2023 con el tipo recalculado (−18,648). Omitía la bajada del τ de cinco años (+4,334): su efecto conjunto es −14,314.

**De qué depende la cifra de N1** (V4; `copia_investigacion_f1.md`):
- **Convención del τ de proyección** (E8.1, fuera de F1):
  - lo firme es que N1 baja el flujo sin crecimiento entre 9 y 12; antes de impuestos, 13,966;
  - con la convención registrada (cinco años) la regla publicada da −11,605, y con el τ de la ventana, −9,141;
  - la diferencia con el tipo fijo cambia de signo: −1,840 frente a +0,622;
  - el caso sintético con impuestos (`caso_fiscal_N1`) muestra que, con tipos homogéneos, la regla sin efecto fiscal da la caja. La diferencia procede de la convención, no de N1.
- **Alcance a 2021–22:**
  - el τ de cinco años promedia 2021 y 2022, que tuvieron ajustes de earnout: (3,0) y 2,4 [P][LECTURA: URD22 p.285; URD23 p.302], con línea fiscal propia en 2022;
  - si la regla los alcanza, +0,416 en el flujo sin crecimiento y +0,466 en el año 11 NORMAL (−11,190 · −18,142);
  - es una opción del texto de (5a).
- **Actualización del earnout:**
  - es la de México, en el resultado financiero: 12,4 / 5,6 / 0,7 [P][LECTURA: DEU24 p.259; URD25 p.313]. No es deducible y también eleva el tipo;
  - si la regla fiscal la alcanzara, −0,790 en el flujo sin crecimiento y −1,661 en el año 11 NORMAL (−12,396 · −20,270);
  - no se incluye en N1 mientras sus cifras no estén en el CSV verificado.

### 5.2 Inversión de transición (5b)

- **Lo publicado:**
  - [P] el gasto del plan climático está dentro del capex de la ventana, sin importe separado: «expenditure under the Climate plan», URD25 p.122;
  - [P] los planes de deterioro suponen por él una inversión superior a la amortización histórica: URD25 p.369.
- **Clasificación por finalidad documentada:**
  - sostenimiento permanente y proporcional a las ventas: en R (en f la proporción crece con las ventas; si el importe es fijo en euros, con crecimiento se cobra de más: caso V2d);
  - sostenimiento u obligación temporal: término explícito con importe y horizonte (E3), **fuera del denominador del ancla de S2C** (E4);
  - ampliación de capacidad: crecimiento, dentro del ancla (caso V2e).
- **La caja se cobra una sola vez.** Casos P1a–P1e a crecimiento cero y V2a–V2e con crecimiento y el ancla calculada:
  - temporal cargada en R: se cobra de más después del plan;
  - permanente con término temporal: se omite;
  - en R y en término: dos veces;
  - como crecimiento sin serlo: desaparece a crecimiento cero;
  - término explícito dentro del ancla: dos veces con crecimiento.
- Sin importe u horizonte, la conclusión afectada queda pendiente. Como la transición está dentro del capex propio, este sigue siendo cota superior de la suma de R_propia y la transición.

### 5.3 Otras

| Dependencia | Peso | Tratamiento |
|---|---|---|
| Peso del arrendamiento | Pagos −16,8; con la ROU, −6,7 en A1 y A2 | (1b) |
| Precio frente a volumen (M5) | Anclas de S2C orgánicas | Solo si el crecimiento proyectado fuera orgánico |
| Convención del τ de proyección (E8.1) | Mueve N1 entre −9,1 y −11,6 | Fuera de F1; se declara con N1 |
| Fuera de F1 (informe, §7–§8): intereses sin endeudamiento nuevo | — | Revisión económica aparte |

---

## 6. Coherencia del conjunto

- **Arrendamiento:** se cuenta una vez en la calibración, en los años 1–10 y en el año 11 (1a). El FCF base, C48 y C49 no cambian: E6 se conserva. E1, D3 y E2 no se tocan.
- **Clientes, PPA y compras:** cada coste tiene un solo sitio (tabla del §2).
  - La PPA no se carga como reposición (2).
  - La reposición propia está en R (3a).
  - Las compras, según (4b): opción A, pendiente hasta M6; opción B, crecimiento por hipótesis declarada. Las de reposición que se documenten van a R o a un término explícito, fuera del ancla.
- **Margen:** EBIT NIIF 16 con la PPA y la amortización ROU como proporción constante (2), con sus efectos de escala declarados.
- **Perímetros:** f, el ancla de S2C (solo inversión de crecimiento), el margen y el ROIC del terminal, el mismo (4a). La comparación del terminal es la del libro.
- **Normalización:** solo ajustes con regla fiscal y caja identificada (5a). La cifra se declara con su convención del tipo. El diagnóstico se conserva.
- **Transición:** por finalidad, con su caja una vez y fuera del ancla si va como término (5b).
- **Controles:** cada decisión aprueba sus controles. El texto de aprobación y E5 usan la misma severidad. Ningún aviso se presenta como prueba de coherencia.
- **Bloqueo:** con R pendiente, Elis sigue en `pendiente_de_datos` y V-F1d la deja «incompleta». Con la opción A de (4b), V-F1j también. **Ninguna recomendación desbloquea una valoración.**
- **Sentido del valor de cada recomendación** (ninguna se apoya en él):
  - (1a) sube el flujo frente a A0, porque corrige un error demostrado;
  - (1b) declara −6,7 en A1 y A2;
  - (2) lo sube frente a A1, con el mismo R; los efectos de escala lo bajan 5,9 en A2;
  - (3a) no da ninguna cifra;
  - (4a) obliga a declarar el ROIC, que hoy cobra más inversión que su S2C;
  - (4b), opción A, no da cifra; la B es más favorable que suponer compras de reposición;
  - (5a) N1 baja el flujo entre 9,1 y 11,6;
  - (5b) no da cifra.

**Qué no se adopta:** A1, A2 ni A1′ con su valor de R; ningún valor de R; ningún umbral; la clasificación de las compras; ninguna valoración de Elis.

**Después de la decisión (no iniciado):**
1. Registrar cada decisión con fecha, persona y motivo, como E1–E6.
2. Aplicarlas en la especificación y en el motor, con sus pruebas (E9, T8, T15 y T16).
3. Encargar una revisión independiente de lo que cambie.

Mientras R falte, Elis sigue en `pendiente_de_datos`.
