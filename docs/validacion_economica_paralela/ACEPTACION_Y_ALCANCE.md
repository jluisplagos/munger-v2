# Criterios de aceptación y trabajo paralelo · revisión de lectura · 15-nov-2026

El estado documentado permite continuar el desarrollo y el análisis supervisado. No acredita todavía aptitud para apoyar una decisión de inversión con dinero real. La aceptación técnica, la calidad del análisis de una empresa y la validación de todo el alcance son tres resultados distintos y se deben registrar por separado.

Este informe solo ha leído los árboles indicados y los dos documentos de traspaso posteriores que se identifican abajo. No se han ejecutado pipeline, LibreOffice, baterías ni reconstrucciones; no se han modificado código, fuentes, expedientes ni el repositorio. Los resultados de pruebas citados son **declarados en los artefactos conservados**, no ejecuciones nuevas de esta revisión. Las condiciones y la organización del trabajo que siguen son **propuestas de conciliación y aceptación iniciales**; no implantan un modelo ni una política de inversión nuevos.

## 1. Evidencia y significado de los estados

Rutas abreviadas:

- **B414** = `/workspace/work/revision414_runtime/munger_v2_r1`.
- **B415** = `/workspace/work/revision415_runtime/munger_v2_r1`.
- **E414** = `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14`.
- **E415** = `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15`.
- **D414** = `E414/documentacion_cierre_4_14`.
- **T15** = `/workspace/attachments/069e6182-3ad5-437b-9a9d-1f8b55439ffd/CONTINUIDAD_TRASPASO.md`.
- **F15** = `/workspace/attachments/1929a2d2-5a68-40de-aeb4-cecb8d376364/REGISTRO_FUENTES_15NOV.txt`.

T15/F15 son documentos aportados posteriores al ZIP 4.14; no forman parte de él. Se ha comprobado su contenido textual, no se han reproducido sus lecturas de Excel ni se han recibido/verificado aquí por ello los bytes de las fuentes que enumeran.

| Estado de la evidencia | Hallazgo |
|---|---|
| **Comprobado por lectura** | `B414/D414/MATRIZ_ALCANCE_4_14.md` dice expresamente que el alcance original no está completado. B tiene dos empresas reales; A no tiene validación económica propia; C solo tiene fixtures sintéticos; la entrada por instrucciones carece de batería propia. |
| **Comprobado por lectura** | `B415/E415/HITO_1_4_15.md`, alcance y §4: no se regeneró ningún expediente. Los tres finales de 4.14 son «no apto por entradas» bajo reglas 4.15: sin vínculos vigentes, sin cifras de juicio completas, prácticas antiguas no declaradas y problemas de reproducibilidad. Las aprobaciones históricas no acreditan la aptitud del material futuro. |
| **Declarado con resultados conservados** | Hito1 §5 y §7: entradas 4.15 105/105, entrada efectiva 40/40, integración V6.4 199/199 y regresión completa PASA. §6 conserva cuatro pasadas de revisión de contexto separado; la cuarta dice «aceptable con correcciones», sin bloqueantes, y enumera límites pendientes. |
| **Comprobado por lectura** | Hito1 §2: Elis 4.14 reproduce 108 solo con el valor migrado; sin él C48 cae a 82,933. El CAMBIO propuesto reproduce 108 con y sin valores migrados, pero los casos 3/4 aún dicen `reproduce: false` y código 1 por diferencias documentales. La prueba con código 0 queda para el expediente regenerado. Vidrala C50 = 0 carece de declaración aunque no mueva el precio del motor B. |
| **Comprobado por lectura** | Hito1 §6: U2–U5 siguen pendientes en esa instantánea; U1 es un límite semántico que una regla sobre fórmulas no elimina. §11 mantiene uso experimental supervisado. El trabajo vivo posterior de Claude debe verificarse en una entrega congelada distinta. |
| **Comprobado por lectura** | `B414/D414/DICTAMEN_4_14.md`, C–E: Viscofan/Vidrala «esperar», objetivos condicionados; Elis «pendiente_de_datos · sin acción». Dice «no es apto para decisiones con dinero real». La réplica numérica no valida las hipótesis ni la capacidad predictiva. |
| **Comprobado por lectura** | `B414/D414/hito1/SELECCION_TERCERA_EMPRESA.md`: Elis fue primera candidata y Ahold reserva, seleccionadas antes de valorar. Si Elis resulta A se debe conservar esa clasificación y evaluar la reserva. Elis no cubre un tercer caso B. |
| **Declarado en traspaso posterior** | T15 §7 define H-P1 y §6 lo relaciona con X2: textos del Control maestro de los tres finales contradicen la base aplicada. Viscofan F5/D88/E88/E100 siguen pendientes/LTM y D88 no declara C97; Vidrala F5/D88 siguen pendientes/LTM; Elis D88 conserva acciones 7-oct-2026 pese a E6 de 31-dic-2025. No se corrigió en el ZIP. |
| **Declarado en registro posterior** | F15 enumera fuentes conseguidas fuera del ZIP con nombres/huellas y carencias. La presentación Beat’30, la transcripción de Vidrala y el PDF del informe Viscofan 2024 siguen sin acreditarse allí como recibidos. La nota 2025 no sustituye a Beat’30; la presentación de Vidrala no sustituye a la transcripción; una web no sustituye al PDF. Nada estaba incorporado a los expedientes según el registro. |

