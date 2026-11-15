# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** C10, respuesta a la revisión n.º 4 (P1–P5). Antes, C9: segunda presentación de cinco entradas del ancla de S2C y corrección de las columnas por país.
**Hora:** 15-nov-2026, hacia las 22:45 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C7 = `9869def325b8820e2ee25618107495a7a7b70229` | Respuesta a la revisión n.º 3 y a su adenda (N1–N10) |
| C8 = `97441770f51761e28c089df7830d3de802bf87e9` | Registra el hash de C7. Congelado de la revisión n.º 4 |
| C9 = `c8764494d9911c59a67a530f13b56616fe86707c` | Segunda presentación de cinco entradas; columnas por país. **No revisado** |
| C10, el commit que contiene esta versión de este archivo | Respuesta a la revisión n.º 4. **No revisado** |

La revisión n.º 4 (a15f706, 22:04 UTC) está copiada sin cambios en `revision/`, con su procedencia, y respondida en la cuarta parte de `revision/RESPUESTAS_AUTOR_1.md`.

## 2. Estado de las pruebas sobre C10

| Prueba | Resultado | Salida |
|---|---|---|
| `especificacion_cifras.py` (regenera el CSV desde los PDF) | CSV idéntico byte a byte (SHA-256 `ebf7edf3…`) | Comparación con `cmp` |
| `verificar_cifras.py` | 743 filas: 729 OK, 14 PENDIENTE, 0 FALLO. Código 2 por las pendientes | `resultados/verificacion_cifras.json`, `verificar_cifras.log` |
| `test_verificar_cifras.py` | 71/71: 15 positivos reales, 5 PENDIENTE esperados y 51 contraejemplos | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 280 comprobaciones, 0 fallidas (136 libro, 115 fuente con 114 residuos, 29 algebraicas); 409 entradas, ninguna pendiente. Código 0 | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 18/18 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 521 filas: 0 diferencias con `cobertura_entradas`; ninguna entrada sin detectar, solo con la Historia o de una página sin identidad entre páginas cambia la referencia. Código 0 | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | 704/704 en unidad y en perímetro | `resultados/sondas_metadatos_C10.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, cuya huella no ha cambiado; sus 18 comprobaciones pasan en el contraste | `resultados/caja_no_nula.json` |
| Scripts de los revisores, sin cambios | Revisiones n.º 1 y n.º 3: igual que sobre C9. Revisión n.º 4: A1, A2 y B1 en PENDIENTE; sus controles, en FALLO | `resultados/*_sobre_C10.txt` |
| Valores de referencia de E9 | Sin cambios (C53 de A1 2,445331695332; de A2 1,612524303305) | `resultados/contraste_f1.json` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **C9 y C10 sin revisar.** Hay que congelar un commit y encargar la revisión independiente de lo que afectan (pasada 5).
2. **Cobertura de la unidad y del perímetro.** Es cobertura pendiente, no acreditada:
   - 13 páginas (41 entradas) sin ninguna identidad entre páginas;
   - 151 entradas con solo identidad de su página;
   - 31 sin segunda línea y 4 solo con la Historia del libro.

   Ninguna de ellas cambia la referencia de la especificación.
3. **Las reglas de unidad y de perímetro son listas y criterios** que detectan señales conocidas. Una cifra de otro perímetro o de otra unidad sin esas señales no se detectaría.
4. **14 filas PENDIENTE** de URD 2022 p.302, y columnas por sociedad PENDIENTE.
5. **Límites de detección por debajo de la cota:** R13 de 2025 y R39 de 2021.
6. **Decisiones económicas [DH]:** F1, política de la PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
7. **Fuera de este frente:** implementación, regeneración de expedientes, réplica y auditoría final.
8. **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Commit C11: solo registra el hash de C10 en `revision/ESTADO.md` y en la fila de C10 de `revision/RESPUESTAS_AUTOR_1.md`, más el manifiesto. Es el congelado de la pasada 5.
2. Encargar la pasada 5 a la sesión de revisión, en un contexto separado del autor, sobre C11. Alcance: `git diff 97441770 C11`, es decir, C9 y C10.
3. Programar una comprobación y, cuando el informe esté publicado:
   1. copiarlo sin cambios, con su procedencia;
   2. registrar la configuración y las horas;
   3. responder a cada objeción con commit y prueba;
   4. guardar un nuevo punto de recuperación.
4. Si la sesión de revisión no responde o llega a un límite de uso: no sustituirla por una revisión del autor; registrarlo y pedir intervención manual.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes segunda, tercera y cuarta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
