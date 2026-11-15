#!/usr/bin/env python3
"""Reproducción de X-a y X-c (control de vigencia de la 4.7.1; encargo 4.8, §4) con el código de un árbol dado.
Solo escribe en un temporal: ni el árbol cuyo código se prueba ni el expediente de referencia se modifican.

Uso: python3 -I reproducir_xa_xc.py --raiz <munger_v2_r1 cuyo código se prueba> [--caso xa|xc|ambos] [--etiqueta TEXTO]

X-a (reproducido externamente por la revisión de la 4.7.1). Copia del expediente aprobado de la 4.6.1 con su resumen_v2.csv y su
historial; se eliminan de la copia fase1_v63.json y texto/ y se ejecuta UNA vez `pipeline.py COPIA --desde 2`. Se observa la
primera salida: código, mensaje final, estado_pipeline.json (estado, auditoría, paso, cierres archivados), ficha.json, informe.md,
diagnóstico y la fila del resumen.

X-c (declarado por el auditor interno de la 4.7.1). Copia del código (personaje_v2 sin expedientes; v6 y el kit enlazados) en la que
se rompe a propósito esquema/ficha.esquema.json (un campo obligatorio inexistente), y copia del mismo expediente aprobado; se ejecuta
UNA vez `pipeline.py COPIA --desde 14` con ese código. Se observan las mismas cosas, y además si alguna ficha no_entregable lleva
`cierre` y a qué causa atribuyen el rechazo el mensaje, el estado y el diagnóstico.
"""
import argparse
import csv
import json
import os
import shutil
import subprocess
import sys
import tempfile

