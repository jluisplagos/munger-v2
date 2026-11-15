# ANEXO D · Esquemas, formatos y salidas

Versión 0.2.1 (2-nov-2026). Todo JSON en UTF-8, números como números (0,07 → `0.07`), fechas `AAAA-MM-DD`, textos en español. Los esquemas definitivos (JSON Schema) se escriben en `esquema/` en la pieza 4 y los validan los scripts. Lo que sigue fija el contenido mínimo.

## D.1 `extracto_v63.md` (agente de extracción V6.3 · Sonnet · ≤ 10.000 palabras)

Complementa el `extracto.md` de la etapa 1 (no lo repite). Secciones, cada dato con `[archivo, PDF p. n]`; si no hay información: «No encontrado en los documentos».

1. **Mercado y cuota**: cifras de tamaño de mercado, crecimiento del mercado y cuota que la propia empresa publique (con la definición que use). Nada de memoria.
2. **Economía por segmento y geografía**: ventas y margen por segmento, reparto geográfico (% de ventas por país o región; es lo que va a `Palancas!A28:B33`), evolución a tipo constante.
3. **Capacidad, capex e inversión**: planes de capacidad, capex anunciado por destino, I+D (importe y % de ventas), adquisiciones con precio y múltiplo si lo dan.
4. **Precios y poder de fijación**: subidas de precio y su efecto en volumen; mezcla; evidencia de que el cliente absorbe o no la subida.
5. **Guía y objetivos de la dirección** (solo como dato, etiquetado «guía»): ventas, margen, capex, dividendo; y si cumplió la guía anterior.
6. **Financiación** (para el motor B y la quiebra): vencimientos, covenants, rating si lo publica, coste medio de la deuda, pasivos por arrendamientos, pensiones, minoritarios.
7. **Regulación y capital** (solo financieras y reguladas): ratios de capital exigidos y mantenidos, límites regulatorios a la distribución.
8. **Hechos medibles para predicciones**: métricas que la empresa publica con regularidad (unidades, tiendas, clientes, cartera de pedidos, márgenes por segmento) y su último valor, para que las predicciones de la fase C sean comprobables.
9. **Lo que no encontré.**

## D.2 `fase_a.json` (Munger cualitativo)

```json
{
  "empresa": "…", "ticker": "…", "fecha_analisis": "AAAA-MM-DD", "version_personaje": "v2.0",
  "cinco_frases": "…",
  "seis_preguntas": {"confio_en_la_gestion": "…", "puede_danar_reputacion": "…", "que_puede_salir_mal": "…", "lo_entiendo": "…", "necesita_capital": "…", "que_caja_espero": "…"},
  "descalificadores": [{"nombre": "deuda que mata", "aplica": false, "evidencia": "…"}],
  "foso": {"tipo": "…", "pruebas": {"sobrino_idiota": "…", "duracion": "…", "quien_me_mata": "…", "empresa_o_nicho": "…"}},
  "cubo_provisional": "Vigilar",
  "limite_del_modelo": {"aplica": false, "cual": null, "porque": null},
  "celdas": {"C11": "Sí", "C12": "Sí", "C13": "No", "C14": "Compounder", "C17": "Sí", "C18": "Sí", "C19": "Sí", "C20": "Incert. alta + riesgo bajo",
             "C25": "Sí", "C27": "Estable", "C51": "Sí", "C56": 0.09, "C61": "No está claro", "C62": "Sí", "C97": "Neutral", "C98": "Buena",
             "Palancas!C5": "Madura en crecimiento", "Palancas!C6": "Ninguno", "Palancas!C8": "Último año", "Palancas!C9": "No", "Palancas!C10": null,
             "Palancas!C43": "No aplica", "Palancas!C47": "Ninguna",
             "B65": "…", "C65": "…", "D65": "…", "B66": "…", "C66": "…", "D66": "…"},
  "herencia": {"C18": {"etapa1": "Sí", "decision": "mantiene", "motivo": "evidencia_nueva", "evidencia_y_razonamiento": "ROIC medio 5 años 22 % frente a r 9 % (Historia C55); margen EBIT 10 años entre 38 y 42 % (fila 29): la ventaja se ve en diez años, no solo en los tres de la etapa 1"}},
  "escenarios": {"MALO": {"historia": "…", "mecanismo": "…", "quien_se_queda_la_mejora": "…", "que_lo_pararia": "…", "hechos_en_que_se_apoya": ["…"]}, "NORMAL": {…}, "BUENO": {…}},
  "observaciones": {"C11": "[Clase: …] [Confianza: …] Hereda: … Apoyo: … Lo sustituiría: …"},
  "lo_que_no_se": ["…"], "que_no_sabria_munger": ["…"]
}
```

`herencia` tiene una entrada por cada una de las **22** celdas heredadas que decide la fase A (`C11:C14`, `C17:C20`, `C25`, `C27`, `C51`, `C56`, `C61`, `C62`, `C97`, `C98`, `B65:D66`). `decision` ∈ {`mantiene`, `cambia`}; `motivo` ∈ {`misma_evidencia`, `evidencia_nueva`, `razonamiento_corregido`, `definicion_o_medicion_distinta`} (D3); `evidencia_y_razonamiento` es obligatorio en todos los casos y tiene que **nombrar la evidencia** (celda de Historia, página del extracto, dato de la V6.3) y el razonamiento; no vale remitirse a la etapa 1 como autoridad. `mantiene` + `misma_evidencia` es una combinación legítima y frecuente. Las otras 12 heredadas llevan el mismo campo `herencia` en `fase_b.json` (`B68:D69`, `C76`: 7) y en `fase_c.json` (`C93`, `B101`, `B102`, `C103`, `C104`: 5); `ficha.py` junta las 34 en `cambios_vs_etapa1`. `limite_del_modelo.aplica = true` (L1 sin motor B posible, L2 o L3 del Anexo B) lleva el análisis a `modelo_no_aplicable` sin fase B; en ese camino `ficha.py` deriva `decision.accion` de `cubo_provisional` (`No` → `descartar`, `Demasiado difícil` → `demasiado_dificil`, otro → `null`), con `precio_objetivo` y `condicion` = `null`. Si el límite lo declara la fase C en su primer turno (paso 10), `ficha.py` deriva la acción igual, de `fase_c.json.cubo_provisional`.

## D.3 Formato de la Observación (columna N de Control maestro y campo `observaciones`)

Una Observación por celda, en una sola celda de texto, con este orden y estas etiquetas (para que los scripts la validen):

```
[Clase: fundamentada | convención | técnico | sin juicio propio] [Confianza: alta | media | baja]
Hereda: <valor etapa 1> → <mantiene | cambia> (<motivo>): <evidencia y razonamiento en una frase>.   (celdas heredadas)
Hereda: nueva en V6.3.                                                                              (celdas nuevas)
Referencia mecánica: <cifra y regla, o «no disponible: motivo»>. Decisión: <cifra o valor>. Desviación: <±x, «ninguna» o «sin referencia»> porque <motivo>.   (solo palancas, probabilidades, quiebra, C76, C44)
Apoyo: <hechos del extracto o de la Historia, con celda o página; citas «…» (PCA p.110; HIM) o (CV p. 7)>.
Lo sustituiría: <qué dato o hecho me haría cambiar esta celda, en qué sentido>.
```

Reglas: ≤ 900 caracteres; toda cita con libro/documento y página; `<motivo>` es uno de los cuatro de D3; la clase *sin juicio propio* solo con «Desviación: ninguna» y referencia disponible; la clase *técnico* solo donde no hay referencia disponible (o la celda no tiene referencia), con «Desviación: sin referencia» y siempre con un rango en «Apoyo»; una Observación de celda heredada siempre lleva la línea `Hereda: … → …`; una de celda nueva lleva exactamente `Hereda: nueva en V6.3.` Una Observación con clase *fundamentada* o *convención* cuya línea «Apoyo» no cite ningún hecho (celda o página) se cuenta como hipótesis insuficientemente fundamentada a efectos de D10.

## D.4 `fase_b.json` (palancas)

```json
{
  "motor": "A",
  "palancas": {
    "crecimiento_1_5": {"MALO": {"referencia_mecanica": 0.0, "referencia_no_disponible_motivo": null, "valor": 0.01, "desviacion": 0.01, "clase": "fundamentada", "confianza": "media", "porque": "…", "apoyo": "…", "lo_sustituiria": "…"}, "NORMAL": {…}, "BUENO": {…}},
    "margen_objetivo": {…}, "s2c": {…}, "g_perpetuo": {…}, "roic_lp": {…},
    "probabilidades": {"MALO": {…}, "NORMAL": {…}, "BUENO": {…}, "argumento": "…"}
  },
  "quiebra": {"C22": null, "C23": null, "disparadores": [], "clase": "convención", "porque": "…"},
  "mercado": {"C24": null, "fuente": null},
  "exceso_caja": {"C76": 0, "clase": "fundamentada", "porque": "…"},
  "fcf_normalizado": {"C44": null, "clase": null, "porque": "…"},
  "desviaciones_justificadas": [{"comprobacion": "G4", "escenario": "NORMAL", "justificacion": "…", "hechos": ["Historia C55", "extracto p. 12"], "clase": "fundamentada"}],
  "limite_del_modelo": {"aplica": false, "cual": null, "porque": null},
  "herencia": {"B68": {"etapa1": 0.015, "decision": "mantiene", "motivo": "misma_evidencia", "evidencia_y_razonamiento": "…"}, "C68": {…}, "D68": {…}, "B69": {…}, "C69": {…}, "D69": {…}, "C76": {…}},
  "dos_errores": {"mas_cerca_de": "regatear | pagar cualquier cosa", "porque": "…"},
  "celdas": {"Palancas!B14": 0.01, "Palancas!C14": 0.04, "Palancas!D14": 0.06, "Palancas!B15": …, "Palancas!B16": …, "Palancas!B18": …, "B68": 0.015, "C68": 0.025, "D68": 0.03, "B69": 0.2, "C69": 0.6, "D69": 0.2, "C76": 0, "Palancas!C22": null, "Palancas!C23": null, "Palancas!C24": null, "Palancas!C44": null},
  "observaciones": {"Palancas!B14": "…", "…": "…"}
}
```

Por palanca y escenario: `referencia_mecanica` (número, o `null` con `referencia_no_disponible_motivo`), `valor`, `desviacion` (`valor − referencia_mecanica`, o `null` si no hay referencia), `clase`, `confianza`, `porque`, `apoyo`, `lo_sustituiria`. Regla G14: `clase = "sin juicio propio"` exige referencia disponible y `desviacion = 0`; con referencia `null` la clase es *fundamentada*, *convención* o *técnico*. `comprobar_gramatica.py` exige que toda comprobación de categoría *desviación económica* disparada tenga su entrada en `desviaciones_justificadas` con `justificacion` no vacía, `hechos` no vacío y clase *fundamentada* o *convención*; un **error** no admite entrada ahí: se corrige. `limite_del_modelo.aplica = true` (L1 detectado al traducir) devuelve la pregunta a la fase A (código 3).

