# Propuesta humana de la entrega 4.13 (sin firmar)

Propuesta sin firmar. Ningún campo humano está relleno y nada de lo que aquí se recomienda está adoptado.

**Estado de los expedientes que la sostienen.** Vidrala · objetivo_condicionado: concluido, esperar, objetivo_condicionado, auditoría APROBADO · Vidrala · bloqueo_del_objetivo: pendiente_de_datos, sin acción, objetivo_bloqueado, auditoría APROBADO · Viscofan (V6.4.1, NIIF 16): concluido, esperar, objetivo_condicionado, auditoría APROBADO

**No se vuelve a pedir como aprobación:** el uso experimental supervisado (autorizado); reparaciones técnicas, contrastes, reproducciones y regeneraciones de lo afectado.

**Información que falta (no son decisiones):** desglose del capex de Vidrala y Viscofan entre mantenimiento, reconstrucción y crecimiento (condiciona P-M1 en los dos); número de acciones de Viscofan al 3-nov-2026 (no hay cifra oficial); altas de derechos de uso de Vidrala 2021–2025 (VIDRALA-PERIMETRO); bytes de los PDF de BORME y CNMV consultados para las acciones de Viscofan, y del PDF del Bundesbank de rf de Vidrala (no conservados).

## 1. Política de salida

### D413-USO

**Pregunta.** ¿Qué uso permite esta entrega? El uso experimental supervisado ya está autorizado; la pregunta es si algo de la 4.13 cambia ese alcance.

**Recomendación (argumentada, no adoptada).** Mantener el uso SUPERVISADO y EXPERIMENTAL de la 4.12 para empresas de motor B, con la V6.4 o la V6.4.1 experimental como ensayo y el modo heredado como control, y los resultados leídos como valores calculados condicionales. No a decisiones con dinero real: siguen abiertas las condiciones de INFORME_INTEGRACION_4_13.md §9 (convenciones y estructuras sin adoptar, hipótesis no observadas, materialidad que depende del juicio del agente, dos empresas y ningún contraste fuera de muestra).

**Alternativas.** usar solo el modo heredado (V6.3 efectiva) y dejar la capa experimental para pruebas técnicas; apoyar decisiones con dinero real ya (no recomendado: ningún APROBADO ni porcentaje de avance lo acredita).

**Evidencia.** INFORME_INTEGRACION_4_13.md §9; REGISTRO_PRUEBAS_4_13.md; revision_interna/REVISION_INTERNA_4_13.md.

**Efectos calculados.** Ninguno en los expedientes: es el alcance del uso.

**Si no se adopta.** Rige el alcance de D412-USO, que esta propuesta no cambia. Sustituye a: D412-USO.

Decisión: — · Fecha: — · Decidido por: —

### D413-PROTOCOLO

**Pregunta.** Con «esperar» por precio y hipótesis experimentales sin fundamento suficiente que mueven el precio objetivo, ¿qué protocolo rige: «objetivo_condicionado» o «bloqueo_del_objetivo»? Los dos siguen como ensayos no adoptados.

**Recomendación (argumentada, no adoptada).** Para el uso supervisado, «objetivo_condicionado»: conserva lo sostenido (la acción, que no cambia en ninguna variante calculada) y marca el objetivo como condicional con sus hipótesis. Para dinero real ninguno basta: habría que fundamentar las hipótesis que condicionan el objetivo. No se recomienda por emitir un precio: con el mismo material, los dos protocolos dan la misma acción calculada.

**Alternativas.** «bloqueo_del_objetivo» siempre (trata una hipótesis sin fundamento como un dato ausente); «objetivo_condicionado» solo si todo el rango calculado del precio de Sí queda por debajo del precio.

**Evidencia.** vidrala_condicionado/ y vidrala_bloqueo/ (mismo material económico; 4.12: COMPARACION_PROTOCOLOS_4_12.md).

