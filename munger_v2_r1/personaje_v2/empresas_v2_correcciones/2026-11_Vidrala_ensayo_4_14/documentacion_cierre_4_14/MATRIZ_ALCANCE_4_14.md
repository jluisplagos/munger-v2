# Matriz del alcance original · Munger v2 · 4.14 (encargo de cierre §8)

**Estado del documento:** versión final de la 4.14, 14-nov-2026. Sustituye a la versión del hito 2 (que daba las auditorías y Elis «en curso»; INCIDENCIAS I18) y al «borrador» que anunciaba el hito 1, que no llegó a escribirse como archivo.

**Columnas:**
- *Existe*: hay código o plantilla.
- *Verificada*: hay una prueba o un recorrido real con evidencia conservada, y se indica cuál.
- *Pendiente*: lo que falta.
- *Evidencia necesaria*: qué cerraría el pendiente.

**Regla del encargo:** no se declara completado el alcance original mientras un componente requerido siga sin validar. **Con esta matriz, el alcance original NO está completado.**

**Separación entre hechos, interpretaciones y propuestas:**
- Las celdas *Existe* y *Verificada* son **hechos**, con su evidencia.
- *Pendiente* es una **interpretación** de lo que falta.
- *Evidencia necesaria* es una **propuesta**.

## 1. Motores y modos

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| **Motor B** (financiación cambiante) con la plantilla V6.4 experimental | sí: plantillas V6.4 y V6.4.1, `configuracion_economica.json`, variantes | **Recorridos reales en la 4.14, con auditoría APROBADO:**<br>• `viscofan_decisiones/Viscofan` (D3 y E1; V6.4.1): concluido · esperar, auditoría SA-bdff49a38c72fabd en el 2.º intento;<br>• `vidrala_decisiones/Vidrala` (E1 y E2; E3 y E4, supuestos; V6.4): concluido · esperar, auditoría SA-fa0472f6bde97775.<br>Cálculo mecánico independiente: precio de Sí reproducido con diferencia 0,0 (`resultados/efecto_*`) y réplica independiente sin errores (`revisiones/INFORME_REPLICA_4_14.md`). Batería V6.4: 198/198. | La suficiencia económica de la convención k = 3 no está demostrada (D11). P-M1, los protocolos del objetivo y k = 3 no están adoptados. | Adopción humana de las convenciones; revisión externa |
| **Motor A** (financiación estable), plantilla V6.3 | sí | Recorridos V6.3 anteriores con auditoría APROBADO: Rational, Hermès, Aarsleff, Nike y Vidrala 4.x (`RESUMEN_EMPRESAS.md`). En la 4.14, `elis_decisiones/Elis` (APROBADO, SA-d58921ca0d0cf0fa). **No hay validación económica propia** (§8: «no heredará la validación… del motor B»). | **Defecto encontrado en la 4.14:** el ancla f del motor A cuenta dos veces los arrendamientos NIIF 16 y los intangibles adquiridos (`documentacion_cierre_4_14/HALLAZGO_MOTOR_A_NIIF16_4_14.md`). Decisión F1 pendiente de la persona responsable; la orquestación supone (a). La ficha V6.3 no muestra la aptitud por entradas (I20). | Especificación, referencia, réplica y recorrido representativo de la corrección (opción b de F1) |
| **Motor A con la plantilla V6.4** | no | — | La V6.4 solo cubre el motor B. El pipeline lo declara como «límite del modelo» y no fuerza el motor (Elis 4.14: `elis/`, `no_entregable · límite del modelo`). | Ampliación de la V6.4 al motor A con especificación propia |
| **Motor C** (banco o aseguradora) | plantilla V6.3 con reglas propias (B16:D16) | solo los dos fixtures sintéticos del motor C en `v6/` | ningún recorrido real | Empresa financiera real con datos oficiales y recorrido completo |
| Caso «otro método» / límite del modelo | sí: C62 y `limite_del_modelo` | recorrido real Elis V6.4.1 (cierra como `no_entregable` sin forzar el motor) | — | — |

## 2. Entrada

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Entrada desde Excel (V5.3 decidida por el v1 + V6.3 con datos) | sí (D2) | recorridos de Viscofan y Vidrala | — | — |
| Entrada desde PDF (`pdf_a_texto.py`, `fase1_historia.py`) | sí | Elis: Historia 2016–2025 construida desde los PDF oficiales descargados por la persona responsable; números con separador de miles con espacio admitidos y probados (`fase1_historia.numero`). Registro de Elis revisado por un revisor independiente (`revisiones/REVISION_INDEPENDIENTE_ELIS_REGISTRO.md`) y, tras E6, apto: 193 de 193 celdas del universo | — | — |
| Entrada desde instrucciones (sin libro previo) | parcial: prompts `historia_anio.md` y `metadatos_fase1.md` | Elis (etapa 1 con instrucciones por año) | sin batería propia | prueba dirigida de la entrada por instrucciones |
| **Verificación completa de las entradas financieras** (requisito obligatorio) | sí: `verificacion_entradas.py`, puerta en el pipeline, invalidación cuando cambian las entradas | Batería 33/33. Los registros de los tres expedientes finales, con un revisor distinto del extractor, son aptos (`comprobar_entrega_4_14.py`). El texto de Palancas!C47 del registro de Viscofan está confirmado (`revisiones/revision_C47_viscofan_decisiones.json`). | Los controles automáticos no comprueban la corrección semántica; el comprobador no detecta un fundamento desfasado cuando el valor coincide (I13). En la V6.3, la aptitud por entradas no aparece en la ficha (I20). | Revisión externa de las fuentes; propuestas de I13 e I20 |

