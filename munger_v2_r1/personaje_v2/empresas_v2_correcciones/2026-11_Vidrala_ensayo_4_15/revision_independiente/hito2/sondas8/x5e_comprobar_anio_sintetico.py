#!/usr/bin/env python3
"""x5e · octava comprobación · X5 en su USO: `comprobar_anio` (R-b: el impreso, importe completo en su línea y en su página) con el código
anterior (45ff57c) y el nuevo (0a0020b), sobre expedientes sintéticos mínimos como los de test_comprobadores.py h1 (texto/AR.txt de una
página y fase1_partes/AR_2025.json), escritos en el TMPDIR del revisor. No usa LibreOffice.
Uso: python3 -I -B x5e_comprobar_anio_sintetico.py"""
import json, os, shutil, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, FO  # noqa: E402
T = "’"


def empresa(c, pagina, comp):
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "texto"))
    os.makedirs(os.path.join(c, "fase1_partes"))
    open(os.path.join(c, "texto", "AR.txt"), "w", encoding="utf-8").write("[PDF PAGE 1]\n" + pagina + "\n")
    p = {k: {} for k in FN.PARTIDAS}
    p["capex"] = {"actual": [comp]}
    json.dump({"anio": 2025, "archivo": "AR.txt", "unidad": "millones", "partidas": p}, open(os.path.join(c, "fase1_partes", "AR_2025.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def comp(imp, lin):
    return {"concepto": "Capital expenditure", "impreso": imp, "pagina": 1, "linea": lin}


CASOS = [  # (nombre, página, impreso, línea, esperado con el código nuevo, nota)
    ("1 trozo detrás de apóstrofo ASCII", "Capital expenditure 1'849,7", "849,7", "Capital expenditure 1'849,7", "RECHAZADO", "X5"),
    ("2 trozo detrás de «’»", f"Capital expenditure 1{T}849,7", "849,7", f"Capital expenditure 1{T}849,7", "RECHAZADO", "X5"),
    ("3 trozo delante de apóstrofo ASCII", "Capital expenditure 849'697", "849", "Capital expenditure 849'697", "RECHAZADO", "X5"),
    ("4 trozo delante de «’»", f"Capital expenditure 849{T}697", "849", f"Capital expenditure 849{T}697", "RECHAZADO", "X5"),
    ("5 control: el importe entero", "Capital expenditure 849,7", "849,7", "Capital expenditure 849,7", "ACEPTADO", "control"),
    ("6 control: trozo con punto", "Capital expenditure 1.849,7", "849,7", "Capital expenditure 1.849,7", "RECHAZADO", "ya rechazado"),
    ("7 el número entero con apóstrofo como impreso", "Capital expenditure 1'849,7", "1'849,7", "Capital expenditure 1'849,7", "RECHAZADO", "numero() no admite el apóstrofo: «no numérico» (prudente, ya existía)"),
    ("8 el número entero con «’» como impreso", f"Capital expenditure 1{T}849,7", f"1{T}849,7", f"Capital expenditure 1{T}849,7", "RECHAZADO", "lo mismo"),
    ("9 trozo y además suelto en la línea (dos columnas)", "Capital expenditure 1'849,7 849,7", "849,7", "Capital expenditure 1'849,7 849,7", "ACEPTADO", "legítimo: está como importe completo"),
    ("10 posesivo en la línea (forma real de Elis)", f"Ventas SBF 120{T}s 849,7", "849,7", f"Ventas SBF 120{T}s 849,7", "ACEPTADO", "control"),
    ("11 francés: letra + ’ + cifra", f"Charges de l{T}exercice 849,7", "849,7", f"Charges de l{T}exercice 849,7", "ACEPTADO", "control"),
    ("12 coste: «Q1'24» y el impreso es 24", "Capital expenditure Q1'24", "24", "Capital expenditure Q1'24", "RECHAZADO", "coste prudente nuevo"),
    ("13 coste: llamada de nota tras comilla de cierre", f"Plan ‘Vision 2030{T}1", "2030", f"Plan ‘Vision 2030{T}1", "RECHAZADO", "coste prudente nuevo"),
    # la línea CORTADA justo en el separador de miles (R-a solo exige que la línea, tal como se da, sea una subcadena de la página)
    ("14 línea cortada tras el apóstrofo; el trozo no está suelto en la página", "Capital expenditure 1'849,7 millones", "849,7", "849,7 millones", "RECHAZADO", "X5, por la comprobación en la página"),
    ("15 línea cortada tras el punto; el trozo no está suelto en la página", "Capital expenditure 1.849,7 millones", "849,7", "849,7 millones", "RECHAZADO", "ya rechazado"),
    ("16 línea cortada tras el apóstrofo; el trozo SÍ está suelto en otra línea de la página", "Capital expenditure 1'849,7 millones\nOther items 849,7", "849,7", "849,7 millones", None, "residuo de R-a (no de X5): ¿se acepta?"),
    ("17 lo mismo con punto de miles", "Capital expenditure 1.849,7 millones\nOther items 849,7", "849,7", "849,7 millones", None, "residuo de R-a, igual con los dos códigos: ¿se acepta?"),
]
ok_todo = True
with tempfile.TemporaryDirectory(prefix="x5e_") as t:
    for nombre, pag, imp, lin, esp, nota in CASOS:
        c = os.path.join(t, "caso")
        empresa(c, pag, comp(imp, lin))
        r = {}
        for et, M in (("anterior", FO), ("nuevo", FN)):
            e = M.comprobar_anio(c, 2025, [])
            r[et] = ("RECHAZADO" if e else "ACEPTADO", e[0] if e else "")
        marca = ""
        if esp is not None and r["nuevo"][0] != esp:
            ok_todo = False
            marca = f"   <<< se esperaba {esp}"
        print(f"   caso {nombre}\n      página «{pag}» · impreso «{imp}» · línea «{lin}»\n      anterior: {r['anterior'][0]:9} · nuevo: {r['nuevo'][0]:9}{' · CAMBIA' if r['anterior'][0] != r['nuevo'][0] else ''} · {nota}{marca}"
              + (f"\n      motivo (nuevo): {r['nuevo'][1][:120]}" if r["nuevo"][1] else ""))
print("\nRESULTADO:", "CONFORME (los casos con resultado esperado)" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
