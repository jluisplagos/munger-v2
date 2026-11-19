#!/usr/bin/env python3
"""Pruebas de las acciones exactas de los metadatos (Análisis!C55; examen, zoetis_t1c; rama producto/minoritarios-acciones).

Zoetis: el 10-K 2025 (p. 68) da 424.927.535 acciones en circulación y los metadatos guardaban 424,928 millones (redondeo a 3 decimales,
que solo vale para importes: verificacion_entradas, N4). Ningún script redondeaba: la cifra llegaba redondeada y nada lo detectaba.
Ahora los metadatos pueden traer la cifra impresa («impreso», su «escala_impreso» y la «dilucion» impresa) y construir se detiene si «valor» no es exactamente esa cifra
en millones; sin «impreso» (metadatos anteriores) todo sigue igual. El libro escribe el valor por su repr (v63_xml), sin redondear.
No escribe en el repositorio: trabaja sobre copias temporales.
Uso: python3 -B pruebas/test_acciones_metadatos_exactas.py      (código 0 si todo pasa)
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
import fase1_historia as F  # noqa: E402
import v63_xml  # noqa: E402

ZOETIS = os.path.join(PV, "empresas_v2_correcciones", "2026-11_examen_universo", "zoetis_t1c", "Zoetis")
PARTES = ("texto", "fase1_partes", "fase1_metadatos.json", "fase1_fuentes.json", "fase1_decisiones.json")
fallos, total = [], 0


def paso(nombre, ok, detalle=""):
    global total
    total += 1
    print(("PASA " if ok else "FALLA") + f" · {nombre}" + (f" · {detalle}" if detalle else ""))
    if not ok:
        fallos.append(nombre)


def defectos(ac):
    """Los defectos, o None si la comprobación no existe (código anterior): None hace fallar toda comprobación, con o sin defecto."""
    try:
        return F.defecto_acciones_meta(ac)
    except AttributeError as ex:
        print(f"      (sin comprobación: {ex})")
        return None


def sin_defecto(ac):
    return defectos(ac) == []


def defecto(ac, *textos):
    """Un único defecto y por el motivo esperado (cada texto tiene que estar en él)."""
    d = defectos(ac)
    return isinstance(d, list) and len(d) == 1 and all(t in d[0] for t in textos), d


def caso(nombre, r):
    ok, d = r if isinstance(r, tuple) else (r, None)
    paso(nombre, ok, "" if d is None else "; ".join(d) if isinstance(d, list) else repr(d))


Z = {"impreso": "424.927.535", "escala_impreso": "unidades"}
# 1 · la comprobación
caso("424.927.535 acciones con valor 424,928: defecto (redondeado)", defecto(dict(Z, valor=424.928), "424.927535", "no se redondea"))
caso("424.927.535 con valor 424,927535: sin defecto", sin_defecto(dict(Z, valor=424.927535)))
caso("escala_impreso por omisión «unidades»", sin_defecto({"valor": 424.927535, "impreso": "424,927,535"}))
caso("(C1) «unidad» es la de «valor» («millones de acciones», como Ahold) y no bloquea con «impreso»",
     sin_defecto({"valor": 886.877, "unidad": "millones de acciones", "impreso": "886,877", "escala_impreso": "miles"}))
caso("(C1) y la escala de «impreso» no se toma de «unidad»: «unidad» «millones» con «impreso» 424.927.535 en unidades",
     sin_defecto(dict(Z, valor=424.927535, unidad="millones")))
caso("escala «millones» («905» → 905)", sin_defecto({"valor": 905, "impreso": "905", "escala_impreso": "millones"}))
caso("escala «miles» («1.500» → 1,5)", sin_defecto({"valor": 1.5, "impreso": "1.500", "escala_impreso": "miles"}))
caso("cifra en unidades tomada como millones (424.927,535): defecto", defecto(dict(Z, valor=424927.535), "no es la cifra impresa", "424.927535"))
caso("(C4) «424.928» en millones: defecto con aviso del separador de miles",
     defecto({"valor": 424.928, "impreso": "424.928", "escala_impreso": "millones"}, "separador de miles", "424.927.535"))
caso("escala que no es de la lista: defecto", defecto(dict(Z, valor=1, escala_impreso="docenas"), "escala_impreso", "no es una de"))
caso("impreso que no es texto: defecto", defecto({"valor": 424.927535, "impreso": 424927535}, "tal como se imprime"))
caso("impreso no numérico: defecto", defecto({"valor": 1, "impreso": "12a"}, "no numérico"))
caso("valor booleano o ausente: defecto", (defecto({"valor": True, "impreso": "1"}, "no es la cifra impresa")[0]
                                          and defecto({"impreso": "1"}, "valor None")[0], None))
caso("impreso cero o guion: defecto (no es un número positivo de acciones)", defecto({"valor": 0, "impreso": "-"}, "número positivo"))
caso("(C2) dilución: circulación + componentes impresos, cada uno con su escala, suma exacta",
     sin_defecto(dict(Z, valor=426.127535, dilucion=[{"impreso": "1.000.000", "escala_impreso": "unidades", "pagina": 70, "concepto": "RSU"},
                                                     {"impreso": "200", "escala_impreso": "miles", "pagina": 70, "concepto": "opciones"}])))
caso("(C2) dilución sumada en valor sin declarar sus componentes: defecto", defecto(dict(Z, valor=426.127535), "no es la cifra impresa"))
caso("(C2) dilución redondeada: defecto que nombra la dilución", defecto(dict(Z, valor=426.128, dilucion=[{"impreso": "1.200.000"}]),
                                                                       "más 1 componentes de dilución", "426.127535"))
caso("(C2) componente de dilución mal formado: defecto", defecto(dict(Z, valor=1, dilucion=[{"impreso": "x"}]), "dilución 1"))
caso("(C2) «dilucion» que no es una lista: defecto", defecto(dict(Z, valor=1, dilucion="1.200.000"), "tiene que ser una lista"))
caso("metadatos sin «impreso» (anteriores a la regla): no bloquean", sin_defecto({"valor": 424.928}) and sin_defecto(None))

# 2 · el libro escribe el valor exacto (repr), sin redondear (documenta lo que ya hacía v63_xml; no prueba el cambio)
paso("v63_xml escribe 424.927535 tal cual", v63_xml._texto_numero(424.927535) == "424.927535", v63_xml._texto_numero(424.927535))

# 3 · la instrucción del agente de metadatos
prm = open(os.path.join(PV, "prompts", "metadatos_fase1.md"), encoding="utf-8").read()
paso("el prompt de metadatos pide «impreso», «escala_impreso», «dilucion» y el valor con todos sus decimales", all(x in prm for x in (
    "`impreso`", "`escala_impreso`", "`dilucion`", "TODOS sus decimales", "nunca redondeada", "`unidad` es la de `valor`")))
paso("(C3) y la capitalización sin redondear el resultado", "sin redondear el resultado" in prm)


# 4 · construir sobre copias de zoetis_t1c
def copiar(dest):
    os.makedirs(dest)
    for n in PARTES:
        s = os.path.join(ZOETIS, n)
        if os.path.isdir(s):
            shutil.copytree(s, os.path.join(dest, n))
        elif os.path.exists(s):
            shutil.copy2(s, os.path.join(dest, n))
    return dest


def construir_con(c, cambio):
    mp = os.path.join(c, "fase1_metadatos.json")
    m = json.load(open(mp, encoding="utf-8"))
    cambio(m["acciones_diluidas"])
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    r = subprocess.run([sys.executable, "-B", os.path.join(PV, "scripts", "fase1_historia.py"), "construir", c], capture_output=True, text=True)
    f = os.path.join(c, "fase1_v63.json")
    return r.returncode, (r.stdout + r.stderr).strip(), (json.load(open(f, encoding="utf-8")) if os.path.exists(f) else None)


t = tempfile.mkdtemp(prefix="acciones_meta_")
try:
    if os.path.isdir(os.path.join(ZOETIS, "fase1_partes")) and os.path.isdir(os.path.join(ZOETIS, "texto")):
        rc, out, f1 = construir_con(copiar(os.path.join(t, "redondeada", "Zoetis")), lambda a: a.update(**Z))
        paso("zoetis_t1c con «impreso» 424.927.535 y valor 424,928: construir se detiene sin escribir fase1_v63.json",
             rc == 1 and f1 is None and "no se redondea" in out, out[-220:])
        rc, out, f1 = construir_con(copiar(os.path.join(t, "exacta", "Zoetis")), lambda a: a.update(valor=424.927535, **Z))
        v = f1 and f1["acciones_diluidas"]["valor"]
        paso("zoetis_t1c con la cifra exacta: construye y fase1_v63.json lleva C55 = 424,927535", rc == 0 and v == 424.927535 and repr(v) == "424.927535",
             repr(v) if rc == 0 else out[-200:])
        rc, out, f1 = construir_con(copiar(os.path.join(t, "anterior", "Zoetis")), lambda a: None)
        v = f1 and f1["acciones_diluidas"]["valor"]
        ref = json.load(open(os.path.join(ZOETIS, "fase1_v63.json"), encoding="utf-8"))["acciones_diluidas"]["valor"]
        paso("zoetis_t1c con sus metadatos de hoy (sin «impreso»): construye igual que antes (424,928)", rc == 0 and v == ref == 424.928,
             repr(v) if rc == 0 else out[-200:])
        rev = open(os.path.join(t, "anterior", "Zoetis", "historia_revision.md"), encoding="utf-8").read()
        paso("(C2) y historia_revision.md avisa de que falta «impreso»", "AVISO: los metadatos no traen «impreso»" in rev)
        paso("(extra) historia_revision.md avisa del signo de los minoritarios impresos (2) y (6) que la Historia guarda en positivo",
             "## Signo de saldos impresos en negativo" in rev and "**minoritarios 2022**" in rev and "**minoritarios 2023**" in rev
             and f1["historia"]["partidas"]["minoritarios"]["valores"][f1["historia"]["anios"].index(2022)] == 2.0
             and "**pensiones" not in rev, "(la conversión no cambia; pensiones, posición neta, no se avisa)")
        rc, out, f1 = construir_con(copiar(os.path.join(t, "c1", "Zoetis")), lambda a: a.update(valor=424.927535, unidad="millones de acciones", **Z))
        rev = open(os.path.join(t, "c1", "Zoetis", "historia_revision.md"), encoding="utf-8").read()
        paso("(C1) con «unidad» «millones de acciones» e «impreso»: construye, conserva la unidad del valor y lo da por comprobado",
             rc == 0 and f1["acciones_diluidas"]["unidad"] == "millones de acciones" and "comprobado exacto contra la cifra impresa" in rev, out[-200:])
        def sin_capitalizacion(a):
            a.update(valor=424.927535, **Z)
        c3 = copiar(os.path.join(t, "c3", "Zoetis"))
        mp = os.path.join(c3, "fase1_metadatos.json")
        m = json.load(open(mp, encoding="utf-8")); m.pop("capitalizacion", None); m["precio"]["valor"] = 73.08
        json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        rc, out, f1 = construir_con(c3, sin_capitalizacion)
        v = f1 and f1["capitalizacion"]["valor"]
        paso("(C3) capitalización de respaldo exacta: 73,08 × 424,927535 = 31.053,7042578 (antes 31.053,7)",
             rc == 0 and F.Fraction(repr(v)) == F.Fraction("31053.7042578"), repr(v) if rc == 0 else out[-200:])
    else:  # el expediente del examen no forma parte de todos los paquetes: sin él, la prueba real se omite y lo dice
        print(f"OMITIDA · construir sobre zoetis_t1c: no está el expediente {ZOETIS}")
finally:
    shutil.rmtree(t, ignore_errors=True)

print(f"\n{total - len(fallos)}/{total} comprobaciones PASAN")
sys.exit(1 if fallos else 0)
