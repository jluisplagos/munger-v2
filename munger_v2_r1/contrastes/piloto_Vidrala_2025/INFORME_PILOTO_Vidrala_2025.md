# Piloto Vidrala 2025 · contraste acotado de cuatro cuestiones

**Fecha:** 8-nov-2026. **Paquete:** `munger_v2_r1`, entrega 4.1 (piloto Vidrala 2025 con las precisiones de cierre), construida sobre la entrega 3.1. **Modelo:** Opus; Fable no se ha usado (motivo en `REGISTRO_PILOTO.md`).

**Entrega 4.1.** Recoge las tres precisiones de cierre de la persona responsable:
- los resultados de arrendamientos se presentan como sensibilidad condicionada a supuestos, no como límites;
- el PDF español completo se incorpora a `fuentes/`;
- en el hallazgo del circulante se separan tres cosas: la corrección documentalmente respaldada, su aplicación (pendiente) y la revisión financiera necesaria antes de llevar una `f` negativa a conclusiones de valoración.

No cambia ningún dato, cálculo, script ni extracción.
**Alcance:** las cuatro cuestiones del encargo para la extracción `personaje_v2/empresas_v2/Vidrala/fase1_partes/AR_2025.json`, que también recoge los comparativos de 2024. No se ha modificado ningún original, no se ha regenerado ningún libro y no se ha cambiado ningún criterio.

Este informe va acompañado de:
- `DOCUMENTOS_Y_FUENTES.md`: documentos utilizados y fuentes ausentes;
- `ANEXO_REPRODUCIBLE.md`: comprobaciones, cálculos y referencias, que se reproducen con `scripts/contraste_vidrala_2025.py`;
- `CORRECCIONES_PROPUESTAS_Y_PENDIENTES.md`: correcciones propuestas, separadas de los datos.

## 0. Versión recibida

- **Hecho.** El encargo preveía `munger_v2_r1_entrega3_H1cierre_H3.zip` (SHA-256 `81a83704…26636644`). Se recibió `munger_v2_r1_entrega3.1_continuidad.zip` (SHA-256 `2e517d8e…bd2def034`, igual a su `.sha256`).
- **Hecho.** Según `REGISTRO_IMPLEMENTACION_H1-H3.md`, la 3.1 es la entrega 3 más documentación de continuidad, un ajuste de la prueba H3 y la retirada de `.lo_perfil/`. El código del sistema no cambia.
- **Hecho.** El expediente de Vidrala no figura en `CAMBIOS_ARCHIVOS.txt`, así que conserva la huella de la base, y el manifiesto lo confirmó.
- **Limitación.** El ZIP de la entrega 3 no estaba disponible, así que la diferencia se ha identificado con el registro, no byte a byte.

## 1. Resultado

| Cuestión | Resultado | ¿Alcanza el cálculo actual? |
|---|---|---|
| 4.1 CFO 2025 y 2024 | **Confirmado.** 380,287 y 362,516 mm cuadran exactamente con sus líneas. La señal «no cuadra» del JSON es una interpretación incorrecta del extractor | No |
| 4.1 (componente) circulante 2024 | **Discrepante y vigente.** El sistema usa −127,840 mm. **Corrección documentalmente respaldada:** +84,994 mm (versión española y `AR_2024.json`). **Aplicación:** pendiente (no hay decisión humana ni expediente nuevo) | **Sí, el dato vigente entra en el cálculo.** Con la corrección, la `f` del libro pasaría mecánicamente de 0,0199 a −0,0276 (fórmulas del libro). **No es una conclusión de valoración:** llevar una `f` negativa a valores exige antes una revisión financiera (§2, 4.1-c) |
| 4.2 Capex | **Confirmado.** 188,503 y 168,800 mm son compras de inmovilizado material e intangible. Los rótulos ingleses son erróneos y la versión española los corrige | No |
| 4.3 Arrendamientos | **Pendiente.** La fila 17 de la Historia guarda el pago total (principal + intereses) con el rótulo «principal», lo que es discrepante de concepto pero no llega al motor. `Análisis C49 = 4,5` es un principal aproximado (pagos − gasto devengado) que la evidencia disponible no demuestra | No determinable con la evidencia disponible. Solo hay una sensibilidad condicionada a supuestos no acreditados (§2, 4.3), que no fija límites. Los datos de 2023 que entran en la media no están contrastados |
| 4.4 Adquisiciones y desinversiones | **Confirmado.** 2025 = 0. En 2024, −241,668 mm por la venta de Vidrala Italia (230,000 + 11,668), conforme a la convención documentada | No: solo entra en el ancla visual S2C y en una condición de validez |

