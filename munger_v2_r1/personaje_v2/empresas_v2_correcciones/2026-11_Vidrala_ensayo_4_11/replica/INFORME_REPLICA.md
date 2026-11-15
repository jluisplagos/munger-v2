# Informe de la réplica independiente · V6.4 experimental del motor B (encargo 4.11 §8)

12 de noviembre de 2026. Réplica escrita en contexto separado, a partir de la especificación y de los análisis fuente, sin leer las fórmulas nuevas de la plantilla.

El informe separa **hechos comprobados** (§1, §5–§9), **interpretaciones** (§4) y **propuestas** (§11).

## 1. Resultado (hechos comprobados)

- Se compararon los **107 casos** del manifiesto con sus libros recalculados. **Coinciden los 107**; el guion termina con código 0. No hay ninguna discrepancia en ningún grupo.
- 93 casos se calculan: 3 en modo heredado, 5 experimentales con R0 y 85 con R1 (88 sobre la base 4.6.1 y 5 sobre la 4.10.1). 14 se rechazan. La réplica rechaza exactamente los 14 casos que el libro no calcula.
- Diferencias máximas entre libro y réplica: 4,7e-13 €/acción en los valores, 6,8e-13 millones en los flujos y 5,0e-12 millones en la conciliación. Las tolerancias pedidas (1e-9) quedan a más de tres órdenes de magnitud.
- Esas diferencias son del orden del redondeo con que el libro guarda sus resultados: ninguno de los 160.061 valores calculados que se leyeron tiene más de 15 cifras significativas.
- La coincidencia completa se obtuvo en la primera ejecución. Los cambios posteriores del guion fueron de comparación, de informe y de validación de entradas; ninguna fórmula del modelo se ajustó para coincidir.
- Ningún valor calculado del libro entra en el cálculo de los tres escenarios: la réplica parte de Historia, Palancas, Análisis y de las celdas de entrada de «Configuración V6.4».

## 2. Qué se implementó

`scripts/replica_independiente_v64.py` (biblioteca estándar y openpyxl; no ejecuta LibreOffice):

1. **Entradas** (especificación §2): Historia C..L de las filas indicadas, Palancas, Análisis y las celdas de entrada de «Configuración V6.4».
2. **Derivados heredados**: V0, margen de partida, tipo de la Historia, deuda, coste de la deuda, puente y bases de los años H..L.
3. **Modo y validez** (§3.2–3.3): cada regla de obligatoriedad o de dominio que no se cumple produce un motivo de rechazo; con algún motivo, la réplica no calcula.
4. **Proyección** de una fila del motor B: modo heredado y R0 (reinversión ΔV ÷ S2C), R1 (máximo de ventas conservado), cartera P0, familias Λ y Θ, estructuras H, S, SR1, SR2 y SRF, convenciones de los años y del terminal, valor por acción con quiebra.
5. **Ponderado y precio de Sí** (k = 3) con un algoritmo propio.
6. **Comparaciones** de la especificación §4, más algunos añadidos que se señalan como tales en §4 y §5.

Salidas: `replica/replica_resultados.json` (por caso: rechazo, diferencias máximas por grupo, discrepancias, modelo y valores de la réplica, SHA-256 del libro) y `replica/replica_salida.txt` (legible, con el resultado global al principio y al final). La salida es determinista: dos ejecuciones sobre el mismo directorio dan archivos idénticos.

## 3. Independencia: qué se leyó y qué no

**Leído.**
- Enteros: la especificación; `analisis_n1_n3.py` (4.7.1); `analisis_reinversion_4_8_1.py` (4.8.1); `analisis_pm1.py` (4.8); `precio_de_si.py`; `casos_v64.py`.
- De la V6.3 heredada: en `v6/scripts/V6.1/build_v6.py`, la construcción de la hoja Motor, las anclas de Historia y la base del Diagnóstico; `V6.1/test_fill.py`; el tratamiento de las pensiones en `patch_v62_base.py` y `patch_v63.py`; `LEEME.txt` y `README_scripts_V6.3.md`.
- Resultados conservados de entregas anteriores, solo para un contraste lateral (§8): `matriz.json` (4.7.1), `pm1_resultados.json` (4.8) y `rf_resultados.json` (4.8.1).
- De los libros, siempre con `data_only=True`: Historia, Palancas y Análisis; Motor, columnas A..BT (filas 4–137 y 237); «Conciliación B» como valores, incluidos sus rótulos; de «Configuración V6.4», solo B4, B11:B16, B21:B23, B28:B32, B36:B51 y B8.
- Durante la exploración se leyó B8 en todos los libros (está vacío en los 93 que calculan) y, en dos libros heredados, valores de Diagnóstico V6 y de las anclas de Historia que la réplica no usa. El guion entregado solo lee B8 cuando hay un rechazo que comprobar.