No se han comprobado en esta revisión las ramas remotas ni el trabajo sin publicar. Según la coordinación, la captura del frente vivo muestra trabajo técnico: Rsign marcado y trabajo U2–U5/I20 en HTML; regresión y revisión pendientes. Esto es evidencia de actividad, no una corrección publicada o aceptada. El estado económico no se infiere de esa captura.

## 2. Aceptación común de cada expediente nuevo

**Propuesta:** cada expediente conserva una ficha de aceptación con resultado por condición, ruta de evidencia, versión del código y del modelo, fecha de corte, autor y revisor. Un «APROBADO» de auditoría no sustituye a estas condiciones.

| Puerta | Criterio concreto | Evidencia para cerrarla |
|---|---|---|
| P0 · base identificada | Origen intacto y expediente nuevo; código, configuración, plantilla, fuentes y decisiones identificados por commit/huella. Se distingue base contable de fecha de precio. | Manifiesto, inventario, cambio de base con declaradas/conservadas/descartadas y sus motivos; sin decisiones implícitas. |
| P1 · datos completos y semántica | Universo de cálculo y de juicio completo; documento oficial, versión/período, página PDF, cita, moneda, unidad, escala y signo; revisión del concepto, columna y perímetro. Cero comprobado, ausente, hipótesis y no aplicable quedan separados. | Mapa de celdas a fuentes y registro íntegro; revisión independiente contra los bytes, no solo búsqueda numérica. Lectura externa material sin bytes no equivale a entrada comprobada. |
| P2 · fundamento vigente | Cada dato o derivado material tiene comprobación independiente y vínculo vigente; un dato tratado como hipótesis y la no materialidad de un dato de juicio quedan razonados y revisados. | Registro sellado por revisor distinto del extractor; huellas de orígenes, evidencia del libro y fundamento. Una huella detecta cambios: no acredita por sí sola autoría ni verdad semántica. |
| P3 · reconstrucción | Se genera en carpeta limpia con modo estricto efectivo; la entrada declarada reproduce C46–C50 sin depender de valores migrados. Reconstrucción con y sin migrados concuerda en datos, fórmulas y resultados. | Declaración coherente de modo, metadatos, registro y estado; resultados y salida exitosa contra el propio expediente ya regenerado. Diferencias documentales solo se excluyen si están identificadas y justificadas previamente. |
| P4 · economía explícita | Motor elegido por los hechos; identidades contables conciliadas; supuestos activos y variantes razonables completos, sin escoger por su resultado. Incertidumbre material acotada con fundamento o abstención sobre la conclusión afectada. | Memoria económica, decisiones aplicadas, alternativas, sensibilidad y razones de materialidad. Cálculo independiente confirma las cifras; revisión económica confirma que el cálculo corresponde al negocio. |
| P5 · salida fiel | Ficha, informe y estado muestran la misma aptitud, límites, modo de entrada, fechas y acción. «Apto por entradas» no se presenta como validación del modelo. | I20 integrado y verificado en la versión usada; recuentos N ≤ M separados por cálculo/juicio y auxiliares. Ninguna cifra antigua en el juicio por no entrar en la fórmula. |
| P6 · auditoría y vigencia | Auditoría de contexto separado sobre el material final exacto. Cambiar material invalida el cierre y genera un relevo válido. | Solicitud/respuesta y huella final coincidentes; I19 comprobado; nueva auditoría después del último cambio; prueba de traspaso sin historial y con auditor separado. |
| P7 · uso concreto | Antes de apoyar una decisión real: revisión externa técnica y financiera de lo que se usa, políticas económicas adoptadas expresamente, fuentes y datos pertinentes para la fecha y juicio documentado para esa decisión. | Dossier con precio y fecha vigentes, supuestos, valor/rango condicionado, sensibilidad, riesgos y factores que invalidan la tesis; revisión humana. La exposición depende de la situación del usuario y no la determina este informe. No se deduce de un contador de tests ni implica ausencia de pérdidas. |

