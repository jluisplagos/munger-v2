#!/usr/bin/env python3
"""Variantes calculadas de la configuración económica V6.4 (encargo 4.11 §6, §9 y §10): materialidad y estructuras compatibles.

Uso: variantes_configuracion_v64.py CARPETA LIBRO_EVALUADO [--config config.json]
Solo con la plantilla V6.4 y configuracion_economica.json en modo experimental (si no, escribe {"aplica": false} y termina con 0).
Para cada variante escribe una COPIA del libro evaluado con otras celdas de «Configuración V6.4» (nunca toca el libro), la
recalcula con recálculo forzado (perfil del expediente; en secuencia), lee los valores (leer_resultados.py) y la escalera
(precio_de_si.py --copia), y escribe configuracion_v64_variantes.json y .md:
  - heredado (V6.3 efectiva), activa (la configuración del expediente) y cada componente AISLADO (N1, N2, R1, P0) y la activa sin
    P-M1, para la materialidad mecánica de cada parámetro (Δ ponderado y Δ precio de Sí frente a la activa y al heredado);
  - con requisito adicional: las cinco estructuras y «sin requisito» con las MISMAS entradas compatibles (familia, parámetro,
    convenciones, cartera, N1–N3), y las dos convenciones alternativas de años y terminal de la estructura activa;
  - (4.13 §7) con la plantilla V6.4.1 y el perímetro declarado: el otro perímetro (Caja ↔ NIIF 16) y sus extremos del rango.
Ninguna variante se elige ni se adopta. «No cambia la zona» solo puede afirmarse de las variantes de esta tabla (campo
`zona_igual_en_todas_las_calculadas`). Código 0 ok · 1 fallo mecánico (se informa la variante; no se reintenta en bucle) · 2 uso.
"""
import argparse
import copy
import hashlib
import json
import os
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import configuracion_economica as CE  # noqa: E402
from v63_xml import LibroV63  # noqa: E402


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
    return r.returncode, (r.stdout + r.stderr)


