#!/usr/bin/env python3
"""Auditoría interna 4.9 · ataques a R-V1 (vigencia de la respuesta de auditoría aceptada).
Uso: python3 -B ataques_rv1.py [nombre_ataque ...]
Trabaja solo en /home/claude/auditoria_4_9/tmp/escenarios/. No modifica la copia auditada."""
import csv, hashlib, json, os, shutil, subprocess, sys, unicodedata

RAIZ = "/home/claude/auditoria_4_9/munger_v2_r1/personaje_v2"
SCR = os.environ.get("SCR_AUDITOR") or os.path.join(RAIZ, "scripts")
EXP = os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
BASE = os.environ.get("BASE_AUDITOR") or "/home/claude/auditoria_4_9/tmp/escenarios"
sys.path.insert(0, SCR); sys.path.insert(0, os.path.join(RAIZ, "pruebas"))
sys.dont_write_bytecode = True
import cierre_v2 as CIE  # noqa
import agentes_sinteticos as AG  # noqa

EMPRESA = "Vidrala, S.A."
FRASE = "Aviso: La evidencia respalda el crecimiento; la reposición queda pendiente. (auditoría sintética de la prueba R-V1)"
PY = sys.executable
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/home/claude/auditoria_4_9/tmp/tmpdir"}


def corre(script, *a):
    r = subprocess.run([PY, "-B", os.path.join(SCR, script), *a], capture_output=True, text=True, env=ENV)
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def filas(p):
    if not os.path.isfile(p):
        return []
    return [(r.get("verificacion") or "")[:24] for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == EMPRESA]


