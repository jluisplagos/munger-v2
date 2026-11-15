# Informe integrado · encargo 4.13 · fiabilidad del motor B y conciliación económica de los dos casos

**Qué es.** El informe de la entrega 4.13. Separa cuatro cosas que no se pueden mezclar: la **integridad técnica** (el código hace lo que dice y no deja una aprobación que ya no corresponde), la **reproducción numérica** (las cifras salen igual por otra vía), el **fundamento económico** (si las hipótesis están sostenidas) y la **aptitud de uso**. Para cada hallazgo externo dice si está resuelto, pendiente o no reproducido, con su evidencia y su consecuencia. Distingue hechos comprobados, interpretaciones y propuestas. Ningún APROBADO ni ningún porcentaje de avance acredita por sí solo aptitud para decisiones con dinero real.

## 1. En breve

- **Integridad técnica.** Las nueve primeras llamadas con JSON estructuralmente incorrecto que conservaban una aprobación (§3) ahora la retiran, en las cuatro vías. El salto entre la acción provisional y la final (§4) ya no llega a ningún cierre ni a material listo para auditoría. El contrato de cobertura (§5) representa lo no determinado como `null`, distingue juicio de cálculo y agrupa los avisos de dominio de todas las variantes. Hay una plantilla nueva, la **V6.4.1 experimental**, con el perímetro de la inversión, su referencia propia y compatibilidad exacta con la V6.4. La batería de integración pasa entera: 195 de 195 en la ronda final sobre una copia limpia del árbol (ronda B; `resultados/bateria_completa_4_13.txt`), comprobada otra vez sobre la descompresión del ZIP (registro externo de verificación).
- **Reproducción numérica.** La réplica independiente coincide en los tres expedientes finales (21 + 21 + 20 libros). Con el perímetro vacío o «Caja», la V6.4.1 da 0 celdas distintas de la V6.4. La valoración de Viscofan de la 4.12 se reproduce exactamente con «Caja» y las palancas de entonces.
- **Fundamento económico.** Nada nuevo queda adoptado. Las acciones de Viscofan están conciliadas, con la contradicción de la fuente declarada y cuatro alternativas calculadas (todas «caro»). El perímetro NIIF 16 de Viscofan es el coherente con el motor B, pero no está adoptado. Las tres interpretaciones de Vidrala de la 4.12 se han corregido sin cambiar ningún parámetro. La materialidad para el objetivo sigue siendo un juicio del agente: con el mismo material, dos agentes la trazan distinta.
- **Aptitud de uso.** Igual que en la 4.12: uso **supervisado y experimental** en empresas de motor B. **No apta para decisiones con dinero real.**
- **Expedientes finales**, con agentes reales y auditorías APROBADO del material vigente:
  - Vidrala condicionado: concluido · Vigilar · esperar · objetivo condicionado 56,02 €.
  - Vidrala bloqueo: pendiente_de_datos · Vigilar · sin acción · objetivo bloqueado.
  - Viscofan: concluido · Vigilar · esperar · objetivo condicionado 40,16 €.

## 2. Integridad técnica (hechos comprobados)

### 2.1 JSON estructuralmente incorrecto antes de la vigencia (§3)
- **Reproducido.** Las nueve primeras llamadas del hallazgo, sobre copias del piloto 4.11 (`scripts/sonda_tipos.py`), fallaban con AttributeError y dejaban la aprobación. También el escalar y `PM1 = "x"`.
- **Corrección del patrón, no de los ejemplos.**
  - `estructura_json.py` (nuevo) declara la estructura de los archivos de control.
  - `configuracion_economica.validar` y `seleccion_plantilla` comprueban la estructura antes de cualquier `.get`.
  - Una segunda barrera (`ESTR.protegido`) envuelve pipeline, ficha, informe y resumen.
  - `cierre_v2.motivo_vigencia` está protegido: una excepción al comprobarla retira la aprobación.
- **Revisión interna.**
  - R1: `ficha.py` leía material antes de la vigencia.
  - R2: la retirada no estaba protegida frente a elementos mal formados en el registro de publicaciones.
  - Corregidos, con 14 pruebas nuevas.
