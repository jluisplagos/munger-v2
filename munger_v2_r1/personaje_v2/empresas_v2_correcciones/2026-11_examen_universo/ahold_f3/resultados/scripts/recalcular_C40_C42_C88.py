#!/usr/bin/env python3
"""ahold_f3 · cifras de juicio desfasadas recalculadas antes de la fase A (encargo del coordinador del 18-nov-2026, noche, tras la revisión
independiente del registro de Ahold: munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/ahold/revision_registro/REVISION.md y .tsv @ 1f6cdc7).
Cada cifra se comprobó antes en texto/ (Q2-2026 PDF p. 11, 13 y 15; AR2020 p. 149, AR2021 p. 184, AR2022 p. 194, AR2023 p. 204, AR2024 p. 263,
AR2025 p. 65 y 216).
 - C42 (EV/EBITDA): la etapa 1 usaba una capitalización sin fuente (28.626 = 33,14 € × 863,79 M). Con C41 vigente = C37 36,05 × C55 886,877259
   (P-O2 a) = 31.971,925: EV = 31.971,925 + deuda C54 19.261 − caja C53 3.196 − negocios conjuntos 244 (Q2-26 p. 13); EBITDA LTM = EBIT 2025 3.542 +
   (1.760 − 1.741) + D&A 2025 3.733 + (1.828 − 1.870) = 7.252 (misma definición que la etapa 1 y que C33).
 - C40 (FCF LTM para el FCF yield): misma definición que la caja base tras P-O1 (c) «regla espejo»: al FCF LTM de la etapa 1 (CFO − capex − intereses
   pagados − pagos de arrendamientos = 1.821) se suman dividendos de negocios conjuntos (21 + 28 − 22 = 27), intereses cobrados (50 + 130 − 76 = 104)
   y cobros de subarriendos (74 + 138 − 68 = 144): 2.096. Salvaguarda de P-O1: C76 = 0, así que los intereses cobrados entran.
 - C88 (P/FCF histórico, mediana 2019–2025): misma definición con P-O1: capitalización de cierre (AR2025 p. 65) ÷ (CFO − capex − intereses − pagos
   de arrendamientos + dividendos de negocios conjuntos + intereses cobrados + cobros de subarriendos), cada año del comparativo del informe
   siguiente (la misma fuente que la Historia).
Hace lo que cambiar_base.py hace con una entrada `analisis` (vaciar en la copia de la etapa 1 + evidencia en Control maestro + entrada declarada en
fase1_metadatos.json), sobre el expediente ya preparado; guarda antes la copia de la etapa 1, los textos y los metadatos en antecedentes/.
Uso: python3 -I recalcular_C40_C42_C88.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO.json"""
import hashlib, json, os, shutil, statistics, sys
C, ANT, REG = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
from v63_xml import LibroV63  # noqa: E402
import cambiar_base as CB  # noqa: E402
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
meta_p = os.path.join(C, "fase1_metadatos.json")
meta = json.load(open(meta_p, encoding="utf-8"))
c41 = meta["capitalizacion"]["valor"]
assert abs(c41 - 36.05 * 886.877259) < 1e-6 and meta["precio"]["valor"] == 36.05
H = json.load(open(os.path.join(C, "datos_v63.json"), encoding="utf-8"))["historia"]["partidas"]
assert (H["ebit"][-1], H["da"][-1]) == (3542, 3733)
# C42
ev = c41 + 19261 - 3196 - 244
ebitda = 3542 + (1760 - 1741) + 3733 + (1828 - 1870)
c42 = ev / ebitda
# C40
fcf_ant = (2500 + 6989 - 2891) - (1229 + 2564 - 1227) - (178 + 261 - 168) - (980 + 1944 - 984)
assert fcf_ant == 1821
cobros_ltm = {"dividendos_negocios_conjuntos": 21 + 28 - 22, "intereses_cobrados": 50 + 130 - 76, "cobros_subarriendos": 74 + 138 - 68}
c40 = fcf_ant + sum(cobros_ltm.values())
# C88
cap = {2025: 30659, 2024: 28668, 2023: 24615, 2022: 26232, 2021: 30482, 2020: 24197, 2019: 24751}   # AR2025 p. 65
cobros = {2019: (36, 56, 94, "AR2020 p. 149"), 2020: (16, 24, 99, "AR2021 p. 184"), 2021: (28, 16, 103, "AR2022 p. 194"), 2022: (38, 56, 115, "AR2023 p. 204"),
          2023: (22, 160, 117, "AR2024 p. 263"), 2024: (22, 196, 125, "AR2025 p. 216"), 2025: (28, 130, 138, "AR2025 p. 216")}
anios = H["anio"]
pfcf = {}
for y in range(2019, 2026):
    i = anios.index(y)
    fcf = H["cfo"][i] - H["capex"][i] - H["intereses_financiacion"][i] - H["arrendamientos_principal"][i] + sum(cobros[y][:3])
    pfcf[y] = {"capitalizacion": cap[y], "fcf_regla_espejo": fcf, "p_fcf": cap[y] / fcf, "cobros": cobros[y]}
