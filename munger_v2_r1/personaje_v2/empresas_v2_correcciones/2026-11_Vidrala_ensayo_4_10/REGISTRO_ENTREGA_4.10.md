# Registro de la entrega 4.10 · consolidación financiera de Vidrala y correcciones de trazabilidad

**Encargo:** «Munger V2 — Encargo 4.10», recibido el 11-nov-2026, posterior a la revisión externa de la 4.9 (ChatGPT).

**Base:** `munger_v2_r1_entrega4.9_integridad_auditoria_y_N4.zip`, SHA-256 `8a48158996a955a0ad1a1e54080f0b1b73729fe3750d75b1457b2514cc552ea5`, de 115.641.984 bytes.

**Quién hizo qué:**
- **Ejecución principal:** Claude (Opus).
- **Revisión interna:** Claude con contexto separado, un agente que no participó en el trabajo (§5). No es la revisión externa.
- **Revisión externa:** la hará ChatGPT, después y fuera de esta entrega.

## 1. Partida

`arranque/ARRANQUE_4_10.md` recoge lo comprobado al empezar:
- huella, tamaño y CRC del ZIP;
- VERSION;
- el manifiesto en una extracción limpia (conservada sin escritura), en una de trabajo y en una con Python `zipfile`, que reproduce la incidencia del nombre UTF-8 (1 ausente y 1 de más);
- la referencia mecánica, reproducida.

La tanda histórica no se repitió como ceremonia de arranque: ya se había ejecutado íntegra sobre el árbol 4.9, con PASA y salidas idénticas.

## 2. Qué se hizo

| Parte | Qué | Dónde |
|---|---|---|
| 3.1–3.4 | ZIP portable; BOM antes de H2; ficha sin marcadores con cierre registrado; comprobante externo del libro final. Reproducción con el código de la 4.9 (26/69) y batería nueva obligatoria (74) | `INFORME_CORRECCIONES_TECNICAS_4_10.md` · `tecnico/` · `personaje_v2/pruebas/test_trazabilidad_v2.py` |
| N4 (§4.1–§4.2) | Definición explícita de otros activos financieros (derivados corrientes por año); evidencia completa, parcial, dependiente de la definición o no aplicable (18/8/9/3); registro separado | `n4/` · `scripts/n4_revision.py` |
| P3 (§4.3) | Conciliación de principal e interés de arrendamientos con el CFO, C48 y C49: situaciones A y B, y lo desconocido | `INFORME_FINANCIERO_4_10.md` §2 |
| N5–N8, N10 (§5) | Pensiones; fecha de E y r_op; acciones; derecho al dividendo; probabilidades e historia adversa | `INFORME_FINANCIERO_4_10.md` §3–§7 |
| Variantes (§6) | 12 variantes recalculadas con LibreOffice en copias identificadas y 14 identidades comprobadas aparte; tabla CSV y JSON | `variantes/` · `scripts/variantes_4_10.py` |
| Copia combinada | C1 (N6 + N7) con cachés y comprobante externo, ÍNTEGRO | `copia_combinada/` |
| Pasos del personaje | Expediente exploratorio con las entradas de C1: el pipeline archivó la aprobación heredada y se detuvo en el paso 5 (código 10, esperando al agente), que es su estado legítimo; motivo en el informe §8 | `expediente_exploratorio/` · `resultados/pipeline_exploratorio_salida.txt` |
| §7 | Propuesta única de decisiones (campos humanos vacíos); aclaración de P-N1; especificación de la integración | `propuestas/` · `ACLARACION_PN1_4_10.md` · `ESPECIFICACION_INTEGRACION_4_10.md` |
| Continuidad | `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` (con la estructura de uso, la línea y el título restaurados), `VERSION`, `DECISIONES.md`, `verificar_paquete.sh` (batería nueva) y el LEEME de controles de la 4.10. Copias de la 4.9 en `reproduccion/` | raíz · `resultados/LEEME_BATERIAS_HISTORICAS.md` |

## 3. Archivos cambiados respecto a la 4.9

