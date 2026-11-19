#!/usr/bin/env python3
"""zoetis_t1d · correcciones del registro de entradas (verificacion_entradas.json, conservado de zoetis_t1c y sellado por «Claude revisor sellado»,
coordinacion/cierre_v2/examen/zoetis/revision_registro/REVISION_SELLADO.md @ 4743cb0) que piden el sellado, las decisiones Z-ACC, Z-R y Z-MIN de la persona
responsable (19-nov-2026) y los datos de mercado con bytes de la Release (anexo 3). Extractor: «Claude orquestación». Cada entrada corregida o nueva queda
PENDIENTE (sin revisor ni vínculo): la revisará otro agente. Las demás no se tocan; su sello sigue solo si `verificacion_entradas.py comprobar` mantiene su
vínculo vigente (nada se reescribe a mano). Uso: python3 -I corregir_registro_zoetis_t1d.py CARPETA_EMPRESA CARPETA_ANTECEDENTES REGISTRO_CAMBIOS.json"""
import copy, hashlib, json, os, shutil, sys
from fractions import Fraction as F
C, ANT, REG = sys.argv[1:4]
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
cons = os.path.join(ANT, "verificacion_entradas_conservado_de_zoetis_t1c.json")
assert not os.path.exists(cons)
shutil.copy2(p, cons)
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"]}
HOY = "2026-11-19"
cambios = []
RM = json.load(open(os.path.join(os.path.dirname(ANT), "resultados", "fuentes_mercado_zoetis_t1d.json"), encoding="utf-8"))
FM = {os.path.basename(a["archivo"]): a for a in RM["archivos"]}


def pendiente(e, nota, nueva=False):
    antes = None if nueva else copy.deepcopy(e)
    c0 = (e.get("comprobacion") or {}) if not nueva else {}
    e["comprobacion"] = {"extractor": "Claude orquestación", "revisor": None, "fecha": HOY, "resultado": "pendiente", "fuente_examinada": None,
                         "nota": f"[Claude orquestación, {HOY}, zoetis_t1d] {nota}"
                         + ("" if nueva else f" · Comprobación anterior (zoetis_t1c): {c0.get('revisor')} {c0.get('fecha')} «{c0.get('resultado')}»: {str(c0.get('nota'))[:500]}"),
                         "vinculo": None}
    cambios.append({"celda": e["celda"], "antes": antes, "despues": copy.deepcopy(e)})


ZACC = ("Desalineación de fechas declarada (decisión Z-ACC de la persona responsable, 19-nov-2026: se mantienen las acciones al cierre del ejercicio, P-O2): "
        "precio del 8-oct-2026 × acciones en circulación al 31-dic-2025")
# 1) C55: acciones exactas (dato publicado: la cifra impresa × 10⁻⁶), sin el redondeo a 3 decimales
AUXA = "aux:zoetis-10k-fy2025_p68_common_stock_shares_outstanding_2025"
assert E[AUXA]["valor_modelo"] == 424.927535 and E[AUXA]["comprobacion"]["resultado"] == "verificado"
e = E["Análisis!C55"]
e["clase"] = "dato_publicado"; e["valor_modelo"] = 424.927535; e["derivacion"] = None
f = copy.deepcopy(E[AUXA]["fuente"])
f["concepto"] = "acciones en circulación al 31-dic-2025 (Common stock … shares outstanding at December 31, 2025), en millones"
f["tratamiento"] = ("cifra impresa en acciones (424.927.535); escala 1e-6 la pasa a millones, sin redondear (un número de acciones no es un importe); sin dilución "
                    "(fase1_metadatos.json: impreso «424,927,535», escala_impreso «unidades»; fase1_historia.py comprueba que valor = impreso × escala). P-O2: acciones al "
                    "cierre del ejercicio, no media ponderada. " + ZACC + " (la desalineación se declara en C41 y C42, que combinan ambos).")
