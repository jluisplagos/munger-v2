# Incidencias de la 4.14 (hito 2)

Hechos, con causa y corrección. Las interpretaciones van marcadas.

## I1 · El comprobador de entradas daba por comprobada una hipótesis con la comprobación pendiente (14-nov, ≈14:55)

- **Hecho.** En el expediente `viscofan_decisiones/Viscofan`, la entrada `Palancas!C47` (hipótesis material, valor «Ninguna») tenía `comprobacion.resultado = "pendiente"`. El motivo: su fundamento lo había sustituido la orquestación por el texto que el revisor propuso en su discrepancia, a la espera de su confirmación. Pese a ello, `verificacion_entradas.py` daba «apto por entradas: True» con «pendientes 0». El pipeline registró ese apto en el paso 12 y emitió la solicitud de auditoría SA-67e5e062d6f94ad2.
- **Causa.** Para las hipótesis y convenciones solo contaba la «discrepancia» (corrección anterior del mismo día). Un «pendiente» explícito no se trataba, y la lista de materiales sin comprobar las excluía por clase.
- **Corrección.**
  - Una hipótesis o convención con el resultado «pendiente» queda pendiente. Si además es material, bloquea el apto.
  - Prueba nueva en `pruebas/test_verificacion_entradas_414.py`; la batería pasa 33/33.
  - Efecto en los registros vigentes: Viscofan decisiones pasa a NO apto (una entrada material sin comprobar). Vidrala decisiones sigue apto. Ningún otro registro de Viscofan o Vidrala tenía hipótesis pendientes. Elis está en revisión.
- **Consecuencia operativa.**
  - Se detuvo el agente auditor de SA-67e5e062d6f94ad2 antes de que escribiera nada. El registro forma parte del material auditado, así que su confirmación cambiará el material y la auditoría habría quedado sin valor.
  - Se pidió la confirmación de C47 a un revisor independiente. Después se rehará el paso 12 y se emitirá una solicitud de auditoría nueva.
- **Interpretación.** Es una puerta de la que depende la aptitud con dinero real. El fallo no cambió ningún precio, pero habría dejado auditar un registro incompleto como si estuviera completo.

## I2 · Los registros de las ramas no son aptos (hecho conocido, declarado aquí)

- **Hecho.** Ninguna rama alcanzó el apto en su paso 12:
  - `viscofan/Viscofan`: C55 y las medias C47–C50 con discrepancia.
  - `vidrala/Vidrala`: C46/C47 redondeados, C48 no evaluable, J14/K14.
- **Qué se hizo.** Esas discrepancias son las que originaron las decisiones E1–E4 y D3, que se aplicaron en expedientes nuevos (`*_decisiones`).
- **Estado.** Las ramas se conservan sin cambios, como expediente anterior, y no se auditan: las sustituyen los expedientes de decisiones.

## I3 · Vidrala decisiones v1 perdió entradas del análisis (14-nov)

- **Hecho.** El primer `CAMBIO` de Vidrala decisiones perdió estas entradas del análisis: C24, C31, C34, C42, C49 (4,5 → 6,764), C53 y C54.
- **Qué se hizo.**
  - El expediente se invalidó y se conserva como evidencia: `vidrala_decisiones_INVALIDO_perdio_analisis`.
  - Se rehízo fusionando el análisis del origen.
  - `cambiar_base.py` tiene ahora un guardián que detiene la preparación ante cualquier entrada del análisis no declarada; está probado en el grupo D, 8/8.

## I4 · Errores propios en los informes de efectos (14-nov)

- **Hecho.** Los informes de efectos de D3 y de E2/E3 daban los deltas frente a la 4.13 y no frente a la rama.
  - D3: lo detectó la persona responsable («40,30 € pasarían aproximadamente a 39,85 €, no a 39,99 €»).
  - E2/E3: lo detectó el agente de la fase C.
- **Corrección.** Están corregidos en el documento y en los mensajes. El script de efectos da ahora las dos bases.

