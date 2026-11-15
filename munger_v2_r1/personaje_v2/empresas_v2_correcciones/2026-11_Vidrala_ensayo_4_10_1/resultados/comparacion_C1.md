# Comparación con C1 de la 4.10 y variante de precisión de C46/C47

| Variante | MALO | NORMAL | BUENO | Ponderado | Precio de Sí | r_op | Puente | FCF base |
|---|---|---|---|---|---|---|---|---|
| C1_control | 53.6597 | 70.7430 | 86.4438 | 70.4665 | 65.6645 | 0.086990 | 160.784 | 161.200 |
| ensayo_control | 53.6597 | 72.7405 | 86.4438 | 71.6650 | 66.5206 | 0.086990 | 160.784 | 161.200 |
| ensayo_palancas_C1 | 53.6597 | 70.7430 | 86.4438 | 70.4665 | 65.6645 | 0.086990 | 160.784 | 161.200 |
| ensayo_C46_C47_precisos | 53.6597 | 72.7405 | 86.4438 | 71.6650 | 66.5206 | 0.086990 | 160.784 | 161.245 |

**Controles:** {"C1_control_reproduce_C1": true, "ensayo_control_reproduce_resultados_json": true}

**Atribución (diferencias en €/acción):**

- entrada_y_convencion (C1 → ensayo con palancas de C1): {"MALO": 0.0, "NORMAL": 0.0, "BUENO": 0.0, "ponderado": 0.0, "precio_de_si": 0.0}
- juicio (palancas nuevas: ensayo con palancas de C1 → ensayo): {"MALO": 0.0, "NORMAL": 1.997478, "BUENO": 0.0, "ponderado": 1.198487, "precio_de_si": 0.856062}
- total (C1 → ensayo): {"MALO": 0.0, "NORMAL": 1.997478, "BUENO": 0.0, "ponderado": 1.198487, "precio_de_si": 0.856062}
- precision_C46_C47 (ensayo → ensayo con 335,413 / 169,668): {"MALO": 0.0, "NORMAL": 0.0, "BUENO": 0.0, "ponderado": 0.0, "precio_de_si": 0.0}

**Celdas de entrada distintas entre C1 y el ensayo con las mismas palancas:** 21 (8 numéricas o fechas; 13 de texto)

Numéricas o fechas (datos y fechas). Ninguna entra en el valor del motor B con E dada (C41): C37 (precio) solo entra en la escalera, y C24, C33, C42, C53, C54 y C57 son datos informativos o de reglas que no mueven B78:D78 (la variante con las palancas de C1 reproduce C1):

- `Análisis!C24`: C1 0.13 → ensayo 0.1394
- `Análisis!C33`: C1 0.69 → ensayo 0.36
- `Análisis!C37`: C1 87.9 → ensayo 90.1
- `Análisis!C42`: C1 7.68 → ensayo 7.82
- `Análisis!C53`: C1 109.4 → ensayo 108.352
- `Análisis!C54`: C1 409.6 → ensayo 262.913
- `Análisis!C57`: C1 0.0329 → ensayo 0.0285
- `Palancas!C45`: C1 datetime.datetime(2026, 11, 3, 0, 0) → ensayo datetime.datetime(2025, 12, 31, 0, 0)

De texto: datos escritos como texto (C34 «No» → «Sí»; D4, fecha de análisis 2026-11-03 → 2026-11-11) y juicios, nombres de escenarios, predicciones y notas de la fase C; no entran en el cálculo del motor:

- `Análisis!B101`
- `Análisis!B102`
- `Análisis!B66`
- `Análisis!C104`
- `Análisis!C34`: C1 'No' → ensayo 'Sí'
- `Análisis!C66`
- `Análisis!D4`: C1 '2026-11-03' → ensayo '2026-11-11'
- `Análisis!D66`
- `Palancas!A38`
- `Palancas!A39`
- `Palancas!A40`
- `Diagnóstico V6!B222`
- `Diagnóstico V6!B223`
