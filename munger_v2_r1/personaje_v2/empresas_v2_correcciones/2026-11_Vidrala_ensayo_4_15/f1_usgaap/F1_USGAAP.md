# F1 · US GAAP (ASC 842) · motor A con arrendamientos operativos y financieros

Fecha: 18-nov-2026. Lo escribe el agente autor de la reparación (Claude, modelo Fable 5.2) en la rama `f1/usgaap`, creada desde
`examen/ahold-f1` @ `1694f08`. **Ronda 2.** La ronda 1 (`34b68fc`) la revisó otro agente: veredicto CORRECCIONES acotadas
(`munger-v2-evidencias-mistral`, `coordinacion/cierre_v2/examen/revisiones/f1_usgaap/REVISION_R1.md`). Este documento describe el
estado después de esas correcciones y de las dos decisiones que la persona responsable tomó tras la revisión. **La ronda 2 no está
revisada todavía.** Se distinguen **hechos** (comprobados con una prueba o un archivo), *interpretaciones* y ***propuestas***.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** Superar estas guardas no acredita aptitud.
La V6.3, la V6.3.1 F1 (`eaece01a…`), sus referencias y los expedientes hechos con ellas **no cambian**. NIIF no cambia de valor (§8).

## 0. Ronda 2: hallazgo → cambio → prueba

Pruebas: **U** = `personaje_v2/pruebas/test_motor_a_f1_usgaap.py` (grupo entre paréntesis); **PU** = `prueba_pipeline_usgaap.py`;
**L** = `probar_libro_v631_usgaap.py`; **M** = `mutaciones_usgaap.py`.

| Hallazgo de la revisión | Cambio | Prueba |
|---|---|---|
| **R1-1** · con el motor B, un libro US GAAP sin declaración F1 llegaba a `concluido` sin evaluar el puente: `Control maestro L4` se leía con un lector que, en los libros que recalcula LibreOffice, devuelve el índice del texto y no el texto | la norma del libro se lee resolviendo los textos compartidos (`_l4_del_libro`). Con el motor B, si la norma no se puede determinar en un expediente de la 4.15 (sin libro legible, `L4` vacío o fuera de la lista, como «U.S. GAAP»), F1 se exige: gancho, vigencia y cierre (falla en cerrado, como el motor A); `F1-NORMA` dice qué falta | U (R1, EX), **PU8** (de extremo a extremo, sin declaración: `pendiente_de_datos` en el paso 7), **PU9** (declaración NIIF con libro US GAAP) |
| **R1-3** · una ubicación falsa con cita real llegaba a `concluido` sin condición y con el valor sobrestimado, por tres caminos («fuera», «fila_8», «los dos en la fila 14») | regla 8: quien afirma una ubicación enseña la línea, y lo que el programa no puede contrastar con una línea no da una conclusión sin condición. Se contrasta con las líneas que la fase 1 sumó de verdad (`fase1_partes`, tomadas como las toma la fase 1 y con la etiqueta entera de las líneas partidas) y con las páginas citadas. Contradicha → DATOS INVÁLIDOS; sin contrastar → CONDICIONADA con su cota | U (F, R3: los casos B1–B7 y C de la revisión, la matriz verdad × declaración de 72 pares × 4 y el error a la baja), **PU5**, **PU6** |
| **R1-4** · decisión **D-US2 bis** | con los dos tramos dentro de la fila 14 no se retira nada ni se bloquea: se publica el valor de la hoja (coste contable) y, al lado, cuánto cambiaría contando los pagos; antes se comprueba que el expediente muestra las dos líneas (cierra el tercer camino de R1-3). Sustituye la lectura estricta de la ronda 1 | U (B), **PU7**, **L7** |
| **R1-5** · decisión **D-WM** | los arrendamientos financieros que la empresa no desglosa se tratan como deuda y activos propios (hipótesis declarada): no se piden su amortización ni su principal; la diferencia estimada se enseña junto al resultado. Zoetis no necesita cambio de producto (se registra `C49`) | U (W) |
| **R1-6** · el contraste de «no_publicada» con la página se anulaba con etiquetas normales y no veía rótulos habituales | un solo patrón, el amplio; solo se excluye la línea del **otro** tramo cuando está declarada con su ubicación, la información complementaria y las líneas solo de financieros. Con `fase1_partes`, la página tiene que ser la del estado de flujos | U (R6: N1–N4 de la revisión, H) |
| **R1-7** · lo que quedaba «a la vista» por D-US2 mezclaba perímetros | `coste_arr_operativo` es el coste de los contratos capitalizados; si la empresa no lo separa, se declara que no es comparable y la diferencia no se calcula (la cota que lo usa se rotula «holgada») | U (R7) |
| **R1-8** · la cota de D-US1 no aparecía en el informe | `condicionada.cota.resumen`: % del flujo sin crecimiento y % del valor presente en el escenario NORMAL; va en el rótulo, en la ficha y en la línea del informe | U (H), **PU1**, **PU6** |
| **R1-9** · con el motor B no se avisaba de lo que F1 no mira, y la línea del informe confundía | `F1-US-ANCLA` (AVISO): el ancla de S2C y el ROIC pueden arrastrar partidas del arrendamiento operativo; la línea del informe habla solo del puente. El puente se contrasta con las líneas de la fila 23 | U (P, R9), **PU10** |
| **R1-11** · la lista cerrada de `L4` se alimentaba de un campo de vocabulario abierto | la instrucción de metadatos de la fase 1 cierra el vocabulario y el paso 2 del pipeline lo comprueba antes de escribir el libro | U (R11), **PU11** |
| **R1-12** · la ficha de un expediente NIIF ganaba dos claves nulas | `condicionada` y `us_gaap` solo se escriben con US GAAP | `prueba_pipeline_f1.py` (P2) |
| **R1-13** · `F1-US-C49`: tolerancia y mensaje | tolerancia = media unidad del último decimal con que se registró `C49` (un cero no dice sus decimales); se admite la diferencia explicada en `conciliacion_fcf_base` (avisa); el mensaje no afirma que sean pagos operativos | U (R13: el caso E6 de la revisión) |
| **R1-14** · excepción sin controlar con una serie mal formada | la declaración se normaliza antes de evaluar: lo mal formado es DATOS INVÁLIDOS (`F1-DECLARACION`); también en el paso 2 (`f1_libro_v631`) | U (R14: 7 casos y 600 declaraciones al azar) |
| **R1-15** · K3b repite la declaración | K3b lleva su fundamento («contrastado», «según lo declarado», «según la hipótesis») y K3 solo se presenta como conforme si las ubicaciones se contrastaron con líneas | U (H, F), **PU1**, **PU6** |
| **R1-16** · con financieros cuya amortización no está en la D&A, declarar la verdad bloqueaba | `financieros.amortizacion_rou.ubicacion`: `fuera_de_la_fila_8`, con su evidencia y su cifra publicada | U (R16: el caso E4 de la revisión) |
| **R1-17** · matices de las citas | recogidos en el §2 | — |

