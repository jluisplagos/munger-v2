#!/usr/bin/env python3
"""Séptima comprobación · adapta las sondas ENTREGADAS e3, e7 y e9 (sondas6) y d7 (sondas5) al arnés comun7: VE = 45ff57c, VP = 8196522,
VQ/VPR = 8196522 con las propuestas de la sexta (prop6). Solo cambian la importación del arnés y los rótulos; los casos son los entregados.
Escribe las adaptadas en sondas7/ con el mismo nombre. Uso: python3 -I -B adaptar_sondas.py"""
import os
AQUI = os.path.dirname(os.path.abspath(__file__))
F = os.path.dirname(AQUI)


def adaptar(origen, destino, cambios, nota):
    s = open(os.path.join(F, origen), encoding="utf-8").read()
    for viejo, nuevo, n in cambios:
        assert s.count(viejo) == n, (origen, viejo[:60], s.count(viejo), n)
        s = s.replace(viejo, nuevo)
    cab = '#!/usr/bin/env python3\n"""'
    assert s.startswith(cab)
    s = cab + f"(ADAPTADA en la séptima comprobación: {nota})\n" + s[len(cab):]
    open(os.path.join(AQUI, destino), "w", encoding="utf-8").write(s)
    print("escrita", destino)


# rótulos: primero 8196522 → 45ff57c y después 876bfc2 → 8196522 (con un marcador intermedio)
def rotulos(s_viejo_nuevo):
    return s_viejo_nuevo


ROT = [("8196522", "\0A\0"), ("876bfc2", "8196522"), ("\0A\0", "45ff57c")]


def con_rotulos(origen, destino, cambios, nota):
    s = open(os.path.join(F, origen), encoding="utf-8").read()
    for viejo, nuevo, n in cambios:
        assert s.count(viejo) == n, (origen, viejo[:60], s.count(viejo), n)
        s = s.replace(viejo, nuevo)
    for a, b in ROT:
        s = s.replace(a, b)
    s = s.replace("propuesta de la 5.ª", "propuesta de la 6.ª").replace("propuesta 5.ª", "propuesta 6.ª").replace("las propuestas de la 5.ª", "las propuestas de la 6.ª")
    cab = '#!/usr/bin/env python3\n"""'
    assert s.startswith(cab)
    s = cab + f"(ADAPTADA en la séptima comprobación: {nota})\n" + s[len(cab):]
    open(os.path.join(AQUI, destino), "w", encoding="utf-8").write(s)
    print("escrita", destino)


con_rotulos("sondas6/e3_apostrofo_y_en_numero.py", "e3_apostrofo_y_en_numero.py",
            [("from comun6 import VE, VP, VQ, ACT, ANT, PV  # noqa: E402", "from comun7 import VE, VP, VQ, ACT, ANT, PV  # noqa: E402", 1)],
            "VE = 45ff57c, VP = 8196522, VQ = 8196522 con las propuestas W3–W5 de la sexta; solo cambian el arnés y los rótulos")
con_rotulos("sondas6/e7_v6_declarado_y_casos_sueltos.py", "e7_v6_declarado_y_casos_sueltos.py",
            [("    from comun6 import VE, VP, ACT, ANT  # noqa: E402", "    from comun7 import VE, VP, ACT, ANT  # noqa: E402", 1),
             ('print("   código:", "sexta (8196522)" if "(hito 2, V2)" in open(VEX.__file__, encoding="utf-8").read() else "anterior (876bfc2, 5.ª comprobación)")',
              'print("   código:", "séptima (CAND)" if "(hito 2, W5)" in open(VEX.__file__, encoding="utf-8").read() else "anterior (PREV, 6.ª comprobación)")', 1)],
            "VE = 45ff57c, VP = 8196522; solo cambian el arnés y los rótulos")
s = open(os.path.join(AQUI, "e7_v6_declarado_y_casos_sueltos.py"), encoding="utf-8").read().replace("séptima (CAND)", "séptima (45ff57c)").replace("anterior (PREV, 6.ª comprobación)", "anterior (8196522, 6.ª comprobación)")
open(os.path.join(AQUI, "e7_v6_declarado_y_casos_sueltos.py"), "w", encoding="utf-8").write(s)
con_rotulos("sondas5/d7_unidad_bordes.py", "d7_unidad_bordes.py",
            [("from comun5 import VE, VP, VPR, ACT, ANT  # noqa: E402", "from comun7 import VE, VP, VQ as VPR, ACT, ANT  # noqa: E402", 1),
             ("VPR = 7a6583b con las propuestas del revisor de la cuarta comprobación", "VPR = 8196522 con las propuestas W3–W5 del revisor de la sexta comprobación", 1),
             ("7a6583b: {a[0]:20} 876bfc2: {b[0]:20} propuesta 4.ª: {p[0]:20}", "ANTERIOR: {a[0]:20} CANDIDATA: {b[0]:20} propuesta 6.ª: {p[0]:20}", 1)],
            "VE = 45ff57c, VP = 8196522, VPR = 8196522 con las propuestas de la sexta; solo cambian el arnés y los rótulos; las notas de los casos son las de la quinta")
s = open(os.path.join(AQUI, "d7_unidad_bordes.py"), encoding="utf-8").read().replace("ANTERIOR: {a[0]:20} CANDIDATA: {b[0]:20}", "8196522: {a[0]:20} 45ff57c: {b[0]:20}")
open(os.path.join(AQUI, "d7_unidad_bordes.py"), "w", encoding="utf-8").write(s)
