# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** incorporación de la revisión n.º 8 (copia sin cambios, procedencia y registro). Su respuesta, C18, está en preparación.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C16 = `66d01b8fc21b277efdae938170cc64815705962e` | Respuesta a la revisión n.º 7 (S1–S7). Revisado en la pasada 8 |
| C17 = `863ddde9190044690bfe4ee7c2a0d6fddc4c811a` | Congelado de la revisión n.º 8 |
| `7e59a8c` | Registra el encargo de la pasada 8 |
| El commit que contiene esta versión de este archivo | Copia de la revisión n.º 8 (3138a6b), procedencia y registro. No cambia código, datos ni resultados |

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

1. **Responder a la revisión n.º 8** (C18). Plan, según sus correcciones propuestas:
   - **T1:** cuando el ejercicio sale de la fecha del rótulo, la dimensión «columna» no puede quedar NO_APLICA: se comprueba la columna del concepto si la tiene declarada y, si no y la fila tiene varias columnas, PENDIENTE;
   - **T2:** la regla de la fecha del rótulo solo para filas de saldo: rótulo en la primera celda de una línea con más celdas, token a su derecha, rótulo que sea la fórmula del saldo y la fecha y no una frase, sin unir una línea de fecha que continúa la anterior;
   - **T3:** unir la línea de encima que termina en el día o en el año (saldos de cierre del estado de cambios en el patrimonio), o declarar el límite;
   - **T4:** la búsqueda de cabecera por países no se corta en la primera línea del rótulo de una fila (DEU 2024 p.315);
   - **T5:** rótulo de las líneas contiguas acotado a 45 caracteres y a la sangría de los rótulos, y no para una línea que solo lleva la pestaña;
   - **T6:** encabezado numerado: rechazar «Note N to the…» y admitir la coma final si la línea siguiente continúa el título, o declararlo;
   - **T7 y T8:** frases y recuentos; reproducir `reproduccion_7` sobre el árbol final.
2. **C18 sin revisar** hasta la pasada 9.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Límites del verificador:** regla de grupos, honorarios por firma en PENDIENTE, rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Leer entera la revisión n.º 8 (§3 a §9) y sus contraejemplos (`revision/resultados_revisor_8/contraejemplos_8.txt`).
2. Implementar el plan de §3.1 con un caso de test por clase. Comprobar que ninguna de las 752 filas reales cambia de estado sin causa explicada, y pasar los barridos de los revisores n.º 6 a 8 entre C16 y C18.
3. Respuesta (octava parte), informe, especificación, estado y registro. Commit C18, push y punto de recuperación; congelar (C19) y encargar la pasada 9.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes sexta, séptima y octava (cuando exista) de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
