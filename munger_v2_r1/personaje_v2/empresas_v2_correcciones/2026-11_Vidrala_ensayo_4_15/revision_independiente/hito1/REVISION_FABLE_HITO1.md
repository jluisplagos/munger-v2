# Revisión independiente del hito 1 de la 4.15 (R1–R3, C48, I13, I8, I9)

Revisor: Fable (Claude, contexto separado del de la implementación; no es una revisión humana) · 15-nov-2026.
Convención del informe: **[Hecho]** = comprobado por el revisor ejecutando o leyendo el código (se dice cuál); **[Interpretación]** = lectura del revisor; **[Propuesta]** = corrección sugerida. Lo que no se ha ejecutado se dice expresamente.

## 0. Qué se ha revisado y cómo

- Encargo: `ENCARGO_CORRECTIVO.txt` §2 (R1–R3), §3 (C48), §4 (I13, I8, I9).
- Árbol revisado: `/home/claude/w/trabajo/munger_v2_r1`, **sin modificarlo**: todo se ejecutó en copias (`/tmp/rev_fable/…`). Árbol 4.14 de comparación: `/home/claude/w/base_4_14/munger_v2_r1`.
- **[Hecho]** El árbol cambió durante la revisión. El diff entregado (`diff_hito1_frente_4_14.diff`) quedó desfasado a las 12:41 (aviso de la coordinación: el código 7 de `rellenar_fase1_v63.py` se sustituyó por el registro «entradas_migradas_distintas» más `verificacion_entradas.entradas_no_reproducibles()`). La revisión se rehízo sobre la instantánea de las **12:44** (copia `/tmp/rev_fable/trabajo_copia`). Huellas SHA-256 de esa instantánea:

| Archivo | SHA-256 |
|---|---|
| personaje_v2/scripts/verificacion_entradas.py | 32cddaf9762836aa1bf30b3c4da0a4bde60f04d3d3835ad8e8b4797ba7e37326 |
| personaje_v2/scripts/rellenar_fase1_v63.py | e5a9afb3b0c65b4d18dfc3a5e54712e39e97eb30273aa771632a09fc906a20e3 |
| personaje_v2/scripts/fase1_historia.py | 86f3492fd9864bd013b1ba998042ea48bc59db3d973ee72cd5c354ad03567bca |
| personaje_v2/scripts/cambiar_base.py | a87aec9e9f9481bcd65439d7368c88957163223669b6dbe856ab18967345c0e5 |
| personaje_v2/scripts/informe.py | a5677e3fcec559f693d069efafb5cdeaee2de586ba3415cb3f13e6abaadba278 |
| personaje_v2/pruebas/test_verificacion_entradas_415.py | a6228a2faba2698e63a2a6603731944880526acc15320e6d2658487d138bed24 |
| personaje_v2/pruebas/test_entrada_efectiva_415.py | 02bc864a06d614036eac8d377a06995ab1e9651d081540ee869f02b64bc15690 |
| personaje_v2/pruebas/test_verificacion_entradas_414.py | f6e38b044c8bf9c4277b043af0478c5025203a965bdbce018c8c44e6f9fe8d24 |
| verificar_paquete.sh | 3d4645573a1225bdbe76b1763a4040a4501600ef4c62a352da9e6869f3a5939e |

  Los números de línea que se citan sin nombre de archivo son de `verificacion_entradas.py` en esa instantánea.
- **[Hecho]** Cambios posteriores a esa instantánea, vistos pero **no revisados a fondo**: `ficha.py`, `informe.py`, `resumen.py`, `alcance_modelo.py`, `test_relevo_caducado_415.py`, `test_alcance_aptitud_415.py` (entre las 12:56 y las 13:09; I19, I20, F1: fuera del alcance pedido) y, a las 13:07, una adición de `control_maestro_textos` en `fase1_historia.py` y `cambiar_base.py` (leída: paso de textos declarativos; no cambia la lógica revisada). `pipeline.py` (I19) tampoco se ha revisado. `verificacion_entradas.py`, `rellenar_fase1_v63.py` y las tres baterías no han cambiado desde las 12:44 (comprobado a las 13:09).
- **No ejecutado** (por indicación: LibreOffice estaba en uso por otra ejecución): `verificar_paquete.sh`, `test_integracion_v64.py`, la batería sintética y la reconstrucción de C48 (`prueba_reconstruccion_c48_4_15.py`). De la reconstrucción solo se han **leído** los resultados que la coordinación regeneró a las 12:50–12:53.
- Reproducciones del revisor: `revision_hito1/reproducciones_fable/` (arnés `fx.py`, copia del fixture de la batería 415, y sondas `p1`…`p10`); sus salidas literales están en `reproducciones_fable/salidas/*.log`. Uso: `cd revision_hito1/reproducciones_fable && PV=<copia del árbol>/personaje_v2 python3 -B p1_r123.py` (p5 usa además `V2=<copia del árbol>` y `B14=<copia del árbol 4.14>`). Todas trabajan en carpetas temporales y no escriben en `PV`.

## 1. Veredicto

**ACEPTABLE CON CORRECCIONES.**

