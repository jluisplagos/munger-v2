# Informe del ensayo · reanudación tras el registro humano de P1 (entrega 4.5, 9-nov-2026)

**Categorías:**
- **[Hecho]**: comprobado directamente por Claude o por un script del paquete.
- **[Interpretación]**: lectura razonada de los hechos.
- **[Propuesta]**: pendiente de decisión de la persona responsable.

**Comprobaciones:** `scripts/comprobar_continuacion.py`, con 60 de 60 cumplidas. La salida está en `resultados/comprobar_continuacion_salida.txt`.

**Alcance.** Es un **ensayo exploratorio**: ruta A, base 2025 y motor B como hipótesis principal.
- Precio de Sí, zona, margen, cubo y C104 son **resultados mecánicos del ensayo**.
- No son una comparación válida con el precio de noviembre de 2026.
- No son una recomendación de compra ni de espera.

## 1. Resultado en una página

**[Hecho] Registro de P1.**
- La persona responsable lo registró el 9-nov-2026 (SHA-256 `b4e47afc…c445a4`).
- Se validó con 10 requisitos y se incorporó sin modificarlo (`registro_P1/REGISTRO_APLICACION_P1.md`).

**[Hecho] Construcción.**
- La Historia difiere del original solo en K14 = +84,994.
- Cambian sus ocho celdas derivadas, entre ellas C53 = 0,915854 y C58 = −0,027608. Coinciden con los controles esperados.
- No apareció ninguna diferencia adicional.

**[Hecho] El personaje se ejecutó de nuevo con el pipeline vigente**, sin reutilizar ninguna salida antigua:
- paso 5: extracción;
- paso 6: fase A;
- paso 8: fase B;
- paso 10: fase C, en dos turnos;
- paso 13: auditoría con contexto independiente.

El pipeline terminó en el paso 14: **concluido · auditoría APROBADO · motor B · cubo Vigilar**. No hubo ninguna corrección ni vuelta entre fases.

**[Hecho] Resultados mecánicos del motor B.** Valor a 31-dic-2025, con derecho al dividendo a cuenta, sobre 35,206 millones de acciones emitidas.

| Escenario | Valor por acción |
|---|---|
| MALO | 53,67 € |
| NORMAL | 70,77 € |
| BUENO | 86,49 € |
| Ponderado (0,2 / 0,6 / 0,2) | 70,50 € |
| Precio de Sí (escalera k = 3) | 65,69 € |

La zona es «caro» frente a 87,9. Ese precio es intradía, del 3-nov-2026 y de una fuente secundaria: la comparación **no es válida** (§5).

**[Hecho] Contraste con el motor A**, en copias separadas y con las mismas palancas.

| Variante | Ponderado | Precio de Sí |
|---|---|---|
| Motor A con datos publicados (T1) | 88,27 | 82,82 |
| Motor A con T3 (condicionada) | 77,67 | 72,87 |

La diferencia se separa en cuatro efectos: tasa, puente, `f` y definición de `f` (§6).

**[Interpretación]** El motor A da más valor **porque proyecta para siempre un `f` negativo**. Ese `f` está hecho de partidas cuya recurrencia no está acreditada: Italia y su plusvalía en T1; devengos en T3. No da más valor por el negocio. El resultado más favorable no es un argumento para elegirlo.

**[Propuesta] Tres decisiones de convención para la persona responsable,** que las fases dejaron visibles (§8):
- el tipo impositivo de la Historia (C52);
- la base del margen (C8);
- el límite de traducción del escenario MALO.

## 2. Registro de P1 y construcción

**Validación y huella.** `registro_P1/` conserva el archivo recibido, su validación y el registro de aplicación.

**Diferencias frente al original** (`comprobar_continuacion.py`, §3–§4, y `resultados/comparacion_con_original.md`, §1 y §3).
- **Valores.** `fase1_v63.json` difiere en un solo valor: el circulante de 2024. Los metadatos son iguales: precio, acciones, capitalización, fecha, tasa sin riesgo y geografía.
- **Anotaciones.** Las demás diferencias de `fase1_v63.json` son anotaciones del código reparado en H1–H3:
  - los 38 ceros pendientes, con su cita;
  - el bloque `analisis` con la fuente de C46–C49;
  - la fuente de P1, con la persona y la fecha del registro.

  Ninguna cambia un valor.