**Efectos calculados.** Vidrala, mismo material: con «objetivo_condicionado», concluido · esperar · objetivo_condicionado (valor calculado condicional 56,02 €); con «bloqueo_del_objetivo», pendiente_de_datos · sin acción · objetivo_bloqueado (el mismo valor, no emitido). Rango calculado del precio de Sí: 51,29–65,72 € en 19 variantes; precio 90,10 €.

**Si no se adopta.** Cada expediente experimental declara su protocolo; sin él no se emite ningún objetivo oficial (objetivo_sin_protocolo). Sustituye a: D412-PROTOCOLO.

Decisión: — · Fecha: — · Decidido por: —

### D413-FUNDAMENTO

**Pregunta.** ¿Qué criterio decide que una hipótesis es material para el objetivo y si tiene fundamento suficiente? Hoy es el juicio económico de la fase C, con su base declarada (calculada, juicio económico o no determinada) y sin umbral adoptado. Además sigue abierta la regla de D412-FUNDAMENTO para «comprar».

**Recomendación (argumentada, no adoptada).** Mantener el juicio declarado con su base y su evidencia, sin umbral, y adoptar dos reglas que no dependen de un número: (1) con «comprar», todo parámetro activo de clase «hipótesis» cuenta como sin fundamento suficiente y va a D10; (2) una materialidad «no determinada» de un parámetro sin fundamento condiciona el objetivo (ya es así en el código). Si se quiere un umbral, que lo fije la persona responsable, relativo al precio de Sí, y que se pruebe en más empresas antes de usarlo.

**Alternativas.** umbral absoluto por empresa (por ejemplo, 1,5 € del precio de Sí, el criterio propio de un agente); umbral relativo (por ejemplo, un porcentaje del precio de Sí) común a todas las empresas; dejarlo todo al juicio de la fase C, también con «comprar» (como ahora).

**Evidencia.** vidrala_condicionado/Vidrala/fase_c.json y vidrala_bloqueo/Vidrala/fase_c.json (configuracion_v64.parametros); REGISTRO_AVANCE_4_13.md (observación de materialidad); revision_interna/REVISION_INTERNA_4_13.md (R14); Anexo D §D.13.

**Efectos calculados.** Con el mismo material de Vidrala, dos agentes trazan líneas distintas: el de condicionado juzga no material N1 (+1,75 € de precio de Sí); el de bloqueo declara un criterio propio de 1,5 € y lo juzga material, aunque fundado. PM1.roic_terminal (+1,06 € en SR2) queda fuera de los condicionantes en los dos por juicio. Ninguno concluye «comprar», así que la regla (1) no cambia ningún expediente de la 4.13.

**Si no se adopta.** La materialidad para el objetivo sigue dependiendo del agente, con su base declarada y revisada por la auditoría. Sustituye a: D412-FUNDAMENTO.

Decisión: — · Fecha: — · Decidido por: —

### D413-DOMINIOS

**Pregunta.** ¿Los avisos de dominio (factor f, inversión fija para crecer negativa, terminal de R1 sin máximo conservado, S2C inerte), ahora calculados en todas las variantes y agrupados, siguen como avisos sin umbral?

**Recomendación (argumentada, no adoptada).** Sí, con sus valores y la conclusión a la que afectan, mientras solo haya dos empresas. Las cotas dependen de las bases y del perímetro: SRF deja de estar definida en λ = 1,2011 con el perímetro NIIF 16 de Viscofan (1,1413 con «Caja») y por encima de 1,50 en Vidrala.

**Alternativas.** umbral fijo para f (por ejemplo, 1,25) que bloquee «comprar»; umbral por empresa en su configuración.

**Evidencia.** personaje_v2/scripts/dominios_v64.py (agrupar); viscofan/resultados/dominios_perimetro.md; configuracion_v64_variantes.md de cada expediente.

**Efectos calculados.** Ninguno en las conclusiones de la 4.13: en los tres expedientes la fase C da los grupos por no materiales para la acción; inversion_fija_para_crecer_negativa forma el extremo superior del rango de Vidrala (variantes con N1, N2 o R0).

