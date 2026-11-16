# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** incorporación de la revisión n.º 6 (copia sin cambios, procedencia y registro). Su respuesta, C14, está en preparación.
**Hora:** 16-nov-2026, hacia las 01:50 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C9 = `c8764494d9911c59a67a530f13b56616fe86707c` | Segunda presentación de cinco entradas; columnas por país. Revisado en la pasada 5 |
| C10 = `95b37e6da22bd4d5adb55c3f09c729b8d4e409f1` | Respuesta a la revisión n.º 4. Revisado en la pasada 5 |
| C11 = `364129afd45ba2e54a1df4141fd50e97fd55ef6d` | Congelado de la revisión n.º 5 |
| `202f566` | Copia de la revisión n.º 5 (595d2f6), procedencia y registro |
| C12 = `4f3f9ba9c8240143269368c41787736b3867e97b` | Respuesta a la revisión n.º 5. **No revisado** |
| C13 = `1b80b5d5348e6e39dd1d632cafbbbf4e5dd3685a` | Registra el hash de C12. **Commit congelado de la revisión n.º 6** |
| `e88699a` | Registra el encargo de la revisión n.º 6 |
| El commit que contiene esta versión de este archivo | Copia de la revisión n.º 6 (9711f04), procedencia y registro. No cambia código, datos ni resultados |

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

1. **Responder a la revisión n.º 6** (C14). Plan:
   - **R1:** en la asignación por orden, comprobar la alineación de cada número con su cabecera y aplicar la regla de cabecera ajena; las filas «of which», «dont», «excluding», «hors» con un país o una jurisdicción no son del grupo;
   - **R2:** las líneas con numeración de nota o apartado («NOTE 13 …», «5.4 …») son títulos y cortan la búsqueda;
   - **R3:** el FALLO por otra columna de ejercicio solo si está alineada con la cifra (a 3 caracteres o menos);
   - **R4:** conservar el criterio de C10, un título de tabla corto que nombra un país; tres países o más en la cabecera sin columna reconocida, PENDIENTE;
   - **R5:** normalizar «CGU»/«UGT» también al comparar con los países;
   - **R6:** la clase entre páginas es por pertenencia; umbrales de R42 por año; identidad lineal de las ventas de 2021–22 con la información por segmentos (URD 2022 p.279, URD 2023 p.296);
   - **R7 y R8:** frases y motivos.
2. **C12 y C14 sin revisar** hasta la pasada 7.
3. **Cobertura de la unidad y del perímetro**, heurísticas del verificador, 14 filas PENDIENTE y límites de detección: como en el punto anterior.
4. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Implementar el plan de §3.1 con un caso de test por clase de la revisión n.º 6. Comprobar que ninguna de las 750 filas reales cambia de estado sin causa explicada.
2. Regenerar la cadena y pasar sin cambios los scripts de los revisores.
3. Respuesta (sexta parte), informe, especificación y registro.
4. Commit C14, push y punto de recuperación; congelar (C15) y encargar la revisión de lo afectado por C14 (pasada 7).

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes segunda, tercera y cuarta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
