# Índice de la evidencia de preparación

Informes de la preparación mecánica del 15-nov-2026, copiados sin cambios (`cp --preserve=timestamps` y comprobados con `cmp`) desde el directorio de trabajo externo `/home/user/e_work`, que no está en el repositorio.

Las rutas que citan `PREPARACION.md` y `preparacion.json` (`inventario/…`, `textos_pdf/…`, `scripts/…`) son relativas a `/home/user/e_work`, no a esta carpeta.

## Archivos copiados

| Archivo copiado | Origen | SHA-256 |
|---|---|---|
| `PREPARACION.md` | `/home/user/e_work/inventario/PREPARACION.md` | `098798c54f56fb741bfc2078488bbf78b996fb7a3097daab758e86a56529ce85` |
| `preparacion.json` | `/home/user/e_work/inventario/preparacion.json` | `7a31775e0ee9f0322e46e26e63b0e12f16d6f82c75da579168b8ccecd85a7c19` |
| `VERIFICACION_BASE_COMPLETA_LOCAL_414.json` | `/home/user/e_work/inventario/VERIFICACION_BASE_COMPLETA_LOCAL_414.json` | `ca941787af3e41d45ff01a3a08db8514a6c112b90212da08553fbf0d3fc3a83f` |
| `log_base414.txt` | `/home/user/e_work/inventario/log_base414.txt` | `53c82e93cc2c0d74f1bcbc0937328efe9476bda944d8dbbd7518b1ca868b5944` |
| `copia_binarios_A_a_B.json` | `/home/user/e_work/inventario/copia_binarios_A_a_B.json` | `99b21958849216698c1a888702016163c0013d3b28c4e30e5849d9ffe17ff21e` |
| `inventario_pdf_elis.json` | `/home/user/e_work/inventario/inventario_pdf_elis.json` | `d2b38e111fc0c241aff8a7418e2a2c9e3821f091f83852248f57a5a3b7e4eedd` |
| `B_manifiesto_ausentes.txt` | `/home/user/e_work/inventario/B_manifiesto_ausentes.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `B_presentes_fuera_manifiesto.txt` | `/home/user/e_work/inventario/B_presentes_fuera_manifiesto.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `log_descarga_intento1.txt` | `/home/user/e_work/inventario/log_descarga_intento1.txt` | `2bf76b478920b663e57e1a18d82efe951684e988360de78f68df6801709d1769` |
| `log_descarga_intento2.txt` | `/home/user/e_work/inventario/log_descarga_intento2.txt` | `2bf76b478920b663e57e1a18d82efe951684e988360de78f68df6801709d1769` |
| `log_descarga_intento3.txt` | `/home/user/e_work/inventario/log_descarga_intento3.txt` | `2bf76b478920b663e57e1a18d82efe951684e988360de78f68df6801709d1769` |
| `log_descarga_intento4.txt` | `/home/user/e_work/inventario/log_descarga_intento4.txt` | `2bf76b478920b663e57e1a18d82efe951684e988360de78f68df6801709d1769` |
| `log_descarga_rest_intento1.txt` | `/home/user/e_work/inventario/log_descarga_rest_intento1.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `log_verif_B_quiet.txt` | `/home/user/e_work/inventario/log_verif_B_quiet.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| `INDICE_textos_pdf.json` | `/home/user/e_work/textos_pdf/INDICE.json` | `2d48f878723b51eb13366fc340f5607e63f6169c438974063552d45bcb2b270f` |
| `scripts/copiar_binarios_a_b.py` | `/home/user/e_work/scripts/copiar_binarios_a_b.py` | `0107a4d76a81c727b8706c9566ac94472a6071bc46e06652afa6d753c916f689` |
| `scripts/informe_preparacion.py` | `/home/user/e_work/scripts/informe_preparacion.py` | `5b757d0025634dbf61177709deb3d600d6d596d77137cfb7b844bc7e92bfe39d` |
| `scripts/inventario_pdf_elis.py` | `/home/user/e_work/scripts/inventario_pdf_elis.py` | `12648dde6078263c03602262e89896f41d2eb3cfc245dd12a11c5308e2ee1cf3` |

`B_manifiesto_ausentes.txt`, `B_presentes_fuera_manifiesto.txt`, `log_descarga_rest_intento1.txt` y `log_verif_B_quiet.txt` están vacíos (0 bytes) en el origen y se copian igualmente.

## Archivos no copiados (voluminosos)

| Archivo (en `/home/user/e_work/inventario/`) | SHA-256 | Bytes | Líneas |
|---|---|---|---|
| `B_rutas_manifiesto.txt` | `9f49ee4ed6955c474aea3efc0f438f5bdfd2dc8ecfe0b0f0686a1bda3a8be7b6` | 799143 | 7004 |
| `B_rutas_presentes.txt` | `9f49ee4ed6955c474aea3efc0f438f5bdfd2dc8ecfe0b0f0686a1bda3a8be7b6` | 799143 | 7004 |
| `log_verif_B_completo.txt` | `6d50af43d60f44cab363bc3966237b3f47999e453f8a8bdc66c1b43d4d920b16` | 827159 | 7004 |

En `log_verif_B_completo.txt`, 7004 líneas acaban en «: OK» y 0 no.

## Textos de los PDF

Los textos por página completos (`/home/user/e_work/textos_pdf/<slug>/pNNNN.txt`) no se copian; tampoco los textos completos por documento (`/home/user/e_work/textos_pdf/_completos/<slug>.txt`). Las páginas citadas están en `../paginas/` y se regeneran con `--exportar-paginas` de `verificar_cifras.py` (en `../../scripts/`, no en `scripts/` de esta carpeta).
