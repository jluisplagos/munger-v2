#!/usr/bin/env python3
"""Retornos históricos en el perímetro F1 declarado y vara del foso (decisión P-FOSO, opción a, 18-nov-2026; dictamen
examen/revisiones/dictamen_perimetro_g4/DICTAMEN.md, defectos D1, D2 y D3).

Qué es. Con F1 declarado en un perímetro sin derechos de uso (A1_sin_ROU o A2_propio, `perimetro_reinversion` de motor_a_f1.json), las
palancas S2C y el ROIC terminal se miden sobre el capital propio (sin arrendamientos), pero Historia!C54 y C55 son de TODO el capital.
Este módulo calcula, con las filas de la Historia del libro y una serie declarada, las medidas del mismo perímetro:
  - ROIC del capital propio pagado todo el alquiler (la vara del foso, P-FOSO):
        (EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos)
        filas 7, 10, 32 y 23 de la Historia; intereses: series.intereses_arrendamiento de motor_a_f1.json (documento y página por año).
  - ROIC sin arrendamientos (ancla de G7 y del tope de la referencia del S2C): EBIT × (1 − t) ÷ (capital invertido − arrendamientos).
  - ROIC de todo el capital (= Historia fila 33; su media de cinco años es C55): solo frente al sector (Palancas!H18).
Por año en los cinco últimos de la Historia (2021–2025 en el examen) y su media simple (como C55).
Regla de la decisión: el foso (Análisis!C18) se juzga comparando el primero con r (Análisis!C56); C55 solo frente al sector; G4 sigue con
r + 3 puntos (decisión del 3-nov-2026, sin cambio).

Qué NO es. No cambia el libro, la plantilla, las fuentes ni la declaración; no decide el foso (la fase A puede seguir en «No» si la ventaja
no le parece duradera); no adopta ningún umbral nuevo; no acredita aptitud. Sin perímetro F1 declarado (o con A0_total/A3_estimado)
devuelve None y nada cambia. La serie de intereses de arrendamiento no está en el libro ni en el universo de verificacion_entradas.py:
se comprueba su fuente con la misma condición mínima que F1-SERIES (cifra publicada, en la página, con la huella del documento) y, si no
pasa, la cifra se da como NO COMPROBADA y no se usa en las referencias mecánicas.
"""
import json
import math
import numbers
import os

PERIMETROS_PROPIOS = ("A1_sin_ROU", "A2_propio")
SERIE_INTERESES = "intereses_arrendamiento"
COLS = "CDEFGHIJKL"
N_ANIOS = 5
DECISION = "P-FOSO (a), 18-nov-2026 (coordinacion/cierre_v2/DECISIONES_PARA_EL_USUARIO.md)"
REGLA = ("con F1 en {per}, el foso (Análisis!C18) se juzga comparando el ROIC del capital propio pagado todo el alquiler, "
         "(EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos), con r (Análisis!C56); Historia!C55 "
         "(ROIC de todo el capital) solo frente al sector (Palancas!H18). G4 sigue con r + 0,03. El foso puede seguir en «No» si la "
         "ventaja no parece duradera: la cifra no decide la celda")


def _num(x):
    """float de un número (int, float o Fraction de motor_a_f1); None para lo demás (texto, vacío, booleano, NaN)."""
    if isinstance(x, bool) or not isinstance(x, numbers.Real):
        return None
    x = float(x)
    return None if math.isnan(x) else x


def perimetro_declarado(decl):
    """Perímetro de la reinversión declarado si es A1_sin_ROU o A2_propio; None en otro caso (sin declaración, A0 o A3)."""
    if not isinstance(decl, dict):
        return None
    d = decl.get("perimetro_reinversion")
    per = d.get("valor") if isinstance(d, dict) else None
    return per if per in PERIMETROS_PROPIOS else None


def _valor(decl, clave):
    d = decl.get(clave) if isinstance(decl, dict) else None
    return d.get("valor") if isinstance(d, dict) else None


def leer_declaracion(carpeta):
    p = os.path.join(carpeta, "motor_a_f1.json") if carpeta else None
    if not p or not os.path.exists(p):
        return None
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def intereses(decl, anios):
    """{año: magnitud} de series.intereses_arrendamiento (misma lectura que las series de motor_a_f1.py), problemas y fuente por año."""
    import motor_a_f1 as F1
    serie, probl = F1.leer_serie(decl, SERIE_INTERESES, set(anios))
    fuente = {}
    for k, e in (((decl.get("series") or {}).get(SERIE_INTERESES)) or {}).items():
        if isinstance(e, dict):
            fuente[str(k)] = f"{e.get('documento')} p. {e.get('pagina')}" + (f" · «{e.get('fila')}»" if e.get("fila") else "")
    return {y: float(v) for y, v in serie.items()}, probl, fuente


