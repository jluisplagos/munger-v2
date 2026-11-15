# Respuesta del autor a la revisión independiente n.º 1 y al contraste externo

**Revisión:** [REVISION_INDEPENDIENTE_1.md](REVISION_INDEPENDIENTE_1.md), sobre el commit del autor 96a69ca.
- Es copia sin cambios, en la misma ruta, del archivo de la rama `auditoria/economica-f1-frente-e-revision` (commit 47551a2e76791445f2515311c40d45de6e36cb1b), como sus scripts (`scripts_revisor/`) y salidas (`resultados_revisor/`).
- Procedencia y huellas: [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).

**Contraste externo:** `docs/validacion_economica_paralela/revision_chatgpt_1/` de la rama `auditoria/economica-f1` (commit 5ce263a), sobre el commit del autor 6fb9294.

**Resultado:**
- 16 objeciones se aceptan y se corrigen tal como se proponen.
- O3 se acepta y se corrige con un matiz: la tolerancia global de ±0,15 que proponía el revisor se sustituye por cotas de redondeo calculadas para cada identidad.
- Ninguna se rechaza.

## Commits

| Clave | Commit | Contenido |
|---|---|---|
| C1 | 96a69ca | Primera entrega; la que revisó el revisor |
| C2 | 6fb9294 | Efecto volumen de 2024–25; registro de la sesión de revisión. Lo revisó el contraste externo |
| C3 | eb77dea | Primera respuesta a O1–O17: control del ejercicio de la columna; residuos afirmados con ±0,15 y dos excepciones; citas nuevas; informe y especificación |
| C4 | d2e585e91638c363682a000bdb416a4b865c6cce (también en [ESTADO.md](ESTADO.md)) | Verificador en cinco dimensiones; cotas de redondeo por identidad y una única excepción fijada; contraste entre páginas; mutantes conjuntos; exceso de caja no nulo; A3 sintético y control del terminal; respuesta individual con su prueba |

## Marcas y pruebas

**Marcas de evidencia:** [P] dato publicado · [D] derivación · [I] interpretación · [H] hipótesis · [DH] decisión humana.

**Pruebas que se citan** (todas en `scripts/`; las salidas, en `resultados/`):
- `verificar_cifras.py`: estado de cada fila en cinco dimensiones (`verificacion_cifras.json`);
- `test_verificar_cifras.py`: 39 casos (`test_verificar_cifras.log`);
- `test_contraste_residuos.py`: 7 casos (`test_contraste_residuos.log`);
- `contraste_f1.py`: 236 comprobaciones (`contraste_f1.json`, `contraste_f1.md`);
- `prueba_caja_no_nula.py`: copia del libro recalculada con LibreOffice (`caja_no_nula.json`);
- `revision/scripts_revisor/prueba_mutantes.py`: los mutantes del revisor, ejecutados sobre C4 sin cambiar nada (`mutantes_revisor_sobre_C4.txt`).

## Materiales

### O1 · dos tercios del lino plano · **aceptada y corregida** (C3, C4)

**Hecho publicado** [P]: «flat linen, two-thirds of which ensures the maintenance of the stock in circulation». Figura en el factor de riesgo de los cinco informes: URD 2025 p.137, DEU 2024 p.135 (en francés), URD 2023 p.239, URD 2022 p.221 y URD 2021 p.189.

**Qué se hizo:**
- C3 cita la frase en el informe, §6.1, con sus límites [I]:
  - solo se refiere al lino plano: 2.217,4 de 4.796,8 de ventas en 2025, el 46,2 % [P][D];
  - mantener el stock en circulación no es la reinversión necesaria para sostener las ventas;
  - es un texto fijo, sin importes;
  - no se extiende a todo el lino ni a todo el capex: dos tercios de las compras de lino serían 396, por debajo de su amortización de 565,1 [D].

  También reescribe el punto 8 del resumen («no publicada como importe») y M1.
