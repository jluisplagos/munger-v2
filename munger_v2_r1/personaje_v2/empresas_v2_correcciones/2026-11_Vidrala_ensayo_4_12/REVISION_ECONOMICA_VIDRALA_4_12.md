# Revisión económica del cierre nuevo de Vidrala (encargo 4.12 §7)

**Qué es.** La revisión que pide el encargo sobre el expediente `cierre_condicionado/Vidrala`: base 2025, configuración de demostración de la 4.11 (no adoptada), agentes reales y código final. Separa los **hechos comprobados** (cifras del libro recalculado y de las variantes calculadas, con su archivo), las **interpretaciones** y lo que queda **condicional**. No cambia ningún criterio ni ninguna conclusión del expediente.

**Fuentes de las cifras.**
- `cierre_condicionado/resultados/datos_revision_economica.md`: la hoja «Conciliación B» por escenario y las bases de «Configuración V6.4».
- `cierre_condicionado/resultados/comparacion_homogenea.md`: heredado frente a experimental, con las mismas entradas y palancas.
- `cierre_condicionado/Vidrala/configuracion_v64_variantes.md`: 15 variantes calculadas sobre copias del libro.
- `cierre_condicionado/resultados/replica_independiente.txt`: la réplica independiente de la 4.11 sobre los 16 libros finales: 16 de 16 coinciden, con diferencias ≤ 6,4e-14 €/acción en los valores y ≤ 4,8e-12 M€ en la conciliación.

Cifras en millones de euros salvo que se diga otra cosa; N = 35,182858 millones de acciones.

**Resultado del expediente.** Con el código final y agentes reales, el expediente termina así:
- estado **concluido**, auditoría interna **APROBADO** (16/16), cubo Vigilar, acción esperar;
- precio 90,10 € (cierre del 31-dic-2025, la fecha base), zona caro; precio de Sí 56,02 € (ponderado 60,70 €);
- objetivo **condicionado y provisional** (`objetivo_condicionado`): lo condicionan PM1.estructura, PM1.familia y PM1.parametro;
- valor calculado condicional 56,018 €;
- rango calculado del precio de Sí: 51,29–65,72 € en 14 variantes, todas en «caro».

## 1. Reposición frente a crecimiento y posibles dobles cómputos

**Hechos.**
- En la activa (SR1 · Λ con λ = 1,15 · P0), cada año del NORMAL invierte:
  - la reposición contable (la amortización menos la cartera P0): 128,5–132,9;
  - el requisito adicional: 19,3–19,9;
  - la inversión fija para crecer: 17,7 en el año 1 y 27,3 en el año 10.

  En total, 165–180 al año en inversión fija bruta, frente a una amortización de 132,9. La Historia de 2021–2025 da un capex de 739,0 frente a 509,6 de amortización (capex ÷ D&A = 1,45), con 188,5 de capex en 2025.
- SR1 reestima el S2C de los años con f = D_hist ÷ (D_hist − Rh) = 530,0 ÷ (530,0 − 75,0) = 1,165. La parte de la reinversión histórica atribuida a reposición (Rh = (λ − 1) × 500,2) se quita del denominador del S2C histórico: así el requisito no se cuenta dos veces en los años.
- Variantes (Δ del precio de Sí frente a la activa, 56,02 €):

  | Variante | Δ precio de Sí |
  |---|---|
  | S (suma sin reestimar) | −0,50 € |
  | SR2 (también ROIC × f en el terminal) | +1,06 € |
  | SRF | +2,41 € |
  | H (la inversión para crecer también repone) | +5,35 € |
  | sin P-M1 | +6,61 € |

**Interpretación.**
- **Años.** El doble cómputo que S tiene y SR1 evita vale poco (0,50 €), porque el crecimiento del NORMAL es moderado (1,5 % en los años 1–5).
- **Terminal.** Queda un doble cómputo posible: SR1 conserva el ROIC de la fase B y además carga el requisito. Si ese ROIC ya era neto de reposición (la pregunta Q-ROIC1, sin decidir), sobra hasta 1,06 € (SR2).
- **Mayor incertidumbre estructural.** Está entre H y el resto (5,35 €): si la misma inversión repone y hace crecer. Las cuentas no lo separan.

## 2. Coherencia del S2C de los años con el ROIC del terminal

**Hechos (Conciliación B, fila «S2C y ROIC efectivos»).**

