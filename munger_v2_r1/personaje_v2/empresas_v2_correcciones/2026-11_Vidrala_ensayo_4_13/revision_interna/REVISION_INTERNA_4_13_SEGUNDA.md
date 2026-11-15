# Segunda revisión interna · entrega 4.13 (lo afectado por las correcciones de R1–R18)

**Qué es.** Revisión **interna** de Claude, hecha por un agente en contexto separado que no participó en el trabajo. **No es la revisión externa ni la sustituye.** Objeto: lo que cambió después de la primera revisión interna, en `/home/claude/trabajo_4_13/munger_v2_r1`, tal como estaba el 13-nov-2026 entre las 16:23 y las 16:45.

**Cómo se hizo.**
- Solo lectura del árbol. La única escritura en él es este informe.
- Las pruebas se ejecutaron sobre una copia parcial del árbol (sin `pruebas/_v64`, sin las entregas 4.5–4.12) en `/tmp/claude-0/-home-claude/d8a381ee-40a6-50ca-8023-33d75d699d51/scratchpad/revision_interna_4_13_segunda/` (`arbol/`), con `python3 -B` y `soffice` sustituido por un ejecutable que falla. No se lanzó LibreOffice ni el pipeline sobre los expedientes reales.
- Los cambios de código se leyeron como diferencia frente a la copia que dejó la primera revisión (estado de las 14:27).
- Scripts del revisor, en esa carpeta: `scripts/fuzz2.py`, `scripts/idem.py`, `scripts/sonda_r4.py` y, reutilizados de la primera revisión, `scripts/caso_no_entregable.py` y `scripts/copia_exp.py`. Salidas en `out/`.

**Límites de esta revisión (hechos).**
- No se recalculó ningún libro. Las cifras se contrastaron entre archivos y con aritmética.
- De la batería solo se ejecutó el grupo E (42 de 42 con el código actual). `grupo_f_revision_413` y las tres pruebas nuevas del grupo H no se ejecutaron (la parte sintética necesita LibreOffice); se leyó su código y el caso R3 se reprodujo aparte, con el recorrido completo.
- No se contrastó nada con BORME ni CNMV (sin internet).
- Mientras se revisaba, la orquestación siguió escribiendo en el árbol (`INFORME_INTEGRACION_4_13.md`, dos scripts nuevos, `pruebas/_v64`). Esos archivos no son objeto de esta revisión; del informe integrado solo se miró lo que afirma sobre R1–R18.

## Resumen por gravedad

| Gravedad | Nº | Hallazgos |
|---|---|---|
| Bloqueante | 0 | — |
| Importante | 1 | S1 |
| Menor | 8 | S2, S3, S4, S5, S6, S7, S8, S9 |
| Observación | 5 | S10, S11, S12, S13, S14 |

| Id | Gravedad | Título |
|---|---|---|
| S1 | Importante | `comprobar_entrega_4_13.py` dará NO CUMPLE en la evidencia activa de Viscofan: la nota nueva de C42 cita «6-oct-2026» y «2.444,4» como antecedente |
| S2 | Menor | `comprobar_entrega_4_13.py`: varias comprobaciones pasarían aunque el hecho fuera falso, y el control deja `__pycache__` en el árbol |
| S3 | Menor | R4: el juicio sobre el objetivo no tiene campo propio; con «juicio_economico» y una inferencia cualquiera, la coherencia acepta un objetivo emitido sin condición |
| S4 | Menor | R6: el S2C NORMAL de Viscofan no cambió (1,1 antes y después); queda un límite de la ficha que ya no es exacto |
| S5 | Menor | Viscofan, Control maestro: la lista de D88 no declara C97, y quedan dos textos heredados que contradicen E88 |
| S6 | Menor | Las tres retiradas previas a rehacer llevan el motivo «no hay auditoria.md», no el cambio de material, y el archivo no guarda la auditoría |
| S7 | Menor | Propuesta: cifras escritas a mano en el script, una alternativa con la redacción invertida y una estimación atribuida a las dos fases C |
| S8 | Menor | Guía: la frase sobre los archivos de control es más fuerte que el código |
| S9 | Menor | Pruebas nuevas: la de R3 solo cubre la ficha provisional y la de R6 solo comprueba etiquetas |
| S10 | Observación | El cambio mayor del objetivo de Viscofan (+1,54 €) viene de repetir las fases A y B con agentes nuevos, no de las correcciones |
| S11 | Observación | N1: el agente de bloqueo marca «calculada» una materialidad que razona con un criterio propio de 1,5 € |
| S12 | Observación | Las dos aprobaciones apartadas no constan en `auditorias_conocidas.json` (no son reutilizables por otra vía) |
| S13 | Observación | Corte a media frase de `causa_si_no_concluido.detalle`: no hacía falta corregirlo antes de cerrar |
| S14 | Observación | Redacción del registro y script de corrección no repetible |

