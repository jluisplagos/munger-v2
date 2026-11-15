"""Tercera pasada · N9 (mensajes con repr): los dos mensajes señalados en la segunda pasada y los que siguen usando «:g»."""
import fx4 as fx
from fx4 import VE, con, ent, con_k, resumen, K, REG

pag = fx.nueva_pagina("Magnitud sintética: 849697.4")
r = con(lambda g: ent(g, K)["fuente"].update(unidad="unidades", escala=0.001, valor_fuente=849697.4, cita="Magnitud sintética: 849697.4", pagina=pag), resellar=True)
print("[dato publicado que NO es un importe (unidad «unidades»), 849697,4 × 0,001 frente a 849,697 del libro]\n   ", "; ".join(con_k(r, K)))
import os
fuera = os.path.join(os.path.dirname(fx.TMP), "fuera_del_paquete_q9"); os.makedirs(fuera, exist_ok=True)
open(os.path.join(fuera, "t.txt"), "w").write("[PDF PAGE 1]\nx\n")
import hashlib
open(os.path.join(fx.FS, "f.pdf"), "wb").write(b"%PDF-1.4\n")
s = hashlib.sha256(open(os.path.join(fx.FS, "f.pdf"), "rb").read()).hexdigest()
r = con(lambda g: ent(g, K)["fuente"].update(archivo="fuentes_sinteticas/f.pdf", sha256=s, archivo_texto=os.path.join(fuera, "t.txt"), sha256_texto="0" * 64), resellar=True)
print("[archivo_texto que EXISTE, pero fuera del expediente y del paquete]\n   ", "; ".join(con_k(r, K)))
vd = fx.inst["celdas"]["Historia!H15"]
def deriva(g):
    g["entradas"].append({"celda": "aux:r", "id": "aux:r", "ambito": "auxiliar", "uso": "x", "material": True, "clase": "convencion", "valor_modelo": 0.88704,
                          "hipotesis": {"fundamento": "x", "alternativas": ["x"], "limites": ["x"]}, "comprobacion": dict(fx.COMPROBADA)})
    e = ent(g, "Historia!H15"); e["fuente"] = {}
    e.update(clase="derivado", justificacion_clase="x", derivacion={"origenes": ["aux:r"], "formula": 'o["aux:r"]', "conciliacion": "x"})
r = con(deriva, resellar=True)
print("[derivado 0,88704 frente a 0,887 del libro (el caso del mensaje «0.1009 y 0.1009»)]\n   ", "; ".join(con_k(r, "Historia!H15")))
import re, inspect
src = inspect.getsource(VE)
print("formatos «:g» que quedan en mensajes de verificacion_entradas.py:", re.findall(r"\{[^{}]*:g\}", src))
fx.limpiar()
