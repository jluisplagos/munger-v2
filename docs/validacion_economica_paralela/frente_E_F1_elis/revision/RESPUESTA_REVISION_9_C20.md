# Novena parte · respuesta a la revisión n.º 9 del verificador (C20) · U1–U6

Fecha: 16-nov-2026.

- **Revisión:** [REVISION_INDEPENDIENTE_9.md](REVISION_INDEPENDIENTE_9.md) (`a3a1a2b`, sobre el congelado C19 `06ad100`).
- **Encargo:** `ENCARGO_C20_CSV.md` de la revisión F1 v3 (`f5775dc`, repositorio auxiliar), primera parte.
- **Base:** `d519eb0`.
- **Esta respuesta:** el commit que la contiene.

**Alcance.** Solo cambia el verificador en lo que señalan U1–U6, sin tocar las tolerancias ni las políticas. Las 752 filas reales dan la misma salida byte a byte. No se añade ninguna fila al CSV: eso es el bloque siguiente («cifras [LECTURA]»).

## Respuesta

| | Corrección | Dónde | Prueba |
|---|---|---|---|
| **U1** | La posición de cada token sale de la tokenización: `tokens_con_posicion`, adaptada de `spans_9.py` del revisor. `spans_numericos` ya no busca el texto en la línea. Así se corrigen los tres usos de C18: `token_del_rotulo`, la condición «a la derecha del rótulo» y `columnas_de_datos`, además de la asignación por columnas anterior | `verificar_cifras.py` | U1a: ejercicio OK, sin el motivo del «día». U1b y U1d: FALLO. U2a: FALLO. U2b: OK. Comprobación directa de la posición del «0» |
| **U2** | **Se decide y se declara la primera opción de la revisión:** los recuentos con fecha cuyo rótulo es la fecha toman el ejercicio de su fecha, que es el correcto, como ya decía C16, y no quedan OK por la unidad y la columna. Las entradas de sumario también la toman y no quedan OK. El código no cambia; cambian las frases | T14, informe §1, octava parte, `ESTADO.md` | U3b en el test: ejercicio OK, fila PENDIENTE. U3a–U3d de los contraejemplos, sin cambio |
| **U3** | **Límite declarado:** «una sola columna de datos» se cuenta en los tokens de la fila, no en las columnas de la tabla. Ningún caso real en las cinco publicaciones (revisión, §4.3) | T14, informe §1 (límites) | — |
| **U4** | Mismo criterio que `rotulo`: el dígito suelto es la pestaña si la línea solo lo lleva o si le sigue una celda de texto. Si le siguen cifras, es una fila de cifras sin rótulo | `rotulos_sin_rotulo` | Comprobaciones directas: «5 · 3» entre rótulos recibe rótulo contiguo; «3 · Report…» no |
| **U5 a** | Con «published», «publié» o «reported» en el rótulo de la fila, la edición no puede ser la vigente: FALLO en edición | `verificar_fila` | U3e: sigue en FALLO de edición. Las 752 filas, sin cambio |
| **U5 c** | El pie de página no es una fila: su folio y su año quedan PENDIENTE. El «1» de «As at January 1» y los años entre paréntesis del rótulo no son cifras | `es_pie_de_pagina`, `token_del_rotulo` | U4a, el folio impar, pasa de OK a PENDIENTE. U4c, «January 1», pasa de OK a PENDIENTE. Comprobación directa del pie |
| **U5 b y d** | **Declarados:** la búsqueda de la cabecera por países salta siempre la línea de una sola celda justo encima de una fila de datos, que es el lado prudente; y el límite de T2 vale para cualquier rótulo hecho solo de las palabras admitidas («Restated», «Net», «Published») | T14, informe §1 | — |
| **U6** | Frases ajustadas | Véase abajo | — |

**U6, frase por frase:**
- **(a)** E9: R42 de 2023–25 sí interviene. Son 18 identidades, y la lista de 2023–25 lleva ahora R42. La conclusión no cambia.
- **(b)** Octava parte, informe §1, T14 y `ESTADO.md`: precisión de U2.
- **(c)** La primera versión del rótulo más corto devolvía la regla a **33 líneas**, no a siete saldos. Eran los siete saldos, el saldo «published» y 25 filas de recuentos.
- **(d)** De los cuatro años que quedaban OK, tres estaban alineados con la columna del ejercicio anterior. El «2021» del URD 2022 p.323 pasaba como cifra de 2022.
- **(e)** Informe §1:
  - la exclusión de la fila bajo la línea que continúa el rótulo exige que esa línea empiece en minúscula;
  - las entradas de sumario sí toman la regla;
  - los límites de C18 y de C20 se añaden a «Límites que quedan».
- **(f)** T14: el límite de T2 no es solo «Balance» o «Solde».
- **(g)** Son cinco tablas del WACC, una por publicación, con seis líneas de cabecera.

## Pruebas ejecutadas

Desde `scripts/`, sobre el árbol `munger_v2_r1` materializado (base 4.14 y binarios del hito 4.15).

| Comando | Resultado | Salida |
|---|---|---|
| `verificar_cifras.py --raiz … --datos ../datos/cifras_fuente.csv --fuentes ../datos/fuentes.json` | Código 2, por las 14 PENDIENTE de siempre. 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO. **Salida idéntica byte a byte** a la guardada | `resultados/verificacion_cifras.json`, sin cambios |
| `test_verificar_cifras.py --raiz …` | Código 0. **143/143 casos** (136 y 7 nuevos de la revisión n.º 9) y **13/13 comprobaciones directas** (9 y 4 nuevas) | `resultados/test_verificar_cifras.log` |
| `contraejemplos_9.py` del revisor, con C18 (`06ad100`) frente a C20 | Código 0. U1a, U1b, U1d, U2a, U2b, U4a y U4c cambian como propone la revisión. U3a–U3e y U5a–U5c, sin cambio | `resultados/revisor9_contraejemplos_9_sobre_C20.txt` |
| `barrido_fecha_rotulo.py --anterior` C18 | 207 líneas, las mismas 207 con el mismo ejercicio que en C18 | `resultados/barrido_fecha_rotulo.txt` |
| `sondas_metadatos.py` | 713/713 en unidad y en perímetro; sonda externa 1/1 | `resultados/sondas_metadatos_C20.json` |

**No se han repetido**, porque su entrada no cambia:
- el contraste y sus tests, que consumen la misma verificación byte a byte;
- la mutación;
- los scripts de los revisores n.º 1 a 8;
- LibreOffice.

## Pendiente

- **Contraste externo de C20**, solo lo afectado: el revisor asignado está en el control común.
- **Siguiente bloque:** pasar al CSV verificado las cifras [LECTURA], con este verificador.
