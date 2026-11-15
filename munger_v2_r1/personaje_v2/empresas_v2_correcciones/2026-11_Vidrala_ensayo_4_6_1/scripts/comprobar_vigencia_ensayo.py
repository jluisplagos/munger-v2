#!/usr/bin/env python3
"""Controles del expediente regenerado de la entrega 4.6.1 (vigencia de las salidas oficiales). Solo lectura.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_vigencia_ensayo.py
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
import pipeline  # noqa: E402

N_OK = N_T = 0
V = pipeline.Pipeline.veredicto_auditoria


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


print("EXPEDIENTE DEL ENSAYO DE VIDRALA · entrega 4.6.1 · vigencia de las salidas oficiales · controles de solo lectura")
print("=" * 100)
print("\n1. REFERENCIAS INTACTAS")
man = {}
for l in open(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"), encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        man[p] = h
for pref, nombre in (("personaje_v2/empresas_v2/", "originales de personaje_v2/empresas_v2/"), ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/", "archivos de la 4.4"),
                     ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_5/", "archivos de la 4.5"), ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_6/", "archivos de la 4.6")):
    sel = {k: v for k, v in man.items() if k.startswith(pref)}
    comprobar(f"Los {len(sel)} {nombre} conservan su huella del manifiesto", sel and all(os.path.exists(os.path.join(RAIZ, k)) and sha(os.path.join(RAIZ, k)) == v for k, v in sel.items()))
comprobar("Registro humano de P1 sin cambios (SHA-256 b4e47afc…c445a4)", sha(os.path.join(E, "fase1_decisiones.json")) == "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4")

print("\n2. VIGENCIA DEL CIERRE ACTUAL")
st = j(E, "estado_pipeline.json")
fij = (CIE.material_fijado(E) or {}).get("id")
comprobar("Pipeline concluido en el paso 14 con auditoría APROBADO del material fijado, que no ha cambiado", st["paso"] == 14 and st["estado_analisis"] == "concluido" and st.get("auditoria") == "APROBADO"
          and CIE.material(E)[0] == fij == st.get("material_auditoria") and CIE.id_en_auditoria(open(os.path.join(E, "auditoria.md"), encoding="utf-8").read()) == fij, fij)
comprobar("cierre_v2.motivo_vigencia: las salidas oficiales son vigentes (ficha e informe registrados en cierre_vigente.json)", CIE.motivo_vigencia(E, V) is None)
cv = j(E, "cierre_vigente.json")
comprobar("cierre_vigente.json: material, ficha, informe y auditoría actuales", cv["material_auditado"] == fij and cv["ficha_sha256"] == sha(os.path.join(E, "ficha.json"))
          and cv["informe_sha256"] == sha(os.path.join(E, "informe.md")) and cv["auditoria_sha256"] == sha(os.path.join(E, "auditoria.md")))
fi = j(E, "ficha.json")
comprobar("ficha.json oficial con cierre {APROBADO, material fijado}", fi.get("cierre") == {"auditoria": "APROBADO", "material_auditado": fij} and "provisional" not in fi)
filas = list(csv.DictReader(open(os.path.join(AQUI, "resumen_v2.csv"), encoding="utf-8")))
mias = [r for r in filas if r["empresa"] == "Vidrala, S.A."]
comprobar("resumen_v2.csv: una sola fila activa, concluido / APROBADO", len(mias) == 1 and mias[0]["estado_analisis"] == "concluido" and mias[0]["verificacion"] == "APROBADO")

print("\n3. CIERRE ANTERIOR ARCHIVADO (NO VIGENTE) Y SU HISTORIAL")
H = os.path.join(E, "historial_cierres")
arch = sorted(os.listdir(H))
r = j(H, arch[0], "RETIRADA.json") if arch else {}
comprobar("historial_cierres/ con el cierre 4.6 archivado (01_74b94f8072dd58c1) y su RETIRADA.json", arch == ["01_74b94f8072dd58c1"] and r.get("material_auditado_en_la_aprobacion") == "74b94f8072dd58c1"
          and r.get("motivo") == "no hay auditoria.md" and r.get("estado_que_presentaba") == "concluido", ", ".join(arch))
E46 = os.path.join(os.path.dirname(AQUI), "2026-11_Vidrala_ensayo_4_6", "Vidrala")
comprobar("la ficha y el informe archivados son exactamente los oficiales de la 4.6", sha(os.path.join(H, arch[0], "ficha.json")) == sha(os.path.join(E46, "ficha.json")) and sha(os.path.join(H, arch[0], "informe.md")) == sha(os.path.join(E46, "informe.md")))
comprobar("la auditoría 4.6 se conserva sin cambios como antecedente", sha(os.path.join(E, "auditoria_4_6_antecedente.md")) == sha(os.path.join(E46, "auditoria.md")))
hf = list(csv.DictReader(open(os.path.join(AQUI, "resumen_v2_historial.csv"), encoding="utf-8")))
comprobar("resumen_v2_historial.csv conserva la fila anterior concluido / APROBADO con su material y motivo de retirada",
          any(x["empresa"] == "Vidrala, S.A." and x["estado_analisis"] == "concluido" and x["verificacion"] == "APROBADO" and x["material_auditado"] == "74b94f8072dd58c1" and x["retirada_motivo"] for x in hf))
comprobar("estado_pipeline.json registra la retirada en cierres_archivados", any(x.get("material_auditado") == "74b94f8072dd58c1" and x.get("auditoria_registrada") == "APROBADO" for x in st.get("cierres_archivados", [])))

print("\n4. MARCAS, ETIQUETAS Y AVISOS DE LA 4.6 CONSERVADOS EN LAS SALIDAS OFICIALES")
inf = open(os.path.join(E, "informe.md"), encoding="utf-8").read()
nec = j(E, "entrada_v63.json")["necesarios_para_listo_provisional"]
comprobar("marca «con datos de etapa 1 incompletos» con las causas exactas (ficha y sección 1)", fi["datos_etapa1_incompletos"]["causas"] == nec and CIE.MARCA_ETAPA1 in seccion(inf, 1))
fc = j(E, "fase_c.json")
comprobar("C104 con la etiqueta de la tabla cerrada", CIE.motivo_c104_fundamento(fc["estado_analisis"], fc["decision"]["accion"], fc["fundamento_material"]["resultado"], fc["celdas"]["C104"]) is None)
al = j(E, "alcance_v2.json")
comprobar("aviso de alcance una vez en cada una de las secciones 1, 6 y 7 y en ficha.alcance", all(seccion(inf, n).count(al["aviso"]) == 1 for n in (1, 6, 7)) and inf.count(al["aviso"]) == 3 and fi.get("alcance") == al)

print("\n5. COMPARACIÓN CON LA 4.6, REPRODUCCIÓN E INTEGRACIÓN EN EL VERIFICADOR")
for script, esperado, salida in (("comparar_con_4_6.py", "RESULTADO: 32 de 32", "comparacion_con_4_6.md"), ("comprobar_integracion_verificador.py", "RESULTADO: 13 de 13", "comprobar_integracion_verificador_salida.txt")):
    rr = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "scripts", script)], capture_output=True, text=True)
    comprobar(f"{script}: «{esperado}» y la salida conservada es idéntica", rr.returncode == 0 and esperado in rr.stdout and open(os.path.join(AQUI, "resultados", salida), encoding="utf-8").read().strip() in rr.stdout)
antes = open(os.path.join(AQUI, "reproduccion", "reproduccion_codigo_4_6.txt"), encoding="utf-8").read()
despues = open(os.path.join(AQUI, "reproduccion", "reproduccion_codigo_4_6_1.txt"), encoding="utf-8").read()
comprobar("reproducción con el código 4.6: el caso se reproduce en sus tres rutas", antes.count("REPRODUCIDO") == 3 and "NO SE REPRODUCE" not in antes)
comprobar("reproducción con el código 4.6.1: no se reproduce en ninguna", despues.count("NO SE REPRODUCE") == 3 and "REPRODUCIDO:" not in despues)
pa = open(os.path.join(AQUI, "reproduccion", "pruebas_aceptacion_con_codigo_4_6.txt"), encoding="utf-8").read()
comprobar("las pruebas de aceptación nuevas fallan con el código 4.6 (43/55: las 12 negativas en FALLA)", "43/55 pruebas de aceptación del cierre PASAN" in pa and pa.count("\nFALLA") == 12)
print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
