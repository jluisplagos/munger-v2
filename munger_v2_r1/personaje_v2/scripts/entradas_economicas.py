#!/usr/bin/env python3
"""Instantánea de las entradas ECONÓMICAS de una valoración (encargo 4.12 §5). Solo lee.

Qué entra: las entradas materiales de la valoración y de la lectura del precio (relación independiente de la V6.3:
v6/scripts/relacion_entradas_materiales.py, 58 entradas, con los rangos de la Historia expandidos) y, en un libro V6.4, las celdas
de entrada de «Configuración V6.4» (configuracion_economica.TRAZA_CELDAS). Qué no entra: los textos de juicio (narrativas, C104,
tesis, Observaciones), las predicciones, la evidencia de Control maestro y las celdas de trazabilidad de la configuración: un
cambio en ellos es editorial y no obliga a repetir las valoraciones. Un cambio en una entrada económica sí.

(4.12, revisión interna R1) En un libro V6.4 entran además las filas de la Historia que alimentan las bases de «Configuración V6.4» y
que no están en la relación de la V6.3: la fila 13 (adquisiciones netas), que entra en D_hist y F_hist y, con ellas, en f y f_fija
(ADICIONALES_V64). Versión de la relación: «4.12+H13». Una instantánea guardada con la relación anterior («4.12», sin campo
`version`) se compara con esa misma relación, y su fila 13 con la del libro de la variante «activa» (copia recalculada en el paso 10).

Funciones:
  instantanea(libro, version)     → {"celdas": {"Hoja!REF": valor}, "tipos": {...}, "ids": {...}, "huella": sha256, "n": N, "version": …}
  comparar(guardada, libro, libro_activa) → (diferencias, instantánea del libro, nota): con la relación con que se guardó
  vector_escenarios(res, precio)  → V MALO/NORMAL/BUENO, probabilidades, ponderado, precio de Sí, precio y zona
  huella_configuracion(conf)      → sha256 de las celdas económicas de la configuración (sin trazabilidad, naturaleza ni protocolo)
  diferencias(a, b)               → celdas cuyo valor cambió entre dos instantáneas
Uso: entradas_economicas.py LIBRO.xlsx   (imprime la huella y el número de celdas)
"""
import hashlib
import json
import os
import re
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import configuracion_economica as CE  # noqa: E402
from v63_xml import LibroV63, NS  # noqa: E402

RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
V63_SCRIPTS = os.path.join(RAIZ, "v6", "scripts")


def relacion():
    """Las 58 entradas materiales de la V6.3 (relación independiente de la 4.7: traza estática y activación empírica)."""
    if V63_SCRIPTS not in sys.path:
        sys.path.append(V63_SCRIPTS)
    import relacion_entradas_materiales as R  # noqa: E402
    return R.ENTRADAS


# (4.12, revisión interna R1) entradas de la Historia que solo usa la V6.4 (bases de «Configuración V6.4» B55 y B59: D_hist y F_hist, y
# con ellas f = D_hist ÷ (D_hist − Rh) de SR1/SR2 y f_fija de SRF). Se comprobó con una traza de precedentes de B54:B63 que es la única
# fila de la Historia fuera de la relación de la V6.3.
ADICIONALES_V64 = [{"id": "h_adquisiciones", "celda": "Historia!C13:L13", "tipo": "dato",
                    "motores": "B (V6.4 experimental: D_hist y F_hist de P-M1)", "cond": "modo experimental de la V6.4 (bases de «Configuración V6.4»)",
                    "periodo": "las columnas H:L (cinco últimos ejercicios) entran en las bases"}]
RELACION_ACTUAL = "4.12+H13"
RELACION_4_12 = "4.12"


def relacion_v64():
    """La relación de la V6.3 y las entradas adicionales de la V6.4."""
    return list(relacion()) + ADICIONALES_V64