**No leído.** Ningún archivo de `v6/v64_experimental/scripts/` ni de `v6/v64_experimental/referencia/`; ninguna fórmula de ningún libro; las columnas BU:DY del Motor (ni como valores); el resto de «Configuración V6.4»; tampoco `generar_libros_casos.py`, `REGISTRO_AVANCE_4_11.md` ni los demás archivos nuevos de la carpeta 4.11, que no hacían falta.

## 4. Decisiones de interpretación

Cada fila dice qué admitía dudas, cómo se resolvió con las fuentes y si los 107 libros permiten contrastarlo. Lo que ningún caso ejercita queda implementado según la lectura indicada, pero **sin contraste**.

| # | Punto | Duda | Resolución y fuente | ¿Lo contrastan los libros? |
|---|---|---|---|---|
| 1 | Precio de Sí | Si la forma cerrada ya acota en el NORMAL | No acota. `p_estrella` da P*; el tope se aplica después: `precio_si = min(P, V_normal)` en `precio_de_si.py` y `min(lo, Vs[1])` en la escalera de la 4.7.1. La réplica hace lo mismo | No: el tope no actúa en ningún caso (P* ≤ 0,94 × V NORMAL) |
| 2 | Textos de opción | Mayúsculas, espacios | Comparación exacta | Solo en B4: «experimental» se rechaza |
| 3 | Campos «no vacíos» | Celdas con solo espacios | Vacío, cadena vacía o solo espacios cuentan como falta | No: los casos solo quitan celdas |
| 4 | N3 con R0 | Circulante opcional | Con los tres números, NWC = (B29 + B30 − B31) ÷ V0, solo para la presentación; si falta alguno, 0; en modo heredado, 0 | Sí con datos (5 casos) y en heredado (3). «R0 sin datos», no |
| 5 | R1, años 1–10 | Equivalencia con `proyeccion(…, "circulante")` de la 4.7.1 | Son algebraicamente iguales: Δcirc = ΔV × NWC y fija = max(0, V − máximo) × (1 ÷ S2C − NWC) | Sí: 2.550 filas con caída y recuperación bajo el máximo; 145 con nuevo máximo |
| 6 | Terminal con R1 | Regla del máximo; base del Δcirc | Como `valorar` de la 4.8.1: sin regla del máximo y Δcirc₁₁ = V₁₀ × g × NWC | Sí |
| 7 | Crédito terminal en H | La especificación dice min(req₁₁, max(0, fija₁₁)); la 4.8.1 usa pagado = max(0, req₁₁ − fija₁₁) | Se sigue la especificación. Coinciden si fija₁₁ ≥ 0 | No: fija₁₁ ≥ 8,03 en las 1.860 filas con H |
| 8 | Condiciones de f y f_fija | Si rechazan en cualquier estructura | Solo donde se usan: f en SR1 y SR2; f_fija en SRF | No |
| 9 | Bases históricas «completas» | Qué celdas cuentan | Capex y D&A numéricos en H..L; circulante o adquisiciones vacíos valen 0 (convención heredada) | No |
| 10 | B32 y B51 (fuentes) | Si son obligatorias | La especificación no lo dice: no se exigen | No |
| 11 | Tolerancia de flujos | «Relativa 1e-9 sobre la escala de las ventas» | Diferencia ≤ 1e-9 × V0 (1,47e-6 millones). La conciliación, sin tolerancia en la especificación, usa la misma | Las diferencias reales (≤ 5,0e-12) pasarían también con 1e-9 absoluto |
| 12 | Referencia | Qué se compara | Réplica y libro, cada uno frente a la referencia, con el `tol` del caso. `tol_V` se admite, pero ningún caso lo trae | Sí: 53 casos (10 sin V) |
| 13 | «El libro no calcula» | Alcance | B78:D78 y C83 sin números, D237 = «INCOMPLETO» y, añadido, ninguna cifra en Motor AU:BK de las filas 6–136 | Sí: 14 casos |
| 14 | Dominio heredado | Si la réplica debe rechazar | r_op > g, ROIC > max(0, g) y V0, S2C y acciones > 0 (regla «Válido» del Motor V6.3) | No: todos los casos lo cumplen |
| 15 | Modo heredado con motor A o C | Alcance | Fuera de alcance: el caso contaría como no comparable | No aparece |
| 16 | Margen, tipo y puente heredados | Detalle de las medias | Anclas de la V6.3: media de los márgenes de los años con ventas; media de H10:L10; pensiones con suelo en 0 | «Media del ciclo», sí. «Último año» y superávit de pensiones, no |

