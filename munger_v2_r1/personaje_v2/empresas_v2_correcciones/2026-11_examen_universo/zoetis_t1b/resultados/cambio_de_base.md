# Cambio de base económica · Zoetis · base 2025-12-31

Ejercicio 2025 de Zoetis (cerrado el 31-dic-2025), la misma base que zoetis_t1 (primer tiempo: nada publicado después del 9-oct-2026). Resuelve la parada del modo estricto del paso 2: C46, C47 y C50 con su media exacta y cálculo declarado sobre el 10-K 2025 (precedente E1, supuesto de la orquestación), y C49 = 1,0 (principal de arrendamientos financieros publicado). P-O1 (c) sin efecto (US GAAP: cobros en el CFO); P-O2 (a): 424,928 M acciones a 31-dic-2025.

- Origen `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1/Zoetis` (sin cambios) → expediente nuevo `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1b/Zoetis`; 27 archivos heredados en `antecedentes/heredados/` con inventario.
- Etapa 1: original en `antecedentes/etapa1_original/Zoetis_evaluada.xlsx` (SHA-256 `c33f17d1583abaa0…`); copia de ensayo `8f0c349503bdc296…`, cambian xl/worksheets/sheet1.xml, xl/worksheets/sheet4.xml.
- Valores de dato vaciados en la copia (los da la fase 1): Análisis!C46, Análisis!C47, Análisis!C49, Análisis!C50.
- Evidencia activa reescrita (Control maestro): 6 celdas en 4 filas — Análisis!C46 (MN); Análisis!C47 (M); Análisis!C49 (MN); Análisis!C50 (M). Los textos anteriores están en `antecedentes/evidencia_anterior.json`.
- Entradas sustituidas en fase1_v63.json: C46 → 2736.667; C47 → 669.333; C49 → 1.0; C50 → 72.333
- Correcciones de extracción en fase1_partes (antes de construir la Historia; originales en `antecedentes/fase1_partes_original/`): ninguna
- Notas retiradas de los metadatos y de fase1_v63.json: 0 (`antecedentes/notas_retiradas.json`).
- Fechas: ejecución 2026-10-09 (real) · base 2025-12-31 · precio 2026-10-08 · acciones 2025-12-31 · fuentes: Form 10-K 2016–2025 y 10-Q T1/T2 2026 de Zoetis (FUENTES.tsv; Release fuentes-examen-20261118); 10-K 2020–2024 en texto por OCR (zoetis_t1/ocr_400dpi/LEEME.md). Corte del primer tiempo: nada publicado después del 9-oct-2026; fecha de análisis = 2026-10-09 (corte), como en zoetis_t1..
- Configuración económica V6.4: no · alcance: sí.
- Entradas `analisis` heredadas de los metadatos del origen que se conservan: ninguna · que se descartan: ninguna.
- Entrada efectiva del FCF base: «estricta» (`entrada_efectiva.json`; expediente nuevo de la 4.15 (modo por defecto)).