- C4:
  - repite la búsqueda en todos los textos de la carpeta de fuentes (2016–2026) con los términos de la revisión y otros. Ninguno publica una tasa ni un importe de reposición (§6.1);
  - concreta en M1 lo que sigue pendiente: (a) el importe invertido en lino plano; (b) la proporción de mantenimiento del resto del capex; (c) cuánto de la dotación a clientes nuevos repone clientes perdidos; (d) la fecha y la base de la estimación;
  - deja automático el ejercicio de la fila de ventas de lino plano, que antes era manual.

  La proporción **no** se usa como porcentaje del capex ni como reposición suficiente: tampoco en la prueba T3b de A3, que usa valores sintéticos.

**Pruebas:**
- `TXT_LINO_2TERCIOS_2021`…`2025`: OK en literal, ejercicio de la publicación y edición por el pie de página;
- `VENTAS_LINO_PLANO_2025`: OK en las cinco dimensiones, en la columna «Total» de la matriz por segmentos;
- casos del test: «positivo: prosa del factor de riesgo», «positivo: total de la matriz por segmentos» y «columna de un segmento (Francia) declarada como grupo» → FALLO en perímetro.

**Conclusión:** `pendiente_de_datos` no cambia.

### O2 · efecto precio y efecto volumen 2024–25 · **aceptada y corregida** (C2, C3)

**Hecho publicado** [P]: hay efecto precio y efecto volumen en 2024 y 2025, en estas páginas:
- volumen: DEU 2024 p.121; URD 2025 p.122 y p.309;
- precio: DEU 2024 p.252–253; URD 2025 p.307.

**Qué se hizo:**
- C2, antes de recibir la revisión, ya citaba el efecto volumen (URD 2025 p.122 y p.309; DEU 2024 p.121).
- C3 añadió el efecto precio, reescribió §3 y §6.2 y redefinió M5.
- C4 comprobó el texto: separa la **existencia publicada** [P] de la **cuantificación ausente**. Elis no publica el reparto precio/volumen del orgánico de 2024–25 a nivel de grupo (§6.2; M5). No se repitió ninguna corrección válida.

**Pruebas:**
- `TXT_VOLUMEN_2025`, `TXT_VOLUMEN_2024` y `TXT_VOLUMEN_COSTES` (C2);
- `TXT_PRECIO_2023`, `TXT_PRECIO_2024_GRUPO`, `TXT_PRECIO_2025_LATAM` y `TXT_PRECIO_2025_UK` (C3);
- todas OK; caso del test «prosa declarada de un ejercicio distinto del de la publicación» → FALLO en ejercicio.

### O3 · los scripts podían pasar con datos incorrectos · **aceptada y corregida, con un matiz** (C3, C4)

**Qué demostró el contraste externo sobre C2.** Con `DA_ROU_2025` tomando 132,2 de la columna de 2024:
- `verificar_cifras.py` pasaba 683/683 y `contraste_f1.py`, 129/129;
- los residuos pasaban a +17,3 y −17,3;
- las referencias de A1 y A2 cambiaban (387,878 → 381,812 y 477,784 → 471,718);
- el año 2031, la unidad «mm EUR» en un porcentaje y el perímetro «segmento Francia» también pasaban;
- una fuente sin `sha256` abortaba con `KeyError`.

**Qué corrigió C3, y por qué no bastaba.** C3 comprobaba el ejercicio de la columna y afirmaba los residuos con ±0,15, y rechazaba M1. Pero no comprobaba unidad, perímetro ni edición: M4 solo fallaba por el año. Además usaba una tolerancia global y ensanchaba la de las dos excepciones (0,25 y 0,45), que así podían absorber errores nuevos de hasta ese tamaño.

