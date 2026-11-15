# Viscofan · descomposición de +1,5386 € y −0,6623 € (encargo de cierre §7; S10)

**Qué es.** Explica el cambio del precio de Sí de Viscofan entre la 4.12 (39,2877 €) y la 4.13 (40,1640 €). Separa los cambios, sus causas, la dependencia del orden y las interacciones.
- Usa **solo** contrastes y libros existentes: los vectores de escenarios (V MALO, NORMAL y BUENO) ya calculados con LibreOffice en el paquete, y las fases B de la 4.12 y de la 4.13.
- La parte de la descomposición que no se puede separar sin recalcular se especifica en §5 para que la ejecute el integrador.
- No se ha ejecutado LibreOffice.

**Base y autoría.** 4.13 (`b1f747a1…f22a`); agente del frente B; trabajo **interno**. `E413/` = `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/`.

**Script y salida.** `agentes/B/scripts/descomposicion_viscofan.py`, que lee los dos `configuracion_v64_variantes.json` y aplica la fórmula cerrada de `precio_de_si.p_estrella` con k = 3, copiada literalmente. Salida: `agentes/B/descomposicion_viscofan_calculo.json`.

---

## 1. Por qué se puede descomponer sin LibreOffice (hecho)

El precio de Sí es una función **solo** del vector de valores de escenario V y de las probabilidades p: `p_estrella(V, p, k = 3)`, en `personaje_v2/scripts/precio_de_si.py`.
- Las probabilidades no entran en el cálculo de V.
- Cada escenario depende solo de sus propias palancas.

Por tanto, cambiar las probabilidades sobre un V ya calculado da el precio de Sí **exacto**, sin recalcular el libro. Además, si las palancas de un escenario no cambian, su V tampoco: V NORMAL es idéntico en la 4.12 y en la 4.13 (44,8547080140724 con «Caja» y 44,1839566126552 con NIIF 16).

En el tramo que aplica aquí (el MALO, por debajo de P\*):

> P\* = (p_N·V_N + p_B·V_B + 3·p_M·V_M) ÷ (p_N + p_B + 3·p_M)

| Probabilidades | Peso de V MALO | Peso de V NORMAL | Peso de V BUENO |
|---|---|---|---|
| 4.12 · 0,25 / 0,60 / 0,15 | 0,500 | 0,400 | 0,100 |
| 4.13 · 0,20 / 0,60 / 0,20 | 0,429 | 0,429 | 0,143 |

## 2. Las cuatro esquinas calculadas (hechos)

| Esquina | Palancas | Perímetro | Origen en el paquete | V MALO / NORMAL / BUENO | Precio de Sí |
|---|---|---|---|---|---|
| A | 4.12 | «Caja» | `E413/viscofan/antecedentes/ejecucion_1_4_13/configuracion_v64_variantes.json`, variante `perimetro_alternativo` (= 4.12 exacta, `comparacion_4_12_4_13.md`) | 30,6925 / 44,8547 / 59,9959 | **39,2877** |
| B | 4.12 | NIIF 16 | ídem, activa de la ejecución 1 | 30,0409 / 44,1840 / 59,2220 | **38,6162** |
| C | 4.13 | «Caja» | `E413/viscofan/Viscofan/configuracion_v64_variantes.json`, `perimetro_alternativo` | 30,6407 / 44,8547 / 59,2983 | **40,8263** |
| D | 4.13 | NIIF 16 | ídem, activa (expediente vigente) | 30,0158 / 44,1840 / 58,5486 | **40,1640** |

**Palancas que cambian de A/B a C/D** (`E413/viscofan/antecedentes/fase_b.json.4_12`, `…/ejecucion_1_4_13/fase_b.json` y `E413/viscofan/Viscofan/fase_b.json`; las demás son iguales):

