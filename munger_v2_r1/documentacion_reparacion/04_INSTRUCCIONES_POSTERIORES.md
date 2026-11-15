# Instrucciones de la persona responsable del proyecto posteriores al diagnóstico (transcripción literal)

Conversación del 8-nov-2026, hora de Europe/Amsterdam. Aquí se transcriben literalmente los mensajes que fijaron o modificaron el alcance, los criterios y la forma de trabajo, en orden cronológico. Las respuestas de Claude no se incluyen: sus resultados están en los archivos del paquete. El encargo inicial está en `00_ENCARGO_INICIAL_diagnostico.txt`.

---

## 15:04 · Petición operativa
> me pasas esto? : la propuesta de reparación y la clasificación del material

---

## 15:12 · Cierre del contrato de reparación H1–H3
> Cierre del contrato de reparación H1–H3
> El diagnóstico entregado confirma los tres hallazgos y contiene los apartados de archivos afectados y criterios de aceptación. Antes de implementar, se solicita precisar esos dos apartados.
>
> Esta entrega debe limitarse a una tabla de reparación y una lista cerrada de archivos. No requiere repetir el diagnóstico ni modificar todavía el sistema.
> 1. Criterios definitivos de aceptación
> H1 · Comprobación de extracciones
> La tabla debe incluir los once casos existentes:
> - Casos 1, 3 y 7: deben dejar de aceptarse.
> - Casos 8, 9 y 11: deben seguir rechazándose.
> - Caso 10: debe seguir aceptándose.
> - Casos 2, 4, 5 y 6: permanecen fuera del alcance de esta reparación y deben figurar como limitaciones conocidas.
> Deben añadirse dos pruebas:
> - Un cero correctamente respaldado por la fuente.
> - Un cero acompañado de una cita literal auténtica que corresponde a otra partida.
> La mera presencia de una cita en la página no debe permitir presentar el cero como comprobado. Si el control automático no puede distinguir ambos casos con fiabilidad, debe proponerse un tratamiento explícito como pendiente de verificación, conservando el dato original y sin aprobarlo silenciosamente.
>
> Debe especificarse cómo se conservarán los ceros existentes y cómo se revisarán posteriormente los rechazos reales cuando estén disponibles los documentos.
> H2 · Lectura de auditorías
> Se adopta como criterio de esta reparación:
> - Auditoría incompleta, puntos duplicados o formato inválido → REPETIR.
> - Cualquier punto FALLA → REPETIR, aunque el veredicto escrito sea APROBADO.
> - Dieciséis puntos válidos, todos PASA, y un único veredicto correcto → APROBADO.
> Las seis auditorías reales originales deben seguir aceptándose sin modificar su contenido para adaptarlas al lector.
>
> La batería sintética debe conservar sus treinta comprobaciones actuales y obtener 30/30 con el generador de auditorías actualizado. Las nuevas pruebas específicas se añadirán sin eliminar las anteriores.
>
> La documentación y el prompt deben reflejar la misma política que el código. Las observaciones no bloqueantes se expresarán como avisos.
> H3 · Corrección de Aarsleff
> Debe crearse un expediente nuevo conservando intacto el original.
>
> Los criterios deben exigir:
> - Corrección de las afirmaciones erróneas y regeneración de sus derivados.
> - Búsqueda de variantes de la afirmación incorrecta sobre esa serie.
> - Controles de citas, celdas e integridad del Excel aprobados.
> - Comparación anterior/posterior que identifique todos los cambios.
> - Datos históricos, fórmulas, hipótesis numéricas, valoraciones, precios y fechas de análisis conservados.
> - C25 permanece en No.
> Cualquier diferencia técnica inevitable de la regeneración debe distinguirse de un cambio de contenido.
> 2. Lista cerrada de archivos
> Para cada archivo, la entrega debe indicar:
> Archivo	Cambio previsto	Motivo	Prueba que lo valida
>
>
> Deben incluirse código, generadores de pruebas, prompts, documentación y archivos derivados afectados. Los elementos opcionales deben quedar separados del alcance obligatorio.
> 3. Cierre
> La respuesta debe identificar cualquier incompatibilidad concreta entre estos criterios y la implementación actual, junto con una solución mínima propuesta.
>
> No deben añadirse otras mejoras ni iniciarse una extracción masiva. Toda la redacción debe permanecer en tercera persona.

