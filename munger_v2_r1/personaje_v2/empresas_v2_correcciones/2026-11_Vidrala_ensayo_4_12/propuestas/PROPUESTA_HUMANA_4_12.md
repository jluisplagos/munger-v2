# Propuesta humana única de la entrega 4.12 (breve, sin firmar)

Propuesta única y breve, sin firmar. Ningún campo humano está relleno y nada de lo que aquí se recomienda está adoptado.

**Estado de los expedientes que la sostienen.** Vidrala · objetivo_condicionado: concluido, esperar, objetivo_condicionado, auditoría APROBADO · Vidrala · bloqueo_del_objetivo: pendiente_de_datos, sin acción, objetivo_bloqueado, auditoría APROBADO · Viscofan: concluido, esperar, objetivo_condicionado, auditoría APROBADO

**No se vuelve a pedir como aprobación:** incorporar el PDF del Bundesbank cuando se disponga de sus bytes (trabajo técnico autorizado); contrastes, reproducciones y correcciones técnicas.

**Información que falta (no son decisiones):** bytes del PDF del Bundesbank (rendbund-data.pdf) para conservar la fuente de rf de Vidrala con su huella; las ediciones exactas de Viscofan de 2016, 2018 y 2021–2023 que cita la fase 1 (sus cifras se contrastaron en otras ediciones); desglose del capex de Vidrala y Viscofan entre mantenimiento, reconstrucción y crecimiento.

## Decisiones necesarias para usar el sistema

### D412-USO

**Pregunta.** ¿Qué uso permite esta entrega: análisis experimental supervisado de empresas de motor B, sin apoyo a decisiones con dinero real?

**Recomendación (argumentada, no adoptada).** Sí a un uso SUPERVISADO y EXPERIMENTAL: expedientes de empresas cuyo motor por los hechos es el B, con la V6.4 en modo experimental como ensayo y el modo heredado (V6.3 efectiva) como control, con la persona responsable revisando cada relevo (guía personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md) y los resultados leídos como valores calculados condicionales. No a decisiones con dinero real mientras sigan abiertas las condiciones del informe (apartado 9): convenciones sin adoptar, hipótesis no observadas, una sola configuración por empresa y dos empresas.

**Alternativas.** usar solo la V6.3 y dejar la V6.4 para pruebas técnicas; apoyar decisiones con dinero real ya (no recomendado: ver apartado 9 del informe).

**Evidencia.** INFORME_INTEGRACION_4_12.md §9 (aptitud de uso y tabla de limitaciones); REGISTRO_PRUEBAS_4_12.md.

**Efectos calculados.** Ninguno en los expedientes: es el alcance del uso.

**Si no se adopta.** La entrega queda como implementación verificada sin uso declarado. Sustituye a: D411-PLANTILLA.

Decisión: — · Fecha: — · Decidido por: —

### D412-PROTOCOLO

**Pregunta.** Cuando hipótesis experimentales sin fundamento suficiente condicionan el precio objetivo (con «esperar» por precio), ¿qué protocolo rige: «objetivo_condicionado» (concluido · esperar, con el precio de Sí como valor calculado condicional y provisional) o «bloqueo_del_objetivo» (pendiente_de_datos, sin acción ni objetivo)?

**Recomendación (argumentada, no adoptada).** Para el uso supervisado, «objetivo_condicionado», porque conserva la información que sí está sostenida (la acción, cuando ninguna variante calculada la cambia) y marca el objetivo como condicional con sus hipótesis. Para cualquier uso con dinero real, ninguno de los dos basta por sí solo: haría falta fundamentar las hipótesis que condicionan el objetivo.

**Alternativas.** «bloqueo_del_objetivo» en todos los casos (más prudente; trata una hipótesis sin fundamento como un dato ausente); «objetivo_condicionado» solo si el rango calculado del precio de Sí está por debajo del precio en todo el ámbito.

**Evidencia.** COMPARACION_PROTOCOLOS_4_12.md; cierre_condicionado/ y cierre_bloqueo/ (mismo material económico, protocolos distintos).

**Efectos calculados.** Vidrala, mismo material: con «objetivo_condicionado» concluido · esperar · objetivo_condicionado (valor calculado condicional 56,02 €); con «bloqueo_del_objetivo» pendiente_de_datos · sin acción · objetivo_bloqueado (el mismo valor calculado condicional, no emitido).

