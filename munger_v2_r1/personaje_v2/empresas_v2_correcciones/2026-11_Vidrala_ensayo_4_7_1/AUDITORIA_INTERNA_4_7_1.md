# Auditoría interna de Claude · entrega 4.7.1

Es una **auditoría interna de Claude**, hecha con un contexto separado del que preparó la entrega (el auditor no vio cómo se hizo el trabajo). **No es una revisión externa** ni sustituye a la revisión independiente. Se distinguen **hechos comprobados por el auditor** (reproducidos con comandos o guiones propios), **interpretaciones** y **propuestas**. Las propuestas no cambian criterios financieros, probabilidades, r, k, escenarios ni conclusiones; las decisiones son de la persona responsable.

## Material auditado

- Lista de huellas: `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7_1/MATERIAL_AUDITORIA_4_7_1.txt`, SHA-256 `72ad66795bf7dbcf7d7729417acbff916a251d8e32859904b9d4355e7ec7050e`, 32 archivos.
- `grep -v '^#' MATERIAL_AUDITORIA_4_7_1.txt | sha256sum -c` desde `munger_v2_r1/`: **al principio (10-nov-2026, 10:03 UTC), 32 de 32 OK**; **al final (10:30 UTC), 32 de 32 OK** (y la lista conserva su SHA-256).
- Además, el auditor tomó al principio las huellas de los 1.437 archivos del árbol real y, antes de escribir este informe, comprobó que no había cambiado ninguno.
- Referencias: el ZIP de la 4.7 (`/home/claude/entrega47/munger_v2_r1_entrega4.7_csv_y_revision_financiera.zip`, SHA-256 `b560977a…764c5b`), descomprimido en el scratchpad; su `MANIFIESTO_SHA256.txt` es idéntico byte a byte a `reproduccion/MANIFIESTO_SHA256_4_7.txt`.
- Dónde se ejecutó: solo en copias del scratchpad de la sesión (`…/scratchpad/aud471/munger_v2_r1`, copia del árbol 4.7.1; `…/scratchpad/aud471_c47/munger_v2_r1`, la misma copia con `cierre_v2.py`, `resumen.py` y `ficha.py` de la 4.7; `…/scratchpad/aud471_zip47/munger_v2_r1`, el ZIP 4.7), con `PYTHONDONTWRITEBYTECODE=1` y `python3 -B`/`-I`. Guiones del auditor en `…/scratchpad/aud471_pruebas/` (`w1_variantes.py`, `n3_independiente.py`, `filas_reales.py`); salidas en `…/scratchpad/aud471_out/`.
- El auditor **no modificó nada** del árbol real; este informe es el único archivo que escribe en él.

## Qué se ejecutó

