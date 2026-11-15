# Frente E · F1 · Elis · conciliación económica

Carpeta propia del frente económico. Solo contiene documentos y cálculos de contraste; no modifica el producto. **F1 sigue abierto.**

| Documento | Contenido |
|---|---|
| [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md) | Conciliación 2023–2025 y horizonte 2021–2025; puente del FCF base 307,933 a f y al motor A; arrendamientos; intangibles adquiridos y reinversión necesaria; impuestos; financiación; alternativas; decisiones pendientes |
| [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md) | Especificación propuesta para el frente técnico, con reglas de control y criterios de prueba. No adoptada |
| [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md) | Modelos, esfuerzo y separación de contextos según lo que expone el entorno |
| [revision/](revision/) | Revisión independiente, objeciones y respuestas |
| `datos/fuentes.json` | Fuentes primarias con huella SHA-256 y ruta en el árbol materializado |
| `datos/cifras_fuente.csv` | 680 cifras con documento, página PDF, literal impreso, signo, unidad y período |
| `scripts/verificar_cifras.py` | Verifica cada cifra contra los bytes del PDF: huella, página, literal y signo |
| `scripts/test_verificar_cifras.py` | 10 contraejemplos que deben fallar |
| `scripts/especificacion_cifras.py` | Regenera el CSV desde los PDF y lo contrasta con la lectura del autor |
| `scripts/contraste_f1.py` | Cálculo independiente: 129 comprobaciones contra la fuente y el libro |
| `scripts/tabla_conciliacion.py` | Genera la tabla de conciliación con literal y página |
| `resultados/` | Salidas reproducibles de los scripts |
| `evidencias/paginas/` | Texto de las páginas citadas, con la huella del PDF de origen. La evidencia primaria es el PDF |

Base congelada del producto: `revision/4.15-hito1` (059f4f68dca7acf465b5f5b21de2dede84c885ff). Binarios de la Release `base-4.14` (ZIP SHA-256 `bb51942c…b97b93e`). Libro de Elis `d2593777…92385`, idéntico en 4.14 y 4.15. Reproducción: informe, §13.
