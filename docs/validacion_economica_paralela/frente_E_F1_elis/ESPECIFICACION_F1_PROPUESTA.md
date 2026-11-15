# Especificación económica propuesta · F1 · motor A con NIIF 16 e intangibles adquiridos

Fecha: 15-nov-2026. Autor: frente E. Estado: **propuesta, no adoptada ni implementada**.
Fundamento: [INFORME_CONCILIACION_F1.md](INFORME_CONCILIACION_F1.md) y `resultados/contraste_f1.json`.

## E0. Condiciones previas

1. Decisión F1 de la persona responsable con la política completa, (a), (b) o (c), según el informe, §10. **Esta especificación solo se aplica si la decisión es (b)**, o (c) con estas reglas como guía del juicio.
2. Implementación sobre una versión técnica fijada por commit del frente T, que se cita. Antes de implementar, comprobar que esa versión no cambia los datos o definiciones usados aquí: Historia filas 6–18, Análisis C46–C52, C57, C58, C70 y Motor. En `d1f1fa9` solo cambia la declaración del signo de los componentes de C48.
3. Conservar: E1, D3, E2 y E6 tal como están registradas; C48 = 108 con su derivación; C52 = 307,933. Expedientes nuevos, con el anterior conservado.
4. No elegir el perímetro por su efecto en el precio. El perímetro y la política PPA son decisiones (informe §10, puntos 2–4).

## E1. Entradas nuevas de la Historia (por año, columnas C–L)

| Fila nueva (propuesta) | Contenido | Fuente en Elis | Regla |
|---|---|---|---|
| D&A de derechos de uso (NIIF 16) | Amortización ROU del año (magnitud) | Nota 4.5 («Right-of-use assets») | Cifra publicada entre paréntesis: declarar `valor_fuente` negativo, `signo` −1 y `tratamiento` (R415-SIGNO). Vacío = desconocido; 0 solo si se verifica |
| Amortización de intangibles de combinaciones (PPA) | Amortización de lo adquirido (magnitud) | Nota 4.5 / cuenta de resultados | Ídem |
| Reinversión necesaria estimada (solo perímetro A3) | Estimación documentada por año, con rango | No publicada (M1) | Exige fuente, método, rango y responsable; nunca se presenta como dato publicado |

Opcional, para el diagnóstico: compras de lino y amortización de lino, y pagos totales de arrendamientos.

Invariantes: D&A ROU ≤ D&A total, PPA ≤ D&A total y D&A ROU + PPA ≤ D&A total (fila 8).

## E2. Parámetro declarado: perímetro de la reinversión necesaria

Nuevo parámetro de configuración del motor A, `perimetro_reinversion`, con estos valores admisibles:

| Valor | D_X,t (D&A que se supone repuesta con capex propio) | Uso |
|---|---|---|
| `A1_sin_ROU` | D&A total − D&A ROU | Arrendamientos coherentes; la PPA se trata como reposición monetaria |
| `A2_propio` | D&A total − D&A ROU − PPA | Arrendamientos coherentes; la PPA, no monetaria y sin reposición |
| `A3_estimado` | Reinversión necesaria estimada (E1) | Si hay dato o estimación documentada |
| `A0_total` | D&A total | **Solo** si D&A ROU = 0 y no hay pagos de arrendamientos en el FCF base (C49 = 0). Es la V6.3 actual |

El parámetro es una decisión: se registra con fecha, persona y motivo, como E1–E6. No lo rellena el agente.

**Parámetro declarado del perímetro del margen** (revisión independiente, O12): `perimetro_margen`, con estos valores admisibles:

| Valor | Significado |
|---|---|
| `EBIT_NIIF16_PPA_constante` | El margen objetivo incluye una PPA de orden constante |
| `EBIT_NIIF16_PPA_decreciente` | El margen objetivo incluye una PPA que se agota según el valor neto publicado |
| `EBIT_NIIF16_sin_PPA` | El margen objetivo excluye la PPA |
| `margen_despues_de_arrendamientos` | El margen objetivo es posterior a los pagos de arrendamiento (EBITDAaL o similar) |

Combinaciones coherentes con `perimetro_reinversion`:
- `A2_propio` exige `EBIT_NIIF16_PPA_constante`, porque f devuelve la PPA entera de forma perpetua. Si se declara `…_decreciente`, f debe devolver solo la PPA proyectada.
- `margen_despues_de_arrendamientos` exige quitar los pagos de arrendamiento de f, o no contarlos en el margen.
- Cualquier otra combinación dispara V-F1h.

## E3. Calibración de f

Misma ventana (C57) y mismas guardas que el C58 actual, sustituyendo la D&A total por D_X en la reinversión:

f = { Σ_w EBIT_t·(1 − τ_t) ⁄ n − Σ_w (capex_t − D_X,t + ΔWC_t) ⁄ n − FCF base } ÷ (Σ_w V_t ⁄ n)

