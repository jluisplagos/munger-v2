#!/usr/bin/env python3
"""Control de la entrega 4.10.1 (corrección de T-1 y ensayo de Vidrala con base económica 2025). Uso (desde munger_v2_r1/, después de
verificar_paquete.sh completa): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10_1/scripts/comprobar_entrega_4_10_1.py
Usa LibreOffice (batería de trazabilidad, reproducción de T-1 y comparación con C1, en temporales): no ejecutar a la vez que otra prueba.
Escribe solo en temporales (y, como cualquier ejecución de la batería, en personaje_v2/.lo_perfil/, que el manifiesto ignora).
Tipos: «reejecuta» (vuelve a ejecutar un script y compara), «recalcula» (calcula aparte), «constata» (comprueba un hecho del árbol).
También detecta si se presentaran como resultados finales salidas heredadas o una espera operativa sin resolver (§6 del encargo)."""
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
E = os.path.join(EXP, "Vidrala")
TMP = tempfile.mkdtemp(prefix="control4101_")
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
REL_EXP = os.path.relpath(EXP, RAIZ) + "/"
CAMBIADOS_FRENTE_A_4_10 = {"VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "CAMBIOS_ARCHIVOS.txt", "verificar_paquete.sh",
                           "personaje_v2/pruebas/test_trazabilidad_v2.py"}
MANIFIESTO_4_10_SHA = "1e63e7c0363a066f9c0e9d1c3963ddeb82b23f0769bbf48053e6a9d5f116bfbc"
SOLICITUD, MATERIAL = "SA-433ea31c3f7fc4bd", "e60b272b654aeece"
sys.path.insert(0, os.path.join(PV, "scripts"))


def comprobar(tipo, nombre, ok, detalle=""):
    global N_OK, N_T
    N_T += 1
    TIPOS[tipo] += 1
    N_OK += bool(ok)
    print(f"{'CUMPLE  ' if ok else 'NO CUMPLE'} · [{tipo}] {nombre}" + (f" · {detalle}" if detalle and not ok else ""), flush=True)


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def manifiesto(p):
    d = {}
    for l in open(p, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, f = l.rstrip("\n").split("  ", 1)
            d[f] = h
    return d


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def j(p):
    return json.load(open(p, encoding="utf-8"))


def py(args, timeout=3600, cwd=None):
    return subprocess.run([sys.executable, "-I", "-B"] + args, capture_output=True, text=True, timeout=timeout, cwd=cwd,
                          env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})


