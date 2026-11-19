#!/usr/bin/env python3
"""Pruebas de las entradas declaradas que dependen de una celda de juicio (entradas_dependientes.py y el paso 9 del pipeline; examen, Jumbo,
decisión J1: Análisis!C46 y C40 con la caja sobrante Análisis!C76, que escribe la fase B).

Antes del cambio, cuando la fase B elegía otro C76, C46 y C40 seguían calculados con el anterior: su derivación registrada no reproducía
el libro (discrepancia en verificacion_entradas.py) y repetir el expediente no convergía (jumbo_e 200 → 160, jumbo_g 160 → 150). Ahora la
dependencia se declara en el registro («derivacion.recalculo») y el pipeline la recalcula en el paso 9, tras escribir la fase B y antes del
recálculo del libro y de la fase C.
Casos: 1) tipo Jumbo sintético sobre la plantilla V6.3.1 F1 (C46 y C40 declarados con C76 = 200; la fase B escribe 150): valores, precisión
U2, registro coherente, vía generativa, partida F1-K3a, notas del Control maestro, rastro y material auditado; 2) idempotencia; 3) sin
declaración no cambia nada; 4) declaraciones mal formadas o copias distintas: se detiene sin escribir nada; 5) precisión U2; 6) el paso 9
del pipeline (orden: fase B → comprobar_celdas → recálculo dependiente → comprobar_celdas → recálculo del libro), sin LibreOffice; 7)
entradas de la fase C; 8) concordancia de cambiar_base.py; 9) jumbo_g real (copia temporal de su estado con la fase B escrita y sin
consumir; si sus libros no están o el expediente ya no está en ese estado, se omite y lo dice): el paso 9 de verdad.
No escribe en el repositorio: trabaja sobre copias temporales (en /dev/shm si existe). Sin LibreOffice.
Uso: python3 -B pruebas/test_entradas_dependientes.py      (código 0 si todo pasa; MUNGER_JUMBO_G=<carpeta jumbo_g> para usar otra copia)
"""
import contextlib
import hashlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
SCRIPTS = os.path.join(PV, "scripts")
sys.path.insert(0, SCRIPTS)
CFG = os.path.join(PV, "config_v2_v631_f1.json")
os.environ["MUNGER_CONFIG"] = CFG  # como lo fija el pipeline para los programas que lanza
import cierre_v2 as CIE  # noqa: E402
import config_v2  # noqa: E402
import verificacion_entradas as VE  # noqa: E402
from v63_xml import LibroV63  # noqa: E402

try:
    import entradas_dependientes as ED  # noqa: E402
except ImportError as ex:  # antes del cambio no existe: las pruebas fallan, no se interrumpen
    ED, ERROR_ED = None, ex
PY = sys.executable
JUMBO_G = os.environ.get("MUNGER_JUMBO_G") or os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "jumbo_g")
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def intento(nombre, f):
    """f() → (ok, detalle). Una excepción (p. ej. sin el módulo, antes del cambio) es un fallo de la prueba, no una interrupción."""
    try:
        ok, det = f()
    except Exception as ex:  # noqa: BLE001
        paso(nombre, False, f"{type(ex).__name__}: {str(ex)[:300]}")
        return
    paso(nombre, ok, det)


def huellas(d):
    out = {}
    for r, ds, fs in os.walk(d):
        ds[:] = [x for x in ds if x not in (".lo_perfil", "__pycache__")]
        for f in fs:
            p = os.path.join(r, f)
            out[os.path.relpath(p, d)] = hashlib.sha256(open(p, "rb").read()).hexdigest()
    return out


def redondeo(x, n):
    """ROUND de la hoja (mitad lejos de cero), exacto; propio de la prueba (no usa el del programa)."""
    q = Fr(10) ** n
    y = abs(x) * q
    e = int(y)
    if y - e >= Fr(1, 2):
        e += 1
    return (e if x >= 0 else -e) / q


def F(x):
    return Fr(repr(x)) if isinstance(x, float) else Fr(x)


# ------------------------------------------------------------------------------------------------ caso tipo Jumbo (cifras de jumbo_g)
E = "EmpresaJ"
A = (2023, 2024, 2025)
CFO = {2023: 323.918862, 2024: 300.687098, 2025: 296.912917}
DIV = {2023: 0.133043, 2024: 0.828384, 2025: 1.8762}
INT = {2023: 18.490712, 2024: 13.791382, 2025: 9.91679}
CUP = {2023: 0.595837, 2024: 0.594641, 2025: 0.595058}
CAJA = {2023: 434.000394, 2024: 444.815962, 2025: 536.668758}
HIST = {"L11": 296.9129, "L12": 38.384, "L16": 2.3258, "L17": 9.7272}  # Historia 2025: CFO, capex, intereses y principal de arrendamientos
IMPORTE_K3A = 9.302  # 316,475 − media de la fila 11 (307,173): la partida F1-K3a del valor declarado con C76 = 200


def esperado_c46(c76):
    s = F(c76) * 3 / sum(F(CAJA[y]) for y in A)
    return sum(F(CFO[y]) + F(DIV[y]) + F(INT[y]) - s * (F(INT[y]) - F(CUP[y])) for y in A) / 3


def esperado_c40(c76):
    caja_media = redondeo(sum(F(CAJA[y]) for y in A) / 3, 4)
    return (F(HIST["L11"]) - F(HIST["L12"]) - F(HIST["L16"]) - F(HIST["L17"]) + F(DIV[2025]) + F(INT[2025])
            - F(c76) / caja_media * (F(INT[2025]) - F(CUP[2025])))


def formula_c46():
    caja = "(" + "+".join(f'o["aux:caja_{y}"]' for y in A) + ")"
    t = "+".join(f'(o["aux:cfo_{y}"]+o["aux:div_{y}"]+o["aux:int_{y}"]-o["Análisis!C76"]*3/{caja}*(o["aux:int_{y}"]-o["aux:cup_{y}"]))' for y in A)
    return f"({t})/3"


def formula_c40():
    caja = "+".join(f'o["aux:caja_{y}"]' for y in A)
    return ('o["Historia!L11"]-o["Historia!L12"]-o["Historia!L16"]-o["Historia!L17"]+o["aux:div_2025"]+o["aux:int_2025"]'
            f'-o["Análisis!C76"]/round(({caja})/3, 4)*(o["aux:int_2025"]-o["aux:cup_2025"])')


