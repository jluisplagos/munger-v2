# Decisiones que deja la verificación de las entradas (14-nov-2026, 13:20) · ninguna adoptada

Estas decisiones salen de la revisión independiente y de las correcciones en las ramas 4.14. Se añaden a D1–D12 (`DECISIONES_PENDIENTES_4_14.md`).
- Los hechos están comprobados en su página, en los informes de corrección de cada rama: `…_4_14/viscofan/Viscofan/CORRECCIONES_ENTRADAS_4_14.md` y `…_4_14/vidrala/Vidrala/CORRECCIONES_ENTRADAS_4_14.md`.
- Mientras no se decida, cada opción se calcula por separado y no se adopta ninguna.
- **Efectos medidos** (14:05) con `efecto_correcciones_entradas_4_14.py`, sobre copias del libro evaluado 4.13 congelado con las fases A, B y C fijas, recalculadas con LibreOffice. Reproducen la activa: Viscofan 40,16401 y Vidrala 56,01809. Resultados en `…_4_14/resultados/efecto_correcciones_{viscofan,vidrala}.md`. **Ningún caso cambia la zona (caro).**
- Las correcciones de hecho ya hechas en la rama mueven el precio de Sí +0,139 € en Viscofan (+0,134 de las pensiones) y −0,016 € en Vidrala (K13).

| Id | Empresa | Qué se decide | Opciones (hechos) | Efecto en el precio de Sí | Propuesta (no adoptada) |
|---|---|---|---|---|---|
| E1 | Viscofan y Vidrala | Si se sustituyen los **valores redondeados que el inversor escribió en la etapa 1** por los exactos de los datos (Viscofan C47–C50; Vidrala C46 y C47). El pipeline no los pisa: hace falta autorizarlo (`--sobrescribir` en Viscofan; vaciarlos en la etapa 1 en Vidrala) | conservar el redondeo (bloquea «apto por entradas» como discrepancia) · usar el exacto (77,533 / 8,294 / 5,547 / 3,707; 335,413 / 169,668) | **medido: 0,000 €** en el precio de Sí (solo motor A) | usar el exacto: es un dato, no un juicio |
| E2 | Vidrala | **Circulante 2024 (K14) con la venta de Italia:** plusvalía de 50,547 (60,065 − 9,518) cobrada en inversión (230,000); ninguna línea de ajustes la elimina y la fuente no dice dónde se compensa | 84,994 (tal cual) · ≈34,447 · ≈33,594 | **medido: +0,053 € (≈34,447) y +0,054 € (≈33,594)** sobre la activa 4.13; con las correcciones de la rama, 56,05107 y 56,05198 €, es decir **+0,049 y +0,050 € frente a la rama (56,00201)**. *Corrección (14-nov, 15:05): antes se dijo «+0,033 y +0,034 con las correcciones»; eran diferencias frente a la activa 4.13, no frente a la rama (mismo error que en E5; lo detectó el agente de la fase C).* La cota grosera del revisor (hasta −0,8 €) no se confirma: signo y magnitud distintos | quitar la plusvalía si se acepta que está en «otros activos y pasivos» (inferencia, no hecho publicado) |
| E3 | Vidrala | **Circulante 2023 (J14) reexpresado por Italia** | pareja A (87,210; 78,805; estado reexpresado, incluye 11,061 de partidas no monetarias de Italia) · pareja B (97,865; 89,866; original consolidado) | **medido: +0,010 €** sobre la activa 4.13; con las correcciones, 56,01192 €, es decir **+0,010 € frente a la rama**. *Corrección (15:05): antes se dijo «−0,006 € con las correcciones»; era la diferencia frente a la activa 4.13.* | B (original consolidado, sin partidas no monetarias) |
| E4 | Vidrala | **Intereses en financiación (C48)**: no hay línea; ninguna nota dice si el interés de arrendamientos está en «Pagos de intereses» o en los pagos de deuda | dato ausente (0) · 2,254 mm | **medido: 0,000 €** en el precio de Sí (solo motor A) | dato ausente, declarado |
| E5 | Viscofan | **Número de acciones** (es D3) | media ponderada diluida 2025, 45,479209 · en circulación a 31-dic-2025, 45,993399 | **medido (E fijo): 39,71499 € sobre la activa 4.13 (−0,449 €) y 39,85225 € con las correcciones de la rama (−0,451 € frente a 40,30282)**. *Corrección (14-nov, 14:15): antes se dijo «−0,312 € con las correcciones»; esa cifra era la diferencia frente a la activa 4.13 (40,16401), no frente a la rama. La persona responsable lo detectó.* | ya propuesta en D3 |
| E6 | Elis | **OCEANE y acciones**: las acciones diluidas medias de 2025 (259,08 M) ya incluyen 23,36 M de la conversión; las OCEANE siguen como deuda a 31-dic-2025 | sin conversión y OCEANE como deuda · con conversión y sin esa deuda | evita contarlas dos veces; por calcular | coherencia obligatoria; elegir una de las dos (relacionada con D3) |

