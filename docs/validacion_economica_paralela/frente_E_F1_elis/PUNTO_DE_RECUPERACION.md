# Punto de recuperación · frente E · F1 · Elis

Se reescribe al terminar cada bloque importante. Las versiones anteriores quedan en el historial de git.

**Bloque cerrado:** encargo de la revisión dirigida a P1–P4 (este commit solo lo registra); antes, en el commit congelado `13f864f910bf0bb3e27007b23c13a8e957f1bfb7`, la reconciliación de la propuesta de decisiones F1 con la especificación, en respuesta a la revisión externa de la propuesta (rama `auditoria/revision-propuesta-f1`, commit `1a07188`, F1-P1 a P4). **Sin implementar nada.**
**Hora:** la del commit que contiene esta versión, en `git log`.
**Rama:** `auditoria/economica-f1-frente-e`.

**F1 sigue abierto.** Elis sigue en `pendiente_de_datos`. Este punto no cierra ningún requisito: solo dice dónde está el trabajo y cómo seguir.

## 1. Dónde está el trabajo

| Commit | Contenido |
|---|---|
| C16 = `66d01b8` · C17 = `863ddde` | Respuesta a la revisión n.º 7 · congelado de la revisión n.º 8 |
| C18 = `f12f8ea79ed5c1b444d85163c5ed08d8d07a6243` | Respuesta a la revisión n.º 8 (verificador) |
| C19 = `06ad100` · `105b57b` · `6d799c6` | Congelado de la revisión n.º 9 · encargo · copia de la revisión n.º 9 (a3a1a2b) |
| `b83803c` | Propuesta de decisiones F1, revisión 1. La revisó la revisión externa `1a07188` |
| **`13f864f910bf0bb3e27007b23c13a8e957f1bfb7`** | **Congelado de la respuesta a la revisión de la propuesta:** [RESPUESTA_REVISION_PROPUESTA_F1.md](RESPUESTA_REVISION_PROPUESTA_F1.md); [PROPUESTA_DECISIONES_F1.md](PROPUESTA_DECISIONES_F1.md), revisión 2, con la tabla única (1a)–(5b); especificación E2–E6, E8 y E9; precisiones del informe (§4.2, §6.4 y §9); `scripts/controles_sinteticos_f1.py` y `scripts/copia_investigacion_f1.py`, con sus salidas. No cambia código existente, datos, libros, fórmulas ni cifras de valoración. Sobre este commit se encarga la revisión dirigida a P1–P4 |
| El commit que contiene esta versión de este archivo | Registra el encargo de la revisión dirigida a P1–P4. No cambia el material revisado |

## 2. Estado de las pruebas

| Prueba | Resultado | Salida |
|---|---|---|
| `controles_sinteticos_f1.py` (nuevo) | Código 0. 22 casos con importes ficticios: 8 coherentes y 14 incoherencias ilustradas, todos con el resultado esperado. 9/9 casos de la revisión reproducidos. El motor sintético coincide con `motor_a` | `resultados/controles_sinteticos_f1.{json,log}` |
| `copia_investigacion_f1.py` (nuevo) | Código 0. 43 controles, 0 fallidos: reproduce f, el τ de 5 años, el flujo sin crecimiento 248,496395342656, los 33 flujos del libro, el FCF base registrado, C48 = 108, el diagnóstico 27,936 y la sensibilidad 16,778237 de la revisión. Variación idéntica en A0, A1 y A2 | `resultados/copia_investigacion_f1.{json,md}` |
| `contraste_f1.py` | Ejecutado de nuevo en este bloque: 292 comprobaciones, 0 fallidas; salidas idénticas byte a byte | `resultados/contraste_f1.{json,md}` |
| `verificar_cifras.py`, `test_verificar_cifras.py`, `test_contraste_residuos.py`, `cobertura_por_mutacion.py`, `tabla_conciliacion.py`, `sondas_metadatos.py`, `barrido_fecha_rotulo.py` y scripts de los revisores n.º 1 a 9 | Sin cambios desde C18; no se han vuelto a ejecutar porque no cambia su código ni sus entradas. Último estado: 752 filas (738 OK, 14 PENDIENTE, 0 FALLO); 136/136 casos y 9/9 comprobaciones directas; 24/24; 530 filas sin incoherencias | Las de C18, en `resultados/` |
| `prueba_caja_no_nula.py` (LibreOffice) | No se ha vuelto a ejecutar desde C4: depende solo del libro, que no cambia | `resultados/caja_no_nula.json` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK | — |

## 3. Incidencias pendientes

0. **Decisiones F1, de la persona responsable:** (1a), (1b), (2), (3a), (3b), (4a), (4b), (5a) y (5b), con el texto exacto que se pide aprobar en la tabla única de la propuesta. No se implementa nada hasta su aprobación.
1. **Revisión económica independiente dirigida a P1–P4**, sobre el commit congelado `13f864f`: **encargada** el 16-nov-2026 a las 14:11:39 UTC, con aviso previo, a la sesión de revisión `session_01W2RVAq9YS8QckcRk1RaGzm`, que escribe en `auditoria/economica-f1-frente-e-revision`. Una sola pasada: si encuentra una carencia de datos o de política, se documenta el bloqueo y se termina.
2. **Carencias que bloquean Elis:**
   - M1 (reparto de la inversión propia, con el plan climático: importe, horizonte y finalidad);
   - M2 (bajas de clientes y desembolso por cliente nuevo);
   - M6 (finalidad de las compras, si no se aprueba (4b));
   - N2 (fiscalidad, caja y reposición de las bajas de 2025 con seguros);
   - actualización del earnout mexicano en el tipo;
   - perímetro de las palancas S2C y ROIC.

   Preguntas preparadas, no enviadas: respuesta, §6.
3. **Respuesta a la revisión n.º 9 del verificador (C20), en espera.** Es trabajo independiente ya abierto. Plan en la versión anterior de este archivo (commit `b83803c`, §3, punto 1): U1–U6 de `revision/REVISION_INDEPENDIENTE_9.md`, §7.
4. **Cobertura de la unidad y del perímetro**, y **límites del verificador:** los de C18 (versión anterior de este archivo, §3, puntos 3 y 4).
5. **Decisiones económicas [DH]** y **sin aptitud para dinero real.** Se conservan C48 = 108, C49, el FCF base 307,933 y E1/D3/E2/E6.

## 4. Siguiente paso exacto

1. Hecho a las 14:11 UTC: aviso a la persona responsable y encargo de la revisión dirigida a P1–P4:
   - sesión nueva, con el modelo y el esfuerzo que el encargo asigna a la revisión económica;
   - sobre este commit congelado, en una rama propia del revisor;
   - con el material de la revisión externa en `1a07188`.
2. Al terminar:
   - copiar su informe con procedencia y huellas;
   - registrar la configuración en `REGISTRO_CONFIGURACION.md` y el resultado en `revision/ESTADO.md`;
   - si señala una carencia de datos o de política, documentar el bloqueo y terminar, sin encadenar otra pasada;
   - commit y push.
3. Esperar las decisiones F1. Lo aprobado se registrará con fecha, persona y motivo, y se aplicará en la especificación y el motor, con las pruebas T15 y T16 y una revisión independiente.

## 5. Cómo reanudar en una sesión nueva

1. `git fetch origin auditoria/economica-f1-frente-e` y `git checkout auditoria/economica-f1-frente-e`.
2. Materializar un árbol `munger_v2_r1`, según la sección de archivos pesados del README del repositorio (`tools/base_414.py`, con el ZIP original de la Release `base-4.14`).
3. Ejecutar los comandos del informe, §13, y los de la respuesta, §1, en ese orden. LibreOffice solo en secuencia.
4. Leer este archivo, `revision/ESTADO.md`, la respuesta y la propuesta revisada.
5. Configuración acordada: la de cada encargo, registrada en `REGISTRO_CONFIGURACION.md`. La revisión la hace una sesión distinta de la autora.