- **Ronda general.** La primera corrección de R1 rompió tres pruebas obligatorias antiguas (trazabilidad e integridad). La segunda las recuperó, pero una revisión en contexto separado (`revision_interna/REVISION_CAMBIO_FICHA_RONDA_4_13.md`) encontró combinaciones que dejaba sin retirar. La tercera aplica la vigencia completa cuando hay archivos ilegibles y comprueba el informe oficial antes de leer el material; tres pruebas nuevas en E. **Declarado (H5):** sin ficha ni cierre registrado y con el material cambiado, la fila del resumen se retira, pero el estado del pipeline conserva APROBADO, como en todas las versiones anteriores.
- **Ronda final.** `resultados/sonda_tipos_4_13.txt`: 96 primeras llamadas (24 alteraciones × 4 vías), sin ninguna excepción; 79 retiran la aprobación y las 17 restantes están explicadas (la solicitud no es material; el registro de publicaciones ilegible deja la retirada pendiente, código 5; el estado del pipeline como lista detiene cada vía con su motivo; una ficha.json alterada, que no es material, sigue la sustitución W-d de la 4.7.1, con la ficha nueva no vigente) — `REGISTRO_PRUEBAS_4_13.md` §3.

### 2.2 Acción provisional y final (§4)
- `objetivo_v64.accion_evaluada`: manda la acción FINAL; la provisional solo cuenta cuando la final es nula.
- `contradicciones_salida` cruza acción final, estado, protocolo, objetivo estructurado y objetivo de la decisión, con el redondeo declarado (dos decimales). La usan la coherencia de la fase C, la ficha, el informe y el resumen.
- Se conservan:
  - S-19 y D10;
  - las compras sin objetivo;
  - los bloqueos con acción nula;
  - la transición legítima entre provisional y final.
- Contraejemplo externo reproducido y rechazado (`scripts/sonda_salto.py` → `resultados/sonda_salto_4_13.txt`): las tres fases C reales se aceptan; sin protocolo, la provisional «descartar» o «comprar» deja el objetivo «sin protocolo» (ningún objetivo oficial); con bloqueo, las dos se rechazan por contradicción.
- Revisión interna, R3: un estado final distinto del que pide el tratamiento ya no emite objetivo («no_emitido_estado_final»).

### 2.3 Cobertura por hipótesis (§5)
- **Tipos de cobertura** (`objetivo_v64.cobertura`): contraste aislado, variación conjunta necesaria, variación conjunta y sin cobertura.
  - Los vínculos necesarios son los que impone la configuración (SR2 ↔ ROIC × f; N1 ↔ escudo; R0 ↔ sin P-M1); no se amplían para dar cobertura.
  - La invariancia de la acción se calcula aparte.
- **Variantes nuevas de contraste:** activa sin N1, escudo alternativo, activa sin N2, R0 sin P-M1, cartera legado, familia alternativa y, con la V6.4.1, el otro perímetro con sus extremos.
- **Base de cada materialidad**, para la acción y, desde R4, también para el objetivo: calculada, juicio económico o no determinada (⇔ `null`).
  - El pipeline rechaza una «calculada» que contradiga los contrastes y un juicio sin inferencias.
  - «No determinada» con un parámetro sin fundamento condiciona el objetivo; nunca se convierte en «no material».
- **Avisos de dominio** de todas las variantes, agrupados con la conclusión a la que afectan. Desde R17, un grupo que en la activa es una lectura sin umbral cuenta como «en la activa».
- **Umbrales.** No se ha inventado ninguno, y ninguna hipótesis va a D10 de forma automática.

### 2.4 Plantilla V6.4.1 experimental (§7)
- Construida desde la V6.4, que no cambia (`v6/v641_experimental/construir_v641_experimental.py`).
  - Referencia nueva y SHA-256.
  - 17 diferencias de fórmula, todas declaradas.
  - ÍNTEGRA con su verificador.
- Selección explícita: la V6.4 rechaza una configuración con perímetro; la V6.4.1 lo exige cuando hay requisito.
- Compatibilidad (`resultados/compatibilidad_v641.md`): con el perímetro vacío, «Caja» explícita o en heredado, 0 celdas distintas de la V6.4.
- La huella económica de las configuraciones anteriores no cambia (4/4 de la 4.12).

### 2.5 Vigencia en la regeneración
- Cada cambio del material retiró la aprobación en la primera llamada y la archivó en `historial_cierres/`.
- Dos auditorías APROBADO de Vidrala se dieron sobre un material que después se corrigió (informe §7 y §14). **No se usaron para cerrar.** Están guardadas en `antecedentes/auditoria_material_<id>/`, y el material se regeneró con `--desde 13` y una auditoría nueva.
- Una auditoría en curso se detuvo antes de escribir nada, porque su material iba a cambiar.

## 3. Reproducción numérica (hechos comprobados)

