# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** C12, respuesta a la revisión n.º 5 (Q1–Q7).
**Hora:** 16-nov-2026, hacia las 00:15 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C9 = `c8764494d9911c59a67a530f13b56616fe86707c` | Segunda presentación de cinco entradas; columnas por país. Revisado en la pasada 5 |
| C10 = `95b37e6da22bd4d5adb55c3f09c729b8d4e409f1` | Respuesta a la revisión n.º 4. Revisado en la pasada 5 |
| C11 = `364129afd45ba2e54a1df4141fd50e97fd55ef6d` | Congelado de la revisión n.º 5 |
| `202f566` | Copia de la revisión n.º 5 (595d2f6), procedencia y registro |
| C12, el commit que contiene esta versión de este archivo | Respuesta a la revisión n.º 5. **No revisado** |

## 2. Estado de las pruebas sobre C12

| Prueba | Resultado | Salida |
|---|---|---|
| `especificacion_cifras.py` (regenera el CSV desde los PDF) | CSV idéntico byte a byte (SHA-256 `576b423c…`) | Comparación con `cmp` |
| `verificar_cifras.py` | 750 filas: 736 OK, 14 PENDIENTE, 0 FALLO; las 743 anteriores no cambian de estado | `resultados/verificacion_cifras.json`, `verificar_cifras.log` |
| `test_verificar_cifras.py` | 89/89: 20 positivos reales, 10 PENDIENTE esperados y 59 contraejemplos | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 290 comprobaciones, 0 fallidas (136 libro, 125 fuente con 124 residuos, 29 algebraicas); 417 entradas. Código 0 | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 22/22 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 528 filas, sin incoherencias. Ninguna entrada que mueva la referencia queda sin identidad entre páginas | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | 711/711 en unidad y en perímetro | `resultados/sondas_metadatos_C12.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, cuya huella no ha cambiado | `resultados/caja_no_nula.json` |
| Scripts de los revisores n.º 1, 3 y 4 | Igual que sobre C10, salvo recuentos | `resultados/*_sobre_C12.txt` |
| Scripts del revisor n.º 5 (`contraejemplos_5`, `clases_5`, `barrido_tablas`, `cobertura_propia`) | Q1–Q6 corregidas en sus casos; cobertura propia idéntica a la declarada | `resultados/revisor5_*_sobre_C12.txt` |
| Valores de referencia de E9 | Sin cambios (C53 de A1 2,445331695332; de A2 1,612524303305) | `resultados/contraste_f1.json` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **C12 sin revisar.** Hay que congelar un commit (C13) y encargar la revisión de lo que afecta (pasada 6).
2. **Cobertura de la unidad y del perímetro:**
   - 8 páginas (24 entradas) sin identidad entre páginas;
   - 140 entradas con solo identidad de su página;
   - 31 sin segunda línea y 2 solo con la Historia.

   Ninguna mueve la referencia.
3. **Reglas heurísticas.** La asignación de columnas y las señales de unidad y perímetro detectan casos conocidos; no acreditan.
4. **14 filas PENDIENTE** de URD 2022 p.302; columnas por sociedad PENDIENTE.
5. **Límites de detección por debajo de la cota:** R13 de 2025, R39 de 2021 y R42 frente a las ventas.
6. **Decisiones económicas [DH]:** F1, PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
7. **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. C13: solo registra el hash de C12 en `revision/ESTADO.md` y en la fila de C12 de las respuestas, más el manifiesto. Es el congelado de la pasada 6.
2. Encargar la pasada 6 a una sesión de revisión nueva, con contexto propio. Alcance: `git diff 364129a C13`, es decir, las correcciones de Q1–Q7 y lo que afectan.
3. Programar una comprobación. Cuando el informe esté publicado:
   1. copiarlo sin cambios, con su procedencia (operación mecánica, con comprobación de los blobs);
   2. registrar la configuración y las horas;
   3. responder a cada objeción con commit y prueba;
   4. guardar un punto de recuperación.
4. Si la sesión de revisión no responde o llega a un límite de uso: no sustituirla por una revisión del autor; registrarlo y avisar.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes segunda, tercera y cuarta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
