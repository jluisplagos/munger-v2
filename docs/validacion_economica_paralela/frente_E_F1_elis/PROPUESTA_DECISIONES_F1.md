# Propuesta de decisiones F1 · Elis · para aprobación

Fecha: 16-nov-2026, revisión 2. **Estado: propuesta. No adoptada ni implementada.**

> **Estado tras la revisión dirigida a P1–P4** (rama `auditoria/economica-f1-frente-e-revision`, commit `8fcc7fd`; copia en [revision/REVISION_PROPUESTA_P1_P4.md](revision/REVISION_PROPUESTA_P1_P4.md)).
> - Veredictos: P1 resuelto en parte; P2 resuelto en parte; P3 resuelto; P4 resuelto en parte. Una objeción material (V1), ocho menores (V2–V9) y dos de forma (V10–V11). Ninguna cambia una cifra de esta propuesta.
> - **Las correcciones no están aplicadas.** Este encargo preveía una sola pasada. Aplicarlas cambiaría el material revisado y exigiría revisar lo afectado; decide la persona responsable.
> - **Antes de decidir (4b), leer V1.** El crecimiento orgánico publicado solo excluye las adquisiciones «importantes», de más de 5,0 millones de ingresos en Francia y de 3,0 en los demás países (URD 2025 p. 313; DEU 2024 p. 259; URD 2023 p. 267). Las compras pequeñas cuentan dentro: 31,5 al año de media en 2023–25, el 10,2 % del FCF base. Lo publicado permite decir «sin compras importantes», no «las bajas se repusieron sin compras». El fundamento de (4b) y de la fila 2, tal como está escrito abajo, no se sostiene. La hipótesis puede seguir declarándose como tal, con un apoyo menor, o quedar bloqueada hasta M6.
> - Otras que afectan al texto que se pide aprobar:
>   - V2, a (5b) y a las compras con término explícito: con crecimiento, el ancla de S2C los cobra otra vez;
>   - V3, a (5a): la caja del earnout está publicada (nota 2.4) y la actualización de 2025 también (0,7);
>   - V4, a (5a): el −11,6 depende de la convención del τ de cinco años; con el de la ventana sería −9,1;
>   - V5, a (1b) y (2)(v): el 16,8 es solo la parte de los pagos; con la amortización ROU que devuelve f, −6,7 en A1 y A2;
>   - V6, a (4a): el libro ya compara el ROIC del terminal, con otra fórmula y un umbral de 5 puntos;
>   - V8, a (3a): 867,2 acota R_propia más la transición, no R total;
>   - V11: el texto de (1a) arrastra (4a) y la severidad de otros controles, y (3b) no es un texto aprobable tal cual.

- Elis sigue bloqueada para valoración (`pendiente_de_datos`) mientras falten datos o fundamento.
- No se adopta A1, A2 ni A1′, ni ningún valor de reinversión.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y las decisiones E1, D3, E2 y E6.
- Ninguna recomendación se hace por su efecto en la valoración. Donde una opción lo mueve, se dice en qué sentido.

**Revisión 2.** Reconcilia la propuesta del commit `b83803c` con la revisión externa del commit `1a07188` (F1-P1 a P4). Qué cambia y por qué: [RESPUESTA_REVISION_PROPUESTA_F1.md](RESPUESTA_REVISION_PROPUESTA_F1.md). La especificación coherente con esta versión está en [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md), E2–E6.

Marcas: **[P]** publicado · **[D]** derivado · **[I]** inferido · **[H]** hipótesis · **[Pol]** política (una decisión, no un dato) · **[DH]** decisión humana registrada.

Cifras:
- las del informe ([INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md)), medias de 2023–25 o base 2025;
- las nuevas de esta revisión salen de dos scripts:
  - `resultados/copia_investigacion_f1.md`, una copia de investigación con cifras verificadas, que no es una entrada registrada ni una valoración;
  - `resultados/controles_sinteticos_f1.json`, ejemplos de política con importes ficticios, que no son datos de Elis.

---

## Tabla única de decisiones

