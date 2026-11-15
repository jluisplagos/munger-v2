"""Revisión interna 4.10: identidades de variantes_4_10.json con aritmética propia (no usa variantes_4_10.py)."""
import json, sys
d = json.load(open(sys.argv[1], encoding="utf-8"))
V = {v["variante"]: v for v in d["variantes"]}
K = ("MALO", "NORMAL", "BUENO", "ponderado", "precio_de_si")
p = d["probabilidades"]
def val(n, k): return V[n]["valores"][k]
ref = {"MALO": 53.670420, "NORMAL": 70.772197, "BUENO": 86.488762, "ponderado": 70.495154, "precio_de_si": 65.688087}
print("base frente a la referencia del encargo:", {k: round(val("base", k) - ref[k], 7) for k in K})
for n in V:
    pon = sum(pi * val(n, e) for pi, e in zip(p, ("MALO", "NORMAL", "BUENO")))
    print(f"{n:28s} ponderado recalculado − JSON = {pon - val(n,'ponderado'):+.2e} · g<r_op {max(V[n]['valores'][g] for g in ('g_MALO','g_NORMAL','g_BUENO')) < val(n,'r_op')} · r={V[n]['valores']['r_C56']} · prob suma {sum(p)}")
# N6: r_op = (r E + i (1-tau) D)/(E+D)
for n in ("base", "N6_E_2025", "N7_conjunto", "C1_31dic2025_con_derecho", "N6_E_2025_tau_2025"):
    v = V[n]["valores"]; E, D, i, t, r = v["E_capitalizacion"], v["D_C64"], v["i_C63"], v["tau_C11"], v["r_C56"]
    rop = (r * E + i * (1 - t) * D) / (E + D)
    print(f"N6 {n:28s} E={E} D={D} i={i:.6f} tau={t} r_op_formula={rop:.9f} r_op_JSON={v['r_op']:.9f} dif={rop - v['r_op']:+.1e}")
v = V["N6_E_2025_tau_2025"]["valores"]
t25 = 0.2433
print("N6 tau 2025 con 0,2433 en el escudo:", (v["r_C56"]*v["E_capitalizacion"] + v["i_C63"]*(1-t25)*v["D_C64"])/(v["E_capitalizacion"]+v["D_C64"]), "frente a", v["r_op"], "· tau_C11 de la variante", v["tau_C11"])
print("E N6 = 90,10 × 35,206258 =", 90.10 * 35.206258, "· E C1 = 90,10 × 35,182858 =", 90.10 * 35.182858, "· referencia 87,90 × 35,206 =", 87.90 * 35.206)
# N7 puro: V' = V N/N'
N0, N1 = 35.206, 35.182858
print("N7 puro V·N/N' − V':", {k: f"{val('base',k)*N0/N1 - val('N7_N_puro',k):+.1e}" for k in K})
# N8: V_sin = V_con − 43,338/N
print("N8 sin − (base − 43,338/35,206):", {k: f"{val('N8_sin_derecho',k) - (val('base',k) - 43.338/N0):+.1e}" for k in K}, "· −43,338/N =", -43.338/N0)
print("N8 puente:", V["N8_sin_derecho"]["valores"]["puente"], "= 160,784 + 43,338 =", 160.784 + 43.338, "· L26", V["N8_sin_derecho"]["valores"]["L26"], "· caja", V["N8_sin_derecho"]["valores"]["caja_C66"], "· r_op igual", V["N8_sin_derecho"]["valores"]["r_op"] == val("base","r_op"), "· E", V["N8_sin_derecho"]["valores"]["E_capitalizacion"])
# C2 = C1 − 43,338/N1
print("C2 − (C1 − 43,338/35,182858):", {k: f"{val('C2_31dic2025_sin_derecho',k) - (val('C1_31dic2025_con_derecho',k) - 43.338/N1):+.1e}" for k in K}, "· −43,338/N1 =", -43.338/N1)
# N5: ΔV = −ΔL25/N
dL = V["N5_neto_impuestos"]["valores"]["L25"] - 6.223
print("N5 L25", V["N5_neto_impuestos"]["valores"]["L25"], "= 6,223×0,75 =", 6.223*0.75, "· ΔV − (−ΔL25/N):", {k: f"{val('N5_neto_impuestos',k)-val('base',k) + dL/N0:+.1e}" for k in K}, "· −ΔL25/N =", -dL/N0)
# P3
for n in ("P3_B1", "P3_B2"):
    v = V[n]["valores"]; print(n, "C48", v["C48"], "C49", v["C49"], "FCF", v["FCF_base"], "f", v["f"], "ΔFCF", v["FCF_base"] - 161.2, "ΔV", {k: val(n,k)-val("base",k) for k in K})
print("P3 medias: (5,861+6,117+8,314)/3 =", (5.861+6.117+8.314)/3, "· I (2,131+2,179+2,452)/3 =", (2.131+2.179+2.452)/3, "· P = ", (5.861+6.117+8.314)/3-(2.131+2.179+2.452)/3)
# N10
v = V["N10_MALO_historia_adversa"]["valores"]; print("N10 MALO", v["MALO"], "pon", v["ponderado"], "pSí", v["precio_de_si"], "NORMAL igual", v["NORMAL"] == val("base","NORMAL"), "BUENO igual", v["BUENO"] == val("base","BUENO"))
for k, s in d["sensibilidad_de_pesos_N10"].items():
    print("N10 pesos", k, json.dumps(s, ensure_ascii=False)[:600])
# i
print("i = 20,8/((393,312+262,913)/2) =", 20.8/((393.312+262.913)/2), "· D = 196,080+66,833 =", 196.080+66.833, "· 2024: 300,624+92,688 =", 300.624+92.688)
# diferencias declaradas en el informe
print("Δ pon N6", val("N6_E_2025","ponderado")-val("base","ponderado"), "· Δ pon N7 puro", val("N7_N_puro","ponderado")-val("base","ponderado"), "· Δ pon N7 conj", val("N7_conjunto","ponderado")-val("base","ponderado"), "· Δ tau vs N6", val("N6_E_2025_tau_2025","ponderado")-val("N6_E_2025","ponderado"), "· Δ tau vs base", val("N6_E_2025_tau_2025","ponderado")-val("base","ponderado"))
print("C1 == N7_conjunto:", all(val("C1_31dic2025_con_derecho",k) == val("N7_conjunto",k) for k in K))
for n in V: print("celdas", n, V[n]["celdas"], V[n].get("sustituciones_estructurales"))
