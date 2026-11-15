# Coherencia de CAMBIOS_ARCHIVOS.txt (4.9) con el árbol y con el de la 4.8.1 prístina (solo lectura)
import os, hashlib, re
def parse(p):
    sec=None; d={"MOD":{}, "NUE":{}}; cur=None
    for l in open(p, encoding="utf-8"):
        l=l.rstrip("\n")
        if l.startswith("## MODIFICADOS"): sec="MOD"; continue
        if l.startswith("## NUEVOS"): sec="NUE"; continue
        if l.startswith("## ELIMINADOS"): sec=None; continue
        if not sec or l.startswith("#") or not l.strip(): continue
        if l.startswith("  "):
            v=l.strip(); d[sec][cur]= v.split(" → ") if sec=="MOD" else v
        else: cur=l
    return d
R="/home/claude/vigencia_4_9/munger_v2_r1"; P="/home/claude/pristina_481/munger_v2_r1"
c=parse(R+"/CAMBIOS_ARCHIVOS.txt"); c0=parse(P+"/CAMBIOS_ARCHIVOS.txt")
H=lambda p: hashlib.sha256(open(p,"rb").read()).hexdigest()
print("mod",len(c["MOD"]),"nue",len(c["NUE"]))
mal=[p for p,(a,b) in c["MOD"].items() if H(os.path.join(R,p))!=b]
mal+= [p for p,b in c["NUE"].items() if H(os.path.join(R,p))!=b]
print("huellas 'nuevo' que no coinciden con el árbol:", mal)
# base de modificados debe ser la misma que en 4.8.1
print("modificados con base distinta a la de 4.8.1:", [p for p in c["MOD"] if p in c0["MOD"] and c0["MOD"][p][0]!=c["MOD"][p][0]])
print("modificados nuevos vs 4.8.1:", set(c["MOD"])^set(c0["MOD"]))
print("nuevos que ya no están:", set(c0["NUE"])-set(c["NUE"]))
arbol=set()
for dp,dn,fn in os.walk(R):
    dn[:]=[x for x in dn if x!="__pycache__"]
    for f in fn: arbol.add(os.path.relpath(os.path.join(dp,f),R))
listados=set(c["MOD"])|set(c["NUE"])
sin=arbol-listados-{"CAMBIOS_ARCHIVOS.txt","MANIFIESTO_SHA256.txt"}
print("sin cambios (árbol − listados):", len(sin))
# los 'sin cambios' deben ser idénticos a la 4.8.1 prístina y no estar en sus listas
print("sin cambios que difieren de 4.8.1:", [p for p in sin if not os.path.exists(os.path.join(P,p)) or H(os.path.join(P,p))!=H(os.path.join(R,p))])
print("sin cambios que en 4.8.1 eran mod/nue:", [p for p in sin if p in c0["MOD"] or p in c0["NUE"]])
