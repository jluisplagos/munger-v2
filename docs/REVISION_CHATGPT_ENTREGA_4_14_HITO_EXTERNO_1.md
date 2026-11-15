# Revisión externa 4.14: primer hito técnico y numérico

Estado: revisión parcial independiente; no aceptación del producto ni verificación del ZIP completo.

## Identidad de los archivos

Nueve partes recibidas: 00,02,21,29,32,33,45,50,53. Todas coinciden con SHA-256 y tamaño de PARTES. Se leyó el directorio central: 7462 miembros, incluidos 6799 archivos. El manifiesto tiene 6798 entradas y se excluye a sí mismo.

Se extrajeron 1618 archivos completos verificando CRC y SHA del manifiesto. Con archivos idénticos de la base 4.13 y deduplicación por SHA-256 se han podido reconstruir 6021 de las 6798 entradas. No se ha comprobado la huella ni el CRC de todos los miembros del ZIP completo. El fichero sparse se llama PARCIAL y no se usa como entrega.

## Pruebas ejecutadas aquí

- Verificación de entradas: 33/33.
- Juicio sobre el objetivo: 27/27.
- H5: 59/59.
- Réplica propia B: 8 libros disponibles, 992 filas; ninguna discrepancia relevante; máximo absoluto por acción 1.009e-12. Valores principales: Vidrala 56.0020051682 y Viscofan 39.7981935351.
- Réplica propia A: reconstrucción de f desde Historia y ancla de FCF desde Análisis; 124 filas; ninguna discrepancia relevante. Elis 7.3020553231. Reproduce el modelo existente, no valida su fundamento ni una corrección F1.
- Registros finales de Vidrala y Viscofan: comprobar() devuelve apto por entradas, 226/226 y 232/232 respectivamente. Sus 11 y 10 archivos fuente están disponibles y coinciden con las huellas registradas. Verificación adicional independiente de existencia de páginas: 241 y 229 referencias publicadas/auxiliares, ninguna página inexistente.
- Fuentes de Elis: PDF URD 2025 recibido y cotejo directo de páginas 327 y 350; constan amortización ROU 149.5, amortización de intangibles de adquisiciones 85.7 y pagos por arrendamientos incluyendo intereses 177.9. Faltan nueve textos para ejecutar el control completo de su registro. Todos están en parte36.

## Defectos nuevos reproducidos del verificador de entradas

Se utilizó una copia de prueba sintética completa, expresamente identificada, construida con el fixture de la batería 4.14. El control positivo es apto. Los siguientes cambios aislados también devuelven apto sin errores ni discrepancias:

1. R414-PAGINA: cambiar la página del dato publicado Historia!F6 a 999999. La fuente existe, pero esa página no. _texto_pagina devuelve None y se omite el contraste. Debe quedar pendiente/discrepancia, no apta como contrastada.
2. R414-FUENTE: cambiar el archivo declarado a fuentes_sinteticas/NO_EXISTE.txt y sha256 a None. Se omite el contraste al no existir la ruta y se acepta la declaración del revisor. Debe distinguir fuente local conservada de fuente externa no conservada y no acreditar automáticamente una comprobación documental reproducible cuando desaparece la fuente local. Los datos publicados de los tres registros finales sí tienen archivo y huella: no se afirma que exploten este caso.
3. R414-CIFRA: valor fuente 45479.209, cita y página real con 45479; incluso ligando la fuente modificada por SHA, se da por apta. _cifras genera representaciones redondeadas a 0–6 decimales y _cita_contiene acepta valores diferentes. Ejemplos directos adicionales: 149.5 aceptado con cita150; .49 aceptado con cita0. Deben admitirse formatos equivalentes y ceros finales, no redondeos que cambian el valor declarado sin transformación explícita.

Evidencia: revision414_sondas_entradas.py y .json; revision414_sonda_citas_redondeadas.json. Son fallos del control reproducidos en fixtures sintéticos, no demostración de que las cifras de los expedientes finales sean erróneas.

## Incidencias del autor contrastadas parcialmente

I12: leído el libro de Elis y fase1_v63.json, confirmada discrepancia C48=108 en Excel versus82.933 en origen; el libro incluye intereses de arrendamientos. Falta asegurar una reconstrucción que preserve la entrada económica efectiva y su derivación.
I13: leído código; la vigencia del valor no liga por sí sola la vigencia del fundamento.
I8/I9: exclusión de cifras descriptivas usadas en juicio y recuento incorrecto conservado en informe final, declarados por el autor.
I19/I20: relevo caducado y falta de estado de aptitud en salida V6.3, declarados y coherentes con lectura de código.
F1: no se declara aquí validada la corrección económica. Se han reproducido fórmulas y confirmado partidas en PDF. Se necesita conciliar el perímetro de EBIT, D&A, reinversión, intereses y pagos antes de adoptar una fórmula alternativa.

## Siguiente paso

Recibir parte36 para completar fuentes de Elis y revisar su registro. Después cerrar la revisión técnica y especificar la reparación acotada de los fallos anteriores, manteniendo separadas las propuestas económicas. La candidata sigue sin acreditar aptitud para dinero real.

## Ampliación tras recibir parte36

La parte36 coincide con su SHA-256. Se han reconstruido por archivo y SHA 6142 de las6798 entradas del manifiesto; faltan656, y el SHA del ZIP completo sigue sin comprobarse. El código y los componentes críticos empleados en las pruebas sí coinciden con el manifiesto final.

El registro de Elis da193/193 al ejecutar el comprobador. Se comprobaron independientemente las248 referencias de página de sus entradas publicadas y auxiliares: existen todas. No equivale a una reauditoría semántica de todas las entradas.

Sensibilidad independiente de I12: si C48 pasa de108.0 a82.933 manteniendo las restantes entradas, el precio de Sí calculado por el motor A existente pasa de7.3020553231 a8.9801824507 (+1.6781271276 euros). No se modificó el libro ni se simuló una reconstrucción completa del pipeline; es el efecto matemático aislado de la discrepancia documentada, no una corrección económica adoptada.

Dictamen de este hito: no aceptar la4.14 para decisiones con dinero real. Deben corregirse los tres fallos nuevos del comprobador y asegurar reproducción de entradas y vigencia de sus fundamentos. El problema económico F1 sigue requiriendo especificación y validación propia; reproducir la fórmula existente no lo resuelve.
