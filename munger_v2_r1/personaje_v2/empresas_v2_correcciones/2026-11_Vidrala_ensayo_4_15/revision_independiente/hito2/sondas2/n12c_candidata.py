#!/usr/bin/env python3
"""n12c · La misma medida de n12 con el código de la CANDIDATA de la primera pasada (que no tiene _apariciones_en_pagina): se toma de la
estable solo la localización de la cita en la página para construir las variantes; el contraste es el de la candidata.
Uso: python3 -I -B n12c_candidata.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dos_codigos as D
import comun2
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "n12_citas_alternativas_reales.py"), encoding="utf-8").read()
src = src.replace("from comun2 import VE, PV, ETIQUETA", "from comun2 import PV\nimport dos_codigos as _D\nVE = _D.VC\nVE._apariciones_en_pagina = _D.VE._apariciones_en_pagina\nETIQUETA = 'candidata (1.ª pasada)'")
exec(compile(src, "n12_citas_alternativas_reales.py[candidata]", "exec"))
