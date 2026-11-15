# Revisión de lo afectado por las correcciones · entrega 4.12

**Qué es.** Segunda revisión **interna**, limitada a lo que cambió después de la primera (`REVISION_INTERNA_4_12.md`, 12-nov, 23:10–23:30). No sustituye a la primera ni a la revisión externa. La hace un agente revisor (Fable) en un contexto separado, que no hizo el trabajo ni las correcciones.

**Fecha y hora.** 13 de noviembre de 2026, de 00:15 a 00:27 (hora de la consola, CET).

**Objeto.** El árbol `/home/claude/trabajo_4_12/munger_v2_r1` tal como estaba entre las 00:15 y las 00:26. Rutas relativas a `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/` salvo que se diga otra cosa.

**Cómo se trabajó.** Solo lectura del árbol. Los tres expedientes se copiaron a la carpeta auxiliar del revisor y allí se ejecutaron funciones sueltas del código (`entradas_economicas`, `trazabilidad_v64`, `dominios_v64`), lecturas con openpyxl y `verify_quotes_v2.py` sobre copias de informes. El estado anterior se tomó de la copia que la orquestación guardó a las 23:09 (`scratchpad/verif412/r0`, que es el «antes» de los diff del encargo) y se comparó directamente con el árbol, porque los diff entregados (00:08) no recogen cambios posteriores del informe integrado (§5), de la comparación de protocolos ni de la propuesta. No se ejecutó el pipeline, LibreOffice ni ninguna batería. No se usó internet. Los marcadores pendientes ([VERIFICACION_FINAL], [REVISION_RE], [FABLE_RE], [ENTREGA]) y el archivo `resultados/LEEME_CONTROLES_HISTORICOS_4_12.md`, que todavía no existe, no se cuentan como hallazgos.

## 1. Veredicto en breve

| Gravedad | Número | Hallazgos |
|---|---|---|
| Bloqueante | 0 | — |
| Importante | 1 | RA1 |
| Menor | 6 | RA2–RA7 |
| Observación | 5 | RA8–RA12 |

- **Hechos.** Las correcciones del código hacen lo que dicen y no cambian ninguna cifra: en los tres expedientes, `precio.json`, `resultados.json`, `fase_c.json`, la configuración, las variantes y los libros evaluados son idénticos byte a byte a los de las 23:09. Los estados, las acciones y los veredictos son los mismos. Cada auditoría vigente responde a su solicitud y a su material, y las 24 huellas de cada material coinciden con los archivos.
- **El hallazgo importante (RA1)** es un efecto de la corrección R1 que no se propagó: el control de entrega `scripts/comprobar_entrega_4_12.py` compara la huella de la relación nueva con la huella guardada de la relación anterior y falla en los tres expedientes. No afecta a ningún resultado, pero la verificación final no puede pasar sin corregirlo.
- **Los menores** son afirmaciones de los documentos que el material no sostiene tal como están escritas (la medición de R8, un aviso de auditoría que el informe repite y que el libro contradice, el resumen de R7, restos de cifras anteriores) y una corrección de R3 que alcanza a la etiqueta pero no a la regla de coherencia.

## 2. Hallazgos

### RA1 · Importante · El control de entrega falla en los tres expedientes desde la corrección R1

**Evidencia.**
- `scripts/comprobar_entrega_4_12.py`, líneas 136–139: `inst = EE.instantanea(libro)` y, en la condición, `inst["huella"] == var["entradas_economicas"]["huella"]`. Desde la corrección, `instantanea` usa por defecto la relación «4.12+H13».
- Las variantes de los tres expedientes no se recalcularon (son las de las 21:31 y las 22:40) y guardan la instantánea de la relación «4.12», sin campo `version`.
- Reproducción (script `chk1.py` de la carpeta auxiliar, sobre copias): huella guardada `ef796fea2af3…` (216 celdas) frente a `5d6686198fce…` (226) en los dos expedientes de Vidrala; `7bff0b2e361f…` (216) frente a `5726038f394b…` (226) en Viscofan. La condición da `False` en los tres. Con `EE.comparar(guardada, libro, activa.xlsx)`, que es lo que usa el pipeline, no hay diferencias.

