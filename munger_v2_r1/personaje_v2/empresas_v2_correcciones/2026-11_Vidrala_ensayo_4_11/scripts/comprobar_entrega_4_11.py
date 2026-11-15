#!/usr/bin/env python3
"""Control de la entrega 4.11 (integración económica experimental del motor B). Uso (desde munger_v2_r1/, después de
verificar_paquete.sh completa y de los controles históricos): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_11/scripts/comprobar_entrega_4_11.py
No usa LibreOffice (la batería de la V6.4, que sí lo usa, va en verificar_paquete.sh completa). Escribe solo en temporales.
Tipos: «reejecuta» (vuelve a ejecutar un script de solo lectura y compara), «constata» (comprueba un hecho del árbol).
Lo que comprueba: alcance de los cambios frente a la 4.10.1 (originales y expedientes anteriores intactos), plantilla V6.4 (huellas,
verificador, reconstrucción determinista) y V6.3 intacta, verificador del paquete, cambio de base (concordancia y sin restos en el
control y en el piloto), control heredado, piloto (selección, configuración de demostración, material auditado, fase C, ficha,
informe, auditoría), réplica, aislamiento de C46/C47 y C49, propuesta humana sin firmar y documentación de la versión."""
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
PIL = os.path.join(EXP, "piloto", "Vidrala")
CTL = os.path.join(EXP, "control_heredado", "Vidrala")
REL_EXP = os.path.relpath(EXP, RAIZ) + "/"
TMP = tempfile.mkdtemp(prefix="control411_")
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "constata": 0}
# archivos de la 4.10.1 que la 4.11 cambia (el resto del manifiesto de la 4.10.1 tiene que estar igual)
CAMBIADOS_FRENTE_A_4_10_1 = {
    "VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "CAMBIOS_ARCHIVOS.txt", "verificar_paquete.sh",
    "personaje_v2/ANEXO_D_salidas_y_formatos.md", "personaje_v2/esquema/fase_c.esquema.json", "personaje_v2/esquema/ficha.esquema.json",
    "personaje_v2/prompts/fase_a.md", "personaje_v2/prompts/fase_b.md", "personaje_v2/prompts/fase_c_turno1.md", "personaje_v2/prompts/fase_c_turno2.md", "personaje_v2/prompts/verificacion.md",
} | {f"personaje_v2/scripts/{s}" for s in (
    "cierre_v2.py", "comprobacion_conjunta.py", "comprobar_entorno.sh", "comprobar_entrada_v63.py", "comprobar_gramatica.py", "config_v2.py",
    "escribir_v63.py", "ficha.py", "informe.py", "leer_resultados.py", "leer_v63.py", "migrar_v53_a_v63.py", "pipeline.py",
    "rellenar_fase1_v63.py", "verificar_todo.sh", "volcar_datos_v63.py")}
NUEVOS_PERMITIDOS = (REL_EXP, "v6/v64_experimental/", "personaje_v2/config_v2_v64_experimental.json", "personaje_v2/pruebas/test_integracion_v64.py",
                     "personaje_v2/scripts/cambiar_base.py", "personaje_v2/scripts/configuracion_economica.py",
                     "personaje_v2/scripts/seleccion_plantilla.py", "personaje_v2/scripts/variantes_configuracion_v64.py")
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
    for l in open(p, encoding="utf-8"):
        if l.strip() and not l.startswith("#"):
            h, f = l.rstrip("\n").split("  ", 1)
            d[f] = h
    return d


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.exists(p) else ""


