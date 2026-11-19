#!/usr/bin/env python3
"""Perímetro F1 en el libro V6.3.1 F1 del motor A (F1-IMPL, recomendación (a) de la revisión): aplicar la declaración al libro y
comprobar que el libro calcula lo declarado.

Qué hace.
  - aplicar: escribe en un libro V6.3.1 F1 (Historia C85:L87 y M85:M87) el perímetro de la reinversión y las series D&A de derechos de
    uso y PPA de la declaración F1 del expediente (motor_a_f1.json), con la misma lectura de las series que motor_a_f1.py (signo ×
    valor_fuente; una entrada inválida no se escribe: queda vacía, que no es cero). Solo A0_total, A1_sin_ROU y A2_propio existen en el
    libro; con otro perímetro (A3_estimado) o sin declaración, C85 queda VACÍO (= A0, el de la V6.3) y la capa sigue bloqueando.
    Siempre reescribe las tres filas entera (lo no declarado queda vacío): no deja valores de una declaración anterior.
  - perimetro_del_libro / replica_dx / corresponde: las usa motor_a_f1.py. La capa queda como ORÁCULO: F1-LIBRO deja de bloquear solo
    si el libro es V6.3.1 F1, su perímetro efectivo es el declarado, sus series y D_X son las declaradas, y f, el ancla y los flujos del
    Motor coinciden con los de la capa; cualquier diferencia bloquea.
No elige ningún perímetro ni ninguna serie: copia la declaración, que rellena la persona.
(19-nov-2026, V-CIRC) Libro V6.3.2 F1 (la V6.3.1 F1 con la sección «NORMALIZACIÓN DEL CIRCULANTE», Historia filas 92–98): `aplicar` escribe además
la regla (C93) y los años normalizados (C94:L94, 1 o vacío) de `normalizacion_circulante`, con la misma lectura que la capa
(motor_a_f1.leer_circulante): solo si la forma es válida y la norma declarada es NIIF; si no, C93:L94 quedan vacías (= sin normalización) y la
capa bloquea (F1-CIRC). En un libro V6.3.1 F1 esas celdas no existen y no se escriben: la capa bloquea con F1-LIBRO si la normalización tiene efecto.
`normalizacion_del_libro` y `replica_circulante` leen y contrastan la sección; `corresponde` contrasta también la normalización declarada.

Uso: f1_libro_v631.py aplicar LIBRO_V631.xlsx SALIDA.xlsx CARPETA_O_DECLARACION   (sin motor_a_f1.json en la carpeta: filas vacías)
"""
import json
import os
import sys
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)

PERIMETROS_LIBRO = ("A0_total", "A1_sin_ROU", "A2_propio")
COLS = "CDEFGHIJKL"
F_SEL, F_ROU, F_PPA, F_DX, F_EF = 85, 86, 87, 88, 89
MARCA = "PERÍMETRO F1 DE LA REINVERSIÓN"   # Historia A84 de la V6.3.1 F1
TOL_F, TOL = Fr(1, 10 ** 12), Fr(1, 10 ** 9)
# (V-CIRC) sección de la V6.3.2 F1: título (A92), regla (C93), años normalizados (C94:L94), circulante excluido (C95:L95), circulante que usa la
# reinversión (C96:L96) y normalización efectiva (C97)
F_CTIT, F_CREG, F_CANI, F_CEXC, F_CUSA, F_CEF = 92, 93, 94, 95, 96, 97
MARCA_CIRC = "NORMALIZACIÓN DEL CIRCULANTE"   # Historia A92 de la V6.3.2 F1
REGLA_CIRC = "circulante_a_cero"               # = motor_a_f1.REGLA_CIRCULANTE
EFECTIVAS_ACTIVAS = (REGLA_CIRC, "no reconocida")   # Historia C97 distinto de «ninguna»: el libro no calcula como la V6.3.1 F1


def _Q(x):
    import motor_a_f1 as F1
    return F1.Q(x)