---

## S1 · El control de la entrega fallará en la evidencia activa de Viscofan (importante)

**Hechos comprobados.**
- `scripts/comprobar_entrega_4_13.py`, sección 6: busca en las filas del Control maestro de C37, C41, C42, C55, C57, D4 y «Periodos» los textos `TEXTOS_RETIRADOS = ("6-oct-2026", "53,60 × 45,6036", "2.444,4", "Cierre 6-oct-2026")`.
- La evidencia nueva de C42 (`fase1_v63.json → analisis.C42.nota`, que `rellenar_fase1_v63.py` escribe en la fila 42) dice: «(4.13) Sustituye al 9,9 de la etapa 1 (EV a 6-oct-2026 con capitalización 2.444,4, deuda a 30-jun-2026 y EBITDA de los doce meses a jun-2026)…».
- Ejecutado el control sobre la copia del revisor (libro `Viscofan_v63_datos.xlsx` idéntico al del árbol): «NO CUMPLE · evidencia activa de C37, C41, C42, C55, C57, D4 y la lista de períodos sin los textos de la etapa 1 que contradicen las entradas · ['Etapa 3 | Análisis!C42 | EV / EBITDA…']». Salida en `out/comprobar_entrega_copia.txt`.

**Cómo se reproduce.** Desde una copia del árbol: `python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/scripts/comprobar_entrega_4_13.py`.

**Consecuencia.** La nota es legítima: nombra el dato sustituido como antecedente, no como evidencia. Pero el control, tal como está, no puede dar «todas cumplen» con el expediente cerrado. Las dos salidas fáciles son malas: cambiar la nota cambia el libro (material auditado: retira la aprobación), y quitar los textos de la lista deja la comprobación sin contenido.

**Qué haría falta.** Ajustar la comprobación, no el libro: buscar los textos retirados en las columnas de período, fuente y literal (G:M) y admitirlos en la nota (N) solo cuando van detrás de «Sustituye a»; o comprobar por separado que la fila 42 dice «3-nov-2026» y «31-dic-2025» en su período. Decirlo en el registro.

## S2 · Comprobaciones del control que pasarían con el hecho falso (menor)

