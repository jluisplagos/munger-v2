# Viscofan · correcciones de entradas financieras en la extracción (rama 4.14)

**Autor:** agente corrector C-Viscofan (Claude, 14-nov-2026). No es una revisión humana ni el revisor independiente.
**Revisión que manda:** `trabajo_4_14/agentes/R_viscofan/INFORME_REVISION.md`, §3 (R-Viscofan), y el bloque `comprobacion` de `verificacion_entradas.json`.
**Rama:** esta carpeta, copia del expediente cerrado de la 4.13. El original congelado (`…/2026-11_Vidrala_ensayo_4_13/viscofan/Viscofan`) no se ha tocado.
**Scripts:** `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/C_viscofan/c_*.py`.

El documento separa tres cosas: **hechos** (con su archivo), **interpretaciones** y **propuestas**. No adopta ninguna decisión.

---

## 0. Resumen

**Hechos**

1. Las 17 discrepancias de dato confirmadas (Historia filas 13, 14, 22 y 25; Análisis C47–C50) tienen su valor correcto documentado (§2). Cada valor lleva documento, página y cita literal, y se comprobó en la página.
2. Se corrigió la salida del extractor en `fase1_partes/AR_2020.json`, `AR_2021.json`, `AR_2024.json` y `AR_2025.json`. Antes de tocarlos se guardó una copia `AR_<año>.antes_4_14.json`.
   - Con estos cambios, la regla de consolidación de `construir` daría el valor correcto en **10 de las 13** celdas de Historia con discrepancia: F25, J25, K25, L25, F14, G14, J14, K14, L14 y G13.
   - Quedan fuera **G25, H25 y D22**: el texto de la edición que cita la fase 1 no se conserva (§3).
3. **`construir` no puede ejecutarse en este expediente.** Termina con código 1 por defectos previos, ajenos a esta corrección (§4):
   - seis textos `AR_<año>.txt` no se conservan;
   - ocho ceros de 2017, 2019 y 2020 son anteriores a la reparación H1 y no llevan cita.

   Por tanto, `fase1_v63.json` **no cambia** (sha256 `62ef829a…`, el mismo que antes) y ningún valor del libro cambia en esta ronda.
4. Análisis C47–C50: `fase1_v63.json` (sección `analisis`) **ya trae** los valores exactos 77.533, 8.294, 5.547 y 3.707, con su fuente. El libro conserva 77.5, 8.3, 5.5 y 3.71 porque son celdas escritas por el inversor en la etapa 1 y `rellenar_fase1_v63.py` no las pisa sin `--sobrescribir`. Así consta en `Viscofan_v63_datos.xlsx.fase1.registro.json`, «no_pisadas».
5. En el registro se reclasificaron los ceros inferidos C23 y D23 (como `no_aplicable`) e I26 (como `derivado` por cuadre, con 8 «aux:» nuevos). Su resultado es «pendiente» para el revisor. A las 17 discrepancias se les añadió `correccion_4_14` y una frase en `incidencia`. Como sus valores en el libro no cambian, conservan el veredicto «discrepancia».

**Interpretación.** La corrección de dato está hecha y documentada en la extracción. Para que llegue al libro hace falta una decisión sobre cómo reconstruir `fase1_v63.json` (propuestas en §8). Mientras no se tome, el expediente sigue bloqueado por esas discrepancias: `apto_por_entradas = False`.

---

## 1. Cómo se construyó este expediente (hechos)

- `fase1_v63.json` lo generó `fase1_historia.py construir` en el expediente de origen (`empresas_v2/Viscofan`, 4-nov-2026). Su Historia y la de aquel `historia_revision.md` coinciden partida por partida. Se usaron los textos `AR_2016.txt`–`AR_2025.txt`, que hoy no se conservan.
  - En la 4.12 se recuperaron doce publicaciones (`CONTRASTE_VISCOFAN_4_12.md` §1). Cinco tienen la misma paginación que la fuente que cita la fase 1 (2017, 2019, 2020, 2024 —como `CF_2024.txt`— y 2025). Las otras son otras ediciones: 2016, 2018, 2021, 2022 y 2023.
  - En la 4.12 y la 4.13 solo cambiaron los metadatos de `fase1_v63.json` (precio, acciones, capitalización, C42, `control_maestro_textos`). La Historia no cambió.
