#!/usr/bin/env python3
"""Pruebas de la plantilla V6.3.2 F1 (V-CIRC: normalización declarada del circulante de la reinversión, 19-nov-2026).

Uso (desde cualquier carpeta):
  python3 -I probar_v632_f1.py estructura                                                       sin LibreOffice
  flock /home/user/e_work/libreoffice.lock python3 -I probar_v632_f1.py a0 DESTINO       con LibreOffice (DESTINO: carpeta nueva fuera del repo)
  flock /home/user/e_work/libreoffice.lock python3 -I probar_v632_f1.py circ DESTINO     con LibreOffice

estructura: reconstrucción determinista desde la V6.3 (mismo SHA-256 que el entregable y que el origen de la referencia); la V6.3 y la V6.3.1 F1 sin
  cambios; la referencia de la V6.3.2 frente a la de la V6.3.1 difiere EXACTAMENTE en las celdas previstas (fórmulas de la fila 30, C53, C58, C76,
  Motor E205 y Panel A1; fórmulas nuevas C95:L97; tres etiquetas; la sección nueva A92:S98; dos validaciones; inventario + C93, C94:L94 y M93:S94);
  con «ninguna» las fórmulas de C53, C58 y C76 contienen literalmente las de la V6.3.1 F1; el verificador de la V6.3.2 acepta la plantilla y rechaza
  dos mutaciones (el circulante de la reinversión sin normalizar; la normalización efectiva fija), y el de la V6.3.1 la rechaza.
a0: sin normalización (C93:L94 vacías), 0 celdas distintas (tolerancia 0, igualdad exacta) en las once hojas frente a la V6.3.1 F1 con las mismas
  entradas, recalculadas las dos por LibreOffice: perímetro vacío y «A0_total» en el libro de Elis (d2593777…) y en los tres ejemplos de la V6.3, y
  A1_sin_ROU y A2_propio en Elis con sus series; con A0, 0 celdas distintas frente a la V6.3. Excluidas solo las etiquetas de versión y las secciones
  nuevas. C97 = «ninguna», fila 95 = 0 y fila 96 = fila 14.
circ: (LibreOffice) el libro calcula la normalización declarada y la capa motor_a_f1.py es su oráculo. Caso tipo Vinci (circulante negativo
  estructural excluido de la caja base: las cifras de la Historia y del FCF base de VINCI sobre las entradas del ejemplo Empresa X): libro = capa en f
  (10⁻¹²), el ancla y los 33 flujos del Motor (10⁻⁹); F1-LIBRO, F1-REPLICA, F1-CIRC y F1-K3c no saltan; identidades con los valores del propio libro
  (f normalizada = f − media del circulante de la ventana ÷ ventas medias; C53 = ΔV ÷ (Σ fila 31 − Σ fila 14 de H–L)). Sin la normalización el libro es
  la V6.3.1 (0 celdas distintas) y K3c bloquea. Solo la ventana: f, sin ancla. Sin un año de la ventana: f vacía y Motor V05 INCOMPLETO. Regla o marca
  no reconocidas: f y ancla vacías y V05 DATOS INVÁLIDOS. A0 con la normalización. Un libro V6.3.1 con la normalización declarada: F1-LIBRO bloquea. Elis
  (caja base CON el circulante) con la normalización: el libro la calcula y la capa bloquea (F1-CIRC, DATOS INVÁLIDOS). (Revisión C1) La carpeta lleva el
  expediente sintético tipo VINCI (pruebas/datos_circulante/expediente_tipo_vinci.py: fase1_v63.json con el cálculo declarado de C46 y su texto), que
  es lo que demuestra la exclusión del circulante en la caja base; C9: la sonda del revisor (caja base CON el circulante y dos partidas C46 que se
  compensan) en un libro V6.3.2 recalculado: el libro calcula f −1,34 % y la capa bloquea con F1-CIRC.
Escribe ../pruebas/resultado_<prueba>.json y .md. Código 0 si todo pasa.
"""
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
V632 = os.path.dirname(AQUI)
V6 = os.path.dirname(V632)
RAIZ = os.path.dirname(V6)
PV = os.path.join(RAIZ, "personaje_v2")
V631 = os.path.join(V6, "v631_f1")
PLANTILLA_V63 = os.path.join(V6, "entregables", "Plantilla_V6.3.xlsx")
REF_V63 = os.path.join(V6, "referencia", "referencia_V6.3.json")
PLANTILLA_V631 = os.path.join(V631, "entregables", "Plantilla_V6.3.1_F1.xlsx")
REF_V631 = os.path.join(V631, "referencia", "referencia_V6.3.1_F1.json")
SHA_V631 = "eaece01a7d6a1d861e82e6c09e4cf8e550a8b5933d900eaea3589fe083898e09"
PLANTILLA = os.path.join(V632, "entregables", "Plantilla_V6.3.2_F1.xlsx")
REF = os.path.join(V632, "referencia", "referencia_V6.3.2_F1.json")
SHA_TXT = os.path.join(V632, "referencia", "SHA256_entregables_V6.3.2_F1.txt")
RECALC = os.path.join(PV, "scripts", "recalc.sh")
ELIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14", "elis_decisiones", "Elis", "Elis_v63_evaluada.xlsx")
SHA_ELIS = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"
EJEMPLOS = [os.path.join(V6, "entregables", n) for n in ("Ejemplo_V6.3_EmpresaX.xlsx", "Ejemplo_ABB_V6.3.xlsx", "Ejemplo_migracion_Hermes_V6.3.xlsx")]
FIX_VINCI = os.path.join(PV, "pruebas", "datos_circulante", "vinci_libro_v631.json")
PY = sys.executable
COLS = "CDEFGHIJKL"
sys.path.insert(0, AQUI)
REGLA = "circulante_a_cero"

