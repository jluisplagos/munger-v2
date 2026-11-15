#!/usr/bin/env python3
"""Comparación numérica del ensayo regenerado (4.6) con el de la entrega 4.5 (encargo 4.6, §9). Solo lectura.

Uso: python3 -I comparar_con_4_5.py   (escribe resultados/comparacion_con_4_5.md y su .json; código 1 si hay una diferencia no explicada)

Comprueba que la reparación del cierre no altera: P1 y sus fuentes, entradas y palancas, probabilidades y r, valores por escenario,
ponderado y escalera, el contraste entre motores y su descomposición, ni la caja y el dividendo. Las únicas diferencias admitidas
son las de formato y presentación previstas por la reparación (etiqueta de C104, material provisional, marca, alcance).
"""
import hashlib
import json
import os
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
A = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_5")
B = AQUI
EA, EB = os.path.join(A, "Vidrala"), os.path.join(B, "Vidrala")
import openpyxl  # noqa: E402

out, lin = [], ["# Comparación numérica · ensayo 4.6 frente a 4.5", "", "Generado por `scripts/comparar_con_4_5.py`. «Igual» significa idéntico (huella o valor exacto) salvo donde se indica.", "",
                "| Control | Resultado | Detalle |", "|---|---|---|"]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def j(p):
    return json.load(open(p, encoding="utf-8"))


def c(nombre, ok, det=""):
    out.append({"control": nombre, "ok": bool(ok), "detalle": det})
    lin.append(f"| {nombre} | {'IGUAL / CUMPLE' if ok else 'DIFIERE'} | {det} |")


# 1. P1, fuentes y entradas
for f in ("fase1_decisiones.json", "fase1_v63.json", "fase1_fuentes.json", "fase1_metadatos.json", "datos_v63.json", "Vidrala_v63_datos.xlsx", "Vidrala_v63_base.xlsx"):
    c(f"{f} (P1, fuentes y entradas)", sha(os.path.join(EA, f)) == sha(os.path.join(EB, f)), sha(os.path.join(EB, f))[:12] + "…")
for d in ("fase1_partes", "texto", "etapa1"):
    fs = sorted(os.listdir(os.path.join(EA, d)))
    c(f"{d}/ ({len(fs)} archivos)", all(sha(os.path.join(EA, d, x)) == sha(os.path.join(EB, d, x)) for x in fs if os.path.isfile(os.path.join(EA, d, x))))
# 2. fases
for f in ("extracto_v63.md", "fase_a.json", "fase_a.md", "fase_b.json", "fase_b.md", "referencias_mecanicas.json", "datos_ausentes.json"):
    c(f"{f} (no se vuelven a ejecutar las fases A y B)", sha(os.path.join(EA, f)) == sha(os.path.join(EB, f)))


