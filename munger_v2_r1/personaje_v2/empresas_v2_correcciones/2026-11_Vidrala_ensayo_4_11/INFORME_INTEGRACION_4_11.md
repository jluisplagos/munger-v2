# Informe de integración · entrega 4.11 · primera integración económica experimental del motor B

**Qué es.** El informe pedido por el encargo 4.11 §11.7: qué funciona, qué sigue condicionado, qué difiere del legado y qué decisiones humanas se proponen. Separa cuatro cosas que no deben confundirse:

1. la **implementación** (el sistema calcula, concilia, rechaza y traza);
2. la **ejecución del piloto** (un expediente real recorrido con la configuración de demostración);
3. la **adopción humana** (ninguna: todo sigue sin firmar);
4. la **validación económica** (pendiente: que una estructura describa bien a la empresa no se ha demostrado).

**Jerga.** Las abreviaturas técnicas se explican en `v6/v64_experimental/docs/README_V6.4_experimental.md` §1. Las de uso más frecuente:

- **motor B:** valoración «operativo con deuda»;
- **N1:** tipo impositivo normalizado;
- **N2:** margen de partida manual;
- **N3:** regla de reinversión con ventas que caen; R0 es la simétrica y R1 libera solo circulante y conserva la capacidad;
- **P-M1:** reposición frente a crecimiento, con las estructuras H, S, SR1, SR2 y SRF, las familias Λ y Θ, y la cartera de clientes P0 o legado;
- **precio de Sí:** el precio que cumple la regla de asimetría con k = 3, una convención experimental.

## 1. Implementación (hechos comprobados)

### Plantilla V6.4 experimental (`v6/v64_experimental/`)

**Construcción.** Se construye desde la V6.3, que no cambia, y la reconstrucción es determinista (mismo SHA-256 `04bab281…`).

**Contenido.**

- **Hoja «Configuración V6.4».** Modo, N1, N2, N3, P-M1, bases históricas, parámetros efectivos, 28 comprobaciones con su motivo y trazabilidad por parámetro activo.
- **Hoja «Conciliación B».** MALO, NORMAL y BUENO, años 1–10 y terminal, con la identidad FCF = NOPAT + D&A − inversión fija bruta − Δcirculante comprobada contra el motor.
- **Columnas BU:DY del Motor.** Están en las 124 filas de valoración: escenarios, sensibilidades, tornado y DCF inverso.

**Cambios frente a la V6.3.**

- Fórmulas cambiadas: 1.994, todas con la heredada literal en la rama heredada. Fórmulas nuevas: 7.870 (Motor 7.068, «Conciliación B» 670, «Configuración V6.4» 131 y Panel!C18). Ninguna quitada.
- Gráficos, controles, validaciones y formatos de la V6.3: idénticos.

**Modo heredado.** Es la V6.3 celda a celda: 0 diferencias en 120.168 celdas en los libros de la 4.6.1 y de la 4.10.1, también con todas las opciones nuevas escritas.

**Modo experimental.** Solo se aplica al motor B; con otro motor, se rechaza. N3 y P-M1 exigen una elección explícita, porque ninguna estructura es central por defecto.

- **Vacío, cero y error son distintos.** Un 0 en N1 o N2 se usa. Un error cuenta como «no cumple».
- **Rechazos.** R0 + P-M1 se rechaza con explicación. Los dominios no se recortan: un valor fuera de rango no calcula. El motivo llega al motor y la regla V35 bloquea el valor (INCOMPLETO).

### Conexión con el pipeline (`personaje_v2/`)

**Selección explícita.** Con `--config config_v2_v64_experimental.json`. `plantilla_activa.json` guarda las huellas. El pipeline se detiene con código 2, sin escribir nada, en cinco casos:

- falta `configuracion_economica.json`;
- la configuración no es válida;
- la configuración V6.4 llega con la V6.3;
- el expediente V6.4 se ejecuta con la V6.3;
- un expediente que empezó con la V6.3 se ejecuta con la V6.4 (revisión interna H1, corregido). Se comprobó también sobre una copia del expediente cerrado de la 4.10.1: código 2, ningún archivo nuevo ni cambiado (`resultados/seleccion_inversa_4_11.md`).

