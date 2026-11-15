"""Verificación de cada cifra citada contra los BYTES del PDF original (frente E · F1 · Elis).

Para cada fila de datos/cifras_fuente.csv comprueba, de forma reproducible y sin depender de textos heredados:
  1. que el PDF existe en la ruta declarada y su SHA-256 coincide con datos/fuentes.json;
  2. que la página PDF citada existe (1 = primera página del archivo, no el folio impreso);
  3. tipo «tabla»: que en esa página hay una línea que contiene la etiqueta y que el token numérico de la
     posición declarada es EXACTAMENTE el literal impreso (con su signo: paréntesis, «-», «+», «%», separadores
     del idioma). El valor con signo que se deduce del literal debe coincidir con «valor_publicado».
     Si la etiqueta aparece en varias líneas y no se fija «ocurrencia», todas deben dar el mismo literal;
  4. tipo «tabla»: que la columna corresponde al EJERCICIO declarado («anio»), según «control_anio»:
       dos_columnas  cabecera más próxima con dos ejercicios, en orden descendente: pos −2 = el más reciente, pos −1 = el anterior;
       crecimiento   tabla de variación: el ejercicio es el más reciente de la cabecera;
       max_cabecera  tabla de movimiento con fechas de apertura y cierre en la cabecera: el ejercicio es el de cierre;
       movimientos   el bloque empieza en el saldo anterior más próximo («AS AT JANUARY 1, Y» → Y; «AS AT 12/31/Y» → Y+1);
       saldo         la fecha está en la propia línea («12/31/Y» → Y; «JANUARY 1, Y» → Y−1);
       manual        sin comprobación automática del ejercicio (debe justificarse en «nota»);
  5. tipo «texto»: que el literal (prosa) está en la página, con espacios normalizados.

No hay tolerancias: un redondeo, un signo cambiado, una columna de otro ejercicio o una página inexistente son FALLO.
Solo biblioteca estándar y los binarios pdftotext/pdfinfo (poppler). Uso:

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
MODOS = {"dos_columnas", "crecimiento", "max_cabecera", "movimientos", "saldo", "manual"}

ANIO = re.compile(r"(?<![\d.,/])(20\d\d)(?![\d.,])")
FECHA_CIERRE = re.compile(r"(?:12/31/|31/12/)(20\d\d)")
# saldos: (patrón, desplazamiento del ejercicio respecto del año de la fecha)
SALDO_APERTURA = re.compile(r"(?:JANUARY 1,|January 1,|1ER JANVIER|1er JANVIER|1er janvier)\s*(20\d\d)")
SALDO_CIERRE = re.compile(r"(?:12/31/|31/12/|DECEMBER 31,\s*|December 31,\s*|31 DÉCEMBRE\s*|31 décembre\s*)(20\d\d)")
MARCA_SALDO = re.compile(r"(AS AT|As at|NET CARRYING AMOUNT|VALEUR NETTE COMPTABLE|^\s*AU\s)")


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
        if es_numero(t, idioma):
            out.append(t)
            continue
        partes = t.split(" ")
        cola = []
        while partes:
            cand = partes[-1]
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
    """Lista de (índice de línea, línea) que contienen la etiqueta (o casan con «re:…»)."""
    lineas = texto.splitlines()
    if etiqueta.startswith("re:"):
        rx = re.compile(etiqueta[3:])
        return [(i, l) for i, l in enumerate(lineas) if rx.search(l)]
    return [(i, l) for i, l in enumerate(lineas) if etiqueta in l]


# ------------------------------------------------------------------ ejercicio de la columna
def anios_linea(linea):
    a = FECHA_CIERRE.findall(linea) or ANIO.findall(linea)
    vistos = []
    for x in a:
        if x not in vistos:
            vistos.append(x)
    return [int(x) for x in vistos]


def cabecera(lineas, i, limite=80):
    """Ejercicios de la cabecera más próxima por encima de la línea i, en orden descendente (las tablas de Elis
    presentan el ejercicio corriente primero). Admite cabeceras partidas en dos líneas («2024» encima de «2025 restated*»)."""
    for j in range(i - 1, max(-1, i - limite), -1):
        a = anios_linea(lineas[j])
        if len(a) >= 2:
            return sorted(set(a), reverse=True)
        if len(a) == 1 and j > 0:
            b = set(a) | set(anios_linea(lineas[j - 1]))
            if len(b) >= 2:
                return sorted(b, reverse=True)
    return None


def anios_bloque_cabecera(lineas, i, limite=60, alto=12):
    """Ejercicios del bloque de cabecera de una tabla de movimientos: las líneas situadas encima de la línea de
    unidades («(In millions of euros)» / «(en millions d'euros)») más próxima por encima de i. Sirve para cabeceras
    con la fecha de apertura y la de cierre en líneas distintas."""
    for j in range(i - 1, max(-1, i - limite), -1):
        if re.search(r"\((?:In|in|en) millions", lineas[j]):
            a = set()
            for k in range(max(0, j - alto), j + 1):
                a |= set(anios_linea(lineas[k]))
            return sorted(a, reverse=True) or None
    return None


def anio_de_saldo(linea):
    m = SALDO_APERTURA.search(linea)
    if m:
        return int(m.group(1)) - 1
    m = SALDO_CIERRE.search(linea)
    if m:
        return int(m.group(1))
    return None


def anio_de_bloque(lineas, i, limite=80):
    """Ejercicio del bloque de movimientos al que pertenece la línea i: el que sigue al saldo más próximo por encima."""
    for j in range(i - 1, max(-1, i - limite), -1):
        if MARCA_SALDO.search(lineas[j]):
            a = anio_de_saldo(lineas[j])
            if a is not None:
                return a + 1
    return None


def comprobar_anio(lineas, i, fila):
    modo = (fila.get("control_anio") or "dos_columnas").strip()
    if modo not in MODOS:
        return "FALLO", f"modo de control del ejercicio desconocido: {modo!r}"
    if modo == "manual":
        if not (fila.get("nota") or "").strip():
            return "FALLO", "control manual del ejercicio sin justificación en «nota»"
        return "manual", "ejercicio no comprobable automáticamente; justificado en la nota"
    anio = int(fila["anio"])
    pos = int(fila["pos"])
    if modo == "saldo":
        a = anio_de_saldo(lineas[i])
        return ("OK", f"saldo de {a}") if a == anio else ("FALLO", f"la línea es un saldo de {a}, no de {anio}")
    if modo == "movimientos":
        a = anio_de_bloque(lineas, i)
        return ("OK", f"bloque de {a}") if a == anio else ("FALLO", f"la línea está en el bloque de {a}, no de {anio}")
    if modo == "max_cabecera":
        bloque = anios_bloque_cabecera(lineas, i)
        if not bloque or len(bloque) < 2:
            return "FALLO", "no se localiza la cabecera de apertura y cierre"
        return ("OK", f"cabecera {bloque}") if bloque[0] == anio else ("FALLO", f"el cierre de la tabla es {bloque[0]}, no {anio}")
    cab = cabecera(lineas, i)
    if not cab:
        return "FALLO", "no se localiza la cabecera de ejercicios"
    if modo == "crecimiento":
        return ("OK", f"cabecera {cab}") if cab[0] == anio else ("FALLO", f"la tabla es de {cab[0]}, no de {anio}")
    if pos not in (-2, -1) or len(cab) < 2:
        return "FALLO", f"dos_columnas exige pos −2/−1 y dos ejercicios en la cabecera (pos {pos}, cabecera {cab})"
    esperado = cab[0] if pos == -2 else cab[1]
    return ("OK", f"columna de {esperado}") if esperado == anio else ("FALLO", f"la columna es de {esperado}, no de {anio}")


def comprobar_tabla(pdf, fila, idioma):
    pag = int(fila["pagina"])
    texto = texto_pagina(pdf, pag)
    lineas = texto.splitlines()
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
    for i, l in cand:
        toks = tokens_numericos(l, idioma)
        try:
            tok = toks[pos]
        except IndexError:
            vistos.append({"i": i, "linea": l.strip(), "token": None})
            continue
        vistos.append({"i": i, "linea": re.sub(r"\s{2,}", "  ", l.strip()), "token": tok})
    literales = {v["token"] for v in vistos}
    if len(literales) != 1 or None in literales:
        return {"estado": "FALLO", "motivo": "etiqueta ambigua o sin token en la posición", "lineas": vistos}
    tok = literales.pop()
    if tok != fila["literal"]:
        return {"estado": "FALLO", "motivo": f"literal impreso {tok!r} ≠ declarado {fila['literal']!r}", "lineas": vistos}
    v = valor(tok, idioma)
    if v != Fraction(fila["valor_publicado"]):
        return {"estado": "FALLO", "motivo": f"valor con signo {float(v)} ≠ valor_publicado {fila['valor_publicado']}", "lineas": vistos}
    estados = [comprobar_anio(lineas, x["i"], fila) for x in vistos]
    malos = [m for e, m in estados if e == "FALLO"]
    if malos:
        return {"estado": "FALLO", "motivo": "ejercicio: " + "; ".join(sorted(set(malos))), "lineas": vistos}
    return {"estado": "OK", "linea": vistos[0]["linea"], "token": tok, "control_anio": estados[0][0], "detalle_anio": estados[0][1]}


def comprobar_texto(pdf, fila):
    texto = re.sub(r"\s+", " ", texto_pagina(pdf, int(fila["pagina"]), layout=False))
    lit = re.sub(r"\s+", " ", normalizar(fila["literal"]))
    if lit in texto:
        return {"estado": "OK", "control_anio": "texto"}
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
        p = a.raiz / f.get("archivo", "")
        info = {"archivo": f.get("archivo"), "existe": p.is_file()}
        esperado = (f.get("sha256") or "").strip().lower()
        if not esperado:
            info["motivo"] = "la fuente no declara SHA-256: no se acepta"
        if p.is_file():
            info["sha256"] = sha256_file(p)
            info["sha256_coincide"] = bool(esperado) and info["sha256"] == esperado
            info["paginas"] = num_paginas(p)
            if info["sha256_coincide"]:
                pdfs[slug] = p
        res["fuentes"][slug] = info
    filas = list(csv.DictReader(a.datos.open(encoding="utf-8"), delimiter=";"))
    citadas = set()
    for fila in filas:
        slug = fila["doc"]
        r = {"id": fila["id"], "doc": slug, "pagina": int(fila["pagina"]), "anio": fila["anio"], "literal": fila["literal"]}
        if slug not in pdfs:
            motivo = res["fuentes"].get(slug, {}).get("motivo") or "fuente ausente o con huella distinta"
            r.update(estado="FALLO", motivo=motivo)
        elif not (1 <= int(fila["pagina"]) <= res["fuentes"][slug]["paginas"]):
            r.update(estado="FALLO", motivo="página inexistente en el PDF")
        else:
            idioma = fuentes[slug]["idioma"]
            r.update(comprobar_texto(pdfs[slug], fila) if fila["tipo"] == "texto" else comprobar_tabla(pdfs[slug], fila, idioma))
            citadas.add((slug, int(fila["pagina"])))
        res["cifras"].append(r)
    ok = sum(1 for r in res["cifras"] if r["estado"] == "OK")
    por_control = {}
    for r in res["cifras"]:
        if r["estado"] == "OK":
            por_control[r.get("control_anio")] = por_control.get(r.get("control_anio"), 0) + 1
    res["resumen"] = {"filas": len(filas), "ok": ok, "fallos": len(filas) - ok,
                      "ejercicio_comprobado_automaticamente": por_control.get("OK", 0),
                      "ejercicio_control_manual_justificado": por_control.get("manual", 0),
                      "texto": por_control.get("texto", 0),
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
