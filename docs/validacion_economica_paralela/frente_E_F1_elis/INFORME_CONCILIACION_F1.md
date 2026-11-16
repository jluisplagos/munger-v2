# F1 · Elis · Conciliación económica, puente del FCF base al motor A y especificación propuesta (frente E)

Fecha: 15-nov-2026. Rama: `auditoria/economica-f1-frente-e`, creada desde `auditoria/economica-f1` (c029018).
**F1 sigue abierto.** Esta entrega cierra la conciliación de cifras y puentes con fuentes primarias y cálculos reproducibles. No cierra la decisión económica: la corrección de la plantilla necesita una decisión humana y datos que Elis no publica. No contiene valoraciones, precios objetivo ni recomendaciones de inversión. No se ha modificado código, libros ni datos de producción.

Marcas usadas en todo el informe:
**[P]** dato publicado (página PDF verificada) · **[D]** derivación aritmética de datos publicados o de fórmulas del libro · **[I]** interpretación económica · **[H]** hipótesis no verificable con la base · **[DH]** decisión humana registrada · **[S]** supuesto de la orquestación (no es decisión humana).

---

## 0. Resumen

1. **Base y evidencia.** Base 4.14 materializada desde el ZIP original y verificada (6.798/6.798 + manifiesto). Árbol del hito 4.15 (059f4f6) verificado con su propio manifiesto (7.004/7.004). El libro de Elis es idéntico en ambos (SHA-256 `d2593777…92385`).
   - 752 cifras y citas de cinco informes anuales de Elis comprobadas contra los bytes de los PDF en seis dimensiones: literal (página, posición y signo), ejercicio, concepto de la columna, unidad, perímetro y edición.
   - Resultado: 738 filas sin incoherencia detectada en ninguna dimensión, 14 PENDIENTE y ninguna en FALLO. Las 14 son filas de arrendamientos de una página del URD 2022 (p.302) en la que el verificador no encuentra ni la unidad ni la cabecera de columnas: quedan PENDIENTE en esas dos dimensiones. Solo una se usa, como contraparte de una identidad.
   - **OK significa que las reglas automáticas no detectan ninguna incoherencia en esa dimensión, no que la cifra esté acreditada** (revisión n.º 3, N1). El concepto de la línea es una declaración: lo acreditan una identidad, el libro o una lectura independiente.
   - Test del verificador: 136/136. Acepta 23 positivos reales y rechaza 77 contraejemplos, cada uno en la dimensión que debe detectarlo. Deja en PENDIENTE 36 casos:
     - el control manual justificado;
     - la columna de una sociedad adquirida;
     - dos recuentos de acciones sin rótulo de recuento (revisión n.º 4, P1);
     - seis cifras de bloques de un país bajo su título (revisión n.º 4, P2, y n.º 5, Q4);
     - once filas de la revisión n.º 6: columnas por marca y por firma auditora, una tabla de vencimientos con la cuenta de columnas desplazada, una línea de prosa, el valor en libros bajo «Valeur comptable», un título de tabla «Mexico», una cabecera con países y sin columna reconocida y la columna de ajuste de una tabla de reexpresión;
     - cuatro de la revisión n.º 7: la tabla de hipótesis con una columna por país y sin declaración de unidades ni de ejercicios, y dos saldos del estado de cambios en el patrimonio, con el ejercicio OK y la columna PENDIENTE desde C18 (revisión n.º 8, T1);
     - once de la revisión n.º 8: un saldo de una tabla de derechos de uso con columnas por concepto y dos del estado de cambios en el patrimonio con el rótulo partido (ejercicio OK y columna PENDIENTE); cinco tokens que no son cifras (el día, el año y la pestaña de un rótulo de saldo, el año de una línea de prosa y el de un título); las dos últimas filas de la tabla del WACC por país del DEU 2024 (perímetro PENDIENTE); y la pestaña del capítulo junto a un párrafo.
     Incluye los mutantes conjuntos de posición y literal, año, unidad, perímetro y edición, los M1–M4 de la revisión n.º 1, los de N1, los contraejemplos de la adenda de la revisión n.º 3, la columna de un país en una tabla con columnas por país (C9) y los de las revisiones n.º 4 a 8. Aparte, nueve comprobaciones directas de funciones del verificador: el criterio de encabezado numerado y el rótulo con viñeta sobre líneas reales, y la excepción «Total» de la cabecera por países sobre dos líneas sintéticas, porque no tiene caso real (revisión n.º 8).
   - Test de los residuos: 24/24. Con el verificador saltado a propósito, los residuos hacen fallar por sí solos el cálculo ante una cifra de otro año o de otra línea, y la excepción fijada no absorbe un error nuevo mayor que su cota. Los errores menores que la cota no los detecta ninguna identidad, y el test documenta ese límite. También falla si la verificación no es la del CSV usado.
2. **Conciliación 2021–2025.** Las 126 identidades cierran dentro de su cota de redondeo [D] (71 de la ventana en la revisión n.º 3; ahora también 2021–2022, los totales de inversión y financiación y la coincidencia entre ediciones):
   - la cota es la suma de media unidad de la última cifra impresa de cada cifra que interviene (de 0,10 a 0,50 según la identidad);
   - el −0,2 del free cash flow de 2024 frente a sus componentes está dentro de su cota de 0,35 (siete cifras impresas): ya no es una excepción;
   - la única excepción es el +0,4 de 2025 entre el interés de arrendamientos de caja (29,6) y el devengado (29,2), una diferencia de concepto sin puente publicado. Se fija en su valor exacto con la cota de redondeo de sus tres cifras (± 0,15). Un error nuevo en ellas cuyo efecto neto supere 0,15 hace fallar la comprobación; uno menor, como 29,3 en lugar de 29,2, no (§5.4). No es material;
   - de las 419 entradas que usa el cálculo, 246 tienen una identidad entre páginas, 140 solo una de la misma página y 2 solo la Historia del libro. Las otras 31 no tienen segunda línea y se listan en `cobertura_entradas`: diferidos, CVAE y relaciones con clientes de la tabla de impuestos, componentes de otros ingresos operativos, OCEANE y algunas del horizonte 2021–22;
   - las 97 entradas que mueven los valores de referencia de la especificación tienen todas una identidad entre páginas:
     - las cinco que solo se comparaban con la Historia (adquisiciones e impuesto de 2021 y 2022, ventas de 2020), desde C9;
     - las cinco que solo tenían identidad de su página (D&A total y resultado antes de impuestos de 2021 y 2022, adquisiciones de 2023), desde C12 (revisión n.º 5, Q6; §2). Hasta C11 este punto decía que ninguna de esas clases movía la referencia, y no era cierto para cinco de las entonces 151;
     - ninguna de las 140, 2 y 31 restantes mueve la referencia;
   - **qué acredita cada clase** (revisión n.º 4, P3):
     - una identidad entre páginas acredita el número y, de forma indirecta, su unidad y su perímetro, porque otra presentación de otro perímetro o de otra unidad la rompería. **La clase es por pertenencia**, no por sensibilidad (revisión n.º 6, R6): basta que la entrada intervenga en una identidad entre páginas. Lo que acredita es el número salvo un error dentro del intervalo que ninguna de esas identidades detecta, que `cobertura_entradas` da para cada entrada (`errores_sin_deteccion_entre_paginas`):
       - el mayor error que no se detecta es de 2 unidades de la última cifra o menos en 145 entradas, de 2 a 5 en 99 y de 5 a 10 en 2: el FCF antes de impuestos y los impuestos pagados de 2024, por R11, que no detecta errores de −0,55 a +0,15. Contado de otro modo (revisión n.º 7, S6 d), un error en los dos sentidos se detecta desde 1 unidad en 5 entradas, desde 2 en 112, desde 3 en 69, desde 4 en 17, desde 5 en 33 y desde 6 en 10 (`detecta_desde_unidades`). Un error igual al umbral no se detecta;
       - las ventas de 2021 a 2025 y las de 2020, por encima de ±0,1, por R23 y R40: un error de 0,1 exacto no se detecta y uno de 0,2, sí (revisión n.º 7, S6 c). Hasta C12 las de 2021 y 2022 solo tenían R42, que no detecta errores de −0,20 a +0,85 y de −2,30 a +0,26;
       - el crecimiento publicado de cada año solo tiene R42 entre páginas. No detecta errores de −0,030 a +0,077 puntos en 2021, de −0,008 a +0,099 en 2022, de −0,068 a +0,038 en 2023, de −0,019 a +0,085 en 2024 y de −0,074 a +0,030 en 2025 (`umbrales_entre_paginas`);
     - una identidad de la misma página solo acredita la coherencia interna de su tabla: una tabla entera de otro perímetro cuadra igual;
     - la Historia acredita el número, salvo un error común a las dos transcripciones;
     - sin segunda línea, quedan el literal y las reglas del verificador.
     De las 55 páginas con entradas usadas, 8 no tienen ninguna entrada contrastada entre páginas. Reúnen 24 entradas, 9 de ellas con solo identidad de su página: las tablas de deuda neta, las de impuestos diferidos y tres páginas sueltas (`cobertura_entradas.paginas_sin_identidad_entre_paginas`). Las tablas de crecimiento están ancladas desde C12 por R42. En ellas la unidad y el perímetro descansan en las reglas del verificador y en la lectura: **es cobertura pendiente**, no acreditada;
   - una prueba de mutación de las 530 filas de la edición vigente coincide con esta clasificación, sin ninguna incoherencia (§1, `scripts/cobertura_por_mutacion.py`).
3. **FCF base 307,933** reproducido por dos vías independientes (CFO y free cash flow publicado menos SBC). **C48 = 108** se mantiene con su derivación: 82,933 de intereses financieros + 25,067 de interés implícito de caja de arrendamientos [D][DH E6].
4. **f = 4,168 %** se descompone exactamente en: pagos de arrendamientos 153,2 (principal 128,1 + interés de caja 25,1), intereses financieros 82,9, efectos fiscales −24,9 y otros −21,1. **Ni la amortización de derechos de uso ni la de intangibles adquiridos están dentro de f**: aparecen en la reinversión histórica (−81,2) [D].
5. **Motor A** reimplementado desde sus ecuaciones documentadas: reproduce los 30 flujos anuales, los 3 del año 11 y los 3 flujos sin crecimiento del libro con diferencias < 10⁻⁹ [D]. Su flujo sin crecimiento, 248,5, es el FCF base −59,4: +39,6 por el nivel del EBIT 2025, −8,0 por el cambio de tipo impositivo, −9,9 por escalar f a las ventas 2025 y −81,2 porque la proyección no reproduce la reinversión histórica [D].
6. **Arrendamientos: inconsistencia demostrada en la definición del modelo** [D], condicionada a una premisa económica explícita (§5.3). La práctica de Elis la apoya: en sus pruebas de deterioro cuenta el arrendamiento una sola vez, como renovación dentro de la inversión (el esquema de A1′).
   - En la calibración el coste de arrendamiento se cuenta una vez: los pagos.
   - En la proyección se cuenta dos veces: la amortización ROU dentro del margen y los pagos completos dentro de f.
   - El exceso equivale a la amortización ROU: 2,9–3,1 % de las ventas, 139,4 en la base 2025 si se corrige f.
   - Es íntegro a crecimiento cero y en el terminal, y no depende del reparto entre reposición y crecimiento. En los años 1–10 solo se compensaría en parte si la palanca S2C se anclara en C53, que no es el caso de este expediente.
   - Es un defecto de definición, no un error de datos. No se corrige aquí.
7. **Intangibles adquiridos: doble cómputo no demostrado.** La V6.3 los trata implícitamente como una reposición monetaria necesaria de 85,7 al año.
   - Publicado [P]: la amortización no es salida de caja y el valor neto de las relaciones con clientes es 275,1 frente a 83,5 de amortización anual. Las altas de 2025 son provisionales.
   - Inferido [I]: la amortización es mayoritariamente no deducible en caja, porque el ingreso por diferido de intangibles, 15,5/20,3/17,5, equivale al 18–24 % de la amortización.
   - El crecimiento orgánico, neto de bajas, fue positivo y con efecto volumen: en la ventana la cartera se repuso orgánicamente. Es evidencia parcial contra la reposición monetaria, no una refutación para el futuro.
   - La tasa de bajas no se publica. Requiere una decisión de política [P][I][H].
8. **Reinversión necesaria frente a crecimiento: no publicada como importe** [P]. Lo único cuantitativo publicado es una proporción parcial: dos tercios de la inversión en lino plano mantienen el stock en circulación, según un factor de riesgo repetido en los URD 2021–2025. Para todo el capex propio no cierra el dato (§6.1).
   - Se acota por inferencia, con premisas explícitas, entre la D&A propia (736,0 de media) y el capex propio (867,2). La premisa de volumen tiene apoyo publicado cualitativo; la referencia inferior tiene evidencia publicada en contra como caso central [I].
   - La V6.3 implica 954,0, por encima de lo que Elis invirtió mientras crecía [I].
   - Es material: el flujo de partida va de 339,8 a 477,8 según el reparto, frente a 248,5 en la V6.3 [D]. Todos esos niveles llevan unos +27,9 de partidas puntuales de la ventana (§4.2).
