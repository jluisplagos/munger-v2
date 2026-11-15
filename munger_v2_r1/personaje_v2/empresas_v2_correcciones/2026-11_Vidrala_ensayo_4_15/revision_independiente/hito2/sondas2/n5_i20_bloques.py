#!/usr/bin/env python3
"""n5 · I20, H8, H9 y H2 (segunda pasada): la ficha y el informe con el bloque de las entradas (ficha.py e informe.py --provisional, como la
batería; sin pipeline ni LibreOffice).
A) V6.4.1 (fixture de la batería: Viscofan 4.13 con registro SINTÉTICO apto): con el modo aplicado ≠ declarado (o la declaración ilegible),
   ¿qué dice cada uno de los DOS bloques de aptitud (aptitud_de_uso de la 4.14 y verificacion_entradas de la 4.15)?
B) V6.3 (copia de elis_decisiones/Elis, registro real no apto): ¿qué queda en la ficha y el informe si se borra verificacion_entradas.json
   (y entrada_efectiva.json)? ¿Y con el modo aplicado ≠ declarado?
Uso: python3 -I -B n5_i20_bloques.py"""
import json, os, re, shutil, subprocess, sys, tempfile
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas"))
import fx5 as X
VE, PV = X.VE, X.PV
import cierre_v2 as CIE  # noqa: E402
print("código:", "estable" if hasattr(VE, "_apariciones_en_pagina") else "candidata (1.ª pasada)")
ENV641 = dict(os.environ, MUNGER_CONFIG=os.path.join(PV, "config_v2_v641_experimental.json"))


def salidas(d, env=None):
    r1 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "ficha.py"), d, "--provisional"], capture_output=True, text=True, env=env or dict(os.environ))
    r2 = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "informe.py"), d, "--provisional"], capture_output=True, text=True, env=env or dict(os.environ))
    fi = json.load(open(os.path.join(d, "ficha_provisional.json"), encoding="utf-8")) if os.path.exists(os.path.join(d, "ficha_provisional.json")) else {}
    inf = open(os.path.join(d, "informe_provisional.md"), encoding="utf-8").read() if os.path.exists(os.path.join(d, "informe_provisional.md")) else ""
    rv = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "validar_esquema.py"), os.path.join(d, "ficha_provisional.json"), "ficha"], capture_output=True, text=True)
    return fi, inf, (r1.returncode, r2.returncode, rv.returncode)


def bloques(inf):
    v64 = re.search(r"\*\*Verificación de las entradas financieras:\*\*[^\n]*", inf)
    i20 = re.search(r"\*\*Entradas financieras:\*\*[^\n]*", inf)
    return (v64.group(0) if v64 else None), (i20.group(0) if i20 else None)


def informe_dice(inf):
    b64, b20 = bloques(inf)
    f = lambda b: None if b is None else (re.findall(r"apta por entradas: (sí|no)", b), re.findall(r"Apta para dinero real: (sí|no)", b))  # noqa: E731
    return {"párrafo de aptitud V6.4": f(b64), "línea de las entradas (I20)": f(b20)}


def ficha_dice(fi):
    ve = fi.get("verificacion_entradas")
    au = fi.get("aptitud_de_uso") or {}
    return {"verificacion_entradas.apto_por_entradas": None if ve is None else ve.get("apto_por_entradas"),
            "verificacion_entradas.resumen.apto_por_entradas": None if ve is None else (ve.get("resumen") or {}).get("apto_por_entradas", "(sin clave)"),
            "verificacion_entradas.motivo_modo": None if ve is None else ve.get("motivo_modo"),
            "aptitud_de_uso.verificacion_entradas.apto_por_entradas": (au.get("verificacion_entradas") or {}).get("apto_por_entradas") if au else "(sin bloque aptitud_de_uso)",
            "aptitud_de_uso.motivos_no_apto": [m[:60] for m in au.get("motivos_no_apto") or []] if au else "(sin bloque aptitud_de_uso)"}


def estado_modo(d, modo):
    p = os.path.join(d, "estado_pipeline.json")
    st = json.load(open(p, encoding="utf-8"))
    st["entrada_efectiva"] = {"modo": modo, "declarado_en": None}
    json.dump(st, open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)


print("\n== A · V6.4.1 con el registro sintético APTO")
c = X.c
r = X.con()
print("   comprobar:", r["apto_por_entradas"], r["comprobadas_universo"], "/", r["universo"])
fi, inf, rcs = salidas(c, ENV641)
print("   A0 control (sin declaración del modo) · códigos", rcs, "· plantilla", (fi.get("versiones") or {}).get("plantilla"))
print("      ficha:", ficha_dice(fi))
print("      informe:", informe_dice(inf))
json.dump({"modo": "estricta", "fecha": "2026-11-15"}, open(os.path.join(c, "entrada_efectiva.json"), "w"))
estado_modo(c, "registrada")
fi, inf, rcs = salidas(c, ENV641)
print("   A1 modo aplicado en el paso 2 «registrada» ≠ declarado ahora «estricta» · códigos", rcs)
for k, v in ficha_dice(fi).items():
    print(f"      ficha · {k}: {v}")