**No tocados, por encargo:** R1-2 (el cero publicado «—» en `F1-SERIES`: lo resuelve la rama `f1/series-escala`; la validación de las series
no se ha reescrito) y R1-10 (la instrucción de la fase 1 `historia_anio.md` no está adaptada a US GAAP: solo información).

## 1. Qué había y qué cambia

**Hecho.** Con US GAAP la capa `personaje_v2/scripts/motor_a_f1.py` bloqueaba siempre (`F1-NORMA`, límite declarado): toda empresa
estadounidense con el motor A terminaba en «límite del modelo». La norma del libro se leía buscando «ifrs|niif|ias» dentro del texto de
`Control maestro L4` (H13 de la revisión de F1-IMPL: «US GAAP (no IFRS)» pasaba como NIIF).

**Cambio.** La norma es un valor cerrado y la capa implanta ASC 842 con los arrendamientos **operativos** y **financieros** por separado.
Se aplican las decisiones F1 ya registradas ((1a) b: la reinversión que calibra f excluye la amortización de los derechos de uso; K3: el
alquiler se cuenta una vez) y las cuatro de la persona responsable del 18-nov-2026 para US GAAP (`DECISIONES_PARA_EL_USUARIO.md`:96–98 y
112–114):

- **D-US1 · hipótesis general declarada.** Si la empresa no publica en qué líneas del estado de flujos van los dos tramos del arrendamiento
  operativo (la amortización del derecho de uso y la variación del pasivo), se supone que van netos dentro del flujo de explotación, fuera
  de las filas 8 y 14 de la Historia. Es una hipótesis, no un dato: la conclusión se presenta como **condicionada**, con su cota. Donde la
  empresa publica las líneas, manda el dato.
- **D-US2.** Cuando el coste lineal y los pagos del año difieren, se cuentan los **pagos** y la diferencia queda a la vista, sin bloquear.
- **D-US2 bis** (caso Nike). Con el alquiler mezclado en las líneas de otros activos y otros pasivos (los dos tramos dentro de la fila 14)
  no se bloquea: se publica el valor de la hoja, que cuenta el **coste contable**, y al lado cuánto cambiaría contando los pagos. Antes, el
  programa comprueba que el expediente muestra las dos líneas (la del activo y la del pasivo).
- **D-WM** (caso Waste Management). Los arrendamientos financieros que la empresa no desglosa se tratan como **deuda y activos propios**
  (hipótesis declarada): su amortización queda dentro de la propia y sus pagos no se restan de la caja base; la diferencia estimada (caja
  pagada − gasto total) se enseña junto al resultado.

No se adopta nada más. Las elecciones del autor que no vienen de una decisión están marcadas como *interpretación* en el §9.

## 2. La norma, en lo que importa al modelo

Las citas de ASC 842 y ASC 230 están escritas de memoria (sesión sin internet). El revisor las contrastó con fuentes secundarias (Deloitte,
BDO, KPMG, CLA, *Journal of Accountancy*) y las halló coherentes; el texto literal de la Codificación sigue sin contrastar.

| | Arrendamiento **operativo** | Arrendamiento **financiero** | NIIF 16 (referencia) |
|---|---|---|---|
| Cuenta de resultados | un solo coste lineal (842-20-25-6); 842-20-45-4 dice «income from continuing operations»: en la práctica, gasto de explotación, y el EBIT lleva el alquiler **entero** | amortización del derecho de uso (con la D&A o aparte) e interés (gasto financiero) | amortización + interés |
| Estado de flujos | los pagos, **dentro del flujo de explotación (CFO)** (842-20-45-5 c; salvo los que son coste de poner otro activo en uso, que van a inversión) | principal en **financiación**; interés en explotación (842-20-45-5 a y b; ASC 230-10-45-17) | principal en financiación |
| Balance | derecho de uso y pasivo, separados de los financieros (842-20-45-1 a 3) | derecho de uso y pasivo propios (a veces dentro del inmovilizado y de la deuda) | derecho de uso y pasivo |
| Notas (842-20-50-4) | coste del arrendamiento operativo; **caja pagada dentro del flujo de explotación** | amortización e interés por separado (no todas las empresas lo cumplen: WM los da sumados); **caja pagada en financiación** | — |
| Lo que la norma no fija | en qué línea de la conciliación del CFO van la amortización no monetaria del derecho de uso y la variación del pasivo: en líneas distintas, en la misma, o dentro de otras | — | — |

