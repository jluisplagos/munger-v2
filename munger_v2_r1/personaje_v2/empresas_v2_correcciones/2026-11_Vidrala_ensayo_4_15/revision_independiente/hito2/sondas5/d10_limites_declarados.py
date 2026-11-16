#!/usr/bin/env python3
"""d10 · los límites que el docstring de _signo_en_cita declara ahora (quinta comprobación): ¿hace el código lo que dice?
«quedan pendientes, por prudencia, formas legítimas como «(149.5m)», «(-x)», «31-dic-2024», «2024-25», «12-2024» o «7-7,5 %» […];
un carácter invisible entre el signo y la cifra la hace leer en positivo; […] el signo escrito con palabras («menos 149,5») no se reconoce».
Uso: python3 -I -B d10_limites_declarados.py"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from comun5 import VE, ACT  # noqa: E402
print("código:", ACT)
for nombre, pag, cita, vf, declarado in (
        ("«(149.5m)» negativo con unidad pegada", "Resultado (149.5m)\n", "Resultado (149.5m)", -149.5, "pendiente"),
        ("«(-149,5)» paréntesis y menos", "Resultado (-149,5)\n", "Resultado (-149,5)", -149.5, "pendiente"),
        ("«31-dic-2024» el año", "Cierre 31-dic-2024\n", "Cierre 31-dic-2024", 2024, "pendiente"),
        ("«2024-25» el 25", "Ejercicio 2024-25\n", "Ejercicio 2024-25", 25, "pendiente"),
        ("«12-2024» el año", "Cierre 12-2024\n", "Cierre 12-2024", 2024, "pendiente"),
        ("«7-7,5 %» el 7,5", "Crecimiento 7-7,5 %\n", "Crecimiento 7-7,5 %", 7.5, "pendiente"),
        ("carácter invisible (guion blando) entre el signo y la cifra, valor positivo", "Resultado -­149,5\n", "Resultado -­149,5", 149.5, "se lee en positivo"),
        ("«menos 149,5» con el valor positivo", "Resultado menos 149,5\n", "Resultado menos 149,5", 149.5, "se lee en positivo"),
        ("«menos 149,5» con el valor negativo", "Resultado menos 149,5\n", "Resultado menos 149,5", -149.5, "(no se reconoce: discrepancia)")):
    r = VE._cita_cifra(cita, vf, pag)
    lo_que_hace = {"ok": "ok", "signo_indeterminado": "pendiente", "no_localizada": "pendiente", "signo_distinto": "discrepancia", "ausente": "discrepancia"}[r[0]]
    conforme = (declarado == "pendiente" and lo_que_hace == "pendiente") or (declarado == "se lee en positivo" and r[0] == "ok") or (declarado.startswith("(no") and lo_que_hace == "discrepancia")
    print(f"   {nombre:78} declarado: {declarado:30} hace: {r[0]:20} {'conforme' if conforme else '<<< NO conforme con lo declarado'}")
