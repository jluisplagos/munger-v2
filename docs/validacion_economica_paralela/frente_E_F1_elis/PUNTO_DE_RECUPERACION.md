# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** correcciones V1–V11 de la revisión dirigida a P1–P4 (`8fcc7fd`), aplicadas por encargo acotado a la propuesta, la especificación, el informe y las herramientas de investigación. **No se adopta ninguna decisión (1a)–(5b) ni se implementa nada en el producto o los libros oficiales.**
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`. Nada se ha fusionado a `main`.

**F1 sigue abierto.** Elis sigue en `pendiente_de_datos`. Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| `13f864f` | Congelado de la respuesta a la revisión de la propuesta (P1–P4). Lo revisó `8fcc7fd` |
| `bb28319` | Incorporación de esa revisión (16/16 blobs), sin aplicar sus correcciones. Punto de partida de este encargo, igual al remoto |
| `593a391` | **Bloque A**, herramientas de investigación: `controles_sinteticos_f1.py` (V2, V9) y `copia_investigacion_f1.py` (V3–V6), con sus salidas |
| `6a48bc4` | **Bloque B**, documentos: propuesta revisión 3 (V1–V11), especificación (E2–E5, E8, E9), informe (§4.2, §6.3, §6.4, §12) y notas de corrección en la respuesta anterior |
| El commit que contiene esta versión de este archivo | **Bloque C:** [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md), numerada V1–V11; README, `revision/ESTADO.md`, `REGISTRO_CONFIGURACION.md`, este punto y el manifiesto. El caso V2a de los controles, con la descripción ajustada a su resultado |

## 2. Estado de las pruebas

| Prueba | Resultado | Salida |
|---|---|---|
| `controles_sinteticos_f1.py` | Código 0. 32 casos con su resultado esperado: 14 coherentes y 18 incoherencias ilustradas; 23 con crecimiento; 8 con el ancla calculada con E4. 9/9 de la revisión externa. 3 guardas V-F1c correctas. Caso fiscal de N1 correcto. Motor = `motor_a` en 4 juegos | `resultados/controles_sinteticos_f1.{json,log}` |
| `copia_investigacion_f1.py` (con `--raiz`) | Código 0. 55 controles, 0 fallidos. 14/14 literales [LECTURA] y 12/12 pasajes en su página del PDF; huellas de los PDF correctas | `resultados/copia_investigacion_f1.{json,md,log}` |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas; salidas idénticas | `resultados/contraste_f1.{json,md}` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |
| Verificador, sus tests, mutación, sondas de metadatos, barrido, scripts de los revisores n.º 1 a 9 y de la revisión dirigida | Sin cambios de código ni de entradas; no se han vuelto a ejecutar. Último estado: el de C18 y el de `8fcc7fd` | — |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4 | — |

## 3. Incidencias pendientes

0. **Revisión externa de las correcciones V1–V11**, solo en lo afectado. No la encarga esta sesión.
1. **Decisiones F1 de la persona responsable:** (1a)–(5b), con el texto exacto de la tabla única de la propuesta, revisión 3. Quedan opciones abiertas:
   - (4b): opción A, pendiente hasta M6 (recomendada), u opción B, hipótesis declarada;
   - (5a): alcance de N1 a 2021–22;
   - (3b): vías para obtener el dato.
2. **Carencias que bloquean:**
   - M1: reparto del capex y del plan climático;
   - M2: bajas de clientes;
   - M6: finalidad de las compras pequeñas y crecimiento orgánico sin ellas;
   - N2: fiscalidad, caja y reposición de las bajas de 2025;
   - perímetro de las palancas S2C y ROIC de Elis.

   Preguntas preparadas, no enviadas.
3. **Política fuera de F1:** convención del τ de proyección (E8.1), que mueve N1 entre −11,6 y −9,1.
4. **Procedimiento:** la actualización del earnout (12,4 / 5,6 / 0,7) y los ajustes de 2021–22 están publicados y comprobados en el PDF, pero no en el CSV verificado.
5. **Respuesta C20 a la revisión n.º 9 del verificador**, en espera (plan en `b83803c`, `PUNTO_DE_RECUPERACION.md`, §3, punto 1).
6. **Decisiones económicas [DH]** y **sin aptitud para dinero real.** Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

Esperar a la persona responsable. No se lanza ninguna revisión ni ronda por iniciativa propia.
1. La revisión externa de lo afectado por V1–V11.
2. Las decisiones (1a)–(5b). Lo aprobado se registrará con fecha, persona y motivo, y se aplicará con las pruebas T8, T15 y T16 y una revisión independiente.
3. Si lo indica, el paso al CSV verificado de las cifras [LECTURA] o la respuesta C20.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos de [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md), §1, y los del informe, §13. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md`, la propuesta (revisión 3) y la respuesta V1–V11.
5. Configuración acordada: la de cada encargo, registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora.
