# Control 4.12 con las palancas de la 4.11

**Resultado: CONCUERDA**.

- Precio de Sí 57.74229205598012 (piloto 57.74229205598012) · ponderado 62.6151093424602 (piloto 62.6151093424602) · zona caro (piloto caro).
- |Δ| máxima: V 0.0 · ponderado 0.0 · precio de Sí 0.0; probabilidades iguales: True.
- Entradas económicas del libro evaluado: 216 celdas; huella del control `aed6dfc7b3c0678e…`, del piloto `aed6dfc7b3c0678e…`; celdas distintas: ninguna.

| Variante | Ponderado control | Ponderado piloto | Precio de Sí control | Precio de Sí piloto | Zona | Igual |
|---|---|---|---|---|---|---|
| heredado | 70.7727096076804 | 70.7727096076804 | 66.01633263114212 | 66.01633263114212 | caro | sí |
| activa | 62.6151093424602 | 62.6151093424602 | 57.74229205598012 | 57.74229205598012 | caro | sí |
| solo_N1 | 68.8072681311826 | 68.8072681311826 | 64.22219571784528 | 64.22219571784528 | caro | sí |
| solo_N2 | 71.7703809544594 | 71.7703809544594 | 66.99696532376382 | 66.99696532376382 | caro | sí |
| solo_R1 | 70.3966870076162 | 70.3966870076162 | 65.2105699167188 | 65.2105699167188 | caro | sí |
| activa_sin_PM1 | 69.4037983765708 | 69.4037983765708 | 64.37230466928848 | 64.37230466928848 | caro | sí |
| activa_solo_P0 | 69.8931635643484 | 69.8931635643484 | 64.86166985706609 | 64.86166985706609 | caro | sí |
| estructura_H | 69.0754536530832 | 69.0754536530832 | 63.10943433292637 | 63.10943433292637 | caro | sí |
| estructura_S | 61.6175799824173 | 61.6175799824173 | 57.029771084520966 | 57.029771084520966 | caro | sí |
| estructura_SR2 | 64.0251809995452 | 64.0251809995452 | 58.86947696065307 | 58.86947696065307 | caro | sí |
| estructura_SRF | 66.1043661578198 | 66.1043661578198 | 60.459406146762696 | 60.459406146762696 | caro | sí |
| convencion_anios_alternativa | 62.1927218730298 | 62.1927218730298 | 57.479933077286304 | 57.479933077286304 | caro | sí |
| convencion_terminal_alternativa | 63.558884332344 | 63.558884332344 | 58.379859697917695 | 58.379859697917695 | caro | sí |

Recorrido del pipeline:

- ESPERANDO: extraccion_v63 → extracto_v63.md (ver ESPERANDO.md y prompts_generados/)
- agente simulado extraccion_v63: extracto_v63.md del piloto 4.11, sin cambios
- ESPERANDO: fase_a → fase_a.json (ver ESPERANDO.md y prompts_generados/)
- agente simulado fase_a: fase_a.json, fase_a.md del piloto 4.11, sin cambios
- ESPERANDO: fase_b → fase_b.json (ver ESPERANDO.md y prompts_generados/)
- agente simulado fase_b: fase_b.json, fase_b.md del piloto 4.11, sin cambios
- ESPERANDO: fase_c_turno1 → fase_c.json (ver ESPERANDO.md y prompts_generados/)
- el pipeline pide la fase C: valoración y variantes hechas; el control termina aquí