def comprobar_fuentes(decl, carpeta, anios):
    """Condición mínima de F1-SERIES (motor_a_f1._guarda_fuentes_series) sobre series.intereses_arrendamiento: la misma función, aplicada a
    esa serie sola. Devuelve {"comprobada": bool, "invalidas", "incompletas", "columna_comprobada", "columna_pendiente"}."""
    import motor_a_f1 as F1
    s = ((decl.get("series") or {}).get(SERIE_INTERESES)) if isinstance(decl, dict) else None
    if not s:
        return {"comprobada": False, "invalidas": [], "incompletas": [f"series.{SERIE_INTERESES} sin declarar"], "columna_comprobada": 0,
                "columna_pendiente": []}
    sub = {"series": {"da_rou": s}, "fuentes_series": decl.get("fuentes_series")}
    G, res = F1.Guardas(), {}
    F1._guarda_fuentes_series(G, sub, carpeta, list(anios), res)
    fs = res.get("F1_SERIES") or {}
    ren = lambda xs: [str(x).replace("series.da_rou", f"series.{SERIE_INTERESES}") for x in xs]  # noqa: E731
    inval, incomp = ren(fs.get("invalidas") or []), ren(fs.get("incompletas") or [])
    return {"comprobada": not (inval or incomp), "invalidas": inval, "incompletas": incomp, "columna_comprobada": fs.get("columna_comprobada", 0),
            "columna_pendiente": ren(fs.get("columna_pendiente") or [])}


def calcular(anios, fila, decl, carpeta=None, r=None, c55=None, c54=None, sector_roic=None, c53=None, c58=None, c52=None, m0=None):
    """Bloque del perímetro F1. anios: los diez años de la Historia (fila 5); fila(n) → lista de diez valores de la fila n de la Historia
    (7 EBIT, 10 tipo, 23 arrendamientos, 32 capital invertido, 6 ventas). None si no hay perímetro F1 declarado sin derechos de uso."""
    per = perimetro_declarado(decl)
    if per is None:
        return None
    anios = [int(a) for a in anios]
    col = dict(zip(anios, COLS))
    H = {n: dict(zip(anios, [_num(x) for x in fila(n)])) for n in (6, 7, 10, 23, 32)}
    ult = anios[-N_ANIOS:]
    ints, probl, fuente = intereses(decl, anios)
    fuentes = comprobar_fuentes(decl, carpeta, ult) if ints else {"comprobada": False, "invalidas": [], "incompletas":
                                                                  [f"series.{SERIE_INTERESES} sin declarar en motor_a_f1.json"],
                                                                  "columna_comprobada": 0, "columna_pendiente": []}
    por = {}
    for y in ult:
        e, t, a, k = H[7][y], H[10][y], H[23][y], H[32][y]
        kp = (k - a) if (k is not None and a is not None) else None
        ok = e is not None and t is not None and kp is not None and kp > 0
        i = ints.get(y)
        por[y] = {"ebit": e, "t": t, "capital_invertido": k, "arrendamientos": a, "capital_propio": kp, "intereses_arrendamiento": i,
                  "roic_todo_el_capital": (e * (1 - t) / k) if (e is not None and t is not None and k) else None,
                  "roic_sin_arrendamientos": (e * (1 - t) / kp) if ok else None,
                  "roic_propio_pagado_el_alquiler": ((e - i) * (1 - t) / kp) if (ok and i is not None) else None,
                  "celdas": f"Historia!{col[y]}7, {col[y]}10, {col[y]}32, {col[y]}23"}

    def med(clave):
        xs = [por[y][clave] for y in ult]
        return sum(xs) / len(xs) if all(x is not None for x in xs) else None
    faltan_int = [y for y in ult if y not in ints]
    out = {
        "decision": DECISION, "perimetro": per, "perimetro_palancas_s2c": _valor(decl, "perimetro_palancas_s2c"),
        "perimetro_roic": _valor(decl, "perimetro_roic"), "anios": ult, "por_anio": {str(y): v for y, v in por.items()},
        "roic_propio_pagado_el_alquiler_medio": med("roic_propio_pagado_el_alquiler"),
        "roic_sin_arrendamientos_medio": med("roic_sin_arrendamientos"), "roic_todo_el_capital_medio": med("roic_todo_el_capital"),
        "intereses_arrendamiento": {"serie": f"motor_a_f1.json · series.{SERIE_INTERESES}", "fuente_por_anio": fuente, "problemas": probl,
                                    "faltan_anios": faltan_int, "comprobacion_fuentes": fuentes},
        "r": _num(r), "C55_todo_el_capital": _num(c55), "C54_s2c_medio_todo_el_capital": _num(c54), "sector_roic_H18": _num(sector_roic),
        "C53_ancla_s2c": _num(c53), "C58_f": _num(c58), "C52_tau": _num(c52), "C48_m0": _num(m0),
        "formulas": {
            "roic_propio_pagado_el_alquiler": "(EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos); filas 7, 10, "
                                              f"32 y 23 de la Historia y series.{SERIE_INTERESES} de motor_a_f1.json; media simple de {N_ANIOS} años",
            "roic_sin_arrendamientos": "EBIT × (1 − t) ÷ (capital invertido − arrendamientos) (NOPAT NIIF 16 ÷ capital propio); filas 7, 10, 32 y 23",
            "roic_todo_el_capital": "EBIT × (1 − t) ÷ capital invertido (fila 33; su media de cinco años es Historia!C55)",
            "roic_terminal_neutro": "r × N ÷ (N − f), N = margen objetivo × (1 − Historia!C52), f = Historia!C58 (el ROIC terminal con el que el "
                                    "crecimiento perpetuo ni crea ni destruye valor en el motor A)"},
        "regla": REGLA.format(per=per),
    }
    rp = out["roic_propio_pagado_el_alquiler_medio"]
    out["roic_propio_utilizable"] = rp is not None and fuentes["comprobada"]
    ul = ult[-1]
    v, kp = H[6][ul], por[ul]["capital_propio"]
    out["s2c_medio_sin_arrendamientos_ultimo"] = (v / kp) if (v is not None and kp) else None
    out["roic_neutro_con_m0"] = neutro(out["r"], out["C48_m0"], out["C52_tau"], out["C58_f"])
    return out


