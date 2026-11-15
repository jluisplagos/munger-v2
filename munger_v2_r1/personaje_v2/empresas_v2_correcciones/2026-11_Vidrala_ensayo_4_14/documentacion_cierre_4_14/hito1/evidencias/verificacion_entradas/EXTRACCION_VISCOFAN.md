# VISCOFAN · informe del extractor (verificación completa de las entradas, 4.14)

Extractor: agente extractor E-Viscofan (Claude), 14-nov-2026. Registro: `Viscofan/verificacion_entradas.json`, que he hecho a partir de la plantilla de 232 celdas. Los campos del revisor están vacíos y todas las comprobaciones siguen en «pendiente». Perímetro declarado: **consolidado** (en el registro no hay operaciones interrumpidas con importe). No he corregido el libro.

Los scripts que generan el registro están en `scripts_extractor/` (`evx_escribir.py`). Cada cita se toma literal de la página «[PDF PAGE n]» del texto y se valida automáticamente en esa página. Para las cifras se comprueba además la posición de la columna en el renglón, no solo que los dígitos estén presentes.

## 1. Recuentos

| Clase | Celdas del universo | Auxiliares «aux:» |
|---|---|---|
| dato_publicado | 124 | 102 |
| derivado | 44 | — |
| cero_comprobado | 12 | — |
| no_aplicable | 9 | — |
| hipotesis | 25 | — |
| convencion | 18 | — |
| **Total** | **232** | **102** (334 entradas) |

Resultado de `verificacion_entradas.py comprobar`:
- universo 232; 0 errores, 0 discrepancias, 0 desactualizadas, 0 entradas sin registro, sobrantes o repetidas;
- 291 pendientes:
  - 246 esperan la revisión independiente;
  - 44 son derivados cuyos orígenes están pendientes;
  - 1 tiene campos sin rellenar (C37, ver §3);
- el comprobador da por «comprobadas» 43 entradas: son las hipótesis y convenciones, porque no les exige revisor. No son datos verificados.

Las 18 diferencias reales llevan `nota = «DISCREPANCIA del extractor»` en `comprobacion`. Hoy no salen como «discrepancias» porque sus orígenes siguen pendientes; la de G13, además, por un fallo del comprobador (ver §2.4 y §4). Saldrán cuando el revisor verifique los orígenes.

Clasificación de las celdas:
- **Derivados:**
  - D&A 2016–2018;
  - tipos impositivos;
  - circulante 2019–2025;
  - deuda (todos los años);
  - arrendamientos 2019–2025;
  - medias C46–C50;
  - capitalización C41;
  - N1.tipo (B11).
- **Ceros comprobados:**
  - arrendamientos 2016–2018 (la NIIF 16 no estaba vigente);
  - adquisiciones 2020–2023;
  - minoritarios 2019–2023.
- **No aplicable:** D5 (ADR), B38 (λ) y B44–B50 (cartera P0).

## 2. Incidencias (original, lo que dice la fuente y evidencia)

1. **Pensiones: el concepto no es el de la fila (F25, G25, H25, J25, K25, L25).**
   - La fila 25 pide el «déficit neto de pensiones (obligación − activos)».
   - En 2019–2021 y 2023–2025 el modelo toma la línea del balance «provisiones no corrientes por prestaciones a los empleados». Esa línea incluye otras retribuciones a largo plazo (incentivos).

   | Año | Libro | Prestación definida | Diferencia | Fuente |
   |---|---|---|---|---|
   | 2019 | 33,294 | 29,995 | 3,299 | AR_2020 p. 61 |
   | 2020 | 37,871 | 28,204 | 9,667 | CF_2021 p. 49 |
   | 2021 | 29,133 | 24,779 | 4,354 | CF_2022 p. 61 |
   | 2023 | 25,916 | 17,266 | 8,650 | CF_2024 p. 67 |
   | 2024 | 19,145 | 16,498 | 2,647 | AR_2025 p. 87 |
   | 2025 | **20,989** | **14,878** | **6,111** | AR_2025 p. 87 |

   - La serie no es homogénea: 2016–2018 y 2022 llevan solo la prestación definida.
   - L25 entra en el puente del motor B: 6,1 mm ≈ 0,13 €/acción.
2. **Circulante: el tratamiento de la serie no es homogéneo (F14, G14, J14, K14, L14).**
   - En 2019, 2020 y 2023–2025 el modelo suma la variación de provisiones.
   - En 2016–2018, 2021 y 2022 no la suma. El subtotal propio de la empresa («Changes in working capital», AR_2017 p. 12, IA_2018 p. 28, AR_2019 p. 12) tampoco la incluye.
   - Valores sin provisiones: 2019 −6,135 (es el subtotal publicado en AR_2019 p. 12); 2020 25,178; 2023 90,646; 2024 8,862; 2025 49,933.
   - Uso: motor A, que no es el elegido.
