# Z-6: aritmética y coherencia de n4/efectos/efectos_n4.json (sin recalcular libros)
import json, hashlib, os, sys
R = "/home/claude/vigencia_4_9/munger_v2_r1"
sys.path.insert(0, R + "/personaje_v2/scripts"); sys.dont_write_bytecode = True
import precio_de_si as PS
d = json.load(open(R + "/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_9/n4/efectos/efectos_n4.json", encoding="utf-8"))
V = {v["variante"]: v for v in d["variantes"]}
b = V["base"]["valores"]
k = ["MALO (Análisis!B78)", "NORMAL (Análisis!C78)", "BUENO (Análisis!D78)"]
ok = True
for n, v in V.items():
    vv = v["valores"]
    p = PS.p_estrella([vv[x] for x in k], [0.2, 0.6, 0.2], 3)
    pond = 0.2 * vv[k[0]] + 0.6 * vv[k[1]] + 0.2 * vv[k[2]]
    dl = {x: (None if not isinstance(vv[x], float) else round(vv[x] - b[x], 6)) for x in vv}
    c_delta = all((v["delta"][x] is None and dl[x] is None) or (dl[x] is not None and abs((v["delta"][x] or 0) - dl[x]) < 1e-9) for x in vv)
    c_sha = hashlib.sha256(open(os.path.join(R, v["copia"]), "rb").read()).hexdigest() == v["copia_sha256"]
    c_p = abs(p - vv["precio de Sí (precio_de_si.p_estrella, k = 3)"]) < 1e-9
    c_pond = abs(pond - vv["ponderado (Análisis!C83)"]) < 1e-6
    ok &= c_delta and c_sha and c_p and c_pond
    print(f"{n:22s} delta=var−base {c_delta} · sha copia {c_sha} · P* recalculado {p:.6f} igual {c_p} · ponderado 0,2/0,6/0,2 {c_pond} · "
          f"C52 {vv['FCF simplificado (Análisis!C52)']} · f {vv['f (Diagnóstico V6!C12)']*100:.2f} % · C50 «{vv['control de rango de f (Diagnóstico V6!C50)'][:10]}»")
print("L26: delta ponderado", V["L26_mas_1"]["delta"]["ponderado (Análisis!C83)"], "· −1/35,206 =", round(-1 / 35.206, 6))
f = V["C48_mas_1"]["delta"]["f (Diagnóstico V6!C12)"]
print("f lineal en C52: Δf/ΔC48 =", f, "· hipótesis 2,254 →", round(2.254 * f, 6), V["H_C48_int_arrend"]["delta"]["f (Diagnóstico V6!C12)"], "· doble cómputo 21,74 →", round(21.74 * f, 6), V["H_C48_doble_computo"]["delta"]["f (Diagnóstico V6!C12)"])
print("TODO COHERENTE:", ok)
