# ELIS · informe del revisor independiente (verificación de entradas, 4.14)

Revisor: revisor independiente R-Elis (Claude, contexto separado del extractor; no es una revisión humana). Fecha: 14-nov-2026.
Expediente: motor A (Munger V2, entrega 4.14), `…/2026-11_Vidrala_ensayo_4_14/elis_motor_A/Elis/`.

## Qué se ha tocado

- `verificacion_entradas.antes_revision.json`: copia previa del registro. Su sha256 (`15c5a380…e43e9b`) coincide con el que da el informe del extractor.
- `verificacion_entradas.json`: solo se han rellenado `comprobacion.revisor`, `fecha`, `resultado`, `fuente_examinada` y `nota` de las 328 entradas.
  - Un script ha comparado el registro con la copia previa: ningún otro campo ha cambiado.
  - El campo `extractor` se conserva.
  - sha256 nuevo: `f6b551b7…5379a`.
- Scripts del revisor: `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/R_elis/r_*.py`. Se han ejecutado con `python3 -B`.
  - No se ha ejecutado LibreOffice ni el pipeline.
  - El libro solo se ha leído con openpyxl.
- **Caché encontrada, no creada por este revisor:** existe `personaje_v2/scripts/__pycache__/`.
  - Sus archivos tienen fecha de 14:52:12–14:52:16. La primera ejecución del comprobador por este revisor fue hacia las 14:56, con `-B`.
  - No se ha borrado porque no es de este revisor; probablemente es de otro agente que trabaja en el directorio compartido. Conviene que el responsable lo compruebe.

Orden de trabajo: el informe del extractor se ha leído al final. Las conclusiones de abajo coinciden con las suyas y añaden las estimaciones de C55/C41 y las observaciones de las secciones 3 y 4.

## 1. Recuento

| Resultado | Entradas |
|---|---|
| verificado | 322 |
| discrepancia | 6: C55, C41, I25, J25, K25, L25 |
| pendiente | 0 |
| **Total** | **328**: 193 celdas del universo y 135 «aux:» |

Por clase revisada:

| Clase | Entradas |
|---|---|
| dato_publicado | 244 |
| derivado | 46 |
| cero_comprobado | 3 |
| no_aplicable | 4 |
| hipótesis | 21 |
| convención | 10 |

Método:
- **Datos publicados:** un script ha mostrado, para cada uno, la línea de la página citada y la cabecera de columnas. Este revisor ha juzgado entrada a entrada:
  - la fila;
  - la columna, con su año y si está reexpresada;
  - la unidad, el signo y el perímetro;
  - que el concepto sea el que pide el `uso` o la etiqueta de la fila del libro.
- **Derivados:** todas las fórmulas se han recalculado desde sus orígenes.
- **PDF renderizados** a 110 ppp y examinados, en las páginas cuya columna depende de la alineación o que soportan las discrepancias:
  - DR 2018, p. 169;
  - URD 2021, p. 228 (balance con tres columnas);
  - DEU 2024, p. 259 y p. 312;
  - URD 2025, p. 314, 355, 366 y 395.
- **Precio:** transcripción y las dos capturas de la fila del 4-nov-2026. Las huellas sha256 se han recalculado y coinciden con `HUELLAS.txt`.

## 2. Discrepancias

### 2.1 C55 (acciones): de concepto, material

**Hecho:** la cifra está bien extraída. Es la fila «Weighted average number of shares used for diluted EPS 259,077,654», columna 2025, URD 2025 PDF p. 395 (folio 393).
- 233.954.020 acciones básicas medias.
- 23.355.764 por la conversión de bonos convertibles.
- 1.767.869 contingentes.

**Discrepancia:** el `uso` pide las acciones vigentes en la fecha de valoración (4-nov-2026), «no la media del ejercicio».

**Hechos posteriores**, que están en el expediente (`fuentes_2026`):
- **A 30-jun-2026:** 232.848.588 acciones emitidas y 16.914.214 en autocartera, compradas en la recompra. En circulación: 215,93 M (H1-2026, PDF p. 14 y p. 46).
- **9-jul-2026:** termina el programa de recompra de 500 mm.
- **7-oct-2026:** se convierte el 99,13 % de las OCEANE.
  - Se entregan 23.569.556 acciones: 18.104.556 de autocartera y 5.465.000 nuevas.
  - El capital queda en **238.313.588** acciones.
  - Los 33 bonos restantes se amortizan en efectivo: 3,3 mm el 13-oct-2026.

