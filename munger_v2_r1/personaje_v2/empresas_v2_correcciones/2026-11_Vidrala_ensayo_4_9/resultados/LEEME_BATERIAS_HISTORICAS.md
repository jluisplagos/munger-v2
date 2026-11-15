# Controles de las entregas sobre el árbol 4.9

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.9, y por qué. Para este árbol sustituye al LEEME de la 4.8.1 (`…_4_8_1/resultados/LEEME_BATERIAS_HISTORICAS.md`), que sigue describiendo el árbol 4.8.1. Los resultados y las salidas de referencia de abajo son los **observados** sobre una descompresión limpia del paquete; la verificación del ZIP final está en `REGISTRO_ENTREGA_4.9.md` §8.

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP;
- **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro y en el orden de las tablas, nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I`. Con `-B`, además, no escriben `__pycache__` en el árbol; sin `-B`, Python puede dejar archivos `.pyc` en las carpetas `scripts/`, que el manifiesto ignora.

**Dónde escriben.** En temporales. Algunos (los que recalculan con LibreOffice usando el perfil del árbol) actualizan además archivos de `personaje_v2/.lo_perfil/`, que no está en el manifiesto. El manifiesto sigue intacto después.

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Comprueban comportamiento y resultados: las baterías de `verificar_paquete.sh completa`, los controles de la 4.2 a la 4.6.1 y el control de la 4.9. **Tienen que dar su resultado completo.** Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo una: el control de la 4.6, por la corrección Z-1 de la 4.9 (§2).
- **Controles ligados a las huellas o al texto de su versión.** Los de la 4.7, la 4.7.1, la 4.8 y la 4.8.1, y las dos comparaciones de baterías del resumen, fijan además huellas de archivos, frases de la documentación o líneas exactas del código de su momento. Dejan de dar el resultado completo en cuanto una entrega posterior cambia esos archivos. **No es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0, en unos 10 minutos. Manifiesto, entorno y piloto 35; 114/114 y 30/30; integridad **103/103**; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55 | — |
| 4.2 | `python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `python3 -I contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `python3 -I contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…/2026-11_Vidrala_ensayo_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…/2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.9** (último) | `…/2026-11_Vidrala_ensayo_4_9/scripts/comprobar_entrega_4_9.py` | **39 de 39**, código 0, en unos 10–11 minutos (vuelve a ejecutar las 31 mutaciones, las dos baterías de R-V1 y los recálculos de N4) | `…_4_9/resultados/comprobar_entrega_4_9_salida.txt` |

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.9 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…/2026-11_Vidrala_ensayo_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1 (24 de 24 hasta la 4.8.1) | `resultados/comprobar_cierre_ensayo_4_6_en_arbol_4_9.txt` |

**Por qué.** El único caso que no cumple es «cierre_v2.motivo_rechazo_cierre: ningún motivo de rechazo» sobre el expediente histórico de la 4.6, que no tiene `cierre_vigente.json`. Por la corrección Z-1 de la 4.9, un cierre sin ningún registro de qué `auditoria.md` se aprobó ya no se acepta («no consta la respuesta de auditoría aprobada»): antes, cualquier APROBADO que nombrara el material lo confirmaba. Es la misma consecuencia que la 4.6.1 ya declaró para la vigencia de esos expedientes. El expediente no se modifica. Queda como decisión D-RV1c (`propuestas/decisiones_y_preguntas_4_9.json`); `comprobar_entrega_4_9.py` lo comprueba.

## 3. Controles ligados a las huellas o al texto de su versión

| Entrega | Orden | Resultado sobre el árbol 4.9 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…/2026-11_Vidrala_ensayo_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS» (código 0 en el árbol 4.8.1) | `resultados/comparar_baterias_4_7_1_en_4_8_1_en_arbol_4_9.txt` |
| 4.7 | `…/2026-11_Vidrala_ensayo_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1, igual que en el árbol 4.8.1 | `resultados/comprobar_entrega_4_7_en_arbol_4_9.txt` |
| 4.7.1 | `…/2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1, igual que en el árbol 4.8.1 | `resultados/comprobar_entrega_4_7_1_en_arbol_4_9.txt` |
| 4.8 | `…/2026-11_Vidrala_ensayo_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1 (33 de 36 en el árbol 4.8.1) | `resultados/comprobar_entrega_4_8_en_arbol_4_9.txt` |
| 4.8 (aparte) | `…/2026-11_Vidrala_ensayo_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.8.1 | `resultados/comparar_baterias_4_7_1_de_4_8_en_arbol_4_9.txt` |
| 4.8.1 | `…/2026-11_Vidrala_ensayo_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **27 de 30**, código 1 (30 de 30 en su propio árbol), en unos 4–5 minutos | `resultados/comprobar_entrega_4_8_1_en_arbol_4_9.txt` |

**Por qué no cumplen los que no cumplen.**
- **Comparación de las baterías del resumen (4.8.1).** Las tres baterías conservadas siguen dando **los mismos estados, fallos y línea final** que en su entrega. Lo que cambia es la lista de huellas distintas: la 4.9 cambia `cierre_v2.py`, `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py`, y la comparación marca como «FUERA DE LO DECLARADO» los que no declararon la 4.8 y la 4.8.1. Es una comprobación de huellas, no de comportamiento.
- **4.7 y 4.7.1:** los mismos 4 y 6 casos que en el árbol 4.8.1 (`…_4_8_1/resultados/LEEME_BATERIAS_HISTORICAS.md` §2). Las listas de archivos con huellas distintas incluyen ahora también los que cambia la 4.9.
- **4.8, 4 casos:**
  - los 3 del árbol 4.8.1 (`cierre_v2.py` cambiado; archivos cambiados fuera de la lista de la 4.8; archivos nuevos en `empresas_v2_correcciones/`), con `informe.py` en la lista;
  - **uno nuevo, «VERSION dice entrega 4.8»:** el control busca ese texto, que estaba contenido en «entrega 4.8.1» y no lo está en «entrega 4.9». Está ligado al texto de `VERSION`.
- **Comparación de baterías de la 4.8:** la misma situación que la de la 4.8.1, con la lista de huellas ampliada.
- **4.8.1, 3 casos, los tres ligados a su versión:**
  1. **«Frente al manifiesto de la 4.8 solo cambian los archivos declarados».** La 4.9 cambia `ficha.py`, `informe.py` y `resumen.py`, que la 4.8.1 no declaró.
  2. **«Mutaciones del código de R-T1: las 25 …».** La mutación M5 («el cierre no compara la respuesta registrada») ya no se puede aplicar: buscaba la línea exacta de la 4.8.1 que comparaba la respuesta por su huella de contenido sin orden, y **esa línea es precisamente la que sustituye la reparación R-V1** (`INFORME_RV1_4_9.md` §2). La propiedad que protegía, que el cierre compare la respuesta registrada, la cubren ahora con más fuerza la batería de integridad (103) y sus mutaciones M01, M04 y M05.
  3. **«VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.8.1».** Ahora describen la 4.9.

  Las reproducciones de ese control con el código de la 4.8 (X-c y la batería de estados con las fechas renovadas, 27/28) **cumplen**: `ficha.py`, `informe.py` y `resumen.py` no dependen de funciones nuevas de `cierre_v2.py` (`REGISTRO_ENTREGA_4.9.md` §7).

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos (fuera de `personaje_v2/pruebas/` y `personaje_v2/.lo_perfil/`).
