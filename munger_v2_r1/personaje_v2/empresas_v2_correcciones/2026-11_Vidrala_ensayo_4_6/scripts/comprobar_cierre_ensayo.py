#!/usr/bin/env python3
"""Controles del expediente regenerado (entrega 4.6, reparación del cierre). Solo lectura.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6/scripts/comprobar_cierre_ensayo.py

1. Integridad de las referencias: originales de empresas_v2/Vidrala/ y expedientes 4.4 y 4.5, con sus huellas del manifiesto.
2. Cierre (I1): pipeline concluido en el paso 14 con una auditoría APROBADO que nombra el material fijado, que sigue sin cambios;
   la primera auditoría de la 4.6, que nombraba una versión anterior del material, se rechazó; ficha oficial con su cierre.
3. Marca (I2), etiqueta de C104 (I3) y avisos de alcance (I4) en la ficha y el informe oficiales.
4. Comparación numérica con la 4.5 (comparar_con_4_5.py, 30 controles) y reproducción de las incidencias antes y después.
"""
import csv
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
PV2 = os.path.abspath(os.path.join(AQUI, "..", ".."))
RAIZ = os.path.dirname(PV2)
E = os.path.join(AQUI, "Vidrala")
sys.path.insert(0, os.path.join(PV2, "scripts"))
import cierre_v2 as CIE  # noqa: E402
import config_v2  # noqa: E402
import pipeline  # noqa: E402

N_OK = N_T = 0


