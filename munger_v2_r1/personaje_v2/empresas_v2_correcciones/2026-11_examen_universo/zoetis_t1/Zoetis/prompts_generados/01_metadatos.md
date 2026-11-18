# Prompt del agente de METADATOS DE FASE 1 (modelo: Sonnet, esfuerzo medio, contexto limpio; necesita búsqueda web)

Recoges los datos de identificación y de mercado de Zoetis que la Plantilla V6.3 necesita además de la Historia. No juzgas ni valoras. Carpeta: `/home/user/e_work/wt_examen/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1/Zoetis`. Informes en `texto/` (marcas `[PDF PAGE n]`; ejercicios 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025). Nombres válidos de sector y de país/región: `fase1_listas.md`.

## Qué recoger (cada dato con su fuente; nada de memoria)
- `empresa` (razón social), `ticker` (bolsa principal), `fecha_analisis` (hoy, AAAA-MM-DD), `sector_texto` (una línea: qué vende), `moneda_modelo` (moneda de los estados), `norma_contable` ("IFRS" / "US GAAP" / …), `cierre_fiscal` (mes), `mercado` (bolsa), `ratio_adr` (null salvo ADR).
- `sector_damodaran`: el nombre EXACTO de `fase1_listas.md` que mejor describe el negocio principal.
- `precio`: `{"valor", "moneda_cotizacion", "fecha", "fx", "fx_fecha", "fuente"}`. Cotización con fecha y hora de una fuente web con nombre (bolsa principal si es posible). Si las fuentes discrepan, da la más reciente con hora y anota el rango visto en `fuente`. `fx` solo si la moneda de cotización difiere de `moneda_modelo` (tipo de cambio y fecha, con fuente).
- `acciones_diluidas`: `{"valor" (millones), "fecha", "fuente", "pagina"}`: **acciones en circulación al cierre del último ejercicio publicado** (emitidas menos autocartera, del balance o de la nota de capital), **no** la media ponderada del año; si hay instrumentos dilutivos materiales (opciones, convertibles), suma la dilución que publique la empresa al cierre y dilo en `fuente`. Escribe en `_notas` también la media diluida del año (nota de beneficio por acción) y la última cifra publicada después del cierre, con fecha, solo como información. Criterio de la persona responsable (P-O2, 18-nov-2026; D3 y E6): acciones al cierre de las cuentas.
- `capitalizacion`: `{"valor" (millones), "fecha", "fuente"}`: precio × acciones diluidas, salvo dato mejor con fuente.
- `tasa_sin_riesgo`: `{"valor", "fuente"}`: rentabilidad a 10 años del bono SIN riesgo de impago en la moneda del modelo, con fecha y fuente web: para el euro, el Bund alemán (no el bono del país de la empresa: su prima de riesgo país la suma la plantilla aparte, en «Riesgo país»); para el dólar, el Treasury; para otras monedas, el bono del Estado emisor (anota su rating).
- Fechas siempre `AAAA-MM-DD` (la hora, si la hay, va en `fuente`).
- `geografia`: hasta 6 filas `{"pais", "pct", "nota"}` con el reparto de ventas por ubicación del cliente del último informe; `pais` es un nombre EXACTO de `fase1_listas.md` (país, o «Región · …» para un grupo). Si una región del informe no encaja con ninguna, elige la más parecida y explícalo en `nota` (convención del ejercicio). Los `pct` suman 1 (±0,002).
- `geografia_fuente`: `{"fuente", "pagina"}` del reparto.
- `convenciones`: `{"caja_incluye_otros_activos_financieros": true|false, "motivo_caja": "..."}`. `true` solo si la empresa mantiene una parte material de su liquidez en depósitos a plazo u otras inversiones financieras corrientes líquidas (dilo con la cifra y la página); si no, `false`.
- `anios_fcf_base`: 3 (convención; la fase A puede cambiarlo).
- `_notas`: lista de frases con lo que no encontraste o las aproximaciones que hiciste.

## Salida: `/home/user/e_work/wt_examen/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_examen_universo/zoetis_t1/Zoetis/fase1_metadatos.json` (solo ese archivo)
Comprueba que es JSON válido (`python3 -m json.tool`). Mensaje final (≤ 6 líneas): precio y fuente, rf y fuente, sector elegido y por qué, aproximaciones de la geografía.
