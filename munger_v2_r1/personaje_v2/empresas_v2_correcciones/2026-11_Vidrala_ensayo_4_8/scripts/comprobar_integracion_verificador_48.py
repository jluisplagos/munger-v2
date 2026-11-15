#!/usr/bin/env python3
"""Comprueba que la batería de COHERENCIA DE ESTADOS (4.8, X-a y X-c) es obligatoria en `verificar_paquete.sh completa`, como las del
resumen y de cierre, con un mínimo de 28 pruebas. Solo en temporales.

(Adaptación del control de la 4.7.1, `…_4_7_1/scripts/comprobar_integracion_verificador_471.py`. El bloque nuevo va antes del del
resumen para que los controles de la 4.6.1, la 4.7 y la 4.7.1, que extraen sus bloques por posición, sigan extrayendo los mismos.)

Uso: python3 -I comprobar_integracion_verificador_48.py

Extrae del verificador real el bloque «batería de coherencia de estados» y lo ejecuta, en modo completa y en modo rápido, contra
sustitutos de test_estados_v2.py: ausente, con fallo, interrumpido sin línea final, con menos de 28 pruebas, con una prueba en FALLA
y correcto.
El bloque tiene que sumar un fallo (el resultado global no puede ser PASA) en todos los casos salvo el correcto, y en el modo
rápido tiene que decir que la batería se omite (su PASA no la cubre).
"""
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BAT, FRASE, MINIMO = "test_estados_v2.py", "pruebas de coherencia de estados PASAN", 28
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
v = open(os.path.join(RAIZ, "verificar_paquete.sh"), encoding="utf-8").read()
m = re.search(r'^echo "== batería de coherencia de estados.*?(?=^echo "== batería del resumen)', v, flags=re.M | re.S)
N_OK = N_T = 0


def comprobar(n, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {n}" + (f" · {det}" if det else ""))


comprobar("verificar_paquete.sh contiene el bloque obligatorio de la batería de coherencia de estados", m is not None)
bloque = m.group(0) if m else ""
SUSTITUTOS = {
    "ausente": None,
    "falla (código 1)": "print('1/28 pruebas de coherencia de estados PASAN'); raise SystemExit(1)",
    "interrumpida sin línea final (código 0)": "print('PASA · algo')",
    "menos de 28 pruebas": "print('27/27 pruebas de coherencia de estados PASAN')",
    "una prueba en FALLA con código 0": "print('27/28 pruebas de coherencia de estados PASAN')",
    "correcta": "print('28/28 pruebas de coherencia de estados PASAN')",
}
for nombre, cuerpo in SUSTITUTOS.items():
    for modo in ("completa", "rapida"):
        with tempfile.TemporaryDirectory() as t:
            os.makedirs(os.path.join(t, "personaje_v2", "pruebas"))
            if cuerpo is not None:
                open(os.path.join(t, "personaje_v2", "pruebas", BAT), "w", encoding="utf-8").write(cuerpo + "\n")
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
