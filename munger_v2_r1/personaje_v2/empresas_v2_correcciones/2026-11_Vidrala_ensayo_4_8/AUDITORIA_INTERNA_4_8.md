# Auditoría interna de la entrega 4.8 · Munger v2, piloto Vidrala

Auditor interno de Claude con contexto separado (no vio cómo se hizo el trabajo). 10-nov-2026. Convenciones:
- **[hecho]**: comprobado por el auditor con una ejecución o una lectura que se cita;
- **[interpretación]**: lectura del auditor sobre hechos comprobados;
- **[propuesta]**: lo que el auditor sugiere; la decisión es de la persona responsable.

Nada de este informe está comprobado externamente.

## 0. Cabecera: material y huellas

| Comprobación | Momento | Resultado |
|---|---|---|
| `tail -n +2 MATERIAL_AUDITORIA_4_8.txt \| sha256sum -c --quiet` | inicio (14:07:42 CET) | **todo OK** (32 archivos, código 0) |
| la misma | final (14:35:07 CET) | **31 OK y 1 FAILED: `verificar_paquete.sh`** (`ce0e69e7…`), el cambio declarado por el autor a las 14:09:26; los otros 31 archivos del material no han cambiado |

**Cambio del material durante la auditoría.** El coordinador avisó de que `verificar_paquete.sh` cambió tras la fijación (huella nueva `ce0e69e7…040c1815`) y de que se añadieron `scripts/comprobar_integracion_verificador_48.py` (`6a26853c…`) y su salida (`c79c0b29…`). La persona auditora lo trató como dato que había que comprobar, no como explicación aceptada:
- [hecho] `diff` del verificador fijado (`f2c14257…`) frente al nuevo: el bloque de la batería de estados se mueve, sin cambiar una sola línea, de detrás del bloque de cierre a delante del bloque del resumen; cambia también el comentario de cabecera (tiempo estimado «≈ 7–10 min»).
- [hecho] Con el verificador **fijado**, el control histórico de la 4.6.1 da `comprobar_integracion_verificador.py` **7/13** y `comprobar_vigencia_ensayo.py` **22/23**; con el **nuevo**, 13/13 y 23/23. Los de la 4.7 (12/13) y la 4.7.1 (13/13) no cambian con ninguno de los dos (12/13 es también su resultado sobre el árbol 4.7.1 de partida). El control nuevo de la 4.8 da 13/13.
- Ambos archivos nuevos se han revisado como parte del material (hallazgo Z-e). `MATERIAL_AUDITORIA_4_8.txt` no se ha actualizado.

**Árboles.** Partida 4.7.1 (`/home/claude/base471/munger_v2_r1`) y trabajo 4.8 (`/home/claude/trabajo48/munger_v2_r1`), ambos solo leídos. Todas las ejecuciones se hicieron en copias `cp -a` dentro de `…/scratchpad/auditor/` (`t48`, `b471`, `mut`), con `PYTHONDONTWRITEBYTECODE=1` y `python3 -I`/`-B`, y ninguna prueba con LibreOffice en paralelo con otra.

## 1. Pruebas ejecutadas por el auditor

