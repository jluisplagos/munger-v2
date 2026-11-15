# Registro de avance · encargo 4.13

**Qué es.** El registro que permite reanudar el encargo 4.13 desde el último punto, sin esperas indefinidas. Cada línea dice qué se hizo, cuándo y con qué resultado. Hechos comprobados, salvo donde se marca «interpretación».

**Base.** `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip` · SHA-256 615d7dd93d1f981ae83fd8b606c7893304714414a21bf33715156c6117006f88 · 408.223.286 bytes · CRC correcto · VERSION 4.12 · manifiesto 3.796 sin cambios (13-nov, 11:44). Árbol de desarrollo: `/home/claude/trabajo_4_13/munger_v2_r1` (extracción con `unzip`).

## Hito 1 · guardas y coherencia (§3 y §4)

- [x] 11:45–11:50 · Reproducidas las nueve primeras llamadas del hallazgo externo sobre copias aisladas del piloto 4.11 (`scripts/sonda_tipos.py`): configuracion_economica.json nula o lista (pipeline y ficha), N1 = [] (pipeline y ficha), plantilla_activa.json nula (pipeline) y lista (pipeline y ficha): AttributeError antes de la vigencia y la aprobación sin retirar. También fallaban el escalar y PM1 = "x". Informe y resumen ya retiraban.
- [x] Corrección del patrón: `estructura_json.py` (nuevo; planos de configuracion_economica.json, plantilla_activa.json y configuracion_v64_variantes.json); `configuracion_economica.validar` comprueba la estructura antes de cualquier `.get`; `seleccion_plantilla` (comprobar, leer, configuracion, estado) también; segunda barrera `ESTR.protegido` en pipeline, ficha, informe y resumen; `cierre_v2.motivo_vigencia` protegido (una excepción al comprobarla retira la aprobación, lado seguro); informe.py se detiene también con una retirada pendiente (registro de publicaciones ilegible).
- [x] 11:50–11:54 · Sonda repetida con 25 alteraciones × 4 vías (el script final tiene 24: 96 llamadas; nota de la ronda final): todas las alteraciones del material retiran la aprobación en la primera llamada. Lo que no se retira está explicado: solicitud_auditoria.json no es material (el registro que manda está en estado_pipeline.json); registro de publicaciones ilegible → retirada pendiente visible (código 5) en las cuatro vías.
- [x] §4 · `objetivo_v64.accion_evaluada`: la acción FINAL manda; la provisional solo cuenta cuando la final es nula. `contradicciones_salida` cruza acción final, estado, protocolo, objetivo estructurado y objetivo de la decisión con el redondeo declarado (dos decimales; antes, tolerancia del 0,5 %). La usan la coherencia de la fase C, ficha.py (oficial y provisional), informe.py y resumen.py.
- [x] Contraejemplo externo sobre copias de la fase C real de Vidrala (`scripts/sonda_salto.py`): con bloqueo y provisional descartar/comprar, la coherencia lo rechaza; sin protocolo, el tratamiento pasa a «sin protocolo» y el pipeline no lo entrega. Las fases C reales de los tres expedientes siguen aceptadas.
- [x] 11:55–12:02 · Grupo E con 15 pruebas nuevas de tipos (decía 16; corregido por la revisión interna, R9) (14 alteraciones × 4 vías y estado/registro como lista): todas PASA. Grupo F: 40/40 tras adaptar una prueba de columnas cuya ficha de partida era contradictoria (objetivo emitido en un análisis no_entregable), que ahora resumen.py no publica; se usa la ficha del bloqueo.
- [x] Hito 1 cerrado (12:05).

## Hito 2 · conciliación de fuentes y bases (§6 y datos del §7)

