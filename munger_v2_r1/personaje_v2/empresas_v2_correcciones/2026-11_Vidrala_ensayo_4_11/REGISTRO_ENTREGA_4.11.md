# Registro de la entrega 4.11 · primera integración económica experimental del motor B

**Qué es.** El registro de la entrega: qué pedía el encargo 4.11, qué se hizo, qué cambió, qué modelos se usaron, cómo se atendió la revisión interna y qué queda.

**Dónde está el resto.**

- Resultados: `INFORME_INTEGRACION_4_11.md`.
- Pruebas: `REGISTRO_PRUEBAS_4_11.md`.
- Decisiones humanas propuestas: `propuestas/PROPUESTA_HUMANA_4_11.md`, sin firmar.
- Cuaderno de trabajo del proceso: `REGISTRO_AVANCE_4_11.md`.

## 1. Encargo y resultado (encargo §11)

| Entregable | Estado |
|---|---|
| 1. Plantilla experimental, referencia, documentación y selección de configuración | **Hecho.** `v6/v64_experimental/` (plantilla, referencia, verificador, inventario, constructor determinista y `docs/README_V6.4_experimental.md`); `personaje_v2/config_v2_v64_experimental.json`; `seleccion_plantilla.py` |
| 2. Scripts, inventarios, esquemas, lectores, escritores, verificadores y prompts conectados | **Hecho.** Lista en §2; batería de 58 pruebas |
| 3. Cambio de base con configuración y evidencia coherentes | **Hecho.** `personaje_v2/scripts/cambiar_base.py`; control y piloto «CONCUERDA Y SIN RESTOS» |
| 4. Configuraciones de reproducción y tabla de resultados aislados y combinados, con conciliación anual y terminal | **Hecho.** `scripts/casos_v64.py` (117 casos con sus referencias completas); `piloto/Vidrala/configuracion_v64_variantes.md`; hoja «Conciliación B» en todos los casos |
| 5. Expediente nuevo completo | **Hecho.** `piloto/Vidrala/`: libros, fases, resultados, ficha, informe, resumen aislado, comprobantes y auditoría interna APROBADO; concluido · Vigilar · esperar |
| 6. Réplica independiente y pruebas reproducibles, con sus límites | **Hecho.** `replica/` (117/117) y `personaje_v2/pruebas/test_integracion_v64.py`; límites en el README §8 y en `replica/INFORME_REPLICA.md` |
| 7. Informe de integración | **Hecho.** `INFORME_INTEGRACION_4_11.md` |
| 8. Registro de cambios, pruebas y revisión interna | **Hecho.** Este archivo, `REGISTRO_PRUEBAS_4_11.md` y `revision_interna/`; la respuesta a la revisión, en §4 |
| 9. VERSION, CONTINUIDAD.md, CAMBIOS_ARCHIVOS.txt, manifiesto y arranque | **Hecho.** Las versiones de la 4.10.1 están en `reproduccion/` |
| 10. ZIP completo con SHA-256, partes y registro externo de verificación | **Hecho al empaquetar.** El registro externo va fuera del ZIP |

## 2. Cambios fuera del expediente

**Archivos nuevos:**

- `v6/v64_experimental/`, entera;
- `personaje_v2/config_v2_v64_experimental.json`;
- `personaje_v2/scripts/`: `cambiar_base.py`, `configuracion_economica.py`, `seleccion_plantilla.py` (también la selección inversa, H1) y `variantes_configuracion_v64.py` (también los extremos del rango, H11, y las variantes sin zona, H10);
- `personaje_v2/pruebas/test_integracion_v64.py`.

**Archivos cambiados frente a la 4.10.1** (huellas antes y después en `CAMBIOS_ARCHIVOS.txt`, sección «RESPECTO A LA 4.10.1»):