- **[Hecho]** Los tres contraejemplos de la revisión externa (R1 página «999999», R2 fuente local ausente con `sha256 = None`, R3 redondeo aceptado como cifra exacta) ya no pasan; las tres baterías pasan; la batería de la 4.14 conserva sus 33 casos sin rebajar; el vínculo de I13 detecta cambios de fundamento, evidencia y transformación con el mismo número; el universo incluye 76–86 celdas de juicio sin tocar la huella de cálculo; C48 de Elis se reconstruye (108,0) desde su cálculo declarado.
- **[Interpretación]** Ningún hallazgo es bloqueante: no se ha encontrado ningún defecto que invalide lo anterior. Sí hay nueve hallazgos **importantes** (1–9), diez menores (10–19) y seis observaciones (20–25). Los importantes, en una frase: con variaciones de una línea de los mismos contraejemplos el comprobador vuelve a decir «apto» sin deber (1, 2, 5); `sellar` permite legitimar en bloque la revisión de la 4.14 (3); el control nuevo de la entrada efectiva falla en abierto, también en un caso real, Vidrala C50 (4); el universo de juicio no incluye el reparto geográfico (6); un cálculo declarado se salta H1 (7); `cambiar_base` pierde tres comportamientos (8); y el vínculo de un derivado no sigue a sus orígenes (9).
- **[Interpretación]** Tres de ellos (1, 2 y 5) y parte del 3 son palancas que ya existían en la 4.14 y que el cambio no introduce, pero dejan sin efecto práctico parte de R1–R3 y son lo primero que encontraría quien repita los contraejemplos externos con una variación; conviene corregirlos, o declararlos como límite expreso, antes de presentar el hito como cumplimiento de §2–§4. Orden sugerido: 1, 2, 3 y 4 (correcciones pequeñas y ligadas al texto del encargo); después 5 a 9.
- **[Interpretación]** El hito no debería describir §3 como cumplido sin matices (apartado 5).

## 2. Baterías ejecutadas por el revisor (sin LibreOffice)

**[Hecho]** `cd personaje_v2/pruebas && python3 -B <archivo>`, en copia:

| Batería | Instantánea 12:44 | Instantánea 13:09 (con los cambios posteriores de ficha/informe) |
|---|---|---|
| test_verificacion_entradas_415.py | 46/46 PASAN (rc 0) | 46/46 PASAN (rc 0) |
| test_entrada_efectiva_415.py | 21/21 PASAN (rc 0) | 21/21 PASAN (rc 0) |
| test_verificacion_entradas_414.py | 33/33 PASAN (rc 0) | 33/33 PASAN (rc 0) |

Sobre la versión del diff entregado (antes de las 12:41) dieron 44/44, 20/20 y 33/33. Salidas en `salidas/bateria_*.log`.

**[Hecho] La batería de la 4.14 no se ha rebajado.** Comparada línea a línea con la del árbol 4.14 (SHA f2345a23…): las 34 llamadas a `paso(...)` y sus condiciones son idénticas salvo el rótulo del control positivo (muestra `comprobadas_universo`); las 30 llamadas `r = con(...)` son idénticas salvo dos casos **positivos** que ahora se sellan de nuevo (`resellar=True`: perímetro justificado y cifra en formato francés). El resto del diff es el fixture: `sha256` de la fuente sintética, vínculo en cada entrada, y la alineación de la copia de `fase1_v63.json` (véanse los hallazgos 4 y 19).

## 3. Respuesta breve a las seis preguntas

1. **Contraejemplos que aún pasan como «apto»:** sí; hallazgos 1, 2, 5, 10, 11, 12 (y 3, 4, 9 para I13 y C48).
2. **Falsos rechazos:** pocos y menores (hallazgo 18). Los tres registros reales de la 4.14 no tienen ninguno en el universo de cálculo (hallazgo 3, salida de `p7`).
3. **I13:** el vínculo cubre clase, materialidad, valor, fuente, derivación, hipótesis, justificación y la fila del Control maestro. No cubre los orígenes de un derivado (9), la trazabilidad de las celdas de «Configuración V6.4» (14) ni los campos de la propia comprobación (3). Una revisión antigua **sí** se puede legitimar: con `sellar` y fecha retroactiva, escribiendo la huella a mano o con la orden `huella` (3). La huella es estable frente al orden de claves y a la ida y vuelta por JSON; no frente a 849697 ↔ 849697.0, NFC ↔ NFD o un espacio (17; falla en el sentido seguro).
4. **I8:** las fórmulas se excluyen bien y la huella de cálculo no cambia (igual a `EE.instantanea` en los tres libros finales y en el fixture). El universo de juicio está incompleto: falta el reparto geográfico (Palancas A28:B33), que fija la r mínima que se da a la fase A (6).
5. **C48:** `calcular_entrada` da 108,0 sin que el redondeo oculte nada en el caso de Elis; tiene defectos de borde (7, 13). El diseño vigente (sin código 7) deja de ser silencioso solo en parte (4 y apartado 5). `cambiar_base` pierde compatibilidad en tres puntos (8).
6. **Pruebas:** las antiguas no se han rebajado; varias nuevas no prueban lo que su rótulo dice (19).

## 4. Hallazgos

### Importantes

#### 1 · `material: false` deja sin efecto R1, R2 y el control de la entrada efectiva, sin intervención de ningún revisor *(palanca de la 4.14; no la introduce el cambio)*

- **[Hecho]** `python3 -B p1_r123.py` y `p6_varios.py`:
```
[R2 fuente local AUSENTE + material:false (sin revisor ni sello)] apto=True comprobadas=307/308 pend=1 … | pendientes: Historia!F6: la fuente local 'fuentes_sinteticas/NO_EXISTE.txt' no está en el expediente ni en el paquete…
[R1 página no inequívoca + material:false (sin revisor ni sello)] apto=True comprobadas=307/308 pend=1 …
[R2 TODOS los datos publicados (246) con fuente ausente y material:false] apto=True comprobadas=62/308 pend=246 desact=0 discr=0 err=0 mat_no=0 ext=0
```
  y, en `p6_varios.py`, con las cuatro entradas C47–C50 que la vía generativa no reproduce (copia de Viscofan 4.13 con su `fase1_v63.json` original):