**Si no se adopta.** Se mantienen los avisos sin umbral. Sustituye a: D412-DOMINIOS.

Decisión: — · Fecha: — · Decidido por: —

## 2. Elecciones económicas por empresa

### VISCOFAN-ACCIONES

**Pregunta.** Viscofan: ¿qué número de acciones divide el valor? El modelo usa 45,479209 millones, la media ponderada «diluida» publicada de 2025, que contradice su propia definición (menor que la básica con el mismo numerador). La etapa 1 había usado 45,60 a 30-jun-2026 y descartado la diluida por esa anomalía.

**Recomendación (argumentada, no adoptada).** Usar un número de acciones con derecho al valor en una fecha declarada, no un promedio de BPA: la circulación a 31-dic-2025 (45,993399, la fecha de las cuentas) si se quiere coherencia con la base, o la de 30-jun-2026 (45,603643) si se prioriza la cercanía al precio; más la dilución potencial del plan 2025–2027 si se decide contarla. No elegir por el valor: ninguna cambia la zona.

**Alternativas.** mantener la media «diluida» publicada (45,479209); media básica de 2025 (45,656226); circulación a 31-dic-2025 (45,993399); circulación a 30-jun-2026 (45,603643).

**Evidencia.** fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md; resultados/alternativas_acciones_viscofan.md (libro vigente) y antecedentes_libro_4_12/.

**Efectos calculados.** Precio de Sí con E fijo: 40,164 € (activa), 40,008 € (básica), 39,715 € (31-dic-2025), 40,054 € (30-jun-2026); todas «caro» con el precio de 54,70 €. Son sensibilidades de definición con fechas mezcladas, no valoraciones actualizadas.

**Si no se adopta.** El expediente sigue con 45,479209, descrito con su concepto real y su contradicción.

Decisión: — · Fecha: — · Decidido por: —

### VISCOFAN-PERIMETRO

**Pregunta.** Viscofan: ¿qué perímetro de la inversión usa P-M1? «NIIF 16» (capex + altas de derechos de uso frente a toda la D&A; el punto de cálculo del expediente, plantilla V6.4.1 experimental) o «Caja» (capex de caja frente a toda la D&A; lo de la V6.4).

**Recomendación (argumentada, no adoptada).** «NIIF 16», porque es el coherente con el motor B, que trata los arrendamientos como capital y como deuda: «Caja» compara un numerador sin las altas de derechos de uso con una D&A que sí incluye su amortización. No adoptarlo hasta revisar la conciliación de los arrendamientos 2021–2025 (altas 24,110; amortización de derechos de uso 27,051).

**Alternativas.** «Caja» (como en la 4.12); solo activos propios (no coherente sin reexpresar NOPAT, capital y puente; no calculado como variante).

**Evidencia.** resultados/conciliacion_arrendamientos_viscofan.md; resultados/compatibilidad_v641.md; viscofan/resultados/dominios_perimetro.md; v6/v641_experimental/docs/README_V6.4.1_experimental.md.

**Efectos calculados.** Precio de Sí de la activa (NIIF 16, θ = 0,5) 40,164 €; con «Caja» 40,826 €; extremos de θ con «Caja» 41,862 y 39,791 €. Exceso observado 2021–2025: 64,923 (NIIF 16) frente a 40,813 («Caja»).

**Si no se adopta.** El expediente sigue con NIIF 16 como punto de cálculo no adoptado y «Caja» como variante.

Decisión: — · Fecha: — · Decidido por: —

### VISCOFAN-CONFIG

**Pregunta.** Viscofan: ¿se adopta alguna de sus otras entradas propias? N1 22,12 % frente a C52 19,83 %; N2 vacío (regla heredada «Último año»); R1 con un circulante del 48,28 % de las ventas; P-M1 SR1 · Θ con θ no observado (rango 0–1, punto de cálculo 0,5); cartera legado.

