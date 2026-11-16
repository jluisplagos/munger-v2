# Correcciones V1–V11 de la revisión dirigida a P1–P4 · propuesta F1 · Elis

Fecha: 16-nov-2026. Autor: frente E (sesión «Conciliación económica Elis/F1»).

- **Revisión que se corrige:** [revision/REVISION_PROPUESTA_P1_P4.md](revision/REVISION_PROPUESTA_P1_P4.md), commit `8fcc7fd792f065cf29e2dc915bda92faeff1d45a`, de la rama `auditoria/economica-f1-frente-e-revision`. Revisó el commit congelado `13f864f`. La copia es idéntica a la del revisor (blob `8ff1930f…`).
- **Punto de partida:** HEAD `bb28319ab7cbf02d7b0ad5c19591a098464dc8ec`, igual al remoto y sin trabajo posterior.
- **Commits de este encargo:**
  - `593a391` · bloque A: herramientas de investigación;
  - `6a48bc4` · bloque B: propuesta, especificación, informe y notas en la respuesta anterior;
  - el commit que contiene este archivo · bloque C: esta respuesta, el registro y el punto de recuperación.

**Qué hace y qué no.**
- **Hace:** corrige los defectos documentales, de especificación y de pruebas señalados en V1–V11.
- **No adopta** ninguna de las decisiones (1a)–(5b), ni implementa nada en el producto ni en los libros oficiales.
- **Conserva** C48 = 108, C49 = 128,1, el FCF base 307,933 y E1/D3/E2/E6. Elis sigue en `pendiente_de_datos`.
- **No elige** R, políticas, probabilidades ni umbrales. Donde la corrección pedía una elección, el texto la ofrece como opción explícita a la persona responsable:
  - (4b), opciones A y B;
  - alcance de N1 en (5a);
  - vías de (3b).
- **No encarga** ninguna revisión ni encadena rondas. Estas correcciones se revisarán externamente solo en lo afectado.
- No se ha enviado ninguna comunicación a terceros.

## 0. Resumen

| | Gravedad | Estado | Dónde | Prueba |
|---|---|---|---|---|
| **V1** | Material | Corregida. Pendiente el dato M6 | Propuesta (tabla, filas 2 y 4b; §2); respuesta anterior (§3, nota); informe (§6.3, §6.4) | Definición publicada comprobada en los PDF (`copia_investigacion_f1`, pasajes V1) |
| **V2** | Menor | Corregida | Especificación E4 (X^v), E2, E3, E5 (V-F1i y V-F1j), T15; propuesta (5b), §2, §4 y §5.2 | Casos V2a–V2h con el ancla calculada con E4 |
| **V3** | Menor | Corregida. Las cifras de la actualización siguen fuera del CSV verificado | Propuesta §5.1 y (5a); especificación E3; respuesta anterior (notas) | Literales comprobados en el PDF; −0,790 [LECTURA] |
| **V4** | Menor | Corregida. El alcance y la convención quedan para quien decide | Propuesta (5a) y §5.1; especificación E3, E8.1, E8.4 y T16; informe §4.2 | −9,141 con el τ de la ventana; +0,416 si alcanza a 2021–22 [LECTURA]; caso fiscal sintético |
| **V5** | Menor | Corregida | Propuesta (1b), (2)(v), §1, §2 y §5.3; especificación E2 (`perimetro_margen`), E8.5 y V-F1f | −16,778 / +10,118 / −6,660; +4,206 / −10,118 / −5,913 |
| **V6** | Menor | Corregida | Propuesta (4a), severidad y §4; especificación E4 y V-F1k | Bloque 10 del libro leído y contrastado; caso P4e |
| **V7** | Menor | Corregida | Especificación E3 (fórmula del término explícito) y E2 (motivo de la PPA decreciente) | Casos V2b y V2g |
| **V8** | Menor | Corregida | Propuesta (3a) y §3 | Medias del CSV: 867,167 / 127,667 / 994,833 |
| **V9** | Menor | Corregida | `controles_sinteticos_f1.py`; especificación T15 y T8 | 32 casos; 3 guardas; caso fiscal; motor = `motor_a` en 4 juegos |
| **V10** | Forma | Corregida | Especificación E2, E4, E5 y T15; propuesta; respuesta anterior (notas) | Sin frases contradictorias (`grep`) |
| **V11** | Forma | Corregida | Propuesta, tabla única: (1a), (3b) y (4b); columna de controles | Lectura |

## 1. Pruebas ejecutadas

