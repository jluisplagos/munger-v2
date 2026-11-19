#!/usr/bin/env python3
"""zoetis_t1d · registro de entradas completo para el sellado, antes de la auditoría (encargo del coordinador, 19-nov-2026). Solo el registro: no cambia
valores del libro ni fases. Cada entrada tocada queda PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo; no se usa `sellar`.
 1) hipótesis y convenciones de las fases: fundamento, alternativas, límites y valor con el texto VIGENTE de las fases de zoetis_t1d (Control maestro N del libro);
 3) entradas selladas en zoetis_t1c cuya huella ya no vale porque cambió su fila de evidencia del Control maestro (decisión Z-MIN), sin cambio de dato:
    vuelven a pendiente con la causa anotada.
 2) C38 (Fair Value de Simply Wall St) y C88 (P/FCF histórico de digrin.com): lecturas de terceros sin bytes, entradas de JUICIO declaradas no
    materiales (regla N1) con la prueba de qué celdas las usan; solo dejan de bloquear si un revisor independiente sella ese juicio de materialidad.
    En zoetis_t1d la fase A eligió el motor B y la conclusión es «Demasiado difícil»; ni C38 ni C88 intervienen en ella.
Uso: python3 -I registro_antes_de_auditoria_zoetis_t1d.py CARPETA_EMPRESA RASTRO.json"""
import copy, hashlib, json, os, re, sys
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
EVID = VE.evidencia_libro(C)
cambios = []
# entradas selladas cuya huella dejó de valer sin que cambie su dato (p. ej. la fila de evidencia del Control maestro cambió en zoetis_t1d): se listan antes de tocar nada
DESACT = {x.split(": ", 1)[0] for x in VE.comprobar(C)["desactualizadas"] if "huella del vínculo distinta" in x}


def pendiente(e, nota, fuente_examinada=None):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, zoetis_t1d, antes de la auditoría] {nota} · Comprobación anterior: {c0.get('extractor')} / {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:300]}",
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "motivo": nota, "antes": antes, "despues": copy.deepcopy(e)})


# ---------------------------------------------------------------------------------------------- 1) hipótesis y convenciones
FASES = {}
for f_ in ("A", "B", "C"):
    p_ = os.path.join(C, f"celdas_{f_}.json")
    if os.path.exists(p_):
        for kk in json.load(open(p_, encoding="utf-8")):
            if "!" in kk:
                FASES[kk.replace("'", "")] = f_
hip = []
for k, e in por.items():
    if k.startswith("aux:") or INST["tipos"].get(k) != "hipótesis" or k == "Historia!C85":
        continue
    ev = EVID.get(k) or {}
    n = str(ev.get("N") or "")
    m_cl = re.match(r"\[Clase: ([^\]]+)\] \[Confianza: ([^\]]+)\]", n)
    if not m_cl:
        raise SystemExit(f"{k}: sin texto de fase en Control maestro N")
    clase_decl, conf = m_cl.group(1), m_cl.group(2)
    clase = "convencion" if clase_decl.startswith("convenci") else "hipotesis"
    fund = n + (f" [Evidencia preparada, Control maestro!M{ev['fila']}: {ev['M']}]" if ev.get("M") else "")
    h0 = e.get("hipotesis") or {}
    if h0.get("fundamento") == fund and e.get("clase") == clase and VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(k)):
        continue
    ref = re.search(r"(Referencia mecánica:.*?)(?=\s*Apoyo:|\s*Lo sustituiría:|$)", n, re.S)
    sust = re.search(r"(Lo sustituiría:.*)$", n, re.S)
    rango = re.search(r"(Rango[^.]*?\d[^.]*?)\.(?:\s|$)", n)
    fase = FASES.get(k)
    proc = f"Control maestro!N{ev.get('fila')} del libro (Zoetis_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e["clase"], e["valor_modelo"] = clase, INST["celdas"].get(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")), "fundamento": fund,
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    pendiente(e, f"texto vigente de la fase en zoetis_t1d (Control maestro!N{ev.get('fila')}); clase «{clase}» según la fase («{clase_decl}»)"
                 + (f"; valor {antes!r} → {e['valor_modelo']!r}" if not VE._igual_exacto(antes, e["valor_modelo"]) else ""), proc)
    hip.append(k)

# ---------------------------------------------------------------------------------------------- 2) C38 y C88: juicio de materialidad (N1)
for k in ("Análisis!C38", "Análisis!C88"):
    assert INST["ambito"][k] == "juicio", k
