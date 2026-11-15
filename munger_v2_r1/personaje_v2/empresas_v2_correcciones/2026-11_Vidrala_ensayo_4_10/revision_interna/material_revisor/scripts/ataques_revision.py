#!/usr/bin/env python3
"""Ataques propios de la revisión interna 4.10 (Claude, contexto separado). No modifica el árbol: trabaja en un temporal.

Uso: python3 -B ataques_revision.py RAIZ_PERSONAJE_V2 [--codigo DIR_CODIGO_4_9]
Sin LibreOffice: solo pipeline.py --desde 13 / reanudación del paso 13→14, ficha.py, informe.py, resumen.py y funciones de cierre_v2.

A1 · ficha sin marcadores (ambos) + cierre_vigente.json eliminado: ¿queda alguna aprobación incoherente (pendiente_de_datos/APROBADO)?
A2 · ficha {} + cierre_vigente.json eliminado: ¿fila sin empresa o APROBADO?
A3 · comprobante del libro con veredicto NO ÍNTEGRO (y SHA-256 correcto): ¿motivo_acreditacion_libro lo acepta?
A4 · comprobante del libro que nombra otro .xlsx del expediente (el de datos) con su SHA-256: ¿lo acepta?
A5 · comprobante eliminado después de un cierre de la 4.10 (con el comprobante en el material): ¿se retira?
"""
import csv, json, os, shutil, subprocess, sys, tempfile

