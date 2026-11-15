# P-M1 · Reposición de Vidrala frente a la amortización del modelo · entrega 4.8

Redactado por Claude (Opus) el 10-nov-2026 para el encargo 4.8, §3. Es una declaración de Claude, con una crítica independiente hecha con Fable (§8) y revisada por la auditoría interna (§8b). Nada está comprobado externamente. El documento distingue:
- **hechos publicados** (con archivo y página);
- **cálculos derivados**;
- **hipótesis**;
- **decisiones humanas**, que siguen sin tomar.

**Aviso de alcance.** Todas las cifras son resultados mecánicos de un ensayo con base económica a 31-dic-2025, motor B y la combinación T1·M1·R1 propuesta en la 4.7. No son comparables con el precio de 87,9 del 3-nov-2026, no son recomendaciones de compra ni de espera y no sirven para fijar el tamaño de una cartera. Las alternativas no son cotas ni previsiones.

**Constantes sin cambios:**
- r = 0,09; probabilidades 0,2 / 0,6 / 0,2; k = 3;
- caja 108,352, sin volver a restar los 43,338;
- puente 160,784; 35,206 millones de acciones;
- palancas de la fase B.

Las únicas diferencias de fórmula frente a la 4.7.1 son las que introduce cada alternativa, y están en `scripts/analisis_pm1.py`.

## 1. Respuesta corta

1. **«Reposición = amortización» no tiene respaldo.** Los indicios conservados apuntan a una reposición mayor que la amortización: la inversión la supera desde 2017, y el cociente λ entre reposición y amortización va de 1,05 a 1,29 según el indicio y sus supuestos (§3 y §5). La hipótesis central se fija en 1,15 (P1), con el mínimo indicado cerca de 1,10 (P1b). Pero la evidencia pública **no separa** reposición, ampliación, eficiencia y descarbonización, para ningún año.
2. **La sensibilidad de −20,6 puntos de la 4.7.1 no es una alternativa coherente.** Unos 309 de los 555 M€ que añade en diez años en el NORMAL, y 463 en el BUENO, ya los pagaba la inversión fija neta del modelo. El S2C de referencia trata el exceso histórico de la inversión sobre la amortización como reinversión. En torno a la mitad de su efecto sobre el ponderado es doble cómputo (§5.2).
3. **Las alternativas coherentes** (con la «regla del hueco», que no cobra dos veces) dan:

   | Rango | Ponderado | Precio de Sí |
   |---|---|---|
   | Alternativas fundamentadas (P0, P1, P6m, P5) | de 69,73 a 62,71 | de 64,75 a 55,83 |
   | Incluido el extremo explorado (nivel de 2025 perpetuo) | hasta 55,70 | hasta 50,25 |
   | Referencia | 69,24 | 64,26 |

   Son rangos explorados, no límites demostrados.
4. **Lo que decide dónde cae el valor no es público:** qué parte de la inversión de 2021–2025 es reposición o competitividad obligada y qué parte es ampliación (Q-E1 y Q-E2). Mientras falte, P-M1 sigue siendo una **incertidumbre material** para una valoración financieramente validada. El bloqueo se reduce y se acota en su forma, pero no desaparece.

## 2. Fuentes y búsqueda

**Conservadas en el paquete** (todas se vuelven a extraer en el guion, con archivo, página y patrón; 94 de 94 se reproducen: `financiero/pm1_evidencia.json`):
- los textos `CF_2016`…`CF_2025.txt` del expediente de referencia, que son las cuentas consolidadas en inglés;
- el **PDF español de 2025** (`contrastes/piloto_Vidrala_2025/fuentes/es_2308…pdf`, SHA-256 `29fd6a29…`). Tiene 372 páginas: cuentas, informe de gestión, informe de sostenibilidad y taxonomía. En la 4.7.1 no se usó más allá de las cuentas.

En las tablas, las citas O\* y S\* son **declaradas por Claude y no reproducibles con el paquete**, porque sus PDF no están en él. Las de 2026 están marcadas como posteriores a la base.