**Qué corrige C4:**
1. **Cinco dimensiones** en `verificar_cifras.py`. Cada una queda en OK, PENDIENTE (con su motivo) o FALLO:
   - **literal;**
   - **ejercicio:** seis modos automáticos; el control manual queda PENDIENTE, nunca OK;
   - **unidad:** la declaración de unidades de la tabla, o el «%» del literal;
   - **perímetro:** la cabecera de la página es de estados consolidados o de resultados del grupo; en una matriz por segmentos solo vale la columna «Total»;
   - **edición:** el pie de cada página fija el ejercicio de la publicación, que debe ser el declarado en `fuentes.json`. Cada fila declara si su fuente es la vigente según la regla de la Historia o una «anterior».

   Resultado sobre los datos reales: 702 OK, 14 PENDIENTE y 0 FALLO. Las PENDIENTE tienen la unidad sin imprimir en la tabla de arrendamientos del URD 2022 p.302, y ningún cálculo usa esas filas.
2. **Entradas de los cálculos.** `contraste_f1.py` solo usa cifras sin FALLO, de la edición vigente, del perímetro del grupo y con la unidad que pide cada cálculo: 363 entradas, ninguna pendiente. Termina con código 2 si usara alguna pendiente.
3. **Cotas de redondeo, no tolerancia global** (el matiz). Cada uno de los 71 residuos se afirma con su cota: media unidad de la última cifra impresa por cada cifra que interviene. La cota va de 0,10 a 0,50 según la identidad; está en `residuos_con_cota`. Un residuo mayor que su cota hace fallar el cálculo:
   - **−0,2 (FCF 2024):** no es una excepción. Está dentro de la cota de sus siete cifras impresas (0,35). La explicación es verificable: la propia cota se calcula desde la precisión impresa;
   - **+0,4 (interés de arrendamientos 2025):** es la única excepción, una diferencia de concepto entre pago (29,6 = 177,9 − 148,3) y devengo (29,2). Se identifica por las etiquetas publicadas y las tres cifras se verifican en tablas distintas. La causa no se publica [H] y es inmaterial (0,133 en C48). Se exige en su valor exacto, +0,4 ± 0,15, de modo que un error nuevo en cualquiera de sus tres cifras la hace fallar.
4. **Contraste entre páginas.** Cinco identidades nuevas comparan una cifra con su segunda presentación en otra página: resultado financiero, resultado antes de impuestos, PPA, ventas por segmentos y adquisiciones. La tabla `cobertura_entradas_clave` muestra que 71 de las 72 entradas clave de la ventana tienen contraste entre páginas. La otra, las adquisiciones de 2023, se compara con la Historia del libro. Las 28 identidades algebraicas siguen marcadas como tales: documentan, no prueban datos.
5. **Mutantes conjuntos**, en `test_verificar_cifras.py` (39 casos). Se mantienen los 16 anteriores, el manual justificado pasa a exigirse PENDIENTE y se añaden positivos reales y mutantes:
   - posición y literal de la columna de otro año (M1);
   - año alterado;
   - tabla de un solo ejercicio declarada de otro año;
   - unidad «%» en millones y «mm EUR» en un porcentaje;
   - tabla en miles de euros de la sociedad matriz;
   - perímetro de segmento, columna de segmento y perímetro desconocido;
   - edición original declarada vigente: cambian a la vez fuente, página, etiqueta, posición, literal y valor;
   - fuente con otro ejercicio o sin él;
   - M4 combinado.

   Cada uno debe fallar en su dimensión y en los coherentes ninguna otra puede fallar.
6. **Segunda línea de defensa** (`test_contraste_residuos.py`, 7 casos). Con el verificador saltado a propósito, los residuos hacen fallar el cálculo ante M1 (R6 y R16 de 2025), ante un error nuevo en las cifras de la excepción fijada (dos casos), en el FCF de 2024 y en las ventas. Documenta el límite: un error menor que la cota no lo detecta ninguna identidad.

**Pruebas:**
- `test_verificar_cifras.py` 39/39 y `test_contraste_residuos.py` 7/7;
- `prueba_mutantes.py` del revisor, sin cambios, sobre C4: M1 FALLO (ejercicio); M4 FALLO (ejercicio, unidad y edición del porcentaje, y perímetro de las ventas); M2 y M3 FALLO con motivo, sin `KeyError`;
- especificación T12 y T14.

## Menores