e["fuente"] = f
pendiente(e, "C55 = 424,927535 exacto (sellado de zoetis_t1c: el redondeo a 3 decimales no se justificaba para acciones); dato publicado con la misma fuente que el auxiliar sellado " + AUXA + "; configuracion/cambio_zoetis_t1d.json")
# 2) C41 = C37 × C55 sin redondear
e = E["Análisis!C41"]
assert F(repr(73.08)) * F(repr(424.927535)) == F("31053.7042578")
e["valor_modelo"] = 31053.7042578
e["derivacion"]["conciliacion"] = ("capitalización = C37 73,08 × C55 424,927535 = 31.053,7042578 exacto = libro (sin redondear las acciones ni el resultado; en zoetis_t1c "
                                    "salía 0,034 mm más con C55 redondeado). " + ZACC + "; con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 PDF p. 5) sería 30.266,37768168. "
                                    "C37: captura de investor.zoetis.com del 8-oct-2026 conservada en fuentes_mercado/ (anexo 3 ter).")
e["incidencia"] = "C37 sale ahora de la captura de investor.zoetis.com del 8-oct-2026 conservada en fuentes_mercado/ (anexo 3 ter), pendiente de revisor."
pendiente(e, "C41 = C37 × C55 exactos (sellado de zoetis_t1c); Z-ACC declarada")
# 3) C33, C40 y C42: convención/aproximación declarada (Fiscal Year Alignment), no derivado exacto
FYA = ("El TTM a 30-jun-2026 se forma con 2025 del 10-K (base anterior a la «Fiscal Year Alignment») − 6M-2025 + 6M-2026 del 10-Q del T2 2026 (base nueva); "
       "el 10-Q da el 6M-2025 «as previously reported» para el BAI (1.712) y el CFO (1.073), que se usan, pero solo reexpresado para intereses (107), D&A (243) "
       "y capex (324): esos tres mezclan bases (10-Q T2 2026 PDF p. 3, 8, 10 y 11)")
JCL = ("{c} es una aproximación declarada, no un derivado exacto del concepto: " + FYA + ". Se registra como convención con su fundamento (como C24; "
       "REVISION_SELLADO.md de zoetis_t1c); la fórmula de «derivacion» solo documenta la aproximación.")
HIP = {
 "Análisis!C33": dict(alt="Con el 6M-2025 todo reexpresado sale ≈ 1,88x; con el 10-Q del T2 2025 en base antigua (no está en el expediente) se podría rehacer en una sola base.",
                      lim="Mezcla bases (ver justificacion_clase). Sin acciones ni precio: no le afecta la desalineación de C41/C42 (deuda neta del 30-jun-2026 y EBITDA de 12 meses a esa fecha)."),
 "Análisis!C40": dict(alt="Todo reexpresado sale 2.316; con el 10-Q del T2 2025 en base antigua (no está en el expediente) se podría rehacer en una sola base.",
                      lim="Mezcla bases (ver justificacion_clase). Sin acciones ni precio: no le afecta la desalineación de C41/C42 (12 meses a 30-jun-2026)."),
 "Análisis!C42": dict(alt="Con el 6M-2025 todo reexpresado (BAI 1.685) ≈ 9,61x; con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 PDF p. 5) 9,48x; con el 10-Q del T2 2025 en base antigua se podría rehacer en una sola base.",
                      lim="Mezcla bases (ver justificacion_clase). " + ZACC + ", balance del 30-jun-2026 y EBITDA de 12 meses a esa fecha. Depende de C41 y de C37 (captura del 8-oct-2026, pendiente de revisor)."),
}
for c, x in HIP.items():
    e = E[c]
    assert e["clase"] == "derivado", c
    if c == "Análisis!C42":
        v = float((F("31053.7042578") + 9048 - 1476) / 3992)
        assert v == 9.675777619689379
        e["valor_modelo"] = v
        e["derivacion"]["conciliacion"] = ("APROXIMACIÓN (documental): EV ÷ EBITDA TTM = (C41 31.053,7042578 + 9.048 − 1.476) ÷ 3.992 = 9,675778 (entrada declarada en "
                                           "cambio_zoetis_t1d.json; en zoetis_t1c era 0,000008x más alto, con C41 de las acciones redondeadas). " + ZACC + ".")
        e["incidencia"] = e["incidencia"].replace("Depende de C41 (C37, fuente de mercado conservada).", "Depende de C41 (exacto en zoetis_t1d) y de C37 (captura de investor.zoetis.com, pendiente de revisor).")
    else:
        e["derivacion"]["conciliacion"] = "APROXIMACIÓN (documental): " + e["derivacion"]["conciliacion"]
    e["clase"] = "convencion"
    e["hipotesis"] = {"identificacion": "V-" + c.split("!")[1],
                      "fundamento": f"{c.split('!')[1]} = {e['valor_modelo']!r}: " + e["derivacion"]["conciliacion"].replace("APROXIMACIÓN (documental): ", "") + " " + FYA + ".",
                      "alternativas": x["alt"], "limites": x["lim"],
                      "procedencia": f"configuracion/cambio_zoetis_t1d.json (analisis {c.split('!')[1]}); Control maestro L–N de la fila de {c.split('!')[1]}; resultados/entradas_r3.json de zoetis_t1c"}
    e["justificacion_clase"] = JCL.format(c=c.split("!")[1])
    pendiente(e, f"{c.split('!')[1]}: de «derivado» a «convencion» con justificacion_clase (aproximación por la Fiscal Year Alignment; REVISION_SELLADO.md de zoetis_t1c)")