| ID | Recomendación | Naturaleza | Condición de aplicación | Carencia | Texto exacto que se pide aprobar |
|---|---|---|---|---|---|
| **1a** | F1 (b): corregir la definición del motor A. El perímetro de la reinversión que calibra f excluye la amortización de los derechos de uso (ROU). FCF base, C48 y C49 sin cambios. `A0_total` solo sin arrendamientos. Controles de E5 con su severidad | Doble cómputo [D]; premisa de reposición por contrato [I], que es la práctica publicada de Elis en sus pruebas de deterioro [P]; elección de (b) [Pol] | Solo la definición del motor. Un caso se usa para una conclusión si ningún control de severidad BLOQUEA salta. Elis sigue bloqueada por R (3a) | Ninguna para la corrección del arrendamiento. La tendencia de los pagos, en (1b) | «Apruebo F1 (b) con la política del §1: el perímetro de la reinversión que calibra f excluye la amortización de los derechos de uso; el FCF base (307,933), C48 = 108 y C49 = 128,1 no cambian; `A0_total` solo se admite sin arrendamientos; los controles de E5 se aplican con su severidad: los de BLOQUEA impiden usar el motor A para una conclusión y los de AVISO se muestran sin acreditar coherencia. No fija R ni libera la valoración de Elis.» |
| **1b** | La media 2023–25 de los pagos de arrendamiento (3,359 % de las ventas) es solo una referencia de ensayo y la convención registrada, **no un peso futuro identificado**. Se declara la sensibilidad: con el peso de 2025 (3,709 %), el flujo sin crecimiento es 16,8 menor | Pagos y ventas [P]; sensibilidad [D]; uso de la media [H] | Valores de prueba y diagnósticos. En una valoración, el peso proyectado es una hipótesis declarada | Por qué los pagos crecen más deprisa que las ventas: 3,04 % → 3,30 % → 3,71 % | «Apruebo que la media 2023–25 de los pagos de arrendamiento se use como referencia de ensayo y convención declarada, con la sensibilidad de 16,8 a la vista; no la apruebo como estimación del peso futuro.» |
| **2** | La PPA no es un desembolso de reposición. El coste de conservar y reponer clientes se cobra una sola vez, donde está: el gasto comercial, en el margen; la inversión propia para los clientes que sustituyen a los perdidos, en R; las compras de cartera necesarias, si se documentan, en R o como término explícito. Margen con la PPA **constante como proporción de las ventas**, la misma que devuelve f | PPA no monetaria [P]; mayoritariamente no deducible [I]; reposición orgánica en la ventana [P][I]; proyección [H]; correspondencia [Pol] | Tabla de correspondencia del §2 sin omisiones ni dobles cargos. R, cuando exista, declara cómo incluye la reposición. Con (4b) | M2: tasa de bajas y desembolso por cliente nuevo. En Elis, la PPA de m0 (1,787 % de las ventas) difiere de la que devuelve f (1,874 %): 4,2 en la base, declarado | «Apruebo como política: (i) la amortización PPA no se trata como desembolso de reposición; (ii) el gasto comercial corriente queda en el margen y no se añade a R; (iii) la inversión propia para sustituir clientes perdidos forma parte de R; (iv) las compras de cartera necesarias para mantener las ventas, si se documentan, se cobran en R o como término explícito, nunca solo como crecimiento; (v) el margen proyectado lleva la PPA como proporción constante de las ventas, la misma que devuelve f.» |
| **3a** | R sigue en `pendiente_de_datos`. El intervalo 736,0–867,2 solo mide la materialidad. Perímetro: R = R_propia + R_compras (+ transición de sostenimiento). La guarda compara cada parte con su caja | Reparto no publicado [P]; cota superior [I]; la referencia inferior no es una cota y tiene evidencia publicada en contra [I][P] | — | M1: reparto por bloque y año, con el plan climático | «Apruebo que R siga en `pendiente_de_datos`, con el perímetro del §3, y que el intervalo 736,0–867,2 solo mida la materialidad.» |
| **3b** | Decidir si se busca el dato (M1, M2, M6 y el plan climático) o una estimación documentada (fuente, método, rango y responsable), por qué vía y quién. Las preguntas están preparadas; su envío no lo autoriza este encargo | Gestión [Pol] | — | M1, M2, M6 y el plan climático | «Decido si se obtienen M1, M2, M6 y los datos del plan climático, o una estimación documentada, y en su caso por qué vía y quién; sin ellos, R sigue pendiente.» |
| **4a** | Un solo perímetro declarado para la reinversión que calibra f, el ancla de S2C, el margen proyectado **y el ROIC del terminal**. Si no casan, el caso no se usa para una conclusión | Matriz de coherencia [D]; regla [Pol] | Las palancas de S2C y de ROIC declaran su perímetro | Anclas numéricas pendientes de R. En Elis, las palancas no declaran perímetro | «Apruebo que f, el ancla de S2C, el margen proyectado y el ROIC del terminal usen un solo perímetro declarado, y que un caso cuyos perímetros no casan no se use para una conclusión.» |
| **4b** | Declarar como **hipótesis, no como dato**, que las compras de sociedades de Elis son crecimiento. Crecimiento proyectado y ancla de S2C, con adquisiciones. Consecuencia: a crecimiento cero no se compra nada. Sensibilidad: cada millón anual de compras que fuera de reposición baja el flujo sostenible en un millón | Crecimiento orgánico positivo todos los años, con efecto volumen en 2024–25 [P]; las bajas se repusieron sin compras en la ventana [I]; futuro [H] | Con (2)(iv): las compras de reposición que se documenten salen de la hipótesis. Se revisa si el crecimiento orgánico en volumen deja de ser positivo | M6: finalidad de las compras. M5: precio frente a volumen, solo para un ancla orgánica | «Apruebo como hipótesis declarada, no como dato, que las compras de sociedades de Elis son inversión de crecimiento, con su fundamento, su consecuencia a crecimiento cero y su sensibilidad; el crecimiento proyectado y el ancla de S2C se miden con adquisiciones.» Alternativa: no aprobarla y exigir M6, lo que bloquea (V-F1j) |
| **5a** | No deducir el 27,936, que es un diagnóstico. Normalizar solo con ajustes concretos y regla fiscal. **N1**, los ajustes de earnout de 2023–25 sin efecto fiscal: −11,6 en el flujo sin crecimiento y −18,6 en el terminal NORMAL. **N2**, las bajas de 2025 con seguros: pendiente. El resto de la nota 4.6 no se normaliza | Partidas [P]; no deducibilidad del earnout [P]; caja del earnout fuera del FCF base [I]; vínculo entre las bajas y los seguros [I]; regla [Pol] | N1 con (4b) y m_obj declarado sin esos ajustes. No cambia los históricos ni las entradas registradas: fila de ajustes con fuente y regla | N2: fiscalidad, caja cobrada y reposición de los activos. Actualización del earnout mexicano en el tipo | «Apruebo la regla N1: en la ventana de calibración, los ajustes de earnout de la nota 4.6 se sacan del EBIT y del resultado antes de impuestos de su año, sin efecto en el gasto por impuesto, con su registro. N2 queda pendiente. Ninguna otra partida se normaliza por su etiqueta. El 27,936 se conserva como diagnóstico.» Alternativa: «Mantengo la calibración sin normalizar y declaro su diagnóstico.» |
| **5b** | La inversión de transición (plan climático) se clasifica por su **finalidad documentada**, con su caja cobrada una sola vez en la ventana, la proyección y el terminal. Sin importe u horizonte, la conclusión afectada queda pendiente. Nunca cero por defecto ni perpetua por su nombre | Gasto del plan dentro del capex [P]; planes de deterioro con inversión superior a la amortización histórica [P]; clasificación [Pol] | Forma parte de la estimación de R (V-F1d) y de V-F1i | Importe, horizonte y finalidad del plan (M1) | «Apruebo que la inversión de transición se clasifique por su finalidad documentada, con su caja cobrada una sola vez en la ventana, la proyección y el terminal, y que sin importe u horizonte la conclusión afectada quede pendiente.» |