| Archivo | Motivo |
|---|---|
| `personaje_v2/scripts/pipeline.py` | Selección explícita (código 2). Aplicación de la configuración en el paso 2. Variantes y entradas de la fase C en el paso 10. `coherencia_v64`. Reaplicación por contenido de las celdas. Comprobación en el paso 12, también de que la variante «activa» es `precio.json` (H10). Motor no cubierto por la configuración: límite del modelo (H3). `MUNGER_CONFIG` para los subprocesos |
| `config_v2.py`, `escribir_v63.py`, `verificar_todo.sh`, `comprobar_entorno.sh`, `comprobar_entrada_v63.py`, `comprobar_gramatica.py`, `migrar_v53_a_v63.py`, `rellenar_fase1_v63.py` | La configuración por omisión sale de `MUNGER_CONFIG`; `--config` vale None por omisión. La V6.3 sigue igual cuando no se elige otra. `comprobar_entrada_v63.py` separa además «no calculable por datos» de «no cubierto por la configuración experimental» (H3) |
| `cierre_v2.py` | `MATERIAL_FIJO` incluye `configuracion_economica.json`, `plantilla_activa.json` y `configuracion_v64_variantes.json` (solo existen en expedientes V6.4). Resumen propio de las filas V6.4 y su historial (`nombre_resumen`, `ruta_historial`; H2); sin cambio para los expedientes V6.3 |
| `leer_v63.py`, `leer_resultados.py`, `volcar_datos_v63.py` | Lectura de la configuración V6.4 y de la conciliación (clave solo en libros V6.4) y sección 0 del volcado |
| `ficha.py`, `informe.py` | Versión de plantilla desde `plantilla_activa.json`; configuración económica (solo V6.4); §14 del informe; distancias con el denominador identificado (solo V6.4). Después de la revisión: «provisional» en el §1 (H7), límites de R1 en la ficha (H12) y cuenta de variantes calculadas (H10) |
| `comprobacion_conjunta.py` | N1, N2, λ y θ pueden moverse en la combinación |
| `esquema/fase_c.esquema.json`, `esquema/ficha.esquema.json` | `configuracion_v64` (opcional) y `configuracion_economica`; `plantilla` ∈ {V6.3, V6.4 experimental} |
| `prompts/fase_a.md` | Con la V6.4 experimental, el motor se elige por los criterios del personaje, como si la configuración no existiera; un motor no cubierto lleva al límite del modelo (H3) |
| `prompts/fase_b.md`, `fase_c_turno1.md`, `fase_c_turno2.md`, `verificacion.md` | La configuración es una entrada, no se descuenta dos veces. La fase C evalúa cada parámetro y el mantenimiento. La auditoría revisa la V6.4 dentro de los puntos 1, 10 y 11 (siguen siendo 16) |
| `ANEXO_D_salidas_y_formatos.md` | §D.12: formatos nuevos |
| `verificar_paquete.sh` | Batería de la V6.4 obligatoria, la primera de las obligatorias (mínimo 58) |
| `VERSION`, `CONTINUIDAD.md`, `PROMPT_NUEVA_VENTANA.md`, `CAMBIOS_ARCHIVOS.txt`, `MANIFIESTO_SHA256.txt` | Describen la 4.11 o se regeneran |

**Lo que no cambia.** La plantilla V6.3 y su referencia, `config_v2.json`, el kit, los originales (`personaje_v2/empresas_v2/`) y los expedientes de entregas anteriores conservan sus bytes. Lo comprueba `scripts/comprobar_entrega_4_11.py`.

**Regresión.** Todas las baterías anteriores pasan con el código nuevo (`REGISTRO_PRUEBAS_4_11.md` §4).

## 3. Modelos y agentes

| Rol | Modelo y esfuerzo | Nota |
|---|---|---|
| Orquestación, construcción e integración | Opus (modelo principal), esfuerzo máximo | Recomendado al empezar y aceptado por la persona responsable («adelante») |
| Réplica independiente | **Fable**, esfuerzo máximo, contexto separado | **Motivo:** contrastar miles de fórmulas con un modelo distinto, sin leer las fórmulas. **Resultado:** 107/107 a la primera y 117/117 sobre la plantilla final; observaciones del terminal con R1, del crédito de H y de las ramas sin caso. Se avisó antes del uso |
| Extracción (paso 5) | Sonnet, esfuerzo medio (el de la configuración) | Contexto limpio |
| Fase A, fase B, fase C (dos turnos, un solo agente) | Opus, esfuerzo extra (como en la 4.10.1; la configuración prevé alto) | Contexto limpio; sin LibreOffice ni pipeline |
| Auditoría (paso 13) | Opus, esfuerzo extra (la configuración prevé medio) | Contexto separado; se identifica como interna; APROBADO 16/16 con avisos |
| Revisión interna | **Fable**, esfuerzo máximo, contexto separado | **Motivo:** es la revisión de más consecuencia (fórmulas, flujo, fuentes y límites económicos) y la hace un modelo distinto del que construyó. Se avisó antes del uso. **Resultado:** §4 |