| # | Qué | Código | Resultado | Salida (en `…/scratchpad/auditor/out/`) |
|---|---|---|---|---|
| 1 | `reproducir_xa_xc.py --raiz` | 4.7.1 | X-a y X-c **reproducidos**; salida idéntica (salvo la etiqueta) a `reproduccion_xa_xc_codigo_4_7_1.txt` | `repro_471.txt` |
| 2 | ídem | 4.8 | X-a y X-c **coherentes** en la primera ejecución; idéntica a `reproduccion_xa_xc_codigo_4_8.txt` | `repro_48.txt` |
| 3 | `test_estados_v2.py` | 4.8 | **25/25** (7 s), mismas líneas que la salida conservada | `test_estados_48.txt` |
| 4 | `test_cierre_v2.py` y después `test_resumen_v2.py` (en secuencia) | 4.8 | **55/55** (2 min 30 s) y **45/45** (31 s); difieren de las conservadas solo en nombres temporales y en identificadores de material dependientes de la hora | `test_cierre_48.txt`, `test_resumen_48.txt` |
| 5 | 10 mutaciones propias sobre `pipeline.py`/`ficha.py` | 4.8 mutado | 6 detectadas (22, 22, 24, 22, 24 y 24/25); 4 sobreviven y son **equivalentes** en el material probado (ver Z-j) | `mutaciones_auditor.txt` |
| 6 | 10 escenarios nuevos N1–N9 (y N6b), no cubiertos por la batería | 4.8 y 4.7.1 | ver §2 | `escenarios_48.txt`, `escenarios_471.txt`, `escenario_N6b.txt`, `escenario_N9.txt` |
| 7 | Regla H2: `inspect.getsource(veredicto_auditoria)` y `diff` del método | 4.7.1 y 4.8 | idénticos (`9edf6252…`) | — |
| 8 | `analisis_pm1.py` en una copia | 4.8 | código 0, «todos los controles cumplen»; **las 8 salidas de `financiero/` idénticas byte a byte** a las del árbol | `pm1_ejecucion.txt` |
| 9 | Recomprobación aritmética independiente de P-M1 (guion propio) | — | ver §3 | `verificar_pm1.py`, `verificar_pm1.txt` |
| 10 | Variante del auditor de P5 con el exceso medido frente a la amortización propia | — | P5 62,71 / 55,83; P5x 57,68 / 51,05 (Z-d) | `pm1_variante_auditor.txt` |
| 11 | Muestras de evidencia contra el PDF español (`pdftotext`, pp. 21, 49–52, 58, 88, 94, 173, 176, 177, 205) y los `CF_2019`/`CF_2020` | — | todas coinciden (§3) | `pdf/` |
| 12 | Descarga de una fuente CNMV (O3) | — | **403 del proxy**: las fuentes externas no son comprobables desde el contenedor | — |
| 13 | `comprobar_entrega_4_8.py` (con el verificador nuevo) | 4.8 | 29/31: fallan solo «VERSION» y «salidas = manifiesto» (manifiesto sin actualizar; no es hallazgo) | `comprobar_48_en_t48.txt` |
| 14 | `comprobar_entrega_4_7_1.py` sobre el árbol 4.8 | 4.8 | 41/44: las tres que fallan son huellas de archivos cambiados a propósito y la cabecera de huellas de la salida conservada del resumen | `comprobar_471_en_t48.txt` |
| 15 | Controles de integración del verificador 4.6.1 / 4.7 / 4.7.1 / 4.8, con el verificador fijado y con el nuevo | — | ver §0 | — |
| 16 | Baterías históricas sobre el árbol 4.8 (verificador nuevo) | 4.8 | 4.2 todas · 4.3 217/217 · 4.3.1 43/43 · 4.4 72/72 · 4.5 60/60 · 4.6 24/24 · 4.6.1 23/23 · 4.7 46/49 (lo esperado) · todas con salida **idéntica** a la de referencia; `test_comprobadores.py` 114/114; `test_pipeline_sintetico.py` 30/30 (5 min 21 s) | `historicas_resumen.txt` |
| 17 | Huellas del manifiesto de la 4.7.1 frente al árbol 4.8 real y frente a `base471` | — | ver §5 | — |

## 2. Escenarios nuevos (X-a, X-c y vías vecinas)

