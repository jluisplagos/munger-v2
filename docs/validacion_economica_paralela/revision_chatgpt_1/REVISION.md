# Recepción y contraste de la revisión independiente F1 n.º1

15-nov-2026. El informe independiente está publicado en la rama auditoria/economica-f1-frente-e-revision, commit47551a2e76791445f2515311c40d45de6e36cb1b. Revisa al autor en96a69ca; la rama del autor ya avanzó a6fb9294. No se han modificado scripts ni datos del autor ni el producto.

## Resultado

La revisión encuentra17 objeciones:3 materiales,10 menores y4 de forma. Su recálculo apoya las cifras y la conclusión económica sobre arrendamientos a crecimiento cero y en el terminal, con condiciones de interpretación que deben mantenerse. No declara aptitud de inversión ni cierra F1. La PPA sigue requiriendo política económica y el dato de reinversión necesaria no está completamente determinado.

## Contraste ejecutado aquí

- O1: reextracción directa de URD2025 PDF p.137 confirma «two-thirds» sobre mantenimiento del stock de lino plano. Es una proporción parcial; no es dos tercios de todo el capex ni resuelve por sí sola la reinversión necesaria para mantener ventas.
- O2: reextracción directa de URD2025 PDF p.122 confirma efecto precio y efecto volumen. El autor YA añadió evidencia de ambos en2024 y2025 en6fb9294. No debe pedirse repetir esa corrección como si no existiera; comprobar su alcance y registrar la respuesta a O2.
- O3: ejecuté prueba_mutantes.py del revisor sobre los scripts y datos del autor ACTUAL6fb9294. La mutación DA_ROU_2025 toma132.2 de2024 y se declara2025: verificar_cifras devuelve683/683, código0; contraste_f1 devuelve129/129, código0. Los residuos2025 cambian a+17.3 y−17.3. El flujo de referencia de A1 cambia387.878→381.812, y A2 477.784→471.718. El registro completo está en mutantes_autor_6fb9294.log.
- También pasan año2031, unidad monetaria para porcentaje y perímetro «segmento Francia» alterados. La fuente sin campo sha256 produceKeyError; la huella vacía se rechaza.

El hallazgo es de suficiencia de los controles. El revisor no encontró errores de concepto/año/edición en las cifras reales del autor; aquí no se afirma que esos datos contengan la mutación sintética. No he vuelto a ejecutar todo su recálculo ni emitido una aceptación económica definitiva.

## Continuación

Corresponde responder en la tarea AUTORA «Conciliación económica Elis/F1». ResolverO1 yO3, documentar el estado actual deO2 y responder individualmenteO1–O17. En particular, no dejar fuera como meros detalles el perímetro del margen, las referencias del terminal, las partidas puntuales y la distinción entre datos publicados e inferencias.

No adoptar automáticamente la propuesta de tolerancia±0.15 del revisor. Las tolerancias deben fundarse en unidad, precisión y agregación; las excepciones actuales−0.2 y+0.4 requieren explicación identificada y verificable, sin permitir que absorban nuevos errores. El test mutante de año debe cambiar conjuntamente posición y literal, preservando la consistencia textual para probar realmente la cabecera/ejercicio.

Después: nueva versión identificada porcommit, respuesta del autor y revisión independiente de lo afectado. Conservar C48=108 y decisionesE1/D3/E2/E6. No implementar una alternativa ni emitir una valoración por acción durante este cierre documental; la especificación propuesta y las decisiones pendientes se trasladarán al frente técnico cuando corresponda.
