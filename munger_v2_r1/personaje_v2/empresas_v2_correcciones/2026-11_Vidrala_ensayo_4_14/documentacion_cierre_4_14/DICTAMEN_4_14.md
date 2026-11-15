# Dictamen de la entrega 4.14 (encargo de cierre §11)

Lo emite la orquestación (Claude, Opus). **Es una revisión interna, no una revisión externa ni una firma humana.**

**Separación.** Los **hechos** se dan con su evidencia. Las *interpretaciones* y las *propuestas* van marcadas.

**Regla.** Ninguna función, motor o expediente hereda una aptitud que no se haya demostrado. Un bloqueo no se convierte en aprobación.

## A. Integridad y funcionamiento técnico

- **Hecho.** Verificación completa de la instantánea de código i5, sobre una copia: pasan las 12 baterías obligatorias y el piloto.
  - Las baterías: comprobadores 114/114, sintético 30/30 con los mismos nombres, H5 59/59, juicio sobre el objetivo 27/27, verificación de las entradas 33/33, integración V6.4 198/198, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
  - Ninguna escritura fuera de la copia.
  - Registro: `ronda_i5/verificacion_completa.txt`, resumido en HITO_2 §4.
- **Hecho.** Controles positivos y negativos conservados en las baterías: material cambiado y aprobaciones antiguas, solicitud y respuesta alteradas, configuración externa equivocada, JSON inválido, cierre legítimo y legados, D10/S-19, contradicciones entre acción, objetivo y protocolo, retirada pendiente y recuperación. No se ha eliminado ningún caso ni se ha rebajado ningún mínimo; los mínimos suben a 33 y 198.
- **Hecho.** La integridad del ZIP (SHA-256, CRC, dos lectores, manifiesto después de las verificaciones y ausencia de cachés) se comprueba sobre la descompresión del propio ZIP. Esos resultados van en el registro externo (`…VERIFICACION.txt` e `…INTEGRIDAD_Y_CREDENCIALES.txt`), porque un archivo del ZIP no puede contener la comprobación de sí mismo.
- **Hecho.** El escáner de la plataforma no forma parte de esta comprobación: no se declara superado.
- **Hecho. Traspaso** (encargo §10; `traspaso/LEEME_TRASPASO.md`). Un agente receptor sin historial, solo con el ZIP candidato y el mensaje de arranque:
  - arrancó y verificó el paquete: PASA, control de la 4.14 35/35 y controles históricos como en el LEEME 4.14;
  - resolvió un relevo real: la auditoría pendiente de `elis_motor_A`, en una copia hermana, con `--desde 12` porque la solicitud estaba caducada;
  - reanudó el pipeline hasta el paso 14.
  
  La auditoría de ese relevo la hizo el propio agente receptor, así que no es de contexto separado. Sus observaciones se corrigen en la final (INCIDENCIAS I18); dos tocan código y se declaran (I19 e I20).

## B. Reproducción numérica

- **Hecho.** El precio de Sí de cada expediente final lo reproducen, con diferencia 0,0, los cálculos de efectos con las fases del expediente anterior fijas:
  - Viscofan: 39,79819 €;
  - Vidrala: 56,00201 €;
  - Elis, caso «todo»: 7,30206 €.
  
  Esos cálculos también reproducen el expediente de partida: 40,30282, 56,00201 y 6,55634 €.
- **Hecho.** Réplica independiente en Python, sin LibreOffice y sin los scripts del proyecto (revisión interna; `revisiones/INFORME_REPLICA_4_14.md` y `revisiones/replica_414/`): **185 PASA y ninguna FALLA en los tres expedientes; 89 PASA en los casos de efecto**. La tolerancia es 1e-6 relativa, y la diferencia mayor, de ≈4,7e-15.
  - Expedientes:
    - Viscofan: 29,7797 / 43,7671 / 57,9470, ponderado 43,8056, precio de Sí 39,79819, caro;
    - Vidrala: 44,3217 / 60,1901 / 78,4785, ponderado 60,6741, precio de Sí 56,00201, caro;
    - Elis: 5,5832 / 7,8244 / 10,8915, ponderado 7,9896, precio de Sí 7,30206, caro.
  - El efecto del denominador es un reescalado exacto: Viscofan, solo C55, −0,450571 €; Elis, solo C55, +0,750200 €.
  - No se reproducen el estado técnico del Motor (se lee de la caché), el motor C ni avisos que no forman parte de la escalera.
  - El primer emparejamiento erróneo de un caso de Elis lo corrigió el propio agente sin cambiar el cálculo (informe §5).
