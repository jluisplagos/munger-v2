"""Revisión independiente n.º 8 · reproducción de las cifras que declara el autor sobre C16/C17 (frente E · F1 · Elis).

Trabaja sobre una COPIA temporal de la carpeta del autor (no escribe en su worktree). Pasos:
  1. manifiesto de la carpeta (sha256sum -c);
  2. CSV regenerado desde los PDF (especificacion_cifras.py) frente a datos/cifras_fuente.csv;
  3. cadena del informe §13, sin LibreOffice (prueba_caja_no_nula.py no se repite: se usa su salida guardada), y cada
     salida frente a la que guarda el autor, byte a byte; composición del test del verificador (OK / PENDIENTE / FALLO
     esperados), contada en su registro;
  4. el verificador de C14 (carpeta --c14, worktree de C15) sobre el mismo CSV: su JSON frente al de C16 (la «salida
     idéntica a la de C14») y frente al que guarda C15;
  5. sondas de metadatos frente a resultados/sondas_metadatos_C16.json;
  6. referencia de E9 (`referencia_especificacion` de contraste_f1.json) en C15 y en C17, y el recuento nuevo
     `detecta_desde_unidades`.

Uso:
  python3 -I reproduccion_8.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis de C17> \
      --c14 <carpeta frente_E_F1_elis de C15> --trabajo <carpeta temporal>
"""
import argparse
import csv
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

LIBRO_REL = "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx"


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def correr(args, cwd):
    t0 = time.time()
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr, time.time() - t0