**Hechos comprobados** (lectura de `scripts/comprobar_entrega_4_13.py`; los hechos que afirma son hoy ciertos, ver «Qué está bien»).
- «auditoría ligada a su solicitud y a su material»: solo exige que `auditoria.md` tenga una línea «Material auditado: …» y otra «Solicitud de auditoría: …», con cualquier identificador. No los compara con `solicitud_auditoria.json` ni con `material_auditoria.json`.
- «no se reutiliza una aprobación»: solo exige que los tres `auditoria.md` sean distintos entre sí y que exista la carpeta `antecedentes/`. No compara la huella de la auditoría vigente con las apartadas ni con las del historial.
- Ninguna comprobación llama a `cierre_v2.motivo_vigencia`. La vigencia se deduce del estado y de las huellas del material; no cubre `ficha.json`, `informe.md` ni `cierre_vigente.json`.
- «réplica independiente» está etiquetada «reejecuta», pero lee `replica_independiente.json`. Ese JSON no guarda la huella del libro final (`plantilla_sha256: null`), así que una réplica de un libro anterior pasaría.
- Las secciones 3, 4 y 5 leen registros de texto (`bateria_completa_4_13.txt`, `sonda_tipos_4_13.txt`, `sonda_salto_4_13.txt`) sin atarlos al código final (ni huella ni fecha): un registro anterior a una edición pasaría.
- «sin `__pycache__` en el árbol»: se comprueba en la sección 1, antes de que el propio control importe `comparar_zip`, `configuracion_economica`, `objetivo_v64` y `entradas_economicas`. La orden documentada (`python3 -I`, sin `-B`) crea `personaje_v2/scripts/__pycache__` después de haber comprobado que no existe. «Escribe solo en temporales» no es cierto con esa orden.
- Hoy hay cuatro `__pycache__` en el árbol (`find … -name __pycache__`: `v6/scripts`, `v6/v64_experimental/scripts`, `v6/v641_experimental/scripts`, `personaje_v2/scripts`).
- «revisión interna presente» solo mira la primera (`R1` y `R18`); no mira este informe.
- La propuesta se comprueba por su estructura; sus cifras no se contrastan con las salidas.

**Consecuencia.** El resultado «N de N cumplen» diría menos de lo que parece en esos puntos. No se ha encontrado ningún hecho falso detrás.

**Qué haría falta.** Comparar los identificadores de la auditoría con los de la solicitud y el material; añadir `motivo_vigencia` a los tres expedientes; comparar la huella de la auditoría vigente con las de `antecedentes/`; ejecutar el control con `-B` (o `PYTHONDONTWRITEBYTECODE=1`) y mover la comprobación de `__pycache__` al final; anotar en los registros de las sondas la huella de los scripts con que se ejecutaron; cambiar la etiqueta de la réplica a «constata».

## S3 · R4: el juicio sobre el objetivo no tiene campo propio (menor)

**Hechos comprobados.**
- `pipeline.py`, `_coherencia_cobertura_413`: para `base_de_la_materialidad_objetivo = "juicio_economico"` solo se exige que `inferencias` no esté vacía. `evidencia`, `hechos` e `inferencias` son las mismas listas que usa el juicio sobre la acción. `informe.py` imprime la misma evidencia y las mismas inferencias bajo los dos juicios.
- Sonda (`scripts/sonda_r4.py`, copia de `vidrala_condicionado`): poner `material_para_objetivo = false` con base «juicio_economico» en los cuatro parámetros sin fundamento suficiente (PM1.estructura tiene contrastes de −0,50 a +7,10 €) → `objetivo_v64.evaluar` da `objetivo_emitido` y `coherencia_fase_c` **acepta**. Con base «calculada» se rechaza («estos contrastes mueven el precio de Sí al redondeo declarado»). Con `null` y «no_determinada», los cuatro condicionan el objetivo.
- Caso real: PM1.roic_terminal, sin fundamento suficiente, mueve el precio de Sí +1,06 € (Vidrala) y +0,58 € (Viscofan) y queda fuera de los condicionantes por juicio en los tres expedientes. Las auditorías lo anotan como aviso.

**Interpretación.** La corrección hace lo que pedía R4: «no determinada» existe, condiciona, y «no material calculada» se contrasta. Lo que queda es inherente a no tener umbral: que un objetivo salga condicionado o emitido depende de un juicio declarado, y el contrato mecánico solo exige que esté declarado. La propuesta lo recoge (D413-FUNDAMENTO).

**Consecuencia.** «R4 resuelto» en el informe integrado es exacto para el contrato, no para la dependencia del juicio. La única barrera frente a un juicio vacío es la auditoría.

