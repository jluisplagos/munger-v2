# Registro de ejecución y cambios · entrega 4.7.1 (10-nov-2026)

## Encargo
La revisión independiente de la entrega 4.7 (ChatGPT, 10-nov-2026) pidió dos subsanaciones dentro de un mismo encargo:
- **W-1 (§1):** completar la sincronización del resumen cuando `resumen.py` encuentra una ficha cerrada que ya no es vigente y recibe otro destino, y revisar la ruta análoga de sustitución de ficha. Una prueba debe comprobar de inmediato las dos filas, los archivos y los historiales, sin una segunda llamada reparadora, y conservar las filas ajenas y la estabilidad de los reintentos.
- **N3 (§2):** separar la inversión fija del circulante; corregir la inversión bruta inferida; identificar la hipótesis de mantenimiento, su evidencia y sus límites; revisar la recuperación de capacidad y, si corresponde, añadir una sensibilidad respaldada por fuentes; actualizar el informe, los cálculos de caja, la matriz y la propuesta D-N3. La comparación sigue siendo exploratoria donde falta evidencia.

Quedan fuera, como pidió la revisión: N1 y N2 (se conservan sus avances), H1–H3, N4, N9, N10, P-N1 y P-N2. La revisión de estas correcciones debe preceder a la adopción humana de las convenciones afectadas.

Todo lo que sigue está ejecutado o declarado por Claude. Nada está comprobado externamente por ChatGPT.

## Modelos
Se usó Opus en todo, también en el agente de auditoría con contexto separado. El control de vigencia lo hizo el mismo agente que la auditoría, y así lo declara. Fable no se usó.

## Punto de partida
- ZIP de la 4.7, SHA-256 `b560977aa0f435d3545d81a0f510fdd224c7b2a97caab4c2c72d4fe069764c5b`, descomprimido en limpio: manifiesto de 1.412 archivos sin diferencias; P1 `b4e47afc…c445a4`.
- El manifiesto de la 4.7 se conserva en `reproduccion/MANIFIESTO_SHA256_4_7.txt`. `comprobar_entrega_4_7_1.py` lo usa para comprobar que solo cambian los archivos declarados.

## W-1
1. **Reproducción con el código 4.7**, con la secuencia de la revisión: REPRODUCIDO (`reproduccion/reproduccion_w1_codigo_4_7.txt`).
2. **Reparación** (detalle en `CIERRE_TECNICO_4_7_1.md`):
   - `resumen.py`: en la rama de ficha cerrada no vigente, tras archivar, sincroniza todos los destinos conocidos en la misma llamada; código 5 si queda una retirada pendiente y 3 si no;
   - `ficha.py`: la sustitución de una ficha cerrada sincroniza en la misma llamada, tras escribir la ficha nueva;
   - `cierre_v2.py`: la aprobación sin registrar del resumen predeterminado se identifica por el contenido publicado (`_fila_de`) frente a las fichas cerradas archivadas, y se conserva si es la de la ficha oficial vigente.
3. **Corrección tras la auditoría interna** (detalle en el cierre técnico, §5):
   - **W-a, bloqueante:** la primera versión detectaba la fila sin registrar por su contenido exacto, y una fila reescrita por una hoja de cálculo o una ficha editada tras el cierre quedaban sin retirar en ninguna llamada, una regresión frente a la 4.7. Ahora la detección vuelve a ser por empresa y fecha (también en formatos de hoja de cálculo), y el contenido, con los números normalizados, solo excluye la fila de la ficha vigente;
   - **W-b:** el predeterminado se retira también con el registro ilegible;
   - **W-e, anterior a la 4.7.1:** dentro del pipeline, la sustitución de la ficha terminaba en «concluido · APROBADO», con código 0 y sin salidas. Ahora el pipeline adopta el archivo que hacen los generadores y termina con código 4;
   - **W-f:** una fila que reaparece en un destino ya retirado se vuelve a retirar;
   - **W-g:** la fila retirada nombra el material de la ficha archivada;
   - **W-d:** `ficha.py` directo avisa en la salida de que la ficha nueva no es vigente, y el Anexo D documenta su código 0;
   - **W-c:** las pruebas 23 y 24 comprueban ahora todo lo pedido de inmediato, y hay ocho pruebas nuevas (26–32).
