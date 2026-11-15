#!/usr/bin/env python3
"""Pruebas de aceptación de la reparación del cierre (entrega 4.6, encargo §3–§6). Trabaja solo en directorios temporales.

Uso: python3 -B pruebas/test_cierre_v2.py [--expediente <carpeta Vidrala del ensayo 4.5>]

4.6.1 · I1 vigencia: siete casos negativos (fase_c.json modificado y --desde 14; informe.py, ficha.py directos; rechazo seguido de
   informe.py; auditoría eliminada; REPETIR o mal formada con salidas anteriores; aprobación de otro material con fila previa) y cinco
   positivos (sin cambios, regeneración repetida, provisional auditable, auditoría nueva que cierra, estados tempranos), observando
   los archivos, el historial y el resumen después del rechazo.

I1 cierre: estado ANTES de la auditoría (sin ficha oficial; material provisional y fijado), REPETIR, auditoría mal formada,
   APROBADO válido (estado, ficha, informe y resumen coherentes), --desde 14 sin aprobación, aprobación de otra versión
   (material cambiado; id ajeno), ficha.py directo, y agotamiento de correcciones (no_entregable conservado).
I2 marca de etapa 1: dato necesario no material, evidencia pendiente con números completos (expediente real), entrada completa,
   ausencia solo no bloqueante, dato material (pendiente_de_datos, acción nula, diagnóstico) y regeneración tras resolverlo.
I3 correspondencia D10 ↔ C104: los cinco casos admitidos, no_procede para eludir una conclusión favorable, etiqueta contradictoria,
   etiqueta desconocida, combinación no permitida, y la fase C real con su etiqueta antigua y con la armonizada.
I4 alcance: secciones 1, 6 y 7 leídas por separado, ficha, valores sin cambios, regeneración sin duplicados y expediente ordinario
   sin aviso inventado.
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

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
SCR = os.path.join(RAIZ, "scripts")
sys.path.insert(0, AQUI)
sys.path.insert(0, SCR)
sys.dont_write_bytecode = True
import agentes_sinteticos as AG  # noqa: E402
import test_pipeline_sintetico as TP  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import config_v2  # noqa: E402
import pipeline  # noqa: E402

PY = sys.executable
TMP = tempfile.mkdtemp(prefix="cierre46_")
TP.BASE = TMP  # las empresas sintéticas se preparan en el temporal, nunca en pruebas/sintetico/
R = []


def paso(grupo, nombre, ok, detalle=""):
    R.append((grupo, nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + f" · {grupo} · {nombre}" + (f" · {detalle}" if detalle else ""))


def j(c, f):
    p = os.path.join(c, f)
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def corre(c, *extra):
    r = subprocess.run([PY, "-B", TP.PIPE, c, *extra], capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr).strip()


def hasta_auditoria(nombre, variante=None, **prep):
    """Empresa sintética llevada hasta que el pipeline pide la auditoría (paso 13)."""
    c = TP.preparar(nombre, **prep)
    reac = TP.reaccion_normal(variante)
    for _ in range(30):
        rc, out = corre(c)
        if rc != 10:
            return c, rc, out
        nombre_ag = open(os.path.join(c, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1]
        if nombre_ag == "verificacion":
            return c, rc, out
        reac(c, nombre_ag)
    return c, None, "demasiadas vueltas"


def copia(c, nombre):
    d = os.path.join(TMP, nombre, os.path.basename(c))
    shutil.copytree(c, d, ignore=shutil.ignore_patterns(".lo_perfil"))
    if os.path.exists(os.path.join(os.path.dirname(c), "resumen_v2.csv")):  # (4.6.1) con su resumen, para observar la fila activa
        shutil.copy(os.path.join(os.path.dirname(c), "resumen_v2.csv"), os.path.join(os.path.dirname(d), "resumen_v2.csv"))
    return d


def fila_activa(d):
    p = os.path.join(os.path.dirname(d), "resumen_v2.csv")
    filas = list(csv.DictReader(open(p, encoding="utf-8"))) if os.path.exists(p) else []
    return [r for r in filas if r.get("empresa") == "Empresa X (inventada)"], filas


def sin_vigencia_obsoleta(d, material_viejo):
    """(4.6.1) Tras un rechazo: ninguna salida oficial presenta la versión actual como cerrada; el cierre anterior está archivado con
    su retirada; la fila activa no dice concluido / APROBADO y la anterior se conserva en el historial del resumen."""
    fi, inf = j(d, "ficha.json"), os.path.join(d, "informe.md")
    hist = os.path.join(d, "historial_cierres")
    ret = [j(os.path.join(hist, x), "RETIRADA.json") for x in sorted(os.listdir(hist))] if os.path.isdir(hist) else []
    mias, _ = fila_activa(d)
    hcsv = os.path.join(os.path.dirname(d), "resumen_v2_historial.csv")
    hfilas = list(csv.DictReader(open(hcsv, encoding="utf-8"))) if os.path.exists(hcsv) else []
    st = j(d, "estado_pipeline.json")
    ok = (fi is None and not os.path.exists(inf) and not os.path.exists(os.path.join(d, "cierre_vigente.json"))
          and any(r and r.get("material_auditado_en_la_aprobacion") == material_viejo for r in ret)
          and len(mias) == 1 and mias[0]["verificacion"].startswith(CIE.NO_VIGENTE) and mias[0]["estado_analisis"] == ""
          and any(r.get("estado_analisis") == "concluido" and r.get("verificacion") == "APROBADO" and r.get("material_auditado") == material_viejo for r in hfilas)
          and st.get("estado_analisis") != "concluido" and os.path.exists(os.path.join(d, "auditoria.md")))
    det = f"ficha {None if fi is None else fi.get('estado_analisis')} · informe {os.path.exists(inf)} · archivos {[x for x in (os.listdir(hist) if os.path.isdir(hist) else [])]} · fila {[m['verificacion'][:40] for m in mias]} · historial {len(hfilas)}"
    return ok, det


def seccion(md, n):
    m = re.search(rf"^## {n}\..*?(?=^## \d+\.|\Z)", md, flags=re.M | re.S)
    return m.group(0) if m else ""


def i1():
    G = "I1 cierre"
    c, rc, out = hasta_auditoria("EmpresaX")
    st = j(c, "estado_pipeline.json")
    fp = j(c, "ficha_provisional.json") or {}
    fij = CIE.material_fijado(c) or {}
    prompt = open(os.path.join(c, "prompts_generados", "13_verificacion.md"), encoding="utf-8").read()
    paso(G, "antes de la auditoría: el pipeline espera al auditor en el paso 13", rc == 10 and st["paso"] == 13, out.splitlines()[-1] if out else "")
    paso(G, "antes de la auditoría: no existe ficha.json ni informe.md oficiales", not os.path.exists(os.path.join(c, "ficha.json")) and not os.path.exists(os.path.join(c, "informe.md")))
    paso(G, "antes de la auditoría: ficha_provisional.json con el estado propuesto y confirmado = false; informe_provisional.md marcado",
         (fp.get("provisional") or {}).get("confirmado") is False and (fp.get("provisional") or {}).get("estado_propuesto") == fp.get("estado_analisis")
         and "Material provisional para la auditoría" in open(os.path.join(c, "informe_provisional.md"), encoding="utf-8").read(), str(fp.get("provisional")))
    paso(G, "antes de la auditoría: material fijado (material_auditoria.json) con la ficha provisional y el libro evaluado, y su id en el prompt",
         fij.get("id") and "ficha_provisional.json" in fij["archivos"] and "EmpresaX_v63_evaluada.xlsx" in fij["archivos"] and f"Material auditado: {fij['id']}" in prompt and st.get("material_auditoria") == fij.get("id"))
    paso(G, "antes de la auditoría: la ficha provisional lleva la huella del libro evaluado auditado (regenerada después del paso 12)",
         (fp.get("hashes") or {}).get("libro_evaluado") == fij.get("archivos", {}).get("EmpresaX_v63_evaluada.xlsx"), str((fp.get("hashes") or {}).get("libro_evaluado"))[:12])
    rcx = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), c, "--estado", "concluido"], capture_output=True, text=True)
    paso(G, "llamada directa ficha.py --estado concluido sin auditoría: código 3 y ninguna ficha oficial", rcx.returncode == 3 and not os.path.exists(os.path.join(c, "ficha.json")), rcx.stdout.strip()[:140])

    # --desde 14 sin aprobación
    d = copia(c, "desde14")
    rc2, out2 = corre(d, "--desde", "14")
    st2 = j(d, "estado_pipeline.json")
    paso(G, "reanudación directa --desde 14 sin aprobación: rechazo explícito (código 4), sin ficha oficial y vuelta al paso 13",
         rc2 == 4 and "CIERRE RECHAZADO" in out2 and not os.path.exists(os.path.join(d, "ficha.json")) and st2["paso"] == 13 and st2.get("estado_analisis") is None, out2.splitlines()[-1] if out2 else "")

    # REPETIR: ningún cierre
    d = copia(c, "repetir")
    AG.auditoria(d, "REPETIR")
    rc3, out3 = corre(d)
    st3 = j(d, "estado_pipeline.json")
    paso(G, "auditoría REPETIR: ninguna confirmación de cierre (vuelve a la fase C; sin ficha oficial)",
         rc3 == 10 and st3["paso"] == 10 and st3.get("auditoria") == "REPETIR" and not os.path.exists(os.path.join(d, "ficha.json")), f"paso {st3['paso']} · {st3.get('esperando')}")

    # auditoría mal formada (falta el punto 16): REPETIR por la regla estricta de H2, ningún cierre
    d = copia(c, "malformada")
    AG.auditoria(d, "APROBADO")
    t = open(os.path.join(d, "auditoria.md"), encoding="utf-8").read()
    open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write("\n".join(l for l in t.splitlines() if not l.startswith("16.")))
    rc4, out4 = corre(d)
    st4 = j(d, "estado_pipeline.json")
    paso(G, "auditoría inválida (sin el punto 16): ningún cierre", rc4 == 10 and st4.get("auditoria") == "REPETIR" and not os.path.exists(os.path.join(d, "ficha.json")), f"auditoría {st4.get('auditoria')} · paso {st4['paso']}")

    # APROBADO de otra versión (id ajeno): se pide otra auditoría, ningún cierre
    d = copia(c, "id_ajeno")
    AG.auditoria(d, "APROBADO", material="0123456789abcdef")
    rc5, out5 = corre(d)
    st5 = j(d, "estado_pipeline.json")
    paso(G, "APROBADO que nombra otro material: se pide otra auditoría (paso 13), sin cierre", rc5 == 10 and st5["paso"] == 13 and st5.get("auditoria") is None
         and not os.path.exists(os.path.join(d, "ficha.json")) and "no corresponde al material" in " ".join(st5["historial"][-3:]), (st5.get("motivo_correccion") or "")[:120])
    # APROBADO sin línea de material
    d = copia(c, "sin_material")
    AG.auditoria(d, "APROBADO", material=False)
    rc6, out6 = corre(d)
    st6 = j(d, "estado_pipeline.json")
    paso(G, "APROBADO sin «Material auditado»: ningún cierre", rc6 == 10 and st6["paso"] == 13 and not os.path.exists(os.path.join(d, "ficha.json")))
    # material cambiado mientras se espera a la auditoría (aprobación de una versión anterior)
    d = copia(c, "cambiado")
    AG.auditoria(d, "APROBADO")  # nombra el material fijado…
    with open(os.path.join(d, "fase_c.md"), "a", encoding="utf-8") as fh:  # …pero un artefacto auditado cambia después
        fh.write("\nLínea añadida después de fijar el material.\n")
    rc7, out7 = corre(d)
    st7 = j(d, "estado_pipeline.json")
    paso(G, "aprobación de una versión anterior (fase_c.md cambió después de fijar el material): ningún cierre", rc7 == 10 and st7["paso"] == 13 and not os.path.exists(os.path.join(d, "ficha.json"))
         and "material cambió" in (st7.get("motivo_correccion") or ""), (st7.get("motivo_correccion") or "")[:120])

    # APROBADO válido y correspondiente: cierre coherente
    AG.auditoria(c, "APROBADO")
    rc8, out8 = corre(c)
    st8 = j(c, "estado_pipeline.json")
    fi = j(c, "ficha.json") or {}
    inf = open(os.path.join(c, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(c, "informe.md")) else ""
    filas = list(csv.DictReader(open(os.path.join(TMP, "resumen_v2.csv"), encoding="utf-8"))) if os.path.exists(os.path.join(TMP, "resumen_v2.csv")) else []
    fila = next((r for r in filas if r.get("empresa") == fi.get("empresa")), {})
    est = st8.get("estado_analisis")
    paso(G, "APROBADO válido: cierre coherente en estado, ficha, informe y resumen",
         rc8 == 0 and st8["paso"] == 14 and st8.get("auditoria") == "APROBADO" and fi.get("estado_analisis") == est and (fi.get("cierre") or {}).get("material_auditado") == st8.get("material_auditoria")
         and "provisional" not in fi and f"Estado `{est}`" in inf and "Material provisional" not in inf and fila.get("estado_analisis") == est and fila.get("verificacion") == "APROBADO",
         f"estado {est} · ficha {fi.get('estado_analisis')} · resumen {fila.get('estado_analisis')}/{fila.get('verificacion')}")
    # tras el cierre, un artefacto cambia y se intenta reanudar en 14 con la aprobación anterior
    d = copia(c, "post_cierre")
    with open(os.path.join(d, "fase_c.md"), "a", encoding="utf-8") as fh:
        fh.write("\nCambio posterior al cierre.\n")
    rc9, out9 = corre(d, "--desde", "14")
    ok9, det9 = sin_vigencia_obsoleta(d, j(c, "material_auditoria.json")["id"])
    paso(G, "aprobación anterior con material cambiado y --desde 14: rechazo (código 4) y, después, ninguna salida ni fila vigente obsoleta", rc9 == 4 and "material cambió" in out9 and ok9, det9)
    rcd = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--estado", "concluido"], capture_output=True, text=True)
    paso(G, "ficha.py directo con la aprobación de otra versión: código 3", rcd.returncode == 3, rcd.stdout.strip()[:120])

    # agotamiento de correcciones: no_entregable conservado
    c2, rc10, out10 = hasta_auditoria("EmpresaY")
    for _ in range(12):
        nombre_ag = open(os.path.join(c2, "ESPERANDO.md"), encoding="utf-8").read().split("**")[1] if os.path.exists(os.path.join(c2, "ESPERANDO.md")) else None
        if nombre_ag == "verificacion":
            AG.auditoria(c2, "REPETIR")
        elif nombre_ag:
            TP.reaccion_normal()(c2, nombre_ag)
        rc10, out10 = corre(c2)
        if rc10 != 10:
            break
    st10 = j(c2, "estado_pipeline.json")
    fi10 = j(c2, "ficha.json") or {}
    paso(G, "agotamiento de correcciones de la auditoría: no_entregable conservado (ficha sin cubo ni acción)",
         rc10 == 0 and st10.get("estado_analisis") == "no_entregable" and fi10.get("estado_analisis") == "no_entregable" and fi10.get("cubo") is None and fi10.get("decision") is None,
         f"estado {st10.get('estado_analisis')} · intentos {st10['intentos']}")
    return c


def i2(c_sint, exp):
    G = "I2 marca de etapa 1"

    def regenera(d):
        subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--provisional"], capture_output=True, text=True)
        subprocess.run([PY, "-B", os.path.join(SCR, "informe.py"), d, "--provisional"], capture_output=True, text=True)
        return j(d, "ficha_provisional.json") or {}, open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read()

    def con_entrada(nombre, nec, nob):
        d = copia(c_sint, nombre)
        e = j(d, "entrada_v63.json")
        e["necesarios_para_listo_provisional"], e["no_bloqueantes"] = nec, nob
        json.dump(e, open(os.path.join(d, "entrada_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
        return d
    nec = [{"dato": "Análisis!C31", "que": "Recompras: dato de etapa 1 ausente", "origen_esperado": "fase1_v63.json"}]
    d = con_entrada("marca_nec", nec, [])
    f, md = regenera(d)
    m = f.get("datos_etapa1_incompletos") or {}
    paso(G, "dato necesario para LISTO · PROVISIONAL ausente y no material: marca presente con la causa exacta",
         m.get("marca") == CIE.MARCA_ETAPA1 and m.get("causas") == nec and CIE.MARCA_ETAPA1 in seccion(md, 1) and "Análisis!C31" in seccion(md, 1))
    dv = os.path.join(TMP, "vidrala_marca", "Vidrala")
    shutil.copytree(exp, dv, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    f, md = regenera(dv)
    nec_real = [x["dato"] for x in j(dv, "entrada_v63.json")["necesarios_para_listo_provisional"]]
    m = f.get("datos_etapa1_incompletos") or {}
    paso(G, "evidencia pendiente con números completos (ensayo real, 6 causas): marca presente con la lista exacta",
         len(nec_real) == 6 and m.get("causas") == j(dv, "entrada_v63.json")["necesarios_para_listo_provisional"] and all(x in seccion(md, 1) for x in nec_real), "; ".join(nec_real))
    d = con_entrada("marca_completa", [], [])
    f, md = regenera(d)
    paso(G, "entrada completa: marca ausente", f.get("datos_etapa1_incompletos") is None and CIE.MARCA_ETAPA1 not in md)
    d = con_entrada("marca_otro_nivel", [], [{"dato": "Palancas!C24", "que": "tamaño del mercado", "origen_esperado": "extractos"}])
    f, md = regenera(d)
    paso(G, "ausencia solo de otro nivel (no bloqueante): la marca no se activa", f.get("datos_etapa1_incompletos") is None and CIE.MARCA_ETAPA1 not in md)
    d = con_entrada("marca_resuelta", nec, [])
    regenera(d)
    e = j(d, "entrada_v63.json")
    e["necesarios_para_listo_provisional"] = []
    json.dump(e, open(os.path.join(d, "entrada_v63.json"), "w", encoding="utf-8"), ensure_ascii=False)
    f, md = regenera(d)
    paso(G, "regeneración después de resolver la carencia: desaparece la marca obsoleta", f.get("datos_etapa1_incompletos") is None and CIE.MARCA_ETAPA1 not in md)
    # dato material: pendiente_de_datos, acción nula y diagnóstico (recorrido completo con la variante de S-19)
    c3, rc, out = hasta_auditoria("EmpresaZ_sin_C34", "datos_ausentes", quitar_fase1=("C34",), quitar_etapa1=("C34",), precio=16)  # como t_datos_ausentes
    AG.auditoria(c3, "APROBADO")
    rc, out = corre(c3)
    st = j(c3, "estado_pipeline.json")
    fi = j(c3, "ficha.json") or {}
    marca_ok = (fi.get("datos_etapa1_incompletos") is not None) == bool(j(c3, "entrada_v63.json")["necesarios_para_listo_provisional"])
    paso(G, "dato material: se mantiene pendiente_de_datos, acción nula y diagnóstico; la marca sigue a su disparador",
         rc == 0 and st.get("estado_analisis") == "pendiente_de_datos" and (fi.get("decision") or {}).get("accion") is None and os.path.exists(os.path.join(c3, "diagnostico.json")) and marca_ok,
         f"estado {st.get('estado_analisis')} · acción {(fi.get('decision') or {}).get('accion')} · marca {fi.get('datos_etapa1_incompletos') is not None}")


def i3(exp):
    G = "I3 D10 ↔ C104"
    casos_ok = [("concluido", "comprar", "sin_limitacion", "lista vacía"), ("concluido", "comprar", "comprobacion_conjunta_superada", "comprobación conjunta superada"),
                ("pendiente_de_investigacion", None, "pendiente_de_investigacion", "pendiente de investigación"), ("pendiente_de_datos", None, "no_procede", "pendiente de datos"),
                ("concluido", "esperar", "no_procede", "no procede (conclusión no favorable)")]
    for est, acc, res, et in casos_ok:
        c104 = f"Pendiente de decisión de cartera · conclusión del personaje: x · zona caro · precio de Sí ≤ 1 · precio esc. MALO 1 · ponderado 1 · fundamento {et}"
        paso(G, f"admitido: {est} · {acc} · {res} → «fundamento {et}»", CIE.motivo_c104_fundamento(est, acc, res, c104) is None)
    base = "Pendiente de decisión de cartera · conclusión del personaje: x · zona caro · precio de Sí ≤ 1 · precio esc. MALO 1 · ponderado 1 · fundamento "
    paso(G, "rechazado: no_procede para eludir los requisitos de una conclusión favorable (comprar)", CIE.motivo_c104_fundamento("concluido", "comprar", "no_procede", base + "no procede (conclusión no favorable)") is not None)
    paso(G, "rechazado: etiqueta contradictoria con el JSON (esperar + no_procede con «lista vacía»)", CIE.motivo_c104_fundamento("concluido", "esperar", "no_procede", base + "lista vacía") is not None)
    paso(G, "rechazado: etiqueta desconocida", CIE.motivo_c104_fundamento("concluido", "esperar", "no_procede", base + "no procede (conclusión no favorable; nota libre)") is not None
         and CIE.motivo_c104_fundamento("concluido", "esperar", "no_procede", base + "XYZ") is not None)
    paso(G, "rechazado: combinación de estado y acción no permitida", CIE.motivo_c104_fundamento("pendiente_de_investigacion", "esperar", "pendiente_de_investigacion", base + "pendiente de investigación") is not None
         and CIE.motivo_c104_fundamento("concluido", None, "no_procede", base + "no procede (conclusión no favorable)") is not None
         and CIE.motivo_c104_fundamento("concluido", "esperar", "sin_limitacion", base + "lista vacía") is not None)
    # fase C real del ensayo 4.5 a través de coherencia_fase_c (sin exigir comprobación conjunta para una conclusión no favorable)
    d = os.path.join(TMP, "vidrala_c104", "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    P = pipeline.Pipeline(d, config_v2.cargar(os.path.join(RAIZ, "config_v2.json")))
    fc = j(d, "fase_c.json")
    r_antigua = P.coherencia_fase_c(fc)
    fc2 = json.loads(json.dumps(fc))
    fc2["celdas"]["C104"] = re.sub(r"fundamento no procede \([^)]*\)", "fundamento no procede (conclusión no favorable)", fc["celdas"]["C104"])
    r_nueva = P.coherencia_fase_c(fc2)
    paso(G, "fase C real 4.5: la etiqueta libre «no procede (…; hipótesis Palancas C8 acotada)» se rechaza; la armonizada se admite sin comprobación conjunta",
         r_antigua is not None and r_nueva is None and not os.path.exists(os.path.join(d, "comprobacion_conjunta.json")), f"antigua: {r_antigua!r} · armonizada: {r_nueva!r}")


def i4(c_sint, exp):
    G = "I4 alcance"
    d = os.path.join(TMP, "vidrala_alcance", "Vidrala")
    shutil.copytree(exp, d, ignore=shutil.ignore_patterns(".lo_perfil", "recalc"))
    aviso = "Resultados mecánicos de prueba (texto del metadato de la prueba)."
    json.dump({"tipo": "ensayo_exploratorio", "aviso": aviso, "fuente": "prueba de aceptación"}, open(os.path.join(d, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False)
    for _ in range(2):  # dos regeneraciones: sin duplicados
        subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--provisional"], capture_output=True, text=True)
        subprocess.run([PY, "-B", os.path.join(SCR, "informe.py"), d, "--provisional"], capture_output=True, text=True)
    md = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read()
    s1, s6, s7 = seccion(md, 1), seccion(md, 6), seccion(md, 7)
    paso(G, "sección 1 (conclusión o acción mecánica), leída por separado, con el aviso", s1.count(aviso) == 1)
    paso(G, "sección 6 (DCF inverso), leída por separado, con el aviso", s6.count(aviso) == 1 and "DCF inverso" in s6)
    paso(G, "sección 7 (escalera, precio de Sí y zona), leída por separado, con el aviso", s7.count(aviso) == 1 and "precio de Sí" in s7 and "Zona" in s7)
    paso(G, "regeneración: ningún aviso duplicado (3 apariciones, una por sección pertinente)", md.count(aviso) == 3)
    f = j(d, "ficha_provisional.json")
    f45 = j(exp, "ficha.json")
    paso(G, "la ficha conserva el alcance y las notas de la fase C (condición e insumos)", (f.get("alcance") or {}).get("aviso") == aviso and (f.get("decision") or {}).get("condicion") == (f45.get("decision") or {}).get("condicion")
         and (f.get("insumos_decision_cartera") or {}) == (f45.get("insumos_decision_cartera") or {}))
    num = ("escalera", "valor_ponderado", "precio", "escenarios", "peso_terminal", "salto_anio_11", "motor")
    paso(G, "los valores financieros permanecen iguales a los de la ficha 4.5", all(f.get(k) == f45.get(k) for k in num), ", ".join(k for k in num if f.get(k) != f45.get(k)) or "iguales")
    os.remove(os.path.join(d, "alcance_v2.json"))
    subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--provisional"], capture_output=True, text=True)
    subprocess.run([PY, "-B", os.path.join(SCR, "informe.py"), d, "--provisional"], capture_output=True, text=True)
    md2 = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read()
    ds = copia(c_sint, "ordinario")
    subprocess.run([PY, "-B", os.path.join(SCR, "informe.py"), ds], capture_output=True, text=True)
    mds = open(os.path.join(ds, "informe.md"), encoding="utf-8").read()
    paso(G, "expediente ordinario (sin alcance_v2.json): ninguna advertencia exploratoria inventada", "Alcance del expediente" not in md2 and aviso not in md2 and "Alcance del expediente" not in mds and j(ds, "ficha.json").get("alcance") is None)
    json.dump({"tipo": "otro", "aviso": "", "fuente": ""}, open(os.path.join(d, "alcance_v2.json"), "w", encoding="utf-8"))
    r = subprocess.run([PY, "-B", os.path.join(SCR, "ficha.py"), d, "--provisional"], capture_output=True, text=True)
    paso(G, "alcance_v2.json mal formado: ficha.py se detiene (código 1)", r.returncode == 1, r.stdout.strip()[:100])


def i1_vigencia(c):
    """(4.6.1) Vigencia de las salidas oficiales: siete casos negativos y cinco positivos sobre copias del expediente sintético cerrado."""
    G = "I1 vigencia"
    mat = j(c, "material_auditoria.json")["id"]
    # la empresa sintética del agotamiento (EmpresaY) comparte nombre y sustituyó la fila del resumen común: se restituye la de c
    subprocess.run([PY, "-B", os.path.join(SCR, "resumen.py"), c, os.path.join(os.path.dirname(c), "resumen_v2.csv")], capture_output=True, text=True)
    aud_sha = hashlib.sha256(open(os.path.join(c, "auditoria.md"), "rb").read()).hexdigest()

    def modifica_b101(d):
        fc = j(d, "fase_c.json")
        fc["celdas"]["B101"] = fc["celdas"]["B101"] + " TESIS DE PRUEBA POSTERIOR"
        json.dump(fc, open(os.path.join(d, "fase_c.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def gen(script, d, *x):
        return subprocess.run([PY, "-B", os.path.join(SCR, script), d, *x], capture_output=True, text=True)

    # foránea: una fila de otra empresa en el resumen de cada copia, que no se toca
    def con_ajena(d):
        p = os.path.join(os.path.dirname(d), "resumen_v2.csv")
        filas = list(csv.DictReader(open(p, encoding="utf-8")))
        cols = list(filas[0].keys())
        filas.append({k: "" for k in cols} | {"empresa": "Otra empresa (ajena)", "estado_analisis": "concluido", "verificacion": "APROBADO"})
        with open(p, "w", encoding="utf-8", newline="") as fh:
            w = csv.DictWriter(fh, fieldnames=cols)
            w.writeheader()
            w.writerows(filas)

    def ajena_intacta(d):
        _, filas = fila_activa(d)
        return any(r["empresa"] == "Otra empresa (ajena)" and r["estado_analisis"] == "concluido" and r["verificacion"] == "APROBADO" for r in filas)

    # 1. fase_c.json modificado → --desde 14
    d = copia(c, "v1"); con_ajena(d); modifica_b101(d)
    rc, out = corre(d, "--desde", "14")
    ok, det = sin_vigencia_obsoleta(d, mat)
    paso(G, "N1 fase_c.json modificado → --desde 14: código 4; ficha, informe y fila activa ya no presentan concluido / APROBADO; cierre archivado; fila ajena intacta",
         rc == 4 and ok and ajena_intacta(d), det)
    # 4. rechazo del pipeline → informe.py directo
    r = gen("informe.py", d)
    paso(G, "N4 tras el rechazo, informe.py directo: código 3 y ningún informe oficial con el contenido nuevo", r.returncode == 3 and not os.path.exists(os.path.join(d, "informe.md")), r.stdout.strip()[:120])
    # P3/P4. el material provisional sigue auditable y una auditoría nueva del material modificado cierra de forma coherente
    rc, out = corre(d)
    fij = CIE.material_fijado(d) or {}
    paso(G, "P3 material modificado: el pipeline prepara material provisional nuevo y espera una auditoría nueva (paso 13)",
         rc == 10 and j(d, "estado_pipeline.json")["paso"] == 13 and fij.get("id") not in (None, mat) and (j(d, "ficha_provisional.json") or {}).get("provisional", {}).get("confirmado") is False, f"material {fij.get('id')}")
    AG.auditoria(d, "APROBADO")
    rc, out = corre(d)
    fi = j(d, "ficha.json") or {}
    mias, _ = fila_activa(d)
    inf = open(os.path.join(d, "informe.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "informe.md")) else ""
    paso(G, "P4 auditoría nueva del material modificado: cierre oficial coherente (ficha, informe con la tesis nueva, fila activa y cierre registrado); el cierre anterior sigue en el historial",
         rc == 0 and fi.get("estado_analisis") == "concluido" and (fi.get("cierre") or {}).get("material_auditado") == fij.get("id") and "TESIS DE PRUEBA POSTERIOR" in inf
         and len(mias) == 1 and mias[0]["verificacion"] == "APROBADO" and (j(d, "cierre_vigente.json") or {}).get("material_auditado") == fij.get("id")
         and os.path.isdir(os.path.join(d, "historial_cierres")) and ajena_intacta(d), f"fila {[m['verificacion'] for m in mias]}")
    # 2. modificado → informe.py directo, sin pasar por el pipeline
    d = copia(c, "v2"); modifica_b101(d)
    r = gen("informe.py", d)
    ok, det = sin_vigencia_obsoleta(d, mat)
    paso(G, "N2 modificado → informe.py directo: código 3, no publica la tesis nueva; salidas anteriores archivadas y fila no vigente", r.returncode == 3 and ok, det)
    # 3. modificado → ficha.py directo
    d = copia(c, "v3"); modifica_b101(d)
    r = gen("ficha.py", d, "--estado", "concluido")
    ok, det = sin_vigencia_obsoleta(d, mat)
    paso(G, "N3 modificado → ficha.py directo: código 3 y la ficha oficial anterior no queda como aprobación vigente", r.returncode == 3 and ok, det)
    # 5. auditoría eliminada después del cierre
    d = copia(c, "v5"); os.remove(os.path.join(d, "auditoria.md"))
    r = gen("informe.py", d)
    fi = j(d, "ficha.json")
    mias, _ = fila_activa(d)
    paso(G, "N5 auditoría eliminada tras el cierre → informe.py: código 3; salidas archivadas y fila no vigente", r.returncode == 3 and fi is None and not os.path.exists(os.path.join(d, "informe.md"))
         and mias and mias[0]["verificacion"].startswith(CIE.NO_VIGENTE), r.stdout.strip()[:120])
    rc, out = corre(d, "--desde", "14")
    paso(G, "N5 auditoría eliminada → --desde 14: código 4 sin salidas oficiales", rc == 4 and j(d, "ficha.json") is None)
    # 6. auditoría REPETIR o mal formada con salidas oficiales anteriores presentes
    for nombre, prepara in (("REPETIR", lambda d: AG.auditoria(d, "REPETIR", material=mat)),
                            ("mal formada", lambda d: open(os.path.join(d, "auditoria.md"), "w", encoding="utf-8").write("1. PASA · solo un punto\nMaterial auditado: " + mat + "\nVeredicto: APROBADO\n"))):
        d = copia(c, "v6" + nombre.replace(" ", "_"))
        prepara(d)
        rc, out = corre(d)
        ok, det = sin_vigencia_obsoleta(d, mat)
        paso(G, f"N6 auditoría {nombre} con salidas oficiales anteriores: archivadas al relanzar; ninguna salida ni fila vigente", ok, det)
    # 7. aprobación de otro material con fila previa concluido / APROBADO
    d = copia(c, "v7"); modifica_b101(d)
    AG.auditoria(d, "APROBADO", material="0123456789abcdef")
    rc, out = corre(d, "--desde", "13")
    ok, det = sin_vigencia_obsoleta(d, mat)
    st = j(d, "estado_pipeline.json")
    paso(G, "N7 aprobación de otro material con fila previa concluido / APROBADO: no cierra, archiva, fila no vigente, se pide otra auditoría",
         rc == 10 and st["paso"] == 13 and ok, det)
    # conservación: la auditoría que aprobó no se borra ni cambia; los datos no cambian
    d = copia(c, "v8"); modifica_b101(d)
    corre(d, "--desde", "14")
    hd = os.path.join(d, "historial_cierres")
    hist = os.path.join(hd, sorted(os.listdir(hd))[0]) if os.path.isdir(hd) and os.listdir(hd) else os.path.join(hd, "(sin archivo)")
    paso(G, "conservación: la auditoría aprobatoria sigue intacta (y copiada al archivo) y la retirada dice de qué material era",
         hashlib.sha256(open(os.path.join(d, "auditoria.md"), "rb").read()).hexdigest() == aud_sha and os.path.exists(os.path.join(hist, "auditoria_en_el_momento_de_la_retirada.md"))
         and (j(hist, "RETIRADA.json") or {}).get("material_auditado_en_la_aprobacion") == mat and f"Aprobación histórica del material {mat}, distinto del actual" in (j(hist, "RETIRADA.json") or {}).get("nota", "") and "copia en este archivo" in (j(hist, "RETIRADA.json") or {}).get("nota", "")
         and all(os.path.exists(os.path.join(hist, f)) for f in ("ficha.json", "informe.md", "cierre_vigente.json")))
    # positivos: sin cambios y aprobación vigente
    d = copia(c, "p1")
    sha_i, sha_f = (hashlib.sha256(open(os.path.join(d, f), "rb").read()).hexdigest() for f in ("informe.md", "ficha.json"))
    r1, r2, r3 = gen("informe.py", d), gen("ficha.py", d, "--estado", "concluido"), gen("resumen.py", d, os.path.join(os.path.dirname(d), "resumen_v2.csv"))
    rc, out = corre(d)
    mias, _ = fila_activa(d)
    paso(G, "P1 material sin cambios y aprobación vigente: informe.py, ficha.py y resumen.py regeneran oficialmente (código 0) y el pipeline no archiva nada",
         r1.returncode == r2.returncode == r3.returncode == 0 and rc == 0 and not os.path.isdir(os.path.join(d, "historial_cierres")) and len(mias) == 1 and mias[0]["verificacion"] == "APROBADO", f"{r1.returncode} {r2.returncode} {r3.returncode} {rc}")
    gen("informe.py", d); gen("ficha.py", d, "--estado", "concluido"); gen("resumen.py", d, os.path.join(os.path.dirname(d), "resumen_v2.csv"))
    mias, filas = fila_activa(d)
    paso(G, "P2 regeneración repetida: resultado estable (mismas huellas de ficha e informe) y sin duplicados en el resumen ni en el historial",
         hashlib.sha256(open(os.path.join(d, "informe.md"), "rb").read()).hexdigest() == sha_i and hashlib.sha256(open(os.path.join(d, "ficha.json"), "rb").read()).hexdigest() == sha_f
         and len(mias) == 1 and not os.path.isdir(os.path.join(d, "historial_cierres")))
    # P5. estados tempranos válidos (sin auditoría): pendiente_de_datos por falta de precio
    c5 = TP.preparar("EmpresaX_sin_precio_461", quitar_precio=True)
    rc, out = corre(c5)
    f5 = j(c5, "ficha.json") or {}
    r1, r2 = gen("informe.py", c5), gen("resumen.py", c5, os.path.join(os.path.dirname(c5), "resumen_v2.csv"))
    paso(G, "P5 estado temprano sin auditoría (pendiente_de_datos): se publica como antes; informe.py y resumen.py directos no lo bloquean",
         rc == 0 and f5.get("estado_analisis") == "pendiente_de_datos" and "cierre" not in f5 and r1.returncode == 0 and r2.returncode == 0 and not os.path.isdir(os.path.join(c5, "historial_cierres")),
         f"estado {f5.get('estado_analisis')} · {r1.returncode} {r2.returncode}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--expediente", default=os.path.join(RAIZ, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_5", "Vidrala"))
    a = ap.parse_args()
    exp = os.path.abspath(a.expediente)
    try:
        c = i1()
        i1_vigencia(c)
        i2(c, exp)
        i3(exp)
        i4(c, exp)
    except Exception as e:  # noqa
        import traceback
        traceback.print_exc()
        paso("excepción", str(e)[:120], False)
    finally:
        shutil.rmtree(TMP, ignore_errors=True)
    n = sum(ok for *_, ok in R)
    print(f"\n{n}/{len(R)} pruebas de aceptación del cierre PASAN")
    sys.exit(0 if n == len(R) else 1)
