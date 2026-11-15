# Frente E · F1 · Elis · conciliación económica

Carpeta propia del frente económico. Solo contiene documentos y cálculos de contraste; no modifica el producto. **F1 sigue abierto.**

| Documento | Contenido |
|---|---|
| [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md) | Conciliación 2023–2025 y horizonte 2021–2025; puente del FCF base 307,933 a f y al motor A; arrendamientos; intangibles adquiridos y reinversión necesaria; impuestos; financiación; alternativas; decisiones pendientes |
| [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md) | Especificación propuesta para el frente técnico, con reglas de control y criterios de prueba. No adoptada |
| [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md) | Modelos, esfuerzo y separación de contextos según lo que expone el entorno |
| [revision/](revision/) | Estado de la revisión independiente; informe, scripts y salidas del revisor (copia sin cambios de su rama, con procedencia y huellas); respuesta del autor a cada objeción |
| `datos/fuentes.json` | Fuentes primarias con huella SHA-256, ruta en el árbol materializado y ejercicio de la publicación |
| `datos/cifras_fuente.csv` | 716 filas (677 cifras de tabla y 39 literales de texto) con documento, página PDF, literal impreso, signo, unidad, perímetro, edición («vigente» o «anterior»), período y modo de control del ejercicio |
| `scripts/verificar_cifras.py` | Verifica cada fila contra los bytes del PDF en cinco dimensiones, cada una OK, PENDIENTE (con motivo) o FALLO: literal (huella, página, etiqueta, posición, signo), ejercicio, unidad, perímetro y edición. Hoy: 702 OK, 14 PENDIENTE (unidad no impresa en URD 2022 p.302; filas que no usa ningún cálculo), 0 FALLO |
| `scripts/test_verificar_cifras.py` | 39 casos: 7 positivos reales y 32 contraejemplos, cada uno detectado en su dimensión. Incluye los mutantes conjuntos de posición y literal, año, unidad, perímetro y edición, y los M1–M4 del revisor |
| `scripts/especificacion_cifras.py` | Regenera el CSV desde los PDF, lo contrasta con la lectura del autor y se detiene si alguna dimensión falla |
| `scripts/contraste_f1.py` | Cálculo independiente con 236 comprobaciones: 136 contra el libro (18 sobre una copia recalculada con exceso de caja no nulo), 72 contra la fuente (71 residuos, cada uno con su cota de redondeo, y la doble vía del FCF base) y 28 algebraicas, que no prueban nada frente a datos externos. Solo usa cifras sin fallo, de la edición vigente, del grupo y con la unidad pedida |
| `scripts/test_contraste_residuos.py` | 7 casos: con el verificador saltado a propósito, los residuos hacen fallar el cálculo ante datos erróneos y la excepción fijada no absorbe errores nuevos |
| `scripts/prueba_caja_no_nula.py` | Recalcula con LibreOffice una copia temporal del libro con exceso de caja 0, 250 y −80 para la identidad del flujo sin crecimiento (revisión, O15) |
| `scripts/tabla_conciliacion.py` | Genera la tabla de conciliación con literal y página |
| `resultados/` | Salidas reproducibles de los scripts |
| `evidencias/paginas/` | Texto de las páginas citadas, con la huella del PDF de origen. La evidencia primaria es el PDF |
| `evidencias/preparacion/` | Informes de la preparación: descarga y verificación de la base 4.14, copia de binarios al árbol del hito 4.15, verificación de su manifiesto e inventario de los PDF de Elis |
| `MANIFIESTO_SHA256.txt` | SHA-256 de cada archivo versionado de esta carpeta, salvo el propio manifiesto. Se comprueba desde esta carpeta con `sha256sum -c MANIFIESTO_SHA256.txt` |

Base congelada del producto: `revision/4.15-hito1` (059f4f68dca7acf465b5f5b21de2dede84c885ff). Binarios de la Release `base-4.14` (ZIP SHA-256 `bb51942c…b97b93e`). Libro de Elis `d2593777…92385`, idéntico en 4.14 y 4.15. Reproducción: informe, §13.