- La conciliación de las filas 73–81 debe mostrar D_X media y sus componentes. Recomendado: también la composición económica de f del informe, §4.2 (arrendamientos, intereses, impuesto, capex neto/bruto, partidas no monetarias), con su suma igual a C79.
- **Tratamiento fiscal.** El cambio de perímetro es antes de impuestos. Los efectos fiscales reales ya están en los impuestos pagados que calibran f; en Elis, el diferido de intangibles aporta 15,5/20,3/17,5 y el de NIIF 16 es casi neutro. No se añade ningún escudo fiscal adicional. Hay que declarar la limitación: el efecto fiscal se escala con las ventas aunque la PPA se agote.
- Sin cambios en la estructura del flujo ni del terminal (Convenciones §1–§3).

## E4. Ancla de S2C con el mismo perímetro

C53 = (V_L − V_G) ÷ Σ_{H..L} (capex − D_X + ΔWC + adquisiciones)

- Variante orgánica opcional, si se dispone del crecimiento orgánico publicado. **El crecimiento orgánico publicado es nominal e incluye precio** (informe §3, §6.2). La variante debe declararse como nominal o deflactarse con un efecto precio documentado; nunca se presenta como productividad en volumen.
- Las palancas S2C (Palancas B16:D16) deben declarar el perímetro con que se anclan. Si no coincide con `perimetro_reinversion`, se emite el aviso V-F1g.
- Con la palanca anclada en C53 y el perímetro `A0_total`, el exceso de arrendamientos de los años 1–10 disminuye con el crecimiento y se anula cerca del crecimiento histórico. A crecimiento cero y en el terminal persiste (informe §5.3). Por eso V-F1a no depende del ancla.

## E5. Reglas de control

| Id | Condición | Efecto |
|---|---|---|
| V-F1a | Motor A, Σ D&A ROU > 0 en la ventana, C49 > 0, perímetro `A0_total`, y D&A ROU media ÷ ventas medias ≥ umbral de materialidad. Umbral propuesto: 0,5 % de las ventas; es un parámetro de configuración, que no se adopta aquí | **MODELO NO APLICABLE** («coste de arrendamiento contado dos veces en la proyección»), no «datos inválidos»: los datos son correctos y la incoherencia es de definición (revisión, O12). Por debajo del umbral, AVISO |
| V-F1b | Motor A, C49 > 0 y fila de D&A ROU vacía en algún año de la ventana | **INCOMPLETO** (vacío ≠ 0) |
| V-F1c | Media de D_X > media de capex propio en la ventana | **AVISO** con justificación obligatoria (hipótesis de infrainversión documentada); sin ella, la entrada pasa a «hipótesis pendiente» |
| V-F1d | `A3_estimado` sin fuente, método, rango o responsable | **INCOMPLETO** |
| V-F1e | Invariantes de E1 incumplidos o signos sin declarar | **DATOS INVÁLIDOS** |
| V-F1f | `A2_propio` con PPA > 0 | Informativo: mostrar valor neto de intangibles adquiridos ÷ PPA (años de agotamiento al ritmo actual) y si las altas del último ejercicio son provisionales |
| V-F1g | Perímetro declarado de las palancas S2C ≠ `perimetro_reinversion` | **AVISO**, con la diferencia de anclas S2C entre perímetros |
| V-F1h | `perimetro_margen` incompatible con `perimetro_reinversion` (E2) | **MODELO NO APLICABLE** hasta que se declare una combinación coherente |

## E6. Presentación en el diagnóstico

- Puente FCF base → flujo sin crecimiento, en cinco líneas (informe §4.3): nivel del EBIT, cambio de tipo, escala de f, reinversión histórica y resultado.
- Tabla «Dónde queda el coste de arrendamiento» (informe §5.2).
- La salida debe decir que el perímetro es una **decisión** y que el reparto entre reposición y crecimiento **no está publicado** cuando así sea. La conclusión de nivel se mantiene como `pendiente_de_datos` mientras M1 esté abierto, salvo que la persona responsable registre otra política.

## E7. Redondeo de las entradas registradas

C46, C47 y C50 se registran con tres decimales, no con su media exacta. El efecto es −7,3·10⁻⁸ en f y ≤ 0,0006 mm en los flujos.

Hay dos opciones; hay que elegir y declarar una:
- (i) mantener «redondeo: 3» y llamarlo redondeo, no «valor exacto», en el registro;
- (ii) guardar la media exacta.

Ambas son admisibles. Lo que no se admite es presentar un redondeo como exacto.

## E8. Fuera de F1 (observaciones para una revisión económica separada; no implementar con F1)

1. Ventana del tipo: f se calibra con τ por año y la proyección usa τ de 5 años. Efecto en Elis: −8,0 en el flujo de partida.
2. Intereses proporcionales a las ventas sin endeudamiento nuevo. Efecto en Elis en el año 1: endeudamiento omitido de 60,4 a 166,1 si la deuda neta se mantuviera en el 63 % de las ventas.
3. Motor B, C63: intereses sin arrendamientos ÷ deuda con arrendamientos.
4. Partidas puntuales dentro de la ventana de f: earnout de 2023 y plusvalía de 2025, con +27,9 en el flujo sin crecimiento de Elis, común a todos los perímetros (informe §4.2). Requieren una regla de normalización, si se decide. **Los valores de referencia de E9 las incluyen**: no están normalizados.
5. Tendencia de los arrendamientos: pagos y amortización ROU crecieron más deprisa que las ventas (informe §5.5). Una razón constante no lo proyecta.
6. Inversión del plan climático: ni reposición ni crecimiento (informe §6.2). Definición pendiente.

