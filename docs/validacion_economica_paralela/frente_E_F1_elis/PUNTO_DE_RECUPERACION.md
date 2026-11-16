# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** respuesta a la revisión n.º 6 (C14), su congelado (C15) y el encargo de la pasada 7.
**Hora:** la del commit que contiene esta versión, en `git log` (C14 es de las 02:44:21 UTC y C15, de las 02:44:38). *(Revisión n.º 6, R8 a: el punto anterior, de c11a6de, decía «hacia las 01:50 UTC» y su commit es de las 01:38:27; desde ahora la hora es la de un commit, no una estimación.)*
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C12 = `4f3f9ba9c8240143269368c41787736b3867e97b` | Respuesta a la revisión n.º 5. Revisado en la pasada 6 |
| C13 = `1b80b5d5348e6e39dd1d632cafbbbf4e5dd3685a` | Congelado de la revisión n.º 6 |
| `c11a6de` | Copia de la revisión n.º 6 (9711f04), procedencia y registro |
| C14 = `cf55865a22035aa8376d8813cd58d0f2fcdd4846` | Respuesta a la revisión n.º 6 (R1–R8). **No revisado** |
| C15 = `c96d544646b2fa5a66c233402a9f31332a643cec` | Registra el hash de C14. **Commit congelado de la revisión n.º 7** |
| El commit que contiene esta versión de este archivo | Registra el encargo de la pasada 7. No cambia código, datos ni resultados |

## 2. Estado de las pruebas sobre C14

| Prueba | Resultado | Salida |
|---|---|---|
| `especificacion_cifras.py` (regenera el CSV desde los PDF) | 752 filas: las 750 anteriores sin cambios y 2 nuevas (ventas por segmentos de 2021 y 2022, R6) | `datos/cifras_fuente.csv` |
| `verificar_cifras.py` | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO. Las 750 anteriores, con el mismo estado y el mismo detalle que en C12 | `resultados/verificacion_cifras.json`, `verificar_cifras.log` |
| `test_verificar_cifras.py` | 108/108: 21 positivos reales, 21 PENDIENTE esperados y 66 contraejemplos | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas (136 libro, 127 fuente con 126 residuos, 29 algebraicas); 419 entradas. Código 0 | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 24/24 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 530 filas, sin incoherencias. Ninguna entrada que mueva la referencia queda sin identidad entre páginas | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | 713/713 en unidad y en perímetro | `resultados/sondas_metadatos_C14.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, cuya huella no ha cambiado | `resultados/caja_no_nula.json` |
| Scripts de los revisores n.º 1, 3, 4 y 5 | Mismos resultados que sobre C12, salvo recuentos y motivos explicados en la sexta parte de las respuestas | `resultados/*_sobre_C14.txt` |
| Scripts del revisor n.º 6 | Sus 48 contraejemplos, con el resultado que se describe en la sexta parte. Barrido completo C13 → C14 (122.604 candidatas) cruzado con su lectura geométrica: ninguna candidata pasa a OK; clase F, 0 | `resultados/revisor6_*_sobre_C14.txt` |
| Valores de referencia de E9 | Sin cambios | `resultados/contraste_f1.json` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

**Qué cubren estas pruebas** (revisión n.º 6, R7 e): los casos de los revisores, las filas reales y el barrido del revisor n.º 6 sobre todas las líneas con rótulo de los cinco PDF, declaradas como cifras del grupo de dos columnas. No cubren otras declaraciones ni clases de error que esos filtros no señalan.

## 3. Incidencias pendientes

1. **C14 sin revisar** hasta la pasada 7. Incluye las tres decisiones que no siguen la propuesta del revisor: R1 (grupos de columnas en el perímetro), R2 (G2 y G4 en PENDIENTE) y R3 (umbral de 5,5 caracteres).
2. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 entradas con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
3. **Verificador:** reglas heurísticas sobre la rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
4. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Esperar a la pasada 7: sesión de revisión nueva creada a las 02:45:09 UTC sobre C15, con publicación en `auditoria/economica-f1-frente-e-revision` sobre 9711f04. Hay una comprobación programada para las 03:46 UTC.
2. Cuando termine: copiar sin cambios su informe, sus scripts y sus salidas, con procedencia (blob y SHA-256); registrar su configuración con `get_session`; actualizar ESTADO, REGISTRO, el informe §12 y este punto. Commit y push.
3. Responder a sus objeciones (C16), con pruebas sobre las filas reales y el barrido, y encargar la revisión de lo que afecten.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes quinta y sexta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