try:
    print("1. CONSERVACIÓN FRENTE A LA 4.10")
    mp = os.path.join(EXP, "reproduccion", "MANIFIESTO_4_10.txt")
    m410, mact = manifiesto(mp), manifiesto(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"))
    comprobar("constata", "el manifiesto de la 4.10 conservado es el del ZIP base (SHA-256 1e63e7c0…, 1.938 archivos)", sha(mp) == MANIFIESTO_4_10_SHA and len(m410) == 1938)
    cambiados = {f for f in m410 if f in mact and mact[f] != m410[f]}
    desaparecidos = {f for f in m410 if f not in mact}
    comprobar("recalcula", "frente a la 4.10 solo cambian los seis archivos declarados y ninguno desaparece", cambiados <= CAMBIADOS_FRENTE_A_4_10 and not desaparecidos,
              f"fuera de lo declarado: {sorted(cambiados - CAMBIADOS_FRENTE_A_4_10)} · desaparecidos {sorted(desaparecidos)[:5]}")
    nuevos = {f for f in mact if f not in m410}
    comprobar("recalcula", "todos los archivos nuevos están en el expediente de la 4.10.1", nuevos and all(f.startswith(REL_EXP) for f in nuevos), str(sorted(f for f in nuevos if not f.startswith(REL_EXP))[:6]))
    prot = [f for f in m410 if f not in CAMBIADOS_FRENTE_A_4_10]
    toc = [f for f in prot if not os.path.exists(os.path.join(RAIZ, f)) or sha(os.path.join(RAIZ, f)) != m410[f]]
    comprobar("recalcula", f"el resto del árbol de la 4.10 conserva sus bytes en disco ({len(prot)} archivos: código de producción, expedientes anteriores, originales, fuentes, plantilla y kit)", not toc, str(toc[:5]))
    scr = [f for f in m410 if f.startswith("personaje_v2/scripts/")]
    comprobar("recalcula", f"el código de producción (personaje_v2/scripts/, {len(scr)} archivos) no cambia: la corrección de T-1 está solo en la prueba",
              scr and all(sha(os.path.join(RAIZ, f)) == m410[f] for f in scr))

    print("2. T-1 · PREPARACIÓN DEL GRUPO L")
    jt = os.path.join(TMP, "traz.json")
    r = py([os.path.join(PV, "pruebas", "test_trazabilidad_v2.py"), "--json", jt], cwd=PV)
    ult = (r.stdout.strip().splitlines() or [""])[-1]
    res = j(jt) if os.path.exists(jt) else []
    comprobar("reejecuta", "la batería de trazabilidad pasa entera (78/78)", r.returncode == 0 and ult.startswith("78/78") and len(res) == 78 and all(x["resultado"] == "PASA" for x in res), ult)
    n410 = j(os.path.join(EXP, "reproduccion", "nombres_trazabilidad_4_10.json"))
    nombres = {(x["grupo"], x["prueba"]) for x in res}
    falta = [x for x in n410["pruebas"] if (x["grupo"], x["prueba"]) not in nombres]
    comprobar("recalcula", "se conservan los 74 casos de la 4.10 (mismos grupos y nombres, de la ejecución del archivo de la 4.10) y se añaden 4",
              len(n410["pruebas"]) == 74 and not falta and len(nombres) == 78, str(falta[:3]))
    grupo_l = [x for x in res if x["grupo"] == "L"]
    comprobar("constata", "el grupo L pasa entero (11 de 11)", len(grupo_l) == 11 and all(x["resultado"] == "PASA" for x in grupo_l))
    src = leer(os.path.join(PV, "pruebas", "test_trazabilidad_v2.py"))
    pc = src.split("def prueba_correspondencia")[1].split("\ndef ")[0] if "def prueba_correspondencia" in src else ""
    orden = [pc.find(x) for x in ("fichas_sinteticas(", "m0 = ", "registra otro libro", "no es el libro acreditado", "no se puede acreditar", "falta el libro acreditado", "rezip_inocuo(")]
    comprobar("constata", "la preparación sigue el orden del encargo: fichas con la identidad del libro antes de m0 y, después, mutaciones separadas y reconstrucción inocua",
              all(x >= 0 for x in orden) and orden[0] < orden[1] < min(orden[2:]))
    r = py([os.path.join(AQUI, "reproducir_T1.py")])   # escribe solo en un temporal propio; el informe sale por la salida estándar
    guard = leer(os.path.join(EXP, "t1", "reproducir_T1_salida.txt"))
    claves = lambda t: [l.strip() for l in t.splitlines() if l.strip().startswith(("este_entorno", "otro_entorno", "A (", "B (", "RESULTADO"))]  # noqa: E731
    k_n, k_g = claves(r.stdout), claves(guard)
    # en otro entorno la línea «este_entorno» puede cambiar (es justo T-1): se exige el diagnóstico, no los bytes de este entorno
    comprobar("reejecuta", "reproducir_T1.py, ejecutado de nuevo, da el diagnóstico guardado: con bytes distintos e inocuos la preparación antigua falla y la nueva es coherente en los dos entornos",
              r.returncode == 0 and len(k_n) == len(k_g) == 7 and k_n[-1] == k_g[-1] and k_n[3].startswith("otro_entorno_simulado") and k_n[3].endswith("False")
              and "registra otro libro evaluado" in k_n[4] and "la prueba antigua FALLA" in k_n[4]
              and k_n[2].endswith("precondición coherente") and k_n[5].endswith("precondición coherente"), (r.stdout + r.stderr)[-300:])
    vp = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    comprobar("constata", "verificar_paquete.sh completa exige la batería de trazabilidad con al menos 78 pruebas", "test_trazabilidad_v2.py" in vp and "-ge 78" in vp)

    print("3. ENTRADAS DE LA BASE 2025")
    for args, nom in (([], "libro de datos"), (["--libro"], "libro evaluado")):
        d = os.path.join(TMP, "conc" + ("_ev" if args else ""))
        os.makedirs(d)
        r = py([os.path.join(AQUI, "concordancia_2025.py")] + args + ["--salida", d])
        suf = "_evaluada" if args else ""
        nuevo = j(os.path.join(d, f"concordancia_2025{suf}.json")) if os.path.exists(os.path.join(d, f"concordancia_2025{suf}.json")) else {}
        comprobar("reejecuta", f"concordancia_2025.py ({nom}): CONCUERDA, sin residuos ni migrados que prevalezcan, e igual a la guardada",
                  r.returncode == 0 and nuevo.get("resultado") == "CONCUERDA" and not nuevo.get("residuos_de_la_base_anterior")
                  and nuevo == j(os.path.join(EXP, "resultados", f"concordancia_2025{suf}.json")), (r.stdout + r.stderr)[-200:])
    ce = j(os.path.join(EXP, "resultados", "concordancia_2025_evaluada.json"))
    ident_txt = {x["celda"] for x in ce.get("textos_heredados_identificados", [])}
    comprobar("constata", "los textos heredados con cifras de la base anterior (no son datos) están identificados uno a uno, incluidos M41 y M52 (capitalización y acciones de la etapa 1), y el informe del recorrido lo dice",
              {"Control maestro!M41", "Control maestro!M52"} <= ident_txt and len(ident_txt) == 15 and "textos heredados identificados" in leer(os.path.join(EXP, "INFORME_RECORRIDO_4_10_1.md")))
    C = j(os.path.join(EXP, "configuracion", "configuracion_ensayo_2025.json"))
    e = C["entradas"]
    comprobar("constata", "configuración principal: 90,10 €; 35.206.258 − 23.400 = 35.182.858; E = 3.169,9755058; rf 0,0285; con derecho; caja 108,352; puente 160,784; r 0,09; 0,2/0,6/0,2; k 3",
              e["precio"]["valor"] == 90.10 and e["acciones_emitidas"]["valor"] - e["autocartera"]["valor"] == e["acciones_en_circulacion"]["valor"] == 35182858
              and e["N_millones"]["valor"] == 35.182858 and e["E_capitalizacion"]["valor"] == 3169.9755058 and abs(90.10 * 35.182858 - 3169.9755058) < 1e-7
              and e["tasa_sin_riesgo"]["valor"] == 0.0285 and e["con_derecho_al_dividendo_a_cuenta"] is True and e["caja_mm"]["valor"] == 108.352
              and e["puente_referencia_mm"]["valor"] == 160.784 and e["r"] == 0.09 and e["probabilidades"] == [0.2, 0.6, 0.2] and e["k"] == 3)
    cp = C["caso_principal_analisis"]
    comprobar("constata", "caso principal: C46/C47 con la precisión de referencia (335,4/169,7) y C48 = 0 / C49 = 4,5 como supuesto heredado declarado",
              (cp["C46"]["valor"], cp["C47"]["valor"], cp["C48"]["valor"], cp["C49"]["valor"]) == (335.4, 169.7, 0, 4.5) and "SUPUESTO HEREDADO" in cp["C49"]["fuente"])
    import openpyxl
    orig, copia = os.path.join(EXP, "antecedentes", "etapa1_original", "Vidrala_evaluada.xlsx"), os.path.join(E, "etapa1", "Vidrala_evaluada.xlsx")
    ref_e1 = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala/etapa1/Vidrala_evaluada.xlsx"
    rx = C["datos_heredados_reexpresados_a_2025"]["vaciar_en_la_copia_de_etapa1"]
    vaciadas = {("Análisis", c) for c in rx["Análisis"]} | {("Control maestro", f"{col}{f}") for f in rx["Control maestro (filas de evidencia, columnas E:N)"] for col in "EFGHIJKLMN"}
    wo, wn = openpyxl.load_workbook(orig, data_only=True), openpyxl.load_workbook(copia, data_only=True)
    otras, no_vacias = [], []
    for h in wo.sheetnames:
        for fila in wo[h].iter_rows():
            for c in fila:
                v = wn[h][c.coordinate].value
                if (h, c.coordinate) in vaciadas:
                    if v not in (None, ""):
                        no_vacias.append(f"{h}!{c.coordinate}")
                elif v != c.value:
                    otras.append(f"{h}!{c.coordinate}")
    comprobar("recalcula", "preparación 2: la etapa 1 original es la de la 4.6.1 y la copia de ensayo solo vacía las celdas declaradas (7 datos y 10 filas de evidencia)",
              sha(orig) == m410[ref_e1] and not otras and not no_vacias, f"{otras[:4]} {no_vacias[:4]}")
    wb = openpyxl.load_workbook(os.path.join(E, "Vidrala_v63_evaluada.xlsx"), data_only=True)
    reex = {c: wb["Análisis"][c].value for c in ("C24", "C31", "C33", "C34", "C42", "C53", "C54")}
    comprobar("recalcula", "el libro evaluado lleva los datos reexpresados a 31-dic-2025 (0,1394; Sí; 0,36; Sí; 7,82; 108,352; 262,913), ninguno de 30-jun-2026",
              reex == {"C24": 0.1394, "C31": "Sí", "C33": 0.36, "C34": "Sí", "C42": 7.82, "C53": 108.352, "C54": 262.913}, str(reex))
    ident = ("antecedente", "anterior", "4.6.1", "noviembre de 2026", "3-nov-2026", "heredad")
    sin_ident = []
    for raiz, ds, fs in os.walk(E):
        ds[:] = [d for d in ds if d not in ("etapa1", "texto", "fase1_partes", "recalc", "prompts_generados", "__pycache__", ".lo_perfil")]
        for f in fs:
            if f.endswith((".md", ".json", ".txt", ".csv")):
                t = leer(os.path.join(raiz, f))
                for m in re.finditer(r"87,90|87\.90 ?€|3\.094,6|3094\.6", t):
                    ventana = t[max(0, m.start() - 250): m.end() + 250]
                    if not any(x in ventana for x in ident):
                        sin_ident.append(f"{os.path.relpath(os.path.join(raiz, f), E)}: …{t[max(0, m.start() - 60): m.end() + 30]}…")
    comprobar("recalcula", "ninguna mención del precio de 87,90 € o de la capitalización antigua en los productos activos sin identificarla como antecedente o comparación",
              not sin_ident, str(sin_ident[:3]))

    print("4. RECORRIDO, AUDITORÍA Y CIERRE")
    import cierre_v2 as CIE
    import pipeline
    V = pipeline.Pipeline.veredicto_auditoria
    st = j(os.path.join(E, "estado_pipeline.json"))
    comprobar("constata", "estado_pipeline.json propio: paso 14, concluido, auditoría APROBADO, sin espera operativa sin resolver, iniciado el 11-nov-2026 en este ensayo",
              st["paso"] == 14 and st["estado_analisis"] == "concluido" and st.get("auditoria") == "APROBADO" and st.get("esperando") is None
              and str(st.get("inicio", "")).startswith("2026-11-11") and not os.path.exists(os.path.join(E, "ESPERANDO.md")))
    comprobar("constata", "el pipeline consumió las cinco salidas de agente de este recorrido y sus contadores no se reiniciaron ni se agotaron (0 correcciones)",
              set(st.get("consumidos", {})) == {"extracto_v63.md", "fase_a.json", "fase_b.json", "fase_c.json", "auditoria.md"}
              and all(v == 0 for v in st["intentos"].values()))
    H = os.path.join(EXP, "antecedentes", "heredados_4_6_1")
    distintas = all(sha(os.path.join(E, f)) != sha(os.path.join(H, f)) for f in ("fase_a.json", "fase_b.json", "fase_c.json", "fase_a.md", "fase_b.md", "fase_c.md", "extracto_v63.md"))
    p1 = os.path.join(EXP, "antecedentes", "preparacion_1_datos_de_2026", "fase_a.json")
    comprobar("constata", "extracción y fases A, B y C nuevas: ninguna es la del antecedente 4.6.1 y la fase A no es la de la primera preparación",
              distintas and sha(os.path.join(E, "fase_a.json")) != sha(p1))
    fb, fbh = j(os.path.join(E, "fase_b.json")), j(os.path.join(H, "fase_b.json"))
    comprobar("constata", "la fase B es propia: margen del NORMAL 0,185 frente a 0,18 del antecedente, y cada palanca con referencia, desviación y apoyo",
              j(os.path.join(E, "celdas_B.json")).get("Palancas!C15") == 0.185 and j(os.path.join(H, "celdas_B.json")).get("Palancas!C15") == 0.18 and fb != fbh)
    aud = CIE.texto_fiel(open(os.path.join(E, "auditoria.md"), "rb").read())
    sols = st.get("solicitudes_auditoria") or []
    comprobar("recalcula", f"auditoría nueva ligada a su solicitud ({SOLICITUD}, respondida) y al material fijado ({MATERIAL}), con veredicto H2 APROBADO e identificada como interna",
              CIE.id_solicitud_en_auditoria(aud) == SOLICITUD and CIE.id_en_auditoria(aud) == MATERIAL == st.get("material_auditoria") == (CIE.material_fijado(E) or {}).get("id")
              and len(sols) == 1 and sols[0]["id"] == SOLICITUD and sols[0]["estado"] == "respondida" and V(aud) == "APROBADO" and "Auditoría interna" in aud)
    comprobar("recalcula", "el material fijado sigue siendo el actual (las huellas de material_auditoria.json coinciden con los archivos)", CIE.material(E)[0] == MATERIAL)
    previas = set(st.get("anteriores_sha256") or [])
    ant = [os.path.join(r_, f) for r_, ds, fs in os.walk(os.path.join(EXP, "antecedentes")) for f in fs if f.startswith("auditoria") and f.endswith(".md")]
    comprobar("constata", "ninguna aprobación heredada: la auditoría vigente no es ninguna de las conocidas antes de la solicitud ni de las de antecedentes",
              sha(os.path.join(E, "auditoria.md")) not in previas and all(sha(a) != sha(os.path.join(E, "auditoria.md")) for a in ant) and len(ant) >= 1)
    comprobar("recalcula", "salidas oficiales vigentes (cierre_v2.motivo_vigencia) y libro final acreditado (motivo_acreditacion_libro)",
              CIE.motivo_vigencia(E, V) is None and CIE.motivo_acreditacion_libro(E) is None)
    fi, cv, ac = j(os.path.join(E, "ficha.json")), j(os.path.join(E, "cierre_vigente.json")), j(os.path.join(E, "acreditacion_libro.json"))
    ev = sha(os.path.join(E, "Vidrala_v63_evaluada.xlsx"))
    comprobar("recalcula", "correspondencia de huellas: libro evaluado = ficha = comprobante; cierre_vigente con la ficha, el informe y la auditoría actuales",
              fi["hashes"]["libro_evaluado"] == ev == ac["archivo_final"]["sha256"] and cv["ficha_sha256"] == sha(os.path.join(E, "ficha.json"))
              and cv["informe_sha256"] == sha(os.path.join(E, "informe.md")) and cv["auditoria_sha256"] == sha(os.path.join(E, "auditoria.md")) and cv["material_auditado"] == MATERIAL)
    res = j(os.path.join(E, "resultados.json"))["valores"]
    pr = j(os.path.join(E, "precio.json"))
    wbe = wb["Análisis"]
    comprobar("recalcula", "resultados y escalera regenerados del libro actual: valores del libro = resultados.json = ficha; precio 90,10 y zona caro",
              all(abs(wbe[c].value - res[c]) < 1e-9 for c in ("B78", "C78", "D78", "C83")) and abs(pr["precio_si"] - fi["escalera"]["precio_si"]) < 1e-12
              and pr["precio"] == 90.1 and pr.get("zona") == "caro" and fi["escalera"]["V"] == [res["B78"], res["C78"], res["D78"]])
    filas = list(csv.DictReader(open(os.path.join(EXP, "resumen_v2.csv"), encoding="utf-8")))
    reg = j(os.path.join(E, "publicaciones_resumen.json"))
    pubs = [p for p in reg.get("publicaciones", []) if p.get("estado") == "publicada"]
    comprobar("constata", "resumen y registro de publicaciones aislados en el ensayo: una fila concluido · APROBADO y una publicación viva en su propio resumen_v2.csv",
              len(filas) == 1 and filas[0]["estado_analisis"] == "concluido" and filas[0]["verificacion"] == "APROBADO"
              and len(pubs) == 1 and os.path.normpath(pubs[0]["csv"]).endswith(os.path.join("2026-11_Vidrala_ensayo_4_10_1", "resumen_v2.csv")))
    fc = j(os.path.join(E, "fase_c.json"))
    comprobar("constata", "conclusión del recorrido: concluido, cubo Vigilar, acción esperar, precio objetivo 66,52 y fundamento «no procede»",
              (fc["estado_analisis"], fc["cubo_final"], fc["decision"]["accion"], fc["decision"]["precio_objetivo"], fc["fundamento_material"]["resultado"]) == ("concluido", "Vigilar", "esperar", 66.52, "no_procede"))
    ref_dec = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/Vidrala/fase1_decisiones.json"
    comprobar("constata", "P3, N4 y la provisión de personal no se declaran resueltos: fase1_decisiones.json es el de la referencia (ningún cero confirmado por la IA)",
              sha(os.path.join(E, "fase1_decisiones.json")) == m410[ref_dec] and all("declaro resuelt" in leer(os.path.join(E, f)) for f in ("fase_c.json", "fase_c.md", "informe.md")))

    print("5. COMPARACIÓN CON C1 Y PRECISIÓN DE C46/C47 (recálculo con LibreOffice en un temporal)")
    d = os.path.join(TMP, "c1")
    os.makedirs(d)
    r = py([os.path.join(AQUI, "comparar_con_C1.py"), "--salida", d], timeout=2400)
    vals = lambda x: {f["variante"]: {k: v for k, v in f["valores"].items() if isinstance(v, (int, float))} for f in x["variantes"]}  # noqa: E731
    nuevo = j(os.path.join(d, "comparacion_C1.json")) if os.path.exists(os.path.join(d, "comparacion_C1.json")) else {"variantes": [], "controles": {}, "atribucion": {}}
    g = j(os.path.join(EXP, "resultados", "comparacion_C1.json"))
    comprobar("reejecuta", "comparar_con_C1.py vuelve a dar los mismos valores de las cuatro variantes y sus dos controles (C1 reproducido; el ensayo reproduce resultados.json)",
              r.returncode == 0 and vals(nuevo) == vals(g) and len(g["variantes"]) == 4 and all(v is True for v in nuevo["controles"].values()), (r.stdout + r.stderr)[-300:])
    at = g["atribucion"]
    comprobar("recalcula", "atribución: entrada y convención 0 €; juicio = total (+1,198 € de ponderado, +0,856 € de precio de Sí, solo en el NORMAL); precisión de C46/C47 0 €",
              all(abs(v) < 1e-9 for v in at["entrada_y_convencion (C1 → ensayo con palancas de C1)"].values())
              and at["juicio (palancas nuevas: ensayo con palancas de C1 → ensayo)"] == at["total (C1 → ensayo)"]
              and abs(at["total (C1 → ensayo)"]["ponderado"] - 1.198487) < 1e-6 and abs(at["total (C1 → ensayo)"]["precio_de_si"] - 0.856062) < 1e-6
              and abs(at["total (C1 → ensayo)"]["MALO"]) < 1e-9 and abs(at["total (C1 → ensayo)"]["BUENO"]) < 1e-9
              and all(abs(v) < 1e-9 for v in at["precision_C46_C47 (ensayo → ensayo con 335,413 / 169,668)"].values()))

    print("6. DOCUMENTACIÓN Y PROPUESTAS")
    pq = j(os.path.join(EXP, "propuestas", "propuestas_4_10_1.json"))
    comprobar("constata", "propuestas humanas agrupadas y sin firmar (8 nuevas, campos humanos vacíos; las 10 de la 4.10 siguen pendientes)",
              len(pq["nuevas"]) == 8 and all(x["decision"] is None and x["fecha"] is None and x["decidido_por"] is None for x in pq["nuevas"]) and len(pq["pendientes_de_la_4_10"]) == 10)
    ver, cont, prom = (leer(os.path.join(RAIZ, f)) for f in ("VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md"))
    zipn = "munger_v2_r1_entrega4.10.1_piloto_2025_y_trazabilidad.zip"
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.10.1 (versión, ZIP, batería de 78, LEEME y este control)",
              "entrega 4.10.1" in ver and zipn in cont and zipn in prom and "78/78" in cont and "78/78" in prom and "comprobar_entrega_4_10_1.py" in prom
              and "2026-11_Vidrala_ensayo_4_10_1/resultados/LEEME_BATERIAS_HISTORICAS.md" in cont)
    for f in ("INFORME_RECORRIDO_4_10_1.md", "t1/INFORME_T1_4_10_1.md", "propuestas/PROPUESTAS_HUMANAS_4_10_1.md", "REGISTRO_PRUEBAS_4_10_1.md",
              "revision_interna/REVISION_INTERNA_4_10_1.md", "REGISTRO_ENTREGA_4.10.1.md", "resultados/LEEME_BATERIAS_HISTORICAS.md"):
        comprobar("constata", f"existe {f}", os.path.isfile(os.path.join(EXP, f)))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
print(f"Tipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
