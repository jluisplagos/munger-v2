# Resolución del dividendo a cuenta y base por acción del ensayo (entrega 4.4, 9-nov-2026)

Se resuelve **antes** de tocar la caja o recalcular el libro, como pide el encargo (§2–3). Las cifras están comprobadas en `scripts/comprobar_ensayo.py`, §8.

**Categorías:**
- **[Hecho]**: está en un documento conservado.
- **[Interpretación]**: lectura razonada de los hechos.
- **[Decisión del ensayo]**: tratamiento elegido para el ensayo, con su alternativa aparte.

## 1. Hechos

**[Hecho] Comunicación de otra información relevante de Vidrala sobre el dividendo a cuenta**
- Documento 2275, conservado en `fuentes/dividendo_2275/`.
- SHA-256 `cbaff23e640718620fd43e7dfb18e9222a4c90fb34e1ce684abdc9c6dc83e25e`.
- Fechada en Llodio el 18-dic-2025.
- Contenido:

| Concepto | Valor |
|---|---|
| Acuerdo del consejo | «en su reunión celebrada el 17 de diciembre de 2025» |
| Importe | 1,2318 € brutos por acción |
| Último día con derecho (*last trading date*) | 10-feb-2026 |
| Fecha sin derecho (*ex-date*) | 11-feb-2026 |
| Fecha de registro (*record date*) | 12-feb-2026 |
| Pago | 13-feb-2026 |

**[Hecho] Cuentas consolidadas de 2025**
- **EN25 p.3:** el patrimonio a 31-dic-2025 ya está reducido por el dividendo a cuenta: «Interim dividend distributed during the year (43,338)».
- **EN25 p.70:** la obligación figura en proveedores y otras cuentas a pagar: «Dividends to shareholders (Note 15) 43,338».
- **EN25 p.67:** la conciliación NIC 7 la incluye entre los pasivos de financiación: «Dividends payables… 43,338».
- **EN25 p.64 y el ESEF en español:** la fecha del consejo es el **19-dic-2025**. El comunicado dice 17-dic. Es una discrepancia documental de fecha sin efecto en el tratamiento: las dos son anteriores al cierre.
- **[Hecho, aritmética]** 43.338.244,48 € ÷ 1,2318 = 35.182.858 acciones. Son las acciones emitidas a 31-dic-2025 (35.206.258) menos la autocartera de esa fecha (23.400; EN25 p.61). El dividendo se repartió entre las acciones en circulación.

**[Hecho] La deuda del puente del motor B no incluye el dividendo.**
- L22 + L23 = préstamos del balance (262,913).
- La caja L24 (108,352) es la caja del balance a 31-dic-2025, antes del pago.

## 2. Definiciones del ensayo

| Pregunta del encargo | Respuesta |
|---|---|
| 1. **Fecha económica del valor** | **31-dic-2025.** El motor descuenta los flujos 1–10 con exponentes enteros desde el año base (2025), y el puente usa los saldos de esa fecha (4.3.1, `ENTRADAS_Y_FECHAS.md`, §2). |
| 2. **¿Incluye el derecho al dividendo?** | **Sí: el valor es con derecho.** El 31-dic-2025 la acción cotizaba con derecho: el último día con derecho fue el 10-feb-2026. Quien tenía la acción ese día tenía también el derecho a cobrar 1,2318 €. |
| 3. **Caja, obligación y distribución** | La caja de 108,352 contiene los fondos con los que se pagará el dividendo. La obligación (43,338) es una deuda de la sociedad con **los mismos accionistas** cuyo valor se calcula, no con terceros. El valor con derecho de esa fecha es caja + negocio − deuda con terceros. La obligación con los propios accionistas no se resta, porque el dividendo forma parte de lo que reciben. Cuando se paga (13-feb-2026), la caja baja 43,3 y el accionista recibe 1,2318 €: el valor total que recibe no cambia. |
| 4. **Dónde se ajusta y cómo se evita el doble cómputo** | En la **ruta A** (este ensayo) **no se hace ningún ajuste**: L24 = 108,352 y L22 sin dividendo, tal como están. Cualquier comparación posterior con un precio sin derecho (cualquier fecha desde el 11-feb-2026, incluido el 3-nov-2026) debe restar el dividendo **una sola vez**. Hay dos formas, y no pueden combinarse: (a) como distribución al trasladar el valor de 31-dic-2025 a esa fecha; (b) usando saldos posteriores al pago. Nunca se resta en el puente de 2025 y otra vez al trasladar el valor. |