### O4 · alcance de la demostración según el ancla de S2C · **aceptada y corregida** (C3; C4 añade la matriz de coherencia)

**[D]** Con la palanca anclada en el C53 de cada perímetro, la brecha del año 1 baja a 81,3 (A1) y 129,6 (A2). Se anula con un aumento de ventas de 517,6 o 496,6. Coincide con el recálculo del revisor.

**Qué se hizo.** C3 lo explica en el informe, §5.3 y nota ¹ de §5.2, y en la especificación, E4. C4 añade en E2 una matriz de coherencia entre margen, reinversión y ancla de S2C.

**Prueba:** `contraste_f1.json → S2C_anclada_en_C53`.

### O5 · premisa de arrendamientos y práctica de Elis · **aceptada y corregida** (C3, C4)

**Qué se hizo:**
- C3: premisa (iv) explícita [I] y conclusión «[D, condicionada a la premisa iv]». Cita la práctica de Elis en sus pruebas de deterioro [P].
- C4 busca evidencia contraria (§5.3):
  - el estado de flujos no tiene capex por derechos de uso [P];
  - las mejoras en locales arrendados son inmovilizado propio [I];
  - los arrendamientos de bajo valor (2,0), a corto plazo (5,9) y variables (0,9) van a gasto, dentro del margen y fuera del ROU [P].

  No se encontró evidencia contra la premisa.

**Pruebas:** `TXT_RENOV_ARR_2025`, `TXT_ARR_BAJO_VALOR_2025`, `TXT_ARR_CORTO_2025` y `TXT_ARR_VARIABLE_2025`, todas OK.

### O6 · evidencia contra la D&A propia como caso central · **aceptada y corregida** (C3)

**[P]** Plan climático con inversión superior a la amortización histórica; inversiones futuras adicionales; señales de contención del capex en 2025. **[I]** No demuestran infrainversión.

**Qué se hizo.** El plan climático figura en §9 como tercer tipo de inversión, pendiente de definición.

**Pruebas:** `TXT_PLAN_CLIMA_A/B/FR`, `TXT_INVERSIONES_FUTURAS` y `TXT_CAPEX_CONTROL/CONTENIDO/NORMAL/ESTABLE`. La frase del URD 2025 p.369 está partida entre columnas y se verifica en dos fragmentos.

### O7 · fiscalidad y agotamiento de los intangibles adquiridos · **aceptada y corregida** (C3; C4 hace reproducible el cálculo)

**Qué se hizo:**
- [I] «Mayoritariamente no deducible»: el ingreso por diferido de intangibles es el 18,3 / 24,2 / 21,0 % de la amortización de relaciones con clientes (84,6 / 83,9 / 83,5) [P][D]. La fila incluye también marcas y otros intangibles.
- [P] Las altas de 2025 (3,7) son provisionales; precedente: las de 2024 pasaron de 18,0 a 32,3.
- [D] Agotamiento: 275,1 ÷ 83,5 = 3,3 años sin compras nuevas, aunque la amortización no caerá de golpe.
- C4 calcula los ratios y el agotamiento en `contraste_f1.py`, tabla `impuestos`.

**Pruebas:** `TXT_ALTAS_PROVIS`; `INT_RC_COMB_FR_2024` (18,0, edición anterior) e `INT_RC_COMB_2024` (32,3, vigente); `TAXDIF_INT_2023`…`2025` (edición vigente: la única publicación que presenta el movimiento de cada año); `INT_RC_AM_*` e `INT_RC_VNC_2025`.

### O8 · crecimiento orgánico neto de bajas como evidencia sobre la PPA · **aceptada y corregida** (C3)

**Qué se hizo:**
- [I] §6.3 enlaza el crecimiento orgánico como evidencia parcial contra la reposición monetaria de la PPA en la ventana, no para el futuro.
- [P] Contratos de cuatro años; bajada cualitativa de la tasa de pérdidas en 2024.
- [D] Compensación numérica: A0 ≈ B − PPA.
- La conclusión «requiere decisión de política» no cambia.

