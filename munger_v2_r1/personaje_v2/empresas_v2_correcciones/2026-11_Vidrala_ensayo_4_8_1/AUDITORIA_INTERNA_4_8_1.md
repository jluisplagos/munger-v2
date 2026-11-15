# Auditoría interna de la entrega 4.8.1 (contexto separado)

**Qué es este documento:**
- es el informe final del agente auditor de Claude, que trabajó con contexto separado, sin haber visto cómo se hizo el trabajo;
- es una transcripción **condensada** del informe: conserva los hallazgos, sus hechos y sus propuestas, pero abrevia algunas tablas y cifras secundarias. El control de vigencia (V-6) señaló que la primera versión omitía una cifra que el registro cita; se ha repuesto en Y-c;
- es salida de un modelo, no una comprobación externa;
- **procedencia:** un agente de Claude (Opus), lanzado el 10-nov-2026 a las 19:41 CET y terminado a las 19:57;
- **actividad:** el auditor registró su avance en un archivo de progreso, revisado durante la ejecución;
- **material auditado:** `MATERIAL_AUDITORIA_4_8_1.txt`, con SHA-256 `4315129b…5ee55f20` y 47 archivos.

Las correcciones de cada hallazgo están en `REGISTRO_ENTREGA_4.8.1.md` §6. El control de vigencia de esas correcciones está en `AUDITORIA_INTERNA_4_8_1_vigencia.md`.

---

## Material

- **Archivo de material:** `MATERIAL_AUDITORIA_4_8_1.txt`. Su SHA-256 `4315129bea90eff4602bbade294d1448cfa3da9c83d089248b0d0d7b5ee55f20` coincide con el esperado.
- **Huellas (hecho):** las 47 huellas coinciden con los archivos del árbol (`sha256sum -c`, 0 discrepancias). Se volvieron a comprobar al terminar y seguían coincidiendo.
- **El árbol no se tocó:** no se modificó ningún archivo ni se creó ningún `__pycache__`.

## Qué se ejecutó

No se ejecutó nada que use LibreOffice. Los temporales estaban en el directorio propio del auditor.

1. **`test_auditorias_v2.py`:** 30/30, código 0, con el mismo estado por prueba que la salida conservada. La huella H2 es `9edf6252…`, la esperada.
2. **`reproducir_rt1.py`** con el código 4.8.1: pide una auditoría nueva en los tres modos, con código 10, igual que la salida conservada. La salida conservada con el código 4.8 muestra la reutilización en UTC y con fechas renovadas.
3. **`analisis_reinversion_4_8_1.py --salida`:** código 0 y seis controles. Las 5 salidas son idénticas byte a byte; las 4 referencias de R-F2 coinciden a 7 decimales; el 60,45 % y el −2,0475 se confirman.
4. **`comprobar_integracion_verificador_481.py`:** 13 de 13.
5. **Casos propios contra R-T1 (K1 a K6)**, sobre copias del expediente 4.6.1: X-c con el esquema roto en una copia del código, después `--desde 13` o `--desde 14`.
6. **Mutaciones adicionales:** M10 y M11 no se detectan (30/30); M12 sí.
7. **Fechas con archivos ZIP reales:** `zip` y `unzip` de Info-ZIP y `zipfile` de Python, con TZ=Europe/Madrid y con UTC.
8. **Sondas financieras propias.** El control con ρ = 0 reproduce exactamente S·L1.15 (61,628529).

## Hallazgos

### Y-a · bloqueante · Un cambio solo de formato del informe antiguo se acepta como respuesta nueva

**Hecho.** Después de X-c y `--desde 13`, se escribió como `auditoria.md` el informe antiguo (`c051cfaa…`) con la línea de la solicitud vigente y un solo cambio de formato. En los cuatro casos el resultado es código 0, `concluido · paso 14`, ficha con `cierre` y fila concluido/APROBADO:
- **K2:** «Veredicto: APROBADO.», con punto final;
- **K2b:** el mismo texto en Unicode NFD;
- **K2c:** « · » cambiado por « - »;
- **K2d:** «Material auditado: \`74b94f8072dd58c1\`.».

**Causa.** `huella_contenido` solo quita los espacios, `*_#>\``, la línea de solicitud y las mayúsculas. La puntuación, los separadores y la forma Unicode cambian la huella.

