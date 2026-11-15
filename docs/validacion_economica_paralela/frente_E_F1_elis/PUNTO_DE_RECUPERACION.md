# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** C9, cambios del autor tras el congelado C8:
- segunda presentación de cinco entradas del ancla de S2C;
- corrección de un hueco del verificador en las tablas con columnas por país.

**Hora:** 15-nov-2026, hacia las 22:20 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C7 = `9869def325b8820e2ee25618107495a7a7b70229` | Respuesta a la revisión n.º 3 y a su adenda (N1–N10) |
| C8 = `97441770f51761e28c089df7830d3de802bf87e9` | Registra el hash de C7. Commit congelado de la revisión n.º 4 |
| `dcc2637` | Primer punto de recuperación |
| C9, el commit que contiene esta versión de este archivo | Segunda presentación de cinco entradas y corrección del verificador. **No revisado** |

La revisión n.º 4 se publicó a las 22:04 UTC en `auditoria/economica-f1-frente-e-revision` (commit a15f706, según los metadatos de la sesión de revisión). **Aún no se ha leído ni incorporado.** El hueco corregido en C9 se encontró sin haber leído ese informe; el orden no lo acredita git (revision/RESPUESTAS_AUTOR_1.md, tercera parte).

## 2. Estado de las pruebas sobre C9

| Prueba | Resultado | Salida |
|---|---|---|
| `especificacion_cifras.py` (regenera el CSV desde los PDF) | CSV idéntico byte a byte (SHA-256 `ebf7edf3…`) | Comparación con `cmp` |
| `verificar_cifras.py` | 743 filas: 729 OK, 14 PENDIENTE, 0 FALLO. Código 2 por las pendientes | `resultados/verificacion_cifras.json`, `verificar_cifras.log` |
| `test_verificar_cifras.py` | 67/67 | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 280 comprobaciones, 0 fallidas: 136 contra el libro, 115 de fuente (114 residuos) y 29 algebraicas. 409 entradas, ninguna pendiente. Código 0 | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 18/18 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 521 filas: 0 diferencias con `cobertura_entradas`. Código 0 | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | 704/704 en unidad y en perímetro | `resultados/sondas_metadatos_C9.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4. Depende solo del libro, cuya huella no ha cambiado; sus 18 comprobaciones pasan en el contraste | `resultados/caja_no_nula.json` |
| Scripts del revisor, sin cambios | Mismos resultados que sobre C7, salvo los recuentos de filas | `resultados/*_sobre_C9.txt` |
| Valores de referencia de E9 | Sin cambios (C53 de A1 2,445331695332; de A2 1,612524303305) | `resultados/contraste_f1.json` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **Revisión n.º 4:** publicada; hay que copiarla, incorporarla y responder a sus objeciones.
2. **C9 sin revisar:** se revisará con lo afectado por la respuesta a la n.º 4.
3. **Cobertura:** 31 entradas sin segunda línea y 4 solo con la Historia del libro; ninguna mueve la referencia.
4. **14 filas PENDIENTE** de URD 2022 p.302.
5. **Columnas por sociedad** en tablas de adquisiciones: PENDIENTE en ejercicio, no FALLO en perímetro.
6. **Límites de detección declarados:** errores por debajo de la cota, como ±0,1 en R13 de 2025 o la cifra publicada de las adquisiciones de 2021 (86,9) frente a la reexpresada (86,8) en R39.
7. **Decisiones económicas [DH]:** F1, política de la PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
8. **Fuera de este frente:** implementación, regeneración de expedientes, réplica y auditoría final.
9. **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Leer el informe de la revisión n.º 4 (a15f706) y consultar los metadatos de su sesión.
2. Copiar sin cambios, en las mismas rutas, `REVISION_INDEPENDIENTE_4.md`, `scripts_revisor_4/` y `resultados_revisor_4/`, con el blob y el SHA-256 de cada archivo en `revision/PROCEDENCIA_REVISOR.md`.
3. Registrar su configuración en `REGISTRO_CONFIGURACION.md` y las horas en `revision/ESTADO.md`.
4. Responder a cada objeción con su commit y su prueba. Comprobar en particular si alguna coincide con el hueco corregido en C9.
5. Congelar un commit y encargar una revisión independiente de lo afectado por C9 y por esa respuesta (pasada 5).
6. Manifiesto, commit, push y nuevo punto de recuperación.
7. Si la sesión de revisión no responde o llega a un límite de uso: no sustituirla por una revisión del autor; registrarlo y pedir intervención manual.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes segunda y tercera de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
