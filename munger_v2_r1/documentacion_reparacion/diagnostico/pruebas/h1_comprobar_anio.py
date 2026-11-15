#!/usr/bin/env python3
"""H1 · Prueba de fase1_historia.comprobar_anio con casos sintéticos mínimos.

Uso: python3 -I -B h1_comprobar_anio.py RUTA_SCRIPTS DIR_TRABAJO SALIDA_JSON
- RUTA_SCRIPTS: personaje_v2/scripts de la COPIA (no se modifica; solo se importa).
- DIR_TRABAJO: carpeta del diagnóstico donde se crean las carpetas de empresa sintéticas.
Cada caso crea DIR_TRABAJO/<caso>/texto/AR.txt (una página) y fase1_partes/AR_2025.json,
llama a comprobar_anio y registra la lista de errores (vacía = ACEPTADO).
"""
import json
import os
import shutil
import sys

scripts, trabajo, salida = sys.argv[1], sys.argv[2], sys.argv[3]
sys.path.insert(0, scripts)
import fase1_historia as F  # noqa: E402


def partidas_vacias():
    return {k: {} for k in F.PARTIDAS}


def caso(nombre, pagina, partidas_extra, unidad="millones", esperado_revisor=None, que_prueba=""):
    c = os.path.join(trabajo, "h1", nombre)
    shutil.rmtree(c, ignore_errors=True)
    os.makedirs(os.path.join(c, "texto"))
    os.makedirs(os.path.join(c, "fase1_partes"))
    open(os.path.join(c, "texto", "AR.txt"), "w", encoding="utf-8").write("[PDF PAGE 1]\n" + pagina + "\n")
    p = partidas_vacias()
    p.update(partidas_extra)
    d = {"anio": 2025, "archivo": "AR.txt", "unidad": unidad, "partidas": p}
    json.dump(d, open(os.path.join(c, "fase1_partes", "AR_2025.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    errs = F.comprobar_anio(c, 2025)
    return {"caso": nombre, "que_prueba": que_prueba, "pagina": pagina, "unidad_declarada": unidad,
            "partidas_declaradas": partidas_extra, "errores": errs,
            "resultado": "ACEPTADO" if not errs else "RECHAZADO", "carpeta": c}


comp = lambda imp, lin, signo=None: ({"concepto": lin.rsplit(" ", 1)[0], "impreso": imp, "pagina": 1, "linea": lin} | ({"signo": signo} if signo is not None else {}))

R = []
# 1. Caso del revisor
R.append(caso("1_revisor_capex_linea_inexistente", "Revenue 123",
              {"capex": {"actual": [comp("123", "Capital expenditure 123")]}},
              que_prueba="Página 'Revenue 123'; capex 123 con línea 'Capital expenditure 123' que no existe en la página."))
# 2. Línea existente pero de otra partida (concepto no comprobado)
R.append(caso("2_concepto_ajeno_linea_real", "Revenue 123",
              {"capex": {"actual": [comp("123", "Revenue 123")]}},
              que_prueba="capex declarado con la línea real 'Revenue 123': ¿se compara el concepto con la partida?"))
# 3. Número contenido dentro de otro número (subcadena)
R.append(caso("3_subcadena_numerica", "Revenue 91234",
              {"capex": {"actual": [comp("123", "Capital expenditure 123")]}},
              que_prueba="Página 'Revenue 91234'; capex 123: '123' solo aparece como parte de 91234."))
# 4. Columna equivocada: el 123 es el comparativo (año anterior), declarado como actual
R.append(caso("4_columna_anterior_como_actual", "2025 2024\nCapital expenditure 150 123",
              {"capex": {"actual": [comp("123", "Capital expenditure 150 123")]}},
              que_prueba="Línea real con dos columnas (2025=150, 2024=123); se declara 123 como 'actual'."))
# 5. Unidad: la página dice miles y se declara 'millones' (factor 1000)
R.append(caso("5_unidad_no_contrastada", "Amounts in thousands of EUR\nCapital expenditure 123",
              {"capex": {"actual": [comp("123", "Capital expenditure 123")]}}, unidad="millones",
              que_prueba="Página en miles; el JSON declara 'millones'."))
# 6. Signo: un cobro impreso en positivo convertido en pago con signo -1
R.append(caso("6_signo_no_contrastado", "Proceeds from sale of businesses 40",
              {"adquisiciones": {"actual": [comp("40", "Proceeds from sale of businesses 40", signo=-1)]}},
              que_prueba="Cobro de 40 declarado con signo -1 (lo convierte en pago)."))
# 7. Cero con motivo cualquiera y página que no habla de la partida
R.append(caso("7_cero_sin_respaldo", "Revenue 123",
              {"capex": {"cero": {"motivo": "no hay capex", "pagina": 1}}},
              que_prueba="capex = cero con motivo libre y página 1, que solo contiene 'Revenue 123'."))
# 8. Control negativo: número que no está en ninguna parte
R.append(caso("8_control_numero_ausente", "Revenue 123",
              {"capex": {"actual": [comp("999", "Capital expenditure 999")]}},
              que_prueba="Control: 999 no aparece en la página."))
# 9. Control negativo: página inexistente
c9 = comp("123", "Capital expenditure 123"); c9["pagina"] = 7
R.append(caso("9_control_pagina_inexistente", "Capital expenditure 123", {"capex": {"actual": [c9]}},
              que_prueba="Control: página 7 inexistente."))
# 10. Control positivo: extracción correcta
R.append(caso("10_control_correcto", "Capital expenditure 123", {"capex": {"actual": [comp("123", "Capital expenditure 123")]}},
              que_prueba="Control: línea y número presentes."))
# 11. Cero con página inexistente (sí se rechaza)
R.append(caso("11_control_cero_pagina_inexistente", "Revenue 123", {"capex": {"cero": {"motivo": "x", "pagina": 9}}},
              que_prueba="Control: cero con página 9 inexistente."))

json.dump(R, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for r in R:
    print(f"{r['caso']:40s} {r['resultado']:10s} {'; '.join(r['errores'])}")
