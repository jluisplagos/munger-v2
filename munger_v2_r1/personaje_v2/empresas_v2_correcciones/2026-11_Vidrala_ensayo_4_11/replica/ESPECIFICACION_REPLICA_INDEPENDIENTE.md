# Especificación de la réplica independiente · V6.4 experimental del motor B (encargo 4.11 §8)

**Para quién.** Para el agente que escribe la réplica en contexto separado. **No** debe leer las fórmulas del Excel de la V6.4 (`v6/v64_experimental/scripts/construir_v64_experimental.py`, la hoja «Configuración V6.4» como fórmulas, las columnas BU:DY del Motor ni la hoja «Conciliación B» como fórmulas). La réplica se escribe desde las definiciones de este documento, del encargo y de los análisis fuente. Lee **valores** de los libros recalculados para comparar.

## 1. Archivos

- **Casos:** `…/2026-11_Vidrala_ensayo_4_11/scripts/casos_v64.py` (entradas, no fórmulas).
- **Libros recalculados:** `<DIR>/rc/<id>.xlsx`. Manifiesto en `<DIR>/manifiesto_casos.json`, con el caso, las entradas, si el recálculo fue bien y la ruta.
- **Fuentes de las definiciones (lectura permitida):**
  - 4.7.1: `…_4_7_1/scripts/analisis_n1_n3.py` (`r_op`, `proyeccion`, `valor`, `escalera`);
  - 4.8.1: `…_4_8_1/scripts/analisis_reinversion_4_8_1.py` (`req_lambda`, `req_nivel`, `valorar`, `f_desc`, `kw_estructura`);
  - 4.8: `…_4_8/scripts/analisis_pm1.py` (cartera P0).
- **Prohibido:** `personaje_v2/scripts/precio_de_si.py` sí puede leerse (es heredado). Los scripts de la V6.4 y las fórmulas nuevas del libro, no.
- **Salidas:**
  - `…/2026-11_Vidrala_ensayo_4_11/scripts/replica_independiente_v64.py`;
  - `…/2026-11_Vidrala_ensayo_4_11/replica/replica_resultados.json`;
  - `…/2026-11_Vidrala_ensayo_4_11/replica/replica_salida.txt`.
- **Uso:** `python3 -I replica_independiente_v64.py <DIR>` (código 0 si todo coincide; 1 si no).
- **Sin LibreOffice:** solo `openpyxl` con `data_only=True`.

## 2. Entradas que lee la réplica (valores de celdas de entrada o de datos)

**Historia** (columnas C..L = años 1..10; L = último año):

| Fila | Contenido |
|---|---|
| 5 | año |
| 6 | ventas |
| 7 | EBIT |
| 8 | D&A |
| 10 | tipo efectivo |
| 12 | capex |
| 13 | adquisiciones netas |
| 14 | aumento del circulante |
| 15 | intereses pagados |
| 22 | deuda |
| 23 | arrendamientos |
| 24 | caja |
| 25 | pensiones |
| 26 | minoritarios |

**Palancas:**
- C8: base del margen, «Último año» o «Media del ciclo».
- B14:D14: crecimiento de los años 1–5 (MALO, NORMAL, BUENO).
- B15:D15: margen objetivo.
- B16:D16: S2C.
- B18:D18: ROIC a largo plazo.
- C22 y C23: probabilidad de quiebra y recuperación. Vacío = 0.

**Análisis:**
- B68:D68: g para siempre.
- B69:D69: probabilidades.
- C41: E, la capitalización.
- C55: N, las acciones en millones.
- C56: r.

**Configuración V6.4** (solo las celdas de entrada): B4, B11:B16, B21:B23, B28:B32, B36:B51. Sus significados están en el §3.

Los cálculos derivados de la Historia los hace la réplica:

| Concepto | Cálculo |
|---|---|
| V0 | L6 |
| Margen anual | EBIT ÷ ventas |
| m0 heredado | «Último año» → L7/L6. «Media del ciclo» → media de los diez márgenes (todos los años con ventas). Vacío → como «Último año» |
| t de la Historia | media de H10:L10 |
| D (deuda + arrendamientos) | L22 + L23 |
| Coste de la deuda i | L15 ÷ ((K22 + K23 + L22 + L23) ÷ 2) |
| Puente | (L22 + L23) + (max(0, L25) + L26) − L24 |
| Reinversión neta total del año y | capex − D&A + Δcirculante + adquisiciones (filas 12 − 8 + 14 + 13) |