Desde `scripts/`, con el árbol `munger_v2_r1` materializado de la base 4.14 y el libro de Elis `d2593777…92385`, leído en solo lectura. `LIBRO` y `RAIZ` son esas rutas.

```bash
python3 -I controles_sinteticos_f1.py --salida ../resultados/controles_sinteticos_f1.json
```

```bash
python3 -I copia_investigacion_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro "$LIBRO" --contraste ../resultados/contraste_f1.json --raiz "$RAIZ" --salida ../resultados/copia_investigacion_f1.json --informe ../resultados/copia_investigacion_f1.md
```

```bash
python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro "$LIBRO" --caja-no-nula ../resultados/caja_no_nula.json --salida ../resultados/contraste_f1.json --informe ../resultados/contraste_f1.md
```

| Script | Resultado | Salida |
|---|---|---|
| `controles_sinteticos_f1.py` | Código 0. **32 casos**, todos con su resultado esperado: 14 coherentes y 18 incoherencias ilustradas. 23 tienen crecimiento y 8 calculan el ancla con la fórmula de E4. Los 9 casos de la revisión externa se reproducen. **3 guardas** V-F1c correctas: una no salta y dos sí. **Caso fiscal** de N1 correcto. El motor sintético coincide exactamente con `motor_a` en **4 juegos**, con g15 ≠ g∞, m0 ≠ m_obj e impuestos | `resultados/controles_sinteticos_f1.{json,log}` |
| `copia_investigacion_f1.py` | Código 0. **55 controles, 0 fallidos.** Reproduce el libro y el diagnóstico, como antes, y las cifras nuevas de la revisión dirigida: −12,396 / −20,270, −11,190 / −18,142, −9,141 / −15,848, −9,763, −10,118 y −6,660. **14 de 14** literales [LECTURA] y **12 de 12** pasajes encontrados en su página del PDF (pdftotext), con las huellas de los PDF iguales a `datos/fuentes.json` | `resultados/copia_investigacion_f1.{json,md,log}` |
| `contraste_f1.py` (sin cambios) | 292 comprobaciones, 0 fallidas; salidas idénticas byte a byte | `resultados/contraste_f1.{json,md}` |
| Manifiesto | `sha256sum -c MANIFIESTO_SHA256.txt`: OK, en cada commit | — |

No se han vuelto a ejecutar el verificador de cifras, sus tests, la mutación ni LibreOffice: no cambia su código ni sus entradas. Los scripts de la revisión dirigida tampoco se han ejecutado: sus cifras se reproducen con el código propio del autor.

## 2. Respuesta numerada

### V1 · material · el crecimiento orgánico publicado no excluye las compras pequeñas

**Corregido.**
1. **Fundamento con la definición publicada.** El crecimiento orgánico solo excluye el efecto de las adquisiciones «importantes», de más de 5,0 millones de ingresos anuales en Francia y de 3,0 en los demás países (URD25 p.313; DEU24 p.259; URD23 p.267). La propuesta (§2, «Compras de sociedades») y el informe (§6.3) lo dicen así. La frase anterior del informe se cita.
2. **Inferencia rebajada.**
   - Se dice ahora: «en la ventana, las ventas se sostuvieron sin compras importantes» [I].
   - Se marca como no publicado [B]: si las bajas se repusieron sin compras, qué parte del efecto volumen procede de las compras pequeñas y si estas reponen o amplían cartera. La empresa las describe como compras que «help to consolidate the Group's position» (URD25 p.339).
3. **Sensibilidad con importes publicados** [P][LECTURA: DEU24 p.288; URD25 p.342 y p.341]. Son referencias, no cifras que elegir para R_compras:
   - 31,5 de media para las «otras adquisiciones» (35,3 / 22,0 / 37,3), el 10,2 % del FCF base;
   - 127,7 para todas, con la nota de que 134,3 de los 383,0 de la ventana son pagos aplazados de Lavartex.
4. **M6 precisado:** la finalidad de las compras pequeñas y el crecimiento orgánico sin ellas (propuesta §3; informe §6.4).
5. **Condición de revisión.** La anterior, «si el crecimiento orgánico en volumen deja de ser positivo», no es observable. Se sustituye por «si se obtiene M6».

**Consecuencia en la recomendación (4b).** Con el apoyo publicado reducido, la propuesta **ya no recomienda aprobar la hipótesis**. Ofrece dos opciones con su texto exacto:
- **A**, recomendada: mantener pendiente la clasificación hasta M6; V-F1j bloquea;
- **B**: aprobar la hipótesis declarada, sabiendo que su apoyo es parcial.

