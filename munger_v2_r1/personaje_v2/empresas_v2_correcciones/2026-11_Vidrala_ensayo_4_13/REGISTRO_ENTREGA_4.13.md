# Registro de la entrega 4.13 · fiabilidad del motor B y conciliación económica de los dos casos

**Qué es.** El registro de la entrega: qué pedía el encargo 4.13 (`ENCARGO_4_13.md`), qué se hizo, qué cambió, qué modelos se usaron, cómo se atendieron las dos revisiones internas y qué queda.

**Dónde está el resto.**
- Resultados, hallazgos externos, límites y aptitud de uso: `INFORME_INTEGRACION_4_13.md`.
- Pruebas: `REGISTRO_PRUEBAS_4_13.md`.
- Vidrala: `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`, `resultados/crecimiento_terminal_vidrala.md`.
- Viscofan: `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`, `resultados/conciliacion_arrendamientos_viscofan.md`, `resultados/alternativas_acciones_viscofan.md`, `viscofan/resultados/`.
- Plantilla V6.4.1: `v6/v641_experimental/` (README, referencia y SHA-256) y `resultados/compatibilidad_v641.md`.
- Comparación con la 4.12: `resultados/comparacion_4_12_4_13.md`.
- Decisiones humanas propuestas, sin firmar: `propuestas/PROPUESTA_HUMANA_4_13.md`.
- Revisión interna: `revision_interna/` (dos pasadas).
- Cuaderno de trabajo: `REGISTRO_AVANCE_4_13.md`; relevos a los agentes: `resultados/relevos_agentes_4_13.md`.
- Controles de las entregas anteriores: `resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`.

## 1. Encargo y resultado

| Entregable (§9) | Estado |
|---|---|
| Código y esquemas | **Hecho.** §2 |
| Plantilla y referencia nuevas | **Hecho.** V6.4.1 experimental, con referencia nueva, SHA-256, selección explícita y compatibilidad con la V6.4; la V6.4 y su referencia no cambian |
| Fuentes y conciliaciones selectivas | **Hecho.** Acciones de Viscofan (nota 20, BORME, CNMV) y arrendamientos 2021–2025; no se rehicieron diez años |
| Comparaciones homogéneas | **Hecho.** `resultados/comparacion_4_12_4_13.md`; alternativas de acciones; θ = 0, 0,5 y 1 con los dos perímetros |
| Expedientes finales con estados y auditorías acordes al material | **Hecho.** Tres expedientes, agentes reales, auditorías APROBADO del material vigente (informe §7) |
| Réplica y pruebas | **Hecho.** Réplica independiente 21 + 21 + 20; batería y ronda general (`REGISTRO_PRUEBAS_4_13.md`) |
| Guía de uso actualizada | **Hecho.** `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` |
| Informe y registros | **Hecho.** Informe con las cuatro separaciones y el estado de cada hallazgo externo; este registro; el de pruebas y el de avance |
| VERSION, CONTINUIDAD, arranque y manifiesto | **Hecho.** `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`; las de la 4.12, en `reproduccion/` |
| ZIP con SHA-256, PARTES y fragmentos de hasta 20 MiB, y registro externo | **Hecho al empaquetar** (§6) |

**Limitaciones que impiden completar una parte.**
- Los bytes de los PDF de BORME y de la CNMV consultados para las acciones de Viscofan no se conservaron: la consola no llega a esos sitios. Las cifras y su página están en la conciliación.
- No hay cifra oficial de acciones de Viscofan al 3-nov-2026.

## 2. Cambios fuera del expediente

La lista completa, con la huella de cada archivo, está en `CAMBIOS_ARCHIVOS.txt` (frente a la 4.12) y en `MANIFIESTO_SHA256.txt`. En breve:
- **Código de `personaje_v2/scripts/`.**
  - Cambian: `pipeline.py`, `cierre_v2.py`, `ficha.py`, `informe.py`, `resumen.py`, `objetivo_v64.py`, `configuracion_economica.py`, `seleccion_plantilla.py`, `entradas_economicas.py`, `dominios_v64.py`, `variantes_configuracion_v64.py`, `comprobacion_conjunta.py`, `leer_v63.py`, `trazabilidad_v64.py`, `volcar_datos_v63.py`, `referencias_mecanicas.py` y `rellenar_fase1_v63.py`.
  - Es nuevo: `estructura_json.py`.
- **Configuración nueva:** `personaje_v2/config_v2_v641_experimental.json`.
- **Plantilla nueva:** `v6/v641_experimental/` (constructor, plantilla, referencia, inventario, verificador, README y SHA-256).
- **Esquemas y prompts:** `fase_c.esquema.json`, `ficha.esquema.json`, `fase_c_turno1.md`, `fase_c_turno2.md` y `verificacion.md`. Los 16 puntos de la auditoría no cambian.
- **Pruebas:** `test_integracion_v64.py` (grupos E y F ampliados, y H nuevo) y `agentes_sinteticos.py`. `verificar_paquete.sh` exige el mínimo nuevo (`REGISTRO_PRUEBAS_4_13.md`).
- **Documentos:** `GUIA_RECORRIDO_SUPERVISADO.md`.
- **No cambian:**
  - las plantillas V6.3 y V6.4 y sus referencias;
  - `config_v2.json` y `config_v2_v64_experimental.json`;
  - el kit y los originales;
  - los expedientes de entregas anteriores, incluidos los de la 4.12.