**Alcance de Fable.** No ejecutó todo el procedimiento: solo la réplica y la revisión interna.

**Ejecución en secuencia.**

- Ningún agente ejecutó el pipeline ni LibreOffice.
- Los recálculos, la batería y los controles los ejecutó la orquestación, nunca dos a la vez.
- Las esperas se resolvieron con avisos de fin de tarea, sin bucles indefinidos.

## 4. Revisión interna y respuesta

**Revisión.** `revision_interna/REVISION_INTERNA_4_11.md` (Fable, esfuerzo máximo, contexto separado; encargo en `ENCARGO_REVISION_INTERNA_4_11.md`). **Veredicto: sin bloqueantes**; se puede entregar como implementación experimental no adoptada. Hallazgos: 4 importantes (H1–H4), 10 menores (H5–H14) y 8 observaciones (O1–O8).

**Vigencia del piloto después de las correcciones** (hecho comprobado, `resultados/vigencia_piloto_4_11.md`). Con el código final y solo en lectura:

- el cierre del piloto sigue vigente (`cierre_v2.motivo_vigencia`, la función que usan el pipeline y los generadores);
- la selección de plantilla es conforme;
- las variantes corresponden a `precio.json` (la comprobación nueva del paso 12);
- las celdas de configuración de los libros son las de `configuracion_economica.json`;
- ninguno de los 282 archivos de `piloto/` cambió.

El material auditado son archivos del expediente, no el código. Las salidas del piloto no se regeneraron: una ficha nueva tendría otro contenido (los límites de R1) y sustituir una ficha cerrada exige una auditoría nueva.

