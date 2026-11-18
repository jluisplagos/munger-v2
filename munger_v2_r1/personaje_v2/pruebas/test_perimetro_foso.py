#!/usr/bin/env python3
"""Batería del perímetro F1 en las fases, G7 y las guardas V-F1g/V-F1k por valores (decisión P-FOSO, opción a, 18-nov-2026; dictamen
examen/revisiones/dictamen_perimetro_g4/DICTAMEN.md, defectos D1, D2 y D3).

Uso (desde personaje_v2/): python3 -B pruebas/test_perimetro_foso.py
Sin LibreOffice y sin binarios: usa el volcado y la declaración F1 del expediente de Ahold (examen, ahold_f2, solo lectura: nada se escribe
en él) y libros sintéticos de valores. Los intereses de arrendamiento de Ahold (no están en su declaración vigente) se declaran aquí, en una
COPIA en memoria, con sus páginas: AR2022 PDF p. 251 (2021 y 2022), AR2023 p. 262, AR2024 p. 321 y AR2025 p. 272, «Interest accretion to
lease liability»; la comprobación de su fuente lee los textos del expediente.
Grupos: PF (cálculo y regla), VOL (volcado datos_v63.md/.json), RM (referencias mecánicas), GRAM (G7 y G4), F1 (V-F1g/V-F1k por valores) y
SIN (sin perímetro declarado nada cambia).
"""
import copy
import json
import os
import shutil
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import config_v2  # noqa: E402
import perimetro_f1 as PF  # noqa: E402
import referencias_mecanicas as RM  # noqa: E402
import volcar_datos_v63 as VOL  # noqa: E402
import comprobar_gramatica as GR  # noqa: E402
import motor_a_f1 as M  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def cerca(a, b, tol=5e-5):
    return a is not None and b is not None and abs(a - b) <= tol


EXP = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "ahold_f2", "Ahold")
CFG = config_v2.cargar(os.path.join(PV, "config_v2.json"))
T0 = json.load(open(os.path.join(EXP, "datos_v63.json"), encoding="utf-8"))
D0 = json.load(open(os.path.join(EXP, "motor_a_f1.json"), encoding="utf-8"))
INT = {2021: ("AR2022", 251, "(337)"), 2022: ("AR2022", 251, "(356)"), 2023: ("AR2023", 262, "(382)"), 2024: ("AR2024", 321, "(422)"),
       2025: ("AR2025", 272, "(465)")}


def con_intereses(d, cambia=None):
    d = copy.deepcopy(d)
    d["series"][PF.SERIE_INTERESES] = {str(y): {"valor_fuente": -int(lit.strip("()")), "signo": -1, "tratamiento": "publicado entre paréntesis; magnitud positiva",
                                                "documento": doc, "archivo": d["fuentes_series"][doc]["archivo"], "pagina": p, "literal": lit,
                                                "fila": "Interest accretion to lease liability", "columna": str(y)} for y, (doc, p, lit) in INT.items()}
    for y, campos in (cambia or {}).items():
        d["series"][PF.SERIE_INTERESES][str(y)].update(campos)
    return d


D1 = con_intereses(D0)

# =========================================================================================== PF · cálculo con las cifras de Ahold
paso("PF · sin declaración, con A0_total o con A3_estimado no hay bloque (None)",
     PF.desde_datos(T0, None) is None and PF.desde_datos(T0, {}) is None
     and all(PF.desde_datos(T0, {**D0, "perimetro_reinversion": {"valor": v}}) is None for v in ("A0_total", "A3_estimado", None)))
pf0 = PF.desde_datos(T0, D0, EXP)
paso("PF · Ahold declara A2_propio: bloque con el perímetro, las palancas y el ROIC terminal declarados",
     pf0 is not None and pf0["perimetro"] == "A2_propio" and pf0["perimetro_palancas_s2c"] == "A2_propio" and pf0["anios"] == [2021, 2022, 2023, 2024, 2025])
paso("PF · ROIC de todo el capital 2021–2025 = Historia!C55 (8,78 %) exactamente",
     cerca(pf0["roic_todo_el_capital_medio"], T0["historia"]["anclas"]["roic_medio_5"], 1e-12) and cerca(pf0["roic_todo_el_capital_medio"], 0.087815),
     f"{pf0['roic_todo_el_capital_medio']:.6f}")
