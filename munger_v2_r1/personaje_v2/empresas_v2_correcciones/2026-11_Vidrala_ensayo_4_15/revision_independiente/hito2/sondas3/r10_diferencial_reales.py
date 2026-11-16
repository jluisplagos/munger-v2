#!/usr/bin/env python3
"""r10 · N4/N10 (tercera pasada): diferencial entre la candidata anterior (92b2362) y la tercera (f3d15e8) sobre las PÁGINAS REALES.
Para cada una de las 1.645 entradas numéricas reales (inventario «ok») se generan, con semilla fija, citas alternativas que son un tramo
de su línea de la página que CONTIENE la cifra entera con sus marcas, cortado en posiciones de carácter al azar (no solo entre palabras):
  tipo P: el tramo empieza y acaba entre palabras (un extractor cuidadoso);   tipo C: empieza o acaba en un carácter cualquiera.
Se contrasta cada una con el valor_fuente real y con el signo contrario, con los dos códigos. Interesa: (1) ¿alguna pasa de rechazo a «ok»
(aceptación nueva)? (2) ¿alguna da «ok» con el signo contrario? (3) ¿cuántas citas de tipo P (legítimas) pasan de «ok» a rechazo, y por qué?
Solo lee.  Uso: python3 -I -B r10_diferencial_reales.py"""
import collections, os, random, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun3 import VE, VP, PV

E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala",
        "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]
MARCAS = "-‐‑‒–—﹣－−"
rnd = random.Random(20261115)
trans = collections.Counter()
ej = collections.defaultdict(list)
n = 0
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf, cita = f.get("valor_fuente"), f.get("cita")
        if not VE._num(vf) or vf == 0 or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(c, f.get("archivo")) if f.get("archivo") else None
        if not (ruta and str(ruta).lower().endswith(".txt")):
            continue
        est, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est != "ok" or VE._cita_cifra(cita, vf, pag)[0] != "ok":
            continue
        apar = VE._apariciones_en_pagina(cita, pag)
        linea, a, b = apar[0]
        m_c = None
        for cf in sorted(VE._cifras(vf), key=len, reverse=True):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(cf) + r"(?!\d|[.,]\d)", linea):
                if m.start() >= a and m.end() <= b:
                    m_c = m
                    break
            if m_c:
                break
        if not m_c:
            continue
        n += 1
        i, j = m_c.start(), m_c.end()
        if i > 0 and linea[i - 1] in "€$£¥":
            i -= 1
        if i > 0 and linea[i - 1] in MARCAS + "(+":
            i -= 1
        if linea[j:j + 1] == ")":
            j += 1
        limites_ini = [0] + [k.end() for k in re.finditer(r"\s+", linea[:i])]
        limites_fin = [k.start() + j for k in re.finditer(r"\s+", linea[j:])] + [len(linea)]
        for _ in range(4):
            for tipo in "PC":
                if tipo == "P":
                    s, t_ = rnd.choice(limites_ini), rnd.choice(limites_fin)
                else:
                    s, t_ = rnd.randint(0, i), rnd.randint(j, len(linea))
                var = linea[s:t_].strip()
                if not var or VE._norm_txt(var) not in VE._norm_txt(pag):
                    continue
                for etq, v in (("real", vf), ("CONTRARIO", -vf)):
                    r1, r2 = VP._cita_cifra(var, v, pag)[0], VE._cita_cifra(var, v, pag)[0]
                    k = (tipo, etq, r1, r2)
                    trans[k] += 1
                    if r1 != r2 and len(ej[k]) < 5:
                        ant, des = linea[max(0, s - 3):s], linea[t_:t_ + 3]
                        ej[k].append((exp.split("/")[0], e.get("celda"), v, var[:70], f"…{ant!r}|cita|{des!r}…"))
print(f"{n} entradas reales no nulas con su cifra localizada en la línea · citas generadas: {sum(v for k, v in trans.items() if k[1] == 'real')}")
print("(tipo de corte, signo, anterior → tercera): nº")
for k in sorted(trans):
    marca = ""
    if k[1] == "CONTRARIO" and k[3] == "ok":
        marca = "   <<< «ok» con el signo CONTRARIO"
    elif k[2] != "ok" and k[3] == "ok":
        marca = "   (aceptación nueva: se examina abajo)"
    elif k[0] == "P" and k[1] == "real" and k[2] == "ok" and k[3] != "ok":
        marca = "   <<< cita cortada entre palabras que antes valía y ahora no"
    print(f"   {k[0]} {k[1]:10} {k[2]:20} → {k[3]:20} {trans[k]}{marca}")
print("ejemplos de cambios:")
for k in sorted(ej):
    for x in ej[k]:
        print(f"   {k}: {x}")
