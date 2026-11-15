# -*- coding: utf-8 -*-
"""Réplica independiente de la escalera de precio (encargo 4.14).

Lee SOLO celdas de entrada (constantes) del libro abierto con data_only=False;
si una celda pedida es una fórmula, se niega (para no arrastrar cálculos del libro).
Las únicas lecturas de caché permitidas son las del estado técnico del Motor
(B252/B253/B254/B255), que esta réplica no reimplementa (49 reglas) y declara.
Nada se guarda en el libro.
"""
import math
import openpyxl
from openpyxl.utils import column_index_from_string, get_column_letter

ESTADO_CACHE = {('Motor', 'B252'), ('Motor', 'B253'), ('Motor', 'B254'), ('Motor', 'B255')}


class EsFormula(Exception):
    pass


def isnum(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def N(x):
    return x if isnum(x) else 0.0


def blank(x):
    return x is None or (isinstance(x, str) and len(x.strip()) == 0)


class Libro:
    def __init__(self, ruta, overrides=None):
        self.ruta = ruta
        self.wf = openpyxl.load_workbook(ruta, data_only=False)
        self.wv = openpyxl.load_workbook(ruta, data_only=True)
        self.ov = dict(overrides or {})
        self.lecturas = set()

    def has(self, sh):
        return sh in self.wf.sheetnames

    def inp(self, sh, ref):
        if (sh, ref) in self.ov:
            return self.ov[(sh, ref)]
        v = self.wf[sh][ref].value
        if isinstance(v, str) and v.startswith('='):
            raise EsFormula(f'{sh}!{ref} es fórmula: {v[:80]}')
        self.lecturas.add((sh, ref))
        return v

    def es_formula(self, sh, ref):
        v = self.wf[sh][ref].value
        return isinstance(v, str) and v.startswith('=')

    def formula(self, sh, ref):
        return self.wf[sh][ref].value

    def cache(self, sh, ref):
        assert (sh, ref) in ESTADO_CACHE, (sh, ref)
        return self.wv[sh][ref].value

    def cached_any(self, sh, ref):  # solo para comparar, nunca para calcular
        return self.wv[sh][ref].value


COLS = [get_column_letter(c) for c in range(3, 13)]  # C..L  (años 1..10 de Historia)


# ------------------------------------------------------------------ Historia
def historia(b):
    H = lambda r, c: b.inp('Historia', f'{c}{r}')
    row = {r: [H(r, c) for c in COLS] for r in range(5, 27)}
    o = {}
    o['C43'] = sum(1 for x in row[6] if isnum(x))
    L6 = row[6][-1]
    o['C44'] = L6 if isnum(L6) else ''
    # fila 29 margen EBIT
    r29 = []
    for i in range(10):
        s, e = row[6][i], row[7][i]
        r29.append(e / s if (isnum(e) and isnum(s) and N(s) != 0) else '')
    o['r29'] = r29
    o['C48'] = r29[-1] if isnum(r29[-1]) else ''
    nums29 = [x for x in r29 if isnum(x)]
    o['C49'] = (sum(nums29) / len(nums29)) if (len(nums29) > 0 and len(nums29) == o['C43']) else ''
    # C52 tipo medio H10:L10
    t5 = row[10][5:10]
    nt = [x for x in t5 if isnum(x)]
    o['C52'] = (sum(nt) / len(nt)) if (o['C43'] > 0 and len(nt) == min(5, o['C43'])) else ''
    # filas 30/31
    r30, r31 = [], []
    for i in range(10):
        cap, da = row[12][i], row[8][i]
        v30 = (cap - da + N(row[14][i])) if (isnum(cap) and isnum(da)) else ''
        r30.append(v30)
        r31.append(v30 + N(row[13][i]) if isnum(v30) else '')
    o['r31'] = r31
    # C63 coste de la deuda
    K22, K23, L22, L23 = row[22][8], row[23][8], row[22][9], row[23][9]
    L15 = row[15][9]
    if isnum(L15) and isnum(K22) and isnum(L22) and (isnum(K23) == isnum(L23)) and (N(K22) + N(K23) + N(L22) + N(L23)) > 0:
        o['C63'] = L15 / ((N(K22) + N(K23) + N(L22) + N(L23)) / 2)
    else:
        o['C63'] = ''
    o['C64'] = (L22 + L23) if (isnum(L22) and isnum(L23)) else ''
    L25, L26 = row[25][9], row[26][9]
    o['C65'] = (max(0, L25) + L26) if (isnum(L25) and isnum(L26)) else ''
    L24 = row[24][9]
    o['C66'] = L24 if isnum(L24) else ''
    o['row'] = row
    o['C57'] = b.inp('Historia', 'C57')
    return o


def analisis_C52(b):
    A = lambda r: b.inp('Análisis', r)
    c46, c47, c48, c49, c50, c51 = (A(x) for x in ('C46', 'C47', 'C48', 'C49', 'C50', 'C51'))
    if not all(isnum(x) for x in (c46, c47, c48, c49, c50)) or c51 not in ('Sí', 'No') or N(c47) < 0:
        return ''
    return c46 - c47 - c48 - c49 - (0 if c51 == 'No' else c50)


def historia_C70(b, c52):
    if not isnum(c52):
        return ''
    nat = b.inp('Palancas', 'C43'); c44 = b.inp('Palancas', 'C44')
    if c52 <= 0 and nat in ('Transitorio', 'Extraordinario') and isnum(c44) and N(c44) > 0:
        return c44
    return c52


def historia_C58(b, h, c70):
    row = h['row']; k = h['C57']; c43 = h['C43']
    if not isnum(c70) or not isnum(k) or k < 1 or c43 < k:
        return ''
    for r in range(6, 15):  # SUMPRODUCT(--(C6:L14<>""),--NOT(ISNUMBER(C6:L14)))>0
        for x in row[r]:
            if x is not None and x != '' and not isnum(x):
                return ''
    k = int(k)
    win = list(range(10 - k, 10))  # índices de las k últimas columnas
    for r in (6, 7, 8, 10, 12, 14):
        if any(row[r][i] is None or row[r][i] == '' for i in win):
            return ''
    ssum = sum(N(row[6][i]) for i in win)
    if ssum <= 0:
        return ''
    nopat = sum(N(row[7][i]) * (1 - N(row[10][i])) for i in win)
    reinv = sum(N(row[12][i]) - N(row[8][i]) + N(row[14][i]) for i in win)
    return ((nopat - reinv) / k - c70) / (ssum / k)


# ------------------------------------------------------------------ Configuración V6.4
OPC36 = ["Sin requisito adicional", "H · hueco (crédito de la inversión para crecer)", "S · suma sin reestimar",
         "SR1 · suma con S2C reestimado", "SR2 · suma con S2C y ROIC reestimados",
         "SRF · suma con inversión fija reestimada"]
NIIF = "NIIF 16 · capex de caja + altas de derechos de uso frente a toda la D&A"
CAJA = "Caja · capex de caja frente a toda la D&A (V6.4)"


def configuracion(b, h, motor):
    """Devuelve el diccionario de parámetros efectivos (filas 76–93) o, sin hoja, el modo heredado."""
    cf = {'B76': False, 'B77': False, 'B78': False, 'B79': False, 'B80': False, 'B81': False, 'B82': False,
          'B83': 0.0, 'B84': 1.0, 'B85': 1.0, 'B86': 1.0, 'B87': 0.0, 'B88': 0.0, 'B89': 0.0, 'B90': True,
          'B54': None, 'B67': False, 'row93': [0.0] * 10, 'hoja': False, 'B18': h['C52'], 'B19': h['C52'],
          'B21': None}
    sh = 'Configuración V6.4'
    if not b.has(sh):
        return cf
    cf['hoja'] = True
    C = lambda r: b.inp(sh, r)
    B4 = C('B4')
    if blank(B4) or B4 == 'Heredado':
        B5 = 'Heredado'
    elif B4 == 'Experimental':
        B5 = 'Experimental'
    else:
        B5 = 'ERROR'
    B6 = motor
    B11, B12, B13, B14, B15, B16 = (C(f'B{r}') for r in range(11, 17))
    B21, B22, B23 = C('B21'), C('B22'), C('B23')
    B28, B29, B30, B31 = C('B28'), C('B29'), C('B30'), C('B31')
    B36, B37, B38, B39, B40, B41, B42, B43 = (C(f'B{r}') for r in range(36, 44))
    B44, B45 = C('B44'), C('B45')
    B46_50 = [C(f'B{r}') for r in range(46, 51)]
    tiene_s11 = b.es_formula(sh, 'B153')  # V6.4.1: perímetro de la inversión
    if tiene_s11:
        B146 = C('B146'); B147_151 = [C(f'B{r}') for r in range(147, 152)]; B152 = C('B152')
        B153 = sum(B147_151) if (B5 == 'Experimental' and B146 == NIIF and sum(isnum(x) for x in B147_151) == 5) else 0
    else:
        B146 = None; B147_151 = []; B152 = None; B153 = 0
    C44 = h['C44']
    B33 = ((B29 + B30 - B31) / C44 if C44 > 0 else '') if all(isnum(x) for x in (B29, B30, B31, C44)) else ''
    row = h['row']
    B54 = row[8][9]
    B55 = sum(N(x) for x in h['r31'][5:10]) + B153
    B66 = (B43 == "P0 · no se repone (explícito)")
    B56 = sum(N(x) for x in B46_50) if B66 else 0
    B57 = B55 + B56
    B58 = sum(N(x) for x in row[12][5:10]) - sum(N(x) for x in row[8][5:10]) + B153
    B59 = sum(N(x) for x in row[13][5:10])
    B60 = B58 + B56
    B61 = B60 / 5
    B62 = B60 + B59
    B63 = sum(N(x) for x in row[8][5:10]) - B56
    B67 = isinstance(B36, str) and B36 != "Sin requisito adicional"
    B68 = (B37 == "Λ · (λ − 1) × amortización que se repone")
    if B67:
        try:
            B69 = B36[:B36.index(' ')]
        except ValueError:
            B69 = '?'
    else:
        B69 = '—'
    B70 = ((B38 - 1) * B54 if isnum(B38) else 0) if (B67 and B68) else ((B39 * B61 if isnum(B39) else 0) if B67 else 0)
    B71 = ((B38 - 1) * B63 if isnum(B38) else 0) if (B67 and B68) else ((B39 * B60 if isnum(B39) else 0) if B67 else 0)
    if B67 and B69 in ('SR1', 'SR2') and isnum(B57):
        B72 = (B57 / (B57 - B71)) if (B57 > 0 and B57 - B71 > 0) else ''
    else:
        B72 = 1
    if B67 and B69 == 'SRF' and isnum(B62):
        B73 = (1 - B71 / B62) if B62 > 0 else ''
    else:
        B73 = 1
    E = (B5 == 'Experimental')
    chk = []
    chk.append(B5 == 'ERROR')
    chk.append(E and B6 != 'B')
    chk.append(E and not (blank(B11) or (isnum(B11) and 0 <= B11 < 1)))
    chk.append(E and isnum(B11) and (blank(B12) or blank(B13) or blank(B14) or B15 not in ("dato publicado", "derivado de datos publicados", "convención", "hipótesis")))
    chk.append(E and isnum(B11) and B16 not in ("Vinculado al tipo aplicado a NOPAT", "Tipo de la Historia (separado)"))
    chk.append(E and not (blank(B21) or (isnum(B21) and -1 < B21 < 1)))
    chk.append(E and isnum(B21) and (blank(B22) or blank(B23)))
    chk.append(E and B28 not in ("R0 · simétrica (heredada)", "R1 · solo circulante; capacidad conservada"))
    chk.append(E and B28 == "R1 · solo circulante; capacidad conservada" and not isnum(B33))
    chk.append(E and isnum(B33) and (B29 < 0 or B30 < 0 or B31 < 0))
    chk.append(E and B36 not in OPC36)
    chk.append(E and B43 not in ("Legado · se repone con la amortización", "P0 · no se repone (explícito)"))
    chk.append(E and (B67 or B66) and B28 != "R1 · solo circulante; capacidad conservada")
    chk.append(E and B67 and B37 not in ("Λ · (λ − 1) × amortización que se repone", "Θ · θ × exceso histórico medio"))
    chk.append(E and B67 and B68 and not (isnum(B38) and B38 >= 1))
    chk.append(E and B67 and B37 == "Θ · θ × exceso histórico medio" and not (isnum(B39) and 0 <= B39 <= 1))
    chk.append(E and B67 and B40 not in ("Plana", "Proporcional a las ventas"))
    chk.append(E and B67 and B41 not in ("Proporcional a las ventas", "Crece con g"))
    chk.append(E and B67 and not ((B69 == 'SR2' and B42 == "ROIC × f (SR2)") or (B69 != 'SR2' and B42 == "ROIC de la fase B sin cambio")))
    chk.append(E and B66 and not (isnum(B44) and isnum(B45) and sum(isnum(x) for x in B46_50) == 5))
    chk.append(E and B66 and sum(isnum(x) for x in [B44, B45] + B46_50) == 7 and (B44 < 0 or B45 < 0 or min(B46_50) < 0))
    chk.append(E and B66 and isnum(B44) and isnum(B45) and B45 > 10 * B44)
    cnt = lambda lst: sum(isnum(x) for x in lst)
    chk.append(E and (B67 or B66) and (cnt(h['r31'][5:10]) < 5 or cnt(row[12][5:10]) < 5 or cnt(row[8][5:10]) < 5))
    chk.append(E and B67 and B69 in ('SR1', 'SR2') and not isnum(B72))
    chk.append(E and B67 and B69 == 'SRF' and not (isnum(B73) and B73 >= 0))
    chk.append(E and B67 and B70 < 0)
    chk.append(E and B67 and B68 and B66 and isnum(B44) and B44 > B54)
    chk.append(E and not isnum(row[8][9]))
    if tiene_s11:
        chk.append(E and ((not blank(B146) and B146 not in (CAJA, NIIF)) or
                          (B146 == NIIF and (cnt(B147_151) < 5 or min([x for x in B147_151 if isnum(x)] or [-1]) < 0 or blank(B152)))))
    B90 = not any(chk)
    B76 = (B5 == 'Experimental') and B90
    B77 = B76 and B28 == "R1 · solo circulante; capacidad conservada"
    B78 = B76 and (B67 or B66)
    B79 = B78 and B69 == 'H'
    B80 = B78 and B67 and B68
    B81 = B78 and B67 and B40 == "Proporcional a las ventas"
    B82 = B78 and B67 and B41 == "Proporcional a las ventas"
    B83 = B33 if (B76 and isnum(B33)) else 0
    B84 = B72 if (B78 and B69 in ('SR1', 'SR2')) else 1
    B85 = B72 if (B78 and B69 == 'SR2') else 1
    B86 = B73 if (B78 and B69 == 'SRF') else 1
    B87 = (B38 - 1) if B80 else 0
    B88 = (B39 * B61) if (B78 and B67 and not B68) else 0
    B89 = B70 if (B78 and B67) else 0
    row93 = [(min(B44, max(0, B45 - B44 * i)) if (B78 and B66) else 0) for i in range(10)]
    B18 = B11 if (B76 and isnum(B11)) else h['C52']
    B19 = h['C52'] if (B76 and isnum(B11) and B16 == "Tipo de la Historia (separado)") else B18
    cf.update(dict(B5=B5, B18=B18, B19=B19, B21=B21, B33=B33, B54=B54, B55=B55, B57=B57, B60=B60, B61=B61,
                   B66=B66, B67=B67, B69=B69, B70=B70, B71=B71, B72=B72, B76=B76, B77=B77, B78=B78, B79=B79,
                   B80=B80, B81=B81, B82=B82, B83=B83, B84=B84, B85=B85, B86=B86, B87=B87, B88=B88, B89=B89,
                   B90=B90, B153=B153, row93=row93, checks=chk, s11=tiene_s11))
    return cf


# ------------------------------------------------------------------ Diagnóstico V6 (base del motor)
def diagnostico(b, h, cf, motor):
    A = lambda r: b.inp('Análisis', r)
    d = {'C5': motor}
    d['C9'] = h['C44']
    C8 = b.inp('Palancas', 'C8')
    heredado_m0 = h['C49'] if C8 == "Media del ciclo" else h['C48']
    d['C10'] = cf['B21'] if (cf['B76'] and isnum(cf['B21'])) else heredado_m0
    d['C11'] = cf['B18'] if cf['B76'] else h['C52']
    d['C12'] = h['C58']
    C56, C41 = A('C56'), A('C41')
    if motor != 'B':
        d['C15'] = '—'
    elif not isnum(h['C64']):
        d['C15'] = ''
    elif isnum(C56) and h['C64'] == 0:
        d['C15'] = C56
    else:
        moneda_ok = b.inp('Palancas', 'C48') == b.inp('Control maestro', 'H4')
        if isnum(C56) and isnum(C41) and N(C41) > 0 and isnum(h['C63']) and moneda_ok:
            tesc = cf['B19'] if cf['B76'] else d['C11']
            d['C15'] = (C56 * C41 + h['C63'] * (1 - N(tesc)) * h['C64']) / (C41 + h['C64'])
        else:
            d['C15'] = ''
    if motor != 'B':
        d['C16'] = '—'
    elif isnum(h['C64']) and isnum(h['C65']) and isnum(h['C66']):
        d['C16'] = h['C64'] + h['C65'] - h['C66']
    else:
        d['C16'] = ''
    return d


# ------------------------------------------------------------------ Motor (una fila)
def fila_motor(b, d, cf, E, F, G, H, I):
    motor = d['C5']
    if motor == 'C':
        raise NotImplementedError('motor C no reimplementado (no hace falta en estos expedientes)')
    A = lambda r: b.inp('Análisis', r)
    C0 = d['C9']; m0 = d['C10']
    J = d['C15'] if motor == 'B' else A('C56')
    K = N(d['C11'])
    Lf = d['C12'] if motor == 'A' else 0
    M = -N(d['C16']) if motor == 'B' else (N(A('C76')) if motor == 'A' else 0)
    Nq = N(b.inp('Palancas', 'C22')); Oq = N(b.inp('Palancas', 'C23'))
    P = A('C55')
    BS = (motor in ('A', 'B', 'C') and all(isnum(x) for x in (C0, m0, E, F, H, I, J, K, Lf)) and J > H and I > 0
          and I > H and N(C0) > 0 and (motor == 'C' or (isnum(G) and N(G) > 0)) and (cf['B90'] if cf['hoja'] else True))
    if not BS:
        return {'BS': False}
    g = [E if t <= 5 else E - (E - H) * (t - 5) / 5 for t in range(1, 11)]
    Lt = []; prev = C0
    for t in range(10):
        prev = prev * (1 + g[t]); Lt.append(prev)
    mt = [m0 + (F - m0) * min(t, 5) / 5 for t in range(1, 11)]
    exp = cf['B76']
    DY = BS and motor == 'B'
    flujo = []
    if exp:
        assert DY
        B83, B84, B86 = cf['B83'], cf['B84'], cf['B86']
        for t in range(10):
            Lprev = C0 if t == 0 else Lt[t - 1]
            BU = (Lt[t] - Lprev) * B83
            if cf['B77']:
                mx = max([C0] + Lt[:t])
                CE = max(0, Lt[t] - mx) * (1 / (G * B84) - B83) * B86
            else:
                CE = (Lt[t] - Lprev) * (1 / G - B83)
            r93 = cf['row93'][t]
            if cf['B78']:
                esc = (Lt[t] / C0) if cf['B81'] else 1
                CO = cf['B87'] * (cf['B54'] * esc - r93) if cf['B80'] else cf['B88'] * esc
            else:
                CO = 0
            CY = min(CO, max(0, CE)) if cf['B79'] else 0
            flujo.append(Lt[t] * mt[t] * (1 - K) + r93 - CE - BU - CO + CY)
        AJ = Lt[9]
        DS = AJ * (1 + H) * F * (1 - K)
        DT = AJ * H * B83
        DU = (DS * H / (I * cf['B85']) - DT) * B86
        if cf['B78'] and cf['B67']:
            DV = (cf['B87'] * cf['B54'] if cf['B80'] else cf['B88']) * (AJ * (1 + H) / C0 if cf['B82'] else 1 + H)
        else:
            DV = 0
        DW = min(DV, max(0, DU)) if cf['B79'] else 0
        BF = DS - DU - DT - DV + DW
    else:
        for t in range(10):
            Lprev = C0 if t == 0 else Lt[t - 1]
            flujo.append(Lt[t] * (mt[t] * (1 - K) - Lf) - (Lt[t] - Lprev) / G)
        AJ = Lt[9]
        BF = AJ * (1 + H) * (F * (1 - K) * (1 - H / I) - Lf)
    BE = sum(flujo[t] / (1 + J) ** (t + 1) for t in range(10))
    BG = BF / (J - H)
    BH = BG / (1 + J) ** 10
    BI = BE + BH + M
    BJ = (1 - Nq) * BI + Nq * Oq
    BK = BJ / P if N(P) > 0 else ''
    return dict(BS=True, J=J, K=K, Lf=Lf, M=M, P=P, flujo=flujo, BE=BE, BF=BF, BG=BG, BH=BH, BI=BI, BJ=BJ, BK=BK,
                BD=flujo[9])


# ------------------------------------------------------------------ valoración completa
def valorar(b):
    A = lambda r: b.inp('Análisis', r)
    C62 = A('C62')
    motor = 'A' if C62 == 'Sí' else ('B' if C62 == 'No · financiación cambia mucho' else
                                    ('C' if C62 in ('No · banco o aseguradora', 'No · banco, aseguradora o regulada') else '—'))
    h = historia(b)
    c52 = analisis_C52(b)
    c70 = historia_C70(b, c52)
    h['C58'] = historia_C58(b, h, c70)
    h['C70'] = c70; h['C52A'] = c52
    cf = configuracion(b, h, motor)
    d = diagnostico(b, h, cf, motor)
    Pl = lambda r: b.inp('Palancas', r)
    filas = {}
    for nom, col in (('MALO', 'B'), ('NORMAL', 'C'), ('BUENO', 'D')):
        E, F = Pl(f'{col}14'), Pl(f'{col}15')
        G = 1 if motor == 'C' else Pl(f'{col}16')
        H = A(f'{col}68'); I = Pl(f'{col}18')
        filas[nom] = fila_motor(b, d, cf, E, F, G, H, I)
    estado = {k: b.cache('Motor', k) for k in ('B252', 'B253', 'B254', 'B255')}
    V = [filas[n]['BK'] for n in ('MALO', 'NORMAL', 'BUENO')]
    p = [A('B69'), A('C69'), A('D69')]
    if sum(isnum(x) for x in V) < 3 or round(abs(sum(p) - 1), 9) > 0.001:
        pond = ''
    else:
        pond = sum(v * q for v, q in zip(V, p)) / sum(p)
    # tabla del DCF inverso (NORMAL con E variable)
    tabla = []
    for r in range(108, 189):
        gr = A(f'A{r}')
        fr = fila_motor(b, d, cf, gr, Pl('C15'), (1 if motor == 'C' else Pl('C16')), A('C68'), Pl('C18'))
        tabla.append((gr, fr['BK'] if fr['BS'] else ''))
    vals = [v for _, v in tabla]
    if sum(isnum(x) for x in vals) < 81:
        B191 = B192 = ''
    else:
        B191 = sum(1 for i in range(80) if vals[i + 1] > vals[i])
        B192 = max(vals) - min(vals)
    precio = A('C37')
    if B191 == '':
        B193 = '—'
    elif B191 == 0:
        B193 = '⚠ REVISAR · con tus palancas crecer destruye valor: el DCF inverso no aplica'
    elif B191 < 80:
        B193 = '⚠ REVISAR · el valor no crece de forma continua con el crecimiento: el DCF inverso no aplica'
    elif isnum(precio) and N(precio) > 0:
        B193 = '⚠ REVISAR · el valor apenas depende del crecimiento: el DCF inverso no informa' if B192 < 0.05 * N(precio) else '✓ PASA'
    else:
        B193 = '✓ PASA'
    return dict(motor=motor, h=h, cf=cf, d=d, filas=filas, V=V, p=p, pond=pond, precio=precio, tabla=tabla,
                B191=B191, B192=B192, B193=B193, estado=estado, C14=Pl('C14'),
                moneda=(Pl('C48'), b.inp('Control maestro', 'H4')))


# ------------------------------------------------------------------ escalera (Anexo C)
def G_(P, V, p):
    return sum(q * max(v - P, 0) for v, q in zip(V, p))


def L_(P, V, p):
    return sum(q * max(P - v, 0) for v, q in zip(V, p))


def p_estrella_cerrada(V, p, k=3.0):
    s = sorted(zip(V, p))
    for j in (1, 2):
        bajo, alto = s[:j], s[j:]
        num = sum(q * v for v, q in alto) + k * sum(q * v for v, q in bajo)
        den = sum(q for _, q in alto) + k * sum(q for _, q in bajo)
        P = num / den
        if s[j - 1][0] - 1e-12 <= P <= s[j][0] + 1e-12:
            return P
    raise ValueError('sin P*')


def p_estrella_biseccion(V, p, k=3.0):
    lo, hi = min(V), max(V)
    F = lambda P: G_(P, V, p) - k * L_(P, V, p)
    if F(hi) >= 0:
        return hi
    for _ in range(300):
        mid = (lo + hi) / 2
        if F(mid) >= 0:
            lo = mid
        else:
            hi = mid
    return lo


def interp_inversa(tabla, precio):
    """Misma regla que Análisis C86: MATCH(precio, B, 1) e interpolación lineal en pasos de 0,005."""
    A = [a for a, _ in tabla]; B = [v for _, v in tabla]
    if precio < B[0]:
        return '< -10%'
    if precio > B[-1]:
        return '> 30%'
    if precio == B[-1]:
        return 0.3
    i = max(j for j in range(len(B)) if B[j] <= precio)
    return A[i] + 0.005 * (precio - B[i]) / (B[i + 1] - B[i])


def escalera(res, k=3.0):
    V, p, pond, precio = res['V'], res['p'], res['pond'], res['precio']
    est = res['estado']
    out = {'sin_lectura': None}
    if est['B255'] != 'COMPLETO Y VÁLIDO' or est['B252'] or not est['B253'] or any(not isnum(v) for v in V) or abs(sum(p) - 1) > 1e-3:
        out['sin_lectura'] = 'estado técnico / moneda / valores'
        return out
    if not (V[0] <= V[1] <= V[2]):
        out['sin_lectura'] = 'valores desordenados (G19)'
        return out
    Pc = p_estrella_cerrada(V, p, k)
    Pb = p_estrella_biseccion(V, p, k)
    VN = V[1]
    psi = min(Pc, VN)
    malo = V[0] if V[0] > 0 else None
    if malo is not None and precio <= malo:
        zona = 'bajo_malo'
    elif precio <= psi:
        zona = 'cumple_regla_k'
    elif precio <= pond:
        zona = 'vigilar'
    else:
        zona = 'caro'
    tabla = res['tabla']
    C14 = res['C14']
    tabla_ok = False
    if res['B193'] == '✓ PASA' and -0.10 <= C14 <= 0.30:
        A = [a for a, _ in tabla]; B = [v for _, v in tabla]
        i = max(j for j in range(len(A)) if A[j] <= C14 + 1e-15)
        vi = B[i] if i == len(A) - 1 else B[i] + (B[i + 1] - B[i]) * (C14 - A[i]) / (A[i + 1] - A[i])
        tabla_ok = abs(vi - VN) <= 0.01 * VN
    if tabla_ok:
        g_act = interp_inversa(tabla, precio); g_si = interp_inversa(tabla, psi)
    else:
        g_act = g_si = 'no utilizable'
    out.update(dict(P_estrella=Pc, P_estrella_biseccion=Pb, precio_si=psi, tope_normal_aplicado=Pc > VN,
                    precio_escenario_malo=malo, ponderado=pond, zona=zona, G=G_(Pc, V, p), L=L_(Pc, V, p),
                    tabla_ok=tabla_ok, g_impl_actual=g_act, g_impl_si=g_si,
                    distancias={'a_precio_si': (precio - psi) / precio,
                                'a_malo': (precio - malo) / precio if malo else None},
                    F_en_Pstar=G_(Pc, V, p) - k * L_(Pc, V, p)))
    return out