**Consecuencia.** La comprobación «las variantes son de las entradas económicas del libro final» del control de entrega fallará en la verificación final y el script saldrá con código distinto de 0. Es un fallo del control, no de los expedientes.

**Qué haría falta.** Que el control use `EE.comparar` con el libro de la variante activa, igual que los pasos 10 y 12, y ejecutarlo antes de empaquetar.

### RA2 · Menor · La medición de R8 es de un ajuste parcial, y su consecuencia para el rango no se dice

**Evidencia.**
- `scripts/sensibilidad_derechos_de_uso_viscofan.py`, líneas 42–46. El método de θ equivalente es exacto para lo que hace: cambiar solo `Configuración V6.4!B60` (exceso histórico) de 40,813 a 67,864. Comprobado en el libro: B60 solo entra en B61, en B71 (rama Θ) y en B62, que solo se usa con SRF.
- La misma D&A entra también en `B55 = SUM(Historia!H31:L31)` y, por tanto, en D_hist (B57) y en f. El script no la ajusta: f sale 1,1292 con D_hist = 296,489. Con D_hist ajustado en los mismos 27,051 saldría 323,540 ÷ (323,540 − 33,932) = 1,117 (cálculo del revisor, no recalculado en el libro).
- Por la propia equivalencia del script, el extremo inferior del rango declarado (38,22 €, θ = 1 con B60 = 40,813) corresponde a θ = 40,813 ÷ 67,864 = 0,60 con el exceso corregido. Para θ entre 0,60 y 1, el precio de Sí queda por debajo de 38,22 €. No hace falta editar la plantilla para saberlo.
- `INFORME_INTEGRACION_4_12.md`, L13 (línea 355): «Sesgo medido de −0,71 € con θ = 0,5; sin medir con θ = 1» y «sigue … por encima del extremo inferior del rango calculado, 38,22 €». Lo mismo en `viscofan/CONTRASTE_VISCOFAN_4_12.md`, línea 53.

**Consecuencia.**
- «Contar solo la amortización que se repone con capex» describe más de lo que se midió: se midió el cambio del exceso, no el de D_hist ni el de la base de mantenimiento.
- La frase sobre el rango es cierta solo en θ = 0,5. Con el exceso corregido, el rango declarado 38,22–41,81 € no cubre la mitad alta del intervalo de θ. Estimación lineal del revisor con los tres puntos del script: unos 36,8 € en θ = 1, la misma que dio la primera revisión. La zona no cambia.

**Qué haría falta.** Decir en L13 y en el contraste que la cifra es del exceso solo, y que con el exceso corregido θ > 0,60 queda por debajo de 38,22 €.

### RA3 · Menor · El informe integrado repite como hecho un aviso de auditoría que el libro contradice

**Evidencia.**
- `INFORME_INTEGRACION_4_12.md`, línea 189: «la fase C dice que los ceros de las adquisiciones de 2021–2022 llegan a D_hist, cuando en el libro entran en F_hist».
- Libro `cierre_condicionado/Vidrala/Vidrala_v63_evaluada.xlsx`: `Historia!L31 = L30 + N(L13)`, `Configuración V6.4!B55 = SUM(Historia!H31:L31)` y `B57 = B55 + B56`. Valores: Σ fila 30 (H:L) = 508,178; Σ fila 13 = 12,418; B55 = 520,596; D_hist = 530,009. Las adquisiciones entran en D_hist **y** en F_hist (B62 = B60 + B59).
- El aviso viene de la auditoría de `cierre_bloqueo/Vidrala` (punto 10). La de Viscofan (punto 10) dice lo mismo de otra forma: la fila 13 «entra en F_hist pero no en f». En Viscofan, B55 = 296,489 = 280,328 + 16,161: también entra en D_hist y en f.
- El propio informe, en §3 (línea 147), lo dice bien: «entran en las bases de P-M1 (D_hist, F_hist, f)».

**Consecuencia.** El §5 contradice al §3 y al libro, y da por error un acierto de la fase C. Dos de las tres auditorías nuevas leen mal la vía por la que la fila 13 entra en el valor, que es justo lo que motivó R1. No cambia ningún veredicto: son avisos dentro de puntos que pasan.

