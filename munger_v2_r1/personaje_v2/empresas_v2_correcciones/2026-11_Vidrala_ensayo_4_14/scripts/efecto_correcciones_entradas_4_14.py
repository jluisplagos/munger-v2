#!/usr/bin/env python3
"""Efecto MECÁNICO de las correcciones de entradas de la rama 4.14 sobre el libro evaluado 4.13 congelado (encargo de cierre §6–§7:
efectos homogéneos, sin compensarlos cambiando otras palancas; requisito de verificación de las entradas).

Qué hace (en COPIAS; el libro 4.13 no se toca; LibreOffice en secuencia):
  1. Reproduce el caso activo (precio de Sí de precio.json del expediente 4.13).
  2. Las celdas de entradas económicas que cambian entre el libro de DATOS 4.13 y el de la rama 4.14 (instantánea de
     entradas_economicas: solo las corregidas en la extracción) se escriben en la copia del libro EVALUADO 4.13, con las fases A, B y C
     de la 4.13 fijas: por grupo (fila de la Historia o celda de Análisis) y todas juntas.
  3. Las opciones de las decisiones pendientes (D3/E5, E1–E4), cada una por separado sobre el caso activo y sobre «todas las
     correcciones». Ninguna se adopta.
No es la valoración de la rama (que rehace las fases con agentes reales): es el efecto de los datos con todo lo demás fijo.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_14/scripts/efecto_correcciones_entradas_4_14.py [viscofan|vidrala]
Escribe resultados/efecto_correcciones_<empresa>.json y .md en la carpeta del ensayo 4.14.
"""
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
E414 = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(E414, "..", ".."))
SCR = os.path.join(PV, "scripts")
E413 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_13")
sys.path.insert(0, SCR)

EMPRESAS = {
    "viscofan": {"control": os.path.join(E413, "viscofan", "Viscofan"), "rama": os.path.join(E414, "viscofan", "Viscofan"), "E": "Viscofan",
                 "decisiones": [("D3/E5 · acciones en circulación a 31-dic-2025 (E fijo)", {"Análisis!C55": 45.993399}),
                                ("E1 · medias exactas C47–C50 (sin el redondeo del inversor)", {"Análisis!C47": 77.533, "Análisis!C48": 8.294, "Análisis!C49": 5.547, "Análisis!C50": 3.707})]},
    "vidrala": {"control": os.path.join(E413, "vidrala_condicionado", "Vidrala"), "rama": os.path.join(E414, "vidrala", "Vidrala"), "E": "Vidrala",
                "decisiones": [("E1 · medias exactas C46 y C47", {"Análisis!C46": 335.413, "Análisis!C47": 169.668}),
                               ("E2 · K14 sin la plusvalía de Italia (≈34,447)", {"Historia!K14": 34.447}),
                               ("E2 · K14 alternativa (≈33,594)", {"Historia!K14": 33.594}),
                               ("E3 · pareja B de 2023 (J8 97,865; J14 89,866)", {"Historia!J8": 97.865, "Historia!J14": 89.866}),
                               ("E4 · intereses en financiación C48 = 2,254", {"Análisis!C48": 2.254})]},
}


def num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def iguales(a, b):
    if num(a) and num(b):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a), abs(b))
    return a == b