---

## 15:30 · Pregunta operativa
> Pinché en descargar todo. Esto se fue a la carpeta Downloads, ¿no?

---

## 15:35 · Inicio de la reparación H1–H3 (precisiones P1–P4)
> Inicio de la reparación H1–H3
> El contrato permite iniciar la implementación en el orden H2 → H1 → H3, sobre una copia y conservando intactos los originales.
> Antes de implementar las partes afectadas, deben incorporarse estas precisiones:
>
> 1. H1: impedir que los ceros pendientes terminen marcados como «Rellenado y verificado» en Excel o sean aprobados silenciosamente por los controles posteriores. La solución mínima elegida debe contar con una prueba del recorrido completo.
> 2. H1: probar la transición de cero pendiente a confirmado mediante decisión humana registrada, incluyendo fuente, fecha y reconstrucción.
> 3. H3: corregir las rutas del contrato: `observaciones.C25` y `seis_preguntas.que_caja_espero`. `celdas.C25` permanece en `No`.
> 4. Entrega final: producir un ZIP completo, autocontenido y versionado, con instrucciones, registro de cambios, pruebas y pendientes. La persona responsable del proyecto no deberá combinar manualmente parches.
>
> No se solicita otro diagnóstico general ni una nueva entrega exclusivamente documental. Las precisiones deben incorporarse al registro de implementación.
> Cada reparación debe presentar los cambios y sus pruebas. Si aparece una incompatibilidad que impida cumplir un criterio, debe identificarse sin rebajarlo ni declarar terminada esa parte.
> La primera entrega de implementación será H2. Toda la comunicación permanecerá en tercera persona.

---

## 15:48 · Continuación: cierre de H2 e implementación de H1 (autorización de Fable)
> Continuación de la reparación: cierre de H2 e implementación de H1
> La revisión externa de la entrega 1 confirmó que las 28 pruebas rápidas pasan y que los expedientes originales permanecen intactos. La entrega constituye un avance válido, pero H2 necesita una corrección adicional antes de declararse cerrada.
> 1. Cerrar la vía restante de H2
> Sobre una auditoría con dieciséis puntos válidos, todos PASA, y un único `Veredicto: APROBADO`, el lector actual sigue devolviendo APROBADO cuando se añade cualquiera de estos encabezados:
>
> ```
> 17. PENDIENTE · revisión pendiente
> ```
>
>
> ```
> 8. PENDIENTE · hecho material sin comprobar
> ```
>
>
> ```
> 100. PASA · punto fuera del rango
> ```
>
> Deben reproducirse, incorporarse a las pruebas y corregirse para que devuelvan REPETIR.
> El lector debe distinguir los encabezados de comprobación de las cifras legítimas utilizadas en la evidencia. No debe ignorar un encabezado incorrecto simplemente porque su estado o numeración no encajen en el formato válido.
> Deben mantenerse aprobadas las pruebas anteriores, las seis auditorías reales sin modificar y las treinta comprobaciones existentes del pipeline.
> 2. Continuar con H1
> Una vez cerrado H2, debe implementarse H1 según el contrato y las precisiones del registro, incluyendo:
>
> * Comprobación de línea, importe completo y respaldo de ceros.
> * Conservación e inventario de los ceros heredados.
> * Recorrido completo de un cero pendiente desde la extracción hasta Excel y los controles posteriores.
> * Prevención de su etiquetado como «Rellenado y verificado» y de su aprobación silenciosa.
> * Prueba de confirmación mediante decisión humana registrada, sin que la IA invente esa confirmación.
> * Tratamiento coherente de las partidas derivadas que dependan de ceros pendientes.
>
> Si existe una incompatibilidad concreta, debe documentarse y proponerse una solución mínima, sin rebajar los criterios.
> 3. Modelos y esfuerzo
> Queda sustituida la prohibición anterior de utilizar Fable.
> Opus será el modelo principal. Claude podrá seleccionar Fable cuando una cuestión concreta requiera mayor profundidad, considerando dificultad, consecuencias y coste, sin solicitar autorización adicional para cada uso.
> El motivo y el resultado de cada uso deberán registrarse brevemente. Una vez resuelta la cuestión, el trabajo continuará con el modelo adecuado. El procedimiento completo no debe ejecutarse en Fable por defecto.
> 4. Entrega
> La próxima entrega contendrá H2 cerrada y H1 implementada, o sus bloqueos concretos si alguno impide terminar.
> Debe incluir un ZIP completo y autocontenido, registro de cambios, pruebas y pendientes. Los originales permanecerán intactos. H3 seguirá identificada como pendiente hasta su ejecución posterior.
> No se solicita otro diagnóstico general ni una entrega exclusivamente documental. Toda la comunicación permanecerá en tercera persona.