**Valor correcto (estimación del revisor):**
- Unos **238,2 M** de acciones en circulación a 4-nov-2026: las 238.313.588 menos una autocartera residual pequeña que el expediente no publica. La cota superior es 238,31 M.
- Entre 239 y 240 M si se quiere la cifra diluida con las acciones de rendimiento contingentes (0,8–1,8 M).
- La cifra exacta exige la «Disclosure of the number of shares … as of 31 10 2026», publicada el 12-nov-2026. El expediente solo guarda su título, en `Elis_comunicados_Euronext.html`.

**Efecto estimado:**
- C55 sobra unos 20,8 M de acciones (+8,8 %).
- Con todo lo demás igual, el valor por acción del motor A subiría alrededor de un 8,8 % (× 259,08 / 238,2).

**Interpretación:** no basta con cambiar C55.
- La base de 2025 no recoge los ~500 mm de la recompra: más deuda o menos caja, y más intereses.
- Tampoco recoge que la OCEANE y su cupón han desaparecido.
- Mientras C55 incluya las 23,36 M de la conversión y la OCEANE siga como deuda (L22, motor B) o su cupón siga en C48 (motor A), hay doble cómputo.
- La decisión E6 sigue pendiente.

### 2.2 C41 (capitalización): de concepto, heredada de C55

- La fórmula se reproduce: 24,18 × 259,077654 = 6.264,498. El libro guarda 6.264,5 (+0,002 de redondeo).
- En la fecha de valoración saldría unos **5.760 mm** (5.762,4 con la cota superior), alrededor de un 8 % menos.
- Contraste: el URD 2025 p. 447 da 5.648,9 mm a 31-dic-2025.

### 2.3 Pensiones I25:L25: de concepto

- El libro usa la línea «(5) = (3) + (4)», que suma las «Other long-term benefits» al déficit neto de prestación definida.
- La fila 25 del libro pide «Posición neta (obligación − activos del plan)», es decir, la línea (3).

| Celda | Libro (5) | Correcto (3) | Ubicación | Diferencia | Efecto |
|---|---|---|---|---|---|
| I25 (2022) | 50,7 | **47,4** | URD 2023, PDF p. 307, columna 12/31/2022 | 3,3 | histórico |
| J25 (2023) | 78,3 | **74,9** | DEU 2024, PDF p. 301, columna 31/12/2023 | 3,4 | histórico |
| K25 (2024) | 104,1 | **91,6** | URD 2025, PDF p. 355, columna 12/31/2024 | 12,5 | histórico |
| L25 (2025) | 79,7 | **67,1** | URD 2025, PDF p. 355 (renderizada), columna 12/31/2025 | 12,6 | solo motor B |

- En L25, la línea (3) es la obligación 414,4 menos los activos 347,3.
- **Efecto en el motor B:** 12,6 mm más de patrimonio, unos 0,05 € por acción.
- **Efecto en el motor A:** ninguno directo.

## 3. Lo que el comprobador marca y este revisor no

El comprobador marca **C46, C47 y C50** como discrepancias porque la fórmula exacta no coincide con el valor redondeado del libro:

| Celda | Libro | Media exacta | Diferencia |
|---|---|---|---|
| C46 | 1.429,4 | 1.429,433 | −0,033 |
| C47 | 857,1 | 857,167 | −0,067 |
| C50 | 28,2 | 28,233 | −0,033 |

- En C47, con las líneas del estado de flujos la media es 857,133.
- Este revisor las da por **verificadas**: las fuentes, los conceptos y los orígenes son correctos, y la diferencia total sobre el FCF base es de unos 0,13 mm (0,04 %).
- C46 y C50 son el redondeo correcto a un decimal. C47 no lo es exactamente: la media de los «Net capex» redondearía a 857,2.
- Para que el comprobador las acepte, el libro tendría que guardar los valores sin redondear o el registro tendría que declarar el redondeo. Decide quien mantiene el libro.

## 4. Observaciones (no son discrepancias con la fuente)

