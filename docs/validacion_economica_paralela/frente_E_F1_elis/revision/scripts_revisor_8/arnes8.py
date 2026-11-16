"""Revisión independiente n.º 8 · módulo común (frente E · F1 · Elis). No modifica nada del autor.

Carga el verificador de una versión como módulo (cada versión, con su propio nombre y su propia caché) y construye
declaraciones de filas sobre líneas reales del PDF, que se evalúan con la función que la ejecución oficial usa para
cada fila de tabla: `comprobar_tabla`. La línea se fija entera (etiqueta «re:^…$» y, si la página la repite, su
ocurrencia), y la posición se declara por la derecha, como en el CSV del autor.
"""
import importlib.util
import json
import re
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")
COD = {"OK": "O", "NO_APLICA": "N", "PENDIENTE": "P", "FALLO": "F", "NO_EVALUADO": "X"}
SEGMENTOS = ("Francia", "Europa central", "Escandinavia y Europa del Este", "Reino Unido e Irlanda", "Latinoamérica",
             "Europa del Sur", "Otros segmentos")
# identificadores de sondeo por modo de control del ejercicio (modo_admitido del verificador los fija por prefijo) y,
# con ellos, la columna esperada de cada familia (COLUMNA_POR_CONCEPTO)
PERFILES_DE_MODO = (
    ("TAXDIF_B8", "max_cabecera"),
    ("LS_B8_ROU_X", "movimientos"), ("LS_B8_PAS_X", "movimientos"), ("INT_RC_B8", "movimientos"), ("INT_MARCA_B8", "movimientos"),
    ("PPE_B8_RM_X", "movimientos"), ("PPE_B8_TOT_X", "movimientos"),
    ("LS_SALDO_ROU_B8", "saldo"), ("LS_SALDO_PAS_B8", "saldo"), ("INT_RC_VNC_B8", "saldo"),
    ("VENTAS_SEG_B8", "titulo"),
    ("CREC_ORG_B8", "crecimiento"), ("CREC_EXT_B8", "crecimiento"), ("CREC_FX_B8", "crecimiento"), ("CREC_PUB_B8", "crecimiento"),
)
ID_GRUPO = "B8_GEN"          # modo «dos_columnas»


class Version:
    def __init__(self, nombre, carpeta, raiz):
        self.nombre, self.carpeta, self.raiz = nombre, Path(carpeta), Path(raiz)
        spec = importlib.util.spec_from_file_location("verificar_" + re.sub(r"\W", "_", nombre), self.carpeta / "scripts" / "verificar_cifras.py")
        self.V = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.V)
        self.fuentes = json.loads((self.carpeta / "datos" / "fuentes.json").read_text(encoding="utf-8"))["fuentes"]
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
        """La función oficial para una fila de tabla, con los mismos argumentos que le da main()."""
        doc = fila["doc"]
        return self.V.comprobar_tabla(self.pdf(doc), fila, self.idioma(doc), self.fuentes[doc], self.ejercicios)

    def estado(self, res):
        return self.V.estado_fila(res["dimensiones"])

    def es_pagina_del_grupo(self, lineas):
        return any(self.V.GRUPO_RX.search(l) for l in [x for x in lineas if x.strip()][:8])

    def edicion_que_pasa(self, modo, anio, doc):
        """Edición («vigente» o «anterior») con la que la dimensión de edición puede quedar OK para ese ejercicio en esa
        publicación, según la regla del propio verificador; si ninguna puede, «anterior»."""
        e = self.publicacion(doc)
        ey = max(anio, e - 1) if modo == "saldo" else anio
        return "vigente" if e == self.V.regla_edicion(ey, modo, self.ejercicios) else "anterior"


def codigo(res):
    """Estados de las seis dimensiones en una cadena de seis letras (O, N, P, F, X), en el orden de DIMS."""
    return "".join(COD[res["dimensiones"][d]["estado"]] for d in DIMS)


def estado_de_codigo(c):
    return "FALLO" if ("F" in c or "X" in c) else ("PENDIENTE" if "P" in c else "OK")


def etiqueta_exacta(linea):
    return "re:^" + re.escape(linea) + "$"


def ocurrencia(lineas, i):
    return 1 + sum(1 for l in lineas[:i] if l == lineas[i])


def fila(doc, pag, lineas, i, k, n, token, valor, anio, idf, modo, unidad, perimetro, edicion):
    """Declaración de la cifra del token k (de n) de la línea i. La posición se declara por la derecha (k − n)."""
    return {"id": idf, "anio": str(anio), "concepto": "barrido de la revisión n.º 8", "doc": doc, "pagina": str(pag), "tipo": "tabla",
            "etiqueta": etiqueta_exacta(lineas[i]), "ocurrencia": str(ocurrencia(lineas, i)), "pos": str(k - n), "literal": token,
            "valor_publicado": str(valor), "unidad": unidad, "perimetro": perimetro, "edicion": edicion, "nota": "", "control_anio": modo}


def leer_csv(ruta):
    import csv
    with open(ruta, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def sin_anios(s):
    return re.sub(r"\b20\d\d\b", "AAAA", s)