**Qué haría falta.** Corregir la frase del §5 y anotar que el aviso de las dos auditorías es inexacto.

### RA4 · Menor · La corrección de R3 cambia la etiqueta «no cubiertas», pero la regla de coherencia de la acción sigue con el criterio anterior

**Evidencia.**
- `personaje_v2/scripts/objetivo_v64.py`, líneas 160–181: `cubiertas` exige ahora un ámbito aislado para los subparámetros de P-M1.
- `personaje_v2/scripts/pipeline.py`, líneas 1340–1351: `material_para_accion = false` se acepta si `ambito_parametro` no está vacío, y `null` se **rechaza** en ese caso («decide true o false»). `ambito_parametro` sigue contando «heredado», los componentes aislados y «activa sin P-M1».
- `fase_c.json` de los tres expedientes: `PM1.familia` lleva `material_para_accion = false` con un ámbito de cinco (Vidrala) o cuatro (Viscofan) variantes que quitan P-M1 entera. `ficha.objetivo.materialidad.materialidad_para_la_accion_no_determinada = []`.
- Anexo D §D.13 sigue definiendo `ambito` como «exactamente las variantes calculadas que lo varían».

**Consecuencia.** La misma hipótesis sale «no cubierta por el ámbito» y, a la vez, «no material para la acción según el ámbito». El pipeline impide declararla «no determinada». Las auditorías nuevas lo anotaron y el informe (§5) lo remite a L15 como juicio del agente; en realidad es la regla la que obliga a ese valor. No cambia el tratamiento ni la acción.

**Qué haría falta.** Declararlo como límite de la regla (no solo del juicio), o aplicar a `material_para_accion` el mismo criterio de ámbito aislado.

### RA5 · Menor · La respuesta a R7 no menciona un aviso activo en el extremo superior del rango de Vidrala

**Evidencia.**
- `resultados/dominios_variantes_4_12.md`, tabla de Vidrala: `solo_N1` (63,04 €) y `solo_N2` (65,72 €, extremo superior del rango) llevan activo `inversion_fija_para_crecer_negativa`. Reproducido con `dominios_v64.avisos` sobre copias: en el MALO, de −31,4 a −9,6 mm al año en los años 1–7.
- La línea «Lectura» del mismo archivo, el README de la V6.4 (§9, punto 15) y L14 del informe solo citan f = 1,309 en λ = 1,25.
- La nota de la tabla («por la caída de las ventas con R0 … no por el dominio») la escribe `scripts/dominios_variantes_4_12.py` (líneas 39–40) con una regla fija (`nwc_efectivo` vacío), no con una comprobación.

**Consecuencia.** El resumen de R7 es incompleto justo en el aviso que trata el punto 15 del README. La explicación de la nota es verosímil (R0 libera capital al caer las ventas, y el motivo del aviso no aplica), pero es una interpretación.

**Qué haría falta.** Citar los dos casos en la «Lectura», en el README y en L14.

### RA6 · Menor · R2 quedó corregido en el informe integrado, pero no en los documentos que lo acompañan

**Evidencia.** `REVISION_ECONOMICA_VIDRALA_4_12.md` (líneas 15 y 92), `COMPARACION_PROTOCOLOS_4_12.md` (línea 36) y `propuestas/PROPUESTA_HUMANA_4_12.md` (línea 121) dan 90,10 € y «un 37,1 % por encima» sin la fecha del precio. Ninguno de los tres contiene «31-dic-2025» ni «cierre de 2025».

**Consecuencia.** La propuesta es el documento sobre el que se decide, y compara con un precio de diez meses y medio antes de la fecha de análisis sin decirlo.

**Qué haría falta.** Añadir la fecha del precio donde se da la cifra.

### RA7 · Menor · Restos de cifras y horas anteriores en los documentos