Motor A: `flujo = V·[m(1−τ) − f] − ΔV/S2C`, con `f = (NOPAT − (capex − D_X + circulante) − FCF base) ÷ ventas`. En régimen estable el flujo
sin crecimiento es `FCF base + capex − D_X + circulante`. El alquiler operativo ya está **una vez** en el FCF base (el pago va en el CFO).
Se contaría **dos veces** si su amortización no monetaria quedara dentro de D_X (fila 8), si quedara sola dentro del circulante (fila 14)
o si sus pagos se restaran otra vez en C49. Se **omitiría** (casi entero) si la variación de su pasivo quedara sola dentro del circulante.
Con los dos tramos netos dentro del circulante, la fila 14 lleva `pagos − coste` y la hoja cuenta el **coste**, no los pagos.

## 3. Reglas

1. **Norma, valor cerrado.** `norma_contable.valor` es `NIIF` o `US_GAAP`. `Control maestro L4` se lee con una lista cerrada de valores
   exactos, sin distinguir mayúsculas ni espacios de más: `IFRS`, `NIIF`, `IFRS (IFRS-EU)`, `IFRS (adoptadas por la Unión Europea)` → NIIF;
   `US GAAP` → US GAAP. Cualquier otro texto bloquea. La declaración y el libro tienen que decir lo mismo. La norma se cierra en su origen:
   la instrucción de metadatos de la fase 1 pide exactamente «IFRS» o «US GAAP», y el paso 2 del pipeline detiene el expediente
   (`pendiente_de_datos`) si `fase1_v63.json` trae otra cosa («Otro», el tercer valor de la lista de la plantilla, pasa; la capa no lo
   soporta y lo dirá en el paso 7).
2. **Financieros.** Por omisión, como NIIF 16: `da_rou` es la amortización de su derecho de uso dentro de la fila 8 y C49 su principal;
   valen V-F1a, V-F1b, V-F1m, `F1-M-SIM`, A1/A2. Dos declaraciones lo cambian, con su evidencia:
   - `financieros.amortizacion_rou.ubicacion`: `fuera_de_la_fila_8` → D_X no la lleva; `da_rou` no se declara y `da_rou_financiero_fuera`
     es su cifra publicada (para la cota). `F1-ROU-HISTORIA` y V-F1m no bloquean.
   - `financieros.desglose`: `no_publicado` → **D-WM**: no se piden `da_rou` ni el principal; nada se excluye de D_X, C49 tiene que ser 0
     y se declaran la caja pagada y el gasto total publicados. La conclusión es condicionada.
3. **Operativos.**

   | Dónde está el tramo | Qué hace la capa |
   |---|---|
   | amortización del derecho de uso **dentro de la fila 8** | la excluye de D_X con A1/A2 (se declara su importe); con A0 bloquea (`F1-US-DA`) |
   | **un solo tramo** dentro de la fila 14 | D-US2: retira su importe del circulante que usa la reinversión, en f y en el ancla de S2C; ningún libro lo retira (`F1-LIBRO`, §7) |
   | **los dos tramos** dentro de la fila 14 | D-US2 bis: no retira nada; publica el valor de la hoja (coste contable) y cuánto cambiaría contando los pagos. Exige las dos líneas contrastadas |
   | **fuera de las filas 8 y 14** | nada (D-US2: se cuentan los pagos) |
   | **no publicada** | hipótesis D-US1: como si estuviera fuera; conclusión **condicionada**, con cota |
   | sin declarar | bloquea · `pendiente_de_datos` (`F1-US-DESGLOSE`) |

4. **Perímetros.** `D_X(A1) = D&A − ROU dentro de la fila 8` y `D_X(A2) = … − PPA`; «ROU dentro de la fila 8» es la de los financieros (si
   está dentro) más la de los operativos que estén dentro de la fila 8. A0 no cambia.
5. **C49 solo lleva principal de arrendamientos financieros** (`F1-US-C49`). Se compara con la media del principal publicado, con la
   tolerancia del redondeo con que se registró C49 (media unidad de su último decimal; mínimo 0,005; un cero se toma exacto). Una diferencia
   mayor bloquea, salvo que esté explicada por una partida declarada con su fuente en `conciliacion_fcf_base` (componente `C49`, la misma
   que usa K3a): entonces avisa. Con D-WM, C49 tiene que ser 0. Con US GAAP no hay intereses pagados «en financiación» (`F1-US-MEZCLA`).
6. **Puente de deuda (motor B).** El pasivo por arrendamiento **operativo** no es deuda del puente: su pago ya está entero en el EBIT que
   proyecta el motor B. Deuda coherente = deuda financiera (fila 22) + pasivo por arrendamientos financieros. El libro resta
   `Historia C64 = fila 22 + fila 23`: si la fila 23 lleva pasivo operativo, `F1-US-PUENTE` **bloquea** con el motor B e informa con el A.
   Lo declarado se contrasta con las líneas que la fase 1 sumó en la fila 23. Con el motor B, F1 se exige solo para esto: si la declaración
   o el libro dicen US GAAP, **y también si la norma no se puede determinar en un expediente de la 4.15** (falla en cerrado). Lo que F1 no
   mira con el motor B se avisa (`F1-US-ANCLA`).
7. **K3.** K3a (caja base por dos vías) no depende de la norma. K3b cuenta el alquiler por clase (operativos: 1 por el EBIT y el CFO, + 1 si
   C49 lleva sus pagos, + 1 si su amortización queda en D_X o sola en el circulante, − 1 si la variación de su pasivo queda sola en el
   circulante; financieros: como NIIF, o «como deuda (D-WM)»). **K3b repite la clasificación declarada: no es una comprobación
   independiente.** Lleva su fundamento y K3 solo se presenta como conforme cuando las ubicaciones se contrastaron con líneas.