| Comando (en la copia salvo indicación) | Resultado |
|---|---|
| `sha256sum -c` de la lista de material (árbol real, solo lectura), al principio y al final | 32/32 OK las dos veces |
| `diff -rq` ZIP 4.7 ↔ árbol 4.7.1 | Cambian solo los 7 archivos declarados (`cierre_v2.py`, `resumen.py`, `ficha.py`, `test_resumen_v2.py`, `verificar_paquete.sh`, `ANEXO_D…`, `DECISIONES.md`), más la carpeta 4.7.1. `pipeline.py` e `informe.py`, iguales |
| Integridad: P1, 489 originales, carpeta 4.7 (57 archivos) frente al manifiesto 4.7 | P1 = `b4e47afc…c445a4`; 489/489 y 57/57 OK |
| `cd personaje_v2 && python3 -B pruebas/test_resumen_v2.py` (código 4.7.1) | **37/37** (18 s) |
| La misma batería con el código 4.7 (copia `aud471_c47`) | **34/37**; fallan exactamente las 3 de W-1, igual que `reproduccion/pruebas_resumen_con_codigo_4_7.txt` |
| `python3 -B pruebas/test_cierre_v2.py` | **55/55** |
| `bash verificar_paquete.sh completa` (copia, 6 min 35 s) | resumen 37/37 PASA; cierre 55/55 PASA; entorno, piloto, pruebas de la reparación y nombres PASA; **manifiesto FALLA** (el `MANIFIESTO_SHA256.txt` raíz sigue siendo el de la 4.7: 7 modificados y los archivos nuevos; ver C-c) → global FALLA (1 bloque) |
| `python3 -I …/scripts/comprobar_entrega_4_7_1.py` | **34 de 35**; solo no cumple «Existe al menos una revisión interna con su material fijado» |
| `python3 -I …_4_7/scripts/comprobar_entrega_4_7.py` sobre el ZIP 4.7 | 49 de 49 (confirma la afirmación del cierre técnico §3) |
| `reproducir_w1.py --raiz` ZIP 4.7 / árbol 4.7.1 | REPRODUCIDO / NO SE REPRODUCE |
| `w1_variantes.py` (escenarios S1–S16, código 4.7.1 y código 4.7) | Ver hallazgos W-a a W-g y «Comprobaciones sin hallazgo» |
| `filas_reales.py` (todas las filas `resumen_v2.csv` del árbol frente a sus fichas) | Las 10 filas reales coinciden con su ficha por contenido (`_fila_de`) |
| Ida y vuelta del `resumen_v2.csv` de la 4.6.1 por LibreOffice (CSV → ODS → CSV, filtro estándar) | `precio_si` pasa de `65.68808732041568` a `65.6880873204157`: la fila deja de coincidir por contenido |
| `n3_independiente.py` (réplica propia del motor B, sin importar `analisis_n1_n3.py`) | Base 53,6704 / 70,7722 / 86,4888 (= libro); 27 combinaciones = 4.7 (desviación ≤ 9,4·10⁻⁵, redondeo del CSV); `n3_anio_a_anio.csv`, 100 filas, desviación ≤ 7,9·10⁻⁴; sensibilidades = CSV (≤ 9,5·10⁻⁵) |

## Hallazgos

### W-a · bloqueante · El criterio por contenido exacto hace permanente la aprobación caducada que la 4.7 retiraba

**Hecho comprobado por el auditor.** `_fila_de` exige igualdad de cadenas en diez columnas (`(r.get(k) or "") == str(x)`). La 4.7 identificaba la fila sin registrar del predeterminado por empresa y fecha de una ficha cerrada archivada. La 4.7.1 cambió también la **detección**, no solo la exclusión de la ficha vigente, y lo mismo en la rama sin ficha de `resumen.py`. Se han hecho tres reproducciones, cada una sobre una copia nueva del expediente aprobado de la 4.6.1, con los dos códigos.

- **S15. Escenario F-2 de la prueba 21:** marcador en B101 y pipeline con `resumen_csv` configurado fuera del predeterminado.
  - Con la fila idéntica, las dos versiones la retiran (control).
  - Con `precio_si` = `65.6880873204157` (justo lo que deja LibreOffice al abrir y guardar el CSV) o con `precio` = `87.90`:
    - la 4.7 la retira en la primera llamada (código 4);
    - la 4.7.1 la deja en «concluido / APROBADO» tras pipeline, pipeline, `ficha.py --estado concluido` y `resumen.py` (códigos 4, 4, 3 y 3).
- **S14. La ruta exacta de W-1** (`resumen.py COPIA OTRO_DESTINO.csv`), en dos casos:
  - con la fila reformateada (`87.90`);
  - con `ficha.json` editada a mano tras el cierre (precio 99,9; motivo «cambió después del cierre») en un expediente sin ficha archivada previa igual.

  Con la 4.7 se retira en la segunda llamada. Con la 4.7.1 no se retira en ninguna de las seis llamadas (`resumen.py` OTRO ×2, `resumen.py` PRED, `informe.py`, `ficha.py`, `pipeline.py --desde 14`). Con el archivo `01_…` de la 4.6.1 presente, la ficha editada sí se retira, pero solo porque esa ficha archivada antigua coincide con la fila publicada.
