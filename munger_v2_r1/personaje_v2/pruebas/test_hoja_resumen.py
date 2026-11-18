#!/usr/bin/env python3
"""Batería de la hoja resumen en lenguaje llano (scripts/hoja_resumen.py), ronda 1 de su revisión crítica. Usa LibreOffice.

Cada caso nuevo lleva el hallazgo que cubre (H1 … H14 de /home/user/e_work/revision_hoja/REVISION_HOJA.md); los de los hallazgos ALTA y
MEDIA fallan con la versión revisada (ef93699) y pasan con la corregida.

Trabaja sobre COPIAS de expedientes cerrados existentes (los originales no cambian; se comprueba al final):
  - Vidrala 4.10.1 (V6.3, motor B, concluido · Vigilar · esperar, cierre vigente): el ejemplo V6.3 (Hermès no es vigente);
  - Vidrala 4.14 (V6.4, objetivo condicionado y provisional, aptitud_de_uso);
  - Viscofan 4.14 (V6.4.1, motor B, aviso A2: la tasa del análisis por debajo de la mínima de la hoja de cálculo);
  - Elis 4.14 (V6.3, motor A, pendiente_de_datos, precio de Sí «no utilizable») y Vidrala 4.13 bloqueo (objetivo bloqueado);
  - Hermès (empresas_v2: sin cierre registrado, NO vigente para la vía oficial);
  - una empresa sintética V6.3.1 F1 cerrada con el pipeline real y los agentes simulados (como P6 de prueba_pipeline_v631.py), con la
    declaración F1 cambiada después del cierre y el pipeline relanzado con «--desde 12».

LibreOffice: hoja_resumen.py toma el cerrojo común en cada recálculo y esta batería lo toma alrededor de cada ejecución del pipeline.
NO envolver esta batería en flock del mismo cerrojo; si ya se tiene (verificar_paquete.sh bajo flock), exportar
HOJA_RESUMEN_CERROJO_YA_TOMADO=1 y no se toma otra vez.

Uso (desde personaje_v2/): python3 -B pruebas/test_hoja_resumen.py
"""
import contextlib
import fcntl
import io
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAIZ = os.path.dirname(PV)
SC = os.path.join(PV, "scripts")
sys.path.insert(0, SC)
sys.dont_write_bytecode = True
import hoja_resumen as H  # noqa: E402
import precio_de_si as PS  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import pipeline as PIPE  # noqa: E402

RES = []
YA_TOMADO = os.environ.get("HOJA_RESUMEN_CERROJO_YA_TOMADO") == "1"
LOCK = getattr(H, "LOCK_DEFECTO", "/home/user/e_work/libreoffice.lock")


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    detalle = " / ".join(x.strip() for x in str(detalle).splitlines() if x.strip())
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def seguro(fn, *a, **k):
    """Ejecuta una comprobación y devuelve su valor; una excepción (p. ej., la función no existe en la versión revisada) es False."""
    try:
        return fn(*a, **k)
    except Exception as e:  # noqa: BLE001
        print(f"      (excepción: {type(e).__name__}: {str(e)[:160]})")
        return False


def huellas_dir(d):
    out = {}
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = H.sha256(p)
    return out


