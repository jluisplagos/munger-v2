# Decisiones pendientes · frente B · encargo de cierre (4.14)

**Qué es.** El paquete de decisiones que el encargo de cierre (§6) pide presentar pronto. Para cada decisión dice qué se decide, por qué hace falta, las opciones, una recomendación, la evidencia, el efecto calculado y el tipo de decisión. Nada de lo que aquí se recomienda está adoptado, y ningún campo humano se rellena.

**Base examinada.** `munger_v2_r1`, entrega 4.13, ZIP SHA-256 `b1f747a18cd2123d71c0c1abdca0da049207b4c4eb215aa099f345aed4fbf22a`, extracción de solo lectura en `/home/claude/trabajo_4_14/base/munger_v2_r1`. Las rutas que empiezan por `E413/` abrevian `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/`.

**Autoría.** Agente del frente B (subagente de Claude, Opus). Es un trabajo **interno**, no una revisión externa. Fecha: 14-nov-2026.

**Convenciones del documento.**
- **Hecho:** comprobado en un archivo del paquete o en una fuente citada.
- **Interpretación:** lectura del agente B, discutible.
- **Propuesta:** lo que se recomienda, sin adoptar.
- **Tipos de decisión** (encargo §6): reparación de software · corrección de un dato · elección de una convención · juicio económico · adopción humana de una política.
- Cuando aquí se da una cifra de efecto, sale de un archivo del paquete que se cita. Las cifras nuevas de este documento son aritmética exacta sobre los vectores de escenarios publicados en el paquete, y se marcan «[cálculo B]». El script está en `agentes/B/scripts/descomposicion_viscofan.py`.

---

## 0. Lo que no se pide (ya registrado o ya ordenado)

**Ya registrado. No se vuelve a pedir:**
- **P1** (corrección del circulante de Vidrala de 2024). Está registrado por la persona responsable y aplicado desde la 4.5 (`CONTINUIDAD.md` §5, fila «Ensayo de Vidrala reanudado (4.5)»; `…_4_5/registro_P1/`).
- **Uso experimental supervisado** del motor B. Está autorizado (`E413/propuestas/PROPUESTA_HUMANA_4_13.md`, «No se vuelve a pedir como aprobación»).
- **Reparaciones técnicas, pruebas, contrastes públicos, expedientes nuevos y regeneraciones necesarias.** Están autorizadas sin confirmaciones rutinarias (encargo de cierre §1).
- **Uso selectivo de Fable**, con su motivo y su resultado registrados (`documentacion_reparacion/04_INSTRUCCIONES_POSTERIORES.md`, 15:48 y 16:26). En este frente no se ha usado.
- **r personal del 9 %, con r operativa calculada con las entradas** (encargo §2).
- Comunicación en tercera persona; originales intactos; sin cambios de criterio; sin extracción masiva (`CONTINUIDAD.md` §6).

**Ya ordenado por el encargo de cierre. No es una decisión pendiente; es trabajo que hay que hacer:**
- «Sin base suficiente se declarará "no determinada", no falso» (§5).
- El criterio de 1,5 € es un juicio del agente y no una política (§5). La representación es reparación de software: ver `materialidad_objetivo_diseno.md`, S11.
- No se inventa un umbral universal ni se manda toda hipótesis a D10 de forma automática (§5).
- **Abstención:** «si una incertidumbre material no puede delimitarse de forma defendible, el sistema deberá abstenerse de emitir la conclusión afectada» (§6). Lo que queda por decidir es si la incertidumbre de P-M1 está delimitada (decisión D2), no si rige la regla.
- Corregir S4 y S5 (§7). Cambian el material y retiran aprobaciones; ese efecto está autorizado.
- **VIDRALA-PERIMETRO** (extraer las altas de derechos de uso y calcular las dos variantes) es trabajo técnico autorizado. Deja de ser una pregunta: solo la elección final del perímetro de Vidrala sería decisión, como en Viscofan.
- **D413-MOTOR-A** («qué se exige antes del motor A»): queda sustituida por el encargo §8, que ordena preparar la validación del motor A en paralelo, desde su propia definición económica.

