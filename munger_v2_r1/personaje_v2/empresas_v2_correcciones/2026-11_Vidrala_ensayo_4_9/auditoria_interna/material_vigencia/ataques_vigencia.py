#!/usr/bin/env python3
"""Control de vigencia 4.9 · ataques propios contra Z-1, Z-2 y la función B (huella_fiel, motivo_respuesta_no_aceptada).
Uso: python3 -I -B ataques_vigencia.py [ataque ...]
Solo trabaja en /home/claude/vigencia_4_9/tmp/escenarios/ (copias). Solo ejecuta pipeline.py --desde 13/14 (y sin --desde
partiendo de un estado en el paso 13/14), ficha.py, informe.py y resumen.py, que no recalculan. No modifica la copia auditada."""
import csv, hashlib, json, os, shutil, subprocess, sys, unicodedata

RAIZ = "/home/claude/vigencia_4_9/munger_v2_r1/personaje_v2"
SCR = os.environ.get("SCR_VIGENCIA") or os.path.join(RAIZ, "scripts")
EXP = os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
BASE = os.environ.get("BASE_VIGENCIA") or "/home/claude/vigencia_4_9/tmp/escenarios"
SAL = "/home/claude/vigencia_4_9/tmp/ejecuciones"
sys.path.insert(0, SCR); sys.path.insert(0, os.path.join(RAIZ, "pruebas"))
sys.dont_write_bytecode = True
import cierre_v2 as CIE  # noqa
import agentes_sinteticos as AG  # noqa

EMPRESA = "Vidrala, S.A."
FRASE = "Aviso: Control de vigencia: la reposición está acreditada y el crecimiento no. (auditoría sintética del control de vigencia)"
PY = sys.executable
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": "/home/claude/vigencia_4_9/tmp/tmpdir"}
LOG = []


def corre(script, *a):
    r = subprocess.run([PY, "-I", "-B", os.path.join(SCR, script), *a], capture_output=True, text=True, env=ENV)
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out


