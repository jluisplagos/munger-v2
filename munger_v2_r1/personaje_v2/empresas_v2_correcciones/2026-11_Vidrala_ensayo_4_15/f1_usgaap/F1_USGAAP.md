# F1 · US GAAP (ASC 842) · motor A con arrendamientos operativos y financieros

Fecha: 18-nov-2026. Lo escribe el agente autor de la reparación (Claude, modelo Fable 5.2) en la rama `f1/usgaap`, creada desde
`examen/ahold-f1` @ `1694f08`. **Ronda 2 y su cierre.** La ronda 1 (`34b68fc`) la revisó otro agente: veredicto CORRECCIONES acotadas
(`munger-v2-evidencias-mistral`, `coordinacion/cierre_v2/examen/revisiones/f1_usgaap/REVISION_R1.md`). La ronda 2 (`bcb6dc3`) la revisó
también otro agente (`REVISION_R2.md`, con sus guiones en `evidencia_r2/`): CORRECCIONES acotadas, **sin pedir otra ronda completa**: basta
con que pasen sus pruebas de aceptación. Este documento describe el estado después de las dos rondas y del cierre (§0 bis). **Las
correcciones del cierre no las ha revisado nadie más que sus pruebas.** Se distinguen **hechos** (comprobados con una prueba o un archivo),
*interpretaciones* y ***propuestas***.

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

## 0 bis. Cierre de la ronda 2 (revisión R2): hallazgo → cambio → prueba

Pruebas: **X** = grupo «X» de la batería `test_motor_a_f1_usgaap.py` (43 casos nuevos, más uno en el grupo W: 246 → 290); **PU12–PU14** =
`prueba_pipeline_usgaap.py`; **L5** = `probar_libro_v631_usgaap.py`; **rNN** = `mutaciones_usgaap.py`; **revisor** = sus guiones de aceptación, sin
cambios, con `COPIA_REVISION` apuntando al árbol corregido (resultados literales en el §8.2).

El cierre lo empezó otro agente y quedó guardado sin probar cuando su modelo agotó el límite (`b234e20`, «WIP»); lo terminó un agente
distinto (Claude, modelo Opus 5.5) en `00aa717`: ejecutó todas las pruebas, corrigió un fallo del borrador (fila R2-2: una declaración veraz
quedaba bloqueada) y escribió los resultados. Ninguno de los dos es el revisor.

