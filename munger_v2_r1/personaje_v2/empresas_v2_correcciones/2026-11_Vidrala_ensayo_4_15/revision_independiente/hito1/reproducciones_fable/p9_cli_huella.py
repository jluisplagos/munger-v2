"""I13: la orden `huella` de verificacion_entradas.py imprime la huella que basta pegar en el registro (sin `sellar`, sin revisor)."""
import copy, json, os, subprocess, sys
import fx
from fx import VE, con, ent, con_k, resumen, K, REG, c, PV
r = con(lambda g: (ent(g, K)["fuente"].update(documento="(prueba) OTRO documento, cambiado después de la revisión"),))
print("fundamento cambiado sin revisión:", resumen(r, K))
p = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py"), "huella", c, K], capture_output=True, text=True)
h = p.stdout.strip(); print("verificacion_entradas.py huella <expediente> Historia!F6 →", h, "rc", p.returncode)
reg = json.load(open(os.path.join(c, VE.REGISTRO), encoding="utf-8"))
ent(reg, K)["comprobacion"]["vinculo"]["huella"] = h      # se pega a mano; sellado_por y fecha siguen siendo los de la revisión anterior
json.dump(reg, open(os.path.join(c, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("huella pegada a mano en el registro:", resumen(VE.comprobar(c), K))
fx.limpiar()
