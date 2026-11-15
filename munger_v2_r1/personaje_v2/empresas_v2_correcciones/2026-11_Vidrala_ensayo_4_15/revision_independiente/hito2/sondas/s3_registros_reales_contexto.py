#!/usr/bin/env python3
"""s3 · Registros reales de la 4.14 (solo lectura): para cada entrada numérica con fuente local de texto,
  (1) estado de _cita_cifra con el pasaje de la página (lo que hace el control);
  (2) el signo leído con el CONTEXTO de la página alrededor del pasaje (la página completa en las posiciones de la cifra): ¿cambia?
  (3) ¿la cita empieza o acaba dentro de una cifra de la página (cita cortada a mitad de un número)?
  (4) ¿la cita aparece más de una vez en la página, con lecturas de signo distintas? (el control toma la primera aparición)
  (5) formas de la cita: empieza por la cifra, es solo la cifra, contiene «%», fechas con guion…
No modifica nada. Uso: python3 -I -B s3_registros_reales_contexto.py > salida"""
import collections, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV

E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["elis_decisiones/Elis", "elis_motor_A/Elis", "vidrala/Vidrala", "vidrala_decisiones/Vidrala", "viscofan/Viscofan", "viscofan_decisiones/Viscofan"]


def pasajes(cita, pagina):
    palabras = str(cita or "").split()
    t = re.sub(r"[\xa0  ]", " ", str(pagina))
    return t, [m.span() for m in re.finditer(r"\s+".join(re.escape(w) for w in palabras), t, re.I)]


def signos_en(t, ini, fin, vf):
    out = []
    for c in VE._cifras(vf):
        for m in re.finditer(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", t[ini:fin]):
            out.append((ini + m.start(), ini + m.end()))
    return sorted(set(out))


tot = collections.Counter()
for exp in EXPS:
    d = os.path.join(E414, exp)
    reg, err = VE.cargar(d)
    cuenta = collections.Counter()
    casos = collections.defaultdict(list)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(d, f.get("archivo")) if f.get("archivo") else None
        rt = ruta if (ruta and str(ruta).lower().endswith(".txt")) else (VE._ruta_fuente(d, f.get("archivo_texto")) if f.get("archivo_texto") else None)
        if not rt:
            cuenta["sin texto examinable"] += 1
            continue
        est_p, pag = VE._pagina_examinable(rt, f.get("pagina"))
        if est_p != "ok":
            cuenta[f"página {est_p}"] += 1
            continue
        cita = f.get("cita")
        estado, det = VE._cita_cifra(cita, vf, pag)
        cuenta[("cero" if vf == 0 else "negativo" if vf < 0 else "positivo") + " · " + estado] += 1
        if VE._norm_txt(cita) not in VE._norm_txt(pag):
            cuenta["cita no está en la página"] += 1
            continue
        t, sp = pasajes(cita, pag)
        if not sp:
            cuenta["pasaje no encontrado (se lee la cita)"] += 1
            casos["pasaje no encontrado"].append((e["celda"], vf, cita[:120]))
            continue
        if len(sp) > 1:
            cuenta["cita con más de una aparición en la página"] += 1
            lect = []
            for a, b in sp:
                lect.append(VE._cita_cifra(t[a:b], vf)[0])
            if len(set(lect)) > 1:
                casos["apariciones con lecturas distintas"].append((e["celda"], vf, lect, cita[:120]))
        a, b = sp[0]
        # (3) cita cortada dentro de una cifra de la página
        if (a > 0 and re.match(r"[\d]", t[a]) and re.match(r"[\d.,]", t[a - 1])) or (b < len(t) and re.match(r"\d", t[b - 1]) and re.match(r"\d|[.,]\d", t[b:b + 2])):
            casos["cita cortada dentro de una cifra"].append((e["celda"], vf, repr(t[max(0, a - 12):b + 12])))
        if vf != 0:
            # (2) signo con el contexto de la página
            s = 1 if vf > 0 else -1
            dentro = [VE._signo_en_cita(t[a:b], i - a, j - a) for i, j in signos_en(t, a, b, vf)]
            contexto = [VE._signo_en_cita(t, i, j) for i, j in signos_en(t, a, b, vf)]
            if dentro != contexto:
                cuenta["el contexto de la página cambia la lectura del signo"] += 1
                casos["contexto cambia el signo"].append((e["celda"], vf, f.get("signo"), dentro, contexto, repr(t[max(0, a - 25):b + 25])[:230]))
            if None in dentro and estado == "ok":
                cuenta["ok con alguna aparición indeterminada"] += 1
                casos["ok con aparición indeterminada"].append((e["celda"], vf, dentro, cita[:140]))
            if len(dentro) > 1:
                cuenta["cifra más de una vez en la cita"] += 1
        c0 = str(cita).strip()
        if any(c0 == x for x in VE._cifras(vf)):
            cuenta["la cita es solo la cifra"] += 1
            casos["cita = solo la cifra"].append((e["celda"], vf, c0))
        elif any(c0.startswith(x) for x in VE._cifras(vf)):
            cuenta["la cita empieza por la cifra"] += 1
            casos["cita empieza por la cifra"].append((e["celda"], vf, c0[:90], repr(t[max(0, a - 20):a + 20])))
        if "%" in c0:
            cuenta["cita con %"] += 1
        if re.search(r"\d-\d|[a-zA-Z]-\d", c0):
            cuenta["cita con guion pegado entre cifras o letras (intervalo, fecha)"] += 1
    print(f"\n=== {exp}")
    for k, v in sorted(cuenta.items()):
        print(f"   {v:4d}  {k}")
    for k, lst in casos.items():
        print(f"   -- {k}: {len(lst)}")
        for x in lst[:12]:
            print("        ", x)
    tot.update(cuenta)
print("\n=== TOTAL (seis expedientes)")
for k, v in sorted(tot.items()):
    print(f"   {v:4d}  {k}")
