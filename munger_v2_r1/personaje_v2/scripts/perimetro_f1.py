#!/usr/bin/env python3
"""Retornos históricos en el perímetro F1 declarado y vara del foso (decisión P-FOSO, opción a, 18-nov-2026; dictamen
examen/revisiones/dictamen_perimetro_g4/DICTAMEN.md, defectos D1, D2 y D3; revisión de la implantación REVISION_IMPLANTACION.md, C1–C4).

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
devuelve None y nada cambia.
Intereses de arrendamiento (C1 de la revisión). La serie no está en el libro ni en el universo de verificacion_entradas.py: su comprobación
es la condición mínima de F1-SERIES (cifra publicada con su signo, en la página, con la huella del documento) y, además, la columna del
ejercicio comprobada en los cinco años (por eso cada año declara «fila»). Solo así la medida es UTILIZABLE: si no, la sección «1 bis» no la
titula ni la compara con r, «V-F1k (valores)» avisa y las referencias mecánicas no la usan; si la fuente es INVÁLIDA, la capa F1 bloquea.
Límites declarados: solo NIIF (con US GAAP el arrendamiento operativo va entero en el EBIT y la fórmula restaría su interés otra vez: la
medida no se emite, C3); la decisión nombra A2_propio y se aplica igual a A1_sin_ROU (mismo trato del arrendamiento: extensión que la
persona conoce); sin el ajuste de la I+D capitalizada que lleva C55 con Palancas!C9 = Sí; con menos de cinco ejercicios en la Historia, la
medida no se emite y se dice; el semáforo del libro de la rentabilidad marginal (Diagnóstico V6, fila 42) sigue con 2 × C55; el capital
propio es el capital invertido menos el PASIVO por arrendamientos (la definición del libro), y pierde sentido si es pequeño o negativo.
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
G4_TEXTO = ("G4 no cambia: hasta r + 0,03 no pide nada; por encima de r + 0,03 exige C18 = Sí y una justificación de cuánto dura la ventaja "
            "(sin foso, por encima de r + 0,03 no hay justificación posible)")
ESTADOS_INTERESES = ("comprobada", "sin_declarar", "incompleta", "columna_pendiente", "invalida")
LIMITES = ("la decisión nombra A2_propio; aquí se aplica igual a A1_sin_ROU (mismo trato del arrendamiento), extensión que la persona conoce",
           "el semáforo del libro de la rentabilidad marginal (Diagnóstico V6, fila 42) sigue comparando con 2 × C55, de todo el capital: con F1 en "
           "este perímetro manda G7 de la gramática",
           "el capital propio es el capital invertido menos el pasivo por arrendamientos (la definición del libro, no el activo por derecho de uso); "
           "con un capital propio pequeño o negativo las medidas pierden sentido")


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
    s = ((decl.get("series") or {}).get(SERIE_INTERESES)) or {}
    for k, e in (s.items() if isinstance(s, dict) else []):
        if isinstance(e, dict):
            fuente[str(k)] = f"{e.get('documento')} p. {e.get('pagina')}" + (f" · «{e.get('fila')}»" if e.get("fila") else " · sin «fila»")
    return {y: float(v) for y, v in serie.items()}, probl, fuente


def comprobar_fuentes(decl, carpeta, anios):
    """Condición mínima de F1-SERIES (motor_a_f1._guarda_fuentes_series, la misma función, aplicada a esta serie sola) sobre los años `anios`.
    Devuelve {"invalidas", "incompletas", "columna_comprobada", "columna_pendiente"}."""
    import motor_a_f1 as F1
    s = ((decl.get("series") or {}).get(SERIE_INTERESES)) if isinstance(decl, dict) else None
    if not isinstance(s, dict) or not s:
        return {"invalidas": [], "incompletas": [f"series.{SERIE_INTERESES} sin declarar en motor_a_f1.json"], "columna_comprobada": 0,
                "columna_pendiente": []}
    sub = {"series": {"da_rou": {k: v for k, v in s.items() if str(k) in {str(a) for a in anios}}}, "fuentes_series": decl.get("fuentes_series")}
    G, res = F1.Guardas(), {}
    F1._guarda_fuentes_series(G, sub, carpeta, list(anios), res)
    fs = res.get("F1_SERIES") or {}
    ren = lambda xs: [str(x).replace("series.da_rou", f"series.{SERIE_INTERESES}") for x in xs]  # noqa: E731
    return {"invalidas": ren(fs.get("invalidas") or []), "incompletas": ren(fs.get("incompletas") or []),
            "columna_comprobada": fs.get("columna_comprobada", 0), "columna_pendiente": ren(fs.get("columna_pendiente") or [])}


def estado_intereses(declarada, probl, faltan, cf, n):
    """C1: «comprobada» solo con la cifra en su página Y la columna del ejercicio comprobada en los n años. «invalida»: la lectura de la serie
    (signo, valor) o su fuente fallan. «incompleta»: faltan años o la fuente no se pudo examinar. «columna_pendiente»: sin «fila» o columna no
    identificable (la cifra podría ser la de otra fila u otro ejercicio de la misma página)."""
    if not declarada:
        return "sin_declarar"
    if probl or cf["invalidas"]:
        return "invalida"
    if faltan or cf["incompletas"]:
        return "incompleta"
    if cf["columna_pendiente"] or cf["columna_comprobada"] < n:
        return "columna_pendiente"
    return "comprobada"


def _no_aplicable(out, motivo):
    out.update({"aplicable": False, "motivo_no_aplicable": motivo, "roic_propio_pagado_el_alquiler_medio": None, "roic_sin_arrendamientos_medio": None,
                "roic_todo_el_capital_medio": None, "roic_propio_utilizable": False, "s2c_medio_sin_arrendamientos_ultimo": None, "roic_neutro_con_m0": None})
    return out


def calcular(anios, fila, decl, carpeta=None, r=None, c55=None, c54=None, sector_roic=None, c53=None, c58=None, c52=None, m0=None, id_capitalizada=None):
    """Bloque del perímetro F1. anios: los diez años de la Historia (fila 5; un vacío es None); fila(n) → lista de diez valores de la fila n de la
    Historia (7 EBIT, 10 tipo, 23 arrendamientos, 32 capital invertido, 6 ventas). None si no hay perímetro F1 declarado sin derechos de uso;
    con perímetro pero sin medida posible (US GAAP, menos de cinco ejercicios), un bloque con «aplicable»: False y su motivo (se dice, no
    desaparece)."""
    per = perimetro_declarado(decl)
    if per is None:
        return None
    norma = _valor(decl, "norma_contable")
    out = {"decision": DECISION, "perimetro": per, "perimetro_palancas_s2c": _valor(decl, "perimetro_palancas_s2c"),
           "perimetro_roic": _valor(decl, "perimetro_roic"), "norma_contable": norma, "aplicable": True, "motivo_no_aplicable": None,
           "r": _num(r), "C55_todo_el_capital": _num(c55), "C54_s2c_medio_todo_el_capital": _num(c54), "sector_roic_H18": _num(sector_roic),
           "C53_ancla_s2c": _num(c53), "C58_f": _num(c58), "C52_tau": _num(c52), "C48_m0": _num(m0),
           "id_capitalizada": id_capitalizada == "Sí", "regla": REGLA.format(per=per), "g4": G4_TEXTO, "limites": list(LIMITES),
           "formulas": {
               "roic_propio_pagado_el_alquiler": "(EBIT − intereses de arrendamiento) × (1 − t) ÷ (capital invertido − arrendamientos); filas 7, 10, "
                                                 f"32 y 23 de la Historia y series.{SERIE_INTERESES} de motor_a_f1.json; media simple de {N_ANIOS} años",
               "roic_sin_arrendamientos": "EBIT × (1 − t) ÷ (capital invertido − arrendamientos) (NOPAT NIIF 16 ÷ capital propio); filas 7, 10, 32 y 23",
               "roic_todo_el_capital": "EBIT × (1 − t) ÷ capital invertido (fila 33; su media de cinco años es Historia!C55)",
               "roic_terminal_neutro": "r × N ÷ (N − f), N = margen objetivo × (1 − Historia!C52), f = Historia!C58 (el ROIC terminal con el que el "
                                       "crecimiento perpetuo ni crea ni destruye valor en el motor A)"}}
    if norma != "NIIF":
        # (C3) con US GAAP el arrendamiento operativo va entero en el EBIT (un solo coste lineal): restar sus «intereses» lo contaría dos veces
        return _no_aplicable(out, f"norma contable {norma!r}: la medida solo tiene fórmula con NIIF (NIIF 16). Con US GAAP el arrendamiento operativo "
                                  "va entero en el EBIT y restarle su interés lo contaría dos veces; no se emite hasta que tenga su fórmula. G7 y las "
                                  "referencias usan C55, de todo el capital, como antes")
    pos = [(i, int(a)) for i, a in enumerate(anios) if isinstance(a, (int, float)) and not isinstance(a, bool) and int(a) == a]
    ult_pos = pos[-N_ANIOS:]
    if len(ult_pos) < N_ANIOS or [p for p, _ in ult_pos] != list(range(len(anios) - N_ANIOS, len(anios))) \
            or [y for _, y in ult_pos] != list(range(ult_pos[0][1], ult_pos[0][1] + N_ANIOS)):
        return _no_aplicable(out, f"la Historia no tiene los {N_ANIOS} últimos ejercicios seguidos (fila 5): sin la media de {N_ANIOS} años, G7 y "
                                  "las referencias usan C55, de todo el capital, como antes")
    filas = {n: list(fila(n)) for n in (6, 7, 10, 23, 32)}
    H = {n: {y: _num(filas[n][i]) if i < len(filas[n]) else None for i, y in ult_pos} for n in filas}
    col = {y: COLS[i] for i, y in ult_pos}
    ult = [y for _, y in ult_pos]
    ints, probl, fuente = intereses(decl, [y for _, y in pos])
    declarada = bool(((decl.get("series") or {}).get(SERIE_INTERESES)))
    faltan_int = [y for y in ult if y not in ints]
    cf = comprobar_fuentes(decl, carpeta, ult) if declarada else {"invalidas": [], "incompletas": [], "columna_comprobada": 0, "columna_pendiente": []}
    estado = estado_intereses(declarada, probl, faltan_int, cf, N_ANIOS)
    cf["comprobada"] = estado == "comprobada"   # (C1) con la columna del ejercicio comprobada en los cinco años, no solo la cifra en la página
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
    rp = med("roic_propio_pagado_el_alquiler")
    out.update({
        "anios": ult, "por_anio": {str(y): v for y, v in por.items()},
        "roic_propio_pagado_el_alquiler_medio": rp, "roic_sin_arrendamientos_medio": med("roic_sin_arrendamientos"),
        "roic_todo_el_capital_medio": med("roic_todo_el_capital"),
        "intereses_arrendamiento": {"serie": f"motor_a_f1.json · series.{SERIE_INTERESES}", "declarada": declarada, "estado": estado,
                                    "fuente_por_anio": fuente, "problemas": probl, "faltan_anios": faltan_int, "comprobacion_fuentes": cf},
        "roic_propio_utilizable": rp is not None and estado == "comprobada"})
    ul = ult[-1]
    v, kp = H[6][ul], por[ul]["capital_propio"]
    out["s2c_medio_sin_arrendamientos_ultimo"] = (v / kp) if (v is not None and kp) else None
    out["roic_neutro_con_m0"] = neutro(out["r"], out["C48_m0"], out["C52_tau"], out["C58_f"])
    return out


def problemas_intereses(pf):
    """Texto de por qué la serie de intereses no es utilizable (vacío si lo es)."""
    fi = (pf or {}).get("intereses_arrendamiento") or {}
    cf = fi.get("comprobacion_fuentes") or {}
    est = fi.get("estado")
    if est == "comprobada":
        return ""
    if est == "sin_declarar":
        return f"series.{SERIE_INTERESES} sin declarar en motor_a_f1.json"
    if est == "columna_pendiente":
        return ("columna del ejercicio sin comprobar en " + str(max(len(cf.get("columna_pendiente") or []), N_ANIOS - (cf.get("columna_comprobada") or 0)))
                + " años (cada año declara «fila» con la etiqueta de la línea; sin ella, la cifra podría ser la de otra fila u otro ejercicio de la "
                  "misma página): " + "; ".join((cf.get("columna_pendiente") or [])[:3]))
    return "; ".join(((fi.get("problemas") or []) + (cf.get("invalidas") or []) + (cf.get("incompletas") or [])
                      + [f"falta el año {y}" for y in fi.get("faltan_anios") or []])[:6])


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
    anios = list(p.get("anio") or [None] * 10)
    return calcular(anios, lambda n: filas[n] or [None] * 10, decl, carpeta, r=(t.get("analisis") or {}).get("C56"),
                    c55=anc.get("roic_medio_5"), c54=anc.get("s2c_medio"), sector_roic=((t.get("palancas") or {}).get("sector") or {}).get("roic_media"),
                    c53=anc.get("s2c_marginal"), c58=anc.get("f"), c52=anc.get("tipo_impositivo_5"), m0=anc.get("margen_ultimo"),
                    id_capitalizada=(t.get("palancas") or {}).get("C9"))


def desde_libro(L, decl, carpeta=None):
    """Desde los valores del libro que lee motor_a_f1.leer_libro."""
    g = lambda ref: L.get(ref)  # noqa: E731
    return calcular([L.get(f"Historia!{c}5") for c in COLS], lambda n: [L.get(f"Historia!{c}{n}") for c in COLS], decl, carpeta,
                    r=g("Análisis!C56"), c55=g("Historia!C55"), c54=g("Historia!C54"), c53=g("Historia!C53"), c58=g("Historia!C58"),
                    c52=g("Historia!C52"), m0=g("Historia!C48"))


def _cerca(x, a, b):
    """«a» o «b»: a cuál de las dos cifras está más cerca x en proporción (|ln x/a| frente a |ln x/b|). Lectura, no umbral."""
    if None in (x, a, b) or min(x, a, b) <= 0:
        return None
    return "a" if abs(math.log(x / a)) <= abs(math.log(x / b)) else "b"


def lectura_palancas(pf, pal, r, tau, f, ancla=None, rot_ancla=None):
    """(D3, C4) Lectura de las palancas en el perímetro, común a la capa F1 (paso 12) y a la gramática (pasos 8–10, que lee la fase C).
    pal: {escenario: {"s2c", "roic", "m_obj"}}. El S2C se compara MEDIO con MEDIO (S2C medio sin arrendamientos frente a C54, de todo el
    capital): lectura orientativa, no umbral; el ancla marginal del perímetro se da aparte. El ROIC terminal, frente al neutro r·N/(N − f).
    Devuelve (detalle por escenario, texto del S2C, texto del ROIC, ¿el NORMAL se parece más al medio de todo el capital?)."""
    s2c_prop, c54 = (pf or {}).get("s2c_medio_sin_arrendamientos_ultimo"), (pf or {}).get("C54_s2c_medio_todo_el_capital")
    det, tg, tk, cruzado = {}, [], [], False
    for esc in ("MALO", "NORMAL", "BUENO"):
        pv = {k: _num(v) for k, v in ((pal or {}).get(esc) or {}).items()}
        if not pv:
            continue
        s2c, roic, mo = pv.get("s2c"), pv.get("roic"), pv.get("m_obj")
        neu = neutro(r, mo, tau, f)
        lado = _cerca(s2c, s2c_prop, c54)
        cerca_de = {"a": "S2C medio sin arrendamientos", "b": "C54 (todo el capital)"}.get(lado)
        det[esc] = {"s2c": s2c, "mas_cerca_de_medio": cerca_de, "mas_cerca_de": cerca_de,
                    "roic_terminal": roic, "roic_neutro": neu, "exceso_sobre_neutro": (roic - neu) if (roic is not None and neu is not None) else None}
        tg.append(f"{esc} {_f(s2c)}" + (f" (más cerca del {'medio sin arrendamientos' if lado == 'a' else 'medio de todo el capital, C54'})" if lado else ""))
        if lado == "b" and esc == "NORMAL":   # solo el NORMAL: el MALO de la referencia (0,75 × NORMAL) cae a menudo hacia C54
            cruzado = True
        tk.append(f"{esc} {_f(roic)} frente al neutro {_p(neu)}" + (f" ({100 * (roic - neu):+.2f} puntos)" if (roic is not None and neu is not None) else ""))
    dif = (s2c_prop / c54 - 1) if (s2c_prop and c54) else None
    txt_s2c = (f"palancas S2C {'; '.join(tg)} · S2C medio sin arrendamientos (último año) = {_f(s2c_prop)} · C54 (medio de todo el capital) = {_f(c54)}"
               + (f" (difieren un {100 * dif:.0f} %)" if dif is not None else "")
               + f" · ancla marginal del perímetro, aparte: {rot_ancla or 'Historia!C53'} = {_f(ancla)}"
               + (" · NORMAL más cerca del medio de todo el capital: ¿perímetro cruzado? (lectura orientativa, no umbral; con medios parecidos "
                  "no discrimina)" if cruzado else " · lectura orientativa, no umbral"))
    rp = (pf or {}).get("roic_propio_pagado_el_alquiler_medio")
    txt_roic = (f"ROIC terminal {'; '.join(tk)} · neutro = r·N/(N − f), N = margen objetivo × (1 − τ), r = {_p(r)}, f del perímetro = {_f(f)} · "
                + (f"histórico del capital propio pagado todo el alquiler = {_p(rp)} (P-FOSO: frente a r para el foso)" if (pf or {}).get("roic_propio_utilizable")
                   else f"histórico del capital propio pagado todo el alquiler NO COMPROBADO ({problemas_intereses(pf)}): no se compara con r")
                + f" · {G4_TEXTO}; r no se traduce a otro perímetro")
    return det, txt_s2c, txt_roic, cruzado


def guardas_valores(G, L, decl, per, pal, decl_r, diag, carpeta=None):
    """(D3) V-F1g y V-F1k por sus VALORES, no por las etiquetas: las palancas S2C (Palancas!B16:D16) y el ROIC terminal (B18:D18) frente a las
    medidas del perímetro. INFORMA, sin umbral nuevo (G4 y G7 siguen siendo los que exigen justificación); «V-F1k (valores)» AVISA si la
    medida del foso no es utilizable. (C1) Una serie de intereses declarada con su fuente o su lectura INVÁLIDAS bloquea (DATOS INVÁLIDOS),
    como F1-SERIES. Sin palancas (paso 7) lo dice y no afirma nada. Solo con F1 en A1_sin_ROU o A2_propio. Devuelve el detalle o None."""
    if per not in PERIMETROS_PROPIOS:
        return None
    pf = desde_libro(L, decl, carpeta) or {}
    if not pf.get("aplicable"):
        for gid in ("V-F1g (valores)", "V-F1k (valores)"):
            G.add(gid, False, None, None, f"perímetro {per} declarado; medidas del perímetro no aplicables: {pf.get('motivo_no_aplicable')}", "(4a) · P-FOSO")
        return {"palancas": None, "aplicable": False, "motivo_no_aplicable": pf.get("motivo_no_aplicable")}
    fi = pf.get("intereses_arrendamiento") or {}
    if fi.get("estado") == "invalida":
        G.add("F1-INTERESES-ARR", True, "BLOQUEA", "DATOS INVÁLIDOS",
              f"series.{SERIE_INTERESES} declarada con la lectura o la fuente inválidas ({problemas_intereses(pf)[:900]}): la medida del foso "
              "(P-FOSO) no se usa y la declaración se corrige", "P-FOSO · C1")
    else:
        G.add("F1-INTERESES-ARR", False, None, None, f"series.{SERIE_INTERESES}: {fi.get('estado')}" + (f" ({problemas_intereses(pf)[:300]})" if fi.get("estado") != "comprobada" else ""),
              "P-FOSO · C1")
    out = {"palancas": None, "aplicable": True, "intereses_estado": fi.get("estado"), "roic_propio_utilizable": pf.get("roic_propio_utilizable"),
           "roic_propio_pagado_el_alquiler_medio": pf.get("roic_propio_pagado_el_alquiler_medio"),
           "roic_sin_arrendamientos_medio": pf.get("roic_sin_arrendamientos_medio")}
    if not pal:
        for gid in ("V-F1g (valores)", "V-F1k (valores)"):
            G.add(gid, False, None, None, f"perímetro {per} declarado; aún sin palancas (antes de la fase B): las cifras de B16:D16 y B18:D18 no se "
                  "han medido frente a las medidas del perímetro; se miden cuando existen (gramática tras la fase B y capa F1 en el paso 12)", "(4a) · P-FOSO")
        return out
    r = _num(L.get("Análisis!C56"))
    f = _num((decl_r or {}).get("f")) if (decl_r or {}).get("f") is not None else _num(L.get("Historia!C58"))
    tau = _num((decl_r or {}).get("tau5")) if (decl_r or {}).get("tau5") is not None else _num(L.get("Historia!C52"))
    ancla = _num((decl_r or {}).get("ancla"))
    cota_a1 = _num(((diag or {}).get("A1_sin_ROU") or {}).get("ancla")) if per == "A2_propio" else None
    if ancla is not None and ancla > 0:
        ref, rot = ancla, f"ancla E4 del perímetro {per}"
    elif cota_a1 is not None and cota_a1 > 0:
        ref, rot = cota_a1, "cota A1 (ancla E4 sin derechos de uso; la de A2 no es calculable)"
    else:
        ref, rot = None, "ancla E4 del perímetro (no es un número > 0)"
    det, txt_g, txt_k, cruzado = lectura_palancas(pf, pal, r, tau, f, ref, rot)
    out.update({"palancas": det, "ancla_perimetro": ref, "ancla_rotulo": rot, "C54_todo_el_capital": pf.get("C54_s2c_medio_todo_el_capital"),
                "s2c_medio_sin_arrendamientos_ultimo": pf.get("s2c_medio_sin_arrendamientos_ultimo"), "r": r, "f": f, "tau": tau})
    G.add("V-F1g (valores)", True, "INFORMA", "INFORMA", txt_g, "(4a) · P-FOSO")   # informa siempre (con cifras): la ficha y el informe la recogen
    util = bool(pf.get("roic_propio_utilizable"))
    G.add("V-F1k (valores)", True, "INFORMA" if util else "AVISO", "INFORMA" if util else "AVISO", txt_k, "(4a) · P-FOSO")
    return out


def _p(x, n=2):
    return "—" if x is None else f"{100 * x:.{n}f} %"


def _f(x, n=4):
    return "—" if x is None else f"{x:.{n}g}"


def seccion_md(pf, motor=None):
    """Sección de datos_v63.md para las fases (D2)."""
    if not pf:
        return []
    per = pf["perimetro"]
    cab = [f"## 1 bis. Perímetro F1 declarado y vara del foso ({pf['decision']})\n",
           f"- Perímetro de la reinversión (motor_a_f1.json): **{per}** · palancas S2C: {pf['perimetro_palancas_s2c'] or '—'} · ROIC terminal: "
           f"{pf['perimetro_roic'] or '—'} · norma contable: {pf.get('norma_contable') or 'sin declarar'}. F1 solo afecta al motor A"
           + (f" (motor del libro: {motor})" if motor else "") + "."]
    if not pf.get("aplicable"):
        return cab + [f"- **Medidas del perímetro NO APLICABLES:** {pf.get('motivo_no_aplicable')}. La regla de la decisión (P-FOSO) queda sin su cifra: "
                      "no compares Historia!C55 (todo el capital) con r como si fuera la del accionista; dilo en la Observación de C18.\n"]
    ul = pf["anios"]
    rp, rs, rt = pf["roic_propio_pagado_el_alquiler_medio"], pf["roic_sin_arrendamientos_medio"], pf["roic_todo_el_capital_medio"]
    fi = pf["intereses_arrendamiento"]
    cf = fi["comprobacion_fuentes"]
    r, c55, h18 = pf["r"], pf["C55_todo_el_capital"], pf["sector_roic_H18"]
    util = pf.get("roic_propio_utilizable")
    md = cab + [
        "- **Qué miden las palancas en este perímetro.** El margen (B15:D15) es el EBIT NIIF 16 (lleva la amortización de los derechos de uso; "
        "el resto del alquiler va en f). El S2C (B16:D16) es ventas nuevas ÷ inversión propia, sin derechos de uso. El ROIC terminal (B18:D18) "
        "está en las unidades del motor y se compara con r: **r no se traduce a otro perímetro** (ya es el listón del flujo del motor) y un "
        "ROIC terminal igual a r no cobra el local dos veces.",
        f"- **Regla (vara del foso):** {pf['regla']}.",
        f"- Historia!C55 y C54 son de **todo el capital** (con los arrendamientos): no se comparan con r.\n",
        f"| Año | EBIT | t | Capital invertido | Arrendamientos | Capital propio | Intereses de arrendamiento | ROIC propio pagado el alquiler | "
        f"ROIC sin arrendamientos | ROIC todo el capital | Celdas |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for y in ul:
        e = pf["por_anio"][str(y)]
        md.append(f"| {y} | {_f(e['ebit'], 8)} | {_f(e['t'])} | {_f(e['capital_invertido'], 8)} | {_f(e['arrendamientos'], 8)} | "
                  f"{_f(e['capital_propio'], 8)} | {_f(e['intereses_arrendamiento'], 8)} ({fi['fuente_por_anio'].get(str(y), 'sin declarar')}) | "
                  f"{_p(e['roic_propio_pagado_el_alquiler']) if util else '(sin comprobar)'} | {_p(e['roic_sin_arrendamientos'])} | "
                  f"{_p(e['roic_todo_el_capital'])} | {e['celdas']} |")
    md.append("")
    if util:
        peor = min(pf["por_anio"][str(y)]["roic_propio_pagado_el_alquiler"] for y in ul)
        md += [f"- **Media {ul[0]}–{ul[-1]} · ROIC del capital propio pagado todo el alquiler: {_p(rp)}** frente a r (Análisis!C56) {_p(r)}: "
               f"{100 * (rp - r):+.2f} puntos (peor año {_p(peor)})." if r is not None else
               f"- **Media {ul[0]}–{ul[-1]} · ROIC del capital propio pagado todo el alquiler: {_p(rp)}** (r no disponible).",
               f"  - Fórmula: {pf['formulas']['roic_propio_pagado_el_alquiler']}. Intereses comprobados en su fuente: cifra publicada en la página citada "
               f"del documento con su huella y columna del ejercicio comprobada en los {N_ANIOS} años (condición mínima de F1-SERIES). No es la "
               "verificación de entradas: la serie no está en el libro ni en el universo de verificacion_entradas.py."]
    else:
        md += [f"- Media {ul[0]}–{ul[-1]} · ROIC del capital propio pagado todo el alquiler: **NO COMPROBADO** ({fi['estado']}: {problemas_intereses(pf)}). "
               + ("No es calculable" if rp is None else "La cifra sin comprobar no se titula ni se compara con r")
               + ": la regla de la decisión queda sin su cifra; no apoyes C18 en ella. Para usarla, declarar series.intereses_arrendamiento en "
               "motor_a_f1.json (documento, página, «fila» y literal por año, los cinco años) en un expediente nuevo."]
    md += [f"- **Media {ul[0]}–{ul[-1]} · ROIC de todo el capital (Historia!C55): {_p(c55)}** frente al sector (Palancas!H18) {_p(h18)}"
           + (f": {100 * (c55 - h18):+.2f} puntos" if (c55 is not None and h18 is not None) else "") + " (misma vara a los dos lados)."
           + (f" **Con la fila 33 sale {_p(rt)}, distinto de C55**: C55 lleva otro ajuste (con I+D capitalizada, la fila 38) que las medidas "
              "del perímetro de esta sección no llevan." if (rt is not None and c55 is not None and abs(rt - c55) > 1e-9) else ""),
           f"- **Media {ul[0]}–{ul[-1]} · ROIC sin arrendamientos (NOPAT NIIF 16 ÷ capital propio): {_p(rs)}** · ancla de G7 y del tope de la "
           f"referencia mecánica del S2C en el perímetro del S2C: 2 × {_p(rs)} = {_p(2 * rs if rs is not None else None)} "
           f"(no 2 × C55 = {_p(2 * c55 if c55 is not None else None)}). Fórmula: " + pf["formulas"]["roic_sin_arrendamientos"] + ".",
           f"- S2C del perímetro: ancla Historia!C53 (marginal, con D_X del perímetro) = {_f(pf['C53_ancla_s2c'])}"
           + ((" (vacía: el ancla del perímetro no es calculable" + (f"; cota A1 de la capa F1 sobre este libro, sin derechos de uso: "
                                                                       f"{_f((pf.get('anclas_capa_f1') or {}).get('A1_sin_ROU'))})"
                                                                       if (pf.get("anclas_capa_f1") or {}).get("A1_sin_ROU") is not None else
                                                                       "; la capa F1 da la cota A1 en motor_a_f1_resultado.md)"))
              if pf["C53_ancla_s2c"] is None else "")
           + f" · S2C medio sin arrendamientos {ul[-1]} (ventas ÷ capital propio) = {_f(pf['s2c_medio_sin_arrendamientos_ultimo'])}"
           f" · C54 (medio de todo el capital) = {_f(pf['C54_s2c_medio_todo_el_capital'])}.",
           f"- ROIC terminal neutro del motor: {pf['formulas']['roic_terminal_neutro']}. Con el margen de partida (Historia!C48 = "
           f"{_f(pf['C48_m0'])}) y f = {_f(pf['C58_f'])}: {_p(pf['roic_neutro_con_m0'])}; con el margen objetivo de cada escenario cambia poco "
           "si f es pequeño (la gramática lo da por escenario tras la fase B). Por encima de él, el ROIC terminal afirma retorno en exceso sobre "
           f"el capital nuevo para siempre. {pf['g4']}.",
           "- Límites: " + "; ".join(pf["limites"] + (["**I+D capitalizada (Palancas!C9 = Sí): C55 usa la fila 38 con la I+D capitalizada; estas medidas "
                                                        "no llevan ese ajuste**"] if pf.get("id_capitalizada") else [])) + ".\n"]
    return md
