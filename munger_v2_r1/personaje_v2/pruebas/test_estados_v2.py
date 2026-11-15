#!/usr/bin/env python3
"""Batería de coherencia de estados (entrega 4.8, encargo §4: X-a y X-c). Trabaja solo en directorios temporales; no modifica el
expediente de referencia ni el código del árbol.

Uso: python3 -B pruebas/test_estados_v2.py [--expediente <carpeta Vidrala aprobada de la 4.6.1>]

Observa la PRIMERA salida de cada ejecución (código, última línea, estado_pipeline.json, ficha.json, informe.md, cierre_vigente.json,
diagnóstico, fila del resumen, historial del resumen y archivo de cierres), no solo los códigos:
  A · falta de datos tras un cierre previo (X-a): copia aprobada sin fase1_v63.json ni texto/, `--desde 2`; segunda ejecución sin
      cambios; retirada pendiente (código 5) y relanzamiento con el destino recuperado (Z-a); terminar() llamado directamente.
  B · fallo de esquema al cerrar (X-c): código con esquema/ficha.esquema.json roto a propósito, `--desde 14`; ficha.py directo con
      no_entregable en el paso 14; subsanación (esquema restaurado y `--desde 13`: exige una auditoría nueva).
  C · estados tempranos legítimos: expediente sin etapa 1 ni cierre previo (pendiente_de_datos en el paso 1), fallo de migración
      tras un cierre previo (no_entregable en el paso 1), parada sin estado final (--hasta) y ficha que no se puede escribir.
  D · cierre válido sin cambios: relanzamiento sin `--desde` y con `--desde 14`.
  E · rechazo de material modificado (4.6.1, sin cambios): fase_c.json modificado y `--desde 14`.
  F · la regla H2 (Pipeline.veredicto_auditoria) es idéntica a la de la 4.7.1.
"""
import argparse
import csv
import hashlib
import inspect
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SCR = os.path.join(RAIZ, "scripts")
sys.path.insert(0, SCR)
sys.dont_write_bytecode = True
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import config_v2  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import pipeline  # noqa: E402

PY = sys.executable
PIPE = os.path.join(SCR, "pipeline.py")
TMP = tempfile.mkdtemp(prefix="estados48_")
EMPRESA = "Vidrala, S.A."
MATERIAL = "74b94f8072dd58c1"
H2_SHA_4_7_1 = "9edf6252ca48c80009b5b51b52aeaa447960ab611150b908738194e526775422"  # inspect.getsource de veredicto_auditoria, código 4.7.1
R = []


