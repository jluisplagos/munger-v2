# Documentos y fuentes · revisión financiera del piloto Vidrala (entrega 4.3; ampliado en la 4.3.1)

## 1. Fuente nueva conservada en esta entrega

**ESEF 2025 completo (doc. 2311).**
- Ruta: `fuentes/esef_2025_completo/2311_en-2025_esef_consolidated_information.zip`.
- URL: `https://www.vidrala.com/default/documentos/2311_en-2025_esef_consolidated_information.zip`.
- Tamaño: 35.979.149 bytes.
- SHA-256: `14264d1f0a07f1bc3c7273450e393ddbe0587855293b487447319dcd1c7bde90`. Coincide con la huella comprobada independientemente que cita el encargo.

**Cómo se obtuvo.**
- Se descargó con `fetch` en el navegador integrado desde vidrala.com.
- La huella se calculó en el navegador.
- Se trasladó en base64 por tramos de 800.000 caracteres y se reconstruyó.
- La huella se comprobó de nuevo tras reconstruirlo y al incorporarlo al paquete.
- Es el mismo procedimiento del piloto (`contrastes/piloto_Vidrala_2025/ANEXO_REPRODUCIBLE.md`, §1).

**Miembros del ZIP** (bytes y SHA-256):

| Miembro | Bytes | SHA-256 |
|---|---|---|
| `reports/…-2025-12-31-1-es.xhtml` | 53.736.635 | `fa161d64dc802f3fd516424c94898b8c6245e93779a22ece34b2a9cade343536` |
| `…_pre.xml` | 189.615 | `04bea85668e1812c22da02b4716cfb20b211cd79ce5f656482705137d12cc297` |
| `…_def.xml` | 184.870 | `a489c7eac4c89cfaa08cac14895ef117f97cdde499f82eb4f93e65106e033ffb` |
| `…_lab-es.xml` | 36.009 | `5a427c1aa908d6a606b8ae60c4f76afff375c4c9067997925f3b504f3e05f705` |
| `…_cal.xml` | 70.886 | `26e111e002912fafcc1b805be720fb926a76a65d6944c10400dc5d20a143d521` |
| `….xsd` | 12.651 | `2fbeca6fcbd49f74415b8f9eab00655ec730c84d5eb1e958d9b216fe4ce4bde2` |
| `META-INF/catalog.xml` | 375 | `509def98ee631db2c819532bbde8c74236e4d760b693509190dd5586a58c6c70` |
| `META-INF/taxonomyPackage.xml` | 624 | `8a939a9c0281bc14da8227b6c14cdff9bf689b8b0733c08cf5c8524ccd8d801e` |
| `META-INF/reportPackage.json` | 77 | `e1a3ea1a579d96b51e829cacdcdefe23e6b9d7a528ae3a4319903ffa20047283` |

**Contenido.**
- El XHTML es el informe consolidado de 2025 **en español** (versión original, que prevalece), con las etiquetas en línea.
- Lo que se ha usado:
  - los 282 hechos numéricos sin dimensión de 2024 y 2025;
  - el texto de la nota 5 (plusvalía de 50 millones y resultado de Italia del primer semestre de 2024);
  - el texto del informe de gestión («perímetro comparable… ajustado por la contribución de Italia… y por la plusvalía contable»).
- Se lee con `zipfile`, sin descomprimirlo en disco.
- El extracto de la 4.2 (`contrastes/vidrala_2023_arrendamientos/fuentes/esef_2311_extracto/`) se conserva sin cambios.

## 1 bis. Fuente nueva de la entrega 4.3.1

**BORME núm. 208, 28-oct-2026, anuncio 5696** (aumento de capital liberado de Vidrala, S.A.).
- Ruta: `fuentes/borme_2026_5696/BORME-C-2026-5696.pdf`.
- URL: `https://www.boe.es/borme/dias/2026/10/28/pdfs/BORME-C-2026-5696.pdf`.
- Tamaño: 198.261 bytes.
- SHA-256: `59ec693b4aa943736d4433d74cdfe2d4b9bd8fea4a42f1f58ff28ab21db6394c`.
- Texto convertido con `personaje_v2/scripts/pdf_a_texto.py`: `BORME-C-2026-5696_texto.txt`, SHA-256 `4c90c93be02c836b3073677dc922f648f193060ed0d52f59e6cf3448cb7e1f81`.

**Cómo se obtuvo.**
- La terminal no llega al sitio (403 del proxy).
- Se descargó con `fetch` en el navegador integrado y se calculó la huella en el navegador.
- Se trasladó en base64 y se comprobó la huella tras reconstruirlo.

