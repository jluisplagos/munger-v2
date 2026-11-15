#!/usr/bin/env python3
"""Ataques del segundo control de vigencia de la 4.9 (auditor interno). Solo trabaja en copias bajo /home/claude/vigencia2_4_9/tmp.
Solo usa pipeline.py (pasos 13/14: --desde 13 para construir el escenario base y --desde 14 o sin --desde en un cierre concluido),
ficha.py, informe.py y resumen.py del árbol de la copia. No usa LibreOffice.

Uso: python3 -I -B ataques_v2.py <grupo> [<grupo>...]   (grupos: rep, nuevos, v3, ficha_ilegible, simbolicos, permisos, h46)
"""
import csv
import json
import os
import shutil
import subprocess
import sys

RAIZ = "/home/claude/vigencia2_4_9/munger_v2_r1"
SCR = os.path.join(RAIZ, "personaje_v2", "scripts")
PRU = os.path.join(RAIZ, "personaje_v2", "pruebas")
EXP461 = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
EXP46 = os.path.join(RAIZ, "personaje_v2", "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6", "Vidrala")
TMP = "/home/claude/vigencia2_4_9/tmp/escenarios"
sys.dont_write_bytecode = True
sys.path.insert(0, SCR)
sys.path.insert(0, PRU)
import cierre_v2 as CIE  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

PY = sys.executable
EMPRESA = "Vidrala, S.A."
FRASE = "Aviso: La evidencia respalda el crecimiento; la reposición queda pendiente. (auditoría sintética de la prueba R-V1)"
RES = []
USUARIO = None  # para el grupo de permisos: ejecutar como otro usuario


