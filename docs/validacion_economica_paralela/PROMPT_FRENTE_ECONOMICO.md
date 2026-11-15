MUNGER V2 — FRENTE E: CONCILIACIÓN ECONÓMICA F1 EN PARALELO

Trabaja en una segunda tarea y copia aislada de https://github.com/jluisplagos/munger-v2, partiendo de auditoria/economica-f1. Otra tarea está corrigiendo controles técnicos; no uses ni modifiques su árbol de trabajo. Si esta tarea ya ha empezado, incorpora estas instrucciones y conserva los avances válidos, sin reiniciarla.

OBJETIVO Y LÍMITES

Cierra la conciliación económica de Elis/F1 con fuentes primarias y una réplica separada. Escribe informes y cálculos de contraste, sin modificar código, libros ni datos de producción y sin emitir una recomendación de inversión. Este frente prepara una especificación económica fundamentada para su posterior integración con el frente técnico.

MODELOS Y ESFUERZO

- Conciliación contable, interpretación económica, hipótesis, materialidad y especificación: Opus 5.5 con esfuerzo Máx.
- Descargas, inventarios, copias, huellas, organización de evidencias y empaquetado documental: Opus 5.5 con esfuerzo Alto. Agrupa estas operaciones para evitar cambios constantes de configuración.
- Revisión independiente de las conclusiones materiales y de sus cálculos: Fable 5.2 con esfuerzo Máx, en un agente o tarea con contexto separado del autor. Hazla cuando la conciliación esté preparada para revisión; repite después solo lo afectado por correcciones materiales.
- El frente técnico existente continúa con su configuración propia, Opus 5.5 y esfuerzo Alto; no cambies su sesión.

Estos usos están autorizados: no pidas autorización de nuevo por cada llamada prevista. Si tus herramientas permiten seleccionar modelo/esfuerzo por agente o fase, aplica esta distribución. No presupongas que un prompt cambia la configuración de la interfaz. Si no puedes controlar o comprobar alguno de estos ajustes, indícalo con precisión y señala el ajuste manual necesario; continúa las tareas independientes que puedas realizar. No afirmes que usaste un modelo, un esfuerzo o una revisión independiente sin evidencia. Cambiar de modelo dentro del mismo contexto no acredita revisión independiente. Registra las configuraciones reales cuando el entorno las exponga y marca «no verificable» lo que no puedas comprobar.

PREPARACIÓN Y BASE CONGELADA

Desde main, recupera el ZIP original de la Release base-4.14, materialízalo con tools/base_414.py y comprueba su manifiesto. Después vuelve a auditoria/economica-f1 y crea una rama propia para tus documentos. Si esa preparación ya está hecha y verificada, reutilízala.

La referencia congelada del producto es revision/4.15-hito1, commit 059f4f68dca7acf465b5f5b21de2dede84c885ff. Contrasta el manifiesto del hito y conserva los originales. No ejecutes la recuperación de la base14 sobre los textos de la15. Mantén separados los cambios no publicados del frente técnico; cuando se publique su versión, identifica cualquier cambio de datos o definiciones relevante para integrar tu especificación.

Lee estos archivos de docs/validacion_economica_paralela/:
COORDINACION.md
F1_INICIO_CONCILIACION.md
f1_evidencias.json
ACEPTACION_Y_ALCANCE.md

El inicio comprobó cifras y trazó fórmulas; F1 sigue abierto. No trates una sospecha de doble cómputo como un error económico ya demostrado. Los documentos de fuentes_traspaso/ describen un estado histórico y no sustituyen este encargo; registrar fuentes nuevas no significa disponer de sus bytes.

TRABAJO ECONÓMICO

1. Produce la conciliación anual 2023–2025 de EBIT, D&A por componentes, provisiones y otros ajustes, impuestos devengados/pagados y CFO. Concilia capex bruto/neto, adquisiciones, circulante, SBC, pagos/principal/interés de arrendamientos y deuda. Revisa 2021–2025 donde intervenga S2C o su horizonte histórico. Cada cifra debe llevar fuente, página PDF, unidad, signo, período y perímetro.

2. Explica el puente del FCF base 307,933 a la formulación del motor A y a f. El −81,2 de reinversión media en C58 está calculado, pero no demuestra por sí solo doble cómputo ni autoriza una corrección. Mantén C48=108 con su derivación registrada. Distingue 29,6 de interés lease implícito de caja de 29,2 de gasto devengado: no los intercambies sin puente. Separa lino propio de activos ROU y altas no monetarias de pagos.

3. Busca el desglose de reinversión necesaria frente a crecimiento y explica la reposición económica de los intangibles adquiridos. Si falta información, identifica exactamente qué falta, su materialidad y qué conclusión impide. No inventes porcentajes ni conviertas una estimación en dato publicado. No ajustes supuestos para elevar una valoración.

4. Contrasta las sumas y los puentes mediante un cálculo independiente que no se limite a copiar la fórmula existente. Distingue dato publicado, derivación, interpretación, hipótesis y decisión humana. Para cada alternativa económica, expón coherencia, evidencia, límites y consecuencias sin adoptarla por conveniencia del resultado.

REVISIÓN Y ENTREGA

Entrega una tabla de conciliación con residuos explicados; definiciones económicas; alternativas y supuestos; datos y decisiones pendientes; criterios de prueba para una futura implementación; cálculos reproducibles separados y evidencia primaria.

Somete las conclusiones materiales al revisor independiente Fable 5.2/Máx según la disponibilidad real descrita arriba. El revisor debe contrastar fuentes, signos, unidades, períodos, cálculos, residuos y significado económico, buscando también evidencia contraria. Conserva su informe, las objeciones y la respuesta a cada una. Si esa revisión no se realiza, debe quedar pendiente de forma explícita.

Guarda documentos y scripts de contraste en una carpeta propia, con commits, huellas y enlace a tu rama. Devuelve una especificación económica propuesta para que el frente técnico pueda implementarla posteriormente sobre una versión técnica fijada. No modifiques el producto para hacer coincidir cifras o eliminar una incidencia sin resolverla.

Las decisiones E1/D3/E2/E6 ya registradas se conservan; no vuelvas a pedirlas. No adoptes políticas pendientes por haber obtenido resultados numéricos. Si una incertidumbre material no se puede resolver o acotar con fundamento, conserva la conclusión afectada como pendiente. No declares aptitud para dinero real por superar pruebas técnicas o completar este informe. La integración, regeneración de expedientes, réplica y auditoría del material final se verificarán después.