| Comprobación | Resultado |
|---|---|
| Réplica independiente (sin fórmulas de la hoja nueva), Vidrala condicionado | 21 de 21 libros |
| Réplica independiente, Vidrala bloqueo | 21 de 21 |
| Réplica independiente con el perímetro desde su definición, Viscofan | 20 de 20 |
| Control negativo: la réplica sin sumar las altas | solo 9 de 20 libros de Viscofan (el perímetro se ejerce de verdad) |
| V6.4.1 con perímetro vacío / «Caja» / heredado frente a V6.4 | 0 / 0 / 0 celdas distintas |
| Viscofan 4.12 con «Caja» y las palancas de la 4.12 | 39,2877008705 = 39,2877008705 (V y ponderado idénticos) |
| Alternativas de acciones: reproducción del caso activo sobre el libro cerrado | 40,16401 = 40,16401 |
| Vidrala 4.13 frente a 4.12 | misma valoración de la activa (56,018) |

**Viscofan: el cambio frente a la 4.12, separado** (`resultados/comparacion_4_12_4_13.md`). Total +0,8763 € de precio de Sí:
- fases A y B rehechas tras la revisión interna, con «Caja»: +1,5386 € (39,2877 → 40,8263);
- perímetro NIIF 16, con las palancas nuevas: −0,6623 € (40,8263 → 40,1640).

Lo que cambió en las palancas: el crecimiento del MALO (1 % → 1,5 %), el S2C del MALO y del BUENO (0,9/1,4 → 0,8/1,3, con la referencia anclada en el perímetro NIIF 16) y las probabilidades (0,25/0,60/0,15 → 0,20/0,60/0,20).

## 4. Fundamento económico

Lo que sigue son hechos comprobados, salvo donde se marca «interpretación».

### 4.1 Viscofan: acciones y evidencia activa (§6)
- **Conciliación** (`fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`).
  - Nota 20 del informe de 2025: básica 45.656.226 (BPA 3,50) y «diluida» 45.479.209 (BPA 3,52), con el mismo numerador. La diluida es menor que la básica, y la nota no lo explica.
  - Emitidas 46.500.000 y propias 506.601: circulación 45.993.399 a 31-dic-2025.
  - BORME: reducción a 46.000.000 en mayo de 2026. CNMV: propias 396.357 a 30-jun-2026.
  - No hay cifra oficial al 3-nov-2026.
  - **Antecedente:** la etapa 1 usó 45,60 a 30-jun-2026 y descartó la diluida por esta anomalía. La media «diluida» la introdujo la fase 1 del pipeline V2.
- **N no se sustituye.** Sigue en 45,479209, descrita con su concepto real.
- **Alternativas** (`resultados/alternativas_acciones_viscofan.md`), con E fijo, todas «caro»:
  - activa 40,164;
  - básica 40,008;
  - 31-dic-2025: 39,715 (−1,12 %);
  - 30-jun-2026: 40,054.
- **Sensibilidad externa** (N = 45,993399: 38,84848 frente a 39,28770). Era del libro de la 4.12. Con aquel libro se reproduce en `resultados/antecedentes_libro_4_12/`.
- **Evidencia activa limpia** en C37, C41, C55, C57 y, tras la revisión interna (R7), también en C42, D4 y la lista de períodos.
  - C42 se recalcula sobre la base: (2.487,7 + 304,075 + 12,243 − 62,79 + 5,422) ÷ 289,99 = 9,47.
  - Algunas celdas de contraste (C24, C31, C33, C34, C38, C40, C53 y C54) conservan datos de 2026 de la etapa 1. **Se declaran, no se borran.** No entran en el motor B.
- **La vía generativa** también está corregida: `rellenar_fase1_v63.py` sustituye la evidencia y guarda la anterior.

### 4.2 Arrendamientos y perímetro de la inversión (§7)
- **Conciliación 2021–2025** (`resultados/conciliacion_arrendamientos_viscofan.md`): concepto, columna, período, signo y unidad de cada cifra, contrastados con el comparativo del informe siguiente.
  - Altas de derechos de uso: 24,110.
  - Amortización de derechos de uso: 27,051.
  - 0 errores de lectura.
  - Desde R11, la línea citada es la de la frase. Eran cinco frases desplazadas en una, no dos.
- **Perímetros:**
  - «Caja»: exceso 40,813;
  - «NIIF 16»: capex + altas frente a toda la D&A, exceso 64,923;
  - solo activos propios: 67,864. No es coherente sin reexpresar NOPAT, capital y puente; no se calcula.