**Evidencia.**
- `INFORME_INTEGRACION_4_12.md`, línea 59: «instantánea de las 216 entradas económicas» sin la fila 13 (el §5 sí lo explica); línea 54: «Grupo F (35 pruebas)» (son 36); línea 65: «Grupo G (14 pruebas)» (son 17); línea 147: «Dos pruebas nuevas en el grupo G» para R1 (es una nueva y una actualizada).
- `REGISTRO_PRUEBAS_4_12.md`, línea 25: G 17/17 «13-nov, 00:00–00:35». El archivo es de las 00:04 y el registro de la ejecución (`scratchpad/verif412/G_plano4.log`) terminó a las 00:03:55, después de tres ejecuciones con 16/17 (23:56, 00:00 y 00:02) mientras se ajustaba la prueba nueva.
- `resultados/diferencias_piloto_4_11_codigo_final.md`: la conclusión dice «cuatro diferencias» y el informe (línea 63), «cinco». Además, desde la corrección R11, la sección 14 del piloto regenerada diría «Variantes calculadas (13, incluida la activa)» (`informe.py`, línea 298; informe del piloto, línea 232): es una sexta diferencia de presentación que el script no compara.

**Consecuencia.** Ninguna en cifras. Son afirmaciones que no coinciden con el código ni con los registros.

### RA8 · Observación · Alcance real del aviso nuevo de la cadena (R4)

- Solo reconoce fechas «AAAA-MM-DD» y «D-mmm-AAAA», y solo en `periodo` y `ajuste_o_criterio` (`trazabilidad_v64.py`, líneas 55–62 y 214–218). «30 jun 2026», «1S26» o una fecha en la fuente o en la observación no avisan.
- Un texto correcto de una capitalización con fechas mixtas (precio de noviembre × acciones de diciembre, que es el caso real de Viscofan) nombraría la fecha de las acciones y daría un aviso de «fecha incoherente», porque la referencia de la capitalización es solo la fecha del precio.
- La tolerancia del valor es del 0,1 %: en Vidrala, «35.206.258 emitidas» coincide con 35,182858 dentro de ella.
- Solo se contrastan tres entradas. El revisor aplicó la misma comprobación de valor a todas las entradas de las dos cadenas y no salió ninguna otra.
- La prueba nueva del grupo G lee el expediente real `viscofan/experimental/Viscofan`: si algún día se corrigen esos textos heredados, la prueba fallará.

### RA9 · Observación · Con la regla nueva, `PM1.roic_terminal` nunca puede salir cubierto

`ambito_aislado("PM1.roic_terminal")` exige variantes que varíen solo ese parámetro, y la única que lo varía (`estructura_SR2`) lo hace ligado a la estructura. Si alguna vez condicionara el objetivo, saldría siempre «no cubierta», aunque SR2 calcule su alternativa. Es un falso aviso del lado prudente. En los tres expedientes no condiciona.

### RA10 · Observación · La fila 13 entra en la cadena de cualquier libro V6.4, también en modo heredado

`instantanea` y `trazabilidad_v64.construir` añaden la fila 13 si el libro tiene la hoja «Configuración V6.4», sea cual sea el modo. En un expediente V6.4 heredado que llegue al paso 12, la cadena llevará esa entrada (con la condición «modo experimental» en su texto) y, si hay ceros pendientes, un aviso más, aunque ahí la fila no entre en el valor. No afecta a ningún expediente de la entrega (la reproducción del heredado de Viscofan no llega al paso 12). En la V6.3 no cambia nada.

### RA11 · Observación · Instrucciones de las auditorías nuevas

- El contexto que recibieron (`resultados/relevos_agentes_4_12.md`, relevos 22–24) dice que «la instantánea … incluye la fila 13». En estos tres expedientes la instantánea guardada no la incluye. La auditoría del condicionado lo detectó por su cuenta.
- La auditoría anterior seguía en la carpeta, con la instrucción de no copiarla. Los textos nuevos son distintos y el registro de huellas no los confunde.
- Los tres envoltorios conservados en el área de trabajo coinciden literalmente con lo que publica el documento de relevos.

### RA12 · Observación · Detalles menores

- `informe.plano` escribe `None` para un valor nulo (informe de Viscofan, línea 233: «lambda = None»).
- El encargo de esta revisión cita cambios en la guía: `GUIA_RECORRIDO_SUPERVISADO.md` no cambió (misma huella que en la primera revisión).
- La lista de decisiones del §9.5 del informe (línea 331) no nombra D412-FUNDAMENTO; L15 sí.
- `objetivo_v64.lecturas_sin_protocolo` conserva la redacción «en N escenarios», sin «la activa».

