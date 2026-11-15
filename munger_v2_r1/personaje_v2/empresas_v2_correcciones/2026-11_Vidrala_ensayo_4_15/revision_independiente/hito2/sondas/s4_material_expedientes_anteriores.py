#!/usr/bin/env python3
"""s4 · I20: ¿añadir entrada_efectiva.json a cierre_v2.MATERIAL_FIJO cambia el identificador del material de algún expediente del árbol?
Para cada carpeta con material_auditoria.json: id fijado, id calculado con el código del hito 2 y con el del hito 1 (solo lectura).
Uso: python3 -I -B s4_material_expedientes_anteriores.py"""
import importlib.util, json, os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PV2 = os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")
PV1 = os.path.join(F, "copia_hito1", "munger_v2_r1", "personaje_v2")
sys.dont_write_bytecode = True


def cargar(pv, nombre):
    sys.path.insert(0, os.path.join(pv, "scripts"))
    try:
        spec = importlib.util.spec_from_file_location(nombre, os.path.join(pv, "scripts", "cierre_v2.py"))
        m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(m)
        return m
    finally:
        sys.path.pop(0)


C2, C1 = cargar(PV2, "cierre_h2"), cargar(PV1, "cierre_h1")
print("MATERIAL_FIJO hito 2 − hito 1:", sorted(set(C2.MATERIAL_FIJO) - set(C1.MATERIAL_FIJO)), "· hito 1 − hito 2:", sorted(set(C1.MATERIAL_FIJO) - set(C2.MATERIAL_FIJO)))
n = dist = vig = con_ee = 0
raiz = os.path.dirname(PV2)
for d, _dirs, files in sorted(os.walk(raiz)):
    if "material_auditoria.json" not in files:
        continue
    n += 1
    try:
        fij = json.load(open(os.path.join(d, "material_auditoria.json"), encoding="utf-8")).get("id")
    except Exception as ex:  # noqa: BLE001
        fij = f"ilegible ({type(ex).__name__})"
    e = os.path.basename(d)
    i2, i1 = C2.material(d)[0], C1.material(d)[0]
    con_ee += "entrada_efectiva.json" in files
    vig += i2 == fij
    if i1 != i2:
        dist += 1
        print("   DISTINTO:", os.path.relpath(d, raiz), fij, i1, i2)
print(f"carpetas con material fijado: {n} · con entrada_efectiva.json: {con_ee} · id hito 1 ≠ id hito 2: {dist} · material vigente = fijado (hito 2): {vig}")