## I5 · Re-extracción de Viscofan frente al encargo

- **Hecho.** La Historia de Viscofan citaba ediciones de los informes que no estaban conservadas. Se re-extrajeron 9 años desde ediciones conservadas.
- **Resultado.** Solo cambiaron 16 celdas, todas confirmadas por el revisor.
- **Conflicto declarado.** Esto contradice la regla «No se reextraerán diez años de datos». Se eligió así porque, sin fuente conservada, la verificación completa de las entradas (requisito obligatorio) no era posible.

## I6 · Nota añadida a una fuente de mercado de Elis

- **Hecho.** Se añadió una nota al txt de Euronext de Elis. Eso cambió su SHA mientras el registro lo citaba.
- **Corrección.**
  - Se restauró el original (SHA 257d6668…).
  - La nota vive ahora en un archivo NOTA aparte.

## I7 · Texto desfasado en la configuración de Viscofan (auditoría SA-5560fe3438e5febb, REPETIR)

- **Hecho.** `configuracion_economica.json` → naturaleza conservaba «N sigue en 45,479209 (VISCOFAN-ACCIONES)» después de D3. La ficha y la sección 14 del informe lo copiaban.
- **Corrección.**
  - La orquestación hizo un cambio editorial. La huella económica de la configuración es la misma (la recalculó el auditor) y no se rehízo ningún cálculo.
  - La fase C hizo la corrección 1.
  - La segunda auditoría dio APROBADO.
- **Prevención.** `textos_prohibidos` del CAMBIO solo revisa la evidencia activa y las notas, no la configuración. *Propuesta:* incluir la naturaleza de la configuración en la búsqueda de restos.

## I8 · Celdas fuera del universo de la verificación de entradas

- **Hecho.** Análisis!C42 (EV/EBITDA) no está en el universo de `verificacion_entradas` porque no alimenta la valoración. En Viscofan quedó con la capitalización anterior y solo lo detectó la auditoría.
- **Interpretación.** El requisito obligatorio cubre las entradas de la valoración. Las celdas descriptivas que usa el juicio, como C42, C33 o C34, no las contrasta el comprobador.
- **En Elis.** Todas las celdas con datos de 2026 se reexpresan a la base 2025.

## I9 · El recuento «N de M comprobadas» sumaba los auxiliares

- **Hecho.** Daba, por ejemplo, «330 de 232».
- **Corrección.** Ahora se cuenta aparte la cobertura del universo (`comprobadas_universo`) en el comprobador, el pipeline y el informe. La batería pasa 33/33.
- **Material cerrado.** Viscofan decisiones conserva el texto anterior.

## I10 · Formato CAMBIO sin vía para corregir la Historia

- **Hecho.** La corrección de pensiones I25:L25 de Elis no cabía en el CAMBIO, porque la Historia la construye `fase1_historia.py` desde fase1_partes.
- **Corrección.** Clave nueva `correcciones_fase1_partes` en `cambiar_base.py`:
  - cada corrección exige el valor impreso esperado, la fuente y el motivo;
  - si lo encontrado no es lo esperado, la preparación se detiene;
  - los originales van a antecedentes y el origen no se toca.
- **Prueba.** Nueva en el grupo D; el grupo pasa 9/9.

## I11 · Limpieza de espacio de disco (14-nov, ≈17:30; autorizada por la persona responsable)

- **Hecho.** Quedaban 3,3 GB libres y las comprobaciones finales necesitaban ≈4 GB.
- **Comprobaciones previas.**
  - Ninguna ejecución activa usaba las rutas.
  - La copia de verificación de i3 coincidía con la instantánea `instantaneas/i3` en todos los archivos comunes; solo tenía de más salidas de pruebas y cachés.