## 3. Estado de cada hallazgo de la primera revisión

| Hallazgo | Estado | En una frase |
|---|---|---|
| R1 | Resuelto en parte | El código incluye la fila 13 y compara bien las instantáneas antiguas; los tres expedientes conservan la instantánea antigua (declarado en §5), y el control de entrega quedó roto (RA1). |
| R2 | Resuelto en parte | Corregido en el informe integrado; falta en la revisión económica, la comparación de protocolos y la propuesta (RA6). |
| R3 | Resuelto en parte | «PM1.familia» sale no cubierta en Vidrala, con prueba; la regla de `material_para_accion` no cambió (RA4). |
| R4 | Resuelto | La cadena de Viscofan lleva los cuatro avisos y la auditoría los comprobó; los textos heredados no se reescriben, y está declarado. |
| R5 | No resuelto en el código; bien declarado | Frase del §2.2, lista y apartado 7 de la revisión económica, L15, Anexo D y D412-FUNDAMENTO coinciden con los expedientes. |
| R6 | Resuelto | Aclarado en el contraste y en L1 con las cifras de θ = 0 y θ = 1; las salidas del expediente no cambian. |
| R7 | Resuelto en parte | Lectura de todas las variantes y README corregido; el pipeline sigue igual (declarado) y el resumen omite dos avisos activos (RA5). |
| R8 | Resuelto en parte | Hay una cifra medida y el método es exacto para el exceso; no mide el ajuste completo ni dice su efecto en el rango (RA2). |
| R9 | Resuelto | Recogido en el contraste, en §9.3 y en L5 y L10. |
| R10 | Pendiente, como estaba anunciado | La ronda completa pasó sobre el código anterior a las correcciones (23:38); sobre el final solo F (36/36) y G (17/17). |
| R11 | Resuelto | Línea de estado, sección 14 y rango con la redacción nueva en los tres informes. |
| R12 | No corregido; bien declarado | Recogido en el §8 y en la comparación de protocolos. |
| R13 | Resuelto | Las instrucciones publicadas de la fase A de Viscofan no citan el heredado; es la transcripción de la orquestación, que el revisor no puede contrastar con otra fuente. |
| R14 | Resuelto | El §9.3 lleva la salvedad. |

## 4. Lo que se comprobó sin encontrar problemas

**Código.**
- **R1.** `comparar` usa la relación con que se guardó la instantánea; con la antigua compara la fila 13 con la del libro de la variante activa, y sin ese libro da diferencia. En los tres expedientes, la fila 13 del libro y la de la activa son iguales. Un rastreo estático de precedentes desde `Análisis!B78:D78` y `C83` confirma que la fila 13 es la única de la Historia que entra por «Configuración V6.4» y no estaba en la relación; las filas 11 y 16–20 solo se alcanzan por el FCF histórico, la capitalización de I+D y la validación del Motor, como antes.
- **R3.** `cubiertas` reproduce las fichas: «PM1.familia» en Vidrala y ninguna en Viscofan.
- **R4.** Sin falsos avisos en Vidrala. Los cuatro de Viscofan corresponden a los textos.
- **Comillas.** Reproducido: `verify_quotes_v2.py` con el informe y el provisional de las 23:09 de Vidrala da 157 fragmentos no encontrados y código 1; con los de Viscofan, 0; con los actuales, 0. Los tres informes actuales no tienen ninguna comilla recta. Una línea de comprobación conjunta con la sintaxis heredada, añadida a los dos informes en una copia, no hizo fallar la verificación (un caso sintético, no una prueba general).
- **V6.3 y heredado.** En un libro V6.3 la instantánea, la comparación y la cadena no cambian. Los archivos del control de palancas, de las dos reproducciones de Viscofan y del piloto 4.11 son idénticos a los de las 23:09 (salvo cachés `.pyc`).

**Pruebas.** La batería tiene 127 pruebas (12 + 21 + 21 + 7 + 13 + 36 + 17). Las cuatro nuevas fallarían con el código anterior: la de R3 porque la familia contaba como cubierta, las de R1 y R4 porque usan funciones y avisos que no existían, y la de las comillas comprueba expresamente que la forma JSON falla. Registros: F 36/36 y G 16/16 a las 23:46; G 17/17 a las 00:03.

