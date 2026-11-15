#!/usr/bin/env python3
"""Controles de la entrega 4.7.1 (W-1, hallazgos de su auditoría interna y subsanación del N3). Solo escribe en temporales.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_entrega_4_7_1.py

Tipos: [reejecuta] vuelve a ejecutar un script o una batería (en copias); [recalcula] recalcula desde los archivos actuales;
[constata] solo lee lo conservado. Tarda unos 4 minutos (reejecuta tres veces la batería del resumen y la de la 4.7).
"""
import csv
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
E47 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_7")
FIN = os.path.join(AQUI, "financiero")
REP = os.path.join(AQUI, "reproduccion")
sys.path.insert(0, os.path.join(PV2, "scripts"))
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402

N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
CODIGO = ["personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/ficha.py", "personaje_v2/scripts/resumen.py", "personaje_v2/scripts/pipeline.py",
          "verificar_paquete.sh", "personaje_v2/pruebas/test_resumen_v2.py"]
DOCUMENTACION = ["personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/DECISIONES.md", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "VERSION", "CAMBIOS_ARCHIVOS.txt", "MANIFIESTO_SHA256.txt"]
ZIP = "munger_v2_r1_entrega4.7.1_w1_y_n3.zip"
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


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


def py(*args, cwd=None):
    return subprocess.run([sys.executable, "-I", *args], capture_output=True, text=True, env=ENV, cwd=cwd)


def veredicto(texto):
    m = re.search(r"^## Veredicto\s*\n+(.*)$", texto, flags=re.M)
    return m.group(1).strip() if m else ""


def resumen_bateria(txt):
    lineas = txt.splitlines()
    final = [l for l in lineas if re.match(r"^\d+/\d+ pruebas", l)]
    return lineas[0] if lineas else "", final[-1] if final else "", [l for l in lineas if l.startswith("FALLA")]