- **Qué se borró:** la copia `ronda_i3/munger_v2_r1` y 54 carpetas temporales de pruebas de /tmp de los días 12 y 13.
- **Qué se conserva:**
  - `instantaneas/i3`, el código exacto de i3;
  - el registro, las huellas, el inicio y el fin de `ronda_i3`;
  - los resultados únicos de la ejecución, en `ronda_i3/conservado_resultados_i3/` (resultados_integracion_v64.json, resultado_comprobadores.json y cuatro archivos de resultados_reparacion).
- **Espacio libre:** 3,3 → 7,1 GB.

## I12 · C48 de Elis: el libro y fase1_v63.json no coinciden (riesgo declarado; revisor RE6)

- **Hecho.** El libro conserva C48 = 108,0 de la etapa 1: 82,933 de intereses netos más 25,067 de intereses de arrendamientos. `fase1_v63.json` reconstruye 82,933. La fase 1 no pisa un valor migrado.
- **Riesgo.** Si el libro se regenerara desde cero, C48 bajaría a 82,933 y el FCF base subiría ≈25 mm sin que nadie lo decidiera.
- **Propuesta:** fijar C48 en `fase1_v63.json` con su derivación en un próximo cambio de base. No se toca en este expediente.

## I13 · El comprobador no detecta un fundamento desfasado si el valor coincide (Elis, 14-nov)

- **Hecho.** Con los libros de Elis regenerados, el comprobador no marcaba nada. Pero los fundamentos registrados de varias hipótesis seguían siendo los del expediente anterior: citaban 259,08, 79,7 y 1.429,4 / 857,1 / 28,2. El valor de cada celda coincidía, y la comprobación de una hipótesis no compara su texto con el del libro.
- **Corrección en este expediente.** El extractor actualizó, de forma manual, los fundamentos con el texto vigente del libro y pasó una vez todas las hipótesis y convenciones. Después las revisa el revisor independiente.
- *Propuesta:* que el comprobador compare el fundamento registrado con el texto vigente de la evidencia (columna N del Control maestro) y marque «desactualizada» si difiere. No se implementa en esta entrega.

## I14 · Segunda limpieza autorizada (14-nov, ≈18:58) y autorización permanente

- **Borrado.** `ronda_i4/munger_v2_r1` (3,1 GB) y `ronda_i5/munger_v2_r1` (3,2 GB), las copias completas de verificación de i4 y de i5.
- **Comprobaciones previas.**
  - Cada copia coincidía con su instantánea (`instantaneas/i4`, `instantaneas/i5`) en todos los archivos comunes; solo tenía de más salidas de pruebas.
  - Ninguna ejecución las usaba.
- **Qué se conserva.**
  - El código exacto, en `instantaneas/i4` e `instantaneas/i5`.
  - De cada ronda: el registro (`verificacion_completa.txt`), las huellas, el inicio y el fin.
  - Los resultados únicos, en `ronda_i4/conservado_resultados_i4/` y `ronda_i5/conservado_resultados_i5/` (6 archivos cada uno).
- **Espacio libre:** 3,3 → 9,5 GB.
- **Autorización permanente de la persona responsable (14-nov, 18:59; literal).** «Para futuras limpiezas equivalentes, queda autorizado eliminar temporales y copias de pruebas reproducibles sin preguntar nuevamente, siempre que: No haya ejecuciones utilizándolas. Se conserven código exacto, evidencias y archivos únicos. No se borren originales, fuentes ni entregables.» Las rutas eliminadas se registran aquí.

## I15 · Aviso de la auditoría de Elis: posible doble cómputo en la variante de dilución por acciones de rendimiento

- **Hecho.** Auditoría SA-d58921ca0d0cf0fa, condición e). La variante suma las acciones de rendimiento al denominador y deja C50 (SBC), que ya resta su coste.
- **Corrección.** La variante se etiqueta ahora como COTA, con posible doble cómputo parcial (`efecto_decisiones_elis_E6.py` y `.md`). Los valores no cambian.
- **Alcance.** El archivo de efectos está fuera del material auditado del expediente.

