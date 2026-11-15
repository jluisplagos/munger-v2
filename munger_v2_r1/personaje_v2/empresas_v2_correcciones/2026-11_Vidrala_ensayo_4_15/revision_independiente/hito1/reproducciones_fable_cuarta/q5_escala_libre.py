"""Cuarta pasada (sonda q5 de la tercera, adaptada) · con una unidad que no está en VE.UNIDADES la «escala» no tenía ningún control;
desde la corrección de T2 tiene que ser una potencia de diez (el dato sigue sin ser «importe»). Variantes nuevas en r2_t2_cifras.py, parte D."""
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG

vK = fx.inst["celdas"][K]
print("UNIDADES reconocidas:", sorted(VE.UNIDADES))
for u in ("euros", "euro", "€", "EUR (unidades)", "miles de €", "en miles de euros", "thousands of euros", "millones", "M€", "MM€", "mn €", "USD", "acciones", "%", "porcentaje", "veces"):
    print(f"   unidad {u!r}: {'reconocida (escala obligada ' + format(VE.UNIDADES[VE._norm_txt(u)], 'g') + ')' if VE._norm_txt(u) in VE.UNIDADES else 'NO reconocida → escala: cualquier potencia de diez; el dato no es «importe»'}")
pag = fx.nueva_pagina("Véase la nota 1 de la memoria consolidada")
for rot, unidad, escala, vf, cita in (("valor_fuente 1 («nota 1») × escala 849,697", "unidades", vK, 1, "Véase la nota 1 de la memoria consolidada"),
                                      ("lo mismo con la unidad «miles de €» (no reconocida)", "miles de €", vK, 1, "Véase la nota 1 de la memoria consolidada"),
                                      ("control: unidad «miles de euros» (reconocida) con esa escala", "miles de euros", vK, 1, "Véase la nota 1 de la memoria consolidada")):
    r = con(lambda g: ent(g, K)["fuente"].update(unidad=unidad, escala=escala, valor_fuente=vf, cita=cita, pagina=pag), resellar=True)
    print(f"[{K} = {vK} como dato publicado: {rot}] {resumen(r, K, 200)}")
fx.limpiar()
