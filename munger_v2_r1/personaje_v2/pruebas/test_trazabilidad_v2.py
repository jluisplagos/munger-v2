#!/usr/bin/env python3
"""Batería de trazabilidad de la entrega 4.10 (encargo 4.10 §3.2, §3.3 y §3.4). Obligatoria en `verificar_paquete.sh completa`.

Uso (desde personaje_v2/): python3 -B pruebas/test_trazabilidad_v2.py [--expediente DIR] [--codigo DIR] [--json SALIDA]
  --codigo DIR: sustituye los .py de personaje_v2/scripts/ por los de DIR en una copia temporal (reproducción con el código de la 4.9).

Grupos:
  B · BOM y transformaciones inocuas (§3.2): una respuesta aceptada que empieza directamente por «1. PASA» (o por la línea de
      material o de solicitud) sigue vigente con BOM, con CRLF y en NFD, en las cuatro vías (paso 14, ficha.py, informe.py,
      resumen.py); una respuesta aceptada que YA traía el BOM cierra; el caso con preámbulo; regresiones negativas con BOM
      (solicitud distinta, ausente o duplicada; mismas palabras con el significado contrario); el cierre sin huella fiel (4.8.1)
      sigue sujeto a sus bytes exactos; las huellas de bytes siguen siendo las de los bytes reales.
  M · ficha que pierde sus marcadores de cierre (§3.3): «cierre» eliminado, estado cambiado a pendiente_de_datos, ambos, ficha {} y
      ambos con cierre_vigente.json borrado (revisión interna R-1):
      la primera llamada de cada vía retira en todos los destinos registrados, conserva el historial y no deja aprobaciones
      incoherentes; un estado temprano legítimo sin cierre previo no se retira; restaurar los bytes o regenerar la ficha no
      reactiva la aprobación; con un destino inaccesible, código 5.
  L · acreditación del libro final (§3.4, P-N2): incorporación efectiva de cachés, ruta sin copia recalculada, detección de una
      modificación posterior y correspondencia con la ficha (4.10.1, T-1: con fichas sintéticas preparadas con la identidad del libro
      recién acreditado ANTES de la precondición, y cada mutación en su copia); comprobante ilegible; falta de correspondencia;
      reconstrucción con bytes distintos e inocuos e identidad estricta del archivo acreditado; igualdad independiente del archivo final de los expedientes de la 4.10
      con su comprobante (en la verificación del paquete, el árbol es el extraído del ZIP).
No arranca LibreOffice (verificar_v63 y add_cached_values son Python), pero se ejecuta en secuencia con las demás, como todas.
"""
import argparse
import csv
import hashlib
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
ap.add_argument("--codigo", help="carpeta con los .py (y .sh) que sustituyen a los de personaje_v2/scripts/")
ap.add_argument("--json")
ARGS = ap.parse_args()
TMP = tempfile.mkdtemp(prefix="trazabilidad410_")


