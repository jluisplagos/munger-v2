# Plantilla V6.4 experimental del motor B

Documentación de la plantilla construida en el encargo 4.11 («Primera integración económica experimental del motor B»). Está escrita para la persona responsable del proyecto y para quien retome el trabajo. La plantilla V6.3 y su referencia no cambian.

## 1. Qué es y qué no es

**Hecho comprobado.** La V6.4 experimental es la V6.3 con una capa nueva para el motor B (el motor «operativo con deuda»):

- dos hojas nuevas, «Configuración V6.4» y «Conciliación B»;
- columnas nuevas en el Motor (BU:DY);
- cuatro fórmulas de Diagnóstico V6 que eligen entre el valor heredado y el experimental.

**Modos de cálculo.** La plantilla tiene dos:

- **Heredado** (celda vacía o «Heredado»). Las fórmulas efectivas son las de la V6.3. Celda a celda, los libros de la 4.6.1 y de la 4.10.1 dan 0 diferencias con tolerancia 1e-12. También coincide el pipeline completo del control heredado de la 4.11 frente a la 4.10.1.
- **Experimental.** Activa, de forma explícita, las cuatro piezas del encargo:
  - N1, el tipo impositivo normalizado;
  - N2, el margen de partida manual;
  - N3, la regla de reinversión con ventas que caen;
  - P-M1, la reposición y el crecimiento.

**Qué no es.** No es una plantilla adoptada. Ninguna estructura, λ, θ, tipo, margen ni convención es una convención aprobada. Las decisiones D-N1, D-N2, D-N3, D-N3b–e y P-M1 siguen sin firmar.

**Interpretación.** Lo que la V6.4 demuestra es que el sistema calcula, concilia, rechaza y traza esas opciones de forma reproducible. No demuestra que alguna describa mejor a la empresa.

**Jerga usada en este documento.**

- **S2C** (*sales to capital*): ventas nuevas por cada euro invertido.
- **NWC** (*net working capital*): circulante comercial sobre ventas.
- **D&A**: amortización.
- **ROIC**: rentabilidad del capital invertido.
- **Terminal**: valor de los años posteriores al 10, calculado como una perpetuidad.
- **VP**: valor presente.

## 2. Archivos

| Archivo | Qué es |
|---|---|
| `entregables/Plantilla_V6.4_experimental.xlsx` | La plantilla (SHA-256 en `referencia/SHA256_entregables_V6.4_experimental.txt`) |
| `referencia/referencia_V6.4_experimental.json` | Referencia de integridad, con un recuento por tipo: 18.834 fórmulas, 5.544 celdas fijas, 62 validaciones y 13 partes del paquete (gráficos, controles y dibujos, idénticas a las de la V6.3) |
| `scripts/construir_v64_experimental.py` | Construye la V6.4 desde `v6/entregables/Plantilla_V6.3.xlsx`; la reconstrucción es determinista (mismo SHA-256) |
| `scripts/generar_referencia.py`, `scripts/verificar_v64.py` | Captura y verificación de integridad (copias de las de la V6.3 que importan el inventario de esta carpeta) |
| `scripts/inventario_entradas.py` | Entradas de la V6.3 más las de «Configuración V6.4»: `B4`, `B11:B16`, `B21:B23`, `B28:B32`, `B36:B51`, `C129:G141` |
| `scripts/trasladar_entradas.py` | Copia las entradas de un libro V6.3 a la V6.4 (escritura XML que conserva controles y gráficos) y, si se pide, una configuración |
| `scripts/comparar_libros.py` | Compara valores celda a celda (las 11 hojas de la V6.3, columnas A:BT) |
| `scripts/add_sliders.py` | Deslizadores (copia del de la V6.3; siempre se aplica al final) |

## 3. Construcción y verificación

Desde `v6/v64_experimental/`:

```
python3 -I scripts/construir_v64_experimental.py ../entregables/Plantilla_V6.3.xlsx /tmp/V64.xlsx
python3 -I scripts/verificar_v64.py entregables/Plantilla_V6.4_experimental.xlsx referencia/referencia_V6.4_experimental.json   # ÍNTEGRO
sha256sum -c referencia/SHA256_entregables_V6.4_experimental.txt
```

