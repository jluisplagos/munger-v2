# Controles de las entregas sobre el árbol 4.10

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.10, y por qué. Para este árbol sustituye al LEEME de la 4.9 (`…_4_9/resultados/LEEME_BATERIAS_HISTORICAS.md`), que sigue describiendo el árbol 4.9. Los resultados y las salidas de referencia de abajo son los **observados** sobre una descompresión limpia del paquete; la verificación del ZIP final está en su registro externo (`…VERIFICACION.txt`).

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP;
- **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro y en el orden de las tablas (primero la 1 sin la 4.10, después la 2, la 3 y, al final, la 4.10), nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I -B`.

**Dónde escriben.** En temporales, en `personaje_v2/.lo_perfil/` y, en algún caso (`efectos_n4.py`, dentro del control de la 4.9), en `.pyc` de `personaje_v2/scripts/__pycache__/`, que el manifiesto ignora. El manifiesto sigue intacto después.

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Tienen que dar su resultado completo. Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo la 4.6, como en el árbol 4.9.
- **Controles ligados a las huellas, al texto o al código de su versión.** Los de la 4.7, la 4.7.1, la 4.8, la 4.8.1 y la 4.9, y las dos comparaciones de baterías del resumen. **No es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0. Manifiesto, entorno y piloto 35; 114/114 y 30/30; trazabilidad **74/74**; integridad 103/103; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55 | — |
| 4.2 | `contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `…/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.10** (último) | `…_4_10/scripts/comprobar_entrega_4_10.py` | **44 de 44**, código 0. Vuelve a ejecutar `n4_revision.py`, las 12 variantes con LibreOffice y la batería de integridad con el equivalente de M22 | `resultados/comprobar_entrega_4_10_salida.txt` |

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.10 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1, igual que en el árbol 4.9 (Z-1, decisión D-RV1c; `…_4_9/resultados/LEEME_BATERIAS_HISTORICAS.md` §2) | `resultados/comprobar_cierre_ensayo_4_6_en_arbol_4_10.txt` |

## 3. Controles ligados a las huellas, al texto o al código de su versión

| Entrega | Orden | Resultado sobre el árbol 4.10 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.9 | `resultados/comparar_baterias_4_7_1_en_4_8_1_en_arbol_4_10.txt` |
| 4.7 | `…_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1 | `resultados/comprobar_entrega_4_7_en_arbol_4_10.txt` |
| 4.7.1 | `…_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1 | `resultados/comprobar_entrega_4_7_1_en_arbol_4_10.txt` |
| 4.8 | `…_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1 | `resultados/comprobar_entrega_4_8_en_arbol_4_10.txt` |
| 4.8 (aparte) | `…_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS» | `resultados/comparar_baterias_4_7_1_de_4_8_en_arbol_4_10.txt` |
| 4.8.1 | `…_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **27 de 30**, código 1 | `resultados/comprobar_entrega_4_8_1_en_arbol_4_10.txt` |
| 4.9 | `…_4_9/scripts/comprobar_entrega_4_9.py` | **35 de 39**, código 1 (39 de 39 en su propio árbol) | `resultados/comprobar_entrega_4_9_en_arbol_4_10.txt` |

**Por qué no cumplen los que no cumplen.**
- **4.7, 4.7.1, 4.8 y 4.8.1.** No cumplen los **mismos casos** que en el árbol 4.9 (comprobado nombre por nombre). Lo único que cambia es el detalle: las listas de archivos con huellas distintas o nuevos incluyen ahora los que cambia o añade la 4.10.
- **Las dos comparaciones de baterías.** Igual que en el árbol 4.9: los estados, los fallos y la línea final son los conservados; cambia la lista de huellas.
- **4.9, 4 casos:**
  1. «Frente al manifiesto de la 4.8.1 solo cambian los archivos declarados…»: la 4.10 cambia archivos que la 4.9 no declaró.
  2. «Los archivos nuevos del manifiesto están en el expediente 4.9…»: la 4.10 añade su expediente, `acreditar_libro.py` y la batería nueva.
  3. «Mutaciones del código de R-V1: las 31…», con 30 de 31. La mutación M22 ya no se puede aplicar: buscaba la línea exacta `txt = datos.decode("utf-8")` de `motivo_rechazo_cierre`, y **esa es la línea que sustituye la corrección 3.2** (lectura común antes de H2). La propiedad que protegía, que un `auditoria.md` no UTF-8 retira la aprobación sin traza, sigue cubierta: la batería de integridad da 103/103, y el control de la 4.10 aplica la mutación equivalente sobre el código nuevo y comprueba que la batería falla.
  4. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.9»: ahora describen la 4.10.

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos (fuera de `personaje_v2/pruebas/` y `personaje_v2/.lo_perfil/`).
