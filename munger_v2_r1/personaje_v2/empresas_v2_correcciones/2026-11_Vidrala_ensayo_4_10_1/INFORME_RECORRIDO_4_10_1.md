# Informe del recorrido · ensayo de Vidrala con base económica 2025 (entrega 4.10.1)

**Qué es.** Qué se ejecutó en el expediente nuevo, qué resultado dio, en qué se diferencia de C1 de la 4.10, qué límites tiene y cuál es el siguiente hito. Las decisiones humanas que siguen haciendo falta están agrupadas, sin firmar, en `propuestas/PROPUESTAS_HUMANAS_4_10_1.md`.

**En una línea.** Recorrido terminado: el pipeline recorrió los pasos 0–14 con agentes reales y cerró en «concluido» con una auditoría interna nueva APROBADO. La conclusión financiera (esperar · cubo Vigilar) es la del ensayo con una configuración exploratoria **no adoptada**: queda pendiente de la revisión externa y de las decisiones humanas de §5, aunque ninguna de las abiertas conocidas cambia la zona.

## 1. Qué se ejecutó

**Preparación** (antes del paso 5; scripts en `scripts/`):
1. **Preparación 1** (`preparar_ensayo_2025.py`): copia del expediente de la 4.6.1 con solo las entradas de partida; todo lo demás, a `antecedentes/heredados_4_6_1/` con inventario y huellas. Metadatos y `fase1_v63.json` activos generados desde `configuracion/configuracion_ensayo_2025.json`. Concordancia: CONCUERDA.
2. **Preparación 2** (`reexpresar_base_2025.py`): la fase A de la primera preparación detectó siete datos de Análisis heredados de la etapa 1 medidos a 30-jun-2026, con operaciones de 2026. Se reexpresaron a 31-dic-2025 por la ruta real, sin cambiar código de producción ni juicios:
   - copia de ensayo de la etapa 1 sin esos datos ni sus filas de evidencia;
   - valores de 2025 por `fase1_v63.json` o derivados de la Historia;
   - la etapa 1 original, en `antecedentes/etapa1_original/` (SHA-256 `6aed2116…`, la de la 4.6.1);
   - la primera preparación, en `antecedentes/preparacion_1_datos_de_2026/`.
   Detalle en `resultados/reexpresion_2025.md`.

| Celda | Etapa 1 (30-jun-2026) | Ensayo (31-dic-2025) |
|---|---|---|
| C24 ROIC (definición A del inversor) | 0,13 | 0,1394 |
| C31 cobros o existencias frente a ventas | Sí | Sí |
| C33 deuda neta ÷ EBITDA | 0,69 | 0,36 (derivada de la Historia) |
| C34 caja frente a deuda a corto | No | Sí (1,62) |
| C42 EV/EBITDA | 7,68 | 7,82 |
| C53 caja | 109,4 | 108,352 |
| C54 deuda total | 409,6 | 262,913 |

Después, el pipeline se relanzó desde el paso 0 con un `estado_pipeline.json` propio (inicio 2026-11-11T21:53:40). La concordancia de entradas, sobre el libro de datos y sobre el evaluado, da **CONCUERDA** (`resultados/concordancia_2025*.md`): los **valores** de las celdas de datos concuerdan con la configuración, sin residuos de la base anterior y sin valores migrados que prevalezcan sin declararse. Quedan **textos** heredados con cifras o fechas de la base anterior en la evidencia de Control maestro y en notas de los metadatos, que no son datos del caso y se identifican uno a uno en esa misma salida (15 en el libro evaluado; ver §4).

**Recorrido** (salidas en `resultados/pipeline_0*.txt`). Cada código 10 fue un relevo: Claude ejecutó el rol que pedía `prompts_generados/` con un agente de contexto separado y relanzó el pipeline.

| Paso | Rol | Quién | Resultado |
|---|---|---|---|
| 0–4 | entorno, migración, fase 1, entrada, volcado | pipeline | ÍNTEGRO; motor calculable |
| 5 | extracción V6.3 | agente (Sonnet, según configuración) | `extracto_v63.md`; se conservó en la preparación 2 porque no cita ninguno de los datos reexpresados |
| 6–7 | fase A | agente Opus, esfuerzo extra | motor B («No · financiación cambia mucho»), cubo provisional Vigilar; revisada sobre el libro de la preparación 2 |
| 8–9 | fase B | agente Opus, esfuerzo extra | gramática código 0; tres desviaciones G5 justificadas |
| 10–11 | fase C, turnos 1 y 2 | un agente Opus, esfuerzo extra, mismo contexto | sin vuelta a B; comprobación conjunta no procede (conclusión no favorable) |
| 12 | verificación y acreditación del libro final | pipeline | ÍNTEGRO, 0 fallos; `acreditacion_libro.json` |
| 13 | auditoría interna | agente Opus, esfuerzo extra, contexto separado | APROBADO, 16/16 en PASA; responde a SA-433ea31c3f7fc4bd sobre el material e60b272b654aeece; se identifica como interna |
| 14 | cierre y publicación | pipeline | concluido · APROBADO (fin 2026-11-11T23:11:22) |