Es la opción prudente cuando falta el dato, no una política nueva. La fila 2 deja de citar «reposición orgánica en la ventana» y dice lo que se sostiene.

**Pendiente:** M6, un dato.

### V2 · menor · lo que se cobra con un término explícito seguía en el denominador del ancla de S2C

**Corregido.**
- **Regla nueva en E4:** C53 = (V_L − V_G) ÷ Σ(capex − D_X + ΔWC + adquisiciones − X^v). X^v es lo que la proyección cobra como término explícito: la transición con `termino_explicito` y las compras de reposición fuera de D_X. Lo que está en D_X ya queda fuera por la resta de D_X.
- **V-F1i y V-F1j** bloquean también lo «cobrado como término y también en el denominador del ancla».
- En la propuesta: (5b), la tabla de correspondencia del §2, el §4 y el §5.2.

**Prueba** (`controles_sinteticos_f1.json`; ventana con ΔV = 5 y crecimiento del 5 % que baja al 2 %):

| Caso | Ancla | Resultado | Diferencia máxima (motor − caja) |
|---|---|---|---|
| V2a · transición temporal como término, E4 anterior | 5/12 | Incoherente: la cobra dos veces y, por el ancla, también en los años 6–10 | −8,509 (año 1: −7,0) |
| V2b · la misma, E4 corregida | 1 | Coherente | 0 |
| V2c · transición permanente proporcional, en R | 1 (por D_X) | Coherente | 0 |
| V2d · transición fija en euros, en R | 1 | Incoherente: f la hace crecer con las ventas | −3,665 (año 11) |
| V2e · transición que amplía capacidad | 5/12 = S2C real | Coherente | 0 |
| V2f · compras de reposición como término, E4 anterior | 5/14 | Incoherente | −10,940 (año 1: −9,0) |
| V2g · las mismas, E4 corregida | 1 | Coherente | 0 |
| V2h · las mismas, en R (`A3_estimado`) | 1 (por D_X) | Coherente | 0 |

Coincide con las sondas S1 y S2 de la revisión, con otras cifras porque mi senda de crecimiento sigue la de `motor_a`.

### V3 · menor · la caja del earnout y la actualización de 2025 están publicadas

**Corregido.**
- **Caja del earnout [P]:** la nota 2.4 separa «Earnouts and deferred consideration» dentro de «Acquisition of subsidiaries, net of cash acquired», en inversión: 34,4 / 93,9 / 23,3, de los que 31,4 / 83,2 / 19,7 son de Lavartex (DEU24 p.288; URD25 p.342 y p.341). El de México se liquidó en 2024 y 2025 (URD25 p.352).
  - La marca pasa de [I] a [P] en la tabla única, en la tabla de correspondencia y en §5.1.
  - Con esto, V-F1l tiene la ubicación de la caja de N1.
- **Actualización de 2025:** 0,7 (URD25 p.313). La frase «la de 2025 no se publica por separado» se corrige con una nota en la respuesta anterior.
- **La línea fiscal cuadra los tres años** al 25,83 % [D]: −15,834 / +0,801 / −0,232, frente a (15,8) / 0,8 / (0,2).
- **Límite cerrado como sensibilidad, no como regla.** Si la regla fiscal de N1 alcanzara también a la actualización (12,4 / 5,6 / 0,7 fuera del BAI que da el tipo): −0,790 en el flujo sin crecimiento y −1,661 en el año 11 NORMAL [LECTURA]. Reproduce la revisión.

**Pendiente:** las cifras de la actualización están publicadas y comprobadas en su página del PDF, pero no en el CSV verificado. Hasta que pasen el procedimiento del CSV, quedan fuera de N1.

### V4 · menor · alcance de N1 en el τ de cinco años y dependencia de E8.1

**Corregido. Las elecciones quedan para quien decide.**
- **Convención.** La cifra de N1 se declara con su convención (propuesta (5a) y §5.1; E3; E8.1; T16):
  - −11,605 y −18,609 con la convención registrada (cinco años);
  - −9,141 y −15,848 con el τ de la ventana. Con el tipo fijo y la ventana, −9,763;
  - antes de impuestos, 13,966.

  Lo firme es que N1 baja el flujo sin crecimiento entre 9 y 12.
- **Caso fiscal sintético** (`caso_fiscal_N1`): ventana de tres años, cargo no monetario y no deducible de 9, caja 52,5.
  - Con la media de la ventana: N1 sin efecto fiscal y N1 con el tipo fijo dan 52,5; deducir la partida entera da 51,639.
  - Con cinco años y los dos anteriores al tipo legal: N1 sin efecto fiscal da 52,5 y el tipo fijo, 52,844.
  - Con los dos anteriores al 31 %, ninguno da la caja. Es la convención, no N1.