def arbol_de_codigo():
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
        if f.endswith((".py", ".sh")):
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
FRASE = "Aviso: La evidencia respalda el crecimiento; la reposición queda pendiente. (auditoría sintética de la prueba 4.10)"
FRASE_CONTRARIA = "Aviso: La evidencia respalda la reposición; el crecimiento queda pendiente. (auditoría sintética de la prueba 4.10)"
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


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def corre(script, *args):
    pre = ["bash"] if script.endswith(".sh") else [PY, "-B"]
    r = subprocess.run(pre + [os.path.join(SCR, script), *args], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out, (out.splitlines() or [""])[-1]


def filas(csv_path, empresa=EMPRESA):
    if not os.path.isfile(csv_path):
        return []
    return [r for r in csv.DictReader(open(csv_path, encoding="utf-8")) if empresa is None or r.get("empresa") == empresa]


def aprobada(p):
    f = filas(p)
    return len(f) == 1 and f[0].get("estado_analisis") == "concluido" and f[0].get("verificacion") == "APROBADO"


def retirada(p):
    f = filas(p)
    return len(f) == 1 and (f[0].get("verificacion") or "").startswith(CIE.NO_VIGENTE)


def incoherentes(p):
    """Filas que presentan una aprobación sin respaldo: APROBADO sin empresa, o APROBADO en un estado que no es concluido."""
    return [(r.get("empresa"), r.get("estado_analisis")) for r in filas(p, None)
            if r.get("verificacion") == "APROBADO" and (not r.get("empresa") or (r.get("empresa") == EMPRESA and r.get("estado_analisis") != "concluido"))]


class Caso:
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

    def historial(self):
        h = os.path.join(self.d, "historial_cierres")
        return sorted(os.listdir(h)) if os.path.isdir(h) else []

    def ultima_retirada(self):
        a = self.historial()
        return j(os.path.join(self.d, "historial_cierres", a[-1]), "RETIRADA.json") if a else None


def forma(txt, primera):
    """Reordena una auditoría sintética: sin el preámbulo, con la línea `primera` («punto», «material» o «solicitud») al principio."""
    ls = [l for l in txt.splitlines() if l.strip() and not l.startswith("# auditoría")]
    if primera == "material":
        ls = [l for l in ls if l.startswith("Material auditado")] + [l for l in ls if not l.startswith("Material auditado")]
    elif primera == "solicitud":
        ls = [l for l in ls if l.startswith("Solicitud de auditor")] + [l for l in ls if not l.startswith("Solicitud de auditor")]
    elif primera == "preambulo":
        return txt
    return "\n".join(ls) + "\n"


ESC = {}


def escenario(nombre, primera="punto", bom_al_responder=False, frase=FRASE, antes_de_auditar=None):
    """Cierre de la 4.9/4.10 sobre una copia del de la 4.6.1: --desde 13 (lo archiva y registra una solicitud), respuesta sintética
    APROBADO con la forma `primera`, cierre y publicación también en un destino configurado. Devuelve (Caso, rc13, rc, rcr)."""
    if nombre in ESC:
        return ESC[nombre]
    c = Caso(os.path.join(TMP, "esc_" + nombre))
    shutil.copytree(ARGS.expediente, c.d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(ARGS.expediente), f)):
            shutil.copy2(os.path.join(os.path.dirname(ARGS.expediente), f), os.path.join(c.base, "exp", f))
    os.makedirs(os.path.dirname(c.extra))
    if antes_de_auditar:
        antes_de_auditar(c)
    rc13, _, _ = corre("pipeline.py", c.d, "--desde", "13")
    AG.auditoria(c.d, "APROBADO")
    txt = forma(open(c.aud, encoding="utf-8").read(), primera) + frase + "\n"
    open(c.aud, "wb").write((b"\xef\xbb\xbf" if bom_al_responder else b"") + txt.encode("utf-8"))
    rc, _, _ = corre("pipeline.py", c.d)
    rcr, _, _ = corre("resumen.py", c.d, c.extra)
    ESC[nombre] = (c, rc13, rc, rcr)
    return ESC[nombre]


def cerrado(c, rc):
    st = c.st()
    return (rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and (j(c.d, "ficha.json") or {}).get("cierre")
            and os.path.exists(os.path.join(c.d, "cierre_vigente.json")))


VIAS = (("paso 14", lambda c: corre("pipeline.py", c.d, "--desde", "14"), 4),
        ("ficha.py", lambda c: corre("ficha.py", c.d, "--estado", "concluido"), 3),
        ("informe.py", lambda c: corre("informe.py", c.d), 3),
        ("resumen.py", lambda c: corre("resumen.py", c.d, c.pred), 3))


def vigente(c, rc, hist_antes):
    st = c.st()
    ok = (rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and (j(c.d, "ficha.json") or {}).get("cierre")
          and os.path.exists(os.path.join(c.d, "cierre_vigente.json")) and aprobada(c.pred) and aprobada(c.extra) and c.historial() == hist_antes)
    return ok, f"código {rc} · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r} · pred {[(r.get('verificacion') or '')[:24] for r in filas(c.pred)]} · retiradas nuevas {len(c.historial()) - len(hist_antes)}"


def retiro(c, rc, rc_esp, hist_antes, diagnostico=None):
    st = c.st()
    ret = c.ultima_retirada() or {}
    hp = os.path.join(os.path.dirname(c.pred), "resumen_v2_historial.csv")
    hist = list(csv.DictReader(open(hp, encoding="utf-8"))) if os.path.exists(hp) else []
    ok = (rc == rc_esp and len(c.historial()) == len(hist_antes) + 1 and not os.path.exists(os.path.join(c.d, "cierre_vigente.json"))
          and st.get("auditoria") is None and st.get("estado_analisis") in (None, "") and retirada(c.pred) and retirada(c.extra)
          and any(r.get("verificacion") == "APROBADO" for r in hist) and not incoherentes(c.pred) and not incoherentes(c.extra)
          and (diagnostico is None or diagnostico in (ret.get("motivo") or "")))
    return ok, (f"código {rc} (esperado {rc_esp}) · estado {st.get('estado_analisis')!r} · auditoría {st.get('auditoria')!r} · cv {os.path.exists(os.path.join(c.d, 'cierre_vigente.json'))}"
                f" · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]} · extra {[(r.get('verificacion') or '')[:22] for r in filas(c.extra)]}"
                f" · incoherentes {incoherentes(c.pred) + incoherentes(c.extra)} · retirada: {(ret.get('motivo') or '')[:110]}")


def con_bom(c):
    b = open(c.aud, "rb").read()
    if not b.startswith(b"\xef\xbb\xbf"):
        open(c.aud, "wb").write(b"\xef\xbb\xbf" + b)


def con_crlf(c):
    t = open(c.aud, "rb").read().replace(b"\r\n", b"\n")
    open(c.aud, "wb").write(t.replace(b"\n", b"\r\n"))


