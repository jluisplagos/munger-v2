# F1 · US GAAP (ASC 842) · motor A con arrendamientos operativos y financieros

Fecha: 18-nov-2026. Lo escribe el agente autor de la reparación (Claude, modelo Fable 5.2) en la rama `f1/usgaap`, creada desde
`examen/ahold-f1` @ `1694f08`. **Sin revisión independiente todavía**: la hará otro agente. Se distinguen **hechos** (comprobados con una
prueba o un archivo), *interpretaciones* y ***propuestas***.

**Aptitud: uso supervisado experimental. No apto para decisiones con dinero real.** Superar estas guardas no acredita aptitud.
La V6.3, la V6.3.1 F1 (`eaece01a…`), sus referencias y los expedientes hechos con ellas **no cambian**. NIIF no cambia (§8).

## 1. Qué había y qué cambia

**Hecho.** Con US GAAP la capa `personaje_v2/scripts/motor_a_f1.py` bloqueaba siempre (`F1-NORMA`, límite declarado): toda empresa
estadounidense con el motor A terminaba en «límite del modelo». La norma del libro se leía buscando «ifrs|niif|ias» dentro del texto de
`Control maestro L4` (H13 de la revisión de F1-IMPL: «US GAAP (no IFRS)» pasaba como NIIF).

**Cambio.** La norma es un valor cerrado y la capa implanta ASC 842 con los arrendamientos **operativos** y **financieros** por separado.
Se aplican las decisiones F1 ya registradas ((1a) b: la reinversión que calibra f excluye la amortización de los derechos de uso; K3: el
alquiler se cuenta una vez) y las dos de la persona responsable del 18-nov-2026 para US GAAP (`DECISIONES_PARA_EL_USUARIO.md`:96–98):

- **D-US1 · hipótesis general declarada.** Si la empresa no publica en qué líneas del estado de flujos van los dos tramos del arrendamiento
  operativo (la amortización del derecho de uso y la variación del pasivo), se supone que van netos dentro del flujo de explotación, fuera
  de las filas 8 y 14 de la Historia. Es una hipótesis, no un dato: la conclusión se presenta como **condicionada**, con su cota. Donde la
  empresa publica las líneas, manda el dato.
- **D-US2.** Cuando el coste lineal y los pagos del año difieren, se cuentan los **pagos** y la diferencia queda a la vista, sin bloquear.

No se adopta nada más. Las elecciones del autor que no vienen de una decisión están marcadas como *interpretación* en el §9.

## 2. La norma, en lo que importa al modelo

Las citas de ASC 842 y ASC 230 están escritas de memoria (sesión sin internet): **el revisor debe contrastarlas**.

| | Arrendamiento **operativo** | Arrendamiento **financiero** | NIIF 16 (referencia) |
|---|---|---|---|
| Cuenta de resultados | un solo coste lineal dentro del resultado de explotación (842-20-25-6, 842-20-45-4): el EBIT lleva el alquiler **entero** | amortización del derecho de uso (con la D&A) e interés (gasto financiero) | amortización + interés |
| Estado de flujos | los pagos, **dentro del flujo de explotación (CFO)** (842-20-45-5 c) | principal en **financiación**; interés en explotación (842-20-45-5 a y b; ASC 230-10-45-17) | principal en financiación |
| Balance | derecho de uso y pasivo, separados de los financieros (842-20-45-1 a 3) | derecho de uso y pasivo propios | derecho de uso y pasivo |
| Notas (842-20-50-4) | coste del arrendamiento operativo; **caja pagada dentro del flujo de explotación** | amortización e interés; **caja pagada en financiación** | — |
| Lo que la norma no fija | en qué línea de la conciliación del CFO van la amortización no monetaria del derecho de uso y la variación del pasivo: cada empresa lo presenta a su manera | — | — |

Motor A: `flujo = V·[m(1−τ) − f] − ΔV/S2C`, con `f = (NOPAT − (capex − D_X + circulante) − FCF base) ÷ ventas`. En régimen estable el flujo
sin crecimiento es `FCF base + capex − D_X + circulante`. El alquiler operativo ya está **una vez** en el FCF base (el pago va en el CFO).
Se contaría **dos veces** si su amortización no monetaria quedara dentro de D_X (fila 8), si quedara sola dentro del circulante (fila 14)
o si sus pagos se restaran otra vez en C49. Se **omitiría** (casi entero) si la variación de su pasivo quedara sola dentro del circulante.

