# Cambio de base económica · Zoetis · base 2025-12-31

Ejercicio 2025 de Zoetis (cerrado el 31-dic-2025), la misma base y las mismas entradas declaradas que zoetis_t1b (primer tiempo: nada publicado después del 9-oct-2026). Cambios: la fila 23 de la Historia solo con el pasivo por arrendamientos financieros (y la fila 22 sin él, para no contarlo dos veces), la fila 17 de 2025 con el principal financiero publicado (2), la declaración F1 con US GAAP y, como fuentes del primer tiempo, los documentos de resultados del T2 2026 publicados el 6-ago-2026 (guía 2026).

- Origen `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1b/Zoetis` (sin cambios) → expediente nuevo `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1c/Zoetis`; 42 archivos heredados en `antecedentes/heredados/` con inventario.
- Etapa 1: original en `antecedentes/etapa1_original/Zoetis_evaluada.xlsx` (SHA-256 `8f0c349503bdc296…`); copia de ensayo `8f0c349503bdc296…`, cambian .
- Valores de dato vaciados en la copia (los da la fase 1): ninguno.
- Evidencia activa reescrita (Control maestro): 0 celdas en 0 filas — . Los textos anteriores están en `antecedentes/evidencia_anterior.json`.
- Entradas sustituidas en fase1_v63.json: 
- Correcciones de extracción en fase1_partes (antes de construir la Historia; originales en `antecedentes/fase1_partes_original/`): ninguna
- Notas retiradas de los metadatos y de fase1_v63.json: 0 (`antecedentes/notas_retiradas.json`).
- Fechas: ejecución 2026-10-09 (real) · base 2025-12-31 · precio 2026-10-08 · acciones 2025-12-31 · fuentes: Form 10-K 2016–2025 y 10-Q T1/T2 2026 de Zoetis (FUENTES.tsv; Release fuentes-examen-20261118); 10-K 2020–2024 en texto por OCR (zoetis_t1/ocr_400dpi/LEEME.md). Corte del primer tiempo: nada publicado después del 9-oct-2026; fecha de análisis = 2026-10-09 (corte), como en zoetis_t1. Añadidos (decisión de la persona responsable, 18-nov-2026): comunicado, presentación y transcripción de la conferencia de resultados del T2 2026, publicados el 6-ago-2026 (Release fuentes-examen-20261118, anexo 2)..
- Configuración económica V6.4: no · alcance: sí.
- Entradas `analisis` heredadas de los metadatos del origen que se conservan: C46 (entrada de zoetis_t1b (cambio_zoetis_t1.json) sin cambio: la corrección de las filas 17, 22 y 23 y la declaración F1 no cambian C46); C47 (entrada de zoetis_t1b (cambio_zoetis_t1.json) sin cambio: la corrección de las filas 17, 22 y 23 y la declaración F1 no cambian C47); C50 (entrada de zoetis_t1b (cambio_zoetis_t1.json) sin cambio: la corrección de las filas 17, 22 y 23 y la declaración F1 no cambian C50); C49 (entrada de zoetis_t1b (cambio_zoetis_t1.json: 1,0 = media del principal de arrendamientos financieros 2 / 1 / —, 10-K 2025 PDF p. 89) sin cambio; la fila 17 corregida da la misma media) · que se descartan: ninguna.
- Entrada efectiva del FCF base: «estricta» (`entrada_efectiva.json`; expediente nuevo de la 4.15 (modo por defecto)).

## Adenda (orquestación, 19-nov-2026)

- Pipeline relanzado tras cerrar la fase C (17daaa5): consumió la fase C y se detuvo en el paso 12 como `no_entregable · fallo_de_implementacion` por la evaluación F1 con las palancas finales (F1-LIBRO, F1-REPLICA; `Zoetis/motor_a_f1_resultado.md`, `Zoetis/diagnostico.md`). El diagnóstico pide continuar desde el paso 2: no se hace sin decisión de la orquestación.
- `registro_entradas_zoetis_t1c.json` (guion `scripts/registro_entradas_zoetis_t1c.py`): `verificacion_entradas.json` del expediente a partir del registro de Mistral (`mistral/examen-zoetis-entradas` @ 790a8f0), adaptado a los valores y fuentes vigentes; fuentes de mercado de Mistral copiadas en `Zoetis/fuentes_mercado/` con sus huellas. Todas las comprobaciones pendientes de un revisor independiente. El paso 12 no ha evaluado aún el registro (la evaluación F1 bloquea antes).
