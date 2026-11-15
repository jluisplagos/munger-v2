# Anexo reproducible · contraste 2023 y arrendamientos (entrega 4.2)

Las rutas son relativas a la raíz `munger_v2_r1/`. Los importes van en miles de euros cuando vienen de los documentos, y en millones (mm) cuando vienen del sistema.

## 1. Reproducción

```
python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py > /tmp/s.txt; echo $?     # 0
diff /tmp/s.txt contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt                                # sin diferencias
python3 -I contrastes/piloto_Vidrala_2025/scripts/contraste_vidrala_2025.py | diff - contrastes/piloto_Vidrala_2025/resultados/contraste_salida.txt   # piloto: 35, sin diferencias
```

El script es de solo lectura, no crea `__pycache__` y hace **45 comprobaciones**. `verificar_paquete.sh` no lo ejecuta; por qué, en `PROPUESTAS_Y_PENDIENTES.md`, P11.

**`comprobar-anio` sobre una copia,** con los textos nuevos copiados como `texto/CF_2023.txt` y `texto/CF_2024.txt`. La copia queda intacta, con las mismas huellas antes y después:

```
cp -r personaje_v2/empresas_v2/Vidrala /tmp/c/ && mkdir /tmp/c/Vidrala/texto
cp contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2023_EXTRACCION_NUEVA.txt /tmp/c/Vidrala/texto/CF_2023.txt
cp contrastes/vidrala_2023_arrendamientos/textos_nuevos/CF_2024_EXTRACCION_NUEVA.txt /tmp/c/Vidrala/texto/CF_2024.txt
python3 -I personaje_v2/scripts/fase1_historia.py comprobar-anio /tmp/c/Vidrala 2023   # 4 ceros heredados sin cita
python3 -I personaje_v2/scripts/fase1_historia.py comprobar-anio /tmp/c/Vidrala 2024   # 3 ceros heredados + 2 líneas de D&A (p.4 → p.7)
```

**Clasificación según el contrato (§1).**
- Las dos líneas de D&A son de **tipo A**: el respaldo está mal atribuido, pero la cifra es correcta. Se corrigen en una versión nueva de `AR_2024.json`, sin tocar el valor (P8).
- Los ceros son del **paso 4**: una persona tiene que revisarlos.

**Obtención de las fuentes.** El procedimiento es el del piloto (`contrastes/piloto_Vidrala_2025/ANEXO_REPRODUCIBLE.md`, §1):
- `fetch` en el navegador desde vidrala.com;
- SHA-256 con `crypto.subtle`;
- traslado en base64 por tramos de 250.000 caracteres: 10 para D7, 6 para D6 y 38 para D9;
- reconstrucción y comprobación de la huella.

El ESEF (D12) se abrió con JSZip 3.10.1 en el navegador. Los hechos se extrajeron con una expresión regular sobre `<ix:nonFraction>`, y los miembros pequeños se trasladaron completos.

## 2. Citas y cálculos

### 2.1 CFO y circulante de 2023

**Informe 2023, D6 p. 7 (inglés), columna 2023:**
- Profit for the year 233.395
- Ajustes: 97.865 + 5.992 − 788 + 1.213 − 131 + 10.647 − 7.504 − 8.352 + 16.435 + 54.098 = **169.475**, igual al impreso.
- Circulante: −83.925 − 34.457 − 6.068 + 36.138 − 1.554 = **−89.866**, igual al impreso «Cash used in operating activities».
- CFO: 233.395 + 169.475 − 89.866 − 12.320 + 7.774 − 45.021 = **263.437**, igual al impreso.

**Informe 2024, D9 p. 14 (español, prevalece), columna 2023 (\*) «Cifras reexpresadas»:**
- Ajustes: 87.210 + 5.659 − 1.478 + 1.213 − 131 + 10.647 − 4.116 − 8.352 + 12.949 + 54.813 = **158.414**, igual al impreso.
- Circulante: −83.925 − 34.457 − 6.068 + **47.199** − 1.554 = **−78.805**, igual al impreso «Efectivo generado por las operaciones».
- CFO: 233.395 + 158.414 − 78.805 − 12.320 + 7.774 − 45.021 = **263.437**.

**Informe 2024, D7 p. 7 (inglés), misma columna.**
- Provisiones (6.553), subvenciones (5.372) y gastos financieros 3.435 **repiten la columna 2022 de D6**.
- Sus ajustes suman 130.444, frente a 158.414 impreso.
- Es un error de la traducción; prevalece D9.

**Diferencia D9 − D6 por línea:**

| Línea | D6 (2023) | D9 (2023 reexpresado) | Diferencia | Cuenta de Italia 2023 (D7 p. 35) |
|---|---|---|---|---|
| Amortización | 97.865 | 87.210 | −10.655 | Amortisation cost (10.655) |
| Deterioro de activos no corrientes | 5.992 | 5.659 | −333 | Impairment (333) |
| Deterioro de deudores | (788) | (1.478) | −690 | — (sin línea propia) |
| Subvenciones | (7.504) | (4.116) | +3.388 | Other incomes 3.387 (diferencia de 1) |
| Gastos financieros | 16.435 | 12.949 | −3.486 | Finance cost (3.486) |
| Impuesto | 54.098 | 54.813 | +715 | Income Tax 715 |
| **Total ajustes** | 169.475 | 158.414 | **−11.061** | |
| Otros activos y pasivos (circulante) | 36.138 | 47.199 | **+11.061** | |

**Flujos de Italia (D7 p. 35):** explotación 2023 = 26.732; inversión 2023 = (28.371).

**Nota 2(b) (D7 p. 10–11):** el estado de flujos de 2023 se reexpresa «to reflect the impact of the sale of the Italy segment».

