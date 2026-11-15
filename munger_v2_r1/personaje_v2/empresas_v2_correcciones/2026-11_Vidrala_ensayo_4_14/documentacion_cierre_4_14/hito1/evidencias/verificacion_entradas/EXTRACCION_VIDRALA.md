# Informe del extractor: verificación de entradas de Vidrala (4.14)

Extractor: agente extractor E-Vidrala (Claude), 14-nov-2026. Este registro es solo del extractor. **Ninguna entrada está comprobada todavía.** Falta la revisión independiente: los campos `revisor`, `fuente_examinada` y `resultado` están vacíos o en «pendiente».

- **Registro:** `/home/claude/trabajo_4_14/agentes/E_vidrala/Vidrala/verificacion_entradas.json`. La plantilla se conserva al lado.
- **Constructor reproducible:** `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/construir.py`. Comprueba que cada cita está, literalmente, en su página.

## 1. Preparación

- **Copia del expediente:** se copió `vidrala_condicionado/Vidrala` sin `recalc/`, `variantes_v64/` ni `prompts_generados/`.
- **Mismas entradas en los dos libros:** `entradas_economicas.instantanea` da 226 celdas, con la huella `5d6686198fcea86575ee25d00919fd88704c272cc5a653872f5566f969cfc79e`. Coincide en:
  - `vidrala_condicionado`;
  - `vidrala_bloqueo`;
  - la copia de trabajo.

  La comparación con `diferencias` da 0 diferencias: el material de entradas es el mismo.
- **Valores del libro y de la extracción:** los valores de la Historia del libro son idénticos a los de `fase1_v63.json`.
- **Perímetro del expediente:** se declara `consolidado`. En la práctica es **mixto por partida**:
  - **Consolidado:** balance, flujos, beneficio neto y la Historia de 2016 a 2022. Incluye Italia hasta su venta en 2024 y Brasil desde noviembre de 2023.
  - **Operaciones continuadas:** la cuenta de resultados de 2023 y 2024 (ventas, EBIT, D&A, impuesto y BAI), tomada de comparativos reexpresados. Cada una de estas entradas lleva su `perimetro_justificacion`.
  - **2025:** no tiene operaciones interrumpidas, así que consolidado y continuadas coinciden.
  - **Configuración:** B11 y B21 son de continuadas; B21 aproxima 2020–2022 restando el segmento Italia.
  - **P1:** aplicado (K14 = 84,994).

## 2. Recuentos

**Universo:** 226 celdas, una entrada por celda, sin repetidas ni sobrantes. Se añaden **119 datos de origen auxiliares** (`aux:…`), que se cuentan aparte.

| Clase | Celdas del universo | Auxiliares |
|---|---|---|
| dato_publicado | 114 | 116 |
| derivado | 58 | 0 |
| cero_comprobado | 5 | 3 |
| no_aplicable | 5 | 0 |
| hipotesis | 27 | 0 |
| convencion | 17 | 0 |
| dato_ausente | 0 | 0 |

**Resultado de `verificacion_entradas.py comprobar --json`:**

| Concepto | Resultado |
|---|---|
| Errores | 0 |
| Discrepancias | 0 |
| Desactualizadas | 0 |
| Sin entrada, sobrantes o repetidas | 0 |
| Pendientes | 301 |
| Comprobadas | 44 |
| Materiales sin comprobar | 182 |
| Apto por entradas | False |

- **Las 44 «comprobadas»** son las hipótesis y convenciones. El contrato no les exige revisor; no son datos verificados.
- **Las 301 pendientes** se explican por la falta de revisor (243 entradas) y por derivados cuyo origen sigue pendiente (58).

**Simulación de revisión:** se hizo una revisión ficticia sobre una copia temporal, ya borrada, para probar las fórmulas. Todas reproducen el libro, salvo **C46 y C47**: son las dos discrepancias reales registradas en la sección 3.

**Ceros, clasificados uno a uno:**

| Grupo | Celdas | Cómo se comprueba |
|---|---|---|
| Cero impreso «-» | C13 (2016) e I13 (2022) | Celda `cero_comprobado` |
| Cero impreso «-» | B46, B47 y B48 (cartera de clientes 2021–2023) | Celda `cero_comprobado` |
| Cero por conciliación del total de inversión | E13, F13, G13, H13 y L13 | Derivado = 0 |
| Cero por conciliación del balance (minoritarios) | C26 a L26: patrimonio neto y pasivo − pasivo − patrimonio de la dominante = 0 | Derivado = 0 |
| No aplicable (antes de NIIF 16) | C23, D23 y E23 | `no_aplicable`. La representación como 0 sigue en D-N4-na, sin confirmación humana |
| Cero no confirmado | C48 | Se deja **pendiente** (sección 3) |

**Ceros heredados fuera del universo:**
- `intereses_financiacion` de 2016 a 2022, `arrendamientos_principal` de 2016 y 2018, y `otros_activos_financieros` no entran en ninguna celda del libro.
- Al revisar todos los balances de 2016 a 2025 se vio que no hay inversiones financieras corrientes. Queda reflejado en el `tratamiento` de la fila 24.

## 3. Incidencias (con evidencia)

1. **Análisis!C46, CFO medio · DISCREPANCIA del extractor (inmaterial).**
   - **El libro:** 335,4.
   - **La fuente:** (263,437 + 362,516 + 380,287) ÷ 3 = **335,413**, según CF_2024 p.7 y CF_2025 p.7.
   - **Causa:** es la «precisión de referencia» heredada de la etapa 1, declarada en `fase1_v63.json`. La fórmula queda fuera de la tolerancia de 0,0011.