print("ENTREGA 4.7.1 · W-1, auditoría interna y subsanación del N3 · controles (solo escriben en temporales)")
print("=" * 100)
print("\n1. REFERENCIAS INTACTAS FRENTE A LA 4.7")
m47 = {}
for l in open(os.path.join(REP, "MANIFIESTO_SHA256_4_7.txt"), encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        m47[p] = h
comprobar("El manifiesto 4.7 conservado es el del paquete 4.7 (SHA-256 2c1c1842…cd75; 1.412 archivos)",
          sha(os.path.join(REP, "MANIFIESTO_SHA256_4_7.txt")) == "2c1c184283305dfe34173f4c42724f37e67182fbe659ca102a8ab78d2045cd75" and len(m47) == 1412)
iguales = {k: v for k, v in m47.items() if k not in CODIGO and k not in DOCUMENTACION}
dif = [k for k, v in iguales.items() if not os.path.exists(os.path.join(RAIZ, k)) or sha(os.path.join(RAIZ, k)) != v]
comprobar(f"Los {len(iguales)} archivos de la 4.7 que no son el código declarado ni documentación conservan su huella (originales, expedientes 4.4–4.7, libros, fases, fuentes, informe.py)", not dif, ", ".join(dif[:5]))
comprobar("Entre ellos, los 489 originales y la carpeta completa de la 4.7", sum(k.startswith("personaje_v2/empresas_v2/") for k in iguales) == 489
          and all(k in iguales for k in m47 if k.startswith("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_7/")))
comprobar("Registro humano de P1 sin cambios (b4e47afc…c445a4)", sha(os.path.join(REF, "fase1_decisiones.json")) == "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4")
ct = leer(AQUI, "CIERRE_TECNICO_4_7_1.md")
tabla1 = dict(re.findall(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", ct.split("## 5.")[0]))
comprobar("Copias del código para reproducir: `reproduccion/codigo_4_7/` = código del manifiesto 4.7 (4 archivos); `codigo_auditado_4_7_1/` = huellas del primer cierre (3 archivos)",
          all(sha(os.path.join(REP, "codigo_4_7", f"{n}.py.txt")) == m47[f"personaje_v2/scripts/{n}.py"] for n in ("cierre_v2", "ficha", "resumen", "pipeline"))
          and all(sha(os.path.join(REP, "codigo_auditado_4_7_1", f"{n}.py.txt")) == tabla1[f"personaje_v2/scripts/{n}.py"] for n in ("cierre_v2", "ficha", "resumen")))

print("\n2. W-1 Y HALLAZGOS W DE LA AUDITORÍA INTERNA · CÓDIGO Y PRUEBAS")
huellas = {}
for bloque in re.split(r"\n## ", ct):
    huellas.update(dict(re.findall(r"\| `([^`]+)` \| `([0-9a-f]{64})` \|", bloque)))
comprobar("El código conserva las huellas de la última tabla del cierre técnico (§6, 7 archivos)", len(huellas) == 7 and all(sha(os.path.join(RAIZ, k)) == v for k, v in huellas.items()),
          ", ".join(k for k, v in huellas.items() if sha(os.path.join(RAIZ, k)) != v))
a = leer(REP, "reproduccion_w1_codigo_4_7.txt")
comprobar("Reproducción de W-1 con el código 4.7 (conservada): REPRODUCIDO", "REPRODUCIDO:" in a and "NO SE REPRODUCE" not in a and "entrega47" in a.splitlines()[0], tipo="constata")
rr = py(os.path.join(AQUI, "scripts", "reproducir_w1.py"), "--raiz", RAIZ)
comprobar("Reproducción de W-1 con el código actual: NO SE REPRODUCE, sin ninguna llamada posterior", rr.returncode == 0 and "NO SE REPRODUCE" in rr.stdout and "REPRODUCIDO:" not in rr.stdout, tipo="reejecuta")
rr = py(os.path.join(AQUI, "scripts", "ejecutar_baterias_4_7_1.py"), "--solo-comprobar")
comprobar("Batería del resumen reejecutada en copias con el código actual, el de la 4.7 y el que vio la auditoría: las tres coinciden con sus salidas conservadas (huellas, estado de cada prueba y línea final)",
          rr.returncode == 0 and rr.stdout.count("coincide con la conservada") == 3, rr.stdout.replace("\n", " | ")[:300], tipo="reejecuta")
h0, f0, x0 = resumen_bateria(leer(AQUI, "resultados", "test_resumen_v2_salida.txt"))
comprobar("…con el código actual: 45/45, con las huellas del cierre revisado", f0 == "45/45 pruebas de aceptación del resumen PASAN" and not x0 and h0.startswith("# código:")
          and f"cierre_v2.py {huellas['personaje_v2/scripts/cierre_v2.py'][:16]}" in h0 and f"pipeline.py {huellas['personaje_v2/scripts/pipeline.py'][:16]}" in h0, tipo="constata")
h1, f1, x1 = resumen_bateria(leer(REP, "pruebas_resumen_con_codigo_4_7.txt"))
comprobar("…con el código 4.7: 35/45; fallan las 3 de W-1 y 7 de las 8 añadidas tras la auditoría (W-a, W-b, W-e, W-f)",
          f1.startswith("35/45") and len(x1) == 10 and sum("· W-1" in l for l in x1) == 3 and sum("· W-a" in l for l in x1) == 4 and all(any(f"· {w}" in l for l in x1) for w in ("W-b", "W-e", "W-f"))
          and f"cierre_v2.py {m47['personaje_v2/scripts/cierre_v2.py'][:16]}" in h1, tipo="constata")
h2, f2, x2 = resumen_bateria(leer(REP, "pruebas_resumen_con_codigo_auditado.txt"))
comprobar("…con el código que vio la auditoría: 36/45; la regresión W-a hace fallar sus 4 pruebas", f2.startswith("36/45") and len(x2) == 9 and sum("· W-a" in l for l in x2) == 4
          and f"cierre_v2.py {tabla1['personaje_v2/scripts/cierre_v2.py'][:16]}" in h2, tipo="constata")
for f, linea in (("test_cierre_v2_salida.txt", "55/55 pruebas de aceptación del cierre PASAN"), ("test_pipeline_sintetico_salida.txt", "30/30 pruebas PASAN")):
    h, fin, x = resumen_bateria(leer(AQUI, "resultados", f))
    comprobar(f"resultados/{f}: {linea.split()[0]} con el código actual (huellas en su cabecera; se reejecuta en verificar_paquete.sh completa)",
              fin == linea and not x and all(f"{os.path.basename(k)} {v[:16]}" in h for k, v in huellas.items()), tipo="constata")
rr = py(os.path.join(AQUI, "scripts", "comprobar_integracion_verificador_471.py"))
comprobar("Integración de la batería del resumen en verificar_paquete.sh completa (mínimo 45): 13 de 13, salida idéntica a la conservada",
          rr.returncode == 0 and "RESULTADO: 13 de 13" in rr.stdout and leer(AQUI, "resultados", "comprobar_integracion_verificador_471_salida.txt").strip() == rr.stdout.strip(), tipo="reejecuta")
rr = py(os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "scripts", "comprobar_integracion_verificador.py"))
comprobar("Integración de la batería de cierre (4.6.1, mínimo 55): 13 de 13", rr.returncode == 0 and "RESULTADO: 13 de 13" in rr.stdout, tipo="reejecuta")
rr = py(os.path.join(E47, "scripts", "comprobar_entrega_4_7.py"))
fallan = [l for l in rr.stdout.splitlines() if "[NO CUMPLE]" in l]
esperados = ("El código del bloque A conserva las huellas del cierre definitivo", "Integración de la batería del resumen en verificar_paquete.sh completa (mínimo 34)", "Control de vigencia final: el material vigente (MATERIAL_VIGENCIA2_4_7.txt")
comprobar("Batería de la 4.7 sobre el árbol 4.7.1: 46 de 49, y solo fallan sus 3 controles ligados al código y a la documentación de la 4.7 (salida idéntica a la conservada)",
          "RESULTADO: 46 de 49" in rr.stdout and len(fallan) == 3 and all(any(e in l for l in fallan) for e in esperados)
          and rr.stdout.strip() == leer(AQUI, "resultados", "comprobar_entrega_4_7_en_arbol_4_7_1.txt").strip(), tipo="reejecuta")
comprobar("El expediente de referencia 4.6.1 sigue vigente con el código 4.7.1, sin registro de publicaciones", CIE.motivo_vigencia(REF, pipeline.Pipeline.veredicto_auditoria) is None
          and not CIE.retiradas_pendientes(REF) and not os.path.exists(os.path.join(REF, CIE.REGISTRO_RESUMEN)) and not os.path.exists(os.path.join(REF, CIE.RESPALDO_RESUMEN)))
# (C-a) la conservación y una variante de W-a se ejecutan, no solo se evalúan
HOJA = {"precio": "87.90", "precio_si": "65.6880873204157", "ponderado": "70.4951544152", "fecha": "11/03/26"}
EMP = json.load(open(os.path.join(REF, "ficha.json"), encoding="utf-8"))["empresa"]


def preparar(tmp, reescribir):
    base = os.path.join(tmp, "exp")
    d = os.path.join(base, "Vidrala")
    shutil.copytree(REF, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        shutil.copy(os.path.join(os.path.dirname(REF), f), os.path.join(base, f))
    pred = os.path.join(base, "resumen_v2.csv")
    if reescribir:
        rd = csv.DictReader(open(pred, encoding="utf-8"))
        cols, filas = rd.fieldnames, [dict(r, **HOJA) if r["empresa"] == EMP else r for r in rd]
        with open(pred, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(filas)
    return d, pred


def fila(p):
    return [r for r in csv.DictReader(open(p, encoding="utf-8")) if r["empresa"] == EMP] if os.path.exists(p) else []


tmp = tempfile.mkdtemp(prefix="c471v_")
try:
    d, pred = preparar(tmp, True)
    antes = open(pred, encoding="utf-8").read()
    otro = os.path.join(tmp, "otro.csv")
    r = subprocess.run([sys.executable, "-B", os.path.join(PV2, "scripts", "resumen.py"), d, otro], capture_output=True, text=True, env=ENV)
    comprobar("Conservación ejecutada: con la ficha vigente y su fila del predeterminado reescrita por una hoja de cálculo, resumen.py hacia otro destino publica (código 0) y no toca el predeterminado",
              r.returncode == 0 and open(pred, encoding="utf-8").read() == antes and [x["verificacion"] for x in fila(otro)] == ["APROBADO"], f"código {r.returncode}", tipo="reejecuta")
    tmp2 = os.path.join(tmp, "b")
    os.makedirs(tmp2)
    d, pred = preparar(tmp2, True)
    fc = json.load(open(os.path.join(d, "fase_c.json"), encoding="utf-8"))
    fc["celdas"]["B101"] += " [MARCADOR control 4.7.1]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(PV2, "scripts", "resumen.py"), d, os.path.join(tmp2, "otro.csv")], capture_output=True, text=True, env=ENV)
    f = fila(pred)
    comprobar("Variante de W-a ejecutada: la misma fila reescrita, con el material invalidado, se retira en la misma llamada (código 3)",
              r.returncode == 3 and len(f) == 1 and f[0]["verificacion"].startswith("SIN APROBACIÓN VIGENTE") and not f[0]["precio_si"], f"código {r.returncode}", tipo="reejecuta")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
anx = leer(PV2, "ANEXO_D_salidas_y_formatos.md")
comprobar("El Anexo D declara el criterio corregido (detección por fecha, exclusión por contenido con tolerancia), el código 0 con aviso de ficha.py, el código 4 del pipeline y el límite residual",
          "**Detección** (como en la 4.7)" in anx and "tolerancia relativa de 10⁻⁶" in anx and "termina con **código 0**, con un «AVISO»" in anx and "termina con **código 4**" in anx and "**Límite residual:**" in anx, tipo="constata")

print("\n3. N3 · DESCOMPOSICIÓN, MANTENIMIENTO Y CAPACIDAD")
tmp = tempfile.mkdtemp(prefix="c471_")
try:
    copia = os.path.join(tmp, "e471")
    shutil.copytree(AQUI, copia, ignore=shutil.ignore_patterns("__pycache__"))
    for n in ("2026-11_Vidrala_ensayo_4_6_1", "2026-11_Vidrala_ensayo_4_7"):
        os.symlink(os.path.join(CORR, n), os.path.join(tmp, n))
    rr = py(os.path.join(copia, "scripts", "analisis_n1_n3.py"))
    comprobar("analisis_n1_n3.py (4.7.1) termina con código 0 («evidencia y control correctos»)", rr.returncode == 0 and "RESULTADO: evidencia y control correctos" in rr.stdout, tipo="reejecuta")
    for f in ("salida.txt", "evidencia.json", "evidencia.md", "matriz.csv", "matriz.json", "matriz.md", "n3_anio_a_anio.csv", "sensibilidades_n3.csv"):
        comprobar(f"financiero/{f} conservado = regenerado byte a byte", sha(os.path.join(FIN, f)) == sha(os.path.join(copia, "financiero", f)), tipo="reejecuta")
finally:
    shutil.rmtree(tmp, ignore_errors=True)
M = json.load(open(os.path.join(FIN, "matriz.json"), encoding="utf-8"))
E = json.load(open(os.path.join(FIN, "evidencia.json"), encoding="utf-8"))
ev = {e["clave"]: e["valor_miles"] for e in E}
comprobar("Evidencia: 123 datos (los 109 de la 4.7 y 14 de inversión, amortización, vida útil, PERTE y mantenimiento), todos reproducidos con su signo",
          len(E) == 123 and all(e["reproduce"] and abs(e["valor_miles"] - e["esperado_miles"]) < 0.5 for e in E)
          and [e["clave"] for e in E[:109]] == [e["clave"] for e in json.load(open(os.path.join(E47, "financiero", "evidencia.json"), encoding="utf-8"))])
comprobar("Control: la matriz de 27 combinaciones tiene los valores de la 4.7 y la regla «circulante_sin_capacidad» reproduce la formulación inicial del R1", M["control"] and M["control_4_7"] and M["control_formulacion_inicial"])
m = {r["combinacion"]: r for r in csv.DictReader(open(os.path.join(FIN, "matriz.csv"), encoding="utf-8"))}
m_47 = {r["combinacion"]: r for r in csv.DictReader(open(os.path.join(E47, "financiero", "matriz.csv"), encoding="utf-8"))}
comprobar("matriz.csv: mismos valores, ponderados y precios de Sí que la 4.7 en las 27 filas", all(m[k][c] == m_47[k][c] for k in m_47 for c in ("V_malo", "V_normal", "V_bueno", "ponderado", "precio_si")) and len(m) == 27)
r1, r0 = m["T1·M1·R1"], m["T0·M0·R0"]
comprobar("Inversión bruta implícita corregida (D&A + inversión fija neta): T1·M1·R1 año 1 = 132,948 con circulante −2,15434 y fija 0; R0 = 118,82278",
          abs(float(r1["inversion_bruta_implicita_malo_a1"]) - 132.948) < 1e-5 and abs(float(r1["delta_circulante_malo_a1"]) + 2.15434) < 1e-5 and abs(float(r1["inversion_fija_neta_malo_a1"])) < 1e-9
          and abs(float(r0["inversion_bruta_implicita_malo_a1"]) - 118.82278) < 1e-5 and "cobertura_compromisos_malo" not in r1)
n3 = list(csv.DictReader(open(os.path.join(FIN, "n3_anio_a_anio.csv"), encoding="utf-8")))
comprobar("n3_anio_a_anio.csv: en cada fila, reinversión = circulante + fija neta e inversión bruta = 132,948 + fija neta", n3 and all(
    abs(float(r["reinversion_neta"]) - float(r["delta_circulante"]) - float(r["inversion_fija_neta"])) < 2e-5 and abs(float(r["inversion_bruta_implicita"]) - 132.948 - float(r["inversion_fija_neta"])) < 2e-5 for r in n3))
S = list(csv.DictReader(open(os.path.join(FIN, "sensibilidades_n3.csv"), encoding="utf-8")))
s0 = [r for r in S if r["base"] == "T1·M1" and r["regla"] == "R1" and float(r["x_sobre_DA"]) == 0]
comprobar("sensibilidades_n3.csv: 20 filas; sin mantenimiento adicional, T1·M1·R1 coincide con la matriz", len(S) == 20 and len(s0) == 1
          and abs(float(s0[0]["ponderado"]) - float(r1["ponderado"])) < 1e-4 and abs(float(s0[0]["precio_si"]) - float(r1["precio_si"])) < 1e-4)
inv = M["inversion"]
capex25 = -(ev["capex_material_2025"] + ev["capex_inmaterial_2025"]) / 1000
comprobar("Niveles de mantenimiento desde la evidencia citada (no desde constantes): (178,746 + 9,757 − 132,948) ÷ 132,948 = 41,8 %, igual que matriz.json, el estado de flujos y la Historia",
          abs(inv["x_2025"] - (capex25 - ev["da_2025"] / 1000) / (ev["da_2025"] / 1000)) < 1e-9 and abs(inv["capex_historia"]["2025"] - capex25) < 1e-6
          and abs(inv["da_historia"]["2025"] - ev["da_2025"] / 1000) < 1e-9 and {r["x_sobre_DA"] for r in S} == {"0.0", str(round(inv["x_2025"] / 2, 6)), str(round(inv["x_2025"], 6))})
dh = json.load(open(os.path.join(FIN, "decisiones_propuestas_N1_N3.json"), encoding="utf-8"))
comprobar("decisiones_propuestas_N1_N3.json (4.7.1): D-N1, D-N2, D-N3 y D-N3b, sin decision, fecha ni confirmado_por; D-N1 y D-N2 iguales a la 4.7; D-N3b dice que «=D&A» es la opción de mayor valor",
          [x["id"] for x in dh["decisiones"]] == ["D-N1", "D-N2", "D-N3", "D-N3b"] and all(x["decision"] is None and x["fecha"] is None and x["confirmado_por"] is None for x in dh["decisiones"])
          and dh["decisiones"][:2] == json.load(open(os.path.join(E47, "financiero", "decisiones_propuestas_N1_N3.json"), encoding="utf-8"))["decisiones"][:2]
          and "la de mayor valor" in dh["decisiones"][3]["propuesta_de_claude"])
inf = leer(AQUI, "INFORME_N3_SUBSANACION.md")
comprobar("El informe declara con exactitud qué sustituye (N-c), que no es comparable con el precio ni una recomendación, que las sensibilidades no son cotas, y los límites en los dos sentidos (N-a, N-b)",
          "sustituye la viñeta «Necesidades de caja» del §4.2" in inf and "son una comparación válida con el precio de 87,9" in inf and "recomendación de compra o espera" in inf
          and "no son alternativas de la matriz ni cotas" in inf and "**Límites en el otro sentido**" in inf and "no la duración de una campaña" in inf and "Es inversión de renovación, no de ampliación" not in inf, tipo="constata")

print("\n4. AUDITORÍA INTERNA DE CLAUDE Y CONTROL DE VIGENCIA")
pares = [("MATERIAL_AUDITORIA_4_7_1.txt", "AUDITORIA_INTERNA_4_7_1.md", "**Con hallazgos bloqueantes**"), ("MATERIAL_VIGENCIA_4_7_1.txt", "AUDITORIA_INTERNA_4_7_1_vigencia.md", "**Sin hallazgos bloqueantes**")]
for mf, af, esperado in pares:
    existe = os.path.exists(os.path.join(AQUI, mf)) and os.path.exists(os.path.join(AQUI, af))
    txt = leer(AQUI, af) if existe else ""
    comprobar(f"{af}: nombra {mf}" + (f" ({sha(os.path.join(AQUI, mf))[:8]}…)" if existe else "") + f" y su veredicto empieza por {esperado}",
              existe and sha(os.path.join(AQUI, mf)) in txt and veredicto(txt).startswith(esperado), tipo="constata")
mf = pares[-1][0]
if os.path.exists(os.path.join(AQUI, mf)):
    filas = [l.split("  ", 1) for l in leer(AQUI, mf).splitlines() if l.strip() and not l.startswith("#")]
    cambiados = [p for h, p in filas if not os.path.exists(os.path.join(RAIZ, p)) or sha(os.path.join(RAIZ, p)) != h]
    comprobar(f"El material del control de vigencia ({mf}, {len(filas)} archivos, con el código y los documentos corregidos) no ha cambiado desde ese control", not cambiados and len(filas) > 30, ", ".join(cambiados[:5]))
else:
    comprobar("El material del control de vigencia está fijado", False)

print("\n5. DOCUMENTACIÓN DE LA ENTREGA")
version = leer(RAIZ, "VERSION")
cont, prom = leer(RAIZ, "CONTINUIDAD.md"), leer(RAIZ, "PROMPT_NUEVA_VENTANA.md")
comprobar("VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.7.1: versión, ZIP, batería del resumen de 45 y este control",
          version.startswith("munger_v2 · r1 · entrega 4.7.1") and ZIP in cont and ZIP in prom and "**45/45 PASAN**" in cont and "37/37, van ya dentro" not in prom
          and "45/45, van ya dentro" in prom and "comprobar_entrega_4_7_1.py" in cont and "comprobar_entrega_4_7_1.py" in prom, tipo="constata")
comprobar("Registro de la entrega presente (REGISTRO_ENTREGA_4.7.1.md)", os.path.exists(os.path.join(AQUI, "REGISTRO_ENTREGA_4.7.1.md")), tipo="constata")
print(f"\nTipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan lo conservado.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