## 3. Reglas

1. **Norma, valor cerrado.** `norma_contable.valor` es `NIIF` o `US_GAAP`. `Control maestro L4` se lee con una lista cerrada de valores
   exactos, sin distinguir mayúsculas ni espacios de más: `IFRS`, `NIIF`, `IFRS (IFRS-EU)`, `IFRS (adoptadas por la Unión Europea)` → NIIF;
   `US GAAP` → US GAAP. Cualquier otro texto bloquea. La declaración y el libro tienen que decir lo mismo.
2. **Financieros (como NIIF 16).** `da_rou` es la amortización de su derecho de uso dentro de la fila 8 y C49 su principal. Valen las reglas
   F1 existentes: V-F1a, V-F1b, V-F1m, `F1-M-SIM`, A1/A2.
3. **Operativos (D-US2: se cuentan los pagos).** La reinversión que calibra f no lleva ninguna partida del arrendamiento operativo:

   | Dónde está el tramo | Qué hace la capa |
   |---|---|
   | amortización del derecho de uso **dentro de la fila 8** | la excluye de D_X con A1/A2 (se declara su importe); con A0 bloquea (`F1-US-DA`) |
   | amortización o variación del pasivo **dentro de la fila 14** | retira su importe del circulante que usa la reinversión, en f y en el ancla de S2C. Un solo tramo: la línea publicada. Los dos: la línea neta publicada o, si no la hay, `pagos − coste lineal` |
   | **fuera de las filas 8 y 14** | nada |
   | **no publicada** | hipótesis D-US1: como si estuviera fuera; conclusión **condicionada** y cota (`F1-US-HIPOTESIS`) |
   | sin declarar | bloquea · `pendiente_de_datos` (`F1-US-DESGLOSE`) |

4. **Perímetros.** `D_X(A1) = D&A − ROU dentro de la fila 8` y `D_X(A2) = … − PPA`; «ROU dentro de la fila 8» es la de los financieros más
   la de los operativos que estén dentro de la fila 8. A0 no cambia.
5. **C49 solo lleva principal de arrendamientos financieros** (`F1-US-C49`): si supera el principal publicado, los pagos operativos se
   restan dos veces; si no lo alcanza, el principal se omite. Con US GAAP no hay intereses pagados «en financiación» (`F1-US-MEZCLA`).
6. **Puente de deuda (motor B).** El pasivo por arrendamiento **operativo** no es deuda del puente: su pago ya está entero en el EBIT que
   proyecta el motor B. Deuda coherente = deuda financiera (fila 22) + pasivo por arrendamientos financieros. El libro resta
   `Historia C64 = fila 22 + fila 23`: si la fila 23 lleva pasivo operativo, `F1-US-PUENTE` **bloquea** con el motor B e informa con el A
   (que no resta deuda). Con el motor B y US GAAP, F1 se exige solo para esto (gancho del pipeline, vigencia y cierre).
7. **K3.** K3a (caja base por dos vías) no depende de la norma. K3b cuenta el alquiler por clase. Operativos: 1 (EBIT y CFO) + 1 si C49
   lleva sus pagos + 1 si su amortización queda en D_X o sola en el circulante − 1 si la variación de su pasivo queda sola en el
   circulante. Financieros: como NIIF. Cada clase que exista tiene que dar exactamente uno. K3c no cambia.
8. **Las ubicaciones declaradas se contrastan con el expediente** (`F1-US-FILAS`): si una línea que la fase 1 sumó en la fila 14 o en la
   fila 8 (`fase1_partes/*.json`) nombra un arrendamiento o un derecho de uso y la declaración dice que no hay nada allí, bloquea.

## 4. Qué se declara (en `motor_a_f1.json`, además de lo de NIIF)

