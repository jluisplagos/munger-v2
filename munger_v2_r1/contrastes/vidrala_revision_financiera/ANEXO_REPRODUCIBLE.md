# Anexo reproducible · revisión financiera del piloto Vidrala (entrega 4.3; ampliado en la 4.3.1)

Las rutas son relativas a `munger_v2_r1/`. Los documentos van en miles de euros; el sistema, en millones (mm).

## 1. Reproducción

```
python3 -I contrastes/vidrala_revision_financiera/scripts/revision_financiera_vidrala.py > /tmp/r.txt; echo $?      # 0
diff /tmp/r.txt contrastes/vidrala_revision_financiera/resultados/revision_salida.txt                              # sin diferencias
```

- **Comprobaciones:** 217. El script termina con código 1 si alguna no cumple.
- **Solo lectura:** abre el libro con `data_only` y comprueba al final que su huella no ha cambiado. No crea `__pycache__`.
- **Fuentes que usa:** sus huellas se comprueban al empezar.
  - Los textos `CF_2024_ES_EXTRACCION_NUEVA.txt`, `CF_2024_EXTRACCION_NUEVA.txt` y `CF_2023_EXTRACCION_NUEVA.txt` (entrega 4.2).
  - `CF_2025_EXTRACCION_NUEVA.txt` (piloto).
  - El ZIP completo del ESEF 2025 (esta entrega), que se lee con `zipfile`, sin descomprimirlo en disco.
- **Cómo cita:** para cada cifra busca la etiqueta en la página indicada y, a continuación y en ese orden, los importes tal como se imprimen.
- **ESEF:** lee los hechos `ix:nonFraction` sin dimensión de 2024 y 2025 y los compara con las cifras de los textos.

Las baterías anteriores siguen igual:

```
python3 -I contrastes/vidrala_2023_arrendamientos/scripts/contraste_2023_arrendamientos.py | diff - contrastes/vidrala_2023_arrendamientos/resultados/contraste_salida.txt   # 45
python3 -I contrastes/piloto_Vidrala_2025/scripts/contraste_vidrala_2025.py | diff - contrastes/piloto_Vidrala_2025/resultados/contraste_salida.txt                     # 35
```

## 2. Fórmulas del libro e identidad de `f`

Libro: `Historia` C74:C80 y C58; `Análisis` C52. La ventana es W = {2023, 2024, 2025} (C57 = 3).

```
C74 = V   = media_W(ventas)
C75       = media_W(EBIT · (1 − t))                 ← NOPAT: filas 7 y 10
C76       = media_W(capex − D&A + circ)             ← reinversión: filas 12, 8 y 14
C70 = C52 = C46 − C47 − C48 − C49 − C50             ← FCF base (C46 y C47 se escriben a mano, con un decimal)
C79       = C75 − C76 − C70
C58 = f   = C79 ÷ C74
```

**D&A entra en C76, no en C75.** Es la corrección de documentación que pide el encargo (§6 de este anexo).

Sustituyendo:

```
f·V = media_W(NOPAT + D&A − circ − CFO) + C48 + C49 + C50 + (C47 − media capex) − (C46 − media CFO)
```

- **El capex se anula.** Si la fila 12 y C47 cambian igual, `f` no cambia. El script lo comprueba con +10 mm.
- **El circulante y el CFO.** Si salen del mismo estado de flujos:

```
CFO + circ = FAC = beneficio del ejercicio + ajustes + intereses cobrados − intereses pagados − impuestos pagados
```

- **La diferencia anual** g = NOPAT + D&A − FAC se descompone sin residuo:

```
g = − discontinuadas − X + (impuestos pagados − t·EBIT) + (intereses pagados − intereses cobrados)
X = (beneficio de continuadas + ajustes) − (EBIT + D&A)
  = provisiones + deterioros + subvenciones + diferencias de cambio + puesta en equivalencia
    + (ingresos financieros de la cuenta + su ajuste) + (gastos financieros del ajuste + los de la cuenta)
impuestos pagados − t·EBIT = (pagado − corriente) + (corriente − devengado) + (devengado − t·EBIT)
```

