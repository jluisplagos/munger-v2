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


def _Q(x):
    import motor_a_f1 as F1
    return F1.Q(x)


# ------------------------------------------------------------------------------------------------------------ aplicar
def celdas(decl, anios):
    """{"Historia!REF": valor} de las filas 85–87 desde la declaración (dict) y los años de la Historia (C5:L5 del libro)."""
    import motor_a_f1 as F1
    decl = decl if isinstance(decl, dict) else {}
    per = (decl.get("perimetro_reinversion") or {}).get("valor") if isinstance(decl.get("perimetro_reinversion"), dict) else None
    out = {f"Historia!C{F_SEL}": per if per in PERIMETROS_LIBRO else None}
    reg = (decl.get("perimetro_reinversion") or {}).get("registro") if isinstance(decl.get("perimetro_reinversion"), dict) else None
    out[f"Historia!M{F_SEL}"] = (f"motor_a_f1.json · perimetro_reinversion = {per} · registro {json.dumps(reg, ensure_ascii=False)[:200]}"
                                 if per in PERIMETROS_LIBRO else None)
    validos = {y for y in anios if isinstance(y, int)}
    for nombre, fila in (("da_rou", F_ROU), ("da_ppa", F_PPA)):
        serie, _ = F1.leer_serie(decl, nombre, validos)
        for c, y in zip(COLS, anios):
            out[f"Historia!{c}{fila}"] = float(serie[y]) if y in serie else None
        docs = sorted({str(e.get("documento")) for e in ((decl.get("series") or {}).get(nombre) or {}).values() if isinstance(e, dict) and e.get("documento")})
        out[f"Historia!M{fila}"] = (f"motor_a_f1.json · series.{nombre} (documento y página por año en la declaración): " + "; ".join(docs))[:900] if serie else None
    return out


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
    cel = celdas(decl, anios)
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


def corresponde(L, per, rou, ppa, anios, col, dx_capa, calc, dif_motor):
    """Motivos por los que el libro V6.3.1 F1 NO calcula el perímetro declarado (lista vacía = corresponde). dx_capa(y): D_X de la capa
    con el perímetro declarado; calc: cálculo de la capa con el perímetro declarado (f, ancla) o None; dif_motor: celdas del Motor distintas."""
    p = perimetro_del_libro(L)
    if p is None:
        return ["el libro no es V6.3.1 F1"]
    m = []
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


if __name__ == "__main__":
    if len(sys.argv) != 5 or sys.argv[1] != "aplicar":
        print(__doc__)
        sys.exit(2)
    if os.path.abspath(sys.argv[2]) == os.path.abspath(sys.argv[3]):
        print("ERROR: la salida no puede ser la entrada (se escribe en una copia)")
        sys.exit(2)
    cel = aplicar(sys.argv[2], sys.argv[3], sys.argv[4])
    print(f"OK: perímetro F1 aplicado al libro V6.3.1 (Historia C{F_SEL} = {cel[f'Historia!C{F_SEL}']!r}; "
          f"{sum(1 for k, v in cel.items() if v is not None and k[9] != 'M' and k != f'Historia!C{F_SEL}')} importes) → {sys.argv[3]}")