# 4) I26 y J26: minoritarios impresos en negativo → 0 (Z-MIN), con la cifra impresa en la conciliación
for celda, anio, aux in (("Historia!I26", 2022, "aux:zoetis-10k-fy2023_p67_noncontrolling_interests_2022"), ("Historia!J26", 2023, "aux:zoetis-10k-fy2024_p66_noncontrolling_interests_2023")):
    e = E[celda]
    assert e["clase"] == "dato_publicado" and e["fuente"]["valor_fuente"] in (-2, -6) and aux not in E
    impreso = e["fuente"]["valor_fuente"]
    fa = copy.deepcopy(e["fuente"])
    fa.update({"signo": 1, "tratamiento": "cifra publicada tal como se imprime, negativa (patrimonio deficitario de minoritarios); signo 1, sin transformación",
               "concepto": f"Equity attributable to noncontrolling interests, {anio} (impreso entre paréntesis: negativo)"})
    na = {"celda": aux, "id": "aux_minoritarios_impresos", "ambito": None, "uso": None, "material": True, "clase": "dato_publicado", "valor_modelo": impreso,
          "fuente": fa, "derivacion": None, "hipotesis": None, "justificacion": None, "comprobacion": None, "incidencia": None}
    d["entradas"].append(na); E[aux] = na
    pendiente(na, f"auxiliar nuevo: minoritarios {anio} impresos {impreso} (origen de {celda}; Z-MIN)", nueva=True)
    e["clase"] = "derivado"; e["valor_modelo"] = 0; e["fuente"] = {}
    e["derivacion"] = {"origenes": [aux], "formula": f'max(o["{aux}"], 0)',
                       "conciliacion": (f"minoritarios {anio}: el balance imprime ({abs(impreso)}) = {impreso} ({fa['archivo']} [PDF PAGE {fa['pagina']}], «{fa['cita']}»): "
                                        f"patrimonio NEGATIVO de minoritarios; la Historia guarda 0 por la decisión Z-MIN de la persona responsable (19-nov-2026: minoritarios "
                                        f"deficitarios → cero con aviso y la cifra impresa en el registro; fase1_historia.py, historia_revision.md «Signo de saldos impresos en "
                                        f"negativo»). max({impreso}, 0) = 0 = libro. En zoetis_t1c el libro guardaba +{abs(impreso)}."),
                       "unidad": "mm"}
    pendiente(e, f"{celda} = 0 con la cifra impresa {impreso} en la conciliación (Z-MIN; REVISION_SELLADO.md de zoetis_t1c)")
