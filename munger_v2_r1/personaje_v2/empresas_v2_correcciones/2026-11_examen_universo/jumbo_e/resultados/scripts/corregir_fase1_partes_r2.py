#!/usr/bin/env python3
"""jumbo_e · correcciones de extracción comprobadas (encargo del coordinador del 18-nov-2026, noche, tras la revisión independiente del
registro de Jumbo: munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/jumbo/revision_registro/REVISION.md y REVISION.tsv @ 57e417a).
Cada cambio se comprobó antes en texto/ (página y línea literales).
 1) J3 también en la columna 1-ene–31-dic-2019 de AR2020 p. 59: el emisor rotula «Lease repayments (1.488.677)» lo que la nota de costes
    financieros (AR2020 p. 86) da como «Interest expense on lease liabilities … 1.488.678», e «Interest paid for leases (4.312.789)» lo que es el
    principal; el informe de transición (p. 57) rotula bien («Lease repayments (4.162.252)», «Interest paid for leases (1.488.679)»). Misma
    corrección que J3 para 2020–2025 (cambio_jumbo_c.json): Historia F15 = 7,124703 + 1,488677 = 8,6134; F16 = 1,4887; F17 = 4,3128.
 2) Ceros con cita que no los prueba: intereses en financiación 2016–2018 (cita → la línea «Interest payable» del bloque de EXPLOTACIÓN, que es
    donde están los intereses pagados), principal de arrendamientos 2016 (cita → la nota de compromisos: solo arrendamientos operativos, antes
    de la NIIF 16), pasivo por arrendamientos 2018 (cita → la frase de aplicación de la NIIF 16), adquisiciones 2019 y 2021 (de un cero sin
    prueba a la línea «Share Capital Change of Subsidiaries» con «-» impreso en la columna del grupo de ese año: AR2020 p. 59 y AR2022 p. 68).
Uso: python3 -I corregir_fase1_partes_r2.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import copy, hashlib, json, os, shutil, sys
C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
P = os.path.join(C, "fase1_partes")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
anios = (2016, 2017, 2018, 2020, 2022)
docs = {a: json.load(open(os.path.join(P, f"AR_{a}.json"), encoding="utf-8")) for a in anios}
nuevos = copy.deepcopy(docs)
cambios = []
LR = "Lease repayments                                                                      (3.408.176)            (1.488.677)            (1.488.679)"
IPL = "Interest paid for leases                                                             (7.769.683)            (4.312.789)            (4.162.252)"
J3 = ("J3 en la columna 2019 (año natural) de AR2020 p. 59: etiquetas cruzadas por el emisor; la nota de costes financieros AR2020 p. 86 da "
      "«Interest expense on lease liabilities 3.408.176 1.488.678 1.488.678» (2020, 2019, 1-jul–31-dic-2019) y el informe de transición p. 57 rotula bien")


def e(concepto, impreso, pagina, linea):
    return {"concepto": concepto, "impreso": impreso, "pagina": pagina, "linea": linea}


def cambia(a, partida, campo, esperado, nuevo, motivo, indice=None):
    p = nuevos[a]["partidas"][partida]
    actual = p.get(campo) if indice is None else (p.get(campo) or [None] * (indice + 1))[indice]
    if actual != esperado:
        sys.exit(f"DETENIDO (nada escrito): AR_{a} · {partida} · {campo}[{indice}]: se esperaba {json.dumps(esperado, ensure_ascii=False)[:200]} y hay {json.dumps(actual, ensure_ascii=False)[:200]}")
    if indice is None:
        p[campo] = nuevo
    else:
        p[campo][indice] = nuevo
    cambios.append({"archivo": f"fase1_partes/AR_{a}.json", "partida": partida, "campo": campo, "indice": indice, "antes": esperado, "despues": nuevo, "motivo": motivo})


d = docs[2020]["partidas"]
cambia(2020, "intereses", "anterior", d["intereses"]["anterior"][1],
       e("Lease repayments 2019 (etiqueta del emisor; es el INTERÉS de arrendamientos: etiquetas cruzadas, J3)", "(1.488.677)", 59, LR), J3, indice=1)
cambia(2020, "intereses_financiacion", "anterior", d["intereses_financiacion"]["anterior"][0],
       e("Lease repayments 2019 (etiqueta del emisor; es el INTERÉS de arrendamientos: etiquetas cruzadas, J3)", "(1.488.677)", 59, LR), J3, indice=0)
cambia(2020, "arrendamientos_principal", "anterior", d["arrendamientos_principal"]["anterior"][0],
       e("Interest paid for leases 2019 (etiqueta del emisor; es el PRINCIPAL de arrendamientos: etiquetas cruzadas, J3)", "(4.312.789)", 59, IPL), J3, indice=0)
for k in ("intereses_financiacion", "arrendamientos_principal"):
    nuevos[2020]["partidas"][k]["nota"] = "(jumbo_e) J3 aplicado también a la columna 2019 de AR2020 p. 59 (nota p. 86). " + str(nuevos[2020]["partidas"][k].get("nota"))
# adquisiciones 2019 y 2021: «-» impreso en la columna del grupo
SCC20 = "Share Capital Change of Subsidiaries                                     5.10                      -                      -                      -"
SCC22 = "Share Capital Change of Subsidiaries                     5.10                         -                        -                 20.336.687                            -"
cambia(2020, "adquisiciones", "anterior", docs[2020]["partidas"]["adquisiciones"].get("anterior"),
       [e("Share Capital Change of Subsidiaries 2019 (grupo, impreso -)", "-", 59, SCC20)],
       "2019 (año natural): la única línea de sociedades dependientes del bloque de inversión del grupo imprime «-»; antes se tomaba el cero del informe de transición (jul–dic 2019) con una cita que no lo prueba")
cambia(2022, "adquisiciones", "anterior", docs[2022]["partidas"]["adquisiciones"].get("anterior"),
       [e("Share Capital Change of Subsidiaries 2021 (grupo, impreso -)", "-", 68, SCC22)],
       "2021: «-» impreso en la columna del grupo de 2021 (los 20.336.687 son de la sociedad matriz en 2022); antes, cero con cita sin relación")
# intereses en financiación 2016–2018: los intereses pagados están en explotación
for a, pg, lin in ((2016, 46, "Interest payable                                 (5.126.891)             (6.205.596)       (4.983.291)     (6.067.344)"),
                   (2017, 47, "Interest payable                                 (5.056.742)             (5.126.891)      (4.882.107)       (4.983.291)"),
                   (2018, 48, "Interest payable                                    (7.149.747)            (5.056.742)       (6.300.851)     (4.882.107)")):
    cz = docs[a]["partidas"]["intereses_financiacion"]["cero"]
    cambia(a, "intereses_financiacion", "cero", cz, {"motivo": "Intereses pagados en el bloque de EXPLOTACIÓN del estado de flujos (línea «Interest payable»); el bloque de financiación no tiene línea de intereses (anterior a la NIIF 16): 0 en financiación",
                                                      "pagina": pg, "cita": " ".join(lin.split())}, "cita anterior («Interest payable», solo la etiqueta) sustituida por la línea completa del bloque de explotación")
cz = docs[2016]["partidas"]["arrendamientos_principal"]["cero"]
cambia(2016, "arrendamientos_principal", "cero", cz, {"motivo": "Antes de la NIIF 16 (aplicada desde el 1-jul-2019): los compromisos son arrendamientos operativos, sin pasivo ni pagos de principal de arrendamientos en financiación",
                                                       "pagina": 93, "cita": "Commitments mostly pertain to operating leases of stores, warehouses and transportation equipment"},
       "cita anterior («Cash flows from financing activities», un encabezado) no probaba el cero")
cz = docs[2018]["partidas"]["arrendamientos"]["cero"]
cambia(2018, "arrendamientos", "cero", cz, {"motivo": "Ejercicio 2018/19, anterior a la aplicación de la NIIF 16 por el grupo (primer ejercicio desde el 1-jul-2019): sin pasivo por arrendamientos en el balance",
                                             "pagina": 52, "cita": "The Group will implement IFRS 16 from its mandatory effective date"},
       "frase de aplicación de la NIIF 16 en lugar de un fragmento («will recognize … rights-of-us assets and lease»)")
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
import fase1_historia as FH  # noqa: E402
tmp = C.rstrip("/") + ".comprobacion_tmp"
os.makedirs(os.path.join(tmp, "fase1_partes"))
os.symlink(os.path.abspath(os.path.join(C, "texto")), os.path.join(tmp, "texto"))
for a, dd in nuevos.items():
    json.dump(dd, open(os.path.join(tmp, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
err = {a: FH.comprobar_anio(tmp, a) for a in nuevos}
shutil.rmtree(tmp)
if any(err.values()):
    sys.exit("DETENIDO (nada escrito): " + json.dumps({a: x for a, x in err.items() if x}, ensure_ascii=False))
O = os.path.join(ANT, "fase1_partes_antes_de_r2")
os.makedirs(O)
reg = {"fecha": "2026-11-18", "autor": "orquestación (Claude, agente de implementación), encargo del coordinador; sin firma humana", "guion": os.path.abspath(__file__),
       "fuente_de_las_correcciones": "revisión independiente del registro de Jumbo (munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/jumbo/revision_registro/, @ 57e417a), comprobada en texto/",
       "archivos": [], "cambios": cambios}
for a, dd in nuevos.items():
    src = os.path.join(P, f"AR_{a}.json")
    shutil.copy2(src, os.path.join(O, f"AR_{a}.json"))
    json.dump(dd, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    reg["archivos"].append({"archivo": f"fase1_partes/AR_{a}.json", "antes": f"antecedentes/fase1_partes_antes_de_r2/AR_{a}.json", "antes_sha256": h(os.path.join(O, f"AR_{a}.json")), "despues_sha256": h(src)})
json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(reg['archivos'])} archivos, {len(cambios)} cambios; comprobar_anio sin errores")
