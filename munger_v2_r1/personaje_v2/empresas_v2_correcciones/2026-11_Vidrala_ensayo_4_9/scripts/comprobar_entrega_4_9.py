#!/usr/bin/env python3
"""Control de la entrega 4.9 (R-V1 y N4). Solo escribe en temporales.

Uso (desde munger_v2_r1/, después de `bash verificar_paquete.sh completa`, sin otras pruebas en paralelo: usa LibreOffice):
    python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/scripts/comprobar_entrega_4_9.py
Tarda unos 10–11 minutos (vuelve a ejecutar las 31 mutaciones, las dos baterías de R-V1 y los recálculos de N4).
Resultado esperado: «RESULTADO: 39 de 39 comprobaciones cumplen.» y salida idéntica a resultados/comprobar_entrega_4_9_salida.txt.

Tipos: «reejecuta» vuelve a ejecutar un script y compara con lo conservado; «recalcula» recalcula un dato desde los archivos;
«constata» comprueba que un archivo existe o dice lo que debe decir.
"""
import csv
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
PV2 = os.path.dirname(CORR)
RAIZ = os.path.dirname(PV2)
SCR = os.path.join(AQUI, "scripts")
REPRO, RES, N4, PROP = (os.path.join(AQUI, x) for x in ("reproduccion", "resultados", "n4", "propuestas"))
PY = sys.executable
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
CAMBIADOS_FRENTE_A_4_8_1 = {"CAMBIOS_ARCHIVOS.txt", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "VERSION", "verificar_paquete.sh",
                            "personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/DECISIONES.md",
                            "personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/pipeline.py", "personaje_v2/scripts/ficha.py", "personaje_v2/scripts/resumen.py",
                            "personaje_v2/scripts/informe.py"}
NUEVOS_FUERA_DEL_EXPEDIENTE = {"personaje_v2/pruebas/test_integridad_auditoria_v2.py"}
TMP = tempfile.mkdtemp(prefix="control49_")
N_ANTES = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reproduccion", "test_integridad_con_codigo_4_8_1.json"), encoding="utf-8"))
N_ANTES = f"{sum(1 for x in N_ANTES['pruebas'] if x['pasa'])}/{len(N_ANTES['pruebas'])}"


