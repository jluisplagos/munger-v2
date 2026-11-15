#!/usr/bin/env python3
"""Aislamiento de los cambios de precisión y de juicio de entrada del piloto 4.11 (encargo §9): C46/C47 y C48/C49 (P3).

El caso principal del ensayo conserva C46 = 335,4 y C47 = 169,7 (precisión de referencia), C48 = 0 y C49 = 4,5 (supuesto heredado,
P3 abierto). fase1_historia.py construye 335,413, 169,668, 0 y 6,764 (este último es el PAGO TOTAL de arrendamientos de la nota 8
denominado «principal»). Este script NO cambia el expediente: escribe COPIAS del libro evaluado final del piloto con esas entradas,
las recalcula (LibreOffice, en secuencia, perfil propio), las lee con leer_resultados.py y precio_de_si.py y atribuye el efecto de
cada cambio por separado y combinado, con la configuración económica del expediente (que las copias conservan).

Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/aislar_entradas_4_11.py [CARPETA_EXPEDIENTE] [--salida NOMBRE]
Escribe …/2026-11_Vidrala_ensayo_4_11/resultados/NOMBRE.json y .md (por omisión aislamiento_entradas_4_11; fuera del expediente: no toca el
material auditado). Las copias recalculadas van a un temporal; el resultado registra la huella de cada copia.
Código 0 si todas las variantes se calcularon y la de control reproduce el precio.json del expediente; 1 si no.
"""
import hashlib
import json
import os
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
sys.path.insert(0, os.path.join(PV, "scripts"))
from v63_xml import LibroV63  # noqa: E402

ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
NOMBRE = sys.argv[sys.argv.index("--salida") + 1] if "--salida" in sys.argv else "aislamiento_entradas_4_11"
if "--salida" in sys.argv:
    ARGS.remove(NOMBRE)
CARP = os.path.abspath(ARGS[0]) if ARGS else os.path.join(ENS, "piloto", "Vidrala")
SALIDA = os.path.join(ENS, "resultados")
TRABAJO = os.path.join(tempfile.mkdtemp(prefix="aislamiento_4_11_"), NOMBRE)  # copias en un temporal: el resultado registra sus huellas


def leer_fcf_base(libro):
    """FCF base (Análisis!C52 = C46 − C47 − C48 − C49 con sus ajustes) del libro recalculado: muestra que la copia cambió la entrada."""
    from openpyxl import load_workbook
    v = load_workbook(libro, data_only=True, read_only=True)["Análisis"]["C52"].value
    return v if isinstance(v, (int, float)) else None


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    return r.returncode, r.stdout + r.stderr