## 3. Modelos y agentes

| Rol | Modelo y esfuerzo | Nota |
|---|---|---|
| Orquestación, desarrollo e integración | Opus (modelo principal) | — |
| Fases A, B y C (la C en dos turnos con el mismo agente) | Opus, esfuerzo alto | Viscofan: fases A, B y C nuevas; Vidrala: fases C nuevas (dos veces cada una: la segunda, por R4 y R17) |
| Auditorías (paso 13) | Opus, esfuerzo medio, siempre un agente nuevo | Diez lanzadas; una se detuvo antes de escribir porque su material iba a cambiar; dos APROBADO de un material anterior se guardaron sin usarse |
| Revisión interna | **Fable**, contexto separado, solo lectura | Dos pasadas. Motivo: la comprobación de mayor consecuencia, hecha por un modelo distinto del que hizo el trabajo. Se avisó a la persona responsable antes de cada una |

**Alcance de Fable.** Solo las dos revisiones internas. No ejecutó ninguna parte del procedimiento.

**Ejecución en secuencia.** Ningún agente ejecutó el pipeline ni LibreOffice. Los recálculos, las baterías, las sondas y los controles los ejecutó la orquestación, nunca dos a la vez. Los 26 relevos están registrados con su texto.

## 4. Revisiones internas y respuesta

Las tablas completas están en el §6 del informe.
- **Primera revisión (R1–R18):** 1 bloqueante, 6 importantes, 6 menores y 5 observaciones.
  - Corregidos en el código, con prueba: R1, R2, R3, R4, R6, R12 y R17.
  - Corregidos en los datos o en los documentos: R5, R7, R8, R9, R10, R11 y R13.
  - Declarados: R14, R15, R16 y R18.
  - Regenerado todo lo afectado, con agentes reales y auditorías nuevas.
- **Segunda revisión (S1–S14):** 0 bloqueantes, 1 importante, 8 menores y 5 observaciones.
  - Corregidos: S1 y S2 (control de la entrega), S7 (propuesta), S8 (guía) y S14.
  - Declarados: S3, S4, S5, S6, S9, S10 y S11.
  - Sin efecto: S12 y S13.
  - Los expedientes no se tocaron: sus defectos declarados son de textos, no de entradas del motor B.
- **Defectos hallados por las auditorías:**
  - en el informe (§7 y §14): corregidos, con el material regenerado y auditorías nuevas;
  - en la fase A de Viscofan de la 4.12 (C97): fase A rehecha.

## 5. Porcentaje orientativo hacia la primera versión integrada supervisada

**Interpretación, no medición.** No mide seguridad inversora, tiempo restante ni probabilidad de rentabilidad. El encargo partía de ≈75 %. Esta entrega lo lleva a **≈80 %**.

**Qué suma** (unos 5 puntos):
- **Fiabilidad técnica del motor B (unos 2 puntos):**
  - guardas de estructura antes de la vigencia en las cuatro vías;
  - coherencia de la acción final con el objetivo;
  - contrato de cobertura con lo no determinado y el juicio separados del cálculo;
  - avisos de dominio de todas las variantes.
- **Conciliación económica (unos 2 puntos):** perímetro de la inversión versionado (V6.4.1) con conciliación, réplica y dominios; acciones de Viscofan conciliadas y alternativas calculadas; evidencia activa limpia.
- **Interpretaciones de Vidrala corregidas y expedientes regenerados (unos 1 punto).**

**Hitos que quedan antes de un uso con dinero real** (ninguno lo da un porcentaje):
1. Decisiones humanas: D413-FUNDAMENTO, VISCOFAN-ACCIONES, VISCOFAN-PERIMETRO y las configuraciones.
2. Revisión externa de la 4.13.
3. Fundamento de P-M1: desglose del capex.
4. Una tercera empresa de motor B y un contraste fuera de muestra.
5. El motor A.

## 6. Entrega

- **ZIP:** `munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip`.
  - Producido con `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/scripts/empaquetar_zip.py`, sin `__pycache__`, `.lo_perfil/` ni `personaje_v2/pruebas/_v64/`.
  - Con partes de hasta 20 MiB y su `.PARTES.txt`.
  - Comprobado con dos lectores: Python `zipfile` y `unzip`.
- **Huella, tamaño y verificación de la descompresión:** en el registro externo `munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.VERIFICACION.txt`, que va fuera del ZIP porque un ZIP no puede contener su propia huella.
- **Verificación antes de empaquetar:** ronda general sobre una copia limpia del árbol final (`REGISTRO_PRUEBAS_4_13.md`).
- **Controles de las entregas anteriores:** salidas de referencia en `resultados/controles_historicos_en_arbol_4_13/`, explicadas en `resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`.