c88 = statistics.median(v["p_fcf"] for v in pfcf.values())
txt = {
 "C42": {"L": "Q2-26 PDF p. 11, 13 y 15; AR2025 PDF p. 216; Análisis C41, C53 y C54",
         "M": f"EV/EBITDA = (C41 31.971,925 + C54 19.261 − C53 3.196 − negocios conjuntos 244) ÷ EBITDA LTM (3.542 + 1.760 − 1.741 + 3.733 + 1.828 − 1.870 = 7.252) = {ev:.3f} ÷ {ebitda} = {c42:.6f}",
         "N": "[Clase: derivado de datos publicados] Recalculado en ahold_f3 (revisión del registro de Ahold, punto 3): la etapa 1 usaba una capitalización sin fuente (28.626 = 33,14 € × 863,79 M) y daba 6,129; ahora usa C41 (36,05 € × 886,877259 M, P-O2 a). Las sensibilidades de la etapa 1 (6,12x, 6,05x, 6,17x…) se calcularon con la capitalización antigua y se retiran."},
 "C40": {"L": "Q2-26 PDF p. 15; AR2025 PDF p. 216",
         "M": (f"FCF LTM a 28-jun-2026 con la regla espejo (P-O1 c), misma definición que la caja base: CFO 6.598 − capex 2.566 − intereses pagados 271 − pagos de "
               f"arrendamientos 1.940 (= 1.821 de la etapa 1) + dividendos de negocios conjuntos 27 + intereses cobrados 104 + cobros de subarriendos 144 = {c40}; "
               "cada partida LTM = 1S-2026 + 2025 − 1S-2025"),
         "N": "[Clase: derivado de datos publicados] Recalculado en ahold_f3 (revisión del registro, C40): la etapa 1 (1.821) es anterior a P-O1; C76 = 0, así que los intereses cobrados entran (salvaguarda de P-O1). Las variantes de la etapa 1 (1.763, 2.220, 2.054, 1.849) tienen la definición anterior. La propia definición de FCF de Ahold (Q2-26 p. 23) suma esos cobros."},
 "C88": {"L": "AR2025 PDF p. 65; AR2020 p. 149, AR2021 p. 184, AR2022 p. 194, AR2023 p. 204, AR2024 p. 263, AR2025 p. 216; Historia F11:L17",
         "M": "Mediana 2019–2025 de capitalización de cierre ÷ FCF con la regla espejo (P-O1 c): " + "; ".join(f"{y} {v['capitalizacion']} ÷ {v['fcf_regla_espejo']} = {v['p_fcf']:.2f}" for y, v in pfcf.items()) + f" → mediana {c88:.4f}",
         "N": "[Clase: derivado de datos publicados] Recalculado en ahold_f3 (revisión del registro, C88): la etapa 1 (14,7x) es anterior a P-O1; con la regla espejo baja a 12,5x (estimación del revisor ≈ 12,5x). Cobros de cada año del comparativo del informe siguiente, como la Historia."}}
valores = {"C40": c40, "C42": c42, "C88": c88}
e1 = os.path.join(C, "etapa1", "Ahold_evaluada.xlsx")
dst = os.path.join(ANT, "etapa1_antes_de_C40_C42_C88")
os.makedirs(dst)
shutil.copy2(e1, os.path.join(dst, "Ahold_evaluada.xlsx"))
shutil.copy2(meta_p, os.path.join(dst, "fase1_metadatos.json"))
lb = LibroV63(e1)
antes = {}
esperado = {"C40": 1821, "C42": 6.129, "C88": 14.7}
for c, v in valores.items():
    a = lb.leer("Análisis", c)
    assert abs(float(a) - esperado[c]) < 1e-3, (c, a)
    antes[f"Análisis!{c}"] = a
    lb.escribir("Análisis", c, None)
    r = CB.fila_de(lb, "Control maestro", f"Análisis!{c}")
    for col, t in txt[c].items():
        antes[f"Control maestro!{col}{r}"] = lb.leer("Control maestro", f"{col}{r}")
        lb.escribir("Control maestro", f"{col}{r}", t, tipo="texto")
lb.marcar_modificada("Análisis")
lb.marcar_modificada("Control maestro")
lb.guardar(e1)
json.dump({"valores_y_textos_anteriores": antes}, open(os.path.join(dst, "evidencia_anterior.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
for c, v in valores.items():
    meta.setdefault("analisis", {})[c] = {"valor": v, "fuente": txt[c]["M"], "pagina": txt[c]["L"], "periodo": {"C40": "12 meses a 28-jun-2026", "C42": "EV con precio del 13-nov-2026 y balance a 28-jun-2026; EBITDA LTM a 28-jun-2026", "C88": "mediana 2019–2025"}[c],
                                           "unidad": {"C40": "mm", "C42": "x", "C88": "x"}[c]}
json.dump(meta, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"fecha": "2026-11-18", "guion": os.path.abspath(__file__), "antes": antes, "despues": valores, "ev": ev, "ebitda_ltm": ebitda, "cobros_ltm": cobros_ltm, "p_fcf_por_anio": pfcf,
           "etapa1_antes_sha256": h(os.path.join(dst, "Ahold_evaluada.xlsx")), "etapa1_despues_sha256": h(e1),
           "no_tocado": "aux:etapa1_capitalizacion_oct2026 está en el registro del repositorio auxiliar (coordinacion/cierre-v2), no en el expediente: en el expediente la convención desaparece (C42 deriva de C41); el auxiliar del registro hay que retirarlo al sellar ahold_f3",
           "motivo": "cifras de juicio desfasadas (precio/acciones de la etapa 1 y definición anterior a P-O1) que la fase A vería"}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(valores)
