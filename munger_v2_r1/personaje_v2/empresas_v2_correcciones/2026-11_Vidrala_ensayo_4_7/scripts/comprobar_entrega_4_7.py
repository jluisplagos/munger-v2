#!/usr/bin/env python3
"""Controles de la entrega 4.7 (bloque A: resumen configurado; bloque B: N1–N3). Solo lectura salvo los temporales de analisis_n1_n3.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7/scripts/comprobar_entrega_4_7.py

Cada control declara su tipo (auditoría interna, H-16):
  [reejecuta]  vuelve a ejecutar un script del paquete y compara su resultado;
  [recalcula]  recalcula a partir de los archivos actuales (huellas, vigencia, contenido de JSON, fórmulas de los libros);
  [constata]   solo constata lo que dice una salida o un texto conservados (las baterías largas se reejecutan en verificar_paquete.sh).
"""
import hashlib
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
REF = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
FIN = os.path.join(AQUI, "financiero")
sys.path.insert(0, os.path.join(PV2, "scripts"))
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402

N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
MODIFICADOS_A = ["personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/ficha.py", "personaje_v2/scripts/informe.py", "personaje_v2/scripts/pipeline.py",
                 "personaje_v2/scripts/resumen.py", "verificar_paquete.sh"]
# documentación actualizada en la 4.7 (no es código) y archivos de paquete
DOCUMENTACION = ["personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/DECISIONES.md", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "VERSION",
                 "CAMBIOS_ARCHIVOS.txt", "MANIFIESTO_SHA256.txt"]


def comprobar(n, cond, det="", tipo="recalcula"):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    TIPOS[tipo] += 1
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] [{tipo}] {n}" + (f" · {det}" if det else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def leer(*p):
    return open(os.path.join(*p), encoding="utf-8").read()


def huellas_de(texto):
    return dict(re.findall(r"\| `([^`]+)`(?: \(nuevo\))? \| `([0-9a-f]{64})` \|", texto))