- **Interpretación.** NIIF 16 es el coherente con el motor B, que trata los arrendamientos como capital y como deuda. «Caja» compara un numerador sin las altas con una D&A que sí incluye su amortización. No hay doble cómputo: las altas entran solo en las bases de P-M1 (Configuración V6.4!B153, sumada en B55 y B58: D_hist y F_hist, y de ahí Rh, f y el S2C del perímetro), no en los flujos ni en el puente, que ya tratan el arrendamiento como capital y como deuda.
- **Propagación comprobada** en la plantilla y en la réplica: D_hist, F_hist, Rh, f/f_fija, S2C, requisito y terminal.
- **Variantes:** θ = 0, 0,5 (punto de cálculo) y 1, con los dos perímetros.
- **Dominios** (`viscofan/resultados/dominios_perimetro.md`): SRF deja de estar definida en λ = 1,2011 con NIIF 16 (1,1413 con «Caja»). La cota se calcula sobre su base y no se traslada.
- **Ninguno está adoptado** (VISCOFAN-PERIMETRO).

### 4.3 Vidrala: interpretaciones corregidas (§8)
Documento: `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`. Los documentos de la 4.12 no se tocan.
- **Q-ROIC1.** Se recupera la condición de la 4.9: un ROIC neto de reposición es coherente con SR1; uno medido sobre la inversión total, con SR2. La 4.12 la invertía. No se elige estructura.
- **ROIC terminal del 9 % frente a r_op 8,689151674 %.** El crecimiento perpetuo no es neutral: aporta +1,57 € al precio de Sí en la activa (`resultados/crecimiento_terminal_vidrala.md`). Tampoco se cae en la conclusión contraria.
- **Inferencia contra H.** Un capex mayor que la amortización sin crecimiento no excluye H: con inversión fija para crecer = 0, H paga todo el requisito.
- **Mezcla fijo/circulante,** con denominadores coherentes: D_hist 530,0 = F_hist 251,2 + circulante 278,8; Rh 75,0. Por euro: SR1 0,157 €/€ y SRF 0,288 €/€.
- **Fases C nuevas.** No nombran una estructura más coherente; descartan S, que carga otra vez el exceso que ya lleva el S2C histórico.

### 4.4 Lo que no tiene fundamento suficiente (interpretación)
- **P-M1.** La estructura, el parámetro (λ en Vidrala, θ en Viscofan) y la familia condicionan el objetivo en los dos casos. Falta el desglose del capex entre mantenimiento y crecimiento.
- **Materialidad para el objetivo.** Es un juicio declarado del agente.
  - Con el mismo material, el agente de Vidrala condicionado juzga no material N1 (+1,75 €).
  - El de Vidrala bloqueo fija un criterio propio de 1,5 € y lo juzga material.
  - El sistema lo representa como juicio, con su evidencia, sin umbral: es la decisión D413-FUNDAMENTO.
- **Rango calculado.** Es una sensibilidad condicional a las variantes calculadas. No es una banda de incertidumbre ni un intervalo de confianza.

## 5. Hallazgos externos: estado

