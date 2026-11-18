#!/usr/bin/env python3
"""Batería de la hoja resumen en lenguaje llano (scripts/hoja_resumen.py). Usa LibreOffice (bajo flock del cerrojo común).

Trabaja sobre COPIAS de dos expedientes cerrados existentes:
  - empresas_v2/Hermes (plantilla V6.3, motor A, sin bloque de aptitud en la ficha);
  - empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/vidrala_decisiones/Vidrala (V6.4 experimental, motor B, con
    aptitud_de_uso y cierre_vigente.json).
Comprueba que la hoja sale, que sus cifras coinciden con la ficha y con el libro recalculado (un recálculo independiente al 10 %),
que la sensibilidad a la tasa heredada (9 %) reproduce EXACTAMENTE el precio de Sí oficial, que ninguna frase del texto llano
carece de origen, que no cambia ningún archivo del expediente ni de los originales, y la regeneración cuando cambia la ficha.

Uso (desde personaje_v2/): python3 -B pruebas/test_hoja_resumen.py
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
SC = os.path.join(PV, "scripts")
sys.path.insert(0, SC)
sys.dont_write_bytecode = True
import hoja_resumen as H  # noqa: E402
import precio_de_si as PS  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import pipeline as PIPE  # noqa: E402

RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


def huellas_dir(d):
    out = {}
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x != "__pycache__"]
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = H.sha256(p)
    return out


def correr(args):
    r = subprocess.run([sys.executable, "-I", os.path.join(SC, "hoja_resumen.py")] + args, capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


EXPEDIENTES = {
    "Hermes": os.path.join(PV, "empresas_v2", "Hermes"),
    "Vidrala": os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "vidrala_decisiones", "Vidrala"),
}

# ------------------------------------------------------------------------------------------------ unidades: frases y limpieza
paso("frases: no corta en «p. 104», «EE. UU.» ni iniciales; corta ante «2)»",
     H.frases("W. Kurtz manda. EE. UU. pesa [ES, PDF p. 104] mucho. 1) Uno. 2) Dos.") == ["W. Kurtz manda.", "EE. UU. pesa [ES, PDF p. 104] mucho.", "1) Uno.", "2) Dos."])
paso("limpiar: quita corchetes de fuente y referencias a celdas, conserva cifras y paréntesis con contenido",
     H.limpiar("Gana el 13,8 % (13,8 % frente al 9,3 %; Historia C55, Palancas H18) y vale 241 € (B78:D78) [ES, PDF p. 9].")
     == "Gana el 13,8 % (13,8 % frente al 9,3 %) y vale 241 €.")
paso("limpiar: un elemento de referencia dentro de una parte se quita («(9,4 %, Historia C33:D33)» → «(9,4 %)»)",
     H.limpiar("fue la tasa (9,4 %, Historia C33:D33) sin") == "fue la tasa (9,4 %) sin")
paso("limpiar: conserva las citas de Munger y los paréntesis con valores («(C33 = −1,35)», «(p(MALO) a 0,3)»)",
     H.limpiar("«x» (AIWTK p.36; HIM). Sin deuda (C33 = −1,35) y (p(MALO) a 0,3).") == "«x» (AIWTK p.36; HIM). Sin deuda (C33 = −1,35) y (p(MALO) a 0,3).")
paso("limpiar: quita el ordinal inicial «1)»", H.limpiar("1) El ROIC ya baja.") == "El ROIC ya baja.")
fc_falso = {"celdas": {"B101": "Uno dos tres cuatro cinco seis. Siete.", "B102": "Ocho nueve diez once doce trece."}, "cambiaria_de_cubo": {"a_no": "Catorce."}}
sel = H.seleccionar_parrafo(fc_falso)
paso("verificar_origen_frases: una frase con una cifra añadida, un campo inexistente o un índice fuera de rango se rechazan",
     H.verificar_origen_frases(sel, fc_falso) == []
     and H.verificar_origen_frases([dict(sel[0], texto=sel[0]["texto"] + " 42")], fc_falso)
     and H.verificar_origen_frases([dict(sel[0], campo="B999")], fc_falso)
     and H.verificar_origen_frases([dict(sel[0], indice=7)], fc_falso))

# ------------------------------------------------------------------------------------------------ expedientes cerrados (copias)
tmp = tempfile.mkdtemp(prefix="test_hoja_")
originales = {n: huellas_dir(p) for n, p in EXPEDIENTES.items()}
try:
    for nombre, orig in EXPEDIENTES.items():
        exp = os.path.join(tmp, nombre)
        shutil.copytree(orig, exp)
        antes = huellas_dir(exp)
        rc, out = correr([exp, "--trabajo", tmp])
        md_p, js_p = os.path.join(exp, H.SALIDA_MD), os.path.join(exp, H.SALIDA_JSON)
        paso(f"{nombre}: la hoja sale (código 0, hoja_resumen.md y hoja_resumen.json)", rc == 0 and os.path.isfile(md_p) and os.path.isfile(js_p), out.strip()[-160:])
        if rc != 0:
            continue
        despues = huellas_dir(exp)
        nuevos = sorted(set(despues) - set(antes))
        cambiados = sorted(p for p in antes if despues.get(p) != antes[p])
        paso(f"{nombre}: no cambia ningún archivo del expediente; solo añade la hoja (y nada de copias temporales)",
             not cambiados and nuevos == [H.SALIDA_JSON, H.SALIDA_MD], f"cambiados {cambiados[:3]} · nuevos {nuevos}")
        md = open(md_p, encoding="utf-8").read()
        t = json.load(open(js_p, encoding="utf-8"))
        ficha = json.load(open(os.path.join(exp, "ficha.json"), encoding="utf-8"))
        precio = json.load(open(os.path.join(exp, "precio.json"), encoding="utf-8"))
        fase_c = json.load(open(os.path.join(exp, "fase_c.json"), encoding="utf-8"))
        mon = ficha.get("moneda")
        v = t["veredicto"]
        paso(f"{nombre}: el veredicto coincide con la ficha (estado, cubo, acción, precio de Sí, precio, zona, ponderado)",
             v["estado_analisis"] == ficha["estado_analisis"] and v["cubo"] == ficha["cubo"] and v["accion"] == ficha["decision"]["accion"]
             and v["precio_si"] == ficha["escalera"]["precio_si"] and v["precio"] == ficha["precio"] and v["zona"] == ficha["insumos_decision_cartera"]["zona"]
             and v["ponderado"] == ficha["valor_ponderado"])
        linea = next((l for l in md.splitlines() if l.startswith("**Veredicto del personaje**")), "")
        paso(f"{nombre}: una sola línea de veredicto con cubo, acción, precio de Sí redondeado y «experimental; no apto para dinero real»",
             sum(l.startswith("**Veredicto del personaje**") for l in md.splitlines()) == 1 and f"**{ficha['cubo']}**" in linea
             and f"**{ficha['decision']['accion']}**" in linea and H.dinero(ficha["escalera"]["precio_si"], mon) in linea
             and "experimental; no apto para dinero real" in linea, linea[:140])
        paso(f"{nombre}: la aptitud sigue a la ficha (si la ficha la declara, se cita; si no, no se presume)",
             ("según la ficha, aptitud_de_uso" in linea) == isinstance(ficha.get("aptitud_de_uso"), dict)
             and (ficha.get("aptitud_de_uso") or {}).get("apto_para_dinero_real") is not True)
        # --- texto llano
        par = t["parrafo"]
        cuerpo = md.split("## En pocas palabras", 1)[1].split("*Origen de cada frase*", 1)[0].strip()
        paso(f"{nombre}: el párrafo tiene entre 5 y 8 frases, cada una con su número de origen en la hoja",
             5 <= len(par) <= 8 and all(f"{e['texto']} [{n}]" in cuerpo for n, e in enumerate(par, 1))
             and len(re.findall(r"\[\d\]", cuerpo)) == len(par), f"{len(par)} frases")
        paso(f"{nombre}: el párrafo empieza por la tesis (qué hace la empresa), incluye la tesis inversa y «a No»",
             par[0]["campo"] == "B101" and par[0]["indice"] == 0 and any(e["campo"] == "B102" for e in par)
             and any(e["campo"] == "cambiaria_de_cubo.a_no" for e in par))
        todas = par + [e for x in t["lo_que_lo_haria_falso"].values() for e in x]
        fallos = H.verificar_origen_frases(todas, fase_c)
        paso(f"{nombre}: ninguna frase del texto llano carece de origen (frase exacta de fase_c.json, limpieza reproducible, sin cifras nuevas)",
             not fallos and len(todas) >= 6, f"{len(todas)} frases" + (f" · {fallos[:2]}" if fallos else ""))
        res = json.load(open(os.path.join(exp, "resultados.json"), encoding="utf-8"))
        paso(f"{nombre}: la tesis y la tesis inversa de fase_c.json son las del libro evaluado (Análisis!B101, B102)",
             all(res["celdas_juicio_analisis"][c] == fase_c["celdas"][c] for c in ("B101", "B102")))
        rc2, out2 = correr([exp, "--verificar-origen"])
        paso(f"{nombre}: --verificar-origen comprueba el origen (código 0)", rc2 == 0 and "ORIGEN COMPROBADO" in out2, out2.strip()[-100:])
        t_mal = json.loads(json.dumps(t))
        t_mal["parrafo"][1]["texto"] += " Subirá un 30 %."
        json.dump(t_mal, open(js_p, "w", encoding="utf-8"), ensure_ascii=False)
        rc3, out3 = correr([exp, "--verificar-origen"])
        paso(f"{nombre}: una frase inventada en la hoja se detecta (--verificar-origen, código 4)", rc3 == 4 and "SIN ORIGEN" in out3, out3.strip()[-120:])
        json.dump(t, open(js_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        # --- sensibilidad
        s = t["sensibilidad"]
        filas = {round(f["r"], 4): f for f in s["filas"]}
        f9 = filas.get(0.09)
        paso(f"{nombre}: tasas 7, 8, 9, 10 y 11 %, cada copia con su r leída en Análisis!C56 tras el recálculo",
             sorted(filas) == [0.07, 0.08, 0.09, 0.10, 0.11] and all(abs(f["C56_leida"] - f["r"]) < 1e-15 for f in s["filas"]))
        paso(f"{nombre}: al 9 % la copia reproduce EXACTAMENTE el precio de Sí oficial (y ponderado, zona, V, crecimiento implícito)",
             f9 is not None and f9["precio_si"] == precio["precio_si"] and f9["ponderado"] == precio["ponderado"] and f9["zona"] == precio["zona"]
             and f9["V"] == precio["V"] and f9["g_impl_actual"] == precio["g_impl_actual"] and s["reproduce_oficial"] is True,
             f"{f9 and f9['precio_si']!r} vs {precio['precio_si']!r}")
        paso(f"{nombre}: el precio de Sí y el ponderado bajan al subir la tasa, y el crecimiento que exige el precio sube",
             all(filas[a]["precio_si"] > filas[b]["precio_si"] and filas[a]["ponderado"] > filas[b]["ponderado"]
                 and filas[a]["g_impl_actual"] < filas[b]["g_impl_actual"] for a, b in zip(sorted(filas), sorted(filas)[1:])))
        p = precio["p"]
        paso(f"{nombre}: cada fila cuadra con la regla de la escalera (P* con k = {precio['k']} sobre V y las mismas probabilidades) y su zona",
             all(abs(f["precio_si"] - min(PS.p_estrella(f["V"], p, precio["k"]), f["V"][1])) < 1e-9
                 and abs(f["ponderado"] - sum(a * b for a, b in zip(f["V"], p))) < 1e-6 * f["ponderado"]
                 and f["zona"] == PS.zona(f["precio"], f["V"][0] if f["V"][0] > 0 else None, f["precio_si"], f["ponderado"]) for f in s["filas"]))
        # recálculo independiente al 10 %: copia propia, recalc.sh bajo flock y lectura directa de las celdas con openpyxl
        import openpyxl
        from v63_xml import LibroV63
        libro = H.libro_evaluado(exp)
        d10 = os.path.join(tmp, f"indep_{nombre}")
        os.makedirs(os.path.join(d10, "in"))
        L = LibroV63(libro)
        L.escribir_celdas({"Análisis!C56": 0.10})
        L.guardar(os.path.join(d10, "in", os.path.basename(libro)))
        subprocess.run(["flock", H.LOCK_DEFECTO, "bash", os.path.join(SC, "recalc.sh"), os.path.join(d10, "in", os.path.basename(libro)),
                        os.path.join(d10, "out"), os.path.join(d10, "perfil")], capture_output=True, text=True)
        wb = openpyxl.load_workbook(os.path.join(d10, "out", os.path.basename(libro)), data_only=True, read_only=True)
        a = wb["Análisis"]
        V10 = [a["B78"].value, a["C78"].value, a["D78"].value]
        f10 = filas[0.10]
        paso(f"{nombre}: al 10 % las cifras coinciden con el libro recalculado de forma independiente (B78:D78, C83, C86)",
             V10 == f10["V"] and a["C83"].value == f10["ponderado"] and a["C86"].value == f10["C86_hoja"]
             and isinstance(f10["g_impl_actual"], float) and abs(f10["g_impl_actual"] - a["C86"].value) <= 0.005, f"{V10} vs {f10['V']}")
        wb.close()
        shutil.rmtree(d10, ignore_errors=True)
        tabla = md.split("## Cuánto depende de la tasa", 1)[1].split("## Predicciones", 1)[0]
        paso(f"{nombre}: la tabla de la hoja muestra las cifras redondeadas de cada fila y rotula la heredada",
             all(H.dinero(f["precio_si"], mon) in tabla and H.dinero(f["ponderado"], mon) in tabla and H.pct(f["g_impl_actual"]) in tabla for f in s["filas"])
             and "| 9 % (heredada) |" in tabla)
        zonas = [filas[r]["zona"] for r in (0.08, 0.09, 0.10)]
        paso(f"{nombre}: rótulos «el 9 % es provisional», «la prueba del 10 % es información, no condición» y firmeza según el tramo 8–10 %",
             "**El 9 % es provisional**" in tabla and "La prueba del 10 % es información, no condición." in tabla
             and s["firme"] == (len(set(zonas)) == 1) and (("Conclusión **firme" in tabla) == s["firme"]))
        # --- predicciones y fechas
        preds = t["predicciones"]
        paso(f"{nombre}: tres predicciones de Palancas A38:C40 (fase C) con fecha y probabilidad, iguales a las de la ficha",
             len(preds) == 3 and all(pr["texto"] == fase_c["celdas"][f"Palancas!A{38 + i}"] and pr["fecha"] == fase_c["celdas"][f"Palancas!B{38 + i}"]
                                     and pr["prob"] == fase_c["celdas"][f"Palancas!C{38 + i}"] and pr["texto"] == ficha["predicciones"][i]["texto"]
                                     and pr["fecha"] == ficha["predicciones"][i]["fecha"] and pr["prob"] == ficha["predicciones"][i]["prob"] for i, pr in enumerate(preds))
             and "Se comprueban en esta fecha con este dato" in md and all(H.fecha_larga(pr["fecha"]) in md and pr["texto"] in md for pr in preds))
        meta = json.load(open(os.path.join(exp, "fase1_metadatos.json"), encoding="utf-8"))
        paso(f"{nombre}: fechas por separado (análisis, datos base, precio, acciones, fuentes) y versión del personaje",
             all(re.search(rf"(?m)^- {r}[^:]*: ", md) for r in ("Análisis", "Datos base", "Precio", "Acciones", "Fuentes"))
             and H.fecha_larga(meta["precio"]["fecha"]) in md and H.fecha_larga(meta["acciones_diluidas"]["fecha"]) in md
             and f"Versión del personaje: {ficha['versiones']['personaje']}" in md)
        paso(f"{nombre}: la hoja no parece una auditoría (sin línea «Material auditado», H2 no la aprueba) ni tiene línea «Veredicto:»",
             not CIE.parece_auditoria(md, PIPE.Pipeline.veredicto_auditoria) and not re.search(r"(?im)^[\s>*#_-]*veredicto[\s*_]*:", md))
        paso(f"{nombre}: la huella de la ficha leída está en la hoja", t["entradas_sha256"]["ficha.json"] == H.sha256(os.path.join(exp, "ficha.json"))
             and t["entradas_sha256"]["ficha.json"][:16] in md)
        # --- vigencia: la ficha cambia después
        rc4, out4 = correr([exp, "--comprobar"])
        paso(f"{nombre}: --comprobar da la hoja por vigente (código 0)", rc4 == 0 and "VIGENTE" in out4, out4.strip()[-90:])
        fp = os.path.join(exp, "ficha.json")
        bytes_ficha = open(fp, "rb").read()
        open(fp, "wb").write(bytes_ficha + b"\n")
        rc5, out5 = correr([exp, "--comprobar"])
        paso(f"{nombre}: si la ficha cambia, --comprobar avisa de que la hoja está desactualizada (código 4)", rc5 == 4 and "DESACTUALIZADA" in out5 and "ficha.json" in out5,
             out5.strip()[-100:])
        if os.path.isfile(os.path.join(exp, "cierre_vigente.json")):
            rc6, out6 = correr([exp, "--trabajo", tmp])
            paso(f"{nombre}: con cierre_vigente.json, una ficha que no es la del cierre no genera hoja (código 3) y no toca la anterior",
                 rc6 == 3 and "cierre vigente" in out6 and json.load(open(js_p, encoding="utf-8"))["entradas_sha256"] == t["entradas_sha256"], out6.strip()[-120:])
        else:
            rc6, out6 = correr([exp, "--trabajo", tmp])
            t2 = json.load(open(js_p, encoding="utf-8"))
            paso(f"{nombre}: sin cierre_vigente.json, la hoja se regenera con aviso y guarda la huella nueva",
                 rc6 == 0 and "AVISO: la ficha cambió" in out6 and t2["entradas_sha256"]["ficha.json"] == H.sha256(fp)
                 and correr([exp, "--comprobar"])[0] == 0, out6.strip()[:120])
        open(fp, "wb").write(bytes_ficha)

    # --- expediente no cerrado o incoherente (sobre la copia de Hermès)
    exp = os.path.join(tmp, "Hermes")
    for f in (H.SALIDA_MD, H.SALIDA_JSON):
        os.remove(os.path.join(exp, f))
    stp = os.path.join(exp, "estado_pipeline.json")
    st_bytes = open(stp, "rb").read()
    st = json.loads(st_bytes)
    st["fin"] = None
    json.dump(st, open(stp, "w", encoding="utf-8"))
    rc7, out7 = correr([exp])
    paso("expediente sin terminar: no se genera hoja (código 3)", rc7 == 3 and not os.path.exists(os.path.join(exp, H.SALIDA_MD)), out7.strip()[-100:])
    open(stp, "wb").write(st_bytes)
    libro = H.libro_evaluado(exp)
    lb = open(libro, "rb").read()
    open(libro, "ab").write(b"\0")
    rc8, out8 = correr([exp])
    paso("libro evaluado distinto del de la ficha: no se genera hoja (código 3)", rc8 == 3 and "libro evaluado" in out8, out8.strip()[-100:])
    open(libro, "wb").write(lb)
    os.remove(os.path.join(exp, "fase_c.json"))
    rc9, out9 = correr([exp])
    paso("falta fase_c.json: no se genera hoja (código 3)", rc9 == 3 and "fase_c.json" in out9, out9.strip()[-100:])
finally:
    shutil.rmtree(tmp, ignore_errors=True)

paso("los expedientes originales del paquete no cambian", all(huellas_dir(p) == originales[n] for n, p in EXPEDIENTES.items()))

n = sum(ok for _, ok in RES)
print(f"{n}/{len(RES)} pruebas de la hoja resumen PASAN" if n == len(RES) else f"{n}/{len(RES)} pruebas de la hoja resumen: FALLAN {len(RES) - n}")
sys.exit(0 if n == len(RES) else 1)
