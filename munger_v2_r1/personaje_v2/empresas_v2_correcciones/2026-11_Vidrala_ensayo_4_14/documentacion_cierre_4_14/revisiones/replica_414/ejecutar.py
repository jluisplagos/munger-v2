# -*- coding: utf-8 -*-
"""Ejecuta la réplica sobre los tres expedientes y los casos del efecto del denominador.
Escribe solo en este directorio (salida_replica.json)."""
import json, os, sys
sys.dont_write_bytecode = True
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from replica import Libro, valorar, escalera, isnum

R = '/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/'
EXP = {
    'Viscofan': R + 'viscofan_decisiones/Viscofan/',
    'Vidrala': R + 'vidrala_decisiones/Vidrala/',
    'Elis': R + 'elis_decisiones/Elis/',
}
TOL = 1e-6


def rel(a, b):
    if not (isnum(a) and isnum(b)):
        return None
    return abs(a - b) / max(abs(b), 1e-300)


def fila(mag, exp, rep):
    if isnum(exp) and isnum(rep):
        d = rep - exp; r = rel(rep, exp)
        return dict(magnitud=mag, expediente=exp, replica=rep, diferencia=d, dif_rel=r, veredicto='PASA' if r <= TOL else 'FALLA')
    ok = (exp == rep)
    return dict(magnitud=mag, expediente=exp, replica=rep, diferencia=None if ok else 'distinto', dif_rel=None,
                veredicto='PASA' if ok else 'FALLA')


def correr(ruta, ov=None):
    b = Libro(ruta, ov)
    res = valorar(b)
    esc = escalera(res)
    return b, res, esc


def intermedios(b, res):
    """Compara pasos intermedios con la caché del libro (solo diagnóstico)."""
    out = []
    cv = b.cached_any
    d = res['d']
    pares = [('Diagnóstico V6!C9 V0', cv('Diagnóstico V6', 'C9'), d['C9']),
             ('Diagnóstico V6!C10 m0', cv('Diagnóstico V6', 'C10'), d['C10']),
             ('Diagnóstico V6!C11 t', cv('Diagnóstico V6', 'C11'), d['C11']),
             ('Diagnóstico V6!C12 f', cv('Diagnóstico V6', 'C12'), d['C12']),
             ('Diagnóstico V6!C15 r_op', cv('Diagnóstico V6', 'C15'), d['C15']),
             ('Diagnóstico V6!C16 pasivos netos', cv('Diagnóstico V6', 'C16'), d['C16'])]
    if res['cf']['hoja']:
        for k in ('B76', 'B77', 'B78', 'B83', 'B84', 'B87', 'B88', 'B89', 'B90'):
            pares.append((f'Configuración V6.4!{k}', cv('Configuración V6.4', k), res['cf'][k]))
    for i, nom in zip((6, 7, 8), ('MALO', 'NORMAL', 'BUENO')):
        f = res['filas'][nom]
        for col, key in (('BE', 'BE'), ('BF', 'BF'), ('BH', 'BH'), ('BI', 'BI'), ('BJ', 'BJ'), ('BK', 'BK'), ('BD', 'BD')):
            pares.append((f'Motor!{col}{i} {nom}', cv('Motor', f'{col}{i}'), f[key]))
    tab_max = 0.0
    for j, (g, v) in enumerate(res['tabla']):
        c = cv('Análisis', f'B{108 + j}')
        if isnum(c) and isnum(v):
            tab_max = max(tab_max, rel(v, c))
    pares.append(('Motor!B191', cv('Motor', 'B191'), res['B191']))
    pares.append(('Motor!B193', cv('Motor', 'B193'), res['B193']))
    for m, e, r in pares:
        if e is None and r == '':
            out.append(dict(magnitud=m + ' (vacío: caché None ≡ réplica "")', expediente=e, replica=r, diferencia=None, dif_rel=None, veredicto='PASA'))
        else:
            out.append(fila(m, e, r))
    out.append(dict(magnitud='Análisis!B108:B188 (máx. dif. rel.)', expediente='81 celdas', replica=tab_max,
                    diferencia=None, dif_rel=tab_max, veredicto='PASA' if tab_max <= TOL else 'FALLA'))
    return out