| Id | Hallazgo (encargo) | Estado | Evidencia | Consecuencia |
|---|---|---|---|---|
| E1 | §3 · nueve primeras llamadas con JSON estructuralmente incorrecto conservan concluido/APROBADO | **Resuelto** | `estructura_json.py`, `ESTR.protegido`; grupo E (`TIPOS_413`, `grupo_e_revision_413`); `resultados/sonda_tipos_4_13.txt` | Ninguna aprobación queda vigente con material alterado en la primera llamada de las cuatro vías |
| E2 | §3 · material intacto con configuración externa equivocada | **Resuelto** (se conserva el rechazo sin tocar nada) | grupo E; grupo H (V6.4 frente a V6.4.1, código 2 sin escribir) | Una selección equivocada no modifica el expediente |
| E3 | §4 · salto del protocolo con la provisional | **Resuelto** | `objetivo_v64.accion_evaluada` y `contradicciones_salida`; `resultados/sonda_salto_4_13.txt`; grupo F | Ninguna contradicción llega a un cierre ni a material listo para auditoría |
| E4 | §5 · PM1.familia «no cubierta, pero no material»; lo no determinado no se representaba | **Resuelto** (contrato); el **fundamento sigue pendiente** | `objetivo_v64.cobertura`; `pipeline._coherencia_cobertura_413`; fases C | La familia aparece como no determinada o juicio, y condiciona el objetivo si no tiene fundamento |
| E5 | §5 · SR2 sin cobertura por cambiar dos campos vinculados | **Resuelto** | tipo «variación conjunta necesaria»; grupo H | SR2 cubre el ROIC terminal sin ampliar los vínculos |
| E6 | §5 · avisos de dominio solo en la activa | **Resuelto** | `dominios_v64.agrupar`; formato 4.13; ficha e informe §14 | Los avisos de todas las variantes llegan agrupados con su conclusión |
| E7 | §6 · N de Viscofan con un concepto contradictorio | **Pendiente** (decisión humana VISCOFAN-ACCIONES); contradicción **declarada** | conciliación de acciones; alternativas | El precio de Sí puede variar ≈ 1 % según la definición; ninguna cambia la zona |
| E8 | §6 · sensibilidad externa a N = 45,993399 | **Reproducido** sobre el libro de la 4.12; recalculado sobre el vigente | `resultados/antecedentes_libro_4_12/`; `resultados/alternativas_acciones_viscofan.md` | Sensibilidad de definición, no corrección |
| E9 | §6 · evidencia activa que contradice las entradas | **Resuelto** en las cifras frescas, C42, D4 y la lista de períodos; **declarado** en las celdas de contraste con datos de 2026 | `viscofan/resultados/correccion_revision_4_13.md`; Control maestro del libro de datos | Ninguna evidencia activa de una entrada del motor B contradice las entradas |
| E10 | §7 · sensibilidad ROU parcial (solo B60) | **Resuelto** en la representación (V6.4.1, perímetro completo, réplica); la **elección queda pendiente** (VISCOFAN-PERIMETRO) | V6.4.1; conciliación; compatibilidad; réplica | −0,66 € de precio de Sí con NIIF 16 frente a «Caja» (palancas nuevas) |
| E11 | §8 · Q-ROIC1 invertido; 9 % = r; inferencia contra H | **Resuelto** (texto corregido); la **estructura sigue sin elegir** | `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`; fases C nuevas | Las justificaciones activas ya no se apoyan en las inferencias corregidas |

Ningún hallazgo externo queda «no reproducido».

## 6. Revisión interna

**Primera revisión** (Fable, contexto separado, solo lectura; `revision_interna/REVISION_INTERNA_4_13.md`): 18 hallazgos.

| Id | Gravedad | Estado |
|---|---|---|
| R1 | bloqueante | resuelto (`ficha.py`: vigencia antes de leer material; 14 pruebas de E) |
| R2 | importante | resuelto (retirada protegida frente a elementos mal formados del registro de publicaciones; campos del estado reparados con los anteriores guardados) |
| R3 | importante | resuelto (objetivo no emitido con otro estado final) |
| R4 | importante | resuelto (base de la materialidad para el objetivo; fases C de Vidrala rehechas) |
| R5 | importante | resuelto (naturaleza de Viscofan con las bases NIIF 16) |
| R6 | importante | resuelto (S2C anclado en B155; fase B de Viscofan rehecha) |
| R7 | importante | resuelto (C42, D4, lista de períodos; conciliación de acciones con el antecedente de la etapa 1) |
| R8 | menor | resuelto (texto de aptitud de la ficha) |
| R9 | menor | resuelto (recuento corregido: 15 pruebas nuevas del grupo E; pruebas de R1, R2 y R3 añadidas; ronda final con el código final) |
| R10 | menor | resuelto (alternativas de acciones sobre el libro vigente) |
| R11 | menor | resuelto (cinco líneas, no dos) |
| R12 | menor | resuelto (`Infinity` y `NaN` rechazados) |
| R13 | menor | resuelto (`__pycache__` borrados y excluidos del paquete) |
| R14 | observación | declarado: la variación conjunta necesaria admite una materialidad «calculada»; es lo que pide el encargo |
| R15 | observación | declarado: campos redundantes de `cierre_vigente.json` que no se comprueban (no deciden la vigencia) |
| R16 | observación | declarado: `mismo_importe` y los medios céntimos (redondeo declarado a dos decimales) |
| R17 | observación | resuelto (`en_la_activa` cuenta las lecturas; variantes recalculadas) |
| R18 | observación | declarado: fecha de un promedio escrita como fecha de un saldo (texto; sin efecto en cifras) |

**Segunda revisión** (Fable, sobre lo afectado por las correcciones; `revision_interna/REVISION_INTERNA_4_13_SEGUNDA.md`): sin bloqueantes; 1 importante, 8 menores y 5 observaciones. Revisó las correcciones R1–R18 (grupo E con el código actual: 42 de 42; 112 primeras llamadas con tipos anidados, sin excepción), los expedientes (vigentes; regenerar ficha, informe y resumen en copias los deja iguales), la aritmética de C42 y de la comparación y la propuesta (cifras iguales a las salidas).