**Recomendación (argumentada, no adoptada).** Adoptar, si se quiere, solo N1 como dato derivado (causa publicada y cuantificada); θ y la estructura siguen siendo hipótesis sin un desglose del capex entre mantenimiento y crecimiento.

**Alternativas.** N1 sin además los ajustes de ejercicios anteriores (22,66 %; la configuración usa 22,12 %); C52 heredado; Λ en lugar de Θ (SRF solo definida hasta λ = 1,2011 con NIIF 16).

**Evidencia.** viscofan/Viscofan/configuracion_economica.json; viscofan/Viscofan/configuracion_v64_variantes.md; viscofan/Viscofan/fase_c.json.

**Efectos calculados.** Precio 54,70 € (cierre del 3-nov-2026); precio de Sí de la activa 40,16 € y de las variantes calculadas de 38,47 a 43,39 € (18); heredado 43,39 €. Estado: concluido · esperar · objetivo_condicionado.

**Si no se adopta.** El expediente de Viscofan sigue siendo un ensayo con configuración no adoptada. Sustituye a: VISCOFAN-CONFIG (4.12).

Decisión: — · Fecha: — · Decidido por: —

### VIDRALA-CONFIG

**Pregunta.** Vidrala: ¿qué configuración económica se adopta, si alguna? Siguen pendientes N1, N2, N3, la estructura de P-M1 (SR1, SR2, SRF, H, S o sin requisito), λ, las convenciones y la cartera P0. La 4.13 corrigió las inferencias que apoyaban SR1 (Q-ROIC1, ROIC frente a r_op y la inferencia contra H).

**Recomendación (argumentada, no adoptada).** Ninguna adopción como valoración. Para la estructura: decidir primero qué ROIC mide el largo plazo (Q-ROIC1: neto de reposición → SR1; sobre una inversión total que incluye la reposición → SR2) y la mezcla futura de fijo y circulante (SR1 frente a SRF). Las fases C nuevas no nombran una estructura más coherente; descartan S, que carga otra vez el exceso que ya lleva el S2C histórico.

**Alternativas.** modo heredado (V6.3 efectiva); configuración de demostración, declarada como no adoptada; otra combinación de las variantes calculadas.

**Evidencia.** CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md; resultados/crecimiento_terminal_vidrala.md; vidrala_condicionado/Vidrala/fase_c.json (configuracion_v64.mantenimiento); …_4_9/PRECISION_ROIC_4_9.md.

**Efectos calculados.** Precio 90,10 €; precio de Sí de la activa 56,02 € y de las variantes calculadas de 51,29 a 65,72 € (19); heredado 64,75 €; H 61,37, SR2 57,08, SRF 58,43, S 55,52 €. El crecimiento perpetuo con ROIC del 9 % y r_op 8,689 % aporta +1,57 € en la activa: no es neutral.

**Si no se adopta.** Los expedientes de Vidrala siguen siendo ensayos con configuración no adoptada. Sustituye a: VIDRALA-CONFIG (4.12).

Decisión: — · Fecha: — · Decidido por: —

### VIDRALA-PERIMETRO

**Pregunta.** Vidrala: ¿se concilia su perímetro de la inversión como el de Viscofan (altas de derechos de uso frente a su amortización) y se corrige el perímetro del S2C histórico (entra Brasil y sale Italia)? Los expedientes usan la V6.4 sin perímetro declarado («Caja»).

**Recomendación (argumentada, no adoptada).** Sí como trabajo técnico de la próxima entrega, sin adoptar nada: extraer las altas de derechos de uso de Vidrala 2021–2025 y calcular las dos variantes, como se hizo con Viscofan. El efecto del S2C del mismo perímetro lo estima la fase C de vidrala_bloqueo (≈ −0,55 € de precio de Sí) y el del margen (≈ +0,8 €); no se ha calculado en el libro.

**Alternativas.** dejar «Caja» en Vidrala (los arrendamientos pesan poco en su balance, sin cuantificar); corregir solo el S2C del mismo perímetro.