salida = {}
for emp, carp in EXP.items():
    libro = carp + f'{emp}_v63_evaluada.xlsx'
    b, res, esc = correr(libro)
    rj = json.load(open(carp + 'resultados.json'))
    pj = json.load(open(carp + 'precio.json'))
    tabla = []
    vr = rj['valores']
    tabla.append(fila('V_MALO (B78)', vr['B78'], res['V'][0]))
    tabla.append(fila('V_NORMAL (C78)', vr['C78'], res['V'][1]))
    tabla.append(fila('V_BUENO (D78)', vr['D78'], res['V'][2]))
    tabla.append(fila('ponderado (C83)', vr['C83'], res['pond']))
    tabla.append(fila('V_MALO precio.json', pj['V'][0], res['V'][0]))
    tabla.append(fila('V_NORMAL precio.json', pj['V'][1], res['V'][1]))
    tabla.append(fila('V_BUENO precio.json', pj['V'][2], res['V'][2]))
    tabla.append(fila('ponderado precio.json', pj['ponderado'], res['pond']))
    tabla.append(fila('P* (k = 3)', pj['P_estrella'], esc['P_estrella']))
    tabla.append(fila('P* por bisección (comprobación)', pj['P_estrella'], esc['P_estrella_biseccion']))
    tabla.append(fila('precio de Sí = mín(P*, V_NORMAL)', pj['precio_si'], esc['precio_si']))
    tabla.append(fila('tope NORMAL aplicado', pj['tope_normal_aplicado'], esc['tope_normal_aplicado']))
    tabla.append(fila('precio del escenario MALO', pj['precio_escenario_malo'], esc['precio_escenario_malo']))
    tabla.append(fila('precio actual (C37)', pj['precio'], res['precio']))
    tabla.append(fila('zona', pj['zona'], esc['zona']))
    tabla.append(fila('G(P*)', pj['G'], esc['G']))
    tabla.append(fila('L(P*)', pj['L'], esc['L']))
    tabla.append(fila('tabla del DCF inverso utilizable', pj['tabla_dcf_inverso_ok'], esc['tabla_ok']))
    tabla.append(fila('g implícito al precio actual', pj['g_impl_actual'], esc['g_impl_actual']))
    tabla.append(fila('g implícito al precio de Sí', pj['g_impl_si'], esc['g_impl_si']))
    tabla.append(fila('distancia a precio de Sí', pj['distancias']['a_precio_si'], esc['distancias']['a_precio_si']))
    tabla.append(fila('distancia a MALO', pj['distancias']['a_malo'], esc['distancias']['a_malo']))
    if isnum(vr.get('C86')):
        tabla.append(fila('C86 frente a g implícito réplica', vr['C86'], esc['g_impl_actual']))
    c158 = b.inp('Diagnóstico V6', 'C158')
    c156 = min(res['V'][0], c158 * res['pond'])
    tabla.append(fila('regla antigua C156 = mín(MALO, 0,75 × ponderado) · precio.json', pj['C156_regla_antigua'], c156))
    tabla.append(fila('regla antigua C156 · resultados.json', rj['precio_referencia_hoja_C156'], c156))
    Ps = esc['P_estrella']
    prop = (abs(esc['F_en_Pstar']) < 1e-9 and Ps >= min(res['V']) - 1e-12 and Ps <= res['pond'] + 1e-12)
    tabla.append(dict(magnitud='propiedades: |G − 3L| en P* < 1e-9 · P* ≥ mín V · P* ≤ ponderado', expediente='(Anexo C.2)',
                      replica=f"|F(P*)| = {abs(esc['F_en_Pstar']):.2e}", diferencia=None, dif_rel=None,
                      veredicto='PASA' if prop else 'FALLA'))
    salida[emp] = dict(libro=libro, motor=res['motor'], modo_v64=res['cf'].get('B5'), estado_cache=res['estado'],
                       tabla=tabla, intermedios=intermedios(b, res), F_en_Pstar=esc['F_en_Pstar'],
                       lecturas_de_entrada=len(b.lecturas))

# ------------------------------------------------------------------ efecto aislado del denominador
efecto = {}
RAMA = {'Viscofan': R + 'viscofan/Viscofan/Viscofan_v63_evaluada.xlsx',
        'Elis': R + 'elis_motor_A/Elis/Elis_v63_evaluada.xlsx'}
DEN = {'Viscofan': (45.993399, 45.479209), 'Elis': (232.47681, 259.077654)}
EFJ = {'Viscofan': R + 'resultados/efecto_decisiones_viscofan.json',
       'Elis': R + 'resultados/efecto_decisiones_elis_E6.json'}
# caso del fichero de efecto que equivale a «libro final con el C55 anterior» (resto de entradas del libro final)
EQUIV_FINAL_C55_VIEJO = {'Viscofan': 'solo la capitalización', 'Elis': 'medias exactas'}


def ovr(celdas):
    o = {}
    for k, v in celdas.items():
        sh, ref = k.split('!')
        o[(sh, ref)] = v
    return o


