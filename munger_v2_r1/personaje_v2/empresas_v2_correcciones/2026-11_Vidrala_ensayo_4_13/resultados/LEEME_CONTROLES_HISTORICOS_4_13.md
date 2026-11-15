# Controles de las entregas sobre el árbol 4.13

**Qué es este documento.** Dice qué da cada control de una entrega cuando se ejecuta sobre el árbol de la 4.13, y por qué. Para este árbol sustituye al LEEME de la 4.12 (`…_4_12/resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`), que sigue describiendo el árbol 4.12.

**De dónde salen las referencias.**
- Las salidas `resultados/controles_historicos_en_arbol_4_13/<control>.txt` se obtuvieron sobre la copia limpia del árbol 4.13 de la ronda B, después de `verificar_paquete.sh completa`, con `scripts/controles_historicos_4_13.py`. Antes se habían corregido dos comprobaciones del propio control de la 4.13 (§3, «4.13»).
- Se volvieron a comprobar sobre la descompresión del ZIP final. El resultado está en el registro externo de verificación.

**Cómo se ejecutan.**
- Desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP.
- **Después** de `bash verificar_paquete.sh completa`.
- Todos de una vez, en orden y uno detrás de otro, con `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/scripts/controles_historicos_4_13.py CARPETA_SALIDA`. Nunca dos a la vez, porque varios usan LibreOffice. Tardan unos 31 minutos; la verificación completa, unos 37.
- El script escribe una salida por control y `resumen.md`, con el código, la última línea y dos comparaciones: si la salida es idéntica a la de referencia de su propia entrega, cuando la tiene, y si es igual que en el árbol 4.12.

**Dónde escriben.** En temporales, en `personaje_v2/.lo_perfil/` y, en algún caso, en `.pyc` de `__pycache__/`. El manifiesto ignora esas tres cosas, y el ZIP no las lleva. La batería de la V6.4 de `verificar_paquete.sh completa` escribe además en `personaje_v2/pruebas/_v64/`.

**Tres clases de controles, que no deben confundirse:**
- **Exigencias funcionales.** Tienen que dar su resultado completo. Un fallo sería una regresión.
- **Exigencia funcional que cambia por una reparación declarada.** Solo la 4.6, como en los árboles 4.9 a 4.12.
- **Controles ligados a las huellas, al texto o al código de su versión.** Son los de la 4.7 a la 4.12 y las dos comparaciones de baterías del resumen. **Que no den su resultado completo no es una regresión**; cada caso se explica en §3.

## 1. Exigencias funcionales (resultado completo)

| Qué | Orden | Resultado | Salida de referencia (idéntica) |
|---|---|---|---|
| Verificación completa | `bash verificar_paquete.sh completa` | PASA, código 0: manifiesto, entorno, piloto 35, 114/114, 30/30, integración V6.4 **195/195**, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55 (unos 37 minutos) | `resultados/bateria_completa_4_13.txt` (registro de la ronda B, con las huellas de los scripts); detalle de la V6.4 en `resultados/bateria_v64_detalle_4_13.txt` |
| 4.2 | `contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | todas | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `…/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `…_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6.1 | `…_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.13** (último) | `…_4_13/scripts/comprobar_entrega_4_13.py` | 89 de 89, código 0 (20 reejecutan, 69 constatan) | `resultados/controles_historicos_en_arbol_4_13/4_13_comprobar_entrega.txt` |

## 2. Exigencia funcional que cambia por una reparación declarada

| Entrega | Orden | Resultado sobre el árbol 4.13 | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.6 | `…_4_6/scripts/comprobar_cierre_ensayo.py` | **23 de 24**, código 1, igual que en los árboles 4.9 a 4.12 (Z-1, decisión D-RV1c) | `resultados/controles_historicos_en_arbol_4_13/4_6_comprobar_cierre_ensayo.txt` |

## 3. Controles ligados a las huellas, al texto o al código de su versión

