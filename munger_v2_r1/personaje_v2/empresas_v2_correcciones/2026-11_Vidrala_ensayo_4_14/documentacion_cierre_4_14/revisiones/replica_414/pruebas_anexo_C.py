# Casos de prueba del Anexo C.5 (k = 3) sobre la forma cerrada y la bisección de la réplica.
import sys; sys.dont_write_bytecode = True
sys.path.insert(0, '/home/claude/trabajo_4_14/agentes/replica_414')
from replica import p_estrella_cerrada, p_estrella_biseccion, G_, L_
casos = [((60, 100, 150), (0.25, 0.5, 0.25), 88.3333333333, 21.25, 7.0833333333, 102.5, 88.3333333333),
         ((90, 100, 160), (0.2, 0.6, 0.2), 102.3076923077, 11.5384615385, 3.8461538462, 110, 100),
         ((100, 100, 100), (0.2, 0.6, 0.2), 100, 0, 0, 100, 100),
         ((-20, 80, 200), (0.2, 0.6, 0.2), 54.2857142857, 44.5714285714, 14.8571428571, 84, 54.2857142857),
         ((40, 70, 300), (0.3, 0.5, 0.2), 77.3076923077, 44.5384615385, 14.8461538462, 107, 70)]
ok = True
for V, p, Ps, G, L, pond, psi in casos:
    Pc = p_estrella_cerrada(list(V), list(p)); Pb = p_estrella_biseccion(list(V), list(p))
    pd = sum(a * b for a, b in zip(V, p)); si = min(Pc, V[1])
    perm = p_estrella_cerrada([V[2], V[0], V[1]], [p[2], p[0], p[1]])
    c = (abs(Pc - Ps) < 1e-8 and abs(Pb - Ps) < 1e-8 and abs(G_(Pc, V, p) - G) < 1e-8 and abs(L_(Pc, V, p) - L) < 1e-8
         and abs(pd - pond) < 1e-9 and abs(si - psi) < 1e-8 and abs(perm - Pc) < 1e-12 and abs(G_(Pc, V, p) - 3 * L_(Pc, V, p)) < 1e-9
         and Pc >= min(V) - 1e-12 and Pc <= pd + 1e-12 and p_estrella_cerrada(list(V), list(p), 4.0) <= Pc + 1e-12)
    ok &= c
    print('PASA' if c else 'FALLA', V, p, 'P*=', Pc, 'bisección=', Pb, 'precio de Sí=', si)
print('TODOS PASAN' if ok else 'HAY FALLOS')