```
[registro comprobado] apto=False comprobadas=304/308 pend=0 desact=0 discr=4 err=0 mat_no=4 ext=0
[las mismas entradas con material:false y la comprobación pendiente (sin revisor)] apto=True comprobadas=304/308 pend=4 desact=0 discr=0 err=0 mat_no=0 ext=0
   entradas_no_reproducibles: 4 | discrepancias: []
```
  Es el contraejemplo R2 de la revisión externa con un campo más (`"material": false`) en una entrada del universo de **cálculo** (ventas de 2019). Causa: `mat_no` (línea 575) solo cuenta las entradas con `material` distinto de `False`, y los estados nuevos de R1/R2 son «pendiente», que solo bloquea si la entrada es material. El vínculo no llega a evaluarse (el control documental devuelve «pendiente» antes), así que el cambio de `material` no exige sello.
- **[Interpretación]** La entrada no se acredita (queda pendiente), pero el expediente sale «apto por entradas»; por el formato de la línea del informe, saldría «62 de 308 … 0 materiales sin comprobar … apta por entradas: sí» (el informe no se ha ejecutado en ese estado). Las celdas de la instantánea de cálculo son, por definición de su relación, entradas materiales. Los tres registros reales tienen `material: true` en todas las entradas: hoy no se usa, pero nada lo impide.
- **[Propuesta]** (a) En el ámbito de cálculo no admitir `material: false` salvo que la entrada esté inactiva para el motor del libro (`relacion_entradas_materiales.activas`); (b) en el de juicio, exigir justificación y revisor, y evaluar el vínculo también en las entradas no materiales; (c) contar y listar las no materiales en `motivo`, ficha e informe; (d) prueba negativa: el contraejemplo R2 con `material: false`.

#### 2 · Un dato reetiquetado como convención, hipótesis o «no aplicable» se libra de R1–R3 *(control de un solo sentido de la 4.14)*

- **[Hecho]** `p1_r123.py`:
```
[dato de cálculo (ventas 2019) reetiquetado como CONVENCIÓN, sin fuente] apto=True comprobadas=308/308 …
[ídem sin revisor ni resultado (vínculo calculado a mano)] apto=True comprobadas=308/308 …
[dato de cálculo con valor reetiquetado como NO_APLICABLE] apto=True comprobadas=308/308 …
[TODOS los datos publicados (246) reetiquetados como convención sin fuente ni revisor] apto=True comprobadas=308/308 pend=0 desact=0 discr=0 err=0
```
  El código rechaza una hipótesis presentada como dato (línea 420), pero no un dato (tipo «dato» de la relación) presentado como hipótesis o convención; `no_aplicable` solo pide justificación aunque la celda tenga valor (línea 513).
- **[Hecho]** Se usa en un registro real: en `vidrala_decisiones` (4.14), `Análisis!C49 = 4,5` y `Análisis!C50 = 0` (entradas del FCF base, tipo «dato») están registradas con clase `hipotesis`; el propio revisor R-Vidrala anotó en `incidencia`: «hipótesis que es, en la práctica, un derivado de datos publicados». También `Historia!H23 = 0` como convención.
- **[Interpretación]** Puede ser legítimo en casos concretos (la unidad «mm» es una convención), pero hoy es una vía general para que una cifra del cálculo no tenga contraste documental y cuente como comprobada, sin revisor.
- **[Propuesta]** Para celdas de tipo «dato»: admitir `hipotesis`/`convencion` solo con una justificación de clase y revisor independiente, y mostrarlas aparte en `comprobar`, ficha e informe («datos del modelo tratados como hipótesis o convención: N»); `no_aplicable` con valor numérico distinto de vacío, solo si la relación la da por inactiva para el motor. Prueba negativa correspondiente.

#### 3 · `sellar` legitima en bloque una revisión anterior con una fecha retroactiva; el vínculo también se puede escribir a mano

- **[Hecho]** `p2_i13.py` (D1): registro en formato 4.14, revisado «el 14-nov»; después se cambian el fundamento de una hipótesis y el documento, el concepto y el tratamiento de un dato; una sola orden:
```
antes de sellar: apto=False comprobadas=0/308 pend=308
CLI sellar (una sola orden, 308 celdas, --fecha 2026-11-14): ['selladas 308 · rechazadas 0'] rc 0
después de sellar: apto=True comprobadas=308/308 pend=0 desact=0 discr=0 err=0
```
- **[Hecho]** Con los registros reales de la 4.14 (copias), `p7_sellar_real.py`, usando los nombres de revisor y la fecha que ya constan en ellos:
```
== viscofan_decisiones/Viscofan · registro formato 4.14 · 330 entradas · antes: comprobadas 0 de 308 (cálculo 0 de 232)
   sellar --revisor «revisor independiente R-Viscofan…» --fecha 2026-11-14 (302 celdas): selladas 302 · rechazadas 0   [y 9, 18 y 1 con los otros tres revisores]
   después: comprobadas 232 de 308 (cálculo 232 de 232; juicio 0 de 76) · … discrepancias 0 · errores 0 · sin entrada 76
== vidrala_decisiones/Vidrala · … 347 entradas … [335, 5 y 7 celdas: selladas todas, rechazadas 0]
   después: comprobadas 226 de 302 (cálculo 226 de 226; juicio 0 de 76) · … discrepancias 0 · errores 0 · sin entrada 76
== elis_decisiones/Elis · … 330 entradas … [299 y 31 celdas: selladas todas, rechazadas 0]
   después: comprobadas 192 de 279 (cálculo 192 de 193; juicio 0 de 86) · … discrepancias 1 [C48 no reproducible] · sin entrada 86
```
  Es decir: 1.007 comprobaciones de la 4.14 quedan vinculadas al fundamento de hoy con nueve órdenes y ninguna revisión; solo las celdas de juicio sin entrada impiden la aptitud.
