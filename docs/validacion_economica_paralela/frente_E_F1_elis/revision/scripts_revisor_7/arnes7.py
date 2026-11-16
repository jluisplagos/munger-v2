"""Arnés de la revisión n.º 7 (frente E · F1 · Elis). No modifica nada del autor: carga en memoria el verificador de una
versión (una carpeta frente_E_F1_elis de un worktree) y, si se pide, una VARIANTE: el mismo módulo con una sola pieza
cambiada en memoria, para medir lo que cuesta o lo que aporta cada una de las tres decisiones de C14:

  al3             ALINEADA = 3 (el umbral que proponía la revisión n.º 6 en R3; C14 usa 5,5);
  sin_grupos      sin la regla de grupos de columnas en el perímetro (grupo_de_columnas → None);
  ajena_en_orden  la regla de cabecera ajena de C9 aplicada también cuando la columna se asigna por orden (la propuesta de
                  la revisión n.º 6 en R1, que C14 no sigue);
  sin_numerado    sin el encabezado numerado como título (es_encabezado_numerado → False), para aislar el efecto de R2;
  sin_corto       sin el título corto de tabla (titulo_corto_de_tabla → None), para aislar el efecto de R4.

Dos formas de ejecutar: Version.tabla(fila) llama a comprobar_tabla, la función que la ejecución oficial usa para cada fila
de tabla; oficial(...) ejecuta verificar_cifras.py como proceso aparte sobre un CSV temporal, como lo ejecuta el autor (solo
para versiones sin variante). La equivalencia de las dos se comprueba en barrido_7.py sobre las filas reales.
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
VARIANTES = ("al3", "sin_grupos", "ajena_en_orden", "sin_numerado", "sin_corto")


def _ajena_en_orden(m):
    def columna_de_token(lineas, i, pos, idioma, claves, maxdist=14, cabeceras_ajenas=False, orden_alineado=False):
        sp = m.spans_numericos(lineas[i], idioma)
        if not sp or not -len(sp) <= pos < len(sp):
            return None, None, "sin token en la posición"
        zona = m.zona_de_cabecera(lineas, i, idioma)
        if not zona:
            return None, None, "no se localiza la cabecera de la tabla"
        cols = m.columnas_de_cabecera(lineas, zona, claves)
        if not cols:
            return None, None, "la cabecera no tiene columnas reconocibles"
        idx = pos % len(sp)
        clave, txt, metodo, _, d = m.asignar_columna(sp, cols, idx, maxdist, orden_alineado)
        if clave is None:
            return clave, txt, metodo
        a, b = sp[idx]
        ajena = m.palabra_de_cabecera_mas_cercana(lineas, zona, claves, (a + b) / 2) if cabeceras_ajenas else None
        if ajena is not None and ajena[0] < d:
            return clave, txt, f"ajena:{d:g}:{ajena[1]}"
        return clave, txt, metodo
    return columna_de_token


class Version:
    """verificar_cifras.py de una versión, cargado como módulo, con sus fuentes y, si se pide, una variante en memoria."""

    def __init__(self, carpeta_autor, raiz, nombre, variante=None):
        self.carpeta = Path(carpeta_autor)
        spec = importlib.util.spec_from_file_location("verificador_" + re.sub(r"\W", "_", nombre + "_" + (variante or "")),
                                                      self.carpeta / "scripts" / "verificar_cifras.py")
        self.m = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.m)
        m = self.m
        if variante == "al3":
            m.ALINEADA = 3
        elif variante == "sin_grupos":
            m.grupo_de_columnas = lambda *a, **k: None
        elif variante == "ajena_en_orden":
            m.columna_de_token = _ajena_en_orden(m)
        elif variante == "sin_numerado":
            m.es_encabezado_numerado = lambda *a, **k: False
        elif variante == "sin_corto":
            m.titulo_corto_de_tabla = lambda *a, **k: None
        elif variante is not None:
            raise ValueError(variante)
        self.nombre, self.variante = nombre, variante
        self.fuentes = json.loads((self.carpeta / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
        self.ejercicios = {f["ejercicio"] for f in self.fuentes.values() if isinstance(f.get("ejercicio"), int)}
        self.raiz = Path(raiz)

    def pdf(self, doc):
        return self.raiz / self.fuentes[doc]["archivo"]

    def lineas(self, doc, pagina):
        return self.m.texto_pagina(self.pdf(doc), pagina).splitlines()

    def paginas(self, doc):
        return self.m.num_paginas(self.pdf(doc))

    def tabla(self, f):
        doc = f["doc"]
        r = self.m.comprobar_tabla(self.pdf(doc), f, self.fuentes[doc]["idioma"], self.fuentes[doc], self.ejercicios)
        r["estado"] = self.m.estado_fila(r["dimensiones"])
        return r


def leer_csv(carpeta_autor):
    with (Path(carpeta_autor) / "datos" / "cifras_fuente.csv").open(encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter=";"))


def fila(idf, **c):
    """Fila de tabla declarada como una cifra del grupo en millones de euros, de dos columnas y de la edición vigente."""
    f = {k: "" for k in CAMPOS}
    f.update(id=idf, tipo="tabla", ocurrencia="0", perimetro=GRUPO, edicion="vigente", unidad="mm EUR", control_anio="dos_columnas",
             concepto="caso de la revisión n.º 7")
    f.update({k: str(v) for k, v in c.items()})
    return f


def etiqueta_de_linea(lineas, i):
    """Etiqueta «re:^…$» que casa la línea i entera y su número de ocurrencia en la página."""
    iguales = [k for k, l in enumerate(lineas) if l == lineas[i]]
    return "re:^" + re.escape(lineas[i]) + "$", iguales.index(i) + 1


def edicion_de_la_regla(anio, E, ejercicios):
    """«vigente» si la publicación E es la que exige la regla de la Historia para ese ejercicio en una tabla de dos
    ejercicios (la del ejercicio siguiente, si está entre las fuentes); si no, «anterior»."""
    regla = anio + 1 if (anio + 1) in ejercicios else anio
    return "vigente" if regla == E else "anterior"


def oficial(carpeta_autor, raiz, filas):
    """(código de salida, {id: registro}) de verificar_cifras.py de esa versión, como proceso aparte, sobre esas filas."""
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


def resumen(reg):
    """Estado de la fila y las dimensiones que no están en OK, con su motivo."""
    e = {k: reg["dimensiones"][k]["estado"] for k in DIMS}
    partes = [f"{k} {e[k]}: {reg['dimensiones'][k].get('detalle', '')}" for k in DIMS if e[k] not in ("OK", "NO_APLICA")]
    return reg["estado"] + (" · " + " · ".join(partes) if partes else " en las seis dimensiones")
