# Registro de pruebas · entrega 4.11

**Qué es.** Recoge qué se ejecutó durante el desarrollo de la 4.11, con qué resultado y dónde está la salida. Las cifras son las de las ejecuciones registradas; no se presenta como ejecutado nada que no lo esté.

**Verificación final.** Sobre una copia limpia del ZIP final, con `verificar_paquete.sh completa` y los controles históricos. Va en el registro externo `munger_v2_r1_entrega4.11_integracion_economica_experimental.VERIFICACION.txt`, fuera del ZIP, porque un ZIP no puede contener su propia huella.

## 1. Batería nueva y obligatoria: `personaje_v2/pruebas/test_integracion_v64.py`

Se ejecuta desde `personaje_v2/` con `python3 -B pruebas/test_integracion_v64.py [A B C D]`. En `verificar_paquete.sh completa` es la primera de las obligatorias y exige al menos 58 pruebas, todas en PASA. Tenía 53 al terminar el piloto; la respuesta a la revisión interna añadió cinco (una en B y cuatro en C).

| Grupo | Qué prueba | Resultado en el desarrollo |
|---|---|---|
| A · plantilla (9) | Reconstrucción determinista desde la V6.3 (mismo SHA-256). Verificador ÍNTEGRO. Referencia ligada a la plantilla. V6.3 intacta. Cambios = los declarados (1.994 fórmulas, 16 columnas × 124 filas del Motor + 9 de Diagnóstico + Panel!A1; 4 textos). Gráficos, controles, validaciones y formatos iguales. Una alteración de Motor!DI7 se detecta y se nombra. Versiones cruzadas dan ALTERADO. Inventario = V6.3 + «Configuración V6.4» | 9/9 PASA |
| B · casos (21) | 117 libros recalculados en secuencia: 94 calculan y 23 se rechazan. Detalle debajo de la tabla. Nueva (H6): contraste numérico de BL, BP, BQ y Diagnóstico B176:D177, recalculados en Python desde las entradas de cada fila | 20/20 PASA en el desarrollo; la nueva, en seco sobre los 117 libros de la batería anterior: 91 casos experimentales válidos (71 con P0), 11.284 filas, 0 diferencias (máxima relativa 9,5e-15) |
| C · pipeline (21) | Redacción de las distancias con denominador. Selección explícita: código 2 sin escribir nada en cinco casos, entre ellos el de un expediente que empezó con la V6.3 y se ejecuta con la V6.4 (H1). Con la configuración experimental y la fase A en el motor A: `no_entregable · limite_del_modelo` y `entrada_v63.md` con datos y cobertura separados (H3). Pasada V6.4 experimental con agentes simulados: concluido · APROBADO, con corrección pedida a una fase C sin `configuracion_v64`. Huellas en `plantilla_activa.json`, configuración en los libros, variantes con los extremos del rango de λ (H11), paso 12 con unas variantes alteradas (H10), ficha, informe, material auditado y verificación. Cambiar λ después del cierre: retirada en la primera llamada (`informe.py`, `ficha.py`); el pipeline reaplica, recalcula y pide auditoría nueva. Heredado V6.4 = V6.3 en el pipeline. Resumen propio de las filas V6.4 (H2) | 21/21 PASA en el desarrollo (12-nov, después de las correcciones) |
| D · cambio de base (7) | Preparación reproducible (mismas entradas activas en dos preparaciones). No sobrescribe. La etapa 1 de ensayo solo cambia las celdas declaradas. Notas retiradas. Fechas separadas. Concordancia y ningún resto tras los pasos 0–4. Control negativo sobre la 4.10.1: M41, M52, … | 7/7 PASA (la primera pasada falló por un defecto de la prueba, no del mecanismo: la nota de `fase1_v63.json` cita el nombre del archivo de cambio, que era distinto en las dos preparaciones; se corrigió la prueba) |

**Detalle del grupo B.**

