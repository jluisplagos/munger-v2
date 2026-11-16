#!/usr/bin/env python3
"""d13 · los casos de prueba que se proponen en V4, evaluados contra el código de 876bfc2 y contra cada mutación que hoy no se detecta
(el texto mutado se carga como módulo, sin ejecutar la batería): ¿separaría cada caso su mutación? No sustituye a la batería: dice solo
si la aserción propuesta daría un resultado distinto con la regla quitada.  Uso: python3 -I -B d13_casos_de_prueba_propuestos.py"""
import importlib.util, os, sys, tempfile
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mutaciones5 as M5  # noqa: E402
from comun5 import VE, F  # noqa: E402
ORIG = open(VE.__file__, encoding="utf-8").read()


def mutado(nombre):
    s = ORIG
    for arch, viejo, nuevo in M5.M[nombre][3]:
        assert arch == M5.VEP and s.count(viejo) == 1
        s = s.replace(viejo, nuevo)
    d = tempfile.mkdtemp(prefix="d13_", dir=os.path.join(F, "tmp"))
    p = os.path.join(d, "verificacion_entradas_mut.py")
    open(p, "w", encoding="utf-8").write(s)
    spec = importlib.util.spec_from_file_location("ve_" + nombre, p)
    m = importlib.util.module_from_spec(spec)
    ruta = list(sys.path)
    sys.path.insert(0, os.path.dirname(VE.__file__))
    spec.loader.exec_module(m)
    sys.path[:] = ruta
    return m


CASOS = [("q3b_prefijo_sin_anclar", "_cita_cifra('Graf2023-2024', 2024)[0]", lambda M: M._cita_cifra("Graf2023-2024", 2024)[0], "signo_indeterminado"),
         ("q3c_sin_rango_1900_2100", "_cita_cifra('Saldo 2023-2849', 2849)[0]", lambda M: M._cita_cifra("Saldo 2023-2849", 2849)[0], "signo_indeterminado"),
         ("q3d_sin_creciente", "_cita_cifra('Variación 2024-2023', 2023)[0]", lambda M: M._cita_cifra("Variación 2024-2023", 2023)[0], "signo_indeterminado"),
         ("q1c_moneda_sin_gbp_jpy", "_unidad_monetaria_no_reconocida('libras/GBP')", lambda M: M._unidad_monetaria_no_reconocida("libras/GBP"), True),
         ("q1c_moneda_sin_gbp_jpy", "_unidad_monetaria_no_reconocida('JPY/¥')", lambda M: M._unidad_monetaria_no_reconocida("JPY/¥"), True),
         ("t8d_fecha_cualquier_cifra", "_cita_cifra('Notas 5-6-849,7', 849.7)[0]", lambda M: M._cita_cifra("Notas 5-6-849,7", 849.7)[0], "signo_indeterminado")]
for nombre, expr, f, esperado in CASOS:
    a, b = f(VE), f(mutado(nombre))
    print(f"   {nombre:28} {expr:52} 876bfc2: {a!r:22} (se espera {esperado!r}: {'bien' if a == esperado else 'MAL'}) · con la mutación: {b!r:22} → {'la separaría' if a == esperado and b != esperado else 'NO la separa'}")
