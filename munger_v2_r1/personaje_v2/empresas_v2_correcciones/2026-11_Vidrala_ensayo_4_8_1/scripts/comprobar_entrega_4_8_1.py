#!/usr/bin/env python3
"""Controles de la entrega 4.8.1 (R-T1, R-F1 y R-F2). Solo escriben en temporales; el árbol no cambia.

Uso (desde munger_v2_r1/, después de `bash verificar_paquete.sh completa`): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_8_1/scripts/comprobar_entrega_4_8_1.py

Tipos de control: [reejecuta] vuelve a ejecutar código; [recalcula] recalcula huellas o cifras; [constata] comprueba lo conservado.
Las reproducciones con el código de la 4.8 se hacen en un árbol temporal en el que se sustituyen pipeline.py, cierre_v2.py y
prompts/verificacion.md por las copias conservadas en reproduccion/codigo_4_8/ (verificadas antes contra el manifiesto de la 4.8).
Tarda unos 10–15 minutos (vuelve a ejecutar las 25 mutaciones). Código 0 si todo cumple.
"""
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

sys.dont_write_bytecode = True
AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CORR = os.path.dirname(AQUI)
PV2 = os.path.dirname(CORR)
RAIZ = os.path.dirname(PV2)
REPRO, RES, FIN = (os.path.join(AQUI, x) for x in ("reproduccion", "resultados", "financiero"))
PY = sys.executable
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "recalcula": 0, "constata": 0}
CAMBIADOS_FRENTE_A_4_8 = {"CAMBIOS_ARCHIVOS.txt", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "VERSION", "verificar_paquete.sh",
                          "personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/DECISIONES.md", "personaje_v2/prompts/verificacion.md",
                          "personaje_v2/pruebas/agentes_sinteticos.py", "personaje_v2/pruebas/test_resumen_v2.py",
                          "personaje_v2/scripts/cierre_v2.py", "personaje_v2/scripts/pipeline.py"}
CODIGO_4_8 = {"personaje_v2/scripts/pipeline.py": "pipeline.py.txt", "personaje_v2/scripts/cierre_v2.py": "cierre_v2.py.txt",
              "personaje_v2/prompts/verificacion.md": "verificacion.md.txt", "personaje_v2/pruebas/agentes_sinteticos.py": "agentes_sinteticos.py.txt",
              "personaje_v2/pruebas/test_resumen_v2.py": "test_resumen_v2.py.txt", "verificar_paquete.sh": "verificar_paquete.sh.txt"}
TMP = tempfile.mkdtemp(prefix="control481_")


