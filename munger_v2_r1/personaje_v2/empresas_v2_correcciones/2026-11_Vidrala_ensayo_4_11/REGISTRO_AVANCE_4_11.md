# Registro de avance · encargo 4.11 (cuaderno de trabajo)

Cuaderno de trabajo para retomar la tarea si se compacta el contexto. Manda lo que dicen los archivos. Se conserva en la entrega como registro del proceso.

## 0. Base y copias (12-nov-2026)
- ZIP 4.10.1: SHA-256 `3a6b80d1…afe018`, 130.579.220 bytes; CRC correcto con `unzip -t` y con Python `testzip`; 2.477 entradas.
- Extracción intacta (solo lectura): `/home/claude/base_intacta/munger_v2_r1`.
- Copia de trabajo: `/home/claude/trabajo/munger_v2_r1` (manifiesto 2.193, sin diferencias al empezar).
- Primera verificación completa y controles históricos: en `/home/claude/verif/` (PASA; 16 controles idénticos a la referencia).

## 1. Hallazgos de la lectura
- **Motor (V6.3):** 124 filas de valoración (6–9 escenarios y estudio; 12–40 sensibilidades; 41–55 tornado; 56–136 DCF inverso), todas con la misma fórmula de flujo:
  `AU = AA·(AK·(1−K) − L) − (AA − C)/G` (motor B: L = 0) y terminal `BF = AJ·(1+H)·(F·(1−K)·(1−H/I) − L)`.
- **R0 = regla de la plantilla:** reinversión ΔV/S2C simétrica (libera capital fijo con ventas que caen).
- **t:** `Diagnóstico V6!C11 = Historia!C52` (media 5 años); el mismo τ en NOPAT y en r_op (`C15`, escudo `Historia!C63·(1−N(C11))`).
- **m0:** `Diagnóstico V6!C10` según Palancas C8 (C48 o C49).
- **Validez:** `Motor!BS` (validez de fila) y `BT` (motivo); la regla V35 convierte un motor no calculable en INCOMPLETO con el motivo de BT7 → BLOQUEO DEL VALOR.
- **Réplicas fuente:** 4.7.1 `analisis_n1_n3.py` (`r_op`, `proyeccion`, `valor`, `escalera`); 4.8.1 `analisis_reinversion_4_8_1.py` (`req_lambda`, `req_nivel`, `valorar`, `f_desc`, `kw_estructura`), sobre el libro 4.6.1.
- **R1 (4.7.1):** Δcirc = ΔV·NWC en todos los casos; fija = max(0, V_t − pico_t)·(1/S2C − NWC) con pico_t = max(V0..V_{t−1}); NWC = (existencias + deudores − acreedores)/ventas 2025 del balance (no está en la Historia).
- **P-M1 (4.8.1):** FCF = NOPAT + cl − fija·f_fija − Δcirc − (req − crédito); crédito = min(req, max(0, fija)) solo en H; terminal: fija11 = (n11·g/(ROIC·f_roic) − ΔV11·NWC)·f_fija, Δcirc11 = V10·g·NWC.
  D_hist = ΣHistoria!H31:L31 + Σcartera (530,01 con P0); F_hist = Σ(capex − (D&A − cartera)) + Σadquisiciones (251,21); f = D/(D − Rh); f_fija = 1 − Rh/F.
  Λ: req = (λ−1)(D&A0 − cl_t) [plana] o (λ−1)(D&A0·V_t/V0 − cl_t) [∝ ventas]; terminal (λ−1)·D&A0·V11/V0; Rh = (λ−1)·Σ(D&A − cartera).
  Θ: nivel = θ·exceso medio 2021–2025 (47,76); terminal nivel·V11/V0; Rh = θ·Σexceso (238,79).
  P0: cl_k = min(CLa, max(0, VNC − CLa·k)), k = 0..9; cartera histórica {2024: 4,921; 2025: 4,492}.
- **Pipeline:** la plantilla, la referencia, el verificador y `scripts_v63` (de donde se importa `inventario_entradas`) salen de `--config`. Las escrituras usan `v63_xml.LibroV63` (XML, conserva controles). `cierre_v2.MATERIAL_FIJO` es la lista de archivos del material auditado.
- **Construcción V6.3:** openpyxl + restauración de gráficos canónicos (`patch_v62_base.restaurar_partes`) + `add_sliders.py` al final + `normalizar_paquete`.