- **S13. Rama sin ficha** de `resumen.py`, con el destino recibido aprobado y `precio` = `87.90`: la 4.7 lo retira y la 4.7.1 no.

**Interpretación.**
- La 4.7.1 cierra la secuencia de §1, pero cambia a peor esta clase de variantes: lo que en la 4.7 duraba «hasta la llamada siguiente» (W-1) ahora no lo retira ninguna llamada, para cualquier fila que no sea byte a byte la de una ficha archivada.
- Dentro de la cadena de herramientas las filas coinciden (`filas_reales.py`). Pero el resumen es una tabla para personas, y la regla F-2 existe precisamente para filas antiguas sin registrar. Basta abrirla y guardarla en una hoja de cálculo.
- El caso de la ficha editada lo prevé el propio `motivo_vigencia`.
- El Anexo D no declara el límite.
- Es el sentido no conservador: deja una aprobación publicada, contra el principio del proyecto («retira una aprobación, nunca la crea»).
- Cambia estados publicados, por eso es bloqueante.

**Propuesta.**
- Detectar como en la 4.7: misma empresa y fecha de una ficha cerrada archivada.
- Usar el contenido solo para **excluir** la fila de la ficha oficial vigente, comparando los números normalizados (float con tolerancia) y no las cadenas.
- Si la exclusión falla, se retira y `resumen.py` vuelve a publicar: es el sentido conservador.
- Añadir pruebas con los escenarios S13, S14 y S15 y con la conservación de la fila vigente (S5).
- Declarar el límite residual en el Anexo D.

### W-b · menor · Con el registro ilegible, la ruta de W-1 no retira el predeterminado

**Hecho comprobado por el auditor (S4).**
- Con `publicaciones_resumen.json` ilegible (`{ilegible`), `resumen.py COPIA OTRO` termina con código 5 y deja la fila del predeterminado en «concluido / APROBADO». La lista de pendientes solo nombra el registro.
- Por `informe.py`, el predeterminado sí se retira, porque es el CSV de la llamada.
- Restaurado el registro, la llamada siguiente lo retira.
- La 4.7 se comporta igual.
- La causa: `sincronizar_resumenes` vuelve antes, en la rama `RegistroIlegible`, sin calcular `pred_aprobado`, aunque la identificación de esa fila no depende del registro.

**Interpretación.** El código 5 avisa y el estado se recupera. Aun así, el Anexo D presenta el predeterminado como «destino conocido» y dice que, con el registro ilegible, «se retiran igualmente» los destinos conocidos.

**Propuesta.** Calcular `pred_aprobado` antes de leer el registro y pasarlo como `csv_extra` también en esa rama. Añadir una prueba.

### W-c · importante · Las pruebas 23–25 no fijan todo lo que pidió la revisión, y el cierre técnico lo sobredeclara

**Hecho comprobado por el auditor** (lectura de `test_resumen_v2.py`, líneas 399–437):

| Prueba | Comprueba | No comprueba |
|---|---|---|
| 23 | el predeterminado; la fila ajena; su historial (+1, «APROBADO»); las salidas archivadas; `historial_cierres` +1; que el otro destino no tiene aprobación; el reintento | el historial del otro destino, `estado_pipeline.json` y el registro |
| 24 (las dos filas aprobadas) | el código, las dos filas y la ajena | ningún historial, el archivo de salidas, `estado_pipeline` y el reintento |

- Ninguna prueba cubre la conservación de la fila vigente con el criterio nuevo, ni las filas no idénticas (W-a).
- El cierre técnico §2 dice que la primera prueba comprueba «los dos historiales», y no es exacto.
- El comportamiento sí es correcto, según el auditor:
  - S1 y S2: historial del predeterminado 1 → 2 y del otro destino 0 → 1; ficha, informe y `cierre_vigente.json` archivados (`02_…`); `estado_pipeline` de concluido/APROBADO/paso 14 a `None`/`None`/paso 13, con `cierres_archivados` de 1 a 2; registro con «retirada»; filas ajenas intactas; reintentos sin duplicar el historial.
  - S5: la fila vigente se conserva con `resumen.py`, `informe.py` y el pipeline.

