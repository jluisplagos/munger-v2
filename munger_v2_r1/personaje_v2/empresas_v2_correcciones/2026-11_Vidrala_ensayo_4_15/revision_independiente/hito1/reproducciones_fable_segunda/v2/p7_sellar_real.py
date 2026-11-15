"""Hallazgo 3 sobre datos reales (copias en /tmp del árbol CONGELADO): los registros de la 4.14, revisados el 14-nov-2026.
(1) `sellar` con su fecha (14-nov) y con la de hoy; (2) reproducción del diagnóstico de la coordinación (vínculo SIMULADO); (3) lo que
se podría sellar tras reescribir las fechas a hoy con un script (límite declarado)."""
import collections, datetime, hashlib, json, os, shutil, subprocess, sys, tempfile
PV = os.environ.get("PV", "/tmp/rev_fable2/congelado/personaje_v2")
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.join(PV, "scripts"))
import verificacion_entradas as VE
HOY = datetime.datetime.now().astimezone().date().isoformat()
CLI = [sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py")]
DIAG = json.load(open(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "resultados", "diagnostico_registros_4_14_con_reglas_4_15.json"), encoding="utf-8"))
sha = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()
for exp in ("viscofan_decisiones/Viscofan", "vidrala_decisiones/Vidrala", "elis_decisiones/Elis"):
    src = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", exp); nom = os.path.basename(src)
    tmp = tempfile.mkdtemp(prefix="rev_fable_sellar_real_"); d = os.path.join(tmp, nom)
    shutil.copytree(src, d, ignore=shutil.ignore_patterns("recalc", "variantes_v64", "prompts_generados", ".lo_perfil", "historial_cierres", "antecedentes"))
    reg = json.load(open(os.path.join(d, VE.REGISTRO), encoding="utf-8")); s0 = sha(os.path.join(d, VE.REGISTRO))
    r0 = VE.comprobar(d)
    print(f"== {exp} · registro formato {reg['formato']} · {len(reg['entradas'])} entradas · con el código congelado: comprobadas {r0['comprobadas_universo']} de {r0['universo']} (cálculo {r0['comprobadas_calculo']} de {r0['universo_calculo']}; juicio {r0['comprobadas_juicio']} de {r0['universo_juicio']}) · apto {r0['apto_por_entradas']}")
    print("   motivo:", str(r0["motivo"])[:420])
    grupos = collections.defaultdict(list)
    for e in reg["entradas"]:
        c = e.get("comprobacion") or {}
        grupos[(c.get("revisor"), c.get("fecha"))].append(e["celda"])
    print("   (revisor, fecha) → nº de entradas:", {(str(k[0])[:28], k[1]): len(v) for k, v in grupos.items()})
    tot = [0, 0]
    for (rev, fecha), celdas in grupos.items():
        p = subprocess.run(CLI + ["sellar", d, "--revisor", str(rev), "--fecha", str(fecha), *celdas], capture_output=True, text=True)
        p2 = subprocess.run(CLI + ["sellar", d, "--revisor", str(rev), "--fecha", HOY, *celdas], capture_output=True, text=True)
        l2 = (p2.stdout.strip().splitlines() or [p2.stderr.strip()[-150:]])[0]
        print(f"   (1) sellar --fecha {fecha} ({len(celdas)} celdas): rc {p.returncode} · {(p.stdout + p.stderr).strip()[:110]} || --fecha {HOY}: rc {p2.returncode} · {l2}")
    print("   registro sin cambios:", sha(os.path.join(d, VE.REGISTRO)) == s0)
    # (2) diagnóstico con vínculo simulado (como scripts/diagnostico_registros_4_14.py)
    reg2 = json.load(open(os.path.join(d, VE.REGISTRO), encoding="utf-8")); reg2["formato"] = "4.15"
    hs = VE.huellas_registro(d, reg2)
    for e in reg2["entradas"]:
        c = e.setdefault("comprobacion", {}) or {}; e["comprobacion"] = c
        c["vinculo"] = {"huella": hs[e["celda"]], "sellado_por": c.get("revisor"), "fecha": c.get("fecha")}
    json.dump(reg2, open(os.path.join(d, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False)
    r = VE.comprobar(d); dg = DIAG[nom]
    print(f"   (2) vínculo SIMULADO: cálculo {r['comprobadas_calculo']} de {r['universo_calculo']} · errores {len(r['errores'])} · discrepancias {len(r['discrepancias'])} · desactualizadas {len(r['desactualizadas'])} · no reproducibles {len(r['entradas_no_reproducibles'])} · datos como hipótesis {len(r['datos_como_hipotesis'])}"
          f" || diagnóstico de la coordinación: {dg['comprobadas_calculo']} de {dg['universo_calculo']} · errores {len(dg['errores'])} · discrepancias {len(dg['discrepancias'])} · iguales: {r['errores'] == dg['errores'] and r['discrepancias'] == dg['discrepancias'] and r['comprobadas_calculo'] == dg['comprobadas_calculo']}")
    clases = collections.Counter((e.get("clase"), "aux" if str(e.get("celda")).startswith("aux:") else "celda") for e in reg["entradas"])
    print("   clases del registro (clase, tipo):", dict(clases))
    aux_hip = [e["celda"] for e in reg["entradas"] if str(e["celda"]).startswith("aux:") and e.get("clase") in ("hipotesis", "convencion")]
    por = {e["celda"]: e for e in reg["entradas"]}
    der_de_aux_hip = [e["celda"] for e in reg["entradas"] if e.get("clase") == "derivado" and any(o in aux_hip for o in (e.get("derivacion") or {}).get("origenes") or [])]
    print("   auxiliares que son hipótesis o convención:", aux_hip[:8], "| derivados que dependen de ellos:", der_de_aux_hip[:8])
    na_cero = [e["celda"] for e in reg["entradas"] if e.get("clase") == "no_aplicable" and isinstance(e.get("valor_modelo"), (int, float)) and not isinstance(e.get("valor_modelo"), bool)]
    print("   «no_aplicable» con un cero en el libro:", na_cero[:10], "| con material false:", [e["celda"] for e in reg["entradas"] if e.get("material") is False][:5])
    # (3) fechas reescritas a hoy + sellar real
    reg3 = json.load(open(os.path.join(src, VE.REGISTRO), encoding="utf-8"))
    for e in reg3["entradas"]:
        if isinstance(e.get("comprobacion"), dict):
            e["comprobacion"]["fecha"] = HOY
    json.dump(reg3, open(os.path.join(d, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False)
    n_ok = n_mal = 0
    for rev in {k[0] for k in grupos}:
        celdas = [e["celda"] for e in reg3["entradas"] if (e.get("comprobacion") or {}).get("revisor") == rev]
        p = subprocess.run(CLI + ["sellar", d, "--revisor", str(rev), "--fecha", HOY, *celdas], capture_output=True, text=True)
        l = (p.stdout.strip().splitlines() or [""])[0]
        try:
            n_ok += int(l.split()[1]); n_mal += int(l.split()[4])
        except Exception:
            print("      ", (p.stdout + p.stderr)[-200:])
    r3 = VE.comprobar(d)
    print(f"   (3) tras reescribir las {len(reg3['entradas'])} fechas a {HOY} con un script y sellar por revisor: selladas {n_ok} · rechazadas {n_mal} → comprobadas {r3['comprobadas_universo']} de {r3['universo']} (cálculo {r3['comprobadas_calculo']} de {r3['universo_calculo']}) · apto {r3['apto_por_entradas']}")
    shutil.rmtree(tmp, ignore_errors=True)
