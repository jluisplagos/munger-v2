#!/usr/bin/env python3
"""Comprueba que la batería de cierre es obligatoria en `verificar_paquete.sh completa` (encargo 4.6.1, §8). Solo trabaja en temporales.

Uso: python3 -I comprobar_integracion_verificador.py

Extrae del verificador real el bloque «batería de cierre» y lo ejecuta, en modo completa y en modo rápido, contra sustitutos de
test_cierre_v2.py: ausente, con fallo, interrumpido sin línea final, con menos de 55 pruebas, con una prueba en FALLA y correcto.
El bloque tiene que sumar un fallo (el resultado global no puede ser PASA) en todos los casos salvo el correcto, y en el modo
rápido tiene que decir que la batería se omite (su PASA no la cubre).
"""
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
v = open(os.path.join(RAIZ, "verificar_paquete.sh"), encoding="utf-8").read()
m = re.search(r'^echo "== batería de cierre.*?(?=^echo "RESULTADO GLOBAL)', v, flags=re.M | re.S)
N_OK = N_T = 0


def comprobar(n, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {n}" + (f" · {det}" if det else ""))


comprobar("verificar_paquete.sh contiene el bloque de la batería de cierre antes del resultado global", m is not None)
bloque = m.group(0) if m else ""
SUSTITUTOS = {
    "ausente": None,
    "falla (código 1)": "print('1/55 pruebas de aceptación del cierre PASAN'); raise SystemExit(1)",
    "interrumpida sin línea final (código 0)": "print('PASA · algo')",
    "menos de 55 pruebas": "print('40/40 pruebas de aceptación del cierre PASAN')",
    "una prueba en FALLA con código 0": "print('54/55 pruebas de aceptación del cierre PASAN')",
    "correcta": "print('55/55 pruebas de aceptación del cierre PASAN')",
}
for nombre, cuerpo in SUSTITUTOS.items():
    for modo in ("completa", "rapida"):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "personaje_v2", "pruebas"))
            if cuerpo is not None:
                open(os.path.join(t, "personaje_v2", "pruebas", "test_cierre_v2.py"), "w", encoding="utf-8").write(cuerpo + "\n")
            guion = os.path.join(t, "bloque.sh")
            open(guion, "w", encoding="utf-8").write("set -uo pipefail\ncd \"$(dirname \"$0\")\"\nfallos=0\n" + bloque + "\necho \"FALLOS=$fallos\"\n")
            r = subprocess.run(["bash", guion] + (["completa"] if modo == "completa" else []), capture_output=True, text=True)
            fallos = re.search(r"FALLOS=(\d+)", r.stdout)
            f = int(fallos.group(1)) if fallos else -1
            if modo == "completa":
                esperado = 0 if nombre == "correcta" else 1
                comprobar(f"modo completa · batería {nombre}: {'PASA' if esperado == 0 else 'FALLA'} y suma {esperado} fallo(s)", f == esperado, re.sub(r"ver /\S+", "ver <temporal>", r.stdout.strip().splitlines()[-2])[:140] if r.stdout.strip() else "")
            else:
                comprobar(f"modo rápido · batería {nombre}: se declara omitida y no suma fallos", f == 0 and "omitida en el modo rápido" in r.stdout)
print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