| Id | Gravedad | Estado |
|---|---|---|
| S1 | importante | resuelto: el control de la entrega confundía la nota de antecedente de C42 («Sustituye al 9,9…») con evidencia activa; ahora la separa y comprueba aparte que la fila declara las fechas de las entradas. No se tocó el libro |
| S2 | menor | resuelto: el control compara los identificadores de la auditoría con la solicitud y el material, llama a `motivo_vigencia`, compara la huella de la auditoría con las apartadas, ata las sondas y la batería a la huella de los scripts, no deja cachés y mira las dos revisiones |
| S3 | menor | **declarado**: el juicio sobre el objetivo comparte `inferencias` con el de la acción; con «juicio_economico» en todos los parámetros sin fundamento, la coherencia aceptaría un objetivo emitido sin condición. Es el límite de un juicio sin umbral (D413-FUNDAMENTO); los expedientes no lo usan así |
| S4 | menor | **declarado**: en Viscofan el S2C NORMAL de las referencias no cambia (1,1 con C53 = 1,146 y con B155 = 1,060, por el redondeo); cambian el MALO y el BUENO. El límite de la ficha «las referencias mecánicas usan las bases heredadas (… S2C sin f)» sigue siendo cierto en «sin f», pero con NIIF 16 el ancla es el S2C histórico del perímetro (B155). Los expedientes cerrados conservan el texto; se corregirá en la próxima entrega |
| S5 | menor | **declarado**: la lista de D88 no nombra C97 (ventana hasta el 7-oct-2026), y dos textos heredados del Control maestro (fila 5, «Pendiente de inversor … LTM jun-26», y E100) contradicen E88. Son textos de la lista de comprobación, no entradas del motor B; corregirlos cambiaría el libro y retiraría la aprobación |
| S6 | menor | declarado: las retiradas previas a rehacer llevan el motivo «no hay auditoria.md», porque la auditoría se apartó antes de la primera llamada; la auditoría está en `antecedentes/` con su huella (`resultados/apartado_*.json`) |
| S7 | menor | resuelto: la propuesta dice qué cifras son literales y de qué documento; «22,66 %» con la redacción de la configuración («sin además los ajustes»); −0,55/+0,8 € atribuidas solo a la fase C de vidrala_bloqueo |
| S8 | menor | resuelto: la guía dice «un archivo del material o un campo de control del que depende la vigencia» |
| S9 | menor | declarado: la prueba de R3 cubre la ficha provisional (el recorrido completo lo reprodujo el revisor) y la de R6 comprueba las etiquetas, no el valor. Los grupos E, F y G con el código final: 112 de 112 (y la ronda final completa) |
| S10 | observación | declarado (§8 y §9.6): repetir las fases A y B con agentes nuevos movió el objetivo de Viscofan +1,54 €, más que el perímetro (−0,66 €), y el rango calculado no recoge esa variación |
| S11 | observación | declarado (D413-FUNDAMENTO): el agente de bloqueo marca «calculada» una materialidad que razona con su criterio de 1,5 € |
| S12 | observación | sin efecto: las dos aprobaciones apartadas responden a solicitudes sustituidas; no queda ninguna aprobación antigua vigente ni reutilizable |
| S13 | observación | sin efecto: el corte a 500 caracteres no cambia el sentido |
| S14 | observación | resuelto en el registro (R2 es el registro de publicaciones); `corregir_viscofan_revision_4_13.py` es de un solo uso, y su registro (`viscofan/resultados/correccion_revision_4_13.json`) guarda lo anterior |

Lo que se corrigió después de la segunda revisión (el control, la propuesta y la guía) no lo volvió a revisar Fable; lo comprueba el propio control en la ronda final.

## 7. Expedientes finales

| Expediente | Plantilla | Estado · cubo · acción · objetivo | Precio de Sí (activa) · rango calculado | Auditoría |
|---|---|---|---|---|
| `vidrala_condicionado/Vidrala` | V6.4 | concluido · Vigilar · esperar · objetivo condicionado 56,02 | 56,018 · 51,29–65,72 (19 variantes) | APROBADO, SA-22a22574c50575fb |
| `vidrala_bloqueo/Vidrala` | V6.4 | pendiente_de_datos · Vigilar · sin acción · objetivo bloqueado | 56,018 · 51,29–65,72 (no emitido) | APROBADO, SA-b2a2c8774c3e5b4a |
| `viscofan/Viscofan` | V6.4.1, NIIF 16 | concluido · Vigilar · esperar · objetivo condicionado 40,16 | 40,164 · 38,47–43,39 (18 variantes) | APROBADO, SA-e87a0723e9f4ab0b |