**Resultado del conjunto.**
- El motor A quedaría corregido en su definición, pero **Elis seguiría bloqueada**: sin R no hay f, ni flujo de partida, ni ancla de S2C, ni compatibilidad del terminal.
- Ninguna decisión pide elegir una cifra para sustituir evidencia ausente.

### Severidad de los controles (E5)

| Severidad | Qué significa | Controles |
|---|---|---|
| **BLOQUEA** | El resultado del motor A no se usa para una conclusión. Puede calcularse y mostrarse como diagnóstico, rotulado | V-F1a (sin umbral adoptado: con cualquier importe), V-F1b, V-F1d, V-F1e, V-F1g, V-F1h, V-F1i, V-F1j, V-F1k (perímetro sin declarar o distinto), V-F1l; V-F1c sin justificación |
| **AVISO** | Se muestra, no bloquea y no acredita coherencia | V-F1c con justificación documentada |
| **INFORMA** | Información para quien decide | V-F1f (agotamiento de la PPA y proporciones de m0 y de f); V-F1k (ROIC frente al que reproduce S2C) |

Un umbral de materialidad para V-F1a sería una decisión aparte. No propongo ninguna cifra; el 0,5 % de la versión anterior no se adopta.

---

## 1. Alternativa F1 y arrendamientos (1a, 1b)

