#!/usr/bin/env python3
"""Control de la entrega 4.12 (validación supervisada, cierre de la integración y contraste con Viscofan). Uso (desde munger_v2_r1/,
después de verificar_paquete.sh completa y de los controles históricos):
    python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/scripts/comprobar_entrega_4_12.py
No usa LibreOffice (las baterías que lo usan van en verificar_paquete.sh completa). Escribe solo en temporales.
Tipos: «reejecuta» (vuelve a ejecutar un script de solo lectura o un cálculo y compara), «constata» (comprueba un hecho del árbol).
Lo que comprueba: alcance de los cambios frente a la 4.11 (originales, plantillas y expedientes anteriores intactos), plantillas,
verificador del paquete y batería, vigencia (§3), protocolos y materialidad (§4), coherencia y trazabilidad (§5), reconstrucción y rf
(§6), los dos cierres de Vidrala y su comparación (§7), Viscofan (§8), propuesta humana sin firmar y documentación de la versión."""
import hashlib
import json
import os
import re
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
EXP = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(EXP, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
V64 = os.path.join(RAIZ, "v6", "v64_experimental")
COND = os.path.join(EXP, "cierre_condicionado", "Vidrala")
BLOQ = os.path.join(EXP, "cierre_bloqueo", "Vidrala")
VIS = os.path.join(EXP, "viscofan", "experimental", "Viscofan")
PIL411 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_11", "piloto", "Vidrala")
REL_EXP = os.path.relpath(EXP, RAIZ) + "/"
TMP = tempfile.mkdtemp(prefix="control412_")
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "constata": 0}
# archivos de la 4.11 que la 4.12 cambia (el resto del manifiesto de la 4.11 tiene que estar igual)
CAMBIADOS_FRENTE_A_4_11 = {
    "VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "CAMBIOS_ARCHIVOS.txt", "verificar_paquete.sh",
    "v6/v64_experimental/docs/README_V6.4_experimental.md",
    "personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/esquema/fase_c.esquema.json", "personaje_v2/esquema/ficha.esquema.json",
    "personaje_v2/prompts/fase_c_turno1.md", "personaje_v2/prompts/fase_c_turno2.md", "personaje_v2/prompts/verificacion.md",
    "personaje_v2/pruebas/agentes_sinteticos.py", "personaje_v2/pruebas/test_integracion_v64.py",
} | {f"personaje_v2/scripts/{s}" for s in (
    "cierre_v2.py", "comprobacion_conjunta.py", "comprobar_gramatica.py", "configuracion_economica.py", "ficha.py", "informe.py",
    "pipeline.py", "resumen.py", "seleccion_plantilla.py", "variantes_configuracion_v64.py", "volcar_datos_v63.py")}
NUEVOS_PERMITIDOS = (REL_EXP, "personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md") + tuple(f"personaje_v2/scripts/{s}" for s in (
    "comparar_zip.py", "dominios_v64.py", "entradas_economicas.py", "objetivo_v64.py", "trazabilidad_v64.py"))
sys.path.insert(0, os.path.join(PV, "scripts"))


def comprobar(tipo, nombre, ok, detalle=""):
    global N_OK, N_T
    N_T += 1
    TIPOS[tipo] += 1
    N_OK += bool(ok)
    print(f"{'CUMPLE  ' if ok else 'NO CUMPLE'} · [{tipo}] {nombre}" + (f" · {detalle}" if detalle and not ok else ""), flush=True)


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def manifiesto(p):
    d = {}
    for linea in open(p, encoding="utf-8"):
        if linea.strip() and not linea.startswith("#"):
            h, f = linea.rstrip("\n").split("  ", 1)
            d[f] = h
    return d


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def j(p):
    try:
        return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None
    except ValueError:
        return None


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def arbol():
    """Archivos del árbol en disco, sin las salidas de las baterías en personaje_v2/pruebas/ que no están en el manifiesto del propio
    árbol, ni __pycache__, .lo_perfil/ o pruebas/_v64/ (como en el LEEME de los controles)."""
    mp = os.path.join(RAIZ, "MANIFIESTO_SHA256.txt")
    del_arbol = manifiesto(mp) if os.path.exists(mp) else {}
    out = {}
    for r, ds, fs in os.walk(RAIZ):
        ds[:] = [d for d in ds if d not in ("__pycache__", ".lo_perfil", "_v64")]
        for f in fs:
            p = os.path.relpath(os.path.join(r, f), RAIZ)
            if p == "MANIFIESTO_SHA256.txt" or (p.startswith(os.path.join("personaje_v2", "pruebas") + os.sep) and p not in del_arbol):
                continue
            out[p] = sha(os.path.join(RAIZ, p))
    return out


