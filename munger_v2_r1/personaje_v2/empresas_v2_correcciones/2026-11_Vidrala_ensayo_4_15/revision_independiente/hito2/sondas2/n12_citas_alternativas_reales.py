#!/usr/bin/env python3
"""n12 · H1 (segunda pasada): ¿rechazos falsos con citas REALES escritas de otra manera? Para cada entrada numérica de los 7 registros
reales (1.645; su valor_fuente y su página son coherentes: inventario «ok»), se construyen citas alternativas que un extractor podría haber
escrito sobre la MISMA página y la MISMA cifra, y se contrastan con el valor_fuente real:
  v1 la línea o líneas completas de la página que contienen la cita;   v2 la cita original más la línea siguiente de la página;
  v3 la cifra sola con sus marcas («(130.8)», «-55.320»);               v4 la cifra sola, sin marcas (recortada);
  v5 la cita original cortada justo después de la cifra;                v6 la cita original empezando justo en la cifra (con sus marcas).
Un resultado distinto de «ok» en v1, v2, v3, v5 o v6 sería un rechazo de una cita legítima; en v4 puede ser «pendiente» legítimo si la
cifra sola aparece más veces en la página con otra lectura. Y al revés (aceptaciones indebidas): cada variante se contrasta también con el
signo CONTRARIO al real: ningún «ok». Solo lee.   Uso: python3 -I -B n12_citas_alternativas_reales.py"""
import collections, os, re, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun2 import VE, PV, ETIQUETA

E14 = os.path.join(PV, "empresas_v2_correcciones", "2026-11_Vidrala_ensayo_4_14")
EXPS = ["vidrala_decisiones_INVALIDO_perdio_analisis/Vidrala", "elis_decisiones/Elis", "viscofan/Viscofan", "elis_motor_A/Elis", "vidrala_decisiones/Vidrala",
        "vidrala/Vidrala", "viscofan_decisiones/Viscofan"]
MARCAS = "-‐‑‒–—﹣－−"
cuenta = collections.Counter()
contrario = collections.Counter()
ejemplos = collections.defaultdict(list)
n = 0
for exp in EXPS:
    c = os.path.join(E14, exp)
    reg, err = VE.cargar(c)
    for e in reg["entradas"]:
        f = e.get("fuente") if isinstance(e.get("fuente"), dict) else {}
        vf, cita = f.get("valor_fuente"), f.get("cita")
        if not VE._num(vf) or e.get("clase") not in ("dato_publicado", "cero_comprobado"):
            continue
        ruta = VE._ruta_fuente(c, f.get("archivo")) if f.get("archivo") else None
        if not (ruta and str(ruta).lower().endswith(".txt")):
            continue
        est, pag = VE._pagina_examinable(ruta, f.get("pagina"))
        if est != "ok" or VE._cita_cifra(cita, vf, pag)[0] != "ok":
            continue
        n += 1
        t = re.sub(r"[\xa0  ]", " ", pag)
        apar = VE._apariciones_en_pagina(cita, pag)
        linea, a, b = apar[0]
        ini_abs = t.find(linea)  # posición de la línea en la página
        variantes = {"v1 línea completa": linea.strip()}
        fin_abs = ini_abs + len(linea)
        sig = t.find("\n", fin_abs + 1)
        variantes["v2 cita + línea siguiente"] = (linea[a:] + " " + t[fin_abs + 1: sig if sig >= 0 else len(t)]).strip()
        # la cifra dentro de la cita, en la línea
        m_c = None
        for cf in sorted(VE._cifras(vf), key=len, reverse=True):
            for m in re.finditer(r"(?<![\d.,])" + re.escape(cf) + r"(?!\d|[.,]\d)", linea):
                if m.start() < b and m.end() > a:
                    m_c = m
                    break
            if m_c:
                break
        if vf != 0 and m_c:
            i, j = m_c.start(), m_c.end()
            i2, j2 = i, j
            if i2 > 0 and linea[i2 - 1] in "€$£¥":
                i2 -= 1
            if i2 > 0 and linea[i2 - 1] in MARCAS + "(+":
                i2 -= 1
            if j2 < len(linea) and linea[j2:j2 + 1] == ")":
                j2 += 1
            variantes["v3 cifra con sus marcas"] = linea[i2:j2]
            variantes["v4 cifra sin marcas (recortada)"] = linea[i:j]
            if j2 > a and j2 < b:
                variantes["v5 cita cortada tras la cifra"] = linea[a:j2]
            if i2 > a:
                variantes["v6 cita desde la cifra"] = linea[i2:b]
        for nombre, var in variantes.items():
            if not var or VE._norm_txt(var) not in VE._norm_txt(pag):
                cuenta[(nombre, "(la variante no está en la página: no se prueba)")] += 1
                continue
            r = VE._cita_cifra(var, vf, pag)[0]
            cuenta[(nombre, r)] += 1
            if r != "ok" and len(ejemplos[(nombre, r)]) < 3:
                ejemplos[(nombre, r)].append((exp.split("/")[0], e.get("celda"), vf, var[:90]))
            if vf != 0:
                rc = VE._cita_cifra(var, -vf, pag)[0]
                contrario[(nombre, rc)] += 1
                if rc == "ok" and len(ejemplos[(nombre, "CONTRARIO ok")]) < 3:
                    ejemplos[(nombre, "CONTRARIO ok")].append((exp.split("/")[0], e.get("celda"), vf, var[:90]))
print("código:", ETIQUETA, "·", n, "entradas numéricas reales con su inventario «ok»")
print("== con el valor_fuente real (se espera «ok»)")
for k in sorted(cuenta):
    print(f"   {k[0]:34} {k[1]:55} {cuenta[k]}")
print("== con el signo CONTRARIO al real (ningún «ok»)")
for k in sorted(contrario):
    print(f"   {k[0]:34} {k[1]:55} {contrario[k]}")
print("== ejemplos de lo que no es «ok» (o del contrario aceptado)")
for k in sorted(ejemplos):
    for x in ejemplos[k]:
        print(f"   {k[0]} · {k[1]}: {x}")
