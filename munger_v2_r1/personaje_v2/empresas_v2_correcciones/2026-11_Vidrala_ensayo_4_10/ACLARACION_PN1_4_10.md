# P-N1 · los dos sentidos actuales de «favorable» (aclaración documental, sin cambio de criterio)

**[Hecho] Fuentes.**
- `personaje_munger_v2.md` §15 (S-19, datos ausentes): una conclusión favorable es «`comprar`, o `esperar` con precio objetivo». Si un dato ausente es material para sostenerla, no se emite: cubo Vigilar, sin acción, `pendiente_de_datos`.
- §14 (D10, fundamento material) y `ANEXO_D` §«Correspondencia D10 ↔ estado ↔ acción»: D10 solo limita `comprar`. Con `concluido` y `esperar`, el fundamento es «no procede (conclusión no favorable)», porque D10 no la limita.
- El orden de prevalencia (§15) es: bloqueo → límite del modelo → descalificador → dato ausente material (S-19) → falta de fundamento (D10) → zona.

**Tabla de casos, según las reglas vigentes:**

| # | Conclusión que el personaje emitiría | Carencia | Regla que actúa | Estado y acción hoy |
|---|---|---|---|---|
| 1 | comprar | ninguna | — | `concluido` · Sí · comprar |
| 2 | comprar | dato ausente material | S-19 | `pendiente_de_datos` · Vigilar · sin acción |
| 3 | comprar | hipótesis sin fundamento (sin comprobación conjunta superada) | D10 | `pendiente_de_investigacion` · Vigilar · sin acción |
| 4 | esperar con objetivo (precio de Sí) | ninguna | — | `concluido` · Vigilar · esperar |
| 5 | esperar con objetivo | dato ausente material | S-19 (esperar con objetivo cuenta como favorable) | `pendiente_de_datos` · Vigilar · sin acción |
| 6 | esperar con objetivo | hipótesis sin fundamento | D10 no actúa (para D10 no es favorable) | `concluido` · Vigilar · esperar · fundamento «no procede» |
| 7 | descartar o demasiado difícil | dato ausente | S-19 no bloquea si se explica por qué no afecta | `concluido` · No / Demasiado difícil |

**[Interpretación] La asimetría.** La falta de datos bloquea «esperar con objetivo» (caso 5); la falta de fundamento, no (caso 6). Es lo que dicen las reglas: no es un error de implementación, y la tabla `FUNDAMENTO_C104` de `cierre_v2.py` lo aplica.

**Aclaración documental (sin cambio de criterio).**
- «Favorable» en S-19 significa **conclusión con objetivo**: comprar, o esperar con precio objetivo.
- «Favorable» en D10 significa **conclusión de compra**: comprar.
- Esta aclaración no amplía D10 a nuevas acciones ni reduce ningún bloqueo.

**Cambio de criterio posible** (se propone aparte como D-PN1, sin aplicar). Que D10 limite también «esperar con objetivo».
- Es más estricto: el caso 6 pasaría a `pendiente_de_investigacion`.
- Consecuencia: los cierres «esperar» con hipótesis sin fundamento dejarían de ser `concluido`, y haría falta revisar los expedientes cerrados afectados.
- Igualar S-19 a D10 (caso 5 → `concluido`) reduciría bloqueos y no se propone.