9. **Alternativas** A1, A1′, A2 y cota B calculadas, con sus consecuencias en f, el flujo de partida y el ancla de S2C. **Ninguna adoptada**. Especificación con reglas de control y criterios de prueba en [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md).
10. **Pendiente:** decisión F1 (a/b/c con política completa), política de intangibles adquiridos, dato o estimación documentada de la reinversión necesaria, perímetro de S2C y del margen. Dos observaciones de la plantilla quedan fuera de F1: la ventana del tipo impositivo y la escala de intereses sin endeudamiento nuevo. La conclusión de nivel de Elis sigue **pendiente_de_datos**.
11. **Revisiones independientes.**
    - La n.º 1 planteó 17 objeciones, 3 materiales, y ninguna invierte una conclusión material. La respuesta individual a cada una, con su commit y su prueba, está en [revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), junto con la respuesta al contraste externo sobre 6fb9294.
    - Las n.º 3 a 8 revisaron las correcciones sucesivas sobre commits congelados (§12).
    - La n.º 7 revisó C14 y planteó S1–S7; la n.º 8 revisó C16 y planteó T1–T8. Ninguna con efecto en las filas reales. La respuesta a la n.º 8 está en C18 (octava parte de las respuestas). La n.º 9 revisó C18 y planteó U1–U6, también sin efecto en las filas reales; su respuesta (C20) está en preparación ([revision/ESTADO.md](revision/ESTADO.md)).

---

## 1. Alcance, base y evidencia

| Elemento | Identificación | Comprobación |
|---|---|---|
| Base 4.14 | ZIP `munger_v2_r1_entrega4.14_cierre_verificacion_entradas.zip`, 1.130.912.246 bytes, SHA-256 `bb51942c…b97b93e` | Descargado por la API REST de la Release (la descarga por GraphQL de `gh release download` está bloqueada en esta sesión); `tools/base_414.py materialize` + `verify`: 6.798/6.798, `complete:true`. Informes en `evidencias/preparacion/` |
| Hito 4.15 | `revision/4.15-hito1` = `059f4f68dca7acf465b5f5b21de2dede84c885ff` | Binarios 4.14 copiados sin sobrescribir; `sha256sum -c` de su MANIFIESTO: 7.004 OK, 0 fallos, 0 archivos de más. No se ejecutó `base_414.py` sobre la 4.15 |
| Libro | `…_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx`, SHA-256 `d2593777650f…9c92385` | Idéntico en 4.14 y 4.15. Solo lectura de valores en caché con openpyxl |
| Fuentes | URD 2021, 2022, 2023 y 2025 (inglés) y DEU 2024 (francés) de `elis_decisiones/Elis/fuentes_pdf/` | SHA-256 de [datos/fuentes.json](datos/fuentes.json); coinciden con `HUELLAS_PDF.txt` y con los homónimos de `elis_motor_A` |
| Frente técnico | `claude/hopeful-bardeen-qap6y0`, observado en `d1f1fa9` (hito 2), en `c0dcbd0` (15-nov, 17:25 UTC) y en `56fca94` (15-nov, 19:20 UTC) | Hasta `d1f1fa9` solo añade a los componentes de C48 la cifra publicada con su signo (`valor_fuente` negativo, `signo` −1): no cambia valores, el 108,0 ni la plantilla V6.3. `bc48f9d`, `c554cc0` y `c0dcbd0` cambian el verificador de entradas, el pipeline y sus pruebas (U6, U7, H-P1/X2). `10018ad` y `56fca94` limitan el bloque `verificacion_entradas` de la ficha a los expedientes con registro de entradas o declaración del modo (I20), ajustan pruebas y `verificar_paquete.sh` y registran la regresión. Ninguno toca `v6/`, los datos de Elis ni `fase1_historia.py`. Sin cambios de datos o definiciones que afecten a F1. **Recomprobar al integrar** |

**Regla de edición** [D]: cada ejercicio se toma de la publicación más reciente que lo presenta, que es la regla de la Historia. 2025 y 2024 proceden del URD 2025; 2023 del DEU 2024 reexpresado; 2022 del URD 2023 reexpresado; 2021 del URD 2022 reexpresado. Las reexpresiones son pequeñas y proceden sobre todo de la contabilización definitiva de combinaciones: la PPA pasa de 80,1 a 82,9 en 2022, de 85,1 a 85,7 en 2023 y de 84,9 a 85,0 en 2024. Hay además un cambio de presentación: hasta el URD 2023 los intereses de arrendamientos iban dentro de «Net interest paid» (90,2 en 2023); desde el DEU 2024 van dentro de los pagos de arrendamientos (70,5 + 130,8) [P: URD23 p.266, p.279; DEU24 p.273].

**Evidencia reproducible.** Todas las rutas son relativas a esta carpeta.
- `datos/cifras_fuente.csv`: 752 filas (713 de tabla y 39 de texto). Cada una lleva documento, página PDF, etiqueta de línea, posición, literal impreso, valor con signo, unidad, perímetro, edición («vigente» o «anterior») y modo de control del ejercicio.
- `scripts/verificar_cifras.py` comprueba cada fila en seis dimensiones y deja cada una en OK (ninguna incoherencia detectada), PENDIENTE (motivo escrito), FALLO o, si no procede, NO_APLICA:
  - **literal:** huella declarada, página, etiqueta, posición, literal y signo;
  - **ejercicio:**
    - en las tablas de dos ejercicios, la columna del token se identifica con su cabecera: por orden, si la cabecera tiene tantas columnas reconocidas (años, «Change», «Notes») como números la línea; si no, por alineación horizontal. Desde C9, si otra palabra de la cabecera que no es una columna reconocida (un país, una sociedad, un ajuste) está más cerca del token que la columna del ejercicio, el ejercicio queda sin acreditar. Desde C12 (revisión n.º 5, Q1–Q3):
      - dos columnas del mismo año en posiciones distintas son columnas distintas («published» y «restated»; «12/31/2020» y «01/01/2020»); si dos cabeceras ocupan el mismo sitio, manda la línea más cercana a la fila;
      - una columna de apertura («01/01/2020») es del ejercicio anterior;
      - las palabras de la celda de una columna reconocida y las llamadas con letra («(a)») no son cabeceras ajenas;
      - si la columna reconocida más próxima es de otro ejercicio, la fila queda en FALLO, no en PENDIENTE. Desde C14, solo si esa columna está alineada con el token, a 5,5 caracteres o menos; si no, PENDIENTE (revisión n.º 6, R3);

      Desde C14 (revisión n.º 6, R1):
      - la asignación por orden exige además que cada número de la línea esté alineado con su columna, a 14 caracteres o menos. Una cuenta de columnas que coincide por accidente ya no desplaza las cifras (URD 2022 p.302). En las columnas de concepto (familias) no se exige: sus cabeceras van alineadas a la izquierda;
      - si entre la declaración de unidades y la fila empieza otra tabla, la cabecera es la de esa tabla y no la de la anterior;

      Desde C16 (revisión n.º 7):
      - el título numerado de la tabla y su continuación sangrada no son cabecera de columnas: su año no es una columna (S1);
      - una fila de saldo cuyo rótulo lleva la fecha («Balance as at December / 31, 2021») es de ese ejercicio (S1). En el barrido del revisor n.º 6, 346 candidatas pasaron así a OK en C16: 341 cifras de saldos y cinco tokens que no son cifras (el año de una línea de prosa, el día de la fecha y la pestaña del margen); con los años sueltos, 411 (revisión n.º 8, §4.3 y T7 a);
      - la primera línea de un rótulo partido, justo encima de la fila, no es la cabecera de ejercicios (S4);

      Desde C18 (revisión n.º 8):
      - la regla de la fecha del rótulo solo vale en una fila de saldo: el rótulo es la primera celda de una línea con más celdas, solo dice la fórmula del saldo y la fecha (con «restated», «retraité», «published» o una llamada) y el token está a su derecha. De las líneas de encima se unen las justas para que el rótulo lleve la fórmula y la fecha, sin absorber la cabecera de columna ni la línea de unidades. No la toman el día, el año ni la pestaña del propio rótulo, la prosa ni los títulos con fecha, ni la fila que está bajo la línea que continúa el rótulo de la anterior (T2). Un año suelto dentro del rótulo de texto de la fila, o el día de su fecha, no es una cifra: queda PENDIENTE en el ejercicio con cualquier regla, también con la de las columnas, que daba OK al año de cuatro rótulos de saldo alineado con la columna del ejercicio anterior. Tampoco toman el ejercicio de la fecha los recuentos con fecha (número de acciones, planes de acciones, autocartera): su ejercicio vuelve a la regla de las columnas, como en C14, con el coste que se declara en la octava parte de las respuestas;
      - el rótulo del saldo puede estar partido en dos o tres líneas, también tras el día o tras el año («SOLDE AU 31 / DÉCEMBRE 2024»; «BALANCE AS AT / DECEMBER 31, 2021 / (RESTATED)»). Lo que se une depende de por dónde parta la línea `pdftotext` (T3);
      - si la fila tiene varias columnas de datos, la columna del token es un concepto (clase de activo, componente del patrimonio) que el modo de dos columnas no declara: queda PENDIENTE. Por eso los saldos de las tablas de varias columnas (estados de cambios en el patrimonio, movimientos de intangibles, inmovilizado y derechos de uso) quedan con el ejercicio OK y la fila PENDIENTE; con una sola columna de datos, OK (T1);
    - en las demás, tabla de crecimiento (solo porcentajes), bloque de movimientos, saldo con fecha, apertura y cierre en la cabecera o año aislado sobre la tabla;
    - el modo de cada concepto es una lista cerrada (`modo_admitido`): la fila no puede declarar otro;
    - en la prosa, el ejercicio de la publicación;
  - **columna:** en las tablas de varias columnas que no son ejercicios (crecimiento, impuestos diferidos, arrendamientos, intangibles, inmovilizado y matrices), la cabecera de la columna del token debe ser la del concepto;
  - **unidad:** la declaración de unidades de la tabla, o el «%» del literal. Una línea cuyo rótulo está en la lista de recuentos, importes por acción, márgenes, años o euros no puede ser «mm EUR». Desde C10, un entero de seis cifras o más queda PENDIENTE por su formato, sin depender del rótulo (revisión n.º 4, P1). Una declaración de otra unidad o de otra tabla deja la fila en FALLO o PENDIENTE;
  - **perímetro:** la cabecera de la página debe ser de estados consolidados o de resultados del grupo. No son del grupo las filas de un segmento (por rótulo, en una tabla por segmentos, o por columna en una matriz, asignada por posición horizontal) ni las de un país en una tabla por países, ni las sublíneas de un segmento, ni, desde C9, la columna de un país en una tabla con columnas por país. Desde C10 y C12, una fila cuyo título de bloque nombra un país o un segmento («FRANCE – DETAILS») deja el perímetro del grupo PENDIENTE. Se busca el primer título, en mayúsculas y en línea propia, desde la fila hasta el principio de la página y, si no lo hay, al final de la anterior (revisiones n.º 4, P2, y n.º 5, Q4). Desde C12, los rótulos de segmento se comparan normalizados («and», «et» y «&»; sin «CGU»), y un rótulo partido en dos líneas se une (revisión n.º 5, Q5). Desde C14 (revisión n.º 6):
    - no son del grupo las filas de una jurisdicción, de una región o del desglose de un país («› of which Ireland», «European Union (excluding France)», «Hors Union européenne»), con el rótulo unido aunque ocupe varias líneas (R1);
    - una columna de un grupo de columnas por entidad o por medida deja el perímetro PENDIENTE. Es el caso en que la cabecera repite los mismos ejercicios en cada grupo: «Elis · Le Jacquard Français · Kennedy Hygiene», cada una con 2025 y 2024, o las firmas auditoras (R1);
    - un encabezado numerado de nota o de apartado («NOTE 13 …», «5.4 …») cuenta como título y corta la búsqueda (R2);
    - vuelve el criterio de C10, acotado: el título corto de una sola celda que va encima de la cabecera de la tabla y nombra un país («Mexico», «Interest rate swap – Chile») deja el perímetro PENDIENTE; la prosa, las líneas con cifras y las de datos cortan la búsqueda (R4);
    - una cabecera que nombra tres países o más y no tiene ninguna columna reconocida deja el perímetro PENDIENTE (R4);
    - el prefijo «CGU»/«UGT» se quita también al comparar el rótulo con los países: la tabla del fondo de comercio por UGE es una tabla por países (R5);
    - desde C16 (revisión n.º 7): una línea de cifras sin rótulo toma el de las líneas de rótulo contiguas de arriba y de abajo (S2); la pestaña del capítulo en el margen («6») no es el rótulo (S3); una tabla sin declaración de unidades ni línea de ejercicios con una cabecera de columnas por país deja el perímetro PENDIENTE (S4); un encabezado numerado en prosa, con comillas o puntuación final, no cuenta como título (S5);
    - desde C18 (revisión n.º 8): las líneas de rótulo contiguas son cortas (45 caracteres o menos) y están en el margen izquierdo, y no se buscan para una línea que empieza por la pestaña del capítulo ni para un rótulo con viñeta («− Matthieu Lecharny») (T5); la primera línea en mayúsculas del rótulo de una fila no corta la búsqueda de la cabecera por países: en C16 las dos últimas filas de la tabla del WACC por país del DEU 2024 p.315 conservaban el perímetro OK (T4); «Note N to the…» no es un encabezado, y un título en mayúsculas lo es aunque lleve comillas o se parta tras una coma (T6);
  - **edición:** el pie de cada página («Elis | Universal Registration Document AAAA») debe coincidir con la fuente, y la fuente debe ser la que exige la regla de edición de la Historia o estar declarada «anterior». Desde C12, la columna «published», «reported» o «publié» de una tabla de reexpresión no puede declararse vigente: es la cifra de la edición anterior (revisión n.º 5, Q1). Desde C14, una cifra bajo una cabecera ajena, como la columna de ajuste «IFRS 3», ya no se marca como de la columna publicada (revisión n.º 6, R8 b).

  Límites que quedan:
  - el perímetro se reconoce por la página, los rótulos y títulos de segmento y de país, las columnas por país y las matrices;
  - la unidad, por la declaración más próxima, por los rótulos de la lista y por el formato de recuento;
  - una cifra de otro perímetro o de otra unidad sin ninguna de esas señales no se detectaría. Las reglas son listas y criterios conocidos, no una acreditación;
  - la asignación de columnas es heurística y depende de la rejilla de caracteres de pdftotext. Precisado en C14 (revisión n.º 6, R7 a):
    - en las tablas con varias medidas bajo una misma fecha, la columna que queda bajo la fecha se acepta, como el valor en libros de la tabla de instrumentos financieros (URD 2023 p.338), y las demás quedan PENDIENTE;
    - en las de vencimientos, el valor en libros y el total sin descontar quedan PENDIENTE. En C12 el URD 2022 p.302 daba un OK y un FALLO (R1), y el DEU 2024 p.323, FALLO a los valores en libros (R3);
    - bajo una cabecera ajena, una cifra queda en FALLO si la columna de otro ejercicio está alineada con ella y en PENDIENTE si no;
  - la regla de grupos de columnas no distingue una columna por firma auditora (los honorarios que el grupo paga a cada firma) de una por marca: las dos quedan PENDIENTE (revisión n.º 6, R1 y R2). No ve la tabla de las hipótesis por marca de los URD 2021, 2022 y 2023, que no tiene ejercicios en la cabecera ni nombra ningún país. En los tres, su perímetro queda PENDIENTE solo porque lo retiene el título de país de la tabla anterior, con un motivo inexacto: «Switzerland» en el URD 2021 p.272, «Sweden» en el URD 2022 p.305 y en el URD 2023 p.324 (revisión n.º 7, §5 a y S7 d; precisado en C18, revisión n.º 8, §5 a y T8 d: hasta C16 se situaba solo en el URD 2022). Corregir el motivo dejaría su perímetro en OK; hoy sus filas seguirían PENDIENTE por el ejercicio, porque su cabecera no tiene columnas de ejercicio;
  - por eso cuentan la segunda línea y la cobertura de `contraste_f1.py`, y por eso las 8 páginas sin identidad entre páginas quedan como cobertura pendiente.

  Resultado: 738 sin incoherencia detectada, 14 PENDIENTE (URD 2022 p.302, sin unidad ni cabecera de columnas localizables) y 0 FALLO. Código de salida 2: hay pendientes. La salida guarda las huellas del CSV y de `fuentes.json`.
