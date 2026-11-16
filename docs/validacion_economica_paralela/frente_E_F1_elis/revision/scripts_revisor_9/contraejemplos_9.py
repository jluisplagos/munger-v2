"""Revisión independiente n.º 9 · contraejemplos sobre filas reales (frente E · F1 · Elis). No modifica nada del autor.

Cada caso es una fila declarada sobre una línea real de un PDF (la línea se fija entera). Se ejecuta el verificador
OFICIAL de cada versión como proceso aparte, con un CSV de una fila y el fuentes.json del autor, y se leen del JSON de
salida los estados y los motivos de las seis dimensiones. No se importa ninguna función del verificador para evaluar.

Uso: python3 -I -B contraejemplos_9.py --raiz <munger_v2_r1> --version C16=<frente C17> --version C18=<frente C19>
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
from fractions import Fraction
from pathlib import Path

GRUPO = "consolidado IFRS, grupo Elis"
DIMS = ("literal", "ejercicio", "columna", "unidad", "perimetro", "edicion")
CAMPOS = ("id", "anio", "concepto", "doc", "pagina", "tipo", "etiqueta", "ocurrencia", "pos", "literal", "valor_publicado", "unidad", "perimetro",
          "edicion", "nota", "control_anio")

# (clave, explicación, doc, página, expresión de la línea, n: el token es la n-ésima aparición (desde 0) del literal entre los
#  tokens de la línea, literal, ejercicio declarado, edición, identificador, modo)
CASOS = [
    ("U1", "El primer «0» de una fila de un plan de acciones con la fecha en el rótulo («as at 12/31/2025 · 0 · 92,485 …»). El verificador "
           "localiza el token buscando su texto y lo encuentra dentro de la fecha del rótulo: lo da por «el día de la fecha»", None),
    ("U1a", "URD 2025 p.360, «Number of rights lapsed or forfeited / as at 12/31/2025», primera cifra (0), declarada 2025",
     "URD2025", 360, r"^\s*as at 12/31/2025\s+0\s+92,485", 0, "0", 2025, "vigente", "R9_U1A", "dos_columnas"),
    ("U1b", "la misma cifra declarada 2024: la fila es de 2025",
     "URD2025", 360, r"^\s*as at 12/31/2025\s+0\s+92,485", 0, "0", 2024, "vigente", "R9_U1B", "dos_columnas"),
    ("U1c", "control: la segunda cifra de esa fila (92,485), declarada 2024",
     "URD2025", 360, r"^\s*as at 12/31/2025\s+0\s+92,485", 0, "92,485", 2024, "vigente", "R9_U1C", "dos_columnas"),
    ("U1d", "DEU 2024 p.306, «Nombre de droits devenus caducs / au 31/12/2024», primera cifra (0), declarada 2023",
     "DEU2024FR", 306, r"^\s*au 31/12/2024\s+0\s+26 718", 0, "0", 2023, "vigente", "R9_U1D", "dos_columnas"),
    ("U1e", "la misma cifra con un identificador de saldo y su ejercicio (2024): en el modo «saldo» la fecha de la línea da el ejercicio",
     "DEU2024FR", 306, r"^\s*au 31/12/2024\s+0\s+26 718", 0, "0", 2024, "anterior", "LS_SALDO_ROU_R9", "saldo"),
    ("U2", "La misma causa en la asignación de columnas, anterior a C18: «Number of fatal accidents · 0(a) · 0 · 0» bajo «Group 2021 · Group "
           "2020 · Group 2019». La celda «0(a)» no es un token; el «0» de 2020 se localiza dentro de ella, bajo 2021, y el de 2019, bajo 2020", None),
    ("U2a", "URD 2021 p.176, el «0» de la columna de 2020 declarado 2021",
     "URD2021", 176, r"^\s*Number of fatal accidents\s", 0, "0", 2021, "anterior", "R9_U2A", "dos_columnas"),
    ("U2b", "el mismo «0» declarado 2020, que es su columna",
     "URD2021", 176, r"^\s*Number of fatal accidents\s", 0, "0", 2020, "vigente", "R9_U2B", "dos_columnas"),
    ("U3", "La regla de la fecha del rótulo en líneas que no son saldos en millones de euros (resto de T2)", None),
    ("U3a", "URD 2021 p.225, sumario: «6.1.5 Consolidated statement of changes in equity / as at December 31, 2021 · 228». El número de página, declarado 2021",
     "URD2021", 225, r"^\s*as at December 31, 2021\s+228\s*$", 0, "228", 2021, "anterior", "R9_U3A", "dos_columnas"),
    ("U3b", "URD 2022 p.294, «Number of rights outstanding / as at 12/31/2022»: rótulo partido antes de «as at». 548,801 declarado 2022",
     "URD2022", 294, r"^\s*as at 12/31/2022\s+-\s+548,801", 0, "548,801", 2022, "anterior", "R9_U3B", "dos_columnas"),
    ("U3c", "URD 2021 p.261, la misma fila en una sola línea, «Number of rights outstanding as at 12/31/2021». 391,839 declarado 2021",
     "URD2021", 261, r"^\s*Number of rights outstanding as at 12/31/2021\s", 0, "391,839", 2021, "anterior", "R9_U3C", "dos_columnas"),
    ("U3d", "URD 2022 p.294, «Number of working beneficiaries / as at 12/31/2022», primera cifra (402), declarada 2022: la línea no dice «Number of»",
     "URD2022", 294, r"^\s*as at 12/31/2022\s+402\s", 0, "402", 2022, "anterior", "R9_U3D", "dos_columnas"),
    ("U3e", "URD 2021 p.257, saldo publicado antes de la reexpresión: «As at December 31, 2019, published · 609.3 …», declarado 2019",
     "URD2021", 257, r"^\s*As at December 31, 2019, published\s", 0, "609.3", 2019, "vigente", "R9_U3E", "dos_columnas"),
    ("U4", "Tokens del rótulo que no son cifras y que la regla nueva no alcanza (ya eran OK en C16)", None),
    ("U4a", "URD 2022 p.261, pie de página impar «Elis | Universal Registration Document 2022 | 259»: el folio, declarado 2021",
     "URD2022", 261, r"Elis \| Universal Registration Document 2022 \| 259\s*$", 0, "259", 2021, "vigente", "R9_U4A", "dos_columnas"),
    ("U4b", "control: URD 2022 p.262, pie de página par «260 | Elis | Universal Registration Document 2022»: el año, declarado 2021",
     "URD2022", 262, r"^\s*260 \| Elis \| Universal Registration Document 2022\s*$", 0, "2022", 2021, "vigente", "R9_U4B", "dos_columnas"),
    ("U4c", "URD 2021 p.218, cabecera «As at January 1» sobre las columnas de 2021 y 2020: el día, declarado 2020",
     "URD2021", 218, r"^\s*As at January 1\s*$", 0, "1", 2020, "vigente", "R9_U4C", "dos_columnas"),
    ("U5", "Controles de C18 sobre filas reales", None),
    ("U5a", "URD 2022 p.284, deterioro de clientes, saldo de cierre (54,3), una sola columna, declarado 2022",
     "URD2022", 284, r"^\s*AS AT DECEMBER 31, 2022\s", 0, "(54.3)", 2022, "anterior", "R9_U5A", "dos_columnas"),
    ("U5b", "URD 2023 p.319, valor neto contable a 31-12-2022 reexpresado («NET CARRYING AMOUNT AS AT DECEMBER 31, 2022 / RESTATED*»), primera columna "
            "(580,7), declarado 2022: lo reconoce C18 por primera vez",
     "URD2023", 319, r"^\s*RESTATED\*\s+580\.7", 0, "580.7", 2022, "vigente", "R9_U5B", "dos_columnas"),
    ("U5c", "DEU 2024 p.336, reserva de coberturas, saldo de apertura «SOLDE AU 1er JANVIER 2023» (6,8), declarado 2022",
     "DEU2024FR", 336, r"^\s*SOLDE AU 1er JANVIER 2023\s", 0, "6,8", 2022, "anterior", "R9_U5C", "dos_columnas"),
]


def normalizar(s):
    import unicodedata
    s = unicodedata.normalize("NFKC", s)
    return s.replace("’", "'").replace("‘", "'")


def lineas_de(pdf, n):
    r = subprocess.run(["pdftotext", "-q", "-f", str(n), "-l", str(n), "-layout", str(pdf), "-"], capture_output=True, check=True)
    return normalizar(r.stdout.decode("utf-8", errors="replace")).splitlines()


def valor(tok, idioma):
    t = tok.replace("%", "").strip()
    neg = t.startswith("(") or t.startswith(("-", "–", "−"))
    t = t.strip("()").lstrip("-–−+")
    t = t.replace(" ", "").replace(",", ".") if idioma == "fr" else t.replace(",", "")
    v = Fraction(t)
    return -v if neg else v


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--version", action="append", required=True, help="NOMBRE=carpeta frente_E_F1_elis")
    a = ap.parse_args()
    versiones = [(v.split("=", 1)[0], Path(v.split("=", 1)[1])) for v in a.version]
    ultima = versiones[-1][1]
    fuentes = json.loads((ultima / "datos" / "fuentes.json").read_text(encoding="utf-8"))
    # los tokens de la línea se cuentan con el tokenizador del verificador más reciente, solo para declarar la posición
    import importlib.util
    spec = importlib.util.spec_from_file_location("v_decl", ultima / "scripts" / "verificar_cifras.py")
    V = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(V)
    print("Contraejemplos de la revisión n.º 9 · verificador oficial de cada versión, como proceso aparte")
    for caso in CASOS:
        if caso[2] is None:
            print()
            print(f"{caso[0]}. {caso[1]}")
            print("-" * 100)
            continue
        clave, txt, doc, pag, rx, k, literal, anio, edicion, idf, modo = caso
        f = fuentes["fuentes"][doc]
        L = lineas_de(a.raiz / f["archivo"], pag)
        cand = [i for i, l in enumerate(L) if re.search(rx, l)]
        if len(cand) != 1:
            print(f"{clave}: la expresión casa con {len(cand)} líneas de {doc} p.{pag}: caso no evaluado")
            continue
        i = cand[0]
        toks = [t for t in V.tokens_numericos(L[i], f["idioma"])]
        iguales = [j for j, t in enumerate(toks) if t == literal]
        if len(iguales) <= k:
            print(f"{clave}: la línea no tiene {k + 1} tokens «{literal}»: caso no evaluado")
            continue
        j, tok = iguales[k], literal
        fila = {"id": idf, "anio": str(anio), "concepto": "contraejemplo de la revisión n.º 9", "doc": doc, "pagina": str(pag), "tipo": "tabla",
                "etiqueta": "re:^" + re.escape(L[i]) + "$", "ocurrencia": str(1 + sum(1 for x in L[:i] if x == L[i])), "pos": str(j - len(toks)),
                "literal": tok, "valor_publicado": str(valor(tok, f["idioma"])), "unidad": "%" if "%" in tok else "mm EUR", "perimetro": GRUPO,
                "edicion": edicion, "nota": "", "control_anio": modo}
        print(f"{clave} · {txt}")
        print(f"     {doc} p.{pag} l.{i + 1}: «{re.sub(chr(92) + 's{2,}', '  ', L[i].strip())[:140]}» · token «{tok}» · ejercicio {anio} · {modo} · edición {edicion}")
        for nombre, carpeta in versiones:
            with tempfile.TemporaryDirectory() as d:
                d = Path(d)
                with (d / "c.csv").open("w", encoding="utf-8", newline="") as g:
                    w = csv.DictWriter(g, fieldnames=CAMPOS, delimiter=";")
                    w.writeheader()
                    w.writerow(fila)
                r = subprocess.run([sys.executable, "-I", "-B", str(carpeta / "scripts" / "verificar_cifras.py"), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"),
                                    "--fuentes", str(ultima / "datos" / "fuentes.json"), "--salida", str(d / "s.json")], capture_output=True, text=True)
                res = json.loads((d / "s.json").read_text(encoding="utf-8"))["cifras"][0]
            dims = res["dimensiones"]
            print(f"     {nombre}: {res['estado']:9} " + " · ".join(f"{x[:3]} {dims[x]['estado']}" for x in DIMS))
            for x in DIMS[1:]:
                if dims[x]["estado"] in ("FALLO", "PENDIENTE") or x in ("ejercicio", "columna"):
                    print(f"          {x}: {dims[x].get('detalle', '')[:200]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