## 2. Diseño (decisiones técnicas rutinarias)
- Carpeta nueva `v6/v64_experimental/` (entregables, referencia, scripts, docs). V6.3 y su referencia, intactas.
- Plantilla V6.4 = V6.3 + hoja «Configuración V6.4» (entradas, parámetros efectivos, validez y trazabilidad) + hoja «Conciliación B» (MALO/NORMAL/BUENO, años 1–10 y terminal) + columnas nuevas en Motor (BU en adelante) para cada una de las 124 filas de valoración; las fórmulas de flujo pasan a `IF(experimental, nueva, heredada)`, con la heredada literal.
- Modo heredado: todas las opciones nuevas se ignoran (aunque estén escritas) → mismas fórmulas efectivas.
- Modo experimental: solo motor B (otro motor → configuración no aplicable, motivo en BT, V35 bloquea el valor). N1 y N2 vacíos = mecanismo histórico (declarado); N3 y P-M1 exigen elección explícita; incompleto → no calcula.
- Vacío/cero/error: ISBLANK/ISNUMBER, nunca N() ni condiciones de verdad para decidir entre valor y respaldo.
- R0 + P-M1: rechazado con explicación (sin especificar).
- Dominios: λ ≥ 1; 0 ≤ θ ≤ 1; D_hist > 0; D_hist − Rh > 0; F_hist > 0; 0 ≤ f_fija; VNC ≤ 10·CLa con P0. Fuera de dominio → no calcula (sin recortes).
- ROIC terminal: entrada explícita y coherente con la estructura (SR2 → × f; las demás → sin cambio).
- Material auditado: se añaden `configuracion_economica.json` y `plantilla_activa.json` a `MATERIAL_FIJO` (solo existen en expedientes V6.4).

## 3. Estado
- [x] Lectura y diseño (tarea 1).
- [x] Plantilla V6.4 construida (`v6/v64_experimental/scripts/construir_v64_experimental.py`; SHA-256 `e21ded39…c272`; referencia `referencia_V6.4_experimental.json`: 18.808 fórmulas, 5.542 fijas, 62 validaciones, 13 partes = las de la V6.3).
  - Cambios frente a la V6.3 (comprobado comparando referencias): 1.994 fórmulas cambiadas = 16 columnas × 124 filas de Motor (AU:BD, BF, BL, BP, BQ, BS, BT) + Diagnóstico B176:D177, C10, C11, C15 + Panel A1; 7.844 nuevas (Motor BU:DY, Configuración, Conciliación, Panel C18); ninguna quitada; gráficos, controles, validaciones, formatos condicionales y nombres de la V6.3 idénticos.
  - Herramientas: `trasladar_entradas.py` (copia las entradas de un libro V6.3 a la V6.4 con LibroV63) y `comparar_libros.py` (valores celda a celda, A:BT de las 11 hojas V6.3).
- Resultados de las primeras pruebas (scratchpad `v64/`):
  - Heredado: libro 4.10.1 → V6.4: 120.168 celdas, 0 diferencias (1e-12); conciliación «cuadra» en los tres escenarios.
  - Experimental sobre el libro 4.6.1: T1·M1·R1 → ponderado 69,24467310975967 y Sí 64,26217677232681 (diferencias ≈ 3e-14); H/S/SR1/SR2/SRF con λ = 1,15 y P0 → 68,9162591 / 61,6285291 / 62,4652723 / 63,6572086 / 65,3842332 (≈ 1e-14).
  - Rechazos: sin N3, λ vacío, λ < 1, θ > 1, R0 + P-M1, modo mal escrito, ROIC incoherente, N1 sin escudo o sin fuente, P0 sin historia → no calcula, V35 INCOMPLETO con el motivo. Cero válido en N1 y N2 → se usa el 0. Vuelta a heredado con las opciones escritas → 0 diferencias y aviso B10.