## D.5 `resultados.json` (lectura del libro recalculado)

Valores (`B78:D78`, `C83`, `C84`, `C85`, `C86`, `C39`, `C87`), estados (`Motor!B255`, `B256`, `B258`, `B266`, `B267`, `B268`, `B269`), causas activas (`Diagnóstico V6!A161:A172`), semáforos (`Diagnóstico V6!B40:D50` con sus textos), «cuánto pagas por crecer» (`C53:D57`), múltiplos (`B61:E65`), autocomprobaciones (`B69:B84`), salto del año 11 (`B176:D178`), tornado (`A215:C221`), precio de referencia (`C156`), evidencias (`Control maestro!D240:D250`), banderas y avisos (`Análisis!C7`, `D7`), tabla del DCF inverso (`Análisis!A108:B188`), `Diagnóstico V6!C5` (motor), `C15:C18` (r operativa y r mínima), `Historia!C43:C66` (anclas), y `recalculo_forzado_comprobado: true` (la prueba de §4.7: una celda dependiente de una celda escrita cambió).

## D.6 `fase_c.json` (revisión inversa, fundamento material y conclusión; se completa en dos turnos)

```json
{
  "una_sola_historia": {"coherente": true, "incoherencias": ["…"]},
  "lo_que_dice_la_hoja": {"semaforos_relevantes": ["…"], "peso_terminal_NORMAL": 0.68, "salto_anio_11": {"MALO": 0.01, "NORMAL": 0.07, "BUENO": 0.12, "explicacion": "…"}, "dcf_inverso": "…", "palanca_mas_influyente": "ROIC / ROE largo plazo (±5 pts)", "nota": "el tornado es información, no criterio"},
  "desviaciones_justificadas": [{"comprobacion": "G16", "escenario": "NORMAL", "justificacion": "…", "hechos": ["…"], "clase": "fundamentada"}],
  "autocomprobacion": [
    {"sesgo": "anclaje en la etapa 1", "hallazgo": "…", "cambio": "ninguno porque … | C18 → …"},
    {"sesgo": "anclaje en el precio o en la fuente externa", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "consistencia y compromiso", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "historia bonita / viento de cola atribuido a la empresa", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "optimismo del BUENO frente a la tasa base", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "doble castigo del mismo riesgo", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "disponibilidad (lo vívido del extracto)", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "autoridad (guía de la dirección como hecho)", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "¿el MALO es de verdad malo?", "hallazgo": "…", "cambio": "…"},
    {"sesgo": "lo no numerable que pesa y no está en las palancas", "hallazgo": "…", "cambio": "…"}
  ],
  "revisar_palancas": false, "instrucciones_revision": null,
  "cubo_provisional": "Sí", "conclusion_provisional": "comprar",
  "revision_datos_ausentes": {
    "revisados": [
      {"dato": "Análisis!C88", "que_falta": "P/FCF histórico", "conclusion_afectada": "ninguna celda de juicio; solo contexto del precio", "material_para_conclusion_favorable": false, "porque": "la escalera no usa C88; el múltiplo histórico serviría de contraste, no de fundamento"},
      {"dato": "Palancas!A28:B33", "que_falta": "reparto geográfico de las ventas", "conclusion_afectada": "prima de riesgo país dentro de r (heredada, S-3) y lectura del mercado del BUENO", "material_para_conclusion_favorable": false, "porque": "el extracto (p. 14) dice que el 91 % de las ventas es de la eurozona: la prima país que falta no cambia r de forma apreciable; lo anoto en lo_que_no_se"}
    ],
    "alguno_material": false
  },
  "fundamento_material": {
    "hipotesis_sin_fundamento": [
      {"celda": "B69:D69", "hipotesis": "probabilidades 0,2/0,6/0,2", "clase": "sin juicio propio", "porque_sin_fundamento": "copiadas de la referencia sin argumento propio",
       "alternativas_defendibles": {"hay_base": true, "rango": {"MALO": [0.2, 0.4], "NORMAL": [0.4, 0.6], "BUENO": [0.1, 0.2]},
         "evidencia": "p(MALO), techo 0,4: en 10 ejercicios (Historia 2015–2024, filas 28–29), 4 tuvieron crecimiento negativo O margen por debajo del margen del MALO (2016, 2019, 2020, 2023) = 0,4. Suelo 0,2: con la definición estricta (las dos cosas a la vez) son 3 (2016, 2020, 2023) = 0,3, y de ellos 2020 fue el cierre por pandemia, que la dirección describe como no repetible y cuyas ventas se recuperaron en 2021 (extracto p. 22): sin ese año, 2 de 10 = 0,2. p(BUENO), suelo 0,1: 1 de 10 ejercicios (2021) cumplió a la vez el crecimiento y el margen del BUENO. Techo 0,2: 2 de 10 (2017, 2021) cumplieron al menos una de las dos condiciones. NORMAL: el resto."}},
      {"celda": "Palancas!D18", "hipotesis": "ROIC LP BUENO 0,18", "clase": "técnico", "porque_sin_fundamento": "sin referencia BUENO (C55 vacía: la empresa publica el desglose necesario solo desde 2022, tres ejercicios de 2015–2024) y sin hechos en los extractos sobre cuánto durará la ventaja",
       "alternativas_defendibles": {"hay_base": false, "rango": null,
         "evidencia": "no hay base para acotarlo: la media del ROIC del sector (Palancas!H18 = 0,14) es un dato de otras empresas, no un suelo de esta; Análisis!C56 + 0,10 = 0,19 es un umbral de aviso de la plantilla, no un techo económico; tres ejercicios propios no permiten decir qué ROIC sostendría esta empresa en el año 11. Lo que haría falta: ROIC por año de los informes 2015–2021 (notas de segmentos) y cualquier dato de la dirección sobre la duración de los contratos que sostienen el margen."}}
    ],
    "comprobacion_conjunta": {
      "procede": false,
      "combinacion": null,
      "coherencia_economica": null,
      "sobrevive": null
    },
    "resultado": "pendiente_de_investigacion",
    "hipotesis_que_mas_condiciona": "Palancas!D18",
    "que_lo_resolveria": "ROIC por año de los informes 2015–2021 (notas de segmentos) para completar Historia fila 33, y la duración media de los contratos que sostienen el margen (pregunta a Relación con Inversores)"
  },
  "estado_analisis": "pendiente_de_investigacion",
  "cubo_final": "Vigilar",
  "escalera": {"de": "precio.json"},
  "decision": {"accion": null, "precio_objetivo": null, "condicion": null, "condiciones_revision": {"al_alza": "…", "a_la_baja": "…"}},
  "insumos_decision_cartera": {"precio_actual": 494, "zona": "cumple_regla_k", "precio_de_si": 520, "precio_escenario_malo": 430, "ponderado": 610, "distancia_a_precio_si": -0.05, "distancia_a_malo": 0.13, "fundamento": "pendiente de investigación (ROIC LP BUENO sin base para acotar)", "datos_ausentes_materiales": [], "descalificadores_considerados": ["…"], "r": 0.09, "r_minima": 0.085, "palanca_mas_influyente": "ROIC / ROE largo plazo (±5 pts)"},
  "herencia": {"C93": {"etapa1": "Sí", "decision": "mantiene", "motivo": "misma_evidencia", "evidencia_y_razonamiento": "…"}, "B101": {…}, "B102": {…}, "C103": {…}, "C104": {…}},
  "comparacion_etapa_1": {"cubo_v1": "Vigilar", "precio_de_si_v1": 686, "cubo_v2": "Vigilar", "precio_de_si_v2": 520, "por_que_difieren": "…"},
  "celdas": {"C93": "Sí", "C103": "Sí", "C104": "Pendiente de decisión de cartera · conclusión del personaje: sin conclusión (pendiente de investigación) · zona cumple_regla_k · precio de Sí ≤ 520 · precio esc. MALO 430 · ponderado 610 · fundamento pendiente de investigación", "B101": "…", "B102": "…",
             "Palancas!A38": "…", "Palancas!B38": "2027-03-31", "Palancas!C38": 0.7, "Palancas!A39": "…", "Palancas!B39": "…", "Palancas!C39": 0.6, "Palancas!A40": "…", "Palancas!B40": "…", "Palancas!C40": 0.5,
             "Diagnóstico V6!B222": "…", "Diagnóstico V6!B223": "…"},
  "celdas_corregidas": {"C18": {"antes": "Sí", "despues": "Sí", "motivo": "…"}},
  "cambiaria_de_cubo": {"a_si": "…", "a_no": "…", "a_demasiado_dificil": "…"},
  "observaciones": {"C93": "…", "C103": "…", "C104": "…", "B101": "…", "B102": "…", "Palancas!A38": "…"}
}
```

Cuando la comprobación conjunta procede (todas las hipótesis con `hay_base = true` y conclusión provisional favorable), el primer turno rellena `comprobacion_conjunta.combinacion` (una sola combinación: celda → valor, cada uno dentro de su rango y en el extremo desfavorable a la tesis, o con la razón de no estarlo) y `coherencia_economica` (la historia única que hace compatibles esos valores); el script escribe `comprobacion_conjunta.json` (§D.6b) y el segundo turno copia `sobrevive` (booleano, el mismo de §D.6b) y rellena el resto. En el ejemplo, la conclusión provisional era `comprar` (precio 494 en zona `cumple_regla_k`); la primera hipótesis tiene rango con cada límite atado a hechos de la empresa, pero la segunda **no tiene base para acotarse** (y el ejemplo dice por qué no valen la media del sector ni el umbral de la plantilla): no procede la comprobación conjunta y el resultado es `pendiente_de_investigacion`, cubo `Vigilar`, acción `null`. `revision_datos_ausentes` (S-19) recorre cada dato de `datos_ausentes.json` con la conclusión afectada y el motivo; si alguno fuera material para la conclusión favorable, `alguno_material = true` y la fase C cerraría igual sin conclusión, con `C104` «… sin conclusión (pendiente de datos: <celdas>)», y el pipeline pondría `pendiente_de_datos`.

