#!/usr/bin/env python3
"""Batería de integridad de la respuesta de auditoría vigente (entrega 4.9, encargo §3: R-V1). Solo trabaja en directorios
temporales: no modifica el expediente de referencia ni el código del árbol.

Uso: python3 -B pruebas/test_integridad_auditoria_v2.py [--expediente <carpeta Vidrala aprobada de la 4.6.1>] [--codigo <carpeta>] [--json <archivo>]

Con --codigo <carpeta>, los .py de esa carpeta sustituyen a los de personaje_v2/scripts/ en una copia temporal del árbol: así se
reproduce el defecto con el código 4.8.1 conservado en …/2026-11_Vidrala_ensayo_4_9/reproduccion/codigo_4_8_1/.

**El defecto (4.8.1).** Tras aceptar una respuesta a una solicitud y cerrar, motivo_rechazo_cierre() daba por buena cualquier
auditoria.md cuya huella de contenido (cierre_v2.huella_contenido: el multiconjunto de sus palabras, SIN la línea de solicitud y
sin el orden) coincidiera con la registrada. Seguían concluido/APROBADO, con código 0, un auditoria.md con la solicitud cambiada,
eliminada o duplicada y otro con las mismas palabras en otro orden y otro significado («La evidencia respalda el crecimiento; la
reposición queda pendiente» ↔ «La evidencia respalda la reposición; el crecimiento queda pendiente»), por el paso 14 y por
ficha.py, informe.py y resumen.py.

**La reparación (4.9).** Dos funciones separadas:
  A. detección de posibles reutilizaciones (paso 13): huella_contenido, detector conservador, sin cambios;
  B. identidad de la respuesta aceptada (vigencia): por separado, la solicitud (exactamente una línea, la registrada, respondida y
     del material fijado), el material (sin cambios) y la respuesta (huella_fiel: contenido y orden íntegros, salvo las
     transformaciones inocuas definidas en cierre_v2.TRANSFORMACIONES_INOCUAS: BOM UTF-8, finales de línea CRLF/CR → LF, saltos de
     línea al final del archivo y forma canónica Unicode NFC).

**Auditorías sintéticas.** Todas las auditorías de esta batería las escribe pruebas/agentes_sinteticos.py y dicen «(sintético)»;
la línea de aviso añadida dice «auditoría sintética de la prueba R-V1».

**Grupos.** Cada caso parte de una copia del mismo cierre (respuesta válida a una solicitud, con la fila publicada en el resumen
predeterminado y en un destino configurado) y observa la PRIMERA llamada: código, última línea, estado del pipeline, ficha,
informe, cierre_vigente.json, filas de los dos destinos, historial del resumen y RETIRADA.json.
  A. Cierre base: respuesta válida, código 0, concluido/APROBADO y la huella fiel registrada.
  B. Por cada vía (paso 14, ficha.py, informe.py, resumen.py): solicitud cambiada, eliminada y duplicada; mismas palabras con otro
     significado; mismas líneas en otro orden; respuesta sustituida; material modificado. Se retira la aprobación en los dos destinos con el diagnóstico propio.
  C. Transformaciones: CRLF por cada vía, CR, BOM y sin salto final (inocuas: siguen vigentes); NFD (inocua: forma canónica);
     espacio al final de una línea y línea en blanco intermedia (no admitidas: se retira).
  D. Destino inaccesible: retirada pendiente identificada (código 5), sin presentarla como completada; al restaurar el destino se completa.
  E. Reanudación: tras la retirada, restaurar la respuesta original no reactiva el cierre; --desde 13 y una respuesta legítima
     nueva cierran (código 0) y el historial conserva el cierre retirado.
  F. Compatibilidad: cierre de la 4.6.1 (sin solicitudes) vigente por las cuatro vías y sin solicitud retroactiva; con su
     auditoría en CRLF no se acredita (huella de bytes) y se retira; cierre de la 4.8.1 (respuesta sin huella fiel registrada):
     vigente con los bytes idénticos; con CRLF o con la reordenación, no acreditable y retirado, sin calcular una huella nueva;
     cierre de la 4.9 sin estado_pipeline.json (cierre_vigente.json lleva solicitud y huella fiel): intacto, vigente; reordenado o con
     otra solicitud, retirado; solicitud que el estado ya no registra como respondida: retirado.
  H. Hallazgos de la auditoría interna de la 4.9:
     - Z-1: sin ningún registro de la respuesta aprobada (cierre_vigente.json borrado en un cierre de la 4.6.1, por las cuatro vías;
       cierre de la 4.6 sin él de origen; cierre de la 4.9 sin estado ni cierre_vigente.json) no se vuelve a cerrar con otra
       aprobación ni se atribuye la huella del archivo actual;
     - Z-2: auditoria.md que no es UTF-8 (por las cuatro vías; cp1252), cierre_vigente.json o estado_pipeline.json ilegibles: se
       retira la aprobación sin interrumpir la vía (el pipeline termina con código 6 después de retirar);
     - Z-3: sin estado y con CRLF sigue vigente por la huella fiel de cierre_vigente.json.
  I. Hallazgos del control de vigencia de la 4.9:
     - V-1: material_auditoria.json ilegible (por las cuatro vías) y ficha.json ilegible: se retira sin traza; con la aprobación
       (ficha.py tampoco vuelve a cerrar: segundo control de vigencia, W-2);
     - V-2: JSON válido que no es un objeto, estructura interna errónea, estado_pipeline.json o auditoria.md que son una carpeta:
       se retira sin traza (el pipeline termina con código 6 después de retirar);
     - V-3: sin estado, ficha.py conserva en cierre_vigente.json la solicitud, la huella fiel y la huella de bytes de la respuesta
       aceptada (también después de una transformación inocua);
     - del segundo control de vigencia: W-1 («cierre» de la ficha que no es un objeto, solicitud sin «id», tipos erróneos en el
       estado por el paso 14) y W-4 (un material_auditado con «../» no saca el archivo del expediente).
  G. Unidades: huella_fiel (también los límites de la lista cerrada: NFKC, U+200B, NBSP, U+2028, VT) y huella_contenido; H2 idéntica a
     la de la 4.7.1.
"""
import argparse
import csv
import glob
import hashlib
import inspect
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
ap = argparse.ArgumentParser()
ap.add_argument("--expediente", default=os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
ap.add_argument("--codigo", help="carpeta con los .py que sustituyen a los de personaje_v2/scripts/ (reproducción con otro código)")
ap.add_argument("--json", help="escribe también los resultados (grupo, prueba, resultado, detalle) en este archivo JSON")
ARGS = ap.parse_args()
TMP = tempfile.mkdtemp(prefix="integridad49_")


def arbol_de_codigo():
    """personaje_v2/scripts del árbol o, con --codigo, una copia temporal con esos .py."""
    if not ARGS.codigo:
        return os.path.join(RAIZ, "scripts")
    raiz = os.path.join(TMP, "codigo")
    os.makedirs(raiz)
    shutil.copytree(RAIZ, os.path.join(raiz, "personaje_v2"),
                    ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(os.path.dirname(RAIZ), x), os.path.join(raiz, x))
    scr = os.path.join(raiz, "personaje_v2", "scripts")
    for f in os.listdir(ARGS.codigo):
        if f.endswith(".py"):
            shutil.copy2(os.path.join(ARGS.codigo, f), os.path.join(scr, f))
    return scr


SCR = arbol_de_codigo()
sys.path.insert(0, SCR)
sys.path.insert(0, AQUI)
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

PY = sys.executable
EMPRESA = "Vidrala, S.A."
H2_SHA_4_7_1 = "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422"
FRASE = "Aviso: La evidencia respalda el crecimiento; la reposición queda pendiente. (auditoría sintética de la prueba R-V1)"
FRASE_REORDENADA = "Aviso: La evidencia respalda la reposición; el crecimiento queda pendiente. (auditoría sintética de la prueba R-V1)"
SA = re.compile(r"SA-[0-9a-f]{16}")
R = []


def paso(grupo, nombre, ok, detalle=""):
    R.append((grupo, nombre, bool(ok), detalle))
    print(("PASA " if ok else "FALLA") + f" · {grupo} · {nombre}" + (f" · {detalle}" if detalle else ""), flush=True)


def j(c, f):
    p = os.path.join(c, f)
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    except ValueError:
        return None


def leer(c, f):
    p = os.path.join(c, f)
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def corre(script, *args):
    r = subprocess.run([PY, "-B", os.path.join(SCR, script), *args], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out, (out.splitlines() or [""])[-1]


def filas(csv_path):
    if not os.path.isfile(csv_path):
        return []
    return [r for r in csv.DictReader(open(csv_path, encoding="utf-8")) if r.get("empresa") == EMPRESA]


def aprobada(csv_path):
    f = filas(csv_path)
    return len(f) == 1 and f[0].get("estado_analisis") == "concluido" and f[0].get("verificacion") == "APROBADO"


def retirada(csv_path):
    f = filas(csv_path)
    return len(f) == 1 and (f[0].get("verificacion") or "").startswith(CIE.NO_VIGENTE)


# ---------- escenario: un cierre por respuesta a una solicitud ----------
class Caso:
    """Copia de un escenario: d (expediente), pred (resumen predeterminado), extra (destino configurado)."""

    def __init__(self, base):
        self.base = base
        self.d = os.path.join(base, "exp", "Vidrala")
        self.pred = os.path.join(base, "exp", "resumen_v2.csv")
        self.extra = os.path.join(base, "otro_destino", "resumen_configurado.csv")
        self.aud = os.path.join(self.d, "auditoria.md")

    def copiar(self, nombre):
        nuevo = os.path.join(TMP, nombre)
        shutil.copytree(self.base, nuevo, symlinks=True)
        return Caso(nuevo)

    def st(self):
        return j(self.d, "estado_pipeline.json") or {}

    def archivos_historial(self):
        h = os.path.join(self.d, "historial_cierres")
        return sorted(os.listdir(h)) if os.path.isdir(h) else []

    def ultima_retirada(self):
        a = self.archivos_historial()
        return j(os.path.join(self.d, "historial_cierres", a[-1]), "RETIRADA.json") if a else None


ESCENARIOS = {}


def escenario_respuesta(exp):
    """Cierre de la 4.8.1/4.9: --desde 13 sobre el cierre de la 4.6.1 (lo archiva y registra una solicitud), respuesta sintética
    válida con la frase de la prueba, cierre (código 0) y publicación en un destino configurado."""
    if "resp" in ESCENARIOS:
        return ESCENARIOS["resp"]
    base = os.path.join(TMP, "escenario_respuesta")
    c = Caso(base)
    shutil.copytree(exp, c.d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(exp), f)):
            shutil.copy2(os.path.join(os.path.dirname(exp), f), os.path.join(base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    rc13, _, _ = corre("pipeline.py", c.d, "--desde", "13")
    AG.auditoria(c.d, "APROBADO")
    open(c.aud, "a", encoding="utf-8").write(FRASE + "\n")
    rc, out, ult = corre("pipeline.py", c.d)
    rcr, _, _ = corre("resumen.py", c.d, c.extra)
    ESCENARIOS["resp"] = (c, rc13, rc, ult, rcr)
    return ESCENARIOS["resp"]


def escenario_historico(exp):
    """Cierre de la 4.6.1 tal como está (sin solicitudes), con la fila publicada también en un destino configurado."""
    if "hist" in ESCENARIOS:
        return ESCENARIOS["hist"]
    base = os.path.join(TMP, "escenario_historico")
    c = Caso(base)
    shutil.copytree(exp, c.d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(exp), f)):
            shutil.copy2(os.path.join(os.path.dirname(exp), f), os.path.join(base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    rcr, _, _ = corre("resumen.py", c.d, c.extra)
    ESCENARIOS["hist"] = (c, rcr)
    return ESCENARIOS["hist"]


# ---------- mutaciones posteriores al cierre ----------
def m_solicitud_cambiada(c):
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="utf-8").write(SA.sub("SA-0123456789abcdef", t))


def m_solicitud_eliminada(c):
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="utf-8").write("\n".join(l for l in t.split("\n") if not l.startswith("Solicitud de auditoría")))


def m_solicitud_duplicada(c):
    t = leer(c.d, "auditoria.md")
    sid = SA.search(t).group(0)
    open(c.aud, "w", encoding="utf-8").write(t + f"Solicitud de auditoría: {sid}\n")


def m_mismas_palabras(c):
    t = leer(c.d, "auditoria.md")
    assert FRASE in t
    open(c.aud, "w", encoding="utf-8").write(t.replace(FRASE, FRASE_REORDENADA))


def m_lineas_intercambiadas(c):
    # mismas líneas, mismo texto, otro orden: la observación pasa delante del veredicto
    t = leer(c.d, "auditoria.md")
    ls = t.split("\n")
    i, k = ls.index(FRASE), next(n for n, l in enumerate(ls) if l.startswith("VEREDICTO"))
    ls[i], ls[k] = ls[k], ls[i]
    open(c.aud, "w", encoding="utf-8").write("\n".join(ls))


def m_respuesta_sustituida(c):
    # otra auditoría sintética APROBADO de la misma solicitud y el mismo material, con otra observación
    AG.auditoria(c.d, "APROBADO", solicitud=(c.st().get("auditoria_respuesta") or {}).get("solicitud") or None)
    open(c.aud, "a", encoding="utf-8").write("Aviso: otra auditoría sintética de la prueba R-V1, con otra evidencia.\n")


def m_material(c):
    r = j(c.d, "resultados.json")
    r["_marca_prueba_rv1"] = "material modificado en una copia temporal"
    json.dump(r, open(os.path.join(c.d, "resultados.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def m_crlf(c):
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r\n"))


def m_cr(c):
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="utf-8", newline="").write(t.replace("\n", "\r"))


def escribir(c, texto):
    """Escribe auditoria.md con el texto ya leído (leer antes de abrir para escribir: abrir con «w» vacía el archivo)."""
    with open(c.aud, "w", encoding="utf-8") as fh:
        fh.write(texto)


def m_bom(c):
    b = open(c.aud, "rb").read()
    open(c.aud, "wb").write(b"\xef\xbb\xbf" + b)


def m_sin_salto_final(c):
    escribir(c, leer(c.d, "auditoria.md").rstrip("\n"))


def m_nfd(c):
    escribir(c, unicodedata.normalize("NFD", leer(c.d, "auditoria.md")))


def m_espacio_final_de_linea(c):
    t = leer(c.d, "auditoria.md")
    assert FRASE + "\n" in t
    escribir(c, t.replace(FRASE + "\n", FRASE + "  \n"))


def m_linea_en_blanco(c):
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="utf-8").write(t.replace("\n2. ", "\n\n2. ", 1))


VIAS = (("paso 14", lambda c: corre("pipeline.py", c.d, "--desde", "14"), 4),
        ("ficha.py", lambda c: corre("ficha.py", c.d, "--estado", "concluido"), 3),
        ("informe.py", lambda c: corre("informe.py", c.d), 3),
        ("resumen.py", lambda c: corre("resumen.py", c.d, c.pred), 3))
CODIGO_VIGENTE = {"paso 14": 0, "ficha.py": 0, "informe.py": 0, "resumen.py": 0}


def observa_retirada(c, rc, out, rc_esperado, aud_antes, diagnostico):
    """La primera llamada retira la aprobación por completo y con el diagnóstico propio."""
    st = c.st()
    ret = c.ultima_retirada() or {}
    hist = list(csv.DictReader(open(os.path.join(os.path.dirname(c.pred), "resumen_v2_historial.csv"), encoding="utf-8"))) if os.path.exists(os.path.join(os.path.dirname(c.pred), "resumen_v2_historial.csv")) else []
    ok = (rc == rc_esperado and not os.path.exists(os.path.join(c.d, "ficha.json")) and not os.path.exists(os.path.join(c.d, "cierre_vigente.json"))
          and not os.path.exists(os.path.join(c.d, "informe.md")) and st.get("estado_analisis") is None and st.get("auditoria") is None
          and retirada(c.pred) and retirada(c.extra) and any(r.get("verificacion") == "APROBADO" for r in hist)
          and diagnostico in (ret.get("motivo") or "") and sha(c.aud) == aud_antes
          and os.path.exists(os.path.join(c.d, "historial_cierres", c.archivos_historial()[-1], "auditoria_en_el_momento_de_la_retirada.md")))
    det = (f"código {rc} (esperado {rc_esperado}) · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r} · ficha {os.path.exists(os.path.join(c.d, 'ficha.json'))}"
           f" · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]} · extra {[(r.get('verificacion') or '')[:22] for r in filas(c.extra)]}"
           f" · retirada: {(ret.get('motivo') or '')[:130]}")
    return ok, det


def observa_vigente(c, rc, via, hu):
    st = c.st()
    ok = (rc == CODIGO_VIGENTE[via] and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and (j(c.d, "ficha.json") or {}).get("cierre")
          and os.path.exists(os.path.join(c.d, "cierre_vigente.json")) and aprobada(c.pred) and aprobada(c.extra) and c.archivos_historial() == hu
          and len([s for s in st.get("solicitudes_auditoria") or [] if s.get("estado") == "pendiente"]) == 0)
    return ok, f"código {rc} · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r} · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]} · extra {[(r.get('verificacion') or '')[:22] for r in filas(c.extra)]}"


CAMBIO = "su contenido o su orden cambiaron"
MUTACIONES_B = (("solicitud cambiada por otra", m_solicitud_cambiada, "nombra la solicitud SA-0123456789abcdef"),
                ("solicitud eliminada", m_solicitud_eliminada, "no tiene ninguna línea «Solicitud de auditoría»"),
                ("solicitud duplicada", m_solicitud_duplicada, "tiene 2 líneas «Solicitud de auditoría»"),
                ("mismas palabras, otro significado", m_mismas_palabras, CAMBIO),
                ("mismas líneas en otro orden", m_lineas_intercambiadas, CAMBIO),
                ("respuesta sustituida por otra aprobación", m_respuesta_sustituida, CAMBIO),
                ("material financiero modificado", m_material, "el material cambió"))


def grupo_a(exp):
    G = "A cierre base por respuesta a una solicitud"
    c, rc13, rc, ult, rcr = escenario_respuesta(exp)
    st = c.st()
    resp = st.get("auditoria_respuesta") or {}
    paso(G, "--desde 13 pide la auditoría (código 10); la respuesta sintética válida cierra (código 0, concluido · paso 14) y se publica en un destino configurado",
         rc13 == 10 and rc == 0 and ult == "estado final: concluido · paso 14" and rcr == 0 and aprobada(c.pred) and aprobada(c.extra), f"{rc13} {rc} {rcr} · {ult[:80]}")
    fiel = getattr(CIE, "huella_fiel", None)
    paso(G, "la respuesta aceptada queda registrada con su solicitud, su material y su huella fiel (contenido y orden)",
         fiel is not None and resp.get("fiel") == fiel(open(c.aud, "rb").read()) and resp.get("solicitud") == SA.search(leer(c.d, "auditoria.md")).group(0)
         and resp.get("material") == (CIE.material_fijado(c.d) or {}).get("id"), str({k: str(v)[:18] for k, v in resp.items()}))


def grupo_b(exp):
    G = "B cambios posteriores al cierre (primera llamada)"
    c0 = escenario_respuesta(exp)[0]
    for etiqueta, mut, diag in MUTACIONES_B:
        for via, llamada, rc_esp in VIAS:
            c = c0.copiar(f"b_{mut.__name__}_{via.split('.')[0].replace(' ', '')}")
            mut(c)
            aud = sha(c.aud)
            rc, out, ult = llamada(c)
            ok, det = observa_retirada(c, rc, out, rc_esp, aud, diag)
            paso(G, f"{etiqueta} · {via}: aprobación retirada en la primera llamada (código {rc_esp}), en los dos destinos, con historial y diagnóstico «{diag}»", ok, det)


def grupo_c(exp):
    G = "C transformaciones inocuas y no admitidas"
    c0 = escenario_respuesta(exp)[0]
    hu = c0.archivos_historial()
    for via, llamada, _ in VIAS:
        c = c0.copiar(f"c_crlf_{via.split('.')[0].replace(' ', '')}")
        m_crlf(c)
        rc, out, ult = llamada(c)
        ok, det = observa_vigente(c, rc, via, hu)
        paso(G, f"CRLF · {via}: transformación inocua, el cierre sigue vigente", ok, det)
    for etiqueta, mut in (("finales CR", m_cr), ("BOM UTF-8 al principio", m_bom), ("sin salto de línea final", m_sin_salto_final), ("Unicode NFD (forma canónica equivalente)", m_nfd)):
        c = c0.copiar(f"c_{mut.__name__}")
        mut(c)
        rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
        ok, det = observa_vigente(c, rc, "paso 14", hu)
        paso(G, f"{etiqueta} · paso 14: transformación inocua, el cierre sigue vigente", ok, det)
    for etiqueta, mut in (("espacios añadidos al final de una línea", m_espacio_final_de_linea), ("línea en blanco intercalada", m_linea_en_blanco)):
        c = c0.copiar(f"c_{mut.__name__}")
        mut(c)
        aud = sha(c.aud)
        rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
        ok, det = observa_retirada(c, rc, out, 4, aud, CAMBIO)
        paso(G, f"{etiqueta} · paso 14: no es una transformación admitida, se retira la aprobación", ok, det)


def grupo_d(exp):
    G = "D destino inaccesible"
    c = escenario_respuesta(exp)[0].copiar("d_inaccesible")
    copia_extra = open(c.extra, encoding="utf-8").read()
    os.remove(c.extra)
    os.makedirs(c.extra)  # el destino configurado deja de ser un archivo accesible
    m_mismas_palabras(c)
    rc, out, ult = corre("informe.py", c.d)
    reg = j(c.d, CIE.REGISTRO_RESUMEN) or {}
    e = next((x for x in reg.get("publicaciones", []) if x.get("csv") == c.extra), {})
    paso(G, "mismas palabras con otro significado e informe.py con un destino inaccesible: código 5, «RETIRADA PENDIENTE» con el destino identificado, salidas archivadas y el predeterminado retirado",
         rc == 5 and "RETIRADA PENDIENTE" in out and e.get("estado") == "retirada_pendiente" and e.get("error") and retirada(c.pred)
         and not os.path.exists(os.path.join(c.d, "ficha.json")) and CAMBIO in ((c.ultima_retirada() or {}).get("motivo") or ""), f"código {rc} · {e.get('estado')} · {ult[:100]}")
    rc2, out2, _ = corre("pipeline.py", c.d, "--desde", "14")
    paso(G, "con la retirada pendiente, el pipeline se detiene con código 5 y no la presenta como completada", rc2 == 5 and "RETIRADA PENDIENTE" in out2 and not os.path.exists(os.path.join(c.d, "ficha.json")), str(rc2))
    shutil.rmtree(c.extra)
    open(c.extra, "w", encoding="utf-8").write(copia_extra)
    rc3, out3, _ = corre("pipeline.py", c.d, "--desde", "14")
    e = next((x for x in (j(c.d, CIE.REGISTRO_RESUMEN) or {}).get("publicaciones", []) if x.get("csv") == c.extra), {})
    paso(G, "al restaurar el destino, la retirada se completa en él (fila «SIN APROBACIÓN VIGENTE») y el cierre sigue rechazado (código 4)",
         rc3 == 4 and retirada(c.extra) and e.get("estado") != "retirada_pendiente" and not os.path.exists(os.path.join(c.d, "ficha.json")), f"código {rc3} · {e.get('estado')}")


def grupo_e(exp):
    G = "E reanudación y cierre legítimo"
    c = escenario_respuesta(exp)[0].copiar("e_reanudacion")
    original = open(c.aud, "rb").read()
    sid0 = (c.st().get("auditoria_respuesta") or {}).get("solicitud")
    m_mismas_palabras(c)
    rc1, _, _ = corre("pipeline.py", c.d, "--desde", "14")
    open(c.aud, "wb").write(original)  # se restaura la respuesta aceptada: no reactiva un cierre ya retirado
    rc2, out2, _ = corre("pipeline.py", c.d, "--desde", "14")
    paso(G, "tras la retirada, restaurar los bytes de la respuesta original no reactiva el cierre (código 4, sin ficha)", rc1 == 4 and rc2 == 4 and not os.path.exists(os.path.join(c.d, "ficha.json")), f"{rc1} {rc2}")
    rc3, _, _ = corre("pipeline.py", c.d, "--desde", "13")
    sols = c.st().get("solicitudes_auditoria") or []
    nueva = sols[-1]["id"] if sols else None
    rc4, _, ult4 = corre("pipeline.py", c.d)  # la respuesta original no responde a la solicitud nueva
    AG.auditoria(c.d, "APROBADO")
    open(c.aud, "a", encoding="utf-8").write("Aviso: auditoría sintética nueva de la prueba R-V1 sobre el material vigente.\n")
    rc5, out5, ult5 = corre("pipeline.py", c.d)
    rcr, _, _ = corre("resumen.py", c.d, c.extra)
    st = c.st()
    paso(G, "--desde 13 registra una solicitud nueva (código 10), la respuesta original no la responde y una respuesta legítima nueva cierra (código 0) y se vuelve a publicar en los dos destinos",
         rc3 == 10 and nueva and nueva != sid0 and rc4 == 10 and rc5 == 0 and ult5 == "estado final: concluido · paso 14" and rcr == 0
         and (st.get("auditoria_respuesta") or {}).get("solicitud") == nueva and aprobada(c.pred) and aprobada(c.extra), f"{rc3} {rc4} {rc5} {rcr} · {ult5[:60]}")
    rets = [j(os.path.join(c.d, "historial_cierres", a), "RETIRADA.json") or {} for a in c.archivos_historial()]
    paso(G, "el historial conserva el cierre retirado con su motivo y la auditoría del momento de la retirada", any(CAMBIO in (r.get("motivo") or "") for r in rets), str(len(rets)))


def grupo_f(exp):
    G = "F compatibilidad con cierres históricos"
    c0, rcr = escenario_historico(exp)
    hu = c0.archivos_historial()
    for via, llamada, _ in VIAS:
        c = c0.copiar(f"f_hist_{via.split('.')[0].replace(' ', '')}")
        rc, out, ult = llamada(c)
        ok, det = observa_vigente(c, rc, via, hu)
        st = c.st()
        paso(G, f"cierre de la 4.6.1 sin solicitudes · {via}: sigue vigente y no recibe ninguna solicitud ni respuesta retroactiva",
             rcr == 0 and ok and not st.get("solicitudes_auditoria") and "auditoria_respuesta" not in st, det)
    c = c0.copiar("f_hist_crlf")
    m_crlf(c)
    aud = sha(c.aud)
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_retirada(c, rc, out, 4, aud, "cierre_vigente.json")
    paso(G, "cierre de la 4.6.1 con su auditoría guardada en CRLF: sin huella fiel registrada no se acredita (huella de bytes) y se retira, sin calcular una nueva", ok and "auditoria_respuesta" not in c.st(), det)
    # cierre de la 4.8.1: respuesta registrada sin huella fiel (se simula quitando el campo que la 4.9 añade)
    c1 = escenario_respuesta(exp)[0].copiar("f_481_base")
    st = c1.st()
    (st.get("auditoria_respuesta") or {}).pop("fiel", None)
    json.dump(st, open(os.path.join(c1.d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cv = j(c1.d, CIE.CIERRE_VIGENTE) or {}
    cv.pop("auditoria_fiel", None)
    json.dump(cv, open(os.path.join(c1.d, CIE.CIERRE_VIGENTE), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    hu1 = c1.archivos_historial()
    c = c1.copiar("f_481_intacto")
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_vigente(c, rc, "paso 14", hu1)
    paso(G, "cierre de la 4.8.1 (respuesta sin huella fiel registrada) con los bytes idénticos: sigue vigente y no se le atribuye ninguna huella nueva",
         ok and "fiel" not in (c.st().get("auditoria_respuesta") or {}), det)
    # cierre de la 4.9 sin estado_pipeline.json: cierre_vigente.json lleva la solicitud y la huella fiel de la respuesta
    c2 = escenario_respuesta(exp)[0]
    cv = j(c2.d, CIE.CIERRE_VIGENTE) or {}
    paso(G, "cierre de la 4.9: cierre_vigente.json registra la solicitud y la huella fiel de la respuesta aceptada",
         bool(cv.get("solicitud")) and cv.get("auditoria_fiel") == (c2.st().get("auditoria_respuesta") or {}).get("fiel"), str({k: str(cv.get(k))[:14] for k in ("solicitud", "auditoria_fiel")}))
    for etiqueta, mut, rc_esp, vigente in (("intacta", None, 0, True), ("con las mismas palabras reordenadas", m_mismas_palabras, 3, False), ("con la solicitud cambiada", m_solicitud_cambiada, 3, False)):
        c = c2.copiar(f"f_sin_estado_{(mut or (lambda x: None)).__name__}")
        os.remove(os.path.join(c.d, "estado_pipeline.json"))
        if mut:
            mut(c)
        rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
        ok = (rc == rc_esp and bool((j(c.d, "ficha.json") or {}).get("cierre")) == vigente and aprobada(c.pred) == vigente and retirada(c.pred) == (not vigente)
              and (vigente or "cierre_vigente.json" in ((c.ultima_retirada() or {}).get("motivo") or "")))
        paso(G, f"sin estado_pipeline.json, respuesta {etiqueta} · ficha.py: " + ("el cierre sigue vigente (código 0)" if vigente else "se retira la aprobación (código 3) por cierre_vigente.json"), ok,
             f"código {rc} · ficha cerrada {bool((j(c.d, 'ficha.json') or {}).get('cierre'))} · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]}")
    # el estado del pipeline ya no registra la solicitud como respondida por esa respuesta
    c = c2.copiar("f_solicitud_no_respondida")
    st = c.st()
    for s in st.get("solicitudes_auditoria") or []:
        if s.get("id") == (st.get("auditoria_respuesta") or {}).get("solicitud"):
            s["estado"] = "sustituida"
    json.dump(st, open(os.path.join(c.d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    aud = sha(c.aud)
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_retirada(c, rc, out, 4, aud, "no consta en estado_pipeline.json como respondida")
    paso(G, "la solicitud de la respuesta ya no consta como respondida en estado_pipeline.json: se retira la aprobación (código 4)", ok, det)
    for etiqueta, mut in (("guardada en CRLF", m_crlf), ("con las mismas palabras reordenadas", m_mismas_palabras)):
        c = c1.copiar(f"f_481_{mut.__name__}")
        mut(c)
        aud = sha(c.aud)
        rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
        ok, det = observa_retirada(c, rc, out, 4, aud, "no puede acreditarse")
        paso(G, f"cierre de la 4.8.1 con la respuesta {etiqueta}: la correspondencia no puede acreditarse con la huella de bytes y se retira (código 4)",
             ok and "fiel" not in (c.st().get("auditoria_respuesta") or {}), det)


def escenario_46(exp):
    """Cierre de la 4.6 (…_4_6/Vidrala: ficha cerrada y material fijado, SIN cierre_vigente.json ni solicitudes de origen)."""
    base = os.path.join(TMP, "escenario_46")
    c = Caso(base)
    e46 = os.path.join(os.path.dirname(os.path.dirname(exp)), "2026-11_Vidrala_ensayo_4_6", "Vidrala")
    shutil.copytree(e46, c.d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(e46), f)):
            shutil.copy2(os.path.join(os.path.dirname(e46), f), os.path.join(base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    return c


def otra_aprobacion(c):
    """Otra auditoría sintética APROBADO del material fijado, sin línea de solicitud (la que encontró la auditoría interna, Z-1)."""
    if os.path.exists(os.path.join(c.d, "solicitud_auditoria.json")):
        os.remove(os.path.join(c.d, "solicitud_auditoria.json"))
    AG.auditoria(c.d, "APROBADO", solicitud=False)
    open(c.aud, "a", encoding="utf-8").write("Aviso: auditoría sintética de la prueba R-V1 que no es la aprobada.\n")


def grupo_h(exp):
    G = "H hallazgos de la auditoría interna de la 4.9 (Z-1, Z-2, Z-3)"
    NO_CONSTA = "no consta la respuesta de auditoría aprobada"
    # Z-1 · sin registro de la respuesta aprobada, ninguna vía vuelve a cerrar ni atribuye la huella del archivo actual
    c0 = escenario_historico(exp)[0]
    for via, llamada, rc_esp in VIAS:
        c = c0.copiar(f"h_461_sin_cv_{via.split('.')[0].replace(' ', '')}")
        os.remove(os.path.join(c.d, CIE.CIERRE_VIGENTE))
        otra_aprobacion(c)
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, NO_CONSTA)
        paso(G, f"cierre de la 4.6.1 sin cierre_vigente.json y con otra aprobación del material · {via}: no se vuelve a cerrar ni se crea un cierre_vigente.json con la huella del archivo actual (código {rc_esp})",
             ok and not os.path.exists(os.path.join(c.d, CIE.CIERRE_VIGENTE)), det)
    c = escenario_46(exp)
    otra_aprobacion(c)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    paso(G, "cierre de la 4.6 (sin cierre_vigente.json de origen) con otra aprobación · ficha.py: código 3, ninguna ficha cerrada y ningún cierre_vigente.json creado",
         rc == 3 and not (j(c.d, "ficha.json") or {}).get("cierre") and not os.path.exists(os.path.join(c.d, CIE.CIERRE_VIGENTE)) and NO_CONSTA in out, ult[:140])
    c = escenario_respuesta(exp)[0].copiar("h_49_sin_estado_ni_cv")
    for f in ("estado_pipeline.json", CIE.CIERRE_VIGENTE):
        os.remove(os.path.join(c.d, f))
    otra_aprobacion(c)
    aud = sha(c.aud)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    ok, det = observa_retirada(c, rc, out, 3, aud, NO_CONSTA)
    paso(G, "cierre de la 4.9 sin estado_pipeline.json ni cierre_vigente.json y con otra aprobación · ficha.py: código 3, aprobación retirada en los dos destinos", ok and not os.path.exists(os.path.join(c.d, CIE.CIERRE_VIGENTE)), det)
    # Z-2 · auditoria.md que no es UTF-8 y archivos de control ilegibles: se retira, sin interrumpir ninguna vía
    c1 = escenario_respuesta(exp)[0]
    for via, llamada, rc_esp in VIAS:
        c = c1.copiar(f"h_no_utf8_{via.split('.')[0].replace(' ', '')}")
        open(c.aud, "ab").write(b"\nAviso: inversi\xf3n\n")
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, "no es texto UTF-8 válido")
        paso(G, f"auditoria.md con un byte que no es UTF-8 · {via}: aprobación retirada (código {rc_esp}) sin traza", ok and "Traceback" not in out, det)
    c = c1.copiar("h_cp1252")
    t = leer(c.d, "auditoria.md")
    open(c.aud, "w", encoding="cp1252", errors="replace").write(t)
    aud = sha(c.aud)
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_retirada(c, rc, out, 4, aud, "no es texto UTF-8 válido")
    paso(G, "la respuesta guardada en cp1252 · paso 14: aprobación retirada (código 4) sin traza", ok and "Traceback" not in out, det)
    for via, llamada, rc_esp in (VIAS[1], VIAS[2]):
        c = c1.copiar(f"h_cv_ilegible_{via.split('.')[0]}")
        open(os.path.join(c.d, CIE.CIERRE_VIGENTE), "w", encoding="utf-8").write("{ilegible")
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, "cierre_vigente.json no se puede leer")
        paso(G, f"cierre_vigente.json ilegible · {via}: aprobación retirada (código {rc_esp}) sin traza", ok and "Traceback" not in out, det)
    c = c1.copiar("h_estado_ilegible_ficha")
    open(os.path.join(c.d, "estado_pipeline.json"), "w", encoding="utf-8").write("")
    aud = sha(c.aud)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    ok, det = observa_retirada(c, rc, out, 3, aud, "estado_pipeline.json no se puede leer")
    paso(G, "estado_pipeline.json vacío · ficha.py: aprobación retirada (código 3) sin traza", ok and "Traceback" not in out, det)
    c = c1.copiar("h_estado_ilegible_pipeline")
    open(os.path.join(c.d, "estado_pipeline.json"), "w", encoding="utf-8").write("{ilegible")
    aud = sha(c.aud)
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_retirada(c, rc, out, 6, aud, "estado_pipeline.json no se puede leer")
    paso(G, "estado_pipeline.json ilegible · pipeline.py: no puede continuar (código 6, «ESTADO DEL PIPELINE ILEGIBLE») pero antes retira la aprobación, sin traza",
         ok and "ESTADO DEL PIPELINE ILEGIBLE" in out and "Traceback" not in out, det)
    # Z-3 · sin estado, una transformación inocua sigue vigente gracias a la huella fiel de cierre_vigente.json (no por bytes)
    c = c1.copiar("h_sin_estado_crlf")
    os.remove(os.path.join(c.d, "estado_pipeline.json"))
    m_crlf(c)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    paso(G, "cierre de la 4.9 sin estado_pipeline.json y con la respuesta en CRLF · ficha.py: sigue vigente por la huella fiel de cierre_vigente.json (código 0)",
         rc == 0 and bool((j(c.d, "ficha.json") or {}).get("cierre")) and aprobada(c.pred) and aprobada(c.extra), f"código {rc} · {ult[:100]}")


def grupo_i(exp):
    G = "I hallazgos de los controles de vigencia de la 4.9 (V-1 a V-3, W-1, W-2 y W-4)"
    c1 = escenario_respuesta(exp)[0]
    # V-1 · material_auditoria.json ilegible: se retira por las cuatro vías, sin traza
    for via, llamada, rc_esp in VIAS:
        c = c1.copiar(f"i_material_ilegible_{via.split('.')[0].replace(' ', '')}")
        open(os.path.join(c.d, "material_auditoria.json"), "w", encoding="utf-8").write("{trunc")
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, "material_auditoria.json no se puede leer")
        paso(G, f"material_auditoria.json ilegible · {via}: aprobación retirada (código {rc_esp}) sin traza", ok and "Traceback" not in out, det)
    # V-1 · ficha.json ilegible: el paso 14, informe.py y resumen.py retiran; ficha.py tampoco vuelve a cerrar (W-2): la archiva como
    # antecedente, retira la aprobación y el cierre exige una auditoría nueva (sin traza en ningún caso)
    for via, llamada, rc_esp in (VIAS[0], VIAS[2], VIAS[3]):
        c = c1.copiar(f"i_ficha_ilegible_{via.split('.')[0].replace(' ', '')}")
        open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8").write("{trunc")
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ret = c.ultima_retirada() or {}
        ok = (rc == rc_esp and "Traceback" not in out and not os.path.exists(os.path.join(c.d, "ficha.json")) and retirada(c.pred) and retirada(c.extra)
              and "ficha.json no se puede leer" in (ret.get("motivo") or "") and sha(c.aud) == aud)
        paso(G, f"ficha.json ilegible · {via}: aprobación retirada (código {rc_esp}) sin traza; la ficha ilegible queda archivada",
             ok, f"código {rc} · {ult[:90]} · retirada: {(ret.get('motivo') or '')[:90]}")
    c = c1.copiar("i_ficha_ilegible_ficha")
    open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8").write("{trunc")
    aud = sha(c.aud)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    ok, det = observa_retirada(c, rc, out, 3, aud, "ficha.json no se puede leer")
    rc2, out2, ult2 = corre("informe.py", c.d)
    paso(G, "ficha.json ilegible · ficha.py: no vuelve a cerrar (código 3); la ficha ilegible queda archivada, la aprobación se retira en los dos destinos y "
         "la llamada siguiente de informe.py no publica nada (segundo control de vigencia, W-2)", ok and "Traceback" not in out and rc2 == 3 and not os.path.exists(os.path.join(c.d, "informe.md")), det)
    c = c1.copiar("i_ficha_ilegible_ficha_sin_estado")
    os.remove(os.path.join(c.d, "estado_pipeline.json"))
    open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8").write("{trunc")
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    paso(G, "ficha.json ilegible y sin estado · ficha.py: no vuelve a cerrar ni crea un cierre_vigente.json más débil (código 3, aprobación retirada en los dos destinos)",
         rc == 3 and "Traceback" not in out and not os.path.exists(os.path.join(c.d, "ficha.json")) and not os.path.exists(os.path.join(c.d, CIE.CIERRE_VIGENTE))
         and retirada(c.pred) and retirada(c.extra), f"código {rc} · {ult[:100]}")
    # W-1 · estructura interna de la ficha y del estado
    def ficha_cierre_texto(c):
        F = j(c.d, "ficha.json")
        F["cierre"] = "APROBADO"
        json.dump(F, open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"))
    def solicitud_sin_id(c):
        st = c.st()
        st["solicitudes_auditoria"] = (st.get("solicitudes_auditoria") or []) + [{"estado": "pendiente"}]
        json.dump(st, open(os.path.join(c.d, "estado_pipeline.json"), "w", encoding="utf-8"))
    for nombre, mutar, (via, llamada, rc_esp), diag in (("ficha.json con «cierre» que no es un objeto", ficha_cierre_texto, VIAS[3], "«cierre» no es un objeto"),
                                                        ("ficha.json con «cierre» que no es un objeto", ficha_cierre_texto, VIAS[1], "«cierre» no es un objeto"),
                                                        ("una solicitud pendiente sin «id»", solicitud_sin_id, VIAS[1], "solicitudes con «id»")):
        c = c1.copiar("i_" + re.sub(r"\W+", "_", nombre + via))
        mutar(c)
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, diag)
        paso(G, f"{nombre} · {via}: aprobación retirada (código {rc_esp}) sin traza (W-1)", ok and "Traceback" not in out, det)
    for nombre, mutar in (("solicitudes_auditoria como objeto", lambda c: json.dump(dict(c.st(), solicitudes_auditoria={"x": 1}), open(os.path.join(c.d, "estado_pipeline.json"), "w"))),
                          ("«historial» como objeto y auditoria.md que no es UTF-8", lambda c: (json.dump(dict(c.st(), historial={"x": 1}), open(os.path.join(c.d, "estado_pipeline.json"), "w")),
                                                                                              open(c.aud, "ab").write(b"\nAviso: inversi\xf3n\n")))):
        c = c1.copiar("i_" + re.sub(r"\W+", "_", nombre) + "_paso14")
        mutar(c)
        rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
        paso(G, f"{nombre} · paso 14: código 6 después de retirar la aprobación en los dos destinos, sin traza (W-1)",
             rc == 6 and "Traceback" not in out and not os.path.exists(os.path.join(c.d, "ficha.json")) and retirada(c.pred) and retirada(c.extra), f"código {rc} · {ult[:100]}")
    # W-4 · un identificador de material con «../» no saca el archivo del expediente
    c = c1.copiar("i_material_con_ruta")
    F = j(c.d, "ficha.json")
    F["cierre"]["material_auditado"] = "../../../../fuera"
    json.dump(F, open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"))
    rc, out, ult = corre("resumen.py", c.d, c.pred)
    fuera = [p for p in glob.glob(os.path.join(c.base, "**", "RETIRADA.json"), recursive=True) if not os.path.abspath(p).startswith(os.path.join(os.path.abspath(c.d), "historial_cierres") + os.sep)]
    paso(G, "ficha.json con material_auditado «../../../../fuera» · resumen.py: la retirada se archiva dentro de historial_cierres/ del expediente (W-4)",
         rc == 3 and not fuera and c.archivos_historial() and "Traceback" not in out, f"código {rc} · fuera {fuera} · {c.archivos_historial()}")
    # V-2 · JSON válido que no es un objeto, estructura interna errónea o un archivo de control que es una carpeta
    casos = (("estado_pipeline.json = []", lambda c: open(os.path.join(c.d, "estado_pipeline.json"), "w").write("[]"), VIAS[1], "estado_pipeline.json no se puede leer"),
             ("cierre_vigente.json = [1]", lambda c: open(os.path.join(c.d, CIE.CIERRE_VIGENTE), "w").write("[1]"), VIAS[1], "cierre_vigente.json no se puede leer"),
             ("solicitudes_auditoria como objeto", lambda c: json.dump(dict(c.st(), solicitudes_auditoria={"x": 1}), open(os.path.join(c.d, "estado_pipeline.json"), "w")), VIAS[2], "solicitudes_auditoria no es una lista"),
             ("auditoria_respuesta como texto", lambda c: json.dump(dict(c.st(), auditoria_respuesta="x"), open(os.path.join(c.d, "estado_pipeline.json"), "w")), VIAS[3], "auditoria_respuesta no es un objeto"))
    for nombre, mutar, (via, llamada, rc_esp), diag in casos:
        c = c1.copiar("i_" + re.sub(r"\W+", "_", nombre))
        mutar(c)
        aud = sha(c.aud)
        rc, out, ult = llamada(c)
        ok, det = observa_retirada(c, rc, out, rc_esp, aud, diag)
        paso(G, f"{nombre} · {via}: aprobación retirada (código {rc_esp}) sin traza", ok and "Traceback" not in out, det)
    c = c1.copiar("i_estado_lista_pipeline")
    open(os.path.join(c.d, "estado_pipeline.json"), "w").write("[]")
    aud = sha(c.aud)
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    ok, det = observa_retirada(c, rc, out, 6, aud, "estado_pipeline.json no se puede leer")
    paso(G, "estado_pipeline.json = [] · pipeline.py: código 6 después de retirar, sin traza", ok and "ESTADO DEL PIPELINE ILEGIBLE" in out and "Traceback" not in out, det)
    c = c1.copiar("i_estado_carpeta_pipeline")
    os.remove(os.path.join(c.d, "estado_pipeline.json"))
    os.makedirs(os.path.join(c.d, "estado_pipeline.json"))
    rc, out, ult = corre("pipeline.py", c.d, "--desde", "14")
    paso(G, "estado_pipeline.json es una carpeta · pipeline.py: código 6 después de retirar la aprobación en los dos destinos, sin traza",
         rc == 6 and "Traceback" not in out and not os.path.exists(os.path.join(c.d, "ficha.json")) and retirada(c.pred) and retirada(c.extra), f"código {rc} · {ult[:100]}")
    c = c1.copiar("i_auditoria_carpeta")
    os.remove(c.aud)
    os.makedirs(c.aud)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    ret = c.ultima_retirada() or {}
    paso(G, "auditoria.md es una carpeta · ficha.py: aprobación retirada (código 3) en los dos destinos, sin traza",
         rc == 3 and "Traceback" not in out and not os.path.exists(os.path.join(c.d, "ficha.json")) and retirada(c.pred) and retirada(c.extra)
         and "auditoria.md no se puede leer" in (ret.get("motivo") or ""), f"código {rc} · {ult[:100]} · retirada: {(ret.get('motivo') or '')[:80]}")
    # V-3 · sin estado, ficha.py conserva en cierre_vigente.json la solicitud, la huella fiel y la huella de bytes de la respuesta aceptada
    c = c1.copiar("i_sin_estado_crlf_registro")
    os.remove(os.path.join(c.d, "estado_pipeline.json"))
    cv0 = j(c.d, CIE.CIERRE_VIGENTE)
    original = open(c.aud, "rb").read()
    m_crlf(c)
    rc, out, ult = corre("ficha.py", c.d, "--estado", "concluido")
    cv1 = j(c.d, CIE.CIERRE_VIGENTE) or {}
    escribir(c, original.decode("utf-8"))
    rc2, out2, ult2 = corre("ficha.py", c.d, "--estado", "concluido")
    cv2 = j(c.d, CIE.CIERRE_VIGENTE) or {}
    claves = ("solicitud", "auditoria_fiel", "auditoria_sha256")
    paso(G, "cierre de la 4.9 sin estado y con la respuesta en CRLF · ficha.py: cierre_vigente.json conserva la solicitud, la huella fiel y la huella de bytes de la respuesta "
         "aceptada; al restaurar los bytes originales sigue vigente (código 0 las dos veces)",
         rc == 0 and rc2 == 0 and all(cv1.get(k) == cv0.get(k) for k in claves) and all(cv2.get(k) == cv0.get(k) for k in claves) and bool((j(c.d, "ficha.json") or {}).get("cierre")),
         f"códigos {rc}/{rc2} · {[k for k in claves if cv1.get(k) != cv0.get(k)]} · {ult2[:80]}")


def grupo_g():
    G = "G unidades"
    fiel = getattr(CIE, "huella_fiel", None)
    base = "# a\n\n1. PASA · x\nAviso: La evidencia respalda el crecimiento; la reposición queda pendiente.\nVEREDICTO: APROBADO\n"
    if fiel is None:
        paso(G, "cierre_v2.huella_fiel existe", False)
    else:
        inocuas = [base.replace("\n", "\r\n"), base.replace("\n", "\r"), "﻿" + base, base.rstrip("\n"), base + "\n\n", unicodedata.normalize("NFD", base)]
        relevantes = [base.replace("el crecimiento; la reposición", "la reposición; el crecimiento"), base.replace("respalda", "no respalda"),
                      base.replace("PASA", "pasa"), base + "Solicitud de auditoría: SA-0123456789abcdef\n", base.replace("1. PASA", "1.  PASA"),
                      "\n".join(reversed(base.rstrip("\n").split("\n"))) + "\n", base.replace("reposición", "reposicion")]
        h0 = fiel(base.encode("utf-8"))
        paso(G, "huella_fiel: iguales con CRLF, CR, BOM, sin o con saltos finales y NFD", all(fiel(x.encode("utf-8")) == h0 for x in inocuas))
        paso(G, "huella_fiel: distinta con otro orden de palabras, una negación, mayúsculas, la línea de solicitud, un espacio, el orden de líneas y una tilde",
             all(fiel(x.encode("utf-8")) != h0 for x in relevantes))
        limites = [base.replace("2 · x", "2² · x").replace("1. PASA · x", "1. PASA · x²"), base.replace("crecimiento", "creci\u200bmiento"), base.replace("la reposición", "la\u00a0reposición"),
                   base.replace("\nAviso", "\u2028Aviso"), base.replace("\nAviso", "\x0bAviso")]
        paso(G, "huella_fiel: fuera de la lista cerrada, también son distintos un carácter de compatibilidad (NFKC: «²»), un espacio de anchura cero, un espacio no separable y los separadores U+2028 y VT",
             fiel(limites[0].encode("utf-8")) != fiel(limites[0].replace("²", "2").encode("utf-8")) and all(fiel(x.encode("utf-8")) != h0 for x in limites[1:]))
        paso(G, "huella_contenido (detector A) sigue siendo un detector conservador: no distingue el orden de las palabras ni la línea de solicitud, y por eso no acredita la identidad",
             CIE.huella_contenido(relevantes[0]) == CIE.huella_contenido(base) and CIE.huella_contenido(relevantes[3]) == CIE.huella_contenido(base)
             and "detector" in (CIE.huella_contenido.__doc__ or "").lower())
    h = hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest()
    paso(G, "Pipeline.veredicto_auditoria es idéntica a la de la 4.7.1 (H2 sin cambios)", h == H2_SHA_4_7_1, h[:16])


def main(exp):
    for g in (grupo_a, grupo_b, grupo_c, grupo_d, grupo_e, grupo_f, grupo_h, grupo_i):
        try:
            g(exp)
        except Exception as e:  # noqa
            import traceback
            traceback.print_exc()
            paso(g.__name__, "excepción " + str(e)[:100], False)
    grupo_g()


if __name__ == "__main__":
    try:
        main(os.path.abspath(ARGS.expediente))
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    n = sum(ok for _, _, ok, _ in R)
    if ARGS.json:
        json.dump({"codigo": ARGS.codigo or "personaje_v2/scripts (árbol)", "pruebas": [{"grupo": g, "prueba": p, "pasa": ok, "detalle": d} for g, p, ok, d in R]},
                  open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"\n{n}/{len(R)} pruebas de integridad de la auditoría vigente PASAN")
    sys.exit(0 if n == len(R) else 1)
