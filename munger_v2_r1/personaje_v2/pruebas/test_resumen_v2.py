#!/usr/bin/env python3
"""Pruebas de aceptación de la retirada de aprobaciones en los resúmenes registrados (reparación 4.7, bloque A). Solo en temporales.

Uso: python3 -B pruebas/test_resumen_v2.py [--expediente <Vidrala aprobado de la 4.6.1>]

Trabajan sobre copias del expediente aprobado de la 4.6.1 (sin LibreOffice) y, para el estado temprano, sobre una empresa sintética.
Observan códigos, salidas oficiales, filas activas, historiales y el registro publicaciones_resumen.json antes y después.
"""
import argparse
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SCR = os.path.join(RAIZ, "scripts")
sys.path.insert(0, AQUI)
sys.path.insert(0, SCR)
sys.dont_write_bytecode = True
import cierre_v2 as CIE  # noqa: E402
import config_v2  # noqa: E402
import test_pipeline_sintetico as TP  # noqa: E402

PY = sys.executable
TMP = tempfile.mkdtemp(prefix="resumen47t_")
TP.BASE = TMP
R = []
EMP = "Vidrala, S.A."
REG = "publicaciones_resumen.json"  # constantes literales: la batería también se puede ejecutar contra el código 4.6.1
NO_VIG = "SIN APROBACIÓN VIGENTE"
N_CASO = [0]


def paso(nombre, ok, det=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + f" · resumen · {nombre}" + (f" · {det}" if det else ""))