| Hallazgo | Respuesta | Dónde | Efecto en el piloto |
|---|---|---|---|
| **H1** · selección inversa V6.3 → V6.4 | **Corregido.** Código 2 sin escribir nada si la carpeta tiene libros V6.3 o pasos hechos y no tiene `plantilla_activa.json`. Prueba en la batería (C) y ejecución del §5.1 sobre una copia del expediente cerrado de la 4.10.1: código 2, 0 archivos nuevos o cambiados | `seleccion_plantilla.py`; `resultados/seleccion_inversa_4_11.md`; README §7; Anexo D §D.12; informe §6.4 | Ninguno: el piloto tiene su `plantilla_activa.json` y la selección es conforme |
| **H2** · el resumen no identifica el modelo | **Corregido (vía mínima).** Las filas V6.4 van a `resumen_v2_v64_experimental.csv`, con su historial aparte, también en una llamada a mano con `config_v2.json`. Prueba en la batería (C). Columnas nuevas: no (vía completa, sin hacer) | `cierre_v2.py`; `config_v2_v64_experimental.json`; Anexo D §D.10 y §D.12; README §7 | Su fila sigue en `piloto/resumen_v2.csv`, registrada; una ejecución nueva publicaría en el archivo nuevo |
| **H3** · motores A y C con la configuración experimental | **Corregido.** `entrada_v63.md` separa datos y cobertura; motor no cubierto → `no_entregable · limite_del_modelo` (código 4 de `comprobar_entrada_v63.py`); párrafo nuevo en `prompts/fase_a.md`; prueba con agentes simulados (C) | README §7 y §8.6; Anexo D §D.12; informe §1 | Su `entrada_v63.md` conserva el texto anterior; la fase A eligió B por los hechos («lo elegiría igual en la V6.3») |
| **H4** · dos reglas para la materialidad del objetivo | **Llevado a decisión humana** (D411-MATERIALIDAD, con recomendación). Anexo D §D.12 define lo que significa hoy `material_para_conclusion`; aviso añadido al informe §3 y límite en el §4. `coherencia_v64` no cambia hasta la decisión | propuesta; Anexo D §D.12; informe §3 y §4.9 | El estado y la conclusión no se cambian (la opción de la fase C es defendible) |
| **H5** · 7.844 fórmulas nuevas | **Corregido:** 7.870 (Motor 7.068, «Conciliación B» 670, «Configuración V6.4» 131 y Panel!C18) | README §3; informe §1 | Ninguno |
| **H6** · BL sin P0 y lecturas sin contraste | **Declarado y probado.** README §5: BL no incluye P0 (en el piloto, 19,80 M€, unos 0,56 €/acción: 58,19 frente a unos 58,75). Contraste numérico nuevo de BL, BP, BQ y Diagnóstico B176:D177 en todos los casos válidos (en la batería: 91 casos, 71 con P0, 11.284 filas, 0 diferencias) | README §5 y §8.10; batería B | Ninguno: BL es una lectura |
| **H7** · §1 del informe sin «provisional» | **Corregido en `informe.py`** para los expedientes nuevos, con las hipótesis cortadas por palabra. Campo propio en la ficha: no (pendiente, declarado en el Anexo D §D.12) | `informe.py`; Anexo D §D.12 | Su `informe.md` conserva la línea original; la marca está en C104, la ficha (`fundamento`) y los §2, §8, §10 y §12. Con el código actual, la línea del §1 llevaría «(provisional: lo condicionan Palancas!B16; Palancas!D16; B69:D69; Configuración V6.4 · P-M1 (PM1.estructura SR1 · PM1.familia Λ · PM1.parametro λ = 1,15))», calculado con la expresión de `informe.py` sobre su ficha, sin regenerar el informe |
| **H8** · `ficha.etapa1.cubo` | Sin cambio: D-FICHA-ETAPA1, abierta desde la 4.10.1 | — | — |
| **H9** · textos de la base anterior fuera del rango | **Corregido:** `comprobar` los lista aparte sin contarlos (F5, H5, B10, B88, D88 y D100); concordancia guardada también del libro evaluado del control y del piloto | `cambiar_base.py`; `…/resultados/concordancia_*`; Anexo D; informe §1 | Ninguno en valores: CONCUERDA Y SIN RESTOS en los dos libros |
| **H10** · variantes no atadas al libro | **Corregido:** paso 12, variante «activa» = `precio.json`; una variante sin zona impide «misma zona en todas»; la ficha cuenta solo las calculadas. Prueba (C) | `pipeline.py`; `variantes_configuracion_v64.py`; `ficha.py` | Ninguno: sus 13 variantes calculan y la «activa» coincide |
| **H11** · el parámetro material sin variante | **Corregido:** campo `PM1.lambda_rango` / `theta_rango` y variantes de los extremos (prueba en C). Para el piloto, recálculo de λ = 1,10 y 1,25 en el libro: precio de Sí 60,12 y 53,00, zona caro | `configuracion_economica.py`; `variantes_configuracion_v64.py`; `resultados/rango_lambda_4_11.md`; propuesta D411-PM1-PARAMETRO | Su archivo de variantes no los tiene (su configuración no declaraba el rango); el cálculo aparte no lo modifica |
| **H12** · límites de R1 en la ficha | **Corregido en `ficha.py`** (terminal y palanca inerte). README §8.8, informe §4.10; la propuesta lleva k = 3 experimental y «no es un backtest» | `ficha.py`; README; informe; propuesta | Su ficha no los tiene; están en el informe de integración |
| **H13** · dominios sin comprobar | **Declarados** (README §8.9, informe §4.11) y **llevados a decisión** (D411-DOMINIOS): el umbral de f es una convención | README; informe; propuesta | Ninguno: no aparecen en el piloto ni en los 117 casos |
| **H14** · texto cortado y rutas en mayúscula | **Corregido** y propuesta regenerada (evaluación de la fase C íntegra; las rutas conservan la minúscula) | `scripts/propuesta_humana_4_11.py` | — |
| **O1** · amortización del terminal en «Conciliación B» | Declarado | README §8.12 | — |
| **O2** · comprobación conjunta con parámetros inactivos | Sin cambio (conservador) | — | No procede en el piloto |
| **O3** · ceros de la cartera P0 | Nota en D411-PM1-CARTERA; ningún cero se confirma | propuesta | — |
| **O4** · G7 y referencias con la base histórica | Declarado | README §8.11; informe §4.13 | Sin efecto |
| **O5** · ejecución a mano sin `MUNGER_CONFIG` | Declarado; el resumen ya no depende de la variable (H2) | README §7; Anexo D §D.12; informe §4.14 | — |
| **O6** · salto del requisito en el año 11 | Sin cambio pedido: el efecto de cada convención está en las variantes | — | — |
| **O7** · registros de pruebas | 58/58 en una sola pasada sobre la copia limpia (`REGISTRO_PRUEBAS_4_11.md` §6) y otra vez sobre la descompresión del ZIP final (registro externo) | `REGISTRO_PRUEBAS_4_11.md` | — |
| **O8** · detalles de texto | 31 % y λ ≈ 1,48 sobre la base de la hoja (informe §3; comprobado con las bases del libro); B177 vacío con g = 0 (README §8.10). Las fuentes de N1 y N2 con la ruta abreviada están en la configuración del piloto, que no se modifica | informe; README | — |

