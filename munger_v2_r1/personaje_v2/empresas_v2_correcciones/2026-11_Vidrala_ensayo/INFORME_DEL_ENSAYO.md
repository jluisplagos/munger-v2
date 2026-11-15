# Informe del ensayo · aplicación controlada del piloto Vidrala (entrega 4.4, 9-nov-2026)

**Categorías:**
- **[Hecho]**: comprobado directamente por Claude.
- **[Interpretación]**: lectura razonada de los hechos.
- **[Propuesta]**: pendiente de decisión.

Las comprobaciones están en `scripts/comprobar_ensayo.py` (72 de 72 cumplen; salida en `resultados/comprobar_ensayo_salida.txt`).

## 1. Resultado en una página

**[Hecho] Estado del ensayo.**
- El expediente nuevo está construido y verificado **hasta el registro humano de P1**.
- Ese registro es el único que falta para continuar (`PROPUESTA_REGISTRO_P1.md`).
- **No se han ejecutado** la construcción de la Historia con P1, el recálculo, las fases A, B y C, la auditoría ni el contraste entre motores. Todo ello depende de P1.
- Hacerlo sin P1, o aplicando P1 por otra vía, habría sido un ensayo sobre datos que se saben erróneos o habría eludido el registro humano.

**[Hecho] Por qué P1 exige un registro humano.**
- Es una cifra incorrecta (tipo B). El procedimiento vigente la fija en `fase1_decisiones.json`, que solo escribe una persona, y la aplica `construir`.
- Claude ha preparado la propuesta exacta y su evidencia. No ha escrito ese archivo ni ha firmado nada.

**[Hecho] Qué se ha completado de lo que no depende de P1.**
1. **Resolución del dividendo**, antes de tocar la caja:
   - valor **con derecho** a 31-dic-2025;
   - sin ajuste en el puente;
   - el dividendo se resta una sola vez en cualquier comparación posterior con un precio sin derecho.

   Corrige la inclinación de la 4.3.1 de restarlo (`RESOLUCION_DIVIDENDO_Y_ACCIONES.md`).
2. **Fuentes nuevas conservadas, con su huella:**
   - comunicación del dividendo (doc. 2275);
   - comunicación de la CNMV sobre la liberada de 2026;
   - cuentas consolidadas de 2016 a 2022.
3. **Expediente nuevo** en `empresas_v2_correcciones/2026-11_Vidrala_ensayo/Vidrala/`:
   - **P8 aplicada** (tipo A: dos páginas de D&A, sin tocar importes);
   - los **39 ceros heredados re-extraídos solo en esa partida**, con cita literal. Quedan **pendientes**: la IA no los confirma;
   - textos de los diez años regenerados desde los PDF oficiales;
   - pasos 0 y 1 del pipeline ejecutados (libro base idéntico al original).
4. **Construir es ahora posible.** Antes no lo era: los textos de 2016 a 2022 faltaban y los ceros sin cita los rechazaba la regla R-c.
   - En una copia temporal, `construir` reproduce la Historia original **valor a valor**.
   - Con una decisión **simulada** de P1, en otra copia temporal y marcada como simulación, solo cambia el circulante de 2024.
   - Los pasos 0–4 del pipeline terminan con 0 bloqueantes y el motor B calculable.
5. **Registro de hipótesis del ensayo**, con valor, definición, fuente, fecha y estado (`REGISTRO_HIPOTESIS_ENSAYO.md`).

**[Interpretación] Alcance.**
- Ni este ensayo ni su continuación permiten una comparación válida con el precio del 3-nov-2026 ni una recomendación de compra o espera.
- Las salidas mecánicas que genere la continuación (precio de Sí, zona, cubo) se conservarán como **resultados mecánicos del ensayo**.

## 2. Resolución del dividendo y acciones

Resumen; el detalle está en `RESOLUCION_DIVIDENDO_Y_ACCIONES.md`.

**Fecha económica y derecho al dividendo.**
- La fecha económica es el 31-dic-2025, y el valor es **con derecho**: último día con derecho, 10-feb-2026; fecha sin derecho, 11-feb-2026; pago, 13-feb-2026.
- La caja (108,352) contiene los fondos del dividendo. La obligación (43,338, EN25 p.70) es con los mismos accionistas.
- No se resta nada. Si más adelante se compara con un precio sin derecho, se resta una vez, como distribución **o** mediante saldos posteriores al pago, nunca de las dos maneras.

**Acciones.**
- El dividendo se pagó sobre 35.182.858 acciones en circulación (= 43.338.244,48 ÷ 1,2318).
- El ensayo conserva C55 = 35,206, la cifra emitida, con la diferencia del 0,07 % declarada.

**Liberada de 2026.**
- La negociación de derechos empezó el 29-oct-2026 y terminó el 11-nov-2026 (hechos). La formalización es posterior a ese período, y la fecha de registro de las acciones nuevas está ausente.
- El 3-nov-2026 el precio era sin derecho (interpretación basada en el calendario oficial).
- Los porcentajes de 2 a 4,9 % son **escenarios condicionados de autocartera**, no límites acreditados.

## 3. Expediente nuevo y cambios respecto al original