**Por qué importa.** El encargo pide que los cambios de formato, por sí solos, no acrediten una respuesta. El Anexo D, DECISIONES y el registro dicen que se descartan.

**Propuesta:**
- normalizar con NFKC y casefold y quitar todo lo que no sea letra o cifra;
- detectar casi duplicados;
- añadir las pruebas de K2 a K2d;
- rebajar la redacción a lo que de verdad se garantiza.

### Y-b · bloqueante · Una auditoría histórica con otro nombre responde a una solicitud nueva

**Hecho (K1).**
- El expediente contiene `auditoria_4_6_antecedente.md`: APROBADO según H2 y con «Material auditado: 74b94f8072dd58c1», el material vigente.
- Después de X-c y `--desde 13`, basta copiarlo como `auditoria.md` y añadirle la línea de la solicitud.
- Resultado: código 0, concluido, ficha cerrada y fila APROBADO.

**Causa:**
- solo se anota como usada la `auditoria.md` presente en el primer paso 13;
- no se anotan las demás auditorías del expediente, ni las de `historial_cierres/`, ni `cierre_vigente.json → auditoria_sha256`;
- ese registro vive solo en `estado_pipeline.json`. Que `--reiniciar` lo borra es una interpretación, sin probar;
- la mutación M11, recordar solo la última respuesta, no se detecta.

**Por qué importa.** El encargo prohíbe asignar una solicitud nueva a una auditoría histórica.

**Propuesta:**
- anotar como usadas todas las auditorías conocidas del expediente, por huella y por contenido;
- guardar ese registro en un archivo propio que `--reiniciar` no borre;
- añadir pruebas.

### Y-c · importante · El denominador de f (den = H31:L31) no es neutral

**Hecho.** den = 520,60 se reparte así:

| Componente | Importe | Peso |
|---|---:|---:|
| Inversión menos amortización | 229,38 | |
| Adquisiciones netas | 12,42 | |
| Circulante | 278,80 | 53,6 % |

- **Desproporción.** Por unidad de ΔV, el circulante histórico es 0,585, y el del modelo, 0,147.
- **Efecto.** f = den ÷ (den − Rh) reparte Rh también sobre el circulante, así que descontamina la inversión fija menos de lo que implica la propia hipótesis.
- **Variante del auditor**, igual de condicionada: descontaminar la inversión fija para crecer con ρ = Rh ÷ inversión fija neta histórica (251,2). Da 65,38 / 59,95 con λ = 1,15 y 62,10 / 55,36 con θ = 1.
- **La cartera.** den resta toda la D&A, también la de la cartera (Σ 9,41), mientras que Rh se mide contra D&A − cartera. Por eso f sale sobrestimado. Cifras del auditor:
  - λ = 1,15: f 1,1684 frente a 1,1442; SR2 pasa de 63,69 a 63,43;
  - θ = 1: f 1,8474 frente a 1,7877.
- **Comparación de la variante** (ponderado):

  | Requisito | Variante | SR1 | SR2 | H |
  |---|---:|---:|---:|---:|
  | λ = 1,15 | 65,38 | 62,48 | 63,69 | 68,92 |
  | θ = 0,5 | 65,92 | 61,30 | 63,23 | 68,63 |
  | θ = 1 | 62,10 | 52,86 | 56,72 | 62,71 |

**Propuesta:**
- declarar la composición de den;
- publicar la variante o justificar den;
- corregir o justificar el tratamiento de la cartera.

### Y-d · importante · El salto del terminal sigue en todas las alternativas de R-F1