## 3. Etapa 1 y transferencia al análisis

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Etapa 1 (extracción con fuente y página) | sí | Viscofan: 9 años re-extraídos desde ediciones conservadas; solo cambiaron 16 celdas, todas confirmadas por el revisor. Elis completa. | Ahold Delhaize (reserva): la persona responsable aún no ha entregado el Excel de la etapa 1 ni ha ejecutado el .bat | — |
| Cambio de base sin tocar el origen (`cambiar_base.py`) | sí | Prueba del grupo D, 9/9, con el guardián frente a análisis no declarados y las correcciones de extracción (`correcciones_fase1_partes`). Incidente real detectado y corregido (Vidrala, decisiones v1). Recorrido real: Elis E6 | — | — |

## 4. Fases de juicio

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Fases A, B y C (dos turnos) con agentes reales | sí | Viscofan, Vidrala y Elis (expedientes de decisiones, con la regla de rama); Elis V6.4.1 (fase A) | variación entre agentes (B5): se explica, no se elimina | — |
| Contrato del juicio sobre el objetivo 4.14 (materialidad §5) | sí | batería 27/27; integración F 54/54 | — | — |

## 5. Valoración, variantes y auditoría

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Precio de Sí, escalera y zonas (Anexo C) | sí | reproducción exacta en los tres expedientes finales y réplica independiente | suficiencia de k = 3 no demostrada | — |
| Variantes de configuración V6.4 | sí | Viscofan: 18 variantes entre 38,13 y 42,98 €; Vidrala: 19 entre 51,26 y 65,72 €; todas «caro» | — | — |
| Auditoría independiente (paso 13) | sí | Baterías: integridad 103/103 y solicitudes 55/55. Auditorías reales APROBADO de los tres expedientes finales (la de Viscofan, en el 2.º intento tras un REPETIR real) | Las ramas 4.14 y `elis_motor_A` están sustituidas y sin auditar (§2, punto 6 de CONTINUIDAD). Un relevo caducado no se avisa (I19) | propuesta de I19 |

## 6. Publicación, actualización, retirada y recuperación

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Publicación, vigencia, retirada y recuperación (H5) | sí: `cierre_v2.py` | baterías H5 59/59 y cierre 55/55; dos revisiones internas | límite declarado: una restauración total de una copia de seguridad no se detecta desde dentro | — |
| Publicación real | — | **no se publica** (regla de la ventana) | — | — |

## 7. Traspaso (encargo §10)

| Función | Existe | Verificada | Pendiente | Evidencia necesaria |
|---|---|---|---|---|
| Continuidad sin historial | sí: `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, guía del recorrido | Agente receptor sin historial sobre el ZIP candidato: verificación completa PASA, control de la 4.14 35/35, relevo real de `elis_motor_A` resuelto en una copia y pipeline reanudado hasta el paso 14 (`documentacion_cierre_4_14/traspaso/`) | La auditoría del relevo la hizo el propio agente receptor, no un agente de contexto separado. Las dificultades que encontró se corrigen en la final (I18); dos se declaran con propuesta (I19 e I20) | Repetir el traspaso sobre la final con un agente que pueda lanzar auditores |

## 8. Tercera empresa (Elis)

- **Hechos.**
  - La selección se justificó antes de conocer el resultado (`hito1/SELECCION_TERCERA_EMPRESA.md`).
  - Datos oficiales: los descargó la persona responsable y quedaron documentados. La configuración es propia y quedó congelada antes de evaluar.
  - Con la V6.4.1 la fase A eligió el motor A, y el cierre fue `no_entregable · límite del modelo`: no se forzó el motor B.
  - El expediente final `elis_decisiones/Elis` (E6, base coherente a 31-dic-2025; motor A, V6.3) está en `pendiente_de_datos · APROBADO · Vigilar · sin acción`. Falta el reparto del capex entre reposición y crecimiento, que no se publica.
  - El recorrido anterior con el motor A (`elis_motor_A/`) se conserva en el paso 13, sustituido.
- **Por el hallazgo NIIF 16, el precio de Sí del motor A (7,30 €) no es una conclusión utilizable.** Sin la doble cuenta, la réplica de la fase C da de 11,08 a 21,89 € frente a 24,18 €: todo «caro».
- **Interpretación.** Elis demuestra la transferencia de la etapa 1, de la verificación de entradas y de las fases de juicio a un tercer caso. No demuestra una valoración utilizable con dinero real. Tampoco es un backtest.