**Motor que elige la fase A** (revisión interna H3, corregido). La fase A elige el motor como si la configuración no existiera. `entrada_v63.md` separa «no calculable por datos» de «no cubierto por la configuración experimental». Si elige el A o el C con el modo experimental, el expediente termina en `no_entregable · limite_del_modelo`, no en una falta de datos.

**Recorrido de la configuración.**

1. `configuracion_economica.json` la escribe la orquestación, nunca un agente de juicio.
2. Se aplica en el paso 2.
3. Se vigila por contenido de las celdas: si cambia, se reaplica y se retrocede.
4. Forma parte del material auditado, junto con la selección y las variantes. Cambiarla después del cierre retira la aprobación en la primera llamada y exige una auditoría nueva.

**Variantes calculadas en el paso 10.** Heredado, activa, componentes aislados, las otras estructuras con entradas compatibles y las convenciones; si la configuración declara un rango de λ o de θ, también sus extremos (revisión interna H11). La fase C las evalúa en `configuracion_v64`: cada parámetro activo, el mantenimiento con `adoptada = false`, y «no cambia la zona» solo respecto de las variantes calculadas. Sin esa evaluación recibe una corrección. Una variante sin zona impide afirmar «misma zona en todas». En el paso 12, la variante «activa» tiene que reproducir `precio.json` (revisión interna H10).

**Salidas conectadas.**

- Lectura de resultados (`configuracion_v64`), volcado de datos (sección 0) y comprobación conjunta (N1, N2, λ y θ movibles).
- Ficha (`versiones.plantilla`, `configuracion_economica` y límites según la configuración activa) e informe (§1 con el objetivo marcado provisional, §14 y distancias con el denominador identificado).
- Resumen propio de las filas V6.4: `resumen_v2_v64_experimental.csv`, junto al expediente, nunca el `resumen_v2.csv` de las filas V6.3 (revisión interna H2, corregido).
- Prompts de las fases B y C y de la verificación.
- Esquemas: `fase_c` y `ficha`.

### Cambio de base (`personaje_v2/scripts/cambiar_base.py`)

Es un mecanismo general y reutilizable, no un parche para Vidrala.

**Qué hace.**

- Crea un expediente nuevo sin sobrescribir el original y mueve lo heredado a antecedentes con inventario.
- Deja una copia de ensayo de la etapa 1 en la que solo cambian las celdas declaradas.
- Sustituye las entradas de `fase1_v63.json`.
- Reescribe la evidencia activa del Control maestro; los textos anteriores van a antecedentes.
- Retira las notas que reintroducían la base anterior.
- Separa las fechas: ejecución real, base, precio, acciones y publicación de las fuentes.

**Restos resueltos.** M41/N41 (capitalización y autocartera de otra base), M52/N52 (34,185 millones y la liberada de 2026), C28, C32, C38, C40, C41, C46, C47, C48, C50, C55, C76 y C97. Las notas de Bolsamanía, Trading Economics y 35,206 M van a `antecedentes/`.

**Comprobación.** `comprobar` busca restos en las columnas G–M de las filas de juicio y en las E–N de las de datos (filas 17–82 y 107–175 del Control maestro). En el control y en el piloto, en el libro de datos y en el evaluado, da «CONCUERDA Y SIN RESTOS». Fuera de ese rango quedan textos de la base anterior en la cabecera y en el bloque de auditoría heredado de la etapa 1 (F5, H5, B10, B88, D88 y D100): no entran en ningún valor, `comprobar` los lista aparte sin contarlos (revisión interna H9) y, de ellos, solo F5 pasa a `datos_v63.json`.

**Reproducibilidad.** Repetir la preparación da las mismas entradas activas: la copia de la etapa 1 tiene el mismo SHA-256 `0276426f…`.

### Pruebas

- **Batería nueva y obligatoria** `personaje_v2/pruebas/test_integracion_v64.py`: 58 pruebas en cuatro grupos (plantilla, 117 casos con la réplica y el contraste numérico de las lecturas, pipeline y cambio de base).
- **Réplica independiente** (Fable, contexto separado, sin leer las fórmulas): 117/117 sobre los libros de la plantilla final.
- **Regresión** de todas las baterías anteriores, sin cambios. Detalle en `REGISTRO_PRUEBAS_4_11.md`.

## 2. Control heredado y diferencias frente al legado

**Control heredado limpio** (`control_heredado/`). La V6.4 en modo heredado, con el expediente preparado por el cambio de base y las salidas de los agentes de la 4.10.1, da exactamente lo de la 4.10.1:

