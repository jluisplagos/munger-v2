# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** segunda parte del código de C18 (respuesta a la revisión n.º 8): el rótulo más corto de T2, que corrige un efecto de la primera parte; el rótulo con viñeta de T5; las comprobaciones directas del test; y el barrido del autor sobre la regla de la fecha del rótulo. Los documentos (octava parte, informe, especificación, estado, registro) y los barridos de los revisores sobre el código final están en curso y **no entran en este commit**.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C16 = `66d01b8fc21b277efdae938170cc64815705962e` | Respuesta a la revisión n.º 7 (S1–S7). Revisado en la pasada 8 |
| C17 = `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` | Congelado de la revisión n.º 8 |
| `7e59a8c` · `63e6090` | Encargo de la pasada 8 · copia de la revisión n.º 8 (3138a6b), procedencia y registro |
| `d3c0f1b` | C18, primera parte: T1–T6 en el verificador, cabecera (T8 c) y casos de test |
| El commit que contiene esta versión de este archivo | C18, segunda parte del código: la que se describe abajo. Sin documentos |

Cambios de esta parte (detalle en el comentario de cada función, con la marca «revisión n.º 8»):

- **T2, rótulo más corto (`rotulo_de_saldo`).** En `d3c0f1b` el rótulo unido podía absorber la cabecera de columna o la línea de unidades de encima, y la condición de las palabras lo rechazaba. Dejaban de reconocerse los saldos de apertura de las cinco tablas de la reserva de coberturas («Cash flow hedges» / «BALANCE AS AT JANUARY 1, 2021») y dos de tablas en miles de euros («(In thousands of euros)» / «As at 12/31/2021»). Ahora se toma el rótulo más corto, desde el de la propia fila hacia arriba, que ya lleva la fórmula del saldo y la fecha. Se admiten también «published», «publié» y «reported». `rotulo_multilinea` se apoya en la nueva `partes_de_rotulo`, sin cambiar su resultado.
- **T5, rótulo con viñeta.** Una línea que empieza por un guion seguido de texto en la misma celda («− Matthieu Lecharny») no es una línea sin rótulo.
- **Test:** caso nuevo de la reserva de coberturas (URD 2022 p.324) y nueve comprobaciones directas de funciones: seis del criterio de encabezado (T6), una del rótulo con viñeta (T5) y dos de la excepción «Total» de la cabecera por países (S4), con líneas sintéticas porque no tiene caso real.
- **`scripts/barrido_fecha_rotulo.py`** (nuevo): todas las líneas de las cinco fuentes en que la regla da un ejercicio y, con `--anterior`, la comparación línea a línea con otra versión. Salida: `resultados/barrido_fecha_rotulo.txt`.

## 2. Estado de las pruebas en este commit

| Prueba | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py` | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO; salida y registro idénticos byte a byte a los de C16 | `resultados/verificacion_cifras.json`, `resultados/verificar_cifras.log` |
| `test_verificar_cifras.py` | 135/135 casos (23 positivos reales, 35 PENDIENTE y 77 contraejemplos) y 9/9 comprobaciones directas. Con el verificador de `d3c0f1b`, 134/135 y 8/9 (fallan el caso de la reserva de coberturas y la comprobación de la viñeta); con el de C16, 119/135 y 4/9 | `resultados/test_verificar_cifras.log` |
| `barrido_fecha_rotulo.py` | La regla da ejercicio en 207 líneas: 191 con la fecha en la propia línea y 16 con la fecha unida de encima, las 16 rótulos de su propio saldo. Frente a C16: 200 líneas con el mismo ejercicio, 7 nuevas (los cinco cierres del estado de cambios en el patrimonio de T3 y dos valores netos del URD 2023) y 500 que C16 reconocía y C18 no: 302 de una sola celda (títulos y continuaciones) y 198 de dos celdas o más, de ellas 166 con un token o ninguno (prosa, títulos, epígrafes) y 32 recuentos o porcentajes con fecha (planes de acciones, número de acciones, autocartera). Ningún saldo en millones de euros | `resultados/barrido_fecha_rotulo.txt` |
| Contraejemplos de la revisión n.º 8 | Los 25 casos, igual que con `d3c0f1b` | `scratchpad`, no versionado; se guardará con C18 |
| `contraste_f1.py`, `test_contraste_residuos.py`, `cobertura_por_mutacion.py`, `tabla_conciliacion.py` | Sin cambios de código ni de entradas desde `d3c0f1b`, donde dieron salidas idénticas a las de C16 | `resultados/` |
| `sondas_metadatos.py` | No ejecutado; se ejecutará sobre C18 | `resultados/sondas_metadatos_C16.json` (anterior) |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, que no cambia | `resultados/caja_no_nula.json` |
| Scripts de los revisores n.º 1 a 8 | Pasada parcial sobre el código de esta mañana, descartada por el cambio de T2: se repiten enteros sobre el código final | — |
| Manifiesto | Calculado sobre los archivos de este commit; `sha256sum -c MANIFIESTO_SHA256.txt`: OK en un checkout limpio | — |

## 3. Incidencias pendientes

1. **Terminar C18:**
   - pasar en secuencia los scripts de los revisores n.º 1 a 8 sobre el código final (anterior: C8 para los n.º 1 a 5 y C17 para los n.º 6 a 8) y guardar sus salidas en `resultados/*_sobre_C18.txt`;
   - documentos: octava parte de las respuestas (con las aceptaciones que retira C18: en la pasada parcial del revisor n.º 6, 336 de las 346 aceptaciones de C16 volvían a PENDIENTE y ninguna candidata pasaba a OK; se recontará), precisiones de C18 en las partes sexta y séptima, informe (§0, §1, §12), especificación (E9 y T14), README, `revision/ESTADO.md` y `REGISTRO_CONFIGURACION.md`. Están escritos en el árbol de trabajo y se revisarán con las cifras finales;
   - `sondas_metadatos_C18.json`; `reproduccion_7` y `reproduccion_8` sobre el árbol final, después del manifiesto (T8 e);
   - límites que se declaran: en T2, el coste en los recuentos con fecha (vuelven a la regla de las columnas, como en C14) y una fila cuyo rótulo sea solo la fórmula del saldo bajo una línea de fecha de la fila anterior; en T5, la sangría exacta de los rótulos; en T6, los títulos en minúsculas partidos tras una coma y las entradas de sumario.
2. **C18 sin revisar** hasta la pasada 9.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Límites del verificador:** regla de grupos, honorarios por firma en PENDIENTE, rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Lanzar en secuencia los scripts de los revisores n.º 1 a 8 sobre el árbol de trabajo, con el registro de control aparte de las salidas.
2. Comparar cada salida con la de C16, completar la octava parte con las cifras finales y revisar los documentos.
3. Sondas, manifiesto, `reproduccion_7` y `reproduccion_8`, manifiesto otra vez. Commit C18, push y punto de recuperación; congelar (C19) y encargar la pasada 9 (Fable 5.2, esfuerzo máximo, sesión nueva, rama `auditoria/economica-f1-frente-e-revision` sobre 3138a6b).

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md`, la revisión n.º 8 (`revision/REVISION_INDEPENDIENTE_8.md`, §7) y las partes sexta y séptima de `revision/RESPUESTAS_AUTOR_1.md` (y la octava cuando exista).
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