**Si no se adopta.** Cada expediente experimental tiene que declarar su protocolo; sin él no se emite ningún objetivo oficial (objetivo_sin_protocolo). Sustituye a: D411-MATERIALIDAD.

Decisión: — · Fecha: — · Decidido por: —

### D412-FUNDAMENTO

**Pregunta.** Las banderas por parámetro de la fase C (material para el objetivo, fundamento suficiente) deciden qué hipótesis condicionan el objetivo y, con «comprar», qué entra en D10, y ninguna regla las contrasta. ¿Se exige que, con «comprar», todo parámetro activo que la propia configuración clasifica como «hipótesis» cuente como sin fundamento suficiente (y vaya a D10 y a la comprobación conjunta)?

**Recomendación (argumentada, no adoptada).** Sí, para «comprar»: es una regla conservadora que impide que un juicio sin contraste deje una hipótesis no observada fuera de D10. Con «esperar» no cambia nada en los expedientes de la 4.12. Para el objetivo, mantener el juicio de la fase C y revisar en la auditoría que cada «fundamento suficiente» de un parámetro de clase «hipótesis» tenga evidencia con página.

**Alternativas.** dejarlo al juicio de la fase C (como ahora); aplicar la regla conservadora también al objetivo (cambiaría las hipótesis que lo condicionan).

**Evidencia.** revision_interna/REVISION_INTERNA_4_12.md (R5); INFORME_INTEGRACION_4_12.md §9.6 (L15); Anexo D §D.13.

**Efectos calculados.** Ninguno en los expedientes de la 4.12 (ninguno concluye «comprar»). Diferencias de juicio observadas: la regla R1 sale con fundamento suficiente en Vidrala y sin él en Viscofan, y la familia de P-M1 de Viscofan es «hipótesis» en la configuración y está fundamentada para la fase C.

**Si no se adopta.** Una compra podría dejar fuera de D10 un parámetro no observado que la fase C dé por fundado.

Decisión: — · Fecha: — · Decidido por: —

### D412-DOMINIOS

**Pregunta.** ¿Los avisos de dominio (factor f, inversión fija para crecer negativa, terminal de R1 sin máximo conservado, S2C inerte) siguen como avisos sin umbral o se fijan umbrales que impidan una conclusión favorable?

**Recomendación (argumentada, no adoptada).** Siguen como avisos con sus valores, sin umbral, mientras solo haya dos empresas: con las bases de Viscofan la estructura SRF deja de estar definida con λ por encima de 1,1413 y con las de Vidrala por encima de 1,50, así que un umbral fijo no sería comparable entre empresas. Un aviso material ya condiciona el objetivo (limite:<id>) y no admite «comprar».

**Alternativas.** umbral fijo para f (por ejemplo, 1,25) que bloquee «comprar»; umbral por empresa fijado en su configuración.

**Evidencia.** personaje_v2/scripts/dominios_v64.py; README de la V6.4 §8 (9) y §9 (13–15); viscofan/configuracion/analisis_configuracion_viscofan.md.

**Efectos calculados.** Ninguno en los expedientes de la 4.12: en Vidrala, los avisos activos (terminal de R1 sin máximo conservado y S2C inerte en el MALO) y la lectura del factor f no son materiales para la conclusión según su fase C; en Viscofan no hay ningún aviso activo y la fase C da el factor f por no material.

**Si no se adopta.** Se mantienen los avisos sin umbral. Sustituye a: D411-DOMINIOS.

Decisión: — · Fecha: — · Decidido por: —

### D411-TERMINAL-R1

**Pregunta.** ¿Se mantiene el terminal prudente de R1 (carga la inversión para crecer al ritmo g aunque en el MALO las ventas sigan por debajo del máximo conservado) o se especifica uno que reconozca la capacidad sobrante?

**Recomendación (argumentada, no adoptada).** Mantenerlo hasta tener una especificación con su réplica: en Vidrala el efecto máximo es de unos 2,5 € del valor MALO (0,5 € del ponderado) y no cambia la zona; en Viscofan no aplica, porque las ventas superan siempre el máximo conservado.

**Alternativas.** terminal que no invierta hasta recuperar el máximo (sin especificar).