8. **Quien afirma una ubicación enseña la línea** (`F1-US-FILAS`). Cada ubicación declarada se contrasta con la página citada y con las
   líneas que la fase 1 sumó en la fila 8 (`da`) y en la fila 14 (`circulante_lineas`) en los años que usa el modelo (la ventana de f y los
   cinco del ancla), tomadas como las toma la fase 1: el lado «anterior» del informe siguiente y, si no lo hay, el «actual». De cada línea
   se reconstruye la etiqueta entera con su página de `texto/` (una etiqueta partida en dos renglones lleva el arrendamiento en el primero).

   | Declarado | Contrastada (sin condición) | Sin contrastar (CONDICIONADA, con cota) | Bloquea |
   |---|---|---|---|
   | `fila_8`, `fila_14` | la cita nombra el arrendamiento y su tramo, y una línea sumada en esa fila lo nombra en cada año del modelo | la cita es de una nota y ninguna línea sumada lo nombra; faltan años | la cita no nombra el arrendamiento o nombra el otro tramo (INCOMPLETO); la línea citada es del estado de flujos y la fase 1 no la sumó ahí (DATOS INVÁLIDOS) |
   | `fuera_de_las_filas_8_y_14` | la cita es una línea del estado de flujos de un informe del modelo, la fase 1 no la sumó, y las líneas sumadas de todos los años se examinaron enteras | sin `fase1_partes` o sin `texto/`; faltan años | la línea citada está entre las sumadas (DATOS INVÁLIDOS); la página no es la del estado de flujos, o la cita solo está en información complementaria (INCOMPLETO: si no hay línea, es `no_publicada`) |
   | `no_publicada` | — | siempre (hipótesis D-US1) | la página muestra una línea de ese tramo (DATOS INVÁLIDOS: manda el dato); la página no es la del estado de flujos (INCOMPLETO) |
   | cualquiera | — | — | una línea sumada en la fila 8 o en la 14 nombra un tramo declarado en otro sitio (DATOS INVÁLIDOS) |
   | los dos `fila_14` (D-US2 bis) | las dos líneas, la del activo y la del pasivo (o una que nombre los dos) | — | no se pueden comprobar las dos líneas (INCOMPLETO): no se publica el valor de la hoja |

   El tramo se reconoce por los términos pegados a «lease» o a «right-of-use» («lease liabilities» → pasivo; «right-of-use assets», «lease
   expense», «non-cash lease» → activo o gasto); una línea que nombra el arrendamiento sin precisar («Operating leases, net») vale para los dos.

## 4. Qué se declara (en `motor_a_f1.json`, además de lo de NIIF)

```json
"norma_contable": {"valor": "US_GAAP", "registro": {"fecha": "…", "persona": "…", "motivo": "…"}},
"arrendamientos_us_gaap": {
  "registro": {"fecha": "…", "persona": "…", "motivo": "…"},
  "operativos":  {"existen": true, "documento": "…", "pagina": 0, "cita": "…",
                  "amortizacion_rou": {"ubicacion": "no_publicada", "documento": "…", "pagina": 0},
                  "variacion_pasivo": {"ubicacion": "fila_14", "documento": "…", "pagina": 0, "cita": "…"},
                  "coste_comparable_con_los_pagos": false, "coste_no_comparable_motivo": "…"},
  "financieros": {"existen": true, "documento": "…", "pagina": 0, "cita": "…",
                  "desglose": "publicado",
                  "amortizacion_rou": {"ubicacion": "fuera_de_la_fila_8", "documento": "…", "pagina": 0, "cita": "…"}}
}
```

- `ubicacion` de los operativos: `fila_8` (solo la amortización), `fila_14`, `fuera_de_las_filas_8_y_14` o `no_publicada`. La cita (literal,
  ≥ 10 caracteres) es **la línea que lo muestra**, en una página de una fuente del expediente con su huella (`fuentes_series`); conviene
  registrar como fuente el mismo texto que usó la fase 1 (`texto/…`). `no_publicada` lleva el documento y la página del estado de flujos.
- `coste_comparable_con_los_pagos` (opcional; por omisión, sí): `false`, con su motivo, si el coste publicado lleva corto plazo o variable
  y la empresa no lo separa.
- `desglose` (opcional; por omisión `publicado`) y `amortizacion_rou` de los financieros (opcional; por omisión dentro de la fila 8): regla 2.
  `desglose: "no_publicado"` (D-WM) y `amortizacion_rou` no se declaran a la vez: da DATOS INVÁLIDOS (`F1-US-DESGLOSE`; comprobado a mano
  el 18-nov-2026, sin caso propio en la batería).

Series (formato de `da_rou`: `valor_fuente` con su signo, `signo`, `tratamiento`, `documento`, `pagina`, `literal`, `fila`):

| Serie | Qué es | Cuándo se exige |
|---|---|---|
| `pagos_arr_operativo` | caja pagada por arrendamientos operativos dentro del flujo de explotación (nota de arrendamientos) | operativos: ventana de f |
| `coste_arr_operativo` | «operating lease cost» de los contratos capitalizados (sin corto plazo ni variable), el mismo perímetro que los pagos | operativos: ventana |
| `da_rou_operativo` | amortización del derecho de uso operativo **dentro de la fila 8** | ubicación `fila_8`: ventana (y H–L para el ancla) |
| `circulante_arr_operativo` | importe del arrendamiento operativo **dentro de la fila 14**, con el signo de esa fila (+ consume caja) | un tramo en la fila 14: ventana y H–L. Los dos: opcional (la línea neta publicada; si falta, pagos − coste) |
| `pasivo_arr_operativo` | pasivo por arrendamiento operativo **dentro de la fila 23**, último ejercicio | motor B: obligatorio; motor A: si falta, avisa |
| `da_rou` | amortización del derecho de uso de los **financieros** dentro de la fila 8 | financieros con desglose publicado y dentro de la fila 8: ventana (y H–L) |
| `pagos_arr_financiero_principal` | principal pagado de los financieros (financiación) | financieros con desglose publicado: ventana |
| `da_rou_financiero_fuera` | amortización publicada del derecho de uso financiero que **no** está dentro de la fila 8 | `fuera_de_la_fila_8`: ventana |
| `caja_pagada_arr_financiero`, `gasto_arr_financiero` | caja pagada y gasto total (amortización + interés) de los financieros, tal como se publican | D-WM: ventana |