- `scripts/sondas_metadatos.py`: reproduce las sondas externas sobre eb77dea, que cambian un solo campo con el año correcto, y las extiende a todas las filas de tabla. Primero cambia solo la unidad de cada fila; después, solo el perímetro. Resultados en `resultados/sondas_metadatos_*.json`:
  - en eb77dea no detecta ninguna (0 de 671 en cada caso): la unidad y el perímetro no se comprobaban;
  - en el commit congelado 1864c4e detecta 677/677 en unidad y 673/677 en perímetro. Las 4 restantes son totales de una matriz por segmentos declarados «segmento Francia», que quedaban PENDIENTE en lugar de FALLO;
  - en f30c66c, 677/677 en las dos; en C7, 697/697; en C9, 704/704; en C12, 711/711, y en C14 y C16, 713/713.

  **Qué miden** (revisión n.º 3, N10): que una etiqueta cambiada se detecta, no que se rechace una cifra de otra unidad o de otro perímetro con una etiqueta verosímil. Esos casos (P1, P2a, U1, U2, B1, B2 y C1 de la revisión n.º 3) son contraejemplos del test.
- `scripts/test_verificar_cifras.py`: 136 casos: 23 positivos reales, 36 PENDIENTE esperados y 77 contraejemplos, y nueve comprobaciones directas de funciones del verificador, que se cuentan aparte. Los casos de las revisiones n.º 5 a 8 se construyen desde la página del PDF, con la línea fijada entera, como en los scripts de los revisores. Algunos fijan además el estado de una dimensión concreta o exigen que un motivo no aparezca, en la fila o en el detalle de una dimensión. Cada contraejemplo debe detectarse en su dimensión. En los mutantes coherentes se cambian a la vez la posición, el literal, el valor, la página o la fuente, de modo que el literal sigue siendo el impreso: solo la dimensión señalada puede rechazarlos y las demás no deben fallar.
- `scripts/contraste_f1.py`: 292 comprobaciones, todas OK, de tres clases:
  - 136 contra el libro. 18 de ellas son de una copia temporal del libro recalculada con LibreOffice con exceso de caja de 0, 250 y −80 (`scripts/prueba_caja_no_nula.py`);
  - 127 de fuente: las dos vías independientes del FCF base y 126 residuos de conciliación, cada uno afirmado con su cota de redondeo y una sola diferencia de concepto fijada;
  - 29 identidades algebraicas, que documentan los puentes, la identidad del exceso de caja, A3_estimado con valores sintéticos y el control del año 11. No prueban los datos.

  Solo calcula con una verificación del mismo CSV (huella, literal y valor de cada fila) y con cifras sin FALLO, de la edición vigente, del perímetro del grupo y con la unidad que pide cada cálculo. Son 419 entradas, ninguna pendiente; una contraparte de identidad pendiente (`LS_AMORT_ROU_2021`) se anota aparte. La revisión n.º 3 cuenta, sobre 1864c4e, 320 entradas con efecto en alguna salida. Sobre C14, la prueba de mutación da 411 con efecto y 8 que el cálculo lee sin efecto en ninguna salida. La tabla `cobertura_entradas` clasifica cada entrada según qué la comprueba además de su literal.
- `scripts/test_contraste_residuos.py`: 24 casos. Salta a propósito el verificador y comprueba que los residuos hacen fallar el cálculo con una cifra de otro año o de otra línea (2022), con un error nuevo mayor que la cota en las cifras de la excepción fijada o en el FCF de 2024, con ventas mal transcritas, con el crecimiento externo en lugar del orgánico, con una línea del circulante de 2021 y, desde C9, con el impuesto de 2022 sin reexpresar, las ventas de 2020 y las adquisiciones de 2022 de otra columna. Desde C12, también con el resultado antes de impuestos y la D&A total de 2021–22, las adquisiciones de 2023 de otra columna y el crecimiento publicado de un segmento. Desde C14, con las ventas de 2021 y de 2022 dentro del intervalo que R42 no detecta: R23 sí lo detecta (revisión n.º 6, R6). También comprueba que el cálculo se niega si la verificación no es la del CSV. Documenta el límite de detección: un error menor que la cota de redondeo no lo detecta ningún residuo. Ejemplos: 29,3 o 29,1 en lugar de 29,2 en el gasto devengado, 178,0 en lugar de 177,9 en los pagos, o la cifra publicada de las adquisiciones de 2021 antes de la reexpresión (86,9 en lugar de 86,8). El caso de los pagos sí lo detectan la doble vía del FCF base y 41 comprobaciones del libro; el de las adquisiciones, 2 del libro (revisión n.º 4, P4).
- `scripts/cobertura_por_mutacion.py`: suma 3,0 a cada una de las 530 filas de tabla de la edición vigente, con el verificador saltado, y clasifica qué detecta el cambio. Es la prueba del revisor n.º 3 con un solo cambio: la verificación falsa corresponde a cada CSV mutado, porque desde C7 el contraste rechaza la de otro CSV. Resultado (`resultados/cobertura_por_mutacion.txt`):
  - 386 detectadas por una identidad de fuente y 2 solo por la comparación con el libro;
  - 23 cambian alguna salida sin que nada falle: son las declaradas sin segunda línea, y ninguna cambia la referencia de la especificación;
  - 8 se leen sin efecto en ninguna salida y 111 no se usan;
  - ninguna difiere de la clase que declara `cobertura_entradas`;
  - ninguna entrada sin identidad entre páginas mueve la referencia, tampoco las de solo identidad de su página. Desde C12 la prueba informa también de esa clase (revisión n.º 5, Q6).

  `cobertura_entradas` dice además qué acredita cada clase, marca para cada entrada si su página tiene alguna identidad entre páginas y lista las 8 páginas que no (revisión n.º 4, P3).

  Resultados en `resultados/contraste_f1.{json,md}`.
- `resultados/tabla_conciliacion.md`: tabla de cifras con literal y página.
- `evidencias/paginas/`: texto de cada página citada, con la huella de su PDF.

---

## 2. Conciliación anual 2023–2025

La tabla completa, con literal impreso y página de cada cifra, está en [resultados/tabla_conciliacion.md](resultados/tabla_conciliacion.md). Resumen en millones de euros, con el signo convertido al uso del modelo:

| Partida | 2023 | 2024 | 2025 | Fuente (página PDF) |
|---|---|---|---|---|
| Ventas | 4.309,4 | 4.573,7 | 4.796,8 | DEU24 p.270; URD25 p.324 [P] |
| EBIT publicado (resultado operativo) | 496,8 | 596,3 | 629,9 | ídem [P] |
| EBIT de la Historia (BAI + financiero) | 496,8 | 596,3 | 630,0 | [D]; residuo 2025 de +0,1 por redondeo |
| D&A total neta (fila 8) | 877,4 | 965,1 | 1.019,4 | DEU24 p.296; URD25 p.350 [P] |
| · lino propio / otros artículos propios / resto | 482,1 / 32,7 / 161,6 | 537,6 / 35,3 / 172,5 | 565,1 / 36,3 / 183,6 | ídem [P] |
| · derechos de uso NIIF 16 | 115,8 | 132,2 | 149,5 | ídem [P] |
| · intangibles de combinaciones (PPA) | 85,7 | 85,0 | 85,7 | ídem [P] |
| · subvenciones (−) / deterioros (+) | 0,5 / 0,0 | 0,9 / 3,3 | 1,0 / 0,1 | ídem [P] |
| Provisiones: dotación neta | 8,1 | −2,6 | 0,4 | ídem [P] |
| Caja antes de financieros e impuestos | 1.457,9 | 1.584,0 | 1.661,3 | DEU24 p.273; URD25 p.327 [P] |
| Circulante (consumo +) | 5,9 | 6,9 | 4,0 | [P] APM; = −Σ líneas del EFE [D] |
| Impuestos pagados | 126,4 | 124,9 | 146,7 | [P] |
| CFO | 1.325,6 | 1.452,1 | 1.510,6 | [P] |
| Capex bruto (intangibles + material) | 823,9 | 887,4 | 890,2 | [P] |
| · lino / otros artículos / resto | 584,3 / 37,3 / 202,3 | 594,3 / 34,6 / 258,6 | 594,2 / 40,8 / 255,2 | DEU24 p.257; URD25 p.311 [P] |
| Cesiones + subvenciones de inversión | 2,9 + 0,3 | 7,3 + 4,1 | 15,3 + 0,2 | ídem [P] |
| Capex neto («Net capex», C47) | 820,8 | 876,0 | 874,7 | DEU24 p.259; URD25 p.314 [P] |
| Adquisiciones netas de caja (fila 13) | 82,1 | 183,3 | 117,6 | [P] |
| SBC no monetario (C50) / cargas sociales / IFRS 2 total | 22,9 / 8,2 / 31,1 | 27,1 / 4,3 / 31,4 | 34,7 / 11,2 / 45,9 | DEU24 p.259, p.273; URD25 p.314, p.327, p.345 [P]; suma exacta [D] |
| Pagos de arrendamientos (principal + intereses) | 130,8 | 150,8 | 177,9 | [P] |
| · principal (C49) | 111,0 | 125,0 | 148,3 | DEU24 p.312; URD25 p.366 [P] |
| · interés implícito de caja (pagos − principal) | 19,8 | 25,8 | 29,6 | [D] |
| · interés devengado (nota 8.2) | 19,8 | 25,8 | 29,2 | DEU24 p.324; URD25 p.379 [P] |
| Intereses financieros netos pagados (sin arrendamientos) | 70,5 | 78,9 | 99,4 | [P] |
| Gasto por impuesto / corriente / diferido | 110,3 / 120,3 / −10,1 | 128,3 / 127,7 / 0,6 | 126,2 / 147,2 / −21,0 | DEU24 p.337; URD25 p.392 [P] |
| Deuda financiera bruta / caja / neta | 3.690,7 / 665,3 / 3.025,4 | 3.660,1 / 622,0 / 3.038,0 | 3.418,3 / 398,1 / 3.020,2 | DEU24 p.329; URD25 p.384 [P] |
| Pasivo por arrendamientos | 538,3 | 606,2 | 703,2 | [P] |
| Free cash flow publicado (APM) | 303,6 | 346,3 | 358,6 | DEU24 p.259; URD25 p.314 [P] |

**Identidades y residuos** (cálculo exacto; `resultados/contraste_f1.md`, primera tabla) [D]:

| Identidad | 2023 | 2024 | 2025 | Explicación |
|---|---|---|---|---|
| EBIT → caja antes de financieros e impuestos (NI + impuesto + financiero + SBC + amortizaciones y provisiones + subvenciones + plusvalías + earnout) | 0,0 | 0,0 | +0,1 | Redondeo de líneas impresas |
| Caja antes − circulante − impuestos pagados = CFO | 0,0 | −0,1 | 0,0 | Redondeo |
| D&A: componentes = total | 0,0 | +0,1 (D&A en EBIT) | +0,1 (total) | Redondeo de componentes |
| Línea del EFE «amortizaciones y provisiones» = D&A total + subvención + provisiones | 0,0 | 0,0 | 0,0 | Exacta: 1.020,8 = 1.019,4 + 1,0 + 0,4. **No se sustituye 1.019,4 por 1.020,8**: la diferencia son subvenciones y provisiones |
| Capex bruto del EFE = lino + otros + resto | 0,0 | −0,1 | 0,0 | Redondeo |
| Capex neto = bruto − cesiones − subvenciones | +0,1 | 0,0 | 0,0 | 2023: 820,8 publicado frente a 820,7 de las líneas; ya registrado en C47 |
| FCF publicado = suma de sus componentes | +0,1 | **−0,2** | 0,0 | 2024: la tabla del URD 2025 imprime 346,3 (346,4 en el DEU 2024) frente a 346,5 de sus componentes. Dentro de la cota de redondeo de sus siete cifras impresas (0,35); no afecta a C52, que se construye por la vía CFO |
| Interés de arrendamientos: caja − devengo | 0,0 | 0,0 | **+0,4** | Diferencia de concepto, fijada en +0,4 (§5.4) |
| Movimiento del pasivo y del ROU | 0,0 | 0,0 / −0,1 | 0,0 | Redondeo |
| Impuesto corriente + diferido = gasto | −0,1 | 0,0 | 0,0 | Redondeo |
| Deuda bruta − caja = deuda neta | 0,0 | +0,1 | 0,0 | Caja 622,0 frente a 622,1 entre ediciones |
| Segundas presentaciones en otra página: resultado financiero (nota 9), resultado antes de impuestos (conciliación del impuesto), PPA (cuenta de resultados frente a nota de D&A), ventas (información por segmentos) y adquisiciones (puente de la deuda neta; 2024–25) | 0,0 | 0,0 | 0,0 | Contraste entre páginas de las entradas clave |
| Amortización ROU: nota de D&A − movimiento de arrendamientos (R16) | **−0,1** | 0,0 | 0,0 | 2023: cota 0,10, la agota. La nota 4.5 imprime 115,8 (DEU 2024 p.296) y el movimiento 115,9 (p.312: 48,2 + 64,1 + 3,6). E1 fija la nota 4.5 como fuente |
| Totales de los flujos de inversión y de financiación; capex neto entre tabla de capex y tabla del FCF; crecimiento publicado = orgánico + externo + divisa; resultado neto; impuesto de la conciliación del tipo; otros ingresos operativos (2024–25) | 0,0 | 0,0 / +0,1 (financiación) | 0,0 | Segunda línea de entradas sin identidad en la revisión n.º 3 (N2) |
| Saldos de cierre de 2023 en el DEU 2024 = apertura de 2024 en el URD 2025 (ROU, pasivo y relaciones con clientes) | — | 0,0 | — | Dos ediciones vigentes para la misma fecha; prevalece la más reciente si difieren (N8 f) |

**Horizonte 2021–2022** (años que solo entran en el ancla de S2C): D&A total = componentes (0,0 y +0,1), amortización ROU de la nota = movimiento (0,0 y 0,0), PPA de la cuenta de resultados = nota (0,0 y 0,0), capex por tipo, EBIT y free cash flow publicado, todas dentro de su cota (N2). También el circulante del APM frente a las líneas del EFE (+0,1 y 0,0, cota 0,40): da una segunda línea entre páginas a las 14 líneas de circulante que entran en el ancla. Desde C9 (residuos 0,0 en todos los casos):
- R17: impuesto corriente + diferido de la nota 9 (URD 2022 p.326; URD 2023 p.345) frente al gasto de la cuenta de resultados;
- R39: adquisiciones del EFE frente al flujo neto total de la nota de combinaciones de negocio (URD 2022 p.277; URD 2023 p.294);
- R40: ventas de 2020 de la cuenta de resultados del URD 2021 (p.226) frente a las del informe de gestión (p.213).

Desde C12 (revisión n.º 5, Q5 y Q6):
- R41: resultado antes de impuestos de la cuenta de resultados frente al de la nota 9 (URD 2022 p.326; URD 2023 p.345);
- R8 de 2021–22: línea del EFE de amortizaciones y provisiones frente a la D&A total más la subvención y las dotaciones netas a provisiones (URD 2022 p.261 y p.284; URD 2023 p.279 y p.301), como en 2023–25;
- R24 de 2023: adquisiciones del EFE frente al puente de la deuda neta del DEU 2024 (p.260);
- R42, de 2021 a 2025: crecimiento publicado frente al crecimiento de las ventas de las cuentas de resultados.
  - Residuos de −0,045 a +0,022, con cotas de 0,052 a 0,054 [D]. No es lineal: la cota se calcula linealizando.
  - Ancla las tablas de crecimiento, porque una fila de segmento la rompe.
  - Su sensibilidad a las ventas es pequeña (revisión n.º 6, R6). Ninguna R42 detecta en las ventas errores de −0,78 a +1,99 en 2020, de −0,20 a +0,85 en 2021, de −2,30 a +0,26 en 2022, de −0,78 a +2,59 en 2023, de −3,24 a +0,83 en 2024 y de −1,38 a +3,40 en 2025 [D]. Hasta C12 era lo único que contrastaba entre páginas las ventas de 2021 y 2022; desde C14 las ventas de todos los años tienen además R23 o R40, que las contrastan por encima de ±0,1.
  - En el crecimiento publicado, R42 no detecta errores de −0,030 a +0,077 puntos en 2021, de −0,008 a +0,099 en 2022, de −0,068 a +0,038 en 2023, de −0,019 a +0,085 en 2024 y de −0,074 a +0,030 en 2025 [D] (`cobertura_entradas.umbrales_entre_paginas`).
  - Compara el crecimiento de la publicación de cada ejercicio con las ventas de la edición vigente, que es la siguiente. Cierra porque las ventas no se reexpresaron. Si se reexpresaran, fallaría sin error en los datos [I] (observación de la revisión n.º 6, §5.3).

Desde C14 (revisión n.º 6, R6):
- R23 de 2021–22: ventas de la cuenta de resultados frente a la información por segmentos de la publicación vigente (URD 2022 p.258 y p.279; URD 2023 p.276 y p.296), como en 2023–25. Residuo 0,0 los dos años, cota 0,10. Las ventas de 2021 y 2022 quedan contrastadas entre páginas por encima de ±0,1.

El informe de gestión del URD 2022 (p.247) imprime las adquisiciones de 2021 como (86,9) bajo la cabecera «2021 restated». Es la cifra publicada antes del ajuste IFRS 3 de 0,1: la tabla de reexpresión (p.271) da (86,9) + 0,1 = (86,8), la del EFE [P]. Por eso R39 usa la nota 2.4 y no esa tabla. La diferencia, 0,1, queda dentro de la cota de R39: ninguna identidad distingue la cifra publicada de la reexpresada.

Cada identidad se **afirma** con su cota de redondeo: para cada cifra impresa que interviene, |coeficiente| × media unidad de su última cifra (0,05 con un decimal). Es el error máximo que puede producir el redondeo de las cifras publicadas. No hay tolerancia global: un residuo mayor que su cota hace fallar el cálculo, salvo la diferencia de concepto de 2025, que se exige en su valor exacto (+0,4 ± 0,15). La tabla `residuos_con_cota` de `resultados/contraste_f1.json` da, para cada identidad y año, el residuo, la cota, las cifras y las páginas que intervienen, y si el contraste es entre páginas o dentro de una.

**Historia y Análisis frente a la fuente** [D]. Se contrastaron 72 celdas de Historia y todas coinciden exactamente con las cifras publicadas:
- 64 de filas: 6, 7, 8, 10, 11, 12, 13, 14, 15, 17 y 18 de 2021–2025, y 22, 23 y 24 de 2023–2025;
- G6 (ventas 2020);
- las anclas C52, C58, C70, C74–C76 y C79.
 Las celdas de Análisis C46–C52 coinciden con las medias publicadas redondeadas a tres decimales: el libro registra 1.429,433, 857,167 y 28,233 frente a las medias exactas 1.429,4333…, 857,1666… y 28,2333…. Por eso C52 vale 307,933 frente a 307,93333. El efecto en f es −7,3·10⁻⁸ y en los flujos ≤ 0,0006 mm. No es material, pero «exacto» en el registro significa redondeado a tres decimales; la especificación debe fijarlo (§E7 de la especificación).

---

## 3. Horizonte 2021–2025 (S2C)

| | 2021 | 2022 | 2023 | 2024 | 2025 |
|---|---|---|---|---|---|
| Ventas (2020: 2.806,3) | 3.048,3 | 3.820,9 | 4.309,4 | 4.573,7 | 4.796,8 |
| Crecimiento orgánico [P] | 7,4 % | 21,0 % | 11,8 % (efecto precio ≈ +9 %) | 5,2 % | 3,8 % |
| Capex bruto | 573,9 | 699,8 | 823,9 | 887,4 | 890,2 |
| · lino − amortización de lino | 19,8 | 94,8 | 102,2 | 56,7 | 29,1 |
| D&A total / ROU / PPA | 744,8 / 92,6 / 81,1 | 799,0 / 103,7 / 82,9 | 877,4 / 115,8 / 85,7 | 965,1 / 132,2 / 85,0 | 1.019,4 / 149,5 / 85,7 |
| D&A propia (total − ROU − PPA) | 571,1 | 612,4 | 675,9 | 747,9 | 784,2 |
| Circulante (consumo +) | −10,2 | 52,6 | 5,9 | 6,9 | 4,0 |
| Adquisiciones | 86,8 | 221,7 | 82,1 | 183,3 | 117,6 |
| Fila 30: capex − D&A total + circulante | −181,1 | −46,6 | −47,6 | −70,8 | −125,2 |
| Capex − D&A propia + circulante | −7,4 | 140,0 | 153,9 | 146,4 | 110,0 |

Fuentes [P]: URD21 p.211 y p.226; URD22 p.243, 247, 258, 261 y 284; URD23 p.261, 266, 276, 279 y 301; más las de 2023–2025.

- **C53 (S2C marginal de 5 años) = 9,04** [D]: (4.796,8 − 2.806,3) ÷ Σ₂₀₂₁₋₂₅ (capex − D&A total + circulante + adquisiciones) = 1.990,5 ÷ 220,2. Su denominador usa la D&A total, que incluye ROU y PPA sin contrapartida en el capex. Con el mismo cálculo y la D&A propia sale 1,61; sin ROU, 2,45 (§9) [D]. Las palancas S2C del expediente (1 / 1,2 / 1,5) no usan C53. La fase C las ancló en «la inversión propia sobre la amortización propia de 2024–25 (S2C ≈ 1,5)» (`elis_decisiones/Elis/fase_c.json`, desviación G7) [I]. **El perímetro de las palancas S2C (propio) no es el de f (D&A total).**
- **Ruptura de presentación en las filas 15/16** [P][D]: 2021 y 2022 incluyen los intereses de arrendamientos (74,6 y 72,9, «including interest on lease liabilities», URD22 p.261), mientras 2023–2025 los excluyen. No afecta a C48, que usa 2023–25 y suma el interés de caja de arrendamientos aparte, ni a C58. Sí afecta a la comparabilidad de la fila 35 de 2021–22 y debe declararse si se amplía la ventana.
- **Fila 18 de 2021** [P][D]: 28,0 procede de la nota 5.2 («Equity-settled share-based payments», URD22 p.287); el EFE da 24,4 (URD22 p.261). Los demás años usan el EFE. Fuera de la ventana de f; se declara como incoherencia de fuente de la fila.
- **El crecimiento orgánico incluye precio en todos los años de la ventana** [P]:
  - en 2023, «price effect of +9% on average» (URD23 p.261);
  - en 2024, «effet prix … et … effet volume», con dinámica de precios favorable ligada a la inflación salarial (DEU24 p.121, 252–253);
  - en 2025, «price effect from residual inflation in 2025, and a volume effect», más ajustes de precio en Latinoamérica y en Reino Unido e Irlanda (URD25 p.122, 307).

  El reparto precio/volumen solo se cuantifica para 2023. Las anclas S2C calculadas sobre crecimiento orgánico nominal sobrestiman la productividad del capital en volumen, también en 2024–25 [I] (revisión, O2).

---

## 4. Puente del FCF base 307,933 a f y al motor A

### 4.1 FCF base (Análisis C46–C52)

FCF base = CFO − capex neto − (intereses financieros + interés de caja de arrendamientos) − principal de arrendamientos − SBC no monetario, en media 2023–25 [DH 10-nov-2026 y E6; D]:

| Año | CFO | − capex neto | − intereses fin. | − interés arr. (caja) | − principal arr. | − SBC | = FCF base del año | Vía FCF publicado − SBC |
|---|---|---|---|---|---|---|---|---|
| 2023 | 1.325,6 | 820,8 | 70,5 | 19,8 | 111,0 | 22,9 | 280,6 | 280,7 |
| 2024 | 1.452,1 | 876,0 | 78,9 | 25,8 | 125,0 | 27,1 | 319,3 | 319,2 |
| 2025 | 1.510,6 | 874,7 | 99,4 | 29,6 | 148,3 | 34,7 | 323,9 | 323,9 |
| Media | 1.429,433 | 857,167 | 82,933 | 25,067 | 128,1 | 28,233 | **307,933** | 307,933 |

- **C48 = 108,0 = 82,933 + 25,067** [D]. Se mantiene. Sustituirlo por 82,933 dejaría sin restar 25,067 de pagos de arrendamientos (FCF base 333,0). Con el interés devengado en lugar del de caja sería 107,867. Ambas son variantes calculadas y **no adoptadas**: el FCF base es un concepto de caja y C48 está conciliado con E6 [DH].
- El cupón en caja de la OCEANE (2,25 % sobre 380,0, URD25 p.380 [P]) está dentro de los intereses pagados según el registro E6; el devengo no monetario del componente de deuda no está [DH E6]. No se cambia.
- FCF base = media del free cash flow publicado − media del SBC (336,167 − 28,233). Las dos vías coinciden en la media aunque por año difieran en ±0,1 [D].

### 4.2 f y su composición económica

Definición de la plantilla (Convenciones V6.3 §10; Historia C58 y filas 73–81) [P/D]:

f = [NOPAT medio − reinversión media − FCF base] ÷ ventas medias = [416,799 − (−81,2) − 307,933] ÷ 4.559,967 = 190,066 ÷ 4.559,967 = **0,041681455**

