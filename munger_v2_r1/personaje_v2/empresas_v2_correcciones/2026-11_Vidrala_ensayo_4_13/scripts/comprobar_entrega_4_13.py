#!/usr/bin/env python3
"""Control de la entrega 4.13 (fiabilidad del motor B y conciliación económica de los dos casos). Uso (desde munger_v2_r1/, después de
verificar_paquete.sh completa y de las sondas de la ronda final):
    python3 -I -B personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/scripts/comprobar_entrega_4_13.py
No usa LibreOffice (las baterías que lo usan van en verificar_paquete.sh completa). Escribe solo en temporales (con -B, ni cachés:
además se fija sys.dont_write_bytecode). La réplica, las sondas y la batería se leen de sus registros («constata»): cada registro
lleva la huella de los scripts con que se ejecutó, y se compara con la de los scripts actuales.
Tipos: «reejecuta» (vuelve a ejecutar un script de solo lectura o un cálculo y compara), «constata» (comprueba un hecho del árbol).
Lo que comprueba: alcance de los cambios frente a la 4.12 (originales, plantillas y expedientes anteriores intactos), plantillas V6.3,
V6.4 y V6.4.1, verificador y batería, guardas de tipos (§3), salto del protocolo (§4), cobertura y avisos de dominio (§5), acciones y
evidencia activa de Viscofan (§6), perímetro y réplica (§7), interpretaciones de Vidrala (§8), los tres expedientes finales, la revisión
interna, la propuesta sin firmar y la documentación de la versión."""
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
V641 = os.path.join(RAIZ, "v6", "v641_experimental")
COND = os.path.join(EXP, "vidrala_condicionado", "Vidrala")
BLOQ = os.path.join(EXP, "vidrala_bloqueo", "Vidrala")
VIS = os.path.join(EXP, "viscofan", "Viscofan")
REL_EXP = os.path.relpath(EXP, RAIZ) + "/"
TMP = tempfile.mkdtemp(prefix="control413_")
N_OK = N_T = 0
TIPOS = {"reejecuta": 0, "constata": 0}
# archivos de la 4.12 que la 4.13 cambia (el resto del manifiesto de la 4.12 tiene que estar igual)
CAMBIADOS_FRENTE_A_4_12 = {
    "VERSION", "CONTINUIDAD.md", "PROMPT_NUEVA_VENTANA.md", "CAMBIOS_ARCHIVOS.txt", "verificar_paquete.sh",
    "personaje_v2/GUIA_RECORRIDO_SUPERVISADO.md",
    "personaje_v2/esquema/fase_c.esquema.json", "personaje_v2/esquema/ficha.esquema.json",
    "personaje_v2/prompts/fase_c_turno1.md", "personaje_v2/prompts/fase_c_turno2.md", "personaje_v2/prompts/verificacion.md",
    "personaje_v2/pruebas/agentes_sinteticos.py", "personaje_v2/pruebas/test_integracion_v64.py",
} | {f"personaje_v2/scripts/{s}" for s in (
    "cierre_v2.py", "comprobacion_conjunta.py", "configuracion_economica.py", "dominios_v64.py", "entradas_economicas.py", "ficha.py", "informe.py",
    "leer_v63.py", "objetivo_v64.py", "pipeline.py", "referencias_mecanicas.py", "rellenar_fase1_v63.py", "resumen.py", "seleccion_plantilla.py",
    "trazabilidad_v64.py", "variantes_configuracion_v64.py", "volcar_datos_v63.py")}
NUEVOS_PERMITIDOS = (REL_EXP, "v6/v641_experimental/", "personaje_v2/scripts/estructura_json.py", "personaje_v2/config_v2_v641_experimental.json")
# textos de la etapa 1 que ya no pueden ser evidencia activa de las cifras frescas de Viscofan (§6 y revisión interna R7)
TEXTOS_RETIRADOS = ("6-oct-2026", "53,60 × 45,6036", "2.444,4", "Cierre 6-oct-2026")
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True   # (segunda revisión interna, S2) el control no deja __pycache__ en el árbol


def cachés():
    """(ronda B) .pyc del árbol con su fecha: el control compara la foto del principio con la del final. Las carpetas __pycache__
    que ya estaban (las dejan verificar_paquete.sh y los controles anteriores) no son del control; el ZIP las excluye."""
    return {os.path.join(r, f): os.path.getmtime(os.path.join(r, f)) for r, _d, fs in os.walk(RAIZ) if os.path.basename(r) == "__pycache__" for f in fs}


