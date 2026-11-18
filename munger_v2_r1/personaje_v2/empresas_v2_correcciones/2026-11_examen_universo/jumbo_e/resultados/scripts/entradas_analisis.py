#!/usr/bin/env python3
"""Entradas de Análisis recalculadas o con la evidencia reescrita sobre un expediente ya preparado (examen, orquestación, 18-nov-2026).
Hace lo que cambiar_base.py hace con una entrada `analisis` (vaciar en la copia de ensayo de la etapa 1 + evidencia de Control maestro +
entrada declarada en fase1_metadatos.json) y, para «solo_evidencia», reescribe columnas de Control maestro (E–N) sin tocar el valor.
Guarda antes la copia de la etapa 1, los metadatos y los textos anteriores en ANTECEDENTES/<etiqueta>/ y comprueba que solo cambian las celdas
declaradas. Uso: python3 -I entradas_analisis.py CARPETA_EMPRESA CARPETA_ANTECEDENTES ETIQUETA ESPEC.json REGISTRO.json
ESPEC: {"declarar": {"C40": {"valor": 0, "esperado": 0, "L": "…", "M": "…", "N": "…", "periodo": "…", "unidad": "…"}},
        "solo_evidencia": {"C88": {"F": "Dato no verificable", "N": "…"}}}"""
import glob, hashlib, json, os, shutil, sys
C, ANT, TAG, ESP, REG = sys.argv[1:6]
sys.path.insert(0, os.path.abspath(os.path.join(C, *[".."] * 4, "scripts")))
from v63_xml import LibroV63  # noqa: E402
import cambiar_base as CB  # noqa: E402
import openpyxl  # noqa: E402
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
esp = json.load(open(ESP, encoding="utf-8"))
e1 = glob.glob(os.path.join(C, "etapa1", "*.xlsx"))
assert len(e1) == 1
e1 = e1[0]
dst = os.path.join(ANT, TAG)
os.makedirs(dst)
meta_p = os.path.join(C, "fase1_metadatos.json")
shutil.copy2(e1, os.path.join(dst, os.path.basename(e1)))
shutil.copy2(meta_p, os.path.join(dst, "fase1_metadatos.json"))
meta = json.load(open(meta_p, encoding="utf-8"))
lb = LibroV63(e1)
antes, cambiadas = {}, set()
for c, d in (esp.get("declarar") or {}).items():
    a = lb.leer("Análisis", c)
    prev = (meta.get("analisis") or {}).get(c, {}).get("valor")
    actual = prev if a is None else a
    assert actual is not None and abs(float(actual) - float(d["esperado"])) <= 1e-3 * max(1, abs(float(d["esperado"]))), (c, a, prev, d["esperado"])
    antes[f"Análisis!{c}"] = a if a is not None else f"(vacío en la etapa 1; entrada declarada anterior {prev!r})"
    if a is not None:
        lb.escribir("Análisis", c, None)
        lb.marcar_modificada("Análisis")
        cambiadas.add(f"Análisis!{c}")
for grupo in ("declarar", "solo_evidencia"):
    for c, d in (esp.get(grupo) or {}).items():
        r = CB.fila_de(lb, "Control maestro", f"Análisis!{c}")
        assert r, c
        for col in "EFGHIJKLMN":
            if col in d:
                antes[f"Control maestro!{col}{r}"] = lb.leer("Control maestro", f"{col}{r}")
                lb.escribir("Control maestro", f"{col}{r}", d[col], tipo="texto")
                cambiadas.add(f"Control maestro!{col}{r}")
        lb.marcar_modificada("Control maestro")
lb.guardar(e1)
wo, wn = openpyxl.load_workbook(os.path.join(dst, os.path.basename(e1)), data_only=True), openpyxl.load_workbook(e1, data_only=True)
otras = [f"{s}!{x.coordinate}" for s in wo.sheetnames for f in wo[s].iter_rows() for x in f if f"{s}!{x.coordinate}" not in cambiadas and wn[s][x.coordinate].value != x.value]
assert not otras, otras[:10]
for c, d in (esp.get("declarar") or {}).items():
    meta.setdefault("analisis", {})[c] = {"valor": d["valor"], "fuente": d["M"], "pagina": d["L"], "periodo": d.get("periodo"), "unidad": d.get("unidad")}
json.dump(meta, open(meta_p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
json.dump({"valores_y_textos_anteriores": antes}, open(os.path.join(dst, "evidencia_anterior.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
json.dump({"fecha": "2026-11-18", "guion": os.path.abspath(__file__), "especificacion": esp, "antes": antes, "celdas_cambiadas": sorted(cambiadas),
           "etapa1_antes_sha256": h(os.path.join(dst, os.path.basename(e1))), "etapa1_despues_sha256": h(e1)},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
print("OK", sorted(cambiadas))