- La rama no contiene `historia_revision.md`. `estado_pipeline.json` de la 4.13 no registra ningún `construir`.
- `pipeline.py` (líneas 552–568) solo llama a `construir` si **falta** `fase1_v63.json`. Si existe, pasa directamente a `rellenar_fase1_v63.py`, sin `--sobrescribir`.
- `rellenar_fase1_v63.py` escribe la Historia (C5:L26) desde `fase1_v63.json`. Las celdas de datos de Análisis las escribe solo si están vacías, si se pasa `--sobrescribir` o si están en `FRESCAS` (C37, C41, C55, C57 y C42).

---

## 2. Tabla de correcciones

Unidad: mm EUR. «Ext.» indica si el valor correcto queda en la salida del extractor (`fase1_partes`) que usaría `construir`. «Libro» indica si llega al libro en esta ronda.

Las citas son la línea del texto conservado, con los espacios normalizados como hace `fase1_historia.norm`. Los documentos están en `texto/`.

### 2.1 Pensiones (fila 25): prestación definida neta, no la línea del balance

La línea del balance «Non-current provisions for employee benefits» suma «Other employee benefits / Other staff remuneration» (incentivo a largo plazo y otras retribuciones), que no son pensiones. La fila pide el déficit neto de prestación definida.

| Celda | Antes | Después | Documento y página | Cita literal | Motivo (revisión) | Ext. | Libro |
|---|---|---|---|---|---|---|---|
| F25 (2019) | 33,294 | **29,995** | AR_2020.txt [PDF PAGE 61], nota 14, col. 2019 | «Defined benefit 28,204 29,995» | §3, F25 | sí (`AR_2020.json`, anterior) | no |
| G25 (2020) | 37,871 | **28,204** | AR_2020.txt [PDF PAGE 61], col. 2020; también CF_2021.txt [PDF PAGE 49] | «Defined benefit 28,204 29,995» · «Defined benefit 24,779 28,204» | §3, G25 | **no** (ver §3) | no |
| H25 (2021) | 29,133 | **24,779** | CF_2022_compilacion.txt [PDF PAGE 61], nota 14, col. 2021; también CF_2021.txt [PDF PAGE 49] | «Defined benefit 16,278 24,779» | §3, H25 | **no** (ver §3) | no |
| J25 (2023) | 25,916 | **17,266** | CF_2024.txt [PDF PAGE 67], nota 13, col. 2023 | «Defined benefit 16,498 17,266» | §3, J25 | sí (`AR_2024.json`, anterior) | no |
| K25 (2024) | 19,145 | **16,498** | AR_2025.txt [PDF PAGE 87], nota 13, col. 2024 | «Defined benefit 14,878 16,498» | §3, K25 | sí (`AR_2025.json`, anterior) | no |
| L25 (2025) | 20,989 | **14,878** | AR_2025.txt [PDF PAGE 87], nota 13, col. 2025 | «Defined benefit 14,878 16,498» | §3, L25 | sí (`AR_2025.json`, actual) | no |

Comprobaciones propias:
- **AR_2025 [PDF PAGE 88]**: «Net liability as at December 31 14,878 16,498» = obligaciones (Alemania 12,818; EE. UU. 18,845; otros 2,048) − activos de los planes de EE. UU. (18,833). Confirma que 14,878 es el pasivo **neto** de prestación definida.
- La «net obligation corresponding to pension plans … 14,096 … 14,400» de CF_2024 [PDF PAGE 67] es solo la de Alemania. El extractor original la había citado en la nota de `AR_2024.json`.

**Homogeneidad (C25, D25, E25 e I25 con el mismo criterio).** Las cuatro ya son la prestación definida y no se tocan:

| Celda | Valor | Fuente |
|---|---|---|
| C25 (2016) | 19,733 | AR_2017.txt [PDF PAGE 73]: «Defined benefit 17.1 18,361 19,733». Sin activos afectos |
| D25 (2017) | 18,361 | Misma línea de AR_2017 [PDF PAGE 73]. Construir usa AR_2018 p. 79 («Prestación definida 17.1 18.012 18.361»). En IA_2018_es.txt, otra edición, figura la misma línea |
| E25 (2018) | 18,012 | AR_2019.txt [PDF PAGE 76]: «Defined benefit 18.1 29,995 18,012»; [PDF PAGE 78]: «Obligation at December 31, … 29,995 18,012», neta de activos (−24,818 en 2019, 0 en 2018) |
| I25 (2022) | 16,278 | CA_2023_es.txt [PDF PAGE 45]: «Defined benefit 17,266 16,278»; CF_2022_compilacion.txt [PDF PAGE 61]: «Defined benefit 16,278 24,779» |

Con las correcciones aplicadas, la serie quedaría entera en «Defined benefit» neto.

### 2.2 Circulante (fila 14): sin la variación de provisiones

Circulante = −(existencias + deudores + acreedores) del estado de flujos. Es el criterio de 2016–2018 y 2021–2022 y el del subtotal de la empresa: AR_2019.txt [PDF PAGE 12], «Changes in working capital 6,135 (48,180)». La variación de provisiones no forma parte del circulante.

| Celda | Antes | Después | Documento y página | Cita literal (las tres líneas) | Motivo | Ext. | Libro |
|---|---|---|---|---|---|---|---|
| F14 (2019) | −12,134 | **−6,135** | AR_2020.txt [PDF PAGE 8], col. 2019 (subtotal en AR_2019 [PDF PAGE 12]) | «Adjustment for decrease (increase) of inventories -20.965 15.023» · «… of receivables -15.602 -6.919» · «… of payables 11.389 -1.969» | §3, F14 | sí (`AR_2020.json`, anterior) | no |
| G14 (2020) | 19,349 | **25,178** | CF_2021.txt [PDF PAGE 8], col. 2020 (mismas cifras en AR_2020 [PDF PAGE 8], col. 2020) | «Adjustment for decrease (increase) of inventories −17,593 −20,965» · «… of receivables −7,660 −15,602» · «… of payables 43,547 11,389» | §3, G14 | sí (`AR_2021.json`, anterior; solo se quitó un componente, ver nota) | no |
| J14 (2023) | 83,032 | **90,646** | CF_2024.txt [PDF PAGE 9], col. 2023 | «Adjustment for inventory write-down (increase) 35,919 -66,607» · «Adjustment for decrease (increase) in accounts receivable -41,828 -5,314» · «Adjustment for (decrease) increases in accounts payable -2,639 -18,725» | §3, J14 | sí (`AR_2024.json`, anterior) | no |
| K14 (2024) | 15,452 | **8,862** | AR_2025.txt [PDF PAGE 27], col. 2024 (reexpresado) | «Adjustment for reduction (increase) in inventories -709 35,919» · «Adjustment for reduction (increase) in accounts receivable -24,319 -41,828» · «Adjustment for (reduction) increases in accounts payable -24,905 -2,953» | §3, K14 | sí (`AR_2025.json`, anterior) | no |
| L14 (2025) | 53,222 | **49,933** | AR_2025.txt [PDF PAGE 27], col. 2025 | las mismas tres líneas, primera columna | §3, L14 | sí (`AR_2025.json`, actual) | no |

Notas:
- **G14.** `AR_2021.txt` no se conserva. En `AR_2021.json` solo se **quitó** el componente «Changes in provisions» (−795 / 5,829) y no se añadió ninguna lectura. Las tres líneas que quedan son las del extractor original. Sus cifras coinciden con CF_2021 [PDF PAGE 8], que es otra edición.
- **K14.** `AR_2024.json` (actual) da ahora 8,548 con el acreedores original (−2,639). `construir` usa el comparativo de 2025, reexpresado (−2,953), y da 8,862, la cifra del revisor.
- **H14 e I14** (2021 y 2022) ya estaban sin provisiones: −18,294 y 106,103.

### 2.3 Deuda 2017 (D22)

