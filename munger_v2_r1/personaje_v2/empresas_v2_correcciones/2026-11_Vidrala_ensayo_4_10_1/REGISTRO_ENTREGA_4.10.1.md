# Registro de la entrega 4.10.1 · corrección de T-1 y ensayo completo de Vidrala con base 2025

**Qué es.** El registro de la entrega: qué pedía el encargo 4.10.1, qué se hizo, qué cambió (con su motivo y sus huellas), qué modelos se usaron, cómo se atendió la revisión interna y qué queda. Los resultados están en `INFORME_RECORRIDO_4_10_1.md` y `t1/INFORME_T1_4_10_1.md`; las pruebas, en `REGISTRO_PRUEBAS_4_10_1.md`.

## 1. Encargo y resultado

| Resultado pedido | Estado |
|---|---|
| 1. T-1 corregido sin debilitar los controles de producción, con una reconstrucción de bytes inocuos | **Hecho.** Solo cambia la prueba; batería 78/78 (74 de la 4.10, con sus nombres, + 4) |
| 2. Expediente nuevo de Vidrala con base 2025, recorrido y diagnóstico o conclusión legítimos y auditoría nueva | **Recorrido terminado:** pasos 0–14 con agentes reales; concluido · auditoría interna APROBADO · motor B · cubo Vigilar · esperar. **Conclusión financiera pendiente de adopción:** configuración exploratoria no firmada, auditoría interna, revisión externa y decisiones humanas por delante |

## 2. Cambios fuera del expediente (motivo y huellas antes → después)

| Archivo | Motivo | SHA-256 4.10 → 4.10.1 |
|---|---|---|
| `personaje_v2/pruebas/test_trazabilidad_v2.py` | T-1: preparación del grupo L con fichas sintéticas de la identidad del libro acreditado; 4 casos nuevos; H-3 (bytes siempre distintos); nombre de la 4.10 conservado | `6e8649db…07123cc1` → `317fd687…e7d19333` |
| `verificar_paquete.sh` | exige al menos 78 pruebas de trazabilidad | `9299697c…6f87a1b6` → `5c303e4f…784fa232` |
| `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md` | describen la 4.10.1 (las de la 4.10 están en `reproduccion/`) | ver `CAMBIOS_ARCHIVOS.txt` |
| `CAMBIOS_ARCHIVOS.txt`, `MANIFIESTO_SHA256.txt` | regenerados (`scripts/generar_cambios_y_manifiesto.py`) | — |

El código de producción (`personaje_v2/scripts/`), la plantilla, el kit, los originales, las fuentes y los expedientes anteriores conservan sus bytes (lo comprueba `scripts/comprobar_entrega_4_10_1.py`). Todo lo demás es nuevo y está en este expediente.

## 3. Modelos y agentes

| Rol | Modelo y esfuerzo | Nota |
|---|---|---|
| Extracción (paso 5) | Sonnet (configuración) | `extracto_v63.md`; se conservó en la preparación 2 |
| Fase A | Opus, esfuerzo extra (a petición de la persona responsable) | una primera fase A con el esfuerzo de la configuración se detuvo para relanzarla; su parcial está en `antecedentes/fase_a_interrumpida/` |
| Fase B | Opus, esfuerzo extra | — |
| Fase C, turnos 1 y 2 | Opus, esfuerzo extra, un solo agente | el prompt pide el mismo contexto para los dos turnos |
| Auditoría (paso 13) | Opus, esfuerzo extra (la configuración prevé medio) | contexto separado; se identifica como interna |
| Revisión interna | Opus | contexto separado, sin participación en el trabajo |

Fable no se usó. Ningún agente ejecutó el pipeline ni LibreOffice en paralelo con otro; los relanzamientos y recálculos los hizo la orquestación, en secuencia.

## 4. Revisión interna y respuesta

| Hallazgo | Respuesta |
|---|---|
| **H-1 (media):** textos de la etapa 1 en la evidencia del libro final (M41, M52: 3.032,2 mm y 34,185) y una concordancia que decía «ninguno» | La concordancia identifica ahora uno a uno los textos heredados con cifras o fechas de la base anterior (17 en el libro de datos y 15 en el evaluado), separados de los datos del caso, que siguen sin residuos. El informe del recorrido corrige la afirmación. El libro cerrado no se reescribe porque eso exige una auditoría nueva: D-EVIDENCIA-2026 |
| **H-2 (baja):** notas obsoletas en los metadatos activos | Identificadas en la misma salida y en D-EVIDENCIA-2026. No se tocan los archivos de entrada de un expediente ya recorrido |
| **H-3 (baja):** `rezip_inocuo` idempotente | Corregido en la prueba y en `reproducir_T1.py`; comprobación de unidad; 78/78 |
| Avisos: papel de la rf, contadores, precio objetivo por acción de 2025, observaciones sobre las palancas y la fase C, `reproducir_T1.py` | Incorporados al informe del recorrido (§1, §2 y §4); `reproducir_T1.py` comprueba códigos y comprobante y no deja `__pycache__` |
| Aviso: excluir `.lo_perfil/` y `__pycache__/` del ZIP | El ZIP se construye desde una copia limpia de la 4.10 más los cambios, sin esas carpetas |

## 5. Porcentaje orientativo hacia la primera versión integrada supervisada

**≈ 61 %** (punto de partida ≈ 55 %).
- **Por qué sube:** es la primera vez que el sistema recorre de principio a fin, con agentes reales y sin respuestas prefabricadas, un expediente con entradas coherentes y trazables. La base es de 2025, con antecedentes separados, reexpresión declarada de los datos heredados, recálculo, acreditación del libro final, auditoría nueva ligada a su material y publicación aislada. Además, la prueba que falló en la revisión externa ya no depende del entorno.
- **Por qué no sube más:**
  - la conclusión no está adoptada: configuración sin firmar, auditoría interna y revisión externa pendiente;
  - N1–N3 y P-M1 siguen sin integrar;
  - hay propuestas humanas abiertas (8 nuevas y 10 de la 4.10);
  - el cambio de base de un expediente con datos heredados aún no tiene un mecanismo general (D-REBASE);
  - no hay validación en otras empresas.
- **Qué no mide:** no es un porcentaje de pruebas superadas, de tiempo ni de fiabilidad de una inversión.

## 6. Entrega

- ZIP completo: `munger_v2_r1_entrega4.10.1_piloto_2025_y_trazabilidad.zip`, producido con `…_4_10/scripts/empaquetar_zip.py` (nombres UTF-8 marcados) y comprobado con Python `zipfile` y con `unzip`.
- Fuera del ZIP van su `.sha256`, sus partes de hasta 20 MiB si hacen falta (con `.PARTES.txt`) y el registro externo de verificación del ZIP exacto (`…VERIFICACION.txt`).
- Se entregaron antes dos puntos de control, copias de seguridad que no son entregas.
