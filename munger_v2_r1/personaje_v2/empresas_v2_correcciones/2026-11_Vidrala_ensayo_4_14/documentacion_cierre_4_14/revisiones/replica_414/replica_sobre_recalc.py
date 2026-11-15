# Réplica sobre las copias recalc/ (de las que lee precio_de_si.py según el Anexo C.1).
import sys, json; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/claude/trabajo_4_14/agentes/replica_414')
from replica import Libro, valorar, escalera, isnum
R = '/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/'
out = {}
for d, n in (('viscofan_decisiones/Viscofan', 'Viscofan'), ('vidrala_decisiones/Vidrala', 'Vidrala'), ('elis_decisiones/Elis', 'Elis')):
    b = Libro(R + d + '/recalc/' + n + '_v63_evaluada.xlsx'); res = valorar(b); e = escalera(res)
    pj = json.load(open(R + d + '/precio.json'))
    filas = [('V_MALO', pj['V'][0], res['V'][0]), ('V_NORMAL', pj['V'][1], res['V'][1]), ('V_BUENO', pj['V'][2], res['V'][2]),
             ('ponderado', pj['ponderado'], res['pond']), ('P*', pj['P_estrella'], e['P_estrella']), ('precio de Sí', pj['precio_si'], e['precio_si'])]
    out[n] = []
    for m, x, y in filas:
        r = abs(y - x) / abs(x)
        out[n].append(dict(magnitud=m, expediente=x, replica=y, dif_rel=r, veredicto='PASA' if r <= 1e-6 else 'FALLA'))
        print(n, m, x, y, f'{r:.2e}', 'PASA' if r <= 1e-6 else 'FALLA')
    print(n, 'zona', pj['zona'], e['zona'], 'PASA' if pj['zona'] == e['zona'] else 'FALLA')
    out[n].append(dict(magnitud='zona', expediente=pj['zona'], replica=e['zona'], veredicto='PASA' if pj['zona'] == e['zona'] else 'FALLA'))
json.dump(out, open('/home/claude/trabajo_4_14/agentes/replica_414/salida_replica_recalc.json', 'w'), ensure_ascii=False, indent=1)
