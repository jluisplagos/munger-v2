#!/usr/bin/env python3
"""s13 · C48 de Elis con el CAMBIO del hito 2 (sin LibreOffice): valor, términos y el texto de «fuente» que escribe calcular_entrada
(se trunca a 1500 caracteres antes de añadir la decisión): ¿cabe entero con las tres transformaciones declaradas? Comparación con el hito 1."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE, PV
import fase1_historia as FH

E415 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]
C2 = json.load(open(os.path.join(E415, "configuracion", "cambio_elis_c48_4_15.json"), encoding="utf-8"))["analisis"]["C48"]
C1 = json.load(open(os.path.join(E415, "reproduccion", "codigo_4_15_hito1", "cambio_elis_c48_4_15.json.txt"), encoding="utf-8"))["analisis"]["C48"]
print("claves de C48 en el CAMBIO:", sorted(C2))
print("diferencias del CAMBIO.analisis.C48 entre el hito 1 y el hito 2 (fuera de los componentes):", {k: (C1.get(k), C2.get(k)) for k in set(C1) | set(C2) if k != "calculo" and C1.get(k) != C2.get(k)})
c1, c2 = C1["calculo"], C2["calculo"]
print("cálculo: operación, años, términos, redondeo, decisión iguales:", all(c1.get(k) == c2.get(k) for k in ("operacion", "anios", "terminos", "redondeo", "decision")))
for a in sorted(c2["componentes"]["pagos_arrendamientos_con_intereses"]):
    x1, x2 = c1["componentes"]["pagos_arrendamientos_con_intereses"][a], c2["componentes"]["pagos_arrendamientos_con_intereses"][a]
    print(f"   {a}: valor {x1['valor']} → {x2['valor']} · claves nuevas {sorted(set(x2) - set(x1))} · resto igual: {all(x1[k] == x2[k] for k in x1)} · valor_fuente {x2.get('valor_fuente')} signo {x2.get('signo')}")
r = FH.calcular_entrada("C48", {"calculo": c2}, H, anios, ELIS)
print("valor:", r["valor"], "· sin redondear:", r["valor_sin_redondear"])
antes_dec = r["fuente"][: -(len(c2["decision"]) + 2)] if c2.get("decision") else r["fuente"]
print("longitud del texto de fuente antes de la decisión:", len(antes_dec), "(límite 1500) · total:", len(r["fuente"]))
print("final del texto antes de la decisión:", repr(antes_dec[-260:]))
esperado = [f"{a} pagos_arrendamientos_con_intereses" for a in c2["anios"]] + [f"{a} arrendamientos_principal" for a in c2["anios"]] + [f"{a} intereses_financiacion" for a in c2["anios"]]
print("términos presentes en el texto de fuente:", {e: (e in r["fuente"]) for e in esperado})
print("páginas de los tres componentes en el texto:", {a: (f"p.{c2['componentes']['pagos_arrendamientos_con_intereses'][a]['pagina']})" in antes_dec.split(f'{a} pagos_arrendamientos_con_intereses')[-1][:420]) for a in sorted(c2['componentes']['pagos_arrendamientos_con_intereses'])})
r1 = FH.calcular_entrada("C48", {"calculo": c1}, H, anios)
print("hito 1 (sin carpeta): valor", r1["valor"], "· longitud del texto de fuente:", len(r1["fuente"]))
