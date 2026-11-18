# Cambio de base económica · Ahold · base 2025-12-28

Ejercicio 2025 de Ahold Delhaize (52 semanas, cerrado el 28-dic-2025), la misma base y las mismas entradas que ahold_f2 (P-O1 (c) y P-O2 (a)). Único cambio: la serie F1 de intereses de arrendamiento (series.intereses_arrendamiento) en motor_a_f1.json, que pide la vara del foso de P-FOSO (a) con F1 en A2_propio; las fases del personaje se repiten con el código integrado.

- Origen `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/ahold_f2/Ahold` (sin cambios) → expediente nuevo `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/ahold_f3/Ahold`; 47 archivos heredados en `antecedentes/heredados/` con inventario.
- Etapa 1: original en `antecedentes/etapa1_original/Ahold_evaluada.xlsx` (SHA-256 `bd09e74ee0744690…`); copia de ensayo `bd09e74ee0744690…`, cambian .
- Valores de dato vaciados en la copia (los da la fase 1): ninguno.
- Evidencia activa reescrita (Control maestro): 0 celdas en 0 filas — . Los textos anteriores están en `antecedentes/evidencia_anterior.json`.
- Entradas sustituidas en fase1_v63.json: 
- Correcciones de extracción en fase1_partes (antes de construir la Historia; originales en `antecedentes/fase1_partes_original/`): ninguna
- Notas retiradas de los metadatos y de fase1_v63.json: 0 (`antecedentes/notas_retiradas.json`).
- Fechas: ejecución 2026-11-18 (real) · base 2025-12-28 · precio 2026-11-13 · acciones 2025-12-28 · fuentes: Informes anuales 2016–2025 de Ahold Delhaize (páginas oficiales del emisor; huellas en INDICE_FUENTES.csv del repositorio auxiliar). Precio y tasa sin riesgo del agente de metadatos, pendientes de fuente oficial..
- Configuración económica V6.4: no · alcance: sí.
- Entradas `analisis` heredadas de los metadatos del origen que se conservan: C46 (entrada de ahold_f2 (cambio_ahold_po1_po2.json, P-O1 (c): media 2023–2025 de CFO + dividendos de negocios conjuntos, cálculo declarado) sin cambio: la serie de intereses de arrendamiento no cambia las entradas del FCF base); C47 (entrada de ahold_f2 (media exacta 2023–2025 declarada en ahold_4_15, precedente E1) sin cambio); C48 (entrada de ahold_f2 (cambio_ahold_po1_po2.json, P-O1 (c): media de intereses pagados − intereses cobrados, cálculo declarado) sin cambio: los intereses de arrendamiento no entran en C48 (van en C49)); C49 (entrada de ahold_f2 (cambio_ahold_po1_po2.json, P-O1 (c): media de pagos de arrendamientos − cobros de subarriendos, cálculo declarado) sin cambio) · que se descartan: ninguna.
- Entrada efectiva del FCF base: «estricta» (`entrada_efectiva.json`; expediente nuevo de la 4.15 (modo por defecto)).