def variantes(conf):
    """[(clave, descripción, configuración)]: la activa y sus variaciones compatibles."""
    out = [("heredado", "modo heredado (V6.3 efectiva: R0, sin P-M1, tipo de la Historia, margen de Palancas C8)", {**conf, "modo": "Heredado", "N1": None, "N2": None, "N3": None, "PM1": None}),
           ("activa", "configuración del expediente", conf)]
    pm = conf.get("PM1") or {}
    sin_pm1 = {"estructura": CE.ESTRUCTURAS[0], "cartera": CE.CARTERA[0]}
    r0 = {"regla": CE.REGLAS[0]}
    base_vacia = {**conf, "N1": None, "N2": None, "N3": r0, "PM1": sin_pm1}
    if conf.get("N1"):
        out.append(("solo_N1", "solo N1 (tipo normalizado), con R0 y sin P-M1", {**base_vacia, "N1": conf["N1"]}))
    if conf.get("N2"):
        out.append(("solo_N2", "solo N2 (margen de partida), con R0 y sin P-M1", {**base_vacia, "N2": conf["N2"]}))
    if (conf.get("N3") or {}).get("regla") == CE.REGLAS[1]:
        out.append(("solo_R1", "solo N3 · R1, sin N1, N2 ni P-M1", {**base_vacia, "N3": conf["N3"]}))
    # (4.13 §5) contrastes AISLADOS (o con sus vinculados necesarios) frente a la activa: quitar toda la configuración o toda P-M1 no
    # demuestra el efecto aislado de un parámetro. Solo los definidos con las entradas declaradas (no se inventa ninguna)
    if conf.get("N1"):
        out.append(("activa_sin_N1", "la activa sin N1 (tipo de la Historia; el escudo va ligado a N1)", {**conf, "N1": None}))
        otro = CE.ESCUDO[1] if conf["N1"].get("escudo") == CE.ESCUDO[0] else CE.ESCUDO[0]
        out.append(("escudo_alternativo", f"la activa con el escudo «{otro}»", {**conf, "N1": {**conf["N1"], "escudo": otro}}))
    if conf.get("N2"):
        out.append(("activa_sin_N2", "la activa sin N2 (margen de partida de Palancas C8)", {**conf, "N2": None}))
    req = pm.get("estructura") in CE.ESTRUCTURAS[1:]
    if (conf.get("N3") or {}).get("regla") == CE.REGLAS[1] and (req or pm.get("cartera") == CE.CARTERA[1]):
        out.append(("activa_R0_sin_PM1", "la activa con R0, que exige quitar P-M1 (R0 + P-M1 no está especificado): variación conjunta necesaria",
                    {**conf, "N3": r0, "PM1": sin_pm1}))
    if pm.get("cartera") == CE.CARTERA[1]:
        out.append(("cartera_legado", "la activa con la cartera legado (se repone con la amortización)", {**conf, "PM1": {**pm, "cartera": CE.CARTERA[0]}}))
    if req:
        otra = CE.FAMILIAS[1] if pm.get("familia") == CE.FAMILIAS[0] else CE.FAMILIAS[0]
        k_otra = "theta" if otra == CE.FAMILIAS[1] else "lambda"
        if isinstance(pm.get(k_otra), (int, float)) and not isinstance(pm.get(k_otra), bool):
            out.append(("familia_alternativa", f"la activa con la familia {otra.split(' ·')[0]} ({k_otra} = {pm[k_otra]} declarado)", {**conf, "PM1": {**pm, "familia": otra}}))
    if pm.get("estructura") in CE.ESTRUCTURAS[1:] or pm.get("cartera") == CE.CARTERA[1]:
        out.append(("activa_sin_PM1", "la activa sin P-M1 (sin requisito adicional y cartera legado)", {**conf, "PM1": sin_pm1}))
    if pm.get("cartera") == CE.CARTERA[1]:
        out.append(("activa_solo_P0", "la activa sin requisito adicional, con P0", {**conf, "PM1": {**pm, "estructura": CE.ESTRUCTURAS[0]}}))
    if pm.get("estructura") in CE.ESTRUCTURAS[1:]:
        for e in CE.ESTRUCTURAS[1:]:
            if e == pm["estructura"]:
                continue
            cod = e.split(" ·")[0]
            out.append((f"estructura_{cod}", f"misma configuración con la estructura {cod} (entradas compatibles)",
                        {**conf, "PM1": {**pm, "estructura": e, "roic_terminal": CE.ROIC_T[1] if cod == "SR2" else CE.ROIC_T[0]}}))
        alt_a = CE.CONV_ANIOS[1] if pm.get("convencion_anios") == CE.CONV_ANIOS[0] else CE.CONV_ANIOS[0]
        alt_t = CE.CONV_TERM[1] if pm.get("convencion_terminal") == CE.CONV_TERM[0] else CE.CONV_TERM[0]
        # (4.11, revisión interna H11) extremos del rango declarado del parámetro (λ o θ), con la misma estructura y convenciones
        k_p, k_r = ("lambda", "lambda_rango") if pm.get("familia") == CE.FAMILIAS[0] else ("theta", "theta_rango")
        for nombre, x in zip(("parametro_minimo", "parametro_maximo"), pm.get(k_r) or []):
            out.append((nombre, f"estructura activa con {('λ' if k_p == 'lambda' else 'θ')} = {x} (extremo del rango declarado)", {**conf, "PM1": {**pm, k_p: x}}))
        # (4.13 §7) V6.4.1: el otro perímetro de la inversión (Caja ↔ NIIF 16) con las mismas entradas, y con los extremos del rango
        if CE.declara_perimetro(conf):
            otro = CE.PERIMETROS[0] if pm.get("perimetro_inversion") == CE.PERIMETROS[1] else CE.PERIMETROS[1]
            if otro == CE.PERIMETROS[0] or pm.get("altas_derechos_uso") is not None:
                pm_o = {**pm, "perimetro_inversion": otro}
                et = otro.split(" ·")[0]
                out.append(("perimetro_alternativo", f"estructura activa con el perímetro «{et}» (mismas entradas)", {**conf, "PM1": pm_o}))
                for nombre, x in zip(("perimetro_alternativo_parametro_minimo", "perimetro_alternativo_parametro_maximo"), pm.get(k_r) or []):
                    out.append((nombre, f"perímetro «{et}» con {('λ' if k_p == 'lambda' else 'θ')} = {x} (extremo del rango declarado)",
                                {**conf, "PM1": {**pm_o, k_p: x}}))
        out.append(("convencion_anios_alternativa", f"estructura activa con los años «{alt_a}»", {**conf, "PM1": {**pm, "convencion_anios": alt_a}}))
        out.append(("convencion_terminal_alternativa", f"estructura activa con el terminal «{alt_t}»", {**conf, "PM1": {**pm, "convencion_terminal": alt_t}}))
    # una variante que la propia configuración no admite no se calcula (ni se presenta como contraste)
    return [x for x in out if x[0] in ("heredado", "activa") or not CE.validar(x[2])]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("libro")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG (la del pipeline) o config_v2.json
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    # (4.12 §5) una llamada a mano sin MUNGER_CONFIG resuelve la selección registrada del expediente (o se detiene sin escribir):
    # nunca calcula variantes de un expediente V6.4 con las referencias o el inventario de la V6.3
    import seleccion_plantilla as SEL
    cfg, m_sel, nota_sel = SEL.resolver(a.carpeta, cfg)
    if m_sel:
        print(f"variantes_configuracion_v64.py: SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}")
        return 2
    if nota_sel:
        print(f"variantes_configuracion_v64.py: {nota_sel}")
    salida = os.path.join(a.carpeta, "configuracion_v64_variantes.json")
    pc = os.path.join(a.carpeta, "configuracion_economica.json")
    if not os.path.exists(pc):
        json.dump({"aplica": False, "motivo": "sin configuracion_economica.json (plantilla V6.3)"}, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("no aplica: sin configuración económica")
        return 0
    conf = json.load(open(pc, encoding="utf-8"))
    if conf.get("modo") != "Experimental":
        json.dump({"aplica": False, "motivo": "modo heredado"}, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("no aplica: modo heredado")
        return 0
    sys.path.insert(0, cfg["plantilla"]["scripts_v63"])
    import inventario_entradas  # noqa: E402
    permitidas = {CE.HOJA: inventario_entradas.conjunto_entradas()[CE.HOJA]}
    carp = os.path.join(a.carpeta, "variantes_v64")
    os.makedirs(os.path.join(carp, "recalc"), exist_ok=True)
    perfil = os.path.join(a.carpeta, ".lo_perfil")
    k = str(cfg.get("convenciones", {}).get("k_asimetria", 3))
    filas = []
    for clave, desc, cv in variantes(conf):
        cv = copy.deepcopy(cv)
        copia = os.path.join(carp, f"{clave}.xlsx")
        libro = LibroV63(a.libro)
        libro.escribir_celdas(CE.celdas(cv, v641="B146" in permitidas[CE.HOJA]), permitidas)  # (4.13 §7) V6.4.1: también vacía el perímetro
        libro.borrar_caches()
        libro.guardar(copia)
        rc, out = run(["bash", os.path.join(AQUI, "recalc.sh"), copia, os.path.join(carp, "recalc"), perfil])
        if rc != 0:
            print(f"FALLO MECÁNICO en la variante {clave}: recálculo: {out[-300:]}")
            return 1
        rec = os.path.join(carp, "recalc", os.path.basename(copia))
        rj, pj = os.path.join(carp, f"{clave}.resultados.json"), os.path.join(carp, f"{clave}.precio.json")
        rc, out = run([sys.executable, os.path.join(AQUI, "leer_resultados.py"), rec, rj, "--exigir-recalculo-forzado"])
        if rc != 0:
            print(f"FALLO MECÁNICO en la variante {clave}: lectura: {out[-300:]}")
            return 1
        rc, out = run([sys.executable, os.path.join(AQUI, "precio_de_si.py"), rj, pj, "--copia", "--k", k])
        res = json.load(open(rj, encoding="utf-8"))
        pr = json.load(open(pj, encoding="utf-8")) if os.path.exists(pj) else {}
        c = res.get("configuracion_v64") or {}
        filas.append({"clave": clave, "descripcion": desc, "resumen_configuracion": CE.resumen(cv),
                      # (4.12 §4) qué parámetros de la configuración del expediente cambia esta variante: ámbito de cada afirmación
                      "parametros_variados": CE.parametros_variados(conf, cv), "valida_en_el_libro": c.get("valida"),
                      "motivo_si_no_valida": c.get("motivo"), "V": [res["valores"].get(x) for x in ("B78", "C78", "D78")],
                      "ponderado": res["valores"].get("C83"), "precio_si": pr.get("precio_si"), "zona": pr.get("zona"), "sin_lectura": pr.get("sin_lectura"),
                      "conciliacion": {n: (v or {}).get("comprobacion") for n, v in (c.get("conciliacion") or {}).items()},
                      "hash_copia": hashlib.sha256(open(copia, "rb").read()).hexdigest()})
        print(f"{clave:32s} ponderado {filas[-1]['ponderado']} · Sí {filas[-1]['precio_si']} · zona {filas[-1]['zona']}", flush=True)
    act = next(f for f in filas if f["clave"] == "activa")
    her = next(f for f in filas if f["clave"] == "heredado")

    def d(x, y):
        return (x - y) if isinstance(x, (int, float)) and isinstance(y, (int, float)) else None
    for f in filas:
        f["delta_ponderado_frente_a_activa"] = d(f["ponderado"], act["ponderado"])
        f["delta_precio_si_frente_a_activa"] = d(f["precio_si"], act["precio_si"])
        f["delta_ponderado_frente_a_heredado"] = d(f["ponderado"], her["ponderado"])
        f["delta_precio_si_frente_a_heredado"] = d(f["precio_si"], her["precio_si"])
    precio = json.load(open(os.path.join(carp, "activa.precio.json"), encoding="utf-8")).get("precio")
    # (4.12 §5) correspondencia con las entradas económicas del libro (no basta con que coincidan ponderado y precio de Sí): instantánea
    # de las entradas económicas del libro de origen, huella económica de la configuración y vector de escenarios de la activa
    import entradas_economicas as EE
    import dominios_v64 as DOM
    inst = EE.instantanea(a.libro)
    res_act = json.load(open(os.path.join(carp, "activa.resultados.json"), encoding="utf-8"))
    pr_act = json.load(open(os.path.join(carp, "activa.precio.json"), encoding="utf-8"))
    avisos = DOM.avisos(os.path.join(carp, "recalc", "activa.xlsx"), res_act)
    # (4.13 §5) avisos de dominio de todas las variantes calculadas (no solo de la activa), agrupados por aviso
    import objetivo_v64 as OBJ
    por_variante = {}
    for f in filas:
        rj = os.path.join(carp, f"{f['clave']}.resultados.json")
        rec = os.path.join(carp, "recalc", f"{f['clave']}.xlsx")
        por_variante[f["clave"]] = DOM.avisos(rec, json.load(open(rj, encoding="utf-8"))) if os.path.exists(rj) and os.path.exists(rec) else []
        f["avisos_de_dominio_activos"] = [x["id"] for x in por_variante[f["clave"]] if x.get("activo") is True]
    grupos = DOM.agrupar(por_variante, filas, OBJ.CLASE_ZONA)
    zonas = sorted({f["zona"] for f in filas if f["zona"]})
    sin_zona = [f["clave"] for f in filas if not f["zona"]]  # (4.11, H10) una variante que no calcula impide afirmar «la misma zona en todas»
    out = {"aplica": True, "libro_origen": os.path.basename(a.libro), "libro_origen_sha256": hashlib.sha256(open(a.libro, "rb").read()).hexdigest(),
           "configuracion_economica_sha256": hashlib.sha256(open(pc, "rb").read()).hexdigest(), "precio": precio, "k": float(k),
           "variantes": filas, "zonas_calculadas": zonas, "variantes_sin_zona": sin_zona, "zona_igual_en_todas_las_calculadas": len(zonas) == 1 and not sin_zona,
           "formato": "4.13", "entradas_economicas": {k: inst[k] for k in ("huella", "n", "celdas", "tipos", "ids", "nota", "version")},
           "configuracion_huella_economica": EE.huella_configuracion(conf), "vector_escenarios_activa": EE.vector_escenarios(res_act, pr_act),
           "avisos_de_dominio": avisos, "avisos_de_dominio_variantes": grupos,
           "nota": ("Variantes mecánicas de la configuración económica (encargo 4.11). Ninguna se elige ni se adopta; la materialidad la evalúa la fase C. "
                    "«No cambia la zona» solo vale para estas variantes calculadas.")}
    json.dump(out, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = ["# Variantes calculadas de la configuración económica V6.4 (materialidad y estructuras compatibles)", "",
          f"Libro de origen `{out['libro_origen']}` · precio {precio} · k = {k}. Ninguna variante se elige ni se adopta; «no cambia la zona» solo vale para esta tabla.", "",
          "| Variante | Configuración | Parámetros que varía (frente a la activa) | V MALO / NORMAL / BUENO | Ponderado | Precio de Sí | Zona | Δ pond. vs activa | Δ Sí vs activa | Δ pond. vs heredado |", "|---|---|---|---|---|---|---|---|---|---|"]
    fmt = lambda x: f"{x:.4f}" if isinstance(x, (int, float)) else str(x)  # noqa: E731
    for f in filas:
        md.append(f"| {f['clave']} | {f['resumen_configuracion']} | {', '.join(f['parametros_variados']) or '—'} | {' / '.join(fmt(v) for v in f['V'])} | {fmt(f['ponderado'])} | {fmt(f['precio_si'])} | {f['zona']} | "
                  f"{fmt(f['delta_ponderado_frente_a_activa'])} | {fmt(f['delta_precio_si_frente_a_activa'])} | {fmt(f['delta_ponderado_frente_a_heredado'])} |")
    fmtv = lambda v: json.dumps(v, ensure_ascii=False, default=str)[:300]  # noqa: E731
    md += ["", "## Avisos de dominio (4.12 §5; sin umbrales adoptados: valores y motivo)", "",
           "| Aviso | Activo | Valores | Motivo |", "|---|---|---|---|"]
    md += [f"| {x['id']} | {'sí' if x['activo'] else ('lectura (sin umbral)' if x['activo'] is None else 'no')} | {fmtv(x['valores'])} | {x['motivo']} |" for x in avisos]
    md += ["", "## Avisos de dominio en las variantes calculadas, agrupados (4.13 §5)", "",
           "| Aviso | Activo en | Lectura sin umbral en | Afecta a | Conclusiones | Rango de f |", "|---|---|---|---|---|---|"]
    md += [f"| {aid} | {', '.join(g['variantes']) or '—'} | {', '.join(g['lecturas']) or '—'} | {'; '.join(g['afecta']) or '—'} | {', '.join(g['conclusiones']) or '—'} | "
           f"{(fmt(g.get('f_minimo')) + '–' + fmt(g.get('f_maximo'))) if 'f_minimo' in g else '—'} |" for aid, g in grupos.items()]
    md += ["", "La fase C evalúa en `configuracion_v64.avisos_de_dominio_variantes` cada grupo activo en alguna variante distinta de la activa y la lectura del factor de reestimación "
               "(material o no, con su consecuencia); uno material condiciona el objetivo como «limite:<id>». Un aviso no es un umbral adoptado."]
    md += ["", f"Entradas económicas del libro de origen: {inst['n']} celdas, huella `{inst['huella'][:16]}…` (las editoriales no cuentan); configuración: huella económica "
               f"`{out['configuracion_huella_economica'][:16]}…`; vector de la activa: {fmtv(out['vector_escenarios_activa'])}."]
    md += ["", f"Zonas calculadas: {', '.join(zonas)} · ¿la misma en todas las calculadas?: {'sí' if out['zona_igual_en_todas_las_calculadas'] else 'NO'}. "
           "Solo vale para estas variantes: no prueba robustez frente a hipótesis no exploradas, y el rango de esta tabla no es un intervalo de confianza.", "",
           "Ámbito por parámetro activo (variantes calculadas que lo varían; 4.12 §4): " + "; ".join(
               f"{k}: {', '.join(v['clave'] for v in filas if k in v['parametros_variados'] and v['zona']) or 'ninguna'}" for k in CE.activos(conf) if k != "modo"), "",
           "Conciliación (identidad FCF y VP iguales al motor) de cada variante: " + "; ".join(f"{f['clave']}: {', '.join(set(v for v in f['conciliacion'].values() if v)) or '—'}" for f in filas)]
    open(os.path.join(a.carpeta, "configuracion_v64_variantes.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"OK: {len(filas)} variantes → configuracion_v64_variantes.json/.md · zonas {zonas}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