| Escenario | 4.7.1 | 4.8 | Lectura |
|---|---|---|---|
| N1 · esquema de ficha roto + `--desde 2` sin datos tras un cierre | `no_entregable`, paso 2; diagnóstico «estado previsto: None» | `no_entregable`, paso 2; diagnóstico «estado previsto: pendiente_de_datos»; última línea con la causa | mejor; queda la línea FIN del historial mezclada (Z-g) |
| N2 · `ficha.py` directo `--estado pendiente_de_datos` / `modelo_no_aplicable` / `pendiente_de_investigacion` en el paso 14 con aprobación registrada | — | ficha con `cierre: APROBADO` del material auditado (que proponía `concluido`) y `cierre_vigente.json` con ese estado; aviso; después `informe.py` lo archiva (código 3) | sin aprobación publicada, pero el criterio de X-c solo excluye `no_entregable` (Z-f) |
| N3 · X-a y segunda ejecución con `--desde 2` | — | ficha e informe idénticos, sin archivos nuevos (el diagnóstico solo difiere en su lista de archivos) | correcto |
| N4 · X-c y subsanación por la vía equivocada (`--desde 14`) | — | **código 4**, «auditoria = None», no reutiliza la aprobación archivada; sin `--desde`, espera la auditoría (código 10) | correcto; el diagnóstico queda obsoleto (Z-h) |
| N5 · X-a con `resumen_csv` configurado en otro CSV | `estado None` | estado coherente; el predeterminado (registrado) queda «SIN APROBACIÓN VIGENTE» y el configurado, `pendiente_de_datos` | correcto |
| N6 / N6b · X-a con retirada pendiente (destino registrado inaccesible) y relanzamiento tras recuperarlo | código 5; al relanzar **vuelve a hacer el paso 2 y publica** la fila `pendiente_de_datos` | código 5; al relanzar, la retirada se completa pero **no se publica nunca** la fila del estado actual | **regresión** (Z-a) |
| N7 · `terminar()` directo con el pipeline en el paso 14 (hipotético) | `None`, paso 13, sin ficha | `pendiente_de_datos` en el estado, **sin `ficha.json` ni `informe.md`** (la ficha llevaba `cierre` y la archivó `informe.py`) | inalcanzable hoy; fragilidad (Z-f) |
| N8 · esquema roto + fallo de migración (`no_entregable` previsto) | — | `no_entregable` por migración; el fallo de esquema solo consta en `ficha_valida = False` | anterior a la 4.8 (Z-g) |
| N9 · `terminar('modelo_no_aplicable')` en el paso 6 tras un cierre, y relanzamiento | coherente | coherente, con causa en la última línea | X-a solo afectaba a `concluido`/`pendiente_*` |

## 3. P-M1: lo comprobado

**[hecho] Reproducción y aritmética.**
- `analisis_pm1.py` reproduce byte a byte las ocho salidas; la réplica de la 4.7.1 se ejecuta sin cambios y coincide (REF 69,2447 / 64,2622; X41 48,61 / 44,01).
- Guion propio: ponderado, precio de Sí (forma cerrada con k = 3) y Δ de las 16 alternativas: error máximo 0,0001. Identidad FCF = NOPAT + D&A − inversión bruta − Δcirculante en las 480 filas de los años 1–10: error máximo 0,00002. **Valor por acción reconstruido** desde el FCF con la tasa operativa del modelo (r_op 0,0868, derivada de r = 0,09 en la 4.7.1), el puente 160,784 y 35,206 M acciones, despejando g con REF (salen exactamente 1,0 % / 2,0 % / 2,5 %): todas las alternativas coinciden con error ≤ 0,004 €, salvo P2 y P4 (≤ 0,03 €, por la cola del escudo fiscal de la ola posterior al año 10, que el guion propio no incluye).
- Regla del hueco: el adicional es max(0, (λ − 1)·(D&A − cartera_t) − inversión fija neta) en todos los años; en el terminal, los adicionales 3,0 / 15,8 / 28,1 / 15,8 / 5,0 / 5,3 coinciden con §5.3.
- Tablas del informe: §1 (rangos), §4 (ratios por año y segmento; Reino Unido 1,0954, Iberia 1,9696 recalculados), §6 (alternativas, escenarios y necesidades de caja) coinciden con `pm1_salida.txt`/`pm1_alternativas.csv`.
- λ: 1,112 / 1,170 / 1,045 / 1,237 y balance 1,192 / 1,288 recalculados.