---

## 1. Resumen

| # | Id | Qué se decide | Tipo | Urgencia | Recomendación (sin adoptar) | Efecto calculado |
|---|---|---|---|---|---|---|
| D1 | D413-FUNDAMENTO | Criterio de materialidad para el objetivo y regla de «comprar» | política (a, b); reparación de software (c) | **alta** (§5 y §6) | Sin umbral numérico. Dos reglas que no dependen de un número. Contrato propio para el juicio sobre el objetivo | Los expedientes no cambian de estado; cambia la lista de condicionantes de Viscofan y de Vidrala (§2.1) |
| D2 | D414-DELIMITACION-PM1 (sustituye a D413-PROTOCOLO) | ¿Está delimitada de forma defendible la incertidumbre de P-M1? ¿Qué protocolo rige? | juicio económico + política | **alta** (§6) | Viscofan: delimitable si se acepta la evidencia del desglose por tipo. Vidrala: no delimitada; abstención del objetivo | Vidrala condicionado → pendiente_de_datos o «no comprar sin objetivo» |
| D3 | VISCOFAN-ACCIONES | Número de acciones que divide el valor | corrección de un dato + convención | media | Circulación en una fecha declarada | 40,164 → 39,715 € (−1,12 %); siempre «caro» |
| D4 | VISCOFAN-PERIMETRO | Perímetro de la inversión de P-M1 | convención + juicio económico | media | NIIF 16 | 40,826 («Caja») → 40,164 € (NIIF 16) |
| D5 | VISCOFAN-CONFIG | N1, θ, estructura y cartera de Viscofan | juicio económico + convención | media-alta | N1 como dato derivado; θ con el método del desglose por tipo (no 0,5 sin más) | θ = 0: 41,862 €; θ = 1: 38,466 €; activa 40,164 € |
| D6 | VIDRALA-CONFIG | Estructura de P-M1, λ, N1–N3 y cartera de Vidrala | juicio económico + convención | media | Ninguna adopción como valoración hasta tener una delimitación de P-M1 | Rango 51,29–65,72 €; precio 90,10 € |
| D7 | D414-VARIACION-AGENTES (nueva) | Cómo tratar la variación de juicio entre agentes (sobre todo, las probabilidades) | convención + reparación de software | alta (§7, S10) | Contraste calculado con las probabilidades de referencia siempre que la fase B se desvíe de ellas | Viscofan: las probabilidades explican ≈ +1,63 a +1,66 € de los +1,5386 € |
| D8 | D413-USO | Política de salida: qué uso permite la entrega | política | alta (§6) | Mantener el uso supervisado y experimental; no apto para dinero real | Ninguno en los expedientes |
| D9 | D413-V641 | V6.4.1 en expedientes nuevos | convención | media (tercera empresa, frente C) | Sí, como experimental | Ninguno en los existentes |
| D10 | D413-DOMINIOS | Avisos de dominio sin umbral | política | baja | Mantener sin umbral | Ninguno |
| D11 | D411-TERMINAL-R1 | Terminal prudente de R1 | convención | baja | Mantener | Del orden de 1 € en el MALO de Vidrala (estimación de su fase C) |
| D12 | D412-V63 | Trazabilidad y protocolo en los V6.3 | convención | baja | Trazabilidad sí; protocolo no | Ninguno |

**Orden recomendado para resolver:** D2 → D1 → D7 → D5 → D3/D4 → D8 → D9. D2 y D1 deciden si hay objetivo. D7 decide si el rango calculado recoge la principal fuente de variación medida.

---

## 2. Detalle

### 2.1 D1 · D413-FUNDAMENTO: criterio de materialidad para el objetivo

**Qué se decide.** Cómo se decide que una hipótesis sin fundamento suficiente es «material para el objetivo» y, por tanto, lo condiciona. Además, la regla para «comprar».