con NOPAT = EBIT × (1 − tipo efectivo de cada año, fila 10, 4 decimales) y reinversión = capex bruto − D&A total + circulante.

**Descomposición independiente** [D]. Sustituyendo las identidades del estado de flujos, f·ventas es exactamente la suma de estos componentes (comprobado por año y en media):

| Componente de f·ventas (media 2023–25) | mm | Naturaleza |
|---|---|---|
| Principal de arrendamientos | 128,100 | caja, financiación |
| Interés de arrendamientos (caja) | 25,067 | caja, financiación |
| Intereses financieros netos pagados | 82,933 | caja, financiación |
| Escudo fiscal del gasto financiero (−τ·financiero) | −35,976 | el NOPAT aplica τ al EBIT; el impuesto real descuenta el gasto financiero |
| Impuesto pagado − gasto por impuesto | +11,067 | caja frente a devengo; incluye la reversión no monetaria del diferido de intangibles (§7) |
| Redondeo de τ a 4 decimales | +0,009 | redondeo |
| Capex neto − bruto (cesiones y subvenciones) | −10,000 | la reinversión usa capex bruto; el FCF base, neto |
| Plusvalías por enajenación (no monetarias en el EBIT) | +3,833 | 2025: +23,1 (bajas de inmovilizado +25,7 en OOIE) |
| Earnout y otros no monetarios | −13,000 | 2023: −48,4 por la reestimación del earnout de México, cargo no monetario en el EBIT 2023 |
| Provisiones | −1,967 | dotación neta no monetaria |
| EBIT de la Historia − EBIT del EFE; residuos del EFE | 0,000 | redondeos que se compensan |
| **Total = Historia C79** | **190,066** | |

Consecuencias [D]:
- f es, en sustancia, **236,1 de financiación y arrendamientos, menos 24,9 de efectos fiscales y menos 21,1 de partidas de la ventana**. Ni la amortización ROU ni la PPA son componentes de f. El SBC no está en f para Elis: se resta en el FCF base y ya está en el EBIT, así que se compensa. Las adquisiciones tampoco: no están en el FCF base.
- La afirmación del hallazgo de 14-nov, «f incluye 85,7 de amortización de intangibles», es imprecisa [I]. La PPA no está en f. Está en el EBIT y se devolvía en la reinversión histórica. Su efecto en la proyección se analiza en §6.
- Dos partidas de la ventana proyectan como fuga permanente algo puntual [I]:
  - el componente de earnout y otros no monetarios (−13,0 de media, dominado por el cargo de −48,4 de 2023) baja f en 0,29 puntos de ventas;
  - las plusvalías netas de la ventana (+3,8 de media; +23,1 en 2025) la suben en 0,08 puntos.

  Además, la plusvalía de 2025 (+25,7 en OOIE, con «a high level of insurance benefits in 2025», URD25 p.309 [P]) eleva m0 (13,13 %) unos 0,54 puntos.

  En el flujo sin crecimiento de la base 2025 estas partidas suman **+27,9**, común a todos los perímetros [D] (revisión, O9):
  - +13,7 del earnout dentro de f; si se cuenta también su efecto en el tipo de 2023, por no ser deducible, el efecto sube a ≈ 18,6. **Precisión** (respuesta a la revisión de la propuesta, P3): ese ≈ 18,6 es solo la parte de f (18,648) y no puede sumarse a los demás. El mismo ajuste baja el τ de 5 años, y su efecto conjunto en el flujo sin crecimiento es −14,314. El de los ajustes de earnout de 2023–25, simétricos y sin efecto fiscal, es −11,605 (`resultados/copia_investigacion_f1.md`);
  - −4,0 de las plusvalías dentro de f;
  - +18,3 de la plusvalía dentro de m0.

  No alteran las diferencias entre alternativas, pero equivalen al 20 % de la anchura del intervalo de §6.4. Son efectos de calibración documentados, no decisiones. Normalizarlos requeriría una regla decidida (especificación, E8). El +27,9 es un diagnóstico del cálculo conservado, no el efecto de una regla. Los ajustes concretos, con su regla fiscal y su cálculo conjunto, están en la propuesta de decisiones, §5.1.

### 4.3 Motor A: réplica y flujo de partida

Ecuaciones de la V6.3 (Convenciones §1–§3), reimplementadas sin leer las fórmulas de las celdas. Coinciden con los 30 flujos anuales (AU6:BD8), los 3 flujos del año 11 (BF6:BF8) y los 3 flujos sin crecimiento, con diferencias < 10⁻⁹ [D]. El flujo sin crecimiento se obtiene del libro como (Motor!BL − Motor!M)·r: Motor!BL = C·(D·(1 − K) − L)/J + M, y M es el exceso de caja del motor A (= Análisis!C76). La identidad se comprobó también con un exceso de caja de 250 y de −80 en una copia temporal del libro recalculada con LibreOffice. La identidad anterior, BL·r − C76, solo acierta con caja cero, que es el caso del libro (revisión, O15):

- flujo_t = V_t·[m_t·(1 − τ) − f] − (V_t − V_{t−1}) ÷ S2C; terminal = V₁₀·(1+g)·[m_obj·(1 − τ)·(1 − g/ROIC) − f].
- V₀ = 4.796,8; m₀ = 630,0/4.796,8 = 13,134 %; τ = 28,82 % (media de 5 años de la fila 10); f = 4,168 %.
- **Flujo sin crecimiento F₀ = V₀·[m₀(1 − τ) − f] = 248,496.**

**Puente FCF base → F₀** [D]:

| Paso | mm |
|---|---|
| FCF base (C52) | 307,933 |
| + nivel del EBIT 2025 (630,0) frente a la media 2023–25 (574,367), al τ de 5 años | +39,600 |
| + τ de 5 años (28,82 %) frente al τ de cada año en la ventana (NOPAT 408,834 frente a 416,799) | −7,965 |
| − f aplicada a las ventas 2025 en lugar de las medias | −9,872 |
| + reinversión histórica media (C76) que la proyección no reproduce | −81,200 |
| **= F₀** | **248,496** |

**Puente F₀ → año 1** [D] (palancas del expediente, que son juicio de la fase C y no se discuten aquí):

| | MALO | NORMAL | BUENO |
|---|---|---|---|
| F₀ | 248,496 | 248,496 | 248,496 |
| + NOPAT por ventas y margen del año 1 | −9,376 | +15,657 | +27,302 |
| − f sobre el aumento de ventas | −3,999 | −8,997 | −10,997 |
| − reinversión de crecimiento ΔV/S2C (S2C = 1 / 1,2 / 1,5) | −95,936 | −179,880 | −175,883 |
| = flujo del año 1 | 139,185 | 75,276 | 88,920 |

### 4.4 Qué es el −81,2

Descomposición exacta de la reinversión media C76 [D]:

| Bloque (media 2023–25) | mm |
|---|---|
| Lino: compras − amortización | +62,667 |
| Otros artículos propios en alquiler: compras − amortización | +2,800 |
| Resto de inmovilizado e intangibles: compras − amortización | +66,133 |
| Subvenciones (+) y deterioros (−) | −0,333 |
| Residuo de redondeo | −0,100 |
| Circulante | +5,600 |
| **Inversión neta propia + circulante** | **+136,767** |
| − amortización de derechos de uso NIIF 16 | −132,500 |
| − amortización de intangibles de combinaciones | −85,467 |
| **= C76** | **−81,200** |

El −81,2 es una identidad de las entradas. **Por sí solo no prueba un doble cómputo**: el mismo signo aparecería si Elis hubiera invertido por debajo de sus necesidades de reposición [I]. Lo que permite concluir es la naturaleza de cada bloque (§5 y §6), no el signo del total.

---

## 5. Arrendamientos

### 5.1 Bloques distintos que no se mezclan [P][D]

| Bloque | Qué es | Caja | No monetario | Dónde está en el libro |
|---|---|---|---|---|
| Lino y equipos propios en alquiler-mantenimiento | Inmovilizado material propio que Elis alquila a sus clientes; amortización de 18 meses a 5 años (URD25 p.367) | Compras de lino 584,3/594,3/594,2 y otros artículos 37,3/34,6/40,8 dentro de las compras de inmovilizado | Inversión devengada 621,6/628,8/635,0, que coincide con la de caja | Capex (fila 12) y D&A propia (fila 8) |
| Derechos de uso NIIF 16 (ROU) | Inmuebles, vehículos y equipos que Elis arrienda (nota 6.3) | Pagos 130,8/150,8/177,9 (financiación) | Altas 159,0/194,3/245,6 (nuevos, reestimaciones y combinaciones); amortización 115,8/132,2/149,5 | Fila 8 (amortización), fila 17 (principal), C48 (interés de caja), fila 23 (pasivo). Las altas no están en ninguna fila |

**El lino propio no es ROU** y no debe reclasificarse. Las altas ROU no son capex de caja y no deben sumarse al capex [P].

### 5.2 Dónde queda el coste de arrendamiento

| | Calibración (2023–25) | Proyección (base 2025) |
|---|---|---|
| Amortización ROU dentro del EBIT/NOPAT | −132,5 | −149,5 (dentro de m₀) |
| Devolución de la amortización ROU por la reinversión (− D&A total en C76) | +132,5 | 0 (ΔV/S2C no la devuelve)¹ |
| Pagos de arrendamiento dentro del FCF base y de f | −153,2 | −161,1 (f·V₀) |
| **Coste de arrendamiento reconocido** | **−153,2 (una vez: los pagos)** | **−310,6 (dos veces)**² |

¹ A crecimiento cero y en el terminal. En los años 1–10, si la palanca S2C se anclara en C53 (perímetro de D&A total), ΔV/S2C devolvería una parte que crece con el crecimiento (§5.3, alcance). En este expediente las palancas no usan C53.
² Ilustración: suma la amortización ROU de 2025, antes de impuestos, con los pagos medios escalados. El exceso exacto en la base 2025 es **139,4**: la amortización ROU media escalada, antes de impuestos, porque el impuesto real ya está dentro de f (revisión, O17).

### 5.3 Demostración (derivación) y su alcance

**Premisas:**
- (i) Las altas ROU no son salidas de caja: las financia el arrendador y aumentan el pasivo [P: URD25 p.366; estado de flujos sin capex ROU].
- (ii) El FCF base resta los pagos completos de arrendamiento (C48 + C49) [DH registrada].
- (iii) La proyección del motor es NOPAT − f·V − ΔV/S2C, sin ningún término que devuelva la amortización ROU [P: Convenciones V6.3; réplica exacta, §4.3].
- (iv) **Premisa económica** [I]: el activo arrendado se repone con nuevos contratos cuyo coste son los pagos, de modo que la amortización ROU no exige además un desembolso propio.
  - Es la práctica de la propia Elis en sus pruebas de deterioro, que definen el flujo como «adjusted EBITDA … − income tax at standard rate − capital expenditure (including lease renewal)» [P: URD25 p.368; DEU24 p.314; URD23 p.322; URD22 p.303].
  - Es decir, cuenta el arrendamiento una sola vez, como renovación dentro de la inversión y sobre un EBITDA sin coste de arrendamiento. Es el mismo esquema que la alternativa A1′ (revisión, O5).
  - **Evidencia contraria buscada.** La premisa fallaría si reponer el activo arrendado exigiera además caja propia, fuera de los pagos, o si parte del coste de arrendamiento estuviera fuera de los pagos y del ROU. Se revisó lo publicado:
    - el estado de flujos no tiene ninguna salida de inversión por derechos de uso, y las altas de ROU (159,0 / 194,3 / 245,6) entran en el pasivo, no en el capex [P: URD25 p.327 y p.366];
    - las mejoras en locales arrendados y cualquier compra de un activo al vencer el contrato son inmovilizado propio. Si existen, están en el capex propio y en la D&A propia, no en el ROU: no generan un tercer cómputo, y su importe no se publica por separado [I];
    - los arrendamientos de bajo valor (2,0), a corto plazo (5,9) y los pagos variables (0,9) de 2025 se registran como gasto [P: URD25 p.366]. Están dentro del margen y no en el ROU ni en los pagos del pasivo, así que tampoco se cuentan dos veces;
    - los pagos crecieron más deprisa que las ventas en la ventana (§5.5). Eso no contradice la premisa, pero limita la razón constante que usa f.

    No se ha encontrado evidencia publicada contra la premisa (iv). La conclusión sigue condicionada a ella.

**Conclusión** [D, condicionada a la premisa iv]. Con crecimiento cero (y en el valor terminal cuando g → 0), el flujo del motor es NOPAT − f·V: resta la amortización ROU dentro del margen y los pagos completos dentro de f. El coste económico de caja del arrendamiento para el accionista son los pagos; con pasivo constante, el principal se repone con nuevos contratos no monetarios. Por tanto el motor carga **de más, aproximadamente, la amortización ROU**:
- 2,906 % de las ventas en media 2023–25 y 3,117 % en 2025;
- 139,4 en la base 2025 si se corrige f con la media de la ventana;
- 43 % del FCF base.

La demostración sintética de `contraste_f1.py` lo confirma con números redondos: sin impuestos, sin crecimiento, EBITDA 100, capex propio = D&A propia = 20, ROU 10 y pagos 12. El FCF verdadero es 68 y la V6.3 da 58 [D].