| | MALO | NORMAL | BUENO |
|---|---|---|---|
| S2C efectivo de los años (= S2C de la fase B × f) | 0,815 | 1,048 | 1,281 |
| Rentabilidad marginal implícita de los años (S2C × margen × (1 − t)) | 9,5 % | 14,7 % | 20,0 % |
| ROIC efectivo del terminal | 9 % | 9 % | 12 % |
| Salto del FCF del año 10 al terminal | −9,5 % | −11,5 % | −11,3 % |

**Interpretación.**
- **Discontinuidad en el año 11.** En el NORMAL, el crecimiento de los años 1–10 rinde en el margen un 14,7 %, por encima de r (9 %). En la perpetuidad rinde el 9 %, igual que r, así que el crecimiento terminal no crea valor.
- **Parte del salto la crea SR1.** Eleva el S2C de los años con f y deja el ROIC del terminal sin cambio. SR2 alinea las dos partes (ROIC × f = 10,5 % en el NORMAL) y da +1,06 €.
- **Lo demás es de la fase B.** El salto también se debe a la elección de un ROIC de largo plazo igual a r en el MALO y el NORMAL, que es una elección de juicio de la fase B, no un efecto de la configuración.

## 3. Efectos de la convención terminal

**Hechos.**
- **Convención activa.** Requisito plano en los años y proporcional a las ventas en el terminal. Por eso el requisito salta en el año 11 un +20,1 % en el NORMAL (V11 ÷ V0 = 1.760 ÷ 1.465) y un +40,4 % en el BUENO.
- **Valor presente del requisito, por acción.** En los años 1–10, 3,6 €. En el terminal, 3,0 € (MALO), 4,4 € (NORMAL) y 5,6 € (BUENO).
- **Alternativas.**
  - Años también proporcionales: −0,13 €.
  - Terminal «crece con g»: +0,40 €.

**Interpretación.** Las convenciones mueven poco el precio de Sí: de −0,13 € a +0,40 €. Sí dejan una incoherencia interna: si la reposición crece con el negocio en la perpetuidad, no hay razón económica para que sea plana en los años de crecimiento. Es una convención declarada, no un error, y no cambia la zona.

## 4. Capacidad conservada (R1) y comportamiento del escenario MALO

**Hechos.**
- **Ventas.** En el MALO bajan de 1.465,2 (2025) a 1.338,2 en los años 7–8 (−8,7 %) y vuelven a 1.358,4 en el año 10 y a 1.371,9 en el terminal. Están siempre por debajo del máximo conservado.
- **Inversión fija para crecer.** Con R1 es 0 en los diez años, y la palanca S2C no actúa (aviso `s2c_inerte`).
- **Circulante.** Se liberan 18,7 en los años de caída y se vuelve a absorber en la recuperación.
- **Requisito.** Se mantiene plano (19,3–19,9) aunque las ventas caigan: la capacidad se conserva y se repone.
- **Terminal.** Carga 15,8 de inversión fija para crecer al ritmo g aunque las ventas del año 11 sigan un 6,4 % por debajo del máximo (límite 1 del README; aviso `terminal_r1_sin_maximo_conservado`). Su valor presente es 2,54 € por acción del valor MALO (44,32 €), unos 0,51 € del ponderado.
- **R1 aislado frente al heredado.** Precio de Sí −1,36 €. Con R0, la caída de ventas libera capital fijo.

**Interpretación.**
- El MALO de R1 es prudente en los dos extremos:
  - en los años no libera capital fijo y mantiene la reposición de una capacidad que no se usa;
  - en el terminal paga crecimiento que la capacidad sobrante podría cubrir.
- Una especificación que reconozca la capacidad sobrante en la perpetuidad (D411-TERMINAL-R1, sin decidir) subiría el valor MALO como mucho unos 2,5 € por acción. Es menos, porque las ventas al 1 % tardarían unos siete años en recuperar el máximo.
- La regla no demuestra que Vidrala conserve la capacidad: es una hipótesis.

## 5. Dependencia de la conclusión respecto de las hipótesis no adoptadas

**Hechos.**
- **Zona.** Las 15 variantes calculadas dan «caro». El precio, 90,10 € (cierre del 31-dic-2025), está por encima del mayor precio de Sí calculado (65,72 €, solo N2): un 37,1 % por encima de él, con la diferencia dividida entre ese precio de Sí.
- **Precio de Sí.**
  - Va de 51,29 € (λ = 1,25) a 65,72 €, frente a 56,02 € de la activa: de −8,4 % a +17,3 %.
  - Con la V6.3 efectiva sobre el mismo libro (heredado) es 64,75 €.
