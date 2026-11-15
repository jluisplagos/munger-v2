#!/usr/bin/env python3
"""s15 · [Propuesta, apoyo; NO es una implementación revisada] Leer la cifra completa y su signo en la PÁGINA, en el lugar donde está la
cita (todas sus apariciones), con el contexto de la línea alrededor del pasaje, en vez de dentro de la cita:
  - una cita cortada dentro de una cifra de la página deja de contener esa cifra como cifra completa;
  - una marca de signo pegada al pasaje por fuera (paréntesis, menos) cuenta;
  - si la cita aparece varias veces con lecturas distintas, o no se localiza, el signo es indeterminado (pendiente).
Se comprueba: A) los contraejemplos de s2 y s14 se rechazan; B) las 32 formas de la batería (casos_ok y casos_no de SG, con la página =
la cita) dan la misma categoría que el código de la candidata; C) las entradas numéricas de los registros reales dan lo mismo que ahora."""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV


def cita_cifra_en_pagina(cita, vf, pagina):
    if not VE._num(vf):
        return "ausente", "valor no numérico"
    palabras = str(cita or "").split()
    if not palabras:
        return "ausente", "cita vacía"
    t = re.sub(r"[\xa0  ]", " ", str(pagina))
    spans = [m.span() for m in re.finditer(r"\s+".join(re.escape(w) for w in palabras), t, re.I)]
    if not spans:
        return "signo_indeterminado", "el pasaje de la cita no se localiza en la página con sus espacios"
    lecturas = set()
    for a, b in spans:
        # contexto: la línea (o líneas) del pasaje
        ini_l = t.rfind("\n", 0, a) + 1
        fin_l = t.find("\n", b)
        fin_l = len(t) if fin_l < 0 else fin_l
        linea = t[ini_l:fin_l]
        a0, b0 = a - ini_l, b - ini_l
        if vf == 0 and (any(a0 <= m.start() < b0 for m in re.finditer(r"(?<![\w.,])[-–—−](?![\w.,]| ?[\d(])", linea))
                        or any(a0 <= m.start() < b0 for m in re.finditer(r"(?<=[\d)] )[-–—−](?= [\d(])", linea))):
            lecturas.add(("ok", "cero impreso como guion"))
            continue
        signos = []
        for c in VE._cifras(vf):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(c) + r"(?!\d|[.,]\d)", linea):
                if a0 <= m.start() and m.end() <= b0:
                    signos.append(VE._signo_en_cita(linea, m.start(), m.end()))
        if not signos:
            lecturas.add(("ausente", "la cifra no aparece como cifra completa en la página dentro del pasaje citado"))
        elif vf == 0:
            lecturas.add(("ok", "cero"))
        else:
            s = 1 if vf > 0 else -1
            if s in signos and -s not in signos:
                lecturas.add(("ok", "signo publicado igual al de valor_fuente"))
            elif -s in signos and s not in signos and None not in signos:
                lecturas.add(("signo_distinto", "la página la publica con el signo contrario"))
            else:
                lecturas.add(("signo_indeterminado", "signo que no puede determinarse"))
    if len({x[0] for x in lecturas}) > 1:
        return "signo_indeterminado", f"la cita aparece {len(spans)} veces en la página con lecturas distintas: {sorted(x[0] for x in lecturas)}"
    return sorted(lecturas)[0]


print("== A · contraejemplos (se espera: ninguno «ok»)")
VFk = 849697.0
for nombre, pag, cita, vf in [
    ("s2 B1", f"Partida sintética de Historia!F6: -{VFk:.3f}", f"{VFk:.3f}", VFk), ("s2 B2", f"Partida sintética de Historia!F6: ({VFk:,.3f})", f"{VFk:,.3f}", VFk),
    ("s2 B3", f"Partida sintética de Historia!F6: ({VFk:,.3f}) (1.000)", f"{VFk:,.3f}) (1.000)", VFk), ("s2 B4", f"Partida sintética de Historia!F6: −{VFk:.3f}", f"{VFk:.3f}", VFk),
    ("s2 C2 (C48, 2023)", "Paiements de passifs locatifs (y compris intérêts sur passifs locatifs) (150,8) (130,8)", "130,8", 130.8),
    ("s14 1", "Partida sintética de Historia!F6: 8496970", "Partida sintética de Historia!F6: 849697", VFk), ("s14 2", "Partida sintética de Historia!F6: 1849697.000", "849697.000", VFk),
    ("s14 3", "Partida sintética de Historia!F6: 849697.499", "Partida sintética de Historia!F6: 849697", VFk), ("s14 4", "Partida sintética de Historia!F6: 849.697.123", "Partida sintética de Historia!F6: 849.697", VFk),
    ("s14 5", "Partida: 0.49", "Partida: 0", 0), ("s14 6", "Ejercicio 2019", "0", 0),
    ("s11 C1", f"Total       -      {VFk:.3f}\nResumen\nTotal - {VFk:.3f}", f"Total - {VFk:.3f}", VFk), ("s11 D1", f"İmporte - {VFk:.3f}", f"i̇mporte -  {VFk:.3f}", VFk)]:
    print(f"   {nombre:18} candidata: {VE._cita_cifra(cita, vf, pag)[0]:20} propuesta: {cita_cifra_en_pagina(cita, vf, pag)}")