**Externas oficiales:** presentaciones de resultados e informe de gestión remitidos a la CNMV entre 2024 y 2026 (O1–O11 en `fuentes/fuentes_externas_pm1.json`, con URL, fecha, huella, página y cita).
- Se leyeron con el navegador del equipo de la persona responsable: el entorno de Claude no puede descargar de la CNMV.
- **Los PDF no se conservan en el paquete.**
- Las fechadas después del 31-dic-2025 se marcan como posteriores a la base y no se mezclan con sus saldos.

**Externas secundarias** (no fundamentan nada por sí solas):
- S1: transcripción de la conferencia de resultados de 2025;
- S2: Caudete;
- S3: Llodio.

**X-e, comprobado directamente en el PDF** [Claude]. La depreciación de derechos de uso es:
- **6,760** en 2025;
- 4,768 en 2024.

Consta en la p. 58 del PDF español (misma línea, 2025 y 2024) y en la versión inglesa. El informe del N3 de la 4.7.1 (§3, «Límites en el otro sentido») citaba la de 2024 como si fuera la del año. La presentación por período correcta es la de este párrafo; el informe de la 4.7.1 se conserva intacto como antecedente. **Discrepancia documental nueva:** en el PDF inglés, la tabla de la p. 69 rotula «as of 31 December 2024» unos importes que son los de 2025.

**No encontrado en ninguna fuente pública consultada:**
- el desglose de la inversión entre reposición, ampliación, eficiencia y descarbonización;
- el inventario de hornos con su última reconstrucción, campaña y capacidad;
- el calendario de reconstrucciones obligatorias frente a aplazables;
- una cifra oficial de inversión para 2026.

La taxonomía de la UE no ayuda: solo el 1 % de la inversión es elegible (PDF, p. 205).

## 3. Matriz de conceptos (hechos, cálculos e interpretaciones)