- **Descomposición frente al heredado** (comparación homogénea): de −8,73 € en total, −6,61 € son de P-M1 con la cartera. Los demás componentes son de N1, N2 y R1:

  | Componente aislado | Δ precio de Sí |
  |---|---|
  | N1 (tipo normalizado) | −1,71 € |
  | R1 | −1,36 € |
  | N2 (margen de partida) | +0,97 € |

  Los efectos aislados no son aditivos.

**Interpretación.**
- **Acción «esperar por precio».** Se sostiene en todo el ámbito calculado: ninguna variante la cambia.
- **Precio objetivo.** Su nivel depende de elecciones no adoptadas: λ, la estructura, la cartera P0, R1 y los tipos y márgenes normalizados. Es un **valor calculado condicional**, no un objetivo adoptado. Esta revisión las lee todas como no observadas. La fase C del expediente, en cambio, da fundamento suficiente a N1, N2, R1 y la cartera, y solo deja como hipótesis que condicionan el objetivo PM1.estructura, PM1.familia y PM1.parametro, que son las que publican las salidas. La diferencia es de juicio: las banderas de la fase C no las contrasta ninguna regla (revisión interna R5; informe integrado §9.6, L15).
- **Rango.** No es un intervalo de confianza. No cubre hipótesis no exploradas, como otros márgenes, otras probabilidades u otra r.

## 6. Qué se sostiene con las fuentes disponibles y qué sigue siendo condicional

- **Se sostiene, con el ámbito declarado:**
  - con estas palancas de la fase B y con cualquiera de las configuraciones calculadas, el precio de 2025 está por encima del precio de Sí;
  - la aritmética de cada variante es correcta: identidad de la conciliación anual y terminal y réplica independiente 16 de 16;
  - las entradas económicas de las variantes son las del libro final (instantánea idéntica).
- **Es condicional:**
  - el nivel del precio de Sí (51–66 €), y con él cualquier objetivo;
  - la parte de reposición por encima de la amortización (λ no observado; la estructura no se puede elegir con las cuentas publicadas);
  - el terminal de R1 en el MALO;
  - la coherencia entre el S2C de los años y el ROIC del terminal;
  - las convenciones de la reposición.
- **Qué lo resolvería** (información, no decisiones):
  - el desglose del capex entre mantenimiento, reconstrucción de hornos y crecimiento, con sus importes por planta, o la vida útil y el coste corriente de reposición de los hornos;
  - el historial de ventas y capacidad en caídas de demanda;
  - una decisión sobre Q-ROIC1 y sobre el terminal de R1.

## 7. Lo que dice la fase C del expediente (juicio del agente, no de esta revisión)

- **Mantenimiento** (`configuracion_v64.mantenimiento`, `adoptada: false`). La reposición supera la amortización: capex ÷ D&A de 1,45 en 2021–2025 y de 1,42 en 2025, con la renovación de hornos como destino principal.
  - Medida contra el exceso histórico, λ = 1,15 es «un tercio del exceso histórico»; todo el exceso como reposición daría λ ≈ 1,46.
  - La estructura más coherente con los hechos sería SR1, con confianza baja:
    - H no encaja: en 2025 hubo exceso sin crecimiento;
    - S cuenta dos veces;
    - SRF quita más de lo que muestra la historia;
    - SR2 corrige un ROIC que en el NORMAL es una convención.
- **Salto del año 11 (G8).** La fase C lo justifica:
  - en el NORMAL, como convención: «con las bases heredadas el salto sería ≈ 4,0 puntos; los 5,7 los crea el factor f de la configuración (SR1)». Es la misma discontinuidad que el apartado 2;
  - en el BUENO, como fundamentado.
- **Avisos de dominio.** Los activos (`terminal_r1_sin_maximo_conservado`, `s2c_inerte`) y el factor f no son materiales para la conclusión, y se dicen en el diagnóstico.

**Coincidencias y diferencias con esta revisión.**
- Coinciden en que el objetivo es condicional por la reposición y en que la discontinuidad del año 11 la amplifica SR1.
- Esta revisión añade la cota del doble cómputo posible del terminal (SR2, +1,06 €) y la del terminal de R1 en el MALO (≤ 2,5 € del valor MALO). También añade la incoherencia de las convenciones (plana en los años, proporcional en el terminal) y la descomposición frente al heredado.
- Difieren en qué hipótesis carecen de fundamento. Esta revisión lee como no observadas también N1, N2, R1 y la cartera P0. La fase C les da fundamento suficiente y deja como condicionantes solo las tres de P-M1 (revisión interna R5). Tampoco cubre el ámbito la familia de P-M1: ninguna variante calcula Θ, y las salidas lo dicen desde la corrección R3.