**[hecho] Evidencia contra el PDF español y los textos.** Coinciden: derechos de uso 6.760 / 4.768 (p. 58, **X-e verificado**); dotación material 118.275, altas 177.848, en curso 208.538, coste 2.194.513 (p. 49); cartera 4.492 y valor neto 21.858, columna «Cartera de clientes» (p. 52); compromisos 66.610 y subvenciones 23.115 (p. 51); «principalmente, en renovación de hornos» (p. 50); vida útil 8–16 (p. 21); −5,4 % orgánico (p. 88); «adaptando nuestra capacidad industrial» (p. 94); electrificación 10–15 % / 25 % / 40 % (p. 173); «3 nuevos hornos» (p. 177); CapEx no elegible 99,0 % (p. 205). Y-1: en `CF_2019` la amortización es 91.088 y el deterioro 6.003 (97.091 = suma), y en `CF_2020` 84.144 sin el deterioro de 1.415: el hallazgo Y-1 es correcto. No se comprobó la discrepancia de la p. 69 del PDF inglés.

**[hecho] Puntos del encargo que se cumplen.** Constantes sin cambios (r, probabilidades, k, caja, puente, acciones); «=D&A» no se propone; campos humanos vacíos; preguntas Q-E1–Q-E7 preparadas y no enviadas; información posterior a 2025 marcada; tabla de mejora presente (registro §8); referencia reproducida antes de las alternativas; por escenario, NOPAT, inversión fija, circulante, FCF, caja, V, ponderado, Sí y peso terminal (en el CSV; en el informe, una selección).

**No comprobable por el auditor:** las 14 fuentes externas (PDF no conservados, CNMV bloqueada desde el contenedor) y el informe de la crítica con Fable (no está en el paquete).

## 4. Hallazgos

### Z-a · importante · regresión: tras una retirada pendiente (código 5) en una terminación que no cierra, el resumen no vuelve a publicar nunca el estado actual

- **Evidencia [hecho].** N6b: copia aprobada sin datos, resumen predeterminado sustituido por una carpeta, `--desde 2`: código 5, estado `pendiente_de_datos`, fila no publicada (correcto). Se restaura el CSV y se relanza sin `--desde`, dos veces: código 0, «estado final: pendiente_de_datos · …», pero la fila de Vidrala sigue «SIN APROBACIÓN VIGENTE …» (sin estado) mientras estado, ficha, informe y diagnóstico dicen `pendiente_de_datos`. Con el código 4.7.1, el relanzamiento repetía el paso 2 (porque el estado era `None`) y publicaba `pendiente_de_datos`. N6 (resumen configurado en otro CSV) da lo mismo: el CSV configurado no llega a existir.
- **Interpretación.** El Anexo D dice que «al recuperar el acceso, la siguiente ejecución completa la retirada» y que, desde la 4.8, estado, ficha, informe, diagnóstico y resumen coinciden. La retirada se completa, pero `resumen.py` ya no se vuelve a ejecutar porque el estado final se conserva. La incoherencia no es aprobatoria (la fila dice «sin aprobación»), pero es duradera y ninguna prueba la cubre.
- **Propuesta.** Cuando `resumen.py` termina con 5 dentro de `salidas_finales`, marcar en `estado_pipeline.json` que la publicación queda pendiente. Al empezar una ejecución con un estado final, después de completar las retiradas, volver a ejecutar `resumen.py`, o como mínimo comprobar que la fila coincide con la ficha. Añadir N6b a `test_estados_v2.py`.

### Z-b · importante · P-M1: «P1 (λ = 1,15) es el mínimo que respaldan los indicios» y «λ ≥ 1,10 en todos los indicios» contradicen las salidas del propio guion

