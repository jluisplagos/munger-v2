# Plantilla V6.3.1 F1 del motor A

Escrita el 18-nov-2026 por el agente autor de la plantilla (Claude, Opus) en la rama `f1/plantilla-v631`, desde `f1/implantacion` @ `24e9a30`.
**Sin revisión independiente todavía**: la hará otro agente. **Estado: punto de control a mitad** (guion, referencia, verificador y
prueba A0). La selección en el pipeline, el cambio de `motor_a_f1.py` y la validación con A1/A2 no están hechos (§5).

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** La V6.3, su referencia, sus ejemplos y los expedientes
hechos con ella **no cambian**.

## 1. Qué es y qué no es

**Hecho.** La V6.3.1 F1 es la V6.3 con un solo cambio de modelo: la amortización que f (Historia C58), el ancla de S2C (C53) y, a través
de f, el terminal del Motor tratan como reposición (D_X) se calcula con el **perímetro F1 de la reinversión** que declara la persona
(decisiones F1 del 17-nov-2026; E2–E4 de la especificación F1):

| Perímetro (Historia C85) | D_X por año (fila 88) | Igual que |
|---|---|---|
| vacío o `A0_total` | D&A total (fila 8) | la V6.3 |
| `A1_sin_ROU` | D&A total − D&A de derechos de uso (fila 86) | — |
| `A2_propio` | D&A total − D&A de derechos de uso − PPA (fila 87) | — |

Los identificadores son los de `personaje_v2/scripts/motor_a_f1.py` (`PERIMETROS`).

**Qué no es.** No elige ningún perímetro: vacío es A0, que es la V6.3. No calcula `A3_estimado` (R estimada), N1 ni los términos
explícitos (transición, compras): con ellos la capa F1 tiene que seguir bloqueando (`F1-LIBRO`). No cambia las series publicadas (fila 8,
FCF base, Análisis C46–C52) ni las entradas registradas.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `entregables/Plantilla_V6.3.1_F1.xlsx` | La plantilla. SHA-256 en `referencia/SHA256_entregables_V6.3.1_F1.txt` y en el manifiesto. **No va en Git** (los `.xlsx` están excluidos): se reconstruye desde la V6.3 de la base con `python3 -I scripts/construir_v631_f1.py ../entregables/Plantilla_V6.3.xlsx entregables/Plantilla_V6.3.1_F1.xlsx` y tiene que dar la misma huella. |
| `referencia/referencia_V6.3.1_F1.json` | Referencia de integridad nueva: 10.975 fórmulas, 5.140 celdas fijas, 52 validaciones, 13 partes del paquete (idénticas a las de la V6.3). |
| `scripts/construir_v631_f1.py` | La construye a partir de la V6.3, que no se modifica. Determinista: dos ejecuciones dan el mismo SHA-256. |
| `scripts/verificar_v631.py`, `generar_referencia.py`, `inventario_entradas.py`, `add_sliders.py` | Copias de los de la V6.3: `add_sliders.py` idéntico; en `verificar_v631.py` y `generar_referencia.py` cambia solo el docstring; el inventario añade Historia C85, C86:L87 y M85:S87. |
| `scripts/trasladar_entradas.py`, `comparar_libros.py` | Copias de las de la V6.4.1, adaptadas (sin hoja de configuración; todas las columnas; solo se excluyen las etiquetas de versión y la sección nueva). |
| `scripts/probar_v631_f1.py` | Pruebas `estructura` (sin LibreOffice) y `a0` (con LibreOffice). Resultados en `pruebas/`. |

## 3. Cambios de fórmula frente a la V6.3

- **Historia, sección nueva (filas 84–90).** C85 perímetro (lista de validación); C86:L86 D&A de derechos de uso y C87:L87 PPA por año
  (≥ 0; vacío = desconocido, no cero); M85:S87 sus fuentes; C88:L88 D_X; C89 perímetro efectivo («no reconocido» con un texto fuera de la
  lista: D_X y f quedan vacías); A90 nota.
