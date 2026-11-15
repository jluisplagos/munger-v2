"""Verificación de cada cifra citada contra los BYTES del PDF original (frente E · F1 · Elis).

Para cada fila de datos/cifras_fuente.csv comprueba, de forma reproducible y sin depender de textos
heredados:
  1. que el PDF existe en la ruta declarada y su SHA-256 coincide con datos/fuentes.json;
  2. que la página PDF citada existe (1 = primera página del archivo, no el folio impreso);
  3. tipo «tabla»: que en esa página hay una línea que contiene la etiqueta y que el token numérico de la
     posición declarada es EXACTAMENTE el literal impreso (con su signo: paréntesis, «-», «+», «%», separadores
     del idioma). El valor con signo que se deduce del literal debe coincidir con «valor_publicado»;
     si la etiqueta aparece en varias líneas y no se fija «ocurrencia», todas deben dar el mismo literal;
  4. tipo «texto»: que el literal (prosa) está en la página, con espacios normalizados.

No hay tolerancias: un redondeo, un signo cambiado o una página inexistente son FALLO.
Solo biblioteca estándar y el binario pdftotext (poppler). Uso:

  python3 -I verificar_cifras.py --raiz <ruta>/munger_v2_r1 --datos ../datos/cifras_fuente.csv \
      --fuentes ../datos/fuentes.json --salida ../resultados/verificacion_cifras.json \
      [--exportar-paginas ../evidencias/paginas]
"""
import argparse
import csv
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from fractions import Fraction
from pathlib import Path

NUM_EN = re.compile(r"^(?P<pre>[+\-–−]\s?)?(?P<par>\()?(?P<sig>[+\-–−])?(?P<num>\d{1,3}(?:,\d{3})*(?:\.\d+)?|\d+(?:\.\d+)?)(?P<cpar>\))?(?P<pct>\s?%)?(?P<cpar2>\))?$")
NUM_FR = re.compile(r"^(?P<pre>[+\-–−]\s?)?(?P<par>\()?(?P<sig>[+\-–−])?(?P<num>\d{1,3}(?: \d{3})*(?:,\d+)?|\d+(?:,\d+)?)(?P<cpar>\))?(?P<pct>\s?%)?(?P<cpar2>\))?$")
PLACEHOLDER = {"-", "–", "—", "−"}


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def normalizar(s):
    s = unicodedata.normalize("NFKC", s)
    return s.replace("’", "'").replace("‘", "'")


_cache = {}


def texto_pagina(pdf, n, layout=True):
    clave = (str(pdf), n, layout)
    if clave not in _cache:
        args = ["pdftotext", "-q", "-f", str(n), "-l", str(n)] + (["-layout"] if layout else []) + [str(pdf), "-"]
        r = subprocess.run(args, capture_output=True, check=True)
        _cache[clave] = normalizar(r.stdout.decode("utf-8", errors="replace"))
    return _cache[clave]


def num_paginas(pdf):
    r = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, check=True, text=True)
    m = re.search(r"^Pages:\s+(\d+)", r.stdout, re.M)
    return int(m.group(1))


def trozos(linea):
    return [t.strip() for t in re.split(r"\s{2,}", linea.strip()) if t.strip()]


def es_numero(tok, idioma):
    rx = NUM_FR if idioma == "fr" else NUM_EN
    return tok in PLACEHOLDER or bool(rx.match(tok))


def tokens_numericos(linea, idioma):
    """Tokens numéricos de una línea en orden (los marcadores «-» cuentan como posición, sin valor)."""
    out = []
    for t in trozos(linea):
        # Un trozo puede llevar la etiqueta pegada al primer número por un solo espacio: separar la cola numérica.
        if es_numero(t, idioma):
            out.append(t)
            continue
        partes = t.split(" ")
        cola = []
        while partes:
            cand = partes[-1]
            # en francés el separador de miles es un espacio: intentar unir con el anterior
            if idioma == "fr" and len(partes) >= 2 and re.fullmatch(r"\(?\d{1,3}", partes[-2]) and re.fullmatch(r"\d{3}(?:,\d+)?\)?%?", cand):
                unido = partes[-2] + " " + cand
                if es_numero(unido, idioma):
                    cola.insert(0, unido)
                    partes = partes[:-2]
                    continue
            if es_numero(cand, idioma) and cand not in PLACEHOLDER:
                cola.insert(0, cand)
                partes = partes[:-1]
            else:
                break
        out.extend(cola)
    return out


def valor(tok, idioma):
    """Fraction con signo del literal impreso; None para marcadores. Los porcentajes se devuelven en puntos (3.8 por «+3.8%»)."""
    if tok in PLACEHOLDER:
        return None
    rx = NUM_FR if idioma == "fr" else NUM_EN
    m = rx.match(tok)
    if not m:
        raise ValueError(f"no numérico: {tok!r}")
    num = m.group("num")
    num = num.replace(" ", "").replace(",", ".") if idioma == "fr" else num.replace(",", "")
    v = Fraction(num)
    neg = bool(m.group("par")) or (m.group("pre") or "").strip() in {"-", "–", "−"} or (m.group("sig") or "") in {"-", "–", "−"}
    return -v if neg else v


def lineas_con(texto, etiqueta):
    if etiqueta.startswith("re:"):
        rx = re.compile(etiqueta[3:])
        return [l for l in texto.splitlines() if rx.search(l)]
    return [l for l in texto.splitlines() if etiqueta in l]