## 5. Resultados por grupo

| Grupo | Casos que pasan | Comparaciones | Diferencia máxima | Dónde |
|---|---|---|---|---|
| 0 · Entradas (añadido): libro = manifiesto = `casos_v64.py` | 107 de 107 | 9.610 | — | — |
| 1 · Validez | 107 de 107 | 684 | — | — |
| 2 · Valores (Análisis B78:D78, C83; Motor BK6:BK8) | 93 de 93 | 651 | 4,7e-13 €/acción | N1_cero · Análisis!D78 |
| 2b · Parámetros de las filas 6–8 (añadido) | 93 de 93 | 4.185 | 2,8e-14 | her_461 · Motor!M6 |
| 2c · Referencia de réplicas anteriores | 53 de 53 | 417 | 7,1e-14 (50 casos, tol 1e-9); 4,5e-07 (3 casos a seis decimales, tol 1e-6) | her_461 · V BUENO |
| 3 · Flujos (Motor AU6:BD8 y BF6:BF8) | 93 de 93 | 3.069 | 6,8e-13 millones | SRF_T0.50 · Motor!AU8 |
| 4 · Conciliación (nueve partidas, tres bloques) | 93 de 93 | 27.621 | 5,0e-12 millones | her_461 · Conciliación B!G7 |
| 5 · Filas 9–136 (sensibilidad, tornado, DCF inverso) | 93 de 93 | 11.253 filas (101.463 comprobaciones) | BK: 8,8e-13 €/acción; flujos: 5,0e-12 millones | N1_cero · Motor!BK120 |
| 6 · Identidades | 93 de 93 | 5.612 | 5,3e-15 | SRF_L1.15 · Conciliación B!E48 |

Los 14 rechazos no tienen valores que comparar: solo les aplican los grupos 0 y 1.

**Validez.** En los 14 rechazos la réplica da un único motivo, que corresponde al del libro, y «Configuración V6.4»!B8 contiene el `motivo_esperado`. Los dos textos de cada caso están en `replica_salida.txt`, sección RECHAZOS. En los 93 restantes el libro calcula y V35 dice «OK».

**Filas 9–136.** Las 121 filas de cada libro calculado tienen valor en AU; en los 14 rechazados, ninguna. Añadidos al valor BK que pide la especificación:
- los once flujos de cada fila;
- que V0, m0, t, puente, quiebra y acciones de cada fila sean los del modelo activo, y que su tasa sea la r operativa activa más el desplazamiento heredado de la fila (0, ±0,01 o ±0,02).

Sin el segundo añadido, un m0 o un tipo heredados en la tabla del DCF inverso pasarían inadvertidos, porque el resto de la fila se toma del libro.

**Identidades.**
- Crédito = 0 fuera de H, también en el terminal: 78 casos, 33 celdas del libro por caso, todas exactamente 0.
- 0 ≤ crédito ≤ min(req, max(0, fija)) en H: 15 casos, en el libro y en la réplica.
- Δcirculante de SRF = el de S, fila a fila: 16 casos SRF. En 15, libro contra libro, con diferencia 0. En `piloto_SRF_L1.15_legado` no hay libro S homólogo y se comprueba con la variante S que calcula la réplica.
- Rh = 0 ⇒ SRF = S: los libros de `SRF_L1.00` y `S_L1.00` son idénticos (diferencia 0) en valores, flujos, inversión fija, requisito y Δcirculante; en la réplica, f_fija = 1 exacto.
- θ = 0 ⇒ f = 1: en `SR1_T0.00` la réplica da f = 1 exacto, y el libro es idéntico (diferencia 0) al de `P0_solo`, el mismo caso sin requisito, en valores, flujos e inversión fija.

## 6. Precio de Sí

