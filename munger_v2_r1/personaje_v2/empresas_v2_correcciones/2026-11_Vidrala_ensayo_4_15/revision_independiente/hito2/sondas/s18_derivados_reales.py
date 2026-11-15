#!/usr/bin/env python3
"""s18 · Los derivados de los registros reales de la 4.14 (solo lectura) con las reglas de fórmulas del hito 2: funciones que usan,
longitud y nodos, constantes no admitidas, orígenes inertes, constante local, y resultado con _importe_libro_exacto frente a la regla del
hito 1 (_igual_libro), a partir de los valores registrados de sus orígenes (valor_modelo del registro; no se comprueba la vigencia)."""
import ast, collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
tot = collections.Counter()
for exp in ["elis_decisiones/Elis", "vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan"]:
    reg, _ = VE.cargar(os.path.join(E414, exp))
    por = {e["celda"]: e for e in reg["entradas"]}
    c = collections.Counter()
    ej = []
    for e in reg["entradas"]:
        if e.get("clase") != "derivado":
            continue
        d = e.get("derivacion") or {}
        f = d.get("formula")
        c["derivados"] += 1
        if not isinstance(f, str):
            c["sin fórmula de texto"] += 1
            continue
        for fn in re.findall(r"\b(abs|min|max|sum|round)\(", f):
            c[f"usa {fn}"] += 1
        c["más de 2000 caracteres"] += len(f) > 2000
        c["más de 400 nodos"] += sum(1 for _ in ast.walk(ast.parse(f, mode="eval"))) > 400
        try:
            ctes = VE._constantes_no_admitidas(f)
        except Exception as ex:  # noqa: BLE001
            c[f"fórmula rechazada ({type(ex).__name__})"] += 1
            ej.append((e["celda"], f[:100], str(ex)[:80]))
            continue
        c["con constantes no admitidas"] += bool(ctes)
        vals = {o: por[o].get("valor_modelo") for o in d.get("origenes") or [] if o in por}
        if len(vals) != len(d.get("origenes") or []) or not all(VE._num(v) for v in vals.values()):
            c["orígenes sin valor numérico en el registro"] += 1
            continue
        try:
            ine, loc = VE._sensibilidad(f, vals, list(d["origenes"]))
            r_ex = VE._eval_formula_exacta(f, vals)
        except Exception as ex:  # noqa: BLE001
            c[f"no evaluable ({type(ex).__name__})"] += 1
            ej.append((e["celda"], f[:100], str(ex)[:80]))
            continue
        c["con orígenes inertes"] += bool(ine)
        c["constante en el punto real"] += not loc
        if ine or not loc:
            ej.append((e["celda"], f[:110], ine, sorted(loc)))
        vm = e.get("valor_modelo")
        importe = VE.UNIDADES.get(VE._norm_txt(d.get("unidad"))) is not None
        h2 = VE._importe_libro_exacto(r_ex, vm) if importe else VE._igual_exacto(float(r_ex), vm)
        h1 = VE._igual_libro(float(r_ex), vm) if importe else VE._igual_exacto(float(r_ex), vm)
        c[f"valor: hito 1 {'reproduce' if h1 else 'no reproduce'} · hito 2 {'reproduce' if h2 else 'no reproduce'}{' · importe' if importe else ''}"] += 1
    print(f"\n=== {exp}")
    for k, v in sorted(c.items()):
        if v:
            print(f"   {v:4d}  {k}")
    for x in ej[:6]:
        print("      ", x)
    tot.update(c)
print("\n=== total:", {k: v for k, v in sorted(tot.items()) if v and (k.startswith(("derivados", "usa", "con ", "constante", "más", "fórmula")))})