**Por qué hace falta.**
- **Hecho:** hoy decide un juicio declarado de la fase C, sin umbral. La coherencia acepta «false · juicio_economico» con una inferencia cualquiera (`pipeline.py`, `_coherencia_cobertura_413`; `E413/revision_interna/REVISION_INTERNA_4_13_SEGUNDA.md` §S3).
- **Hechos, en los expedientes vigentes:**
  - en Viscofan, `PM1.roic_terminal` no tiene fundamento suficiente y mueve el precio de Sí +0,576 € (estructura_SR2 40,7401 frente a 40,1640). Queda fuera de los condicionantes con la inferencia «+0,58 € no es material para el objetivo (juicio)» (`E413/viscofan/Viscofan/fase_c.json`, parámetro PM1.roic_terminal);
  - en Vidrala ocurre lo mismo con +1,058 € (estructura_SR2 57,0765 frente a 56,0181; `E413/vidrala_condicionado/Vidrala/configuracion_v64_variantes.json`);
  - en Viscofan también quedan fuera N3.regla y PM1.convencion_anios, los dos sin fundamento suficiente (fase_c.json).
- **Hecho:** con el mismo material, el agente de vidrala_condicionado juzga N1.tipo no material (+1,75 €, base «juicio_economico»), y el de vidrala_bloqueo lo juzga material con «mi criterio de 1,5 € (juicio mío, no un umbral adoptado)», marcando la base «calculada» (S11). N1.tipo tiene fundamento suficiente en los dos, así que no condiciona ninguno.

**Opciones.**
1. Lo de hoy: juicio declarado, sin umbral, con el contrato actual.
2. **Juicio declarado con contrato propio para el objetivo**, más dos reglas que no dependen de un número:
   - (R-a) con «comprar», todo parámetro activo de clase «hipótesis» cuenta como sin fundamento suficiente y va a D10;
   - (R-b) un parámetro sin fundamento suficiente cuyo contraste mueve el precio de Sí al redondeo declarado solo puede quedar fuera de los condicionantes con un juicio económico con evidencia propia del objetivo. Si no, «no_determinada», que condiciona (encargo §5).
3. Umbral relativo común (un porcentaje del precio de Sí), fijado por la persona responsable y probado en más empresas.
4. Umbral absoluto por empresa (por ejemplo, el 1,5 € de un agente).

**Recomendación (propuesta).** La opción 2. Las reglas R-a y R-b son una política sin número; el contrato propio es una reparación de software (`materialidad_objetivo_diseno.md`).
- No se recomienda un umbral (opciones 3 y 4) con dos empresas.
- El 1,5 € es el criterio de un agente, sin respaldo de pruebas: adoptarlo sería inventar un umbral (encargo §5).
- Interpretación: R-b no manda nada a D10 de forma automática. Solo impide que una frase sin contenido económico excluya una hipótesis que el cálculo muestra que mueve el objetivo.

**Evidencia.** `E413/revision_interna/REVISION_INTERNA_4_13_SEGUNDA.md` §S3 y §S11; `personaje_v2/scripts/pipeline.py` (`_coherencia_cobertura_413`); `personaje_v2/scripts/objetivo_v64.py` (`condicionantes`, `tratamiento`); las fases C de los tres expedientes.

**Efecto calculado (interpretación de una lectura del código, sin ejecutarlo).** Si se aplicara R-b, sin evidencia propia del objetivo:
- en Viscofan entrarían en los condicionantes PM1.roic_terminal, N3.regla y PM1.convencion_anios;
- en Vidrala entraría PM1.roic_terminal.

El tratamiento no cambia: todas las variantes calculadas siguen en «caro», así que la acción se sostiene en el ámbito y ninguno de esos parámetros es material para la acción (`objetivo_v64.evaluar`). Siguen objetivo_condicionado, objetivo_bloqueado y objetivo_condicionado, con más hipótesis nombradas. R-a no cambia ningún expediente, porque ninguno concluye «comprar».