CACHÉS_AL_EMPEZAR = cachés()


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
    kw.setdefault("env", {**os.environ, "PYTHONDONTWRITEBYTECODE": "1"})   # (ronda B) los subprocesos tampoco escriben cachés
    r = subprocess.run(cmd, capture_output=True, text=True, **kw)
    return r.returncode, r.stdout + r.stderr


def arbol():
    """Archivos del árbol en disco, sin __pycache__, .lo_perfil/, pruebas/_v64/ ni las salidas de las baterías en personaje_v2/pruebas/
    que no están en el manifiesto del propio árbol."""
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
    return st, st.get("paso") == 14 and st.get("estado_analisis") not in (None, "") and not os.path.exists(os.path.join(c, "ESPERANDO.md"))


def expediente_real(c, nombre, version, plantilla):
    """Comprobaciones comunes de un expediente V6.4/V6.4.1 recorrido con agentes reales y el código final."""
    import configuracion_economica as CE
    import entradas_economicas as EE
    import objetivo_v64 as OB
    st, ok_cierre = cerrado(c)
    comprobar("constata", f"{nombre}: el pipeline terminó (estado {st.get('estado_analisis')!r}, auditoría {st.get('auditoria')!r}) sin una espera abierta", ok_cierre)
    comprobar("constata", f"{nombre}: auditoría APROBADO de la solicitud vigente, sobre el material vigente",
              st.get("auditoria") == "APROBADO" and (st.get("solicitudes_auditoria") or [{}])[-1].get("estado") == "respondida"
              and (st.get("solicitudes_auditoria") or [{}])[-1].get("material") == st.get("material_auditoria"))
    conf = j(os.path.join(c, "configuracion_economica.json")) or {}
    comprobar("constata", f"{nombre}: configuración experimental válida, declarada como ensayo y con protocolo del objetivo",
              conf.get("modo") == "Experimental" and not CE.validar(conf) and conf.get("protocolo_objetivo") in CE.PROTOCOLOS and "adopci" in conf.get("naturaleza", ""))
    pa = j(os.path.join(c, "plantilla_activa.json")) or {}
    comprobar("constata", f"{nombre}: plantilla_activa.json = {version} con la huella de la plantilla entregada", pa.get("version") == version and pa.get("archivo_sha256") == sha(plantilla))
    mat = j(os.path.join(c, "material_auditoria.json")) or {}
    comprobar("constata", f"{nombre}: el material auditado incluye la configuración, la selección, las variantes y la cadena de trazabilidad",
              {"configuracion_economica.json", "plantilla_activa.json", "configuracion_v64_variantes.json", "cadena_trazabilidad.json"} <= set(mat.get("archivos") or []))
    arch = mat.get("archivos") if isinstance(mat.get("archivos"), dict) else {}
    fallos = [f for f, h in arch.items() if not os.path.exists(os.path.join(c, f)) or sha(os.path.join(c, f)) != h]
    comprobar("reejecuta", f"{nombre}: las {len(arch)} huellas del material auditado coinciden con los archivos", arch and not fallos, str(fallos[:3]))
    fc = j(os.path.join(c, "fase_c.json")) or {}
    var = j(os.path.join(c, "configuracion_v64_variantes.json")) or {}
    fi = j(os.path.join(c, "ficha.json")) or {}
    ev = OB.evaluar(c) or {}
    ob = fi.get("objetivo") or {}
    comprobar("reejecuta", f"{nombre}: objetivo_v64.evaluar sobre el material final da el tratamiento que publica la ficha y el estado del expediente",
              ev.get("tratamiento") == ob.get("tratamiento") and (ev.get("estado_esperado") in (None, st.get("estado_analisis"))),
              f"evaluar {ev.get('tratamiento')}/{ev.get('estado_esperado')} · ficha {ob.get('tratamiento')} · estado {st.get('estado_analisis')}")
    comprobar("reejecuta", f"{nombre}: objetivo_v64.contradicciones_salida no encuentra ninguna contradicción en la salida final (acción, estado, protocolo y los dos objetivos)",
              not OB.contradicciones_salida(st.get("estado_analisis"), fi.get("decision") or {}, ob, ev))
    pr = j(os.path.join(c, "precio.json")) or {}
    act = next((x for x in var.get("variantes") or [] if x.get("clave") == "activa"), {})
    emp = os.path.basename(c)
    dif_ee, _inst, nota_ee = EE.comparar(var.get("entradas_economicas"), os.path.join(c, f"{emp}_v63_evaluada.xlsx"), os.path.join(c, "variantes_v64", "recalc", "activa.xlsx"))
    comprobar("reejecuta", f"{nombre}: variantes de formato 4.13; la «activa» reproduce precio.json (1e-9) y las variantes son de las entradas económicas del libro final",
              var.get("formato") == "4.13" and abs((act.get("ponderado") or 0) - (pr.get("ponderado") or 1)) <= 1e-9
              and abs((act.get("precio_si") or 0) - (pr.get("precio_si") or 1)) <= 1e-9 and dif_ee == [], f"diferencias {dif_ee[:3]} · {nota_ee or 'relación actual'}")
    # §5: contrato de cobertura en la fase C (todos los parámetros activos evaluados, base declarada, null ⇔ no determinada)
    pars = (fc.get("configuracion_v64") or {}).get("parametros") or []
    bases_ok = pars and all(p.get("base_de_la_materialidad") in ("calculada", "juicio_economico", "no_determinada")
                            and (p.get("material_para_accion") is None) == (p.get("base_de_la_materialidad") == "no_determinada")
                            and p.get("base_de_la_materialidad_objetivo") in ("calculada", "juicio_economico", "no_determinada")
                            and (p.get("material_para_objetivo") is None) == (p.get("base_de_la_materialidad_objetivo") == "no_determinada") for p in pars)
    comprobar("constata", f"{nombre}: fase C con el contrato de cobertura (base de la materialidad para la acción y para el objetivo, null ⇔ no determinada) en sus {len(pars)} parámetros", bases_ok)
    gv = (fc.get("configuracion_v64") or {}).get("avisos_de_dominio_variantes") or []
    comprobar("constata", f"{nombre}: los grupos de avisos de dominio de las variantes llegan evaluados a la fase C, la ficha y el informe",
              set(var.get("avisos_de_dominio_variantes") or {}) == {a.get("id") for a in gv if isinstance(a, dict)}
              and set((fi.get("configuracion_economica") or {}).get("avisos_de_dominio_variantes") or {}) == set(var.get("avisos_de_dominio_variantes") or {})
              and "Avisos de dominio en las variantes calculadas" in leer(os.path.join(c, "informe.md")))
    aud = leer(os.path.join(c, "auditoria.md"))
    ult = (st.get("solicitudes_auditoria") or [{}])[-1]
    m_mat, m_sol = re.search(r"^Material auditado: (\S+)", aud, re.M), re.search(r"^Solicitud de auditoría: (\S+)", aud, re.M)
    comprobar("constata", f"{nombre}: auditoría ligada a la solicitud vigente y al material vigente (los identificadores coinciden con solicitud_auditoria.json y material_auditoria.json)",
              m_mat and m_sol and m_sol.group(1) == ult.get("id") == (j(os.path.join(c, "solicitud_auditoria.json")) or {}).get("id")
              and m_mat.group(1) == mat.get("id") == st.get("material_auditoria") and ult.get("respuesta_sha256") == sha(os.path.join(c, "auditoria.md")),
              f"{m_sol.group(1) if m_sol else None}/{ult.get('id')} · {m_mat.group(1) if m_mat else None}/{mat.get('id')}")
    import cierre_v2 as CIE
    import pipeline as PIPE
    mv = CIE.motivo_vigencia(c, PIPE.Pipeline.veredicto_auditoria)
    comprobar("reejecuta", f"{nombre}: cierre_v2.motivo_vigencia da la salida oficial por vigente (ficha, informe, cierre registrado y aprobación del material)", mv is None, str(mv)[:200])
    ant = [os.path.join(r, f) for r, _d, fs in os.walk(os.path.join(os.path.dirname(c), "antecedentes")) for f in fs if f == "auditoria.md"]
    ant += [os.path.join(r, f) for r, _d, fs in os.walk(os.path.join(c, "historial_cierres")) for f in fs if f.startswith("auditoria")]
    comprobar("constata", f"{nombre}: la auditoría vigente no es ninguna de las apartadas ni de las archivadas ({len(ant)}), por huella",
              sha(os.path.join(c, "auditoria.md")) not in {sha(x) for x in ant})
    rep = j(os.path.join(os.path.dirname(c), "resultados", "replica_independiente.json")) or {}
    rtxt = os.path.join(os.path.dirname(c), "resultados", "replica_independiente.json")
    libro_ev = os.path.join(c, "recalc", f"{emp}_v63_evaluada.xlsx")
    comprobar("constata", f"{nombre}: el registro de la réplica es posterior al libro evaluado final recalculado",
              os.path.exists(rtxt) and os.path.exists(libro_ev) and os.path.getmtime(rtxt) >= os.path.getmtime(libro_ev))
    comprobar("constata", f"{nombre}: réplica independiente de los libros finales (sin fórmulas de la hoja nueva): todos los casos coinciden",
              bool(rep.get("n_casos")) and rep.get("n_pasan") == rep.get("n_casos") == rep.get("n_calculados"), f"{rep.get('n_pasan')} de {rep.get('n_casos')}")
    return st