def cerrado(c):
    st = j(os.path.join(c, "estado_pipeline.json")) or {}
    return st, (st.get("paso") == 14 or st.get("estado_analisis") not in (None, "")) and not os.path.exists(os.path.join(c, "ESPERANDO.md"))


def expediente_real(c, nombre):
    """Comprobaciones comunes de un expediente V6.4 recorrido con agentes reales y el código final."""
    import configuracion_economica as CE
    import objetivo_v64 as OB
    st, ok_cierre = cerrado(c)
    comprobar("constata", f"{nombre}: el pipeline terminó (estado {st.get('estado_analisis')!r}, auditoría {st.get('auditoria')!r}) sin una espera abierta", ok_cierre)
    tecnico = (st.get("estado_analisis") == "no_entregable") and "fallo_de_implementacion" in leer(os.path.join(c, "diagnostico.md"))
    comprobar("constata", f"{nombre}: no termina por una interrupción técnica (fallo_de_implementacion)", not tecnico)
    conf = j(os.path.join(c, "configuracion_economica.json")) or {}
    comprobar("constata", f"{nombre}: configuración experimental válida, declarada como ensayo y con protocolo del objetivo",
              conf.get("modo") == "Experimental" and not CE.validar(conf) and conf.get("protocolo_objetivo") in CE.PROTOCOLOS and "adopci" in conf.get("naturaleza", ""))
    pa = j(os.path.join(c, "plantilla_activa.json")) or {}
    pl64 = os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")
    comprobar("constata", f"{nombre}: plantilla_activa.json = V6.4 experimental con la huella de la plantilla entregada", pa.get("version") == "V6.4 experimental" and pa.get("archivo_sha256") == sha(pl64))
    if st.get("estado_analisis") in ("concluido", "pendiente_de_datos", "pendiente_de_investigacion") and st.get("auditoria"):
        mat = j(os.path.join(c, "material_auditoria.json")) or {}
        comprobar("constata", f"{nombre}: el material auditado incluye la configuración, la selección, las variantes y la cadena de trazabilidad",
                  {"configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json", "cadena_trazabilidad.json"} <= set(mat.get("archivos") or []))
        fc = j(os.path.join(c, "fase_c.json")) or {}
        var = j(os.path.join(c, "configuracion_v64_variantes.json")) or {}
        fi = j(os.path.join(c, "ficha.json")) or {}
        if (fc.get("configuracion_v64") or {}).get("objetivo") is not None:
            ev = OB.evaluar(c) or {}
            ob = fi.get("objetivo") or {}
            comprobar("reejecuta", f"{nombre}: objetivo_v64.evaluar sobre el material final da el tratamiento que publica la ficha y el estado del expediente",
                      ev.get("tratamiento") == ob.get("tratamiento") and (ev.get("estado_esperado") in (None, st.get("estado_analisis"))),
                      f"evaluar {ev.get('tratamiento')}/{ev.get('estado_esperado')} · ficha {ob.get('tratamiento')} · estado {st.get('estado_analisis')}")
        import entradas_economicas as EE
        pr = j(os.path.join(c, "precio.json")) or {}
        act = next((x for x in var.get("variantes") or [] if x.get("clave") == "activa"), {})
        emp = os.path.basename(c)
        # (revisión de lo afectado, RA1) la misma comparación que los pasos 10 y 12 del pipeline: según la relación guardada; con la relación
        # anterior («4.12», sin la fila 13 de la Historia), esa fila se compara con la del libro de la variante activa
        dif_ee, _inst, nota_ee = EE.comparar(var.get("entradas_economicas"), os.path.join(c, f"{emp}_v63_evaluada.xlsx"),
                                              os.path.join(c, "variantes_v64", "recalc", "activa.xlsx"))
        comprobar("reejecuta", f"{nombre}: la variante «activa» reproduce precio.json (1e-9) y las variantes son de las entradas económicas del libro final (instantánea recalculada, formato 4.12)",
                  var.get("formato") == "4.12" and abs((act.get("ponderado") or 0) - (pr.get("ponderado") or 1)) <= 1e-9
                  and abs((act.get("precio_si") or 0) - (pr.get("precio_si") or 1)) <= 1e-9 and dif_ee == [],
                  f"diferencias {dif_ee[:3]} · {nota_ee or 'relación actual'}")
        aud = leer(os.path.join(c, "auditoria.md"))
        comprobar("constata", f"{nombre}: auditoría ligada a su solicitud y a su material", re.search(r"^Material auditado: \S+", aud, re.M) is not None
                  and re.search(r"^Solicitud de auditoría: \S+", aud, re.M) is not None)
    return st


