#!/usr/bin/env python3
"""d14 · ¿detectan de paso las pruebas nuevas alguna de las mutaciones de T2 y N4 que la cuarta comprobación dejó sin detectar y para las
que el autor NO declara prueba nueva? Solo las cinco pruebas nuevas que son llamadas puras a funciones (Q1, Q3, Q4, N10/Q4 y las 150
apariciones, sin el reloj), evaluadas contra el código mutado cargado como módulo. No sustituye a la batería: es una estimación a nivel
de unidad, y no dice nada de las pruebas que usan el registro.  Uso: python3 -I -B d14_pruebas_nuevas_y_mutaciones_antiguas.py"""
import importlib.util, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutaciones5 as M5  # noqa: E402
from comun5 import VE, F  # noqa: E402
m4 = M5.m4
ORIG = open(VE.__file__, encoding="utf-8").read()
ANTIGUAS = {"t2b_sin_limite_inicial_cifra": [(m4.LIM1, m4.LIM1.replace('(r"(?<![\\d.,])" if re.match(r"\\d", palabras[0]) else ', '("" if re.match(r"\\d", palabras[0]) else '))],
            "t2d_sin_limite_final_cifra": [(m4.LIM2, m4.LIM2.replace('(r"(?!\\d|[.,]\\d)" if re.search(r"\\d$", palabras[-1]) else ', '("" if re.search(r"\\d$", palabras[-1]) else '))],
            "t2e_sin_limite_final_letra": [(m4.LIM2, m4.LIM2.replace('r"(?![^\\W\\d_])" if re.search(r"[^\\W\\d_]$", palabras[-1]) else ""', '""'))],
            "n4_solapa": [(m4.DENTRO, '        return ventana is None or (a < ventana[1] and b > ventana[0])')]}


def cargar_texto(nombre, s):
    d = tempfile.mkdtemp(prefix="d14_", dir=os.path.join(F, "tmp"))
    p = os.path.join(d, "ve_mut.py")
    open(p, "w", encoding="utf-8").write(s)
    spec = importlib.util.spec_from_file_location("ve_" + nombre, p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    sys.path.insert(0, os.path.dirname(VE.__file__))
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


VF_K = 849697.0


def pruebas(M):
    q1 = {"euros/EUR": True, "EUR/€": True, "Euros / Euro": True, "USD/$": True, "USD por EUR": False, "EUR/USD": False}
    q3 = {("Saldo 2023-1849", 1849): "signo_indeterminado", ("Graf2023-1849", 1849): "signo_indeterminado", ("9-10", 10): "signo_indeterminado",
          ("2019-2020", 2020): "ok", ("FY2023-2024", 2024): "ok", ("31-12-2024", 2024): "ok"}
    muchas = " ".join([f"Total: {VF_K:.3f}"] * 3000)
    pocas = " ".join([f"Partida {i}: {i}.5" for i in range(8000)] + [f"Total: {VF_K:.3f}"] * 150)
    return {"(Q1)": not [u for u, e in q1.items() if M._unidad_monetaria_no_reconocida(u) != e],
            "(Q3)": not [k for k, e in q3.items() if M._cita_cifra(*k)[0] != e],
            "(Q4)": M._cita_cifra("849,7", 849.7, "ejercicio.849,7")[0] == "no_localizada" and M._cita_cifra("849,7", 849.7, "total 1.849,7")[0] == "ausente",
            "(N10, Q4)": M._cita_cifra(f"Total: {VF_K:.3f}", VF_K, muchas)[0] == "signo_indeterminado",
            "(N10) 150": M._cita_cifra(f"Total: {VF_K:.3f}", VF_K, pocas)[0] == "ok"}


base = pruebas(VE)
print("876bfc2:", base)
assert all(base.values())
for nombre, cambios in ANTIGUAS.items():
    s = ORIG
    for viejo, nuevo in cambios:
        assert s.count(viejo) == 1, nombre
        s = s.replace(viejo, nuevo)
    r = pruebas(cargar_texto(nombre, s))
    fallan = [k for k, v in r.items() if not v]
    print(f"   {nombre:32} pruebas nuevas (puras) que fallarían: {fallan or 'ninguna'}")