| Entrega | Orden | Resultado sobre el árbol 4.13 | Salida de referencia (idéntica) |
|---|---|---|---|
| Baterías del resumen de la 4.7.1 (4.8.1) | `…_4_8_1/scripts/comparar_baterias_4_7_1_en_4_8_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.12 | `resultados/controles_historicos_en_arbol_4_13/4_8_1_comparar_baterias_4_7_1_en_4_8_1.txt` |
| 4.7 | `…_4_7/scripts/comprobar_entrega_4_7.py` | **45 de 49**, código 1, igual que en el árbol 4.12 | `resultados/controles_historicos_en_arbol_4_13/4_7_comprobar_entrega.txt` |
| 4.7.1 | `…_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **38 de 44**, código 1, igual que en el árbol 4.12 | `resultados/controles_historicos_en_arbol_4_13/4_7_1_comprobar_entrega.txt` |
| 4.8 | `…_4_8/scripts/comprobar_entrega_4_8.py` | **32 de 36**, código 1, igual que en el árbol 4.12 | `resultados/controles_historicos_en_arbol_4_13/4_8_comprobar_entrega.txt` |
| 4.8 (aparte) | `…_4_8/scripts/comparar_baterias_4_7_1.py` | Código 1, «HAY DIFERENCIAS», igual que en el árbol 4.12 | `resultados/controles_historicos_en_arbol_4_13/4_8_comparar_baterias_4_7_1.txt` |
| 4.8.1 | `…_4_8_1/scripts/comprobar_entrega_4_8_1.py` | **25 de 30**, código 1 (27 de 30 en el árbol 4.12) | `resultados/controles_historicos_en_arbol_4_13/4_8_1_comprobar_entrega.txt` |
| 4.9 | `…_4_9/scripts/comprobar_entrega_4_9.py` | **34 de 39**, código 1, como en el árbol 4.12, con otro detalle | `resultados/controles_historicos_en_arbol_4_13/4_9_comprobar_entrega.txt` |
| 4.10 | `…_4_10/scripts/comprobar_entrega_4_10.py` | **40 de 44**, código 1, como en el árbol 4.12, con otro detalle | `resultados/controles_historicos_en_arbol_4_13/4_10_comprobar_entrega.txt` |
| 4.10.1 | `…_4_10_1/scripts/comprobar_entrega_4_10_1.py` | **38 de 43**, código 1, como en el árbol 4.12, con otro detalle | `resultados/controles_historicos_en_arbol_4_13/4_10_1_comprobar_entrega.txt` |
| 4.11 | `…_4_11/scripts/comprobar_entrega_4_11.py` | **34 de 38**, código 1, como en el árbol 4.12, con otro detalle | `resultados/controles_historicos_en_arbol_4_13/4_11_comprobar_entrega.txt` |
| 4.12 | `…_4_12/scripts/comprobar_entrega_4_12.py` | **59 de 63**, código 1 (63 de 63 en su propio árbol) | `resultados/controles_historicos_en_arbol_4_13/4_12_comprobar_entrega.txt` |

«Igual que en el árbol 4.12» quiere decir que la salida es idéntica byte a byte a la que se guardó en ese árbol (`…_4_12/resultados/controles_historicos_en_arbol_4_12/`).

### Por qué no cumplen los que no cumplen

**Salida idéntica a la del árbol 4.12.** La 4.6 (tabla 2), las dos comparaciones de baterías, la 4.7, la 4.7.1 y la 4.8. No cumplen los mismos casos, por los motivos que explican los LEEME de la 4.10.1, la 4.11 y la 4.12.

**4.9, 4.10 y 4.10.1: el mismo recuento que en el árbol 4.12, con otro detalle.** Las comprobaciones «solo cambian los archivos declarados» y «los archivos nuevos están en…» listan ahora también los archivos de la 4.13: el expediente de la 4.13, la plantilla `v6/v641_experimental/`, `config_v2_v641_experimental.json` y `estructura_json.py`. En la 4.9 sigue sin cumplir, como en el árbol 4.12, «CONTINUIDAD.md §2 remite al LEEME de la 4.9»: ahora remite a este LEEME.

**4.11: el mismo recuento que en el árbol 4.12, con otro detalle.**
- «Los archivos de la 4.10.1 que cambian son exactamente los declarados» lista además `referencias_mecanicas.py`, que la 4.13 cambia para anclar el S2C del perímetro NIIF 16 en B155 (R6).
- «Los archivos nuevos están…» lista los nuevos de la 4.13.
- Los otros dos casos, el mínimo de la batería de la V6.4 y los documentos de versión, son los del árbol 4.12.