**Evidencia.** REVISION_ECONOMICA_VIDRALA_4_12.md §4; README de la V6.4 §8 (1).

**Efectos calculados.** Solo en el escenario MALO.

**Si no se adopta.** Sigue el terminal prudente.

Decisión: — · Fecha: — · Decidido por: —

### D412-V63

**Pregunta.** ¿Se extienden a los expedientes V6.3 la cadena de trazabilidad del paso 12 y el protocolo del objetivo?

**Recomendación (argumentada, no adoptada).** La cadena de trazabilidad sí (es de solo lectura y ya se puede ejecutar a mano sobre un expediente V6.3); el protocolo del objetivo no, mientras no se decida D412-PROTOCOLO (en la V6.3 rige el Anexo B §B.6.7).

**Alternativas.** las dos; ninguna.

**Evidencia.** Anexo D §D.13; personaje_v2/scripts/trazabilidad_v64.py.

**Efectos calculados.** Ninguno sobre los expedientes históricos (no se reabren).

**Si no se adopta.** Los expedientes V6.3 siguen como en la 4.11.

Decisión: — · Fecha: — · Decidido por: —

## Elecciones económicas de cada empresa

### VIDRALA-CONFIG

**Pregunta.** Vidrala: ¿qué configuración económica se adopta, si alguna? Sigue pendiente de la 4.11: N1 (T1 22,05 % o C52), N2 (M1 18,55 % o C8), N3 (R1 o R0), la estructura de P-M1 (SR1, SR2, SRF, H, S o sin requisito), λ (punto o rango 1,10–1,25), las convenciones y la cartera P0, además de P3 (C49) y C46/C47.

**Recomendación (argumentada, no adoptada).** Ninguna adopción todavía como valoración: la acción («esperar» por precio) no cambia en ninguna de las variantes calculadas, pero el nivel del precio de Sí sí depende de ellas. Si se quiere un punto de partida para el uso supervisado, la configuración de demostración, declarada como no adoptada.

**Alternativas.** modo heredado (V6.3 efectiva); configuración de demostración; otra combinación de las variantes calculadas.

**Evidencia.** cierre_condicionado/resultados/comparacion_homogenea.md; REVISION_ECONOMICA_VIDRALA_4_12.md; propuesta 4.11 (D411-N1 … D411-C46C47).

**Efectos calculados.** Precio 90,10 € (cierre del 31-dic-2025); precio de Sí de la activa 56,02 € y de las variantes calculadas de 51,29 a 65,72 €; heredado 64,75 €.

**Si no se adopta.** Los expedientes de Vidrala siguen siendo ensayos con configuración no adoptada. Sustituye a: D411-N1, D411-N2, D411-N3, D411-PM1-ESTRUCTURA, D411-PM1-PARAMETRO, D411-PM1-CARTERA, D411-P3, D411-C46C47.

Decisión: — · Fecha: — · Decidido por: —

### VISCOFAN-CONFIG

**Pregunta.** Viscofan: ¿se adopta alguna de sus entradas propias? N1 22,12 % (sin las activaciones de bases imponibles negativas) frente a C52 19,83 %; N2 vacío (regla heredada «Último año», 16,36 %); R1 con un circulante del 48,28 % de las ventas; P-M1 SR1 · Θ con θ no observado (rango 0–1, punto de cálculo 0,5); cartera legado.

**Recomendación (argumentada, no adoptada).** Adoptar, si se quiere, solo N1 como dato derivado (la causa del 10,1 % de 2025 está publicada y cuantificada); θ y la estructura siguen siendo hipótesis: no adoptarlas sin un desglose del capex entre mantenimiento y crecimiento.

**Alternativas.** N1 con además los ajustes de ejercicios anteriores (22,66 %); C52 heredado; Λ en lugar de Θ (SRF solo definida hasta λ = 1,1413).

**Evidencia.** viscofan/configuracion/analisis_configuracion_viscofan.md; viscofan/experimental/Viscofan/configuracion_v64_variantes.md.

**Efectos calculados.** Precio 54,70 € (cierre del 3-nov-2026); precio de Sí de la activa 39,29 € y de las variantes calculadas de 38,22 a 41,81 €; heredado 41,81 €.

**Si no se adopta.** El expediente de Viscofan sigue siendo un ensayo con configuración no adoptada.

Decisión: — · Fecha: — · Decidido por: —