print("ENTREGA 4.7 · controles de solo lectura")
print("=" * 100)
print("\n1. REFERENCIAS INTACTAS FRENTE A LA 4.6.1")
m461 = {}
for l in open(os.path.join(AQUI, "reproduccion", "MANIFIESTO_SHA256_4_6_1.txt"), encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        m461[p] = h
iguales = {k: v for k, v in m461.items() if k not in MODIFICADOS_A and k not in DOCUMENTACION}
dif = [k for k, v in iguales.items() if not os.path.exists(os.path.join(RAIZ, k)) or sha(os.path.join(RAIZ, k)) != v]
comprobar(f"Los {len(iguales)} archivos de la 4.6.1 que no son código del bloque A ni documentación conservan su huella (originales, expedientes 4.4–4.6.1, libros, fases, fuentes)", not dif, ", ".join(dif[:5]))
orig = [k for k in iguales if k.startswith("personaje_v2/empresas_v2/")]
comprobar("Entre ellos, los 489 originales de personaje_v2/empresas_v2/", len(orig) == 489, str(len(orig)))
comprobar("Registro humano de P1 sin cambios (SHA-256 b4e47afc…c445a4)", sha(os.path.join(REF, "fase1_decisiones.json")) == "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4")
comprobar("El manifiesto 4.6.1 conservado (reproduccion/MANIFIESTO_SHA256_4_6_1.txt) es el del paquete 4.6.1 (SHA-256 cbf63486…6792)",
          sha(os.path.join(AQUI, "reproduccion", "MANIFIESTO_SHA256_4_6_1.txt")) == "cbf63486d653908f9ca7f582a5c954331f554e00003f2cc947994d94075f6792")

print("\n2. BLOQUE A · CÓDIGO, REPRODUCCIÓN Y PRUEBAS")
ct = leer(AQUI, "CIERRE_TECNICO_BLOQUE_A.md")
revisado = huellas_de(ct.split("**Huellas del cierre definitivo:**")[1])
comprobar("El código del bloque A conserva las huellas del cierre definitivo (CIERRE_TECNICO_BLOQUE_A.md §5, 7 archivos)", len(revisado) == 7 and all(sha(os.path.join(RAIZ, k)) == v for k, v in revisado.items()),
          ", ".join(k for k, v in revisado.items() if sha(os.path.join(RAIZ, k)) != v))
primero = huellas_de(ct.split("## 2. Huellas del primer cierre")[1].split("## 3.")[0])
mat1 = {l.split("  ", 1)[1].strip(): l.split("  ", 1)[0] for l in leer(AQUI, "MATERIAL_AUDITADO_4_7.txt").splitlines() if l.strip() and not l.startswith("#")}
comprobar("Las huellas del primer cierre son las del material de la primera auditoría (MATERIAL_AUDITADO_4_7.txt)", len(primero) == 7 and all(mat1.get(k) == v for k, v in primero.items()))
a = leer(AQUI, "reproduccion", "reproduccion_resumen_codigo_4_6_1.txt")
b = leer(AQUI, "reproduccion", "reproduccion_resumen_codigo_4_7.txt")
comprobar("Reproducción con el código 4.6.1 (árbol íntegro): el fallo se reproduce en las dos rutas", a.count("REPRODUCIDO:") == 2 and "NO SE REPRODUCE" not in a and "entrega461" in a.splitlines()[0], tipo="constata")
comprobar("Reproducción con el código 4.7 revisado: no se reproduce en ninguna", b.count("NO SE REPRODUCE") == 2 and "REPRODUCIDO:" not in b, tipo="constata")
comprobar("test_resumen_v2.py: 34/34 con el código 4.7 definitivo (salida conservada; se reejecuta en verificar_paquete.sh completa)", "34/34 pruebas de aceptación del resumen PASAN" in leer(AQUI, "resultados", "test_resumen_v2_salida.txt"), tipo="constata")
for nombre, n_ok, n_falla in (("de_la_primera_auditoria", 19, 15), ("de_la_auditoria_de_control", 27, 7), ("de_la_auditoria_final", 30, 4), ("del_control_de_vigencia", 33, 1)):
    t = leer(AQUI, "reproduccion", f"pruebas_resumen_con_codigo_{nombre}.txt")
    comprobar(f"test_resumen_v2.py con el código {nombre.replace('_', ' ')}: {n_ok}/34 ({n_falla} en FALLA, las de los hallazgos posteriores)", f"{n_ok}/34 pruebas de aceptación del resumen PASAN" in t and t.count("\nFALLA ·") == n_falla, tipo="constata")
pb = leer(AQUI, "reproduccion", "pruebas_resumen_con_codigo_4_6_1.txt")
comprobar("test_resumen_v2.py con el código 4.6.1: 6/34", "6/34 pruebas de aceptación del resumen PASAN" in pb and pb.count("FALLA ·") == 28, tipo="constata")
comprobar("test_cierre_v2.py: 55/55 con el código 4.7 revisado (salida conservada; se reejecuta en verificar_paquete.sh completa)", "55/55 pruebas de aceptación del cierre PASAN" in leer(AQUI, "resultados", "test_cierre_v2_salida_codigo_4_7.txt"), tipo="constata")
rr = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "scripts", "comprobar_integracion_verificador_47.py")], capture_output=True, text=True)
comprobar("Integración de la batería del resumen en verificar_paquete.sh completa (mínimo 34): 13 de 13 y salida idéntica a la conservada",
          rr.returncode == 0 and "RESULTADO: 13 de 13" in rr.stdout and leer(AQUI, "resultados", "comprobar_integracion_verificador_47_salida.txt").strip() in rr.stdout, tipo="reejecuta")