**Ejecuciones pedidas en el §5 de la revisión.**

1. Selección inversa (H1): hecha, CONFORME.
2. Fase A que elige el motor A (H3): hecha con agentes simulados en la batería; termina en `no_entregable · limite_del_modelo`.
3. Extremos de λ (H11): hechos; coinciden con la réplica del revisor (60,1154 y 52,9960). θ = 1 y λ = 1,46 no se recalcularon: solo se citan como réplica, sin afirmar zona.
4. Batería completa en una sola pasada: hecha, 58/58 en la copia limpia (`REGISTRO_PRUEBAS_4_11.md` §6).
5. Concordancia del libro evaluado del piloto (H9): hecha, CONCUERDA Y SIN RESTOS.

## 5. Porcentaje orientativo hacia la primera versión integrada supervisada

**Interpretación, no medición.** El encargo partía de ≈60 %. Esta entrega lo lleva a **≈68 %**.

**Qué suma** (unos 8 puntos):

- la integración técnica que pedía la especificación de la 4.10: plantilla V6.4, pipeline conectado, cambio de base general, batería obligatoria, réplica independiente y revisión interna sin bloqueantes, con H1–H3 corregidos (unos 6 puntos);
- un expediente real recorrido de punta a punta con agentes reales y auditoría APROBADO, más el control heredado igual que la 4.10.1 (unos 2 puntos).

**Qué no suma todavía:**

- **Adopción humana:** ninguna de las 13 decisiones está tomada. Sin D411-PLANTILLA y D411-MATERIALIDAD no hay versión «integrada» que ensayar.
- **Ensayos con dos o tres empresas:** no iniciados. De las seis analizadas, solo Viscofan (y Vidrala) usan el motor B; para las demás, la fase A tendría que elegirlo por sus criterios, o haría falta extender la integración al motor A.
- **Revisión externa** de esta entrega.
- **Validación económica:** que una estructura P-M1 describa mejor a la empresa no se ha demostrado; λ y θ siguen siendo hipótesis.

**Lectura del número.** El 68 % mide el camino hacia una primera versión integrada y supervisada del motor B. Para el uso con muchas empresas pesa además la cobertura del motor A, que hoy queda fuera de la capa experimental.

## 6. Entrega

- **ZIP completo:** `munger_v2_r1_entrega4.11_integracion_economica_experimental.zip`.
  - Se produce con `…_4_10/scripts/empaquetar_zip.py`, con los nombres UTF-8 marcados.
  - Se comprueba con Python `zipfile` y con `unzip`.
- **Acompañan al ZIP:**
  - su `.sha256`;
  - las partes de hasta 20 MiB, con su `.PARTES.txt`;
  - el registro externo `…VERIFICACION.txt`, fuera del ZIP.
- **Verificación final** sobre una copia limpia del ZIP: `verificar_paquete.sh completa` y los controles históricos, con las salidas de referencia en `resultados/` y el LEEME de controles.