- Plantilla reconstruida con la tabla de trazabilidad por parámetro activo (H/I): SHA-256 `04bab281…bef`; reconstrucción determinista (mismo SHA); referencia 18.834 fórmulas.
- Casos: `…_4_11/scripts/casos_v64.py` (93 casos + 14 rechazos; 53 con referencia leída con todos los decimales de matriz.json y rf_resultados.json) y `generar_libros_casos.py`. Libros congelados para la réplica en el scratchpad `casos_replica/` (plantilla e21ded39…, anterior al ajuste de trazabilidad; las fórmulas de valoración son las mismas).
- Réplica independiente: lanzada con Fable (esfuerzo máximo, contexto separado; especificación en `replica/ESPECIFICACION_REPLICA_INDEPENDIENTE.md`). Se avisó a la persona responsable antes del uso.
- [x] Integración en el pipeline (tarea 3, primera versión):
  - `config_v2_v64_experimental.json` (plantilla V6.4; resto idéntico a config_v2.json).
  - `seleccion_plantilla.py`: selección explícita; `plantilla_activa.json`; código 2 sin escribir si la selección no coincide o falta la configuración.
  - `configuracion_economica.py`: formato v1, validación (incluida la trazabilidad de cada parámetro activo), celdas, aplicación con LibroV63 y verificador V6.4.
  - `variantes_configuracion_v64.py`: heredado, activa, componentes aislados, estructuras compatibles y convenciones (copias recalculadas) → `configuracion_v64_variantes.json/.md`.
  - `pipeline.py`: MUNGER_CONFIG para los subprocesos (config_v2.cargar, verificar_todo.sh, comprobar_entorno.sh, defaults de --config → None); paso 2 aplica la configuración; paso 10 calcula variantes y añade entradas a la fase C; `coherencia_v64` (fase C: parámetros, mantenimiento con adoptada = false, zona solo de variantes calculadas); reaplicación si la configuración cambia (por contenido de las celdas) con vuelta al paso 9/7/3; comprobación en el paso 12.
  - `cierre_v2.MATERIAL_FIJO` += configuracion_economica.json, plantilla_activa.json, configuracion_v64_variantes.json.
  - `leer_v63.configuracion_v64`, `leer_resultados` (clave solo en V6.4), `volcar_datos_v63` (sección 0), `ficha.py` (versiones.plantilla y configuracion_economica, solo V6.4), `informe.py` (§14 y distancias con denominador, solo V6.4), `comprobacion_conjunta.py` (N1, N2, λ, θ movibles), esquemas fase_c (configuracion_v64 opcional) y ficha (plantilla enum, configuracion_economica), prompts fase B, fase C (punto 9) y verificación (dentro de los puntos 1, 10 y 11; siguen siendo 16).
  - Pasada sintética V6.4 (motor B, agentes simulados): concluido · APROBADO; cambiar λ después del cierre → informe.py retira en la primera llamada; el pipeline reaplica, recalcula (21,087 → 20,325), pide fase C y auditoría nuevas y vuelve a cerrar.
