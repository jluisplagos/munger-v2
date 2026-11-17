# Decisiones económicas F1 · Elis · una por una

**Fecha:** 17-nov-2026.
**Estado:** presentación para la persona responsable. **No adopta ninguna política económica.**
- Cada decisión sale de [PROPUESTA_DECISIONES_F1.md](PROPUESTA_DECISIONES_F1.md), revisión 3:
  - las correcciones V1–V11 las revisó la revisión F1 v3, `f5775dc`;
  - las correcciones W1–W3 las contrastó Mistral C/F, `90329a1`, conforme con límites.
- El texto que se pediría aprobar es el de la tabla única de esa propuesta. Aquí no se cambia.

**Lo que se mantiene, decida lo que decida:**
- Elis sigue en `pendiente_de_datos` mientras falte R (la reinversión necesaria).
- No se adopta ningún valor de R ni ningún umbral.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y E1/D3/E2/E6.
- Ninguna recomendación se hace por su efecto en el valor. Donde lo hay, se dice en qué sentido.

**Hechos posteriores a la revisión 3 que afectan a estas decisiones:**
- **Bloque CSV (`77ff89f`, contrastado en `c7716a0`).**
  - La actualización del earnout (12,4 / 5,6 / 0,7) y los ajustes de earnout de 2021–22 ((3,0) y 2,4) ya están en el CSV verificado.
  - Por eso, la opción de incluir la actualización en N1 (5a) **ya es aplicable**, si se elige. Antes estaba excluida por falta de verificación.
  - Las sensibilidades no cambian.
- **Revisión de E-ELIS (fuentes públicas oficiales).**
  - **M1, M2 y M6 siguen sin localizarse** en esta búsqueda. Los 11 documentos nuevos están conservados en la Release `fuentes-elis-e-20261117`.
  - **N2:**
    - en la nota 4.6 (URD 2025 p.350), el +25,7 va en una línea propia, separado de las partidas monetarias (−28,2);
    - en el estado de flujos (p.327), los cobros por bajas (15,3) están en inversión;
    - f usa +23,1 y m0 usa +25,7.

    La fiscalidad y la reposición de los activos siguen sin identificarse.
  - Esto refuerza que N2 quede **pendiente**. La vía (ii) de (3b), buscar en fuentes públicas, ya se ha ejecutado sin resultado para M1, M2 y M6.

**Orden sugerido** (sin dependencias circulares):
1. (1a) y (1b);
2. (2);
3. (4a);
4. (4b);
5. (3a) y (3b);
6. (5a);
7. (5b).

---

## (1a) Arrendamientos en el perímetro de la reinversión

- **Qué se decide.** Si la reinversión que calibra f excluye la amortización de los derechos de uso (NIIF 16).
- **Recomendación.** Sí: la alternativa F1 (b).
  - El FCF base, C48 y C49 no cambian.
  - `A0_total` solo se admite sin arrendamientos: D&A ROU = 0 y C49 = 0.
  - Se aplican V-F1a, V-F1b, V-F1e y V-F1m con la severidad de E5. A0 tiene cuatro casos (W3):
    - D&A ROU y C49 positivos: V-F1a, doble cómputo;
    - los dos a cero: admisible;
    - solo uno positivo: V-F1m, fuera de dominio;
    - que V-F1a no salte no admite A0.
- **Alternativas.**
  - (a) Declarar el límite: los casos con NIIF 16 quedan sin motor A.
  - (c) Juicio caso a caso: no auditable.
  - A1′, el FCF base sin el principal: cambia C49 y la decisión E6. Su variante de margen cuenta dos veces el interés del arrendamiento, 25,1 de media.
  - Motor B: tiene su propia incoherencia en el coste de la deuda (C63), y elegir motor es cosa de la fase A.
- **Fundamento.**
  - En la proyección, el arrendamiento se cuenta dos veces: la amortización ROU en el margen y los pagos en f [D]. El exceso es de 139,4 en la base 2025, íntegro a crecimiento cero y en el año 11.
  - Las pruebas de deterioro de Elis definen el flujo con «capital expenditure (including lease renewal)» sobre un EBITDA sin coste de arrendamiento [P: URD25 p.368; DEU24 p.314]. Eso apoya contar el coste una vez. No valida por sí solo todo el flujo al accionista.