**Tipo.**
- R-a y R-b: adopción humana de una política.
- Contrato propio del juicio sobre el objetivo y marca de un criterio propio del agente (S11): reparación de software. No necesitan decisión.

---

### 2.2 D2 · D414-DELIMITACION-PM1 (sustituye a D413-PROTOCOLO)

**Qué se decide.** Si la incertidumbre de P-M1 (estructura, familia y parámetro λ o θ) está delimitada de forma defendible en cada empresa. De eso depende qué protocolo puede regir el objetivo.

**Por qué hace falta.**
- El encargo §6 fija la regla: sin delimitación defendible, el sistema se abstiene de la conclusión afectada. Un objetivo condicionado o un conjunto de variantes no bastan.
- Hoy Vidrala condicionado y Viscofan emiten un objetivo condicionado (56,02 € y 40,16 €; `E413/INFORME_INTEGRACION_4_13.md` §7). Si P-M1 no está delimitada, eso contradice la regla del encargo.

**Hechos pertinentes.**
- **Viscofan.**
  - θ es «la parte del exceso histórico que fue reposición»: el dominio [0, 1] es lógico, no observado (`viscofan/Viscofan/configuracion_economica.json`, trazabilidad de PM1.parametro). θ = 0: 41,8616 €; θ = 1: 38,4664 €; con «Caja», 41,8616 y 39,7911 €. Estructuras: S 39,5398 €, SR2 40,7401 €, SRF 42,1031 € y H 41,8616 € (`configuracion_v64_variantes.json`). La familia Λ no está calculada y su materialidad para el objetivo es «no determinada».
  - **Hecho nuevo para el paquete:** Viscofan publica cada año el **desglose de su inversión por tipo**. Los textos conservados en el paquete lo traen para 2016, 2019, 2020, 2022 y 2025 (por ejemplo, AR 2025 p. 123 impresa (PDF 144): «€30.9 million (37%) corresponded to investments aimed at increasing capacity … €22.4 million (27%) … environmental and safety … €19.2 million (22%) in process improvements … €11.6 million (14%) in other ordinary investments»; CF 2022, PDF p. 202: «40% … capacity and machinery. 30% … process improvements … 16% … sustainability … 14% … ordinary»; `viscofan/Viscofan/texto/`).
  - La fase C vigente dice que «solo consta 2025, AR_2025 p. 143», y no es exacto: el paquete tiene también 2021 (`IA_2021_es.txt`, PDF p. 213) y 2023 (`IA_2023_es.txt`, PDF p. 250), y 2024 está en la web. Detalle y método en `evidencia_economica.md` §a.
  - **Hecho nuevo:** la contradicción del BPA de Viscofan está también en el formulario estadístico de la CNMV (II semestre de 2025, p. G-11). Afecta a D3; ver `evidencia_economica.md` §b.
- **Vidrala.** λ ∈ [1,10; 1,25] es el rango de una crítica independiente de la 4.8, no una medición (`vidrala_condicionado/Vidrala/configuracion_economica.json`). λ = 1,10: 58,38 €; λ = 1,25: 51,29 €; estructuras de 55,52 a 61,37 €. Las fases C piden el desglose de los hornos, que no está publicado. Búsqueda en `evidencia_economica.md` §a.

**Opciones.**
1. **Delimitada en las dos:** se acepta que el rango calculado de las variantes cubre P-M1. Sigue «objetivo_condicionado».
2. **Por empresa.** Viscofan, delimitada si se acepta un método replicable sobre el desglose por tipo (que sitúa θ cerca de 0 o por debajo; ver D5). Vidrala, no delimitada: abstención del objetivo.
3. **No delimitada en ninguna:** abstención del objetivo en las dos.

Para la abstención hay dos formas:
- (i) «bloqueo_del_objetivo», el protocolo existente: pendiente_de_datos, sin acción ni objetivo;
- (ii) **conclusión sin objetivo:** «no comprar al precio actual», que se sostiene porque todas las variantes están en «caro», sin precio objetivo. Es una extensión nueva de software y no existe hoy: los tratamientos son los de `objetivo_v64.TRATAMIENTOS`. Mantendría los dos protocolos actuales y añadiría un tercero con especificación y pruebas.

