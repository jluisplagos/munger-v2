# Preparación del frente de auditoría económica (solo lectura)

Fecha: 2026-11-15. Raíz de trabajo: `/home/user/e_work`. El repositorio `/home/user/munger-v2` no se ha tocado: solo se ejecutaron `git worktree add --detach` y `git worktree list`. Detalle completo en `preparacion.json`.

| Paso | Estado | Dato clave |
|---|---|---|
| 1. Worktree A `wt_main414` | OK | HEAD d69d4837f0e99ce30f38d3461f15cceee9a58730 |
| 2. Descarga ZIP base-4.14 | OK, con desviación | `gh release download` falla (4 intentos, 403: GraphQL no disponible en la sesión). Se descargó el mismo asset (id 750814858) por la API REST (`gh api … releases/assets/750814858`). 1130912246 bytes; SHA-256 bb51942c…b97b93e, coincide. |
| 3. materialize + verify en A | OK | Códigos 0/0; 1008 recuperados; verified 6798/6798, missing 0, changed 0, complete true; manifiesto 028762e4…f848 coincide con baselines/4.14.json. Log: `log_base414.txt`. 0 archivos versionados modificados. |
| 4. Worktree B `wt_hito415` + binarios | OK | HEAD 059f4f68…5ff. Copiados 1008 binarios (release_asset), 0 ya existentes, 0 distintos, SHA-256 comprobado tras copiar. Manifiesto propio de B (línea 1 = cabecera): 7004 entradas, 7004 OK, 0 FAILED, 0 ausentes, 0 archivos fuera del manifiesto. `tools/base_414.py` no se ejecutó en B. |
| 5. Huellas xlsx Elis | OK | 12 xlsx (elis_decisiones y elis_motor_A); A y B idénticos. `Elis_v63_evaluada.xlsx` (elis_decisiones) = d2593777…9c92385, coincide. |
| 6. Inventario PDF fuentes Elis | OK | 14 PDF (10 en fuentes_pdf, 4 en fuentes_2026/pdf); todos coinciden con HUELLAS_PDF.txt / HUELLAS*.txt; URD2025 y DEU2024FR coinciden con las huellas del encargo; los 10 homónimos de elis_motor_A son idénticos; los PDF de B son idénticos a A. |
| 7. Texto por página | OK | 14/14 con páginas extraídas = pdfinfo. Índice: `textos_pdf/INDICE.json`. |

## Observaciones (sin interpretación económica)

- Tratamiento del salto de página final: pdftotext termina cada página con `\f`; el segmento vacío posterior al último `\f` se descartó en los 14 documentos y no cuenta como página.
- Páginas sin texto (posibles imágenes sin capa de texto): URD2018 (150, 164, 290, 306), URD2019 (143, 157, 259, 273), URD2021 (1, 20, 28, 42), URD2022 (20, 34, 52), URD2023 (45 páginas, sobre todo 2–56; además 130, 236, 258, 274, 380, 398), DEU2024FR (21: 1, 2, 4, 25–27, 44, 45, 48, 50, 52, 56, 58–60, 62, 154, 250, 268, 374, 400), URD2025 (11: 1, 4, 24, 44, 58, 62, 158, 304, 322, 434, 458). Sin páginas vacías: URD2016, URD2017, URD2020 y los 4 documentos de 2026.
- `fuentes_2026/HUELLAS_descarga_persona_responsable.txt` nombra `Elis_OCEANE_2029_ajuste_ratio.html` sin huella, y ese archivo no está en la carpeta (no es PDF; solo se registra).
- pdftotext emite avisos «Syntax Warning» sobre fuentes en varios documentos; código de salida 0 en todos.
- En A, la materialización deja los 1008 binarios como archivos no versionados (esperado); no hay cambios en archivos versionados de A ni de B.

## Archivos

- `inventario/preparacion.json`, `inventario/log_base414.txt`, `inventario/VERIFICACION_BASE_COMPLETA_LOCAL_414.json`
- `inventario/copia_binarios_A_a_B.json`, `inventario/log_verif_B_completo.txt`, `inventario/B_*.txt`
- `inventario/inventario_pdf_elis.json`, `textos_pdf/INDICE.json`, `textos_pdf/<slug>/pNNNN.txt`, `textos_pdf/_completos/<slug>.txt`
- Scripts: `scripts/copiar_binarios_a_b.py`, `scripts/inventario_pdf_elis.py`, `scripts/informe_preparacion.py`
