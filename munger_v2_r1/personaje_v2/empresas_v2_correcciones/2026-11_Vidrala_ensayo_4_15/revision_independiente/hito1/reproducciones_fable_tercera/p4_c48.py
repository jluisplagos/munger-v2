"""Sondas de la vía generativa (C48) sobre el árbol CONGELADO: calcular_entrada, construir, rellenar (--estricta) y entradas_no_reproducibles.
Hallazgos 4, 7, 13 y observación 22. Sin LibreOffice."""
import copy, json, os, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable3/congelado3/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as FH
import verificacion_entradas as VE
from v63_xml import LibroV63
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
ELIS = os.path.join(E414, "elis_decisiones", "Elis"); VIDRALA = os.path.join(E414, "vidrala_decisiones", "Vidrala"); VISCOFAN = os.path.join(E414, "viscofan_decisiones", "Viscofan")
CAMBIO = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json")
TMP = tempfile.mkdtemp(prefix="rev_fable_c48_")
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]
CALC = json.load(open(CAMBIO, encoding="utf-8"))["analisis"]["C48"]["calculo"]
REL = os.path.join(PV, "scripts", "rellenar_fase1_v63.py"); CFG = os.path.join(PV, "config_v2.json")


def calc(cal, carpeta=None, **d):
    try:
        r = FH.calcular_entrada("C48", dict(d, calculo=cal), H, anios, carpeta)
        return f"valor={r['valor']!r}" + (f" pendiente_verificacion={r.get('pendiente_verificacion')}" if r.get("pendiente_verificacion") else "")
    except Exception as ex:
        return f"{type(ex).__name__}: {str(ex)[:150]}"