def construir():
    b = os.path.join(BASE, "_base")
    if os.path.exists(os.path.join(b, "LISTO")):
        return b
    shutil.rmtree(b, ignore_errors=True)
    d = os.path.join(b, "exp", "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(b, "exp", f))
    os.makedirs(os.path.join(b, "otro"))
    print("desde13", corre("pipeline.py", d, "--desde", "13")[0])
    AG.auditoria(d, "APROBADO")
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write(FRASE + "\n")
    print("cierre", corre("pipeline.py", d)[0])
    print("resumen extra", corre("resumen.py", d, os.path.join(b, "otro", "resumen_configurado.csv"))[0])
    open(os.path.join(b, "LISTO"), "w").write("ok")
    return b


def copia(nombre):
    b = construir()
    n = os.path.join(BASE, nombre)
    shutil.rmtree(n, ignore_errors=True)
    shutil.copytree(b, n, symlinks=True)
    return n, os.path.join(n, "exp", "Vidrala")


def estado(n, d):
    st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "estado_pipeline.json")) else {}
    F = json.load(open(os.path.join(d, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "ficha.json")) else None
    return {"estado": st.get("estado_analisis"), "auditoria": st.get("auditoria"), "ficha_cerrada": bool(F and F.get("cierre")),
            "cierre_vigente": os.path.exists(os.path.join(d, "cierre_vigente.json")),
            "pred": filas(os.path.join(n, "exp", "resumen_v2.csv")), "extra": filas(os.path.join(n, "otro", "resumen_configurado.csv"))}


VIAS = {"paso14": lambda n, d: corre("pipeline.py", d, "--desde", "14"),
        "sin_desde": lambda n, d: corre("pipeline.py", d),
        "ficha": lambda n, d: corre("ficha.py", d, "--estado", "concluido"),
        "informe": lambda n, d: corre("informe.py", d),
        "resumen": lambda n, d: corre("resumen.py", d, os.path.join(n, "exp", "resumen_v2.csv"))}


def leer(d):
    return open(os.path.join(d, "auditoria.md"), "rb").read()


def esc(d, b):
    open(os.path.join(d, "auditoria.md"), "wb").write(b)


def t(d):
    return leer(d).decode("utf-8")


# --- mutaciones: (nombre, función, debe_retirarse) ---
def m_byte_invalido(d):
    esc(d, leer(d) + b"\xff\n")


def m_cp1252(d):
    esc(d, t(d).encode("cp1252"))


def m_utf16(d):
    esc(d, t(d).encode("utf-16"))


def m_zwsp(d):
    esc(d, t(d).replace("respalda el crecimiento", "respalda el​ crecimiento").encode())


def m_nbsp(d):
    esc(d, t(d).replace("respalda el crecimiento", "respalda el crecimiento").encode())


def m_vt(d):
    esc(d, t(d).replace("el crecimiento", "el\x0bcrecimiento").encode())


def m_ls(d):
    esc(d, t(d).replace("el crecimiento", "el crecimiento").encode())


def m_bom_medio(d):
    esc(d, t(d).replace("el crecimiento", "el﻿crecimiento").encode())


def m_fullwidth_solicitud(d):
    import re
    esc(d, re.sub(r"SA-([0-9a-f]{16})", lambda m: "ＳＡ-" + m.group(1), t(d)).encode())


def m_greek_qm(d):
    # U+037E (signo de interrogación griego) es canónicamente equivalente a «;» (NFC lo convierte): transformación inocua declarada
    esc(d, t(d).replace("crecimiento;", "crecimiento;").encode())


def m_kelvin(d):
    esc(d, t(d).replace("Aviso", "Aviso").replace("VEREDICTO", "VEREDICTO").encode())


def m_doble_bom(d):
    esc(d, b"\xef\xbb\xbf\xef\xbb\xbf" + leer(d))


def m_crlf_bom_nfd_sin_final(d):
    esc(d, b"\xef\xbb\xbf" + unicodedata.normalize("NFD", t(d)).rstrip("\n").replace("\n", "\r\n").encode())


def m_negacion(d):
    esc(d, t(d).replace("respalda el crecimiento", "no respalda el crecimiento").encode())


MUT = {"byte_invalido": (m_byte_invalido, True), "cp1252": (m_cp1252, True), "utf16": (m_utf16, True), "zwsp": (m_zwsp, True), "nbsp": (m_nbsp, True),
       "vt": (m_vt, True), "ls_u2028": (m_ls, True), "bom_medio": (m_bom_medio, True), "fullwidth_solicitud": (m_fullwidth_solicitud, True),
       "doble_bom": (m_doble_bom, True), "greek_qm_nfc": (m_greek_qm, False), "combinada_inocua": (m_crlf_bom_nfd_sin_final, False),
       "negacion": (m_negacion, True)}


def ataque_mutaciones(nombres_vias=("paso14", "ficha", "informe", "resumen")):
    res = []
    for mn, (f, retirar) in MUT.items():
        for v in nombres_vias:
            n, d = copia(f"m_{mn}_{v}")
            f(d)
            rc, out = VIAS[v](n, d)
            e = estado(n, d)
            retirada = (not e["ficha_cerrada"]) and all(x.startswith("SIN APROB") for x in e["pred"] + e["extra"])
            vigente = e["ficha_cerrada"] and e["cierre_vigente"] and all(x == "APROBADO" for x in e["pred"] + e["extra"])
            ok = retirada if retirar else vigente
            ult = (out.splitlines() or [""])[-1][:150]
            res.append({"mutacion": mn, "via": v, "esperado": "retirada" if retirar else "vigente", "rc": rc, "ok": ok, **e, "ultima": ult})
            print(("OK   " if ok else "FALLO"), mn, v, rc, e, ult, flush=True)
            shutil.rmtree(n, ignore_errors=True)
    return res


def ataque_sin_estado_ni_cierre_vigente():
    """Borrar estado_pipeline.json y cierre_vigente.json (sin reescribir ninguna huella) y sustituir auditoria.md por otra APROBADO
    del mismo material: ¿vuelve a cerrar ficha.py y a publicar resumen.py?"""
    out = []
    n, d = copia("x_sin_estado_ni_cv")
    os.remove(os.path.join(d, "estado_pipeline.json"))
    os.remove(os.path.join(d, "cierre_vigente.json"))
    AG.auditoria(d, "APROBADO", solicitud=False)  # otra auditoría APROBADO, sin solicitud, con el material fijado
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("Aviso: auditoría distinta de la aceptada (prueba del auditor interno).\n")
    rc1, o1 = corre("ficha.py", d, "--estado", "concluido")
    e1 = estado(n, d)
    rc2, o2 = corre("resumen.py", d, os.path.join(n, "exp", "resumen_v2.csv"))
    e2 = estado(n, d)
    rc3, o3 = corre("resumen.py", d, os.path.join(n, "otro", "resumen_configurado.csv"))
    e3 = estado(n, d)
    rc4, o4 = corre("informe.py", d)
    cv = json.load(open(os.path.join(d, "cierre_vigente.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "cierre_vigente.json")) else None
    r = {"ficha.py": [rc1, o1.splitlines()[-1][:200], e1], "resumen.py pred": [rc2, o2.splitlines()[-1][:200], e2], "resumen.py extra": [rc3, o3.splitlines()[-1][:200], e3],
         "informe.py": [rc4, o4.splitlines()[-1][:200]], "cierre_vigente": cv,
         "auditoria_sha_actual": hashlib.sha256(leer(d)).hexdigest()}
    print(json.dumps(r, ensure_ascii=False, indent=1))
    out.append(r)
    return out


def ataque_sin_estado_ni_cv_pipeline():
    """Igual, pero con pipeline.py --desde 14 (sin estado: el pipeline crea uno nuevo)."""
    n, d = copia("x_sin_estado_ni_cv_pipeline")
    os.remove(os.path.join(d, "estado_pipeline.json"))
    os.remove(os.path.join(d, "cierre_vigente.json"))
    AG.auditoria(d, "APROBADO", solicitud=False)
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("Aviso: auditoría distinta de la aceptada (prueba del auditor interno).\n")
    rc, o = corre("pipeline.py", d, "--desde", "14")
    e = estado(n, d)
    print(rc, o.splitlines()[-3:], e)
    return [{"rc": rc, "out": o.splitlines()[-3:], **e}]


def ataque_reiniciar_estado():
    """Solo se borra estado_pipeline.json (lo que hace --reiniciar) y se cambia auditoria.md: debe retirarse por cierre_vigente.json."""
    n, d = copia("x_sin_estado")
    os.remove(os.path.join(d, "estado_pipeline.json"))
    AG.auditoria(d, "APROBADO", solicitud=False)
    rc, o = corre("ficha.py", d, "--estado", "concluido")
    e = estado(n, d)
    print(rc, o.splitlines()[-1][:200], e)
    return [{"rc": rc, **e}]


def ataque_sin_desde_y_desde13():
    res = []
    for v in ("sin_desde",):
        for mn in ("negacion", "byte_invalido"):
            f, _ = MUT[mn]
            n, d = copia(f"s_{mn}_{v}")
            f(d)
            rc, out = VIAS[v](n, d)
            e = estado(n, d)
            print(mn, v, rc, e, out.splitlines()[-2:])
            res.append({"mutacion": mn, "via": v, "rc": rc, **e, "ultimas": out.splitlines()[-2:]})
    n, d = copia("s_negacion_desde13")
    m_negacion(d)
    rc, out = corre("pipeline.py", d, "--desde", "13")
    e = estado(n, d)
    print("negacion desde13", rc, e, out.splitlines()[-2:])
    res.append({"mutacion": "negacion", "via": "desde13", "rc": rc, **e, "ultimas": out.splitlines()[-2:]})
    return res


ATAQUES = {"mutaciones": ataque_mutaciones, "sin_estado_ni_cv": ataque_sin_estado_ni_cierre_vigente, "sin_estado_ni_cv_pipeline": ataque_sin_estado_ni_cv_pipeline,
           "sin_estado": ataque_reiniciar_estado, "otras_vias": ataque_sin_desde_y_desde13}

def ataque_461_sin_cv():
    """Cierre real de la 4.6.1 (sin solicitudes): se borra SOLO cierre_vigente.json y se sustituye auditoria.md por otra APROBADO del
    mismo material. ¿ficha.py vuelve a cerrar y registra la huella del archivo nuevo?"""
    res = {}
    n = os.path.join(BASE, "x_461_sin_cv")
    shutil.rmtree(n, ignore_errors=True)
    d = os.path.join(n, "exp", "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(n, "exp", f))
    os.makedirs(os.path.join(n, "otro"))
    sha0 = hashlib.sha256(leer(d)).hexdigest()
    os.remove(os.path.join(d, "cierre_vigente.json"))
    AG.auditoria(d, "APROBADO", solicitud=False)
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("Aviso: auditoría distinta de la que aprobó el cierre de la 4.6.1 (prueba del auditor interno).\n")
    rc1, o1 = corre("ficha.py", d, "--estado", "concluido")
    e1 = estado(n, d)
    rc2, o2 = corre("informe.py", d)
    rc3, o3 = corre("resumen.py", d, os.path.join(n, "exp", "resumen_v2.csv"))
    e3 = estado(n, d)
    cv = json.load(open(os.path.join(d, "cierre_vigente.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "cierre_vigente.json")) else None
    rc4, o4 = corre("pipeline.py", d, "--desde", "14")
    e4 = estado(n, d)
    res = {"sha_auditoria_original": sha0, "sha_auditoria_nueva": hashlib.sha256(leer(d)).hexdigest(),
           "ficha.py": [rc1, o1.splitlines()[-1][:200], e1], "informe.py": [rc2, o2.splitlines()[-1][:200]], "resumen.py": [rc3, o3.splitlines()[-1][:200], e3],
           "cierre_vigente_tras_ficha": cv, "pipeline --desde 14": [rc4, o4.splitlines()[-2:], e4]}
    print(json.dumps(res, ensure_ascii=False, indent=1))
    return [res]


ATAQUES["461_sin_cv"] = ataque_461_sin_cv

def ataque_ilegibles():
    """auditoria.md cambiada y, además, cierre_vigente.json o estado_pipeline.json ilegibles (JSON truncado)."""
    res = []
    for cual in ("cierre_vigente.json", "estado_pipeline.json"):
        for v in ("ficha", "resumen", "paso14"):
            n, d = copia(f"i_{cual.split('.')[0]}_{v}")
            m_negacion(d)
            p = os.path.join(d, cual)
            open(p, "w", encoding="utf-8").write(open(p, encoding="utf-8").read()[:40])
            rc, out = VIAS[v](n, d)
            e = estado(n, d) if cual != "estado_pipeline.json" else {"pred": filas(os.path.join(n, "exp", "resumen_v2.csv")), "extra": filas(os.path.join(n, "otro", "resumen_configurado.csv")),
                                                                     "ficha_existe": os.path.exists(os.path.join(d, "ficha.json"))}
            ult = (out.splitlines() or [""])[-1][:160]
            print(cual, v, rc, e, ult, flush=True)
            res.append({"ilegible": cual, "via": v, "rc": rc, **e, "ultima": ult})
            shutil.rmtree(n, ignore_errors=True)
    return res


ATAQUES["ilegibles"] = ataque_ilegibles

if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    sel = sys.argv[1:] or list(ATAQUES)
    todo = {}
    for a in sel:
        todo[a] = ATAQUES[a]()
    json.dump(todo, open(f"/home/claude/auditoria_4_9/tmp/ataques_rv1{os.environ.get("SUFIJO_AUDITOR","")}_{'_'.join(sel)}.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)