## 3. Datos por año (mm) y descomposición

Fuentes:
- **2023 y 2024:** ES24 p.11 (cuenta reexpresada) y p.14 (estado de flujos).
- **2025:** EN25 p.4 y p.7.
- **Impuesto corriente:** ES24 p.69 y EN25 p.56.

Las cifras de 2024 y 2025 coinciden con el ESEF.

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Ventas · EBIT · t (libro) | 1.427,473 · 267,508 · 0,204 | 1.588,267 · 331,008 · 0,2143 | 1.465,160 · 292,068 · 0,2433 |
| NOPAT = EBIT·(1 − t) | 212,936 | 260,073 | 221,008 |
| D&A | 87,210 | 117,720 | 132,948 |
| Beneficio del ejercicio (continuadas + discontinuadas) | 233,395 (213,836 + 19,559) | 298,315 (238,250 + 60,065) | 209,341 (209,341 + 0) |
| Ajustes | 158,414 | 240,195 | 224,195 |
| Intereses cobrados · pagados | 7,774 · 12,320 | 11,200 · 32,100 | 7,509 · 20,800 |
| Impuestos pagados · corriente · devengado | 45,021 · 63,249 · 54,813 | 70,100 · 65,376 · 64,968 | 40,757 · 56,136 · 67,320 |
| **FAC** (= CFO + circulante del mismo estado) | 342,242 (263,437 + 78,805) | 447,510 (362,516 + 84,994) | 379,488 (380,287 − 0,799) |
| **g = NOPAT + D&A − FAC** | **−42,096** | **−69,717** | **−25,532** |
| − discontinuadas | −19,559 | −60,065 | 0 |
| − X | −17,532 | −29,717 | −8,520 |
| X: provisiones · deterioros · subvenciones | 10,647 · 5,394 · −4,116 | 20,024 · 9,465 · −0,266 | 3,829 · 2,414 · −3,453 |
| X: diferencias de cambio · puesta en equivalencia · financieros | −0,131 · 5,607 · 0,131 | 2,245 · 0,494 · −2,245 | 0 · 0,493 · 5,237 |
| Impuestos pagados − t·EBIT | −9,551 | −0,835 | −30,303 |
| … de ello, pagado − corriente | −18,228 | +4,724 | −15,379 |
| … corriente − devengado (diferido y ajustes) | +8,436 | +0,408 | −11,184 |
| … devengado − t·EBIT | +0,241 | −5,967 | −3,740 |
| Intereses netos pagados | +4,546 | +20,900 | +13,291 |

**Medias, con V = 1.493,633:**

| Componente | mm/año | `f` |
|---|---|---|
| Discontinuadas | −26,541 | −0,017770 |
| X | −18,590 | −0,012446 |
| Impuestos: pagado − devengado | −10,408 | −0,006968 |
| … de ello, corriente no pagado en el año | −9,628 | |
| … de ello, diferido y ajustes | −0,780 | |
| Impuestos: devengado − t·EBIT | −3,155 | −0,002112 |
| Intereses netos pagados | +12,912 | +0,008645 |
| C49 | +4,500 | +0,003013 |
| Redondeo de C46 y C47 | +0,046 | +0,000031 |
| **T1** | **−41,236** | **−0,027608** |

## 4. Réplicas por tratamiento

**Constantes en todas:**
- ventas, EBIT, tipo y D&A de 2023–2025;
- capex (fila 12) y C47, salvo en la comprobación de que el capex se anula;
- C48 = C50 = 0;
- C57 = 3, salvo en el diagnóstico de ventana.