**Política propuesta (1a):**

> El motor A no supone que la amortización de los derechos de uso (NIIF 16) se reponga con inversión propia. La reinversión que calibra f se mide con un perímetro declarado (`perimetro_reinversion`) que excluye esa amortización. El mismo perímetro se usa en el ancla de S2C, en el margen proyectado y en el ROIC del terminal. El FCF base (307,933), C48 = 108 y C49 = 128,1 no cambian. `A0_total` (D&A total) solo se admite sin arrendamientos (D&A ROU = 0 y C49 = 0). Los controles V-F1a–l se aplican con la severidad de E5: si salta uno que BLOQUEA, el motor A no se usa para una conclusión. Cada perímetro se registra con fecha, persona y motivo.

**Fundamento:**
- En la calibración, el arrendamiento se cuenta una vez: los pagos están dentro del FCF base. En la proyección se cuenta dos veces: la amortización ROU en el margen y los pagos en f [D].
- El exceso es de 139,4 en la base 2025 y es íntegro a crecimiento cero y en el terminal [D]. Casos sintéticos: arrendamiento una vez, 68; A0, 58 en todos los años y en el terminal (P4d).
- La premisa es que el activo arrendado se repone con contratos nuevos, cuyo coste son los pagos [I]. Es la definición de flujo de las pruebas de deterioro de Elis: «capital expenditure (including lease renewal)», sobre un EBITDA sin coste de arrendamiento [P: URD25 p.368; DEU24 p.314]. Esa práctica apoya contar el coste una vez; no valida por sí sola todo el flujo al accionista del motor A.

**Alternativas y consecuencias:**
- **(a) Declarar el límite** (supuesto vigente): todos los casos con NIIF 16 quedan sin motor A.
- **(c) Juicio caso a caso:** sin regla escrita, no se puede auditar ni reproducir.
- **A1′ (FCF base sin el principal):**
  - cambia C49 y la construcción registrada del FCF base (decisión del 10-nov-2026 y E6);
  - su variante de margen después de arrendamientos contaría dos veces el interés de arrendamiento, 25,1 de media.
- **Motor B:** tiene su propia incoherencia de perímetro en el coste de la deuda (C63), y la elección de motor es de la fase A.
- **Efecto en el valor:** frente a A0, la corrección sube el flujo 139,4 en la base 2025. No la recomiendo por eso, sino porque A0 es incoherente con NIIF 16.

**Peso del arrendamiento (1b):**
- f aplica la media de la ventana, el 3,3589 % de las ventas: 161,122 sobre las de 2025, frente a 177,9 pagados.
- Con el peso de 2025 (3,7087 %), el flujo sin crecimiento sería 16,778 menor (`copia_investigacion_f1.md`; coincide con la revisión).
- La media es una referencia de ensayo y una convención, no un dato del peso futuro. No se elige otro punto.

---

## 2. Correspondencia de costes: PPA, reposición de clientes y adquisiciones (2, 4b)

**Dónde se cobra cada coste.** Ningún euro se omite ni se cobra dos veces, tampoco a crecimiento cero.

| Coste o desembolso | Ventana (calibración) | Años 1–10 | Terminal | No admitido |
|---|---|---|---|---|
| Pagos de arrendamiento | FCF base (C48 y C49) | En f, proporcional a las ventas | En f | Cobrar además la amortización ROU como reposición (A0) |
| Amortización ROU | EBIT (no es caja) | En el margen; se devuelve en f al excluirla de D_X | Igual | Tratarla como reposición |
| Gasto comercial corriente | EBIT y FCF base | En el margen | En el margen | Añadirlo a R (caso P2f) |
| Capex propio necesario, incluida la dotación a los clientes que sustituyen a los perdidos | FCF base (capex) | R_propia, en f | R_propia, en f | Excluirlo de R o cobrarlo también como crecimiento |
| Compras de cartera necesarias para mantener las ventas, si se documentan | Fuera del FCF base | R_compras, en f, o término explícito proporcional a las ventas | Igual | Cobrarlas solo como crecimiento (P2a, P4c) o también en el ancla (P2c) |
| Compras de crecimiento | Fuera del FCF base | ΔV/S2C, con el ancla con adquisiciones | g∞/ROIC, con el ROIC con adquisiciones | Contarlas en R |
| PPA | EBIT (no es caja) | En el margen, como proporción constante; devuelta en f (A2) | Igual | Cobrarla como reposición (A1) sin dato; PPA en euros o decreciente con A2 (P2h, P2i) |
| Inversión de transición | Dentro del capex propio y del FCF base | Según su finalidad: R; término explícito con horizonte; o crecimiento si amplía ventas (§5.2) | Solo si es permanente | Excluirla de toda salida; cero por defecto; perpetua por su nombre (P1a–P1e) |
| Ajustes normalizados (N1) | Fuera del EBIT y del BAI de su año, sin efecto fiscal; su caja está en las compras | — | — | Deducir el diagnóstico 27,936 |
| Partidas recurrentes de la nota 4.6 | EBIT y FCF base | En el margen; m_obj se declara con ellas | Igual | Normalizarlas por su etiqueta |
| Inversión de crecimiento propia y circulante | FCF base | ΔV/S2C | g∞/ROIC | — |