RES = []


def chk(nombre, ok, detalle=""):
    RES.append({"prueba": nombre, "ok": bool(ok), "detalle": detalle})
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def run(args, **kw):
    r = subprocess.run(args, capture_output=True, text=True, **kw)
    return r.returncode, (r.stdout + r.stderr).strip()


def _fila(k):
    return int("".join(ch for ch in k.split("!")[1] if ch.isdigit()))


# ------------------------------------------------------------------------------------------------------------------ estructura
def estructura():
    ref63, ref631, ref = json.load(open(REF_V63)), json.load(open(REF_V631)), json.load(open(REF))
    chk("la V6.3 no cambia (SHA-256 = origen de su referencia)", sha(PLANTILLA_V63) == ref63["sha256_origen"], sha(PLANTILLA_V63)[:16])
    chk("la V6.3.1 F1 no cambia (SHA-256 eaece01a… = origen de su referencia): los expedientes V6.3.1 siguen con sus huellas",
        sha(PLANTILLA_V631) == SHA_V631 == ref631["sha256_origen"], sha(PLANTILLA_V631)[:16])
    with tempfile.TemporaryDirectory() as tmp:
        out = os.path.join(tmp, "Plantilla_V6.3.2_F1.xlsx")
        rc, txt = run([PY, "-I", os.path.join(AQUI, "construir_v632_f1.py"), PLANTILLA_V63, out])
        s_re = sha(out) if rc == 0 else None
    s_ent = sha(PLANTILLA)
    chk("reconstrucción determinista: el guion desde la V6.3 da el mismo SHA-256 que el entregable", rc == 0 and s_re == s_ent, f"{str(s_re)[:16]} / {s_ent[:16]}")
    chk("la referencia salió de este entregable", ref["sha256_origen"] == s_ent and ref["version"] == "V6.3.2 F1")
    lin = open(SHA_TXT, encoding="utf-8").read().split()
    chk("SHA256_entregables_V6.3.2_F1.txt coincide", s_ent in lin and "Plantilla_V6.3.2_F1.xlsx" in lin)
    f1, f = ref631["formulas"], ref["formulas"]
    alteradas = {k for k in f1 if k in f and f1[k] != f[k]}
    quitadas = set(f1) - set(f)
    nuevas = set(f) - set(f1)
    prev_alt = {f"Historia!{c}30" for c in COLS} | {"Historia!C53", "Historia!C58", "Historia!C76", "Motor!E205", "Panel!A1"}
    prev_new = {f"Historia!{c}{r}" for c in COLS for r in (95, 96)} | {"Historia!C97"}
    chk("frente a la V6.3.1: fórmulas alteradas = fila 30, C53, C58, C76, Motor E205 y Panel A1 (y ninguna más)", alteradas == prev_alt,
        f"de más {sorted(alteradas - prev_alt)[:5]} · de menos {sorted(prev_alt - alteradas)[:5]}")
    chk("ninguna fórmula de la V6.3.1 quitada", not quitadas, str(sorted(quitadas)[:5]))
    chk("fórmulas nuevas = Historia C95:L95 (excluido), C96:L96 (circulante de la reinversión) y C97 (normalización efectiva)", nuevas == prev_new,
        str(sorted(nuevas ^ prev_new)[:5]))
    ning = '=IF($C$97="ninguna",'
    for c in ("C53", "C58", "C76"):
        chk(f"Historia {c}: con «ninguna» la fórmula de la V6.3.1 F1 literal (y con ella, con A0, la de la V6.3)", f[f"Historia!{c}"].startswith(ning + f1[f"Historia!{c}"][1:] + ","))
    chk("fila 30: la de la V6.3.1 con el circulante de la fila 96 en lugar del de la fila 14",
        all(f[f"Historia!{c}30"] == f1[f"Historia!{c}30"].replace(f"N({c}14)", f"N({c}96)") for c in COLS))
    chk("C58 con «circulante_a_cero»: exige normalizados todos los años de la ventana (C94:L94 = 1) antes de la rama de D_X de la V6.3.1",
        f'IF($C$97="{REGLA}",IF(NOT(ISNUMBER($C$57)),"",IF(SUMPRODUCT(--(COLUMN($C$6:$L$6)>12-$C$57),--($C$94:$L$94<>1))>0,"",' in f["Historia!C58"])
    chk("C53 con «circulante_a_cero»: los cinco años H–L de las filas 12, 13, 14 y 88 y normalizados los cinco (no se mezclan)",
        "COUNT($H$88:$L$88)<5,SUMPRODUCT(--($H$94:$L$94=1))<5)" in f["Historia!C53"])
    o, nw = f1["Motor!E205"], f["Motor!E205"]
    i = o.rfind('en algún año de la ventana","")') + len('en algún año de la ventana",')
    pre, suf = o[:i], o[i + 2:]
    medio = nw[len(pre):len(nw) - len(suf)] if nw.startswith(pre) and nw.endswith(suf) else ""
    chk("Motor E205: la de la V6.3.1 más dos causas al final (normalización no reconocida: INV; ventana sin normalizar: INC) en lugar del último «»",
        medio.startswith('IF(Historia!$C$97="no reconocida","INV|') and medio.endswith('",""))') and "INC|Motor A · normalización del circulante" in medio
        and medio.count("Historia!$C$97") == 2, medio[:90])
    x1, x = ref631["fijos"], ref["fijos"]
    alt_f = {k for k in x1 if k in x and x1[k] != x[k]}
    chk("celdas fijas alteradas = tres etiquetas de versión", alt_f == {"Análisis!A1", "Guía V6!A1", "Control maestro!A3"}, str(sorted(alt_f)))
    chk("ninguna celda fija de la V6.3.1 quitada", not (set(x1) - set(x)))
    nf = set(x) - set(x1)
    chk("celdas fijas nuevas solo en la sección nueva (Historia filas 92–98)", nf and all(k.startswith("Historia!") and 92 <= _fila(k) <= 98 for k in nf), f"{len(nf)} celdas")
    chk("mismas hojas, formato condicional, nombres definidos y partes del paquete que la V6.3.1 (y la V6.3)",
        ref["hojas"] == ref631["hojas"] and ref["formato_condicional"] == ref631["formato_condicional"] and ref["nombres_definidos"] == ref631["nombres_definidos"]
        and ref["partes_paquete"] == ref631["partes_paquete"] == ref63["partes_paquete"], f"{len(ref['partes_paquete'])} partes")
    v1, v = ref631["validaciones"], ref["validaciones"]
    dv_nuevas = [d for d in v["Historia"] if d not in v1["Historia"]]
    chk("validaciones: solo dos nuevas en la Historia (lista de la regla en C93; 1 o vacío en C94:L94)",
        all(v[h] == v1[h] for h in v1 if h != "Historia") and all(d in v["Historia"] for d in v1["Historia"]) and sorted(d[0] for d in dv_nuevas) == ["C93", "C94:L94"],
        str(dv_nuevas))
    e1, e = ref631["entradas"], ref["entradas"]
    chk("inventario de entradas: el de la V6.3.1 F1 más Historia C93, C94:L94 y M93:S94",
        {h: r for h, r in e.items() if h != "Historia"} == {h: r for h, r in e1.items() if h != "Historia"} and e["Historia"] == e1["Historia"] + ["C93", "C94:L94", "M93:S94"],
        str(e["Historia"]))
    ver = os.path.join(AQUI, "verificar_v632.py")
    rc, txt = run([PY, "-I", ver, PLANTILLA, REF])
    chk("verificar_v632.py: la plantilla es ÍNTEGRA frente a su referencia", rc == 0 and "ÍNTEGRO · 0 fallos" in txt, txt.splitlines()[-1])
    rc, txt = run([PY, "-I", os.path.join(V631, "scripts", "verificar_v631.py"), PLANTILLA, REF_V631])
    chk("verificar_v631.py (V6.3.1) rechaza la V6.3.2: una plantilla no pasa por la otra", rc == 1, (txt.splitlines() or [""])[1])
    rc, txt = run([PY, "-I", os.path.join(V631, "scripts", "verificar_v631.py"), PLANTILLA_V631, REF_V631])
    chk("verificar_v631.py sigue aceptando la V6.3.1 F1", rc == 0 and "ÍNTEGRO · 0 fallos" in txt)
    with tempfile.TemporaryDirectory() as tmp:
        sys.path.insert(0, os.path.join(PV, "scripts"))
        from v63_xml import LibroV63
        from trasladar_entradas import escribir_formula
        for celda, formula, nombre in (("H96", "H14", "el circulante de la reinversión sin normalizar (H96 = H14)"),
                                       ("C97", '"circulante_a_cero"', "la normalización efectiva fija (C97 = «circulante_a_cero»)")):
            lb = LibroV63(PLANTILLA)
            escribir_formula(lb, "Historia", celda, formula)
            m = os.path.join(tmp, f"mut_{celda}.xlsx")
            lb.guardar(m)
            rc, txt = run([PY, "-I", ver, m, REF])
            chk(f"verificar_v632.py rechaza una mutación: {nombre}", rc == 1 and f"Historia!{celda}" in txt, (txt.splitlines() or [""])[1])