**Hecho.**
- **Reposición contable.** En el NORMAL, 132,95 en los años 1–10, plana, y 165,30 en el terminal.
- **Requisito.** λ = 1,15: de 19,94 a 24,80, un +24 % frente a un +2 % de ventas. θ = 1: de 47,76 a 59,38.
- **§2.** Solo mide la convención con el nivel 55,555; no la mide para las familias Λ y Θ.
- **Cuantificación propia:** en S·L1.15, terminal plano × (1 + g) +0,77 y años proporcionales a las ventas −0,33; en S·T1.00, +1,84 y −0,79.
- **«Coherentes».** §3.7 y D-N3b llaman coherentes a SR1 y SR2, pero solo lo son en cuanto al crédito.
- **`ORIGEN`.** Clasifica la reposición plana de los años 1–10 como dato, cuando es una convención.

**Propuesta:**
- cuantificar la convención en cada celda;
- matizar «coherentes»;
- reclasificar la reposición de los años 1–10 como convención.

### Y-e · importante · Afirmaciones retiradas de la 4.8 que siguen en documentos vigentes

**Hecho:**
- `CONTINUIDAD.md` §9, punto 0f, sigue diciendo «P1 propuesta como hipótesis central, con P5 y P6 siempre a la vista»;
- el punto 0g remite «como en 0f»;
- `DECISIONES.md`, entrada de la 4.8, mantiene sin marca «contiene doble cómputo», «alternativas coherentes … 69,7 a 62,7» y «P1 … hipótesis central».

**Propuesta.** Anotar la retirada en los dos sitios.

### Y-f · importante · La documentación de R-T1 promete más de lo que hace el código

**Hecho.** Estas afirmaciones son falsas por Y-a, Y-b, Y-g o Y-h:

| Dónde | Afirmación |
|---|---|
| Anexo D | «un informe antiguo copiado, reescrito o con otra fecha no responde» |
| DECISIONES | «a las auditorías históricas no se les asigna ninguna solicitud» |
| CONTINUIDAD y REGISTRO §2 | «el paso 14 rechaza … con otro `auditoria.md`», sin limitarlo a los cierres de la 4.8.1 |
| REGISTRO §3.4 | «vale también para `ficha.py` y para la comprobación de vigencia» |
| REGISTRO §3 | la batería «cubre todos los casos del encargo» |

**Propuesta.** Corregir el código o rebajar cada afirmación a lo que esté comprobado.

### Y-g · menor · Cierres anteriores a la 4.8.1: sustituir `auditoria.md` mantiene el cierre y lo reescribe

**Hecho (K3).**
- `auditoria.md` se sustituyó por `auditoria_4_6_antecedente.md`.
- Sin `--desde`, el cierre sigue vigente.
- Con `--desde 14`, se cierra de nuevo y `cierre_vigente.auditoria_sha256` pasa de `c051cfaa…` a `57f48faa…`.

**Propuesta.** Sin `auditoria_respuesta`, comparar con `cierre_vigente.auditoria_sha256`.

### Y-h · menor · Una solicitud pendiente no afecta a la vigencia ni a `ficha.py`

**Hecho (K4).** `--desde 13` sobre un expediente concluido, sin X-c, termina con código 10 y una solicitud pendiente. Mientras tanto:
- `estado_pipeline.auditoria` sigue en `APROBADO`;
- la ficha cerrada y la fila APROBADO siguen;
- `ficha.py --estado concluido` reescribe la ficha cerrada con código 0.

**Propuesta:**
- decidir si pedir una auditoría nueva retira el cierre;
- como mínimo, rechazar en `motivo_rechazo_cierre` o limpiar `auditoria`;
- añadir la prueba.

### Y-i · menor · Un cambio de bytes sin contenido nuevo anula para siempre una respuesta legítima

**Hecho (K6).**
- Tras un cierre válido de la 4.8.1, `auditoria.md` se volvió a guardar con finales de línea CRLF.
- La comprobación de vigencia archiva el cierre y registra una solicitud nueva.
- Restaurar los bytes originales ya no sirve, y solo queda una auditoría nueva.

**Propuesta.** Comparar por la huella de contenido, o al menos documentarlo.