# ------------------------------------------------------------------------------------------------------------ aplicar
def celdas(decl, anios, circulante=False):
    """{"Historia!REF": valor} de las filas 85–87 desde la declaración (dict) y los años de la Historia (C5:L5 del libro). (V-CIRC) Con
    circulante=True (libro V6.3.2 F1), también C93 (regla), C94:L94 (años normalizados: 1 o vacío) y su procedencia en M93:M94; vacías sin una
    normalización aplicable (motor_a_f1.leer_circulante: forma válida y norma NIIF)."""
    import motor_a_f1 as F1
    decl = decl if isinstance(decl, dict) else {}
    # (F1 · US GAAP, ronda 2, R1-14) una serie o una clave mal formada no hace fallar el paso 2: se lee como vacía (la fila queda vacía en el libro) y la
    # capa lo dice en el paso 7 (F1-DECLARACION, DATOS INVÁLIDOS)
    decl = F1._declaracion_bien_formada(decl)[0]
    per = (decl.get("perimetro_reinversion") or {}).get("valor") if isinstance(decl.get("perimetro_reinversion"), dict) else None
    out = {f"Historia!C{F_SEL}": per if per in PERIMETROS_LIBRO else None}
    reg = (decl.get("perimetro_reinversion") or {}).get("registro") if isinstance(decl.get("perimetro_reinversion"), dict) else None
    out[f"Historia!M{F_SEL}"] = (f"motor_a_f1.json · perimetro_reinversion = {per} · registro {json.dumps(reg, ensure_ascii=False)[:200]}"
                                 if per in PERIMETROS_LIBRO else None)
    validos = {y for y in anios if isinstance(y, int)}
    us = (decl.get("norma_contable") or {}).get("valor") == "US_GAAP" if isinstance(decl.get("norma_contable"), dict) else False
    for nombre, fila in (("da_rou", F_ROU), ("da_ppa", F_PPA)):
        serie, _ = F1.leer_serie(decl, nombre, validos)
        nombres = (nombre,)
        if us and nombre == "da_rou":
            # (F1 · US GAAP) la fila 86 lleva la amortización de derechos de uso DENTRO de la fila 8: la de los arrendamientos financieros (da_rou)
            # más la de los operativos que esté declarada dentro de la fila 8 (da_rou_operativo), con la misma lectura que la capa (rou_fila8)
            serie, nombres = F1.rou_fila8(decl, validos), ("da_rou", "da_rou_operativo")
        for c, y in zip(COLS, anios):
            out[f"Historia!{c}{fila}"] = float(serie[y]) if y in serie else None
        docs = sorted({str(e.get("documento")) for n_ in nombres for e in ((decl.get("series") or {}).get(n_) or {}).values() if isinstance(e, dict) and e.get("documento")})
        out[f"Historia!M{fila}"] = (f"motor_a_f1.json · series.{' + series.'.join(nombres)} (documento y página por año en la declaración): " + "; ".join(docs))[:900] if serie else None
    if circulante:
        C = F1.leer_circulante(decl, validos)
        ap = bool(C and C["aplicable"])
        out[f"Historia!C{F_CREG}"] = REGLA_CIRC if ap else None
        for c, y in zip(COLS, anios):
            out[f"Historia!{c}{F_CANI}"] = 1 if (ap and y in C["anios"]) else None
        reg = C.get("registro") if C else None
        out[f"Historia!M{F_CREG}"] = (f"motor_a_f1.json · {F1.CIRCULANTE} · regla {REGLA_CIRC} · registro {json.dumps(reg, ensure_ascii=False)[:300]}"[:900]
                                      if ap else None)
        out[f"Historia!M{F_CANI}"] = (f"motor_a_f1.json · {F1.CIRCULANTE}.anios = {C['anios']} · fundamento: {str(C.get('fundamento') or '')[:400]}"[:900]
                                      if ap else None)
    return out


def es_v632(lb):
    """(V-CIRC) El libro (LibroV63) tiene la sección de la normalización del circulante de la V6.3.2 F1."""
    return MARCA_CIRC in str(lb.leer("Historia", f"A{F_CTIT}") or "") and lb.tiene_formula("Historia", f"C{F_CEF}")