- **Lino frente a NIIF 16:**
  - **C49 y la fila 23** son solo pasivos y principal NIIF 16: inmuebles, vehículos e instalaciones que Elis arrienda. Comprobado en las conciliaciones renderizadas: DEU 2024 p. 312 y URD 2025 p. 366.
  - **El lino y los equipos propios alquilados** a clientes son inmovilizado material. Su compra está en el capex (fila 12, C47) y su amortización en D&A.
  - **D&A (fila 8)** es el total de la nota 4.5. Desde 2019 incluye la amortización de los derechos de uso. En 2025: lino propio 565,1; derechos de uso 149,5; intangibles de combinaciones 85,7.
- **C47 es capex NETO**, elegido por el inversor. La Historia, fila 12, es bruta: la media 2023–2025 sería 867,167. Son unos 10 mm al año menos de inversión en el FCF base. Es una elección del inversor, no un error.
- **C48 = 108,0** se reproduce exactamente: 82,933 de intereses netos más 25,067 de intereses de arrendamientos implícitos. Incluye previsiblemente el cupón de la OCEANE (~8,6 mm al año, ~2,8 % del FCF base), que se suma al doble cómputo de C55.
- **Fila 15 (intereses), serie no homogénea:**
  - 2019–2022 incluye los intereses de arrendamientos.
  - 2023–2025 los excluye.
  - L15 = 99,4. Serían 129,0 si «total» se leyera con los 29,6 de intereses de arrendamientos.
- **L22** incluye la OCEANE: 362,0 (364,4 con intereses). Es correcto a 31-dic-2025, pero la OCEANE se convirtió o se amortizó antes del precio.
- **Pensiones 2016–2021 (C25:H25):** son la línea (3), el concepto correcto.
  - El URD 2022 imprimió 50,7 como (3) para 2022, y el URD 2023 lo reexpresa como (5) = 47,4 + 3,3.
  - Por tanto, hasta 2021 la línea (3) podría englobar otros beneficios a largo plazo no separados (~3 mm). Es solo referencia histórica.
- **Precio (C37):**
  - Las capturas añadidas a las 15:00 sí muestran la fila del 4-nov-2026 resaltada, con CLOSE 24,18. La frase del registro que dice lo contrario está superada.
  - El filtro Non-Adjusted solo consta declarado.
- **Hipótesis y convenciones (31):** ninguna es un dato publicado disfrazado. Las cifras de apoyo que este revisor ha contrastado cuadran: caja 398,1; deuda a menos de un año 800,5; deuda más arrendamientos 4.121,5.
  - C23 (recuperación) cita unas pensiones de 79,7; el concepto correcto da 67,1.
  - C47 (causa de desviación) = «Ninguna»: es coherente por construcción, porque C41 = C37 × C55. La causa real está en C55.
- **Ceros:**
  - K26 y L26: «0.0» impreso en el balance.
  - El «aux» de beneficios a empleados de 2016: «(0.0)» impreso.
  - C23:E23 son no_aplicable, no cero: NIIF 16 adoptada el 1-ene-2019 sin reexpresar (URD 2019 p. 200).

## 5. Resultado del comprobador (`verificacion_entradas.py comprobar … --json`, rc = 1)

| Campo | Resultado |
|---|---|
| Universo | 193 celdas + 135 auxiliares |
| Comprobadas | 319 |
| Pendientes | 1 (C41, porque su origen C55 está en discrepancia) |
| Discrepancias | 8 (C55, C46, C47, C50, I25, J25, K25, L25) |
| Desactualizadas | 0 |
| Errores del contrato | 0 |
| Sin entrada, sobrantes o repetidas | 0 |
| Materiales no comprobadas | 9 |
| **apto_por_entradas** | **False** |

## 6. Límites de esta revisión

- Se ha trabajado sobre el texto extraído de cada página citada. Se han renderizado y mirado 8 páginas de PDF, no todas.
- En las demás, la columna se ha juzgado por la cabecera y por el orden «actual / anterior» de la línea. Todas las líneas tienen las dos cifras, y en los balances con tres columnas o con columna de notas se ha contado la posición.
- No se ha contrastado ninguna cifra con fuentes externas al expediente.
- No se ha verificado el número exacto de acciones a 4-nov-2026: no está en el expediente.
- `Elis_OCEANE_2029_ajuste_ratio.html` figura en `HUELLAS_descarga_persona_responsable.txt` pero no existe en la carpeta.
- No se juzga el acierto de las hipótesis, solo que no sean datos publicados disfrazados.
- Las citas de apoyo de las hipótesis (Control maestro, columna N) no se han contrastado una a una.
- Esta revisión es de un agente (Claude) con contexto separado del extractor. **No es una revisión humana.**
