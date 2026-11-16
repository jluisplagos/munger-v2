#!/usr/bin/env python3
"""x5b · octava comprobación · X5 sobre DATOS REALES (solo lectura del árbol congelado; nada se escribe en él).
 A. todos los expedientes del árbol con fase1_partes/: `comprobar_anio` con el código anterior (45ff57c) y con el nuevo (0a0020b), año a
    año: mismos errores y mismos ceros pendientes; componente a componente, `importe_completo` en la línea y en la página con los dos códigos;
 B. todos los textos conservados (texto/*.txt) del árbol, sin repetir contenidos: ¿hay «cifra + apóstrofo + cifra» (ASCII, «’» u otros
    signos parecidos)?; y los `impreso` y `linea` de todas las extracciones: ¿llevan apóstrofo pegado a una cifra?;
 C. los `calculo` declarados reales (C48 de Elis, cambio_elis_c48_4_15.json): sus citas, y `calcular_entrada` con la carpeta de
    elis_decisiones con el código del árbol (contrasta cada componente con su página): el valor reconstruido.
Uso: python3 -I -B x5b_reales.py"""
import collections, glob, hashlib, json, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun8 import FN, FO, CONGELADO, PV, cargar  # noqa: E402

ok_todo = True


def dicho(ok, t):
    global ok_todo
    ok_todo = ok_todo and bool(ok)
    print(("   CONFORME     " if ok else "   NO CONFORME  ") + t)


PVC = os.path.join(CONGELADO, "personaje_v2")
print("A · comprobar_anio y componentes, anterior frente a nuevo")
dirs = sorted(os.path.dirname(d) for d in glob.glob(os.path.join(PVC, "**", "fase1_partes"), recursive=True))
tot = collections.Counter()
dif_err, dif_comp = [], []
por_exp = []
for c in dirs:
    anios = sorted(int(re.search(r"AR_(\d+)\.json$", f).group(1)) for f in glob.glob(os.path.join(c, "fase1_partes", "AR_*.json")) if re.search(r"AR_(\d+)\.json$", f))
    con_texto = os.path.isdir(os.path.join(c, "texto"))
    n_err = n_comp = n_ok = 0
    for a in anios:
        po, pn = [], []
        eo, en = FO.comprobar_anio(c, a, po), FN.comprobar_anio(c, a, pn)
        tot["años"] += 1
        tot["años sin errores (nuevo)"] += not en
        n_err += len(en)
        if eo != en or po != pn:
            dif_err.append((os.path.relpath(c, PVC), a, [x for x in en if x not in eo][:3], [x for x in eo if x not in en][:3]))
        d = json.load(open(os.path.join(c, "fase1_partes", f"AR_{a}.json"), encoding="utf-8"))
        arch = d.get("archivo")
        if not arch or not os.path.exists(os.path.join(c, "texto", arch)):
            tot["años sin texto conservado"] += 1
            P = None
        else:
            P = {k: FN.norm(v) for k, v in FN.paginas(os.path.join(c, "texto", arch)).items()}
        for k, p in (d.get("partidas") or {}).items():
            if not isinstance(p, dict):
                continue
            for cual in ("actual", "anterior"):
                for comp in FN.componentes(p.get(cual)):
                    imp, pg, lin = comp.get("impreso"), comp.get("pagina"), comp.get("linea")
                    tot["componentes"] += 1
                    n_comp += 1
                    if imp is None or not lin:
                        tot["componentes sin impreso o sin línea"] += 1
                        continue
                    lo, ln = FO.importe_completo(FO.norm(imp), FO.norm(lin)), FN.importe_completo(FN.norm(imp), FN.norm(lin))
                    tot["en su línea: completo (anterior)"] += lo
                    tot["en su línea: completo (nuevo)"] += ln
                    if lo != ln:
                        dif_comp.append((os.path.relpath(c, PVC), a, k, cual, "línea", imp, lin[:80]))
                    if re.search(r"\d['’ʼ′´`‘]|['’ʼ′´`‘]\d", str(imp)):
                        tot["impresos con apóstrofo pegado a cifra"] += 1
                    if re.search(r"\d['’ʼ′´`‘]\d", FN.norm(lin)):
                        tot["líneas con cifra+apóstrofo+cifra"] += 1
                    if re.search(r"['’]", str(lin)):
                        tot["líneas con algún apóstrofo (ASCII o ’)"] += 1
                    if P is not None and isinstance(pg, int) and pg in P:
                        tot["componentes con página examinable"] += 1
                        go, gn = FO.importe_completo(FO.norm(imp), P[pg]), FN.importe_completo(FN.norm(imp), P[pg])
                        tot["en su página: completo (anterior)"] += go
                        tot["en su página: completo (nuevo)"] += gn
                        n_ok += ln and gn and FN.norm(lin) in P[pg]
                        if go != gn:
                            dif_comp.append((os.path.relpath(c, PVC), a, k, cual, "página", imp, pg))
    por_exp.append((os.path.relpath(c, PVC), len(anios), "con texto" if con_texto else "SIN texto/", n_comp, n_ok, n_err))
print(f"   expedientes con fase1_partes/: {len(dirs)} ({sum(1 for x in por_exp if x[2] == 'con texto')} con texto/ conservado)")
for e in por_exp:
    print(f"     {e[0][:98]:98} {e[1]:2} años · {e[2]:10} · {e[3]:4} componentes · {e[4]:4} conformes (línea, página e importe) · {e[5]:3} errores de comprobar_anio (nuevo)")