| Hallazgo de la revisión R2 | Cambio | Prueba |
|---|---|---|
| **R2-1** (ALTA acotada) · una línea que nombra el arrendamiento **sin ser el tramo** («Loss on lease termination», el deterioro del derecho de uso…) valía como cita de «fuera» y llevaba a `concluido` sin condición; y con esa misma línea la declaración veraz «no_publicada» se bloqueaba | lista cerrada de términos **ajenos al tramo** (`_LINEA_AJENA`: deterioro, baja, cancelación, modificación, abandono, costes de salida, incentivos, venta con arrendamiento posterior, resultados; inglés y español), aplicada a los dos lados y sobre la etiqueta **entera** (también partida en renglones): una línea ajena **no** hace saltar «manda el dato» (la declaración veraz concluye CONDICIONADA, con su cota y la línea a la vista), **no** vale como cita de una ubicación (INCOMPLETO; el mensaje lleva a «no_publicada») y **no** cuenta entre las líneas sumadas que nombran un tramo | X (13), **PU12**, r01–r06 · revisor: `capa_r2.py C`, `pipeline_r2.py Y4 Y4h`, `matriz_r2.py` |
| **R2-2** (MEDIA) · un tramo contrastado dentro de la fila 14 admitía un importe declarado 0 sin compararlo con la cifra impresa | el importe declarado dentro de una fila se compara, año a año, con lo que la línea **propia** que la fase 1 sumó aporta a esa fila (su cifra impresa con el signo y la escala de la fase 1): otro importe —también un 0, se declare como se declare (con `cero_comprobado` en la rama de series incluido)— es DATOS INVÁLIDOS. Si la línea es **mezclada** con otras partidas (o su cifra no se puede leer), el importe no se puede comparar: con un tramo solo dentro de la fila 14 la conclusión queda CONDICIONADA, con los pagos o el coste como cota. Sin `fase1_partes`, la cota de un tramo declarado en la fila 14 cubre también el importe. La cifra de una línea que nombra **también los financieros**, o, en la fila 8, la de una línea **genérica** del derecho de uso («Amortization of right-of-use assets») cuando la amortización de los financieros puede estar dentro (por omisión o con D-WM), no es la del tramo operativo y **no se compara** (en la fila 14 condiciona; en la fila 8 es el límite 11). El borrador del cierre sí la comparaba y bloqueaba como DATOS INVÁLIDOS una declaración veraz (operativos 10 + financieros 5 = 15 impreso) | X (15), **PU13**, **L5**, r07–r15, r25–r26 · revisor: `capa_r2.py D`, `pipeline_r2.py Y5`, `fusion_r2.py` (M2), `matriz_r2.py` |
| **R2-3** (MEDIA) · la amortización del derecho de uso **financiero** «dentro de la fila 8» por omisión no miraba una línea contraria a la vista, y K3b decía «contrastado» | si el estado de flujos la muestra en una línea propia que la fase 1 **no** sumó en la fila 8 → DATOS INVÁLIDOS (el mensaje dice cómo declararla: `fuera_de_la_fila_8`); si ninguna línea sumada la nombra (una genérica del derecho de uso o una que nombra los financieros, también junto a los operativos), el tramo queda «por_omision» y K3b dice «según lo declarado» (K3 no se presenta como conforme). El caso por omisión sigue sin condicionar (como NIIF 16) | X (5), r16–r18, r27 · revisor: `capa_r2.py E` |
| **R2-4** (MEDIA) · la comprobación de forma de la ronda 2 bloqueaba la declaración real de `jumbo_d` (NIIF) por una nota de texto dentro de `series` | dentro de `series`, un **texto** en una clave que no es el nombre de una serie es una **nota**: se admite, no entra en el cálculo y queda a la vista (`F1-DECLARACION`, INFORMA; `notas_en_series`). Un texto en el lugar de una serie conocida sigue siendo DATOS INVÁLIDOS y el mensaje dice dónde se escribe una nota. Vacío = sin declarar: `[]`, `""` o `0` donde va un objeto se toman como vacíos, como antes de la ronda 2 (las 3 formas que pasaban de utilizable a bloqueada vuelven a ser utilizables). El expediente no se ha tocado | X (5), r19–r21 · la declaración real de Jumbo y las 135 formas del revisor (§8.2) |
| **Interpretación 5** · «Otro» en `L4` terminaba en `pendiente_de_datos`, como si faltara un dato | es un **límite del modelo**: `F1-NORMA` · MODELO NO APLICABLE (clase «norma»), que manda sobre lo que falte en la declaración → `no_entregable · límite del modelo`, con los motores A y B | X (4), **PU14**, r22–r23 · revisor: `pipeline_r2.py Y9` |
| **R2-6** (baja) · el aviso de `F1-US-C49` «explicado» pedía comprobar el riesgo contrario cuando C49 queda por debajo del principal | el texto distingue el sentido de la diferencia | X (1), r24 |

**No tocados** (gravedad baja, no pedidos en el cierre): R2-5 (a: con D-US2 bis, «cuánto cambiaría» usa la línea neta declarada aunque
contradiga pagos − coste; b: si no se puede calcular, publica igual, sin condición), la huella de `fase1_partes` en `vigencia()` (límite 5)
y el importe dentro de una D&A mezclada (D3: límite 11). Siguen sin tocar R1-2 (rama `f1/series-escala`) y R1-10.

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
   (`pendiente_de_datos`) si `fase1_v63.json` trae otra cosa. «Otro», el tercer valor de la lista de la plantilla, pasa el paso 2, y en el
   paso 7 la capa lo declara **límite del modelo** (F1 solo tiene reglas para NIIF y US GAAP; ningún dato lo arregla): `no_entregable`.