«Confirmado» significa que el dato y su tratamiento coinciden con la fuente. No es una aprobación de la tesis de inversión.

## 2. Por cuestión

### 4.1 CFO

- **Evidencia.** Las cuentas consolidadas de 2025 en inglés (doc. 2355), PDF p. 7, y en español (doc. 2308, prevalece), PDF p. 14. Hay dos subtotales sin rótulo claro:
  - 224.195 es la suma de los diez **ajustes**, sin el beneficio;
  - 799 («Cash used in operating activities») es el subtotal del **circulante**.

  CFO = 209.341 + 224.195 + 799 − 20.800 + 7.509 − 40.757 = **380.287**. En 2024: 298.315 + 240.195 − 84.994 − 32.100 + 11.200 − 70.100 = **362.516**. Las dos sumas coinciden con el total impreso.
- **Extracción inicial.** CFO = total impreso, con la nota «el subtotal impreso no cuadra… erratas». La nota del lector de 2024 en `fase1_v63.json` dice lo mismo.
- **Decisiones posteriores.** Ninguna.
- **Dato efectivo.** Historia L11 = 380,287 y K11 = 362,516. `Análisis C46 = 335,4`, la media de 2023 a 2025.
- **Resultado.** Confirmado. La señal del JSON era una **interpretación incorrecta de las partidas**: el extractor esperaba que el subtotal sin rótulo fuera beneficio + ajustes, y es solo la suma de los ajustes (la nota de 2024 lo deja ver al calcular «538,510 de ajustes» = 298.315 + 240.195). No es una discrepancia del documento.

**Hallazgo en un componente del CFO: circulante 2024**

- **Evidencia.** La versión inglesa imprime «Other current liabilities … 106,417)», sin el paréntesis de apertura. La española imprime «(106.417)», en negativo. Con −106.417, las cinco líneas suman −84.994, que es el subtotal impreso.
- **Extracción inicial.**
  - `AR_2025.json` copia «106,417)» sin `signo` y explica en su nota que es negativo, pero esa nota no se traslada al dato.
  - `fase1_historia.numero()` lee «106,417)» como +106.417, así que el sistema calcula un circulante de 2024 de −127,840 mm.
  - El informe de 2024 (`AR_2024.json`) daba 84,994. El sistema aplicó su regla de usar el comparativo más reciente, y `historia_revision.md` lo anotó como «revisar si la diferencia es grande».
- **Decisiones posteriores.** Ninguna en `fase1_decisiones.json`.
- **Dato efectivo.** Historia K14 = −127,84.
- **Resultado.** **Discrepante y vigente.** Es un defecto de la extracción inicial, sumado a una lectura del sistema que no detecta el signo perdido (limitación L4 declarada). No es un fallo del documento original español.
El estado del hallazgo tiene tres partes, que se mantienen separadas:

- **a) Corrección documentalmente respaldada.** El aumento del circulante de 2024 es **+84,994 mm**. Lo respaldan:
  - la versión española (D3, PDF p. 14, «(106.417)»), con la que las cinco líneas suman el subtotal impreso;
  - el informe de 2024 (`AR_2024.json`).

  Este es el único punto que el piloto da por acreditado.
- **b) Aplicación: pendiente.** El dato vigente en el expediente sigue siendo −127,84. Para cambiarlo hace falta:
  - una decisión humana en `fase1_decisiones.json` de un expediente nuevo (propuesta P1);
  - `construir`;
  - recalcular el libro.

  Nada de eso se ha hecho.