**Reposición de clientes.** El coste de conservar y reponer clientes tiene hasta tres partes de caja:
- **(a) Gasto comercial:** en el margen, no en R.
- **(b) Inversión propia para los clientes nuevos que sustituyen a los perdidos:** en R_propia. Es el «initial outlay required to set up a new customer» [P: URD25 p.312].
- **(c) Compras de cartera que reponen ventas perdidas:** en R_compras o en un término explícito.

«Reponer clientes va en R» se refiere a (b) y, si existe, a (c). «Su coste ya está en el EBIT y el capex» describe la ventana: (a) y (b) están pagados ahí, y por eso la PPA no es un coste adicional. «Las compras son crecimiento» es la hipótesis (c) = 0 de (4b).

**PPA (2).**
- [P] La PPA de 2025, 85,7, son relaciones con clientes (83,5) y marcas (2,2). Vidas de 4 a 14 años; cartera neta de 275,1; altas de 2025 provisionales.
- [D] Sin compras nuevas, la cartera se agotaría en unos 3,3 años al ritmo actual.
- [I] No es caja y en su mayor parte no es deducible: el ingreso fiscal diferido de los intangibles equivale al 18–24 % de su amortización.
- **«PPA constante» significa constante como proporción de las ventas.** f es una proporción de las ventas por construcción. La PPA, que no es caja, solo se anula en el flujo si el margen la lleva en la misma proporción que f devuelve (P2g). En euros, fija o agotándose, no casa (P2h y P2i).
- En Elis, f devuelve en A2 el 1,8743 % de las ventas (la media de la ventana) y m0 lleva el 1,7866 % (la PPA real de 2025). La diferencia, 4,206 en la base, es un efecto de escala de la definición y se declara.
- La proporción constante es una convención del perímetro [H]: no hay dato sobre cómo evolucionará la PPA en euros.

**Alternativas:**
- **A1 (PPA como reposición en caja perpetua, unos 85,7 al año):** ningún dato publicado la sostiene. Con el mismo R, el flujo de partida es 89,9 menor.
- **Modelizar las adquisiciones** como salida de caja, con su PPA: exige M2, M6 y otra estructura del motor.
- **Efecto en el valor:** con el mismo R, la política recomendada da más flujo que A1. Mientras R siga pendiente, no produce ninguna valoración.

**Compras de sociedades (4b).**
- Fundamento de la hipótesis:
  - [P] crecimiento orgánico positivo todos los años de 2021–2025 (7,4 %, 21,0 %, 11,8 %, 5,2 % y 3,8 %);
  - [P] con efecto volumen publicado en 2024 y 2025; en 2023, unos 9 de los 11,8 puntos fueron de precio;
  - [I] el crecimiento orgánico se mide neto de los clientes perdidos, también los de sociedades compradas antes. En la ventana, las bajas se repusieron sin compras, y las compras añadieron ventas (crecimiento externo del 1,2 % al 3,1 % al año en 2022–2025).
- Es una evidencia parcial de la ventana. Para el futuro es una hipótesis [H], no un dato.
- **Consecuencia:** a crecimiento cero no se compra nada.
- **Sensibilidad:** cada millón anual de compras que fuera de reposición bajaría el flujo sostenible en un millón, también en el terminal.
- Si no se aprueba, hace falta M6 (finalidad de las compras), y sin él el caso queda bloqueado (V-F1j).
- **Ancla con adquisiciones o sin ellas:**
  - orgánica en los dos lados: exige M5 (precio frente a volumen) y da anclas más altas (en A2, de 2,07 a 3,13, frente a 1,61). Es la opción más favorable para el valor, y no la recomiendo sin M5;
  - mezclar los dos lados es incoherente.

