#!/usr/bin/env python3
"""s1b · R415-SIGNO, casos de unidad adicionales: (a) una aparición con el signo de valor_fuente y otra indeterminada → «ok»;
(b) el cero impreso como guion cuando la página trae un menos separado de su cifra (formato de contabilidad);
(c) el cero entre dos cifras a un espacio («784.366 - 784.366») frente al signo de la segunda cifra."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun import VE
for cita, vf in [("Importe 149,5 - 149,5", 149.5), ("Importe 149,5 - 149,5", -149.5), ("Importe (149,5) - 149,5", -149.5), ("Importe 149,5 149,5-", 149.5),
                 ("Cargo    -     1.234,00 €", 0), ("Cargo    -     1.234,00 €", 1234.0), ("Cargo    -     1.234,00 €", -1234.0),
                 ("Total 784.366 - 784.366", 0), ("Total 784.366 - 784.366", 784366), ("Total 784.366 - 784.366", -784366),
                 ("Total 784.366 - 100.000", 100000), ("Total 784.366 - 100.000", -100000)]:
    print(f"   _cita_cifra({cita!r}, {vf!r}) -> {VE._cita_cifra(cita, vf)}")