## 3. Modelo

### 3.1 Motor B heredado (V6.3; también el modo experimental sin cambios efectivos)

Escenario s = (g1, m_obj, S2C, ROIC, g), con m0, t, r_op, N y el puente:

- g_t = g1 si t ≤ 5; si 6 ≤ t ≤ 10, g_t = g1 − (g1 − g)·(t − 5)/5.
- V_t = V_{t−1}·(1 + g_t), con V_0 = V0.
- m_t = m0 + (m_obj − m0)·min(t, 5)/5.
- FCF_t = V_t·m_t·(1 − t) − (V_t − V_{t−1})/S2C, para t = 1..10.
- Terminal: FCF_11 = V_10·(1 + g)·m_obj·(1 − t)·(1 − g/ROIC); TV = FCF_11/(r_op − g).
- VP = Σ FCF_t/(1 + r_op)^t + TV/(1 + r_op)^10.
- Valor por acción = ((1 − p)·(VP − puente) + p·recuperación)/N.
- r_op = (r·E + i·(1 − τ_escudo)·D)/(E + D). En el heredado, τ_escudo = t = t de la Historia.
- Ponderado = Σ p_s·V_s (Análisis C83).
- Precio de Sí: el precio más alto P con G(P) ≥ k·L(P), con k = 3.
  - G(P) = Σ p·max(V − P, 0).
  - L(P) = Σ p·max(P − V, 0).
  - Si sale por encima del NORMAL, se toma el NORMAL. Es la convención de `precio_de_si.py`: comprobar si esa forma cerrada ya acota en V_NORMAL, y reproducir lo que hace ese script.

### 3.2 Modo y validez

- **Modo:** B4 vacío → Heredado. «Heredado» → Heredado. «Experimental» → Experimental. Cualquier otro texto → **no válido**: la réplica marca el caso como rechazado.
- **En modo Heredado**, todo lo demás de la hoja se ignora, aunque esté escrito.
- **En modo Experimental:**
  - solo con el motor B (Análisis C62 = «No · financiación cambia mucho»). Con otro motor, el caso se rechaza;
  - una entrada obligatoria que falte o un valor fuera de su dominio rechazan el caso. Las reglas están en el §3.3; no se recorta nada.

### 3.3 Entradas experimentales

**N1 · B11, tipo normalizado.**
- Vacío → t = t de la Historia.
- Un número en [0, 1) → t = B11, que se aplica al NOPAT de los años 1–10 y del terminal.
- Si hay número, son obligatorios:
  - B12, B13 y B14: fuente, período y perímetro, no vacíos;
  - B15: la clase, una de «dato publicado», «derivado de datos publicados», «convención» o «hipótesis»;
  - B16: el escudo, «Vinculado al tipo aplicado a NOPAT» (τ_escudo = t aplicado) o «Tipo de la Historia (separado)» (τ_escudo = t de la Historia).
- r = Análisis C56 no cambia; r_op se recalcula con τ_escudo.

**N2 · B21, margen de partida manual.**
- Vacío → m0 heredado.
- Un número en (−1, 1) → m0 = B21. El 0 es válido.
- Con número, B22 y B23 son obligatorios (no vacíos).
- El margen de partida (año 0) no es el margen objetivo del NORMAL.

**N3 · B28, regla de reinversión.** Obligatoria: «R0 · simétrica (heredada)» o «R1 · solo circulante; capacidad conservada».
- NWC = (B29 + B30 − B31)/V0. Con R1 son obligatorios los tres números, todos ≥ 0.
- **R0:** reinversión = ΔV_t/S2C, en las dos direcciones. Presentación: Δcirc_t = ΔV_t·NWC, con NWC = 0 si no hay datos, y fija_t = ΔV_t/S2C − Δcirc_t.
- **R1:** pico_t = max(V_0 … V_{t−1}).
  - Δcirc_t = ΔV_t·NWC en todos los casos: libera al caer y repone al recuperar.
  - Inversión fija para crecer: fija_t = max(0, V_t − pico_t)·(1/S2C_ef − NWC)·f_fija.
  - Con ventas que caen o por debajo del máximo conservado, la fija es 0.
  - Por encima del máximo: (V_t − pico_t)/S2C_ef menos su circulante.

