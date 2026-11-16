"""Revisión independiente n.º 8 · contraejemplos sobre filas reales del PDF, con el verificador OFICIAL de cada versión
ejecutado como proceso aparte (frente E · F1 · Elis). No modifica nada del autor.

Cada caso fija una línea real de una página (por una expresión regular que debe casar con una sola línea), un token de esa
línea y una declaración (ejercicio, unidad, perímetro, edición, identificador y modo). Con todos los casos se escribe un
CSV temporal con el formato de datos/cifras_fuente.csv y se ejecuta `verificar_cifras.py` de cada versión sobre él, tal
como lo ejecuta el autor. Se imprime, por caso y versión, el estado de la fila y el de cada dimensión que no es OK, con su
motivo; del ejercicio y de la columna se imprime siempre el motivo.

Uso: python3 -I -B contraejemplos_8.py --raiz <munger_v2_r1> --version C14=<frente C15> --version C16=<frente C17>
"""
import argparse
import csv
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import arnes8 as H  # noqa: E402

G = H.GRUPO
# (clave, título del bloque) y casos: (id, descripción, doc, página, regex de la línea, token, ejercicio, edición, perímetro, identificador)
BLOQUES = [
    ("T1", "Regla de S1 y dimensión «columna»: un saldo de una tabla con columnas por CONCEPTO queda OK en las seis dimensiones "
           "sin que nada compruebe la columna (NO_APLICA). Con el identificador de un concepto de saldo, la misma cifra falla en «columna»", [
        ("T1a", "derechos de uso a 31-12-2024: columna «Vehicles» (237,4) declarada con un identificador genérico (p. ej., como el total)",
         "URD2025", 366, r"^\s*AS AT 12/31/2024\s", "237.4", 2024, "vigente", G, "R8_T1A"),
        ("T1b", "la misma cifra con el identificador de saldo de los derechos de uso (columna esperada: «Total»)",
         "URD2025", 366, r"^\s*AS AT 12/31/2024\s", "237.4", 2024, "vigente", G, "LS_SALDO_ROU_R8"),
        ("T1c", "control: el total (572,8) con el identificador de saldo",
         "URD2025", 366, r"^\s*AS AT 12/31/2024\s", "572.8", 2024, "vigente", G, "LS_SALDO_ROU_R8B"),
        ("T1d", "patrimonio a 31-12-2021: columna «Non-controlling interests» (0,7) declarada con un identificador genérico",
         "URD2022", 262, r"^\s*31, 2021 restated\(a\)\s", "0.7", 2021, "vigente", G, "R8_T1D"),
        ("T1e", "inmovilizado material a 31-12-2024: columna «Vehicles» (13,0) declarada con un identificador genérico",
         "URD2025", 367, r"^\s*NET CARRYING AMOUNT AS AT DECEMBER 31, 2024\s", "13.0", 2024, "vigente", G, "R8_T1E"),
    ]),
    ("T2", "Regla de S1: tokens que no son cifras del saldo y quedan OK en las seis dimensiones como millones de euros del grupo", [
        ("T2a", "el día de la fecha («31» de «DECEMBER, 31 2022»), declarado 2022", "URD2022", 262, r"^\s*DECEMBER, 31 2022\s", "31", 2022, "anterior", G, "R8_T2A"),
        ("T2b", "la pestaña del capítulo («6») en la línea «6 · As at December 31, 2021 · (57.9)», declarada 2021",
         "URD2022", 284, r"^6\s+As at December 31, 2021\s", "6", 2021, "vigente", G, "R8_T2B"),
        ("T2c", "el año de la fecha en una línea de PROSA («…au 31 décembre 2023)»), declarado 2023",
         "DEU2024FR", 257, r"^d'euros \(contre 902,3 millions", "2023)", 2023, "vigente", G, "R8_T2C"),
        ("T2d", "el año de la fecha en la línea intermedia del rótulo («DECEMBER 31, 2021», sin cifras del saldo), declarado 2021",
         "URD2022", 263, r"^\s*DECEMBER 31, 2021\s*$", "2021", 2021, "vigente", G, "R8_T2D"),
        ("T2e", "el año de un título de apartado («…d'application obligatoire / au 1er janvier 2024»), declarado 2023",
         "DEU2024FR", 277, r"^au 1er janvier 2024\s*$", "2024", 2023, "vigente", G, "R8_T2E"),
    ]),
    ("T3", "Regla de S1: saldos de CIERRE del estado de cambios en el patrimonio que la regla no reconoce (rótulo partido tras el día "
           "o en tres líneas). Son cifras legítimas declaradas con su ejercicio", [
        ("T3a", "DEU 2024 p.274 · «SOLDE AU 31 / DÉCEMBRE 2024» · capital a 31-12-2024 (236,7), declarado 2024", "DEU2024FR", 274, r"^\s*DÉCEMBRE 2024\s+236,7", "236,7", 2024, "anterior", G, "R8_T3A"),
        ("T3b", "DEU 2024 p.275 · «SOLDE AU 31 / DÉCEMBRE 2023 / RETRAITÉ*» · capital a 31-12-2023 (234,0), declarado 2023", "DEU2024FR", 275, r"^\s*RETRAITÉ\*\s+234,0", "234,0", 2023, "vigente", G, "R8_T3B"),
        ("T3c", "URD 2022 p.263 · «BALANCE AS AT / DECEMBER 31, 2021 / (RESTATED)» · capital a 31-12-2021 (224,1), declarado 2021", "URD2022", 263, r"^\s*\(RESTATED\)\s+224\.1", "224.1", 2021, "vigente", G, "R8_T3C"),
        ("T3d", "URD 2025 p.329 · «BALANCE AS AT / DECEMBER 31, 2024 / RESTATED*» · capital a 31-12-2024 (236,7), declarado 2024", "URD2025", 329, r"^\s*RESTATED\*\s+236\.7", "236.7", 2024, "vigente", G, "R8_T3D"),
        ("T3e", "URD 2021 p.231 · «BALANCE AS AT / DECEMBER 31, 2020 / (RESTATED)» · capital a 31-12-2020 (221,8), declarado 2020", "URD2021", 231, r"^\s*\(RESTATED\)\s+221\.8", "221.8", 2020, "vigente", G, "R8_T3E"),
        ("T3f", "control: URD 2023 p.281 · «BALANCE AS AT DECEMBER / 31, 2022, RESTATED*» · capital a 31-12-2022 (230,1), declarado 2022", "URD2023", 281, r"^\s*31, 2022, RESTATED\*\s", "230.1", 2022, "vigente", G, "R8_T3F"),
    ]),
    ("T4", "Regla de S1: la fecha de la línea de continuación del rótulo de la fila ANTERIOR se atribuye a la fila siguiente "
           "(URD 2022 p.350, cuentas de la sociedad dominante; aquí las dos filas son de la misma fecha)", [
        ("T4a", "fila «Number of rights lapsed or forfeited / as at 12/31/2022»: su fecha va en la línea de debajo", "URD2022", 350, r"^\s*Number of rights lapsed or forfeited\s", "186,469", 2022, "anterior", G, "R8_T4A"),
        ("T4b", "fila siguiente, «Number of rights outstanding»: recibe la fecha de la línea de encima, que es del rótulo anterior", "URD2022", 350, r"^\s*Number of rights outstanding\s", "1,307,749", 2022, "anterior", G, "R8_T4B"),
    ]),
    ("T5", "S4, resto: en la tabla del WACC por país del DEU 2024 p.315 las dos últimas filas conservan el perímetro OK "
           "(la primera línea del rótulo, en mayúsculas, se toma por título y corta la búsqueda de la cabecera)", [
        ("T5a", "«TAUX D'ACTUALISATION AVANT / IMPÔT 2024 (APPROXIMATION)», columna de Francia (11,2 %)", "DEU2024FR", 315, r"^\s*IMPÔT 2024 \(APPROXIMATION\)\s", "11,2%", 2024, "anterior", G, "R8_T5A"),
        ("T5b", "«Taux d'actualisation avant impôt / 2023 (approximation)», columna de Brasil (19,4 %)", "DEU2024FR", 315, r"^\s*2023 \(approximation\)\s", "19,4%", 2023, "vigente", G, "R8_T5B"),
        ("T5c", "control: «WACC 2024», columna de Francia (8,3 %)", "DEU2024FR", 315, r"^\s*WACC 2024\s", "8,3%", 2024, "anterior", G, "R8_T5C"),
        ("T5d", "control: la misma fila en el URD 2025 p.369, «PRE-TAX DISCOUNT RATE 2025 / (APPROXIMATION)» (10,9 %)", "URD2025", 369, r"^\s*\(APPROXIMATION\)\s", "10.9%", 2025, "vigente", G, "R8_T5D"),
    ]),
    ("T6", "S2: el «rótulo de las líneas contiguas» toma líneas que no son el rótulo de la fila", [
        ("T6a", "URD 2023 p.261 · línea con solo la pestaña del capítulo («5»): su «rótulo» es la prosa contigua, que nombra la Unión Europea",
         "URD2023", 261, r"^\s*5\s*$", "5", 2023, "anterior", G, "R8_T6A"),
        ("T6b", "URD 2022 p.376 (organigrama) · «100% ELIS COLOMBIA» declarado del segmento Francia: «France» es la leyenda contigua",
         "URD2022", 376, r"^\s*100%\s+ELIS COLOMBIA\s*$", "100%", 2022, "anterior", "segmento Francia", "R8_T6B"),
        ("T6c", "control (S2 del revisor n.º 7): ventas de 2023 de Escandinavia y Europa del Este (599,2) declaradas de su segmento",
         "URD2023", 261, r"^\s*599\.2\s+580\.7", "599.2", 2023, "anterior", "segmento Escandinavia y Europa del Este", "R8_T6C"),
    ]),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True)
    ap.add_argument("--version", action="append", required=True, help="NOMBRE=carpeta (se puede repetir)")
    a = ap.parse_args()
    versiones = [H.Version(n, c, a.raiz) for n, c in (v.split("=", 1) for v in a.version)]
    ref = versiones[-1]
    filas, meta = [], {}
    for _, _, casos in BLOQUES:
        for cid, desc, doc, pag, rx, tok, anio, edicion, perimetro, idf in casos:
            lineas = ref.lineas(doc, pag)
            cand = [i for i, l in enumerate(lineas) if re.search(rx, l)]
            if len(cand) != 1:
                sys.exit(f"{cid}: la expresión casa con {len(cand)} líneas de {doc} p.{pag}")
            i = cand[0]
            toks = ref.V.tokens_numericos(lineas[i], ref.idioma(doc))
            ks = [k for k, t in enumerate(toks) if t == tok]
            if not ks:
                sys.exit(f"{cid}: el token {tok!r} no está en la línea: {toks}")
            k = ks[0]
            modo = ref.V.modo_admitido(idf)
            f = H.fila(doc, pag, lineas, i, k, len(toks), tok, ref.V.valor(tok, ref.idioma(doc)), anio, idf, modo,
                       "%" if "%" in tok else "mm EUR", perimetro, edicion)
            filas.append(f)
            meta[idf] = (cid, desc, doc, pag, i, lineas[i], tok, anio, edicion, perimetro, modo, k, len(toks))
    res = {}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        with (d / "c.csv").open("w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()), delimiter=";")
            w.writeheader()
            w.writerows(filas)
        for v in versiones:
            r = subprocess.run([sys.executable, "-I", "-B", str(v.carpeta / "scripts" / "verificar_cifras.py"), "--raiz", str(a.raiz), "--datos", str(d / "c.csv"),
                                "--fuentes", str(v.carpeta / "datos" / "fuentes.json"), "--salida", str(d / f"{v.nombre}.json")], capture_output=True, text=True)
            j = json.loads((d / f"{v.nombre}.json").read_text(encoding="utf-8"))
            res[v.nombre] = ({x["id"]: x for x in j["cifras"]}, r.returncode)
    print("Contraejemplos de la revisión n.º 8 · verificador oficial de cada versión, como proceso aparte")
    print("Códigos de salida: " + ", ".join(f"{n}: {c}" for n, (_, c) in res.items()))
    for clave, titulo, casos in BLOQUES:
        print()
        print(f"{clave}. {titulo}")
        print("-" * 100)
        for cid, desc, doc, pag, rx, tok, anio, edicion, perimetro, idf in casos:
            _, _, _, _, i, linea, _, _, _, _, modo, k, n = meta[idf]
            print()
            print(f"{cid} · {desc}")
            print(f"    {doc} p.{pag} l.{i + 1} · «{re.sub(r' {2,}', '  ', linea.strip())[:150]}» · token {k + 1}/{n} «{tok}» · declarado {anio}, "
                  f"{'%' if '%' in tok else 'mm EUR'}, {'grupo' if perimetro == G else perimetro}, edición {edicion}, identificador {idf} (modo {modo})")
            for v in versiones:
                x = res[v.nombre][0][idf]
                dims = x["dimensiones"]
                no_ok = [f"{dname} {dims[dname]['estado']}: {dims[dname]['detalle']}" for dname in H.DIMS if dims[dname]["estado"] in ("FALLO", "PENDIENTE", "NO_EVALUADO")]
                cab = "OK en las seis dimensiones" if x["estado"] == "OK" else x["estado"]
                print(f"    {v.nombre}: {cab}" + ("" if not no_ok else " · " + " | ".join(no_ok)))
                print(f"         ejercicio {dims['ejercicio']['estado']}: {dims['ejercicio']['detalle']} · columna {dims['columna']['estado']}: {dims['columna']['detalle']}"
                      + (f" · perímetro {dims['perimetro']['estado']}: {dims['perimetro']['detalle']}" if dims['perimetro']['estado'] == 'OK' and clave in ('T5', 'T6') else ""))


if __name__ == "__main__":
    main()
