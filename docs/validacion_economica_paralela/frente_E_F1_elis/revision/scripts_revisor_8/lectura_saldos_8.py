"""Revisión independiente n.º 8 · lectura con otro motor (PDFium) de las filas de saldo que C16 acepta por la regla de S1.

Para cada línea con alguna aceptación nueva (candidata G que no era OK en C14 y es OK en las seis dimensiones en C16), se
busca en el texto de la página extraído con PDFium (pypdfium2), no con pdftotext, la secuencia de las cifras de la fila,
en su orden; el rótulo es lo que PDFium pone delante de la primera cifra en esa línea y, si ahí no hay una fecha completa,
también la línea anterior o las dos anteriores. La fecha se lee con expresiones propias (no las del verificador) y su ejercicio se compara con
el que da la regla del autor (`anio_de_saldo_en_rotulo`): cierre a 31 de diciembre de A → A; apertura a 1 de enero de A →
A − 1. No modifica nada del autor.

Uso: python3 -I -B lectura_saldos_8.py --todas <jsonl.gz de barrido_8.py> --raiz <munger_v2_r1> --c16 <frente C17>
"""
import argparse
import gzip
import json
import re
import sys
import unicodedata
from collections import Counter
from pathlib import Path

import pypdfium2

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes8 as H  # noqa: E402

CIERRE = [r"(?i)december\s*,?\s*31\s*,?\s*(20\d\d)", r"(?i)31\s+d[ée]cembre\s+(20\d\d)", r"12/31/(20\d\d)", r"31/12/(20\d\d)"]
APERTURA = [r"(?i)january\s+1\s*,?\s*(20\d\d)", r"(?i)1er\s+janvier\s+(20\d\d)"]


def ejercicio(rotulo):
    """Ejercicio de la última fecha completa del rótulo (la más próxima a las cifras), o None."""
    mejor = None
    for rxs, d in ((CIERRE, 0), (APERTURA, -1)):
        for rx in rxs:
            for m in re.finditer(rx, rotulo):
                if mejor is None or m.start() > mejor[0]:
                    mejor = (m.start(), int(m.group(1)) + d)
    return None if mejor is None else mejor[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--todas", required=True)
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--c16", required=True)
    a = ap.parse_args()
    N = H.Version("C16", a.c16, a.raiz)
    lineas = []
    with gzip.open(a.todas, "rt", encoding="utf-8") as f:
        for l in f:
            ln = json.loads(l)
            if any(H.estado_de_codigo(g["n"]) == "OK" and H.estado_de_codigo(g["a"]) != "OK" for t in ln["toks"] for g in t["G"].values()):
                lineas.append(ln)
    lineas.sort(key=lambda x: (x["doc"], x["p"], x["i"]))
    docs = {}

    def texto(doc, pag):
        d = docs.setdefault(doc, pypdfium2.PdfDocument(str(N.pdf(doc))))
        t = d[pag - 1].get_textpage().get_text_range()
        return unicodedata.normalize("NFKC", t).replace("’", "'").replace("\r\n", "\n").replace("\r", "\n")

    print(f"Lectura con PDFium (pypdfium2 {pypdfium2.version.PYPDFIUM_INFO}) de las líneas con aceptaciones nuevas de C16: {len(lineas)} líneas")
    res = Counter()
    for ln in lineas:
        nuevos = [t for t in ln["toks"] if any(H.estado_de_codigo(g["n"]) == "OK" and H.estado_de_codigo(g["a"]) != "OK" for g in t["G"].values())]
        # cifras de la fila: los tokens que no son un año, ni la pestaña del margen, ni el día de la fecha del rótulo
        ini_cifras = len(ln["l"]) - len(ln["l"].lstrip()) + len(ln["rot16"]) + (ln["l"].lstrip().find(ln["rot16"]) if ln["rot16"] in ln["l"] else 0)
        figs = [t["tok"] for t in ln["toks"] if not re.fullmatch(r"\(?20\d\d\)?", t["tok"]) and t["a0"] >= ini_cifras]
        cab = f"{ln['doc']} p.{ln['p']} l.{ln['i'] + 1}"
        if not figs:
            res["sin cifras de saldo en la línea (solo el año u otro token de la fecha)"] += 1
            print(f"  {cab} · sin cifras de saldo en la línea: tokens aceptados {[t['tok'] for t in nuevos]} · «{re.sub(r' {2,}', ' · ', ln['l'].strip())[:90]}»")
            continue
        t = texto(ln["doc"], ln["p"])
        rx = r"[ \t]*".join(re.escape(x).replace(r"\ ", r"[ \t]?") for x in figs)
        ms = list(re.finditer(rx, t))
        cand = []
        for m in ms:
            ls = t.rfind("\n", 0, m.start()) + 1
            actual = t[ls:m.start()].strip()
            rot, fin = actual, ls
            for _ in range(2):          # hasta dos líneas anteriores (PDFium parte «(a)» en línea propia)
                if ejercicio(rot) is not None:
                    break
                ps = t.rfind("\n", 0, max(0, fin - 1)) + 1
                rot, fin = (t[ps:fin].strip() + " " + rot).strip(), ps
            cand.append((rot, ejercicio(rot)))
        if not cand:
            res["PDFium no da las cifras de la fila en ese orden"] += 1
            print(f"  {cab} · NO ENCONTRADA en PDFium la secuencia {figs[:6]}")
            continue
        ok = [c for c in cand if c[1] == ln["a_rot"]]
        if ok:
            res["el rótulo leído con PDFium lleva la fecha y da el mismo ejercicio"] += 1
            print(f"  {cab} · {len(figs)} cifras · rótulo PDFium «{ok[0][0][:70]}» → {ok[0][1]} = regla del autor ({ln['a_rot']})")
        else:
            res["DISTINTO"] += 1
            print(f"  {cab} · {len(figs)} cifras · DISTINTO: rótulos PDFium {[(c[0][:60], c[1]) for c in cand[:3]]} · regla del autor {ln['a_rot']}")
    print()
    for k, v in sorted(res.items(), key=lambda kv: -kv[1]):
        print(f"{v:4} · {k}")


if __name__ == "__main__":
    main()
