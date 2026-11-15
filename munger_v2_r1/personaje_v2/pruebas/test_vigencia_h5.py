"""Batería de la reparación 4.13.1 (H5 del encargo de cierre, §4): una aprobación publicada que pierde su respaldo deja de figurar vigente,
en el estado interno y en las salidas públicas, en la PRIMERA llamada de cualquiera de las cuatro vías (pipeline, ficha, informe, resumen).

Cada caso trabaja sobre una copia independiente del piloto cerrado de la 4.11 (inicialmente vigente), con el destino del resumen y el
registro de publicaciones (y su respaldo) reubicados dentro de la copia (test_integracion_v64.copia_piloto): ninguna prueba toca
publicaciones originales. Las auditorías sintéticas (agentes_sinteticos.auditoria) solo se usan en G (intervalo legítimo), H (recuperación) e I (D1-1 y D1-4),
identificadas como tales.

Grupos:
  A  cuatro primeras llamadas sin ficha.json ni cierre_vigente.json, con el material cambiado (PM1.lambda = 1,25), intacto e ilegible
  B  ausencias individuales y combinadas: solo ficha, solo cierre registrado, registro de publicaciones (con respaldo) y registro y respaldo
  C  ninguna salida oficial restante (tampoco informe.md)
  D  destino inaccesible: retirada pendiente visible (código 5) sin conservar la aprobación interna
  E  idempotencia: la segunda llamada no añade antecedentes ni cambia el resultado
  F  restaurar archivos antiguos (salidas y estado del pipeline) no reactiva la aprobación
  G  intervalo legítimo entre la aceptación de la auditoría (paso 13) y la publicación del paso 14: no se retira nada y el paso 14 cierra
  H  recuperación completa con una auditoría nueva después de la retirada
  I  casos de la revisión interna D1 de la 4.13.1: dos expedientes de la misma empresa en una carpeta (D1-1), destino no actualizable sin
     registro (D1-2), estado ilegible en la primera llamada (D1-3), registro ilegible en el intervalo (D1-4), cierre anterior a la 4.8.1
     (D1-5) y aprobaciones_retiradas.json ilegible (D1-6); el paso 13 y el arranque del paso 14 se emulan con cierre_v2, como en la revisión
No arranca LibreOffice: los cambios de material no llegan a recalcular (las vías se detienen o el pipeline se para con --hasta 8).
Uso: python3 -B test_vigencia_h5.py [--json salida.json]
"""
import argparse, csv, glob, json, os, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.path.insert(0, AQUI); sys.path.insert(0, os.path.join(PV, "scripts"))
import test_integracion_v64 as T  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--json")
ARGS = ap.parse_args()
os.makedirs(T.TMP, exist_ok=True)
VIAS = ("pipeline", "ficha", "informe", "resumen")
RES = []


def paso(grupo, nombre, ok, detalle=""):
    RES.append({"grupo": grupo, "prueba": nombre, "resultado": "PASA" if ok else "FALLA", "detalle": detalle})
    print(f"[{grupo}] {'PASA ' if ok else 'FALLA'} {nombre}" + (f" · {detalle}" if detalle else ""))


def resumenes(c):
    base = os.path.dirname(c)
    return sorted(p for p in glob.glob(os.path.join(base, "resumen_v2*.csv")) if not p.endswith("_historial.csv"))


def filas_aprobadas(c):
    out = []
    for p in resumenes(c):
        out += [os.path.basename(p) for r in csv.DictReader(open(p, encoding="utf-8", newline="")) if (r.get("verificacion") or "").strip() == "APROBADO"]
    return out


def registro(c):
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(c, n)
        if os.path.exists(p):
            return [e.get("estado") for e in (json.load(open(p, encoding="utf-8")).get("publicaciones") or [])]
    return []


def st(c):
    return json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))


def retiradas(c):
    return sorted(glob.glob(os.path.join(c, "historial_cierres", "*", "RETIRADA.json")))


