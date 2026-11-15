"""Cuarta pasada · T1/T2 sobre los derivados de los tres registros REALES de la 4.14 (solo lectura; sin vínculo ni estado de los orígenes:
solo las reglas de la fórmula). Para cada derivado se compara:
  - la regla de la tercera pasada: evaluación con floats y «exacto» = |r − modelo| ≤ 1e-9 × el mayor origen (o _igual_exacto);
  - la regla vigente: VE._eval_formula_exacta (fractions) y _igual_libro (si derivacion.unidad es monetaria) o _igual_exacto;
y se aplican los controles nuevos de T2/T3 (constantes no admitidas, clase de los orígenes, orígenes que no influyen)."""
import ast, fractions, json, os, sys

PV = os.environ.get("PV", "/tmp/rev_fable4/congelado4/personaje_v2")
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import verificacion_entradas as VE  # noqa: E402

print("árbol:", PV)
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
tot = dif = 0
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    reg = json.load(open(os.path.join(E414, exp, "verificacion_entradas.json"), encoding="utf-8"))
    por = {e["celda"]: e for e in reg["entradas"]}
    n = ok3 = ok4 = 0
    ctes, inertes, clases, forma = [], [], [], []
    for e in reg["entradas"]:
        d = e.get("derivacion") or {}
        if e.get("clase") != "derivado":
            continue
        n += 1
        vals = {o: por[o]["valor_modelo"] for o in d["origenes"]}
        vm = e["valor_modelo"]
        # regla de la tercera pasada
        r3 = VE._eval_formula(d["formula"], vals)
        esc_o = max([abs(x) for x in vals.values()] + [abs(r3), abs(vm), 1e-300])
        a3 = abs(r3 - vm) <= 1e-9 * esc_o or VE._igual_exacto(r3, vm)
        # regla vigente
        r4 = float(VE._eval_formula_exacta(d["formula"], vals))
        importe = VE.UNIDADES.get(VE._norm_txt(d.get("unidad"))) is not None
        a4 = VE._igual_libro(r4, vm) if importe else VE._igual_exacto(r4, vm)
        ok3 += a3; ok4 += a4
        if a3 != a4:
            dif += 1
            print(f"   DISTINTO {exp} {e['celda']}: tercera pasada {'acepta' if a3 else 'rechaza'} ({r3!r}) · vigente {'acepta' if a4 else 'rechaza'} ({r4!r}) · modelo {vm!r} · {d['formula'][:70]}")
        if not isinstance(d["origenes"], list) or not all(isinstance(o, str) and o for o in d["origenes"]) or not isinstance(d["formula"], str):
            forma.append(e["celda"])
        if VE._constantes_no_admitidas(d["formula"]):
            ctes.append((e["celda"], VE._constantes_no_admitidas(d["formula"])))
        for o in d["origenes"]:
            if por[o].get("clase") not in ("dato_publicado", "cero_comprobado", "derivado", "hipotesis", "convencion"):
                clases.append((e["celda"], o, por[o].get("clase")))
        base = VE._eval_formula_exacta(d["formula"], vals, sin_redondeo=True)
        for o in d["origenes"]:
            v_o = VE._frac(vals[o])
            pert = dict(vals, **{o: v_o * (1 + fractions.Fraction(1, 10 ** 7)) + fractions.Fraction(1, 10 ** 7)})
            if VE._eval_formula_exacta(d["formula"], pert, sin_redondeo=True) == base:
                inertes.append((e["celda"], o, vals[o]))
    tot += n
    ceros = sum(1 for e in reg["entradas"] if e.get("clase") == "derivado" for o in e["derivacion"]["origenes"] if por[o]["valor_modelo"] == 0)
    menos1 = sum(1 for e in reg["entradas"] if e.get("clase") == "derivado" for o in e["derivacion"]["origenes"] if por[o]["valor_modelo"] == -1)
    print(f"{exp}: {n} derivados · aceptados por la fórmula con la regla de la tercera pasada: {ok3} · con la vigente: {ok4}")
    print(f"      controles nuevos → «origenes»/«formula» mal formados: {forma} · constantes no admitidas: {ctes} · orígenes de clase no admitida: {clases} · orígenes que no influyen: {inertes}")
    print(f"      orígenes con valor 0 usados en derivados: {ceros} · con valor −1: {menos1}")
print(f"total {tot} derivados reales · decisiones distintas entre las dos reglas: {dif}")

print("\n¿Pasarán los registros regenerados? Tasas de la fila 10 con round(…, 4) declarado y medias del FCF base con derivacion.unidad = «mm»;")
print("fuentes y escalas de los datos publicados y ceros comprobados (para T2-escala y T4):")
import collections, re  # noqa: E402
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    reg = json.load(open(os.path.join(E414, exp, "verificacion_entradas.json"), encoding="utf-8"))
    por = {e["celda"]: e for e in reg["entradas"]}
    ok10 = n10 = okf = nf = 0
    ext, esc, ctes = collections.Counter(), collections.Counter(), collections.Counter()
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        if e.get("clase") in ("dato_publicado", "cero_comprobado"):
            ext[(os.path.splitext(str(f.get("archivo") or ""))[1].lower() or "(sin extensión)", "con archivo_texto" if f.get("archivo_texto") else "sin archivo_texto")] += 1
            mon = VE.UNIDADES.get(VE._norm_txt(f.get("unidad"))) is not None
            esc[("unidad monetaria reconocida" if mon else "otra unidad", repr(f.get("escala")))] += 1
        if e.get("clase") != "derivado":
            continue
        d = e["derivacion"]; vals = {o: por[o]["valor_modelo"] for o in d["origenes"]}; vm = e["valor_modelo"]
        for n_ in ast.walk(ast.parse(d["formula"], mode="eval")):
            if isinstance(n_, ast.Constant) and isinstance(n_.value, (int, float)):
                ctes[n_.value] += 1
        if re.match(r"Historia![C-L]10$", e["celda"]):
            n10 += 1; ok10 += VE._igual_exacto(float(VE._eval_formula_exacta(f"round({d['formula']}, 4)", vals)), vm)
        elif re.match(r"Análisis!C(4[6-9]|50)$", e["celda"]):
            nf += 1; okf += VE._igual_libro(float(VE._eval_formula_exacta(d["formula"], vals)), vm)
    print(f"{exp}: fila 10 con round(…, 4): {ok10}/{n10} · medias del FCF base con unidad «mm»: {okf}/{nf} · constantes de las fórmulas: {dict(ctes)}")
    print(f"      fuentes: {dict(ext)} · escalas: {dict(esc)}")