- **[Hecho]** Otras vías (`p2_i13.py` D2, D3; `p9_cli_huella.py`): un vínculo `{"huella": huella_fundamento(...)}` escrito por un script en las 308 entradas da `apto=True` (es lo que hacen los fixtures de las dos baterías y el diagnóstico de la orquestación `/home/claude/w/scripts_orq/diagnostico_r1_r3_reales.py`, que lo llama «vínculo SIMULADO»); la orden `verificacion_entradas.py huella <expediente> <celda>` imprime la huella y pegarla devuelve la entrada a «comprobada»; después del sello se pueden cambiar `revisor`, `fecha`, `fuente_examinada`, `nota`, `incidencia` y los propios `vinculo.sellado_por`/`vinculo.fecha` sin perder la vigencia. `comprobar` solo compara `vinculo.huella`.
- **[Interpretación]** La condición «la fecha de la comprobación es la de esta revisión» (línea 642) compara dos valores que da quien llama; no hay reloj ni límite de celdas. El docstring («nunca en bloque para legitimar una revisión anterior», «sellar no … legitima una revisión anterior») y el rótulo de la prueba V («sella solo la revisada por ese revisor hoy») afirman una garantía que el código no da. El encargo pide no actualizar las huellas para legitimar una revisión antigua: la herramienta no lo hace sola, pero lo permite con una orden. Un registro JSON no puede impedir la escritura manual; lo exigible es que la herramienta no lo facilite, que lo que afirma sea cierto y que el rastro quede.
- **[Hecho favorable]** La coordinación no ha sellado los registros reales: con el código vigente los tres dan 0 comprobadas.
- **[Propuesta]** (a) `sellar` exige que `--fecha` sea la fecha del sistema y registra `sellado_en` (marca de tiempo); una comprobación fechada antes no se sella (hay que revisarla y fecharla de nuevo); (b) incluir en la huella `revisor`, `fecha`, `resultado` y `fuente_examinada`, y que `comprobar` exija `vinculo.sellado_por == comprobacion.revisor` y `vinculo.fecha == comprobacion.fecha`; (c) negarse a sellar una entrada que no pasa sus controles automáticos; (d) retirar la orden `huella` o dejarla como diagnóstico que no imprime la huella completa; (e) corregir docstring y prueba: el vínculo detecta cambios, no acredita quién lo escribió (eso lo cubre la auditoría del registro como material).

#### 4 · `entradas_no_reproducibles` falla en abierto; caso real: Vidrala C50

- **[Hecho]** `p4_c48.py` (apartado 3; copias de `elis_decisiones` y `vidrala_decisiones`) y, las dos últimas líneas, `p6_varios.py` (fixture con el registro comprobado):
```
Elis 4.14 tal cual: {'Análisis!C48': (108, 82.933)}
(a) sin fase1_v63.json en la carpeta: {}
(b) fase1_v63.json ilegible: {}
(c) fase1_v63.json sin declarar C48 (el libro sigue con 108 migrado): {}
(d) fase1_v63.json editado a mano: C48.valor = 108 (sin cálculo, con la fuente de la media 82,933): {}
(e) valor declarado como texto «82.933»: {}
(f) Vidrala final 4.14 (dato real): libro C50 = 0 | base C50 = 0 | fase1_v63.json declara C50: False | entradas_no_reproducibles: {}
    Vidrala reconstruida sin los valores migrados del FCF base: rc 0 → {…'C50': None} | libro final: {…'C50': 0}
    rellenar sobre la base de Vidrala (C50 = 0 migrado, sin declarar): rc 0 | entradas_migradas_distintas: None | avisos sobre C50: [] | no_pisadas C50: []
[sin fase1_v63.json en la carpeta] apto=True comprobadas=308/308 pend=0 desact=0 discr=0 err=0 mat_no=0 ext=0      (el mismo expediente daba 4 discrepancias)
[fase1_v63.json = [] (JSON válido, no un objeto)] comprobar LANZA AttributeError 'list' object has no attribute 'get'
```
- **[Interpretación]** (c)/(f) es el caso más puro de «valor protegido solo porque la celda ya lo tenía»: la vía generativa no declara nada y ni `rellenar` (no llama a `poner`) ni `comprobar` (`_num(vf)` falso) lo ven. En Vidrala es real (C50 = 0 lo sostiene únicamente la etapa 1; el registro lo trata como hipótesis), aunque no mueve su valoración (motor B). (a) permite que desaparezca la discrepancia borrando un archivo. (d) es exactamente lo que hacen los fixtures de las baterías 414 y 415 («declara en su copia el valor efectivo del libro»): el control compara con un archivo intermedio editable, no con lo que `construir` produce desde las entradas declaradas, y ni `fase1_v63.json` ni `fase1_metadatos.json` están en `cierre_v2.MATERIAL_FIJO` (comprobado) ni su huella en el registro. Además la conversión a discrepancia solo ocurre si la entrada estaba «comprobada» (línea 563), de modo que con `material: false` no bloquea (hallazgo 1).
- **[Propuesta]** (a) Tratar como no reproducible «libro con valor y celda sin declarar o declarada no numérica» y como no determinable (pendiente que bloquea) «sin `fase1_v63.json` legible»; capturar también una raíz que no sea objeto; (b) bloquear con independencia del estado de la entrada y de `material`; (c) atar `fase1_v63.json` a sus entradas: que `construir` guarde la huella de `fase1_metadatos.json` y `fase1_partes/` y marque las entradas sustituidas después (cambiar_base), y que `comprobar` la verifique; o incluir `fase1_v63.json` en el material; (d) en los fixtures, declarar el valor con un `calculo` (con `redondeo`) en lugar de editar el número.

#### 5 · La tolerancia absoluta de 0,0011 se aplica a tasas, ratios y probabilidades *(constante de la 4.14; I8 la hace más relevante)*

- **[Hecho]** `TOL_ABS = 0.0011` («3 decimales en mm», línea 84) se usa en `_igual` para todo: vigencia del valor, `signo × escala × valor_fuente`, coherencia de la escala y cero comprobado. `p1_r123.py`:
```
[R3 tasa del libro 0.0335 contrastada con una fuente que publica 3.25 % (0,10 pp menos)] apto=True comprobadas=308/308 … comprobada
[vigencia: registro con g = 0.019 y libro con 0.02] apto=True comprobadas=308/308 … comprobada
[R3/unidades: la misma cifra (miles) declarada en «euros» con escala 0,001] apto=True comprobadas=308/308 … comprobada
```
  y directamente: `VE._igual(0.25, 0.2511)`, `VE._igual(0.001, 0)`, `VE._igual(0.001, 1e-06)`, `VE._igual(0.002, 0.001)` → `True`.