- [x] Acciones de Viscofan: `fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`. Contradicción de la nota 20 del AR 2025 confirmada (diluido 2025 < básico con el mismo numerador; en 2024 no). Fuentes oficiales consultadas: BORME (reducción de 500.000 acciones propias inscrita el 11-may-2026 → 46.000.000 acciones; dividendo flexible de junio con amortización simultánea) y CNMV, informe del primer semestre de 2026 (autocartera 396.357 a 30-jun-2026). Sin cifra a 3-nov-2026. Bytes de los PDF de BORME y CNMV no conservados (la consola no llega a esos sitios).
- [x] Vía generativa de la evidencia corregida: `rellenar_fase1_v63.py` sustituye entera la evidencia de Control maestro (G:N) de las celdas frescas (C37, C41, C55, C57) y deja el texto anterior en el registro de la fase 1 (`evidencias_sustituidas`). Probado en una copia de Viscofan: desaparecen «Cierre 6-oct-2026», «53,60 × 45,6036» y «45,60 a 30-jun-2026».
- [x] Contraste selectivo y conciliación de arrendamientos 2021–2025: `scripts/conciliacion_arrendamientos_viscofan.py` → `resultados/conciliacion_arrendamientos_viscofan.md`. 0 errores de lectura; altas 24,110; amortización de derechos de uso 27,051; perímetros: caja (exceso 40,813), NIIF 16 completo (64,923; coherente con el motor B), solo activos propios (67,864; no coherente sin reexpresar NOPAT, capital y puente).

- [x] Plantilla V6.4.1 experimental (`v6/v641_experimental/`): la construye `construir_v641_experimental.py` desde la V6.4, que no cambia. Tiene referencia nueva, SHA-256 y README. ÍNTEGRA con su verificador. Las 17 diferencias de fórmula frente a la referencia V6.4 son todas declaradas.
- [x] Hito 2 cerrado. La evidencia de C37, C41 y C55 del expediente Viscofan nuevo se hará en el Hito 4, al prepararlo.

## Hito 3 · variantes económicas (§5, §7 y §8)

- [x] §7 · Integración de la V6.4.1 en el pipeline:
  - `seleccion_plantilla`: familia V6.4. La V6.4 rechaza el perímetro; la V6.4.1 lo exige cuando hay requisito.
  - `configuracion_economica`: campos `PM1.perimetro_inversion`, `altas_derechos_uso` y `altas_fuente`; traza «PM1.perimetro» en la fila 142; alternativa del otro perímetro. La huella de las configuraciones anteriores no cambia: comprobado con las 4 variantes guardadas de la 4.12.
  - `variantes_configuracion_v64`: `perimetro_alternativo` y sus extremos.
  - Escritura en los libros V6.4.1: vacía siempre el perímetro no declarado.
  - Lectura (`leer_v63`) del perímetro efectivo, en ficha, informe y volcado.
  - Resumen propio: `resumen_v2_v641_experimental.csv`.
  - `config_v2_v641_experimental.json`; esquema de la ficha; prompt de la fase C.
- [x] `compatibilidad_v641.py` vuelto a ejecutar con los textos del resumen B9 excluidos y comprobados: caja 0, caja explícita 0 y heredado 0 diferencias; réplica 0 discrepancias.
- [x] Grupo H de la batería de integración (14 pruebas), incluida una pasada completa del pipeline con la V6.4.1 y NIIF 16: 14/14 PASA.
- [x] §5 · Contrato de cobertura (variantes con formato «4.13»):
  - `objetivo_v64.cobertura`: contraste aislado, variación conjunta necesaria (SR2 ↔ ROIC × f; N1 ↔ escudo; R0 ↔ sin P-M1), variación conjunta o sin cobertura, con la invariancia de la acción aparte.
  - Variantes nuevas de contraste: activa sin N1, escudo alternativo, activa sin N2, R0 sin P-M1, cartera legado y familia alternativa (si la otra familia tiene su parámetro declarado).
  - Fase C: base de la materialidad (calculada, juicio económico o no determinada ⇔ null); evidencia, hechos e inferencias; discrepancias con la configuración revisadas (R5, sin umbral).
  - Avisos de dominio de todas las variantes, agrupados con su efecto (R7, RA5).
  - Ficha, informe, esquemas y prompts de la fase C y de la auditoría.
  - Grupo F 49/49 (9 pruebas nuevas); C, G y H 52/52.