- **Hecho.** Elis: la réplica propia de la fase C reproduce la hoja al céntimo.

## C. Fundamento económico por expediente

- **Viscofan** (motor B, V6.4.1, con NIIF 16 como punto de cálculo no adoptado).
  - **Hecho:** concluido · Vigilar · esperar · objetivo condicionado de 39,80 € frente a 54,70 € del 3-nov-2026.
  - **Hecho:** 18 variantes, entre 38,13 y 42,98 €, todas «caro».
  - **Hecho:** las entradas están verificadas, con un revisor independiente.
  - **Hecho:** D3 con sus cinco condiciones cumplidas. Las fechas son distintas: acciones del 31-dic-2025 y precio del 3-nov-2026.
  - *Interpretación:* la zona «caro» es robusta a las variantes calculadas. El objetivo depende de P-M1 (estructura, familia y parámetro), que no está adoptado.
  - **Hecho:** la suficiencia de k = 3 no está demostrada.
- **Vidrala** (motor B, V6.4).
  - **Hecho:** concluido · Vigilar · esperar · objetivo condicionado de 56,00 € frente a 90,10 €.
  - **Hecho:** 19 variantes, entre 51,26 y 65,72 €, todas «caro».
  - **Hecho:** E2 con reserva, +0,049 € si la alternativa se adoptara. E3 y E4 son supuestos.
  - *Interpretación:* igual que en Viscofan.
- **Elis** (motor A, V6.3; tercera empresa).
  - **Hecho:** pendiente_de_datos · Vigilar · sin acción. El reparto del capex entre reposición y crecimiento no se publica.
  - **Hecho:** el motor A cuenta dos veces los arrendamientos NIIF 16 y los intangibles adquiridos (F1). El precio de Sí de la hoja, 7,30 €, **no es una conclusión utilizable**.
  - **Hecho:** sin esa doble cuenta, la réplica de la fase C da un precio de Sí de 11,08 a 21,89 € y un ponderado de hasta 23,42 € frente a 24,18 €: todo «caro», con poca holgura arriba. Solo con r = 0,08, por debajo de la r mínima y no aplicada, se cumpliría la regla.
  - *Interpretación:* el sistema se abstiene correctamente, y **eso no cuenta como objetivo económico cumplido** (encargo §11).

## D. Alcance realmente validado

En `MATRIZ_ALCANCE_4_14.md`: **el alcance original no está completado.**

| Componente | Estado |
|---|---|
| Motor B con la V6.4 / V6.4.1 | recorridos reales en dos empresas, con auditoría y reproducción |
| Motor A | sin validación propia; defecto F1 |
| Motor C | sin recorrido real |
| Entrada desde Excel y desde PDF | recorridas |
| Entrada por instrucciones | sin batería propia |
| Etapa 1 y cambio de base | recorridos, con guardianes probados |
| Publicación real | no ejecutada (no se publica) |

**Interpretación.** La tercera empresa demuestra que la etapa 1, la verificación de las entradas y las fases se transfieren a un tercer caso. **No** es un backtest ni demuestra capacidad predictiva.

## E. Aptitud de uso y restricciones

- **Aptitud: uso supervisado y experimental.** **No es apto para decisiones con dinero real.**
- **Condiciones que faltan:**
  - una revisión externa;
  - la decisión de F1 y, en su caso, la corrección del motor A;
  - la adopción humana de las convenciones experimentales: P-M1, el protocolo del objetivo y k = 3;
  - la validación del motor C;
  - y, para Elis, el dato material del capex.
- **Defectos declarados sin corregir que afectan al uso:**
  - un relevo caducado no se avisa (I19). El fallo es cerrado: no se aprueba nada con otro material;
  - la ficha V6.3 no muestra la aptitud por entradas (I20). En Elis el registro es apto (193/193, en `estado_pipeline.json`), pero la ficha no lo dice.
- La verificación completa de las entradas es una condición necesaria, no suficiente: los controles automáticos comprueban la cobertura, las conciliaciones y la coherencia, no la corrección semántica. Esa la cubre la revisión independiente de las fuentes, que es interna, de Claude, y no humana.
- Ninguna conclusión es una recomendación de compra. Las tres son «esperar» o «sin acción». La posición en cartera la decide la persona responsable.