paso("PF · ROIC sin arrendamientos (NOPAT NIIF 16 ÷ capital propio) 2021–2025 = 14,82 % (dictamen: 14,8 %; ancla de G7 2 × = 29,64 %)",
     cerca(pf0["roic_sin_arrendamientos_medio"], 0.148181), f"{pf0['roic_sin_arrendamientos_medio']:.6f}")
paso("PF · sin la serie de intereses de arrendamiento: ROIC propio pagado el alquiler no calculable y no utilizable; se dice qué falta",
     pf0["roic_propio_pagado_el_alquiler_medio"] is None and not pf0["roic_propio_utilizable"]
     and "sin declarar" in " ".join(pf0["intereses_arrendamiento"]["comprobacion_fuentes"]["incompletas"]))
pf1 = PF.desde_datos(T0, D1, EXP)
paso("PF · con los intereses publicados: ROIC del capital propio pagado todo el alquiler 2021–2025 = 13,03 % (dictamen 13,0 %)",
     cerca(pf1["roic_propio_pagado_el_alquiler_medio"], 0.130280), f"{pf1['roic_propio_pagado_el_alquiler_medio']:.6f}")
pa = {int(k): v["roic_propio_pagado_el_alquiler"] for k, v in pf1["por_anio"].items()}
paso("PF · por año 14,22 / 14,75 / 11,48 / 10,67 / 14,03 % (el peor, 2024: 10,7 %), con sus celdas",
     all(cerca(pa[y], x, 6e-5) for y, x in ((2021, 0.1422), (2022, 0.1475), (2023, 0.1148), (2024, 0.1067), (2025, 0.1403)))
     and pf1["por_anio"]["2025"]["celdas"] == "Historia!L7, L10, L32, L23", str({y: round(v, 4) for y, v in pa.items()}))
paso("PF · fuente de los intereses comprobada (cifra en la página del documento con su huella; columna del ejercicio en los 5 años) → utilizable",
     pf1["roic_propio_utilizable"] and pf1["intereses_arrendamiento"]["comprobacion_fuentes"]["columna_comprobada"] == 5)
pfx = PF.desde_datos(T0, con_intereses(D0, {2025: {"valor_fuente": -466, "literal": "(466)"}}), EXP)
paso("PF · un literal que no está en la página (466 en lugar de 465) → NO comprobada, no utilizable, y el problema nombra la serie",
     not pfx["roic_propio_utilizable"] and any("intereses_arrendamiento.2025" in x for x in pfx["intereses_arrendamiento"]["comprobacion_fuentes"]["invalidas"]))
paso("PF · ROIC terminal neutro r·N/(N − f) con el margen de partida y la f de A2 = 9,04 % (dictamen: 9,04 % en el NORMAL)",
     cerca(pf1["roic_neutro_con_m0"], 0.0904, 1e-4) and cerca(PF.neutro(0.09, 0.04, T0["historia"]["anclas"]["tipo_impositivo_5"], T0["historia"]["anclas"]["f"]), 0.090402, 2e-6))
paso("PF · la regla es la de la decisión (foso con el capital propio pagado el alquiler frente a r; C55 solo frente al sector; G4 r + 0,03)",
     all(s in pf1["regla"] for s in ("(EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos)", "con r (Análisis!C56)",
                                     "Historia!C55 (ROIC de todo el capital) solo frente al sector", "G4 sigue con r + 0,03")))

# =========================================================================================== VOL · volcado para las fases (D2)
H = {"existe": False}
T1 = copy.deepcopy(T0)
T1["perimetro_f1"] = pf1
md1 = VOL.seccion_md(T1, H)
md0 = VOL.seccion_md(copy.deepcopy(T0), H)
paso("VOL · datos_v63.md con F1 en A2: sección «1 bis» con el perímetro declarado, la regla y la fórmula",
     "## 1 bis. Perímetro F1 declarado y vara del foso" in md1 and "Perímetro de la reinversión (motor_a_f1.json): **A2_propio**" in md1
     and pf1["regla"] in md1 and "(EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos)" in md1)
paso("VOL · cifras por año y medias: 13.03 % frente a r 9.00 % (+4.03 puntos), 14.82 % y ancla de G7 29.64 % (no 2 × C55 = 17.56 %), C55 8.78 % solo frente al sector",
     all(s in md1 for s in ("ROIC del capital propio pagado todo el alquiler: 13.03 %", "+4.03 puntos", "14.82 %", "29.64 %", "17.56 %", "| 2024 | 2784 |",
                            "Historia!K7, K10, K32, K23", "AR2024 p. 321")))
