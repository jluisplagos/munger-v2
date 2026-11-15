# Baterías y controles históricos sobre el árbol 4.8.1

**Qué es este documento.** Dice qué debe dar cada control de una entrega anterior cuando se ejecuta sobre el árbol de la 4.8.1, y por qué. Sirve a la persona responsable para comprobar que la 4.8.1 no rompe nada de lo anterior.

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP;
- **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro, nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I`.

Todos escriben solo en temporales; el manifiesto sigue intacto después.

**La 4.8.1 separa dos cosas:**
- **las exigencias funcionales del código vigente:** las baterías de `verificar_paquete.sh completa` y el control de la 4.8.1;
- **los controles históricos ligados a las huellas de su versión:** los de la 4.7, la 4.7.1 y la 4.8. Esos dejan de dar su resultado completo en cuanto una entrega posterior cambia los archivos cuyas huellas fijan. No es una regresión.

Las reproducciones del defecto con código antiguo (`reproduccion/`) son otra cosa: muestran el fallo, no exigen nada al código vigente.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado esperado | Salida de referencia |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA. Manifiesto, entorno y piloto 35; 114/114 y 30/30; solicitudes de auditoría **55/55**; estados 28/28; resumen 45/45; cierre 55/55 | — |
| 4.2 | `python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` (idéntica) |
| 4.3 | `python3 -I contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `…/resultados/revision_salida.txt` (idéntica) |
| 4.3.1 | `python3 -I contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `…/resultados/subsanacion_salida.txt` (idéntica) |
| 4.4 | `python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` (idéntica) |
| 4.5 | `…/2026-11_Vidrala_ensayo_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` (idéntica) |
| 4.6 | `…/2026-11_Vidrala_ensayo_4_6/scripts/comprobar_cierre_ensayo.py` | 24 de 24 | `…_4_6/resultados/comprobar_cierre_ensayo_salida.txt` (idéntica) |
| 4.6.1 | `…/2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` (idéntica) |
| Baterías del resumen de la 4.7.1 | `…/2026-11_Vidrala_ensayo_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 0. Las tres baterías coinciden en el estado de cada prueba, el principio de las que fallan y la línea final: 45/45, 35/45 y 36/45. Solo cambian las huellas de archivos declarados por la 4.8 y la 4.8.1 | `resultados/comparar_baterias_4_7_1_en_4_8_1_salida.txt` (idéntica) |
| **4.8.1** | `…/2026-11_Vidrala_ensayo_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **30 de 30**, código 0, en unos 10–15 minutos (vuelve a ejecutar las 25 mutaciones) | `resultados/comprobar_entrega_4_8_1_salida.txt` (idéntica) |

## 2. Controles ligados a las huellas de su versión (por diseño, incompletos sobre este árbol)

| Entrega | Orden | Resultado esperado | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.7 | `…/2026-11_Vidrala_ensayo_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1 | `resultados/comprobar_entrega_4_7_en_arbol_4_8_1.txt` |
| 4.7.1 | `…/2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1 | `resultados/comprobar_entrega_4_7_1_en_arbol_4_8_1.txt` |
| 4.8 | `…/2026-11_Vidrala_ensayo_4_8/scripts/comprobar_entrega_4_8.py` | **33 de 36**, código 1 | `resultados/comprobar_entrega_4_8_en_arbol_4_8_1.txt` |
| 4.8 (aparte) | `…/2026-11_Vidrala_ensayo_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS». Los estados son iguales, pero cambian huellas que la 4.8 no declaraba (§1 tiene la versión de la 4.8.1) | `resultados/comparar_baterias_4_7_1_de_4_8_en_arbol_4_8_1.txt` |

**Por qué no cumplen los que no cumplen.** Todos los casos se explican por los archivos que la 4.8.1 declara cambiados:
- `pipeline.py` y `cierre_v2.py`;
- `prompts/verificacion.md`;
- `pruebas/agentes_sinteticos.py` y `pruebas/test_resumen_v2.py`. Los dos escriben la línea «Solicitud de auditoría», sin tocar ninguna expectativa;
- `verificar_paquete.sh`;
- el Anexo D y `DECISIONES.md`;
- `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`;
- los archivos nuevos del expediente `…_4_8_1/`.

**4.7, los 4 que no cumplen:**
1. Huellas de los 1.342 archivos de la 4.6.1: cambian `prompts/verificacion.md` y `agentes_sinteticos.py`.
2. Huellas del código del bloque A.
3. Integración de la batería del resumen. Ya no cumplía sobre el árbol 4.7.1.
4. Control de vigencia final.

Frente al árbol 4.8 se añade el punto 1.

**4.7.1, los 6 que no cumplen:**
1. Huellas de los 1.400 archivos de la 4.7.
2. Huellas del código del cierre técnico.
3. Las tres baterías del resumen. Cambia la línea de huellas; los estados son iguales (§1).
4. La 4.7 dentro de la 4.7.1, que esperaba 46 de 49.
5. Material del control de vigencia.
6. Documentación de la 4.7.1.

Frente al árbol 4.8 se añaden los puntos 1 y 4.

**4.8, los 3 que no cumplen:**
1. «El código 4.7.1 reconstruido […] y el resto del código del cierre no cambió»: cambia `cierre_v2.py`.
2. «Respecto a la 4.7.1 solo cambian los archivos declarados»: el control compara el manifiesto vigente con la lista de la 4.8, y la 4.8.1 cambia además `prompts/verificacion.md`, `pruebas/agentes_sinteticos.py`, `pruebas/test_resumen_v2.py` y `cierre_v2.py`.
3. «Ningún archivo añadido en los originales ni en los expedientes anteriores»: el control de la 4.8 cuenta como añadido cualquier archivo nuevo en `empresas_v2_correcciones/`, y los de la 4.8.1 lo son.

## 3. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las dos tablas.
- Un recuento distinto del esperado.
- En la tabla 2, un control que no cumple y no está en las listas de arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos.
