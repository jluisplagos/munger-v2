"""Sondas I13 (vínculo, sellar, huella) de extremo a extremo (arnés fx.py; copia en /tmp)."""
import copy, hashlib, json, os, shutil, subprocess, sys, unicodedata
import fx
from fx import VE, con, ent, con_k, resumen, K, REG, c, FS, nueva_pagina, PV

def caso(nombre, r, k=K):
    print(f"[{nombre}] {resumen(r, k)}")

r = con(); caso("control positivo", r)
k_hip = next(e["celda"] for e in REG["entradas"] if e["clase"] == "hipotesis")
print("evidencia_libro de K:", json.dumps(fx.EVID.get(K), ensure_ascii=False)[:400])
print("evidencia_libro de", k_hip, ":", json.dumps(fx.EVID.get(k_hip), ensure_ascii=False)[:400])
print("celdas del universo sin fila de evidencia en el Control maestro:", sum(1 for k in fx.inst["celdas"] if k not in fx.EVID), "de", fx.inst["n"],
      "| ejemplos:", [k for k in fx.inst["celdas"] if k not in fx.EVID][:8])

print("\n=== D1 · sellar con fecha retroactiva legitima en bloque una revisión antigua")
cs = os.path.join(fx.TMP, "sellar_retro", "Viscofan"); shutil.copytree(c, cs)
reg = copy.deepcopy(REG); reg["formato"] = "4.14"
for e in reg["entradas"]:
    e["comprobacion"].pop("vinculo", None); e["comprobacion"]["fecha"] = "2026-11-14"   # revisión «antigua» de la 4.14
# después de aquella revisión cambian el fundamento de una hipótesis y la evidencia (documento, concepto, tratamiento) de un dato, con el mismo número
ent(reg, k_hip)["hipotesis"]["fundamento"] = "(prueba) fundamento NUEVO, escrito después de la revisión del 14-nov"
ent(reg, K)["fuente"].update(documento="(prueba) OTRO documento", concepto="(prueba) otro concepto", tratamiento="(prueba) otra transformación")
json.dump(reg, open(os.path.join(cs, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
r0 = VE.comprobar(cs); print("antes de sellar:", resumen(r0))
celdas = [e["celda"] for e in reg["entradas"]]
p = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "verificacion_entradas.py"), "sellar", cs, "--revisor", "revisor sintético", "--fecha", "2026-11-14", *celdas], capture_output=True, text=True)
print("CLI sellar (una sola orden, %d celdas, --fecha 2026-11-14):" % len(celdas), p.stdout.strip().splitlines()[:3], "rc", p.returncode)
r1 = VE.comprobar(cs); print("después de sellar:", resumen(r1))
print("   K:", con_k(r1, K) or "comprobada", "|", k_hip, ":", con_k(r1, k_hip) or "comprobada")

print("\n=== D2 · vínculo escrito a mano (sin `sellar`)")
reg2 = copy.deepcopy(reg)
evid = VE.evidencia_libro(cs)
for e in reg2["entradas"]:
    e["comprobacion"]["vinculo"] = {"huella": VE.huella_fundamento(e, evid.get(e["celda"]))}