- **Precios de los casos.** Vidrala 90,10 € (31-dic-2025); Viscofan 54,70 € (3-nov-2026). No se han actualizado cotizaciones.
- **Fases.** Las de Vidrala A y B son las de la 4.12; sus fases C son nuevas. Las de Viscofan A, B y C son nuevas. Todas las hicieron agentes reales (`resultados/relevos_agentes_4_13.md`, 26 relevos).
- **Avisos de las auditorías que no impiden aprobar.** Están en `REGISTRO_AVANCE_4_13.md` y no se han corregido después del cierre:
  - textos de agentes («robusta en todas las variantes» sin «calculadas»; «51 % bajo el precio» sin denominador);
  - el corte a media frase de `causa_si_no_concluido.detalle` por su límite de longitud;
  - hechos tomados de `texto/` fuera de los extractos;
  - la huella del libro antes de las cachés en `verificacion_integridad.txt`.

## 8. Qué falló y cómo se trató

- **Un error que había aprobado una auditoría (hecho).** La fase A de Viscofan de la 4.12 decía que no constaban operaciones de directivos, pero su evidencia de fase 1 (CNMV, 10 compras y 1 venta) sí las recogía. La auditoría de la 4.12 lo aprobó; la de la 4.13 lo encontró. La fase A se rehízo con un agente real. **Interpretación:** una auditoría APROBADO no garantiza que no queden errores de lectura.
- **Defectos del informe hallados por las auditorías.** «Activo en ninguna» para un grupo que sí se lee en la activa, los juicios sobre el objetivo sin su evidencia y «0 hipótesis sin fundamento» junto a cuatro parámetros sin fundamento. Se corrigió el código y se regeneró el material. No se cerró con las aprobaciones del material anterior.
- **Una regresión de una corrección (hecho).** En la ronda A, la corrección R1 de `ficha.py` (vigencia antes de leer el material) rompió dos pruebas de trazabilidad y una de integridad. Comprobaba la vigencia completa, también la identidad de la ficha oficial, y así trataba como retirada la sustitución de una ficha cerrada que esas baterías exigen. Se corrigió el código y no las pruebas. Una revisión en contexto separado del cambio encontró además combinaciones no cubiertas (H1–H4), que también se corrigieron, con tres pruebas nuevas. H5 queda declarado.
- **Dos defectos del control de la entrega (hecho).** En la ronda B, el control de la 4.13 buscaba en el registro de la batería una palabra que `verificar_paquete.sh` no escribe, y exigía un árbol sin `__pycache__` cuando esas carpetas las dejan la batería y los controles anteriores. Se corrigieron las dos comprobaciones (`resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`). El motor no cambió.
- **Revisión interna (R1–R18).** Afectó a material ya aprobado. Se regeneró todo lo afectado: tres fases C, una fase A, una fase B, variantes y auditorías.
- **Variación entre agentes (hecho e interpretación).** Repetir las fases A y B de Viscofan con agentes nuevos movió el precio de Sí +1,54 € (crecimiento del MALO, S2C con la referencia nueva y probabilidades), más que el cambio de perímetro (−0,66 €). **Interpretación:** con el mismo material, el juicio de un agente nuevo mueve el valor más que una corrección económica; el rango calculado de las variantes no recoge esa variación.

## 9. Evaluación expresa de aptitud de uso

### 9.1 Integridad y funcionamiento técnico comprobados
Vigencia ante JSON estructuralmente incorrecto en las cuatro vías. Coherencia entre la acción final, el estado, el protocolo y los dos objetivos. Contrato de cobertura. Plantilla V6.4.1 con referencia y compatibilidad. Pipeline de punta a punta con agentes reales en tres expedientes. Batería de integración: 195 de 195 en la ronda final sobre una copia limpia del árbol (ronda B; `resultados/bateria_completa_4_13.txt`), comprobada otra vez sobre la descompresión del ZIP (registro externo de verificación). Ronda general: `verificar_paquete.sh completa` PASA entera en la ronda B, en unos 37 minutos: manifiesto, entorno, piloto 35, 114/114, 30/30, V6.4 195/195, trazabilidad 78/78, integridad 103/103, solicitudes 55/55, estados 28/28, resumen 45/45 y cierre 55/55. Los controles de las entregas anteriores dan lo que fija `resultados/LEEME_CONTROLES_HISTORICOS_4_13.md`, y el de la 4.13 da 89 de 89.

