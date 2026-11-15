#!/usr/bin/env python3
"""Descomposición aritmética del contraste de motores (entrega 4.5, §7 del encargo). Solo lectura de contraste_motores/.

Uso: python3 -I descomponer_contraste.py   (después de contraste_motores.py)

1. Replica en Python las fórmulas de valor por acción de los motores A y B con los parámetros que la hoja recalculada deja en
   resultados.json (V0, m0, t, palancas, g, tasa, puente, acciones, f) y EXIGE que reproduzca los valores de la hoja de las cinco
   variantes (tolerancia 0,005 €). Si no los reproduce, no descompone nada (código 1).
2. Pasa de B0 a A1 cambiando una sola cosa en cada paso, y atribuye a cada paso la diferencia que produce:
     tasa (r_op → r = 0,09) · puente (restar pasivos netos → no restar) · f (0 → f de T3) · definición de f (T3 → T1 publicada).
   El reparto depende del orden de los pasos (la tasa interactúa con los flujos), así que se da también el orden inverso.
3. Separa en el contraste T3 el efecto de C49 (A2a, A2b), que solo entra por f.
Es aritmética de la hoja; no es una valoración ni un argumento para elegir motor.
"""
import json
import os
import sys

AQUI = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
S = os.path.join(AQUI, "contraste_motores")
K = 3.0


def valor(V0, m0, t, g1, m5, s2c, g, roic, r, puente, acc, f=0.0):
    V = [V0]
    for k in range(1, 11):
        gk = g1 if k <= 5 else g1 + (g - g1) * (k - 5) / 5
        V.append(V[-1] * (1 + gk))
    pv = 0.0
    for k in range(1, 11):
        mk = m0 + (m5 - m0) * min(k, 5) / 5
        pv += (V[k] * mk * (1 - t) - (V[k] - V[k - 1]) / s2c - f * V[k]) / (1 + r) ** k
    n11 = V[10] * (1 + g) * m5 * (1 - t)
    tv = (n11 * (1 - g / roic) - f * V[10] * (1 + g)) / (r - g)
    return (pv + tv / (1 + r) ** 10 - puente) / acc


def escalera(Vs, p):
    lo, hi = 0.0, max(Vs)
    for _ in range(200):
        mid = (lo + hi) / 2
        G = sum(pi * max(v - mid, 0) for v, pi in zip(Vs, p))
        L = sum(pi * max(mid - v, 0) for v, pi in zip(Vs, p))
        lo, hi = (mid, hi) if G >= K * L else (lo, mid)
    return min(lo, Vs[1]), sum(v * pi for v, pi in zip(Vs, p))


def params(v):
    r = json.load(open(os.path.join(S, v, "resultados.json"), encoding="utf-8"))
    p = r["palancas"]
    esc = [(p[c + "14"], p[c + "15"], p[c + "16"], r["g_perpetuo"][i], p[c + "18"]) for i, c in enumerate("BCD")]
    return r, dict(V0=r["V0"], m0=r["m0"], t=r["t"], acc=r["valores"]["C55"], esc=esc, prob=r["probabilidades"],
                   r=(r["r_operativa_C15"] if r["motor"] == "B" else r["valores"]["C56"]),
                   puente=(r["pasivos_netos_B_C16"] if r["motor"] == "B" else 0.0), f=(0.0 if r["motor"] == "B" else r["f"]))


def calc(q):
    Vs = [valor(q["V0"], q["m0"], q["t"], *e, q["r"], q["puente"], q["acc"], q["f"]) for e in q["esc"]]
    ps, pond = escalera(Vs, q["prob"])
    return Vs, pond, ps


print("DESCOMPOSICIÓN DEL CONTRASTE DE MOTORES · aritmética de la hoja, no una valoración")
P = {}
ok = True
for v in ("B0", "A1", "A2", "A2a", "A2b"):
    r, q = params(v)
    P[v] = q
    Vs, pond, ps = calc(q)
    hoja = r["por_escenario"]["valor_por_accion"]
    pr = json.load(open(os.path.join(S, v, "precio.json"), encoding="utf-8"))
    rep = all(abs(a - b) < 0.005 for a, b in zip(Vs, hoja)) and abs(pond - pr["ponderado"]) < 0.005 and abs(ps - pr["precio_si"]) < 0.005
    ok &= rep
    print(f"  réplica {v}: {'REPRODUCE' if rep else 'NO REPRODUCE'} la hoja · V = {[round(x, 2) for x in Vs]} (hoja {[round(x, 2) for x in hoja]}) · ponderado {pond:.2f} ({pr['ponderado']:.2f}) · precio de Sí {ps:.2f} ({pr['precio_si']:.2f})")