- **Historia del libro recalculado.** Solo difieren K14 y sus derivadas: K30, K31, C53, C58, C76, C77, C79 y C80. Todas son fórmulas que dependen de la fila 14.
- **Texto.** Las diferencias de texto son notas y fuentes de la columna M, más C68 (= Palancas!C9, que escribe la fase B).

**Conservado.**
- P8: los AR de la copia son idénticos a los de la 4.4.
- Los 38 ceros siguen pendientes. `construir` registra «0 confirmados por decisión humana».

**Comprobación de entrada.**
- 0 bloqueantes; motores A, B y C calculables.
- 6 evidencias pendientes para «LISTO · PROVISIONAL»: C48 y los ceros pendientes de adquisiciones, intereses en financiación, principal de arrendamientos, arrendamientos de 2016 y minoritarios.

**Estado del libro.**
- El final es «NO LISTO · evidencias incompletas (2 pendientes) · cálculo completo». Las dos evidencias no verificables son ceros pendientes de H1, L26 y C48.
- El original figuraba «LISTO · PROVISIONAL» porque se construyó antes de la reparación H1. La diferencia la causa la marca de los ceros pendientes, no el ensayo.

## 3. Ejecución nueva del personaje

**[Hecho] Entradas de cada agente.**
- El prompt generado por el pipeline.
- `ENTRADAS_AGENTES_4_5.md`, que remite a:
  - `REGISTRO_HIPOTESIS_ENSAYO_4_5.md`;
  - `RESOLUCION_DIVIDENDO_Y_ACCIONES.md` de la 4.4;
  - las conclusiones pertinentes de la 4.3 y la 4.3.1.

**[Hecho] Restricciones.** Todos los agentes tuvieron prohibido leer el expediente original. Cada fase se ejecutó en un contexto separado, como prevén los prompts.

**Extracción (paso 5).**
- `extracto_v63.md`: 6.304 palabras y 9 secciones, con 27 datos no encontrados.
- El agente comprobó cada cita contra las marcas de página.
- Registra tres contradicciones entre informes y no elige entre ellas:
  - coste medio de la deuda de 2024: 4,03 % frente a 5,31 %;
  - tasas del test de deterioro de 2024;
  - crecimientos del test de 2021.
- `etapa1/extracto.md` no existe en el expediente (tampoco en el original). La extracción solo complementa `datos_v63.md`.

**Fase A (paso 6): motor B justificado de nuevo con evidencia** (`fase_a.md` §6). Argumentos a favor:
- tres regímenes de financiación dentro de la ventana 2023–2025: deuda con arrendamientos de 599,0 → 393,3 → 262,9; compra de Vidroporto; venta de Italia; dividendo extraordinario de 128,6; coste medio de 1,52 % → 6,29 %;
- `f` = −0,0276 no es representativo tras P1;
- el puente y V0 comparten perímetro a 31-dic-2025.

También registra lo que pesa en contra:
- financiación baja a 31-dic-2025;
- `r_op` derivada con fechas mezcladas;
- L25 aproximada;
- L26 y C48 pendientes;
- el desfase de fechas, que el motor B no resuelve.

Otras decisiones:
- **Celdas cambiadas frente a la etapa 1:** C27 «Estable», C97 «Neutral» (la única evidencia de directivos es una fuente secundaria no verificada) y las narrativas B66:D66.
- **C8 = «Media del ciclo».** La aplica la regla con C6 = cíclica. Arranca del 16,9 % de Historia C49, con perímetro mixto, y el límite queda declarado.

**Fase B (paso 8): palancas decididas de nuevo**, sin copiar la referencia S2C ≈0,92.

| | MALO | NORMAL | BUENO |
|---|---|---|---|
| Crecimiento de los años 1–5 | −1 % | 2 % | 3,5 % |
| Margen objetivo | 15 % | 18 % | 20 % |
| S2C | 0,9 | 0,9 | 1,0 |
| ROIC a largo plazo | 9 % | 11 % | 12 % |
| g | 1 % | 2 % | 2,5 % |
| Probabilidad | 0,2 | 0,6 | 0,2 |

