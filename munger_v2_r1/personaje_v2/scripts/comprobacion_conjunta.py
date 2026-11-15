#!/usr/bin/env python3
"""Comprobación conjunta de las hipótesis sin fundamento (D10; Anexo B §B.6; Anexo D §D.6b).

Uso: comprobacion_conjunta.py CARPETA <E>_v63_evaluada.xlsx [--config config_v2.json]
Lee fase_c.json → fundamento_material.comprobacion_conjunta.combinacion ({"Hoja!REF": valor}) y rangos_y_evidencia (si los hay).
Escribe la combinación en una COPIA DE PRUEBA (comprobacion_conjunta/<E>_conj.xlsx; nunca toca el libro), recalcula con
recálculo forzado, lee valores (leer_resultados.py), calcula la escalera (precio_de_si.py --copia), pasa la gramática sobre la
copia y escribe comprobacion_conjunta.json con `sobrevive`. El script NO decide: la fase C lee el resultado en su segundo turno.
Código 0 ok · 1 no se pudo ejecutar (fallo mecánico) · 2 uso · 3 combinación mal formada por el agente (celda ajena a las 52 de A/B, de la
fase C, de Control maestro, o valor no numérico): el pipeline pide corrección a la fase C.
(4.12 §4 y §9) Con la plantilla V6.4 en modo experimental:
  - la combinación solo puede mover los parámetros numéricos ACTIVOS de la configuración (configuracion_economica.numericos_activos:
    N1 si hay N1, N2 si hay N2, λ o θ según la familia activa); mover uno inactivo es una combinación mal formada (código 3);
  - `comprobacion_conjunta.alternativas_no_numericas` (lista de claves, p. ej. ["PM1.estructura"]) evalúa de forma explícita las
    hipótesis no numéricas sin fundamento suficiente: la misma combinación se recalcula con cada alternativa DEFINIDA
    (configuracion_economica.alternativas), una a una (las combinaciones cruzadas entre alternativas no se calculan y se declaran).
    Una clave sin alternativas definidas, o una alternativa que no sobrevive, hace `sobrevive` = false. `por_alternativa` guarda cada
    resultado y `sobrevive_combinacion_activa`, el de la configuración del expediente.
"""
import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402