- **Efecto.** Frente a A0, sube el flujo 139,4 (base 2025), porque corrige un error demostrado. No libera la valoración: R sigue pendiente.
- **Límites.** No fija R. La regla de un solo perímetro es (4a). El peso futuro del arrendamiento es (1b).

## (1b) Peso del arrendamiento

- **Qué se decide.** El estatus de la media 2023–25 de los pagos y de la amortización ROU.
- **Recomendación.** Usarla como **referencia de ensayo y convención declarada, no como estimación del peso futuro**, con su sensibilidad al peso de 2025 a la vista:
  - pagos: −16,8 en el flujo sin crecimiento (A0, A1 y A2);
  - amortización ROU que devuelve f: +10,1 (A1 y A2);
  - total en A1 y A2: **−6,7**.
- **Alternativas.**
  - Tomar el peso de 2025 u otro punto: sería elegir una cifra sin dato.
  - Estimar la tendencia: exige explicar por qué los pagos crecen más deprisa que las ventas (3,04 % → 3,30 % → 3,71 %), y eso no está publicado.
- **Fundamento.** Los pagos, la amortización y las ventas están publicados [P]. La sensibilidad es un cálculo [D]. El uso de la media es una hipótesis [H].
- **Efecto.** Ninguno en cifras registradas. Declara un intervalo de sensibilidad.
- **Límites.** El peso proyectado, en una valoración, sería una hipótesis declarada.

## (2) PPA, reposición de clientes y compras: dónde se cobra cada coste

- **Qué se decide.** La correspondencia de costes (tabla del §2 de la propuesta).
- **Recomendación.**
  - (i) La PPA no es un desembolso de reposición.
  - (ii) El gasto comercial queda en el margen, no en R.
  - (iii) La inversión propia en los clientes que sustituyen a los perdidos va en R.
  - (iv) Las compras de cartera necesarias, si se documentan, van en R o como término explícito, nunca solo como crecimiento.
  - (v) El margen lleva la PPA y la amortización ROU **como proporción constante de las ventas**, la misma que devuelve f, con sus efectos de escala declarados.
  - Se aplican V-F1f y V-F1h.
- **Alternativas.**
  - A1, la PPA como reposición perpetua en caja (≈ 85,7 al año): ningún dato publicado la sostiene. Con el mismo R, el flujo de partida baja 89,9.
  - Modelizar las adquisiciones como salida de caja con su PPA: exige M2, M6 y otra estructura del motor.
- **Fundamento.**
  - La PPA no es caja y en su mayor parte no es deducible [P][I].
  - Una partida que no es caja solo se anula en el flujo si el margen la lleva en la misma proporción que f devuelve. En euros fijos, o agotándose, no casa (casos P2g–P2i).
- **Efecto en Elis (escala).** La PPA, +4,2 en el flujo sin crecimiento de A2. La amortización ROU, −10,1 en A1 y A2. Juntas, en A2, −5,9. Frente a A1, con el mismo R, más flujo.
- **Límites.** Falta M2: la tasa de bajas y el desembolso por cliente nuevo. La «proporción constante» es una convención [H].

## (3a) Reinversión necesaria R

- **Qué se decide.** El estado y el perímetro de R.
- **Recomendación.**
  - R sigue en `pendiente_de_datos`, con perímetro R = R_propia + R_compras (+ la transición de sostenimiento).
  - La guarda V-F1c compara cada parte con su caja.
  - El intervalo 736,0–867,2 solo mide la materialidad de R_propia más la transición. Se aplican V-F1c y V-F1d.
- **Alternativas.**
  - Tomar un extremo:
    - el capex propio (cota B, flujo de partida 339,8) supone crecimiento sin inversión;
    - la D&A propia (A2, 477,8) tiene evidencia publicada en contra como caso central.
  - Un punto intermedio: sería elegir la cifra que falta. **No se propone.**
- **Fundamento.**
  - No hay ningún reparto publicado entre mantenimiento y crecimiento [B]. La revisión de E-ELIS lo confirma.
  - El capex propio es cota superior [I]. La D&A propia no es cota [I][P].