- **Alcance a 2021–22.** Es una opción del texto de (5a): «solo en la ventana 2023–25 / también en 2021–22». Con 2021–22 [LECTURA: (3,0) en URD22 p.285; 2,4 en URD23 p.302]: +0,416 en el flujo sin crecimiento y +0,466 en el año 11 NORMAL (−11,190 y −18,142). Reproduce la revisión.

**Pendiente:** la convención del tipo (E8.1) es política fuera de F1; el alcance, de quien decide (5a).

### V5 · menor · la sensibilidad de 16,8 era solo la de los pagos; faltaba la amortización ROU

**Corregido.**
- **Sensibilidad por partes** (propuesta (1b) y §1; E8.5):

  | | A0 | A1 y A2 |
  |---|---|---|
  | Pagos | −16,778 | −16,778 |
  | Amortización ROU que devuelve f | — | +10,118 |
  | Total | −16,778 | −6,660 |

- **(2)(v) y `perimetro_margen`** (E2) incluyen la amortización ROU: el margen la lleva como proporción constante, la misma que devuelve f.
- **Efectos de escala con su sentido:**
  - PPA, +4,206: sube el flujo sin crecimiento de A2;
  - ROU, −10,118: baja el de A1 y A2;
  - las dos en A2, −5,913.
- V-F1f informa de ellos.
- Cifras de `copia_investigacion_f1.md`, iguales a las de la revisión.

### V6 · menor · dos fórmulas para la misma comprobación del terminal

**Corregido.**
- **Rige la del libro** (Convenciones V6.3 §3; `Diagnóstico V6`, bloque 10): la rentabilidad marginal S2C·m_obj·(1−τ) frente al ROIC, con aviso si el salto supera C179.
  - El libro de Elis da 7,4739 / 10,6770 / 14,4140 % frente a 7 / 10 / 12 %.
  - Saltos de −0,47 / −0,68 / −2,41 puntos; C179 = 0,05 (5 puntos, «ajustable»), leído del libro.
- **V-F1k** bloquea si falta el perímetro del ROIC. Avisa si el salto supera C179, como el libro, e informa si no.
  - No se añade otra comparación ni otro umbral, y no se cambia el vigente.
  - Se elimina «debe justificarse», que no tenía consecuencia: no se crea una obligación nueva de justificar.
- **La igualdad exacta**, con el factor (1+g∞), se informa como precisión (−0,55 / −0,89 / −2,77 puntos). Caso P4e: con el salto nulo del libro, el año 11 cobra (1+g∞) veces ΔV/S2C; diferencia de −0,049 en el ejemplo.
- Escrito igual en la propuesta (severidad y §4), en E4 y en E5.

### V7 · menor · E3 decía «sin cambios en la estructura del flujo» frente a los términos explícitos

**Corregido.** E3 da la fórmula:
- años 1–10: flujo_t = V_t·[m_t(1−τ) − f] − ΔV_t/S2C − X_t;
- año 11: … − X₁₁;
- transición: X_t = T_t si t ≤ H, y 0 después; X₁₁ = 0 si H ≤ 10;
- compras de reposición proporcionales: X_t = a·V_t y X₁₁ = a·V₁₁;
- sin efecto fiscal, como ΔV/S2C, y fuera del ancla (V2).

**Conciliación con la PPA decreciente (E2).** Los términos de E3 son solo de caja (inversión). Una PPA decreciente con A2 exigiría un término no monetario con efecto fiscal nocional, que no está especificado; por eso sigue sin ser admisible.

### V8 · menor · la cota 867,2 era de R_propia más la transición

**Corregido** (propuesta (3a) y §3):
- el capex propio, 867,2, acota R_propia más la transición, no R total;
- el intervalo 736,0–867,2 mide la materialidad bajo la opción B de (4b);
- si alguna compra fuera de reposición, R_compras se añadiría: media de las adquisiciones 127,7; capex propio más adquisiciones, 994,8 [D].

### V9 · menor · controles sintéticos con el ancla a mano, P1 sin crecimiento y N1 sin caso

