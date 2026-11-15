# Registro de pruebas de la entrega 4.14

## 1. Durante el desarrollo (pruebas dirigidas)

| Batería o prueba | Qué cubre | Resultado | Dónde |
|---|---|---|---|
| `test_vigencia_h5.py` | reparación 4.13.1 (H5) | 59/59 | hito1 |
| `test_juicio_objetivo_414.py` | contrato del juicio sobre el objetivo | 27/27 | hito1 |
| `test_verificacion_entradas_414.py` | verificación de las entradas: cobertura, cita con la cifra completa, vacío ≠ cero, escala y signo, derivaciones, revisor distinto, hipótesis con discrepancia o pendiente, invalidación, aptitud en la ficha y en el informe, material auditado | 33/33 | este registro |
| `test_integracion_v64.py` grupo D | cambio de base: reproducibilidad, no sobrescribir, guardián de `analisis` y correcciones de `fase1_partes` | 9/9 | este registro |
| `test_integracion_v64.py` grupo F | materialidad y protocolos (adaptado al contrato 4.14) | 54/54 | hito1 |

## 2. Verificación completa de la instantánea de código i5

`resultados/bateria_completa_i5_4_14.txt`: 14-nov-2026, de 17:51 a 18:27, sobre una copia de `instantaneas/i5`. Las huellas están en `resultados/huellas_instantanea_i5.txt` y el diff frente a i4, en `resultados/cambios_i5_frente_a_i4.diff`.

- **Pasa:** entorno, piloto (35), comprobadores 114/114, sintético 30/30 (mismos nombres), H5 59/59, juicio sobre el objetivo 27/27, verificación de las entradas 33/33, integración V6.4 198/198, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
- **Falla el manifiesto,** como se espera en un árbol modificado. Ninguna escritura fuera de la copia.

## 3. Expedientes reales (agentes reales, sin agentes sintéticos)

| Expediente | Auditoría | Registro de las entradas | Reproducción |
|---|---|---|---|
| `viscofan_decisiones/Viscofan` | APROBADO (2.º intento; el 1.º, REPETIR por un texto de la configuración) | apto: 232 de 232 celdas, revisor independiente | efectos (diferencia 0) y réplica independiente (PASA) |
| `vidrala_decisiones/Vidrala` | APROBADO | apto: 226 de 226 | efectos (0) y réplica (PASA) |
| `elis_decisiones/Elis` | APROBADO | apto: 193 de 193 | efectos (0; «todo» = expediente nuevo) y réplica (PASA) |

## 4. Réplica independiente

`documentacion_cierre_4_14/revisiones/INFORME_REPLICA_4_14.md`: 185 PASA en los expedientes y 89 en los casos de efecto, ninguna FALLA (revisión interna).

## 5. Candidata (ZIP SHA-256 `f9f888e393bd90e699a031e66d9d553067d4f38c0e6414837fc1e0299b4f5a24`)

Sobre la descompresión de la candidata, en secuencia:
- **Integridad.** CRC correcto. Las extracciones con Python y con unzip son idénticas byte a byte. Manifiesto: 6.694 archivos, sin modificados, ausentes ni de más.
- **Verificación completa.** `bash verificar_paquete.sh completa` (19:18–19:54): RESULTADO GLOBAL PASA, código 0 (`resultados/bateria_completa_candidata_4_14.txt`).
- **Control de la 4.14.** 35/35 (`resultados/comprobar_entrega_4_14_candidata.txt`).
- **Controles históricos.** Los resultados y su explicación están en `resultados/LEEME_CONTROLES_HISTORICOS_4_14.md` y `resultados/controles_historicos_en_arbol_4_14/`. El primer intento se detuvo por falta de disco (INCIDENCIAS I17).

## 6. Prueba de traspaso (encargo §10)

Un agente receptor sin historial trabajó solo con el ZIP candidato y el mensaje de arranque (`documentacion_cierre_4_14/traspaso/`):
- **Verificación completa.** PASA, código 0 (20:24–21:00).
- **Control de la 4.14.** 35/35.
- **Controles históricos.** Los mismos resultados que el LEEME 4.14.
- **Relevo real.** `elis_motor_A/Elis` se resolvió en una copia hermana con `--desde 12`: solicitud SA-21babb1dd24901d1, APROBADO y paso 14, `pendiente_de_datos`. La auditoría la hizo el propio agente receptor, no un agente de contexto separado.
- Después del relevo, el control de la 4.14 sigue en 35/35 y el `elis_motor_A` original no cambia.

Las observaciones del agente están en INCIDENCIAS I18–I20.

## 7. Final

La integridad del ZIP final (SHA-256, CRC, extracción con dos lectores, manifiesto después de las verificaciones y ausencia de cachés) y las comprobaciones sobre su descompresión van en el registro externo de verificación del ZIP (`…VERIFICACION.txt`). Un archivo del ZIP no puede contener la comprobación de sí mismo.
- **Cambios frente a la candidata:** solo documentos. Son los de CONTINUIDAD, el mensaje de arranque, la guía, la matriz, HITO_2, las incidencias, el dictamen y los registros, más la evidencia del traspaso y las copias de resultados. Ningún código ni expediente cambia (`CAMBIOS_ARCHIVOS.txt`).
- Por eso la final repite lo que esos cambios pueden invalidar: el manifiesto, la extracción doble y el control de la 4.14.