**Qué haría falta.** Decirlo así en el informe integrado. Si se quiere reforzar sin umbral: un campo propio para la evidencia y la inferencia del juicio sobre el objetivo, y exigir que cite los contrastes que mueven el precio de Sí cuando los hay.

## S4 · R6: el S2C NORMAL de Viscofan no cambió (menor)

**Hechos comprobados.**
- `viscofan/Viscofan/referencias_mecanicas.json`: ancla B155 = 1,05996 (antes C53 = 1,14616). Referencias: 0,8 / 1,1 / 1,3 (antes 0,9 / 1,1 / 1,4). El redondeo a un decimal deja el NORMAL en 1,1 con las dos anclas.
- `fase_b.json` (nueva) lo dice: «los dos redondean a 1,1, así que la cifra no depende del perímetro». Palancas S2C: 0,8 / 1,1 / 1,3.
- El S2C NORMAL que entra en S2C × f sigue un 3,8 % por encima del histórico con el perímetro NIIF 16 (1,1 ÷ 1,06). En la primera revisión, R6 estimó «en torno a un 8 %» comparando las anclas; con la palanca redondeada era ya un 3,8 %.
- `ficha.py:292` sigue escribiendo el límite «G7 de la gramática y las referencias mecánicas usan las bases heredadas (tipo de la Historia y S2C sin f)». En Viscofan la referencia del S2C usa ahora una celda de la V6.4.1 (B155), que no es una base heredada. El texto está en la ficha y en el informe aprobados.
- El informe integrado dice «R6 resuelto (S2C anclado en B155; fase B de Viscofan rehecha)».

**Consecuencia.** La corrección cambia el ancla y las referencias del MALO y del BUENO; no cambia el escenario NORMAL. La mezcla de perímetros que señalaba R6 queda resuelta en el ancla y absorbida por el redondeo en la cifra. No afecta a ningún estado.

**Qué haría falta.** Decir en el informe integrado que el NORMAL no cambió y por qué. Corregir el texto del límite en una entrega posterior (cambia la ficha: retira aprobaciones si se hace ahora).

## S5 · Viscofan, Control maestro: lo declarado en D88 y dos textos heredados (menor)

**Hechos comprobados** (`Viscofan_v63_evaluada.xlsx` y `Viscofan_v63_datos.xlsx`, hoja «Control maestro», openpyxl, `data_only=True`).
- Las ocho celdas que declara D88 conservan de verdad datos de 2026: C24 (LTM jun-26), C31 (30-jun-2026), C33 (deuda 30-jun-2026, EBITDA LTM), C34 (30-jun-2026), C40 (LTM jun-26), C53 y C54 (30-jun-2026) y C38 (referencia externa del 28-sep-2026).
- Falta una: la fila 76 (Análisis!C97, operaciones de directivos) tiene período «7-oct-2025 a 7-oct-2026». No es una celda de contraste: la fase A nueva la usa para «Comprando».
- Fila 5 (cabecera): «Periodo usado en medias DCF | Pendiente de inversor: 5a (2021–25) / 3a (2023–25) / LTM jun-26». E88 dice que el inversor lo fijó el 23-oct-2026 (2023–2025).
- E100: «C48 informado cuando se fije periodo», con el período ya fijado.
- C42: 2.487,7 + 304,075 + 12,243 − 62,790 + 5,422 = 2.746,65; ÷ (204,794 + 85,196 = 289,990) = 9,4715 → 9,47. Correcto. El texto dice «EV 2746.6» por el formato de 2.746,65.
- No queda «6-oct-2026», «53,60 × 45,6036» ni «45,60 a 30-jun-2026» como evidencia de C37, C41, C55 o C57. `fase1_v63.json` y `fase1_metadatos.json` coinciden con el libro.

**Consecuencia.** La declaración de D88 es correcta pero no completa. Los dos textos heredados no afectan a ninguna cifra. Cambiar el libro retira la aprobación.