- **S2C de 0,9.** Sale de dos medidas propias: ventas sobre capital invertido de 2025 (0,93, el único año con perímetro homogéneo) y Δventas sobre Δcapital de 2016–2025 (0,90). En el MALO toma el valor menos favorable de su rango.
- **Márgenes.** Se basan en el ciclo energético de 2019–2025 (18,1 % publicado) y no compensan el arranque en el 16,9 %.
- **Celdas vacías:** C22 y C23 (el disparador es un saldo de 30-jun-2026, fuera del ensayo), C24 y C76.
- **Condiciones del motor B:** g < `r_op` (0,0869) y ROIC > g en los tres escenarios.
- **Gramática:** código 0, con tres desviaciones G5 justificadas.

**Fase C (paso 10).**
- **Coherencia.** Revisó la coherencia del conjunto. No pide revisar palancas (`revisar_palancas` = false). No hay ningún dato ausente material (34 de 34 revisados).
- **Fundamento material.** Lo condiciona sobre todo C8, acotada entre el 16,9 % y el 19,9 %.
- **Estado.** `concluido`, con la condición escrita: ruta A cerrada con las reglas del personaje; no es una valoración comparable con el precio.
- **C104.** Sigue el formato de la plantilla («Pendiente de decisión de cartera · conclusión del personaje: esperar: precio de Sí ≤ 65.69 · …»). Añade el aviso de resultado mecánico, no comparable con 87,9 y que no es una recomendación de compra ni de espera.
- **Celdas reescritas** con evidencia propia: B101, B102, C93, C103 y las predicciones. No contienen cifras de la etapa 1 (Chile, deuda a 30-jun-2026, ≈74 €, ≈48 €).

**Auditoría (paso 13).**
- La hizo un agente sin participación en las fases.
- Resultado: 16 de 16 puntos pasan. **Veredicto: APROBADO**.
- Sus avisos no bloqueantes están en §8.

## 4. Resultados mecánicos

| Concepto | Valor |
|---|---|
| Motor | B · `r_op` = 0,0869 (convención 4; r = 0,09 sin cambio) · puente = 160,784 mm |
| V0 · margen de partida · tipo | 1.465,16 · 16,86 % · 20,03 % |
| Valor por acción MALO / NORMAL / BUENO | 53,67 / 70,77 / 86,49 € |
| Ponderado · precio de Sí · precio del escenario MALO | 70,50 · 65,69 · 53,67 € |
| Peso del valor terminal | 42–57 % |
| Palanca más influyente | La tasa: ±1 punto equivale a ±13,2 € por acción (tornado de la hoja) |
| Zona · cubo · estado | caro · Vigilar · concluido (auditoría APROBADO) |

**[Interpretación]** La zona, las distancias, el DCF inverso (9,5 % implícito) y la lectura B267 comparan un valor de 31-dic-2025 con un precio de 3-nov-2026. Son mecánicos. La hoja los calcula, pero el ensayo no los lee como conclusión.

## 5. Dividendo, fechas y alcance (sin cambios respecto a la 4.4)

**[Hecho] Dividendo y caja.**
- La caja de Historia L24 es 108,352: los 43,338 del dividendo a cuenta no se restan.
- El puente = 213,613 + 49,3 + 6,223 + 0 − 108,352 = 160,784. Lo comprueba `comprobar_continuacion.py`, §6.
- Si se comparara con un precio sin derecho, el dividendo se restaría una sola vez, como distribución o mediante saldos posteriores al pago, nunca de las dos maneras.
- La fase C cuantifica la alternativa sin derecho (no ejecutada) en −1,23 € por acción.

**[Hecho] Datos no actualizados.** No se han actualizado precio, acciones, capitalización ni datos de 2026, y E1–E7 no se han completado. Toro, Kristin, la deuda nueva y las recompras quedan fuera de las palancas.

## 6. Contraste controlado con el motor A y T3

**Cómo se hizo** (`scripts/contraste_motores.py`; salidas en `contraste_motores/`).
- Copias separadas del libro evaluado final; el libro del ensayo no se modifica.
- Palancas, probabilidades, V0, margen de partida, tipo y acciones son comunes.
- Cada variante se recalculó con LibreOffice.

**Variantes:**
- **A1:** C62 = «Sí»; C76 = 0, referencia mecánica.
- **A2:** A1 + T3, con C46 = 322,65, J14 = 85,978 y K14 = 36,487. Son circulantes derivados, no publicados, y δ = 0 es una hipótesis.
- **A2a y A2b:** A2 con C49 = 6,8 y con C49 = 0.