def _expandir(celda):
    """«Historia!C6:L6» → [(Historia, C6), …, (Historia, L6)]; «'Control maestro'!H4» → [(Control maestro, H4)]."""
    hoja, rango = celda.rsplit("!", 1)
    hoja = hoja.strip("'")
    m = re.fullmatch(r"([A-Z]+)(\d+):([A-Z]+)(\d+)", rango)
    if not m:
        return [(hoja, rango)]
    c0, f0, c1, f1 = m.group(1), int(m.group(2)), m.group(3), int(m.group(4))
    if len(c0) != 1 or len(c1) != 1:
        raise ValueError(f"rango no admitido: {celda}")
    return [(hoja, f"{chr(c)}{f}") for f in range(f0, f1 + 1) for c in range(ord(c0), ord(c1) + 1)]


class _Lector:
    """Valores tal como están en el XML, con las cadenas compartidas resueltas (LibroV63.leer devuelve el índice)."""

    def __init__(self, libro):
        from lxml import etree
        self.lb = LibroV63(libro)
        self.ss = []
        dat = self.lb._datos.get("xl/sharedStrings.xml")
        if dat:
            for si in etree.fromstring(dat).findall(f"{{{NS}}}si"):
                self.ss.append("".join(si.itertext()))

    def leer(self, hoja, ref):
        c = self.lb._celda(hoja, ref)
        if c is not None and c.get("t") == "s" and c.find(f"{{{NS}}}f") is None:
            v = c.find(f"{{{NS}}}v")
            if v is not None and v.text is not None and v.text.isdigit() and int(v.text) < len(self.ss):
                return self.ss[int(v.text)]
        x = self.lb.leer(hoja, ref)
        return list(x) if isinstance(x, tuple) else x


def _norm(v):
    if isinstance(v, float) and v.is_integer():
        return int(v)
    return v


def instantanea(libro, version=RELACION_ACTUAL):
    lec = _Lector(libro)
    hojas = set(lec.lb.hojas())
    celdas, tipos, ids = {}, {}, {}
    rel = relacion_v64() if (CE.HOJA in hojas and version != RELACION_4_12) else relacion()
    for e in rel:
        for hoja, ref in _expandir(e["celda"]):
            if hoja not in hojas:
                continue
            k = f"{hoja}!{ref}"
            celdas[k] = _norm(lec.leer(hoja, ref))
            tipos[k] = e["tipo"]
            ids[k] = e["id"]
    if CE.HOJA in hojas:
        for clave, refs in CE.TRAZA_CELDAS.items():
            for ref in refs:
                if ref in CE.CELDAS_METADATOS:
                    continue  # fuente, período, perímetro…: metadatos de trazabilidad (editoriales)
                k = f"{CE.HOJA}!{ref}"
                v = _norm(lec.leer(CE.HOJA, ref))
                if v is None and ref in CE.SOLO_V641:
                    continue  # (4.13 §7) celdas de la V6.4.1 vacías = V6.4: no cambian la huella de los libros anteriores
                celdas[k] = v
                tipos[k] = "configuracion"
                ids[k] = clave
    if "Historia" in hojas and "PERÍMETRO F1 DE LA REINVERSIÓN" in str(lec.leer("Historia", "A84") or ""):
        # (revisión V6.3.1, V631-3) libro V6.3.1 F1: el perímetro (C85) y las series D&A de derechos de uso y PPA (C86:L87) mueven f, el ancla
        # y el terminal: entran en la huella y en el universo de verificacion_entradas.py (los libros V6.3 y V6.4 no cambian de huella)
        for ref, tipo, ident in ([("C85", "configuracion", "F1.perimetro_reinversion")]
                                 + [(f"{c}{f}", "dato", n) for f, n in ((86, "F1.da_rou"), (87, "F1.da_ppa")) for c in "CDEFGHIJKL"]):
            k = f"Historia!{ref}"
            celdas[k] = _norm(lec.leer("Historia", ref))
            tipos[k] = tipo
            ids[k] = ident
    texto = json.dumps(sorted(celdas.items()), ensure_ascii=False, default=str, separators=(",", ":"))
    return {"celdas": celdas, "tipos": tipos, "ids": ids, "n": len(celdas), "huella": hashlib.sha256(texto.encode("utf-8")).hexdigest(),
            "version": version if CE.HOJA in hojas else RELACION_4_12,
            "nota": "entradas materiales de la valoración y de la lectura del precio (relación independiente de la V6.3) y, en la V6.4, las de «Configuración V6.4» sin sus metadatos; "
                    "los textos de juicio, las predicciones, la evidencia y la trazabilidad no entran (son editoriales)"}