def anclas_capa(carpeta, libro_sha256):
    """Anclas E4 del S2C que calculó la capa F1 (motor_a_f1_resultado.json, paso 7) SOLO si se calcularon sobre este mismo libro (huella):
    la del perímetro declarado y la cota A1 (sin derechos de uso). None si no hay resultado o es de otro libro."""
    p = os.path.join(carpeta, "motor_a_f1_resultado.json") if carpeta else None
    if not p or not os.path.exists(p):
        return None
    try:
        r = json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None
    if not libro_sha256 or r.get("libro_sha256") != libro_sha256:
        return None
    diag = r.get("diagnostico_por_perimetro") or {}
    return {"declarado": _num((r.get("calculo_perimetro_declarado") or {}).get("ancla_s2c_E4")),
            "A1_sin_ROU": _num((diag.get("A1_sin_ROU") or {}).get("ancla_s2c_E4")), "libro_sha256": libro_sha256}


def neutro(r, m, tau, f):
    """ROIC terminal neutro del motor A: r·N/(N − f), N = m(1 − τ). None si falta algo o N ≤ f."""
    if None in (r, m, tau, f):
        return None
    N = m * (1 - tau)
    return r * N / (N - f) if N - f > 0 else None


def desde_datos(t, decl, carpeta=None):
    """Desde el volcado de leer_v63.todo (datos_v63.json)."""
    h = t["historia"]
    p, s = h["partidas"], h["series"]
    filas = {6: p.get("ventas"), 7: p.get("ebit"), 10: p.get("tipo_impositivo"), 23: p.get("arrendamientos"), 32: s.get("capital_invertido")}
    anc = h.get("anclas") or {}
    try:
        anios = [int(a) for a in p["anio"]]
    except (TypeError, ValueError, KeyError):
        return None
    return calcular(anios, lambda n: filas[n] or [None] * 10, decl, carpeta, r=(t.get("analisis") or {}).get("C56"),
                    c55=anc.get("roic_medio_5"), c54=anc.get("s2c_medio"), sector_roic=((t.get("palancas") or {}).get("sector") or {}).get("roic_media"),
                    c53=anc.get("s2c_marginal"), c58=anc.get("f"), c52=anc.get("tipo_impositivo_5"), m0=anc.get("margen_ultimo"))


