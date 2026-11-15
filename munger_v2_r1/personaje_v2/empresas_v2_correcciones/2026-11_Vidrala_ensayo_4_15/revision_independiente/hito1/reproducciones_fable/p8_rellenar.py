"""Sondas de rellenar_fase1_v63.py (sin LibreOffice): rama H1 pendiente y celdas de juicio migradas distintas de las declaradas."""
import copy, json, os, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable/trabajo_copia/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE
from v63_xml import LibroV63
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
REL = os.path.join(PV, "scripts", "rellenar_fase1_v63.py")
TMP = tempfile.mkdtemp(prefix="rev_fable_rell_")
print("=== celdas de datos de Análisis: libro final frente a lo que declara fase1_v63.json (4.14 finales y sus orígenes)")
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis", "elis_motor_A/Elis", "viscofan/Viscofan", "vidrala/Vidrala"):
    d = os.path.join(E414, exp)
    if not os.path.isdir(d):
        continue
    f1 = json.load(open(os.path.join(d, "fase1_v63.json"), encoding="utf-8")); L = LibroV63(VE.libro_de(d))
    dif = []
    for c in ("C24", "C26", "C28", "C31", "C32", "C33", "C34", "C38", "C40", "C42", "C46", "C47", "C48", "C49", "C50", "C53", "C54", "C57", "C60", "C88", "C96"):
        x = (f1.get("analisis") or {}).get(c, "—"); v = x.get("valor") if isinstance(x, dict) else x
        if c == "C57":
            t = f1.get("tasa_sin_riesgo"); v = t.get("valor") if isinstance(t, dict) else t
        b = L.leer("Análisis", c)
        if v == "—":
            if b not in (None, ""):
                dif.append(f"{c}: libro {b!r} · sin declarar")
        elif not ((isinstance(v, (int, float)) and isinstance(b, (int, float)) and abs(v - b) <= 1e-9 * max(1, abs(v))) or v == b):
            dif.append(f"{c}: libro {b!r} · declarado {v!r}")
    print(f"  {exp}: " + ("; ".join(dif) or "todas las declaradas coinciden con el libro"))

print("\n=== rama H1: valor migrado ≠ declarado con un cero pendiente en la ventana")
ELIS = os.path.join(E414, "elis_decisiones", "Elis")
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
g = copy.deepcopy(f1); g["anios_fcf_base"] = 10
vals = g["historia"]["partidas"]["arrendamientos_principal"]["valores"]; g["analisis"]["C49"] = dict(g["analisis"]["C49"], valor=round(sum(vals) / 10, 3))
p = os.path.join(TMP, "f1_h1.json"); json.dump(g, open(p, "w", encoding="utf-8"), ensure_ascii=False)
out = os.path.join(TMP, "h1.xlsx")
r = subprocess.run([sys.executable, "-B", REL, os.path.join(ELIS, "Elis_v63_base.xlsx"), p, out, "--config", os.path.join(PV, "config_v2.json")], capture_output=True, text=True)
rg = json.load(open(out + ".fase1.registro.json", encoding="utf-8"))
Lo = LibroV63(out) if os.path.exists(out) else None
print("  rellenar rc", r.returncode, "| C49 del libro:", Lo and Lo.leer("Análisis", "C49"), "| declarado:", g["analisis"]["C49"]["valor"], "| entradas_migradas_distintas:", [x["celda"] for x in rg.get("entradas_migradas_distintas") or []])
print("  avisos de C49:", [a[:160] for a in rg["avisos"] if "C49" in a], "| Control maestro N46:", str(Lo and Lo.leer("Control maestro", "N46"))[-150:])
shutil.rmtree(TMP, ignore_errors=True)