2. **Análisis!C47, capex medio · DISCREPANCIA del extractor (inmaterial).**
   - **El libro:** 169,7.
   - **La fuente:** (151,700 + 168,800 + 188,503) ÷ 3 = **169,668**.
   - **Causa:** la misma que en C46.
3. **Historia!F8, D&A de 2019 · DISCREPANCIA de concepto.**
   - **El libro:** 97,091 = 91,088 + 6,003 de deterioro (CF_2020 p.13).
   - **El resto de la serie** excluye el deterioro. El valor coherente es 91,088.
   - Es la incidencia Y-1 ya conocida (CONTINUIDAD §9.6), todavía sin corregir. La fórmula reproduce el libro.
4. **Análisis!C48 = 0, cero no confirmado.**
   - **Lo que se ve:** el bloque de financiación de 2023 a 2025 no tiene línea de intereses, y su total cuadra con sus líneas (CF_2024 p.7 y CF_2025 p.7).
   - **Lo que falta:** se desconoce en qué línea van los pagos por arrendamientos. Su interés devengado es de 2,131, 2,179 y 2,452 miles (Q-N4a, D-N4-C48, P3).
   - Por eso queda pendiente.
5. **Análisis!C49 = 4,5, registrado como hipótesis.**
   - Es un supuesto heredado, no un principal publicado.
   - La nota 8 solo da el pago total: 5,861, 6,117 y 8,314 miles, con media 6,764.
   - Si al pago se le resta el interés devengado, la media queda en unos 4,510.
6. **Análisis!C50 = 0, SBC.**
   - No hay cifra ni una afirmación expresa de que no existan planes para todo el grupo.
   - El informe de remuneraciones (ES 2025 p.357) solo da 0,00 en los planes de los consejeros.
   - Se registra como hipótesis, porque el contrato no admite `dato_ausente` cuando la celda tiene un valor.
7. **Configuración B46 a B48, cartera de clientes.**
   - El 0 es correcto: la nota imprime «-».
   - Pero la justificación de `configuracion_economica.json` falla:
     - para 2021 y 2022 dice «no había cartera», cuando sí había una cartera de 13,237 totalmente amortizada (CF_2022 p.44);
     - para 2023 dice «supuesto», cuando la nota publica «-» (CF_2023 p.46).
8. **Notas sin discrepancia** (están en las entradas):
   - **J14:** el 78,805 de 2023 incluye la reclasificación de 11,061 de Italia. Es la decisión de perímetro P7, pendiente.
   - **I14:** el subtotal de CF_2023 es (117,545), 1 miles distinto de la suma de líneas. En CF_2022, la línea de acreedores (132,341) es una errata.
   - **G23:** el saldo de 1,303 viene rotulado «At December 31 2019», por errata (CF_2020 p.20).
   - **H23:** el pasivo NIIF 16 de 2021 no se publica por separado. Se registra como convención: el pasivo queda dentro de la deuda.
   - **Capex:** los rótulos están desplazados en 2018–2021 y la traducción dice «Payments from sale» en 2022–2025.
   - **C8:** el estado de flujos da 75,557 y la cuenta de resultados, 75,556.
   - **D13:** se cita CF_2017, porque el comparativo de CF_2018 solo trae una cifra.
   - **K13:** se excluye la compra de una sociedad por puesta en equivalencia (6,000). Es dudoso que «Other effects of disposal» (11,668) pertenezca a la venta.
   - **Fila 22, deuda:** incluye «Finance Lease - Others», unos 60 mm, según la regla de `fase1_decisiones.json`.
   - **Fila 25, pensiones:** la provisión «Personnel» incluye otras obligaciones con empleados.
   - **B21:** el EBIT de Italia de 2020–2022 es una aproximación (BAI del segmento + gastos financieros − ingresos financieros).

## 4. Fuentes que faltan

| Dato | Período | Documento necesario |
|---|---|---|
| Bytes y huella de los PDF originales de CF_2016 a CF_2022. Solo se conservan los .txt, cuya huella está registrada; para 2023–2025 los PDF están en `contrastes/` | 2016–2022 | PDF de las cuentas consolidadas, CNMV |
| Principal e interés pagados de arrendamientos, y en qué línea del estado de flujos van (C48, C49; Q-N4a) | 2023–2025 | Consulta a Vidrala o desglose del ESEF |
| Gasto por pagos basados en acciones de todo el grupo, o la afirmación expresa de que no existe (C50) | 2023–2025 | Nota de gastos de personal o de remuneración de la alta dirección |
| Pasivo NIIF 16 separado (H23) | 31-dic-2021 | Cuentas 2021 en español o ESEF |
| EBIT publicado del segmento Italia, para sustituir la aproximación de B21 | 2020–2022 | Información por segmentos con el resultado de explotación |
| Circulante de 2023 solo de continuadas (P7) | 2023 | Desglose de Italia en el flujo reexpresado |
| Composición de «Other effects of disposal» (K13) | 2024 | Nota 5 o consulta a Vidrala |
| Boletín de cotización de BME para el precio de C37 (D-N6) | 31-dic-2025 | Boletín de BME |

No se ejecutó LibreOffice ni el pipeline, y no se tocaron la base ni `trabajo/`.