# 5) E26: cero publicado («—» del 10-K 2018), no dato ausente
e = E["Historia!E26"]; assert e["clase"] == "dato_ausente"
f = copy.deepcopy(E["Historia!D26"]["fuente"]); assert f["archivo"] == "texto/zoetis-10k-fy2018.txt" and f["pagina"] == 73
f.update({"concepto": "participación de no controladores en el patrimonio (impresa como guion; cero)", "columna": "2018 (columna del ejercicio corriente del informe 2018)",
          "periodo": "ejercicio 2018 (cerrado el 31-12-2018)", "reexpresado": "no aplica (ejercicio corriente del informe 2018; el 10-K 2019 no tiene la línea)",
          "tratamiento": "cero comprobado: «Equity attributable to noncontrolling interests» es «—» en 2018 (16 en 2017)", "valor_fuente": 0})
e["clase"] = "cero_comprobado"; e["valor_modelo"] = 0; e["fuente"] = f; e["justificacion"] = None
pendiente(e, "E26 = 0, cero publicado («—», 10-K 2018 PDF p. 73), con la corrección registrada de fase1_partes/AR_2018.json (resultados/correccion_fase1_partes_t1d.json)")
# 6) justificaciones de C86:G86 y C87:G87 (las series F1 se declaran solo para 2021–2025)
for fila, serie, extra in (("86", "F1.da_rou (amortización de derechos de uso de arrendamientos FINANCIEROS, D-US1: la de los operativos no está en la fila 8)",
                            "Además, hasta 2023 Zoetis solo tenía arrendamientos operativos (10-K 2023 PDF p. 87: los financieros aparecen en 2023), como dicen H86 e I86 (no aplicable)."),
                           ("87", "F1.da_ppa (ajustes de la contabilidad de compras «Amortization and depreciation» de la conciliación del beneficio ajustado, p. ej. 10-K 2022 PDF p. 52; cota superior de la PPA)",
                            "La partida SÍ se publica: el vacío no se debe a que falte, sino a que la serie no se declara para ese año.")):
    for col, anio in zip("CDEFG", range(2016, 2021)):
        e = E[f"Historia!{col}{fila}"]; assert e["clase"] == "dato_ausente" and e["valor_modelo"] is None
        e["justificacion"] = (f"Celda vacía en el libro (vacío no es cero). motor_a_f1.json declara C85 = A2_propio (US GAAP, D-US1) y la serie {serie} solo para 2021–2025 "
                              f"(H{fila}:L{fila}): la ventana de f (2023–2025) y los cinco años del ancla de S2C (2021–2025). {anio} no lo usa ningún cálculo del perímetro F1, así "
                              f"que no se declara; fase1_v63.json no declara cálculo para Historia!{col}{fila}. {extra}")
        pendiente(e, "justificación corregida (REVISION_SELLADO.md de zoetis_t1c: la serie F1 está declarada para 2021–2025)")
# 7) Z-R: agrupación geográfica de A31/B31 y A33/B33 sin cambios, con la diferencia anotada
ZR = ("Decisión Z-R de la persona responsable (19-nov-2026): se deja la agrupación y se anota la diferencia con las etiquetas del informe. ")
e = E["Palancas!A31"]
e["hipotesis"]["limites"] = (ZR + "La etiqueta «Región · Asia» no es una etiqueta del informe: suma China 227 + Japón 154 + «Other emerging markets» 913 (que mezcla Asia, "
                             "Latinoamérica, Europa del Este, Oriente Medio y África, sin desglose), así que atribuye a Asia ventas que no son solo suyas y fija con ellas la prima "
                             "de esa región en la r mínima. " + e["hipotesis"]["limites"])
pendiente(e, "Z-R: agrupación conservada con la diferencia anotada en «limites»")
e = E["Palancas!B31"]
e["derivacion"]["conciliacion"] += (" · " + ZR + "El peso incluye «Other emerging markets» (913 de 1.294 mm), que no es solo Asia (10-K 2025 PDF p. 77).")
pendiente(e, "Z-R: peso conservado con la diferencia anotada en la conciliación")
e = E["Palancas!A33"]
e["hipotesis"]["limites"] = (ZR + "La etiqueta «Región · Australia & New Zealand» no es una etiqueta del informe: suma Australia 329 + «Other developed markets» 641 (sin "
                             "desglose por país) + «Contract manufacturing & human health» 116 (sin ubicación de cliente). " + e["hipotesis"]["limites"])
