#!/usr/bin/env python3
"""Propuestas del revisor de la SÉPTIMA comprobación, aplicadas sobre copias ligeras del código de 45ff57c. NO es código entregado ni
revisado: sirve para comprobar que lo que se propone es compatible con las baterías y con los registros reales. Nunca toca el árbol congelado.
  fix7t · SOLO PRUEBAS: (W5: el mensaje; W4: cuatro casos de la cifra citada sola) y cuatro casos con la cita COMPLETA y el valor cortado (lo único que llega a los límites de la cifra de
          _lectura_cifra desde que los límites de la CITA llevan el apóstrofo, W4) y dos controles positivos (la cifra entera con apóstrofo).
          Con el código de la candidata la prueba «(V3, V7)» tiene que FALLAR: es la demostración de X1.
  fix7  · fix7t + CÓDIGO: una línea, la :542 — «(?<!\\d[’])» pasa a «(?<!\\d['’])» (el apóstrofo ASCII que 8196522 tenía y la sexta proponía conservar).
Uso: python3 -I -B propuestas7.py   (escribe fable/fix7t y fable/fix7, y los diff en salidas/)"""
import os, shutil, subprocess
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPIA = os.path.join(F, "copia", "munger_v2_r1")
T415, VEP = "pruebas/test_verificacion_entradas_415.py", "scripts/verificacion_entradas.py"

PRUEBAS = [
    (T415, '''      ("849,7", 849.7, "Total 1\\u2019849,7"): "ausente", ("849,7 mill", 849.7, "Ventas 2023\\n849,7 millones"): "no_localizada"}''',
           '''      ("849,7", 849.7, "Total 1\\u2019849,7"): "ausente", ("849,7 mill", 849.7, "Ventas 2023\\n849,7 millones"): "no_localizada",
      # (séptima, propuesta del revisor, X1) la cita COMPLETA con el valor cortado: desde W4 es lo único que llega a los límites de la cifra de _lectura_cifra
      ("Total 1'849,7", 849.7, "Total 1'849,7"): "ausente", ("Total 1\\u2019849,7", 849.7, "Total 1\\u2019849,7"): "ausente",
      ("Total 849'697", 849, "Total 849'697"): "ausente", ("Total 849\\u2019697", 849, "Total 849\\u2019697"): "ausente",
      ("Total 1'849.7", 1849.7, "Total 1'849.7"): "ok", ("Total 849'697", 849697, "Total 849'697"): "ok",  # controles: la cifra entera con apóstrofo se lee
      # (séptima, propuesta del revisor, W4) la cifra citada sola que además está dentro de un número con apóstrofo se lee en su aparición suelta
      ("849,7", 849.7, "Total 1'849,7\\nOtros 849,7"): "ok", ("849,7", 849.7, "Total 1\\u2019849,7\\nOtros 849,7"): "ok",
      ("Total 849", 849, "Total 849'697\\nTotal 849"): "ok", ("Total 849", 849, "Total 849\\u2019697\\nTotal 849"): "ok"}'''),
    (T415, '''mal_v3 = {k_[2]: VE._cita_cifra(*k_)[0] for k_, e_ in v3.items() if VE._cita_cifra(*k_)[0] != e_}''',
           '''mal_v3 = {k_: VE._cita_cifra(*k_)[0] for k_, e_ in v3.items() if VE._cita_cifra(*k_)[0] != e_}  # (séptima, propuesta) la clave entera: ya hay casos con la misma página'''),
]
PRUEBAS.append((T415, '''r_v5[0] == "signo_indeterminado" and n_v5 == VE.MAX_APARICIONES_CITA + 1 and _time.time() - t0 < 5,''',
                '''r_v5[0] == "signo_indeterminado" and "más de" in r_v5[1] and n_v5 == VE.MAX_APARICIONES_CITA + 1 and _time.time() - t0 < 5,  # (séptima, propuesta) W5: el mensaje'''))
CODIGO = [
    (VEP, r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d[’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7""",
          r"""        for m in re.finditer(r"(?<![\d.,])(?<!\d['’])" + re.escape(c) + r"(?!\d|[.,'’]\d)", t):  # (hito 2, V7 y W3) «1'849,7» ni «1’849,7» contienen 849,7"""),  # un solo carácter: «[’]» → «['’]»; el comentario de la línea no cambia
]


def construir(nombre, cambios):
    dst = os.path.join(F, nombre, "munger_v2_r1")
    if os.path.lexists(os.path.join(F, nombre)):
        raise SystemExit(f"{nombre} ya existe: bórrese a mano si se quiere rehacer")
    os.makedirs(os.path.join(dst, "personaje_v2"))
    for x in os.listdir(COPIA):
        if x != "personaje_v2":
            os.symlink(os.path.realpath(os.path.join(COPIA, x)), os.path.join(dst, x))
    for x in os.listdir(os.path.join(COPIA, "personaje_v2")):
        o, n = os.path.join(COPIA, "personaje_v2", x), os.path.join(dst, "personaje_v2", x)
        if x in ("scripts", "pruebas", "esquema"):
            shutil.copytree(o, n, ignore=shutil.ignore_patterns("__pycache__"), symlinks=True)
        else:
            os.symlink(os.path.realpath(o), n)
    for arch, viejo, nuevo in cambios:
        p = os.path.join(dst, "personaje_v2", arch)
        s = open(p, encoding="utf-8").read()
        assert s.count(viejo) == 1, (nombre, arch, viejo[:70], s.count(viejo))
        open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
    d = subprocess.run(["diff", "-ru", os.path.join("copia", "munger_v2_r1", "personaje_v2"), os.path.join(nombre, "munger_v2_r1", "personaje_v2"), "-x", "__pycache__",
                        "-x", "empresas_v2*", "-x", "corpus", "-x", "prompts"], cwd=F, capture_output=True, text=True).stdout
    open(os.path.join(F, "salidas", f"propuestas7_{nombre}.diff"), "w", encoding="utf-8").write(d)
    print(f"{nombre}: {len(cambios)} cambios · {len(d.splitlines())} líneas de diff")


if __name__ == "__main__":
    construir("fix7t", PRUEBAS)
    construir("fix7", PRUEBAS + CODIGO)