| Concepto | Hecho publicado (fuente) | Cálculo o interpretación | Clasificación |
|---|---|---|---|
| Composición de la amortización de 2025 (132,948) | Material 118,275 (p. 49); intangibles 7,913, de ellos cartera de clientes 4,492 (p. 52); derechos de uso 6,760 (p. 58) | La suma cuadra con 132,948 | hecho |
| Cartera de clientes | Valor neto 21,858 a 31-dic-2025 (p. 52) | No se repone; el modelo la cobra como inversión. Se agota en unos 4,9 años | hecho → **P0** |
| Derechos de uso | 6,760; altas del pasivo 2,404 y otros 9,596 (p. 58) | El modelo cobra la depreciación como reposición. Equivale a los arrendamientos nuevos, que no están en el FCF ni en el puente: es coherente y no se cambia | interpretación |
| Inversión de caja frente a amortización propia | 188,503 frente a 121,696 (material + intangibles − cartera) | 1,549 (frente a 1,418 con la amortización total). Comparar la inversión de caja con la amortización total infravalora el exceso | cálculo |
| Reparación y mantenimiento | 41,854 de gasto en 2025 (4.7.1); costes posteriores capitalizados solo si generan beneficios futuros (p. 21) | Ya está en el EBIT: no se resta otra vez | hecho |
| Vida útil contable frente a campaña | Hornos, instalaciones y maquinaria, 8–16 años (p. 21); vida contable media implícita ≈ 11,5 años (coste aún en amortización ÷ dotación) | La duración real de las campañas no se publica | hecho / insuficiente |
| Bienes totalmente amortizados en uso | 182 (2016) → 207 → 362 → 408 → 413 → 457 → 500 → 543 → 706 (2024) → 627 (2025) M€; el 28,6 % del coste bruto | Indican cohortes agrupadas y una ola de reposición, con una amortización de 2025 que no es estacionaria. No miden λ | hecho / interpretación |
| Destino de la inversión | 2017–2018 Italia; 2018–2022 Reino Unido; 2019–2023 Portugal («complete update»); 2024–2025 «primarily in the renewal of furnaces» en España, Portugal y Reino Unido (p. 50); tres hornos nuevos en 2025 (p. 177); paradas y arrancadas (p. 176) | Programa rotatorio de renovación por plantas. «Primarily» no excluye ampliación | hecho / interpretación |
| Ampliación dentro de la renovación | Brasil: «capacity expansion» (O5); Llodio +capacidad (S3); Caudete +10 % (S2, 2026) | Reposición y crecimiento van en los mismos proyectos | hecho (oficial) / indicio (secundario) |
| Descarbonización | Electrificación del 10–15 %, del 25 % en hornos nuevos y objetivo del 40 % en 2030 (p. 173); PERTE 10,298 + 6,316; subvenciones diferidas 23,115 (p. 51) | Coste real de conservar competitividad que λ no mide (→ P6) | hecho / interpretación |
| Obligatoria frente a aplazable | Compromisos 66,610 (p. 51); plan «ambicioso» ≈ 12 % de las ventas previsto para 2025 (O6) y ≈ 13 % realizado (O1, posterior a la base) | El plan se presentó como extraordinario. No hay plazos acreditados | insuficiente |
| Capacidad frente a ventas | Ventas orgánicas 2025 −5,4 % (p. 88); volúmenes Iberia −0,1 %, Reino Unido −5 %, Brasil −0,8 % (S1); «adaptando nuestra capacidad industrial» (p. 94); reestructuración del Reino Unido 13,668 (p. 34); volúmenes Q1 / Q2 2026 −2,9 % / −0,6 % (O10, posterior) | La caída de 2025 fue sobre todo de precio: no hay capacidad ociosa grande, y en el Reino Unido se adaptó a la baja | indicio |
| Perímetro | Italia hasta 2024; Brasil desde noviembre de 2023; The Park (Reino Unido) en 2023 | Las ratios del grupo mezclan perímetros; los segmentos lo limitan en parte | hecho |
| Definición de la amortización de 2019 (**Y-1, nuevo**) | 91,088 en el estado de flujos del informe 2019; deterioro 6,003 aparte | La Historia usa 97,091 = amortización + deterioro, una definición distinta de la del resto de años (por el comparativo de 2020). Afecta a la ratio de 2019 (1,10 frente a 1,18) y a la fila 30 de 2019, fuera de la ventana de C53. No cambia valores. No se corrige: está en el expediente vigente | hallazgo documental |

## 4. Conciliación por año y por segmento (`financiero/pm1_conciliacion_anual.csv`, `pm1_segmentos.csv`)

**Grupo (Historia).** Inversión ÷ amortización:

| 2016 | 2017 | 2018 | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|---|---|
| 0,73 | 1,16 | 1,15 | 1,10* | 1,60 | 1,27 | 1,41 | 1,74 | 1,43 | 1,42 |

(*) Con la definición de Y-1.

- Inversión ÷ ventas: media del 10,6 %, entre el 7,1 % y el 13,6 %.
- Exceso medio 2021–2025: 45,9 M€/año. En 2025: 55,6.

**Segmentos.** Inversiones del ejercicio ÷ amortización:

| Segmento | 2019 | 2020 | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|---|---|
| Iberia y resto | 1,14 | 1,77 | 1,78 | 2,31 | 2,51 | 2,32 | 2,02 |
| Reino Unido e Irlanda (2018: 1,18) | 1,52 | 1,72 | 0,91 | 1,54 | 0,65 | 0,82 | 0,87 |
| Brasil | — | — | — | — | — | 1,30 | 1,04 |

- **Reino Unido, ciclo 2018–2025:** 1,095 (1,113 con la cifra de 2018 de su propio informe).
- **Iberia, 2019–2025:** 1,97.

