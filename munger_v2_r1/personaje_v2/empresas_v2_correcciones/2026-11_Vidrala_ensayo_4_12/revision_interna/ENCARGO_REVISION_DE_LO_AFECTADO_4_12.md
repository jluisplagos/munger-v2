# Encargo · revisión de lo afectado por las correcciones · entrega 4.12

**Qué es.** El encargo de una segunda revisión interna, limitada a lo que cambió después de la primera (`REVISION_INTERNA_4_12.md`, 12-nov, 23:10–23:30). La primera revisión cubre la versión que vio. **No cubre el material nuevo**, y esta revisión no la sustituye: revisa solo lo afectado.

**Quién la hace.** Un agente con Fable, en un contexto separado, que no hizo el trabajo ni las correcciones. Motivo: comprobar con un modelo distinto que las correcciones resuelven los hallazgos sin abrir fallos nuevos, antes de dar la entrega por cerrada.

## 1. Qué cambió desde la primera revisión

Las diferencias exactas están en `diferencias_desde_la_revision/` (antes = el árbol que vio la primera revisión; después = el árbol actual):
- `codigo_scripts.diff`: `entradas_economicas.py`, `trazabilidad_v64.py`, `objetivo_v64.py`, `pipeline.py`, `variantes_configuracion_v64.py` e `informe.py`;
- `pruebas.diff` y `verificar_paquete.diff`: pruebas nuevas de los grupos F y G y mínimo de la batería (127);
- `scripts_del_ensayo.diff`: scripts del ensayo 4.12 (lecturas de R7 y R8, control de la entrega);
- `documentos_del_ensayo.diff` y `documentos_generales.diff`: informe integrado, revisión económica de Vidrala, contraste de Viscofan, registro de pruebas, Anexo D, guía y README de la V6.4.

La respuesta de la orquestación a cada hallazgo está en el §8 del informe integrado, y los fallos corregidos, en su §3. Al repetir los expedientes apareció un defecto más que la primera revisión no vio (valores de los avisos de dominio escritos en JSON en el informe, que hacían fallar la verificación de citas al repetir desde el paso 12). Está en el §3.

Los tres expedientes se repitieron desde el paso 11 con el código corregido, tuvieron auditorías nuevas (Opus, contexto limpio) y se cerraron: `cierre_condicionado/Vidrala`, `cierre_bloqueo/Vidrala` y `viscofan/experimental/Viscofan`. Los cierres anteriores están en `historial_cierres/` de cada uno.

## 2. Qué hay que comprobar

1. **Correcciones del código.** Para R1, R3, R4, R11 y el defecto de las comillas: ¿resuelven el hallazgo? ¿Son completas (otros sitios con el mismo problema)? ¿Introducen fallos nuevos, falsos avisos o cambios de comportamiento no declarados (en la V6.3, en el modo heredado de la V6.4 o en el piloto 4.11)?
2. **Pruebas nuevas.** ¿Prueban de verdad lo corregido? ¿Fallarían con el código anterior?
3. **Expedientes cerrados.** ¿El material y las salidas nuevas reflejan las correcciones (fila 13 en la instantánea y en la cadena, avisos de Viscofan, «PM1.familia» en Vidrala, línea de estado, aptitud de uso)? ¿Las cifras de valoración, los estados y los veredictos son los mismos que antes y, si no, está explicado? ¿Cada auditoría responde a su solicitud y a su material?
4. **Documentos.** ¿Lo que dicen coincide con los expedientes y con el código? En particular: R2, R5 (frase del §2.2, lista de la revisión económica, límite L15 y decisión D412-FUNDAMENTO de la propuesta), R6, R8 (método de θ equivalente de `scripts/sensibilidad_derechos_de_uso_viscofan.py` y su conclusión), R9, R13 y R14.
5. **Lo no corregido.** ¿Está bien declarado lo que se dejó sin corregir (R5 en el código, R7 en el pipeline, R12, las dos líneas heredadas del fundamento material)?

## 3. Reglas

- Escribe SOLO `revision_interna/REVISION_DE_LO_AFECTADO_4_12.md` en la carpeta del ensayo 4.12. No modifiques, muevas ni borres nada más del árbol. Notas y scripts auxiliares en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/agentes_4_12/revision_afectado/` (créala).
- Nada de internet. No ejecutes el pipeline, LibreOffice ni las baterías completas (las ejecuta la orquestación, en secuencia). Puedes leer libros con openpyxl en solo lectura y ejecutar scripts de comprobación de solo lectura y funciones sueltas del código sobre copias en tu carpeta auxiliar.
- No valoras las empresas: compruebas que el sistema hace lo que dice y que los documentos dicen lo que hay.
- Separa hechos comprobados, interpretaciones y propuestas. Español claro; sin tratamientos de segunda persona hacia la persona responsable del proyecto.

## 4. Formato del resultado

- **Veredicto en breve** (unas líneas).
- **Hallazgos**, cada uno con: clase (bloqueante, importante, menor u observación), evidencia (archivo y línea), consecuencia y qué haría falta. Numerados RA1, RA2…
- **Estado de cada hallazgo de la primera revisión** (R1–R14): resuelto, resuelto en parte o no resuelto, con una frase.
- **Lo que se comprobó sin encontrar problemas.**
- **Límites de esta revisión.**
- **Huellas SHA-256** de los archivos principales revisados.