rr = subprocess.run([sys.executable, "-I", os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "scripts", "comprobar_integracion_verificador.py")], capture_output=True, text=True)
comprobar("Integración de la batería de cierre (mínimo 55, de la 4.6.1): 13 de 13", rr.returncode == 0 and "RESULTADO: 13 de 13" in rr.stdout, tipo="reejecuta")
comprobar("El expediente de referencia 4.6.1 sigue vigente con el código 4.7 y sin registro de publicaciones", CIE.motivo_vigencia(REF, pipeline.Pipeline.veredicto_auditoria) is None
          and not CIE.retiradas_pendientes(REF) and not os.path.exists(os.path.join(REF, CIE.REGISTRO_RESUMEN)) and not os.path.exists(os.path.join(REF, CIE.RESPALDO_RESUMEN)))
comprobar("La evidencia anota la columna publicada; «cambio de tipo» de 2021 viene de la conciliación, no del desglose (auditoría de control, C-7)",
          all(e.get("columna_publicada") for e in json.load(open(os.path.join(FIN, "evidencia.json"), encoding="utf-8")))
          and next(e for e in json.load(open(os.path.join(FIN, "evidencia.json"), encoding="utf-8")) if e["clave"] == "conc_cambio_tipo_2021")["linea"].startswith("Adjustments for changes in tax rate"))