- MALO 53,659650, NORMAL 72,740491 y BUENO 86,443849;
- ponderado 71,664994325 y precio de Sí 66,520610325;
- zona caro y estados técnicos iguales;
- |Δ| = 0.

En el libro, las 44 diferencias son la evidencia reescrita y la fecha de análisis.

**Diferencias del modo experimental frente al legado.** En el libro 4.6.1 de las réplicas de la 4.7.1 y la 4.8.1, con los parámetros completos de sus archivos fuente:

| Configuración (libro 4.6.1) | Ponderado | Precio de Sí | Fuente de la referencia |
|---|---|---|---|
| Heredado (V6.3) | 70,495154 | 65,688087 | 4.6.1 |
| T1 · M1 · R1 | 69,244673 | 64,262177 | `…_4_7_1/financiero/matriz.json` |
| T1 · M1 · R1 + H · Λ 1,15 · P0 | 68,916259 | — | `…_4_8_1/financiero/rf_resultados.json` |
| T1 · M1 · R1 + S · Λ 1,15 · P0 | 61,628529 | — | ídem |
| T1 · M1 · R1 + SR1 · Λ 1,15 · P0 | 62,465272 | — | ídem |
| T1 · M1 · R1 + SR2 · Λ 1,15 · P0 | 63,657209 | — | ídem |
| T1 · M1 · R1 + SRF · Λ 1,15 · P0 | 65,384233 | — | ídem |

Los precios de Sí de las estructuras están en las salidas de la batería y de la réplica: `replica/replica_salida_plantilla_final.txt`.

**Interpretación.** P-M1 es la pieza con más efecto. Con λ = 1,15 mueve el ponderado entre −0,3 € (H) y −7,6 € (S) frente a T1·M1·R1. Con Θ el rango es mayor: en la 4.8.1, de 50,2 a 69,3. N1, N2 y R1 juntas mueven unos −1,25 € frente al heredado. Estas cifras son mecánicas: no dicen qué estructura describe mejor a Vidrala.

## 3. Ejecución del piloto (`piloto/Vidrala/`)

**Qué es.** Un expediente completo con N1–N3 y una estructura P-M1 explícita de demostración (encargo §9). La configuración es T1 22,05 % (escudo vinculado), M1 18,55 %, R1, SR1 · Λ con λ = 1,15 (años planos, terminal proporcional a las ventas) y cartera P0. Se eligió para ejercitar el sistema, no por su valor, y no se adopta. Base: 31-dic-2025, precio 90,10 €, N 35,182858, E 3.169,9755058, caja 108,352, puente 160,784, r 0,09, probabilidades 0,2/0,6/0,2 y k = 3 experimental. P1 sigue aplicada, sin otra resta del dividendo.

**Preparación.** `cambiar_base.py preparar` con `configuracion/cambio_de_base_piloto.json`. El origen, la 4.6.1, queda intacto. Datos de la preparación:

- 128 celdas de evidencia en 23 filas;
- 7 datos de la etapa 1 vaciados (los da la fase 1);
- 10 entradas de `fase1_v63.json` sustituidas, con constancia expresa de que C49 se conserva en 4,5 frente al 6,764 reconstruido (P3);
- 3 notas retiradas.

**Recorrido.** Pipeline real con `--config config_v2_v64_experimental.json`; cada código 10 fue un relevo de trabajo. Las salidas están en `piloto/resultados/pipeline_0*.txt`.

| Pasos | Rol | Quién | Resultado |
|---|---|---|---|
| 0–4 | entorno, migración, fase 1, configuración, entrada y volcado | pipeline | ÍNTEGRO; 96 celdas de configuración escritas; 0 bloqueantes; motor B calculable |
| 5 | extracción | agente Sonnet, esfuerzo medio (configuración), contexto limpio | `extracto_v63.md`, 3.881 palabras; los hechos posteriores al cierre, etiquetados |
| 6–7 | fase A | agente Opus, esfuerzo extra, contexto limpio | motor B («No · financiación cambia mucho», por los hechos y no por la plantilla); cubo provisional Vigilar; herencia revisada celda a celda |
| 8–9 | fase B | agente Opus, esfuerzo extra | gramática con código 0 antes del recálculo (tres G5 justificadas); después del recálculo, dos G8 sin justificar (salto del año 11: NORMAL 0,057, BUENO 0,080), que pasan a la fase C |
| 10 | variantes V6.4 y fase C (dos turnos, un solo agente) | pipeline y agente Opus, esfuerzo extra | 13 variantes calculadas; G8 justificadas; gramática con fase C, código 0; comprobación conjunta: no procede (conclusión no favorable) |
| 11–12 | material provisional y verificación | pipeline | `verificar_todo.sh` PASS; libro acreditado |
| 13 | auditoría interna | agente Opus, esfuerzo extra, contexto separado | **APROBADO, 16/16 en PASA**, responde a SA-a843decaaf51d16e sobre el material 6dd711561fd92f12; avisos para la revisión externa |
| 14 | cierre | pipeline | **concluido · APROBADO** (fin 12:43:28); resumen publicado en el destino aislado `piloto/resumen_v2.csv` |

