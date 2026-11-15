# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** incorporación de la revisión n.º 5 (copia sin cambios, procedencia y registro). Su respuesta, C12, está en preparación.
**Hora:** 15-nov-2026, hacia las 23:40 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C7 = `9869def325b8820e2ee25618107495a7a7b70229` | Respuesta a la revisión n.º 3 y a su adenda (N1–N10) |
| C8 = `97441770f51761e28c089df7830d3de802bf87e9` | Registra el hash de C7. Congelado de la revisión n.º 4 |
| C9 = `c8764494d9911c59a67a530f13b56616fe86707c` | Segunda presentación de cinco entradas; columnas por país. **No revisado** |
| C10 = `95b37e6da22bd4d5adb55c3f09c729b8d4e409f1` | Respuesta a la revisión n.º 4. **No revisado** |
| C11 = `364129afd45ba2e54a1df4141fd50e97fd55ef6d` | Registra el hash de C10. **Commit congelado de la revisión n.º 5** |
| `0caa7ee` | Registra el encargo de la revisión n.º 5 |
| El commit que contiene esta versión de este archivo | Copia de la revisión n.º 5 (595d2f6), procedencia y registro. No cambia código, datos ni resultados |

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

1. **Responder a la revisión n.º 5** (C12). Plan:
   - **Q1**, columnas «published» de las tablas de reexpresión con edición vigente: reconocer por separado dos columnas del mismo año y marcar «published», «reported» y «publié» como edición anterior;
   - **Q2**, asignación por orden en el balance del URD 2021: contar como columnas distintas dos fechas distintas del mismo año;
   - **Q3**, regresión de C9 por la marca «(a)»: incluir las llamadas con letra entre los calificadores y mantener el FALLO cuando la columna reconocida más próxima es de otro ejercicio;
   - **Q4**, regla del título de C10: buscar el título hasta el principio de la página y en la anterior; exigir que sea una línea propia y en mayúsculas;
   - **Q5**, rótulos de segmento: normalizar «and», «et» y «&», unir los rótulos partidos y añadir la identidad entre páginas del crecimiento publicado frente a las ventas;
   - **Q6**, cinco entradas de solo misma página que mueven la referencia: R41 (resultado antes de impuestos, nota 9), R8 de 2021–22 (línea del EFE y provisiones) y R24 de 2023 (puente de la deuda neta del DEU 2024 p.260). Corregir las tres frases y que la prueba de mutación informe también de esa clase;
   - **Q7**, forma: (a), (c), (d), (e) y (f); (b) ya corregida en 0caa7ee.
2. **C9, C10 y C12 sin revisar** hasta la pasada 6.
3. **Cobertura de la unidad y del perímetro:** cobertura pendiente donde no hay identidad entre páginas.
4. **14 filas PENDIENTE** de URD 2022 p.302; columnas por sociedad PENDIENTE.
5. **Límites de detección por debajo de la cota:** R13 de 2025 y R39 de 2021.
6. **Decisiones económicas [DH]:** F1, PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
7. **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Implementar el plan de §3.1 con un caso de test por clase. Comprobar que ninguna de las 743 filas reales cambia de estado sin causa explicada.
2. Regenerar toda la cadena y pasar los scripts de los revisores, sin cambios, sobre el resultado.
3. Escribir la respuesta (quinta parte de las respuestas), el informe, la especificación y el registro.
4. Commit C12, push y punto de recuperación; congelar (C13) y encargar la revisión de lo afectado por C12 (pasada 6).

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes segunda, tercera y cuarta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