- [x] §8 · `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`:
  - Q-ROIC1: condición recuperada de la 4.9.
  - ROIC 9 % frente a r_op: `resultados/crecimiento_terminal_vidrala.md`; el crecimiento perpetuo aporta +1,57 € al precio de Sí en la activa, no es neutral.
  - H no queda excluido por 2025; mezcla fijo/circulante con sus denominadores para SR1/SRF.
- [x] Hito 3 cerrado.

## Hito 4 · regeneración de lo afectado

- [x] `scripts/preparar_expedientes_4_13.py`:
  - `vidrala_condicionado` y `vidrala_bloqueo`: copias de los cierres de la 4.12; cambio editorial en la configuración, con la huella económica igual.
  - `viscofan`: expediente nuevo con la V6.4.1, perímetro NIIF 16 como punto de cálculo, acciones y notas con su concepto y antecedentes para reutilizar.
- [x] Vidrala condicionado y bloqueo, `--desde 10`: aprobación archivada en la primera llamada; 20 variantes 4.13, todas «caro», con la activa en 56,018; espera la fase C. La fase C de la 4.12 se aparta a `antecedentes/fase_c_4_12/`.
- [x] Viscofan:
  - expediente rehecho antes de ningún agente: se añadieron notas de sensibilidad a C55 y C41; el primer intento queda fuera del árbol.
  - Pipeline con `config_v2_v641_experimental.json`. Reutilización comprobada (`scripts/comprobar_reutilizacion_viscofan.py` → `viscofan/resultados/reutilizacion_4_12.md`): prompts iguales salvo la ruta; libro de datos solo con fecha, evidencia fresca, perímetro y etiquetas; fuentes con los mismos bytes; las salidas no citan cifras de la configuración.
  - Extracto, fase A y fase B de la 4.12 copiados sin cambios.
  - Paso 10: 19 variantes, todas «caro». Activa (NIIF 16, θ 0,5) 38,616; perímetro Caja 39,288; θ = 1 36,878.
- [x] Agentes reales de la fase C, turno 1 (Opus, alto), lanzados en paralelo para Vidrala condicionado, Vidrala bloqueo y Viscofan: no usan LibreOffice. Los relevos están en `resultados/relevos_agentes_4_13.md`.
- [x] Vidrala bloqueo: fase C turnos 1 y 2 aceptados → pendiente_de_datos · Vigilar · objetivo_bloqueado (protocolo). Solicitud SA-c10baafe718ca2a8 (material 8a3db1f6c7bdfb95); el pipeline rechazó la auditoría copiada de la 4.12 (huella ya usada), apartada en antecedentes/. Auditoría nueva (Opus, medio) lanzada.
- [x] Vidrala condicionado: fase C turnos 1 y 2 aceptados → concluido · Vigilar · esperar · objetivo_condicionado 56,02 (provisional). Solicitud SA-f91696ada1687e54 (material 795e4ff5ad2ff161); auditoría de la 4.12 apartada; auditoría nueva (Opus, medio) lanzada.
- [x] Viscofan: fase C turno 1 aceptado (esperar · Vigilar · objetivo_condicionado 38,62; condicionan PM1.estructura y PM1.parametro); turno 2 pedido al mismo agente.
- [x] Vidrala bloqueo: auditoría APROBADO, 16/16 (SA-c10baafe718ca2a8, material 8a3db1f6c7bdfb95, huella dfff8567…). Avisos que no impiden aprobar:
  - la herencia de C93 no nombra la celda;
  - «lo digo en el diagnóstico» para los avisos de dominio no materiales, que solo aparecen en la §14 del informe y en la ficha;
  - N2.margen y PM1.cartera con juicios dentro de `evaluacion` y las inferencias vacías;
  - no existe el historial del resumen.

  Cierre: **pendiente_de_datos · APROBADO · Vigilar · sin acción · objetivo_bloqueado** (valor calculado condicional 56,018).