**Recomendación (propuesta).** La opción 2, con la forma (i) mientras no se especifique la (ii).
- Viscofan pasa a ser delimitable solo si la persona responsable acepta el método de `evidencia_economica.md` §a como juicio económico, con sus límites.
- Vidrala debe abstenerse del objetivo para cualquier uso que no sea el ensayo experimental. Es exactamente lo que ya hace el expediente vidrala_bloqueo.
- Interpretación: la acción «esperar» de Vidrala y de Viscofan se sostiene en todo el ámbito calculado, pero «esperar» por precio supone un precio que esperar. Por eso la forma (ii) describe mejor lo sostenido («no comprar a 90,10 €») que (i), que deja la acción nula. Si se quiere (ii), es una reparación de software con su especificación, no una firma.

**Evidencia.**
- `E413/vidrala_condicionado/` y `E413/vidrala_bloqueo/`: mismo material, dos protocolos.
- `E413/viscofan/Viscofan/configuracion_v64_variantes.json`.
- `viscofan/Viscofan/texto/AR_2025.txt` (líneas 5948–5975), `CF_2022_compilacion.txt` (8947–8956), `AR_2020.txt` (11250–11258) y `AR_2019.txt` (10555–10562).
- Encargo §6.

**Efecto calculado.**
- Vidrala con abstención (i): pendiente_de_datos · Vigilar · sin acción · objetivo bloqueado. Es el estado vigente de `vidrala_bloqueo` (mismo valor calculado, 56,018 €, no emitido).
- Viscofan con abstención (i): pendiente_de_datos · Vigilar · sin acción (`objetivo_v64.ESPERADO`; no calculado como expediente).
- La forma (ii) no está calculada.

**Tipo.** Juicio económico (¿delimitada?) más adopción humana de una política (qué protocolo rige). La forma (ii) sería además una reparación o ampliación de software.

---

### 2.3 D3 · VISCOFAN-ACCIONES

**Qué se decide.** Qué número de acciones divide el valor de Viscofan.

**Por qué hace falta.** El modelo usa 45,479209 millones, la media ponderada «diluida» de 2025 de la nota 20.2. Es inferior a la básica (45,656226) con el mismo numerador, lo que contradice su propia definición (`E413/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md` §2). La etapa 1 la había descartado por esa anomalía.

**Opciones.**
1. Mantener 45,479209.
2. Media básica de 2025: 45,656226.
3. Circulación a 31-dic-2025 (fecha de las cuentas): 46.500.000 − 506.601 = 45,993399.
4. Circulación a 30-jun-2026 (última cifra oficial antes del precio): 46.000.000 − 396.357 = 45,603643.
5. 3 o 4, más la dilución potencial del plan 2025–2027: hasta 0,315 o 0,4725 millones, con entrega en 2028.

**Recomendación (propuesta).** Un número de acciones con derecho al valor en una fecha declarada, no un promedio de BPA.
- La opción 3 si se prioriza la coherencia con la base de las cuentas.
- La opción 4 si se prioriza la cercanía al precio.
- La dilución potencial, solo si se decide contarla.
- No elegir por el valor.
- **Hecho nuevo** (`evidencia_economica.md` §b): el formulario estadístico de la CNMV del II semestre de 2025 (p. G-11) repite el BPA diluido de 3,52, mayor que el básico de 3,50. La contradicción está en dos ediciones oficiales, así que no es solo una errata del informe en inglés. La opción 1 descansa en una cifra que la propia fuente contradice.

**Evidencia.** `E413/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md`; `E413/resultados/alternativas_acciones_viscofan.md`; `evidencia_economica.md` §b.

**Efecto calculado (E fijo; `alternativas_acciones_viscofan.md`).** Precio de Sí:
- activa: 40,164 €;
- básica: 40,008 €;
- circulación a 31-dic-2025: 39,715 € (−1,12 %);
- circulación a 30-jun-2026: 40,054 €.