| Palanca | 4.12 | 4.13 | Referencia mecánica 4.12 → 4.13 |
|---|---|---|---|
| Crecimiento de los años 1–5, MALO (Palancas!B14) | 0,010 | 0,015 | −0,01 → −0,01 |
| S2C MALO (B16) | 0,9 | 0,8 | 0,9 → 0,8 |
| S2C BUENO (D16) | 1,4 | 1,3 | 1,4 → 1,3 |
| Probabilidades (Análisis!B69:D69) | 0,25 / 0,60 / 0,15 | 0,20 / 0,60 / 0,20 | 0,20 / 0,60 / 0,20 → igual |

## 3. Causas de cada cambio (hechos e interpretación)

**S2C del MALO y del BUENO: corrección R6 (hecho).**
- La referencia mecánica pasó de anclarse en Historia!C53 (1,146, perímetro «Caja») a Configuración V6.4!B155 (1,060, NIIF 16). `referencias_mecanicas.json` da la regla «MALO = 0,75 × NORMAL; BUENO = 1,25 × NORMAL».
- En la 4.12, 0,75 × 1,146 = 0,86 y 1,25 × 1,146 = 1,43, que redondean a 0,9 y 1,4. En la 4.13, 0,75 × 1,06 = 0,795 y 1,25 × 1,06 = 1,325, que redondean a 0,8 y 1,3.
- Los dos agentes adoptan la referencia. El S2C NORMAL redondea a 1,1 con las dos anclas (S4).
- **Es el efecto de una corrección**, aunque su valor lo eligiera un agente nuevo.

**Crecimiento del MALO: juicio con la misma evidencia (hecho e interpretación).**
- Los dos textos citan el mismo dato, «Historia C45 = 1,4 %», el peor tramo de tres años. Uno toma 1,0 % y el otro 1,5 %.
- Interpretación: es un redondeo distinto de la misma cifra (1,4 → 1,0 o 1,5), no una lectura distinta de los hechos.

**Probabilidades: desacuerdo argumentado (hecho).**
- El agente de la 4.12 se desvía de la convención 0,2/0,6/0,2 a 0,25/0,6/0,15. Su razón: el MALO «es la continuación de lo que ya pasa (… C27 = Comprimiendo) y su mecanismo estaba en marcha», y el BUENO «es la historia menos probada».
- El de la 4.13 vuelve a la convención: «subir también su probabilidad castigaría dos veces el mismo riesgo»; el 14 % del MALO «ya está por debajo de todo lo observado».
- Interpretación: no es una variación espontánea. Son dos juicios económicos opuestos sobre el doble castigo, los dos con hechos de la empresa.

**Por qué el agente nuevo pudo cambiarlo (hecho).**
- Para corregir R6 no se cambió solo el S2C: se rehízo la fase B entera con un agente nuevo (relevo 16, `E413/resultados/relevos_agentes_4_13.md`), que tenía la fase B anterior como antecedente con la instrucción «no la copies».
- La corrección expuso a un juicio nuevo todas las palancas.

**Fase A (hecho).**
- Cambió C97 de «Neutral» a «Comprando» (corrección de un error de lectura), Palancas!C5 de «Madura en crecimiento» a «Madura» y los textos de los escenarios.
- Ninguna de esas celdas mueve V: V NORMAL es idéntico.
- No se puede establecer si influyeron en el juicio de probabilidades de la fase B.

## 4. Descomposición [cálculo B]

### 4.1 Total y bloques

| Paso | Efecto en el precio de Sí |
|---|---|
| A → D (total) | **+0,8763** |
| A → C: palancas con «Caja» (el +1,5386 del informe) | +1,5386 |
| B → D: palancas con NIIF 16 | +1,5478 |
| C → D: perímetro con las palancas de la 4.13 (el −0,6623 del informe) | −0,6623 |
| A → B: perímetro con las palancas de la 4.12 | −0,6715 |
| **Interacción perímetro × palancas** | **+0,0091** (= −0,6623 − (−0,6715)) |

La interacción es pequeña. La dependencia del orden del par perímetro/palancas es de 0,009 €.

### 4.2 Dentro de las palancas (Shapley sobre tres factores; los seis órdenes están en el JSON)

