#!/usr/bin/env python3
"""vinci_b · registro de entradas completo para el sellado, antes de la auditoría (encargo del coordinador, 20-nov-2026). Solo el registro: no cambia
valores del libro ni fases. Cada entrada tocada queda PENDIENTE de revisor, extractor «Claude orquestación», sin vínculo; no se usa `sellar`.
 1) hipótesis y convenciones de las fases: fundamento, alternativas, límites y valor con el texto VIGENTE de las fases de vinci_b (Control maestro N del libro);
 3) entradas selladas cuya huella ya no vale porque cambió su fila de evidencia del Control maestro, sin cambio de dato:
    vuelven a pendiente con la causa anotada.
 2) C38 (Fair Value de Simply Wall St, sin bytes) y C88 (mediana P/FCF de la etapa 1 con precios de cierre de año no conservados): entradas de JUICIO declaradas
    no materiales (regla N1) con la prueba de qué celdas las usan; solo dejan de bloquear si un revisor independiente sella ese juicio de materialidad.
 4) C46 y C40 (límite 9.4.1: el verificador no detecta compensaciones parciales entre componentes reales): cada componente con su valor, su celda u origen y su
    página y cita, para que el revisor los compruebe uno a uno; C52 no está en el universo del registro.
 6) C31: fuente precisa de la comparación junio frente a junio (semestral 2026, p. 1 y 3).
 5) decisiones del constructor a la vista del revisor: H87 (PPA 2021 = 0) como no_aplicable y las seis series F1 (H86:K86, J87, K87) citadas del URD del propio
    ejercicio en lugar del comparativo del informe siguiente que declara motor_a_f1.json.
Uso: python3 -I registro_antes_de_auditoria_vinci_b.py CARPETA_EMPRESA RASTRO.json"""
import copy, hashlib, json, os, re, sys
C, RASTRO = sys.argv[1:3]
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "..", "..", "scripts"))
import verificacion_entradas as VE  # noqa: E402
HOY, EXT = "2026-11-20", "Claude orquestación"
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
p = os.path.join(C, VE.REGISTRO)
antes_sha = h(p)
reg = json.load(open(p, encoding="utf-8"))
por = {e["celda"]: e for e in reg["entradas"]}
INST = VE.universo(C)
EVID = VE.evidencia_libro(C)
cambios = []
# entradas selladas cuya huella dejó de valer sin que cambie su dato (p. ej. la fila de evidencia del Control maestro cambió en vinci_b): se listan antes de tocar nada
DESACT = {x.split(": ", 1)[0] for x in VE.comprobar(C)["desactualizadas"] if "huella del vínculo distinta" in x}


