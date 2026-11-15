#!/usr/bin/env python3
"""Mutaciones de la reparación R-V1 (entrega 4.9). Solo trabaja en temporales.

Uso: python3 -I -B mutar_rv1.py [--salida ARCHIVO.json]   (unos 10 minutos; no usa LibreOffice)

Cada mutación cambia UNA cosa de cierre_v2.py o pipeline.py del árbol (en una copia temporal) y ejecuta
pruebas/test_integridad_auditoria_v2.py con --codigo sobre esa copia. Una mutación queda DETECTADA si la batería falla (código ≠ 0);
se registran las pruebas que fallan. Si alguna mutación no se detecta, el código de salida es 1.
"""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", "..", "..", ".."))
SCR = os.path.join(RAIZ, "personaje_v2", "scripts")
BAT = os.path.join(RAIZ, "personaje_v2", "pruebas", "test_integridad_auditoria_v2.py")

MUTACIONES = [
    ("M01", "cierre_v2.py", "la identidad vuelve a aceptarse por el detector (huella de contenido sin orden), como en la 4.8.1",
     'm = motivo_respuesta_no_aceptada(carpeta, datos, st, resp)',
     'm = None if (resp.get("contenido") or "") == huella_contenido(txt) else motivo_respuesta_no_aceptada(carpeta, datos, st, resp)'),
    ("M02", "cierre_v2.py", "sin línea de solicitud se supone la registrada", "ids = lineas_solicitud(txt)\n", 'ids = lineas_solicitud(txt) or [resp.get("solicitud")]\n'),
    ("M03", "cierre_v2.py", "se admiten líneas de solicitud duplicadas si nombran la misma", "if len(ids) > 1:", "if len(set(ids)) > 1:"),
    ("M04", "cierre_v2.py", "no se compara el identificador de la solicitud", 'if ids[0] != resp.get("solicitud"):', 'if False and ids[0] != resp.get("solicitud"):'),
    ("M05", "cierre_v2.py", "no se compara la huella fiel", 'if huella_fiel(datos) != resp["fiel"]:', "if False:"),
    ("M06", "cierre_v2.py", "la huella fiel no tiene en cuenta el orden de las líneas", 'return unicodedata.normalize("NFC", t).rstrip("\\n")',
     'return "\\n".join(sorted(unicodedata.normalize("NFC", t).rstrip("\\n").split("\\n")))'),
    ("M07", "cierre_v2.py", "CRLF y CR dejan de ser transformaciones admitidas", 't = t.replace("\\r\\n", "\\n").replace("\\r", "\\n")', "t = t"),
    ("M08", "cierre_v2.py", "los espacios al final de línea pasan a ser inocuos (no lo son)", 'return unicodedata.normalize("NFC", t).rstrip("\\n")',
     'return re.sub(r"[ \\t]+(?=\\n)", "", unicodedata.normalize("NFC", t)).rstrip("\\n")'),
    ("M09", "cierre_v2.py", "un cierre de la 4.8.1 sin huella fiel se acredita por el contenido sin orden, no por los bytes",
     'elif hashlib.sha256(datos).hexdigest() != resp.get("sha256"):', 'elif huella_contenido(texto_fiel(datos) or "") != resp.get("contenido"):'),
    ("M10", "cierre_v2.py", "cierre_vigente.json deja de registrar la solicitud y la huella fiel", 'reg.update(solicitud=resp.get("solicitud"), auditoria_fiel=resp["fiel"])', "pass"),
    ("M11", "cierre_v2.py", "sin estado del pipeline, cierre_vigente.json solo compara la solicitud", 'if ids != [cv["solicitud"]] or huella_fiel(datos) != cv["auditoria_fiel"]:',
     'if ids != [cv["solicitud"]]:'),
    ("M12", "cierre_v2.py", "no se comprueba que la solicitud conste como respondida por esa respuesta",
     'if not sol or sol.get("estado") != "respondida" or sol.get("respuesta_sha256") != resp.get("sha256"):', "if not sol:"),
    ("M13", "pipeline.py", "el paso 13 no registra la huella fiel de la respuesta aceptada", 'hf = CIE.huella_fiel(open(destino, "rb").read())', "hf = None"),
    ("M14", "cierre_v2.py", "el BOM deja de ser una transformación admitida", 'if datos.startswith(b"\\xef\\xbb\\xbf"):\n        datos = datos[3:]', "pass"),
    ("M15", "cierre_v2.py", "NFC/NFD deja de ser una transformación admitida", 'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return t.rstrip("\\n")'),
    # (auditoría interna de la 4.9, Z-3) límites de la lista cerrada de transformaciones inocuas
    ("M16", "cierre_v2.py", "la huella fiel normaliza con NFKC en lugar de NFC (iguala «²» y «2»)", 'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return unicodedata.normalize("NFKC", t).rstrip("\\n")'),
    ("M17", "cierre_v2.py", "la huella fiel elimina los caracteres de formato (U+200B y otros)", 'return unicodedata.normalize("NFC", t).rstrip("\\n")',
     'return "".join(ch for ch in unicodedata.normalize("NFC", t) if unicodedata.category(ch) != "Cf").rstrip("\\n")'),
    ("M18", "cierre_v2.py", "la huella fiel convierte el espacio no separable en un espacio", 'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return unicodedata.normalize("NFC", t).replace("\\u00a0", " ").rstrip("\\n")'),
    ("M19", "cierre_v2.py", "la huella fiel trata VT, FF y U+2028 como saltos de línea", 't = t.replace("\\r\\n", "\\n").replace("\\r", "\\n")', 't = "\\n".join(t.splitlines())'),
    ("M20", "cierre_v2.py", "sin estado del pipeline, se ignora la huella fiel de cierre_vigente.json (solo bytes)", 'if cv.get("auditoria_fiel") and cv.get("solicitud"):', 'if False:'),
    # (Z-1) sin registro de la respuesta aprobada
    ("M21", "cierre_v2.py", "sin ningún registro de la respuesta aprobada se acepta cualquier APROBADO del material (comportamiento anterior)", 'elif not cv.get("auditoria_sha256"):', 'elif False:'),
    # (Z-2) archivos que no se pueden leer
    ("M22", "cierre_v2.py", "un auditoria.md que no es UTF-8 vuelve a interrumpir las vías", '        txt = datos.decode("utf-8")\n    except UnicodeDecodeError:\n',
     '        txt = datos.decode("utf-8")\n    except KeyError:\n'),
    ("M23", "cierre_v2.py", "un cierre_vigente.json ilegible deja de ser motivo de retirada", '    if err_cv:\n        return', '    if False:\n        return'),
    # (control de vigencia de la 4.9, V-1 a V-3)
    ("M24", "cierre_v2.py", "un material_auditoria.json ilegible deja de ser motivo de retirada",
     'm = err_f and f"{err_f}: no consta qué material se aprobó; la aprobación se retira" or _motivo_estructura(st, cv, fij)', "m = _motivo_estructura(st, cv, fij)"),
    ("M25", "cierre_v2.py", "un JSON válido que no es un objeto vuelve a aceptarse como archivo de control", "    if not isinstance(obj, dict):", "    if False:"),
    ("M26", "cierre_v2.py", "una ficha.json ilegible vuelve a tomarse por «sin salida cerrada»", "    if err_f:", "    if False:"),
    ("M27", "cierre_v2.py", "sin estado, registrar_cierre vuelve a registrar la huella del archivo actual y pierde la solicitud y la huella fiel",
     'elif not resp and previo.get("auditoria_fiel")', 'elif False and previo.get("auditoria_fiel")'),
    ("M28", "pipeline.py", "un estado_pipeline.json que es una carpeta vuelve a interrumpir el pipeline", "except (ValueError, OSError) as e:", "except ValueError as e:"),
    # (segundo control de vigencia de la 4.9, W-1, W-2 y W-4)
    ("M29", "cierre_v2.py", "una ficha con «cierre» que no es un objeto vuelve a aceptarse", '    if F is not None and F.get("cierre") is not None and not isinstance(F.get("cierre"), dict):', "    if False:"),
    ("M30", "ficha.py", "ficha.py vuelve a cerrar sobre una ficha oficial ilegible", '        if vieja_ilegible or (vieja and vieja.get("cierre") is not None and not isinstance(vieja.get("cierre"), dict)):', "        if False:"),
    ("M31", "cierre_v2.py", "el identificador del material vuelve a usarse sin limpiar en la ruta del archivo", 're.sub(r"[^0-9A-Za-z_-]", "_", str(mat or "sin_material"))', 'str(mat or "sin_material")'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--salida", default=os.path.join(AQUI, "..", "resultados", "mutaciones_rv1.json"))
    a = ap.parse_args()
    res = []
    for mid, arch, desc, viejo, nuevo in MUTACIONES:
        with tempfile.TemporaryDirectory(prefix=f"mut_{mid}_") as d:
            for f in sorted({"cierre_v2.py", "pipeline.py", arch}):
                shutil.copy2(os.path.join(SCR, f), os.path.join(d, f))
            p = os.path.join(d, arch)
            s = open(p, encoding="utf-8").read()
            n = s.count(viejo)
            if n != 1:
                res.append({"id": mid, "descripcion": desc, "aplicada": False, "detectada": False, "motivo": f"el texto a mutar aparece {n} veces"})
                print(f"{mid} NO APLICADA ({n} apariciones) · {desc}", flush=True)
                continue
            open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
            r = subprocess.run([sys.executable, "-B", BAT, "--codigo", d], capture_output=True, text=True, timeout=1800)
            fallan = [l[8:].split(" · ")[0] + " · " + l[8:].split(" · ")[1][:110] for l in r.stdout.splitlines() if l.startswith("FALLA")]
            final = (r.stdout.strip().splitlines() or [""])[-1]
            res.append({"id": mid, "archivo": arch, "descripcion": desc, "aplicada": True, "detectada": r.returncode != 0, "resultado_bateria": final, "pruebas_que_fallan": fallan})
            print(f"{mid} {'DETECTADA' if r.returncode != 0 else 'NO DETECTADA'} · {final} · {desc}", flush=True)
    n = sum(x["detectada"] for x in res)
    json.dump({"bateria": os.path.relpath(BAT, RAIZ), "mutaciones": res, "detectadas": n, "total": len(res)},
              open(os.path.abspath(a.salida), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"{n} de {len(res)} mutaciones detectadas")
    sys.exit(0 if n == len(res) else 1)


if __name__ == "__main__":
    main()
