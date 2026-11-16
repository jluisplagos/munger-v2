"""Revisión n.º 7 (frente E · F1 · Elis). Reproducción de las cifras que declara el autor sobre el commit congelado C15.
No modifica nada del autor: trabaja sobre una COPIA temporal de su carpeta frente_E_F1_elis.

Pasos:
  1. manifiesto de la carpeta (sha256sum -c);
  2. regenera el CSV desde los PDF (especificacion_cifras.py) y lo compara con el del autor;
  3. ejecuta la cadena del informe §13 (sin LibreOffice: prueba_caja_no_nula.py no se repite) y sondas_metadatos.py, y
     compara cada salida, byte a byte, con la que guarda el autor;
  4. compara las filas comunes de la verificación con las del congelado anterior (C13): estado y detalle de cada dimensión;
  5. compara los valores de referencia de E9 (referencia_especificacion) entre versiones;
  6. con --revisores, ejecuta los scripts de las revisiones n.º 1, 3, 4, 5 y 6 sobre C14, tal como los copia el autor, y
     compara cada salida con resultados/*_sobre_C14.txt.

Uso: python3 -I reproduccion_7.py --raiz <munger_v2_r1> --autor <frente C15> --c13 <frente C13> [--otra NOMBRE=<frente> ...]
        [--revisores --c8 <frente C8>] [--trabajo <carpeta temporal>]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def run(args, cwd, salida=None):
    r = subprocess.run([sys.executable, "-I"] + [str(x) for x in args], cwd=str(cwd), capture_output=True, text=True)
    if salida is not None:
        Path(salida).write_text(r.stdout, encoding="utf-8")
    return r.returncode, r.stdout, r.stderr


def igual(a, b):
    return Path(a).is_file() and Path(b).is_file() and Path(a).read_bytes() == Path(b).read_bytes()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--raiz", required=True, type=Path)
    ap.add_argument("--autor", required=True, type=Path)
    ap.add_argument("--c13", required=True, type=Path)
    ap.add_argument("--otra", action="append", default=[], help="NOMBRE=carpeta de otra versión, para comparar la referencia de E9")
    ap.add_argument("--revisores", action="store_true")
    ap.add_argument("--c8", type=Path)
    ap.add_argument("--trabajo", type=Path)
    a = ap.parse_args()
    autor = a.autor.resolve()
    libro = a.raiz / "personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx"
    trabajo = Path(a.trabajo or tempfile.mkdtemp(prefix="rev7_"))
    copia = trabajo / "frente_E_F1_elis"
    if copia.exists():
        shutil.rmtree(copia)
    shutil.copytree(autor, copia)
    sc, res = copia / "scripts", copia / "resultados"
    p = print
    p("Reproducción de la revisión n.º 7 sobre una copia de la carpeta del autor\n")
    fu = json.loads((autor / "datos" / "fuentes.json").read_text(encoding="utf-8"))
    p(f"Libro: SHA-256 {sha(libro)} · declarado {fu['libro']['sha256']} · {'coincide' if sha(libro) == fu['libro']['sha256'] else 'DISTINTO'}")
    for k, f in sorted(fu["fuentes"].items()):
        h = sha(a.raiz / f["archivo"])
        p(f"Fuente {k}: {'huella coincide' if h == f['sha256'] else 'HUELLA DISTINTA'} ({h[:12]}…)")

    r = subprocess.run(["sha256sum", "-c", "MANIFIESTO_SHA256.txt"], cwd=str(autor), capture_output=True, text=True)
    lin = [x for x in r.stdout.splitlines() if x.strip()]
    p(f"\n1. Manifiesto: {sum(1 for x in lin if x.endswith(': OK'))} de {len(lin)} archivos con la huella declarada; código {r.returncode}")

    csv_autor = sha(autor / "datos" / "cifras_fuente.csv")
    cod, out, err = run(["especificacion_cifras.py", "--raiz", a.raiz, "--fuentes", "../datos/fuentes.json", "--salida", "../datos/cifras_fuente.csv"], sc)
    n = sum(1 for _ in (copia / "datos" / "cifras_fuente.csv").open(encoding="utf-8")) - 1
    p(f"\n2. CSV regenerado desde los PDF: código {cod}; {n} filas; SHA-256 {sha(copia / 'datos' / 'cifras_fuente.csv')[:16]}… · "
      f"{'IDÉNTICO al del autor' if sha(copia / 'datos' / 'cifras_fuente.csv') == csv_autor else 'DISTINTO del del autor'}")

    p("\n3. Cadena del informe §13 (salida regenerada frente a la que guarda el autor)")
    cod, out, _ = run(["verificar_cifras.py", "--raiz", a.raiz, "--datos", "../datos/cifras_fuente.csv", "--fuentes", "../datos/fuentes.json",
                       "--salida", "../resultados/verificacion_cifras.json", "--exportar-paginas", "../evidencias/paginas"], sc, trabajo / "verificar_cifras.log")
    v = json.loads((res / "verificacion_cifras.json").read_text(encoding="utf-8"))
    pag_a = sorted(x.name for x in (autor / "evidencias" / "paginas").iterdir())
    pag_c = sorted(x.name for x in (copia / "evidencias" / "paginas").iterdir())
    pag_ig = pag_a == pag_c and all(igual(autor / "evidencias" / "paginas" / x, copia / "evidencias" / "paginas" / x) for x in pag_a)
    p(f"   verificar_cifras.py: código {cod} · {v['resumen']['filas']} filas, {v['resumen']['ok']} OK, {v['resumen']['pendientes']} PENDIENTE, "
      f"{v['resumen']['fallos']} FALLO · JSON {'idéntico' if igual(res / 'verificacion_cifras.json', autor / 'resultados' / 'verificacion_cifras.json') else 'DISTINTO'} · "
      f"registro {'idéntico' if igual(trabajo / 'verificar_cifras.log', autor / 'resultados' / 'verificar_cifras.log') else 'DISTINTO'} · "
      f"{len(pag_c)} páginas exportadas, {'idénticas' if pag_ig else 'DISTINTAS'}")
    cod, out, _ = run(["test_verificar_cifras.py", "--raiz", a.raiz], sc, trabajo / "test_verificar_cifras.log")
    esperados = {"OK": 0, "PENDIENTE": 0, "FALLO": 0}
    for l in out.splitlines():
        for k in esperados:
            if l.rstrip().endswith("→ " + k):
                esperados[k] += 1
    p(f"   test_verificar_cifras.py: código {cod} · {out.strip().splitlines()[-1]} · por resultado esperado {esperados} · "
      f"registro {'idéntico' if igual(trabajo / 'test_verificar_cifras.log', autor / 'resultados' / 'test_verificar_cifras.log') else 'DISTINTO'}")
    cod, out, _ = run(["contraste_f1.py", "--cifras", "../datos/cifras_fuente.csv", "--verificacion", "../resultados/verificacion_cifras.json", "--libro", libro,
                       "--caja-no-nula", "../resultados/caja_no_nula.json", "--salida", "../resultados/contraste_f1.json", "--informe",
                       "../resultados/contraste_f1.md"], sc, trabajo / "contraste_f1.log")
    k = json.loads((res / "contraste_f1.json").read_text(encoding="utf-8"))
    ce = k["tablas"]["cobertura_entradas"]
    p(f"   contraste_f1.py: código {cod} · {k['resumen']['comprobaciones']} comprobaciones {k['resumen']['por_clase']}, {k['resumen']['fallidas']} fallidas · "
      f"{k['resumen']['entradas_usadas']} entradas · JSON {'idéntico' if igual(res / 'contraste_f1.json', autor / 'resultados' / 'contraste_f1.json') else 'DISTINTO'} · "
      f"tabla {'idéntica' if igual(res / 'contraste_f1.md', autor / 'resultados' / 'contraste_f1.md') else 'DISTINTA'} · "
      f"registro {'idéntico' if igual(trabajo / 'contraste_f1.log', autor / 'resultados' / 'contraste_f1.log') else 'DISTINTO'}")
    nres = sum(len(x) for x in k["tablas"]["residuos_con_cota"].values())
    p(f"      residuos con cota: {nres} · cobertura {ce['resumen']} · páginas {ce['resumen_paginas']} · umbrales "
      f"{ce['umbrales_entre_paginas']['por_tramo_en_unidades_de_la_ultima_cifra']}")
    cod, out, _ = run(["test_contraste_residuos.py", "--libro", libro], sc, trabajo / "test_contraste_residuos.log")
    p(f"   test_contraste_residuos.py: código {cod} · {out.strip().splitlines()[-1]} · "
      f"registro {'idéntico' if igual(trabajo / 'test_contraste_residuos.log', autor / 'resultados' / 'test_contraste_residuos.log') else 'DISTINTO'}")
    cod, out, _ = run(["cobertura_por_mutacion.py", "--libro", libro], sc, trabajo / "cobertura_por_mutacion.txt")
    p(f"   cobertura_por_mutacion.py: código {cod} · {out.splitlines()[0]} · "
      f"salida {'idéntica' if igual(trabajo / 'cobertura_por_mutacion.txt', autor / 'resultados' / 'cobertura_por_mutacion.txt') else 'DISTINTA'}")
    for l in out.splitlines()[1:7]:
        p("      " + l.strip())
    cod, out, _ = run(["tabla_conciliacion.py", "--cifras", "../datos/cifras_fuente.csv", "--salida", "../resultados/tabla_conciliacion.md"], sc)
    p(f"   tabla_conciliacion.py: código {cod} · tabla {'idéntica' if igual(res / 'tabla_conciliacion.md', autor / 'resultados' / 'tabla_conciliacion.md') else 'DISTINTA'}")
    cod, out, _ = run(["sondas_metadatos.py", "--raiz", a.raiz, "--autor", autor, "--etiqueta", "C14 (commit que contiene este archivo)", "--salida",
                       trabajo / "sondas_metadatos_C14.json"], sc)
    p(f"   sondas_metadatos.py: código {cod} · JSON {'idéntico' if igual(trabajo / 'sondas_metadatos_C14.json', autor / 'resultados' / 'sondas_metadatos_C14.json') else 'DISTINTO'}")
    for l in out.splitlines():
        if "cada fila de tabla" in l:
            p("      " + l.strip())
    r = subprocess.run(["sha256sum", "-c", "MANIFIESTO_SHA256.txt"], cwd=str(copia), capture_output=True, text=True)
    lin = [x for x in r.stdout.splitlines() if x.strip()]
    p(f"   manifiesto sobre la copia regenerada: {sum(1 for x in lin if x.endswith(': OK'))} de {len(lin)}")

    p("\n4. Filas comunes con el congelado anterior (C13)")
    v13 = {x["id"]: x for x in json.loads((a.c13 / "resultados" / "verificacion_cifras.json").read_text(encoding="utf-8"))["cifras"]}
    v15 = {x["id"]: x for x in v["cifras"]}
    com = sorted(set(v13) & set(v15))
    dif = [i for i in com if v13[i]["estado"] != v15[i]["estado"] or any(
        (v13[i]["dimensiones"][d]["estado"], v13[i]["dimensiones"][d]["detalle"]) != (v15[i]["dimensiones"][d]["estado"], v15[i]["dimensiones"][d]["detalle"])
        for d in v13[i]["dimensiones"])]
    p(f"   C13: {len(v13)} filas · C15: {len(v15)} · comunes: {len(com)} · con estado o detalle distinto en alguna dimensión: {len(dif)} {dif[:5]} · "
      f"con cualquier campo distinto: {sum(1 for i in com if v13[i] != v15[i])}")
    for i in sorted(set(v15) - set(v13)):
        x = v15[i]
        p(f"   nueva: {i} · {x['doc']} p.{x['pagina']} · {x['anio']} · «{x['literal']}» · {x['estado']} · " +
          "; ".join(f"{d}: {x['dimensiones'][d]['detalle']}" for d in x["dimensiones"]))
    p(f"   desaparecen: {sorted(set(v13) - set(v15))}")

    p("\n5. Valores de referencia de E9 (referencia_especificacion)")
    ref = k["referencia_especificacion"]
    p(f"   C15: C53 de A1 {ref['perimetros']['A1']['S2C_C53']} · de A2 {ref['perimetros']['A2']['S2C_C53']} · f de A0 {ref['perimetros']['A0']['f']}")
    for nom, carpeta in [("C13", a.c13)] + [x.split("=", 1) for x in a.otra]:
        o = json.loads((Path(carpeta) / "resultados" / "contraste_f1.json").read_text(encoding="utf-8")).get("referencia_especificacion")
        p(f"   igual que en {nom}: {'sí' if o == ref else 'NO'}")

    if a.revisores:
        p("\n6. Scripts de las revisiones anteriores sobre C14 (salida regenerada frente a resultados/*_sobre_C14.txt del autor)")
        rv = autor / "revision"
        c13, c8 = a.c13.resolve(), a.c8.resolve()
        b6 = trabajo / "b6"
        b6.mkdir(exist_ok=True)
        tareas = [
            ("mutantes_revisor", [rv / "scripts_revisor/prueba_mutantes.py", "--raiz", a.raiz, "--autor", autor, "--libro", libro]),
            ("revisor3_prueba_mutantes_3", [rv / "scripts_revisor_3/prueba_mutantes_3.py", "--raiz", a.raiz, "--autor", autor, "--libro", libro]),
            ("revisor3_prueba_mutantes_3b", [rv / "scripts_revisor_3/prueba_mutantes_3b.py", "--raiz", a.raiz, "--autor", autor, "--libro", libro]),
            ("revisor3_sondas", [rv / "scripts_revisor_3/sondas_revisor.py", "--raiz", a.raiz, "--libro", libro, "--version", f"C14={autor}"]),
            ("revisor4_contraejemplos_4", [rv / "scripts_revisor_4/contraejemplos_4.py", "--raiz", a.raiz, "--autor", autor, "--libro", libro]),
            ("revisor4_paginas_sin_ancla", [rv / "scripts_revisor_4/paginas_sin_ancla.py", "--contraste", autor / "resultados" / "contraste_f1.json"]),
            ("revisor5_contraejemplos_5", [rv / "scripts_revisor_5/contraejemplos_5.py", "--raiz", a.raiz, "--version", f"C14={autor}"]),
            ("revisor5_clases_5", [rv / "scripts_revisor_5/clases_5.py", "--raiz", a.raiz, "--anterior", f"C8={c8}", "--nueva", f"C14={autor}"]),
            ("revisor5_cobertura_propia", [rv / "scripts_revisor_5/cobertura_propia.py", "--autor", autor, "--libro", libro]),
            ("revisor5_barrido_tablas", [rv / "scripts_revisor_5/barrido_tablas.py", "--raiz", a.raiz, "--nueva", autor, "--anterior", c8, "--salida", trabajo / "bt"]),
            ("revisor6_barrido_6", [rv / "scripts_revisor_6/barrido_6.py", "--raiz", a.raiz, "--anterior", f"C13={c13}", "--nueva", f"C14={autor}", "--todas",
                                    b6 / "todas.jsonl.gz", "--salida", b6 / "barrido_6.txt"]),
            ("(lectura geométrica)", [rv / "scripts_revisor_6/lectura_geometrica.py", "--raiz", a.raiz, "--autor", autor, "--todas", b6 / "todas.jsonl.gz",
                                      "--salida", b6 / "lectura.jsonl.gz", "--solo-grupo"]),
            ("revisor6_clases_6", [rv / "scripts_revisor_6/clases_6.py", "--todas", b6 / "todas.jsonl.gz", "--lectura", b6 / "lectura.jsonl.gz", "--anterior", "C13",
                                   "--nueva", "C14"]),
            ("revisor6_contraejemplos_6", [rv / "scripts_revisor_6/contraejemplos_6.py", "--raiz", a.raiz, "--version", f"C13={c13}", "--version", f"C14={autor}"]),
            ("revisor6_consultas_6", [rv / "scripts_revisor_6/consultas_6.py", "--raiz", a.raiz, "--todas", b6 / "todas.jsonl.gz", "--anterior", f"C13={c13}",
                                      "--nueva", f"C14={autor}"]),
            ("revisor6_lectura_filas_c12", [rv / "scripts_revisor_6/lectura_filas_c12.py", "--raiz", a.raiz, "--autor", autor]),
            ("revisor6_cobertura_6", [rv / "scripts_revisor_6/cobertura_6.py", "--raiz", a.raiz, "--autor", autor, "--libro", libro]),
        ]
        for nombre, args in tareas:
            cod, out, err = run(args, Path(args[0]).parent)
            if nombre.startswith("("):
                p(f"   {nombre}: código {cod} · {out.strip().splitlines()[-1] if out.strip() else ''}")
                continue
            if nombre == "revisor5_barrido_tablas":
                out = (trabajo / "bt" / "barrido_tablas.txt").read_text(encoding="utf-8")
            elif nombre == "revisor6_barrido_6":
                out = (b6 / "barrido_6.txt").read_text(encoding="utf-8")
            guardada = (autor / "resultados" / f"{nombre}_sobre_C14.txt").read_text(encoding="utf-8")
            p(f"   {nombre}: código {cod} · {len(out.splitlines())} líneas · {'IDÉNTICA' if out == guardada else 'DISTINTA'} a la guardada"
              + (f" · primera línea: «{out.splitlines()[0][:90]}»" if nombre == "revisor5_barrido_tablas" else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