def anotadas(c):
    p = os.path.join(c, CIE.APROBACIONES_RETIRADAS)
    d = CIE._j_tolerante(p)
    return (d.get("retiradas") or []) if isinstance(d, dict) else []


def foto(c):
    s = st(c)
    return (f"estado {s.get('auditoria')}/{s.get('estado_analisis')} · filas APROBADO {filas_aprobadas(c)} · registro {registro(c)} · "
            f"antecedentes {len(retiradas(c))} · anotadas {len(anotadas(c))}")


def retirada_completa(c, ident):
    """Estado sin la aprobación, ninguna fila APROBADO, ninguna publicación «publicada», y el antecedente con motivo, rastro previo e identidad."""
    s = st(c)
    ret = retiradas(c)
    R = json.load(open(ret[-1], encoding="utf-8")) if ret else {}
    rp = os.path.join(os.path.dirname(ret[-1]), "rastro_previo", "estado_pipeline.json") if ret else ""
    previo = json.load(open(rp, encoding="utf-8")) if rp and os.path.exists(rp) else {}
    return (s.get("auditoria") != "APROBADO" and s.get("estado_analisis") != "concluido" and not filas_aprobadas(c)
            and "publicada" not in registro(c) and bool(R.get("motivo")) and previo.get("auditoria") == "APROBADO"
            and (R.get("aprobacion_retirada") or {}).get("solicitud") == ident[0]
            and any(e.get("solicitud") == ident[0] for e in anotadas(c)))


def preparar(nombre, quitar=("ficha.json", "cierre_vigente.json"), material="valida_modificada"):
    c = T.copia_piloto(nombre)
    ident = CIE.identidad_aprobacion(st(c))
    for n in quitar:
        os.remove(os.path.join(c, n))
    if material == "json_roto":
        T.alterar(c, "json_roto")
    elif material:
        T.alterar(c, material)
    return c, ident


def llamar(c, via):
    rc, out = T.primera_llamada(c, via)
    return rc, out, ("Traceback" in out)


def corre_pipeline(c, *args):
    env = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}
    r = subprocess.run([T.PY, "-B", os.path.join(PV, "scripts", "pipeline.py"), c, "--config", T.CFG64, *args], capture_output=True, text=True, env=env, timeout=1800)
    return r.returncode, r.stdout + r.stderr


# ---------- A ----------
for mat, etiqueta in (("valida_modificada", "material cambiado"), (None, "material intacto"), ("json_roto", "material ilegible (JSON roto)")):
    for via in VIAS:
        c, ident = preparar(f"A_{mat}_{via}", material=mat)
        rc, out, tb = llamar(c, via)
        paso("A", f"sin ficha ni cierre registrado, {etiqueta}: la primera llamada de {via} retira la aprobación interna y pública, con antecedente y rastro",
             ident is not None and not tb and retirada_completa(c, ident) and (via == "pipeline" or rc in (3, 5)),
             f"código {rc} · {foto(c)}")

# ---------- B ----------
VARIANTES_B = (("solo sin ficha.json", ("ficha.json",)), ("solo sin cierre_vigente.json", ("cierre_vigente.json",)),
               ("sin ficha, sin cierre y sin registro de publicaciones (con respaldo)", ("ficha.json", "cierre_vigente.json", CIE.REGISTRO_RESUMEN)),
               ("sin ficha, sin cierre, sin registro ni respaldo", ("ficha.json", "cierre_vigente.json", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN)))
for k, (etiqueta, quitar) in enumerate(VARIANTES_B):
    for via in VIAS:
        c, ident = preparar(f"B{k}_{via}", quitar=quitar)
        rc, out, tb = llamar(c, via)
        paso("B", f"{etiqueta}, material cambiado: {via} retira en la primera llamada", ident is not None and not tb and retirada_completa(c, ident),
             f"código {rc} · {foto(c)}")

