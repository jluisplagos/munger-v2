"""I13 sobre datos reales (copias en /tmp): los registros de la 4.14, revisados el 14-nov-2026, se sellan con `sellar` y fecha retroactiva, sin revisión nueva."""
import collections, json, os, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable/trabajo_copia/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    src = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", exp)
    tmp = tempfile.mkdtemp(prefix="rev_fable_sellar_real_"); d = os.path.join(tmp, os.path.basename(src))
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("recalc", "variantes_v64", "prompts_generados", ".lo_perfil", "historial_cierres", "antecedentes", "fuentes_pdf"))
    reg = json.load(open(os.path.join(d, VE.REGISTRO), encoding="utf-8"))
    r0 = VE.comprobar(d)
    print(f"== {exp} · registro formato {reg['formato']} · {len(reg['entradas'])} entradas · antes: comprobadas {r0['comprobadas_universo']} de {r0['universo']} (cálculo {r0['comprobadas_calculo']} de {r0['universo_calculo']})")
    grupos = collections.defaultdict(list)
    for e in reg["entradas"]:
        c = e.get("comprobacion") or {}
        grupos[(c.get("revisor"), c.get("fecha"))].append(e["celda"])
    tot_ok = tot_mal = 0
    for (rev, fecha), celdas in grupos.items():
        p = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py"), "sellar", d, "--revisor", str(rev), "--fecha", str(fecha), *celdas], capture_output=True, text=True)
        print(f"   sellar --revisor «{str(rev)[:60]}…» --fecha {fecha} ({len(celdas)} celdas): {p.stdout.strip().splitlines()[0] if p.stdout.strip() else p.stderr.strip()[-200:]}")
    r1 = VE.comprobar(d)
    print(f"   después: comprobadas {r1['comprobadas_universo']} de {r1['universo']} (cálculo {r1['comprobadas_calculo']} de {r1['universo_calculo']}; juicio {r1['comprobadas_juicio']} de {r1['universo_juicio']}) · pendientes {len(r1['pendientes'])} · desactualizadas {len(r1['desactualizadas'])} · discrepancias {len(r1['discrepancias'])} · errores {len(r1['errores'])} · sin entrada {len(r1['sin_entrada'])} · apto {r1['apto_por_entradas']}")
    print("   discrepancias:", [x[:150] for x in r1["discrepancias"]][:3], "| pendientes que no son «sin entrada»:", [x[:150] for x in r1["pendientes"] if "sin entrada" not in x][:3])
    shutil.rmtree(tmp, ignore_errors=True)