- **[Interpretación]** Es un número distinto aceptado como el mismo sin transformación declarada (el sentido de R3), por otra puerta que `_cifras`: para importes en mm es inmaterial; para tasas (C57), tipos impositivos (Historia fila 10), ratios (C24, C32, C33, C60, C96) y palancas (g, r, probabilidades) son 0,11 puntos porcentuales. El control de unidades no distingue euros de miles. Con I8 entran en el universo precisamente las cifras pequeñas.
- **[Propuesta]** Vigencia del valor: comparación exacta (`EE.iguales`, 1e-9 relativo); producto fuente–modelo: tolerancia ligada al redondeo declarado del libro solo cuando la unidad es un importe, y relativa en lo demás; escala: comparación relativa. Pruebas negativas: 3,25 % frente a 3,35 %; «euros» con escala 0,001.

#### 6 · I8: el universo de juicio no incluye el reparto geográfico, que determina la r mínima que se da a la fase A

- **[Hecho]** `p3_i8.py` (libros finales de la 4.14, solo lectura): fuera del universo y con dato tecleado (no fórmula) están `Palancas!A28:B32` (p. ej. Viscofan: Spain 0,126; Western Europe 0,2836; Asia 0,1362; North America 0,3094; Central and South America 0,1449), `Palancas!C7` (sector de Damodaran), `C45`/`C46` (fechas del precio y de las acciones), `C5`, `C9`. `datos_v63.md` las da a las fases: «Reparto geográfico (Palancas A28:B33): Spain 0.126 (prima 0.0148374)…» y «r mínima (Diagnóstico!C17): 0.0946343 · ⚠ REVISAR · tu r (9.0 %) < r mínima (9.5 %)»; `prompts/fase_a.md` pide a la fase A decir si r está por debajo de la r mínima. `rellenar_fase1_v63.py` escribe esas celdas desde `fase1_v63.json` (`geografia`, con fuente y página).
- **[Hecho]** Lo demás está bien delimitado: de `volcar_datos_v63.DATOS_ANALISIS` solo quedan fuera del universo B3, D3, B4, D4 (identificación) y C52 (fórmula); C59, que también se vuelca, es fórmula; las anclas `Historia!C43:C66` son fórmulas salvo C57 (ya en el cálculo); la huella de cálculo y `n_calculo` coinciden con `EE.instantanea` en los tres libros.
- **[Interpretación]** El reparto geográfico es una cifra financiera publicada por la empresa que el juicio usa (a través de la r mínima) y que el encargo no permite dejar fuera «por llamarla descriptiva». El sector (C7) decide qué cuartiles sectoriales ve el juicio. Las cifras de `extracto_v63.md` también llegan al juicio y quedan fuera de este control (las cubre, si acaso, la verificación de citas): conviene decirlo.
- **[Propuesta]** Añadir al ámbito de juicio `Palancas!A28:B33` (filas con dato), `C7`, `C45` y `C46`; cambiar la prueba J, que hoy solo exige un subconjunto, por la igualdad `DATOS_ANALISIS − universo = {B3, D3, B4, D4, C52}` y un caso para la geografía; documentar la frontera con el extracto.

#### 7 · Un `calculo` declarado no hereda los ceros pendientes de verificación (H1)

- **[Hecho]** `p4_c48.py` (apartados 1 y 2), con la Historia real de Elis (`arrendamientos_principal` 2016–2018 = 0,0 pendientes de verificación):
```
media 2016–2018 de intereses_financiacion − arrendamientos_principal (…PENDIENTES de verificación): valor=55.233
   pendientes de la Historia: {'arrendamientos_principal': [2016, 2017, 2018], 'arrendamientos': [2016, 2017, 2018]} | pendientes_celda('C48'): []
construir: rc 0 …   C48: {'valor': 55.233, 'periodo': '2016–2018'}
rellenar: rc 0 | C48 = 55.233 | Control maestro F45 = Rellenado y verificado | J45 = Cálculo declarado (media 2016–2018 de: …
```
  La propagación de H1 usa el mapa fijo `DEP_ANALISIS` (C48 → `intereses_financiacion`, últimos `anios_fcf_base` años; `fase1_historia.py` línea 540), no los términos ni los años del cálculo.
- **[Interpretación]** El C48 real de Elis (2023–2025) no está afectado. Es un camino nuevo que se salta una garantía existente («nunca Rellenado y verificado» con un cero sin verificar).
- **[Propuesta]** En `construir`, unir a los pendientes de la celda los de las partidas y años que usa su `calculo` (`rellenar` ya respeta `pendiente_verificacion` de la entrada). Prueba con este caso.

#### 8 · `cambiar_base.py`: los descartes dejan de descartar, las entradas se heredan sin declararlas y se pierde el diagnóstico de lo que construye la Historia

