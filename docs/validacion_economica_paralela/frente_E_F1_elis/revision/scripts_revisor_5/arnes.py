"""Arnés común de los scripts de la revisión n.º 5 (frente E · F1 · Elis). No modifica nada del autor.

Dos formas de ejecutar el verificador de una versión del autor (una carpeta frente_E_F1_elis de un worktree):

  oficial(...)   ejecuta scripts/verificar_cifras.py de esa versión como proceso aparte sobre un CSV temporal, igual que
                 lo ejecuta el autor, y devuelve su código de salida y su JSON. Es la vía de todos los contraejemplos.
  Modulo(...)    carga ese mismo archivo como módulo para llamar a sus funciones por dimensión sobre muchas líneas (barridos).
                 Su equivalencia con la vía oficial se comprueba en barrido_tablas.py sobre todas las filas reales.

Los CSV temporales se escriben en una carpeta temporal propia de cada llamada.
"""
import csv
import importlib.util
import json
import subprocess
import sys
import tempfile
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
CAMPOS = ["id", "anio", "concepto", "doc", "pagina", "tipo", "etiqueta", "ocurrencia", "pos", "literal", "valor_publicado", "unidad",
          "perimetro", "edicion", "nota", "control_anio"]
DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")


def leer_csv(carpeta_autor):
    with (Path(carpeta_autor) / "datos" / "cifras_fuente.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def fila(idf, **c):
    """Fila de tabla con los valores por defecto de una cifra del grupo en millones de euros, de dos columnas."""
    f = {k: "" for k in CAMPOS}
    f.update(id=idf, tipo="tabla", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR", control_anio="dos_columnas",
             concepto="caso del revisor n.º 5")
    f.update({k: str(v) for k, v in c.items()})
    return f


def oficial(carpeta_autor, raiz, filas):
    """(código de salida, {id: registro}) de verificar_cifras.py de esa versión sobre esas filas."""
    carpeta_autor = Path(carpeta_autor)
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as f:
            w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
            w.writeheader()
            w.writerows(filas)
        r = subprocess.run([sys.executable, "-I", str(carpeta_autor / "scripts" / "verificar_cifras.py"), "--raiz", str(raiz), "--datos",
                            str(d / "c.csv"), "--fuentes", str(carpeta_autor / "datos" / "fuentes.json"), "--salida", str(d / "v.json")],
                           capture_output=True, text=True)
        if not (d / "v.json").is_file():
            raise RuntimeError(r.stderr[-800:])
        v = json.loads((d / "v.json").read_text(encoding="utf-8"))
    return r.returncode, {x["id"]: x for x in v["cifras"]}


def estados(reg):
    return {k: reg["dimensiones"][k]["estado"] for k in DIMS}


def resumen(reg, dims=("ejercicio", "unidad", "perimetro")):
    """Estado de la fila y, de las dimensiones pedidas, las que no están en OK con su motivo."""
    e = estados(reg)
    partes = [f"{k}={e[k]}" for k in DIMS if e[k] not in ("OK", "NO_APLICA")]
    return reg["estado"] + (" (" + ", ".join(partes) + ")" if partes else " en las seis dimensiones")


def motivo(reg, dim):
    return reg["dimensiones"][dim].get("detalle", "")


class Modulo:
    """verificar_cifras.py de una versión, cargado como módulo, con sus fuentes."""

    def __init__(self, carpeta_autor, raiz, nombre):
        carpeta_autor = Path(carpeta_autor)
        spec = importlib.util.spec_from_file_location(nombre, carpeta_autor / "scripts" / "verificar_cifras.py")
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        self.fuentes = json.loads((carpeta_autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
        self.ejercicios = {f["ejercicio"] for f in self.fuentes.values() if isinstance(f.get("ejercicio"), int)}
        self.raiz = Path(raiz)

    def pdf(self, doc):
        return self.raiz / self.fuentes[doc]["archivo"]

    def texto(self, doc, pagina):
        return self.m.texto_pagina(self.pdf(doc), pagina)

    def paginas(self, doc):
        return self.m.num_paginas(self.pdf(doc))

    def tabla(self, f):
        """Registro de comprobar_tabla para una fila (dimensiones y estado)."""
        doc = f["doc"]
        r = self.m.comprobar_tabla(self.pdf(doc), f, self.fuentes[doc]["idioma"], self.fuentes[doc], self.ejercicios)
        r["estado"] = self.m.estado_fila(r["dimensiones"])
        return r

    def dimensiones(self, doc, lineas, texto, i, f):
        """Las cinco dimensiones que siguen al literal para la línea i de una página, sin buscar la etiqueta: lo mismo
        que hace comprobar_tabla una vez localizada la línea y comprobado el literal."""
        m, idioma, pos = self.m, self.fuentes[doc]["idioma"], int(f["pos"])
        d = {"ejercicio": m.comprobar_anio(lineas, i, f, idioma), "columna": m.comprobar_columna(lineas, i, f, pos, idioma),
             "unidad": m.comprobar_unidad(lineas, i, f, idioma), "perimetro": m.comprobar_perimetro(lineas, i, f, pos, idioma)}
        e, det, _ = m.comprobar_edicion(texto, f, self.fuentes[doc], self.ejercicios)
        d["edicion"] = (e, det)
        return d