**Alcance:**
- No depende del reparto entre reposición y crecimiento.
- **A crecimiento cero y en el terminal**, que reinvierte con g/ROIC y no con S2C, el exceso es íntegro y no depende de la palanca S2C.
- **En los años 1–10 depende del ancla de S2C** (revisión, O4) [D]. La plantilla es coherente consigo misma solo en su senda histórica: si la palanca se anclara en C53, que comparte el perímetro de D&A total con f, ΔV/S2C devolvería la reinversión neta histórica, que ya lleva restadas la amortización ROU y la PPA.
  - Con el ancla propia de cada perímetro y el crecimiento del escenario NORMAL (4,5 %), la brecha frente a A0 baja de 139,4 a 81,3 (A1) y de 229,3 a 129,6 (A2) en el año 1.
  - La brecha se anula con un aumento de ventas de 517,6 (A1) o 496,6 (A2), un 10–11 %, del orden del crecimiento compuesto de 2020–2025 (11,3 %).

  En este expediente las palancas (1 / 1,2 / 1,5) no usan C53 sino un perímetro propio (§3): el exceso se aplica entero en todos los años (`resultados/contraste_f1.md`, tabla «Palanca S2C anclada en el C53»).
- No depende del margen objetivo, salvo que se definiera como margen después de pagos de arrendamiento. No es el caso: la fase C ancla los márgenes en el EBIT NIIF 16 publicado [I, `fase_c.json` G5].
- La revisión independiente no encontró ninguna lectura razonable de la plantilla, de las palancas del expediente o del FCF base registrado bajo la que el coste se cuente una sola vez a crecimiento cero y en el terminal (REVISION_INDEPENDIENTE_1 §5).

Es un **defecto de definición** de la calibración de f en el motor A para empresas con NIIF 16 material, no un error de datos. **No cuantifica por sí solo el error de valor**: este depende también de §6 y de las palancas. **No autoriza una corrección**: corresponde a la decisión F1 [DH pendiente].

### 5.4 Interés de caja 29,6 frente a devengado 29,2

En 2023 y 2024 coinciden (19,8 y 25,8). En 2025 difieren en 0,4 [D]. Las notas publicadas no traen un puente: el movimiento del pasivo no muestra los intereses devengados por separado. Posibles causas no verificables [H]: interés devengado no pagado al cierre, efecto del tipo de cambio en las fechas de pago, modificaciones de contratos o el residuo de «otros movimientos» (0,3).

**Materialidad:** 0,133 en C48 (0,04 % del FCF base). **Tratamiento:** se conserva la cifra de caja, coherente con un FCF de caja y con la derivación registrada de C48, y se registra el residuo. No se intercambian los datos.

**En el contraste** el residuo se fija en +0,4 con la cota de redondeo de sus tres cifras (0,15), no con una tolerancia ampliada. Un error nuevo cuyo efecto neto supere 0,15 la hace fallar: por ejemplo, 148,0 en lugar de 148,3 o 29,5 en lugar de 29,2. Uno menor no lo detecta: con el gasto en 29,3 o en 29,1, R13 pasa. Es el límite de detección de cualquier identidad, y un caso de `test_contraste_residuos.py` lo documenta (revisión n.º 3, N6). Su explicación identificada es la diferencia de concepto entre pago y devengo, verificable en las etiquetas publicadas. Su causa concreta no se publica [H].

### 5.5 Pasivo por arrendamientos y deuda

En el motor A el pasivo por arrendamientos (703,2) no se resta: es coherente con un flujo al accionista que ya paga los arrendamientos dentro de f [D]. Entre 2022 y 2025 el pasivo creció de 485,4 a 703,2 por altas no monetarias superiores al principal [P]. Con f proporcional a las ventas, los pagos crecen con el negocio, lo que equivale a suponer que la cartera arrendada crece con él [I].

**Tendencia (revisión, O10)** [P][D]. En la ventana la cartera arrendada creció bastante más deprisa que las ventas:

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Pagos ÷ ventas | 3,04 % | 3,30 % | 3,71 % |
| Amortización ROU ÷ ventas | 2,69 % | 2,89 % | 3,12 % |
| Pasivo: variación anual | +10,9 % | +12,6 % | +16,0 % |
| Ventas: variación anual | +12,8 % | +6,1 % | +4,9 % |

- f aplica la media, 3,359 % de las ventas: 161,1 sobre las ventas de 2025, frente a 177,9 pagados (16,8 menos).
- En A1 y A2 el margen de partida lleva la amortización ROU de 2025 (149,5) y f devuelve la media escalada (139,4): quedan 10,1 sin devolver.

Es una limitación de proyectar una razón constante, no un defecto de las alternativas. Debe declararse al calificarlas de coherentes con los arrendamientos.

**Un matiz que refuerza ese límite** (revisión n.º 3, §6.3):
- según la revisión, el informe del primer semestre de 2026 (p.10) dice que el grupo «also benefits from a rent-free period on its new headquarters, running until December 2028». Es un documento fuera de las cinco fuentes verificadas por los scripts de este informe y posterior a la fecha base, así que se cita solo como lectura de la revisión;
- [P] las altas de derechos de uso de inmuebles fueron 57,1 en 2025, frente a 10,4 en 2024 y 26,9 en 2023 (URD 2025 p.366; DEU 2024 p.312);
- [I] si la sede forma parte del alta de 2025, sus pagos quedan por debajo de su coste hasta 2028. No contradice la premisa (iv), que trata de un desembolso adicional a los pagos y no de su calendario. Pero la razón de pagos sobre ventas de la ventana puede quedarse corta.

---

## 6. Intangibles adquiridos y reinversión necesaria frente a crecimiento

### 6.1 Búsqueda del desglose [P]

**Alcance de la búsqueda.**
- El autor buscó en los cinco informes 2021–2025 y en el comunicado de resultados de 2025. Términos en inglés y francés: «maintenance capex», «growth capex», «replacement», «renewal», «churn», «attrition», «retention rate», «investissements de maintenance/de croissance», «renouvellement», «taux de perte».
- La búsqueda **no encontró** la frase de mantenimiento del lino plano que sigue. La localizó la revisión independiente (O1), que buscó además en los documentos de 2016 a 2020 de la misma carpeta y no halló importes de reparto. El Registration Document 2017 (p.52) describe el capex de mantenimiento solo de forma cualitativa.
- Después de la revisión, el autor repitió la búsqueda en todos los textos extraídos de la carpeta de fuentes de Elis: URD 2016–2023 y 2025, DEU 2024, comunicado de 2025 y documentos del primer semestre de 2026. Se usaron, además, «two-thirds/two thirds», «deux tiers», «maintenance capital», «churn», «attrition rate» y «retention rate». Resultado:
  - las demás apariciones de «dos tercios» son de otros temas (remuneración, plantas, salas blancas);
  - la retención y la pérdida de clientes solo se describen de forma cualitativa: «attrition rates are monitored» (URD 2019–2025), mejoras de retención en el URD 2019 y, en la presentación del primer semestre de 2026, «new client wins outpacing churn» y «lower churn»;
  - ningún documento publica una tasa ni un importe de reposición.

  Los documentos de 2016–2020 y de 2026 no están entre las cinco fuentes verificadas de este informe: se citan solo como alcance de la búsqueda, no como cifra.

**No hay importes de reparto entre mantenimiento y crecimiento.** Lo publicado:

- **Proporción parcial de mantenimiento del lino plano** [P], repetida en el factor de riesgo de la hostelería: «investments in linen are automatically impacted, particularly flat linen, two-thirds of which ensures the maintenance of the stock in circulation, which is greatly reduced in the event of a downturn» (URD25 p.137; URD23 p.239; URD22 p.221; URD21 p.189). En francés: «le linge plat dont les deux tiers assurent la maintenance du stock en circulation» (DEU24 p.135).

  Límites que impiden usarla para cerrar M1:
  - Se refiere solo al lino plano, que fueron 2.217,4 de 4.796,8 de ventas en 2025, un 46,2 % (URD25 p.347) [P][D]. Las compras de lino no se publican separadas entre lino plano y ropa de trabajo.
  - «Mantenimiento del stock en circulación» no es la reinversión necesaria para sostener las ventas: no incluye la dotación de clientes nuevos que sustituyen a los perdidos [I].
  - Es un texto fijo, idéntico en todos los informes, sin importes.
  - No se puede extender mecánicamente a todo el lino. Dos tercios de las compras de lino de 2025 serían 396, por debajo de su amortización de 565,1 [D]. Es una ilustración del límite, no una estimación.

  Es evidencia que una estimación documentada (perímetro `A3_estimado` de la especificación) debería considerar.
- La inversión industrial «covers investments for both growth (new plants or to increase capacity) and maintenance (equipment replacement)» (URD25 p.312; DEU24 p.258).
- Gasto en lino: «Growth investments thus make up a large percentage of this expenditure because of the initial outlay required to set up a new customer» (URD25 p.312). No da porcentaje.
- «customer attrition rates are monitored at the Executive Committee», pero la tasa no se publica (URD25 p.141).
- Capex por tipo de activo (lino, otros artículos, resto; URD25 p.311; DEU24 p.257; URD23 p.266; URD22 p.247). Es un desglose por activo, no por finalidad.
- Inversión neta del 18,2–19,2 % de las ventas; lino, 12,4 % (2025) y 13,0 % (2024) de las ventas (URD25 p.311).

Fuentes que podrían contenerlo y **no están en la base**: presentaciones de mercado de capitales, respuestas de Relación con Inversores (el expediente ya redactó la pregunta en `Diagnóstico V6!B223`) y transcripciones de presentaciones de resultados. Registrar su existencia no equivale a disponer de sus bytes.

### 6.2 Lo que se puede derivar e inferir

- **[D]** Inversión neta propia (capex − D&A propia + circulante): −7,4 / 140,0 / 153,9 / 146,4 / 110,0 en 2021–2025. En lino: 19,8 / 94,8 / 102,2 / 56,7 / 29,1. En 2025 el lino casi iguala su amortización y el resto del inmovilizado la supera en 71,6.
- **[I] Cota superior de la reinversión necesaria: el capex propio.** Elis creció en todos los ejercicios: orgánico de 3,8 % en 2025 y 5,2 % en 2024. Además declara que una parte grande del lino y parte de la inversión industrial son crecimiento. Por tanto, su reinversión necesaria para sostener las ventas fue menor que el capex propio (867,2 de media). Premisa: el crecimiento orgánico tuvo un componente de volumen, no solo de precio.
  - **La premisa tiene apoyo publicado** para 2024 y 2025, sin cifra [P] (revisión, O2):
    - el crecimiento de 2025 fue «driven by a price effect from residual inflation in 2025, and a volume effect» (URD25 p.122);
    - el de 2024 fue «tirée par l'effet prix … et par l'effet volume» (DEU24 p.121);
    - los costes de proceso de 2025 subieron «in connection with the continued growth in volumes processed» y los de distribución por «volume growth and cost inflation» (URD25 p.309).
  - El crecimiento de esos años tampoco fue solo volumen: hubo dinámica de precios favorable ligada a la inflación salarial (DEU24 p.252–253; URD25 p.307). En 2023 el efecto precio fue ≈ +9 % sobre el 11,8 % orgánico (URD23 p.261).
  - **Lo que falta es la cuantificación** del reparto precio/volumen de 2024–25 a nivel de grupo, no su existencia.
  - **Límite** [I] (revisión, O6): si en 2025 hubiera habido infrainversión, la cota superior no valdría para ese año. Hay señales de contención del capex que la empresa presenta como eficiencia y normalización, no como infrainversión:
    - «effective management of capital expenditure, particularly in linen, has kept depreciation under control» y «capex contained despite new workwear contracts and expenditure under the Climate plan» (URD25 p.122);
    - «The Group's capital expenditure has returned to normal levels since 2024» (URD25 p.312) y «They remained stable after the sharp increase in previous years» (URD25 p.311);
    - la inversión neta en lino cae de 102,2 a 56,7 y a 29,1 en 2023–2025, con compras planas y amortización creciente [D].

    No demuestran infrainversión, pero son la evidencia pertinente y deben pesar en cualquier estimación.
- **[I] Referencia inferior: la D&A propia** (736,0 de media). No es una cota demostrada. Con inflación, reponer a coste actual cuesta más que la amortización a coste histórico, sobre todo en edificios y maquinaria de vida larga. El lino, con vidas de 18 meses a 5 años, se aproxima más a su amortización.
  - **Evidencia publicada en contra de tomarla como caso central** [P] (revisión, O6): los planes de negocio de las pruebas de deterioro suponen «the Group's climate plan, with a level of investment greater than the amortization and depreciation historically recorded» (URD25 p.369; DEU24 p.315 «supérieur aux amortissements historiquement constatés»), y esas hipótesis «include additional future investments» (URD25 p.333). La empresa planifica invertir por encima de la amortización histórica.
  - El plan climático es además un tercer tipo de inversión, ni reposición ni crecimiento de ventas, que la definición de §9 no contemplaba. Se añade como pendiente de definición.
- **[D] La V6.3 implica una reinversión necesaria igual a la D&A total** (954,0 de media; 1.003,5 en la base 2025): 86,8 más que el capex propio medio mientras la empresa crecía. Con las premisas anteriores, esa hipótesis implícita es **incompatible con la historia publicada** [I].

### 6.3 Reposición económica de los intangibles adquiridos [P][D][I]

- **Composición [P].** La PPA de 85,7 (2025) son relaciones con clientes, 83,5, y marcas, 2,2 (URD25 p.364). Las relaciones con clientes se amortizan en 4–14 años (URD25 p.364; DEU24 p.310).
- **Agotamiento [P/D].** Valor neto de las relaciones con clientes: 471,5 (1-ene-2023) → 414,9 → 351,6 (reexpresado) → **275,1** (31-dic-2025). Las altas por combinaciones fueron 20,6 / 32,3 / 3,7. Sin compras nuevas, el ritmo actual de amortización no puede durar más de unos 3,3 años (275,1 ÷ 83,5) [D]. Bruto acumulado 1.444,5, del que 1.169,4 ya está amortizado: es sobre todo la cartera de compras anteriores.

  Salvedades (revisión, O7):
  - **Las altas de 2025 (3,7) son provisionales** [P: «the amounts above are only provisional», URD25 p.340]. Hay precedente en la misma serie: las de 2024 eran 18,0 en el DEU 2024 (p.310) y son 32,3 reexpresadas en el URD 2025 (p.364).
  - La amortización no caerá de golpe, porque las vidas van de 4 a 14 años.
  - Las compras siguen reponiendo cartera a un ritmo de 20–32 al año.
