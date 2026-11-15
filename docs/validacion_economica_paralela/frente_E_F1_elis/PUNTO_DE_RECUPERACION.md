# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** respuesta a la revisión n.º 3 y a su adenda (C7) y encargo de la revisión n.º 4.
**Hora:** 15-nov-2026, hacia las 21:55 UTC.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C7 = `9869def325b8820e2ee25618107495a7a7b70229` | Respuesta a la revisión n.º 3 y a su adenda (N1–N10): verificador, contraste, tests, cobertura por mutación, informe, especificación y respuestas |
| C8 = `97441770f51761e28c089df7830d3de802bf87e9` | Registra el hash de C7. **Commit congelado de la revisión n.º 4** |
| El commit que añade este archivo | Solo añade este punto de recuperación, su fila en el README y el manifiesto. No cambia código, datos ni resultados |

## 2. Estado de las pruebas

Sobre C7, con los mismos datos y scripts que C8. Árbol del hito 4.15 materializado; libro de Elis `d2593777…92385`.

| Prueba | Resultado | Salida |
|---|---|---|
| `especificacion_cifras.py` (regenera el CSV desde los PDF) | CSV idéntico byte a byte (SHA-256 `f24966e9…`) | Comparación con `cmp`; no se guarda salida |
| `verificar_cifras.py` | 736 filas: 722 OK, 14 PENDIENTE y 0 FALLO. Código 2, porque hay pendientes | `resultados/verificacion_cifras.json`, `verificar_cifras.log` |
| `test_verificar_cifras.py` | 63/63 | `resultados/test_verificar_cifras.log` |
| `contraste_f1.py` | 275 comprobaciones, 0 fallidas: 136 contra el libro, 110 de fuente (109 residuos) y 29 algebraicas. 402 entradas usadas, ninguna pendiente. Código 0 | `resultados/contraste_f1.{json,md,log}` |
| `test_contraste_residuos.py` | 14/14 | `resultados/test_contraste_residuos.log` |
| `cobertura_por_mutacion.py` | 0 diferencias con `cobertura_entradas`. Código 0 | `resultados/cobertura_por_mutacion.txt` |
| `sondas_metadatos.py` | Unidad y perímetro cambiados en cada fila de tabla: 697 de 697 detectados | `resultados/sondas_metadatos_C7.json` |
| `prueba_caja_no_nula.py` (LibreOffice) | **No se ha vuelto a ejecutar desde C4** (d2e585e). Depende solo del libro, cuya huella no ha cambiado. Sus 18 comprobaciones pasan dentro del contraste | `resultados/caja_no_nula.json` |
| Scripts del revisor, sin cambios | Algunos no pueden medir C7 tal como están escritos; se explica en `revision/RESPUESTAS_AUTOR_1.md`, «Los scripts del revisor sobre C7» | `resultados/mutantes_revisor_sobre_C7.txt`, `resultados/revisor3_*_sobre_C7.txt` |
| Copia de los archivos de la revisión n.º 3 | 16 de 16 blobs iguales a los de 034301c | `revision/PROCEDENCIA_REVISOR.md` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

1. **Revisión independiente n.º 4** de lo afectado por C7, sobre C8:
   - encargada hacia las 21:49 UTC; según los metadatos de su sesión, a las 21:50 UTC leía el commit congelado;
   - hasta que conste su informe, las correcciones de C7 **no están revisadas**;
   - su alcance incluye la pregunta de la persona responsable: si la unidad y el perímetro están acreditados por otra vía independiente y trazable, o si su cobertura queda pendiente.
2. **Cobertura de segunda línea:**
   - 5 entradas mueven los valores de referencia de la especificación y solo se comparan con la Historia del libro: adquisiciones e impuesto de 2021 y 2022, y ventas de 2020;
   - 31 entradas no tienen segunda línea; ninguna mueve la referencia.
3. **14 filas PENDIENTE** de URD 2022 p.302: el verificador no encuentra ni la unidad ni la cabecera de columnas. Una de ellas se usa como contraparte de R16 de 2021.
4. **Matrices por segmentos con cabeceras en orden no canónico** (URD 2021 p.247): el verificador deja el perímetro PENDIENTE. Ninguna fila real procede de ellas.
5. **Límites de detección declarados.** Ninguna identidad detecta un error menor que su cota de redondeo, como ±0,1 en las cifras de R13 de 2025.
6. **Decisiones económicas pendientes, que toma una persona [DH]:**
   - decisión F1;
   - política de la PPA;
   - dato o estimación de la reinversión necesaria (M1 a–d, M2);
   - perímetros de S2C y del margen.
7. **Fuera de este frente:** implementación, regeneración de expedientes, réplica y auditoría final.
8. **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. **Esperar el informe de la revisión n.º 4.** Hay una comprobación programada en la sesión autora para las 22:35 UTC; si la revisión sigue en curso, se vuelve a programar.
2. **Cuando el informe esté en `auditoria/economica-f1-frente-e-revision`:**
   1. consultar los metadatos de la sesión de revisión y registrar su configuración en `REGISTRO_CONFIGURACION.md`, sin identificadores de modelo;
   2. copiar sin cambios, en las mismas rutas, `REVISION_INDEPENDIENTE_4.md`, `scripts_revisor_4/` y `resultados_revisor_4/`, con el blob y el SHA-256 de cada archivo en `revision/PROCEDENCIA_REVISOR.md`;
   3. actualizar `revision/ESTADO.md` (horas del encargo y del informe) e informe §12;
   4. responder a cada objeción nueva con su commit y su prueba, sin cambiar fuentes ni huellas para legitimar un resultado;
   5. si hay correcciones, congelar un commit nuevo y encargar una revisión independiente de lo que esas correcciones afectan (pasada 5);
   6. manifiesto, commit, push y nuevo punto de recuperación.
3. **Si la sesión de revisión no termina o llega a un límite de uso:** no sustituirla por una revisión del autor. Registrarlo y pedir intervención manual.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, en ese orden. LibreOffice solo en secuencia, nunca a la vez que otro pipeline.
4. Leer este archivo, `revision/ESTADO.md` y la segunda parte de `revision/RESPUESTAS_AUTOR_1.md`.
5. Configuración acordada: la del encargo («MODELOS Y ESFUERZO»), registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora; su rama es `auditoria/economica-f1-frente-e-revision`.