def corre(script, *args):
    if script == "pipeline.py" and "--desde" not in args and not os.path.isfile(os.path.join(args[0], "estado_pipeline.json")):
        raise RuntimeError("salvaguarda del auditor: pipeline.py sin --desde y sin estado arrancaría en el paso 0 (LibreOffice)")
    if script == "pipeline.py" and "--desde" in args and int(args[list(args).index("--desde") + 1]) < 13:
        raise RuntimeError("salvaguarda del auditor: --desde < 13")
    cmd = [PY, "-I", "-B", os.path.join(SCR, script), *args]
    if USUARIO:
        cmd = ["setpriv", f"--reuid={USUARIO}", f"--regid={USUARIO}", "--clear-groups"] + cmd
    r = subprocess.run(cmd, capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def filas(p):
    if not os.path.isfile(p):
        return []
    return [r for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == EMPRESA]


def ver(p):
    f = filas(p)
    return [(r.get("verificacion") or "")[:22] for r in f]


def jl(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except Exception:
        return None


class Caso:
    def __init__(self, base):
        self.base = base
        self.d = os.path.join(base, "exp", "Vidrala")
        self.pred = os.path.join(base, "exp", "resumen_v2.csv")
        self.extra = os.path.join(base, "otro_destino", "resumen_configurado.csv")
        self.aud = os.path.join(self.d, "auditoria.md")

    def copiar(self, nombre):
        nuevo = os.path.join(TMP, nombre)
        if os.path.exists(nuevo):
            subprocess.run(["chmod", "-R", "u+rwX", nuevo])
            shutil.rmtree(nuevo)
        shutil.copytree(self.base, nuevo, symlinks=True)
        return Caso(nuevo)

    def p(self, f):
        return os.path.join(self.d, f)

    def st(self):
        return jl(self.p("estado_pipeline.json")) if os.path.isfile(self.p("estado_pipeline.json")) else None

    def ultima_retirada(self):
        h = self.p("historial_cierres")
        a = sorted(os.listdir(h)) if os.path.isdir(h) else []
        return (jl(os.path.join(h, a[-1], "RETIRADA.json")) or {}) if a else {}


def base_respuesta():
    """Como escenario_respuesta de test_integridad_auditoria_v2.py: --desde 13 sobre una copia del cierre de la 4.6.1, respuesta
    sintética válida con la frase de la prueba, cierre (código 0) y publicación en un destino configurado."""
    base = os.path.join(TMP, "base_respuesta")
    c = Caso(base)
    if os.path.exists(os.path.join(base, "LISTO")):
        return c
    if os.path.exists(base):
        shutil.rmtree(base)
    shutil.copytree(EXP461, c.d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP461), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP461), f), os.path.join(base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    rc13, o13 = corre("pipeline.py", c.d, "--desde", "13")
    AG.auditoria(c.d, "APROBADO")
    open(c.aud, "a", encoding="utf-8").write(FRASE + "\n")
    rc, out = corre("pipeline.py", c.d)
    rcr, _ = corre("resumen.py", c.d, c.extra)
    print(f"BASE respuesta: --desde 13 → {rc13}; cierre → {rc} ({out.splitlines()[-1][:80]}); resumen extra → {rcr}; pred {ver(c.pred)} extra {ver(c.extra)}")
    assert rc13 == 10 and rc == 0 and rcr == 0
    open(os.path.join(base, "LISTO"), "w").write("ok")
    return c


def base_historico():
    base = os.path.join(TMP, "base_historico")
    c = Caso(base)
    if os.path.exists(os.path.join(base, "LISTO")):
        return c
    if os.path.exists(base):
        shutil.rmtree(base)
    shutil.copytree(EXP461, c.d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP461), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP461), f), os.path.join(base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    rcr, _ = corre("resumen.py", c.d, c.extra)
    assert rcr == 0
    open(os.path.join(base, "LISTO"), "w").write("ok")
    return c


VIAS = {
    "paso14": lambda c: corre("pipeline.py", c.d, "--desde", "14"),
    "pipeline": lambda c: corre("pipeline.py", c.d),
    "ficha": lambda c: corre("ficha.py", c.d, "--estado", "concluido"),
    "informe": lambda c: corre("informe.py", c.d),
    "resumen": lambda c: corre("resumen.py", c.d, c.pred),
}


def observa(c, rc, out):
    st = c.st()
    F = jl(c.p("ficha.json")) if os.path.isfile(c.p("ficha.json")) else None
    return {"rc": rc, "traza": "Traceback" in out, "ultima": (out.splitlines() or [""])[-1][:200],
            "estado": (st or {}).get("estado_analisis") if isinstance(st, dict) else "?", "auditoria": (st or {}).get("auditoria") if isinstance(st, dict) else "?",
            "ficha_cerrada": bool(isinstance(F, dict) and F.get("cierre")), "ficha_existe": os.path.lexists(c.p("ficha.json")),
            "cv_existe": os.path.lexists(c.p("cierre_vigente.json")), "pred": ver(c.pred), "extra": ver(c.extra),
            "retirada": (c.ultima_retirada().get("motivo") or "")[:160]}


def publicada(o):
    return any(x == "APROBADO" for x in o["pred"] + o["extra"])


def caso(grupo, nombre, base, mutar, via, esperado="retira"):
    c = base.copiar(f"{grupo}__{nombre}__{via}".replace(" ", "_").replace("/", "_"))
    mutar(c)
    rc, out = VIAS[via](c)
    o = observa(c, rc, out)
    if esperado == "retira":
        ok = not o["traza"] and not o["ficha_cerrada"] and not publicada(o) and rc in (3, 4, 5, 6)
    else:
        ok = not o["traza"] and o["ficha_cerrada"] and o["pred"] == ["APROBADO"] and o["extra"] == ["APROBADO"] and rc == 0
    RES.append(dict(grupo=grupo, caso=nombre, via=via, esperado=esperado, cumple=ok, **o))
    print(f"{'OK  ' if ok else 'MAL '} · {grupo} · {nombre} · {via} · rc {rc} · traza {o['traza']} · estado {o['estado']!r}/{o['auditoria']!r} · ficha cerrada {o['ficha_cerrada']} · cv {o['cv_existe']} · pred {o['pred']} · extra {o['extra']} · {o['ultima'][:110]}", flush=True)
    if o["traza"]:
        tb = [l for l in out.splitlines() if "Error" in l or "line " in l][-3:]
        print("       traza:", " | ".join(x.strip()[:120] for x in tb), flush=True)
    return c, o, out


def escribe(nombre, contenido, modo="w"):
    def f(c):
        p = c.p(nombre)
        if os.path.isdir(p) and not os.path.islink(p):
            shutil.rmtree(p)
        elif os.path.lexists(p):
            os.remove(p)
        if isinstance(contenido, bytes):
            open(p, "wb").write(contenido)
        else:
            open(p, "w", encoding="utf-8").write(contenido)
    return f


def carpeta(nombre):
    def f(c):
        p = c.p(nombre)
        if os.path.lexists(p):
            os.remove(p)
        os.makedirs(p)
    return f


def edita_json(nombre, fn):
    def f(c):
        d = jl(c.p(nombre))
        fn(d)
        json.dump(d, open(c.p(nombre), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return f


def compone(*fs):
    def f(c):
        for x in fs:
            x(c)
    return f


def no_utf8(c):
    open(c.aud, "ab").write(b"\nAviso: inversi\xf3n\n")


# ---------- reproducción de V-1 y V-2 ----------
def g_rep():
    b = base_respuesta()
    G = "rep"
    for via in ("paso14", "pipeline", "ficha", "informe", "resumen"):
        caso(G, "material_trunc", b, escribe("material_auditoria.json", "{trunc"), via)
    for via in ("paso14", "pipeline", "informe", "resumen"):
        caso(G, "ficha_trunc", b, escribe("ficha.json", "{trunc"), via)
    for via in ("paso14", "ficha", "informe", "resumen"):
        caso(G, "estado_lista", b, escribe("estado_pipeline.json", "[]"), via)
        caso(G, "cv_lista", b, escribe("cierre_vigente.json", "[1]"), via)
        caso(G, "material_lista", b, escribe("material_auditoria.json", "[]"), via)
        caso(G, "ficha_lista", b, escribe("ficha.json", "[]"), via)
        caso(G, "ficha_null", b, escribe("ficha.json", "null"), via)
        caso(G, "sols_objeto", b, edita_json("estado_pipeline.json", lambda d: d.update(solicitudes_auditoria={"x": 1})), via)
        caso(G, "resp_texto", b, edita_json("estado_pipeline.json", lambda d: d.update(auditoria_respuesta="x")), via)
    for via in ("paso14", "pipeline", "ficha", "informe", "resumen"):
        caso(G, "estado_carpeta", b, carpeta("estado_pipeline.json"), via)
    for via in ("paso14", "ficha", "informe", "resumen"):
        caso(G, "auditoria_carpeta", b, carpeta("auditoria.md"), via)
        caso(G, "cv_carpeta", b, carpeta("cierre_vigente.json"), via)
        caso(G, "material_carpeta", b, carpeta("material_auditoria.json"), via)
        caso(G, "ficha_carpeta", b, carpeta("ficha.json"), via)


# ---------- ataques nuevos del mismo tipo ----------
def g_nuevos():
    b = base_respuesta()
    G = "nuevos"
    vias4 = ("paso14", "ficha", "informe", "resumen")
    # archivos vacíos
    for via in vias4:
        for f in ("cierre_vigente.json", "material_auditoria.json", "ficha.json", "estado_pipeline.json"):
            caso(G, f"vacio_{f}", b, escribe(f, ""), via)
        caso(G, "auditoria_vacia", b, escribe("auditoria.md", ""), via)
    # material_auditoria.json con tipos internos erróneos
    for via in vias4:
        caso(G, "material_archivos_lista", b, edita_json("material_auditoria.json", lambda d: d.update(archivos=[])), via)
        caso(G, "material_archivos_texto", b, edita_json("material_auditoria.json", lambda d: d.update(archivos="x")), via)
        caso(G, "material_id_numero", b, edita_json("material_auditoria.json", lambda d: d.update(id=5)), via)
        caso(G, "material_sin_id", b, edita_json("material_auditoria.json", lambda d: d.pop("id")), via)
    # cierre_vigente.json con tipos internos erróneos
    for via in vias4:
        caso(G, "cv_fiel_numero", b, edita_json("cierre_vigente.json", lambda d: d.update(auditoria_fiel=1)), via)
        caso(G, "cv_solicitud_lista", b, edita_json("cierre_vigente.json", lambda d: d.update(solicitud=[d.get("solicitud")])), via)
        caso(G, "cv_sha_numero", b, edita_json("cierre_vigente.json", lambda d: d.update(auditoria_sha256=5)), via)
        caso(G, "cv_material_lista", b, edita_json("cierre_vigente.json", lambda d: d.update(material_auditado=[d.get("material_auditado")])), via)
        caso(G, "cv_ficha_sha_lista", b, edita_json("cierre_vigente.json", lambda d: d.update(ficha_sha256=[d.get("ficha_sha256")])), via)
    # ficha.json legible con tipos internos erróneos («cierre» que no es un objeto)
    for via in vias4:
        caso(G, "ficha_cierre_texto", b, edita_json("ficha.json", lambda d: d.update(cierre="APROBADO")), via)
        caso(G, "ficha_cierre_lista", b, edita_json("ficha.json", lambda d: d.update(cierre=[1])), via)
        caso(G, "ficha_escalera_lista", b, edita_json("ficha.json", lambda d: d.update(escalera=[1])), via)
    # estado_pipeline.json con tipos internos erróneos
    for via in vias4:
        caso(G, "estado_sol_pendiente_sin_id", b, edita_json("estado_pipeline.json", lambda d: d["solicitudes_auditoria"].append({"estado": "pendiente"})), via)
        caso(G, "estado_resp_vacia", b, edita_json("estado_pipeline.json", lambda d: d.update(auditoria_respuesta={})), via, esperado="vigente")
        caso(G, "estado_resp_fiel_numero", b, edita_json("estado_pipeline.json", lambda d: d["auditoria_respuesta"].update(fiel=5)), via)
        # con un motivo de retirada legítimo (auditoria.md no UTF-8) y estructuras del estado que usa archivar_salidas
        caso(G, "no_utf8_y_historial_objeto", b, compone(no_utf8, edita_json("estado_pipeline.json", lambda d: d.update(historial={}))), via)
        caso(G, "no_utf8_y_cierres_archivados_texto", b, compone(no_utf8, edita_json("estado_pipeline.json", lambda d: d.update(cierres_archivados="x"))), via)
        caso(G, "no_utf8_y_paso_texto", b, compone(no_utf8, edita_json("estado_pipeline.json", lambda d: d.update(paso="x"))), via)


def g_traversal():
    """material_auditado con «../» en ficha.json: ¿dónde archiva archivar_salidas?"""
    b = base_respuesta()
    G = "traversal"
    for via in ("ficha", "informe", "resumen", "paso14"):
        c, o, out = caso(G, "material_auditado_con_barras", b, edita_json("ficha.json", lambda d: d["cierre"].update(material_auditado="../../../../FUERA_DEL_EXPEDIENTE")), via)
        fuera = os.path.join(c.base, "FUERA_DEL_EXPEDIENTE")
        print(f"       ¿carpeta creada fuera del expediente ({os.path.relpath(fuera, TMP)})? {os.path.isdir(fuera)} · contenido {sorted(os.listdir(fuera)) if os.path.isdir(fuera) else None}")
        RES[-1]["fuera_del_expediente"] = sorted(os.listdir(fuera)) if os.path.isdir(fuera) else None


# ---------- V-3 y el registro sin estado ----------
def crlf(c):
    t = open(c.aud, encoding="utf-8").read()
    open(c.aud, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n"))


def g_v3():
    b = base_respuesta()
    G = "v3"
    c = b.copiar("v3__sin_estado_crlf_restaurar")
    cv0 = jl(c.p("cierre_vigente.json"))
    original = open(c.aud, "rb").read()
    os.remove(c.p("estado_pipeline.json"))
    crlf(c)
    print("CRLF escrito:", b"\r\n" in open(c.aud, "rb").read())
    rc1, out1 = corre("ficha.py", c.d, "--estado", "concluido")
    cv1 = jl(c.p("cierre_vigente.json"))
    open(c.aud, "wb").write(original)
    rc2, out2 = corre("ficha.py", c.d, "--estado", "concluido")
    cv2 = jl(c.p("cierre_vigente.json"))
    k = ("solicitud", "auditoria_fiel", "auditoria_sha256")
    print("cv0", {x: (cv0 or {}).get(x, "")[:16] for x in k})
    print("cv1", {x: (cv1 or {}).get(x, "")[:16] for x in k}, "rc", rc1, (out1.splitlines() or [''])[-1][:100])
    print("cv2", {x: (cv2 or {}).get(x, "")[:16] for x in k}, "rc", rc2, (out2.splitlines() or [''])[-1][:100])
    ok = rc1 == 0 and rc2 == 0 and all((cv1 or {}).get(x) == cv0.get(x) for x in k) and all((cv2 or {}).get(x) == cv0.get(x) for x in k)
    RES.append(dict(grupo=G, caso="sin estado + CRLF + ficha.py, luego bytes originales + ficha.py", via="ficha", esperado="vigente", cumple=ok, rc=[rc1, rc2],
                    cv0={x: cv0.get(x) for x in k}, cv1={x: (cv1 or {}).get(x) for x in k}, cv2={x: (cv2 or {}).get(x) for x in k}))
    # después de restaurar, las otras tres vías siguen dando el cierre por vigente
    # (corrección del auditor, 12:37) sin estado_pipeline.json, pipeline.py arranca en el paso 0 y llega a LibreOffice: no se usa aquí
    for via in ("informe", "resumen"):
        rc, out = VIAS[via](c)
        o = observa(c, rc, out)
        print(f"   tras restaurar · {via}: rc {rc} · traza {o['traza']} · ficha cerrada {o['ficha_cerrada']} · pred {o['pred']} · extra {o['extra']} · {o['ultima'][:90]}")
        RES.append(dict(grupo=G, caso="tras restaurar", via=via, esperado="vigente", cumple=rc == 0 and o["ficha_cerrada"] and not o["traza"], **o))
    # variante: sin estado y en CRLF, por informe.py y resumen.py (sin reescribir el registro)
    for via in ("informe", "resumen"):
        caso(G, "sin_estado_crlf", b, compone(lambda c: os.remove(c.p("estado_pipeline.json")), crlf), via, esperado="vigente")


def g_ficha_ilegible():
    """ficha.json ilegible por ficha.py: ¿la ficha reescrita es vigente después? ¿qué queda en cierre_vigente.json?"""
    b = base_respuesta()
    G = "ficha_ilegible"
    for sin_estado, crlf_antes in ((False, False), (True, False), (True, True)):
        nombre = "con_estado" if not sin_estado else ("sin_estado_crlf" if crlf_antes else "sin_estado")
        c = b.copiar(f"fi__{nombre}")
        cv0 = jl(c.p("cierre_vigente.json"))
        original = open(c.aud, "rb").read()
        if sin_estado:
            os.remove(c.p("estado_pipeline.json"))
        if crlf_antes:
            crlf(c)
        open(c.p("ficha.json"), "w").write("{trunc")
        rc, out = corre("ficha.py", c.d, "--estado", "concluido")
        o = observa(c, rc, out)
        cv1 = jl(c.p("cierre_vigente.json")) or {}
        print(f"{nombre} · ficha.py: rc {rc} · traza {o['traza']} · estado {o['estado']!r}/{o['auditoria']!r} · ficha cerrada {o['ficha_cerrada']} · pred {o['pred']} · extra {o['extra']}")
        for l in out.splitlines():
            print("      |", l[:200])
        print("      cv antes:", {x: str(cv0.get(x))[:16] for x in ("solicitud", "auditoria_fiel", "auditoria_sha256")})
        print("      cv después:", {x: str(cv1.get(x))[:16] for x in ("solicitud", "auditoria_fiel", "auditoria_sha256")})
        o.pop("rc", None)
        r = dict(grupo=G, caso=nombre, via="ficha", rc=rc, cv_antes={x: cv0.get(x) for x in ("solicitud", "auditoria_fiel", "auditoria_sha256")},
                 cv_despues={x: cv1.get(x) for x in ("solicitud", "auditoria_fiel", "auditoria_sha256")}, **o)
        # ¿la ficha reescrita es vigente? informe.py (vía que no la reescribe)
        rc2, out2 = corre("informe.py", c.d)
        o2 = observa(c, rc2, out2)
        print(f"      después · informe.py: rc {rc2} · ficha cerrada {o2['ficha_cerrada']} · {o2['ultima'][:150]}")
        r["despues_informe"] = o2
        if crlf_antes:
            open(c.aud, "wb").write(original)
            rc3, out3 = corre("informe.py", c.d)
            o3 = observa(c, rc3, out3)
            print(f"      tras restaurar los bytes aceptados · informe.py: rc {rc3} · ficha cerrada {o3['ficha_cerrada']} · {o3['ultima'][:160]}")
            r["tras_restaurar_informe"] = o3
        RES.append(r)


def g_simbolicos():
    b = base_respuesta()
    G = "simbolicos"

    def enlace(nombre, destino):
        def f(c):
            p = c.p(nombre)
            if os.path.lexists(p):
                if os.path.isdir(p) and not os.path.islink(p):
                    shutil.rmtree(p)
                else:
                    os.remove(p)
            os.symlink(destino, p)
        return f

    for via in ("paso14", "ficha", "informe", "resumen"):
        caso(G, "estado_roto", b, enlace("estado_pipeline.json", "/nonexistent/estado.json"), via)
        caso(G, "cv_roto", b, enlace("cierre_vigente.json", "/nonexistent/cv.json"), via)
        caso(G, "material_roto", b, enlace("material_auditoria.json", "/nonexistent/m.json"), via)
        caso(G, "ficha_rota", b, enlace("ficha.json", "/nonexistent/ficha.json"), via)
        caso(G, "auditoria_rota", b, enlace("auditoria.md", "/nonexistent/a.md"), via)
        caso(G, "cv_a_dev_null", b, enlace("cierre_vigente.json", "/dev/null"), via)
        caso(G, "auditoria_a_carpeta", b, enlace("auditoria.md", "/home/claude/vigencia2_4_9/tmp/tmpdir"), via)
        caso(G, "material_a_carpeta", b, enlace("material_auditoria.json", "/home/claude/vigencia2_4_9/tmp/tmpdir"), via)
    # la auditoría aceptada servida por un enlace al mismo contenido: sigue vigente (no es un ataque, es una comprobación)
    def enlace_mismo(c):
        dst = os.path.join(c.base, "auditoria_fuera.md")
        shutil.copy2(c.aud, dst)
        os.remove(c.aud)
        os.symlink(dst, c.aud)
    caso(G, "auditoria_enlace_mismo_contenido", b, enlace_mismo, "informe", esperado="vigente")


def g_permisos():
    """Como otro usuario (setpriv), con un archivo de control sin permiso de lectura."""
    global USUARIO
    b = base_respuesta()
    G = "permisos"
    USUARIO = 65534

    def sin_lectura(nombre):
        def f(c):
            subprocess.run(["chmod", "-R", "a+rwX", c.base], check=True)
            os.chmod(c.p(nombre), 0)
        return f

    def todo_rw(c):
        subprocess.run(["chmod", "-R", "a+rwX", c.base], check=True)

    caso(G, "control_sin_cambios_como_otro_usuario", b, todo_rw, "informe", esperado="vigente")
    for via in ("paso14", "ficha", "informe", "resumen"):
        for f in ("estado_pipeline.json", "cierre_vigente.json", "material_auditoria.json", "ficha.json", "auditoria.md", "resultados.json"):
            caso(G, f"sin_lectura_{f}", b, sin_lectura(f), via)
    USUARIO = None


def g_h46():
    """Z-1 sobre el expediente histórico de la 4.6 (en una copia): motivo_rechazo_cierre y huella."""
    import hashlib
    import pipeline
    G = "h46"
    d = os.path.join(TMP, "h46_copia", "Vidrala")
    if os.path.exists(os.path.dirname(d)):
        shutil.rmtree(os.path.dirname(d))
    shutil.copytree(EXP46, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    m = CIE.motivo_rechazo_cierre(d, pipeline.Pipeline.veredicto_auditoria)
    mv = CIE.motivo_vigencia(d, pipeline.Pipeline.veredicto_auditoria)
    print("motivo_rechazo_cierre(copia 4.6):", m)
    print("motivo_vigencia(copia 4.6):", mv)
    print("¿cierre_vigente.json en el original?", os.path.exists(os.path.join(EXP46, "cierre_vigente.json")), "· ¿estado_pipeline.json?", os.path.exists(os.path.join(EXP46, "estado_pipeline.json")))
    st = jl(os.path.join(EXP46, "estado_pipeline.json")) or {}
    print("estado 4.6: auditoria", st.get("auditoria"), "· auditoria_respuesta", st.get("auditoria_respuesta"), "· solicitudes", st.get("solicitudes_auditoria"))
    h = hashlib.sha256(open(os.path.join(EXP46, "auditoria.md"), "rb").read()).hexdigest()
    print("sha256 4.6/Vidrala/auditoria.md:", h)
    RES.append(dict(grupo=G, motivo_rechazo=m, motivo_vigencia=mv, sha_auditoria=h))


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    grupos = {"rep": g_rep, "nuevos": g_nuevos, "traversal": g_traversal, "v3": g_v3, "ficha_ilegible": g_ficha_ilegible, "simbolicos": g_simbolicos,
              "permisos": g_permisos, "h46": g_h46}
    for g in sys.argv[1:]:
        grupos[g]()
    salida = f"/home/claude/vigencia2_4_9/tmp/ejecuciones/ataques_{'_'.join(sys.argv[1:])}.json"
    json.dump(RES, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    n = sum(1 for r in RES if "cumple" in r)
    print(f"\n{sum(1 for r in RES if r.get('cumple'))} de {n} casos con el resultado esperado · {salida}")