Vocabulario cerrado: `estado_analisis` ∈ {`concluido`, `pendiente_de_investigacion`, `modelo_no_aplicable`} desde la fase C (`concluido` es provisional: lo confirma el pipeline tras la auditoría APROBADO y hasta entonces no se escribe en la ficha oficial `ficha.json`: desde la 4.6 la ficha provisional `ficha_provisional.json` lo lleva solo como estado propuesto, con `provisional.confirmado = false`; `pendiente_de_datos` y `no_entregable` los pone solo el pipeline; cuando la propia revisión de datos ausentes de la fase C declara `alguno_material = true` (S-19), la fase C escribe `estado_analisis = pendiente_de_datos` (único caso en que lo escribe ella; el pipeline lo confirma tras escribir las celdas de C) y cierra con `cubo_final = Vigilar` y `accion = null`, nunca con `Sí`/`comprar`); `cubo_final` ∈ {`Sí`, `Vigilar`, `No`, `Demasiado difícil`}, con `Sí` solo si `estado_analisis = concluido` y `accion = comprar`; `decision.accion` ∈ {`comprar`, `esperar`, `descartar`, `demasiado_dificil`, `null`}; `fundamento_material.resultado` ∈ {`sin_limitacion` (lista vacía), `comprobacion_conjunta_superada`, `pendiente_de_investigacion`, `no_procede` (conclusión provisional no favorable, o favorable bloqueada antes por un dato ausente material, S-19; si la comprobación se hizo igualmente, su escalera se informa como rango del precio de Sí y `resultado` sigue siendo `no_procede`)}. No existe ningún campo de tamaño de posición ni porcentaje alguno, tampoco «0 %» (D16). `revision_datos_ausentes.revisados` tiene una entrada por cada dato de `datos_ausentes.json` (el verificador lo comprueba). El mapa cubo ↔ acción ↔ estado está en el encargo, §8. `Palancas!C38:C40` es la probabilidad de que **cada predicción** se cumpla dado el escenario NORMAL.

### Correspondencia D10 ↔ estado ↔ acción ↔ etiqueta de C104 (reparación del cierre, 4.6)

Tabla cerrada (`scripts/cierre_v2.py → FUNDAMENTO_C104`); la aplica `coherencia_fase_c` del pipeline y la comprueba la auditoría (punto 11). Formaliza la etiqueta de presentación de `no_procede` en los casos que D10 ya admitía; no crea ningún resultado financiero nuevo ni relaja los requisitos de una conclusión favorable.

| `estado_analisis` | `decision.accion` | `fundamento_material.resultado` admitido | Etiqueta visible en `C104` («fundamento …») |
|---|---|---|---|
| `concluido` | `comprar` | `sin_limitacion` (lista vacía) | lista vacía |
| `concluido` | `comprar` | `comprobacion_conjunta_superada` (lista no vacía, comprobación conjunta del script superada) | comprobación conjunta superada |
| `concluido` | `esperar`, `descartar`, `demasiado_dificil` | `no_procede` (conclusión no favorable: D10 no la limita; la comprobación conjunta es opcional) | no procede (conclusión no favorable) |
| `pendiente_de_investigacion` | `null` | `pendiente_de_investigacion` | pendiente de investigación |
| `pendiente_de_datos` | `null` | `no_procede` (dato ausente material, S-19; desde la 4.12, también el objetivo bloqueado por el protocolo experimental «bloqueo_del_objetivo», §D.13) | pendiente de datos |

Cualquier otra combinación (p. ej. `comprar` con `no_procede`, `esperar` con `sin_limitacion`, una etiqueta desconocida o una etiqueta que no corresponde al JSON) es un error de coherencia: corrección a la fase C. `modelo_no_aplicable` no escribe `C104` (§4.7). Se mantienen el prefijo «Pendiente de decisión de cartera», la prohibición de porcentajes (D16), los requisitos de fundamento de `comprar` y la revisión de datos ausentes materiales; con `esperar` y alguna hipótesis sin base, el precio objetivo sigue marcándose provisional en `C104`.

### Cierre, material provisional y alcance declarado (reparación del cierre, 4.6)

- **Material provisional (paso 11):** `ficha_provisional.json` (la ficha con `provisional.estado_propuesto`, `confirmado = false`) e `informe_provisional.md`. Es lo que audita el paso 13. Una `ficha.json` o un `informe.md` oficiales anteriores se mueven a `.anterior`.
- **Material auditado (paso 13):** antes de pedir la auditoría, el pipeline regenera el material provisional (después del paso 12, que deja el libro evaluado con sus cachés, para que la huella del libro en la ficha provisional sea la del libro auditado) y escribe `material_auditoria.json` (SHA-256 de `fase_a/b/c.json` y `.md`, `extracto_v63.md`, `datos_ausentes.json`, `entrada_v63.json`, `referencias_mecanicas.json`, `resultados.json`, `precio.json`, `gramatica.json`, `comprobacion_conjunta.json`, los provisionales, `alcance_v2.json` y los libros de datos y evaluado, los que existan) y su `id`. La auditoría lleva una línea `Material auditado: <id>`. La regla del veredicto de H2 no cambia: la línea de material es una condición adicional, no una flexibilización.
- **Solicitud de auditoría (4.8.1, R-T1):** cada petición de auditoría del paso 13 es una **solicitud** con un identificador propio (`SA-` y 16 cifras hexadecimales, imprevisible).
  - **Dónde consta.** El identificador va en `estado_pipeline.json → solicitudes_auditoria`, en `solicitud_auditoria.json`, en el prompt y en `ESPERANDO.md`.
  - **Qué es una respuesta.** La auditoría lleva una línea propia `Solicitud de auditoría: <id>`, exactamente una. El paso 13 acepta `auditoria.md` como respuesta solo si:
    - nombra la solicitud **pendiente**;
    - si aprueba según H2, no es una auditoría ya **conocida**, ni por su huella SHA-256 ni por su contenido sin formato.
  - **Qué auditorías son conocidas.** Las anota el pipeline cada vez que registra una solicitud, y desde entonces ninguna puede acreditar una aprobación que la responda:
    - todo archivo de texto del expediente, con cualquier nombre y en cualquier subcarpeta, que tenga una línea «Material auditado» o que H2 califique APROBADO. Se leen archivos en UTF-8, UTF-16 con BOM o cp1252, de hasta 50 MB; no se leen los binarios, libros, PDF ni imágenes, ni archivos en otras codificaciones (W-2);
    - la huella que guarda `cierre_vigente.json`;
    - las respuestas ya aceptadas.
  - **Dónde se anotan.** Por huella y por contenido, en `estado_pipeline.json` (`anteriores_sha256`, `anteriores_contenido`) y en `auditorias_conocidas.json`. Este último registro persistente solo se amplía y `--reiniciar` no lo borra.
  - **Sin asignación retroactiva.** A ninguna de esas auditorías se le asigna una solicitud.
  - **Contenido sin formato.** Es el **multiconjunto de palabras** del texto, sin la línea de solicitud: secuencias de letras y cifras, tras la forma Unicode NFKC, sin marcas diacríticas (las tildes) y con casefold. No cuentan los espacios, los saltos ni los cortes de línea, la puntuación, los separadores, las marcas ni el orden. Sí cuenta cuántas veces aparece cada palabra (tercera revisión, W-1).
  - **Una respuesta REPETIR puede repetir el contenido de otra.** Es un auditor que vuelve a encontrar lo mismo, y no puede cerrar nada.
  - **Límite declarado.** El pipeline no puede probar que el auditor haya hecho de nuevo las dieciséis comprobaciones. Detecta la reutilización de una auditoría del expediente o de una respuesta anterior:
    - literal;
    - con otro formato: tildes, orden o cortes de línea, puntuación o forma Unicode;
    - con cualquier nombre o en cualquier carpeta del expediente.

    No detecta:
    - una auditoría antigua a la que se cambian o añaden palabras (basta un «Aviso:» nuevo);
    - una auditoría traída de fuera del expediente;
    - una corrección por material distinto que solo cambia la línea de material, aunque el pipeline pide repetir las dieciséis comprobaciones.

    A la inversa, una auditoría rehecha de verdad con un texto idéntico al de otra ya usada no se acepta: el pipeline sigue esperando con el motivo y no cuenta una corrección fallida (control de vigencia, V-10).
  - **Respuesta que no es UTF-8 válido.** No se consume. El pipeline sigue esperando, con el motivo, a que se guarde en UTF-8 (W-3).
  - **Registro ilegible.** Si `auditorias_conocidas.json` no se puede leer, o sus listas no son de huellas, el pipeline termina con el código 6 y el motivo («REGISTRO DE AUDITORÍAS ILEGIBLE»), sin aceptar ninguna auditoría.
  - **Si no lo es.** El archivo no se consume; el pipeline sigue esperando (código 10), con el motivo en `ESPERANDO.md`, en la última línea y en `ultima_auditoria_no_aceptada`.
  - **Las fechas no deciden nada.** Las fechas de modificación ya no intervienen en el paso 13.
  - **Relanzamientos.** Mientras la respuesta está pendiente y el material fijado es el mismo, los relanzamientos (también con `--desde 13`) conservan la misma solicitud. Si el material cambia, la pendiente queda `sustituida` y se registra otra.
  - **Pedir una auditoría nueva retira el cierre vigente (Q-T5, propuesta pendiente de la persona responsable).** Si al registrar una solicitud hay una ficha cerrada (por ejemplo, `--desde 13` sobre un expediente concluido), en esa misma ejecución:
    - ficha, informe y fila del resumen se archivan con su retirada;
    - la aprobación registrada se retira.
  - **Respuesta aceptada.** Una respuesta aceptada deja la solicitud `respondida`, con su huella, la de su contenido y su veredicto, y `auditoria_respuesta` = {solicitud, sha256, contenido, material}; **(4.9, R-V1)** además `fiel` (también `respuesta_fiel` en la solicitud): la huella del texto íntegro, con su orden, tras aplicar solo las transformaciones inocuas de `cierre_v2.TRANSFORMACIONES_INOCUAS` (BOM UTF-8; finales CRLF o CR leídos como LF; saltos de línea al final del archivo; forma Unicode NFC o NFD). La huella `contenido` (palabras sin orden) queda solo como **detector** de reutilizaciones del paso 13. Toda petición posterior es una solicitud nueva: una corrección por material distinto o la auditoría siguiente a una vuelta REPETIR.
  - **Lo que no cambia.** La regla H2 (`veredicto_auditoria`, idéntica a la de la 4.7.1) y la vinculación al material se aplican después, sin cambios. Las demás salidas de agente (pasos 5–10) siguen con el criterio de fechas, fuera del alcance de R-T1 (Q-T4).