**Interpretación.** La revisión pidió que una prueba comprobara de inmediato las dos filas, los archivos y los historiales. Ninguna lo hace junto.

**Propuesta.**
- Ampliar la 24 con los dos historiales, el archivo, `estado_pipeline` y el reintento.
- Añadir S5 y las variantes de W-a.
- Corregir la frase del cierre técnico.

### W-d · menor · La sustitución directa en `ficha.py` devuelve 0 y «OK … estado concluido» con una ficha que ya nace no vigente

**Hecho comprobado por el auditor (S9, S10).**
- La sustitución archiva la ficha anterior (`02_…`) y retira en la misma llamada la fila del predeterminado (historial +1, fila ajena intacta).
- Escribe una `ficha.json` con `cierre: APROBADO` y un `cierre_vigente.json` nuevo, y devuelve **0**.
- Para esa ficha, `motivo_vigencia` dice: «el pipeline no registró una auditoría APROBADO válida (auditoria = None)».
- La llamada siguiente devuelve 3 y archiva la ficha (`03_…`).
- Con el predeterminado sin escritura posible, devuelve 5 (retirada pendiente), y al recuperar el acceso se completa.

**Interpretación.**
- La Observación del cierre técnico es exacta para la llamada directa.
- El código 0 y el mensaje dan por cerrada una ficha que el propio sistema rechaza.
- El Anexo D documenta para `ficha.py` los códigos 3 y 5, no este 0. La prueba 25 fija `rc == 0`.

**Propuesta (decisión de la persona responsable).** Como mínimo, documentar ese 0 en el Anexo D y avisar en la salida. Como alternativa, no escribir `cierre` en la ficha nueva y devolver 3.

### W-e · importante · Dentro del pipeline, la sustitución termina en «concluido», código 0, sin salidas oficiales y con su registro sobrescrito

**Hecho comprobado por el auditor (S16; igual con el código 4.7).** Se cambia `datos_v63.json` (fuera del material: `H4_moneda`), en una copia vigente, y se ejecuta `pipeline.py --desde 14`.
- `ficha.py` sustituye la ficha (archivo `02_…`).
- `informe.py` rechaza la nueva y la archiva (`03_…`).
- `resumen.py` ya no encuentra ficha.
- El pipeline imprime «FIN · estado concluido · auditoría APROBADO» y termina con **código 0**.
- Queda así:
  - sin `ficha.json` ni `informe.md`;
  - con la fila del predeterminado retirada;
  - `estado_pipeline.json` dice concluido/APROBADO/paso 14, con **1** entrada en `cierres_archivados` (las de `02` y `03` se pierden, aunque sus carpetas y `RETIRADA.json` existen).
- Una segunda ejecución vuelve a publicar «concluido / APROBADO» con la ficha nueva, ya vigente.

**Interpretación.**
- El pipeline guarda su estado en memoria y sobrescribe el que dejaron `ficha.py` e `informe.py`.
- En esta ruta no se cumple la frase de la Observación («deja el pipeline sin aprobación registrada»), ni el Anexo D: el estado del pipeline deja de decir `concluido` y registra la retirada en `cierres_archivados`.
- Es anterior a la 4.7.1 y conservador para el CSV.
- Pero es la ruta análoga de sustitución por la que pasa normalmente `ficha.py`, por ejemplo al subir la versión de la configuración, y el pipeline declara completado lo que no lo está.

**Propuesta.**
- Tras cada generador de `salidas_finales`, recargar el estado del disco o comprobar la vigencia antes de declarar `concluido`.
- Terminar con un código distinto de 0 si no hay ficha vigente.
- Añadir una prueba.
- La persona responsable decide si se repara en la 4.7.1 o se registra como límite declarado.

