# Frente E · F1 · Elis · conciliación económica

Carpeta propia del frente económico. Solo contiene documentos y cálculos de contraste; no modifica el producto. **F1 sigue abierto.**

| Documento | Contenido |
|---|---|
| [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md) | Conciliación 2023–2025 y horizonte 2021–2025; puente del FCF base 307,933 a f y al motor A; arrendamientos; intangibles adquiridos y reinversión necesaria; impuestos; financiación; alternativas; decisiones pendientes |
| [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md) | Especificación propuesta para el frente técnico, con reglas de control y criterios de prueba. No adoptada |
| [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md) | Modelos, esfuerzo y separación de contextos según lo que expone el entorno |
| [revision/](revision/) | Estado de la revisión independiente; informe, scripts y salidas del revisor (copia sin cambios de su rama, con procedencia y huellas); respuesta del autor a cada objeción |
| `datos/fuentes.json` | Fuentes primarias con huella SHA-256 y ruta en el árbol materializado |
| `datos/cifras_fuente.csv` | 707 filas (671 cifras de tabla y 36 literales de texto) con documento, página PDF, literal impreso, signo, unidad, período y modo de control del ejercicio |
| `scripts/verificar_cifras.py` | Verifica cada fila contra los bytes del PDF: huella declarada, página, etiqueta, posición del literal, signo y ejercicio de la columna (670 filas comprobadas automáticamente y 1 con control manual justificado) |
| `scripts/test_verificar_cifras.py` | Un control positivo y 15 contraejemplos que deben fallar: signo, redondeo, página inexistente o equivocada, huella distinta, fuente ausente o sin huella declarada, posición distinta con el mismo literal, columna, bloque o saldo de otro ejercicio y control manual sin justificar |
| `scripts/especificacion_cifras.py` | Regenera el CSV desde los PDF y lo contrasta con la lectura del autor |
| `scripts/contraste_f1.py` | Cálculo independiente con 186 comprobaciones: 115 contra el libro, 58 contra la fuente (incluidos los residuos de conciliación, con tolerancia declarada) y 13 algebraicas, que no prueban nada frente a datos externos |
| `scripts/tabla_conciliacion.py` | Genera la tabla de conciliación con literal y página |
| `resultados/` | Salidas reproducibles de los scripts |
| `evidencias/paginas/` | Texto de las páginas citadas, con la huella del PDF de origen. La evidencia primaria es el PDF |
| `evidencias/preparacion/` | Informes de la preparación: descarga y verificación de la base 4.14, copia de binarios al árbol del hito 4.15, verificación de su manifiesto e inventario de los PDF de Elis |
| `MANIFIESTO_SHA256.txt` | SHA-256 de cada archivo versionado de esta carpeta, salvo el propio manifiesto. Se comprueba desde esta carpeta con `sha256sum -c MANIFIESTO_SHA256.txt` |

Base congelada del producto: `revision/4.15-hito1` (059f4f68dca7acf465b5f5b21de2dede84c885ff). Binarios de la Release `base-4.14` (ZIP SHA-256 `bb51942c…b97b93e`). Libro de Elis `d2593777…92385`, idéntico en 4.14 y 4.15. Reproducción: informe, §13.