paso("VOL · C54 y C55 rotulados «todo el capital» en las anclas, y ROIC terminal neutro 9.04 %",
     "roic_medio_5 (todo el capital" in md1 and "s2c_medio (todo el capital" in md1 and "9.04 %" in md1 and "r no se traduce a otro perímetro" in md1)
paso("VOL · sin intereses comprobados la sección lo dice («NO COMPROBADOS») y no da la media como cifra",
     "**NO COMPROBADOS**" in VOL.seccion_md({**copy.deepcopy(T0), "perimetro_f1": pf0}, H) and "no es calculable" in VOL.seccion_md({**copy.deepcopy(T0), "perimetro_f1": pf0}, H))
paso("SIN · sin perímetro F1 el volcado no lleva la sección ni los rótulos nuevos", "1 bis" not in md0 and "todo el capital" not in md0 and "P-FOSO" not in md0)
lineas0, lineas1 = md0.splitlines(), md1.splitlines()
quitadas = [x for x in lineas0 if x not in lineas1]
paso("SIN · con F1 solo se AÑADE la sección y cambian dos rótulos (C54, C55): el resto del volcado es idéntico",
     len(quitadas) == 2 and all(x.startswith("| s2c_medio |") or x.startswith("| roic_medio_5 |") for x in quitadas), str(quitadas)[:200])