**Cambios frente a la V6.3** (hecho comprobado en la batería, grupo A):

- **Fórmulas cambiadas, 1.994:**
  - 16 columnas × 124 filas de valoración del Motor: AU:BD (flujos de los años 1–10), BF (terminal), BL (valor sin crecimiento), BP (reinversión del año 1), BQ (ROIC marginal), BS (validez) y BT (motivo);
  - Diagnóstico V6: C10, C11, C15 y B176:D177;
  - Panel!A1.
- **Fórmulas nuevas, 7.870:** 7.068 en el Motor (columnas BU:DY), 670 en «Conciliación B», 131 en «Configuración V6.4» y Panel!C18 (la línea de configuración del Panel, junto a la etiqueta de B18). La plantilla tiene 18.834 fórmulas y la V6.3, 10.964.
- **Fórmulas quitadas:** ninguna.
- **Textos fijos cambiados, 4:** Análisis!A1, Control maestro!A3, Diagnóstico V6!E11 y Guía V6!A1.

Cada fórmula envuelta conserva la heredada literal: `=IF($BS7,IF(experimental,nuevo,HEREDADA),"")`. Una alteración no autorizada se detecta y se nombra; la batería altera Motor!DI7 para comprobarlo.

## 4. Hoja «Configuración V6.4»

| Bloque | Entradas | Calculadas |
|---|---|---|
| 1 · Modo | B4 | B5 modo efectivo (vacío = Heredado; un texto distinto de los dos válidos = ERROR), B6 motor, B7 ¿válida?, B8 motivo, B9 resumen, B10 aviso si el modo heredado tiene opciones escritas (se ignoran) |
| 2 · N1 | B11 tipo (decimal; vacío = Historia C52), B12 fuente, B13 período, B14 perímetro, B15 clase, B16 escudo de la deuda | B17 tipo de la Historia, B18 tipo aplicado a NOPAT, B19 tipo del escudo en r_op |
| 3 · N2 | B21 margen de partida (vacío = Palancas C8), B22 perímetro, B23 procedencia | B24 margen heredado, B25 margen aplicado (m0). m0 es el margen del año 0, no el objetivo del NORMAL |
| 4 · N3 | B28 regla (R0 o R1), B29 existencias, B30 deudores, B31 acreedores, B32 fuente | B33 NWC = (B29 + B30 − B31) ÷ ventas del último año (Historia C44), B34 regla efectiva |
| 5 · P-M1 | B36 estructura, B37 familia, B38 λ, B39 θ, B40 convención de los años, B41 convención del terminal, B42 ROIC del terminal, B43 cartera de clientes, B44 amortización anual de la cartera (P0), B45 valor neto contable (P0), B46:B50 amortización histórica de la cartera de los cinco años H–L, B51 fuente | — |
| 6 · Bases históricas | — | B54 D&A₀ (Historia L8), B55 Σ reinversión neta H–L, B56 Σ cartera (P0), B57 D_hist, B58 Σ(capex − D&A), B59 Σ adquisiciones, B60 exceso acumulado, B61 exceso medio, B62 F_hist, B63 Σ amortización que se repone |
| 7 · Derivados | — | B66 ¿P0?, B67 ¿requisito?, B68 ¿Λ?, B69 código de la estructura, B70 requisito a ventas constantes, B71 Rh, B72 f, B73 f_fija |
| 8 · Efectivos (los lee el motor) | — | B76 EXPERIMENTAL ACTIVO Y VÁLIDO, B77 R1, B78 P-M1, B79 H, B80 Λ, B81 años ∝ ventas, B82 terminal ∝ ventas, B83 NWC efectivo, B84 f del S2C, B85 f del ROIC, B86 f_fija, B87 λ − 1, B88 nivel Θ, B89 requisito sin crecimiento |
| 9 · Comprobaciones | — | B96:B123: 28 comprobaciones; B90 = ninguna falla; B91 = motivo de la primera que falla; B93:K93 cartera no repuesta por año |
| 10 · Trazabilidad | C129:G141 (clase, confianza, fuente o condición, justificación, materialidad de cada parámetro) | B129:B141 valor efectivo; H activo; I sin traza; B143 estado |

