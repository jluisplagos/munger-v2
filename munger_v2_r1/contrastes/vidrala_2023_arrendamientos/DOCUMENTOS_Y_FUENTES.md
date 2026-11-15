# Documentos y fuentes · contraste 2023 y arrendamientos (entrega 4.2)

Todas las descargas son **nuevas**: se recuperaron el 8-nov-2026, después de las 20:25 (Europa/Ámsterdam), desde el centro de resultados de Vidrala:
- inglés: <https://www.vidrala.com/en/investors/results-centre/>;
- español: <https://www.vidrala.com/es/inversores/centro-de-resultados/>.

Se usó el navegador integrado de la aplicación de escritorio, porque el entorno de trabajo no puede conectarse a vidrala.com. Cada archivo se trasladó por tramos y se reconstruyó, y su SHA-256 coincide con el calculado en el navegador.

Las rutas son relativas a `contrastes/vidrala_2023_arrendamientos/`.

## Tres cosas distintas

| | `CF_2024.txt` (fuente de los datos de 2023 en el sistema) | `CF_2023.txt` |
|---|---|---|
| **Identidad del archivo original** | **No comprobable.** No está en el paquete ni registra huella | **No comprobable,** por la misma razón |
| **Correspondencia del contenido citado** | 49 de las 51 líneas de `AR_2024.json` están en su página del texto nuevo D8, con los espacios normalizados. Las otras 2 (D&A) están en la p. 7 y no en la p. 4 citada. Ninguna línea coincide carácter a carácter, porque las líneas del JSON van con los espacios normalizados | 56 de 56 líneas de `AR_2023.json` en su página del texto nuevo D10, con los espacios normalizados |
| **Evidencia nueva** | D7 (PDF inglés 2024) y D9 (PDF español 2024, que prevalece) | D6 (PDF inglés 2023) |

`comprobar-anio` sobre una copia, con los textos nuevos:
- **2023:** solo rechaza ceros heredados sin cita (adquisiciones, intereses de financiación, otros activos financieros y minoritarios).
- **2024:** rechaza los mismos ceros heredados más las dos líneas de D&A con la página mal atribuida.

## Documentos utilizados

| # | Documento · ejercicio | Procedencia (URL) | Idioma | Tamaño | Ruta | SHA-256 |
|---|---|---|---|---|---|---|
| D6 | *Vidrala, S.A. and Subsidiaries · Consolidated Annual Accounts 31 December 2023*. 79 páginas; creado el 12-mar-2024; servidor: 14-jun-2024 | <https://www.vidrala.com/default/documentos/1831_en-2023_consolidated_financial_information.pdf> | Inglés (traducción libre) | 1.031.910 B | `fuentes/en_1831_descarga_2026-11-08/1831_en-2023_consolidated_financial_information.pdf` | `8f88818c624bc253d99ca92eed47dc1639bd77e1d76ba7924fcb5fb89aab195d` |
| D7 | *… Consolidated Annual Accounts 31 December 2024*. 85 páginas; creado el 13-mar-2025; servidor: 14-abr-2025 | <https://www.vidrala.com/default/documentos/2145_en-2024_consolidated_financial_information.pdf> | Inglés (traducción libre) | 1.745.352 B | `fuentes/en_2145_descarga_2026-11-08/2145_en-2024_consolidated_financial_information.pdf` | `c2d4c12ea89ad43896b05f2645c289bf4d37fb9ef0ee98c10aa9836c0b4f1325` |
| D9 | *Vidrala, S.A. y Sociedades Dependientes · Cuentas Anuales Consolidadas 31-dic-2024*. 389 páginas; creado el 27-feb-2025; servidor: 14-abr-2025 | <https://www.vidrala.com/default/documentos/2118_es-informacion_financiera_consolidada_2024.pdf> | **Español (prevalece)** | 7.077.560 B | `fuentes/es_2118_descarga_2026-11-08/2118_es-informacion_financiera_consolidada_2024.pdf` | `365eea9eb1238ea2536a4e3c465c61401bfd9ce01c34ce9fca50235d9b7e7dcf` |
| D8 | `CF_2024_EXTRACCION_NUEVA.txt` (de D7) | Extracción nueva con `personaje_v2/scripts/pdf_a_texto.py` (pdftotext 24.02.0 `-layout`) | Inglés | — | `textos_nuevos/` | `fd37a10ecd5933b3bd6fb9355923d07be1e0190caad98fc715abb1233f3b7f7f` |
| D10 | `CF_2023_EXTRACCION_NUEVA.txt` (de D6) | Igual | Inglés | — | `textos_nuevos/` | `8fbc85ec5aa773c7129d86af84e11a9323eaa82b40d3090be66c5a0db44962b0` |
| D11 | `CF_2024_ES_EXTRACCION_NUEVA.txt` (de D9) | Igual | Español | — | `textos_nuevos/` | `39a91c9cc9c68f447d9227238a6cd90299774b48fb68ea6e622782fdb00b526d` |
| D12 | ESEF consolidado 2025: ZIP oficial de 35.979.149 B, SHA-256 `14264d1f…1c7bde90`. Incluye el XHTML español de 53.736.635 B, SHA-256 `fa161d64…cade343536` | <https://www.vidrala.com/default/documentos/2311_en-2025_esef_consolidated_information.zip> | Español (XHTML) | ver la columna anterior | `fuentes/esef_2311_extracto/`: (a) `esef_2025_hechos_numericos.json`, con los 378 hechos numéricos, los contextos y la huella de cada miembro del ZIP; (b) `taxonomia/`, con los 8 archivos pequeños del ZIP **completos**, cuyas huellas coinciden con las del JSON | JSON: `289627f36e898fbbdaa0faae28c3972660ab3297890cc30e14e338890f1518f5` |
| — | Del piloto (sin cambios): D1 (PDF inglés 2025), D2 (texto nuevo CF_2025), D3 (PDF español 2025) | `contrastes/piloto_Vidrala_2025/fuentes/` | | | | Ver el piloto |