| Factor | Con «Caja» (A → C) | Rango según el orden | Con NIIF 16 (B → D) | Rango según el orden | Causa |
|---|---|---|---|---|---|
| **Probabilidades** | **+1,6474** | +1,6306 … +1,6642 | **+1,6412** | +1,6258 … +1,6565 | juicio (convención frente a desviación) |
| V BUENO (solo S2C 1,4 → 1,3) | −0,0847 | −0,0698 … −0,0997 | −0,0818 | −0,0673 … −0,0962 | R6 |
| V MALO (crecimiento 1,0 → 1,5 % **y** S2C 0,9 → 0,8, juntos) | −0,0240 | −0,0222 … −0,0259 | −0,0116 | −0,0107 … −0,0125 | redondeo + R6 (no separables sin recálculo) |
| Total | +1,5386 | | +1,5478 | | |

**Cambio de los valores de escenario.**

| Perímetro | Δ V MALO | Δ V NORMAL | Δ V BUENO |
|---|---|---|---|
| «Caja» | −0,0518 | 0 | −0,6977 |
| NIIF 16 | −0,0250 | 0 | −0,6734 |

El Δ V BUENO pesa poco en P\* (peso 0,10–0,14). El Δ V MALO pesa mucho (0,43–0,50), pero es pequeño porque las dos palancas del MALO tiran en sentidos opuestos: más crecimiento sube V y un S2C menor lo baja.

### 4.3 Cruces exactos (otros órdenes, sin LibreOffice)

| V de la esquina | con p de la 4.12 | con p de la 4.13 |
|---|---|---|
| A (palancas 4.12, «Caja») | 39,2877 | 40,9482 |
| B (palancas 4.12, NIIF 16) | 38,6162 | 40,2709 |
| C (palancas 4.13, «Caja») | 39,1920 | 40,8263 |
| D (palancas 4.13, NIIF 16) | 38,5364 | 40,1640 |

**Lectura (interpretación).**
1. El bloque de +1,5386 € es, en un **107 %**, el cambio de probabilidades: entre +1,63 y +1,66 € según el orden.
2. Las demás palancas del bloque restan juntas entre 0,09 y 0,13 € con «Caja» y entre 0,08 y 0,11 € con NIIF 16, según el orden. La corrección R6 (S2C) es negativa: de −0,07 a −0,10 € en el BUENO, más su parte del MALO, que no se puede separar sin recálculo.
3. Atribuir el bloque entero a la «variación espontánea entre agentes» sería inexacto por los dos lados:
   - la parte del S2C es una **corrección** (R6);
   - la parte grande, la de las probabilidades, es un **desacuerdo de juicio argumentado**, no ruido.
4. El perímetro (−0,66 a −0,67 €) es estable entre los dos juegos de palancas.
5. **R6 aplicada sola** (cambiar solo el S2C en una rama y conservar las demás palancas de la 4.12; encargo §7, «sin compensarlos cambiando otras palancas»). Con lo calculado, su efecto **no se puede acotar del todo**:
   - la parte del BUENO es exacta: −0,067 € con las probabilidades de la 4.12 (0,1 × −0,6734, NIIF 16);
   - la parte del MALO no. El Δ V MALO observado (−0,025) suma un efecto positivo del crecimiento y uno negativo del S2C, y cada uno por separado puede ser mayor que la suma.

   Lo que sí se sabe: el efecto conjunto «S2C (R6) + crecimiento del MALO» es de −0,08 a −0,13 € según el perímetro y el orden, y el de R6 sola es negativo y como mínimo del orden de la parte del BUENO. La cifra exacta exige el recálculo de §5 (copia m2).
6. Con las probabilidades de la 4.12 y todas las palancas nuevas, el precio de Sí sería 38,5364 € (cruce D con p de la 4.12, exacto), frente a 40,1640 €.

### 4.4 Consecuencias

