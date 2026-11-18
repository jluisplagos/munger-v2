#!/usr/bin/env python3
"""zoetis_t1c · corrección registrada de fase1_partes (filas 22, 23 y 17 de la Historia), tras cambiar_base.py preparar.

Por qué: con US GAAP la fila 23 («arrendamientos») tiene que llevar SOLO el pasivo por arrendamientos FINANCIEROS: el pasivo operativo no es deuda del
puente (su pago va entero en el EBIT) y el producto lo indica como salida de F1-US-PUENTE («que la fila 23 lleve solo el pasivo por arrendamientos
financieros (corrección registrada de las entradas en un expediente nuevo)», motor_a_f1.py; revisión R2 de f1/usgaap §8). Para no contar dos veces
el pasivo financiero, la fila 22 («deuda») deja de llevarlo (la fase 1 lo había puesto en deuda en 2023–2025, «criterio dudoso» según su propia nota).
La fila 17 de 2025 recoge el principal financiero publicado (2), que la fase 1 dejó vacío (F1-K3a). Cada valor nuevo lleva su línea literal y su página
del texto del expediente; los ceros de 2019–2021 llevan una cita literal (quedan PENDIENTES de verificación, H1, como todo cero con cita).
Uso: python3 -I corregir_fase1_partes.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json
Nunca sobrescribe un original guardado; cada edición comprueba antes el valor que espera encontrar (si no, se detiene sin escribir nada)."""
import copy, hashlib, json, os, shutil, sys

C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
P = os.path.join(C, "fase1_partes")
ORIG = os.path.join(ANT, "fase1_partes_original")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
docs = {a: json.load(open(os.path.join(P, f"AR_{a}.json"), encoding="utf-8")) for a in range(2019, 2026)}
nuevos = copy.deepcopy(docs)
cambios = []

FIN_C_25 = "Finance lease liabilities - current (in Other current liabilities)                                                                                             1                                  1"
FIN_N_25 = "Finance lease liabilities - noncurrent (in Other noncurrent liabilities)                                                                                       6                                  7"
PRIN_25 = "Financing cash flows – finance leases                                                                                           2                                 1                                 —"
FIN_C_24 = "Finance lease liabilities - current (in Other current liabilities) 1 1"
FIN_N_24 = "Finance lease liabilities - noncurrent (in Other noncurrent liabilities) 7 8"
FIN_C_23 = "Finance lease liabilities - current (in Other current liabilities)                                                                                              1                          —"
FIN_N_23 = "Finance lease liabilities - noncurrent (in Other noncurrent liabilities)                                                                                        8                           —"
CITA_SOLO_OP = "Our current portfolio includes only operating leases which are recorded as a right of use"
PAG_SOLO_OP = {2019: 77, 2020: 80, 2021: 78, 2022: 70}


def e(concepto, impreso, pagina, linea):
    return {"concepto": concepto, "impreso": impreso, "pagina": pagina, "linea": linea}


def cambia(a, partida, campo, esperado, nuevo, motivo):
    actual = nuevos[a]["partidas"][partida].get(campo)
    if actual != esperado:
        sys.exit(f"DETENIDO (nada escrito): AR_{a} · {partida} · {campo}: se esperaba {json.dumps(esperado, ensure_ascii=False)[:200]} y hay "
                 f"{json.dumps(actual, ensure_ascii=False)[:200]}")
    nuevos[a]["partidas"][partida][campo] = nuevo
    cambios.append({"archivo": f"fase1_partes/AR_{a}.json", "partida": partida, "campo": campo, "antes": esperado, "despues": nuevo, "motivo": motivo})


def sin_fin(lista):
    return [x for x in lista if not str(x.get("concepto", "")).startswith("Finance lease liabilities")]