**Desviación declarada (D12).** El ZIP del ESEF (36 MB) y su XHTML (54 MB) **no se conservan completos**: su traslado por el canal del navegador habría requerido unos 190 tramos.
- **Qué se conserva:** su URL; la huella del ZIP y de cada miembro; los archivos de taxonomía completos; y todos los hechos numéricos extraídos (378, de 112 conceptos).
- **Para qué se usó:** solo para comprobar qué etiquetas usa la empresa. Las conclusiones dependen únicamente de los hechos conservados.
- **Si hace falta el original:** se puede descargar de la URL y comprobar con su huella.

## Fuentes identificadas y no utilizadas

| Documento | URL | Tamaño · SHA-256 | Por qué no se usó |
|---|---|---|---|
| Cuentas consolidadas 2023 en español (doc. 1809) | <https://www.vidrala.com/default/documentos/1809_es-informacion_financiera_consolidada_2023.pdf> | 21.589.690 B · `59b51d0474aa946ffd7985955c1fdf4ec0be360e72fcadbfe3c998fa58b67de8` | El estado de flujos inglés de 2023 cuadra internamente y coincide con el comparativo español de 2024 en todas las líneas que no reexpresa. Se usarían si la persona responsable quiere contrastar también la traducción de 2023 (son 116 tramos) |
| ESEF consolidado 2024 (doc. 2129) | <https://www.vidrala.com/default/documentos/2129_en-2024_esef_consolidated_information.zip> | 71.889.840 B · `051de4e2df2589be53b8db629c354fe10f417ac98919fb3b23fc1699b083b169` | No consultado. El ESEF 2025 mostró que las notas solo se etiquetan en bloques de texto, y no se espera más desglose |

## Fuentes ausentes

| Falta | Qué impide |
|---|---|
| `CF_2023.txt` y `CF_2024.txt` originales | Comprobar la identidad byte a byte de las fuentes usadas en la extracción |
| Desglose del principal y del interés pagado por arrendamientos, y de su línea en el estado de flujos (no está en D6, D7, D9, D1, D3 ni D12) | Acreditar el tratamiento de C49 |
| Variación del circulante de 2023 solo de las operaciones continuadas (no se publica) | Un circulante de 2023 con el mismo perímetro que ventas, EBIT y D&A |
