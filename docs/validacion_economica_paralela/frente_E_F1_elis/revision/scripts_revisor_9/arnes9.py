"""Revisión independiente n.º 9 · módulo común (frente E · F1 · Elis). No modifica nada del autor.

Carga `verificar_cifras.py` de una carpeta (o de un archivo suelto) como módulo propio, con su propia caché de páginas, y
declara filas sobre líneas reales del PDF para evaluarlas con `comprobar_tabla`, la función que la ejecución oficial
aplica a cada fila de tabla. La línea se fija entera (etiqueta «re:^…$» más su ocurrencia) y la posición se cuenta por la
derecha, como en el CSV del autor.
"""
import importlib.util
import json
import re
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")
LETRA = {"OK": "O", "NO_APLICA": "N", "PENDIENTE": "P", "FALLO": "F", "NO_EVALUADO": "X"}
SEGMENTOS = ("Francia", "Europa central", "Escandinavia y Europa del Este", "Reino Unido e Irlanda", "Latinoamérica",
             "Europa del Sur", "Otros segmentos")
ID_GENERICO = "R9_GEN"   # sin prefijo conocido: modo «dos_columnas»
# identificadores de sondeo de los demás modos (el verificador fija el modo por el prefijo)
PERFILES = (("TAXDIF_R9", "max_cabecera"), ("LS_R9_ROU_X", "movimientos"), ("LS_R9_PAS_X", "movimientos"), ("INT_RC_R9", "movimientos"),
            ("INT_MARCA_R9", "movimientos"), ("PPE_R9_RM_X", "movimientos"), ("PPE_R9_TOT_X", "movimientos"),
            ("LS_SALDO_ROU_R9", "saldo"), ("LS_SALDO_PAS_R9", "saldo"), ("INT_RC_VNC_R9", "saldo"), ("VENTAS_SEG_R9", "titulo"),
            ("CREC_ORG_R9", "crecimiento"), ("CREC_EXT_R9", "crecimiento"), ("CREC_FX_R9", "crecimiento"), ("CREC_PUB_R9", "crecimiento"))


class Version:
    """Un verificador cargado como módulo. `origen` es la carpeta frente_E_F1_elis de la versión o un archivo .py suelto;
    `datos` es la carpeta de la que se leen fuentes.json (por defecto, la propia)."""

    def __init__(self, nombre, origen, raiz, datos=None):
        origen = Path(origen)
        py = origen if origen.suffix == ".py" else origen / "scripts" / "verificar_cifras.py"
        self.nombre, self.raiz, self.py = nombre, Path(raiz), py
        spec = importlib.util.spec_from_file_location("verificador_" + re.sub(r"\W", "_", nombre), py)
        self.V = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.V)
        carpeta = Path(datos) if datos else origen
        self.carpeta = carpeta
        self.fuentes = json.loads((carpeta / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
        self.ejercicios = {f["ejercicio"] for f in self.fuentes.values() if isinstance(f.get("ejercicio"), int)}

    def pdf(self, doc):
        return self.raiz / self.fuentes[doc]["archivo"]

    def idioma(self, doc):
        return self.fuentes[doc]["idioma"]

    def publicacion(self, doc):
        return self.fuentes[doc]["ejercicio"]

    def paginas(self, doc):
        return self.V.num_paginas(self.pdf(doc))

    def lineas(self, doc, pag):
        return self.V.texto_pagina(self.pdf(doc), pag).splitlines()

    def tabla(self, fila):
        doc = fila["doc"]
        return self.V.comprobar_tabla(self.pdf(doc), fila, self.idioma(doc), self.fuentes[doc], self.ejercicios)

    def pagina_del_grupo(self, lineas):
        return any(self.V.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8])

    def edicion_posible(self, modo, anio, doc):
        """La edición con la que la dimensión «edicion» puede dar OK para ese ejercicio en esa publicación, según la regla
        del propio verificador («anterior» si ninguna puede)."""
        e = self.publicacion(doc)
        ey = max(anio, e - 1) if modo == "saldo" else anio
        return "vigente" if e == self.V.regla_edicion(ey, modo, self.ejercicios) else "anterior"


def codigo(res):
    return "".join(LETRA[res["dimensiones"][d]["estado"]] for d in DIMS)


def estado(cod):
    return "FALLO" if ("F" in cod or "X" in cod) else ("PENDIENTE" if "P" in cod else "OK")


def detalles(res):
    return {d: res["dimensiones"][d].get("detalle", "") for d in DIMS[1:]}


def declarar(doc, pag, lineas, i, k, n, tok, val, anio, idf, modo, unidad, perimetro, edicion):
    """Fila declarada para el token k (de n) de la línea i de la página."""
    return {"id": idf, "anio": str(anio), "concepto": "barrido de la revisión n.º 9", "doc": doc, "pagina": str(pag), "tipo": "tabla",
            "etiqueta": "re:^" + re.escape(lineas[i]) + "$", "ocurrencia": str(1 + sum(1 for x in lineas[:i] if x == lineas[i])),
            "pos": str(k - n), "literal": tok, "valor_publicado": str(val), "unidad": unidad, "perimetro": perimetro, "edicion": edicion,
            "nota": "", "control_anio": modo}


def sangria(l):
    return len(l) - len(l.lstrip())