**[Decisión del ensayo]** El ensayo usa el **valor con derecho a 31-dic-2025**, sin modificar la caja ni la deuda.
- Corrige la inclinación de la 4.3.1 (P16c: «restarlo»), que trataba el dividendo como «ya repartido» en una fecha en la que no lo estaba.
- No requiere ningún cambio de datos.

**[Alternativa, por separado; no se ejecuta] Valor sin derecho a 31-dic-2025**
- Se calcularía restando 43,338 del valor del capital, es decir, tratando el dividendo a pagar como deuda.
- Solo tendría sentido para compararlo con un precio sin derecho de una fecha muy próxima.
- Si se usara, el traslado a otra fecha **no** podría volver a restar esos 43,338.
- No se propone para el ensayo: introduce una definición distinta de la de la fecha económica sin ganar coherencia.

**Dividendo complementario de 2025.**
- 16.490.205,54 € propuestos a la junta (EN25 p.65); pagados el 15-jul-2026 según la herencia, no contrastado.
- A 31-dic-2025 no estaba aprobado ni reconocido. No es una obligación del puente. En una comparación posterior, sería otra distribución que restar una sola vez.

**Base por acción.**
- El valor con derecho a 31-dic-2025 corresponde a las 35.182.858 acciones en circulación de esa fecha.
- El ensayo conserva C55 = 35,206 (acciones emitidas, autocartera incluida; +0,07 %). No se actualiza en silencio.
- La diferencia queda declarada en `REGISTRO_HIPOTESIS_ENSAYO.md`.

## 3. Ampliación liberada 1×20 de 2026

**[Hecho] Documento de la CNMV**
- Comunicación de otra información relevante de Vidrala, conservada en `fuentes/cnmv_liberada_2026/`.
- SHA-256 `3259cf30e9bb9985648c4abbd9e37c32b9cc37409cd946eaf140a17a9a93c29d`.
- Fechada en Llodio el 20-oct-2026; PDF creado el 20-oct-2026.
- Origen: URL de la CNMV indicada por la persona responsable (sección 4 de `FUENTES_Y_PROCEDENCIA.md`).

| Momento | Fecha | Fuente | Estado |
|---|---|---|---|
| Anuncio en el BORME | 28-oct-2026 | BORME 5696 (4.3.1) y CNMV, calendario | Hecho |
| Legitimados | Titulares al cierre del 28-oct-2026 (día anterior al inicio) | CNMV §4; BORME | Hecho |
| **Inicio de la negociación de derechos** | **29-oct-2026** | CNMV §12: «Inicio del periodo de negociación de los derechos de asignación gratuita» | Hecho |
| Fin de la negociación de derechos | 11-nov-2026 | CNMV §12 | Hecho |
| **Formalización** (aplicación de reservas a capital) | «una vez finalice el período de asignación gratuita» | CNMV §7 | Hecho; fecha concreta no publicada en estos documentos |
| **Registro de las acciones nuevas** en Iberclear y admisión a cotización | Posterior; sus derechos corren «desde la fecha de inscripción» | CNMV §8–9 | Fecha **ausente** |
| Acciones en circulación al ejecutar | 35.206.258 («existen en circulación»); acciones nuevas: 1.760.312 | CNMV §1 | Hecho. No informa de la autocartera |

**[Interpretación] El precio del 3-nov-2026.**
- Esa fecha cae dentro del período de negociación de derechos. La acción y el derecho cotizaban por separado.
- El precio de 87,9 es el de una acción **sin** el derecho a la acción nueva (cotización sin derecho).
- La lectura procede del calendario oficial. La CNMV no usa la expresión «fecha ex».

**[Interpretación] Base por acción para una comparación económica con ese precio (ruta B; no se ejecuta aquí):**
- acciones posteriores a la liberada, netas de autocartera, multiplicadas por el precio sin derecho;
- o, de forma equivalente, acciones anteriores a la liberada multiplicadas por (precio + valor del derecho).

**Escenarios condicionados de autocartera.** Los porcentajes de la 4.3.1 («+2,0 % a +4,9 %») **no son límites acreditados**:
- +4,93 % si en la fecha de registro no había más autocartera que las 23.400 acciones de 31-dic-2025;
- +1,96 % si había ≈1,021 millones de acciones en autocartera. Es una cifra heredada del Control maestro, no contrastada, y mayor que el programa documentado de 350.000 acciones.

La autocartera a 28-oct-2026 sigue **ausente** (E3).

**[Decisión del ensayo]** El ensayo de la ruta A no se compara con el precio. Conserva C37 = 87,9, C55 = 35,206 y C41 = 3.094,6 tal como están, como **resultados mecánicos sin lectura económica frente al precio**. No actualiza en silencio ni el precio ni las acciones.