- **Evidencia [hecho].**
  - `pm1_salida.txt` imprime λ(10 años, 1 %) = 1,045 y el ciclo del Reino Unido 1,095.
  - El guion rotula P1b (λ = 1,10) como «el indicio más bajo» y λ = 1,15 como «central elevado de 1,10 a 1,15 tras la crítica independiente».
  - El informe dice en §1 «λ entre 1,10 y 1,29 según el indicio» y en §7 «λ ≈ 1,15 (P1) … Es el mínimo que respaldan los indicios». `decisiones_y_preguntas_4_8.json` (D-N3b) dice «P1, como el ajuste mínimo que respaldan los indicios», y `DECISIONES.md` dice «P1 (λ = 1,15) como ajuste mínimo».
  - El registro (§8, columna «qué supuesto queda respaldado») dice «el desfase de inflación existe (λ ≥ 1,10 en todos los indicios)», mientras el informe clasifica P1 como **hipótesis condicionada**.
  - §7 añade «Sin ese dato, el valor cae en algún punto entre P1 y P5 (68,9 a 63,5)», que es una cota, cuando §1 dice «rangos explorados, no límites demostrados». Con λ ≈ 1,05–1,10, el valor queda por encima de P1 (P1b 69,25; P0 69,73).
- **Efecto.** P1 frente a P1b: ponderado 68,92 frente a 69,25; precio de Sí 63,00 frente a 63,72.
- **Propuesta.** Decir que P1 es la hipótesis central (λ = 1,15, elegida tras la crítica) dentro de un abanico de indicios de 1,05 a 1,29, con el mínimo indicado cerca de 1,10 (P1b). Mantener la clase «condicionada» en todos los documentos y quitar «respaldado» de la tabla de mejora. Sustituir «el valor cae entre P1 y P5» por «las alternativas exploradas van de …».

### Z-c · importante · P3 = P1 por construcción de la regla del hueco, no porque la recuperación sea pequeña

- **Evidencia [hecho].** En `pm1_anio_a_anio.csv`, P3 MALO añade inversión fija neta de 2,665 / 8,011 / 13,432 en los años 8–10, y el adicional de reposición baja exactamente en lo mismo (17,277 / 11,931 / 6,510 frente a 19,942). La inversión bruta queda en 152,890 y el FCF es idéntico. En la 4.7.1, la misma variante «R1 sin capacidad» bajaba el V MALO de 51,8059 a 51,4935 (`sensibilidades_n3.csv`). El informe (§5.4) lo explica así: «porque en el MALO las ventas apenas se recuperan … La capacidad no es material en este modelo». P4 hereda el mismo efecto.
- **Interpretación.** La regla del hueco descuenta del requisito de reposición cualquier inversión fija neta, también la que recupera capacidad perdida. El argumento de la regla (ΔV ÷ S2C nominal ya incluye el desfase de inflación) vale para el crecimiento nominal de una base conservada, no para reconstruir una capacidad que no se conservó. La explicación del informe es errónea, y la conclusión «capacidad no material» descansa en ese artefacto. El efecto numérico es pequeño (unos −0,3 €/acción en el V MALO), pero delimita el dominio de validez de la regla que usan todas las alternativas.
- **Propuesta.** Corregir la explicación y presentar P3/P4 con el hueco aplicado solo a la inversión que no es recuperación de capacidad. Declarar en §5.2 el dominio de la regla.

### Z-d · importante · P5 y P5x miden el exceso frente a la amortización total (con la cartera) y a la vez aplican P0