Todas quedan en «caro» con el precio de 54,70 €. No cambia el estado.

**Tipo.** Corrección de un dato: la cifra contradictoria. Elección de una convención: la fecha y la dilución.

---

### 2.4 D4 · VISCOFAN-PERIMETRO

**Qué se decide.** El perímetro de la inversión en P-M1: «NIIF 16» (capex de caja más altas de derechos de uso, frente a toda la D&A) o «Caja».

**Por qué hace falta.** «Caja» compara un numerador sin las altas con una D&A que sí incluye su amortización (`E413/resultados/conciliacion_arrendamientos_viscofan.md` §3).

**Opciones.**
1. NIIF 16 (el punto de cálculo actual).
2. «Caja», como en la 4.12.
3. Solo activos propios. No es coherente sin reexpresar el NOPAT, el capital y el puente; no está calculado.

**Recomendación (propuesta).** NIIF 16, coherente con el motor B, que trata los arrendamientos como capital y como deuda.
- **Hecho adicional:** la propia Viscofan define su CapEx como «Investments in intangible assets, property, plant and equipment and rights-of-use assets» (AR 2025, informe de gestión, tabla de taxonomía; `viscofan/Viscofan/texto/AR_2025.txt`, línea 13495).
- Es un apoyo documental a incluir las altas. No prueba que el motor B deba hacerlo, pero indica que la empresa mide su inversión con ese perímetro.

**Evidencia.** `conciliacion_arrendamientos_viscofan.md` (altas 24,110; amortización de derechos de uso 27,051; 0 errores de lectura); `compatibilidad_v641.md`; `viscofan/resultados/dominios_perimetro.md`.

**Efecto calculado.**
- Precio de Sí con las palancas vigentes: NIIF 16, 40,164 €; «Caja», 40,826 € (`configuracion_v64_variantes.json`, perimetro_alternativo).
- Con las palancas de la 4.12: 38,616 frente a 39,288 € (`E413/viscofan/antecedentes/ejecucion_1_4_13/configuracion_v64_variantes.json`).
- No cambia el estado.

**Tipo.** Elección de una convención, apoyada en un juicio económico de coherencia del motor.

---

### 2.5 D5 · VISCOFAN-CONFIG

**Qué se decide.** Las entradas propias de Viscofan:
- N1: 22,12 % frente a C52 19,83 %;
- N2: vacío;
- R1: circulante del 48,28 % de las ventas;
- P-M1: SR1 · Θ con θ = 0,5;
- cartera: legado.

**Por qué hace falta.** θ = 0,5 es el punto medio de un dominio, «sin central económica adoptada» (configuracion_economica.json). Por eso el objetivo depende de una cifra sin construcción económica.

**Opciones para θ.**
1. Punto medio, 0,5 (como ahora).
2. **θ estimado con el desglose por tipo de la propia empresa** (método de `evidencia_economica.md` §a), con su banda.
3. θ = 0 (todo el exceso fue crecimiento; equivale a H o a no tener P-M1).
4. θ = 1 (todo el exceso fue reposición).

**Recomendación (propuesta).**
- Adoptar N1 como dato derivado: causa publicada y cuantificada (`PROPUESTA_HUMANA_4_13.md`, VISCOFAN-CONFIG).
- Para θ, sustituir el punto medio por la opción 2 si la persona responsable acepta el método.
- **Interpretación** (`evidencia_economica.md` §a.2, [cálculo B]): ya hay desglose de los cinco años de 2021–2025; los de 2021, 2022, 2023 y 2025 están en el paquete y el de 2024 solo como texto web. En todos, la inversión que no es de capacidad queda por debajo de la D&A, incluso contando como reposición las mejoras de proceso y EHS. Con la definición amplia, θ = −1,52, que se acota a 0. Para θ = 0,5 habría que tratar como reposición el 80 % de lo que la empresa declara como capacidad.
- No elegir por el valor: θ = 0 sube el precio de Sí y no cambia la zona.