```json
"norma_contable": {"valor": "US_GAAP", "registro": {"fecha": "…", "persona": "…", "motivo": "…"}},
"arrendamientos_us_gaap": {
  "registro": {"fecha": "…", "persona": "…", "motivo": "…"},
  "operativos":  {"existen": true, "documento": "…", "pagina": 0, "cita": "…",
                  "amortizacion_rou": {"ubicacion": "no_publicada", "documento": "…", "pagina": 0},
                  "variacion_pasivo": {"ubicacion": "fila_14", "documento": "…", "pagina": 0, "cita": "…"}},
  "financieros": {"existen": false, "documento": "…", "pagina": 0, "cita": "…"}
}
```

`ubicacion`: `fila_8` (solo la amortización), `fila_14`, `fuera_de_las_filas_8_y_14` o `no_publicada`. Cada clasificación lleva documento,
página y una cita literal (≥ 10 caracteres) que se busca en esa página de una fuente del expediente con su huella (`fuentes_series`).
`no_publicada` lleva el documento y la página del estado de flujos examinado: tiene que existir y no mostrar una línea propia del
arrendamiento operativo.

Series (formato de `da_rou`: `valor_fuente` con su signo, `signo`, `tratamiento`, `documento`, `pagina`, `literal`, `fila`):

| Serie | Qué es | Cuándo se exige |
|---|---|---|
| `pagos_arr_operativo` | caja pagada por arrendamientos operativos dentro del flujo de explotación (nota de arrendamientos) | operativos: ventana de f |
| `coste_arr_operativo` | coste lineal del arrendamiento operativo | operativos: ventana (D-US2: la diferencia, a la vista) |
| `da_rou_operativo` | amortización del derecho de uso operativo **dentro de la fila 8** | ubicación `fila_8`: ventana (y H–L para el ancla) |
| `circulante_arr_operativo` | importe del arrendamiento operativo **dentro de la fila 14**, con el signo de esa fila (+ consume caja) | un tramo en la fila 14: ventana y H–L; los dos: opcional (si falta, pagos − coste) |
| `pasivo_arr_operativo` | pasivo por arrendamiento operativo **dentro de la fila 23**, último ejercicio | motor B: obligatorio; motor A: si falta, avisa |
| `da_rou` | amortización del derecho de uso de los **financieros** dentro de la fila 8 | financieros: ventana (y H–L) |
| `pagos_arr_financiero_principal` | principal pagado de los financieros (financiación) | financieros: ventana |

Sin arrendamientos de una clase (`existen: false`, con su evidencia) no se declaran sus series. Los identificadores de los perímetros
no cambian: con US GAAP, `EBIT_NIIF16_PPA_constante` designa el EBIT publicado (con el coste lineal del arrendamiento operativo, la
amortización del derecho de uso financiero y la PPA dentro).

## 5. Qué bloquea