| Celda | Antes | Después | Documento y página | Cita literal | Motivo | Ext. | Libro |
|---|---|---|---|---|---|---|---|
| D22 (2017) | 82,794 | **93,698** | AR_2017.txt [PDF PAGE 83], nota 19, «Carrying amount» 2017; igual en IA_2018_es.txt [PDF PAGE 104] | «Total at December 31, 2017 10,028 9,358 64,619 9,717 93,722 93,722» − «Derivative financial instruments 3 20 1 - 24 24» = 93,698 = 68,832 + 228 + 190 + «Other financial liabilities 7,363 5,429 8,617 3,039 24,448 24,448» | §3, D22 | **no** (ver §3) | no |

`AR_2017.json` (actual) **ya da 93,698**. El valor erróneo viene del comparativo de `AR_2018.json`, que solo suma COFIDES y CDTI de los «Otros pasivos financieros». Ese texto no se conserva.

### 2.4 Adquisiciones 2020 (G13)

| Celda | Antes | Después | Documento y página | Cita literal | Motivo | Ext. | Libro |
|---|---|---|---|---|---|---|---|
| G13 (2020) | vacía (desconocido) | **0** (impreso «-») | AR_2020.txt [PDF PAGE 8], col. 2020 | «Acquisition of subsidiaries, net of cash acquired 2.1 - -1.544» | §3, G13 y §6 (ubicación fiable: AR_2020 p. 8, no CF_2021 p. 8, cuyos rótulos están desplazados) | sí (`AR_2020.json`, actual: componente impreso «-») | no |

Se registra como **componente impreso** «-», que `fase1_historia.numero` convierte en 0. No se registra como `cero` inferido, que la reparación H1 dejaría pendiente. `AR_2021.json` no trae comparativo de adquisiciones, así que `construir` usaría esta cifra. Total de inversión: −53.576 = −55.320 + 605 + 1.139.

### 2.5 Medias de Análisis (C47–C50)

| Celda | Libro | Valor exacto | Cálculo con los orígenes verificados | Vía | Libro |
|---|---|---|---|---|---|
| C47 | 77.5 | **77.533** | (77.126 + 75.027 + 80.447) / 3, Historia J12:L12 | `fase1_v63.json` analisis.C47 = 77.533; ya estaba | no |
| C48 | 8.3 | **8.294** | (6.275 + 9.726 + 8.881) / 3, J16:L16 | analisis.C48 = 8.294 | no |
| C49 | 5.5 | **5.547** | (5.296 + 5.843 + 5.503) / 3, J17:L17 | analisis.C49 = 5.547 | no |
| C50 | 3.71 | **3.707** | (2.346 + 2.001 + 6.775) / 3, J18:L18 | analisis.C50 = 3.707 | no |

La fuente que declara la sección `analisis` es «Historia de fase1_v63.json, media 2023–2025 de …». Los orígenes de Historia los verificó el revisor (CF_2024 p. 9; AR_2025 pp. 27–28).

No hacía falta cambiar nada en `fase1_v63.json`. Lo que impide que llegue al libro es la regla de no pisar de `rellenar_fase1_v63.py`: las cifras redondeadas son las del inversor en la etapa 1, Control maestro J «AR2025; IF_1S26», M «Decisión del inversor (23-oct-2026)…».

---

## 3. Lo que no se corrigió y por qué (hechos)

| Celda o grupo | Por qué no | Qué haría falta |
|---|---|---|
| **G25, H25** | `construir` toma el comparativo de `AR_2021.json` (G25) y de `AR_2022.json` (H25). Sus textos (`AR_2021.txt`, `AR_2022.txt`) no se conservan, y escribir la línea «Defined benefit …» con su página exige leerla en esa edición. Hacerlo desde otra edición (CF_2021 p. 49, CF_2022 p. 61) sería inventar la línea y la página de un texto que nadie ha visto. `AR_2020.json` (actual) sí lleva ya 28,204 | Reextraer 2021 y 2022 sobre las ediciones conservadas, o una decisión humana (§8) |
| **D22** | Ídem con `AR_2018.json` (comparativo 2017): `AR_2018.txt` no se conserva. `AR_2017.json` ya trae 93,698. Anular el comparativo para forzar que se use esa cifra alteraría la regla «cifra más reciente publicada», así que no se hace | Ídem (2018) |
| **Historia en el libro** (todas las celdas de §2.1–2.4) | `construir` termina con código 1 (§4), así que `fase1_v63.json` no cambia | §8, P1 |
| **C47–C50 en el libro** | `rellenar_fase1_v63.py` no pisa las celdas migradas de la etapa 1. El encargo prohíbe ejecutarlo sobre el libro, y cambiar `FRESCAS` sería cambiar el código | §8, P2 |
| **Análisis!C55 (acciones) y C41 (capitalización)** | Dependen de la decisión D3 (VISCOFAN-ACCIONES), pendiente. No se tocan | — |