---

## 3. Reinversión necesaria (3a, 3b)

**Recomendación:** R sigue en `pendiente_de_datos` y, con ella, f, el flujo de partida, el ancla de S2C y la compatibilidad del terminal de Elis.

**Perímetro de R:**
- R = **R_propia** + **R_compras** + la inversión de transición que se clasifique como sostenimiento (5b);
- R_propia: el capex propio necesario para sostener las ventas a volumen constante, incluida la dotación a los clientes que sustituyen a los perdidos;
- R_compras: las compras de cartera necesarias para mantener las ventas. Cero bajo la hipótesis (4b);
- R no incluye el gasto comercial, que está en el margen.

**Guarda (V-F1c):** R_propia frente al capex propio, y R_compras frente a las compras. Comparar R total con el capex propio daría alarma de infrainversión sin que la haya: con R = 29 = 20 + 9 y capex propio 20, la guarda anterior dispara y la propuesta no (`controles_sinteticos_f1.json`, `guarda_R_frente_a_capex`).

**No hay fundamento suficiente para una estimación con rango que pueda usarse** (`A3_estimado`; V-F1d exige fuente, método, rango, responsable y el tratamiento de la reposición de clientes y de la transición):
- **[P]** No se publica ningún reparto entre mantenimiento y crecimiento.
  - Solo hay un texto fijo, sin importe: dos tercios de la inversión en lino plano mantienen el stock en circulación.
  - El lino plano es el 46,2 % de las ventas, y la proporción no puede extenderse a todo el lino: dos tercios de sus compras serían 396, frente a 565,1 de amortización.
- **[I] Cota superior: el capex propio, 867,2 de media.** Elis creció en volumen, con apoyo publicado cualitativo en 2024 y 2025. La cota incluye la inversión de transición, que está dentro del capex. Dejaría de valer si en 2025 hubo infrainversión; hay señales de contención del capex que la empresa presenta como normalización.
- **[I] Referencia inferior: la D&A propia, 736,0.** No es una cota, y hay evidencia publicada en contra de tomarla como caso central:
  - con inflación, reponer cuesta más que la amortización a coste histórico;
  - los planes de deterioro suponen una inversión superior a la amortización histórica [P: URD25 p.369].
- **[D]** La V6.3 supone R igual a la D&A total, 954,0: más que el capex propio de unos años en que la empresa crecía.

**Alternativas:**
- Usar un extremo:
  - capex propio (cota B, flujo de partida 339,8): supone crecimiento sin inversión;
  - D&A propia (A2, 477,8): tiene evidencia en contra como caso central.
- Un punto intermedio convertiría la falta del dato en una cifra a escoger. No lo propongo.
- **Lo que está en juego:** de 339,8 a 477,8 en el flujo de partida, 138, el 45 % del FCF base. Los dos extremos llevan las partidas de la ventana sin normalizar (§5.1).

**Evidencia ausente:**
- **M1:** reparto por bloque y año (lino plano, resto del lino, otros artículos, industrial y TI, plan climático con su importe, horizonte y finalidad); la base y la fecha de los dos tercios;
- **M2:** la parte de la dotación a clientes nuevos que repone clientes perdidos;
- **M6:** la finalidad de las compras, si no se aprueba (4b).

**Preguntas preparadas, no enviadas** (respuesta, §6): reparto del capex; plan climático; bajas de clientes y desembolso por cliente nuevo; finalidad de las compras; indemnizaciones de seguros de 2025. La de M1 ya está redactada en `Diagnóstico V6!B223`. Decidir si se piden y quién es la decisión (3b).

---

## 4. Perímetros coherentes: f, S2C, margen y terminal (4a, 4b)

**Recomendación (4a):** un solo perímetro declarado para:
- la reinversión que calibra f;
- el ancla de S2C de los años 1–10;
- el margen proyectado;
- el ROIC del terminal.

Si no casan, el caso no se usa para una conclusión: V-F1g, V-F1h y V-F1k bloquean.