2. **Financieros.** Por omisión, como NIIF 16: `da_rou` es la amortización de su derecho de uso dentro de la fila 8 y C49 su principal;
   valen V-F1a, V-F1b, V-F1m, `F1-M-SIM`, A1/A2. El caso por omisión no se condiciona, pero manda el dato: si el estado de flujos muestra
   esa amortización en una línea propia que la fase 1 no sumó en la fila 8, es DATOS INVÁLIDOS; y si ninguna línea sumada la nombra, el tramo
   queda «por_omision» y K3b no dice «contrastado» (R2-3). Dos declaraciones lo cambian, con su evidencia:
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
   | `fila_8`, `fila_14` con su importe (R2-2) | el importe es el de la línea **propia** sumada en esa fila, cada año | un tramo solo en la fila 14 cuya línea es **mezclada**: el importe no se puede comparar | el importe no es el de su línea propia, también si es 0 (DATOS INVÁLIDOS) |
   | cualquier cita (R2-1) | — | — | la cita es, o está dentro de, una línea **ajena al tramo** (INCOMPLETO: si no hay línea del tramo, es `no_publicada`) |
   | los dos `fila_14` (D-US2 bis) | las dos líneas, la del activo y la del pasivo (o una que nombre los dos) | — | no se pueden comprobar las dos líneas (INCOMPLETO): no se publica el valor de la hoja |

   El tramo se reconoce por los términos pegados a «lease» o a «right-of-use» («lease liabilities» → pasivo; «right-of-use assets», «lease
   expense», «non-cash lease» → activo o gasto); una línea que nombra el arrendamiento sin precisar («Operating leases, net») vale para los dos.

   **Líneas ajenas al tramo** (R2-1). Una línea que nombra el arrendamiento junto a un término de otra cosa —*impairment, write-off,
   termination, modification, remeasurement, abandonment, exit, incentive, leaseback, gain, loss*; deterioro, saneamiento, baja, cancelación,
   rescisión, modificación, abandono, costes de salida, incentivo, arrendamiento posterior, ganancia, pérdida— no es ni la amortización del
   derecho de uso ni la variación del pasivo. Se mira la etiqueta entera (en «Impairment of long-lived assets and operating lease» /
   «right-of-use assets» el término está en el primer renglón). Una línea ajena no hace saltar «manda el dato», no prueba una ubicación y no
   cuenta entre las sumadas; las que haya en la página examinada quedan a la vista (`contraste_de_ubicaciones.lineas_ajenas_al_tramo`).

   **Importes** (R2-2). Lo que hay dentro de una fila es lo que la fase 1 sumó: cifra impresa × signo × escala del informe (en la fila 14,
   con el signo cambiado: «(10)» consume 10 de caja). Una línea es **propia** si su etiqueta entera solo lleva palabras de un tramo
   («Operating lease liabilities», «Non-cash lease expense»); con cualquier otra partida («accounts payable, accrued liabilities, operating
   lease liabilities and other…», «Depreciation and amortization, including…») es **mezclada** y su cifra no es la del arrendamiento.
   Tampoco es la del tramo operativo la cifra de una línea que nombra los financieros («Operating and finance lease liabilities») ni, en la
   fila 8, la de una línea genérica del derecho de uso («Amortization of right-of-use assets») cuando la amortización de los financieros
   puede estar dentro de la fila 8 (por omisión o con D-WM): esas cifras no se comparan.

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
  `desglose: "no_publicado"` (D-WM) y `amortizacion_rou` no se declaran a la vez: da DATOS INVÁLIDOS (`F1-US-DESGLOSE`; grupo W de la batería).
