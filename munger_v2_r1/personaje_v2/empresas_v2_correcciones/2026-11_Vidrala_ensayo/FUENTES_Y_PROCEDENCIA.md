# Fuentes nuevas y procedencia (entrega 4.4, 9-nov-2026)

**Cómo se obtuvo cada fuente nueva:**
- La terminal no llega a esos sitios; se usó el navegador integrado de la aplicación de escritorio.
- Se descargó con `fetch` y se calculó la huella SHA-256 en el navegador.
- Se trasladó en base64 por tramos (de 800.000 caracteres como máximo) y se reconstruyó.
- La huella se comprobó tras reconstruir y otra vez en el script `scripts/comprobar_ensayo.py`, §1.

## 1. Cuentas consolidadas de 2016 a 2022 (`fuentes/cuentas_consolidadas_2016_2022/`)

**Origen:** centro de resultados de Vidrala, en inglés (`https://www.vidrala.com/en/investors/results-centre/`), enlaces «Consolidated financial information».

| Ejercicio | Archivo (URL `https://www.vidrala.com/default/documentos/<archivo>`) | Bytes | SHA-256 |
|---|---|---|---|
| 2016 | `1279_en-2016_consolidated_financial_information.pdf` | 1.062.656 | `53849fe52385ae7e62a0806bb4ba0e8f06c9fe0a6778cd335bd58b0e70940b7b` |
| 2017 | `1285_en-2017_consolidated_financial_information.pdf` | 1.882.943 | `da068c8b28642e59bfc498893b46b3a853a8a1c4707522d39fa4f4b5d4bac6ae` |
| 2018 | `1291_en-2018_consolidated_financial_information.pdf` | 2.875.699 | `907687f9e3f05df84099fdf84638ba64ea643373d8bd1958cba1af5732308492` |
| 2019 | `1297_en-2019_consolidated_financial_information.pdf` | 2.915.706 | `9c38b260482bb501673b0bb1a0382846405fb4d4ee636d668a4e5ed64814a6c3` |
| 2020 | `1304_en-2020_consolidated_financial_information.pdf` | 2.919.572 | `35264bc723624779682c504b9e7057f85aaf11b68600a7b351a128c08188b10e` |
| 2021 | `1413_en-2021_consolidated_financial_information.pdf` | 957.898 | `2b966a4188615e6dfce4ee1051c2314c5faec9c272f27ea4525763a5f3958494` |
| 2022 | `1668_en-2022_consolidated_financial_information.pdf` | 1.003.070 | `180b3608c7e910a8010018bb40b33f0808ff1247170acef38c783d65aeb8382b` |

**Nota.** El documento de 2016 enlazado como inglés («en») está en español. Los textos originales del expediente (`CF_2016.txt`) también lo estaban, porque sus citas en español pasan.

Para 2023, 2024 y 2025 se reutilizan los PDF ingleses conservados en entregas anteriores (docs. 1831, 2145 y 2355, en `contrastes/`).

## 2. Textos de `Vidrala/texto/` (nuevos; no idénticos acreditados a los originales ausentes)

**Cómo se generaron.** Con `personaje_v2/scripts/pdf_a_texto.py`, sin opciones: `pdftotext -layout` y marcas `[PDF PAGE n]`. El script de comprobación los vuelve a generar desde los PDF y verifica que coinciden byte a byte. Los de 2023, 2024 y 2025 coinciden con los textos nuevos de la 4.2 y del piloto.

**Relación con los originales.** Los `CF_*.txt` originales del expediente **no están en el paquete**. No se afirma que los nuevos sean idénticos byte a byte. Lo comprobado es más acotado:
- las **535 citas** (línea e importe) de los `AR_*.json` originales aparecen en la página citada de los textos nuevos;
- las únicas excepciones son las dos de D&A de 2024 (página 4 en lugar de 7, P8);
- `comprobar-anio` da OK en los diez años, con las versiones nuevas de los AR.

## 3. Comunicación del dividendo a cuenta (`fuentes/dividendo_2275/`)

| Campo | Valor |
|---|---|
| URL (dada por la persona responsable) | `https://www.vidrala.com/default/documentos/2275_es-otra_informacion_relevante.pdf` |
| Respuesta | 200, `application/pdf` |
| Bytes | 95.056 |
| SHA-256 | `cbaff23e640718620fd43e7dfb18e9222a4c90fb34e1ce684abdc9c6dc83e25e` |
| Procedencia | Dominio oficial de Vidrala; dirigida «A la Comisión Nacional del Mercado de Valores»; firmada por el secretario del consejo |
| Fecha y lugar | Llodio, 18-dic-2025 |

## 4. Comunicación de la ampliación liberada de 2026 (`fuentes/cnmv_liberada_2026/`)

| Campo | Valor |
|---|---|
| URL (dada por la persona responsable) | `https://www.cnmv.es/webservices/verdocumento/ver?t=%7B5b51ba57-6933-44f5-b47f-8a2e7fd53fed%7D` |
| Respuesta | 200, `application/pdf` |
| Bytes | 131.641 |
| SHA-256 | `3259cf30e9bb9985648c4abbd9e37c32b9cc37409cd946eaf140a17a9a93c29d` |
| Archivo conservado | `CNMV_OIR_Vidrala_ampliacion_liberada_2026_5b51ba57.pdf` |
| Procedencia | Servicio de documentos de la CNMV. Comunicación de otra información relevante de Vidrala con el informe del artículo 1.5(g) del Reglamento 2017/1129 |
| Fecha | Llodio, 20-oct-2026; metadatos del PDF: creado el 20-oct-2026 |
| Páginas | 5 |

**Relación con el BORME de la 4.3.1.** Es coherente con él: 1.760.312 acciones nuevas, el anuncio del 28-oct-2026 y el período de catorce días.

## 5. Discrepancia documental registrada

La fecha del consejo que aprobó el dividendo a cuenta no coincide entre los documentos:
- 17-dic-2025 según la comunicación 2275;
- 19-dic-2025 según las cuentas (EN25 p.64 y el ESEF en español).

No afecta al tratamiento: las dos fechas son anteriores al cierre.
