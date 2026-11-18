#!/usr/bin/env python3
"""jumbo_e · ronda 3 de fase1_partes (revisión independiente de la orquestación, auxiliar @ 9740e27, REVISION_ORQUESTACION.md):
 1) adquisiciones 2019 y 2021: la ronda 2 las había pasado a cifra impresa «-» (salían de los ceros pendientes) con la línea «Share Capital Change of
    Subsidiaries», que recoge aportaciones a filiales y no compras de negocios; 2020 tiene la misma línea y sigue como cero pendiente. Vuelven a cero
    PENDIENTE (H1) del informe propio, con esa línea como cita (mismo trato que 2020): se retiran los comparativos «-» de AR_2020 y AR_2022. 2021: AR2021
    PDF p. 63. 2019: el cero solo puede citar el informe propio (comprobar_anio), que es el de transición (jul–dic 2019, p. 57); la columna del año natural
    2019 de AR2020 p. 59 imprime también «-» y queda en el motivo. No se confirman (no hay decisión humana).
 2) principal de arrendamientos 2016 y pasivo por arrendamientos 2018: la prueba es el bloque de financiación del propio estado de flujos, sin línea de
    arrendamientos (NIC 17), AR2016-17 PDF p. 46 y AR2018-19 PDF p. 48. `no_aplicable` no existe en el esquema de fase1_partes (solo actual, anterior y
    cero): se queda cero PENDIENTE con esa cita.
Uso: python3 -I corregir_fase1_partes_r3.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import copy, hashlib, json, os, shutil, sys
C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
P = os.path.join(C, "fase1_partes")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
anios = (2016, 2018, 2019, 2020, 2021, 2022)
docs = {a: json.load(open(os.path.join(P, f"AR_{a}.json"), encoding="utf-8")) for a in anios}
n = copy.deepcopy(docs)
cambios = []


def cambia(a, partida, campo, nuevo, motivo):
    antes = n[a]["partidas"][partida].get(campo)
    n[a]["partidas"][partida][campo] = nuevo
    cambios.append({"archivo": f"fase1_partes/AR_{a}.json", "partida": partida, "campo": campo, "antes": antes, "despues": nuevo, "motivo": motivo})


assert docs[2020]["partidas"]["adquisiciones"]["anterior"][0]["impreso"] == "-" and docs[2022]["partidas"]["adquisiciones"]["anterior"][0]["impreso"] == "-"
cambia(2020, "adquisiciones", "anterior", [], "se retira el «-» de la ronda 2: 2019 vuelve a cero pendiente (revisión de la orquestación)")
cambia(2022, "adquisiciones", "anterior", [], "se retira el «-» de la ronda 2: 2021 vuelve a cero pendiente (revisión de la orquestación)")
cambia(2021, "adquisiciones", "cero", {"motivo": "El bloque de inversión del grupo no tiene ninguna línea de compra ni venta de negocios; la única línea de sociedades dependientes, «Share Capital Change of Subsidiaries», imprime «-» en la columna del grupo de 2021 (y del grupo de 2021 en AR2022 p. 68); esa línea recoge aportaciones a filiales, no compras: cero PENDIENTE de verificación, como 2020",
                                      "pagina": 63, "cita": "Share Capital Change of Subsidiaries"}, "cita: la línea de sociedades dependientes del bloque de inversión (antes «Net cash flows from investing activities»)")
cambia(2019, "adquisiciones", "cero", {"motivo": "El bloque de inversión del grupo no tiene ninguna línea de compra ni venta de negocios; «Share Capital Change of Subsidiaries» imprime «-» en la columna del grupo (informe de transición, jul–dic 2019, p. 57; la columna del año natural 2019 de AR2020 PDF p. 59 imprime también «-», pero el cero solo puede citar el informe propio); esa línea recoge aportaciones a filiales, no compras: cero PENDIENTE de verificación, como 2020",
                                      "pagina": 57, "cita": "Share Capital Change of"}, "cita: la línea de sociedades dependientes del bloque de inversión (antes «Net cash flows from investing activities»)")
cambia(2016, "arrendamientos_principal", "cero", {"motivo": "NIC 17: el bloque de financiación del estado de flujos (dividendos, devolución de capital, dividendo a cuenta, préstamos obtenidos y devueltos) no tiene ninguna línea de pagos de arrendamientos; los compromisos son sobre todo arrendamientos operativos (p. 93): cero PENDIENTE de verificación",
                                                   "pagina": 46, "cita": "Cash flows from financing activities"}, "cita: el bloque de financiación sin línea de arrendamientos (revisión: «mostly» no excluye arrendamientos financieros NIC 17)")
cambia(2018, "arrendamientos", "cero", {"motivo": "Ejercicio 2018/19, anterior a la aplicación de la NIIF 16 por el grupo (1-jul-2019): el bloque de financiación del estado de flujos (dividendos, préstamos, costes del bono, devoluciones) no tiene ninguna línea de pagos de arrendamientos, así que no hay pasivo por arrendamientos financieros NIC 17 que pagar: cero PENDIENTE de verificación",
                                         "pagina": 48, "cita": "Cash flows from financing activities"}, "cita: el bloque de financiación sin línea de arrendamientos (revisión: la frase de la NIIF 16 no prueba la falta de pasivo)")
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
import fase1_historia as FH  # noqa: E402
tmp = C.rstrip("/") + ".comprobacion_tmp"
os.makedirs(os.path.join(tmp, "fase1_partes"))
os.symlink(os.path.abspath(os.path.join(C, "texto")), os.path.join(tmp, "texto"))
for a, dd in n.items():
    json.dump(dd, open(os.path.join(tmp, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
err = {a: FH.comprobar_anio(tmp, a) for a in n}
shutil.rmtree(tmp)
if any(err.values()):
    sys.exit("DETENIDO (nada escrito): " + json.dumps({a: x for a, x in err.items() if x}, ensure_ascii=False))
O = os.path.join(ANT, "fase1_partes_antes_de_r3")
os.makedirs(O)
R = {"fecha": "2026-11-18", "guion": os.path.abspath(__file__), "fuente": "REVISION_ORQUESTACION.md (auxiliar @ 9740e27)", "archivos": [], "cambios": cambios}
for a, dd in n.items():
    src = os.path.join(P, f"AR_{a}.json")
    shutil.copy2(src, os.path.join(O, f"AR_{a}.json"))
    json.dump(dd, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    R["archivos"].append({"archivo": f"fase1_partes/AR_{a}.json", "antes_sha256": h(os.path.join(O, f"AR_{a}.json")), "despues_sha256": h(src)})
json.dump(R, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(cambios)} cambios")