**P-M1.** Solo con R1. R0 con P-M1 se rechaza: «R0 + P-M1 no está especificado».
- **B36, estructura.** Obligatoria. Una de:
  - «Sin requisito adicional»;
  - «H · hueco (crédito de la inversión para crecer)»;
  - «S · suma sin reestimar»;
  - «SR1 · suma con S2C reestimado»;
  - «SR2 · suma con S2C y ROIC reestimados»;
  - «SRF · suma con inversión fija reestimada».
- **B43, cartera.** Obligatoria: «Legado · se repone con la amortización» o «P0 · no se repone (explícito)».
- **P0:**
  - B44 = amortización anual prevista de la cartera (CLa); B45 = valor neto (VNC);
  - B46:B50 = amortización de la cartera de los años H..L. Los cinco son obligatorios; 0 explícito si no la hubo. Todo ≥ 0;
  - VNC > 10·CLa se rechaza;
  - cl_k = min(CLa, max(0, VNC − CLa·(k − 1))) para k = 1..10; en el terminal, 0;
  - la cartera no repuesta se suma al FCF de cada año (cl_k);
  - con P0 sin requisito adicional («Sin requisito adicional» + P0), la cartera también entra, y exige R1.
- **Con requisito adicional** (estructura ≠ «Sin requisito adicional»), son obligatorios:
  - B37, la familia: «Λ · (λ − 1) × amortización que se repone» o «Θ · θ × exceso histórico medio»;
  - B38: λ ≥ 1 (Λ);
  - B39: θ en [0, 1] (Θ);
  - B40, años 1–10: «Plana» o «Proporcional a las ventas»;
  - B41, terminal: «Proporcional a las ventas» o «Crece con g»;
  - B42, ROIC: «ROIC × f (SR2)» si la estructura es SR2, y «ROIC de la fase B sin cambio» en las demás. Otra combinación se rechaza;
  - las bases históricas de los cinco años H..L completas: filas 31 (reinversión neta), 12 y 8.

**Bases históricas** (años H..L; ΣCart = Σ B46:B50 con P0, y 0 con legado):

| Base | Definición |
|---|---|
| D&A₀ | Historia L8 |
| D_hist | Σ reinversión neta total H..L + ΣCart |
| Exceso acumulado | Σ(capex − D&A) H..L + ΣCart |
| Exceso medio | exceso acumulado ÷ 5 |
| F_hist | exceso acumulado + Σ adquisiciones H..L |
| Σ amortización que se repone | Σ D&A H..L − ΣCart |

**Requisito anual del año t:**
- Λ: (λ − 1)·(D&A₀·a_t − cl_t), con a_t = 1 (plana) o V_t/V0 (proporcional).
- Θ: θ·(exceso medio)·a_t.

**Requisito del terminal:**
- Λ: (λ − 1)·D&A₀·b.
- Θ: θ·exceso medio·b.
- b = V_10·(1 + g)/V0 (proporcional) o (1 + g) (crece con g).

**Rh** (parte de D_hist atribuida a la reposición):
- Λ: (λ − 1)·Σ amortización que se repone.
- Θ: θ·exceso acumulado.

**Factores:**
- f = D_hist/(D_hist − Rh), en SR1 y SR2. Exige D_hist > 0 y D_hist − Rh > 0; si no, el caso se rechaza.
- f_fija = 1 − Rh/F_hist, en SRF. Exige F_hist > 0 y f_fija ≥ 0; si no, se rechaza.
- El requisito a ventas constantes (Λ: (λ − 1)·D&A₀; Θ: θ·exceso medio) < 0 se rechaza.
- Λ con P0 y CLa > D&A₀ se rechaza.

**Por estructura:**