4. **Con el código revisado:** NO SE REPRODUCE (`reproduccion/reproduccion_w1_codigo_4_7_1.txt`).
5. **Pruebas,** ejecutadas en copias por `scripts/ejecutar_baterias_4_7_1.py`, con las huellas del código en la cabecera de cada salida:
   - `test_resumen_v2.py`: 45/45;
   - con el código 4.7: 35/45, porque fallan las 3 de W-1 y 7 de las 8 nuevas;
   - con el código que vio la auditoría: 36/45, con 9 fallos;
   - `test_cierre_v2.py`: 55/55;
   - `test_pipeline_sintetico.py`: 30/30, porque `pipeline.py` cambia;
   - `verificar_paquete.sh` exige al menos 45.

   Las salidas del primer cierre (37/37 y 34/37) están en `reproduccion/primer_cierre/`.
6. **Documentación:** Anexo D (criterio corregido, códigos de `ficha.py` y del pipeline, límite residual) y `DECISIONES.md` (entrada del 10-nov-2026).

## N3
1. **Corrección de la identidad** (hecho señalado por la revisión): inversión bruta = amortización + inversión fija neta = amortización + reinversión total − variación del circulante. R1, año 1: 132,948 (no 130,79366); R0: 118,82278.
2. **Sin cambios de valor:** la matriz de 27 combinaciones, los ponderados, los precios de Sí y la combinación propuesta son los de la 4.7; el script lo comprueba (`control_4_7`).
3. **Evidencia nueva:** 14 datos (amortización 2020, 2024 y 2025; inversión material e inmaterial de esos años; vida útil de hornos; PERTE; reparación y mantenimiento), 123 en total, todos reproducidos con su signo.
4. **Hipótesis de mantenimiento explícita:** reposición = amortización, en los tres escenarios. La inversión supera a la amortización todos los años desde 2017 (1,10–1,74), también con ventas en caída, y se destina sobre todo a renovar hornos. Los textos conservados no separan reposición, eficiencia, descarbonización y crecimiento.
5. **Capacidad:** la variante «sin capacidad» reproduce la formulación inicial del R1 de la 4.7 (`control_formulacion_inicial`) y cambia poco (−0,06 de ponderado y −0,13 de precio de Sí en T1·M1).
6. **Sensibilidades exploratorias:** mantenimiento adicional de 20,9 % y 41,8 % de la amortización, solo en el MALO y en todos los escenarios (`financiero/sensibilidades_n3.csv`). No son alternativas de la matriz ni cotas.
7. **Decisiones:** D-N3 reescrita y D-N3b nueva en `financiero/decisiones_propuestas_N1_N3.json`; D-N1 y D-N2 iguales a la 4.7; las cuatro sin `decision`, `fecha` ni `confirmado_por`.
8. **Informe:** `INFORME_N3_SUBSANACION.md`. Sustituye la viñeta «Necesidades de caja» del §4.2 del informe de la 4.7 y su mención del §6 a la cobertura de los compromisos. El informe de la 4.7 se conserva intacto.
9. **Correcciones tras la auditoría interna, sin cambios de cálculo:**
   - **N-a:** dos frases que se presentaban como hechos pasan a interpretación o se retiran («renovación, no ampliación»; «los hornos se reconstruyen por campañas»);
   - **N-b:** los límites se dan ahora en los dos sentidos (la amortización de la cartera de clientes y de los derechos de uso, y los cambios de perímetro), y se dice de forma explícita que «=D&A» es la opción de mayor valor de D-N3b;
   - **N-c:** se precisa qué sustituye el informe.
10. **Corrección propia antes de la auditoría:** cinco diferencias del informe se habían calculado con valores redondeados (por ejemplo −1,92 en vez de −1,93). Se recalcularon con los valores sin redondear.

## Auditoría interna de Claude
Dos revisiones con contexto separado, cada una sobre material fijado por huellas. Ninguna es una revisión externa.

