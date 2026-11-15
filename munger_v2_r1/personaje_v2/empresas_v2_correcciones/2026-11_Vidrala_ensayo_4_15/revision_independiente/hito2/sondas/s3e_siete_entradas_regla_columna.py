#!/usr/bin/env python3
"""s3e · Las entradas reales cuyo signo positivo sale de la regla «guion a 2+ espacios = otra columna» (s3b): la línea completa de la
página y su vecindad, para que se vea si el guion es de verdad el cero de otra columna (solo lectura)."""
import os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
MARCAS = VE.GUIONES + VE.MENOS_UNICODE
for exp in ["vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan", "elis_decisiones/Elis"]:
    d = os.path.join(E414, exp)
    reg, _ = VE.cargar(d)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or vf == 0 or e.get("clase") != "dato_publicado":
            continue
        ruta = VE._ruta_fuente(d, f.get("archivo")) if f.get("archivo") else None
        if not ruta or not str(ruta).lower().endswith(".txt"):
            continue
        est_p, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est_p != "ok":
            continue
        t = re.sub(r"[\xa0  ]", " ", pag)
        palabras = str(f.get("cita") or "").split()
        m0 = re.search(r"\s+".join(re.escape(w) for w in palabras), t, re.I)
        if not m0:
            continue
        pas = m0.group(0)
        usa = False
        for c in VE._cifras(vf):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", pas):
                if re.search("[" + re.escape(MARCAS) + r"]\s{2,}$", pas[:m.start()]):
                    usa = True
        if not usa:
            continue
        ini = t.rfind("\n", 0, m0.start()) + 1
        fin = t.find("\n", m0.end())
        lineas = t[:ini].rstrip("\n").split("\n")[-4:] + [">>> " + t[ini:fin]] + t[fin + 1:].split("\n")[:2]
        print(f"\n=== {exp} · {e['celda']} · valor_fuente {vf!r} signo {f.get('signo')} · modelo {e.get('valor_modelo')!r} · {os.path.basename(ruta)} p.{f.get('pagina')}")
        print(f"    cita: {f.get('cita')!r}")
        for l in lineas:
            if l.strip():
                print("    | " + l[:190])
