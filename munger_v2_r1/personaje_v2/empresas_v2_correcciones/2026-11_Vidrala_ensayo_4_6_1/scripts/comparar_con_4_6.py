#!/usr/bin/env python3
"""Comparación del expediente regenerado (4.6.1) con el aprobado de la 4.6 (encargo 4.6.1, §10). Solo lectura.

Uso: python3 -I comparar_con_4_6.py   (escribe resultados/comparacion_con_4_6.md y .json; código 1 si hay una diferencia no explicada)

Compara archivo a archivo las dos carpetas Vidrala/. Exige: P1, fuentes, datos, fases A, B y C, libros (de datos, evaluado y
recalculado), resultados, escalera y material provisional IDÉNTICOS byte a byte; el contraste entre motores y su descomposición,
repetidos sobre el libro 4.6.1, idénticos; y que las únicas diferencias sean las del cierre (auditoría nueva, registros de vigencia,
estado del pipeline, prompt de la auditoría y LÉEME).
"""
import hashlib
import json
import os
import sys

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
A, B = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6"), AQUI
EA, EB = os.path.join(A, "Vidrala"), os.path.join(B, "Vidrala")
EXCL = (".lo_perfil",)


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def lista(base):
    out = {}
    for r, ds, fs in os.walk(base):
        ds[:] = [d for d in ds if d not in EXCL]
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, base)] = sha(p)
    return out


la, lb = lista(EA), lista(EB)
iguales = sorted(k for k in la if lb.get(k) == la[k])
distintos = sorted(k for k in la if k in lb and lb[k] != la[k])
solo_a = sorted(k for k in la if k not in lb)
solo_b = sorted(k for k in lb if k not in la)
PERMITIDO_DISTINTO = {"estado_pipeline.json", "LEEME_ANTES_DE_CONTINUAR.md", "prompts_generados/13_verificacion.md", "auditoria.md"}
PERMITIDO_SOLO_A = {"auditoria.md"}
PERMITIDO_SOLO_B = {"auditoria_4_6_antecedente.md", "cierre_vigente.json"}
OBLIGATORIOS = ["fase1_decisiones.json", "fase1_v63.json", "datos_v63.json", "extracto_v63.md", "fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md",
                "fase_c.json", "fase_c.md", "Vidrala_v63_datos.xlsx", "Vidrala_v63_evaluada.xlsx", "recalc/Vidrala_v63_evaluada.xlsx", "resultados.json", "precio.json",
                "gramatica.json", "referencias_mecanicas.json", "datos_ausentes.json", "entrada_v63.json", "alcance_v2.json", "ficha_provisional.json",
                "informe_provisional.md", "material_auditoria.json"]
res = []


def c(n, ok, det=""):
    res.append({"control": n, "ok": bool(ok), "detalle": det})


for f in OBLIGATORIOS:
    c(f"{f} idéntico byte a byte", la.get(f) is not None and la.get(f) == lb.get(f), (lb.get(f) or "ausente")[:12])
c("fase1_partes/, texto/ y etapa1/ idénticos", all(lb.get(k) == v for k, v in la.items() if k.split("/")[0] in ("fase1_partes", "texto", "etapa1")))
hist = [k for k in solo_b if k.startswith("historial_cierres/")]
c("archivos distintos solo los del cierre (estado del pipeline, LÉEME, prompt de la auditoría, auditoría nueva)", set(distintos) <= PERMITIDO_DISTINTO, ", ".join(distintos))
c("archivos que faltan respecto a la 4.6: ninguno salvo los oficiales de la 4.6 archivados en historial_cierres/ y la auditoría 4.6 renombrada",
  set(solo_a) <= PERMITIDO_SOLO_A | {"ficha.json", "informe.md"}, ", ".join(solo_a) or "ninguno")
c("archivos nuevos solo de vigencia y cierre (historial_cierres/, cierre_vigente.json, auditoría 4.6 como antecedente)", all(k in PERMITIDO_SOLO_B or k.startswith("historial_cierres/") for k in solo_b), ", ".join(k for k in solo_b if k not in PERMITIDO_SOLO_B and not k.startswith("historial_cierres/")) or "ninguno")
c("la auditoría 4.6 se conserva sin cambios como antecedente", sha(os.path.join(EB, "auditoria_4_6_antecedente.md")) == la.get("auditoria.md"))
c("el cierre 4.6 se conserva archivado sin cambios (ficha.json e informe.md idénticos a los de la 4.6)",
  any(k.endswith("/ficha.json") and lb[k] == la.get("ficha.json") for k in hist) and any(k.endswith("/informe.md") and lb[k] == la.get("informe.md") for k in hist))
if os.path.exists(os.path.join(EB, "ficha.json")):
    fa, fb = json.load(open(os.path.join(EA, "ficha.json"), encoding="utf-8")), json.load(open(os.path.join(EB, "ficha.json"), encoding="utf-8"))
    c("ficha oficial 4.6.1 igual a la 4.6 en todo (valores, estado, cubo, decisión, marcas, alcance); el cierre nombra el material aprobado", {k: v for k, v in fa.items() if k != "cierre"} == {k: v for k, v in fb.items() if k != "cierre"},
      f"cierre 4.6 {fa.get('cierre')} · 4.6.1 {fb.get('cierre')}")
ca = json.load(open(os.path.join(A, "contraste_motores", "contraste_resultados.json"), encoding="utf-8"))
cb = json.load(open(os.path.join(B, "contraste_motores", "contraste_resultados.json"), encoding="utf-8"))
campos = ("motor", "f", "r_operativa_C15", "pasivos_netos_B_C16", "valor_por_accion", "valor_final", "peso_terminal", "ponderado", "precio_si", "precio_escenario_malo", "zona")
c("contraste entre motores repetido sobre el libro 4.6.1: mismos valores (B0, A1, A2, A2a, A2b)", all(x.get(k) == y.get(k) for x, y in zip(ca["variantes"], cb["variantes"]) for k in campos) and len(cb["variantes"]) == 5)
c("descomposición del contraste idéntica", json.load(open(os.path.join(A, "contraste_motores", "descomposicion.json"))) == json.load(open(os.path.join(B, "contraste_motores", "descomposicion.json"))))
n = sum(x["ok"] for x in res)
L = ["# Comparación · expediente 4.6.1 frente al aprobado de la 4.6", "", "Generado por `scripts/comparar_con_4_6.py`.", "", "| Control | Resultado | Detalle |", "|---|---|---|"]
L += [f"| {x['control']} | {'CUMPLE' if x['ok'] else 'NO CUMPLE'} | {x['detalle']} |" for x in res]
L += ["", f"Archivos idénticos: {len(iguales)} · distintos: {len(distintos)} · solo en la 4.6: {len(solo_a)} · solo en la 4.6.1: {len(solo_b)}.", "", f"RESULTADO: {n} de {len(res)} controles cumplen."]
os.makedirs(os.path.join(B, "resultados"), exist_ok=True)
open(os.path.join(B, "resultados", "comparacion_con_4_6.md"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(res, open(os.path.join(B, "resultados", "comparacion_con_4_6.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(L))
sys.exit(0 if n == len(res) else 1)