**Vacío, cero y error son distintos.**

- Una celda vacía se reconoce con `LEN(TRIM(x&""))=0`; un número, con `ISNUMBER`. Nunca se usa `N()` ni una condición de verdad para decidir entre el valor y el respaldo.
- Un 0 escrito en N1 o N2 es un valor válido y se usa (casos `N1_cero` y `N2_cero`).
- Cada comprobación va envuelta en `IFERROR(…, TRUE)`, así que un error cuenta como «no cumple».

**Rechazos.** Una configuración no válida no calcula. El Motor marca las filas como no calculables (BS falso, motivo «Configuración V6.4: …» en BT). La regla V35 convierte ese estado en INCOMPLETO (Motor B255) y bloquea el valor (B252). No hay recortes de dominio: un valor fuera de rango se rechaza, no se ajusta. Las 28 comprobaciones:

| # | Qué exige |
|---|---|
| 1 | Modo reconocido |
| 2 | Solo motor B |
| 3–5 | N1: tipo en [0, 1) o vacío; fuente, período, perímetro y clase; escudo elegido |
| 6–7 | N2: margen en (−1, 1) o vacío; perímetro y procedencia |
| 8–10 | N3: regla elegida; con R1, circulante completo y no negativo |
| 11–12 | Estructura y cartera elegidas |
| 13 | R0 + P-M1 rechazado: las estructuras parten de R1 y su combinación con R0 no está especificada |
| 14–19 | Familia; λ ≥ 1; θ en [0, 1]; convenciones; ROIC del terminal «× f» en SR2 y «sin cambio» en las demás |
| 20–22 | P0: siete importes, no negativos, y la cartera se agota en diez años |
| 23 | Bases históricas de los cinco años |
| 24 | f definido (D_hist > 0 y D_hist − Rh > 0) |
| 25 | f_fija en [0, 1] |
| 26 | Requisito a ventas constantes ≥ 0 |
| 27 | Con Λ y P0, la cartera no supera la amortización total |
| 28 | D&A del último año presente |

## 5. Fórmulas del modo experimental

**Notación** (fila r del Motor, año t = 1…10):

- V_t: ventas;
- m_t: margen;
- τ: tipo aplicado a NOPAT;
- S2C: Motor G;
- ROIC: Motor I;
- g: crecimiento perpetuo (Motor H);
- V0: ventas del año 0 (Motor C);
- a_t = V_t ÷ V0 con la convención «proporcional a las ventas», o 1 con la convención «plana».

**N1.** NOPAT usa B18; el escudo de la deuda en r_op usa B19:

- r_op = (r·E + i·(1 − τ_escudo)·D) ÷ (E + D);
- con el escudo «vinculado», τ_escudo = B18.

**N2.** m0 = B21 si se informa. La senda del margen va de m0 al margen objetivo en el año 5, como en la V6.3.

**N3.**

- Δcirculante_t = (V_t − V_{t−1})·NWC.
- R0 (simétrica): inversión fija_t = (V_t − V_{t−1})·(1 ÷ S2C − NWC). La reinversión total sigue siendo ΔV ÷ S2C. Sin datos del circulante, NWC = 0 y el valor no cambia (caso `T1_M1_R0_sin_circulante`).
- R1: inversión fija para crecer_t = max(0, V_t − pico_t)·(1 ÷ (S2C·f) − NWC)·f_fija, con pico_t = max(V0, …, V_{t−1}).

  **Interpretación.** Con ventas que caen solo se libera circulante. Al recuperarse por debajo del máximo, se repone circulante sin invertir en capacidad. Por encima del máximo, se invierte por completo.

**P-M1. Requisito de reposición adicional.**

- Λ: req_t = (λ − 1)·(D&A₀·a_t − cl_t).
- Θ: req_t = θ·exceso medio·a_t.
- cl_t es la amortización de la cartera de clientes no repuesta (P0): cl_k = min(CLa, max(0, VNC − CLa·(k − 1))). Con «legado» vale 0.