| Revisión | Material (SHA-256 del archivo de huellas) | Veredicto | Hallazgos |
|---|---|---|---|
| auditoría interna | `MATERIAL_AUDITORIA_4_7_1.txt` · `72ad6679…` (32 archivos) | **Con hallazgos bloqueantes** (1) | W-a bloqueante; W-c y W-e importantes; W-b, W-d, W-f, W-g, N-a, N-b, N-c, C-a, C-b y C-c menores |
| control de vigencia (mismo auditor; lo declara) | `MATERIAL_VIGENCIA_4_7_1.txt` · `7863eb91…` (47 archivos) | **Sin hallazgos bloqueantes** | W-a a C-b resueltos, comprobados también con siete mutaciones (cada corrección revertida hace fallar al menos una prueba); C-c es este empaquetado; seis hallazgos nuevos menores, X-a a X-f |

- Los informes están en `AUDITORIA_INTERNA_4_7_1.md` y `AUDITORIA_INTERNA_4_7_1_vigencia.md`. Las correcciones están en el cierre técnico, §5, y en el informe del N3.
- **Incidencia de procedimiento.** Durante la auditoría, Claude borró del espacio temporal de la sesión unas carpetas antiguas que creía suyas. Una era la primera descompresión del ZIP 4.7 que había hecho el auditor, y este tuvo que volver a extraerla. No afectó al material auditado, que el auditor comprobó por huellas al principio y al final. Desde entonces Claude no tocó las carpetas del auditor.
- **Tras el control de vigencia no se cambió nada del material** fijado en `MATERIAL_VIGENCIA_4_7_1.txt`. `comprobar_entrega_4_7_1.py` lo comprueba. Por eso X-a a X-f quedan declarados y sin corregir (abajo).

## Mejora frente a la 4.7

| Aspecto | 4.7 | 4.7.1 |
|---|---|---|
| Aprobación del predeterminado publicada antes del registro, con `resumen.py` hacia otro destino | sobrevivía (W-1) | se retira en la misma llamada |
| Sustitución de una ficha cerrada en `ficha.py` | retiraba solo en una llamada posterior | retira en la misma llamada (código 5 si queda pendiente) |
| Identificación de esa aprobación | por la fecha, solo sin ficha vigente | por la fecha, con o sin ficha vigente; el contenido normalizado solo excluye la fila de la ficha vigente |
| Sustitución de la ficha dentro del pipeline | «concluido», código 0, sin salidas y con el estado sobrescrito | código 4, estado sin aprobación y archivo registrado |
| Fila sin registrar reescrita por una hoja de cálculo | se retiraba por la fecha si coincidía exactamente | se retira con la fecha en los formatos habituales; la de la ficha vigente se conserva |
| Batería del resumen | 34 | 45 |
| Inversión bruta implícita del N3 | D&A + reinversión total (130,79 en R1) | D&A + inversión fija neta (132,948 en R1) |
| Hipótesis de mantenimiento | implícita | explícita, con evidencia, límites y sensibilidad |
| Recuperación de capacidad | supuesta | sensibilidad con la formulación inicial |
| Propuesta D-N3 | R1 | R1 condicionada a D-N3b, con la sensibilidad visible |
| Evidencia | 109 datos | 123 datos |

