# Encargo de la revisión interna · entrega 4.12 (validación supervisada, cierre de la integración y contraste con Viscofan)

**Para quién.** Para el agente revisor. Trabaja en un contexto separado y no ha participado en el trabajo. Es una revisión **interna** de Claude: no es la revisión externa ni la sustituye, y el informe tiene que identificarse así.

**Objeto.** El código y el material finales de la 4.12 en `/home/claude/trabajo_4_12/munger_v2_r1`. Se buscan errores reales, lagunas no declaradas y afirmaciones que el material no sostiene, no estilo. Cada hallazgo lleva:
- gravedad: bloqueante, importante, menor u observación;
- evidencia: archivo, línea o celda, y la orden que lo reproduce si la hay;
- consecuencia: qué cifra, estado o afirmación afecta.

**Qué no hace el revisor.** No modifica nada del árbol salvo su informe, `revision_interna/REVISION_INTERNA_4_12.md`. Sus temporales van en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna_4_12/`. No ejecuta el pipeline sobre los expedientes reales ni lanza LibreOffice. Puede leer libros con openpyxl (`data_only=True` para valores) y ejecutar los scripts de solo lectura sobre copias en sus temporales. No busca en internet.

Rutas relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/` salvo que se diga otra cosa. El encargo del usuario está resumido en `INFORME_INTEGRACION_4_12.md` y en `REGISTRO_AVANCE_4_12.md`.

## Puntos de atención (encargo 4.12 §9)

### 1. Vigencia de las aprobaciones
- `personaje_v2/scripts/pipeline.py` (vigencia antes del rechazo; paso 13 con `libros_verificados`; reaplicación por cambio de protocolo, con el motivo ya en el turno 1 de la fase C), `cierre_v2.py`, `seleccion_plantilla.py`, `ficha.py`, `informe.py` y `resumen.py`.
- Los dos expedientes de Vidrala se cerraron, se corrigió después el código que escribe la ficha y el informe y se regeneraron con `--desde 13`, con auditorías nuevas (`REGISTRO_AVANCE_4_12.md`, §7). ¿Queda alguna aprobación anterior vigente o reutilizada? ¿Las salidas oficiales corresponden al material auditado?
- ¿Una aprobación puede quedar vigente con material cambiado en alguna primera llamada, incluidas las llamadas a mano sin `MUNGER_CONFIG`?
- ¿La copia `cierre_bloqueo/Vidrala` arrastra como vigente algo del original? Mirar `historial_cierres/`, `auditoria.md`, la solicitud y el registro de publicaciones reubicado.

### 2. Trazabilidad de los resultados
- `trazabilidad_v64.py` y `cadena_trazabilidad.md` de los expedientes:
  - `cierre_condicionado/Vidrala`;
  - `cierre_bloqueo/Vidrala`;
  - `viscofan/experimental/Viscofan`.
- `entradas_economicas.py`: ¿la instantánea cubre todas las entradas que mueven el valor?
- ¿Cada cifra de la conclusión se puede seguir hasta su fuente, con la clase correcta (dato, cálculo, convención, hipótesis)?
- ¿Los avisos de ceros pendientes, vacíos, signos, unidades, stock/flujo y fechas son correctos?

### 3. Materialidad para la acción y para el objetivo
- `objetivo_v64.py`, `pipeline.coherencia_v64`, `comprobacion_conjunta.py`, `configuracion_economica.alternativas` y `numericos_activos`.
- Los `fase_c.json` de los tres expedientes y sus fichas.
- ¿El tratamiento del objetivo sale de las reglas y no del agente?
- ¿El ámbito es exactamente el de las variantes calculadas?
- ¿Algún parámetro material sin fundamento queda fuera de los condicionantes?
- ¿Una compra podría aprobarse dejando una hipótesis experimental fuera de las listas heredadas?
- ¿Un rango se presenta como intervalo de confianza?

### 4. Coherencia económica de la inversión y del terminal
- `REVISION_ECONOMICA_VIDRALA_4_12.md` y `cierre_condicionado/resultados/datos_revision_economica.md`.
- `viscofan/configuracion/analisis_configuracion_viscofan.md` y el README de la V6.4 (§5, §8 y §9).
- Reposición frente a crecimiento y dobles cómputos (SR1 frente a S, SR2 y H).
- Coherencia del S2C de los años con el ROIC del terminal.
- Convención terminal, R1 y capacidad conservada en el MALO.
- Dominios: f, f_fija, inversión fija negativa con circulante alto.
- La amortización de derechos de uso dentro de la D&A.
- ¿Las conclusiones de la revisión económica se siguen de las cifras?

### 5. Transferencia a Viscofan
- `viscofan/fuentes/` (inventario, huellas, ediciones, contraste de la Historia), `viscofan/configuracion/` y `viscofan/experimental/`.
- ¿Algo se trasladó de Vidrala (tipo, margen, cartera, λ, proporción de mantenimiento)?
- ¿N1 y N2 tienen análisis de perímetro y período?
- ¿El circulante, las bases de reinversión y las adquisiciones tienen fuente y conciliación propias?
- ¿θ tiene una central disfrazada?
- ¿Las combinaciones no definidas se declaran?
- ¿Las fechas van separadas?
- ¿La fase A eligió el motor por los hechos? En particular, la sección 0 de `datos_v63.md` antes de la fase A.
- ¿Se llama «original recuperado» a alguna edición distinta?

### 6. Correspondencia entre lo verificado y lo que afirman la ficha, el informe y el resumen
- `ficha.json → aptitud_de_uso`, el bloque de la sección 1 del informe y la columna del resumen V6.4 (encargo §9: la aptitud se refleja de forma diferenciada en las salidas nuevas, sin cambiar el contrato de 16 puntos ni los veredictos históricos). ¿Está separada de la auditoría? ¿Dice «experimental» sin atribuir aptitud? ¿Las salidas V6.3 y V6.4 heredadas no cambian?
- Por expediente: `ficha.json`, `informe.md`, la fila del resumen V6.4 (`resumen_v2_v64_experimental.csv` junto a cada expediente), `precio.json`, `configuracion_v64_variantes.json`, `auditoria.md` y `material_auditoria.json`.
- ¿Cada afirmación de las salidas está respaldada por lo verificado (valores, variantes, zona, objetivo, estado, distancias con denominador)?
- ¿«Valor calculado condicional» y «precio objetivo emitido» están separados en las tres salidas?

### 7. Documentos de la entrega
- `INFORME_INTEGRACION_4_12.md`, sobre todo la evaluación de aptitud de uso y la tabla de limitaciones.
- `COMPARACION_PROTOCOLOS_4_12.md` y `viscofan/CONTRASTE_VISCOFAN_4_12.md` (qué se reutiliza, qué es propio de la empresa y qué impide generalizar).
- La propuesta humana (`propuestas/`).
- `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` y el Anexo D §D.13.
- ¿Afirman algo que no se ha ejecutado? ¿Atribuyen aptitud general por dos empresas?

## Formato del informe

`revision_interna/REVISION_INTERNA_4_12.md`, en español claro y en tercera persona, con:
- quién revisa, la fecha y la hora;
- las huellas SHA-256 de los archivos principales revisados;
- el veredicto en breve (número de hallazgos por gravedad);
- los hallazgos numerados (R1, R2…);
- lo que se comprobó sin encontrar problemas;
- los límites de la propia revisión: qué no se pudo examinar y por qué.
