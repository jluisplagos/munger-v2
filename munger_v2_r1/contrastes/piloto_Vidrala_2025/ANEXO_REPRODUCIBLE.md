# Anexo reproducible · piloto Vidrala 2025

Las rutas son relativas a la raíz `munger_v2_r1/`. Los importes van en miles de euros cuando vienen del documento, y en millones (mm) cuando vienen del sistema.

## 1. Cómo se obtuvieron las fuentes (no se repite al verificar)

1. **Sin acceso desde el entorno de trabajo.** El entorno donde se trabajó no puede conectarse a vidrala.com: la conexión se rechaza con un 403 del proxy. Por eso se usó el navegador integrado de la aplicación de escritorio, vinculado a la sesión, en <https://www.vidrala.com/en/investors/results-centre/>.
2. **PDF en inglés.** Se hizo `fetch()` del D1 desde esa página y se calculó su SHA-256 con `crypto.subtle`.
3. **Traslado al entorno.** Los bytes se pasaron en base64 en tres tramos y se reconstruyeron. La huella del archivo reconstruido coincide con la del navegador.
4. **PDF en español.** El D3 (13,5 MB) se leyó igual y su huella se calculó en el navegador.
   - **Entrega 4.** Se extrajo solo el texto de las páginas 14 y 58 con pdf.js 4.0.379 (cdnjs), ordenando las piezas de cada página por posición. La huella del texto (D4) se calculó en el navegador y coincide con la del archivo guardado.
   - **Entrega 4.1.** Se trasladó el PDF completo, en 72 tramos de base64, y se reconstruyó. Su SHA-256 es `29fd6a29…698f14e7`, el mismo que en el navegador y que el de la descarga independiente de la revisión externa. Ahora está en `fuentes/es_2308_descarga_2026-11-08/`.
5. **Texto nuevo.** El D2 se generó así:

   ```
   mkdir -p X/pdf && cp D1 X/pdf/CF_2025.pdf
   python3 -I personaje_v2/scripts/pdf_a_texto.py X
   ```

   Es el conversor del proyecto (pdftotext 24.02.0, `-layout`).

## 2. Cómo se reproduce

Desde la raíz del paquete, en una descompresión limpia:

```
python3 -I contrastes/piloto_Vidrala_2025/scripts/contraste_vidrala_2025.py > /tmp/salida.txt; echo $?   # 0
diff /tmp/salida.txt contrastes/piloto_Vidrala_2025/resultados/contraste_salida.txt                     # sin diferencias
```

El script es de solo lectura y no crea `__pycache__`. Tarda un par de segundos. Hace 35 comprobaciones y debe terminar con «todas las comprobaciones esperadas se cumplen». `verificar_paquete.sh` lo ejecuta y compara su salida con la de referencia.

**`comprobar-anio` sobre una copia.** Es el procedimiento del contrato (§1). Se ejecutó así:

```
cp -r personaje_v2/empresas_v2/Vidrala /tmp/copia/ && mkdir /tmp/copia/Vidrala/texto
cp contrastes/piloto_Vidrala_2025/fuentes/texto_nuevo_CF_2025/CF_2025_EXTRACCION_NUEVA.txt /tmp/copia/Vidrala/texto/CF_2025.txt
python3 -I personaje_v2/scripts/fase1_historia.py comprobar-anio /tmp/copia/Vidrala 2025
```

- **Salida** (código 1), solo tres rechazos, todos de ceros heredados sin cita que ya están en `personaje_v2/empresas_v2_correcciones/ceros_heredados_H1.csv`:
  - `intereses_financiacion: «cero» sin «cita» literal de la página 7`
  - `otros_activos_financieros: «cero» sin «cita» literal de la página 2`
  - `minoritarios: «cero» sin «cita» literal de la página 3`
- **Clasificación según el contrato:** ninguno es de tipo A, B ni C. Son el paso 4: una persona tiene que revisar cada cero.
- **Copia intacta:** la huella de cada archivo de la copia antes y después de la ejecución es la misma.
- **Lo que no detecta:** la discrepancia del circulante de 2024 **no** la detecta `comprobar-anio`, porque «106,417)» está en su línea y en su página. Es un caso de la limitación L4 (signo).

**Contraste del extracto D4 con el PDF completo D3** (entrega 4.1; se comprueba a mano, porque el script del piloto no cambia):

