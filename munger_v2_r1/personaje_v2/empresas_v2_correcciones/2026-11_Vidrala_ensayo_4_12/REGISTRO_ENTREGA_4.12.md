# Registro de la entrega 4.12 · validación supervisada, cierre de la integración y contraste con Viscofan

**Qué es.** El registro de la entrega: qué pedía el encargo 4.12, qué se hizo, qué cambió, qué modelos se usaron, cómo se atendió la revisión interna y qué queda.

**Dónde está el resto.**
- Resultados, límites y aptitud de uso: `INFORME_INTEGRACION_4_12.md`.
- Pruebas: `REGISTRO_PRUEBAS_4_12.md`.
- Vidrala: `REVISION_ECONOMICA_VIDRALA_4_12.md` y `COMPARACION_PROTOCOLOS_4_12.md`.
- Viscofan: `viscofan/CONTRASTE_VISCOFAN_4_12.md`.
- Decisiones humanas propuestas, sin firmar: `propuestas/PROPUESTA_HUMANA_4_12.md`.
- Revisión interna: `revision_interna/`.
- Cuaderno de trabajo: `REGISTRO_AVANCE_4_12.md`.
- Controles de las entregas anteriores: `resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`.

## 1. Encargo y resultado

| Entregable (§9) | Estado |
|---|---|
| 1. Código, pruebas, configuraciones y formatos, con documentación de uso y guía breve del recorrido supervisado | **Hecho.** Lista en §2; batería de 127 pruebas; Anexo D §D.13; README de la V6.4 §9; `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` |
| 2. Expedientes nuevos de Vidrala y Viscofan, controles heredados, variantes, conciliaciones y réplicas | **Hecho.** `cierre_condicionado/`, `cierre_bloqueo/`, `control_palancas_4_11/` y `viscofan/` (fuentes, reproducción del heredado, configuración y expediente experimental), con sus variantes, comparaciones homogéneas, datos de revisión económica y réplicas |
| 3. Informe integrado | **Hecho.** `INFORME_INTEGRACION_4_12.md`, con la evaluación de aptitud en el §9 |
| 4. Propuesta humana única y breve, sin firmas | **Hecho.** `propuestas/PROPUESTA_HUMANA_4_12.md`: 8 decisiones, 6 de uso del sistema y 2 elecciones económicas |
| 5. Registro de cambios, revisión interna, VERSION, CONTINUIDAD, arranque, manifiesto y registro externo de verificación | **Hecho.** Este archivo, `revision_interna/`, `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`; las versiones de la 4.11 están en `reproduccion/`. El registro externo va fuera del ZIP |
| 6. ZIP con SHA-256 y partes de hasta 20 MiB | **Hecho al empaquetar** (§6) |

**Limitación que impide completar una parte.** La fuente oficial de rf (PDF del Bundesbank) no se pudo incorporar con sus bytes. La consola no llega a bundesbank.de y la carpeta conectada no la tenía. Se registró el contraste textual y se continuó (§6 del encargo).

## 2. Cambios fuera del expediente

La lista completa, con la huella de cada archivo, está en `CAMBIOS_ARCHIVOS.txt` (frente a la 4.11) y en `MANIFIESTO_SHA256.txt`. El resumen por archivo, en el §4 del informe integrado. En breve:
- **Código de `personaje_v2/scripts/`:** `pipeline.py`, `cierre_v2.py`, `seleccion_plantilla.py`, `ficha.py`, `informe.py`, `resumen.py`, `variantes_configuracion_v64.py`, `comprobacion_conjunta.py`, `configuracion_economica.py`, `comprobar_gramatica.py` y `volcar_datos_v63.py` cambian; `objetivo_v64.py`, `entradas_economicas.py`, `dominios_v64.py`, `trazabilidad_v64.py` y `comparar_zip.py` son nuevos.
- **Esquemas y prompts:** `fase_c.esquema.json`, `ficha.esquema.json`, `fase_c_turno1.md`, `fase_c_turno2.md` y `verificacion.md` (los 16 puntos de la auditoría no cambian).
- **Pruebas:** `test_integracion_v64.py` (grupos E, F y G; 127 pruebas) y `agentes_sinteticos.py`; `verificar_paquete.sh` exige al menos 127.
- **Documentos:** Anexo D, README de la V6.4 §9 y `GUIA_RECORRIDO_SUPERVISADO.md` (nueva).
- **No cambian:** las plantillas V6.3 y V6.4 y su referencia, `config_v2.json`, el kit, los originales y los expedientes de entregas anteriores, incluido el piloto 4.11.

## 3. Modelos y agentes

