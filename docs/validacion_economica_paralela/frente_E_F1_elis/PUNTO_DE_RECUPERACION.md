# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** respuesta a la revisión n.º 7 (C16). Falta congelarla (C17) y encargar su revisión (pasada 8).
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C14 = `cf55865a22035aa8376d8813cd58d0f2fcdd4846` | Respuesta a la revisión n.º 6. Revisado en la pasada 7 |
| C15 = `c96d544646b2fa5a66c233402a9f31332a643cec` | Congelado de la revisión n.º 7 |
| `f1dd6c5` | Copia de la revisión n.º 7 (d192cab), procedencia y registro |
| `559828e` | Primera parte de C16: verificador (S1–S5, S7 c y e) y test |
| C16 = el commit que contiene esta versión de este archivo | Respuesta completa a la revisión n.º 7 (S1–S7). **No revisado** |

## 2. Estado de las pruebas sobre C16

| Prueba | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py` | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO; salida idéntica byte a byte a la de C14 | `resultados/verificacion_cifras.json` |
| `test_verificar_cifras.py` | 117/117: 23 positivos reales, 23 PENDIENTE esperados y 71 contraejemplos | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas; 419 entradas; referencia de E9 sin cambios | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 24/24 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 530 filas, sin incoherencias | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | 713/713 en unidad y en perímetro | `resultados/sondas_metadatos_C16.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro | `resultados/caja_no_nula.json` |
| Scripts de los revisores n.º 1 a 7 | Ver la séptima parte de las respuestas. Aceptaciones nuevas: 346, todas saldos con la fecha en el rótulo (S1) | `resultados/*_sobre_C16.txt` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

**Qué cubren estas pruebas:** los casos de los revisores, las filas reales y los barridos de los revisores n.º 6 y 7. El del n.º 7 recorre también las líneas sin rótulo.

## 3. Incidencias pendientes

1. **C16 sin revisar** hasta la pasada 8. Incluye las 346 aceptaciones nuevas de la regla de S1 y la decisión de declarar S7 d.
2. **Límites declarados del verificador:** regla de grupos (firma frente a marca; tablas de marcas de un solo ejercicio o sin ejercicios); honorarios por firma en PENDIENTE; dependencia de la rejilla de pdftotext; un bloque de otro perímetro sin señales no se detecta.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **14 filas PENDIENTE** (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Congelar C16: commit C17, que solo registra el hash de C16 en `revision/ESTADO.md`, en la tabla de commits de las respuestas y en el manifiesto. Push.
2. Encargar la pasada 8 sobre C17 a una sesión de revisión nueva, con el modelo y el esfuerzo que el encargo asigna a la revisión independiente, en la rama `auditoria/economica-f1-frente-e-revision` sobre d192cab. Alcance: `git diff f1dd6c5 C16`. Programar una comprobación y registrar la configuración.
3. Al terminar: copiar sus archivos sin cambios, con procedencia, y responder.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes quinta y sexta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