def pendiente(e, nota, fuente_examinada=None):
    antes = copy.deepcopy(e)
    c0 = e.get("comprobacion") or {}
    e["comprobacion"] = {"extractor": EXT, "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": fuente_examinada,
                         "nota": f"[{EXT}, {HOY}, vinci_b, antes de la auditoría] {nota} · Comprobación anterior: {c0.get('extractor')} / {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:300]}",
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
    proc = f"Control maestro!N{ev.get('fila')} del libro (Vinci_v63_evaluada.xlsx)" + (f"; escrito en la fase {fase} (celdas_{fase}.json)" if fase else "")
    antes = e.get("valor_modelo")
    e["clase"], e["valor_modelo"] = clase, INST["celdas"].get(k)
    e["hipotesis"] = {
        "identificacion": ("V-" if clase == "convencion" else "H-") + str(e.get("id")), "fundamento": fund,
        "alternativas": " · ".join(x.group(1).strip() for x in (ref, sust) if x) or "El texto de la fase no declara alternativa.",
        "limites": ((f"Rango declarado: {rango.group(1)}." if rango else "Sin rango declarado.") + f" Confianza declarada: {conf}. Es juicio del inversor "
                    f"({ev.get('D')}), clase declarada «{clase_decl}»: no es un dato publicado ni se demuestra con una firma; las cifras y páginas de apoyo "
                    "no se contrastan en este registro (apoyan el juicio, no son entradas). Si una fase lo reescribe, este fundamento deja de describir la celda."),
        "procedencia": proc}
    pendiente(e, f"texto vigente de la fase en vinci_b (Control maestro!N{ev.get('fila')}); clase «{clase}» según la fase («{clase_decl}»)"
                 + (f"; valor {antes!r} → {e['valor_modelo']!r}" if not VE._igual_exacto(antes, e["valor_modelo"]) else ""), proc)
    hip.append(k)

# ---------------------------------------------------------------------------------------------- 2) C38 y C88: juicio de materialidad (N1)
for k in ("Análisis!C38", "Análisis!C88"):
    assert INST["ambito"][k] == "juicio", k
LIBRO = ("Celdas del libro Vinci_v63_evaluada.xlsx (búsqueda en todas las fórmulas de las 11 hojas) que leen {k}: {usos}. Ninguna fórmula de la valoración "
         "(Motor, escenarios, precio de Sí, precio ponderado, FCF base) ni de la Historia la usa; no está en la instantánea de entradas_economicas (universo de "
         "cálculo): es una entrada de juicio (DATOS_JUICIO_ANALISIS).")
e = por["Análisis!C38"]
e["material"] = False
e["justificacion_materialidad"] = (
    f"Fair Value de un tercero (Simply Wall St, {INST['celdas']['Análisis!C38']} €) sin bytes: solo es contexto. "
    + LIBRO.format(k="Análisis!C38", usos="Análisis!C39 (descuento frente a la fuente externa) y su rótulo D39; Análisis!C87 (valor ponderado frente a la fuente externa) y "
                   "su rótulo D87; el texto de Análisis!E43; el aviso Motor!E235 (solo si C38 no es numérico)")
    + " Juicio: las fases A y B no la citan (fase_a.json, fase_b.json: 0 menciones de C38, C39, C87 ni Simply Wall St). La fase C la menciona solo en su autocomprobación "
      "(fase_c.json → autocomprobacion[1]) para descartarla: «El Fair Value ajeno (111,79) no entra en nada». Con otro "
      "valor (o vacía) cambiarían C39, C87 y esos rótulos informativos, no el precio de Sí, la acción ni el estado. Límite: la fase C la vio; "
      "el revisor decide si eso la hace material.")
e["incidencia"] = "«Dato no verificable»: tercero sin bytes ni captura en el expediente; es contexto, no dato verificado."
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis C39, D39, C87, D87, E43; Motor E235); fase_a.json, fase_b.json, fase_c.json")
e = por["Análisis!C88"]
e["material"] = False
e["justificacion_materialidad"] = (
    f"Mediana del P/FCF de fin de año 2019–2025 sin 2020 ({INST['celdas']['Análisis!C88']}x) calculada por la etapa 1 con precios de cierre de año que no están conservados en el expediente (convención: no es una cifra publicada ni reproducible). "
    + LIBRO.format(k="Análisis!C88", usos="solo Análisis!D88, un rótulo informativo («ℹ … x implícito vs … x histórico · investiga la diferencia»); las banderas "
                   "Motor!B311 y Motor!C311 leen D88 pero solo saltan si D88 contiene «BANDERA» o «REVISAR», que su fórmula nunca escribe")
    + " Juicio: ninguna fase la cita (fase_a.json, fase_b.json, fase_c.json: 0 menciones de C88, D88 ni de su fuente). Con otro valor (o vacía) solo cambiaría el rótulo D88.")
pendiente(e, "declarada no material (regla N1) con la prueba de qué celdas la usan; pendiente de que un revisor independiente selle ese juicio de materialidad",
          "fórmulas del libro (Análisis D88; Motor B311, C311); fase_a.json, fase_b.json, fase_c.json")


# ---------------------------------------------------------------------------------------------- 4) C46 y C40: cada componente con su origen (límite 9.4.1)
def componentes(k):
    d = por[k]["derivacion"]
    filas = []
    for o in d["origenes"]:
        eo = por[o]
        f = eo.get("fuente") or {}
        v = eo.get("valor_modelo") if o.startswith("aux:") else INST["celdas"].get(o)
        if f.get("archivo"):
            org = f"{f['archivo']} [PDF PAGE {f.get('pagina')}], «{str(f.get('cita'))[:140]}» (valor_fuente {f.get('valor_fuente')}, signo {f.get('signo')})"
        else:
            sub = (eo.get("derivacion") or {})
            org = f"derivado: {sub.get('formula')} — {str(sub.get('conciliacion'))[:200]}"
        filas.append(f"{o} = {v} ← {org}")
    return filas


