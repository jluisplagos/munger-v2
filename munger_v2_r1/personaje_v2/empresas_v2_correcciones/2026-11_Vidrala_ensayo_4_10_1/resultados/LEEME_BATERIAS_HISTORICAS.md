# Controles de las entregas sobre el árbol 4.10.1

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.10.1, y por qué. Para este árbol sustituye al LEEME de la 4.10 (`…_4_10/resultados/LEEME_BATERIAS_HISTORICAS.md`), que sigue describiendo el árbol 4.10. Las salidas de referencia de las tablas 2 y 3 y de los controles de la 4.10 y la 4.10.1 se obtuvieron sobre una copia limpia del árbol 4.10.1, después de `verificar_paquete.sh completa`, y se volvieron a comprobar sobre la descompresión del ZIP final (registro externo `…VERIFICACION.txt`).

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP;
- **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro y en el orden de las tablas (primero la 1 sin la 4.10.1, después la 2, la 3, el control de la 4.10 y, al final, el de la 4.10.1), nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I -B`.

**Dónde escriben.** En temporales, en `personaje_v2/.lo_perfil/` y, en algún caso, en `.pyc` de `personaje_v2/scripts/__pycache__/`, que el manifiesto ignora. El manifiesto sigue intacto después (comprobado: 2.193 archivos, ninguno modificado, ausente o de más, fuera de `personaje_v2/pruebas/` y `personaje_v2/.lo_perfil/`).

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Tienen que dar su resultado completo. Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo la 4.6, como en los árboles 4.9 y 4.10.
- **Controles ligados a las huellas, al texto o al código de su versión.** Los de la 4.7, la 4.7.1, la 4.8, la 4.8.1, la 4.9 y la 4.10, y las dos comparaciones de baterías del resumen. **No es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0. Manifiesto (2.193), entorno y piloto 35; 114/114 y 30/30; trazabilidad **78/78**; integridad 103/103; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55 | — |
| 4.2 | `contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `…/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.10.1** (último) | `…_4_10_1/scripts/comprobar_entrega_4_10_1.py` | **43 de 43**, código 0. Vuelve a ejecutar la batería de trazabilidad (78), `reproducir_T1.py`, las dos concordancias y `comparar_con_C1.py` (cuatro recálculos con LibreOffice) | `resultados/comprobar_entrega_4_10_1_salida.txt` |

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.10.1 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1, igual que en los árboles 4.9 y 4.10 (Z-1, decisión D-RV1c; `…_4_9/resultados/LEEME_BATERIAS_HISTORICAS.md` §2). La salida es idéntica byte a byte a la del árbol 4.10 | `resultados/comprobar_cierre_ensayo_4_6_en_arbol_4_10_1.txt` |

## 3. Controles ligados a las huellas, al texto o al código de su versión

| Entrega | Orden | Resultado sobre el árbol 4.10.1 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS», igual que en los árboles 4.9 y 4.10 | `resultados/comparar_baterias_4_7_1_en_4_8_1_en_arbol_4_10_1.txt` |
| 4.7 | `…_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1 | `resultados/comprobar_entrega_4_7_en_arbol_4_10_1.txt` |
| 4.7.1 | `…_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1 | `resultados/comprobar_entrega_4_7_1_en_arbol_4_10_1.txt` |
| 4.8 | `…_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1 | `resultados/comprobar_entrega_4_8_en_arbol_4_10_1.txt` |
| 4.8 (aparte) | `…_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS» | `resultados/comparar_baterias_4_7_1_de_4_8_en_arbol_4_10_1.txt` |
| 4.8.1 | `…_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **27 de 30**, código 1 | `resultados/comprobar_entrega_4_8_1_en_arbol_4_10_1.txt` |
| 4.9 | `…_4_9/scripts/comprobar_entrega_4_9.py` | **35 de 39**, código 1 (39 de 39 en su propio árbol) | `resultados/comprobar_entrega_4_9_en_arbol_4_10_1.txt` |
| 4.10 | `…_4_10/scripts/comprobar_entrega_4_10.py` | **41 de 44**, código 1 (44 de 44 en su propio árbol) | `resultados/comprobar_entrega_4_10_en_arbol_4_10_1.txt` |

**Por qué no cumplen los que no cumplen.**
- **4.7, 4.7.1, 4.8, 4.8.1 y las dos comparaciones de baterías.** Sus salidas son **idénticas byte a byte** a las del árbol 4.10 (`…_4_10/resultados/*_en_arbol_4_10.txt`): no cumplen los mismos casos, por los mismos motivos que explica el LEEME de la 4.10. La 4.10.1 no cambia nada de lo que fijan.
- **4.9.** No cumplen los mismos 4 casos que en el árbol 4.10. Solo cambia el detalle del caso 2 («Los archivos nuevos del manifiesto están en el expediente 4.9…»): la lista de archivos nuevos incluye ahora los del expediente de la 4.10.1.
- **4.10, 3 casos**, los tres por la propia 4.10.1:
  1. «los archivos nuevos están en el expediente de la 4.10, salvo acreditar_libro.py y la batería nueva»: la 4.10.1 añade su expediente;
  2. «verificar_paquete.sh completa exige la batería de trazabilidad (al menos 74 pruebas)»: el control busca el texto literal `-ge 74`, y ahora se exigen al menos 78 (`-ge 78`), es decir, la exigencia sube;
  3. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.10»: ahora describen la 4.10.1.

  Sus otras 41 comprobaciones cumplen: frente a la 4.9 solo cambian los archivos declarados, se reejecutan `n4_revision.py` y las 12 variantes con sus 14 identidades, y el equivalente de la mutación M22 hace fallar la batería de integridad.

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos (fuera de `personaje_v2/pruebas/` y `personaje_v2/.lo_perfil/`).
