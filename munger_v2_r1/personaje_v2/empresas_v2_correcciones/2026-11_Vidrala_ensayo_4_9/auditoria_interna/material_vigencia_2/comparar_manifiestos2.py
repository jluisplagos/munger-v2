"""Manifiesto del paquete frente al árbol y frente a MANIFIESTO_4_8_1.txt (segundo control de vigencia 4.9). Solo lectura."""
import hashlib, os, sys
R = "/home/claude/vigencia2_4_9/munger_v2_r1"
E = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9"
def man(p):
    return {l.rstrip("\n").split("  ", 1)[1]: l.split("  ", 1)[0] for l in open(p, encoding="utf-8") if l.strip() and not l.startswith("#")}
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
arbol = {os.path.relpath(os.path.join(r, f), R) for r, ds, fs in os.walk(R) for f in fs}
m = man(os.path.join(R, "MANIFIESTO_SHA256.txt"))
print("cabecera:", open(os.path.join(R, "MANIFIESTO_SHA256.txt"), encoding="utf-8").readline().strip()[:200])
print("archivos en el árbol:", len(arbol), "· en el manifiesto:", len(m))
print("en el árbol y no en el manifiesto:", sorted(arbol - set(m)))
print("en el manifiesto y no en el árbol:", sorted(set(m) - arbol))
print("huellas distintas:", [p for p in m if p in arbol and sha(os.path.join(R, p)) != m[p]])
m481 = man(os.path.join(R, E, "reproduccion", "MANIFIESTO_4_8_1.txt"))
mod = sorted(p for p in m481 if p in arbol and sha(os.path.join(R, p)) != m481[p])
aus = sorted(p for p in m481 if p not in arbol)
nue = sorted(p for p in arbol if p not in m481)
print("4.8.1:", len(m481), "· modificados", len(mod), "· ausentes", len(aus), "· nuevos", len(nue))
print("modificados:", mod)
print("nuevos fuera de E:", [p for p in nue if not p.startswith(E + "/")])
sys.path.insert(0, os.path.join(R, E, "scripts"))
src = open(os.path.join(R, E, "scripts", "comprobar_entrega_4_9.py"), encoding="utf-8").read()
import ast
t = ast.parse(src)
cam = next(ast.literal_eval(n.value) for n in t.body if isinstance(n, ast.Assign) and getattr(n.targets[0], "id", "") == "CAMBIADOS_FRENTE_A_4_8_1")
print("CAMBIADOS_FRENTE_A_4_8_1 (", len(cam), "):", sorted(cam))
print("modificados == CAMBIADOS − {MANIFIESTO}:", set(mod) == cam - {"MANIFIESTO_SHA256.txt"}, "· diferencia:", sorted(set(mod) ^ (cam - {"MANIFIESTO_SHA256.txt"})))
hist = [p for p in mod if p.startswith("personaje_v2/empresas_v2_correcciones/") or p.startswith("contrastes/") or p.startswith("personaje_v2/empresas_v2/")]
print("históricos/expedientes modificados:", hist)
print("__pycache__/.pyc en el árbol:", [p for p in arbol if "__pycache__" in p or p.endswith(".pyc")])
dirs_vacios = [os.path.relpath(r, R) for r, ds, fs in os.walk(R) if not ds and not fs]
print("carpetas vacías:", len(dirs_vacios), dirs_vacios[:5])
print("carpetas .lo_perfil:", [os.path.relpath(r, R) for r, ds, fs in os.walk(R) if os.path.basename(r) == ".lo_perfil"])