- **Notas** (R2-4; vale también con NIIF): una nota de texto se escribe en `nota` (primer nivel), en `nota` dentro del año de una serie o,
  dentro de `series`, como texto en una clave que **no** sea el nombre de una serie (queda a la vista en `notas_en_series`). Un texto en el
  lugar de una serie es DATOS INVÁLIDOS. Vacío = sin declarar (`null`, `{}`, `[]`, `""`, `0`).

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
| `F1-NORMA` | norma sin declarar o fuera de la lista; `L4` vacío o no reconocido; declaración ≠ libro. `L4` = «Otro»: límite del modelo | BLOQUEA (con «Otro»: MODELO NO APLICABLE → `no_entregable`, aunque falten datos) |
| `F1-DECLARACION` | claves no reconocidas, o una clave con contenido que tiene que ser un objeto y no lo es. Notas de texto dentro de `series`: INFORMA | BLOQUEA · DATOS INVÁLIDOS (las notas no bloquean) |
| `F1-US-MEZCLA` | declaración NIIF con claves o series de US GAAP; US GAAP con intereses pagados en financiación | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DESGLOSE` | falta `arrendamientos_us_gaap`, su registro, la existencia de una clase, una ubicación, su evidencia o una serie exigida; declaraciones incoherentes entre sí | BLOQUEA · INCOMPLETO o DATOS INVÁLIDOS |
| `F1-US-C49` | C49 distinto del principal financiero publicado más allá de su redondeo y sin explicar; C49 > 0 sin financieros o con D-WM | BLOQUEA · DATOS INVÁLIDOS (explicado: AVISO) |
| `F1-US-DA` | amortización del derecho de uso operativo dentro de la D&A con A0, o sola dentro del circulante sin su importe: dos veces | BLOQUEA · MODELO NO APLICABLE |
| `F1-US-SIM` | la simétrica: variación del pasivo sola dentro del circulante sin su importe, o amortización excluida de D_X sin pagos en el CFO | BLOQUEA · FUERA DEL DOMINIO |
| `F1-US-FILAS` | regla 8: contradicha (también por el importe de una línea propia, o por una línea propia de la amortización financiera que la fase 1 no sumó en la fila 8) o sin la línea que la prueba (también si la cita es de una línea ajena al tramo) | BLOQUEA · DATOS INVÁLIDOS o INCOMPLETO; sin contrastar: AVISO |
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
| un tramo declarado en la fila 14 sin contrastar | + el importe retirado (con su signo), si no estuviera dentro; y, si el importe fuera mayor que el declarado: como máximo, − (los pagos − el importe) para el pasivo o + (el coste − el importe) para la amortización |
| un tramo dentro de una línea mezclada de la fila 14 (ubicación contrastada, importe sin comparar) | las dos anteriores, sobre el importe |
| amortización financiera declarada fuera de la fila 8 sin contrastar | + el importe publicado |
| D-WM | − (caja pagada − gasto total): **estimación**, no cota |

El resumen (`cota.resumen`) suma las variaciones del mismo signo (dos ubicaciones falsas a la vez se acumulan) y no compensa las de signo
contrario. Con declaraciones veraces, la cota cubre el error en todos los casos de la matriz de la revisión; con la matriz de la revisión R2
(360 pares, cinco formas de citar), también con las falsas: ningún caso utilizable con el error fuera de la cota ni con error y sin condición (§8.2).

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
| US GAAP · línea que nombra el arrendamiento sin ser un tramo (deterioro, cancelación…) | no es un tramo: «no_publicada» veraz → D-US1; como cita de «fuera» → INCOMPLETO | X, PU12 | condicionada · `pendiente_de_datos` |
| US GAAP · un tramo en una línea propia de la fila 14 con otro importe (un 0) | DATOS INVÁLIDOS: el importe es el de su línea | X, PU13 | `pendiente_de_datos` |
| US GAAP · un tramo en una línea mezclada de la fila 14 con importe 0 | el importe no se puede comparar: condicionada, con los pagos o el coste como cota | X | utilizable y condicionada |
| US GAAP · amortización operativa en una línea genérica de la D&A que también lleva la de los financieros (10 + 5 impreso como 15) | su cifra no es la del tramo operativo: no se compara (límite 11) | X | utilizable (declaración veraz) |
| US GAAP · amortización financiera en una línea propia que la fase 1 no sumó en la fila 8, declarada dentro por omisión | DATOS INVÁLIDOS: se declara `fuera_de_la_fila_8` | X | `pendiente_de_datos` |
| Mezcla de normas | `F1-NORMA`, `F1-US-MEZCLA` | N, PU9 | `pendiente_de_datos` |
| Norma «Otro» | `F1-NORMA` · límite del modelo | X, PU14 | `no_entregable` |
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

LibreOffice siempre con `flock /home/user/e_work/libreoffice.lock`, una ejecución detrás de otra. Salidas en `resultados/` (las de una
ronda anterior se conservan con el sufijo de su commit o se sustituyen por las nuevas del mismo guion).

### 8.1 Ronda 2 (código de `a6fc300`; es lo que examinó la revisión R2)

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
campaña repetida con ese cambio da la misma salida, byte a byte (`84 de 84 mutaciones detectadas`), y no deja nada. Quedaba un defecto
menor: una ejecución normal de la batería dejaba 41 carpetas **vacías** (el bucle de declaraciones al azar, cuando la declaración mutada no
deja escribir la fuente). **Corregido en el cierre de la ronda 2:** la batería ya no deja ninguna y borra las suyas también si se interrumpe.

### 8.2 Cierre de la ronda 2 (correcciones de la revisión R2; código de `00aa717`)

Los guiones del revisor (`evidencia_r2/` de la revisión R2) se ejecutan **sin cambios**, con `COPIA_REVISION` = el árbol del worktree y
`TMP_R2` = una carpeta temporal propia. Salidas: `resultados/guiones_de_la_revision_R2_contra_el_cierre.txt` (salidas completas de los
guiones de aceptación) y `resultados/diferenciales_niif_y_examen_cierre.txt` (NIIF, expedientes reales y declaraciones al azar); las de las
baterías del autor sustituyen a las de la ronda 2 (`mutaciones_usgaap.txt`, `prueba_pipeline_usgaap.txt`, `probar_libro_v631_usgaap.json`,
`prueba_pipeline_f1_gancho.txt`, `regresion_elis_f1_tras_usgaap.md`).

**Pruebas de aceptación de la revisión R2** (criterios de su §5):

| Guion del revisor | Criterio | Resultado literal |
|---|---|---|
| `capa_r2.py C` (R2-1) | C1 utilizable y condicionado; C2–C4 ya no «contrastada» | C1: `utilizable True · CONDICIONADA (D-US1) cota [-12.0, 12.0] · flujo capa 78.0 · … error +10.0 · bloquean []` (antes bloqueaba `F1-SERIES`); C2: `utilizable False · … bloquean ['F1-US-FILAS'] · contraste [am:insuficiente/pas:hipotesis_D_US1]`; C3 y C4: `utilizable False · … bloquean ['F1-US-FILAS'] · contraste [am:insuficiente/pas:insuficiente]` (antes utilizables sin condición, error +10); C5: `bloquean ['F1-US-FILAS']` (antes error −10 sin condición); C6: los 14 rótulos, `lados —` |
| `capa_r2.py D` (R2-2) | D2 bloquea; D1 igual que hoy | D1: `utilizable False · sin condición · flujo capa 68.0 · flujo del libro 78.0 · bloquean ['F1-LIBRO'] · contraste [am:contrastada/pas:contrastada]` (igual que en `bcb6dc3`); D2: `utilizable False · … bloquean ['F1-US-FILAS'] · contraste [am:contrastada/pas:contradicha]` (antes utilizable sin condición, error +10); D2b: `CONDICIONADA (F1-US-FILAS) cota [-12.0, 12.0] · … error +10.0` (antes cota `[0, 12.0]`, que no cubría el error); D3 y D4, sin cambio (límite 11 y R2-5, no pedidos) |
| `capa_r2.py E` (R2-3) | E2 no se acepta; K3b no dice «contrastado» | E1: `utilizable True · sin condición · … contraste [am:contrastada/pas:contrastada/fin:por_omision] · K3b una vez (no contrastado)` (el caso por omisión no se condiciona: interpretación 8); E2: `utilizable False · … bloquean ['F1-US-FILAS'] · contraste [… fin:contradicha]` (antes +5 sin condición); E3 y E4 sin cambio |
| `matriz_r2.py` | 0 «ERROR SIN CONDICIÓN» y 0 «FUERA DE COTA» | pasada A: `utilizables 8 de 120 · con error y SIN condición: 0 · condicionados con el error FUERA de la cota: 0`; pasada B: `utilizables 24 de 120 · … 0 · … 0`; pasada C: `utilizables 24 de 120 · … 0 · … 0` (en `bcb6dc3`: 2 y 1, 1 y 3, 0 y 2) |
| `pipeline_r2.py Y0 Y4 Y4h Y5 Y9` (LibreOffice) | Y4h `concluido` CONDICIONADA; Y4 no `concluido` sin condición; Y5 | Y0 (control): `estado final: concluido · paso 14 · … bloquean []`, flujo 148,000; Y4: `estado final: pendiente_de_datos · paso 7 · … bloquean ['F1-US-FILAS']` (INCOMPLETO: «la cita 'Loss on lease termination' nombra el arrendamiento junto a…»; antes `concluido` sin condición, +2,695); Y4h: `estado final: concluido · paso 14 · … bloquean []`, `condicionada: D-US1`, `cota: el flujo sin crecimiento podría cambiar entre -3.449 y +3.557 mm (-2.3 % y +2.4 %)` (error +2,695, dentro; antes `pendiente_de_datos`); Y5: `estado final: pendiente_de_datos · paso 7 · … bloquean ['F1-US-FILAS']` (DATOS INVÁLIDOS; antes `concluido` sin condición); Y9: `estado final: no_entregable · paso 7 · motor B · … bloquean ['F1-NORMA']`, `causa: limite_del_modelo` (antes `pendiente_de_datos`) |
| `fusion_r2.py`, árbol fusionado con `origin/f1/series-escala` @ `a27788c` | M2 bloquea | M2: `utilizable: False · condicionada: None · bloquean: ['F1-US-FILAS'] · flujo 78.0 (correcto 68) · contraste {'amortizacion_rou': 'contrastada', 'variacion_pasivo': 'contradicha'}` (antes utilizable sin condición); M1 (Zoetis real, «—» de 2023) igual que en la revisión: `bloquean: ['F1-K3a', 'F1-LIBRO'] · condicionada: D-US1` |

El árbol fusionado se obtiene sin fusionar ramas: `git merge-tree --write-tree HEAD origin/f1/series-escala` (solo choca el manifiesto;
`motor_a_f1.py`, `metadatos_fase1.md`, `README_V6.3.1_F1.md` y `verificar_paquete.sh` se fusionan solos), con `personaje_v2/{scripts,
pruebas,esquema,prompts}` y los `config*.json` de ese árbol en una carpeta temporal y lo demás enlazado en solo lectura. En él: `290/290 pruebas del motor A F1 con US GAAP PASAN`, `163/163 pruebas del motor A F1 (4.15) PASAN`, `80/80 pruebas de F1-SERIES con escala y ceros PASAN` (`test_f1_series_escala.py`) y `29/29 pruebas V6.3.1 F1 (sin LibreOffice) PASAN`; con la declaración real de Jumbo, la nota tampoco bloquea.

**Baterías del autor** (código de `00aa717`):

| Orden | Resultado literal |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1_usgaap.py` (ronda 2: 246; borrador del cierre: 287) | `290/290 pruebas del motor A F1 con US GAAP PASAN` |
| `python3 -I …/f1_usgaap/scripts/mutaciones_usgaap.py` (112: las 84 de la ronda 2, n47 y las 27 del cierre, r01–r27) | `112 de 112 mutaciones detectadas` (15 min 34 s con dos trabajadores; `resultados/mutaciones_usgaap.txt`) |
| `flock … python3 -B …/f1_usgaap/scripts/prueba_pipeline_usgaap.py` (ronda 2: 22) | `26/26 pruebas de F1 · US GAAP en el pipeline PASAN` (582 s) |
| `flock … python3 -I …/f1_usgaap/scripts/probar_libro_v631_usgaap.py <carpeta nueva>` (ronda 2: 15) | `16/16 comprobaciones de F1 · US GAAP sobre el libro V6.3.1 PASAN` |
| NIIF: `python3 -B pruebas/test_motor_a_f1.py` | `163/163 pruebas del motor A F1 (4.15) PASAN` |
| `python3 -B pruebas/test_v631_f1.py` | `29/29 pruebas V6.3.1 F1 (sin LibreOffice) PASAN` |
| `python3 -I v6/v631_f1/scripts/probar_v631_f1.py estructura` | `21/21 comprobaciones V6.3.1 F1 (estructura) PASAN` |
| `flock … prueba_pipeline_f1.py` (gancho) | `8/8 pruebas del gancho F1 del pipeline PASAN` |
| `python3 -I …/f1_impl/scripts/regresion_elis_f1.py <copia>` | `39/39 PASAN` (el informe es el de la ronda 2, salvo la ruta de la copia; los archivos que el guion reescribe en `f1_impl/resultados/` se han devuelto a su versión registrada) |