def comprobar(n, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {n}" + (f" · {det}" if det else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def j(*p):
    return json.load(open(os.path.join(*p), encoding="utf-8"))


def seccion(md, n):
    m = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", md, flags=re.M | re.S)
    return m.group(0) if m else ""


print("EXPEDIENTE REGENERADO DEL ENSAYO DE VIDRALA · entrega 4.6 · controles de solo lectura")
print("=" * 100)
print("\n1. REFERENCIAS INTACTAS")
man = {}
for l in open(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"), encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        man[p] = h
for pref, nombre in (("personaje_v2/empresas_v2/", "originales de personaje_v2/empresas_v2/"), ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/", "archivos de la 4.4"),
                     ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_5/", "archivos de la 4.5 (expediente, registro de P1, contraste, controles)")):
    sel = {k: v for k, v in man.items() if k.startswith(pref)}
    comprobar(f"Los {len(sel)} {nombre} conservan su huella del manifiesto", sel and all(os.path.exists(os.path.join(RAIZ, k)) and sha(os.path.join(RAIZ, k)) == v for k, v in sel.items()))
comprobar("Registro humano de P1 sin cambios en la copia 4.6 (SHA-256 b4e47afc…c445a4)", sha(os.path.join(E, "fase1_decisiones.json")) == "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4")

print("\n2. CIERRE (I1)")
st = j(E, "estado_pipeline.json")
fij = CIE.material_fijado(E) or {}
actual, _ = CIE.material(E, "Vidrala")
aud = open(os.path.join(E, "auditoria.md"), encoding="utf-8").read()
comprobar("Pipeline concluido en el paso 14 con auditoría APROBADO", st["paso"] == 14 and st["estado_analisis"] == "concluido" and st.get("auditoria") == "APROBADO")
comprobar("auditoria.md: APROBADO por la regla estricta de H2 y «Material auditado» igual al material fijado", pipeline.Pipeline.veredicto_auditoria(aud) == "APROBADO" and CIE.id_en_auditoria(aud) == fij.get("id") == st.get("material_auditoria"), fij.get("id"))
comprobar("El material actual es el auditado (ningún artefacto cambió después de la aprobación)", actual == fij.get("id"))
comprobar("cierre_v2.motivo_rechazo_cierre: ningún motivo de rechazo", CIE.motivo_rechazo_cierre(E, pipeline.Pipeline.veredicto_auditoria, st, "Vidrala") is None)
h = "\n".join(st["historial"])
prim = open(os.path.join(E, "auditoria_4_6_primera_material_305c3a5b.md"), encoding="utf-8").read()
comprobar("La primera auditoría 4.6 (APROBADO de una versión anterior del material) se rechazó y no cerró", CIE.id_en_auditoria(prim) == "305c3a5bea1c90ab" and "la auditoría corresponde al material 305c3a5bea1c90ab, no al fijado" in h)
comprobar("La auditoría 4.5 se conserva como antecedente (sin línea de material: no sirve para cerrar la 4.6)", CIE.id_en_auditoria(open(os.path.join(E, "auditoria_4_5_antecedente.md"), encoding="utf-8").read()) is None)
fi = j(E, "ficha.json")
fp = j(E, "ficha_provisional.json")
comprobar("ficha.json oficial: concluido con cierre {APROBADO, material auditado} y sin bloque provisional", fi["estado_analisis"] == "concluido" and fi.get("cierre") == {"auditoria": "APROBADO", "material_auditado": fij.get("id")} and "provisional" not in fi)
comprobar("ficha_provisional.json: estado propuesto, confirmado = false, y huella del libro igual a la del libro auditado",
          fp["provisional"]["confirmado"] is False and fp["hashes"]["libro_evaluado"] == fij["archivos"]["Vidrala_v63_evaluada.xlsx"] == sha(os.path.join(E, "Vidrala_v63_evaluada.xlsx")))
filas = list(csv.DictReader(open(os.path.join(AQUI, "resumen_v2.csv"), encoding="utf-8")))
comprobar("resumen_v2.csv: fila concluido con verificación APROBADO", any(r["estado_analisis"] == "concluido" and r["verificacion"] == "APROBADO" for r in filas))

print("\n3. MARCA (I2), ETIQUETA DE C104 (I3) Y AVISOS DE ALCANCE (I4) EN LAS SALIDAS OFICIALES")
inf = open(os.path.join(E, "informe.md"), encoding="utf-8").read()
nec = j(E, "entrada_v63.json")["necesarios_para_listo_provisional"]
comprobar("I2 · ficha: marca «con datos de etapa 1 incompletos» con las causas exactas de entrada_v63.json", (fi.get("datos_etapa1_incompletos") or {}).get("marca") == CIE.MARCA_ETAPA1 and fi["datos_etapa1_incompletos"]["causas"] == nec, f"{len(nec)} causas")
comprobar("I2 · informe: la marca y sus causas en la sección 1, y en ninguna otra", CIE.MARCA_ETAPA1 in seccion(inf, 1) and all(x["dato"] in seccion(inf, 1) for x in nec) and inf.count(CIE.MARCA_ETAPA1) == 1)
fc = j(E, "fase_c.json")
P = pipeline.Pipeline(E, config_v2.cargar(os.path.join(PV2, "config_v2.json")))
comprobar("I3 · C104 con la etiqueta de la tabla para concluido · esperar · no_procede, y coherencia de la fase C sin errores",
          CIE.etiqueta_en_c104(fc["celdas"]["C104"]) == "no procede (conclusión no favorable)" and CIE.motivo_c104_fundamento(fc["estado_analisis"], fc["decision"]["accion"], fc["fundamento_material"]["resultado"], fc["celdas"]["C104"]) is None and P.coherencia_fase_c(fc) is None)
al = j(E, "alcance_v2.json")
comprobar("I4 · ficha.alcance igual a alcance_v2.json", fi.get("alcance") == al)
for n in (1, 6, 7):
    comprobar(f"I4 · informe, sección {n} leída por separado: el aviso una vez", seccion(inf, n).count(al["aviso"]) == 1)
comprobar("I4 · el aviso no aparece en otras secciones (3 apariciones en total) y el informe oficial no lleva la nota de material provisional",
          inf.count(al["aviso"]) == 3 and "Material provisional" not in inf)

print("\n4. COMPARACIÓN NUMÉRICA CON LA 4.5 Y REPRODUCCIÓN")
r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "scripts", "comparar_con_4_5.py")], capture_output=True, text=True)
comprobar("comparar_con_4_5.py: 30 de 30 controles iguales o cumplidos, y la salida conservada es idéntica",
          r.returncode == 0 and "RESULTADO: 30 de 30" in r.stdout and open(os.path.join(AQUI, "resultados", "comparacion_con_4_5.md"), encoding="utf-8").read() in r.stdout)
antes = open(os.path.join(AQUI, "reproduccion", "reproduccion_codigo_4_5.txt"), encoding="utf-8").read()
despues = open(os.path.join(AQUI, "reproduccion", "reproduccion_codigo_4_6.txt"), encoding="utf-8").read()
comprobar("Reproducción con el código 4.5: las cuatro incidencias (cinco comprobaciones) REPRODUCIDAS", antes.count("REPRODUCIDA") == 5 and "NO SE REPRODUCE" not in antes)
comprobar("Reproducción con el código 4.6: ninguna se reproduce", despues.count("NO SE REPRODUCE") == 5 and "REPRODUCIDA" not in despues)
print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