CONFIG_V64 = "Configuración V6.4"
PARAMETROS_V64 = ("B11", "B21", "B38", "B39")   # N1 tipo, N2 margen de partida, λ, θ


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    return r.returncode, (r.stdout + r.stderr)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("libro")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG (la del pipeline) o config_v2.json
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    # (4.12 §5) una llamada a mano sin MUNGER_CONFIG resuelve la selección registrada del expediente (o se detiene sin escribir)
    import seleccion_plantilla as SEL
    cfg, m_sel, nota_sel = SEL.resolver(a.carpeta, cfg)
    if m_sel:
        print(f"comprobacion_conjunta.py: SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}")
        return 2
    if nota_sel:
        print(f"comprobacion_conjunta.py: {nota_sel}")
    fc = json.load(open(os.path.join(a.carpeta, "fase_c.json"), encoding="utf-8"))
    fm = fc.get("fundamento_material") or {}
    cc = fm.get("comprobacion_conjunta") or {}
    comb = cc.get("combinacion")
    if not cc.get("procede") or (not comb and not cc.get("alternativas_no_numericas")):
        print("no procede: fase_c.json no trae una combinación (procede = false o combinacion vacía y sin alternativas_no_numericas)")
        return 3
    comb = comb or {}  # (4.12) solo alternativas no numéricas: la combinación numérica puede estar vacía
    if not isinstance(comb, dict):
        print(f"ERROR: combinacion tiene que ser un objeto celda → valor (es {type(comb).__name__})")
        return 3
    # claves sin hoja → Análisis (mismo criterio que fase_a_celdas.py y el ejemplo de §D.6b)
    comb = {(k if "!" in k else f"Análisis!{k}"): v for k, v in comb.items()}
    # (4.11) con la plantilla V6.4 experimental, los parámetros numéricos de la configuración económica (N1, N2, λ, θ) también son
    # hipótesis que la comprobación conjunta puede mover (no quedan fuera de los controles por no estar en las 68 celdas)
    comb_cfg = {k: v for k, v in comb.items() if k.split("!")[0] == CONFIG_V64 and k.split("!")[1] in PARAMETROS_V64}
    comb = {k: v for k, v in comb.items() if k not in comb_cfg}
    conf = None
    pconf = os.path.join(a.carpeta, "configuracion_economica.json")
    if os.path.exists(pconf):
        import configuracion_economica as CE
        try:
            conf = json.load(open(pconf, encoding="utf-8"))
        except (OSError, ValueError):
            conf = None
    alt_claves = cc.get("alternativas_no_numericas") or []
    if comb_cfg or alt_claves:
        import configuracion_economica as CE
        activos_num = set((CE.numericos_activos(conf) if conf else {}).values())
        inactivos = sorted(k for k in comb_cfg if k not in activos_num)
        if inactivos:
            # (4.12) un parámetro inactivo no cambia nada en el libro: moverlo aparentaría una comprobación que no se hizo
            print(f"ERROR: la combinación mueve parámetros de la configuración que no están activos en configuracion_economica.json: {inactivos} "
                  f"(activos numéricos: {sorted(activos_num) or 'ninguno'})")
            return 3
        if alt_claves and (not conf or conf.get("modo") != "Experimental"):
            print("ERROR: alternativas_no_numericas solo existe con la plantilla V6.4 en modo experimental")
            return 3
        malas_alt = [k for k in alt_claves if not isinstance(k, str) or k not in CE.activos(conf) or k == "modo"]
        if malas_alt:
            print(f"ERROR: alternativas_no_numericas nombra claves que no son parámetros activos de la configuración: {malas_alt}")
            return 3
    if comb_cfg:
        from v63_xml import LibroV63
        if CONFIG_V64 not in LibroV63(a.libro).hojas():
            print(f"ERROR: la combinación toca {sorted(comb_cfg)} pero el libro no es V6.4 (sin la hoja «{CONFIG_V64}»)")
            return 3
    permitidas = C.lista_blanca_juicio()
    malas = [k for k in comb if k.split("!")[0] not in permitidas or k.split("!")[1] not in permitidas[k.split("!")[0]] or k.startswith("Control maestro")]
    if malas:
        print(f"ERROR: la combinación toca celdas que no son de juicio: {malas}")
        return 3
    fase_c_solo = [k for k in comb if C.CELDAS[k.split("!")[0]][k.split("!")[1]].get("fase") == "C"]
    if fase_c_solo:
        print(f"ERROR: la combinación toca celdas de la fase C (todavía no escritas): {fase_c_solo}")
        return 3
    no_num = [k for k, v in list(comb.items()) + list(comb_cfg.items()) if not isinstance(v, (int, float)) or isinstance(v, bool)]
    if no_num:
        print(f"ERROR: la combinación trae valores no numéricos: {no_num}")
        return 3
    carp = os.path.join(a.carpeta, "comprobacion_conjunta")
    os.makedirs(carp, exist_ok=True)
    base = os.path.basename(a.libro).replace("_v63_evaluada", "").replace(".xlsx", "")
    perfil = os.path.join(a.carpeta, ".lo_perfil") if cfg.get("recalc", {}).get("perfil_por_empresa", True) else cfg.get("recalc", {}).get("perfil", os.path.join(carp, ".lo_perfil"))

    def evaluar(sufijo, celdas_cfg):
        """Escribe la combinación (y, si las hay, las celdas de configuración de una alternativa) en una copia de prueba, recalcula,
        lee, calcula la escalera y pasa la gramática. Devuelve (dict, None) o (None, motivo de fallo mecánico)."""
        sub = os.path.join(carp, sufijo) if sufijo else carp
        os.makedirs(sub, exist_ok=True)
        copia = os.path.join(sub, f"{base}_conj.xlsx")
        cj = os.path.join(sub, "combinacion.json")
        json.dump(comb, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out = run([sys.executable, os.path.join(AQUI, "escribir_v63.py"), a.libro, copia, "--celdas", cj, "--copia-de-prueba"])
        if rc != 0:
            return None, "ERROR al escribir la copia de prueba: " + out[-400:]
        if comb_cfg or celdas_cfg:
            from v63_xml import LibroV63
            lb = LibroV63(copia)
            if celdas_cfg:
                sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
                import inventario_entradas  # noqa: E402  (el de la plantilla activa)
                perm_cfg = inventario_entradas.conjunto_entradas()[CONFIG_V64]
                if "B146" in perm_cfg:  # (4.13 §7) V6.4.1: las celdas del perímetro que la alternativa no declara, vacías
                    import configuracion_economica as _CE
                    celdas_cfg = {**{f"{CONFIG_V64}!{r}": None for r in sorted(_CE.SOLO_V641)}, **celdas_cfg}
                lb.escribir_celdas(celdas_cfg, {CONFIG_V64: perm_cfg})
            if comb_cfg:
                lb.escribir_celdas(comb_cfg, {CONFIG_V64: set(PARAMETROS_V64)})
            lb.borrar_caches()
            lb.guardar(copia)
        rc, out = run(["bash", os.path.join(AQUI, "recalc.sh"), copia, os.path.join(sub, "recalc"), perfil])
        if rc != 0:
            return None, "ERROR al recalcular la copia: " + out[-400:]
        rec = os.path.join(sub, "recalc", os.path.basename(copia))
        res_path = os.path.join(sub, "resultados.json")
        rc, out = run([sys.executable, os.path.join(AQUI, "leer_resultados.py"), rec, res_path, "--exigir-recalculo-forzado"])
        if rc != 0:
            return None, "ERROR al leer la copia recalculada: " + out[-400:]
        res = json.load(open(res_path, encoding="utf-8"))
        res["copia_de_prueba"] = True
        json.dump(res, open(res_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
        precio_path = os.path.join(sub, "precio.json")
        if os.path.exists(precio_path):
            os.remove(precio_path)
        rc, out = run([sys.executable, os.path.join(AQUI, "precio_de_si.py"), res_path, precio_path, "--copia", "--k", str(cfg.get("convenciones", {}).get("k_asimetria", 3))])
        if rc not in (0, 5) or not os.path.exists(precio_path):
            return None, f"ERROR: precio_de_si.py sobre la copia terminó con código {rc}: " + out[-400:]
        precio = json.load(open(precio_path, encoding="utf-8"))
        # gramática sobre la copia (carpeta temporal con fase_b, referencias, datos y los resultados de la copia)
        tmp = os.path.join(sub, "gramatica_copia")
        os.makedirs(tmp, exist_ok=True)
        for f in ("fase_b.json", "referencias_mecanicas.json", "datos_v63.json"):
            shutil.copy(os.path.join(a.carpeta, f), os.path.join(tmp, f))
        shutil.copy(res_path, os.path.join(tmp, "resultados.json"))
        rc_g, out_g = run([sys.executable, os.path.join(AQUI, "comprobar_gramatica.py"), tmp, "--tras-recalculo", "--copia-de-prueba"])
        if rc_g == 4 or not os.path.exists(os.path.join(tmp, "gramatica.json")):
            return None, "ERROR: la gramática no pudo ejecutarse sobre la copia: " + out_g[-400:]
        gram = json.load(open(os.path.join(tmp, "gramatica.json"), encoding="utf-8"))
        errores = [f"{x['id']} {x.get('escenario') or ''}: {x['detalle']}" for x in gram["hallazgos"] if x["categoria"] in ("error", "límite del modelo")]
        zona = precio.get("zona")
        sobrevive = (zona in ("cumple_regla_k", "bajo_malo")) and not errores and "sin_lectura" not in precio and "sin_escalera" not in precio
        return {"copia": copia, "res": res, "precio": precio, "errores": errores, "zona": zona, "sobrevive": sobrevive}, None

    ev, fallo = evaluar(None, None)
    if fallo:
        print(fallo)
        return 1
    copia, res, precio, errores, zona, sobrevive = ev["copia"], ev["res"], ev["precio"], ev["errores"], ev["zona"], ev["sobrevive"]
    original = json.load(open(os.path.join(a.carpeta, "precio.json"), encoding="utf-8")) if os.path.exists(os.path.join(a.carpeta, "precio.json")) else {}
    # (4.12) alternativas no numéricas evaluadas de forma explícita, una a una, con la misma combinación
    por_alt = []
    for k_alt in alt_claves:
        alts, motivo_alt = CE.alternativas(conf, k_alt)
        if not alts:
            por_alt.append({"clave": k_alt, "alternativa": None, "definida": False, "motivo": motivo_alt, "zona": None, "sobrevive": False})
            continue
        for n_alt, (etiqueta, conf_alt) in enumerate(alts, 1):
            ev_a, fallo_a = evaluar(f"alternativa_{k_alt.replace('.', '_')}_{n_alt}", CE.celdas(conf_alt))
            if fallo_a:
                print(f"{fallo_a} (alternativa {k_alt} = {etiqueta})")
                return 1
            por_alt.append({"clave": k_alt, "alternativa": etiqueta, "definida": True, "resumen_configuracion": CE.resumen(conf_alt),
                            "precio_si": ev_a["precio"].get("precio_si"), "ponderado": ev_a["precio"].get("ponderado"), "zona": ev_a["zona"],
                            "errores_gramatica": ev_a["errores"], "sobrevive": ev_a["sobrevive"],
                            "hash_copia": hashlib.sha256(open(ev_a["copia"], "rb").read()).hexdigest()})
    sobrevive_activa = sobrevive
    sobrevive = sobrevive_activa and all(x["sobrevive"] for x in por_alt)
    out = {
        "libro_origen": a.libro, "copia_de_prueba": copia, "hash_copia": hashlib.sha256(open(copia, "rb").read()).hexdigest(),
        "combinacion": comb, "rangos_y_evidencia": cc.get("rangos_y_evidencia") or {h.get("celda"): h.get("alternativas_defendibles") for h in (fm.get("hipotesis_sin_fundamento") or [])},
        "coherencia_economica": cc.get("coherencia_economica"),
        "recalculo_forzado_comprobado": res.get("recalculo_forzado_comprobado"),
        "precio_actual": precio.get("precio"),
        "resultados_bajo_combinacion": {"B78": res["valores"].get("B78"), "C78": res["valores"].get("C78"), "D78": res["valores"].get("D78"), "C83": res["valores"].get("C83"),
                                        "Motor!B255": res["estados"].get("estado_tecnico_B255"), "semaforos": {k: v[1:] for k, v in (res.get("semaforos") or {}).items() if k in ("fila40", "fila41", "fila42", "fila43", "fila44")},
                                        "errores_gramatica": errores},
        "escalera_bajo_combinacion": {k: precio.get(k) for k in ("P_estrella", "precio_si", "precio_escenario_malo", "ponderado", "zona")} | {"zona_precio_actual": zona, "sin_lectura": precio.get("sin_lectura"), "sin_escalera": precio.get("sin_escalera")},
        "escalera_original": {k: original.get(k) for k in ("V", "p", "P_estrella", "precio_si", "precio_escenario_malo", "ponderado", "zona")} | {"zona_precio_actual": original.get("zona")},
        "sobrevive": sobrevive,
        "nota": "superar esta comprobación no es una garantía de seguridad; su fuerza depende de los rangos declarados (S-17)",
    }
    if alt_claves:
        out["sobrevive_combinacion_activa"] = sobrevive_activa
        out["alternativas_no_numericas"] = alt_claves
        out["por_alternativa"] = por_alt
        out["nota_alternativas"] = ("cada alternativa no numérica se recalcula una a una con la misma combinación; las combinaciones cruzadas entre "
                                    "alternativas no se calculan; una clave sin alternativas definidas no sobrevive (no se inventan entradas)")
    json.dump(out, open(os.path.join(a.carpeta, "comprobacion_conjunta.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    print(f"OK: comprobación conjunta → sobrevive = {sobrevive} · zona bajo la combinación: {zona} (original: {original.get('zona')}) · errores de gramática: {len(errores)}"
          + (f" · alternativas no numéricas: {sum(1 for x in por_alt if x['sobrevive'])}/{len(por_alt)} sobreviven" if alt_claves else "") + " → comprobacion_conjunta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
