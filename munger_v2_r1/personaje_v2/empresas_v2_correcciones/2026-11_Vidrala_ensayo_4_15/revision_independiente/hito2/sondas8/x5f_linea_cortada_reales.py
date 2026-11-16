#!/usr/bin/env python3
"""x5f · octava comprobación · fuera del diff: R-a de `comprobar_anio` solo exige que la `linea`, tal como la da la extracción, sea una
SUBCADENA de la página (`norm(lin) in P[pg]`), sin límites. Una línea cortada justo en un separador de miles deja el trozo como «importe
completo en su línea» (x5e, casos 16 y 17). ¿Hay líneas así en las extracciones reales? Para cada componente real con página examinable se
buscan todas las apariciones de la línea en su página y se mira si ALGUNA no está cortada dentro de un número (por delante: la línea
empieza por cifra y la precede cifra, «.», «,» o «cifra+apóstrofo»; por detrás: acaba en cifra y siguen «[\\d.,'’]*\\d»).
Solo lectura. Uso: python3 -I -B x5f_linea_cortada_reales.py"""
import collections, glob, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, CONGELADO  # noqa: E402
PVC = os.path.join(CONGELADO, "personaje_v2")
DEL = re.compile(r"(?:[\d.,]|\d['’])\Z")
DET = re.compile(r"[\d.,'’]*\d")
tot = collections.Counter()
ej = []
vistos = set()
for c in sorted(os.path.dirname(d) for d in glob.glob(os.path.join(PVC, "**", "fase1_partes"), recursive=True)):
    if not os.path.isdir(os.path.join(c, "texto")):
        continue
    for f in sorted(glob.glob(os.path.join(c, "fase1_partes", "AR_*.json"))):
        d = json.load(open(f, encoding="utf-8"))
        arch = d.get("archivo")
        if not arch or not os.path.exists(os.path.join(c, "texto", arch)):
            continue
        P = {k: FN.norm(v) for k, v in FN.paginas(os.path.join(c, "texto", arch)).items()}
        for k, p in (d.get("partidas") or {}).items():
            if not isinstance(p, dict):
                continue
            for cual in ("actual", "anterior"):
                for comp in FN.componentes(p.get(cual)):
                    imp, pg, lin = comp.get("impreso"), comp.get("pagina"), comp.get("linea")
                    if imp is None or not lin or not isinstance(pg, int) or pg not in P:
                        continue
                    L = FN.norm(lin)
                    clave = (arch, pg, L, FN.norm(imp))
                    tot["componentes con página examinable"] += 1
                    if clave in vistos:
                        continue
                    vistos.add(clave)
                    tot["distintos (archivo, página, línea, impreso)"] += 1
                    pos, limpia, ini = [], False, 0
                    while True:
                        i = P[pg].find(L, ini)
                        if i < 0:
                            break
                        pos.append(i)
                        cort_del = L[0].isdigit() and DEL.search(P[pg][max(0, i - 2):i]) is not None
                        cort_det = L[-1].isdigit() and DET.match(P[pg], i + len(L)) is not None
                        limpia = limpia or not (cort_del or cort_det)
                        ini = i + 1
                    if not pos:
                        tot["línea que no está en la página"] += 1
                    elif not limpia:
                        tot["línea que SOLO aparece cortada dentro de un número"] += 1
                        if len(ej) < 8:
                            ej.append((os.path.relpath(c, PVC)[-40:], arch[:30], pg, imp, L[:70]))
                    else:
                        tot["línea con alguna aparición no cortada dentro de un número"] += 1
                    if L[0].isdigit():
                        tot["líneas que empiezan por cifra"] += 1
                    if L[-1].isdigit():
                        tot["líneas que acaban en cifra"] += 1
for k in sorted(tot):
    print(f"   {k}: {tot[k]:,}")
print("   ejemplos de líneas solo cortadas:", ej or "ninguno")