pendiente(e, "Z-R: agrupación conservada con la diferencia anotada en «limites»")
e = E["Palancas!B33"]
e["derivacion"]["conciliacion"] += (" · " + ZR + "El peso incluye «Other developed markets» (641) y «Contract manufacturing & human health» (116) de 1.086 mm, que no son solo Australia y Nueva Zelanda (10-K 2025 PDF p. 77).")
pendiente(e, "Z-R: peso conservado con la diferencia anotada en la conciliación")
# 8) C57 y Palancas!C7 con los bytes oficiales de la Release
tt = FM["US_Treasury_par_yield_2026_Release_766892834.txt"]; tc = FM["US_Treasury_par_yield_2026_Release_766892834.csv"]
fila_t = tt["fila_usada"].split(" (columna")[0]
e = E["Análisis!C57"]
e["fuente"].update({
    "version": (f"CSV oficial us_treasury_par_yield_2026.csv subido por la persona responsable a la Release fuentes-examen-20261118 de jluisplagos/munger-v2-evidencias-mistral "
                f"(asset {tc['asset']}), descarga cruda conservada byte a byte en {tc['archivo']}, sha256 {tc['sha256']} (la huella publicada, RELEASE_FUENTES_EXAMEN_VERIFICACION.md "
                f"anexo 3); conservado como texto con marca [PDF PAGE 1] y celdas separadas por « | », sin tocar ninguna cifra, sha256 {tt['sha256']}"),
    "archivo": tt["archivo"], "sha256": tt["sha256"], "pagina": 1, "folio": None,
    "ubicacion": "tabla de la curva par diaria 2026 (cabecera «Date | 1 Mo | … | 10 Yr | 20 Yr | 30 Yr»), fila 10/08/2026",
    "columna": "10 Yr (13.ª columna)", "cita": fila_t, "valor_fuente": 5.22,
    "tratamiento": "tasa publicada en porcentaje; escala 0,01 la pasa a tanto por uno del modelo (5,22 % → 0,0522). Misma fecha que el precio (8-oct-2026)."})
pendiente(e, "C57 con los bytes del CSV oficial del Tesoro (Release, asset 766892834); resultados/fuentes_mercado_zoetis_t1d.json")
dt_ = FM["Damodaran_margin_industry_averages_2026-01_Release_766892761.txt"]; dx = FM["Damodaran_margin_2026-01_Release_766892761.xls"]
e = E["Palancas!C7"]
e["fuente"] = {
    "documento": "Damodaran (NYU Stern), «Margins by industry» (margin.xls), hoja «Industry Averages», empresas de EE. UU., «Date updated» 2026-01-05",
    "version": (f"XLS damodaran_margin.xls subido por la persona responsable a la Release fuentes-examen-20261118 (asset {dx['asset']}), descarga cruda conservada byte a byte en "
                f"{dx['archivo']}, sha256 {dx['sha256']} (la huella publicada, anexo 3); hoja «Industry Averages» conservada como texto con marca [PDF PAGE 1], una línea por fila "
                f"(«fila n: celda | celda …», xlrd 2.0.1), sha256 {dt_['sha256']}"),
    "conservacion": "local", "archivo": dt_["archivo"], "sha256": dt_["sha256"], "pagina": 1, "folio": None,
    "ubicacion": f"hoja «Industry Averages», fila {dt_['fila']} (columna A «Industry Name»)", "concepto": "sector de Damodaran asignado a Zoetis",
    "columna": f"Industry Name (columna A), fila {dt_['fila']} de la hoja", "periodo": "clasificación de los datos de enero de 2026 («Date updated» 2026-01-05)",
    "unidad": "texto", "escala": 1, "signo": 1,
    "tratamiento": "etiqueta de industria tal como figura en la tabla (228 empresas en esa fila, las mismas que la fila de mgnroc.html del extracto anterior); Zoetis es una emisora de EE. UU. y la tabla es de empresas de EE. UU.",
    "perimetro": "no aplica: clasificación sectorial externa", "perimetro_justificacion": "la clasificación sectorial es un dato externo al perímetro contable del grupo",
    "reexpresado": "no aplica", "valor_fuente": "Drugs (Pharmaceutical)", "cita": f"fila {dt_['fila']}: Drugs (Pharmaceutical) | 228"}
