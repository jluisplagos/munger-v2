#!/usr/bin/env python3
"""Control de la entrega 4.10. Uso (desde munger_v2_r1/, después de verificar_paquete.sh completa y de los controles históricos):
    python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/scripts/comprobar_entrega_4_10.py
Usa LibreOffice (vuelve a calcular las variantes en un temporal): no ejecutar a la vez que otra prueba. Escribe solo en temporales.
Tipos: «reejecuta» (vuelve a ejecutar un script y compara), «recalcula» (calcula aparte), «constata» (comprueba un hecho del árbol)."""
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
TMP = tempfile.mkdtemp(prefix="control410_")
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
CAMBIADOS_FRENTE_A_4_9 = {"VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "verificar_paquete.sh", "CAMBIOS_ARCHIVOS.txt",
                          "personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/pipeline.py", "personaje_v2/scripts/ficha.py",
                          "personaje_v2/scripts/informe.py", "personaje_v2/scripts/resumen.py", "personaje_v2/scripts/verificar_todo.sh",
                          "personaje_v2/DECISIONES.md"}
NUEVOS_FUERA_DEL_EXPEDIENTE = {"personaje_v2/scripts/acreditar_libro.py", "personaje_v2/pruebas/test_trazabilidad_v2.py"}


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


try:
    print("1. CONSERVACIÓN FRENTE A LA 4.9")
    m49 = manifiesto(os.path.join(EXP, "reproduccion", "MANIFIESTO_4_9.txt"))
    m410 = manifiesto(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"))
    comprobar("constata", "el manifiesto de la 4.9 conservado es el del ZIP base (1.733 archivos)", len(m49) == 1733)
    cambiados = {f for f in m49 if f in m410 and m410[f] != m49[f]}
    desaparecidos = {f for f in m49 if f not in m410}
    comprobar("recalcula", "frente al manifiesto de la 4.9 solo cambian los archivos declarados y ninguno desaparece",
              cambiados <= CAMBIADOS_FRENTE_A_4_9 and not desaparecidos, f"fuera de lo declarado: {sorted(cambiados - CAMBIADOS_FRENTE_A_4_9)} · desaparecidos {sorted(desaparecidos)[:5]}")
    nuevos = {f for f in m410 if f not in m49}
    fuera = {f for f in nuevos if not f.startswith("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_10/")} - NUEVOS_FUERA_DEL_EXPEDIENTE
    comprobar("recalcula", "los archivos nuevos están en el expediente de la 4.10, salvo acreditar_libro.py y la batería nueva", not fuera, str(sorted(fuera)[:6]))
    prot = [f for f in m49 if f.startswith(("personaje_v2/empresas_v2/", "personaje_v2/empresas_v2_correcciones/", "contrastes/", "v6/", "kit_pipeline_munger/"))]
    toc = [f for f in prot if sha(os.path.join(RAIZ, f)) != m49[f]] if all(os.path.exists(os.path.join(RAIZ, f)) for f in prot) else ["(falta alguno)"]
    comprobar("recalcula", f"originales, expedientes anteriores (incluida la 4.9), fuentes, plantilla y kit conservan sus bytes ({len(prot)} archivos, SHA-256 en disco)", not toc, str(toc[:5]))
    ref_dec = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "fase1_decisiones.json")
    comprobar("recalcula", "fase1_decisiones.json de la referencia conserva su huella (ninguna confirmación de la IA)", sha(ref_dec) == m49[os.path.relpath(ref_dec, RAIZ)])

    print("2. CORRECCIONES TÉCNICAS")
    sys.path.insert(0, os.path.join(PV, "scripts"))
    import cierre_v2 as CIE
    comprobar("constata", "H2 (Pipeline.veredicto_auditoria) no cambia: el texto de la función es el de la 4.9",
              leer(os.path.join(PV, "scripts", "pipeline.py")).split("def veredicto_auditoria")[1].split("\n    def ")[0]
              == leer(os.path.join(EXP, "tecnico", "reproduccion", "codigo_4_9", "pipeline.py")).split("def veredicto_auditoria")[1].split("\n    def ")[0])
    t = CIE.texto_fiel(b"\xef\xbb\xbf1. PASA \xc2\xb7 x\r\nVeredicto: APROBADO\r\n")
    comprobar("recalcula", "la lectura común quita el BOM y los CRLF antes de H2 y conserva el texto (texto_fiel)", t == "1. PASA · x\nVeredicto: APROBADO")
    comprobar("constata", "la lectura común se usa en motivo_rechazo_cierre y en el paso 13",
              "txt = texto_fiel(datos)" in leer(os.path.join(PV, "scripts", "cierre_v2.py")) and "CIE.texto_fiel(open(destino" in leer(os.path.join(PV, "scripts", "pipeline.py")))
    comprobar("constata", "ficha.py, informe.py, resumen.py y el pipeline exigen vigencia con un cierre registrado aunque la ficha pierda sus marcadores",
              all("cierre_vigente.json" in leer(os.path.join(PV, "scripts", s)) and "4.10" in leer(os.path.join(PV, "scripts", s)) for s in ("ficha.py", "informe.py", "resumen.py", "pipeline.py")))
    comprobar("constata", "verificar_todo.sh acredita el archivo final después de las cachés (acreditar_libro.py, al final)",
              leer(os.path.join(PV, "scripts", "verificar_todo.sh")).index("acreditar_libro.py") > leer(os.path.join(PV, "scripts", "verificar_todo.sh")).index('mv "$C/con_cache.tmp.xlsx"'))
    rep = j(os.path.join(EXP, "tecnico", "reproduccion", "trazabilidad_con_codigo_4_9.json"))
    comprobar("constata", "la reproducción con el código de la 4.9 conserva sus fallos: 26 de 69 pasan (BOM, ambos marcadores, {}, restauración, fila sin empresa, libro)",
              sum(1 for r in rep if r["resultado"] == "PASA") == 26 and len(rep) == 69)
    # la mutación M22 de la 4.9 ya no se aplica (buscaba la línea «txt = datos.decode("utf-8")», que sustituye la corrección 3.2); su
    # equivalente sobre el código de la 4.10 (volver a decodificar sin la lectura común) tiene que hacer fallar la batería de integridad
    mut = os.path.join(TMP, "mut22")
    os.makedirs(mut)
    src = leer(os.path.join(PV, "scripts", "cierre_v2.py"))
    ancla = "    txt = texto_fiel(datos)\n    if txt is None:\n        # (4.9, Z-2) antes, una excepción"  # la de motivo_rechazo_cierre (única)
    open(os.path.join(mut, "cierre_v2.py"), "w", encoding="utf-8").write(src.replace(ancla, '    txt = datos.decode("utf-8")\n    if txt is None:\n        # (4.9, Z-2) antes, una excepción', 1))
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "pruebas", "test_integridad_auditoria_v2.py"), "--codigo", mut], capture_output=True, text=True, cwd=PV,
                       env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}, timeout=1800)
    ult = (r.stdout.strip().splitlines() or [""])[-1]
    comprobar("reejecuta", "el equivalente de la mutación M22 de la 4.9 sobre el código de la 4.10 (decodificar sin la lectura común) hace fallar la batería de integridad",
              src.count(ancla) == 1 and r.returncode != 0 and "PASAN" in ult and not ult.startswith("103/103"), ult)
    vp = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    comprobar("constata", "verificar_paquete.sh completa exige la batería de trazabilidad (al menos 74 pruebas)", "test_trazabilidad_v2.py" in vp and '-ge 74' in vp)
    comprobar("constata", "existe el productor del ZIP portable y el arranque documenta la incidencia del nombre",
              os.path.exists(os.path.join(AQUI, "empaquetar_zip.py")) and "enga├▒os.txt" in leer(os.path.join(EXP, "arranque", "ARRANQUE_4_10.md")))
    noascii = [f for f in m410 if not f.isascii()]
    comprobar("constata", "el nombre de la 4.9 con «ñ» sigue en el manifiesto tal cual (no se renombró)", any(f.endswith("n4_paginas_reales_engaños.txt") for f in noascii))

    print("3. N4 REVISADA")
    out = os.path.join(TMP, "n4")
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(AQUI, "n4_revision.py"), "--salida", out], capture_output=True, text=True)
    m = j(os.path.join(EXP, "n4", "matriz_n4_4_10.json"))
    comprobar("reejecuta", "n4_revision.py, ejecutado de nuevo en un temporal, da la misma matriz revisada que la entregada",
              r.returncode == 0 and os.path.exists(os.path.join(out, "matriz_n4_4_10.json")) and j(os.path.join(out, "matriz_n4_4_10.json")) == m)
    rec = {k: v["n"] for k, v in m["recuento"].items()}
    comprobar("constata", "la matriz revisada da 18 completas, 8 parciales, 9 dependientes de la definición y 3 no aplicables (38)",
              r.returncode == 0 and rec == {"completa": 18, "parcial": 8, "depende_de_la_definicion": 9, "no_aplicable": 3} and m["total"] == 38, f"{rec} · {r.stderr[-200:]}")
    der = {x["anio"]: x.get("derivados_corrientes_mm") for x in m["matriz"] if x["partida"] == "otros_activos_financieros"}
    comprobar("constata", "derivados corrientes de 2024 y 2025 (25,567 y 1,157; balance español de 2025, pág. 9) y 2023 sin derivados",
              der.get(2024) == 25.567 and der.get(2025) == 1.157 and der.get(2023) == 0.0)
    comprobar("constata", "ningún campo humano relleno en la matriz revisada", all(all(v is None for k, v in x["registro"].items() if k != "nota") for x in m["matriz"]))
    comprobar("constata", "la matriz de la 4.9 no se reescribió", sha(os.path.join(EXP, "..", "2026-11_Vidrala_ensayo_4_9", "n4", "matriz_n4.json")) == m49["personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/n4/matriz_n4.json"])

    print("4. VARIANTES (recálculo con LibreOffice en un temporal)")
    dv = os.path.join(TMP, "variantes")
    r = subprocess.run([sys.executable, "-I", "-B", os.path.join(AQUI, "variantes_4_10.py"), "--salida", dv, "--copia-combinada", os.path.join(TMP, "copia_combinada")],
                       capture_output=True, text=True, timeout=2400)
    nuevo = j(os.path.join(dv, "variantes_4_10.json")) if os.path.exists(os.path.join(dv, "variantes_4_10.json")) else {"variantes": [], "identidades": {}}
    guard = j(os.path.join(EXP, "variantes", "variantes_4_10.json"))
    vals = lambda d: {f["variante"]: {k: v for k, v in f["valores"].items() if isinstance(v, (int, float))} for f in d["variantes"]}  # noqa: E731
    comprobar("reejecuta", "variantes_4_10.py vuelve a dar exactamente los mismos valores de las 12 variantes y cumple sus 14 identidades",
              r.returncode == 0 and vals(nuevo) == vals(guard) and len(guard["variantes"]) == 12 and len(nuevo["identidades"]) == 14 and all(nuevo["identidades"].values()),
              f"código {r.returncode} · {r.stdout[-300:]}")
    V = vals(guard)
    b = V["base"]
    comprobar("recalcula", "la base reproduce la referencia mecánica (53,670420 · 70,772197 · 86,488762 · 70,495154 · 65,688087)",
              all(abs(b[k] - x) < 5e-7 for k, x in (("MALO", 53.670420), ("NORMAL", 70.772197), ("BUENO", 86.488762), ("ponderado", 70.495154), ("precio_de_si", 65.688087))))
    comprobar("recalcula", "N8: V_sin = V_con − 43,338/35,206 en los tres escenarios, el ponderado y el precio de Sí (cálculo de este control)",
              all(abs(V["N8_sin_derecho"][k] - (b[k] - 43.338 / 35.206)) < 1e-9 for k in ("MALO", "NORMAL", "BUENO", "ponderado", "precio_de_si")))
    comprobar("recalcula", "N7 puro: V' = V·35,206/35,182858 (cálculo de este control)", all(abs(V["N7_N_puro"][k] - b[k] * 35.206 / 35.182858) < 1e-9 for k in ("MALO", "NORMAL", "BUENO", "ponderado")))
    ro = lambda x: (0.09 * x["E_capitalizacion"] + x["i_C63"] * (1 - x["tau_C11"]) * x["D_C64"]) / (x["E_capitalizacion"] + x["D_C64"])  # noqa: E731
    comprobar("recalcula", "N6: r_op de C1 = (r·E + i·(1−τ)·D)/(E+D) con E = 90,10 × 35,182858 (cálculo de este control)",
              abs(ro(V["C1_31dic2025_con_derecho"]) - V["C1_31dic2025_con_derecho"]["r_op"]) < 1e-12 and abs(V["C1_31dic2025_con_derecho"]["E_capitalizacion"] - 90.10 * 35.182858) < 1e-6)
    comprobar("recalcula", "P3: las dos representaciones de la situación B dan lo mismo y no cambian la valoración del motor B",
              all(abs(V["P3_B1"][k] - V["P3_B2"][k]) < 1e-9 for k in ("FCF_base", "f", "ponderado")) and abs(V["P3_B1"]["ponderado"] - b["ponderado"]) < 1e-9 and abs(V["P3_B1"]["FCF_base"] - (b["FCF_base"] - 2.254)) < 1e-3)
    comprobar("constata", "ninguna variante cambia r (0,09), salvo la de historia adversa ninguna toca palancas, y todas declaran sus celdas",
              all(f["valores"]["r_C56"] == 0.09 for f in guard["variantes"]) and all(not any(k.startswith("Palancas") for k in f["celdas"]) for f in guard["variantes"] if f["variante"] != "N10_MALO_historia_adversa"))
    cc = os.path.join(EXP, "copia_combinada")
    ac = j(os.path.join(cc, "acreditacion_libro.json"))
    comprobar("recalcula", "la copia combinada es, byte a byte, la acreditada en su comprobante, y su verificación final es ÍNTEGRO",
              sha(os.path.join(cc, "Vidrala_v63_evaluada.xlsx")) == ac["archivo_final"]["sha256"] and str(ac["archivo_final"]["veredicto"]).startswith("ÍNTEGRO"))
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(cc, "Vidrala_v63_evaluada.xlsx"), data_only=True, read_only=True)
    c1 = V["C1_31dic2025_con_derecho"]
    comprobar("recalcula", "los valores guardados en la copia combinada son los de C1", all(abs(wb["Análisis"][c].value - c1[k]) < 1e-9 for c, k in (("B78", "MALO"), ("C78", "NORMAL"), ("D78", "BUENO"), ("C83", "ponderado"))))
    sens = guard["sensibilidad_de_pesos_N10"]["base"]
    comprobar("recalcula", "N10: ponderados de la sensibilidad de pesos = suma de pesos × valores (cálculo de este control)",
              abs(sens["cola adversa 0,3/0,5/0,2"]["ponderado"] - round(0.3 * b["MALO"] + 0.5 * b["NORMAL"] + 0.2 * b["BUENO"], 6)) < 1e-6)

    print("5. EXPEDIENTE EXPLORATORIO, DECISIONES Y DOCUMENTACIÓN")
    ex = os.path.join(EXP, "expediente_exploratorio", "Vidrala")
    st = j(os.path.join(ex, "estado_pipeline.json"))
    comprobar("constata", "el expediente exploratorio está en su estado legítimo: paso 5, esperando al agente de extracción, sin auditoría ni ficha oficial",
              st.get("paso") == 5 and st.get("esperando") == "5:extracto_v63.md" and st.get("auditoria") is None and not os.path.exists(os.path.join(ex, "ficha.json")))
    hist = sorted(os.listdir(os.path.join(ex, "historial_cierres")))
    ret = j(os.path.join(ex, "historial_cierres", hist[-1], "RETIRADA.json"))
    comprobar("constata", "la copia no heredó la aprobación: el pipeline archivó el cierre de la 4.6.1 al cambiar el material", "material cambió" in ret.get("motivo", ""))
    f1 = j(os.path.join(ex, "fase1_v63.json"))
    comprobar("constata", "las entradas de C1 en la copia (N = 35,182858; E = 3.169,975506 con fecha 31-dic-2025) y el alcance exploratorio declarado",
              f1["acciones_diluidas"]["valor"] == 35.182858 and f1["capitalizacion"]["valor"] == 3169.975506 and "COPIA EXPLORATORIA" in j(os.path.join(ex, "alcance_v2.json"))["aviso"])
    dq = j(os.path.join(EXP, "propuestas", "decisiones_4_10.json"))
    comprobar("constata", "propuesta única: diez decisiones con los campos humanos vacíos", len(dq["decisiones"]) == 10 and all(d["decision"] is None and d["fecha"] is None and d["decidido_por"] is None for d in dq["decisiones"]))
    ver, cont, prom = (leer(os.path.join(RAIZ, f)) for f in ("VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md"))
    zipn = "munger_v2_r1_entrega4.10_consolidacion_financiera_y_trazabilidad.zip"
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.10 (versión, ZIP, batería de 74, LEEME de la 4.10 y este control)",
              "entrega 4.10" in ver and zipn in cont and zipn in prom and "74/74" in cont and "74/74" in prom and "2026-11_Vidrala_ensayo_4_10/resultados/LEEME_BATERIAS_HISTORICAS.md" in cont
              and "comprobar_entrega_4_10.py" in prom)
    comprobar("constata", "el mensaje de arranque recupera la estructura de uso: pasos, línea separadora y título del mensaje",
              "\n---\n" in prom and "# Continuación del proyecto Munger v2 · verificación inicial" in prom and ".PARTES.txt" in prom)
    for f in ("INFORME_FINANCIERO_4_10.md", "INFORME_CORRECCIONES_TECNICAS_4_10.md", "ACLARACION_PN1_4_10.md", "ESPECIFICACION_INTEGRACION_4_10.md",
              "propuestas/PROPUESTA_DECISIONES_4_10.md", "REGISTRO_ENTREGA_4.10.md", "resultados/LEEME_BATERIAS_HISTORICAS.md", "arranque/ARRANQUE_4_10.md"):
        comprobar("constata", f"existe {f}", os.path.isfile(os.path.join(EXP, f)))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
print(f"Tipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
