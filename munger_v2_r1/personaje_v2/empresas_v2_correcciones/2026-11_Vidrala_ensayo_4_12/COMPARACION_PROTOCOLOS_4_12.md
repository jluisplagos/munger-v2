# Vidrala · los dos protocolos experimentales del objetivo sobre el mismo material (encargo 4.12 §7)

**Qué es.** La lectura de la comparación entre `cierre_condicionado/Vidrala` (protocolo «objetivo_condicionado») y su copia identificada `cierre_bloqueo/Vidrala` (protocolo «bloqueo_del_objetivo»). Los datos lado a lado están en `resultados/comparacion_protocolos.md`, que genera `scripts/comparar_protocolos.py` (solo lee). **Ninguno de los dos protocolos está adoptado**: comparar no es elegir. La elección es la decisión D412-PROTOCOLO de la propuesta humana, sin firmar.

**Jerga.** El *precio de Sí* es el precio por debajo del cual el personaje compraría. El *valor calculado condicional* es lo que da el libro con hipótesis no adoptadas. El *precio objetivo emitido* es el que la salida presenta como objetivo. El *ámbito calculado* son las variantes que se calcularon de verdad (15 en Vidrala); el *rango calculado* es la dispersión del precio de Sí en ellas, no un intervalo de confianza.

## 1. Hechos comprobados

**Las dos copias tienen el mismo material económico** (`resultados/comparacion_protocolos.md`):
- celdas de la configuración, `precio.json` y entradas económicas de las variantes, iguales;
- `datos_ausentes.json`, idéntico byte a byte: el protocolo de bloqueo no añade ningún dato ausente.

**Ninguna aprobación se copió entre ellas.**
- La copia retiró en su primera llamada la aprobación que traía del original (`cierre_bloqueo/Vidrala/historial_cierres/01_47e1c83dc70a3d86`).
- Cada una tiene su solicitud (SA-2427fb9cd6e753fe y SA-8da4a78afc939a43), su material (5025f54d0c143062 y f7a0ba07431707e3) y su auditoría, hecha por un agente distinto que no vio el trabajo. Las dos auditorías dan APROBADO.
- Las dos se regeneraron desde el paso 13 con el código final y se auditaron de nuevo. Las aprobaciones anteriores no se consumieron o quedaron archivadas (`REGISTRO_AVANCE_4_12.md`, §7).
- Restos del original en la copia que no dan vigencia a nada (revisión interna R12): `configuracion_v64_variantes.json` es el del original (variantes reutilizadas; su campo `configuracion_economica_sha256` es la huella de la configuración del original, y el pipeline compara la huella económica, que coincide), `entrada_v63.json` y los resultados de las variantes guardan rutas del original, y `publicaciones_resumen.json` comparte `registro_id` con él, con las entradas reubicadas a la copia.

**La fase C de la copia** la hizo un agente nuevo (Opus, esfuerzo alto) con la del original como referencia. Según su sección «Cambios frente a la fase C del cierre condicionado», solo cambia lo que depende del protocolo: el bloque `configuracion_v64.objetivo` y algunas redacciones. No cambia ninguna palanca, ni la materialidad de los parámetros, ni la lista D10 (vacía), ni el cubo, ni la conclusión provisional («esperar»).

| | «objetivo_condicionado» | «bloqueo_del_objetivo» |
|---|---|---|
| Estado · auditoría | concluido · APROBADO | pendiente_de_datos · APROBADO |
| Cubo · acción | Vigilar · esperar | Vigilar · ninguna |
| Tratamiento del objetivo | `objetivo_condicionado` (emitido, condicionado) | `objetivo_bloqueado` (origen: protocolo de bloqueo) |
| Valor calculado condicional | 56,01809018887024 € | 56,01809018887024 € |
| Precio objetivo emitido | 56,02 €, marcado como provisional | ninguno |
| Hipótesis que lo condicionan | PM1.estructura, PM1.familia, PM1.parametro | las mismas |
| Rango calculado del precio de Sí | 51,29–65,72 € en la activa y 14 escenarios (las 15 variantes), todos «caro»; la familia de P-M1 no queda cubierta por ese ámbito (ninguna variante calcula Θ) | el mismo |
| Diagnóstico | — | falta de datos: el objetivo depende de P-M1; se continuaría desde el paso 8 con información nueva (el desglose del capex por destino) |
| Aptitud de uso (ficha, informe §1, resumen) | experimental | experimental |

