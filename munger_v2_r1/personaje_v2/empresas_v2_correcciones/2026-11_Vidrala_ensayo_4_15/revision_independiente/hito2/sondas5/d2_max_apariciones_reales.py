#!/usr/bin/env python3
"""d2 · MAX_APARICIONES_CITA = 200 (quinta comprobación) sobre los REGISTROS REALES. Solo lee.
A) Para cada entrada numérica con página de los siete registros de la 4.14: cuántas veces aparece su cita en la página citada
   (_apariciones_en_pagina, lo que cuenta el máximo). Distribución, máximo y las diez más repetidas. ¿Alguna supera 200?
B) Lo mismo si la cita se recortara a la sola cifra (la cita legítima más corta: «valor_fuente» tal como está impreso en la línea).
C) Peor caso de las páginas reales: para CADA página de los textos conservados citados, la «palabra» numérica que más se repite como
   aparición completa (lo que contaría una cita de una sola cifra, p. ej. «0», «1», «-» no: solo cifras) y la página más larga.
D) Si la «página» fuera el DOCUMENTO ENTERO (lo que ocurre con una fuente HTML: contraste_pagina lee la cifra también en todo el texto
   visible del documento): cuántas veces aparece cada cita real en su documento completo (texto conservado sin partir por páginas).
   Es una simulación con los textos reales, no un registro real: ninguno tiene fuente HTML.
Uso: python3 -I -B d2_max_apariciones_reales.py"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, PV, ACT  # noqa: E402
E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "vidrala/Vidrala", "elis_motor_A/Elis",
        "vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala"]
MAX = VE.MAX_APARICIONES_CITA
print(f"código: {ACT} · MAX_APARICIONES_CITA = {MAX}")
paginas, docs = {}, {}
hist_a, hist_b, hist_d = collections.Counter(), collections.Counter(), collections.Counter()
top_a, top_b, top_d = [], [], []
n_ent = 0
estados_doc = collections.Counter()
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado") or not f.get("archivo"):
            continue
        ruta = VE._ruta_fuente(c, f.get("archivo"))
        if not (ruta and str(ruta).lower().endswith(".txt")):
            continue
        est, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est != "ok":
            continue
        n_ent += 1
        paginas[(os.path.realpath(ruta), VE._numero_pagina(f.get("pagina")))] = pag
        cita = f.get("cita")
        na = len(VE._apariciones_en_pagina(cita, pag))
        hist_a[na] += 1
        top_a.append((na, exp.split("/")[0], e.get("celda"), str(cita)[:70]))
        # B) la cita recortada a la cifra: cada forma equivalente de vf que esté en la cita
        formas = [x for x in VE._cifras(vf) if re.search(r"(?<![\d.,])" + re.escape(x) + r"(?!\d|[.,]\d)", str(cita))]
        nb = max((len(VE._apariciones_en_pagina(x, pag)) for x in formas), default=0)
        hist_b[nb] += 1
        top_b.append((nb, exp.split("/")[0], e.get("celda"), vf, formas[:2]))
        # D) el documento entero como «página»
        rp = os.path.realpath(ruta)
        if rp not in docs:
            docs[rp] = open(rp, encoding="utf-8", errors="replace").read()
        nd = len(VE._apariciones_en_pagina(cita, docs[rp]))
        hist_d[nd] += 1
        top_d.append((nd, exp.split("/")[0], e.get("celda"), str(cita)[:70], os.path.basename(rp)[:40]))
        if nd > MAX:
            estados_doc[VE._cita_cifra(cita, vf, docs[rp])[0]] += 1


def resumen(h):
    tot = sum(h.values())
    tramos = [(1, 1), (2, 2), (3, 5), (6, 20), (21, 50), (51, 100), (101, 200), (201, 10 ** 9)]
    return " · ".join(f"{a}{'' if a == b else '–' + (str(b) if b < 10 ** 9 else '∞')}: {sum(v for k, v in h.items() if a <= k <= b)}" for a, b in tramos) + f" · (0: {h.get(0, 0)}) · total {tot}"


print(f"\n== A · apariciones de la cita REAL en su página ({n_ent} entradas numéricas con página, siete registros)")
print("   " + resumen(hist_a))
print(f"   máximo: {max(hist_a)} · entradas con más de {MAX}: {sum(v for k, v in hist_a.items() if k > MAX)}")
for x in sorted(top_a, reverse=True)[:10]:
    print("     ", x)
print("\n== B · apariciones si la cita se recortara a la sola cifra (la forma impresa de valor_fuente)")
print("   " + resumen(hist_b))
print(f"   máximo: {max(hist_b)} · entradas con más de {MAX}: {sum(v for k, v in hist_b.items() if k > MAX)}")
for x in sorted(top_b, key=lambda t: -t[0])[:10]:
    print("     ", x)

print(f"\n== C · peor caso de las páginas reales ({len(paginas)} páginas citadas distintas)")
peor = []
for (ruta, n), pag in paginas.items():
    t = re.sub(r"[   ]", " ", pag)
    cnt = collections.Counter(m.group(0) for m in re.finditer(r"(?<![\d.,])\d+(?:[.,]\d+)*(?!\d|[.,]\d)", t))
    if cnt:
        tok, k = cnt.most_common(1)[0]
        peor.append((k, tok, os.path.basename(ruta)[:44], n, len(pag)))
peor.sort(reverse=True)
print("   la cifra más repetida de cada página (nº de veces, cifra, texto, página, caracteres de la página); las diez mayores:")
for x in peor[:10]:
    print("     ", x)
print(f"   páginas en las que alguna cifra se repite más de {MAX} veces: {sum(1 for x in peor if x[0] > MAX)} de {len(peor)}")
lon = sorted((len(p), os.path.basename(r)[:44], n) for (r, n), p in paginas.items())
print(f"   página citada más larga: {lon[-1]} · mediana {lon[len(lon) // 2][0]} caracteres")

print("\n== D · simulación: el documento ENTERO como «página» (lo que se lee en una fuente HTML)")
print("   " + resumen(hist_d))
print(f"   máximo: {max(hist_d)} · entradas cuya cita real aparece más de {MAX} veces en su documento: {sum(v for k, v in hist_d.items() if k > MAX)} de {n_ent}")
print(f"   estado de _cita_cifra(cita, vf, documento) en esas entradas: {dict(estados_doc)}")
for x in sorted(top_d, reverse=True)[:12]:
    print("     ", x)

print("\n== C2 · guiones por página (una cita que fuera solo «-» o «–», el cero impreso como guion, cuenta TODOS los guiones de la página)")
gui = sorted(((sum(pag.count(g) for g in "-‐‑‒–—−"), os.path.basename(r)[:44], n) for (r, n), pag in paginas.items()), reverse=True)
print(f"   páginas con más de {MAX} guiones: {sum(1 for x in gui if x[0] > MAX)} de {len(gui)} · las cinco con más: {gui[:5]}")
ceros = collections.Counter()
for exp in EXPS:
    reg, err = VE.cargar(os.path.join(E14, exp))
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if VE._num(f.get("valor_fuente")) and f.get("valor_fuente") == 0 and e.get("clase") in ("dato_publicado", "cero_comprobado"):
            ceros[len(str(f.get("cita") or "").split())] += 1
print(f"   entradas reales con valor_fuente 0, por nº de palabras de su cita: {dict(sorted(ceros.items()))} (ninguna cita es un guion solo si no hay clave 1 con un guion)")
solo_guion = [(exp, e.get("celda"), e["fuente"].get("cita")) for exp in EXPS for e in VE.cargar(os.path.join(E14, exp))[0]["entradas"]
              if isinstance(e.get("fuente"), dict) and str(e["fuente"].get("cita") or "").strip() in tuple("-‐‑‒–—−")]
print(f"   entradas reales cuya cita es solo un guion: {len(solo_guion)} {solo_guion[:3]}")

print("\n== D2 · simulación: la cita recortada a la CIFRA y el documento entero como «página», con 7a6583b (sin máximo) y con 876bfc2")
from comun5 import VP  # noqa: E402
c2 = collections.Counter()
ej2 = {}
for exp in EXPS[:3]:  # los tres registros finales
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado") or not f.get("archivo"):
            continue
        ruta = VE._ruta_fuente(c, f.get("archivo"))
        if not (ruta and str(ruta).lower().endswith(".txt")) or VE._pagina_examinable(ruta, f.get("pagina"))[0] != "ok":
            continue
        doc = docs[os.path.realpath(ruta)]
        formas = [x for x in VE._cifras(vf) if re.search(r"(?<![\d.,])" + re.escape(x) + r"(?!\d|[.,]\d)", str(f.get("cita")))]
        if not formas:
            continue
        x = max(formas, key=len)
        n = len(VE._apariciones_en_pagina(x, doc))
        a, b = VP._cita_cifra(x, vf, doc)[0], VE._cita_cifra(x, vf, doc)[0]
        k_ = ("más de 200 apariciones" if n > MAX else "hasta 200", a, b)
        c2[k_] += 1
        ej2.setdefault(k_, (exp.split("/")[0], e.get("celda"), x, n))
for k_, v in sorted(c2.items()):
    print(f"   {k_[0]:24} 7a6583b {k_[1]:20} → 876bfc2 {k_[2]:20} {v:5}   ej.: {ej2[k_]}")
