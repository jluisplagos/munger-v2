"""Prueba con exceso de caja distinto de cero sobre una COPIA TEMPORAL del libro (frente E · F1 · Elis; revisión, O15).

En el libro de Elis el exceso de caja del motor A (Análisis!C76) es 0. Con ese valor, la identidad
«flujo sin crecimiento = Motor!BL·r − exceso de caja» y la correcta «(Motor!BL − Motor!M)·r» dan lo mismo, y la
prueba no distingue una de otra. Este script copia el libro a una carpeta temporal y, con LibreOffice sin interfaz:
  1. pone Análisis!C76 = X para cada X pedido (0 incluido);
  2. recalcula todo el libro;
  3. lee Motor!BL, Motor!M y Motor!J de las filas 6–8 (MALO, NORMAL, BUENO).
contraste_f1.py --caja-no-nula <salida> comprueba después que (BL − M)·r es el flujo sin crecimiento que él mismo
calcula y que M = X.

No modifica el libro original: comprueba su SHA-256 antes y después, y la copia se borra al terminar.
LibreOffice se usa en un solo proceso, con un perfil propio y temporal; no debe correr otro pipeline de LibreOffice
a la vez en la misma máquina.

Uso:  python3 -I prueba_caja_no_nula.py --libro <ruta>/Elis_v63_evaluada.xlsx --salida ../resultados/caja_no_nula.json [--valores 0 250 -80]
"""
import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

SHA_LIBRO = "d2593777650f1d9d77bcc7b9eaa6f4c0c12a742fa4706bd20b35808f99c92385"


def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--libro", required=True, type=Path)
    ap.add_argument("--salida", required=True, type=Path)
    ap.add_argument("--valores", nargs="+", type=float, default=[0.0, 250.0, -80.0])
    a = ap.parse_args()
    if sha256(a.libro) != SHA_LIBRO:
        sys.exit("el libro no es el de referencia (SHA-256 distinto)")
    import uno  # noqa: E402  (LibreOffice: python3-uno)
    from com.sun.star.beans import PropertyValue  # noqa: E402

    version = subprocess.run(["soffice", "--version"], capture_output=True, text=True).stdout.strip()
    out = {"libro_sha256": SHA_LIBRO, "libreoffice": version, "resultados": {},
           "nota": "copia temporal del libro recalculada con LibreOffice; el original no se modifica"}
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        copia = d / "copia.xlsx"
        shutil.copyfile(a.libro, copia)
        perfil = d / "perfil"
        tubo = f"frenteE_{int(time.time())}"
        proc = subprocess.Popen(["soffice", "--headless", "--invisible", "--nologo", "--norestore", "--nodefault",
                                 f"-env:UserInstallation={uno.systemPathToFileUrl(str(perfil))}",
                                 f"--accept=pipe,name={tubo};urp;StarOffice.ComponentContext"],
                                stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            local = uno.getComponentContext()
            resolver = local.ServiceManager.createInstanceWithContext("com.sun.star.bridge.UnoUrlResolver", local)
            ctx = None
            for _ in range(120):
                try:
                    ctx = resolver.resolve(f"uno:pipe,name={tubo};urp;StarOffice.ComponentContext")
                    break
                except Exception:  # noqa: BLE001  (LibreOffice aún arrancando)
                    time.sleep(0.5)
            if ctx is None:
                sys.exit("no se pudo conectar con LibreOffice")
            desktop = ctx.ServiceManager.createInstanceWithContext("com.sun.star.frame.Desktop", ctx)
            oculto = PropertyValue()
            oculto.Name, oculto.Value = "Hidden", True
            doc = desktop.loadComponentFromURL(uno.systemPathToFileUrl(str(copia)), "_blank", 0, (oculto,))
            analisis, motor = doc.Sheets.getByName("Análisis"), doc.Sheets.getByName("Motor")
            for X in a.valores:
                analisis.getCellRangeByName("C76").setValue(X)
                doc.calculateAll()
                clave = f"{X:g}"
                out["resultados"][clave] = {}
                for fila in ("6", "7", "8"):
                    out["resultados"][clave][fila] = {c: motor.getCellRangeByName(f"{c}{fila}").getValue() for c in ("BL", "M", "J")}
                out["resultados"][clave]["Análisis!C76"] = analisis.getCellRangeByName("C76").getValue()
            doc.close(True)
            try:
                desktop.terminate()
            except Exception:  # noqa: BLE001  (la conexión se cierra al terminar)
                pass
        finally:
            try:
                proc.wait(timeout=60)
            except subprocess.TimeoutExpired:
                proc.kill()
    if sha256(a.libro) != SHA_LIBRO:
        sys.exit("el libro original ha cambiado: no debería ocurrir")
    out["libro_original_sin_cambios"] = True
    a.salida.parent.mkdir(parents=True, exist_ok=True)
    a.salida.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps({k: {f: v[f] for f in ("6", "7", "8")} for k, v in out["resultados"].items()}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