- **Evidencia [hecho].**
  - `EXCESO_MEDIO = Σ(CAPEX_H − DA_H)/5` usa la amortización total, que en 2024–2025 incluye la de la cartera (4,921 y 4,492).
  - El mismo informe (§3) advierte que «comparar la inversión de caja con la amortización total infravalora el exceso» (1,549 frente a 1,418).
  - Con P0, la inversión bruta del año 1 de P5x en el MALO es 184,011, no el nivel de 2025 (188,503) que dice representar.
  - Variante del auditor con el exceso frente a la amortización propia (+cartera): P5 pasa de 63,45 / 56,55 a **62,71 / 55,83**, y P5x de 59,52 / 52,80 a **57,68 / 51,05**.
  - El 51 % de doble cómputo de X41 (que se compara con P5x sin P0) no cambia.
- **Interpretación.** Es una incoherencia de definición entre P0 y P5. Mueve el borde inferior del abanico «fundamentado» que el informe (§1) y D-N3b ofrecen a la decisión humana. No cambia las conclusiones cualitativas.
- **Propuesta.** Medir el exceso frente a la amortización que se repone (sin la cartera) cuando se aplica P0, o no aplicar P0 en P5, y actualizar §1, §6, §7 y D-N3b.

### Z-e · importante (subsanado después de la fijación; falta registrarlo) · el verificador fijado rompía un control histórico, y el control de la 4.8 no lo detecta

- **Evidencia [hecho].** Ver §0. Con el `verificar_paquete.sh` fijado, el control de vigencia de la 4.6.1 daba 22/23 (integración 7/13). El autor lo detectó y lo corrigió tras la fijación; el auditor verificó que el cambio es solo un traslado del bloque y que, con él, todos los controles históricos dan su resultado esperado con salida idéntica (§1, fila 16).
  - El registro (§1) solo documenta las baterías históricas sobre el árbol 4.7.1 de partida, no sobre el 4.8.
  - `comprobar_entrega_4_8.py` no ejecuta ningún control histórico.
  - `MATERIAL_AUDITORIA_4_8.txt` no incluye el verificador nuevo ni los dos archivos añadidos.
  - El control de la 4.7.1 da 41/44 sobre el árbol 4.8 (por diseño), y nada lo declara como resultado esperado.
- **Propuesta.**
  - Registrar el cambio y su motivo en el registro (§2 o §7) con las huellas nuevas.
  - Volver a ejecutar las baterías históricas sobre el árbol final y anotar sus resultados esperados, incluido el 41/44 de la 4.7.1, como hizo la 4.7.1 con el 46/49 de la 4.7.
  - Añadir a `comprobar_entrega_4_8.py` la ejecución de los controles de integración de la 4.6.1, la 4.7.1 y la 4.8.

### Z-f · menor · el criterio de X-c en `ficha.py` solo excluye `no_entregable`; `pipeline.py` confía en la posición «paso 14»

- **Evidencia [hecho].** En N2, `ficha.py --estado pendiente_de_datos` (o `modelo_no_aplicable`, o `pendiente_de_investigacion`) sobre el expediente aprobado escribe `cierre: {APROBADO, 74b94f80…}` y `cierre_vigente.json` con ese estado. La auditoría aprobó un material que proponía `concluido`. No llega a publicarse: hay un aviso, `informe.py` lo archiva y `resumen.py` no escribe fila. En N7 (hipotético), `terminar()` con el pipeline en el paso 14 acaba con `pendiente_de_datos` en el estado y sin `ficha.json` ni `informe.md`, porque `conservar_estado` mantiene el estado aunque `informe.py` archive la ficha. Ningún camino actual llama a `terminar()` en el paso 14.
- **Propuesta.**
  - Que `ficha.py` escriba `cierre` solo si el estado coincide con el `estado_propuesto` de `ficha_provisional.json` del material fijado, o con un indicador explícito del pipeline.
  - Que `salidas_finales(cierre=False)` compruebe al final que `ficha.json` existe y, si no, no conserve el estado.
  - Puede tratarse junto con Q-T3.

### Z-g · menor · mensajes mezclados cuando el esquema falla en una terminación temprana

