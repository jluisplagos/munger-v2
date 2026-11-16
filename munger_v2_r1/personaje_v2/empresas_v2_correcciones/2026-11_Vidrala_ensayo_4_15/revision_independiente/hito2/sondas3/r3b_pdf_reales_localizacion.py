#!/usr/bin/env python3
"""r3b · N3 (tercera pasada), con los PDF reales: ¿en cuántas entradas reales la lectura nueva en el documento llega a hacerse? Para cada
entrada de Elis, Viscofan y Vidrala con PDF en el árbol: el estado de _cita_cifra(cita, valor_fuente, texto del PDF) con «pdftotext -layout»
y sin layout. Si en los dos es «no_localizada» (la cita está en el PDF sin espacios —lo exige el control anterior— pero no con sus palabras
separadas igual), la lectura del documento NO se hace y manda el texto conservado, como antes de N3. Solo lee.
Uso: python3 -I -B r3b_pdf_reales_localizacion.py"""
import collections, glob, hashlib, json, os, re, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, PV
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
E0 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo")
_SHA = {}
VE._sha = lambda p: (_SHA.setdefault(p, hashlib.sha256(open(p, "rb").read()).hexdigest()) if os.path.isfile(p) else None)
CASOS = []
exp = os.path.join(E414, "elis_decisiones", "Elis")
CASOS.append(("Elis", exp, {os.path.basename(p)[:-4] + ".txt": p for p in glob.glob(os.path.join(exp, "fuentes_pdf", "*.pdf"))}))
exp = os.path.join(E414, "viscofan_decisiones", "Viscofan")
CASOS.append(("Viscofan", exp, {os.path.basename(p)[:-4] + ".txt": p for p in glob.glob(os.path.join(E412, "viscofan", "fuentes", "pdf", "*.pdf"))}))
exp = os.path.join(E414, "vidrala_decisiones", "Vidrala")
pv = {}
for p in glob.glob(os.path.join(E0, "fuentes", "cuentas_consolidadas_2016_2022", "*.pdf")):
    m = re.search(r"en-(\d{4})_consolidated", os.path.basename(p))
    if m:
        pv[f"CF_{m.group(1)}.txt"] = p
CASOS.append(("Vidrala", exp, pv))
tot = collections.Counter()
for nombre, exp, pdfs in CASOS:
    reg = json.load(open(os.path.join(exp, VE.REGISTRO), encoding="utf-8"))
    c = collections.Counter()
    ej = []
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else None
        if e.get("clase") not in ("dato_publicado", "cero_comprobado") or not f or not str(f.get("archivo") or "").startswith("texto/"):
            continue
        pdf = pdfs.get(os.path.basename(f["archivo"]))
        vf = f.get("valor_fuente")
        if not pdf or not VE._num(vf):
            continue
        est, pag = VE._pagina_examinable(os.path.join(exp, f["archivo"]), f.get("pagina"))
        if est != "ok" or VE._cita_cifra(f.get("cita"), vf, pag)[0] != "ok":
            continue
        n = VE._numero_pagina(f.get("pagina"))
        t1, t2 = VE._texto_pdf(pdf, n)[1], VE._texto_pdf(pdf, n, layout=False)[1]
        if VE._cmp_txt(f.get("cita")) not in VE._cmp_txt(t1) and VE._cmp_txt(f.get("cita")) not in VE._cmp_txt(t2):
            c["(la cita no está en el PDF)"] += 1
            continue
        s1, s2 = VE._cita_cifra(f.get("cita"), vf, t1)[0], VE._cita_cifra(f.get("cita"), vf, t2)[0]
        c[(s1, s2)] += 1
        if s1 == s2 == "no_localizada" and len(ej) < 4:
            ej.append((e["celda"], f.get("pagina"), str(f.get("cita"))[:90]))
    print(f"== {nombre}: (lectura con -layout, lectura sin layout) → nº de entradas")
    for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
        print(f"   {str(k):48} {v}")
        tot[k if isinstance(k, str) else ("alguna lectura en el documento" if "ok" in k or any(x not in ("ok", "no_localizada") for x in k) else "ninguna (no localizada en los dos)")] += v
    for x in ej:
        print("      no localizada en ninguno de los dos:", x)
print("\ntotal:", dict(tot))