RAIZ = os.path.abspath(sys.argv[1])
SCR = os.path.join(RAIZ, "scripts")
if "--codigo" in sys.argv:
    # copia temporal del árbol de código con los .py de otra versión (para comparar con la 4.9)
    alt = sys.argv[sys.argv.index("--codigo") + 1]
    base_cod = tempfile.mkdtemp(prefix="rev410_cod_", dir=os.environ.get("TMPDIR"))
    shutil.copytree(RAIZ, os.path.join(base_cod, "personaje_v2"), ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
    for x in ("v6", "kit_pipeline_munger"):
        os.symlink(os.path.join(os.path.dirname(RAIZ), x), os.path.join(base_cod, x))
    SCR = os.path.join(base_cod, "personaje_v2", "scripts")
    for f in os.listdir(alt):
        if f.endswith((".py", ".sh")):
            shutil.copy2(os.path.join(alt, f), os.path.join(SCR, f))
sys.path.insert(0, SCR)
sys.path.insert(0, os.path.join(RAIZ, "pruebas"))
sys.dont_write_bytecode = True
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402
import agentes_sinteticos as AG  # noqa: E402

PY = sys.executable
EXP = os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala")
TMP = tempfile.mkdtemp(prefix="rev410_", dir=os.environ.get("TMPDIR"))
R = []


def corre(script, *a):
    r = subprocess.run([PY, "-B", os.path.join(SCR, script), *a], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    return r.returncode, (r.stdout + r.stderr).strip()


def filas(p):
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.isfile(p) else []


def j(p):
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    except ValueError:
        return None


def cierre_base(nombre):
    base = os.path.join(TMP, nombre)
    d = os.path.join(base, "exp", "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(EXP), f)):
            shutil.copy2(os.path.join(os.path.dirname(EXP), f), os.path.join(base, "exp", f))
    corre("pipeline.py", d, "--desde", "13")
    AG.auditoria(d, "APROBADO")
    rc, out = corre("pipeline.py", d)
    pred = os.path.join(base, "exp", "resumen_v2.csv")
    ok = rc == 0 and (j(os.path.join(d, "estado_pipeline.json")) or {}).get("auditoria") == "APROBADO" and os.path.exists(os.path.join(d, "cierre_vigente.json"))
    return d, pred, ok, rc


def aprob_incoherentes(pred):
    return [(r.get("empresa"), r.get("estado_analisis"), r.get("verificacion")) for r in filas(pred)
            if r.get("verificacion") == "APROBADO" and (not r.get("empresa") or r.get("estado_analisis") != "concluido")]


def anota(id_, desc, detectado, det):
    R.append((id_, desc, detectado, det))
    print(f"{id_} · {'DETECTADO' if detectado else 'NO DETECTADO'} · {desc} · {det}", flush=True)


d0, pred0, ok0, rc0 = cierre_base("cierre")
print(f"cierre de partida: {'OK' if ok0 else 'FALLO'} (código {rc0}) · fila {[(r.get('estado_analisis'), r.get('verificacion')) for r in filas(pred0)]}")


def copia(nombre):
    dst = os.path.join(TMP, nombre)
    shutil.copytree(os.path.dirname(os.path.dirname(d0)), dst, symlinks=True)
    return os.path.join(dst, "exp", "Vidrala"), os.path.join(dst, "exp", "resumen_v2.csv")


# A1 y A2: marcadores perdidos + cierre_vigente.json eliminado (registro de publicaciones y estado del pipeline intactos)
for id_, mut, nombre in (("A1", lambda F: {**{k: v for k, v in F.items() if k != "cierre"}, "estado_analisis": "pendiente_de_datos"}, "ambos marcadores"),
                         ("A2", lambda F: {}, "ficha {}")):
    for via in ("resumen.py", "informe.py", "ficha.py --estado pendiente_de_datos"):
        d, pred = copia(f"{id_}_{via.split()[0]}")
        F = j(os.path.join(d, "ficha.json"))
        json.dump(mut(F), open(os.path.join(d, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False)
        os.remove(os.path.join(d, "cierre_vigente.json"))
        if via == "resumen.py":
            rc, out = corre("resumen.py", d, pred)
        elif via == "informe.py":
            rc, out = corre("informe.py", d)
            rc2, out2 = corre("resumen.py", d, pred)
            out += f" | luego resumen.py → {rc2}: {out2[-120:]}"
        else:
            rc, out = corre("ficha.py", d, "--estado", "pendiente_de_datos")
            rc2, out2 = corre("resumen.py", d, pred)
            out += f" | luego resumen.py → {rc2}: {out2[-120:]}"
        st = j(os.path.join(d, "estado_pipeline.json")) or {}
        inc = aprob_incoherentes(pred)
        hist = os.listdir(os.path.join(d, "historial_cierres")) if os.path.isdir(os.path.join(d, "historial_cierres")) else []
        detectado = not inc and st.get("auditoria") != "APROBADO"
        anota(id_, f"{nombre} + cierre_vigente.json eliminado · {via}", detectado,
              f"código {rc} · filas {[(r.get('empresa'), r.get('estado_analisis'), (r.get('verificacion') or '')[:24]) for r in filas(pred)]} · "
              f"estado_pipeline.auditoria {st.get('auditoria')!r} · estado_analisis {st.get('estado_analisis')!r} · historial {len(hist)} · {out[-160:]}")

# A3 y A4: comprobante del libro
d, pred = copia("A3")
ev = os.path.join(d, "Vidrala_v63_evaluada.xlsx")
ac = {"archivo_final": {"archivo": "Vidrala_v63_evaluada.xlsx", "sha256": CIE._sha(ev), "veredicto": "NO ÍNTEGRO · 3 fallos", "verificacion": "verificacion_libro_final.txt"},
      "caches": "fallidas"}
json.dump(ac, open(os.path.join(d, "acreditacion_libro.json"), "w", encoding="utf-8"), ensure_ascii=False)
m = CIE.motivo_acreditacion_libro(d)
anota("A3", "comprobante con SHA-256 correcto y veredicto «NO ÍNTEGRO» (acreditar_libro.py lo escribe igual y sale con 1)", m is not None, f"motivo_acreditacion_libro → {m!r}")
dat = os.path.join(d, "Vidrala_v63_datos.xlsx")
ac = {"archivo_final": {"archivo": "Vidrala_v63_datos.xlsx", "sha256": CIE._sha(dat), "veredicto": "ÍNTEGRO · 0 fallos · 0 avisos"}}
json.dump(ac, open(os.path.join(d, "acreditacion_libro.json"), "w", encoding="utf-8"), ensure_ascii=False)
F = j(os.path.join(d, "ficha.json")) or {}
m = CIE.motivo_acreditacion_libro(d)
anota("A4", "comprobante que acredita el libro de DATOS (no el evaluado) con su SHA-256", m is not None,
      f"motivo_acreditacion_libro → {m!r} · ficha.hashes.libro_evaluado {str((F.get('hashes') or {}).get('libro_evaluado'))[:12]}… · evaluado {CIE._sha(ev)[:12]}…")
F2 = j(os.path.join(d, "ficha_provisional.json")) or {}
for fic in ("ficha.json", "ficha_provisional.json"):
    p = os.path.join(d, fic)
    G = j(p) or {}
    (G.get("hashes") or {}).pop("libro_evaluado", None)
    json.dump(G, open(p, "w", encoding="utf-8"), ensure_ascii=False)
m = CIE.motivo_acreditacion_libro(d)
anota("A4b", "lo mismo, sin «hashes.libro_evaluado» en las fichas (solo funciones; el material ya cambió aparte)", m is not None, f"motivo_acreditacion_libro → {m!r}")

# A5: cierre de la 4.10 con comprobante en el material; después se elimina el comprobante
base5 = os.path.join(TMP, "A5")
d5 = os.path.join(base5, "exp", "Vidrala")
shutil.copytree(EXP, d5, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
ref = subprocess.run([PY, os.path.join(SCR, "config_v2.py"), "plantilla.referencia", os.path.join(os.path.dirname(SCR), "config_v2.json")], capture_output=True, text=True).stdout.strip()
ver = subprocess.run([PY, os.path.join(SCR, "config_v2.py"), "plantilla.verificador", os.path.join(os.path.dirname(SCR), "config_v2.json")], capture_output=True, text=True).stdout.strip()
rca, outa = corre("acreditar_libro.py", d5, os.path.join(d5, "Vidrala_v63_evaluada.xlsx"), os.path.join(d5, "Vidrala_v63_datos.xlsx"), ref, ver, "sin_copia_recalculada")
corre("pipeline.py", d5, "--desde", "13")
AG.auditoria(d5, "APROBADO")
rc5, _ = corre("pipeline.py", d5)
en_material = CIE.ACREDITACION_LIBRO in ((j(os.path.join(d5, "material_auditoria.json")) or {}).get("archivos") or {})
os.remove(os.path.join(d5, CIE.ACREDITACION_LIBRO))
m = CIE.motivo_vigencia(d5, pipeline.Pipeline.veredicto_auditoria)
anota("A5", "comprobante eliminado después de un cierre que lo tenía en el material", m is not None,
      f"acreditar_libro {rca} · cierre {rc5} · en el material {en_material} · motivo_vigencia → {str(m)[:140]!r}")

json.dump([{"id": a, "ataque": b, "detectado": c, "detalle": d} for a, b, c, d in R], open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "salidas",
          "ataques_revision" + ("_codigo_4_9" if "--codigo" in sys.argv else "") + ".json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
shutil.rmtree(TMP, ignore_errors=True)