- **Efecto.** Ninguna cifra. Lo que está en juego, bajo la opción B de (4b), es de 339,8 a 477,8 en el flujo de partida: 138, el 45 % del FCF base.
- **Límites.** Elis sigue bloqueada mientras falte M1 (o M2 y M6, según las compras).

## (3b) Vía para obtener M1, M2, M6 y el plan climático

- **Qué se decide.** Cómo se intenta obtener esos datos. **Es una decisión de gestión, no económica.**
- **Opciones** (se puede elegir más de una):
  - (i) pedir el dato a Relación con Inversores, **por quien designe la persona responsable**. Este programa no envía mensajes a empresas;
  - (ii) más fuentes públicas no examinadas, como presentaciones de mercado de capitales o transcripciones. La búsqueda acotada de E-ELIS ya se hizo sin resultado; ampliarla tiene un rendimiento esperado bajo;
  - (iii) encargar una estimación documentada, con fuente, método, rango, responsable y revisión (V-F1d). Conserva su naturaleza de estimación;
  - (iv) mantener el bloqueo.
- **Recomendación.** (i) si la persona responsable quiere designar a alguien, y si no, (iv). (iii) solo con un responsable de la estimación.
- **Efecto.** Mientras no haya dato ni estimación documentada, R sigue pendiente.
- **Límites.** Una estimación aprobada no se convierte en dato publicado.

## (4a) Un solo perímetro para f, ancla de S2C, margen y ROIC del terminal

- **Qué se decide.** Si esos cuatro elementos deben usar el mismo perímetro declarado.
- **Recomendación.** Sí. Si no casan, el caso no se usa para una conclusión.
  - Se aplican V-F1g y V-F1k.
  - El terminal se compara con lo que ya tiene el libro, el bloque 10 de `Diagnóstico V6` con su umbral vigente C179. No se añade otro.
  - Signo, según la corrección W2: fila 178 = rentabilidad marginal − ROIC. Si |salto| > C179, G8 exige justificación.
- **Alternativas.** Permitir perímetros distintos: el caso mezclaría tratamientos del arrendamiento, la PPA o las compras.
- **Fundamento.** La especificación exige coherencia entre perímetros [D]. El orgánico publicado incluye precio y compras pequeñas [P].
- **Efecto en Elis.** Las palancas actuales no declaran perímetro, así que la compatibilidad del terminal queda pendiente. Los saltos del libro son +0,47, +0,68 y +2,41 puntos, todos por debajo de 5: informa, no avisa.
- **Límites.** Las anclas numéricas dependen de R.

## (4b) Clasificación de las compras de sociedades

- **Qué se decide.** Si las compras de sociedades de Elis cuentan como inversión de crecimiento.
- **Recomendación: opción A.** Se mantiene pendiente hasta M6, y V-F1j bloquea.
- **Alternativa: opción B.** Una hipótesis declarada, no un dato: las compras son crecimiento, con su apoyo parcial, y se revisa si llega M6.
- **Fundamento.**
  - El orgánico solo excluye las compras «importantes»: más de 5,0 M€ de ingresos en Francia y más de 3,0 M€ en otros países [P: URD25 p.313].
  - Las compras pequeñas, 31,5 al año de media en 2023–25, están **dentro** del orgánico.
  - La finalidad de esas compras no está publicada [B]; la búsqueda de E-ELIS no la localizó.
  - Según la revisión de E-ELIS, el 117,6 de 2025 es el total de M&A. Las compras pequeñas de 2025 son 37,3. Bodensee figura entre las «six major acquisitions» (URD25 p.312 y p.341).
- **Efecto.** Con la opción B, a crecimiento cero no se compra nada. Cada millón anual de compras que fuera de reposición bajaría el flujo sostenible en un millón, también en el año 11.
- **Límites.** Con la opción B, el crecimiento proyectado y el ancla se miden con adquisiciones. Un ancla orgánica exigiría M5, precio frente a volumen.

## (5a) Normalización de partidas de la ventana