**NIIF y expedientes reales** (solo lectura; `resultados/diferenciales_niif_y_examen_cierre.txt`):
- Declaraciones NIIF reales del examen sobre sus libros (`examen_real_worker.py`): Ahold ×3 y Elis, idénticas a `bcb6dc3` (todo el
  resultado salvo versión y fecha). Jumbo (`jumbo_d`) vuelve a lo de la base (`1694f08`): bloquea solo `F1-SERIES` (la escala de su
  declaración, que trata `f1/series-escala`), con la nota a la vista (`F1-DECLARACION` · INFORMA, `notas_en_series`); sin la nota, lo
  mismo. Con el código fusionado, igual: la nota ya no bloquea. El expediente no se ha tocado.
- 135 formas mal construidas de una declaración NIIF utilizable (`formas_niif_worker.py`): «utilizable» igual que en la ronda 1 en las
  135 (31 utilizables; en la ronda 2, 28): las tres de `normalizacion` con `[]`, `""` o `0` vuelven a ser utilizables; ninguna excepción
  (cuatro de la ronda 1 son ahora DATOS INVÁLIDOS).
- `vigencia()` de F1 de los expedientes con `estado_pipeline.json`: 53 del árbol y 21 del examen, **0 distintos** entre `bcb6dc3` y `00aa717`.
- Zoetis real (`zoetis_real_r2.py`): el mismo resultado que en la revisión; solo aparece el tramo financiero como `por_omision` (R2-3).
- `fuzz_r2.py 3000`: ninguna excepción; 46 utilizables, todos sin tramos del arrendamiento operativo.