def aplicar(libro, salida, declaracion):
    from v63_xml import LibroV63
    lb = LibroV63(libro)
    if not lb.tiene_formula("Historia", f"C{F_EF}") or MARCA not in str(lb.leer("Historia", "A84") or ""):
        raise SystemExit(f"{libro} no es un libro V6.3.1 F1 (Historia A84/C{F_EF}): el perímetro F1 no se puede aplicar")
    anios = []
    for c in COLS:
        v = lb.leer("Historia", f"{c}5")
        anios.append(int(v) if isinstance(v, (int, float)) and int(v) == v else None)
    decl = {}
    if declaracion and os.path.isdir(declaracion):
        declaracion = os.path.join(declaracion, "motor_a_f1.json")
    if declaracion and os.path.exists(declaracion):
        decl = json.load(open(declaracion, encoding="utf-8"))
    cel = celdas(decl, anios, circulante=es_v632(lb))
    permitidas = {"Historia": {k.split("!")[1] for k in cel}}
    lb.escribir_celdas({k: ({"valor": v, "tipo": "texto"} if isinstance(v, str) else v) for k, v in cel.items()}, permitidas)
    lb.borrar_caches()
    lb.guardar(salida)
    return cel


# ------------------------------------------------------------------------------------------------------------ oráculo
def perimetro_del_libro(L):
    """Perímetro efectivo de un libro V6.3.1 F1 recalculado (Historia C89); None si el libro no es V6.3.1 F1."""
    if MARCA not in str(L.get("Historia!A84") or ""):
        return None
    return L.get(f"Historia!C{F_EF}") or ""


def replica_dx(L, anios, col):
    """Réplica de D_X (fila 88) con las filas 8, 86 y 87 del propio libro y su perímetro efectivo: lista de diferencias."""
    p = perimetro_del_libro(L)
    if p is None:
        return []
    dif = []
    for y in anios:
        c = col[y]
        da, rou, ppa, dx = (_Q(L.get(f"Historia!{c}{f}")) for f in (8, F_ROU, F_PPA, F_DX))
        if p == "A0_total":
            esp = da
        elif p == "A1_sin_ROU":
            esp = da - rou if da is not None and rou is not None else None
        elif p == "A2_propio":
            esp = da - rou - ppa if None not in (da, rou, ppa) else None
        else:
            esp = None
        if (esp is None) != (dx is None) or (esp is not None and abs(esp - dx) > TOL):
            dif.append(f"Historia {c}{F_DX} (D_X {y}) {None if dx is None else float(dx)} ≠ réplica {None if esp is None else float(esp)}")
    return dif


