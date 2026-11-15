# Encargo de la segunda revisión interna · entrega 4.13 (lo afectado por las correcciones)

**Para quién.** Para el agente revisor, que trabaja en un contexto separado y no ha participado en el trabajo. Es una revisión **interna** de Claude: no es la revisión externa ni la sustituye, y su informe tiene que decirlo. El encargo 4.13 pide que, si una corrección posterior cambia el material revisado, se revise de nuevo lo afectado. Esta es esa revisión.

**Antecedente.** La primera revisión interna (`revision_interna/REVISION_INTERNA_4_13.md`, hallazgos R1–R18) y su encargo (`revision_interna/ENCARGO_REVISION_INTERNA_4_13.md`) están en esta carpeta. El registro de lo hecho después está en `REGISTRO_AVANCE_4_13.md`, desde «Revisión interna recibida». Los relevos a los agentes, en `resultados/relevos_agentes_4_13.md` (entradas 13 a 26).

**Objeto.** Lo que cambió después de la primera revisión, en `/home/claude/trabajo_4_13/munger_v2_r1`. Se buscan errores reales, lagunas no declaradas, afirmaciones que el material no sostiene y regresiones. No se revisa el estilo. Cada hallazgo lleva:
- **gravedad:** bloqueante, importante, menor u observación;
- **evidencia:** archivo, línea o celda, y la orden que lo reproduce, si la hay;
- **consecuencia:** qué cifra, estado o afirmación afecta;
- **qué haría falta.**

**Qué no hace el revisor.**
- No modifica nada del árbol. Su única escritura es su informe, `revision_interna/REVISION_INTERNA_4_13_SEGUNDA.md`.
- Sus temporales van en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna_4_13_segunda/`. Cuidado con el disco: no copie expedientes enteros con sus libros; copie solo lo que necesite.
- No ejecuta el pipeline sobre los expedientes reales ni lanza LibreOffice.
- Puede leer libros con openpyxl (`data_only=True` para valores) y ejecutar scripts de solo lectura sobre copias en sus temporales, con `python3 -B` para no dejar cachés en el árbol.
- No busca en internet.

**Rutas.** Relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/` salvo que se diga otra cosa. El encargo de la persona responsable está en `ENCARGO_4_13.md`.

## Puntos de atención

### 1. Correcciones de código de R1–R18
Código en `personaje_v2/scripts/`: `ficha.py` (R1, R8), `cierre_v2.py` (R2), `objetivo_v64.py` (R3, R4), `pipeline.py` (`_coherencia_cobertura_413`, R4), `referencias_mecanicas.py` (R6), `configuracion_economica.py` (R12), `dominios_v64.py` (R17), `rellenar_fase1_v63.py` (R7: `FRESCAS`, `control_maestro_textos`, período de D4); prompts y esquemas de la fase C y de la verificación; `scripts/conciliacion_arrendamientos_viscofan.py` (R11).
- ¿Cada corrección resuelve el hallazgo sin abrir otro? ¿Alguna afirmación del registro sobre esas correcciones es más fuerte que lo que hace el código?
- Pruebas: `personaje_v2/pruebas/test_integracion_v64.py`, `grupo_e_revision_413`, `grupo_f_revision_413` y las tres nuevas del grupo H (R6, R12, R17). ¿Prueban lo que dicen?

### 2. Correcciones del informe tras las auditorías
`personaje_v2/scripts/informe.py`, sección 7 (parámetros sin fundamento aparte de la lista D10) y sección 14 (grupos de avisos que solo son lecturas; evidencia de los juicios sobre el objetivo).
- ¿Son correctas y completas? ¿Quedan otros puntos del informe o de la ficha que digan «ninguna», «0» o «no material» donde el material dice «no determinada» o «lectura en la activa»?
- Avisos de las auditorías declarados y no corregidos (en `REGISTRO_AVANCE_4_13.md`): por ejemplo, el corte a media frase de `causa_si_no_concluido.detalle` y de diagnostico.md. ¿Alguno debía corregirse antes de cerrar?

### 3. Viscofan regenerado
- `scripts/corregir_viscofan_revision_4_13.py` → `viscofan/resultados/correccion_revision_4_13.md`: R5 (naturaleza), R7 (C42 = 9,47, D88/E88, D4) y la retirada de la marca de consumo de la extracción para reutilizarla. ¿Es correcta la aritmética de C42? ¿Está justificada la reutilización de la extracción? ¿La retirada de la marca de consumo es una manipulación del estado que oculte algo, o está registrada y es legítima?
- Fases A, B y C nuevas, auditoría APROBADO (`viscofan/Viscofan/`). ¿Quedan evidencias activas que contradigan las entradas (Control maestro del libro de datos, fase1_v63.json, fase1_metadatos.json)? ¿Las celdas declaradas como «evidencia heredada no actualizada» en D88 son las que de verdad conservan datos de 2026?
- `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md` (antecedente de la etapa 1), `resultados/alternativas_acciones_viscofan.md` (libro vigente; R10) y `resultados/comparacion_4_12_4_13.md` (descomposición del cambio en fases A y B nuevas y perímetro). ¿Las cifras y la descomposición son correctas?

### 4. Vidrala regenerado
`vidrala_condicionado/` y `vidrala_bloqueo/`: fases C nuevas (contrato R4), variantes recalculadas (R17) y las auditorías. Dos aprobaciones de material anterior se guardaron en `antecedentes/auditoria_material_<id>/` y no se usaron para cerrar.
- ¿Los estados y las auditorías finales son acordes al material vigente? ¿Queda alguna aprobación antigua vigente o reutilizada?
- Los dos agentes trazan la materialidad para el objetivo de forma distinta con el mismo material (N1). ¿Lo representa bien el sistema (juicio declarado, sin umbral) y lo recoge la propuesta?

### 5. Propuesta, guía y control de la entrega
- `scripts/propuesta_humana_4_13.py` → `propuestas/PROPUESTA_HUMANA_4_13.md` y `.json`. ¿Tres grupos (política de salida, elecciones por empresa, ampliaciones), con recomendación, alternativas, evidencia y efectos, y firmas vacías? ¿Las cifras de efecto son las de las salidas? ¿Alguna recomendación adopta algo, inventa un umbral o elige una cifra por su valor?
- `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md`. ¿Lo que dice coincide con el código?
- `scripts/comprobar_entrega_4_13.py` (todavía sin ejecutar: espera la ronda final y las sondas). ¿Comprueba lo que dice? ¿Hay comprobaciones que pasarían aunque el hecho fuera falso?

Formato del informe: una tabla de resumen por gravedad y después un apartado por hallazgo (S1, S2…), con la evidencia, la consecuencia y qué haría falta. Al final, una sección «Qué está bien», breve, solo con lo comprobado.