**Hechos ya resueltos con la fuente (no son decisiones):**
- Vidrala K13 = −224,000, efecto neto publicado por la empresa (Informe de Gestión 2024, p. 114).
- Vidrala F8 = 91,088.
- Viscofan: pensiones (prestación definida), circulante sin provisiones, deuda 2017 y adquisiciones 2020 se rehacen en la extracción con las ediciones conservadas.

**Decisiones de la persona responsable (14-nov-2026, ≈14:10, en la conversación):**
- **E1:** usar los valores exactos de los datos (Viscofan C47–C50: 77,533 / 8,294 / 5,547 / 3,707; Vidrala C46–C47: 335,413 / 169,668) en lugar de los redondeos de la etapa 1.
- **D3:** autorizar 45,993399 millones de acciones en circulación a 31-dic-2025 (46.500.000 emitidas − 506.601 propias) para la rama con esa base, conservando fuente y conciliación. Condiciones:
  - conciliar el efecto (solo denominador: 40,30 → ≈39,85 €);
  - si cambian la capitalización, la r operativa u otras entradas, identificar cada cambio y separar sus efectos;
  - comprobar y declarar aparte la dilución potencial;
  - no presentarlo como actualización a 2026 (precio del 3-nov-2026 frente a acciones del 31-dic-2025: fechas distintas y sus límites, explícitos);
  - recalcular y auditar el material final, conservando el expediente anterior.
- **E2 (decisión, ≈14:30):** mantener K14 = +84,994 millones (cifra publicada) y conservar P1 ya registrado. Instrucciones:
  - No descontar los 50,547 millones sin una conciliación documental que demuestre su inclusión y el ajuste necesario, evitando duplicidades.
  - Separar la comprobación de la cifra publicada (verificable como dato) de la incertidumbre sobre su composición y su tratamiento económico (reserva registrada).
  - Conservar 34,447 millones como alternativa exploratoria identificada, sin convertirla en dato publicado ni adoptarla por su efecto.
  - Consecuencia sobre la conclusión: quitar la plusvalía movería el precio de Sí **+0,049 €** frente a la rama (se dijo +0,033 por error; ver la fila E2) y la zona seguiría siendo «caro». La conclusión no depende de la reserva.

**Supuestos de la orquestación (no son decisiones de la persona responsable).** La persona responsable no contestó E3 ni E4 y pidió seguir con un supuesto razonable y decirlo:
- **E3:** sin cambios. Se queda la pareja A (87,210; 78,805), el comparativo reexpresado que publica la empresa, que es lo que usa la regla de construcción (la cifra publicada más reciente), con el mismo criterio que E2: no cambiar una cifra publicada sin conciliación documental.
  - Reserva: las partidas no monetarias de Italia (11,061).
  - Alternativa: la pareja B (+0,010 € frente a la rama).
- **E4:** C48 queda como dato ausente declarado (vacío) y no como un cero no publicado. Así lo exige el requisito de verificación de la persona responsable (cero verificado ≠ dato ausente).
  - Efecto en el precio de Sí: 0,000 €.
  - Consecuencia: el motor A deja de ser calculable para Vidrala. El motor B no se ve afectado.
  - Alternativa no adoptada: 2,254 mm.
- Los dos supuestos se pueden revertir con una decisión explícita.

