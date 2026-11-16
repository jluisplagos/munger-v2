# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** respuesta a la revisión n.º 8 (C18), completa: verificador, test, barrido del autor, documentos y salidas de los scripts de los revisores n.º 1 a 8 sobre C18. Lo afectado por C18 está **sin revisar** hasta la pasada 9.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C16 = `66d01b8fc21b277efdae938170cc64815705962e` | Respuesta a la revisión n.º 7 (S1–S7). Revisado en la pasada 8 |
| C17 = `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` | Congelado de la revisión n.º 8 |
| `7e59a8c` · `63e6090` | Encargo de la pasada 8 · copia de la revisión n.º 8 (3138a6b), procedencia y registro |
| `d3c0f1b` · `485de8d` | C18, primera y segunda parte del código |
| C18 = el commit que contiene esta versión de este archivo | Respuesta a la revisión n.º 8: el año del rótulo como no cifra (`token_del_rotulo`), la octava parte de las respuestas, los documentos y las salidas |

Qué cambia C18, en breve (detalle en la octava parte de `revision/RESPUESTAS_AUTOR_1.md`):
- **T1:** con la fecha del saldo en el rótulo y varias columnas de datos, «columna» queda PENDIENTE. De las 346 aceptaciones de C16 quedan diez (las tablas de deterioro de clientes, de una sola columna).
- **T2:** la regla solo vale en filas de saldo, con el rótulo más corto que lleva la fórmula y la fecha; los tokens del rótulo, la prosa, los títulos y los recuentos con fecha no la toman. Un año suelto dentro del rótulo de texto, o el día de su fecha, no es una cifra.
- **T3:** se reconocen los 20 saldos de apertura y cierre de los diez estados de cambios en el patrimonio.
- **T4:** las seis tablas del WACC por país quedan sin ningún perímetro OK.
- **T5:** líneas contiguas de 45 caracteres o menos y en el margen; sin pestaña ni viñeta.
- **T6:** «Note N to the…» no es encabezado; los títulos en mayúsculas sí, con comillas o con coma final continuada.
- **T7 y T8:** frases y recuentos corregidos en su sitio; argumento retirado fuera de T14; cabecera del verificador; `reproduccion_7` regenerado al final.

## 2. Estado de las pruebas en C18

| Prueba | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py` | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO; salida, registro y páginas exportadas idénticos byte a byte a los de C16 | `resultados/verificacion_cifras.json`, `resultados/verificar_cifras.log` |
| `test_verificar_cifras.py` | 136/136 casos (23 positivos reales, 36 PENDIENTE y 77 contraejemplos) y 9/9 comprobaciones directas. Con el verificador de C16, 119/136 y 4/9; con el de `d3c0f1b`, 134/136 y 8/9 | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas; 419 entradas; salidas idénticas byte a byte a las de C16; referencia de E9 sin cambios | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 24/24; registro idéntico | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 530 filas, sin incoherencias; salida idéntica | `resultados/cobertura_por_mutacion.txt` |
| `tabla_conciliacion.py` | Salida idéntica | `resultados/tabla_conciliacion.md` |
| `sondas_metadatos.py` | 713/713 en unidad y en perímetro; igual que en C16 salvo la etiqueta | `resultados/sondas_metadatos_C18.json` |
| `barrido_fecha_rotulo.py` | 207 líneas con ejercicio por la fecha del rótulo; frente a C16, 200 iguales, 7 nuevas y 500 fuera, ninguna un saldo en millones de euros | `resultados/barrido_fecha_rotulo.txt` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, que no cambia | `resultados/caja_no_nula.json` |
| Scripts de los revisores n.º 1 a 8 | Los 28 pasos, con código 0. Resultados en la octava parte de las respuestas («Resultados sobre C18»). En el barrido del revisor n.º 6, ninguna candidata pasa a OK y 336 pasan de OK a PENDIENTE; en el del n.º 8, ninguna pasa a OK y 414 pasan de OK a PENDIENTE (331 cifras de saldos, por T1, y 83 tokens que no son cifras) | `resultados/*_sobre_C18.txt` |
| `reproduccion_7.py` y `reproduccion_8.py` | Sobre el árbol final, con el manifiesto ya regenerado: idénticos | `resultados/revisor7_reproduccion_7_sobre_C18.txt`, `resultados/revisor8_reproduccion_8_sobre_C18.txt` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **Revisión independiente de lo afectado por C18** (pasada 9): por encargar sobre el congelado C19, con el alcance `git diff 63e6090 C18`.
2. **Límites que C18 declara:**
   - T2: los recuentos con fecha vuelven a la regla de las columnas, como en C14 (coste); una fila cuyo rótulo sea solo la fórmula del saldo, sin fecha propia, bajo una línea de fecha de la fila anterior que no empieza en minúscula, tomaría esa fecha (no encontrado);
   - T1: con varias columnas de datos, los saldos con la fecha en el rótulo quedan PENDIENTE de columna;
   - T5: el margen izquierdo, no la sangría exacta de los rótulos;
   - T6: los títulos en minúsculas partidos tras una coma no cuentan como encabezado, y las entradas de sumario sí.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Límites del verificador:** regla de grupos (S7 d en los URD 2021, 2022 y 2023), honorarios por firma en PENDIENTE (176 cifras), rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Congelar C19: registrar el hash de C18 en `revision/ESTADO.md` y en la línea de C18 de las respuestas, regenerar el manifiesto, commit y push.
2. Encargar la pasada 9 a una sesión nueva (Fable 5.2, esfuerzo máximo), sobre C19, con salida en la rama `auditoria/economica-f1-frente-e-revision` sobre 3138a6b; programar una comprobación y registrar el encargo en `revision/ESTADO.md`, `REGISTRO_CONFIGURACION.md` y este archivo.
3. Al recibir la revisión: copiarla sin cambios con su procedencia, comprobar los blobs y responder en C20.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes séptima y octava de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