- **[Hecho]** `p5_cambiar_base.py` (código vigente con el CAMBIO 4.15, frente al código 4.14 con su CAMBIO; sin LibreOffice):
```
A (código vigente): sustituidas (construido_por_fase1_historia → valor): {'C24': (0.097, 0.097), … 'C47': (857.167, 857.167), …}
   nota de fase1_v63.json: … Entradas sustituidas por cambiar_base.py …: C24 0.097 → 0.097; … C47 857.167 → 857.167 …
old (código 4.14):  sustituidas: {'C24': (None, 0.097), … 'C47': (867.167, 857.167), …}
B (código vigente; origen = A; analisis = {}; descarta C42): rc 0
   C42 en el fase1_v63.json nuevo: 5.53 | registrado como descartado: [{'de': 'fase1_v63.json (analisis del origen descartadas por el CAMBIO)', 'nota': {'C42': …}}]
   entradas heredadas sin declarar en el CAMBIO B: {'C24': 0.097, …, 'C46': 1429.433, 'C47': 857.167, 'C50': 28.233, 'C48': 108.0, 'C49': 128.1}
B2 (código 4.14; origen = old; analisis = {}; descarta C42): rc 1 | PREPARACIÓN DETENIDA: el CAMBIO perdería entradas `analisis` del origen que no declara ni descarta …
```
- **[Interpretación]** Al persistir `analisis` en `fase1_metadatos.json` (correcto para la reconstrucción): (a) `analisis_que_se_descartan` ya no retira una entrada persistida por un cambio anterior, y `notas_retiradas.json` la da por descartada; (b) un cambio de base posterior hereda en silencio constantes declaradas para la base anterior (p. ej. «media 2023–2025»), y el guardián de la 4.14, que obligaba a declararlas o descartarlas, deja de actuar; (c) `construido_por_fase1_historia` y la nota de `fase1_v63.json` ya no dicen qué daría la Historia (antes: C47 867,167 → 857,167), que es el diagnóstico que pide §3.
- **[Propuesta]** (a) Quitar de `meta["analisis"]` las celdas descartadas y comprobar que no están en el `fase1_v63.json` nuevo; (b) listar las entradas heredadas en `cambio_de_base.json/.md` y exigir que el CAMBIO las reconozca (p. ej. `analisis_que_se_conservan`); (c) conservar el valor que construiría la Historia (cálculo aparte) en el registro; (d) un caso de batería para cada punto. `comprobar` de `cambiar_base` se ha leído y es coherente con el cálculo declarado; no se ha ejecutado.

#### 9 · El vínculo de un derivado no incluye el de sus orígenes

- **[Hecho]** `p2_i13.py` (D4):
```
[el origen aux:a cambia de documento, concepto, página y cita (mismo número), sin nueva revisión] apto=False … pendientes: …: el origen aux:a no está comprobado (desactualizada)
[se revisa y se sella de nuevo SOLO el origen: el derivado, sin revisar, vuelve a valer] apto=True comprobadas=308/308 … comprobada
```
- **[Interpretación]** Mientras el origen está desactualizado el derivado queda pendiente (bien). Una vez resellado el origen, la comprobación antigua del derivado revive sin que nadie haya revisado si la derivación sigue valiendo con la evidencia nueva: es el caso que I13 describe (cambia la evidencia, coincide el número).
- **[Propuesta]** Incluir en la huella del derivado las huellas vigentes de sus orígenes (recursivamente), al sellar y al comprobar.

### Menores

#### 10 · R3: `_decimales_exactos` usa una tolerancia relativa y vuelve a aceptar redondeos en cifras grandes
- **[Hecho]** `VE._cita_contiene("Ingresos: 1.234.567.890", 1234567890.45)`, `("Ingresos: 100.000.000", 100000000.1)`, `("Ingresos: 10.000.000", 10000000.01)`, `("Tasa: 54,7", 54.70000001)` y `("Partida: 0", 4.9e-10)` → `True`. De extremo a extremo (`p1`): `valor_fuente 849697000.45 € con una cita que solo trae 849,697,000 → comprobada`. Además `_cita_contiene("x 0,12345678901", 0.12345678901)` → `False` y `_cita_contiene("x 0,12345679", 0.12345678901)` → `True`: se rechaza la cifra completa y se acepta la redondeada.
- **[Interpretación]** Error relativo ≤ 1e-9: inmaterial, pero es la regla que R3 prohíbe, alcanzable con fuentes en euros.
- **[Propuesta]** Contar los decimales con `decimal.Decimal(repr(x))` en lugar de una tolerancia.

#### 11 · R2: una fuente «local» puede estar fuera del expediente y del paquete
- **[Hecho]** `p1`: `archivo` con ruta absoluta en `/tmp/…` o relativa con `../` que sale del paquete → `apto=True … comprobada`. `_ruta_fuente` (línea 193) no comprueba que la ruta resuelta quede dentro.
- **[Propuesta]** Rechazar rutas absolutas o que salgan de la carpeta del expediente y de `personaje_v2/` (pendiente: «no conservada con el expediente»).

#### 12 · R1 en datos de texto y en fuentes no textuales
- **[Hecho]** `p1`: un dato publicado de texto (`Palancas!C48 = EUR`) con una cita que no contiene el valor, o con una cita de un solo espacio, queda comprobado (el contraste solo exige que la cita esté en la página, y `" "` normalizado es la cadena vacía). Un «PDF» de bytes ajenos con un `archivo_texto` cualquiera y su huella queda comprobado: nada vincula el texto con el PDF (la propia batería usa como PDF una copia del .txt).
- **[Propuesta]** Exigir cita no vacía tras normalizar; para datos de texto, que la cita contenga el valor o una equivalencia declarada; aceptar `archivo_texto` solo si consta como extracción de ese PDF (p. ej. en `fase1_fuentes.json`, con ambas huellas).

#### 13 · `calcular_entrada`: redondeo sin límite, errores no capturados y componentes sin contraste
- **[Hecho]** `p4_c48.py` (apartado 1): con un componente que da una media exacta de 108,3667, `redondeo = 0` devuelve 108,0 y acepta el valor declarado 108; `redondeo = -1` da 110,0; `2.5` se trunca a 2; `redondeo = None` o un año `None` lanzan `TypeError` (no `ValueError`: `construir` termina con traza); años repetidos `[2025, 2025, 2025]` se aceptan y dan 129,0 como «media»; un componente con fuente inexistente, página 99999 y sin cita se acepta; un componente con una errata ×10 da 641,7 sin aviso. En el caso real, la media sin redondear es 108,0.
- **[Interpretación]** No inventa ni redondea en silencio en el caso de Elis; pero el redondeo declarado no tiene límite ni aparece en el texto de la fuente generada, y «no se acepta una cifra sin su fuente» (rótulo de la prueba) solo significa «sin un texto no vacío». El contraste real del componente queda en el registro de entradas (derivado con orígenes `aux:`), que es independiente.
- **[Propuesta]** `redondeo` entero ≥ 3 (o guardar el valor sin redondear y el redondeo en la salida y en la fuente); validar tipos y años distintos; contrastar cada componente con su fuente reutilizando `contraste_pagina`/`_cita_contiene`.