**Interpretación.** El exceso del grupo se concentra en la ola de Iberia, la de Portugal desde 2019 y la de España desde 2024. El Reino Unido terminó la suya en 2022 y desde entonces invierte por debajo de su amortización. Las limitaciones de ese tramo:
- la amortización del Reino Unido sube con The Park (2023);
- la reestructuración de 2025 reduce capacidad;
- ocho años no cubren una campaña de 8–16.

El ciclo del Reino Unido es, por tanto, un indicio débil de λ (crítica independiente, §8).

## 5. Traducción al modelo

### 5.1 Identidades y dónde está la reposición

- FCF = NOPAT + D&A − inversión bruta − Δcirculante.
- Reinversión total = inversión fija neta + Δcirculante.

`pm1_anio_a_anio.csv` comprueba la identidad en todas las filas de todas las alternativas, con la inversión bruta de caja (sin la cartera, que no se repone).

En el motor B el margen EBIT ya descuenta la amortización. El FCF solo resta la reinversión neta: ΔV ÷ S2C en los años 1–10 y g ÷ ROIC_lp × NOPAT en el terminal. Por tanto, **la reposición implícita es D&A + inversión fija neta**, no D&A sola:
- en el NORMAL, la referencia ya invierte 1,21 × D&A el año 1;
- en el BUENO, 1,33 × D&A;
- en el MALO con R1, la inversión fija neta es 0 durante los diez años: es el único escenario con «reposición = D&A» literal.

### 5.2 Doble cómputo

- El S2C de referencia (C53 = 0,9159) es ΔVentas 2020–2025 ÷ Σ reinversión neta total 2021–2025. Esa reinversión incluye el exceso de la inversión sobre la amortización, 229,4 M€ en esos cinco años. El S2C de la fase B (0,9 / 0,9 / 1,0) se ancla en él.
- Añadir encima un mantenimiento fijo cobra dos veces la parte que el modelo ya reinvierte con el crecimiento nominal.
- **Regla del hueco** (todas las alternativas nuevas): se añade solo lo que falta sobre la inversión que el modelo ya hace, cada año y en el terminal, es decir, max(0, requisito − inversión fija neta del modelo).
- **Cuantificación en X41**, la sensibilidad de la 4.7.1:
  - ya pagados: 309,3 de 555,5 en el NORMAL y 462,6 en el BUENO;
  - la parte no duplicada es P5x0 (el mismo nivel con hueco y sin P0): −10,21 puntos frente a −20,64, es decir, alrededor del 51 % de su efecto es doble cómputo.
- **Dominio de la regla** (auditoría interna, Z-c). La regla vale para la inversión fija neta que paga el crecimiento nominal de una base conservada. No vale para la que reconstruye una capacidad que no se conservó. Por eso, en P3 y P4 solo se descuenta la inversión fija de R1.

### 5.3 Impuestos, evolución de D&A y terminal

- **Desfase estacionario (P1):** sin escudo fiscal adicional. En estado estacionario la amortización de coste histórico va por detrás del coste corriente y ese desfase no se recupera fiscalmente.
  - Límite (crítica, M2): en el MALO la amortización no crece y los adicionales generarían algo de escudo. Es una omisión prudente, de unos +0,3–0,4 €/acción en el V MALO.
- **Ola temporal (P2):** escudo diferido al tipo T1, en 12 años.
- **Margen y D&A** (crítica, M1). No hay doble cómputo entre λ y el margen. Pero con más inversión subirá la amortización:
  - 208,5 M€ en curso, que entrarán en uso;
  - la amortización sobre ventas pasó del 6,1 % (2023) al 9,1 % (2025);
  - un margen EBIT del 18 % en el NORMAL exige entonces un EBITDA del 27–28 %, dentro de lo histórico (25,3 / 28,6 / 30,1 %). Se declara como condición del margen M1, no se cambia.
