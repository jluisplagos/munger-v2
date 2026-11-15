# Informe de reparación del cierre y la presentación (entrega 4.6, 9-nov-2026)

**Categorías:**
- **[Hecho]**: comprobado directamente por Claude o por un script del paquete.
- **[Antecedente externo]**: comprobado por otra parte.
- **[Pendiente]**: queda abierto.

**Alcance del encargo.**
- **Autoriza** cambios de código, documentación, formatos y pruebas estrictamente necesarios para cuatro incidencias.
- **No autoriza** cambiar criterios financieros, umbrales, materialidad, palancas ni probabilidades.

**Ningún número del ensayo ha cambiado** (`resultados/comparacion_con_4_5.md`, 30 de 30 controles).

## 0. Cómo se ha procedido

1. **Reproducción antes de corregir.** `scripts/reproducir_incidencias.py` se ejecutó con el código de la 4.5 sobre copias temporales. Resultado: las cuatro incidencias se reproducen en cinco comprobaciones (`reproduccion/reproduccion_codigo_4_5.txt`).
2. **Reparación mínima:**
   - un módulo nuevo, `scripts/cierre_v2.py`;
   - cambios acotados en `pipeline.py`, `ficha.py`, `informe.py` y `verificar_todo.sh`;
   - armonización de prompts, anexos, personaje y encargo.
3. **Pruebas.**
   - Acceptance tests nuevos: `pruebas/test_cierre_v2.py`, 40 de 40.
   - Regresión: 114/114 y 30/30, con los mismos nombres.
   - Reproducción con el código reparado: ninguna incidencia se reproduce (`reproduccion/reproduccion_codigo_4_6.txt`).
4. **Expediente regenerado** en `Vidrala/`. Es una copia del de la 4.5, que se conserva intacto.
   - Se reanudó en el segundo turno de la fase C con el código reparado.
   - Las fases A y B no se volvieron a ejecutar.
   - Auditoría nueva con contexto independiente (§5).

## 1. Incidencia I1 · `concluido` publicado antes de la auditoría

**Comportamiento anterior reproducido** [Hecho]:
- Con `--desde 11 --hasta 11` y sin auditoría, el paso 11 escribía `ficha.json` oficial con `concluido`.
- Con `--desde 14` sin auditoría, el pipeline cerraba `concluido` con código 0.

**Requisito incumplido:** el Anexo D §D.6 dice que «`concluido` es provisional: lo confirma el pipeline tras la auditoría APROBADO y hasta entonces no se escribe en la ficha». El encargo pide además que las reanudaciones, las llamadas directas y las aprobaciones de otra versión no cierren.

**Qué cambia:**
- **Paso 11.** Escribe solo **material provisional**: `ficha_provisional.json`, con `provisional.estado_propuesto` y `confirmado = false`, e `informe_provisional.md`, con la nota de material provisional. Una salida oficial anterior se mueve a `.anterior`.
- **Paso 13.** Antes de pedir la auditoría:
  - regenera el material provisional después del paso 12, para que la huella del libro sea la del libro auditado;
  - fija el **material auditado** en `material_auditoria.json`, con la SHA-256 de los artefactos y un identificador.

  El prompt pide la línea `Material auditado: <id>`. Un APROBADO que no nombra el material vigente no cierra: se pide otra auditoría, hasta `max_correcciones_esquema`, y después `no_entregable`.
- **Paso 14.** Cierra solo si se cumplen tres condiciones:
  - APROBADO según la regla estricta de H2 (`Pipeline.veredicto_auditoria`, **sin cambios**);
  - el identificador nombrado es el fijado;
  - el material actual es el fijado.

  Si falta alguna, el resultado es «CIERRE RECHAZADO» (código 4): ninguna salida oficial y vuelta al paso 13. Se aplica también con `--desde 14`.
- **`ficha.py --estado concluido`** sin `--provisional` aplica la misma comprobación; si falla, termina con código 3 y no escribe nada.
- **Sin estados nuevos.** No se añade un sexto estado ni se usa `pendiente_*` ni `no_entregable` para representar la espera.
- **Estados que no pasan por la auditoría** (`no_entregable`, `pendiente_de_datos` o `modelo_no_aplicable` tempranos): se escriben como antes.

**Pruebas que lo acreditan** (`test_cierre_v2.py`, grupo I1, 16 pruebas):
- estado antes de recibir la auditoría:
  - sin ficha ni informe oficiales;
  - provisional marcado;
  - material fijado con su id en el prompt;
  - huella del libro igual a la auditada;