- **Cierre oficial (paso 14):** solo con auditoría APROBADO (regla de H2), `Material auditado` igual al `id` fijado y el material actual igual al fijado. Si no, «CIERRE RECHAZADO», código 4, ninguna salida oficial y el pipeline vuelve al paso 13; también con `--desde 14`. **(4.8.1, R-T1)** Además:
  - con una solicitud de auditoría pendiente, ninguna aprobación anterior cierra: ni el paso 14, ni `ficha.py`, ni la comprobación de vigencia;
  - en un cierre aprobado como respuesta a una solicitud, `auditoria.md` tiene que ser esa respuesta. **(4.9, R-V1; hasta la 4.8.1 se comparaba su contenido sin formato y sin orden, lo que no acredita la identidad)** Se comprueban por separado: (1) la solicitud: exactamente una línea «Solicitud de auditoría», la de la respuesta aceptada, que `estado_pipeline.json` registra como respondida por ella y del material fijado; (2) el material, sin cambios; (3) la respuesta íntegra, con su contenido y su orden (`fiel`), salvo las transformaciones inocuas. Volver a guardarla con otros finales de línea, con BOM o en NFD no la cambia; cambiar, quitar o duplicar la línea de solicitud, reordenar palabras o líneas, añadir espacios o líneas, o sustituirla por otra retira la aprobación en la primera llamada (paso 14, `ficha.py`, `informe.py` o `resumen.py`) y en todos los destinos registrados del resumen. Sin `estado_pipeline.json`, la comprobación usa la solicitud y la huella fiel que registra `cierre_vigente.json` (4.9). Un cierre de la 4.8.1, cuya respuesta no tiene huella fiel registrada, solo se acredita con los bytes exactos (no se calcula una huella nueva para atribuírsela). **(4.9, auditoría interna Z-1 y Z-2)** Sin ningún registro de la respuesta aprobada (ni `auditoria_respuesta` ni `cierre_vigente.json`), ningún APROBADO cierra ni sigue vigente: hace falta una auditoría nueva; un `auditoria.md` que no es UTF-8 válido, o un `estado_pipeline.json` o `cierre_vigente.json` ilegibles, retiran la aprobación en lugar de interrumpir la vía (con `estado_pipeline.json` ilegible, el pipeline retira y termina con código 6);
  - en los cierres anteriores a la 4.8.1, sin solicitud, `auditoria.md` tiene que ser la que registra `cierre_vigente.json`, byte a byte.

  Continúa la regla del cierre: `ficha.py --estado concluido` sin `--provisional` aplica la misma comprobación (código 3 si falla). Con APROBADO que no nombra el material vigente se pide otra auditoría (hasta `max_correcciones_esquema`; después `no_entregable`). Los estados que no pasan por la auditoría (`no_entregable`, `pendiente_de_datos` o `modelo_no_aplicable` tempranos) se escriben como antes. **(4.8, X-a)** Si uno de esos estados llega después de un cierre (por ejemplo, `--desde 2` sin `fase1_v63.json` ni `texto/`), la ficha cerrada anterior se archiva con su retirada, la aprobación registrada se retira y el estado nuevo queda igual en la memoria del pipeline, en `estado_pipeline.json`, en `ficha.json`, en `informe.md`, en el diagnóstico y en el resumen **desde la primera ejecución**. **(4.8, X-c)** Si en el paso 14 la ficha oficial no cumple su esquema (criterio 7 †), el análisis termina en `no_entregable` por `fallo_de_implementacion`, en el paso 14 y con **código 0** (es un estado final, no un rechazo del cierre por la auditoría): ninguna ficha `no_entregable` lleva `cierre` (`ficha.py` no lo escribe en ese estado, aunque el pipeline esté en el paso 14), la ficha cerrada anterior queda archivada y el diagnóstico atribuye el fallo al esquema y dice «continuar desde el paso 13»: corregir `ficha.py` o el esquema y pedir una auditoría nueva, porque la aprobación anterior no se reutiliza. La última línea del pipeline dice, en todo estado distinto de `concluido`, el estado, la causa y el paso desde el que se continúa. Si en esa terminación el resumen no se pudo publicar (retirada pendiente, código 5), queda anotado (`resumen_pendiente`) y la ejecución siguiente, ya con las retiradas completas, vuelve a publicar la fila. Al reanudar con `--desde` desde un estado final, su diagnóstico pasa a `diagnostico.*.anterior`. `ficha.py` escribe `cierre` solo en el estado que propuso el material auditado (`ficha_provisional.json`), y rechaza `--estado concluido` con código 3 si se propuso otro (4.8, Z-a, Z-h y Z-f de la auditoría interna).
- **Marca de etapa 1:** `ficha.datos_etapa1_incompletos` = {`marca`: «con datos de etapa 1 incompletos», `causas`: la lista exacta de `entrada_v63.json → necesarios_para_listo_provisional`, cada entrada copiada entera} cuando esa lista no está vacía; si lo está, `null`. La sección 1 del informe la muestra con sus causas. No la activan los no bloqueantes ni el texto «NO LISTO», y no sustituye la revisión S-19.
- **Alcance declarado:** `alcance_v2.json` (opcional) = {`tipo`: `ensayo_exploratorio`, `aviso`: texto, `fuente`: el encargo que lo fija}. Lo escribe quien define el expediente, no un agente de juicio. Si existe, `ficha.alcance` lo conserva y el informe repite el aviso dentro de las secciones 1, 6 y 7; si no existe, no hay aviso. Un archivo mal formado detiene `ficha.py` (código 1).

### Vigencia de las salidas oficiales (reparación 4.6.1)

Una salida oficial cerrada por una auditoría (`ficha.json` con `cierre`, o con `estado_analisis = concluido`) solo es **vigente** si se cumplen las tres condiciones:
1. **Aprobación válida para el material actual:** la regla del cierre (`cierre_v2.motivo_rechazo_cierre`).
2. **Ficha e informe registrados:** la ficha (y el informe, si existe) son los registrados al cerrar en `cierre_vigente.json`, que escribe `ficha.py` al cerrar y completa `informe.py`.
3. **Mismo material:** `cierre.material_auditado` es el material aprobado vigente.

**Si no es vigente,** la salida se **archiva** como antecedente (`cierre_v2.archivar_salidas`):
- `ficha.json`, `informe.md` y `cierre_vigente.json` pasan a `historial_cierres/<n>_<material>/`, junto con una copia de la auditoría de ese momento (si había `auditoria.md`) y `RETIRADA.json`, que dice qué material aprobó, cuál es el actual y por qué se retira; su nota dice «aprobación histórica de otro material» cuando el material cambió, y «ya no está respaldada por una aprobación válida» (con el motivo) cuando el material es el mismo pero falta o no vale la aprobación;
- la fila de la empresa en el resumen activo pasa a «SIN APROBACIÓN VIGENTE · cierre anterior (APROBADO del material <id>) archivado», y la fila anterior se conserva en `resumen_v2_historial.csv`; las filas de otras empresas no se tocan;
- el estado del pipeline deja de decir `concluido` (vuelve, como mucho, al paso 13) y registra la retirada en `cierres_archivados`.

**La auditoría que aprobó no se borra ni cambia.** No se usa ningún estado financiero para representar la espera.

**Dónde se comprueba:**
- **Al empezar cada ejecución del pipeline,** también con `--desde`.
- **En el paso 11:** la salida anterior se archiva al empezar un material provisional nuevo.
- **En el rechazo del paso 14.**
- **En las llamadas directas:**
  - `ficha.py --estado concluido` sin aprobación válida archiva y termina con código 3;
  - `informe.py` oficial exige `ficha.json`; con una ficha cerrada, exige además la vigencia. Si no la hay, archiva y termina con código 3;
  - `resumen.py`, con una ficha cerrada no vigente, archiva y termina con código 3;
  - `ficha.py`, al **sustituir** una ficha cerrada vigente por otra de contenido distinto (por ejemplo, por una entrada de la ficha fuera del material auditado), archiva la anterior, escribe la nueva y termina con **código 0**, con un «AVISO» en la salida: el archivo deja el pipeline sin aprobación registrada (como en la 4.6.1), así que la ficha nueva **no es vigente** hasta una auditoría nueva, e `informe.py` y `resumen.py` la rechazan (código 3). Si debe negarse a escribirla lo decide la persona responsable (4.7.1, W-d de la auditoría interna). Dentro del pipeline, esa misma sustitución termina con **código 4** («CIERRE RECHAZADO»): el pipeline adopta el archivo que hacen los generadores, no sobrescribe su estado y no declara `concluido` sin salida oficial vigente (4.7.1, W-e).

**Una ficha oficial cerrada no se sobrescribe en silencio:** si cambia su contenido, la anterior se archiva antes. Los estados tempranos sin auditoría (ficha sin `cierre` y estado ≠ `concluido`) se publican como antes.

### Destinos registrados del resumen (reparación 4.7)

La revisión independiente reprodujo que, con `resumen_csv` configurado en `config_v2.json`, una invalidación por una vía directa (`informe.py`, `ficha.py` o `resumen.py` sin `--config`) retiraba la fila del resumen predeterminado (`resumen_v2.csv` junto al expediente) y dejaba «concluido / APROBADO» en el resumen configurado; el relanzamiento posterior ya no lo retiraba porque las salidas estaban archivadas.