- **Fiscalidad.** Publicado [P]: el diferido de la fila «Intangible assets» aporta un ingreso de 15,5 / 20,3 / 17,5 en 2023–2025 (URD23 p.346; DEU24 p.338; URD25 p.393).

  Inferido [I]: la amortización de lo adquirido es **mayoritariamente no deducible** en caja. Ese ingreso equivale al 18,3 %, 24,2 % y 21,0 % de la amortización de relaciones con clientes (84,6 / 83,9 / 83,5) [D], cerca de los tipos nominales. Hay dos límites: la fila incluye también marcas y otros intangibles, y el fondo de comercio con amortización fiscal tiene una fila aparte (revisión, O7).
- **Interpretación [I].** Las relaciones adquiridas se consumen a medida que se van clientes. Elis las repone (a) orgánicamente, con coste comercial ya incluido en el EBIT y lino para clientes nuevos ya incluido en el capex propio, o (b) con nuevas adquisiciones, que son caja fuera del FCF base e incluidas en C53 a través de la fila 13. La amortización contable de lo adquirido no mide ninguna de las dos. Que no sea salida de caja **no demuestra** que la cartera se mantenga gratis. Lo que indica es que su coste de reposición está en el EBIT y en el capex, o en las compras, y no en la PPA.
- **Evidencia parcial de la ventana (revisión, O8)** [P][I].
  - El crecimiento orgánico se mide sobre las ventas totales, netas de clientes perdidos, adquiridos o no. Fue positivo todos los años y con efecto volumen positivo publicado en 2024 y 2025. Eso indica que, en la ventana, la cartera se repuso orgánicamente, con un coste que ya está en el EBIT y en el capex propio.
  - Es evidencia parcial contra la hipótesis de reposición monetaria igual a la PPA. No la refuta para el futuro, que es una hipótesis de proyección.
  - Otros hechos publicados: «contracts are usually valid for an initial four-year term», con renovación automática y penalización por rescisión de casi todo el valor residual (URD25 p.141). En 2024, la calidad del servicio «a permis de baisser le taux de pertes» (DEU24 p.121). La tasa sigue sin publicarse.
- **Hipótesis implícita de la V6.3 [H].** Cargar la PPA de forma perpetua equivale a suponer una reposición monetaria igual a la PPA, unos 85,7 al año. Ningún dato publicado la sostiene; la evidencia de la ventana se inclina en contra, sin demostrarlo. **Doble cómputo no demostrado. Requiere decisión de política** (§10).
  - Compensación numérica que no debe confundirse con coherencia [D] (revisión, O8). El nivel de A0 coincide casi con «todo el capex propio es reposición y además la PPA se repone con caja»: 339,8 − 89,9 = 249,9, frente a 248,5. La razón es que el capex menos la D&A propia (131,2) casi iguala a la amortización ROU (132,5). Son dos efectos que se compensan, no ausencia de doble cómputo, y la contradice la evidencia anterior.

### 6.4 Qué falta, cuánto pesa y qué impide concluir

| # | Dato que falta | Materialidad (flujo, base 2025) | Conclusión que bloquea |
|---|---|---|---|
| M1 | Reparto de la inversión propia entre reposición y crecimiento, como importe, por bloque (lino, otros artículos, industrial/TI, plan climático) y año. Lo publicado no lo cierra (§6.1). Solo se publica una proporción parcial: dos tercios de la inversión en lino plano mantienen el stock en circulación. Siguen pendientes: (a) el importe invertido en lino plano, que no se publica separado de la ropa de trabajo, y por tanto también el importe de esos dos tercios; (b) la proporción de mantenimiento del resto del lino, de los otros artículos, de la inversión industrial y de TI, y del plan climático; (c) cuánto de la dotación a clientes nuevos repone clientes perdidos, que es reinversión necesaria aunque no sea «mantenimiento del stock» (enlaza con M2); (d) la fecha y la base de la estimación de los dos tercios, un texto fijo desde al menos el URD 2020 | Flujo de partida entre 339,8 (todo el capex es reposición) y 477,8 (reposición = D&A propia); intervalo de 138, el 45 % del FCF base. Ambos extremos llevan +27,9 de partidas puntuales de la ventana (§4.2) | Nivel del flujo de partida del motor A y, con él, cualquier nivel de valor del motor A; anclaje de S2C |
| M2 | Tasa de bajas de clientes, en particular de los adquiridos, y desembolso inicial por cliente nuevo. Publicado: contratos de cuatro años y bajada cualitativa de la tasa de pérdidas en 2024 | Política PPA: 85,7 al año (28 % del FCF base); diferencia entre A1 y A2 en el flujo de partida: 89,9 | Si la PPA es un coste de reposición |
| M3 | Política de proyección: crecimiento orgánico frente a crecimiento con adquisiciones | Cambia el ancla de S2C: en A2, 1,61 con adquisiciones frente a 2,07–3,13 orgánico; en A1, 2,45 frente a 5,52–13,85 | Coherencia entre crecimiento proyectado, inversión y PPA |
| M4 | Puente caja/devengo del interés de arrendamientos de 2025 | 0,4 (0,04 % del FCF base) | Ninguna |
| M5 | **Cuantificación** del efecto precio y del efecto volumen del crecimiento orgánico de 2024–25. Su existencia está publicada (§6.2) | Anclas S2C orgánicas | Calibración de las palancas S2C, no de f |
| M6 | Finalidad de las compras de sociedades: qué parte repone cartera perdida y qué parte amplía ventas. Añadido en la respuesta a la revisión de la propuesta (P2) | Cada millón anual de compras que fuera de reposición bajaría el flujo sostenible en un millón, también en el terminal | Sustituir por un dato la hipótesis de que las compras son crecimiento (propuesta, 4b) |

M1 y M2 son materiales y no se pueden resolver con la base. **Se conserva `pendiente_de_datos` para la conclusión de nivel**, como ya hace el expediente.

---

## 7. Impuestos

| | 2023 | 2024 | 2025 | Fuente |
|---|---|---|---|---|
| τ de la fila 10 (gasto ÷ BAI, 4 decimales) | 29,63 % | 27,54 % | 25,60 % | [D] de DEU24 p.270; URD25 p.324 |
| Impuesto nocional τ·EBIT (dentro del NOPAT) | 147,2 | 164,2 | 161,3 | [D] |
| Gasto por impuesto | 110,3 | 128,3 | 126,2 | [P] |
| · diferencia = escudo del gasto financiero τ·financiero | 36,9 | 35,9 | 35,1 | [D] |
| Corriente / diferido | 120,3 / −10,1 | 127,7 / 0,6 | 147,2 / −21,0 | [P] DEU24 p.337; URD25 p.392 |
| · diferido por intangibles (ingreso no monetario) | 15,5 | 20,3 | 17,5 | [P] URD23 p.346 (la única publicación que presenta el movimiento de 2023); DEU24 p.338; URD25 p.393 |
| · diferido de ROU + pasivos por arrendamiento | −0,4 | 2,3 | 1,7 | [P] ídem |
| Impuestos pagados | 126,4 | 124,9 | 146,7 | [P] |
| Pagado − nocional (componente fiscal de f) | −20,8 | −39,3 | −14,6 | [D] |
| Partidas especiales | earnout no deducible: +15,8 de impuesto | — | contribución excepcional francesa: 4,9 | [P] DEU24 p.337; URD25 p.392 |
| CVAE/IRAP incluidos en el gasto | 4,6 | 3,5 | 3,7 | [P] |

- No se toma el gasto (126,2) por el impuesto de caja (146,7). f recoge, como fuga, la diferencia entre el impuesto pagado y el nocional [D].
- **Tratamiento fiscal de los ajustes ROU y PPA.** Las alternativas de §9 cambian un concepto de caja antes de impuestos: el perímetro de la reinversión. La identidad de calibración se mantiene exacta y no necesita un ajuste fiscal adicional [D]. Los efectos fiscales reales ya están en los impuestos pagados que calibran f: la PPA es mayoritariamente no deducible en caja [I, §6.3] y NIIF 16 tiene un efecto casi neutro [P].
  - **Limitación [I]:** en la proyección esos efectos se escalan con las ventas, aunque la PPA se agote. El escudo nocional τ·PPA dentro del NOPAT es 25,4 / 23,4 / 21,9 y queda compensado en la historia por el diferido de intangibles.
  - La limitación de proyección no es solo fiscal: en A2, f devuelve la PPA entera de forma perpetua (1,87 % de las ventas). Eso solo es coherente si el margen objetivo incluye una PPA de ese orden. Por eso la especificación añade un perímetro declarado del margen (E2 y V-F1h; revisión, O12).
- **Observación fuera de F1 [D]:** f se calibra con el τ de cada año (media efectiva ponderada ≈ 27,4 %) y la proyección aplica el τ de 5 años (28,82 %, que incluye el 33,1 % de 2021). Efecto en la base: −8,0 al año. Es una convención (Convenciones §4 y C52), no un error. Si se revisa, debe decidirse expresamente.

---

## 8. Financiación y flujo al accionista

| | 2023 | 2024 | 2025 |
|---|---|---|---|
| Free cash flow publicado | 303,6 | 346,3 | 358,6 |
| FCF base del año (después de SBC) | 280,6 | 319,3 | 323,9 |
| Adquisiciones | 82,1 | 183,3 | 117,6 |
| Dividendos | 61,7 | 101,3 | 105,1 |
| Recompras − ampliaciones | −9,1 | −8,2 | 139,0 |
| Emisión neta de deuda (EFE) | +208,9 | −95,8 | −210,6 |
| Deuda financiera neta al cierre | 3.025,4 | 3.038,0 | 3.020,2 |
| Pasivo por arrendamientos al cierre | 538,3 | 606,2 | 703,2 |
| OCEANE (componente de deuda) | 343,1 | 352,3 | 362,0 |

Fuentes [P]: DEU24 p.259, 273 y 329; URD25 p.314, 327 y 384. El puente publicado de la deuda neta cierra en 2025 (FCF 358,6 − adquisiciones 117,6 − deuda adquirida 9,1 − otros flujos 12,7 − dividendos 105,1 − capital y acciones propias 139,0 + otros 42,7 = 17,8 de reducción) y en 2024 con un residuo de 0,1 [D].

- **Deuda constante [D/I].** El FCF base resta intereses pero no amortizaciones ni nuevas emisiones de deuda financiera: equivale a un flujo al accionista con la deuda refinanciada. La deuda neta fue estable en 2023–25 (3.025 → 3.038 → 3.020), lo que es coherente con esa lectura histórica. Tiene cuatro límites (revisión, O11):
  1. **Los arrendamientos no están en base de deuda constante.** El FCF base resta su principal (128,1) y no acredita las altas no monetarias (159,0 / 194,3 / 245,6). La financiación se trata de forma asimétrica: deuda financiera renovada y arrendamientos amortizados. Es legítimo, pero es el origen de F1 y la razón de que A1′ sea la variante simétrica.
  2. **Deuda constante no es interés constante.** Con la deuda neta plana, los intereses netos pagados subieron un 41 %, de 70,5 a 99,4, por la refinanciación a tipos más altos y el reembolso anticipado del bono de 2026 [P: «refinancing transactions in 2024 and 2025 at higher interest rates», URD25 p.312]. f usa la media, 82,9, que escalada a 2025 da 87,2, por debajo del último dato.
  3. **Lo estable es la deuda neta.** La bruta bajó de 3.690,7 a 3.418,3 y la caja de 665,3 a 398,1 [P].
  4. **El devengo no monetario de la OCEANE** (9,7 en 2025 [P: URD25 p.314]) aumenta el pasivo sin caja. No está en C48 por la decisión E6, que no se discute, pero significa que ese pasivo no es constante.
- **Observación fuera de F1 [D][I].** En la proyección, f escala los intereses con las ventas (1,82 % de las ventas) sin el endeudamiento nuevo que haría falta para que la deuda creciera con el negocio. En el año 1:
  - los intereses adicionales son 1,7 / 3,9 / 4,8 (MALO / NORMAL / BUENO);
  - si la deuda neta se mantuviera en el 63 % de las ventas, el endeudamiento neto omitido sería 60,4 / 135,9 / 166,1.

  La plantilla lo declara («supone que escala con el negocio»). Es una convención con sesgo prudente cuya revisión es económica y no forma parte de F1.
- Acciones, SBC y OCEANE se mantienen según E6 [DH]: acciones en circulación a 31-dic-2025, OCEANE como deuda y sin acciones de conversión. El SBC se resta como coste (C50), y la dilución potencial de la OCEANE y de las acciones de rendimiento se identifica aparte, sin contarla dos veces.

---

## 9. Definiciones económicas y alternativas coherentes (ninguna adoptada)

**Definiciones propuestas:**
- **Reinversión necesaria (R):** inversión propia anual para sostener las ventas a volumen constante. Incluye la reposición de clientes perdidos.
- **Inversión de crecimiento:** capex propio − R + circulante.
- **D&A propia:** D&A total − ROU − PPA.
- **Perímetro de la reinversión:** el conjunto de D&A que se supone repuesto con capex propio. Debe ser el mismo en la calibración de f, en el ancla de S2C y en la proyección.
- **Perímetro del margen:** qué costes no monetarios incluye el margen proyectado: EBIT NIIF 16 con PPA constante, con PPA decreciente o sin PPA. Debe casar con el perímetro de la reinversión (revisión, O12).
- **Inversión del plan climático:** ni reposición ni crecimiento de ventas. Queda **pendiente de definición**; no se asigna a ninguno de los dos (revisión, O6).
- **Precisión de la respuesta a la revisión de la propuesta (P1, P2).** La propuesta de decisiones (revisión 2) concreta estas definiciones sin adoptarlas:
  - R = R_propia + R_compras + la transición de sostenimiento. R_propia incluye la dotación a los clientes que sustituyen a los perdidos; R_compras son las compras de cartera necesarias para mantener las ventas;
  - el gasto comercial queda en el margen y no en R;
  - la inversión climática se clasifica por su finalidad documentada, con su caja cobrada una sola vez;
  - tabla de correspondencia de costes en la propuesta, §2.