**Pruebas:** `TXT_CONTRATOS_4A` y `TXT_PERDIDAS_2024`.

### O9 · partidas puntuales y límites de las referencias · **aceptada y corregida** (C3, C4)

**Qué se hizo:**
- C3 [D]: +27,9 en el flujo sin crecimiento (+13,7 / −4,0 / +18,3), común a todos los perímetros. Salvedad en el resumen, M1, §9 y E8.4.
- C4 escribe en la especificación (E9) los límites de los valores de referencia:
  - son valores de prueba de una implementación;
  - incluyen esas partidas sin normalizar;
  - usan las palancas actuales;
  - en A3 son sintéticos;
  - no son valores por acción.

**Pruebas:** `contraste_f1.json → partidas_puntuales_en_flujo_sin_crecimiento`; `TXT_SEGUROS_2025`.

### O10 · tendencia de los arrendamientos · **aceptada y corregida** (C3)

**[D]** Pagos de 2025 frente a los escalados: 16,8 menos. ROU de 2025 sin devolver en A1 y A2: 10,1. Es una limitación de proyectar una razón constante.

**Prueba:** `contraste_f1.json → arrendamientos_tendencia`.

### O11 · deuda constante con cuatro límites · **aceptada y corregida** (C3)

**Qué se hizo.** §8 recoge los cuatro límites:
- asimetría de los arrendamientos;
- intereses al alza;
- deuda bruta y caja;
- devengo de la OCEANE.

Se conserva E6.

**Pruebas:** `TXT_REFIN_TIPOS` y `TXT_OCEANE_DEVENGO`; residuo R19 de deuda neta dentro de su cota.

### O12 · perímetro del margen; estado y umbral de V-F1a · **aceptada y corregida** (C3; C4 añade la coherencia con la reinversión y con S2C)

**Qué se hizo:**
- C3:
  - parámetro `perimetro_margen` y regla V-F1h;
  - V-F1a pasa a «MODELO NO APLICABLE», con un umbral configurable (0,5 % propuesto, no adoptado);
  - identificador V-F1g para el aviso de E4;
  - variante orgánica de C53 declarada nominal o deflactada.
- C4: matriz de coherencia en E2, que cruza `perimetro_reinversion`, `perimetro_margen`, f y el ancla de la palanca S2C.

**Prueba:** criterio T8 de la especificación. Las reglas solo se pueden ejecutar cuando el frente técnico las implemente: aquí quedan especificadas, no probadas.

### O13 · referencias de los flujos y prueba de A3 · **aceptada y corregida** (C3, C4)

**Qué se hizo:**
- C3: flujos de los años 1–11 de A1 y A2 con las palancas actuales; T3b.
- C4:
  - separa los años 1–10 del año 11 terminal (`A1_A2_flujos_detalle`);
  - añade un control negativo por escenario y perímetro: si el terminal conserva la f de A0, el año 11 se desvía en V₁₀·(1+g)·(f_A0 − f_k), distinto de cero;
  - hace ejecutable la prueba de A3 con tres estimaciones sintéticas, que no son datos de Elis:
    - D_X = capex propio reproduce la cota B;
    - D_X = D&A propia reproduce A2;
    - el punto medio da f = 0,008263813331969 y un flujo sin crecimiento de 408,794140209212 (`A3_estimado_sintetico`).

**Pruebas:** 4 comprobaciones de A3 y 6 de la implementación parcial en `contraste_f1.py`; especificación T2, T3 y T3b.

## Forma

### O14 · «33 flujos» · **aceptada y corregida** (C3)

§4.3 dice ahora «30 flujos anuales», más los 3 del año 11.

### O15 · identidad del exceso de caja · **aceptada y corregida** (C3, C4)