**Crédito (solo H).** crédito_t = min(req_t, max(0, inversión fija_t)). Es la parte de la inversión para crecer que también cumple la función de reponer.

**Factores de las estructuras.**

- Rh = (λ − 1)·Σ amortización que se repone (Λ), o θ·exceso acumulado (Θ).
- f = D_hist ÷ (D_hist − Rh) multiplica el S2C de los años en SR1 y SR2, y el ROIC del terminal en SR2.
- f_fija = 1 − Rh ÷ F_hist multiplica la inversión fija para crecer en SRF.

**Flujo de los años 1–10.** FCF_t = V_t·m_t·(1 − τ) + cl_t − inversión fija_t − Δcirculante_t − req_t + crédito_t.

**Terminal (año 11).**

- NOPAT₁₁ = V10·(1 + g)·m·(1 − τ).
- Δcirc₁₁ = V10·g·NWC.
- fija₁₁ = (NOPAT₁₁·g ÷ (ROIC·f_ROIC) − Δcirc₁₁)·f_fija.
- req₁₁ = (λ − 1)·D&A₀ o nivel Θ, multiplicado por V11 ÷ V0 (convención proporcional) o por (1 + g) (convención «crece con g»).
- crédito₁₁ = min(req₁₁, max(0, fija₁₁)) en H.
- FCF₁₁ = NOPAT₁₁ − fija₁₁ − Δcirc₁₁ − req₁₁ + crédito₁₁.

**Valor sin crecimiento (BL).** Resta el requisito a ventas constantes, descontado (B89 ÷ r).

- **No incluye la cartera P0** (revisión interna H6). Con P0 activa, los flujos de los años suman cl_t y, con Λ, el requisito baja en (λ − 1)·cl_t mientras dura la cartera: en total, λ·cl_t por año. BL no lo recoge.
- **Es una lectura.** BL no entra en el valor, el ponderado ni el precio de Sí.
- **Magnitud en el piloto** (cálculo sobre los valores del libro con los factores de descuento de «Conciliación B», no un recálculo): Σ λ·cl_t × factor_t = 19,80 M€, unos 0,56 €/acción. BL da 58,19 €/acción; con la cartera daría unos 58,75.
- **Contraste numérico.** BL, BP, BQ y Diagnóstico B176:D177 se recalculan en Python desde las entradas de cada fila en todos los casos válidos de la batería (grupo B).

**Filas del Motor.** Todas las filas de valoración usan el modelo activo: escenarios, sensibilidades, tornado y DCF inverso. Así, el DCF inverso, el tornado y la comprobación conjunta nunca muestran el modelo heredado junto a una valoración experimental.

## 6. Hoja «Conciliación B»

**Disposición.** Tres bloques, MALO, NORMAL y BUENO, que empiezan en las filas 5, 35 y 65. Las columnas B:K son los años 1–10 y la L, el terminal. Partidas, por filas, a partir del inicio del bloque:

- +1 a +8: año, ventas, máximo conservado, margen, NOPAT, D&A, cartera P0 y reposición contable;
- +9 a +15: requisito, inversión fija para crecer, crédito, adicional pagada, Δcirculante, inversión fija bruta e inversión total;
- +16 a +22: FCF por la identidad, FCF del motor, diferencia, factor de descuento, VP, sumas de VP y peso del terminal;
- +23: salto año 10 → terminal;
- +24: S2C y ROIC efectivos;
- +25: comprobación de la fila.

**Comprobación de la fila.** Debe dar «✓ cuadra» cuando se cumplen a la vez:

- la identidad FCF = NOPAT + D&A − inversión fija bruta − Δcirculante, en los años y en el terminal;
- las sumas de VP iguales a las del motor.

**Interpretación.** Es un control aritmético: no prueba que una misma inversión reponga y haga crecer, ni que λ o θ describan a la empresa.

## 7. Uso en el pipeline

**Selección de la plantilla.** Siempre explícita:

```
python3 personaje_v2/scripts/pipeline.py CARPETA --config personaje_v2/config_v2_v64_experimental.json
```