# main(): carpeta temporal con el libro ausente → se prueba la lectura de la declaración por la carpeta
tmp = tempfile.mkdtemp(prefix="perimetro_foso_")
try:
    c = os.path.join(tmp, "Ahold")
    os.makedirs(c)
    paso("VOL · leer_declaracion: sin motor_a_f1.json → None (expediente antiguo)", PF.leer_declaracion(c) is None)
    json.dump(D0, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"))
    paso("VOL · leer_declaracion: con motor_a_f1.json → la declaración", (PF.leer_declaracion(c) or {}).get("perimetro_reinversion", {}).get("valor") == "A2_propio")
    res_f1 = json.load(open(os.path.join(EXP, "motor_a_f1_resultado.json"), encoding="utf-8"))
    json.dump(res_f1, open(os.path.join(c, "motor_a_f1_resultado.json"), "w", encoding="utf-8"))
    ac = PF.anclas_capa(c, res_f1["libro_sha256"])
    paso("VOL · cota A1 de la capa F1 (5,10 en Ahold) solo si el resultado es del mismo libro (huella); de otro libro → None",
         ac is not None and cerca(ac["A1_sin_ROU"], 5.10165, 1e-4) and ac["declarado"] is None and PF.anclas_capa(c, "0" * 64) is None)
    pfa = dict(pf0, anclas_capa_f1=ac)
    paso("VOL · con C53 vacía la sección da la cota A1 sobre este libro", "cota A1 de la capa F1 sobre este libro, sin derechos de uso: 5.102"
         in VOL.seccion_md({**copy.deepcopy(T0), "perimetro_f1": pfa}, H))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# =========================================================================================== RM · referencias mecánicas
Ts = copy.deepcopy(T0)
Ts["historia"]["anclas"]["s2c_marginal"] = 5.1   # ancla sintética del perímetro (cota A1 de Ahold, 5,10) para que la referencia del S2C exista
rm0 = RM.calcular(copy.deepcopy(Ts), CFG)
rm1 = RM.calcular({**copy.deepcopy(Ts), "perimetro_f1": pf1}, CFG)
rmn = RM.calcular({**copy.deepcopy(Ts), "perimetro_f1": pf0}, CFG)
paso("RM · S2C BUENO: el tope 2 × ROIC histórico usa el del perímetro (2 × 14,82 %): 6,4 sin recortar; con C55 (17,56 %) se recorta",
     rm1["palancas"]["s2c"]["BUENO"] == 6.4 and rm0["palancas"]["s2c"]["BUENO"] < 6.4
     and rm1["palancas"]["s2c"]["anclas_usadas"].get("roic_perimetro_f1_sin_arrendamientos") is not None,
     f"{rm0['palancas']['s2c']['BUENO']} → {rm1['palancas']['s2c']['BUENO']}")
paso("RM · ROIC terminal BUENO: con P-FOSO (13,03 % comprobado) = mín(13,03 %, r + 0,03) = 0,12; con C55 (8,78 % < r) = r = 0,09",
     rm1["palancas"]["roic_lp"]["BUENO"] == 0.12 and rm0["palancas"]["roic_lp"]["BUENO"] == 0.09
     and rm1["palancas"]["roic_lp"]["MALO"] == rm1["palancas"]["roic_lp"]["NORMAL"] == 0.09,
     f"{rm0['palancas']['roic_lp']['BUENO']} → {rm1['palancas']['roic_lp']['BUENO']}")
paso("RM · sin intereses comprobados: ROIC BUENO como antes (C55) y la nota lo dice; el tope del S2C sí usa el perímetro (filas del libro)",
     rmn["palancas"]["roic_lp"]["BUENO"] == 0.09 and any("P-FOSO" in x and "C55" in x for x in rmn["palancas"]["roic_lp"]["notas"])
     and rmn["palancas"]["s2c"]["BUENO"] == 6.4)
Tb = {**copy.deepcopy(Ts), "perimetro_f1": pf1}
Tb["diagnostico"]["motor"] = "B"
Tb["diagnostico"]["r_operativa"] = 0.07   # tasa del motor B (Diagnóstico V6!C15), sintética
paso("SIN · con el motor B el perímetro F1 no se usa (F1 solo afecta al motor A)", RM.calcular(Tb, CFG)["palancas"]["s2c"] == RM.calcular({**copy.deepcopy(Ts), "diagnostico": Tb["diagnostico"]}, CFG)["palancas"]["s2c"])
paso("SIN · sin perímetro las referencias no cambian (mismas cifras y notas que sin la clave)", rm0 == RM.calcular(copy.deepcopy(Ts), CFG))

# =========================================================================================== GRAM · G7 y G4 (D1)


def gramatica(datos, motor=None):
    tmp = tempfile.mkdtemp(prefix="perimetro_foso_gram_")
    try:
        for n in ("fase_b.json", "fase_a.json", "referencias_mecanicas.json"):
            shutil.copy(os.path.join(EXP, n), os.path.join(tmp, n))
        json.dump(datos, open(os.path.join(tmp, "datos_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
        g = GR.Gramatica(tmp, "antes", False, CFG)
        if motor:
            g.motor = motor
        g.correr()
        return g.h, g.codigo()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


h0, c0 = gramatica(copy.deepcopy(T0))
h1, c1 = gramatica({**copy.deepcopy(T0), "perimetro_f1": pf1})
g7 = lambda h: [x for x in h if x["id"] == "G7"]  # noqa: E731
g4 = lambda h: [x for x in h if x["id"] == "G4"]  # noqa: E731
paso("GRAM · sin perímetro (como hoy): G7 BUENO salta, 0,209 > 2 × C55 = 0,176, con el mismo texto que la gramática del expediente",
     [x["escenario"] for x in g7(h0)] == ["BUENO"] and "= 0.209 > 2 × ROIC histórico (0.176)" in g7(h0)[0]["detalle"] and "perímetro F1" not in g7(h0)[0]["detalle"])
paso("GRAM · con A2: G7 BUENO deja de saltar (0,209 < 2 × 14,82 % = 0,296)", not g7(h1), str([x["detalle"][:80] for x in g7(h1)]))
paso("GRAM · G4 sigue igual con A2: tres G4 sin justificar con C18 = No (0,13/0,15/0,15 > r + 0,03); el hallazgo recuerda la vara P-FOSO",
     [x["escenario"] for x in g4(h1)] == ["MALO", "NORMAL", "BUENO"] and all(not x["justificada"] for x in g4(h1)) and c1 == 1
     and all("P-FOSO" in x["detalle"] and "0.1303" in x["detalle"] for x in g4(h1)) and all("P-FOSO" not in x["detalle"] for x in g4(h0)))
h2, _ = gramatica({**copy.deepcopy(T0), "perimetro_f1": pf1}, motor="B")
paso("SIN · con motor B el perímetro F1 no cambia G7", [x["escenario"] for x in g7(h2)] == ["BUENO"] and "perímetro F1" not in g7(h2)[0]["detalle"])
paso("SIN · sin perímetro, los hallazgos fuera de G7/G4 son idénticos con y sin la clave", [x for x in h0 if x["id"] not in ("G7", "G4")] == [x for x in h1 if x["id"] not in ("G7", "G4")])
# un G7 que salta también con el perímetro: S2C 9,0 en el BUENO → 9 × 0,045 × (1 − 0,214) = 0,318 > 0,296
fb = json.load(open(os.path.join(EXP, "fase_b.json"), encoding="utf-8"))
tmp = tempfile.mkdtemp(prefix="perimetro_foso_gram_")
try:
    for n in ("fase_a.json", "referencias_mecanicas.json"):
        shutil.copy(os.path.join(EXP, n), os.path.join(tmp, n))
    fb["palancas"]["s2c"]["BUENO"]["valor"] = 9.0
    json.dump(fb, open(os.path.join(tmp, "fase_b.json"), "w", encoding="utf-8"), ensure_ascii=False)
    json.dump({**copy.deepcopy(T0), "perimetro_f1": pf1}, open(os.path.join(tmp, "datos_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
    g = GR.Gramatica(tmp, "antes", False, CFG)
    g.correr()
    x7 = g7(g.h)
    paso("GRAM · con A2 G7 sigue saltando por encima de 2 × el ROIC del perímetro (S2C 9,0 → 0,318 > 0,296) y lo rotula",
         [x["escenario"] for x in x7] == ["BUENO"] and "0.296" in x7[0]["detalle"] and "perímetro F1 A2_propio" in x7[0]["detalle"])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# =========================================================================================== F1 · V-F1g / V-F1k por valores (D3)
COLS = "CDEFGHIJKL"
ANIOS = list(range(2016, 2026))
REG = {"fecha": "2026-11-18", "persona": "prueba sintética", "motivo": "caso de prueba"}


def libro(pal=None):
    """Libro sintético del motor A (solo valores) con arrendamientos: ventas 1000, EBIT 70, D&A 30 (ROU 10, PPA 5), τ 0,2, capex 20,
    capital invertido 600 con 200 de arrendamientos. Las anclas, con las fórmulas de la plantilla."""
    v, e, da, tau, capex, princ, cap, arr = 1000.0, 70.0, 30.0, 0.2, 20.0, 10.0, 600.0, 200.0
    L = {"sha256": "sintetico", "Diagnóstico V6!C5": "A", "Control maestro!L4": "IFRS", "Diagnóstico V6!C179": 0.05, "Análisis!C56": 0.09}
    for c, y in zip(COLS, ANIOS):
        for fila, x in ((5, y), (6, v), (7, e), (8, da), (10, tau), (12, capex), (13, 0.0), (14, 0.0), (17, princ), (23, arr), (32, cap),
                        (16, 0.0), (18, 0.0)):
            L[f"Historia!{c}{fila}"] = x
        L[f"Historia!{c}11"] = 50.0 + capex + 2.0 + princ
        L[f"Historia!{c}35"] = 50.0
    L.update({"Historia!C57": 3, "Historia!C70": 50.0, "Historia!C44": v, "Historia!C48": e / v, "Historia!C52": tau, "Historia!C53": "",
              "Historia!C54": v / cap, "Historia!C55": e * (1 - tau) / cap,
              "Historia!C58": (e * (1 - tau) - (capex - da) - 50.0) / v,
              "Análisis!C46": 82.0, "Análisis!C47": capex, "Análisis!C48": 2.0, "Análisis!C49": princ, "Análisis!C50": 0.0, "Análisis!C51": "Sí", "Análisis!C52": 50.0})
    for c, (g15, mo, s2c, gi, roic) in (pal or {}).items():
        L[f"Palancas!{c}14"], L[f"Palancas!{c}15"], L[f"Palancas!{c}16"], L[f"Palancas!{c}18"], L[f"Análisis!{c}68"] = g15, mo, s2c, roic, gi
    for c in "BCD":
        L[f"Diagnóstico V6!{c}178"], L[f"Diagnóstico V6!{c}176"], L[f"Diagnóstico V6!{c}177"] = 0.01, 0.11, 0.1
    return L


def decl(per="A2_propio"):
    s = lambda x: {str(y): {"valor_fuente": -x, "signo": -1, "tratamiento": "entre paréntesis", "documento": "sintético", "pagina": 1, "literal": f"({x})"}  # noqa: E731
                   for y in ANIOS}
    return {"norma_contable": {"valor": "NIIF", "registro": REG}, "perimetro_reinversion": {"valor": per, "registro": REG},
            "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REG}, "perimetro_palancas_s2c": {"valor": per, "registro": REG},
            "perimetro_roic": {"valor": per, "registro": REG}, "clasificacion_compras": {"valor": "sin_compras", "registro": REG},
            "transicion": {"conocida": False, "tratamiento": None, "registro": REG}, "series": {"da_rou": s(10), "da_ppa": s(5)}}


def fila(r, gid):
    return [x for x in r["guardas"] if x["id"] == gid]


r_sin = M.evaluar(libro(), decl())
gs = fila(r_sin, "V-F1g")
paso("F1 · V-F1g sin palancas (paso 7) ya no afirma «palancas S2C en el mismo perímetro»: dice que compara etiquetas, no cifras",
     gs and not gs[0]["salta"] and "palancas S2C en el mismo perímetro" not in gs[0]["detalle"] and "no cifras" in gs[0]["detalle"]
     and "no cifras" in fila(r_sin, "V-F1k")[0]["detalle"])
paso("F1 · sin palancas: «V-F1g (valores)» y «V-F1k (valores)» dicen «aún sin palancas» y no saltan",
     all(fila(r_sin, k) and not fila(r_sin, k)[0]["salta"] and "aún sin palancas" in fila(r_sin, k)[0]["detalle"] for k in ("V-F1g (valores)", "V-F1k (valores)"))
     and r_sin["perimetro_f1_valores"] == {"palancas": None})
PAL_TODO = {"B": (0.0, 0.03, 1.3, 0.01, 0.13), "C": (0.025, 0.04, 1.6, 0.02, 0.15), "D": (0.04, 0.045, 1.8, 0.025, 0.15)}
PAL_PROP = {"B": (0.0, 0.03, 1.9, 0.01, 0.09), "C": (0.025, 0.04, 2.5, 0.02, 0.09), "D": (0.04, 0.045, 2.8, 0.025, 0.12)}
r_t = M.evaluar(libro(PAL_TODO), decl())
r_p = M.evaluar(libro(PAL_PROP), decl())
vt, vp = (fila(r_t, "V-F1g (valores)") or [{}])[0], (fila(r_p, "V-F1g (valores)") or [{}])[0]
paso("F1 · con palancas: V-F1g (valores) INFORMA y señala el NORMAL más cerca de C54 (todo el capital, 1,67) que del ancla del perímetro "
     "(S2C medio sin arrendamientos 2,5)", vt.get("salta") and vt.get("severidad") == "INFORMA" and "NORMAL: la cifra se parece más a la de todo el capital" in vt.get("detalle", ""))
paso("F1 · con el S2C del perímetro (NORMAL 2,5) la fila informa sin señalar; nunca bloquea", vp and not vp.get("salta") and not any(
     x["severidad"] == "BLOQUEA" for x in fila(r_t, "V-F1g (valores)") + fila(r_t, "V-F1k (valores)")))
kv = (r_t.get("perimetro_f1_valores") or {}).get("palancas") or {"NORMAL": {"roic_neutro": None, "exceso_sobre_neutro": None}}
N = 0.04 * (1 - 0.2)
fA2 = (70 * 0.8 - (20 - 15) - 50) / 1000   # f del perímetro A2: D_X = D&A − ROU − PPA = 15
paso("F1 · V-F1k (valores): ROIC terminal frente al neutro r·N/(N − f) con la f del perímetro; exceso del NORMAL 0,15 sobre el neutro",
     cerca(kv["NORMAL"]["roic_neutro"], 0.09 * N / (N - fA2), 1e-9) and cerca(kv["NORMAL"]["exceso_sobre_neutro"], 0.15 - 0.09 * N / (N - fA2), 1e-9)
     and (fila(r_t, "V-F1k (valores)") or [{}])[0].get("severidad") == "INFORMA", f"neutro {kv['NORMAL']['roic_neutro']}")
r_a0 = M.evaluar(libro(PAL_TODO), decl("A0_total"))
paso("SIN · con A0_total no hay filas «(valores)» ni detalle numérico (nada cambia para los expedientes sin perímetro propio)",
     not fila(r_a0, "V-F1g (valores)") and not fila(r_a0, "V-F1k (valores)") and r_a0.get("perimetro_f1_valores") is None)
paso("SIN · la guarda por etiquetas sigue bloqueando un perímetro declarado distinto (palancas A0 con reinversión A2)",
     any(x["salta"] and x["severidad"] == "BLOQUEA" for x in fila(M.evaluar(libro(PAL_TODO), {**decl(), "perimetro_palancas_s2c": {"valor": "A0_total", "registro": REG}}), "V-F1g")))

n_ok = sum(1 for _, ok in R if ok)
print(f"\n{n_ok}/{len(R)} pruebas del perímetro F1 y la vara del foso (P-FOSO) PASAN")
sys.exit(0 if n_ok == len(R) else 1)
