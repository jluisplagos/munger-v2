"""Sondas de la vía generativa (C48): calcular_entrada, construir, rellenar y entradas_no_reproducibles. Sin LibreOffice."""
import copy, json, os, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable/trabajo_copia/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as FH
import verificacion_entradas as VE
from v63_xml import LibroV63
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
ELIS = os.path.join(E414, "elis_decisiones", "Elis"); VIDRALA = os.path.join(E414, "vidrala_decisiones", "Vidrala")
CAMBIO = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json")
TMP = tempfile.mkdtemp(prefix="rev_fable_c48_")
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]
CALC = json.load(open(CAMBIO, encoding="utf-8"))["analisis"]["C48"]["calculo"]

def calc(cal, **d):
    try:
        r = FH.calcular_entrada("C48", dict(d, calculo=cal), H, anios); return f"valor={r['valor']!r}"
    except Exception as ex:
        return f"{type(ex).__name__}: {str(ex)[:110]}"

print("=== 1 · calcular_entrada")
sin_red = copy.deepcopy(CALC); sin_red["redondeo"] = 12; print("media sin redondear (redondeo=12):", calc(sin_red))
for red in (0, -1, -2, None, "3", 2.5):
    c2 = copy.deepcopy(CALC); c2["redondeo"] = red; c2["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = 179.0   # 108,367 exacto
    print(f"  componente 2025 = 179,0 (media exacta 108,3667) con redondeo={red!r}:", calc(c2), "| con valor declarado 108:", calc(c2, valor=108))
c3 = copy.deepcopy(CALC); c3["anios"] = [2025, 2025, 2025]; print("años repetidos [2025, 2025, 2025]:", calc(c3))
c4 = copy.deepcopy(CALC); c4["anios"] = [2019, 2022, 2025]; print("años salteados [2019, 2022, 2025] (sin componente de 2019/2022):", calc(c4))
c5 = copy.deepcopy(CALC); c5["anios"] = ["2023", 2024.0, 2025]; print("años como texto y decimal:", calc(c5))
c6 = copy.deepcopy(CALC); c6["anios"] = [2023, None, 2025]; print("un año None:", calc(c6))
c7 = copy.deepcopy(CALC); c7["terminos"][0]["signo"] = True; print("signo True:", calc(c7))
c8 = copy.deepcopy(CALC); c8["componentes"]["pagos_arrendamientos_con_intereses"]["2025"].update(fuente="texto/NO_EXISTE.txt", pagina=99999, cita=None); print("componente con fuente inexistente, página 99999 y sin cita:", calc(c8))
c9 = copy.deepcopy(CALC); c9["componentes"]["pagos_arrendamientos_con_intereses"]["2025"]["valor"] = 1779.0; print("componente 2025 = 1779,0 (errata ×10), nada lo contrasta con la página:", calc(c9))
print("valor declarado True:", calc(CALC, valor=True), "| valor declarado '108':", calc(CALC, valor="108"))
c10 = copy.deepcopy(CALC); c10["anios"] = [2016, 2017, 2018]; c10["terminos"] = [{"partida": "intereses_financiacion", "signo": 1}, {"partida": "arrendamientos_principal", "signo": -1}]
print("media 2016–2018 de intereses_financiacion − arrendamientos_principal (los tres 0,0 de arrendamientos_principal están PENDIENTES de verificación):", calc(c10))
print("   pendientes de la Historia:", {k: p.get("pendientes_verificacion") for k, p in H.items() if p.get("pendientes_verificacion")}, "| pendientes_celda('C48'):", FH.pendientes_celda("C48", H, anios, 3))

print("\n=== 2 · construir + rellenar con un cálculo que usa ceros pendientes (H1)")
dF = os.path.join(TMP, "construir", "Elis"); os.makedirs(dF)
for n in ("fase1_metadatos.json", "fase1_partes", "fase1_fuentes.json", "texto", "etapa1"):
    o = os.path.join(ELIS, n); (shutil.copytree if os.path.isdir(o) else shutil.copy2)(o, os.path.join(dF, n))
m = json.load(open(os.path.join(dF, "fase1_metadatos.json"), encoding="utf-8"))
m.setdefault("analisis", {})["C48"] = {"calculo": c10}
json.dump(m, open(os.path.join(dF, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", dF], capture_output=True, text=True)
print("construir: rc", r.returncode, (r.stdout + r.stderr).strip()[-160:])
g = json.load(open(os.path.join(dF, "fase1_v63.json"), encoding="utf-8"))
print("   C48:", {k: v for k, v in g["analisis"]["C48"].items() if k in ("valor", "pendiente_verificacion", "periodo")}, "| C49:", {k: v for k, v in g["analisis"].get("C49", {}).items() if k in ("valor", "pendiente_verificacion")})
base = os.path.join(ELIS, "Elis_v63_base.xlsx"); vacio = os.path.join(TMP, "base_sin_migrados.xlsx")
lb = LibroV63(base); lb.escribir_celdas({f"Análisis!{c}": None for c in ("C46", "C47", "C48", "C49", "C50")}); lb.guardar(vacio)
REL = os.path.join(PV, "scripts", "rellenar_fase1_v63.py"); CFG = os.path.join(PV, "config_v2.json")
out = os.path.join(TMP, "h1.xlsx")
r = subprocess.run([sys.executable, "-B", REL, vacio, os.path.join(dF, "fase1_v63.json"), out, "--config", CFG], capture_output=True, text=True)
L = LibroV63(out) if os.path.exists(out) else None
print("rellenar: rc", r.returncode, "| C48 =", L and L.leer("Análisis", "C48"), "| Control maestro F45 =", L and L.leer("Control maestro", "F45"), "| J45 =", str(L and L.leer("Control maestro", "J45"))[:110])
reg = json.load(open(out + ".fase1.registro.json", encoding="utf-8")); print("   pendientes_verificacion del registro de rellenar:", reg.get("pendientes_verificacion"))

print("\n=== 3 · entradas_no_reproducibles: casos que no detecta")
def copia(src, nombre):
    d = os.path.join(TMP, nombre, os.path.basename(src))
    shutil.copytree(src, d, ignore=shutil.ignore_patterns(".lo_perfil", "variantes_v64", "recalc", "prompts_generados", "__pycache__", "historial_cierres", "antecedentes", "texto", "fuentes_pdf", "fase1_partes"))
    return d
e0 = copia(ELIS, "e0"); print("Elis 4.14 tal cual:", VE.entradas_no_reproducibles(e0, VE.universo(e0)))
e1 = copia(ELIS, "e1"); os.remove(os.path.join(e1, "fase1_v63.json")); print("(a) sin fase1_v63.json en la carpeta:", VE.entradas_no_reproducibles(e1, VE.universo(e1)))
e2 = copia(ELIS, "e2"); open(os.path.join(e2, "fase1_v63.json"), "w").write("{ roto"); print("(b) fase1_v63.json ilegible:", VE.entradas_no_reproducibles(e2, VE.universo(e2)))
e3 = copia(ELIS, "e3"); x = json.load(open(os.path.join(e3, "fase1_v63.json"), encoding="utf-8")); del x["analisis"]["C48"]; json.dump(x, open(os.path.join(e3, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(c) fase1_v63.json sin declarar C48 (el libro sigue con 108 migrado):", VE.entradas_no_reproducibles(e3, VE.universo(e3)))
e4 = copia(ELIS, "e4"); x = json.load(open(os.path.join(e4, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"]["valor"] = 108; json.dump(x, open(os.path.join(e4, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(d) fase1_v63.json editado a mano: C48.valor = 108 (sin cálculo, con la fuente de la media 82,933):", VE.entradas_no_reproducibles(e4, VE.universo(e4)), "| fuente que sigue declarando:", x["analisis"]["C48"]["fuente"][:90])
e5 = copia(ELIS, "e5"); x = json.load(open(os.path.join(e5, "fase1_v63.json"), encoding="utf-8")); x["analisis"]["C48"]["valor"] = "82.933"; json.dump(x, open(os.path.join(e5, "fase1_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("(e) valor declarado como texto «82.933»:", VE.entradas_no_reproducibles(e5, VE.universo(e5)))
v0 = copia(VIDRALA, "v0"); iv = VE.universo(v0); fv = json.load(open(os.path.join(v0, "fase1_v63.json"), encoding="utf-8"))
print("(f) Vidrala final 4.14 (dato real): libro C50 =", repr(iv["celdas"].get("Análisis!C50")), "| base C50 =", repr(LibroV63(os.path.join(VIDRALA, "Vidrala_v63_base.xlsx")).leer("Análisis", "C50")),
      "| fase1_v63.json declara C50:", "C50" in fv["analisis"], "| entradas_no_reproducibles:", VE.entradas_no_reproducibles(v0, iv))
outv = os.path.join(TMP, "vidrala_sin_migrados.xlsx"); bv = os.path.join(TMP, "vidrala_base_sin_migrados.xlsx")
lbv = LibroV63(os.path.join(VIDRALA, "Vidrala_v63_base.xlsx")); lbv.escribir_celdas({f"Análisis!{c}": None for c in ("C46", "C47", "C48", "C49", "C50")}); lbv.guardar(bv)
cfgv = os.path.join(PV, json.load(open(os.path.join(VIDRALA, "plantilla_activa.json"), encoding="utf-8"))["config"])
r = subprocess.run([sys.executable, "-B", REL, bv, os.path.join(VIDRALA, "fase1_v63.json"), outv, "--config", cfgv], capture_output=True, text=True)
Lv = LibroV63(outv) if os.path.exists(outv) else None
print("    Vidrala reconstruida sin los valores migrados del FCF base: rc", r.returncode, "→", {c: (Lv.leer("Análisis", c) if Lv else None) for c in ("C46", "C47", "C48", "C49", "C50")}, "| libro final:", {c: iv["celdas"].get(f"Análisis!{c}") for c in ("C46", "C47", "C48", "C49", "C50")})
outw = os.path.join(TMP, "vidrala_con_migrados.xlsx")
r = subprocess.run([sys.executable, "-B", REL, os.path.join(VIDRALA, "Vidrala_v63_base.xlsx"), os.path.join(VIDRALA, "fase1_v63.json"), outw, "--config", cfgv], capture_output=True, text=True)
rg = json.load(open(outw + ".fase1.registro.json", encoding="utf-8"))
print("    rellenar sobre la base de Vidrala (C50 = 0 migrado, sin declarar): rc", r.returncode, "| entradas_migradas_distintas:", rg.get("entradas_migradas_distintas"), "| avisos sobre C50:", [a for a in rg["avisos"] if "C50" in a], "| no_pisadas C50:", [x for x in rg["no_pisadas"] if x["celda"].endswith("C50")])
shutil.rmtree(TMP, ignore_errors=True)