- **Qué se decide.** Si se normalizan partidas concretas, con su regla fiscal, en lugar del diagnóstico 27,936.
- **Recomendación.**
  - No deducir el 27,936.
  - Regla **N1**: los ajustes de earnout de la nota 4.6 se sacan del EBIT y del resultado antes de impuestos de su año, sin efecto en el gasto por impuesto.
  - **N2** queda pendiente.
  - El resto de la nota 4.6 no se normaliza.
  - Se aplica V-F1l.
- **Opciones dentro de N1** (hay que elegirlas en el texto):
  - alcance: solo 2023–25, o también 2021–22, que solo entran en el τ de cinco años (+0,416 en el flujo sin crecimiento y +0,466 en el año 11 NORMAL);
  - incluir o no la actualización del earnout, ya verificada: −0,790 en el flujo sin crecimiento y −1,661 en el año 11 NORMAL.
- **Alternativa.** Mantener la calibración sin normalizar y declarar el diagnóstico.
- **Fundamento.**
  - Los ajustes de earnout son una revaluación del precio de adquisiciones, no coste de explotación.
  - No son deducibles: tienen línea propia en la conciliación fiscal [P].
  - Su caja está en las adquisiciones, fuera del FCF base [P].
- **Efecto.** N1 baja el flujo sin crecimiento entre **9,1 y 11,6**, según la convención del τ de proyección:
  - con el τ registrado de cinco años: −11,605, y −18,609 en el año 11 NORMAL;
  - con el τ de la ventana: −9,141.
- **Límites.** La cifra depende de una convención aparte (E8.1, abajo) y de la clasificación de las compras (4b o M6). N2 no se aplica mientras no se identifiquen la fiscalidad, la caja y la reposición.

## (5b) Inversión de transición (plan climático)

- **Qué se decide.** Cómo se clasifica la inversión de transición.
- **Recomendación.**
  - Se clasifica por su **finalidad documentada**, con su caja cobrada una sola vez: en la ventana, en los años 1–10 y en el año 11.
  - Como término explícito, sale del ancla de S2C. Si es temporal y dura más allá del año 10, lo pendiente se descuenta fuera de Gordon (W1, E3); **hasta implementarlo, H > 10 bloquea** (V-F1i).
  - Sin importe ni horizonte, la conclusión afectada queda pendiente.
  - Nunca cero por defecto ni perpetua por su nombre.
- **Alternativas.**
  - En R, proporcional a las ventas, si es sostenimiento permanente.
  - Como crecimiento, si amplía capacidad.
  - Lo que se descarta: cero por defecto, o perpetua por su nombre. Los casos P1a–P1e y V2a–V2e muestran los dobles cobros u omisiones que producirían.
- **Fundamento.**
  - El gasto del plan está dentro del capex, sin importe separado [P: URD25 p.122].
  - Los planes de deterioro suponen por él una inversión superior a la amortización histórica [P: p.369].
- **Efecto.** Ninguna cifra mientras falte M1.
- **Límites.** La taxonomía de la UE (1.160,0 / 842,0) no mide el plan climático: incluye derechos de uso y altas por combinaciones. Lo señaló la revisión de E-ELIS.

---

## Otras decisiones abiertas, sin cifra propuesta

- **Convención del τ de proyección (E8.1).**
  - Opciones: el τ registrado de cinco años o el de la ventana 2023–25.
  - Mueve N1 entre −9,1 y −11,6.
  - Es una decisión fuera de F1 que se declara con N1. No hay recomendación de cifra: la diferencia procede de la convención, no de N1.
- **Umbral de materialidad de V-F1a.** No se propone ninguno; el 0,5 % de la versión 1 no se adopta. Sin umbral, V-F1a bloquea con cualquier importe.

## Qué no valida ninguna de estas decisiones

- La aptitud para decisiones con dinero real.
- La valoración de Elis, que sigue en `pendiente_de_datos` por R.
- La identificación de θ/λ (P-M1).
- La solvencia ni el capital regulatorio de ningún caso C.

**Si se aprueban:**
1. registrarlas con fecha, persona y motivo, como E1–E6;
2. aplicarlas a la especificación y al motor con sus pruebas (E9, T8, T15 y T16), en la tarea F1-IMPL;
3. revisión independiente de lo que cambie.
