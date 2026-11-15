# Registro de hipótesis del ensayo · Vidrala, ruta A con el motor B (entrega 4.5)

**Versión 4.5.** Copia del registro de la 4.4 (`../2026-11_Vidrala_ensayo/REGISTRO_HIPOTESIS_ENSAYO.md`, que se conserva intacto) con un solo cambio: la fila del circulante de 2024 pasa a contrastada y registrada, porque la persona responsable registró P1 el 9-nov-2026. Ninguna otra fila cambia.

Este registro se prepara **antes de recalcular**, como pide el encargo (§5). Las hipótesis no pasan a ser hechos por usarse en el ensayo.

**Clases** (las de la 4.3.1):
- **C** contrastada;
- **D** derivada por convención;
- **H** hipótesis;
- **L** localizada sin contraste;
- **A** ausente o pendiente de registro humano.

**r = 0,09** se conserva.

| Entrada | Valor del ensayo | Definición | Fuente | Fecha | Estado |
|---|---|---|---|---|---|
| Motor (C62) | B: «No · financiación cambia mucho» | Hipótesis principal del ensayo, fijada antes de ver resultados | Encargo de la 4.4 y de la 4.5; informe 4.3.1, §6.1 | — | H (metodológica). La fase A del ensayo debe justificarla; no se reutiliza la fase A antigua |
| **Circulante 2024 (K14)** | **84,994** | Aumento del circulante = −(suma de las líneas de variación del estado de flujos). La línea «(84.994)» da +84,994 | ES24 p.14, «Efectivo generado por las operaciones (84.994)»; EN25 p.7, comparativo «Cash used in operating activities (84,994)» con la línea «106,417)» sin paréntesis | 2024 | C · **registrado por la persona responsable** en `fase1_decisiones.json` (fecha 2026-11-09; SHA-256 del archivo `b4e47afc…c445a4`). La confirmación cubre solo P1 |
| D&A 2023 y 2024 (citas) | 87,21 · 117,72 | Sin cambio de importe | CF_2024.txt p.7 (antes p.4) | 2023–2024 | C (P8 aplicada, tipo A) |
| Deuda (L22) · arrendamientos (L23) | 213,613 · 49,3 | Préstamos del balance, arrendamientos incluidos, y pasivo NIIF 16 | EN25 p.3 y p.52 | 31-dic-2025 | C |
| Caja (L24) | 108,352 | Efectivo del balance, **con** los fondos del dividendo a cuenta | EN25 p.2 y p.7 | 31-dic-2025 | C. El tratamiento con derecho está en `RESOLUCION_DIVIDENDO_Y_ACCIONES.md` |
| Dividendo a cuenta | No se resta | Valor con derecho a 31-dic-2025; la obligación con los propios accionistas no es deuda del puente | OIR 2275; EN25 p.64, p.67 y p.70 | Sin derecho desde el 11-feb-2026 | Decisión del ensayo, con la alternativa documentada. Control de doble cómputo en la resolución, §2 |
| Pensiones (L25) | 6,223 | **Provisión de personal**: planes de prestación definida «y otras obligaciones con empleados». No es el déficit neto (obligación − activos del plan) | EN25 p.71–72 | 31-dic-2025 | C como provisión · H como déficit · A el déficit neto |
| Minoritarios (L26) | 0 | Cero heredado. Desde esta entrega lleva una cita literal: «Equity attributed to equity holders of the Parent 1,412,878 1,309,830» | EN25 p.3 (AR_2025, re-extracción de la partida) | 31-dic-2025 | **Pendiente de verificación** (H1): la IA no confirma ceros. El libro lo marcará «Dato no verificable» |
| Intereses en financiación (C48 e Historia fila 16) | 0 | Cero heredado. Cita: la línea «Interest paid» en explotación | EN25 p.7 y los años anteriores | 2016–2025 | Pendiente de verificación, igual que el anterior |
| Otros ceros heredados (adquisiciones, arrendamientos y principal antes de NIIF 16, otros activos financieros) | 0 | Ídem, con cita literal | AR_2016–AR_2025 | 2016–2025 | Pendientes de verificación (38 en total). No bloquean el valor; impiden el estado «LISTO · PROVISIONAL» completo |
| C63 · i | 0,0634 | Intereses pagados de 2025 ÷ deuda media con arrendamientos de 2024–2025 | Fórmula del libro | 2025 | D (aproximación histórica). No recoge la deuda de 2026 ni aclara si los intereses incluyen los de arrendamientos |
| `r_op` | ≈0,0869 (aritmética de la 4.3.1; el ensayo dará la del libro nuevo) | r·E/(E+D) + i·(1−τ)·D/(E+D) | Convención 4 | Mezcla: E de 3-nov-2026, D de 31-dic-2025, i de 2025 | D (tasa personalizada, no coste de mercado) |
| C52 · τ | 0,20032 | Tipo medio de 5 años (2021–2025) | Fórmula del libro | 2021–2025 | D; perímetro mixto (2021–2022 con Italia) |
| C37 · precio | 87,9 | Cotización intradía de una fuente secundaria. Probablemente sin derecho a la liberada | Control maestro (Bolsamanía, 3-nov-2026 10:13) | 3-nov-2026 | L · A el cierre oficial. Se conserva **sin lectura económica** en la ruta A |
| C55 · acciones | 35,206 | Emitidas a 31-dic-2025, autocartera incluida | EN25 p.60 y p.76 | 31-dic-2025 | C para 2025 (en circulación: 35,183, −0,07 %) · H para la fecha del precio · A las acciones a 3-nov-2026 |
| C41 · capitalización (E de `r_op`) | 3.094,6 | C37 × C55 | Libro | Fechas mezcladas | D · H su idoneidad. En la ruta A se usa solo como peso de `r_op` |
| C49 · arrendamientos (principal) | 4,5 | Hipótesis heredada | Control maestro (decisión del inversor del 23-oct-2026) | 2023–2025 | H. **No entra en el valor del motor B**; sí en `f` y en el FCF base mostrados |
| C46 · C47 · C52 | 335,4 · 169,7 · 161,2 | FCF base de la etapa 1 (decisión del inversor) | Control maestro | 2023–2025 | Perímetro mixto (4.3). No entran en el valor del motor B; contexto |
| Palancas (escenarios, S2C, márgenes, probabilidades) | **Por decidir en la fase B del ensayo** | Las antiguas son hipótesis heredadas, no decisiones nuevas | — | — | H. El S2C de referencia ≈0,92 es una consecuencia aritmética de P1, **no la palanca elegida** |
| Datos de 2026 heredados (C53, C54, C33 y C34: saldos de 30-jun-2026; Toro; recompras; Kristin) | Contexto | Semestral 1S2026 (doc. 2487), no conservado | Control maestro | 2026 | L, no contrastados. No entran en el motor B. La fase C debe tratarlos como hipótesis |

**Qué se excluye expresamente del ensayo:**
- cualquier lectura de precio frente a valor (precio de Sí, zona, margen o cubo como decisión);
- E1–E7;
- la actualización de 2026.