### 2.2 Capex de 2023
- D6 p. 7: (143.848) y (7.852).
- D9 p. 14: «Pagos por la adquisición de inmovilizado material (143.848)» y «… de activos intangibles (7.852)».
- Suma: 151.700, igual a Historia J12 (151,7).

### 2.3 Arrendamientos (nota 8)

| | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|
| Fuente | D6 p. 52 | D6 p. 52; D7 p. 56; D9 p. 64 | D7 p. 56; D9 p. 64 | D1 p. 52; D3 p. 58 |
| Saldo inicial | 776 | 2.346 | 45.382 | 44.904 |
| Altas por combinación de negocios | — | 46.123 | — | — |
| Altas | 2.133 | 643 | 1.429 | 2.404 |
| Gasto financiero devengado | 50 | 2.131 | 2.179 | 2.452 |
| Pagos | (613) | (5.861) | (6.117) | (8.314) |
| Otros / conversión | — | — | 2.031 | 9.596 / (1.742) |
| Saldo final (cuadra) | 2.346 | 45.382 | 44.904 | 49.300 |
| «Gastos por arrendamientos a corto plazo y de poco valor» | 613 | 5.861 | 6.117 | 8.314 |

**Estado de flujos.** En los tres años, el bloque de financiación no tiene línea de arrendamientos ni de intereses.

**Flujos de deuda del estado de flujos frente a la nota 16 y la conciliación NIC 7:**
- **2024:** las líneas de deuda suman −205.736 (229.495 − 201.931 − 233.300), que es la variación del saldo de préstamos, arrendamientos incluidos: 599.048 → 393.312. Los «cash flows» de la tabla NIC 7 (D7 p. 72) son −195.696, y la conversión −10.040.
- **2025:** las líneas de deuda suman −130.399, que es la variación del saldo. La NIC 7 da −129.454 de flujos y −945 de conversión.
- **2023:** las líneas de deuda suman 107.377 (257.877 − 4.500 − 146.000). La variación del saldo es 275.495, y la NIC 7 (D6 p. 67) da 53.722 de flujos, 224.781 de combinación de negocios y −3.008 de conversión. No hay igualdad.
- **Errata de D6:** la columna 2022 imprime «112,5000».

**ESEF 2025 (D12).**
- 378 hechos numéricos de 112 conceptos.
- Ningún concepto contiene «Lease».
- «Pagos de intereses» va etiquetado `ifrs-full:InterestPaidClassifiedAsOperatingActivities` (20.800 y 32.100).
- Etiquetas de la financiación de 2025:
  - `ProceedsFromBorrowings`: 219.500, que es «Cobros procedentes de otras deudas»;
  - `RepaymentsOfBorrowings`: 125.259;
  - extensiones `vidrala:CobrosProcedentesDeLasDeudasConEntidadesDeCredito` (2.626) y `vidrala:PagosProcedentesDeOtrasDeudas` (227.266).
- Las notas solo están etiquetadas como bloques de texto, por ejemplo `DescriptionOfAccountingPolicyForLeasesExplanatory`.

**Bristol.**
- D7 p. 75: cuotas mensuales de 466 miles € (387 miles £), al 5 %, hasta febrero de 2034.
- D1 p. 69: 554 miles € (483 miles £) en 2025, y «GBP 354 thousand in 2024». Es inconsistente con D7.
- Orden de magnitud (aritmética, no evidencia de principal): 466 × 12 = 5.592 frente a pagos de 2024 de 6.117; 554 × 12 = 6.648 frente a pagos de 2025 de 8.314.

### 2.4 Recorrido hasta las celdas

| Dato 2023 | `AR_2024.json` (anterior) | Decisión | `fase1_v63.json` | Celda | Uso |
|---|---|---|---|---|---|
| CFO | 263.437 (p. 7) | — | 263,437 | Historia J11 | C46 = media J11:L11 = 335,4 |
| Capex | 143.848 + 7.852 (p. 7) | — | 151,7 | J12 | C47 = 169,7; C76 |
| Circulante | (78.805) (p. 7) | — | 78,805 | J14 | filas 30 y 31; C53; **C76 → C58 (`f`)** |
| Pago de arrendamientos | (5.861) (p. 56) | — | 5,861 | J17 | fila 35, informativa. C49 = 4,5 no la usa: procede de la herencia V5.3 |
| D&A (contexto) | 87.210 (cita p. 4; está en p. 7) | — | 87,21 | J8 | C76 (reinversión); no entra en C75 (NOPAT = EBIT × (1 − t)) · corregido en la entrega 4.3 |

### 2.5 Réplicas

Repiten las fórmulas de Historia C74:C80 y Análisis C52 sobre los valores en caché del libro.

**Constantes en todas:** ventas, EBIT, tipo, D&A y capex de 2023 a 2025; C57 = 3; C46, C47, C48 y C50.

| Escenario | Cambia | C76 | C79 | `f` | FCF base |
|---|---|---|---|---|---|
| Libro | — | 40,4303 | 29,7087 | 0,019890 | 161,2 |
| A | K14 = 84,994 | 111,3750 | −41,2359 | −0,027608 | 161,2 |
| B | K14 = 84,994 y J14 = 89,866 | 115,0620 | −44,9229 | −0,030076 | 161,2 |
| C | J14 = 89,866 | 44,1173 | 26,0217 | 0,017422 | 161,2 |
| D (sensibilidad condicionada) | C49 = 6,8 | 40,4303 | — | 0,021430 | 158,9 |
| E (sensibilidad condicionada) | C49 = 0 | 40,4303 | — | 0,016877 | 165,7 |

Ninguna réplica es una conclusión de valoración ni valida la ventana, todas las entradas de `f` o la conveniencia de proyectar una `f` negativa.