### Y-j · menor · Huecos de la batería

**Hecho:**
- M10 y M11 no se detectan.
- Faltan pruebas para:
  - las variantes de puntuación y de Unicode;
  - las auditorías históricas con otro nombre;
  - la respuesta penúltima;
  - `ficha.py` con una solicitud pendiente;
  - la sustitución en un cierre anterior a la 4.8.1;
  - el cambio de material mientras la solicitud está pendiente (K5: funciona, pero no se prueba).
- Con el código 4.8, los grupos D y E se interrumpen con IndexError en vez de mostrar el fallo.

**Propuesta.** Añadir esos casos y sus mutaciones.

### Y-k · menor · La explicación del defecto con fechas ZIP depende de la herramienta

**Hecho:**
- `zipfile` e Info-ZIP con `-X` reproducen los dos modos: −0,21 s en CET y +3.599,8 s en UTC.
- Info-ZIP por defecto (campo UT) da la misma fecha en CET y en UTC.
- Sin el campo UT, redondea hacia arriba los segundos impares (+0,79 s): el código 4.8 aceptaría la auditoría también en CET.
- La frase del registro «Leído en CET … como mucho 2 s antes» no es general.

**Por qué importa poco.** Solo afecta a la explicación: el código 4.8.1 no usa fechas.

**Propuesta.** Precisarlo en el registro.

### Y-l · menor · Marcadores sin rellenar y salidas de referencia inexistentes

**Hecho:**
- «__N481__» sigue en el LEEME y en el PROMPT;
- faltan seis salidas citadas en `resultados/`;
- el registro tiene §6, §7 y §10 por completar.

**Propuesta.** Completarlo todo antes de empaquetar.

### Y-m · menor · El Δ frente a REF en R-F1 mezcla P0 con el requisito

**Hecho.** H·L1.10 aparece con +0,01 frente a REF, pero frente a P0 es −0,48.

**Propuesta.** Añadir el Δ frente a P0.

## Lo que se comprobó y está bien

- **Las fechas y la regla H2.** La huella H2 es la esperada y las fechas no intervienen en el paso 13.
- **El escenario del encargo:**
  - X-c → `--desde 13`, y X-c → `--desde 14` → `--desde 13`;
  - los relanzamientos, con fecha reciente y con fecha futura, conservan la solicitud y no cierran nada.
- **Las respuestas rechazadas:**
  - las que no nombran la solicitud, nombran otra o la nombran dos veces;
  - las que nombran una solicitud sustituida (K5).
- **Material distinto y H2.** Un material distinto da una solicitud nueva; una auditoría que incumple H2 da REPETIR.
- **La respuesta válida** cierra en los tres modos, y el informe antiguo puesto después en su lugar se rechaza.
- **El cierre de la 4.6.1** sigue vigente sin ninguna solicitud retroactiva.
- **Las mutaciones** 1 a 9 y la M12 se detectan.
- **La integración** del verificador da 13 de 13.
- **El material de las pruebas anteriores.** `agentes_sinteticos.py` y la prueba 8 de `test_resumen_v2.py` solo añaden la línea de la solicitud; no cambia ninguna expectativa.
- **R-F2.** El diseño 2 × 2 está bien, Shapley cierra y las cifras coinciden.
- **R-F1:**
  - las tablas coinciden con el CSV;
  - θ figura como hipótesis;
  - P1s está bien diagnosticado;
  - se cumplen las identidades;
  - solo hay crédito en la estructura H;
  - las retiradas constan en VERSION, en DECISIONES (4.8.1) y en el JSON;
  - los campos humanos están vacíos.
- **Las reglas permanentes** no han cambiado.

## Límites de esta revisión

- No se ejecutó nada que use LibreOffice. Para eso se confía en las salidas conservadas.
- No se probaron `--reiniciar` ni el modo `--agentes-simulados` de principio a fin.
- Las variantes de Y-c y de Y-d son contrastes igual de condicionados que los de la entrega.
- No se revisaron las fuentes públicas.