Sin arrendamientos de una clase (`existen: false`, con su evidencia) no se declaran sus series. Los identificadores de los perímetros
no cambian: con US GAAP, `EBIT_NIIF16_PPA_constante` designa el EBIT publicado.

## 5. Qué bloquea, qué avisa y qué condiciona

| Id | Salta cuando | Efecto |
|---|---|---|
| `F1-NORMA` | norma sin declarar o fuera de la lista; `L4` vacío o no reconocido; declaración ≠ libro | BLOQUEA |
| `F1-DECLARACION` | claves no reconocidas, o una clave que tiene que ser un objeto y no lo es | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-MEZCLA` | declaración NIIF con claves o series de US GAAP; US GAAP con intereses pagados en financiación | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DESGLOSE` | falta `arrendamientos_us_gaap`, su registro, la existencia de una clase, una ubicación, su evidencia o una serie exigida; declaraciones incoherentes entre sí | BLOQUEA · INCOMPLETO o DATOS INVÁLIDOS |
| `F1-US-C49` | C49 distinto del principal financiero publicado más allá de su redondeo y sin explicar; C49 > 0 sin financieros o con D-WM | BLOQUEA · DATOS INVÁLIDOS (explicado: AVISO) |
| `F1-US-DA` | amortización del derecho de uso operativo dentro de la D&A con A0, o sola dentro del circulante sin su importe: dos veces | BLOQUEA · MODELO NO APLICABLE |
| `F1-US-SIM` | la simétrica: variación del pasivo sola dentro del circulante sin su importe, o amortización excluida de D_X sin pagos en el CFO | BLOQUEA · FUERA DEL DOMINIO |
| `F1-US-FILAS` | regla 8: contradicha o sin la línea que la prueba | BLOQUEA · DATOS INVÁLIDOS o INCOMPLETO; sin contrastar: AVISO |
| `F1-US-PUENTE` | la fila 23 lleva pasivo por arrendamiento operativo, o lo declarado contradice sus líneas | BLOQUEA con el motor B · INFORMA o AVISA con el A |
| `F1-K3b` | alguna clase no se cuenta exactamente una vez | BLOQUEA |
| `F1-LIBRO` | además: hay que retirar del circulante el importe de **un** tramo, que ningún libro retira (§7) | BLOQUEA · límite declarado |
| `F1-SERIES` | además: series de US GAAP, citas de las clasificaciones y página de un «no_publicada» | BLOQUEA si nada más bloquea |
| `F1-US-HIPOTESIS` | la conclusión es **condicionada**: hipótesis D-US1, ubicación sin contrastar o hipótesis D-WM; con su cota | AVISO |
| `F1-US-BASE` | D-US2: se cuentan los pagos; coste − pagos (INFORMA). D-US2 bis: valor de la hoja y cuánto cambiaría contando los pagos (AVISO) | no bloquea |
| `F1-US-ANCLA` | motor B con arrendamientos operativos: F1 no mira el ancla de S2C ni el ROIC | AVISO |

**La cota** (`condicionada.cota`; mm, % del flujo sin crecimiento y, con palancas, % del valor presente de los flujos por escenario):

| Condición | Si no fuera cierta, el flujo sin crecimiento cambiaría en |
|---|---|
| variación del pasivo no publicada, o declarada fuera sin contrastar | como máximo, − los pagos (estaría sola en la fila 14) |
| amortización no publicada, o declarada fuera sin contrastar | como máximo, + el coste lineal (estaría en la fila 8 o sola en la 14) |
| amortización declarada en la fila 8 sin contrastar | − el importe declarado (exacto) |
| un tramo declarado en la fila 14 sin contrastar | + el importe retirado (con su signo) |
| amortización financiera declarada fuera de la fila 8 sin contrastar | + el importe publicado |
| D-WM | − (caja pagada − gasto total): **estimación**, no cota |

El resumen (`cota.resumen`) suma las variaciones del mismo signo (dos ubicaciones falsas a la vez se acumulan) y no compensa las de signo
contrario. Con declaraciones veraces, la cota cubre el error en todos los casos de la matriz de la revisión.

## 6. Norma → tratamiento → prueba

Empresa de referencia: ventas 1.000; EBIT 68 tras un alquiler operativo de 12; CFO 88; capex = D&A propia = 20; FCF base 68.

