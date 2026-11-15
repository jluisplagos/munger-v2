#!/usr/bin/env python3
"""Comprobante externo del libro final (entrega 4.10, P-N2). Lo llama verificar_todo.sh al final, DESPUÉS de todas las escrituras
del libro evaluado (también de la incorporación de cachés).

Uso: acreditar_libro.py CARPETA LIBRO_EVALUADO LIBRO_ENTRADA REFERENCIA VERIFICADOR CACHES
     CACHES: «incorporadas» (había copia recalculada y add_cached_values + verificar_v63 pasaron), «sin_copia_recalculada» (no había
     copia recalculada: el libro final es el verificado antes) o «fallidas» (había copia, pero la incorporación o su verificación
     fallaron: el libro final sigue siendo el de antes).

Hasta la 4.10, verificacion_integridad.txt (escrito ANTES de las cachés) acreditaba un archivo distinto del entregado, y la verificación
posterior nombraba el temporal con_cache.tmp.xlsx. Este script:
  1. vuelve a verificar el ARCHIVO FINAL (verificar_v63.py) y deja su salida en verificacion_libro_final.txt;
  2. escribe acreditacion_libro.json, fuera del libro (el libro no lleva su propio hash ni ninguna referencia circular), con tres
     identidades distintas: libro de entrada, libro evaluado verificado antes de las cachés (lo que acredita verificacion_integridad.txt)
     y archivo final (SHA-256, bytes y su verificación).
Una modificación posterior del libro invalida la correspondencia (cierre_v2.motivo_acreditacion_libro). No cambia fórmulas, valores
ni criterios. Código 0 si el archivo final está ÍNTEGRO; 1 si no.
"""
import datetime as dt
import hashlib
import json
import os
import re
import subprocess
import sys


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    c, ev, en, ref, ver, caches = sys.argv[1:7]
    r = subprocess.run([sys.executable, ver, ev, ref], capture_output=True, text=True)
    salida = (r.stdout + r.stderr)
    open(os.path.join(c, "verificacion_libro_final.txt"), "w", encoding="utf-8").write(salida)
    veredicto = next((l.split(":", 1)[1].strip() for l in salida.splitlines() if l.startswith("VEREDICTO:")), None)
    previa = ""
    p_int = os.path.join(c, "verificacion_integridad.txt")
    if os.path.isfile(p_int):
        previa = open(p_int, encoding="utf-8", errors="replace").read()
    m = re.search(r"SHA-256 ([0-9a-f]{8,64})", previa)
    final = sha(ev)
    reg = {
        "nota": ("Comprobante EXTERNO al libro (4.10, P-N2): se escribe después de todas las escrituras del libro evaluado. "
                 "verificacion_integridad.txt acredita el libro evaluado ANTES de las cachés; el archivo entregado es «archivo_final»."),
        "libro_entrada": {"archivo": os.path.basename(en), "sha256": sha(en) if os.path.isfile(en) else None},
        "libro_evaluado_verificado_antes_de_caches": {"informe": "verificacion_integridad.txt", "sha256_prefijo": m.group(1) if m else None},
        "caches": caches,
        "archivo_final": {"archivo": os.path.basename(ev), "sha256": final, "bytes": os.path.getsize(ev),
                          "verificacion": "verificacion_libro_final.txt", "veredicto": veredicto,
                          "igual_al_verificado_antes_de_caches": bool(m) and final.startswith(m.group(1))},
        "escrito": dt.datetime.now().astimezone().isoformat(timespec="seconds"),
    }
    json.dump(reg, open(os.path.join(c, "acreditacion_libro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    ok = r.returncode == 0 and bool(veredicto) and veredicto.startswith("ÍNTEGRO")
    print(f"acreditacion_libro.json · archivo final {os.path.basename(ev)} SHA-256 {final[:16]}… · cachés {caches} · verificación final {veredicto}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