Valores de C55 y C41:
- **C55**, actual: 45,479209 millones. Es la media ponderada «diluida» de 2025 (AR_2025 p. 119), inferior a la básica (45,656226).
- **C55**, alternativa señalada por el revisor: **45,993399** millones en circulación a 31-dic-2025 (46.500.000 acciones, p. 76, − 506.601 propias, p. 83).
- **C41**, actual: 2.487,7 (54,70 × 45,479209 = 2.487,713). Con 45,993399 sería 2.515,84.

---

## 4. Resultado de `comprobar-anio` y `construir` (hechos)

Archivo: `C_viscofan/c_comprobar_anio_despues.txt`. Con los mismos errores antes y después de la corrección:

| Año | Resultado | Causa |
|---|---|---|
| 2016, 2018, 2021, 2022, 2023, 2024 | **error** | «"archivo" ausente o inexistente en texto/: 'AR_<año>.txt'» |
| 2017 | **error** | Ceros sin «cita» en arrendamientos_principal, sbc y arrendamientos. Son anteriores a la reparación H1 del 8-nov |
| 2019 | **error** | Ídem, más minoritarios |
| 2020 | **error** | Cero de minoritarios sin «cita». Los componentes nuevos (pensiones p. 61, adquisiciones p. 8) y los de circulante pasan: no aparece ningún error suyo |
| 2025 | **OK** | — |

Ninguno de esos errores lo introduce la corrección. Cada componente nuevo o conservado de las partidas tocadas se comprobó además con las reglas de `comprobar_anio`: línea normalizada en su página e importe completo en la línea y en la página.
- AR_2020 y AR_2025 se comprobaron contra su texto.
- AR_2024 se comprobó contra `CF_2024.txt`, que tiene la misma paginación.
- Resultado: OK en todos (`c_partes_registro.json`).
- AR_2021 no es comprobable porque su texto no se conserva. Solo se quitó un componente.

`construir`, ejecutado sobre una **copia** de la rama (`C_viscofan/copia_construir/`, para no dejar en la rama un `historia_revision.md` de «SALIDAS INVÁLIDAS»):
- devuelve código 1 con los 14 problemas anteriores (`c_construir_salida.txt`);
- no escribe `fase1_v63.json` (sha256 sin cambio).

Prueba informativa, solo en la copia: con `archivo = "CF_2024.txt"` en `AR_2024.json`, `comprobar-anio 2024` da **OK**.

Simulación de la regla de consolidación sin las comprobaciones de página (`c_simulacion.txt`): con las partes corregidas cambiarían F25, J25, K25, L25, F14, G14, J14, K14, L14 y G13, a los valores de §2. G25, H25 y D22 seguirían igual.

---

## 5. Registro de verificación (`verificacion_entradas.json`)

Copia previa: `C_viscofan/registro_antes_4_14.json`. sha256 antes `f57e5711…`, después `93dcd84a…`.

**Ceros inferidos reclasificados.** El valor del libro sigue siendo 0. El bloque anterior se conserva en `comprobacion_anterior`. El nuevo lleva extractor = C-Viscofan, revisor vacío, resultado «pendiente» y la nota «corregido en la rama 4.14; pendiente de nueva revisión independiente».