M23 = "fila 23 solo con el pasivo por arrendamientos financieros (US GAAP; F1-US-PUENTE)"
M22 = "fila 22 sin el pasivo por arrendamientos financieros, que pasa a la fila 23 (no se cuenta dos veces)"
# ---- 2025 (10-K FY2025, PDF p. 89)
d = docs[2025]["partidas"]
cambia(2025, "arrendamientos", "actual", d["arrendamientos"]["actual"],
       [e("Finance lease liabilities - current (in Other current liabilities)", "1", 89, FIN_C_25),
        e("Finance lease liabilities - noncurrent (in Other noncurrent liabilities)", "6", 89, FIN_N_25)], M23)
cambia(2025, "arrendamientos", "anterior", d["arrendamientos"]["anterior"],
       [e("Finance lease liabilities - current (in Other current liabilities) 2024", "1", 89, FIN_C_25),
        e("Finance lease liabilities - noncurrent (in Other noncurrent liabilities) 2024", "7", 89, FIN_N_25)], M23)
cambia(2025, "deuda", "actual", d["deuda"]["actual"], sin_fin(d["deuda"]["actual"]), M22)
cambia(2025, "deuda", "anterior", d["deuda"]["anterior"], sin_fin(d["deuda"]["anterior"]), M22)
cambia(2025, "arrendamientos_principal", "actual", None, [e("Financing cash flows – finance leases", "2", 89, PRIN_25)],
       "fila 17 de 2025 = principal de arrendamientos financieros publicado (la fase 1 la dejó vacía; F1-K3a)")
cambia(2025, "arrendamientos_principal", "anterior", None, [e("Financing cash flows – finance leases 2024", "1", 89, PRIN_25)],
       "fila 17 de 2024 con el comparativo del 10-K 2025 (igual que el 10-K 2024: 1)")
# ---- 2024 (10-K FY2024 por OCR, PDF p. 86)
d = docs[2024]["partidas"]
cambia(2024, "arrendamientos", "actual", d["arrendamientos"]["actual"],
       [e("Finance lease liabilities - current (in Other current liabilities)", "1", 86, FIN_C_24),
        e("Finance lease liabilities - noncurrent (in Other noncurrent liabilities)", "7", 86, FIN_N_24)], M23)
cambia(2024, "arrendamientos", "anterior", d["arrendamientos"]["anterior"],
       [e("Finance lease liabilities - current 2023", "1", 86, FIN_C_24), e("Finance lease liabilities - noncurrent 2023", "8", 86, FIN_N_24)], M23)
cambia(2024, "deuda", "actual", d["deuda"]["actual"], sin_fin(d["deuda"]["actual"]), M22)
cambia(2024, "deuda", "anterior", d["deuda"]["anterior"], sin_fin(d["deuda"]["anterior"]), M22)
# ---- 2023 (10-K FY2023 por OCR, PDF p. 87): 2023 financieros 1 + 8; 2022 «—» (no había)
d = docs[2023]["partidas"]
cambia(2023, "arrendamientos", "actual", d["arrendamientos"]["actual"],
       [e("Finance lease liabilities - current (in Other current liabilities)", "1", 87, FIN_C_23),
        e("Finance lease liabilities - noncurrent (in Other noncurrent liabilities)", "8", 87, FIN_N_23)], M23)
cambia(2023, "arrendamientos", "anterior", d["arrendamientos"]["anterior"],
       [e("Finance lease liabilities - current 2022 (impreso —)", "—", 87, FIN_C_23),
        e("Finance lease liabilities - noncurrent 2022 (impreso —)", "—", 87, FIN_N_23)], M23 + "; 2022: «—» impreso (sin arrendamientos financieros)")
