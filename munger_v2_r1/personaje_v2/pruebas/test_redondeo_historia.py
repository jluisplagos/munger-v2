#!/usr/bin/env python3
"""Pruebas del redondeo exacto de la Historia (fase1_historia.py; examen, jumbo_f, celda Historia!I17).

El generador redondeaba con aritmética binaria: 7.035.150 € impresos × 10⁻⁶ = 7,03515 mm se guardaba como 7,0351499… y round(…, 4) daba
7,0351, mientras que ROUND de la hoja (mitad lejos de cero) da 7,0352. Ahora los importes se calculan exactos (fracciones) desde la cifra
impresa como texto y se redondean una sola vez con la regla de la hoja. No cambia ninguna otra regla de construcción.
No escribe en el repositorio: trabaja sobre copias temporales.
Uso: python3 -B pruebas/test_redondeo_historia.py      (código 0 si todo pasa)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as F  # noqa: E402

JUMBO = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "jumbo_f", "Jumbo")
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def intento(nombre, f, esperado):
    try:
        r = f()
    except Exception as ex:  # noqa: BLE001 — antes del cambio faltan las funciones: la prueba falla, no se interrumpe
        paso(nombre, False, f"{type(ex).__name__}: {ex}")
        return
    paso(nombre, r == esperado and type(r) is type(esperado), f"{r!r} (se espera {esperado!r})")


def mm(impreso, unidad="unidades"):
    """La cifra impresa en mm, como la lee construir (exacta desde el texto)."""
    return F.numero_exacto(impreso) * F.ESCALA_EXACTA[unidad]


# 1 · el caso de jumbo_f (Historia!I17) y sus variantes de signo y escala
intento("7.035.150 € → 7,0352 mm (no 7,0351)", lambda: F.redondear(mm("7.035.150"), 4), 7.0352)
intento("(7.035.150) → −7,0352 (mitad lejos de cero también en negativo)", lambda: F.redondear(mm("(7.035.150)"), 4), -7.0352)
intento("-7,035,150 → −7,0352", lambda: F.redondear(mm("-7,035,150"), 4), -7.0352)
intento("7.035,15 miles → 7,0352", lambda: F.redondear(mm("7.035,15", "miles"), 4), 7.0352)
intento("7.035150 sin empate a 3 decimales → 7,035", lambda: F.redondear(mm("7.035.150"), 3), 7.035)
intento("circulante de jumbo_f 2025: −Σ componentes = 61,15855 → 61,1586",
        lambda: F.redondear(-sum((mm(x) for x in ("(49.627.440)", "1.798.445", "(19.492.757)", "1.450.000", "4.713.202")), Fraction(0)), 4), 61.1586)

# 2 · empates: ROUND de la hoja (mitad lejos de cero), ni al par ni binario
for x, n, esp in ((2.5, 0, 3.0), (-2.5, 0, -3.0), (0.5, 0, 1.0), (-0.5, 0, -1.0), (1.5, 0, 2.0),
                  (1.0005, 3, 1.001), (-1.0005, 3, -1.001), (2.675, 2, 2.68), (-2.675, 2, -2.68), (0.00005, 4, 0.0001),
                  (1.00049, 3, 1.0), (-1.00049, 3, -1.0), (1.00051, 3, 1.001)):
    intento(f"ROUND({x}; {n}) = {esp}", lambda x=x, n=n: F.redondear(x, n), esp)
intento("fracción exacta −7035150/10⁶ a 4 decimales", lambda: F.redondear(Fraction(-7035150, 10 ** 6), 4), -7.0352)
intento("entero sin decimales", lambda: F.redondear(7, 3), 7.0)
intento("−0,00004 → 0 (sin cero negativo)", lambda: str(F.redondear(-0.00004, 4)), "0.0")

# 3 · la lectura exacta coincide con numero() (que no cambia) y no admite lo que numero() no admite
casos = ["1,125,977", "(12.345)", "-8,580", "3.463", "–", "-", "", "11.37", "4 573,7", "(130,8)", "1.031", "0.5", "905"]
try:
    paso("numero_exacto ≡ numero (misma lectura, exacta)", all(float(F.numero_exacto(s)) == F.numero(s) for s in casos),
         "; ".join(f"{s!r}→{F.numero_exacto(s)}" for s in casos[:6]))
    try:
        F.numero_exacto("12a")
        paso("numero_exacto rechaza «12a»", False)
    except ValueError:
        paso("numero_exacto rechaza «12a»", True)
    try:
        F.exacto(True)
        paso("exacto rechaza un booleano", False)
    except TypeError:
        paso("exacto rechaza un booleano", True)
    try:
        F.exacto("7.0352")
        paso("exacto rechaza un texto (la cifra impresa se lee con numero_exacto)", False)
    except TypeError:
        paso("exacto rechaza un texto (la cifra impresa se lee con numero_exacto)", True)
    try:
        F.redondear(float("nan"), 3)
        paso("redondear rechaza NaN", False)
    except ValueError:
        paso("redondear rechaza NaN", True)
except AttributeError as ex:
    paso("lectura exacta disponible", False, str(ex))

# 4 · cálculo declarado de Análisis (media/suma): la suma de las cifras declaradas es exacta y se redondea con ROUND de la hoja
H = {"p": {"valores": [1.0001, 1.0004, 2.0015, 2.0015, 2.0015, -1.0004, -0.0001]}}
anios = [2019, 2020, 2021, 2022, 2023, 2024, 2025]


def entrada(op, sel, terms, red=3):
    return F.calcular_entrada("C99", {"calculo": {"operacion": op, "anios": sel, "terminos": terms, "redondeo": red}}, H, anios)


intento("suma 1,0001 + 1,0004 = 2,0005 → 2,001", lambda: entrada("suma", [2019, 2020], [{"partida": "p"}])["valor"], 2.001)
intento("suma con signo −(1,0001 + 1,0004) → −2,001", lambda: entrada("suma", [2019, 2020], [{"partida": "p", "signo": -1}])["valor"], -2.001)
intento("suma −1,0004 − 0,0001 = −1,0005 → −1,001", lambda: entrada("suma", [2024, 2025], [{"partida": "p"}])["valor"], -1.001)
intento("media de 2,0015 ×3 = 2,0015 → 2,002", lambda: entrada("media", [2021, 2022, 2023], [{"partida": "p"}])["valor"], 2.002)
intento("media (1,0001 + 1,0004)/2 = 1,00025 → 1,0003 a 4 decimales", lambda: entrada("media", [2019, 2020], [{"partida": "p"}], 4)["valor"], 1.0003)
intento("media (1,0001 + 1,0004 + 2,0015)/3 = 1,334 exacto", lambda: entrada("media", [2019, 2020, 2021], [{"partida": "p"}])["valor"], 1.334)
intento("valor sin redondear de la suma = 2,0005 (float de la suma exacta)", lambda: entrada("suma", [2019, 2020], [{"partida": "p"}])["valor_sin_redondear"], 2.0005)

# 5 · construir sobre jumbo_f real (copia temporal): Historia!I17 = 7,0352
t = tempfile.mkdtemp(prefix="redondeo_historia_")
try:
    if os.path.isdir(os.path.join(JUMBO, "fase1_partes")) and os.path.isdir(os.path.join(JUMBO, "texto")):
        c = os.path.join(t, "Jumbo")
        os.makedirs(c)
        for n in ("texto", "fase1_partes", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_decisiones.json"):
            s = os.path.join(JUMBO, n)
            if os.path.isdir(s):
                shutil.copytree(s, os.path.join(c, n))
            elif os.path.exists(s):
                shutil.copy2(s, os.path.join(c, n))
        r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", c], capture_output=True, text=True)
        paso("jumbo_f: construye", r.returncode == 0, (r.stdout + r.stderr).strip()[-160:])
        if r.returncode == 0:
            d = json.load(open(os.path.join(c, "fase1_v63.json"), encoding="utf-8"))
            h = d["historia"]
            i = h["anios"].index(2022)
            v = h["partidas"]["arrendamientos_principal"]["valores"][i]
            paso("jumbo_f: Historia!I17 (arrendamientos_principal 2022) = 7,0352", v == 7.0352, repr(v))
            v = h["partidas"]["circulante"]["valores"][h["anios"].index(2025)]
            paso("jumbo_f: Historia!L14 (circulante 2025, suma de componentes 61,15855) = 61,1586", v == 61.1586, repr(v))
            ok = all(x is None or (Fraction(repr(float(x))) * 10 ** 4).denominator == 1 for p in h["partidas"].values() for x in p["valores"])
            paso("jumbo_f: toda la Historia con 4 decimales como mucho", ok)
    else:  # el expediente del examen no forma parte de todos los paquetes: sin él, la prueba real se omite y lo dice
        print(f"OMITIDA · construir sobre jumbo_f: no está el expediente {JUMBO}")
finally:
    shutil.rmtree(t, ignore_errors=True)

print(f"\n{total - len(fallos)}/{total} comprobaciones PASAN")
sys.exit(1 if fallos else 0)
