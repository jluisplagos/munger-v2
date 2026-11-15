"""Sección 6 de comprobar_continuacion.py: fases, resultados, estado, contraste de motores (entrega 4.5). Solo lectura.

Las cifras esperadas son las que produjo esta ejecución del ensayo (9-nov-2026); el control comprueba que el expediente entregado
las conserva y que son coherentes entre sí, no que sean «correctas» como valoración.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

ESPERADO = {"V": [53.6704195834156, 70.7721966823599, 86.4887624455832], "ponderado": 70.4951544152157, "precio_si": 65.68808732041568, "zona": "caro",
            "r_op": 0.0869221113286847, "puente": 160.784}


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def _j(*p):
    return json.load(open(os.path.join(*p), encoding="utf-8"))


def comprobaciones(AQUI, E, O, RAIZ):
    out = []

    def c(n, cond, det=""):
        out.append((n, bool(cond), det))
    st = _j(E, "estado_pipeline.json")
    c("Pipeline terminado en el paso 14: estado concluido, auditoría APROBADO, motor B", st["paso"] == 14 and st["estado_analisis"] == "concluido" and st.get("auditoria") == "APROBADO" and st.get("motor") == "B")
    c("Sin correcciones ni vueltas (fase B, fase C, auditoría, C→B, B→A: 0)", all(v == 0 for v in st["intentos"].values()), str(st["intentos"]))
    h = "\n".join(st["historial"])
    for patron, nombre in ((r"verificar_todo\.sh .*PASS", "verificar_todo.sh: PASS"), (r"comprobar_celdas_v2\.py .*--fases A,B,C → 0 · PASS: 0 errores", "comprobar_celdas_v2 (fases A, B, C): 0 errores"),
                           (r"comprobar_gramatica\.py Vidrala --tras-recalculo --con-fase-c → 0 · código 0 · errores 0", "gramática tras la fase C: código 0, 0 errores"),
                           (r"validar_esquema\.py ficha\.json ficha .*VÁLIDO", "ficha.json válida")):
        c(f"Historial del pipeline: {nombre}", re.search(patron, h))
    for f, n in (("fase_a.json", "fase_a"), ("fase_b.json", "fase_b"), ("fase_c.json", "fase_c")):
        c(f"{f} es nuevo: distinto del original (no se reutilizan salidas antiguas)", _sha(os.path.join(E, f)) != _sha(os.path.join(O, f)))
    for f in ("extracto_v63.md", "auditoria.md", "fase_a.md", "fase_b.md", "fase_c.md"):
        c(f"{f} nuevo y distinto del original", os.path.exists(os.path.join(E, f)) and _sha(os.path.join(E, f)) != _sha(os.path.join(O, f)))
    fa, fb, fc = _j(E, "fase_a.json"), _j(E, "fase_b.json"), _j(E, "fase_c.json")
    c("Fase A: C62 = «No · financiación cambia mucho» (motor B, hipótesis principal fijada antes de los resultados)", fa["celdas"]["C62"] == "No · financiación cambia mucho")
    c("Fase A: r (C56) = 0,09 conservada", fa["celdas"]["C56"] == 0.09)
    import openpyxl
    wb = openpyxl.load_workbook(os.path.join(E, "recalc", "Vidrala_v63_evaluada.xlsx"), data_only=True)
    an, pa, hi = wb["Análisis"], wb["Palancas"], wb["Historia"]
    c("Libro evaluado: Análisis!C56 = 0,09 y C62 = motor B; C76 vacía (motor B)", an["C56"].value == 0.09 and an["C62"].value == "No · financiación cambia mucho" and an["C76"].value in (None, ""))
    s2c = [pa[x].value for x in ("B16", "C16", "D16")]
    c("Fase B: S2C decidido por la fase (0,9 / 0,9 / 1,0), no copiado de la referencia Historia C53 ≈ 0,9159", s2c == [0.9, 0.9, 1.0] and all(abs(x - hi["C53"].value) > 1e-6 for x in s2c), f"{s2c} · C53 {hi['C53'].value:.4f}")
    g = [an[x].value for x in ("B68", "C68", "D68")]
    roic = [pa[x].value for x in ("B18", "C18", "D18")]
    rr = _j(E, "resultados.json")
    c("Condiciones del motor B en los tres escenarios: g < r_op y ROIC a largo plazo > g", all(x < rr["r_operativa_C15"] for x in g) and all(a > b for a, b in zip(roic, g)), f"g {g} · ROIC {roic} · r_op {rr['r_operativa_C15']:.4f}")
    c("Probabilidades de la lista que suman 1", abs(sum(an[x].value for x in ("B69", "C69", "D69")) - 1) < 1e-12)
    c("Caja (Historia L24) = 108,352, sin restar el dividendo a cuenta de 43,338", abs(hi["L24"].value - 108.352) < 1e-9)
    pu = hi["L22"].value + hi["L23"].value + max(0, hi["L25"].value) + hi["L26"].value - hi["L24"].value
    c("Puente del motor B = deuda + arrendamientos + pensiones + minoritarios − caja de 31-dic-2025 = 160,784 (sin doble cómputo del dividendo)", abs(pu - ESPERADO["puente"]) < 1e-9 and abs(rr["pasivos_netos_B_C16"] - ESPERADO["puente"]) < 1e-9, f"{pu:.3f}")
    pr = _j(E, "precio.json")
    c("Resultados mecánicos conservados (V 53,67 / 70,77 / 86,49; ponderado 70,50; precio de Sí 65,69; zona caro)",
      all(abs(a - b) < 1e-9 for a, b in zip(pr["V"], ESPERADO["V"])) and abs(pr["ponderado"] - ESPERADO["ponderado"]) < 1e-9 and abs(pr["precio_si"] - ESPERADO["precio_si"]) < 1e-9 and pr["zona"] == ESPERADO["zona"])
    c("Ponderado = Σ p·V y la escalera coincide con la hoja (C86)", abs(sum(p * v for p, v in zip(pr["p"], pr["V"])) - pr["ponderado"]) < 1e-9 and pr.get("coincide_C86") is True)
    c104 = str(an["C104"].value)
    c("C104 empieza por «Pendiente de decisión de cartera», sin porcentajes, y declara que es un resultado mecánico no comparable con el precio ni una recomendación",
      c104.startswith("Pendiente de decisión de cartera") and "%" not in c104 and "resultado mecánico de un ensayo exploratorio" in c104 and "no comparable con el precio" in c104 and "no es una recomendación de compra ni de espera" in c104)
    for celda in ("B101", "B102", "C103", "C93"):
        v = str(an[celda].value or "")
        c(f"Análisis!{celda} sin cifras heredadas de la etapa 1 (Chile, 30-jun-2026, ≈74 €, ≈48 €)", not re.search(r"Chile|30-jun-2026|≈ ?74|≈ ?48", v))
    fi = _j(E, "ficha.json")
    c("ficha.json: concluido, cubo Vigilar, motor B, valor ponderado igual a precio.json", fi["estado_analisis"] == "concluido" and fi["cubo"] == "Vigilar" and fi["motor"] == "B" and abs(fi["valor_ponderado"] - pr["ponderado"]) < 1e-9)
    au = open(os.path.join(E, "auditoria.md"), encoding="utf-8").read()
    c("auditoria.md: «Veredicto: APROBADO» y ningún punto FALLA", "Veredicto: APROBADO" in au and "FALLA" not in au)
    c("Fase C: estado concluido con la condición de ensayo exploratorio de ruta A", fc.get("estado_analisis") == "concluido" and "ruta A" in json.dumps(fc, ensure_ascii=False))
    # contraste
    S = os.path.join(AQUI, "contraste_motores")
    cr = _j(S, "contraste_resultados.json")
    c("Contraste: hecho sobre el libro evaluado final (huella igual)", cr["sha256_libro_de_partida"] == _sha(os.path.join(E, "Vidrala_v63_evaluada.xlsx")))
    var = {v["variante"]: v for v in cr["variantes"]}
    c("Contraste B0 reproduce el ensayo principal (ponderado y precio de Sí)", abs(var["B0"]["ponderado"] - pr["ponderado"]) < 1e-9 and abs(var["B0"]["precio_si"] - pr["precio_si"]) < 1e-9)
    esperado_f = {"A1": -0.0276077999509027, "A2": -0.009847, "A2a": -0.008307, "A2b": -0.012860}
    c("Contraste: f de A1 (T1) y de A2/A2a/A2b (T3, C49 4,5 / 6,8 / 0) iguales a las réplicas de la 4.3", all(abs(var[k]["f"] - v) < 5e-7 for k, v in esperado_f.items()), str({k: round(var[k]["f"], 6) for k in esperado_f}))
    c("Contraste: las variantes A tienen motor A y r = 0,09; B0 motor B", var["B0"]["motor"] == "B" and all(var[k]["motor"] == "A" and var[k]["r_C56"] == 0.09 for k in esperado_f))
    r = subprocess.run([sys.executable, "-I", os.path.join(AQUI, "scripts", "descomponer_contraste.py")], capture_output=True, text=True)
    c("Descomposición: la réplica reproduce las cinco variantes de la hoja y la salida conservada es idéntica",
      r.returncode == 0 and "RESULTADO: réplica reproduce la hoja" in r.stdout and open(os.path.join(S, "descomposicion.md"), encoding="utf-8").read() in r.stdout)
    return out