**Ayudas de las pruebas.** Desde el borrador del cierre, las ayudas que también usan los guiones del revisor (`expediente()` de la batería,
`escribir_fuente`/`preparar` de `prueba_pipeline_usgaap.py` y el expediente de `probar_libro_v631_usgaap.py`) imprimen en las líneas
propias del arrendamiento que la fase 1 suma en la fila 14 la cifra que suma de verdad («(10)» → +10 en la fila; «10» → −10), coherente
con el libro, y llevan la unidad del informe en `fase1_partes` (la fase 1 la exige). Antes llevaban una cifra cualquiera, que nadie
comparaba; sin ese cambio el D1 veraz del revisor daría DATOS INVÁLIDOS. Los guiones del revisor no se han tocado.

**Paquete.** `verificar_paquete.sh completa` no se ha repetido en el cierre: sus bloques de F1 se han ejecutado uno a uno (arriba: US GAAP
290, 26 y 16; motor A F1 163; gancho 8; V6.3.1 29 y 21); los demás (comprobadores, sintética, V6.4, cierre…) no. Sus mínimos pasan a 290,
26 y 16. El modo rápido sobre una copia limpia se registra en el commit siguiente, en el que solo cambian este documento y el manifiesto.

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
   contraste con una línea. Desde el cierre (R2-3): manda el dato si una línea propia que la fase 1 no sumó la muestra fuera, y K3b no dice
   «contrastado» si ninguna línea sumada la nombra. La revisión R2 la juzgó «razonable como omisión»; no viene de ninguna decisión.
