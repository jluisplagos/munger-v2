# Plantilla V6.4.1 experimental del motor B

Esta plantilla se construyó en el encargo 4.13 §7, «conciliación completa y versionada del mantenimiento y los arrendamientos». Está escrita para la persona responsable del proyecto y para quien retome el trabajo.

La V6.4 experimental, su referencia y los expedientes hechos con ella **no cambian**. Sus bytes se conservan y cada expediente V6.4 sigue fijado a su plantilla por `plantilla_activa.json`.

## 1. Qué es y qué no es

**Hecho comprobado.** La V6.4.1 es la V6.4 experimental con un solo cambio de modelo: el **perímetro de la inversión** con el que se calculan las bases históricas de P-M1. P-M1 es la parte que mide la reposición y el crecimiento.

En la V6.4, esas bases comparan el capex de caja con toda la amortización (D&A). Esa amortización incluye la de los derechos de uso, es decir, de los arrendamientos según NIIF 16. Lo que repone esos activos (las altas de derechos de uso) no aparece en el capex de caja, porque se financia con deuda de arrendamiento.

La V6.4.1 deja elegir de forma explícita entre dos perímetros:

| Perímetro (Configuración V6.4!B146) | Inversión | Amortización | Igual que |
|---|---|---|---|
| vacío o «Caja · capex de caja frente a toda la D&A (V6.4)» | capex de caja | toda la D&A | la V6.4 |
| «NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A» | capex de caja + altas de derechos de uso de los años H–L (B147:B151) | toda la D&A | — |

**Interpretación.** De las dos alternativas, NIIF 16 completo es la que casa con el motor B.

- El motor B trata los arrendamientos como capital (Historia, fila 32) y como deuda (puente, Diagnóstico V6 C16).
- Su NOPAT ya descuenta la amortización de los derechos de uso.
- No resta los pagos por arrendamiento.

Hay otra alternativa: excluir la amortización de los derechos de uso. Solo sería coherente si se reexpresaran a la vez el NOPAT, el capital y el puente, y eso no se hace.

**Qué no es.** No es una plantilla adoptada y ningún perímetro es el central por defecto.

- Con requisito adicional, la configuración económica tiene que declarar el perímetro (`PM1.perimetro_inversion`) con su trazabilidad (`PM1.perimetro`).
- La elección para cada empresa es una decisión humana pendiente: VISCOFAN-PERIMETRO en la entrega 4.13.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `entregables/Plantilla_V6.4.1_experimental.xlsx` | La plantilla. Su SHA-256 está en `referencia/SHA256_entregables_V6.4.1_experimental.txt`. |
| `referencia/referencia_V6.4.1_experimental.json` | Referencia de integridad nueva. Recuento: 18.846 fórmulas, 5.555 celdas fijas y 13 partes del paquete, idénticas a las de la V6.4. |
| `scripts/construir_v641_experimental.py` | La construye a partir de la V6.4, que no se modifica. |
| `scripts/verificar_v64.py`, `inventario_entradas.py`, `trasladar_entradas.py`, `generar_referencia.py`, `comparar_libros.py`, `add_sliders.py` | Copias de los de la V6.4: `add_sliders.py` y `comparar_libros.py` son idénticos; en `generar_referencia.py`, `trasladar_entradas.py` y `verificar_v64.py` cambia solo la primera línea del docstring; el único cambio de código está en el inventario de entradas, que añade B146:B152 y C142:G142. |

La configuración del pipeline que la selecciona es `personaje_v2/config_v2_v641_experimental.json`.

- Nunca es la configuración por defecto.
- Sus filas van a `resumen_v2_v641_experimental.csv`. No se mezclan con las de la V6.4 (`resumen_v2_v64_experimental.csv`) ni con las de la V6.3.

## 3. Cambios de fórmula frente a la V6.4

En «Configuración V6.4»:

- **Sección 11 nueva (filas 145–156).**
  - B146: perímetro, con lista de validación.
  - B147:B151: altas de derechos de uso H–L, en millones.
  - B152: fuente de las altas.
  - B153: Σ de las altas que entran en las bases. Vale 0 con «Caja», en modo heredado o si falta alguna alta.
  - B154: perímetro efectivo.
  - B155: S2C histórico de referencia con el perímetro. Con «Caja» es el de Historia C53.
- **B55 y B58** suman B153. De B58 salen el exceso histórico (B60, B61), F_hist (B62), Rh (B71), f (B72), f_fija (B73), el requisito anual (B70, B88, B89) y su terminal. Todas esas celdas están condicionadas por B67, el requisito adicional: sin requisito, el perímetro no cambia ningún valor.
- **Fila 142 de la trazabilidad:** «P-M1 · perímetro de la inversión». Está activa con requisito adicional, y B143 la cuenta.
- **Comprobación 29 (fila 124):** salta con un perímetro no reconocido, o con NIIF 16 sin las cinco altas (≥ 0, con el 0 explícito) o sin su fuente.
- **B9 (resumen):** añade « · perímetro Caja | NIIF 16». Conciliación B!A3 y Panel!C18 repiten ese texto.

## 4. Compatibilidad y efecto (comprobado con LibreOffice sobre copias)

`personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/resultados/compatibilidad_v641.md` usa las entradas del libro evaluado de Viscofan de la 4.12. Resultados:

- **Perímetro vacío** frente al libro V6.4: 0 celdas distintas, con tolerancia 1e-12, en las once hojas de la V6.3, «Configuración V6.4» y «Conciliación B». Las únicas celdas excluidas son las nuevas y los textos que repiten el resumen B9; para estos se comprueba que solo añaden « · perímetro Caja».
- **«Caja» escrito de forma explícita:** 0 celdas distintas.
- **Modo heredado** V6.4.1 frente a heredado V6.4: 0 celdas distintas.
- **NIIF 16** con las altas conciliadas (24,110 millones en 2021–2025), con θ = 0, 0,5 y 1:

| θ | Precio de Sí, Caja | Precio de Sí, NIIF 16 |
|---|---|---|
| 0 | 40,35 | 40,35 |
| 0,5 | 39,29 | 38,62 |
| 1 | 38,22 | 36,88 |

  Los seis casos quedan en zona «caro» y dentro del dominio.
- **Réplica independiente de las bases** (D_hist, exceso, F_hist, Rh, f y requisito), calculada en Python: 0 discrepancias.

## 5. Uso en el pipeline

**Selección (`seleccion_plantilla.py`).** La V6.4.1 pertenece a la familia V6.4.

- Exige `configuracion_economica.json`.
- Rechaza declarar el perímetro con la V6.4: no se ignora en silencio.
- Con la V6.4.1 y requisito adicional, exige declararlo.
- Un expediente solo se ejecuta con la plantilla registrada. Para pasar de la V6.4 a la V6.4.1 se prepara un expediente nuevo.

**Configuración (`configuracion_economica.py`).** En `PM1` hay tres campos opcionales:

- `perimetro_inversion`;
- `altas_derechos_uso`: cinco números ≥ 0;
- `altas_fuente`.

Con «Caja» las altas pueden quedar declaradas, porque el libro no las suma. Así se calcula la variante de control con los mismos datos.

Una configuración que no declara el perímetro conserva su huella económica exacta.

**Variantes (`variantes_configuracion_v64.py`).** Con el perímetro declarado se añaden tres variantes: `perimetro_alternativo` (Caja ↔ NIIF 16, mismas entradas) y sus extremos del rango del parámetro. La comprobación conjunta también puede usar el otro perímetro como alternativa no numérica de `PM1.perimetro`.

**Lectura (`leer_v63.py`).** Lee el perímetro efectivo, las altas que entran en las bases y el S2C de referencia solo de los libros V6.4.1. Las salidas de los libros V6.4 no cambian.
