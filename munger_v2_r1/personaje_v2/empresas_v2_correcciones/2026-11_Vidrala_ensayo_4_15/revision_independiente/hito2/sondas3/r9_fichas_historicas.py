#!/usr/bin/env python3
"""r9 · N1 y N2 (tercera pasada): ¿cambia la ficha o el informe de algún expediente CERRADO del árbol con el ficha.py de la tercera candidata?
Para cada carpeta del árbol congelado con cierre_vigente.json que no es un archivo de historial (12 expedientes), sobre UNA copia temporal:
ficha.py e informe.py --provisional con el código de la candidata anterior (92b2362) y con el de la tercera (f3d15e8), con la configuración
por defecto y con la experimental V6.4.1 (MUNGER_CONFIG). Se comparan byte a byte ficha_provisional.json e informe_provisional.md de los dos
códigos. Si son iguales, el cambio de N1 y N2 no altera lo que esos expedientes generarían. No ejecuta el pipeline ni LibreOffice.
Uso: python3 -I -B r9_fichas_historicas.py"""
import hashlib, json, os, shutil, subprocess, sys, tempfile
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONG = os.path.join(os.path.dirname(F), "munger_v2_r1", "personaje_v2")
PVS = {"anterior": os.path.join(F, "prev", "munger_v2_r1", "personaje_v2"), "tercera": os.path.join(F, "copia", "munger_v2_r1", "personaje_v2")}
TMP = tempfile.mkdtemp(prefix="rev3_r9_", dir=os.path.join(F, "tmp"))
ENV = dict(os.environ, PATH=os.path.join(F, "bin") + os.pathsep + os.environ["PATH"], PYTHONDONTWRITEBYTECODE="1", TMPDIR=os.path.join(F, "tmp"))
exps = []
for d, ds, fs in os.walk(CONG):
    ds[:] = [x for x in ds if x not in (".lo_perfil", "__pycache__")]
    if "cierre_vigente.json" in fs and "historial_cierres" not in d and "antecedentes" not in d and "salidas_copia_relevo" not in d:
        exps.append(d)
print("expedientes cerrados (cierre_vigente.json, fuera de historiales y antecedentes):", len(exps))
n_dist = 0
for d in sorted(exps):
    rel = os.path.relpath(d, CONG)
    dst = os.path.join(TMP, hashlib.sha1(rel.encode()).hexdigest()[:8], os.path.basename(d))
    shutil.copytree(d, dst, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"), symlinks=True)
    orig = {n: (hashlib.sha256(open(os.path.join(d, n), "rb").read()).hexdigest()[:12] if os.path.exists(os.path.join(d, n)) else None) for n in ("ficha.json", "ficha_provisional.json")}
    fo = json.load(open(os.path.join(d, "ficha.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "ficha.json")) else {}
    res = {}
    for cfg in (None, "config_v2_v641_experimental.json"):
        for et, pv in PVS.items():
            for n in ("ficha_provisional.json", "informe_provisional.md"):
                if os.path.exists(os.path.join(dst, n)):
                    os.remove(os.path.join(dst, n))
            env = dict(ENV, **({"MUNGER_CONFIG": os.path.join(pv, cfg)} if cfg else {}))
            env.pop("MUNGER_CONFIG", None) if not cfg else None
            r1 = subprocess.run([sys.executable, "-B", os.path.join(pv, "scripts", "ficha.py"), dst, "--provisional"], capture_output=True, text=True, env=env)
            r2 = subprocess.run([sys.executable, "-B", os.path.join(pv, "scripts", "informe.py"), dst, "--provisional"], capture_output=True, text=True, env=env)
            out = {}
            for n in ("ficha_provisional.json", "informe_provisional.md"):
                p = os.path.join(dst, n)
                out[n] = hashlib.sha256(open(p, "rb").read()).hexdigest()[:12] if os.path.exists(p) else None
            fp = json.load(open(os.path.join(dst, "ficha_provisional.json"), encoding="utf-8")) if out["ficha_provisional.json"] else {}
            res[(cfg or "por defecto", et)] = (r1.returncode, r2.returncode, out, "verificacion_entradas" in fp, "aptitud_de_uso" in fp)
    print(f"\n{rel}\n   ficha.json oficial: bloque verificacion_entradas {'sí' if 'verificacion_entradas' in fo else 'no'} · aptitud_de_uso {'sí' if 'aptitud_de_uso' in fo else 'no'}"
          f" · registro {'sí' if os.path.exists(os.path.join(d, 'verificacion_entradas.json')) else 'no'} · entrada_efectiva.json {'sí' if os.path.exists(os.path.join(d, 'entrada_efectiva.json')) else 'no'}")
    for cfg in ("por defecto", "config_v2_v641_experimental.json"):
        a, b = res[(cfg, "anterior")], res[(cfg, "tercera")]
        igual = a[2] == b[2] and a[:2] == b[:2]
        n_dist += not igual
        print(f"   config {cfg:34} códigos (ficha, informe) anterior {a[:2]} tercera {b[:2]} · bloque I20 {a[3]}/{b[3]} · aptitud_de_uso {a[4]}/{b[4]} · ficha e informe provisionales "
              + ("IGUALES byte a byte" if igual else f"DISTINTOS: {a[2]} / {b[2]}"))
    shutil.rmtree(os.path.dirname(dst), ignore_errors=True)
print(f"\nexpedientes × configuraciones con salida distinta entre los dos códigos: {n_dist}")
shutil.rmtree(TMP, ignore_errors=True)