9. (cierre) **La lista de términos ajenos es cerrada y es del autor** (los diez de la revisión, sus variantes y sus equivalentes en español).
   Una línea que mezcla un tramo con un término ajeno («Amortization and impairment of operating lease right-of-use assets») se trata como
   ajena: no se puede citar y no hace saltar «manda el dato»; la conclusión sale condicionada, con la cota que cubre el tramo.
10. (cierre) Una línea es «propia» por vocabulario (`_PALABRAS_PROPIAS`): en caso de duda se toma como mezclada, que condiciona en lugar de
   bloquear. El importe se compara también en la fila 8 cuando la amortización es una línea propia que la fase 1 sumó en la D&A, salvo que la
   línea nombre también los financieros o que sea genérica («Amortization of right-of-use assets») y la amortización de los financieros
   pueda estar dentro de la fila 8 (por omisión o con D-WM): su cifra puede sumar las dos y no se compara (en la fila 14 la misma regla
   condiciona). Ante la duda, no comparar: una comparación equivocada bloquearía una declaración veraz (lo hacía el borrador del cierre).
11. (cierre) Dentro de `series`, cualquier texto en una clave que no sea una serie se admite como nota. Las claves desconocidas que sí son
   un objeto por año se siguen sin examinar, como antes.

Límites:
1. **El cero publicado sigue sin poder declararse** (R1-2): un principal «—», o un importe «dentro de la fila» igual a cero, da
   `F1-SERIES` DATOS INVÁLIDOS. Zoetis (principal de 2023 «—») no concluye hasta que se integre `f1/series-escala`.