# ---- 2019–2022: solo arrendamientos operativos → fila 23 = 0 (cero con cita literal; el comparativo del informe siguiente se vacía)
for a in (2019, 2020, 2021, 2022):
    d = docs[a]["partidas"]
    cambia(a, "arrendamientos", "actual", d["arrendamientos"]["actual"], [], M23 + f"; {a}: solo arrendamientos operativos")
    cambia(a, "arrendamientos", "cero", d["arrendamientos"]["cero"],
           {"motivo": f"US GAAP: en {a} Zoetis solo tenía arrendamientos operativos; su pasivo no va en la fila 23 (que lleva solo los financieros): sin pasivo por arrendamientos financieros",
            "pagina": PAG_SOLO_OP[a], "cita": CITA_SOLO_OP}, M23 + f"; {a}: cero con cita (pendiente de verificación, H1)")
    if a in (2020, 2021, 2022):
        cambia(a, "arrendamientos", "anterior", d["arrendamientos"]["anterior"], [], M23 + f"; comparativo de {a - 1}: solo operativos (se toma el cero del informe {a - 1})")
for a in range(2019, 2026):
    if any(c["archivo"].endswith(f"AR_{a}.json") for c in cambios):
        nota_ant = nuevos[a]["partidas"]["arrendamientos"].get("nota")
        nuevos[a]["partidas"]["arrendamientos"]["nota"] = ("(zoetis_t1c, corrección registrada) Fila 23 solo con el pasivo por arrendamientos FINANCIEROS (US GAAP): "
            "el pasivo operativo no va en ella (F1-US-PUENTE). Nota anterior: " + str(nota_ant))
# las notas de los lectores que ya no describen la partida corregida se conservan detrás de un prefijo que dice qué cambió
for a, partida, txt in ((2025, "deuda", "sin el pasivo por arrendamientos financieros (pasa a la fila 23)"), (2024, "deuda", "sin el pasivo por arrendamientos financieros (pasa a la fila 23)"),
                        (2025, "arrendamientos_principal", "2025 = 2 y 2024 = 1, principal de arrendamientos financieros publicado (Financing cash flows – finance leases, PDF p. 89)")):
    nuevos[a]["partidas"][partida]["nota"] = f"(zoetis_t1c, corrección registrada) {txt}. Nota anterior del lector: " + str(nuevos[a]["partidas"][partida].get("nota"))
# comprobación con las reglas de la fase 1 antes de escribir
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
import fase1_historia as FH  # noqa: E402
tmp = C.rstrip("/") + ".comprobacion_tmp"
if os.path.exists(tmp):
    sys.exit(f"existe {tmp}")
os.makedirs(os.path.join(tmp, "fase1_partes"))
os.symlink(os.path.abspath(os.path.join(C, "texto")), os.path.join(tmp, "texto"))
for a, dd in nuevos.items():
    json.dump(dd, open(os.path.join(tmp, "fase1_partes", f"AR_{a}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
errores = {a: FH.comprobar_anio(tmp, a) for a in nuevos}
shutil.rmtree(tmp)
if any(errores.values()):
    sys.exit("DETENIDO (nada escrito): las correcciones no pasan comprobar_anio: " + json.dumps({a: x for a, x in errores.items() if x}, ensure_ascii=False))
os.makedirs(ORIG, exist_ok=True)
reg = {"fecha": "2026-11-18", "autor": "orquestación (Claude, agente de implementación), encargo del coordinador; sin firma humana", "guion": os.path.abspath(__file__),
       "archivos": [], "cambios": cambios}
for a, dd in nuevos.items():
    if dd == docs[a]:
        continue
    src = os.path.join(P, f"AR_{a}.json")
    o = os.path.join(ORIG, f"AR_{a}.json")
    if os.path.exists(o):
        sys.exit(f"ya existe el original guardado {o}: no se sobrescribe")
    shutil.copy2(src, o)
    json.dump(dd, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    reg["archivos"].append({"archivo": f"fase1_partes/AR_{a}.json", "original": os.path.relpath(o, os.path.dirname(ANT)), "original_sha256": h(o), "nuevo_sha256": h(src)})
json.dump(reg, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(reg['archivos'])} archivos corregidos, {len(cambios)} cambios; comprobar_anio sin errores")