3. **Deuda de 2017 (D22): el tratamiento no es el de 2016 y 2018.**
   - El libro tiene 82,794: bancos, intereses, arrendamiento financiero, COFIDES y CDTI (IA_2018 pp. 104–105). Deja fuera 10,904 de «Otros pasivos financieros» (entre ellos, proveedores de inmovilizado por 8,079).
   - 2016 y 2018 incluyen todos los «Otros pasivos financieros».
   - Con ese criterio, 2017 sería 93,722 − 24 = 93,698.
4. **Adquisiciones de 2020 (G13): el libro está vacío y la fuente dice cero.**
   - CF_2021 p. 8 imprime «0»; AR_2020 p. 8 imprime «-».
   - El total de inversión cuadra sin adquisiciones: −53,576 = −55,320 + 605 + 1,139.
   - Sin efecto en las bases de P-M1, que usan 2021–2025.
5. **Redondeos de valores escritos por el inversor y no pisados por la fase 1.**

   | Celda | Libro | Cálculo |
   |---|---|---|
   | C41 | 2487.7 | 2487.713 |
   | C47 | 77.5 | 77.533 |
   | C48 | 8.3 | 8.294 |
   | C49 | 5.5 | 5.547 |
   | C50 | 3.71 | 3.707 |

   Evidencia: `Viscofan_v63_datos.xlsx.fase1.registro.json`, «no_pisadas». Efecto neto en el FCF base: +0,07 mm. Es inmaterial.
6. **Observaciones que no son discrepancias con la fuente:**
   - **C55 (acciones):** la media «diluida» publicada (45,479,209) queda por debajo de la básica (45,656,226), en AR_2025 p. 119. Eso contradice la NIC 33. Además, el concepto es la media de 2025 y no las acciones vigentes el 3-nov-2026. La decisión VISCOFAN-ACCIONES está pendiente.
   - **C49:** el estado de flujos da el pago total por arrendamientos, sin separar principal e intereses.
   - **EBIT de 2016, 2018 y 2019:** incluye diferencias negativas de combinaciones de negocios (4,475; 5,486; 10,889) y, en 2019, un deterioro del fondo de comercio (−3,520).

## 3. Fuentes que faltan o son débiles

- **Análisis!C37 (precio de 54,70 €, cierre del 3-nov-2026): no hay fuente en el paquete.** Solo consta la declaración de Bolsamania en `fase1_metadatos.json`. Hace falta el cierre del 3-nov-2026 de BME: VIS, de un proveedor, conservado con su huella. Por esto C41 también queda sin origen comprobable.
- **Ediciones con la paginación de la fase 1 que no se han recuperado:** AR_2016, AR_2018, AR_2021, AR_2022 y AR_2023. He usado otras ediciones con sus propias páginas: IA_2018_es, CF_2021, CF_2022_compilacion y CA_2023_es. Todas contienen las cifras del modelo.
- **Problemas de extracción del texto** que el revisor debe mirar en el PDF:
  - CF_2021 recorta ceros finales («912,16», «51,99»). Por eso ventas, caja y capex de 2020 se citan en AR_2020.
  - CF_2021 p. 8 tiene desplazados los rótulos del bloque de inversión.
  - CF_2024 p. 9 tiene desordenado el rótulo de provisiones. La provisión de 2023 se cita en CA_2023 p. 8.
- **Lo que no he revisado:** he trabajado sobre el texto extraído y no he abierto las páginas del PDF. Las citas que apoyan las hipótesis (fase B y C) tampoco se han contrastado: son apoyo del juicio, no entradas.

## 4. Observaciones sobre las comprobaciones automáticas

- **Un cero comprobado con la celda vacía en el libro no se detecta.** `_norm_txt(0)` devuelve «», así que el comprobador da por iguales el 0 y el vacío. Afecta a G13.
- **La prueba de dígitos de una cita no sirve para los ceros impresos como «-» o «—», ni para las ausencias contables.** Pasa por coincidencia con otros ceros del pasaje (por ejemplo, el «0» de «2019»). Lo indico en la nota de cada entrada afectada.
- **Las hipótesis y convenciones cuentan como «comprobadas» sin revisión.**

## 5. Incidente operativo

El directorio temporal está compartido con el agente E-Vidrala, que sobrescribió mi `construir.py`. Al ejecutar mi script de prueba se importó su `construir.py` y **se reescribió `/home/claude/trabajo_4_14/agentes/E_vidrala/Vidrala/verificacion_entradas.json` (14-nov 11:19)** con la salida de su propio script. Debería coincidir con lo que ese agente genera, pero conviene que lo regenere y lo compruebe. Después aislé mis scripts con nombres propios (`evx_*`).
