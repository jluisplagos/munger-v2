#!/usr/bin/env python3
"""Resumen de las mutaciones ejecutadas (lee fable/mut*/<nombre>/resultado.json)."""
import json, os, sys
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for base in ("mut", "mut_hito1"):
    d0 = os.path.join(F, base)
    if not os.path.isdir(d0):
        continue
    print(f"=== {'código del hito 2 (candidata)' if base == 'mut' else 'código y pruebas del HITO 1 (comparación)'}")
    for n in sorted(os.listdir(d0)):
        p = os.path.join(d0, n, "resultado.json")
        if not os.path.exists(p):
            print(f"{n}: (en curso o sin resultado)")
            continue
        r = json.load(open(p, encoding="utf-8"))
        if "error" in r:
            print(f"{n}: ERROR DE LA MUTACIÓN {r['error']}")
            continue
        det = all(v["codigo"] == 0 and not v["fallan"] for v in r["baterias"].values())
        print(f"{n} · {r['descripcion']}\n    → {'NO DETECTADA (todas las baterías pasan)' if det else 'detectada'}")
        for b, v in r["baterias"].items():
            print(f"      {b}: código {v['codigo']} · {v['pasan']} · fallan {len(v['fallan'])} · {v['segundos']} s" + (f" · traza: {v['traza'][-1][:160]}" if v["traza"] and v["codigo"] != 0 and not v["fallan"] else ""))
            for x in v["fallan"][:6]:
                print(f"         {x[:200]}")