| Norma y caso | Tratamiento | Prueba | Resultado |
|---|---|---|---|
| NIIF 16 | sin cambio: A1/A2 excluyen `da_rou`; C49 lleva el principal | batería F1 existente (163), regresión de Elis (39), U «NIIF» | iguales (§8) |
| US GAAP · solo operativos, tramos fuera con su línea | nada: A0 y A2 dan la caja (68); una vez | U1 | utilizable, sin condición |
| US GAAP · operativos + financieros | financieros como NIIF 16: A2 da 62 = FCF base; A0, 57 y V-F1a | U2, L3 | utilizable con A2 (libro V6.3.1) |
| US GAAP · D&A con derecho de uso operativo dentro | A0 bloquea (`F1-US-DA`; daría 58); A2 lo excluye (68) | U3, L1, L2 | utilizable con A2 |
| US GAAP · C49 con pagos operativos | `F1-US-C49`; K3b «operativos: dos veces» (FCF base 56) | U4, PU4 | `pendiente_de_datos` |
| US GAAP · desglose ausente | `F1-US-DESGLOSE` | U5, PU3 | `pendiente_de_datos` |
| US GAAP · un tramo solo en la fila 14 | la capa lo retira (68; tal cual, 78); sin importe, `F1-US-SIM` o `F1-US-DA` | U6, L5, PU2 | la capa calcula; el libro no → `F1-LIBRO` |
| US GAAP · los dos tramos en la fila 14 (Nike) | D-US2 bis: valor de la hoja (coste) y cuánto cambiaría contando los pagos | B, L7, PU7 | utilizable (libro V6.3.1 tal cual) |
| US GAAP · tramos no publicados (Zoetis, WM) | D-US1: fuera de las filas; condicionada, con cota | H, L4, PU1 | utilizable y condicionada |
| US GAAP · ubicación sin contrastar | condicionada, con cota | F, R3, PU6 | utilizable y condicionada |
| US GAAP · ubicación contradicha | `F1-US-FILAS` | F, R3, PU5 | `pendiente_de_datos` |
| US GAAP · coste lineal ≠ pagos | D-US2: se cuentan los pagos; diferencia a la vista | D, PU1, R7 | no bloquea |
| US GAAP · financieros no desglosados (WM) | D-WM: como deuda; diferencia estimada a la vista | W | utilizable y condicionada |
| US GAAP · amortización financiera fuera de la D&A (Zoetis) | `fuera_de_la_fila_8` | R16 | utilizable (condicionada si no se contrasta) |
| Mezcla de normas | `F1-NORMA`, `F1-US-MEZCLA` | N, PU9 | `pendiente_de_datos` |
| Motor B con US GAAP | puente sin el pasivo operativo; `F1-US-PUENTE`; `F1-US-ANCLA` | P, R9, L6, EX, PU8, PU10 | bloquea si la fila 23 lo lleva |
| Motor B, norma sin determinar (4.15) | F1 se exige; `F1-NORMA` | R1, EX, PU8 | `pendiente_de_datos` |

## 7. Qué calcula el libro V6.3.1 tal cual y qué no

**Hecho** (L1, L3, L4, L7, PU1, PU6, PU7): el libro V6.3.1 F1 sin tocar calcula, con la capa como oráculo (f a 10⁻¹², ancla a 10⁻⁹, 33 flujos):
- tramos **no publicados** (D-US1) o **fuera de las filas**: el caso de Zoetis y de Waste Management;
- amortización operativa **dentro de la fila 8**, con o sin financieros: la fila 86 lleva la suma y A2 la excluye;
- **los dos tramos dentro de la fila 14** (D-US2 bis): el caso de Nike;
- financieros tratados como deuda (D-WM) o con su amortización fuera de la fila 8: la fila 86 no los lleva.

**Límite declarado** (`F1-LIBRO`; U6, L5, PU2): ningún libro retira nada del circulante. No se puede concluir cuando **un solo tramo** está
dentro de la fila 14: la variación del pasivo como línea propia del circulante con la amortización en otra línea (frecuente), o la
amortización sola. Salida: una corrección registrada de las entradas en un expediente nuevo (la fila 14 sin esa línea), o que la fase 1 no
sume en las filas 8 y 14 las líneas propias del arrendamiento operativo (R1-10 de la revisión: es especificación de la fase 1 y está
fuera de esta rama; la decide la persona). ***Propuesta*** que sigue en pie: una plantilla hermana de la V6.3.1 con una fila para el ajuste
del circulante y otra para el pasivo operativo del puente. No se ha construido: la V6.3.1 no se puede cambiar porque
`plantilla_activa.json` de los expedientes en curso fija sus huellas.

**Puente (motor B):** ningún libro excluye el pasivo operativo de `Historia C64`. Salida: que la fila 23 lleve solo el pasivo por
arrendamientos financieros (corrección registrada). El coste de la deuda (C63), los pesos de la r operativa, el capital invertido y el ROIC
histórico (filas 32–33, C54–C55) también usan la fila 23: no se ajustan.

## 8. Pruebas ejecutadas (hechos; resultados literales)

LibreOffice siempre con `flock /home/user/e_work/libreoffice.lock`, una ejecución detrás de otra. Salidas de la ronda 2 en `resultados/`
(las de la ronda 1 se conservan con el sufijo de su commit o se sustituyen por las nuevas del mismo guion).