- **c) Efecto mecánico en `f` y revisión financiera pendiente.**
  - **Efecto mecánico.** La fila 14 entra en `f` («fugas al accionista», Historia C58), y el motor A, que es el activo, resta `f` de cada flujo. Con 84,994, la reinversión media 2023–2025 (C76) pasaría de 40,43 a 111,38 mm, y `f` pasaría de **+0,019890 a −0,027608**. Es aritmética de las fórmulas del libro, con todas las demás entradas sin cambios.
  - **Antes de llevarlo a conclusiones de valoración, hay que revisar:**
    - qué significa económicamente una `f` negativa en esta empresa. Con el dato corregido, el FCF base (161,2) supera al flujo operativo implícito de la ventana (NOPAT − reinversión = 119,96). La convención de la plantilla dice que un `f` negativo «no es un error», pero proyectarlo como porcentaje constante de las ventas supone que esa diferencia se mantiene y crece con el negocio;
    - la composición de la ventana 2023–2025. Los datos de 2023 no están contrastados: CFO, capex, pagos y devengado de arrendamientos que entran en C46, C47 y C49. Además, el circulante de 2023 tiene su propia diferencia sin investigar (PE5);
    - si se mantiene la elección del motor A, que en la fase A se apoyó en «f = 0,020 está en rango».
  - **Sin esa revisión,** el cambio de `f` no debe leerse como un aumento de valor. La magnitud aritmética del término (Δf × ventas ≈ 0,0475 × 1.465 ≈ 70 mm al año) describe cuánto cambiaría ese término de la fórmula, no el efecto en la valoración. Esa cifra no se ha calculado: exige regenerar el libro (sección 3).

### 4.2 Capex

- **Evidencia.** PDF p. 7 en inglés: «Payments from sale of property, plant and equipment (178,746) (160,063)» y «Payments from sale of other intangible assets», con las cifras (9,757) (8,737) en la línea siguiente. PDF p. 14 en español: «Pagos por la **adquisición** de inmovilizado material (178.746) (160.063)» y «Pagos por la adquisición de activos intangibles (9.757) (8.737)». No hay líneas de cobros por venta de inmovilizado. Las líneas de inversión suman el total impreso en los dos años.
- **Extracción inicial.** Las dos líneas, negativas, se convierten en un capex positivo: 188,503 y 168,800.
- **Decisiones posteriores.** Ninguna.
- **Dato efectivo.** Historia L12 y K12; `Análisis C47 = 169,7` (media de 2023 a 2025).
- **Resultado.** Confirmado. Los rótulos ingleses contienen un **error de traducción del documento**; el concepto (compras) y el signo (salida de caja) quedan acreditados por la versión española, que prevalece.

### 4.3 Arrendamientos

- **Evidencia.** Nota 8, PDF p. 52 en inglés y p. 58 en español:
  - el movimiento del pasivo cuadra: 44.904 + 2.404 de altas + 2.452 de **gasto financiero devengado** − 8.314 de **pagos** + 9.596 de otros − 1.742 de conversión = 49.300;
  - los pagos reducen un pasivo al que se suma el interés devengado, así que **incluyen intereses** (NIIF 16);
  - **en las dos versiones del documento**, los mismos importes 8.314 y 6.117 aparecen también como «gastos por arrendamientos a corto plazo y de poco valor»; es una discrepancia presente en el original que no se puede resolver;
  - el estado de flujos no tiene línea de arrendamientos ni de intereses en financiación;
  - la conciliación NIC 7 (p. 67) atribuye toda la variación de la deuda con arrendamientos (−130.399) a flujos y conversión, sin los 14.452 de movimientos no monetarios de la nota 8.
- **Lo que falta.** No consta ni el principal ni el interés **pagado** de los arrendamientos, ni la línea del estado de flujos donde están. Tampoco consta si «Interest paid» (explotación) incluye intereses de arrendamientos.
- **Extracción inicial.** `arrendamientos_principal` = pago total, 8,314 y 6,117, con una nota que dice que incluye intereses.
- **Decisiones posteriores.** `Análisis C49 = 4,5` procede de la herencia V5.3: «principal NIIF 16: 2025 5,9 · media 3a 4,5», es decir, pagos menos gasto devengado. La decisión del inversor del 23-oct-2026 eligió el periodo (media de 3 años), no el método.
- **Dato efectivo.**
  - Historia L17 = 8,314. Solo la usa la fila 35, informativa, y una validación.
  - `Análisis C49 = 4,5` entra en el FCF base (C52 = 161,2) y, a través de él, en `f`.