d = informe_dice(inf)
print("      informe:", d)
dist = d["párrafo de aptitud V6.4"] and d["línea de las entradas (I20)"] and d["párrafo de aptitud V6.4"][0] != d["línea de las entradas (I20)"][0]
print("      ->", "LOS DOS BLOQUES DEL MISMO INFORME SE CONTRADICEN sobre «apta por entradas»" if dist else "los dos bloques dicen lo mismo")
open(os.path.join(c, "entrada_efectiva.json"), "w").write("{ilegible")
fi, inf, rcs = salidas(c, ENV641)
print("   A2 declaración del modo ilegible · códigos", rcs)
for k, v in ficha_dice(fi).items():
    print(f"      ficha · {k}: {v}")
d = informe_dice(inf)
print("      informe:", d)
dist = d["párrafo de aptitud V6.4"] and d["línea de las entradas (I20)"] and d["párrafo de aptitud V6.4"][0] != d["línea de las entradas (I20)"][0]
print("      ->", "LOS DOS BLOQUES DEL MISMO INFORME SE CONTRADICEN sobre «apta por entradas»" if dist else "los dos bloques dicen lo mismo")
os.remove(os.path.join(c, "entrada_efectiva.json"))

print("\n== B · V6.3 (copia de elis_decisiones/Elis, registro real)")
TMPB = tempfile.mkdtemp(prefix="rev2_n5_")
dB = os.path.join(TMPB, "Elis")
shutil.copytree(os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis"), dB,
                ignore=shutil.ignore_patterns(".lo_perfil", "recalc", "variantes_v64", "prompts_generados", "historial_cierres", "antecedentes", "__pycache__"))
st = json.load(open(os.path.join(dB, "estado_pipeline.json"), encoding="utf-8"))
print("   estado_pipeline.json: claves de la 4.14/4.15 presentes:", {k: (k in st) for k in ("verificacion_entradas", "entrada_efectiva")},
      "| verificacion_entradas.apto en el estado:", (st.get("verificacion_entradas") or {}).get("apto_por_entradas"))


def ver(rotulo):
    fi, inf, rcs = salidas(dB)
    mat = CIE.material(dB, "Elis")[0]
    b20 = bloques(inf)[1]
    print(f"   {rotulo}\n      códigos (ficha, informe, esquema) {rcs} · material {mat} · bloque en la ficha: {'verificacion_entradas' in fi}"
          f" · apto_por_entradas: {(fi.get('verificacion_entradas') or {}).get('apto_por_entradas')} · motivo_modo: {(fi.get('verificacion_entradas') or {}).get('motivo_modo')}"
          f"\n      informe: {'«apta por entradas» ' + str(re.findall(r'apta por entradas: (sí|no)', inf)) + ' · «Apta para dinero real» ' + str(re.findall(r'Apta para dinero real: (sí|no)', inf))}"
          f" · línea I20: {'sí' if b20 else 'NO HAY'}" + (f" · «{b20[-150:]}»" if b20 else ""))
    return fi, inf


ver("B0 tal cual (con su registro, sin declaración del modo)")
shutil.move(os.path.join(dB, "verificacion_entradas.json"), os.path.join(TMPB, "verificacion_entradas.json.fuera"))
ver("B1 se borra verificacion_entradas.json (no hay entrada_efectiva.json)")
json.dump({"modo": "estricta", "fecha": "2026-11-15"}, open(os.path.join(dB, "entrada_efectiva.json"), "w"))
ver("B2 sin registro, con entrada_efectiva.json «estricta» (como un expediente que prepara cambiar_base.py)")
estado_modo(dB, "registrada")
shutil.copy(os.path.join(TMPB, "verificacion_entradas.json.fuera"), os.path.join(dB, "verificacion_entradas.json"))
ver("B3 con registro, modo aplicado «registrada» ≠ declarado «estricta»")
os.remove(os.path.join(dB, "verificacion_entradas.json"))
os.remove(os.path.join(dB, "entrada_efectiva.json"))
ver("B4 lo mismo, borrando los dos archivos (el estado sigue diciendo que el paso 2 aplicó «registrada»)")
# el modo declarado en alcance_v2.json (forma del hito 1 de la 4.15), sin registro ni entrada_efectiva.json
json.dump({"tipo": "ensayo_exploratorio", "aviso": "(prueba) ensayo", "fuente": "(prueba)", "entrada_efectiva": "estricta"}, open(os.path.join(dB, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False)
print("      modo declarado según pipeline.modo_entrada_efectiva:", __import__("pipeline").modo_entrada_efectiva(dB))
ver("B5 sin registro ni entrada_efectiva.json, con el modo «estricta» declarado en alcance_v2.json (forma del hito 1 de la 4.15)")
os.remove(os.path.join(dB, "alcance_v2.json"))
# T5: fase1_metadatos.json registra el modo y entrada_efectiva.json se ha borrado (pipeline.modo_entrada_efectiva falla en cerrado)
mp = os.path.join(dB, "fase1_metadatos.json")
meta = json.load(open(mp, encoding="utf-8")) if os.path.exists(mp) else {}
meta["entrada_efectiva"] = "estricta"
json.dump(meta, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
try:
    print("      modo declarado según pipeline.modo_entrada_efectiva:", __import__("pipeline").modo_entrada_efectiva(dB))
except ValueError as ex:
    print("      pipeline.modo_entrada_efectiva: ERROR ·", ex)
ver("B6 fase1_metadatos.json registra «estricta», entrada_efectiva.json borrado y sin registro (declaración con error, T5)")
shutil.copy(os.path.join(TMPB, "verificacion_entradas.json.fuera"), os.path.join(dB, "verificacion_entradas.json"))
ver("B7 lo mismo con el registro presente (control: el error de la declaración sí se ve)")
shutil.rmtree(TMPB, ignore_errors=True)
X.limpiar()
