# Cambio de base económica · Jumbo · base 2025-12-31

Ejercicio 2025 de Jumbo S.A., la misma base y las mismas entradas que jumbo_d (J1–J3, precio verificado 27,28 €, P-O2 (a)). Único cambio: la declaración F1 del motor A en el formato del código integrado (escala «unidades», PPA con «cero_comprobado» pendiente de revisor, serie de intereses de arrendamiento para P-FOSO (a) y la nota de texto fuera de «series»).

- Origen `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/jumbo_d/Jumbo` (sin cambios) → expediente nuevo `personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/jumbo_e/Jumbo`; 21 archivos heredados en `antecedentes/heredados/` con inventario.
- Etapa 1: original en `antecedentes/etapa1_original/Jumbo_evaluada.xlsx` (SHA-256 `53f3a20e19bbd0bc…`); copia de ensayo `53f3a20e19bbd0bc…`, cambian .
- Valores de dato vaciados en la copia (los da la fase 1): ninguno.
- Evidencia activa reescrita (Control maestro): 0 celdas en 0 filas — . Los textos anteriores están en `antecedentes/evidencia_anterior.json`.
- Entradas sustituidas en fase1_v63.json: 
- Correcciones de extracción en fase1_partes (antes de construir la Historia; originales en `antecedentes/fase1_partes_original/`): ninguna
- Notas retiradas de los metadatos y de fase1_v63.json: 0 (`antecedentes/notas_retiradas.json`).
- Fechas: ejecución 2026-11-18 (real) · base 2025-12-31 · precio 2026-11-17 · acciones 2025-12-31 · fuentes: Informes anuales oficiales 2016/17–2025 y semestral H1 2026 de Jumbo S.A. (FUENTES.tsv; Release fuentes-examen-20261118). Precio: página oficial de Euronext Athens leída por la persona responsable el 18-nov-2026 (coordinacion/cierre_v2/examen/precios/JUMBO_BELA_20261118.md). Tasa sin riesgo del agente de metadatos (buscador)..
- Configuración económica V6.4: no · alcance: sí.
- Entradas `analisis` heredadas de los metadatos del origen que se conservan: C46 (entrada de jumbo_d (= jumbo_c, cambio_jumbo_c.json) sin cambio: la declaración F1 no cambia las entradas registradas del FCF base); C47 (entrada de jumbo_d (= jumbo_c, cambio_jumbo_c.json) sin cambio: la declaración F1 no cambia las entradas registradas del FCF base); C48 (entrada de jumbo_d (= jumbo_c, cambio_jumbo_c.json) sin cambio: la declaración F1 no cambia las entradas registradas del FCF base); C49 (entrada de jumbo_d (= jumbo_c, cambio_jumbo_c.json) sin cambio: la declaración F1 no cambia las entradas registradas del FCF base); C50 (entrada de jumbo_d (= jumbo_c, cambio_jumbo_c.json) sin cambio: la declaración F1 no cambia las entradas registradas del FCF base) · que se descartan: ninguna.
- Entrada efectiva del FCF base: «estricta» (`entrada_efectiva.json`; expediente nuevo de la 4.15 (modo por defecto)).

## Adenda (orquestación, 18-nov-2026, después de la preparación)

La línea «Correcciones de extracción en fase1_partes … ninguna» describe solo la preparación con `cambiar_base.py`. Después se aplicaron, con su rastro:
- `declaracion_f1_jumbo_e.json` y `declaracion_f1_jumbo_e_r3.json`: declaración F1 (`motor_a_f1.json`) en el formato integrado y motivo de la PPA de 2023 (NIVAMO).
- `correccion_fase1_partes_r2.json`: J3 en la columna 2019 de AR2020 p. 59 y citas de ceros (originales en `antecedentes/fase1_partes_antes_de_r2/`).
- `correccion_fase1_partes_r3.json`: adquisiciones 2019 y 2021 de vuelta a cero pendiente; citas del bloque de financiación en 2016 y 2018 (originales en `antecedentes/fase1_partes_antes_de_r3/`).
- `recalculo_C42.json`: C42 con el precio activo (copia anterior en `antecedentes/etapa1_antes_de_C42/`).
- `entradas_r3.json` y `entradas_r3_registro.json`: C40, C96, notas de C42 y C88 (copia anterior en `antecedentes/entradas_antes_de_r3/`).
- `relevo_extraccion_jumbo_e_r2.json` y los relevos de extracción posteriores.
- `registro_entradas_jumbo_e.json` (guion `scripts/registro_entradas_jumbo_e.py`, 19-nov-2026): `verificacion_entradas.json` del expediente a partir del registro de Mistral (`mistral/examen-jumbo-entradas` @ fced486), adaptado a los valores y fuentes vigentes; fuentes de mercado de Mistral copiadas en `Jumbo/fuentes_mercado/` con sus huellas. Todas las comprobaciones pendientes de un revisor independiente.