**Qué haría falta.** Declararlo en el informe integrado como evidencia heredada no actualizada, o corregirlo en la próxima regeneración (`control_maestro_textos` ya lo permite para E100; la fila 5 no entra en C86:E102).

## S6 · Motivo de las retiradas previas a rehacer (menor)

**Hechos comprobados.**
- `corregir_viscofan_revision_4_13.py` y `apartar_para_rehacer_4_13.py` copian `auditoria.md` a `antecedentes/` y la borran del expediente **antes** de la primera llamada al pipeline.
- `viscofan/Viscofan/historial_cierres/01_c76627e1181d2041/RETIRADA.json`: «motivo: no hay auditoria.md»; «en el momento de la retirada no había auditoria.md en el expediente». Lo mismo en el historial del estado de los dos expedientes de Vidrala (`05_795e4ff5…` y `05_8a3db1f6…`: «no hay auditoria.md»).
- Esos tres archivos del historial no contienen `auditoria_en_el_momento_de_la_retirada.md`. Las auditorías están en `antecedentes/ejecucion_1_4_13/auditoria.md`, con su SHA-256 en `resultados/apartado_*.json` y en `correccion_revision_4_13.json`, y constan en `auditorias_conocidas.json`.
- La retirada de la marca de consumo de la extracción (`consumidos["extracto_v63.md"]`) está registrada en `correccion_revision_4_13.json` y `.md` y en el registro de avance. No consta en `estado_pipeline.json → historial`.

**Interpretación.** No oculta nada: la aprobación se retiró, la auditoría se conserva y el motivo real está en el registro de avance. La extracción reutilizada tiene los mismos bytes que la de la 4.12 (`2c526eac…`) y no cita C42, la lista de períodos, D4 ni la configuración (`grep` en `extracto_v63.md`): reutilizarla está justificado. Quitar la marca es una edición manual del estado, declarada.

**Consecuencia.** Quien lea solo `historial_cierres/` verá un motivo que no es la causa (el material cambió por las correcciones) y no encontrará allí la auditoría. El registro dice «aprobación retirada y archivada», que es cierto.

**Qué haría falta.** Una frase en el informe integrado. En adelante, apartar la auditoría después de la primera llamada al pipeline, para que el archivo la guarde y el motivo sea el del material.

## S7 · Propuesta: cifras a mano, una redacción invertida y una atribución (menor)

**Hechos comprobados.**
- Estructura: 13 decisiones (4 + 5 + 4), cada una con pregunta, recomendación, alternativas, evidencia, efectos y «si no se adopta»; `decision`, `fecha` y `decidido_por` son `null` en las trece. Ninguna recomendación adopta nada ni elige una cifra por su valor; el 1,5 € y el 1,25 aparecen solo como alternativas con su origen.
- Las cifras de efecto coinciden con las salidas: Vidrala 56,02; 51,29–65,72; heredado 64,75; H 61,37; SR2 57,08; SRF 58,43; S 55,52. Viscofan 40,164; «Caja» 40,826; extremos de θ con «Caja» 41,862 y 39,791; acciones 40,008 / 39,715 / 40,054; rango 38,47–43,39; heredado 43,39. Cotas: 1 + 81,084 ÷ 403,132 = 1,2011; Vidrala 1 + 251,2 ÷ 500 = 1,50.
- `propuesta_humana_4_13.py` lee de los expedientes los precios de Sí y los rangos, pero lleva escritas a mano: +1,75; +1,06; 1,5 €; 1,2011; 1,1413; 1,50; 24,110; 27,051; 64,923; 40,813; 22,66 %; 19,83 %; +1,57; −0,55; +0,8; «del orden de 1 €». El registro dice «cifras leídas de los expedientes».
- VISCOFAN-CONFIG, alternativas: «N1 con los ajustes de ejercicios anteriores (22,66 %)». La configuración dice lo contrario: «Sin además los ajustes de ejercicios anteriores sería 22,66 %».
- VIDRALA-PERIMETRO: «lo estima la fase C (≈ −0,55 €…) y el del margen (≈ +0,8 €)», con evidencia en las dos fases C. Las dos cifras están solo en `vidrala_bloqueo/Vidrala/fase_c.json`.
- Las referencias a `INFORME_INTEGRACION_4_13.md` §9, §10 y §11 existen ya (el informe se escribió durante esta revisión).