El expediente tiene que traer `configuracion_economica.json`. Su formato está en `personaje_v2/scripts/configuracion_economica.py` y lo escribe la orquestación, nunca un agente de juicio. El pipeline se detiene con código 2, sin escribir nada, si:

- falta la configuración o no es válida;
- el expediente se preparó con otra plantilla: un expediente V6.4 que se ejecuta con la V6.3 y, al revés, uno que empezó con la V6.3 que se ejecuta con la V6.4. Este último se reconoce porque tiene libros `*_v63_base.xlsx`, `*_v63_datos.xlsx` o `*_v63_evaluada.xlsx`, o un `estado_pipeline.json` con pasos hechos, y no tiene `plantilla_activa.json` (revisión interna H1);
- una configuración V6.4 llega con la configuración V6.3.

**Expediente nuevo para la V6.4.** Se prepara con `cambiar_base.py` o, si la base no cambia, en una carpeta nueva con solo las entradas de partida: `etapa1/`, `fase1_v63.json` y `configuracion_economica.json`. No se copian libros, `estado_pipeline.json` ni salidas de una ejecución V6.3.

**Motor elegido por la fase A.** La fase A elige el motor por los criterios del personaje, como si la configuración no existiera (`prompts/fase_a.md`). `entrada_v63.md` separa «no calculable por datos» de «no cubierto por la configuración experimental». Si la fase A elige el motor A o el C con el modo experimental, el expediente termina en `no_entregable · limite_del_modelo`, con «qué hace falta»: modo heredado o la V6.3 en un expediente nuevo. No termina en una falta de datos (revisión interna H3).

**Archivos y pasos.**

- `plantilla_activa.json` registra la plantilla, la referencia y el verificador, con sus huellas.
- Paso 2: el pipeline aplica la configuración al libro de datos.
- Paso 10: calcula `configuracion_v64_variantes.json/.md`, con las variantes heredado, activa, componentes aislados, estructuras compatibles y convenciones, sobre copias recalculadas. Si la configuración declara `PM1.lambda_rango` o `PM1.theta_rango` ([mín, máx], con el valor activo dentro), añade los dos extremos (`parametro_minimo` y `parametro_maximo`). La fase C las evalúa en `configuracion_v64`: cada parámetro activo, el mantenimiento con `adoptada = false`, y la zona solo respecto de variantes calculadas.
- Una variante sin zona impide afirmar «misma zona en todas» (`variantes_sin_zona`), y la ficha cuenta solo las calculadas.
- Paso 12: la variante «activa» tiene que reproducir `precio.json` (ponderado y precio de Sí, 1e-9) y las variantes tienen que ser de la configuración actual. Si no, el expediente termina en `no_entregable · fallo_de_implementacion` (revisión interna H10).
- Resumen: las filas de los expedientes V6.4 se publican en `resumen_v2_v64_experimental.csv`, en la carpeta que contiene el expediente, y nunca en el `resumen_v2.csv` de las filas V6.3 (revisión interna H2). El nombre lo fija `config_v2_v64_experimental.json` (`resumen_csv_nombre`) y, sin él, lo decide `plantilla_activa.json` del expediente, así que se mantiene también en una llamada a mano con `config_v2.json`. El historial de las filas retiradas es `resumen_v2_v64_experimental_historial.csv`. La fila no lleva columnas de plantilla, modo ni marca de objetivo provisional: el archivo identifica la plantilla y la ficha y el informe dan el resto. Excepción: una configuración con `resumen_csv` (una ruta fija) manda sobre todo lo anterior; ni `config_v2.json` ni la de la V6.4 lo tienen.

**Ejecución a mano.** `ficha.py`, `informe.py` y `resumen.py` no comprueban la selección de plantilla. Sobre un expediente V6.4 se ejecutan con `MUNGER_CONFIG=personaje_v2/config_v2_v64_experimental.json`, que es como los llama el pipeline. Sin esa variable cargan `config_v2.json` para todo lo demás (revisión interna O5).

**Vigencia.** La configuración, la selección y las variantes forman parte del material auditado. Si la configuración cambia después del cierre:

1. `informe.py` y `ficha.py` retiran la aprobación en la primera llamada;
2. el pipeline reaplica la configuración, recalcula y pide variantes, fase C y auditoría nuevas.

## 8. Límites conocidos

1. **Terminal con R1 en el MALO** (observación de la réplica independiente, no una discrepancia). El terminal no aplica la regla del máximo conservado: carga la inversión fija para crecer al ritmo g aunque las ventas del año 11 sigan por debajo del máximo. Ejemplo: 16,39 millones en el MALO de `H_L1.15`. Es la definición de la 4.7.1 y la 4.8.1, y es prudente: da menos valor en el MALO. Una alternativa que reconozca la capacidad sobrante en la perpetuidad está sin especificar.
2. **Crédito terminal en H.** La fórmula min(req₁₁, max(0, fija₁₁)) coincide con la forma literal de la 4.8.1 solo si fija₁₁ ≥ 0, que es lo que ocurre en todos los casos calculados. Ningún caso tiene inversión fija terminal negativa.
3. **Ramas heredadas sin caso propio.** Quiebra > 0 y base «Último año» no tienen caso en la V6.4. Son ramas de la V6.3, sin cambios.
4. **Recálculo.** Los valores salen de LibreOffice (recálculo forzado, siempre en secuencia). Un libro escrito y no recalculado no tiene valores válidos.
5. **Precio de Sí.** Es min(P*, V NORMAL), con k = 3, que sigue siendo una convención experimental. En ningún caso calculado actúa el tope: P* ≤ 0,94 × V NORMAL.
6. **Alcance.** Solo motor B. Los motores A, C y D no cambian. Con el modo experimental y otro motor, la configuración se rechaza en el libro (comprobación 2) y, en el pipeline, el expediente termina en el límite del modelo (§7).
7. **λ y θ son hipótesis, no mediciones.** La plantilla las calcula con el valor que se le da. Que una describa a la empresa no lo prueba la plantilla.
8. **Palanca S2C inerte con R1** (revisión interna H12). Con R1, en un escenario cuyas ventas no superan en ningún año el máximo anterior, la inversión fija para crecer es 0 y la palanca S2C no actúa. Ocurre en el MALO del piloto.
9. **Dominios que no se comprueban** (revisión interna H13). En el piloto y en los 117 casos no aparece ninguno; no hay aviso automático.
   - **f sin cota superior.** Solo se exige D_hist − Rh > 0. Con los datos del piloto, f es 1,16 con λ = 1,15, 1,89 con λ = 1,5 y 17,8 con λ = 2,0, y deja de estar definida en λ ≈ 2,06 (cifras de la revisión interna, comprobadas con las bases del libro del piloto: D_hist 530,009 y Σ amortización que se repone 500,209). El valor no se dispara, pero el S2C reestimado pierde sentido mucho antes.
   - **Inversión fija para crecer negativa.** El término (1 ÷ (S2C·f) − NWC) es negativo si S2C·f > 1 ÷ NWC. Puede ocurrir con f = 1 en una empresa con poco activo fijo y mucho circulante (por ejemplo, S2C = 4 y NWC = 0,30).
   - **Inversión fija terminal negativa.** Además del crédito de H (límite 2), afecta a SRF: f_fija reduciría una liberación en lugar de una inversión.
   - **g ≤ 0 con R1.** El terminal no aplica el máximo conservado en ningún sentido. El pipeline acota g ≥ 0 con la gramática; un libro escrito a mano admite de −10 % a 10 % (regla V15).
10. **Lecturas.** BL no incluye la cartera P0 (§5). Diagnóstico B177 queda vacío con g = 0 (no hay crecimiento terminal que medir).
11. **Controles mecánicos con la base histórica** (revisión interna O4). La regla G7 de la gramática y las referencias mecánicas usan el tipo de la Historia y el S2C sin f también en modo experimental (diseño declarado en `prompts/fase_b.md`). En ese modo, la rentabilidad marginal que vigila G7 no es la que calcula el motor.
12. **«Conciliación B» es un control aritmético** (revisión interna O1). Sus partidas salen de las mismas columnas del motor. La amortización del terminal se muestra siempre proporcional a las ventas, con cualquier convención: se cancela en la identidad y solo afecta a la presentación.