def correr(args):
    r = subprocess.run([sys.executable, "-I", os.path.join(SC, "hoja_resumen.py")] + args, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def leer(p):
    return open(p, encoding="utf-8").read() if os.path.isfile(p) else ""


def jload(p):
    return json.load(open(p, encoding="utf-8"))


@contextlib.contextmanager
def cerrojo():
    if YA_TOMADO:
        yield
        return
    os.makedirs(os.path.dirname(LOCK) or ".", exist_ok=True)
    with open(LOCK, "a") as f:
        fcntl.flock(f, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(f, fcntl.LOCK_UN)


def en_proceso(fn, *a, **k):
    """Llama a una función de hoja_resumen en este proceso y devuelve (código, salida)."""
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        try:
            rc = fn(*a, **k)
        except Exception as e:  # noqa: BLE001
            rc = f"excepción {type(e).__name__}: {e}"
    return rc, buf.getvalue()


AFIRMA_APTO = re.compile(r"(?<!no )(?<!no es )apt[oa] para (?:el )?dinero real", re.I)
CORR = os.path.join(PV, "empresas_v2_correcciones")
EXPEDIENTES = {
    "V6.3_Vidrala_4_10_1": os.path.join(CORR, "2026-11_Vidrala_ensayo_4_10_1", "Vidrala"),
    "V6.4_Vidrala_4_14": os.path.join(CORR, "2026-11_Vidrala_ensayo_4_14", "vidrala_decisiones", "Vidrala"),
    "V6.4.1_Viscofan_4_14": os.path.join(CORR, "2026-11_Vidrala_ensayo_4_14", "viscofan_decisiones", "Viscofan"),
    "Elis_4_14": os.path.join(CORR, "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis"),
    "Vidrala_4_13_bloqueo": os.path.join(CORR, "2026-11_Vidrala_ensayo_4_13", "vidrala_bloqueo", "Vidrala"),
    "Hermes": os.path.join(PV, "empresas_v2", "Hermes"),
}

# ------------------------------------------------------------------------------------------------ unidades: frases y limpieza
paso("frases: no corta en «p. 104», «EE. UU.» ni iniciales; corta ante «2)»",
     H.frases("W. Kurtz manda. EE. UU. pesa [ES, PDF p. 104] mucho. 1) Uno. 2) Dos.") == ["W. Kurtz manda.", "EE. UU. pesa [ES, PDF p. 104] mucho.", "1) Uno.", "2) Dos."])
paso("limpiar: quita corchetes de fuente y referencias a celdas, conserva cifras y paréntesis con contenido",
     H.limpiar("Gana el 13,8 % (13,8 % frente al 9,3 %; Historia C55, Palancas H18) y vale 241 € (B78:D78) [ES, PDF p. 9].")
     == "Gana el 13,8 % (13,8 % frente al 9,3 %) y vale 241 €.")
paso("limpiar: un elemento de referencia dentro de una parte se quita («(9,4 %, Historia C33:D33)» → «(9,4 %)»)",
     H.limpiar("fue la tasa (9,4 %, Historia C33:D33) sin") == "fue la tasa (9,4 %) sin")
paso("limpiar: conserva las citas de Munger y los paréntesis con valores («(C33 = −1,35)», «(p(MALO) a 0,3)»)",
     H.limpiar("«x» (AIWTK p.36; HIM). Sin deuda (C33 = −1,35) y (p(MALO) a 0,3).") == "«x» (AIWTK p.36; HIM). Sin deuda (C33 = −1,35) y (p(MALO) a 0,3).")
paso("limpiar: quita el ordinal inicial «1)»", H.limpiar("1) El ROIC ya baja.") == "El ROIC ya baja.")
paso("H6 · limpiar: «(Historia filas 29 y 33)» es una referencia y se quita",
     H.limpiar("El margen subió (Historia filas 29 y 33) y bajó.") == "El margen subió y bajó.")
paso("H12 · una tasa no entera no se redondea a la de al lado (0,085 → «8,5 %»; 0,09 → «9 %»)",
     seguro(lambda: H.tasa_txt(0.085) == "8,5 %" and H.tasa_txt(0.09) == "9 %" and H.tasa_txt(0.1) == "10 %"))
fc_falso = {"celdas": {"B101": "Uno dos tres cuatro cinco seis. Pero siete ocho nueve diez once doce. Trece catorce quince dieciséis diecisiete.",
                       "B102": "Breve. Ocho nueve diez once doce trece. Riesgo concreto con deuda alta y metas incumplidas. Final del riesgo."},
            "cambiaria_de_cubo": {"a_no": "Catorce quince dieciséis."}}
pq = seguro(lambda *a, **k: getattr(H, "seleccionar_por_que")(*a, **k), fc_falso) or {}
paso("H5 · la tesis y la tesis inversa se muestran ENTERAS (también la salvedad «Pero…» y el riesgo concreto)",
     [e["indice"] for e in pq.get("tesis") or []] == [0, 1, 2] and [e["indice"] for e in pq.get("tesis_inversa") or []] == [0, 1, 2, 3]
     and any(e["texto"].startswith("Pero") for e in pq.get("tesis") or []))
todas_f = (pq.get("tesis") or []) + (pq.get("tesis_inversa") or [])
paso("verificar_origen_frases: una frase con una cifra añadida, un campo inexistente o un índice fuera de rango se rechazan",
     bool(todas_f) and H.verificar_origen_frases(todas_f, fc_falso) == []
     and H.verificar_origen_frases([dict(todas_f[0], texto=todas_f[0]["texto"] + " 42")], fc_falso)
     and H.verificar_origen_frases([dict(todas_f[0], campo="B999")], fc_falso)
     and H.verificar_origen_frases([dict(todas_f[0], indice=7)], fc_falso))
preds_ok = [{"texto": "Las ventas de 2027 crecerán", "fecha": "2028-03-31", "prob": 0.7}] * 3
paso("H5 · contenido mínimo: «a No» con «…», tesis vacía o menos de tres predicciones con fecha y probabilidad → faltas",
     seguro(lambda: H.contenido_minimo(pq, {"cambiaria_de_cubo.a_no": H.texto_con_origen({"cambiaria_de_cubo": {"a_no": "…"}}, "cambiaria_de_cubo.a_no")}, preds_ok, {"cubo": "Sí"})
            and H.contenido_minimo({"tesis": [], "tesis_inversa": pq.get("tesis_inversa")}, {"cambiaria_de_cubo.a_no": H.texto_con_origen(fc_falso, "cambiaria_de_cubo.a_no")}, preds_ok, {"cubo": "Sí"})
            and H.contenido_minimo(pq, {"cambiaria_de_cubo.a_no": H.texto_con_origen(fc_falso, "cambiaria_de_cubo.a_no")}, preds_ok[:2], {"cubo": "Sí"})
            and not H.contenido_minimo(pq, {"cambiaria_de_cubo.a_no": H.texto_con_origen(fc_falso, "cambiaria_de_cubo.a_no")}, preds_ok, {"cubo": "Sí"})))
plano = [{"r": r, "precio_si": 757.05, "ponderado": 800.0, "r_operativa_C15": 0.09} for r in (0.08, 0.09, 0.10)]
paso("H10 · un «recálculo» que no recalcula (mismas cifras con cualquier tasa) se detecta",
     bool(seguro(lambda *a, **k: getattr(H, "comprobar_recalculo")(*a, **k), plano)) and seguro(lambda *a, **k: getattr(H, "comprobar_recalculo")(*a, **k), [dict(f, precio_si=f["precio_si"] - 100 * f["r"], ponderado=800 - 100 * f["r"],
                                                                                         r_operativa_C15=f["r"]) for f in plano]) is None)

# --- H1 y H3 sin LibreOffice: el veredicto y la aptitud salen de la ficha
base_f = {"moneda": "EUR", "cubo": "Vigilar", "estado_analisis": "concluido", "decision": {"accion": "esperar", "precio_objetivo": 18.12}}
precio_cumple = {"precio_si": 18.12, "precio": 16.0, "zona": "cumple_regla_k", "ponderado": 20.0}
v_inv = seguro(lambda *a, **k: getattr(H, "veredicto")(*a, **k), dict(base_f, estado_analisis="pendiente_de_investigacion", decision={"accion": None, "precio_objetivo": None},
                                 causa_si_no_concluido={"detalle": "incertidumbre no acotada"}), precio_cumple, {}) or {}
paso("H1 · pendiente_de_investigacion con el precio por debajo del precio de Sí: «Sin conclusión de compra», sin precio de compra y con la causa",
     "Sin conclusión de compra" in str(v_inv.get("conclusion")) and v_inv.get("precio_compra") is None
     and "no da precio de compra" in str(v_inv.get("linea_precio")) and v_inv.get("causa") == "incertidumbre no acotada")
v_no = seguro(lambda *a, **k: getattr(H, "veredicto")(*a, **k), dict(base_f, cubo="No", decision={"accion": "descartar", "precio_objetivo": None}), precio_cumple, {}) or {}
paso("H1 · «No · descartar» con zona favorable: la conclusión es «La descarta» y no hay precio de compra",
     str(v_no.get("conclusion", "")).startswith("La descarta.") and v_no.get("precio_compra") is None)
v_bl = seguro(lambda *a, **k: getattr(H, "veredicto")(*a, **k), dict(base_f, estado_analisis="pendiente_de_datos", decision={"accion": None, "precio_objetivo": None},
                                objetivo={"estado_del_objetivo": "bloqueado", "precio_objetivo_emitido": None}), precio_cumple, {}) or {}
paso("H1 · objetivo bloqueado: la ficha no da precio de compra y la cifra de la hoja de cálculo se presenta como tal, con el motivo",
     v_bl.get("precio_compra") is None and "objetivo está bloqueado" in str(v_bl.get("linea_precio")))
v_f1 = seguro(lambda *a, **k: getattr(H, "veredicto")(*a, **k), dict(base_f, motor_a_f1={"utilizable_para_conclusion": False}), precio_cumple, {}) or {}
paso("H1/H3 · ficha concluido con motor_a_f1 no utilizable: sin conclusión y sin precio de compra",
     v_f1.get("concluye") is False and v_f1.get("precio_compra") is None)
apt_l, apt_d = seguro(lambda *a, **k: getattr(H, "aptitud")(*a, **k), {"aptitud_de_uso": {"apto_para_dinero_real": True, "version": "9.9", "caracter": "experimental"},
                                   "verificacion_entradas": {"apto_por_entradas": False, "resumen": {"universo": 309, "comprobadas_universo": 0, "motivo": "ninguna entrada verificada"}},
                                   "motor_a_f1": {"rotulo": "motor A sin validar", "utilizable_para_conclusion": True}}, {}) or ([], {})
txt_apt = "\n".join(apt_l)
paso("H3 · aptitud: dice «no vale para decidir con dinero real», «datos de entrada verificados: no» y F1; nunca afirma «apto para dinero real»",
     "no vale para decidir con dinero real" in txt_apt and "verificados contra sus fuentes: **no**" in txt_apt and "Motor A · F1" in txt_apt
     and not AFIRMA_APTO.search(txt_apt), txt_apt[:200])
apt_v, _ = seguro(lambda *a, **k: getattr(H, "aptitud")(*a, **k), {}, {}) or ([], {})
paso("H3 · sin ningún bloque de aptitud: «la ficha no dice nada sobre la aptitud; no se presume ninguna» (sin «es anterior a ese bloque»)",
     "no dice nada sobre la aptitud" in "\n".join(apt_v) and "anterior a ese bloque" not in "\n".join(apt_v))

# ------------------------------------------------------------------------------------------------ expedientes (copias)
tmp = tempfile.mkdtemp(prefix="test_hoja_")
originales = {n: huellas_dir(p) for n, p in EXPEDIENTES.items()}


def copia(nombre, sub=None):
    destino = os.path.join(tmp, sub or nombre, os.path.basename(EXPEDIENTES[nombre]))
    shutil.copytree(EXPEDIENTES[nombre], destino)
    return destino


def hoja_de(exp):
    return leer(os.path.join(exp, H.SALIDA_MD)), (jload(os.path.join(exp, H.SALIDA_JSON)) if os.path.isfile(os.path.join(exp, H.SALIDA_JSON)) else {})


def restaurar_apartada(exp):
    """Devuelve a su sitio la hoja que el programa apartó como NO_VIGENTE (para seguir probando sobre la misma copia)."""
    for n in ("hoja_resumen.NO_VIGENTE.md", "hoja_resumen.NO_VIGENTE.json"):
        if os.path.exists(os.path.join(exp, n)):
            os.replace(os.path.join(exp, n), os.path.join(exp, n.replace(".NO_VIGENTE", "")))


def seccion(md, titulo, siguiente="\n## "):
    return md.split(titulo, 1)[1].split(siguiente, 1)[0] if titulo in md else ""


try:
    # ============================== Vidrala 4.10.1 (V6.3, vigente): el caso completo
    exp = copia("V6.3_Vidrala_4_10_1")
    antes = huellas_dir(exp)
    rc, out = correr([exp, "--trabajo", tmp])
    md_p, js_p = os.path.join(exp, H.SALIDA_MD), os.path.join(exp, H.SALIDA_JSON)
    paso("V6.3 Vidrala 4.10.1 (cierre vigente): la hoja sale (código 0)", rc == 0 and os.path.isfile(md_p) and os.path.isfile(js_p), out.strip()[-200:])
    despues = huellas_dir(exp)
    paso("V6.3: no cambia ningún archivo del expediente; solo añade la hoja (y nada de copias temporales)",
         not [p for p in antes if despues.get(p) != antes[p]] and sorted(set(despues) - set(antes)) == [H.SALIDA_JSON, H.SALIDA_MD])
    md, t = hoja_de(exp)
    ficha = jload(os.path.join(exp, "ficha.json"))
    precio = jload(os.path.join(exp, "precio.json"))
    fase_c = jload(os.path.join(exp, "fase_c.json"))
    mon = ficha.get("moneda")
    v = t.get("veredicto") or {}
    paso("V6.3: el veredicto de la hoja es el de la ficha (estado, cubo, acción, precio de compra = decision.precio_objetivo)",
         v.get("estado_analisis") == ficha["estado_analisis"] and v.get("cubo") == ficha["cubo"] and v.get("accion") == ficha["decision"]["accion"]
         and v.get("precio_compra") == ficha["decision"]["precio_objetivo"] and v.get("concluye") is True)
    paso("H1 · V6.3: «Qué concluye: No comprar ahora; esperar a mejor precio» y «a 66,52 € por acción o menos»",
         "No comprar ahora; esperar a mejor precio." in md and f"a {H.dinero(ficha['decision']['precio_objetivo'], mon)} por acción o menos" in md)
    paso("H6 · cabecera llana: «Resumen para estudiar. No es una recomendación de compra ni un documento oficial» y la fecha de la hoja",
         "Resumen para estudiar. No es una recomendación de compra ni un documento oficial." in md and "Hecho el " in md.split("##", 1)[0])
    paso("H3 · V6.3 sin bloques de aptitud: «no vale para decidir con dinero real», «no se presume ninguna» y ninguna frase «es anterior a ese bloque»",
         "Experimental: no vale para decidir con dinero real." in md and "no se presume ninguna" in md and "anterior a ese bloque" not in md
         and not AFIRMA_APTO.search(md))
    # texto llano
    pq = t.get("por_que") or {}
    n_t, n_ti = len(H.frases(fase_c["celdas"]["B101"])), len(H.frases(fase_c["celdas"]["B102"]))
    paso("H5 · V6.3: la tesis y la tesis inversa están enteras (todas sus frases), cada una en la página",
         len(pq.get("tesis") or []) == n_t and len(pq.get("tesis_inversa") or []) == n_ti
         and all(e["texto"] in md for e in (pq.get("tesis") or []) + (pq.get("tesis_inversa") or [])), f"{n_t} + {n_ti} frases")
    todas = seguro(lambda *a, **k: getattr(H, "frases_de_la_traza")(*a, **k), t) or []
    paso("ninguna frase del personaje carece de origen (frase exacta de fase_c.json, limpieza reproducible, sin cifras nuevas)",
         len(todas) >= 6 and not H.verificar_origen_frases(todas, fase_c))
    rc2, out2 = correr([exp, "--verificar-origen"])
    paso("V6.3: --verificar-origen comprueba el origen (código 0)", rc2 == 0 and "ORIGEN COMPROBADO" in out2, out2.strip()[-100:])
    t_mal = json.loads(json.dumps(t))
    if (t_mal.get("por_que") or {}).get("tesis"):
        t_mal["por_que"]["tesis"][1]["texto"] += " Subirá un 30 %."
    json.dump(t_mal, open(js_p, "w", encoding="utf-8"), ensure_ascii=False)
    rc3, out3 = correr([exp, "--verificar-origen"])
    paso("V6.3: una frase inventada en la traza se detecta (--verificar-origen, código 4)", rc3 == 4 and "SIN ORIGEN" in out3, out3.strip()[-120:])
    json.dump(t, open(js_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # rótulos de «lo que lo haría falso»
    paso("H6 · rótulos llanos: «Lo descartaría si…», «Lo compraría si…», «Lo dejaría por demasiado difícil si…», «Bajaría/Subiría el precio de Sí si…»",
         all(x in md for x in ("Lo descartaría si…", "Lo compraría si…", "Lo dejaría por demasiado difícil si…", "Bajaría el precio de Sí si…", "Subiría el precio de Sí si…"))
         and "Pasaría a **No**" not in md)
    # sensibilidad
    s = t.get("sensibilidad") or {}
    filas = {round(f["r"], 4): f for f in s.get("filas") or []}
    f9 = filas.get(0.09)
    paso("V6.3: tasas 7, 8, 9, 10 y 11 %, cada copia con su r leída en Análisis!C56 tras el recálculo",
         sorted(filas) == [0.07, 0.08, 0.09, 0.10, 0.11] and all(abs(f["C56_leida"] - f["r"]) < 1e-15 for f in s.get("filas") or []))
    paso("V6.3: al 9 % la copia reproduce EXACTAMENTE el precio de Sí de precio.json (y ponderado, zona, V, crecimiento implícito)",
         f9 is not None and all(f9[c] == precio[c] for c in ("precio_si", "ponderado", "zona", "V", "g_impl_actual")) and s.get("reproduce_oficial") is True)
    paso("V6.3: el precio de Sí y el ponderado bajan al subir la tasa, y el crecimiento que exige el precio sube",
         len(filas) == 5 and all(filas[a]["precio_si"] > filas[b]["precio_si"] and filas[a]["ponderado"] > filas[b]["ponderado"]
                                 and filas[a]["g_impl_actual"] < filas[b]["g_impl_actual"] for a, b in zip(sorted(filas), sorted(filas)[1:])))
    paso(f"V6.3: cada fila cuadra con la regla de la escalera (P* con k = {precio['k']}) y su zona",
         bool(filas) and all(abs(f["precio_si"] - min(PS.p_estrella(f["V"], precio["p"], precio["k"]), f["V"][1])) < 1e-9
                             and f["zona"] == PS.zona(f["precio"], f["V"][0] if f["V"][0] > 0 else None, f["precio_si"], f["ponderado"]) for f in filas.values()))
    # recálculo independiente al 10 %: copia propia, recalc.sh y lectura directa de las celdas con openpyxl
    if 0.10 in filas:
        import openpyxl
        from v63_xml import LibroV63
        libro = H.libro_evaluado(exp)
        d10 = os.path.join(tmp, "indep")
        os.makedirs(os.path.join(d10, "in"))
        L = LibroV63(libro)
        L.escribir_celdas({"Análisis!C56": 0.10})
        L.guardar(os.path.join(d10, "in", os.path.basename(libro)))
        with cerrojo():
            subprocess.run(["bash", os.path.join(SC, "recalc.sh"), os.path.join(d10, "in", os.path.basename(libro)), os.path.join(d10, "out"),
                            os.path.join(d10, "perfil")], capture_output=True, text=True)
        wb = openpyxl.load_workbook(os.path.join(d10, "out", os.path.basename(libro)), data_only=True, read_only=True)
        a = wb["Análisis"]
        V10, f10 = [a["B78"].value, a["C78"].value, a["D78"].value], filas[0.10]
        paso("V6.3: al 10 % las cifras coinciden con el libro recalculado de forma independiente (B78:D78, C83, C86)",
             V10 == f10["V"] and a["C83"].value == f10["ponderado"] and a["C86"].value == f10["C86_hoja"], f"{V10} vs {f10['V']}")
        wb.close()
        shutil.rmtree(d10, ignore_errors=True)
    tabla = seccion(md, "## Cuánto cambia el resultado")
    paso("V6.3: la tabla muestra las cifras redondeadas de cada fila y rotula la tasa del análisis",
         bool(filas) and all(H.dinero(f["precio_si"], mon) in tabla and H.dinero(f["ponderado"], mon) in tabla for f in filas.values())
         and "| 9 % (la del análisis) |" in tabla)
    paso("H12 · sin «Conclusión firme»: «Frente a la tasa, el resultado no cambia/cambia … no dice que el análisis sea seguro»",
         "firme" not in (tabla + seccion(md, "## Qué concluye el análisis")).lower() and "Frente a la tasa, el resultado" in tabla and "no dice que el análisis sea seguro" in tabla)
    paso("H7 · avisos junto a la tabla: la zona no es la conclusión, el escenario malo no es un suelo, regla experimental k = 3, lo demás se deja quieto",
         "no es la conclusión" in tabla and "no es un suelo" in tabla and "regla experimental" in tabla and "(k = 3)" in tabla
         and "no qué habría decidido el personaje con otra tasa" in tabla)
    paso("H7 · motor B: la tabla dice con qué tasa descuenta la hoja de cálculo en cada fila",
         "descuenta al" in tabla and "la hoja de cálculo la ajusta" in tabla)
    meta = jload(os.path.join(exp, "fase1_metadatos.json"))
    paso("H8 · «Precio usado en el análisis: 90,10 € (31 de diciembre de 2025)» con aviso de que no es el de hoy (más de 90 días antes del análisis)",
         f"**Precio usado en el análisis:** {H.dinero(precio['precio'], mon)} ({H.fecha_larga(meta['precio']['fecha'])})" in md
         and "días antes del análisis, no el de hoy" in md and "precio actual" not in (seccion(md, "## Qué concluye el análisis") + tabla).lower())
    paso("H6 · glosario con los términos de la página (precio de Sí, tasa, ROIC…) y sin referencias «Análisis!C56» ni «fase_c.json» antes del pie",
         "## Palabras que pueden no ser conocidas" in md and "**Precio de Sí:**" in md and "**Tasa:**" in md
         and "Análisis!C56" not in md.split("## Para comprobar esta hoja")[0] and "fase_c.json" not in md.split("## Para comprobar esta hoja")[0])
    preds = t.get("predicciones") or []
    paso("V6.3: tres predicciones de Palancas A38:C40 (fase C) con fecha y probabilidad, iguales a las de la ficha",
         len(preds) == 3 and all(pr["texto"] == ficha["predicciones"][i]["texto"] and pr["fecha"] == ficha["predicciones"][i]["fecha"]
                                 and pr["prob"] == ficha["predicciones"][i]["prob"] for i, pr in enumerate(preds))
         and all(H.fecha_larga(pr["fecha"]) in md and pr["texto"] in md for pr in preds))
    paso("V6.3: la hoja no parece una auditoría (sin «Material auditado», H2 no la aprueba) ni tiene línea «Veredicto:»",
         not CIE.parece_auditoria(md, PIPE.Pipeline.veredicto_auditoria) and not re.search(r"(?im)^[\s>*#_-]*veredicto[\s*_]*:", md))
    rc4, out4 = correr([exp, "--comprobar"])
    paso("V6.3: --comprobar da la hoja por vigente (código 0)", rc4 == 0 and "HOJA VIGENTE" in out4, out4.strip()[-120:])
    # H9: la página editada a mano
    md_bytes = open(md_p, "rb").read()
    open(md_p, "w", encoding="utf-8").write(md.replace("No comprar ahora; esperar a mejor precio.", "Compraría hoy. Apto para dinero real."))
    rc5, out5 = correr([exp, "--comprobar"])
    rc5b, out5b = correr([exp, "--verificar-origen"])
    paso("H9 · una edición a mano de hoja_resumen.md se detecta (--comprobar y --verificar-origen, código 4)",
         rc5 == 4 and "EDITADA" in out5 and rc5b == 4, (out5 + out5b).strip()[-160:])
    open(md_p, "wb").write(md_bytes)
    # H4: --comprobar no da por vigente una hoja cuyo json dice que no reproducía el precio de Sí
    js_bytes = open(js_p, "rb").read()
    t_nr = json.loads(js_bytes)
    t_nr.setdefault("sensibilidad", {})["reproduce_oficial"] = False
    open(js_p, "w", encoding="utf-8").write(json.dumps(t_nr, ensure_ascii=False, indent=1) + "\n")
    rc6, out6 = correr([exp, "--comprobar"])
    paso("H4 · --comprobar falla (código 4) si la hoja registra que no reproducía el precio de Sí de precio.json", rc6 == 4, out6.strip()[-120:])
    open(js_p, "wb").write(js_bytes)
    # H4: códigos 4 y 5 no escriben hoja (en este proceso, con la sensibilidad sustituida para no recalcular)
    falsa = [dict({c: precio.get(c) for c in ("precio_si", "ponderado", "zona", "V", "precio", "g_impl_actual")}, r=r, C56_leida=r) for r in (0.08, 0.09, 0.10)]
    respaldo = {n: getattr(H, n, None) for n in ("sensibilidad", "comprobar_recalculo", "reproduce_oficial", "verificar_origen_frases")}
    try:
        H.sensibilidad = lambda *a, **k: [dict(f) for f in falsa]
        H.comprobar_recalculo = lambda filas: None
        H.reproduce_oficial = lambda fila, precio: (False, {"precio_si": (1.0, 2.0)})
        rc7, out7 = en_proceso(H.generar, exp, exp, tmp, LOCK, [0.09])
        paso("H4 · código 5 (no reproduce el precio de Sí): no queda hoja_resumen.md y la anterior se aparta como NO_VIGENTE",
             rc7 == 5 and not os.path.exists(md_p) and not os.path.exists(js_p) and os.path.isfile(os.path.join(exp, "hoja_resumen.NO_VIGENTE.md")), str(rc7) + " " + out7.strip()[-120:])
        rc7b, _ = correr([exp, "--comprobar"])
        paso("H4 · después de un código 5, --comprobar no encuentra hoja vigente (código 4)", rc7b == 4)
        H.reproduce_oficial = respaldo["reproduce_oficial"]
        H.verificar_origen_frases = lambda frases_hoja, fase_c: ["frase sin origen (simulada)"]
        rc8, out8 = en_proceso(H.generar, exp, exp, tmp, LOCK, [0.09])
        paso("H4 · código 4 (frase sin origen): no se escribe hoja", rc8 == 4 and not os.path.exists(md_p), str(rc8) + " " + out8.strip()[-120:])
        H.verificar_origen_frases = respaldo["verificar_origen_frases"]
        H.contenido_minimo, cm0 = (lambda *a: ["la tesis está vacía (simulado)"]), getattr(H, "contenido_minimo", None)
        rc9, out9 = en_proceso(H.generar, exp, exp, tmp, LOCK, [0.09])
        paso("H5 · contenido mínimo incumplido: código 4 y no se escribe hoja", rc9 == 4 and not os.path.exists(md_p), str(rc9) + " " + out9.strip()[-120:])
        H.contenido_minimo = cm0
    finally:
        for n, f in respaldo.items():
            if f is not None:
                setattr(H, n, f)
    restaurar_apartada(exp)
    rc10, out10 = correr([exp, "--comprobar"])
    paso("(control) restaurada la hoja buena, --comprobar vuelve a darla por vigente", rc10 == 0, out10.strip()[-100:])
    # H2: la ficha cambia → no se genera y la hoja anterior se aparta
    fp = os.path.join(exp, "ficha.json")
    bytes_ficha = open(fp, "rb").read()
    open(fp, "wb").write(bytes_ficha + b"\n")
    rc11, out11 = correr([exp, "--comprobar"])
    paso("H2 · si la ficha cambia, --comprobar dice que la hoja ya no vale (código 4)", rc11 == 4 and ("NO VIGENTE" in out11 or "DESACTUALIZADA" in out11), out11.strip()[-120:])
    rc12, out12 = correr([exp, "--trabajo", tmp])
    paso("H2/H4 · con una ficha que no es la del cierre no se genera hoja (código 3) y la anterior se aparta como NO_VIGENTE",
         rc12 == 3 and not os.path.exists(md_p) and os.path.isfile(os.path.join(exp, "hoja_resumen.NO_VIGENTE.md")), out12.strip()[-140:])
    open(fp, "wb").write(bytes_ficha)
    # H2: fase_c.json cambiado después de la auditoría (A1/A6)
    restaurar_apartada(exp)
    fcp = os.path.join(exp, "fase_c.json")
    fc_bytes = open(fcp, "rb").read()
    fc2 = json.loads(fc_bytes)
    fc2["cambiaria_de_cubo"]["a_no"] = "Nada me haría pasar a No."
    json.dump(fc2, open(fcp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    rc13, out13 = correr([exp, "--comprobar"])
    rc14, out14 = correr([exp, "--trabajo", tmp])
    paso("H2 · fase_c.json cambiado después de la auditoría: --comprobar → 4 y la hoja no se genera (código 3, «el material cambió»)",
         rc13 == 4 and rc14 == 3 and "material cambió" in out14 and not os.path.exists(md_p), (out13 + " | " + out14).strip()[-200:])
    # H2 + decisión del coordinador: al retirar la aprobación, la hoja se archiva como NO VIGENTE
    restaurar_apartada(exp)
    motivo, archivo = CIE.asegurar_vigencia(exp, PIPE.Pipeline.veredicto_auditoria, None, None)
    arch_md = os.path.join(archivo or "", "hoja_resumen.NO_VIGENTE.md")
    paso("H2 · retirada oficial de la aprobación (asegurar_vigencia): la hoja se archiva con el antecedente como NO VIGENTE y sale del expediente",
         bool(archivo) and os.path.isfile(arch_md) and os.path.isfile(os.path.join(archivo, "HOJA_RESUMEN_NO_VIGENTE.json"))
         and not os.path.exists(md_p) and (jload(os.path.join(archivo, "RETIRADA.json")).get("hoja_resumen_no_vigente") or []),
         f"{(motivo or '')[:80]} · {archivo and os.path.relpath(archivo, exp)}")
    open(fcp, "wb").write(fc_bytes)
    rc15, out15 = correr([exp, "--trabajo", tmp])
    paso("H2 · restaurar fase_c.json no reactiva la aprobación retirada: la hoja no se genera (código 3)", rc15 == 3 and not os.path.exists(md_p), out15.strip()[-140:])

    # ============================== A4 y H13: sin cierre registrado, JSON mal formado, fase_c vacío (sin LibreOffice)
    exp = copia("V6.3_Vidrala_4_10_1", "A4")
    os.remove(os.path.join(exp, "cierre_vigente.json"))
    rc, out = correr([exp, "--trabajo", tmp])
    paso("H2 · A4: sin cierre_vigente.json la hoja no se genera (código 3)", rc == 3 and not os.path.exists(os.path.join(exp, H.SALIDA_MD)), out.strip()[-140:])
    exp = copia("V6.3_Vidrala_4_10_1", "H13")
    stp = os.path.join(exp, "estado_pipeline.json")
    open(stp, "w", encoding="utf-8").write(open(stp, encoding="utf-8").read()[:200])
    rc, out = correr([exp, "--trabajo", tmp])
    paso("H13 · un JSON truncado del expediente da código 3 con mensaje, sin traza de Python", rc == 3 and "Traceback" not in out and "estado_pipeline.json" in out, out.strip()[-140:])
    exp = copia("V6.3_Vidrala_4_10_1", "fase_c_vacia")
    open(os.path.join(exp, "fase_c.json"), "w").write("{}")
    rc, out = correr([exp, "--trabajo", tmp])
    paso("H2/H5 · fase_c.json = {}: no hay hoja (código 3: material cambiado), nunca una hoja vacía con «OK»", rc == 3 and not os.path.exists(os.path.join(exp, H.SALIDA_MD)), out.strip()[-120:])
    exp = copia("V6.3_Vidrala_4_10_1", "H11")
    lockp = os.path.join(tmp, "cerrojo_privado.lock")
    with open(lockp, "a") as fl:
        fcntl.flock(fl, fcntl.LOCK_EX)
        r11 = subprocess.run([sys.executable, "-I", os.path.join(SC, "hoja_resumen.py"), exp, "--trabajo", tmp, "--lock", lockp,
                              "--espera-cerrojo", "3", "--tasas", "0.09"], capture_output=True, text=True, timeout=120,
                             env=dict(os.environ, HOJA_RESUMEN_CERROJO_YA_TOMADO="0"))
        fcntl.flock(fl, fcntl.LOCK_UN)
    paso("H11 · con el cerrojo ocupado (p. ej., lanzada dentro de flock), la hoja no se queda esperando: código 6 con mensaje claro y sin hoja",
         r11.returncode == 6 and "cerrojo" in r11.stdout and not os.path.exists(os.path.join(exp, H.SALIDA_MD)), r11.stdout.strip()[-160:])

    # ============================== Vidrala 4.14 (V6.4, objetivo condicionado y provisional)
    exp = copia("V6.4_Vidrala_4_14")
    rc, out = correr([exp, "--trabajo", tmp, "--tasas", "0.09"])
    md, t = hoja_de(exp)
    ficha = jload(os.path.join(exp, "ficha.json"))
    paso("V6.4 Vidrala 4.14: la hoja sale (código 0)", rc == 0 and bool(md), out.strip()[-160:])
    paso("H1 · objetivo condicionado: «Es un precio provisional: el objetivo está condicionado», con la condición de la ficha en las salvedades",
         "Es un precio provisional: el objetivo está condicionado" in md and "- Condición: esperar por precio" in md
         and "emitido con condiciones (provisional)" in md)
    paso("H1 · Vidrala 4.14: se copian el fundamento y el alcance de la ficha y la marca «con datos de etapa 1 incompletos»",
         "- Fundamento: no procede" in md and "- Alcance: ENSAYO" in md and "con datos de etapa 1 incompletos" in md)
    paso("H3 · V6.4 con aptitud_de_uso: cita la evaluación de la entrega y no afirma «apto para dinero real»",
         f"Evaluación de la entrega {ficha['aptitud_de_uso']['version']}" in md and not AFIRMA_APTO.search(md))
    tabla = seccion(md, "## Cuánto cambia el resultado")
    paso("H12 · las tasas vecinas de la del análisis (8 % y 10 %) se calculan siempre para decir si el resultado cambia con la tasa",
         sorted(round(f["r"], 4) for f in (t.get("sensibilidad") or {}).get("filas") or []) == [0.08, 0.09, 0.10] and "Frente a la tasa, el resultado" in tabla)
    paso("H7 · Vidrala 4.14 al 8 %: la fila avisa de que la tasa queda por debajo de la mínima de la hoja (8,2 %)",
         bool(re.search(r"\| 8 % \|[^\n]*por debajo de la mínima de la hoja \(8,2 %\)", tabla)), tabla[-400:])

    # ============================== Viscofan 4.14 (V6.4.1, motor B, aviso A2)
    exp = copia("V6.4.1_Viscofan_4_14")
    rc, out = correr([exp, "--trabajo", tmp, "--tasas", "0.07,0.09"])
    md, t = hoja_de(exp)
    tabla = seccion(md, "## Cuánto cambia el resultado")
    paso("V6.4.1 Viscofan 4.14: la hoja sale (código 0)", rc == 0 and bool(md), out.strip()[-160:])
    paso("H7 · aviso A2: «la hoja de cálculo avisa de que el 9 % queda por debajo de su tasa mínima de referencia (9,5 %)»",
         "queda por debajo de su tasa mínima de referencia (9,5 %)" in tabla)
    paso("H7 · la fila del 7 % lleva el aviso «por debajo de la mínima» y la tasa con que descuenta el motor B",
         bool(re.search(r"\| 7 % \|[^\n]*por debajo de la mínima de la hoja \(9,5 %\)[^\n]*descuenta al", tabla)))

    # ============================== Elis 4.14 (pendiente_de_datos: sin conclusión)
    exp = copia("Elis_4_14")
    rc, out = correr([exp, "--trabajo", tmp, "--tasas", "0.09"])
    md, t = hoja_de(exp)
    ficha = jload(os.path.join(exp, "ficha.json"))
    concl = seccion(md, "## Qué concluye el análisis")
    paso("Elis 4.14 (pendiente_de_datos, cierre vigente): la hoja sale (código 0)", rc == 0 and bool(md), out.strip()[-160:])
    paso("H1 · sin conclusión: «Sin conclusión: falta un dato», el motivo de la ficha y «la ficha no da precio de compra»",
         "Sin conclusión: falta un dato." in concl and "Motivo, según la ficha:" in concl and "Reparto del capex" in concl
         and "la ficha no da precio de compra" in concl and (t.get("veredicto") or {}).get("precio_compra") is None)
    paso("H1 · Elis: el 7,30 € de la hoja de cálculo no aparece como precio de compra («a 7,30 € por acción o menos») y se dice por qué",
         "7,30 € por acción o menos" not in md and "La hoja de cálculo arroja un precio de Sí de 7,30 €, pero la ficha dice que esa cifra no es utilizable" in concl)
    tabla = seccion(md, "## Cuánto cambia el resultado")
    paso("H1 · Elis: la tabla se presenta como «lectura de la hoja de cálculo, no una conclusión», sin «firme» ni «oficial» en la comprobación",
         "lectura de la hoja de cálculo, no una conclusión" in tabla and "no es un precio de compra" in tabla and "firme" not in tabla.lower()
         and "precio de Sí oficial" not in md)
    paso("H12 · el crecimiento «no utilizable» se explica («no se puede calcular»)", "no se puede calcular" in tabla and "no utilizable" in tabla)

    # ============================== Vidrala 4.13 bloqueo (objetivo bloqueado)
    exp = copia("Vidrala_4_13_bloqueo")
    rc, out = correr([exp, "--trabajo", tmp, "--tasas", "0.09"])
    md, t = hoja_de(exp)
    concl = seccion(md, "## Qué concluye el análisis")
    paso("Vidrala 4.13 bloqueo: la hoja sale (código 0)", rc == 0 and bool(md), out.strip()[-160:])
    paso("H1 · objetivo bloqueado: sin conclusión, «la ficha no da precio de compra … la ficha dice que el objetivo está bloqueado», sin «56,02 € por acción o menos»",
         "Sin conclusión" in concl and "objetivo está bloqueado" in concl and "56,02 € por acción o menos" not in md
         and "- Objetivo de precio: bloqueado" in md)

    # ============================== Hermès (empresas_v2: sin cierre registrado, no vigente)
    exp = copia("Hermes")
    rc, out = correr([exp, "--trabajo", tmp])
    paso("H2 · Hermès (no vigente para la vía oficial): la hoja no se genera (código 3, «no está vigente»)",
         rc == 3 and "no está vigente" in out and not os.path.exists(os.path.join(exp, H.SALIDA_MD)), out.strip()[-160:])
    rc, out = correr([exp, "--trabajo", tmp, "--tasas", "0.09", "--antecedente"])
    md, t = hoja_de(exp)
    rc2, out2 = correr([exp, "--comprobar"])
    paso("H2 · --antecedente: la hoja sale rotulada arriba «NO VIGENTE · ANTECEDENTE» y --comprobar nunca la da por vigente (código 4)",
         rc == 0 and md.split("\n## ", 1)[0].count("NO VIGENTE · ANTECEDENTE") == 1 and (t.get("vigencia") or {}).get("vigente") is False
         and rc2 == 4 and "NO VIGENTE" in out2, (out + " | " + out2).strip()[-200:])

    # ============================== V6.3.1 F1 sintética: cierre, hoja, F1 cambiada y relanzamiento con --desde 12
    try:
        sys.path.insert(0, os.path.join(RAIZ, "v6", "v631_f1", "scripts"))
        import prueba_pipeline_v631 as PP  # noqa: E402
        TS, PF = PP.TS, PP.PF
        base0, TS.BASE = TS.BASE, os.path.join(tmp, "sint631")
        os.makedirs(TS.BASE)
        c = PF.preparar("EmpresaX_V631", PP.declaracion())
        with cerrojo():
            rcp, outp = PP.correr(c, PP.CFG631)
        st = TS.estado(c)
        paso("F1 · la empresa sintética V6.3.1 F1 se cierra con el pipeline real (concluido, cierre vigente)",
             rcp == 0 and st.get("estado_analisis") == "concluido" and os.path.isfile(os.path.join(c, "cierre_vigente.json")), f"código {rcp} · {st.get('estado_analisis')}")
        rc, out = correr([c, "--trabajo", tmp, "--tasas", "0.09"])
        paso("H5 · los textos sintéticos (tesis inversa y «a No» casi vacíos) no dan hoja: código 4 por contenido mínimo, sin hoja_resumen.md",
             rc == 4 and "CONTENIDO MÍNIMO" in out and not os.path.exists(os.path.join(c, H.SALIDA_MD)), out.strip()[-160:])
        d_, libro_, huellas_ = H.leer_expediente(c)
        pr_ = d_["precio.json"]
        filas_ = [dict({k: pr_.get(k) for k in ("precio_si", "ponderado", "zona", "V", "precio", "g_impl_actual")}, r=0.09)]
        md, t = H.componer(c, d_, libro_, huellas_, filas_, 0.09, True, {})
        apt_txt = seccion(md, "## Qué concluye el análisis")
        paso("H3 · V6.3.1 F1: la hoja dice «Datos de entrada verificados contra sus fuentes: no» (verificacion_entradas) y la línea «Motor A · F1»",
             "Datos de entrada verificados contra sus fuentes: **no**" in apt_txt and "Motor A · F1:" in apt_txt and not AFIRMA_APTO.search(md))
        # para probar el relanzamiento hace falta una hoja: se escribe en este proceso con la regla de contenido mínimo desactivada
        cm0 = H.contenido_minimo
        H.contenido_minimo = lambda *a: []
        try:
            rc, out = en_proceso(H.generar, c, c, tmp, LOCK, [0.09], cerrojo_ya_tomado=YA_TOMADO)
        finally:
            H.contenido_minimo = cm0
        rc_v0, _ = correr([c, "--comprobar"])
        paso("F1 · (preparación) hoja escrita sobre el cierre V6.3.1 F1 y vigente", rc == 0 and rc_v0 == 0, str(rc) + " " + out.strip()[-140:])
        d = PP.declaracion(0.31)
        PF.escribir_fuente(c, d)
        json.dump(d, open(os.path.join(c, "motor_a_f1.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc_v, out_v = correr([c, "--comprobar"])
        paso("H2 · F1 cambiada después del cierre: --comprobar ya no da la hoja por vigente (código 4)", rc_v == 4, out_v.strip()[-140:])
        os.environ["MUNGER_CONFIG"] = PP.CFG631
        try:
            with cerrojo():
                r = subprocess.run([TS.PY, TS.PIPE, c, "--desde", "12"], capture_output=True, text=True)
                if r.returncode == 10:
                    PP.correr(c, PP.CFG631)
        finally:
            os.environ.pop("MUNGER_CONFIG", None)
        st = TS.estado(c)
        hist = sorted(os.listdir(os.path.join(c, "historial_hojas_resumen"))) if os.path.isdir(os.path.join(c, "historial_hojas_resumen")) else []
        paso("H2 · decisión del coordinador: al relanzar el pipeline (--desde 12) la hoja anterior se archiva como NO VIGENTE y «fin» deja de estar",
             not os.path.exists(os.path.join(c, H.SALIDA_MD)) and bool(hist)
             and os.path.isfile(os.path.join(c, "historial_hojas_resumen", hist[-1], "hoja_resumen.NO_VIGENTE.md"))
             and bool(st.get("fin_anterior")) and (st.get("fin") is None or st.get("estado_analisis") == "concluido"),
             f"estado {st.get('estado_analisis')} · fin {st.get('fin')} · fin_anterior {st.get('fin_anterior')} · {hist}")
        rc, out = correr([c, "--trabajo", tmp, "--tasas", "0.09"])
        paso("H2 · P10: con F1 bloqueando tras el relanzamiento no hay hoja (código 3)", rc == 3 and not os.path.exists(os.path.join(c, H.SALIDA_MD)), out.strip()[-160:])
        TS.BASE = base0
    except Exception as e:  # noqa: BLE001
        paso("F1 · caso sintético V6.3.1 F1 ejecutado", False, f"{type(e).__name__}: {str(e)[:200]}")
finally:
    shutil.rmtree(tmp, ignore_errors=True)

paso("los expedientes originales del paquete no cambian", all(huellas_dir(p) == originales[n] for n, p in EXPEDIENTES.items()))
gs = subprocess.run(["git", "-C", RAIZ, "status", "--porcelain", "--", "personaje_v2/empresas_v2", "personaje_v2/empresas_v2_correcciones",
                     "personaje_v2/pruebas/sintetico"], capture_output=True, text=True)
paso("nada cambia en empresas_v2, empresas_v2_correcciones ni pruebas/sintetico del paquete (git status vacío)",
     gs.returncode != 0 or not gs.stdout.strip(), gs.stdout.strip()[:200])

n = sum(ok for _, ok in RES)
print(f"{n}/{len(RES)} pruebas de la hoja resumen PASAN" if n == len(RES) else f"{n}/{len(RES)} pruebas de la hoja resumen: FALLAN {len(RES) - n}")
sys.exit(0 if n == len(RES) else 1)