**Evidencia.** `viscofan/Viscofan/configuracion_economica.json`; `configuracion_v64_variantes.md`; `fase_c.json`; textos de AR 2019, 2020, 2022 y 2025 (D2); `evidencia_economica.md` §a.

**Efecto calculado** (`configuracion_v64_variantes.json`).
- θ = 0: 41,8616 €.
- θ = 1: 38,4664 €.
- Activa (θ = 0,5): 40,1640 €.
- activa_sin_N1: 41,6917 €.
- Siempre «caro» con 54,70 €.

**Tipo.** Juicio económico (θ y la estructura); corrección de un dato derivado (N1); elección de una convención (cartera y años).

---

### 2.6 D6 · VIDRALA-CONFIG

**Qué se decide.** La configuración económica de Vidrala: N1, N2, N3, la estructura de P-M1 (SR1, SR2, SRF, H, S o sin requisito), λ, las convenciones y la cartera P0.

**Por qué hace falta.** Sin configuración adoptada, los dos expedientes de Vidrala son ensayos. La 4.13 corrigió las inferencias que apoyaban SR1 (`E413/CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`). Las fases C nuevas no nombran una estructura más coherente; descartan S.

**Opciones.** El modo heredado (V6.3 efectiva); la configuración de demostración, declarada como no adoptada; otra combinación de las variantes calculadas.

**Recomendación (propuesta).** Ninguna adopción como valoración mientras P-M1 no esté delimitada (D2).
- Decidir primero Q-ROIC1, es decir, qué ROIC mide el largo plazo: neto de reposición lleva a SR1; sobre una inversión total, a SR2.
- Buscar evidencia del ciclo de los hornos: vida, coste de reconstrucción y capacidad añadida (`evidencia_economica.md` §a).
- **Hecho:** el crecimiento perpetuo no es neutral (+1,57 € en la activa; `E413/resultados/crecimiento_terminal_vidrala.md`).

**Evidencia.** `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md`; `crecimiento_terminal_vidrala.md`; `vidrala_condicionado/Vidrala/fase_c.json` (configuracion_v64.mantenimiento).

**Efecto calculado** (`PROPUESTA_HUMANA_4_13.md`, VIDRALA-CONFIG).
- Precio de Sí de la activa: 56,02 €.
- Rango calculado: 51,29–65,72 € (19 variantes).
- Heredado 64,75 €; H 61,37; SR2 57,08; SRF 58,43; S 55,52 €.
- Siempre «caro» con 90,10 €.

**Tipo.** Juicio económico (estructura y λ) y elección de una convención.

---

### 2.7 D7 · D414-VARIACION-AGENTES (nueva)

**Qué se decide.** Cómo se trata la variación del juicio entre agentes en la fase B, que hoy no recoge el rango calculado (S10).

**Por qué hace falta.**
- **Hecho [cálculo B]:** de los +1,5386 € de Viscofan («Caja»), las probabilidades de los escenarios explican entre +1,63 y +1,66 €, según el orden. Pasaron de 0,25/0,60/0,15 (4.12, desviadas de la referencia) a 0,20/0,60/0,20 (la referencia mecánica).
- **Hecho [cálculo B]:** los cambios de S2C por R6 y del crecimiento del MALO restan entre 0,08 y 0,13 € según el perímetro y el orden (`descomposicion_viscofan.md`).
- Es decir, casi todo el «bloque de palancas» es una sola desviación de juicio respecto de la referencia, que el agente de la 4.12 tomó y el de la 4.13 no.

**Opciones.**
1. Nada: declararlo como límite, como hoy.
2. **Contraste calculado de probabilidades:** siempre que la fase B se desvíe de la referencia mecánica de probabilidades, se calcula la variante «probabilidades de referencia». Sale exacta sin LibreOffice, porque el precio de Sí depende solo de los valores de escenario y de las probabilidades (`personaje_v2/scripts/precio_de_si.py`, `p_estrella`). Entra en el rango calculado y en el contrato de cobertura.
3. Dos fases B independientes por expediente, con su dispersión declarada. Duplica el coste de los agentes y no resuelve qué juicio vale.

