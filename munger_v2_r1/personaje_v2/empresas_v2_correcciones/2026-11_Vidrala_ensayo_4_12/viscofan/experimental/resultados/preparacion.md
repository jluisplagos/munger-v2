# Viscofan · preparación del expediente experimental (encargo 4.12 §8)

- Origen `personaje_v2/empresas_v2/Viscofan` (sin cambios) → `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/viscofan/experimental/Viscofan`. Entradas de partida copiadas: etapa1, fase1_v63.json, fase1_metadatos.json, fase1_fuentes.json, fase1_partes, fase1_listas.md.
- Único campo cambiado en las copias: `fecha_analisis` 2026-11-04 → 2026-11-12 (fecha real de ejecución) en fase1_v63.json y fase1_metadatos.json.
- texto/: 10 publicaciones recuperadas con su nombre propio: `texto/AR_2025.txt` (2025, SHA-256 `0c58cd37df86…`); `texto/CF_2024.txt` (2024, SHA-256 `01ab41285f06…`); `texto/CA_2023_es.txt` (2023, SHA-256 `15260cfcdd0a…`); `texto/CF_2022_compilacion.txt` (2022, SHA-256 `c154770c089a…`); `texto/CF_2021.txt` (2021, SHA-256 `40bf9969f25b…`); `texto/AR_2020.txt` (2020, SHA-256 `2ac223dcca45…`); `texto/AR_2019.txt` (2019, SHA-256 `7f5917e89359…`); `texto/IA_2018_es.txt` (2018, SHA-256 `267ebb36685a…`); `texto/AR_2017.txt` (2017, SHA-256 `844f922178af…`); `texto/IA_2016_es.txt` (2016, SHA-256 `34fca454bc36…`).
- Configuración: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/viscofan/configuracion/configuracion_economica_viscofan_experimental.json` (SHA-256 `6030330c79abd672…`): modo experimental · N1 0.221191 (escudo vinculado) · N2 vacío (Palancas C8) · R1 · P-M1 SR1 · Θ 0.5 · años Plana · terminal Proporcional a las ventas · cartera legado.
- Antecedentes (no son entradas del pipeline): `antecedentes/extracto_v63_origen.md`, para que la extracción lo reutilice y contraste.
- No se copia: libros V6.3, estado del pipeline, fases A–C, auditoría, ficha, informe y resumen del origen (el pipeline los genera de nuevo con agentes reales).

**Fechas, por separado:**

- base economica: 2025-12-31 (cuentas consolidadas de 2025)
- ejecucion: 2026-11-12
- precio: 54.7 € del 2026-11-03 (Bolsamania, cierre del 2026-11-03 17:35 (54,70 EUR, rango día 54,50-55,30). Otras fuentes más antiguas: Investing.com 54,00 EUR (2026-10-28), Google Finance 55,20 EUR (2026-10-23))
- acciones: 45.479209 millones, media ponderada diluida de 2025 (2025-12-31)
- tasa sin riesgo: 0.0335 (Bund alemán a 10 años, ~3,35% el 2026-11-04 por la mañana (Euronews 2026-11-04); Trading Economics ~3,3% (2026-11-03), Finimize 3,33%. Rating Alemania AAA)
- fuentes: publicaciones recuperadas el 2026-11-12 (copias de la carpeta de la persona responsable, en dos entregas: 20:38 y 21:59); el informe anual 2025 es un PDF creado el 25-mar-2026
- fecha analisis del origen: 2026-11-04

**Adenda.** 12-nov 22:12: se añaden a texto/ IA_2021_es.txt e IA_2023_es.txt (informes anuales en español con el informe de gestión), antes de dar por terminada la extracción, porque las cuentas recuperadas de 2021 y 2023 no traen los datos de mercado que citan los hechos del extracto anterior. preparar_viscofan_experimental.py ya los incluye: una preparación nueva da los mismos doce textos. Textos añadidos: `texto/IA_2021_es.txt` (2021, SHA-256 `47e472a600f4…`); `texto/IA_2023_es.txt` (2023, SHA-256 `e64be3a2f8c3…`).