**Expedientes.**
- Material: 24 de 24 huellas en los tres. Solo cambian respecto de las 23:09 `cadena_trazabilidad.json`, `acreditacion_libro.json`, `informe_provisional.md` y, en Vidrala, `ficha_provisional.json`.
- Auditorías: SA-2dfc317a5da12a95 / d6ddea627a0b290d; SA-b485abe6363fd044 / 6111eb9cf586324c; SA-3ede622664324251 / e0959b899e66d5b8. Las tres, 16 de 16 y APROBADO. `cierre_vigente.json` coincide con ficha, informe y auditoría.
- Las fichas oficiales difieren de las del cierre anterior solo en el material y, en Vidrala, en `hipotesis_no_cubiertas_por_el_ambito`. Los informes, solo en las líneas que tocan R3, R11 y las comillas.
- Cadenas: 71, 71 y 70 entradas, 4 avisos cada una. Resumen, línea de estado y aptitud de uso («experimental») coinciden con las fichas.
- Los cierres anteriores están en `historial_cierres/` con su `RETIRADA.json`.

**Documentos.** Coinciden con los expedientes y con el código: las solicitudes y materiales del §5, lo que no se repitió (variantes, controles), R5 en sus cuatro sitios, R6, R9, R13, R14, el mínimo de 127 en `verificar_paquete.sh` y en el control de entrega, y el Anexo D en R1, R3, R4 y R5. La propuesta tiene ocho decisiones, ninguna firmada.

## 5. Límites de esta revisión

- **No se ejecutó nada que recalcule ni que escriba en el árbol.** Las baterías, los pasos del pipeline y los recálculos de R8 se toman de sus registros.
- **El árbol cambió mientras se revisaba.** El informe integrado, el registro de avance y el documento de relevos se escribieron entre las 00:14 y las 00:16. Las huellas del apartado 6 son las del momento de cerrar esta revisión.
- **Auditorías.** Se comprobó a qué responden, su veredicto y sus avisos. No se rehicieron sus dieciséis puntos.
- **Código leído en lo afectado.** Completos: `entradas_economicas.py`, las partes cambiadas de `trazabilidad_v64.py`, `objetivo_v64.py`, `informe.py` y `pipeline.py`, y los dos scripts nuevos del ensayo. No se releyó el resto.
- **Rastreo de precedentes.** Es estático: alcanza ramas que no se activan. Sirve para decir qué filas pueden entrar, no cuánto pesan.
- **Estimaciones propias.** Las cifras de RA2 marcadas como cálculo del revisor no están recalculadas en el libro.
- **Misma familia de modelos** que quienes construyeron y auditaron el trabajo.

## 6. Huellas SHA-256 de los archivos principales revisados

**Documentos y scripts del ensayo**