| Elemento | Ensayo | Respecto a `empresas_v2/Vidrala/` |
|---|---|---|
| `etapa1/`, `fase1_fuentes.json`, `fase1_metadatos.json`, `fase1_listas.md` | Copiados | Idénticos (huella) |
| `fase1_decisiones.json` | Copiado; **sin P1** | Idéntico. P1 está propuesto aparte |
| `fase1_partes/AR_*.json` | Versiones nuevas | Solo 41 cambios: 39 `cita` añadidas a ceros y 2 páginas de D&A 4 → 7. Ningún importe, línea, signo ni nota cambia |
| `texto/CF_2016.txt` … `CF_2025.txt` | Regenerados desde los PDF oficiales | Los originales no están en el paquete. Las 535 citas de los AR originales están en sus páginas, salvo las dos de P8 |
| `Vidrala_v63_base.xlsx` | Pasos 0–1 del pipeline | Idéntico celda a celda |
| `fase1_v63.json`, libros de datos y evaluado, fases | **No existen todavía** | Pendientes del registro de P1 |
| Estado del pipeline | Paso 2, sin estado final | El original está `concluido` (cubo Vigilar). Ese estado no se hereda |

**[Hecho] Comparación con decisión simulada** (solo pasos 0–4; copia descartada; `resultados/simulacion_pasos_0_4.txt`).
- **Historia C5:L26:** la única diferencia es K14, que pasa de −127,84 a 84,994.
- **Análisis:** C37, C41, C46–C50, C52, C55 y C56 iguales.
- **Derivadas:** Historia C53 pasa de 1,5492 a 0,9159 y C58 de 0,0199 a −0,0276. Coinciden con las réplicas de la 4.3.
- **Entrada:** 0 bloqueantes; motores A, B y C calculables. Hay 6 evidencias pendientes para «LISTO · PROVISIONAL»: C48 y los ceros pendientes de adquisiciones, intereses en financiación, principal de arrendamientos, arrendamientos de 2016 y minoritarios.

## 4. Lo heredado no se reutiliza como decisión

**[Hecho] Fases.**
- El expediente de ensayo no contiene `fase_a.json`, `fase_b.json`, `fase_c.json`, `extracto_v63.md` ni `auditoria.md`.
- No se registraron salidas antiguas como agentes simulados, a diferencia de H3.
- Las fases tendrán que escribirse de nuevo.
- Las palancas, probabilidades y escenarios antiguos son hipótesis heredadas para la fase B (registro de hipótesis).

**[Hecho] Ceros.**
- Los 38 ceros en uso siguen **pendientes**. La re-extracción solo añade la cita literal que exige la regla R-c.
- Su confirmación es humana y no bloquea el ensayo.

## 5. Continuación, una vez registrado P1 (pasos y salvaguardas)

1. **Pipeline desde el paso 2:** `construir` con P1, relleno, comprobación de entrada y volcado. Se espera lo mismo que en la simulación.
2. **Paso 5 · extracción:** debe recoger como entradas `REGISTRO_HIPOTESIS_ENSAYO.md` y `RESOLUCION_DIVIDENDO_Y_ACCIONES.md`.
3. **Paso 6 · fase A:**
   - C62 = «No · financiación cambia mucho», justificado de nuevo (motor B como hipótesis principal fijada antes de los resultados);
   - «qué caja espero» con perímetro de continuadas;
   - la nota de fechas y la definición con derecho.
4. **Paso 8 · fase B:**
   - S2C justificado con evidencia propia. La referencia ≈0,92 es aritmética de P1, no la palanca, y conserva sus problemas de comparabilidad (G6 con Italia, Vidroporto en J31, el cobro de Italia en K31);
   - condiciones del motor B: g < `r_op` y ROIC a largo plazo > g.
5. **Paso 10 · fase C:** revisión conjunta de datos, hipótesis y resultados.
6. **Paso 13 · auditoría:** sin contexto previo.
7. **Contraste con el motor A y T3**, en una copia separada del libro del ensayo:
   - mismas palancas comunes;
   - con T3 (C46 = 322,65; J14 = 85,978; K14 = 36,487 derivados; δ = 0 como hipótesis; C49 sin acreditar);
   - separando el efecto del motor, el de la definición de `f` y el de C49;
   - el resultado más favorable no es un argumento.

## 6. Bloqueos, decisiones e hipótesis pendientes

| # | Qué | Tipo | Bloquea |
|---|---|---|---|
| **B1** | **Registro de P1 en `fase1_decisiones.json`** (`PROPUESTA_REGISTRO_P1.md`) | Registro humano | **Sí: es el único bloqueo para continuar** |
| B2 | Confirmación de los 38 ceros pendientes, sobre todo L26 y C48, que afectan al motor B | Registro humano | No; impide el estado «LISTO · PROVISIONAL» completo |
| B3 | L25: déficit neto de pensiones frente a provisión de personal | Evidencia (pregunta 11 de la 4.3.1) | No; es una hipótesis declarada |
| B4 | E1–E7 (ruta B) | Evidencia | Solo la comparación con el precio (fuera de este encargo) |
| B5 | Alternativa del dividendo (valor sin derecho) | Decisión de definición | No; el ensayo usa el valor con derecho |
| B6 | Discrepancia de la fecha del consejo (17 frente a 19-dic-2025) | Nota documental | No |

## 7. Comprobado, antecedentes y pendiente

**Comprobado directamente por Claude:**
- las huellas de las fuentes;
- la reproducción de los textos;
- las diferencias de los AR;
- `comprobar-anio` de los diez años;
- `construir` en copia;
- la simulación de P1 (construir, y pasos 0–4 del pipeline);
- los hechos del dividendo y de la liberada;
- la integridad de los originales.

**Antecedentes comprobados externamente** (según la persona responsable): la integridad de la 4.3.1 y las baterías de 43, 217, 45 y 35.

**Pendiente:** todo lo de §5 y la tabla de §6.

**Modelos.** Opus en todo el procedimiento. Fable no se usó, porque el bloqueo es de registro, no de razonamiento. Sin subagentes. Las re-extracciones de ceros las hizo Claude (Opus) siguiendo el prompt `historia_anio.md` del sistema, que prevé Sonnet: es una diferencia de modelo declarada.