for k in sorted(tot):
    print(f"   {k}: {tot[k]:,}")
dicho(not dif_err, f"comprobar_anio da los mismos errores y los mismos ceros pendientes con los dos códigos en los {tot['años']} años" + (f" · DIFIEREN: {dif_err[:5]}" if dif_err else ""))
dicho(not dif_comp, f"importe_completo da lo mismo con los dos códigos en todos los componentes (línea y página)" + (f" · DIFIEREN {len(dif_comp)}: {dif_comp[:5]}" if dif_comp else ""))

print("\nB · «cifra + apóstrofo + cifra» en los textos conservados y en las extracciones")
vistos, n_arch = {}, 0
pat = {"ASCII '": re.compile(r"\d'\d"), "tipográfico ’": re.compile(r"\d’\d"), "otros (ʼ ′ ´ ` ‘)": re.compile(r"\d[ʼ′´`‘]\d")}
pegado = re.compile(r"\d['’]|['’]\d")
cuenta, ejemplos, n_pegado, ej_pegado = collections.Counter(), collections.defaultdict(list), 0, collections.Counter()
for f in sorted(glob.glob(os.path.join(PVC, "**", "texto", "*.txt"), recursive=True)):
    n_arch += 1
    b = open(f, "rb").read()
    h = hashlib.sha256(b).hexdigest()
    if h in vistos:
        continue
    vistos[h] = f
    t = b.decode("utf-8", errors="replace")
    for nombre, rx in pat.items():
        for m in rx.finditer(t):
            cuenta[nombre] += 1
            if len(ejemplos[nombre]) < 12:
                ejemplos[nombre].append((os.path.basename(f)[:40], t[max(0, m.start() - 25): m.end() + 25].replace("\n", "⏎")))
    for m in pegado.finditer(t):
        n_pegado += 1
        ctx = t[max(0, m.start() - 6): m.end() + 3].replace("\n", "⏎")
        forma = re.sub(r"\d", "9", re.sub(r"[^\W\d_]", "a", t[max(0, m.start() - 1): m.end() + 1]))
        ej_pegado[forma] += 1
print(f"   archivos texto/*.txt en el árbol: {n_arch} · contenidos distintos: {len(vistos)}")
for nombre in pat:
    print(f"   cifra + {nombre} + cifra: {cuenta[nombre]}" + ("".join(f"\n       {e[0]}: «{e[1]}»" for e in ejemplos[nombre]) if ejemplos[nombre] else ""))
print(f"   apóstrofos (ASCII o ’) pegados a una cifra por algún lado: {n_pegado} · formas (9 = cifra, a = letra): {dict(ej_pegado.most_common(12))}")
print("   (si hay «cifra + apóstrofo + cifra» en un texto, solo afectaría a un componente cuyo impreso fuese un trozo de ese número: parte A)")

print("\nC · cálculos declarados reales (C48 de Elis)")
CAMBIO = os.path.join(PVC, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "configuracion", "cambio_elis_c48_4_15.json")
ELIS = os.path.join(PVC, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis")
cal = json.load(open(CAMBIO, encoding="utf-8"))["analisis"]["C48"]["calculo"]
n_c = n_apo = 0
for nombre, serie in (cal.get("componentes") or {}).items():
    for anio, cmp in sorted(serie.items()):
        n_c += 1
        cita = str(cmp.get("cita"))
        apo = bool(re.search(r"\d['’ʼ′´`‘]\d", cita))
        n_apo += apo
        print(f"     {nombre} {anio}: valor {cmp.get('valor')!r} · valor_fuente {cmp.get('valor_fuente')!r} · {cmp.get('fuente')} p.{cmp.get('pagina')} · cita «{cita[:70]}»" + (" · CON cifra+apóstrofo+cifra" if apo else ""))
dicho(n_apo == 0, f"componentes del cálculo: {n_c} · con «cifra + apóstrofo + cifra» en la cita: {n_apo}")
f1 = json.load(open(os.path.join(ELIS, "fase1_v63.json"), encoding="utf-8"))
H, anios = f1["historia"]["partidas"], f1["historia"]["anios"]
VE = cargar(os.path.join(PV, "scripts", "verificacion_entradas.py"), "verificacion_entradas", os.path.join(PV, "scripts"))
sys.modules["verificacion_entradas"] = VE   # calcular_entrada lo importa al ejecutarse: el del árbol (4b00aa2a…)
assert hashlib.sha256(open(VE.__file__, "rb").read()).hexdigest().startswith("4b00aa2a")
try:
    r = FN.calcular_entrada("C48", {"calculo": cal}, H, anios, carpeta=ELIS)
    dicho(r["valor"] == 108.0, f"calcular_entrada(C48) con la carpeta de elis_decisiones y el código del árbol: valor {r['valor']!r} (sin redondear {r['valor_sin_redondear']!r}); cada componente, contrastado con su página")
except Exception as ex:  # noqa: BLE001
    dicho(False, f"calcular_entrada(C48) con el código del árbol da error: {ex}")
print("\nRESULTADO:", "CONFORME" if ok_todo else "NO CONFORME")
sys.exit(0 if ok_todo else 1)
