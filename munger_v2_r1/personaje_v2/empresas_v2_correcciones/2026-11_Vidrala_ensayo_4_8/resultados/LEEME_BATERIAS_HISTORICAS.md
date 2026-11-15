# Baterías y controles históricos sobre el árbol 4.8

**Qué es este documento.** Fija qué debe dar cada control de entregas anteriores cuando se ejecuta sobre el árbol de la 4.8, y por qué. Sirve a la persona responsable para comprobar que la 4.8 no rompe nada de lo anterior.

**Cómo se ejecutan:**
- desde `munger_v2_r1/`, sobre una descompresión limpia del ZIP y **después** de `bash verificar_paquete.sh completa`;
- uno detrás de otro, nunca dos a la vez, porque varios usan LibreOffice;
- todos con `python3 -I`.

Todos escriben solo en temporales; el manifiesto sigue intacto después.

## 1. Controles que deben dar su resultado completo

Las rutas parten de `personaje_v2/empresas_v2_correcciones/` salvo las de `contrastes/`.

| Entrega | Orden | Resultado esperado | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.2 | `python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py` | 45 comprobaciones | `contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt` |
| 4.3 | `python3 -I contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py` | 217 de 217 | `contrastes/vidrala_revision_financiera/resultados/revision_salida.txt` |
| 4.3.1 | `python3 -I contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py` | 43 de 43 | `contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt` |
| 4.4 | `python3 -I …/2026-11_Vidrala_ensayo/scripts/comprobar_ensayo.py` | 72 de 72 | `…/2026-11_Vidrala_ensayo/resultados/comprobar_ensayo_salida.txt` |
| 4.5 | `python3 -I …/2026-11_Vidrala_ensayo_4_5/scripts/comprobar_continuacion.py` | 60 de 60 | `…/2026-11_Vidrala_ensayo_4_5/resultados/comprobar_continuacion_salida.txt` |
| 4.6 | `python3 -I …/2026-11_Vidrala_ensayo_4_6/scripts/comprobar_cierre_ensayo.py` | 24 de 24 | `…/2026-11_Vidrala_ensayo_4_6/resultados/comprobar_cierre_ensayo_salida.txt` |
| 4.6.1 | `python3 -I …/2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_vigencia_ensayo.py` | 23 de 23 | `…/2026-11_Vidrala_ensayo_4_6_1/resultados/comprobar_vigencia_ensayo_salida.txt` |
| **4.8** | `python3 -I …/2026-11_Vidrala_ensayo_4_8/scripts/comprobar_entrega_4_8.py` | **36 de 36**, código 0 (unos 45 s) | `resultados/comprobar_entrega_4_8_salida.txt` |
| 4.8 (aparte) | `python3 -I …/2026-11_Vidrala_ensayo_4_8/scripts/comparar_baterias_4_7_1.py` | código 0; las tres baterías del resumen de la 4.7.1 coinciden en todo salvo las huellas (unos 45 s) | `resultados/comparar_baterias_4_7_1_salida.txt` |

Los controles de integración del verificador de la 4.6.1, la 4.7.1 y la 4.8 (13 de 13 cada uno) los reejecuta `comprobar_entrega_4_8.py`.

## 2. Controles que, por diseño, no dan su resultado completo

Los controles de la 4.7 y la 4.7.1 fijan las huellas del código y de la documentación **de su propia versión**. Sobre su ZIP intacto dan 49 de 49 y 44 de 44. En cuanto una entrega posterior cambia esos archivos, los controles que miran sus huellas dejan de cumplir. No es una regresión: es lo que deben hacer.

| Entrega | Orden | Resultado esperado sobre este árbol | Salida de referencia (idéntica) |
|---|---|---|---|
| 4.7 | `python3 -I …/2026-11_Vidrala_ensayo_4_7/scripts/comprobar_entrega_4_7.py` | **46 de 49**, código 1 | `resultados/comprobar_entrega_4_7_en_arbol_4_8.txt`, idéntica byte a byte a la de la 4.7.1 (`…_4_7_1/resultados/comprobar_entrega_4_7_en_arbol_4_7_1.txt`) |
| 4.7.1 | `python3 -I …/2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_entrega_4_7_1.py` | **40 de 44**, código 1 (unos 1,5 min) | `resultados/comprobar_entrega_4_7_1_en_arbol_4_8.txt` |

**4.7: los tres que no cumplen.** Son los mismos tres que ya no cumplían sobre el árbol 4.7.1, y por la misma razón:
- las huellas del código del bloque A;
- la integración de la batería del resumen, que compara una salida que incluye `verificar_paquete.sh`;
- el control de vigencia final.

**4.7.1: los cuatro que no cumplen.** Todos se explican por los archivos que la 4.8 declara cambiados (`ficha.py`, `pipeline.py`, `verificar_paquete.sh`, el Anexo D, `DECISIONES.md`, `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`):
1. **Huellas del código del cierre técnico (§6).** Cambian `ficha.py`, `pipeline.py` y `verificar_paquete.sh`.
2. **Las tres baterías del resumen.** Hecho: la primera línea de cada salida conservada lleva las huellas del código, y en las tres copias cambia al menos la de `verificar_paquete.sh`. `comparar_baterias_4_7_1.py` reutiliza sin modificarlo el ejecutor de la 4.7.1 y comprueba lo que queda:
   - el estado de cada prueba, el principio de las que fallan y la línea final son **iguales** a los conservados: 45/45 con el código actual, 35/45 con el de la 4.7 y 36/45 con el auditado;
   - solo cambian las huellas de archivos declarados.
3. **Material del control de vigencia de la 4.7.1.** Cambian `ficha.py`, `pipeline.py`, `verificar_paquete.sh`, el Anexo D y `DECISIONES.md`.
4. **VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md.** Ahora describen la 4.8.

Los otros 40 controles de la 4.7.1 cumplen sobre este árbol: referencias intactas, reproducción de W-1, el N3, la auditoría conservada y las decisiones sin rellenar.

## 3. Qué haría saltar una alarma

- Cualquier diferencia con la salida de referencia, en cualquiera de las dos tablas.
- Un recuento distinto del esperado.
- Un archivo del manifiesto modificado, ausente o de más después de ejecutarlos.
- En la 4.7.1 o la 4.7, un control que no cumple y que no está en las listas de arriba.
