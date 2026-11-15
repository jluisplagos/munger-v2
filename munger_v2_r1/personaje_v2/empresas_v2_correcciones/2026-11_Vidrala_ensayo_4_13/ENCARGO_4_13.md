# Munger V2 — Encargo 4.13
# Cierre de brechas de fiabilidad del motor B y conciliación económica de los dos casos

## 1. Resultado, alcance y autoridad

Se ejecutará este encargo completo sobre la entrega 4.12.

El objetivo es resolver las incidencias concretas que la revisión externa encontró antes de ampliar el sistema al motor A.

El producto final debe poder apoyar decisiones que comprometen dinero real mediante evidencia, cálculo reproducible, razonamiento económico defendible y capacidad de abstenerse. Esta entrega no se declarará apta para ese uso por superar pruebas técnicas.

El alcance queda limitado al motor B y a los expedientes existentes de Vidrala y Viscofan:

- Vigencia.
- Coherencia de la decisión y del objetivo.
- Cobertura de hipótesis.
- Acciones y evidencia activa.
- Conciliación de inversión, amortización y arrendamientos.

No se incorpora otra empresa ni el motor A. No se rehacen diez años de extracción ni se inicia un backtest general. No se actualizarán cotizaciones para aparentar una valoración actual.

Se autoriza reparar código y contratos, contrastar fuentes públicas, construir variantes experimentales necesarias y reabrir las fases afectadas.

Las decisiones técnicas se resolverán durante el trabajo. No se rellenarán firmas humanas ni se adoptarán automáticamente hipótesis o políticas pendientes.

Los ensayos supervisados ya están autorizados: no se pedirá otra aprobación para realizarlos.

Este encargo sustituye los antiguos arranques de «verificar y esperar». Comunicación en español claro y tercera persona.

No se contactará con empresas ni se enviarán preguntas a terceros externos. No hace falta recibir archivos auxiliares de ChatGPT.

## 2. Base, ventana y conservación

Puede continuarse en la ventana que entregó la 4.12 si conserva el árbol y su contexto.

Si hace falta otra, se adjuntará la base y este prompt directamente, sin ejecutar antes el antiguo arranque.

Base:
munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip

SHA-256:
615d7dd93d1f981ae83fd8b606c7893304714414a21bf33715156c6117006f88

Tamaño: 408.223.286 bytes.
Partes: parte00 a parte19.
Manifiesto: 3.796 archivos, además del propio manifiesto.

Se comprobarán huella, CRC, VERSION y manifiesto. Desarrollo y pruebas en copias.

Los originales, los expedientes previos y las plantillas y referencias ya entregadas conservarán sus bytes.

Se permiten los cambios necesarios en código, esquemas, inventarios y documentación.

Una modificación de fórmulas exige una plantilla y referencia nuevas, identificadas como experimentales, selección explícita y compatibilidad con las anteriores.

La revisión externa confirmó:

- Integridad y preservación.
- Control 4.12: 63/63.
- Grupos A/E/F/G de integración: 78/78.
- Réplica matemática propia: 31 libros y 3.844 filas, sin discrepancias, con máximo de 7,11e-13 €/acción.
- Las 3.796 huellas del manifiesto intactas después de las comprobaciones externas.

Reprodujo además las incidencias siguientes, no cubiertas por esos casos.

No reejecutó toda la verificación general ni todos los controles históricos. Los resultados conservados se distinguirán de lo realmente reejecutado externamente.

No se repetirá toda la tanda histórica antes de empezar ni en cada edición.

## 3. JSON estructuralmente incorrecto: retirar la aprobación antes del fallo

La 4.12 corrige λ=0,9, ausencias y JSON sintácticamente roto.

Pero quedan nueve primeras llamadas de los probes externos con material alterado que conservan:

- concluido/APROBADO;
- ficha cerrada;
- cierre registrado;
- CSV aprobado.

Se produce AttributeError antes de la vigencia.

Reproducciones sobre copias independientes del piloto 4.11, inicialmente vigente, con publicaciones redirigidas a las copias:

- configuracion_economica.json = null o []: fallan pipeline y ficha;
- dentro de una configuración económica, N1 = []: fallan pipeline y ficha;
- plantilla_activa.json = null: falla pipeline;
- plantilla_activa.json = []: fallan pipeline y ficha.

Se corregirá el patrón:

- Validación estructural explícita antes de usar .get.
- Una guarda de vigencia que no dependa de interpretar correctamente el archivo alterado.