- [x] Viscofan: fase C turno 2 aceptado → concluido · Vigilar · esperar · objetivo_condicionado 38,62 (provisional; rango 36,88–41,81 en 18 variantes). Solicitud SA-d2b166589c51ea3d (material 003ca0abecdd6d83). Auditoría nueva (Opus, medio) lanzada.
- [x] Vidrala condicionado: auditoría APROBADO, 16/16 (SA-f91696ada1687e54, material 795e4ff5ad2ff161). Avisos: la fase C cita como evidencia de método dos documentos de la orquestación que están fuera del expediente (CORRECCIONES y crecimiento_terminal); «como en la etapa 1» en D68 y B69; «lo digo en el diagnóstico» de los avisos de dominio. Cierre: **concluido · APROBADO · Vigilar · esperar · objetivo_condicionado 56,02 (provisional)**.
- [x] Réplica independiente de los libros finales con `scripts/replica_independiente_v641.py`. Es la de la 4.11 con el perímetro añadido desde su definición económica; la de la 4.11 no cambia.
  - Vidrala condicionado: 21 de 21.
  - Vidrala bloqueo: 21 de 21.
  - Viscofan (V6.4.1, NIIF 16): 20 de 20.
  - Control negativo: la misma réplica sin sumar las altas solo coincide en 9 de 20 libros de Viscofan, así que el perímetro se ejerce de verdad.
- [x] Viscofan: auditoría (Opus, medio) **REPETIR**, 15/16. Falla el punto 9: la herencia de C97 de la fase A reutilizada dice que no hay operaciones de directivos, pero la fila 76 del Control maestro (CNMV, art. 19 MAR) recoge 10 compras y 1 venta. El error ya estaba en la fase A de la 4.12, cuya auditoría lo aprobó: hallazgo para el informe.

  Avisos de la auditoría:
  - la fecha de la ficha es la de la fase A reutilizada (2026-11-12);
  - 59,47 € es la media del precio, no la de la recompra;
  - la naturaleza de la configuración conserva el exceso con «Caja» (40,813).

  Corrección pedida al mismo agente de la fase C, como manda el prompt; no se toca la fase A.
- [x] Viscofan: turno 1 corregido y aceptado (C97 anotada en incoherencias y en celdas_corregidas sin reescribirla; dato ausente de directivos reescrito; recompras y exceso por perímetro corregidos; conclusión igual). Turno 2 pedido.
- [x] Viscofan: turno 2 corregido aceptado → solicitud SA-2f0f7c499ff43a26 (material c76627e1181d2041). Auditoría REPETIR conservada en viscofan/resultados/auditoria_repetir_1/. Segunda auditoría (agente nuevo, Opus, medio) lanzada.
- [x] Viscofan: segunda auditoría APROBADO, 16/16 (SA-2f0f7c499ff43a26, material c76627e1181d2041). Avisos:
  - el informe conserva tres textos de la fase A sobre los directivos (C97), contradichos y anotados por la fase C;
  - las 1.599.709 acciones compradas solo están en texto/AR_2025.txt;
  - el «40,813» de la naturaleza de la configuración;
  - la fecha de la ficha;
  - PM1.perimetro pasa de «convención» (configuración) a «fundamentada» (fase C) sin entrada en contradicciones_revisadas. El contrato mecánico no lo define como discrepancia, pero el prompt de verificación dice «toda discrepancia»: incoherencia entre el prompt y el contrato, para la revisión.

  Cierre: **concluido · APROBADO · Vigilar · esperar · objetivo_condicionado 38,62 (provisional)**.
- [x] `scripts/comparar_4_12_4_13.py` → `resultados/comparacion_4_12_4_13.md`.
  - Vidrala: la misma valoración, más ámbito y juicios nuevos.
  - Viscofan: −0,6715 € de precio de Sí solo por el perímetro; la variante «Caja» reproduce exactamente la 4.12.
- [x] Hito 4 cerrado.

## Hito 5 · revisión, documentos y empaquetado