**Qué haría falta.** Corregir la redacción de 22,66 % y la atribución de −0,55 / +0,8; leer del material las cifras que se puedan o decir en el script cuáles son literales.

## S8 · Guía: archivos de control (menor)

**Hechos comprobados.**
- `GUIA_RECORRIDO_SUPERVISADO.md`: «Cualquier cambio del material auditado […], también un archivo de entrada o de control con una estructura JSON incorrecta (nulo, lista, escalar o campo anidado de otro tipo), retira la aprobación en la primera llamada».
- `scripts/fuzz2.py` (112 primeras llamadas, material intacto o cambiado): con `estado_pipeline.json → intentos = []`, con `auditorias_conocidas.json → sha256 = "x"` y con una huella de `material_auditoria.json → archivos` cambiada a lista, pipeline, informe y resumen **conservan** la aprobación (el material no cambió y el identificador coincide). Sin excepción en ningún caso.
- El resto de la guía coincide con el código: código 6 con el estado ilegible (visto: `rc 6`), código 5 con la retirada pendiente, las dos configuraciones, `control_maestro_textos` limitado a C86:E102, y el contrato de cobertura.

**Consecuencia.** La frase vale para el material y para los campos que deciden la vigencia, no para cualquier campo de un archivo de control. El comportamiento es correcto; la frase es más fuerte.

**Qué haría falta.** «…o un campo de control del que depende la vigencia…».

## S9 · Alcance de las pruebas nuevas (menor)

**Hechos comprobados** (`pruebas/test_integracion_v64.py`).
- `grupo_e_revision_413` (R1 y R2): prueba lo que dice. Ejecutado por el revisor: 14 de 14; grupo E completo, 42 de 42 (`out/grupo_E.log`).
- `grupo_f_revision_413`, R3: solo llama a `ficha.py --estado no_entregable --provisional`. No prueba la ficha oficial, el esquema, `informe.py`, `resumen.py` ni `Pipeline.terminar`. El revisor reprodujo el recorrido completo en copias de los tres expedientes (`caso_no_entregable.py`): ficha válida, informe y fila escritos, `estado_del_objetivo = no_emitido_estado_final`, `resumen_pendiente = False`. Funciona; la prueba no lo cubre.
- Grupo H, R6: comprueba que la regla y las anclas nombran B155; no comprueba el valor de la referencia. R12 y R17: prueban lo que dicen.
- `pruebas/_v64/resultados_integracion_v64.json` (15:09) solo contiene el grupo H (19 de 19). No hay registro guardado de E ni de F con el código final; el registro los deja para la ronda final.

**Qué haría falta.** Añadir a la prueba de R3 la terminación completa; a la de R6, el valor (NORMAL = B155 redondeado). Guardar la ronda final con su fecha.

## S10 · De dónde viene el cambio del objetivo de Viscofan (observación)

**Hechos.** `comparacion_4_12_4_13.md`: 39,2877 → 40,8263 (+1,5386, fases A y B nuevas, con «Caja») → 40,1640 (−0,6623, perímetro NIIF 16). Las sumas cuadran con `configuracion_v64_variantes.json` (`perimetro_alternativo` = 40,8263). Entre la fase B de la 4.12 y la nueva cambian: crecimiento del MALO (1,0 % → 1,5 %), S2C del MALO y del BUENO (0,9 → 0,8; 1,4 → 1,3) y las probabilidades (25/60/15 → 20/60/20). En la fase A cambian C97, C27, Palancas!C5 y las frases de los escenarios.

