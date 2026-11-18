#!/usr/bin/env python3
"""jumbo_e · Análisis!C42 (EV/EBITDA) recalculado con el precio activo del expediente (27,28 €, C37), no con el de la etapa 1 (24,72 €).
Encargo del coordinador del 18-nov-2026 (noche), tras la revisión independiente del registro de Jumbo (REVISION.md, punto 3, @ 57e417a).
Misma fórmula que la etapa 1 (comprobada: (24,72 × 134,365561 + 62,247 − 546,140) ÷ 440,24 = 6,4458), con cifras exactas en euros (precedente E1):
  EV = 27,28 × 134,365561 + 62,247015 (pasivos por arrendamiento, 30-jun-2026, H1 2026 PDF p. 57) − 546,140091 (caja, H1 2026 PDF p. 25)
  EBITDA LTM = 435,659964 (2025, AR2025 PDF p. 148) + 169,927311 (H1 2026) − 165,352664 (H1 2025) (H1 2026 PDF p. 23)
Hace lo que cambiar_base.py hace con una entrada `analisis` (vaciar_en_etapa1 + evidencia + entrada declarada en fase1_metadatos.json), sobre el
expediente ya preparado: guarda antes la copia de ensayo de la etapa 1 y los textos anteriores en antecedentes/.
Uso: python3 -I recalcular_C42.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import hashlib, json, os, shutil, sys
C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
from v63_xml import LibroV63  # noqa: E402
import cambiar_base as CB  # noqa: E402
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
precio, acciones, arr, caja = 27.28, 134.365561, 62.247015, 546.140091
ebitda = 435.659964 + 169.927311 - 165.352664
ev = precio * acciones + arr - caja
valor = ev / ebitda
meta_p = os.path.join(C, "fase1_metadatos.json")
meta = json.load(open(meta_p, encoding="utf-8"))
assert meta["precio"]["valor"] == precio and abs(meta["acciones_diluidas"]["valor"] - acciones) < 1e-12
e1 = os.path.join(C, "etapa1", "Jumbo_evaluada.xlsx")
dst = os.path.join(ANT, "etapa1_antes_de_C42")
os.makedirs(dst)
shutil.copy2(e1, os.path.join(dst, "Jumbo_evaluada.xlsx"))
lb = LibroV63(e1)
antes = {"Análisis!C42": lb.leer("Análisis", "C42")}
assert abs(float(antes["Análisis!C42"]) - 6.4458) < 5e-4, antes
lb.escribir("Análisis", "C42", None)
lb.marcar_modificada("Análisis")
r = CB.fila_de(lb, "Control maestro", "Análisis!C42")
ev_txt = {"L": "H1 2026 PDF p. 23, p. 25, p. 57; AR2025 PDF p. 148",
          "M": (f"C42 = EV ÷ EBITDA LTM = (27,28 × 134,365561 + 62,247015 − 546,140091) ÷ (435,659964 + 169,927311 − 165,352664) = {ev:.6f} ÷ {ebitda:.6f} = {valor:.6f}. "
                "Misma fórmula que la etapa 1 (6,4458 con 24,72 €), con el precio activo del expediente (C37 = 27,28 €, 17-nov-2026) y las acciones de P-O2 (a)."),
          "N": ("[Clase: derivado de datos publicados] Recalculado en jumbo_e (revisión del registro de Jumbo, punto 3): el valor de la etapa 1 y sus sensibilidades "
                "se calcularon con 24,72 € y ya no corresponden al precio del expediente. Con las cifras redondeadas de la etapa 1 (440,24) sale 7,2270.")}
for col, txt in ev_txt.items():
    antes[f"Control maestro!{col}{r}"] = lb.leer("Control maestro", f"{col}{r}")
    lb.escribir("Control maestro", f"{col}{r}", txt, tipo="texto")
lb.marcar_modificada("Control maestro")
lb.guardar(e1)
json.dump({"valores_y_textos_anteriores": antes}, open(os.path.join(dst, "evidencia_anterior.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
shutil.copy2(meta_p, os.path.join(dst, "fase1_metadatos.json"))
meta.setdefault("analisis", {})["C42"] = {"valor": valor, "fuente": ev_txt["M"], "pagina": ev_txt["L"], "periodo": "EV con precio del 17-nov-2026 y balance a 30-jun-2026; EBITDA LTM a 30-jun-2026", "unidad": "x"}
json.dump(meta, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": "2026-11-18", "celda": "Análisis!C42", "antes": antes["Análisis!C42"], "despues": valor, "ev": ev, "ebitda_ltm": ebitda, "fila_control_maestro": r,
           "etapa1_antes_sha256": h(os.path.join(dst, "Jumbo_evaluada.xlsx")), "etapa1_despues_sha256": h(e1), "guion": os.path.abspath(__file__),
           "motivo": "cifra de juicio desfasada respecto al precio activo (vigencia; revisión del registro de Jumbo, punto 3)"}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("C42", antes["Análisis!C42"], "→", valor, "· fila CM", r)