for emp in ('Viscofan', 'Elis'):
    nuevo, viejo = DEN[emp]
    ej = json.load(open(EFJ[emp]))
    casos = list(ej['casos'])
    if 'dilucion_potencial_declarada_aparte' in ej:
        base_celdas = [c for c in casos if 'denominador y capitalización' in c['caso']][0]['celdas']
        for c in ej['dilucion_potencial_declarada_aparte']['casos']:
            cel = dict(base_celdas); cel['Análisis!C55'] = c['acciones_mm']; cel['Análisis!C41'] = c['capitalizacion']
            casos.append(dict(caso='dilución · ' + c['caso'], celdas=cel, precio_si=c['precio_si'], zona=c['zona'], ponderado=c['ponderado']))
    out = {}
    comp = []
    # (a) cada caso del fichero, aplicado al libro anterior/rama con la réplica
    _, rR, eR = correr(RAMA[emp])
    for c in casos:
        _, rc, ec = correr(RAMA[emp], ovr(c['celdas']))
        comp.append(fila(f"[libro anterior + celdas del caso] {c['caso']} · precio de Sí", c['precio_si'], ec['precio_si']))
        comp.append(fila(f"[libro anterior + celdas del caso] {c['caso']} · ponderado", c['ponderado'], rc['pond']))
        comp.append(fila(f"[libro anterior + celdas del caso] {c['caso']} · zona", c['zona'], ec['zona']))
        if 'r_operativa' in c:
            comp.append(fila(f"[libro anterior + celdas del caso] {c['caso']} · r operativa", c['r_operativa'], rc['d']['C15']))
        d_exp = c.get('delta_frente_a_la_rama', c.get('delta_frente_al_anterior'))
        if isnum(d_exp):
            comp.append(fila(f"[libro anterior + celdas del caso] {c['caso']} · Δ precio de Sí", d_exp, ec['precio_si'] - eR['precio_si']))
    # (b) efecto aislado del denominador en el libro FINAL (todo lo demás fijo)
    _, rF, eF = correr(EXP[emp] + f'{emp}_v63_evaluada.xlsx')
    _, rFv, eFv = correr(EXP[emp] + f'{emp}_v63_evaluada.xlsx', {('Análisis', 'C55'): viejo})
    ce = [c for c in casos if EQUIV_FINAL_C55_VIEJO[emp] in c['caso']][0]
    comp.append(fila(f"[libro final con C55 = {viejo}] ≡ caso «{ce['caso']}» · precio de Sí", ce['precio_si'], eFv['precio_si']))
    comp.append(fila(f"[libro final con C55 = {viejo}] ≡ caso «{ce['caso']}» · ponderado", ce['ponderado'], rFv['pond']))
    comp.append(fila(f"[libro final con C55 = {viejo}] · zona (sin caso en el fichero)", eF['zona'], eFv['zona']))
    cd = [c for c in casos if 'solo el denominador' in c['caso']][0]
    d_rama = cd['precio_si'] - [c for c in casos if 'reproducción' in c['caso']][0]['precio_si']
    out['efecto_en_libro_final'] = dict(
        C55_nuevo=nuevo, C55_viejo=viejo,
        V_C55_nuevo=rF['V'], V_C55_viejo=rFv['V'], pond_nuevo=rF['pond'], pond_viejo=rFv['pond'],
        precio_si_nuevo=eF['precio_si'], precio_si_viejo=eFv['precio_si'], zona_nuevo=eF['zona'], zona_viejo=eFv['zona'],
        d_precio_si=eF['precio_si'] - eFv['precio_si'], d_pond=rF['pond'] - rFv['pond'],
        cociente_precio_si=eF['precio_si'] / eFv['precio_si'], cociente_acciones=viejo / nuevo,
        d_precio_si_en_rama_segun_fichero=d_rama,
        r_op_igual=(rF['d']['C15'] == rFv['d']['C15']))
    out['comparacion'] = comp
    efecto[emp] = out

json.dump(dict(expedientes=salida, efecto_denominador=efecto), open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'salida_replica.json'), 'w'),
          ensure_ascii=False, indent=1, default=str)


def pr(t):
    for f in t:
        e = f['expediente']; r = f['replica']
        print(f"  {f['veredicto']:5s} {f['magnitud'][:60]:60s} exp={str(e)[:22]:22s} rep={str(r)[:22]:22s} drel={f['dif_rel']}")


for emp, s in salida.items():
    print('==', emp, s['motor'], s['modo_v64'], s['estado_cache'])
    pr(s['tabla'])
    print('  -- intermedios')
    pr(s['intermedios'])
for emp, s in efecto.items():
    print('== efecto', emp)
    pr(s['comparacion'])
    print('  efecto en libro final:', s['efecto_en_libro_final'])
