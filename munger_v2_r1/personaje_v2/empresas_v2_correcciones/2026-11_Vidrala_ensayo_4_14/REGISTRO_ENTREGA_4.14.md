# Registro de la entrega 4.14 · cierre con verificación completa de las entradas financieras

Encargo: «MUNGER V2 — ENCARGO PRIORITARIO DE CIERRE» (`documentacion_cierre_4_14/ENCARGO_CIERRE.txt`), más el requisito obligatorio «VERIFICACIÓN COMPLETA DE LAS ENTRADAS FINANCIERAS» (`documentacion_cierre_4_14/REQUISITO_VERIFICACION_ENTRADAS.txt`). Base: entrega 4.13 (ZIP SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a`). Fecha: 14-nov-2026.

**Separación.** Los **hechos** se dan con su evidencia. Las *interpretaciones* y las *propuestas* van marcadas. Ningún APROBADO, porcentaje ni recuento acredita aptitud para decisiones con dinero real.

## 1. Qué contiene

| Parte | Dónde | Estado |
|---|---|---|
| Reparación 4.13.1 (H5: vigencia de la publicación y retirada) | código en `personaje_v2/scripts/cierre_v2.py`; registro en `documentacion_cierre_4_14/hito1/REGISTRO_REPARACION_4_13_1.md` | corregida; batería H5 59/59; dos revisiones internas |
| Contrato del juicio sobre el objetivo (materialidad §5) | `scripts/objetivo_v64.py`, `pruebas/test_juicio_objetivo_414.py` | 27/27 |
| Verificación completa de las entradas (requisito) | `scripts/verificacion_entradas.py` (puerta del paso 12, invalidación cuando cambian las entradas), `pruebas/test_verificacion_entradas_414.py` | 33/33; los registros de las tres empresas, con revisor distinto del extractor, son aptos |
| Cambio de base con correcciones de extracción | `scripts/cambiar_base.py` (guardián de entradas `analisis` no declaradas; `correcciones_fase1_partes`) | grupo D 9/9 |
| Viscofan con D3 y E1 | `viscofan_decisiones/Viscofan` | concluido · Vigilar · esperar · objetivo condicionado de 39,80 € · auditoría APROBADO (2.º intento) |
| Vidrala con E1 y E2 (E3 y E4, supuestos) | `vidrala_decisiones/Vidrala` | concluido · Vigilar · esperar · objetivo condicionado de 56,00 € · auditoría APROBADO |
| Elis (tercera empresa) con E6 | `elis_decisiones/Elis` | pendiente_de_datos · Vigilar · sin acción · auditoría APROBADO; motor A no validado con NIIF 16 (F1) |
| Expedientes anteriores conservados | `viscofan/`, `vidrala/` (ramas 4.14), `elis/` (V6.4.1, límite del modelo), `elis_motor_A/` y el incidente `vidrala_decisiones_INVALIDO_perdio_analisis/`; controles de la 4.13 sin tocar | sin cambios |
| Efectos separados | `resultados/efecto_*` y `scripts/efecto_*.py` | reproducen los expedientes con diferencia 0 |
| Decisiones y supuestos | `documentacion_cierre_4_14/DECISIONES_ENTRADAS_4_14.md` | literales; supuestos marcados |
| Hallazgo del motor A con NIIF 16 | `documentacion_cierre_4_14/HALLAZGO_MOTOR_A_NIIF16_4_14.md` | F1 sin decidir; supuesto (a) |
| Matriz del alcance | `documentacion_cierre_4_14/MATRIZ_ALCANCE_4_14.md` | **alcance original no completado** |
| Incidencias | `documentacion_cierre_4_14/INCIDENCIAS_4_14.md` (I1–I21) | declaradas |
| Prueba de traspaso (encargo §10) | `documentacion_cierre_4_14/traspaso/` | agente receptor sin historial sobre el ZIP candidato: verificación PASA, control 35/35, relevo real resuelto y pipeline reanudado; auditoría del relevo no independiente |
| Hitos | `documentacion_cierre_4_14/HITO_0_ARRANQUE.md`, `hito1/`, `HITO_2.md` | — |
| Descargas que ejecutó la persona responsable | `documentacion_cierre_4_14/descargas_bat/` | — |
| Control de la entrega | `scripts/comprobar_entrega_4_14.py` | ver §3 |

## 2. Decisiones de la persona responsable y supuestos de la orquestación

- **Decisiones**, recogidas literalmente: E1 (medias exactas), D3 (acciones de Viscofan a 31-dic-2025, con cinco condiciones), E2 (K14 de Vidrala = 84,994, con reserva) y E6 (Elis con base coherente a 31-dic-2025).
- **Autorizaciones de limpieza**, con las rutas en INCIDENCIAS I11 e I14.
- **Supuestos, reversibles con una decisión explícita:**
  - E3 (pareja de 2023 de Vidrala);
  - E4 (intereses en financiación de Vidrala);
  - F1 = (a): se declara el defecto del motor A y no se corrige;
  - medias exactas en Elis, por el precedente de E1;
  - precio de Elis del 4-nov-2026 con las acciones de 2025, por el mismo criterio que D3.

## 3. Comprobaciones

Las comprobaciones de la candidata y la prueba de traspaso están en `REGISTRO_PRUEBAS_4_14.md` §5 y §6. Las de la final, en el registro externo `…VERIFICACION.txt`.

**Verificación completa de la instantánea de código i5**, sobre una copia (14-nov, 17:51–18:27; registro en `documentacion_cierre_4_14/HITO_2.md` §4): pasan las 12 baterías y el piloto.
- Comprobadores 114/114, sintético 30/30, H5 59/59, juicio sobre el objetivo 27/27, verificación de entradas 33/33, integración V6.4 198/198, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55.
- El manifiesto falla, como se espera en un árbol modificado.

## 4. Limitaciones y pendientes (resumen; detalle en la matriz y en las incidencias)

- **Motor A:** cuenta dos veces los arrendamientos NIIF 16 y los intangibles adquiridos en el ancla f. El precio de Sí de Elis no es una conclusión utilizable. *Propuesta:* corregirlo con la opción (b) de F1, con especificación, referencia, réplica y recorrido.
- **Motor C:** sin recorrido real.
- **Entrada por instrucciones:** sin batería propia.
- **Publicación real:** no se ha ejecutado.
- **Riesgos y avisos registrados en los expedientes:**
  - C48 de Elis: el libro y `fase1_v63.json` no coinciden (I12);
  - Análisis!C42 de Viscofan sigue con la capitalización anterior (no entra en el motor B);
  - el comprobador no detecta un fundamento desfasado si el valor coincide (I13).
- **Traspaso (I18–I20):** documentación corregida en la final. Declarados con propuesta: el relevo caducado sin aviso (I19) y la aptitud por entradas, que no aparece en la ficha V6.3 (I20).
- **Ahold Delhaize (reserva de la tercera empresa):** el .bat está preparado; la persona responsable no lo ha ejecutado ni ha entregado el Excel de la etapa 1.
- **Aptitud de uso:** supervisada y experimental. No es apta para decisiones con dinero real (dictamen §E).