## I16 · Limpieza bajo la autorización permanente (14-nov, ≈19:20)

- **Borrado.** `comprobar_zip_414/extraccion_python` (1,5 GB): la extracción con Python del ZIP candidato.
- **Por qué se puede.** `empaquetar_zip.py --comprobar` la dio idéntica byte a byte a la extracción con unzip, que se conserva. Ninguna ejecución la usaba.
- **Qué se conserva.** La extracción con unzip, que sirve para la verificación completa de la candidata.

## I17 · Disco lleno durante los controles históricos de la candidata (14-nov, ≈19:55)

- **Hecho.** La primera ejecución de `controles_historicos_4_13.py` sobre la descompresión de la candidata se detuvo por falta de espacio («No space left on device»). Había hecho 8 controles; el de la batería 4.8.1 llenaba /tmp con unos 2 GB.
- **Limpieza bajo la autorización permanente.** Ninguna ejecución activa usaba estas rutas:
  - `personaje_v2/pruebas/_v64` de esa descompresión: salidas de la batería ya registrada en `verificacion_completa_candidata.txt`;
  - `/tmp/bat471_m0sm6lg2`: temporal del control interrumpido;
  - `/tmp/tmptbjeou_f`.
- **Pérdida declarada.** La copia de `resultados_integracion_v64.json` de esa ronda falló por falta de espacio y quedó vacía. Los recuentos están en el registro de la batería.
- **Resultado.** Se repitió entera la ejecución de los controles históricos. Los resultados están en `resultados/controles_historicos_en_arbol_4_14/` y se explican en `resultados/LEEME_CONTROLES_HISTORICOS_4_14.md`.

## I18 · Prueba de traspaso: documentación desfasada o incompleta (14-nov, ≈21:30)

- **Hecho.** Un agente receptor sin historial recibió solo el ZIP candidato y `PROMPT_NUEVA_VENTANA.md` (informe en `documentacion_cierre_4_14/traspaso/INFORME_TRASPASO.md`). La verificación completa dio PASA y el control de la 4.14, 35/35. El agente resolvió un relevo real y reanudó el pipeline hasta el paso 14.
- **Hecho.** El agente encontró estas dificultades en la documentación del ZIP candidato:
  1. la matriz del alcance y HITO_2 eran los del hito 2: auditorías «en curso», recuentos antiguos (32, 196, grupo D 8/8), Vidrala con «E1 + E4», el pendiente de C47 asignado a Vidrala y una ruta errónea del hallazgo del motor A;
  2. el resultado esperado de los controles históricos sobre el árbol 4.14 no estaba en el paquete. El LEEME de la 4.13 exige 89/89 en el control de la 4.13, que en el árbol 4.14 da 83/89;
  3. CONTINUIDAD decía «12 baterías» en §1 y «diez» en §2, y sus secciones §4, §5 y §7 no tenían la 4.14;
  4. ningún documento listaba los relevos vivos, ni decía si un relevo de un expediente sustituido se reanuda en su sitio o en una copia;
  5. no se documentaba el espacio en disco necesario;
  6. la guía daba 20–30 minutos para la verificación completa (medido: 36).
- **Corrección en la final.**
  - La matriz y HITO_2 se actualizan al estado final.
  - El LEEME de los controles sobre el árbol 4.14 ya va en la final (`resultados/LEEME_CONTROLES_HISTORICOS_4_14.md`).
  - CONTINUIDAD: recuento de baterías, §4, §5 y §7 con la 4.14, una lista de relevos vivos (§2, punto 6) y el espacio en disco.
  - La guía: la duración y la regla de la copia hermana.
- **Lo que no se corrige.** I19 e I20 se declaran, con propuesta. No se cambia código después de la candidata.

## I19 · Un relevo caducado no se avisa (prueba de traspaso)

