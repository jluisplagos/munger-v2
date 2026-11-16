#!/usr/bin/env python3
"""c9 · T9 (cuarta comprobación): la anotación de «material_refijado» en el paso 13 con la bandera «relevo_por_refijar». NO se ejecuta
pipeline.py ni ningún paso: se EXTRAEN del código de cada candidata (texto de pipeline.py) las líneas que siguen a
«st["material_auditoria"] = CIE.fijar_material(…)» hasta «self.guardar()» y se ejecutan sobre un estado escrito por la sonda.
(La sección 5 de r16 llevaba esas líneas copiadas a mano de la candidata anterior; aquí salen del archivo.)
Uso: python3 -I -B c9_relevo_refijar.py"""
import copy, os, re, sys, textwrap
F = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def lineas_paso13(arbol):
    src = open(os.path.join(F, arbol, "munger_v2_r1", "personaje_v2", "scripts", "pipeline.py"), encoding="utf-8").read()
    i = src.index('st["material_auditoria"] = CIE.fijar_material(self.c, self.E)')
    i = src.index("\n", i) + 1
    j = src.index("self.guardar()", i)
    j = src.rfind("\n", 0, j) + 1
    return textwrap.dedent(src[i:j])


def deteccion(arbol):
    src = open(os.path.join(F, arbol, "munger_v2_r1", "personaje_v2", "scripts", "pipeline.py"), encoding="utf-8").read()
    i = src.index('st["relevos_caducados"].append({"material_fijado": fijado')
    j = src.index('st["paso"] = 12', i)
    return src[i:j]


A, B, C = "a" * 16, "b" * 16, "c" * 16
REL = {"material_fijado": A, "material_vigente": B, "archivos_cambiados": ["verificacion_entradas.json"], "detectado": "2026-11-15T11:00:00+00:00"}
CASOS = [
    ("1 relevo recién detectado (sin material_refijado; la detección puso la bandera) y el paso 13 fija B", {"relevos_caducados": [dict(REL)], "relevo_por_refijar": True, "material_auditoria": B}),
    ("2 relevo ANTERIOR a esta candidata (ya con «solicitud», sin material_refijado, sin bandera) y el paso 13 fija C por otra causa (T9)",
     {"relevos_caducados": [dict(REL, solicitud="SA-000000000000000f")], "material_auditoria": C}),
    ("3 relevo ya anotado (B) y el paso 13 fija C por otra causa, sin bandera", {"relevos_caducados": [dict(REL, material_refijado=B, solicitud="SA-1")], "material_auditoria": C}),
    ("4 dos relevos seguidos antes de fijar (bandera puesta): se anota solo el último", {"relevos_caducados": [dict(REL), dict(REL, material_fijado=B, material_vigente=C)], "relevo_por_refijar": True, "material_auditoria": C}),
    ("5 bandera puesta y relevos_caducados vacío o mal formado", {"relevos_caducados": [], "relevo_por_refijar": True, "material_auditoria": B}),
    ("6 bandera puesta y el último relevo no es un objeto", {"relevos_caducados": ["x"], "relevo_por_refijar": True, "material_auditoria": B}),
    ("7 sin relevos", {"material_auditoria": B}),
]
for arbol, nombre in (("prev", "anterior (f3d15e8)"), ("copia", "cuarta (7a6583b)")):
    cod = lineas_paso13(arbol)
    print(f"== {nombre}: líneas del paso 13 tras fijar el material\n" + textwrap.indent(cod.rstrip(), "      | "))
    print("   la detección del relevo pone la bandera:", 'st["relevo_por_refijar"] = True' in deteccion(arbol))
    for titulo, st0 in CASOS:
        st = copy.deepcopy(st0)
        try:
            exec(cod, {}, {"st": st})
            err = None
        except Exception as ex:  # noqa: BLE001
            err = f"{type(ex).__name__}: {ex}"
        rels = st.get("relevos_caducados")
        ref = [r.get("material_refijado") if isinstance(r, dict) else "—" for r in rels] if isinstance(rels, list) else rels
        print(f"   {titulo}\n      → material_refijado de cada relevo: {ref} · bandera después: {st.get('relevo_por_refijar', '(sin bandera)')}" + (f" · EXCEPCIÓN {err}" if err else ""))
    print()