### W-f · menor · Un destino registrado como «retirada» cuya fila reaparece no se vuelve a retirar

**Hecho comprobado por el auditor (S12; igual en la 4.7).**
- Tras retirar con `informe.py` (el predeterminado queda registrado como «retirada»), se restaura el CSV de una copia de seguridad, y la fila vuelve a «concluido / APROBADO».
- Ni `resumen.py COPIA OTRO` (código 3) ni el pipeline (código 4) la retiran.
- `sincronizar_resumenes` sí la detecta (`pred_aprobado`), pero `retirar_publicaciones` descarta el `csv_extra`, porque el destino ya está en el registro y su entrada no está «viva».

**Interpretación.** El estado «sin_archivo» se vuelve a vigilar en cada sincronización; el estado «retirada», no. No está declarado.

**Propuesta.** Tratar `pred_aprobado` como objetivo aunque el destino esté registrado, o volver a comprobar las entradas «retirada». Si no se hace, declararlo en el Anexo D.

### W-g · menor · Trazabilidad de la retirada del predeterminado

**Hecho comprobado por el auditor (S1).** El material es conocido por la ficha archivada (`74b94f8072dd58c1`). Aun así:
- la fila activa dice «APROBADO del material sin registrar»;
- la fila del historial lleva `material_auditado` vacío y el motivo genérico «sin salida oficial vigente…».

**Propuesta.** Pasar el material de la ficha archivada que coincide y el motivo concreto de la invalidación.

### N-a · menor · Dos afirmaciones presentadas como «Hechos publicados» no están en los textos

**Hecho comprobado por el auditor.** CF_2025, PDF p. 44, dice: «…primarily in the renewal of furnaces…». El informe, §3, añade en la lista de hechos dos frases que los textos no contienen:

| Frase del informe | Qué hay en los textos conservados |
|---|---|
| «Es inversión de renovación, no de ampliación.» | «primarily» no excluye ampliación, eficiencia ni descarbonización. El propio informe reconoce después que los textos no separan esas partes |
| «Los hornos se reconstruyen por campañas.» | Ninguna aparición de *campaign*, *rebuild* ni *cold repair* en CF_2016–CF_2025. Los 8–16 años de la p. 14 son la vida útil contable de «furnaces, installations, and production machinery», no la duración de una campaña, aunque el §4 los usa así |

El resto de citas y signos comprobados reproduce, en valor y en página:
- D&A 132,948 y 117,720;
- inversión (178,746) + (9,757) = 188,503 y 168,800;
- 2020: 84,144 y 134,248;
- vida útil 8–16; PERTE 10,298 y 6,316 «from 2026 onwards»;
- compromisos 66,610 y 9,622; reparación y mantenimiento (41,854);
- apagón del 28-abr-2025, p. 72; autogeneración, p. 37;
- la serie 2016–2025 de la Historia (0,73 · 1,16 · 1,15 · 1,10 · 1,60 · 1,27 · 1,41 · 1,74 · 1,43 · 1,42; ventas −2,2 % y −7,8 % en los dos únicos años con caída).

**Propuesta.** Pasar las dos frases a «Interpretación» o retirarlas, y conservar «sobre todo» (*primarily*).

### N-b · menor · Los límites de la hipótesis de mantenimiento apuntan en un solo sentido

**Hecho comprobado por el auditor.**
- La D&A de 2025 incluye 7,913 mm de amortización de intangibles. De ella, 4,492 son de la cartera de clientes adquirida (CF_2025, p. 46), que no es reposición.
- La D&A salta de 87,2 a 117,7 y a 132,9 con el cambio de perímetro (Brasil desde nov-2023, Italia fuera en 2024).
- La fila 2020 de la tabla es el publicado de 2020, con Italia (`evidencia.json`), frente a las continuadas de 2024–2025. El informe no lo señala en la tabla.
- La «evidencia» de D-N3b solo enumera indicios de reposición mayor que la amortización.
- La propuesta «=D&A» es, de las tres opciones de D-N3b, la de mayor valor.

