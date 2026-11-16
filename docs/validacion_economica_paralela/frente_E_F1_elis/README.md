# Frente E · F1 · Elis · conciliación económica

Carpeta propia del frente económico. Solo contiene documentos y cálculos de contraste; no modifica el producto. **F1 sigue abierto.**

| Documento | Contenido |
|---|---|
| [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md) | Conciliación 2023–2025 y horizonte 2021–2025; puente del FCF base 307,933 a f y al motor A; arrendamientos; intangibles adquiridos y reinversión necesaria; impuestos; financiación; alternativas; decisiones pendientes |
| [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md) | Especificación propuesta para el frente técnico, con reglas de control y criterios de prueba. No adoptada |
| [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md) | Modelos, esfuerzo y separación de contextos según lo que expone el entorno |
| [PUNTO_DE_RECUPERACION.md](PUNTO_DE_RECUPERACION.md) | Estado de las pruebas, incidencias pendientes y siguiente paso exacto. Se reescribe al terminar cada bloque importante |
| [revision/](revision/) | Estado de la revisión independiente; informe, scripts y salidas del revisor (copia sin cambios de su rama, con procedencia y huellas); respuesta del autor a cada objeción |
| `datos/fuentes.json` | Fuentes primarias con huella SHA-256, ruta en el árbol materializado y ejercicio de la publicación |
| `datos/cifras_fuente.csv` | 752 filas (713 cifras de tabla y 39 literales de texto) con documento, página PDF, literal impreso, signo, unidad, perímetro, edición («vigente» o «anterior»), período y modo de control del ejercicio |
| `scripts/verificar_cifras.py` | Comprueba cada fila contra los bytes del PDF en seis dimensiones: literal (huella, página, etiqueta, posición, signo), ejercicio, concepto de la columna, unidad, perímetro y edición. Cada una queda en OK, PENDIENTE (con motivo), FALLO o NO_APLICA. OK significa «sin incoherencia detectada», no «acreditada». Hoy: 738 OK, 14 PENDIENTE (URD 2022 p.302: ni unidad ni cabecera de columnas localizables), 0 FALLO. Guarda las huellas del CSV y de `fuentes.json` |
| `scripts/test_verificar_cifras.py` | 136 casos: 23 positivos reales, 36 PENDIENTE esperados y 77 contraejemplos, cada uno detectado en su dimensión. Incluye los mutantes conjuntos de posición y literal, año, unidad, perímetro y edición, los M1–M4 de la revisión n.º 1, las sondas externas sobre eb77dea, los mutantes y contraejemplos de la revisión n.º 3, las columnas por país o por sociedad de C9 y los contraejemplos de las revisiones n.º 4 a 8. Además, nueve comprobaciones directas de funciones del verificador (revisión n.º 8: encabezado numerado, rótulo con viñeta y la excepción «Total» de la cabecera por países), que se cuentan aparte |
| `scripts/barrido_fecha_rotulo.py` | Barrido del autor (C18, revisión n.º 8, T2 y T3): todas las líneas de las cinco fuentes en que la regla de la fecha del rótulo da un ejercicio, y las que toman la fecha de una línea unida de encima. Salida en `resultados/barrido_fecha_rotulo.txt` |
| `scripts/sondas_metadatos.py` | Cambia un solo campo (unidad o perímetro) en todas las filas de tabla de una versión y cuenta las etiquetas cambiadas que el verificador de esa versión no detecta. No mide si se rechaza una cifra de otra unidad o de otro perímetro con una etiqueta verosímil |
| `scripts/especificacion_cifras.py` | Regenera el CSV desde los PDF, lo contrasta con la lectura del autor y se detiene si alguna dimensión falla |
| `scripts/contraste_f1.py` | Cálculo independiente con 292 comprobaciones: 136 contra el libro (18 sobre una copia recalculada con exceso de caja no nulo), 127 contra la fuente (126 residuos, cada uno con su cota de redondeo, y la doble vía del FCF base) y 29 algebraicas, que no prueban nada frente a datos externos. Solo calcula con la verificación del mismo CSV y con cifras sin fallo, de la edición vigente, del grupo y con la unidad pedida. Clasifica la cobertura de cada entrada usada y da, para las contrastadas entre páginas, el intervalo de errores que ninguna identidad entre páginas detecta |
| `scripts/test_contraste_residuos.py` | 24 casos: con el verificador saltado a propósito, los residuos hacen fallar el cálculo ante datos erróneos y la excepción fijada no absorbe errores nuevos mayores que su cota. El cálculo se niega con una verificación de otro CSV. Documenta los límites de detección |
| `scripts/cobertura_por_mutacion.py` | Suma 3,0 a cada fila de tabla de la edición vigente, con el verificador saltado, y clasifica qué detecta el cambio. Compara el resultado con la cobertura que declara el contraste y termina con código 1 si difieren. Adaptación del script del revisor n.º 3 con un solo cambio: la verificación falsa corresponde a cada CSV mutado |
| `scripts/prueba_caja_no_nula.py` | Recalcula con LibreOffice una copia temporal del libro con exceso de caja 0, 250 y −80 para la identidad del flujo sin crecimiento (revisión, O15) |
| `scripts/tabla_conciliacion.py` | Genera la tabla de conciliación con literal y página |
| `resultados/` | Salidas reproducibles de los scripts |
| `evidencias/paginas/` | Texto de las páginas citadas, con la huella del PDF de origen. La evidencia primaria es el PDF |
| `evidencias/preparacion/` | Informes de la preparación: descarga y verificación de la base 4.14, copia de binarios al árbol del hito 4.15, verificación de su manifiesto e inventario de los PDF de Elis |
| `MANIFIESTO_SHA256.txt` | SHA-256 de cada archivo versionado de esta carpeta, salvo el propio manifiesto. Se comprueba desde esta carpeta con `sha256sum -c MANIFIESTO_SHA256.txt` |

Base congelada del producto: `revision/4.15-hito1` (059f4f68dca7acf465b5f5b21de2dede84c885ff). Binarios de la Release `base-4.14` (ZIP SHA-256 `bb51942c…b97b93e`). Libro de Elis `d2593777…92385`, idéntico en 4.14 y 4.15. Reproducción: informe, §13.