- **Evidencia [hecho].**
  - En N1, la última entrada FIN del historial dice «FIN · estado no_entregable · falta_de_datos: falta fase1_v63.json…». El tipo es el de `terminar()`, no `fallo_de_implementacion`. La última línea impresa y el diagnóstico sí son correctos.
  - En N8 (estado previsto `no_entregable` y esquema roto), el fallo de esquema no se declara en ninguna parte salvo `ficha_valida = False`. Esto ya ocurría antes de la 4.8.
- **Propuesta.**
  - Que `terminar()` tome el tipo y el detalle de `diagnostico.json` cuando `salidas_finales` devuelve un fallo de esquema.
  - Que, con `no_entregable` previsto, el fallo de esquema se añada al diagnóstico.

### Z-h · menor · el diagnóstico queda obsoleto cuando un estado final se abandona

- **Evidencia [hecho].** En N4, tras X-c y un `--desde 14`, el estado es `None` en el paso 13 (rechazo, código 4), pero `diagnostico.json` sigue diciendo `no_entregable` por el esquema. Lo mismo ocurre mientras se espera la auditoría nueva en la subsanación correcta. La última línea no lo usa, porque solo lo lee si el estado coincide, y el comportamiento es anterior a la 4.8.
- **Propuesta.** Mover el diagnóstico a `.anterior` al rechazar el cierre o al reanudar con `--desde` desde un estado final, como ya se hace con `concluido`.

### Z-i · menor · lógica de `comprobar_entrega_4_8.py`

- **Evidencia [hecho].**
  1. Ejecuta `analisis_pm1.py` **en el árbol**, que reescribe `financiero/` antes de comparar con el manifiesto. Si una salida cambiara, la original se perdería.
  2. La comprobación de conservación recorre solo las entradas del manifiesto 4.7.1: un archivo **añadido** en `empresas_v2/` o en un expediente anterior no se detecta. Además compara manifiestos, no archivos.
  3. El texto dice «48,6084 / 44,0081 ±0,0001» y el código tolera 0,01.
  4. Las fuentes externas solo se comprueban por formato.
  5. No ejecuta los controles históricos (Z-e).
- **Propuesta.** Ejecutar P-M1 en una copia temporal. Comprobar también los archivos nuevos bajo los prefijos protegidos. Alinear la tolerancia con el texto. Ver Z-e.

### Z-j · menor (observación) · mutantes equivalentes

- **Evidencia [hecho].** Sobreviven cuatro mutaciones propias:
  - quitar `self.st["auditoria"] = None` tras el fallo de esquema;
  - no forzar el paso 14;
  - la segunda adopción sin `conservar_estado`;
  - `conservar = True` eliminado.

  Son equivalentes con el material probado: `archivar_salidas` ya retira la aprobación del disco y no toca un `no_entregable`. Las seis que tocan la corrección se detectan, igual que las M1–M5 declaradas.
- **Propuesta.** Ninguna obligatoria: son defensas. Conviene declararlas como redundantes, o cubrirlas con un caso en que `ficha.py` no archive.

### Z-k · menor · fuentes externas y crítica con Fable no comprobables desde el paquete

- **Evidencia [hecho].** Los PDF de la CNMV no se conservan y la descarga desde el contenedor da 403 (comprobado). El informe de la crítica con Fable «se conserva en el contexto de la sesión», no en el paquete, así que la cifra del 63 % no se puede verificar. En la matriz §3 del informe, la columna «Hecho publicado» mezcla datos reproducidos con citas O*/S* declaradas, y O1 (posterior a la base) se cita en «Obligatoria frente a aplazable» sin marca de posterior.
- **Propuesta.** Marcar las citas O*/S* como «declaradas por Claude, no reproducibles en el paquete» y marcar O1 como posterior. Si la persona responsable lo quiere, adjuntar los PDF (las huellas ya constan) y un resumen escrito de la crítica.