ap = argparse.ArgumentParser()
ap.add_argument("--raiz", required=True)
ap.add_argument("--caso", default="ambos", choices=("xa", "xc", "ambos"))
ap.add_argument("--etiqueta", help="nombre del código que se prueba en la salida (por defecto, la ruta)")
a = ap.parse_args()
RAIZ = os.path.abspath(a.raiz)
EXP = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
EMPRESA = "Vidrala, S.A."
ENV = {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"}


def j(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def copia_expediente(tmp):
    base = os.path.join(tmp, "exp")
    d = os.path.join(base, "Vidrala")
    shutil.copytree(EXP, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        shutil.copy(os.path.join(os.path.dirname(EXP), f), os.path.join(base, f))
    return d


def observar(d, rc, out):
    st = j(os.path.join(d, "estado_pipeline.json")) or {}
    fi = j(os.path.join(d, "ficha.json"))
    dg = j(os.path.join(d, "diagnostico.json")) or {}
    filas = [r for r in csv.DictReader(open(os.path.join(os.path.dirname(d), "resumen_v2.csv"), encoding="utf-8")) if r.get("empresa") == EMPRESA]
    hist = os.path.join(d, "historial_cierres")
    archivadas = []
    for x in sorted(os.listdir(hist)) if os.path.isdir(hist) else []:
        f = j(os.path.join(hist, x, "ficha.json"))
        archivadas.append((x, (f or {}).get("estado_analisis"), bool((f or {}).get("cierre"))))
    ultimas = [l for l in out.splitlines() if l.strip()][-3:]
    print(f"   código de salida: {rc}")
    print("   últimas líneas: " + " | ".join(l.strip()[:150] for l in ultimas))
    print(f"   estado_pipeline.json: estado_analisis={st.get('estado_analisis')!r} · auditoria={st.get('auditoria')!r} · paso={st.get('paso')!r} · "
          f"cierres_archivados={len(st.get('cierres_archivados') or [])} · ficha_valida={st.get('ficha_valida')!r}")
    print(f"   ficha.json: " + ("ninguna" if fi is None else f"estado={fi.get('estado_analisis')!r} · cierre={fi.get('cierre')!r}"))
    print(f"   informe.md: {'sí' if os.path.exists(os.path.join(d, 'informe.md')) else 'no'} · cierre_vigente.json: {'sí' if os.path.exists(os.path.join(d, 'cierre_vigente.json')) else 'no'}")
    print(f"   diagnostico.json: estado={dg.get('estado_analisis')!r} · causa={((dg.get('causa') or {}).get('tipo'))!r} · detalle={str((dg.get('causa') or {}).get('detalle'))[:150]!r} · "
          f"paso={dg.get('paso_en_que_se_detuvo')!r} · desde_que_paso={(dg.get('para_continuar') or {}).get('desde_que_paso')!r} · que_hace_falta={str((dg.get('para_continuar') or {}).get('que_hace_falta'))[:150]!r}")
    print(f"   fila del resumen: {[(r.get('estado_analisis'), (r.get('verificacion') or '')[:60]) for r in filas]}")
    print(f"   carpetas archivadas: {archivadas}")
    return st, fi, dg, filas, archivadas


def caso_xa():
    tmp = tempfile.mkdtemp(prefix="xa_")
    try:
        d = copia_expediente(tmp)
        os.remove(os.path.join(d, "fase1_v63.json"))
        shutil.rmtree(os.path.join(d, "texto"))
        print("X-a · copia aprobada de la 4.6.1, sin fase1_v63.json ni texto/ · pipeline.py COPIA --desde 2 (una sola ejecución)")
        r = subprocess.run([sys.executable, "-B", os.path.join(RAIZ, "personaje_v2", "scripts", "pipeline.py"), d, "--desde", "2"], capture_output=True, text=True, env=ENV)
        st, fi, dg, filas, arch = observar(d, r.returncode, r.stdout + r.stderr)
        coherente = (r.returncode == 0 and st.get("estado_analisis") == "pendiente_de_datos" and st.get("auditoria") is None
                     and fi is not None and fi.get("estado_analisis") == "pendiente_de_datos" and not fi.get("cierre")
                     and dg.get("estado_analisis") == "pendiente_de_datos" and filas and all(f.get("estado_analisis") == "pendiente_de_datos" for f in filas)
                     and any(e == "concluido" and c for _, e, c in arch))
        print("   X-a " + ("NO SE REPRODUCE: estado, ficha, diagnóstico y resumen coherentes en la primera ejecución; aprobación caducada retirada y archivada"
                          if coherente else "REPRODUCIDO: la primera ejecución deja un estado incoherente"))
        return coherente
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def caso_xc():
    tmp = tempfile.mkdtemp(prefix="xc_")
    try:
        raiz = os.path.join(tmp, "raiz")
        os.makedirs(raiz)
        shutil.copytree(os.path.join(RAIZ, "personaje_v2"), os.path.join(raiz, "personaje_v2"),
                        ignore=shutil.ignore_patterns("empresas_v2", "empresas_v2_correcciones", "pruebas", ".lo_perfil", "__pycache__"))
        for x in ("v6", "kit_pipeline_munger"):
            os.symlink(os.path.join(RAIZ, x), os.path.join(raiz, x))
        esq = os.path.join(raiz, "personaje_v2", "esquema", "ficha.esquema.json")
        e = json.load(open(esq, encoding="utf-8"))
        e["required"] = list(e["required"]) + ["campo_inexistente_xc"]
        json.dump(e, open(esq, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        d = copia_expediente(tmp)
        print("X-c · código con esquema de ficha roto (campo obligatorio inexistente) · copia aprobada de la 4.6.1 · pipeline.py COPIA --desde 14 (una sola ejecución)")
        r = subprocess.run([sys.executable, "-B", os.path.join(raiz, "personaje_v2", "scripts", "pipeline.py"), d, "--desde", "14"], capture_output=True, text=True, env=ENV)
        out = r.stdout + r.stderr
        st, fi, dg, filas, arch = observar(d, r.returncode, out)
        no_ent_con_cierre = (fi is not None and fi.get("estado_analisis") == "no_entregable" and fi.get("cierre")) or any(e == "no_entregable" and c for _, e, c in arch)
        print(f"   ¿alguna ficha no_entregable con «cierre» (actual o archivada)? {'sí' if no_ent_con_cierre else 'no'}")
        causa_esquema = "esquema" in str((dg.get("causa") or {}).get("detalle") or "") and "esquema" in out.splitlines()[-1] if out.strip() else False
        coherente = (r.returncode == 0 and not no_ent_con_cierre and st.get("estado_analisis") == "no_entregable" and st.get("auditoria") is None
                     and fi is not None and fi.get("estado_analisis") == "no_entregable" and dg.get("estado_analisis") == "no_entregable"
                     and (dg.get("causa") or {}).get("tipo") == "fallo_de_implementacion" and causa_esquema
                     and "CIERRE RECHAZADO" not in out and filas and all(f.get("estado_analisis") == "no_entregable" for f in filas)
                     and any(e == "concluido" and c for _, e, c in arch))
        print("   X-c " + ("NO SE REPRODUCE: no_entregable sin cierre, atribuido al fallo de esquema en el estado, el diagnóstico y el mensaje; aprobación anterior archivada"
                          if coherente else "REPRODUCIDO: estado mixto o causa atribuida a otra cosa"))
        return coherente
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


print(f"código: {a.etiqueta or RAIZ}")
res = {}
if a.caso in ("xa", "ambos"):
    res["xa"] = caso_xa()
if a.caso in ("xc", "ambos"):
    res["xc"] = caso_xc()
print("RESULTADO: " + " · ".join(f"{k.upper().replace('X', 'X-')} {'coherente' if v else 'incoherente'}" for k, v in res.items()))