| Archivo | SHA-256 |
|---|---|
| `INFORME_INTEGRACION_4_12.md` | `1bac0ddff524fd3f6f7839aabd2e647d6265ad42d05bcb5c3e2ce4813b933ff5` |
| `REGISTRO_AVANCE_4_12.md` | `2227c3071be3134ec180cfc7a20fbf5d55c37ba345367fa1d33c1a50d0ba0f62` |
| `REGISTRO_PRUEBAS_4_12.md` | `4d32cd50cff652cb4c1a62532892b51909516678185c62283c96e6cf54b92c70` |
| `REGISTRO_ENTREGA_4.12.md` | `93984dfc57e24799f942e88e99c053ebc9d4ffa24c97878521c441168c3819c4` |
| `REVISION_ECONOMICA_VIDRALA_4_12.md` | `f6cbfed4b5ec9d064fc5884219664d353d63df55decfc689de4d7cd1b1478aee` |
| `COMPARACION_PROTOCOLOS_4_12.md` | `3fb83831152dd3fa86cb52d8a52f096f80241060f2dc4531df20b170925b14a2` |
| `viscofan/CONTRASTE_VISCOFAN_4_12.md` | `093ba9f75fa1eb3acd9f1668f27e874dbba92dfee97738b7d957c9be93977935` |
| `propuestas/PROPUESTA_HUMANA_4_12.md` | `83d3ee8a4a64115e6e5b407ea68a851995653dbf037b3e9bdc5db1e0a31c36ac` |
| `propuestas/propuesta_humana_4_12.json` | `52d4dc2ae7f5a5296c0063b1e5cf8d73fa7e5bebee363904e1f250434bb80f64` |
| `resultados/relevos_agentes_4_12.md` | `19be9e87b7d13965f7235250073e6ef768d3c1aa7906460c7a5c7da217cc46a8` |
| `resultados/dominios_variantes_4_12.md` | `66db773bed17b002a0270b3c597af3fe41c3a4e79992a4f9187e3ec3a9ceea39` |
| `resultados/diferencias_piloto_4_11_codigo_final.md` | `37483074445d722f7277dd1eae06254c649fd2b30ff1e11b0c5e5c385d9fdf72` |
| `viscofan/resultados/sensibilidad_derechos_de_uso.md` | `2790fcf4cb557317bafddb88eb2936582af86656673163ebb72dc4292a92dcc4` |
| `scripts/sensibilidad_derechos_de_uso_viscofan.py` | `237f3df1056cc23c4f070295a4cbb2be9a3eec286c9740ac42b8991bfdc8a324` |
| `scripts/dominios_variantes_4_12.py` | `a4345aaa9538892f6e54ea9a08df097587893a087627b635d1d02a3c798286d4` |
| `scripts/comprobar_entrega_4_12.py` | `66d7d68ef185a46857680f7c5cd8ac6f1e12ddf46db924cae102b3320c19ff5c` |
| `scripts/propuesta_humana_4_12.py` | `4b1ea4a460ae48dd503133abc29e70340bfa07873678fef0d2f9397feb905674` |
| `revision_interna/ENCARGO_REVISION_DE_LO_AFECTADO_4_12.md` | `89a444e30eef9329a9f5b043f24efa2439ec68efe55734a73e247dc02285da6d` |
| `revision_interna/REVISION_INTERNA_4_12.md` | `1ce66d157d83b5208f6d046928a76766f98d1c52461f5a8e6e29e6e88b0c2f3c` |
| `revision_interna/diferencias_desde_la_revision/codigo_scripts.diff` | `d808d924a9636d9afaa820190f1428ad9e5fb7e456e58fa4bb91c6ae8e5f63cf` |
| `revision_interna/diferencias_desde_la_revision/documentos_del_ensayo.diff` | `7dd1096584ae903666486562273bcd7684466b7bac8d82808143db1e6864e0cf` |
| `revision_interna/diferencias_desde_la_revision/documentos_generales.diff` | `d5d3375b3c1c88cf9f365295a4d0247d18145437d1917b8dc403840ea2e6cdc7` |
| `revision_interna/diferencias_desde_la_revision/pruebas.diff` | `993e5408318dc74a8098e2b5f9a685cb666e6828d8a44a0e815632e64889710e` |
| `revision_interna/diferencias_desde_la_revision/scripts_del_ensayo.diff` | `8556e69bafc252e6b8bb970155bb81d3eebf2686da4bf7c060943eeff64f9b7e` |
| `revision_interna/diferencias_desde_la_revision/verificar_paquete.diff` | `2a0287ce82d21154efea5eb6c6bad414bed416320eac7b89e8314e7375e86bd8` |

**Documentos generales, pruebas y código**