- **Modo heredado frente a la V6.3**, celda a celda (120.168 celdas, tolerancia 1e-12): en los libros 4.6.1 y 4.10.1, 0 diferencias.
- **Referencias.** Reproduce 53:
  - 4.10.1 (1) y 4.6.1 (2), referencias a seis decimales, con |Δ| ≤ 4,2e-7;
  - `…_4_7_1/financiero/matriz.json` (4), con 5,7e-14;
  - `…_4_8_1/financiero/rf_resultados.json` (46), con 7,1e-14.
- **Rechazos (23).** Cada uno da V35 INCOMPLETO, el bloqueo del valor y su motivo.
- **Cero válido** en N1 y N2.
- **Vuelta al heredado** con todas las opciones escritas: igual que la V6.3.
- **Identidades y comprobaciones de la conciliación:**
  - identidad de la conciliación en los años y en el terminal, con los VP;
  - crédito acotado y solo en H;
  - SRF conserva el circulante de S;
  - Rh = 0;
  - R0 sin datos de circulante;
  - R1 con caída (años 1–5), recuperación por debajo del máximo (6–7) y nuevo máximo (8–10);
  - salto del requisito al terminal;
  - DCF inverso y tornado con el modelo activo.
- **Réplica independiente: 117/117.**

**Rechazos añadidos tras la réplica.** La réplica independiente señaló ramas sin caso. Se añadieron nueve rechazos por dominio (N1 y N2 fuera de rango, N2 sin procedencia, circulante negativo, P0 negativo, P0 que no se agota, f no definido, f_fija fuera de [0, 1] y cartera mayor que la amortización) y un caso válido (R0 sin circulante). Con ellos pasaron de 107 a 117 casos.

## 2. Réplica independiente (Fable, contexto separado)

- **Especificación:** `replica/ESPECIFICACION_REPLICA_INDEPENDIENTE.md`. **Guion:** `scripts/replica_independiente_v64.py`, que no lee ninguna fórmula del Excel. **Informe del agente:** `replica/INFORME_REPLICA.md`.
- **Primera ejecución**, sobre los 107 libros congelados con la plantilla anterior al ajuste de trazabilidad (SHA-256 `e21ded39…`; las fórmulas de valoración son las mismas): 107/107 a la primera.
- **Sobre los 117 libros de la plantilla final**, dentro de la batería: 117/117. La salida está en `replica/replica_salida_plantilla_final.txt` y `replica_resultados_plantilla_final.json`.
- **Diferencias máximas:** valores 4,7e-13 €/acción; flujos 6,8e-13; conciliación 5,0e-12; sensibilidades, tornado y DCF inverso 8,8e-13.

## 3. Control heredado limpio frente a la 4.10.1

Guion: `scripts/control_heredado_4_11.py`.

**Ejecución.** La V6.4 en modo heredado recorre el pipeline real hasta el paso 12. Las salidas de los agentes son las de la 4.10.1: es una comparación mecánica, no un análisis nuevo.

**Resultados.**

- V, ponderado (71,664994325), precio de Sí (66,520610325), zona (caro) y estados técnicos: idénticos, |Δ| = 0.
- Libro evaluado recalculado: 120.168 celdas y 44 diferencias, todas en el Control maestro (evidencia reescrita por el cambio de base) o en la fecha de análisis (D4 y sus copias).
- `cambiar_base.py comprobar`: **CONCUERDA Y SIN RESTOS**. La primera pasada encontró cuatro restos y se corrigió la configuración:
  - M44, la cifra «LTM» de los doce meses a 30-jun-2026;
  - K45/L45, el informe semestral 1S2026 y su página G-16;
  - la nota propia de metadatos, que nombraba las fuentes retiradas.

Salidas: `control_heredado/resultados/control_heredado.json/.md` y `control_heredado/resultados/cambio_de_base.json/.md`.

## 4. Regresión de las baterías existentes con el código modificado

**Ejecución.** Sobre una copia del árbol de trabajo, con `verificar_paquete.sh completa` antes de añadir la batería nueva.

**Resultado: todo PASA** salvo el manifiesto, que falla porque la copia tiene los archivos cambiados (esperado):

- entorno y piloto (35);
- `test_comprobadores.py` 114/114;
- sintética 30/30, con los mismos 30 nombres que la línea de base v2.2;
- trazabilidad 78/78;
- integridad 103/103;
- solicitudes 55/55;
- estados 28/28;
- resumen 45/45;
- cierre 55/55.

