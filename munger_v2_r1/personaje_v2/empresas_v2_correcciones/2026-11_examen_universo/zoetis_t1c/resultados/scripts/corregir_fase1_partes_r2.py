#!/usr/bin/env python3
"""zoetis_t1c · ronda 2 de correcciones de extracción comprobadas (encargo del coordinador del 18-nov-2026, noche, tras la revisión independiente
del registro de Zoetis: munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/zoetis/revision_registro/REVISION.md y REVISION.tsv @ 1563156).
Cada cambio se comprobó antes en texto/.
 1) EBIT derivado (fila 7): «Interest expense, net of capitalized interest» se imprime en POSITIVO dentro de «Costs and expenses» (p. ej. 222 en
    2025, 10-K 2025 PDF p. 66; igual en los diez 10-K), así que EBIT = BAI + ese gasto. El extractor le puso signo −1 (pensado para un gasto
    impreso entre paréntesis, prompts/historia_anio.md) y el EBIT salía BAI − intereses (3.138 en 2025 en vez de 3.582). Se pone signo +1 en el
    componente de intereses de ebit_derivado en todos los informes (lados actual y anterior). «Other (income)/deductions—net» sigue dentro del
    EBIT (regla vigente: no es componente).
 2) Adquisiciones (fila 13): 2017 (D13): «Net proceeds from sales of assets» son ventas de ACTIVOS, no de negocios; el propio 10-K 2017 (AR_2017)
    solo toma «Acquisitions (82)», así que se retiran del comparativo de AR_2018 (y del lado actual, por coherencia): D13 = 82 (antes 119). 2023
    (J13): «Proceeds from sale of businesses, net of cash sold 293 96 —» es un COBRO por venta de negocios: signo +1 (como K13 en AR_2025): J13 =
    155 − 96 = 59 (antes 251).
 3) Ceros cuya cita no los probaba: intereses en financiación 2016–2025 → la línea suplementaria «Interest, net of capitalized interest» (los
    intereses pagados se informan aparte, en explotación con US GAAP; la sección de financiación no tiene línea de intereses), en la página del
    estado de flujos de cada 10-K; principal y pasivo de arrendamientos (financieros) 2016–2022 → la nota de arrendamientos de cada 10-K, que solo
    describe arrendamientos operativos (2016–2018: «We have facilities, vehicles and office equipment under various non-cancellable operating
    leases with third parties.»; 2019–2022: «Our current portfolio includes only operating leases which are recorded as a right of use»). El
    comparativo de 2018 de AR_2019 (pasivo OPERATIVO «—») se retira: la fila 23 lleva solo financieros y 2018 se toma del cero de AR_2018.
 No se cambia (límite, se informa): minoritarios negativos de 2022 y 2023 (impresos (2) y (6)): fase1_historia.py aplica valor absoluto a
 «minoritarios», así que el signo impreso no se puede llevar a la Historia sin cambiar el producto.
Uso: python3 -I corregir_fase1_partes_r2.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import copy, hashlib, json, os, shutil, sys
C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
P = os.path.join(C, "fase1_partes")
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
docs = {a: json.load(open(os.path.join(P, f"AR_{a}.json"), encoding="utf-8")) for a in range(2016, 2026)}
nuevos = copy.deepcopy(docs)
cambios = []


def reg(a, partida, campo, antes, despues, motivo):
    cambios.append({"archivo": f"fase1_partes/AR_{a}.json", "partida": partida, "campo": campo, "antes": antes, "despues": despues, "motivo": motivo})


M1 = ("«Interest expense, net of capitalized interest» se imprime en positivo dentro de «Costs and expenses» (estado de resultados): EBIT = BAI + gasto por "
      "intereses; el signo −1 lo restaba (revisión del registro de Zoetis, punto 1)")
for a in range(2016, 2026):
    p = nuevos[a]["partidas"]["ebit_derivado"]
    for lado in ("actual", "anterior"):
        for i, c in enumerate(p.get(lado) or []):
            if c.get("signo") == -1:
                assert c["concepto"].lower().startswith("interest expense") and "(" not in c["impreso"], (a, lado, c)
                antes = dict(c)
                c["signo"] = 1
                reg(a, "ebit_derivado", f"{lado}[{i}].signo", antes, dict(c), M1)
    p["nota"] = ("(zoetis_t1c, ronda 2) EBIT derivado = BAI + «Interest expense, net of capitalized interest» (gasto impreso en positivo: signo +1); "
                 "«Other (income)/deductions—net» sigue dentro del EBIT. Nota anterior: " + str(p.get("nota")))
# adquisiciones
p = nuevos[2018]["partidas"]["adquisiciones"]
for lado in ("actual", "anterior"):
    antes = copy.deepcopy(p[lado])
    p[lado] = [c for c in p[lado] if not c["concepto"].startswith("Net proceeds from sales of assets")]
    assert len(p[lado]) == len(antes) - 1
    reg(2018, "adquisiciones", lado, antes, p[lado], "«Net proceeds from sales of assets» (56 en 2018, 37 en 2017) son ventas de activos, no de negocios (el 10-K 2017 tampoco las resta: AR_2017 solo «Acquisitions (82)»); con signo −1 se sumaban como pagos: D13 = 82")
p["nota"] = "(zoetis_t1c, ronda 2) Sin las ventas de activos (no son ventas de negocios). Nota anterior: " + str(p.get("nota"))
p = nuevos[2024]["partidas"]["adquisiciones"]
for lado in ("actual", "anterior"):
    for i, c in enumerate(p[lado]):
        if c["concepto"].startswith("Proceeds from sale of businesses"):
            assert c.get("signo") == -1 and "(" not in c["impreso"]
            antes = dict(c); c["signo"] = 1
            reg(2024, "adquisiciones", f"{lado}[{i}].signo", antes, dict(c), "cobro por venta de negocios impreso en positivo: resta de las adquisiciones (signo +1, como en AR_2025): J13 = 155 − 96 = 59")
p["nota"] = "(zoetis_t1c, ronda 2) Cobros por venta de negocios con su signo impreso (+1). Nota anterior: " + str(p.get("nota"))
# ceros
CF = {2016: 76, 2017: 74, 2018: 76, 2019: 75, 2020: 78, 2021: 76, 2022: 68, 2023: 69, 2024: 68, 2025: 70}
for a, pg in CF.items():
    p = nuevos[a]["partidas"]["intereses_financiacion"]
    antes = p.get("cero")
    assert antes and not p.get("actual") and not p.get("anterior"), a
    p["cero"] = {"motivo": "US GAAP (ASC 230): los intereses pagados van en el flujo de explotación; el estado de flujos los da solo como información suplementaria («Cash paid during the period for: … Interest, net of capitalized interest») y su sección de financiación no tiene línea de intereses: 0 en financiación",
                 "pagina": pg, "cita": "Interest, net of capitalized interest"}
    reg(a, "intereses_financiacion", "cero", antes, p["cero"], "cita anterior sin relación con el dato (revisión, punto 5)")
NOTA16 = "We have facilities, vehicles and office equipment under various non-cancellable operating leases with third parties."
SOLO = "Our current portfolio includes only operating leases which are recorded as a right of use"
PL = {2016: (106, NOTA16), 2017: (103, NOTA16), 2018: (110, NOTA16), 2019: (77, SOLO), 2020: (80, SOLO), 2021: (78, SOLO), 2022: (70, SOLO)}
for a, (pg, cita) in PL.items():
    for k, que in (("arrendamientos_principal", "sin pagos de principal de arrendamientos financieros"), ("arrendamientos", "sin pasivo por arrendamientos financieros (la fila 23 lleva solo financieros)")):
        p = nuevos[a]["partidas"][k]
        antes = p.get("cero")
        if antes is None:
            continue
        p["cero"] = {"motivo": f"{a}: la nota de arrendamientos solo describe arrendamientos operativos (no hay arrendamientos financieros hasta 2023: 10-K 2023 PDF p. 87, «Finance lease liabilities … 1 —»): {que}",
                     "pagina": pg, "cita": cita}
        reg(a, k, "cero", antes, p["cero"], "cita anterior que no probaba el cero (revisión, punto 5)")
p = nuevos[2019]["partidas"]["arrendamientos"]
antes = copy.deepcopy(p["anterior"])
assert len(antes) == 1 and antes[0]["impreso"] == "—"
p["anterior"] = []
reg(2019, "arrendamientos", "anterior", antes, [], "comparativo de 2018 del pasivo OPERATIVO («—»): la fila 23 lleva solo financieros; 2018 se toma del cero de AR_2018")
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
ORIG = os.path.join(ANT, "fase1_partes_original")
R = {"fecha": "2026-11-18", "autor": "orquestación (Claude, agente de implementación), encargo del coordinador; sin firma humana", "guion": os.path.abspath(__file__),
     "fuente_de_las_correcciones": "revisión independiente del registro de Zoetis (munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/zoetis/revision_registro/, @ 1563156), comprobada en texto/",
     "no_aplicado": "minoritarios negativos de 2022 (I26, impreso (2)) y 2023 (J26, impreso (6)): fase1_historia.py aplica abs() a «minoritarios»; llevar el signo exige cambiar el producto (inmaterial)",
     "archivos": [], "cambios": cambios}
for a, dd in nuevos.items():
    if dd == docs[a]:
        continue
    src = os.path.join(P, f"AR_{a}.json")
    shutil.copy2(src, os.path.join(O, f"AR_{a}.json"))
    if not os.path.exists(os.path.join(ORIG, f"AR_{a}.json")):
        shutil.copy2(src, os.path.join(ORIG, f"AR_{a}.json"))   # original de zoetis_t1b (no lo tocó la ronda 1)
    json.dump(dd, open(src, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    R["archivos"].append({"archivo": f"fase1_partes/AR_{a}.json", "antes": f"antecedentes/fase1_partes_antes_de_r2/AR_{a}.json", "antes_sha256": h(os.path.join(O, f"AR_{a}.json")), "despues_sha256": h(src)})
json.dump(R, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"OK: {len(R['archivos'])} archivos, {len(cambios)} cambios; comprobar_anio sin errores")