## E9. Criterios de prueba

Tolerancia 10⁻⁹ salvo indicación. Los valores de referencia están en `resultados/contraste_f1.json → referencia_especificacion` y proceden de cifras verificadas contra los PDF. Incluyen las partidas puntuales de la ventana, sin normalizar (E8.4).

| Id | Prueba | Resultado esperado |
|---|---|---|
| T1 | Elis, perímetro `A0_total` (comparación, con V-F1a desactivada solo en la prueba) | f = 0,041681455273796; flujo sin crecimiento = 248,496395342656; flujos MALO/NORMAL/BUENO de los años 1–11 = los del libro actual (`A0_flujos_libro`); C53 = 9,039509536785 |
| T2 | Elis, `A1_sin_ROU` | f = 0,012624225323285; flujo sin crecimiento = 387,878115969269; C53 = 2,445331695332; flujos MALO/NORMAL/BUENO de los años 1–10 y 11 con las palancas actuales = `A1_A2_flujos_palancas_actuales.A1` (detecta una implementación que cambie f en un término y no en otro; revisión, O13) |
| T3 | Elis, `A2_propio` | f = −0,006118601744165; flujo sin crecimiento = 477,783708846410; C53 = 1,612524303305; flujos de los años 1–11 = `A1_A2_flujos_palancas_actuales.A2` |
| T3b | `A3_estimado` con una estimación sintética (D_X = capex propio en cada año) | Reproduce la cota B: f = 0,022646228408102; flujo sin crecimiento = 339,804571572014. Sin fuente, método, rango o responsable dispara V-F1d |
| T4 | Identidad de calibración | Para cualquier perímetro, f·ventas medias = NOPAT medio − reinversión media − FCF base. En A0, la suma de los componentes del informe §4.2 = f·ventas con medias exactas (190,065713333…); con las entradas registradas de C46/C47/C50, C79 = 190,066046666667. La diferencia, 0,000333, es el redondeo de E7 |
| T5 | Caso sintético solo con arrendamientos (τ = 0, sin crecimiento: EBITDA 100; capex propio = D&A propia = 20; ROU 10; pagos 12 = 10 + 2) | FCF verdadero 68; A1 y A2 dan 68; A0 da 58 (prueba negativa que documenta el defecto) |
| T6 | Caso sintético con PPA 5 sin reposición | A2 = 68; A1 = 63; A0 = 53 |
| T7 | Sin NIIF 16 ni PPA (ROU = PPA = 0, C49 = 0) | Los cuatro perímetros dan el mismo resultado que la V6.3. Los casos de referencia del motor A de `v6/pruebas/resultados_v63.json` no cambian |
| T8 | Reglas V-F1a…V-F1h | Cada una dispara su efecto con un caso positivo y no se dispara con su caso negativo. V-F1a, además, con un caso por debajo del umbral de materialidad (solo AVISO) |
| T9 | Signos | D&A ROU y PPA publicados «(149.5)»/«(85.7)» se aceptan con `valor_fuente` negativo, `signo` −1 y `tratamiento`. La magnitud positiva sin esa declaración se rechaza (coherente con R415-SIGNO) |
| T10 | Invariantes de Elis | C46–C52, C48 = 108, C70 = 307,933, acciones, OCEANE y decisiones E1/D3/E2/E6 sin cambios. Solo cambian f (C58), C53, los flujos del motor y lo que dependa de ellos |
| T11 | Motor B (Viscofan, Vidrala) | Sin cambios en resultados de valoración (f = 0). Si cambia C53, solo cambian semáforos de diagnóstico, y se documenta |
| T12 | Reproducción independiente (revisión, O3) | Sobre el material regenerado, por separado:<br>(a) `verificar_cifras.py`: 0 fallos en las 707 filas, con el ejercicio de la columna comprobado (670 automáticas y 1 manual justificada) y `test_verificar_cifras.py` 16/16, incluido el contraejemplo de columna de otro ejercicio con su propio literal;<br>(b) `contraste_f1.py`: 0 fallos en cada clase. Las 115 comparaciones con el libro y las 58 de fuente prueban datos: incluyen 57 residuos dentro de ±0,15, con solo las excepciones declaradas del FCF de 2024 (0,2) y del interés de arrendamientos de 2025 (0,4). Las 13 identidades algebraicas documentan, no prueban;<br>(c) la réplica del motor coincide con los flujos del libro regenerado.<br>El código de salida 0 no basta por sí solo |

## E10. Lo que esta especificación no decide

- El perímetro ni la política de la PPA.
- El valor de la reinversión necesaria.
- La validez del motor A para Elis.
- Ningún precio ni recomendación.

Tras implementarla hay que repetir la réplica, regenerar los expedientes del motor A y auditar el material final con un auditor de contexto separado.