**Interpretación.** De esos cambios, solo el S2C del MALO y del BUENO sale de una corrección (R6). El resto es el juicio de un agente nuevo ante casi las mismas entradas. Ese efecto (+1,54 €) es mayor que el del perímetro (0,66 €) y que la línea de materialidad que usa un agente (1,5 € en Vidrala). El «rango calculado» no lo recoge. La descomposición depende del orden (con las palancas antiguas el perímetro valía −0,6715) y el documento lo declara.

## S11 · N1 y la etiqueta «calculada» (observación)

**Hechos.** Con el mismo material, `vidrala_condicionado` declara N1.tipo no material para el objetivo, base «juicio_economico» (+1,75 €, «es juicio»); `vidrala_bloqueo` lo declara material, base «calculada», y lo razona con «mi criterio de 1,5 € (juicio mío, no un umbral adoptado)». N1.tipo tiene fundamento suficiente en los dos: no condiciona ninguno. Las fichas lo reflejan (`materiales_para_el_objetivo` con y sin N1.tipo) y la propuesta lo recoge en D413-FUNDAMENTO.

**Interpretación.** El sistema lo representa como juicio declarado y sin umbral. El contrato admite «true calculada» siempre que haya contraste, así que la etiqueta de bloqueo es válida, pero «calculada» significa ahí «un contraste lo mueve», no «el cálculo dice que es material». Conviene decirlo en la guía.

## S12 · Aprobaciones apartadas (observación)

**Hechos.** Las dos aprobaciones de material anterior (`antecedentes/auditoria_material_f2fe5abba7dcd698/` y `…_9725b95f43a36cc8/`) no están en `auditorias_conocidas.json` (el pipeline nunca las consumió). Responden a solicitudes sustituidas (SA-5f070ad666596e5f y SA-ef4407f16aae3f08) y a un material que solo difiere en `informe_provisional.md`. Las auditorías vigentes son otras (huellas `45c308b8…` y `8a3b986b…`), nombran la solicitud y el material vigentes y coinciden con `cierre_vigente.json`. No queda ninguna aprobación antigua vigente ni reutilizada.

## S13 · Avisos de las auditorías no corregidos (observación)

**Hechos.** `ficha.json → causa_si_no_concluido.detalle` de `vidrala_bloqueo` tiene 500 caracteres exactos y termina en «La acción se sostiene en» (`pipeline.py:887`, `[:500]`); `diagnostico.md` repite el corte. El texto completo está en `ficha.objetivo.motivo` y en la sección 14 del informe. El corte no cambia el sentido: lo que precede ya dice «objetivo bloqueado».

**Interpretación.** Ninguno de los avisos declarados debía corregirse antes de cerrar. Este conviene arreglarlo después (cortar en un límite de frase o marcar «…»), porque cambia la ficha.

## S14 · Redacción del registro y script de corrección (observación)

**Hechos.**
- `REGISTRO_AVANCE_4_13.md`: «R2 (registro de auditorías con entradas mal formadas)». R2 trata del registro de **publicaciones** del resumen y de los campos del estado. El informe integrado lo dice bien.
- `corregir_viscofan_revision_4_13.py` no se puede volver a ejecutar sobre el expediente actual (sus `assert` buscan el texto anterior) y lleva escrito 54,70 × 45,479209. Es un script de un solo uso; su resultado está registrado.
- La fase C de Viscofan cita como evidencia `CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md §1`, que está fuera del expediente (mismo tipo de aviso que las auditorías anotaron en Vidrala).

---

## Respuestas breves a los puntos de atención