def paso(grupo, nombre, ok, detalle=""):
    R.append((grupo, nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + f" · {grupo} · {nombre}" + (f" · {detalle}" if detalle else ""))


def j(c, f):
    p = os.path.join(c, f)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.exists(p) else None


def copia(exp, nombre):
    base = os.path.join(TMP, nombre, "exp")
    d = os.path.join(base, "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(exp), f)):
            shutil.copy(os.path.join(os.path.dirname(exp), f), os.path.join(base, f))
    return d


def corre(d, *extra, pipe=PIPE):
    r = subprocess.run([PY, "-B", pipe, d, *extra], capture_output=True, text=True, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})
    out = (r.stdout + r.stderr).strip()
    return r.returncode, out, (out.splitlines() or [""])[-1]


def filas(d, empresa=EMPRESA):
    p = os.path.join(os.path.dirname(d), "resumen_v2.csv")
    return [r for r in csv.DictReader(open(p, encoding="utf-8"))] if os.path.exists(p) and empresa is None else \
        [r for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == empresa] if os.path.exists(p) else []


def historial_resumen(d):
    p = os.path.join(os.path.dirname(d), "resumen_v2_historial.csv")
    return list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []


def archivos(d):
    h = os.path.join(d, "historial_cierres")
    out = []
    for x in sorted(os.listdir(h)) if os.path.isdir(h) else []:
        f = j(os.path.join(h, x), "ficha.json")
        out.append({"carpeta": x, "estado": (f or {}).get("estado_analisis"), "cierre": bool((f or {}).get("cierre")),
                    "retirada": os.path.exists(os.path.join(h, x, "RETIRADA.json"))})
    return out


def aprobacion_en_historial(d):
    return any(r.get("estado_analisis") == "concluido" and r.get("verificacion") == "APROBADO" and r.get("material_auditado") == MATERIAL for r in historial_resumen(d))


def codigo_con_esquema_roto():
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
    return os.path.join(raiz, "personaje_v2", "scripts", "pipeline.py"), os.path.join(raiz, "personaje_v2", "scripts", "ficha.py")


def grupo_a(exp):
    G = "A falta de datos tras un cierre previo (X-a)"
    d = copia(exp, "xa")
    os.remove(os.path.join(d, "fase1_v63.json"))
    shutil.rmtree(os.path.join(d, "texto"))
    arch0 = len(archivos(d))
    rc, out, ult = corre(d, "--desde", "2")
    st, fi, dg = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json"), j(d, "diagnostico.json") or {}
    paso(G, "código 0 y la última línea dice pendiente_de_datos y su causa (primera ejecución)",
         rc == 0 and ult.startswith("estado final: pendiente_de_datos · paso 2") and "falta_de_datos" in ult, ult[:160])
    paso(G, "estado_pipeline.json en la primera ejecución: pendiente_de_datos, paso 2, auditoría retirada (None)",
         st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 2 and st.get("auditoria") is None,
         f"{st.get('estado_analisis')!r} · paso {st.get('paso')} · auditoría {st.get('auditoria')!r}")
    paso(G, "ficha.json pendiente_de_datos sin «cierre», sin cubo de compra y sin cierre_vigente.json",
         fi is not None and fi.get("estado_analisis") == "pendiente_de_datos" and not fi.get("cierre") and (fi.get("decision") or {}).get("accion") is None
         and not os.path.exists(os.path.join(d, "cierre_vigente.json")), f"ficha {(fi or {}).get('estado_analisis')} · cierre {(fi or {}).get('cierre')}")
    inf = open(os.path.join(d, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "informe.md")) else ""
    paso(G, "informe.md regenerado con el estado pendiente_de_datos (no presenta el cierre anterior)", "pendiente_de_datos" in inf and "APROBADO del material" not in inf)
    paso(G, "diagnóstico coherente: pendiente_de_datos · falta_de_datos · paso 2 · continuar desde el paso 2",
         dg.get("estado_analisis") == "pendiente_de_datos" and (dg.get("causa") or {}).get("tipo") == "falta_de_datos" and dg.get("paso_en_que_se_detuvo") == 2
         and (dg.get("para_continuar") or {}).get("desde_que_paso") == 2)
    f = filas(d)
    paso(G, "fila del resumen pendiente_de_datos sin aprobación; la fila concluido/APROBADO del material anterior queda en el historial",
         len(f) == 1 and f[0].get("estado_analisis") == "pendiente_de_datos" and "APROBADO" not in (f[0].get("verificacion") or "") and aprobacion_en_historial(d),
         str([(r.get("estado_analisis"), (r.get("verificacion") or "")[:40]) for r in f]))
    ar = archivos(d)
    paso(G, "la ficha cerrada anterior queda archivada (una carpeta nueva con RETIRADA.json; el historial anterior se conserva)",
         len(ar) == arch0 + 1 and ar[-1]["estado"] == "concluido" and ar[-1]["cierre"] and ar[-1]["retirada"] and len(st.get("cierres_archivados") or []) == len(ar),
         str(ar))
    huellas = {x: sha(os.path.join(d, x)) for x in ("ficha.json", "informe.md", "estado_pipeline.json")}
    rc2, _, ult2 = corre(d)
    st2 = j(d, "estado_pipeline.json") or {}
    paso(G, "segunda ejecución sin cambios: código 0, mismo estado, ninguna carpeta archivada nueva, ficha e informe idénticos",
         rc2 == 0 and st2.get("estado_analisis") == "pendiente_de_datos" and len(archivos(d)) == len(ar)
         and sha(os.path.join(d, "ficha.json")) == huellas["ficha.json"] and sha(os.path.join(d, "informe.md")) == huellas["informe.md"], ult2[:120])
    # (4.8, Z-a de la auditoría interna) retirada pendiente (código 5) en una terminación que no cierra y relanzamiento tras recuperar el destino
    d4 = copia(exp, "xa_pendiente")
    os.remove(os.path.join(d4, "fase1_v63.json"))
    shutil.rmtree(os.path.join(d4, "texto"))
    pred = os.path.join(os.path.dirname(d4), "resumen_v2.csv")
    os.replace(pred, pred + ".guardado")
    os.makedirs(pred)  # destino inaccesible: una carpeta donde debería estar el CSV
    rc4, _, ult4 = corre(d4, "--desde", "2")
    st4 = j(d4, "estado_pipeline.json") or {}
    os.rmdir(pred)
    os.replace(pred + ".guardado", pred)
    rc5, _, ult5 = corre(d4)
    st5 = j(d4, "estado_pipeline.json") or {}
    f5 = filas(d4)
    paso(G, "retirada pendiente (código 5) y relanzamiento con el destino recuperado: se completa la retirada y se publica la fila pendiente_de_datos",
         rc4 == 5 and st4.get("estado_analisis") == "pendiente_de_datos" and st4.get("resumen_pendiente") is True and rc5 == 0
         and st5.get("estado_analisis") == "pendiente_de_datos" and not st5.get("resumen_pendiente")
         and len(f5) == 1 and f5[0].get("estado_analisis") == "pendiente_de_datos" and aprobacion_en_historial(d4),
         f"códigos {rc4} → {rc5} · fila {[(r.get('estado_analisis'), (r.get('verificacion') or '')[:30]) for r in f5]}")
    # terminar() directamente (V1 del control de vigencia de la 4.7.1)
    d3 = copia(exp, "xa_directo")
    cfg = config_v2.cargar(os.path.join(RAIZ, "config_v2.json"))
    p = pipeline.Pipeline(d3, cfg)
    p.st["paso"] = 2
    p.st["estado_analisis"] = None
    p.terminar("pendiente_de_datos", "falta_de_datos", "prueba directa de terminar() tras un cierre previo", 2, desde=2)
    st3 = j(d3, "estado_pipeline.json") or {}
    paso(G, "terminar() directo: memoria y disco dicen pendiente_de_datos; auditoría retirada; ficha sin cierre",
         p.st.get("estado_analisis") == "pendiente_de_datos" and st3.get("estado_analisis") == "pendiente_de_datos" and st3.get("auditoria") is None
         and not (j(d3, "ficha.json") or {}).get("cierre"), f"memoria {p.st.get('estado_analisis')!r} · disco {st3.get('estado_analisis')!r}")


def grupo_b(exp):
    G = "B fallo de esquema al cerrar (X-c)"
    pipe_roto, ficha_rota = codigo_con_esquema_roto()
    d = copia(exp, "xc")
    hist0 = list((j(d, "estado_pipeline.json") or {}).get("historial") or [])
    rc, out, ult = corre(d, "--desde", "14", pipe=pipe_roto)
    st, fi, dg = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json"), j(d, "diagnostico.json") or {}
    paso(G, "código 0 (estado final no_entregable), sin «CIERRE RECHAZADO» y con la causa de esquema en la última línea",
         rc == 0 and "CIERRE RECHAZADO" not in out and ult.startswith("estado final: no_entregable · paso 14") and "esquema" in ult, ult[:170])
    paso(G, "estado_pipeline.json: no_entregable, paso 14, auditoría None, ficha_valida False",
         st.get("estado_analisis") == "no_entregable" and st.get("paso") == 14 and st.get("auditoria") is None and st.get("ficha_valida") is False,
         f"{st.get('estado_analisis')!r} · paso {st.get('paso')} · auditoría {st.get('auditoria')!r} · válida {st.get('ficha_valida')!r}")
    ar = archivos(d)
    paso(G, "ficha.json no_entregable sin «cierre», sin cubo ni acción; ninguna ficha no_entregable archivada con «cierre»; sin cierre_vigente.json",
         fi is not None and fi.get("estado_analisis") == "no_entregable" and not fi.get("cierre") and fi.get("cubo") is None and fi.get("decision") is None
         and not any(a["estado"] == "no_entregable" and a["cierre"] for a in ar) and not os.path.exists(os.path.join(d, "cierre_vigente.json")), str(ar))
    det = str((dg.get("causa") or {}).get("detalle") or "")
    que = str((dg.get("para_continuar") or {}).get("que_hace_falta") or "")
    paso(G, "diagnóstico: fallo_de_implementacion por el esquema de la ficha (estado previsto concluido), paso 14, continuar desde el 13 con auditoría nueva",
         dg.get("estado_analisis") == "no_entregable" and (dg.get("causa") or {}).get("tipo") == "fallo_de_implementacion" and "esquema" in det
         and "estado previsto: concluido" in det and dg.get("paso_en_que_se_detuvo") == 14 and (dg.get("para_continuar") or {}).get("desde_que_paso") == 13
         and "auditoría nueva" in que and "auditoria = None" not in det, det[:120])
    f = filas(d)
    paso(G, "fila del resumen no_entregable sin aprobación; la aprobación anterior queda en el historial del resumen",
         len(f) == 1 and f[0].get("estado_analisis") == "no_entregable" and "APROBADO" not in (f[0].get("verificacion") or "") and aprobacion_en_historial(d),
         str([(r.get("estado_analisis"), (r.get("verificacion") or "")[:40]) for r in f]))
    hist = st.get("historial") or []
    paso(G, "historial conservado: las entradas anteriores siguen al principio y el archivo de la ficha cerrada consta en cierres_archivados",
         hist[:len(hist0)] == hist0 and any(c.get("material_auditado") == MATERIAL and c.get("auditoria_registrada") == "APROBADO" for c in (st.get("cierres_archivados") or [])[1:])
         and any("esquema" in h for h in hist[len(hist0):]), f"{len(hist0)} → {len(hist)} entradas")
    # subsanación: el esquema vuelve a ser el bueno; --desde 13 exige una auditoría nueva (no se reutiliza la archivada)
    rc2, out2, ult2 = corre(d, "--desde", "13")
    st2 = j(d, "estado_pipeline.json") or {}
    esp = open(os.path.join(d, "ESPERANDO.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "ESPERANDO.md")) else ""
    paso(G, "subsanación (esquema restaurado, --desde 13): espera una auditoría nueva (código 10), no publica ningún cierre con la aprobación archivada y el diagnóstico anterior pasa a .anterior",
         rc2 == 10 and "verificacion" in esp and st2.get("auditoria") is None and not (j(d, "ficha.json") or {}).get("cierre")
         and not os.path.exists(os.path.join(d, "cierre_vigente.json")) and not os.path.exists(os.path.join(d, "diagnostico.json"))
         and (j(d, "diagnostico.json.anterior") or {}).get("estado_analisis") == "no_entregable", ult2[:120])
    # ficha.py directo: no_entregable en el paso 14 con una aprobación registrada no recibe «cierre»
    d2 = copia(exp, "xc_ficha")
    r = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d2, "--estado", "no_entregable"], capture_output=True, text=True)
    f2 = j(d2, "ficha.json") or {}
    paso(G, "ficha.py directo con --estado no_entregable en el paso 14 y aprobación registrada: ficha sin «cierre», cierre anterior archivado, sin cierre_vigente.json",
         r.returncode == 0 and f2.get("estado_analisis") == "no_entregable" and not f2.get("cierre") and not os.path.exists(os.path.join(d2, "cierre_vigente.json"))
         and any(a["estado"] == "concluido" and a["cierre"] for a in archivos(d2)[1:]), (r.stdout + r.stderr).strip().splitlines()[-1][:120] if (r.stdout + r.stderr).strip() else "")


def grupo_c(exp):
    G = "C estados tempranos legítimos"
    d = os.path.join(TMP, "temprana", "exp", "EmpresaVacia")
    os.makedirs(d)
    rc, out, ult = corre(d)
    st, fi, dg = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json"), j(d, "diagnostico.json") or {}
    paso(G, "sin etapa 1 ni cierre previo: código 0, pendiente_de_datos en el paso 1, ficha sin cierre, diagnóstico, ningún archivo de cierres",
         rc == 0 and st.get("estado_analisis") == "pendiente_de_datos" and st.get("paso") == 1 and fi is not None and fi.get("estado_analisis") == "pendiente_de_datos"
         and not fi.get("cierre") and dg.get("estado_analisis") == "pendiente_de_datos" and not os.path.isdir(os.path.join(d, "historial_cierres"))
         and not st.get("cierres_archivados") and ult.startswith("estado final: pendiente_de_datos · paso 1"), ult[:140])
    d2 = copia(exp, "migracion")
    open(os.path.join(d2, "etapa1", "Vidrala_evaluada.xlsx"), "wb").write(b"no es un libro xlsx")
    arch0 = len(archivos(d2))
    rc, out, ult = corre(d2, "--desde", "1")
    st, fi, dg = j(d2, "estado_pipeline.json") or {}, j(d2, "ficha.json"), j(d2, "diagnostico.json") or {}
    f = filas(d2)
    paso(G, "fallo de migración tras un cierre previo: no_entregable en el paso 1 en memoria, disco, ficha (sin cierre), diagnóstico y resumen",
         rc == 0 and st.get("estado_analisis") == "no_entregable" and st.get("paso") == 1 and st.get("auditoria") is None and fi is not None
         and fi.get("estado_analisis") == "no_entregable" and not fi.get("cierre") and dg.get("estado_analisis") == "no_entregable"
         and dg.get("paso_en_que_se_detuvo") == 1 and len(f) == 1 and f[0].get("estado_analisis") == "no_entregable", ult[:140])
    ar = archivos(d2)
    paso(G, "fallo de migración tras un cierre previo: la ficha cerrada queda archivada con RETIRADA.json y la aprobación pasa al historial del resumen",
         len(ar) == arch0 + 1 and ar[-1]["estado"] == "concluido" and ar[-1]["cierre"] and ar[-1]["retirada"] and aprobacion_en_historial(d2), str(ar))


def grupo_c2(exp):
    G = "C estados tempranos legítimos"
    # (V-a del control de vigencia) ejecución que se detiene sin estado final (--hasta): código 0 y «estado final: None»
    d = copia(exp, "hasta")
    rc, out, ult = corre(d, "--desde", "3", "--hasta", "3")
    paso(G, "parada sin estado final (--desde 3 --hasta 3): código 0, sin traza y «estado final: None · paso 4»",
         rc == 0 and "Traceback" not in out and ult == "estado final: None · paso 4", ult[:120])
    # (V-b) ficha.py no puede escribir la ficha (alcance_v2.json ilegible): el estado no_entregable y su diagnóstico se conservan
    d2 = copia(exp, "alcance")
    os.remove(os.path.join(d2, "fase1_v63.json"))
    shutil.rmtree(os.path.join(d2, "texto"))
    open(os.path.join(d2, "alcance_v2.json"), "w", encoding="utf-8").write("{ilegible")
    rc, out, ult = corre(d2, "--desde", "2")
    st, dg = j(d2, "estado_pipeline.json") or {}, j(d2, "diagnostico.json") or {}
    paso(G, "ficha.py no llega a escribir la ficha (alcance ilegible): sin traza; estado y diagnóstico coinciden (no se pierde el estado final)",
         "Traceback" not in out and rc == 0 and st.get("estado_analisis") is not None and dg.get("estado_analisis") == st.get("estado_analisis"),
         f"código {rc} · estado {st.get('estado_analisis')!r} · diagnóstico {dg.get('estado_analisis')!r}")


def grupo_d(exp):
    G = "D cierre válido sin cambios"
    d = copia(exp, "valido")
    hu = {x: sha(os.path.join(d, x)) for x in ("ficha.json", "informe.md", "cierre_vigente.json")}
    arch0 = len(archivos(d))
    rc, out, ult = corre(d)
    paso(G, "relanzamiento sin --desde: código 0, concluido, ficha, informe y cierre_vigente.json idénticos, sin archivos nuevos",
         rc == 0 and ult == "estado final: concluido · paso 14" and all(sha(os.path.join(d, x)) == h for x, h in hu.items()) and len(archivos(d)) == arch0, ult[:120])
    rc, out, ult = corre(d, "--desde", "14")
    st, fi = j(d, "estado_pipeline.json") or {}, j(d, "ficha.json") or {}
    f = filas(d)
    paso(G, "--desde 14 sin cambios: código 0, concluido · APROBADO del material fijado, sin archivos nuevos, fila del resumen concluido/APROBADO",
         rc == 0 and st.get("estado_analisis") == "concluido" and st.get("auditoria") == "APROBADO" and (fi.get("cierre") or {}).get("material_auditado") == MATERIAL
         and os.path.exists(os.path.join(d, "cierre_vigente.json")) and len(archivos(d)) == arch0 and len(f) == 1 and f[0].get("estado_analisis") == "concluido"
         and f[0].get("verificacion") == "APROBADO" and CIE.motivo_vigencia(d, pipeline.Pipeline.veredicto_auditoria) is None, ult[:120])


def grupo_e(exp):
    G = "E rechazo de material modificado"
    d = copia(exp, "material")
    fc = j(d, "fase_c.json")
    fc["celdas"]["B101"] += " [MARCADOR 4.8]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    arch0 = len(archivos(d))
    rc, out, ult = corre(d, "--desde", "14")
    st = j(d, "estado_pipeline.json") or {}
    ar = archivos(d)
    ret = j(os.path.join(d, "historial_cierres", ar[-1]["carpeta"]), "RETIRADA.json") if ar else {}
    f = filas(d)
    paso(G, "código 4 (cierre rechazado), sin ficha ni informe oficiales, estado sin cierre (None, paso 13), auditoría retirada",
         rc == 4 and not os.path.exists(os.path.join(d, "ficha.json")) and not os.path.exists(os.path.join(d, "informe.md"))
         and st.get("estado_analisis") is None and st.get("paso") == 13 and st.get("auditoria") is None, ult[:120])
    paso(G, "archivo con el motivo del material cambiado, fila del resumen SIN APROBACIÓN VIGENTE y aprobación en el historial del resumen",
         len(ar) == arch0 + 1 and "material cambió" in str((ret or {}).get("motivo")) and len(f) == 1 and (f[0].get("verificacion") or "").startswith(CIE.NO_VIGENTE)
         and aprobacion_en_historial(d), str((ret or {}).get("motivo"))[:120])


def grupo_f():
    G = "F regla H2"
    h = hashlib.sha256(inspect.getsource(pipeline.Pipeline.veredicto_auditoria).encode()).hexdigest()
    paso(G, "Pipeline.veredicto_auditoria es idéntica a la de la 4.7.1 (la detección H2 no se rebaja)", h == H2_SHA_4_7_1, h[:16])


def main(exp):
    for g in (grupo_a, grupo_b, grupo_c, grupo_c2, grupo_d, grupo_e):
        try:
            g(exp)
        except Exception as e:  # noqa
            import traceback
            traceback.print_exc()
            paso(g.__name__, "excepción " + str(e)[:100], False)
    grupo_f()


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--expediente", default=os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
    a = ap.parse_args()
    try:
        main(os.path.abspath(a.expediente))
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    n = sum(ok for _, _, ok in R)
    print(f"\n{n}/{len(R)} pruebas de coherencia de estados PASAN")
    sys.exit(0 if n == len(R) else 1)