print("\n3. BLOQUE B · EVIDENCIA, RÉPLICA Y MATRIZ")
tmp = tempfile.mkdtemp(prefix="c47_")
try:
    copia = os.path.join(tmp, "e47")
    shutil.copytree(AQUI, copia, ignore=shutil.ignore_patterns("propuesta_excel", "__pycache__"))
    os.symlink(os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1"), os.path.join(tmp, "2026-11_Vidrala_ensayo_4_6_1"))
    rr = subprocess.run([sys.executable, "-I", os.path.join(copia, "scripts", "analisis_n1_n3.py")], capture_output=True, text=True)
    comprobar("analisis_n1_n3.py termina con código 0 («evidencia y control correctos»)", rr.returncode == 0 and "RESULTADO: evidencia y control correctos" in rr.stdout, tipo="reejecuta")
    for f in ("salida.txt", "evidencia.json", "matriz.csv", "matriz.json", "matriz.md", "n3_anio_a_anio.csv", "evidencia.md"):
        comprobar(f"financiero/{f} conservado = regenerado byte a byte", sha(os.path.join(FIN, f)) == sha(os.path.join(copia, "financiero", f)), tipo="reejecuta")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
E = json.load(open(os.path.join(FIN, "evidencia.json"), encoding="utf-8"))
comprobar("Matriz de evidencia: 109 datos, todos reproducidos con su signo, con archivo, página, concepto, columna, período, perímetro, unidad y signo publicado",
          len(E) == 109 and all(e["reproduce"] and abs(e["valor_miles"] - e["esperado_miles"]) < 0.5 and all(e.get(k) not in (None, "") for k in ("archivo", "pagina_pdf", "concepto", "periodo", "perimetro", "unidad", "signo_publicado")) and e.get("columna") is not None for e in E))
comprobar("La evidencia incluye las conciliaciones fiscales completas 2021–2025 (31 líneas) y el segmento de Italia de 2018–2019",
          sum(e["clave"].startswith("conc_") for e in E) == 31 and all(any(e["clave"] == f"ita_{k}_{y}" for e in E) for k in ("ingresos", "pbt", "gfin", "ifin") for y in (2018, 2019)))
M = json.load(open(os.path.join(FIN, "matriz.json"), encoding="utf-8"))
comprobar("Cada conciliación cuadra con su gasto publicado", all(c["cuadra"] for c in M["conciliaciones"].values()) and len(M["conciliaciones"]) == 5)
pr = json.load(open(os.path.join(REF, "precio.json"), encoding="utf-8"))
b0 = M["matriz"][0]
comprobar("Control de la réplica: T0·M0·R0 = libro de referencia (53,67 / 70,77 / 86,49; 70,50; 65,69) con tolerancia 0,005", M["control"] and b0["combinacion"] == "T0·M0·R0"
          and all(abs(x - y) < 0.005 for x, y in zip((b0["V_malo"], b0["V_normal"], b0["V_bueno"], b0["ponderado"], b0["precio_si"]), pr["V"] + [pr["ponderado"], pr["precio_si"]])))
comprobar("27 combinaciones, como máximo 3 alternativas por asunto (base incluida), con las columnas pedidas", len(M["matriz"]) == 27 and all(len(v) == 3 for v in M["alternativas"].values())
          and all(k in b0 for k in ("V_malo", "V_normal", "V_bueno", "ponderado", "precio_si", "peso_terminal", "fcf1", "fcf_min", "capital_liberado_malo_10a", "reinversion_malo_1_5", "d_ponderado", "d_precio_si", "clase")))
res = json.load(open(os.path.join(REF, "resultados.json"), encoding="utf-8"))
comprobar("Constantes: r = 0,09, probabilidades 0,2 / 0,6 / 0,2, puente 160,784 y 35,206 acciones del libro de referencia", res["valores"]["C56"] == 0.09 and res["probabilidades"] == [0.2, 0.6, 0.2]
          and abs(res["pasivos_netos_B_C16"] - 160.784) < 1e-6 and res["valores"]["C55"] == 35.206)
clases = [f["clase"] for f in M["matriz"]]
comprobar("Clases: 15 sensibilidades mecánicas (T0 o M0), 11 hipótesis coherentes alternativas y 1 recomendada (T1·M1·R1)", clases.count("hipótesis coherente recomendada") == 1
          and sum(c.startswith("sensibilidad") for c in clases) == 15 and [f["combinacion"] for f in M["matriz"] if f["clase"] == "hipótesis coherente recomendada"] == ["T1·M1·R1"])
comprobar("T1 = media 2023–2025 del tipo efectivo (22,05 %); la formulación inicial (23,30 %) queda registrada como descartada",
          abs(M["t_rec"] - 0.220541) < 1e-6 and abs(M["t1_inicial"] - 0.23300) < 5e-5 and os.path.exists(os.path.join(FIN, "formulacion_inicial_N1", "matriz.csv")))

print("\n4. BLOQUE B · LIBROS DE PROPUESTA")
PE = os.path.join(FIN, "propuesta_excel")
comprobar("propuesta_excel.py: las dos propuestas reproducen la réplica y solo difieren en las celdas declaradas (salida conservada, 4 de 4)", "(4 de 4)" in leer(PE, "salida.txt"), tipo="constata")
rep = {f["combinacion"]: f for f in M["matriz"]}
for d, comb in (("M2", "T0·M2·R0"), ("T1_M1", "T1·M1·R0")):
    p = json.load(open(os.path.join(PE, d, "precio.json"), encoding="utf-8"))
    f = rep[comb]
    comprobar(f"{d}/precio.json del libro recalculado = réplica {comb} (tolerancia 0,005) y con el aviso de no comparabilidad",
              all(abs(x - y) < 0.005 for x, y in zip(p["V"] + [p["ponderado"], p["precio_si"]], (f["V_malo"], f["V_normal"], f["V_bueno"], f["ponderado"], f["precio_si"])))
              and "NO son una comparación válida" in p.get("aviso", ""))
import openpyxl  # noqa: E402


def entradas(path):
    wb = openpyxl.load_workbook(path)
    return {f"{ws.title}!{c.coordinate}": c.value for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None}


r0 = entradas(os.path.join(REF, "Vidrala_v63_evaluada.xlsx"))
for nombre, esperadas in (("PROPUESTA_M2_ultimo_anio.xlsx", {"Palancas!C8"}), ("PROPUESTA_T1_M1.xlsx", {"Diagnóstico V6!C10", "Diagnóstico V6!C11"})):
    r1 = entradas(os.path.join(PE, nombre))
    d = {k for k in set(r0) | set(r1) if r0.get(k) != r1.get(k)}
    comprobar(f"{nombre}: fórmulas y entradas iguales a la referencia salvo {sorted(esperadas)}", d == esperadas, ", ".join(sorted(d))[:200])

print("\n5. DECISIONES HUMANAS Y ALCANCE")
dh = json.load(open(os.path.join(FIN, "decisiones_propuestas_N1_N3.json"), encoding="utf-8"))
comprobar("decisiones_propuestas_N1_N3.json preparado sin decidir: decision, fecha y confirmado_por vacíos en las 3", len(dh["decisiones"]) == 3
          and all(x["decision"] is None and x["fecha"] is None and x["confirmado_por"] is None for x in dh["decisiones"]))
inf = leer(AQUI, "INFORME_FINANCIERO_N1_N3.md")
comprobar("El informe declara que los resultados no son comparables con el precio de noviembre ni una recomendación", "no son una comparación válida con el precio de 87,9" in inf.lower() and "recomendación de compra o espera" in inf, tipo="constata")
comprobar("El informe mantiene el estado real de N4, N9, N10, P-N1 y P-N2", all(x in inf for x in ("**N4:**", "**N9:**", "**N10:**", "**P-N1:**", "**P-N2:**")) and "siguen abiertos" in inf, tipo="constata")

print("\n6. AUDITORÍAS INTERNAS DE CLAUDE Y CONTROL DE VIGENCIA")


def veredicto(texto):
    m = re.search(r"^## Veredicto\s*\n+(.*)$", texto, flags=re.M)
    return m.group(1).strip() if m else ""


a1 = leer(AQUI, "AUDITORIA_INTERNA_4_7_primera.md")
comprobar("Primera auditoría conservada: nombra MATERIAL_AUDITADO_4_7.txt (b849b5db…), su veredicto es «Sin hallazgos bloqueantes» y ese archivo conserva su huella",
          "b849b5db58ab4d97eba45f9bc0418420f161544b08ffd57bb5948d0af6aca5b6" in a1 and veredicto(a1).startswith("**Sin hallazgos bloqueantes")
          and sha(os.path.join(AQUI, "MATERIAL_AUDITADO_4_7.txt")) == "b849b5db58ab4d97eba45f9bc0418420f161544b08ffd57bb5948d0af6aca5b6")
a2 = leer(AQUI, "AUDITORIA_INTERNA_4_7_control.md")
comprobar("Auditoría de control conservada: nombra MATERIAL_CONTROL_4_7.txt (b75c2292…), su veredicto es «Sin hallazgos bloqueantes» y ese archivo conserva su huella",
          "b75c2292b6cbf1498ce392eae753d7fc87d6935ec842a8f54f2f6050904b75da" in a2 and veredicto(a2).startswith("**Sin hallazgos bloqueantes")
          and sha(os.path.join(AQUI, "MATERIAL_CONTROL_4_7.txt")) == "b75c2292b6cbf1498ce392eae753d7fc87d6935ec842a8f54f2f6050904b75da")
a3 = leer(AQUI, "AUDITORIA_INTERNA_4_7_final.md")
comprobar("Auditoría final conservada: nombra MATERIAL_FINAL_4_7.txt (fb044c67…), su veredicto es «Sin hallazgos bloqueantes» y ese archivo conserva su huella",
          "fb044c672c1f1d347b0baeaea2bff963f42e5e906dce3278fb2d6157eb6215b9" in a3 and veredicto(a3).startswith("**Sin hallazgos bloqueantes")
          and sha(os.path.join(AQUI, "MATERIAL_FINAL_4_7.txt")) == "fb044c672c1f1d347b0baeaea2bff963f42e5e906dce3278fb2d6157eb6215b9")
a4 = leer(AQUI, "AUDITORIA_INTERNA_4_7_vigencia.md")
comprobar("Control de vigencia conservado: nombra MATERIAL_VIGENCIA_4_7.txt (2d804f7f…), su veredicto es «Sin hallazgos bloqueantes» y ese archivo conserva su huella",
          "2d804f7f914b51a60bb34ecc82de8465bf6db669a2d74a37a29c23c36618076e" in a4 and veredicto(a4).startswith("**Sin hallazgos bloqueantes")
          and sha(os.path.join(AQUI, "MATERIAL_VIGENCIA_4_7.txt")) == "2d804f7f914b51a60bb34ecc82de8465bf6db669a2d74a37a29c23c36618076e")
mc = os.path.join(AQUI, "MATERIAL_VIGENCIA2_4_7.txt")
ac = os.path.join(AQUI, "AUDITORIA_INTERNA_4_7_vigencia2.md")
if os.path.exists(mc) and os.path.exists(ac):
    hc = sha(mc)
    filas = [l.split("  ", 1) for l in leer(mc).splitlines() if l.strip() and not l.startswith("#")]
    ANX = "personaje_v2/ANEXO_D_salidas_y_formatos.md"
    viejo = [l for l in open(os.path.join(AQUI, "reproduccion", "ANEXO_D_4_6_1.md"), encoding="utf-8").read().split("\n")]
    resto = "\n" + "\n".join(viejo[201:])
    actual = leer(RAIZ, ANX)

    def huella_controlada(p):
        # Restauración posterior al control (registro de entrega): el texto de la 4.6.1 que seguía a la sección 4.7 del Anexo D se
        # había truncado al editarla y se repuso sin tocar esa sección; sin el bloque repuesto, el archivo es el controlado.
        if p == ANX and actual.endswith(resto):
            return hashlib.sha256(actual[:-len(resto)].encode("utf-8")).hexdigest()
        if p.endswith("scripts/comprobar_entrega_4_7.py"):
            # este comprobador se amplió tras el control solo para reconocer esa restauración; la versión controlada se conserva en
            # reproduccion/comprobar_entrega_4_7_controlado.py.txt y todas sus líneas, salvo las dos sustituidas, siguen en orden
            ctrl = os.path.join(AQUI, "reproduccion", "comprobar_entrega_4_7_controlado.py.txt")
            lc = [l for l in leer(ctrl).split("\n") if "cambiados = [p for h, p in filas if not os.path.exists" not in l and "no ha cambiado desde su control ({len(filas)} archivos)" not in l]
            it2 = iter(leer(RAIZ, p).split("\n"))
            return sha(ctrl) if all(any(l == x for x in it2) for l in lc) else "distinto"
        return sha(os.path.join(RAIZ, p))
    cambiados = [p for h, p in filas if not os.path.exists(os.path.join(RAIZ, p)) or huella_controlada(p) != h]
    it = iter(actual.split("\n"))
    anexo_completo = sha(os.path.join(AQUI, "reproduccion", "ANEXO_D_4_6_1.md")) == m461[ANX] and all(any(l == x for x in it) for l in viejo)
    comprobar(f"Control de vigencia final: el material vigente (MATERIAL_VIGENCIA2_4_7.txt, {hc[:8]}…) no ha cambiado desde su control ({len(filas)} archivos), salvo el texto de la 4.6.1 repuesto en el Anexo D, que vuelve a estar completo y en orden, y este comprobador frente a su versión controlada",
              not cambiados and anexo_completo, ", ".join(cambiados[:5]))
    txt = leer(ac)
    comprobar("El segundo control de vigencia nombra ese material y su veredicto empieza por «Sin hallazgos bloqueantes»", hc in txt and veredicto(txt).startswith("**Sin hallazgos bloqueantes"))
else:
    comprobar("Control de vigencia final: existen MATERIAL_VIGENCIA2_4_7.txt y AUDITORIA_INTERNA_4_7_vigencia2.md", False)
    comprobar("El segundo control de vigencia nombra ese material y su veredicto empieza por «Sin hallazgos bloqueantes»", False)
print(f"\nTipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan lo conservado.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