1. **Código de R1–R18.** Cada corrección resuelve su hallazgo y no se ha encontrado ninguna que abra otro. R1 y R2: sin excepciones y sin aprobación superviviente en 112 primeras llamadas nuevas con tipos anidados. R3: recorrido completo correcto. R4: ver S3. R6: ver S4. R12 y R17: correctos. Afirmaciones más fuertes que el código: «R6 resuelto» y «R4 resuelto» sin matiz (S3, S4) y la frase de la guía (S8).
2. **Informe tras las auditorías.** Las correcciones de las secciones 7 y 14 son correctas en los tres informes. No se ha encontrado otro «ninguna», «0» o «no material» que contradiga el material: «materiales para la acción ninguno (no determinada: ninguno)» es lo que dice cada fase C, y PM1.familia de Viscofan aparece como no determinada y como condicionante. Avisos sin corregir: S13.
3. **Viscofan.** C42 correcto. Reutilización de la extracción justificada; la retirada de la marca está registrada (S6). No queda evidencia activa que contradiga las entradas en las filas frescas; quedan los restos de S5. Conciliación, alternativas y comparación: cifras y descomposición correctas (S10).
4. **Vidrala.** Estados y auditorías acordes al material vigente; ninguna aprobación antigua vigente (S12). N1 está representado como juicio declarado y recogido en la propuesta (S11).
5. **Propuesta, guía y control.** Propuesta correcta en estructura y cifras, con los detalles de S7. Guía: S8. Control: S1 y S2.

## Qué está bien (solo lo comprobado)

- **Guardas (R1, R2).** Grupo E con el código actual: 42 de 42. `fuzz2.py`: 28 alteraciones de tipos anidados en `ficha.json`, `cierre_vigente.json`, `material_auditoria.json`, `estado_pipeline.json`, `acreditacion_libro.json`, `auditorias_conocidas.json` y el registro de publicaciones × 4 vías = 112 primeras llamadas, 0 excepciones. En los 44 casos con el material cambiado, el estado deja de ser concluido · APROBADO en todos; la fila deja de decir APROBADO salvo cuando la entrada del registro apunta a otra ruta, y ahí queda «RETIRADA PENDIENTE» con código 5.
- **R3.** Terminación en `no_entregable` después de la fase C, en copias de los tres expedientes: ficha válida, informe, fila y `no_emitido_estado_final`.
- **Expedientes finales.** En los tres: `motivo_vigencia` no da motivo; las 24 huellas del material coinciden con los archivos; `auditoria.md`, `ficha.json` e `informe.md` tienen las huellas de `cierre_vigente.json`; la auditoría nombra la solicitud y el material vigentes. Estados: `vidrala_condicionado` concluido · APROBADO (1beff82a21fffcd6), `vidrala_bloqueo` pendiente_de_datos · APROBADO (86e66e0a6876aba2), `viscofan` concluido · APROBADO (ea1e6fb9f9173a1c). En copias aisladas, `ficha.py`, `informe.py` y `resumen.py` a mano dejan iguales la ficha, el informe, el estado y el CSV.
- **R8.** Las tres fichas declaran la aptitud de la 4.13 y citan un informe que ya existe con ese apartado.
- **R5.** `naturaleza` de Viscofan con 64,923 y 1,2011; misma huella económica (`75726ca4…`).
- **R7.** C42 = 9,47 con su aritmética; D4 con su período; D88 y E88 con las fechas de las entradas; la conciliación atribuye la N a la fase 1 del pipeline V2 y cita el antecedente de la etapa 1.
- **R10.** Alternativas sobre el libro vigente: 40,16401 reproducido; las otras cifras cuadran con 40,164 × 45,479209 ÷ N y E = 54,70 × N; −1,12 % con E fijo y −1,25 % con E recalculado.
- **R11.** Las frases de altas están en las líneas 2374 (`AR_2025.txt`) y 2318 (`CF_2021.txt`), como dice ahora el documento.
- **R17.** `factor_de_reestimacion` sale «en la activa» en las variantes de los tres expedientes y en la sección 14 de los tres informes.
- **Comparación 4.12 → 4.13.** Vidrala: misma valoración (56,018 y 60,697). Viscofan: 39,2877 + 1,5386 − 0,6623 = 40,1640.
- **Propuesta.** Trece decisiones en tres grupos, firmas vacías, cifras de efecto iguales a las de las salidas.