No bastará capturar esos ejemplos de manera aislada.

Los errores devolverán motivo y estado de recuperación, sin dejar aprobaciones actuales que ya no correspondan al material.

Se ensayarán tipos nulo, lista, escalar y estructuras anidadas incorrectas en las entradas y archivos de control afectados.

En cada vía —pipeline, ficha, informe y resumen— se probará la PRIMERA llamada sobre su propia copia.

Se conservarán antecedentes y retirada de todos los destinos publicados. Si uno no es actualizable, retirada pendiente visible y sin continuar como aprobado.

Material intacto y llamada con configuración externa equivocada seguirá rechazándose sin modificar el expediente.

No se reescribirán huellas o selecciones para legitimarlas antes de la comprobación.

Los destinos de prueba permanecerán aislados de los originales.

## 4. Acción provisional y final: impedir el salto del protocolo

Incidencia externa demostrada en esquema y validadores, sin atribuirle un cierre oficial completo:

1. Partir de la fase C real de cierre_condicionado/Vidrala.
2. Conservar decisión final concluido/esperar/objetivo 56,02.
3. Quitar protocolo_objetivo o declarar bloqueo_del_objetivo.
4. Cambiar conclusion_provisional a descartar o comprar y actualizar el bloque de objetivo con el propio evaluador.
5. Esquema y coherencias aceptan. El bloque estructurado dice no aplicable/no emitido mientras decision.precio_objetivo conserva 56,02.

OBJ.tratamiento prioriza conclusion_provisional y omite controles de la decisión final.

Se corregirá la semántica de la evaluación y se cruzarán:

- Acción final.
- Estado.
- Protocolo.
- Objetivo estructurado.
- Objetivo de la decisión.

La coherencia se mantendrá también en ficha, informe y resumen.

No se impondrá igualdad universal entre conclusión provisional y final: una transición legítima debe seguir siendo posible.

El antecedente provisional no puede eximir la salida final de sus reglas.

Se preservarán S-19 y D10, las compras sin objetivo de espera y los objetivos bloqueados con acción nula.

Se respetará el redondeo declarado de las salidas.

Se reproducirá el contraejemplo y se verificará también de extremo a extremo en expedientes sintéticos:

- Ninguna contradicción podrá alcanzar un cierre oficial.
- Ninguna contradicción podrá generar material aparentemente listo para auditoría.

No se usarán agentes sintéticos en los casos financieros reales.

## 5. Cobertura por hipótesis y fundamento económico

RA4 y R5 de la revisión interna siguen pendientes.

En Vidrala, PM1.familia aparece no cubierta, pero no material para la acción. El contrato no representa correctamente lo no determinado.

Se distinguirán:

- Contraste aislado.
- Variación conjunta.
- Variación conjunta necesaria por el dominio.
- Juicio económico.
- Ausencia de cobertura.

Quitar toda P-M1 no demuestra el efecto aislado de su familia.

Una alternativa ligada como SR2 no debe quedar automáticamente sin cobertura por cambiar dos campos necesariamente vinculados.

Cuando no haya contraste o evidencia suficiente para atribuir materialidad, se representará como no determinada, sin convertirlo en falso.

Un juicio económico explícito se identificará como juicio, con su evidencia. No se presentará como una constatación calculada.

La invariancia de la acción en las variantes efectivamente calculadas se distinguirá de la materialidad de un parámetro no identificado.

El rango seguirá siendo una sensibilidad condicional, no una banda completa de incertidumbre ni un intervalo de confianza.

No se inventará un umbral para decidir fundamento suficiente ni se enviará automáticamente toda hipótesis a D10.

Sí se exigirá:

- Evaluar todos los parámetros activos.
- Citar evidencia pertinente.
- Separar hechos e inferencias.
- Revisar contradicciones.

Las reparaciones de coherencia no se devolverán a una aprobación humana rutinaria.

Los avisos de dominio se calcularán para las variantes, no solo para la activa.

Se agruparán para que la revisión sea legible, indicando cuáles afectan al caso y a qué conclusión.

Se conservarán los dos protocolos como ensayos no adoptados, sin favorecer uno por emitir un precio.

## 6. Viscofan: acciones, fuente de EPS y evidencia activa

Fuente conservada:
viscofan/fuentes/pdf/AR_2025.pdf

SHA-256:
e997bc7d07392b5d50226a9ad18839897c9e705c46a81d8acbc51174f638b83c