def igual(a, b):
    a, b = Path(a), Path(b)
    return a.is_file() and b.is_file() and a.read_bytes() == b.read_bytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--c14", required=True, type=Path)
    ap.add_argument("--trabajo", required=True, type=Path)
    a = ap.parse_args()
    py = [sys.executable, "-I"]
    libro = a.raiz / LIBRO_REL
    out = []

    def p(*x):
        s = " ".join(str(v) for v in x)
        out.append(s)
        print(s, flush=True)

    p("# Reproducción n.º 8 · carpeta del autor:", a.autor.name, "· versión de pdftotext:",
      subprocess.run(["pdftotext", "-v"], capture_output=True, text=True).stderr.splitlines()[0])
    # 1. manifiesto
    r = subprocess.run(["sha256sum", "-c", "MANIFIESTO_SHA256.txt"], cwd=a.autor, capture_output=True, text=True)
    lin = [l for l in r.stdout.splitlines() if l.strip()]
    p(f"1. Manifiesto: {sum(1 for l in lin if l.endswith(': OK'))} de {len(lin)} OK (código {r.returncode})")
    p(f"   libro {sha(libro)}")

    cop = a.trabajo / "copia_autor"
    if cop.exists():
        shutil.rmtree(cop)
    shutil.copytree(a.autor, cop)
    sc = cop / "scripts"

    # 2. CSV regenerado
    reg = a.trabajo / "cifras_regenerado.csv"
    cod, so, se, dt = correr(py + ["especificacion_cifras.py", "--raiz", str(a.raiz), "--fuentes", "../datos/fuentes.json", "--salida", str(reg)], sc)
    with reg.open(encoding="utf-8", newline="") as f:
        filas = sum(1 for _ in csv.DictReader(f, delimiter=";"))
    p(f"2. CSV regenerado desde los PDF: código {cod}, {filas} filas, SHA-256 {sha(reg)[:8]}…{sha(reg)[-4:]} · "
      f"{'IDÉNTICO' if igual(reg, a.autor / 'datos/cifras_fuente.csv') else 'DISTINTO'} al del autor ({dt:.0f} s)")
    tipos = {}
    with reg.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            tipos[fila["tipo"]] = tipos.get(fila["tipo"], 0) + 1
    p(f"   por tipo: {tipos}")

    # 3. cadena del §13
    p("3. Cadena del informe §13 (sobre la copia)")
    cod, so, se, dt = correr(py + ["verificar_cifras.py", "--raiz", str(a.raiz), "--datos", "../datos/cifras_fuente.csv", "--fuentes", "../datos/fuentes.json",
                                   "--salida", "../resultados/verificacion_cifras.json", "--exportar-paginas", "../evidencias/paginas"], sc)
    v = json.loads((cop / "resultados/verificacion_cifras.json").read_text(encoding="utf-8"))
    rs = v["resumen"]
    p(f"   verificar_cifras.py: código {cod}; filas {rs['filas']}, OK {rs['ok']}, PENDIENTE {rs['pendientes']}, FALLO {rs['fallos']} ({dt:.0f} s)")
    p(f"     JSON {'IDÉNTICO' if igual(cop / 'resultados/verificacion_cifras.json', a.autor / 'resultados/verificacion_cifras.json') else 'DISTINTO'} al guardado; "
      f"registro (salida estándar) {'IDÉNTICO' if so == (a.autor / 'resultados/verificar_cifras.log').read_text(encoding='utf-8') else 'DISTINTO'} a verificar_cifras.log")
    pags = sorted((a.autor / "evidencias/paginas").glob("*.txt"))
    dist = [x.name for x in pags if not igual(x, cop / "evidencias/paginas" / x.name)]
    nuevas = [x.name for x in (cop / "evidencias/paginas").glob("*.txt") if not (a.autor / "evidencias/paginas" / x.name).is_file()]
    p(f"     páginas exportadas: {len(pags)} guardadas, {len(dist)} distintas, {len(nuevas)} de más")
    pend = sorted({(r_["doc"], r_["pagina"]) for r_ in v["cifras"] if r_["estado"] == "PENDIENTE"})
    p(f"     PENDIENTE por página: {pend}")
    p(f"     por dimensión: {json.dumps(rs['por_dimension'], ensure_ascii=False)}")

    cod, so, se, dt = correr(py + ["test_verificar_cifras.py", "--raiz", str(a.raiz)], sc)
    guard = (a.autor / "resultados/test_verificar_cifras.log").read_text(encoding="utf-8")
    ult = so.strip().splitlines()[-1] if so.strip() else ""
    esperados = {}
    for l in so.splitlines():
        m = re.match(r"^(OK|MAL)\s.*→ (OK|PENDIENTE|FALLO)\s*$", l)
        if m:
            esperados[(m.group(1), m.group(2))] = esperados.get((m.group(1), m.group(2)), 0) + 1
    p(f"   test_verificar_cifras.py: código {cod}; «{ult}»; registro {'IDÉNTICO' if so == guard else 'DISTINTO'} al guardado ({dt:.0f} s)")
    p(f"     composición (resultado del caso, estado esperado): {sorted(esperados.items())}")

    cod, so, se, dt = correr(py + ["contraste_f1.py", "--cifras", "../datos/cifras_fuente.csv", "--verificacion", "../resultados/verificacion_cifras.json",
                                   "--libro", str(libro), "--caja-no-nula", "../resultados/caja_no_nula.json", "--salida", "../resultados/contraste_f1.json",
                                   "--informe", "../resultados/contraste_f1.md"], sc)
    c = json.loads((cop / "resultados/contraste_f1.json").read_text(encoding="utf-8"))
    res = c.get("resumen", {})
    p(f"   contraste_f1.py: código {cod}; comprobaciones {res.get('comprobaciones')}, fallidas {res.get('fallidas')}, por clase {res.get('por_clase')}, "
      f"entradas {res.get('entradas_usadas')} ({dt:.0f} s)")
    p(f"     JSON {'IDÉNTICO' if igual(cop / 'resultados/contraste_f1.json', a.autor / 'resultados/contraste_f1.json') else 'DISTINTO'}; "
      f"tabla {'IDÉNTICA' if igual(cop / 'resultados/contraste_f1.md', a.autor / 'resultados/contraste_f1.md') else 'DISTINTA'}; "
      f"registro {'IDÉNTICO' if so == (a.autor / 'resultados/contraste_f1.log').read_text(encoding='utf-8') else 'DISTINTO'}")

    cod, so, se, dt = correr(py + ["test_contraste_residuos.py", "--libro", str(libro)], sc)
    ult = so.strip().splitlines()[-1] if so.strip() else ""
    p(f"   test_contraste_residuos.py: código {cod}; «{ult}»; registro "
      f"{'IDÉNTICO' if so == (a.autor / 'resultados/test_contraste_residuos.log').read_text(encoding='utf-8') else 'DISTINTO'} ({dt:.0f} s)")

    cod, so, se, dt = correr(py + ["cobertura_por_mutacion.py", "--libro", str(libro)], sc)
    p(f"   cobertura_por_mutacion.py: código {cod}; salida {'IDÉNTICA' if so == (a.autor / 'resultados/cobertura_por_mutacion.txt').read_text(encoding='utf-8') else 'DISTINTA'} ({dt:.0f} s)")
    for l in so.splitlines()[:8]:
        p("     " + l.strip())

    cod, so, se, dt = correr(py + ["tabla_conciliacion.py", "--cifras", "../datos/cifras_fuente.csv", "--salida", "../resultados/tabla_conciliacion.md"], sc)
    p(f"   tabla_conciliacion.py: código {cod}; tabla {'IDÉNTICA' if igual(cop / 'resultados/tabla_conciliacion.md', a.autor / 'resultados/tabla_conciliacion.md') else 'DISTINTA'}")

    # 4. verificador de C14 sobre el mismo CSV
    p("4. Verificador de C14 (worktree de C15) sobre el mismo CSV")
    s14 = a.trabajo / "verificacion_c14.json"
    cod, so14, se, dt = correr(py + [str(a.c14 / "scripts/verificar_cifras.py"), "--raiz", str(a.raiz), "--datos", str(a.autor / "datos/cifras_fuente.csv"),
                                     "--fuentes", str(a.autor / "datos/fuentes.json"), "--salida", str(s14)], a.trabajo)
    p(f"   código {cod}; JSON de C14 {'IDÉNTICO' if igual(s14, cop / 'resultados/verificacion_cifras.json') else 'DISTINTO'} al de C16 recién generado; "
      f"{'IDÉNTICO' if igual(s14, a.c14 / 'resultados/verificacion_cifras.json') else 'DISTINTO'} al que guarda C15; "
      f"CSV de C15 {'IDÉNTICO' if igual(a.c14 / 'datos/cifras_fuente.csv', a.autor / 'datos/cifras_fuente.csv') else 'DISTINTO'} al de C17")
    v14 = json.loads(s14.read_text(encoding="utf-8"))
    dif = 0
    for x, y in zip(v14["cifras"], v["cifras"]):
        if x != y:
            dif += 1
    p(f"   filas con algún campo distinto entre C14 y C16 (estado, detalle de las seis dimensiones, línea, token): {dif} de {len(v['cifras'])}")

    # 5. sondas
    p("5. Sondas de metadatos")
    ss = a.trabajo / "sondas_C16.json"
    cod, so, se, dt = correr(py + ["sondas_metadatos.py", "--raiz", str(a.raiz), "--autor", str(cop), "--etiqueta", "C16 (commit que contiene este archivo)", "--salida", str(ss)], sc)
    for l in so.splitlines():
        p("   " + l)
    p(f"   JSON {'IDÉNTICO' if igual(ss, a.autor / 'resultados/sondas_metadatos_C16.json') else 'DISTINTO'} al guardado ({dt:.0f} s)")

    # 6. referencia de E9 y recuento nuevo
    p("6. Referencia de E9 y recuento nuevo del contraste")
    c14 = json.loads((a.c14 / "resultados/contraste_f1.json").read_text(encoding="utf-8"))
    for k in ("referencia_especificacion",):
        p(f"   {k}: {'IGUAL' if c14.get(k) == c.get(k) else 'DISTINTA'} en C15 y en C17 ({len(json.dumps(c.get(k)))} caracteres)")
    claves14, claves16 = set(c14), set(c)
    p(f"   claves de primer nivel solo en C17: {sorted(claves16 - claves14)}; solo en C15: {sorted(claves14 - claves16)}")
    cambiadas = [k for k in sorted(claves14 & claves16) if c14[k] != c[k]]
    p(f"   claves de primer nivel con contenido distinto: {cambiadas}")
    t14, t16 = c14.get("tablas", {}), c.get("tablas", {})
    p(f"   tablas con contenido distinto: {[k for k in sorted(set(t14) | set(t16)) if t14.get(k) != t16.get(k)]}")
    p(f"   comprobaciones: {'IGUALES' if c14.get('comprobaciones') == c.get('comprobaciones') else 'DISTINTAS'} ({len(c.get('comprobaciones', []))})")
    ce14, ce16 = t14.get("cobertura_entradas", {}), t16.get("cobertura_entradas", {})
    for k in sorted(set(ce14) | set(ce16)):
        if ce14.get(k) != ce16.get(k):
            if k == "entradas":
                e14, e16 = ce14[k], ce16[k]
                solo_campo = all({kk for kk in set(e14[i]) ^ set(e16[i])} <= {"detecta_desde_unidades"} and
                                 all(e14[i][kk] == e16[i][kk] for kk in e14[i]) for i in e16)
                p(f"   cobertura_entradas.entradas: {len(e16)} entradas; la única diferencia es el campo nuevo «detecta_desde_unidades»: {solo_campo}")
            else:
                p(f"   cobertura_entradas.{k}: distinto · C15: {json.dumps(ce14.get(k), ensure_ascii=False)[:300]}")
                p(f"   {'':24} C17: {json.dumps(ce16.get(k), ensure_ascii=False)[:600]}")
    (a.trabajo / "reproduccion_8.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