```
sha256sum contrastes/piloto_Vidrala_2025/fuentes/es_2308_descarga_2026-11-08/2308_es-informacion_financiera_consolidada_2025.pdf
#   29fd6a299d37270279195e8eb194820869a1bb2c513dd6a646963034698f14e7
pdftotext -layout -f 14 -l 14 contrastes/piloto_Vidrala_2025/fuentes/es_2308_descarga_2026-11-08/*.pdf - | grep -E "Otros activos y pasivos|adquisición de inmovilizado|Otros efectos enajenación"
pdftotext -layout -f 58 -l 58 contrastes/piloto_Vidrala_2025/fuentes/es_2308_descarga_2026-11-08/*.pdf - | grep -E "Pagos|poco valor"
```

Resultado el 8-nov-2026:
- con pdftotext 24.02.0, las cifras de las páginas 14 (74 cifras) y 58 (23) son las mismas que en D4;
- las líneas clave aparecen igual: «Otros activos y pasivos corrientes y no corrientes (23.477) (106.417)», «Pagos por la adquisición de inmovilizado material (178.746) (160.063)» y «corrientes y de poco valor 8.314 6.117»;
- el extracto obtenido con pdf.js queda así confirmado con un segundo método de extracción.

## 3. Comprobaciones y cálculos auxiliares

La salida completa está en `resultados/contraste_salida.txt`. Estos son los cálculos clave.

**4.1 CFO.** D1 p. 7 y D3 p. 14.

| | 2025 | 2024 |
|---|---|---|
| Beneficio del ejercicio | 209.341 | 298.315 |
| Suma de los 10 ajustes (= subtotal impreso sin rótulo) | 224.195 | 240.195 |
| Circulante (= «Cash used in operating activities» / «Efectivo generado por las operaciones») | 799 | (84.994) |
| Intereses pagados · cobrados · impuestos pagados | (20.800) · 7.509 · (40.757) | (32.100) · 11.200 · (70.100) |
| **CFO calculado = impreso** | **380.287** | **362.516** |

- **Circulante de 2024, línea a línea:** 36.800 − 15.655 + 3.916 − **106.417** − 3.638 = −84.994. Con «+106.417», como lo lee el sistema, la suma da +127.840.
- **Comparación de las dos versiones:** el estado de flujos inglés y el español tienen las mismas cifras, con una sola excepción: «106,417)» en inglés frente a «(106.417)» en español.

**Cadena del circulante de 2024:**

| Eslabón | Contenido |
|---|---|
| `AR_2025.json` | `circulante_lineas.anterior` lleva «106,417)» sin `signo` |
| `fase1_historia.numero("106,417)")` | +106.417 |
| Serie del sistema | −(36.800 − 15.655 + 3.916 + 106.417 − 3.638)/1000 = **−127,840** |
| `historia_revision.md` | informe 2024 = 84,994 · comparativo 2025 = −127,84 → «se usa el más reciente» |
| `fase1_decisiones.json` | nada |
| `fase1_v63.json` | circulante 2024 = −127,84 |
| Libro | Historia K14 = −127,84 |

**Réplica de `f`.** Son las fórmulas de Historia C58 y C74 a C80, sobre la ventana C57 = 3 (2023–2025). La réplica reproduce la `f` del libro con error < 1e-12.

| | Libro | Con circulante 2024 = 84,994 |
|---|---|---|
| C74 · ventas medias | 1.493,633 | igual |
| C75 · NOPAT medio | 231,339 | igual |
| C76 · reinversión media (capex − D&A + circulante) | 40,430 | 111,375 |
| C77 · flujo implícito | 190,909 | 119,964 |
| C78 · FCF base | 161,2 | igual |
| C79 · fugas (mm/año) | 29,709 | −41,236 |
| **C58 · f** | **0,019890** | **−0,027608** |

**Dónde entra `f`:**
- C58 alimenta `Diagnóstico V6 C12`, que leen 125 fórmulas del libro, entre ellas `Motor L6` y siguientes, cuando `Diagnóstico V6 C5 = "A"`, como en este libro.
- Convención (`v6/docs/Convenciones_financieras_V6_3.md`): flujo del motor A = `V_t·[m_t·(1−τ) − f] − ΔV/S2C`, y en el terminal también se resta `f`. Con una `f` menor, el flujo de cada año crece en `Δf·V_t`.
- **Magnitud aritmética del término de la fórmula, no efecto en la valoración:** 0,0475 × 1.465 ≈ 70 mm. Es lo que cambiaría el término `f·V` en un año, con todo lo demás igual. Llevar una `f` negativa a conclusiones de valoración exige antes la revisión financiera de PE7, y el efecto en valores exige recalcular el libro (PE1).