NOTA941 = ("LÍMITE 9.4.1: el verificador comprueba que la fórmula reproduce el libro con todos sus orígenes, pero no detecta compensaciones parciales entre componentes "
           "reales (un componente mal leído que otro compensa): el revisor comprueba cada componente en su página, uno a uno. ")
e = por["Análisis!C46"]
e["derivacion"]["conciliacion"] = (e["derivacion"]["conciliacion"] + " · " + NOTA941 + "Normalización F1-CIRC (motor_a_f1.json → normalizacion_circulante, regla "
    "«circulante_a_cero», decisiones V-CIRC (a) y V-ANCLA (a), 19-nov-2026): la caja base excluye el circulante entero; su efecto es la media 2023–2025 de la fila 14, "
    "(−1.463 − 2.311 − 2.496) / 3 = −2.090 (conciliacion_fcf_base, componente C46). El dividendo de 2023 se lee en la línea «Other» de la nota 3.1 del URD 2024 "
    "(PDF p. 348), que el URD 2025 rotula «Dividends received from unconsolidated companies» (decisión documentada en fase1_v63.json → analisis.C46). COMPONENTES: "
    + " | ".join(componentes("Análisis!C46")))
pendiente(e, "conciliación con cada componente y su origen (límite 9.4.1) y la normalización F1-CIRC; fórmula y valor sin cambios")
e = por["Análisis!C40"]
e["derivacion"]["conciliacion"] = (e["derivacion"]["conciliacion"] + " · " + NOTA941 + "Misma definición que C46 (sin la entrada de circulante: fila 14 de 2025 = "
    "−2.496). COMPONENTES: " + " | ".join(componentes("Análisis!C40")))
pendiente(e, "conciliación con cada componente y su origen (límite 9.4.1); fórmula y valor sin cambios")
e = por["aux:vinci-urd-2024_p348_div_2023"]
e["incidencia"] = ("Decisión de la orquestación (fase1_v63.json → analisis.C46): el dividendo de sociedades no consolidadas de 2023 se lee en la línea «Other» del cuadro de la "
                   "nota 3.1 del URD 2024 (PDF p. 348), sin rótulo propio; el URD 2025 rotula la misma línea «Dividends received from unconsolidated companies 40 41» (PDF p. 370, "
                   "mismo 41 de 2024) y el URD 2023 la da como «Other 31 20» (PDF p. 170). El revisor confirma que la línea es el dividendo.")
pendiente(e, "incidencia: la línea «Other» como dividendo de 2023 (decisión documentada); cifra y cita sin cambios", (e.get("comprobacion") or {}).get("fuente_examinada"))

# ---------------------------------------------------------------------------------------------- 5) decisiones del constructor en la capa F1
DEC = ("DECISIÓN DEL CONSTRUCTOR (registro_entradas_vinci_b.py): se cita el URD del propio ejercicio y no el comparativo del informe siguiente que declara "
       "motor_a_f1.json, porque ese comparativo publica la cifra entre paréntesis dentro de una frase («(€{v} million…») y el contraste de signo (R415-SIGNO) la lee "
       "como «signo indeterminado» (comprobado el {hoy} con _cita_cifra): la entrada quedaría pendiente para siempre. Las dos fuentes dan la misma cifra (ver «reexpresado»); "
       "el revisor comprueba las dos.")
for k in ("Historia!H86", "Historia!I86", "Historia!J86", "Historia!K86", "Historia!J87", "Historia!K87"):
    e = por[k]
    e["incidencia"] = DEC.format(v=e["valor_modelo"], hoy=HOY)
    pendiente(e, "incidencia: documentada la decisión de citar el URD del propio ejercicio (R415-SIGNO); cifra, cita y fuente sin cambios",
              (e.get("comprobacion") or {}).get("fuente_examinada"))