PDF 119, página impresa 99, nota 20:

En 2025 figuran:

- Media básica: 45.656.226; EPS 3,50.
- Media denominada diluida: 45.479.209; EPS 3,52.
- Mismo numerador: 159.917 miles.

La nota no explica esa inversión. El modelo utiliza 45,479209 millones.

Que el número esté en la página no resuelve su concepto ni la contradicción.

Otros datos de la misma publicación:

- PDF 76, página impresa 56: emitidas 46.500.000 a 31-dic-2025.
- PDF 83, página impresa 63: propias 506.601.
- Circulación de cierre de 2025: 45.993.399.

No se sustituirá N automáticamente por ese stock.

Promedio de EPS, stock con derecho al valor y dilución potencial son conceptos distintos.

El precio del caso es 54,70 de 3-nov-2026.

Se conciliarán definiciones, fechas, unidades y operaciones de capital, consultando otra fuente oficial o edición cuando sea posible.

Si no se resuelve una contradicción de la fuente, se declarará y se compararán alternativas identificadas, sin elegir por el valor obtenido ni presentar una cifra incierta como dato definitivo.

La sensibilidad externa a N=45,993399 da:

- Precio de Sí 38,84848 con E/r_op fijos.
- Aproximadamente 38,79687 recalculando E=54,70×N.
- Frente a 39,28770 del caso activo.

Son sensibilidades de definición con fechas mezcladas, no correcciones adoptadas ni valoraciones actualizadas.

Se limpiará la evidencia activa que contradice las entradas de Viscofan:

- fase1_metadatos.
- fase1_v63.
- Control maestro.
- Fuentes y notas que puedan regenerar textos antiguos.

Se conservarán los antecedentes y se corregirá la vía generativa con un mapeo o extracción selectiva.

No se rehacen diez años.

El contraste deberá demostrar concepto, columna, período, signo y unidad, además de encontrar dígitos en una página.

Se mantendrán separadas la reproducción histórica y cualquier alternativa con entradas corregidas.

## 7. Arrendamientos y mantenimiento: conciliación completa y versionada

La sensibilidad ROU de la 4.12 es parcial: cambia el exceso B60 sin conciliar todas las bases de reinversión y sus efectos.

La depreciación ROU 2021–2025 de Viscofan suma 27,051 M€.

No basta el método de θ equivalente sobre la base anterior.

Se definirá explícitamente el perímetro de inversión y amortización.

Se conciliarán:

- Capex de caja.
- Altas ROU.
- Depreciación de activos propios y arrendados.
- Pagos.
- Tratamiento del pasivo.
- Posibles dobles cómputos en el puente y los flujos.

No se presumirá que restar depreciación ROU de dos bases sea por sí solo la solución.

La alternativa deberá ser contablemente y económicamente coherente y propagarse a:

- D_hist.
- F_hist.
- Rh.
- f/f_fija.
- S2C.
- Requisito anual.
- Terminal.

Se ajustará todo lo que corresponda según su definición.

Se conservarán las series publicadas. Los ajustes tendrán entradas y derivaciones separadas.

Si la representación exige modificar fórmulas protegidas, se creará una plantilla y referencia experimental nueva y se conectará a la selección y al pipeline.

No se editará la referencia antigua para hacerla pasar.

Se conservará el legado como control y se compararán las alternativas con las mismas restantes entradas.

Se comprobarán:

- Ambos extremos θ=0 y θ=1.
- El punto de cálculo θ=0,5.
- Los dominios de las estructuras pertinentes.

Una combinación no definida se identificará sin recortar parámetros para lograr un valor.

No se trasladará una cota numérica de la base antigua a otra base como si fuera evidencia económica.

Habrá conciliación anual y terminal y réplica independiente.

Si faltan datos para elegir la representación, se entregarán las alternativas condicionadas y la carencia precisa. Ninguna será adoptada por defecto.

La comparación no podrá limitarse a otra calculadora auxiliar si se declara resuelta la integración del modelo.

## 8. Corregir interpretaciones económicas de Vidrala

Se corregirán estas explicaciones, conservando el historial y sin cambiar automáticamente los parámetros para hacerlas coincidir:

### Q-ROIC1

PRECISION_ROIC_4_9.md define neto de reposición como inversión que excede mantenimiento, asociado a SR1.

La inversión total contaminada por mantenimiento requiere reestimación.

REVISION_ECONOMICA_VIDRALA_4_12.md invierte la condición al justificar SR2.

