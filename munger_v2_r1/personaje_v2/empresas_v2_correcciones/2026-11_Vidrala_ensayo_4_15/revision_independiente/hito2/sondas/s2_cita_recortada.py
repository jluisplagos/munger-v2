#!/usr/bin/env python3
"""s2 · R415-SIGNO: ¿se acredita una cifra con el signo contrario al publicado si la CITA se recorta para dejar fuera la marca del signo?
El signo se lee dentro del pasaje de la página que corresponde a la cita (_pasaje_en_pagina), no en lo que rodea al pasaje en la página.
A) nivel de unidad (_cita_cifra con la página); B) registro sintético completo y positivo (mismo arnés que la batería), contraejemplo de la
revisión externa con la cita recortada; C) calcular_entrada con los componentes reales de C48 de Elis (hito 1) y la cita recortada."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx5 as X
VE = X.VE

print("== A · unidad: _cita_cifra(cita, vf, pagina)")
pag = "Estado de flujos\nPagos por arrendamientos (150,8) (130,8)\nResultado del ejercicio -849697.000\nOtros − 12,5\n"
for cita, vf in [("150,8", 150.8), ("150,8)", 150.8), ("130,8", 130.8), ("849697.000", 849697), ("12,5", 12.5),
                 ("Pagos por arrendamientos (150,8)", 150.8), ("Pagos por arrendamientos (150,8)", -150.8),
                 ("Resultado del ejercicio -849697.000", 849697), ("ejercicio -849697.000", 849697),
                 ("697.000", 697), ("9697.000", 9697)]:
    en_pagina = VE._norm_txt(cita) in VE._norm_txt(pag)
    res = VE._cita_cifra(cita, vf, pag) if hasattr(VE, "_cita_cifra") else ("(código del hito 1) _cita_contiene", VE._cita_contiene(cita, vf))
    print(f"   cita={cita!r:45} vf={vf!r:10} cita en la página: {en_pagina} -> {res}")

print("\n== B · registro sintético completo: Historia!F6 (valor_fuente positivo, signo 1, tratamiento «ninguno»)")
K = X.K
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
r0 = X.con()
print("   control positivo:", X.resumen(r0, K))


def caso(nombre, texto_pagina, cita, vf=VF, signo=1):
    pg = X.nueva_pagina(texto_pagina)
    r = X.con(lambda g: X.ent(g, K)["fuente"].update(pagina=pg, cita=cita, valor_fuente=vf, signo=signo), resellar=True)
    print(f"   {nombre}\n      página={texto_pagina!r}\n      cita={cita!r} valor_fuente={vf!r} signo={signo}\n      -> {X.resumen(r, K)}")
    return r


caso("B0 contraejemplo literal de la revisión externa (cita completa)", f"Partida sintética de {K}: -{VF:.3f}", f"Partida sintética de {K}: -{VF:.3f}")
caso("B1 la misma página; la cita empieza en la cifra", f"Partida sintética de {K}: -{VF:.3f}", f"{VF:.3f}")
caso("B2 página con paréntesis contables; la cita es solo la cifra", f"Partida sintética de {K}: ({VF:,.3f})", f"{VF:,.3f}")
caso("B3 página con paréntesis; la cita acaba en la cifra y empieza tras el paréntesis", f"Partida sintética de {K}: ({VF:,.3f}) (1.000)", f"{VF:,.3f}) (1.000)")
caso("B4 menos Unicode; la cita empieza en la cifra", f"Partida sintética de {K}: −{VF:.3f}", f"{VF:.3f}")
caso("B5 sentido inverso: la página publica en positivo «x-y: 849697.000»; cita recortada «-849697.000» no existe (control)", f"Partida sintética de {K}: {VF:.3f}", f"{VF:.3f}", vf=-VF, signo=-1)
caso("B6 cifra a mitad de otra: la página publica 1849697.000 y la cita es «849697.000»", f"Partida sintética de {K}: 1{VF:.3f}", f"{VF:.3f}")

print("\n== C · calcular_entrada, C48 de Elis: cálculo del HITO 1 (magnitudes positivas, sin declarar la conversión)")
import json, copy, re
import fase1_historia as FH
PV = X.PV
E415 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15")
CALC_H1 = json.load(open(os.path.join(E415, "reproduccion", "codigo_4_15_hito1", "cambio_elis_c48_4_15.json.txt"), encoding="utf-8"))["analisis"]["C48"]["calculo"]
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")  # el mismo expediente que usa la batería
CALC_H2 = json.load(open(os.path.join(E415, "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))["analisis"]["C48"]["calculo"]
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]


def probar(nombre, calc, carpeta=ELIS):
    try:
        r = FH.calcular_entrada("C48", {"calculo": calc}, H, anios, carpeta)
        print(f"   {nombre}\n      -> ACEPTADO valor={r['valor']!r}\n      fuente: {r['fuente'][:330]}")
    except (ValueError, TypeError) as ex:
        print(f"   {nombre}\n      -> ERROR {type(ex).__name__}: {str(ex)[:300]}")


cmps_h1 = CALC_H1["componentes"]["pagos_arrendamientos_con_intereses"]
print("   citas del hito 1:", {a: (c["valor"], c["cita"]) for a, c in cmps_h1.items()})
probar("C1 cálculo del hito 1 tal cual (130,8 frente a «(130,8)», sin declarar la conversión)", CALC_H1)
rec = copy.deepcopy(CALC_H1)
for a, c in rec["componentes"]["pagos_arrendamientos_con_intereses"].items():
    m = re.search(r"\(?(\d+[.,]\d)\)?", c["cita"])
    # la cifra del componente tal como está impresa, sin los paréntesis
    c["cita"] = next(x for x in re.findall(r"\d+[.,]\d", c["cita"]) if abs(float(x.replace(",", ".")) - c["valor"]) < 1e-9)
print("   citas recortadas:", {a: (c["valor"], c["cita"]) for a, c in rec["componentes"]["pagos_arrendamientos_con_intereses"].items()})
probar("C2 el MISMO cálculo del hito 1 con cada cita recortada a la cifra (sin los paréntesis), sin valor_fuente/signo/tratamiento", rec)
rec2 = copy.deepcopy(CALC_H1)
for a, c in rec2["componentes"]["pagos_arrendamientos_con_intereses"].items():
    c["cita"] = re.sub(r"^.*?(\d+[.,]\d\)(?: \(\d+[.,]\d\))?)$", r"\1", c["cita"]) if a != "2023" else re.sub(r"^.*\((\d+,\d\))$", r"\1", c["cita"])
print("   citas recortadas tras el paréntesis de apertura:", {a: (c["valor"], c["cita"]) for a, c in rec2["componentes"]["pagos_arrendamientos_con_intereses"].items()})
probar("C3 lo mismo con la cita empezando justo después de «(»", rec2)
probar("C4 control: el cálculo del hito 2 (valor_fuente negativo, signo −1, tratamiento)", CALC_H2)
probar("C5 sin carpeta: el cálculo del hito 1 (no hay contraste con la fuente)", CALC_H1, carpeta=None)
X.limpiar()
