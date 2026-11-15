# Condiciones de la decisión D3 · Viscofan (expediente viscofan_decisiones)

Decisión: C55 = 45,993399 millones de acciones en circulación a 31-dic-2025. Comprobado el 14-nov-2026 sobre el material 53644d4b827d31a0, sin modificar nada del expediente ni del anterior.

a) CUMPLE · La fuente y la conciliación se conservan en todas las capas. El libro (Control maestro J52 y J181) dice «46.500.000 emitidas − 506.601 propias (AR 2025, nota 12.4, PDF p. 83; PDF p. 76)» y remite a 2026-11_Vidrala_ensayo_4_13/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md, que existe y cuadra el movimiento de 2025 hasta 506.601. Lo mismo dicen datos_v63.md §2 (C55), configuracion/cambio_decisiones_viscofan_4_14.json (metadatos.acciones_diluidas) y verificacion_entradas.json, con aux:AR2025_p76 y aux:AR2025_p83 «verificado». Comprobé las dos cifras en texto/AR_2025.txt: línea 2725 (46,500,000 shares) y línea 3093 (506,601 own shares).

b) CUMPLE · resultados/efecto_decisiones_viscofan.json separa cada efecto:
- Solo el denominador (C55, con E fijo): 40,30282 → 39,85225 € (−0,45057 €).
- Solo la capitalización (C41 = 2.515,838925): −0,05466 €, a través de la r operativa (8,26034 % → 8,26768 %).
- Las dos juntas: 39,79819 € (−0,50462 €).
- E1: 0,000 €.

fase_c.md (§1.8 y «Cambios frente a la rama», 1) recoge esas cifras y avisa de que los efectos no suman exactamente. resultados.json confirma C55 = 45,993399, C41 = 2515,838925 y r_operativa_C15 = 0,0826769.
Observación: Análisis!C42 (EV/EBITDA 9,47) depende de la capitalización y no se actualizó. Su evidencia (Control maestro J42, datos_v63.md) sigue con «capitalización 2487.7 (… × 45,479209 millones)»; con D3 sería ≈9,57. No entra en el motor B, así que no mueve el precio de Sí.

c) CUMPLE · La dilución potencial se comprobó y se declara aparte, sin adoptarla. El plan 2025–2027 prevé hasta 315.000 acciones (incentivo objetivo) o 472.500 (máximo), y la nota no dice si se entregarán con autocartera o con acciones nuevas; lo comprobé en texto/AR_2025.txt, PDF p. 130, línea 5283. Con ellas, el precio de Sí sería 39,52748 € (objetivo) o 39,39350 € (máximo), con la capitalización sin cambiar, en efecto_decisiones_viscofan.json → dilucion_potencial_declarada_aparte. Se declara aparte en fase_c.md §1.8, §9 y §10, en ficha.decision.condiciones_revision.a_la_baja, en ficha.insumos_decision_cartera.fundamento y en el informe.

d) CUMPLE · Ninguna salida presenta la elección como actualización a 2026. «no es una actualización a 2026» aparece 17 veces en informe_provisional.md, 28 en ficha_provisional.json y 4 en fase_c.md, siempre en negativo. Cada comparación con el precio del 3-nov-2026 lleva al lado la diferencia de fechas: el aviso de alcance en las secciones 1, 6, 7 y 14, C104 («fechas distintas»), la tesis B101, ficha.insumos_decision_cartera y fase_c.md §1.8 con el aviso V28 de la hoja (más de 90 días).
Observación: la limitación se queda en «la autocartera al 3-nov-2026 no consta». fase_c.md, el informe y la ficha no dicen que la última cifra oficial anterior al precio es otra: 46.000.000 emitidas tras la amortización de mayo de 2026 y 396.357 propias a 30-jun-2026, es decir, 45,603643 M en circulación. Esa cifra está en el propio expediente (datos_v63.md §2, evidencia de C41, y la conciliación de 4_13). Con ese divisor, el precio de Sí sería algo mayor: unos +0,3 € por el solo denominador, según una estimación proporcional mía que no está calculada en la hoja.

e) CUMPLE · empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/viscofan/Viscofan existe (97 entradas). Su archivo más reciente es verificacion_entradas.json, del 14-nov-2026 a las 14:00:25, y ningún archivo es posterior a las 14:03:03, cuando se creó viscofan_decisiones. Los 200 heredados de antecedentes/heredados/ tienen la misma fecha y el mismo tamaño que sus originales. fase_c.rama.json y fase_c.rama.md tienen el mismo SHA-256 que fase_c.json y fase_c.md del anterior (3e48cb09… y f38d7823…). Solo comparé existencia, fechas y tamaños; no modifiqué nada.

Observación aparte (no es una de las cinco condiciones): la sección 14 del informe y ficha.configuracion_economica reproducen de configuracion_economica.json → naturaleza la frase «N sigue en 45,479209 (VISCOFAN-ACCIONES)». Contradice D3 en el material entregado. Es el motivo del punto 10 de auditoria.md, que termina en REPETIR.
