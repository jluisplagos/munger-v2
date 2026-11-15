MUNGER V2 — FRENTE E: CONCILIACIÓN ECONÓMICA F1 EN PARALELO

Trabaja en una segunda tarea y copia aislada de https://github.com/jluisplagos/munger-v2. Otra tarea está corrigiendo controles técnicos; no uses ni modifiques su árbol de trabajo.

Tu encargo es cerrar la conciliación económica de Elis/F1, con fuentes primarias y réplica separada. En esta fase escribe informes y cálculos de contraste, sin modificar código, libros ni datos de producción y sin emitir una recomendación de inversión.

Preparación: desde main, recupera el ZIP original de la Release base-4.14, materialízalo con tools/base_414.py y comprueba su manifiesto. Después cambia a auditoria/economica-f1 y crea una rama propia para tus documentos. La referencia congelada del producto es revision/4.15-hito1, commit 059f4f68dca7acf465b5f5b21de2dede84c885ff. Contrasta el manifiesto del hito y conserva los originales. No ejecutes la recuperación de la base14 sobre los textos de la15.

Lee docs/validacion_economica_paralela/COORDINACION.md, F1_INICIO_CONCILIACION.md, f1_evidencias.json y ACEPTACION_Y_ALCANCE.md. El inicio comprobó cifras y trazó fórmulas; F1 sigue abierto. No trates una sospecha de doble cómputo como un error económico ya demostrado.

Produce la conciliación anual 2023–2025 de EBIT, D&A por componentes, provisiones y otros ajustes, impuestos devengados/pagados y CFO. Concilia capex bruto/neto, adquisiciones, circulante, SBC, pagos/principal/interés de arrendamientos y deuda. Revisa2021–2025 donde intervenga S2C o su horizonte histórico. Cada cifra debe llevar fuente, página PDF, unidad, signo, período y perímetro.

Explica el puente del FCF base307,933 a la formulación del motor A y a f. El−81,2 de reinversión media en C58 está calculado, pero no demuestra por sí solo doble cómputo ni autoriza una corrección. Mantén C48=108 con su derivación registrada. Distingue29,6 de interés lease implícito de caja de29,2 de gasto devengado; no los intercambies sin puente. Separa lino propio de activos ROU y altas no monetarias de pagos.

Busca el desglose de reinversión necesaria frente a crecimiento y explica la reposición económica de los intangibles adquiridos. Si falta información, identifica exactamente qué falta, su materialidad y qué conclusión impide. No inventes porcentajes ni conviertas una estimación en dato publicado. No ajustes supuestos para elevar una valoración.

Entrega: tabla de conciliación con residuos explicados; definiciones económicas; alternativas coherentes con sus consecuencias y supuestos; datos y decisiones pendientes; criterios de prueba para una futura implementación; cálculos reproducibles separados y evidencia primaria. Contrasta las sumas mediante un cálculo independiente que no se limite a copiar la fórmula existente. Pide una revisión independiente de las conclusiones y documenta sus límites.

Guarda documentos y scripts de contraste en una carpeta propia, con commits, huellas y enlace a tu rama. Devuelve una especificación económica propuesta para que el frente T pueda implementarla posteriormente sobre una versión técnica fijada. No declares aptitud para dinero real ni adoptes políticas pendientes por haber obtenido resultados numéricos. Las decisiones E1/D3/E2/E6 ya registradas se conservan; no vuelvas a pedirlas.