print("=== 1 · hallazgo 13: calcular_entrada")
r0 = FH.calcular_entrada("C48", {"calculo": CALC}, H, anios, ELIS)
print("caso real (con carpeta):", r0["valor"], "| sin redondear:", repr(r0.get("valor_sin_redondear")), "| fuente:", r0["fuente"][:230])
for red in (0, -1, 2, None, "3", 2.5, True, 3, 6):
    c2 = copy.deepcopy(CALC); c2["redondeo"] = red; c2["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = 179.0
    print(f"  componente 2025 = 179,0 (media exacta 108,3667) con redondeo={red!r} (sin carpeta):", calc(c2), "| con valor declarado 108:", calc(c2, valor=108))
c3 = copy.deepcopy(CALC); c3["anios"] = [2025, 2025, 2025]; print("años repetidos:", calc(c3))
c5 = copy.deepcopy(CALC); c5["anios"] = ["2023", 2024.0, 2025]; print("años como texto y decimal:", calc(c5))
c6 = copy.deepcopy(CALC); c6["anios"] = [2023, None, 2025]; print("un año None:", calc(c6))
c6b = copy.deepcopy(CALC); c6b["anios"] = [2025, 2023, 2024]; print("años desordenados [2025, 2023, 2024]:", calc(c6b, ELIS), "| periodo:", FH.calcular_entrada("C48", {"calculo": c6b}, H, anios, ELIS)["periodo"])
c7 = copy.deepcopy(CALC); c7["terminos"][0]["signo"] = True; print("signo True:", calc(c7))
c8 = copy.deepcopy(CALC); c8["componentes"]["pagos_arrendamientos_con_intereses"]["2025"].update(fuente="texto/NO_EXISTE.txt", pagina=99999, cita=None)
print("componente con fuente inexistente, página 99999 y sin cita: sin carpeta →", calc(c8), "| con carpeta →", calc(c8, ELIS))
c9 = copy.deepcopy(CALC); c9["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = 1779.0
print("componente 2025 = 1779,0 (errata ×10): sin carpeta →", calc(c9), "| con carpeta →", calc(c9, ELIS))
c9b = copy.deepcopy(CALC); c9b["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = 150.8
print("componente 2025 = 150,8 (la cifra de la OTRA columna de la misma cita: 2024): con carpeta →", calc(c9b, ELIS))
c9c = copy.deepcopy(CALC); c9c["componentes"]["pagos_arrendamientos_con_intereses"]["2025"].update(fuente="/etc/hostname")
print("componente con fuente de ruta absoluta: con carpeta →", calc(c9c, ELIS))
c9d = copy.deepcopy(CALC); c9d["componentes"]["pagos_arrendamientos_con_intereses"]["2025"].update(pagina="327-328")
print("componente con página «327-328»: con carpeta →", calc(c9d, ELIS))
c9e = copy.deepcopy(CALC); c9e["terminos"].append({"componente": "pagos_arrendamientos_con_intereses", "signo": -1}); c9e["terminos"].append({"partida": "ventas", "signo": 1})
print("términos arbitrarios (se añade − el mismo componente y + ventas): con carpeta →", calc(c9e, ELIS))
c9f = copy.deepcopy(CALC); c9f["componentes"] = ["x"]; print("componentes que no son un objeto:", calc(c9f))
c9g = copy.deepcopy(CALC); c9g["terminos"] = "x"; print("términos que no son una lista:", calc(c9g))
c9h = copy.deepcopy(CALC); c9h["componentes"]["pagos_arrendamientos_con_intereses"] = "x"; print("un componente que no es un objeto:", calc(c9h))
print("valor declarado True:", calc(CALC, valor=True), "| valor declarado '108':", calc(CALC, valor="108"), "| valor declarado 108.0004:", calc(CALC, valor=108.0004))
try:
    print("calculo que no es un objeto:", FH.calcular_entrada("C48", {"calculo": [1]}, H, anios))
except Exception as ex:
    print("calculo que no es un objeto:", type(ex).__name__, str(ex)[:80])

print("\n=== 2 · hallazgo 7: un cálculo declarado que usa ceros pendientes de verificación (H1)")
c10 = copy.deepcopy(CALC); c10["anios"] = [2016, 2017, 2018]; c10["terminos"] = [{"partida": "intereses_financiacion", "signo": 1}, {"partida": "arrendamientos_principal", "signo": -1}]
print("pendientes de la Historia:", {k: p.get("pendientes_verificacion") for k, p in H.items() if isinstance(p, dict) and p.get("pendientes_verificacion")}, "| pendientes_celda('C48'):", FH.pendientes_celda("C48", H, anios, 3))
print("media 2016–2018 de intereses_financiacion − arrendamientos_principal:", calc(c10))
dF = os.path.join(TMP, "construir", "Elis"); os.makedirs(dF)
for n in ("fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json", "texto", "etapa1"):
    o = os.path.join(ELIS, n); (shutil.copytree if os.path.isdir(o) else shutil.copy2)(o, os.path.join(dF, n))
m = json.load(open(os.path.join(dF, "fase1_metadatos.json"), encoding="utf-8"))
m.setdefault("analisis", {})["C48"] = {"calculo": c10}
json.dump(m, open(os.path.join(dF, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dF], capture_output=True, text=True)
print("construir: rc", r.returncode, (r.stdout + r.stderr).strip()[-160:])
g = json.load(open(os.path.join(dF, "fase1_v63.json"), encoding="utf-8"))
print("   C48:", {k: v for k, v in g["analisis"]["C48"].items() if k in ("valor", "pendiente_verificacion", "periodo", "nota")})
base = os.path.join(ELIS, "Elis_v63_base.xlsx"); vacio = os.path.join(TMP, "base_sin_migrados.xlsx")
lb = LibroV63(base); lb.escribir_celdas({f"Análisis!{c}": None for c in ("C46", "C47", "C48", "C49", "C50")}); lb.guardar(vacio)
out = os.path.join(TMP, "h1.xlsx")
r = subprocess.run([sys.executable, "-B", REL, vacio, os.path.join(dF, "fase1_v63.json"), out, "--config", CFG], capture_output=True, text=True)
L = LibroV63(out) if os.path.exists(out) else None
print("rellenar (base sin migrados): rc", r.returncode, "| C48 =", L and L.leer("Análisis", "C48"), "| Control maestro F45 =", L and L.leer("Control maestro", "F45"), "| N45 =", str(L and L.leer("Control maestro", "N45"))[:160])
out2 = os.path.join(TMP, "h1b.xlsx")
r = subprocess.run([sys.executable, "-B", REL, base, os.path.join(dF, "fase1_v63.json"), out2, "--config", CFG], capture_output=True, text=True)
L2 = LibroV63(out2) if os.path.exists(out2) else None
rg2 = json.load(open(out2 + ".fase1.registro.json", encoding="utf-8")) if os.path.exists(out2 + ".fase1.registro.json") else {}
print("rellenar (base CON el 108 migrado; la declarada 55,233 está pendiente por H1): rc", r.returncode, "| C48 =", L2 and L2.leer("Análisis", "C48"), "| F45 =", L2 and L2.leer("Control maestro", "F45"),
      "| entradas_migradas_distintas:", [(x["celda"], x["libro"], x["fase1_v63"], x["motivo"][:60]) for x in rg2.get("entradas_migradas_distintas") or []])
r = subprocess.run([sys.executable, "-B", REL, base, os.path.join(dF, "fase1_v63.json"), out2 + ".e.xlsx", "--config", CFG, "--estricta"], capture_output=True, text=True)
print("   ídem con --estricta: rc", r.returncode, "| libro escrito:", os.path.exists(out2 + ".e.xlsx"), "|", (r.stdout + r.stderr).strip().splitlines()[0][:130])

print("\n=== 3 · hallazgo 4: entradas_no_reproducibles")
def copia(src, nombre):
    d = os.path.join(TMP, nombre, os.path.basename(src))
    shutil.copytree(src, d, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__", "historial_cierres", "antecedentes", "texto", "fuentes_pdf", "fase1_partes"))
    return d
def nr(d):
    return {k: (v[0], v[1], v[2][:60]) for k, v in VE.entradas_no_reproducibles(d, VE.universo(d)).items()}
e0 = copia(ELIS, "e0"); print("Elis 4.14 tal cual:", nr(e0))
e1 = copia(ELIS, "e1"); os.remove(os.path.join(e1, "fase1_v63.json")); print("(a) sin fase1_v63.json:", sorted(nr(e1)), "| apto:", VE.comprobar(e1)["apto_por_entradas"])
e2 = copia(ELIS, "e2"); open(os.path.join(e2, "fase1_v63.json"), "w").write("{ roto"); print("(b) fase1_v63.json ilegible:", sorted(nr(e2)))
e2b = copia(ELIS, "e2b"); json.dump([], open(os.path.join(e2b, "fase1_v63.json"), "w"));
try:
    print("(b') fase1_v63.json = []:", sorted(nr(e2b)), "| comprobar sin excepción: apto =", VE.comprobar(e2b)["apto_por_entradas"])
except Exception as ex:
    print("(b') LANZA", type(ex).__name__, ex)
e2c = copia(ELIS, "e2c"); x = json.load(open(os.path.join(e2c, "fase1_v63.json"), encoding="utf-8")); x["analisis"] = ["x"]; json.dump(x, open(os.path.join(e2c, "fase1_v63.json"), "w"))
print("(b'') «analisis» que no es un objeto:", sorted(nr(e2c)))
e3 = copia(ELIS, "e3"); x = json.load(open(os.path.join(e3, "fase1_v63.json"), encoding="utf-8")); del x["analisis"]["C48"]; json.dump(x, open(os.path.join(e3, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(c) fase1_v63.json sin declarar C48:", nr(e3))
e4 = copia(ELIS, "e4"); x = json.load(open(os.path.join(e4, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"]["valor"] = 108; json.dump(x, open(os.path.join(e4, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(d) fase1_v63.json editado a mano: C48.valor = 108 (sin cálculo, con la fuente de la media 82,933):", nr(e4), "| fuente que sigue declarando:", x["analisis"]["C48"]["fuente"][:90])
e5 = copia(ELIS, "e5"); x = json.load(open(os.path.join(e5, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"]["valor"] = "108"; json.dump(x, open(os.path.join(e5, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(e) valor declarado como texto «108»:", nr(e5))
e6 = copia(ELIS, "e6"); x = json.load(open(os.path.join(e6, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"] = 108; json.dump(x, open(os.path.join(e6, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(e') declaración escalar C48 = 108 (sin objeto ni fuente):", nr(e6))
e7 = copia(ELIS, "e7"); x = json.load(open(os.path.join(e7, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"]["valor"] = 108.0000000005; json.dump(x, open(os.path.join(e7, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(e'') declaración 108.0000000005:", nr(e7), "| 108.0004:", end=" ")
x["analisis"]["C48"]["valor"] = 108.0004; json.dump(x, open(os.path.join(e7, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False); print(nr(e7))
for nom, src in (("Vidrala", VIDRALA), ("Viscofan", VISCOFAN)):
    v0 = copia(src, "v_" + nom); iv = VE.universo(v0); fv = json.load(open(os.path.join(v0, "fase1_v63.json"), encoding="utf-8"))
    print(f"(f) {nom} final 4.14: libro", {c: iv["celdas"].get(f"Análisis!{c}") for c in ("C46", "C47", "C48", "C49", "C50")}, "| declaradas:", {c: (fv["analisis"].get(c) or {}).get("valor") if isinstance(fv["analisis"].get(c), dict) else fv["analisis"].get(c) for c in ("C46", "C47", "C48", "C49", "C50")}, "| no reproducibles:", nr(v0))
# libro con la celda vacía y declaración con valor (sentido contrario)
e8 = copia(ELIS, "e8"); lb8 = LibroV63(VE.libro_de(e8)); lb8.escribir_celdas({"Análisis!C48": None}); lb8.guardar(VE.libro_de(e8))
print("(g) libro con C48 VACÍA y fase1_v63.json que declara 82,933 (sentido contrario):", nr(e8))

print("\n=== 4 · rellenar: registro de entradas migradas y --estricta en los tres expedientes finales de la 4.14")
for nom, src in (("Elis", ELIS), ("Vidrala", VIDRALA), ("Viscofan", VISCOFAN)):
    cfg = os.path.join(PV, json.load(open(os.path.join(src, "plantilla_activa.json"), encoding="utf-8"))["config"]) if os.path.exists(os.path.join(src, "plantilla_activa.json")) else CFG
    o = os.path.join(TMP, f"rel_{nom}.xlsx")
    r = subprocess.run([sys.executable, "-B", REL, os.path.join(src, f"{nom}_v63_base.xlsx"), os.path.join(src, "fase1_v63.json"), o, "--config", cfg], capture_output=True, text=True)
    rg = json.load(open(o + ".fase1.registro.json", encoding="utf-8")) if os.path.exists(o + ".fase1.registro.json") else {}
    r7 = subprocess.run([sys.executable, "-B", REL, os.path.join(src, f"{nom}_v63_base.xlsx"), os.path.join(src, "fase1_v63.json"), o + ".e.xlsx", "--config", cfg, "--estricta"], capture_output=True, text=True)
    print(f"{nom}: rc {r.returncode} · entradas_migradas_distintas: {[(x['celda'].split('!')[1], x['libro'], x['fase1_v63']) for x in rg.get('entradas_migradas_distintas') or []]} · --estricta: rc {r7.returncode}, libro escrito: {os.path.exists(o + '.e.xlsx')}, registro escrito: {os.path.exists(o + '.e.xlsx.fase1.registro.json')}")
# --estricta con --sobrescribir
o = os.path.join(TMP, "rel_elis_sobre.xlsx")
r = subprocess.run([sys.executable, "-B", REL, os.path.join(ELIS, "Elis_v63_base.xlsx"), os.path.join(ELIS, "fase1_v63.json"), o, "--config", CFG, "--estricta", "--sobrescribir"], capture_output=True, text=True)
print("Elis --estricta --sobrescribir: rc", r.returncode, "| C48 =", LibroV63(o).leer("Análisis", "C48") if os.path.exists(o) else None, "|", (r.stdout + r.stderr).strip().splitlines()[0][:140])
shutil.rmtree(TMP, ignore_errors=True)