- **Esfuerzo:** la persona responsable pidió esfuerzo extra para las fases y la auditoría. La configuración prevé esfuerzo alto para las fases y medio para la verificación.
- **Fase A interrumpida:** la primera fase A, con el esfuerzo de la configuración, se detuvo para relanzarla con esfuerzo extra. Su salida parcial está en `antecedentes/fase_a_interrumpida/`.
- **Contadores:** el estado se creó de nuevo al relanzar en la preparación 2; el de la preparación 1, archivado, tenía todos los contadores a 0 (no se eludió ningún límite). Desde entonces no se reinició ninguno y ninguna fase pidió corrección (fase B 0, fase C 0, auditoría 0).
- **Lo que no se usó:** `agentes_sinteticos.py`, respuestas prefabricadas y aprobaciones escritas a mano.

## 2. Resultado

| | MALO | NORMAL | BUENO | Ponderado | Precio de Sí (k = 3) | Precio |
|---|---|---|---|---|---|---|
| €/acción | 53,66 | 72,74 | 86,44 | 71,66 | 66,52 | 90,10 (cierre de 2025) |

- **Conclusión:** zona «caro»: el precio queda un 26 % por encima del precio de Sí. Estado concluido, cubo Vigilar, acción esperar, precio objetivo 66,52 € (por acción de 31-dic-2025, antes de la ampliación liberada de 2026, que no se incorpora). Fundamento: no procede (conclusión no favorable).
- **Motor B:** r_op 0,086990, puente 160,784 (el dividendo a cuenta no se resta otra vez) y FCF base 161,2.
- **Palancas** (M/N/B):
  - crecimiento −0,01 / 0,02 / 0,035;
  - margen 0,15 / 0,185 / 0,20;
  - S2C 0,9 / 0,9 / 1,0;
  - g 0,01 / 0,02 / 0,025;
  - ROIC 0,09 / 0,11 / 0,12;
  - probabilidades 0,2 / 0,6 / 0,2.
- **Predicciones del NORMAL** (emitidas el 11-nov-2026; comprobación el 31-mar-2028):
  - margen EBIT de 2027 entre el 16,0 % y el 20,5 % (probabilidad 0,7);
  - ventas de Vidrala Europe en 2027 entre 680 y 770 mm (0,75);
  - pagos por inmovilizado de 2027 por encima de la amortización (0,8).
- **Salidas oficiales vigentes:** ficha, informe y resumen, con las huellas en correspondencia:
  - libro evaluado `da053c79…`, que es el de la ficha y el del comprobante;
  - `cierre_vigente.json` con ficha, informe y auditoría actuales;
  - `motivo_vigencia` y `motivo_acreditacion_libro` sin motivo.
- **Destinos de publicación:** `resumen_v2.csv` y `Vidrala/publicaciones_resumen.json`, los dos del ensayo, aislados. No se tocó ninguna publicación de otro expediente.

## 3. Diferencias frente a C1 de la 4.10

Las calcula `scripts/comparar_con_C1.py` sobre copias identificadas con recálculo forzado (`resultados/comparacion_C1.md`):
- **Control:** el libro de la referencia con C41/C55 de C1 reproduce C1 (70,4665 / 65,6645).
- **Mismas entradas y palancas:** el libro final del ensayo con las palancas de C1 da **exactamente C1**.

Atribución:
- **Entrada y convención: 0,00 €.** Precio, rf 0,0285 frente a 0,0329, los siete datos reexpresados y la fecha no mueven la valoración del motor B con E dada. C37 (precio) solo entra en la escalera.
- **Juicio: +2,00 € en el NORMAL, +1,20 € en el ponderado y +0,86 € en el precio de Sí.** Toda la diferencia es el margen objetivo del NORMAL (0,185 frente a 0,18): la fase B pesa Brasil completo frente a las bajadas de precio de 2026. El resto de palancas coincide con la referencia.
- **Fórmula: ninguna.** El código y la plantilla no cambian.
- **Precisión de C46/C47** (335,413 / 169,668 frente a 335,4 / 169,7): el FCF base pasa de 161,2 a 161,245, pero la valoración no cambia, porque el motor B no usa esa base. La variante queda aparte; el caso principal conserva la precisión de referencia.

