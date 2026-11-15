# Encargo de la revisión interna · entrega 4.13 (fiabilidad del motor B y conciliación económica de los dos casos)

**Para quién.** Para el agente revisor, que trabaja en un contexto separado y no ha participado en el trabajo. Es una revisión **interna** de Claude: no es la revisión externa ni la sustituye, y su informe tiene que decirlo.

**Objeto.** El código y el material finales de la 4.13, en `/home/claude/trabajo_4_13/munger_v2_r1`.

Se buscan errores reales, lagunas no declaradas y afirmaciones que el material no sostiene; no se revisa el estilo. Cada hallazgo lleva:
- **gravedad:** bloqueante, importante, menor u observación;
- **evidencia:** archivo, línea o celda, y la orden que lo reproduce, si la hay;
- **consecuencia:** qué cifra, estado o afirmación afecta;
- **qué haría falta.**

**Qué no hace el revisor.**
- No modifica nada del árbol. Su única escritura es su informe, `revision_interna/REVISION_INTERNA_4_13.md`.
- Sus temporales van en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna_4_13/`.
- No ejecuta el pipeline sobre los expedientes reales ni lanza LibreOffice.
- Puede leer libros con openpyxl (`data_only=True` para valores) y ejecutar scripts de solo lectura sobre copias en sus temporales, con `python3 -B` para no dejar cachés en el árbol.
- No busca en internet.

**Rutas.** Son relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/` salvo que se diga otra cosa. El encargo de la persona responsable está en `ENCARGO_4_13.md`, en esta misma carpeta, y el avance, en `REGISTRO_AVANCE_4_13.md`.

## Puntos de atención (encargo 4.13 §3–§8)

### 1. JSON estructuralmente incorrecto y vigencia (§3)
Código: `personaje_v2/scripts/estructura_json.py`, `configuracion_economica.validar`, `seleccion_plantilla.py`, `cierre_v2.motivo_vigencia`, y `pipeline.py`, `ficha.py`, `informe.py` y `resumen.py` (barreras `ESTR.protegido`).
- ¿Queda alguna lectura de un archivo de entrada o de control que interprete su contenido (`.get`, índices, iteración) antes de comprobar la vigencia?
- ¿Una alteración de tipo (null, lista, escalar, campo anidado) puede dejar una aprobación vigente en la primera llamada de alguna de las cuatro vías?
- ¿El material intacto con una selección equivocada sigue rechazándose sin tocar nada?
- Pruebas: `personaje_v2/pruebas/test_integracion_v64.py`, grupo E (`TIPOS_413`), y `scripts/sonda_tipos.py`.

### 2. Acción provisional y final (§4)
Código: `objetivo_v64.accion_evaluada`, `tratamiento`, `contradicciones_salida` y `mismo_importe`; `pipeline.coherencia_v64`, `ficha.py`, `informe.py` y `resumen.py`.
- ¿Alguna combinación de acción final, estado, protocolo, objetivo estructurado y `decision.precio_objetivo` contradictoria alcanza un cierre o material listo para auditoría?
- ¿Sigue siendo posible una transición legítima entre la conclusión provisional y la final?
- ¿Se conservan S-19, D10, las compras sin objetivo y los bloqueos con acción nula?
- Pruebas: grupo F (`grupo_f_413`) y `scripts/sonda_salto.py`.

### 3. Cobertura por hipótesis y fundamento (§5)
Código:
- `objetivo_v64.cobertura`, `vinculados_necesarios` y `discrepancias_con_la_configuracion`;
- `pipeline._coherencia_cobertura_413`;
- las variantes nuevas de contraste en `variantes_configuracion_v64.py`;
- `dominios_v64.agrupar` y `grupos_a_evaluar`;
- el formato «4.13» de las variantes.

