#!/usr/bin/env python3
"""Auditoría interna 4.9: mutaciones adicionales a las 15 de mutar_rv1.py (solo temporales en /home/claude/auditoria_4_9/tmp).
Una mutación NO DETECTADA (la batería sigue 63/63) indica una propiedad que la batería no comprueba."""
import json, os, shutil, subprocess, sys, tempfile

RAIZ = "/home/claude/auditoria_4_9/munger_v2_r1"
SCR = os.path.join(RAIZ, "personaje_v2", "scripts")
BAT = os.path.join(RAIZ, "personaje_v2", "pruebas", "test_integridad_auditoria_v2.py")
TMP = "/home/claude/auditoria_4_9/tmp/tmpdir"
MUT = [
    ("X1", "cierre_v2.py", "texto_fiel usa NFKC (equivalencia de compatibilidad, no canónica) en vez de NFC",
     'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return unicodedata.normalize("NFKC", t).rstrip("\\n")'),
    ("X2", "cierre_v2.py", "texto_fiel quita todos los espacios finales del archivo, no solo los saltos",
     'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return unicodedata.normalize("NFC", t).rstrip()'),
    ("X3", "cierre_v2.py", "texto_fiel elimina caracteres de formato invisibles (categoría Cf: ZWSP, BOM interior…)",
     'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return "".join(c for c in unicodedata.normalize("NFC", t) if unicodedata.category(c) != "Cf").rstrip("\\n")'),
    ("X4", "cierre_v2.py", "sin estado del pipeline se ignora la huella fiel de cierre_vigente.json (vuelve la comparación de bytes)",
     'if cv.get("auditoria_fiel") and cv.get("solicitud"):', 'if False:'),
    ("X5", "cierre_v2.py", "texto_fiel convierte los espacios no separables en espacios",
     'return unicodedata.normalize("NFC", t).rstrip("\\n")', 'return unicodedata.normalize("NFC", t).replace("\\u00a0", " ").rstrip("\\n")'),
    ("X6", "cierre_v2.py", "no se comprueba que la respuesta aceptada sea del material fijado (resp/sol)",
     'if resp.get("material") != fij or sol.get("material") != fij:', 'if False:'),
    ("X7", "cierre_v2.py", "texto_fiel trata los separadores de línea Unicode (VT, FF, U+2028…) como saltos",
     't = t.replace("\\r\\n", "\\n").replace("\\r", "\\n")', 't = "\\n".join(t.splitlines()) + ("\\n" if t.endswith(("\\n", "\\r")) else "")'),
]


def main():
    res = []
    for mid, arch, desc, viejo, nuevo in MUT:
        with tempfile.TemporaryDirectory(prefix=f"mutx_{mid}_", dir=TMP) as d:
            for f in ("cierre_v2.py", "pipeline.py"):
                shutil.copy2(os.path.join(SCR, f), os.path.join(d, f))
            p = os.path.join(d, arch)
            s = open(p, encoding="utf-8").read()
            assert s.count(viejo) == 1, (mid, s.count(viejo))
            open(p, "w", encoding="utf-8").write(s.replace(viejo, nuevo))
            r = subprocess.run([sys.executable, "-B", BAT, "--codigo", d], capture_output=True, text=True, env={**os.environ, "TMPDIR": TMP, "PYTHONDONTWRITEBYTECODE": "1"})
            ult = (r.stdout.strip().splitlines() or [""])[-1]
            fallan = [l[:160] for l in r.stdout.splitlines() if l.startswith("FALLA")]
            res.append({"id": mid, "descripcion": desc, "detectada": r.returncode != 0, "resultado": ult, "fallan": fallan})
            print(mid, "DETECTADA" if r.returncode != 0 else "NO DETECTADA", "·", ult, "·", desc, flush=True)
    json.dump(res, open("/home/claude/auditoria_4_9/tmp/mutar_extra.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    main()
