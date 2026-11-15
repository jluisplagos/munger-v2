# Condiciones de la decisión D3 · Viscofan (expediente viscofan_decisiones) · segunda comprobación

Decisión: C55 = 45,993399 millones de acciones en circulación a 31-dic-2025. La comprobé el 14-nov-2026 sobre el material vigente: ac9c53796eab59cd, solicitud SA-bdff49a38c72fabd. Los 25 SHA-256 de material_auditoria.json coinciden con los archivos. No modifiqué nada del expediente ni del anterior; el libro lo leí con openpyxl en solo lectura.

a) CUMPLE · La fuente y la conciliación de «emitidas − autocartera» se conservan.
- El libro vigente (Viscofan_v63_evaluada.xlsx, Control maestro J52 y J181) dice: «46.500.000 emitidas − 506.601 propias (AR 2025, nota 12.4, PDF p. 83; capital y número de acciones, PDF p. 76)». Remite a 2026-11_Vidrala_ensayo_4_13/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md.
- Esa conciliación existe y cuadra el movimiento de 2025: 690.795 al inicio + 1.599.709 compradas − entregas + recibidas = 506.601. En circulación quedan 45.993.399.
- Comprobé las dos cifras en texto/AR_2025.txt: la línea 2725 (PDF p. 76) da 46,500,000 shares y la línea 3093 (PDF p. 83) da 506,601 own shares.
- El libro tiene Análisis!C55 = 45.993399. Lo mismo recogen resultados.json, datos_v63.md §2 y la incoherencia [7] de fase_c.json.

b) CUMPLE · El efecto del solo denominador está identificado y separado de los demás cambios. Fuente: resultados/efecto_decisiones_viscofan.json.
- Solo el denominador (C55, con E fijo): 40,30282 → 39,85225 € (−0,45057 €).
- Solo la capitalización (C41 = 2.515,838925): −0,05466 €, por la r operativa (8,26034 % → 8,26768 %).
- Denominador y capitalización juntos: 39,79819 € (−0,50462 €).
- E1: 0,000 €.
- Las correcciones de entradas de la rama van aparte, en efecto_correcciones_viscofan.json: 40,16401 → 40,30282 €.

fase_c.md (§1.8) y la incoherencia [7] recogen esas cifras y avisan de que los efectos no suman exactamente. resultados.json da C55 = 45,993399, C41 = 2515,838925 y r_operativa_C15 = 0,0826769, igual que el caso conjunto. precio.json da P* = 39,79819.
Observación: Análisis!C42 (EV/EBITDA 9,47) sigue sin actualizar. Su evidencia (datos_v63.md línea 47; Control maestro J42) usa la capitalización 2.487,7 = 54,70 € × 45,479209 M; con D3 sería 9,569, según mi recálculo. La fase C ya lo anota como incoherencia [11]. No entra en el motor B ni en precio.json, así que no mueve el precio de Sí.

c) CUMPLE · La dilución potencial está comprobada y se declara aparte, sin adoptarla.
- El plan 2025–2027 prevé un máximo de 315.000 acciones (incentivo objetivo) o 472.500 (máximo): texto/AR_2025.txt, línea 5283, PDF p. 130.
- Con ellas, el precio de Sí sería 39,52748 € o 39,39350 €, con la capitalización sin cambiar (efecto_decisiones_viscofan.json → dilucion_potencial_declarada_aparte).
- Aparece aparte y como no adoptada en ficha.decision.condiciones_revision.a_la_baja («39,53 € … 39,39 €»), en ficha.insumos_decision_cartera.fundamento («declarada aparte y no adoptada: 39,53 / 39,39 €»), en Control maestro J52 («Dilución potencial NO incluida») y en configuracion_economica.json → naturaleza («se declara aparte y no se incluye»).

d) CUMPLE · Nada se presenta como actualización a 2026, y las comparaciones con el precio posterior explicitan la diferencia de fechas.
- «no es una actualización a 2026» aparece 18 veces en informe_provisional.md, 29 en ficha_provisional.json y 3 en fase_c.md, siempre en negativo. La única variante es «No es una actualización a 2026», en fase_c.md línea 173.
- Cada comparación con el precio del 3-nov-2026 lleva al lado las fechas distintas: el aviso de alcance en las secciones 1, 6, 7 y 14, C104 («acciones en circulación a 31-dic-2025 (D3) y precio del 3-nov-2026: fechas distintas»), Control maestro J41 y J180, ficha.insumos_decision_cartera.fundamento y el aviso V28 de la hoja (más de 90 días).
- Se corrigió lo observado en la primera comprobación. La limitación da ahora la última cifra oficial anterior al precio (30-jun-2026: 46.000.000 emitidas y 396.357 propias, 45,603643 M), con su fuente (datos_v63.md línea 46; Control maestro J41), citada y no adoptada. Da también su efecto aproximado: ≈+0,34 € por el solo denominador, que reproduje como 0,3406. Esto figura en fase_c.md, en la ficha y en el informe.
- La frase «N sigue en 45,479209» ya no está en configuracion_economica.json → naturaleza ni en el informe. El cambio es editorial: la huella económica (entradas_economicas.huella_configuracion) es 75726ca4a566c9ae… antes y después.

e) CUMPLE · Se conserva el expediente anterior. Solo comprobé existencia, fechas y tamaños.
- empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/viscofan/Viscofan existe, con 99 entradas.
- Su archivo más reciente es verificacion_entradas.json, del 14-nov-2026 a las 14:00:25. Ninguno es posterior a las 14:03:03, cuando se creó viscofan_decisiones.
- Los 200 archivos de antecedentes/heredados/ tienen la misma fecha y el mismo tamaño que sus originales.
- fase_c.rama.json y fase_c.rama.md tienen el mismo SHA-256 que fase_c.json y fase_c.md del anterior (3e48cb09… y f38d7823…).
