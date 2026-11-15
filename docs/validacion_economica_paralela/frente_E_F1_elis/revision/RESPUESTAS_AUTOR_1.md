# Respuestas del autor a la revisión independiente n.º 1

Revisión: [REVISION_INDEPENDIENTE_1.md](REVISION_INDEPENDIENTE_1.md), sobre el commit del autor 96a69ca. Es copia sin cambios, en la misma ruta, del archivo de la rama `auditoria/economica-f1-frente-e-revision` (commit 47551a2), como sus scripts (`scripts_revisor/`) y salidas (`resultados_revisor/`). La procedencia y las huellas están en [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).
Respuesta: 15-nov-2026. **Las 17 objeciones se aceptan, total o parcialmente. Ninguna se rechaza.**

Las citas nuevas que aporta el revisor se comprobaron en los PDF antes de usarlas. Se añadieron como filas verificadas de `datos/cifras_fuente.csv`, todas OK en `resultados/verificacion_cifras.json`.

| Obj. | Gravedad | Respuesta | Acción y ubicación |
|---|---|---|---|
| O1 | material | **Aceptada.** La búsqueda no encontró la frase de los dos tercios del lino plano: los términos usados no incluían «maintenance of the stock». El revisor tiene razón | Cita [P] con sus límites en el informe §6.1; resumen, punto 8, reescrito («no publicada como importe»); M1 actualizado; alcance real de la búsqueda declarado. Filas `TXT_LINO_2TERCIOS_2021…2025` y `VENTAS_LINO_PLANO_2025`. La conclusión `pendiente_de_datos` no cambia |
| O2 | material | **Aceptada.** La frase «para 2024–25 no hay un efecto precio publicado en las páginas revisadas» era incorrecta, incluso dentro de las páginas exportadas | El autor ya había añadido en 6fb9294 las citas de efecto volumen de URD25 p.122, DEU24 p.121 y URD25 p.309, después del commit revisado. Ahora: §3 y §6.2 reescritos con el efecto precio de 2024–25 (DEU24 p.252–253; URD25 p.307) y M5 redefinido como cuantificación no publicada. Filas `TXT_PRECIO_2024_GRUPO`, `TXT_PRECIO_2025_LATAM`, `TXT_PRECIO_2025_UK` |
| O3 | material | **Aceptada.** El verificador no comprobaba el ejercicio de la columna y el contraste no afirmaba los residuos | `verificar_cifras.py` comprueba ahora el ejercicio, con implementación propia: cabecera de dos ejercicios, tabla de crecimiento, bloque de movimientos, saldo con fecha y apertura/cierre en la cabecera. Cubre 670 filas automáticamente y 1 manual con justificación obligatoria. `test_verificar_cifras.py` pasa de 10 a 16 casos e incluye la mutación M1 del revisor, ahora rechazada. `contraste_f1.py` afirma los 57 residuos con ±0,15 y dos excepciones declaradas, y clasifica las 186 comprobaciones: 115 libro, 58 fuente, 13 algebraicas. T12 de la especificación reescrito |
| O4 | menor | **Aceptada.** El matiz es correcto: la plantilla solo es coherente consigo misma en su senda histórica si la palanca S2C se ancla en C53 | Informe §5.3 (alcance) y nota ¹ de §5.2; especificación E4. Cálculo propio en `contraste_f1.json → S2C_anclada_en_C53`: coincide con el del revisor (81,3 y 129,6 en el año 1; 517,6 y 496,6 de aumento de ventas) |
| O5 | menor | **Aceptada.** | Premisa (iv) explícita y conclusión marcada «[D, condicionada a la premisa iv]» en §5.3. Cita de Elis «capital expenditure (including lease renewal)» en §5.3 y en la evidencia de A1′ (§9). Fila `TXT_RENOV_ARR_2025` |
| O6 | menor | **Aceptada.** | §6.2: evidencia del plan climático contra la D&A propia como caso central, señales de contención del capex en 2025 y límite de la cota superior si hubiera infrainversión. §9: el plan climático como tercer tipo de inversión, pendiente de definición. Filas `TXT_PLAN_CLIMA_*`, `TXT_INVERSIONES_FUTURAS`, `TXT_CAPEX_*`. La cita del URD25 p.369 está partida entre columnas: se verifica en dos fragmentos |
| O7 | menor | **Aceptada.** | Resumen, punto 7, y §6.3: «mayoritariamente no deducible [I]», con los ratios 18,3 / 24,2 / 21,0 % y los límites de la fila de intangibles. Altas de 2025 provisionales (`TXT_ALTAS_PROVIS`) con el precedente 18,0 → 32,3. La amortización no caerá de golpe. §7 retocado |
| O8 | menor | **Aceptada.** La incoherencia entre §6.2 y §6.3 era real | §6.3 enlaza el crecimiento orgánico neto de bajas como evidencia parcial; cita los contratos de cuatro años y la bajada cualitativa de la tasa de pérdidas (`TXT_CONTRATOS_4A`, `TXT_PERDIDAS_2024`) y la compensación numérica A0 ≈ B − PPA. La conclusión «requiere decisión de política» no cambia |
| O9 | menor | **Aceptada.** | §4.2: efecto neto de +27,9 en el flujo sin crecimiento (cálculo propio: +13,7 / −4,0 / +18,3). Comprobé además el ≈ 18,6 del earnout con su efecto en el tipo de 2023 (18,65). Salvedad en el resumen, punto 8, en M1, en §9 y en la especificación (E8.4 y E9). Fila `TXT_SEGUROS_2025` |
| O10 | menor | **Aceptada.** | §5.5: tabla de tendencia y limitación de la razón constante (16,8 y 10,1); nota ³ de §9; especificación E8.5. Cálculo en `contraste_f1.json → arrendamientos_tendencia` |
| O11 | menor | **Aceptada.** | §8: cuatro límites de la deuda constante. Filas `TXT_REFIN_TIPOS` y `TXT_OCEANE_DEVENGO` |
| O12 | menor | **Aceptada.** | Especificación: parámetro `perimetro_margen` y regla V-F1h; V-F1a pasa a «MODELO NO APLICABLE», con umbral de materialidad configurable (0,5 % propuesto, no adoptado); aviso V-F1g con identificador; variante orgánica de C53 declarada nominal o deflactada. Informe §7 y §9 |
| O13 | menor | **Aceptada.** | Especificación T2/T3 con flujos de los años 1–11 de A1 y A2 (`referencia_especificacion.A1_A2_flujos_palancas_actuales`), y T3b para `A3_estimado` |
| O14 | forma | **Aceptada.** El resumen ya se había corregido en 96a69ca; faltaba §4.3 | §4.3: «30 flujos anuales» |
| O15 | forma | **Aceptada.** Era un error real de la comprobación, latente porque C76 = 0 | `contraste_f1.py`: F₀ = (BL − C76)·r |
| O16 | forma | **Aceptada.** | README separa las clases de comprobaciones; el caso pasa a llamarse «posición distinta con el mismo literal»; una fuente sin huella se rechaza con motivo, sin `KeyError` (caso 11 del test) |
| O17 | forma | **Aceptada.** | Nota ² de §5.2: el exceso exacto es 139,4 |

