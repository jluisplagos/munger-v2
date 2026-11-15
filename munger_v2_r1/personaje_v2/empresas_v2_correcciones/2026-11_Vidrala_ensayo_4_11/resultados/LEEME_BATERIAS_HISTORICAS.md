# Controles de las entregas sobre el árbol 4.11

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.11, y por qué. Para este árbol sustituye al LEEME de la 4.10.1 (`…_4_10_1/resultados/LEEME_BATERIAS_HISTORICAS.md`), que sigue describiendo el árbol 4.10.1.

**De dónde salen las referencias.** Las salidas de referencia de las tablas 2 y 3 y del control de la 4.11 se obtuvieron sobre una copia limpia del árbol 4.11, después de `verificar_paquete.sh completa`. La de la 4.9 lista entero, por diseño, cada archivo nuevo del manifiesto, y entre ellos están estas mismas salidas de referencia: por eso se tomó de la descompresión del ZIP, que ya las contiene. Todas se volvieron a comprobar sobre la descompresión del ZIP final; el resultado está en el registro externo `…VERIFICACION.txt`.

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP;
- **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro y en el orden de las tablas: primero la 1 sin la 4.11, después la 2 y la 3, y al final el control de la 4.11;
- nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I -B`.

**Dónde escriben.** En temporales, en `personaje_v2/.lo_perfil/` y, en algún caso, en `.pyc` de `personaje_v2/scripts/__pycache__/`. El manifiesto ignora esas tres cosas. La batería de la V6.4 de `verificar_paquete.sh completa` escribe además en `personaje_v2/pruebas/_v64/`.

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Tienen que dar su resultado completo. Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo la 4.6, como en los árboles 4.9, 4.10 y 4.10.1.
- **Controles ligados a las huellas, al texto o al código de su versión.** Son los de la 4.7 a la 4.10.1 y las dos comparaciones de baterías del resumen. **Que no den su resultado completo no es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0: manifiesto, entorno, piloto 35, 114/114, 30/30, integración V6.4 **58/58**, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55 | — |
| 4.2 | `contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `…/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.11** (último) | `…_4_11/scripts/comprobar_entrega_4_11.py` | 38 de 38, código 0 (7 reejecutan, 31 constatan) | `resultados/comprobar_entrega_4_11_salida.txt` |

**Detalle del 4.6.1.** Mantiene su resultado completo porque el bloque de la batería de la V6.4 va el primero de los obligatorios de `verificar_paquete.sh`. Su control de integración (`comprobar_integracion_verificador.py`) extrae el tramo que va desde el bloque de cierre hasta el resultado global. Con el bloque nuevo en ese tramo daba 22 de 23, y se corrigió el orden.

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.11 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1, igual que en los árboles 4.9, 4.10 y 4.10.1 (Z-1, decisión D-RV1c) | `resultados/comprobar_cierre_ensayo_4_6_en_arbol_4_11.txt` |

## 3. Controles ligados a las huellas, al texto o al código de su versión

| Entrega | Orden | Resultado sobre el árbol 4.11 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS», igual que en los árboles 4.9, 4.10 y 4.10.1 | `resultados/comparar_baterias_4_7_1_en_4_8_1_en_arbol_4_11.txt` |
| 4.7 | `…_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1 | `resultados/comprobar_entrega_4_7_en_arbol_4_11.txt` |
| 4.7.1 | `…_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1 | `resultados/comprobar_entrega_4_7_1_en_arbol_4_11.txt` |
| 4.8 | `…_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1 | `resultados/comprobar_entrega_4_8_en_arbol_4_11.txt` |
| 4.8 (aparte) | `…_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS» | `resultados/comparar_baterias_4_7_1_de_4_8_en_arbol_4_11.txt` |
| 4.8.1 | `…_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **27 de 30**, código 1 | `resultados/comprobar_entrega_4_8_1_en_arbol_4_11.txt` |
| 4.9 | `…_4_9/scripts/comprobar_entrega_4_9.py` | **35 de 39**, código 1 | `resultados/comprobar_entrega_4_9_en_arbol_4_11.txt` |
| 4.10 | `…_4_10/scripts/comprobar_entrega_4_10.py` | **40 de 44**, código 1 (41 de 44 en el árbol 4.10.1) | `resultados/comprobar_entrega_4_10_en_arbol_4_11.txt` |
| 4.10.1 | `…_4_10_1/scripts/comprobar_entrega_4_10_1.py` | **38 de 43**, código 1 (43 de 43 en su propio árbol) | `resultados/comprobar_entrega_4_10_1_en_arbol_4_11.txt` |

### Por qué no cumplen los que no cumplen

**Mismos casos que en el árbol 4.10.1, con otro detalle.** En la 4.7, la 4.7.1, la 4.8, la 4.8.1 y la 4.9 no cumplen los mismos casos, por los mismos motivos que explica el LEEME de la 4.10.1, con el mismo recuento. Solo cambia el detalle de las comprobaciones «solo cambian los archivos declarados / conservan su huella» y «los archivos nuevos están en…»: la lista de archivos que cambian empieza ahora por los de la 4.11 (Anexo D, esquemas, prompts y scripts de la integración) y la de archivos nuevos incluye los de la 4.11.

**Salida idéntica a la del árbol 4.10.1.** Las dos comparaciones de baterías y, en la tabla 2, la 4.6.

**4.10: un caso más que en el árbol 4.10.1 (40 de 44 frente a 41).** «Frente al manifiesto de la 4.9 solo cambian los archivos declarados» no cumple porque la 4.11 cambia archivos que la 4.10 no declaró: el Anexo D, los dos esquemas, cinco prompts y 16 scripts de producción. Los otros tres casos son los del árbol 4.10.1.

**4.10.1: cinco casos, los cinco por la propia 4.11.**
1. «Frente a la 4.10 solo cambian los seis archivos declarados»: la 4.11 cambia 24 más (Anexo D, dos esquemas, cinco prompts y 16 scripts).
2. «Todos los archivos nuevos están en el expediente de la 4.10.1»: los nuevos de la 4.11 están en su expediente, en `v6/v64_experimental/` y en los scripts, la configuración y la batería que declara.
3. «El resto del árbol de la 4.10 conserva sus bytes en disco»: la 4.11 cambia los archivos que declara en `REGISTRO_ENTREGA_4.11.md` §2.
4. «El código de producción (`personaje_v2/scripts/`, 31 archivos) no cambia»: la 4.11 cambia, a propósito, 16 de ellos.
5. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.10.1»: ahora describen la 4.11.

Sus otras 38 comprobaciones cumplen. Entre ellas están:
- la batería de trazabilidad reejecutada (78/78);
- la reproducción de T-1;
- las dos concordancias;
- la comparación con C1, con cuatro recálculos.

**Nota sobre el desarrollo.** Durante el desarrollo, sobre el árbol de trabajo, la 4.10 dio 41 de 44 y la 4.10.1, 40 de 43. Esos dos controles comparan con el `MANIFIESTO_SHA256.txt` del propio árbol, que entonces era todavía el de la 4.10.1. Las cifras válidas son las de esta tabla, obtenidas con el manifiesto de la 4.11.

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos. No cuentan `personaje_v2/pruebas/`, `personaje_v2/.lo_perfil/` ni las carpetas `.lo_perfil/` de los expedientes.