La coincidencia numérica de MALO y BUENO no sustituye la revisión de juicios: las fases A–C se hicieron de nuevo con las entradas de 2025. Por ejemplo, la quiebra ya no necesita justificar un disparador de 30-jun-2026 (C34 = Sí) y las tesis se reescribieron sin Chile.

## 4. Límites

**Configuración y método:**
- La configuración del ensayo es una hipótesis explícita autorizada por el encargo, no una firma de D-N6, D-N7 ni D-N8. La fecha de análisis es la real (11-nov-2026) y no es un backtest.
- N1–N3 y P-M1 no se integran ni se adoptan.
- k = 3 es experimental.

**Abiertos financieros (ninguno se declara resuelto; materialidad evaluada por la fase C y comprobada en la auditoría):**
- **P3** (C48 = 0, C49 = 4,5, supuesto heredado): nula para el motor B; −0,7 % del precio de Sí en el peor caso.
- **Reservas N4** (ceros pendientes; L26 = 0): −0,028 €/acción por cada millón. No se confirma ningún cero.
- **Provisión de personal** (L25 = 6,223): 0,18 €/acción. No se descarta un doble cómputo con los flujos futuros, porque no hay desglose.

**Sensibilidades que quedan para la persona responsable** (ninguna cambia zona ni cubo):
- tipo impositivo de la hoja (Historia C52 = 20,0 % frente al 24,3 % de 2025): −5,7 % del precio de Sí, hasta 62,71;
- base del margen (C8 sobre C49 = 16,9 %, que mezcla perímetros): de 0 a +2,7 %;
- capital que libera el MALO, que la plantilla no puede representar: −1,3 %.

**Restos documentales y fuentes** (revisión interna, H-1 y H-2):
- La evidencia de Control maestro de varias celdas de datos conserva el texto de la etapa 1 aunque el valor sea de 2025. Lo más visible: M41 y M52 explican la capitalización y las acciones de la etapa 1 (88,70 × 34,185 = 3.032,2 mm; 35,206 − 1,021 = 34,185), frente a C41 = 3.169,9755058 y C55 = 35,182858. Hay también menciones de 2026 en N41, N52, C28, C32, C40, C46, C50 y C76 (G82). Las notas `_notas` de `fase1_metadatos.json` y `fase1_v63.json` heredadas de la 4.6.1 citan además la rentabilidad de Trading Economics de noviembre de 2026 y las 35,206 M acciones.
- Ninguno es un dato del caso ni entra en el cálculo, y todos están identificados en `resultados/concordancia_2025*.md` («textos heredados identificados»). No se corrigen en el libro cerrado porque eso cambia el material auditado y exige una auditoría nueva; queda en D-EVIDENCIA-2026.
- C38 (Simply Wall St, 08-oct-2026) es contexto posterior a la base; no se usa.
- El PDF del Bundesbank para la rf no se pudo conservar, porque la consola no tiene red hacia bundesbank.de; consta la fila citada y la URL.
- **Papel de la rf** (revisión interna): no entra en el valor del motor B, pero sí en la r mínima, en el texto de D57, en las referencias mecánicas de g y en la regla G3. Con rf = 0,0285, la referencia mecánica de g del BUENO redondea a 0,03, por encima de la rf; la fase B eligió 0,025, así que no tiene efecto.

**Ficha** (avisos de la auditoría):
- `ficha.etapa1.cubo` copia entero el texto C104 de la etapa 1;
- C97 técnico aparece en `recuento_clases`, pero no en `hipotesis_sin_fundamento`.

**Observaciones para la revisión externa** (revisión interna):
- 11 de las 12 palancas coinciden con la 4.6.1, con las mismas referencias mecánicas; la fase B lo razona con los datos de 2025.
- La fase A activa es una revisión de la de la preparación 1 (la mayoría de los textos se mantienen). La fase C leyó la del antecedente, declarado «sin copiarla».

**Alcance:**
- La auditoría es interna (agente de Claude con contexto separado). No sustituye a la revisión externa.
- No valida otras empresas.

## 5. Siguiente hito y propuestas humanas

**Siguiente hito:** la primera versión integrada supervisada. Requiere:
- la revisión externa de esta entrega;
- las firmas humanas que hagan falta (D-N6 a D-N8 de la 4.10 y las de `propuestas/PROPUESTAS_HUMANAS_4_10_1.md`, entre ellas el tipo impositivo de la hoja y la base del margen);
- la integración de N1–N3 y P-M1 según la especificación de la 4.10;
- un mecanismo general, no de ensayo, para cambiar la base económica de un expediente con datos heredados.

Las propuestas están agrupadas y con los campos humanos vacíos.
