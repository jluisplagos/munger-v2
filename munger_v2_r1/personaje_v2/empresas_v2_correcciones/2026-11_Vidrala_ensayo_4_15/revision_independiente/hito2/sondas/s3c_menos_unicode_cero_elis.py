#!/usr/bin/env python3
"""s3c · ¿El signo menos Unicode «−» (U+2212) se usa para imprimir un cero en las fuentes reales? (el código dice: «siempre un signo menos (no
se usa para imprimir un cero)»). Solo lectura: páginas citadas por los registros reales de la 4.14.
A) apariciones de «−» aislado (entre espacios o al final de línea) y de «−» a UN espacio de una cifra, con su contexto;
B) lo que lee el control en esos pasajes: _cita_cifra(pasaje, ±cifra) y el cero impreso como «−»."""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
for exp in ["elis_decisiones/Elis", "vidrala_decisiones/Vidrala", "viscofan_decisiones/Viscofan"]:
    d = os.path.join(E414, exp)
    reg, _ = VE.cargar(d)
    paginas = {}
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        ruta = VE._ruta_fuente(d, f.get("archivo")) if f.get("archivo") else None
        if ruta and str(ruta).lower().endswith(".txt"):
            est_p, pag = VE._pagina_examinable(ruta, f.get("pagina"))
            if est_p == "ok":
                paginas[(os.path.basename(ruta), str(f.get("pagina")))] = pag
    todo = collections.Counter()
    un_espacio, aislado = [], []
    for (arch, pg), pag in sorted(paginas.items()):
        t = re.sub(r"[\xa0  ]", " ", pag)
        for car, nombre in (("−", "U+2212 −"), ("-", "U+002D -"), ("–", "U+2013 –"), ("—", "U+2014 —")):
            todo[f"{nombre}: aislado (espacio o inicio antes; 2+ espacios o fin de línea después)"] += len(re.findall(r"(?:(?<=\s)|^)" + re.escape(car) + r"(?=\s{2,}|\s*$)", t, re.M))
            todo[f"{nombre}: a UN espacio de una cifra o «(»"] += len(re.findall(r"(?:(?<=\s)|^)" + re.escape(car) + r" (?=[\d(])", t, re.M))
            todo[f"{nombre}: pegado a una cifra"] += len(re.findall(r"(?:(?<=\s)|^)" + re.escape(car) + r"(?=\d)", t, re.M))
        for m in re.finditer(r"(?:(?<=\s)|^)− (?=[\d(])", t, re.M):
            ini = t.rfind("\n", 0, m.start()) + 1
            fin = t.find("\n", m.end())
            un_espacio.append((arch, pg, t[ini:fin if fin > 0 else None].strip()[:170]))
        for m in re.finditer(r"(?:(?<=\s)|^)−(?=\s{2,}\(?\d)", t, re.M):
            ini = t.rfind("\n", 0, m.start()) + 1
            fin = t.find("\n", m.end())
            aislado.append((arch, pg, t[ini:fin if fin > 0 else None].strip()[:170]))
    print(f"\n=== {exp} ({len(paginas)} páginas citadas)")
    for k, v in sorted(todo.items()):
        if v:
            print(f"   {v:5d}  {k}")
    print(f"   -- «−» (U+2212) a UN espacio de una cifra: {len(un_espacio)} líneas")
    for x in un_espacio[:14]:
        print("        ", x)
    print(f"   -- «−» (U+2212) aislado y seguido, en la misma línea, de una cifra a 2+ espacios: {len(aislado)} líneas")
    for x in aislado[:6]:
        print("        ", x)

print("\n=== lo que lee el control")
for cita, vf in [("Acquisitions  −   (12.3)", 0), ("Acquisitions  -   (12.3)", 0), ("Acquisitions −", 0), ("Dividends − 42.2", 42.2), ("Dividends − 42.2", -42.2),
                 ("Dividends - 42.2", 42.2), ("Dividends - 42.2", -42.2), ("Dividends −                 42.2", 42.2), ("Dividends −                 42.2", -42.2)]:
    print(f"   _cita_cifra({cita!r}, {vf!r}) -> {VE._cita_cifra(cita, vf)}")