#### 14 · I13: la evidencia de las celdas de «Configuración V6.4» no entra en el vínculo
- **[Hecho]** `p6_varios.py`: 29 de las 308 celdas del universo de Viscofan no tienen fila en el Control maestro (son las de configuración); cambiando en el libro la fuente y el período del tipo impositivo (`Configuración V6.4!B12`, `B13`) la entrada `B11` sigue comprobada.
- **[Propuesta]** Añadir a `evidencia_libro` las celdas de trazabilidad de cada clave (`CE.CELDAS_METADATOS` y la tabla de trazabilidad).

#### 15 · Un `sellar` rechazado reescribe el registro y lo pasa a formato 4.15
- **[Hecho]** `p2_i13.py` (D9): `sellar rechazado: [] … | formato ahora: 4.15 | el archivo cambió: True`. El registro es material auditado: una orden que no sella nada cambia su huella.
- **[Propuesta]** Escribir solo si se selló alguna entrada.

#### 16 · I9: `informe.py` sigue imprimiendo «330 de 232» con una ficha anterior
- **[Hecho]** `p10_i9_informe.py` (informe.py de la instantánea de las 12:44 sobre copias de los expedientes finales, sin regenerar la ficha):
```
viscofan_decisiones/Viscofan: ficha guardada → comprobadas 330, universo 232, 'comprobadas_universo' presente: False | informe.py rc 0 | Verificación de las entradas financieras:** 330 de 232 celdas del universo comprobadas (+98 datos de origen auxiliares) ·
vidrala_decisiones/Vidrala: … 347 de 226 celdas del universo comprobadas (+121 datos de origen auxiliares) ·
```
  Causa: `ve.get('comprobadas_universo', ve.get('comprobadas'))` (línea 210) recurre al recuento que incluye los auxiliares. Con la ficha regenerada (lo que hace la batería y el pipeline) el recuento es correcto. Sin libro, `aptitud` devuelve `universo: None, comprobadas_universo: None` (cómo lo imprime el informe no se ha ejecutado).
- **[Propuesta]** Quitar ese recurso (si falta `comprobadas_universo`, decir que la ficha es anterior y no dar recuento). La regeneración de las salidas finales queda para el hito siguiente, como declara la coordinación.

#### 17 · La huella es sensible a la forma de escribir el mismo dato
- **[Hecho]** `p2_i13.py` (D5): igual tras ida y vuelta por JSON y con otro orden de claves; distinta con `849697` en vez de `849697.0`, la página `22` en vez de `"22"`, el mismo texto en NFD o un espacio final → «desactualizada».
- **[Interpretación]** Falla en el sentido seguro; puede obligar a resellar tras una reserialización inocua.
- **[Propuesta]** Canonizar antes de calcular la huella (números por valor, NFC, espacios).

