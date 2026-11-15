#!/usr/bin/env python3
"""s3b · Registros reales (solo lectura): ¿cuántas entradas dependen de la regla «un guion separado de la cifra por dos o más espacios
es otra columna (un cero) y la cifra es positiva»? Y ¿cuántas cifras negativas se leen por paréntesis, por menos pegado o por menos Unicode?
Además: en TODAS las páginas citadas, cuántas veces aparece un guion o un menos seguido de 2 o más espacios y una cifra (el caso dudoso)."""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["elis_decisiones/Elis", "vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan"]
MARCAS = VE.GUIONES + VE.MENOS_UNICODE
for exp in EXPS:
    d = os.path.join(E414, exp)
    reg, err = VE.cargar(d)
    cuenta = collections.Counter()
    ejemplos = collections.defaultdict(list)
    paginas = {}
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or vf == 0 or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(d, f.get("archivo")) if f.get("archivo") else None
        if not ruta or not str(ruta).lower().endswith(".txt"):
            continue
        est_p, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est_p != "ok":
            continue
        paginas[(ruta, f.get("pagina"))] = pag
        t = re.sub(r"[\xa0  ]", " ", str(VE._pasaje_en_pagina(f.get("cita"), pag) or f.get("cita") or ""))
        for c in VE._cifras(vf):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", t):
                antes, despues = t[:m.start()], t[m.end():]
                antes = re.sub("[" + VE.MONEDAS + r"]\s?$", "", antes)
                s = VE._signo_en_cita(t, m.start(), m.end())
                if re.search(r"\(\s*$", antes):
                    via = "paréntesis"
                elif re.search(VE.MENOS_UNICODE + r"\s?$", antes):
                    via = "menos Unicode"
                elif re.search("[" + re.escape(VE.GUIONES) + r"]$", antes):
                    via = "guion pegado"
                elif re.search("[" + re.escape(VE.GUIONES) + r"]\s$", antes):
                    via = "guion a un espacio"
                elif re.search("[" + re.escape(MARCAS) + r"]\s{2,}$", antes):
                    via = "guion o menos a 2+ espacios (regla de la otra columna)"
                else:
                    via = "sin marca"
                cuenta[f"signo leído {s!r:>4} · {via}"] += 1
                if via.startswith("guion o menos a 2+") or via == "guion a un espacio":
                    ejemplos[via].append((e["celda"], vf, repr(t[max(0, m.start() - 40):m.end() + 5])))
    print(f"\n=== {exp}")
    for k, v in sorted(cuenta.items()):
        print(f"   {v:4d}  {k}")
    for k, lst in ejemplos.items():
        print(f"   -- {k}: {len(lst)}")
        for x in lst[:10]:
            print("        ", x)
    # el caso dudoso en las páginas citadas, se cite o no
    dud = collections.Counter()
    ej = []
    for (ruta, pg), pag in paginas.items():
        tt = re.sub(r"[\xa0  ]", " ", pag)
        for m in re.finditer(r"(?<![\w.,])([" + re.escape(MARCAS) + r"])( {2,})(\(?\d[\d.,  ]*)", tt):
            dud["marca + 2 o más espacios + cifra en la misma línea"] += 1
            if len(ej) < 6:
                ej.append(repr(tt[max(0, m.start() - 50):m.end() + 10]))
        for m in re.finditer(r"(?<![\w.,])([" + re.escape(MARCAS) + r"]) (\(?\d)", tt):
            dud["marca + 1 espacio + cifra"] += 1
        for m in re.finditer(r"(?<![\w.,)])([" + re.escape(MARCAS) + r"])(\d)", tt):
            dud["marca pegada a una cifra"] += 1
    print(f"   en las {len(paginas)} páginas citadas: {dict(dud)}")
    for x in ej:
        print("        ", x)