| Estructura | S2C_ef de los años | ROIC del terminal | f_fija | Crédito |
|---|---|---|---|---|
| H | S2C | ROIC | 1 | crédito_t = min(req_t, max(0, fija_t)) |
| S | S2C | ROIC | 1 | 0 |
| SR1 | S2C·f | ROIC | 1 | 0 |
| SR2 | S2C·f | ROIC·f | 1 | 0 |
| SRF | S2C | ROIC | f_fija | 0 |
| Sin requisito | S2C | ROIC | 1 | 0 (req = 0) |

**FCF experimental de los años 1–10:**
FCF_t = V_t·m_t·(1 − t) + cl_t − fija_t − Δcirc_t − req_t + crédito_t.
Equivale a NOPAT + D&A − inversión fija bruta − Δcirc, con inversión fija bruta = (D&A − cl) + fija + (req − crédito).

**Terminal experimental:**
- NOPAT_11 = V_10·(1 + g)·m_obj·(1 − t).
- Δcirc_11 = V_10·g·NWC.
- fija_11 = (NOPAT_11·g/ROIC_ef − Δcirc_11)·f_fija.
- req_11 según lo anterior. crédito_11 = min(req_11, max(0, fija_11)) solo en H.
- FCF_11 = NOPAT_11 − fija_11 − Δcirc_11 − req_11 + crédito_11; TV = FCF_11/(r_op − g).
- Con R1 sin P-M1, FCF_11 = NOPAT_11·(1 − g/ROIC), igual que el heredado.

El valor por acción, el ponderado y el precio de Sí se calculan como en el §3.1.

## 4. Comparaciones que debe hacer la réplica, caso a caso

**1. Validez.**
- Si la réplica rechaza el caso, el libro no debe calcular: Análisis B78:D78 no son números y Motor D237 (V35) = «INCOMPLETO».
- Si la réplica no lo rechaza, el libro debe calcular.
- En los casos `rechazo_*`, el motivo del libro (`Configuración V6.4` B8) contiene `motivo_esperado`.

**2. Valores**, con tolerancia de 1e-9 €/acción:
- V_MALO, V_NORMAL, V_BUENO frente a Análisis B78, C78 y D78;
- el ponderado frente a C83;
- el precio de Sí, sin celda en el libro: se compara con `referencia.precio_si` cuando el caso la trae;
- si `referencia` existe, comparación con su tolerancia (`tol` y `tol_V`).

**3. Flujos** (tolerancia relativa 1e-9 sobre la escala de las ventas): FCF_t (t = 1..10) y FCF_11 de los escenarios MALO, NORMAL y BUENO frente a Motor AU6:BD8 y BF6:BF8.

**4. Conciliación**, hoja «Conciliación B». Los bloques empiezan en las filas 5 (MALO), 35 (NORMAL) y 65 (BUENO); columnas B..K = años 1..10 y L = terminal. Partidas, en filas relativas al bloque:

| Fila | Partida |
|---|---|
| +2 | ventas |
| +3 | máximo conservado |
| +5 | NOPAT |
| +7 | cartera |
| +9 | requisito |
| +10 | fija para crecer |
| +11 | crédito |
| +13 | Δcirc |
| +17 | FCF del motor |

Se compara cada una con la réplica.

**5. Filas de sensibilidad, tornado y DCF inverso** (Motor, filas 9–136 con fórmula en AU):
- la réplica toma de cada fila sus parámetros C..P (C V0, D m0, E g1, F m_obj, G S2C, H g, I ROIC, J r, K t, M ajuste = −puente, N p, O recuperación, P N);
- recalcula el valor por acción BK con el modelo activo (§3);
- compara con BK, con 1e-9.
Así se comprueba que la tabla del DCF inverso y el tornado usan el modelo activo.

**6. Identidades:**
- crédito = 0 fuera de H, también en el terminal;
- 0 ≤ crédito ≤ min(req, max(0, fija)) en H;
- en SRF el Δcirc es el de S, fila a fila;
- con Rh = 0, SRF = S (casos SRF_L1.00 y S_L1.00);
- con θ = 0, f = 1.

**Informe:**
- `replica_resultados.json`: por caso, rechazado o no, las diferencias máximas por grupo y si pasa;
- `replica_salida.txt`: legible, con el resultado global.

La réplica **no** corrige ningún archivo del paquete. Si encuentra una discrepancia, la informa con el caso, la celda, el valor del libro y el de la réplica.