### 9.2 Resultados financieros reproducidos
- Réplica independiente de los 62 libros finales.
- Reproducción exacta de la 4.12 de Viscofan con «Caja».
- Compatibilidad V6.4 = V6.4.1 con el perímetro vacío.
- Alternativas de acciones que reproducen el caso activo.

### 9.3 Hipótesis y convenciones: contrastadas o pendientes
- **Contrastadas con fuentes:** las cifras de acciones y de arrendamientos de Viscofan (con página, concepto, período, signo y unidad).
- **Pendientes de decisión humana:**
  - N y el perímetro de Viscofan;
  - la configuración de los dos casos;
  - el criterio de materialidad;
  - los protocolos;
  - los dominios.
- **No observadas:** la estructura y el parámetro de P-M1 en los dos casos.

### 9.4 Uso que permite la evidencia
Análisis **experimental supervisado** de empresas de motor B: la persona responsable revisa cada relevo, y los resultados se leen como valores calculados condicionales con sus hipótesis. Guía: `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md`.

### 9.5 Condiciones pendientes antes de apoyar decisiones con dinero real
1. Fundamentar o decidir las hipótesis de P-M1 (desglose del capex).
2. Un criterio de materialidad que no dependa del agente (D413-FUNDAMENTO).
3. Decidir N y el perímetro de Viscofan.
4. Más de dos empresas, y un contraste fuera de muestra (no hay backtest).
5. La revisión externa de esta entrega.

### 9.6 Limitaciones relevantes
- Dos empresas de motor B.
- Bases de 2025 con precios posteriores: no son valoraciones al cierre ni backtests.
- Bytes de BORME, CNMV y Bundesbank no conservados.
- La materialidad depende del agente.
- Una auditoría APROBADO puede dejar errores de lectura (§8).
- El juicio de los agentes varía de una ejecución a otra: en Viscofan, +1,54 € de precio de Sí al repetir las fases A y B (§8); el rango calculado no lo recoge.

## 10. Trabajo pendiente para un producto fiable con dinero real
1. Desglose del capex de Vidrala y Viscofan entre mantenimiento, reconstrucción y crecimiento, con fuentes.
2. Criterio de materialidad adoptado por la persona responsable, y probado en más empresas.
3. Perímetro de Vidrala (altas de derechos de uso) y S2C del mismo perímetro.
4. Tercera empresa de motor B, preparada de cero con la V6.4.1.
5. Un contraste fuera de muestra con bases anteriores, sin rehacer diez años de extracción.

## 11. Siguiente paso antes del motor A
Antes de ampliar al motor A:
1. La revisión externa de la 4.13.
2. Las decisiones D413-FUNDAMENTO, VISCOFAN-ACCIONES y VISCOFAN-PERIMETRO (propuesta sin firmar: `propuestas/PROPUESTA_HUMANA_4_13.md`).
3. Una tercera empresa de motor B con arrendamientos relevantes.

El motor A no comparte P-M1 ni el perímetro: necesitará su propia capa experimental, plantilla, referencia y réplica.

## 12. Alcance real de las pruebas
**Ejecutado de verdad** (el detalle, en `REGISTRO_PRUEBAS_4_13.md`):
- Las baterías obligatorias, en tres rondas. La ronda A sacó a la luz una regresión de la corrección R1 (§8). La ronda B, sobre el árbol final, pasó entera. La ronda C se hizo sobre la descompresión del ZIP.
- Las 96 primeras llamadas de la sonda de tipos y la sonda del salto entre la acción provisional y la final, con la huella de los scripts con que se ejecutaron.
- La réplica independiente de los 62 libros finales, la compatibilidad V6.4.1 frente a V6.4, la reproducción de la 4.12 de Viscofan con «Caja» y las alternativas de acciones.
- El pipeline de punta a punta en tres expedientes, con agentes reales y auditorías nuevas del material vigente.
- Los controles de las entregas 4.2 a 4.13.

**No ejecutado:**
- Ningún backtest, ni un contraste fuera de muestra (fuera del encargo).
- Ninguna tercera empresa.
- Ninguna prueba del motor A.
- Fable no ejecutó pruebas con LibreOffice en su revisión: leyó el código.

**Qué no prueban las pruebas:**
- Que las hipótesis económicas sean correctas.
- Que dos agentes distintos lleguen al mismo juicio de materialidad, que de hecho no llegan (§8).
- Que la variación entre agentes quede dentro del rango de las variantes.