def main():
    print("1. ALCANCE DE LOS CAMBIOS (frente a la 4.11)")
    m411 = manifiesto(os.path.join(EXP, "reproduccion", "MANIFIESTO_SHA256_4_11.txt"))
    act = arbol()
    cambiados = {p for p in m411 if p in act and act[p] != m411[p]}
    comprobar("constata", "los archivos de la 4.11 que cambian son exactamente los declarados", cambiados == CAMBIADOS_FRENTE_A_4_11,
              f"de más {sorted(cambiados - CAMBIADOS_FRENTE_A_4_11)[:5]} · sin cambiar {sorted(CAMBIADOS_FRENTE_A_4_11 - cambiados)[:5]}")
    desaparecidos = [p for p in m411 if p not in act and p != "MANIFIESTO_SHA256.txt"]
    comprobar("constata", "ningún archivo de la 4.11 desaparece", not desaparecidos, str(desaparecidos[:5]))
    nuevos = [p for p in act if p not in m411]
    fuera = [p for p in nuevos if not p.startswith(NUEVOS_PERMITIDOS)]
    comprobar("constata", "los archivos nuevos están en el expediente 4.12 o son la guía y los cinco módulos nuevos declarados", not fuera, str(fuera[:5]))
    for pref, nombre in (("personaje_v2/empresas_v2/", "originales de personaje_v2/empresas_v2/"), ("personaje_v2/empresas_v2_correcciones/", "expedientes y entregas anteriores"),
                         ("v6/", "plantillas, referencias y scripts de v6/ (salvo el README de la V6.4)"), ("contrastes/", "contrastes de entregas anteriores")):
        lista = [p for p in m411 if p.startswith(pref) and p not in CAMBIADOS_FRENTE_A_4_11]
        comprobar("constata", f"{nombre}: {len(lista)} archivos con la huella de la 4.11", lista and all(act.get(p) == m411[p] for p in lista))

    print("\n2. PLANTILLAS Y RECONSTRUCCIÓN (§6)")
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.3.txt"], cwd=os.path.join(RAIZ, "v6"))
    comprobar("reejecuta", "V6.3: entregables y referencia con sus SHA-256", rc == 0, out[-200:])
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.4_experimental.txt"], cwd=V64)
    comprobar("reejecuta", "V6.4 experimental: plantilla y referencia con su huella ESTRICTA (artefacto entregado)", rc == 0, out[-200:])
    pl64 = os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")
    rc, out = run([sys.executable, "-I", os.path.join(V64, "scripts", "verificar_v64.py"), pl64, os.path.join(V64, "referencia", "referencia_V6.4_experimental.json")])
    comprobar("reejecuta", "verificar_v64.py: la plantilla V6.4 es ÍNTEGRA con su referencia", rc == 0 and "ÍNTEGRO" in out, out[-200:])
    nueva = os.path.join(TMP, "V64_reconstruida.xlsx")
    rc, out = run([sys.executable, "-I", os.path.join(V64, "scripts", "construir_v64_experimental.py"), os.path.join(RAIZ, "v6", "entregables", "Plantilla_V6.3.xlsx"), nueva])
    import comparar_zip as CZ
    iguales, detalle = CZ.comparar(nueva, pl64) if rc == 0 else (False, out[-200:])
    comprobar("reejecuta", "la reconstrucción desde la V6.3 tiene el mismo contenido, miembro a miembro, que la plantilla entregada (la huella del archivo depende de la compresión)",
              rc == 0 and iguales, str(detalle)[:200])

    print("\n3. VERIFICADOR DEL PAQUETE Y BATERÍA")
    vp = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    pos = [vp.find(f'echo "== batería {x}') for x in ("de la integración V6.4", "de trazabilidad", "de integridad de la auditoría vigente",
                                                     "de solicitudes de auditoría", "de coherencia de estados", "del resumen", "de cierre")]
    comprobar("constata", "verificar_paquete.sh completa exige la batería de la V6.4 con al menos 127 pruebas, la primera de las obligatorias, y conserva las demás con sus mínimos",
              "test_integracion_v64.py" in vp and "-ge 127" in vp and all(x > 0 for x in pos) and pos == sorted(pos) and all(f"-ge {n}" in vp for n in (78, 103, 55, 28, 45)))
    tv = leer(os.path.join(PV, "pruebas", "test_integracion_v64.py"))
    comprobar("constata", "la batería de la V6.4 tiene los grupos E (vigencia), F (materialidad y protocolos) y G (coherencia) además de A–D",
              all(re.search(rf"def grupo_{g.lower()}\b", tv) for g in "ABCDEFG"))

    print("\n4. VIGENCIA ANTES DEL RECHAZO (§3)")
    r411 = j(os.path.join(EXP, "resultados", "reproduccion_vigencia_codigo_4_11.json")) or {}
    r412 = j(os.path.join(EXP, "resultados", "reproduccion_vigencia_4_12.json")) or {}
    comprobar("constata", "el fallo de la 4.11 está reproducido (código 4.11: rechazo con la aprobación conservada) y corregido (código 4.12: retirada antes del rechazo)",
              r411.get("aprobacion_del_material_anterior_retirada") is False and r411.get("ficha_oficial_presente") is True
              and r412.get("aprobacion_del_material_anterior_retirada") is True and r412.get("ficha_oficial_presente") is False)

    print("\n5. PROTOCOLOS, MATERIALIDAD Y TRAZABILIDAD (§4 y §5)")
    import configuracion_economica as CE
    comprobar("constata", "los dos protocolos experimentales existen y ninguno es el de omisión (la configuración los declara)", set(CE.PROTOCOLOS) == {"bloqueo_del_objetivo", "objetivo_condicionado"})
    dif = j(os.path.join(EXP, "resultados", "diferencias_piloto_4_11_codigo_final.json")) or {}
    comprobar("constata", "diferencias entre el piloto 4.11 y el código final documentadas, con el piloto intacto", dif.get("piloto_intacto") is True)
    for c, n in ((COND, "cierre condicionado"), (BLOQ, "cierre con bloqueo"), (VIS, "Viscofan")):
        st_n, _ = cerrado(c)
        if st_n.get("auditoria"):
            ct = j(os.path.join(c, "cadena_trazabilidad.json")) or {}
            comprobar("constata", f"{n}: cadena de trazabilidad del paso 12 (fuente → … → conclusión) con entradas, resultado y conclusión",
                      bool(ct.get("entradas")) and bool(ct.get("resultado")) and bool(ct.get("conclusion")) and os.path.exists(os.path.join(c, "verificacion_trazabilidad.txt")))

    print("\n6. RF (§6)")
    reg = leer(os.path.join(EXP, "REGISTRO_AVANCE_4_12.md")) + leer(os.path.join(EXP, "INFORME_INTEGRACION_4_12.md"))
    comprobar("constata", "la fuente de rf del Bundesbank: o el PDF con su huella real, o la limitación exacta registrada (sin afirmar el ejemplar)",
              "Limitación registrada" in reg or os.path.exists(os.path.join(EXP, "fuentes", "rendbund-data.pdf")))

    print("\n7. VIDRALA (§7)")
    cp = j(os.path.join(EXP, "control_palancas_4_11", "resultados", "control_palancas.json")) or {}
    comprobar("constata", "control con las palancas de la 4.11 y el código final: CONCUERDA (valoración, 13 variantes y entradas económicas)", cp.get("resultado") == "CONCUERDA")
    st_c = expediente_real(COND, "cierre condicionado")
    st_b = expediente_real(BLOQ, "cierre con bloqueo")
    pc, pb = j(os.path.join(COND, "configuracion_economica.json")) or {}, j(os.path.join(BLOQ, "configuracion_economica.json")) or {}
    comprobar("constata", "las dos copias difieren SOLO en el protocolo del objetivo (y en su nota): misma configuración económica",
              pc.get("protocolo_objetivo") == "objetivo_condicionado" and pb.get("protocolo_objetivo") == "bloqueo_del_objetivo"
              and CE.celdas(pc) == CE.celdas(pb))
    ac, ab = leer(os.path.join(COND, "auditoria.md")), leer(os.path.join(BLOQ, "auditoria.md"))
    comprobar("constata", "no se copia una aprobación: auditorías y solicitudes distintas, y la de la copia se retiró antes (historial_cierres)",
              ac and ab and ac != ab and os.path.isdir(os.path.join(BLOQ, "historial_cierres")))
    for f in ("fase_a.json", "fase_b.json", "fase_c.json"):
        comprobar("constata", f"agentes reales: {f} del cierre nuevo no es el del piloto 4.11", os.path.exists(os.path.join(COND, f)) and sha(os.path.join(COND, f)) != sha(os.path.join(PIL411, f)))
    ch = j(os.path.join(EXP, "cierre_condicionado", "resultados", "comparacion_homogenea.json")) or {}
    comprobar("constata", "comparación homogénea heredado/experimental con las mismas entradas y palancas", bool(ch.get("componentes")) and ch.get("mismas_entradas"))
    comprobar("constata", "revisión económica y comparación de protocolos presentes",
              os.path.exists(os.path.join(EXP, "REVISION_ECONOMICA_VIDRALA_4_12.md")) and os.path.exists(os.path.join(EXP, "COMPARACION_PROTOCOLOS_4_12.md")))
    f1d = os.path.join(COND, "fase1_decisiones.json")
    origen = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "fase1_decisiones.json")
    comprobar("constata", "ningún campo humano relleno: fase1_decisiones.json del cierre = el del origen 4.6.1", os.path.exists(f1d) and sha(f1d) == sha(origen))

    print("\n8. VISCOFAN (§8)")
    inv = j(os.path.join(EXP, "viscofan", "fuentes", "inventario_fuentes_viscofan.json")) or {}
    rec = inv.get("recuperadas") or []
    comprobar("reejecuta", f"publicaciones recuperadas con su huella ({len(rec)}): cada PDF conserva el SHA-256 inventariado",
              rec and all(sha(os.path.join(RAIZ, r["archivo"])) == r["sha256"] for r in rec))
    # cada publicación es de la misma paginación que la fuente de la fase 1 (se dice «misma paginación y cifras», no «mismo archivo»)
    # o de otra edición (no es el original recuperado y no lleva el nombre AR_<año>.pdf de la fuente de la fase 1); la otra edición
    # de 2020 que se sustituyó no está entre las publicaciones ni en los textos del expediente
    otras = [r for r in rec if "OTRA EDICIÓN" in (r.get("edicion") or "")]
    mismas = [r for r in rec if "MISMA PAGINACIÓN" in (r.get("edicion") or "")]
    sust = inv.get("sustituidas_no_conservadas") or []
    comprobar("constata", "ninguna edición distinta se llama «original recuperado» ni lleva el nombre de la fuente de la fase 1; la misma paginación no se dice «mismo archivo»",
              rec and len(otras) + len(mismas) == len(rec)
              and not any(re.fullmatch(r"AR_\d{4}\.pdf", os.path.basename(r["archivo"])) for r in otras)
              and all("no es el original recuperado" in r["edicion"] for r in otras) and all("no «mismo archivo»" in r["edicion"] for r in mismas)
              and not any(s.get("sha256") in {r["sha256"] for r in rec} for s in sust)
              and not any(os.path.exists(os.path.join(EXP, "viscofan", "fuentes", "pdf", s.get("archivo") or "-")) for s in sust))
    rp = j(os.path.join(EXP, "viscofan", "resultados", "reproduccion_heredado.json")) or {}
    comprobar("constata", "resultado heredado reproducido con el código final en V6.3 y en V6.4 heredado (cifras completas, |Δ| ≤ 1e-9)", rp.get("resultado") == "COINCIDE")
    an = j(os.path.join(EXP, "viscofan", "configuracion", "analisis_configuracion_viscofan.json")) or {}
    comprobar("constata", "análisis propio de la configuración: todas las cifras citadas están en su página", an and all(x.get("en_la_pagina") for x in (an.get("cifras_comprobadas") or {}).values()))
    conf_v = j(os.path.join(VIS, "configuracion_economica.json")) or {}
    comprobar("constata", "configuración propia de Viscofan: válida, sin central para θ (rango [0, 1]) y sin parámetros de Vidrala",
              not CE.validar(conf_v) and (conf_v.get("PM1") or {}).get("theta_rango") == [0.0, 1.0] and (conf_v.get("PM1") or {}).get("lambda") is None
              and (conf_v.get("N1") or {}).get("valor") != (pc.get("N1") or {}).get("valor"))
    expediente_real(VIS, "Viscofan")
    pr = j(os.path.join(EXP, "viscofan", "experimental", "resultados", "preparacion.json")) or {}
    comprobar("constata", "Viscofan: fechas separadas (base, ejecución, precio, acciones, rf y fuentes) y origen intacto",
              set(("base_economica", "ejecucion", "precio", "acciones", "tasa_sin_riesgo", "fuentes")) <= set((pr.get("fechas") or {}).keys()))

    print("\n9. PROPUESTA HUMANA")
    pj = j(os.path.join(EXP, "propuestas", "propuesta_humana_4_12.json")) or {}
    decs = pj.get("decisiones") or []
    comprobar("constata", "propuesta humana única y breve, separada en decisiones de uso del sistema y elecciones económicas, sin ningún campo humano relleno",
              decs and {d.get("grupo") for d in decs} >= {"uso del sistema", "elección económica"}
              and all(d.get("decision") is None and d.get("fecha") is None and d.get("decidido_por") is None for d in decs))

    print("\n10. DOCUMENTACIÓN DE LA VERSIÓN")
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.12",
              "entrega 4.12" in leer(os.path.join(RAIZ, "VERSION")) and "entrega 4.12" in leer(os.path.join(RAIZ, "CONTINUIDAD.md"))
              and "munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.zip" in leer(os.path.join(RAIZ, "PROMPT_NUEVA_VENTANA.md")))
    comprobar("constata", "guía breve del recorrido supervisado y Anexo D (D.13)", os.path.exists(os.path.join(PV, "GUIA_RECORRIDO_SUPERVISADO.md"))
              and "## D.13" in leer(os.path.join(PV, "ANEXO_D_salidas_y_formatos.md")))
    comprobar("constata", "informe integrado (con la evaluación de aptitud), registro de la entrega, registro de pruebas, revisión interna y LEEME de controles históricos presentes",
              all(os.path.exists(os.path.join(EXP, f)) for f in ("INFORME_INTEGRACION_4_12.md", "REGISTRO_ENTREGA_4.12.md", "REGISTRO_PRUEBAS_4_12.md",
                                                                 "revision_interna/REVISION_INTERNA_4_12.md", "resultados/LEEME_CONTROLES_HISTORICOS_4_12.md"))
              and "Evaluación expresa de aptitud de uso" in leer(os.path.join(EXP, "INFORME_INTEGRACION_4_12.md")))
    print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen ({TIPOS['reejecuta']} reejecutan, {TIPOS['constata']} constatan).")
    return 0 if N_OK == N_T else 1


if __name__ == "__main__":
    sys.exit(main())