| Tratamiento | Qué cambia | Fuente de lo que cambia | Supuesto | `f` | Semáforo (−0,02 a 0,05) |
|---|---|---|---|---|---|
| T0 libro | — | — | — | +0,019890 | Pasa (artefacto) |
| T1 | K14 = 84,994 | ES24 p.14 | Ninguno: corrección factual P1 | −0,027608 | Revisar |
| T2 | T1 y J14 = 89,866 | EN23 p.7 | La presentación del informe 2023, que incluye los ajustes no monetarios de Italia | −0,030076 | Revisar |
| **T3** | C46 = 322,650; J14 = 85,978; K14 = 36,487 (FAC de continuadas) | CFO y explotación de Italia (ES24 p.43); FAC − discontinuadas | Que la explotación de Italia de la nota 5 sea su parte en el CFO (NIIF 5); **δ = 0 (hipótesis)**; circulante derivado, no publicado | **−0,009847** | Pasa (negativa) |
| T3δ | T3 con δ = devengo de Italia (2023: 3,486; 2024: 0,548) | ES24 p.42–43 | Que Italia pagara lo devengado. **Sensibilidad condicionada, no cota**: el pago real podría ser menor o mayor | −0,010747 | Pasa |
| T3a · T3b | T3 con C49 = 6,8 · 0 | Nota 8 (entrega 4.2) | Clasificación de los arrendamientos | −0,008307 · −0,012860 | Pasa |
| T4 (contraste) | g = intereses netos pagados + (devengado − t·EBIT); sin discontinuadas, sin X y con impuestos pagados = devengados | Todo lo anterior | **Normalización:** el calendario fiscal y las provisiones no se repiten y los intereses siguen como en la ventana | +0,009545 | Pasa |

**Carácter de T3 (precisión de la 4.3.1).** −0,009847 se reproduce exactamente, pero solo bajo sus supuestos: δ = 0 y circulante derivado. T3δ y T3a/T3b son sensibilidades a supuestos concretos. No delimitan ningún intervalo demostrado de `f`.

Las etiquetas impresas por el script de 217 comprobaciones se conservan sin cambios para no alterar su salida de referencia. Una de ellas dice «preferente si se mantiene el motor A», y el carácter condicionado que fijan este anexo y el informe prevalece sobre ella.

**Cómo se construye T3:**
- C46 de continuadas = media(263,437 − 26,732; 362,516 − 11,558; 380,287) = 322,650.
- El circulante de continuadas se deriva: FAC de continuadas − CFO de continuadas. Coincide con 84,994 − 50,547 (plusvalía) + (11,558 − 9,518) en 2024, y el script lo comprueba.
- En T3, C70 (148,45) combina el CFO de continuadas con el capex consolidado: no es un FCF base con significado propio, pero `f` no depende de él.

**Diagnóstico de ventana con T3** (no es una propuesta):
- 2024–2025: −0,008575.
- 2025 solo: −0,014355.

## 5. Otras réplicas

**FCF base de continuadas (condicionada).**
- C47 = media(151,7 − 4,315; 168,8; 188,503) = 168,229.
- Supuestos: el capex en caja de Italia de 2023 ≈ sus altas por devengo (EN23 p.30) y el del 1S 2024 = 0.
- FCF = 322,650 − 168,229 − 4,5 = **149,921**, frente a 161,2.
- No es un dato ni una valoración.

**Arrendamientos.**
- Media de los pagos 2023–2025 = (5,861 + 6,117 + 8,314) ÷ 3 = 6,764 → 6,8.
- Media de (pago − interés devengado) = (3,730 + 3,938 + 5,862) ÷ 3 = 4,510 → 4,5.
- Cada mm de C49 mueve `f` en 0,000670.

**S2C de referencia (Historia C53) con P1.**
- K31: −318,428 → −105,594.
- SUMA(H31:L31): 307,762 → 520,596.
- C53 = 476,790 ÷ 520,596 = **0,9159** (libro: 1,5492).
- La cuenta de la fase B (ventas 2025 − 2020 − Brasil 2025 = 298,523 frente a la reinversión orgánica H30:L30):
  - libro: 295,344 → 1,01;
  - con P1: 508,178 → 0,59;
  - con el circulante de continuadas derivado en 2023–2024: 466,844 → 0,64.
- Son aritmética de las filas, no una palanca.