def comprobar(tipo, nombre, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    TIPOS[tipo] += 1
    print(f"{'CUMPLE  ' if cond else 'NO CUMPLE'} · [{tipo}] {nombre}" + (f" · {det}" if det else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.isfile(p) else ""


def manifiesto(p):
    return {l.rstrip("\n").split("  ", 1)[1]: l.split("  ", 1)[0] for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")}


def corre(args, cwd=RAIZ, timeout=3600):
    r = subprocess.run([PY, "-B", *args], capture_output=True, text=True, cwd=cwd, timeout=timeout, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return r.returncode, r.stdout + r.stderr


def estados(p):
    return [(x["grupo"], x["prueba"], x["pasa"]) for x in json.load(open(p, encoding="utf-8"))["pruebas"]]


def sin_rutas(o):
    """Matriz o propuestas sin los campos que dependen de la carpeta de salida."""
    o = json.loads(json.dumps(o))
    o.pop("efectos", None)
    return o


try:
    print("ENTREGA 4.9 · R-V1 y N4 · controles (solo escriben en temporales)\n" + "=" * 100)
    print("1. CONSERVACIÓN")
    m481 = manifiesto(os.path.join(REPRO, "MANIFIESTO_4_8_1.txt"))
    dif = sorted(p for p, h in m481.items() if sha(os.path.join(RAIZ, p)) != h)
    actuales = {os.path.relpath(os.path.join(r, f), RAIZ) for r, ds, fs in os.walk(RAIZ) for f in fs if "__pycache__" not in r}
    nuevos = {p for p in manifiesto(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt")) if p not in m481}
    nuevos_fuera = {p for p in nuevos if not p.startswith("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/")}
    comprobar("recalcula", f"Frente al manifiesto de la 4.8.1 ({len(m481)} archivos) solo cambian los archivos declarados y ninguno desaparece; originales, expedientes anteriores, libro de referencia y decisiones registradas intactos",
              set(dif) == CAMBIADOS_FRENTE_A_4_8_1 - {"MANIFIESTO_SHA256.txt"} and all(os.path.exists(os.path.join(RAIZ, p)) for p in m481),
              ", ".join(sorted(set(dif) ^ CAMBIADOS_FRENTE_A_4_8_1)) or f"{len(dif)} cambiados, todos declarados")
    comprobar("recalcula", "Los archivos nuevos del manifiesto están en el expediente 4.9, salvo la batería nueva de R-V1", nuevos_fuera == NUEVOS_FUERA_DEL_EXPEDIENTE, ", ".join(sorted(nuevos_fuera)))
    p1 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_5", "Vidrala", "fase1_decisiones.json")
    ref = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
    dec = json.load(open(os.path.join(ref, "fase1_decisiones.json"), encoding="utf-8"))
    comprobar("recalcula", "El registro humano de P1 conserva su huella b4e47afc…c445a4 y fase1_decisiones.json de la referencia no cambia: ninguna de las 38 entradas está registrada (ningún cero confirmado por la IA)",
              (sha(p1) or "").startswith("b4e47afc") and sha(p1).endswith("c445a4") and sha(os.path.join(ref, "fase1_decisiones.json")) == m481["personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala/fase1_decisiones.json"],
              f"partidas registradas: {', '.join(k for k in dec if not k.startswith('_'))}")
    sys.path.insert(0, os.path.join(PV2, "scripts"))
    import pipeline  # noqa: E402
    import cierre_v2 as CIE  # noqa: E402
    h2 = hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest()
    comprobar("recalcula", "La regla H2 (Pipeline.veredicto_auditoria) es idéntica a la de la 4.7.1, la 4.8 y la 4.8.1", h2 == "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422", h2[:16])
    comprobar("recalcula", "Las copias del código de la 4.8.1 de reproduccion/codigo_4_8_1/ (cierre_v2.py, pipeline.py, ficha.py, resumen.py e informe.py: todo el código que cambia la 4.9) tienen las huellas del manifiesto de la 4.8.1",
              all(sha(os.path.join(REPRO, "codigo_4_8_1", f)) == m481[f"personaje_v2/scripts/{f}"] for f in ("cierre_v2.py", "pipeline.py", "ficha.py", "resumen.py", "informe.py")))

    print("2. R-V1 · INTEGRIDAD DE LA RESPUESTA DE AUDITORÍA VIGENTE")
    bat = os.path.join(PV2, "pruebas", "test_integridad_auditoria_v2.py")
    j49 = os.path.join(TMP, "despues.json")
    rc, out = corre([bat, "--json", j49], cwd=PV2)
    comprobar("reejecuta", "Batería de integridad con el código actual: 103/103 y el mismo estado de cada prueba que la salida conservada",
              rc == 0 and "103/103 pruebas de integridad de la auditoría vigente PASAN" in out and estados(j49) == estados(os.path.join(RES, "test_integridad_auditoria_v2.json")), (out.strip().splitlines() or [""])[-1])
    j481 = os.path.join(TMP, "antes.json")
    rc, out = corre([bat, "--codigo", os.path.join(REPRO, "codigo_4_8_1"), "--json", j481], cwd=PV2)
    comprobar("reejecuta", f"La misma batería con el código de la 4.8.1 reproduce el defecto ({N_ANTES}) con el mismo estado de cada prueba que la reproducción conservada",
              rc == 1 and f"{N_ANTES} pruebas" in out and estados(j481) == estados(os.path.join(REPRO, "test_integridad_con_codigo_4_8_1.json")), (out.strip().splitlines() or [""])[-1])
    antes = {(g, p): ok for g, p, ok in estados(j481)}
    clave = [k for k in antes if k[0].startswith("B") and k[1].startswith(("solicitud cambiada", "solicitud eliminada", "solicitud duplicada", "mismas palabras"))]
    comprobar("recalcula", "Con el código 4.8.1, la solicitud cambiada, eliminada o duplicada y las mismas palabras con otro significado siguen APROBADO por las cuatro vías (16 casos)",
              len(clave) == 16 and not any(antes[k] for k in clave), f"{len(clave)} casos")
    zh = [k for k in antes if k[0].startswith("H")]
    comprobar("recalcula", "Hallazgos Z-1 y Z-2 de la auditoría interna: con el código 4.8.1 fallan los casos sin registro de la respuesta, no UTF-8 y archivos de control ilegibles (el defecto era anterior a la 4.9); con el actual pasan todos",
              len(zh) >= 14 and sum(1 for k in zh if not antes[k]) >= 12 and all(ok for g, p_, ok in estados(j49) if g.startswith("H")), f"{sum(1 for k in zh if not antes[k])} de {len(zh)} fallan con el 4.8.1")
    zi = [k for k in antes if k[0].startswith("I")]
    comprobar("recalcula", "Hallazgos V-1 a V-3 del control de vigencia: con el código 4.8.1 fallan los casos de material_auditoria.json y ficha.json ilegibles, JSON que no es un objeto, carpetas y el registro sin estado; con el actual pasan todos",
              len(zi) >= 15 and sum(1 for k in zi if not antes[k]) >= 12 and all(ok for g, p_, ok in estados(j49) if g.startswith("I")), f"{sum(1 for k in zi if not antes[k])} de {len(zi)} fallan con el 4.8.1")
    e46 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6", "Vidrala")
    m46 = CIE.motivo_rechazo_cierre(e46, pipeline.Pipeline.veredicto_auditoria, json.load(open(os.path.join(e46, "estado_pipeline.json"), encoding="utf-8")), "Vidrala") or ""
    comprobar("recalcula", "Consecuencia declarada de Z-1 sobre el expediente histórico de la 4.6 (sin cierre_vigente.json): motivo_rechazo_cierre ya no lo acepta («no consta la respuesta de auditoría aprobada»), por eso su control da 23 de 24; el expediente no cambia",
              m46.startswith("no consta la respuesta de auditoría aprobada") and sha(os.path.join(e46, "auditoria.md")) == m481["personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6/Vidrala/auditoria.md"], m46[:60])
    rc, out = corre([os.path.join(SCR, "mutar_rv1.py"), "--salida", os.path.join(TMP, "mut.json")])
    m_act, m_con = json.load(open(os.path.join(TMP, "mut.json"), encoding="utf-8")), json.load(open(os.path.join(RES, "mutaciones_rv1.json"), encoding="utf-8"))
    comprobar("reejecuta", "Mutaciones del código de R-V1 (también las de los límites de la lista cerrada, de Z-1 y Z-2 y de V-1 a V-3 y W-1 a W-4): las 31 hacen fallar la batería (detección igual a la conservada)",
              rc == 0 and m_act["detectadas"] == m_act["total"] == 31 and [(x["id"], x["detectada"]) for x in m_act["mutaciones"]] == [(x["id"], x["detectada"]) for x in m_con["mutaciones"]], f"{m_act['detectadas']} de {m_act['total']}")
    for nombre in ("comprobar_integracion_verificador_49.py", os.path.join("..", "..", "2026-11_Vidrala_ensayo_4_8_1", "scripts", "comprobar_integracion_verificador_481.py")):
        rc, out = corre([os.path.join(SCR, nombre)])
        comprobar("reejecuta", f"Control de integración del verificador {os.path.basename(nombre)}: 13 de 13", rc == 0 and "RESULTADO: 13 de 13 comprobaciones cumplen." in out)
    v = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    pos = [v.find(f'echo "== batería {x}') for x in ("de integridad de la auditoría vigente", "de solicitudes de auditoría", "de coherencia de estados", "del resumen", "de cierre")]
    comprobar("constata", "verificar_paquete.sh: el bloque de integridad (mínimo 103) va antes de los de solicitudes, estados, resumen y cierre, en ese orden",
              all(p >= 0 for p in pos) and pos == sorted(pos) and '"${n_tot:-0}" -ge 103 ]; then\n    echo "$linea"; echo "RESULTADO integridad: PASA"' in v)
    t = CIE.TRANSFORMACIONES_INOCUAS
    base = "Aviso: La evidencia respalda el crecimiento; la reposición queda pendiente.\nVEREDICTO: APROBADO\n"
    comprobar("recalcula", "Ejemplo del encargo: las dos frases tienen la misma huella de contenido (detector A) y distinta huella fiel (identidad B); CRLF no cambia la huella fiel",
              CIE.huella_contenido(base) == CIE.huella_contenido(base.replace("el crecimiento; la reposición", "la reposición; el crecimiento"))
              and CIE.huella_fiel(base) != CIE.huella_fiel(base.replace("el crecimiento; la reposición", "la reposición; el crecimiento"))
              and CIE.huella_fiel(base) == CIE.huella_fiel(base.replace("\n", "\r\n")) and len(t) == 4)
    an = leer(os.path.join(PV2, "ANEXO_D_salidas_y_formatos.md"))
    comprobar("constata", "Anexo D: la identidad de la respuesta aceptada se comprueba por solicitud, material y huella fiel, con la lista cerrada de transformaciones inocuas",
              "4.9, R-V1" in an and "TRANSFORMACIONES_INOCUAS" in an and "`fiel`" in an)

    print("3. N4 · CEROS PENDIENTES DE VIDRALA")
    sal = os.path.join(TMP, "n4")
    os.makedirs(os.path.join(sal, "efectos"))
    rc, out = corre([os.path.join(SCR, "efectos_n4.py"), "--salida", os.path.join(sal, "efectos")])
    e_act, e_con = (json.load(open(os.path.join(x, "efectos", "efectos_n4.json"), encoding="utf-8")) for x in (sal, N4))
    mismo = [(x["variante"], x["valores"], x["delta"]) for x in e_act["variantes"]] == [(x["variante"], x["valores"], x["delta"]) for x in e_con["variantes"]]
    leeme = leer(os.path.join(sal, "efectos", "copias", "LEEME.txt"))
    comprobar("reejecuta", "efectos_n4.py: el recálculo forzado de la base reproduce la referencia, los valores y efectos de las 10 variantes son idénticos a los conservados y las copias llevan su LEEME de copias exploratorias",
              rc == 0 and e_act["recalculo_base_reproduce_referencia"] and mismo and leeme.startswith("COPIAS EXPLORATORIAS") and leeme == leer(os.path.join(N4, "efectos", "copias", "LEEME.txt")), f"{len(e_act['variantes'])} variantes")
    rc, out = corre([os.path.join(SCR, "n4_investigacion.py"), "--salida", sal, "--propuestas", os.path.join(sal, "prop")])
    m_act = json.load(open(os.path.join(sal, "matriz_n4.json"), encoding="utf-8"))
    m_con = json.load(open(os.path.join(N4, "matriz_n4.json"), encoding="utf-8"))
    p_act = json.load(open(os.path.join(sal, "prop", "propuestas_n4_sin_firmar.json"), encoding="utf-8"))
    p_con = json.load(open(os.path.join(PROP, "propuestas_n4_sin_firmar.json"), encoding="utf-8"))
    comprobar("reejecuta", "n4_investigacion.py: matriz, recuento, CSV y propuestas idénticos a los conservados",
              rc == 0 and sin_rutas(m_act) == sin_rutas(m_con) and p_act == p_con and leer(os.path.join(sal, "matriz_n4.csv")) == leer(os.path.join(N4, "matriz_n4.csv")))
    rc, out = corre([os.path.join(SCR, "test_n4_comprobaciones.py")])
    comprobar("reejecuta", "Pruebas de las comprobaciones N4 contra falsos positivos (también los rótulos alternativos y las condiciones generales de la auditoría interna, Z-4, y los engaños estructurales del control de vigencia, V-4): 19/19", rc == 0 and "19/19 pruebas de las comprobaciones N4 PASAN" in out)
    rec = m_con["recuento"]
    comprobar("recalcula", "Recuento real: 38 pendientes en fase1_v63.json (28 con fila y 10 auxiliares) frente a 39 en ceros_heredados_H1.csv, con la diferencia explicada (adquisiciones de AR_2023, sustituida por el comparativo)",
              rec["pendientes_en_fase1_v63"] == 38 and rec["ceros_heredados_csv_vidrala"] == 39 and rec["con_fila_en_la_historia"] == 28 and rec["auxiliares_sin_fila"] == 10 and rec["en_csv_y_no_pendientes"] == [[2023, "adquisiciones"]])
    cob = m_con["cobertura"]
    comprobar("recalcula", "Cobertura: 38 investigadas; 35 respaldadas (8 con reserva), 3 no aplicables, 0 sin evidencia suficiente, 0 discrepantes; ninguna de las 38 con decisión registrada",
              (cob["investigadas"], cob["respaldadas_clase_1_o_2"], cob["de_ellas_con_reserva"], cob["no_aplicables_clase_4"], cob["sin_evidencia_suficiente_clase_3"], cob["discrepantes_clase_5"]) == (38, 35, 8, 3, 0, 0)
              and not any(e["registro_en_fase1_decisiones"]["decision_registrada_para_esta_entrada"] for e in m_con["matriz"])
              and all(not e["condiciones_generales_no_cumplidas"] for e in m_con["matriz"]))
    l26 = next(e for e in m_con["matriz"] if e["id"] == "N4-minoritarios-2025")
    vs = l26["contrastes"]["version_espanola"]
    comprobar("recalcula", "L26: cuadre completo en el texto inglés, en la versión española (1.412.878 + 901.354 = 2.314.232) y en el ESEF (ProfitLoss = atribuido); clase 2, valor documentado 0",
              l26["clasificacion"] == 2 and vs["cuadre_balance"] and vs["cuadre_resultado"] and vs["patrimonio_atribuido"][0] + vs["total_pasivo"][0] == vs["total_pn_y_pasivo"][0] == 2314232 and l26["contrastes"]["esef_2025"]["iguales"])
    d = {x["variante"]: x["delta"] for x in e_con["variantes"]}
    V = [53.6704195834156, 70.7721966823599, 86.4887624455832]
    dps = d["L26_mas_1"]["precio de Sí (precio_de_si.p_estrella, k = 3)"]
    comprobar("recalcula", "Efecto de L26: −1/35,206 € por acción por millón en MALO, NORMAL, BUENO y ponderado, y lo mismo en el precio de Sí (k = 3)",
              all(abs(d["L26_mas_1"][k] + 1 / 35.206) < 1e-5 for k in ("MALO (Análisis!B78)", "NORMAL (Análisis!C78)", "BUENO (Análisis!D78)", "ponderado (Análisis!C83)")) and abs(dps + 1 / 35.206) < 1e-5, f"{d['L26_mas_1']['ponderado (Análisis!C83)']:+.6f}; precio de Sí {dps:+.6f}")
    c48 = d["C48_mas_1"]
    vb = {x["variante"]: x["valores"] for x in e_con["variantes"]}
    comprobar("recalcula", "Efecto de C48: ninguno en la valoración del motor B (B78:D78, C83) ni en el precio de Sí; −1 en el FCF base; el doble cómputo (C48 = 21,74) baja el FCF base a 139,46 y convierte el aviso de f en un PASA falso",
              "REVISAR" in (vb["base"]["control de rango de f (Diagnóstico V6!C50)"] or "") and "PASA" in (vb["H_C48_doble_computo"]["control de rango de f (Diagnóstico V6!C50)"] or "")
              and abs(vb["base"]["f (Diagnóstico V6!C12)"] + 0.0276078) < 1e-6 and abs(vb["H_C48_doble_computo"]["f (Diagnóstico V6!C12)"] + 0.0130527) < 1e-6 and abs(c48["precio de Sí (precio_de_si.p_estrella, k = 3)"]) < 1e-9 and
              all(abs(c48[k]) < 1e-9 for k in ("MALO (Análisis!B78)", "NORMAL (Análisis!C78)", "BUENO (Análisis!D78)", "ponderado (Análisis!C83)")) and abs(c48["FCF simplificado (Análisis!C52)"] + 1) < 1e-9
              and abs(d["H_C48_doble_computo"]["FCF simplificado (Análisis!C52)"] + 21.74) < 1e-6)
    c48e = [e for e in m_con["matriz"] if e["partida"] == "intereses_financiacion" and e["anio"] >= 2023]
    comprobar("recalcula", "C48 (2023–2025): intereses pagados en explotación y financiación cuadrada sin intereses (también en español y en el ESEF 2024–2025), con la reserva de arrendamientos declarada",
              all(e["clasificacion"] == 2 and e.get("reserva") for e in c48e) and all(e["contrastes"]["esef_2025"]["InterestPaidClassifiedAsFinancingActivities"] is None for e in c48e if e["anio"] >= 2024))
    gr = p_con["grupos"]
    comprobar("constata", "Propuestas N4 agrupadas por partida y clase (sin una solicitud por celda dependiente), con decision, fecha y confirmado_por vacíos",
              len(gr) == 6 and all(g["decision"] is None and g["fecha"] is None and g["confirmado_por"] is None for g in gr) and sum(len(g["anios"]) for g in gr) == 38)
    dq = json.load(open(os.path.join(PROP, "decisiones_y_preguntas_4_9.json"), encoding="utf-8"))
    comprobar("constata", "Decisiones y preguntas de la 4.9: campos humanos vacíos y ninguna pregunta enviada",
              all(x["decision"] is None and x["fecha"] is None and x["decidido_por"] is None for x in dq["decisiones"]) and not any(q["enviada"] for q in dq["preguntas"]))

    print("4. PRECISIÓN DEL ROIC, AUTOMATIZACIÓN Y DOCUMENTACIÓN")
    fb = json.load(open(os.path.join(ref, "fase_b.json"), encoding="utf-8"))
    r = fb["palancas"]["roic_lp"]
    comprobar("recalcula", "La justificación del ROIC terminal está en fase_b.json → palancas → roic_lp (porque y apoyo en los tres escenarios) y en fase_b.md; PRECISION_ROIC_4_9.md lo corrige sin elegir estructura",
              all(r[e].get("porque") and r[e].get("apoyo") for e in ("MALO", "NORMAL", "BUENO")) and "ROIC a largo plazo" in leer(os.path.join(ref, "fase_b.md"))
              and "no elige ninguna estructura" in leer(os.path.join(AQUI, "PRECISION_ROIC_4_9.md")))
    pa = leer(os.path.join(AQUI, "PROPUESTA_AUTOMATIZACION_4_9.md"))
    comprobar("constata", "La propuesta de automatización está separada y declara que no está activada ni cambia el contrato de confirmaciones",
              "No está activada" in pa and "contrato de confirmaciones" in pa)
    ver, cont, prom = (leer(os.path.join(RAIZ, f)) for f in ("VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md"))
    zipn = "munger_v2_r1_entrega4.9_integridad_auditoria_y_N4.zip"
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.9: versión, ZIP, batería de integridad de 103, LEEME de la 4.9 y este control",
              "entrega 4.9" in ver and zipn in cont and zipn in prom and "103/103" in cont and "103/103" in prom and "2026-11_Vidrala_ensayo_4_9/resultados/LEEME_BATERIAS_HISTORICAS.md" in cont
              and "comprobar_entrega_4_9.py" in cont and "comprobar_entrega_4_9.py" in prom)
    comprobar("constata", "CONTINUIDAD.md §2 remite a los resultados de los controles históricos del LEEME de la 4.9 (sin los esperados de versiones anteriores)",
              "45 de 49" not in cont.split("## 3.")[0] and "46 de 49" not in cont.split("## 3.")[0] and "LEEME_BATERIAS_HISTORICAS.md" in cont.split("## 3.")[0])
    for f in ("INFORME_RV1_4_9.md", "INFORME_N4_4_9.md", "REGISTRO_ENTREGA_4.9.md", "resultados/LEEME_BATERIAS_HISTORICAS.md", "AUDITORIA_INTERNA_4_9.md", "AUDITORIA_INTERNA_4_9_vigencia.md", "AUDITORIA_INTERNA_4_9_vigencia_2.md"):
        comprobar("constata", f"existe {f}", os.path.isfile(os.path.join(AQUI, f)))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
print(f"Tipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