def hojas(x, r=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from hojas(v, f"{r}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from hojas(v, f"{r}[{i}]")
    else:
        yield r, x


fa, fb = dict(hojas(j(os.path.join(EA, "fase_c.json")))), dict(hojas(j(os.path.join(EB, "fase_c.json"))))
dif = sorted(k for k in set(fa) | set(fb) if fa.get(k) != fb.get(k))
c("fase_c.json: única diferencia la etiqueta «fundamento …» de C104 (formato armonizado; juicios y números iguales)", dif == [".celdas.C104"],
  f"{dif} · antes «…{fa.get('.celdas.C104', '')[150:260]}…» · después «…{fb.get('.celdas.C104', '')[150:290]}…»")
ma, mb = open(os.path.join(EA, "fase_c.md"), encoding="utf-8").read().splitlines(), open(os.path.join(EB, "fase_c.md"), encoding="utf-8").read().splitlines()
dl = [i for i, (x, y) in enumerate(zip(ma, mb), 1) if x != y]
c("fase_c.md: solo cambian las líneas que citan la etiqueta de C104 (la de C104 y la que explica su etiqueta)", len(ma) == len(mb) and len(dl) == 2 and all("fundamento no procede" in mb[i - 1] for i in dl), f"líneas {dl}")
# 3. libro evaluado (fórmulas y entradas) y recalculado (valores)
for nombre, ruta, data_only in (("libro evaluado (celdas escritas y fórmulas)", "Vidrala_v63_evaluada.xlsx", False), ("libro evaluado recalculado (valores)", os.path.join("recalc", "Vidrala_v63_evaluada.xlsx"), True)):
    wa, wb = openpyxl.load_workbook(os.path.join(EA, ruta), data_only=data_only), openpyxl.load_workbook(os.path.join(EB, ruta), data_only=data_only)
    difs = []
    for s in wa.sheetnames:
        for row in wa[s].iter_rows():
            for cel in row:
                x, y = cel.value, wb[s][cel.coordinate].value
                if x != y and not (isinstance(x, float) and isinstance(y, float) and abs(x - y) < 1e-9):
                    difs.append(f"{s}!{cel.coordinate}")
    c(f"{nombre}: única celda distinta Análisis!C104", difs == ["Análisis!C104"], ", ".join(difs[:6]))
# 4. resultados, escalera, caja y dividendo
ra, rb = j(os.path.join(EA, "resultados.json")), j(os.path.join(EB, "resultados.json"))
ra.pop("origen", None), rb.pop("origen", None)
cja, cjb = ra.pop("celdas_juicio_analisis", {}), rb.pop("celdas_juicio_analisis", {})
c("resultados.json (salvo la ruta de origen): valores, estados, palancas, probabilidades, r_op, puente, V0, m0, t, f", ra == rb, ", ".join(k for k in ra if ra.get(k) != rb.get(k)) or "iguales")
c("resultados.json → celdas_juicio_analisis: única diferencia C104", sorted(k for k in set(cja) | set(cjb) if cja.get(k) != cjb.get(k)) == ["C104"])
pa, pb = j(os.path.join(EA, "precio.json")), j(os.path.join(EB, "precio.json"))
c("precio.json: V por escenario, ponderado, precio de Sí, MALO, zona, DCF inverso", pa == pb, f"ponderado {pb['ponderado']:.4f} · precio de Sí {pb['precio_si']:.4f} · zona {pb['zona']}")
c("r = 0,09 y probabilidades 0,2 / 0,6 / 0,2", rb["valores"]["C56"] == 0.09 and rb["probabilidades"] == [0.2, 0.6, 0.2])
c("caja 108,352 sin restar el dividendo; puente 160,784", rb["anclas_historia"]["caja_ultimo"] == 108.352 and abs(rb["pasivos_netos_B_C16"] - 160.784) < 1e-9)
# 5. contraste y descomposición
ca, cb = j(os.path.join(A, "contraste_motores", "contraste_resultados.json")), j(os.path.join(B, "contraste_motores", "contraste_resultados.json"))
campos = ("motor", "f", "r_operativa_C15", "pasivos_netos_B_C16", "valor_por_accion", "valor_final", "peso_terminal", "ponderado", "precio_si", "precio_escenario_malo", "zona")
dc = [(v1["variante"], k) for v1, v2 in zip(ca["variantes"], cb["variantes"]) for k in campos if v1.get(k) != v2.get(k)]
c("contraste entre motores (B0, A1, A2, A2a, A2b) sobre el libro 4.6: mismos valores que en la 4.5", not dc and [v["variante"] for v in cb["variantes"]] == ["B0", "A1", "A2", "A2a", "A2b"], str(dc[:5]))
da, db = j(os.path.join(A, "contraste_motores", "descomposicion.json")), j(os.path.join(B, "contraste_motores", "descomposicion.json"))
c("descomposición del contraste: idéntica", da == db)
# 6. cambios de presentación previstos
fi = j(os.path.join(EB, "ficha.json")) if os.path.exists(os.path.join(EB, "ficha.json")) else j(os.path.join(EB, "ficha_provisional.json"))
f45 = j(os.path.join(EA, "ficha.json"))
num = ("escalera", "valor_ponderado", "precio", "escenarios", "peso_terminal", "salto_anio_11", "motor", "estado_analisis", "cubo", "decision", "fundamento_material")
c("ficha: mismos valores, estado, cubo, decisión y fundamento que en la 4.5", all(fi.get(k) == f45.get(k) for k in num), ", ".join(k for k in num if fi.get(k) != f45.get(k)) or "iguales")
nuevos = sorted(k for k in fi if k not in f45)
c("ficha: campos nuevos solo los de la reparación (datos_etapa1_incompletos, alcance y cierre o provisional)", set(nuevos) <= {"datos_etapa1_incompletos", "alcance", "cierre", "provisional"}, ", ".join(nuevos))
n_ok = sum(x["ok"] for x in out)
lin += ["", f"RESULTADO: {n_ok} de {len(out)} controles iguales o cumplidos."]
os.makedirs(os.path.join(B, "resultados"), exist_ok=True)
open(os.path.join(B, "resultados", "comparacion_con_4_5.md"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
json.dump(out, open(os.path.join(B, "resultados", "comparacion_con_4_5.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(lin))
sys.exit(0 if n_ok == len(out) else 1)