- `ficha.py` directo sin auditoría (código 3);
- `--desde 14` sin aprobación (código 4, vuelta al paso 13);
- REPETIR, que vuelve a la fase C sin cierre;
- auditoría mal formada, sin el punto 16, que da REPETIR por H2;
- APROBADO con otro id;
- APROBADO sin línea de material;
- material cambiado mientras se espera;
- APROBADO válido, con estado, ficha, informe y resumen coherentes;
- aprobación anterior con material cambiado y `--desde 14` (código 4);
- `ficha.py` directo con la aprobación de otra versión (código 3);
- agotamiento de las correcciones de la auditoría, que conserva `no_entregable`.

**En el ensayo real** [Hecho]. La primera auditoría nueva (APROBADO, material `305c3a5b…`) dejó dos avisos sobre artefactos del material:
- la huella del libro en la ficha provisional era anterior a las cachés del paso 12;
- una frase de `fase_c.md` estaba desactualizada.

Se corrigieron el código y esa frase, y el pipeline **rechazó** esa auditoría para el material nuevo (`74b94f80…`): «la auditoría corresponde al material 305c3a5bea1c90ab, no al fijado 74b94f8072dd58c1». Una segunda auditoría nueva e independiente aprobó el material vigente, y solo entonces el paso 14 escribió las salidas oficiales.

## 2. Incidencia I2 · marca «con datos de etapa 1 incompletos»

**Comportamiento anterior reproducido** [Hecho]. Con seis datos en `entrada_v63.json → necesarios_para_listo_provisional`, ni la ficha ni la sección 1 del informe llevaban la marca.

**Requisito incumplido:** encargo del personaje §3.4: «la conclusión se marca "con datos de etapa 1 incompletos"».

**Qué cambia:**
- `ficha.datos_etapa1_incompletos` = {`marca`, `causas`, `nota`}. Las causas son la lista exacta del disparador estructurado, con cada entrada copiada entera.
- La sección 1 del informe muestra la marca con las causas.
- No se activa por el texto «NO LISTO» ni por los no bloqueantes.
- No sustituye la revisión S-19: un dato material mantiene `pendiente_de_datos`.

**Pruebas que lo acreditan** (grupo I2, 6 pruebas):
- dato necesario no material: marca presente y causa exacta;
- evidencia pendiente con números completos (el expediente real, 6 causas): marca presente;
- entrada completa: marca ausente;
- solo no bloqueante: marca ausente;
- dato material: recorrido completo con `pendiente_de_datos`, acción nula y diagnóstico;
- regeneración tras resolver la carencia: la marca desaparece.

## 3. Incidencia I3 · correspondencia entre D10, el JSON y C104

**Comportamiento anterior reproducido** [Hecho]:
- La fase C escribió «fundamento no procede (conclusión no favorable; hipótesis Palancas C8 acotada)», fuera de las cuatro etiquetas de la plantilla.
- `coherencia_fase_c` lo aceptaba, igual que «fundamento XYZ inventada» o «fundamento lista vacía» con `no_procede`.

**Requisito incumplido:** una correspondencia inequívoca entre resultado, estado, acción, hipótesis y etiqueta visible.

**Qué cambia:**
- **Tabla cerrada** (`cierre_v2.FUNDAMENTO_C104`; Anexo D §D.6, subsección nueva):

  | Estado y acción | Resultado | Etiqueta |
  |---|---|---|
  | concluido · comprar | sin_limitacion | «lista vacía» |
  | concluido · comprar | comprobacion_conjunta_superada | «comprobación conjunta superada» |
  | concluido · esperar, descartar o demasiado_dificil | no_procede | «no procede (conclusión no favorable)» |
  | pendiente_de_investigacion | pendiente_de_investigacion | «pendiente de investigación» |
  | pendiente_de_datos | no_procede | «pendiente de datos» |

- **Combinaciones rechazadas:** cualquier otra, entre ellas `comprar` con `no_procede`, una etiqueta desconocida o una etiqueta contradictoria con el JSON.
- **Comprobación conjunta:** no se exige para una conclusión no favorable.
- **Se mantienen:**
  - el prefijo;
  - D16;
  - los requisitos de `comprar`;
  - S-19;
  - el precio objetivo provisional.
- **Documentos armonizados:**
  - `personaje_munger_v2.md`;
  - `ANEXO_A` (C104);
  - `ENCARGO_personaje_v2.md`;
  - `prompts/fase_c_turno2.md`;
  - `prompts/verificacion.md` (punto 11);
  - `ANEXO_D`.

  La etiqueta del auditor sintético para `no_procede` pasa de «lista no vacía (conclusión no favorable)» a la armonizada (adaptación justificada: era la misma contradicción).