## 2. Qué hace cada protocolo con el mismo material (interpretación)

**Lo que comparten.** El material económico es el mismo: libros, palancas, variantes, `precio.json` y la evaluación de cada parámetro por la fase C. Los dos dicen lo mismo de la valoración:
- el precio (90,10 €) está por encima del precio de Sí en las 15 variantes calculadas;
- el precio de Sí depende de tres hipótesis sin fundamento suficiente: la estructura, la familia y el parámetro de P-M1, es decir, cuánta inversión hace falta para reponer los hornos por encima de la amortización;
- falta el desglose del capex por destino, que Vidrala no publica.

**Dónde se separan.** Solo en lo que se emite.

- **«objetivo_condicionado»** emite la acción que el ámbito calculado sostiene («esperar», cubo Vigilar, estado concluido). Da el precio de Sí como precio objetivo, marcado como condicionado y provisional, con sus hipótesis, el rango (51,29–65,72 € en la activa y 14 escenarios) y la naturaleza de ese rango.
- **«bloqueo_del_objetivo»** trata la información que falta como un bloqueo. No emite acción ni objetivo (estado pendiente_de_datos, cubo Vigilar), y el diagnóstico dice qué información falta. El valor calculado condicional (56,02 €) aparece solo como tal, no como objetivo.

## 3. Contradicciones y riesgos de cada uno (interpretación)

### «objetivo_condicionado»

1. **Una cifra que parece más firme de lo que es.** El objetivo condicionado es una sola cifra (56,02 €), pero su nivel depende de hipótesis no observadas: con las mismas palancas, el precio de Sí va de 51,29 a 65,72 €. La marca «condicionado, provisional», la lista de hipótesis y el rango están en la ficha, en la línea de estado y en la sección 14. Aun así, un lector apresurado puede tomar la cifra como objetivo.
2. **Robustez que solo vale dentro de lo calculado.** «La acción se sostiene en el ámbito» quiere decir que ninguna de las 15 variantes cambia la zona. No cubre hipótesis no exploradas, como otros márgenes, probabilidades, r o palancas de la fase B. El protocolo lo declara, pero el estado «concluido» puede leerse como más completo de lo que es.
3. **Tensión con el ideal de no dar cifras sin fundamento.** El objetivo se emite aunque sus condicionantes no tienen fundamento suficiente. La regla D10 lo permite marcándolo como provisional; S-19, en cambio, bloquea cuando falta un dato material. El protocolo se apoya en que una hipótesis incierta no es un dato ausente (encargo §4).

### «bloqueo_del_objetivo»

1. **Bloquea una acción que el ámbito sí sostiene.** Con el precio un 37 % por encima del mayor precio de Sí calculado, «esperar» se sostiene en todo el ámbito. El bloqueo deja el expediente sin acción y sin objetivo y pierde esa información útil.
2. **Puede no tener salida.** «Pendiente de datos» apunta a un desglose del capex que Vidrala no publica. Si nunca se publica, el expediente queda bloqueado indefinidamente aunque la conclusión de precio no dependa de él.
3. **Acerca una hipótesis a un dato ausente.** Trata la falta de fundamento de una hipótesis de modelo (P-M1) como S-19 trata un dato ausente material. El encargo pide que una hipótesis incierta no se convierta automáticamente en un dato ausente. El protocolo no lo hace en las listas (`datos_ausentes.json` no cambia), pero el estado resultante es el mismo que el de S-19.

### Los dos

- Ninguno corrige la valoración ni elige la estructura de P-M1: cambian la presentación, no la cifra.
- Ninguno convierte el expediente en apto para decidir con dinero real. La aptitud de uso de las dos salidas es «experimental».
- Sin protocolo declarado, el pipeline no emite objetivo oficial (`objetivo_sin_protocolo`). Lo prueba la batería, grupo F.

## 4. Qué decide la persona responsable (no se decide aquí)

D412-PROTOCOLO de la propuesta humana: qué protocolo rige cuando hipótesis sin fundamento condicionan el objetivo. Hay una recomendación argumentada y alternativas, sin firmar. Mientras no se decida, cada expediente experimental declara el suyo.