def j(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def arbol():
    """Archivos del árbol en disco. Como en el LEEME de los controles, no cuentan las salidas que las baterías escriben en
    personaje_v2/pruebas/ (los archivos de esa carpeta que no están en el MANIFIESTO_SHA256.txt del propio árbol), ni __pycache__,
    .lo_perfil/ o pruebas/_v64/: así el control da lo mismo antes y después de verificar_paquete.sh completa."""
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


def main():
    print("1. ALCANCE DE LOS CAMBIOS (frente a la 4.10.1)")
    m4101 = manifiesto(os.path.join(EXP, "reproduccion", "MANIFIESTO_SHA256_4_10_1.txt"))
    act = arbol()
    cambiados = {p for p in m4101 if p in act and act[p] != m4101[p]}
    comprobar("constata", "los archivos de la 4.10.1 que cambian son exactamente los declarados", cambiados == CAMBIADOS_FRENTE_A_4_10_1,
              f"de más {sorted(cambiados - CAMBIADOS_FRENTE_A_4_10_1)[:5]} · sin cambiar {sorted(CAMBIADOS_FRENTE_A_4_10_1 - cambiados)[:5]}")
    desaparecidos = [p for p in m4101 if p not in act and p != "MANIFIESTO_SHA256.txt"]
    comprobar("constata", "ningún archivo de la 4.10.1 desaparece", not desaparecidos, str(desaparecidos[:5]))
    nuevos = [p for p in act if p not in m4101]
    fuera = [p for p in nuevos if not p.startswith(NUEVOS_PERMITIDOS)]
    comprobar("constata", "los archivos nuevos están en el expediente 4.11, en v6/v64_experimental/ o son los scripts, la configuración y la batería declarados",
              not fuera, str(fuera[:5]))
    orig = [p for p in m4101 if p.startswith("personaje_v2/empresas_v2/")]
    comprobar("constata", f"originales intactos: los {len(orig)} archivos de personaje_v2/empresas_v2/ con la huella de la 4.10.1",
              orig and all(act.get(p) == m4101[p] for p in orig))
    previos = [p for p in m4101 if p.startswith("personaje_v2/empresas_v2_correcciones/")]
    comprobar("constata", f"expedientes y entregas anteriores intactos ({len(previos)} archivos de empresas_v2_correcciones/)",
              all(act.get(p) == m4101[p] for p in previos))

    print("\n2. PLANTILLAS")
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.3.txt"], cwd=os.path.join(RAIZ, "v6"))
    comprobar("reejecuta", "V6.3: entregables y referencia con sus SHA-256", rc == 0, out[-200:])
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.4_experimental.txt"], cwd=V64)
    comprobar("reejecuta", "V6.4 experimental: plantilla y referencia con sus SHA-256", rc == 0, out[-200:])
    pl64 = os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")
    rc, out = run([sys.executable, "-I", os.path.join(V64, "scripts", "verificar_v64.py"), pl64, os.path.join(V64, "referencia", "referencia_V6.4_experimental.json")])
    comprobar("reejecuta", "verificar_v64.py: la plantilla V6.4 es ÍNTEGRA con su referencia", rc == 0 and "ÍNTEGRO" in out, out[-200:])
    nueva = os.path.join(TMP, "V64_reconstruida.xlsx")
    rc, out = run([sys.executable, "-I", os.path.join(V64, "scripts", "construir_v64_experimental.py"), os.path.join(RAIZ, "v6", "entregables", "Plantilla_V6.3.xlsx"), nueva])
    comprobar("reejecuta", "la reconstrucción desde la V6.3 da el mismo SHA-256 que la plantilla entregada (determinista)", rc == 0 and sha(nueva) == sha(pl64), out[-200:])
    ref = j(os.path.join(V64, "referencia", "referencia_V6.4_experimental.json"))
    comprobar("constata", "la referencia V6.4 salió de la plantilla entregada", ref and ref.get("sha256_origen") == sha(pl64))
    cfg64 = j(os.path.join(PV, "config_v2_v64_experimental.json"))
    cfg63 = j(os.path.join(PV, "config_v2.json"))
    propias = ("plantilla", "_nota", "version_config", "resumen_csv_nombre", "_nota_resumen")
    comprobar("constata", "config_v2_v64_experimental.json = config_v2.json salvo la plantilla, las notas, la versión de la configuración y el nombre propio del resumen "
              "(resumen_v2_v64_experimental.csv, revisión interna H2); config_v2.json sin cambios",
              {k: v for k, v in cfg64.items() if k not in propias} == {k: v for k, v in cfg63.items() if k not in propias} and "resumen_csv_nombre" not in cfg63
              and cfg64["plantilla"]["version"] == "V6.4 experimental" and cfg64.get("resumen_csv_nombre") == "resumen_v2_v64_experimental.csv"
              and "config_v2.json" not in CAMBIADOS_FRENTE_A_4_10_1)

    print("\n3. VERIFICADOR DEL PAQUETE")
    vp = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    pos = [vp.find(f'echo "== batería {x}') for x in ("de la integración V6.4", "de trazabilidad", "de integridad de la auditoría vigente",
                                                     "de solicitudes de auditoría", "de coherencia de estados", "del resumen", "de cierre")]
    comprobar("constata", "verificar_paquete.sh completa exige la batería de la V6.4 (al menos 58 pruebas), la primera de las obligatorias, y conserva las demás con sus mínimos",
              "test_integracion_v64.py" in vp and "-ge 58" in vp and all(x > 0 for x in pos) and pos == sorted(pos)
              and all(f"-ge {n}" in vp for n in (78, 103, 55, 28, 45)))

    print("\n4. CAMBIO DE BASE")
    for nombre, conf in (("control heredado", "cambio_de_base_control_heredado.json"), ("piloto", "cambio_de_base_piloto.json")):
        rc, out = run([sys.executable, "-I", os.path.join(PV, "scripts", "cambiar_base.py"), "comprobar", os.path.join(EXP, "configuracion", conf)], cwd=RAIZ)
        comprobar("reejecuta", f"{nombre}: entradas concordantes y ningún resto de la base anterior en la evidencia activa ni en las notas", rc == 0 and "CONCUERDA Y SIN RESTOS" in out, out[-300:])
    rc, out = run([sys.executable, "-I", os.path.join(AQUI, "preparar_configuraciones_4_11.py"), os.path.join(TMP, "configuracion")], cwd=RAIZ)
    comprobar("reejecuta", "las dos configuraciones de cambio de base se reproducen byte a byte con preparar_configuraciones_4_11.py (en un temporal)",
              rc == 0 and all(sha(os.path.join(TMP, "configuracion", n)) == sha(os.path.join(EXP, "configuracion", n))
                              for n in ("cambio_de_base_control_heredado.json", "cambio_de_base_piloto.json")), out[-200:])
    for d in (PIL, CTL):
        reg = j(os.path.join(os.path.dirname(d), "resultados", "cambio_de_base.json")) or {}
        comprobar("constata", f"{os.path.relpath(d, EXP)}: etapa 1 original archivada con la huella de la 4.6.1 y fechas separadas",
                  reg.get("etapa1", {}).get("original_sha256", "").startswith("6aed21169576aa44") and reg.get("fechas", {}).get("precio") == "2025-12-31"
                  and (j(os.path.join(d, "fase1_metadatos.json")) or {}).get("fecha_analisis") not in (None, "2025-12-31"))

    print("\n5. CONTROL HEREDADO")
    ch = j(os.path.join(EXP, "control_heredado", "resultados", "control_heredado.json")) or {}
    comprobar("constata", "control heredado: V6.4 en modo heredado = 4.10.1 (V, ponderado, precio de Sí, zona y estados; libro sin otras diferencias)",
              ch.get("resultado") == "CONCUERDA" and all(v == 0 for v in (ch.get("diferencias_valoracion") or {"x": 1}).values()) and ch.get("libro", {}).get("otras") == [])

    print("\n6. PILOTO (V6.4 experimental, configuración de demostración)")
    st = j(os.path.join(PIL, "estado_pipeline.json")) or {}
    pa = j(os.path.join(PIL, "plantilla_activa.json")) or {}
    comprobar("constata", "plantilla_activa.json: V6.4 experimental con la huella de la plantilla entregada", pa.get("version") == "V6.4 experimental" and pa.get("archivo_sha256") == sha(pl64))
    conf_p = j(os.path.join(PIL, "configuracion_economica.json"))
    conf_d = (j(os.path.join(EXP, "configuracion", "cambio_de_base_piloto.json")) or {}).get("configuracion_economica")
    import configuracion_economica as CE
    comprobar("constata", "la configuración del piloto es la de demostración declarada (válida, experimental, no adoptada)",
              conf_p == conf_d and not CE.validar(conf_p) and conf_p.get("modo") == "Experimental" and "NO es una adopción" in conf_p.get("naturaleza", ""))
    terminado = st.get("paso") == 14 or st.get("estado_analisis") not in (None, "")
    comprobar("constata", f"el pipeline del piloto terminó (estado {st.get('estado_analisis')!r}, paso {st.get('paso')}, auditoría {st.get('auditoria')!r}) sin una espera abierta",
              terminado and not os.path.exists(os.path.join(PIL, "ESPERANDO.md")))
    mat = j(os.path.join(PIL, "material_auditoria.json")) or {}
    comprobar("constata", "el material auditado incluye configuracion_economica.json, plantilla_activa.json y configuracion_v64_variantes.json",
              {"configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json"} <= set(mat.get("archivos") or []))
    fc = j(os.path.join(PIL, "fase_c.json")) or {}
    cv = fc.get("configuracion_v64") or {}
    claves = {x.get("clave") for x in cv.get("parametros") or []}
    var = j(os.path.join(PIL, "configuracion_v64_variantes.json")) or {}
    comprobar("constata", "la fase C evalúa cada parámetro activo y el mantenimiento (adoptada = false) y solo afirma «no cambia la zona» si las variantes calculadas lo respaldan",
              set(CE.activos(conf_p)) - {"modo"} <= claves and (cv.get("mantenimiento") or {}).get("adoptada") is False
              and str((cv.get("mantenimiento") or {}).get("evaluacion") or "").strip() != ""
              and (not cv.get("zona_igual_en_variantes_calculadas") or var.get("zona_igual_en_todas_las_calculadas") is True))
    comprobar("constata", "las variantes del paso 10 incluyen heredado, activa, componentes aislados y las otras cuatro estructuras con entradas compatibles",
              var.get("aplica") and {"heredado", "activa", "solo_N1", "solo_N2", "solo_R1", "activa_sin_PM1", "activa_solo_P0",
                                     "estructura_H", "estructura_S", "estructura_SR2", "estructura_SRF"} <= {v["clave"] for v in var.get("variantes", [])})
    fi = j(os.path.join(PIL, "ficha.json")) or {}
    inf = leer(os.path.join(PIL, "informe.md"))
    if st.get("estado_analisis") == "concluido":
        comprobar("constata", "ficha e informe: plantilla V6.4 experimental, configuración no adoptada (§14) y distancias con denominador identificado",
                  (fi.get("versiones") or {}).get("plantilla") == "V6.4 experimental" and (fi.get("configuracion_economica") or {}).get("modo") == "Experimental"
                  and "14. Plantilla y configuración económica" in inf and "no adoptada" in inf and "denominador identificado" in inf)
        aud = leer(os.path.join(PIL, "auditoria.md"))
        comprobar("constata", "auditoría del piloto: APROBADO, interna y ligada a su solicitud y su material",
                  st.get("auditoria") == "APROBADO" and re.search(r"^Material auditado: \S+", aud, re.M) and re.search(r"^Solicitud de auditoría: \S+", aud, re.M) is not None)
    else:
        diag = leer(os.path.join(PIL, "diagnostico.md"))
        comprobar("constata", "el piloto no concluido tiene un diagnóstico que dice qué falta y desde qué paso seguir", bool(diag.strip()))
    f1d = os.path.join(PIL, "fase1_decisiones.json")
    origen = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_6_1", "Vidrala", "fase1_decisiones.json")
    comprobar("constata", "ningún campo humano relleno: fase1_decisiones.json del piloto = el del origen 4.6.1",
              os.path.exists(f1d) and sha(f1d) == sha(origen))

    print("\n7. RÉPLICA, AISLAMIENTO Y PROPUESTA")
    rp = leer(os.path.join(EXP, "replica", "replica_salida_plantilla_final.txt"))
    man = j(os.path.join(EXP, "replica", "manifiesto_casos_plantilla_final.json")) or {}
    comprobar("constata", "réplica independiente sobre los libros de la plantilla final: 117 de 117 casos coinciden",
              "117 de 117 casos coinciden" in rp and man.get("plantilla_sha256") == sha(pl64) and len(man.get("casos") or []) == 117)
    ai = j(os.path.join(EXP, "resultados", "aislamiento_entradas_4_11.json")) or {}
    comprobar("constata", "aislamiento de C46/C47 (precisión) y C49 (P3): el control reproduce el expediente y cada variante tiene su efecto",
              ai.get("control_reproduce_el_expediente") is True and {"C46_C47_precisos", "C49_pago_total", "combinada"} <= {v["clave"] for v in ai.get("variantes", []) if "fallo" not in v})
    pj = j(os.path.join(EXP, "propuestas", "propuesta_humana_4_11.json")) or {}
    decs = pj.get("decisiones") or []
    comprobar("constata", "propuesta humana única y agrupada, con recomendación argumentada, alternativas, evidencia, efectos y consecuencias, y sin ningún campo humano relleno",
              decs and all(d.get("recomendacion") and d.get("alternativas") and d.get("evidencia") and d.get("efectos") and d.get("si_no_se_adopta") for d in decs)
              and all(d.get("decision") is None and d.get("fecha") is None and d.get("decidido_por") is None for d in decs))
    comprobar("constata", "la propuesta recoge las decisiones que abrió la revisión interna (D411-MATERIALIDAD por H4 y D411-DOMINIOS por H13): 13 en total",
              len(decs) == 13 and {"D411-MATERIALIDAD", "D411-DOMINIOS"} <= {d.get("id") for d in decs})

    print("\n7b. RESPUESTA A LA REVISIÓN INTERNA (ejecuciones del §5)")
    si = j(os.path.join(EXP, "resultados", "seleccion_inversa_4_11.json")) or {}
    comprobar("constata", "selección inversa sobre una copia de un expediente V6.3 cerrado (H1): código 2, ningún archivo nuevo ni cambiado",
              si.get("resultado") == "CONFORME" and si.get("codigo_de_salida") == 2 and not si.get("archivos_nuevos") and not si.get("archivos_cambiados"))
    rl = j(os.path.join(EXP, "resultados", "rango_lambda_4_11.json")) or {}
    comprobar("constata", "extremos del rango de λ recalculados en el libro (H11), con la variante «activa» igual al precio.json del piloto",
              rl.get("control_activa_reproduce_el_expediente") is True and {"parametro_minimo", "parametro_maximo"} <= {v.get("clave") for v in rl.get("variantes") or []})
    vg = j(os.path.join(EXP, "resultados", "vigencia_piloto_4_11.json")) or {}
    comprobar("constata", "vigencia del piloto con el código final, en lectura: cierre vigente, selección, variantes y celdas conformes, y piloto intacto",
              vg.get("resultado") == "VIGENTE" and vg.get("piloto_intacto") is True and vg.get("motivo_vigencia") is None)
    cdp = [j(os.path.join(PIL if d == "p" else CTL, "..", "resultados", f"concordancia_Vidrala_v63_{t}.json")) for d in ("p", "c") for t in ("datos", "evaluada")]
    comprobar("constata", "concordancia del cambio de base guardada para el libro de datos y el evaluado del piloto y del control (H9)",
              all(isinstance(x, dict) and x.get("resultado") == "CONCUERDA Y SIN RESTOS" for x in cdp))

    print("\n8. DOCUMENTACIÓN DE LA VERSIÓN")
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.11",
              "entrega 4.11" in leer(os.path.join(RAIZ, "VERSION")) and "entrega 4.11" in leer(os.path.join(RAIZ, "CONTINUIDAD.md"))
              and "munger_v2_r1_entrega4.11_integracion_economica_experimental.zip" in leer(os.path.join(RAIZ, "PROMPT_NUEVA_VENTANA.md")))
    readme = leer(os.path.join(V64, "docs", "README_V6.4_experimental.md"))
    comprobar("constata", "documentación de la V6.4 (README con fórmulas y límites) y formatos nuevos en el Anexo D (D.12)",
              "## 8. Límites conocidos" in readme and "máximo conservado" in readme and "## D.12" in leer(os.path.join(PV, "ANEXO_D_salidas_y_formatos.md")))
    comprobar("constata", "informe de integración, registro de la entrega, registro de pruebas, revisión interna y LEEME de controles históricos presentes",
              all(os.path.exists(os.path.join(EXP, f)) for f in ("INFORME_INTEGRACION_4_11.md", "REGISTRO_ENTREGA_4.11.md", "REGISTRO_PRUEBAS_4_11.md",
                                                                 "revision_interna/REVISION_INTERNA_4_11.md", "resultados/LEEME_BATERIAS_HISTORICAS.md")))
    print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen ({TIPOS['reejecuta']} reejecutan, {TIPOS['constata']} constatan).")
    return 0 if N_OK == N_T else 1


if __name__ == "__main__":
    sys.exit(main())
