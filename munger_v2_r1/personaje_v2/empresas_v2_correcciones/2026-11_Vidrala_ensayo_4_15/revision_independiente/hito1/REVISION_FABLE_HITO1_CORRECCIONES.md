# Revisión afectada de las correcciones del hito 1 de la 4.15

Revisor: Fable (Claude, contexto separado de la implementación; no es una revisión humana) · 15-nov-2026.
Convención: **[Hecho]** = comprobado por el revisor ejecutando o leyendo (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida.

## 0. Qué se ha revisado y cómo

- **[Hecho]** Árbol: `revision_hito1/arbol_congelado/munger_v2_r1`, sin modificarlo; todo se ejecutó en una copia (`/tmp/rev_fable2/congelado`). Las huellas de los 59 scripts y pruebas, de `verificar_paquete.sh` y de `VERSION` del árbol congelado eran las mismas al empezar y al terminar (también tras el reinicio del servidor). SHA-256 de `verificacion_entradas.py`: `ecbe5909…5d59d48`; `rellenar_fase1_v63.py`: `641ddf31…a9bc8c`; `fase1_historia.py`: `1cf6844d…5dbd9`; `cambiar_base.py`: `0387aa46…3d4a`.
- **[Hecho]** Reproducciones: `revision_hito1/reproducciones_fable/v2/` (arnés `fx2.py`, adaptado a `huellas_registro`, y sondas `p1`, `p1b`, `p2`–`p7`, `p5b`, `p10`); salidas literales en `reproducciones_fable/salidas_v2/*.log`. Uso: `cd reproducciones_fable/v2 && PV=<copia>/personaje_v2 python3 -B p1_r123.py` (p5 usa `V2=<copia>`).
- **No ejecutado:** nada que use LibreOffice (`verificar_paquete.sh`, integración, sintética, reconstrucción de C48). De la reconstrucción se han **leído** los 8 JSON y su resumen; del diagnóstico de los registros reales se ha **reproducido** el resultado (sonda p7: coincide entrada por entrada).
- No se han revisado de nuevo I19, I20 ni F1 (fuera del hito). De `pipeline.py` solo se han leído los dos cambios del diff.

## 1. Baterías (sin LibreOffice, en la copia)

| Batería | Resultado | Código |
|---|---|---|
| test_verificacion_entradas_415.py | **71/71** PASAN | 0 |
| test_entrada_efectiva_415.py | **27/27** PASAN | 0 |
| test_verificacion_entradas_414.py | **33/33** PASAN | 0 |

**[Hecho]** La batería de la 4.14 sigue sin rebajarse: frente a la del árbol 4.14 conserva sus 35 llamadas `paso(...)` y 30 `r = con(...)`; solo cambian el rótulo del control positivo, dos casos positivos que se resellan y el fixture (interfaz nueva de `entradas_no_reproducibles` y vínculo con `huellas_registro`).

## 2. Tabla hallazgo → estado

| # | Hallazgo de la primera pasada | Estado | Reproducción (sonda → resultado) |
|---|---|---|---|
| 1 | `material: false` anula R1/R2 | **Parcialmente** | p1: en cálculo → error, no apto (también los 259 a la vez). **Residuo:** las 88 entradas de juicio con dato marcadas `material: false` con justificación «x», fuente ausente y sin revisor → `apto=True`, 233/321, `motivo: None` (N1). |
| 2 | Dato reetiquetado como convención/hipótesis/no aplicable | **Parcialmente** | p1: sin `justificacion_clase` → error; con ella y sin revisor → pendiente; con ella y revisor → comprobada y listada (`dato_hip`). `no_aplicable` con valor ≠ 0 → error. **Residuo:** p1b: los 156 datos numéricos de cálculo como `derivado` de un `aux:` «convención» sin fuente ni revisor → `apto=True`, 321/321, `datos_como_hipotesis: 0`; derivado con fórmula constante → comprobada; los 11 ceros de cálculo como `no_aplicable` «x» → `apto=True` (N2). |
| 3 | `sellar` legitima en bloque con fecha retroactiva | **Corregido, con límite declarado y un residuo** | p2 D1: `--fecha 2026-11-14` → rc 1; con fecha de hoy y comprobaciones del 14-nov → 0 selladas, 321 rechazadas; registro sin tocar. p7: los tres registros reales, 0 selladas. Orden `huella` → rc 2, no imprime huella. Cambiar revisor, fecha, extractor o fuente examinada tras el sello → desactualizada. **Residuo:** parámetro `hoy` de la API (N3). Límite declarado en el docstring: fechas reescritas por script + una orden → 321 selladas (p2 D1d); vínculo a mano con revisor y fecha copiados → apto (p2 D2b). |
| 4 | `entradas_no_reproducibles` falla en abierto | **Corregido** | p4 §3: sin `fase1_v63.json`, ilegible, `[]`, `analisis` no objeto, celda sin declarar, valor de texto → no reproducible y no apto; Vidrala C50 (real) detectada; Viscofan ninguna. p6: bloquea con el registro pendiente o con `material: false`. Editar la declaración tras el sello → desactualizada (batería). Límite aceptable: un `fase1_v63.json` editado **antes** del sello (C48 = 108 sin cálculo) no lo ve este control; lo cubren el sello del revisor y la reconstrucción. |
| 5 | Tolerancia 0,0011 en tasas y ratios | **Corregido para dato publicado y vigencia; parcialmente en derivados** | p1: 3,25 % frente a 0,0335 → discrepancia; g 0,019 frente a 0,02 → desactualizada; «euros» con escala 0,001 → error; ratio 0,887 con fuente 88,74 % → discrepancia. **Residuo:** el mismo ratio como `derivado` de un auxiliar 0,8874 sin `round` declarado → comprobada (N4). `_igual` y `TOL_ABS` quedan como código sin uso. |
| 6 | Universo de juicio sin el reparto geográfico | **Corregido** | p3: Palancas C7, C45, C46 y A28:B32 con dato dentro (juicio 89 / 85 / 99); huella y `n_calculo` iguales a `EE.instantanea` en los tres libros. La prueba J exige ya la igualdad `{B3, D3, B4, D4, C52}`. Quedan fuera C5 («Madura») y C9 («No»): selecciones, no cifras. |
| 7 | Un `calculo` declarado se salta H1 | **Corregido** | p4 §2: media 2016–2018 → `pendiente_verificacion=[2016, 2017, 2018]`; `construir` la conserva; `rellenar` → F45 «Dato no verificable» (antes «Rellenado y verificado»). |
| 8 | `cambiar_base`: descartes, herencia y diagnóstico | **Parcialmente** | p5: (a) C42 descartada ya no está en metadatos ni en `fase1_v63.json` ✔; (b) sin reconocer las heredadas → PREPARACIÓN DETENIDA, destino retirado ✔; (c) C47 867,167 → 857,167 y C48 82,933 → 108,0 ✔. **Residuos** (N5): las ocho celdas que la Historia no construye siguen como «0.097 → 0.097» (4.14: «None → 0.097»); el registro del cambio no lista las heredadas reconocidas ni sus motivos (p5b); motivo vacío aceptado; una celda declarada y descartada a la vez se acepta y consta como descartada; ningún caso de batería cubre (a), (b) ni (c). |
| 9 | El vínculo de un derivado no sigue a sus orígenes | **Corregido** | p2 D4 (con el `sellar` real): resellado solo el origen → derivado desactualizado; cadena de dos niveles también; sellar un derivado con un origen sin sellar → rechazado. |
| 10 | `_decimales_exactos` con tolerancia relativa | **Corregido** | p1: los cinco contraejemplos → `False`; 849697000.45 € con cita sin céntimos → discrepancia; con la cita completa → comprobada. |
| 11 | Fuente «local» fuera del expediente | **Corregido** | p1: ruta absoluta, relativa que sale, enlace simbólico hacia fuera y `archivo_texto` absoluto → pendiente; `..` que queda dentro → aceptada. |
| 12 | R1 en datos de texto y fuentes no textuales | **Parcialmente** | p1: cita vacía → pendiente; cita sin el valor → discrepancia ✔. **No corregido:** p1b: «PDF» de bytes ajenos + `archivo_texto` con su huella → comprobada (nada vincula el texto con el PDF). Menor: «EUR» vale dentro de «NEURROS» (subcadena). |
| 13 | `calcular_entrada`: redondeo, errores, componentes | **Corregido, con un residuo trivial** | p4 §1: redondeo < 3, no entero, años repetidos o no enteros → `ValueError`; con carpeta, fuente inexistente, página 99999 o errata ×10 → `ValueError`. Residuo: un componente que no es objeto lanza `AttributeError` (no lo captura `construir`); años desordenados dan «periodo 2025–2024». Límite: 150,8 (la otra columna de la misma cita) se acepta. |
| 14 | Trazabilidad de «Configuración V6.4» fuera del vínculo | **Corregido** | p6: 0 de 321 celdas sin evidencia en el vínculo (antes 29); cambiar B12/B13 → B11 desactualizada; las 9 celdas de metadatos invalidan alguna comprobación. |
| 15 | Un `sellar` rechazado reescribe el registro | **Corregido** | p2 D9: API y CLI, archivo idéntico y formato 4.14 conservado. |
| 16 | «330 de 232» con ficha anterior | **Corregido** | p10: «ficha anterior a la corrección del recuento: sin recuento del universo». La línea sigue diciendo «apta por entradas: sí» (dato de la ficha guardada) hasta la regeneración. |
| 17 | Huella sensible a la forma | **Corregido** | p2 D5: 849697/849697.0, NFD, espacio final y doble espacio → misma huella. Siguen distintas página `"22"`/`22` y signo `1`/`"+1"` (sentido seguro). |
| 18 | Falsos rechazos de formato | **Corregido** | p1: «849 697.0», «1 234 567.89», «45'479.209», «149,5000000», sha256 en mayúsculas. No acepta el apóstrofo tipográfico «’». |
| 19 | Pruebas que no prueban su rótulo | **Parcialmente (como se declara)** | Corregidos (a), (b), (c), (e), (f: casos 7 y 8). Queda (d): el fixture sigue editando `fase1_v63.json`. Nuevo: la prueba (h17) termina en `… or huella(e0) == huella(e1)`, así que no prueba «ni un espacio final». |
| 21 | `comprobar` lanza con registros mal formados | **Corregido** | p6: 21 registros o declaraciones mal formados, ninguna excepción. |
| 22 | Rama H1 de `rellenar` sin registro | **Corregido** | p4 §2: C48 108 frente a 55,233 queda en `entradas_migradas_distintas`; con `--estricta`, rc 7 sin libro. |

Observación 20 (cero con guion, «1.234» ambiguo, signo impreso): sin cambios; no se declaraba corregida.

## 3. Hallazgos nuevos o residuales

### Importantes

**N1 · I8 se puede vaciar con `material: false` en las entradas de juicio (residuo del 1).**
- **[Hecho]** p1: las 88 entradas de juicio con dato, con `material: false`, `justificacion_materialidad: "x"`, fuente ausente, comprobación pendiente y sin revisor → `apto=True comprobadas=233/321 pend=88 no_mat=88`, `motivo: None`. El informe no imprime el recuento de no materiales (`informe.py` solo añade las lecturas externas).
- **[Interpretación]** Es «dejar fuera una cifra usada en la conclusión» por otra etiqueta; el encargo §4 lo excluye. La justificación no la revisa nadie.
- **[Propuesta]** Exigir revisor independiente y vínculo vigente para una entrada no material; contar las no materiales en `motivo` y en la línea del informe aunque el registro sea apto; caso negativo en la batería.

**N2 · El reetiquetado indirecto no se lista ni se justifica (residuo del 2).**
- **[Hecho]** p1b: 156 datos de cálculo como `derivado` de `aux:cN` de clase `convencion` (sin fuente, sin `justificacion_clase`, sin revisor en el auxiliar) → `apto=True 321/321`, `datos_como_hipotesis: 0`. Un derivado con fórmula constante que no usa su origen → comprobada. Sin revisor en el derivado, no apto. Los tres registros reales no usan auxiliares de hipótesis o convención (p7); sí tienen 2–3 ceros de cálculo como `no_aplicable` (`Historia!C23:E23`).
- **[Propuesta]** Tratar como dato presentado como hipótesis un derivado de celda «dato» con algún origen `aux:` de clase hipótesis/convención (justificación, revisor, lista); exigir que la fórmula use todos sus orígenes; `no_aplicable` con un cero numérico, solo con fuente o listado aparte.

**N6 · La documentación del árbol congelado no refleja las correcciones y afirma hechos que el propio árbol contradice.**
- **[Hecho]** `HITO_1_4_15.md`: §3 dice «232/232, 226/226 y 193/193 … sin errores, discrepancias ni pendientes»; el JSON que cita, y la reproducción p7, dan **219/232, 213/226 y 181/193**, con 1/4/1 errores y 12/9/11 discrepancias (tipos impositivos de la fila 10 de la Historia redondeados a 4 decimales sin `round` declarado; moneda y norma cuya cita no contiene el texto; `J4` como convención sin justificación; Vidrala C49, C50 y H23; C48 y C50 no reproducibles). §4: «No hay ninguna vía para actualizar las huellas en bloque» (el docstring ya declara lo contrario) y no menciona la fecha del día ni lo que cubre ahora la huella. §5: 76/76/86 celdas de juicio (son 89/85/99). §6: no describe `--estricta`, presenta el código 7 solo como «intento descartado», la tabla tiene 6 casos (hay 8) y da a Vidrala «vía generativa: sí» (el caso 6 dice `reproduce_por_via_generativa: false` por C50). §8: 46/46 y 21/21, «mínimos 46 y 21» (`verificar_paquete.sh` exige 71 y 27). §11: 8 archivos cambiados, sin `pipeline.py`. `CONTINUIDAD.md` §1 repite 46 y 21.
- **[Propuesta]** Actualizar ambos documentos antes de publicar el hito; es la corrección más barata y la que antes vería un revisor externo.

**N7 · El modo estricto existe, pero nada lo activa.**
- **[Hecho]** `rellenar --estricta` funciona (p4 §4: Elis rc 7 por C48, Vidrala rc 7 por C50, Viscofan rc 0; sin libro escrito). Pero `"entrada_efectiva": "estricta"` no aparece en ningún expediente, CAMBIO ni plantilla del árbol (búsqueda en todo el árbol: solo lo leen `pipeline.py` y el docstring de `rellenar`). `alcance_v2.json` solo es válido con `tipo = ensayo_exploratorio`, aviso y fuente (`cierre_v2.alcance`), así que un expediente ordinario no puede declararlo. Si el archivo falta o es ilegible, el pipeline sigue en modo no estricto. Ninguna batería prueba el paso del argumento por el pipeline.
- **[Interpretación]** «Como en los expedientes nuevos de la 4.15» es hoy una intención, no un hecho.
- **[Propuesta]** Declararlo en el CAMBIO de Elis 4.15 y en lo que cree expedientes nuevos (o hacerlo valor por defecto con exclusión expresa para la línea de base v2.2); sacar la clave de un archivo que solo existe en ensayos exploratorios; un caso de batería del pipeline.

### Menores

- **N3 · `sellar(..., hoy=…)`.** **[Hecho]** p2 D1c: `VE.sellar(cs, celdas, "revisor sintético", "2026-11-14", hoy="2026-11-14")` → 321 selladas, `apto=True` (queda `sellado_en` con la hora real). Nadie usa el parámetro (ni la CLI ni las baterías). **[Propuesta]** Quitarlo.
- **N4 · Redondeo a 3 decimales en derivados de cualquier magnitud.** **[Hecho]** `_igual_libro(r, vm)` se aplica a todo derivado (línea 676); p1: ratio 0,887 = `o["aux:ratio"]` con 0,8874 → comprobada. Con valores del libro de 4 decimales no pasa (0,03354 frente a 0,0335 → discrepancia). **[Interpretación]** Error máximo 0,05 pp; «solo para importes» es cierto para `dato_publicado`, no para derivados. **[Propuesta]** Decirlo en el docstring o exigir `round` en la fórmula cuando el derivado no es un importe.
- **N5 · Residuos de `cambiar_base`** (tabla, fila 8). **[Propuesta]** `construido_historia.get(celda)` cuando la construcción de diagnóstico terminó bien; listar heredadas y motivos en `cambio_de_base.json/.md`; rechazar motivo vacío y celdas en dos listas; tres casos de batería.
- **N8 · `sellar` no puede sellar una lectura externa de un auxiliar.** **[Hecho]** p2 D10: `aux:ext` → «no pasa los controles automáticos (estado True)»; causa: `x.split(":")[0]` sobre «aux:ext: …» da «aux» (línea 828). Falla en el sentido seguro; el motivo impreso no informa. **[Propuesta]** Cortar por `": "` o guardar las claves aparte.
- **N9 · Mensajes.** **[Hecho]** «la fórmula da 0.1009 y el modelo 0.1009» (diagnóstico real, `Historia!L10`: `:g` oculta la diferencia); «el texto de la fuente … no existe» para un `archivo_texto` que existe fuera del paquete. **[Propuesta]** Usar `repr` y distinguir «fuera de lo conservado».

## 4. ¿Introducen las correcciones defectos nuevos?

- **[Hecho]** No se ha encontrado ninguno que acepte lo que antes se rechazaba. Los nuevos son N3 (parámetro sin uso que anula el control de fecha desde Python), N8 (falso rechazo), la prueba (h17) vacua y N6 (documentación desfasada). N7 es una corrección sin conectar.
- **[Hecho]** Las reglas nuevas son más estrictas con los registros reales (219/232, 213/226, 181/193 con vínculo simulado): es la dirección segura y obliga a declarar `round(…, 4)`, `equivalencia` y `justificacion_clase` al regenerarlos.
- **[Hecho, proceso]** Esta vez la ronda completa corre sobre una copia del mismo árbol congelado; a las 14:10 de hoy había pasado las dos baterías nuevas y estaba en la integración V6.4. Su resultado no forma parte de esta revisión.

## 5. Veredicto y §3

**ACEPTABLE CON CORRECCIONES.**

- **[Hecho]** De los nueve hallazgos importantes, cinco están corregidos (3 con límite declarado, 4, 6, 7, 9) y cuatro lo están en parte (1, 2, 5, 8). De los menores declarados, corregidos 10, 11, 13, 14, 15, 16, 17, 18, 21 y 22; parciales 12 y 19.
- **[Interpretación]** Ningún residuo es bloqueante: los contraejemplos directos de la primera pasada ya no pasan y todos los residuos exigen una declaración expresa en un registro que es material auditado. Antes de publicar el hito conviene, por este orden: N6 (documentación), N1 y N2 (dos variantes de una línea que devuelven «apto»), N7 y N3. N4, N5, N8, N9 y el resto del 12 pueden ir al hito siguiente si se declaran.
- **§3 del encargo:** **puede declararse cumplido con matices**, no sin ellos.
  - **[Hecho]** Cumplido: la vía generativa reconstruye C48 = 108,0 desde su cálculo declarado, con componentes contrastados con su página y su cita y herencia de H1; el conflicto con el valor migrado ya no es silencioso en ningún caso probado, incluido el de la celda sin declarar (Vidrala C50); el control bloquea siempre; la reconstrucción leída reproduce la sensibilidad del encargo (7,3020553231 → 8,9801824507, +1,6781271276) y, con el CAMBIO 4.15, da C48 = 108 y el mismo precio con y sin valores migrados, sin diferencias de datos, fórmulas ni resultados.
  - **[Interpretación] Matices que hay que escribir:** (1) fuera del modo estricto la consecuencia es «no apto por entradas», no una parada, y el modo estricto no está activado en ningún expediente (N7); (2) en los casos 3 y 4 la herramienta marca `reproduce: false` y código 1 por las celdas de fecha y de evidencia documental, clasificadas pero no excluidas; la prueba con `reproduce: true` y código 0 solo existirá con el expediente de Elis regenerado (hito siguiente), porque la referencia de hoy es un expediente ensamblado; (3) la reconstrucción se ha leído, no repetido, en esta revisión.

## 6. Resumen en 10 líneas

1. Las tres baterías pasan en la copia del árbol congelado: 71/71, 27/27 y 33/33; la de la 4.14 no se ha rebajado.
2. Corregidos sin reservas: 4, 6, 7, 9, 10, 11, 14, 15, 16, 17, 18, 21 y 22; el 13, con un residuo trivial.
3. El 3 está corregido en lo exigible (fecha del día, controles, orden `huella` retirada) con el límite declarado; sobra el parámetro `hoy`.
4. Parciales: 1 (juicio no material sin revisor), 2 (reetiquetado indirecto por un auxiliar o una fórmula constante), 5 (derivados), 8, 12 y 19.
5. N1: 88 entradas de juicio con `material: false` y justificación «x» dan `apto=True` sin revisor: I8 se puede vaciar.
6. N2: 156 datos de cálculo como derivados de un auxiliar «convención» dan `apto=True` sin fuente y sin aparecer en la lista nueva.
7. N6: `HITO_1_4_15.md` y `CONTINUIDAD.md` están desfasados; dicen 232/232 sin discrepancias donde el árbol da 219/232 con 12, y 46/21 pruebas donde hay 71/27.
8. N7: `--estricta` funciona, pero ningún expediente lo declara y solo cabe en un `alcance_v2.json` de ensayo exploratorio.
9. No se ha encontrado ninguna regresión que acepte lo que antes se rechazaba; las reglas nuevas dejan los tres registros reales en no apto, como se declara.
10. Veredicto: ACEPTABLE CON CORRECCIONES; §3 cumplido con tres matices (etiqueta y no parada fuera del modo estricto, `reproduce: false` formal en los casos 3 y 4, reconstrucción leída y no repetida).
