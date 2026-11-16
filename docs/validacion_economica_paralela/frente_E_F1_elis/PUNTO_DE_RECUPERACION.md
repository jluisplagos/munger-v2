# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** primera parte de la respuesta a la revisión n.º 8 (C18): correcciones T1 a T6 del verificador y sus casos de test. El resto de C18 (T7, T8, documentos y barridos de los revisores) está en preparación.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C16 = `66d01b8fc21b277efdae938170cc64815705962e` | Respuesta a la revisión n.º 7 (S1–S7). Revisado en la pasada 8 |
| C17 = `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` | Congelado de la revisión n.º 8 |
| `7e59a8c` · `63e6090` | Encargo de la pasada 8 · copia de la revisión n.º 8 (3138a6b), procedencia y registro |
| El commit que contiene esta versión de este archivo | C18, primera parte: `verificar_cifras.py` (T1–T6 y cabecera, T8 c), `test_verificar_cifras.py` y su salida |

Cambios del verificador (detalle en el comentario de cada función, con la marca «revisión n.º 8»):

- **T1:** en el modo `dos_columnas`, si el ejercicio sale de la fecha del rótulo y la fila tiene más de una columna de datos a la derecha del rótulo, «columna» queda PENDIENTE (en ese modo ningún concepto tiene columna esperada: la lista cerrada de modos lleva a otros modos los que la tienen). Con una sola columna de datos, NO_APLICA.
- **T2:** la regla de la fecha del rótulo solo vale para filas de saldo: rótulo en la primera celda de una línea con más celdas, token a su derecha y rótulo que solo diga la fórmula del saldo y la fecha («balance», «solde», «as at», «au», «net carrying amount», con «restated», «retraité» o una llamada). No se une una línea en minúscula que está justo debajo de una fila de datos (continúa el rótulo de esa fila).
- **T3:** el rótulo del saldo une también las líneas de encima cuyas únicas cifras son el día o el año («SOLDE AU 31» / «DÉCEMBRE 2024»; «BALANCE AS AT» / «DECEMBER 31, 2021» / «(RESTATED)»). `rotulo_multilinea` lleva para ello el parámetro `fecha`.
- **T4:** la búsqueda de la cabecera por países no se corta en la primera línea del rótulo de una fila (una sola celda con la sangría de la fila de datos que tiene debajo); las líneas de unidades siguen cortándola.
- **T5:** las líneas contiguas que dan rótulo a una línea de cifras sin rótulo tienen como mucho 45 caracteres y están en el margen izquierdo (12 caracteres de sangría o menos; no se mide la sangría exacta de los rótulos de cada tabla); una línea que empieza por la pestaña del capítulo no es una línea sin rótulo.
- **T6:** un encabezado numerado no es «Note N to the…» (ni «of the», «à l», «au», «aux»); en mayúsculas admite comillas y la coma final si la línea de debajo continúa el título, también en mayúsculas. Los títulos en minúsculas partidos tras una coma quedan fuera (límite).

## 2. Estado de las pruebas en este commit

| Prueba | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py` | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO; salida, registro y páginas exportadas idénticos byte a byte a los de C16 | `resultados/verificacion_cifras.json`, `resultados/verificar_cifras.log` |
| `test_verificar_cifras.py` | 134/134 casos y 6/6 comprobaciones directas del criterio de encabezado (T6). Sobre el verificador de C16, 119/134 y 2/6: fallan los 15 casos que prueban las correcciones (13 nuevos y A1 y A10, que pasan de OK a PENDIENTE por T1) | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas; 419 entradas; salidas idénticas byte a byte | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 24/24; registro idéntico | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 530 filas, sin incoherencias; salida idéntica | `resultados/cobertura_por_mutacion.txt` |
| `tabla_conciliacion.py` | Salida idéntica | `resultados/tabla_conciliacion.md` |
| `sondas_metadatos.py` | No ejecutado en este commit; se ejecutará sobre C18 | `resultados/sondas_metadatos_C16.json` (anterior) |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, que no cambia | `resultados/caja_no_nula.json` |
| Contraejemplos de la revisión n.º 8 (`contraejemplos_8.py`, C16 frente al árbol de trabajo) | Los 25 casos dan lo esperado: T1a, T1d y T1e con «columna» PENDIENTE; T2a–T2e con el ejercicio PENDIENTE; T3a–T3f con el ejercicio OK por la fecha y «columna» PENDIENTE (T1); T4b sin la fecha de la fila anterior; T5a y T5b con el perímetro PENDIENTE; T6a sin FALLO de perímetro; T6b con FALLO; controles sin cambio | `scratchpad`, no versionado; se guardará con C18 |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **Terminar C18:**
   - pasar los scripts de los revisores n.º 1 a 8 sobre C18 (anterior: C17) y guardar sus salidas en `resultados/*_sobre_C18.txt`; en particular, los barridos `clases_8`, `barrido_8`, `lectura_saldos_8` y `consultas_8`, para cuantificar las aceptaciones que se retiran (T1, T2) y las que se añaden (T3);
   - **T7 a–g** y **T8 a, d, e** (T8 b y f se corrigieron al incorporar la revisión; T8 c, la cabecera del verificador, va en este commit): frases y recuentos de la séptima parte, del informe (§0, §1, §12), de E9 y T14 y de este punto; quitar el argumento retirado de T14 y de la sexta parte (R2); regenerar `reproduccion_7` sobre el árbol final (manifiesto, script, manifiesto);
   - octava parte de `revision/RESPUESTAS_AUTOR_1.md`, con los límites que quedan: títulos en minúsculas partidos tras una coma (T6), entradas de sumario tomadas por encabezado (T6), saldo cuyo rótulo es solo «Balance» sin fecha propia (T2 c, no encontrado);
   - informe, especificación (T14: los positivos A1 y A10 pasan a PENDIENTE de columna), `README.md`, `revision/ESTADO.md`, `REGISTRO_CONFIGURACION.md`, `sondas_metadatos_C18.json` y manifiesto.
2. **C18 sin revisar** hasta la pasada 9.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Límites del verificador:** regla de grupos, honorarios por firma en PENDIENTE, rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Crear un worktree de C17 (`863ddde`) como versión «anterior» y pasar, en secuencia, los scripts de los revisores n.º 1 a 8 sobre el árbol de trabajo, con el registro de control aparte de las salidas.
2. Comparar cada salida con la de C16 y explicar cada diferencia en la octava parte de las respuestas.
3. Escribir la octava parte, corregir los documentos (T7, T8), ejecutar las sondas, regenerar `reproduccion_7` y el manifiesto. Commit C18, push y punto de recuperación; congelar (C19) y encargar la pasada 9 (Fable 5.2, esfuerzo máximo, sesión nueva, rama `auditoria/economica-f1-frente-e-revision`).

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md`, la revisión n.º 8 (`revision/REVISION_INDEPENDIENTE_8.md`, §7) y las partes sexta y séptima de `revision/RESPUESTAS_AUTOR_1.md` (y la octava cuando exista).
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