- **Registro:** cada publicación de una ficha cerrada en un resumen (pipeline o `resumen.py`, con el destino configurado o con uno explícito) se anota en `publicaciones_resumen.json` del expediente, y en su respaldo `.publicaciones_resumen.respaldo.json`, que se escribe con cada cambio. El registro lleva un `registro_id` y cada entrada lleva `csv` (ruta absoluta efectiva), `empresa`, `expediente` (ruta real del expediente), `material_auditado`, `estado` (`publicada` · `retirada` · `retirada_pendiente` · `sin_archivo` · `descartada`), `fecha` y `error`. La escritura es atómica. El registro sobrevive al archivo de las salidas.
- **Retirada:** toda invalidación (pipeline, `informe.py`, `ficha.py`, `resumen.py`) retira la aprobación en todos los destinos registrados de ese expediente y en su resumen predeterminado (`resumen_v2.csv` junto a la ubicación **actual** del expediente). También retira allí una aprobación publicada antes de la 4.7 sin registrar. **Detección** (como en la 4.7): fila «APROBADO» de la empresa con la **fecha** de una ficha cerrada que el expediente archivó; la fecha se lee en ISO y en los formatos numéricos habituales de una hoja de cálculo (día/mes/año y mes/día/año, con barras; día.mes.año; día-mes-año). No se leen, por ejemplo, «3-Nov-26», «03-nov-2026» ni «2026.11.03» (4.8, precisión X-d del control de vigencia de la 4.7.1): una fila así cae en el límite residual de abajo. **Exclusión:** no se retira si es la fila de la ficha oficial vigente, comparada por su contenido publicado (estado, precio, moneda, precio de Sí, ponderado, zona, acción, cubo y motor) con los números normalizados (tolerancia relativa de 10⁻⁶). Si la exclusión falla (por ejemplo, porque una hoja de cálculo redondeó los números), la fila se retira y `resumen.py` la vuelve a publicar **en el CSV en que escribe**: es el sentido conservador (4.7.1, W-a de la auditoría interna). Si `resumen.py` escribe en otro destino, la fila retirada del predeterminado queda «SIN APROBACIÓN VIGENTE» aunque la aprobación sea vigente, hasta la siguiente publicación en él (precisión X-d). La empresa sale de la ficha, nunca del nombre de la carpeta. La fila retirada nombra el material de la ficha archivada, y ese material pasa a su historial y al registro. `resumen.py` sin ficha retira con el mismo criterio en el destino que recibe. Un destino de la llamada que ya figuraba como `retirada` y cuya fila aprobada reaparece (por ejemplo, al restaurar una copia de seguridad) se vuelve a retirar (W-f). **Límite residual:** una fila sin registrar cuya fecha se haya cambiado o ya no se pueda leer como fecha no se reconoce como publicación de este expediente (la regla V-2 protege así las filas de otros expedientes de la misma empresa, salvo cuando su fecha es ambigua entre día/mes y mes/día y una de las dos lecturas coincide con la de este expediente: entonces se retira, en el sentido conservador; precisión X-d). **En la misma llamada** (4.7.1, W-1 de la revisión independiente): `resumen.py` con una ficha cerrada no vigente, tras archivar las salidas y retirar en el destino recibido, sincroniza también los demás destinos conocidos, incluido el predeterminado; `ficha.py`, al sustituir una ficha cerrada (lo que archiva la anterior y deja el pipeline sin aprobación registrada), sincroniza igual (`cierre_v2.retirar_publicaciones`), aunque las salidas ya estén archivadas, sin buscar en el sistema de archivos. La fila afectada queda como en la 4.6.1 («SIN APROBACIÓN VIGENTE …», sin precios ni acción) y la anterior pasa al historial de ese destino; las filas de otras empresas no se tocan; un reintento no duplica el historial.
- **Ligado al expediente:** una entrada cuya ruta real es la de este expediente es propia. Si es otra:
  - **copia:** si en esa ruta sigue un expediente con un registro del **mismo** `registro_id`, este expediente es una copia del original vivo. Registra como propios los destinos equivalentes (la misma ruta relativa al expediente) que existan y sean distintos de los del original, recibe un `registro_id` nuevo y guarda las entradas del original en `heredadas_del_original`, sin tocar sus filas;
  - **original trasladado o renombrado:** si no hay en esa ruta un expediente con el mismo `registro_id` (ruta ausente, otro expediente o sin registro), las entradas se adoptan (`trasladado_desde`). Un destino solo pasa a su ruta trasladada si su carpeta registrada ya no está accesible y la trasladada sí; si la registrada sigue accesible, se conserva;
  - un registro sin `registro_id` no reconoce copias: cualquier otra ruta se trata como traslado. Límite declarado: en una copia del árbol con el original vivo, ese registro haría que la copia retirara las filas del original y dejara aprobado su propio CSV configurado. El código actual siempre escribe `registro_id`; solo un registro editado a mano o escrito por una versión intermedia no entregada lo dejaría sin él;
  - si el original se movió o se borró **antes** de que la copia resolviera su identidad, la copia adopta sus entradas y puede retirar sus filas, en el sentido conservador. Una vez resuelta, la copia solo responde de sus propios destinos;
  - **límites declarados:**
    - una copia del expediente solo, llevada a otro árbol, registra como propio el CSV equivalente de ese árbol si existe, y retira allí la fila de la empresa (extensión de H-7, conservadora);
    - si se renombra un expediente y, antes de ninguna sincronización, se coloca una copia suya en la ruta antigua, la copia se queda las publicaciones. La copia es idéntica y su cierre respalda la misma aprobación;
    - si se traslada solo el expediente, el predeterminado de la ubicación anterior no se considera suyo: una aprobación sin registrar que quede allí no se retira;
    - una invalidación por el pipeline con la configuración del árbol de destino retira en el CSV de esa configuración, que es el destino de la llamada.
- **Límite declarado (CSV compartido):** la fila del resumen se identifica por empresa. Si dos expedientes de la misma empresa publican en el mismo CSV, invalidar uno retira también la fila del otro. Es el sentido conservador: retira una aprobación, nunca la crea.
- **Fallo de acceso** (error de escritura o carpeta del destino ausente) **o registro ilegible:** la entrada queda `retirada_pendiente` con el error. Un registro ilegible no se sobrescribe, pero se retiran igualmente el destino conocido de la llamada, la aprobación sin registrar del resumen predeterminado (su detección no depende del registro; 4.7.1, W-b) y los destinos del respaldo, si es legible. El pipeline termina con **código 5** («RETIRADA PENDIENTE») y no declara nada completado. Lo comprueba al empezar y al terminar, también si la retirada pendiente nació durante la ejecución. `ficha.py`, `informe.py` y `resumen.py` también terminan con código 5, este último también sin `ficha.json`. Al recuperar el acceso, la siguiente ejecución completa la retirada.
- **CSV ausente en una carpeta accesible:** la entrada queda `sin_archivo`, no bloquea y se vuelve a comprobar en cada sincronización; si el CSV reaparece con la aprobación, se retira. Límite declarado: una carpeta accesible y vacía no se distingue de una unidad desmontada con su punto de montaje presente (código 3, no 5, hasta la siguiente sincronización).
- **Destino que no volverá (salida humana):** la persona responsable puede poner en la entrada `estado` «descartada», con `descartado_por` y `fecha_descarte` no vacíos, en el registro y en su respaldo. Desde entonces deja de bloquear. Un descarte incompleto sigue como retirada pendiente (código 5): la entrada vuelve al estado `retirada_pendiente`, conserva los campos escritos y hay que marcarla de nuevo, completa. Claude no lo hace por su cuenta.
- **Registro borrado:** se usa el respaldo, con un aviso por la salida de error. Si faltan los dos, el expediente no puede saber dónde publicó (límite residual).
- **Sincronización:** el pipeline al empezar cada ejecución (también con `--desde`) y los tres generadores comparan el registro con la vigencia (`cierre_v2.sincronizar_resumenes`): sin ficha cerrada vigente se retiran todas las publicaciones; con ella, las de otros materiales. Además, todo archivo de salidas (paso 11, rechazo del paso 14, llamadas directas) retira en los destinos registrados.
- Los estados tempranos sin auditoría se publican como antes y no se registran como aprobación.
- Correcciones tras las auditorías internas de la 4.7 (H-1 a H-9, C-1 a C-4 y F-1 a F-6): `…/2026-11_Vidrala_ensayo_4_7/CIERRE_TECNICO_BLOQUE_A.md`, §3 a §5.
- Corrección de la 4.7.1 (W-1) y de su auditoría interna (W-a, W-b, W-d, W-e y W-f): `…/2026-11_Vidrala_ensayo_4_7_1/CIERRE_TECNICO_4_7_1.md`.
- Corrección de la 4.8 (X-a y X-c) y precisiones de X-d: `…/2026-11_Vidrala_ensayo_4_8/CIERRE_TECNICO_4_8.md`; batería `pruebas/test_estados_v2.py`, obligatoria en `verificar_paquete.sh completa`.

## D.6b `comprobacion_conjunta.json` (lo escribe `comprobacion_conjunta.py`; D10, Anexo B §B.6)

Ejemplo construido sobre **la misma empresa y las mismas cifras de §D.6, suponiendo que la segunda hipótesis sí tuviera base** (cinco ejercicios de ROIC en `Historia` fila 33 en vez de tres): muestra qué habría hecho la comprobación conjunta. En el caso real de §D.6 no procede.

```json
{
  "libro_origen": "<E>_v63_evaluada.xlsx", "copia_de_prueba": "comprobacion_conjunta/<E>_conj.xlsx", "hash_copia": "…",
  "combinacion": {"B69": 0.4, "C69": 0.5, "D69": 0.1, "Palancas!D18": 0.14},
  "rangos_y_evidencia": {"B69:D69": {"rango": "MALO 0,2–0,4 · NORMAL 0,4–0,6 · BUENO 0,1–0,2", "evidencia": "p(MALO) techo 0,4: 4 de 10 ejercicios con crecimiento negativo O margen bajo el del MALO (Historia 2015–2024, filas 28–29: 2016, 2019, 2020, 2023); suelo 0,2: con las dos condiciones a la vez son 3 (2016, 2020, 2023), y 2020 fue el cierre por pandemia, no repetible según la dirección, con ventas recuperadas en 2021 (extracto p. 22): 2 de 10. p(BUENO) suelo 0,1: 1 de 10 (2021) cumplió a la vez crecimiento y margen del BUENO; techo 0,2: 2 de 10 (2017, 2021) cumplieron al menos una condición"}, "Palancas!D18": {"rango": "0,14–0,18", "evidencia": "techo 0,18 = el ROIC más alto de la propia serie de cinco ejercicios (Historia fila 33, 2021), que coincide con la tesis del BUENO: por encima de lo mejor que ya hizo, ningún hecho del extracto lo sostiene. Suelo 0,14 = el ROIC más bajo de la misma serie (2022, año de la subida de costes de materias primas, extracto p. 31), que la empresa sostuvo sin perder cuota ni precio: por debajo de lo que ya demostró en un mal año habría que suponer un deterioro que ningún hecho del extracto anuncia. La media del sector (H18) y el umbral C56 + 0,10 no se usan como límites."}},
  "coherencia_economica": "si el foso dura menos de lo que supone el BUENO, ese escenario es menos probable y su ROIC terminal cae al nivel del peor año propio; el MALO gana la probabilidad que pierde el BUENO; S2C y márgenes no mejoran a la vez que cae el ROIC",
  "recalculo_forzado_comprobado": true,
  "precio_actual": 494,
  "resultados_bajo_combinacion": {"B78": 430, "C78": 520, "D78": 900, "C83": 522, "Motor!B255": "COMPLETO Y VÁLIDO", "semaforos": ["…"], "errores_gramatica": []},
  "escalera_bajo_combinacion": {"P_estrella": 481.1, "precio_si": 481.1, "precio_escenario_malo": 430, "ponderado": 522, "zona_precio_actual": "vigilar"},
  "escalera_original": {"valores": [430, 520, 1060], "probabilidades": [0.2, 0.6, 0.2], "P_estrella": 540.8, "precio_si": 520, "precio_escenario_malo": 430, "ponderado": 610, "zona_precio_actual": "cumple_regla_k"},
  "sobrevive": false,
  "nota": "superar esta comprobación no es una garantía de seguridad; su fuerza depende de los rangos declarados"
}
```

`sobrevive` = la zona del precio actual bajo la combinación sigue siendo `cumple_regla_k` o `bajo_malo` y no aparece ningún error de gramática ni de mecánica. La copia de prueba no se entrega ni se verifica con `verificar_v63.py` (no hace falta: no sustituye al libro), pero se conserva para el estudio.

## D.7 `ficha.json` (para la capa entre empresas y el futuro Damodaran independiente)