- **Para S10.** El rango calculado de las variantes (38,47–43,39 €) **no** recoge la variación de probabilidades. Un contraste «probabilidades de referencia» la recogería de forma exacta y barata: decisión D7, en `decisiones_pendientes.md`.
- **Para el procedimiento.** Una corrección mecánica de referencias (como R6) debería aplicarse en una rama que cambie solo las palancas afectadas. El rehacer completo con un agente nuevo debería ir aparte, con su efecto mostrado por separado. Es una elección de procedimiento (convención), no un cambio de criterio.

## 5. Recálculo necesario para separar el MALO (especificación para el integrador; **no ejecutado**)

**Objetivo.** Separar Δ V MALO (−0,0518 con «Caja»; −0,0250 con NIIF 16) en crecimiento del MALO (Palancas!B14) y S2C del MALO (Palancas!B16), y comprobar que Δ V BUENO es solo D16.

**Libros de partida** (solo lectura; trabajar sobre copias):

| Perímetro | Libro | SHA-256 | Confirmado con openpyxl (B146 · B14 · B16 · D16 · B69:D69) |
|---|---|---|---|
| NIIF 16 | `E413/viscofan/Viscofan/variantes_v64/activa.xlsx` | `44d4edc7301a0726572b7690874f7aad8bc5d79d0f481b9351d4b2a790467951` | «NIIF 16 · …» · 0,015 · 0,8 · 1,3 · 0,2/0,6/0,2 |
| «Caja» | `E413/viscofan/Viscofan/variantes_v64/perimetro_alternativo.xlsx` | `e2ab9c120e0befcef4f5cb9ed9a2ea7a71768998a0acb0a262fdff9571bf453a` | «Caja · capex de caja frente a toda la D&A (V6.4)» · 0,015 · 0,8 · 1,3 · 0,2/0,6/0,2 |

**Copias y celdas.** Para cada libro de partida, las copias de la tabla, con las celdas como valores numéricos. Si el expediente tiene el escritor de celdas del pipeline, usar el mismo con el que `variantes_configuracion_v64.py` escribe las variantes. Si no, openpyxl, conservando el libro, y comprobar después que solo cambiaron esas celdas.

| Copia | Cambios | Para qué |
|---|---|---|
| m1 | Palancas!B14 = 0,01 | V MALO con el crecimiento de la 4.12 y el S2C de la 4.13 |
| m2 | Palancas!B16 = 0,9 | V MALO con el crecimiento de la 4.13 y el S2C de la 4.12 |
| b1 | Palancas!D16 = 1,4 | V BUENO con el S2C de la 4.12 (comprobación: tiene que dar el V BUENO de A o B) |
| ctl | B14 = 0,01; B16 = 0,9; D16 = 1,4; Análisis!B69 = 0,25, C69 = 0,6, D69 = 0,15 | control: tiene que reproducir A (39,2877008705) o B (38,6162260536) a 10 decimales |

**Orden.** Siempre en secuencia, nunca dos LibreOffice a la vez:
1. `bash personaje_v2/scripts/recalc.sh <copia> <dir_recalc> <perfil>`, con un perfil propio y nuevo.
2. `python3 personaje_v2/scripts/leer_resultados.py <dir_recalc>/<copia> <copia>.resultados.json --exigir-recalculo-forzado`.
3. `python3 personaje_v2/scripts/precio_de_si.py <copia>.resultados.json <copia>.precio.json --k 3`.

Primero ctl, para validar el procedimiento; después m1, m2 y b1. Son 4 × 2 = 8 recálculos.

**Lectura.** Con los V MALO de m1 y m2 y los de la esquina, el script de B (función `p_estrella`) da los efectos del crecimiento y del S2C del MALO en los dos órdenes y su interacción, con cualquier juego de probabilidades, sin más recálculos.

**Criterio de aceptación.**
- ctl reproduce la esquina.
- b1 reproduce el V BUENO de la esquina antigua (59,9959132127 con «Caja»; 59,2219987881 con NIIF 16).
- Si b1 no lo reproduce, en el BUENO cambió algo más que el S2C, y hay que investigarlo antes de atribuir nada.

**No hace falta recalcular nada para separar las probabilidades** (§4.2–4.3): es exacto.
