#!/usr/bin/env python3
"""Contraste de las cifras de la Historia de Viscofan con las publicaciones recuperadas (encargo 4.12 §8: «se reutilizarán las cifras
anteriores y se contrastarán»). Solo lee el origen y viscofan/fuentes/; escribe viscofan/fuentes/contraste_cifras_historia.json y .md.

Para cada partida y año de la Historia (personaje_v2/empresas_v2/Viscofan/fase1_v63.json), la fuente dice de qué informe salió (AR_X) y
si es su cifra propia o el comparativo del informe siguiente. Las cifras impresas que la fase 1 sumó para esa celda
(fase1_partes/AR_X.json, columna «actual» o «anterior») se buscan, por sus dígitos y en cualquier página, en la publicación recuperada
de ese ejercicio X y, si no la hay o no está, en la del año de la cifra. Estados:
  - contrastada: todas sus cifras impresas (de 4 o más dígitos) están en una publicación recuperada (se dice cuál y en qué página);
  - parcial: alguna sí y alguna no; corta: solo cifras de 1–3 dígitos (coincidencia no concluyente);
  - no encontrada: hay publicación recuperada y no aparece; sin publicación: no hay publicación recuperada del ejercicio;
  - sin cifra: la celda es un cero con motivo o está vacía (DESCONOCIDO).
Encontrar los dígitos no prueba que hablen de esa partida (la página y el contexto sí); no encontrarlos en otra edición no prueba que
la cifra antigua sea errónea. Es un contraste, no una verificación del PDF original (que no está).
Uso (desde munger_v2_r1/): python3 -I …/scripts/contraste_cifras_viscofan.py
"""
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
ORIG = os.path.join(PV, "empresas_v2", "Viscofan")
F = os.path.join(EXP, "viscofan", "fuentes")
DOCS = {2025: "AR_2025.txt", 2024: "CF_2024.txt", 2023: "CA_2023_es.txt", 2022: "CF_2022_compilacion.txt", 2021: "CF_2021.txt", 2020: "AR_2020.txt",
        2019: "AR_2019.txt", 2018: "IA_2018_es.txt", 2017: "AR_2017.txt", 2016: "IA_2016_es.txt"}
EQUIV = {"circulante": "circulante_lineas", "tipo_impositivo": ("impuestos", "bai")}
NUM = re.compile(r"(?<![\w.,])[-−(]?\d[\d.,]*\d\)?|(?<![\w.,])\d(?![\w.,])")


def digitos(s):
    return re.sub(r"\D", "", str(s or ""))


def indice(arch):
    t = open(os.path.join(F, "texto", arch), encoding="utf-8").read()
    p = re.split(r"\[PDF PAGE (\d+)\]", t)
    idx = {}
    for i in range(1, len(p), 2):
        for m in NUM.finditer(p[i + 1]):
            idx.setdefault(digitos(m.group(0)), set()).add(int(p[i]))
    return idx


def fuentes_por_anio(fuente):
    """«2016 AR_2017.txt p.8 (comparativo del informe siguiente); …» → {2016: (2017, 'anterior'), …}; desconocido o cero → (X, None)."""
    out = {}
    for trozo in str(fuente or "").split(";"):
        m = re.match(r"\s*(\d{4})\s+(?:AR_(\d{4})\.txt\s+p\.[\d,]+(.*)|desconocido)", trozo)
        if not m:
            continue
        y = int(m.group(1))
        if not m.group(2):
            out[y] = (None, None)
            continue
        resto = m.group(3) or ""
        out[y] = (int(m.group(2)), None if "cero:" in resto else ("anterior" if "comparativo" in resto else "actual"))
    return out