def origenes_c46():
    return [f"aux:{n}_{y}" for n in ("cfo", "div", "int", "cup", "caja") for y in A] + ["Análisis!C76"]


def origenes_c40():
    return ["Historia!L11", "Historia!L12", "Historia!L16", "Historia!L17", "aux:div_2025", "aux:int_2025", "aux:cup_2025"] + \
        [f"aux:caja_{y}" for y in A] + ["Análisis!C76"]


V46_200, V40_200 = float(redondeo(esperado_c46(200), 3)), float(redondeo(esperado_c40(200), 3))
V46_150, V40_150 = float(redondeo(esperado_c46(150), 3)), float(redondeo(esperado_c40(150), 3))
VACIA = "vacía"  # la fase B deja vacía la celda de juicio
RECALCULO_C46 = {"celdas_de_juicio": ["Análisis!C76"], "regla": "J1 (sintética en la prueba): los intereses de la caja sumada en C76 no entran",
                 "conciliacion_f1": True}
RECALCULO_C40 = {"celdas_de_juicio": ["Análisis!C76"], "regla": "J1 (sintética en la prueba): los intereses de la caja sumada en C76 no entran"}


def registro(declarar=True):
    ents = []
    for n, serie in (("cfo", CFO), ("div", DIV), ("int", INT), ("cup", CUP), ("caja", CAJA)):
        for y in A:
            ents.append({"celda": f"aux:{n}_{y}", "id": f"{n}_{y}", "ambito": "calculo", "material": True, "clase": "dato_publicado", "valor_modelo": serie[y],
                         "fuente": {"documento": f"informe anual {y} (sintético)", "pagina": 1}, "comprobacion": {"resultado": "pendiente"}})
    d46 = {"origenes": origenes_c46(), "formula": formula_c46(), "conciliacion": "J1 con C76 = 200 (sintética)", "unidad": "millones de euros"}
    d40 = {"origenes": origenes_c40(), "formula": formula_c40(), "conciliacion": "J1 con C76 = 200 (sintética)", "unidad": "millones de euros"}
    if declarar:
        d46["recalculo"], d40["recalculo"] = json.loads(json.dumps(RECALCULO_C46)), json.loads(json.dumps(RECALCULO_C40))
    ents += [{"celda": "Análisis!C46", "id": "cfo_media", "ambito": "calculo", "material": True, "clase": "derivado", "valor_modelo": V46_200,
              "derivacion": d46, "comprobacion": {"extractor": "extractor", "revisor": None, "resultado": "pendiente"}},
             {"celda": "Análisis!C40", "id": "juicio_C40", "ambito": "juicio", "material": True, "clase": "derivado", "valor_modelo": V40_200,
              "derivacion": d40, "comprobacion": {"extractor": "extractor", "revisor": None, "resultado": "pendiente"}},
             {"celda": "Análisis!C76", "id": "exceso_caja", "ambito": "calculo", "material": True, "clase": "hipotesis", "valor_modelo": 200,
              "hipotesis": {"fundamento": "caja sobrante (sintética)", "alternativas": "0", "limites": "120–220"}, "comprobacion": {"resultado": "pendiente"}}]
    return {"formato": "4.15", "empresa": E, "entradas": ents}


def construir(nombre, declarar=True, c76_tras_fase_b=150):
    """Ensayo sintético <BASE>/<nombre>/<E>: libros de la plantilla V6.3.1 F1 con C46/C40 calculados con C76 = 200 y, en el evaluado, la
    celda de juicio que escribió la fase B (None: la fase B todavía no está escrita)."""
    cfg = config_v2.cargar(CFG)
    ens = os.path.join(BASE, nombre)
    c = os.path.join(ens, E)
    os.makedirs(c)
    lb = LibroV63(cfg["plantilla"]["archivo"])
    for k, v in HIST.items():
        lb.escribir("Historia", k, v)
    for ref, v in (("C46", V46_200), ("C40", V40_200), ("C76", 200)):
        lb.escribir("Análisis", ref, v)
    lb.escribir("Control maestro", "N43", "C46 = media 2023–2025 con J1 y C76 = 200 (preparación sintética).")
    lb.escribir("Control maestro", "N40", "C40 = FCF 2025 con J1 y C76 = 200 (preparación sintética).")
    for h in ("Historia", "Análisis", "Control maestro"):
        lb.marcar_modificada(h)
    lb.borrar_caches()
    lb.guardar(os.path.join(c, f"{E}_v63_datos.xlsx"))
    if c76_tras_fase_b is None:
        shutil.copy(os.path.join(c, f"{E}_v63_datos.xlsx"), os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    else:
        lb = LibroV63(os.path.join(c, f"{E}_v63_datos.xlsx"))
        lb.escribir("Análisis", "C76", None if c76_tras_fase_b == VACIA else c76_tras_fase_b)
        lb.marcar_modificada("Análisis")
        lb.guardar(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    an = {"C46": {"valor": V46_200, "fuente": "J1 con C76 = 200 (sintética)", "pagina": None, "periodo": "2023–2025", "unidad": "mm"},
          "C40": {"valor": V40_200, "fuente": "J1 con C76 = 200 (sintética)", "pagina": None, "periodo": "ejercicio 2025", "unidad": "mm"}}
    for n, d in (("fase1_v63.json", {"empresa": E, "analisis": an}), ("fase1_metadatos.json", {"empresa": E, "analisis": json.loads(json.dumps(an))}),
                 (VE.REGISTRO, registro(declarar)),
                 ("motor_a_f1.json", {"formato": "sintético", "conciliacion_fcf_base": [
                     {"componente": "C46", "importe": IMPORTE_K3A, "partida": "dividendos e intereses que no son de la caja de C76 (C76 = 200)",
                      "fuente": {"documento": "sintético", "pagina": "1"}}]}),
                 ("fase_b.json", {"celdas": {"C76": c76_tras_fase_b if isinstance(c76_tras_fase_b, int) else 150}})):
        open(os.path.join(c, n), "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    return c


def leer(c, n, k):
    return LibroV63(os.path.join(c, n)).leer(*k.split("!"))


def editar_registro(c, f):
    p = os.path.join(c, VE.REGISTRO)
    d = json.load(open(p, encoding="utf-8"))
    f({e["celda"]: e for e in d["entradas"]}, d)
    open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))


def coherente(c, k):
    """La fórmula registrada, con la celda de juicio del libro, da el valor del libro (regla U2) y valor_modelo es el del libro."""
    reg, _ = VE.cargar(c)
    por = {e["celda"]: e for e in reg["entradas"]}
    lb = LibroV63(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    d = por[k]["derivacion"]
    vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else lb.leer(*o.split("!"))) for o in d["origenes"]}
    ex = VE._eval_formula_exacta(d["formula"], vals)
    vm = lb.leer(*k.split("!"))
    return VE._importe_libro_exacto(ex, vm) and VE._igual_exacto(vm, por[k]["valor_modelo"]), f"libro {vm!r} · registro {por[k]['valor_modelo']!r} · exacto {float(ex)!r}"


