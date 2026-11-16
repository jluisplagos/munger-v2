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
| C6 | f30c66c8651dba134b4e66fff9a08c2b50359b6c (también en [ESTADO.md](ESTADO.md)) | Adenda tras las sondas externas sobre eb77dea: columna de la matriz por segmentos para el perímetro declarado; tres casos de test; sondas de un solo campo en todas las filas (`sondas_metadatos.py`) |
| C7 | 9869def325b8820e2ee25618107495a7a7b70229 (también en [ESTADO.md](ESTADO.md)) | Respuesta a la revisión n.º 3 y su adenda: lista cerrada de modos; columna identificada por su cabecera; dimensión «columna»; contraejemplos de unidad y perímetro; huella de la verificación; 109 residuos, también en 2021–22; cobertura de todas las entradas usadas y su prueba de mutación; scripts del revisor sobre C7 |
| C8 | 97441770f51761e28c089df7830d3de802bf87e9 | Registra el hash de C7. Congelado de la revisión n.º 4 |
| C9 | c8764494d9911c59a67a530f13b56616fe86707c | Segunda presentación de cinco entradas del ancla de S2C (R17, R39 y R40 de 2021–22); hueco del verificador hallado por el autor: columnas por país. Sin revisar (tercera parte) |
| C10 | 95b37e6da22bd4d5adb55c3f09c729b8d4e409f1 (también en [ESTADO.md](ESTADO.md)) | Respuesta a la revisión n.º 4 (P1–P5): criterio de formato de recuento, título de país o de segmento sobre la tabla, páginas sin identidad entre páginas, precisiones de forma (cuarta parte) |
| C11 | 364129afd45ba2e54a1df4141fd50e97fd55ef6d | Registra el hash de C10. Congelado de la revisión n.º 5 |
| C12 | 4f3f9ba9c8240143269368c41787736b3867e97b (también en [ESTADO.md](ESTADO.md)) | Respuesta a la revisión n.º 5 (Q1–Q7): columnas del mismo año y de apertura, columna «published», celdas y llamadas de la cabecera, título del bloque hasta la página anterior, rótulos de segmento normalizados, R41, R8 de 2021–22, R24 de 2023 y R42 (quinta parte) |
| C13 | 1b80b5d5348e6e39dd1d632cafbbbf4e5dd3685a | Registra el hash de C12. Congelado de la revisión n.º 6 |
| C14 | El hash consta en el congelado siguiente (C15) y en [ESTADO.md](ESTADO.md) | Respuesta a la revisión n.º 6 (R1–R8): asignación por orden con alineación, cabecera de la propia tabla, grupos de columnas por entidad, filas de jurisdicción, encabezados numerados, título corto de tabla, prefijo de UGE, FALLO solo con la columna alineada, ventas de 2021–22 por segmentos (R23) y umbrales de detección (sexta parte) |

## Marcas y pruebas

**Marcas de evidencia:** [P] dato publicado · [D] derivación · [I] interpretación · [H] hipótesis · [DH] decisión humana.

**Pruebas que se citan** (todas en `scripts/`; las salidas, en `resultados/`):
- `verificar_cifras.py`: estado de cada fila en cinco dimensiones (`verificacion_cifras.json`);
- `test_verificar_cifras.py`: 42 casos (`test_verificar_cifras.log`);
- `sondas_metadatos.py`: sondas de un solo campo, unidad o perímetro, en todas las filas (`sondas_metadatos_eb77dea.json`, `sondas_metadatos_1864c4e.json`, `sondas_metadatos_C6.json`);
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
5. **Mutantes conjuntos**, en `test_verificar_cifras.py` (42 casos tras C6). Se mantienen los 16 anteriores, el manual justificado pasa a exigirse PENDIENTE y se añaden positivos reales y mutantes:
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
- `test_verificar_cifras.py` 42/42 y `test_contraste_residuos.py` 7/7;
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

## Sondas externas de un solo campo sobre eb77dea · **confirmadas; corregidas en C4 y completadas en C6**

**Evidencia externa:** `revision_chatgpt_1/seguimiento_eb77dea/` de la rama `auditoria/economica-f1` (commit e57239c). Sobre eb77dea, con los años correctos, cambiar un solo campo pasaba con código 0 y 707/707:
- solo la unidad de `CREC_ORG_2025` («%» → «mm EUR»);
- o solo el perímetro de `IS_VENTAS_2025` (→ «segmento Francia»).

El rechazo de M4 se debía solo a su año.

**Reproducción del autor** (`scripts/sondas_metadatos.py`): las mismas dos mutaciones y su extensión a todas las filas de tabla, un campo cada vez. Se ejecuta con el verificador y los datos de cada versión:

| Versión | Unidad cambiada en cada fila | Perímetro cambiado en cada fila | Las dos sondas externas |
|---|---|---|---|
| eb77dea (C3) | 0 de 671 detectadas | 0 de 671 | Pasan (código 0) |
| 1864c4e (C4, congelado) | 677 de 677, todas en la dimensión unidad | 673 de 677. Las 4 sin detectar son totales de una matriz por segmentos declarados «segmento Francia»: quedaban PENDIENTE en lugar de FALLO | Rechazadas (código 1) |
| C6 | 677 de 677 | 677 de 677 | Rechazadas |