- **En el ensayo:** C104 pasa a «… · fundamento no procede (conclusión no favorable) · hipótesis que más condiciona: Palancas C8 (acotada) · …». La información de la hipótesis se conserva en un segmento aparte. La frase de `fase_c.md` que explicaba la etiqueta libre se actualiza.

**Pruebas que lo acreditan** (grupo I3, 10 pruebas):
- los cinco casos admitidos;
- `no_procede` para eludir los requisitos de `comprar`;
- una etiqueta contradictoria;
- una etiqueta desconocida;
- una combinación no permitida;
- la fase C real 4.5: la etiqueta libre se rechaza y la armonizada se admite sin comprobación conjunta.

## 4. Incidencia I4 · avisos de alcance junto a las comparaciones con el precio

**Comportamiento anterior reproducido** [Hecho]. Las secciones 6 (DCF inverso: «el precio actual descuenta…») y 7 (escalera, zona frente a 87,90) no llevaban ningún aviso del alcance exploratorio.

**Requisito incumplido:** el alcance declarado tiene que repetirse dentro de cada sección afectada, sin codificar la empresa, las fechas ni las cifras en el generador.

**Qué cambia:**
- **Metadato explícito y opcional:** `alcance_v2.json` = {`tipo`: `ensayo_exploratorio`, `aviso`, `fuente`}. Lo escribe quien define el expediente.
  - **En este ensayo** lo escribió la orquestación con la fuente del encargo 4.5 §6 y 4.6 §6. El texto es el del alcance ya declarado en la 4.5.
- **Generadores:**
  - `ficha.alcance` lo conserva;
  - `informe.py` repite su aviso dentro de las secciones 1, 6 y 7;
  - sin el metadato no hay ningún aviso;
  - un metadato mal formado detiene `ficha.py`.

**Pruebas que lo acreditan** (grupo I4, 8 pruebas):
- secciones 1, 6 y 7, leídas por separado, con el aviso una vez cada una;
- ningún duplicado tras regenerar;
- la ficha conserva el alcance y las notas de la fase C;
- los valores financieros son iguales a los de la ficha 4.5;
- un expediente ordinario no recibe ningún aviso inventado;
- un metadato mal formado detiene `ficha.py`.

## 5. Auditoría nueva

**[Hecho] Agente sin participación en la reparación ni en el análisis**, con el prompt generado (16 comprobaciones y la línea de material) y la instrucción expresa de verificar I1–I4 dentro de los puntos 1, 10, 11 y 16.
- **Resultado:** 16 de 16 en PASA, sin FALLA, `Material auditado: 74b94f8072dd58c1`, **Veredicto: APROBADO**.
- **Comprobaciones que hizo:**
  - recalculó las 18 huellas del material;
  - verificó la marca entrada por entrada;
  - verificó la etiqueta de C104 contra la tabla;
  - verificó el aviso en cada sección.
- **Avisos no bloqueantes:**
  - `verificacion_integridad.txt` registra la huella del libro antes de las cachés del paso 12 (comportamiento anterior, fuera del encargo);
  - el tipo impositivo (pendiente financiero N1);
  - el recuento de citas de la sección 13;
  - `ficha.etapa1` copia lo heredado;
  - C104 repite «precio de Sí ≤».
- **Tensiones normativas declaradas, ninguna sin resolver:**
  - **`concluido` en la ficha provisional.** Lo resuelve la regla específica de la 4.6. El Anexo D §D.6 se ha precisado: «no se escribe en la ficha oficial `ficha.json`».
  - **«Conclusión favorable» con dos sentidos.** En S-19 incluye `esperar`; en D10, solo `comprar`. Queda como pendiente normativo P-N1: la reparación no cambia criterios.
  - **Encabezado del prompt ambiguo.** Corregido en `pipeline.py` para próximas ejecuciones.

La auditoría de la 4.5 y la primera de la 4.6 se conservan como antecedentes (`auditoria_4_5_antecedente.md`, `auditoria_4_6_primera_material_305c3a5b.md`).

**La aprobación del ensayo no es una validación financiera para invertir.**

## 6. Verificación numérica y regresión

