# Registro de pruebas · entrega 4.10.1

**Qué es.** Qué se ejecutó para comprobar la 4.10.1, dónde, con qué resultado y con qué límites. Solo figura lo que se ejecutó de verdad. La verificación del ZIP final exacto está fuera del paquete, en su registro externo `munger_v2_r1_entrega4.10.1_piloto_2025_y_trazabilidad.zip.VERIFICACION.txt`, porque un ZIP no puede contener su propia huella.

## 1. T-1

| Prueba | Dónde | Resultado |
|---|---|---|
| `test_trazabilidad_v2.py` (versión final, tras H-3) | árbol de trabajo, 12-nov | **78/78**, código 0; grupo L 11/11 |
| La misma batería, desde la revisión interna (antes de H-3) | árbol de trabajo, 11-nov | 78/78; grupo L 11/11 |
| Archivo de la 4.10 (`reproduccion/test_trazabilidad_v2_4_10.py.txt`), ejecutado para registrar sus nombres | árbol de trabajo, 12-nov | 74/74; los 74 grupos y nombres (`reproduccion/nombres_trazabilidad_4_10.json`) están todos en la 4.10.1, que añade 4 |
| `scripts/reproducir_T1.py` (endurecido tras la revisión) | árbol de trabajo | código 0; salida idéntica a `t1/reproducir_T1_salida.txt`; sin `__pycache__` |
| Unidad de `rezip_inocuo` (H-3), extraída de la batería | árbol de trabajo | con un origen que ya tiene la forma de la prueba, bytes distintos y contenido igual (`t1/h3_rezip_unidad_salida.txt`) |
| Reproducción con las pruebas reales en «otro entorno» provocado | revisión interna (scratchpad propio) | batería de la 4.10: 73/74, con el fallo y el mensaje de la revisión externa; batería de la 4.10.1: 78/78 |

## 2. Ensayo 2025

| Prueba | Resultado |
|---|---|
| Pipeline, pasos 0–14 (`resultados/pipeline_0*.txt`) | relevos con código 10 en los pasos 5, 6, 8, 10 (dos turnos) y 13; fin en el paso 14 con código 0: concluido · APROBADO |
| Verificación del paso 12 (`verificar_todo.sh`) | libro final ÍNTEGRO, 0 fallos, 0 avisos; acreditado |
| Fases: esquema, citas y gramática (por los agentes y por el pipeline) | fase A VÁLIDO y citas PASS; fase B gramática 0, VÁLIDO, citas PASS; fase C turno 1 y 2 VÁLIDO, citas PASS |
| Auditoría interna (H2) | APROBADO, 16/16 en PASA, ligada a SA-433ea31c3f7fc4bd y e60b272b654aeece |
| `concordancia_2025.py` (libro de datos y evaluado) | CONCUERDA; 0 residuos como datos del caso; 0 migrados que prevalezcan sin declararse; 17 y 15 textos heredados identificados |
| `comparar_con_C1.py` | C1 reproducido (70,4665 / 65,6645); el ensayo reproduce `resultados.json`; entrada 0 €, juicio +1,198487 € de ponderado, precisión de C46/C47 0 € |
| Vigencia (`motivo_vigencia`, `motivo_acreditacion_libro`) | sin motivo: salidas oficiales vigentes y libro acreditado |

## 3. Paquete

| Prueba | Dónde | Resultado |
|---|---|---|
| `bash verificar_paquete.sh completa` | copia limpia del candidato (4.10 limpia + cambios de la 4.10.1), 11/12-nov | **PASA**, código 0: manifiesto 2.193, entorno y piloto 35, 114/114, 30/30, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45, cierre 55/55 (10 min 48 s) |
| Controles de las entregas (tablas 1–3 de `resultados/LEEME_BATERIAS_HISTORICAS.md`) | misma copia, después | tabla 1 idéntica a sus referencias; tabla 2 y 3 con los recuentos del LEEME; 4.7–4.8.1 y las dos comparaciones, idénticas byte a byte a las del árbol 4.10; 4.9, los mismos 4 casos; 4.10, 41 de 44 por los 3 casos explicados |
| Control de la 4.10.1 | primer candidato | 42 de 43: el caso de la auditoría fallaba por un error del propio control (comparaba el primer carácter del veredicto); corregido, sin cambiar la exigencia. Su salida de referencia es la del candidato corregido |
| Manifiesto después de los controles | misma copia | 2.193 · 0 modificados · 0 ausentes · 0 de más (fuera de `personaje_v2/pruebas/` y `personaje_v2/.lo_perfil/`) |
| ZIP final: construcción, doble extracción, verificación completa y controles sobre su descompresión | ver el registro externo | — |

## 4. Revisión interna

`revision_interna/REVISION_INTERNA_4_10_1.md`: agente de revisión de Claude con contexto separado, que no participó en el trabajo (11-nov, 23:13–23:45). Veredicto: T-1 correcto; expediente con recorrido legítimo y conclusión coherente. Hallazgos H-1 (media), H-2 y H-3 (bajas), atendidos como dice `REGISTRO_ENTREGA_4.10.1.md` §4. No es la revisión externa.

## 5. Límites

- Todo se ejecutó en el entorno de Claude. El «otro entorno» de T-1 es una simulación (bytes distintos e inocuos), no otra máquina.
- La auditoría del expediente y la revisión interna son internas.
- Los resultados financieros son los del ensayo con una configuración exploratoria no adoptada.