## 9. Encargo 4.12: la plantilla no cambia; lo que añade el pipeline y lo que se ha observado

**La plantilla y su referencia son las de la 4.11, byte a byte.** Lo nuevo está en el pipeline y en los módulos de `personaje_v2/scripts/` (formatos en el Anexo D §D.13):

- **Vigencia antes del rechazo.** Si el material auditado cambió, la primera llamada retira la aprobación antes de rechazar una selección incoherente.
- **Protocolo experimental del objetivo** (`objetivo_v64.py`). Distingue el valor calculado condicional del precio objetivo emitido. Ninguno de los dos protocolos está adoptado.
- **Variantes en formato «4.12».** Atadas a la instantánea de las entradas económicas del libro y a la huella económica de la configuración.
- **Avisos de dominio con sus valores** (`dominios_v64.py`). Cubren el límite 9 en los expedientes, sin umbrales adoptados: la plantilla sigue sin comprobarlos.
- **Cadena de trazabilidad** (`trazabilidad_v64.py`).
- **Salidas del objetivo.** La línea de estado del informe da el rango calculado y su ámbito con cualquier tratamiento del objetivo (corrección tras la auditoría del cierre de bloqueo de Vidrala).
- **Aptitud de uso separada de la auditoría** (`ficha.json → aptitud_de_uso`, sección 1 del informe y columna del resumen V6.4). Mientras el resultado sea experimental lo dice expresamente: ni el estado «concluido» ni una auditoría APROBADO lo hacen apto para decidir con dinero real.

**Límites observados al contrastar con Viscofan** (`…_4_12/viscofan/configuracion/analisis_configuracion_viscofan.md`):

13. **La D&A de la Historia incluye la amortización de los derechos de uso (NIIF 16).** Esa parte se repone con arrendamientos, que son financiación, y no con capex. La plantilla no la separa, y eso tiene dos efectos:
    - la base de Λ (D&A₀ y Σ amortización que se repone) incluye una parte que no se repone con capex;
    - el exceso de Θ (Σ capex − D&A) queda por debajo del exceso sobre la amortización que sí se repone con capex.

    En Viscofan son 5,1–5,8 M€ al año: 27,1 M€ en 2021–2025, frente a un exceso de 40,8 M€. Es un límite de definición, no de cálculo.
14. **El dominio de SRF con Λ depende de las bases de cada empresa.** f_fija = 1 − (λ − 1) × Σ amortización que se repone ÷ F_hist. La comprobación 25 rechaza f_fija < 0.
    - Viscofan: Σ amortización que se repone es 403,1 y F_hist 57,0, así que SRF solo está definida hasta λ = 1,1413, y f hasta λ = 1,7355.
    - Vidrala: F_hist es 251,2, así que SRF está definida hasta λ ≈ 1,50.

    Con Θ, f_fija = 1 − θ × exceso ÷ F_hist ≥ 0 en todo [0, 1] siempre que el exceso no supere F_hist.
15. **Circulante alto.** Con NWC = 48,3 % (Viscofan), la inversión fija para crecer de R1 es negativa si S2C × f > 1 ÷ NWC ≈ 2,07. El pipeline calcula los avisos de `dominios_v64.py` sobre la variante **activa**; los de las demás variantes no van en sus salidas y se leen aparte (en la 4.12, `…_4_12/resultados/dominios_variantes_4_12.md`: el extremo λ = 1,25 de Vidrala lleva f = 1,309, y en Viscofan no hay ningún aviso activo en ninguna variante).

**Revisión interna de la 4.12 (pipeline, no plantilla).** La instantánea de las entradas económicas y la cadena de trazabilidad incluyen la fila 13 de la Historia (adquisiciones netas), que entra en D_hist y F_hist; una hipótesis que condiciona el objetivo solo cuenta como cubierta por el ámbito si alguna variante calcula una alternativa suya (un subparámetro de P-M1, de forma aislada); y la cadena avisa de fechas o resultados de los textos de evidencia del precio, la capitalización y las acciones que no corresponden al valor.
