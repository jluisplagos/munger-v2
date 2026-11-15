"""I8 / hallazgo 6: universo de juicio en los libros finales de la 4.14 (árbol CONGELADO; solo lectura)."""
import json, os, re, sys
PV = os.environ.get("PV", "/tmp/rev_fable2/congelado/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE, entradas_economicas as EE, volcar_datos_v63 as VD, leer_v63 as L
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
print("DATOS_JUICIO_PALANCAS:", VE.DATOS_JUICIO_PALANCAS, "| FILAS_GEOGRAFIA:", list(VE.FILAS_GEOGRAFIA))
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    c = os.path.join(E414, exp); lb = VE.libro_de(c); inst = VE.universo(c); lec = EE._Lector(lb); ee = EE.instantanea(lb)
    print(f"===== {exp} · universo {inst['n']} = cálculo {inst['n_calculo']} + juicio {inst['n_juicio']} · huella de cálculo == EE.instantanea: {inst['huella'] == ee['huella']} · n_calculo == EE.n: {inst['n_calculo'] == ee['n']}")
    def est(h, r):
        k = f"{h}!{r}"; v = EE._norm(lec.leer(h, r)); f = VE._es_formula(v) or lec.lb.tiene_formula(h, r)
        return k, ("FÓRMULA" if f else v), (k in inst["celdas"]), inst["ambito"].get(k)
    fuera = [est("Análisis", r) for r in VD.DATOS_ANALISIS + ["C59"]]
    print("  Análisis (DATOS_ANALISIS + C59) fuera del universo:", [(k, v) for k, v, d, a in fuera if not d])
    pal = [est("Palancas", r) for r in ["C5", "C6", "C7", "C8", "C9", "C10", "C45", "C46", "C47", "C48"] + [f"{c_}{i}" for i in range(28, 35) for c_ in "ABC"]]
    print("  Palancas dentro (ámbito):", [(k.split('!')[1], v if not isinstance(v, str) else v[:22], a) for k, v, d, a in pal if d])
    print("  Palancas con dato (no fórmula) FUERA del universo:", [(k.split('!')[1], v) for k, v, d, a in pal if not d and v not in (None, "", "FÓRMULA")])
    cmc = [est("Control maestro", r) for r in ["H4", "J4", "L4", "D5"]]
    print("  Control maestro (cabecera que se da al juicio):", [(k.split('!')[1], v, "dentro" if d else "FUERA") for k, v, d, a in cmc])
    reg = json.load(open(os.path.join(c, VE.REGISTRO), encoding="utf-8"))
    con_ent = {e["celda"] for e in reg["entradas"]}
    juicio = [k for k, a in inst["ambito"].items() if a == "juicio"]
    print(f"  celdas de juicio: {len(juicio)} · sin entrada en el registro de la 4.14: {len([k for k in juicio if k not in con_ent])} · de ellas Palancas: {sorted(k for k in juicio if k.startswith('Palancas!') and k not in con_ent)}")
    md = open(os.path.join(c, "datos_v63.md"), encoding="utf-8").read()
    for pat in (r"- Reparto geográfico.*", r"- Sector de Damodaran.*"):
        m = re.search(pat, md); print("  datos_v63.md:", m.group(0).strip()[:300] if m else "(no está)")
# geografía con 6 filas / fila 33 / fórmulas: comprobación de la regla «filas con dato»
print("\nFilas de la Historia de juicio = leer_v63.FILAS_HISTORIA sin el año:", set(VE.FILAS_HISTORIA_JUICIO) == set(L.FILAS_HISTORIA) - {5})
print("DATOS_JUICIO_ANALISIS ⊆ DATOS_ANALISIS:", set(VE.DATOS_JUICIO_ANALISIS) <= set(VD.DATOS_ANALISIS), "| DATOS_ANALISIS − DATOS_JUICIO_ANALISIS:", sorted(set(VD.DATOS_ANALISIS) - set(VE.DATOS_JUICIO_ANALISIS)))
