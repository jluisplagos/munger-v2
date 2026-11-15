import hashlib, os, sys
esperado = {}
for l in open("MANIFIESTO_SHA256.txt", encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        esperado[p] = h
actual = {}
for r, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.relpath(os.path.join(r, f), ".")
        if p != "MANIFIESTO_SHA256.txt":
            actual[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
mod = sorted(p for p in esperado if p in actual and actual[p] != esperado[p])
falt = sorted(p for p in esperado if p not in actual)
extra = sorted(p for p in actual if p not in esperado)
print(f"{len(esperado)} archivos en el manifiesto · modificados {len(mod)} · ausentes {len(falt)} · de más {len(extra)}")
for etiqueta, lista in (("MODIFICADO", mod), ("AUSENTE", falt), ("DE MÁS", extra)):
    for p in lista[:20]:
        print(f"  {etiqueta}: {p}")
print("RESULTADO manifiesto:", "PASA" if not (mod or falt or extra) else "FALLA (¿se ejecutaron ya pruebas en esta copia? descomprimir de nuevo)")
sys.exit(0 if not (mod or falt or extra) else 1)