def main():
    f1 = json.load(open(os.path.join(ORIG, "fase1_v63.json"), encoding="utf-8"))
    H = f1["historia"]["partidas"]
    anios = f1["historia"]["anios"]
    AR = {}
    for a in anios:
        p = os.path.join(ORIG, "fase1_partes", f"AR_{a}.json")
        if os.path.exists(p):
            AR[a] = json.load(open(p, encoding="utf-8"))["partidas"]
    IDX = {a: indice(d) for a, d in DOCS.items()}
    tabla, cuenta = {}, {}
    for k, v in H.items():
        if not isinstance(v, dict) or "valores" not in v:
            continue
        fa = fuentes_por_anio(v.get("fuente"))
        if k == "tipo_impositivo":  # «impuestos ÷ resultado antes de impuestos; 2016 AR_2017.txt p.8 (…) / AR_2017.txt p.8 (…); …»
            fa = fuentes_por_anio(";".join(x.split("/")[0] for x in str(v.get("fuente")).split(";")[1:]))
        claves = EQUIV.get(k, k)
        claves = claves if isinstance(claves, tuple) else (claves,)
        fila = {}
        for i, y in enumerate(anios):
            val = v["valores"][i]
            x, lado = fa.get(y, (None, None))
            if val is None or x is None or lado is None:
                fila[y] = {"estado": "sin cifra", "valor": val}
                continue
            comps = []
            for kk in claves:
                c = ((AR.get(x) or {}).get(kk) or {}).get(lado) or []
                comps += [z for z in c if isinstance(z, dict) and z.get("impreso")]
            if not comps:
                fila[y] = {"estado": "sin cifra", "valor": val, "nota": f"sin cifras impresas en AR_{x}.json ({lado})"}
                continue
            docs = [d for d in (x, y) if d in IDX]
            if not docs:
                fila[y] = {"estado": "sin publicación", "valor": val, "informe": f"AR_{x}", "lado": lado}
                continue
            res = []
            for z in comps:
                dg = digitos(z["impreso"])
                if len(dg) <= 3:
                    res.append(("corta", z["impreso"], None))
                    continue
                hall = next(((d, sorted(IDX[d][dg])[:3]) for d in docs if dg in IDX[d]), None)
                res.append(("si" if hall else "no", z["impreso"], hall))
            largos = [r for r in res if r[0] != "corta"]
            if not largos:
                est = "corta"
            elif all(r[0] == "si" for r in largos):
                est = "contrastada"
            elif any(r[0] == "si" for r in largos):
                est = "parcial"
            else:
                est = "no encontrada"
            fila[y] = {"estado": est, "valor": val, "informe": f"AR_{x}", "lado": lado,
                       "cifras": [{"impreso": imp, "encontrada": e, "en": (f"{DOCS[h[0]]} p. {', '.join(map(str, h[1]))}" if h else None)} for e, imp, h in res]}
        tabla[k] = fila
        for y, c in fila.items():
            cuenta.setdefault(y, {}).setdefault(c["estado"], 0)
            cuenta[y][c["estado"]] += 1
    out = {"origen": "personaje_v2/empresas_v2/Viscofan/fase1_v63.json", "publicaciones": DOCS, "por_anio": cuenta, "tabla": tabla}
    json.dump(out, open(os.path.join(F, "contraste_cifras_historia.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    sim = {"contrastada": "✓", "parcial": "≈", "no encontrada": "✗", "sin publicación": "·", "sin cifra": "—", "corta": "c"}
    md = ["# Viscofan · contraste de las cifras de la Historia con las publicaciones recuperadas (encargo 4.12 §8)", "",
          "✓ contrastada (todas sus cifras impresas de 4 o más dígitos están en una publicación recuperada) · ≈ parcial · ✗ no encontrada en la publicación recuperada · "
          "· sin publicación recuperada del ejercicio · — cero con motivo o vacío · c solo cifras cortas (no concluyente). Encontrar los dígitos no prueba que hablen de esa "
          "partida; no encontrarlos en otra edición no prueba que la cifra antigua sea errónea. No es una verificación del PDF original, que no está.", "",
          "| Partida | " + " | ".join(str(a) for a in anios) + " |", "|---|" + "---|" * len(anios)]
    for k, fila in tabla.items():
        md.append(f"| {k} | " + " | ".join(sim[fila[a]["estado"]] for a in anios) + " |")
    md += ["", "| Año | " + " | ".join(sim.values()) + " |", "|---|" + "---|" * len(sim)]
    for a in anios:
        md.append(f"| {a} | " + " | ".join(str(cuenta.get(a, {}).get(e, 0)) for e in sim) + " |")
    md += ["", "Detalle de las no encontradas y parciales:", ""]
    for k, fila in tabla.items():
        for a in anios:
            c = fila[a]
            if c["estado"] in ("no encontrada", "parcial"):
                md.append(f"- {k} {a} ({c['informe']}, {c['lado']}): " + "; ".join(f"«{z['impreso']}» {'en ' + z['en'] if z['en'] else z['encontrada']}" for z in c["cifras"]))
    open(os.path.join(F, "contraste_cifras_historia.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    tot = {e: sum(cuenta.get(a, {}).get(e, 0) for a in anios) for e in sim}
    print("OK: " + " · ".join(f"{e} {n}" for e, n in tot.items()) + " → viscofan/fuentes/contraste_cifras_historia.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