| Rol | Modelo y esfuerzo | Nota |
|---|---|---|
| Orquestación, desarrollo e integración | Opus (modelo principal), esfuerzo máximo | — |
| Extracción (paso 5) | Sonnet, esfuerzo medio (el de la configuración) | Vidrala, una vez; Viscofan, dos recorridos (el primero, con fuentes parciales, archivado como antecedente) y un relevo de contraste con dos informes añadidos |
| Fases A, B y C (la C en dos turnos con el mismo agente) | Opus, esfuerzo alto (el de la configuración) | Contexto limpio; sin pipeline, LibreOffice ni Excel; notas en el área de trabajo |
| Auditorías (paso 13) | Opus, esfuerzo medio (el de la configuración) | Agentes que no vieron el trabajo; ninguna copió una aprobación |
| Revisión interna | **Fable**, contexto separado | Motivo: la comprobación de mayor consecuencia (lo que se dice de la aptitud para decisiones con dinero real), hecha por un modelo distinto del que hizo el trabajo. Resultado: 0 bloqueantes, 5 importantes, 4 menores y 5 observaciones (informe integrado, §8). Segunda revisión, de lo afectado por las correcciones (motivo: comprobar con un modelo distinto que resuelven los hallazgos sin abrir fallos nuevos): 0 bloqueantes, 1 importante, 6 menores y 5 observaciones; las correcciones posteriores (RA1–RA12) no las revisó Fable (informe integrado, §8) |

**Alcance de Fable.** Solo la revisión interna y la nueva revisión de lo afectado por las correcciones. No ejecutó ninguna parte del procedimiento. Se avisó a la persona responsable antes de cada uso.

**Ejecución en secuencia.** Ningún agente ejecutó el pipeline ni LibreOffice. Los recálculos, las baterías y los controles los ejecutó la orquestación, nunca dos a la vez. Las esperas se resolvieron con avisos de fin de tarea.

## 4. Revisión interna y respuesta

La tabla de respuesta a cada hallazgo (R1–R14) está en el §8 del informe integrado, y los fallos corregidos, en su §3. En breve:
- **Corregidos en el código, con prueba:** R1 (fila 13 de la Historia en la instantánea y en la cadena), R3 (cobertura del ámbito por subparámetro de P-M1) y R4 (fechas y valores incoherentes en los textos de evidencia). R11, en la redacción del informe.
- **Corregidos en los documentos:** R2, R5 (la frase del §2.2 y la lista de la revisión económica), R6, R9, R13 y R14. R7 y R8, con lecturas nuevas (`resultados/dominios_variantes_4_12.md` y `viscofan/resultados/sensibilidad_derechos_de_uso.md`).
- **No corregido en el código y declarado:** R5. Contrastar los dos juicios del agente exigiría un umbral que el encargo no permite adoptar. Queda como límite L15 y como decisión D412-FUNDAMENTO de la propuesta.
- **Sin cambio:** R10 (se resuelve en la verificación final) y R12 (restos sin efecto).
- **Segunda revisión (RA1–RA12):** RA1 (el control de la entrega comparaba instantáneas de relaciones distintas) corregido en el script; RA2–RA7 corregidos o declarados en los documentos; RA8–RA10, límite L16; RA11 y RA12, reconocidos o corregidos. Tabla en el §8 del informe integrado.
- **Defecto nuevo al repetir los expedientes:** los valores de los avisos de dominio iban al informe en JSON y hacían fallar la verificación de citas en una repetición desde el paso 12. Corregido, con prueba; los tres expedientes se repitieron desde el paso 11 y tuvieron auditorías nuevas.

## 5. Porcentaje orientativo hacia la primera versión integrada supervisada

**Interpretación, no medición.** El encargo partía de ≈68 %. Esta entrega lo lleva a **≈75 %**.

**Qué suma** (unos 7 puntos):
- la fiabilidad del recorrido supervisado (unos 3 puntos): vigencia antes del rechazo, materialidad separada, protocolos, variantes atadas a las entradas, dominios, trazabilidad y aptitud de uso en las salidas;
- el cierre de Vidrala con el código final y los dos protocolos sobre el mismo material (unos 2 puntos);
- la segunda empresa recorrida de punta a punta con agentes reales, fuentes recuperadas y configuración propia (unos 2 puntos).

**Qué no suma todavía:**
- **Adopción humana:** ninguna decisión está tomada (D412-USO, D412-PROTOCOLO, configuraciones).
- **Revisión externa** de la 4.12.
- **Validación económica:** P-M1 sigue sin observarse y no hay ensayo en el tiempo.
- **Motor A:** cinco de las seis empresas originales lo usan, y la capa experimental no lo cubre.

## 6. Entrega

- **ZIP:** `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip`, producido con `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/scripts/empaquetar_zip.py`, con partes de hasta 20 MiB y su `.PARTES.txt`, y comprobado con dos lectores (Python `zipfile` y `unzip`).
- **Huella, tamaño y verificación de la descompresión:** en el registro externo `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.VERIFICACION.txt`, que va fuera del ZIP porque un ZIP no puede contener su propia huella.
- **Verificación antes de empaquetar:** ronda definitiva sobre una copia limpia del árbol final (`REGISTRO_PRUEBAS_4_12.md`, último apartado, y §7 del informe integrado).
- **Controles de las entregas anteriores:** salidas de referencia en `resultados/controles_historicos_en_arbol_4_12/`, explicadas en `resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`.
- **Fuentes:** los doce PDF de Viscofan van dentro del paquete (`viscofan/fuentes/pdf/`). El PDF del Bundesbank no está (§1).
