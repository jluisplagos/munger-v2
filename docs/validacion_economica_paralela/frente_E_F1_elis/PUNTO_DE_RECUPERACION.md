# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** encargo de reconciliación de la propuesta de decisiones F1 con la especificación (revisión externa `1a07188`, F1-P1 a P4), con su única revisión independiente dirigida a P1–P4 ya incorporada. **Sin implementar nada.** El encargo termina aquí: si la revisión encuentra una carencia de datos o de política, se documenta el bloqueo y no se encadena otra pasada.
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Elis sigue en `pendiente_de_datos`. Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C18 = `f12f8ea` · C19 = `06ad100` · `6d799c6` | Respuesta a la revisión n.º 8 del verificador · congelado de la n.º 9 · copia de la n.º 9 |
| `b83803c` | Propuesta de decisiones F1, revisión 1. La revisó la revisión externa `1a07188` |
| `13f864f910bf0bb3e27007b23c13a8e957f1bfb7` | **Congelado de la respuesta a la revisión de la propuesta:** respuesta P1–P4, propuesta revisión 2 con tabla única (1a)–(5b), especificación E2–E6, E8 y E9, precisiones del informe y dos scripts nuevos con sus salidas |
| `d5188bb` | Registro del encargo de la revisión dirigida a P1–P4 |
| `8fcc7fd792f065cf29e2dc915bda92faeff1d45a` (rama `auditoria/economica-f1-frente-e-revision`) | Revisión dirigida a P1–P4, de una sesión nueva distinta de la autora |
| El commit que contiene esta versión de este archivo | Copia de esa revisión, sin cambios (16/16 blobs), con procedencia. Registro de su configuración y de su resultado. Avisos en la cabecera de la propuesta, la respuesta y la especificación, y salvedad V1 en el informe, §6.3. **Las correcciones V1–V11 no están aplicadas** |

## 2. Estado de las pruebas

Ningún script ha cambiado desde `13f864f`.

| Prueba | Resultado | Quién |
|---|---|---|
| `controles_sinteticos_f1.py` | Código 0; 22 casos con el resultado esperado; 9/9 del revisor externo | Autor; reproducido byte a byte por la revisión dirigida |
| `copia_investigacion_f1.py` | Código 0; 43 controles, 0 fallidos | Autor; reproducido byte a byte. N1 recalculado con otra implementación: −11,605 y −18,609; coinciden 108 valores y 89 celdas del libro |
| `contraste_f1.py` | 292 comprobaciones, 0 fallidas; salidas idénticas | Autor y revisión dirigida |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | Autor; la revisión dirigida, 356 de 356 sobre `13f864f` |
| Scripts de la revisión dirigida (`revision/scripts_revisor_p1_p4/`) | Ejecutados por el revisor; salidas en `revision/resultados_revisor_p1_p4/`. El autor no los ha vuelto a ejecutar | Revisor |
| Verificador, sus tests, mutación, sondas de metadatos, barrido y scripts de los revisores n.º 1 a 9 | Sin cambios desde C18: 752 filas (738 OK, 14 PENDIENTE, 0 FALLO); 136/136 y 9/9; 24/24; 530 filas | Últimas ejecuciones de C18 |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4 | — |

## 3. Incidencias pendientes

0. **Decisiones F1, de la persona responsable:** (1a)–(5b), con el texto exacto de la tabla única de la propuesta. Antes de decidir, leer el aviso de su cabecera, sobre todo V1 para (4b). No se implementa nada hasta su aprobación.
1. **Correcciones V1–V11 de la revisión dirigida, no aplicadas.** Aplicarlas cambiaría el material revisado y exigiría revisar lo afectado. Decide la persona responsable si se aplican y con qué revisión.
   - V1 (material): fundamento de (4b) y de la fila 2; informe §6.3.
   - V2: términos explícitos en el ancla de S2C.
   - V3: caja del earnout y actualización de 2025, publicadas.
   - V4: alcance de N1 en el τ de cinco años.
   - V5: amortización ROU en la sensibilidad del arrendamiento y en «PPA constante».
   - V6: control del terminal frente al del libro.
   - V7: fórmula de los términos explícitos.
   - V8: cota de R.
   - V9: casos sintéticos con crecimiento y ancla calculada.
   - V10–V11: forma y textos de aprobación.
2. **Carencias que bloquean y no son defectos** (revisión dirigida, §10):
   - M1: reparto del capex y del plan climático;
   - M2: bajas de clientes;
   - M6: finalidad de las compras, en concreto de las pequeñas, y crecimiento orgánico sin ellas;
   - N2: fiscalidad y caja de la plusvalía de 2025;
   - perímetro de las palancas S2C y ROIC de Elis;
   - convención del tipo de proyección, fuera de F1;
   - umbral de V-F1a y del aviso del terminal del libro.

   Preguntas preparadas, no enviadas: respuesta, §6.
3. **Respuesta a la revisión n.º 9 del verificador (C20), en espera.** Es trabajo independiente ya abierto. Plan en el commit `b83803c`, `PUNTO_DE_RECUPERACION.md`, §3, punto 1.
4. **Límites del verificador** y **cobertura de la unidad y del perímetro:** los de C18 (`b83803c`, mismo archivo, §3, puntos 3 y 4).
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real.** Se conservan C48 = 108, C49, el FCF base 307,933 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

Esperar a la persona responsable. No se lanza ninguna pasada más por iniciativa propia.
1. Sus decisiones sobre (1a)–(5b). Lo aprobado se registrará con fecha, persona y motivo, y se aplicará con las pruebas T15 y T16 y una revisión independiente.
2. Si quiere que se apliquen V1–V11: un encargo nuevo y acotado, con su revisión dirigida a lo afectado.
3. Si no indica otra cosa, la respuesta C20 a la revisión n.º 9 del verificador sigue en espera.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, y los de la respuesta, §1. LibreOffice solo en secuencia. Los de la revisión dirigida: su §12.
4. Leer este archivo, `revision/ESTADO.md`, la propuesta con su aviso, la respuesta (§7) y `revision/REVISION_PROPUESTA_P1_P4.md`.
5. Configuración acordada: la de cada encargo, registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora.