**Contadores.** Ninguna fase pidió corrección por formato. Las dos G8 las trató la fase C, como prevé el flujo. No se usaron agentes sintéticos ni respuestas prefabricadas.

**Resultado** (€/acción; las palancas son las de la fase B de este piloto, que no son las de la 4.10.1):

| | MALO | NORMAL | BUENO | Ponderado | Precio de Sí (k = 3) | Zona (90,10 €) |
|---|---|---|---|---|---|---|
| Configuración de demostración (activa) | 45,56 | 61,93 | 81,74 | 62,62 | 57,74 | caro |
| La misma hoja en modo heredado (V6.3 efectiva) | 54,13 | 69,67 | 90,73 | 70,77 | 66,02 | caro |

**Conclusión del personaje** (es la del ensayo, no una adopción): concluido · Vigilar · esperar. El precio objetivo provisional es 57,74 €. Lo condiciona la reposición P-M1 de la configuración de demostración; con la V6.3 efectiva sería 66,02 €.

**Distancias, con el denominador identificado:**

- 90,10 está un 56,04 % por encima del precio de Sí (diferencia ÷ precio de Sí);
- el precio de Sí está un 35,91 % por debajo del precio (diferencia ÷ precio).

**Comparación de estructuras con entradas compatibles** (`piloto/Vidrala/configuracion_v64_variantes.md`). Mismas palancas, mismas N1–N3, λ = 1,15 y P0:

| Variante | Ponderado | Precio de Sí |
|---|---|---|
| sin P-M1 | 69,40 | 64,37 |
| H | 69,08 | 63,11 |
| SRF | 66,10 | 60,46 |
| SR2 | 64,03 | 58,87 |
| SR1 (activa) | 62,62 | 57,74 |
| S | 61,62 | 57,03 |

**Componentes aislados frente al heredado:**

| Componente | Ponderado | Precio de Sí |
|---|---|---|
| N1 | −1,97 | −1,79 |
| N2 | +1,00 | +0,98 |
| R1 (solo el MALO) | −0,38 | −0,81 |
| P0 (frente a sin P-M1) | +0,49 | — |

**Convenciones alternativas frente a la activa** (ponderado): años proporcionales a las ventas, −0,42; terminal que crece con g, +0,94. La zona es «caro» en las 13 variantes calculadas; solo de ellas se afirma que la zona no cambia.

**Mantenimiento** (fase C, `configuracion_v64.mantenimiento`).

- **Hechos:** la reposición supera la amortización. El capex es ≥ 1,10 × la amortización todos los años desde 2017, y 1,45 × en 2021–2025, con ventas orgánicas planas o a la baja. El destino principal es la renovación de hornos.
- **Magnitud:** no se mide. Según la fase C, λ = 1,15 equivale a un 33 % del exceso histórico, y «todo reposición» daría λ ≈ 1,46. Esas dos cifras usan el exceso sobre la amortización total (229,4). Con la base que usa la hoja, el exceso sobre la amortización que se repone (238,8), serían un 31 % y λ ≈ 1,48 (revisión interna O8; comprobado con las bases del libro: 0,15 × 500,209 = 75,03; 75,03 ÷ 238,794 = 31,4 %; 1 + 238,794 ÷ 500,209 = 1,477).
- **Estructura más coherente según la fase C:** SR1, con confianza baja.
  - H no encaja con capex alto y ventas a la baja.
  - S cuenta dos veces el exceso.
  - SRF quita más de lo que muestra la historia.