Se recuperará la definición original y se explicará qué mide cada ROIC, sin elegir otra estructura por autoridad o por valor.

### ROIC y tasa de descuento

ROIC terminal 9%=r personal 9% no demuestra neutralidad del crecimiento en motor B, que descuenta a r_op 8,689151674%.

Tampoco se sustituirá por la conclusión simplista contraria: P-M1 introduce inversión adicional.

r personal permanece en 9% y r_op seguirá calculándose con las entradas.

### Inferencia contra H

Capex mayor que D&A sin crecimiento no excluye H:

- Con inversión fija para crecer=0, su crédito=min(req,0)=0.
- Por tanto, paga todo el requisito.

Ese hecho no selecciona por sí solo SR1.

La comparación SR1/SRF requiere explicitar la mezcla histórica y futura de fijo/circulante, sin confundir porcentajes con denominadores distintos.

Se revisarán las justificaciones activas que dependan de esas inferencias.

Una corrección de texto no obliga a cambiar una palanca, pero si su fundamento deja de sostenerse se revisará el juicio y se mostrará su efecto separado.

Ninguna elección pendiente se considerará firmada.

## 9. Ejecución, pruebas y entrega

Se trabajará por hitos:

1. Guardas y coherencia.
2. Conciliación de fuentes y bases.
3. Variantes económicas.
4. Regeneración de lo afectado.
5. Revisión y empaquetado.

Se conservarán registros que permitan reanudar sin esperas indefinidas.

No se declarará trabajo en segundo plano si no hay ejecución o agentes activos verificables.

Se reutilizarán fuentes y fases válidas.

Se reabrirán únicamente las afectadas conforme a dependencias, sin entregar una aprobación vieja para material nuevo.

Las auditorías financieras serán de agentes reales en contexto separado.

Si una corrección posterior cambia el material revisado, se revisará de nuevo lo afectado.

### Pruebas necesarias

- Primeras llamadas de las cuatro vías con tipos JSON erróneos.
- Material intacto y selección equivocada.
- Retiradas pendientes.
- Contradicciones provisional/final/objetivo y transiciones legítimas.
- Cobertura no determinada y parámetros vinculados.
- D10 y S-19.
- Fuentes y unidades.
- Controles heredados.
- Alternativas ROU completas y extremos.
- Integridad de fórmulas.
- Vigencia ante cambios económicos.

No se editará código mientras corra una batería.

LibreOffice y pipelines que lo utilizan irán siempre en secuencia.

Después de las pruebas dirigidas y la revisión interna, se hará una ronda general completa sobre la extracción final limpia, con los controles históricos afectados y las diferencias esperadas justificadas.

No se cambiarán referencias para ocultar regresiones.

Se comprobará el ZIP con dos lectores y se verificará el manifiesto después de todo.

### Entregables

Se entregarán:

- Código y esquemas.
- Plantilla y referencia nuevas, si procede.
- Fuentes y conciliaciones selectivas.
- Comparaciones homogéneas.
- Expedientes finales con estados y auditorías acordes al material.
- Réplica y pruebas.
- Guía de uso actualizada.
- Informe y registros.
- VERSION, CONTINUIDAD, arranque y manifiesto.

El informe separará:

- Integridad técnica.
- Reproducción numérica.
- Fundamento económico.
- Aptitud de uso.

Para cada hallazgo externo dirá resuelto, pendiente o no reproducido, con evidencia y consecuencia.

Ningún APROBADO ni porcentaje de avance acreditará por sí solo aptitud para decisiones con dinero real.

Las decisiones pendientes se agruparán en:

1. Política de salida.
2. Elecciones económicas por empresa.
3. Ampliaciones futuras.

Cada una tendrá recomendación, alternativas, evidencia y efectos; firmas vacías.

No se pedirán de nuevo autorizaciones para el uso experimental o las reparaciones técnicas ya concedidas.

Entrega:

munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip

Con SHA-256, PARTES y fragmentos de hasta 20 MiB, más registro externo de verificación.

No se publicará ni se desplegará el producto.

El mensaje final indicará:

- Lo realmente implementado y ejecutado.
- Incidencias pendientes.
- Aptitud de uso.
- Próximo paso antes del motor A.
- Porcentaje orientativo actualizado con hitos.

Punto de partida: aproximadamente 75% hacia una primera versión integrada supervisada.

No mide seguridad inversora, tiempo restante ni probabilidad de rentabilidad.