def vector_escenarios(res, precio):
    v = (res or {}).get("valores") or {}
    return {"V": [v.get("B78"), v.get("C78"), v.get("D78")], "probabilidades": (res or {}).get("probabilidades"), "ponderado": v.get("C83"),
            "precio_si": (precio or {}).get("precio_si"), "precio": (precio or {}).get("precio"), "zona": (precio or {}).get("zona")}


def huella_configuracion(conf):
    """Huella de la parte económica de la configuración: las celdas de entrada que escribe en el libro (sin la trazabilidad)."""
    if not conf:
        return None
    c = CE.celdas(conf)
    econ = {f"{CE.HOJA}!{r}": c.get(f"{CE.HOJA}!{r}") for refs in CE.TRAZA_CELDAS.values() for r in refs if r not in CE.CELDAS_METADATOS
            and not (r in CE.SOLO_V641 and c.get(f"{CE.HOJA}!{r}") is None)}  # (4.13 §7) sin perímetro, la huella de antes
    return hashlib.sha256(json.dumps(sorted(econ.items()), ensure_ascii=False, default=str).encode("utf-8")).hexdigest()


def _adicionales(libro):
    """{celda: valor} de ADICIONALES_V64 en un libro V6.4 ({} si el libro no es V6.4)."""
    lec = _Lector(libro)
    if CE.HOJA not in set(lec.lb.hojas()):
        return {}
    return {f"{h}!{r}": _norm(lec.leer(h, r)) for e in ADICIONALES_V64 for h, r in _expandir(e["celda"])}


def comparar(guardada, libro, libro_activa=None):
    """(4.12, revisión interna R1) Compara la instantánea que guardaron las variantes con la del libro, con la relación con que se guardó.
    Con la relación anterior («4.12»), las entradas adicionales de la V6.4 se comparan además con las del libro de la variante «activa»
    (la copia recalculada del libro evaluado en el paso 10); si falta ese libro, no se pueden acreditar y cuenta como diferencia.
    Devuelve (diferencias, instantánea del libro, nota)."""
    ver = (guardada or {}).get("version") or RELACION_4_12
    inst = instantanea(libro, version=ver)
    dif = diferencias(guardada, inst) if (guardada or {}).get("huella") != inst["huella"] else []
    nota = None
    if ver == RELACION_4_12:
        nuevas = _adicionales(libro)
        if nuevas:
            if libro_activa and os.path.exists(libro_activa):
                previas = _adicionales(libro_activa)
                dif += sorted(k for k in set(nuevas) | set(previas) if nuevas.get(k) != previas.get(k))
                nota = "instantánea guardada con la relación «4.12»: la fila 13 de la Historia se comparó con la del libro de la variante «activa»"
            else:
                dif.append("Historia!C13:L13 (sin acreditar: instantánea de la relación «4.12» y sin el libro de la variante «activa»)")
                nota = "instantánea guardada con la relación «4.12» y sin el libro de la variante «activa»: la fila 13 de la Historia no se puede acreditar"
    return dif, inst, nota


def diferencias(a, b):
    ca, cb = (a or {}).get("celdas") or {}, (b or {}).get("celdas") or {}
    return sorted(k for k in set(ca) | set(cb) if ca.get(k) != cb.get(k))


def iguales(x, y, tol=1e-9):
    if isinstance(x, (int, float)) and isinstance(y, (int, float)) and not isinstance(x, bool) and not isinstance(y, bool):
        return abs(x - y) <= tol * max(1.0, abs(y))
    if isinstance(x, list) and isinstance(y, list):
        return len(x) == len(y) and all(iguales(a, b, tol) for a, b in zip(x, y))
    return x == y


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(2)
    i = instantanea(sys.argv[1])
    print(f"{i['n']} entradas económicas · huella {i['huella']}")
