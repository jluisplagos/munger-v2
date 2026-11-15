#!/usr/bin/env python3
"""Batería de solicitudes de auditoría (entrega 4.8.1, encargo §2: R-T1). Solo trabaja en directorios temporales: no modifica el
expediente de referencia ni el código del árbol.

Uso: python3 -B pruebas/test_auditorias_v2.py [--expediente <carpeta Vidrala aprobada de la 4.6.1>]

**El defecto (4.8).** El paso 13 aceptaba como respuesta cualquier auditoria.md cuya fecha de modificación fuera posterior a la
anotada al consumirla. Tras provocar X-c, restaurar el esquema y relanzar desde el 13, el resultado dependía de cómo se hubieran
descomprimido las fechas: con las del ZIP en CET se pedía una auditoría nueva (código 10); interpretadas en UTC, o renovadas, se
reutilizaba la misma auditoría y se cerraba concluido/APROBADO.

**Cómo prueba esta batería que no depende de las fechas.** Fija ella misma las fechas de la copia en tres modos, sea cual sea la
zona horaria con la que se descomprimió el paquete:
  - cet: las fechas del ZIP leídas en CET; auditoria.md tiene la fecha anotada al consumirla, truncada a 2 s como en el formato DOS;
  - utc: las mismas fechas una hora después, como si las fechas DOS se leyeran en UTC;
  - renovadas: todas las fechas, ahora.

**Grupos.** Observan la primera ejecución: código, última línea, estado_pipeline.json, solicitud, prompt, ESPERANDO.md, ficha,
informe, diagnóstico, fila e historial del resumen.
  A. En los tres modos: X-c (esquema roto, `--desde 14`), esquema restaurado y `--desde 13` directo. Se pide una auditoría nueva.
  B. En los tres modos: X-c, intento intermedio con `--desde 14` (cierre rechazado), y después `--desde 13`. Se pide una auditoría nueva.
  C. Relanzamientos mientras la respuesta sigue pendiente (sin `--desde`, con `--desde 13`, informe antiguo con fecha reciente y
     `--desde 14`): la solicitud es siempre la misma y no se cierra nada.
  D. Respuestas que no valen:
     - informe antiguo reescrito, y con la línea de la solicitud vigente añadida y otro formato (mismo contenido: puntuación, Unicode,
       tildes, orden y corte de las líneas);
     - auditoría nueva sin línea de solicitud, con una solicitud equivocada o con dos líneas;
     - material distinto: se pide una corrección con una solicitud nueva;
     - auditoría que incumple H2: REPETIR y vuelta a la fase C.
  E. En los tres modos: respuesta válida a la solicitud vigente y cierre correcto. Después:
     - relanzamientos sin cambios;
     - sustitución de auditoria.md por el informe antiguo: se rechaza.
  H. Vías que encontró la auditoría interna: penúltima respuesta reutilizada; registro persistente sin el estado de las solicitudes;
     ficha.py con una solicitud pendiente; --desde 13 sobre un cierre vigente; cambio de material con la solicitud pendiente; la
     respuesta registrada guardada con CRLF; una REPETIR repetida (se acepta: no cierra nada); cierre anterior a la 4.8.1 con auditoria.md
     sustituida.
  I. Vías del control de vigencia y de la tercera revisión: auditorías históricas con mayúscula, con otra extensión, en una subcarpeta,
     en cp1252, en UTF-16 o con relleno de más de 2 MB; respuesta que no es UTF-8 válido; registro ilegible o con tipos inválidos.
  F. Cierre histórico sin solicitudes (4.6.1), relanzado sin `--desde` y con `--desde 14`: sigue vigente y no se le asigna
     ninguna solicitud.
  G. La regla H2 (Pipeline.veredicto_auditoria) es idéntica a la de la 4.7.1.
"""
import argparse
import csv
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import textwrap
import time
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SCR = os.path.join(RAIZ, "scripts")
sys.path.insert(0, SCR)
sys.path.insert(0, AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

PY = sys.executable
PIPE = os.path.join(SCR, "pipeline.py")
TMP = tempfile.mkdtemp(prefix="auditorias481_")
EMPRESA = "Vidrala, S.A."
MATERIAL = "74b94f8072dd58c1"
H2_SHA_4_7_1 = "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422"
MODOS = ("cet", "utc", "renovadas")
SA = re.compile(r"SA-[0-9a-f]{16}")
R = []


def paso(grupo, nombre, ok, detalle=""):
    R.append((grupo, nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + f" · {grupo} · {nombre}" + (f" · {detalle}" if detalle else ""))


def j(c, f):
    p = os.path.join(c, f)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def leer(c, f):
    p = os.path.join(c, f)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def copia(exp, nombre, modo):
    base = os.path.join(TMP, nombre, "exp")
    d = os.path.join(base, "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(exp), f)):
            shutil.copy2(os.path.join(os.path.dirname(exp), f), os.path.join(base, f))
    fechas(base, d, modo)
    return d


def fechas(base, d, modo):
    """Fija las fechas de toda la copia en el modo pedido, con independencia de la zona horaria de la descompresión."""
    todos = [os.path.join(r, f) for r, _, fs in os.walk(base) for f in fs]
    if modo == "renovadas":
        t = time.time()
        for p in todos:
            os.utime(p, (t, t))
        return
    consumido = (j(d, "estado_pipeline.json") or {}).get("consumidos", {}).get("auditoria.md")
    objetivo = (int(consumido) // 2) * 2 + (3600 if modo == "utc" else 0)
    delta = objetivo - os.path.getmtime(os.path.join(d, "auditoria.md"))
    for p in todos:
        mt = os.path.getmtime(p) + delta
        os.utime(p, (mt, mt))


def corre(d, *extra, pipe=PIPE):
    r = subprocess.run([PY, "-B", pipe, d, *extra], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out, (out.splitlines() or [""])[-1]


def filas(d):
    p = os.path.join(os.path.dirname(d), "resumen_v2.csv")
    return [r for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == EMPRESA] if os.path.exists(p) else []


def historial_resumen(d):
    p = os.path.join(os.path.dirname(d), "resumen_v2_historial.csv")
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def aprobacion_en_historial(d):
    return any(r.get("estado_analisis") == "concluido" and r.get("verificacion") == "APROBADO" and r.get("material_auditado") == MATERIAL for r in historial_resumen(d))


def solicitudes(d):
    return (j(d, "estado_pipeline.json") or {}).get("solicitudes_auditoria") or []


def pendientes(d):
    return [s for s in solicitudes(d) if s.get("estado") == "pendiente"]


CODIGO_ROTO = {}


def codigo_con_esquema_roto():
    if CODIGO_ROTO:
        return CODIGO_ROTO["pipe"]
    raiz = os.path.join(TMP, "codigo_roto")
    os.makedirs(raiz)
    shutil.copytree(RAIZ, os.path.join(raiz, "personaje_v2"),
                    ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(os.path.dirname(RAIZ), x), os.path.join(raiz, x))
    esq = os.path.join(raiz, "personaje_v2", "esquema", "ficha.esquema.json")
    e = json.load(open(esq, encoding="utf-8"))
    e["required"] = list(e["required"]) + ["campo_inexistente_xc"]
    json.dump(e, open(esq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    CODIGO_ROTO["pipe"] = os.path.join(raiz, "personaje_v2", "scripts", "pipeline.py")
    return CODIGO_ROTO["pipe"]


def provocar_xc(d):
    rc, _, ult = corre(d, "--desde", "14", pipe=codigo_con_esquema_roto())
    return rc == 0 and ult.startswith("estado final: no_entregable · paso 14") and (j(d, "estado_pipeline.json") or {}).get("auditoria") is None


def espera_auditoria_nueva(d, rc, ult, n_solicitudes=1):
    """Comprobaciones comunes de «se pide una auditoría nueva»; devuelve (ok, detalle)."""
    st = j(d, "estado_pipeline.json") or {}
    sol = j(d, "solicitud_auditoria.json") or {}
    pend = pendientes(d)
    prompt = leer(d, os.path.join("prompts_generados", "13_verificacion.md"))
    esp = leer(d, "ESPERANDO.md")
    fi = j(d, "ficha.json") or {}
    f = filas(d)
    ok = (rc == 10 and "ESPERANDO" in ult and "auditoria.md" in ult and len(pend) == 1 and len(solicitudes(d)) == n_solicitudes
          and pend[0]["id"] == sol.get("id") and pend[0]["material"] == st.get("material_auditoria") == (CIE.material_fijado(d) or {}).get("id")
          and pend[0]["id"] in prompt and f"Solicitud de auditoría: {pend[0]['id']}" in prompt and pend[0]["id"] in esp and "NO aceptada" in esp
          and st.get("auditoria") is None and st.get("estado_analisis") is None and st.get("paso") == 13 and st.get("esperando") == "13:auditoria.md"
          and not fi.get("cierre") and not os.path.exists(os.path.join(d, "cierre_vigente.json")) and "APROBADO del material" not in leer(d, "informe.md")
          and not any("APROBADO" == (r.get("verificacion") or "") for r in f) and aprobacion_en_historial(d)
          and any(pend[0]["id"] in h and "registrada" in h for h in st.get("historial") or []))
    det = f"código {rc} · {ult[:110]} · solicitudes {[(s['id'][:10], s['estado']) for s in solicitudes(d)]} · auditoría {st.get('auditoria')!r} · estado {st.get('estado_analisis')!r} · paso {st.get('paso')}"
    return ok, det


def grupo_a(exp):
    G = "A X-c, esquema restaurado y --desde 13 directo"
    for modo in MODOS:
        d = copia(exp, f"a_{modo}", modo)
        xc = provocar_xc(d)
        rc, out, ult = corre(d, "--desde", "13")
        ok, det = espera_auditoria_nueva(d, rc, ult)
        dg_ant = j(d, "diagnostico.json.anterior") or {}
        paso(G, f"[{modo}] primera ejecución: código 10, solicitud nueva registrada y nombrada en el prompt, sin cierre ni aprobación vigente; diagnóstico X-c como antecedente",
             xc and ok and dg_ant.get("estado_analisis") == "no_entregable" and not os.path.exists(os.path.join(d, "diagnostico.json")), det)
        st = j(d, "estado_pipeline.json") or {}
        paso(G, f"[{modo}] el informe antiguo no se acepta y su huella queda anotada como ya usada, sin asignarle ninguna solicitud",
             (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", "").startswith("auditoria.md es una auditoría ya usada (su huella SHA-256")
             and sha(os.path.join(d, "auditoria.md")) in (st.get("anteriores_sha256") or [])
             and all(s.get("respuesta_sha256") is None for s in solicitudes(d)), str(st.get("ultima_auditoria_no_aceptada"))[:140])


def grupo_b(exp):
    G = "B X-c con intento intermedio desde 14"
    for modo in MODOS:
        d = copia(exp, f"b_{modo}", modo)
        xc = provocar_xc(d)
        rc14, out14, ult14 = corre(d, "--desde", "14")
        st14, fi14 = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json") or {}
        ok14 = rc14 == 4 and "CIERRE RECHAZADO" in out14 and not fi14.get("cierre") and not os.path.exists(os.path.join(d, "cierre_vigente.json")) and st14.get("auditoria") is None
        rc, out, ult = corre(d, "--desde", "13")
        ok, det = espera_auditoria_nueva(d, rc, ult)
        paso(G, f"[{modo}] --desde 14 rechaza el cierre (código 4, sin ficha cerrada) y --desde 13 pide una auditoría nueva (código 10, solicitud registrada)",
             xc and ok14 and ok, f"código 14 → {rc14} · " + det)


def grupo_c(exp):
    G = "C relanzamientos mientras la respuesta sigue pendiente"
    d = copia(exp, "c", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    sid = (pendientes(d) or [{}])[0].get("id")
    vistos = []
    for etiqueta, prep, extra in (("sin --desde", None, ()), ("--desde 13", None, ("--desde", "13")),
                                  ("informe antiguo con fecha reciente", lambda: os.utime(os.path.join(d, "auditoria.md"), None), ()),
                                  ("informe antiguo con fecha futura", lambda: os.utime(os.path.join(d, "auditoria.md"), (time.time() + 86400 * 400,) * 2), ("--desde", "13"))):
        if prep:
            prep()
        rc, out, ult = corre(d, *extra)
        ok, det = espera_auditoria_nueva(d, rc, ult)
        vistos.append(sid is not None and (pendientes(d) or [{}])[0].get("id") == sid)
        paso(G, f"{etiqueta}: código 10, la misma solicitud pendiente ({(sid or '')[:10]}…), nada cerrado", ok and vistos[-1], det)
    rc, out, ult = corre(d, "--desde", "14")
    st = j(d, "estado_pipeline.json") or {}
    paso(G, "--desde 14 con la solicitud pendiente: cierre rechazado (código 4) por la solicitud pendiente, sin ficha cerrada; la solicitud sigue pendiente",
         rc == 4 and "solicitud de auditoría pendiente" in out and not (j(d, "ficha.json") or {}).get("cierre") and [s["id"] for s in pendientes(d)] == [sid], ult[:140])
    rc, out, ult = corre(d, "--desde", "13")
    ok, det = espera_auditoria_nueva(d, rc, ult)
    paso(G, "después del rechazo, --desde 13 conserva la misma solicitud", ok and (pendientes(d) or [{}])[0].get("id") == sid, det)


def grupo_d(exp):
    G = "D respuestas que no valen"
    d = copia(exp, "d", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    sid = pendientes(d)[0]["id"]
    vieja = leer(d, "auditoria.md")
    ruta = os.path.join(d, "auditoria.md")

    def escribe(texto):
        open(ruta, "w", encoding="utf-8").write(texto)

    def dos_lineas():
        AG.auditoria(d, "APROBADO")
        open(ruta, "a", encoding="utf-8").write(f"Solicitud de auditoría: {sid}\n")

    casos = (("informe antiguo reescrito (otra huella, mismo contenido) sin línea de solicitud", lambda: escribe(vieja + "\n"), "repite el contenido de una auditoría ya usada"),
             ("informe antiguo con la línea de la solicitud vigente añadida y otro formato",
              lambda: escribe("  " + vieja.replace("\n", "  \n").rstrip() + f"\n\n**Solicitud de auditoría:** `{sid}`\n"), "repite el contenido de una auditoría ya usada"),
             ("informe antiguo con punto final en el veredicto (puntuación)", lambda: escribe(vieja.replace("Veredicto: APROBADO", "Veredicto: APROBADO.") + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo en Unicode NFD (visualmente idéntico)", lambda: escribe(unicodedata.normalize("NFD", vieja) + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo con otros separadores (« · » → « - »)", lambda: escribe(vieja.replace(" · ", " - ") + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo con el material entre comillas invertidas y punto", lambda: escribe(re.sub(r"Material auditado: ([0-9a-f]{16})", r"Material auditado: `\1`.", vieja) + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo con la línea de material al principio (orden de líneas)", lambda: escribe("\n".join(sorted(vieja.splitlines(), key=lambda l: 0 if l.startswith("Material auditado") else 1)) + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo con los 16 puntos en orden inverso", lambda: escribe("\n".join(reversed(vieja.splitlines())) + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("informe antiguo sin tildes", lambda: escribe("".join(c for c in unicodedata.normalize("NFKD", vieja) if unicodedata.category(c) != "Mn") + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             # (W-1) a 170 columnas el informe sigue siendo APROBADO según H2; con cortes más estrechos H2 ya lo lee como REPETIR, que no cierra
             ("informe antiguo con las líneas cortadas de nuevo a 170 columnas", lambda: escribe("\n".join(textwrap.fill(l, 170) for l in vieja.splitlines()) + f"\nSolicitud de auditoría: {sid}\n"), "repite el contenido"),
             ("auditoría histórica con otro nombre (auditoria_4_6_antecedente.md) copiada como respuesta", lambda: escribe(leer(d, "auditoria_4_6_antecedente.md") + f"\nSolicitud de auditoría: {sid}\n"), "ya usada"),
             ("auditoría nueva sin línea de solicitud", lambda: AG.auditoria(d, "APROBADO", solicitud=False), "no tiene exactamente una línea «Solicitud de auditoría"),
             ("auditoría nueva con una solicitud equivocada", lambda: AG.auditoria(d, "APROBADO", solicitud="SA-0123456789abcdef"), "responde a la solicitud SA-0123456789abcdef (desconocida)"),
             ("auditoría nueva con dos líneas de solicitud", dos_lineas, "no tiene exactamente una línea"))
    for etiqueta, prepara, motivo in casos:
        prepara()
        rc, out, ult = corre(d)
        ok, det = espera_auditoria_nueva(d, rc, ult)
        st = j(d, "estado_pipeline.json") or {}
        paso(G, f"{etiqueta}: código 10, no se consume, la solicitud sigue pendiente y el motivo consta en el estado",
             ok and pendientes(d)[0]["id"] == sid and motivo in (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", ""), det)
    # material distinto: la respuesta corresponde a la solicitud, pero nombra otro material → corrección con una solicitud nueva
    AG.auditoria(d, "APROBADO", material="0123456789abcdef")
    h_mal = sha(os.path.join(d, "auditoria.md"))
    rc, out, ult = corre(d)
    sols = solicitudes(d)
    st = j(d, "estado_pipeline.json") or {}
    paso(G, "material distinto: la respuesta se consume (respondida, con su huella) y se pide una corrección con una solicitud NUEVA; la misma respuesta ya no vale para la nueva",
         rc == 10 and len(sols) == 2 and sols[0]["id"] == sid and sols[0]["estado"] == "respondida" and sols[0]["respuesta_sha256"] == h_mal and sols[1]["estado"] == "pendiente"
         and sols[1]["id"] != sid and st.get("auditoria") is None and "ya usada" in (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", "")
         and sols[1]["id"] in leer(d, os.path.join("prompts_generados", "13_verificacion.md")) and not (j(d, "ficha.json") or {}).get("cierre"),
         f"código {rc} · {[(s['id'][:10], s['estado']) for s in sols]}")
    # auditoría que incumple H2 (un encabezado inválido) con la solicitud vigente: REPETIR y vuelta a la fase C
    sid2 = sols[1]["id"]
    AG.auditoria(d, "APROBADO")
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("\n17. PASA · punto que no existe\n")
    rc, out, ult = corre(d)
    st = j(d, "estado_pipeline.json") or {}
    s2 = [s for s in solicitudes(d) if s["id"] == sid2][0]
    paso(G, "auditoría que incumple H2 con la solicitud vigente: se consume con veredicto REPETIR, vuelve a la fase C (código 10) y no se cierra nada",
         rc == 10 and st.get("auditoria") == "REPETIR" and s2["estado"] == "respondida" and s2["veredicto"] == "REPETIR" and st.get("esperando") == "10:fase_c.json"
         and not (j(d, "ficha.json") or {}).get("cierre") and not os.path.exists(os.path.join(d, "cierre_vigente.json")), f"código {rc} · {ult[:100]}")


def grupo_e(exp):
    G = "E respuesta válida y cierre"
    for modo in MODOS:
        d = copia(exp, f"e_{modo}", modo)
        provocar_xc(d)
        corre(d, "--desde", "13")
        sid = pendientes(d)[0]["id"]
        AG.auditoria(d, "APROBADO")  # auditor (sintético) que responde a la solicitud vigente sobre el material fijado
        h = sha(os.path.join(d, "auditoria.md"))
        rc, out, ult = corre(d)
        st, fi = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json") or {}
        f = filas(d)
        s = solicitudes(d)[0]
        paso(G, f"[{modo}] respuesta válida: código 0, concluido · paso 14, aprobación de la solicitud {sid[:10]}… con su huella, ficha cerrada con el material fijado, cierre_vigente.json, fila concluido/APROBADO",
             rc == 0 and ult == "estado final: concluido · paso 14" and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO"
             and s["estado"] == "respondida" and s["veredicto"] == "APROBADO" and s["respuesta_sha256"] == h
             and {k: (st.get("auditoria_respuesta") or {}).get(k) for k in ("solicitud", "sha256", "material")} == {"solicitud": sid, "sha256": h, "material": s["material"]}
             and (fi.get("cierre") or {}).get("material_auditado") == s["material"] and os.path.exists(os.path.join(d, "cierre_vigente.json"))
             and len(f) == 1 and f[0].get("estado_analisis") == "concluido" and f[0].get("verificacion") == "APROBADO" and not os.path.exists(os.path.join(d, "ESPERANDO.md"))
             and any(sid in x and "consumida" in x for x in st.get("historial") or []), f"código {rc} · {ult[:100]}")
        if modo != "renovadas":
            continue
        hu = {x: sha(os.path.join(d, x)) for x in ("ficha.json", "informe.md", "cierre_vigente.json")}
        rc1, _, ult1 = corre(d)
        rc2, _, ult2 = corre(d, "--desde", "14")
        paso(G, "relanzamientos sin cambios (sin --desde y con --desde 14): concluido, ninguna solicitud nueva, salidas idénticas",
             rc1 == rc2 == 0 and ult1 == ult2 == "estado final: concluido · paso 14" and len(solicitudes(d)) == 1
             and all(sha(os.path.join(d, x)) == v for x, v in hu.items()), f"{rc1} {rc2}")
        shutil.copy2(os.path.join(exp, "auditoria.md"), os.path.join(d, "auditoria.md"))  # el informe antiguo (APROBADO del mismo material) sustituye a la respuesta
        os.utime(os.path.join(d, "auditoria.md"), None)
        rc3, out3, ult3 = corre(d, "--desde", "14")
        st3 = j(d, "estado_pipeline.json") or {}
        paso(G, "informe antiguo en lugar de la respuesta registrada: el cierre se archiva y se rechaza (código 4); no queda ninguna ficha cerrada",
             rc3 == 4 and "no es la respuesta registrada" in out3 and not os.path.exists(os.path.join(d, "ficha.json")) and st3.get("estado_analisis") is None, ult3[:140])


def grupo_i(exp):
    G = "I vías del control de vigencia de la 4.8.1"
    # auditorías históricas guardadas en el expediente con nombres o carpetas que no son auditoria*.md (V-2)
    for etiqueta, destino in (("con mayúscula (Auditoria_4_6.md)", "Auditoria_4_6.md"), ("con otra extensión (auditoria_4_6.md.bak)", "auditoria_4_6.md.bak"),
                              ("en una subcarpeta (antecedentes/auditoria.md)", os.path.join("antecedentes", "auditoria.md"))):
        d = copia(exp, "i_" + os.path.basename(destino).replace(".", "_"), "renovadas")
        os.makedirs(os.path.dirname(os.path.join(d, destino)), exist_ok=True)
        os.replace(os.path.join(d, "auditoria_4_6_antecedente.md"), os.path.join(d, destino))
        provocar_xc(d)
        corre(d, "--desde", "13")
        sid = pendientes(d)[0]["id"]
        open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(leer(d, destino) + f"\nSolicitud de auditoría: {sid}\n")
        rc, out, ult = corre(d)
        ok, det = espera_auditoria_nueva(d, rc, ult)
        st = j(d, "estado_pipeline.json") or {}
        paso(G, f"auditoría histórica guardada {etiqueta} y copiada como respuesta: no se acepta (código 10, sin cierre)",
             ok and "ya usada" in (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", ""), det)
    # auditorías históricas en otra codificación o con relleno (W-2)
    for etiqueta, destino, escribir in (("en cp1252", os.path.join("antecedentes", "auditoria_4_6.txt"), lambda p, s: open(p, "w", encoding="cp1252", errors="replace").write(s)),
                                        ("en UTF-16", os.path.join("notas", "auditoria_4_6.md"), lambda p, s: open(p, "w", encoding="utf-16").write(s)),
                                        ("con 2,1 millones de líneas vacías al final (más de 2 MB)", "auditoria_4_6_relleno.md", lambda p, s: open(p, "w", encoding="utf-8").write(s + "\n" * 2_100_000))):
        d = copia(exp, "i_cod_" + os.path.basename(destino).replace(".", "_"), "renovadas")
        texto = leer(d, "auditoria_4_6_antecedente.md")
        os.remove(os.path.join(d, "auditoria_4_6_antecedente.md"))
        os.makedirs(os.path.dirname(os.path.join(d, destino)), exist_ok=True)
        escribir(os.path.join(d, destino), texto)
        provocar_xc(d)
        corre(d, "--desde", "13")
        sid = pendientes(d)[0]["id"]
        open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(texto + f"\nSolicitud de auditoría: {sid}\n")
        rc, out, ult = corre(d)
        ok, det = espera_auditoria_nueva(d, rc, ult)
        paso(G, f"auditoría histórica guardada {etiqueta} y copiada en UTF-8 como respuesta: no se acepta (código 10, sin cierre)", ok, det)
    # respuesta que no es UTF-8 válido (W-3): no se consume; el pipeline sigue esperando con el motivo, sin traza
    d = copia(exp, "i_no_utf8", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    with open(os.path.join(d, "auditoria.md"), "ab") as fh:
        fh.write(b"\nAviso: inversi\xf3n\n")
    rc, out, ult = corre(d)
    st = j(d, "estado_pipeline.json") or {}
    paso(G, "respuesta que no es UTF-8 válido: no se consume (solicitud pendiente, código 10, motivo explícito, sin traza ni cierre)",
         rc == 10 and "Traceback" not in out and len(pendientes(d)) == 1 and "UTF-8" in (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", "")
         and not (j(d, "ficha.json") or {}).get("cierre"), ult[:140])
    # registro ilegible (V-9): código 6, motivo explícito, nada cerrado
    d = copia(exp, "i_registro", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    resultados = []
    for contenido in ("{ilegible", '{"sha256": 5}'):
        open(os.path.join(d, "auditorias_conocidas.json"), "w", encoding="utf-8").write(contenido)
        rc, out, ult = corre(d)
        resultados.append((contenido, rc, "REGISTRO DE AUDITORÍAS ILEGIBLE" in out and "Traceback" not in out))
    paso(G, "auditorias_conocidas.json ilegible o con tipos inválidos: código 6, «REGISTRO DE AUDITORÍAS ILEGIBLE» sin traza y nada cerrado",
         all(rc == 6 and ok for _, rc, ok in resultados) and not (j(d, "ficha.json") or {}).get("cierre"), str(resultados))


def grupo_h(exp):
    G = "H vías adicionales (auditoría interna de la 4.8.1)"
    # penúltima respuesta reutilizada (M11)
    d = copia(exp, "h_penultima", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    r1 = leer(d, "auditoria.md")
    rc1, _, _ = corre(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    open(os.path.join(d, "auditoria.md"), "a", encoding="utf-8").write("Aviso: segunda auditoría sintética, con otra evidencia.\n")
    rc2, _, _ = corre(d)
    corre(d, "--desde", "13")
    sid3 = (pendientes(d) or [{}])[0].get("id")
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(re.sub(r"Solicitud de auditoría: SA-[0-9a-f]{16}", f"Solicitud de auditoría: {sid3}", r1))
    rc3, out3, ult3 = corre(d)
    ok, det = espera_auditoria_nueva(d, rc3, ult3, n_solicitudes=3)
    paso(G, "la penúltima respuesta (ya usada) con la línea de la solicitud vigente no responde a una solicitud nueva",
         rc1 == 0 and rc2 == 0 and ok and "ya usada" in ((j(d, "estado_pipeline.json") or {}).get("ultima_auditoria_no_aceptada") or {}).get("motivo", ""), det)
    # registro persistente: una respuesta ya usada que ya no está en el expediente ni en el estado (lo que dejarían --reiniciar y una
    # limpieza de la carpeta) sigue sin poder responder, porque su huella está en auditorias_conocidas.json
    d = copia(exp, "h_registro", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    r1 = leer(d, "auditoria.md")
    rc1, _, _ = corre(d)
    shutil.rmtree(os.path.join(d, "historial_cierres"))
    for f in [x for x in os.listdir(d) if x.startswith("auditoria") and x.endswith(".md")] + ["ficha.json", "informe.md", "cierre_vigente.json"]:
        if os.path.exists(os.path.join(d, f)):
            os.remove(os.path.join(d, f))
    st = j(d, "estado_pipeline.json")
    for k in ("solicitudes_auditoria", "anteriores_sha256", "anteriores_contenido", "auditoria_respuesta"):
        st.pop(k, None)
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    corre(d, "--desde", "13")
    sidr = (pendientes(d) or [{}])[0].get("id")
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(re.sub(r"Solicitud de auditoría: SA-[0-9a-f]{16}", f"Solicitud de auditoría: {sidr}", r1))
    rc, out, ult = corre(d)
    st = j(d, "estado_pipeline.json") or {}
    paso(G, "auditorias_conocidas.json guarda las huellas fuera de estado_pipeline.json: una respuesta usada que ya no está ni en la carpeta ni en el estado sigue sin valer",
         rc1 == 0 and rc == 10 and sidr is not None and "ya usada" in (st.get("ultima_auditoria_no_aceptada") or {}).get("motivo", "") and st.get("auditoria") is None
         and not (j(d, "ficha.json") or {}).get("cierre"), f"código {rc1} → {rc} · {ult[:100]}")
    # ficha.py directo con una solicitud pendiente no cierra
    d = copia(exp, "h_ficha", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    st = j(d, "estado_pipeline.json")
    st["auditoria"] = "APROBADO"  # aunque el estado conservara una aprobación anterior, la solicitud pendiente impide cerrar
    json.dump(st, open(os.path.join(d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--estado", "concluido"], capture_output=True, text=True)
    paso(G, "ficha.py --estado concluido con una solicitud pendiente (y una aprobación anterior en el estado): código 3 y ninguna ficha cerrada",
         r.returncode == 3 and not (j(d, "ficha.json") or {}).get("cierre") and not os.path.exists(os.path.join(d, "cierre_vigente.json")), (r.stdout + r.stderr).strip()[-120:])
    # --desde 13 sobre un cierre vigente sin X-c: el cierre se archiva en la misma ejecución
    d = copia(exp, "h_desde13", "renovadas")
    arch0 = len(os.listdir(os.path.join(d, "historial_cierres")))
    rc, out, ult = corre(d, "--desde", "13")
    ok, det = espera_auditoria_nueva(d, rc, ult)
    paso(G, "--desde 13 sobre un cierre vigente: en la primera ejecución el cierre se archiva, la fila deja de estar APROBADO y la aprobación pasa al historial; se espera la respuesta",
         ok and not os.path.exists(os.path.join(d, "ficha.json")) and len(os.listdir(os.path.join(d, "historial_cierres"))) == arch0 + 1, det)
    # cambio de material con la solicitud pendiente: la pendiente queda sustituida
    d = copia(exp, "h_material", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    s1 = pendientes(d)[0]["id"]
    fc = j(d, "fase_c.json")
    fc["celdas"]["B101"] += " [MARCADOR 4.8.1]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out, ult = corre(d, "--desde", "13")
    sols = solicitudes(d)
    paso(G, "cambio de material con la solicitud pendiente: la anterior queda «sustituida» y se registra otra del material nuevo (código 10)",
         rc == 10 and len(sols) == 2 and sols[0]["id"] == s1 and sols[0]["estado"] == "sustituida" and sols[1]["estado"] == "pendiente" and sols[1]["material"] != sols[0]["material"],
         str([(s["id"][:10], s["estado"], s["material"]) for s in sols]))
    # la misma respuesta guardada con otros finales de línea sigue siendo la respuesta registrada
    d = copia(exp, "h_crlf", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    corre(d)
    txt = leer(d, "auditoria.md")
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8", newline="").write(txt.replace("\n", "\r\n"))
    rc, out, ult = corre(d)
    paso(G, "la respuesta registrada guardada de nuevo con finales CRLF: el cierre sigue vigente, sin solicitud nueva",
         rc == 0 and ult == "estado final: concluido · paso 14" and len(solicitudes(d)) == 1 and (j(d, "ficha.json") or {}).get("cierre"), ult[:120])
    # una respuesta que no aprueba (REPETIR) puede repetir el contenido de otra: no cierra nada (la regla de reutilización es para aprobaciones)
    d = copia(exp, "h_repetir", "renovadas")
    provocar_xc(d)
    corre(d, "--desde", "13")
    AG.auditoria(d, "REPETIR")
    rep1 = leer(d, "auditoria.md")
    rca, _, _ = corre(d)
    corre(d, "--desde", "13")
    s2 = (pendientes(d) or [{}])[0].get("id")
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(re.sub(r"Solicitud de auditoría: SA-[0-9a-f]{16}", f"Solicitud de auditoría: {s2}", rep1))
    rcb, outb, ultb = corre(d)
    stb = j(d, "estado_pipeline.json") or {}
    paso(G, "una REPETIR con el mismo contenido que otra anterior responde a la solicitud nueva (se consume y vuelve a la fase C; no cierra nada)",
         rca == 10 and rcb == 10 and stb.get("auditoria") == "REPETIR" and [s["estado"] for s in solicitudes(d)] == ["respondida", "respondida"] and stb.get("esperando") == "10:fase_c.json"
         and not (j(d, "ficha.json") or {}).get("cierre"), f"{rca} {rcb} · {[(s['id'][:8], s['estado'], s.get('veredicto')) for s in solicitudes(d)]}")
    # cierre anterior a la 4.8.1 con auditoria.md sustituida por otra aprobación del mismo material
    d = copia(exp, "h_historico", "renovadas")
    shutil.copy2(os.path.join(d, "auditoria_4_6_antecedente.md"), os.path.join(d, "auditoria.md"))
    rc, out, ult = corre(d, "--desde", "14")
    paso(G, "cierre anterior a la 4.8.1 con auditoria.md sustituida: no sigue vigente ni se vuelve a cerrar (código 4, sin ficha cerrada)",
         rc == 4 and not (j(d, "ficha.json") or {}).get("cierre") and "cierre_vigente.json" in out, ult[:140])


def grupo_f(exp):
    G = "F cierre histórico sin solicitudes"
    d = copia(exp, "f", "renovadas")
    hu = {x: sha(os.path.join(d, x)) for x in ("ficha.json", "informe.md", "cierre_vigente.json", "auditoria.md")}
    rc1, _, ult1 = corre(d)
    rc2, _, ult2 = corre(d, "--desde", "14")
    st = j(d, "estado_pipeline.json") or {}
    paso(G, "el cierre aprobado de la 4.6.1 sigue vigente (sin --desde y con --desde 14) y no recibe ninguna solicitud retroactiva",
         rc1 == rc2 == 0 and ult1 == ult2 == "estado final: concluido · paso 14" and not st.get("solicitudes_auditoria") and "auditoria_respuesta" not in st
         and "anteriores_sha256" not in st and all(sha(os.path.join(d, x)) == v for x, v in hu.items()) and (j(d, "ficha.json") or {}).get("cierre", {}).get("material_auditado") == MATERIAL,
         f"{rc1} {rc2}")


def grupo_g():
    G = "G regla H2"
    h = hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest()
    paso(G, "Pipeline.veredicto_auditoria es idéntica a la de la 4.7.1 (16 puntos únicos, todos PASA, un único APROBADO, ningún FALLA ni encabezado inválido)", h == H2_SHA_4_7_1, h[:16])
    lee = getattr(CIE, "id_solicitud_en_auditoria", None)  # con un código sin la reparación, la prueba falla sin interrumpir la batería
    paso(G, "el identificador de solicitud solo se lee en una línea propia («Solicitud de auditoría: SA-<16 hex>»), exactamente una vez",
         lee is not None and lee("Solicitud de auditoría: SA-0123456789ABCDEF") == "SA-0123456789abcdef"
         and lee("**Solicitud de auditoria:** `SA-0123456789abcdef`") == "SA-0123456789abcdef"
         and lee("texto SA-0123456789abcdef") is None
         and lee("Solicitud de auditoría: SA-0123456789abcdef\nSolicitud de auditoría: SA-0123456789abcdee") is None)


def main(exp):
    for g in (grupo_a, grupo_b, grupo_c, grupo_d, grupo_e, grupo_h, grupo_i, grupo_f):
        try:
            g(exp)
        except Exception as e:  # noqa
            import traceback
            traceback.print_exc()
            paso(g.__name__, "excepción " + str(e)[:100], False)
    grupo_g()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--expediente", default=os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
    a = ap.parse_args()
    try:
        main(os.path.abspath(a.expediente))
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    n = sum(ok for _, _, ok in R)
    print(f"\n{n}/{len(R)} pruebas de solicitudes de auditoría PASAN")
    sys.exit(0 if n == len(R) else 1)