- **Convención de D&A:** constante en los años 1–10 y proporcional a las ventas en el año 11. No cambia P1 (crítica, M4).
- **Terminal.** El requisito se compara con la inversión fija del año 11, que es g ÷ ROIC × NOPAT menos el circulante:
  - en P1 solo aparece un adicional en el MALO: 3,0 con λ = 1,15 y 15,8 con 1,25;
  - en P5, en los tres escenarios: 29,9 / 18,2 / 7,6;
  - **punto frágil (crítica, I2):** en el terminal del MALO la holgura entre la inversión fija y el requisito es de unos 3,5 M€ con λ = 1,10.

### 5.4 Capacidad (R1)

R1 supone capacidad conservada para la recuperación. Los indicios son mixtos:
- la caída de 2025 fue sobre todo de precio, así que no demuestra capacidad ociosa disponible;
- el Reino Unido redujo capacidad y plantilla.

La variante «capacidad no conservada» en el MALO (P3) paga en los años 8–10 la inversión fija que recupera ventas (2,7 / 8,0 / 13,4) **además** de la reposición. Resultado: el V MALO pasa de 48,21 a 47,89 (−0,32), el ponderado a 68,85 (−0,07) y el precio de Sí a 62,87 (−0,13), en línea con los −0,31 de la 4.7.1.
- **Corrección.** En la primera versión, la regla del hueco descontaba esa inversión de la reposición y daba P3 = P1, y el informe lo atribuía, por error, a que las ventas apenas se recuperan (auditoría interna, Z-c).
- **Lectura.** La capacidad tiene un efecto pequeño en este modelo, porque el MALO se recupera poco. La reposición pesa mucho más.

## 6. Alternativas y resultados (`financiero/pm1_alternativas.csv`)

Fundamentos fijados antes de calcular (`ALTERNATIVAS` en el guion). λ central y P5–P6 se revisaron tras la crítica independiente y antes de redactar este informe (§8).

| Clave | Tratamiento | V MALO / NORMAL / BUENO | Ponderado (Δ) | Precio de Sí (Δ) | Peso terminal | Clase |
|---|---|---|---|---|---|---|
| REF | =D&A (4.7.1) | 51,81 / 69,78 / 85,08 | 69,24 | 64,26 | 0,42 / 0,52 / 0,57 | referencia, no respaldada |
| P0 | cartera no repuesta | 52,30 / 70,27 / 85,56 | 69,73 (+0,49) | 64,75 (+0,49) | 0,42 / 0,52 / 0,56 | respaldada con alcance y límites |
| **P1** | λ = 1,15 con hueco + P0 | 48,21 / 70,27 / 85,56 | **68,92 (−0,33)** | **63,00 (−1,26)** | 0,44 / 0,52 / 0,56 | hipótesis condicionada (central) |
| P1b | λ = 1,10 | 49,89 / 70,27 / 85,56 | 69,25 (+0,01) | 63,72 (−0,54) | 0,44 / 0,52 / 0,56 | sensibilidad |
| P1a | λ = 1,25 | 43,72 / 69,86 / 85,56 | 67,78 (−1,47) | 60,90 (−3,36) | 0,44 / 0,52 / 0,56 | sensibilidad |
| P1s | S2C reestimado + reposición explícita | 48,21 / 67,59 / 83,40 | 66,88 (−2,37) | 61,54 (−2,72) | 0,44 / 0,54 / 0,58 | contraste de estructura |
| P2 | P1 + ola 2026–2027 | 47,14 / 69,51 / 85,32 | 68,20 (−1,05) | 62,18 (−2,08) | 0,45 / 0,52 / 0,57 | condicionada (secundaria, posterior) |
| P3 | P1 sin capacidad en el MALO | 47,89 / 70,27 / 85,56 | 68,85 (−0,39) | 62,87 (−1,40) | 0,44 / 0,52 / 0,56 | condicionada |
| P4 | λ = 1,25 + ola + sin capacidad | 42,77 / 69,22 / 85,32 | 67,15 (−2,09) | 60,19 (−4,08) | 0,45 / 0,52 / 0,57 | sensibilidad |
| **P5** | exceso medio 2021–2025 sobre la amortización repuesta (47,8), en nivel, con hueco + P0 | 38,65 / 63,72 / 83,70 | **62,71 (−6,54)** | **55,83 (−8,43)** | 0,44 / 0,52 / 0,56 | hipótesis condicionada |
| P5x | exceso de 2025 sobre la amortización repuesta (60,0), en nivel, con hueco + P0 | 34,46 / 58,63 / 78,06 | 57,68 (−11,56) | 51,05 (−13,21) | 0,44 / 0,51 / 0,55 | sensibilidad |
| **P6m** | suelo del 10,6 % de las ventas, con hueco + P0 | 47,89 / 68,36 / 83,82 | **67,36 (−1,88)** | **61,80 (−2,46)** | 0,44 / 0,53 / 0,57 | hipótesis condicionada |
| P6i | suelo del 12 % (previsión oficial de 2025, O6) | 41,04 / 61,95 / 79,74 | 61,33 (−7,92) | 55,53 (−8,73) | 0,43 / 0,55 / 0,60 | sensibilidad |
| P6x | suelo del 12,9 % perpetuo (nivel de 2025) | 36,64 / 56,23 / 73,16 | 55,70 (−13,54) | 50,25 (−14,01) | 0,43 / 0,55 / 0,60 | extremo explorado, no cota |
| X41 | +41,8 % de D&A en todo, sin hueco (4.7.1) | 32,51 / 49,03 / 63,43 | 48,61 (−20,64) | 44,01 (−20,25) | 0,40 / 0,53 / 0,58 | con doble cómputo (≈ 51 %) |