def recalcular(libro_ev, celdas, nombre, tmp, perfil):
    from v63_xml import LibroV63
    lb = LibroV63(libro_ev)
    hojas = {}
    for k in celdas:
        h, c = k.split("!")
        hojas.setdefault(h, set()).add(c)
    if celdas:
        lb.escribir_celdas(celdas, hojas)
    lb.borrar_caches()
    copia = os.path.join(tmp, f"{nombre}.xlsx")
    lb.guardar(copia)
    r = subprocess.run(["bash", os.path.join(SCR, "recalc.sh"), copia, os.path.join(tmp, "recalc"), perfil], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"recálculo {nombre}: {(r.stdout + r.stderr)[-300:]}")
    rec = os.path.join(tmp, "recalc", f"{nombre}.xlsx")
    rj, pj = os.path.join(tmp, f"{nombre}.resultados.json"), os.path.join(tmp, f"{nombre}.precio.json")
    r = subprocess.run([sys.executable, os.path.join(SCR, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"], capture_output=True, text=True)
    if r.returncode != 0:
        raise RuntimeError(f"lectura {nombre}: {(r.stdout + r.stderr)[-300:]}")
    subprocess.run([sys.executable, os.path.join(SCR, "precio_de_si.py"), rj, pj, "--copia", "--k", "3"], capture_output=True, text=True)
    res, pr = json.load(open(rj, encoding="utf-8")), json.load(open(pj, encoding="utf-8"))
    return {"precio_si": pr.get("precio_si"), "zona": pr.get("zona"), "ponderado": res["valores"].get("C83"),
            "valida_v64": (res.get("configuracion_v64") or {}).get("valida")}


def main():
    import entradas_economicas as EE
    clave = (sys.argv[1] if len(sys.argv) > 1 else "viscofan").lower()
    emp = EMPRESAS[clave]
    E = emp["E"]
    libro_ev = os.path.join(emp["control"], f"{E}_v63_evaluada.xlsx")
    d413 = EE.instantanea(os.path.join(emp["control"], f"{E}_v63_datos.xlsx"))["celdas"]
    d414 = EE.instantanea(os.path.join(emp["rama"], f"{E}_v63_datos.xlsx"))["celdas"]
    ev = EE.instantanea(libro_ev)["celdas"]
    cambios = {k: d414.get(k) for k in sorted(set(d413) | set(d414)) if not iguales(d413.get(k), d414.get(k))}
    # solo las celdas que el libro evaluado conserva del libro de datos (si una fase las sobrescribió, no se tocan y se dice)
    tocadas_por_fases = sorted(k for k in cambios if not iguales(ev.get(k), d413.get(k)))
    aplicables = {k: v for k, v in cambios.items() if k not in tocadas_por_fases}
    grupos = {}
    for k in aplicables:
        m = re.match(r"^Historia!([A-Z]+)(\d+)$", k)
        grupos.setdefault(f"Historia fila {m.group(2)}" if m else k, {})[k] = aplicables[k]
    pr0 = json.load(open(os.path.join(emp["control"], "precio.json"), encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix=f"efecto_{clave}_")
    perfil = os.path.join(tmp, ".lo_perfil")
    os.makedirs(os.path.join(tmp, "recalc"))
    filas = []
    try:
        base = recalcular(libro_ev, {}, "activa", tmp, perfil)
        filas.append({"caso": "activa 4.13 (reproducción)", "celdas": {}, **base})
        for i, (g, cs) in enumerate(sorted(grupos.items())):
            filas.append({"caso": f"corrección · {g}", "celdas": {k: [d413.get(k), v] for k, v in cs.items()}, **recalcular(libro_ev, cs, f"g{i}", tmp, perfil)})
        todas = recalcular(libro_ev, aplicables, "todas", tmp, perfil)
        filas.append({"caso": "TODAS las correcciones de la rama", "celdas": {k: [d413.get(k), v] for k, v in aplicables.items()}, **todas})
        for j, (nombre, cs) in enumerate(emp["decisiones"]):
            filas.append({"caso": f"decisión (no adoptada) · {nombre} · sobre la activa", "celdas": {k: [ev.get(k), v] for k, v in cs.items()}, **recalcular(libro_ev, cs, f"d{j}a", tmp, perfil)})
            filas.append({"caso": f"decisión (no adoptada) · {nombre} · con todas las correcciones", "celdas": {k: [ev.get(k), v] for k, v in cs.items()},
                          **recalcular(libro_ev, dict(aplicables, **cs), f"d{j}b", tmp, perfil)})
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    ok = abs((base["precio_si"] or 0) - pr0["precio_si"]) <= 1e-9
    p0 = base["precio_si"]
    p_todas = next((f["precio_si"] for f in filas if f["caso"].startswith("TODAS")), None)
    for f in filas:
        f["delta_precio_si"] = (f["precio_si"] - p0) if num(f.get("precio_si")) and num(p0) else None
        # (14-nov, dos errores de lectura: E5 y E2/E3) una opción «con todas las correcciones» se compara también con la rama
        f["delta_frente_a_la_rama"] = (f["precio_si"] - p_todas) if "con todas las correcciones" in f["caso"] and num(p_todas) else None
    out = {"empresa": E, "libro_evaluado_4_13": os.path.relpath(libro_ev, PV), "reproduce_el_caso_activo": ok, "precio_si_activo": pr0["precio_si"],
           "naturaleza": "efecto mecánico con las fases A, B y C de la 4.13 fijas; no es la valoración de la rama; las decisiones no se adoptan",
           "celdas_cambiadas": {k: [d413.get(k), v] for k, v in cambios.items()}, "celdas_que_las_fases_sobrescriben": tocadas_por_fases, "casos": filas}
    res = os.path.join(E414, "resultados")
    os.makedirs(res, exist_ok=True)
    json.dump(out, open(os.path.join(res, f"efecto_correcciones_{clave}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    g = lambda x, d=5: (f"{x:+.{d}f}" if d == 5 and x is not None and False else f"{x:.{d}f}").replace(".", ",") if num(x) else "—"  # noqa: E731
    md = [f"# {E} · efecto mecánico de las correcciones de entradas (rama 4.14)", "",
          "**Qué es.** Copias del libro evaluado 4.13 congelado con las fases A, B y C fijas, en las que se escriben los datos corregidos en la rama (por grupo y todos juntos) y, aparte, las opciones de las decisiones pendientes; recalculadas con LibreOffice. Mide el efecto de los DATOS con todo lo demás fijo. **No es la valoración de la rama** (que rehace las fases con agentes reales) y **ninguna decisión se adopta**.", "",
          f"**Reproducción del caso activo:** {'sí' if ok else 'NO'} (precio de Sí {g(p0)} frente a {g(pr0['precio_si'])} de precio.json).", "",
          f"**Celdas de entradas que cambian en la rama:** {len(cambios)}" + (f"; {len(tocadas_por_fases)} las sobrescriben las fases en el libro evaluado y no se tocan: {', '.join(tocadas_por_fases)}" if tocadas_por_fases else "") + ".", "",
          "| Caso | Celdas (antes → después) | Precio de Sí | Δ frente a la activa 4.13 | Δ frente a la rama (todas las correcciones) | Ponderado | Zona |", "|---|---|---|---|---|---|---|"]
    for f in filas:
        cel = "; ".join(f"{k.replace('Historia!', 'H!').replace('Análisis!', 'A!')} {g(a, 3)} → {g(b, 3)}" for k, (a, b) in f["celdas"].items()) or "—"
        md.append(f"| {f['caso']} | {cel if len(cel) < 400 else cel[:400] + '…'} | {g(f['precio_si'])} | {g(f['delta_precio_si'])} | {g(f.get('delta_frente_a_la_rama'))} | {g(f['ponderado'], 3)} | {f['zona']} |")
    open(os.path.join(res, f"efecto_correcciones_{clave}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md[4:]))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