def corresponde(L, per, rou, ppa, anios, col, dx_capa, calc, dif_motor, circ=None, circ_efecto=False):
    """Motivos por los que el libro V6.3.1 F1 NO calcula el perímetro declarado (lista vacía = corresponde). dx_capa(y): D_X de la capa
    con el perímetro declarado; calc: cálculo de la capa con el perímetro declarado (f, ancla) o None; dif_motor: celdas del Motor distintas.
    (V-CIRC) circ: años de la normalización declarada y aplicable del circulante (None sin ella); circ_efecto: cambia algún circulante que usa la
    reinversión. Un libro V6.3.2 F1 tiene que tener la misma normalización efectiva y los mismos años; uno V6.3.1 F1 no la calcula."""
    p = perimetro_del_libro(L)
    if p is None:
        return ["el libro no es V6.3.1 F1"]
    m = []
    nl = normalizacion_del_libro(L, anios, col)
    if nl is None:
        if circ is not None and circ_efecto:
            m.append("el libro V6.3.1 F1 no normaliza el circulante (no tiene la sección de la V6.3.2 F1, Historia C93:L97): con la normalización declarada "
                     "(V-CIRC) su reinversión sigue llevando la fila 14; hace falta la plantilla V6.3.2 F1, en un expediente nuevo")
    elif nl["efectiva"] not in ("ninguna",) + EFECTIVAS_ACTIVAS:
        m.append(f"normalización del circulante del libro (Historia C{F_CEF}) sin valor calculado ({nl['efectiva']!r}): libro sin recalcular")
    elif circ is None and nl["efectiva"] != "ninguna":
        m.append(f"normalización del circulante del libro (Historia C{F_CEF}) «{nl['efectiva']}» y la declaración no tiene una normalización aplicable")
    elif circ is not None and nl["efectiva"] != REGLA_CIRC:
        m.append(f"normalización del circulante del libro (Historia C{F_CEF}) «{nl['efectiva']}» ≠ declarada «{REGLA_CIRC}»")
    elif circ is not None and nl["anios"] != sorted(circ):
        m.append(f"años normalizados del libro (Historia C{F_CANI}:L{F_CANI}) {nl['anios']} ≠ declarados {sorted(circ)}")
    if per not in PERIMETROS_LIBRO:
        m.append(f"el perímetro declarado {per!r} no está en el libro V6.3.1 (solo {', '.join(PERIMETROS_LIBRO)})")
    if p != per:
        m.append(f"perímetro efectivo del libro (Historia C{F_EF}) {p!r} ≠ declarado {per!r}")
    for nombre, fila, serie in (("D&A de derechos de uso", F_ROU, rou), ("PPA", F_PPA, ppa)):
        for y in anios:
            v = _Q(L.get(f"Historia!{col[y]}{fila}"))
            d = serie.get(y)
            if (v is None) != (d is None) or (v is not None and abs(v - d) > TOL):
                m.append(f"{nombre} {y}: libro (Historia {col[y]}{fila}) {None if v is None else float(v)} ≠ declaración {None if d is None else float(d)}")
    for y in anios:
        v, d = _Q(L.get(f"Historia!{col[y]}{F_DX}")), dx_capa(y)
        if (v is None) != (d is None) or (v is not None and abs(v - d) > TOL):
            m.append(f"D_X {y}: libro {None if v is None else float(v)} ≠ capa {None if d is None else float(d)}")
    c58, c53 = _Q(L.get("Historia!C58")), _Q(L.get("Historia!C53"))
    f, an = (calc or {}).get("f"), (calc or {}).get("ancla")
    if (c58 is None) != (f is None) or (f is not None and abs(c58 - f) > TOL_F):
        m.append(f"f: libro (Historia C58) {None if c58 is None else float(c58)} ≠ capa {None if f is None else float(f)}")
    # (revisión V6.3.1, V631-4) con A0 la rama de la V6.3 calcula C53 con tres años o más; la capa solo con los cinco completos: con A0 se
    # contrasta C53 solo si la capa lo calcula (como F1-REPLICA). Con A1/A2, el libro y la capa exigen lo mismo y se contrasta en los dos sentidos
    if per == "A0_total" and an is None:
        pass
    elif (c53 is None) != (an is None) or (an is not None and abs(c53 - an) > TOL):
        m.append(f"ancla de S2C: libro (Historia C53) {None if c53 is None else float(c53)} ≠ capa {None if an is None else float(an)}")
    if dif_motor:
        m.append(f"flujos del Motor distintos de los de la capa en {len(dif_motor)} celdas ({', '.join(dif_motor[:4])})")
    return m


def _num(v):
    """Número de una celda (int o float; no texto ni booleano), como Fraction; None si no es un número."""
    if isinstance(v, bool) or not isinstance(v, (int, float)):
        return None
    return _Q(v)