Están en `CAMBIOS_ARCHIVOS.txt`, sección «RESPECTO A LA 4.9», con las huellas antes y después.

**Modificados:**
- `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` y `verificar_paquete.sh`;
- `personaje_v2/DECISIONES.md`;
- `personaje_v2/scripts/cierre_v2.py`, `pipeline.py`, `ficha.py`, `informe.py`, `resumen.py` y `verificar_todo.sh`;
- `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`, que se regeneran.

**Nuevos:**
- `personaje_v2/scripts/acreditar_libro.py`;
- `personaje_v2/pruebas/test_trazabilidad_v2.py`;
- el expediente `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/`.

**Intactos:** ningún original, expediente anterior (tampoco la 4.9), fuente, libro de referencia ni decisión registrada. Lo comprueba `scripts/comprobar_entrega_4_10.py` frente al manifiesto de la 4.9.

El motivo de cada cambio de código está en `INFORME_CORRECCIONES_TECNICAS_4_10.md`.

## 4. Decisiones técnicas tomadas (rutinarias según el encargo §1; revisables)

- **La lectura común es `texto_fiel`;** no se crea otra función. Solo cambia dónde se aplica.
- **Cierre registrado:** cuenta como tal la presencia de `cierre_vigente.json`, aunque sea ilegible. En los scripts, la condición se comprueba localmente, para no depender de funciones nuevas de `cierre_v2.py` (como en la 4.9).
- **Con un solo marcador cambiado,** `ficha.py` mantiene la sustitución de la 4.6.1 y la 4.7.1 (código 0 con aviso). Es la decisión pendiente de §9.5, que no se toma aquí.
- **Acreditación del libro:** el comprobante entra en el material auditado. Los expedientes sin comprobante no reciben uno a posteriori.
- **Variantes:**
  - `escribir_v63.py` se niega a escribir en celdas con fórmula. Para el dividendo se usa la celda de valor `Historia!L26`, que solo entra en el puente, como vehículo declarado.
  - La alternativa de τ en r_op, que no es representable, se calcula en una copia estructural identificada.
- **Pasos del personaje:** el expediente exploratorio se detiene en el paso 5. La fase C compararía con el precio de noviembre de 2026, y la actualización de la oportunidad queda fuera del encargo.

## 5. Modelos y revisión interna

**Modelos.** Opus en todo el procedimiento. Fable no se usó: el trabajo era sobre todo de comprobación reproducible (código, cuadres con fuentes y recálculo), con criterios fijados por el encargo, y una crítica de razonamiento con Fable no compensaba su coste.

**Revisión interna.**
- **Quién y sobre qué.** Un agente de Claude (Opus) con contexto separado, que no participó en el trabajo. Revisó el ZIP candidato 1 (SHA-256 `450ef3d6…b933f`) sobre una copia propia de la extracción con `unzip`.
- **Material fijado:** `revision_interna/MATERIAL_REVISION_4_10.txt`, 48 archivos con la misma huella al empezar y al terminar.
- **Informe:** `revision_interna/REVISION_INTERNA_4_10.md`; sus scripts y salidas están en `revision_interna/material_revisor/`.
- **Lo que ejecutó el revisor:**
  - las baterías de trazabilidad (68/68), integridad (103/103), solicitudes (55/55) y resumen (45/45);
  - `n4_revision.py`, con una matriz idéntica;
  - las cifras, contra el PDF español;
  - las identidades, con aritmética propia;
  - la conservación;
  - seis ataques propios.

**Incidencia: se incumplió la regla de LibreOffice.**
- A las 17:43:30–17:43:37 (hora local), `test_resumen_v2.py` arrancó LibreOffice en la copia del revisor. Su última prueba recalcula una empresa sintética; las instrucciones la daban por segura, y era un error de quien las escribió.
- En ese momento estaba en curso la verificación del candidato 1 (17:37–17:48).
- Esa verificación dio PASA, pero no se usa como resultado de referencia: la del ZIP final se repite en secuencia, sin ninguna otra tarea en marcha (§6).
- `CONTINUIDAD.md` §2 dice ahora que `test_resumen_v2.py` usa LibreOffice (R-8).