Las `f` de las variantes reproducen las réplicas de la 4.3 (−0,027608; −0,009847; −0,008307; −0,012860).

| Variante | Motor | f | Tasa | Ponderado | Precio de Sí |
|---|---|---|---|---|---|
| B0 · ensayo | B | 0 en el valor (el libro muestra −0,0276) | `r_op` 0,0869 | 70,50 | 65,69 |
| A1 · T1, datos publicados | A | −0,027608 | r 0,09 | 88,27 | 82,82 |
| A2 · T3, condicionada | A | −0,009847 | r 0,09 | 77,67 | 72,87 |
| A2a · T3 con C49 = 6,8 | A | −0,008307 | r 0,09 | 76,75 | 72,00 |
| A2b · T3 con C49 = 0 | A | −0,012860 | r 0,09 | 79,47 | 74,55 |

**Separación de efectos** (`scripts/descomponer_contraste.py`; `contraste_motores/descomposicion.md`).
- Una réplica en Python reproduce las cinco variantes de la hoja al céntimo.
- Cada paso cambia una sola cosa. Ponderado, en el orden tasa → puente → `f`:

| Paso | Efecto en el ponderado | Nota |
|---|---|---|
| Tasa: `r_op` → r | −3,27 | −3,54 en el orden inverso |
| Puente: no restar 160,784 mm | +4,57 | Igual en los dos órdenes |
| `f` de 0 al de T3 | +5,88 | +6,15 en el orden inverso |
| Definición de `f`: T3 → T1 | +10,60 | |

- C49 mueve el ponderado de A2 entre −0,92 y +1,80. En el motor B no entra.

**[Interpretación]**
- La mayor parte de la diferencia entre motores no es del motor en sí: es la definición de `f`. La sola corrección T3 → T1 vale +10,60.
- El efecto de motor propiamente dicho (tasa y puente) es pequeño y de signos opuestos.
- En el motor A, un `f` negativo suma flujo cada año y para siempre. En T1 lo componen Italia y su plusvalía, que no se repiten. En T3 lo componen partidas de devengo (impuestos pagados por debajo de los devengados, provisiones) con recurrencia **no acreditada**, lo que no equivale a un carácter no recurrente demostrado.
- No hay intervalos demostrados para `f`. T3δ no se ejecutó: δ = 0 se mantiene como hipótesis, según el encargo.
- El resultado más favorable del motor A **no es un argumento para elegirlo**. La elección del motor B se fijó antes de los resultados y se justificó por adecuación (fase A).

## 7. Comparación con el original

El detalle está en `resultados/comparacion_con_original.md`, generado por `scripts/comparar_con_original.py`. Contiene:
- las entradas;
- las 68 celdas de juicio, de las que 32 difieren;
- la Historia recalculada;
- los estados y los resultados.

| Concepto | Original | Ensayo |
|---|---|---|
| Motor | A | B |
| Circulante de 2024 | −127,84 | 84,994 |
| `f` | 0,0199 | −0,0276; no entra en el valor B |
| Valor por acción MALO / NORMAL / BUENO | 43,80 / 57,87 / 77,69 | 53,67 / 70,77 / 86,49 |
| Ponderado | 59,02 | 70,50 |
| Precio de Sí | 54,67 | 65,69 |
| Zona y cubo | caro · Vigilar | caro · Vigilar |
| Estado del libro | LISTO · PROVISIONAL | NO LISTO · 2 evidencias pendientes (ceros de H1) |

**[Interpretación]** Las dos columnas no son comparables como valoraciones. Cambian:
- el dato de 2024 (P1);
- el motor;
- las palancas, decididas de nuevo;
- la fecha a la que se refiere el valor.

## 8. Hipótesis, decisiones y pendientes que siguen abiertos