def filas(p):
    if not os.path.isfile(p):
        return []
    return [(r.get("verificacion") or "")[:24] for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == EMPRESA]


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def _preparar(b):
    d = os.path.join(b, "exp", "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(b, "exp", f))
    os.makedirs(os.path.join(b, "otro"))
    return d


def base_hist():
    """Cierre de la 4.6.1 tal cual (sin solicitudes), publicado también en un destino configurado."""
    b = os.path.join(BASE, "_hist")
    if os.path.exists(os.path.join(b, "LISTO")):
        return b
    shutil.rmtree(b, ignore_errors=True)
    d = _preparar(b)
    rc = corre("resumen.py", d, os.path.join(b, "otro", "resumen_configurado.csv"))[0]
    LOG.append(("base_hist resumen extra", rc))
    open(os.path.join(b, "LISTO"), "w").write("ok")
    return b


def base_resp():
    """Cierre de la 4.9: --desde 13 sobre la 4.6.1, respuesta sintética válida con otra frase, cierre y publicación extra."""
    b = os.path.join(BASE, "_resp")
    if os.path.exists(os.path.join(b, "LISTO")):
        return b
    shutil.rmtree(b, ignore_errors=True)
    d = _preparar(b)
    r13 = corre("pipeline.py", d, "--desde", "13")[0]
    AG.auditoria(d, "APROBADO")
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write(FRASE + "\n")
    rc = corre("pipeline.py", d)[0]
    rr = corre("resumen.py", d, os.path.join(b, "otro", "resumen_configurado.csv"))[0]
    LOG.append(("base_resp", r13, rc, rr))
    assert (r13, rc, rr) == (10, 0, 0), (r13, rc, rr)
    open(os.path.join(b, "LISTO"), "w").write("ok")
    return b


def copia(base, nombre):
    n = os.path.join(BASE, nombre)
    shutil.rmtree(n, ignore_errors=True)
    shutil.copytree(base, n, symlinks=True)
    return n, os.path.join(n, "exp", "Vidrala")


def estado(n, d):
    try:
        st = json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8"))
        st = st if isinstance(st, dict) else {"_no_objeto": repr(st)[:20]}
    except (OSError, ValueError):
        st = {"_ilegible": True} if os.path.exists(os.path.join(d, "estado_pipeline.json")) else {}
    try:
        F = json.load(open(os.path.join(d, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "ficha.json")) else None
    except ValueError:
        F = "ilegible"
    hist = os.path.join(d, "historial_cierres")
    return {"estado": st.get("estado_analisis", st.get("_ilegible") and "ILEGIBLE"), "auditoria": st.get("auditoria"),
            "ficha": None if F is None else ("ilegible" if F == "ilegible" else ("cerrada" if F.get("cierre") else "sin cierre")),
            "cierre_vigente": os.path.exists(os.path.join(d, "cierre_vigente.json")),
            "n_hist": len(os.listdir(hist)) if os.path.isdir(hist) else 0,
            "pred": filas(os.path.join(n, "exp", "resumen_v2.csv")), "extra": filas(os.path.join(n, "otro", "resumen_configurado.csv"))}


VIAS = {"paso14": lambda n, d: corre("pipeline.py", d, "--desde", "14"),
        "sin_desde": lambda n, d: corre("pipeline.py", d),
        "ficha": lambda n, d: corre("ficha.py", d, "--estado", "concluido"),
        "informe": lambda n, d: corre("informe.py", d),
        "resumen": lambda n, d: corre("resumen.py", d, os.path.join(n, "exp", "resumen_v2.csv"))}
CUATRO = ("paso14", "ficha", "informe", "resumen")


def ult(out):
    ls = [l for l in out.splitlines() if l.strip()]
    tb = next((l for l in reversed(ls) if l.startswith(("Traceback", "  File"))), None)
    return {"ultima": (ls[-1] if ls else "")[:220], "traza": "Traceback" in out, "excepcion": (ls[-1][:160] if "Traceback" in out else None)}


def registra(nombre, via, rc, n, d, extra=None):
    e = {"ataque": nombre, "via": via, "rc": rc, **estado(n, d), **(extra or {})}
    print(json.dumps(e, ensure_ascii=False), flush=True)
    return e


def otra_aprobacion(d, solicitud=False, aviso="Aviso: otra auditoría sintética del control de vigencia, que no es la aprobada."):
    if os.path.exists(os.path.join(d, "solicitud_auditoria.json")):
        os.remove(os.path.join(d, "solicitud_auditoria.json"))
    AG.auditoria(d, "APROBADO", solicitud=solicitud)
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write(aviso + "\n")


def huellas_en_arbol(d, h):
    """Rutas de cierre_vigente.json (también archivados) que registran la huella h."""
    r = []
    for raiz, _, fs in os.walk(d):
        for f in fs:
            if f == "cierre_vigente.json":
                try:
                    if json.load(open(os.path.join(raiz, f), encoding="utf-8")).get("auditoria_sha256") == h:
                        r.append(os.path.relpath(os.path.join(raiz, f), d))
                except (ValueError, AttributeError):
                    pass
    return r


# ---------------- Z-1 ----------------
def ataque_z1():
    res = []
    hb = base_hist()
    # a) reproducción del caso pedido, con una aprobación distinta de la de la batería (con una línea de solicitud inventada)
    for v in CUATRO:
        n, d = copia(hb, f"z1a_{v}")
        os.remove(os.path.join(d, "cierre_vigente.json"))
        otra_aprobacion(d, solicitud="SA-00000000deadbeef")
        h = sha(os.path.join(d, "auditoria.md"))
        rc, out = VIAS[v](n, d)
        res.append(registra("Z1a 4.6.1 sin cierre_vigente.json, otra APROBADO (con solicitud inventada)", v, rc, n, d,
                            {"huella_atribuida_en": huellas_en_arbol(d, h), **ult(out)}))
    # b) la misma auditoría original (legítima) sin cierre_vigente.json: ¿se vuelve a cerrar?
    for v in ("ficha", "paso14"):
        n, d = copia(hb, f"z1b_{v}")
        os.remove(os.path.join(d, "cierre_vigente.json"))
        h = sha(os.path.join(d, "auditoria.md"))
        rc, out = VIAS[v](n, d)
        res.append(registra("Z1b 4.6.1 sin cierre_vigente.json, auditoría original", v, rc, n, d, {"huella_atribuida_en": huellas_en_arbol(d, h), **ult(out)}))
    # c) cierre_vigente.json legible pero vacío ({}), o sin auditoria_sha256, o solo con auditoria_fiel
    for etiqueta, cv in (("{}", {}), ("auditoria_sha256 null", "null_sha"), ("solo auditoria_fiel sin solicitud", "solo_fiel")):
        n, d = copia(hb, f"z1c_{len(res)}")
        p = os.path.join(d, "cierre_vigente.json")
        c0 = json.load(open(p, encoding="utf-8"))
        if cv == "null_sha":
            c0["auditoria_sha256"] = None; cv = c0
        elif cv == "solo_fiel":
            c0["auditoria_fiel"] = CIE.huella_fiel(b"x"); c0.pop("auditoria_sha256"); cv = c0
        json.dump(cv, open(p, "w", encoding="utf-8"))
        otra_aprobacion(d)
        h = sha(os.path.join(d, "auditoria.md"))
        rc, out = VIAS["ficha"](n, d)
        res.append(registra(f"Z1c 4.6.1 cierre_vigente.json = {etiqueta}, otra APROBADO", "ficha", rc, n, d, {"huella_atribuida_en": huellas_en_arbol(d, h), **ult(out)}))
    rb = base_resp()
    # d) 4.9: estado legible sin auditoria_respuesta (clave borrada) y sin cierre_vigente.json, otra APROBADO
    for v in ("ficha", "paso14", "resumen"):
        n, d = copia(rb, f"z1d_{v}")
        p = os.path.join(d, "estado_pipeline.json")
        st = json.load(open(p, encoding="utf-8")); st.pop("auditoria_respuesta", None)
        json.dump(st, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        os.remove(os.path.join(d, "cierre_vigente.json"))
        otra_aprobacion(d)
        h = sha(os.path.join(d, "auditoria.md"))
        rc, out = VIAS[v](n, d)
        res.append(registra("Z1d 4.9 estado sin auditoria_respuesta y sin cierre_vigente.json, otra APROBADO", v, rc, n, d, {"huella_atribuida_en": huellas_en_arbol(d, h), **ult(out)}))
    # e) 4.9: estado_pipeline.json = null (JSON válido), sin cierre_vigente.json
    n, d = copia(rb, "z1e")
    open(os.path.join(d, "estado_pipeline.json"), "w").write("null")
    os.remove(os.path.join(d, "cierre_vigente.json"))
    otra_aprobacion(d)
    h = sha(os.path.join(d, "auditoria.md"))
    rc, out = VIAS["ficha"](n, d)
    res.append(registra("Z1e 4.9 estado_pipeline.json = null y sin cierre_vigente.json, otra APROBADO", "ficha", rc, n, d, {"huella_atribuida_en": huellas_en_arbol(d, h), **ult(out)}))
    # f) 4.9 --reiniciar (borra el estado) y cierre_vigente.json borrado, otra APROBADO por el paso 14
    n, d = copia(rb, "z1f")
    os.remove(os.path.join(d, "cierre_vigente.json"))
    otra_aprobacion(d)
    rc, out = corre("pipeline.py", d, "--reiniciar", "--desde", "14")
    res.append(registra("Z1f 4.9 --reiniciar --desde 14 sin cierre_vigente.json, otra APROBADO", "pipeline --reiniciar --desde 14", rc, n, d, ult(out)))
    # g) límite declarado: reescritura de DOS archivos (4.6.1: auditoria.md + cierre_vigente.json con la huella nueva)
    n, d = copia(hb, "z1g")
    otra_aprobacion(d)
    p = os.path.join(d, "cierre_vigente.json")
    c0 = json.load(open(p, encoding="utf-8")); c0["auditoria_sha256"] = sha(os.path.join(d, "auditoria.md"))
    json.dump(c0, open(p, "w", encoding="utf-8"))
    rc, out = VIAS["paso14"](n, d)
    res.append(registra("Z1g 4.6.1 auditoria.md y cierre_vigente.json reescritos (2 archivos)", "paso14", rc, n, d, ult(out)))
    # h) límite declarado en la 4.9: estado borrado + cierre_vigente.json con la solicitud y la huella fiel de otra auditoría
    n, d = copia(rb, "z1h")
    os.remove(os.path.join(d, "estado_pipeline.json"))
    sid = json.load(open(os.path.join(d, "cierre_vigente.json"), encoding="utf-8"))["solicitud"]
    otra_aprobacion(d, solicitud=sid)
    p = os.path.join(d, "cierre_vigente.json")
    c0 = json.load(open(p, encoding="utf-8")); c0["auditoria_fiel"] = CIE.huella_fiel(open(os.path.join(d, "auditoria.md"), "rb").read())
    json.dump(c0, open(p, "w", encoding="utf-8"))
    rc, out = VIAS["ficha"](n, d)
    res.append(registra("Z1h 4.9 estado borrado + cierre_vigente.json con la huella fiel de otra auditoría (2 archivos)", "ficha", rc, n, d, ult(out)))
    return res


# ---------------- Z-2 ----------------
def _z2(base, nombre, mutar, vias):
    res = []
    for v in vias:
        n, d = copia(base, f"z2_{nombre}_{v}")
        mutar(d)
        rc, out = VIAS[v](n, d)
        res.append(registra(f"Z2 {nombre}", v, rc, n, d, ult(out)))
    return res


def w(d, f, contenido, modo="w"):
    p = os.path.join(d, f)
    if modo == "wb":
        open(p, "wb").write(contenido)
    else:
        open(p, "w", encoding="utf-8").write(contenido)


def ataque_z2():
    rb = base_resp()
    R = []
    TODAS = ("paso14", "sin_desde", "ficha", "informe", "resumen")
    # casos no cubiertos por la batería
    R += _z2(rb, "cierre_vigente_ilegible", lambda d: w(d, "cierre_vigente.json", "{trunc"), ("paso14", "resumen"))
    R += _z2(rb, "estado_ilegible", lambda d: w(d, "estado_pipeline.json", "{trunc"), ("sin_desde", "informe", "resumen"))
    R += _z2(rb, "estado_con_BOM", lambda d: w(d, "estado_pipeline.json", b"\xef\xbb\xbf" + open(os.path.join(d, "estado_pipeline.json"), "rb").read(), "wb"), ("paso14", "ficha"))
    R += _z2(rb, "estado_no_utf8", lambda d: w(d, "estado_pipeline.json", open(os.path.join(d, "estado_pipeline.json"), "rb").read().replace(b"\xc3\xb3", b"\xf3"), "wb"), ("paso14", "ficha"))
    R += _z2(rb, "auditoria_utf16_sin_BOM", lambda d: w(d, "auditoria.md", open(os.path.join(d, "auditoria.md"), encoding="utf-8").read().encode("utf-16-le"), "wb"), ("paso14", "resumen"))
    R += _z2(rb, "auditoria_surrogate", lambda d: w(d, "auditoria.md", open(os.path.join(d, "auditoria.md"), "rb").read() + b"\xed\xa0\x80\n", "wb"), ("ficha",))
    # JSON válido que no es un objeto
    R += _z2(rb, "estado_lista", lambda d: w(d, "estado_pipeline.json", "[]"), TODAS)
    R += _z2(rb, "cierre_vigente_lista", lambda d: w(d, "cierre_vigente.json", "[1]"), ("paso14", "ficha", "informe", "resumen"))

    def sol_dict(d):
        p = os.path.join(d, "estado_pipeline.json"); st = json.load(open(p, encoding="utf-8"))
        st["solicitudes_auditoria"] = {"x": 1}; json.dump(st, open(p, "w", encoding="utf-8"))
    R += _z2(rb, "estado_solicitudes_no_lista", sol_dict, ("paso14", "ficha"))

    def resp_str(d):
        p = os.path.join(d, "estado_pipeline.json"); st = json.load(open(p, encoding="utf-8"))
        st["auditoria_respuesta"] = "SA-x"; json.dump(st, open(p, "w", encoding="utf-8"))
    R += _z2(rb, "estado_respuesta_no_objeto", resp_str, ("ficha",))
    # otros archivos de control y salidas oficiales
    R += _z2(rb, "estado_es_carpeta", lambda d: (os.remove(os.path.join(d, "estado_pipeline.json")), os.makedirs(os.path.join(d, "estado_pipeline.json"))), ("sin_desde", "paso14", "ficha"))
    R += _z2(rb, "material_auditoria_ilegible", lambda d: w(d, "material_auditoria.json", "{trunc"), ("paso14", "ficha", "informe", "resumen"))
    R += _z2(rb, "ficha_ilegible", lambda d: w(d, "ficha.json", "{trunc"), ("paso14", "ficha", "informe", "resumen"))
    R += _z2(rb, "auditoria_es_carpeta", lambda d: (os.remove(os.path.join(d, "auditoria.md")), os.makedirs(os.path.join(d, "auditoria.md"))), ("ficha",))
    # estado ilegible con un destino inaccesible: el encargo dice código 5
    for v in ("paso14", "sin_desde"):
        n, d = copia(rb, f"z2_estado_ilegible_destino_inaccesible_{v}")
        x = os.path.join(n, "otro", "resumen_configurado.csv"); os.remove(x); os.makedirs(x)
        w(d, "estado_pipeline.json", "{trunc")
        rc, out = VIAS[v](n, d)
        R.append(registra("Z2 estado_ilegible + destino configurado inaccesible", v, rc, n, d, ult(out)))
    return R


# ---------------- función B ----------------
def _b(nombre, mut, vias=("paso14",)):
    rb = base_resp()
    res = []
    for v in vias:
        n, d = copia(rb, f"b_{nombre}_{v}")
        p = os.path.join(d, "auditoria.md")
        antes = open(p, "rb").read()
        nuevo = mut(antes)
        open(p, "wb").write(nuevo)
        resp = (json.load(open(os.path.join(d, "estado_pipeline.json"), encoding="utf-8")).get("auditoria_respuesta") or {})
        igual_fiel = CIE.huella_fiel(nuevo) == resp.get("fiel")
        rc, out = VIAS[v](n, d)
        res.append(registra(f"B {nombre}", v, rc, n, d, {"huella_fiel_igual": igual_fiel, **ult(out)}))
    return res


def ataque_b():
    R = []
    T = lambda f: (lambda b: f(b.decode("utf-8")).encode("utf-8"))  # noqa
    # NFC «singletons»: equivalencias canónicas que cambian el carácter visible (dentro de lo declarado como inocuo)
    R += _b("acento_grave_por_U+1FEF", T(lambda t: t.replace("Aviso:", "`Aviso`:")), ("paso14",))
    R += _b("punto_medio_por_U+0387", T(lambda t: t.replace("·", "·")), ("paso14",))
    R += _b("ohmio_U+2126_y_angstrom_U+212B", T(lambda t: t + "Ω Å\n"), ("paso14",))
    R += _b("combinantes_reordenados", T(lambda t: t + "ạ́\n"), ("paso14",))
    # saltos y espacios no declarados
    R += _b("CR_CR_LF_intermedio", lambda b: b.replace(b"\n", b"\r\r\n", 1), ("paso14",))
    R += _b("LF_CR_al_final", lambda b: b.rstrip(b"\n") + b"\n\r\n\r", ("paso14",))
    R += _b("NEL_U+0085_antes_de_la_solicitud", T(lambda t: t.replace("\nSolicitud de auditoría", "\u0085Solicitud de auditoría")), ("paso14", "ficha"))
    R += _b("FF_al_final", lambda b: b + b"\x0c", ("paso14",))
    R += _b("espacio_y_salto_al_final", lambda b: b + b" \n", ("paso14",))
    R += _b("tabulador_por_espacio", T(lambda t: t.replace("VEREDICTO: ", "VEREDICTO:\t")), ("paso14",))
    # la línea de solicitud
    R += _b("solicitud_en_mayusculas_hex", T(lambda t: __import__("re").sub(r"SA-([0-9a-f]{16})", lambda m: "SA-" + m.group(1).upper(), t)), ("paso14", "resumen"))
    R += _b("solicitud_rotulo_en_mayusculas", T(lambda t: t.replace("Solicitud de auditoría:", "SOLICITUD DE AUDITORÍA:")), ("paso14",))
    R += _b("solicitud_sin_tilde", T(lambda t: t.replace("Solicitud de auditoría:", "Solicitud de auditoria:")), ("paso14",))
    R += _b("solicitud_en_negrita", T(lambda t: __import__("re").sub(r"(Solicitud de auditoría: SA-[0-9a-f]{16})", r"**\1**", t)), ("ficha",))
    R += _b("solicitud_en_cita", T(lambda t: t.replace("Solicitud de auditoría:", "> Solicitud de auditoría:")), ("paso14",))
    R += _b("solicitud_tras_ZWSP", T(lambda t: t.replace("Solicitud de auditoría:", "​Solicitud de auditoría:")), ("paso14",))
    R += _b("solicitud_duplicada_en_bloque_de_codigo", T(lambda t: t + "```\n" + [l for l in t.splitlines() if l.startswith("Solicitud")][0] + "\n```\n"), ("paso14",))
    # BOM UTF-8 con NFD con CR y BOM interior... (combinadas) y texto vacío
    R += _b("bom_cr_nfd_saltos_finales", lambda b: b"\xef\xbb\xbf" + unicodedata.normalize("NFD", b.decode("utf-8")).replace("\n", "\r").encode("utf-8") + b"\r\r\r", ("paso14", "ficha", "informe", "resumen"))
    R += _b("archivo_vacio", lambda b: b"", ("ficha",))
    # el material: la misma respuesta, otro identificador de material en minúsculas/mayúsculas
    R += _b("material_en_mayusculas", T(lambda t: __import__("re").sub(r"Material auditado: ([0-9a-f]{16})", lambda m: "Material auditado: " + m.group(1).upper(), t)), ("paso14",))
    return R


def ataque_b_estado():
    """Manipulaciones del estado sin tocar auditoria.md (función B)."""
    rb = base_resp()
    R = []

    def st_mut(nombre, f, v="paso14"):
        n, d = copia(rb, f"be_{nombre}")
        p = os.path.join(d, "estado_pipeline.json"); st = json.load(open(p, encoding="utf-8")); f(st, d)
        json.dump(st, open(p, "w", encoding="utf-8"), ensure_ascii=False)
        rc, out = VIAS[v](n, d)
        R.append(registra(f"B-estado {nombre}", v, rc, n, d, ult(out)))

    st_mut("fiel_vacio_y_bytes_iguales", lambda st, d: st["auditoria_respuesta"].update(fiel=""))
    def crlf(d):
        p = os.path.join(d, "auditoria.md"); b = open(p, "rb").read()  # (corregido: leer antes de abrir para escribir)
        open(p, "wb").write(b.replace(b"\n", b"\r\n"))
    st_mut("fiel_vacio_tras_CRLF", lambda st, d: (st["auditoria_respuesta"].update(fiel=""), crlf(d)))
    st_mut("material_de_la_respuesta_cambiado", lambda st, d: st["auditoria_respuesta"].update(material="0" * 16))
    st_mut("solicitud_duplicada_en_estado_otra_pendiente", lambda st, d: st["solicitudes_auditoria"].append({**[s for s in st["solicitudes_auditoria"] if s["id"] == st["auditoria_respuesta"]["solicitud"]][0], "estado": "pendiente"}))
    st_mut("solicitud_duplicada_en_estado_otra_respondida_por_otra", lambda st, d: st["solicitudes_auditoria"].insert(0, {**[s for s in st["solicitudes_auditoria"] if s["id"] == st["auditoria_respuesta"]["solicitud"]][0], "respuesta_sha256": "0" * 64}))
    st_mut("auditoria_registrada_None", lambda st, d: st.update(auditoria=None))
    return R


def ataque_registrar_cierre():
    """Tras un nuevo cierre de ficha.py sin estado (respuesta en CRLF, vigente por huella fiel): ¿qué registra cierre_vigente.json?"""
    rb = base_resp()
    n, d = copia(rb, "rc_sin_estado_crlf")
    cv0 = json.load(open(os.path.join(d, "cierre_vigente.json"), encoding="utf-8"))
    os.remove(os.path.join(d, "estado_pipeline.json"))
    p = os.path.join(d, "auditoria.md"); orig = open(p, "rb").read()
    open(p, "wb").write(orig.replace(b"\n", b"\r\n"))
    # ficha.py sustituye la ficha (cambia el estado leído: sin estado) o la reescribe igual: se observa cierre_vigente.json
    rc, out = VIAS["ficha"](n, d)
    cv1 = json.load(open(os.path.join(d, "cierre_vigente.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "cierre_vigente.json")) else None
    R = [registra("RC ficha.py sin estado y con CRLF", "ficha", rc, n, d, {"cv_antes": {k: cv0.get(k) and str(cv0.get(k))[:16] for k in ("auditoria_sha256", "solicitud", "auditoria_fiel")},
                                                                           "cv_despues": cv1 and {k: cv1.get(k) and str(cv1.get(k))[:16] for k in ("auditoria_sha256", "solicitud", "auditoria_fiel")},
                                                                           "sha_actual": sha(p)[:16], **ult(out)})]
    # luego se restaura el archivo original con LF (inocuo respecto a la respuesta aceptada)
    open(p, "wb").write(orig)
    rc2, out2 = VIAS["ficha"](n, d)
    R.append(registra("RC después: respuesta original restaurada (LF)", "ficha", rc2, n, d, ult(out2)))
    return R


ATAQUES = {"z1": ataque_z1, "z2": ataque_z2, "b": ataque_b, "b_estado": ataque_b_estado, "registrar_cierre": ataque_registrar_cierre}

if __name__ == "__main__":
    os.makedirs(BASE, exist_ok=True)
    sel = sys.argv[1:] or list(ATAQUES)
    todo = {}
    for a in sel:
        todo[a] = ATAQUES[a]()
    suf = os.environ.get("SUFIJO_VIGENCIA", "")
    json.dump({"bases": LOG, **todo}, open(os.path.join(SAL, f"ataques_vigencia{suf}_{'_'.join(sel)}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
