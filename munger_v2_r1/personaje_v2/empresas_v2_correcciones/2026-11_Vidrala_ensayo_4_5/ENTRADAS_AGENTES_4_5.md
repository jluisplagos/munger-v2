# Entradas adicionales de los agentes · ensayo Vidrala 4.5 (9-nov-2026)

Este documento se añade a las entradas de cada paso de agente del pipeline (extracción, fases A, B y C, verificación). Lo exige el encargo de la 4.5 (§5). No sustituye los prompts del sistema: los complementa.

## 1. Qué es este análisis
- **Ensayo exploratorio, ruta A, base 2025.** El valor del motor B queda referido al 31-dic-2025. No es una valoración comparable con el precio del 3-nov-2026 ni una recomendación de compra o espera. Precio de Sí, zona, margen y cubo son **resultados mecánicos del ensayo**.
- **Motor B como hipótesis principal del ensayo** (C62 = «No · financiación cambia mucho»), fijada antes de conocer resultados. La fase A debe justificarlo de nuevo con la evidencia; si la evidencia no lo sostiene, debe decirlo, no forzarlo.
- **r = 0,09** (rentabilidad exigida de la persona responsable). No se cambia.
- **Ninguna hipótesis, probabilidad o escenario se modifica para obtener un Sí.** Todo cambio se justifica con evidencia y se registra.
- **Lo heredado no es decisión nueva.** El expediente original (`personaje_v2/empresas_v2/Vidrala/`) tiene fases A, B y C, extracto y auditoría antiguos. **No deben leerse ni copiarse.** Sus palancas, probabilidades y escenarios son hipótesis heredadas; los informes de la 4.3 y la 4.3.1 los citan como tales.

## 2. Documentos que deben leerse (rutas relativas a la raíz del paquete `munger_v2_r1/`)
1. `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_5/REGISTRO_HIPOTESIS_ENSAYO_4_5.md`: valor, definición, fuente, fecha y estado de cada entrada del ensayo.
2. `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/RESOLUCION_DIVIDENDO_Y_ACCIONES.md`: valor **con derecho** al dividendo a cuenta, a 31-dic-2025; la caja publicada (108,352) no se reduce en 43,338; cualquier comparación posterior con un precio sin derecho resta el dividendo **una sola vez**. Acciones (C55 = 35,206 emitidas; 35,183 en circulación) y liberada de 2026 (escenarios de autocartera condicionados, no límites).
3. Conclusiones pertinentes de la 4.3 y la 4.3.1 (`contrastes/vidrala_revision_financiera/`):
   - `INFORME_DEL_PERSONAJE.md` §3 (cadena de datos: perímetro tras la venta de Italia, NOPAT, FCF base, `f`), §4 (arrendamientos), §5 (adecuación del motor) y §6 (recomendación y alternativas). Las citas que hace de `fase_a.md` y de otras salidas antiguas describen la ejecución anterior; no son decisiones de este ensayo.
   - `ENTRADAS_Y_FECHAS.md` (clases C/D/H/L/A de las entradas del motor B; fechas; ruta A frente a ruta B).
   - `NOTA_SUBSANACION_4.3.1.md` («la recurrencia no acreditada no equivale a un carácter no recurrente demostrado»).
   - `MATRIZ_DE_COHERENCIA.md` §5 (comparabilidad histórica tras la venta de Italia).
   - `DECISIONES_PENDIENTES.md` (pendientes abiertos).

## 3. Hechos de la construcción del ensayo (comprobados)
- **P1 aplicado por registro humano** (`fase1_decisiones.json`, confirmado por la persona responsable el 9-nov-2026): Historia K14 = +84,994 (antes −127,84). Consecuencias aritméticas: Historia C53 (S2C de referencia) 1,549 → 0,916; C58 (`f` de referencia) 0,0199 → −0,0276.
- **El S2C de referencia ≈0,92 no es la palanca.** La fase B decide el S2C con su propio fundamento; la referencia arrastra problemas de comparabilidad (G6 con Italia, Vidroporto en 2023, el cobro de Italia en 2024).
- **P8** (dos páginas de D&A de 2024), sin cambio de importes.
- **38 ceros pendientes de verificación** (L26 minoritarios, C48 e Historia fila 16 intereses en financiación, adquisiciones 2018–2022, arrendamientos y principal antes de NIIF 16). La IA no los confirma; se mantienen pendientes y visibles.
- **Condiciones del motor B** (4.3, §5.2): g < `r_op`; ROIC a largo plazo > g; su valor resta deuda + arrendamientos + pensiones + minoritarios − caja de 31-dic-2025.

## 4. Fuera de alcance
- E1–E7 (ruta B), la actualización de 2026 (precio, acciones, capitalización, deuda nueva, Toro, recompras): no se completan ni se actualizan en silencio. Los datos de 2026 heredados en el libro son contexto no contrastado (registro de hipótesis, última fila).
- La rentabilidad exigida y la decisión de cartera pertenecen a la persona responsable.