P0–P6 definen un expediente técnicamente reproducible y revisable; P4 también exige juicio financiero. P7 exige evidencias adicionales del uso concreto. Ninguna puerta sirve para prometer que se evitarán pérdidas: datos correctos y un modelo coherente pueden producir una inversión perdedora.

## 3. Condiciones adicionales por expediente

**Propuestas**, apoyadas en los pendientes documentados:

| Expediente | Pendientes que deben resolverse y conservarse |
|---|---|
| **Viscofan** | Regenerar universo completo (cálculo y juicio), vínculos, redondeos/unidades explícitos. Reexpresar `Análisis!C42` con la capitalización coherente con D3 o justificar una base distinta; que no entre en motor B no permite dejar un dato de juicio desfasado. Mantener D3/E1 ya autorizados y separar fecha de acciones 2025/precio 2026 y dilución potencial. Resolver con fundamento P-M1, estructura, perímetro y parámetros; contrastar probabilidades de referencia si el agente se aparta. Auditoría nueva. |
| **Vidrala** | Declarar C50 antes de reconstruir; no promoverlo a cero verificado sin fuente/derivación válida. Conservar E1 y E2/P1 ya decididos; E2 mantiene K14 publicado y reserva económica separada, sin descontar plusvalía sin conciliación. E3/E4 siguen siendo supuestos declarados, no decisiones humanas. Delimitar P-M1 o abstenerse del objetivo afectado; documentar altas NIIF 16 y perímetro antes de elegirlos. Registros y auditoría nuevos. |
| **Elis** | C48 = 108 con derivación completa y reconstrucción sin migrados; prueba exitosa sobre el expediente nuevo. Mantener E6: base coherente 31-dic-2025, OCEANE como deuda y sin añadir también las acciones de conversión; dilución e intereses separados; no presentarlo como actualización 2026. Resolver F1 mediante especificación, referencia, réplica y recorrido nuevo si se corrige. Delimitar capex de reposición/crecimiento con dato o estimación defendible; si no, conservar `pendiente_de_datos`. No utilizar el precio defectuoso de 7,30 €. |
| **Tercer caso B** | Confirmar disponibilidad del expediente de Ahold y fuentes; inventariar antes de repetir etapa 1. Fase A puede concluir otro motor: no se fuerza B. Solo contará como tercer caso B si la clasificación B está fundada y completa el recorrido con datos revisados, configuración propia congelada antes de valorar, reconstrucción y auditoría. Si no, registrar el resultado y seleccionar otra candidata con reglas previas. |
| **Caso real C** | Empresa financiera real, fuentes oficiales y especificación económica propia de banco o aseguradora. Definir qué entradas y fórmula corresponden a ese negocio; completar reconstrucción, réplica y auditoría. Dos fixtures no acreditan transferencia real; un caso real tampoco acredita todos los bancos y aseguradoras. |

**Evitar aprobaciones repetidas o falsas.** `B414/D414/DECISIONES_ENTRADAS_4_14.md` registra E1, D3, E2 y E6 como decisiones de la persona responsable. No siguen pendientes por el mero hecho de que `DECISIONES_PENDIENTES_4_14.md` los contuviera antes. E3/E4 y el tratamiento actual de F1 son supuestos de la orquestación. P-M1, protocolo del objetivo y k = 3 no están adoptados por pasar las pruebas.