json.dump(reg2, open(os.path.join(cs, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("vínculo = {'huella': huella_fundamento(...)} en las %d entradas, sin sellado_por ni fecha:" % len(reg2["entradas"]), resumen(VE.comprobar(cs)))

print("\n=== D3 · cambios posteriores al sello que no lo invalidan")
r = con(lambda g: ent(g, K)["comprobacion"].update(revisor="otro revisor cualquiera", fecha="2019-01-01", fuente_examinada="ninguna en particular", nota="cambiada")); caso("revisor, fecha, fuente examinada y nota de la comprobación cambiados DESPUÉS del sello", r)
r = con(lambda g: ent(g, K).update(incidencia=None, uso="otro uso", id="otro_id")); caso("incidencia, uso e id cambiados después del sello", r)
r = con(lambda g: ent(g, K)["comprobacion"]["vinculo"].update(sellado_por="nadie", fecha="1999-01-01")); caso("vinculo.sellado_por y vinculo.fecha cambiados (la huella es la misma)", r)

print("\n=== D4 · derivado cuyo origen cambia de fundamento")
k_der = next(e["celda"] for e in REG["entradas"] if e["clase"] == "dato_publicado" and e["celda"].startswith("Historia!") and isinstance(e["valor_modelo"], (int, float)) and e["valor_modelo"] > 0 and e["celda"] != K)
vm = fx.inst["celdas"][k_der]
p1 = nueva_pagina(f"Parte A de {k_der}: {vm * 0.6 * 1000:.3f}"); p2 = nueva_pagina(f"Parte B de {k_der}: {vm * 0.4 * 1000:.3f}")
p1b = nueva_pagina(f"OTRA partida de OTRO documento (nada que ver): {vm * 0.6 * 1000:.3f}")
def aux(nombre, pag, cita, v, **extra):
    f = dict(ent(REG, K)["fuente"], pagina=pag, cita=cita, valor_fuente=round(v * 1000, 6), concepto=f"concepto de {nombre}", columna="31-dic-2025", periodo="31-dic-2025"); f.update(extra)
    return {"celda": nombre, "id": nombre, "ambito": "auxiliar", "uso": "origen", "material": True, "clase": "dato_publicado", "valor_modelo": v, "comprobacion": dict(fx.COMPROBADA), "incidencia": None, "fuente": f}
def derivar(g, cambio_origen=False, resellar_solo_origen=False):
    e = ent(g, k_der); e.pop("fuente", None)
    e.update(clase="derivado", derivacion={"origenes": ["aux:a", "aux:b"], "formula": 'o["aux:a"] + o["aux:b"]', "conciliacion": "suma de las dos partes publicadas"})
    g["entradas"].append(aux("aux:a", p1, f"Parte A de {k_der}: {vm * 0.6 * 1000:.3f}", vm * 0.6))
    g["entradas"].append(aux("aux:b", p2, f"Parte B de {k_der}: {vm * 0.4 * 1000:.3f}", vm * 0.4))
    fx.sellar_todo(g)   # revisión completa: derivado y orígenes sellados
    if cambio_origen:
        ent(g, "aux:a")["fuente"].update(pagina=p1b, cita=f"OTRA partida de OTRO documento (nada que ver): {vm * 0.6 * 1000:.3f}", documento="OTRO documento", concepto="OTRO concepto", tratamiento="otra transformación")
        if resellar_solo_origen:
            ev = VE.evidencia_libro(c)
            ent(g, "aux:a")["comprobacion"]["vinculo"] = {"huella": VE.huella_fundamento(ent(g, "aux:a"), ev.get("aux:a"))}
r = con(lambda g: derivar(g)); caso("derivado con sus dos orígenes, todo sellado", r, k_der)
r = con(lambda g: derivar(g, cambio_origen=True)); caso("el origen aux:a cambia de documento, concepto, página y cita (mismo número), sin nueva revisión", r, k_der); print("   aux:a:", con_k(r, "aux:a"))
r = con(lambda g: derivar(g, cambio_origen=True, resellar_solo_origen=True)); caso("se revisa y se sella de nuevo SOLO el origen: el derivado, sin revisar, vuelve a valer", r, k_der); print("   aux:a:", con_k(r, "aux:a") or "comprobada")
print("\n=== D5 · estabilidad de la huella")
e = copy.deepcopy(ent(REG, K)); h0 = VE.huella_fundamento(e, fx.EVID.get(K))
e2 = json.loads(json.dumps(e, ensure_ascii=True, sort_keys=False)); print("ida y vuelta por JSON (ensure_ascii, otro orden de claves):", VE.huella_fundamento(dict(reversed(list(e2.items()))), fx.EVID.get(K)) == h0)
e3 = copy.deepcopy(e); e3["fuente"] = dict(reversed(list(e3["fuente"].items()))); print("orden de claves de «fuente» invertido:", VE.huella_fundamento(e3, fx.EVID.get(K)) == h0)
e4 = copy.deepcopy(e); e4["fuente"]["valor_fuente"] = int(e4["fuente"]["valor_fuente"]); print(f"valor_fuente {e['fuente']['valor_fuente']!r} → {e4['fuente']['valor_fuente']!r} (entero en vez de decimal, mismo número):", VE.huella_fundamento(e4, fx.EVID.get(K)) == h0)
e5 = copy.deepcopy(e); e5["fuente"]["escala"] = 1e-3; print("escala 0.001 → 1e-3:", VE.huella_fundamento(e5, fx.EVID.get(K)) == h0)
e6 = copy.deepcopy(e); e6["fuente"]["documento"] = unicodedata.normalize("NFD", e6["fuente"]["documento"]); print("mismo texto en NFD en vez de NFC:", VE.huella_fundamento(e6, fx.EVID.get(K)) == h0)
e7 = copy.deepcopy(e); e7["fuente"]["cita"] = e7["fuente"]["cita"] + " "; print("un espacio final en la cita:", VE.huella_fundamento(e7, fx.EVID.get(K)) == h0)
e8 = copy.deepcopy(e); e8["fuente"]["pagina"] = int(e8["fuente"]["pagina"]); print("página '22' → 22:", VE.huella_fundamento(e8, fx.EVID.get(K)) == h0)
r = con(lambda g: ent(g, K)["fuente"].update(valor_fuente=int(ent(g, K)["fuente"]["valor_fuente"]))); caso("registro reescrito con 849697 en vez de 849697.0 (mismo número), sin resellar", r)

print("\n=== D9 · sellar fallido cambia el formato del registro")
cf = os.path.join(fx.TMP, "sellar_formato", "Viscofan"); shutil.copytree(c, cf)
reg = copy.deepcopy(REG); reg["formato"] = "4.14"
for e in reg["entradas"]:
    e["comprobacion"].pop("vinculo", None)
json.dump(reg, open(os.path.join(cf, VE.REGISTRO), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
sha_a = hashlib.sha256(open(os.path.join(cf, VE.REGISTRO), "rb").read()).hexdigest()
ok, mal = VE.sellar(cf, [K], "revisor que no es", "2026-11-15")
sha_b = hashlib.sha256(open(os.path.join(cf, VE.REGISTRO), "rb").read()).hexdigest()
print("sellar rechazado:", ok, mal[:1], "| formato ahora:", json.load(open(os.path.join(cf, VE.REGISTRO), encoding="utf-8"))["formato"], "| el archivo cambió:", sha_a != sha_b)
fx.limpiar()