**Qué se hizo:**
- C3 corrigió la identidad a (BL − C76)·r.
- C4 usa el término exacto de la fórmula de Motor!BL, BL = C·(D·(1 − K) − L)/J + M, con M = Análisis!C76 en el motor A. La comprueba con un exceso de caja distinto de cero de dos formas:
  - **algebraica:** con 0, 250 y −80. La identidad anterior se desvía en M·(r − 1), −227,5 con 250;
  - **sobre una copia temporal del libro recalculada con LibreOffice,** con C76 = 0, 250 y −80. En los tres escenarios, M = C76 y (BL − M)·r = 248,496395342656. El libro original no cambia: se comprueba su SHA-256 antes y después.

**Pruebas:** `prueba_caja_no_nula.py` → `caja_no_nula.json`; 18 comprobaciones de clase «libro» y 5 algebraicas; especificación T13.

### O16 · README, nombre del caso y `KeyError` · **aceptada y corregida** (C3, C4)

**Qué se hizo.** C3 separó las clases de comprobaciones en el README, renombró el caso y quitó el `KeyError`. C4 actualiza el README a las cinco dimensiones.

**Prueba:** caso «fuente sin huella declarada: diagnóstico controlado», que exige el motivo «no declara SHA-256».

### O17 · nota de §5.2 · **aceptada y corregida** (C3)

**[D]** El exceso exacto en la base 2025 es 139,4.

**Prueba:** `contraste_f1.json → arrendamientos_exceso_exacto_base_2025`.

## Respuesta al contraste externo (revision_chatgpt_1)

| Punto | Respuesta |
|---|---|
| O1 confirmado en el URD 2025 p.137, como proporción parcial | Coincide con lo incorporado en C3. Se mantienen los límites que señala: no es dos tercios de todo el capex ni resuelve la reinversión necesaria. C4 concreta lo pendiente (M1, a–d) |
| O2 confirmado en el URD 2025 p.122; C2 ya había corregido el volumen | C3 añadió el precio sin repetir lo de C2. El texto separa existencia y cuantificación |
| O3 reproducido sobre C2 (683/683, 129/129, residuos de ±17,3; año, unidad y perímetro falsos; `KeyError`) | Corregido en C4: ver O3. Sobre C4, los mutantes del revisor se rechazan en su dimensión. Si se salta el verificador, los residuos R6 y R16 de 2025 hacen fallar el cálculo |
| No adoptar sin más la tolerancia de ±0,15 | No se adopta: hay una cota de redondeo por identidad, fundada en la precisión impresa y en el número de cifras agregadas |
| Las excepciones −0,2 y +0,4 requieren explicación identificada y verificable, sin absorber errores nuevos | −0,2: dentro de su cota (0,35), ya no es excepción. +0,4: diferencia de concepto fijada en su valor exacto (± 0,15); dos casos de `test_contraste_residuos.py` prueban que un error nuevo en sus cifras la hace fallar |
| El mutante de año debe cambiar a la vez la posición y el literal | Así es en M1 y en los demás mutantes coherentes del test. El caso exige que el literal siga siendo el impreso y que solo falle la dimensión señalada |
| Conservar C48 = 108 y E1/D3/E2/E6; no implementar una alternativa ni valorar | Se conservan; ninguna alternativa se adopta, no hay valoraciones por acción y no se modifica el producto |

## Lo que queda abierto

- **Decisión F1** (a, b o c, con política completa) [DH pendiente].
- **Política de los intangibles adquiridos** (PPA) [DH pendiente].
- **Dato, o estimación documentada, de la reinversión necesaria:** M1, a–d, y M2. Sin él, la conclusión de nivel de Elis sigue `pendiente_de_datos`.
- **Perímetro declarado de la palanca S2C y del margen objetivo** (E2 y E4) [DH pendiente].
- **14 filas PENDIENTE de unidad** (URD 2022 p.302): no las usa ningún cálculo. Se acreditarían con otra presentación de la misma tabla que imprima la unidad.
- **Causa del +0,4 de 2025:** no se publica; es inmaterial.
- **Revisión independiente** de lo afectado, sobre el commit congelado que contiene C4: pendiente ([ESTADO.md](ESTADO.md)).
- **Integración, regeneración de expedientes, réplica y auditoría final** con el frente técnico: posteriores.

Nada de lo anterior declara aptitud para dinero real.
