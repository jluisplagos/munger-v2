#!/usr/bin/env python3
"""Controles del expediente de continuación del ensayo de Vidrala (entrega 4.5). Solo lectura: no escribe en el paquete.

Uso: python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_5/scripts/comprobar_continuacion.py

Secciones:
  1. Registro humano de P1: archivo recibido conservado, incorporado byte a byte y válido (10 requisitos).
  2. Referencias intactas: expediente de la 4.4 y originales de empresas_v2/Vidrala/ (huellas del manifiesto) y entradas
     del ensayo heredadas de la 4.4 sin cambios en la copia de continuación.
  3. Construcción (fase1_v63.json) frente al original: solo cambia el circulante de 2024; metadatos iguales; 38 ceros pendientes.
  4. Libro de datos recalculado frente al libro evaluado original: Historia difiere solo en K14 y en sus celdas derivadas.
  5. Comprobación de entrada: 0 bloqueantes, motores calculables.
  6. Fases, resultados y estado (se añade cuando las fases existen).
"""
import hashlib
import json
import os
import re
import subprocess
import sys

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
PV2 = os.path.dirname(CORR)
RAIZ = os.path.dirname(PV2)
E = os.path.join(AQUI, "Vidrala")
E44 = os.path.join(CORR, "2026-11_Vidrala_ensayo", "Vidrala")
O = os.path.join(PV2, "empresas_v2", "Vidrala")
SHA_P1 = "b4e47afcb3ddbc6bda35bff9f20c8cfc6881c0b800bc731a34e4205b63c445a4"
N_OK = N_T = 0