**Interpretación.**
- Nada de esto cambia cifras ni la conclusión de que no puede fijarse una cifra.
- La propuesta no depende de buscar un valor más favorable: mantiene la convención, no cambia valores, y R1 baja el MALO frente a R0.
- Pero la revisión pidió «evidencia y límites», y conviene decir de forma explícita que «=D&A» es el extremo favorable y que se elige por falta de cuantificación, no por evidencia.

**Propuesta.** Añadir esos límites en el §3 del informe y en D-N3b. Sin cambios de cálculo.

### N-c · menor · «Qué sustituye» es impreciso y deja fuera contenido vigente

**Hecho comprobado por el auditor.**
- La «fila de “cálculos de caja” del §4.3» del informe 4.7 no existe. La viñeta «Necesidades de caja» está en el §4.2, y el §4.3 es la tabla R0–R1–R2.
- El §6 del informe 4.7 sigue describiendo «la cobertura de los compromisos», una columna que la 4.7.1 retira.
- Al sustituir el §4.2 entero se pierden dos cosas que el documento nuevo no vuelve a decir:
  - el circulante del 14,70 % en 2025 y del 14,88 % en 2024;
  - la advertencia de que el terminal reinvierte g ÷ ROIC desde el año 11 con el MALO por debajo del máximo.

**Propuesta.** Enumerar con exactitud lo sustituido (§4.2 y la frase del §6) y conservar esa advertencia.

### C-a · menor · El control 4.7.1 constata algunas cosas que debería reejecutar, y le faltan comprobaciones

**Hecho comprobado por el auditor.**
- Los controles de 37/37, 34/37 y 55/55 son de tipo [constata]: leen salidas conservadas, sin la huella del código con que se obtuvieron.
- «Su fila … se conserva» evalúa `_fila_de`, pero no ejecuta la sincronización.
- «Niveles de mantenimiento» compara `matriz.json` con constantes escritas en el propio control, así que es en parte circular. El cotejo con la fuente está en la evidencia.
- No hay ningún control de las variantes de W-a ni de la coherencia entre documentos.
- El resto es sustantivo: regeneración byte a byte de 8 salidas, identidades, 4.7 intacta y W-1 reejecutado.

**Propuesta.** Reejecutar `test_resumen_v2.py` en el control (unos 20 s) y añadir como controles los escenarios S5 y S13–S15 de esta auditoría.

### C-b · menor · Detalles de documentación

**Hecho comprobado por el auditor.**
- La cabecera de `comprobar_integracion_verificador_471.py` sigue hablando de la «batería de cierre», de `test_cierre_v2.py` y de 55 pruebas, con otro nombre de archivo en «Uso». El código comprueba bien la batería del resumen con mínimo 37: 13 de 13.
- La lista de códigos de las llamadas directas del Anexo D no recoge el 0 de la sustitución en `ficha.py` (W-d).

**Propuesta.** Corregirlo al rehacer la documentación.

### C-c · menor · Falta el empaquetado

**Hecho comprobado por el auditor.**
- `VERSION`, `CONTINUIDAD.md`, `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt` siguen siendo los de la 4.7.
- `sha256sum -c` del manifiesto raíz sobre el árbol real da 7 FAILED, los archivos declarados.
- `verificar_paquete.sh` falla en el bloque del manifiesto hasta regenerarlo.
- El control 4.7.1 exime esos archivos.

**Interpretación.** Es lo esperado antes de empaquetar, pero hay que hacerlo antes de entregar.

## Comprobaciones sin hallazgo

- **W-1, secuencia de la revisión (S1; `reproducir_w1.py`).**
  - Con el código 4.7 se reproduce y con el 4.7.1 no.
  - Todo de inmediato y sin segunda llamada: código 3, fila del predeterminado «SIN APROBACIÓN VIGENTE …», historial +1, `historial_cierres/02_…` con `RETIRADA.json`, `estado_pipeline` sin `concluido` ni APROBADO, fila ajena intacta, sin aprobación en el otro destino.
  - Reintentos estables (códigos 3, 3, 3 y 4) sin duplicar el historial.