- **Adopción:** no se adopta. La fase C marca P-M1 (estructura, familia y parámetro) como material para el objetivo (−10,3 % del precio de Sí frente a sin P-M1), pero no para la acción. Por eso el objetivo es provisional y no se fuerza otra conclusión.

**Rango de λ, recalculado en el libro** (`resultados/rango_lambda_4_11.md`; revisión interna H11). Con la estructura, la familia y las convenciones de la demostración:

| λ | Ponderado | Precio de Sí | Zona |
|---|---|---|---|
| 1,10 | 65,04 | 60,12 | caro |
| 1,15 (activa) | 62,62 | 57,74 | caro |
| 1,25 | 57,76 | 53,00 | caro |

La variante «activa» de ese cálculo reproduce el `precio.json` del piloto. Las cifras coinciden con la réplica de la revisión interna (60,1154 y 52,9960).

**Aislamiento de C46/C47 y C49** (`resultados/aislamiento_entradas_4_11.md`; en el control heredado, `…_control_heredado.md`). Ni la precisión de C46/C47 (335,413 y 169,668) ni C49 = 6,764 cambian el valor del motor B: 0,000000 € de ponderado y de precio de Sí. Sí cambian el FCF base (C52): de 161,200 a 161,245 y a 158,936. P3 sigue abierto y los ceros pendientes siguen pendientes.

**Avisos de la auditoría** (no bloquean; quedan para la revisión externa):

- C12 = Sí convive con un foso de duración desconocida.
- C98 = Buena choca con el disparador de recompras de la propia fase A; la fase C lo anota en `celdas_corregidas`.
- La carga de capex sin ventas del MALO solo está acotada con una réplica (−3,4 % del precio de Sí).
- El §1 de `informe.md` da el precio objetivo sin decir «provisional», aunque lo dicen C104, la ficha y los §2, §8, §10 y §12.
- `ficha.etapa1` copia el texto heredado de C104 (D-FICHA-ETAPA1, abierto desde la 4.10.1).
- El objetivo depende en más de un 10 % de P-M1 (−10,3 % del precio de Sí frente a sin P-M1), y la fase C lo trata como objetivo provisional y no como dato material (S-19). La revisión interna lo examinó (H4): las dos reglas escritas encajan con el caso y dan estados distintos (`concluido` con objetivo provisional, o `pendiente_de_datos`). La opción de la fase C es defendible y no se cambia; qué regla manda pasa a la propuesta (D411-MATERIALIDAD).

**Correcciones posteriores al cierre del piloto.** Después de la revisión interna se corrigieron en el código el «provisional» del §1 del informe (H7), los límites de la ficha con R1 (H12) y la cuenta de variantes calculadas (H10). También se separaron en `entrada_v63.md` «no calculable por datos» y «no cubierto por la configuración experimental» (H3), y las filas V6.4 pasaron a su propio resumen (H2). El piloto se cerró antes y conserva sus salidas tal como se produjeron: no se regeneraron.

- Su `entrada_v63.md` presenta todavía los motores A y C como «NO calculable»; la fase A eligió el B por los hechos y lo dejó escrito («lo elegiría igual en la V6.3»).
- Su fila del resumen está en `piloto/resumen_v2.csv`, registrada en `publicaciones_resumen.json`; una ejecución nueva publicaría en `resumen_v2_v64_experimental.csv`.
- El material auditado son archivos del expediente, no el código, así que esas correcciones no retiran su aprobación (comprobado en una copia: `REGISTRO_ENTREGA_4.11.md` §4). Las versiones nuevas las prueba la batería con agentes simulados.

## 4. Qué sigue condicionado (límites declarados)