La medida auxiliar P5x0 (exceso de 2025 sobre la amortización total, sin P0) da 59,04 y 52,31. Solo sirve para medir el doble cómputo de X41.

**Por escenario.** NOPAT / inversión fija neta / Δcirculante / cartera no repuesta (P0, se suma) / reposición adicional (se resta) / FCF, en M€. En el año 11, la inversión fija y el circulante son las dos partes de g ÷ ROIC × NOPAT. La suma es: FCF = NOPAT − fija − Δcirculante + cartera − adicional.

| Alt. | Escenario | Año 1 | Año 5 | Año 10 | Año 11 (terminal) |
|---|---|---|---|---|---|
| REF | MALO | 201,7 / 0,0 / −2,2 / 0,0 / 0,0 / 203,8 | 162,9 / 0,0 / −2,1 / 0,0 / 0,0 / 165,0 | 164,5 / 0,0 / 2,0 / 0,0 / 0,0 / 162,5 | 166,2 / 16,4 / 2,1 / 0,0 / 0,0 / 147,7 |
| REF | NORMAL | 214,8 / 28,3 / 4,3 / 0,0 / 0,0 / 182,2 | 227,0 / 30,6 / 4,7 / 0,0 / 0,0 / 191,7 | 250,6 / 33,8 / 5,1 / 0,0 / 0,0 / 211,7 | 255,6 / 41,2 / 5,3 / 0,0 / 0,0 / 209,1 |
| P1 | MALO | 201,7 / 0,0 / −2,2 / 4,5 / 19,3 / 189,0 | 162,9 / 0,0 / −2,1 / 3,9 / 19,4 / 149,5 | 164,5 / 0,0 / 2,0 / 0,0 / 19,9 / 142,5 | 166,2 / 16,4 / 2,1 / 0,0 / 3,0 / 144,8 |
| P1 | NORMAL | 214,8 / 28,3 / 4,3 / 4,5 / 0,0 / 186,7 | 227,0 / 30,6 / 4,7 / 3,9 / 0,0 / 195,6 | 250,6 / 33,8 / 5,1 / 0,0 / 0,0 / 211,7 | 255,6 / 41,2 / 5,3 / 0,0 / 0,0 / 209,1 |
| P5 | MALO | 201,7 / 0,0 / −2,2 / 4,5 / 47,8 / 160,6 | 162,9 / 0,0 / −2,1 / 3,9 / 47,8 / 121,1 | 164,5 / 0,0 / 2,0 / 0,0 / 47,8 / 114,7 | 166,2 / 16,4 / 2,1 / 0,0 / 29,9 / 117,8 |
| P5 | NORMAL | 214,8 / 28,3 / 4,3 / 4,5 / 19,5 / 167,2 | 227,0 / 30,6 / 4,7 / 3,9 / 17,2 / 178,4 | 250,6 / 33,8 / 5,1 / 0,0 / 14,0 / 197,7 | 255,6 / 41,2 / 5,3 / 0,0 / 18,2 / 191,0 |
| P6m | MALO | 201,7 / 0,0 / −2,2 / 4,5 / 25,3 / 183,0 | 162,9 / 0,0 / −2,1 / 3,9 / 18,6 / 150,2 | 164,5 / 0,0 / 2,0 / 0,0 / 16,2 / 146,3 | 166,2 / 16,4 / 2,1 / 0,0 / 5,3 / 142,4 |
| P6m | NORMAL | 214,8 / 28,3 / 4,3 / 4,5 / 1,7 / 185,0 | 227,0 / 30,6 / 4,7 / 3,9 / 11,8 / 183,8 | 250,6 / 33,8 / 5,1 / 0,0 / 22,6 / 189,1 | 255,6 / 41,2 / 5,3 / 0,0 / 0,0 / 209,1 |