**`r_op` del motor B con las celdas del libro.**
- Fórmula: r·E/(E + D) + i·(1 − τ)·D/(E + D).
- Valores: r = 0,09 (C56, sin cambiar), E = 3.094,6, D = 262,913, i = 0,063393, τ = 0,20032.
- Resultado: **0,086922**. Es aritmética de la convención 4, no una valoración.

## 6. Corrección de documentación (D&A y NOPAT)

El encargo pide corregir la atribución de un efecto directo de D&A sobre NOPAT. Se han cambiado, con una nota «corregido en la entrega 4.3», solo estos dos lugares:

- `contrastes/vidrala_2023_arrendamientos/INFORME_2023_Y_ARRENDAMIENTOS.md`, §1, último párrafo del perímetro.
  - Decía: «Esto afecta a `f` (NOPAT medio y reinversión media de C75 y C76)».
  - Ahora separa los canales: ventas → C74; EBIT y tipo → C75 (NOPAT); D&A, capex y circulante → C76 (reinversión); CFO y capex → C46, C47 y C70 (FCF base).
- `contrastes/vidrala_2023_arrendamientos/ANEXO_REPRODUCIBLE.md`, §2.4, fila de D&A.
  - Decía «C76, NOPAT y reinversión».
  - Ahora dice «C76 (reinversión); no entra en C75 (NOPAT = EBIT × (1 − t))».

No se ha cambiado ninguna cifra, script ni salida de la 4.2. Las salidas de 45 y 35 comprobaciones siguen idénticas.

## 7. Subsanación 4.3.1: entradas, fechas y acciones

```
python3 -I contrastes/vidrala_revision_financiera/scripts/subsanacion_entradas_fechas.py > /tmp/s.txt; echo $?    # 0
diff /tmp/s.txt contrastes/vidrala_revision_financiera/resultados/subsanacion_salida.txt                          # sin diferencias
```

- **Comprobaciones:** 43.
- **Qué hace:** solo lectura; comprueba las huellas, las citas de EN25 y del BORME conservado, las celdas del libro y las notas heredadas del Control maestro (`datos_v63.json`), que clasifica como no contrastadas.
- **Qué no hace:** no calcula ningún valor por acción ni ningún precio de Sí, y no modifica el script de 217 comprobaciones.

**Aritmética explícita.** Cada cifra lleva su fuente:
- **Acciones:**
  - emitidas a 31-dic-2025: 35,206258 (EN25 p.60);
  - en circulación a esa fecha: 35,182858, netas de 23.400 en autocartera (p.61);
  - emitidas tras la liberada: 36,966570 (+1.760.312; BORME);
  - en circulación tras la liberada: 36,942001 con la autocartera de 2025 y 35,894521 con la autocartera heredada de 2026 (≈1,021 mm, **no contrastada**).
- **Tiempo:** 307 días entre el 31-dic-2025 y el 3-nov-2026 → (1,09)^(307/365) − 1 = 7,52 %. Es la convención de descuento del motor (exponentes enteros desde el año base), no una valoración.
- **Dividendos de 2026:** 43,338 (hecho; EN25 p.64) + 16,490 (propuesto; EN25 p.65; pago del 15-jul-2026 heredado) = 59,828 mm = 1,93 % de C41.
- **Deuda neta con arrendamientos:** 154,561 a 31-dic-2025 (contrastada) y 300,2 a 30-jun-2026 (heredada); +145,6 = 4,71 % de C41.
- **`r_op` (convención 4):**
  - libro: 0,086922;
  - con E sobre las acciones tras la liberada y la autocartera heredada: +0,5 pb;
  - con D a 30-jun-2026 (heredado): −15,2 pb.

**Supuestos declarados:**
- La fecha sin derecho de la liberada se interpreta; el BORME no la fija.
- La autocartera de 2026 y los saldos de 30-jun-2026 son herencia no contrastada del Control maestro. Su fuente, el semestral 1S2026 (doc. 2487), no está conservada.

