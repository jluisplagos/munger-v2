# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** incorporación de la revisión n.º 9 (copia sin cambios de a3a1a2b, procedencia y registro). Su respuesta, C20, está en preparación.
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
| C18 = `f12f8ea79ed5c1b444d85163c5ed08d8d07a6243` | Respuesta a la revisión n.º 8: el año del rótulo como no cifra (`token_del_rotulo`), la octava parte de las respuestas, los documentos y las salidas |
| C19 = `06ad1003aa5320445d0c42498c3d0efaec971f06` | Congelado de la revisión n.º 9: solo registra el hash de C18 |
| `105b57b` | Registra el encargo de la pasada 9 |
| El commit que contiene esta versión de este archivo | Copia de la revisión n.º 9 (a3a1a2b, 24/24 blobs), procedencia y registro. No cambia código, datos ni resultados |

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

1. **Responder a la revisión n.º 9** (C20). Plan, según sus correcciones propuestas (`revision/REVISION_INDEPENDIENTE_9.md`, §7):
   - **U1:** que la tokenización devuelva la posición de cada token, sin buscar su texto en la línea (el «0» de una fila se localizaba en el «0» de la fecha del rótulo y `token_del_rotulo` retiraba ocho ceros reales); casos U1a y U2a de `contraejemplos_9`;
   - **U2:** decidir y declarar si los recuentos con fecha toman el ejercicio de su fecha. Si no lo toman, la primera línea del rótulo de la fila cuenta para la condición de las palabras, y la regla no se aplica bajo un encabezado numerado (sumario). Ajustar las frases; casos U3a y U3b;
   - **U3:** contar las columnas en la tabla (el máximo de las filas del bloque o las celdas de la cabecera), o declarar el límite;
   - **U4:** el criterio de la pestaña en `rotulos_sin_rotulo`, el mismo que en `rotulo`;
   - **U5:** (a) con «published», «publié» o «reported» en el rótulo, la edición no puede ser la vigente; (c) el pie de página no es una fila, y un token de una celda con letras no se evalúa como cifra; (b) y (d), declararlos;
   - **U6 (a)–(g):** frases de E9 (R42 de 2023–25 sí interviene: 18 identidades), de la octava parte, del informe §1 (límites), de T14 y de este punto («cinco tablas del WACC», no seis).
   - Pruebas: regresión de las 752 filas, test, scripts de los revisores n.º 1 a 9 sobre C20 y reproducción; congelado C21 y pasada 10.
2. **C18, revisado en la pasada 9.** C20, sin revisar hasta la pasada 10.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Límites del verificador:** regla de grupos (S7 d en los URD 2021, 2022 y 2023), honorarios por firma en PENDIENTE (176 cifras), rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42; los que declara C18 (T1, T2, T5 y T6).
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Leer entera la revisión n.º 9 (§2 a §9) y sus contraejemplos (`revision/resultados_revisor_9/contraejemplos_9.txt` y `sondas_sinteticas_9.txt`).
2. Implementar el plan de §3.1 con un caso de test por clase. Comprobar que ninguna de las 752 filas reales cambia de estado sin causa explicada, y pasar los barridos de los revisores n.º 6 a 9 entre C18 y C20.
3. Novena parte de las respuestas, informe, especificación, estado y registro. Commit C20, push y punto de recuperación; congelar (C21) y encargar la pasada 10.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes séptima y octava de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