Campos: `empresa`, `ticker`, `fecha`, `moneda`, `versiones` {`personaje`, `plantilla` = «V6.3», `gramatica`, `referencias_mecanicas`, `config`}, `hashes` {`libro_entrada`, `libro_evaluado`}, `estado_analisis` (§3.4), `causa_si_no_concluido` {`tipo`: falta_de_datos | incertidumbre_no_acotada | limite_del_modelo | fallo_de_implementacion, `detalle`}, `etapa1` {`cubo`, `precio_de_si`, `fecha`, `r`}, `cubo`, `cubo_cualitativo_fase_a`, `decision` (de D.6; en `modelo_no_aplicable` derivada de `fase_a.json` como dice §D.2; `accion` puede ser `null`), `insumos_decision_cartera` (de D.6), `motor`, `escenarios` {MALO / NORMAL / BUENO, cada uno: `historia`, `probabilidad`, `valor_accion`, `palancas` {`g15`, `m_obj`, `s2c`, `g_inf`, `roic_lp`, cada una {`referencia_mecanica`, `referencia_no_disponible_motivo`, `valor`, `desviacion`, `clase`, `confianza`}}}, `valor_ponderado`, `precio`, `escalera` (de `precio.json`, con `convencion`), `fundamento_material` (de D.6, con la lista completa) y `comprobacion_conjunta` (de D.6b si existe), `estado_libro`, `estado_evidencias`, `palanca_mas_influyente` {`nombre`, `clase`, `nota`: «información, no criterio»}, `semaforos` (lista), `salto_anio_11`, `peso_terminal`, `cambios_vs_etapa1` (las 34 celdas heredadas: {`celda`, `antes`, `despues`, `decision`, `motivo`, `evidencia_y_razonamiento`}), `predicciones` (3 × {`texto`, `fecha`, `prob`, `resultado`: null}), `incertidumbre_pendiente`, `que_lo_resolveria`, `cambiaria_de_cubo`, `autocomprobacion`, `recuento_clases` {`fundamentada`, `convencion`, `tecnico`, `sin_juicio`}, `desviaciones_justificadas` (número y lista), `avisos` (lista), `confianza_global`, `que_falta` (datos de etapa 1 o de fase 1 ausentes, con su nivel de §3.4), `revision_datos_ausentes` (de D.6: por dato, conclusión afectada, material o no, por qué), `citas` {`munger`: n, `damodaran`: n}. En los estados `pendiente_de_datos` y `modelo_no_aplicable` los campos que no existen van a `null`, nunca se inventan; en `pendiente_de_datos` tras la fase C (S-19), `decision.accion` = `null` y `causa_si_no_concluido.tipo` = `falta_de_datos` con `detalle` = los datos ausentes materiales, la conclusión que afectan y por qué.

## D.8 `informe.md` (trece secciones, en este orden; las que no aplican al estado se escriben con una línea «No aplica en estado …»)

1. Estado del análisis, cubo y conclusión en una línea (con precios si los hay). 2. Qué cambió respecto a la etapa 1 y por qué (con el motivo de D3). 3. Las seis preguntas. 4. Los tres escenarios contados. 5. Tabla de palancas: referencia mecánica → decisión → desviación → clase → por qué. 6. Lo que dice la hoja (semáforos, peso del terminal, salto del año 11, DCF inverso, tornado como información). 7. Escalera de precios (convención experimental), fundamento material (lista de hipótesis, alternativas, combinación y resultado de la comprobación conjunta, con la frase «no es una garantía de seguridad» si se superó) y los dos errores opuestos. 8. Tesis y tesis inversa. 9. Predicciones. 10. Qué me haría cambiar de cubo. 11. Autocomprobación. 12. Qué no sé y qué pediría (incluido qué no sabría Munger; la revisión de datos ausentes con qué afecta cada uno; en `pendiente_de_investigacion` o `pendiente_de_datos`, lo que haría falta para continuar). 13. Citas usadas (Munger y Damodaran, con página).

Sin preámbulos ni cierres. Frases cortas. Todo hecho con su fuente; todo juicio como juicio. Ningún tamaño de posición.

## D.9 `auditoria.md` (agente de verificación)

**(4.8.1, R-T1)** Además de los dieciséis puntos y del veredicto, la auditoría lleva exactamente una línea `Material auditado: <id de material_auditoria.json>` y exactamente una línea `Solicitud de auditoría: <id de solicitud_auditoria.json>`. Sin la segunda, o con otro identificador, el paso 13 no acepta el archivo como respuesta y sigue esperando, sin consumirlo.

Lista numerada con PASA/FALLA y una línea cada una: (1) mecánica (todos los scripts PASS; `verificar_v63.py` íntegro; estado del libro el esperado según el encargo §7.3, con recálculo forzado comprobado); (2) literalidad de C11–C13; (3) herencia: cada celda heredada con «mantiene/cambia», motivo válido y evidencia nombrada (no «como ya se dijo»); (4) gramática: ningún error; toda desviación justificada con hechos y clase válida; límites del modelo tratados como tales; (5) coherencia de las 68 con las historias; (6) citas de Munger y Damodaran con página (grep); (7) tesis inversa con hechos; (8) nada de internet ni de memoria; (9) evidencia de fase 1 usada antes de decir «no consta»; (10) escalera coherente con `precio.json` y presentada como convención; (11) **fundamento material (D10)**: la lista `hipotesis_sin_fundamento` es completa (el verificador busca por su cuenta clases *sin juicio propio* / *técnico* y Observaciones sin hechos), cada límite de cada rango está atado a un hecho de esta empresa con la explicación de por qué acota (una media sectorial, un umbral de la plantilla o la variabilidad histórica por sí sola no valen), las limitaciones sin base están registradas con lo que haría falta, la combinación toma los extremos desfavorables o explica por qué no, es económicamente coherente, el resultado y el estado son los que corresponden, y ningún texto presenta la comprobación como garantía; (12) `C104` sin ningún porcentaje, tampoco «0 %», y ningún tamaño en ficha ni informe (D16); (13) predicciones falsables y sobre el negocio; (14) autocomprobación con contenido (no frases vacías); (15) comparación honesta con la etapa 1; (16) **revisión de datos ausentes (S-19)**: una entrada por cada dato de `datos_ausentes.json`, con conclusión afectada y motivo específico, y estado coherente con la materialidad declarada. Veredicto: APROBADO / REPETIR, y en una línea qué corregir. **APROBADO exige los 16 puntos, cada uno una sola vez y todos en PASA, y la palabra «FALLA» en ninguna parte de la auditoría: cualquier FALLA es REPETIR sin excepción.** Una observación que no impide aprobar va dentro de un punto en PASA como «Aviso: …». Toda línea con forma de encabezado (número de 1–3 cifras al principio seguido de «.», «)», «:» o guion, o de una palabra en mayúsculas) tiene que ser uno de los 16 puntos válidos («N. PASA» o «N. FALLA»); cualquier otra, como «17. PENDIENTE» o «100. PASA», es REPETIR (reparación H2, 8-nov-2026; sustituye a la regla que solo bloqueaba con FALLA en 1, 4, 11, 12 o 16).

## D.10 `resumen_v2.csv`

`empresa, fecha, estado_analisis, causa_si_no_concluido, cubo_v1, cubo_v2, motor, precio, moneda, precio_escenario_malo, precio_si, ponderado, zona, accion, fundamento_material, estado_libro, palanca_mas_influyente, n_desviaciones, n_sin_juicio, n_tecnico, n_hipotesis_sin_fundamento, comprobacion_conjunta, n_datos_ausentes, n_datos_ausentes_materiales, intentos_B, intentos_C, verificacion, coste_estimado, tiempo_min`

**(4.11, revisión interna H2)** Los expedientes V6.4 publican en `resumen_v2_v64_experimental.csv`, junto al expediente, y su historial de filas retiradas es `resumen_v2_v64_experimental_historial.csv`. El nombre lo fija `config_v2_v64_experimental.json` (`resumen_csv_nombre`) y, si la configuración no fija ninguno, `plantilla_activa.json` del expediente (`cierre_v2.nombre_resumen`): también una llamada a mano con `config_v2.json` publica y retira en el archivo de la V6.4. La detección de publicaciones sin registrar anteriores a la 4.7 mira el mismo archivo. Una configuración con `resumen_csv` (una ruta fija) manda sobre todo lo anterior. Una fila V6.4 nunca comparte archivo con las filas V6.3. Las columnas son las mismas: el archivo identifica la plantilla; el modo y la marca de objetivo provisional están en la ficha y el informe.

## D.11 `diagnostico.md` y `diagnostico.json` (D18; siempre que `estado_analisis ≠ concluido`)

```json
{
  "empresa": "…", "fecha": "AAAA-MM-DD", "estado_analisis": "no_entregable",
  "causa": {"tipo": "fallo_de_implementacion", "detalle": "G2 (N2): ROIC largo plazo del MALO 0,02 ≤ g para siempre 0,025 tras 2 correcciones de la fase B; en las tres pasadas la fase B bajó el ROIC del MALO sin bajar su g", "comprobacion": "G2", "categoria": "error"},
  "paso_en_que_se_detuvo": 8,
  "intentos": {"fase_b": 3, "fase_c": 0, "auditoria": 0},
  "lo_que_sigue_valido": {"libro": "íntegro; celdas de la fase A escritas y verificadas", "cubo_cualitativo": "Vigilar", "descalificadores": "ninguno aplica", "gestion": "Buena", "seis_preguntas": true, "celdas_verificadas": ["C11", "…"]},
  "lo_que_no_es_valido": ["palancas de la fase B", "escalera"],
  "para_continuar": {"que_hace_falta": "revisar el prompt de la fase B en la regla N2 (si el ROIC a largo plazo de un escenario es ≤ g, ese escenario tiene que bajar g, no mantenerlo)", "desde_que_paso": 8, "quien": "Claude Code | José Luis (datos)"},
  "archivos": ["entrada_v63.md", "fase_a.json", "gramatica.md", "verificacion_*.txt"]
}
```

`causa.tipo` ∈ {`falta_de_datos`, `incertidumbre_no_acotada`, `limite_del_modelo`, `fallo_de_implementacion`}. `diagnostico.md` es la misma información en diez líneas legibles. Para `pendiente_de_investigacion` y `modelo_no_aplicable` el diagnóstico es breve y remite a la ficha y al informe, que existen; para `pendiente_de_datos` lista exactamente lo que falta (de `entrada_v63.md`) y, si viene de la revisión de la fase C (S-19), qué conclusión afecta cada dato y por qué, con `para_continuar` = de dónde debería salir el dato; para `no_entregable` dice qué falló, en qué paso y qué se conserva. Nunca «revisar el prompt» sin decir qué regla.

## D.12 Plantilla V6.4 experimental del motor B (encargo 4.11)

Solo en expedientes ejecutados con `--config config_v2_v64_experimental.json`. Con la V6.3, ninguno de estos archivos ni campos existe, y las salidas de la V6.3 no cambian.

