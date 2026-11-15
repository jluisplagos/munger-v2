# Encargo de la revisión interna · entrega 4.11 (integración económica experimental del motor B)

**Para quién.** Para el agente revisor. Trabaja en un contexto separado y no ha participado en el trabajo. Es una revisión **interna** de Claude: no es la revisión externa (ChatGPT), y el informe tiene que identificarse así.

**Objeto.** El material final de la 4.11 en `/home/claude/trabajo/munger_v2_r1`. El encargo §10 pide comprobar fórmulas, concatenación del flujo, fuentes y límites económicos. Se buscan errores reales y lagunas no declaradas, no estilo.

## Qué se revisa

### 1. Fórmulas

Fuentes:
- la plantilla `v6/v64_experimental/entregables/Plantilla_V6.4_experimental.xlsx`;
- su constructor `v6/v64_experimental/scripts/construir_v64_experimental.py`;
- la documentación `v6/v64_experimental/docs/README_V6.4_experimental.md`.

Se comparan con las definiciones de:
- `…_4_11/replica/ESPECIFICACION_REPLICA_INDEPENDIENTE.md`;
- el encargo 4.11 (resumido en el README §5);
- los análisis fuente, `…_4_7_1` (`analisis_n1_n3.py`) y `…_4_8_1` (`analisis_reinversion_4_8_1.py`).

Puntos de atención:

**Columnas del Motor.** BU:DY y las fórmulas envueltas AU:BD, BF, BL, BP, BQ, BS y BT, en las 124 filas.
- La heredada tiene que estar literal en la rama heredada.
- Signos y periodos en los años 1–10 y en el terminal.

**Piezas del modelo:**
- R1 con el máximo conservado;
- factores f y f_fija;
- crédito de H;
- P0;
- convenciones de años y terminal;
- ROIC del terminal;
- valor sin crecimiento;
- Diagnóstico C10, C11, C15 y B176:D177.

**Hoja «Configuración V6.4».**
- Vacío, cero y error tratados de forma distinta.
- Las 28 comprobaciones, su orden y sus motivos.
- Parámetros efectivos que solo actúan en modo experimental válido.
- Trazabilidad.

**Hoja «Conciliación B».** La identidad y la comprobación de la fila.

**Material de contraste.** Los libros recalculados de los casos están en `personaje_v2/pruebas/_v64/casos/rc/` (117) y la réplica en `…_4_11/replica/` (`INFORME_REPLICA.md`). Los libros se leen con openpyxl; con `data_only=True` se leen valores.

### 2. Concatenación del flujo

Selección de la plantilla: `personaje_v2/scripts/seleccion_plantilla.py`, `config_v2_v64_experimental.json` y el código 2.

Recorrido en `pipeline.py`:
1. paso 2 (aplicación de `configuracion_economica.json`);
2. recálculo;
3. lectura (`leer_v63.py`, `leer_resultados.py`);
4. precio de Sí;
5. paso 10 (`variantes_configuracion_v64.py` y entradas de la fase C);
6. coherencia de la fase C (`coherencia_v64`);
7. material auditado (`cierre_v2.MATERIAL_FIJO`);
8. paso 12;
9. auditoría;
10. cierre;
11. vigencia: retirada y reaplicación si la configuración cambia.

Salidas: la ficha, el informe (§14 y distancias con denominador) y el resumen tienen que reflejar el modelo activo. El DCF inverso, el tornado y la comprobación conjunta no pueden mezclar el modelo heredado con el experimental.

Cambio de base: `personaje_v2/scripts/cambiar_base.py` y las configuraciones de `…_4_11/configuracion/`. El original no se toca. Las fuentes nuevas no pueden convivir con derivaciones antiguas, y las fechas tienen que ir separadas.

### 3. Fuentes

Entradas del piloto (`…_4_11/configuracion/cambio_de_base_piloto.json` → `piloto/Vidrala/`):
- N1 (T1) y N2 (M1): `…_4_7_1/financiero/matriz.json`;
- N3: balance de 2025, en `texto/CF_2025.txt`;
- cartera P0: nota de intangibles, `…_4_8/scripts/analisis_pm1.py` y `texto/ES_2025…txt`;
- precio, acciones y E: ES 2025;
- rf: Bundesbank, cuyo PDF no se conserva (límite declarado).

Comprobaciones:
- Cada valor y su fuente coinciden.
- La evidencia activa del Control maestro del libro de datos y del evaluado es coherente con esas fuentes.
- No quedan restos de la base anterior.

### 4. Límites económicos

Para cada límite, se mira si está declarado donde corresponde: README §8, informe del piloto, propuesta humana e informe de integración. Los conocidos:
- el terminal con R1 no aplica el máximo conservado;
- el crédito terminal de H;
- λ y θ son hipótesis, no mediciones;
- dominios de f y f_fija;
- P-M1 no resuelta;
- la configuración de demostración no está adoptada;
- P3 (C48/C49) y C46/C47;
- k = 3 experimental;
- el ensayo no es un backtest.

También se buscan límites no declarados.

**Piloto.** Se revisa además el expediente `…_4_11/piloto/Vidrala/`:
- fases A, B y C, con la evaluación `configuracion_v64` de la fase C;
- auditoría;
- ficha e informe.

La fase C tiene que evaluar el mantenimiento y su estructura. «No cambia la zona» solo puede afirmarse de las variantes calculadas.

## Reglas

1. Solo lectura. El único archivo que se escribe es `…_4_11/revision_interna/REVISION_INTERNA_4_11.md`. Los temporales van al scratchpad de la sesión: `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna/`.
2. Se puede leer y ejecutar Python de solo lectura (openpyxl, scripts de comprobación en temporales).
3. No se ejecutan LibreOffice, `recalc.sh`, `pipeline.py` ni `verificar_paquete.sh`. Si un hallazgo necesita un recálculo, se pide en el informe.
4. No se cambian criterios financieros, probabilidades, rentabilidad exigida, escenarios ni conclusiones. No se rellenan campos humanos ni se confirman ceros.
5. En español, en tercera persona (la persona responsable del proyecto no recibe tratamiento de segunda persona). Se distinguen hechos comprobados, interpretaciones y propuestas, y se explica la jerga necesaria.

## Informe (`REVISION_INTERNA_4_11.md`)

- **Cabecera.** «Revisión interna (Claude, contexto separado; no es la revisión externa)», fecha y huellas SHA-256 de lo revisado: plantilla, referencia, constructor, `pipeline.py`, configuración del piloto y estado del piloto.
- **Qué se revisó y qué no.**
- **Hallazgos numerados.** Cada uno lleva:
  - gravedad: **bloqueante**, **importante**, **menor** u **observación**;
  - evidencia exacta: archivo y línea, o celda;
  - por qué importa;
  - corrección propuesta.
- **Veredicto.** «sin bloqueantes» o «con bloqueantes», y si el material puede entregarse como implementación experimental no adoptada.