**El terminal no usa S2C.** Reinvierte g∞/ROIC del NOPAT, antes de f: V₁₀·(1+g∞)·[m_obj(1−τ)(1 − g∞/ROIC) − f].
- El ROIC compatible con esta propuesta es el rendimiento de la inversión nueva, medido:
  - sobre el NOPAT del perímetro del margen;
  - sobre el capital de crecimiento del perímetro del ancla de S2C: con adquisiciones si (4b) lo está; sin la ROU, porque el arrendamiento se paga en f; y sin R, porque la reposición está en f.
- El terminal cobra la misma inversión de crecimiento que ΔV/S2C si ROIC = (1+g∞)·m_obj·(1−τ)·S2C (caso P4a). Un ROIC de otro perímetro cobra otra inversión (P4b).
- Con g∞ = 0, el terminal es V·[m_obj(1−τ) − f]: un coste recurrente cobrado solo como crecimiento desaparece también ahí (P4c).

**Palancas actuales de Elis** (`copia_investigacion_f1.md`, sin estimar ningún ROIC nuevo):

| | ROIC | ROIC que reproduce S2C | S2C implícita en el ROIC | Inversión del terminal con ROIC − con S2C |
|---|---|---|---|---|
| MALO | 7 % | 7,55 % | 0,93 frente a 1 | +4,45 |
| NORMAL | 10 % | 10,89 % | 1,10 frente a 1,2 | +10,28 |
| BUENO | 12 % | 14,77 % | 1,22 frente a 1,5 | +28,96 |

- El ROIC de las palancas cobra en el terminal algo más de inversión que su propia S2C. La diferencia se informa (V-F1k) y debe justificarse.
- Las palancas S2C (1 / 1,2 / 1,5) se anclaron en un perímetro propio (≈ 1,5), no en C53; el C53 de A0 es 9,04. Su perímetro no está declarado y depende de R: **compatibilidad del terminal pendiente.**

**Fundamento:**
- La especificación exige que los perímetros describan el mismo tratamiento del arrendamiento, de la PPA y de las compras [D].
- El crecimiento orgánico publicado incluye precio todos los años [P]. Un ancla orgánica nominal sobrestima la productividad del capital en volumen [I].

---

## 5. Dependencias: normalización, inversión de transición y otras

### 5.1 Partidas de la ventana (5a)

El **27,936** es un diagnóstico del cálculo actual:
- +13,675 de earnout y otros no monetarios dentro de f;
- −4,032 de plusvalías dentro de f;
- +18,293 de la plusvalía de 2025 dentro de m0.

No es el efecto de ninguna regla, por tres razones:
- toma las líneas del estado de flujos de los tres años, que incluyen otros elementos y las pérdidas ordinarias por bajas;
- las quita de f antes de impuestos;
- no quita la plusvalía de 2025 del NOPAT que calibra f.

**Ajustes concretos** (perímetro A0; la variación es idéntica en A1 y A2):

| Ajuste | Fuente | Original → normalizado | Motivo | Fiscalidad | Caja y dependencias | Flujo sin crecimiento · terminal NORMAL |
|---|---|---|---|---|---|---|
| **N1** · ajustes de earnout 2023–25 | Nota 4.6: −48,9 / +8,7 / −0,2 [P: DEU24 p.296; URD25 p.350] | Sin el ajuste, en el EBIT y el BAI de su año | Revaluación del precio de adquisiciones, no coste de explotación; no monetaria al reconocerse; simétrica en los tres años | No deducible [P: DEU24 p.337; URD25 p.392]. Gasto sin cambios, tipo recalculado | Pago fuera del FCF base [I]. Requiere (4b) y m_obj sin estos ajustes | **−11,605 · −18,609**. Con el tipo fijo, −9,765 · −14,598 |
| **N2** · bajas de 2025 con seguros | Nota 4.6: +25,7 [P: URD25 p.350]; «insurance benefits» [P: p.309]; que sean la misma partida es [I] | Sin la plusvalía, en el EBIT de 2025 y en m0 | Suceso extraordinario [I] | No publicada: tres hipótesis | Caja no identificada (cobros por bajas 15,3 < plusvalía 23,1); reposición de los activos no identificada; la simetría tocaría el FCF base registrado | De −10,305 a −11,598 · de +9,9 a +12,3, parcial. **Pendiente** |
| No se proponen | Resto de la nota 4.6 (reestructuración, sistemas, medio ambiente, litigios); pérdidas ordinarias por bajas | — | Recurrentes; su caja está en el FCF base | — | Normalizarlas las pasaría a f: la nota entera da −20,057 · −32,803 | — |