- **`configuracion_economica.json`** (formato v1; validación en `scripts/configuracion_economica.py`, `ESQUEMA_RESUMIDO`).
  - Lo escribe la orquestación (o una persona), **nunca un agente de juicio**. No es una adopción.
  - Contiene el modo (`Heredado` | `Experimental`) y la `naturaleza` (ensayo, no adopción).
  - En modo experimental lleva:
    - `N1` {valor, fuente, periodo, perimetro, clase, escudo} o null;
    - `N2` {valor, perimetro, procedencia} o null;
    - `N3` {regla, existencias, deudores, acreedores, fuente};
    - `PM1` {estructura, familia, lambda, theta, convencion_anios, convencion_terminal, roic_terminal, cartera y, con P0, cartera_anual, cartera_vnc, cartera_historica[5], cartera_fuente}. Opcional: `lambda_rango` o `theta_rango` = [mín, máx], dos números ordenados dentro del dominio y con el valor activo dentro; sus extremos se calculan como variantes (revisión interna H11);
    - `trazabilidad` de cada parámetro activo (clase, confianza, fuente_o_condicion, justificacion, materialidad).
  - En modo heredado no se escriben opciones experimentales.
  - El paso 2 la escribe en el libro de datos (todas las entradas de la hoja; las no usadas, vacías). Si cambia más tarde, el pipeline la reaplica y retrocede.
- **`plantilla_activa.json`**: la selección explícita de plantilla, referencia y verificador, con sus huellas. Se detienen con código 2, sin escribir nada:
  - un expediente V6.4 que se ejecuta con la configuración V6.3;
  - al revés, un expediente que empezó con la V6.3 (libros `*_v63_base.xlsx`, `*_v63_datos.xlsx` o `*_v63_evaluada.xlsx`, o un `estado_pipeline.json` con pasos hechos, y sin `plantilla_activa.json`) que se ejecuta con la V6.4 (4.11, revisión interna H1). Para la V6.4 se prepara un expediente nuevo: con `cambiar_base.py` o con solo las entradas de partida (`etapa1/`, `fase1_v63.json` y `configuracion_economica.json`).
- **`entrada_v63.md` y `entrada_v63.json`** (paso 7): con el modo experimental, cada motor lleva `cubierto_por_configuracion_v64` (solo el B). «Calculable» se decide por los datos, simulando el modo heredado. Si la fase A elige un motor calculable no cubierto, `comprobar_entrada_v63.py` termina con código 4 («MOTOR NO CUBIERTO») y el análisis, en `no_entregable · limite_del_modelo`, con «qué hace falta»: modo heredado o la V6.3 en un expediente nuevo (revisión interna H3).
- **`configuracion_v64_variantes.json` y `.md`** (paso 10, `scripts/variantes_configuracion_v64.py`).
  - Variantes mecánicas sobre copias recalculadas del libro evaluado: heredado, activa, cada componente aislado, las estructuras compatibles y las convenciones.
  - Por variante: V, ponderado, precio de Sí, zona, conciliación y diferencias frente a la activa y al heredado.
  - Con `PM1.lambda_rango` o `theta_rango`, las variantes `parametro_minimo` y `parametro_maximo`.
  - Campos generales: `configuracion_economica_sha256`, `zonas_calculadas`, `variantes_sin_zona` y `zona_igual_en_todas_las_calculadas`, que solo es true si todas calcularon y tienen la misma zona.
  - Paso 12 (revisión interna H10): la variante «activa» tiene que dar el ponderado y el precio de Sí de `precio.json` (1e-9) y las variantes tienen que ser de la configuración actual. Si no, `no_entregable · fallo_de_implementacion`, continuar desde el paso 10.
  - Ninguna variante se elige ni se adopta.
- **`fase_c.json` → `configuracion_v64`** (obligatorio en modo experimental; lo comprueba `coherencia_v64`):
  - `parametros`: una entrada por parámetro activo, con clave, clase, confianza, materialidad, `material_para_conclusion` (booleano) y evaluación. En la 4.11, true quería decir que el parámetro es material para alguna parte de la conclusión, la acción o el precio objetivo, sin consecuencia mecánica (revisión interna H4). **Desde la 4.12 se conserva por compatibilidad** y tiene que ser `material_para_accion` o `material_para_objetivo`; la materialidad separada y el protocolo del objetivo están en §D.13;
  - `mantenimiento` {evaluacion, evidencia, estructura_mas_coherente, `adoptada` = false};
  - `zona_igual_en_variantes_calculadas` (booleano): solo puede ser true si las variantes calculadas lo respaldan.
- **`resultados.json` → `configuracion_v64`**: parámetros efectivos, validez y motivo, trazabilidad y comprobación de la «Conciliación B» (MALO, NORMAL y BUENO).
- **`ficha.json`**:
  - `versiones.plantilla` ∈ {«V6.3», «V6.4 experimental»} (se lee de `plantilla_activa.json`);
  - `configuracion_economica`: selección y configuración efectiva, con la marca de no adoptada; `variantes_calculadas.n` cuenta solo las variantes con zona y `sin_calcular` nombra las demás;
  - `limites` según la configuración activa: con R1, el del terminal sin el máximo conservado y el de la palanca S2C que no actúa en los años sin ventas por encima del máximo (revisión interna H12).
- **`informe.md`**:
  - en la línea de estado de la sección 1, con `esperar` y alguna hipótesis sin fundamento, «(provisional: lo condiciona …)» junto al precio objetivo (revisión interna H7; Anexo B §B.6.7). La ficha no tiene todavía un campo propio para esa marca: la llevan C104, `insumos_decision_cartera.fundamento` y el informe;
  - sección 14 «Plantilla y configuración económica (V6.4 experimental; no adoptada)»;
  - en la sección 7, las distancias entre precio y precio de Sí con el denominador identificado. Ejemplo: 66,52 está un 26,17 % por debajo de 90,10 (sobre el precio); 90,10 está un 35,45 % por encima de 66,52 (sobre el precio de Sí).
- **`datos_v63.md`**: sección 0, configuración V6.4 efectiva.
- **Resumen**: `resumen_v2_v64_experimental.csv` junto al expediente (§D.10).
- **Ejecución a mano** de `ficha.py`, `informe.py`, `resumen.py`, `variantes_configuracion_v64.py` o `comprobacion_conjunta.py` sobre un expediente V6.4: desde la 4.12 comprueban o resuelven la selección del expediente (`seleccion_plantilla.resolver`): sin `MUNGER_CONFIG`, usan la configuración registrada en `plantilla_activa.json` solo si sus archivos de plantilla, referencia y verificador tienen las huellas registradas; si no, terminan con código 2 sin escribir nada. Nunca producen una salida aparentemente V6.4 con referencias o configuración V6.3 (antes, revisión interna O5).

**Cambio de base** (`scripts/cambiar_base.py`, encargo 4.11 §7). Se usa para preparar un expediente de ensayo con otra base económica, sin tocar el original.

- `preparar CAMBIO.json`:
  - crea un expediente nuevo (nunca sobrescribe) y mueve lo heredado a `antecedentes/` con inventario;
  - deja una copia de ensayo de la etapa 1 en la que solo cambian las celdas declaradas;
  - reescribe la evidencia activa declarada del Control maestro; los textos anteriores van a `antecedentes/evidencia_anterior.json`;
  - retira las notas que reintroducían la base anterior (`antecedentes/notas_retiradas.json`);
  - separa las fechas: ejecución real, base, precio, acciones y publicación de las fuentes;
  - escribe `resultados/cambio_de_base.json/.md`.
- `comprobar CAMBIO.json`: concordancia entre la configuración, `fase1_v63.json` y el libro de datos, y búsqueda de restos de la base anterior en la evidencia activa y en las notas.
  - Busca en las columnas G–M de las filas de juicio y en las E–N de las de datos (filas 17–82 y 107–175 del Control maestro).
  - El resultado es «CONCUERDA Y SIN RESTOS» o la lista de celdas.
  - Además informa, sin contar para el resultado, de los textos con la base anterior fuera de ese rango (cabecera y bloque de auditoría 84–102): `textos_de_la_base_anterior_fuera_de_la_evidencia_activa` (revisión interna H9).
  - `comprobar CAMBIO.json LIBRO` examina el libro que se le pasa, el de datos o el evaluado. En la 4.11 se guardó la de los dos libros del control y del piloto.

## D.13 Vigencia, materialidad, protocolo del objetivo, coherencia y trazabilidad (encargo 4.12)

Solo cambia el comportamiento de los expedientes V6.4; las salidas de la V6.3 y del modo heredado de la V6.4 no cambian, salvo la vigencia, que es general.

**Vigencia antes del rechazo (§3).** Si una llamada de `pipeline.py` llega con una selección de plantilla que no se acredita y el material auditado del expediente cambió (o falta, o no se puede leer), primero se retiran la aprobación y las publicaciones registradas (como en cualquier otra primera llamada) y después se detiene: código 2, o 5 si una retirada queda pendiente. Con el material intacto, el rechazo no cambia nada. `plantilla_activa.json` solo se escribe después de esa comprobación. Diferencia intencionada respecto de la 4.11: añadir `configuracion_economica.json` a un expediente V6.3 cerrado cambia su material y ahora retira su aprobación en la primera llamada (el rechazo H1 se mantiene: para la V6.4 se prepara un expediente nuevo).

**Protocolo experimental del objetivo (§4).** `configuracion_economica.json → protocolo_objetivo` ∈ {`bloqueo_del_objetivo`, `objetivo_condicionado`}. Lo declara la orquestación en cada expediente experimental nuevo; es un ensayo, no una regla adoptada. Es opcional (las configuraciones de la 4.11 siguen siendo válidas) y no se admite en modo heredado, donde rige el Anexo B §B.6.7. `scripts/objetivo_v64.py` (solo lee) calcula lo que corresponde y `pipeline.coherencia_v64` lo exige:

| Situación (conclusión provisional `esperar` con la zona por encima del precio de Sí) | Tratamiento | Estado · cubo · acción · precio objetivo |
|---|---|---|
| Nada condiciona el objetivo | `objetivo_emitido` | `concluido` · Vigilar · `esperar` · precio de Sí |
| Condicionantes y `objetivo_condicionado`, con la acción sostenida en todo el ámbito calculado | `objetivo_condicionado` | `concluido` · Vigilar · `esperar` · precio de Sí, marcado como condicionado (provisional) |
| Condicionantes y `objetivo_condicionado`, sin la acción sostenida | `objetivo_bloqueado` (origen `accion_no_sostenida_en_el_ambito`) | `pendiente_de_investigacion` · Vigilar · `null` · `null` |
| Condicionantes y `bloqueo_del_objetivo` | `objetivo_bloqueado` (origen `protocolo_de_bloqueo`) | `pendiente_de_datos` · Vigilar · `null` · `null` (lectura S-19 del objetivo) |
| Condicionantes sin protocolo declarado | `objetivo_sin_protocolo` | el pipeline termina en `no_entregable · limite_del_modelo` en el paso 10, explica las dos lecturas y no emite ningún objetivo oficial |

