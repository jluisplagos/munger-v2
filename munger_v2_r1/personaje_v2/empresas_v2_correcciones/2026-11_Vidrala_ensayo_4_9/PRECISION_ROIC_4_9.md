# Precisión sobre el ROIC terminal (entrega 4.9, encargo §6)

**Qué se corrige.** El informe de la 4.8.1 (`…/2026-11_Vidrala_ensayo_4_8_1/INFORME_REINVERSION_4_8_1.md`) dice dos veces que falta la justificación del ROIC a largo plazo de la fase B:
- en la línea 251: «**Información insuficiente:** falta cómo se fijó el ROIC_lp en la fase B»;
- en la fila de la tabla de la línea 310: «Falta la justificación de ese parámetro en la fase B».

**[Hecho] Esa afirmación no es correcta.** La justificación está conservada en el expediente de referencia (`…/2026-11_Vidrala_ensayo_4_6_1/Vidrala/`), escenario por escenario:
- `fase_b.json` → `palancas` → `roic_lp`. Para MALO, NORMAL y BUENO recoge la referencia mecánica, el valor, la desviación, la clase («fundamentada»), la confianza, el `porque`, el `apoyo` con sus celdas y páginas, y `lo_sustituiria`:
  - MALO, 0,09: el foso se diluye y el rendimiento converge a la tasa y al sector (9,3 %).
  - NORMAL, 0,11: foso estrecho; 2 puntos sobre la tasa; unos 2 puntos de erosión frente a la rentabilidad marginal de los años 1–10, que es de ≈13 %.
  - BUENO, 0,12: el ROIC de los peores años desde 2018.
- `fase_b.md`, sección «ROIC a largo plazo (B18:D18)», con el mismo razonamiento y la comprobación ROIC > g en los tres escenarios.

La 4.9 no modifica el informe de la 4.8.1, que es un expediente histórico. La corrección vale desde aquí y queda anotada en `CONTINUIDAD.md` y en `REGISTRO_ENTREGA_4.9.md`.

**[Hecho] Lo que sí falta.** Ni `fase_b.json` ni `fase_b.md` dicen si el ROIC_lp del terminal se mide:
- **neto de la reposición**, es decir, sobre la inversión que excede el mantenimiento;
- o **sobre una inversión que ya la incluye**.

Tampoco lo separan del crecimiento. Esa separación es la que distinguiría entre las estructuras SR1 y SR2 de la 4.8.1, que reestiman el S2C sin reestimar el ROIC del terminal o reestimándolo.

**[Interpretación] Esta precisión no elige ninguna estructura.**
- Saber cómo se fijó el ROIC_lp no dice cómo se trata la reposición en el terminal.
- SR1, SR2 y SRF siguen siendo alternativas sin elegir.
- D-N3b y D-N3e siguen sin rellenar.
- P-M1 sigue abierta.

La 4.9 no inicia ninguna selección de hipótesis de mantenimiento ni amplía el encargo a N5–N10.

**[Propuesta] Pregunta para la persona responsable o para una fase B futura** (no enviada, sin efecto):
- ¿El ROIC_lp de 0,09 / 0,11 / 0,12 se pensó como rendimiento de la inversión neta de reposición o de la inversión total?
- Si es lo primero, la combinación coherente con la suma es la que no reestima el ROIC del terminal.
- Si es lo segundo, la combinación coherente es la que lo reestima.

La pregunta está en `propuestas/decisiones_y_preguntas_4_9.json` (Q-ROIC1).
