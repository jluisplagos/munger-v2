#!/usr/bin/env python3
"""jumbo_g · correcciones del registro tras el sellado (munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/jumbo/revision_registro/REVISION_SELLADO.md
@ 50f0b71; producto 3355b60), por encargo del coordinador (19-nov-2026). Solo el registro: no cambia valores del libro ni fases. Cada entrada tocada queda
PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo.
 1) C46 y C40: la conciliación aún decía «C76 = 160, fase B de jumbo_e» (317,617 / 255,108); se pone al día con C76 = 150 (fase B de jumbo_g) y los valores del
    recálculo del paso 9 (resultados/recalculo_dependientes_Jumbo.json; en el expediente, recalculo_dependientes.json).
 2) C38 y C88: entradas de JUICIO (no de cálculo) leídas de terceros sin bytes. Se declaran no materiales con su justificación y la prueba de qué celdas las usan
    (regla N1 de verificacion_entradas.py: solo dejan de bloquear si un revisor independiente sella ese juicio de materialidad).
 3) C31: no hay en texto/ una fuente equivalente al informe del 1S-2025 (inventario 316,66 y deudores 90,28 a 30-jun-2025); queda pendiente, con la aproximación
    que sí sale del expediente anotada como incidencia.
Uso: python3 -I corregir_registro_tras_sellado_jumbo_g.py CARPETA_EMPRESA RASTRO.json"""
import copy, hashlib, json, os, sys
C, RASTRO = sys.argv[1:3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402
HOY, EXT = "2026-11-19", "Claude orquestación"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
p = os.path.join(C, VE.REGISTRO)
antes_sha = h(p)
reg = json.load(open(p, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
INST = VE.universo(C)
rec = json.load(open(os.path.join(C, "..", "resultados", "recalculo_dependientes_Jumbo.json"), encoding="utf-8"))["vigente"]
cambios = []


def pendiente(e, nota, fuente_examinada=None):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, jumbo_g, tras REVISION_SELLADO.md @ 50f0b71] {nota} · Comprobación anterior: {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:400]}",
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "motivo": nota, "antes": antes, "despues": copy.deepcopy(e)})


# ---------------------------------------------------------------------------------------------- 1) C46 y C40
c76 = INST["celdas"]["Análisis!C76"]
assert c76 == 150
for k in ("Análisis!C46", "Análisis!C40"):
    r = rec[k]
    assert r["celdas_de_juicio"] == {"Análisis!C76": 150} and VE._igual_exacto(r["valor"], INST["celdas"][k]), k
    e = por[k]
    vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else INST["celdas"][o]) for o in e["derivacion"]["origenes"]}
    ex = VE._eval_formula_exacta(e["derivacion"]["formula"], vals)
    assert VE._importe_libro_exacto(ex, INST["celdas"][k]), k
    if k == "Análisis!C46":
        conc = ("C46 = media 2023–2025 de [CFO + dividendos cobrados de la cartera cotizada + intereses cobrados − s × (intereses cobrados − cupones de bonos)], con "
                "s = C76 × 3 ÷ Σ caja 2023–2025 = 150 × 3 ÷ 1.415,485114 = 0,317912 (decisiones P-O1 (c), J1 y J2; C76 = 150, hipótesis vigente de la fase B de jumbo_g). "
                "CFO 323,918862 / 300,687098 / 296,912917; dividendos 0,133043 / 0,828384 / 1,8762; intereses cobrados 18,490712 / 13,791382 / 9,91679; cupones "
                "0,595837 / 0,594641 / 0,595058; caja 434,000394 / 444,815962 / 536,668758. Resultado exacto 317,902497 → libro 317,902 (redondeo a 3 decimales admitido "
                "en importe). Es el recálculo determinista del paso 9 tras la fase B (recalculo_dependientes.json → vigente → Análisis!C46: valor declarado 317,617 "
                "con C76 = 160 → 317,902 con C76 = 150; copia en resultados/recalculo_dependientes_Jumbo.json).")
    else:
        conc = ("FCF del accionista 2025 con la definición de C46: CFO 296,9129 − capex 38,384 − intereses de arrendamientos 2,3258 − principal 9,7272 + dividendos "
                "1,8762 + intereses cobrados 9,91679 − C76 ÷ round(caja media, 4) × (9,91679 − cupones 0,595058), con C76 = 150 (hipótesis vigente de la fase B de "
                "jumbo_g) y caja media 471,8284 → 255,305398; libro 255,305 (redondeo a 3 decimales admitido en importe). Es el recálculo determinista del paso 9 tras "
                "la fase B (recalculo_dependientes.json → vigente → Análisis!C40: valor declarado 255,108 con C76 = 160 → 255,305 con C76 = 150; copia en "
                "resultados/recalculo_dependientes_Jumbo.json).")
    e["derivacion"]["conciliacion"] = conc
    e["incidencia"] = None
    pendiente(e, f"conciliación al día con C76 = 150 (fase B de jumbo_g) y el recálculo del paso 9 ({r['valor']}; exacto {float(ex):.6f}); la fórmula y los orígenes no cambian",
              "recalculo_dependientes.json; fórmula y orígenes del registro")

# ---------------------------------------------------------------------------------------------- 2) C38 y C88: juicio de materialidad
for k in ("Análisis!C38", "Análisis!C88"):
    assert INST["ambito"][k] == "juicio", k
