# F1 · US GAAP (ASC 842) · motor A con arrendamientos operativos y financieros

Fecha: 18-nov-2026. Lo escribe el agente autor de la reparación (Claude) en la rama `f1/usgaap`, creada desde `examen/ahold-f1` @ `1694f08`.
**Sin revisión independiente todavía**: la hará otro agente. Aquí se distinguen **hechos** (comprobados con una prueba o un archivo),
*interpretaciones* y ***propuestas***.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** Superar estas guardas no acredita aptitud.
La V6.3, la V6.3.1 F1 (`eaece01a…`), sus referencias y los expedientes hechos con ellas **no cambian**. NIIF no cambia.

## 1. Qué había y qué cambia

**Hecho.** Con US GAAP la capa `personaje_v2/scripts/motor_a_f1.py` bloqueaba siempre (`F1-NORMA`, límite declarado): toda empresa
estadounidense con el motor A terminaba en «límite del modelo». Además la norma del libro se leía buscando «ifrs|niif|ias» dentro del texto
de `Control maestro L4` (H13 de la revisión de F1-IMPL: «US GAAP (no IFRS)» pasaba como NIIF).

**Cambio.** La norma es un valor cerrado y la capa implanta ASC 842 con los arrendamientos **operativos** y **financieros** por separado.
No se adopta ninguna política económica nueva: se aplican las decisiones F1 ya registradas ((1a) b: la reinversión que calibra f excluye la
amortización de los derechos de uso; un solo perímetro; K3: el alquiler se cuenta una vez) a lo que la norma estadounidense publica.

## 2. La norma, en lo que importa al modelo

Citas de ASC 842 y ASC 230 escritas de memoria por el autor (sesión sin internet): **el revisor debe contrastarlas**.

| | Arrendamiento **operativo** (ASC 842) | Arrendamiento **financiero** (ASC 842) | NIIF 16 (referencia) |
|---|---|---|---|
| Cuenta de resultados | un solo coste lineal dentro del resultado de explotación (842-20-25-6, 842-20-45-4): el EBIT ya lleva el alquiler **entero** | amortización del derecho de uso (con la D&A) e interés (con el gasto financiero) | amortización + interés |
| Estado de flujos | los pagos, **dentro del flujo de explotación (CFO)** (842-20-45-5 c) | principal en **financiación**; interés en explotación (842-20-45-5 a y b; ASC 230-10-45-17) | principal en financiación; interés en explotación o financiación |
| Balance | activo por derecho de uso y pasivo, separados de los financieros (842-20-45-1 a 3) | activo y pasivo propios | activo y pasivo |
| Notas (842-20-50-4) | coste del arrendamiento operativo; **caja pagada dentro del flujo de explotación** | amortización del derecho de uso e interés; **caja pagada en financiación** | — |
| Lo que la norma **no** fija | en qué línea de la conciliación del CFO va la amortización no monetaria del derecho de uso ni la variación del pasivo: cada empresa lo presenta a su manera | — | — |

Consecuencia para el motor A (`flujo = V·[m(1−τ) − f] − ΔV/S2C`, con `f = (NOPAT − (capex − D_X + circulante) − FCF base) ÷ ventas`):
en régimen estable el flujo sin crecimiento es `FCF base + capex − D_X + circulante`. El alquiler operativo ya está **una vez** en el FCF
base (el pago va en el CFO). Se cuenta **dos veces** si su amortización no monetaria está dentro de D_X (fila 8) o si sus pagos se restan
otra vez en C49; se **omite** (casi entero) si la variación de su pasivo está sola dentro del circulante (fila 14). Los financieros se
comportan como en NIIF 16.

## 3. Reglas (qué hace la capa con US GAAP)

1. **Norma, valor cerrado.** `norma_contable.valor` es `NIIF` o `US_GAAP`. `Control maestro L4` se lee con una lista cerrada de valores
   exactos (`IFRS`, `NIIF`, las dos variantes históricas `IFRS (IFRS-EU)` e `IFRS (adoptadas por la Unión Europea)` → NIIF; `US GAAP` →
   US GAAP). Cualquier otro texto bloquea. Declaración y libro tienen que decir lo mismo.
2. **Financieros (como NIIF 16).** `da_rou` es la amortización del derecho de uso de los arrendamientos **financieros** dentro de la fila 8;
   C49 es su principal (financiación). Valen las reglas F1 existentes: V-F1a, V-F1b, V-F1m, `F1-M-SIM`, A1/A2.