def main():
    print("1. ALCANCE DE LOS CAMBIOS (frente a la 4.12)")
    m412 = manifiesto(os.path.join(EXP, "reproduccion", "MANIFIESTO_SHA256_4_12.txt"))
    act = arbol()
    cambiados = {p for p in m412 if p in act and act[p] != m412[p]}
    comprobar("constata", "los archivos de la 4.12 que cambian son exactamente los declarados", cambiados == CAMBIADOS_FRENTE_A_4_12,
              f"de más {sorted(cambiados - CAMBIADOS_FRENTE_A_4_12)[:5]} · sin cambiar {sorted(CAMBIADOS_FRENTE_A_4_12 - cambiados)[:5]}")
    desaparecidos = [p for p in m412 if p not in act and p != "MANIFIESTO_SHA256.txt"]
    comprobar("constata", "ningún archivo de la 4.12 desaparece", not desaparecidos, str(desaparecidos[:5]))
    nuevos = [p for p in act if p not in m412]
    fuera = [p for p in nuevos if not p.startswith(NUEVOS_PERMITIDOS)]
    comprobar("constata", "los archivos nuevos están en el expediente 4.13, en la V6.4.1 o son los dos nuevos declarados (estructura_json.py y la configuración V6.4.1)", not fuera, str(fuera[:5]))
    for pref, nombre in (("personaje_v2/empresas_v2/", "originales de personaje_v2/empresas_v2/"), ("personaje_v2/empresas_v2_correcciones/", "expedientes y entregas anteriores"),
                         ("v6/", "plantillas, referencias y scripts de v6/"), ("contrastes/", "contrastes de entregas anteriores")):
        lista = [p for p in m412 if p.startswith(pref)]
        comprobar("constata", f"{nombre}: {len(lista)} archivos con la huella de la 4.12", lista and all(act.get(p) == m412[p] for p in lista))

    print("\n2. PLANTILLAS (V6.3, V6.4 y V6.4.1)")
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.3.txt"], cwd=os.path.join(RAIZ, "v6"))
    comprobar("reejecuta", "V6.3: entregables y referencia con sus SHA-256", rc == 0, out[-200:])
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.4_experimental.txt"], cwd=V64)
    comprobar("reejecuta", "V6.4 experimental: plantilla y referencia con su huella (sin cambios)", rc == 0, out[-200:])
    rc, out = run(["sha256sum", "-c", "referencia/SHA256_entregables_V6.4.1_experimental.txt"], cwd=V641)
    comprobar("reejecuta", "V6.4.1 experimental: plantilla y referencia NUEVAS con su huella", rc == 0, out[-200:])
    pl64 = os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx")
    pl641 = os.path.join(V641, "entregables", "Plantilla_V6.4.1_experimental.xlsx")
    rc, out = run([sys.executable, "-I", "-B", os.path.join(V641, "scripts", "verificar_v64.py"), pl641, os.path.join(V641, "referencia", "referencia_V6.4.1_experimental.json")])
    comprobar("reejecuta", "verificar_v64.py (V6.4.1): la plantilla V6.4.1 es ÍNTEGRA con su referencia nueva", rc == 0 and "ÍNTEGRO" in out, out[-200:])
    nueva = os.path.join(TMP, "V641_reconstruida.xlsx")
    rc, out = run([sys.executable, "-I", "-B", os.path.join(V641, "scripts", "construir_v641_experimental.py"), pl64, nueva])
    import comparar_zip as CZ
    iguales, detalle = CZ.comparar(nueva, pl641) if rc == 0 else (False, out[-200:])
    comprobar("reejecuta", "la reconstrucción de la V6.4.1 desde la V6.4 tiene el mismo contenido, miembro a miembro, que la plantilla entregada", rc == 0 and iguales, str(detalle)[:200])
    cp = j(os.path.join(EXP, "resultados", "compatibilidad_v641.json")) or {}
    comprobar("constata", "compatibilidad: con el perímetro vacío o «Caja» y en heredado, la V6.4.1 da 0 celdas distintas de la V6.4, y la réplica de las bases no discrepa",
              all(((cp.get("casos") or {}).get(k) or {}).get("diferencias") == 0 for k in ("experimental_caja", "experimental_caja_explicita", "heredado"))
              and (cp.get("replica") or {}).get("discrepancias") == [])

    print("\n3. VERIFICADOR DEL PAQUETE Y BATERÍA")
    vp = leer(os.path.join(RAIZ, "verificar_paquete.sh"))
    m = re.search(r'"\$\{n_tot:-0\}" -ge (\d+) \]; then\s*\n\s*echo "\$linea"; echo "RESULTADO integración V6\.4', vp)
    comprobar("constata", "verificar_paquete.sh completa exige la batería de la V6.4 con al menos 195 pruebas y conserva las demás con sus mínimos",
              "test_integracion_v64.py" in vp and m is not None and int(m.group(1)) >= 195 and all(f"-ge {n}" in vp for n in (78, 103, 55, 28, 45)), (m.group(1) if m else "sin mínimo"))
    tv = leer(os.path.join(PV, "pruebas", "test_integracion_v64.py"))
    comprobar("constata", "la batería de la V6.4 tiene los grupos A–H (H: V6.4.1, cobertura y avisos agrupados) y las pruebas de la revisión interna",
              all(re.search(rf"def grupo_{g.lower()}\b", tv) for g in "ABCDEFGH") and "grupo_e_revision_413" in tv and "grupo_f_revision_413" in tv)
    def huellas_al_dia(txt):
        """(segunda revisión interna, S2) un registro de la ronda lleva líneas «huella <ruta> <sha>»: tienen que ser las de hoy."""
        hs = re.findall(r"^huella (\S+) ([0-9a-f]{64})$", txt, re.M)
        return bool(hs) and all(os.path.exists(os.path.join(RAIZ, r)) and sha(os.path.join(RAIZ, r)) == h for r, h in hs)
    lb = leer(os.path.join(EXP, "resultados", "bateria_completa_4_13.txt"))
    mm = re.search(r"(\d+)/(\d+) pruebas de integración V6\.4 PASAN", lb)
    # (ronda B) se acredita con lo que escribe verificar_paquete.sh: «RESULTADO GLOBAL: PASA», «rc=0» del registro y la V6.4 entera
    comprobar("constata", "la ronda final de verificar_paquete.sh completa está registrada y la batería de la V6.4 pasa entera",
              "RESULTADO GLOBAL: PASA" in lb and re.search(r"^rc=0$", lb, re.M) is not None and "FALLA" not in lb
              and mm is not None and mm.group(1) == mm.group(2) and huellas_al_dia(lb), (mm.group(0) if mm else "sin registro"))

    print("\n4. GUARDAS DE TIPOS ANTES DE LA VIGENCIA (§3)")
    st_ = leer(os.path.join(EXP, "resultados", "sonda_tipos_4_13.txt"))
    filas = [x for x in st_.splitlines() if re.match(r"^\S+\s+(pipeline|ficha|informe|resumen)\s+rc=", x)]
    # lo que no se retira está explicado (REGISTRO_PRUEBAS_4_13.md §3): la solicitud no es material; el registro de publicaciones
    # ilegible deja la retirada pendiente (código 5); el estado del pipeline como lista detiene cada vía con su motivo (6 o 3) sin
    # cambiar el material; ficha.json alterado (no es material) con ficha.py es la sustitución W-d (código 0, «NO es vigente»)
    def explicada(x):
        if x.startswith(("sol_lista", "pub_lista", "pub_publicaciones_dict")):
            return True
        if x.startswith("est_lista"):
            return re.search(r"rc=(6|3)\b", x) is not None
        if x.startswith("ficha_decision_texto") and " ficha " in x:
            return "rc=0" in x and "NO es vigente" in x
        return False
    no_ret = [x for x in filas if "retirada=NO" in x and not explicada(x)]
    comprobar("constata", f"sonda de tipos con el código final: {len(filas)} primeras llamadas sobre copias del piloto; toda alteración del material retira la aprobación sin excepción",
              len(filas) >= 96 and not no_ret and "EXCEPCIÓN" not in st_ and huellas_al_dia(st_), str(no_ret[:2]))
    pend = [x for x in filas if x.startswith(("pub_lista", "pub_publicaciones_dict"))]
    comprobar("constata", "registro de publicaciones ilegible: retirada pendiente visible (código 5) en las cuatro vías", pend and all("rc=5" in x for x in pend), str(pend[:2]))

    print("\n5. ACCIÓN PROVISIONAL Y FINAL (§4)")
    ss = leer(os.path.join(EXP, "resultados", "sonda_salto_4_13.txt"))
    reales = [x for x in ss.splitlines() if x.startswith(("cond_real", "bloq_real", "visc_real"))]
    contra = [x for x in ss.splitlines() if x.startswith(("cond_sin_protocolo", "cond_bloqueo"))]
    comprobar("constata", "contraejemplo del salto del protocolo: las fases C reales se aceptan y las cuatro alteraciones se rechazan o quedan sin protocolo",
              len(reales) == 3 and all("ACEPTA" in x for x in reales) and len(contra) == 4
              and all(("ACEPTA" not in x) or ("objetivo_sin_protocolo" in x) for x in contra) and huellas_al_dia(ss), (ss[-300:] if ss else "sin registro"))

    print("\n6. VISCOFAN: ACCIONES Y EVIDENCIA ACTIVA (§6)")
    cn = leer(os.path.join(EXP, "fuentes", "CONCILIACION_ACCIONES_VISCOFAN_4_13.md"))
    comprobar("constata", "conciliación de acciones: las cifras de la nota 20, la circulación de cierre y el antecedente de la etapa 1 (R7)",
              all(x in cn for x in ("45.656.226", "45.479.209", "45.993.399", "Antecedente de la etapa 1")))
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(VIS, "Viscofan_v63_datos.xlsx"), read_only=True, data_only=True)
    cm = wb["Control maestro"]
    activas = []
    for row in cm.iter_rows(values_only=True):
        t = " | ".join(str(x) for x in row if x is not None)
        if re.search(r"Análisis!C(37|41|42|55|57)\b|Análisis!D4\b|^Periodos", t):
            activas.append(t)
    # (segunda revisión interna, S1) la nota de C42 nombra el dato sustituido como antecedente («Sustituye al 9,9 de la etapa 1 (…)»): es
    # legítima y no es evidencia; se busca en el resto de la fila (período, fuente, literal) y en la nota antes de «Sustituye a»
    def sin_antecedente(t):
        return re.sub(r"\(4\.13\) Sustituye al?[^|]*", "", t)
    malas = [t[:80] for t in activas if any(x in sin_antecedente(t) for x in TEXTOS_RETIRADOS)]
    comprobar("constata", "evidencia activa de C37, C41, C42, C55, C57, D4 y la lista de períodos sin los textos de la etapa 1 que contradicen las entradas (la nota de antecedente de C42 aparte)", activas and not malas, str(malas[:2]))
    f42 = next((t for t in activas if "Análisis!C42" in t), "")
    comprobar("constata", "la fila de C42 declara las fechas de las entradas (precio del 3-nov-2026, balance a 31-dic-2025) y el antecedente sustituido",
              "3-nov-2026" in f42 and "31-dic-2025" in f42 and "Sustituye al 9,9" in f42)
    an = wb["Análisis"]
    comprobar("constata", "N = 45,479209 con su concepto (media «diluida» publicada y contradictoria) y C42 recalculado sobre la base de 2025",
              abs((an["C55"].value or 0) - 45.479209) < 1e-9 and abs((an["C42"].value or 0) - 9.47) < 1e-9
              and any("contradice" in t.lower() or "contradictoria" in t.lower() for t in activas if "C55" in t))
    al = j(os.path.join(EXP, "resultados", "alternativas_acciones_viscofan.json")) or {}
    comprobar("constata", "alternativas de acciones sobre el libro vigente del expediente 4.13 (R10): reproducen el caso activo",
              al.get("reproduce_el_caso_activo") is True and "2026-11_Vidrala_ensayo_4_13" in (al.get("libro") or "")
              and abs((al.get("precio_si_activo") or 0) - ((j(os.path.join(VIS, "precio.json")) or {}).get("precio_si") or 1)) <= 1e-9)

    print("\n7. PERÍMETRO DE LA INVERSIÓN Y RÉPLICA (§7)")
    ca = j(os.path.join(EXP, "resultados", "conciliacion_arrendamientos_viscofan.json")) or {}
    comprobar("constata", "conciliación de arrendamientos 2021–2025 sin errores de lectura, con las líneas de las frases de altas corregidas (R11)",
              ca and ca.get("errores") == [] and not any(o.get("error") for o in ca.get("observaciones") or [])
              and all(o.get("linea") != 2373 for o in ca.get("observaciones") or []) and any(o.get("linea") == 2374 for o in ca.get("observaciones") or []))
    vv = {x.get("clave"): x for x in (j(os.path.join(VIS, "configuracion_v64_variantes.json")) or {}).get("variantes") or []}
    comprobar("constata", "Viscofan: el otro perímetro y los extremos de θ (0 y 1) calculados como variantes, con θ = 0,5 como punto de cálculo",
              {"perimetro_alternativo", "perimetro_alternativo_parametro_minimo", "perimetro_alternativo_parametro_maximo", "parametro_minimo", "parametro_maximo"} <= set(vv))
    dp = leer(os.path.join(EXP, "viscofan", "resultados", "dominios_perimetro.md"))
    comprobar("constata", "dominios del perímetro: la cota de SRF con NIIF 16 (1,2011) se calcula sobre su base, no se traslada la de «Caja» (1,1413)", "1,2011" in dp and "1,1413" in dp)
    conf_v = j(os.path.join(VIS, "configuracion_economica.json")) or {}
    comprobar("constata", "naturaleza de la configuración de Viscofan con las bases del perímetro NIIF 16 (R5)", "64,923" in conf_v.get("naturaleza", "") and "1,2011" in conf_v.get("naturaleza", ""))
    rm = j(os.path.join(VIS, "referencias_mecanicas.json")) or {}
    comprobar("constata", "referencia mecánica del S2C anclada en el S2C histórico del perímetro NIIF 16 (B155; R6)", "s2c_perimetro_niif16_B155" in json.dumps(rm))

    print("\n8. INTERPRETACIONES ECONÓMICAS DE VIDRALA (§8)")
    ce = leer(os.path.join(EXP, "CORRECCIONES_ECONOMICAS_VIDRALA_4_13.md"))
    ct = j(os.path.join(EXP, "resultados", "crecimiento_terminal_vidrala.json")) or {}
    comprobar("constata", "Q-ROIC1 con la condición de la 4.9, r_op frente a r personal calculado y la mezcla fijo/circulante con sus denominadores",
              "Q-ROIC1" in ce and "8,689151674" in ce and "530,0" in ce and bool(ct))

    print("\n9. EXPEDIENTES FINALES")
    import configuracion_economica as CE
    st_c = expediente_real(COND, "Vidrala condicionado", "V6.4 experimental", os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx"))
    st_b = expediente_real(BLOQ, "Vidrala bloqueo", "V6.4 experimental", os.path.join(V64, "entregables", "Plantilla_V6.4_experimental.xlsx"))
    st_v = expediente_real(VIS, "Viscofan", "V6.4.1 experimental", pl641)
    pc, pb = j(os.path.join(COND, "configuracion_economica.json")) or {}, j(os.path.join(BLOQ, "configuracion_economica.json")) or {}
    comprobar("constata", "las dos copias de Vidrala difieren SOLO en el protocolo del objetivo: misma configuración económica",
              pc.get("protocolo_objetivo") == "objetivo_condicionado" and pb.get("protocolo_objetivo") == "bloqueo_del_objetivo" and CE.celdas(pc) == CE.celdas(pb))
    auds = [leer(os.path.join(c, "auditoria.md")) for c in (COND, BLOQ, VIS)]
    comprobar("constata", "no se reutiliza una aprobación: tres auditorías distintas y las anteriores apartadas como antecedentes",
              all(auds) and len(set(auds)) == 3 and all(os.path.isdir(os.path.join(os.path.dirname(c), "antecedentes")) for c in (COND, BLOQ, VIS)))
    comprobar("constata", "estados acordes al protocolo: condicionado concluido · esperar; bloqueo pendiente_de_datos sin acción",
              st_c.get("estado_analisis") == "concluido" and st_b.get("estado_analisis") == "pendiente_de_datos"
              and (j(os.path.join(BLOQ, "ficha.json")) or {}).get("decision", {}).get("accion") is None)
    rel = leer(os.path.join(EXP, "resultados", "relevos_agentes_4_13.md"))
    comprobar("constata", "relevos a agentes reales registrados (fases A, B y C de Viscofan, fases C de Vidrala y auditorías)",
              all(x in rel for x in ("viscofan fase A", "viscofan fase B", "viscofan fase C", "vidrala_condicionado fase C", "vidrala_bloqueo fase C", "auditoría")))

    print("\n10. REVISIÓN INTERNA, PROPUESTA Y DOCUMENTACIÓN")
    ri = leer(os.path.join(EXP, "revision_interna", "REVISION_INTERNA_4_13.md"))
    ri2 = leer(os.path.join(EXP, "revision_interna", "REVISION_INTERNA_4_13_SEGUNDA.md"))
    comprobar("constata", "las dos revisiones internas en contexto separado presentes y declaradas como internas (R1–R18 y S1–S14)",
              "R1" in ri and "R18" in ri and "intern" in ri.lower() and "S1" in ri2 and "S14" in ri2 and "intern" in ri2.lower())
    pj = j(os.path.join(EXP, "propuestas", "propuesta_humana_4_13.json")) or {}
    decs = pj.get("decisiones") or []
    comprobar("constata", "propuesta en tres grupos (política de salida, elecciones por empresa, ampliaciones), con recomendación, alternativas, evidencia y efectos, y firmas vacías",
              decs and {d.get("grupo") for d in decs} == {"política de salida", "elección económica por empresa", "ampliación futura"}
              and all(d.get("recomendacion") and d.get("alternativas") and d.get("evidencia") and d.get("efectos") for d in decs)
              and all(d.get("decision") is None and d.get("fecha") is None and d.get("decidido_por") is None for d in decs))
    efe = " ".join(d.get("efectos") or "" for d in decs)
    fmt = lambda x: f"{x:,.2f}".replace(",", " ").replace(".", ",").replace(" ", ".")  # noqa: E731
    pv_, pc_ = (j(os.path.join(VIS, "precio.json")) or {}), (j(os.path.join(COND, "precio.json")) or {})
    comprobar("constata", "las cifras de efecto de la propuesta incluyen los precios de Sí de las activas finales (leídos de precio.json)",
              fmt(pv_.get("precio_si") or 0) in efe and fmt(pc_.get("precio_si") or 0) in efe)
    comprobar("constata", "VERSION, CONTINUIDAD.md y PROMPT_NUEVA_VENTANA.md describen la 4.13",
              "entrega 4.13" in leer(os.path.join(RAIZ, "VERSION")) and "entrega 4.13" in leer(os.path.join(RAIZ, "CONTINUIDAD.md"))
              and "munger_v2_r1_entrega4.13_fiabilidad_motor_B_y_conciliacion_economica.zip" in leer(os.path.join(RAIZ, "PROMPT_NUEVA_VENTANA.md")))
    inf = leer(os.path.join(EXP, "INFORME_INTEGRACION_4_13.md"))
    comprobar("constata", "informe integrado con las cuatro separaciones (integridad, reproducción, fundamento económico, aptitud) y el estado de cada hallazgo externo",
              all(x in inf for x in ("Integridad técnica", "Reproducción numérica", "Fundamento económico", "Aptitud de uso")) and inf.count("| E") >= 11)
    comprobar("constata", "guía de uso actualizada para la 4.13 y registros de la entrega y de pruebas presentes",
              "4.13" in leer(os.path.join(PV, "GUIA_RECORRIDO_SUPERVISADO.md")) and all(os.path.exists(os.path.join(EXP, f)) for f in ("REGISTRO_ENTREGA_4.13.md", "REGISTRO_PRUEBAS_4_13.md", "REGISTRO_AVANCE_4_13.md")))
    nuevas = sorted(p for p, t in cachés().items() if CACHÉS_AL_EMPEZAR.get(p) != t)
    comprobar("constata", "el control no escribe ningún .pyc en el árbol (revisión interna R13 y S2; las cachés previas no son suyas y el ZIP las excluye)",
              not nuevas, ", ".join(os.path.relpath(p, RAIZ) for p in nuevas[:3]))
    print(f"\nRESULTADO: {N_OK} de {N_T} comprobaciones cumplen ({TIPOS['reejecuta']} reejecutan, {TIPOS['constata']} constatan).")
    return 0 if N_OK == N_T else 1


if __name__ == "__main__":
    sys.exit(main())