**Recomendación (propuesta).** La opción 2, y la 3 solo como prueba puntual de reproducibilidad.
- Interpretación: no elige entre los dos juicios y no cambia ninguna palanca. Hace visible la desviación de mayor efecto medido.
- No es una variación «espontánea»: los dos agentes argumentan; uno sube el MALO por un mecanismo en marcha y el otro lo rechaza por doble castigo (`descomposicion_viscofan.md` §3).

**Evidencia.** `E413/viscofan/antecedentes/fase_b.json.4_12` y `E413/viscofan/Viscofan/fase_b.json` (palancas.probabilidades); los vectores de escenarios de los dos `configuracion_v64_variantes.json`; `descomposicion_viscofan.md`.

**Efecto calculado [cálculo B].**
- Viscofan vigente con las probabilidades de la 4.12: 38,5364 € (frente a 40,1640).
- Viscofan de la 4.12 con las de referencia: 40,9482 € (frente a 39,2877).
- No cambia la zona.

**Tipo.** Elección de una convención (qué se contrasta) más reparación de software (calcular la variante e incluirla en la cobertura).

---

### 2.8 D8 · D413-USO (política de salida)

**Qué se decide.** Qué uso permite la entrega.

**Por qué hace falta.** El encargo §6 pone la política de salida entre las prioridades, y §1 pide apoyar decisiones con dinero real «dentro de un alcance demostrado».

**Opciones.**
1. Mantener el uso supervisado y experimental del motor B.
2. Solo el modo heredado.
3. Dinero real ya.

**Recomendación (propuesta).** La opción 1. No apto para dinero real mientras sigan abiertas D1 y D2 y la delimitación de P-M1, con dos empresas y sin contraste fuera de muestra. Si D2 se resuelve con abstención, la salida «sin objetivo» sería la conclusión apta en ese alcance.

**Evidencia.** `E413/INFORME_INTEGRACION_4_13.md` §9.

**Efecto calculado.** Ninguno en los expedientes.

**Tipo.** Adopción humana de una política.

---

### 2.9 D9 · D413-V641

**Qué se decide.** Si la V6.4.1 experimental sustituye a la V6.4 en los expedientes nuevos de motor B.

**Por qué hace falta ahora.** La tercera empresa (frente C) necesita una plantilla antes de empezar.

**Opciones.** V6.4.1 en los nuevos; elegir por expediente; solo la V6.4.

**Recomendación (propuesta).** V6.4.1 en los nuevos. Con el perímetro vacío o «Caja» da 0 celdas distintas de la V6.4 (`E413/resultados/compatibilidad_v641.md`).

**Efecto.** Ninguno en los existentes.

**Tipo.** Elección de una convención.

### 2.10 D10 a D12 (pueden esperar)

- **D413-DOMINIOS:** mantener los avisos sin umbral. Efecto nulo en la 4.13. Política.
- **D411-TERMINAL-R1:** mantener el terminal prudente hasta tener una especificación con réplica. Del orden de 1 € en el MALO de Vidrala, según su fase C (no calculado en el libro). Convención.
- **D412-V63:** la trazabilidad sí; el protocolo no. Sin efecto. Convención.

Su texto completo está en `PROPUESTA_HUMANA_4_13.md` y no cambia.

---

## 3. Acciones humanas que no son decisiones

1. **Descargar los documentos oficiales** de la lista de `evidencia_economica.md` §d y dejarlos en la carpeta conectada para conservar sus bytes y huellas (bloqueo B3).
2. **Preguntas a las empresas.** Q-E1–Q-E7 de Vidrala (4.8) y P19 (4.3.1) siguen sin enviar. El sistema no contacta a empresas (encargo §1). Si la persona responsable quiere pedir el desglose de los hornos de Vidrala o el desglose por tipo de 2021, 2023 y 2024 de Viscofan, si no aparece, lo haría ella. No es una condición para continuar el resto.