| Celda | Antes | Después |
|---|---|---|
| C23 (2016) | `cero_comprobado` (el control lo marcaba como discrepancia: «la cita no contiene 0») | `no_aplicable`, con justificación: NIIF 16 no vigente; AR_2017 p. 21 y p. 11; el arrendamiento NIC 17 (342) está en C22. La fuente anterior pasa a `evidencia_no_aplicable` |
| D23 (2017) | ídem | `no_aplicable`: IA_2018 p. 37 y p. 27; el arrendamiento NIC 17 (190) está en D22 |
| I26 (2022) | ídem | `derivado` por cuadre: `o[PN] − (capital + prima + otras reservas + acciones propias + resultado + dividendo a cuenta + ajustes por cambio de valor)` = 906,870 − 906,870 = 0, con 8 «aux:CA2023_p3_…_2022» nuevos (`dato_publicado`, CA_2023_es.txt [PDF PAGE 3], columna 2022, cita literal de cada fila, p. ej. «Patrimonio Neto 957.772 906.870») |

Los 8 «aux:» nuevos tienen resultado «pendiente». Se comprobó en una copia desechable que, si el revisor los diera por verificados, C23, D23, I26 y los 8 «aux:» pasarían el contrato sin errores. No se ha aflojado ningún control: el comprobador no se ha modificado.

**Discrepancias confirmadas** (F25, G25, H25, J25, K25, L25, F14, G14, J14, K14, L14, D22, G13, C47, C48, C49 y C50):
- **Se conserva:** su valor en el libro no cambia en esta ronda, así que no se cumple la condición del encargo («cuyo valor del modelo cambie»). Por eso se mantienen `fuente`, `derivacion`, `valor_modelo` y el veredicto «discrepancia» del revisor.
- **Se añade:**
  - `correccion_4_14`: valor corregido, fuente del valor corregido, estado (corregido o no en la extracción) y `aplicado_al_libro: false`;
  - una frase «(4.14) Valor corregido: …» en `incidencia`.
- **Interpretación:** marcarlas «pendiente» con el valor erróneo todavía en el libro habría presentado como «por revisar» un error ya confirmado.

**Comprobador** (`verificacion_entradas.py comprobar --json`; `c_comprobador_antes.json` / `c_comprobador_despues.json`):

| | Antes | Después |
|---|---|---|
| universo / auxiliares | 232 / 102 | 232 / 110 |
| discrepancias | 21 | 18 (salen C23, D23 e I26) |
| pendientes | 1 (C41) | 12 (C41; C23, D23 e I26; los 8 «aux:») |
| errores, desactualizadas, sin entrada, sobrantes, repetidas | 0 | 0 |
| materiales sin comprobar | 22 | 22 |
| apto_por_entradas | False | False |

---

## 6. Efecto esperado cuando las correcciones lleguen al libro (interpretación)

El efecto es cualitativo. Las cifras son las estimaciones lineales del revisor, sin recalcular. El recálculo lo hará el pipeline.

- **L25**: entra en el puente del motor B (Historia!C65 = MAX(0;L25) + L26). Al bajar 6,111 mm, el valor por acción **sube** ≈ +0,13 € (44,22 → ≈ 44,36, según el revisor). Es la única corrección de Historia con efecto directo en el valor del motor elegido, y es corregible por la vía de extracción (AR_2025, `comprobar-anio 2025` OK).
- **F25–K25**: solo historia.
- **J14, K14 y L14**: entran en la ventana 2023–2025 y 2021–2025. Afectan al motor A (no elegido) y a la reinversión histórica: Historia!C76 baja ≈ −0,755 mm/año; S2C 2021–2025 pasa de 1,146 a ≈ 1,155. Sin efecto directo en el valor del motor B.
- **F14 y G14**: fuera de esas ventanas.
- **D22**: solo capital invertido y ROIC de 2017.
- **G13**: efecto nulo (el libro usa N(G13); la base de P-M1 suma H13:L13). Cambia el estado: vacío pasa a cero impreso.
- **C47–C50**: neto +0,071 mm de FCF base, solo en el motor A. Inmaterial.
- **C55/C41** (D3, no se corrigen): con 45,993399 millones de acciones, el revisor estima ≈ 43,73 € (−1,1 %), y ≈ 43,86 € con L25 corregida.

