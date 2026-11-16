#!/usr/bin/env python3
"""Testigos de las mutaciones NO detectadas de verificacion_entradas.py (cuarta comprobación): para cada una, una entrada concreta con la
que el código mutado da otro resultado que el de la candidata. Sirve para descartar que la mutación sea equivalente (que no cambie nada):
si hay testigo, la regla cambia de verdad y ninguna prueba de las baterías lo ve. El módulo mutado se carga en memoria con el mismo
cambio de texto que usa mutaciones4.py; no se escribe ningún árbol.   Uso: python3 -I -B mutaciones4_testigos.py"""
import importlib.util, os, sys, tempfile, time, types
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "sondas3"))
from comun3 import VE, F  # noqa: E402
spec = importlib.util.spec_from_file_location("mutaciones4", os.path.join(os.path.dirname(os.path.abspath(__file__)), "mutaciones4.py"))
M4 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M4)
SRC = open(VE.__file__, encoding="utf-8").read()
TMP = tempfile.mkdtemp(prefix="rev4_testigos_", dir=os.path.join(F, "tmp"))


def mutado(nombre):
    s = SRC
    for arch, viejo, nuevo in M4.M[nombre][3]:
        assert arch == M4.VEP and s.count(viejo) == 1
        s = s.replace(viejo, nuevo)
    m = types.ModuleType("ve_" + nombre)
    m.__file__ = VE.__file__
    exec(compile(s, VE.__file__ + "[" + nombre + "]", "exec"), m.__dict__)
    return m


def html(M, contenido, ext=".html", binario=None):
    p = os.path.join(TMP, f"t{len(os.listdir(TMP))}{ext}")
    open(p, "wb").write(binario if binario is not None else contenido.encode("utf-8"))
    e, t = M._texto_html_visible(p)
    return "pendiente" if e != "ok" else ("presente" if "849697.000" in t else "ausente")


def coste(M):
    pag = " ".join(["2024"] * 1500) + "\n"
    t0 = time.time()
    r = M._cita_cifra("2024", 2024, pag)[0]
    return f"{r} en {'menos de 2 s' if time.time() - t0 < 2 else 'más de 2 s'}"


XN = 'xmlns="http://www.w3.org/1999/xhtml"'
TESTIGOS = {
    "t1b_search_en_vez_de_fullmatch": ("_unidad_monetaria_no_reconocida('importe en USD por EUR al cierre')", lambda M: M._unidad_monetaria_no_reconocida("importe en USD por EUR al cierre")),
    "t1c_sin_palabra_de_escala": ("_unidad_monetaria_no_reconocida('meur/keur')", lambda M: M._unidad_monetaria_no_reconocida("meur/keur")),
    "t2e_sin_limite_final_letra": ("_cita_cifra('Ventas 849,7 mill', 849.7, 'Ventas 849,7 millones')", lambda M: M._cita_cifra("Ventas 849,7 mill", 849.7, "Ventas 849,7 millones\n")[0]),
    "t2b_sin_limite_inicial_cifra": ("_cita_cifra('849,7', 849.7, 'Ventas 849,7 / Total 5.849,7')", lambda M: M._cita_cifra("849,7", 849.7, "Ventas 849,7\nTotal 5.849,7\n")[0]),
    "t2d_sin_limite_final_cifra": ("_cita_cifra('Total 849', 849, 'Total 849 / Total 849.697')", lambda M: M._cita_cifra("Total 849", 849, "Total 849\nTotal 849.697\n")[0]),
    "t2h_en_numero_sin_inicio": ("_cita_cifra('697.000', 697, 'Total 849,697.000')", lambda M: M._cita_cifra("697.000", 697, "Total 849,697.000\n")[0]),
    "t2i_en_numero_sin_final": ("_cita_cifra('Total 849697', 849697, 'Total 8496970')", lambda M: M._cita_cifra("Total 849697", 849697, "Total 8496970\n")[0]),
    "t3a_xhtml_por_contenido": (".html con el xmlns y <div hidden/> antes del texto", lambda M: html(M, f"<html {XN}><body><div hidden/><p>Partida: 849697.000</p></body></html>")),
    "t3d_codecs_por_prefijos": ("documento que declara charset=cp875 con el texto en EBCDIC", lambda M: html(M, "", binario=b'<meta charset="cp875">' + "Partida: 849697.000".encode("cp875"))),
    "t4b_html_con_invisibles": ("lectura de «849697.000 total» en el texto del HTML «-849697.000 to<U+00AD>tal» (lo que entra en textos_fuente)", None),
    "n10c_sin_recorte_400": ("coste: línea única con 1.500 apariciones de la cita «2024»", coste),
    "n4_solapa": ("_cita_cifra('Total 849.', 849697, 'Total 849.697')", lambda M: M._cita_cifra("Total 849.", 849697, "Total 849.697\n")[0]),
    "n3c_solo_signo_distinto": None, "n3d_solo_layout": None, "n3e_solo_sin_layout": None, "t4c_pendiente_aunque_un_texto_lea": None,
    "n5c_sin_limite_antes": ("_cita_cifra('Flujo 1.234-567', 567, 'Flujo 1.234-567')", lambda M: M._cita_cifra("Flujo 1.234-567", 567, "Flujo 1.234-567\n")[0]),
    "t8c_sin_fecha": ("_cita_cifra('Cierre 31-12-2024', 2024, …)", lambda M: M._cita_cifra("Cierre 31-12-2024", 2024, "Cierre 31-12-2024\n")[0]),
    "t8d_fecha_cualquier_cifra": ("_cita_cifra('Notas 5-6-849,7', 849.7, …)", lambda M: M._cita_cifra("Notas 5-6-849,7", 849.7, "Notas 5-6-849,7\n")[0]),
}
for nombre, t in TESTIGOS.items():
    if t is None or t[1] is None:
        continue
    desc, f = t
    try:
        a, b = f(VE), f(mutado(nombre))
    except Exception as ex:  # noqa: BLE001
        a, b = "—", f"EXCEPCIÓN {type(ex).__name__}: {ex}"
    print(f"{nombre:36} {desc}\n{'':36} candidata: {a!s:28} mutada: {b!s:28} " + ("TESTIGO (la regla cambia)" if a != b else "sin diferencia con esta entrada"))
