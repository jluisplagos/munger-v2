# Revisión externa de la 4.15, hito 1

Fecha: 15-nov-2026. Revisión ejecutada por ChatGPT sobre una copia aislada de la base 4.14 completa y el parche recibido. Rama de conservación: revision/4.15-hito1. No se ha modificado el código recibido ni fusionado con main.

## Dictamen

Las correcciones R1–R3 aportadas y la reproducción de C48 tienen evidencia favorable. El hito es intermedio: no cierra la verificación de entradas ni acredita aptitud para dinero real. Hay un hallazgo importante adicional, R415-SIGNO, que debe corregirse antes de dar por cerrado ese control. F1 y las fases pendientes del encargo siguen su curso.

## Integridad y alcance

- Base 4.14: ZIP original completo previamente verificado, SHA-256 bb51942cefb848e409a4828e3faeb70f94aa4d29af39cda6d90cd0a97cb7b93e.
- Parche recibido: munger_v2_r1_entrega4.15_hito1_cambios.zip, 2170738 bytes, SHA-256 2a56061cf223f22d15d9cf0e9c7ce2a7714a703983767517ac01e15162c1f2d0. CRC y rutas comprobados antes de extraer.
- Aplicación del parche en una copia aislada: 7004 entradas del manifiesto coincidentes; ninguna ausente o alterada. El propio manifiesto se conserva también.
- Cambios respecto a las entradas del manifiesto 4.14: 12 modificadas, 206 nuevas, ninguna eliminada; además se sustituye el manifiesto.
- El .sha256 aportado corresponde al ZIP completo 4.15, no al parche pequeño. Ese ZIP completo no se ha recibido y su huella no se declara verificada. La revisión del árbol completo es posible con la base 4.14 y el parche: no requiere recibir otra vez todas las partes.

## Comprobaciones ejecutadas

Se repitieron las baterías dirigidas recibidas: entradas 4.15 105/105, entrada efectiva 40/40 y entradas 4.14 adaptadas 33/33. Total: 178 pruebas, ninguna fallida. Sus JSON y registros están junto a este informe.

Las sondas propias confirman el bloqueo de página 999999 y fuente local ausente sin SHA, y el rechazo de los tres redondeos denunciados anteriormente (149.5 frente a 150; 0.49 frente a 0; 45479.209 frente a 45479). El control positivo sintético completo es apto.

Se ejecutaron las ocho reconstrucciones aportadas, con LibreOffice en secuencia y expedientes temporales. El detalle está en reconstruccion/RECONSTRUCCION_C48_4_15.md y sus JSON.

- Elis 4.14: conserva 108 solo con su valor migrado; retirándolo reproduce 82.933 y la diferencia calculada de +1.6781271276 por acción.
- Elis con el CAMBIO 4.15: reconstruye 108 con y sin el valor migrado; diferencia de resultado calculado cero. Persisten diferencias documentales de fecha/evidencia, declaradas por el autor, por lo que la igualdad integral del expediente nuevo deberá verificarse tras regenerarlo.
- Viscofan y Vidrala: resultados calculados iguales a las referencias. La reconstrucción de Vidrala confirma C50=0 sin declaración en la entrada generativa; al quitarlo cambian C50 y seis celdas de su lectura, sin efecto en el resultado de B.

Esta ejecución repite las herramientas de reconstrucción del autor; no constituye una validación económica independiente de F1. La regresión completa de 14 baterías está documentada por el autor y no se ha vuelto a ejecutar aquí: se ha concentrado la revisión en los cambios y los contraejemplos.

## R415-SIGNO — importante, reproducido

En el fixture SINTÉTICO completo y positivo:

- Historia!F6: valor_modelo 849.697; valor_fuente 849697; escala 0.001; signo 1; tratamiento «ninguno».
- Se cambia la página realmente conservada y la cita a «Partida sintética de Historia!F6: -849697.000».
- Se actualizan la huella de la fuente y los vínculos sintéticos de revisión, manteniendo el resto del registro coherente.
- Resultado: apto_por_entradas=true y la celda aparece comprobada, sin error, discrepancia ni pendiente.

También son True _cita_contiene('Importe: -149.5',149.5), el sentido inverso y la cantidad positiva frente a «(149.5)». La causa es que _cifras utiliza abs(x), y la búsqueda del token no conserva el signo publicado. No se afirma que esos errores se hayan cometido en los expedientes reales: el hallazgo demuestra que el control no los detecta.

El signo declarado para transformar la cifra hacia el modelo no sustituye al signo de la cifra publicada. Los registros reales ya usan valor_fuente negativo con signo=-1 para transformar pagos negativos en magnitudes positivas: ese tratamiento debe seguir admitido cuando está justificado. La reparación debe comprobar la cifra publicada con su signo y aplicar la transformación por separado.

Precaución específica para C48: calcular_entrada consume el mismo comparador. Los componentes actuales 130.8, 150.8 y 177.9 son magnitudes positivas de pagos publicados entre paréntesis. La conversión debe declararse explícitamente, preservando el cálculo justificado y el 108. Una reparación que rechace todos los pagos negativos, o altere el 108 para acomodar el comparador, sería incorrecta.

Reproducción portable:

    python -B docs/revision_externa_4_15_hito1/sondas_independientes.py --root munger_v2_r1 --output resultado_sondas.json

## Límites declarados que siguen abiertos

U2–U5 constan en el informe del autor: empates de redondeo monetario, round con coste sin acotar, sensibilidad con rechazos falsos y fuentes HTML con contenido no visible/codificaciones. Se han leído, no se presentan como nuevos hallazgos propios ni como reparaciones ya verificadas. Deben quedar resueltos o bloqueados de forma efectiva antes del cierre correspondiente. La propuesta de tolerancia general del autor no se adopta por esta revisión.

U1 requiere revisión independiente del sentido económico del derivado; ninguna regla sobre literales demuestra por sí sola ese sentido. I19, I20, F1, H-P1/X2 y la regeneración/auditoría de expedientes continúan pendientes de las fases posteriores. No se necesita reiniciar el trabajo de Claude para incorporar estos resultados.

## Discrepancia menor del empaquetado

MANIFIESTO_CAMBIOS.txt clasifica MANIFIESTO_SHA256.txt como cambiado y como nuevo. Por ello anuncia 13 cambiados y 207 nuevos, con una entrada contada en ambos grupos. El árbol recibido sí está completo y coincide con sus 7004 entradas. Corregir esa clasificación al preparar la siguiente entrega; no hace falta repetir una regresión funcional por una corrección exclusivamente documental del índice.

## Continuación

El mensaje completo para Claude está en PROMPT_PARA_CLAUDE.md. Incorporar las reparaciones al trabajo vigente, agrupar pruebas y revisión de lo afectado y ejecutar la regresión completa una vez estabilizada la candidata. Conservar la base y todas las evidencias. Este hito sigue siendo experimental supervisado.
