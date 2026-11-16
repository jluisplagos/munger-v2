"""Revisión independiente n.º 9 · reproducción de las cifras que declara el autor sobre C18/C19 (frente E · F1 · Elis).

No escribe en el worktree del autor: copia su carpeta a --trabajo y ejecuta allí. Pasos:
  1. manifiesto de la carpeta congelada (sha256sum -c) y huella del libro;
  2. CSV regenerado desde los PDF (especificacion_cifras.py) frente a datos/cifras_fuente.csv;
  3. cadena del informe §13 sin LibreOffice (se usa la salida guardada de prueba_caja_no_nula.py) y cada salida frente a
     la guardada, byte a byte;
  4. el verificador de C16 (carpeta --c16, worktree de C17) sobre el mismo CSV: su JSON frente al de C18, fila a fila, y
     las páginas exportadas («salida idéntica a la de C16»);
  5. el test del verificador de C18: casos y comprobaciones directas, su composición, y el MISMO test con el verificador
     de C16 y con el de d3c0f1b (--d3c0f1b: archivo verificar_cifras.py de ese commit), para lo que declara la octava parte
     («con el verificador de C16, 119/136 y 4/9; con el de d3c0f1b, 134/136 y 8/9»);
  6. sondas de metadatos frente a resultados/sondas_metadatos_C18.json;
  7. contraste: JSON, tabla y registro de C19 frente a los de C17, y `referencia_especificacion` (E9);
  8. el barrido del autor (barrido_fecha_rotulo.py con --anterior C16) frente a resultados/barrido_fecha_rotulo.txt.

Uso:
  python3 -I -B reproduccion_9.py --raiz <ruta>/munger_v2_r1 --autor <carpeta frente_E_F1_elis de C19> \
      --c16 <carpeta frente_E_F1_elis de C17> --d3c0f1b <verificar_cifras.py de d3c0f1b> --trabajo <carpeta temporal>
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
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def correr(args, cwd):
    t0 = time.time()
    r = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr, time.time() - t0


def mismo(a, b):
    a, b = Path(a), Path(b)
    return a.is_file() and b.is_file() and a.read_bytes() == b.read_bytes()


def si(c, ok="IDÉNTICO", mal="DISTINTO"):
    return ok if c else mal


def resumen_test(so):
    """(casos bien, casos, directas bien, directas, composición por estado esperado, nombres de lo que falla)."""
    casos = re.search(r"^(\d+)/(\d+) casos con el resultado esperado", so, re.M)
    direc = re.search(r"^(\d+)/(\d+) comprobaciones directas", so, re.M)
    comp, mal, en_casos = {}, [], True
    for l in so.splitlines():
        if re.match(r"^\d+/\d+ casos", l):
            en_casos = False
        m = re.match(r"^(OK |MAL)\s*(.*)$", l)
        if not m:
            continue
        if m.group(1) == "MAL":
            mal.append(("caso: " if en_casos else "directa: ") + m.group(2)[:150])
        if en_casos:
            e = re.search(r"→ (OK|PENDIENTE|FALLO)\s*$", l)
            if e:
                comp[e.group(1)] = comp.get(e.group(1), 0) + 1
    return (tuple(int(x) for x in casos.groups()) if casos else None, tuple(int(x) for x in direc.groups()) if direc else None, comp, mal)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--c16", required=True, type=Path)
    ap.add_argument("--d3c0f1b", required=True, type=Path)
    ap.add_argument("--trabajo", required=True, type=Path)
    a = ap.parse_args()
    py = [sys.executable, "-I", "-B"]
    libro = a.raiz / LIBRO_REL
    out = []

    def p(*x):
        s = " ".join(str(v) for v in x)
        out.append(s)
        print(s, flush=True)

    a.trabajo.mkdir(parents=True, exist_ok=True)
    p("# Reproducción n.º 9 · carpeta del autor:", a.autor.name, "·",
      subprocess.run(["pdftotext", "-v"], capture_output=True, text=True).stderr.splitlines()[0], "· Python", sys.version.split()[0])

    # 1. manifiesto y libro
    r = subprocess.run(["sha256sum", "-c", "MANIFIESTO_SHA256.txt"], cwd=a.autor, capture_output=True, text=True)
    lin = [l for l in r.stdout.splitlines() if l.strip()]
    versionados = [x for x in a.autor.rglob("*") if x.is_file() and x.name != "MANIFIESTO_SHA256.txt"]
    p(f"1. Manifiesto: {sum(1 for l in lin if l.endswith(': OK'))} de {len(lin)} OK (código {r.returncode}); archivos de la carpeta "
      f"sin contar el manifiesto: {len(versionados)}")
    p(f"   libro {sha(libro)}")
    fuentes = json.loads((a.autor / "datos/fuentes.json").read_text(encoding="utf-8"))
    for slug, f in sorted(fuentes["fuentes"].items()):
        p(f"   fuente {slug}: {si(sha(a.raiz / f['archivo']) == f['sha256'], 'huella coincide', 'HUELLA DISTINTA')}")
    p(f"   libro: {si(sha(libro) == fuentes['libro']['sha256'], 'huella coincide con fuentes.json', 'HUELLA DISTINTA')}")

    cop = a.trabajo / "copia_autor"
    if cop.exists():
        shutil.rmtree(cop)
    shutil.copytree(a.autor, cop)
    sc = cop / "scripts"

    # 2. CSV regenerado
    reg = a.trabajo / "cifras_regenerado.csv"
    cod, so, se, dt = correr(py + ["especificacion_cifras.py", "--raiz", str(a.raiz), "--fuentes", "../datos/fuentes.json", "--salida", str(reg)], sc)
    tipos = {}
    with reg.open(encoding="utf-8", newline="") as f:
        for fila in csv.DictReader(f, delimiter=";"):
            tipos[fila["tipo"]] = tipos.get(fila["tipo"], 0) + 1
    p(f"2. CSV regenerado desde los PDF: código {cod}; {sum(tipos.values())} filas {tipos}; SHA-256 {sha(reg)}")
    p(f"   {si(mismo(reg, a.autor / 'datos/cifras_fuente.csv'))} a datos/cifras_fuente.csv del congelado; "
      f"{si(mismo(reg, a.c16 / 'datos/cifras_fuente.csv'))} al CSV de C17 ({dt:.0f} s)")

    # 3. cadena del §13
    p("3. Cadena del informe §13 (sobre la copia; sin LibreOffice)")
    cod, so, se, dt = correr(py + ["verificar_cifras.py", "--raiz", str(a.raiz), "--datos", "../datos/cifras_fuente.csv", "--fuentes", "../datos/fuentes.json",
                                   "--salida", "../resultados/verificacion_cifras.json", "--exportar-paginas", "../evidencias/paginas"], sc)
    v = json.loads((cop / "resultados/verificacion_cifras.json").read_text(encoding="utf-8"))
    rs = v["resumen"]
    p(f"   verificar_cifras.py: código {cod}; filas {rs['filas']}, OK {rs['ok']}, PENDIENTE {rs['pendientes']}, FALLO {rs['fallos']} ({dt:.0f} s)")
    p(f"     JSON {si(mismo(cop / 'resultados/verificacion_cifras.json', a.autor / 'resultados/verificacion_cifras.json'))} al guardado; registro "
      f"{si(so == (a.autor / 'resultados/verificar_cifras.log').read_text(encoding='utf-8'))} a verificar_cifras.log")
    pags = sorted((a.autor / "evidencias/paginas").glob("*.txt"))
    dist = [x.name for x in pags if not mismo(x, cop / "evidencias/paginas" / x.name)]
    nuevas = [x.name for x in (cop / "evidencias/paginas").glob("*.txt") if not (a.autor / "evidencias/paginas" / x.name).is_file()]
    p(f"     páginas exportadas: {len(pags)} guardadas, {len(dist)} distintas, {len(nuevas)} de más")
    p(f"     PENDIENTE por página: {sorted({(x['doc'], x['pagina']) for x in v['cifras'] if x['estado'] == 'PENDIENTE'})}")
    p(f"     por dimensión: {json.dumps(rs['por_dimension'], ensure_ascii=False)}")

    cod, so_c18, se, dt = correr(py + ["test_verificar_cifras.py", "--raiz", str(a.raiz)], sc)
    casos, direc, comp, mal = resumen_test(so_c18)
    p(f"   test_verificar_cifras.py: código {cod}; casos {casos}; comprobaciones directas {direc}; composición por estado esperado {sorted(comp.items())}; "
      f"registro {si(so_c18 == (a.autor / 'resultados/test_verificar_cifras.log').read_text(encoding='utf-8'))} al guardado ({dt:.0f} s)")

    cod, so, se, dt = correr(py + ["contraste_f1.py", "--cifras", "../datos/cifras_fuente.csv", "--verificacion", "../resultados/verificacion_cifras.json",
                                   "--libro", str(libro), "--caja-no-nula", "../resultados/caja_no_nula.json", "--salida", "../resultados/contraste_f1.json",
                                   "--informe", "../resultados/contraste_f1.md"], sc)
    c = json.loads((cop / "resultados/contraste_f1.json").read_text(encoding="utf-8"))
    res = c.get("resumen", {})
    p(f"   contraste_f1.py: código {cod}; comprobaciones {res.get('comprobaciones')}, fallidas {res.get('fallidas')}, por clase {res.get('por_clase')}, "
      f"entradas {res.get('entradas_usadas')} ({dt:.0f} s)")
    p(f"     JSON {si(mismo(cop / 'resultados/contraste_f1.json', a.autor / 'resultados/contraste_f1.json'))}; "
      f"tabla {si(mismo(cop / 'resultados/contraste_f1.md', a.autor / 'resultados/contraste_f1.md'), 'IDÉNTICA', 'DISTINTA')}; "
      f"registro {si(so == (a.autor / 'resultados/contraste_f1.log').read_text(encoding='utf-8'))}")

    cod, so, se, dt = correr(py + ["test_contraste_residuos.py", "--libro", str(libro)], sc)
    ult = so.strip().splitlines()[-1] if so.strip() else ""
    p(f"   test_contraste_residuos.py: código {cod}; «{ult}»; registro "
      f"{si(so == (a.autor / 'resultados/test_contraste_residuos.log').read_text(encoding='utf-8'))} ({dt:.0f} s)")

    cod, so, se, dt = correr(py + ["cobertura_por_mutacion.py", "--libro", str(libro)], sc)
    p(f"   cobertura_por_mutacion.py: código {cod}; salida "
      f"{si(so == (a.autor / 'resultados/cobertura_por_mutacion.txt').read_text(encoding='utf-8'), 'IDÉNTICA', 'DISTINTA')} a la guardada; "
      f"{si(so == (a.c16 / 'resultados/cobertura_por_mutacion.txt').read_text(encoding='utf-8'), 'IDÉNTICA', 'DISTINTA')} a la de C17 ({dt:.0f} s)")
    for l in so.splitlines()[:8]:
        p("     " + l.strip())

    cod, so, se, dt = correr(py + ["tabla_conciliacion.py", "--cifras", "../datos/cifras_fuente.csv", "--salida", "../resultados/tabla_conciliacion.md"], sc)
    p(f"   tabla_conciliacion.py: código {cod}; tabla "
      f"{si(mismo(cop / 'resultados/tabla_conciliacion.md', a.autor / 'resultados/tabla_conciliacion.md'), 'IDÉNTICA', 'DISTINTA')}")

    # 4. verificador de C16 sobre el mismo CSV
    p("4. Verificador de C16 (worktree de C17) sobre el mismo CSV")
    t16 = a.trabajo / "c16"
    if t16.exists():
        shutil.rmtree(t16)
    (t16 / "paginas").mkdir(parents=True)
    cod, so16, se, dt = correr(py + [str(a.c16 / "scripts/verificar_cifras.py"), "--raiz", str(a.raiz), "--datos", str(a.autor / "datos/cifras_fuente.csv"),
                                     "--fuentes", str(a.autor / "datos/fuentes.json"), "--salida", str(t16 / "verificacion.json"),
                                     "--exportar-paginas", str(t16 / "paginas")], a.trabajo)
    v16 = json.loads((t16 / "verificacion.json").read_text(encoding="utf-8"))
    dif = sum(1 for x, y in zip(v16["cifras"], v["cifras"]) if x != y)
    p(f"   código {cod}; JSON de C16 {si(mismo(t16 / 'verificacion.json', cop / 'resultados/verificacion_cifras.json'))} al de C18 recién generado y "
      f"{si(mismo(t16 / 'verificacion.json', a.c16 / 'resultados/verificacion_cifras.json'))} al que guarda C17")
    p(f"   filas con algún campo distinto entre C16 y C18 (estado, detalle de las seis dimensiones, línea, token): {dif} de {len(v['cifras'])}; "
      f"registro {si(so16 == (a.autor / 'resultados/verificar_cifras.log').read_text(encoding='utf-8'))}")
    dist16 = [x.name for x in pags if not mismo(x, t16 / "paginas" / x.name)]
    p(f"   páginas exportadas por C16: {len(list((t16 / 'paginas').glob('*.txt')))}; distintas de las de C18: {len(dist16)}")

    # 5. el test de C18 con verificadores anteriores
    p("5. El test de C18 (el mismo archivo) con otros verificadores")
    for nombre, verif in (("C16 (worktree de C17)", a.c16 / "scripts/verificar_cifras.py"), ("d3c0f1b", a.d3c0f1b)):
        t = a.trabajo / ("test_con_" + re.sub(r"\W+", "_", nombre))
        if t.exists():
            shutil.rmtree(t)
        shutil.copytree(cop, t)
        shutil.copyfile(verif, t / "scripts/verificar_cifras.py")
        cod, so, se, dt = correr(py + ["test_verificar_cifras.py", "--raiz", str(a.raiz)], t / "scripts")
        casos, direc, comp, mal = resumen_test(so)
        p(f"   con el verificador de {nombre}: código {cod}; casos {casos}; comprobaciones directas {direc} ({dt:.0f} s)")
        for m in mal:
            p("     MAL · " + m)
        if se.strip():
            p("     stderr: " + se.strip().splitlines()[-1][:200])

    # 6. sondas
    p("6. Sondas de metadatos")
    ss = a.trabajo / "sondas_C18.json"
    cod, so, se, dt = correr(py + ["sondas_metadatos.py", "--raiz", str(a.raiz), "--autor", str(cop), "--etiqueta", "C18 (commit que contiene este archivo)",
                                   "--salida", str(ss)], sc)
    for l in so.splitlines():
        p("   " + l)
    s18 = json.loads(ss.read_text(encoding="utf-8"))
    s16 = json.loads((a.c16 / "resultados/sondas_metadatos_C16.json").read_text(encoding="utf-8"))
    sin = lambda d: {k: x for k, x in d.items() if k != "version"}
    p(f"   JSON {si(mismo(ss, a.autor / 'resultados/sondas_metadatos_C18.json'))} al guardado; igual al de C16 salvo «version»: {sin(s18) == sin(s16)} ({dt:.0f} s)")

    # 7. contraste frente a C17 y referencia de E9
    p("7. Contraste de C19 frente al de C17")
    for f in ("contraste_f1.json", "contraste_f1.md", "contraste_f1.log", "test_contraste_residuos.log", "tabla_conciliacion.md", "caja_no_nula.json",
              "verificacion_cifras.json", "verificar_cifras.log"):
        p(f"   resultados/{f}: {si(mismo(a.autor / 'resultados' / f, a.c16 / 'resultados' / f))} en C17 y en C19")
    c16 = json.loads((a.c16 / "resultados/contraste_f1.json").read_text(encoding="utf-8"))
    ref = c.get("referencia_especificacion")
    p(f"   referencia_especificacion: {si(ref == c16.get('referencia_especificacion'), 'IGUAL', 'DISTINTA')} en C17 y en la ejecución de hoy "
      f"({len(json.dumps(ref))} caracteres)")
    hallados = []

    def buscar(o, ruta=""):
        if isinstance(o, dict):
            for k, x in o.items():
                buscar(x, f"{ruta}/{k}")
        elif isinstance(o, list):
            for k, x in enumerate(o):
                buscar(x, f"{ruta}[{k}]")
        elif isinstance(o, (int, float)) and not isinstance(o, bool):
            if abs(o - 2.445331695332) < 5e-10 or abs(o - 1.612524303305) < 5e-10:
                hallados.append((ruta, o))
    buscar(ref)
    for ruta, o in hallados:
        p(f"     {ruta} = {o!r}")

    # 8. barrido del autor
    p("8. Barrido del autor (barrido_fecha_rotulo.py, con --anterior C16)")
    etiqueta = None
    guard = (a.autor / "resultados/barrido_fecha_rotulo.txt").read_text(encoding="utf-8")
    m = re.search(r"^Comparación con (.*?): \{", guard, re.M)
    if m:
        etiqueta = m.group(1)
    cod, so, se, dt = correr(py + ["barrido_fecha_rotulo.py", "--raiz", str(a.raiz), "--anterior", str(a.c16 / "scripts/verificar_cifras.py")]
                             + (["--etiqueta", etiqueta] if etiqueta else []), sc)
    p(f"   código {cod}; salida {si(so == guard, 'IDÉNTICA', 'DISTINTA')} a resultados/barrido_fecha_rotulo.txt (etiqueta «{etiqueta}») ({dt:.0f} s)")
    for l in so.splitlines():
        if l.startswith(("Líneas en que", "Líneas con la fecha", "Comparación con", "Solo la versión")):
            p("     " + l[:400])
    (a.trabajo / "reproduccion_9.txt").write_text("\n".join(out) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