3. **Operativos.** Se declara dónde están, en el estado de flujos, sus dos tramos no monetarios, y con eso:

   | Amortización no monetaria del derecho de uso | Variación del pasivo | Qué hace la capa | La proyección cuenta |
   |---|---|---|---|
   | fuera de las filas 8 y 14 | fuera de las filas 8 y 14 | nada: el alquiler ya está una vez (EBIT y CFO) | los pagos |
   | **dentro de la fila 8** (se declara su importe) | fuera | la excluye de D_X con A1/A2 ((1a) b); con A0 **bloquea** (`F1-US-DA`) | los pagos |
   | fuera | **dentro de la fila 14** (se declara su importe) | la retira del circulante que usa la reinversión; sin importe **bloquea** (`F1-US-SIM`) | los pagos |
   | dentro de la fila 8 | dentro de la fila 14 | las dos cosas | los pagos |
   | dentro de la fila 14 | dentro de la fila 14 | nada: los dos tramos están netos en el circulante publicado | el coste lineal |
   | dentro de la fila 14 | fuera | retira del circulante el tramo del activo (importe con su signo); sin importe **bloquea** (`F1-US-DA`) | los pagos |
   | sin declarar, o «no publicada» | | **bloquea** · `pendiente_de_datos` (`F1-US-DESGLOSE`) | — |

4. **Perímetros.** `D_X(A1) = D&A − ROU dentro de la fila 8` y `D_X(A2) = … − PPA`, donde «ROU dentro de la fila 8» es la de los
   financieros más la de los operativos que estén dentro de la fila 8. A0 no cambia.
5. **C49 solo lleva principal de arrendamientos financieros.** Con US GAAP los pagos operativos están en el CFO: si C49 supera el
   principal financiero publicado, se restarían dos veces (`F1-US-C49`); si no lo alcanza, el principal financiero se omitiría.
6. **Puente de deuda (motor B).** El pasivo por arrendamiento **operativo** no es deuda del puente: su pago ya está entero en el EBIT que
   proyecta el motor B. La deuda coherente del puente es `deuda financiera + pasivo por arrendamientos financieros`. Si la fila 23 del
   libro lleva pasivo operativo, el motor B lo restaría además (`Historia C64 = fila 22 + fila 23`): `F1-US-PUENTE` **bloquea** con el
   motor B e informa con el motor A (que no resta deuda). Con el motor B y US GAAP, F1 se exige solo para esto.
7. **K3.** K3a (caja base por dos vías) no depende de la norma. K3b cuenta el alquiler por clase: los operativos, 1 (EBIT y CFO) + 1 si
   C49 lleva pagos operativos + 1 si su amortización queda en D_X o sola en el circulante − 1 si la variación del pasivo queda sola en el
   circulante; los financieros, como en NIIF. Tiene que dar exactamente uno en cada clase que exista. K3c no cambia.

## 4. Qué se declara (en `motor_a_f1.json`, además de lo de NIIF)

```json
"norma_contable": {"valor": "US_GAAP", "registro": {"fecha": "…", "persona": "…", "motivo": "…"}},
"arrendamientos_us_gaap": {
  "registro": {"fecha": "…", "persona": "…", "motivo": "…"},
  "operativos":  {"existen": true, "documento": "…", "pagina": 0, "cita": "…",
                  "amortizacion_rou": {"ubicacion": "fuera_de_las_filas_8_y_14", "documento": "…", "pagina": 0, "cita": "…"},
                  "variacion_pasivo": {"ubicacion": "fila_14", "documento": "…", "pagina": 0, "cita": "…"}},
  "financieros": {"existen": false, "documento": "…", "pagina": 0, "cita": "…"}
}
```

`ubicacion`: `fila_8` (solo la amortización), `fila_14`, `fuera_de_las_filas_8_y_14` o `no_publicada`. Cada clasificación lleva documento,
página y una cita literal, que se busca en la página de una fuente del expediente con su huella (`fuentes_series`), como `F1-SERIES`.

Series (mismo formato que `da_rou`: `valor_fuente` con su signo, `signo`, `tratamiento`, `documento`, `pagina`, `literal`, `fila`):

| Serie | Qué es (dónde se publica) | Cuándo se exige |
|---|---|---|
| `pagos_arr_operativo` | caja pagada por arrendamientos operativos dentro del flujo de explotación (nota de arrendamientos) | operativos: años de la ventana |
| `da_rou_operativo` | amortización del derecho de uso operativo **dentro de la fila 8** | ubicación `fila_8`: ventana (y H–L para el ancla) |
| `circulante_arr_operativo` | importe del arrendamiento operativo **dentro de la fila 14**, con el signo de la fila 14 (+ consume caja) | un solo tramo en la fila 14: ventana (y H–L) |
| `pasivo_arr_operativo` | pasivo por arrendamiento operativo **dentro de la fila 23** | operativos: último ejercicio |
| `da_rou` | amortización del derecho de uso de los **financieros** dentro de la fila 8 | financieros: ventana (y H–L) |
| `pagos_arr_financiero_principal` | principal pagado de los financieros (financiación) | financieros, o C49 > 0: ventana |
| `coste_arr_operativo` | coste lineal del arrendamiento operativo | opcional: solo para la sensibilidad coste − pagos |

Sin arrendamientos de una clase (`existen: false`, con su evidencia) no se declaran sus series.

## 5. Qué bloquea (guardas nuevas o cambiadas)