# ---------- C ----------
for via in VIAS:
    c, ident = preparar(f"C_{via}", quitar=("ficha.json", "cierre_vigente.json", "informe.md"), material=None)
    rc, out, tb = llamar(c, via)
    R = json.load(open(retiradas(c)[-1], encoding="utf-8")) if retiradas(c) else {}
    paso("C", f"ninguna salida oficial restante (ni ficha, ni informe, ni cierre registrado): {via} retira e invalida el estado igualmente",
         not tb and retirada_completa(c, ident) and R.get("archivos") == [] and bool(R.get("sin_salidas_oficiales")), f"código {rc} · {foto(c)}")

# ---------- D ----------
for via in VIAS:
    c, ident = preparar(f"D_{via}", material=None)
    for n in (CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        p = os.path.join(c, n)
        reg = json.load(open(p, encoding="utf-8"))
        for e in reg.get("publicaciones") or []:
            e["csv"] = os.path.join(os.path.dirname(c), "carpeta_inaccesible", "resumen_v2.csv")
        json.dump(reg, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out, tb = llamar(c, via)
    s = st(c)
    paso("D", f"destino inaccesible: {via} deja la retirada pendiente visible{' (código 5)' if via != 'pipeline' else ''} sin conservar la aprobación interna",
         not tb and s.get("auditoria") != "APROBADO" and s.get("estado_analisis") != "concluido" and "retirada_pendiente" in registro(c)
         and len(retiradas(c)) == 1 and (via == "pipeline" or rc == 5), f"código {rc} · {foto(c)}")

# ---------- E ----------
for via in VIAS:
    c, ident = preparar(f"E_{via}")
    rc1, _, _ = llamar(c, via)
    f1, n1 = foto(c), len(anotadas(c))
    rc2, out2, tb = llamar(c, via)
    paso("E", f"idempotencia de {via}: la segunda llamada no añade antecedentes ni anotaciones y deja el mismo resultado",
         not tb and foto(c) == f1 and len(anotadas(c)) == n1 == 1 and len(retiradas(c)) == 1, f"códigos {rc1}/{rc2} · {foto(c)}")

# ---------- F ----------
for via in VIAS:
    c, ident = preparar(f"F_{via}", quitar=(), material=None)
    guard = os.path.join(os.path.dirname(c), "_guardados")
    os.makedirs(guard)
    for n in ("ficha.json", "cierre_vigente.json", "informe.md", "estado_pipeline.json", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        shutil.copy2(os.path.join(c, n), os.path.join(guard, n))
    os.remove(os.path.join(c, "ficha.json")); os.remove(os.path.join(c, "cierre_vigente.json"))
    rc1, _, _ = llamar(c, via)
    for n in os.listdir(guard):  # se restauran TODOS los archivos antiguos: salidas, estado y registro de publicaciones
        shutil.copy2(os.path.join(guard, n), os.path.join(c, n))
    rcs = [llamar(c, v)[0] for v in ("ficha", "informe", "resumen")]
    s = st(c)
    paso("F", f"tras la retirada por {via}, restaurar la ficha, el informe, el cierre registrado, el estado y el registro antiguos no reactiva la aprobación",
         ident is not None and not filas_aprobadas(c) and "publicada" not in registro(c)
         and CIE.motivo_rechazo_cierre(c, T_veredicto := __import__("pipeline").Pipeline.veredicto_auditoria) is not None,
         f"códigos {rc1}/{rcs} · {foto(c)} · motivo «{(CIE.motivo_rechazo_cierre(c, T_veredicto) or '')[:90]}»")

# ---------- G ----------
c = T.copia_piloto("G_intervalo")
rc13, out13 = corre_pipeline(c, "--desde", "13")
AG.auditoria(c, "APROBADO")
rc13b, out13b = corre_pipeline(c, "--hasta", "13")
s = st(c)
en_intervalo = s.get("auditoria") == "APROBADO" and not os.path.exists(os.path.join(c, "ficha.json")) and "publicada" not in registro(c)
ant0, anot0, acept = len(retiradas(c)), len(anotadas(c)), CIE.identidad_aprobacion(s)
rcs = {v: llamar(c, v)[0] for v in ("informe", "resumen")}
s2 = st(c)
paso("G", "intervalo legítimo (paso 13 aceptado, sin ficha cerrada ni publicación): informe.py y resumen.py no retiran la aprobación aceptada "
     "(la del cierre anterior quedó anotada al pedir la auditoría; la nueva no)",
     en_intervalo and acept is not None and s2.get("auditoria") == "APROBADO" and len(retiradas(c)) == ant0 and len(anotadas(c)) == anot0
     and not any(e.get("solicitud") == acept[0] for e in anotadas(c)),
     f"códigos 13: {rc13}/{rc13b} · llamadas {rcs} · {foto(c)}")
rc14, out14 = corre_pipeline(c, "--desde", "14")
F = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
paso("G", "después del intervalo, el paso 14 cierra y publica con la auditoría aceptada (ficha cerrada, cierre registrado, fila APROBADO)",
     rc14 == 0 and st(c).get("auditoria") == "APROBADO" and CIE.ficha_cerrada(F) and os.path.exists(os.path.join(c, "cierre_vigente.json"))
     and filas_aprobadas(c) and "publicada" in registro(c), f"código {rc14} · {foto(c)} · {out14.strip().splitlines()[-1][:100] if out14.strip() else ''}")

# ---------- H ----------
c, ident = preparar("H_recuperacion", material=None)
rc1, _, _ = llamar(c, "ficha")
retirado = retirada_completa(c, ident)
rc13, _ = corre_pipeline(c, "--desde", "13")
AG.auditoria(c, "APROBADO")
rc14, out14 = corre_pipeline(c)
F = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "ficha.json")) else {}
nueva = CIE.identidad_aprobacion(st(c))
paso("H", "recuperación: tras la retirada H5, una auditoría nueva (solicitud nueva) vuelve a cerrar y publicar; la retirada anterior sigue anotada",
     retirado and rc14 == 0 and st(c).get("auditoria") == "APROBADO" and CIE.ficha_cerrada(F) and filas_aprobadas(c) and "publicada" in registro(c)
     and nueva is not None and nueva[0] != ident[0] and any(e.get("solicitud") == ident[0] for e in anotadas(c)),
     f"códigos {rc1}/{rc13}/{rc14} · {foto(c)} · {out14.strip().splitlines()[-1][:100] if out14.strip() else ''}")

# ---------- I · casos de la revisión interna D1 de la 4.13.1 (emulaciones del paso 13 y del arranque del paso 14 de la revisión) ----------
import datetime as _dt  # noqa: E402
VER = __import__("pipeline").Pipeline.veredicto_auditoria


def corre_sc(script, *args, cfg=None):
    env = {k: v for k, v in os.environ.items() if k != "MUNGER_CONFIG"}
    if cfg:
        env["MUNGER_CONFIG"] = cfg
    r = subprocess.run([T.PY, "-B", os.path.join(PV, "scripts", script), *args], capture_output=True, text=True, env=env, timeout=900)
    return r.returncode, (r.stdout + r.stderr)


def guardar_st(c, s):
    json.dump(s, open(os.path.join(c, "estado_pipeline.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def pedir_auditoria(c, csv_path):
    """Emulación del paso 13 sin solicitud pendiente (Pipeline.solicitud_auditoria_vigente): solicitud nueva, Y-h y auditoría = None."""
    s = st(c)
    nueva = CIE.nueva_solicitud(s.get("material_auditoria"), "auditoría del material fijado en el paso 13", _dt.datetime.now().astimezone().isoformat(timespec="seconds"))
    shas, conts = CIE.auditorias_del_expediente(c, VER)
    s["anteriores_sha256"] = sorted(set(s.get("anteriores_sha256") or []) | shas)
    s["anteriores_contenido"] = sorted(set(s.get("anteriores_contenido") or []) | conts)
    CIE.anotar_auditorias(c, shas, conts, f"solicitud {nueva['id']}")
    s.setdefault("solicitudes_auditoria", []).append(nueva)
    CIE.escribir_solicitud(c, nueva)
    F = CIE._j_tolerante(os.path.join(c, "ficha.json"))
    if CIE.ficha_cerrada(F) or os.path.lexists(os.path.join(c, "cierre_vigente.json")):
        CIE.archivar_salidas(c, f"se pidió una auditoría nueva (solicitud {nueva['id']}): el cierre anterior no vale hasta su respuesta", csv_path, s)
    s.update(auditoria=None, paso=13, estado_analisis=None)
    guardar_st(c, s)
    return nueva["id"]


def aceptar_auditoria(c):
    """Emulación del paso 13 con una auditoría SINTÉTICA APROBADO (agentes_sinteticos.auditoria), identificada como tal."""
    AG.auditoria(c, "APROBADO")
    s = st(c)
    sol = [x for x in s["solicitudes_auditoria"] if x.get("estado") == "pendiente"][-1]
    p = os.path.join(c, "auditoria.md")
    datos = open(p, "rb").read()
    h, hc, hf = CIE.sha_archivo(p), CIE.huella_contenido(CIE.texto_fiel(datos)), CIE.huella_fiel(datos)
    sol.update(estado="respondida", respuesta_sha256=h, respuesta_contenido=hc, respuesta_fiel=hf, respondida=_dt.datetime.now().isoformat(timespec="seconds"), veredicto="APROBADO")
    s["auditoria_respuesta"] = {"solicitud": sol["id"], "sha256": h, "contenido": hc, "fiel": hf, "material": sol.get("material")}
    CIE.anotar_auditorias(c, [h], [hc], f"respuesta a la solicitud {sol['id']}")
    s.update(auditoria="APROBADO", paso=14, esperando=None)
    guardar_st(c, s)
    return sol["id"]


def paso14(c, csv_path):
    """Emulación del arranque del paso 14 y de salidas_finales(cierre=True): ficha, informe y resumen con la configuración V6.4."""
    s = st(c)
    est = s.get("estado_pendiente") or "concluido"
    s["estado_analisis"] = est
    guardar_st(c, s)
    return [corre_sc("ficha.py", c, "--estado", est, cfg=T.CFG64)[0], corre_sc("informe.py", c, cfg=T.CFG64)[0], corre_sc("resumen.py", c, csv_path, cfg=T.CFG64)[0]]


def csv_piloto(c):
    return os.path.join(os.path.dirname(c), "resumen_v2.csv")


def fila_de(p):
    return [(r.get("verificacion") or "") for r in csv.DictReader(open(p, encoding="utf-8", newline=""))] if os.path.exists(p) else []


# I1 (D1-1): dos expedientes de la misma empresa en la misma carpeta; B, nuevo y sin registro, en su primer cierre legítimo
a = T.copia_piloto("I1")
b = os.path.join(os.path.dirname(a), "Vidrala_segundo")
shutil.copytree(a, b)
for n in ("ficha.json", "cierre_vigente.json", "informe.md", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
    if os.path.exists(os.path.join(b, n)):
        os.remove(os.path.join(b, n))
shutil.rmtree(os.path.join(b, "historial_cierres"), ignore_errors=True)
for n in os.listdir(b):
    if n.startswith("Vidrala_v63_"):
        os.replace(os.path.join(b, n), os.path.join(b, n.replace("Vidrala_v63_", "Vidrala_segundo_v63_", 1)))
pa = os.path.join(b, "acreditacion_libro.json")
if os.path.exists(pa):
    ac = json.load(open(pa, encoding="utf-8"))
    ac["archivo_final"]["archivo"] = ac["archivo_final"]["archivo"].replace("Vidrala_v63_", "Vidrala_segundo_v63_")
    json.dump(ac, open(pa, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
s = st(b)
s.update(auditoria=None, estado_analisis=None, cierres_archivados=[], material_auditoria=CIE.fijar_material(b, "Vidrala_segundo"))
guardar_st(b, s)
dest_b = CIE.ruta_resumen(b, json.load(open(T.CFG64, encoding="utf-8")))
pedir_auditoria(b, dest_b)
aceptar_auditoria(b)
rcs = paso14(b, dest_b)
paso("I", "(D1-1) dos expedientes de la misma empresa en la misma carpeta: el primer cierre legítimo de B (sin registro) no se bloquea y la fila y la vigencia de A no cambian",
     rcs == [0, 0, 0] and st(b).get("auditoria") == "APROBADO" and CIE.motivo_vigencia(a, VER) is None and "APROBADO" in fila_de(csv_piloto(a)),
     f"códigos de B {rcs} · A vigente: {CIE.motivo_vigencia(a, VER) is None} · fila de A {fila_de(csv_piloto(a))}")

# I2 (D1-2): sin registro ni respaldo y con el resumen imposible de actualizar: retirada pendiente visible (código 5) sin la aprobación interna
for via in ("ficha", "informe", "resumen"):
    c = T.copia_piloto(f"I2_{via}")
    for n in ("ficha.json", "cierre_vigente.json", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        os.remove(os.path.join(c, n))
    os.makedirs(os.path.join(os.path.dirname(c), "resumen_v2_historial.csv"))  # el historial es una carpeta: _retirar_fila falla (OSError)
    rc, out = corre_sc(*{"ficha": ("ficha.py", c), "informe": ("informe.py", c), "resumen": ("resumen.py", c, csv_piloto(c))}[via])
    paso("I", f"(D1-2) sin registro y con el destino imposible de actualizar, {via}: código 5, retirada pendiente visible y sin aprobación interna",
         rc == 5 and st(c).get("auditoria") != "APROBADO" and "retirada_pendiente" in registro(c) and bool(CIE.retiradas_pendientes(c)),
         f"código {rc} · {foto(c)}")

# I3 (D1-3): estado ilegible en la primera llamada; al restaurarlo, ninguna vía vuelve a cerrar ni a publicar la aprobación antigua
c = T.copia_piloto("I3")
ep = os.path.join(c, "estado_pipeline.json")
guard = open(ep, encoding="utf-8").read()
os.remove(os.path.join(c, "ficha.json")); os.remove(os.path.join(c, "cierre_vigente.json"))
open(ep, "w", encoding="utf-8").write("{")
rc0, _ = corre_sc("resumen.py", c, csv_piloto(c))
open(ep, "w", encoding="utf-8").write(guard)
rcs = [corre_sc("ficha.py", c, "--estado", "concluido")[0], corre_sc("informe.py", c)[0], corre_sc("resumen.py", c, csv_piloto(c))[0]]
paso("I", "(D1-3) estado ilegible en la primera llamada y restaurado después: ficha, informe y resumen no reactivan la aprobación antigua",
     0 not in rcs and not filas_aprobadas(c) and st(c).get("auditoria") != "APROBADO" and "publicada" not in registro(c),
     f"códigos {rc0}/{rcs} · {foto(c)}")

# I4 (D1-4): registro de publicaciones ilegible en el intervalo legítimo: retirada pendiente (código 5) sin perder la aprobación nueva
c = T.copia_piloto("I4")
pedir_auditoria(c, csv_piloto(c))
sid = aceptar_auditoria(c)
p = os.path.join(c, CIE.REGISTRO_RESUMEN)
guard = open(p, encoding="utf-8").read()
open(p, "w", encoding="utf-8").write("{")
os.remove(os.path.join(c, CIE.RESPALDO_RESUMEN))
r1 = paso14(c, csv_piloto(c))
conserva = st(c).get("auditoria") == "APROBADO" and not any(e.get("solicitud") == sid for e in anotadas(c))
open(p, "w", encoding="utf-8").write(guard)
r2 = paso14(c, csv_piloto(c))
paso("I", "(D1-4) registro ilegible en el intervalo: el paso 14 queda en retirada pendiente sin perder la aprobación nueva, y cierra al restaurar el registro",
     r1[0] == 5 and conserva and r2 == [0, 0, 0] and CIE.motivo_vigencia(c, VER) is None, f"códigos {r1} → {r2} · {foto(c)}")

# I5 (D1-5): cierre anterior a la 4.8.1 (ensayo 4.6.1): H5 y restauración de los archivos antiguos
d = os.path.join(T.TMP, "vigencia", "I5")
shutil.rmtree(d, ignore_errors=True)
shutil.copytree(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1"), d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc", "__pycache__", "prompts_generados"))
c = os.path.join(d, "Vidrala")
guard = os.path.join(d, "_guardados"); os.makedirs(guard)
for n in ("ficha.json", "cierre_vigente.json", "informe.md", "estado_pipeline.json"):
    shutil.copy2(os.path.join(c, n), os.path.join(guard, n))
vig0 = CIE.motivo_vigencia(c, VER) is None
os.remove(os.path.join(c, "ficha.json")); os.remove(os.path.join(c, "cierre_vigente.json"))
rc1, _ = corre_sc("resumen.py", c, os.path.join(d, "resumen_v2.csv"))
retirado = st(c).get("auditoria") != "APROBADO"
for n in os.listdir(guard):
    shutil.copy2(os.path.join(guard, n), os.path.join(c, n))
rc2, _ = corre_sc("resumen.py", c, os.path.join(d, "resumen_v2.csv"))
paso("I", "(D1-5) cierre anterior a la 4.8.1: H5 retira también la aprobación interna y restaurar ficha, cierre, informe y estado no la reactiva",
     vig0 and retirado and rc2 != 0 and st(c).get("auditoria") != "APROBADO" and "APROBADO" not in fila_de(os.path.join(d, "resumen_v2.csv")),
     f"vigente antes {vig0} · códigos {rc1}/{rc2} · {foto(c)}")

# I6 (D1-6): aprobaciones_retiradas.json ilegible no retira un cierre vigente sano
c = T.copia_piloto("I6")
open(os.path.join(c, CIE.APROBACIONES_RETIRADAS), "w", encoding="utf-8").write("{roto")
rc, _ = corre_sc("resumen.py", c, csv_piloto(c))
paso("I", "(D1-6) aprobaciones_retiradas.json ilegible: un cierre vigente sano sigue vigente (las otras dos señales deciden)",
     rc == 0 and st(c).get("auditoria") == "APROBADO" and CIE.motivo_vigencia(c, VER) is None and "APROBADO" in fila_de(csv_piloto(c)), f"código {rc} · {foto(c)}")

# ---------- J · casos de la segunda revisión interna (D2) ----------
# J1 (D2-1): sin registro ni respaldo, la línea de la publicación del historial truncada (ruta larga) o con un espacio
largo = "/home/usuario_con_nombre_largo/Documentos/Proyectos_de_inversión/copias_de_trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/piloto/resumen_v2.csv"
for etq, ruta in (("ruta larga (línea truncada a 200 caracteres)", largo), ("ruta con un espacio", "/home/usuario/Mis proyectos/munger_v2_r1/piloto/resumen_v2.csv")):
    c = T.copia_piloto(f"J1_{len(etq)}")
    for n in ("ficha.json", "cierre_vigente.json", CIE.REGISTRO_RESUMEN, CIE.RESPALDO_RESUMEN):
        os.remove(os.path.join(c, n))
    s = st(c)
    s["historial"] = [("  $ python3 resumen.py Vidrala resumen_v2.csv → 0 · " + ("OK: fila de Vidrala, S.A. en " + ruta)[:200]) if isinstance(h, str) and "OK: fila de" in h else h
                      for h in s["historial"]]
    guardar_st(c, s)
    rc, _ = corre_sc("resumen.py", c, csv_piloto(c))
    paso("J", f"(D2-1) sin registro, {etq}: la fila publicada se retira junto al expediente (por la línea de la orden) y la aprobación interna se quita",
         st(c).get("auditoria") != "APROBADO" and "APROBADO" not in fila_de(csv_piloto(c)), f"código {rc} · {foto(c)}")

# J2 (D2-2): cierre vigente y una fila editada por una hoja de cálculo; la sincronización no retira la APROBACIÓN y resumen.py la vuelve a publicar
c = T.copia_piloto("J2")
cfg64 = json.load(open(T.CFG64, encoding="utf-8"))
csv64 = CIE.ruta_resumen(c, cfg64)
pedir_auditoria(c, csv64)
sid = aceptar_auditoria(c)
r = paso14(c, csv64)
F = json.load(open(os.path.join(c, "ficha.json"), encoding="utf-8"))
filas = list(csv.DictReader(open(csv64, encoding="utf-8", newline="")))
for f in filas:
    if f["empresa"] == F["empresa"]:
        f["precio_si"] = f"{float(f['precio_si']):.2f}"
with open(csv64, "w", encoding="utf-8", newline="") as fh:
    w = csv.DictWriter(fh, fieldnames=list(filas[0].keys()))
    w.writeheader()
    for f in filas:
        w.writerow(f)
CIE.sincronizar_resumenes(c, VER)
vig = CIE.motivo_vigencia(c, VER)
rc, _ = corre_sc("resumen.py", c, csv64)
paso("J", "(D2-2) fila editada y sincronización: el cierre vigente sigue vigente, su aprobación no consta como retirada y resumen.py la vuelve a publicar",
     r == [0, 0, 0] and vig is None and rc == 0 and st(c).get("auditoria") == "APROBADO" and not any(e.get("solicitud") == sid for e in anotadas(c))
     and "APROBADO" in fila_de(csv64), f"cierre {r} · vigencia {vig!r:.80} · resumen {rc} · {foto(c)}")

# J3 (D2-3): en el intervalo, un «paso 14 · FIN» que no es un cierre (no_entregable) no cuenta como publicación
c = T.copia_piloto("J3")
pedir_auditoria(c, csv_piloto(c))
sid = aceptar_auditoria(c)
s = st(c)
s["historial"] += [f"2026-11-14T11:00:00 · paso 13 · auditoría consumida: respuesta a la solicitud {sid} (SHA-256 …)",
                   "2026-11-14T11:05:00 · paso 14 · FIN · estado no_entregable · fallo_de_implementacion: reaplicar configuración (emulado)"]
guardar_st(c, s)
r = paso14(c, csv_piloto(c))
paso("J", "(D2-3) intervalo con un «paso 14 · FIN» de no_entregable: no cuenta como cierre publicado y el paso 14 reanudado cierra",
     r == [0, 0, 0] and st(c).get("auditoria") == "APROBADO" and not any(e.get("solicitud") == sid for e in anotadas(c)), f"códigos {r} · {foto(c)}")

n_ok = sum(r["resultado"] == "PASA" for r in RES)
print(f"{n_ok}/{len(RES)} pruebas de vigencia H5 (4.13.1) PASAN")
print("RESULTADO vigencia H5: " + ("PASA" if n_ok == len(RES) else "FALLA"))
if ARGS.json:
    json.dump(RES, open(ARGS.json, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
sys.exit(0 if n_ok == len(RES) else 1)