- **Convención.** Precio de Sí = min(P*, V NORMAL), donde P* es el precio más alto con G(P) ≥ 3 × L(P). La réplica obtiene P* resolviendo G − 3L = 0 en el tramo entre valores consecutivos donde cambia de signo.
- **Contraste con las referencias.** 53 casos. En los 50 con tolerancia 1e-9, la diferencia máxima es 2,1e-14; en los 3 a seis decimales, 3,2e-07, que es el redondeo de la referencia.
- **Contraste con las dos fuentes.** Los cinco casos del autotest de `precio_de_si.py` y 200.000 ternas aleatorias, ordenadas y positivas: diferencia máxima 8,5e-14 frente a la forma cerrada y frente a la escalera de la 4.7.1. En 59.622 de ellas el tope del NORMAL actúa.
- **Fuera del dominio de los casos las dos fuentes difieren.** `precio_de_si.py` exige valores ordenados (error G19) y la bisección de la 4.7.1 no baja de 0. Con V = (−80, −10, 30) y probabilidades (0,5; 0,3; 0,2), la forma cerrada da −58,5 y la escalera, −10. La réplica calcula P* siempre y marca los valores desordenados. En los 93 casos los valores están ordenados y son positivos.
- **Sin contraste.** Los 40 casos calculados sin referencia: el libro no tiene celda para el precio de Sí.

## 7. Discrepancias

Ninguna. La sección DISCREPANCIAS de `replica_salida.txt` está vacía, y las listas `discrepancias` de `replica_resultados.json`, también.

## 8. Comprobación de que la comparación discrimina

Una coincidencia total a la primera obliga a comprobar que la comparación no es vacía. Se hicieron tres pruebas fuera del guion entregado.

**Lecturas alternativas.** Se alteró a propósito una pieza de la réplica cada vez y se contó cuántos casos dejaban de coincidir:

| Lectura alternativa | Casos que dejan de coincidir |
|---|---|
| R1: la recuperación bajo el máximo paga ΔV ÷ S2C | 85 |
| El máximo conservado incluye el año en curso | 93 (85 en el valor) |
| Terminal de R1 con la regla del máximo | 85 |
| Δcirculante terminal sobre V₁₁ en lugar de V₁₀ | 90 (27 en el valor; el resto, solo en la conciliación) |
| Cartera P0 con un año de desfase | 71 |
| Convención de los años, o del terminal, intercambiada | 73 cada una |
| Λ anual sin restar la cartera | 36 |
| Θ con el exceso sin la cartera | 38 |
| f con D_hist sin la cartera | 27 |
| Rh de Λ con la amortización total | 22 |
| F_hist sin adquisiciones | 15 |
| SR2 sin ROIC × f | 14 |
| SRF sin f_fija en el terminal; H sin crédito en el terminal | 15 cada una |
| Escudo siempre al tipo de la Historia | 86 |
| Escudo siempre vinculado | 1 (`T1_M1_R1_escudo_separado`) |
| R0 experimental con NWC = 0 en la presentación | 5 (solo en la conciliación) |
| P0 sin requisito: la cartera no entra | 2 |
| Crédito de H sin el max(0, ·); forma literal de la 4.8 en el terminal de H; precio de Sí sin tope | **0: los libros no las distinguen** (filas 1 y 7 de §4) |

**Prueba negativa.** Sobre copias de cinco libros, fuera del paquete, se alteraron siete valores guardados: un valor por acción en 2e-9 €, un flujo en 1e-5, dos créditos, un valor y un m0 de filas del DCF inverso, y un rechazo al que se le puso un valor numérico. El guion detectó las siete alteraciones, nombró cada celda con el valor del libro y el de la réplica, y terminó con código 1. También termina con código 1 si falta un libro, si el manifiesto marca un recálculo fallido o si el manifiesto no coincide con `casos_v64.py`.

**Intermedios frente a entregas anteriores.** Rh, f, f_fija y peso del terminal de las 35 alternativas de la 4.8.1, y r operativa, NWC y cartera por año de la 4.8, coinciden con los conservados (diferencia máxima 7,1e-15). Tres casos sin referencia en el manifiesto (`T1_M0_R0`, `T0_M1_R0` y `T2_M1_R1`) coinciden con la matriz de la 4.7.1 (2,8e-14).

## 9. Observaciones que no son discrepancias

- **El terminal no aplica la regla del máximo conservado.** En el MALO de la base 4.6.1 con R1, las ventas del año 11 (1.421,3) siguen por debajo del máximo conservado (1.465,2) y, aun así, el terminal carga inversión fija para crecer (16,39 millones en `H_L1.15`). Es lo que dicen la especificación y la 4.8.1, y la réplica lo reproduce. Se anota como decisión de modelo ya tomada.
- **Autocomprobación del libro.** En los 93 libros calculados, los tres bloques de «Conciliación B» dicen «✓ cuadra» y su fila de diferencia no supera 2,1e-14. La réplica no usa esas filas.