### Z-l · menor · alternativas fijadas después de ver valores; P6i sin fundamento

- **Evidencia [hecho].** λ central (1,10 → 1,15), P5 y P6 se añadieron o cambiaron tras la crítica, que vio valores de la primera versión. Está declarado en el informe (§6, §8) y en el guion. El encargo pedía alternativas fundamentadas antes de comparar valores. El cambio va en sentido adverso, lo que reduce el riesgo de selección interesada. P6i (11,5 %) no tiene fundamento escrito en `ALTERNATIVAS`.
- **Propuesta.** Dar el fundamento de P6i (o retirarla) y mantener la declaración del orden en que se fijaron las alternativas.

### Z-m · menor · presentación de la tabla por escenario (§6)

- **Evidencia [hecho].**
  - Las columnas «NOPAT / inversión fija / Δcirculante / reposición adicional / FCF» no suman sin el término de la cartera (P0): en P1 MALO, año 1, 201,7 + 2,2 − 19,3 = 184,6 frente a 189,0.
  - El año 11 no muestra el circulante.
  - «+4,5 M€ los años 1–4» omite los 3,9 del año 5.
- **Propuesta.** Añadir la columna de la cartera y el circulante del año 11.

### Observación fuera del material (no es hallazgo)

`VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md` se modificaron entre las 14:11 y las 14:12, durante la auditoría. `CONTINUIDAD.md` ya dice que «una auditoría interna … y un control de vigencia revisaron la entrega (`AUDITORIA_INTERNA_4_8*.md`)» antes de que esta terminara. La persona responsable debería comprobar que el texto final refleje los resultados reales.

## 5. Conservación de originales y expedientes previos

- [hecho] Las 1.454 huellas de `base471/MANIFIESTO_SHA256.txt` se compararon con los archivos reales de `trabajo48`. Difieren solo:
  - los cinco archivos declarados (`pipeline.py`, `ficha.py`, `ANEXO_D`, `DECISIONES.md`, `verificar_paquete.sh`);
  - `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`, fuera del material y previstos.
- [hecho] No falta ningún archivo. Fuera de la carpeta 4.8 solo hay uno nuevo: `personaje_v2/pruebas/test_estados_v2.py`. El manifiesto de la raíz sigue siendo el de la 4.7.1.
- [hecho] Los originales de `empresas_v2/` y los expedientes 4.4–4.7.1 conservan sus huellas. No hay `__pycache__` ni `.pyc` en ningún árbol.
- [hecho] `base471` cumple su manifiesto sin cambios ni archivos de más.

## 6. Comprobación final y veredicto

- [hecho] Comprobación final (14:35:07): de los 32 archivos del material, 31 dan OK. El que falla es `verificar_paquete.sh`, cuyo cambio está declarado y revisado (§0 y Z-e). `base471` sigue cumpliendo su manifiesto. No hay `__pycache__` en ningún árbol. La auditoría no ha escrito nada en `trabajo48` ni en `base471`.
- **Veredicto: sin bloqueantes.** Quedan **cinco hallazgos importantes**:
  - Z-a: regresión de coherencia del resumen en la vía del código 5;
  - Z-b, Z-c y Z-d: P-M1, con una clasificación contradictoria de λ, una explicación errónea de P3 y una incoherencia de definición entre P0 y P5;
  - Z-e: verificador fijado que rompía un control histórico, ya subsanado pero sin registrar.

  Hay además ocho menores (Z-f a Z-m). X-a y X-c quedan reparados en las vías que pide el encargo, sin aprobaciones indebidas en ninguno de los escenarios probados. La regla H2 no cambia. Las baterías dan 25/55/45 y las históricas, sus resultados esperados. La aritmética de P-M1 se reproduce de forma independiente. La persona auditora recomienda corregir Z-a a Z-e antes de dar la entrega por cerrada, o declararlos como pendientes con su efecto.
