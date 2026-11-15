# Controles de las entregas sobre el árbol 4.12

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.12, y por qué. Para este árbol sustituye al LEEME de la 4.11 (`…_4_11/resultados/LEEME_BATERIAS_HISTORICAS.md`), que sigue describiendo el árbol 4.11.

**De dónde salen las referencias.** Las salidas `resultados/controles_historicos_en_arbol_4_12/<control>.txt` se obtuvieron sobre una copia limpia del árbol 4.12, después de `verificar_paquete.sh completa`, con `scripts/controles_historicos_4_12.py`. Se volvieron a comprobar sobre la descompresión del ZIP final; el resultado está en el registro externo de verificación.

**Cómo se ejecutan.**
- Desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP.
- **Después** de `bash verificar_paquete.sh completa`.
- Todos de una vez, en orden y uno detrás de otro, con `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/scripts/controles_historicos_4_12.py CARPETA_SALIDA`. Nunca dos a la vez, porque varios usan LibreOffice.
- El script escribe una salida por control y `resumen.md`, con el código, la última línea y dos comparaciones: si la salida es idéntica a la de referencia de su propia entrega, cuando la tiene, y si es igual que en el árbol 4.11.

**Dónde escriben.** En temporales, en `personaje_v2/.lo_perfil/` y, en algún caso, en `.pyc` de `personaje_v2/scripts/__pycache__/`. El manifiesto ignora esas tres cosas. La batería de la V6.4 de `verificar_paquete.sh completa` escribe además en `personaje_v2/pruebas/_v64/`.

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Tienen que dar su resultado completo. Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo la 4.6, como en los árboles 4.9 a 4.11.
- **Controles ligados a las huellas, al texto o al código de su versión.** Son los de la 4.7 a la 4.11 y las dos comparaciones de baterías del resumen. **Que no den su resultado completo no es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0: manifiesto, entorno, piloto 35, 114/114, 30/30, integración V6.4 **127/127**, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55 (unos 23 minutos) | — |
| 4.2 | `contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `…/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.12** (último) | `…_4_12/scripts/comprobar_entrega_4_12.py` | 63 de 63, código 0 (11 reejecutan, 52 constatan) | `resultados/controles_historicos_en_arbol_4_12/4_12_comprobar_entrega.txt` |

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.12 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1, igual que en los árboles 4.9 a 4.11 (Z-1, decisión D-RV1c) | `resultados/controles_historicos_en_arbol_4_12/4_6_comprobar_cierre_ensayo.txt` |

## 3. Controles ligados a las huellas, al texto o al código de su versión

| Entrega | Orden | Resultado sobre el árbol 4.12 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_8_1_comparar_baterias_4_7_1_en_4_8_1.txt` |
| 4.7 | `…_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1, igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_7_comprobar_entrega.txt` |
| 4.7.1 | `…_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1, igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_7_1_comprobar_entrega.txt` |
| 4.8 | `…_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1, igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_8_comprobar_entrega.txt` |
| 4.8 (aparte) | `…_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_8_comparar_baterias_4_7_1.txt` |
| 4.8.1 | `…_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **27 de 30**, código 1, igual que en el árbol 4.11 | `resultados/controles_historicos_en_arbol_4_12/4_8_1_comprobar_entrega.txt` |
| 4.9 | `…_4_9/scripts/comprobar_entrega_4_9.py` | **34 de 39**, código 1 (35 de 39 en el árbol 4.11) | `resultados/controles_historicos_en_arbol_4_12/4_9_comprobar_entrega.txt` |
| 4.10 | `…_4_10/scripts/comprobar_entrega_4_10.py` | **40 de 44**, código 1, como en el árbol 4.11, con otro detalle | `resultados/controles_historicos_en_arbol_4_12/4_10_comprobar_entrega.txt` |
| 4.10.1 | `…_4_10_1/scripts/comprobar_entrega_4_10_1.py` | **38 de 43**, código 1, como en el árbol 4.11, con otro detalle | `resultados/controles_historicos_en_arbol_4_12/4_10_1_comprobar_entrega.txt` |
| 4.11 | `…_4_11/scripts/comprobar_entrega_4_11.py` | **34 de 38**, código 1 (38 de 38 en su propio árbol) | `resultados/controles_historicos_en_arbol_4_12/4_11_comprobar_entrega.txt` |

«Igual que en el árbol 4.11» quiere decir que la salida es idéntica byte a byte a la que se guardó en ese árbol (`…_4_11/resultados/*_en_arbol_4_11.txt`).

### Por qué no cumplen los que no cumplen

**Salida idéntica a la del árbol 4.11.** La 4.6 (tabla 2), las dos comparaciones de baterías, la 4.7, la 4.7.1, la 4.8 y la 4.8.1. No cumplen los mismos casos, por los motivos que explican los LEEME de la 4.10.1 y de la 4.11 (`…_4_11/resultados/LEEME_BATERIAS_HISTORICAS.md`).

**4.10 y 4.10.1: el mismo recuento que en el árbol 4.11, con otro detalle.** Las comprobaciones «solo cambian los archivos declarados» y «los archivos nuevos están en…» listan ahora también los archivos de la 4.12: la guía del recorrido supervisado, el expediente de la 4.12 y los scripts nuevos de la integración.

**4.9: un caso más que en el árbol 4.11 (34 de 39 frente a 35).**
- «CONTINUIDAD.md §2 remite a los resultados de los controles históricos del LEEME de la 4.9» no cumple porque el apartado 2 de `CONTINUIDAD.md` remite ahora a este LEEME, `LEEME_CONTROLES_HISTORICOS_4_12.md`, y el control busca el nombre de los LEEME de la 4.9 a la 4.11 (`LEEME_BATERIAS_HISTORICAS.md`).
- Los otros cuatro casos son los del árbol 4.11, con las listas de archivos de la 4.12.

**4.11: cuatro casos, los cuatro por la propia 4.12.**
1. «Los archivos de la 4.10.1 que cambian son exactamente los declarados»: la 4.12 cambia además `resumen.py` y `agentes_sinteticos.py` (§4 del informe integrado).
2. «Los archivos nuevos están en el expediente 4.11, en `v6/v64_experimental/` o son los declarados»: los nuevos de la 4.12 están en su expediente, en la guía y en los scripts nuevos de la integración.
3. «`verificar_paquete.sh completa` exige la batería de la V6.4 (al menos 58 pruebas)»: ahora exige al menos 127 (la batería de la 4.12).
4. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.11»: ahora describen la 4.12.

Sus otras 34 comprobaciones cumplen, entre ellas las siete que reejecutan.

**4.12 (tabla 1).** Durante el desarrollo, una ronda provisional sobre una copia del árbol anterior a la respuesta a la segunda revisión interna dio 59 de 63. Tres casos eran el defecto RA1 del propio control (comparaba instantáneas de relaciones distintas), corregido. El cuarto era la falta de este LEEME, que entonces no existía. Las cifras válidas son las de la tabla, obtenidas sobre el árbol final.

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia de esta carpeta, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos. No cuentan `personaje_v2/pruebas/`, `personaje_v2/.lo_perfil/` ni las carpetas `.lo_perfil/` de los expedientes.