e = por["Historia!H87"]
e["incidencia"] = ("DECISIÓN DEL CONSTRUCTOR: motor_a_f1.json declara la PPA de 2021 como cero por lectura (series.da_ppa.2021, F1-SERIES-CERO, pendiente de revisor); "
                   "en el registro va como no_aplicable porque la página no imprime un 0 de la partida (un cero_comprobado exige la cifra en la cita). La compra de Cobra IS "
                   "se cerró el 31-dic-2021: no hubo amortización de su PPA ese año. Límite: la frase no prueba por sí sola que no haya otras PPA.")
pendiente(e, "incidencia: documentada la decisión no_aplicable frente al cero por lectura de motor_a_f1.json; justificación sin cambios", (e.get("comprobacion") or {}).get("fuente_examinada"))

# ---------------------------------------------------------------------------------------------- 6) C31: fuente precisa de la comparación junio frente a junio
e = por["Análisis!C31"]
HY = "texto/vinci-hy-interim-fs-2026.txt"
for pag, cita in ((1, "Revenue (*)"), (3, "Trade and other receivables"), (3, "Inventories and work in progress")):
    assert cita in open(os.path.join(C, HY), encoding="utf-8").read(), cita
e["incidencia"] = ("FUENTE PRECISA (el apoyo del libro cita «H1 p.~20»): estados financieros semestrales del 1S-2026, texto/vinci-hy-interim-fs-2026.txt — [PDF PAGE 3] "
                   "«Trade and other receivables 20,923 20,451 19,504» (30/06/2026, 30/06/2025, 31/12/2025): +2,31 % junio frente a junio; «Inventories and work in progress "
                   "1,754 1,808 1,700»; cobros + inventarios 22.677 frente a 22.259 = +1,88 %; [PDF PAGE 1] «Revenue (*) 35,597 34,852 74,599» (1S-2026, 1S-2025, 2025): "
                   "+2,14 %. Reproducen las cifras del apoyo (Control maestro M34). El veredicto «No» es la decisión del inversor (23-oct-2026) de no contar la diferencia de "
                   "0,17 pp por Fletcher; con la lectura literal sería «Sí».")
pendiente(e, "incidencia con la fuente precisa del semestral 2026 (p. 1 y 3) que reproduce el apoyo; clase y fundamento sin cambios", f"{HY} [PDF PAGE 1, 3]")

# ---------------------------------------------------------------------------------------------- 3) sellos que ya no valen por un cambio de evidencia
resellar = []
for k in sorted(DESACT):
    e = por[k]
    if INST["tipos"].get(k) == "hipótesis" or k in hip or not VE._igual_exacto(e.get("valor_modelo"), INST["celdas"].get(k)):
        continue
    ev = EVID.get(k) or {}
    pendiente(e, ("el sello anterior no vale: su huella incluye la fila de evidencia del Control maestro de la celda (fila " + str(ev.get("fila")) + "), que cambió en "
                  "vinci_b; el dato y la fuente del registro no cambian. Vuelve a revisarse con la evidencia vigente: "
                  "F «" + str(ev.get("F")) + "», J «" + str(ev.get("J"))[:400] + "»"), (e.get("comprobacion") or {}).get("fuente_examinada"))
    resellar.append(k)

reg["nota_vinci_b_antes_de_auditoria"] = (f"{HOY}, {EXT}: hipótesis y convenciones con el texto vigente de las fases de vinci_b; C38 y C88 no materiales (N1), pendientes de que "
                                           "un revisor selle ese juicio; C46/C40 con sus componentes; decisiones de la capa F1 documentadas. Rastro: resultados/registro_antes_de_auditoria_vinci_b.json")
json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": HOY, "guion": "resultados/scripts/registro_antes_de_auditoria_vinci_b.py", "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p),
           "hipotesis_actualizadas": hip, "sellos_por_cambio_de_evidencia": resellar, "cambios": cambios}, open(RASTRO, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("cambiadas", len(cambios), "hipótesis", len(hip))