**Hallazgos y tratamiento** (ninguno bloqueante):

| Hallazgo | Gravedad | Tratamiento | Dónde se comprueba |
|---|---|---|---|
| **R-1.** Con los dos marcadores perdidos y además `cierre_vigente.json` borrado, `resumen.py` volvía a publicar pendiente_de_datos/APROBADO: el estado del pipeline seguía con APROBADO. Venía de la 4.9 | Importante | **Corregido.** `aprobacion_sin_ficha_cerrada` es motivo de retirada; las cuatro vías la comprueban y `archivar_salidas` reinicia el estado. `resumen.py` no escribe «APROBADO» para una ficha no cerrada | Grupo M, 4 pruebas nuevas |
| **R-2.** El comprobante de la copia combinada daba como libro de entrada el de la 4.6.1 (sin las entradas de C1); el expediente exploratorio mezcla datos de C1 con el evaluado de la 4.6.1 | Importante | **Corregido** en la copia combinada: su libro de entrada es el de datos con C41 y C55 de C1. En el expediente exploratorio se **declara**: `expediente_exploratorio/LEEME.md` lista los archivos que siguen siendo de la 4.6.1 hasta los pasos 5–12. La copia combinada no es un expediente y no pasa `verificar_todo.sh` completo (se dice en el informe §8) | `variantes_4_10.py` · `comprobar_entrega_4_10.py` |
| **R-3.** La acreditación aceptaba un comprobante «NO ÍNTEGRO» con la huella correcta y cualquier `.xlsx` | Menor | **Corregido.** Exige el veredicto ÍNTEGRO y el libro evaluado | Grupo L, 1 prueba nueva |
| **R-4.** Equivalencia de P3 dada con 6,764, cuando la variante usa 6,754; efecto de τ sin decir la base | Menor | **Corregido** en el informe, la propuesta y el JSON (6,754 = 4,5 + 2,254; τ: +0,155 respecto a la referencia y +0,232 respecto a N6) | — |
| **R-5.** «`L26` solo entra en el puente»: mueve también los múltiplos EV/ventas y EV/EBITDA | Menor | **Corregido** en la descripción de la variante y en el informe | — |
| **R-6.** La copia estructural de τ figuraba como «COMPLETO Y VÁLIDO» sin matiz | Menor | **Corregido:** campo `aviso` en la variante y matiz en el informe §8 | — |
| **R-7.** El expediente exploratorio conservaba sin marcar archivos de la 4.6.1; no seguir es una decisión de alcance | Menor | **Corregido:** `expediente_exploratorio/LEEME.md` y la redacción del informe | — |
| **R-8.** `CONTINUIDAD.md` no decía que `test_resumen_v2.py` usa LibreOffice | Menor | **Corregido** | — |
| **R-9.** La composición de «Otros activos corrientes» solo está comprobada en 2024–2025 | Menor | **Declarado** como límite en el informe §1 | — |

**Lo que no se pudo comprobar:**
- **La verificación del árbol 4.9.** Su salida se conserva ahora en `arranque/verificacion_arbol_4_9/`.
- **Los recálculos con LibreOffice y las baterías que lo usan.** Los cubre la verificación final de §6.
- **El caso de `ficha.json` ausente con un cierre registrado.** El revisor solo lo leyó en el código; se ha añadido una prueba dirigida (grupo M, por el paso 14).
- **Las correcciones de R-1 a R-9.** No las ha revisado un segundo control independiente. Las ha comprobado Claude con la batería ampliada y con la verificación final, y quedan para la revisión externa.

## 6. Verificación

Todas las ejecuciones de esta sección las hizo Claude. Cada ZIP se construyó con `scripts/empaquetar_zip.py`, que extrae con Python y con `unzip`, comprueba el manifiesto en las dos extracciones y compara los árboles byte a byte.

