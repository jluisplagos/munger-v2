# Comparación numérica · ensayo 4.6 frente a 4.5

Generado por `scripts/comparar_con_4_5.py`. «Igual» significa idéntico (huella o valor exacto) salvo donde se indica.

| Control | Resultado | Detalle |
|---|---|---|
| fase1_decisiones.json (P1, fuentes y entradas) | IGUAL / CUMPLE | b4e47afcb3dd… |
| fase1_v63.json (P1, fuentes y entradas) | IGUAL / CUMPLE | 8afd98798895… |
| fase1_fuentes.json (P1, fuentes y entradas) | IGUAL / CUMPLE | 06a2f2ea5ae2… |
| fase1_metadatos.json (P1, fuentes y entradas) | IGUAL / CUMPLE | 470be1364cf7… |
| datos_v63.json (P1, fuentes y entradas) | IGUAL / CUMPLE | 6456c7acea20… |
| Vidrala_v63_datos.xlsx (P1, fuentes y entradas) | IGUAL / CUMPLE | b3b7f9413bc7… |
| Vidrala_v63_base.xlsx (P1, fuentes y entradas) | IGUAL / CUMPLE | c21b41512be2… |
| fase1_partes/ (10 archivos) | IGUAL / CUMPLE |  |
| texto/ (10 archivos) | IGUAL / CUMPLE |  |
| etapa1/ (3 archivos) | IGUAL / CUMPLE |  |
| extracto_v63.md (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| fase_a.json (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| fase_a.md (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| fase_b.json (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| fase_b.md (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| referencias_mecanicas.json (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| datos_ausentes.json (no se vuelven a ejecutar las fases A y B) | IGUAL / CUMPLE |  |
| fase_c.json: única diferencia la etiqueta «fundamento …» de C104 (formato armonizado; juicios y números iguales) | IGUAL / CUMPLE | ['.celdas.C104'] · antes «… · ponderado 70.5 · fundamento no procede (conclusión no favorable; hipótesis Palancas C8 acotada) · resultado…» · después «… · ponderado 70.5 · fundamento no procede (conclusión no favorable) · hipótesis que más condiciona: Palancas C8 (acotada) · resultado mecáni…» |
| fase_c.md: solo cambian las líneas que citan la etiqueta de C104 (la de C104 y la que explica su etiqueta) | IGUAL / CUMPLE | líneas [135, 137] |
| libro evaluado (celdas escritas y fórmulas): única celda distinta Análisis!C104 | IGUAL / CUMPLE | Análisis!C104 |
| libro evaluado recalculado (valores): única celda distinta Análisis!C104 | IGUAL / CUMPLE | Análisis!C104 |
| resultados.json (salvo la ruta de origen): valores, estados, palancas, probabilidades, r_op, puente, V0, m0, t, f | IGUAL / CUMPLE | iguales |
| resultados.json → celdas_juicio_analisis: única diferencia C104 | IGUAL / CUMPLE |  |
| precio.json: V por escenario, ponderado, precio de Sí, MALO, zona, DCF inverso | IGUAL / CUMPLE | ponderado 70.4952 · precio de Sí 65.6881 · zona caro |
| r = 0,09 y probabilidades 0,2 / 0,6 / 0,2 | IGUAL / CUMPLE |  |
| caja 108,352 sin restar el dividendo; puente 160,784 | IGUAL / CUMPLE |  |
| contraste entre motores (B0, A1, A2, A2a, A2b) sobre el libro 4.6: mismos valores que en la 4.5 | IGUAL / CUMPLE | [] |
| descomposición del contraste: idéntica | IGUAL / CUMPLE |  |
| ficha: mismos valores, estado, cubo, decisión y fundamento que en la 4.5 | IGUAL / CUMPLE | iguales |
| ficha: campos nuevos solo los de la reparación (datos_etapa1_incompletos, alcance y cierre o provisional) | IGUAL / CUMPLE | alcance, cierre, datos_etapa1_incompletos |

RESULTADO: 30 de 30 controles iguales o cumplidos.
