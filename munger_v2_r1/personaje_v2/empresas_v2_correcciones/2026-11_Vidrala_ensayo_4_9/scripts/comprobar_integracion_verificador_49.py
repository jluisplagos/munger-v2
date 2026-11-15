#!/usr/bin/env python3
"""Comprueba que la batería de INTEGRIDAD DE LA AUDITORÍA VIGENTE (4.9, R-V1) es obligatoria en `verificar_paquete.sh completa`, como
las de solicitudes, estados, resumen y cierre, con un mínimo de 103 pruebas. Solo en temporales.

(Adaptación del control de la 4.8.1, `…_4_8_1/scripts/comprobar_integracion_verificador_481.py`. El bloque nuevo va antes del de
solicitudes de auditoría para que los controles de la 4.6.1 a la 4.8.1, que extraen sus bloques por posición, sigan extrayendo los mismos.)

Uso: python3 -I comprobar_integracion_verificador_49.py

Extrae del verificador real el bloque «batería de integridad de la auditoría vigente» y lo ejecuta, en modo completa y en modo
rápido, contra sustitutos de test_integridad_auditoria_v2.py: ausente, con fallo, interrumpido sin línea final, con menos de 103
pruebas, con una prueba en FALLA y correcto.
El bloque tiene que sumar un fallo (el resultado global no puede ser PASA) en todos los casos salvo el correcto, y en el modo
rápido tiene que decir que la batería se omite (su PASA no la cubre).
"""
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
BAT, FRASE, MINIMO = "test_integridad_auditoria_v2.py", "pruebas de integridad de la auditoría vigente PASAN", 103
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", ".."))
v = open(os.path.join(RAIZ, "verificar_paquete.sh"), encoding="utf-8").read()
m = re.search(r'^echo "== batería de integridad de la auditoría vigente.*?(?=^echo "== batería de solicitudes de auditoría)', v, flags=re.M | re.S)
N_OK = N_T = 0


def comprobar(n, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {n}" + (f" · {det}" if det else ""))


comprobar("verificar_paquete.sh contiene el bloque obligatorio de la batería de integridad de la auditoría vigente, antes del de solicitudes", m is not None)
bloque = m.group(0) if m else ""
SUSTITUTOS = {
    "ausente": None,
    "falla (código 1)": "print('1/103 pruebas de integridad de la auditoría vigente PASAN'); raise SystemExit(1)",
    "interrumpida sin línea final (código 0)": "print('PASA · algo')",
    "menos de 103 pruebas": "print('102/102 pruebas de integridad de la auditoría vigente PASAN')",
    "una prueba en FALLA con código 0": "print('102/103 pruebas de integridad de la auditoría vigente PASAN')",
    "correcta": "print('103/103 pruebas de integridad de la auditoría vigente PASAN')",
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