def main():
    reg = json.load(open(os.path.join(os.path.dirname(CARP), "resultados", "cambio_de_base.json"), encoding="utf-8"))["sustituidas_en_fase1_v63"]
    construido = {c: reg[c]["construido_por_fase1_historia"] for c in ("C46", "C47", "C48", "C49")}
    principal = {c: reg[c]["valor"] for c in ("C46", "C47", "C48", "C49")}
    variantes = [
        ("control", "caso principal del ensayo (sin cambios; debe reproducir precio.json)", {}),
        ("C46_C47_precisos", f"C46 {construido['C46']} y C47 {construido['C47']} (los que construye fase1_historia.py; precisión, no juicio)",
         {"Análisis!C46": construido["C46"], "Análisis!C47": construido["C47"]}),
        ("C49_pago_total", f"C49 {construido['C49']} (pago total de arrendamientos P+I de la nota 8, en lugar del supuesto heredado 4,5; P3)",
         {"Análisis!C49": construido["C49"]}),
        ("combinada", "las dos a la vez", {"Análisis!C46": construido["C46"], "Análisis!C47": construido["C47"], "Análisis!C49": construido["C49"]}),
    ]
    if construido["C48"] != principal["C48"]:
        variantes.insert(3, ("C48_construido", f"C48 {construido['C48']}", {"Análisis!C48": construido["C48"]}))
    nombre = os.path.basename(CARP)
    libro = os.path.join(CARP, f"{nombre}_v63_evaluada.xlsx")
    pa = json.load(open(os.path.join(CARP, "plantilla_activa.json"), encoding="utf-8"))
    sys.path.insert(0, os.path.join(RAIZ, "v6", "v64_experimental", "scripts") if "V6.4" in pa["version"] else os.path.join(RAIZ, "v6", "scripts"))
    import inventario_entradas  # noqa: E402  (el de la plantilla del expediente)
    permitidas = {"Análisis": inventario_entradas.conjunto_entradas()["Análisis"]}
    os.makedirs(os.path.join(TRABAJO, "recalc"), exist_ok=True)
    perfil = os.path.join(TRABAJO, "perfil_lo")
    precio_exp = json.load(open(os.path.join(CARP, "precio.json"), encoding="utf-8"))
    filas, ok = [], True
    for clave, desc, celdas in variantes:
        copia = os.path.join(TRABAJO, f"{clave}.xlsx")
        lb = LibroV63(libro)
        if celdas:
            lb.escribir_celdas(celdas, permitidas)
        lb.borrar_caches()
        lb.guardar(copia)
        rc, out = run(["bash", os.path.join(PV, "scripts", "recalc.sh"), copia, os.path.join(TRABAJO, "recalc"), perfil])
        rec = os.path.join(TRABAJO, "recalc", f"{clave}.xlsx")
        rj, pj = os.path.join(TRABAJO, f"{clave}.resultados.json"), os.path.join(TRABAJO, f"{clave}.precio.json")
        if rc != 0 or not os.path.exists(rec):
            filas.append({"clave": clave, "descripcion": desc, "fallo": "recálculo: " + out[-300:]})
            ok = False
            continue
        rc1, o1 = run([sys.executable, os.path.join(PV, "scripts", "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"])
        rc2, o2 = run([sys.executable, os.path.join(PV, "scripts", "precio_de_si.py"), rj, pj, "--copia", "--k", str(precio_exp.get("k", 3))])
        if rc1 != 0 or not os.path.exists(pj):
            filas.append({"clave": clave, "descripcion": desc, "fallo": (o1 + o2)[-300:]})
            ok = False
            continue
        res, pr = json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))
        filas.append({"clave": clave, "descripcion": desc, "celdas": celdas, "V": [res["valores"].get(x) for x in ("B78", "C78", "D78")],
                      "ponderado": res["valores"].get("C83"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona"),
                      "fcf_base_C52": leer_fcf_base(rec), "estado_tecnico": res["estados"].get("estado_tecnico_B255"),
                      "configuracion_valida": (res.get("configuracion_v64") or {}).get("valida"), "hash_copia": hashlib.sha256(open(copia, "rb").read()).hexdigest()})
        print(f"{clave:20s} ponderado {filas[-1]['ponderado']} · Sí {filas[-1]['precio_si']} · zona {filas[-1]['zona']}", flush=True)
    ctrl = next((f for f in filas if f["clave"] == "control" and "fallo" not in f), None)
    if ctrl is None or abs(ctrl["ponderado"] - precio_exp["ponderado"]) > 1e-9 or abs(ctrl["precio_si"] - precio_exp["precio_si"]) > 1e-9:
        ok = False
    for f in filas:
        if "fallo" not in f and ctrl:
            f["delta_ponderado"] = f["ponderado"] - ctrl["ponderado"]
            f["delta_precio_si"] = f["precio_si"] - ctrl["precio_si"]
    out = {"expediente": os.path.relpath(CARP, RAIZ), "libro": os.path.basename(libro), "libro_sha256": hashlib.sha256(open(libro, "rb").read()).hexdigest(),
           "configuracion_economica_sha256": hashlib.sha256(open(os.path.join(CARP, "configuracion_economica.json"), "rb").read()).hexdigest()
           if os.path.exists(os.path.join(CARP, "configuracion_economica.json")) else None,
           "precio_del_expediente": {k: precio_exp.get(k) for k in ("precio", "ponderado", "precio_si", "zona")}, "caso_principal": principal,
           "construido_por_fase1_historia": construido, "variantes": filas, "control_reproduce_el_expediente": bool(ok and ctrl),
           "nota": ("Aislamiento mecánico (encargo 4.11 §9). C46/C47 es un cambio de PRECISIÓN; C49 = 6,764 es una alternativa de JUICIO (P3, abierto): "
                    "ninguna se adopta y los ceros pendientes siguen pendientes.")}
    os.makedirs(SALIDA, exist_ok=True)
    json.dump(out, open(os.path.join(SALIDA, NOMBRE + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    f6 = lambda x: f"{x:.6f}" if isinstance(x, (int, float)) else "—"  # noqa: E731
    md = [f"# Aislamiento de C46/C47 (precisión) y C49 (P3) · `{out['expediente']}`", "",
          f"Expediente `{out['expediente']}` · libro evaluado final (SHA-256 `{out['libro_sha256'][:16]}…`), copias recalculadas con la configuración del expediente. "
          "El expediente no se modifica.", "",
          "| Variante | Qué cambia | Ponderado | Δ | Precio de Sí | Δ | Zona | FCF base (C52) |", "|---|---|---|---|---|---|---|---|"]
    for f in filas:
        if "fallo" in f:
            md.append(f"| {f['clave']} | {f['descripcion']} | FALLO: {f['fallo'][:80]} | | | | | |")
        else:
            md.append(f"| {f['clave']} | {f['descripcion']} | {f6(f['ponderado'])} | {f6(f.get('delta_ponderado'))} | {f6(f['precio_si'])} | {f6(f.get('delta_precio_si'))} | {f['zona']} | {f6(f['fcf_base_C52'])} |")
    md += ["", f"Control: {'reproduce' if out['control_reproduce_el_expediente'] else 'NO reproduce'} el precio.json del expediente "
           f"(ponderado {f6(precio_exp.get('ponderado'))}, precio de Sí {f6(precio_exp.get('precio_si'))}, zona {precio_exp.get('zona')}).", "",
           "**Lectura.** " + out["nota"] + " Con el motor B, el FCF base (C52) no entra en el valor: lo usan los diagnósticos y la referencia del motor A."]
    open(os.path.join(SALIDA, NOMBRE + ".md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