**Evidencia.** vidrala_bloqueo/Vidrala/fase_c.json (estimación del S2C del mismo perímetro y del margen); vidrala_condicionado/Vidrala/fase_c.json (Palancas!C15, sin cifra).

**Efectos calculados.** No calculados: falta la extracción de las altas de derechos de uso de Vidrala.

**Si no se adopta.** Vidrala sigue con el perímetro «Caja» implícito de la V6.4.

Decisión: — · Fecha: — · Decidido por: —

## 3. Ampliaciones futuras

### D413-MOTOR-A

**Pregunta.** ¿Qué se exige antes de ampliar el sistema al motor A?

**Recomendación (argumentada, no adoptada).** Antes del motor A: decidir D413-FUNDAMENTO (criterio de materialidad) y las elecciones de acciones y de perímetro de Viscofan; una tercera empresa de motor B con arrendamientos relevantes, preparada de cero con la V6.4.1; y una revisión externa de la 4.13. El motor A no comparte P-M1 ni el perímetro: necesitará su propia capa experimental, plantilla, referencia y réplica.

**Alternativas.** empezar el motor A ya, con el motor B como está; ampliar primero el motor B a más empresas y dejar el motor A para después.

**Evidencia.** INFORME_INTEGRACION_4_13.md §10 y §11.

**Efectos calculados.** Ninguno en los expedientes.

**Si no se adopta.** El sistema sigue limitado al motor B.

Decisión: — · Fecha: — · Decidido por: —

### D413-V641

**Pregunta.** ¿La plantilla V6.4.1 experimental (perímetro de la inversión) sustituye a la V6.4 en los expedientes nuevos de motor B?

**Recomendación (argumentada, no adoptada).** Sí para expedientes nuevos, como experimental: con el perímetro vacío o «Caja» da exactamente la V6.4 (0 celdas distintas), y obliga a declarar el perímetro cuando hay requisito. Los expedientes V6.4 existentes no se reabren.

**Alternativas.** mantener las dos y elegir por expediente (como ahora); seguir solo con la V6.4.

**Evidencia.** resultados/compatibilidad_v641.md; pruebas del grupo H; v6/v641_experimental/.

**Efectos calculados.** Ninguno en los expedientes existentes.

**Si no se adopta.** Se elige plantilla por expediente con la selección explícita.

Decisión: — · Fecha: — · Decidido por: —

### D411-TERMINAL-R1

**Pregunta.** ¿Se mantiene el terminal prudente de R1 (carga la inversión para crecer al ritmo g aunque en el MALO las ventas sigan por debajo del máximo conservado) o se especifica uno que reconozca la capacidad sobrante?

**Recomendación (argumentada, no adoptada).** Mantenerlo hasta tener una especificación con su réplica.

**Alternativas.** terminal que no invierta hasta recuperar el máximo (sin especificar).

**Evidencia.** …_4_12/REVISION_ECONOMICA_VIDRALA_4_12.md §4; README de la V6.4 §8 (1); grupo terminal_r1_sin_maximo_conservado de las variantes de Vidrala.

**Efectos calculados.** Solo en el escenario MALO (en Vidrala, del orden de 1 € del precio de Sí según su fase C).

**Si no se adopta.** Sigue el terminal prudente.

Decisión: — · Fecha: — · Decidido por: —

### D412-V63

**Pregunta.** ¿Se extienden a los expedientes V6.3 la cadena de trazabilidad del paso 12 y el protocolo del objetivo?

**Recomendación (argumentada, no adoptada).** La cadena de trazabilidad sí (es de solo lectura); el protocolo del objetivo no, mientras no se decida D413-PROTOCOLO.

**Alternativas.** las dos; ninguna.

**Evidencia.** Anexo D §D.13; personaje_v2/scripts/trazabilidad_v64.py.

**Efectos calculados.** Ninguno sobre los expedientes históricos (no se reabren).

**Si no se adopta.** Los expedientes V6.3 siguen como en la 4.11.

Decisión: — · Fecha: — · Decidido por: —