**H-P1/X2 en los tres expedientes:** conciliar todos los textos del Control maestro con la base/decisiones vigentes, no solo las celdas que alimentan fórmulas. Registrar F5/D88/E88/E100 y C97 cuando correspondan, regenerar desde la primera dependencia afectada en expedientes nuevos y auditar de nuevo el material final. La ausencia de efecto en precio no cierra la contradicción documental. T15 lo declara posterior a las auditorías; esta revisión no lo ha reproducido directamente sobre los libros.

**F1 tiene una discrepancia documental.** El hallazgo original ofrece (a) declarar/no usar en esos casos, (b) corregir, (c) juicio caso a caso; `CONTINUIDAD.md` §9.19 abrevia (c) como «excluir». La resolución debe describir la política completa, no solo una letra.

## 4. Aceptación del alcance

**Propuesta:** mantener una matriz con columnas «implementado», «probado», «recorrido real», «validado económicamente» y «permitido para este uso». Sin porcentaje global.

- **B:** cerrar el tercer caso real B y la revisión económica de P-M1, k = 3, protocolo/materialidad del objetivo y variación de agentes. Dos casos ya recorridos no bastan para declarar validación general.
- **A:** F1 y validación propia; no hereda la evidencia de B. Si el alcance de A se excluye explícitamente, la entrega puede aceptarse como alcance reducido; el alcance original seguirá incompleto.
- **C:** recorrido real y validación propia; no hereda la de A/B.
- **Entrada por instrucciones:** prueba dirigida con instrucciones ambiguas, datos ausentes, correcciones y trazabilidad; comportamiento de abstención cuando falta información. No basta con que Elis haya usado prompts.
- **Continuidad/publicación:** relevo vigente y auditor separado; publicación real supervisada solo si el encargo la autoriza, con retirada/recuperación comprobadas. No simular esa evidencia ejecutando una publicación no autorizada.
- **I19/I20 y U2–U5:** exigir casos positivos y negativos sobre una instantánea congelada, con regresión pertinente y revisión de lo cambiado; luego regenerar material afectado. Esta revisión no evalúa la implementación viva.
- **H-P1/X2:** enlazar T15 §6–§7 con la reproducción en libros originales y la corrección documentada de los tres expedientes nuevos; aceptar contra esos casos. No asociarlo por coincidencia a otros «X2» históricos.

## 5. Frentes paralelos que pueden adelantarse ahora

**Propuesta de reparto:** Claude mantiene el frente de producto y su único integrador. Los frentes independientes escriben expedientes de evidencia separados; no ejecutan pipelines contra el árbol vivo ni regeneran referencias. Usan solo B414/B415 congelados e identifican toda dependencia posterior.

| Frente | Trabajo útil ahora | Entregable revisable | Dependencia para integrarlo |
|---|---|---|---|
| **Fuentes y alcance por empresa** | Inventario de archivos ya conservados; versión, origen, SHA-256, períodos, páginas y conceptos; mapa de huecos materiales. Conciliar F15 con los bytes realmente accesibles: «registrado» no equivale a «recibido». Revisar fecha de la rf en Bundesbank y necesidad de OCR del PDF 2021. En Ahold, confirmar Excel/respuesta y documentos, sin suponer que el .bat se ejecutó. En C, criterios de selección y fuentes públicas candidatas. | Tabla por empresa con «registrado sin bytes / conservado sin examinar / conservado y examinado / ausente», celdas afectadas y qué falta. | Ninguna para inventariar. Para sellar y regenerar, esperar contrato/código final de entradas. |
| **Fundamento económico y decisiones** | Reconciliar pendientes con decisiones ya registradas. Preparar D2 → D1 → D7 y configuraciones con opciones, evidencia, efectos ya calculados, incertidumbre, consecuencias y qué necesita decisión humana. Revisar capex/perímetro/NIIF 16 y F1 en papel, sin tocar plantilla. | Dossier de decisiones con cada afirmación marcada como dato, inferencia, convención o propuesta; ninguna casilla humana rellenada por la IA. | Decisiones explícitas para adoptar política; réplica y código final para cambiar el producto. |
| **Protocolo fuera de muestra** | Fijar selección, corte de información, reglas del modelo y métricas antes de observar resultados. Separar prueba de transferencia, de reproducibilidad y de resultados de inversión. | Protocolo fechado y versionado; lista de casos candidatos y motivo; plantillas de observaciones/errores/exclusiones. | Ninguna para diseñarlo. Para ejecutar, versión cerrada, fuentes y parámetros fijados. |
| **Revisión independiente de la entrega** | Preparar matriz hallazgo → evidencia esperada → prueba positiva/negativa y checklist de P0–P7. Se puede revisar semántica de datos ya conservados con contexto separado. | Plan de aceptación y observaciones, sin modificar código de quien implementa. | Snapshot o commit entregado por Claude para emitir conclusión sobre la corrección y ejecutar pruebas. |