- [x] 14:27 · Se avisó a la persona responsable. Revisión interna con Fable en contexto separado y solo lectura (`revision_interna/ENCARGO_REVISION_INTERNA_4_13.md` → `REVISION_INTERNA_4_13.md`), en curso. Mientras tanto no se edita código: el revisor lee el árbol.
- [x] Revisión interna recibida: 18 hallazgos (R1–R18; `revision_interna/REVISION_INTERNA_4_13.md`). Correcciones de código:
  - R1 (`ficha.py` leía material antes de la vigencia), R2 (retirada frente a elementos mal formados del registro de publicaciones), R3 (objetivo con un estado final distinto) y R4 (materialidad para el objetivo con su base): corregidos, con pruebas `grupo_e_revision_413` (14/14) y `grupo_f_revision_413` (4/4);
  - R6 (referencia mecánica del S2C con el perímetro NIIF 16), R12 (`Infinity`/`NaN`) y R17 (`en_la_activa` cuenta las lecturas): corregidos, con tres pruebas nuevas del grupo H (19/19);
  - R8 (texto de aptitud de la ficha) y R11 (línea citada de las altas: eran cinco frases, no dos, todas desplazadas en una; `conciliacion_arrendamientos_viscofan.py` corregido y regenerado, solo cambian líneas y etiquetas);
  - R13: seis `__pycache__` borrados; el empaquetado los excluye (las ejecuciones del pipeline los vuelven a crear).
- [x] R5 y R7 · Viscofan (`scripts/corregir_viscofan_revision_4_13.py` → `viscofan/resultados/correccion_revision_4_13.md`):
  - naturaleza de la configuración con el exceso y la cota de SRF del perímetro NIIF 16 (64,923 y 1,2011), cambio editorial con la misma huella económica;
  - C42 = 9,47 sobre la base de 2025 y el precio de las entradas (antes 9,9 de la etapa 1);
  - lista de períodos D88/E88 con las fechas de las entradas y las celdas de contraste que conservan datos de 2026, declaradas;
  - D4 con su período (`rellenar_fase1_v63.py`);
  - la conciliación de acciones dice ahora que la N la introdujo la fase 1 del pipeline V2, no la etapa 1 (que usó 45,60 a 30-jun-2026 y descartó la diluida por la anomalía NIC 33).