- [x] Regresión de las baterías existentes con el código modificado (copia en el scratchpad `regresion/`): entorno, piloto 35, 114/114, 30/30 (mismos nombres que la línea de base), 78/78, 103/103, 55/55, 28/28, 45/45 y cierre 55/55 PASAN; el manifiesto FALLA porque la copia tiene los archivos cambiados (esperado).
- [x] Réplica independiente (Fable, contexto separado): 107/107 casos coinciden a la primera; informe en `replica/INFORME_REPLICA.md`. Observaciones: el terminal con R1 no aplica la regla del máximo conservado (definición de la 4.7.1/4.8.1; límite declarado); crédito terminal en H equivalente a la 4.8.1 solo con fija₁₁ ≥ 0 (todos los casos); ramas sin caso → se añadieron 9 rechazos por dominio y R0 sin circulante (117 casos; la réplica, sobre libros nuevos de la plantilla final: 117/117).
- [x] Control heredado (`scripts/control_heredado_4_11.py`): V6.4 en modo heredado, pipeline real hasta el paso 12 con las salidas de los agentes de la 4.10.1 → V, ponderado 71,664994325, precio de Sí 66,520610325, zona caro y estados idénticos (|Δ| = 0); libro: 120.168 celdas, 44 diferencias, todas en Control maestro (evidencia reescrita) o en la fecha de análisis. `cambiar_base.py comprobar`: CONCUERDA Y SIN RESTOS (la primera pasada encontró 4 restos —M44 «LTM», K45/L45 informe semestral y G-16, y la nota propia que nombraba Bolsamanía/Trading Economics— y se corrigió la configuración: C47 M, C48 K/L y nota de metadatos).
- [x] Batería obligatoria `personaje_v2/pruebas/test_integracion_v64.py` (grupos A plantilla, B casos y réplica, C pipeline, D cambio de base): A 9/9, B 20/20, C 15/15; D en repetición tras corregir la prueba de determinismo (la nota de fase1_v63.json cita el nombre del archivo de cambio: se usa el mismo nombre en las dos preparaciones).
- [ ] Piloto 4.11 (`piloto/Vidrala`, V6.4 experimental, configuración de DEMOSTRACIÓN): preparado con `cambiar_base.py`; pasos 0–4 hechos (96 celdas de configuración escritas); extracción real (Sonnet, esfuerzo medio, contexto limpio): `extracto_v63.md`, 3.881 palabras. Fase A lanzada (Opus, esfuerzo extra, como en la 4.10.1; contexto limpio; sin LibreOffice). Salidas del pipeline en `piloto/resultados/pipeline_0N_*.txt`.
- [ ] Aislamiento de C46/C47 y C49 (`scripts/aislar_entradas_4_11.py`, escrito; se ejecuta tras el cierre del piloto).
- [x] Batería: 53 pruebas (C ganó la de redacción de distancias; `informe.distancias_con_denominador` con «coincide» si son iguales). `verificar_paquete.sh`: bloque V6.4 PRIMERO de los obligatorios (el control de integración de la 4.6.1 extrae el tramo «cierre → RESULTADO GLOBAL»; con el bloque ahí daba 22/23) y mínimo 52.
- [x] Documentación hecha: `v6/v64_experimental/docs/README_V6.4_experimental.md`, `referencia/SHA256_entregables_V6.4_experimental.txt`, ANEXO_D §D.12, `PROMPT_NUEVA_VENTANA.md` (4.11), `REGISTRO_PRUEBAS_4_11.md` (borrador), `INFORME_INTEGRACION_4_11.md` (borrador; falta §3 piloto), `revision_interna/ENCARGO_REVISION_INTERNA_4_11.md` (avisar antes de usar Fable), `scripts/comprobar_entrega_4_11.py`, `scripts/generar_cambios_y_manifiesto.py`, `reproduccion/` (CAMBIOS, MANIFIESTO, CONTINUIDAD, PROMPT, VERSION y verificar_paquete de la 4.10.1).
- [ ] Pendiente al final: CONTINUIDAD.md, VERSION, REGISTRO_ENTREGA_4.11.md, propuesta humana, LEEME de controles históricos (salidas de la copia limpia), borrar `personaje_v2/pruebas/_v64/` y `.lo_perfil` antes del manifiesto, ZIP, partes, verificación sobre copia limpia.

## Respuesta a la revisión interna (12-nov, tarde)

- [x] Código: H1 (selección inversa), H2 (resumen propio de las filas V6.4 y su historial; `cierre_v2.nombre_resumen`), H3 (cobertura del motor y límite del modelo; párrafo en `prompts/fase_a.md`), H7 (§1 del informe), H9 (textos fuera del rango, informativos), H10 (paso 12 y variantes sin zona), H11 (rango de λ o θ y sus extremos), H12 (límites de R1 en la ficha), H14 (propuesta).
- [x] Batería: 58 pruebas (B 21: contraste numérico de las lecturas, H6; C 21: H1, H3, H10 y H2). Grupo C, 21/21; contraste de B, en seco, 0 diferencias en 11.284 filas.
- [x] Ejecuciones del §5 de la revisión: selección inversa sobre una copia del expediente cerrado de la 4.10.1 (CONFORME), rango de λ en el libro del piloto (60,12 y 53,00) y vigencia del piloto con el código final (VIGENTE, en lectura). Un primer intento de la comprobación de vigencia pasó el nombre de la empresa en lugar del de la carpeta y dio un falso «material cambiado»; se corrigió el guion y no se tocó nada del piloto.
- [x] Documentos: README §3, §5, §7 y §8; Anexo D §D.10 y §D.12; informe de integración §1, §3, §4, §5 y §6; propuesta (13 decisiones: D411-MATERIALIDAD y D411-DOMINIOS nuevas); registro de la entrega §4 y §5.