PRUEBA_LIBRO = ("Celdas del libro Jumbo_v63_evaluada.xlsx (búsqueda en todas las fórmulas de las 11 hojas) que leen {k}: {usos}. Ninguna fórmula de la valoración "
                "(Motor, escenarios, precio de Sí, precio ponderado, FCF base) ni de la Historia la usa; no está en la instantánea de entradas_economicas (universo de "
                "cálculo): es una entrada de juicio (DATOS_JUICIO_ANALISIS).")
e = por["Análisis!C38"]
e["material"] = False
e["justificacion_materialidad"] = (
    "Valor intrínseco de un tercero (Simply Wall St, 33,04 €) sin bytes: solo es contexto. "
    + PRUEBA_LIBRO.format(k="Análisis!C38", usos="Análisis!C39 (descuento frente a la fuente externa) y su rótulo D39; Análisis!C87 (valor ponderado frente a la fuente "
                          "externa) y su rótulo D87; el texto de Análisis!E43; el aviso Motor!E235 (solo si C38 no es numérico)")
    + " Juicio: las fases A y B no la citan (fase_a.json, fase_b.json: 0 menciones de C38, C39, C87 ni Simply Wall St). La fase C la examina en su autocomprobación "
      "(fase_c.json → autocomprobacion[1]) solo para descartarla: «ninguna [Observación] cita C38 … no uso C38 ni como contraste de la conclusión»; la cercanía del precio "
      "de Sí (33,42 €) con 33,04 € queda anotada como casual. Ninguna celda de juicio ni la conclusión dependen de su valor: con otro valor (o vacía) cambiarían C39, C87 "
      "y esos rótulos informativos, no el precio de Sí, la acción ni el estado. Límite: la fase C la vio; el revisor decide si eso la hace material.")
e["incidencia"] = ("«Dato no verificable»: tercero sin bytes ni captura. En el libro sigue «Rellenado y verificado» (Control maestro F39, evidencia de la etapa 1); "
                   "cambiar esa marca exige tocar la etapa 1 y regenerar el libro: no se hace.")
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis C39, D39, C87, D87, E43; Motor E235); fase_a.json, fase_b.json, fase_c.json")
e = por["Análisis!C88"]
e["material"] = False
e["justificacion_materialidad"] = (
    "P/FCF histórico de terceros (MarketScreener / StockAnalysis, 15,2x) sin bytes, que el expediente ya marca «Dato no verificable» (Control maestro F73). "
    + PRUEBA_LIBRO.format(k="Análisis!C88", usos="solo Análisis!D88, un rótulo informativo («ℹ … x implícito vs … x histórico · investiga la diferencia»); las banderas "
                          "Motor!B311 y Motor!C311 leen D88 pero solo saltan si D88 contiene «BANDERA» o «REVISAR», que su fórmula nunca escribe")
    + " Juicio: ninguna fase la cita (fase_a.json, fase_b.json, fase_c.json: 0 menciones de C88 ni de su valor). Con otro valor (o vacía) solo cambiaría el rótulo D88.")
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis D88; Motor B311, C311); fase_a.json, fase_b.json, fase_c.json")

# ---------------------------------------------------------------------------------------------- 3) C31
e = por["Análisis!C31"]
e["incidencia"] = (
    "SIN FUENTE EQUIVALENTE EN EL EXPEDIENTE: el apoyo (Control maestro L34/M34) cita el informe del 1S-2025 (inventario 316,66 y deudores 90,28 a 30-jun-2025), que no "
    "está en texto/; el semestral del H1-2026 compara su balance con el 31-dic-2025 (inventario 325.764.610 frente a 310.497.568, PDF p. 25; deudores 86.024.991 frente a "
    "75.235.066, p. 25) y no publica el nivel a 30-jun-2025. Aproximación con fuentes del expediente (no es la cifra publicada): inventario a 31-dic-2024 260.870.129 "
    "(AR2025 PDF p. 150) + aumento del 1S-2025 56.587.171 (H1-2026 PDF p. 61, «(Increase)/ decrease in inventories», columna 01.01–30.06.2025) = 317,46 mm frente a 316,66 "
    "(la diferencia, 0,80 mm, son partidas sin caja como deterioros); con ella el inventario sube un 2,6 % frente a ventas del 1S +4,42 % (519.257.126 frente a 497.278.437, "
    "H1-2026 PDF p. 23): mismo veredicto «No». Los deudores a 30-jun-2025 no se pueden aproximar con lo conservado. Queda pendiente: hace falta el informe del 1S-2025 "
    "o reescribir el apoyo en la evidencia del libro (decisión de la orquestación).")
pendiente(e, "sin fuente equivalente en texto/ para el 1S-2025; se anota la aproximación con fuentes del expediente; queda pendiente",
          "texto/jumbo-h1-2026-financial-results.txt [PDF PAGE 23, 25, 61]; texto/jumbo-annual-report-fy2025.txt [PDF PAGE 150]")

reg["nota_jumbo_g_tras_sellado"] = (f"{HOY}, {EXT}: tras REVISION_SELLADO.md @ 50f0b71 — conciliación de C46/C40 con C76 = 150; C38 y C88 declaradas no materiales (N1) con "
                                    "su prueba, pendientes de que un revisor selle ese juicio; C31 sin fuente equivalente (pendiente). Rastro: resultados/registro_tras_sellado_jumbo_g.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/corregir_registro_tras_sellado_jumbo_g.py", "revision": "REVISION_SELLADO.md @ 50f0b71 (auxiliar); producto 3355b60",
           "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p), "cambios": cambios}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", len(cambios))