- [x] 15:11 · Viscofan desde el paso 2: aprobación retirada y archivada (historial_cierres/01_c76627e1181d2041); fases A, B y C y auditoría apartadas a `viscofan/antecedentes/ejecucion_1_4_13/`; extracción reutilizada otra vez (no cita lo que cambia). Fase A nueva con agente real (Opus, alto) lanzada.
- [x] 15:12 · Vidrala condicionado y bloqueo desde el paso 10: aprobaciones retiradas y archivadas (05_795e4ff5…, 05_8a3db1f6…); fase C, auditoría y variantes apartadas a `antecedentes/ejecucion_1_4_13/`. Variantes recalculadas con R17: `factor_de_reestimacion` pasa a «en la activa» en los dos. Fases C nuevas con agentes reales (Opus, alto) lanzadas.
- [x] Viscofan: fase A nueva aceptada (esquema y citas en el pipeline). Motor B; C97 pasa a «Comprando» con la evidencia de la CNMV; C27 a «Comprimiendo»; B66–D66 reescritas. Referencia mecánica del S2C anclada en B155 = 1,0600 (NIIF 16; antes C53 = 1,1462). Fase B nueva con agente real (Opus, alto) lanzada.
- [x] Vidrala condicionado y bloqueo: turnos 1 nuevos aceptados (esperar · Vigilar; 19 variantes, todas «caro»); turnos 2 pedidos a los mismos agentes. Observación para el informe (hecho, no hallazgo de código): con el mismo material, los dos agentes trazan líneas de materialidad para el objetivo distintas. El de condicionado juzga no material N1 (+1,75 € de precio de Sí); el de bloqueo declara un criterio propio de 1,5 € y lo juzga material, aunque fundado. No hay umbral adoptado, y ninguno se inventa en el sistema: la materialidad para el objetivo depende hoy del juicio del agente (decisión D413-FUNDAMENTO).
- [x] Vidrala condicionado: turno 2 aceptado → concluido · Vigilar · esperar · objetivo_condicionado 56,02 (provisional; rango calculado 51,29–65,72 en 19 variantes). Solicitud SA-5f070ad666596e5f (material f2fe5abba7dcd698). Auditoría nueva (Opus, medio) lanzada.
- [x] Vidrala bloqueo: turno 2 aceptado → pendiente_de_datos · Vigilar · sin acción · objetivo_bloqueado (protocolo). Solicitud SA-ef4407f16aae3f08 (material 9725b95f43a36cc8). Auditoría nueva (Opus, medio) lanzada.
- [x] Viscofan: fase B nueva aceptada (gramática en el pipeline). Palancas NORMAL: crecimiento 4,5 %, margen 16,5 %, S2C 1,1 (la referencia NIIF 16), g 2 %, ROIC 11 %. Variantes recalculadas (las anteriores, apartadas): 19, todas «caro»; activa 40,164 (antes 38,616 con las fases A y B antiguas); rango 38,47–43,39. Grupo de avisos `factor_de_reestimacion` «en la activa» (R17).
- [x] R10 · `scripts/alternativas_acciones_viscofan.py` lee por defecto el libro vigente del expediente 4.13 (`--libro-4-12` repite la lectura antigua, conservada en `resultados/antecedentes_libro_4_12/`). Reproduce el caso activo (40,16401); todas «caro»; con la circulación a 31-dic-2025 el precio de Sí baja un 1,12 %. Se repetirá sobre el libro cerrado.
- [x] Fase C nueva de Viscofan con agente real (Opus, alto) lanzada.
- [x] Vidrala condicionado: auditoría APROBADO, 16/16 (SA-5f070ad666596e5f, material f2fe5abba7dcd698). Dos de sus avisos son defectos de presentación del informe (§14): un grupo de avisos que solo es lectura sin umbral salía «activo en ninguna» (R17 no llegaba al informe) y los juicios económicos sobre el objetivo salían sin su evidencia. `informe.py` corregido (probado en una copia). Como cambia el material auditado, no se cierra con esa aprobación: queda en `vidrala_condicionado/antecedentes/auditoria_material_f2fe5abba7dcd698/`, y `--desde 13` regenera el material (SA-3210a93cafb191c9, material c6693061d0cf8e86). Auditoría nueva (Opus, medio) lanzada. Los otros avisos (ROIC terminal fuera de los condicionantes por juicio; vida de 15 años de los hornos fuera del extracto) van al informe.
- [x] Vidrala bloqueo: auditoría APROBADO, 16/16 (SA-ef4407f16aae3f08, material 9725b95f43a36cc8). Avisos: el mismo «activo en ninguna» de la §14; la §7 del informe decía «0 hipótesis sin fundamento suficiente» (lista D10) mientras la ficha lista cuatro parámetros de la configuración sin fundamento, legible como contradicción; «robusta en todas las variantes» sin «calculadas» en fase_c.md (texto del agente); y el ROIC terminal fuera de los condicionantes por un criterio propio de la fase C (1,06 € frente a 1,5 €), no por un umbral adoptado. `informe.py` corregido también en la §7 (probado en una copia). La auditoría en curso de condicionado (relevo 22) se detuvo antes de escribir nada, porque su material iba a cambiar. Aprobación de bloqueo apartada en `vidrala_bloqueo/antecedentes/auditoria_material_9725b95f43a36cc8/`. `--desde 13` en los dos: SA-22a22574c50575fb (condicionado, material 1beff82a21fffcd6) y SA-b2a2c8774c3e5b4a (bloqueo, material 86e66e0a6876aba2). Auditorías nuevas (Opus, medio) lanzadas.
- [x] Vidrala condicionado: auditoría APROBADO, 16/16 (SA-22a22574c50575fb, material 1beff82a21fffcd6) → **concluido · APROBADO · Vigilar · esperar · objetivo_condicionado 56,02**. Avisos que no impiden aprobar: verificacion_integridad.txt habla del libro antes de las cachés (el final lo acreditan verificacion_libro_final.txt y acreditacion_libro.json); ventas por segmento de 2020 citadas de texto/CF_2021.txt, fuera del extracto; «un 51 % bajo el precio» sin denominador (texto de una Observación de la fase B heredada, no del código); el ROIC terminal fuera de los condicionantes por juicio económico, con su evidencia.
- [x] Vidrala bloqueo: auditoría APROBADO, 16/16 (SA-b2a2c8774c3e5b4a, material 86e66e0a6876aba2) → **pendiente_de_datos · APROBADO · Vigilar · sin acción · objetivo_bloqueado**. Comprueba que las correcciones de §7 y §14 están hechas. Avisos que no impiden aprobar: «como en la etapa 1» en D68 y B69 (con evidencia propia); dos documentos de la orquestación citados como metodología; `causa_si_no_concluido.detalle` y diagnostico.md cortan el motivo a media frase por su límite de longitud (el completo está en `ficha.objetivo.motivo` y en la §14); «robusta en todas las variantes» sin «calculadas»; datos ausentes con «Ninguna celda de juicio» como conclusión afectada.
- [x] Viscofan: fase C nueva, turnos 1 y 2 aceptados → concluido · Vigilar · esperar · objetivo_condicionado 40,16 (provisional; 18 variantes con zona, todas «caro», 38,47–43,39; condicionan PM1.estructura, PM1.parametro y PM1.familia, esta con materialidad para el objetivo no determinada). Solicitud SA-e87a0723e9f4ab0b (material ea1e6fb9f9173a1c). Auditoría nueva (Opus, medio) lanzada.
- [x] Mientras tanto: `scripts/propuesta_humana_4_13.py` (tres grupos, firmas vacías, cifras leídas de los expedientes), `scripts/comprobar_entrega_4_13.py` (control de la entrega frente al manifiesto de la 4.12, conservado en `reproduccion/`) y la guía de uso actualizada. El árbol frente a la 4.12: solo cambia el código declarado; ningún expediente ni plantilla anterior cambia.
- [x] Viscofan: auditoría APROBADO, 16/16 (SA-e87a0723e9f4ab0b, material ea1e6fb9f9173a1c) → **concluido · APROBADO · Vigilar · esperar · objetivo_condicionado 40,16**. Comprueba C97 corregida, el S2C anclado en B155 y la evidencia activa de C37, C41, C42, C55, C57, D4 y D88/E88. Avisos: verificacion_integridad.txt con el libro antes de las cachés; tres citas «palabra, p. n» en fase_c.md; dos hechos tomados de `texto/` (Danville; 1.599.709 acciones propias), verificables en su página y permitidos por el relevo, pero fuera de los extractos; N3.regla «convención» con una evaluación que la llama hipótesis.
- [x] Réplica independiente de Viscofan: 20 de 20. Alternativas de acciones sobre el libro cerrado: reproduce 40,16401; todas «caro»; −1,12 % con la circulación a 31-dic-2025.
- [x] `comparar_4_12_4_13.py`: Vidrala, misma valoración. Viscofan: la reproducción histórica sigue siendo exacta (39,2877008705 con «Caja» y las palancas de la 4.12, primera ejecución de la 4.13); el cambio de la activa (+0,8763 €) se separa en fases A y B nuevas (+1,5386 €, con «Caja») y perímetro NIIF 16 (−0,6623 €, con las palancas nuevas).
- [x] `propuesta_humana_4_13.py` → 13 decisiones (4 de política de salida, 5 de elección por empresa, 4 de ampliación), firmas vacías.
- [x] Hito 4 bis cerrado: los tres expedientes regenerados tras la revisión interna, con agentes reales y auditorías APROBADO del material vigente.
- [x] Segunda revisión interna (Fable, contexto separado, solo lectura; se avisó a la persona responsable antes): `revision_interna/REVISION_INTERNA_4_13_SEGUNDA.md`, 0 bloqueantes, 1 importante (S1), 8 menores, 5 observaciones. Resueltos: S1 y S2 (control de la entrega), S7 (propuesta), S8 (guía), S14 (registro). Declarados en el informe §6: S3, S4, S5, S6, S9, S10, S11. Sin efecto: S12, S13. Los expedientes no se tocan (sus defectos declarados son de textos y no de entradas del motor B).
- [x] Grupos E, F y G con el código final: 112/112 PASAN (antes de la ronda general).
- [x] Sondas de la ronda final sobre el código final (`resultados/sonda_tipos_4_13.txt` y `sonda_salto_4_13.txt`, con la huella de los scripts): 96 primeras llamadas (24 alteraciones × 4 vías), sin excepción; 80 retiran la aprobación con la primera corrección de R1 (79 tras corregir la regresión de la ronda A: ver REGISTRO_PRUEBAS_4_13.md §3). Salto del protocolo: las tres fases C reales se aceptan; las dos sin protocolo quedan en «objetivo_sin_protocolo» y las dos con bloqueo se rechazan.
- [x] Documentos: `REGISTRO_ENTREGA_4.13.md`, `INFORME_INTEGRACION_4_13.md` (pendientes los datos de la ronda), propuesta, guía; `scripts/actualizar_documentos_version_4_13.py` (VERSION, CONTINUIDAD y arranque desde sus copias de la 4.12), `scripts/controles_historicos_4_13.py`, `scripts/generar_cambios_y_manifiesto.py` (4.13).
- [x] CAMBIOS y MANIFIESTO generados (frente a la 4.12: 28 cambiados, 770 nuevos, 0 desaparecidos). Ronda A (`verificar_paquete.sh completa` sobre una copia limpia) lanzada, para fijar el mínimo de la batería.
- [x] Ronda A (40 min): integración V6.4 192/192 y las demás obligatorias pasan salvo trazabilidad 76/78 e integridad 102/103 (regresión de la corrección R1 en `ficha.py`: la comprobación previa miraba también la identidad de la ficha oficial) y el manifiesto (perfiles `.lo_perfil/` de LibreOffice en los tres expedientes). `ficha.py` corregido (solo la aprobación del material, con el motivo siempre impreso; las pruebas no se tocan): trazabilidad 78/78, integridad 103/103, E 42/42. Perfiles borrados. `verificar_paquete.sh` exige al menos 192. VERSION, CONTINUIDAD y arranque actualizados.
- [x] Revisión (Opus, contexto separado) del cambio de `ficha.py` tras la ronda A: H1–H3 (combinaciones con un archivo ilegible; informe cambiado a mano) y H4, H6 corregidos; H5 declarado. Tres pruebas nuevas en E. E 45/45, trazabilidad 78/78, integridad 103/103. Mínimo de la batería: 195. Sondas repetidas con el código final (96 llamadas; 79 retiran; 17 explicadas).
- [x] Ronda B (copia limpia del árbol final, 13-nov 17:42–18:50): `verificar_paquete.sh completa` PASA entera, con la V6.4 en 195/195 (37 min), y el manifiesto queda sin cambios. Controles de las entregas (31 min): 4.2 a 4.6.1 completos; 4.6 en 23/24 (Z-1); 4.7 a 4.8 iguales que en el árbol 4.12; 4.9 a 4.12 con las listas de la 4.13.
  - 4.8.1 da 25/30: el árbol mixto de la 4.8 falla con el `ficha.py` actual (`cierre_v2.leer_ficha_control` no existe en la 4.8). Con el `ficha.py` de la 4.12 en la misma mezcla, da 27/28 y R-T1 sale idéntica: no es una regresión.
  - La 4.13 dio 87/89 por dos defectos del propio control: buscaba «VEREDICTO» y exigía un árbol sin `__pycache__`. Las dos comprobaciones están corregidas.
  - Registro de la batería, detalle de la V6.4 y LEEME en `resultados/`. Huecos del informe y del registro de pruebas rellenados.
- [x] Segunda pasada de los controles, solo los controles, sobre la copia de la ronda B ya con el registro de la batería, el LEEME y el control corregido (30 min).
  - La 4.13 da 89/89.
  - Los demás controles dan lo mismo que en la primera pasada. La 4.9 solo cambia en su lista de archivos nuevos, que incluye los 23 añadidos.
  - Sus salidas son las referencias de `resultados/controles_historicos_en_arbol_4_13/`.
  - CAMBIOS y manifiesto regenerados: 4591 archivos. Siguen el ZIP y la ronda C sobre su descompresión.