Con `comprar`, `descartar`, `demasiado_dificil`, un dato ausente material (S-19 manda antes) o `esperar` por una condición que no es de precio, el tratamiento es `sin_objetivo` y rigen las reglas de siempre. **Condicionantes** = los parámetros con `material_para_objetivo = true` y `fundamento_suficiente = false`, toda la lista D10 (`hipotesis_sin_fundamento`, como en §B.6.7) y los avisos de dominio que la fase C declara materiales (`limite:<id>`). **Hipótesis no cubiertas por el ámbito** (revisión interna R3) = las que condicionan el objetivo y ningún escenario calculado varía: un subparámetro de P-M1 (familia, parámetro, convenciones, ROIC del terminal, cartera) solo cuenta como cubierto por una variante que lo varía de forma aislada, con P-M1 activa, o por la comprobación conjunta; las variantes que quitan P-M1 entera («heredado», componentes aislados, «activa sin P-M1») no calculan ninguna alternativa suya. El rango calculado incluye la activa y los escenarios del ámbito (`rango_calculado.n_escenarios` cuenta los escenarios, sin la activa). **Acción sostenida** = ningún escenario del ámbito calculado (todas las variantes con zona, sin la activa, y, si se ejecutó, la comprobación conjunta y sus alternativas) cambia la acción por la zona (por encima del precio de Sí = `caro` o `vigilar`; cumple la regla = `cumple_regla_k` o `bajo_malo`) y ningún condicionante es material para la acción. El rango del precio de Sí de ese ámbito no es un intervalo de confianza ni mide toda la incertidumbre económica, y «la zona no cambia» no prueba robustez frente a hipótesis no exploradas.

**Materialidad separada (§4).** `fase_c.json → configuracion_v64.parametros[]` añade `material_para_accion` (true · false · null = no determinada: ninguna variante calculada lo varía), `material_para_objetivo`, `fundamento_suficiente` (false = hipótesis sin fundamento suficiente: no es un dato ausente), `informacion_que_falta` (obligatoria con fundamento insuficiente) y `ambito` (exactamente las variantes calculadas que lo varían: `configuracion_v64_variantes.json → variantes[].parametros_variados`). `false` en la acción exige variantes que lo varíen y que no cambien la acción. El bloque `configuracion_v64.objetivo` lleva `protocolo`, `hipotesis_que_condicionan`, `informacion_no_disponible`, `accion_sostenida_en_ambito`, `ambito`, `tratamiento`, `origen_del_bloqueo` y `motivo`, y la decisión de la fase C tiene que ser la de la tabla. Las comprobaciones cruzan esos campos con la acción, el estado, el objetivo y los datos ausentes.

**Compra (§4 y §9).** Con `comprar`, todo parámetro activo con `fundamento_suficiente = false` va en `hipotesis_sin_fundamento` (celda `Configuración V6.4!REF`, `configuracion_economica.celda_principal`); los numéricos activos (B11 con N1, B21 con N2, B38 o B39 según la familia) se mueven en la combinación de la comprobación conjunta, que no puede mover un parámetro inactivo (código 3 del script y error de coherencia); los no numéricos van en `comprobacion_conjunta.alternativas_no_numericas` y `comprobacion_conjunta.py` recalcula, una a una y con la misma combinación, cada alternativa definida (`configuracion_economica.alternativas`; una sin definir no sobrevive) → `comprobacion_conjunta.json → por_alternativa`, `sobrevive_combinacion_activa` y `sobrevive` (todas). Un objetivo provisional no exime una compra de nada, y un aviso de dominio material no admite comprar.

**Salidas del objetivo (§4).** `ficha.json → objetivo` (solo V6.4 experimental con fase C de la 4.12): `protocolo`, `tratamiento`, `estado_del_objetivo`, `origen_del_bloqueo`, `valor_calculado_condicional` (el precio de Sí calculado), `precio_objetivo_emitido`, `provisional`, `hipotesis_que_lo_condicionan` (con la información que falta), `hipotesis_no_cubiertas_por_el_ambito`, `accion_sostenida_en_ambito`, `rango_calculado` (precio de Sí y ponderado, escenarios y naturaleza), `materialidad` (datos ausentes materiales, hipótesis sin fundamento suficiente, materiales para la acción y para el objetivo, no determinadas, límites del modelo materiales y ámbito por parámetro, también el aislado) y, sin protocolo, `lecturas_posibles`. `decision.precio_objetivo` sigue siendo el objetivo emitido (compatibilidad). Un expediente con fase C de la 4.11 no tiene `objetivo` (no se reconstruye lo que esa fase C no evaluó). El informe lo muestra en la línea de estado de la sección 1 y en la sección 14; la línea de estado da el rango calculado y su ámbito con cualquier tratamiento (condicionado, bloqueado o sin protocolo), sin llamarlo intervalo de confianza (corrección de la 4.12 tras la auditoría del cierre de bloqueo de Vidrala). `resumen_v2_v64_experimental.csv` añade al final las columnas `protocolo_objetivo`, `estado_del_objetivo`, `valor_calculado_condicional`, `precio_objetivo_emitido`, `objetivo_provisional`, `hipotesis_que_condicionan`, `rango_precio_si_min`, `rango_precio_si_max`, `escenarios_calculados` y `aptitud_de_uso`; un resumen V6.4 anterior migra su cabecera la primera vez que se escribe, y el de la V6.3 no cambia.

**Aptitud de uso, separada de la auditoría (§9).** `ficha.json → aptitud_de_uso` (solo V6.4 experimental, como `objetivo`): `caracter` («experimental»), `version` de la entrega, `uso_que_permite`, `no_apto_para`, `distinta_de_la_auditoria` y `evaluacion` (dónde está la evaluación de la entrega). Es la evaluación de la versión del código, no del expediente, y se actualiza con cada entrega (`ficha.py → APTITUD_V64`). El informe la muestra en la sección 1, debajo de la línea de estado, y el resumen V6.4 en la columna `aptitud_de_uso`. No forma parte de la auditoría de 16 puntos: no cambia su contrato ni ningún veredicto, y una auditoría APROBADO o el estado «concluido» no acreditan la aptitud para decidir con dinero real. Las salidas V6.3 y V6.4 heredadas no la llevan.

**Correspondencia de las variantes (§5).** `configuracion_v64_variantes.json` (formato «4.12») registra la instantánea de las entradas económicas del libro de origen (`entradas_economicas.py`: las 58 entradas materiales de la relación independiente de la V6.3, con la Historia expandida, y las de «Configuración V6.4» sin sus metadatos de fuente, período o perímetro; desde la revisión interna de la 4.12 (R1), también la fila 13 de la Historia, adquisiciones netas, que entra en D_hist y F_hist y con ellas en f y f_fija: relación «4.12+H13», en `entradas_economicas.version`. Una instantánea guardada con la relación anterior, sin `version`, se compara con esa relación, y su fila 13 con la del libro de la variante «activa» del paso 10; sin ese libro no se acredita), la huella económica de la configuración (sin trazabilidad, naturaleza ni protocolo) y el vector de escenarios de la activa. El paso 10 reutiliza las variantes si no cambia ninguna entrada económica, ni la configuración económica, ni k; el paso 12 exige la misma instantánea, la misma configuración económica y el mismo vector (V, probabilidades, ponderado, precio de Sí, precio y zona); el formato anterior se rechaza. Un cambio editorial (textos, Observaciones, trazabilidad) no repite las valoraciones; uno económico sí. Un cambio solo del protocolo repite la fase C (paso 10) con las mismas variantes y exige una auditoría nueva.

**Avisos de dominio (§5).** `dominios_v64.py` calcula, sobre la copia recalculada de la activa, `inversion_fija_para_crecer_negativa`, `factor_de_reestimacion` (lectura sin umbral, con las estructuras que reestiman: f, D_hist, Rh y el λ en que f deja de estar definida), `terminal_r1_sin_maximo_conservado` y `s2c_inerte`, con valores y motivo; van en las variantes, la ficha (`configuracion_economica.avisos_de_dominio`) y la sección 14. No hay umbrales adoptados ni recortes. La fase C evalúa cada aviso activo y el factor en `configuracion_v64.avisos_de_dominio` (`material_para_conclusion`, `consecuencia`); uno material condiciona el objetivo como `limite:<id>` y no admite comprar.

**Lecturas con bases parciales (§5).** La gramática (G7, con una nota en `gramatica.md`), las referencias mecánicas y la sección 0 de `datos_v63.md` dicen que usan las bases heredadas (tipo de la Historia y S2C sin f); con P0, el valor sin crecimiento (BL) y «cuánto pagas por crecer» no incluyen la cartera. La ficha lo lleva en `configuracion_economica.limites`. No se presentan como comprobación del modelo experimental.

**Juicios de la fase C que nada contrasta (revisión interna R5).** El tratamiento del objetivo sale mecánicamente de dos banderas por parámetro que declara la fase C, `material_para_objetivo` y `fundamento_suficiente`; las reglas comprueban que sean booleanas y coherentes con el ámbito y la acción, pero no las contrastan con la clase que da la configuración ni con los efectos calculados. Con «comprar», la exigencia de D10 solo alcanza a los parámetros marcados sin fundamento suficiente. Es una limitación declarada (informe integrado de la 4.12, §9.6) y una decisión de la propuesta humana (D412-FUNDAMENTO).

**Cadena de trazabilidad (§5).** El paso 12 de los expedientes V6.4 escribe `cadena_trazabilidad.json` (en el material auditado), `cadena_trazabilidad.md` y `verificacion_trazabilidad.txt` con `scripts/trazabilidad_v64.py` (también se puede ejecutar a mano sobre un expediente V6.3): fuente → dato extraído → transformación o supuesto → entrada del modelo → cálculo → resultado → conclusión, con identificadores por clase (D- dato publicado, C- cálculo derivado, V- convención, H- hipótesis), la magnitud (stock, flujo, precio, acciones, tasa o parámetro), las fechas separadas (ejecución, base, precio, acciones, revisión de fuentes) y avisos de unidad, signo, fecha, stock frente a flujo, celdas vacías y ceros pendientes de verificación (un dato desconocido nunca es cero). Desde la revisión interna de la 4.12: en un libro V6.4 incluye la fila 13 de la Historia (R1), y en el precio, la capitalización y las acciones avisa si el período o la transformación nombran otra fecha que la declarada, o si el resultado que escribe la transformación («… = N») no es el valor que entra en el modelo (R4). Los avisos no deciden nada.

**Reconstrucción portable (§6).** Para el artefacto entregado se exige la huella estricta (`referencia/SHA256_entregables_V6.4_experimental.txt`); para una reconstrucción en otro entorno, el mismo contenido miembro a miembro (`scripts/comparar_zip.py`), además de fórmulas, formatos, controles, validaciones, relaciones e inventario. No se promete identidad binaria entre entornos: la huella del archivo depende de la compresión.

**Sección 0 antes de la fase A (§8).** Mientras el libro conserva el motor de la etapa 1 y la configuración solo es inválida por el motor, la sección 0 de `datos_v63.md` no dice «configuración válida: False … revisa Análisis C62»: dice que la validez depende del motor que elija la fase A, que la fase A elige como si la configuración no existiera y que otro motor termina en el límite del modelo experimental, un resultado legítimo. Después de la fase A (volcado con `--referencias-mecanicas`) la sección vuelve a mostrar la validez del libro.