| Orden | Resultado literal |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1_usgaap.py` (sin LibreOffice; ronda 1: 121) | `246/246 pruebas del motor A F1 con US GAAP PASAN` |
| `python3 -I …/f1_usgaap/scripts/mutaciones_usgaap.py` (84 líneas de la capa cambiadas a propósito: las 38 de la ronda 1, puestas al día, y 46 de la ronda 2) | `84 de 84 mutaciones detectadas` (`resultados/mutaciones_usgaap.txt`) |
| `flock … python3 -B …/f1_usgaap/scripts/prueba_pipeline_usgaap.py` (pipeline con la V6.3.1; ronda 1: 11) | `22/22 pruebas de F1 · US GAAP en el pipeline PASAN` |
| `flock … python3 -I …/f1_usgaap/scripts/probar_libro_v631_usgaap.py <carpeta nueva>` (libro V6.3.1 real; ronda 1: 13) | `15/15 comprobaciones de F1 · US GAAP sobre el libro V6.3.1 PASAN` |
| **NIIF no cambia:** `python3 -B pruebas/test_motor_a_f1.py` | `163/163 pruebas del motor A F1 (4.15) PASAN` (sin tocar en la ronda 2) |
| `python3 -B pruebas/test_v631_f1.py` | `29/29 pruebas V6.3.1 F1 (sin LibreOffice) PASAN` (28 + la desdoblada por R1-1) |
| `python3 -I v6/v631_f1/scripts/probar_v631_f1.py estructura` | `21/21 comprobaciones V6.3.1 F1 (estructura) PASAN` (plantilla `eaece01a…`) |
| `flock … prueba_pipeline_f1.py` (gancho; un caso más: la ficha y el informe NIIF no llevan nada de US GAAP) | `8/8 pruebas del gancho F1 del pipeline PASAN` |
| estado F1 (`vigencia()`) de los expedientes con pipeline, con el código de la ronda 1 y con el de la ronda 2 | 38 del árbol y 10 del examen (solo lectura): **0 distintos** |
| diferencial NIIF de la revisión (400 casos al azar, el libro real de Elis con sus declaraciones y 21 variantes de `L4`), ronda 1 frente a ronda 2 | `idénticos (todo el resultado salvo versión y fecha): 425 · distintos: 0` (`resultados/diferencial_niif_ronda1_ronda2.txt`) |
| `python3 -I …/f1_impl/scripts/regresion_elis_f1.py <copia>` | `39/39 PASAN` (`resultados/regresion_elis_f1_tras_usgaap.md`) |
| los guiones de la revisión, **sin cambios**, contra la capa de la ronda 2 (`adversarial_capa.py`, `matriz_verdad_declaracion.py`, `error_a_la_baja.py`, `fuzz_us.py 3000`) | B1–B6 y C1 bloquean; B7 condicionada con cota; E6 no salta; N1–N3 bloquean; N4: los 14 rótulos se ven; G3 bloquea; matriz: `sin condición ni cota: 0` en las dos pasadas; 3.000 declaraciones al azar sin excepciones (`resultados/guiones_de_la_revision_R1_contra_la_ronda_2.txt`, con su montaje y dos matices) |
| `flock … bash verificar_paquete.sh completa` sobre una copia limpia de `a6fc300`, el commit del código de la ronda 2 (manifiesto 8063 · modificados 0 · ausentes 0 · de más 0; 83 minutos) | `RESULTADO GLOBAL: PASA`, código 0 (`resultados/verificacion_completa_a6fc300.txt`): los 27 bloques en PASA; comprobadores 114/114, sintética 30/30, vigencia H5 59/59, juicio 27/27, entradas 33/33 y 190/190, entrada efectiva 62/62, relevo 5/5, motor A F1 163/163, gancho 8/8, **US GAAP 246/246, 22/22 y 15/15**, V6.3.1 29/29, 21/21, 22/22, 35/35 y 9/9, V6.4 199/199, trazabilidad 78/78, integridad 103/103, auditorías 55/55, estados 28/28, resumen 45/45, cierre 55/55. Después de `a6fc300` no cambia nada de lo que ejecuta `completa`, salvo el manifiesto: solo este documento, el registro, el guion de mutaciones (limpieza de sus carpetas temporales; no forma parte de `completa`), `CAMBIOS_ARCHIVOS.txt` y el manifiesto. Sobre una copia limpia del último commit: manifiesto sin diferencias (modo rápido, PASA) y las baterías sin LibreOffice 246/246, 163/163 y 29/29 |

**NIIF no cambia de valor.** Cambios de comportamiento con NIIF, todos sobre casos antes mal tratados: (a) un libro NIIF cuyo `L4` no es
de la lista cerrada bloquea con `F1-NORMA` (ronda 1, H13) y ahora se detiene antes, en el paso 2; (b) con el motor B, un expediente de la
4.15 cuyo libro no dice una norma de la lista (o sin libro legible) exige F1 y bloquea con `F1-NORMA` (R1-1); (c) una declaración mal
formada da DATOS INVÁLIDOS en lugar de un fallo del programa (R1-14). El estado F1 de los 38 expedientes del árbol con pipeline y de los
10 del examen es el mismo con el código de la ronda 1 y con el de la ronda 2 (`vigencia()` ejecutada con los dos). La ficha de un
expediente NIIF vuelve a no llevar ninguna clave de US GAAP (R1-12).

Las pruebas de US GAAP están registradas en `verificar_paquete.sh completa` (mínimos 246, 22 y 15; el gancho, 8; la V6.3.1 sin LibreOffice, 29). Una prueba de la V6.3.1
(`test_v631_f1.py`, «V631-1: con el motor B F1 no se exige») afirmaba lo contrario de R1-1 para un expediente de la 4.15 sin libro
evaluado: se ha desdoblado (sin libro, se exige; con un libro NIIF, no).

**Limpieza de las pruebas** (hecho, después de la verificación completa). Una batería que se interrumpe no borra sus carpetas temporales
`f1_us_*`, y el guion de mutaciones interrumpe muchas: en esta sesión se habían acumulado 23.059 carpetas (unos 360 MB) en el directorio
temporal del sistema, ya borradas. Ahora cada batería mutada crea sus carpetas dentro de su copia (`TMPDIR`) y se borran con ella; la
campaña repetida con ese cambio da la misma salida, byte a byte (`84 de 84 mutaciones detectadas`), y no deja nada. Queda un defecto menor
sin corregir, para no cambiar después de verificarlo ningún archivo de los que ejecuta `completa`: una ejecución normal de la batería deja
41 carpetas **vacías** (el bucle de declaraciones al azar, cuando la declaración mutada no deja escribir la fuente). No afecta a ningún
resultado; se corrige con el próximo cambio de código.

## 9. Interpretaciones del autor y límites para el revisor

*Interpretaciones* (no vienen literalmente de una decisión):
1. **D-US2 bis se aplica siempre que los dos tramos están dentro de la fila 14**, vayan en líneas mezcladas (Nike) o en dos líneas propias.
   Con una línea neta publicada declarada, «cuánto cambiaría» usa esa línea; si no, `pagos − coste`. Con un **solo** tramo dentro sigue la
   regla de la ronda 1 (se retira; `F1-LIBRO`).
2. Con D-US2 bis, si no se pueden comprobar las dos líneas (también sin `fase1_partes`) **se bloquea** (INCOMPLETO) en lugar de condicionar:
   la decisión pone la comprobación como condición previa.
3. **D-WM se declara por expediente como un hecho** (`desglose: no_publicado`, con su evidencia); la regla es general. Exige C49 = 0 y la
   caja pagada y el gasto total de la ventana. La diferencia estimada supone que las dos cifras llevan el mismo interés; si la caja pagada
   fuera solo el principal, sería mayor en el interés (lo dice el resultado).
4. Una ubicación declarada que no se puede contrastar **se usa en el cálculo** y condiciona la conclusión, con la cota del caso contrario.
   La alternativa (tratarla como no publicada) cambiaría el valor en contra de lo declarado con una cifra publicada.
5. Con la norma sin determinar y el motor B, F1 se exige **solo en expedientes de la 4.15** (los que declaran F1 o llevan
   `entrada_efectiva`); los históricos no cambian. «Otro» en `L4` cuenta como norma sin determinar: F1 no tiene regla para otras
   normas y, con los motores A y B, un expediente de la 4.15 con «Otro» no concluye (`F1-NORMA`).
6. Tolerancia de `F1-US-C49`: la del redondeo con que está escrito C49; un cero se toma exacto.
7. A0 con amortización operativa dentro de la fila 8 bloquea siempre; `F1-US-MEZCLA` con C48 o fila 16 positivos; `coste_arr_operativo`
   es obligatorio aunque no sea comparable (hace de cota holgada); con el motor A la falta de `pasivo_arr_operativo` solo avisa.
8. La amortización del derecho de uso **financiero** dentro de la fila 8 (el caso por omisión, como NIIF 16) no se condiciona aunque no se
   contraste con una línea; solo se contrasta la declaración contraria (`fuera_de_la_fila_8`).

Límites:
1. **El cero publicado sigue sin poder declararse** (R1-2): un principal «—», o un importe «dentro de la fila» igual a cero, da
   `F1-SERIES` DATOS INVÁLIDOS. Zoetis (principal de 2023 «—») no concluye hasta que se integre `f1/series-escala`.
2. El contraste de la regla 8 es **por el texto de las etiquetas**, con patrones en inglés y en español. No ve un arrendamiento dentro de
   una línea que no lo nombra en ningún renglón: por eso lo que no se puede contrastar queda condicionado, no acreditado. Una cabecera sin
   cifras y sin dos puntos justo encima de una línea se toma como primer renglón de su etiqueta; si nombrara el arrendamiento, la línea
   se trataría como suya (bloquearía; no cambia ningún valor).
3. **Falsos positivos del patrón amplio** (R1-6 pidió usarlo; es el lado seguro, pero no tiene salida en la declaración). Una línea de la
   conciliación que nombra un arrendamiento sin ser uno de los dos tramos (el deterioro de un derecho de uso, el resultado por cancelar un
   arrendamiento, incentivos) hace saltar «manda el dato» frente a un `no_publicada` veraz, y una línea así sumada en la fila 8 o en la 14
   contradice una declaración veraz: el expediente queda en `pendiente_de_datos`. No debería afectar a Zoetis ni a Waste Management: según
   el §4 de la revisión R1, sus estados de flujos no nombran el arrendamiento (es una previsión; su fase 1 no se ha ejecutado).
   ***Propuesta***, sin implantar porque abre una vía que hay que revisar: permitir declarar, con
   su cita y su motivo, las líneas de la página que nombran un arrendamiento y **no** son el tramo, dejando la conclusión condicionada y
   esas líneas a la vista.
4. «Fuera» queda contrastada con la página de **un** informe; en los demás años del modelo se comprueba que ninguna línea sumada nombra el
   tramo, no que la línea citada exista también en esos estados de flujos.
5. Las series y clasificaciones de US GAAP no están en el libro: quedan fuera del universo de `verificacion_entradas.py`. `F1-SERIES`
   es una condición mínima (cifra con su signo y cita en su página; sin revisor ni sello). El resultado guarda la huella de las líneas de
   la fase 1 examinadas (`fase1_partes_sha256`), pero `vigencia()` no la comprueba.
6. No se tratan: ventas con arrendamiento posterior, incentivos, deterioros del derecho de uso, ni ventanas con ejercicios anteriores a
   ASC 842 (antes de 2019).
7. Con la plantilla V6.4.1 (motor B, perímetro «NIIF 16»), las altas de derechos de uso operativos no deberían entrar con US GAAP: no hay
   guarda.
8. Con el motor B, F1 solo mira el puente. El ancla de S2C y el ROIC histórico pueden llevar partidas del arrendamiento operativo: se avisa,
   no se corrige. El motor B cuenta el alquiler por su coste lineal (va en el EBIT; no tiene f): D-US2 no se le aplica.
9. K3c (reinversión media negativa con ventas que no bajan) puede saltar con D-US2 bis cuando el neto dentro de la fila 14 es negativo
   (pagos < coste) y la inversión neta propia es casi nula: es la regla general, con su salida (justificación declarada).
10. Todo el recálculo es LibreOffice; Excel real, sin probar. No se ha ejecutado la fase 1 ni el pipeline con Zoetis, Waste Management o
   Nike reales.