def comprobar(nombre, cond, detalle=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    print(f"  [{'CUMPLE' if cond else 'NO CUMPLE'}] {nombre}" + (f" · {detalle}" if detalle else ""))


def sha(p):
    with open(p, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()


def hojas(x, r=""):
    if isinstance(x, dict):
        for k, v in x.items():
            yield from hojas(v, f"{r}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x):
            yield from hojas(v, f"{r}[{i}]")
    else:
        yield r, x


print("EXPEDIENTE DE CONTINUACIÓN DEL ENSAYO DE VIDRALA · entrega 4.5 · controles de solo lectura")
print("=" * 100)

print("\n1. REGISTRO HUMANO DE P1")
rec = os.path.join(AQUI, "registro_P1", "PROPUESTA_fase1_decisiones_con_P1_cumplimentada.json")
comprobar("Archivo recibido conservado con su huella (SHA-256 b4e47afc…c445a4)", sha(rec) == SHA_P1)
comprobar("fase1_decisiones.json del expediente idéntico byte a byte al archivo recibido", sha(os.path.join(E, "fase1_decisiones.json")) == SHA_P1)
r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "scripts", "validar_registro_P1.py"), rec], capture_output=True, text=True)
comprobar("validar_registro_P1.py: 10 de 10 requisitos (decisiones anteriores, solo circulante_lineas 2024, 84.994, fuente, campos humanos)",
          r.returncode == 0 and "RESULTADO: 10 de 10" in r.stdout, r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
comprobar("Salida de la validación conservada idéntica (registro_P1/validacion_salida.txt)",
          open(os.path.join(AQUI, "registro_P1", "validacion_salida.txt"), encoding="utf-8").read().replace(rec, "").splitlines()[2:] == r.stdout.replace(rec, "").splitlines()[2:])

print("\n2. REFERENCIAS INTACTAS")
man = {}
for l in open(os.path.join(RAIZ, "MANIFIESTO_SHA256.txt"), encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        man[p] = h
for pref, nombre in (("personaje_v2/empresas_v2/Vidrala/", "originales de empresas_v2/Vidrala/"),
                     ("personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/", "archivos de la entrega 4.4 (expediente, fuentes, documentos, script y salidas)")):
    sel = {k: v for k, v in man.items() if k.startswith(pref)}
    comprobar(f"Los {len(sel)} {nombre} conservan su huella del manifiesto", sel and all(os.path.exists(os.path.join(RAIZ, k)) and sha(os.path.join(RAIZ, k)) == v for k, v in sel.items()))
here = sorted(os.path.relpath(os.path.join(d, f), E44) for d, _, fs in os.walk(E44) for f in fs)
dif = [p for p in here if p not in ("fase1_decisiones.json", "LEEME_ANTES_DE_CONTINUAR.md") and (not os.path.exists(os.path.join(E, p)) or (p != "estado_pipeline.json" and sha(os.path.join(E, p)) != sha(os.path.join(E44, p))))]
comprobar("La copia de continuación conserva todos los archivos de entrada de la 4.4 sin cambios (salvo fase1_decisiones.json, el estado del pipeline y el LÉEME de la 4.4, sustituido por el de la 4.5)", not dif, ", ".join(dif[:5]))

print("\n3. CONSTRUCCIÓN (fase1_v63.json) FRENTE AL ORIGINAL")
a = json.load(open(os.path.join(O, "fase1_v63.json"), encoding="utf-8"))
b = json.load(open(os.path.join(E, "fase1_v63.json"), encoding="utf-8"))
va = {k: v["valores"] for k, v in a["historia"]["partidas"].items()}
vb = {k: v["valores"] for k, v in b["historia"]["partidas"].items()}
difs = [(k, i, x, y) for k in sorted(set(va) | set(vb)) for i, (x, y) in enumerate(zip(va.get(k, []), vb.get(k, []))) if x != y]
comprobar("Mismas 21 partidas y mismos años", a["historia"]["anios"] == b["historia"]["anios"] and set(va) == set(vb), str(len(vb)))
comprobar("Historia: la única diferencia de valor es el circulante de 2024 (−127,84 → 84,994)", difs == [("circulante", 8, -127.84, 84.994)], str(difs))
meta = [k for k in a if not isinstance(a[k], (dict, list))] + ["precio", "acciones_diluidas", "capitalizacion", "tasa_sin_riesgo", "geografia"]
comprobar("Metadatos (precio, acciones, capitalización, fecha, tasa sin riesgo, geografía…) iguales a los originales", all(a.get(k) == b.get(k) for k in meta),
          ", ".join(k for k in meta if a.get(k) != b.get(k)))
comprobar("La fuente del circulante de 2024 recoge la decisión humana registrada (persona y fecha del registro)",
          "decisión de Jose Luis Pino Lagos el 2026-11-09" in b["historia"]["partidas"]["circulante"]["fuente"])
pv = b.get("pendientes_verificacion", [])
comprobar("38 ceros PENDIENTES de verificación en fase1_v63.json (la IA no confirma ceros)", len(pv) == 38, str(len(pv)))
st = json.load(open(os.path.join(E, "estado_pipeline.json"), encoding="utf-8"))
hc = [h for h in st["historial"] if "fase1_historia.py construir" in h]
comprobar("construir registró 38 ceros pendientes y 0 confirmados por decisión humana", hc and "38 ceros pendientes de verificación, 0 confirmados por decisión humana" in hc[0], hc[0][-160:] if hc else "")
ar = [p for p in os.listdir(os.path.join(E, "fase1_partes"))]
comprobar("AR_*.json de la copia idénticos a los de la 4.4 (P8 y citas de ceros conservadas)", all(sha(os.path.join(E, "fase1_partes", p)) == sha(os.path.join(E44, "fase1_partes", p)) for p in ar), str(len(ar)))

print("\n4. LIBRO DE DATOS RECALCULADO FRENTE AL LIBRO EVALUADO ORIGINAL (Historia)")
import openpyxl  # noqa: E402
wo = openpyxl.load_workbook(os.path.join(O, "Vidrala_v63_evaluada.xlsx"), data_only=True)["Historia"]
wn = openpyxl.load_workbook(os.path.join(E, "recalc", "Vidrala_v63_datos.xlsx"), data_only=True)["Historia"]
wf = openpyxl.load_workbook(os.path.join(E, "Vidrala_v63_datos.xlsx"))["Historia"]
num, txt = {}, []
for row in wo.iter_rows():
    for c in row:
        x, y = c.value, wn[c.coordinate].value
        if x == y:
            continue
        if isinstance(x, (int, float)) and isinstance(y, (int, float)):
            if abs(x - y) > 1e-9:
                num[c.coordinate] = (x, y)
        else:
            txt.append(c.coordinate)
esperadas = {"K14", "K30", "K31", "C53", "C58", "C76", "C77", "C79", "C80"}
comprobar("Celdas numéricas distintas: K14 y sus derivadas (K30, K31, C53, C58, C76, C77, C79, C80)", set(num) == esperadas, ", ".join(sorted(num)))
comprobar("K14 = 84,994 (antes −127,84)", num.get("K14") == (-127.84, 84.994))
comprobar("C53 (S2C de referencia) ≈ 0,9159 (antes 1,5492)", "C53" in num and abs(num["C53"][1] - 0.915854136) < 1e-6 and abs(num["C53"][0] - 1.549216602) < 1e-6, f"{num.get('C53')}")
comprobar("C58 (f de referencia) ≈ −0,027608 (antes 0,019890)", "C58" in num and abs(num["C58"][1] + 0.0276078) < 1e-6 and abs(num["C58"][0] - 0.0198902) < 1e-6, f"{num.get('C58')}")
dep = {c: str(wf[c].value) for c in esperadas - {"K14"}}
comprobar("Las otras ocho son fórmulas que dependen de la fila 14 (directamente o por la fila 31 o C58)",
          all(v.startswith("=") and re.search(r"K14|\$C\$14:\$L\$14|C14:L14|H31:L31|K30|\$C\$58|\$C\$7[5-9]", v) for v in dep.values()),
          "; ".join(f"{c}: {v[:50]}" for c, v in sorted(dep.items()) if not re.search(r"K14|\$C\$14:\$L\$14|C14:L14|H31:L31|K30|\$C\$58|\$C\$7[5-9]", v)))
comprobar("Las demás diferencias son notas y fuentes de la columna M y C68 (=Palancas!C9, que escribe la fase B; vacía antes de las fases)",
          all(re.fullmatch(r"M\d+", c) for c in txt if c != "C68") and ("C68" not in txt or str(wf["C68"].value) == "=Palancas!$C9"), ", ".join(txt[:10]))

print("\n5. COMPROBACIÓN DE ENTRADA")
ent = json.load(open(os.path.join(E, "entrada_v63.json"), encoding="utf-8"))
comprobar("0 bloqueantes y libro íntegro", ent["bloqueantes"] == [] and ent["integro"] is True)
comprobar("Motores A, B y C calculables", all(ent["motores"][m]["calculable"] for m in "ABC"))
nec = [x["dato"] for x in ent["necesarios_para_listo_provisional"]]
comprobar("6 evidencias pendientes para LISTO · PROVISIONAL (C48 y los ceros pendientes), visibles", len(nec) == 6, "; ".join(nec))

if os.path.exists(os.path.join(AQUI, "scripts", "comprobar_continuacion_fases.py")):
    print("\n6. FASES, RESULTADOS Y ESTADO")
    sys.path.insert(0, os.path.join(AQUI, "scripts"))
    import comprobar_continuacion_fases as F  # noqa: E402
    for nombre, cond, det in F.comprobaciones(AQUI, E, O, RAIZ):
        comprobar(nombre, cond, det)

print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
