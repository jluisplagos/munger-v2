# T-1 · Preparación del grupo L de la batería de trazabilidad (entrega 4.10.1, encargo §3)

**Qué es.** El informe de la corrección de T-1: qué falló en la revisión externa, por qué, cómo se ha corregido la prueba y qué queda demostrado.

## Hecho: qué falló

- **Archivo y prueba.** En `personaje_v2/pruebas/test_trazabilidad_v2.py`, grupo L, falló la prueba «una modificación posterior del libro o una ficha que registra otro libro invalidan la correspondencia».
- **Resultado de la revisión externa:** 73/74.
- **Lo que hacía la prueba de la 4.10:**
  - reconstruía el libro evaluado sin cachés (`escribir_v63.py --copia-de-prueba`);
  - le incorporaba las cachés con `verificar_todo.sh`, que lo acreditaba;
  - comprobaba la precondición `m0 = motivo_acreditacion_libro(…) is None` con las fichas copiadas de la referencia de la 4.6.1.
- **Por qué fallaba.** Esas fichas registran el libro histórico, `1020bb53…`. En el entorno de Claude la reconstrucción reproducía esos bytes exactamente, y la prueba pasaba. En otro entorno los bytes del ZIP interno del Excel pueden diferir. Entonces `m0` ya era un rechazo («ficha.json registra otro libro evaluado…»), y era **correcto**: el control de producción rechazaba una correspondencia rota.
- **Dónde estaba el error:** en la preparación de la prueba, no en el código del proyecto.

## Reproducción

`scripts/reproducir_T1.py` construye el mismo caso dos veces: en este entorno y simulando otro entorno, en el que el libro final tiene bytes distintos e inocuos (los mismos miembros del ZIP, con las mismas fórmulas y valores) y se vuelve a acreditar. La salida está en `t1/reproducir_T1_salida.txt`:

| Entorno | Libro final | Preparación de la 4.10 (fichas copiadas) | Preparación de la 4.10.1 (fichas sintéticas) |
|---|---|---|---|
| Este | 1020bb53… (igual al histórico) | m0 = None: la prueba antigua pasa | m0 = None: precondición coherente |
| Otro (simulado) | fa874f1c… | m0 = «ficha.json registra otro libro evaluado (1020bb53…) que el acreditado (fa874f1c…)»: **la prueba antigua falla**, como en la revisión externa | m0 = None: precondición coherente |

## Corrección (solo en la prueba; el código del proyecto no cambia)

`prueba_correspondencia`, en el orden que pide el encargo:
1. El libro sintético final ya está construido y acreditado por `verificar_todo.sh`.
2. `fichas_sinteticas` prepara las fichas **del material de la prueba** con la identidad de ese archivo **antes** de comprobar `m0`. No se toca ninguna ficha, auditoría ni cierre real.
3. Se comprueba que la precondición es coherente: `m0 is None`.
4. Cada mutación se aplica por separado, en su propia copia, con su rechazo.

**Rechazos conservados** (sin quitar la comprobación de la huella ni rebajar ninguna expectativa):

| Caso | Diagnóstico que se exige |
|---|---|
| Ficha que nombra otro libro | «registra otro libro» |
| Modificación posterior del libro | «no es el libro acreditado» |
| Comprobante inválido: JSON ilegible (prueba nueva) | «no se puede acreditar» |
| Comprobante inválido: verificación final no ÍNTEGRO, u otro `.xlsx` (prueba de R-3, ya existente) | — |
| Falta de correspondencia: el comprobante nombra un libro evaluado ausente (prueba nueva) | «falta el libro acreditado» |

**Reconstrucción sintética con bytes distintos e inocuos** (pruebas nuevas, aunque 74/74 ya pasaba en este entorno):
- `rezip_inocuo` reescribe el `.xlsx` con los mismos miembros y el mismo contenido (se comprueban miembro a miembro, igual que el valor de `Análisis!C83`), pero con otra fecha interna y otro nivel de compresión.
- **Acreditado y con las fichas de su identidad, la precondición es coherente:** la preparación no depende de recuperar el ZIP interno del Excel histórico.
- **Identidad estricta:** si después se pone en su lugar el archivo con los bytes originales, que es equivalente, se rechaza («no es el libro acreditado»). No se relaja la identidad de un archivo ya acreditado.

La prueba de R-3 se prepara de la misma forma: las fichas con la identidad del libro antes de su precondición.

## Correcciones tras la revisión interna (solo en la prueba y en la reproducción)

- **H-3 · `rezip_inocuo` idempotente.** Con una fecha y un nivel de compresión fijos, un libro que ya tuviera esa forma daría los mismos bytes y las dos pruebas nuevas fallarían en falso (la revisión interna lo provocó: 76/78). Ahora, si una forma coincide con los bytes del origen, se usa la siguiente, y el resultado siempre tiene bytes distintos con el mismo contenido. Ninguna aserción cambia. Comprobación de unidad: con un origen que ya tiene la forma de la prueba, los bytes salen distintos y el contenido igual.
- **Nombre conservado.** La última prueba del grupo L vuelve a llamarse como en la 4.10 («los libros finales de los expedientes de la 4.10 son, byte a byte, …»); desde la 4.10.1 cubre también los expedientes posteriores, que aparecen en su detalle. Así los 74 nombres de la 4.10 se conservan exactamente: `reproduccion/nombres_trazabilidad_4_10.json`, obtenido ejecutando el archivo de la 4.10 (74/74), que se conserva en `reproduccion/test_trazabilidad_v2_4_10.py.txt`.
- **`reproducir_T1.py`:** comprueba los códigos de retorno, que `verificar_todo.sh` acredite el libro final y que exista el comprobante, y no deja `__pycache__` (ni el suyo ni el de sus subprocesos). Su salida es idéntica a la guardada.

La revisión interna reprodujo además T-1 con las pruebas reales en un «otro entorno» provocado: la batería de la 4.10 dio 73/74 con el mismo fallo y mensaje que la revisión externa, y la de la 4.10.1, 78/78 (`../revision_interna/REVISION_INTERNA_4_10_1.md`).

## Pruebas

- **Batería de trazabilidad en el árbol de trabajo:** **78/78**. Los 74 casos de la 4.10 se conservan y se añaden 4: comprobante ilegible, falta de correspondencia, reconstrucción inocua e identidad estricta.
- **Grupo L:** 11 de 11.
- `verificar_paquete.sh completa` exige ahora al menos 78 pruebas.
- **La última prueba del grupo L** comprueba también los comprobantes del libro de los expedientes posteriores a la 4.10, incluido el ensayo 2025 de la 4.10.1.

**Límite.** Este informe no presenta como ejecutado por la revisión externa nada que no ejecutara ella: obtuvo 7/7 en el grupo L con su propia corrección de la preparación, pero no 74/74 ni 78/78 sobre este paquete.
