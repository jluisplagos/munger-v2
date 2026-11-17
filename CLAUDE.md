Esta es la candidata de integración técnica del programa de cierre (rama `integracion/candidata-cierre-v2`, según `jluisplagos/munger-v2-evidencias-mistral`, rama `coordinacion/cierre-v2`, `coordinacion/cierre_v2/INTEGRACION.md`:7), sobre 957af65: entrega 4.15 · hito 2 (`munger_v2_r1/VERSION`), intermedia y pendiente de revisión externa (`munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/PUNTO_DE_RECUPERACION.md`, «Siguiente paso exacto»). El código contiene las correcciones técnicas de los hitos 1 y 2, sin cierre económico ni aprobación final. Leer docs/revision_externa_4_15_hito1/, el registro del hito 2 (`munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/HITO_2_4_15.md`) y el encargo correctivo vigente. Mantener en main la base histórica 4.14. No sobrescribir el trabajo en curso de ninguna sesión de Claude.

# Instrucciones de continuidad

Idioma: español claro.
Leer primero README.md, docs/MIGRATION_STATUS.json y la revisión externa de docs/.
La base histórica está completa: 5790 archivos de texto en Git y los 1008 binarios dentro del ZIP original de la Release base-4.14. La descarga y los 6798 archivos del manifiesto se verificaron. Confirmar la materialización local con tools/base_414.py verify antes de ejecutar el pipeline.
No declarar completa la migración ni iniciar el pipeline financiero por el mero hecho de poder leer este repositorio.

La base histórica de referencia es la 4.14 (main); esta candidata es la 4.15 · hito 2. Las dos son experimentales supervisadas; no aptas para dinero real.
La revisión externa parcial de la 4.14 encontró:
1. página inexistente aceptada por verificacion_entradas;
2. fuente local ausente aceptada si no lleva huella;
3. redondeo aceptado como si fuera la cifra exacta;
4. C48 de Elis: 108 en Excel frente a 82.933 en fase1_v63. Conservar la entrada 108 justificada por sus fuentes y corregir la derivación/reconstrucción; no sustituirla automáticamente por 82.933;
5. vigencia de fundamentos, cifras de juicio y recuentos desfasados;
6. relevo caducado y aptitud por entradas omitida en salidas V6.3;
7. F1: el modelo A requiere conciliación y validación propias.

Situación en esta candidata (`munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/HITO_2_4_15.md` §7 y §9): el código de los hitos 1 y 2 de la 4.15 corrige las verificaciones de 1–3, la derivación de C48 en la vía 4.15 (108; punto 4), la vigencia de fundamentos, la cobertura de las cifras de juicio y los recuentos (5), y la aptitud por entradas en las salidas y la detección del relevo caducado (6). No está cerrado: los expedientes Viscofan, Vidrala y Elis siguen «no aptos por entradas» y C48 y C50 no son reproducibles en los expedientes 4.14 hasta su regeneración y auditoría con extractor y revisor reales; U1; U6 (a); los límites del §5; el control de la entrega 4.14 (29/35); el límite H9 del relevo caducado (I19/H9). 7, F1, sigue abierto en otra tarea y pendiente de decisión.

Los contraejemplos y la revisión externa están en docs/. Los 119 tests repetidos de la 4.14 no cubrían los tres huecos nuevos; desde la 4.15 los cubre `test_verificacion_entradas_415.py` (190 pruebas en el hito 2).

Mantener originales y decisiones humanas registradas. Trabajar en ramas y expedientes nuevos.
No cambiar fuentes ni huellas para legitimar un resultado antiguo.
LibreOffice y pipelines que lo usan van en secuencia.
No reactivar aprobaciones retiradas ni aceptar una auditoría de material distinto.
No inventar firmas, política económica ni aptitud por superar controles de software.

Usar Opus con esfuerzo alto para coordinación e implementación ordinaria.
Fable con esfuerzo máximo de forma selectiva para problemas económicos o técnicos difíciles y revisión crítica,
con aviso y registro, sin pedir otra autorización en cada uso.
La revisión debe hacerse por un agente distinto del autor del cambio.

El encargo correctivo vigente pegado por la persona responsable prevalece sobre propuestas antiguas de continuidad.

No interrumpir los encargos que corran en otras sesiones de Claude. La entrega del hito 2 de la 4.15 ya está importada en esta candidata, sobre 957af65. Otras correcciones aún en curso no se han importado: F1 sigue en otra tarea y esta candidata es una integración técnica. Esperar su entrega final y conservarla; después importarla como nueva versión sobre una copia completa, nunca sobrescribirla con la base histórica.

Para recuperar los binarios históricos, leer la sección de archivos pesados del README. Para una nueva entrega, seguir docs/RECEPCION_ENTREGA_CLAUDE.md. Usar el ZIP original completo de la Release base-4.14; la alternativa de recuperación parcial quedó sustituida. Las herramientas de recuperación son exclusivas de la base histórica 4.14.