**Candidato 1** (SHA-256 `450ef3d6…b933f`):
- Extracción doble: PASA.
- `verificar_paquete.sh completa`: PASA, código 0, aunque coincidió con la incidencia de LibreOffice de §5.
- Controles: la 4.9 dio 35 de 39 (M22 ligada al código, §3 del LEEME) y la 4.10, 43 de 43.
- **No se usa como referencia.** Sobre este candidato se hizo la revisión interna.

**Candidato 2** (SHA-256 `473ba39a…16c3`; con las correcciones de R-1 a R-9, la batería ampliada a 74 y las salidas de referencia del árbol 4.10 aún provisionales):
- Extracción doble: PASA. Manifiesto con 1.938 archivos: 0 modificados, 0 ausentes y 0 adicionales con los dos lectores; árboles idénticos.
- `verificar_paquete.sh completa`, en secuencia y sin ninguna otra tarea: **PASA**, código 0, en 11 min 12 s.
  - Manifiesto, entorno y piloto (35, salida idéntica): PASA.
  - `test_comprobadores.py` 114/114; sintético 30/30 con los mismos nombres.
  - Trazabilidad **74/74**; integridad 103/103; solicitudes 55/55; estados 28/28; resumen 45/45; cierre 55/55.
- Controles, en el orden del LEEME:
  - salidas idénticas a sus referencias en la 4.2 (45), la 4.3 (217 de 217), la 4.3.1 (43 de 43), la 4.4 (72 de 72), la 4.5 (60 de 60) y la 4.6.1 (23 de 23);
  - la 4.6, 23 de 24;
  - las dos comparaciones de baterías, «HAY DIFERENCIAS»;
  - la 4.7 (45 de 49), la 4.7.1 (38 de 44), la 4.8 (32 de 36) y la 4.8.1 (27 de 30), con los mismos casos que no cumplen en el árbol 4.9;
  - la 4.9, 35 de 39.

  Esas salidas son las referencias de `resultados/…_en_arbol_4_10.txt`.
- `comprobar_entrega_4_10.py`: **43 de 44**. El caso que no cumplía era un **error del propio control**, no del paquete. La mutación equivalente a M22 sí se detectó (la batería de integridad bajó a 97/103), pero el ancla del control aparece dos veces en `cierre_v2.py`. Se corrigió el ancla y, con el control corregido sobre la misma extracción, dio **44 de 44**, código 0 (3 reejecutan, 13 recalculan y 28 constatan); su salida es la referencia `resultados/comprobar_entrega_4_10_salida.txt`.
- Después de todo, el manifiesto sigue intacto (fuera de `pruebas/` y `.lo_perfil/`).

**ZIP final.** Es el candidato 2 con el control de la 4.10 corregido, este apartado, el LEEME y las salidas de referencia, y `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` regenerados.
- Su verificación (extracción doble, `verificar_paquete.sh completa` y todos los controles, en secuencia, sobre una extracción limpia) es posterior a este registro.
- No puede figurar dentro del propio ZIP: se entrega aparte, en `munger_v2_r1_entrega4.10_consolidacion_financiera_y_trazabilidad.VERIFICACION.txt`, con la huella exacta del ZIP.

## 7. Límites y pendientes

- **N6:** el precio de cierre de 2025 procede del informe financiero anual depositado en la CNMV; no se ha contrastado con el boletín de BME.
- **N5:** sin el desglose de la provisión «Personal».
- **P3:** la línea de flujos de los intereses de arrendamientos no se publica (Q-N4a); la discrepancia de la nota 8 sigue abierta.
- **P-M1** sigue abierta, y la integración de N1–N3 está solo especificada.
- **Ningún cero está confirmado.** Las propuestas esperan a la persona responsable (CONTINUIDAD §9.9).
- **La política de verificación automática de ceros sigue sin activar.** Sus once engaños conocidos (4.9, W-5) quedan para un encargo propio; el clasificador actual no es una solución genérica validada.
- **Fuera del encargo:** N9/ruta B de 2026, la actualización frente a 87,90 €, empresas nuevas, el reanálisis masivo, los contactos externos y la publicación.