| | A0 · V6.3 actual | A1 · sin ROU | A1′ · arrendamientos como deuda renovada | A2 · perímetro propio | B · cota |
|---|---|---|---|---|---|
| Reinversión necesaria supuesta | D&A total | D&A total − ROU | D&A total; FCF base sin principal | D&A propia | Capex propio |
| R media 2023–25 | 954,0 | 821,5 | 954,0 | 736,0 | 867,2 |
| R − capex medio | **+86,8** | −45,7 | +86,8 | −131,2 | 0 |
| f | 4,168 % | 1,262 % | 1,359 % | −0,612 % | 2,265 % |
| Flujo sin crecimiento (base 2025) | 248,5 | 387,9 | 383,2 | 477,8 | 339,8 |
| S2C total 2021–25 (con adquisiciones) | 9,04 | 2,45 | — | 1,61 | 2,65 |
| S2C orgánico 2023–25 / 2021–25 | no definido | 5,52 / 13,85 | — | 2,07 / 3,13 | no significativo |
| Coherencia con los arrendamientos³ | **No** (§5.3) | Sí | Sí, en estado estacionario (principal ≈ amortización ROU) | Sí | Sí |
| Tratamiento de la PPA | Reposición monetaria implícita | Reposición monetaria implícita | Reposición monetaria implícita | No monetaria, sin reposición; exige un margen con PPA de ese orden | Incluida en el capex observado |
| Evidencia | Hipótesis implícita contraria a la historia (R > capex) [I] | Lease: [D]; PPA: [H] | Lease: [D], y es el esquema que usa Elis en sus pruebas de deterioro: «capital expenditure (including lease renewal)» (URD25 p.368) [P]; cambia una entrada registrada | Lease: [D]; PPA: [I]/[H], con evidencia parcial a favor en la ventana (§6.3); R = D&A propia: [H], con evidencia publicada en contra como caso central (§6.2) | Cota: [I] |
| Límites | Doble coste de arrendamiento | Mantiene la hipótesis PPA | Sustituye el principal de caja (128,1) por la amortización ROU (132,5); **modifica C49, registrado: requiere decisión** | Si la reposición a coste actual supera la D&A propia, sobrestima el flujo | No es una alternativa: supone crecimiento sin inversión |

³ Con una salvedad común a todas las columnas: los pagos y la amortización ROU crecieron más deprisa que las ventas en la ventana, y una razón constante no lo proyecta (§5.5). Todos los flujos llevan +27,9 de partidas puntuales (§4.2).

Fuente: `resultados/contraste_f1.md`, tabla «Alternativas».

Lectura [I], sin adoptar nada:
- A0 es incoherente con la mecánica de NIIF 16 y su reinversión implícita supera lo invertido.
- A1 y A2 corrigen el arrendamiento y difieren solo en la política de la PPA.
- A1′ es coherente, pero toca la construcción registrada del FCF base.
- El intervalo B–A2 refleja la falta del dato M1.
- **Motor B como vía alternativa:** con f = 0 y el pasivo por arrendamientos restado, trata los arrendamientos de forma coherente, porque en estado estacionario las altas ROU equivalen a la amortización ROU. Mantiene la misma cuestión de la PPA y una incoherencia propia de perímetro en el coste de la deuda: C63 divide intereses sin arrendamientos entre deuda con arrendamientos. La elección de motor (C62 = Sí) es de la fase A y no se cambia aquí.

**Ninguna alternativa se elige por su efecto en el resultado.** La elección depende de la decisión F1 y de los datos M1–M3.

---

## 10. Hipótesis, incertidumbres y decisiones

**Decisiones humanas registradas que se conservan** [DH]: E1 (valores exactos en Viscofan/Vidrala), D3 (acciones de Viscofan), E2 (K14 de Vidrala) y E6 (Elis: base coherente a 31-dic-2025, acciones en circulación, OCEANE como deuda sin acciones de conversión, C48 conciliado, dilución aparte). No se vuelven a pedir y este informe no altera ninguna. La construcción del FCF base (media 2023–25, capex neto, C48 = 82,9 + 25,1) procede de la decisión del inversor del 10-nov-2026 registrada en C47/C48.

**Supuestos de la orquestación que siguen vigentes** [S]: F1 opción (a), es decir, motor A «no validado para casos con NIIF 16» y precio de Sí no utilizable. Medias de C46/C47/C50 registradas con tres decimales.

**Decisiones pendientes** (de la persona responsable; no se adoptan por obtener números):
1. **F1:** (a) declarar el límite y no usar el motor A en esos casos; (b) corregir la definición; (c) juicio caso a caso. Debe redactarse la política completa, no solo la letra. `CONTINUIDAD.md` §9.19 abrevia (c) como «excluir»; este informe no lo resuelve.
2. Si (b): **política de arrendamientos**. Para que el motor A sea coherente, el perímetro debe excluir la amortización ROU (A1/A2) o el FCF base debe excluir el principal (A1′, que modifica C49).
3. Si (b): **política de intangibles adquiridos** (A1 frente a A2, o modelización explícita de adquisiciones). Requiere M2 y M3.
4. Si (b): **reinversión necesaria**: dato (M1) o estimación documentada con rango, evidencia operativa y responsable. Si no existe, se mantiene `pendiente_de_datos`.
5. **Perímetro de S2C y del margen** coherentes con el anterior. El ancla C53, las palancas S2C y el margen objetivo deben declarar el mismo perímetro.
6. **Tratamiento de la inversión del plan climático** (§6.2): ni reposición ni crecimiento. Hace falta una definición antes de usarla en una estimación.
7. **Normalización de partidas puntuales** de la ventana (+27,9; §4.2): solo con una regla decidida.
8. Observaciones de la plantilla fuera de F1 (§7 y §8): ventana del tipo impositivo y escala de intereses sin endeudamiento nuevo. Requieren revisión económica propia.

**Incertidumbres que no se pueden acotar con la base:** M1 y M2 (§6.4). La conclusión afectada, el nivel del flujo y del valor del motor A para Elis, **queda pendiente**.

---

## 11. Especificación propuesta y criterios de prueba

Ver [ESPECIFICACION_F1_PROPUESTA.md](ESPECIFICACION_F1_PROPUESTA.md). Es una propuesta para que el frente técnico la implemente sobre una versión técnica fijada, después de la decisión F1. Incluye entradas nuevas de la Historia, parámetro declarado de perímetro, calibración de f y de S2C con ese perímetro, reglas de control, presentación del puente y criterios de prueba con valores de referencia de este informe.

## 12. Revisión independiente

Estado y documentos en [revision/](revision/).

- **Revisión n.º 1**, sobre 96a69ca: 17 objeciones, 3 materiales; ninguna invierte una conclusión material.
- **Contraste externo** sobre 6fb9294 (`revision_chatgpt_1/`) y sus sondas de un solo campo sobre eb77dea (`revision_chatgpt_1/seguimiento_eb77dea/`).
- **Revisión n.º 3**, sobre el commit congelado 1864c4e, con adenda sobre f30c66c. Sesión distinta de la del autor y con la configuración que el encargo asigna, comprobada en sus metadatos ([REGISTRO_CONFIGURACION.md](REGISTRO_CONFIGURACION.md)).
  - Resuelve O1, O2 y O4–O17. Deja O3 parcialmente resuelta.
  - Plantea N1 (material), N2–N5 y N9–N10 (menores) y N6–N8 (forma). No cambia ninguna conclusión material.
  - Informe, scripts y salidas: copia sin cambios en `revision/`, con procedencia en [revision/PROCEDENCIA_REVISOR.md](revision/PROCEDENCIA_REVISOR.md).
- **Revisión n.º 2:** no existe. Se encargó sobre eb77dea y se interrumpió a los pocos minutos, sin resultado.
- **Respuestas** a O1–O17, al contraste externo y a N1–N10, cada una con su commit y su prueba: [revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md).
- **Revisión de lo afectado por las correcciones de N1–N10** (pasada 4, sobre el congelado 9744177): **hecha** (a15f706, 22:04 UTC). Reproduce todas las cifras, da por corregidas N2–N10 y N1 en parte y plantea P1–P5. Copia y procedencia en `revision/`. Respuesta en C10 ([revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), cuarta parte). Hasta que conste, esas correcciones no están revisadas de forma independiente.
- **Revisión n.º 5** (lo afectado por C9 y C10, sobre el congelado 364129a): **hecha** por una sesión de revisión nueva (595d2f6, 23:19 UTC). Reproduce todas las cifras, confirma las siete filas de C9 y plantea Q1–Q7. Copia y procedencia en `revision/`. Respuesta en C12 ([revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), quinta parte).
- **Revisión n.º 6** (lo afectado por C12, sobre el congelado 1b80b5d): **hecha** por otra sesión de revisión nueva (9711f04, 01:24 UTC). Reproduce todas las cifras, confirma las filas nuevas de C12 y plantea R1–R8: efectos de las correcciones de C12 en el verificador, sin efecto en las filas reales. Copia y procedencia en `revision/`. Respuesta en C14 ([revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), sexta parte).
- **Revisión n.º 7** (lo afectado por C14, sobre el congelado c96d544): **hecha** por otra sesión de revisión nueva (d192cab, 04:18 UTC). Reproduce todas las cifras, confirma las dos filas nuevas y los intervalos de detección, da por sostenidas las tres decisiones de C14 que no seguían la propuesta de la revisión n.º 6 y plantea S1–S7: restos de las clases de R3, R4 y R5 y casos de líneas sin rótulo, sin efecto en las filas reales. Copia y procedencia en `revision/`. Respuesta en C16 ([revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), séptima parte).
- **Revisión n.º 8** (lo afectado por C16, sobre el congelado 863ddde): **hecha** por otra sesión de revisión nueva (3138a6b, 06:40 UTC). Reproduce todas las cifras; de las 346 aceptaciones nuevas, 341 son saldos legítimos y 5 no son cifras; plantea T1–T8 sobre la regla de S1 y otros restos, sin efecto en las filas reales. Copia y procedencia en `revision/`. Respuesta en C18 ([revision/RESPUESTAS_AUTOR_1.md](revision/RESPUESTAS_AUTOR_1.md), octava parte). Hasta que la revise la pasada 9, lo afectado por C18 no está revisado de forma independiente.
- **Revisión n.º 9** (lo afectado por C18, sobre el congelado 06ad100): **hecha** por otra sesión de revisión nueva (a3a1a2b, 10:36 UTC). Reproduce todas las cifras; en su barrido ninguna candidata pasa a OK; da T1–T6 por corregidas y plantea U1–U2 (menores) y U3–U6 (forma): la posición de los tokens, los recuentos con fecha, la cuenta de columnas y restos de forma, sin efecto en las filas reales. Copia y procedencia en `revision/`. Respuesta en preparación (C20).

## 13. Reproducción

Desde esta carpeta, con un árbol `munger_v2_r1` materializado (base 4.14 o hito 4.15; mismos binarios), Python 3.10+, pdftotext/pdfinfo (poppler) y openpyxl:

```bash
cd scripts
LIBRO=<ruta>/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx
python3 -I verificar_cifras.py --raiz <ruta>/munger_v2_r1 --datos ../datos/cifras_fuente.csv --fuentes ../datos/fuentes.json --salida ../resultados/verificacion_cifras.json --exportar-paginas ../evidencias/paginas
python3 -I test_verificar_cifras.py --raiz <ruta>/munger_v2_r1
python3 -I prueba_caja_no_nula.py --libro "$LIBRO" --salida ../resultados/caja_no_nula.json
python3 -I contraste_f1.py --cifras ../datos/cifras_fuente.csv --verificacion ../resultados/verificacion_cifras.json --libro "$LIBRO" --caja-no-nula ../resultados/caja_no_nula.json --salida ../resultados/contraste_f1.json --informe ../resultados/contraste_f1.md
python3 -I test_contraste_residuos.py --libro "$LIBRO"
python3 -I cobertura_por_mutacion.py --libro "$LIBRO" > ../resultados/cobertura_por_mutacion.txt
python3 -I tabla_conciliacion.py --cifras ../datos/cifras_fuente.csv --salida ../resultados/tabla_conciliacion.md
```

- `verificar_cifras.py` termina con código 2 porque hay 14 filas PENDIENTE; su informe las lista con el motivo.
- `contraste_f1.py` termina con 0 si ninguna comprobación falla y ninguna entrada que usa está pendiente; con 2 si usa alguna pendiente; con 1 si falla algo.
- `prueba_caja_no_nula.py` necesita LibreOffice (python3-uno). Trabaja sobre una copia temporal y comprueba que el libro original no cambia. No debe correr a la vez que otro pipeline de LibreOffice.
- `especificacion_cifras.py` regenera el CSV desde los PDF. Se detiene si una lectura del autor no coincide con el literal impreso o si alguna dimensión falla, y lista las que quedan pendientes.

**Lo que este informe no hace:** no valora la empresa, no emite precio objetivo ni recomendación, no cambia la plantilla, no regenera expedientes, no declara aptitud para dinero real y no sustituye la integración, réplica y auditoría del material final, que se comprobarán después.