LIBRO = ("Celdas del libro Zoetis_v63_evaluada.xlsx (búsqueda en todas las fórmulas de las 11 hojas) que leen {k}: {usos}. Ninguna fórmula de la valoración "
         "(Motor, escenarios, precio de Sí, precio ponderado, FCF base) ni de la Historia la usa; no está en la instantánea de entradas_economicas (universo de "
         "cálculo): es una entrada de juicio (DATOS_JUICIO_ANALISIS).")
e = por["Análisis!C38"]
e["material"] = False
e["justificacion_materialidad"] = (
    f"Fair Value de un tercero (Simply Wall St, {INST['celdas']['Análisis!C38']} USD) sin bytes: solo es contexto. "
    + LIBRO.format(k="Análisis!C38", usos="Análisis!C39 (descuento frente a la fuente externa) y su rótulo D39; Análisis!C87 (valor ponderado frente a la fuente externa) y "
                   "su rótulo D87; el texto de Análisis!E43; el aviso Motor!E235 (solo si C38 no es numérico)")
    + " Juicio: las fases A y B no la citan (fase_a.json, fase_b.json: 0 menciones de C38, C39, C87 ni Simply Wall St). La fase C la menciona solo en su autocomprobación "
      "(fase_c.json → autocomprobacion[1]) para descartarla: «No uso el Fair Value de Simply Wall St (197,36, no verificable) ni el objetivo de analistas (96)». Con otro "
      "valor (o vacía) cambiarían C39, C87 y esos rótulos informativos, no el precio de Sí, la acción ni el estado («Demasiado difícil», motor B). Límite: la fase C la vio; "
      "el revisor decide si eso la hace material.")
e["incidencia"] = "«Dato no verificable»: tercero sin bytes ni captura en el expediente; es contexto, no dato verificado."
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis C39, D39, C87, D87, E43; Motor E235); fase_a.json, fase_b.json, fase_c.json")
e = por["Análisis!C88"]
e["material"] = False
e["justificacion_materialidad"] = (
    f"P/FCF histórico de un tercero (digrin.com, {INST['celdas']['Análisis!C88']}x) sin bytes, que el expediente marca «Dato no verificable». "
    + LIBRO.format(k="Análisis!C88", usos="solo Análisis!D88, un rótulo informativo («ℹ … x implícito vs … x histórico · investiga la diferencia»); las banderas "
                   "Motor!B311 y Motor!C311 leen D88 pero solo saltan si D88 contiene «BANDERA» o «REVISAR», que su fórmula nunca escribe")
    + " Juicio: ninguna fase la cita (fase_a.json, fase_b.json, fase_c.json: 0 menciones de C88, D88 ni de su fuente). Con otro valor (o vacía) solo cambiaría el rótulo D88.")
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis D88; Motor B311, C311); fase_a.json, fase_b.json, fase_c.json")

# ---------------------------------------------------------------------------------------------- 3) sellos que ya no valen por un cambio de evidencia
resellar = []
for k in sorted(DESACT):
    e = por[k]
    if INST["tipos"].get(k) == "hipótesis" or k in hip or not VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(k)):
        continue
    ev = EVID.get(k) or {}
    pendiente(e, ("el sello anterior no vale: su huella incluye la fila de evidencia del Control maestro de la celda (fila " + str(ev.get("fila")) + "), que cambió en "
                  "zoetis_t1d (decisión Z-MIN de los minoritarios deficitarios); el dato y la fuente del registro no cambian. Vuelve a revisarse con la evidencia vigente: "
                  "F «" + str(ev.get("F")) + "», J «" + str(ev.get("J"))[:400] + "»"), (e.get("comprobacion") or {}).get("fuente_examinada"))
    resellar.append(k)

reg["nota_zoetis_t1d_antes_de_auditoria"] = (f"{HOY}, {EXT}: hipótesis y convenciones con el texto vigente de las fases de zoetis_t1d; C38 y C88 no materiales (N1), pendientes de que "
                                           "un revisor selle ese juicio. Rastro: resultados/registro_antes_de_auditoria_zoetis_t1d.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/registro_antes_de_auditoria_zoetis_t1d.py", "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p),
           "hipotesis_actualizadas": hip, "sellos_por_cambio_de_evidencia": resellar, "cambios": cambios}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", len(cambios), "hipótesis", len(hip))