No asignar a dos agentes el mismo archivo, expediente, fuente derivada o referencia. Reservar un directorio por frente y un responsable por artefacto; la coordinación integra una sola vez tras contrastar evidencia. Los revisores no corrigen silenciosamente el material auditado: devuelven el hallazgo al responsable y revisan la nueva versión.

## 6. Protocolo fuera de muestra propuesto

1. **Congelar antes de mirar el resultado:** reglas del motor, parámetros/convenciones adoptados, fecha de corte y criterio de elegibilidad. Publicar internamente el manifiesto del protocolo. Registrar todas las candidatas, incluidas excluidas, motor elegido y motivo, para evitar seleccionar solo resultados favorables.
2. **Separar los objetivos:** un tercer caso B demuestra transferencia a otro negocio; un caso C demuestra una primera aplicación real del motor C. Ninguno es por sí solo un backtest. Para capacidad de inversión hace falta estudiar resultados posteriores o simular una decisión histórica con información disponible entonces.
3. **Controlar información futura:** en cada caso histórico conservar documentos y precio que existían en la fecha de decisión, sin reexpresiones futuras no disponibles entonces, supervivencia selectiva ni ajustes posteriores a la valoración. Si esto no se puede acreditar, etiquetar el caso como retrospectivo exploratorio.
4. **Fijar evaluación antes de resultados:** decisión/abstención, objetivos o rangos, horizonte y reglas de seguimiento; retorno total con dividendos, operaciones societarias, costes e impuestos según el uso, comparador pertinente, caídas y errores de tesis. No fijar números arbitrarios ahora: cada definición requiere fundamento y, si es política, adopción.
5. **Separar roles:** extracción, revisión de fuentes, análisis, réplica y auditoría independientes donde corresponda. Quien conoce el desenlace no ajusta el modelo del caso. Registrar divergencias entre agentes y qué parte del resultado depende de probabilidades.
6. **Conservar fallos:** fuentes insuficientes, abstenciones, errores, casos que no encajan y resultados desfavorables forman parte del registro. Un caso sin dato material no pasa a ser aprobado por obtener una valoración prudente.
7. **Cambios de modelo:** toda corrección genera versión nueva y evaluación nueva claramente identificada; no reescribir el resultado anterior como si se hubiese conocido de antemano.

La suficiencia para un uso real exige decidir qué evidencia respalda ese uso y sus límites. No hay aquí datos para afirmar tasa de acierto, rentabilidad esperada, número suficiente de casos o plazo de finalización.

## 7. Qué diferencia pasar pruebas de apoyar una decisión financiera

Pasar pruebas demuestra comportamiento en los casos definidos y reproducción de unas fórmulas. Revisar fuentes acredita origen y tratamiento de los datos hasta el alcance revisado. Una réplica exacta demuestra concordancia numérica. Ninguno de estos pasos demuestra que el negocio generará los flujos supuestos.

Para apoyar una decisión concreta se necesita además un modelo adecuado a ese negocio, supuestos económicos defendibles y expresamente adoptados cuando son política, incertidumbre material acotada, datos relevantes para la fecha y una revisión externa que conozca esos límites. La decisión debe poder justificarse con el dossier final vigente y las circunstancias de la cartera. La inversión seguirá expuesta a pérdidas, incluso si todo el software funciona.

**Conclusión de esta revisión:** trabajar en paralelo ya es útil en fuentes, fundamento y protocolo. La aceptación de una nueva entrega requiere el material exacto que Claude publique; la de un análisis financiero requiere superar las condiciones del expediente y su uso. El alcance original de Munger V2 no se puede dar por terminado con los hechos actualmente documentados.