**Otras celdas afectadas:**
- **S2C marginal** (C53), que solo sirve de referencia visual en Palancas F16: con el circulante corregido pasaría de 1,549 a 0,916.
- **Uso de cada fila,** según la búsqueda de referencias del script:
  - fila 13: la usan la fila 31, C58 (solo para comprobar que la celda es numérica) y una validación;
  - fila 14: la usan la fila 30, C58 y C76;
  - fila 17: solo la usan la fila 35 y una validación;
  - fila 35: no la usa ninguna fórmula.

**4.2 Capex.** D1 p. 7 y D3 p. 14.
- **Inversión 2025:** −178.746 − 9.757 = **−188.503**, igual al total impreso.
- **Inversión 2024:** −160.063 − 8.737 − 6.000 + 230.000 + 11.668 = **66.868**, igual al total impreso.
- **Capex del sistema:** 188,503 y 168,800, iguales a −(PP&E + intangibles)/1000.

**4.3 Arrendamientos.** D1 p. 52 y D3 p. 58; D1 p. 66 y 67; D1 p. 7.

| | 2025 | 2024 |
|---|---|---|
| Saldo inicial | 44.904 | 45.382 |
| + Altas | 2.404 | 1.429 |
| + Gasto financiero devengado | 2.452 | 2.179 |
| − Pagos | (8.314) | (6.117) |
| + Otros (actualización de tarifas) | 9.596 | — |
| ± Conversión | (1.742) | 2.031 |
| **= Saldo final (cuadra)** | **49.300** | **44.904** |
| «Short-term / low-value lease expenses» (mismo importe que los pagos, en las dos versiones) | 8.314 | 6.117 |

- **NIC 7 (p. 67).** Los flujos (−129.454) más la conversión (−945) dan −130.399, que es la variación del saldo total de la nota 16 (393.312 → 262.913, arrendamientos incluidos). Los cobros y pagos de deuda del estado de flujos suman también −130.399. Ni la tabla ni el estado de flujos separan los 14.452 de movimientos no monetarios de arrendamientos (2.404 + 2.452 + 9.596).
- **Origen de `Análisis C49`.** La media 2023–2025 de pagos − devengado es ((5,861 − 2,131) + (6,117 − 2,179) + (8,314 − 2,452))/3 = **4,51**, que coincide con C49 = 4,5. La media de los pagos totales sería 6,764. El 2,131 de 2023 solo consta en la nota del lector de 2024 (F2).
- **Sensibilidad condicionada (no son límites).**
  - **Con C49 = 6,8**, el FCF base sería 335,4 − 169,7 − 0 − 6,8 − 0 = 158,9 y `f` pasaría a 0,021430 (+0,001540). Supone que todo el pago de arrendamientos, intereses incluidos, está fuera del CFO.
  - **El valor actual, C49 = 4,5**, supone que el interés pagado es igual al devengado, que está dentro de «Interest paid» (explotación) y que el principal está en financiación.
  - **Ninguno de los dos supuestos está acreditado,** y ninguno de los dos valores acota el correcto ni valida el principal o su clasificación en el estado de flujos.
  - **Datos de 2023 sin contrastar:** las dos medias usan los pagos de 2023 (5,861) y, en el caso de 4,5, el devengado de 2023 (2,131), que solo consta en una nota del lector (F2).
  - **La salida del script** escribe «sensibilidad arrendamientos: …»; se lee con estas condiciones.

**4.4 Adquisiciones.** D1 p. 7, D3 p. 14 y D1 p. 10 (venta de Vidrala Italia, 4-jul-2024).
- **2024:** −(230.000 + 11.668)/1000 = −241,668.
- **2025:** 0, porque todas las líneas se imprimen «-».
- **Participada por puesta en equivalencia (−6.000 en 2024):** queda fuera por la convención «negocios/dependientes».

## 4. Referencias de página

| Contenido | D1 (EN), PDF = página impresa | D3 (ES), PDF (impresa) |
|---|---|---|
| Balance (caja, patrimonio) | 2–3 | — |
| Cuenta de resultados | 4 | — |
| Estado de flujos | 7 | 14 (6) |
| Venta de Vidrala Italia | 10 | — |
| Nota 8, arrendamientos | 52 | 58 (50) |
| Nota 16, deuda y conciliación NIC 7 (arrendamiento de Bristol, p. 69) | 66–69 | — |
| Nota 26, gasto financiero | 75 | — |
| Nota 27, BPA y acciones | 75–76 | — |