- **Fila 30** (y con ella la 31): `capex − D_X + circulante`. Con A0, D_X es el valor de la fila 8: la misma operación.
- **C58 (f), C76 (conciliación de f) y C53 (ancla de S2C):** `=IF($C$89="A0_total", <fórmula literal de la V6.3>, <fórmula con D_X>)`.
  Con A1/A2: la reinversión es la de la fila 30; f exige D_X en todos los años de la ventana (vacío ≠ 0) y el ancla, los cinco años H–L
  (la V6.3 admite tres; *interpretación*: con un perímetro F1 el ancla de E4 es la suma de H–L y un año sin D_X no se rellena).
- **Motor E205 (validación V05 del motor A):** al final, tres causas nuevas, que solo pueden saltar con A1/A2 o con un texto no reconocido:
  perímetro no reconocido (INV), D_X vacía en la ventana (INC) y D&A de derechos de uso + PPA mayor que la D&A total (INV).
- **Etiquetas de versión:** Panel A1, Análisis A1, Guía V6 A1 y Control maestro A3.

## 4. Pruebas ejecutadas (hechos)

| Orden (desde `v6/v631_f1/scripts/`) | Resultado literal |
|---|---|
| `python3 -I probar_v631_f1.py estructura` | `21/21 comprobaciones V6.3.1 F1 (estructura) PASAN` |
| `flock /home/user/e_work/libreoffice.lock python3 -I probar_v631_f1.py a0 <carpeta nueva fuera del repo>` | `22/22 comprobaciones V6.3.1 F1 (a0) PASAN` |

- *estructura*: reconstrucción con el mismo SHA-256; la V6.3 sin cambios; la referencia nueva difiere de la de la V6.3 exactamente en las
  celdas del §3 (ninguna fórmula o celda fija de la V6.3 quitada; formato condicional, nombres y partes del paquete idénticos); con A0,
  C53, C58 y C76 contienen literalmente la fórmula de la V6.3; el verificador nuevo acepta la plantilla y rechaza una mutación de D_X
  (C88 = C8); el de la V6.3 rechaza la V6.3.1.
- *a0*: libro de Elis (`Elis_v63_evaluada.xlsx`, d2593777…, el que concilió el frente E) y los tres ejemplos de la V6.3 (Empresa X, ABB,
  Hermès). Las entradas se trasladan a la V6.3 y a la V6.3.1 por la misma vía y los dos libros se recalculan con LibreOffice: con el
  perímetro **vacío** y con **`A0_total`** escrito, **0 celdas distintas** de 39.846 en las once hojas, con **igualdad exacta**
  (tolerancia 0), excluidas solo las cuatro etiquetas de versión y la sección nueva. Además: el libro V6.3.1 con las entradas es ÍNTEGRO
  frente a su referencia; con A0, D_X = D&A; el libro de Elis tal cual, recalculado, coincide con la V6.3 con sus entradas trasladadas
  (el traslado es fiel); los orígenes no cambian.

## 5. Lo que falta (después del punto de control)

1. Selección explícita: `personaje_v2/config_v2_v631_f1.json` y `seleccion_plantilla.py` (familia V6.3; un expediente solo con su plantilla).
2. Aplicar la declaración F1 al libro (perímetro, D&A de derechos de uso y PPA con sus fuentes) y que `motor_a_f1.py` deje de bloquear con
   `F1-LIBRO` **solo** si el libro es V6.3.1, su perímetro efectivo y sus series son los declarados y f, el ancla y los 33 flujos del Motor
   coinciden con la capa (oráculo).
3. Validación con A1 y A2 en el libro de Elis recalculado por LibreOffice frente a la capa; un caso sintético NIIF 16 pesado; vacío → f
   vacía; las baterías existentes.
4. No previsto en este encargo: D_X y sus series en el control de evidencias del libro (Control maestro) y en la verificación de entradas
   de la 4.15.

**No comprobado:** Excel real (todo el recálculo es LibreOffice); A1/A2 en el libro (§5).