print("   controles positivos:", [cita_cifra_en_pagina(c, v, p)[0] for c, v, p in [
    ("Partida sintética de Historia!F6: 849697.000", VFk, "Partida sintética de Historia!F6: 849697.000"), ("(130,8)", -130.8, "locatifs) (150,8) (130,8)"),
    ("Saldo 0", 0, "Saldo 0\n"), ("Acquisitions - (12.3)", 0, "Acquisitions      -      (12.3)"), ("Net gains − 42.2", 0, "Net gains    −      42.2")]])

print("\n== B · las formas de la batería SG (página = cita)")
casos_ok = [("Importe: (149.5)", -149.5), ("Importe: −149,5", -149.5), ("Importe: − 149,5", -149.5), ("Importe: -149,5", -149.5),
            ("Importe: —149,5", -149.5), ("(€149,5)", -149.5), ("(149,5 €)", -149.5), ("-€149,5", -149.5), ("+149,5", 149.5),
            ("Importe: 149,5", 149.5), ("Saldo 0", 0), ("Saldo (0)", 0), ("Saldo -0", 0), ("Acquisitions  -   (12.3)", 0), ("Acquisitions  -   (12.3)", -12.3),
            ("Payments -55.320 -62.755", -62755), ("Interest paid (7,230) (9,776)", -9776), ("2019-2020", 2019)]
casos_no = [("Importe: -149.5", 149.5), ("Importe: 149.5", -149.5), ("Importe: (149.5)", 149.5), ("Importe: −149,5", 149.5), ("Importe - 149,5", 149.5), ("Importe - 149,5", -149.5),
            ("x 149,5 (149,5)", 149.5), ("-(149,5)", -149.5), ("(149,5", -149.5), ("149,5-", 149.5), ("2019-2020", 2020), ("EBITDA-149,5", -149.5), ("Importe: 150", 149.5), ("Importe: -150", -149.5)]
dist = [(c, v, VE._cita_cifra(c, v)[0], cita_cifra_en_pagina(c, v, c)[0]) for c, v in casos_ok + casos_no if VE._cita_cifra(c, v)[0] != cita_cifra_en_pagina(c, v, c)[0]]
print(f"   {len(casos_ok) + len(casos_no)} formas; categoría distinta entre la candidata y la propuesta: {len(dist)} {dist[:4]}")

print("\n== C · registros reales de la 4.14 (seis expedientes): estado con la candidata y con la propuesta")
E414 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
tot = collections.Counter()
cambian = []
for exp in ["elis_decisiones/Elis", "elis_motor_A/Elis", "vidrala/Vidrala", "vidrala_decisiones/Vidrala", "viscofan/Viscofan", "viscofan_decisiones/Viscofan"]:
    d = os.path.join(E414, exp)
    reg, _ = VE.cargar(d)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf = f.get("valor_fuente")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(d, f.get("archivo")) if f.get("archivo") else None
        if not ruta or not str(ruta).lower().endswith(".txt"):
            continue
        est_p, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est_p != "ok" or VE._norm_txt(f.get("cita")) not in VE._norm_txt(pag):
            tot["sin página o cita fuera de la página"] += 1
            continue
        a, b = VE._cita_cifra(f.get("cita"), vf, pag)[0], cita_cifra_en_pagina(f.get("cita"), vf, pag)[0]
        tot[f"candidata {a} · propuesta {b}"] += 1
        if a != b:
            cambian.append((exp, e["celda"], vf, a, b, str(f.get("cita"))[:90]))
for k, v in sorted(tot.items()):
    print(f"   {v:5d}  {k}")
print("   entradas que cambian de estado:", len(cambian))
for x in cambian[:12]:
    print("      ", x)