## 10. Límites de la réplica

- **Compara valores, no fórmulas.** Demuestra que el libro da los resultados correctos en estos 107 casos y en sus 11.253 filas de sensibilidad; no demuestra que las fórmulas sean correctas fuera de ellos.
- **Ramas implementadas sin contraste**, porque ningún caso las ejercita:
  - modo heredado con el resto de la hoja escrito (la regla «se ignora» no tiene caso);
  - R0 sin datos de circulante;
  - H con inversión fija terminal negativa, y cualquier fila con g ≤ 0;
  - precio de Sí con el tope del NORMAL activo, con valores desordenados o negativos;
  - probabilidad de quiebra > 0, base «Último año», superávit de pensiones, empresa sin deuda;
  - rechazos por dominio: valor neto de la cartera > 10 veces su amortización, requisito negativo, cartera mayor que la amortización, f o f_fija no definidos, N1 o N2 fuera de rango, circulante negativo, bases históricas incompletas.
- **Filas 9–136.** Crecimiento, margen objetivo, S2C, g, ROIC y el desplazamiento de la tasa se toman de la fila, como pide la especificación. La réplica no reconstruye esos parámetros desde Palancas.
- **Motivos de rechazo.** Se comprueba que el libro contiene el motivo esperado y que la réplica rechaza; la correspondencia entre el motivo de la réplica y el del libro se lee en la salida, no se verifica de forma automática.
- **Fuera de alcance.** Motores A y C; Panel, Diagnóstico y demás hojas; el crecimiento implícito de Análisis C86 (se comprueba su tabla, no la interpolación); la idoneidad económica de las entradas y de las hipótesis.
- **Recálculo.** Los libros son los recalculados con LibreOffice que se entregaron. La réplica no recalcula ni comprueba Excel.

## 11. Propuestas

Ninguna es necesaria para el resultado de §1.

1. **Añadir casos para las ramas sin contraste de §10.** Los dos más útiles: un caso en modo heredado con toda la hoja de configuración rellena, que es la garantía de que el modo heredado no cambia; y un caso con el tope del NORMAL activo en el precio de Sí.
2. **Precisar en la especificación** los puntos 3, 4, 7, 8, 9 y 10 de §4, la tolerancia de la conciliación y el uso de `tol_V`, que la especificación menciona y el manifiesto no trae.
3. **Decidir la convención del precio de Sí fuera del dominio habitual** (valores desordenados o negativos), donde `precio_de_si.py` y la escalera de la 4.7.1 no dan lo mismo.
4. **Conservar las pruebas de §8** en el paquete si se quiere repetirlas: hoy están en la carpeta temporal de la sesión, no en el paquete.

## 12. Archivos y reproducción

- Guion: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/scripts/replica_independiente_v64.py`
- Resultados: `…/2026-11_Vidrala_ensayo_4_11/replica/replica_resultados.json` y `replica_salida.txt`
- Este informe: `…/2026-11_Vidrala_ensayo_4_11/replica/INFORME_REPLICA.md`

Orden, desde la raíz del paquete:

```
python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/scripts/replica_independiente_v64.py DIR_CASOS \
    --json personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/replica/replica_resultados.json \
    --txt  personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/replica/replica_salida.txt
```

Código 0 si todos los casos coinciden; 1 si alguno no coincide o no puede compararse; 2 si el uso es incorrecto. La ejecución tarda unos 45 segundos (Python 3.13.18, openpyxl 3.1.5). El guion no escribe nada más en el paquete.

SHA-256 de esta ejecución:

| Archivo | SHA-256 |
|---|---|
| `replica_independiente_v64.py` | `50fdc3c7fab353210cacad4889eed7b5b64d0dc2a8a4cbb639c6c46a58253bf9` |
| `replica_resultados.json` | `f8484cfff998d9969c8f48ceee744ea637be466b169b0d9ef6548462c3357919` |
| `replica_salida.txt` | `cead6c2635629d3baa9bf9ef3d6b1c41815edd921e4ae9fd42b08047a8f88d28` |
| `manifiesto_casos.json` del directorio comparado | `5a3fab1316fcc833d256df64324fc59f74bae4bd856f50e4e61b8f6463a10ddb` |