## Pendientes, por prioridad
1. **Revisión externa** de estas correcciones, antes de pedir la adopción humana de las convenciones afectadas.
2. **Decisiones de la persona responsable:** D-N1, D-N2, D-N3 y D-N3b (archivo de la 4.7.1).
3. **P-M1 · hipótesis de mantenimiento de la plantilla** (reposición = amortización en todos los escenarios): necesita la separación entre reposición y crecimiento de la inversión y las reconstrucciones de hornos programadas, que no están en los textos conservados.
4. **Calendario de campañas de hornos** frente a la vida útil declarada, para la sensibilidad de capacidad.
5. **`ficha.py` al sustituir una ficha cerrada:** decidir si debe negarse a escribir la nueva. Hoy la escribe sin aprobación registrada, como en la 4.6.1, con código 0 y un aviso (W-d).
6. **De la 4.7, sin cambios:** cómo llevar las propuestas a la plantilla si se aplican; los datos que faltan del N1–N2; W-2 (precisión del Anexo D); los límites declarados del bloque A.
7. **Pendientes que siguen como estaban:** N4, N9, N10, P-N1 y P-N2.
8. **Hallazgos menores del control de vigencia, declarados y sin corregir.** Las propuestas del auditor están en su informe.
   - **X-a:** `adoptar_archivo` pisa el estado de una terminación no cerrada. Si al terminar en `pendiente_de_datos` se archiva una ficha cerrada anterior, esa ejecución acaba con `estado_analisis` vacío, aunque la ficha y la fila dicen `pendiente_de_datos`. La siguiente ejecución lo corrige. Con el código anterior quedaba en cambio una aprobación caducada registrada.
   - **X-b:** es una consecuencia de W-e, y conservadora. Relanzar el paso 14 de un expediente aprobado cuando la ficha regenerada cambia archiva la aprobación y exige una auditoría nueva, aunque el cambio sea solo un metadato (por ejemplo, `version_config`). La persona responsable decide si las diferencias solo de versiones deben contar como sustitución.
   - **X-c:** un fallo de esquema de la ficha en el paso 14 termina con código 4 y un motivo que no es la causa. El origen es anterior a la 4.7.1: `ficha.py` pone `cierre` siempre que el paso es 14. Antes se publicaba «no_entregable / APROBADO».
   - **X-d:** márgenes de la detección por fecha. Todos retiran de más o están cubiertos por el límite residual del Anexo D:
     - una fecha ambigua día/mes de otro expediente de la misma empresa se retira;
     - «3-Nov-26» y formatos parecidos no se leen;
     - una fila vigente con los números redondeados se retira, y solo se vuelve a publicar si `resumen.py` escribe en ese CSV.

     El Anexo D debería enumerar los formatos y matizar esos dos puntos.
   - **X-e:** en 2025 la amortización de derechos de uso es 6,760 (CF_2025, p. 52, según el auditor); el informe del N3 cita la de 2024 (4,768). Además, el §6 repite una frase. Ningún cálculo cambia.
   - **X-f:** el recuento de 40 de 44 que Claude declaró en el encargo del control era el de antes de fijar su material; con el material fijado eran 41. La cabecera de `comprobar_entrega_4_7_1.py` dice «unos 4 minutos» y tarda unos 1,2.

## Verificación del paquete 4.7.1
Se verificó sobre una descompresión limpia del ZIP candidato, cuyo contenido es el mismo que el del final salvo este apartado y los archivos que dependen de él (`CAMBIOS_ARCHIVOS.txt` y el manifiesto). El ZIP final se volvió a verificar del mismo modo. Sus huellas están en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque escribirlas cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA», en unos 6,5 minutos.
- manifiesto: 1.454 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base;
- batería del resumen: **45/45**, «RESULTADO resumen: PASA»;
- batería de cierre: **55/55**, «RESULTADO cierre: PASA».

**Aparte,** sobre la misma descompresión y después de la verificación completa, todas con salida idéntica a la de referencia:
- 45 de la 4.2, 217 de la 4.3, 43 de la 4.3.1, 72 de la 4.4, 60 de la 4.5, 24 de la 4.6 y 23 de la 4.6.1, todas con código 0;
- 4.7: **46 de 49**, por diseño. Lo esperado es una salida idéntica a `resultados/comprobar_entrega_4_7_en_arbol_4_7_1.txt`, y sobre su ZIP intacto da 49 de 49;
- **4.7.1: 44 de 44**, código 0.

Tras las pruebas, los 1.454 archivos del manifiesto siguen intactos. P1 conserva `b4e47afc…c445a4`.

**Respecto a la 4.7:**
- cambian 11 archivos: `cierre_v2.py`, `ficha.py`, `resumen.py`, `pipeline.py`, `test_resumen_v2.py`, `verificar_paquete.sh`, el Anexo D, `DECISIONES.md`, `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`;
- se regeneran `CAMBIOS_ARCHIVOS.txt` y el manifiesto;
- no desaparece ninguno;
- hay 42 nuevos, todos en `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7_1/`;
- `informe.py`, los originales y los expedientes de la 4.4 a la 4.7 son idénticos.
