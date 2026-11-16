#!/usr/bin/env python3
"""r3 · N3 (tercera pasada) con PDF REALES (solo lectura): la parte B de q12_pdf.py (tercera pasada del hito 1), ampliada a Vidrala y a los
dos códigos. Cada entrada real de Elis, Viscofan y Vidrala (registros finales de la 4.14) cuya fuente es un texto conservado con PDF en el
árbol se contrasta (VE.contraste_pagina) citando el .txt (como hoy) y citando el PDF con el .txt como «archivo_texto». Con N3, citando el
PDF la cifra y su signo se leen también en el texto del PDF (pdftotext con «-layout» y sin él): ¿rechaza entradas legítimas?
Además, para cada entrada se prueban sobre el PDF: (v1) la línea completa del texto conservado, (v3) la cifra sola con sus marcas y
(v4) la cifra sola sin marcas; y todas ellas con el signo CONTRARIO al real (ninguna debería pasar).
Uso: python3 -I -B r3_pdf_reales.py"""
import collections, copy, glob, hashlib, json, os, re, shutil, sys, tempfile, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, PV, ACT, ANT

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
E412 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_12")
E0 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo")
MARCAS = "-‐‑‒–—﹣－−"
_SHA = {}


def sha(p):
    if p not in _SHA:
        _SHA[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return _SHA[p]


# el control calcula la huella del PDF en cada llamada (para su caché); aquí los archivos no cambian: se memoriza (solo acelera la sonda)
for M in (VE, VP):
    M._sha = (lambda orig: (lambda p: sha(p) if os.path.isfile(p) else None))(M._sha)


def preparar(nombre, exp, pdfs):
    """Copia temporal del expediente (registro y textos) con los PDF dentro, en fuentes_pdf/<nombre del texto>.pdf (enlaces a los reales)."""
    tmp = tempfile.mkdtemp(prefix="rev3_pdf_")
    carpeta = os.path.join(tmp, nombre)
    os.makedirs(os.path.join(carpeta, "fuentes_pdf"))
    shutil.copytree(os.path.join(exp, "texto"), os.path.join(carpeta, "texto"))
    shutil.copy(os.path.join(exp, VE.REGISTRO), carpeta)
    for txt, pdf in pdfs.items():
        shutil.copy(pdf, os.path.join(carpeta, "fuentes_pdf", txt[:-4] + ".pdf"))
    return carpeta


def variantes(M, cita, vf, pag):
    """Citas alternativas sobre la misma página y la misma cifra (como n12 de la segunda pasada)."""
    out = {}
    apar = M._apariciones_en_pagina(cita, pag)
    if not apar:
        return out
    linea, a, b = apar[0]
    out["v1 línea completa"] = linea.strip()
    if vf == 0:
        return out
    for cf in sorted(M._cifras(vf), key=len, reverse=True):
        for m in re.finditer(r"(?<![\d.,])" + re.escape(cf) + r"(?!\d|[.,]\d)", linea):
            if m.start() >= a and m.end() <= b:
                i, j = m.start(), m.end()
                i2, j2 = i, j
                if i2 > 0 and linea[i2 - 1] in "€$£¥":
                    i2 -= 1
                if i2 > 0 and linea[i2 - 1] in MARCAS + "(+":
                    i2 -= 1
                if linea[j2:j2 + 1] == ")":
                    j2 += 1
                out["v3 cifra con sus marcas"] = linea[i2:j2]
                out["v4 cifra sin marcas"] = linea[i:j]
                return out
    return out


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

print(f"VE = {ACT} · VP = {ANT}")
for nombre, exp, pdfs in CASOS:
    t0 = time.time()
    carpeta = preparar(nombre, exp, pdfs)
    reg = json.load(open(os.path.join(carpeta, VE.REGISTRO), encoding="utf-8"))
    n_tot = n_sin = 0
    c = collections.Counter()
    solo_n3, det_var = [], collections.defaultdict(list)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else None
        if e.get("clase") not in ("dato_publicado", "cero_comprobado") or not f or not str(f.get("archivo") or "").startswith("texto/"):
            continue
        n_tot += 1
        txt = f["archivo"]
        pdf = "fuentes_pdf/" + os.path.basename(txt)[:-4] + ".pdf"
        if not os.path.isfile(os.path.join(carpeta, pdf)):
            n_sin += 1
            continue
        vf = f.get("valor_fuente")
        f2 = dict(copy.deepcopy(f), archivo=pdf, sha256=sha(os.path.join(carpeta, pdf)), archivo_texto=txt, sha256_texto=sha(os.path.join(carpeta, txt)))
        r_txt = VE.contraste_pagina(carpeta, e["celda"], f, VE._ruta_fuente(carpeta, txt), vf)
        r_ant = VP.contraste_pagina(carpeta, e["celda"], f2, VP._ruta_fuente(carpeta, pdf), vf)
        r_act = VE.contraste_pagina(carpeta, e["celda"], f2, VE._ruta_fuente(carpeta, pdf), vf)
        c["citando el .txt: pasa"] += r_txt is None
        c[f"citando el PDF, {ANT}: pasa"] += r_ant is None
        c[f"citando el PDF, {ACT}: pasa"] += r_act is None
        if r_ant is None and r_act is not None:
            solo_n3.append((e["celda"], os.path.basename(pdf), f.get("pagina"), r_act[0], str(f.get("cita"))[:100], r_act[1][:170]))
        if not VE._num(vf) or r_txt is not None:
            continue
        est, pag = VE._pagina_examinable(VE._ruta_fuente(carpeta, txt), f.get("pagina"))
        for nv, var in variantes(VE, f.get("cita"), vf, pag).items():
            for etq, signo in (("real", 1), ("CONTRARIO", -1)):
                if signo == -1 and vf == 0:
                    continue
                fv = dict(f2, cita=var, valor_fuente=signo * vf)
                ra = VP.contraste_pagina(carpeta, e["celda"], fv, VP._ruta_fuente(carpeta, pdf), signo * vf)
                rn = VE.contraste_pagina(carpeta, e["celda"], fv, VE._ruta_fuente(carpeta, pdf), signo * vf)
                clave = (nv, etq, "pasa" if ra is None else ra[0], "pasa" if rn is None else rn[0])
                c[clave] += 1
                if (ra is None) != (rn is None) or (rn is not None and ra is not None and ra[0] != rn[0]):
                    if len(det_var[clave]) < 4:
                        det_var[clave].append((e["celda"], os.path.basename(pdf), f.get("pagina"), var[:80], (rn or ra)[1][:150]))
    print(f"\n== {nombre}: {n_tot} entradas con fuente texto/…; sin PDF en el árbol: {n_sin}  ({time.time() - t0:.0f} s)")
    for k in sorted(k for k in c if isinstance(k, str)):
        print(f"   {k:48} {c[k]}")
    print(f"   rechazadas SOLO por la lectura nueva en el PDF (N3): {len(solo_n3)}")
    for x in solo_n3[:15]:
        print("      ", x)
    print("   citas alternativas sobre el PDF (variante, signo, resultado anterior → resultado actual): nº")
    for k in sorted(k for k in c if isinstance(k, tuple)):
        print(f"      {k[0]:26} {k[1]:10} {k[2]:14} → {k[3]:14} {c[k]}")
        for x in det_var.get(k, []):
            print("           ", x)
    shutil.rmtree(os.path.dirname(carpeta), ignore_errors=True)