En P1 y REF, el NORMAL y el BUENO difieren solo por P0: +4,5 M€ en los años 1–4 y +3,9 en el año 5. El año a año completo de todas las alternativas y escenarios, también el BUENO, está en `pm1_anio_a_anio.csv`.

**Necesidades de caja en el MALO** (FCF del año 1 · mínimo · suma de los años 1–5 · inversión bruta de caja del año 1):

| Alternativa | FCF año 1 | Mínimo | Suma años 1–5 | Inversión bruta año 1 |
|---|---|---|---|---|
| REF | 203,8 | 161,5 | 921,1 | 132,9 |
| P1 | 189,0 | 141,6 | 846,6 | 147,7 |
| P2 | 156,8 | 142,5 | 801,4 | 180,0 |
| P4 | 156,8 | 116,3 | 755,1 | 180,0 |
| P5 | 160,6 | 113,8 | 704,2 | 176,2 |
| P6x | 149,7 | 113,9 | 668,8 | 187,1 |

**Frente a la 4.7.1.**
- La referencia y la sensibilidad X41 se reproducen exactamente. El modelo de la 4.7.1 se ejecuta sin cambios y sus salidas son idénticas byte a byte.
- Las diferencias son las de cada tratamiento: P0, el hueco, λ o el nivel. Ninguna procede de cambios en r, probabilidades, k, caja, puente, acciones o palancas.

## 7. Conclusión por tratamiento

| Tratamiento | Conclusión |
|---|---|
| Reposición = D&A (REF) | **No respaldada.** Ningún indicio la sostiene. Se mantiene solo como referencia de la plantilla |
| P0 (cartera de clientes) | **Respaldada con alcance y límites**: dato publicado. Falta la deducibilidad fiscal y el efecto en el margen al agotarse |
| Desfase de inflación, λ ≈ 1,15 (P1) | **Hipótesis condicionada (central).** Los indicios van de 1,05 a 1,29: vida contable e inflación, balance y Reino Unido. El rango explorado es 1,10–1,25, y no es una cota |
| Exceso estructural en nivel (P5) o intensidad de inversión (P6) | **Información insuficiente para elegir.** Falta el dato material: el desglose de la inversión de 2021–2025 por naturaleza y el inventario de hornos con su calendario (Q-E1 y Q-E2). Las alternativas exploradas van de 69,7 (P0) a 62,7 (P5). P6i (61,3, la previsión de 2025 como nivel permanente) y P6x (55,7) son extremos explorados. Nada de esto es una cota |
| Ola 2026–2027 (P2) | **Hipótesis condicionada**, con fuente secundaria y posterior a la base. Falta la cifra oficial (Q-E5) |
| Capacidad conservada (R1) | **Hipótesis condicionada**, de efecto pequeño en este modelo (P3: −0,07 de ponderado; −0,32 en el V MALO) |
| +41,8 % en todo (X41) | **No es una alternativa coherente**: alrededor de la mitad de su efecto es doble cómputo. Su parte no duplicada es P5x |