## 5. Controles históricos durante el desarrollo

Se ejecutaron sobre el árbol de trabajo, en secuencia:

- 4.2, 4.3, 4.3.1, 4.4 y 4.5: salidas idénticas a las de referencia.
- 4.6 (23 de 24): idéntica, por la reparación declarada Z-1.
- 4.6.1: primero dio 22 de 23. El nuevo bloque de `verificar_paquete.sh` estaba entre el de cierre y el resultado global, y el control de integración de la 4.6.1 extrae ese tramo. El bloque se movió para que sea el primero de los obligatorios, como hicieron las entregas anteriores. Ahora da 23 de 23, idéntica.
- Controles de extracción de bloques de la 4.7 a la 4.9: 13 de 13. La 4.7 da 12 de 13, igual que en el árbol 4.10.1.

Los demás controles, ligados a las huellas de su versión, se documentan en `resultados/LEEME_BATERIAS_HISTORICAS.md` con las salidas de la copia limpia.

## 6. Verificación completa sobre una copia limpia del árbol de la entrega (12-nov, antes de empaquetar)

**Copia.** El árbol de trabajo sin `.lo_perfil/`, `__pycache__/` ni `personaje_v2/pruebas/_v64/`: 2.679 archivos, todos con la huella del manifiesto regenerado. Después se hizo un último cambio de presentación en `informe.py` (la marca «provisional» del §1 corta las hipótesis por palabra y no a 80 caracteres) y en documentos; la verificación del ZIP final, en el registro externo, ya los incluye.

**`bash verificar_paquete.sh completa`: RESULTADO GLOBAL: PASA, código 0**, en 18 min (14:13:48 a 14:31:53):

- manifiesto, entorno y contraste del piloto (35 CUMPLEN, salida idéntica);
- `test_comprobadores.py` 114/114 y sintética 30/30, con los mismos nombres que la línea de base;
- **integración V6.4: 58/58**. El contraste numérico nuevo (H6) dio 91 casos experimentales válidos (71 con P0), 11.284 filas y 0 diferencias; la réplica independiente, 117 de 117 casos;
- trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.

**Controles de las entregas sobre la misma copia, después de la verificación** (salidas de referencia y explicación en `resultados/LEEME_BATERIAS_HISTORICAS.md`):

- tabla 1: 4.2, 4.3 (217/217), 4.3.1 (43/43), 4.4 (72/72), 4.5 (60/60) y 4.6.1 (23/23), con salidas idénticas a las de referencia;
- tabla 2: 4.6, 23 de 24, idéntica a la del árbol 4.10.1;
- tabla 3: las dos comparaciones de baterías, idénticas; 4.7 (45/49), 4.7.1 (38/44), 4.8 (32/36), 4.8.1 (27/30) y 4.9 (35/39), con los recuentos del árbol 4.10.1; 4.10 (40/44) y 4.10.1 (38/43), por los cambios de la propia 4.11;
- control de la 4.11: **38 de 38**.

**Referencia de la 4.9.** Su salida lista entero cada archivo nuevo del manifiesto, y las salidas de referencia de la 4.11 también lo son. En la primera descompresión del ZIP, la 4.9 dio el mismo recuento (35 de 39) con una lista distinta: la tomada en la copia limpia no tenía esos archivos. La referencia se tomó de esa descompresión y se volvió a empaquetar y comprobar.

**Incidencia del control de la 4.11.** La primera pasada sobre la copia dio 37 de 38. La comprobación de los archivos nuevos contaba las salidas que las baterías de `verificar_paquete.sh completa` escriben en `personaje_v2/pruebas/` (`resultado_comprobadores.json`, `sintetico/…`). Por la regla del LEEME, esas salidas no cuentan. Se corrigió la lista del árbol en `comprobar_entrega_4_11.py`: ahora no cuenta los archivos de `pruebas/` que no están en el manifiesto del propio árbol. La segunda pasada, sobre la misma copia, dio 38 de 38.