2. El contraste de la regla 8 es **por el texto de las etiquetas**, con patrones en inglés y en español. No ve un arrendamiento dentro de
   una línea que no lo nombra en ningún renglón: por eso lo que no se puede contrastar queda condicionado, no acreditado. Una cabecera sin
   cifras y sin dos puntos justo encima de una línea se toma como primer renglón de su etiqueta; si nombrara el arrendamiento, la línea
   se trataría como suya (bloquearía; no cambia ningún valor).
3. **Líneas que nombran el arrendamiento sin ser un tramo** (R2-1). Cerrado para los términos de la lista (regla 8). Queda el límite de toda
   lista cerrada: una línea que nombre el arrendamiento, no sea un tramo y no lleve ninguno de esos términos sigue valiendo como cita de
   «fuera» y sigue bloqueando un `no_publicada` veraz. La comprobación más robusta que propone la revisión (con los dos tramos «fuera» en
   líneas propias, que sus cifras impresas sumen coste − pagos) **no** está implantada: exige leer las cifras de líneas que la fase 1 no
   guarda. Según la revisión R2 (§8, con sus datos reales), Zoetis y Waste Management no tienen líneas de este tipo.
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
11. **El importe dentro de una D&A mezclada no se compara con ninguna cifra impresa** (R2-2, caso D3 de la revisión): con la amortización del
   derecho de uso operativo dentro de una D&A que la nombra, un importe inflado sobrevalora y uno reducido infravalora, sin condición. Es
   el mismo límite que tiene NIIF con `da_rou`: el importe lleva su propia cifra publicada (`F1-SERIES`), no la de la línea. Lo mismo con una
   línea genérica del derecho de uso que puede llevar también la amortización de los financieros (interpretación 10).
12. Con **un solo tramo** dentro de la fila 14 la declaración veraz sigue sin salida (R1-10, `F1-LIBRO`): con su importe, ningún libro lo
   retira; con otro importe, DATOS INVÁLIDOS o condicionada. La salida sigue siendo la del §7.
13. R2-5 (D-US2 bis): «cuánto cambiaría contando los pagos» usa la línea neta declarada aunque no coincida con pagos − coste, y si no se
   puede calcular se publica igual, sin condición. Sin tocar.
