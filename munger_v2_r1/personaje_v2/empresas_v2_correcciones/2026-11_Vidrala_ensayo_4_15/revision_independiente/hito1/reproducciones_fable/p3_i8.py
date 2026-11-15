"""I8: cifras que datos_v63.md da a las fases de juicio y que no están en el universo de verificación (libros finales de la 4.14; solo lectura)."""
import json, os, re, sys
PV = os.environ.get("PV", "/tmp/rev_fable/trabajo_copia/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE, entradas_economicas as EE, volcar_datos_v63 as VD
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    c = os.path.join(E414, exp); lb = VE.libro_de(c); inst = VE.universo(c); lec = EE._Lector(lb); ee = EE.instantanea(lb)
    print(f"===== {exp} · universo {inst['n']} = cálculo {inst['n_calculo']} + juicio {inst['n_juicio']} · huella de cálculo == EE.instantanea: {inst['huella'] == ee['huella']} · n_calculo == EE.n: {inst['n_calculo'] == ee['n']}")
    def est(h, r):
        k = f"{h}!{r}"; v = EE._norm(lec.leer(h, r)); f = VE._es_formula(v) or lec.lb.tiene_formula(h, r)
        return k, ("FÓRMULA" if f else v), (k in inst["celdas"])
    fuera = [est("Análisis", r) for r in VD.DATOS_ANALISIS + ["C59"]]
    print("  Análisis (DATOS_ANALISIS de volcar_datos_v63 + C59) fuera del universo:", [(k, v) for k, v, d in fuera if not d])
    pal = [est("Palancas", r) for r in ["C5", "C7", "C9", "C10", "C45", "C46"] + [f"{c_}{i}" for i in range(28, 34) for c_ in "AB"]]
    print("  Palancas con dato (no fórmula) fuera del universo:", [(k, v) for k, v, d in pal if not d and v not in (None, "", "FÓRMULA")])
    md = open(os.path.join(c, "datos_v63.md"), encoding="utf-8").read()
    for pat in (r"- Reparto geográfico.*", r"- Tasa sin riesgo.*"):
        m = re.search(pat, md); print("  datos_v63.md:", m.group(0).strip()[:330] if m else "(no está)")