**Corregido** (`controles_sinteticos_f1.py`; T15 y T8):
- **De extremo a extremo:** ventanas con crecimiento y ancla calculada con la fórmula de E4, anterior y corregida (V2a–V2h).
- **P1 con crecimiento:** V2a–V2e.
- **Compras de reposición como término explícito con el ancla de E4:** V2f y V2g.
- **Terminal:** fórmula del libro (P4e) y senda de `motor_a` (P4f).
- **N1:** caso fiscal sintético con caja conocida y tres convenciones (V4).
- **Guarda V-F1c:** casos en que salta (R_propia 25 frente a 20; R_compras 9 frente a 5) y en que no (R = 20 + 9).
- **Motor sintético.** Sigue la senda de `motor_a`: g15 en los años 1–5, lineal hasta g∞ en los años 6–10; margen lineal de m0 a m_obj en cinco años. Coincide exactamente con él en 4 juegos, con impuestos. La frase de T15 dice ahora su alcance: sin términos explícitos, que `motor_a` no tiene.

### V10 · forma · frases sin sincronizar y rótulos

**Corregido:**
- E4: «salta V-F1g, que bloquea (E5)». E2, matriz: «V-F1a si hay arrendamientos, con cualquier importe (E5)».
- V-F1i: «cuando hay una transición conocida, publicada o documentada aunque sin importe», sin «material».
- «Terminal NORMAL» pasa a «año 11 NORMAL», la variación del flujo del año 11, en la propuesta y en T16. La propuesta lo define al principio. En la respuesta anterior se conserva el texto revisado, y esta nota lo aclara.
- Líneas fiscales con su signo, (15,8) / 0,8 / (0,2), en la propuesta y en una nota de la respuesta anterior.
- «Reparto no publicado [P]» pasa a [B], el resultado de una búsqueda. La marca [B] se define al principio de la propuesta.
- «Coincide con `motor_a»»: con su alcance, en T15 y en una nota de la respuesta anterior.
- Tabla de correspondencia:
  - «de los costes que tocan estas decisiones», con los que quedan fuera;
  - la columna del año 11 de la transición recoge las tres clasificaciones;
  - `en_R` supone proporcionalidad a las ventas (caso V2d);
  - los gastos de transacción de las compras, en su fila.

### V11 · forma · textos de aprobación

**Corregido** (tabla única):
- **(1a)** se limita al arrendamiento y a sus controles: V-F1a, V-F1b y V-F1e. La regla de un solo perímetro es (4a). Cada decisión aprueba sus controles; la lista está bajo la tabla de severidad.
- **(3b)** da las vías como opciones:
  - pedir el dato, por quien designe la persona responsable;
  - buscar en fuentes públicas que no están en la base;
  - encargar una estimación documentada con las exigencias de V-F1d;
  - mantener el bloqueo.
- **(4b)** queda con dos textos, A y B, y el fundamento corregido por V1.

## 3. Pendientes

| Pendiente | Clase | Qué impide | Quién |
|---|---|---|---|
| M1: reparto del capex propio y del plan climático (importe, horizonte y finalidad) | Dato | R, f, el flujo de partida y el ancla de Elis; clasificar la transición | (3b) |
| M2: tasa de bajas y desembolso por cliente nuevo | Dato | La parte de R_propia que repone clientes | (3b) |
| M6: finalidad de las compras pequeñas y crecimiento orgánico sin ellas | Dato | (4b): con la opción A, V-F1j bloquea | (3b) o (4b) |
| N2: fiscalidad, caja y reposición de las bajas de 2025 | Dato | La normalización de N2 | — |
| Actualización del earnout y ajustes de 2021–22 en el CSV verificado | Procedimiento | Incluirlos en N1 si se aprueba su alcance | Frente E, con encargo |
| Convención del τ de proyección (E8.1) | Política, fuera de F1 | La cifra de N1: −11,6 o −9,1 | Persona responsable |
| Alcance de N1 (2021–22) | Política | Su cifra, ±0,4 | Persona responsable (5a) |
| Perímetro de las palancas S2C y ROIC de Elis | Juicio de la fase C, con R | V-F1g y V-F1k | Fase C |
| Umbral de V-F1a, si se quiere | Política | Nada: sin umbral, bloquea | Persona responsable |
| Revisión externa de estas correcciones | Revisión | Sin ella, no están revisadas | Persona responsable |

## 4. Manifiesto y recuperación

- `MANIFIESTO_SHA256.txt` regenerado en cada bloque; `sha256sum -c` OK.
- Punto de recuperación: [PUNTO_DE_RECUPERACION.md](PUNTO_DE_RECUPERACION.md).
- Estado de las revisiones: [revision/ESTADO.md](revision/ESTADO.md).
- Configuración: [REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md).
- Nada se ha fusionado a `main`.