def desde_libro(L, decl, carpeta=None):
    """Desde los valores del libro que lee motor_a_f1.leer_libro."""
    anios = [L.get(f"Historia!{c}5") for c in COLS]
    if not all(isinstance(a, (int, float)) for a in anios):
        return None
    g = lambda ref: L.get(ref)  # noqa: E731
    return calcular(anios, lambda n: [L.get(f"Historia!{c}{n}") for c in COLS], decl, carpeta, r=g("Análisis!C56"), c55=g("Historia!C55"),
                    c54=g("Historia!C54"), c53=g("Historia!C53"), c58=g("Historia!C58"), c52=g("Historia!C52"), m0=g("Historia!C48"))


def _cerca(x, a, b):
    """«a» o «b»: a cuál de las dos anclas está más cerca x en proporción (|ln x/a| frente a |ln x/b|). Lectura, no umbral."""
    if None in (x, a, b) or min(x, a, b) <= 0:
        return None
    return "a" if abs(math.log(x / a)) <= abs(math.log(x / b)) else "b"


def guardas_valores(G, L, decl, per, pal, decl_r, diag, carpeta=None):
    """(D3) V-F1g y V-F1k por sus VALORES, no por las etiquetas: las palancas S2C (Palancas!B16:D16) frente al ancla del perímetro y a C54
    (todo el capital), y el ROIC terminal (B18:D18) frente al ROIC neutro del motor con la f del perímetro declarado. Severidad INFORMA, sin
    umbral nuevo: G4 (r + 0,03) y G7 siguen siendo los que exigen justificación. Sin palancas (paso 7) lo dice y no afirma nada.
    Solo con F1 en A1_sin_ROU o A2_propio. Devuelve el detalle numérico (dict) o None."""
    if per not in PERIMETROS_PROPIOS:
        return None
    if not pal:
        for gid in ("V-F1g (valores)", "V-F1k (valores)"):
            G.add(gid, False, None, None, f"perímetro {per} declarado; aún sin palancas (antes de la fase B): las cifras de B16:D16 y B18:D18 no se "
                  "han medido frente a las anclas del perímetro; se miden cuando existen (paso 12)", "(4a) · P-FOSO")
        return {"palancas": None}
    pf = desde_libro(L, decl, carpeta) or {}
    r = _num(L.get("Análisis!C56"))
    f = _num((decl_r or {}).get("f")) if (decl_r or {}).get("f") is not None else _num(L.get("Historia!C58"))
    tau = _num((decl_r or {}).get("tau5")) if (decl_r or {}).get("tau5") is not None else _num(L.get("Historia!C52"))
    ancla = _num((decl_r or {}).get("ancla"))
    cota_a1 = _num(((diag or {}).get("A1_sin_ROU") or {}).get("ancla")) if per == "A2_propio" else None
    c54 = _num(L.get("Historia!C54"))
    s2c_prop = pf.get("s2c_medio_sin_arrendamientos_ultimo")
    # ancla del perímetro: E4 del perímetro declarado; si no es un número > 0, la cota A1 (con A2); si tampoco, el S2C medio sin arrendamientos
    if ancla is not None and ancla > 0:
        ref_per, rot_per = ancla, f"ancla E4 del perímetro {per}"
    elif cota_a1 is not None and cota_a1 > 0:
        ref_per, rot_per = cota_a1, "cota A1 (ancla E4 sin derechos de uso; la de A2 no es calculable)"
    else:
        ref_per, rot_per = s2c_prop, "S2C medio sin arrendamientos del último año (el ancla E4 del perímetro no es un número > 0)"
    out = {"palancas": {}, "ancla_perimetro": ref_per, "ancla_rotulo": rot_per if ref_per is not None else None, "C54_todo_el_capital": c54,
           "s2c_medio_sin_arrendamientos_ultimo": s2c_prop, "r": r, "f": f, "tau": tau,
           "roic_propio_pagado_el_alquiler_medio": pf.get("roic_propio_pagado_el_alquiler_medio"),
           "roic_sin_arrendamientos_medio": pf.get("roic_sin_arrendamientos_medio")}
    txt_g, txt_k, otro = [], [], []
    for esc in ("MALO", "NORMAL", "BUENO"):
        if esc not in pal:
            continue
        pv = {k: _num(v) for k, v in pal[esc].items()}
        s2c, roic, mo = pv.get("s2c"), pv.get("roic"), pv.get("m_obj")
        neu = neutro(r, mo, tau, f)
        lado = _cerca(s2c, ref_per, c54)
        out["palancas"][esc] = {"s2c": s2c, "mas_cerca_de": {"a": "ancla del perímetro", "b": "C54 (todo el capital)"}.get(lado),
                                "roic_terminal": roic, "roic_neutro": neu, "exceso_sobre_neutro": (roic - neu) if (roic is not None and neu is not None) else None}
        txt_g.append(f"{esc} {_f(s2c)}" + (f" (más cerca de {'el ancla del perímetro' if lado == 'a' else 'C54, de todo el capital'})" if lado else ""))
        if lado == "b" and esc == "NORMAL":   # solo el NORMAL marca la fila: el MALO de la referencia (0,75 × NORMAL) cae a menudo hacia C54
            otro.append(esc)
        txt_k.append(f"{esc} {_f(roic)} frente al neutro {_p(neu)}" + (f" ({100 * (roic - neu):+.2f} puntos)" if (roic is not None and neu is not None) else ""))
    G.add("V-F1g (valores)", bool(otro), "INFORMA", "INFORMA",
          f"palancas S2C {'; '.join(txt_g)} · {rot_per if ref_per is not None else 'ancla del perímetro no calculable'} = {_f(ref_per)} · "
          f"S2C medio sin arrendamientos (último año) = {_f(s2c_prop)} · C54 (todo el capital) = {_f(c54)}"
          + (" · NORMAL: la cifra se parece más a la de todo el capital que al ancla del perímetro (¿perímetro cruzado?; lectura, no umbral)" if otro else ""),
          "(4a) · P-FOSO")
    rp = pf.get("roic_propio_pagado_el_alquiler_medio")
    G.add("V-F1k (valores)", True, "INFORMA", "INFORMA",
          f"ROIC terminal {'; '.join(txt_k)} · neutro = r·N/(N − f), N = margen objetivo × (1 − τ), r = {_p(r)}, f del perímetro = {_f(f)} · "
          f"histórico del capital propio pagado todo el alquiler = {_p(rp)} (P-FOSO: frente a r para el foso) · G4 limita el ROIC terminal a r + 0,03 "
          "y sin foso no admite exceso; r no se traduce a otro perímetro", "(4a) · P-FOSO")
    return out