---

## 16:26 · Cierre de H1 y continuación con H3
> Cierre de H1 y continuación con H3
> La revisión externa reprodujo las 82 comprobaciones aprobadas de la entrega 2 y considera H2 cerrada para su alcance contratado.
> H1 requiere corregir la actualización de evidencias cuando existen datos o estados anteriores.
> 1. Reproducir y corregir los casos pendientes
> Caso A: libro previamente rellenado.
> Al aplicar una Historia con ceros pendientes sobre un libro cuyas filas estaban verificadas, pueden conservarse las etiquetas «Rellenado y verificado». Debe comprobarse con y sin `--sobrescribir`.
> Caso B: media previamente presente.
> Si `fase1_metadatos.json → analisis.C50` ya contiene una media de SBC procedente de la misma Historia y ventana temporal, `construir` no le propaga el pendiente. Debe probarse conservando C50 en los metadatos, sin eliminarla para preparar la prueba.
> Caso C: confirmación posterior.
> Tras registrar decisiones humanas válidas y reconstruir la Historia sin esos pendientes, la actualización de un libro previamente pendiente puede conservar las marcas antiguas.
> Las ubicaciones relevantes son:
>
> * `fase1_historia.py`: propagación de pendientes a C46–C50 dentro de la condición que crea entradas ausentes.
> * `rellenar_fase1_v63.py`: salida anticipada de `poner` cuando existe valor y salto de filas de Control maestro cuando existe estado.
>
> 2. Criterios de aceptación
>
> * Un dato dependiente de un cero pendiente no conserva una etiqueta de verificado por estar previamente rellenado.
> * La incertidumbre se propaga a las medias existentes que dependan de esa misma Historia.
> * Una fuente verdaderamente independiente no se considera validada por su mera declaración: cualquier excepción requiere respaldo explícito y trazable.
> * Tras una confirmación válida, se actualizan únicamente las evidencias afectadas; otros pendientes permanecen.
> * Los cambios de estado no modifican silenciosamente los valores.
> * Si determinada reutilización del libro no está soportada, debe rechazarse expresamente y exigir una regeneración segura. No puede aparentar una actualización correcta conservando etiquetas obsoletas.
> * Se mantienen las 82 comprobaciones anteriores y las treinta del pipeline. Los nuevos casos se añaden.
>
> No se solicita otra entrega exclusivamente documental.
> 3. Continuación con H3
> Una vez superados esos criterios y las pruebas de regresión, podrá ejecutarse H3 conforme al contrato: expediente nuevo de Aarsleff, correcciones en las rutas ya identificadas, auditoría nueva y comparación completa que demuestre la conservación de cifras, fórmulas, hipótesis y fechas.
> Si H1 queda bloqueada, debe declararse el bloqueo sin presentar la reparación completa como terminada.
> 4. Modelos y entrega
> Se mantiene la autorización de uso selectivo de Fable cuando Claude lo considere justificado por dificultad, consecuencias y coste, registrando motivo y resultado. Opus continúa como modelo principal.
> La entrega será un ZIP completo, autocontenido y versionado, con registro, pruebas y pendientes, conservando intactos los originales. Toda la comunicación permanecerá en tercera persona.

---

## 17:03 · Continuidad
> muy importante: La calidad de esta revision no dependerá cada vez de recordar conversaciones largas y más de un expediente verificable no? Alucinaciones? ¿Podemos continuar en esta ventana o es necesario crear una especie de archivo de continuidad? ¿Entiendes a lo que me refiero o no?

## 17:04 · Encargo de la entrega 3.1
> Perfecto, perfecto. Prepara el archivo entonces, prepara todo lo que sea necesario, cosa de que yo abra una ventana, suba lo que tenga que subir y pueda continuar desde ahí. ¿Mm? Y asegúrate de que todo esté 100% correcto. No puede haber ninguna omisión ni errores. ¿Puedes hacerlo?
