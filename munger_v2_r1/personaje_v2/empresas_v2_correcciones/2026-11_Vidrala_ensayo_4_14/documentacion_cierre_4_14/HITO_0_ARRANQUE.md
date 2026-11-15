# Munger V2 · encargo prioritario de cierre · Hito 0: arranque

Sábado 14-nov-2026, 10:15 (Europa/Ámsterdam). Base: `munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip`, SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a`.

## 1. Estado de la base (hechos comprobados)

| Comprobación | Resultado | Evidencia |
|---|---|---|
| SHA-256 del ZIP | coincide (478 487 657 bytes) | recalculado hoy |
| CRC | correcto en los 4592 archivos, sin cifrado | `…INTEGRIDAD_Y_CREDENCIALES.txt` del 13-nov; se reutiliza porque el SHA-256 de hoy es el mismo |
| VERSION | `munger_v2 · r1 · entrega 4.13 … · 2026-11-13 · base SHA-256 61c70800…` | leído de la extracción de hoy |
| Manifiesto | 4591 archivos: 0 distintos, 0 ausentes, 0 de más | comprobado hoy sobre una extracción nueva |
| Batería y controles | ronda C del 13-nov sobre la descompresión de estos mismos bytes: PASA, 195/195, 20 salidas idénticas a su referencia | `…VERIFICACION.txt`; se reutiliza sin presentarla como ejecución nueva |

La extracción de la base es de solo lectura y no se modificará. El trabajo se hará sobre copias.

**Incidencia del entorno:** el contenedor se reinició esta mañana, pero los archivos de trabajo se conservaron.

## 2. Capacidad disponible (hechos)

| Recurso | Disponible | Consecuencia |
|---|---|---|
| Máquina | 2 núcleos, 7 GB de memoria, 22 GB libres | La batería completa tarda unos 37 min y los controles históricos unos 30 min: unos 70 min por ronda general. LibreOffice y los pipelines siempre en secuencia; nunca dos a la vez. |
| Agentes | subagentes de Claude (Opus) con contexto separado, cada uno con su copia | Su revisión es **interna**, aunque sea independiente del autor. Solo un responsable integra en los archivos compartidos. |
| Fable | disponible | Se avisará antes de cada uso, como en las entregas anteriores. |
| Red desde la consola | ninguna (comprobado hoy con cnmv.es, boe.es, viscofan.com y vidrala.com) | Las búsquedas y la lectura web dan **texto**. Los PDF oficiales no se pueden guardar con sus bytes desde aquí (bloqueo B3). |
| LibreOffice / Python | 24.2.7 / 3.13 | Los mismos que en la ronda C. |

## 3. Plan (propuesta de organización)

Se trabaja en cuatro frentes, con copias y salidas propias. Los trabajos que usan LibreOffice van en una sola cola.

- **A · H5, vigencia y coherencia del cierre** (responsable de la integración; primero). Reproducir el H5 externo y corregir su causa compartida en las cuatro vías.
  - Pruebas dirigidas de §4: cuatro primeras llamadas, ausencias individuales y combinadas, material intacto/cambiado/ilegible, sin salidas oficiales, destino inaccesible, idempotencia, restauración de archivos antiguos, intervalo auditoría → paso 14 y recuperación con una auditoría nueva.
  - Sale como **reparación 4.13.1**, con su propio registro.
- **B · Materialidad y evidencia económica** (agente de investigación en paralelo; los cambios de código los integra A).
  - Separar la justificación de la acción de la del objetivo (§5), y S3/S11.
  - Fundamento de P-M1 (desglose del capex), acciones y fechas de Viscofan, perímetro y arrendamientos.
  - Descomposición de +1,5386 € y −0,6623 €; S4/S5 en una rama separada del control congelado.
  - Fuentes que faltan.
  - Paquete de decisiones con recomendación, alternativas, evidencia y efectos, **hoy mismo**.
- **C · Alcance y validación adicional** (agente en paralelo, sin LibreOffice).
  - Matriz del alcance original (motores A/B/C y modos; entrada desde Excel, instrucciones y PDF; etapa 1 y transferencia; fases de juicio; valoración, variantes y auditoría; publicación, actualización, retirada y recuperación).
  - Selección justificada de la tercera empresa, antes de conocer su resultado.
  - Preparación de la validación del motor A desde su propia definición económica.
- **D · Revisión y traspaso.**
  - Revisión interna independiente de cada hito.
  - Guía de arranque, prompt de continuación y prueba con un agente receptor sin historial.

**Calendario objetivo** (objetivos de publicación, no de resolución):

| Hito | Objetivo | Contenido |
|---|---|---|
| 0 · arranque | ahora | este documento |
| 1 · primera instantánea | sábado ≈ 13:00–14:00 | H5 reproducido y corregido con pruebas dirigidas (paquete pequeño ligado al SHA de la base); matriz del alcance en borrador |
| 2 · primer día | sábado noche | 4.13.1 revisada; paquete de decisiones; primeras evidencias económicas; selección de la tercera empresa |
| 3 · mitad de la ventana | domingo ≈ 22:00 | materialidad separada; S4/S5; descomposición de Viscofan; tercera empresa en curso; resultados de validación y bloqueos concretos |
| 4 · candidata 4.14 | lunes ≈ 14:00 | paquete completo para la revisión externa: congelación, auditorías, batería, controles, recorrido real, réplica e integridad |
| 5 · final | martes por la mañana | correcciones de bloqueantes, comprobaciones repetidas y dictamen A–E |

Los hitos intermedios irán en paquetes pequeños de cambios y evidencia, ligados al SHA de la base. Las 23 partes solo se generarán para la candidata y la final.

## 4. Bloqueos conocidos

1. **B1 · Decisiones humanas pendientes:** D413-FUNDAMENTO (criterio de materialidad), VISCOFAN-ACCIONES, VISCOFAN-PERIMETRO y las configuraciones de cada caso. No se firman ni se adoptan aquí. Se presentarán hoy con recomendación, para resolverlas en paralelo.
2. **B2 · P-M1 sin desglose del capex.** Puede que las empresas no publiquen el desglose entre mantenimiento y crecimiento. Si no se encuentra, se propondrá un método de estimación replicable, con sus supuestos y límites. Si tampoco se puede acotar de forma defendible, el sistema debe abstenerse en la conclusión afectada, y eso no cuenta como objetivo económico cumplido.
3. **B3 · Bytes de fuentes oficiales.** Sin red desde la consola, los PDF de BORME, CNMV, Bundesbank y los informes nuevos no se pueden guardar con sus bytes. Acción concreta: la persona responsable descarga los documentos de una lista que se le pasará y los adjunta. Mientras tanto se declaran como fuentes solo en texto web.
4. **B4 · Alcance original.** Es poco probable validar en tres días el motor A, el motor C, la entrada desde PDF, la etapa 1 y todo lo que queda fuera del motor B. Se prepararán y se medirán en la matriz, pero no se declarará completado el alcance si falta algo. La tercera empresa necesita sus propios datos oficiales y un recorrido completo; es el trabajo más largo y con más riesgo de no terminar.
5. **B5 · Variación del juicio entre agentes** (S10: +1,54 € en Viscofan). Afecta a la reproducibilidad del objetivo y no se resuelve con código; se explicará y delimitará (frente B).
6. **B6 · Escáner de la plataforma.** La parte00 de un ZIP partido no pasa la comprobación automática de credenciales; con la parte00 de la 4.13 hizo falta elegir «Send it». Para los hitos se enviarán paquetes pequeños. Para la candidata se repetirán las comprobaciones propias, sin presentar como superado el escaneo de la plataforma.
7. **B7 · Límite de uso de la cuenta de Claude**, que desde aquí no se ve. Si se corta la sesión, el paquete y los hitos permiten retomar.

## 5. Siguiente acción

Reproducir H5 en cuatro copias independientes del piloto 4.11 (frente A) y lanzar en paralelo los agentes de B y C, sin LibreOffice.