- **Hecho.** `elis_motor_A/Elis` esperaba la auditoría SA-ed5561eac1cc5897 del material 9e1a725d…. `verificacion_entradas.json` se escribió después de fijar ese material, y desde la 4.14 forma parte de él (`cierre_v2.MATERIAL_FIJO`). El material calculado hoy es otro (72f855cf…).
- **Hecho, por lectura del código** (`pipeline.py`, paso 13): mientras espera, el pipeline no vuelve a fijar el material. Un APROBADO para la solicitud antigua se rechaza por `motivo_auditoria_no_corresponde`, y la corrección vuelve a pedir el material antiguo. Al agotar las correcciones, el expediente termina en `no_entregable`. *Interpretación:* el fallo es cerrado, porque nada se aprueba con un material distinto, pero el relevo no se puede cerrar siguiendo el prompt.
- **Salida probada.** `pipeline.py … --desde 12` en una copia hermana. Repite la verificación, fija el material nuevo (de91ac88…) y emite una solicitud nueva (SA-21babb1dd24901d1). La auditoría la respondió y el pipeline terminó en el paso 14.
- **Rutas absolutas.** Los prompts de `prompts_generados/` y varios JSON llevan rutas del entorno que los produjo. Al relanzar el pipeline, los prompts se regeneran con las rutas actuales. Las plantillas de relevo de la 4.13 son históricas.
- ***Propuesta*** (sin aplicar; toca código): que el paso 13, mientras espera, compare el material fijado con el calculado y, si difieren, vuelva a fijarlo y emita una solicitud nueva.

## I20 · La ficha y el informe de la V6.3 no muestran la aptitud por entradas

- **Hecho.** `ficha.py` escribe `aptitud_de_uso`, con la verificación de las entradas, solo en la vía V6.4 / V6.4.1. En la V6.3 (motor A), el resultado queda en `estado_pipeline.json → verificacion_entradas` y en el registro del pipeline, pero no en la ficha ni en el informe.
  - `elis_decisiones/Elis`: el registro es apto, 193 de 193, pero la ficha no lo dice.
  - En la copia del relevo de `elis_motor_A`, el registro no es apto y la ficha tampoco lo dice.
- **Hecho.** La guía §8.2 decía que la ficha y el informe muestran «apta por entradas: no» sin distinguir la plantilla. Se corrige: eso vale para la V6.4 y la V6.4.1. En la V6.3 se lee en `estado_pipeline.json`.
- *Interpretación.* Ninguna salida V6.3 se presenta como apta para dinero real, porque no lleva ningún bloque de aptitud. Pero quien lea la ficha no ve si las entradas están verificadas. El motor A ya no está validado (F1).
- ***Propuesta*** (sin aplicar): `aptitud_de_uso` también en la V6.3. Cambia las salidas V6.3, y por eso el piloto y las referencias de los controles. Requiere encargo, una batería y la regeneración de las referencias.

## I21 · Limpiezas de la prueba de traspaso (14-nov, ≈21:03 y ≈21:40)

- **En la descompresión del agente receptor** (`/home/claude/traspaso_414`, fuera del paquete), bajo la regla 11.10: los `*.xlsx` y `vigencia/` de `personaje_v2/pruebas/_v64/` y `/tmp/bat471_v8aovwgv`. Las rutas están en `traspaso/_logs/LIMPIEZAS.txt`.
- **Después del informe, por la orquestación.** Lo único se conservó en `documentacion_cierre_4_14/traspaso/`: el informe, los registros, el relevo, y la auditoría y las salidas de la copia del relevo. El borrado de la descompresión del agente receptor (`/home/claude/traspaso_414/munger_v2_r1`, 1,9 GB, fuera del paquete) lo detuvo una comprobación de seguridad del entorno, y no se hizo. Esa carpeta queda en el contenedor de trabajo: no forma parte de ninguna entrega.
- **Borrado sí hecho.** Las partes de 20 MiB del ZIP candidato, que se reproducen dividiendo el ZIP. Se conservan el ZIP candidato y su `.sha256`.