# ------------------------------------------------------------------------------------------------------------------ LibreOffice
def recalc(libro, dest):
    perfil = os.path.join(dest, "_perfil_lo")
    out = os.path.join(dest, "recalc")
    rc, txt = run(["bash", RECALC, libro, out, perfil])
    r = os.path.join(out, os.path.basename(libro))
    if rc != 0 or not os.path.exists(r):
        raise SystemExit(f"LibreOffice no recalculó {libro}: {txt[-300:]}")
    return r


def _modulo(nombre, carpeta):
    """Importa un módulo de una carpeta concreta (trasladar_entradas y comparar_libros existen con el mismo nombre en la V6.3.1 y la V6.3.2)."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(f"{nombre}_{os.path.basename(os.path.dirname(carpeta))}", os.path.join(carpeta, f"{nombre}.py"))
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, carpeta)
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path.remove(carpeta)
    return m


T632 = None


def preparar(origen, plantilla, salida, otras=None):
    """Traslada las entradas (con el inventario de la V6.3.2, que contiene el de la V6.3.1 y el de la V6.3) y vacía las celdas de entrada que el origen
    tiene vacías y la plantilla trae con un texto de ayuda. La misma vía para las tres plantillas."""
    global T632
    T632 = T632 or _modulo("trasladar_entradas", AQUI)
    sys.path.insert(0, os.path.join(PV, "scripts"))
    from v63_xml import LibroV63
    src, pl = LibroV63(origen), LibroV63(plantilla)
    vaciar = {}
    for hoja, refs in T632.INV.conjunto_entradas().items():
        if hoja not in src.hojas():
            continue
        vs, vp = src.todas_las_celdas(hoja), pl.todas_las_celdas(hoja)
        for r in refs:
            if vs.get(r) is None and vp.get(r) is not None and not (isinstance(vp[r], tuple) and vp[r][:1] == ("=",)):
                vaciar[f"{hoja}!{r}"] = None
    if plantilla != PLANTILLA:   # la sección de la V6.3.2 no existe en las otras: no se escribe en ellas
        vaciar = {k: v for k, v in vaciar.items() if not (k.startswith("Historia!") and 91 <= _fila(k) <= 98)}
    return T632.trasladar(origen, plantilla, salida, {**vaciar, **(otras or {})})


def _escribir_libro(libro, salida, celdas):
    sys.path.insert(0, os.path.join(PV, "scripts"))
    from v63_xml import LibroV63
    lb = LibroV63(libro)
    lb.escribir_celdas({k: ({"valor": v, "tipo": "texto"} if isinstance(v, str) else v) for k, v in celdas.items()})
    lb.borrar_caches()
    lb.guardar(salida)


def _nuevo(dest):
    if os.path.exists(dest):
        raise SystemExit(f"{dest} ya existe: las pruebas escriben en una carpeta nueva")
    if os.path.commonpath([os.path.abspath(dest), RAIZ]) == RAIZ:
        raise SystemExit("DESTINO va fuera del repositorio")
    os.makedirs(dest)


def _decl_elis(per, cif, RE, ELIS_DIR, TEXTOS):
    d = RE.declaracion(cif, True, False)
    d["perimetro_reinversion"] = {"valor": per, "registro": {"fecha": "2026-11-19", "persona": "prueba V6.3.2 F1 (no es una decisión)", "motivo": "caso de prueba del libro"}}
    for n_ in ("da_rou", "da_ppa"):
        for y_, e in d["series"][n_].items():
            e["fila"] = cif["series"][n_][y_]["etiqueta"]
    d["fuentes_series"] = {doc: {"archivo": os.path.join("texto", n_), "sha256": sha(os.path.join(ELIS_DIR, "texto", n_))} for doc, n_ in TEXTOS.items()}
    return d


def _elis():
    F1D = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_15", "f1_impl")
    sys.path.insert(0, os.path.join(F1D, "scripts"))
    import regresion_elis_f1 as RE
    cif = json.load(open(os.path.join(F1D, "datos", "elis_cifras_f1.json"), encoding="utf-8"))
    ELIS_DIR = os.path.dirname(ELIS)
    TEXTOS = {"URD2022": "Elis - 2022 Universal Registration Document.txt", "URD2023": "Elis_Universal Registration Document_2023_EN.txt",
              "DEU2024FR": "Elis_Document d'enregistrement universel_2024_FR.txt", "URD2025": "Elis - 2025 Universal Registration Document.txt"}
    return cif, RE, ELIS_DIR, TEXTOS


def a0(dest):
    sys.path.insert(0, os.path.join(PV, "scripts"))
    import f1_libro_v631 as F
    CL = _modulo("comparar_libros", AQUI)
    _nuevo(dest)
    chk("libro de Elis: el que concilió el frente E (d2593777…), sin cambios", sha(ELIS) == SHA_ELIS)
    cif, RE, ELIS_DIR, TEXTOS = _elis()
    casos = [("Elis", ELIS)] + [(os.path.basename(p).replace(".xlsx", ""), p) for p in EJEMPLOS]
    detalle = {}
    from openpyxl import load_workbook
    for nombre, origen in casos:
        h0 = sha(origen)
        variantes = [("vacio", None), ("A0", "A0_total")] + ([("A1", "A1_sin_ROU"), ("A2", "A2_propio")] if nombre == "Elis" else [])
        for etq, per in variantes:
            b631, b632 = (os.path.join(dest, f"{nombre}_{etq}_{s}.xlsx") for s in ("V6.3.1", "V6.3.2"))
            for pl, b in ((PLANTILLA_V631, b631), (PLANTILLA, b632)):
                base = b + ".entradas.xlsx"
                preparar(origen, pl, base)
                if per in ("A1_sin_ROU", "A2_propio"):
                    dp = os.path.join(dest, f"{nombre}_{etq}.motor_a_f1.json")
                    json.dump(_decl_elis(per, cif, RE, ELIS_DIR, TEXTOS), open(dp, "w", encoding="utf-8"), ensure_ascii=False)
                    F.aplicar(base, b, dp)
                else:
                    _escribir_libro(base, b, {"Historia!C85": per})
            rc, txt = run([PY, "-I", os.path.join(AQUI, "verificar_v632.py"), b632, REF])
            chk(f"{nombre} · {etq}: el libro V6.3.2 con las entradas es ÍNTEGRO frente a su referencia", rc == 0, txt.splitlines()[1])
            r631, r632 = recalc(b631, dest), recalc(b632, dest)
            d1, ncel = CL.comparar(r631, r632, tol=0)
            chk(f"{nombre} · {etq}: sin normalización, 0 celdas distintas frente a la V6.3.1 F1 (igualdad exacta)", not d1, f"{ncel} celdas · {len(d1)} distintas {d1[:3]}")
            wb = load_workbook(r632, data_only=True)
            hs = wb["Historia"]
            ok = hs["C97"].value == "ninguna" and all(hs[f"{c}95"].value == 0 for c in COLS) and all(
                (hs[f"{c}96"].value == hs[f"{c}14"].value) if isinstance(hs[f"{c}14"].value, (int, float)) else hs[f"{c}96"].value in (None, "") for c in COLS)
            chk(f"{nombre} · {etq}: C97 «ninguna», fila 95 = 0 y fila 96 = fila 14", ok, f"C97 {hs['C97'].value!r} · C58 {hs['C58'].value!r} · C53 {hs['C53'].value!r}")
            detalle[f"{nombre}_{etq}"] = {"origen": os.path.relpath(origen, RAIZ), "origen_sha256": h0, "celdas_comparadas": ncel, "distintas_frente_a_V6.3.1": len(d1),
                                          "C58": hs["C58"].value, "C53": hs["C53"].value, "C76": hs["C76"].value, "Motor_D205": wb["Motor"]["D205"].value}
            wb.close()
            if etq == "A0":
                b63 = os.path.join(dest, f"{nombre}_V6.3.xlsx")
                preparar(origen, PLANTILLA_V63, b63)
                d2, _ = CL.comparar(recalc(b63, dest), r632, tol=0, filas_nuevas=CL.FILAS_V631)
                chk(f"{nombre} · A0: 0 celdas distintas frente a la V6.3 (igualdad exacta)", not d2, f"{len(d2)} distintas {d2[:3]}")
                detalle[f"{nombre}_A0"]["distintas_frente_a_V6.3"] = len(d2)
        chk(f"{nombre}: el origen no cambia", sha(origen) == h0)
    shutil.rmtree(os.path.join(dest, "_perfil_lo"), ignore_errors=True)
    return detalle


VINCI_HISTORIA = (6, 7, 8, 10, 11, 12, 13, 14, 16, 17, 18, 23)


def _vinci_entradas():
    """Las cifras de VINCI (fijadas en pruebas/datos_circulante/vinci_libro_v631.json): la Historia que usan f, el ancla y K3a, C57, el FCF base
    (Análisis C46–C51) y el perímetro A2 con sus series. Se escriben sobre las entradas del ejemplo Empresa X (el resto: palancas, sector…)."""
    v = json.load(open(FIX_VINCI, encoding="utf-8"))["valores"]
    cel = {f"Historia!{c}5": v[f"Historia!{c}5"] for c in COLS}
    for fila in VINCI_HISTORIA:
        for c in COLS:
            cel[f"Historia!{c}{fila}"] = v.get(f"Historia!{c}{fila}")
    for c in COLS:   # el resto de la Historia de Empresa X no casa con las cifras de VINCI: se vacía lo que no sea de VINCI en las filas 15–26
        for fila in (15, 19, 20, 21, 22, 24, 25, 26):
            cel[f"Historia!{c}{fila}"] = v.get(f"Historia!{c}{fila}")
    cel["Historia!C57"] = v["Historia!C57"]
    for k in ("C46", "C47", "C48", "C49", "C50", "C51"):
        cel[f"Análisis!{k}"] = v[f"Análisis!{k}"]
    cel["Control maestro!L4"] = "IFRS"
    return cel, v


ROU_V = {2021: 605, 2022: 623, 2023: 668, 2024: 714, 2025: 817}
PPA_V = {2021: 0, 2022: 128, 2023: 128, 2024: 108, 2025: 38}
FUENTE_TXT = "fuente_tipo_vinci.txt"
FUENTE = "[PDF PAGE 1]\nInforme sintético (tipo Vinci): 605 623 668 714 817 0 128 108 38\n[PDF PAGE 2]\n"
REGP = {"fecha": "2026-11-19", "persona": "prueba V6.3.2 F1 (no es una decisión)", "motivo": "caso de prueba del libro"}
CONC = [{"componente": "C46", "importe": -2090.0, "partida": "entrada de caja del circulante excluida del CFO en C46", "fuente": {"documento": "sintético", "pagina": 1}},
        {"componente": "C46", "importe": 37.333333, "partida": "dividendos de no consolidadas", "fuente": {"documento": "sintético", "pagina": 1}},
        {"componente": "C47", "importe": -213.0, "partida": "cuentas a cobrar PPP", "fuente": {"documento": "sintético", "pagina": 1}},
        {"componente": "C47", "importe": 165.666667, "partida": "ventas de inmovilizado", "fuente": {"documento": "sintético", "pagina": 1}},
        {"componente": "C50", "importe": 119.333333, "partida": "SBC frente a la fila 18", "fuente": {"documento": "sintético", "pagina": 1}}]


def _decl_vinci(per="A2_propio", anios=(2021, 2022, 2023, 2024, 2025), con_norm=True):
    def serie(vals):
        return {str(y): {"valor_fuente": x, "signo": 1, "tratamiento": "ninguno", "documento": "sintético", "pagina": 1, "literal": str(x), "archivo": FUENTE_TXT}
                for y, x in vals.items()}
    d = {"norma_contable": {"valor": "NIIF", "registro": REGP}, "perimetro_reinversion": {"valor": per, "registro": REGP},
         "perimetro_margen": {"valor": "EBIT_NIIF16_PPA_constante", "registro": REGP}, "perimetro_palancas_s2c": {"valor": per, "registro": REGP},
         "perimetro_roic": {"valor": per, "registro": REGP}, "clasificacion_compras": {"valor": "crecimiento_por_hipotesis", "registro": REGP, "fundamento": "prueba"},
         "transicion": {"conocida": False, "tratamiento": None, "registro": REGP}, "series": {"da_rou": serie(ROU_V), "da_ppa": serie(PPA_V)},
         "conciliacion_fcf_base": copy.deepcopy(CONC),
         "fuentes_series": {"sintético": {"archivo": FUENTE_TXT, "sha256": hashlib.sha256(FUENTE.encode("utf-8")).hexdigest()}}}
    if con_norm:
        d["normalizacion_circulante"] = {"regla": REGLA, "anios": list(anios), "fundamento": "prueba: la caja base excluye el circulante (M43 en VINCI)", "registro": REGP}
    return d


def circ(dest):
    from openpyxl import load_workbook
    sys.path.insert(0, os.path.join(PV, "scripts"))
    import motor_a_f1 as M
    import f1_libro_v631 as F
    CL = _modulo("comparar_libros", AQUI)
    _nuevo(dest)
    open(os.path.join(dest, FUENTE_TXT), "w", encoding="utf-8").write(FUENTE)
    cel, vf = _vinci_entradas()
    # (revisión C1) el expediente sintético tipo VINCI: fase1_v63.json con el cálculo declarado de C46 (CFO + fila 14 + dividendos) y su texto
    sys.path.insert(0, os.path.join(PV, "pruebas", "datos_circulante"))
    import expediente_tipo_vinci as EXP
    EXP.escribir(dest, vf)
    detalle = {}
    bases = {}
    for pl, nom in ((PLANTILLA, "V6.3.2"), (PLANTILLA_V631, "V6.3.1")):
        b = os.path.join(dest, f"Vinci_tipo_{nom}_entradas.xlsx")
        preparar(EJEMPLOS[0], pl, b, cel)
        bases[nom] = b

    def libro(nombre, d, plantilla="V6.3.2", despues=None):
        dp = os.path.join(dest, f"{nombre}.motor_a_f1.json")
        json.dump(d, open(dp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        b = os.path.join(dest, f"{nombre}.xlsx")
        F.aplicar(bases[plantilla], b, dp)
        if despues:
            _escribir_libro(b, b + ".tmp.xlsx", despues)
            os.replace(b + ".tmp.xlsx", b)
        return recalc(b, dest)

    def evaluar(rec, d):
        return M.evaluar(M.leer_libro(rec), d, carpeta=dest)

    def salta(r, gid):
        return any(g["salta"] for g in r["guardas"] if g["id"] == gid)

    def bloquean(r):
        return sorted({g["id"] for g in r["guardas"] if g["salta"] and g["severidad"] == "BLOQUEA"})

    def flujos(mo):
        return {(esc, t): mo[f"{c}{fila}"].value for esc, fila in (("MALO", 6), ("NORMAL", 7), ("BUENO", 8))
                for t, c in enumerate(["AU", "AV", "AW", "AX", "AY", "AZ", "BA", "BB", "BC", "BD", "BF"])}

    # ---------------------------------------------------------------- C1 · normalización 2021–2025, libro = capa
    d1 = _decl_vinci()
    rec1 = libro("Vinci_tipo_norm", d1)
    wb = load_workbook(rec1, data_only=True)
    h, mo = wb["Historia"], wb["Motor"]
    r1 = evaluar(rec1, d1)
    cd = r1["calculo_perimetro_declarado"] or {}
    chk("C1 · Vinci tipo, normalización 2021–2025: C97 «circulante_a_cero», fila 95 = fila 14 en 2021–2025 (0 antes), fila 96 = 0, Motor V05 OK",
        h["C97"].value == REGLA and all(h[f"{c}95"].value == h[f"{c}14"].value and h[f"{c}96"].value == 0 for c in "HIJKL")
        and all(h[f"{c}95"].value == 0 for c in "CDEFG") and mo["D205"].value == "OK", f"V05 {mo['D205'].value!r} · {mo['F205'].value!r}"[:200])
    chk("C1 · libro = capa: f (C58) a 10⁻¹², ancla (C53) a 10⁻⁹ y reinversión media (C76) a 10⁻⁹; f ≈ 1,574 % y ancla ≈ 2,3226",
        abs(h["C58"].value - cd["f"]) <= 1e-12 and abs(h["C53"].value - cd["ancla_s2c_E4"]) <= 1e-9 and abs(h["C76"].value - cd["reinversion_media"]) <= 1e-9
        and abs(h["C58"].value - 0.0157439542) < 1e-9 and abs(h["C53"].value - 31365 / 13504) < 1e-9, f"C58 {h['C58'].value!r} · C53 {h['C53'].value!r} · C76 {h['C76'].value!r}")
    fl = flujos(mo)
    dev = max(abs(fl[(esc, t)] - (cd["escenarios"][esc]["anios_1_10"][t] if t < 10 else cd["escenarios"][esc]["anio_11"])) for esc, t in fl)
    chk("C1 · los 33 flujos del Motor (años 1–10 y 11, tres escenarios con las palancas del ejemplo) = capa (10⁻⁹)", dev <= 1e-9, f"desviación máxima {dev:.2e}")
    chk("C1 · F1-LIBRO, F1-REPLICA, F1-CIRC y F1-K3c no saltan; F1-LIBRO dice que el libro V6.3.2 calcula la normalización (33 flujos)",
        not any(salta(r1, x) for x in ("F1-LIBRO", "F1-REPLICA", "F1-CIRC", "F1-K3c")) and r1["libro_v631_f1"]["flujos_contrastados"] == 33
        and "V6.3.2 F1" in [g for g in r1["guardas"] if g["id"] == "F1-LIBRO"][0]["detalle"], str(bloquean(r1)))
    # ---------------------------------------------------------------- C2 · sin la normalización: la V6.3.1 exacta; K3c bloquea
    d2 = _decl_vinci(con_norm=False)
    rec2, rec2b = libro("Vinci_tipo_sin", d2), libro("Vinci_tipo_sin_v631", d2, plantilla="V6.3.1")
    dd, ncel = CL.comparar(rec2b, rec2, tol=0)
    chk("C2 · sin la normalización: el libro V6.3.2 es la V6.3.1 F1 con las mismas entradas (0 celdas distintas, igualdad exacta)", not dd, f"{ncel} celdas · {dd[:3]}")
    r2 = evaluar(rec2, d2)
    w2 = load_workbook(rec2, data_only=True)["Historia"]
    chk("C2 · sin la normalización K3c BLOQUEA (reinversión −1.514,333) y el libro y la capa coinciden (F1-LIBRO no salta)",
        salta(r2, "F1-K3c") and not salta(r2, "F1-LIBRO") and abs(w2["C76"].value + 1514.333333) < 1e-5, str(bloquean(r2)))
    S = sum(w2[f"{c}6"].value for c in "JKL") / 3
    mwc = sum(w2[f"{c}14"].value for c in "JKL") / 3
    chk("C1/C2 · identidad con los valores del libro: f normalizada = f − media del circulante de la ventana ÷ ventas medias (10⁻¹²)",
        abs(h["C58"].value - (w2["C58"].value + mwc / S)) <= 1e-12, f"{h['C58'].value!r} frente a {w2['C58'].value + mwc / S!r}")
    s31 = sum(w2[f"{c}31"].value for c in "HIJKL")
    s14 = sum(w2[f"{c}14"].value for c in "HIJKL")
    chk("C1/C2 · identidad: C53 normalizada = ΔV ÷ (Σ fila 31 sin normalizar − Σ fila 14 de H–L) (10⁻⁹)",
        abs(h["C53"].value - (w2["L6"].value - w2["G6"].value) / (s31 - s14)) <= 1e-9)
    detalle["Vinci_tipo"] = {"C58_normalizado": h["C58"].value, "C53_normalizado": h["C53"].value, "C76_normalizado": h["C76"].value, "C58_sin": w2["C58"].value,
                             "C53_sin": w2["C53"].value, "C76_sin": w2["C76"].value, "flujo_sin_crecimiento_capa": cd["flujo_sin_crecimiento"],
                             "bloquean_normalizado": bloquean(r1), "bloquean_sin": bloquean(r2)}
    wb.close()
    # ---------------------------------------------------------------- C3 · solo la ventana; C4 · sin un año de la ventana
    d3 = _decl_vinci(anios=(2023, 2024, 2025))
    rec3 = libro("Vinci_tipo_ventana", d3)
    w3 = load_workbook(rec3, data_only=True)["Historia"]
    r3 = evaluar(rec3, d3)
    chk("C3 · solo la ventana (2023–2025): f normalizada, C53 vacía en el libro y en la capa; F1-CIRC bloquea (INCOMPLETO) y F1-LIBRO no",
        abs(w3["C58"].value - h["C58"].value) <= 1e-15 and w3["C53"].value in (None, "") and r3["calculo_perimetro_declarado"]["ancla_s2c_E4"] is None
        and salta(r3, "F1-CIRC") and not salta(r3, "F1-LIBRO"), str(bloquean(r3)))
    d4 = _decl_vinci(anios=(2021, 2022, 2023, 2025))
    rec4 = libro("Vinci_tipo_sin_2024", d4)
    wb4 = load_workbook(rec4, data_only=True)
    r4 = evaluar(rec4, d4)
    chk("C4 · sin 2024 (ventana): f y C53 vacías, Motor V05 INCOMPLETO con su causa; la capa en pendiente_de_datos (F1-CIRC) sin error ni F1-REPLICA",
        wb4["Historia"]["C58"].value in (None, "") and wb4["Motor"]["D205"].value == "INCOMPLETO" and "normalización del circulante" in str(wb4["Motor"]["F205"].value)
        and r4["estado_propuesto"] == "pendiente_de_datos" and not salta(r4, "F1-REPLICA"), f"{wb4['Motor']['F205'].value!r}"[:160])
    # ---------------------------------------------------------------- C5 · regla y marca no reconocidas
    for nombre, despues in (("regla", {"Historia!C93": "otra_regla"}), ("marca", {"Historia!K94": 2})):
        rec5 = libro(f"Vinci_tipo_no_reconocida_{nombre}", d1, despues=despues)
        wb5 = load_workbook(rec5, data_only=True)
        r5 = evaluar(rec5, d1)
        chk(f"C5 · {nombre} no reconocida: C97 «no reconocida», f y C53 vacías, Motor V05 DATOS INVÁLIDOS; la capa bloquea (F1-LIBRO) sin F1-REPLICA",
            wb5["Historia"]["C97"].value == "no reconocida" and wb5["Historia"]["C58"].value in (None, "") and wb5["Historia"]["C53"].value in (None, "")
            and wb5["Motor"]["D205"].value == "DATOS INVÁLIDOS" and salta(r5, "F1-LIBRO") and not salta(r5, "F1-REPLICA"), str(bloquean(r5)))
    # ---------------------------------------------------------------- C6 · A0 con la normalización
    d6 = _decl_vinci(per="A0_total")
    rec6 = libro("Vinci_tipo_A0_norm", d6)
    w6 = load_workbook(rec6, data_only=True)["Historia"]
    r6 = evaluar(rec6, d6)
    cd6 = r6["calculo_perimetro_declarado"] or {}
    chk("C6 · A0_total con la normalización: el libro usa la rama de D_X con la fila 30 normalizada; f y ancla = capa; réplica conforme",
        abs(w6["C58"].value - cd6["f"]) <= 1e-12 and abs(w6["C53"].value - cd6["ancla_s2c_E4"]) <= 1e-9 and not salta(r6, "F1-REPLICA")
        and r6["libro_v631_f1"]["motivos"] == [], str(bloquean(r6)))
    # ---------------------------------------------------------------- C7 · V6.3.1 con la normalización declarada
    rec7 = libro("Vinci_tipo_v631_norm", d1, plantilla="V6.3.1")
    r7 = evaluar(rec7, d1)
    chk("C7 · libro V6.3.1 con la normalización declarada: F1-LIBRO bloquea (límite declarado: la salida es la V6.3.2 F1) y la capa da las cifras normalizadas",
        salta(r7, "F1-LIBRO") and "V6.3.2 F1" in [g for g in r7["guardas"] if g["id"] == "F1-LIBRO"][0]["detalle"]
        and abs(r7["calculo_perimetro_declarado"]["f"] - cd["f"]) <= 1e-15 and not salta(r7, "F1-REPLICA"), str(bloquean(r7)))
    # ---------------------------------------------------------------- C8 · Elis (caja base con el circulante)
    if sha(ELIS) == SHA_ELIS:
        cif, RE, ELIS_DIR, TEXTOS = _elis()
        de = _decl_elis("A2_propio", cif, RE, ELIS_DIR, TEXTOS)
        de["normalizacion_circulante"] = {"regla": REGLA, "anios": [2021, 2022, 2023, 2024, 2025], "fundamento": "prueba (Elis no excluye el circulante de su caja base)",
                                          "registro": REGP}
        be = os.path.join(dest, "Elis_entradas.xlsx")
        preparar(ELIS, PLANTILLA, be)
        dp = os.path.join(dest, "Elis_norm.motor_a_f1.json")
        json.dump(de, open(dp, "w", encoding="utf-8"), ensure_ascii=False)
        F.aplicar(be, os.path.join(dest, "Elis_norm.xlsx"), dp)
        rece = recalc(os.path.join(dest, "Elis_norm.xlsx"), dest)
        we = load_workbook(rece, data_only=True)["Historia"]
        re_ = M.evaluar(M.leer_libro(rece), de, carpeta=ELIS_DIR)
        cde = re_["calculo_perimetro_declarado"] or {}
        chk("C8 · Elis (su caja base NO excluye el circulante) con la normalización: el libro la calcula (= capa) y la capa bloquea con F1-CIRC DATOS INVÁLIDOS",
            we["C97"].value == REGLA and abs(we["C58"].value - cde["f"]) <= 1e-12 and any(g["salta"] and g["efecto"] == "DATOS INVÁLIDOS" for g in re_["guardas"] if g["id"] == "F1-CIRC")
            and not salta(re_, "F1-LIBRO") and not salta(re_, "F1-REPLICA"), str(bloquean(re_)))
    else:
        chk("C8 · libro de Elis d2593777… materializado", False, sha(ELIS)[:16])
    # ---------------------------------------------------------------- C9 · (revisión C1) la sonda del revisor en un libro V6.3.2 recalculado
    d9 = _decl_vinci()
    d9["conciliacion_fcf_base"].append({"componente": "C46", "importe": 2090.0, "partida": "compensación", "fuente": {"documento": "x", "pagina": 1}})
    rec9 = libro("Vinci_tipo_compensadas", d9, despues={"Análisis!C46": 11417.333})
    w9 = load_workbook(rec9, data_only=True)
    r9 = evaluar(rec9, d9)
    g9 = [g for g in r9["guardas"] if g["id"] == "F1-CIRC"]
    chk("C9 · (C1) caja base CON el circulante (C46 = 11.417,333) y dos partidas C46 que se compensan (−2.090 y +2.090, documento «x»): el libro calcula "
        "la normalización (f −1,34 % = capa) y la capa bloquea con F1-CIRC DATOS INVÁLIDOS (el cálculo declarado de C46 da 9.327,333), y solo con él",
        w9["Historia"]["C97"].value == REGLA and abs(w9["Historia"]["C58"].value - r9["calculo_perimetro_declarado"]["f"]) <= 1e-12
        and abs(w9["Historia"]["C58"].value + 0.013411) < 1e-5 and abs(w9["Análisis"]["C52"].value - 6509.333) < 1e-6 and bloquean(r9) == ["F1-CIRC"]
        and g9 and g9[0]["efecto"] == "DATOS INVÁLIDOS" and "9327.333" in g9[0]["detalle"] and not salta(r9, "F1-K3a") and not salta(r9, "F1-K3c")
        and r9["utilizable_para_conclusion"] is False, f"{bloquean(r9)} · C58 {w9['Historia']['C58'].value!r} · {(g9[0]['detalle'] if g9 else '')[:140]}")
    detalle["sonda_C1"] = {"C58": w9["Historia"]["C58"].value, "C52": w9["Análisis"]["C52"].value, "bloquean": bloquean(r9),
                           "F1_CIRC": g9[0]["detalle"][:400] if g9 else None}
    w9.close()
    rc, txt = run([PY, "-I", os.path.join(AQUI, "verificar_v632.py"), os.path.join(dest, "Vinci_tipo_norm.xlsx"), REF])
    chk("C1 · el libro con la normalización aplicada (antes de recalcular) es ÍNTEGRO frente a la referencia: C93:L94 son entradas", rc == 0, txt.splitlines()[1])
    shutil.rmtree(os.path.join(dest, "_perfil_lo"), ignore_errors=True)
    return detalle


def escribir(nombre, extra=None):
    ok = all(r["ok"] for r in RES)
    out = {"prueba": nombre, "fecha": dt.date.today().isoformat(), "plantilla_sha256": sha(PLANTILLA), "referencia_sha256": sha(REF),
           "resultado": "PASA" if ok else "FALLA", "total": len(RES), "pasan": sum(r["ok"] for r in RES), "comprobaciones": RES}
    if extra is not None:
        out["detalle"] = extra
    d = os.path.join(V632, "pruebas")
    os.makedirs(d, exist_ok=True)
    json.dump(out, open(os.path.join(d, f"resultado_{nombre}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Pruebas V6.3.2 F1 · {nombre}", "", f"Fecha {out['fecha']} · plantilla `{out['plantilla_sha256'][:16]}…` · referencia `{out['referencia_sha256'][:16]}…`", "",
          f"**{out['resultado']}: {out['pasan']}/{out['total']}**", "", "| Comprobación | Resultado | Detalle |", "|---|---|---|"]
    md += [f"| {r['prueba']} | {'PASA' if r['ok'] else 'FALLA'} | {str(r['detalle']).replace('|', '/')[:300]} |" for r in RES]
    open(os.path.join(d, f"resultado_{nombre}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print(f"{out['pasan']}/{out['total']} comprobaciones V6.3.2 F1 ({nombre}) {'PASAN' if ok else 'FALLAN'}")
    return 0 if ok else 1


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ("estructura", "a0", "circ"):
        print(__doc__)
        sys.exit(2)
    if sys.argv[1] == "estructura":
        estructura()
        sys.exit(escribir("estructura"))
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    det = (a0 if sys.argv[1] == "a0" else circ)(sys.argv[2])
    sys.exit(escribir(sys.argv[1], det))