**Conjunto N1 + N2:** de −22,060 a −23,353, parcial porque N2 está pendiente.

El «≈ 18,6» de la versión anterior era solo la parte de f del ajuste de 2023 con el tipo recalculado (−18,648). Omitía la bajada del τ de 5 años (+4,334): su efecto conjunto es −14,314.

**Límite de N1.** La actualización del complemento de precio de México (12,4 en 2023 y 5,6 en 2024, en el resultado financiero; no deducible [P: DEU24 p.259 y p.337]) también eleva el tipo. No se calcula: no está en el CSV verificado y la de 2025 no se publica por separado.

### 5.2 Inversión de transición (5b)

- **Lo publicado:**
  - [P] el gasto del plan climático está dentro del capex de la ventana, sin importe separado: «expenditure under the Climate plan», URD25 p.122;
  - [P] los planes de deterioro suponen por él una inversión superior a la amortización histórica: URD25 p.369.
- **Clasificación por finalidad documentada:**
  - sostenimiento permanente: en R;
  - sostenimiento u obligación temporal: término explícito con importe y horizonte;
  - ampliación de capacidad: crecimiento.
- La caja se cobra una sola vez. Casos P1a–P1e:
  - temporal cargada en R: se cobra de más después del plan;
  - permanente con término temporal: se omite;
  - en R y en término: dos veces;
  - como crecimiento: desaparece a crecimiento cero.
- Sin importe u horizonte, la conclusión afectada queda pendiente. Como la transición está dentro del capex propio, este sigue siendo cota superior de la suma de R y la transición.

### 5.3 Otras

| Dependencia | Peso | Tratamiento |
|---|---|---|
| Peso del arrendamiento | 16,8 en la base 2025 | (1b) |
| Precio frente a volumen (M5) | Anclas de S2C orgánicas | Solo si el crecimiento proyectado fuera orgánico (4b) |
| Fuera de F1 (informe, §7–§8): ventana del tipo impositivo; intereses sin endeudamiento nuevo | — | Revisión económica aparte |

---

## 6. Coherencia del conjunto

- **Arrendamiento:** se cuenta una vez en la calibración, en los años 1–10 y en el terminal (1a). El FCF base, C48 y C49 no cambian: E6 se conserva. E1, D3 y E2 no se tocan.
- **Clientes, PPA y compras:** cada coste tiene un solo sitio (tabla del §2).
  - La PPA no se carga como reposición (2).
  - La reposición propia está en R (3a).
  - Las compras van en el crecimiento por hipótesis declarada (4b). Si se documentan compras de reposición, pasan a R o a un término explícito.
- **Margen:** EBIT NIIF 16 con la PPA como proporción constante, la única combinación admisible con (2).
- **Perímetros:** f, el ancla de S2C, el margen y el ROIC del terminal, el mismo (4a).
- **Normalización:** solo ajustes con regla fiscal y caja identificada (5a). El diagnóstico se conserva.
- **Transición:** por finalidad, con su caja una vez (5b).
- **Controles:** el texto de aprobación y E5 usan la misma severidad. Ningún aviso se presenta como prueba de coherencia.
- **Bloqueo:** con R pendiente, Elis sigue en `pendiente_de_datos` y V-F1d la deja «incompleta». **Ninguna recomendación desbloquea una valoración.**
- **Sentido del valor de cada recomendación** (ninguna se apoya en él):
  - (1a) sube el flujo frente a A0, porque corrige un error demostrado;
  - (2) lo sube frente a A1, con el mismo R;
  - (3a) no da ninguna cifra;
  - (4a) obliga a declarar el ROIC, que hoy cobra más inversión que su S2C;
  - (4b) es más favorable que suponer compras de reposición, y se declara como hipótesis con su sensibilidad;
  - (5a) N1 baja el flujo 11,6 y el terminal 18,6;
  - (5b) no da cifra.

**Qué no se adopta:** A1, A2 ni A1′ con su valor de R; ningún valor de R; ningún umbral; ninguna valoración de Elis.

**Después de la decisión (no iniciado):**
1. Registrar cada decisión con fecha, persona y motivo, como E1–E6.
2. Aplicarlas en la especificación y en el motor, con sus pruebas (E9, T15 y T16).
3. Encargar una revisión independiente de lo que cambie.

Mientras R falte, Elis sigue en `pendiente_de_datos`.
