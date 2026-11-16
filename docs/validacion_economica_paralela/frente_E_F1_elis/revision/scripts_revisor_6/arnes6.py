"""Arnés común de los scripts de la revisión n.º 6 (frente E · F1 · Elis). No modifica nada del autor.

Dos formas de ejecutar el verificador de una versión del autor (una carpeta frente_E_F1_elis de un worktree):

  oficial(...)   ejecuta scripts/verificar_cifras.py de esa versión como proceso aparte sobre un CSV temporal, igual que
                 lo ejecuta el autor, y devuelve su código de salida y su JSON. Es la vía de los contraejemplos.
  Modulo(...)    carga ese mismo archivo como módulo y llama a su función comprobar_tabla, que es la que usa la ejecución
                 oficial para cada fila de tabla (incluye la página anterior y la edición de la columna). La línea se fija
                 con una etiqueta «re:^…$» que casa la línea entera y con su número de ocurrencia. La equivalencia con la
                 ejecución oficial se comprueba en barrido_6.py sobre todas las filas reales de cada versión.
"""
import csv
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
CAMPOS = ["id", "anio", "concepto", "doc", "pagina", "tipo", "etiqueta", "ocurrencia", "pos", "literal", "valor_publicado", "unidad",
          "perimetro", "edicion", "nota", "control_anio"]
DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")
DIM5 = DIMS[1:]


def leer_csv(carpeta_autor):
    with (Path(carpeta_autor) / "datos" / "cifras_fuente.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def fila(idf, **c):
    """Fila de tabla con los valores por defecto de una cifra del grupo en millones de euros, de dos columnas."""
    f = {k: "" for k in CAMPOS}
    f.update(id=idf, tipo="tabla", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR", control_anio="dos_columnas",
             concepto="caso del revisor n.º 6")
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


def resumen(reg):
    """Estado de la fila y las dimensiones que no están en OK, con su motivo."""
    e = estados(reg)
    partes = [f"{k} {e[k]}: {reg['dimensiones'][k].get('detalle', '')}" for k in DIMS if e[k] not in ("OK", "NO_APLICA")]
    return reg["estado"] + (" · " + " · ".join(partes) if partes else " en las seis dimensiones")


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
        """Registro de comprobar_tabla para una fila (dimensiones y estado), como en la ejecución oficial."""
        doc = f["doc"]
        r = self.m.comprobar_tabla(self.pdf(doc), f, self.fuentes[doc]["idioma"], self.fuentes[doc], self.ejercicios)
        r["estado"] = self.m.estado_fila(r["dimensiones"])
        return r


def etiqueta_de_linea(lineas, i):
    """(etiqueta «re:^…$» que casa la línea i entera, ocurrencia) para fijar esa línea en una fila del CSV."""
    iguales = [k for k, l in enumerate(lineas) if l == lineas[i]]
    return "re:^" + re.escape(lineas[i]) + "$", iguales.index(i) + 1


def edicion_que_exige_la_regla(anio, E, ejercicios, modo="dos_columnas"):
    """«vigente» si la publicación E es la que la regla de la Historia exige para ese ejercicio; si no, «anterior»."""
    regla = anio if modo in ("crecimiento", "max_cabecera") else (anio + 1 if (anio + 1) in ejercicios else anio)
    return "vigente" if regla == E else "anterior"