Preguntas:
- ¿Los vínculos necesarios son los que impone la configuración (SR2 ↔ ROIC × f, N1 ↔ escudo, R0 ↔ sin P-M1), sin ampliarlos para dar cobertura?
- ¿«No determinada» puede convertirse en «no material» en alguna salida?
- ¿Un juicio económico se presenta como constatación calculada?
- ¿Se ha inventado algún umbral de fundamento suficiente?
- ¿Toda hipótesis va a D10 de forma automática?
- ¿Los avisos de dominio de las variantes llegan agrupados a la fase C, a la ficha y al informe, con la conclusión a la que afectan?
- Expedientes: los `fase_c.json` de `vidrala_condicionado/`, `vidrala_bloqueo/` y `viscofan/`.

### 4. Viscofan: acciones y evidencia activa (§6)
Material:
- `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md` y `resultados/alternativas_acciones_viscofan.md`;
- `rellenar_fase1_v63.py` (`FRESCAS` y `evidencias_sustituidas`);
- `viscofan/Viscofan/fase1_v63.json` y `fase1_metadatos.json`;
- el Control maestro del libro de datos;
- `viscofan/resultados/reutilizacion_4_12.md`.

Preguntas:
- ¿Queda alguna evidencia activa que contradiga las entradas: fecha, cifra, concepto, período o unidad?
- ¿N se presenta como dato definitivo o con su concepto real?
- ¿La reutilización de la extracción y de las fases A y B está justificada por lo que leen?
- La auditoría encontró un error en la fase A reutilizada (C97, operaciones de directivos): ¿hay otros del mismo tipo?

### 5. Arrendamientos y plantilla V6.4.1 (§7)
Material:
- `v6/v641_experimental/`: constructor, referencia, inventario, README y SHA-256;
- `resultados/conciliacion_arrendamientos_viscofan.md`, `resultados/compatibilidad_v641.md` y `viscofan/resultados/dominios_perimetro.md`;
- `scripts/replica_independiente_v641.py`;
- la integración: `seleccion_plantilla`, el perímetro en `configuracion_economica`, `entradas_economicas` (huellas), `leer_v63`, `variantes_configuracion_v64` y `comprobacion_conjunta`.

Preguntas:
- ¿El perímetro NIIF 16 es contable y económicamente coherente con el motor B (puente, NOPAT, capital, pagos) y se propaga a D_hist, F_hist, Rh, f/f_fija, S2C, requisito y terminal?
- ¿Hay algún doble cómputo?
- ¿La V6.4 y sus expedientes conservan bytes y huellas?
- ¿Se trasladó alguna cota de la base anterior a la nueva?
- ¿La réplica es independiente de la plantilla?

### 6. Interpretaciones económicas de Vidrala (§8)
Material:
- `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md` y `resultados/crecimiento_terminal_vidrala.md`;
- `…_4_9/PRECISION_ROIC_4_9.md`;
- las justificaciones activas de las configuraciones y de las fases C nuevas.

Preguntas:
- ¿La condición de Q-ROIC1 es la de la 4.9?
- ¿La lectura de r_op frente a la r personal es correcta y no cae en la conclusión contraria?
- ¿El argumento sobre H y la mezcla fijo/circulante usa denominadores coherentes?
- ¿Alguna justificación activa sigue apoyándose en las inferencias corregidas?

### 7. Expedientes finales y documentos
- **Estados y auditorías:** ¿son acordes al material?
  - `vidrala_condicionado/Vidrala`: concluido · APROBADO;
  - `vidrala_bloqueo/Vidrala`: pendiente_de_datos · APROBADO;
  - `viscofan/Viscofan`: estado final en `estado_pipeline.json`.
- **Aprobaciones antiguas:** ¿queda alguna vigente o reutilizada (historial_cierres, auditorías apartadas en antecedentes/)?
- **Comparaciones:** `resultados/comparacion_4_12_4_13.md` y las réplicas, `resultados/replica_independiente.*` en cada carpeta.
- **Ámbito de las pruebas:** ¿lo que dicen los registros coincide con lo ejecutado?

Formato del informe: una tabla de resumen por gravedad y después un apartado por hallazgo (R1, R2…), con la evidencia, la consecuencia y qué haría falta. Al final, una sección «Qué está bien», breve, solo con lo comprobado.