#### 18 · Falsos rechazos de formatos legítimos
- **[Hecho]** No se aceptan miles con espacio y punto decimal («849 697.0», «1 234 567.89»), apóstrofo («45'479.209»), más de seis decimales con ceros finales («149,5000000»), ni un `sha256` en mayúsculas (→ «desactualizada»); «p. 22», «pág. 22» y «22.0» quedan pendientes (coherente con exigir la página del PDF, pero conviene decirlo en el mensaje). Un .txt sin marcas `[PDF PAGE n]` queda pendiente; las dos fuentes de mercado reales las tienen. En los registros reales no hay ningún falso rechazo en el universo de cálculo (`p7`).
- **[Propuesta]** Añadir esas variantes a `_cifras`; comparar huellas sin distinguir mayúsculas.

#### 19 · Pruebas nuevas que no prueban lo que dice su rótulo
- **[Hecho]** (a) Batería 415, V «sellar: … sella solo la revisada por ese revisor hoy; rechaza … otra fecha» y el encabezado «`sellar` no legitima revisiones antiguas»: la fecha es un argumento; véase el hallazgo 3. (b) J: solo comprueba `DATOS_JUICIO_ANALISIS ⊆ DATOS_ANALISIS`; no detectaría una celda nueva sin cubrir ni la geografía. (c) Entrada efectiva, R «Vidrala …: ninguna entrada migrada distinta (las entradas declaradas y el libro concuerdan)»: C50 no está declarada. (d) E «con la declaración alineada con el libro (fixture), ninguna entrada no reproducible» da por bueno que editar `fase1_v63.json` silencie el control. (e) `prueba_reconstruccion_c48_4_15.py` escribe «todas dependen de C48» como texto fijo cuando hay más de cuatro diferencias; no lo calcula, y clasifica solo los 60 primeros ejemplos. (f) La reconstrucción no ejecuta `--sin-migrados` para Viscofan ni Vidrala; en `6_vidrala_4_14_declarado.json` (leído) consta `reproduce_por_via_generativa: true` con C50 0 → 0.
- **[Propuesta]** Renombrar o reforzar esos casos; añadir `--sin-migrados` a los tres expedientes; calcular la dependencia o quitar la frase.

### Observaciones

20. **[Hecho]** Límites que ya estaban en la 4.14 y siguen: un cero comprobado se acredita con cualquier guion aislado de la cita (`_cita_contiene("Deuda neta - total: 12,3", 0)`, `("12,3 - 4,5", 0)` → `True`; de extremo a extremo en `p1`); «1.234» vale como 1,234 y como 1234 (el control no conoce el separador decimal del documento: bastaría declararlo en la fuente); el signo impreso no se contrasta («(149,5)» vale para +149,5 y −149,5).
21. **[Hecho]** `comprobar` dice que nunca lanza y lanza con un registro mal formado: hipótesis con `fuente` de texto (`AttributeError`), `clase` que es una lista (`TypeError`), dos derivados que se citan (`RecursionError`); son rutas de la 4.14. La nueva con `fase1_v63.json = []` está en el hallazgo 4.
22. **[Hecho]** `rellenar`: en la rama H1 (cero pendiente en la ventana) el valor migrado distinto se conserva y se avisa en el Control maestro, pero no entra en `entradas_migradas_distintas` (`p8_rellenar.py`: C49 128,1 frente a 72,19; solo se registra C48). `comprobar` sí lo vería.
23. **[Hecho]** En los libros finales de la 4.14, muchas cifras de juicio de Análisis están en el libro sin declaración en `fase1_v63.json` (`p8_rellenar.py`: Viscofan, 14: C24, C26, C28, C31, C32, C33, C34, C38, C40, C53, C54, C60, C88, C96; Vidrala, 9 más C50; Elis, 7): vienen de la etapa 1 o, alguna, de la derivación de `rellenar` desde la Historia. **[Interpretación]** No mueven la valoración; con I8 tendrán que contrastarse en el registro. Es el mismo patrón de C48 en el ámbito de juicio, y el mecanismo por el que una cifra como C42 pudo quedar desfasada.
24. **[Hecho]** `universo_calculo()` no se usa. `ficha.py` de la instantánea revisada aún rotulaba la aptitud como «4.14» (archivo cambiado después).
25. **[Hecho, proceso]** `verificar_paquete.sh completa` se inició a las 12:54 y seguía en ejecución a las 13:15 (listas de procesos de las 12:59, 13:03 y 13:15); durante ese tiempo cambiaron `ficha.py` e `informe.py` (12:59), se creó `alcance_modelo.py` (13:01) y cambiaron `fase1_historia.py` y `cambiar_base.py` (13:07). **[Interpretación]** Esa ronda no es «sobre el código definitivo» (§8): habrá que repetirla con el árbol congelado, junto con la reconstrucción si cambia algo de su cadena.

## 5. ¿Cumple el diseño vigente el §3 («no proteger el resultado únicamente porque una celda ya tenga un valor migrado»)?

- **[Hecho]** Lo que hace: `rellenar` conserva el valor migrado (regla v2.2), termina con código 0 y lo anota en `entradas_migradas_distintas` y en los avisos; `comprobar` convierte en discrepancia «no reproducible» una entrada C46–C50 comprobada cuyo valor del libro no es el de `fase1_v63.json`. El pipeline no se detiene: `VE.aptitud` solo alimenta el registro del paso 12 y la línea «apta por entradas: sí/no» de la ficha y el informe.
- **[Hecho]** Para Elis con el CAMBIO 4.15, la entrada efectiva (108,0) sale de su `calculo` y la celda de la etapa 1 se vacía. Resultados de la reconstrucción regenerados por la coordinación a las 12:50–12:53 (leídos, no ejecutados): caso 2 (4.14 sin migrados) C48 108 → 82,933 y precio de Sí 7,3020553231 → 8,9801824507 (+1,6781271276, las cifras del encargo); casos 3 y 4 (CAMBIO 4.15, con y sin migrados) C48 = 108 y precio de Sí idéntico, con diferencias solo en celdas de fecha de ejecución y de evidencia documental (`reproduce: false` en sentido estricto por ellas; el informe las clasifica).
- **[Interpretación]** La primera frase de §3 («corregir la vía generativa para conservar la entrada efectiva justificada») se cumple para una entrada declarada con su cálculo. La segunda solo en parte: cuando no hay declaración que coincida, el resultado sigue protegido por el valor migrado; lo nuevo es que deja de ser silencioso **en los casos que el control detecta** y que eso impide la aptitud por entradas. Donde el control falla en abierto (hallazgo 4: celda sin declarar —Vidrala C50—, sin `fase1_v63.json`, `fase1_v63.json` editado, entrada no material) la protección sigue siendo silenciosa.
- **[Interpretación]** Mantener la regla v2.2 para no romper la línea de base es defendible (lo contrario habría sido editar una referencia), y el código 7 anterior era más estricto pero incompatible con ella.
- **[Propuesta]** Para poder decir que §3 se cumple: (1) cerrar el hallazgo 4; (2) un modo estricto que el pipeline active en expedientes nuevos (p. ej. `--entrada-efectiva estricta` o una clave de configuración), en el que `rellenar` se detenga con un código propio, dejando el modo actual para la línea de base v2.2; (3) ejecutar la reconstrucción `--sin-migrados` en los tres expedientes; (4) decir en la documentación del hito que, fuera del modo estricto, la consecuencia es una etiqueta y no una parada.

## 6. Límites de esta revisión

- No se ha ejecutado nada que use LibreOffice ni la ronda completa; la reconstrucción de C48 se ha leído, no repetido.
- No se han revisado `pipeline.py` (I19), `alcance_modelo.py`, ni los cambios de `ficha.py`, `informe.py` y `resumen.py` posteriores a las 12:44 (I20, F1), ni la corrección de C42 de Viscofan y sus textos (parte de I8 que depende de regenerar expedientes).
- Los contraejemplos son sintéticos salvo donde se dice «real» (Vidrala C49/C50, registros de la 4.14, libros finales). No demuestran que los registros reales contengan esos errores: en el universo de cálculo de los tres registros de la 4.14 las reglas nuevas no encuentran ninguna discrepancia de página, conservación o redondeo.
- La revisión no es humana ni sustituye a la externa.