**4.12: cuatro casos, los cuatro por la propia 4.13.**
1. «Los archivos de la 4.11 que cambian son exactamente los declarados»: la 4.13 cambia además `leer_v63.py` (lectura del perímetro efectivo), `referencias_mecanicas.py` (ancla del S2C, R6) y `rellenar_fase1_v63.py` (sustitución de la evidencia activa, §6). Son cambios declarados en `CAMBIOS_ARCHIVOS.txt` y en la lista de cambios del control de la 4.13.
2. «Los archivos nuevos están en el expediente 4.12 o son los declarados»: los nuevos de la 4.13 están en su expediente, en `v6/v641_experimental/`, en `estructura_json.py` y en la configuración V6.4.1.
3. «`verificar_paquete.sh completa` exige la batería de la V6.4 con al menos 127 pruebas»: ahora exige al menos 195 (la batería de la 4.13).
4. «VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.12»: ahora describen la 4.13.

Sus otras 59 comprobaciones cumplen, entre ellas las once que reejecutan.

**4.8.1: dos casos más que en el árbol 4.12 (25 de 30 frente a 27).** Los tres del árbol 4.12 siguen igual, con las listas de archivos de la 4.13. Los dos nuevos son reejecuciones con el código de la 4.8 y tienen la misma causa:
- «Con el código de la 4.8, X-c + esquema restaurado + `--desde 13` reutiliza la auditoría antigua…: salida idéntica a la conservada».
- «Batería de estados con el código de la 4.8 y todas las fechas renovadas: 27/28». Da 11/28.

**Causa.** El control monta un árbol mixto. Pone el `pipeline.py` y el `cierre_v2.py` de la 4.8, y deja el resto de los scripts del árbol, entre ellos el `ficha.py` actual. La corrección R1 de la 4.13 hace que `ficha.py` lea la ficha con `cierre_v2.leer_ficha_control`. Esa función existe desde la 4.9 y no está en el `cierre_v2.py` de la 4.8, así que en el árbol mixto `ficha.py` falla con `AttributeError` y el pipeline de la 4.8 se detiene donde antes llegaba.

**Comprobación.** Sobre el mismo árbol mixto, con el `ficha.py` de la 4.12 (huella `d269982e…`, la del manifiesto de la 4.12) en lugar del actual:
- la batería de estados da exactamente **27/28**, con la misma prueba fallida de X-c que espera el control;
- la reproducción de R-T1 sale **idéntica** a `…_4_8_1/reproduccion/rt1_con_codigo_4_8.txt`.

Lo que cambia es la compatibilidad del `ficha.py` actual con el `cierre_v2.py` de la 4.8, que el paquete no usa. No hay una regresión del código de la 4.8 ni del actual. Dentro del paquete, `ficha.py` y `cierre_v2.py` son de la misma versión, y las baterías obligatorias pasan.

**4.13 (tabla 1).** La ronda B, antes de corregir el control, dio 87 de 89. Los dos casos eran defectos del propio control, no del motor:
- «La ronda final de `verificar_paquete.sh completa` está registrada»: buscaba en el registro la palabra «VEREDICTO», que `verificar_paquete.sh` no escribe, y el registro aún no estaba en el árbol. Ahora se acredita con «RESULTADO GLOBAL: PASA», `rc=0`, la V6.4 entera y las huellas de los scripts al día.
- «Sin `__pycache__` en el árbol al terminar el control»: las carpetas las dejaban `verificar_paquete.sh` y los controles anteriores, no el control de la 4.13. Ahora se comprueba que el control no escribe ningún `.pyc` (foto al empezar y al terminar), y sus subprocesos tampoco escriben cachés. El ZIP no lleva `__pycache__`, y eso se comprueba en el registro externo.

Las cifras válidas son las de la tabla, obtenidas con el control corregido.

## 4. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia de esta carpeta, en cualquiera de las tablas.
- Un recuento distinto del de la tabla.
- En las tablas 2 y 3, un caso que no cumple y no está explicado arriba.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos. No cuentan `personaje_v2/pruebas/`, `personaje_v2/.lo_perfil/`, las carpetas `.lo_perfil/` de los expedientes ni las `__pycache__/`.