| Id | Salta cuando | Efecto |
|---|---|---|
| `F1-NORMA` | norma sin declarar o fuera de la lista cerrada; `L4` vacío o no reconocido; declaración ≠ libro (mezcla de normas) | BLOQUEA |
| `F1-US-MEZCLA` | declaración NIIF con claves o series de US GAAP; US GAAP con intereses pagados en financiación (C48 o fila 16 > 0: no existen en US GAAP, se restarían dos veces) | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DESGLOSE` | falta `arrendamientos_us_gaap`, su registro, la existencia de una clase, una ubicación, su evidencia o una serie exigida; ubicación «no publicada» | BLOQUEA · INCOMPLETO (`pendiente_de_datos`) |
| `F1-US-C49` | C49 distinto del principal financiero publicado (de más: pagos operativos restados dos veces; de menos: principal omitido); C49 > 0 sin financieros | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DA` | amortización del derecho de uso operativo dentro de la D&A con A0, o sola dentro del circulante sin retirar: alquiler contado dos veces | BLOQUEA · MODELO NO APLICABLE |
| `F1-US-SIM` | lo simétrico: variación del pasivo sola en el circulante sin retirar, o amortización operativa excluida de D_X sin pagos en el CFO: alquiler omitido | BLOQUEA · FUERA DEL DOMINIO |
| `F1-US-PUENTE` | la fila 23 lleva pasivo por arrendamiento operativo: con el motor B bloquea (contado en el EBIT y en la deuda); con el A informa | BLOQUEA (B) · INFORMA (A) |
| `F1-US-BASE` | informa de si la proyección cuenta los pagos o el coste lineal, y de la diferencia si se declaran los dos | INFORMA |
| `F1-K3b` | cuenta por clase distinta de uno | BLOQUEA |
| `F1-LIBRO` | además: hay un ajuste del circulante declarado, que ningún libro calcula hoy (§7) | BLOQUEA · límite declarado |
| `F1-SERIES` | además: las series de US GAAP y las citas de las clasificaciones | BLOQUEA si nada más bloquea |

## 6. Casos sintéticos (batería `personaje_v2/pruebas/test_motor_a_f1_usgaap.py`)

Empresa estable: ventas 1.000; resultado antes de alquileres y amortizaciones 100; capex propio = D&A propia = 20; alquiler operativo 12
(coste lineal = pago; 10 de amortización no monetaria y 2 de actualización del pasivo). EBIT 68, CFO 88, FCF base 68. La caja verdadera
sin crecimiento es 68. Con financieros: derecho de uso 5, interés 1, principal 5 → EBIT 63, CFO 87, FCF base 62.

| Caso | Datos | Resultado esperado |
|---|---|---|
| U1 · solo operativos, tramos fuera de las filas | fila 8 = 20; fila 14 = 0; C49 = 0 | A0 y A2 dan 68; alquiler una vez; utilizable |
| U2 · operativos + financieros | fila 8 = 25; C49 = 5 | A2 da 62; A0 da 57 y bloquea V-F1a |
| U3 · D&A con derecho de uso operativo dentro | fila 8 = 30 | A0 da 58 y bloquea `F1-US-DA` (dos veces); A2 da 68 |
| U4 · C49 con pagos operativos | C49 = 12; FCF base 56 | `F1-US-C49` bloquea; dos veces |
| U5 · desglose ausente | sin `arrendamientos_us_gaap`, sin ubicación, «no publicada» | `F1-US-DESGLOSE`; `pendiente_de_datos` |
| U6 · variación del pasivo sola en la fila 14 | fila 14 = +10 | tal cual daría 78; con el ajuste, 68; sin el importe, `F1-US-SIM` (ninguna vez); con el importe, `F1-LIBRO` (el libro no lo calcula) |
| U7 · los dos tramos en la fila 14 | fila 14 = −10 + 10 | 68 sin tocar nada; la proyección cuenta el coste lineal |
| U8 · mezcla de normas | US GAAP declarada y libro IFRS; NIIF con claves US; US GAAP con C48 > 0 | `F1-NORMA` / `F1-US-MEZCLA` |
| U9 · simétricas | financieros con A2 y C49 = 0; operativos excluidos de D_X sin pagos | `F1-M-SIM` / `F1-US-SIM` |
| U10 · puente | fila 23 con 50 de pasivo operativo | motor A informa; motor B bloquea; deuda coherente = fila 22 + fila 23 − 50 |
| U11 · NIIF no cambia | casos T5, T6, T7 y AH de la batería existente | mismas cifras y mismas guardas |
| U12 · libro V6.3.1 | la fila 86 lleva la suma (financieros + operativos dentro de la fila 8) | el oráculo coincide |
| U13 · con crecimiento e impuestos | ventas +5 %; τ 25 % | A2 da la caja sostenible a crecimiento cero |

## 7. Límites declarados

*(Se completa al final con las pruebas ejecutadas.)*