pendiente(e, "lectura externa → fuente local: tabla de Damodaran de la Release (asset 766892761); resultados/fuentes_mercado_zoetis_t1d.json")
# 9) C37 y C38: anotaciones (no se corrigen; la comprobación del revisor no se toca)
tp = FM["Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.txt"]; pg = FM["Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.png"]
e = E["Análisis!C37"]
e["fuente"].update({
    "documento": "Página oficial de la empresa (Zoetis Investor Relations), «Stock Information» → «Historical Stock Quote», Lookup Date 2026 Oct 8",
    "version": (f"captura de pantalla de https://investor.zoetis.com/stock-information/default.aspx#stock-historical entregada por la persona responsable el 19-nov-2026 "
                f"(RELEASE_FUENTES_EXAMEN_VERIFICACION.md, anexo 3 ter), conservada byte a byte en {pg['archivo']}, sha256 {pg['sha256']}; transcripción con marca [PDF PAGE 1] "
                f"hecha por Claude orquestación leyendo la imagen, sha256 {tp['sha256']} (el revisor la contrasta con la imagen). Sustituye la transcripción de la tabla "
                "hecha por el extractor (Zoetis_IR_XNYS_ZTS_historico_acciones_20261118.txt, que se conserva)"),
    "archivo": tp["archivo"], "sha256": tp["sha256"], "pagina": 1, "folio": None,
    "ubicacion": "cuadro «Historical Stock Quote» con Lookup Date 2026 Oct 8 (Day's Open $71.36, Intraday Low $71.15, Intraday High $73.75, Volume 6,176,469)",
    "columna": "Closing Price (Lookup Date 2026 Oct 8)", "cita": "Closing Price $73.08", "valor_fuente": 73.08})
pendiente(e, "C37 con la captura de investor.zoetis.com del 8-oct-2026 (anexo 3 ter), conservada con su huella, en vez de la transcripción del extractor; resultados/fuentes_mercado_zoetis_t1d.json")
E["Análisis!C38"]["incidencia"] = ("(zoetis_t1d, 19-nov-2026) En el libro, Control maestro F de C38 = «Dato no verificable» (copia de ensayo, cambio_zoetis_t1d.json): "
                                   "tercero sin bytes; solo contexto.")
cambios.append({"celda": "Análisis!C38", "solo": "incidencia", "despues": E["Análisis!C38"]["incidencia"]})
# fuentes de mercado y nota
for a in RM["archivos"]:
    d["fuentes_mercado"]["contenido"][os.path.basename(a["archivo"])] = {"que": a["que"] + (f"; {a['fila_usada']}" if a.get("fila_usada") else "") + " (zoetis_t1d; Release fuentes-examen-20261118, anexo 3)", "sha256": a["sha256"]}
d["nota_del_extractor_complementario"] = str(d.get("nota_del_extractor_complementario") or "") + (
    f" (zoetis_t1d, {HOY}) Registro conservado de zoetis_t1c tras su sellado (REVISION_SELLADO.md, 4743cb0); Claude orquestación corrigió o añadió {len(cambios)} entradas "
    "(resultados/registro_cambios_zoetis_t1d.json): quedan pendientes de otro revisor.")
json.dump(d, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": HOY, "guion": "resultados/scripts/corregir_registro_zoetis_t1d.py", "registro_antes_sha256": h(cons), "registro_despues_sha256": h(p),
           "entradas_corregidas": [x["celda"] for x in cambios], "cambios": cambios}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("corregidas o anotadas", len(cambios), [x["celda"] for x in cambios])
