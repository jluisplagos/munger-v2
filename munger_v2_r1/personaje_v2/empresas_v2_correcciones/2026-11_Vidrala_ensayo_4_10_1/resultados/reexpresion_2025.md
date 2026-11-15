# Preparación 2 del ensayo 2025 · reexpresión de los datos heredados a 31-dic-2025

(4.10.1, preparación 2) La revisión de la fase A (primera preparación) detectó que siete celdas de DATOS de Análisis heredadas de la etapa 1 (migración V5.3 → V6.3) estaban medidas a 30-jun-2026 o con EBITDA de los doce meses a 30-jun-2026 (IPP CNMV 1S2026), es decir, con operaciones de 2026 (emisión de 259,4 mm, recompras, dividendos, Chile). Con la base económica 2025 del encargo no se incorporan. Como rellenar_fase1_v63.py no pisa un valor migrado (regla de producción, sin cambios), la reexpresión se hace en la ENTRADA: una copia de ensayo de etapa1/Vidrala_evaluada.xlsx sin esos valores de dato ni sus filas de evidencia (Control maestro E:N), con el original conservado en antecedentes/etapa1_original/ con su huella; los juicios de la etapa 1 no se tocan. Los valores de 31-dic-2025 entran por fase1_v63.json → analisis (C24, C31, C34, C42, C53, C54) o los deriva rellenar_fase1_v63.py de la Historia (C33). Además se vacían las filas de evidencia de D4, C37 y C57 (su columna de periodo seguía diciendo 10/10/2026 y 09/10/2026); sus valores los fuerza la fase 1.

| Celda | Etapa 1 (30-jun-2026) | Ensayo (31-dic-2025) |
|---|---|---|
| Análisis!C24 | 0.13 | 0.1394 |
| Análisis!C31 | 'Sí' | 'Sí' |
| Análisis!C33 | 0.69 | 0.36 (derivada de la Historia) |
| Análisis!C34 | 'No' | 'Sí' |
| Análisis!C42 | 7.68 | 7.82 |
| Análisis!C53 | 109.4 | 108.352 |
| Análisis!C54 | 409.6 | 262.913 |

Filas de evidencia vaciadas en la copia de ensayo (Control maestro E:N): 20 (Análisis!D4), 29 (Análisis!C24), 34 (Análisis!C31), 36 (Análisis!C33), 37 (Análisis!C34), 38 (Análisis!C37), 42 (Análisis!C42), 50 (Análisis!C53), 51 (Análisis!C54), 54 (Análisis!C57).

Etapa 1 original: `antecedentes/etapa1_original/Vidrala_evaluada.xlsx` (SHA-256 `6aed21169576aa444a3b5d46a2c5906a7548e63ee45f23b9c60a78e4a22b2675`). Copia de ensayo: SHA-256 `d8c78658f5adf348f7d4a123df9013018326f9c12c748894409f644120396d12`; solo cambian xl/worksheets/sheet1.xml, xl/worksheets/sheet4.xml; ninguna otra celda cambia (comprobado).

Primera preparación archivada en `antecedentes/preparacion_1_datos_de_2026` (16 archivos, con INVENTARIO.json).

Se conserva `extracto_v63.md`: el extracto de la primera preparación no cita ninguna de las siete cifras ni datos de 2026 de la etapa 1 (comprobado por búsqueda: 409,6; 0,69; 109,4; 7,68; 30-jun-2026; 1S2026); se basa en los textos, que no cambian.

No se reexpresa: {"C38": "Valor intrínseco de fuente externa (Simply Wall St, 171,8, consultado el 08-oct-2026): dato de contexto de terceros con fecha anterior a la de análisis; no hay una valoración externa de cierre de 2025 en el paquete y no se fabrica. Se declara como posterior a la base.", "juicios heredados (C76, C97 y demás)": "los revisa la fase A con los datos reexpresados; no se tocan aquí."}
