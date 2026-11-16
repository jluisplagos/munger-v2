# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** conciliación del plan visible con el trabajo realmente hecho. No se ha iniciado ninguna revisión ni se ha repetido ninguna prueba. El último encargo sustantivo, las correcciones V1–V11, terminó en `fd474d3`.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`, en `jluisplagos/munger-v2`. No está fusionada a `main`. Antes de este commit, HEAD local = remoto = `fd474d325ef0983660c6a1851a4e50b3976ab64c`, sin cambios sin publicar.

**F1 sigue abierto.** Elis sigue en `pendiente_de_datos`. **Estado: esperando** a la persona responsable (§4). No hay nada en ejecución ni tareas programadas.

## 1. Plan frente a trabajo real

«Revisado» solo se dice de una revisión hecha por una sesión distinta de la autora, o de la revisión externa aportada por la persona responsable. Las comprobaciones del autor van en «probado». Integrado significa en esta rama: nada está en `main` ni en el producto.

| # | Tarea | Entregado | Revisado | Probado (última ejecución) | Pendiente | Siguiente |
|---|---|---|---|---|---|---|
| 1–6 | Preparación, cambios del frente técnico, conciliación 2021–25, puente del FCF base y f, reinversión e intangibles, contraste | Informe, CSV, verificador y contraste desde C1 `96a69ca`. Últimos cambios: verificador C18 `f12f8ea`, contraste C16 `66d01b8` | Revisión n.º 1 (`47551a2`, sobre C1) y siguientes de lo afectado. La n.º 9 (`a3a1a2b`, sobre C19 `06ad100`) cubrió C18 | Verificador: 752 filas, 738 OK, 14 PENDIENTE, 0 FALLO (código C18; salida igual desde C14). Test: 136/136 y 9/9 (C18). Contraste: 292/0 (salida igual desde C16; repetido en `13f864f` y `593a391`). Caja no nula, con LibreOffice: C4 `d2e585e` | U1–U6 de la n.º 9 sin responder (#26). Datos M1, M2, M6 y N2 (#29) | Persona responsable |
| 10–13, 15–22 | Respuestas a las revisiones 1, 3, 4, 5, 6 y 7 | C3 `eb77dea`, C4 `d2e585e`, C7 `9869def`, C9 `c876449`, C10 `95b37e6`, C12 `4f3f9ba`, C14 `cf55865`, C16 `66d01b8` | Revisiones 3 (`11b999a` y `034301c`), 4 (`a15f706`), 5 (`595d2f6`), 6 (`9711f04`), 7 (`d192cab`) y 8 (`3138a6b`), cada una sobre su congelado. Contraste externo (`5ce263a` y `e57239c`, rama `auditoria/economica-f1`), aportado por la persona responsable | Las de cada commit, en `revision/RESPUESTAS_AUTOR_1.md` | — | — |
| 23 | Respuesta a la revisión n.º 8 | C18 `f12f8ea` | Revisión n.º 9 (`a3a1a2b`, sobre `06ad100`) | 28 pasos de los revisores 1–8 con código 0 (C18) | U1–U6 (#26) | Persona responsable |
| 24 | Respuesta a la revisión de la propuesta (P1–P4) | `13f864f`; copia de la revisión dirigida en `bb28319` | Revisión externa de la propuesta (`1a07188`, sobre `b83803c`). Revisión dirigida (`8fcc7fd`, sobre `13f864f`): P3 resuelto; P1, P2 y P4 en parte | Controles 22 casos; copia 43 controles; contraste 292/0 (en `13f864f`), reproducidos por la revisión dirigida | Sus correcciones: #25 | — |
| 25 | Correcciones V1–V11 | `593a391` (herramientas), `6a48bc4` (documentos), `fd474d3` ([RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md)) | **No revisado** | Controles: 32 casos, 3 guardas y caso fiscal (`fd474d3`). Copia: 55/0, con 14/14 literales y 12/12 pasajes en el PDF (`593a391`). Contraste: 292/0, idéntico (`593a391`) | Revisión externa (#27) | Persona responsable |
| 7 | Informe y especificación | `INFORME_CONCILIACION_F1.md` y `ESPECIFICACION_F1_PROPUESTA.md`; últimos cambios en `6a48bc4` | Hasta `13f864f`, por `8fcc7fd`; los cambios de `6a48bc4`, no | Documentos; sus valores de referencia, en la copia y los controles | Revisión externa (#27). No adoptada (#28). Implementación (#31) | Persona responsable; frente técnico |
| 8 | Revisiones independientes | Revisiones 1, 3–9 y dirigida, copiadas con procedencia en `revision/` | Son las revisiones (sesiones distintas; `REGISTRO_CONFIGURACION.md`) | — | Respuesta a la n.º 9 (#26) | — |
| 9 | Rama publicada | `auditoria/economica-f1-frente-e`, con manifiesto de 374 archivos en `fd474d3` | La revisión dirigida comprobó el de `13f864f` (356/356); el actual, no | `sha256sum -c`: OK (autor) | — | — |
| 14 | Congelados y publicación | C8, C11, C13, C15, C17, C19 y `13f864f` | Cada uno por su revisión | — | V1–V11 no tiene congelado propio (#27) | — |

Las tareas #26–#31 del plan visible están pendientes y no tienen entrega.

## 2. Estado de las pruebas

Sin cambios desde `fd474d3`. Ninguna prueba se ha vuelto a ejecutar en este bloque. Las versiones de código son los commits citados en §1. Las salidas no registran el intérprete; el entorno actual es Python 3.13.18, pdftotext 24.02.0 y openpyxl 3.1.5.

## 3. Clasificación de lo pendiente

- **Terminado en el último encargo, V1–V11:** `593a391`, `6a48bc4` y `fd474d3`.
- **Pendiente de revisión externa:** las correcciones V1–V11 (#27):
  - propuesta, revisión 3;
  - especificación: E2–E5, E8 y E9;
  - informe: §4.2, §6.3, §6.4 y §12;
  - los dos scripts de investigación y sus salidas;
  - las notas en la respuesta anterior;
  - el manifiesto de 374 archivos.
- **Pendiente de datos** (#29): M1, M2, M6 y N2. Con ellos, R, f, el flujo de partida y el ancla de S2C de Elis.
- **Pendiente de decisión explícita** (#28):
  - (1a)–(5b), con (4b) A o B, el alcance de N1 y las vías de (3b);
  - la convención del τ de proyección (E8.1);
  - si se quiere un umbral para V-F1a;
  - si se hacen #26 y #30.
- **Trabajo técnico no realizado:**
  - C20 (#26);
  - cifras [LECTURA] al CSV verificado (#30);
  - implementación en el producto (#31), del frente técnico y tras #28;
  - las 14 filas PENDIENTE del verificador (URD 2022 p.302) siguen así.

## 4. Siguiente paso exacto

Esperar a la persona responsable. No se lanza ninguna revisión ni ronda por iniciativa propia. Hace falta:
1. el resultado de la revisión externa de V1–V11 (#27);
2. las decisiones (1a)–(5b) y las opciones abiertas (#28);
3. indicación sobre #26 (C20) y #30 ([LECTURA] al CSV);
4. para desbloquear Elis, los datos de #29 o una estimación documentada.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos de [RESPUESTA_CORRECCIONES_V1_V11.md](RESPUESTA_CORRECCIONES_V1_V11.md), §1, y los del informe, §13. LibreOffice solo en secuencia.
4. Leer este archivo, [revision/ESTADO.md](revision/ESTADO.md), [PROPUESTA_DECISIONES_F1.md](PROPUESTA_DECISIONES_F1.md) y la respuesta V1–V11.
5. Configuración: la de cada encargo, en [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md). La revisión la hace una sesión distinta de la autora.