---

## 7. Archivos tocados

| Archivo | sha256 (después) | Copia previa |
|---|---|---|
| `fase1_partes/AR_2020.json` | `cee08bee…` | `AR_2020.antes_4_14.json` (`9bcb90af…`) |
| `fase1_partes/AR_2021.json` | `cc16faa4…` | `AR_2021.antes_4_14.json` (`3eb7a782…`) |
| `fase1_partes/AR_2024.json` | `1845874b…` | `AR_2024.antes_4_14.json` (`f6901f3c…`) |
| `fase1_partes/AR_2025.json` | `77c8a26a…` | `AR_2025.antes_4_14.json` (`234d68df…`) |
| `verificacion_entradas.json` | `93dcd84a…` | `C_viscofan/registro_antes_4_14.json` (`f57e5711…`) |
| `CORRECCIONES_ENTRADAS_4_14.md` | este documento | — |

Cada AR modificado lleva:
- `correcciones_4_14` en la raíz (autor, motivo, copia previa, partidas);
- una `nota` en cada partida tocada que empieza por «(4.14, corrección C-Viscofan…)» y conserva la nota anterior del extractor.

No se han tocado:
- `fase1_v63.json`;
- `fase1_decisiones.json`, que no existe;
- los libros `.xlsx`;
- las hipótesis, las convenciones ni la configuración;
- los scripts;
- el expediente congelado de la 4.13.

No se ha ejecutado LibreOffice, ni el pipeline, ni `rellenar_fase1_v63.py`.

---

## 8. Propuestas (para que decida una persona; ninguna está adoptada)

- **P1 · Llevar la Historia corregida a `fase1_v63.json`.** Opciones, de más a menos trazable:
  - (a) Reextraer con un agente los años cuyos textos no se conservan, sobre las ediciones conservadas, con `archivo` = nombre real y citas en los ceros. Esto permitiría ejecutar `construir` con normalidad y corregiría también G25, H25 y D22.
    - 2024: basta con `archivo = CF_2024.txt` (probado: OK).
    - 2016: `IA_2016_es`.
    - 2018: `IA_2018_es`.
    - 2021: `CF_2021` o `IA_2021_es`.
    - 2022: `CF_2022_compilacion`.
    - 2023: `CA_2023_es` o `IA_2023_es`.
    - 2017, 2019 y 2020: añadir las citas de sus ceros.

    Hay que contar con que `construir` regeneraría `fase1_v63.json` desde `fase1_metadatos.json`. Copia `analisis` (con C42), pero no `control_maestro_textos`, que sí está en `fase1_metadatos.json` y que `construir` no traslada. Ese texto de la 4.13 se perdería. Habría que comprobarlo antes.
  - (b) Autorizar, de forma expresa y trazada, la edición de la sección `historia` de `fase1_v63.json` con los 13 valores de §2. No pasa por `construir`, así que no es la vía de extracción.
  - (c) `fase1_decisiones.json` (solo lo escribe una persona) no basta por sí solo: `construir` se detiene antes por los errores de §4.
- **P2 · C47–C50.** Decidir si las medias exactas sustituyen a las redondeadas de la etapa 1. Las vías son dos:
  - regenerar con `rellenar_fase1_v63.py --sobrescribir`, que pisaría también otras celdas migradas, como B4, y recalcularía C24, C26, C28 y C33;
  - un cambio de código: añadirlas a `FRESCAS`.

  El efecto es inmaterial (§6).
- **P3 · E23 y H26** (fuera del encargo). El revisor también los califica de ceros inferidos (§5 del informe). E23 pasa el control automático. H26 lo pasa con una cita que es un movimiento («Transactions with non-controlling interests 0»), no el saldo. Convendría reclasificarlos como C23, D23 e I26 para que el control no los dé por buenos por dígitos ajenos.
- **P4 · Revisión independiente.** C23, D23, I26 y los 8 «aux:» nuevos, y cuando se regenere el libro las 17 celdas de §2, necesitan una nueva revisión independiente del extractor, que examine las páginas citadas.