| # | Qué | Tipo | Efecto cuantificado por la fase C (precio de Sí) | Bloquea |
|---|---|---|---|---|
| N1 | **Tipo impositivo de la Historia (C52 = 20,0 %, media de 2021–2025 con perímetro mixto) frente al 24,3 % de 2025** | Convención de la persona responsable; ninguna fase cambia datos | −2,6 % con el tipo de 2023–2025; −5,7 % con el de 2025. No cambia la zona | No |
| N2 | **C8 = «Media del ciclo»:** arranque desde el 16,9 % mezclado, cuando las narrativas parten del 19,9 % de 2025 | Límite declarado (fase A; acotado por la fase C) | De 0 a +2,7 % | No |
| N3 | **Límite de traducción del MALO:** el motor libera capital con ventas que caen | Límite de la plantilla (fase B) | −1,3 % sin esa liberación | No |
| N4 | 38 ceros pendientes, sobre todo L26 y C48 | Registro humano | L26 necesitaría ≈115 mm para mover un 5 % | Impide «LISTO · PROVISIONAL» |
| N5 | L25: provisión de personal frente a déficit neto | Evidencia | ±0,27 % | No |
| N6 | `r_op`: E de 3-nov-2026, D de 31-dic-2025, i de 2025 | Convención 4 | +1,0 % / −0,4 % | No |
| N7 | C55 emitidas (35,206) frente a 35,183 en circulación | Hipótesis declarada | +0,07 % | No |
| N8 | Alternativa sin derecho al dividendo | Definición (no ejecutada) | −1,23 € por acción | No |
| N9 | E1–E7 (ruta B), cierre oficial y liberada, datos de 2026 | Evidencia | — | Solo la comparación con un precio |
| N10 | Probabilidades 0,2 / 0,6 / 0,2: cumplen la regla, pero se apoyan sobre todo en la serie de márgenes | Hipótesis (auditoría, punto 11) | −3,9 % / +3,3 % | No |
| N11 | Contradicciones entre informes: coste de la deuda de 2024; tasas de deterioro de 2024 | Nota documental (extracción) | — | No |
| N12 | Discrepancia de la fecha del consejo (17 frente a 19-dic-2025) | Nota documental (4.4) | — | No |

**[Hecho] Observaciones de procedimiento de la auditoría** (no bloqueantes; no se ha cambiado código):
1. El pipeline ejecuta `ficha.py --estado concluido` antes de la auditoría, aunque el Anexo D dice que `concluido` no se escribe hasta APROBADO. Tras el APROBADO se reescribió igual.
2. Falta la marca literal «con datos de etapa 1 incompletos» (encargo §3.4) en la ficha y el informe.
3. `informe.md` §6–§7 muestra la zona frente a 87,90 sin repetir el aviso de ruta A. El aviso está en §1, en `fase_c.md` y en C104.
4. «Fundamento no procede» en C104 no es una de las cuatro etiquetas de la sección 15: ninguna describe una lista no vacía con una conclusión no favorable.

[Propuesta] Revisar estos puntos del procedimiento en un encargo aparte.

## 9. Controles técnicos

- **Pipeline:**
  - `verificar_todo.sh`: PASS;
  - `comprobar_celdas_v2.py` (fases A, B y C): 0 errores;
  - gramática tras la fase C: código 0;
  - esquemas: todos válidos;
  - citas (`verify_quotes_v2.py --paginas-estrictas`): PASS en las tres fases;
  - recálculo forzado comprobado.
- **`scripts/comprobar_continuacion.py`: 60 de 60.** Cubre:
  - el registro de P1;
  - la integridad de los originales y de la entrega 4.4;
  - la construcción;
  - el libro recalculado;
  - la entrada;
  - las fases;
  - los resultados;
  - el dividendo y el puente;
  - C104 y las celdas reescritas;
  - el contraste y la descomposición.
- **Las 72 comprobaciones de la 4.4** se ejecutan sobre su expediente intacto, que describe el estado anterior a P1, y no se han modificado.

## 10. Modelos y agentes

- **Orquestación, controles y documentos:** Claude (Opus).
- **Agentes de contexto separado** (todos Opus): extracción, fase A, fase B, fase C (los dos turnos en el mismo agente, como prevé el procedimiento) y auditoría.
- **Diferencia con el procedimiento:** `config_v2.json` prevé Sonnet con esfuerzo medio para la extracción y Opus con esfuerzo medio para la verificación. En este ensayo se usó Opus en ambas, porque el encargo fija Opus como modelo principal.
- **Fable no se usó:** ningún paso lo requería.
- **Comprobaciones propias de los agentes:** ejecutaron validar_esquema y verify_quotes antes de entregar. Sus archivos temporales quedaron fuera del expediente.
