# Expediente exploratorio de la 4.10 (copia combinada C1 recorrida por el pipeline)

**Qué es.** Una copia del expediente de la 4.6.1 con dos cambios en `Vidrala/fase1_v63.json`, procedentes de la variante C1 de `../variantes/` y propuestos como D-N6 y D-N7, sin adoptar:
- E = 90,10 × 35,182858 = 3.169,975506, con fecha 31-dic-2025;
- N = 35,182858.

Además, `Vidrala/alcance_v2.json` declara el alcance exploratorio.

**Qué hizo el pipeline** (`python3 -B personaje_v2/scripts/pipeline.py …/Vidrala --desde 2`; salida en `../resultados/pipeline_exploratorio_salida.txt`):
- Archivó la aprobación heredada de la 4.6.1 en `historial_cierres/02_…`: «el material cambió … la aprobación no vale para la versión nueva».
- Ejecutó los pasos 2–4: rellenó el libro de datos con las entradas de C1, comprobó la entrada y volcó los datos.
- Se detuvo en el paso 5, con el código 10, esperando al agente de extracción (`ESPERANDO.md`).

**Archivos que todavía son de la 4.6.1** y no corresponden a las entradas de C1 hasta que se ejecuten los pasos 5–12:
- el libro evaluado, `Vidrala_v63_evaluada.xlsx`;
- `resultados.json`, `precio.json`, `referencias_mecanicas.json` y `gramatica.json`;
- las fases A, B y C y sus `.md`;
- `extracto_v63.md`, `ficha_provisional.json`, `informe_provisional.md`, los `verificacion_*.txt` y `LEEME_ANTES_DE_CONTINUAR.md`.

No son resultados de C1: los resultados mecánicos de C1 están en `../variantes/variantes_4_10.json` y en `../copia_combinada/`.

**Por qué se detiene aquí.** Es una decisión de alcance del encargo 4.10, no algo que impongan los datos. La fase C compararía la escalera con el precio de noviembre de 2026, y esa actualización queda fuera del encargo. Además, las entradas de C1 son propuestas sin adoptar. Seguir exige ejecutar los agentes de los pasos 5–10 y una auditoría nueva del material actual (paso 13).