**Expedientes de las decisiones** (creados con `cambiar_base.py`; las ramas 4.14 se conservan sin cambios como expediente anterior):
- `…_4_14/viscofan_decisiones/Viscofan` (D3 y E1);
- `…_4_14/vidrala_decisiones/Vidrala` (E1 y E4).

**Decisión de la persona responsable sobre E6 (Elis; 14-nov-2026, ≈15:58, en la conversación; literal):**
«Usar la base coherente a 31-dic-2025: Acciones efectivamente en circulación a esa fecha: emitidas menos autocartera, con fuente y conciliación. Mantener las OCEANE como deuda por el importe que corresponda al pasivo a esa fecha. No añadir simultáneamente las acciones de su conversión al denominador. Conciliar el tratamiento de intereses en C48 con esa misma base. Identificar por separado la dilución potencial y su tratamiento; no ignorarla ni contarla dos veces. Corregir también el error de pensiones I25:L25 contra las fuentes. Recalcular, mostrar los efectos separados y auditar el material final. Conservar el expediente anterior. Esta rama será un análisis con base 2025. No presentarla como una valoración actualizada a 2026 ni aplicar parcialmente la conversión o la recompra.»
- Aplicación: expediente nuevo `…_4_14/elis_decisiones/Elis`, creado con `cambiar_base.py` desde `elis_motor_A/Elis`, que se conserva sin cambios. Extractor y revisor independiente son distintos. Los efectos se miden por separado.
- La declaración de acciones a 31-oct-2026 (238.313.588 emitidas; GlobeNewswire, 12-nov-2026) solo sirve de contexto y de dilución: no entra en la base.

**F1 (motor A y NIIF 16): sin respuesta de la persona responsable (14-nov, ≈15:58).** Supuesto de la orquestación: opción (a).
- En esta entrega se declara el defecto y no se corrige.
- El motor A queda como «no validado para casos con NIIF 16».
- El precio de Sí de Elis con el motor A no se presenta como conclusión utilizable.
- La corrección (b) queda pendiente.
- El supuesto se puede revertir con una decisión explícita.

**Cierres (14-nov-2026):**
- `vidrala_decisiones/Vidrala`: auditoría APROBADO (SA-fa0472f6bde97775, material 7ad2b7ae3c04b02a). Las condiciones de E2, de a) a f), se cumplen (`auditoria_condiciones_E2.md`). Paso 14: concluido.
- `viscofan_decisiones/Viscofan`: primera auditoría válida REPETIR (SA-5560fe3438e5febb).
  - Punto 10: la configuración seguía citando el divisor de la 4.13 en su naturaleza. La orquestación lo corrigió como cambio editorial, sin recálculo.
  - Corrección 1 de la fase C (terminada: la segunda auditoría, abajo, la aprueba).
  - Las condiciones de D3, de a) a e), se cumplen (`auditoria_condiciones_D3.md`).
- `viscofan_decisiones/Viscofan`: segunda auditoría APROBADO (SA-bdff49a38c72fabd, material ac9c53796eab59cd); las cinco condiciones de D3 se cumplen (`auditoria_condiciones_D3.v2.md`). Paso 14: concluido · Vigilar · esperar · objetivo condicionado de 39,80 €.
  - Avisos que no impiden aprobar:
    - Análisis!C42 (EV/EBITDA 9,47; con D3 sería 9,569) sigue con la capitalización anterior en el libro; no entra en el motor B;
    - la sección 1 del informe dice «330 de 232 celdas»: el numerador suma los auxiliares. Corregido en el código para los expedientes siguientes, no en este material cerrado.
- `elis_decisiones/Elis` (E6): auditoría APROBADO (SA-d58921ca0d0cf0fa, material e122326117abed07). Las nueve condiciones de E6, de a) a i), se cumplen, y el supuesto F1 está declarado (`auditoria_condiciones_E6.md`). Paso 14: **pendiente_de_datos · Vigilar · sin acción** (reparto del capex entre reposición y crecimiento no publicado; motor A no validado con NIIF 16).
  - Precio de Sí del motor A: 7,30 €, solo como zona (caro frente a 24,18 € del 4-nov-2026).
  - Rango de la réplica sin el doble cómputo F1: 11,08–21,89 €, con el ponderado máximo en 23,42 €, todo «caro».