def comprobar(tipo, nombre, cond, det=""):
    global N_OK, N_T
    N_T += 1
    N_OK += bool(cond)
    TIPOS[tipo] += 1
    print(f"{'CUMPLE  ' if cond else 'NO CUMPLE'} · [{tipo}] {nombre}" + (f" · {det}" if det else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.isfile(p) else ""


def manifiesto(p):
    return {l.rstrip("\n").split("  ", 1)[1]: l.split("  ", 1)[0] for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")}


def corre(args, cwd=RAIZ, timeout=1800):
    r = subprocess.run([PY, "-B", *args], cwd=cwd, capture_output=True, text=True, timeout=timeout, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return r.returncode, r.stdout + r.stderr


def firma_bateria(txt):
    """Estado de cada prueba (en orden) y línea final: los detalles llevan identificadores aleatorios de solicitud."""
    estados = [l.split(" ")[0] for l in txt.splitlines() if l.startswith(("PASA ", "FALLA"))]
    fin = [l for l in txt.splitlines() if re.match(r"^\d+/\d+ pruebas ", l)]
    return estados, (fin[-1] if fin else None)


def arbol(nombre, codigo_4_8=False, fechas_renovadas=False):
    """Árbol temporal con personaje_v2 (sin los originales ni los expedientes salvo el de la 4.6.1) y enlaces a v6 y al kit."""
    raiz = os.path.join(TMP, nombre, "munger_v2_r1")
    shutil.copytree(PV2, os.path.join(raiz, "personaje_v2"), ignore=lambda d, fs: [f for f in fs if f in ("empresas_v2", ".lo_perfil", "__pycache__")
                                                                                     or (os.path.basename(d) == "empresas_v2_correcciones" and f != "2026-11_Vidrala_ensayo_4_6_1")])
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(RAIZ, x), os.path.join(raiz, x))
    if codigo_4_8:
        for dest, f in CODIGO_4_8.items():
            if dest.startswith("personaje_v2/scripts/") or dest.startswith("personaje_v2/prompts/"):
                shutil.copy(os.path.join(REPRO, "codigo_4_8", f), os.path.join(raiz, dest))
    if fechas_renovadas:
        t = time.time()
        for r, _, fs in os.walk(os.path.join(raiz, "personaje_v2", "empresas_v2_correcciones")):
            for f in fs:
                os.utime(os.path.join(r, f), (t, t))
    return raiz


try:
    print("ENTREGA 4.8.1 · R-T1, R-F1 y R-F2 · controles (solo escriben en temporales)\n" + "=" * 100)
    print("1. CONSERVACIÓN")
    m48 = manifiesto(os.path.join(REPRO, "MANIFIESTO_SHA256_4_8.txt"))
    dif = sorted(p for p, h in m48.items() if sha(os.path.join(RAIZ, p)) != h)
    comprobar("recalcula", f"Frente al manifiesto de la 4.8 ({len(m48)} archivos) solo cambian los archivos declarados; ninguno desaparece; originales, expedientes anteriores y decisiones de la 4.7.1 y la 4.8 intactos",
              set(dif) == CAMBIADOS_FRENTE_A_4_8 - {"MANIFIESTO_SHA256.txt"} and all(os.path.exists(os.path.join(RAIZ, p)) for p in m48), ", ".join(sorted(set(dif) ^ CAMBIADOS_FRENTE_A_4_8)) or f"{len(dif)} cambiados, todos declarados")
    p1 = os.path.join(CORR, "2026-11_Vidrala_ensayo_4_5", "Vidrala", "fase1_decisiones.json")
    comprobar("recalcula", "El registro humano de P1 conserva su huella b4e47afc…c445a4", (sha(p1) or "").startswith("b4e47afc") and sha(p1).endswith("c445a4"))
    sys.path.insert(0, os.path.join(PV2, "scripts"))
    import pipeline  # noqa: E402
    h2 = hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest()
    comprobar("recalcula", "La regla H2 (Pipeline.veredicto_auditoria) es idéntica a la de la 4.7.1 y la 4.8", h2 == "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422", h2[:16])
    comprobar("recalcula", "Las copias del código de la 4.8 de reproduccion/codigo_4_8/ tienen las huellas del manifiesto de la 4.8",
              all(sha(os.path.join(REPRO, "codigo_4_8", f)) == m48[d] for d, f in CODIGO_4_8.items()))

    print("2. R-T1 · SOLICITUDES DE AUDITORÍA")
    a48 = arbol("codigo_4_8", codigo_4_8=True)
    rc, out = corre([os.path.join(AQUI, "scripts", "reproducir_rt1.py"), "--raiz", a48, "--etiqueta", "la 4.8 (ZIP 6fc60aed…)"])
    comprobar("reejecuta", "Con el código de la 4.8, X-c + esquema restaurado + --desde 13 reutiliza la auditoría antigua con fechas UTC y renovadas (pide una nueva solo en CET): salida idéntica a la conservada",
              rc == 1 and out == leer(os.path.join(REPRO, "rt1_con_codigo_4_8.txt")) and "se reutiliza en: utc, renovadas" in out, out.strip().splitlines()[-1][:120])
    rc, out = corre([os.path.join(AQUI, "scripts", "reproducir_rt1.py"), "--raiz", RAIZ, "--etiqueta", "la 4.8.1"])
    comprobar("reejecuta", "Con el código actual, en los tres modos de fechas se pide una auditoría nueva (código 10, nada cerrado): salida idéntica a la conservada",
              rc == 0 and out == leer(os.path.join(REPRO, "rt1_con_codigo_4_8_1.txt")), out.strip().splitlines()[-1][:120])
    rc, out = corre(["pruebas/test_auditorias_v2.py"], cwd=PV2)
    f_act, f_cons = firma_bateria(out), firma_bateria(leer(os.path.join(RES, "test_auditorias_v2_salida.txt")))
    comprobar("reejecuta", "Batería de solicitudes de auditoría con el código actual: 55/55 y el mismo estado de cada prueba que la salida conservada",
              rc == 0 and f_act[1] == "55/55 pruebas de solicitudes de auditoría PASAN" and f_act == f_cons, str(f_act[1]))
    rc, out = corre(["pruebas/test_auditorias_v2.py", "--expediente", os.path.join(CORR, "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")], cwd=os.path.join(a48, "personaje_v2"))
    f48 = firma_bateria(out)
    comprobar("reejecuta", "La misma batería con el código de la 4.8 falla (la reparación no estaba): mismo estado de cada prueba que la reproducción conservada",
              rc != 0 and f48 == firma_bateria(leer(os.path.join(REPRO, "test_auditorias_con_codigo_4_8.txt"))) and f48[0].count("FALLA") > 0, str(f48[1]))
    for etiqueta, cod48, esperado in (("actual", False, "28/28"), ("de la 4.8", True, "27/28")):
        ar = arbol(f"estados_renovadas_{'48' if cod48 else '481'}", codigo_4_8=cod48, fechas_renovadas=True)
        rc, out = corre(["pruebas/test_estados_v2.py"], cwd=os.path.join(ar, "personaje_v2"))
        fin = firma_bateria(out)[1]
        comprobar("reejecuta", f"Batería de estados con el código {etiqueta} y TODAS las fechas renovadas: {esperado}" + (" (la subsanación de X-c reutilizaba la auditoría; es el 27/28 de la revisión externa)" if cod48 else ""),
                  (fin or "").startswith(esperado) and ((rc != 0 and "FALLA · B fallo de esquema al cerrar (X-c) · subsanación" in out) if cod48 else rc == 0), str(fin))
    mut = arbol("mutaciones")
    rc, out = corre([os.path.join(AQUI, "scripts", "mutar_rt1.py"), mut])
    comprobar("reejecuta", "Mutaciones del código de R-T1: las 25 hacen fallar la batería (resultado igual al conservado)",
              rc == 0 and "RESULTADO: 25 de 25 mutaciones detectadas" in out and leer(os.path.join(REPRO, "mutaciones_rt1.txt")).strip().endswith("RESULTADO: 25 de 25 mutaciones detectadas"), out.strip().splitlines()[-1][:80])
    for rel, nombre in (("2026-11_Vidrala_ensayo_4_8_1/scripts/comprobar_integracion_verificador_481.py", "4.8.1 (bloque nuevo de solicitudes de auditoría)"),
                        ("2026-11_Vidrala_ensayo_4_8/scripts/comprobar_integracion_verificador_48.py", "4.8 (estados)"),
                        ("2026-11_Vidrala_ensayo_4_7_1/scripts/comprobar_integracion_verificador_471.py", "4.7.1 (resumen)"),
                        ("2026-11_Vidrala_ensayo_4_6_1/scripts/comprobar_integracion_verificador.py", "4.6.1 (cierre)")):
        rc, out = corre([os.path.join(CORR, rel)])
        comprobar("reejecuta", f"Control de integración del verificador {nombre}: 13 de 13", rc == 0 and "RESULTADO: 13 de 13 comprobaciones cumplen." in out)
    v = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    comprobar("constata", "verificar_paquete.sh: el bloque de solicitudes de auditoría (mínimo 55) va antes del de estados, que sigue antes del del resumen y del de cierre",
              0 < v.find("== batería de solicitudes de auditoría") < v.find("== batería de coherencia de estados") < v.find("== batería del resumen") < v.find("== batería de cierre") and '-ge 55 ]; then\n    echo "$linea"; echo "RESULTADO auditorías: PASA"' in v)
    ax = leer(os.path.join(PV2, "ANEXO_D_salidas_y_formatos.md"))
    pr = leer(os.path.join(PV2, "prompts", "verificacion.md"))
    comprobar("constata", "Anexo D y prompt de verificación piden la línea «Solicitud de auditoría: <id>» y declaran que las fechas no intervienen en el paso 13",
              "Solicitud de auditoría (4.8.1, R-T1)" in ax and "Las fechas no deciden nada" in ax and "`Solicitud de auditoría: {SOLICITUD_AUDITORIA}`" in pr)

    print("3. R-F1 Y R-F2 · REINVERSIÓN (modelo auxiliar)")
    sal = os.path.join(TMP, "rf")
    rc, out = corre([os.path.join(AQUI, "scripts", "analisis_reinversion_4_8_1.py"), "--salida", sal])
    archivos = ("rf1_alternativas.csv", "rf2_credito_y_convencion.csv", "rf_conciliacion_anual_y_terminal.csv", "rf_resultados.json", "rf_salida.txt")
    iguales = {f: sha(os.path.join(sal, f)) == sha(os.path.join(FIN, f)) for f in archivos}
    comprobar("reejecuta", "analisis_reinversion_4_8_1.py: código 0 (réplica de la 4.8 idéntica, motor que reproduce la 4.8, identidades) y sus cinco salidas idénticas a las conservadas",
              rc == 0 and all(iguales.values()), ", ".join(f for f, ok in iguales.items() if not ok) or "5/5 idénticas")
    d = json.load(open(os.path.join(FIN, "rf_resultados.json"), encoding="utf-8"))
    casos = d["rf2"]["casos"]
    refs = {"REF": (69.2446731, 64.2621768), "X41": (48.6081961, 44.0094136), "X41c": (61.0825280, 53.6729333), "P5x0": (59.0350469, 52.3123793)}
    comprobar("recalcula", "R-F2: las cuatro referencias externas del encargo se reproducen a 7 decimales (REF, X41, X41 con el mismo requisito y crédito, P5x0)",
              all(round(casos[k]["ponderado"], 7) == a and round(casos[k]["precio_si"], 7) == b for k, (a, b) in refs.items()))
    e = d["rf2"]["efectos"]["ponderado"]
    comprobar("recalcula", "R-F2: el crédito explica el 60,45 % de la caída de X41 y la convención terminal −2,0475 frente al contraste; la descomposición de Shapley cierra",
              round(e["fraccion_caida_X41_atribuida_al_credito"], 4) == 0.6045 and round(e["convencion_con_credito"], 4) == -2.0475
              and abs(e["shapley_credito"] + e["shapley_convencion"] - e["P5x0_menos_X41"]) < 1e-12, f"{e['fraccion_caida_X41_atribuida_al_credito']:.4%} · {e['convencion_con_credito']:+.4f}")
    alt = d["rf1"]["alternativas"]
    comprobar("recalcula", "R-F1: con cada requisito, la estructura del hueco da el valor más alto y la suma sin reestimar el más bajo (no se elige ninguna; el abanico se publica entero)",
              all(alt[f"H·{rk}"]["ponderado"] >= max(alt[f"{s}·{rk}"]["ponderado"] for s in ("S", "SR1", "SR2")) and alt[f"S·{rk}"]["ponderado"] <= min(alt[f"{s}·{rk}"]["ponderado"] for s in ("SR1", "SR2"))
                  for rk in ("L1.10", "L1.15", "L1.25", "T0.25", "T0.50", "T0.75", "T1.00")))
    dec = json.load(open(os.path.join(FIN, "decisiones_y_preguntas_4_8_1.json"), encoding="utf-8"))
    comprobar("constata", "Decisiones de la 4.8.1: campos humanos vacíos; D-N3b revisada sin estructura por defecto; P1s de la 4.8 retirado",
              all(x["decision"] is None and x["fecha"] is None and x["confirmado_por"] is None for x in dec["decisiones"])
              and "Ninguna estructura por defecto" in dec["decisiones"][0]["propuesta_de_claude"] and "P1s de la 4.8 se retira" in dec["decisiones"][0]["propuesta_de_claude"])
    inf = leer(os.path.join(AQUI, "INFORME_REINVERSION_4_8_1.md"))
    comprobar("constata", "El informe retira las afirmaciones de la 4.8 sobre el doble cómputo y el mantenimiento cubierto, y deja P-M1 abierta",
              "## 4. Afirmaciones de la 4.8 que se retiran" in inf and "P-M1 sigue abierta" in inf and "60,45 %" in inf)

    print("4. DOCUMENTACIÓN DE LA ENTREGA")
    ver, cont, prm = (leer(os.path.join(RAIZ, x)) for x in ("VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md"))
    zipn = "munger_v2_r1_entrega4.8.1_auditorias_y_reinversion.zip"
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.8.1: versión, ZIP, batería de solicitudes de auditoría de 55 y este control",
              ver.startswith("munger_v2 · r1 · entrega 4.8.1") and zipn in cont and zipn in prm and "55/55" in prm and "comprobar_entrega_4_8_1.py" in cont and "comprobar_entrega_4_8_1.py" in prm)
    for f in ("REGISTRO_ENTREGA_4.8.1.md", "INFORME_REINVERSION_4_8_1.md", "AUDITORIA_INTERNA_4_8_1.md", "AUDITORIA_INTERNA_4_8_1_vigencia.md", "AUDITORIA_INTERNA_4_8_1_tercera.md", "resultados/LEEME_BATERIAS_HISTORICAS.md"):
        comprobar("constata", f"existe {f}", os.path.isfile(os.path.join(AQUI, f)))
finally:
    shutil.rmtree(TMP, ignore_errors=True)
print(f"Tipos de control: {TIPOS['reejecuta']} reejecutan, {TIPOS['recalcula']} recalculan y {TIPOS['constata']} solo constatan lo conservado.")
print(f"RESULTADO: {N_OK} de {N_T} comprobaciones cumplen.")
sys.exit(0 if N_OK == N_T else 1)