- **Variantes cubiertas:**
  - otro destino también aprobado (S2: las dos filas y los dos historiales, de inmediato);
  - predeterminado sin escritura posible (S3: código 5 con «retirada_pendiente»; se completa al recuperar el acceso);
  - expediente trasladado con su predeterminado (S11);
  - fila idéntica de otra empresa, que se conserva (S6);
  - fila de la ficha vigente, que se conserva (S5);
  - `informe.py` y pipeline con la configuración por defecto, también con filas reformateadas (S7, S8), porque allí el predeterminado es el CSV de la llamada.
- **Pruebas:** 37/37 con el 4.7.1 y 34/37 con el 4.7 (las tres de W-1); 55/55 de cierre; integración con mínimo 37 correcta; `verificar_paquete.sh completa` con resumen y cierre en PASA.
- **N3, identidades:**
  - reinversión = circulante + fija neta, y bruta = 132,948 + fija neta, en las 100 filas de `n3_anio_a_anio.csv` (≤ 1·10⁻⁵) y en las 27 de la matriz;
  - R1, año 1: ΔV −14,6516; circulante −2,15434; fija 0; bruta 132,948 (la 4.7 daba 130,79366);
  - R0: fija −14,12522; bruta 118,82278 (la 4.7 daba 116,66844).
- **N1/N2 conservados:**
  - matriz, ponderados y precios de Sí idénticos a la 4.7;
  - D-N1 y D-N2 idénticas a la 4.7;
  - `circulante_sin_capacidad` reproduce la formulación inicial del R1 de la 4.7 en T0·M0, T0·M1 y T0·M2.
- **Sensibilidades, recalculadas de forma independiente** con una resta analítica (x·D&A en los años 1–10 y x·D&A·(1+g)/(r−g) en el terminal, sin efecto fiscal):
  - +20,9 % solo MALO: 42,16 / 67,32 (−1,93) / 60,13 (−4,13);
  - +41,8 % en todos los escenarios: 48,61 (−20,64) / 44,01 (−20,25);
  - capacidad no conservada: 69,18 (−0,06) / 64,13 (−0,13);
  - la recuperación del MALO es del +1,81 % desde el mínimo del año 7.
- **Presentación y reglas.** Las sensibilidades se presentan como exploratorias y no como cotas, y la comparación con los compromisos se retira. D-N3 y D-N3b quedan sin `decision`, `fecha` ni `confirmado_por`, y nada se presenta como decidido. Se mantienen los avisos de no comparabilidad con 87,9 y de que no es una recomendación. r = 0,09, probabilidades 0,2/0,6/0,2, k = 3 y puente 160,784, sin cambios. No se reabren H1–H3.
- **Integridad:** originales, 4.7 y P1 intactos; nada modificado fuera de lo declarado.

## Veredicto

**Con hallazgos bloqueantes** (1). W-a: la identificación por contenido exacto introduce una regresión frente a la 4.7. Una aprobación caducada sin registrar en el predeterminado, si la fila no es byte a byte la de una ficha archivada (CSV guardado por una hoja de cálculo, o ficha editada tras el cierre), ya no se retira en ninguna llamada: ni en la ruta de W-1, ni en el pipeline configurado (F-2), ni en `resumen.py` sin ficha.

La secuencia literal de §1 sí queda cerrada, y N3 queda subsanado en lo sustancial: identidades, evidencia, sensibilidades y propuestas correctas, con observaciones menores de redacción y límites.

Importantes: W-c (cobertura de las pruebas frente a lo pedido) y W-e (sustitución dentro del pipeline, anterior a la 4.7.1). La revisión de estas correcciones debería preceder a solicitar la adopción humana de D-N3 y D-N3b.