def normalizacion_del_libro(L, anios=None, col=None):
    """(V-CIRC) None si el libro no es V6.3.2 F1 (sin la sección «NORMALIZACIÓN DEL CIRCULANTE», Historia A92); si lo es: {efectiva (C97: «ninguna»,
    «circulante_a_cero» o «no reconocida»; None sin recalcular), regla (C93) y, con los años: anios (los marcados con 1 en C94:L94), marcas (lo escrito
    en C94:L94), excluido (fila 95) y circulante (fila 96) por año}."""
    if MARCA_CIRC not in str(L.get(f"Historia!A{F_CTIT}") or ""):
        return None
    out = {"efectiva": L.get(f"Historia!C{F_CEF}"), "regla": L.get(f"Historia!C{F_CREG}"), "anios": [], "marcas": {}, "excluido": {}, "circulante": {}}
    for y in anios or []:
        c = col[y]
        v = L.get(f"Historia!{c}{F_CANI}")
        out["marcas"][y] = v
        if _num(v) == 1:
            out["anios"].append(y)
        out["excluido"][y] = _Q(L.get(f"Historia!{c}{F_CEXC}"))
        out["circulante"][y] = _Q(L.get(f"Historia!{c}{F_CUSA}"))
    out["anios"].sort()
    return out


def replica_circulante(L, anios, col):
    """(V-CIRC) Réplica de las filas 95–97 de un libro V6.3.2 F1 con sus entradas (fila 14, C93 y C94:L94): lista de diferencias ([] si el libro no es
    V6.3.2 F1). Efectiva: «ninguna» con C93 y C94:L94 vacíos; «circulante_a_cero» con esa regla y solo 1 o vacío en C94:L94; si no, «no reconocida».
    Fila 95 = fila 14 en los años marcados con la regla efectiva (0 en los demás); fila 96 = fila 14 − fila 95 (vacía con la fila 14 vacía)."""
    nl = normalizacion_del_libro(L, anios, col)
    if nl is None:
        return []
    marcas = [v for v in nl["marcas"].values() if v not in (None, "")]
    if nl["regla"] in (None, "") and not marcas:
        esp = "ninguna"
    elif nl["regla"] == REGLA_CIRC and all(_num(v) == 1 for v in marcas):
        esp = REGLA_CIRC
    else:
        esp = "no reconocida"
    dif = [] if nl["efectiva"] == esp else [f"Historia C{F_CEF} (normalización efectiva) {nl['efectiva']!r} ≠ réplica {esp!r}"]
    for y in anios:
        c = col[y]
        w = _num(L.get(f"Historia!{c}14"))
        e95 = (w or Fr(0)) if (esp == REGLA_CIRC and y in nl["anios"]) else Fr(0)
        e96 = None if w is None else w - e95
        v95, v96 = nl["excluido"].get(y), nl["circulante"].get(y)
        if v95 is None or abs(v95 - e95) > TOL:
            dif.append(f"Historia {c}{F_CEXC} (circulante excluido {y}) {None if v95 is None else float(v95)} ≠ réplica {float(e95)}")
        if (e96 is None) != (v96 is None) or (e96 is not None and abs(v96 - e96) > TOL):
            dif.append(f"Historia {c}{F_CUSA} (circulante de la reinversión {y}) {None if v96 is None else float(v96)} ≠ réplica {None if e96 is None else float(e96)}")
    return dif


if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "aplicar":
        print(__doc__)
        sys.exit(2)
    if os.path.abspath(sys.argv[2]) == os.path.abspath(sys.argv[3]):
        print("ERROR: la salida no puede ser la entrada (se escribe en una copia)")
        sys.exit(2)
    cel = aplicar(sys.argv[2], sys.argv[3], sys.argv[4])
    # (V-CIRC) con un libro V6.3.2 F1, la línea dice además la normalización del circulante escrita (C93 y los años de C94:L94)
    circ = (f" · normalización del circulante (V6.3.2 F1): C{F_CREG} = {cel[f'Historia!C{F_CREG}']!r}, marcadas las columnas "
            f"{''.join(c for c in COLS if cel.get(f'Historia!{c}{F_CANI}') == 1) or 'ninguna'} de la fila {F_CANI}") if f"Historia!C{F_CREG}" in cel else ""
    print(f"OK: perímetro F1 aplicado al libro V6.3.1 (Historia C{F_SEL} = {cel[f'Historia!C{F_SEL}']!r}; "
          f"{sum(1 for k, v in cel.items() if v is not None and k[9] != 'M' and k != f'Historia!C{F_SEL}')} importes){circ} → {sys.argv[3]}")