- **Resultado.** **Pendiente.** Restar el gasto devengado al pago total es justo la operación que el encargo no admite sin evidencia, y la evidencia no basta para confirmarla ni para rechazarla.
- **Efecto: no determinable. Solo hay una sensibilidad condicionada.** Cambiar C49 cambia el FCF base y `f`. Dos valores ilustran la sensibilidad, cada uno bajo supuestos que **no** están acreditados:
  - **C49 = 4,5 (valor actual).** Supone que el interés pagado por arrendamientos es igual al devengado, que ese interés está ya dentro de «Interest paid» (explotación) y que el principal se paga en financiación. FCF base 161,2; `f` 0,019890.
  - **C49 = 6,8 (media de los pagos totales).** Supone que todo el pago de arrendamientos, intereses incluidos, está fuera del CFO. FCF base 158,9; `f` 0,021430.

  Estos dos valores **no son límites** y no validan el principal ni su clasificación en el estado de flujos. Por ejemplo, si la cifra repetida de 8.314 correspondiera en realidad a un gasto de arrendamientos a corto plazo ya incluido en el CFO, ninguno de los dos supuestos se aplicaría.

  Además, las dos medias incluyen datos de 2023 **sin contrastar**: los pagos de 5,861 y el devengado de 2,131, que solo consta en una nota del lector, porque el informe de 2024 no está en el paquete (F2).

### 4.4 Adquisiciones y desinversiones

- **Evidencia.**
  - PDF p. 7 en inglés y p. 14 en español: en 2025, todas las líneas de negocios van con «-»; «Acquisition of a subsidiary» no tiene importes.
  - En 2024 hay dos cobros: «pérdida de control de dependientes» (230.000) y «Otros efectos **enajenación**» (11.668). El rótulo español confirma que este último pertenece a la venta.
  - La memoria fecha la venta de Vidrala Italia el 4-jul-2024.
  - La compra de participadas por puesta en equivalencia (6.000) está en una línea aparte.
- **Extracción inicial y dato efectivo.** Adquisiciones = −(pagos y cobros de negocios dependientes): 2025 = 0 y 2024 = −241,668 (Historia L13 y K13). La convención (`prompts/historia_anio.md`) dice «negocios/dependientes», así que la participada queda fuera.
- **Decisiones posteriores.** Ninguna.
- **Resultado.** Confirmado. La exclusión de los 6.000 es coherente con la convención; si conviene revisarla es una decisión de la persona responsable.
- **Efecto.** Ninguno en la valoración:
  - la fila 13 solo alimenta la reinversión total (fila 31) y el ancla «S2C marginal» (C53), que se muestra en Palancas F16 y no entra en ninguna fórmula del motor;
  - en `f`, solo se comprueba que la celda sea numérica.

## 3. Lo que queda pendiente y por qué

- **Circulante 2024: aplicación de la corrección.** Requiere que una persona fije el dato en `fase1_decisiones.json` de un expediente nuevo (propuesta P1) y que se ejecute `construir`. No se ha hecho.
- **Circulante 2024: revisión financiera antes de sacar conclusiones de valoración** (PE7). Tiene que cubrir:
  - el significado de una `f` negativa en esta empresa;
  - la ventana 2023–2025, con sus datos de 2023 sin contrastar;
  - si se mantiene la elección del motor A.

  Es un juicio financiero que corresponde a la persona responsable. Este piloto no lo sustituye.
- **Efecto en las valoraciones** (MALO, NORMAL y BUENO, precio de Sí y cubo). Solo tiene sentido calcularlo después de los dos puntos anteriores, y exige recalcular el libro en un expediente nuevo (PE1). No se ha hecho, porque el encargo no permite regenerar libros.
- **Principal de arrendamientos.** Hace falta evidencia del interés pagado o de la línea de financiación, o una decisión humana sobre la hipótesis (propuesta P3). También hay que contrastar los datos de 2023 (F2).
- **El `CF_2025.txt` original no está en el paquete** y ningún archivo registra su huella. La correspondencia con el PDF descargado está probada por contenido: las 61 líneas citadas aparecen carácter a carácter en sus páginas, y `comprobar-anio` solo rechaza los tres ceros heredados sin cita. Su identidad byte a byte no se puede comprobar.