1. **Ninguna configuración está adoptada.** La del piloto es de demostración (encargo §9), elegida para ejercitar el sistema: N1, N2, R1, el factor f del S2C (SR1), la cartera P0 y las bases históricas. No se eligió por su valor. D-N1, D-N2, D-N3, D-N3b–e y P-M1 siguen sin firmar.
2. **P-M1 no queda resuelta por implementarse.** λ y θ son hipótesis, no mediciones: falta el desglose de la inversión y el calendario de hornos (Q-E1–Q-E3, preguntas no enviadas). La estructura depende además de si el ROIC_lp de la fase B ya es neto de reposición (Q-ROIC1).
3. **Terminal con R1.** No aplica la regla del máximo conservado: en el MALO carga la inversión fija para crecer aunque las ventas sigan por debajo del máximo. Es la definición de la 4.7.1/4.8.1 y es prudente. Lo señaló la réplica.
4. **Crédito terminal de H.** Equivale a la forma de la 4.8.1 solo si la inversión fija terminal es ≥ 0, lo que ocurre en todos los casos calculados.
5. **P3 (C48/C49) y C46/C47.** El caso principal conserva C49 = 4,5 y C46/C47 con la precisión de referencia. Las alternativas se aíslan en §3. P3 sigue abierto y los ceros pendientes siguen pendientes.
6. **Fuente de la rf.** El PDF del Bundesbank no se conserva en el paquete: la consola no tiene red hacia bundesbank.de (proxy 403). La herramienta web leyó la fila de diciembre de 2025 (2,85 %, ejemplar de 11.11.2026), pero no da los bytes, así que no hay huella propia. Se cita la que registró la revisión externa, `6ace5ac7…`, como dato de esa revisión.
7. **k = 3 sigue siendo experimental.** El ensayo no es un backtest: la fecha de análisis es la real y la base, el 31-dic-2025.
8. **Fe de erratas de la 4.10.1.** `INFORME_RECORRIDO_4_10_1.md` §2 dice que «el precio queda un 26 % por encima del precio de Sí». Con el denominador identificado:
   - 90,10 está un 35,45 % por encima de 66,5206103 (diferencia ÷ precio de Sí);
   - 66,5206103 está un 26,17 % por debajo de 90,10 (diferencia ÷ precio).

   El documento histórico no se modifica. Las salidas nuevas (informe §7) calculan las dos lecturas con sus propios valores.
9. **Regla de materialidad sin fijar** (revisión interna H4). Cuando un parámetro experimental es material solo para el precio objetivo, dos reglas escritas del personaje dan estados distintos. Mientras no se decida (D411-MATERIALIDAD), cada fase C lo resuelve con criterio propio y la auditoría no tiene regla con la que comprobarlo.
10. **Palanca S2C inerte con R1** (revisión interna H12). En un escenario cuyas ventas no superan nunca el máximo anterior, la inversión fija para crecer es 0 y la palanca S2C no actúa (MALO del piloto). Junto con el límite 3, en el MALO del piloto el terminal carga 16,39 M€ de inversión fija para crecer con las ventas por debajo del máximo.
11. **Dominios sin comprobar** (revisión interna H13; README §8.9). f no tiene cota superior; la inversión fija para crecer puede salir negativa si S2C·f > 1 ÷ NWC; la fija terminal negativa afecta también a SRF; y con R1 y g ≤ 0 el terminal no aplica el máximo conservado. No aparecen en el piloto ni en los 117 casos. Los avisos pasan a la propuesta (D411-DOMINIOS).
12. **Lecturas experimentales.** El valor sin crecimiento (BL) no incluye la cartera P0: en el piloto, 58,19 €/acción frente a unos 58,75 con ella (revisión interna H6). Es una lectura: no entra en el valor ni en el precio de Sí. Desde esta entrega, BL, BP, BQ y Diagnóstico B176:D177 tienen contraste numérico en la batería.
13. **Controles mecánicos con la base histórica** (revisión interna O4). La regla G7 de la gramática y las referencias mecánicas usan el tipo de la Historia y el S2C sin f también en modo experimental. Es un diseño declarado y no tuvo efecto en el piloto.
14. **Ejecución a mano** (revisión interna O5). `ficha.py`, `informe.py` y `resumen.py` no comprueban la selección de plantilla: sobre un expediente V6.4 se ejecutan con `MUNGER_CONFIG` apuntando a `config_v2_v64_experimental.json`.

## 5. Decisiones humanas propuestas

La propuesta es única y agrupada, y está sin firmar: `propuestas/PROPUESTA_HUMANA_4_11.md` y `propuestas/propuesta_humana_4_11.json`. Contiene 13 decisiones, cada una con recomendación argumentada, alternativas, evidencia, efectos calculados y consecuencias de no adoptarla:

- **D411-PLANTILLA:** usar la V6.4 en los ensayos supervisados.
- **D411-N1, D411-N2 y D411-N3:** las convenciones de N1, N2 y N3.
- **D411-PM1-ESTRUCTURA, D411-PM1-PARAMETRO y D411-PM1-CARTERA:** la estructura, el parámetro y las convenciones, y la cartera de P-M1.
- **D411-TERMINAL-R1:** el límite del terminal con R1.
- **D411-P3:** C49, sin efecto en el motor B.
- **D411-C46C47:** la precisión de C46/C47.
- **D411-RF-FUENTE:** incorporar el PDF del Bundesbank.
- **D411-MATERIALIDAD:** qué regla manda cuando un parámetro experimental es material solo para el objetivo (revisión interna H4).
- **D411-DOMINIOS:** avisos, no rechazos, para los dominios que la plantilla no comprueba (revisión interna H13).

Tres propuestas anteriores quedan resueltas por ejecución, porque el encargo las autorizaba como trabajo técnico: D-REBASE, D-EVIDENCIA-2026 y D-MALO-CAPITAL.

## 6. Qué falta para probar la versión con dos o tres empresas ya analizadas (sin iniciarlo)

1. **Decisiones mínimas.**
   - D411-PLANTILLA: usar la V6.4 en ensayos supervisados.
   - D411-MATERIALIDAD: sin ella, cada expediente con P-M1 activa puede terminar en `concluido` o en `pendiente_de_datos` según el criterio de su fase C.
   - Para cada empresa, la configuración de ensayo que se quiere probar (N1, N2, N3 y P-M1), declarada como ensayo. Si las convenciones de Vidrala se dan por buenas (D411-N1 a D411-PM1-CARTERA), sirven de patrón, pero cada empresa necesita sus propias entradas.
2. **Elegibilidad por motor (hecho comprobado).**
   - La capa experimental solo se aplica al motor B.
   - De las seis empresas analizadas en `personaje_v2/empresas_v2/`, cinco usaron el motor A en su expediente original: Aarsleff, Hermès, Nike, Rational y Vidrala (Vidrala usa el B desde el ensayo 4.5). Solo Viscofan usó el B.
   - Por tanto, hoy solo Viscofan, además de Vidrala, puede probarse directamente.
   - Para las demás hay dos caminos: que una fase A nueva elija el motor B por los criterios del personaje (no se puede forzar), o un encargo que extienda la integración al motor A. Esto último está fuera de este encargo.
3. **Datos por empresa.**
   - Circulante comercial del último año: existencias, deudores y acreedores, con su fuente.
   - Análisis del tipo normalizado (como T1) y del margen de partida (como M1), con perímetro y período.
   - Cartera de clientes adquirida, si la hay (P0).
   - Las cinco bases históricas H–L de la Historia, que ya tienen los expedientes V6.3.
   - Para P-M1, al menos la relación entre capex y amortización. Sin datos de mantenimiento (como Q-E1–Q-E3), λ y θ seguirán siendo hipótesis y los ensayos tendrán que enseñar el rango de estructuras.
4. **Preparación.**
   - Un expediente nuevo por empresa, con `cambiar_base.py` si cambia la base económica. Si no cambia, en una carpeta nueva con solo las entradas de partida: `etapa1/`, `fase1_v63.json` y `configuracion_economica.json`. No se copian libros, `estado_pipeline.json` ni salidas V6.3; una copia completa de un expediente V6.3 se detiene con código 2 (H1).
   - Las carpetas de los ensayos, separadas de las de los expedientes V6.3. Sus filas ya van a `resumen_v2_v64_experimental.csv` (H2).
   - Su `configuracion_economica.json`, con trazabilidad completa.
   - Un control heredado (V6.4 en modo heredado = su resultado V6.3) antes del experimental.
5. **Ejecución.**
   - Pipeline completo con agentes reales (extracción, fases A–C y auditoría), en secuencia: unas 1,5–2 horas por empresa con esfuerzo extra.
   - Variantes y evaluación de la fase C.
   - Comparación con el expediente original.
6. **Antes de empezar.**
   - La revisión externa de esta entrega.
   - La corrección de lo que encuentre.
   - Las correcciones que la revisión interna pedía antes de probar otras empresas ya están hechas: H1, H2 y H3. Queda decidir H4 (D411-MATERIALIDAD); H13 (D411-DOMINIOS) pesa sobre todo en empresas con poco activo fijo.
   - Si se quiere, D-FICHA-ETAPA1 y un campo propio en la ficha para la marca de objetivo provisional. El «provisional» del §1 del informe ya está corregido para los expedientes nuevos (H7).
