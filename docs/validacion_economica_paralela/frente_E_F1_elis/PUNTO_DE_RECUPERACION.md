# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** incorporación de la revisión n.º 7 (copia sin cambios, procedencia y registro). Su respuesta, C16, está en preparación.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C14 = `cf55865a22035aa8376d8813cd58d0f2fcdd4846` | Respuesta a la revisión n.º 6 (R1–R8). Revisado en la pasada 7 |
| C15 = `c96d544646b2fa5a66c233402a9f31332a643cec` | Registra el hash de C14. Congelado de la revisión n.º 7 |
| `66d188c` | Registra el encargo de la pasada 7 |
| El commit que contiene esta versión de este archivo | Copia de la revisión n.º 7 (d192cab), procedencia y registro. No cambia código, datos ni resultados |

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

1. **Responder a la revisión n.º 7** (C16). Plan, según sus correcciones propuestas:
   - **S1:** no tomar por cabecera de columnas la línea de un encabezado numerado ni su continuación (el año del título del estado de cambios en el patrimonio no es una columna); en las filas con la fecha del saldo en el rótulo, aunque esté partido en dos líneas, tomar el ejercicio de la fila. Casos A1, A8 y A9;
   - **S2:** si la línea de la cifra no tiene rótulo, tomarlo de las líneas contiguas de arriba y de abajo (URD 2023 p.261, Escandinavia y Europa del Este). Casos B1 y B3; barrer también las líneas sin rótulo;
   - **S3:** descartar como rótulo un dígito suelto al principio de la línea seguido de una celda de texto (número de capítulo del margen; «CGU France» del URD 2022 p.298). Caso C1;
   - **S4:** sin declaración de unidades ni línea de ejercicios, buscar la cabecera en la línea de celdas que precede al bloque de filas (hipótesis del WACC por UGE); no tomar por cabecera de ejercicios la primera línea de un rótulo partido. Casos D1 y D5;
   - **S5:** que el encabezado numerado no sea prosa;
   - decisión (b) de C14: revisar el argumento que, según el revisor, no es de perímetro, y declarar el límite de la regla de grupos (tabla de marcas con un solo ejercicio, URD 2021–2023);
   - **S6 y S7:** frases y recuentos.
2. **C16 sin revisar** hasta la pasada 8.
3. **Cobertura de la unidad y del perímetro:** 8 páginas (24 entradas) sin identidad entre páginas, 140 con solo identidad de su página, 31 sin segunda línea y 2 solo con la Historia. Ninguna mueve la referencia.
4. **Verificador:** reglas heurísticas sobre la rejilla de pdftotext; 14 filas PENDIENTE (URD 2022 p.302); límites de detección de R13, R39 y R42.
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real**; se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Leer entera la revisión n.º 7 (§3 a §9) y sus contraejemplos (`revision/resultados_revisor_7/contraejemplos_7.txt`).
2. Implementar el plan de §3.1 con un caso de test por clase. Comprobar que ninguna de las 752 filas reales cambia de estado sin causa explicada, y pasar los barridos de los revisores n.º 6 y 7 entre C14 y C16.
3. Respuesta (séptima parte), informe, especificación, estado y registro. Commit C16, push y punto de recuperación; congelar (C17) y encargar la pasada 8.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md` y las partes quinta y sexta de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora, en la rama `auditoria/economica-f1-frente-e-revision`.