def j(c, f):
    p = os.path.join(c, f)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def run(script, *args):
    r = subprocess.run([PY, "-B", os.path.join(SCR, script), *args], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def filas(p, empresa=EMP):
    return [r for r in csv.DictReader(open(p, encoding="utf-8"))] if os.path.exists(p) and os.path.isfile(p) else [] if empresa is None else \
        [r for r in csv.DictReader(open(p, encoding="utf-8")) if r.get("empresa") == empresa] if os.path.isfile(p) else []


def de(p, empresa=EMP):
    return [r for r in filas(p, None) if r.get("empresa") == empresa]


def caso(exp, absoluta=False):
    """Copia del expediente aprobado con su resumen predeterminado, y una configuración válida con resumen_csv personalizado
    (relativo a la configuración, o absoluto). El CSV personalizado lleva una fila ajena."""
    N_CASO[0] += 1
    base = os.path.join(TMP, f"c{N_CASO[0]:02d}")
    d = os.path.join(base, "exp", "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    for f in ("resumen_v2.csv", "resumen_v2_historial.csv"):
        if os.path.exists(os.path.join(os.path.dirname(exp), f)):
            shutil.copy(os.path.join(os.path.dirname(exp), f), os.path.join(base, "exp", f))
    cfg = {k: v for k, v in config_v2.cargar(os.path.join(RAIZ, "config_v2.json")).items() if not k.startswith("_")}
    os.makedirs(os.path.join(base, "cfg", "cartera"))
    pers = os.path.join(base, "cfg", "cartera", "resumen_global.csv")
    cfg["resumen_csv"] = pers if absoluta else "cartera/resumen_global.csv"
    conf = os.path.join(base, "cfg", "config.json")
    json.dump(cfg, open(conf, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    cols = list(csv.DictReader(open(os.path.join(base, "exp", "resumen_v2.csv"), encoding="utf-8")).fieldnames)
    with open(pers, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerow({k: "" for k in cols} | {"empresa": "Otra empresa (ajena)", "estado_analisis": "concluido", "verificacion": "APROBADO", "precio_si": "10"})
    return d, conf, pers, os.path.join(base, "exp", "resumen_v2.csv")


def aprobada(rows):
    return len(rows) == 1 and rows[0]["estado_analisis"] == "concluido" and rows[0]["verificacion"] == "APROBADO"


def retirada(rows):
    r0 = rows[0] if len(rows) == 1 else {}
    return len(rows) == 1 and r0["verificacion"].startswith(NO_VIG) and all(r0.get(k, "") == "" for k in ("estado_analisis", "precio_si", "accion", "ponderado", "zona", "cubo_v2"))


def hist(p):
    h = os.path.join(os.path.dirname(p), "resumen_v2_historial.csv")
    return de(h)


def ajena(p):
    return any(r["empresa"] == "Otra empresa (ajena)" and r["verificacion"] == "APROBADO" and r["precio_si"] == "10" for r in filas(p, None))


def marca(d):
    fc = j(d, "fase_c.json")
    fc["celdas"]["B101"] += " [MARCADOR 4.7]"
    json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def main(exp):
    # 1. secuencia externa completa, CSV personalizado relativo a la configuración
    d, conf, pers, pred = caso(exp)
    n_hist_pred = len(hist(pred))
    rc1, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    reg = j(d, REG) or {}
    paso("secuencia · publicación configurada: código 0, fila concluido / APROBADO en el CSV personalizado y destino registrado (ruta resuelta respecto a la configuración)",
         rc1 == 0 and aprobada(de(pers)) and any(e["csv"] == pers and e["estado"] == "publicada" and e["material_auditado"] for e in reg.get("publicaciones", [])), str([e["csv"][-40:] for e in reg.get("publicaciones", [])]))
    marca(d)
    rc2, out2 = run("informe.py", d)
    paso("secuencia · informe.py directo sin --config: código 3; inmediatamente después, el CSV personalizado y el predeterminado ya no presentan la aprobación; fila ajena intacta; historiales con la fila anterior",
         rc2 == 3 and retirada(de(pers)) and retirada(de(pred)) and ajena(pers) and len(hist(pers)) == 1 and hist(pers)[0]["verificacion"] == "APROBADO" and not os.path.exists(os.path.join(d, "ficha.json"))
         and len(hist(pred)) == n_hist_pred + 1 and hist(pred)[-1]["verificacion"] == "APROBADO",
         f"pers {[r['verificacion'][:30] for r in de(pers)]} · hist {len(hist(pers))} · hist pred {n_hist_pred}→{len(hist(pred))}")
    rc3, out3 = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("secuencia · relanzamiento configurado: código 4; el CSV personalizado sigue sin aprobación y sin historial duplicado", rc3 == 4 and retirada(de(pers)) and len(hist(pers)) == 1 and ajena(pers), f"código {rc3}")
    run("informe.py", d)
    run("ficha.py", d, "--estado", "concluido")
    paso("repetición estable: más invalidaciones no duplican filas ni historiales", retirada(de(pers)) and len(hist(pers)) == 1 and len(de(pred)) == 1 and ajena(pers))
    st_reg = [e["estado"] for e in (j(d, REG) or {}).get("publicaciones", [])]
    paso("registro de destinos: todas las publicaciones de la empresa quedan como «retirada»", st_reg and all(x == "retirada" for x in st_reg), str(st_reg))
    # 1b. una copia del expediente (con su registro) no retira las filas que publicó el original
    d0, conf0, pers0, pred0 = caso(exp)
    run("pipeline.py", d0, "--config", conf0, "--desde", "14")
    dc = os.path.join(os.path.dirname(os.path.dirname(d0)), "copia_del_expediente", "Vidrala")
    shutil.copytree(d0, dc)
    shutil.copy(pred0, os.path.join(os.path.dirname(dc), "resumen_v2.csv"))
    marca(dc)
    rc, _ = run("informe.py", dc)
    paso("copia del expediente invalidada: retira su propio resumen y no toca las filas que publicó el original (registro ligado al expediente)",
         rc == 3 and aprobada(de(pers0)) and aprobada(de(pred0)) and retirada(de(os.path.join(os.path.dirname(dc), "resumen_v2.csv"))))
    # 2. CSV personalizado con ruta absoluta; invalidación por el pipeline (sin pasar por los generadores)
    d, conf, pers, pred = caso(exp, absoluta=True)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    ok_pub = aprobada(de(pers))
    marca(d)
    rc, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("ruta absoluta · invalidación por el pipeline configurado: código 4; ficha, informe y fila personalizada retirados", ok_pub and rc == 4 and retirada(de(pers)) and not os.path.exists(os.path.join(d, "ficha.json")) and ajena(pers))
    # 3. invalidación por ficha.py directo
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    marca(d)
    rc, _ = run("ficha.py", d, "--estado", "concluido")
    paso("ficha.py directo sin --config: código 3 y retirada en el CSV personalizado registrado", rc == 3 and retirada(de(pers)) and not os.path.exists(os.path.join(d, "ficha.json")))
    # 4. invalidación por resumen.py directo con otro destino explícito
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    marca(d)
    otro = os.path.join(os.path.dirname(pers), "otro_destino.csv")
    rc, _ = run("resumen.py", d, otro)
    paso("resumen.py directo con otro destino: código 3; retirada también en el CSV personalizado registrado; el destino nuevo no recibe una aprobación",
         rc == 3 and retirada(de(pers)) and not any(r["verificacion"] == "APROBADO" for r in de(otro)))
    # 5. publicación directa de resumen.py con destino explícito, registro y retirada posterior
    d, conf, pers, pred = caso(exp)
    otro = os.path.join(os.path.dirname(pers), "explicito.csv")
    rc_a, _ = run("resumen.py", d, otro)
    reg = j(d, REG) or {}
    paso("resumen.py con destino explícito y material intacto: código 0, fila aprobada y destino registrado con el material", rc_a == 0 and aprobada(de(otro))
         and any(e["csv"] == otro and e["material_auditado"] == (j(d, "cierre_vigente.json") or {}).get("material_auditado") for e in reg.get("publicaciones", [])))
    marca(d)
    rc_b, _ = run("informe.py", d)
    paso("…y una invalidación posterior lo retira en ese destino explícito", rc_b == 3 and retirada(de(otro)))
    # 6. retirada pendiente: destino inaccesible con las demás salidas ya archivadas
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    copia = open(pers, encoding="utf-8").read()
    os.remove(pers)
    os.makedirs(pers)  # el destino deja de ser un archivo accesible
    marca(d)
    rc, out = run("informe.py", d)
    reg = j(d, REG) or {}
    e = next((x for x in reg.get("publicaciones", []) if x["csv"] == pers), {})
    paso("destino inaccesible: código 5 (error operativo), retirada pendiente registrada con su error; ficha, informe y cierre ya archivados",
         rc == 5 and e.get("estado") == "retirada_pendiente" and e.get("error") and not os.path.exists(os.path.join(d, "ficha.json")) and "RETIRADA PENDIENTE" in out, (e.get("error") or "")[:80])
    rc_p, out_p = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("con la retirada pendiente, el pipeline se detiene con código 5 y no declara nada completado", rc_p == 5 and "RETIRADA PENDIENTE" in out_p)
    shutil.rmtree(pers)
    open(pers, "w", encoding="utf-8").write(copia)
    rc_q, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    e = next((x for x in (j(d, REG) or {}).get("publicaciones", []) if x["csv"] == pers), {})
    paso("al recuperar el acceso, el reintento retira la fila (ficha, informe y cierre ya archivados), sin duplicar historial, y el rechazo sigue (código 4)",
         rc_q == 4 and e.get("estado") == "retirada" and retirada(de(pers)) and len(hist(pers)) == 1 and ajena(pers), f"código {rc_q} · {e.get('estado')}")
    # 7. material intacto conserva su aprobación
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    n_arch = len(os.listdir(os.path.join(d, "historial_cierres"))) if os.path.isdir(os.path.join(d, "historial_cierres")) else 0
    r1, _ = run("informe.py", d)
    r2, _ = run("ficha.py", d, "--estado", "concluido")
    r3, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("material intacto: generadores y pipeline configurado con código 0; la fila personalizada conserva concluido / APROBADO; sin historial",
         r1 == r2 == r3 == 0 and aprobada(de(pers)) and not hist(pers) and len(os.listdir(os.path.join(d, "historial_cierres"))) == n_arch, f"{r1} {r2} {r3}")
    # 8. auditoría nueva válida del material modificado: cierre y publicación del material nuevo
    marca(d)
    rc, _ = run("pipeline.py", d, "--config", conf)
    st = j(d, "estado_pipeline.json")
    fp = j(d, "ficha_provisional.json") or {}
    paso("material modificado: el pipeline prepara material provisional (confirmado = false) y espera una auditoría nueva; fila personalizada retirada",
         rc == 10 and st["paso"] == 13 and (fp.get("provisional") or {}).get("confirmado") is False and retirada(de(pers)))
    nuevo = (j(d, "material_auditoria.json") or {}).get("id")
    aud = open(os.path.join(d, "historial_cierres", sorted(os.listdir(os.path.join(d, "historial_cierres")))[-1], "auditoria_en_el_momento_de_la_retirada.md"), encoding="utf-8").read()
    sol = (j(d, "solicitud_auditoria.json") or {}).get("id")  # (4.8.1, R-T1) el auditor simulado responde a la solicitud vigente
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write(re.sub(r"Material auditado: [0-9a-f]{16}", f"Material auditado: {nuevo}\nSolicitud de auditoría: {sol}", aud))  # auditor simulado del material nuevo
    rc, _ = run("pipeline.py", d, "--config", conf)
    reg = j(d, REG) or {}
    paso("auditoría nueva válida: cierre del material nuevo y fila personalizada concluido / APROBADO registrada con ese material; historial conservado",
         rc == 0 and aprobada(de(pers)) and any(e["csv"] == pers and e["estado"] == "publicada" and e["material_auditado"] == nuevo for e in reg.get("publicaciones", [])) and len(hist(pers)) == 1 and ajena(pers), f"código {rc}")
    # 10. (auditoría interna, H-1) carpeta del destino ausente en el momento de la invalidación
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    cart = os.path.dirname(pers)
    shutil.move(cart, cart + "_fuera")
    marca(d)
    rc, out = run("informe.py", d)
    e = next((x for x in (j(d, REG) or {}).get("publicaciones", []) if x["csv"] == pers), {})
    ok1 = rc == 5 and e.get("estado") == "retirada_pendiente" and "RETIRADA PENDIENTE" in out
    shutil.move(cart + "_fuera", cart)
    rc2, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("carpeta del destino ausente: código 5 y retirada pendiente (no «retirada»); al volver la carpeta, el relanzamiento retira la fila (código 4)",
         ok1 and rc2 == 4 and retirada(de(pers)) and ajena(pers), f"{rc} {e.get('estado')} {rc2}")
    # 11. (H-1) CSV ausente en una carpeta accesible: se vigila y se retira si reaparece
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    shutil.move(pers, pers + ".fuera")
    marca(d)
    rc, _ = run("informe.py", d)
    e = next((x for x in (j(d, REG) or {}).get("publicaciones", []) if x["csv"] == pers), {})
    ok1 = rc == 3 and e.get("estado") == "sin_archivo"
    shutil.move(pers + ".fuera", pers)
    rc2, _ = run("resumen.py", d, pred)
    paso("CSV ausente en carpeta accesible: queda «sin_archivo»; si reaparece con la aprobación, la siguiente llamada (resumen.py sin ficha) la retira",
         ok1 and rc2 == 3 and retirada(de(pers)) and ajena(pers), f"{rc} {e.get('estado')} {rc2}")
    # 12. (H-2) expediente trasladado después de publicar
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    nuevo_dir = os.path.join(os.path.dirname(os.path.dirname(d)), "exp_trasladado")
    shutil.move(os.path.dirname(d), nuevo_dir)
    dn = os.path.join(nuevo_dir, "Vidrala")
    marca(dn)
    rc, _ = run("informe.py", dn)
    reg = j(dn, REG) or {}
    paso("expediente trasladado o renombrado: sus publicaciones se adoptan y la invalidación directa retira la fila del CSV personalizado",
         rc == 3 and retirada(de(pers)) and ajena(pers) and any(x.get("trasladado_desde") for x in reg.get("publicaciones", [])), f"código {rc}")
    # 13. (H-3) resumen.py con las salidas archivadas y una retirada pendiente
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    copia = open(pers, encoding="utf-8").read()
    os.remove(pers)
    os.makedirs(pers)
    marca(d)
    run("informe.py", d)
    rc1, out1 = run("resumen.py", d, pred)
    shutil.rmtree(pers)
    open(pers, "w", encoding="utf-8").write(copia)
    rc2, _ = run("resumen.py", d, pred)
    paso("resumen.py con las salidas archivadas: código 5 mientras la retirada está pendiente; al recuperar el acceso la completa (código 3) sin publicar",
         rc1 == 5 and "RETIRADA PENDIENTE" in out1 and rc2 == 3 and retirada(de(pers)) and retirada(de(pred)) and not os.path.exists(os.path.join(d, "ficha.json")), f"{rc1} {rc2}")
    # 14. (H-8) registro ilegible: retirada pendiente, sin sobrescribirlo; registro borrado: se usa el respaldo
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    open(os.path.join(d, REG), "w").write("{ilegible")
    marca(d)
    rc, out = run("informe.py", d)
    paso("registro ilegible: código 5 con el motivo y el registro se conserva sin tocar", rc == 5 and "ilegible" in out and open(os.path.join(d, REG)).read() == "{ilegible", f"código {rc}")
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    if os.path.exists(os.path.join(d, REG)):
        os.remove(os.path.join(d, REG))
    marca(d)
    rc, _ = run("informe.py", d)
    paso("registro borrado: se recupera del respaldo y la invalidación directa retira la fila del CSV personalizado", rc == 3 and retirada(de(pers)) and ajena(pers), f"código {rc}")
    # 15. (auditoría de control, C-1a) copia de todo el árbol (expediente, configuración y su CSV) con el original vivo
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    base = os.path.dirname(os.path.dirname(d))
    base2 = base + "_copia_arbol"
    shutil.copytree(base, base2)
    d2, pers2, pred2 = d.replace(base, base2), pers.replace(base, base2), pred.replace(base, base2)
    marca(d2)
    rc, _ = run("informe.py", d2)
    paso("copia de todo el árbol con el original vivo: la invalidación directa de la copia retira la fila de SU CSV configurado y no toca las del original",
         rc == 3 and retirada(de(pers2)) and retirada(de(pred2)) and aprobada(de(pers)) and aprobada(de(pred)) and ajena(pers2), f"código {rc}")
    # 16. (C-1b) expediente renombrado y otro expediente nuevo en la ruta antigua
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    vieja = os.path.dirname(d)
    shutil.move(vieja, vieja + "_renombrado")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil"))  # expediente nuevo, sin registro, en la ruta antigua
    dr = os.path.join(vieja + "_renombrado", "Vidrala")
    marca(dr)
    rc, _ = run("informe.py", dr)
    paso("expediente renombrado con otro expediente en la ruta antigua: el renombrado adopta sus publicaciones y retira la fila del CSV configurado",
         rc == 3 and retirada(de(pers)) and ajena(pers), f"código {rc}")
    # 17. (C-2) traslado de todo el árbol: las rutas de los destinos se trasladan; sin código 5 permanente
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    base = os.path.dirname(os.path.dirname(d))
    shutil.move(base, base + "_trasladado")
    dt, perst, predt = d.replace(base, base + "_trasladado"), pers.replace(base, base + "_trasladado"), pred.replace(base, base + "_trasladado")
    marca(dt)
    rc, out = run("informe.py", dt)
    rc2, _ = run("pipeline.py", dt, "--config", conf.replace(base, base + "_trasladado"), "--desde", "14")
    paso("traslado de todo el árbol: la invalidación retira en los destinos trasladados (código 3, no 5) y el relanzamiento sigue con el rechazo (código 4)",
         rc == 3 and rc2 == 4 and retirada(de(perst)) and retirada(de(predt)) and ajena(perst), f"{rc} {rc2}")
    # 18. (C-3) registro ilegible: código 5, pero el destino conocido de la llamada se retira igualmente
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    open(os.path.join(d, REG), "w").write("{ilegible")
    marca(d)
    rc, _ = run("informe.py", d)
    paso("registro ilegible: código 5 y, aun así, se retiran el resumen predeterminado y los destinos del respaldo legible",
         rc == 5 and retirada(de(pred)) and retirada(de(pers)) and open(os.path.join(d, REG)).read() == "{ilegible", f"código {rc}")
    # 19. (C-2) salida humana para un destino que no volverá (registro humano SIMULADO en la prueba)
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    cart = os.path.dirname(pers)
    shutil.rmtree(cart)
    marca(d)
    rc1, _ = run("informe.py", d)
    reg = j(d, REG) or {}
    for e in reg.get("publicaciones", []):
        if e["csv"] == pers:
            e.update({"estado": "descartada", "descartado_por": "PRUEBA (registro humano simulado)", "fecha_descarte": "2026-11-09"})
    for nombre in (REG, ".publicaciones_resumen.respaldo.json"):
        if os.path.exists(os.path.join(d, nombre)) or nombre == REG:
            json.dump(reg, open(os.path.join(d, nombre), "w", encoding="utf-8"))
    rc2, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    rc3, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("destino que no volverá: código 5 hasta que la persona responsable lo descarta (descartado_por y fecha_descarte); después, el rechazo normal (código 4)",
         rc1 == 5 and rc2 == 4 and rc3 == 4, f"{rc1} {rc2} {rc3}")
    # 20. (auditoría final, F-1) solo el expediente se traslada a otro árbol donde existe, por casualidad, el CSV equivalente
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    otro_arbol = os.path.join(TMP, "otro_arbol_f1")
    os.makedirs(os.path.join(otro_arbol, "cfg", "cartera"))
    ajeno = os.path.join(otro_arbol, "cfg", "cartera", "resumen_global.csv")
    shutil.copy(pers, ajeno)  # un CSV ajeno con la misma estructura y una fila aprobada de la empresa
    dn = os.path.join(otro_arbol, "exp", "Vidrala")
    shutil.move(d, dn)
    marca(dn)
    rc, _ = run("informe.py", dn)
    paso("expediente trasladado a un árbol con un CSV equivalente ajeno: se retira el CSV realmente publicado y el ajeno no se toca",
         rc == 3 and retirada(de(pers)) and aprobada(de(ajeno)), f"código {rc}")
    # 21. (F-2) aprobación anterior a la 4.7 (sin registrar) en el resumen predeterminado e invalidación por el pipeline configurado
    d, conf, pers, pred = caso(exp)
    ok0 = aprobada(de(pred)) and not os.path.exists(os.path.join(d, REG))
    marca(d)
    rc, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    ok1 = retirada(de(pred))  # (vigencia, V-5) inmediatamente después del pipeline, antes de cualquier otra llamada
    rc2, _ = run("resumen.py", d, pred)
    paso("aprobación sin registrar en el resumen predeterminado: la invalidación por el pipeline configurado la retira por sí sola (código 4)", ok0 and rc == 4 and ok1, f"{rc}")
    paso("…y resumen.py sin ficha no la reaviva (código 3)", rc2 == 3 and retirada(de(pred)), f"{rc2}")
    # 21b. (V-2) una fila aprobada del predeterminado que no es de una ficha cerrada de este expediente (otra fecha) no se retira
    d, conf, pers, pred = caso(exp)
    filas_p = list(csv.DictReader(open(pred, encoding="utf-8")))
    cols = list(filas_p[0].keys())
    for r in filas_p:
        if r["empresa"] == EMP:
            r["fecha"] = "2099-01-01"  # fila de otro expediente de la misma empresa
    with open(pred, "w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        w.writerows(filas_p)
    marca(d)
    rc, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("fila aprobada del predeterminado que no corresponde a una ficha cerrada de este expediente: no se retira (no es su publicación)", rc == 4 and aprobada(de(pred)), f"{rc}")
    # 22. (F-3) descarte incompleto (sin descartado_por): sigue bloqueando con código 5
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    shutil.rmtree(os.path.dirname(pers))
    marca(d)
    run("informe.py", d)
    reg = j(d, REG) or {}
    for e in reg.get("publicaciones", []):
        if e["csv"] == pers:
            e.update({"estado": "descartada", "fecha_descarte": "2026-11-09"})  # sin descartado_por (registro humano simulado e incompleto)
    for nombre in (REG, ".publicaciones_resumen.respaldo.json"):
        json.dump(reg, open(os.path.join(d, nombre), "w", encoding="utf-8"))
    rc, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("descarte incompleto (falta descartado_por): sigue como retirada pendiente y el pipeline termina con código 5", rc == 5, f"código {rc}")
    # 23. (4.7.1, W-1 de la revisión independiente) resumen.py con una ficha cerrada no vigente hacia OTRO destino: en la misma
    # llamada se retira también la aprobación sin registrar del resumen predeterminado; filas ajenas y reintentos estables
    def con_ajena(p):
        rows = filas(p, None)
        cols = list(csv.DictReader(open(p, encoding="utf-8")).fieldnames)
        rows.append({k: "" for k in cols} | {"empresa": "Otra empresa (ajena)", "estado_analisis": "concluido", "verificacion": "APROBADO", "precio_si": "10"})
        with open(p, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    def cerrado(d, n_arch):
        """Salidas oficiales archivadas (una carpeta más en historial_cierres) y estado del pipeline sin cierre ni aprobación, con el archivo registrado."""
        st = j(d, "estado_pipeline.json") or {}
        dirs = os.listdir(os.path.join(d, "historial_cierres")) if os.path.isdir(os.path.join(d, "historial_cierres")) else []
        return (not any(os.path.exists(os.path.join(d, f)) for f in ("ficha.json", "informe.md", "cierre_vigente.json")) and len(dirs) == n_arch + 1
                and st.get("estado_analisis") is None and st.get("auditoria") is None and (st.get("paso") or 0) <= 13 and len(st.get("cierres_archivados") or []) == len(dirs))
    d, conf, pers, pred = caso(exp)
    con_ajena(pred)
    mat = (j(d, "cierre_vigente.json") or {}).get("material_auditado")
    n_hist = len(hist(pred))
    n_arch = len(os.listdir(os.path.join(d, "historial_cierres")))
    otro = os.path.join(os.path.dirname(os.path.dirname(d)), "otro_destino.csv")
    marca(d)
    rc, _ = run("resumen.py", d, otro)
    e_pred = next((x for x in (j(d, REG) or {}).get("publicaciones", []) if x["csv"] == pred), {})
    ok_inmediato = (rc == 3 and retirada(de(pred)) and ajena(pred) and len(hist(pred)) == n_hist + 1 and hist(pred)[-1]["verificacion"] == "APROBADO"
                    and cerrado(d, n_arch) and not any(aprobada([r]) for r in de(otro)) and not hist(otro)
                    and e_pred.get("estado") == "retirada" and mat and e_pred.get("material_auditado") == mat and hist(pred)[-1].get("material_auditado") == mat
                    and mat in de(pred)[0]["verificacion"])
    rc2, _ = run("resumen.py", d, otro)
    paso("W-1: resumen.py con ficha invalidada hacia otro destino retira en esa misma llamada la aprobación sin registrar del predeterminado: las dos filas, los dos historiales, "
         "las salidas archivadas, el estado del pipeline y el registro (con el material de la ficha archivada) comprobados de inmediato; el reintento no cambia nada",
         ok_inmediato and rc2 == 3 and retirada(de(pred)) and ajena(pred) and len(hist(pred)) == n_hist + 1 and not hist(otro), f"{rc} {rc2} · hist {n_hist}→{len(hist(pred))} · {e_pred.get('estado')}")
    # 24. (W-1) el mismo caso con OTRO destino que también lleva la fila aprobada (sin registrar) y una fila ajena
    d, conf, pers, pred = caso(exp)
    otro = os.path.join(os.path.dirname(os.path.dirname(d)), "otro_destino.csv")
    shutil.copy(pred, otro)
    con_ajena(otro)
    n_hist, n_arch = len(hist(pred)), len(os.listdir(os.path.join(d, "historial_cierres")))
    marca(d)
    rc, _ = run("resumen.py", d, otro)
    ok1 = (rc == 3 and retirada(de(pred)) and retirada(de(otro)) and ajena(otro) and len(hist(pred)) == n_hist + 1 and len(hist(otro)) == 1
           and hist(otro)[0]["verificacion"] == "APROBADO" and cerrado(d, n_arch))
    rc2, _ = run("resumen.py", d, otro)
    paso("W-1: con el otro destino también aprobado, la misma llamada retira las dos filas, con los dos historiales, las salidas archivadas y el estado del pipeline; "
         "fila ajena conservada; el reintento no duplica nada",
         ok1 and rc2 == 3 and retirada(de(pred)) and retirada(de(otro)) and len(hist(pred)) == n_hist + 1 and len(hist(otro)) == 1 and ajena(otro), f"{rc} {rc2}")
    # 25. (W-1, ruta análoga) ficha.py sustituye una ficha cerrada vigente: en la misma llamada se retira la fila que publicó la
    # anterior en el resumen predeterminado (sin registrar) aunque el resumen de la llamada sea el configurado
    d, conf, pers, pred = caso(exp)
    dv = j(d, "datos_v63.json")
    dv.setdefault("control_maestro", {}).setdefault("cabecera", {})["H4_moneda"] = "EUR (prueba 4.7.1)"  # entrada de la ficha fuera del material auditado
    json.dump(dv, open(os.path.join(d, "datos_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    n_hist = len(hist(pred))
    n_arch = len(os.listdir(os.path.join(d, "historial_cierres")))
    rc, out = run("ficha.py", d, "--estado", "concluido", "--config", conf)
    ok1 = (rc == 0 and "AVISO" in out and "NO es vigente" in out and retirada(de(pred)) and ajena(pers) and len(hist(pred)) == n_hist + 1 and hist(pred)[-1]["verificacion"] == "APROBADO"
           and len(os.listdir(os.path.join(d, "historial_cierres"))) == n_arch + 1 and (j(d, "estado_pipeline.json") or {}).get("auditoria") is None)
    # la sustitución archiva la aprobación (4.6.1): la ficha nueva no es vigente hasta una auditoría nueva; las llamadas siguientes
    # no publican nada ni duplican el historial
    rc2, _ = run("ficha.py", d, "--estado", "concluido", "--config", conf)
    rc3, _ = run("resumen.py", d, pred)
    paso("W-1 (ficha.py): al sustituir una ficha cerrada, la misma llamada retira la fila de la anterior en el resumen predeterminado sin registrar, aunque el de la llamada sea el configurado; las llamadas siguientes no publican ni duplican el historial",
         ok1 and rc2 == 3 and rc3 == 3 and retirada(de(pred)) and len(hist(pred)) == n_hist + 1 and ajena(pers), f"{rc} {rc2} {rc3}")
    # 26. (4.7.1, W-a de la auditoría interna) filas que no son byte a byte las de la ficha: el CSV guardado por una hoja de cálculo
    # (números y fecha reescritos) o una ficha editada tras el cierre. Se detectan por empresa y fecha, como en la 4.7
    def reformatear(p, **cambios):
        rows = filas(p, None)
        cols = list(csv.DictReader(open(p, encoding="utf-8")).fieldnames)
        for r in rows:
            if r["empresa"] == EMP:
                r.update(cambios)
        with open(p, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(rows)
    HOJA = {"precio": "87.90", "precio_si": "65.6880873204157", "ponderado": "70.4951544152", "fecha": "11/03/26"}  # como lo reescribe una hoja de cálculo
    d, conf, pers, pred = caso(exp)
    reformatear(pred, **HOJA)
    con_ajena(pred)
    n_hist = len(hist(pred))
    otro = os.path.join(os.path.dirname(os.path.dirname(d)), "otro_destino.csv")
    marca(d)
    rc, _ = run("resumen.py", d, otro)
    paso("W-a: fila del predeterminado reescrita por una hoja de cálculo (87.90, 65.6880873204157, 11/03/26): la ruta de W-1 la retira en la misma llamada",
         rc == 3 and retirada(de(pred)) and ajena(pred) and len(hist(pred)) == n_hist + 1, f"código {rc}")
    d, conf, pers, pred = caso(exp)
    shutil.rmtree(os.path.join(d, "historial_cierres"))  # expediente sin ninguna ficha archivada antes
    fj = j(d, "ficha.json")
    fj["precio"] = 99.9  # ficha editada a mano después del cierre
    json.dump(fj, open(os.path.join(d, "ficha.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, _ = run("resumen.py", d, otro)
    paso("W-a: ficha.json editada tras el cierre (precio 99,9) en un expediente sin fichas archivadas: la ruta de W-1 retira la fila publicada del predeterminado",
         rc == 3 and retirada(de(pred)), f"código {rc}")
    # 27. (W-a) resumen.py sin ficha, con el destino recibido aprobado y reescrito por una hoja de cálculo
    d, conf, pers, pred = caso(exp)
    x = os.path.join(os.path.dirname(os.path.dirname(d)), "destino_x.csv")
    shutil.copy(pred, x)
    reformatear(x, **HOJA)
    con_ajena(x)
    marca(d)
    run("informe.py", d)
    rc, _ = run("resumen.py", d, x)
    paso("W-a: resumen.py sin ficha retira la aprobación del destino recibido aunque la fila esté reescrita; fila ajena conservada", rc == 3 and retirada(de(x)) and ajena(x), f"código {rc}")
    # 28. (W-a, F-2) pipeline con resumen configurado y la fila sin registrar del predeterminado reescrita
    d, conf, pers, pred = caso(exp)
    reformatear(pred, **HOJA)
    marca(d)
    rc, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("W-a: con la fila reescrita, la invalidación por el pipeline configurado la retira por sí sola (código 4)", rc == 4 and retirada(de(pred)), f"código {rc}")
    # 29. (W-a, conservación) la fila de la ficha oficial VIGENTE se conserva aunque esté reescrita, con resumen.py, informe.py y el pipeline
    d, conf, pers, pred = caso(exp)
    reformatear(pred, **HOJA)
    antes = open(pred, encoding="utf-8").read()
    n_hist = len(hist(pred))
    r1, _ = run("resumen.py", d, otro)
    r2, _ = run("informe.py", d)
    r3, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("W-a: la fila sin registrar de la ficha vigente, reescrita por una hoja de cálculo, se conserva (resumen.py hacia otro destino, informe.py y pipeline con código 0)",
         r1 == r2 == r3 == 0 and open(pred, encoding="utf-8").read() == antes and len(hist(pred)) == n_hist and aprobada(de(otro)) and aprobada(de(pers)), f"{r1} {r2} {r3}")
    # 30. (W-b) registro ilegible en la ruta de W-1: código 5 y, aun así, se retira el predeterminado
    d, conf, pers, pred = caso(exp)
    open(os.path.join(d, REG), "w").write("{ilegible")
    marca(d)
    rc, out = run("resumen.py", d, otro)
    paso("W-b: con el registro ilegible, la ruta de W-1 termina con código 5 y retira igualmente la aprobación sin registrar del predeterminado; el registro no se toca",
         rc == 5 and "ilegible" in out and retirada(de(pred)) and open(os.path.join(d, REG)).read() == "{ilegible", f"código {rc}")
    # 31. (W-f) un destino registrado como «retirada» cuya fila aprobada reaparece (copia de seguridad restaurada) se vuelve a retirar
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    copia_pred = open(pred, encoding="utf-8").read()
    marca(d)
    run("informe.py", d)
    ya = any(e["csv"] == pred and e["estado"] == "retirada" for e in (j(d, REG) or {}).get("publicaciones", []))
    open(pred, "w", encoding="utf-8").write(copia_pred)
    ok0 = aprobada(de(pred))
    rc, _ = run("resumen.py", d, otro)
    paso("W-f: la fila aprobada que reaparece en un destino ya registrado como «retirada» se vuelve a retirar (resumen.py sin ficha, código 3)",
         ya and ok0 and rc == 3 and retirada(de(pred)), f"{ya} {ok0} {rc}")
    # 32. (W-e) sustitución de la ficha cerrada DENTRO del pipeline (entrada de la ficha fuera del material, --desde 14): el pipeline no
    # sobrescribe el archivo que hacen los generadores ni declara completado un cierre que ya no existe
    d, conf, pers, pred = caso(exp)
    run("pipeline.py", d, "--config", conf, "--desde", "14")
    ok0 = aprobada(de(pers))
    n_arch = len(os.listdir(os.path.join(d, "historial_cierres")))
    dv = j(d, "datos_v63.json")
    dv.setdefault("control_maestro", {}).setdefault("cabecera", {})["H4_moneda"] = "EUR (prueba 4.7.1)"
    json.dump(dv, open(os.path.join(d, "datos_v63.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc, out = run("pipeline.py", d, "--config", conf, "--desde", "14")
    st = j(d, "estado_pipeline.json") or {}
    dirs = os.listdir(os.path.join(d, "historial_cierres"))
    ok1 = (rc == 4 and "CIERRE RECHAZADO" in out and "FIN · estado concluido" not in out and not os.path.exists(os.path.join(d, "ficha.json")) and not os.path.exists(os.path.join(d, "informe.md"))
           and st.get("estado_analisis") is None and st.get("auditoria") is None and (st.get("paso") or 0) <= 13 and len(dirs) == n_arch + 2
           and len(st.get("cierres_archivados") or []) == len(dirs) and retirada(de(pers)) and retirada(de(pred)) and ajena(pers))
    rc2, _ = run("pipeline.py", d, "--config", conf, "--desde", "14")
    paso("W-e: la sustitución dentro del pipeline termina con código 4 (no «concluido»), sin salidas oficiales, con el estado sin aprobación y los dos archivos registrados; "
         "filas retiradas; el relanzamiento sigue rechazado y no publica",
         ok0 and ok1 and rc2 == 4 and retirada(de(pers)) and len(hist(pers)) == 1 and not os.path.exists(os.path.join(d, "ficha.json")), f"{rc} {rc2} · dirs {n_arch}→{len(dirs)} · {len(st.get('cierres_archivados') or [])}")
    # 9. estado temprano legítimo (sin auditoría) con resumen configurado
    c5 = TP.preparar("EmpresaX_temprana_47", quitar_precio=True)
    cfg = {k: v for k, v in config_v2.cargar(os.path.join(RAIZ, "config_v2.json")).items() if not k.startswith("_")}
    pers5 = os.path.join(TMP, "temprana", "resumen.csv")
    os.makedirs(os.path.dirname(pers5))
    cfg["resumen_csv"] = pers5
    conf5 = os.path.join(TMP, "temprana", "config.json")
    json.dump(cfg, open(conf5, "w", encoding="utf-8"))
    rc = subprocess.run([PY, "-B", TP.PIPE, c5, "--config", conf5], capture_output=True, text=True).returncode
    f5 = j(c5, "ficha.json") or {}
    r_res, _ = run("resumen.py", c5, pers5)
    paso("estado temprano sin auditoría (pendiente_de_datos) con resumen configurado: se publica como antes y no se registra como aprobación",
         rc == 0 and f5.get("estado_analisis") == "pendiente_de_datos" and r_res == 0 and any(r["estado_analisis"] == "pendiente_de_datos" for r in filas(pers5, None)) and not (j(c5, REG) or {}).get("publicaciones"))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--expediente", default=os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala"))
    a = ap.parse_args()
    try:
        main(os.path.abspath(a.expediente))
    except Exception as e:  # noqa
        import traceback
        traceback.print_exc()
        paso("excepción " + str(e)[:100], False)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    n = sum(ok for _, ok in R)
    print(f"\n{n}/{len(R)} pruebas de aceptación del resumen PASAN")
    sys.exit(0 if n == len(R) else 1)
