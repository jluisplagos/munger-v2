#!/usr/bin/env python3
"""Control 4.12 con las palancas de la 4.11 (encargo 4.12 §7): antes del cierre nuevo de Vidrala, se comprueba que el código final,
con las MISMAS entradas (cambio de base de la 4.11) y las MISMAS palancas (salidas de los agentes del piloto 4.11: extracto, fases A
y B, copiadas sin cambios cuando el pipeline las pide), da la misma valoración que el piloto: V, probabilidades, ponderado, precio de
Sí, zona y las trece variantes de la configuración. No hay fase C nueva ni auditoría: el pipeline se detiene cuando pide la fase C.

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/scripts/control_palancas_4_11.py
Escribe control_palancas_4_11/resultados/control_palancas.json y .md. Código 0 si todo coincide (tolerancia 1e-9 €).
"""
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
PV = os.path.abspath(os.path.join(EXP, "..", ".."))
RAIZ = os.path.dirname(PV)
CONF = os.path.join(EXP, "configuracion", "cambio_de_base_control_palancas_4_11.json")
ENS = os.path.join(EXP, "control_palancas_4_11")
DEST = os.path.join(ENS, "Vidrala")
PIL = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "piloto", "Vidrala")
CFG = os.path.join(PV, "config_v2_v64_experimental.json")
PIPE = os.path.join(PV, "scripts", "pipeline.py")
ARCHIVOS = {"extraccion_v63": ["extracto_v63.md"], "fase_a": ["fase_a.json", "fase_a.md"], "fase_b": ["fase_b.json", "fase_b.md"]}
sys.path.insert(0, os.path.join(PV, "scripts"))


def correr():
    salidas = []
    for _ in range(25):
        r = subprocess.run([sys.executable, PIPE, DEST, "--config", CFG], capture_output=True, text=True)
        salidas.append(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr[-200:])
        if r.returncode != 10:
            return r.returncode, salidas
        nombre = open(os.path.join(DEST, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1]
        if nombre == "fase_c_turno1":
            return 0, salidas + ["el pipeline pide la fase C: valoración y variantes hechas; el control termina aquí"]
        if nombre not in ARCHIVOS:
            return 99, salidas + [f"agente no previsto: {nombre}"]
        for f in ARCHIVOS[nombre]:
            shutil.copy(os.path.join(PIL, f), os.path.join(DEST, f))
            os.utime(os.path.join(DEST, f), None)
        salidas.append(f"agente simulado {nombre}: {', '.join(ARCHIVOS[nombre])} del piloto 4.11, sin cambios")
    return 98, salidas + ["demasiadas vueltas"]


def main():
    import entradas_economicas as EE
    if not os.path.exists(DEST):
        r = subprocess.run([sys.executable, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "preparar", CONF], cwd=RAIZ, capture_output=True, text=True)
        print((r.stdout + r.stderr).strip().splitlines()[-1] if (r.stdout + r.stderr).strip() else "")
        if r.returncode != 0:
            return 1
    rc, salidas = correr()
    j = lambda d, n: json.load(open(os.path.join(d, n), encoding="utf-8"))  # noqa: E731
    out = {"pipeline_rc": rc, "salidas": salidas}
    os.makedirs(os.path.join(ENS, "resultados"), exist_ok=True)
    if rc != 0:
        json.dump(out, open(os.path.join(ENS, "resultados", "control_palancas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("\n".join(salidas))
        return 1
    p_c, p_p = j(DEST, "precio.json"), j(PIL, "precio.json")
    v_c, v_p = j(DEST, "configuracion_v64_variantes.json"), j(PIL, "configuracion_v64_variantes.json")
    d = {"V": max(abs(a - b) for a, b in zip(p_c["V"], p_p["V"])), "ponderado": abs(p_c["ponderado"] - p_p["ponderado"]),
         "precio_si": abs(p_c["precio_si"] - p_p["precio_si"]), "probabilidades": p_c.get("p") == p_p.get("p"), "zona": p_c["zona"] == p_p["zona"]}
    vc = {x["clave"]: x for x in v_c["variantes"]}
    vp = {x["clave"]: x for x in v_p["variantes"]}
    var = []
    for k in vp:
        a, b = vc.get(k) or {}, vp[k]
        var.append({"clave": k, "ponderado_control": a.get("ponderado"), "ponderado_piloto": b.get("ponderado"),
                    "precio_si_control": a.get("precio_si"), "precio_si_piloto": b.get("precio_si"), "zona_control": a.get("zona"), "zona_piloto": b.get("zona"),
                    "igual": bool(a) and abs((a.get("ponderado") or 0) - (b.get("ponderado") or 0)) <= 1e-9 and abs((a.get("precio_si") or 0) - (b.get("precio_si") or 0)) <= 1e-9 and a.get("zona") == b.get("zona")})
    i_c = EE.instantanea(os.path.join(DEST, "Vidrala_v63_evaluada.xlsx"))
    i_p = EE.instantanea(os.path.join(PIL, "Vidrala_v63_evaluada.xlsx"))
    dif = EE.diferencias(i_p, i_c)
    ok = d["V"] <= 1e-9 and d["ponderado"] <= 1e-9 and d["precio_si"] <= 1e-9 and d["probabilidades"] and d["zona"] and all(x["igual"] for x in var) and set(vc) == set(vp) and not dif
    out.update({"diferencias_valoracion": d, "variantes": var, "mismas_variantes": set(vc) == set(vp),
                "entradas_economicas": {"huella_control": i_c["huella"], "huella_piloto": i_p["huella"], "n": i_c["n"], "celdas_distintas": dif},
                "resultado": "CONCUERDA" if ok else "NO CONCUERDA",
                "nota": "control con las palancas de la 4.11 y el código final; las fases A y B son las del piloto 4.11 (agentes reales de la 4.11), copiadas sin cambios"})
    json.dump(out, open(os.path.join(ENS, "resultados", "control_palancas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Control 4.12 con las palancas de la 4.11", "", f"**Resultado: {out['resultado']}**.", "",
          f"- Precio de Sí {p_c['precio_si']} (piloto {p_p['precio_si']}) · ponderado {p_c['ponderado']} (piloto {p_p['ponderado']}) · zona {p_c['zona']} (piloto {p_p['zona']}).",
          f"- |Δ| máxima: V {d['V']} · ponderado {d['ponderado']} · precio de Sí {d['precio_si']}; probabilidades iguales: {d['probabilidades']}.",
          f"- Entradas económicas del libro evaluado: {i_c['n']} celdas; huella del control `{i_c['huella'][:16]}…`, del piloto `{i_p['huella'][:16]}…`; celdas distintas: {dif or 'ninguna'}.", "",
          "| Variante | Ponderado control | Ponderado piloto | Precio de Sí control | Precio de Sí piloto | Zona | Igual |", "|---|---|---|---|---|---|---|"]
    md += [f"| {x['clave']} | {x['ponderado_control']} | {x['ponderado_piloto']} | {x['precio_si_control']} | {x['precio_si_piloto']} | {x['zona_control']} | {'sí' if x['igual'] else 'NO'} |" for x in var]
    md += ["", "Recorrido del pipeline:", ""] + [f"- {s}" for s in salidas]
    open(os.path.join(ENS, "resultados", "control_palancas.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{out['resultado']}: precio de Sí {p_c['precio_si']} · ponderado {p_c['ponderado']} · {len(var)} variantes · celdas económicas distintas {len(dif)}")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