## Cambios del autor posteriores al commit revisado que no proceden de la revisión

En el commit 6fb9294, preparado mientras se revisaba 96a69ca:
- tres citas verificadas de efecto volumen (URD25 p.122 y p.309; DEU24 p.121);
- recuentos actualizados;
- observación de los commits del frente técnico hasta c0dcbd0, sin cambios relevantes para F1;
- configuración de la sesión de revisión en el registro.

En la versión que responde a esta revisión, además de lo que figura en la tabla:
- se retiraron los identificadores de modelo de `REGISTRO_CONFIGURACION.md`, del §12 del informe y de `revision/ESTADO.md`, por las reglas de la sesión;
- se observaron los commits del frente técnico hasta 56fca94: el bloque `verificacion_entradas` de la ficha (I20), pruebas y registros de regresión, sin cambios relevantes para F1 (informe, §1);
- se volvieron a exportar las páginas citadas (64);
- se añadieron los informes de la preparación (`evidencias/preparacion/`), la copia de los archivos del revisor con su procedencia y un manifiesto SHA-256 de la carpeta.

## Segunda pasada solicitada

Se pide al mismo revisor, que conserva su contexto, una segunda pasada **solo sobre lo afectado**:
- O1, O2 y O3 (material);
- las secciones del informe reescritas (§0, §3, §4.2, §5.2–§5.5, §6.1–§6.4, §7, §8, §9 y §10);
- la especificación (E2, E4, E5, E8 y E9);
- los scripts `verificar_cifras.py`, `test_verificar_cifras.py`, `especificacion_cifras.py` y `contraste_f1.py`.

Su informe se copiará igual, sin cambios y en la ruta que use en su rama, y se registrará en PROCEDENCIA_REVISOR.md, con las respuestas que procedan.
