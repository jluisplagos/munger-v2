"""Cuarta pasada (sonda q4c de la tercera; solo cambia el árbol: el caso real de T1).
Texto original: Tercera pasada · T1 en un registro REAL: Viscofan 4.14, fila 10 de la Historia (tipo impositivo efectivo = impuesto / BAI, con 4
decimales en el libro y sin round declarado). Vínculo SIMULADO en una copia temporal, como diagnostico_registros_4_14.py. Solo lectura
del árbol. Con el código de la segunda pasada (PV=<copia de arbol_congelado>/personaje_v2) L10 era una discrepancia."""
import json, os, shutil, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
REG_PV = os.environ.get("REG_PV", "/tmp/rev_fable4/congelado4/personaje_v2")  # de dónde se toma el expediente (el del árbol de la tercera pasada)
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE  # noqa: E402
exp = os.path.join(REG_PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "viscofan_decisiones", "Viscofan")
tmp = tempfile.mkdtemp(prefix="rev_fable_l10_"); dst = os.path.join(tmp, "Viscofan")
shutil.copytree(exp, dst, ignore=shutil.ignore_patterns("recalc", "variantes_v64", "prompts_generados", ".lo_perfil", "historial_cierres", "antecedentes"))
reg = json.load(open(os.path.join(dst, VE.REGISTRO), encoding="utf-8")); reg["formato"] = "4.15"
hs = VE.huellas_registro(dst, reg)
for e in reg["entradas"]:
    c = e.setdefault("comprobacion", {}) or {}
    e["comprobacion"] = c; c["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": c.get("revisor"), "fecha": c.get("fecha")}
json.dump(reg, open(os.path.join(dst, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False)
r = VE.comprobar(dst)
print("código:", PV)
print("Viscofan (vínculo simulado): cálculo", r["comprobadas_calculo"], "de", r["universo_calculo"], "· discrepancias", len(r["discrepancias"]), "· errores", len(r["errores"]))
por = {e["celda"]: e for e in reg["entradas"]}
for k in [f"Historia!{c}10" for c in "CDEFGHIJKL"]:
    e = por[k]; d = e.get("derivacion") or {}
    vals = {o: por[o]["valor_modelo"] for o in d.get("origenes") or []}
    rr = VE._eval_formula(d["formula"], vals)
    est = "comprobada" if k in r["comprobadas"] else "discrepancia" if any(x.startswith(k + ":") for x in r["discrepancias"]) else "otro"
    print(f"   {k}: modelo {e['valor_modelo']!r} · fórmula {rr!r} · |dif| {abs(rr - e['valor_modelo']):.3g} · 1e-9 × mayor origen {1e-9 * max(abs(x) for x in vals.values()):.3g} → {est}")
shutil.rmtree(tmp, ignore_errors=True)