**[Hecho] `scripts/comparar_con_4_5.py`, 30 de 30 controles.** No cambian:
- P1 (el registro humano, idéntico byte a byte), las fuentes, `fase1_v63.json` y los libros de datos;
- extracto, fases A y B, referencias y datos ausentes;
- `resultados.json`: valores, estados, palancas, probabilidades, `r_op`, puente, V0, m0, t y `f`;
- `precio.json`: V 53,67 / 70,77 / 86,49, ponderado 70,50, precio de Sí 65,69, zona caro;
- r = 0,09; la caja de 108,352 sin restar el dividendo; el puente de 160,784;
- el contraste entre motores, con sus cinco variantes recalculadas sobre el libro 4.6, y su descomposición, idénticos.

**Únicas diferencias**, todas de presentación: C104 (en fase_c.json, el libro y `celdas_juicio_analisis`), dos líneas de `fase_c.md` y los campos nuevos de la ficha (`datos_etapa1_incompletos`, `alcance`, `cierre`).

**Pruebas de regresión** sobre el código reparado:
- `test_comprobadores.py`: 114/114;
- `test_pipeline_sintetico.py`: 30/30, con los mismos nombres;
- las baterías acotadas de la 4.2 a la 4.5 (45, 217, 43, 72 y 60) sobre sus referencias intactas, en la verificación del paquete;
- `scripts/comprobar_cierre_ensayo.py`: 24 de 24.

## 7. Archivos modificados y nuevos (código y documentación)

**Modificados** (respecto a la 4.5):

| Archivo | Cambio |
|---|---|
| `personaje_v2/scripts/pipeline.py` | Pasos 11, 13 y 14; código 4; coherencia D10↔C104 |
| `personaje_v2/scripts/ficha.py` | `--provisional`; guarda del cierre; marca; alcance; `cierre` |
| `personaje_v2/scripts/informe.py` | `--provisional`; marca en §1; aviso en §1, §6 y §7 |
| `personaje_v2/scripts/verificar_todo.sh` | Valida y cita también el material provisional |
| `personaje_v2/prompts/verificacion.md` | Material provisional, línea de material, I1–I4 en los puntos 1, 10, 11 y 16 |
| `personaje_v2/prompts/fase_c_turno2.md` | Etiqueta formal y tabla |
| `personaje_v2/personaje_munger_v2.md` · `ANEXO_A_celdas_de_juicio_V6_3.md` · `ENCARGO_personaje_v2.md` | Formato de C104; paso 11 |
| `personaje_v2/ANEXO_D_salidas_y_formatos.md` | Tabla de correspondencia y cierre con material provisional |
| `personaje_v2/DECISIONES.md` | Entrada del 9-nov-2026 |
| `personaje_v2/pruebas/agentes_sinteticos.py` | Auditor sintético con el id del material; etiqueta de `no_procede` |

**Nuevos:** `personaje_v2/scripts/cierre_v2.py` y `personaje_v2/pruebas/test_cierre_v2.py`.

La relación completa con huellas está en `CAMBIOS_ARCHIVOS.txt`.

**Sin cambios:**
- `verificar_paquete.sh`;
- H1–H3;
- `veredicto_auditoria`;
- `v6/`;
- los expedientes y contrastes anteriores.

## 8. Pendientes que se conservan

- **[Pendiente] Financieros, sin cambios** (`../2026-11_Vidrala_ensayo_4_5/INFORME_DEL_ENSAYO_4_5.md` §8):
  - N1, el tipo impositivo de C52;
  - N2, la base del margen C8;
  - N3, el límite del MALO;
  - N4, los 38 ceros pendientes;
  - N5, L25;
  - N6, `r_op`;
  - N7, las acciones;
  - N8, el dividendo sin derecho;
  - N9, la ruta B;
  - N10, las probabilidades;
  - N11 y N12, notas documentales.
- **[Pendiente] Normativos nuevos, sin resolver por este encargo:**
  - **P-N1.** Armonizar los dos sentidos de «conclusión favorable» (S-19 frente a D10).
  - **P-N2.** `verificacion_integridad.txt` del paso 12 registra la huella del libro antes de sus cachés.
  - **P-N3.** Incluir `test_cierre_v2.py` en `verificar_paquete.sh`. No se hace aquí para no cambiar el verificador del paquete; se ejecuta aparte.

**[Antecedente externo]** Según la persona responsable, la revisión de ChatGPT de la 4.5 comprobó la integridad, los originales, P1, las baterías y las cinco variantes.

**Modelos.** Opus en todo, con dos agentes de auditoría de contexto separado, ambos Opus. Fable no se usó: ningún paso lo justificaba.
