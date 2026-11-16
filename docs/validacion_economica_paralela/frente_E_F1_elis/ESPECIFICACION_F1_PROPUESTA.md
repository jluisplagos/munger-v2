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
- `A2_propio` exige `EBIT_NIIF16_PPA_constante`, porque f devuelve la PPA entera de forma perpetua.
- **No admisibles por ahora** (revisión n.º 3, N4). Disparan V-F1h hasta que se especifiquen con su fórmula y su prueba:
  - `margen_despues_de_arrendamientos`: la variante A1′ solo quita de f el principal (C49), y el interés de arrendamiento sigue en C48. Con un margen posterior a los pagos se contaría dos veces: 25,067 de media, 26,4 en la base 2025, antes de impuestos. Quitarlo de C48 chocaría con E0.3. Una definición posible, no adoptada: calibrar f con el NOPAT calculado sobre el mismo margen que se proyecta y con la reinversión sin ROU;
  - `EBIT_NIIF16_PPA_decreciente` con `A2_propio`: devolver solo la PPA proyectada exige una f que cambie con el tiempo o un término aparte, y E3 no cambia la estructura del flujo ni del terminal.
- Cualquier otra combinación dispara V-F1h.

**Matriz de coherencia de los tres perímetros** (revisión, O4 y O12). El margen objetivo, la reinversión que calibra f (E3) y el ancla de la palanca S2C (E4) deben describir el mismo tratamiento del arrendamiento y de la PPA:

| `perimetro_reinversion` | `perimetro_margen` coherente | f (E3) | Ancla de la palanca S2C (E4) | Si no casa |
|---|---|---|---|---|
| `A0_total` | EBIT NIIF 16 con PPA constante | Reinversión con D&A total | C53 con D&A total | V-F1a si hay arrendamientos materiales |
| `A1_sin_ROU` | `EBIT_NIIF16_PPA_constante`: la PPA se trata como coste de reposición que persiste | Reinversión con D&A total − ROU | C53 con el mismo D_X | V-F1h (margen) o V-F1g (ancla) |
| `A2_propio` | `EBIT_NIIF16_PPA_constante` (con `…_decreciente`: no admisible por ahora) | Reinversión con D&A propia; f devuelve la PPA entera | C53 con D&A propia | V-F1h o V-F1g |
| `A3_estimado` | El que declare la estimación para la PPA; si no lo declara, el de `A2_propio` | Reinversión con la D_X estimada (E1) | C53 con la misma D_X | V-F1d (estimación incompleta), V-F1h o V-F1g |
| Cualquiera con `margen_despues_de_arrendamientos` | No admisible por ahora: A1′ deja el interés de arrendamiento en f (N4) | — | — | V-F1h |

En este expediente las palancas S2C (1 / 1,2 / 1,5) no se anclan en C53 sino en un perímetro propio (informe §3). Con cualquier perímetro de reinversión, la regla V-F1g avisaría.

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

Tolerancia 10⁻⁹ salvo indicación. Los valores de referencia están en `resultados/contraste_f1.json → referencia_especificacion` y proceden de cifras verificadas contra los PDF.

**Límites de los valores de referencia.** Son valores de prueba de una implementación, no estimaciones económicas:
- se calculan con los datos, las palancas y la convención de redondeo actuales (E7). Si cambia cualquiera de ellos, hay que recalcularlos con `contraste_f1.py`;
- incluyen las partidas puntuales de la ventana sin normalizar, +27,9 en el flujo sin crecimiento (E8.4);
- los flujos de A1 y A2 usan las palancas S2C actuales, que no están ancladas en el perímetro de cada alternativa (V-F1g);
- los de `A3_estimado` usan estimaciones sintéticas de D_X, que no son datos de Elis;
- el C53 de referencia depende de las entradas del horizonte 2021–2025: ventas de 2020 y 2025, capex, D&A total, ROU y PPA, circulante, adquisiciones e impuesto de cada año. Desde C12 todas tienen una identidad entre páginas: las 97 entradas que mueven la referencia (R5, R8, R16, R17, R22, R34, R36 y R39–R42 en 2021–22, y R24 y R42 en 2023–25; véase `cobertura_entradas`. Precisión de C16, revisión n.º 7, S6 e: la lista citaba también R25 y R35 de 2021–22, que son de la misma página, y R23 de 2021–22, en la que no interviene ninguna de las 97). La clase es por pertenencia: lo que una identidad entre páginas acredita es el número salvo un error dentro del intervalo que no detecta, que se da para cada entrada (`errores_sin_deteccion_entre_paginas`; revisión n.º 6, R6). Para las 97, el mayor error que ninguna identidad entre páginas detecta va de 0,1 a 0,5; un error igual a ese umbral no se detecta. Hasta C11 esta frase decía «desde C9», pero cinco de ellas solo tenían identidad de su página (revisión n.º 5, Q6). La prueba de mutación lo comprueba para todas las clases (`resultados/cobertura_por_mutacion.txt`). Límite declarado: la cifra publicada de las adquisiciones de 2021 antes de la reexpresión (86,9) y la reexpresada (86,8) difieren en 0,1, dentro de la cota de R39, así que ninguna identidad las distingue. Antes de C7, la amortización ROU y la PPA de 2021–22 solo estaban comprobadas por lectura (revisión n.º 3, N2);
- no son valores por acción ni sirven para elegir un perímetro.