def con_nfd(c):
    b = open(c.aud, "rb").read()
    pre = b"\xef\xbb\xbf" if b.startswith(b"\xef\xbb\xbf") else b""
    t = b[len(pre):].decode("utf-8")
    open(c.aud, "wb").write(pre + unicodedata.normalize("NFD", t).encode("utf-8"))


# ---------------- grupo B · BOM ----------------
def grupo_b():
    c0, rc13, rc, rcr = escenario("bom_respuesta", "punto", bom_al_responder=True)
    paso("B", "respuesta nueva aceptada con BOM ante «1. PASA»: el pipeline la consume y cierra (código 0, concluido, APROBADO, cierre_vigente.json)",
         cerrado(c0, rc) and open(c0.aud, "rb").read().startswith(b"\xef\xbb\xbf1. PASA") and rcr == 0, f"códigos {rc13}/{rc}/{rcr} · estado {c0.st().get('estado_analisis')!r} · auditoría {c0.st().get('auditoria')!r}")
    resp = c0.st().get("auditoria_respuesta") or {}
    paso("B", "la huella de bytes registrada es la de los bytes reales (con BOM) y la fiel, la del texto normalizado (distintas de las del texto sin BOM)",
         resp.get("sha256") == sha(c0.aud) and resp.get("fiel") == CIE.huella_fiel(open(c0.aud, "rb").read()[3:]) and resp.get("sha256") != hashlib.sha256(open(c0.aud, "rb").read()[3:]).hexdigest())
    for via, f, _ in VIAS:
        c = c0.copiar(f"bom_respuesta_{via.replace(' ', '_')}")
        h0 = c.historial()
        rcv, _, _ = f(c)
        ok, det = vigente(c, rcv, h0)
        paso("B", f"respuesta aceptada con BOM: {via} la mantiene vigente", ok, det)
    for nombre, primera, trans in (("bom_añadido", "punto", (con_bom,)), ("bom_material_primera", "material", (con_bom,)),
                                   ("bom_solicitud_primera", "solicitud", (con_bom,)), ("bom_y_crlf", "punto", (con_bom, con_crlf)),
                                   ("bom_y_nfd", "punto", (con_bom, con_nfd)), ("bom_con_preambulo", "preambulo", (con_bom,))):
        cb, _, rcb, _ = escenario(nombre.replace("ñ", "n"), primera)
        etiqueta = {"punto": "«1. PASA»", "material": "«Material auditado»", "solicitud": "«Solicitud de auditoría»", "preambulo": "el preámbulo"}[primera]
        paso("B", f"cierre de partida sin BOM con {etiqueta} como primera línea ({nombre})", cerrado(cb, rcb))
        for via, f, _ in VIAS:
            c = cb.copiar(f"{nombre}_{via.replace(' ', '_')}".replace("ñ", "n"))
            for t in trans:
                t(c)
            h0 = c.historial()
            rcv, _, _ = f(c)
            ok, det = vigente(c, rcv, h0)
            paso("B", f"{' + '.join(t.__name__.replace('con_', '').upper() for t in trans)} añadido después del cierre ({etiqueta} primera): {via} la mantiene vigente", ok, det)
    # regresiones negativas con BOM: la normalización no se amplía a otras diferencias
    cb, _, _, _ = escenario("bom_anadido", "punto")
    sol = (cb.st().get("auditoria_respuesta") or {}).get("solicitud")
    negativos = (("solicitud distinta", lambda t: t.replace(sol, "SA-0123456789abcdef"), "nombra la solicitud SA-0123456789abcdef"),
                 ("solicitud ausente", lambda t: "\n".join(l for l in t.split("\n") if not l.startswith("Solicitud de auditor")), "no tiene ninguna línea"),
                 ("solicitud duplicada", lambda t: t + f"Solicitud de auditoría: {sol}\n", "líneas «Solicitud de auditoría»"),
                 ("mismas palabras con el significado contrario", lambda t: t.replace(FRASE, FRASE_CONTRARIA), "su contenido o su orden cambiaron"))
    for i, (nombre, mut, diag) in enumerate(negativos):
        via, f, rc_esp = VIAS[i % 4]
        c = cb.copiar(f"neg_{i}")
        t = open(c.aud, encoding="utf-8").read()
        open(c.aud, "wb").write(b"\xef\xbb\xbf" + mut(t).encode("utf-8"))
        h0 = c.historial()
        rcv, _, _ = f(c)
        ok, det = retiro(c, rcv, rc_esp, h0, diag)
        paso("B", f"BOM + {nombre}: {via} retira en la primera llamada con su diagnóstico", ok, det)
    # cierre de la 4.8.1 (sin huella fiel registrada): sigue sujeto a sus bytes exactos; un BOM no se le atribuye como inocuo
    c = cb.copiar("legado_sin_fiel")
    st = c.st()
    st["auditoria_respuesta"].pop("fiel", None)
    for s in st.get("solicitudes_auditoria") or []:
        s.pop("respuesta_fiel", None)
    json.dump(st, open(os.path.join(c.d, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cv = j(c.d, "cierre_vigente.json")
    cv.pop("auditoria_fiel", None)
    json.dump(cv, open(os.path.join(c.d, "cierre_vigente.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    m0 = CIE.motivo_rechazo_cierre(c.d, pipeline.Pipeline.veredicto_auditoria)
    con_bom(c)
    h0 = c.historial()
    rcv, _, _ = corre("resumen.py", c.d, c.pred)
    ok, det = retiro(c, rcv, 3, h0, "no es byte a byte la respuesta aceptada")
    paso("B", "cierre sin huella fiel (como los de la 4.8.1): vigente con sus bytes exactos y retirado al añadir un BOM (no se le atribuye identidad nueva)", m0 is None and ok, f"antes {m0!r} · {det}")


# ---------------- grupo M · marcadores de cierre ----------------
def m_sin_cierre(F):
    F.pop("cierre", None)
    return F


def m_pendiente(F):
    F["estado_analisis"] = "pendiente_de_datos"
    return F


def m_ambos(F):
    return m_pendiente(m_sin_cierre(F))


def m_vacia(F):
    return {}


def grupo_m():
    c0, _, rc, rcr = escenario("marcadores", "preambulo")
    paso("M", "cierre de partida (código 0, publicado en el predeterminado y en el configurado)", cerrado(c0, rc) and aprobada(c0.pred) and aprobada(c0.extra), f"códigos {rc}/{rcr}")
    for nombre, mut in (("«cierre» eliminado", m_sin_cierre), ("estado cambiado a pendiente_de_datos", m_pendiente),
                        ("«cierre» eliminado y estado pendiente_de_datos", m_ambos), ("ficha {}", m_vacia)):
        for via, f, rc_esp in VIAS:
            c = c0.copiar(f"m_{mut.__name__}_{via.replace(' ', '_')}")
            F = mut(j(c.d, "ficha.json"))
            json.dump(F, open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
            h0 = c.historial()
            rcv, out, _ = f(c)
            if via == "ficha.py" and mut in (m_sin_cierre, m_pendiente):
                # con UN solo marcador la ficha sigue «cerrada»: ficha.py la trata como la sustitución de la 4.6.1/4.7.1 (W-d, código 0 con
                # aviso): archiva el cierre, retira las filas y escribe una ficha nueva que NO es vigente (pendiente de decisión, §9.5)
                st = c.st()
                ok = (rcv == 0 and "NO es vigente" in out and len(c.historial()) == len(h0) + 1 and st.get("auditoria") is None and retirada(c.pred)
                      and retirada(c.extra) and not incoherentes(c.pred) and not incoherentes(c.extra)
                      and CIE.motivo_vigencia(c.d, pipeline.Pipeline.veredicto_auditoria) is not None)
                det = f"código {rcv} · retiradas nuevas {len(c.historial()) - len(h0)} · auditoría {st.get('auditoria')!r} · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]}"
                paso("M", f"{nombre}: ficha.py archiva el cierre (sustitución, aviso), retira en todos los destinos y la ficha nueva no es vigente", ok, det)
                continue
            ok, det = retiro(c, rcv, rc_esp, h0)
            paso("M", f"{nombre}: la primera llamada de {via} retira en todos los destinos, conserva el historial y no deja aprobaciones incoherentes", ok, det)
    # (revisión interna R-1) los dos marcadores perdidos y además cierre_vigente.json borrado: el estado del pipeline sigue con APROBADO
    for via, f, rc_esp in VIAS:
        c = c0.copiar(f"m_sin_registro_{via.replace(' ', '_')}")
        json.dump(m_ambos(j(c.d, "ficha.json")), open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        os.remove(os.path.join(c.d, "cierre_vigente.json"))
        h0 = c.historial()
        rcv, _, _ = f(c)
        ok, det = retiro(c, rcv, rc_esp, h0)
        paso("M", f"ambos marcadores perdidos y cierre_vigente.json borrado (el pipeline sigue con APROBADO): {via} retira y no publica APROBADO", ok, det)
    # ficha.json ausente con el cierre registrado (revisión interna: solo leído en el código)
    c = c0.copiar("m_ficha_ausente")
    os.remove(os.path.join(c.d, "ficha.json"))
    h0 = c.historial()
    rcv, out, _ = corre("pipeline.py", c.d, "--desde", "14")
    st = c.st()
    paso("M", "ficha.json ausente con un cierre registrado: el paso 14 archiva el resto del cierre, retira en todos los destinos y no cierra",
         rcv == 4 and len(c.historial()) == len(h0) + 1 and not os.path.exists(os.path.join(c.d, "cierre_vigente.json")) and st.get("auditoria") is None
         and retirada(c.pred) and retirada(c.extra) and not incoherentes(c.pred) and not incoherentes(c.extra),
         f"código {rcv} · retiradas nuevas {len(c.historial()) - len(h0)} · auditoría {st.get('auditoria')!r} · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]}")
    # restaurar los bytes o regenerar la ficha no reactiva la aprobación retirada
    c = c0.copiar("m_restaurar")
    orig = open(os.path.join(c.d, "ficha.json"), "rb").read()
    json.dump(m_ambos(json.loads(orig)), open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"))
    corre("resumen.py", c.d, c.pred)
    open(os.path.join(c.d, "ficha.json"), "wb").write(orig)
    rcr2, _, _ = corre("resumen.py", c.d, c.pred)
    rcf, _, _ = corre("ficha.py", c.d, "--estado", "concluido")
    rcr3, _, _ = corre("resumen.py", c.d, c.pred)
    paso("M", "restaurar los bytes de la ficha o regenerarla no reactiva la aprobación retirada",
         rcr2 == 3 and rcf == 3 and rcr3 != 0 and not aprobada(c.pred) and not incoherentes(c.pred) and c.st().get("auditoria") is None,
         f"códigos {rcr2}/{rcf}/{rcr3} · pred {[(r.get('verificacion') or '')[:22] for r in filas(c.pred)]}")
    # destino registrado inaccesible: código 5 (retirada pendiente)
    c = c0.copiar("m_pendiente_5")
    json.dump(m_ambos(j(c.d, "ficha.json")), open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"))
    os.remove(c.extra)
    os.makedirs(c.extra)  # el destino registrado existe pero no se puede escribir como CSV (error de escritura): retirada pendiente
    rcv, out, _ = corre("resumen.py", c.d, c.pred)
    paso("M", "con un destino registrado inaccesible, la retirada queda pendiente (código 5) y el predeterminado se retira", rcv == 5 and retirada(c.pred), f"código {rcv} · {out[-120:]}")
    # estado temprano legítimo sin cierre previo: no se retira nada
    c = c0.copiar("m_temprano")
    CIE.archivar_salidas(c.d, "preparación de la prueba: retirada legítima previa", c.pred)
    h0 = c.historial()
    rcf, _, _ = corre("ficha.py", c.d, "--estado", "pendiente_de_datos")
    rci, _, _ = corre("informe.py", c.d)
    rcr, _, _ = corre("resumen.py", c.d, c.pred)
    f = filas(c.pred)
    paso("M", "estado temprano legítimo sin cierre registrado: ficha.py, informe.py y resumen.py escriben (código 0) sin retiradas nuevas ni APROBADO",
         rcf == 0 and rci == 0 and rcr == 0 and c.historial() == h0 and not os.path.exists(os.path.join(c.d, "cierre_vigente.json"))
         and len(f) == 1 and f[0].get("estado_analisis") == "pendiente_de_datos" and "APROBADO" not in (f[0].get("verificacion") or ""),
         f"códigos {rcf}/{rci}/{rcr} · retiradas nuevas {len(c.historial()) - len(h0)} · fila {[(r.get('estado_analisis'), (r.get('verificacion') or '')[:20]) for r in f]}")
    # una ficha {} sin cierre registrado no publica una fila sin empresa
    c = c0.copiar("m_vacia_sin_registro")
    CIE.archivar_salidas(c.d, "preparación de la prueba: retirada legítima previa", c.pred)
    json.dump({}, open(os.path.join(c.d, "ficha.json"), "w", encoding="utf-8"))
    rcv, _, _ = corre("resumen.py", c.d, c.pred)
    paso("M", "ficha {} sin cierre registrado: resumen.py no escribe una fila sin empresa (código 3)", rcv == 3 and not [r for r in filas(c.pred, None) if not r.get("empresa")], f"código {rcv}")


# ---------------- grupo L · acreditación del libro final ----------------
def preparar_libro(c, con_recalc):
    """Libro evaluado sin cachés (copia de prueba de escribir_v63) y, si `con_recalc`, la copia «recalculada» (el libro con valores)."""
    ev = os.path.join(c.d, "Vidrala_v63_evaluada.xlsx")
    con_valores = os.path.join(TMP, os.path.basename(c.base) + "_con_valores.xlsx")
    shutil.copy2(ev, con_valores)
    vacio = os.path.join(TMP, os.path.basename(c.base) + "_celdas.json")
    json.dump({}, open(vacio, "w"))
    rc, out, _ = corre("escribir_v63.py", con_valores, ev, "--celdas", vacio, "--lista-blanca", "cualquiera", "--copia-de-prueba")
    if con_recalc:
        os.makedirs(os.path.join(c.d, "recalc"), exist_ok=True)
        shutil.copy2(con_valores, os.path.join(c.d, "recalc", "Vidrala_v63_evaluada.xlsx"))
    return rc, ev


def fichas_sinteticas(d, h):
    """(4.10.1, T-1) Fichas del material SINTÉTICO de la prueba con la identidad del libro que se acaba de acreditar. No toca ningún
    expediente real: la copia es de la prueba, y las fichas copiadas de la referencia registran el libro histórico (1020bb53…), cuyos
    bytes no tiene por qué reproducir la reconstrucción en otro entorno."""
    for fic in ("ficha.json", "ficha_provisional.json"):
        F = j(d, fic)
        if isinstance(F, dict):
            F.setdefault("hashes", {})["libro_evaluado"] = h
            json.dump(F, open(os.path.join(d, fic), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def rezip_inocuo(origen, destino):
    """Reconstrucción sintética del .xlsx con bytes distintos e inocuos: los mismos miembros con el mismo contenido (fórmulas y valores),
    otra fecha interna y otro nivel de compresión. (Revisión interna 4.10.1, H-3) si una forma coincidiera con los bytes del origen (un libro
    que ya la tuviera), se usa la siguiente: los bytes del resultado son siempre distintos de los del origen, sin rebajar ninguna aserción."""
    import zipfile
    h0 = sha(origen)
    for fecha, nivel in (((2001, 2, 3, 4, 5, 6), 1), ((2003, 4, 5, 6, 7, 8), 9), ((2005, 6, 7, 8, 9, 10), 5)):
        with zipfile.ZipFile(origen) as zi, zipfile.ZipFile(destino, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=nivel) as zo:
            for it in zi.infolist():
                ni = zipfile.ZipInfo(it.filename, date_time=fecha)
                ni.compress_type = zipfile.ZIP_DEFLATED
                zo.writestr(ni, zi.read(it.filename))
        if sha(destino) != h0:
            break
    with zipfile.ZipFile(origen) as a, zipfile.ZipFile(destino) as b:
        return sorted(a.namelist()) == sorted(b.namelist()) and all(a.read(n) == b.read(n) for n in a.namelist())


def prueba_correspondencia(c, ev):
    """(4.10.1, T-1) 1) libro sintético final ya acreditado; 2) fichas sintéticas con su identidad ANTES de comprobar m0; 3) precondición
    coherente; 4) cada mutación por separado, en su propia copia, con su rechazo."""
    import openpyxl
    final = sha(ev)
    fichas_sinteticas(c.d, final)
    m0 = CIE.motivo_acreditacion_libro(c.d)

    def copia(nombre):
        d = os.path.join(TMP, "corr_" + nombre)
        shutil.copytree(c.d, d, symlinks=True)
        return d
    d1 = copia("ficha_otra")
    F = j(d1, "ficha_provisional.json") or j(d1, "ficha.json")
    fic = "ficha_provisional.json" if j(d1, "ficha_provisional.json") else "ficha.json"
    F.setdefault("hashes", {})["libro_evaluado"] = "0" * 64
    json.dump(F, open(os.path.join(d1, fic), "w", encoding="utf-8"))
    m_ficha = CIE.motivo_acreditacion_libro(d1)
    d2 = copia("modificado")
    wb = openpyxl.load_workbook(os.path.join(d2, "Vidrala_v63_evaluada.xlsx"))
    wb["Análisis"]["A1"] = (wb["Análisis"]["A1"].value or "") + " "
    wb.save(os.path.join(d2, "Vidrala_v63_evaluada.xlsx"))
    m1 = CIE.motivo_acreditacion_libro(d2)
    paso("L", "una modificación posterior del libro o una ficha que registra otro libro invalidan la correspondencia",
         m0 is None and m1 is not None and "no es el libro acreditado" in m1 and m_ficha is not None and "registra otro libro" in m_ficha,
         f"precondición {m0!r} · ficha {str(m_ficha)[:70]!r} · después {str(m1)[:90]!r}")
    d3 = copia("comprobante_invalido")
    open(os.path.join(d3, "acreditacion_libro.json"), "w", encoding="utf-8").write("{ no es JSON")
    m3 = CIE.motivo_acreditacion_libro(d3)
    paso("L", "un comprobante ilegible (JSON inválido) no acredita el libro", m0 is None and m3 is not None and "no se puede acreditar" in m3, f"{str(m3)[:90]!r}")
    d4 = copia("sin_correspondencia")
    ac = j(d4, "acreditacion_libro.json")
    ac["archivo_final"]["archivo"] = "Otra_v63_evaluada.xlsx"
    json.dump(ac, open(os.path.join(d4, "acreditacion_libro.json"), "w", encoding="utf-8"))
    m4 = CIE.motivo_acreditacion_libro(d4)
    paso("L", "falta de correspondencia: el comprobante nombra un libro evaluado que no está en el expediente", m0 is None and m4 is not None and "falta el libro acreditado" in m4, f"{str(m4)[:90]!r}")
    # reconstrucción sintética con bytes distintos e inocuos: la preparación no depende de recuperar el ZIP interno del Excel histórico
    d5 = copia("reconstruccion_inocua")
    ev5 = os.path.join(d5, "Vidrala_v63_evaluada.xlsx")
    orig = os.path.join(TMP, "corr_original_bytes.xlsx")
    shutil.copy2(ev5, orig)
    mismo = rezip_inocuo(orig, ev5)
    va = openpyxl.load_workbook(orig, data_only=True, read_only=True)["Análisis"]["C83"].value
    vb = openpyxl.load_workbook(ev5, data_only=True, read_only=True)["Análisis"]["C83"].value
    rc, _, _ = corre("acreditar_libro.py", d5, ev5, os.path.join(d5, "Vidrala_v63_datos.xlsx"), CIE_REF(), CIE_VER(), "sin_copia_recalculada")
    h5 = sha(ev5)
    fichas_sinteticas(d5, h5)
    m5 = CIE.motivo_acreditacion_libro(d5)
    paso("L", "reconstrucción sintética con bytes distintos e inocuos (mismos miembros, fórmulas y valores): acreditada y con fichas de su identidad, la precondición es coherente",
         mismo and va == vb and h5 != sha(orig) and rc == 0 and m5 is None, f"mismo contenido {mismo} · C83 {va!r}/{vb!r} · acreditar {rc} · {m5!r}")
    shutil.copy2(orig, ev5)
    m6 = CIE.motivo_acreditacion_libro(d5)
    paso("L", "identidad estricta: el archivo acreditado no se sustituye por su equivalente inocuo con otros bytes", m6 is not None and "no es el libro acreditado" in m6, f"{str(m6)[:90]!r}")


def grupo_l():
    import openpyxl
    for nombre, con_recalc in (("incorporación efectiva de cachés", True), ("ruta sin copia recalculada", False)):
        c = Caso(os.path.join(TMP, "libro_" + ("cache" if con_recalc else "sin_recalc")))
        shutil.copytree(ARGS.expediente, c.d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
        rcp, ev = preparar_libro(c, con_recalc)
        antes = sha(ev)
        rc, out, _ = corre("verificar_todo.sh", c.d, ev, os.path.join(c.d, "Vidrala_v63_datos.xlsx"))
        ac = j(c.d, "acreditacion_libro.json") or {}
        fin = ac.get("archivo_final") or {}
        pre = (ac.get("libro_evaluado_verificado_antes_de_caches") or {}).get("sha256_prefijo") or ""
        vf = open(os.path.join(c.d, "verificacion_libro_final.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(c.d, "verificacion_libro_final.txt")) else ""
        integridad = open(os.path.join(c.d, "verificacion_integridad.txt"), encoding="utf-8").read() if os.path.exists(os.path.join(c.d, "verificacion_integridad.txt")) else ""
        final = sha(ev)
        valor = openpyxl.load_workbook(ev, data_only=True, read_only=True)["Análisis"]["C83"].value
        if con_recalc:
            ok = (ac.get("caches") == "incorporadas" and fin.get("sha256") == final and final != antes and antes.startswith(pre) and pre in integridad
                  and isinstance(valor, (int, float)) and final[:16] in vf and "ÍNTEGRO" in vf and fin.get("igual_al_verificado_antes_de_caches") is False)
        else:
            ok = (ac.get("caches") == "sin_copia_recalculada" and fin.get("sha256") == final == antes and fin.get("igual_al_verificado_antes_de_caches") is True
                  and final[:16] in vf and "ÍNTEGRO" in vf)
        paso("L", f"{nombre}: acreditacion_libro.json identifica el archivo FINAL (SHA-256 calculado aparte) y lo distingue del verificado antes de las cachés",
             rcp == 0 and ok, f"verificar_todo.sh {rc} · cachés {ac.get('caches')} · final {final[:12]} · antes {antes[:12]} · acreditado {str(fin.get('sha256'))[:12]} · C83 {valor!r}")
        if con_recalc:
            prueba_correspondencia(c, ev)
    # cierre con libro acreditado y modificación posterior: la primera llamada retira
    def acreditar(c):
        ev = os.path.join(c.d, "Vidrala_v63_evaluada.xlsx")
        corre("acreditar_libro.py", c.d, ev, os.path.join(c.d, "Vidrala_v63_datos.xlsx"), CIE_REF(), CIE_VER(), "sin_copia_recalculada")
    # (revisión interna R-3) un comprobante con la verificación final NO ÍNTEGRO, o que nombra otro .xlsx, no acredita nada
    c3 = Caso(os.path.join(TMP, "libro_comprobante_malo"))
    shutil.copytree(ARGS.expediente, c3.d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    acreditar(c3)
    fichas_sinteticas(c3.d, sha(os.path.join(c3.d, "Vidrala_v63_evaluada.xlsx")))  # (4.10.1, T-1) la misma preparación
    ac = j(c3.d, "acreditacion_libro.json") or {}
    m_ok = CIE.motivo_acreditacion_libro(c3.d)
    ac["archivo_final"]["veredicto"] = "NO ÍNTEGRO · 1 fallo"
    json.dump(ac, open(os.path.join(c3.d, "acreditacion_libro.json"), "w", encoding="utf-8"))
    m_ver = CIE.motivo_acreditacion_libro(c3.d)
    ac["archivo_final"].update(veredicto="ÍNTEGRO · 0 fallos · 0 avisos", archivo="Vidrala_v63_datos.xlsx", sha256=sha(os.path.join(c3.d, "Vidrala_v63_datos.xlsx")))
    json.dump(ac, open(os.path.join(c3.d, "acreditacion_libro.json"), "w", encoding="utf-8"))
    m_otro = CIE.motivo_acreditacion_libro(c3.d)
    paso("L", "un comprobante con la verificación final no ÍNTEGRO, o que nombra otro .xlsx con su huella, no acredita el libro",
         m_ok is None and m_ver is not None and "no es ÍNTEGRO" in m_ver and m_otro is not None and "libro evaluado final" in m_otro, f"{m_ok!r} · {str(m_ver)[:60]!r} · {str(m_otro)[:60]!r}")
    c, _, rc, _ = escenario("libro_acreditado", "preambulo", antes_de_auditar=acreditar)
    fij = (j(c.d, "material_auditoria.json") or {}).get("archivos") or {}
    paso("L", "un cierre con el libro acreditado: el comprobante forma parte del material auditado y el cierre se confirma",
         cerrado(c, rc) and CIE.ACREDITACION_LIBRO in fij and CIE.motivo_acreditacion_libro(c.d) is None, f"código {rc} · en el material: {CIE.ACREDITACION_LIBRO in fij}")
    c2 = c.copiar("libro_acreditado_modificado")
    ac = j(c2.d, "acreditacion_libro.json")
    ac["archivo_final"]["sha256"] = "f" * 64
    json.dump(ac, open(os.path.join(c2.d, "acreditacion_libro.json"), "w", encoding="utf-8"))
    h0 = c2.historial()
    rcv, _, _ = corre("informe.py", c2.d)
    ok, det = retiro(c2, rcv, 3, h0)
    paso("L", "una correspondencia rota después del cierre retira la aprobación en la primera llamada (no se actualiza el cierre antiguo)", ok, det)
    # igualdad independiente del archivo final de los expedientes de la 4.10 con su comprobante (en la verificación, el árbol extraído del ZIP)
    base410 = os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_10")
    comprobantes = []
    # (4.10.1) también los expedientes posteriores (2026-11_Vidrala_ensayo_4_10_*, p. ej., el ensayo 2025 de la 4.10.1)
    raices = [base410] + sorted(os.path.join(RAIZ, "empresas_v2_correcciones", d) for d in os.listdir(os.path.join(RAIZ, "empresas_v2_correcciones"))
                                if d.startswith("2026-11_Vidrala_ensayo_4_10_"))
    for r, ds, fs in (x for raiz in raices for x in os.walk(raiz)):
        if "acreditacion_libro.json" in fs:
            ac = j(r, "acreditacion_libro.json") or {}
            fin = ac.get("archivo_final") or {}
            comprobantes.append((os.path.relpath(r, RAIZ), sha(os.path.join(r, fin.get("archivo") or "-")) == fin.get("sha256")))
    # (4.10.1) se mantiene el nombre de la 4.10 (trazabilidad de los casos); desde la 4.10.1 incluye los expedientes posteriores (detalle)
    paso("L", "los libros finales de los expedientes de la 4.10 son, byte a byte, los acreditados en su comprobante (SHA-256 calculado aparte)",
         bool(comprobantes) and all(ok for _, ok in comprobantes) or (not os.path.isdir(base410) and ARGS.codigo), f"{comprobantes}")


def CIE_REF():
    return subprocess.run([PY, os.path.join(SCR, "config_v2.py"), "plantilla.referencia", os.path.join(os.path.dirname(SCR), "config_v2.json")], capture_output=True, text=True).stdout.strip()


def CIE_VER():
    return subprocess.run([PY, os.path.join(SCR, "config_v2.py"), "plantilla.verificador", os.path.join(os.path.dirname(SCR), "config_v2.json")], capture_output=True, text=True).stdout.strip()


try:
    for g in (grupo_b, grupo_m, grupo_l):
        try:
            g()
        except Exception as e:  # un fallo del propio grupo cuenta como FALLA, no interrumpe los demás
            import traceback
            paso(g.__name__[-1].upper(), f"el grupo terminó con una excepción: {type(e).__name__}: {str(e)[:160]}", False, traceback.format_exc().splitlines()[-3][:200])
finally:
    shutil.rmtree(TMP, ignore_errors=True)
n_ok = sum(1 for r in R if r[2])
if ARGS.json:
    json.dump([{"grupo": g, "prueba": n, "resultado": "PASA" if ok else "FALLA", "detalle": d} for g, n, ok, d in R],
              open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"\n{n_ok}/{len(R)} pruebas de trazabilidad de la 4.10 PASAN")
sys.exit(0 if n_ok == len(R) else 1)