def comprobar_tabla(pdf, fila, idioma):
    pag = int(fila["pagina"])
    texto = texto_pagina(pdf, pag)
    cand = lineas_con(texto, fila["etiqueta"])
    if not cand:
        return {"estado": "FALLO", "motivo": "etiqueta no encontrada en la página"}
    occ = int(fila["ocurrencia"] or 0)
    if occ:
        if occ > len(cand):
            return {"estado": "FALLO", "motivo": f"solo hay {len(cand)} líneas con la etiqueta"}
        cand = [cand[occ - 1]]
    pos = int(fila["pos"])
    vistos = []
    for l in cand:
        toks = tokens_numericos(l, idioma)
        try:
            tok = toks[pos]
        except IndexError:
            vistos.append({"linea": l.strip(), "token": None})
            continue
        vistos.append({"linea": re.sub(r"\s{2,}", "  ", l.strip()), "token": tok})
    literales = {v["token"] for v in vistos}
    if len(literales) != 1 or None in literales:
        return {"estado": "FALLO", "motivo": "etiqueta ambigua o sin token en la posición", "lineas": vistos}
    tok = literales.pop()
    if tok != fila["literal"]:
        return {"estado": "FALLO", "motivo": f"literal impreso {tok!r} ≠ declarado {fila['literal']!r}", "lineas": vistos}
    v = valor(tok, idioma)
    if v != Fraction(fila["valor_publicado"]):
        return {"estado": "FALLO", "motivo": f"valor con signo {float(v)} ≠ valor_publicado {fila['valor_publicado']}", "lineas": vistos}
    return {"estado": "OK", "linea": vistos[0]["linea"], "token": tok}


def comprobar_texto(pdf, fila):
    texto = re.sub(r"\s+", " ", texto_pagina(pdf, int(fila["pagina"]), layout=False))
    lit = re.sub(r"\s+", " ", normalizar(fila["literal"]))
    if lit in texto:
        return {"estado": "OK"}
    return {"estado": "FALLO", "motivo": "literal no encontrado en la página (modo texto)"}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--raiz", required=True, type=Path, help="carpeta munger_v2_r1 materializada (con binarios)")
    ap.add_argument("--datos", required=True, type=Path)
    ap.add_argument("--fuentes", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--exportar-paginas", type=Path, help="escribe el texto de cada página citada, con cabecera de huella")
    a = ap.parse_args()
    fuentes = json.loads(a.fuentes.read_text(encoding="utf-8"))["fuentes"]
    res = {"fuentes": {}, "cifras": [], "resumen": {}}
    pdfs = {}
    for slug, f in fuentes.items():
        p = a.raiz / f["archivo"]
        info = {"archivo": f["archivo"], "existe": p.is_file()}
        if p.is_file():
            info["sha256"] = sha256_file(p)
            info["sha256_coincide"] = info["sha256"] == f["sha256"]
            info["paginas"] = num_paginas(p)
            if info["sha256_coincide"]:
                pdfs[slug] = p
        res["fuentes"][slug] = info
    filas = list(csv.DictReader(a.datos.open(encoding="utf-8"), delimiter=";"))
    citadas = set()
    for fila in filas:
        slug = fila["doc"]
        r = {"id": fila["id"], "doc": slug, "pagina": int(fila["pagina"]), "literal": fila["literal"]}
        if slug not in pdfs:
            r.update(estado="FALLO", motivo="fuente ausente o con huella distinta")
        elif not (1 <= int(fila["pagina"]) <= res["fuentes"][slug]["paginas"]):
            r.update(estado="FALLO", motivo="página inexistente en el PDF")
        else:
            idioma = fuentes[slug]["idioma"]
            r.update(comprobar_texto(pdfs[slug], fila) if fila["tipo"] == "texto" else comprobar_tabla(pdfs[slug], fila, idioma))
            citadas.add((slug, int(fila["pagina"])))
        res["cifras"].append(r)
    ok = sum(1 for r in res["cifras"] if r["estado"] == "OK")
    res["resumen"] = {"filas": len(filas), "ok": ok, "fallos": len(filas) - ok,
                      "fuentes_verificadas": sum(1 for v in res["fuentes"].values() if v.get("sha256_coincide")),
                      "fuentes_declaradas": len(fuentes)}
    if a.exportar_paginas:
        a.exportar_paginas.mkdir(parents=True, exist_ok=True)
        for slug, n in sorted(citadas):
            cab = (f"# Fuente: {fuentes[slug]['archivo']}\n# SHA-256: {res['fuentes'][slug]['sha256']}\n"
                   f"# Página PDF: {n} (texto extraído con pdftotext -layout; la evidencia primaria es el PDF)\n\n")
            (a.exportar_paginas / f"{slug}_p{n:03d}.txt").write_text(cab + texto_pagina(pdfs[slug], n), encoding="utf-8")
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(res, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(res["resumen"], ensure_ascii=False))
    for r in res["cifras"]:
        if r["estado"] != "OK":
            print("FALLO", r["id"], r.get("motivo"), json.dumps(r.get("lineas", ""), ensure_ascii=False)[:400])
    return 0 if res["resumen"]["fallos"] == 0 and res["resumen"]["fuentes_verificadas"] == len(fuentes) else 1


if __name__ == "__main__":
    sys.exit(main())