| Id | Prueba | Resultado esperado |
|---|---|---|
| T1 | Elis, perímetro `A0_total` (comparación, con V-F1a desactivada solo en la prueba) | f = 0,041681455273796; flujo sin crecimiento = 248,496395342656; flujos MALO/NORMAL/BUENO de los años 1–11 = los del libro actual (`A0_flujos_libro`); C53 = 9,039509536785 |
| T2 | Elis, `A1_sin_ROU` | f = 0,012624225323285; flujo sin crecimiento = 387,878115969269; C53 = 2,445331695332. Flujos MALO/NORMAL/BUENO con las palancas actuales: los años 1–10 y el año 11 terminal = `A1_A2_flujos_detalle.A1` (año 11: 294,942490201187 / 413,845194930899 / 488,862107627977). Detecta una implementación que cambie f en un término y no en otro (revisión, O13). Control negativo: si el terminal conserva la f de A0, el año 11 se desvía en V₁₀·(1+g)·(f_A0 − f_A1): 166,6 / 205,4 / 223,9 (`desvio_anio_11_implementacion_parcial`) |
| T3 | Elis, `A2_propio` | f = −0,006118601744165; flujo sin crecimiento = 477,783708846410; C53 = 1,612524303305. Años 1–10 y año 11 terminal = `A1_A2_flujos_detalle.A2` (año 11: 402,413237593105 / 546,310847791079 / 633,271006526708). Mismo control negativo del terminal: desvíos de 274,1 / 337,8 / 368,3 |
| T3b | `A3_estimado` con estimaciones **sintéticas** de D_X, que no son datos de Elis (`A3_estimado_sintetico`) | (a) D_X = capex propio en cada año: reproduce la cota B, f = 0,022646228408102 y flujo sin crecimiento = 339,804571572014. (b) D_X = D&A propia: reproduce A2. (c) D_X = (capex propio + D&A propia)/2: f = 0,008263813331969 y flujo sin crecimiento = 408,794140209212, el punto medio exacto de A2 y B, porque f es lineal en la D_X media. (d) Sin fuente, método, rango o responsable de la estimación, dispara V-F1d. No se usa la proporción de dos tercios del lino plano: es parcial y no es una proporción del capex total (informe §6.1). (e) Para cada caso, el C53 con la misma D_X (2,651525243106 / 1,612524303305 / 2,005440531963) y los flujos de los años 1–10 y del año 11 con las palancas actuales (`A3_estimado_sintetico.*.flujos_palancas_actuales`). Así se detecta una implementación que aplique la D_X a f pero no al ancla ni al terminal (revisión n.º 3, N5) |
| T4 | Identidad de calibración | Para cualquier perímetro, f·ventas medias = NOPAT medio − reinversión media − FCF base. En A0, la suma de los componentes del informe §4.2 = f·ventas con medias exactas (190,065713333…); con las entradas registradas de C46/C47/C50, C79 = 190,066046666667. La diferencia, 0,000333, es el redondeo de E7 |
| T5 | Caso sintético solo con arrendamientos (τ = 0, sin crecimiento: EBITDA 100; capex propio = D&A propia = 20; ROU 10; pagos 12 = 10 + 2) | FCF verdadero 68; A1 y A2 dan 68; A0 da 58 (prueba negativa que documenta el defecto) |
| T6 | Caso sintético con PPA 5 sin reposición | A2 = 68; A1 = 63; A0 = 53 |
| T7 | Sin NIIF 16 ni PPA (ROU = PPA = 0, C49 = 0) | Los cuatro perímetros dan el mismo resultado que la V6.3. Los casos de referencia del motor A de `v6/pruebas/resultados_v63.json` no cambian |
| T8 | Reglas V-F1a…V-F1h | Cada una dispara su efecto con un caso positivo y no se dispara con su caso negativo. V-F1a, además, con un caso por debajo del umbral de materialidad (solo AVISO) |
| T9 | Signos | D&A ROU y PPA publicados «(149.5)»/«(85.7)» se aceptan con `valor_fuente` negativo, `signo` −1 y `tratamiento`. La magnitud positiva sin esa declaración se rechaza (coherente con R415-SIGNO) |
| T10 | Invariantes de Elis | C46–C52, C48 = 108, C70 = 307,933, acciones, OCEANE y decisiones E1/D3/E2/E6 sin cambios. Solo cambian f (C58), C53, los flujos del motor y lo que dependa de ellos |
| T11 | Motor B (Viscofan, Vidrala) | Sin cambios en resultados de valoración (f = 0). Si cambia C53, solo cambian semáforos de diagnóstico, y se documenta |
| T12 | Reproducción independiente (revisión, O3; contraste externo; revisión n.º 3, N1–N3 y N10) | Sobre el material regenerado y por separado:<br>(a) `verificar_cifras.py`: 0 FALLO en las 752 filas y en cada una de las seis dimensiones (literal, ejercicio, columna, unidad, perímetro, edición). Las PENDIENTE deben ser solo las listadas en su salida, con su motivo: hoy 14, de URD 2022 p.302, sin unidad ni cabecera de columnas localizables, y una sola se usa, como contraparte. OK significa «sin incoherencia detectada por las reglas», no «acreditada». `test_verificar_cifras.py` 117/117: 23 positivos reales, 23 PENDIENTE esperados y 71 contraejemplos detectados en su dimensión, incluidos los de las revisiones n.º 1, n.º 3 y su adenda, n.º 4 a 7 y la columna de un país (C9). `sondas_metadatos.py`: 0 etiquetas cambiadas sin detectar. Mide la detección de etiquetas cambiadas, no la de cifras de otra unidad o de otro perímetro con una etiqueta verosímil;<br>(b) `contraste_f1.py`: se niega a calcular con una verificación de otro CSV. 0 fallos en cada clase y ninguna entrada usada con dimensión PENDIENTE. Los 126 residuos, dentro de su cota de redondeo calculada por cifra; la única excepción es la diferencia de concepto fijada de 2025 (+0,4 ± 0,15), con su límite de detección declarado. Las entradas usadas sin segunda línea deben estar listadas (`cobertura_entradas.sin_comprobacion`): hoy 31, ninguna con efecto en estos valores de referencia. Deben listarse también las páginas sin ninguna identidad entre páginas (`cobertura_entradas.paginas_sin_identidad_entre_paginas`, hoy 8 con 24 entradas): en ellas la unidad y el perímetro no están acreditados por una segunda línea. Ninguna entrada que mueva estos valores de referencia puede quedar sin identidad entre páginas (`cobertura_por_mutacion.py`). `test_contraste_residuos.py` 24/24. `cobertura_por_mutacion.py`: ninguna entrada declarada con una comprobación que la mutación no haga fallar, ni ninguna usada sin declarar. Las identidades algebraicas documentan, no prueban;<br>(c) la réplica del motor coincide con los flujos del libro regenerado.<br>Ni el código de salida 0 ni el número de comprobaciones bastan por sí solos |
| T13 | Exceso de caja distinto de cero (revisión, O15) | En una copia del libro recalculada con Análisis!C76 = 250 y = −80 (`prueba_caja_no_nula.py`): Motor!M6:M8 = C76 y (Motor!BL − Motor!M)·r = 248,496395342656 en los tres escenarios. Control negativo: la identidad anterior, BL·r − C76, se desvía en C76·(r − 1), que es −227,5 con 250 y +72,8 con −80 |
| T14 | Verificación de entradas del frente técnico | Debe rechazar los mismos contraejemplos que `test_verificar_cifras.py`, en la dimensión correspondiente:<br>· página inexistente o equivocada; fuente ausente, sin huella o con otra huella; redondeo; signo; posición distinta con el mismo literal;<br>· columna, bloque o saldo de otro ejercicio, también en una tabla con una tercera columna (F1);<br>· modo de control no admitido para el concepto (A1, A2, A4, H1);<br>· columna de otro concepto (D1, D2, activo frente a pasivo);<br>· recuentos e importes por acción como millones de euros (B1, B2, U1, U2);<br>· segmento, sublínea de un segmento, país o fila «Other» como grupo (C1, P1, P2a);<br>· edición no vigente;<br>· columna de una matriz con una celda vacía (N9);<br>· columna de un país en una tabla con columnas por país, y columna de una sociedad que no se asigna al ejercicio (C9);<br>· **criterio de formato**: un entero de seis cifras o más declarado en millones de euros queda PENDIENTE aunque su rótulo no sea de la lista (revisión n.º 4, P1: efectos de dilución en acciones);<br>· **criterio de título**: una fila bajo un título de bloque que nombra un país o un segmento queda PENDIENTE como del grupo. El título se busca hasta el principio de la página y al final de la anterior (revisiones n.º 4, P2, y n.º 5, Q4: bloques de pensiones de Francia, Irlanda y Reino Unido, en inglés y en francés);<br>· columna «published», «reported» o «publié» de una tabla de reexpresión declarada vigente: FALLO en edición; la «restated», OK (revisión n.º 5, Q1);<br>· columna de apertura («01/01/AAAA») y dos fechas del mismo año (revisión n.º 5, Q2). **Límite** (revisión n.º 6, R1): con columnas distintas para cada aparición del año, la cuenta de columnas puede igualar a la de números por accidente. Por eso la asignación por orden exige que cada número esté alineado con su columna (URD 2022 p.302: F13 y F14, PENDIENTE);<br>· **grupos de columnas**: si la cabecera repite los mismos ejercicios en cada grupo (una marca, una firma auditora), la columna del grupo no es la del grupo consolidado: perímetro PENDIENTE (revisión n.º 6, R1: F9; también los honorarios por firma, G2 y G4);<br>· **filas de una jurisdicción, una región o el desglose de un país** («› of which Ireland», «European Union (excluding France)», «Hors Union européenne»), con el rótulo unido aunque ocupe varias líneas: FALLO como del grupo; el TOTAL de esa tabla, OK (revisión n.º 6, R1: F1, F4 y F7);<br>· **encabezado numerado** de nota o de apartado («NOTE 13 …», «5.4 …»): cuenta como título y corta la búsqueda (revisión n.º 6, R2: G9);<br>· **cifra bajo una cabecera ajena**: FALLO solo si la columna de otro ejercicio está alineada con ella (5,5 caracteres o menos); si no, PENDIENTE (revisión n.º 6, R3: G6, el valor en libros bajo «Valeur comptable»);<br>· **título corto de la tabla** (de una sola celda, encima de su cabecera) que nombra un país, y cabecera con tres países o más sin ninguna columna reconocida: perímetro PENDIENTE (revisión n.º 6, R4: H1 y H2);<br>· filas de UGE con el prefijo «CGU» o «UGT» en la tabla del fondo de comercio (revisión n.º 6, R5: I12 e I14);<br>· **título numerado de la tabla y su continuación** («6.1.5 Consolidated statement of changes in equity / as at December 31, 2022»): no son cabecera de columnas; y una fila cuyo rótulo lleva la fecha de un saldo es de ese ejercicio (revisión n.º 7, S1: A1 y A10, OK; A8 y A9, FALLO);<br>· **línea de cifras sin rótulo**: toma el de las líneas de rótulo contiguas; un segmento así no pasa como grupo (revisión n.º 7, S2: B1 y B3);<br>· **pestaña del capítulo en el margen** al principio de la línea: no es el rótulo (revisión n.º 7, S3: C1);<br>· **tabla con una columna por país sin declaración de unidades ni de ejercicios**: perímetro PENDIENTE; la primera línea de un rótulo partido no es la cabecera de ejercicios (revisión n.º 7, S4: D1 y D5);<br>· **encabezado numerado en prosa** (con comillas o puntuación final): no es título (revisión n.º 7, S5);<br>· llamada con letra («(a)») en la cabecera: no deja PENDIENTE la cifra legítima ni rebaja a PENDIENTE la de otro ejercicio (revisión n.º 5, Q3);<br>· rótulos de segmento con «and», «et» o «CGU», o partidos en dos líneas (revisión n.º 5, Q5).<br>Estos criterios y las listas de rótulos detectan señales conocidas; no acreditan la unidad ni el perímetro (E9, T12).<br>Debe aceptar sus veintitrés positivos reales, entre ellos F2, F3, P2b, X2, el total de la nota de combinaciones de negocio, el total por países de la nota de pensiones, la columna «restated», el total del grupo bajo prosa que nombra un país, el impuesto total del grupo de la tabla por jurisdicción y los saldos de apertura y de cierre del estado de cambios en el patrimonio declarados con su ejercicio. Responde a los huecos de la revisión externa del hito 4.15 y de la revisión n.º 3 |

## E10. Lo que esta especificación no decide

- El perímetro ni la política de la PPA.
- El valor de la reinversión necesaria.
- La validez del motor A para Elis.
- Ningún precio ni recomendación.

Tras implementarla hay que repetir la réplica, regenerar los expedientes del motor A y auditar el material final con un auditor de contexto separado.