**Motivo.** Resolver una cuestión concreta de la subsanación: si la liberada de 2026 se ejecutó antes de la fecha del precio. La localizó una búsqueda web; el resumen automático de la página no se usa como evidencia, solo el PDF conservado.

**Contenido usado:**
- fecha de publicación;
- acuerdo de la junta del 29-abr-2026;
- 1.760.312 acciones nuevas, una por cada veinte;
- período de asignación de catorce días naturales desde el día siguiente a la publicación;
- legitimados: titulares al cierre del día anterior.

**No conservadas e identificadas (ruta B):**
- el semestral 1S2026 (doc. 2487, URL en el Control maestro);
- el calendario oficial de la liberada;
- las comunicaciones de autocartera de 2026;
- el cierre oficial del 3-nov-2026.

## 2. Fuentes de entregas anteriores usadas aquí (sin cambios)

| Sigla | Documento | Texto usado | SHA-256 del texto |
|---|---|---|---|
| ES24 | Informe 2024, español (doc. 2118, D9), prevalece | `contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2024_ES_EXTRACCION_NUEVA.txt` | `39a91c9c…b526d` |
| EN24 | Informe 2024, inglés (doc. 2145, D7) | `…/textos_nuevos/CF_2024_EXTRACCION_NUEVA.txt` | `fd37a10e…7f7f` |
| EN23 | Informe 2023, inglés (doc. 1831, D6) | `…/textos_nuevos/CF_2023_EXTRACCION_NUEVA.txt` | `8fbc85ec…62b0` |
| EN25 | Informe 2025, inglés (doc. 2355, D1) | `contrastes/piloto_Vidrala_2025/fuentes/texto_nuevo_CF_2025/CF_2025_EXTRACCION_NUEVA.txt` | `ebfe0f35…a4e4` |

Los PDF de origen y sus huellas están en los `DOCUMENTOS_Y_FUENTES.md` del piloto y de la 4.2. El script comprueba las huellas completas de los cuatro textos.

## 3. Páginas citadas

| Documento | Páginas | Contenido |
|---|---|---|
| ES24 | 11 | Cuenta de resultados 2024 y 2023 reexpresado |
| ES24 | 14 | Estado de flujos 2024 y 2023 reexpresado |
| ES24 | 37 | Segmentos 2024, con columna «Italia» |
| ES24 | 42–43 | Venta de Italia, plusvalía, cuenta de Italia (1S 2024 y 2023), activos enajenados y flujos de Italia |
| ES24 | 69 | Impuesto corriente; diferencias permanentes por la exención de la plusvalía |
| EN23 | 4, 7 | Cuenta de resultados y estado de flujos de 2023 en su propio informe (con Italia) |
| EN23 | 30 | «Investments» de Italia en 2023 (4,315) |
| EN24 | 31 | La misma tabla geográfica, con 2023 reexpresado |
| EN25 | 2, 3 | Balance: caja; préstamos; sin línea de minoritarios |
| EN25 | 4, 7 | Cuenta de resultados y estado de flujos de 2025 y 2024 |
| EN25 | 27–29 | Segmentos 2025; reestructuración de Reino Unido; Vidroporto en 2023 |
| EN25 | 31 | Plusvalía de Italia (cita de `fase_a.md`) |
| EN25 | 52 | Nota 8: saldo de arrendamientos 49,300 |
| EN25 | 56 | Impuesto corriente y diferido |
| EN25 | 71–72 | Provisiones: derechos de emisión y personal |
| EN25 | 60–61, 64–65, 76, 78 | Acciones, autocartera y programa de recompra; dividendo a cuenta y complementario; media ponderada; hechos posteriores: Toro y Kristin (4.3.1) |

## 4. Del sistema (solo lectura)

- `personaje_v2/empresas_v2/Vidrala/Vidrala_v63_evaluada.xlsx`, SHA-256 `21c38671…1da07`. Solo valores en caché; el script comprueba que no cambia.
- `personaje_v2/personaje_munger_v2.md` (SHA-256 `df43573b…ab6c`), `fase_a.md`, `fase_b.md`, `fase_c.md` e `informe.md`. Solo lectura.
- `v6/docs/Convenciones_financieras_V6_3.md` (convenciones 4, 5, 7 y 10) y `v6/docs/Replica_independiente_V6_2.md` (advertencia sobre el perímetro de `f`).
- `personaje_v2/scripts/comprobar_gramatica.py`, línea 367: aviso A6, «f fuera de rango».
- `personaje_v2/empresas_v2/Vidrala/datos_v63.json` (Control maestro heredado), solo lectura, desde la 4.3.1. Se usan sus notas de C34, C37, C41, C53, C54 y C55 como **herencia no contrastada**.