| Archivo | SHA-256 |
|---|---|
| `personaje_v2/ANEXO_D_salidas_y_formatos.md` | `0839e3f08df29584330d4520fe62c75aca8aaa1b8c1d5019c2afd4fd0466e50c` |
| `personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md` | `435c12e3fb55a434576c89d683d34a9db072e568a3829a1de4b4cd24f13b6db3` |
| `v6/v64_experimental/docs/README_V6.4_experimental.md` | `27c4935aef56cadad68038ba16975cbfe7e6b0bdd3cd09e33137a1e0acbd9b43` |
| `verificar_paquete.sh` | `2299e7c9bdfc5d5b96d3ac58e4cd8d3456d4d3b19f50f31e4fd63d61e34634fd` |
| `personaje_v2/pruebas/test_integracion_v64.py` | `6f4f7e65a296c21607ca39b977966417e73d89caadbc5cdf578ef84ec584c35c` |
| `personaje_v2/scripts/pipeline.py` | `99f0cd3c6dd4731e5ed23627922381620154d084f3b148de2cce6870ded89e2e` |
| `personaje_v2/scripts/entradas_economicas.py` | `470fb224844d19ab12f856d4d21420ea06efd670c21bffcc7b94e6387c0a6bb4` |
| `personaje_v2/scripts/trazabilidad_v64.py` | `b4f62ee801ac47f359b22918f0442087629369e7f11f0c575ac64a347aa21ab1` |
| `personaje_v2/scripts/objetivo_v64.py` | `ac983c86326825cfcea702360a244fd1d18c476ca7f1b2779c3593726b425dc3` |
| `personaje_v2/scripts/informe.py` | `a80c05d2e9013f610b02ca564f2ec66b49bc87814a6f5974399ed2c4be6563cb` |
| `personaje_v2/scripts/variantes_configuracion_v64.py` | `1d36dc7f97c48090a07df73e9833f0927dd2fe85f4ab11bce840470ad0379d6c` |
| `personaje_v2/scripts/ficha.py` | `d269982e9692d92d99fa59988b11ee330c3a082298d6ce1a67a25c108c35b84e` |
| `personaje_v2/scripts/resumen.py` | `c3057e5025fda7d4e5e001ce4e6e15b78345fc80d4fbe89cc80c8163df5a5dd5` |
| `personaje_v2/scripts/dominios_v64.py` | `cc561771bc9bc05fd190a525fc9daa54c0a8c2604b2314386142ea7bf49de942` |
| `personaje_v2/scripts/verify_quotes_v2.py` | `3083ca073b84a941e6abb14d742807f2acdeb7dca3df5060f70ec5ab096e3d66` |

**Expedientes** (16 primeros caracteres)

| Archivo | `cierre_condicionado/Vidrala` | `cierre_bloqueo/Vidrala` | `viscofan/experimental/Viscofan` |
|---|---|---|---|
| `ficha.json` | `9721497f624ada03…` | `18a385694556940a…` | `508033a34d2df3de…` |
| `informe.md` | `e576b5ed9c87af48…` | `da9e8fdb81dba185…` | `160018948c9573d5…` |
| `auditoria.md` | `91433a352826693e…` | `e8ae995119dd36ce…` | `262c2ea7b5eaafb3…` |
| `material_auditoria.json` | `51bfa223f3f5de61…` | `fa60f9cd4dea5003…` | `e34d2cd4e573c365…` |
| `solicitud_auditoria.json` | `73c2188922270368…` | `f2d924b4341e73f7…` | `f0026d6bf2c733d1…` |
| `cierre_vigente.json` | `27137b6ba846189a…` | `2c0e6e7cb241cac6…` | `f36d58c1a739cd9e…` |
| `cadena_trazabilidad.json` | `e06d07bcd860a9ca…` | `96862e18bd362f72…` | `650bcc13f0b04ea7…` |
| `verificacion_trazabilidad.txt` | `e70fca6729f3b32b…` | `e70fca6729f3b32b…` | `b031a56b2d23e565…` |
| `fase_c.json` | `4332ba9b3b2e1939…` | `91a6f0d4cda6dd56…` | `5986b127f2637d1d…` |
| `precio.json` | `ff1438f5cdf48ee4…` | `ff1438f5cdf48ee4…` | `46446a661f0c6d4b…` |
| `resultados.json` | `cf4bdda2313cd47d…` | `18f5ca026df8c982…` | `3c53ddff6f11d490…` |
| `configuracion_economica.json` | `bd092502a40cf27b…` | `2abd044a21b9863d…` | `73a9f23dc963b36a…` |
| `configuracion_v64_variantes.json` | `dab33cb4fbccb143…` | `dab33cb4fbccb143…` | `55d9dbb2c7faf112…` |
| `<empresa>_v63_evaluada.xlsx` | `0f87bdc9c2817a49…` | `0a6e41800078f1f5…` | `33cf616b3ac6d571…` |

Las huellas completas de `ficha.json`, `informe.md` y `auditoria.md` son las que registra el `cierre_vigente.json` de cada expediente, comprobadas contra los archivos.