def _p(x, n=2):
    return "—" if x is None else f"{100 * x:.{n}f} %"


def _f(x, n=4):
    return "—" if x is None else f"{x:.{n}g}"


def seccion_md(pf, motor=None):
    """Sección de datos_v63.md para las fases (D2)."""
    if not pf:
        return []
    per, ul = pf["perimetro"], pf["anios"]
    rp, rs, rt = pf["roic_propio_pagado_el_alquiler_medio"], pf["roic_sin_arrendamientos_medio"], pf["roic_todo_el_capital_medio"]
    fi = pf["intereses_arrendamiento"]
    cf = fi["comprobacion_fuentes"]
    r = pf["r"]
    md = [f"## 1 bis. Perímetro F1 declarado y vara del foso ({pf['decision']})\n",
          f"- Perímetro de la reinversión (motor_a_f1.json): **{per}** · palancas S2C: {pf['perimetro_palancas_s2c'] or '—'} · ROIC terminal: "
          f"{pf['perimetro_roic'] or '—'}. F1 solo afecta al motor A" + (f" (motor del libro: {motor})" if motor else "") + ".",
          "- **Qué miden las palancas en este perímetro.** El margen (B15:D15) es el EBIT NIIF 16 (lleva la amortización de los derechos de uso; "
          "el resto del alquiler va en f). El S2C (B16:D16) es ventas nuevas ÷ inversión propia, sin derechos de uso. El ROIC terminal (B18:D18) "
          "está en las unidades del motor y se compara con r: **r no se traduce a otro perímetro** (ya es el listón del flujo del motor) y un "
          "ROIC terminal igual a r no cobra el local dos veces.",
          f"- **Regla (vara del foso):** {pf['regla']}.",
          f"- Historia!C55 y C54 son de **todo el capital** (con los arrendamientos): C55 = {_p(pf['C55_todo_el_capital'])}, frente al sector "
          f"(Palancas!H18) {_p(pf['sector_roic_H18'])}; C54 = {_f(pf['C54_s2c_medio_todo_el_capital'])}. No se comparan con r.\n",
          f"| Año | EBIT | t | Capital invertido | Arrendamientos | Capital propio | Intereses de arrendamiento | ROIC propio pagado el alquiler | "
          f"ROIC sin arrendamientos | ROIC todo el capital | Celdas |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for y in ul:
        e = pf["por_anio"][str(y)]
        md.append(f"| {y} | {_f(e['ebit'], 8)} | {_f(e['t'])} | {_f(e['capital_invertido'], 8)} | {_f(e['arrendamientos'], 8)} | "
                  f"{_f(e['capital_propio'], 8)} | {_f(e['intereses_arrendamiento'], 8)} ({fi['fuente_por_anio'].get(str(y), 'sin declarar')}) | "
                  f"{_p(e['roic_propio_pagado_el_alquiler'])} | {_p(e['roic_sin_arrendamientos'])} | {_p(e['roic_todo_el_capital'])} | {e['celdas']} |")
    exc = (rp - r) if (rp is not None and r is not None) else None
    md += ["", f"- **Media {ul[0]}–{ul[-1]} · ROIC del capital propio pagado todo el alquiler: {_p(rp)}** frente a r (Análisis!C56) {_p(r)}"
           + (f": {100 * exc:+.2f} puntos" if exc is not None else "") + ". Fórmula: " + pf["formulas"]["roic_propio_pagado_el_alquiler"] + ".",
           "  - Intereses de arrendamiento: " + (
               "comprobados en su fuente (cifra publicada en la página citada del documento con su huella; condición mínima de F1-SERIES"
               + (f", columna del ejercicio comprobada en {cf['columna_comprobada']} años" if cf.get("columna_comprobada") else "")
               + (f", PENDIENTE en {len(cf['columna_pendiente'])}" if cf.get("columna_pendiente") else "") + "). No es la verificación de entradas: "
               "la serie no está en el libro ni en el universo de verificacion_entradas.py." if cf["comprobada"] else
               "**NO COMPROBADOS** (" + "; ".join((fi["problemas"] + cf["invalidas"] + cf["incompletas"])[:6]) + "): la media de arriba "
               + ("no es calculable" if rp is None else "es una cifra sin comprobar") + "; para usarla, declarar "
               "series.intereses_arrendamiento en motor_a_f1.json (documento, página, fila y literal por año) en un expediente nuevo."),
           f"- **Media {ul[0]}–{ul[-1]} · ROIC sin arrendamientos (NOPAT NIIF 16 ÷ capital propio): {_p(rs)}** · ancla de G7 y del tope de la "
           f"referencia mecánica del S2C en el perímetro del S2C: 2 × {_p(rs)} = {_p(2 * rs if rs is not None else None)} "
           f"(no 2 × C55 = {_p(2 * pf['C55_todo_el_capital'] if pf['C55_todo_el_capital'] is not None else None)}). Fórmula: "
           + pf["formulas"]["roic_sin_arrendamientos"] + ".",
           f"- Media {ul[0]}–{ul[-1]} · ROIC de todo el capital: {_p(rt)} (Historia!C55 = {_p(pf['C55_todo_el_capital'])}): solo frente al sector.",
           f"- S2C del perímetro: ancla Historia!C53 (con D_X del perímetro) = {_f(pf['C53_ancla_s2c'])}"
           + ((" (vacía: el ancla del perímetro no es calculable" + (f"; cota A1 de la capa F1 sobre este libro, sin derechos de uso: "
                                                                       f"{_f((pf.get('anclas_capa_f1') or {}).get('A1_sin_ROU'))})"
                                                                       if (pf.get("anclas_capa_f1") or {}).get("A1_sin_ROU") is not None else
                                                                       "; la capa F1 da la cota A1 en motor_a_f1_resultado.md)"))
              if pf["C53_ancla_s2c"] is None else "")
           + f" · S2C medio sin arrendamientos {ul[-1]} (ventas ÷ capital propio) = {_f(pf['s2c_medio_sin_arrendamientos_ultimo'])}"
           f" · C54 (todo el capital) = {_f(pf['C54_s2c_medio_todo_el_capital'])}.",
           f"- ROIC terminal neutro del motor: {pf['formulas']['roic_terminal_neutro']}. Con el margen de partida (Historia!C48 = "
           f"{_f(pf['C48_m0'])}) y f = {_f(pf['C58_f'])}: {_p(pf['roic_neutro_con_m0'])}; con el margen objetivo de cada escenario cambia poco "
           "si f es pequeño (la capa F1 lo da por escenario tras la fase B). Un ROIC terminal por encima de él es retorno en exceso sobre el "
           "capital nuevo para siempre: es la afirmación sobre el foso que G4 limita a r + 0,03.\n"]
    return md