**Sobre la decisión humana D-N3b** (propuesta de Claude, sin aplicar, en `financiero/decisiones_y_preguntas_4_8.json`):
- P1 como hipótesis central (no como mínimo respaldado: P1b y P0 quedan por encima);
- siempre acompañado de P5, P6m y P6x;
- no se propone «=D&A».

La confirmación humana de una cifra no sustituye el dato que falta.

## 8. Crítica independiente con Fable

**Motivo.** Es la hipótesis de mayor efecto potencial del ensayo y el encargo señala esta crítica como aplicación pertinente de Fable. Se usó una sola vez, como agente de contexto separado y de solo lectura, sobre el código y las salidas de la primera versión.

**Resultado** (informe transcrito en `CRITICA_FABLE_PM1.md`; resumen en `REGISTRO_ENTREGA_4.8.md`, §4). Según la crítica:
- la regla del hueco es correcta como identidad y el doble cómputo de X41 existe;
- **bloqueante:** el abanico estaba truncado. Con λ = 1,10 y sin alternativas de nivel estructural, la primera versión concluía que la reposición apenas movía el valor (−0,0 / −1,8), y la envolvente coherente llega a −5 / −13;
- **importantes:** el indicio del Reino Unido es débil (perímetro, ocho años); λ central debería ser 1,15; falta la intensidad de inversión real (electrificación); la suficiencia de la regla del hueco descansa en que el S2C sea causal; el terminal del MALO es frágil;
- **menores:** margen y D&A, escudo del MALO, límites de P0, convención de D&A, P3 y P4.

**Qué cambió.**
- λ central pasa de 1,10 a 1,15, con rango 1,10–1,25.
- Se añaden el indicio de balance, P5, P5x y P6.
- X41 pasa de «descartada» a «cerca de la mitad es doble cómputo».
- La conclusión se expresa como rango.
- Se declaran los menores.

**§8b · Auditoría interna** (`AUDITORIA_INTERNA_4_8.md`). Corrigió, entre otras cosas:
- la presentación de λ como «mínimo respaldado» y una cota implícita entre P1 y P5 (Z-b);
- la regla del hueco aplicada a la recuperación de capacidad en P3 y P4 (Z-c);
- la medida del exceso de P5 frente a la amortización total con P0 aplicado (Z-d);
- el fundamento de P6i, que ahora es la previsión oficial de 2025 (Z-l);
- la tabla por escenario (Z-m);
- la marca de las citas externas (Z-k).

Las cifras de esta versión ya los incorporan.

**Qué no se adoptó, y por qué.** La crítica estimaba en un 63 % el doble cómputo de X41, con un terminal plano. Con la convención de este guion (adicional proporcional a las ventas en el terminal), sale en torno al 51 %. Las dos cifras se dan como de convención.

## 9. Qué sigue bloqueado y qué falta

- **Valoración financieramente validada.** Sigue bloqueada por P-M1, porque falta Q-E1/Q-E2, y por los pendientes que conservan su estado: N4 (38 ceros, que la IA no confirma), N9 (ruta B, E1–E7), N10 (probabilidades), P-N1 y P-N2.
- **Plantilla.** No admite reposición explícita ni la regla del hueco. Cualquier adopción exige un cambio de plantilla o el modelo auxiliar identificado. No se ha tocado ninguna fórmula protegida.
- **Preguntas a la empresa.** Q-E1 a Q-E7 están preparadas y **no enviadas**: el encargo no autoriza a contactar.