| Id | Salta cuando | Efecto |
|---|---|---|
| `F1-NORMA` | norma sin declarar o fuera de la lista; `L4` vacío o no reconocido; declaración ≠ libro (mezcla de normas) | BLOQUEA |
| `F1-US-MEZCLA` | declaración NIIF con claves o series de US GAAP; US GAAP con intereses pagados en financiación (C48 o fila 16 > 0) | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DESGLOSE` | falta `arrendamientos_us_gaap`, su registro, la existencia de una clase, una ubicación, su evidencia o una serie exigida; declaraciones incoherentes entre sí | BLOQUEA · INCOMPLETO o DATOS INVÁLIDOS |
| `F1-US-C49` | C49 distinto del principal financiero publicado (± 0,005), o C49 > 0 sin financieros | BLOQUEA · DATOS INVÁLIDOS |
| `F1-US-DA` | amortización del derecho de uso operativo dentro de la D&A con A0, o sola dentro del circulante sin su importe: dos veces | BLOQUEA · MODELO NO APLICABLE |
| `F1-US-SIM` | la simétrica: variación del pasivo sola dentro del circulante sin su importe, o amortización excluida de D_X sin pagos en el CFO: omitido | BLOQUEA · FUERA DEL DOMINIO |
| `F1-US-FILAS` | la declaración contradice las líneas que la fase 1 sumó en las filas 8 y 14 | BLOQUEA · DATOS INVÁLIDOS (sin `fase1_partes`, informa) |
| `F1-US-PUENTE` | la fila 23 lleva pasivo por arrendamiento operativo | BLOQUEA con el motor B · INFORMA con el A |
| `F1-K3b` | alguna clase no se cuenta exactamente una vez | BLOQUEA |
| `F1-LIBRO` | además: hay que retirar del circulante un importe distinto de cero, que ningún libro retira (§7) | BLOQUEA · límite declarado |
| `F1-SERIES` | además: series de US GAAP, citas de las clasificaciones y página de un «no_publicada» | BLOQUEA si nada más bloquea |
| `F1-US-HIPOTESIS` | se aplica D-US1: conclusión condicionada, con su cota | AVISO (no bloquea) |
| `F1-US-BASE` | informa: se cuentan los pagos; coste lineal − pagos | INFORMA |

Cota de D-US1 (`condicionada.cota`): si la variación del pasivo estuviera sola dentro de la fila 14, el flujo sin crecimiento bajaría
**como máximo** en los pagos medios a la escala del año base; si la amortización estuviera dentro de la fila 8 o sola en la 14, subiría
como máximo en el coste lineal. Se da en mm, en % del flujo y, con palancas, en % del valor presente de los flujos por escenario.

## 6. Norma → tratamiento → prueba

Baterías: **U** = `personaje_v2/pruebas/test_motor_a_f1_usgaap.py` (sin LibreOffice); **L** = `f1_usgaap/scripts/probar_libro_v631_usgaap.py`
(libro V6.3.1 real, LibreOffice); **PU** = `f1_usgaap/scripts/prueba_pipeline_usgaap.py` (pipeline de extremo a extremo, LibreOffice).
Empresa de referencia: ventas 1.000; EBIT 68 tras un alquiler operativo de 12; CFO 88; capex = D&A propia = 20; FCF base 68.

| Norma y caso | Tratamiento | Prueba | Resultado |
|---|---|---|---|
| NIIF 16 | sin cambio: A1/A2 excluyen `da_rou`; C49 lleva el principal | batería F1 existente (163), regresión de Elis (39), U «NIIF» | iguales (§8) |
| US GAAP · solo operativos, tramos fuera de las filas | nada: A0 y A2 dan la caja (68); una vez | U1 | utilizable |
| US GAAP · operativos + financieros | financieros como NIIF 16: A2 da 62 = FCF base; A0, 57 y V-F1a | U2, L3 | utilizable con A2 (libro V6.3.1) |
| US GAAP · D&A con derecho de uso operativo dentro | A0 bloquea (`F1-US-DA`; daría 58); A2 lo excluye (68) | U3, L1, L2 | utilizable con A2 |
| US GAAP · C49 con pagos operativos | `F1-US-C49`; K3b «operativos: dos veces» (FCF base 56) | U4, PU4 | `pendiente_de_datos` |
| US GAAP · desglose ausente | `F1-US-DESGLOSE` | U5, PU3 | `pendiente_de_datos` |
| US GAAP · variación del pasivo sola en la fila 14 | la capa la retira (68; tal cual, 78); sin importe, `F1-US-SIM` | U6, L5, PU2 | la capa calcula; el libro no → `F1-LIBRO` |
| US GAAP · los dos tramos netos en la fila 14 | se retira pagos − coste lineal; con pagos = coste, nada | U7, D | utilizable si pagos = coste; si no, `F1-LIBRO` |
| US GAAP · tramos no publicados | D-US1: fuera de las filas; condicionada, con cota | H, L4, PU1, F | utilizable y condicionada (libro V6.3.1 tal cual) |
| US GAAP · coste lineal ≠ pagos | D-US2: se cuentan los pagos; diferencia a la vista | D, PU1 | no bloquea |
| Mezcla de normas | `F1-NORMA`, `F1-US-MEZCLA` | N | `pendiente_de_datos` |
| Motor B con US GAAP | puente sin el pasivo operativo; `F1-US-PUENTE` | P, L6, EX | bloquea si la fila 23 lo lleva |

## 7. Qué calcula el libro V6.3.1 tal cual y qué no

**Hecho** (L1, L3, L4, PU1): el libro V6.3.1 F1 sin tocar calcula, con la capa como oráculo (f a 10⁻¹², ancla a 10⁻⁹, 33 flujos):
- tramos **no publicados** (D-US1) o **fuera de las filas**: el caso habitual. PU1 llega a `concluido`, condicionado;
- amortización operativa **dentro de la fila 8**, con o sin financieros: la fila 86 lleva la suma y A2 la excluye.

**Límite declarado** (`F1-LIBRO`; U6, D, L5, PU2): ningún libro retira nada del circulante. No se pueden concluir:
- la **variación del pasivo sola dentro de la fila 14** (frecuente cuando el estado de flujos trae «Operating lease liabilities» entre las
  variaciones del circulante y la amortización en una línea aparte);
- la amortización sola dentro de la fila 14;
- **los dos tramos netos dentro de la fila 14 cuando pagos ≠ coste lineal**: D-US2 manda contar los pagos, y eso exige retirar la diferencia.

Salida: corregir la fila 14 con una corrección registrada de las entradas en un expediente nuevo (la fila 14 sin esas líneas; entonces los
tramos quedan «fuera de las filas»). ***Propuesta:*** una plantilla hermana de la V6.3.1 con una fila para el ajuste del circulante y otra
para el pasivo operativo del puente, con su referencia y su selección propias. No se ha construido: la V6.3.1 no se puede cambiar porque
`plantilla_activa.json` de los expedientes en curso fija sus huellas.

**Puente (motor B):** ningún libro excluye el pasivo operativo de `Historia C64`. Salida: que la fila 23 lleve solo el pasivo por
arrendamientos financieros (corrección registrada). El coste de la deuda (C63), los pesos de la r operativa, el capital invertido y el ROIC
histórico (filas 32–33, C54–C55) también usan la fila 23: no se ajustan.

## 8. Pruebas ejecutadas (hechos; resultados literales)

LibreOffice siempre con `flock /home/user/e_work/libreoffice.lock`, una ejecución detrás de otra. Salidas en `resultados/`.

| Orden | Resultado literal |
|---|---|
| `cd personaje_v2 && python3 -B pruebas/test_motor_a_f1_usgaap.py` (nueva; sin LibreOffice) | `121/121 pruebas del motor A F1 con US GAAP PASAN` |
| `python3 -I …/f1_usgaap/scripts/mutaciones_usgaap.py` (38 líneas de la capa cambiadas a propósito) | `38 de 38 mutaciones detectadas` (`resultados/mutaciones_usgaap.txt`) |
| `flock … python3 -B …/f1_usgaap/scripts/prueba_pipeline_usgaap.py` (nueva; pipeline con la V6.3.1) | `11/11 pruebas de F1 · US GAAP en el pipeline PASAN` |
| `flock … python3 -I …/f1_usgaap/scripts/probar_libro_v631_usgaap.py <carpeta nueva>` (nueva; libro V6.3.1 real) | `13/13 comprobaciones de F1 · US GAAP sobre el libro V6.3.1 PASAN` |
| **NIIF no cambia:** `python3 -B pruebas/test_motor_a_f1.py` | `163/163 pruebas del motor A F1 (4.15) PASAN` (161 sin tocar; las 2 «US», que afirmaban el límite, reescritas) |
| `python3 -B pruebas/test_v631_f1.py` | `28/28 pruebas V6.3.1 F1 (sin LibreOffice) PASAN` |
| `python3 -I v6/v631_f1/scripts/probar_v631_f1.py estructura` | `21/21 comprobaciones V6.3.1 F1 (estructura) PASAN` (plantilla reconstruida `eaece01a…`) |
| `flock … probar_v631_f1.py a0 <carpeta>` | `22/22 comprobaciones V6.3.1 F1 (a0) PASAN` |
| `flock … probar_v631_f1.py f1 <carpeta>` | `35/35 comprobaciones V6.3.1 F1 (f1) PASAN` (Elis A1/A2 = E9) |
| `python3 -I …/f1_impl/scripts/regresion_elis_f1.py <copia>` | `39/39 PASAN`; los tres resultados F1 de Elis, idénticos a los de antes del cambio salvo versión, fecha y rutas (`resultados/regresion_elis_f1_tras_usgaap.md`) |
| `flock … prueba_pipeline_f1.py` (gancho; P3 reescrita: mezcla de normas) | `7/7 pruebas del gancho F1 del pipeline PASAN` |
| `flock … prueba_pipeline_v631.py` | `9/9 pruebas de la V6.3.1 F1 en el pipeline PASAN` |

**Hecho que no es de esta reparación:** en la base (`1694f08`) la regresión de Elis no se ejecutaba: llama a `motor_a_f1.py` con `python3 -I` y,
desde la V6.3.1, la capa importa módulos hermanos que así no se encontraban. Corregido con una línea (`sys.path`); con ella y antes de
cualquier otro cambio daba `39/39 PASAN`, y esa ejecución es la referencia de la comparación.

Las tres pruebas nuevas están registradas en `verificar_paquete.sh completa` (mínimos 121, 11 y 13). Las salidas de `regresion_elis_f1.py`,
`probar_v631_f1.py` y las pruebas del pipeline de F1-IMPL y de la V6.3.1 no se han vuelto a escribir en sus carpetas (son registros de sus
entregas): las de esta reparación están en `f1_usgaap/resultados/`.

## 9. Interpretaciones del autor y límites para el revisor

*Interpretaciones* (no vienen literalmente de una decisión):
1. Con los dos tramos dentro de la fila 14 y sin línea neta publicada, lo que se retira es `pagos − coste lineal` (identidad de ASC 842
   entre dos cifras publicadas). Consecuencia de D-US2 leída de forma estricta: con pagos ≠ coste el libro no lo calcula (§7). Si la persona
   prefiere dejar en ese caso lo publicado (coste lineal) con la diferencia a la vista, es una línea de `leer_us`.
2. A0 con amortización operativa dentro de la fila 8 bloquea siempre, aunque la variación del pasivo esté en la fila 14 (lo publicado
   compensaría los dos tramos y contaría el coste lineal; D-US2 cuenta los pagos).
3. `F1-US-MEZCLA` con C48 o fila 16 positivos: con US GAAP los intereses pagados no van en financiación.
4. Con el motor B y US GAAP, F1 pasa a exigirse (solo el puente). Con el motor A, un libro US GAAP exige F1 siempre.
5. La cota de D-US1 usa los pagos y el coste lineal como máximos (la parte que reduce el pasivo y la amortización son menores).
6. `coste_arr_operativo` es obligatorio (para que la diferencia de D-US2 quede a la vista); con el motor A la falta de
   `pasivo_arr_operativo` solo avisa; tolerancia de `F1-US-C49`: 0,005.
7. La lista cerrada de `L4` incluye las dos variantes NIIF que ya existían en los libros (Elis y Viscofan).

Límites:
1. Las series y clasificaciones de US GAAP no están en el libro: quedan fuera del universo de `verificacion_entradas.py`. `F1-SERIES`
   es una condición mínima (cifra con su signo y cita en su página; sin revisor ni sello).
2. Una ubicación «fuera de las filas» declarada con una cita real pero falsa en su sentido no la detecta la capa, salvo que
   `fase1_partes` muestre la línea (`F1-US-FILAS`). Una línea mixta que no nombra el arrendamiento escapa a ese contraste.
3. El contraste de «no_publicada» con la página es por texto, con patrones en inglés.
4. No se tratan: ventas con arrendamiento posterior, incentivos, deterioros del derecho de uso, ni ventanas con ejercicios anteriores a
   ASC 842 (antes de 2019).
5. Con la plantilla V6.4.1 (motor B, perímetro «NIIF 16»), las altas de derechos de uso operativos no deberían entrar con US GAAP: no hay
   guarda.
6. Con el motor B, F1 solo mira el puente. El ancla de S2C (`Historia C53`) y el ROIC histórico que usa su fase B pueden llevar partidas
   del arrendamiento operativo (filas 8, 14 y 23): no se evalúan. El motor B cuenta el alquiler por su coste lineal (va en el EBIT; no
   tiene f): D-US2 no se le aplica.
7. Todo el recálculo es LibreOffice; Excel real, sin probar. El recorrido de extremo a extremo con el motor B no se ha ejecutado (el gancho
   se prueba ejecutándolo directamente).
