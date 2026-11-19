#!/usr/bin/env python3
"""ahold_f4 · registro de entradas completo para el sellado, antes de la auditoría (encargo del coordinador, 19-nov-2026). Solo el registro: no cambia
valores del libro ni fases. Cada entrada tocada queda PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo; no se usa `sellar`.
 1) hipótesis y convenciones de las fases: fundamento, alternativas, límites y valor con el texto VIGENTE de las fases de ahold_f4 (Control maestro N del libro);
 2) C38 (valor intrínseco de Simply Wall St, tercero sin bytes): entrada de JUICIO declarada no material (regla N1) con la prueba de qué celdas la usan; solo deja
    de bloquear si un revisor independiente sella ese juicio de materialidad. C88 no se toca: en ahold_f4 es un derivado de cifras publicadas (capitalizaciones de
    AR2025 p. 65 y FCF de la Historia con la regla espejo), no una lectura de terceros.
Uso: python3 -I registro_antes_de_auditoria_ahold_f4.py CARPETA_EMPRESA RASTRO.json"""
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


def pendiente(e, nota, fuente_examinada=None):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, ahold_f4, antes de la auditoría] {nota} · Comprobación anterior: {c0.get('extractor')} / {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:300]}",
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
    proc = f"Control maestro!N{ev.get('fila')} del libro (Ahold_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e["clase"], e["valor_modelo"] = clase, INST["celdas"].get(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")), "fundamento": fund,
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    pendiente(e, f"texto vigente de la fase en ahold_f4 (Control maestro!N{ev.get('fila')}); clase «{clase}» según la fase («{clase_decl}»)"
                 + (f"; valor {antes!r} → {e['valor_modelo']!r}" if not VE._igual_exacto(antes, e["valor_modelo"]) else ""), proc)
    hip.append(k)

# ---------------------------------------------------------------------------------------------- 2) C38: juicio de materialidad (N1)
assert INST["ambito"]["Análisis!C38"] == "juicio"
e = por["Análisis!C38"]
e["material"] = False
e["justificacion_materialidad"] = (
    "Valor intrínseco de un tercero (Simply Wall St, 61,27 €) sin bytes: solo es contexto. Celdas del libro Ahold_v63_evaluada.xlsx (búsqueda en todas las fórmulas "
    "de las 11 hojas) que leen Análisis!C38: Análisis!C39 (descuento frente a la fuente externa) y su rótulo D39; Análisis!C87 (valor ponderado frente a la fuente "
    "externa) y su rótulo D87; el texto de Análisis!E43; el aviso Motor!E235 (solo si C38 no es numérico). Ninguna fórmula de la valoración (Motor, escenarios, precio "
    "de Sí, precio ponderado, FCF base) ni de la Historia la usa; no está en la instantánea de entradas_economicas (universo de cálculo): es una entrada de juicio "
    "(DATOS_JUICIO_ANALISIS). Juicio: las fases A y B no la citan (fase_a.json, fase_b.json: 0 menciones de C38, C39, C87 ni Simply Wall St). La fase C la menciona "
    "solo en su autocomprobación (fase_c.json → autocomprobacion[1]) para descartarla: «El valor de Simply Wall St (61,27, C38) es dato no verificable y no lo usé». "
    "Con otro valor (o vacía) cambiarían C39, C87 y esos rótulos informativos, no el precio de Sí, la acción ni el estado. Límite: la fase C la vio; el revisor decide "
    "si eso la hace material.")
e["incidencia"] = "«Dato no verificable»: tercero sin bytes ni captura en el expediente; es contexto, no dato verificado."
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis C39, D39, C87, D87, E43; Motor E235); fase_a.json, fase_b.json, fase_c.json")

reg["nota_ahold_f4_antes_de_auditoria"] = (f"{HOY}, {EXT}: hipótesis y convenciones con el texto vigente de las fases de ahold_f4; C38 no material (N1), pendiente de que "
                                           "un revisor selle ese juicio. Rastro: resultados/registro_antes_de_auditoria_ahold_f4.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/registro_antes_de_auditoria_ahold_f4.py", "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p),
           "hipotesis_actualizadas": hip, "cambios": cambios}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", len(cambios), "hipótesis", len(hip))