def guardia_libros(c):
    """comprobar_celdas_v2 sin fases: solo la guardia 4 (fuera de las celdas de juicio, el evaluado igual que el de datos)."""
    r = subprocess.run([PY, "-B", os.path.join(SCRIPTS, "comprobar_celdas_v2.py"), os.path.join(c, f"{E}_v63_evaluada.xlsx"),
                        os.path.join(c, f"{E}_v63_datos.xlsx"), "--fases", "ninguna"], capture_output=True, text=True)
    return r.returncode == 0, (r.stdout.strip().splitlines() or [""])[0][:200]


def caso_jumbo_sintetico():
    c = construir("jumbo_200_150")
    h0 = huellas(os.path.dirname(c))
    cfg = config_v2.cargar(CFG)
    r = {}

    def aplicar():
        r["res"] = ED.aplicar(c, "B", cfg)
        return bool(r["res"].get("cambios")), ED.resumen_texto(r["res"])[:300]
    intento("tipo Jumbo: con C76 200 → 150 en la fase B, el recálculo cambia C46 y C40", aplicar)
    intento("tipo Jumbo: C46 = ROUND(exacto con C76 = 150; 3) en los dos libros (cálculo propio de la prueba)",
            lambda: (all(leer(c, n, "Análisis!C46") == V46_150 for n in (f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx")) and V46_150 != V46_200,
                     f"esperado {V46_150!r} (antes {V46_200!r}); exacto {float(esperado_c46(150))!r}"))
    intento("tipo Jumbo: C40 = ROUND(exacto con C76 = 150; 3) en los dos libros",
            lambda: (all(leer(c, n, "Análisis!C40") == V40_150 for n in (f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx")) and V40_150 != V40_200,
                     f"esperado {V40_150!r} (antes {V40_200!r})"))
    intento("tipo Jumbo: con menos caja sobrante en C76 entran más intereses cobrados: C46 y C40 suben (la regla J1 no cambia)",
            lambda: (V46_150 > V46_200 and V40_150 > V40_200, f"C46 {V46_200} → {V46_150} · C40 {V40_200} → {V40_150}"))
    intento("tipo Jumbo: precisión U2 (el exacto o su redondeo a 3 decimales; aquí 3 decimales como mucho)",
            lambda: (VE._importe_libro_exacto(esperado_c46(150), V46_150) and VE._importe_libro_exacto(esperado_c40(150), V40_150)
                     and (F(V46_150) * 1000).denominator == 1 and (F(V40_150) * 1000).denominator == 1, f"{V46_150!r}, {V40_150!r}"))
    intento("tipo Jumbo: el registro de C46 sigue coherente (su fórmula con C76 del libro da el valor del libro; valor_modelo = libro)",
            lambda: coherente(c, "Análisis!C46"))
    intento("tipo Jumbo: el registro de C40 sigue coherente", lambda: coherente(c, "Análisis!C40"))

    def via_generativa():
        lb = LibroV63(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
        inst = {"celdas": {k: lb.leer(*k.split("!")) for k in VE.ENTRADAS_FCF_BASE}}
        nr = VE.entradas_no_reproducibles(c, inst)
        f1 = json.load(open(os.path.join(c, "fase1_v63.json"), encoding="utf-8"))["analisis"]
        me = json.load(open(os.path.join(c, "fase1_metadatos.json"), encoding="utf-8"))["analisis"]
        return ("Análisis!C46" not in nr and f1["C46"]["valor"] == V46_150 and me["C46"]["valor"] == V46_150 and f1["C40"]["valor"] == V40_150
                and me["C40"]["valor"] == V40_150), f"no reproducibles {sorted(nr)} · fase1_v63 {f1['C46']['valor']}/{f1['C40']['valor']}"
    intento("tipo Jumbo: la vía generativa reproduce el libro (fase1_v63.json y fase1_metadatos.json con el valor nuevo; ninguna entrada del FCF base "
            "no reproducible)", via_generativa)

    def k3a():
        it = json.load(open(os.path.join(c, "motor_a_f1.json"), encoding="utf-8"))["conciliacion_fcf_base"][0]
        dif = F(it["importe"]) - F(IMPORTE_K3A)
        return (dif == F(V46_150) - F(V46_200) and "C76 = 150" in it["partida"] and it["recalculo_dependiente"]["importe_declarado"] == IMPORTE_K3A,
                f"importe {IMPORTE_K3A} → {it['importe']} (Δ {float(dif)}) · {it['partida'][-110:]}")
    intento("tipo Jumbo: la partida F1-K3a de C46 (conciliacion_f1) cambia exactamente lo que cambia C46", k3a)

    def notas():
        ns = [LibroV63(os.path.join(c, n)).leer("Control maestro", "N43") for n in (f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx")]
        return (ns[0] == ns[1] and "Análisis!C76 = 150" in ns[0] and "(preparación sintética)" in ns[0] and ns[0].count(ED.MARCA_NOTA) == 1,
                ns[0][-160:])
    intento("tipo Jumbo: nota en la evidencia del Control maestro (N43), la misma en los dos libros, sin perder el texto anterior", notas)
    intento("tipo Jumbo: comprobar_celdas_v2 (guardia de los libros) sigue exigiendo los dos libros iguales fuera de las celdas de juicio, y pasa",
            lambda: guardia_libros(c))

    def verificador():
        cfg_ = config_v2.cargar(CFG)
        rs = [subprocess.run([PY, cfg_["plantilla"]["verificador"], os.path.join(c, n), cfg_["plantilla"]["referencia"]], capture_output=True, text=True)
              for n in (f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx")]
        return all(x.returncode == 0 for x in rs), " · ".join((x.stdout.strip().splitlines() or [""])[-1] for x in rs)[:200]
    intento("tipo Jumbo: los dos libros siguen íntegros (verificador de la plantilla V6.3.1 F1)", verificador)

    def rastro():
        t = json.load(open(os.path.join(c, ED.RASTRO), encoding="utf-8"))
        v = t["vigente"]["Análisis!C46"]
        h = t["historial"][-1]
        cam = {x["celda"]: x for x in h["cambios"]}
        ok = (v["valor"] == V46_150 and v["valor_declarado"] == V46_200 and v["celdas_de_juicio"] == {"Análisis!C76": 150}
              and cam["Análisis!C46"]["antes"] == V46_200 and cam["Análisis!C46"]["despues"] == V46_150 and cam["Análisis!C40"]["despues"] == V40_150
              and set(h["archivos"]) >= {f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx", VE.REGISTRO, "fase1_v63.json", "motor_a_f1.json"}
              and h["origenes"]["Análisis!C46"]["Análisis!C76"]["valor"] == 150)
        return ok, f"vigente {v['valor_declarado']} → {v['valor']} con {v['celdas_de_juicio']} · archivos {sorted(h['archivos'])}"
    intento("tipo Jumbo: rastro auditado (recalculo_dependientes.json): antes, después, C76 usado, orígenes y huellas de los archivos", rastro)

    def resultados():
        res = os.path.join(os.path.dirname(c), "resultados")
        md = open(os.path.join(res, f"recalculo_dependientes_{E}.md"), encoding="utf-8").read()
        js = json.load(open(os.path.join(res, f"recalculo_dependientes_{E}.json"), encoding="utf-8"))
        return ("Análisis!C76 = 150" in md and str(V46_150).replace(".", ",") in md and js == json.load(open(os.path.join(c, ED.RASTRO), encoding="utf-8")),
                md.splitlines()[0])
    intento("tipo Jumbo: rastro en resultados/ (recalculo_dependientes_<E>.json, idéntico al auditado, y .md)", resultados)
    intento("tipo Jumbo: el rastro forma parte del material auditado (cierre_v2.MATERIAL_FIJO)",
            lambda: (ED.RASTRO in CIE.MATERIAL_FIJO and ED.RASTRO in CIE.material(c)[1], f"{len(CIE.material(c)[1])} archivos en el material"))

    def solo_lo_declarado():
        h1 = huellas(os.path.dirname(c))
        cambiados = sorted(k for k in h1 if h0.get(k) != h1[k])
        esperados = sorted([f"{E}/{n}" for n in (f"{E}_v63_datos.xlsx", f"{E}_v63_evaluada.xlsx", VE.REGISTRO, "fase1_v63.json", "fase1_metadatos.json",
                                                 "motor_a_f1.json", ED.RASTRO)] + [f"resultados/recalculo_dependientes_{E}.json", f"resultados/recalculo_dependientes_{E}.md"])
        return cambiados == esperados, f"cambiados {cambiados}"
    intento("tipo Jumbo: solo cambian los libros, las declaraciones de esas entradas y el rastro (fase_b.json y el resto, intactos)", solo_lo_declarado)

    def registro_solo_valor():
        reg = {e["celda"]: e for e in VE.cargar(c)[0]["entradas"]}
        orig = {e["celda"]: e for e in registro(True)["entradas"]}
        otros = [k for k in orig if k not in ("Análisis!C46", "Análisis!C40") and reg[k] != orig[k]]
        e = reg["Análisis!C46"]
        sin = {x: y for x, y in e.items() if x not in ("valor_modelo", "recalculo_dependiente")}
        o = {x: y for x, y in orig["Análisis!C46"].items() if x != "valor_modelo"}
        return not otros and sin == o, f"otras entradas cambiadas {otros}; comprobación {e['comprobacion']}"
    intento("tipo Jumbo: del registro solo cambian valor_modelo y el rastro de las dos entradas (ni la comprobación, ni la fórmula, ni las demás)",
            registro_solo_valor)

    def idempotente():
        a = huellas(os.path.dirname(c))
        r2 = ED.aplicar(c, "B", cfg)
        b = huellas(os.path.dirname(c))
        return a == b and not r2["cambios"] and not r2["escrito"], ED.resumen_texto(r2)[:200]
    intento("idempotencia: repetir el recálculo con la misma fase B no cambia ningún archivo", idempotente)

    def cli_previsualizar():
        a = huellas(os.path.dirname(c))
        fb = os.path.join(BASE, "fase_b_140.json")
        open(fb, "w", encoding="utf-8").write(json.dumps({"celdas": {"C76": 140}}))
        rr = subprocess.run([PY, "-B", os.path.join(SCRIPTS, "entradas_dependientes.py"), "previsualizar", c, "--fase-b", fb], capture_output=True, text=True)
        b = huellas(os.path.dirname(c))
        v140 = float(redondeo(esperado_c46(140), 3))
        return rr.returncode == 0 and repr(v140) in rr.stdout and "no se ha escrito nada" in rr.stdout and a == b, rr.stdout.strip().splitlines()[0][:200]
    intento("previsualizar (con las celdas de una fase_b.json) no escribe nada y da el valor que tendría", cli_previsualizar)
    return c


def caso_c76_vuelve():
    """La fase B corrige C76 dos veces (150 → 140 → 150): el resultado final no depende del camino."""
    c = construir("camino")
    cfg = config_v2.cargar(CFG)
    ED.aplicar(c, "B", cfg)
    lb = LibroV63(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    lb.escribir("Análisis", "C76", 140)
    lb.marcar_modificada("Análisis")
    lb.guardar(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    ED.aplicar(c, "B", cfg)
    v140 = leer(c, f"{E}_v63_evaluada.xlsx", "Análisis!C46")
    lb = LibroV63(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    lb.escribir("Análisis", "C76", 150)
    lb.marcar_modificada("Análisis")
    lb.guardar(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    ED.aplicar(c, "B", cfg)
    d = construir("directo")
    ED.aplicar(d, "B", cfg)
    mismo = all(json.load(open(os.path.join(c, n), encoding="utf-8")) == json.load(open(os.path.join(d, n), encoding="utf-8"))
                for n in ("fase1_v63.json", "fase1_metadatos.json", VE.REGISTRO, "motor_a_f1.json"))
    it = json.load(open(os.path.join(c, "motor_a_f1.json"), encoding="utf-8"))["conciliacion_fcf_base"][0]
    hist = json.load(open(os.path.join(c, ED.RASTRO), encoding="utf-8"))["historial"]
    return (mismo and v140 == float(redondeo(esperado_c46(140), 3)) and leer(c, f"{E}_v63_datos.xlsx", "Análisis!C46") == V46_150
            and F(it["importe"]) == F(IMPORTE_K3A) + F(V46_150) - F(V46_200) and len(hist) == 3,
            f"140 → {v140} · final {leer(c, f'{E}_v63_datos.xlsx', 'Análisis!C46')} · importe {it['importe']} · {len(hist)} aplicaciones en el historial")


def caso_sin_declaracion():
    c = construir("sin_declaracion", declarar=False)
    h0 = huellas(os.path.dirname(c))
    r = ED.aplicar(c, "B", config_v2.cargar(CFG))
    h1 = huellas(os.path.dirname(c))
    return (h0 == h1 and not r["declaradas"] and not ED.hay_declaraciones(c) and leer(c, f"{E}_v63_evaluada.xlsx", "Análisis!C46") == V46_200,
            f"declaradas {r['declaradas']} · archivos iguales {h0 == h1}")


def sin_cambios_si_falla(nombre, preparar, se_espera, c76=150):
    """Una declaración o un estado defectuoso detiene el recálculo (ErrorRecalculo) sin escribir nada."""
    def f():
        c = construir(nombre, c76_tras_fase_b=c76)
        preparar(c)
        h0 = huellas(os.path.dirname(c))
        try:
            ED.aplicar(c, "B", config_v2.cargar(CFG))
            return False, "no se detuvo"
        except ED.ErrorRecalculo as ex:
            h1 = huellas(os.path.dirname(c))
            return h0 == h1 and se_espera in str(ex), f"{str(ex)[:230]} · sin escribir: {h0 == h1}"
    intento(f"se detiene sin escribir nada: {nombre}", f)


def casos_defectuosos():
    def con(k, cambio):
        return lambda c: editar_registro(c, lambda por, d: cambio(por[k], por, d))
    sin_cambios_si_falla("celda de juicio que no es origen de la fórmula",
                         con("Análisis!C46", lambda e, p, d: e["derivacion"]["recalculo"].update(celdas_de_juicio=["Análisis!C76", "Análisis!C68"])),
                         "no es un origen")
    sin_cambios_si_falla("celda de la fase C (se escribe después del recálculo)",
                         con("Análisis!C46", lambda e, p, d: e["derivacion"]["recalculo"].update(celdas_de_juicio=["Análisis!C76", "Análisis!C93"])),
                         "fase C")
    sin_cambios_si_falla("celda de datos declarada como de juicio",
                         con("Análisis!C40", lambda e, p, d: e["derivacion"]["recalculo"].update(celdas_de_juicio=["Análisis!C76", "Historia!L11"])),
                         "no es una celda de juicio")

    def origen_juicio(e, p, d):
        e["derivacion"]["origenes"].append("Palancas!B14")
        e["derivacion"]["formula"] = "(" + e["derivacion"]["formula"] + ")+o[\"Palancas!B14\"]"
    sin_cambios_si_falla("origen de juicio de la fase B sin declarar", con("Análisis!C40", origen_juicio), "no se declara")
    sin_cambios_si_falla("cifra escrita en la fórmula (C76 = 160 dentro de ella)",
                         con("Análisis!C40", lambda e, p, d: e["derivacion"].update(formula=e["derivacion"]["formula"].replace(
                             'o["Análisis!C76"]/', '(o["Análisis!C76"]+160-160)/'))),
                         "escribe cifras")

    def no_usa(e, p, d):
        e["derivacion"]["origenes"].append("aux:cfo_2024")
    sin_cambios_si_falla("la fórmula no usa todos sus orígenes", con("Análisis!C40", no_usa), "los orígenes son")
    sin_cambios_si_falla("entrada que no es un derivado", con("Análisis!C40", lambda e, p, d: e.update(clase="dato_publicado")), "clase")

    def historia(e, p, d):
        e["celda"] = "Historia!L11"
    sin_cambios_si_falla("celda que no es una entrada de datos de Análisis", con("Análisis!C40", historia), "solo se recalculan celdas de datos de Análisis")
    sin_cambios_si_falla("clave desconocida en «recalculo» (errata)",
                         con("Análisis!C40", lambda e, p, d: e["derivacion"]["recalculo"].update(celda_de_juicio="Análisis!C76")), "no admitidas")
    sin_cambios_si_falla("«regla» vacía", con("Análisis!C40", lambda e, p, d: e["derivacion"]["recalculo"].update(regla=" ")), "regla")
    sin_cambios_si_falla("conciliacion_f1 sin partida en motor_a_f1.json", lambda c: os.remove(os.path.join(c, "motor_a_f1.json")), "una sola partida")

    def dos_partidas(c):
        p = os.path.join(c, "motor_a_f1.json")
        d = json.load(open(p, encoding="utf-8"))
        d["conciliacion_fcf_base"].append(dict(d["conciliacion_fcf_base"][0], importe=0.1))
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    sin_cambios_si_falla("conciliacion_f1 con dos partidas del componente", dos_partidas, "una sola partida")
    sin_cambios_si_falla("partida F1-K3a del componente sin declarar conciliacion_f1",
                         con("Análisis!C46", lambda e, p, d: e["derivacion"]["recalculo"].pop("conciliacion_f1")), "hay que declarar «conciliacion_f1»")

    def cadena(e, p, d):
        d["entradas"].append({"celda": "Análisis!C88", "clase": "derivado", "valor_modelo": 14.4, "derivacion": {
            "origenes": ["Análisis!C40", "aux:caja_2025"], "formula": 'o["aux:caja_2025"]/o["Análisis!C40"]', "conciliacion": "x", "unidad": "x"}})
    sin_cambios_si_falla("derivada del registro que usa una entrada dependiente sin declararse", con("Análisis!C40", cadena), "no es una entrada dependiente declarada")

    def formula_libro(e, p, d):
        e["derivacion"]["origenes"].append("Análisis!C52")
        e["derivacion"]["formula"] = "(" + e["derivacion"]["formula"] + ")+o[\"Análisis!C52\"]"
    sin_cambios_si_falla("origen que es una fórmula del libro (sin valor vigente antes del recálculo)", con("Análisis!C40", formula_libro), "fórmula del libro")
    sin_cambios_si_falla("celda de juicio vacía tras la fase B", lambda c: None, "vacía", c76=VACIA)

    def copia_distinta(c):
        p = os.path.join(c, "fase1_v63.json")
        d = json.load(open(p, encoding="utf-8"))
        d["analisis"]["C46"]["valor"] = 300.0
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    sin_cambios_si_falla("una copia del valor distinta (fase1_v63.json) del libro y del recalculado", copia_distinta, "las copias no tienen")

    def con_calculo(c):
        p = os.path.join(c, "fase1_metadatos.json")
        d = json.load(open(p, encoding="utf-8"))
        d["analisis"]["C46"]["calculo"] = {"operacion": "media", "anios": [2025], "terminos": []}
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
    sin_cambios_si_falla("la entrada tiene además un «calculo» de fase1_historia", con_calculo, "dos derivaciones")

    def partida_tocada(c):
        ED.aplicar(c, "B", config_v2.cargar(CFG))
        p = os.path.join(c, "motor_a_f1.json")
        d = json.load(open(p, encoding="utf-8"))
        d["conciliacion_fcf_base"][0]["importe"] = 11.0
        open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
        lb = LibroV63(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
        lb.escribir("Análisis", "C76", 140)
        lb.marcar_modificada("Análisis")
        lb.guardar(os.path.join(c, f"{E}_v63_evaluada.xlsx"))
    sin_cambios_si_falla("partida F1-K3a cambiada a mano después de un recálculo", partida_tocada, "se revisa a mano")


def casos_precision():
    intento("U2: un exacto con 3 decimales se guarda exacto", lambda: (ED._valor_libro(Fr(317617, 1000), "millones de euros")[0] == 317.617, ""))
    intento("U2: empate x,xxx5 → mitad lejos de cero (1,2345 → 1,235; −1,2345 → −1,235)",
            lambda: (ED._valor_libro(Fr(12345, 10000), "mm")[0] == 1.235 and ED._valor_libro(Fr(-12345, 10000), "mm")[0] == -1.235, ""))
    intento("U2: un importe periódico (1/3) → 0,333, que la verificación admite",
            lambda: (ED._valor_libro(Fr(1, 3), "mm")[0] == 0.333 and VE._importe_libro_exacto(Fr(1, 3), 0.333), ""))
    intento("U2: lo que no es un importe se guarda exacto (sin el redondeo del libro)",
            lambda: (ED._valor_libro(Fr(1, 3), "x")[0] == 1 / 3 and VE._igual_exacto(ED._valor_libro(Fr(1, 3), "x")[0], 1 / 3), ""))


def pipeline_paso9(nombre, declarar=True, preparar=None):
    """Paso 9 del pipeline sobre el ensayo sintético, sin LibreOffice: la escritura de la fase B y comprobar_celdas_v2 se simulan (anotando el
    orden y lo que ven) y el recálculo del libro se detiene. Devuelve (eventos, pipeline, carpeta, terminado)."""
    import pipeline as PL
    c = construir(nombre, declarar=declarar, c76_tras_fase_b=None)
    if preparar:
        preparar(c)
    P = PL.Pipeline(c, config_v2.cargar(CFG))
    P.st["paso"], P.st["motor"] = 9, "A"
    ev = []
    ev_libro = os.path.join(c, f"{E}_v63_evaluada.xlsx")

    def escribir(fase_json, fase, li, lo):
        ev.append(("escribir", fase))
        lb = LibroV63(li)
        lb.escribir("Análisis", "C76", 150)
        lb.marcar_modificada("Análisis")
        lb.guardar(lo)
        return 0, "OK (escritura de la fase B simulada)"
    run0 = P.run

    def run(cmd, ok=(0,)):
        n = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ""
        if n == "comprobar_celdas_v2.py":
            ev.append(("comprobar_celdas", LibroV63(cmd[2]).leer("Análisis", "C46")))
            return 0, "PASS (simulado)"
        if n == "entradas_dependientes.py":
            ev.append(("dependientes", cmd[2]))
        return run0(cmd, ok)

    class Alto(Exception):
        pass

    def recalc(libro):
        lb = LibroV63(libro)
        ev.append(("recalculo_del_libro", lb.leer("Análisis", "C46"), lb.leer("Análisis", "C40")))
        raise Alto()
    term = []
    P.escribir, P.run, P.recalc_leer_precio = escribir, run, recalc
    P.terminar = lambda *a, **k: term.append((a, k))
    try:
        P.correr(hasta=9)
    except Alto:
        pass
    return ev, P, c, term, ev_libro


def casos_pipeline():
    def con():
        ev, P, c, term, _ = pipeline_paso9("paso9")
        esperado = [("escribir", "B"), ("comprobar_celdas", V46_200), ("dependientes", "aplicar"), ("comprobar_celdas", V46_150),
                    ("recalculo_del_libro", V46_150, V40_150)]
        return ev == esperado and not term, f"{ev}"
    intento("paso 9: fase B escrita → comprobar_celdas → recálculo dependiente → comprobar_celdas de nuevo → recálculo del libro con C46/C40 nuevos", con)

    def estado():
        ev, P, c, term, _ = pipeline_paso9("paso9_estado")
        st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8"))
        r = st.get("recalculo_dependientes") or {}
        linea = [h for h in st["historial"] if "entradas dependientes de celdas de juicio" in h]
        return ([x["celda"] for x in r.get("cambios") or []] == ["Análisis!C46", "Análisis!C40"] and linea and "C76" in linea[0]
                and P.st.get("fase_b_escrita") is True, (linea or [""])[0][:220])
    intento("paso 9: el estado del pipeline y su historial registran el recálculo (antes/después, C76)", estado)

    def sin():
        ev, P, c, term, _ = pipeline_paso9("paso9_sin", declarar=False)
        st = json.load(open(os.path.join(c, "estado_pipeline.json"), encoding="utf-8")) if os.path.exists(os.path.join(c, "estado_pipeline.json")) else P.st
        return (ev == [("escribir", "B"), ("comprobar_celdas", V46_200), ("recalculo_del_libro", V46_200, V40_200)] and not term
                and not os.path.exists(os.path.join(c, "recalculo_dependientes.json")) and "recalculo_dependientes" not in st
                and not any("dependientes" in h for h in st.get("historial") or [])), f"{ev}"
    intento("paso 9 sin declaraciones: igual que antes (ni lanza el programa, ni rastro, ni línea en el historial)", sin)

    def mala():
        ev, P, c, term, ev_libro = pipeline_paso9("paso9_mala", preparar=lambda c: editar_registro(
            c, lambda por, d: por["Análisis!C46"]["derivacion"]["recalculo"].update(celdas_de_juicio=["Análisis!C93"])))
        a, k = term[0] if term else ((), {})
        return (bool(term) and a[0] == "no_entregable" and a[1] == "fallo_de_implementacion" and k.get("desde") == 9 and "recalculo_del_libro" not in [x[0] for x in ev]
                and LibroV63(ev_libro).leer("Análisis", "C46") == V46_200), f"{a[:2]} desde {k.get('desde')} · {str(a[2])[:150] if a else ''}"
    intento("paso 9 con una declaración mal formada: no_entregable (fallo de implementación), continuar desde el paso 9, sin recalcular nada", mala)

    def fase_c():
        import pipeline as PL
        cap = {}
        c = construir("fase_c")
        for con_rastro in (False, True):
            if con_rastro:
                ED.aplicar(c, "B", config_v2.cargar(CFG))
            P = PL.Pipeline(c, config_v2.cargar(CFG))
            P.st.update(paso=10, motor="A", fase_b_escrita=True)

            def agente(paso_, nombre, salida, entradas, alternativas=(), _k=con_rastro):
                cap[_k] = list(entradas)
                raise PL.Esperando("prueba")
            P.agente = agente
            try:
                P.correr(hasta=10)
            except PL.Esperando:
                pass
        return (not any("recalculo_dependientes" in x for x in cap.get(False, [])) and any(x.startswith("recalculo_dependientes.json") for x in cap.get(True, [])),
                str(cap.get(True, [])[-1:])[:200])
    intento("fase C: recibe recalculo_dependientes.json entre sus entradas si existe (datos_v63.md da los valores anteriores); si no, nada cambia", fase_c)

    def paso2():
        import pipeline as PL
        res = {}
        for nombre, preparar in (("paso2_mala", lambda c: editar_registro(c, lambda por, d: por["Análisis!C46"]["derivacion"]["recalculo"].update(
                celdas_de_juicio=["Análisis!C93"]))), ("paso2_bien", None), ("paso2_sin", "sin")):
            c = construir(nombre, declarar=preparar != "sin")
            if callable(preparar):
                preparar(c)
            P = PL.Pipeline(c, config_v2.cargar(CFG))
            P.st["paso"] = 2
            datos = os.path.join(c, f"{E}_v63_datos.xlsx")
            run0, vistos, term = P.run, [], []

            def run(cmd, ok=(0,), _v=vistos, _r=run0, _d=datos):
                n = os.path.basename(str(cmd[1])) if len(cmd) > 1 else ""
                _v.append(n)
                if n == "rellenar_fase1_v63.py":
                    return 0, "OK (rellenar simulado: el libro de datos ya está escrito)"
                if n == "f1_libro_v631.py":
                    shutil.copy(_d, _d + ".f1.xlsx")
                    return 0, "OK (capa F1 simulada)"
                return _r(cmd, ok)
            P.run = run
            P.terminar = lambda *a, _t=term, **k: _t.append((a, k))
            P.correr(hasta=2)
            res[nombre] = (vistos, term, P.st["paso"])
        m_v, m_t, _ = res["paso2_mala"]
        b_v, b_t, b_p = res["paso2_bien"]
        s_v, s_t, s_p = res["paso2_sin"]
        return (bool(m_t) and m_t[0][0][0] == "no_entregable" and m_t[0][1].get("desde") == 2 and "entradas_dependientes.py" in m_v
                and not b_t and b_p == 3 and "entradas_dependientes.py" in b_v and not s_t and s_p == 3 and "entradas_dependientes.py" not in s_v,
                f"mala: {m_t[0][0][:2] if m_t else None} · bien: paso {b_p} · sin declaración: paso {s_p}, programas {s_v}")
    intento("paso 2: la declaración se valida antes de las fases (mal formada: no_entregable, continuar desde el paso 2; sin declaraciones, ni se lanza)", paso2)


def caso_concordancia():
    import cambiar_base as CB
    c = construir("concordancia")
    ED.aplicar(c, "B", config_v2.cargar(CFG))
    ens = os.path.dirname(c)
    conf = {"destino": ens, "empresa": E, "analisis": {"C46": {"valor": V46_200}, "C40": {"valor": V40_200}}, "metadatos": {}, "textos_prohibidos": []}
    with contextlib.redirect_stdout(io.StringIO()):
        ok = CB.comprobar(conf, os.path.join(c, f"{E}_v63_datos.xlsx"))
    filas = json.load(open(os.path.join(ens, "resultados", f"concordancia_{E}_v63_datos.json"), encoding="utf-8"))["concordancia"]
    f46 = next(x for x in filas if x["celda"] == "Análisis!C46")
    return (ok and f46["concuerda"] and f46["configuracion"] == V46_150 and f46["recalculada_tras_fase_b"]["valor_declarado"] == V46_200,
            f"{f46}"[:220])


def caso_jumbo_g():
    """jumbo_g real: la fase B escrita (C76 = 150) y sin consumir. Copia temporal, declaración en el registro (como la añadiría la orquestación)
    y el paso 8 → 9 de verdad (validar_esquema, citas, gramática, escritura de la fase B, comprobar_celdas_v2), con el recálculo del libro
    detenido (sin LibreOffice)."""
    E_ = "Jumbo"
    src = os.path.join(JUMBO_G, E_)
    libros_ = [os.path.join(src, f"{E_}_v63_{x}.xlsx") for x in ("datos", "evaluada")]
    st0 = json.load(open(os.path.join(src, "estado_pipeline.json"), encoding="utf-8")) if os.path.isfile(os.path.join(src, "estado_pipeline.json")) else {}
    if not all(os.path.isfile(p) for p in libros_):
        print(f"OMITIDA · jumbo_g real: no están sus libros ({os.path.relpath(src, PV) if src.startswith(PV) else src}); los binarios del expediente no están en Git")
        return
    lb0 = LibroV63(libros_[1])
    if not (st0.get("paso") == 8 and st0.get("esperando") == "8:fase_b.json" and lb0.leer("Análisis", "C76") == 200 and lb0.leer("Análisis", "C46") == 317.617
            and os.path.isfile(os.path.join(src, "fase_b.json"))):
        print("OMITIDA · jumbo_g real: el expediente ya no está en el estado de partida (paso 8 esperando fase_b.json, C76 = 200 y C46 = 317,617 en el libro)")
        return
    import pipeline as PL
    h_fb = hashlib.sha256(open(os.path.join(src, "fase_b.json"), "rb").read()).hexdigest()

    def correr(declarar):
        ens = os.path.join(BASE, "jumbo_g" if declarar else "jumbo_g_sin_declaracion")
        shutil.copytree(JUMBO_G, ens, ignore=shutil.ignore_patterns("pdf", ".lo_perfil", "__pycache__"))
        cc = os.path.join(ens, E_)
        if declarar:  # como la añadiría la orquestación: solo la declaración, en las dos entradas del registro
            p = os.path.join(cc, VE.REGISTRO)
            d = json.load(open(p, encoding="utf-8"))
            for e in d["entradas"]:
                if e["celda"] in ("Análisis!C46", "Análisis!C40"):
                    e["derivacion"]["recalculo"] = json.loads(json.dumps(RECALCULO_C46 if e["celda"] == "Análisis!C46" else RECALCULO_C40))
                    e["derivacion"]["recalculo"]["regla"] = "J1 (DECISIONES_PARA_EL_USUARIO.md, 18-nov-2026)"
            open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
        P = PL.Pipeline(cc, config_v2.cargar(CFG))
        visto = {}

        class Alto(Exception):
            pass

        def recalc(libro):
            lb = LibroV63(libro)
            visto.update(C46=lb.leer("Análisis", "C46"), C40=lb.leer("Análisis", "C40"), C76=lb.leer("Análisis", "C76"))
            raise Alto()
        P.recalc_leer_precio = recalc
        try:
            P.correr(hasta=9)
        except Alto:
            pass
        except PL.Esperando as ex:
            visto["esperando"] = str(ex)
        return cc, P, visto
    cc, P, visto = correr(True)
    hist = P.st.get("historial") or []
    i_dep = next((i for i, h in enumerate(hist) if "entradas_dependientes.py aplicar" in h), None)
    celdas_ok = [h for h in hist[i_dep:] if "comprobar_celdas_v2.py" in h and "→ 0" in h] if i_dep is not None else []
    paso("jumbo_g real: el paso 9 consume la fase B escrita (C76 = 150) y recalcula C46 317,617 → 317,902 y C40 255,108 → 255,305 antes del recálculo del libro",
         visto.get("C76") == 150 and visto.get("C46") == 317.902 and visto.get("C40") == 255.305 and i_dep is not None, f"{visto}")
    paso("jumbo_g real: comprobar_celdas_v2 (fases A y B, de verdad) pasa sobre los libros recalculados",
         bool(celdas_ok), (celdas_ok or [""])[-1][:200])
    paso("jumbo_g real: la fase B no se reabre (fase_b.json intacto y consumido; no se pide ningún agente)",
         hashlib.sha256(open(os.path.join(cc, "fase_b.json"), "rb").read()).hexdigest() == h_fb and "fase_b.json" in (P.st.get("consumidos") or {})
         and not visto.get("esperando") and P.st.get("esperando") is None, f"esperando {P.st.get('esperando')!r}")
    reg, _ = VE.cargar(cc)
    por = {e["celda"]: e for e in reg["entradas"]}
    lb = LibroV63(os.path.join(cc, f"{E_}_v63_evaluada.xlsx"))
    bien = []
    for k in ("Análisis!C46", "Análisis!C40"):
        d = por[k]["derivacion"]
        vals = {o: (por[o]["valor_modelo"] if o.startswith("aux:") else lb.leer(*o.split("!"))) for o in d["origenes"]}
        ex = VE._eval_formula_exacta(d["formula"], vals)
        bien.append(VE._importe_libro_exacto(ex, lb.leer(*k.split("!"))) and VE._igual_exacto(lb.leer(*k.split("!")), por[k]["valor_modelo"]))
    paso("jumbo_g real: el registro de C46 y C40 sigue coherente (su fórmula con C76 = 150 da el valor del libro)", all(bien), f"{bien}")
    it = json.load(open(os.path.join(cc, "motor_a_f1.json"), encoding="utf-8"))["conciliacion_fcf_base"][0]
    paso("jumbo_g real: la partida F1-K3a de C46 pasa de 10,444 a 10,729 (lo que cambia C46)", it["importe"] == 10.729, f"{it['importe']}")
    # sin la declaración: el defecto que corrige el cambio (C46 sigue con C76 = 160 y su derivación no reproduce el libro)
    cc2, P2, visto2 = correr(False)
    reg2, _ = VE.cargar(cc2)
    por2 = {e["celda"]: e for e in reg2["entradas"]}
    lb2 = LibroV63(os.path.join(cc2, f"{E_}_v63_evaluada.xlsx"))
    d = por2["Análisis!C46"]["derivacion"]
    vals = {o: (por2[o]["valor_modelo"] if o.startswith("aux:") else lb2.leer(*o.split("!"))) for o in d["origenes"]}
    ex2 = VE._eval_formula_exacta(d["formula"], vals)
    paso("jumbo_g real sin declaración: el pipeline no cambia nada y la derivación de C46 no reproduce el libro (el defecto de partida)",
         visto2.get("C46") == 317.617 and visto2.get("C76") == 150 and not VE._importe_libro_exacto(ex2, 317.617) and not os.path.exists(os.path.join(cc2, "recalculo_dependientes.json")),
         f"libro {visto2.get('C46')} · fórmula con C76 = 150: {float(ex2):.6f}")


if __name__ == "__main__":
    BASE = tempfile.mkdtemp(prefix="entradas_dependientes_", dir="/dev/shm" if os.path.isdir("/dev/shm") else None)
    try:
        if ED is None:
            paso("existe scripts/entradas_dependientes.py", False, f"{type(ERROR_ED).__name__}: {ERROR_ED}")
        caso_jumbo_sintetico()
        intento("camino: C76 150 → 140 → 150 deja los mismos archivos que 150 directamente (determinista)", caso_c76_vuelve)
        intento("sin declaración en el registro no cambia nada (ni libros, ni declaraciones, ni rastro)", caso_sin_declaracion)
        casos_defectuosos()
        casos_precision()
        casos_pipeline()
        intento("cambiar_base.py comprobar: la entrada recalculada concuerda con el valor recalculado y lo dice", caso_concordancia)
        try:
            caso_jumbo_g()
        except Exception as ex:  # noqa: BLE001
            paso("jumbo_g real", False, f"{type(ex).__name__}: {str(ex)[:300]}")
    finally:
        shutil.rmtree(BASE, ignore_errors=True)
    print(f"{total - len(fallos)}/{total} pruebas de las entradas dependientes PASAN")
    sys.exit(0 if not fallos else 1)