**¿Hay otra vía independiente y trazable que acredite estos campos?**
- **En eb77dea, no.** La unidad y el perímetro eran campos declarados: el verificador no los leía y `contraste_f1.py` no los usaba. Las comparaciones con la Historia del libro y los residuos acreditan magnitudes, no etiquetas: si se cambia la etiqueta y la cifra queda intacta, ningún cálculo cambia y ninguna de esas vías lo detecta. Su cobertura en eb77dea estaba pendiente.
- **Desde C4, la vía es el propio PDF**, independiente de lo declarado y trazada fila a fila en `verificacion_cifras.json`, en las dimensiones `unidad` y `perimetro`, con su motivo:
  - **unidad:** la declaración de unidades más próxima por encima de la línea, como «(In millions of euros)» o «(en millions d'euros)», incluida la partida en dos líneas, cuya línea queda anotada; o el «%» del literal;
  - **perímetro:** la cabecera de la página (estados consolidados o resultados del grupo), el rótulo de la línea (segmentos) y, en las matrices por segmentos, la columna del token, que C6 identifica por el orden horizontal de las ocho cabeceras.
- **Barrera adicional:** `contraste_f1.py` rechaza una entrada si su unidad o su perímetro declarados no son los que pide el cálculo.
- **Vía de magnitud,** no de etiqueta: la Historia del libro y los residuos entre páginas. Una cifra en miles o de un segmento romperían esas comparaciones.

**Cobertura pendiente o limitada, que se declara:**
- 14 filas sin unidad impresa (URD 2022 p.302) quedan PENDIENTE. Ningún cálculo las usa.
- El perímetro del grupo se acredita por la cabecera de cada página, no de cada tabla. Una tabla de otro perímetro, sin rótulos de segmento, en una página consolidada no se detectaría [límite]. Ninguna de las filas usadas está en ese caso: todas tienen su segunda presentación o su comparación con el libro.
- La unidad se acredita por la declaración más próxima por encima de la línea. Una tabla sin declaración propia heredaría la de la tabla anterior de la misma página [límite].
- Fuera de las matrices de ocho columnas, un segmento solo se acredita por el rótulo de la línea.

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

---

# Respuesta a la revisión independiente n.º 3 y a su adenda

**Revisión:** [REVISION_INDEPENDIENTE_3.md](REVISION_INDEPENDIENTE_3.md) de la rama `auditoria/economica-f1-frente-e-revision`. El informe principal está en el commit 11b999a, sobre el congelado 1864c4e, y la adenda en el 034301c, sobre f30c66c (C6). Copia sin cambios y procedencia: [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).

**Resultado de la revisión:**
- O1, O2 y O4–O17, resueltas;
- O3, parcialmente resuelta, por N1–N3;
- objeciones nuevas: N1 (material), N2–N5 y N9–N10 (menores) y N6–N8 (forma);
- ninguna conclusión material cambia.

**Esta respuesta** acepta las diez objeciones y las corrige en **C7**: el commit que contiene esta sección, cuyo hash consta en [ESTADO.md](ESTADO.md). Las pruebas que se citan están en `scripts/` y sus salidas en `resultados/`. Los scripts del revisor de `revision/scripts_revisor_3/` se ejecutaron sin cambios sobre C7, con salida en `resultados/revisor3_*_sobre_C7.txt`. Algunas de sus pruebas no pueden medir C7 tal como están escritas: entregan al contraste la verificación de otro CSV, que C7 rechaza (N3), o declaran modos fuera de la lista cerrada (N1). Se explica en «Los scripts del revisor sobre C7», al final de esta parte.

## N1 · material · el verificador daba OK a cifras incorrectas · **aceptada y corregida** (C7)

Cada caso del revisor y lo que hace ahora `verificar_cifras.py`:

| Caso del revisor | Corrección en C7 | Resultado sobre C7 |
|---|---|---|
| F1–F3: tabla con una tercera columna «Change» | En el modo por defecto, la columna del token ya no se supone por su posición. Se identifica con su cabecera: por orden, si la cabecera tiene tantas columnas reconocidas (años, «Change», «Notes») como números la línea; si no, por alineación horizontal. Si el token no queda bajo un ejercicio, la fila queda PENDIENTE o FALLO, nunca OK | F1, FALLO en ejercicio; F2 y F3, los valores correctos, OK |
| A1, A2, A4, H1: modo declarado | El modo es una lista cerrada por concepto (`modo_admitido`), la misma para el constructor del CSV y para el verificador. Otro modo es FALLO. «crecimiento» solo admite porcentajes y «max_cabecera» exige fechas de apertura y cierre en la cabecera | FALLO en ejercicio |
| D1, D2: concepto de la columna | Nueva dimensión `columna`. En las tablas de varias columnas que no son ejercicios, la cabecera de la columna del token debe ser la del concepto. Abarca crecimiento, impuestos diferidos, arrendamientos, intangibles, inmovilizado y matrices | FALLO en columna. También el activo ROU declarado como pasivo |
| B1, B2: acciones y beneficio por acción | Las líneas cuyo rótulo está en la lista de recuentos, importes por acción, márgenes, años o euros no pueden ser «mm EUR». *(Precisión de C12, revisión n.º 5, Q7 c: la lista no cubre la clase entera; desde C10 la completa el criterio de formato de recuento.)* Además, una declaración de otra unidad corta la búsqueda, y una declaración de otra tabla deja la fila PENDIENTE | FALLO en unidad |
| C1: margen de Francia | Una sublínea («As a % of revenue», «of which») bajo el rótulo de un segmento, en una tabla por segmentos, no es del grupo | FALLO en perímetro. El margen del grupo, bajo el TOTAL, queda OK |
| H5: otra línea de la misma tabla | El concepto de la línea no lo acredita el verificador: la etiqueta es una declaración. Lo acredita una identidad (N2): R25 y R16 de 2022 hacen fallar el cálculo | Lo detecta el contraste (`test_contraste_residuos.py`) |

**Lo que significa OK** (N1, corrección 5; N8 a). El informe dice ahora que OK significa «ninguna incoherencia detectada por las reglas automáticas en esa dimensión», no «acreditada». El concepto de la línea lo acreditan una identidad, el libro o una lectura independiente.

**Datos reales:** las 736 filas quedan en 722 OK, 14 PENDIENTE y 0 FALLO. Ninguna fila real cambia de estado con las reglas nuevas.

**Pruebas:**
- `test_verificar_cifras.py` 63/63: 13 positivos reales, 1 PENDIENTE y 49 contraejemplos, con todos los de N1 y de la adenda;
- `prueba_mutantes_3.py` del revisor, sin cambios, sobre C7: todos los mutantes de N1 en FALLO en su dimensión, y F2 y F3 en OK;
- especificación T14.

## N2 · menor · entradas con efecto sin segunda línea · **aceptada y corregida** (C7)

**Identidades nuevas** (de 71 a 109 residuos afirmados, cada uno con su cota):
- en 2021 y 2022:
  - R25, componentes de la D&A frente al total;
  - R16, amortización ROU de la nota frente al movimiento de arrendamientos;
  - R22, PPA de la cuenta de resultados frente a la nota;
  - R34, capex por tipo;
  - R35, EBIT;
  - R36, free cash flow publicado;
  - R32, composición del crecimiento (solo 2022);
  - R5, circulante del APM frente a las líneas del EFE, añadida tras la prueba de mutación (abajo).
  Las cuatro entradas sin detectar que fijaban el C53 de referencia (amortización ROU y PPA de 2021 y 2022) ya tienen segunda línea;
- en 2023–2025: R29 y R30, totales de los flujos de inversión y de financiación; R31, capex neto entre la tabla de capex y la del FCF; R32, crecimiento publicado frente a orgánico + externo + divisa; R33, resultado neto; R37, impuesto de la conciliación del tipo; R38, otros ingresos y gastos operativos (2024–25);
- entre ediciones: R26, R27 y R28, cierre de 2023 en el DEU 2024 frente a apertura de 2024 en el URD 2025 (ROU, pasivo y relaciones con clientes). Responden también a N8 f.

**Cobertura de todas las entradas usadas** (`cobertura_entradas`), no solo de las clave. Clasifica las 402 en cuatro grupos:

| Estado | Entradas |
|---|---|
| Contrastadas entre páginas | 211 |
| Solo identidad de la misma página | 151 |
| Solo Historia del libro | 9 |
| Sin segunda línea | 31 |

La clasificación se hace al final del cálculo, y una aserción exige que abarque todas las entradas usadas. En un borrador de C7 se hacía antes de la sección de impuestos y dejaba fuera cuatro.

Las 31 sin segunda línea se listan con sus usos:
- de la tabla de impuestos, que sostienen el [I] de O7: diferido por naturaleza (9), CVAE/IRAP (3) y amortización (3) y valor neto contable (1) de las relaciones con clientes;
- componentes de otros ingresos y gastos operativos (6). `OOIE_PLUSV_2025` entra en el +18,3 de las partidas puntuales;
- OCEANE (3);
- interés devengado de arrendamientos de 2021–22 (2), cesiones de 2021–22 (2), pagos en acciones del EFE de 2021 (1) y crecimiento orgánico de 2021 (1).

Para ellas valen las reglas del verificador y su literal, y el informe lo dice donde se citan.

**Cobertura por mutación** (`scripts/cobertura_por_mutacion.py`; salida en `resultados/cobertura_por_mutacion.txt`).
- Es el script del revisor con un solo cambio: la verificación falsa, que declara OK todas las filas, corresponde a cada CSV mutado.
- El del revisor, sin cambios, entrega a cada CSV mutado la verificación del original. C7 la rechaza (N3), y sus 514 mutaciones terminan en «aborta» (`resultados/revisor3_cobertura_por_mutacion_sobre_C7.txt`).

Cada una de las 514 filas de tabla de la edición vigente se altera en +3,0:

| Cobertura declarada | Resultado de la mutación | Entradas |
|---|---|---|
| Entre páginas | Falla una identidad de fuente | 211 |
| Solo misma página | Falla una identidad de fuente | 151 |
| Solo Historia del libro | Solo falla la comparación con el libro | 9 |
| Sin segunda línea | Cambia alguna salida y no falla nada | 23 |
| Sin segunda línea | No cambia ninguna salida | 8 |
| No usada | No cambia ninguna salida | 112 |

- **Ninguna incoherencia.** Ninguna entrada declarada con una comprobación escapa a ella, y ninguna entrada con efecto falta de la tabla.
- **Las 23 sin detectar no cambian la referencia de la especificación.** Cambian las tablas de impuestos (16), financiación (3), arrendamientos (2) y partidas puntuales (1). El crecimiento orgánico de 2021 cambia las de alternativas y horizonte.
- **Las 8 sin efecto** son cesiones de 2021–22 (2), pagos en acciones del EFE de 2021 (1) y, de la nota de otros ingresos y gastos operativos, el earn-out de 2023–25 (3) y las plusvalías de 2023–24 (2). El cálculo solo usa la plusvalía de 2025 de esa nota. El earn-out y las plusvalías que entran en f son los del EFE, que comprueba R3.
- **Lo que corrigió la prueba.** La primera pasada sobre C7 encontró 14 líneas de circulante de 2021–22 que entran en el C53 de referencia y solo tenían la Historia del libro. Se añadió R5 para 2021–22 con el circulante del APM, que ya estaba registrado y verificado (URD 2022 p.250 y URD 2023 p.268). Residuos: +0,1 y 0,0, cota 0,40. No cambia ningún valor de referencia.
- **Lo que queda.** Cinco entradas cambian la referencia y solo se comparan con la Historia del libro: adquisiciones e impuesto de 2021 y 2022 y ventas de 2020. La Historia es otra transcripción de las mismas publicaciones: no protege de un error común a las dos lecturas.

**Pruebas:**
- `contraste_f1.json` → `residuos_con_cota`, `cobertura_entradas`;
- `test_contraste_residuos.py` 14/14, con H5 y D2 detectados por R25, R16 y R32, y una línea del circulante de 2021 por R5;
- `cobertura_por_mutacion.py`, arriba.

**Límites de las referencias de E9:** se declara de qué entradas depende el C53.

## N3 · menor · verificación que no corresponde al CSV · **aceptada y corregida** (C7)

`verificar_cifras.py` guarda en su salida la huella SHA-256 del CSV y de `fuentes.json`, y el literal y el valor de cada fila. `contraste_f1.py` no calcula si la huella del CSV no es la verificada, ni si el literal o el valor de una fila no son los verificados.

**Pruebas:** caso H2 de `test_contraste_residuos.py`, en el que el contraste termina con código 1 y el motivo «la verificación no corresponde a este CSV»; H2 de `prueba_mutantes_3b.py` del revisor sobre C7, con el mismo resultado.

## N4 · menor · dos combinaciones de la matriz de coherencia sin fórmula · **aceptada y corregida** (C7)

Se retiran de las combinaciones admisibles y quedan en V-F1h hasta que se especifiquen con su fórmula y su prueba:
- `margen_despues_de_arrendamientos`: A1′ solo quita el principal y el interés de arrendamiento seguiría en C48 y en f;
- `EBIT_NIIF16_PPA_decreciente` con `A2_propio`: exigiría una f que varíe con el tiempo.

La vía que propone el revisor queda descrita como posible definición futura, sin adoptarla: calibrar f con el NOPAT sobre el mismo margen que se proyecta.

**Prueba:** especificación E2 y T8.

## N5 · menor · A3 sin ancla ni flujos de referencia · **aceptada y corregida** (C7)

`A3_estimado_sintetico` da para cada caso sintético el C53 y los flujos de los años 1–10 y del año 11 con las palancas actuales. Los C53 son 2,651525243106, 1,612524303305 y 2,005440531963, el del punto medio: coinciden con los del revisor.

**Prueba:** comprobación «A3 sintético, punto medio: C53 entre los de A2 y B»; especificación T3b.

## N6 · forma · afirmaciones sobre los residuos más fuertes que la prueba · **aceptada y corregida** (C7)

1. §5.4 y estas respuestas dicen ahora que la diferencia fijada solo detecta un error neto mayor que 0,15. Con el gasto devengado en 29,3 o en 29,1, o con los pagos en 178,0, R13 pasa: es su límite de detección. Tres casos de `test_contraste_residuos.py` lo documentan (H3a–H3c), y otro comprueba que 29,5 sí falla (H4). Ningún otro residuo los detecta: R11 y R12, que también usan los pagos, tienen cotas de 0,35 y 0,25. *(Precisión de C10, revisión n.º 4, P4:)* el de los pagos, H3c, sí lo detectan la doble vía del FCF base, que es una comprobación de fuente, y 41 comprobaciones del libro.
2. R16 de 2023 (−0,1 con cota 0,10) se muestra en la tabla de §2, con su causa [P]: la amortización ROU de 2023 se imprime como 115,8 en la nota 4.5 (DEU 2024 p.296) y como 115,9 en el movimiento de arrendamientos (p.312). E1 fija la nota 4.5 como fuente.

## N7 · forma · «359 entradas» · **aceptada y corregida** (C7)

§1 da las entradas que el cálculo lee: 402 en C7. Distingue también las que tienen efecto en alguna salida: 320 según el revisor sobre 1864c4e y, sobre C7, 394 según la prueba de mutación, más 8 que se leen sin efecto (N2).

## N8 · forma · varios · **aceptada y corregida** (C6, C7)

- **(a)** Ver N1, «Lo que significa OK».
- **(b)** §0.6: Elis cuenta el arrendamiento una sola vez, como renovación dentro de la inversión (el esquema de A1′). No respalda literalmente que el coste sean los pagos.
- **(c)** Recuentos del test: positivos, PENDIENTE esperado y contraejemplos por separado.
- **(d)** T2 y T3 dan los desvíos del año 11 de la implementación parcial: 166,6 / 205,4 / 223,9 (A1) y 274,1 / 337,8 / 368,3 (A2).
- **(e)** Corregida en C6.
- **(f)** Regla de los saldos: cada movimiento se concilia con la tabla de su propio bloque. Si el cierre de un ejercicio y la apertura del siguiente difieren entre publicaciones, prevalece la más reciente para el saldo como dato, y la diferencia se muestra como reexpresión. R26–R28 lo comprueban: hoy coinciden (513,7, 538,3 y 414,9).

## N9 · menor · `columna_de_matriz` contaba desde la derecha · **aceptada y corregida** (C7)

La columna se asigna por la posición horizontal del token respecto a las ocho cabeceras. Con ocho números, la cuenta desde la derecha debe coincidir; si no coincide, la fila queda PENDIENTE.

**Pruebas:** casos X1 (margen de Francia declarado «segmento Europa central»: FALLO) y X2 (declarado «segmento Francia»: OK) del test.

## N10 · menor · las sondas presentadas como cobertura · **aceptada y corregida** (C7)

**Qué miden las sondas.** Que una etiqueta cambiada se detecta. No que una cifra de otra unidad o de otro perímetro con una etiqueta verosímil se rechace. Así se dice ahora en el informe §1, en T12 y en la sección de sondas de estas respuestas.

**Contraejemplos de la adenda:** esos casos, que eran OK, quedan ahora en FALLO y forman parte del test y de T14. *(Precisión de C10, revisión n.º 4, P5:)* su clase no queda cerrada: otras filas de la misma clase sin las señales de las listas pasaban (P1 y P2 de la revisión n.º 4):
- **P1**, tabla por países;
- **P2a**, fila «Other» en una tabla por segmentos;
- **U1 y U2**, recuentos de acciones;
- **C1**, sublínea de un segmento.

P2b (la fila «Other» declarada «segmento Otros segmentos») pasa a OK.

**Corrección de una frase.** La de estas respuestas sobre la cobertura de las filas usadas era inexacta: 31 entradas usadas no tienen segunda línea (N2). Se corrige abajo.

**Corrección a la sección «Sondas externas de un solo campo sobre eb77dea»:** donde dice «todas tienen su segunda presentación o su comparación con el libro», debe decir que, de las entradas usadas, 31 no tienen ni identidad ni comparación con el libro (lista en `cobertura_entradas`).

## Los scripts del revisor sobre C7

Se ejecutaron sin cambios. Salidas en `resultados/`:

| Script | Salida | Resultado sobre C7 |
|---|---|---|
| `prueba_mutantes.py` (revisión n.º 1) | `mutantes_revisor_sobre_C7.txt` | M1–M4 en FALLO en su dimensión |
| `prueba_mutantes_3.py` | `revisor3_prueba_mutantes_3_sobre_C7.txt` | Todos los mutantes de N1 en FALLO en su dimensión. F2 y F3, los valores correctos, en OK |
| `prueba_mutantes_3b.py` | `revisor3_prueba_mutantes_3b_sobre_C7.txt` | H1, FALLO en ejercicio, y el contraste no calcula. H2: el contraste se niega. H5: fallan R25 y R16 de 2022. **H3a–H3c y H4 no miden lo que pretenden** (abajo) |
| `sondas_revisor.py` | `revisor3_sondas_sobre_C7.txt` | Unidad y perímetro cambiados en cada fila: 697 de 697 detectados, en la dimensión del campo. Con una etiqueta cambiada y una verificación de otro CSV, el contraste se niega. Contraejemplos: abajo |
| `cobertura_por_mutacion.py` | `revisor3_cobertura_por_mutacion_sobre_C7.txt` | 514 de 514 «aborta»: el contraste rechaza la verificación de otro CSV. La medida está en la adaptación del autor (N2) |

**H3a–H3c y H4 de `prueba_mutantes_3b.py`.**
- Entregan la verificación del CSV original a un CSV mutado. El contraste se niega y no escribe salida.
- El script lee entonces el `k.json` que dejó H5 en la misma carpeta temporal. Por eso los cuatro muestran los fallos de R25 y R16 de 2022 y un R13 sin mutar (0,4).
- Es un efecto del script, no de C7.
- Los mismos cuatro casos están en `test_contraste_residuos.py`, con la verificación falsa ligada al CSV mutado. H4 (29,5) hace fallar R13. H3a (29,3), H3b (29,1) y H3c (178,0) no los detecta ningún residuo, porque están dentro de la cota (N6). *(Precisión de C10, revisión n.º 4, P4:)* H3c lo detectan la doble vía del FCF base y 41 comprobaciones del libro, no «42 comprobaciones contra el libro».

**Contraejemplos de `sondas_revisor.py`.**
- P1, P2a, U1, U2 y X1: FALLO en la dimensión que deben.
- P2b y X2, los positivos: perímetro OK, pero FALLO en ejercicio. La sonda los crea con identificadores nuevos (`CE_…`) y les declara los modos «crecimiento» y «titulo». La lista cerrada de N1 asigna a un identificador desconocido el modo por defecto, «dos_columnas», y rechaza otro declarado. Es la defensa buscada contra el truco del modo (A1, A2, A4 y H1). Con identificadores de la lista cerrada, los mismos positivos quedan OK en el test (`MUT_OTHER_SEG` y `VENTAS_SEG_MARGEN_X2`).
- X3 y X4 (matriz del URD 2021 p.247 con cabeceras en otro orden): perímetro PENDIENTE en los dos, porque la columna no se puede acreditar. Ni el perímetro falso ni el correcto se aceptan.
- X5, el total de esa matriz: perímetro OK y columna PENDIENTE.
- Ninguna fila real del CSV procede de esa matriz.

## Lo que queda abierto tras C7

- **Revisión independiente de lo afectado por C7**, sobre un commit congelado: pendiente ([ESTADO.md](ESTADO.md)).
- **31 entradas usadas sin segunda línea** (N2), listadas. Ninguna cambia la referencia de la especificación. Para ellas valen el literal y las reglas automáticas.
- **5 entradas que cambian la referencia de la especificación con la Historia del libro como única segunda línea** (N2): adquisiciones e impuesto de 2021 y 2022 y ventas de 2020.
- **14 filas PENDIENTE** (URD 2022 p.302: el verificador no encuentra ni la unidad ni la cabecera de columnas). Una de ellas, `LS_AMORT_ROU_2021`, solo se usa como contraparte de R16 de 2021, y cuadra con la nota de D&A.
- **Lo económico no cambia:** decisión F1, política de la PPA, dato o estimación de la reinversión necesaria (M1 a–d, M2) y perímetros declarados de S2C y del margen, todos [DH] pendientes. Sin aptitud para dinero real.

# Cambios del autor tras el congelado C8 (C9)

No responden a ninguna objeción. Se hicieron mientras la revisión n.º 4 trabajaba sobre C8. **No están revisados**: entran en la pasada siguiente, junto con la respuesta a la n.º 4.

**Cronología.**
- El hueco del verificador descrito abajo lo encontré hacia las 22:05 UTC, al probar contraejemplos de las filas nuevas, sin haber leído el informe de la revisión n.º 4.
- Ese informe se publicó a las 22:04 UTC (commit a15f706 de la rama del revisor), antes que este commit, así que git no puede acreditar el orden.
- Si la revisión n.º 4 señala el mismo hueco, cuenta como hallazgo del revisor.

## Segunda presentación de cinco entradas del ancla de S2C

Tras C7, cinco entradas que cambian los valores de referencia de la especificación solo se comparaban con la Historia del libro: adquisiciones e impuesto de 2021 y 2022, y ventas de 2020 (N2, «Lo que queda»). C9 añade siete filas de las mismas publicaciones, verificadas en las seis dimensiones, y tres identidades del horizonte:

| Identidad | 2021 | 2022 | Páginas |
|---|---|---|---|
| R17 impuesto corriente + diferido (nota 9) − gasto por impuesto | 0,0 (cota 0,15) | 0,0 (cota 0,15) | URD 2022 p.258 y p.326; URD 2023 p.276 y p.345 |
| R39 adquisiciones del EFE − flujo neto total de la nota 2.4 | 0,0 (cota 0,10) | 0,0 (cota 0,10) | URD 2022 p.261 y p.277; URD 2023 p.279 y p.294 |
| R40 ventas de 2020: cuenta de resultados − informe de gestión | 0,0 (cota 0,10) | — | URD 2021 p.226 y p.213 |

- Los valores de referencia de E9 no cambian: C53 de A1 = 2,445331695332 y de A2 = 1,612524303305.
- [P] El informe de gestión del URD 2022 (p.247) imprime las adquisiciones de 2021 como (86,9) bajo la cabecera «2021 restated». Es la cifra publicada antes del ajuste IFRS 3 de 0,1: la tabla de reexpresión (p.271) da (86,9) + 0,1 = (86,8), la del EFE. Por eso R39 usa la nota 2.4.
- **Límite:** 0,1 queda dentro de la cota de R39, así que ninguna identidad distingue la cifra publicada de la reexpresada. Lo documenta un caso de `test_contraste_residuos.py`.

## Hueco del verificador encontrado por el autor

- **Qué.** Tabla de flujos de adquisiciones de la nota 2.4 del URD 2022 (p.277): una columna de total del ejercicio («12/31/2021») seguida de columnas por país. La cifra de Bélgica, contigua al total, declarada del grupo y de 2021, quedaba OK en las seis dimensiones:
  - el ejercicio se asignaba por alineación a la única columna de ejercicio de la cabecera, aunque el token estuviera más cerca de «Belgium»;
  - el perímetro no miraba las columnas por país.
- **Alcance.** Existe en C7 y en C8, el congelado de la revisión n.º 4. Ninguna fila real lo aprovechaba: ninguna procedía de una tabla así antes de C9, y las de C9 toman la columna del total.
- **Corrección:**
  - ejercicio: si una palabra de la cabecera que no es una columna reconocida (un país, una sociedad, un ajuste) está más cerca del token que la columna del ejercicio, el ejercicio queda PENDIENTE. Solo se aplica a las columnas de ejercicio; en las de concepto la cabecera es una frase y solo una palabra casa con la clave;
  - perímetro: en una tabla con tres países o más en la cabecera, la columna de un país no es del grupo (FALLO).
- **Pruebas:**
  - 4 casos nuevos en `test_verificar_cifras.py` (67/67): el total, OK; Bélgica y Suecia, FALLO en perímetro; una sociedad adquirida (URD 2023 p.294), PENDIENTE;
  - las 736 filas anteriores no cambian de estado en ninguna dimensión;
  - los scripts del revisor, sin cambios, dan sobre C9 los mismos resultados que sobre C7, salvo los recuentos de filas (`resultados/*_sobre_C9.txt`).
- **Límite que queda:** las columnas por sociedad no se reconocen como tales. Quedan PENDIENTE en ejercicio, no FALLO en perímetro. *(Precisión de C12, revisión n.º 5, Q7 d:)* quedaban además dos clases, corregidas en C12: la columna «published» de las tablas de reexpresión (Q1) y la asignación por orden con dos fechas del mismo año (Q2). *(Precisión de C14, revisión n.º 6, R7 c:)* la frase vale para el caso del test, una sociedad adquirida (URD 2023 p.294), que sigue PENDIENTE. Tras C12, las columnas por marca, de la misma clase, quedaban OK (R1); desde C14 quedan PENDIENTE en perímetro por la regla de grupos de columnas, como las de las firmas auditoras.

## Resultados sobre C9

| Prueba | Resultado |
|---|---|
| Verificador | 743 filas: 729 OK, 14 PENDIENTE, 0 FALLO |
| `test_verificar_cifras.py` | 67/67 |
| Contraste | 280 comprobaciones (136 libro, 115 fuente con 114 residuos, 29 algebraicas), 0 fallidas; 409 entradas |
| Cobertura declarada | 223 entre páginas, 151 solo misma página, 4 solo Historia y 31 sin segunda línea. Ninguna de las dos últimas clases cambia la referencia |
| `test_contraste_residuos.py` | 18/18 |
| Mutación (521 filas vigentes) | 374 por identidad, 4 solo libro, 23 sin detectar, 8 leídas sin efecto y 112 no usadas; sin incoherencias |
| Sondas de un solo campo | 704/704 en unidad y en perímetro |
| Regeneración del CSV desde los PDF | Idéntico byte a byte |

## Lo que queda abierto tras C9

- **Revisión n.º 4** (sobre C8): publicada, pendiente de incorporar y responder.
- **Revisión de lo afectado por C9 y por esa respuesta:** pendiente.
- **Cobertura:** 31 entradas sin segunda línea y 4 solo con la Historia; ninguna cambia la referencia.
- **14 filas PENDIENTE** de URD 2022 p.302.
- **Columnas por sociedad:** PENDIENTE, no FALLO. *(Precisión de C14, R7 c: véase arriba.)*
- **Límites de detección por debajo de la cota:** R13 de 2025 y R39 de 2021.
- **Decisiones económicas [DH] y aptitud:** como tras C7. Sin aptitud para dinero real.

# Respuesta a la revisión independiente n.º 4

**Revisión:** [REVISION_INDEPENDIENTE_4.md](REVISION_INDEPENDIENTE_4.md). Commit a15f706 de la rama `auditoria/economica-f1-frente-e-revision` (22:04 UTC), sobre el congelado 97441770 (C8). Copia sin cambios y procedencia: [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).

**Resultado de la revisión:**
- reproduce todas las cifras del autor, con salidas idénticas;
- N2–N10, corregidas; N1, corregida en parte: las reglas de unidad y de perímetro son listas de rótulos;
- objeciones nuevas: P1–P3 (menores) y P4–P5 (forma);
- ninguna conclusión material cambia y no encuentra errores en los datos reales.

**Esta respuesta** acepta las cinco objeciones y las corrige en **C10**. El revisor no ha visto C9, cuyos cambios son posteriores a su congelado. C9 y C10 entran juntos en la pasada siguiente.

**Relación con C9.** La revisión no señala el hueco de las columnas por país corregido en C9. Su P2 es de la misma familia, un perímetro que se deduce de señales de la tabla, pero es otro caso: un título por encima de la tabla, no una columna.

## P1 · menor · un recuento sin rótulo de recuento pasaba como millones de euros · **aceptada y corregida** (C10)

- **Corrección.** Se aplica el criterio que no depende del rótulo, el primero que propone el revisor: un literal entero, sin parte decimal y con seis cifras o más, declarado en millones de euros queda PENDIENTE en unidad.
  - Queda PENDIENTE y no FALLO porque el formato sugiere un recuento, pero no lo prueba.
  - La segunda variante propuesta, cualquier línea cuyo formato no sea el de su tabla, no se implementa: exige inferir el formato de cada tabla y no tiene contraejemplo real. Queda como mejora posible.
- **Pruebas:**
  - los casos A1 y A2 del revisor quedan en PENDIENTE y su control A3, en FALLO (`resultados/revisor4_contraejemplos_4_sobre_C10.txt`);
  - dos casos nuevos en `test_verificar_cifras.py`;
  - ninguna de las 743 filas reales cambia de estado;
  - T14 incluye el criterio de formato.

## P2 · menor · el bloque de un país bajo su título pasaba como grupo · **aceptada y corregida** (C10)

- **Corrección.** Se aplica la primera de las dos vías propuestas. Se busca el título más próximo por encima de la tabla:
  - primero, lo que queda en la línea de unidades después de la declaración;
  - después, hacia arriba, la primera línea corta sin cifras.

  Si ese título nombra un país o un segmento («FRANCE – DETAILS»), el perímetro del grupo queda PENDIENTE. La segunda vía, el mismo rótulo en la página anterior con otro valor, no se implementa.
- **Pruebas:**
  - el caso B1 del revisor (pensiones de Francia, 45,2) queda en PENDIENTE, y sus controles B2 y B3, en FALLO;
  - un caso nuevo en el test y un positivo: el total por países de la misma página (67,1), bajo «INFORMATION BY REGION», sigue en OK;
  - ninguna fila real cambia de estado.
- **Límite:** no se detecta un bloque de otro perímetro sin título ni rótulo que lo nombre.

## P3 · menor · la identidad de la misma página no acredita la unidad ni el perímetro · **aceptada y corregida** (C10)

- `cobertura_entradas` dice ahora:
  - qué acredita cada clase;
  - si la página de cada entrada tiene alguna identidad entre páginas;
  - qué páginas no tienen ninguna.
- Tras C9 son 13 de 52 páginas, con 41 entradas, 25 de ellas con solo identidad de su página. C9 ancla la p.226 del URD 2021 con R40; por eso son 13 y no las 14 que cuenta el revisor sobre C8.
- El informe (§0.2 y §1) y T12 dicen qué acredita cada clase y que esas 13 páginas son **cobertura pendiente**.
- **Pruebas:**
  - `paginas_sin_ancla.py` del revisor, sin cambios, sobre C10 (`resultados/revisor4_paginas_sin_ancla_sobre_C10.txt`);
  - `cobertura_por_mutacion.py`: ninguna de las 41 entradas de esas páginas cambia la referencia de la especificación. Cambian las tablas de crecimiento orgánico (alternativas y horizonte), financiación, arrendamientos e impuestos.

## P4 · forma · el caso de los pagos en 178,0 · **aceptada y corregida** (C10)

- Las respuestas (N6 y «Los scripts del revisor sobre C7») y el informe (§1) dicen ahora: ningún residuo lo detecta; lo detectan la doble vía del FCF base y 41 comprobaciones del libro.
- `test_contraste_residuos.py` separa por clase lo que detecta los casos que quedan por debajo de la cota:
  - en H3c, 1 comprobación de fuente y 41 del libro;
  - en el de las adquisiciones de 2021 (C9), 2 del libro.

## P5 · forma · dos frases absolutas · **aceptada y corregida** (C10)

- Informe §1, unidad: la regla vale para los rótulos de la lista; se añade el criterio de formato, y los límites lo dicen.
- Respuestas, N10: esos casos quedan en FALLO, pero su clase no queda cerrada.

## Cobertura de la unidad y del perímetro: respuesta a la pregunta de la persona responsable (§6 de la revisión)

- **La unidad y el perímetro no quedan acreditados por las reglas del verificador.** Son listas de rótulos y criterios que detectan señales conocidas.
- Los acredita, de forma indirecta, una identidad entre páginas. Sobre C10, eso cubre 223 de las 409 entradas usadas.
- Del resto:
  - 151 tienen solo identidad de su página, que acredita la coherencia de su tabla, no su unidad ni su perímetro;
  - 4 solo la Historia del libro;
  - 31, ninguna segunda línea.
- 13 páginas, con 41 entradas, no tienen ninguna identidad entre páginas. Es **cobertura pendiente**. Ninguna de esas entradas cambia los valores de referencia de la especificación.

## Observaciones de la revisión

- **`LS_AMORT_ROU_2021`.** Esta contraparte PENDIENTE da a R16 de 2021 una cifra cuya unidad no está acreditada. La amortización ROU de 2021 la cubre además R25, de su misma página. Se mantiene declarado.
- **Casos C1 y C2 del revisor.** Una línea equivocada en dos de las 31 entradas sin segunda línea pasa las dos defensas. Cambia el ratio fiscal de 2025 y las partidas puntuales, no la referencia. Confirman el límite declarado en N2; no se propone corrección.

## Resultados sobre C10

| Prueba | Resultado |
|---|---|
| Verificador | 743 filas: 729 OK, 14 PENDIENTE, 0 FALLO |
| `test_verificar_cifras.py` | 71/71: 15 positivos reales, 5 PENDIENTE esperados y 51 contraejemplos |
| Contraste | 280 comprobaciones, 0 fallidas; 409 entradas |
| `test_contraste_residuos.py` | 18/18 |
| Mutación | Sin incoherencias con `cobertura_entradas` |
| Scripts del revisor, sin cambios | `resultados/*_sobre_C10.txt` |

## Lo que queda abierto tras C10

- **Revisión independiente de lo afectado por C9 y C10**, sobre un commit congelado (pasada 5): pendiente.
- **Cobertura de la unidad y del perímetro:**
  - 13 páginas (41 entradas) sin identidad entre páginas;
  - 151 entradas con solo identidad de su página;
  - 31 sin segunda línea y 4 solo con la Historia.

  Ninguna de esas entradas cambia la referencia de la especificación. *(Precisión de C12, revisión n.º 5, Q6:)* no era cierto para cinco de las 151 con solo identidad de su página: D&A total y resultado antes de impuestos de 2021 y 2022 y adquisiciones de 2023. Desde C12 tienen identidad entre páginas.
- **Reglas de unidad y perímetro:** listas y criterios que detectan señales conocidas, no acreditación.
- **14 filas PENDIENTE** de URD 2022 p.302, y columnas por sociedad PENDIENTE. *(Precisión de C14, revisión n.º 6, R7 c: la de una sociedad adquirida; las de marca quedaban OK tras C12 y quedan PENDIENTE desde C14.)*
- **Límites de detección por debajo de la cota:** R13 de 2025 y R39 de 2021.
- **Decisiones económicas [DH]:** F1, política de la PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
- **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

# Respuesta a la revisión independiente n.º 5

**Revisión:** [REVISION_INDEPENDIENTE_5.md](REVISION_INDEPENDIENTE_5.md). Commit 595d2f6 de la rama `auditoria/economica-f1-frente-e-revision` (23:19 UTC), sobre el congelado 364129a (C11). La hizo una sesión de revisión nueva, distinta de la de las pasadas 1, 3 y 4. Copia sin cambios y procedencia: [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).

**Resultado de la revisión:**
- reproduce todas las cifras del autor, con salidas idénticas;
- las siete filas de C9 son correctas: las leyó con otras dos herramientas de lectura de PDF y en la página renderizada;
- la corrección de las columnas por país de C9 es correcta para esa clase;
- P1, P3 y P4, corregidas; P5, con un resto; P2, en parte;
- objeciones nuevas: Q1–Q6 (menores) y Q7 (forma);
- no encuentra errores en los datos reales y ninguna conclusión material cambia.

**Esta respuesta** acepta las siete objeciones y las corrige en **C12**. Las pruebas se ejecutan con los scripts del revisor, sin cambios, sobre C12 (`resultados/revisor5_*_sobre_C12.txt`). Para `clases_5.py` y `barrido_tablas.py` se usa como base un worktree temporal de C8. El barrido rotula «C11» la versión nueva porque lo tiene escrito así; aquí es C12.

## Q1 · menor · la columna «published» pasaba como edición vigente · **aceptada y corregida** (C12)

- **Corrección:**
  - dos apariciones del mismo año en posiciones distintas son ahora columnas distintas, así que la reexpresada se reconoce;
  - una columna de ejercicio cuya cabecera dice «published», «reported» o «publié» no puede declararse vigente: FALLO en edición.
- **Pruebas:**
  - en las tablas de reexpresión de las cinco publicaciones (`revisor5_clases_5_sobre_C12.txt`, R), la columna publicada queda en FALLO en 589 de 589 (antes, OK) y la reexpresada en OK en 589 de 589 (antes, PENDIENTE);
  - casos B1 y B2 en el test.
- **Límite:** la tabla del informe de gestión que imprime la cifra publicada bajo «2021 restated» (B4, el 86,9) sigue en OK. La cabecera dice «restated» y el verificador no puede saberlo; la diferencia, 0,1, queda dentro de la cota de R39 (declarado en C9).

## Q2 · menor · la asignación por orden aceptaba la columna equivocada · **aceptada y corregida** (C12)

- **Corrección:**
  - con columnas distintas para fechas distintas del mismo año, el balance del URD 2021 tiene cuatro columnas reconocidas, no tres;
  - una columna de apertura («01/01/2020») se asigna al ejercicio anterior;
  - si dos cabeceras ocupan el mismo sitio, manda la línea más cercana a la fila. La zona de cabecera puede incluir la línea de unidades de la tabla anterior, con su propia fecha (DEU 2024 p.304).
- **Pruebas:**
  - B13 y B14 en FALLO; B15 y B16, las correctas, en OK; B19 (saldo de apertura con nota), en FALLO;
  - en las tablas de vencimientos (B17 y B18) las dos quedan PENDIENTE: la cabecera tiene varias medidas. *(Precisión de C14, revisión n.º 6, R7 b:)* cierto para B17 y B18 (URD 2025 p.366), no para el URD 2022 p.302, donde la cuenta de columnas coincidía por accidente y el orden daba un FALLO al valor en libros y un OK al total sin descontar (R1). Desde C14 los dos quedan PENDIENTE.
- **Límite:** la asignación por orden sigue sin comprobar la alineación de cada número. Se corrige la causa encontrada, la cuenta de columnas, no el método.

## Q3 · menor · la marca «(a)» dejaba PENDIENTE cifras legítimas y rebajaba FALLO a PENDIENTE · **aceptada y corregida** (C12)

- **Corrección:**
  - las palabras de la misma celda que una columna reconocida («restated (a)», «Adjusted») y las llamadas con letra no son cabeceras ajenas;
  - si la columna reconocida más próxima es de otro ejercicio, la fila queda en FALLO aunque haya una cabecera ajena más cerca.
- **Pruebas:**
  - en los estados del URD 2021 (`clases_5`, S), los 75 tokens legítimos quedan en OK y los 75 de otro ejercicio, en FALLO, como en C8;
  - casos C1, C2, C5 y C6 del revisor; C1 y C2, en el test.

## Q4 · menor · el criterio de título dejaba pasar la mayor parte de los bloques por país · **aceptada y corregida** (C12)

- **Corrección.** Se busca el título del bloque, no el de la tabla:
  - el primer título, en mayúsculas y en línea propia, desde la fila hasta el principio de la página;
  - si no lo hay, el último de la página anterior;
  - para todas las filas, estén por encima o por debajo de la línea de unidades.

  La prosa y las cabeceras de columna en minúsculas no cuentan como título. Lo que queda en la línea de unidades solo cuenta si es un único país o segmento («(In millions of euros) France»).
- **Pruebas:**
  - bloques de la nota de pensiones de las cinco publicaciones (`clases_5`, P): ninguna cifra en millones queda OK (367 PENDIENTE y 9 FALLO de 376) y ninguno de los 209 porcentajes;
  - casos E2–E7 en PENDIENTE; E18, el total del grupo bajo prosa que nombra el Reino Unido, en OK; E19, el positivo de C10, en OK;
  - seis casos nuevos en el test.
- **Un falso positivo propio, corregido antes del commit.** En un primer intento, la línea de unidades de las tablas de combinaciones de negocio («(In millions of euros) Acquisition date Belgium Brazil…») se tomaba como título y dejaba PENDIENTE también la columna del total. Ahora decide la regla de las columnas por país. *(Precisión de C14, revisión n.º 6, R7 d:)* en la tabla del URD 2022 p.274, sin ninguna columna reconocida, esa regla no actuaba y la columna de Alemania quedaba OK en perímetro (R4). Desde C14, una cabecera con tres países o más y sin columna reconocida deja el perímetro PENDIENTE.
- **Frases alineadas:** informe §1 y T14. El límite de P2 en estas respuestas se mantiene: no se detecta un bloque de otro perímetro sin título que lo nombre.

## Q5 · menor · filas de segmento con rótulos fuera de las listas · **aceptada y corregida** (C12)

- **Corrección:**
  - los rótulos de segmento se comparan normalizados: «and», «et» y «&» valen lo mismo, y se quita el prefijo «CGU»;
  - un rótulo partido en dos líneas se une con el de la línea anterior;
  - se añaden «République d'Irlande», «Eire», «Great Britain» y «Latvia» a los países;
  - **identidad nueva R42:** crecimiento publicado frente al crecimiento de las ventas de las cuentas de resultados, de 2021 a 2025. Es la que propone el revisor y sus residuos coinciden con los suyos. Ancla las cinco tablas de crecimiento.
- **No se implementa el criterio de estructura** (las filas que preceden a TOTAL no son del grupo). En las tablas por naturaleza, las filas anteriores al total son componentes del grupo; el criterio exigiría distinguir las tablas por segmento de las tablas por naturaleza.
- **Pruebas:**
  - en las tablas de crecimiento (`clases_5`, G), ninguna fila de segmento queda OK en ventas ni en crecimiento orgánico;
  - E8–E16 en FALLO;
  - cuatro casos nuevos en el test y uno en el de residuos: R42 falla con el crecimiento de un segmento.
- **Sensibilidad de R42:** un +3 en las ventas del año anterior mueve el crecimiento unos 0,07 puntos; en 2024 eso no supera la cota. La cobertura propia del revisor lo refleja: deriva para R42 de 2024 dos páginas y no tres.

## Q6 · menor · tres frases sobre la referencia más fuertes que su prueba · **aceptada y corregida** (C12)

- **Identidades nuevas** para las cinco entradas de solo misma página que mueven la referencia, con siete filas nuevas de páginas publicadas:
  - R41: resultado antes de impuestos frente a la nota 9 (URD 2022 p.326 y URD 2023 p.345), para 2021 y 2022;
  - R8 de 2021–22: línea del EFE (p.261 y p.279) y dotaciones netas a provisiones (p.284 y p.301);
  - R24 de 2023: puente de la deuda neta del DEU 2024 (p.260).

  Todas con residuo 0,0. Las 97 entradas que mueven la referencia tienen ya identidad entre páginas.
- **Frases corregidas:** E9 de la especificación y «Lo que queda abierto tras C10». El punto de recuperación de C10 ya no las repite.
- `cobertura_por_mutacion.py` informa ahora también de la clase «solo identidad de la misma página»: 0 entradas con efecto en la referencia.
- **Pruebas:**
  - `cobertura_propia.py` del revisor, sin cambios, sobre C12: 244, 140, 2 y 31, con 0 discrepancias, y 97 de 97 entradas que mueven la referencia con identidad entre páginas;
  - tres casos nuevos en el test de residuos.

## Q7 · forma · varios · **aceptada y corregida** (C12)

- **(a)** Informe §0.11, alineado con §12.
- **(b)** Ya corregida en 0caa7ee.
- **(c)** Fila «B1, B2» de la tabla de N1, con su precisión.
- **(d)** «Límite que queda» de C9, con Q1 y Q2.
- **(e)** Coma del README.
- **(f)** El FALLO de perímetro de una columna por país nombra la cabecera completa, uniendo las palabras apiladas en el mismo sitio.

## Resultados sobre C12

| Prueba | Resultado |
|---|---|
| Verificador | 750 filas: 736 OK, 14 PENDIENTE, 0 FALLO. Las 743 anteriores no cambian de estado en ninguna dimensión |
| `test_verificar_cifras.py` | 89/89: 20 positivos reales, 10 PENDIENTE esperados y 59 contraejemplos |
| Contraste | 290 comprobaciones (136 libro, 125 fuente con 124 residuos, 29 algebraicas), 0 fallidas; 417 entradas |
| Cobertura | 244 entre páginas, 140 solo misma página, 2 solo Historia y 31 sin segunda línea. 8 de 53 páginas sin identidad entre páginas (24 entradas) |
| `test_contraste_residuos.py` | 22/22 |
| Mutación (528 filas) | Sin incoherencias. Ninguna entrada que mueva la referencia queda sin identidad entre páginas |
| Sondas | 711/711 en unidad y en perímetro |
| Valores de referencia de E9 | Sin cambios |
| Scripts de los revisores n.º 1, 3 y 4 | Mismos resultados que sobre C10, salvo los recuentos |

## Lo que queda abierto tras C12

- **Revisión independiente de lo afectado por C12** (pasada 6): pendiente.
- **Cobertura de la unidad y del perímetro:**
  - 8 páginas (24 entradas) sin identidad entre páginas;
  - 140 entradas con solo identidad de su página;
  - 31 sin segunda línea y 2 solo con la Historia.

  Ninguna de ellas mueve la referencia; las 97 que la mueven tienen identidad entre páginas.
- **Las reglas del verificador detectan señales conocidas; no acreditan:**
  - la asignación de columnas sigue siendo heurística;
  - la tabla de gestión con la cifra publicada bajo «restated» no se detecta;
  - un bloque de otro perímetro sin título ni rótulo que lo nombre, tampoco.
- **14 filas PENDIENTE** de URD 2022 p.302, y columnas por sociedad PENDIENTE. *(Precisión de C14, revisión n.º 6, R7 c: la de una sociedad adquirida; las de marca quedaban OK tras C12 y quedan PENDIENTE desde C14.)*
- **Límites de detección por debajo de la cota:** R13 de 2025, R39 de 2021 y R42 frente a las ventas.
- **Decisiones económicas [DH]:** F1, política de la PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
- **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.

# Respuesta a la revisión independiente n.º 6

**Revisión:** [REVISION_INDEPENDIENTE_6.md](REVISION_INDEPENDIENTE_6.md). Commit 9711f04 de la rama `auditoria/economica-f1-frente-e-revision` (01:24 UTC), sobre el congelado 1b80b5d (C13). La hizo una sesión de revisión nueva, distinta de las de las pasadas anteriores. Copia sin cambios y procedencia: [PROCEDENCIA_REVISOR.md](PROCEDENCIA_REVISOR.md).

**Resultado de la revisión:**
- reproduce todas las cifras del autor, con salidas idénticas;
- las siete filas nuevas de C12 son correctas, leídas con otras dos herramientas y a la vista;
- Q1, Q3 y Q6, corregidas; Q4, con dos efectos nuevos; Q2 y Q5, en parte; Q7, con un resto;
- objeciones nuevas: R1–R5 (menores) y R6–R8 (forma). Ninguna afecta a las 750 filas reales;
- ninguna conclusión material cambia.

**Esta respuesta** acepta las ocho objeciones y las corrige en **C14**. En tres puntos la corrección no es la que propone el revisor; se explica en cada uno y queda para la pasada 7:
- R1: las columnas por entidad se tratan en el perímetro, con una regla de grupos de columnas, y no se aplica la regla de cabecera ajena a la asignación por orden;
- R2: G2 y G4 quedan PENDIENTE, no OK, por esa regla de grupos;
- R3: el umbral de alineación es de 5,5 caracteres, no de 3.

**Pruebas.** Los scripts de las seis revisiones, sin cambios, sobre C14 (`resultados/*_sobre_C14.txt`). El barrido del revisor n.º 6 compara C13 con C14, y sus clases se cruzan con su propia lectura geométrica (`revisor6_barrido_6_sobre_C14.txt`, `revisor6_clases_6_sobre_C14.txt`). La versión anterior es un worktree temporal de C13; para `clases_5.py` y `barrido_tablas.py`, uno de C8, como en C12.

**Las 750 filas reales no cambian:** el mismo estado y el mismo detalle en las seis dimensiones que en C12 y C13. Las dos filas nuevas de R6 quedan OK.

## R1 · menor · con el año repetido en la cabecera la fila se asignaba por orden · **aceptada y corregida** (C14), con otra regla para las columnas por entidad

- **Corrección:**
  - **alineación en la asignación por orden.** Las columnas de ejercicio se asignan por orden solo si, además de coincidir la cuenta, cada número de la línea está a 14 caracteres o menos de su columna. Si no, por alineación. En el URD 2022 p.302, el valor en libros (485,5) y el total sin descontar (612,1) quedan PENDIENTE (F13, F14), como en C11. En las columnas de concepto (familias) no se exige: la regresión de las filas reales lo mostró antes del commit, porque la tabla de crecimiento del URD 2023 p.261, con las cabeceras alineadas a la izquierda, perdía la asignación correcta de tres columnas;
  - **la cabecera es la de la propia tabla.** Si entre la declaración de unidades y la fila empieza otra tabla (una línea de ejercicios tras filas de datos), la cabecera es la de esa tabla. Antes, la zona de cabecera de la tabla de marcas del DEU 2024 p.317 incluía la prosa de la tabla anterior: de ahí el motivo de F12 (R8 c);
  - **grupos de columnas.** Si los ejercicios de las columnas repiten un mismo bloque (2025, 2024, 2025, 2024…), cada grupo es una entidad o una medida (una marca, una firma auditora). La columna de un grupo deja el perímetro PENDIENTE, con el rótulo del grupo en el motivo; el grupo «Total» o «Group» se acepta. En el impuesto por jurisdicción los ejercicios no se repiten así (2025, 2025, 2025, 2024…: una columna por medida dentro de cada ejercicio), y el TOTAL del grupo queda OK (F7);
  - **filas de jurisdicción o de desglose.** Una fila cuyo rótulo, unido con las líneas de rótulo que tiene encima, nombra una jurisdicción o una región («European Union», «Union européenne», «Non-cooperative jurisdictions», «Pays non coopératifs») o un país tras «of which», «dont», «including», «excluding» u «hors» no es del grupo: FALLO.
- **Por qué no la regla propuesta para la rama por orden.** Con orden y alineación, cada número tiene su propia columna reconocida y alineada. Una palabra ajena más próxima es parte de la misma celda apilada («Income (loss) / before tax 2025», «Amount (excl tax)»), no otra columna. Aplicar ahí la regla de C9 dejaría PENDIENTE, por un motivo ajeno, el total del impuesto (F7), que el revisor da por correcto, y las filas de honorarios con «(excl». La columna por entidad la detecta la regla de grupos, y en el perímetro: su ejercicio es correcto, como dice el revisor.
- **Pruebas** (`revisor6_contraejemplos_6_sobre_C14.txt`): F1–F6, FALLO de perímetro; F7, OK; F8, FALLO; F9–F12, PENDIENTE de perímetro, y F12 con el motivo «Elis», sin prosa; F13, F14 y F19, PENDIENTE de ejercicio; F15 y F16, PENDIENTE, como en C13; F17 y F18, PENDIENTE por la regla de grupos. En el barrido, ninguna candidata pasa a OK (clase D del revisor: 0). De las 161 candidatas cuyo rótulo nombra un país, una región, una UGE o una jurisdicción y que quedaban OK como del grupo en C13 (clase E), quedan 11. Las 11 son líneas del grupo que nombran un país de pasada: el efecto de impuestos no basados en el resultado, la contribución excepcional francesa y la actualización del complemento de precio. Casos nuevos en el test: F1, F4, la fila de la Unión Europea partida en dos líneas, F7 (positivo), F9, F12, F13, F14 y F19.

## R2 · menor · un encabezado numerado no contaba como título · **aceptada y corregida** (C14), con G2 y G4 en PENDIENTE

- **Corrección:** una línea que empieza por una numeración de nota o de apartado («NOTE 13 …», «5.4 …») y no tiene más cifras es un título y corta la búsqueda, vaya o no en mayúsculas.
- **Pruebas:** los honorarios (G1–G4) ya no ven «SWITZERLAND», «SWEDEN» ni «SUISSE». Bajo «5.4 Share-based payments», el plan de acciones G9 queda con el perímetro OK (la unidad falla: es un recuento). En el barrido, 387 tokens de los planes de acciones pasan de PENDIENTE a OK en perímetro, y la lectura propia del revisor no nombra ningún país en ninguno (clase C).
- **Divergencia: G2 y G4 quedan PENDIENTE, no OK.** La cabecera de los honorarios repite 2022 y 2021 por firma y por medida, y la regla de grupos de R1 la trata como una tabla por entidad. El verificador no distingue la columna de una firma auditora, cuyos honorarios paga el grupo, de la de una marca, cuya cifra es de la marca. Además, la columna de una firma es un desglose por firma, no el total del grupo. Se prefiere PENDIENTE para las dos clases antes que OK. G2 y G4 están en el test con PENDIENTE esperado, el motivo de la regla de grupos y sin el título de país.

## R3 · menor · «el FALLO manda» daba FALLO a cifras legítimas del cierre · **aceptada y corregida** (C14), con otro umbral

- **Corrección:** bajo una cabecera ajena, el FALLO por la columna de otro ejercicio solo se mantiene si esa columna está alineada con el token, a 5,5 caracteres o menos. Si no, PENDIENTE, con la distancia en el motivo.
- **Por qué 5,5 y no 3.** El umbral se mide en la rejilla de caracteres de pdftotext. Una fecha «12/31/2025» alineada a la derecha sobre una cifra de un carácter tiene el centro a 4,5 caracteres del de la cifra; se suma uno de holgura. La lectura geométrica del revisor sobre el barrido C13 → C14 (clases_6, A) lo confirma:
  - con 3, 208 cifras cuya cabecera alineada es de otro ejercicio pasaban de FALLO a PENDIENTE, 131 de ellas a 3,5 caracteres: impuestos diferidos («12/31/2023 net»), valor razonable y vencimientos;
  - con 5,5, son 24, todas a más de 5,5: prosa y columnas de vencimientos;
  - los valores en libros del DEU 2024 p.323 están a 13,5.
- **Pruebas:** G6 y G7, PENDIENTE; clase F del revisor (cifras que fallan con los tres ejercicios en C14 y no en C13): 0. Casos nuevos: G6, y como control, el total sin descontar de 2022 (612,1) declarado 2021, que sigue en FALLO.
- **Efecto en el barrido** (páginas del grupo): 1.829 candidatas pasan de FALLO a PENDIENTE en ejercicio. Según la lectura del revisor, 1.716 no tienen ninguna fecha alineada, 86 no tienen lectura, 24 tienen alineada la cabecera de otro ejercicio y 3 la del ejercicio declarado. Ninguna pasa a OK.

## R4 · menor · el título de tabla en caja normal y las columnas por país sin columna reconocida dejaban de detectarse · **aceptada y corregida** (C14)

- **Corrección:**
  - vuelve el criterio de C10, acotado. Desde la cabecera de la tabla hacia arriba, las líneas de cabecera en columnas se saltan; una línea de datos, con cifras, de más de 40 caracteres o con puntuación de frase corta la búsqueda; la primera línea de una sola celda decide. Es título si nombra un país o un segmento con cuatro palabras más como mucho («Mexico», «Interest rate swap – Chile»). Así no vuelve el falso positivo de C10: el total del grupo bajo prosa que nombra el Reino Unido (E18) sigue OK;
  - una cabecera con tres países o más y sin ninguna columna reconocida deja el perímetro PENDIENTE.
- **Pruebas:** H1–H5, PENDIENTE de perímetro. En el barrido, 1.207 tokens de las tablas de sensibilidad y de combinaciones de negocio pasan de OK a PENDIENTE en perímetro, y la lectura propia del revisor nombra un país en todos (clase C). Casos nuevos: H1 y H2.

## R5 · menor · en la tabla del fondo de comercio por UGE solo fallaba «CGU France» · **aceptada y corregida** (C14)

- **Corrección:** el prefijo «CGU»/«UGT» se quita también al comparar el rótulo con la lista de países, y se añade «Grande-Bretagne».
- **Pruebas:** I11–I15, FALLO; las filas de UGE de las cinco publicaciones pasan a FALLO. Casos nuevos: I12 e I14.

## R6 · forma · la clase «entre páginas» es por pertenencia · **aceptada y corregida** (C14)

- **Corrección:**
  - `que_acredita_cada_clase` y el informe §0.2 dicen que la clase es por pertenencia;
  - cada entrada contrastada entre páginas lleva el intervalo de errores que ninguna identidad entre páginas detecta (`errores_sin_deteccion_entre_paginas`) y su umbral en unidades de su última cifra. Resumen en `umbrales_entre_paginas`: 145 entradas hasta 2 unidades, 99 de 2 a 5, 2 de 5 a 10 y ninguna de más de 10;
  - el informe §2 sustituye el caso de 2024 por el intervalo de cada año, en las ventas y en el crecimiento publicado;
  - **identidad nueva R23 de 2021–22:** las ventas de la cuenta de resultados frente a la información por segmentos del URD 2022 (p.279) y del URD 2023 (p.296), con dos filas nuevas, OK en las seis dimensiones. Residuo 0,0 los dos años. Las ventas de 2021 y 2022 quedan contrastadas desde ±0,1; con solo R42, de −0,20 a +0,85 y de −2,30 a +0,26.
- **Pruebas:** dos casos nuevos en el test de residuos. Las ventas de 2021 con +0,5 y las de 2022 con −1,0 quedan dentro de lo que R42 no detecta, y R23 falla en los dos.
- **Lo que queda:** el crecimiento publicado solo tiene R42 entre páginas (intervalos en el informe, §2).

## R7 · forma · frases más fuertes que su prueba · **aceptada y corregida** (C14)

- **(a)** Informe §1, límites: acotado a lo que ocurre en cada clase de tabla.
- **(b)** Q2 de la quinta parte: precisado en su sitio.
- **(c)** «Límite que queda» de C9 y «Lo que queda abierto» tras C10 y tras C12: precisados en su sitio.
- **(d)** Q4 de la quinta parte: precisado en su sitio.
- **(e)** El punto de recuperación dice qué cubren las pruebas: los casos de los revisores y el barrido completo del revisor n.º 6.
- **(f)** T14: la exigencia de alineación y las reglas nuevas, con sus casos.

## R8 · forma · varios · **aceptada y corregida** (C14)

- **(a)** La versión del punto de recuperación que daba «00:15» queda en el historial y no se cambia; el commit de C12 es de las 00:11:29 UTC. **El autor repitió el error:** el punto de recuperación de c11a6de dice «hacia las 01:50 UTC» y el commit es de las 01:38:27. Desde esta versión, la hora del punto es la de un commit, verificable, y no una estimación.
- **(b)** La regla de edición usa la misma regla de cabecera ajena que el ejercicio: la columna de ajuste («IFRS 3») ya no se marca como publicada. En el barrido, 102 candidatas pasan de FALLO a OK en edición: 97 de la columna de ajuste según la lectura del revisor y 5 sin lectura («IAS 19», «IFRS 3» y prosa). La columna publicada sigue en FALLO en 591 de 591, y la reexpresada en OK en 588 de 588. Caso nuevo: la columna de ajuste (0,1), con edición OK y ejercicio PENDIENTE.
- **(c)** El motivo de las columnas por país une solo celdas cortas, sin cifras, y la cabecera es la de la propia tabla (R1).
- **(d)** `segmento_de_sublinea` atribuye la fila de la que depende con `segmento_de_rotulo`.

## Resultados sobre C14

| Prueba | Resultado |
|---|---|
| Verificador | 752 filas: 738 OK, 14 PENDIENTE, 0 FALLO. Las 750 anteriores no cambian de estado ni de detalle en ninguna dimensión; las 2 nuevas, OK |
| `test_verificar_cifras.py` | 108/108: 21 positivos reales, 21 PENDIENTE esperados y 66 contraejemplos |
| Contraste | 292 comprobaciones (136 libro, 127 fuente con 126 residuos, 29 algebraicas), 0 fallidas; 419 entradas |
| Cobertura | 246 entre páginas, 140 solo misma página, 2 solo Historia y 31 sin segunda línea. 8 de 55 páginas sin identidad entre páginas (24 entradas). Umbrales entre páginas: 145, 99, 2 y 0 |
| `test_contraste_residuos.py` | 24/24 |
| Mutación (530 filas) | Sin incoherencias: 386 por identidad, 2 solo libro, 23 sin detectar y sin efecto en la referencia, 8 leídas sin efecto y 111 no usadas |
| Sondas | 713/713 en unidad y en perímetro |
| Valores de referencia de E9 | Sin cambios |
| Scripts de los revisores n.º 1, 3, 4 y 5 | Mismos resultados que sobre C12, salvo los recuentos y tres efectos de C14 (`*_sobre_C14.txt`): «Germany & Luxembourg», en el orden de la página (R8 c); un título «France» (R4); la columna de ajuste de las tablas de reexpresión, PENDIENTE en lugar de FALLO en 75 casos (R8 b). `barrido_tablas.py` compara C8 con C14 y recoge todas las transiciones de C14, que el barrido del revisor n.º 6 clasifica |
| Scripts del revisor n.º 6 | `contraejemplos_6`, barrido y clases C13 → C14, consultas, cobertura y lectura de las filas de C12 (`revisor6_*_sobre_C14.txt`) |

## Lo que queda abierto tras C14

- **Revisión de lo afectado por C14** (pasada 7): pendiente. Incluye las tres decisiones en las que C14 no sigue la propuesta del revisor (R1, R2 y R3).
- **Cobertura de la unidad y del perímetro:**
  - 8 páginas (24 entradas) sin identidad entre páginas;
  - 140 entradas con solo identidad de su página;
  - 31 sin segunda línea y 2 solo con la Historia.

  Ninguna de ellas mueve la referencia; las 97 que la mueven tienen identidad entre páginas.
- **Las reglas del verificador detectan señales conocidas; no acreditan:**
  - la asignación de columnas depende de la rejilla de caracteres de pdftotext y de dos umbrales (14 y 5,5 caracteres);
  - la regla de grupos no distingue una columna por firma auditora de una por marca: las dos quedan PENDIENTE;
  - la tabla de gestión con la cifra publicada bajo «restated» no se detecta;
  - un bloque de otro perímetro sin título ni rótulo que lo nombre, tampoco.
- **14 filas PENDIENTE** de URD 2022 p.302.
- **Límites de detección por debajo de la cota:** R13 de 2025, R39 de 2021 y R42 en el crecimiento publicado (intervalos en el informe, §2).
- **Decisiones económicas [DH]:** F1, política de la PPA, reinversión necesaria (M1 a–d, M2), perímetros de S2C y del margen.
- **Sin aptitud para dinero real.** Se conservan C48 = 108 y E1/D3/E2/E6.