comunes = all(P[v][k] == P["B0"][k] for v in P for k in ("V0", "m0", "t", "acc", "esc", "prob"))
print(f"  palancas, probabilidades, V0, margen de partida, tipo y acciones comunes a las cinco variantes: {'SÍ' if comunes else 'NO'}")
if not (ok and comunes):
    print("RESULTADO: la réplica no reproduce la hoja o las variantes no comparten las hipótesis comunes; no se descompone.")
    sys.exit(1)


def recorrido(orden):
    q = dict(P["B0"])
    filas = [("B0 · motor B (ensayo)", calc(q))]
    for paso in orden:
        if paso == "tasa":
            q["r"] = P["A2"]["r"]; nombre = f"tasa r_op {P['B0']['r']:.4f} → r {P['A2']['r']:.2f}"
        elif paso == "puente":
            q["puente"] = 0.0; nombre = f"sin restar pasivos netos ({P['B0']['puente']:.3f} mm)"
        elif paso == "f_T3":
            q["f"] = P["A2"]["f"]; nombre = f"f 0 → {P['A2']['f']:.6f} (T3, condicionada)"
        elif paso == "f_T1":
            q["f"] = P["A1"]["f"]; nombre = f"definición de f: T3 → T1 publicada ({P['A1']['f']:.6f}) → estado = A1"
        if q["r"] == P["A2"]["r"] and q["puente"] == 0.0 and q["f"] == P["A2"]["f"]:
            nombre += " → estado = A2"
        filas.append((nombre, calc(q)))
    return filas


out = {"replica_reproduce": True, "recorridos": {}}
lin = ["# Descomposición del contraste de motores (entrega 4.5)", "",
       "Aritmética de la hoja reproducida en Python (la réplica coincide con las cinco variantes recalculadas por LibreOffice al céntimo). Cada paso cambia una sola cosa. **No es una valoración ni un argumento para elegir motor.** Las palancas de la fase B, las probabilidades, V0, el margen de partida, el tipo y las acciones son comunes.", ""]
for etiqueta, orden in (("tasa → puente → f", ["tasa", "puente", "f_T3", "f_T1"]), ("f → puente → tasa", ["f_T3", "puente", "tasa", "f_T1"])):
    filas = recorrido(orden)
    lin += [f"## Orden {etiqueta}", "", "| Paso | V NORMAL | Δ V NORMAL | Ponderado | Δ ponderado | Precio de Sí | Δ precio de Sí |", "|---|---|---|---|---|---|---|"]
    prev = None
    reg = []
    for nombre, (Vs, pond, ps) in filas:
        d = ("—", "—", "—") if prev is None else (f"{Vs[1] - prev[0][1]:+.2f}", f"{pond - prev[1]:+.2f}", f"{ps - prev[2]:+.2f}")
        lin.append(f"| {nombre} | {Vs[1]:.2f} | {d[0]} | {pond:.2f} | {d[1]} | {ps:.2f} | {d[2]} |")
        reg.append({"paso": nombre, "V": Vs, "ponderado": pond, "precio_si": ps})
        prev = (Vs, pond, ps)
    out["recorridos"][etiqueta] = reg
    lin.append("")
c49 = [(v, calc(P[v])) for v in ("A2", "A2a", "A2b")]
lin += ["## C49 dentro del motor A con T3 (solo entra por f)", "", "| Variante | f | Ponderado | Precio de Sí |", "|---|---|---|---|"]
for v, (Vs, pond, ps) in c49:
    lin.append(f"| {v} | {P[v]['f']:.6f} | {pond:.2f} | {ps:.2f} |")
out["c49"] = [{"variante": v, "f": P[v]["f"], "ponderado": x[1], "precio_si": x[2]} for v, x in c49]
lin += ["", "Cómo entra la financiación en cada motor: en el B, por el puente (deuda + arrendamientos + pensiones + minoritarios − caja de 31-dic-2025) y por `r_op`; en el A, por `f` (que recoge, entre otras partidas, los intereses pagados) y por r. Un f negativo suma flujo cada año y para siempre.", "", "En el motor B, C49 no entra en el valor (f = 0; los arrendamientos están en el puente como deuda contrastada)."]
open(os.path.join(S, "descomposicion.md"), "w", encoding="utf-8").write("\n".join(lin) + "\n")
json.dump(out, open(os.path.join(S, "descomposicion.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("\n".join(lin))
print("\nRESULTADO: réplica reproduce la hoja; descomposición escrita en contraste_motores/descomposicion.md")
