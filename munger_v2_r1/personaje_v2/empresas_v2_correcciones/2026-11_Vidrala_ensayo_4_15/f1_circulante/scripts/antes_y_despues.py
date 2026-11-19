#!/usr/bin/env python3
"""(V-CIRC) La batería nueva contra el código ANTERIOR: cuántas de sus pruebas pasan con el producto de un commit dado (por omisión, el de partida de
la rama f1/circulante-normalizado) y cuántas con el árbol actual.

Uso (desde munger_v2_r1/): python3 -I personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_circulante/scripts/antes_y_despues.py \
        [COMMIT] [--bateria personaje_v2/pruebas/test_circulante_f1.py] [--tmp DIR] [--lista]
Con el código anterior la batería no llega a ejecutarse entera (llama a funciones que no existen): se ejecuta sentencia a sentencia de primer nivel y
una sentencia que falla no registra sus pruebas. Las que faltan respecto del árbol actual cuentan como no pasadas. Escribe la salida en pantalla.
(Revisión C1) Con un commit de la rama (p. ej. fbb146d) se copian también la configuración, los guiones, la referencia y la plantilla de la V6.3.2 si
el commit los tiene, y todos los datos de prueba de pruebas/datos_circulante; con --lista, los nombres de las pruebas que no pasan con el código
anterior y sí con el actual.
"""
import ast
import json
import os
import shutil
import subprocess
import sys
import tempfile

RAIZ = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "..", ".."))   # munger_v2_r1
REPO = os.path.dirname(RAIZ)
ARNES = r'''
import ast, io, os, sys, contextlib, json
ruta = sys.argv[1]
src = open(ruta, encoding="utf-8").read()
mod = ast.parse(src)
g = {"__name__": "__main__", "__file__": ruta}
errores = []
for nodo in mod.body:
    codigo = compile(ast.Module(body=[nodo], type_ignores=[]), ruta, "exec")
    try:
        exec(codigo, g)
    except SystemExit:
        pass
    except Exception as e:  # noqa: BLE001
        errores.append(f"línea {nodo.lineno}: {type(e).__name__}: {str(e)[:120]}")
R = g.get("R") or g.get("RES") or []
ok = lambda x: bool(x[1] if isinstance(x, tuple) else x.get("ok"))
nom = lambda x: str(x[0] if isinstance(x, tuple) else x.get("prueba"))
print("@@" + json.dumps({"pasan": sum(1 for x in R if ok(x)), "registradas": len(R), "errores": errores,
                         "nombres_pasan": [nom(x) for x in R if ok(x)]}, ensure_ascii=False))
'''


def correr(arbol, bateria):
    ruta = os.path.join(arbol, bateria)
    with tempfile.NamedTemporaryFile("w", suffix=".py", delete=False) as f:
        f.write(ARNES)
    try:
        r = subprocess.run([sys.executable, "-B", f.name, ruta], capture_output=True, text=True, cwd=os.path.join(arbol, "personaje_v2"))
    finally:
        os.unlink(f.name)
    lin = [x for x in r.stdout.splitlines() if x.startswith("@@")]
    return json.loads(lin[-1][2:]) if lin else {"pasan": 0, "registradas": 0, "errores": [r.stderr[-300:]]}


def main():
    a = sys.argv[1:]
    commit = a[0] if a and not a[0].startswith("--") else "ebf47fc"
    bateria = a[a.index("--bateria") + 1] if "--bateria" in a else "personaje_v2/pruebas/test_circulante_f1.py"
    tmp = a[a.index("--tmp") + 1] if "--tmp" in a else tempfile.mkdtemp(prefix="circ_antes_")
    viejo = os.path.join(tmp, "anterior")
    os.makedirs(viejo, exist_ok=True)
    # el producto del commit anterior (personaje_v2 y v6, sin binarios) y, encima, la batería nueva y sus datos de prueba
    rutas = ["munger_v2_r1/personaje_v2/scripts", "munger_v2_r1/personaje_v2/esquema",
             "munger_v2_r1/personaje_v2/config_v2.json", "munger_v2_r1/personaje_v2/config_v2_v631_f1.json", "munger_v2_r1/personaje_v2/config_v2_v632_f1.json",
             "munger_v2_r1/personaje_v2/config_v2_v64_experimental.json", "munger_v2_r1/personaje_v2/config_v2_v641_experimental.json",
             "munger_v2_r1/v6/v631_f1/scripts", "munger_v2_r1/v6/v631_f1/referencia", "munger_v2_r1/v6/v632_f1/scripts", "munger_v2_r1/v6/v632_f1/referencia",
             "munger_v2_r1/v6/scripts"]
    en_commit = set(subprocess.run(["git", "-C", REPO, "ls-tree", "--name-only", "-r", commit, "--"] + rutas, capture_output=True, text=True,
                                   check=True).stdout.split())
    rutas = [r for r in rutas if r in en_commit or any(x.startswith(r + "/") for x in en_commit)]   # (C1) solo las que existen en el commit
    arch = subprocess.run(["git", "-C", REPO, "archive", commit] + rutas, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", viejo], input=arch, check=True)
    va = os.path.join(viejo, "munger_v2_r1")
    datos = os.path.join("personaje_v2", "pruebas", "datos_circulante")
    for rel in [bateria] + [os.path.join(datos, f) for f in sorted(os.listdir(os.path.join(RAIZ, datos))) if not f.startswith((".", "__"))]:
        os.makedirs(os.path.dirname(os.path.join(va, rel)), exist_ok=True)
        shutil.copy2(os.path.join(RAIZ, rel), os.path.join(va, rel))
    for rel in ("v6/v631_f1/entregables/Plantilla_V6.3.1_F1.xlsx", "v6/entregables/Plantilla_V6.3.xlsx",   # binarios de la base (sin cambios) y, si el
                "v6/v632_f1/entregables/Plantilla_V6.3.2_F1.xlsx"):                                       # commit tiene la V6.3.2, su plantilla
        if rel.startswith("v6/v632_f1/") and not os.path.isdir(os.path.join(va, "v6", "v632_f1")):
            continue
        os.makedirs(os.path.dirname(os.path.join(va, rel)), exist_ok=True)
        shutil.copy2(os.path.join(RAIZ, rel), os.path.join(va, rel))
    antes, despues = correr(va, bateria), correr(RAIZ, bateria)
    total = despues["registradas"]
    print(f"batería {bateria}")
    print(f"código anterior ({commit}): pasan {antes['pasan']} de {total} (registradas {antes['registradas']}; sentencias con error {len(antes['errores'])})")
    for e in antes["errores"][:12]:
        print(f"  · {e}")
    print(f"código actual: pasan {despues['pasan']} de {total} (sentencias con error {len(despues['errores'])})")
    if "--lista" in a:
        nuevas = [x for x in despues.get("nombres_pasan", []) if x not in set(antes.get("nombres_pasan", []))]
        print(f"no pasan con {commit} y sí con el actual ({len(nuevas)}):")
        for x in nuevas:
            print(f"  · {x[:230]}")
    shutil.rmtree(tmp, ignore_errors=True)
    return 0 if despues["pasan"] == total and not despues["errores"] else 1


if __name__ == "__main__":
    sys.exit(main())
