#!/usr/bin/env python3
"""s11 · R415-SIGNO en el registro sintético completo (arnés fx5 = fixture de la batería): la página conservada y la cita, con formatos
que el revisor considera realistas. Para cada caso: lo que publica la página, valor_fuente y signo declarados, y el resultado.
«esperado» = juicio del revisor (apta / no apta)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fx5 as X
VE, K = X.VE, X.K
VF = X.ent(X.REG, K)["fuente"]["valor_fuente"]
TRAT = "pago publicado en negativo; el modelo usa su magnitud positiva (signo −1)"
print("control positivo:", X.resumen(X.con(), K))
n_mal = 0


def caso(nombre, pagina, cita=None, vf=VF, signo=1, trat=None, esperado="no apta", k=K, clase=None):
    global n_mal
    pg = X.nueva_pagina(pagina)

    def cambio(g):
        f = X.ent(g, k)["fuente"]
        f.update(pagina=pg, cita=cita if cita is not None else pagina, valor_fuente=vf, signo=signo)
        if trat:
            f["tratamiento"] = trat
    r = X.con(cambio, resellar=True)
    res = "apta" if (r["apto_por_entradas"] and k in r["comprobadas"]) else "no apta"
    marca = "" if res == esperado else ("   <<< ACEPTADA con un signo que la página no publica así" if res == "apta" else "   <<< rechazo falso")
    n_mal += bool(marca)
    det = "; ".join(x[:150] for x in X.con_k(r, k))
    print(f"   {nombre}\n      página={pagina!r}\n      cita={cita if cita is not None else '(la página)'!r} valor_fuente={vf!r} signo={signo}\n      -> {res}{marca}" + (f"\n         {det}" if det else ""))


print("\n== A · formatos con el menos separado de la cifra")
caso("A1 formato de contabilidad de Excel (es-ES): menos a la izquierda de la celda, cifra a la derecha; valor_fuente POSITIVO", f"Partida sintética de {K}:   -          {VF:,.3f} €")
caso("A2 lo mismo con valor_fuente NEGATIVO y signo −1 (lo que publica la página)", f"Partida sintética de {K}:   -          {VF:,.3f} €", vf=-VF, signo=-1, trat=TRAT, esperado="apta")
caso("A3 «-£   849,697.000» (contabilidad en-GB); valor_fuente POSITIVO", f"Partida sintética de {K}: -£   {VF:,.3f}")
caso("A4 menos Unicode a dos espacios «−  849 697,000»; valor_fuente POSITIVO", f"Partida sintética de {K}: −  " + f"{VF:,.3f}".replace(",", " ").replace(".", ","))
caso("A5 menos Unicode a UN espacio en una tabla estrecha, donde «−» es el cero de la columna anterior (como en Elis 2017, p. 228); valor_fuente NEGATIVO y signo −1",
     f"Partida sintética de {K} − {VF:.3f}", vf=-VF, signo=-1, trat=TRAT)
caso("A6 lo mismo con valor_fuente POSITIVO (la cifra de la segunda columna es positiva)", f"Partida sintética de {K} − {VF:.3f}", esperado="apta")
print("\n== B · paréntesis y moneda")
caso("B1 «(EUR 849,697.000)»: negativo contable con el código de moneda dentro; valor_fuente POSITIVO", f"Partida sintética de {K}: (EUR {VF:,.3f})")
caso("B2 «(849,697.000 m)» negativo con unidad dentro; valor_fuente NEGATIVO, signo −1", f"Partida sintética de {K}: ({VF:,.3f} m)", vf=-VF, signo=-1, trat=TRAT, esperado="apta")
caso("B3 «$-849,697.000»; valor_fuente NEGATIVO, signo −1", f"Partida sintética de {K}: $-{VF:,.3f}", vf=-VF, signo=-1, trat=TRAT, esperado="apta")
caso("B4 «(-849697.000)»; valor_fuente NEGATIVO, signo −1", f"Partida sintética de {K}: (-{VF:.3f})", vf=-VF, signo=-1, trat=TRAT, esperado="apta")
caso("B5 signo −1 con tratamiento «ninguno» (la transformación no se explica)", f"Partida sintética de {K}: ({VF:,.3f})", vf=-VF, signo=-1, trat="ninguno")
print("\n== C · dos apariciones de la cita en la página (el control lee la primera)")
caso("C1 primera aparición con el guion en otra columna y segunda con el guion a un espacio", f"Total       -      {VF:.3f}\nResumen\nTotal - {VF:.3f}", cita=f"Total - {VF:.3f}")
caso("C2 al revés", f"Total - {VF:.3f}\nResumen\nTotal       -      {VF:.3f}", cita=f"Total - {VF:.3f}")
print("\n== D · el pasaje no se encuentra con re.I pero la cita normalizada sí está en la página (se lee el signo en la CITA)")
caso("D1 página con «İ» (U+0130) y guion a UN espacio; la cita escribe «i̇» y DOS espacios", f"İmporte - {VF:.3f}", cita=f"i̇mporte -  {VF:.3f}")
caso("D2 control: la misma página con la cita literal", f"İmporte - {VF:.3f}")
print("\n== E · cero impreso como «−» (U+2212), como en Elis 2017 p. 228")
KZ = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "cero_comprobado")
caso(f"E1 cero comprobado ({KZ}) cuya página imprime «−» en su columna", "Net gains on site disposals        −                 42.2", vf=0, k=KZ, esperado="apta")
caso(f"E2 lo mismo con guion ASCII (control)", "Net gains on site disposals        -                 42.2", vf=0, k=KZ, esperado="apta")
print("\n== F · auxiliar (dato de origen de un derivado): ¿se contrasta también con su signo?")
import copy
k_der = next(e["celda"] for e in X.REG["entradas"] if e["clase"] == "dato_publicado" and e["ambito"] == "calculo" and e["celda"].startswith("Historia!") and e["celda"] != K and isinstance(e["valor_modelo"], float) and not e["celda"].endswith("5"))
vd = X.ent(X.REG, k_der)["valor_modelo"]
for nombre, pag_aux, vf_aux, esp in (("F1 auxiliar con página «-…» y valor_fuente positivo", "Partida sintética de aux:a1: -{v}", 1, "no apta"), ("F2 auxiliar con página y valor_fuente positivos (control)", "Partida sintética de aux:a1: {v}", 1, "apta")):
    v_aux = round(vd * 1000)
    pg = X.nueva_pagina(pag_aux.format(v=v_aux))

    def cambio(g, pg=pg, pag_aux=pag_aux, vf_aux=vf_aux):
        base_f = dict(X.ent(g, K)["fuente"])
        g["entradas"].append({"celda": "aux:a1", "id": "aux:a1", "ambito": "auxiliar", "uso": f"origen de {k_der}", "material": True, "clase": "dato_publicado", "valor_modelo": v_aux * 0.001 if False else round(v_aux / 1000, 6),
                              "fuente": dict(base_f, pagina=pg, valor_fuente=v_aux, cita=pag_aux.format(v=v_aux), periodo=X.ent(g, k_der)["fuente"]["periodo"], columna=X.ent(g, k_der)["fuente"]["columna"]),
                              "comprobacion": dict(X.COMPROBADA), "incidencia": None})
        X.ent(g, k_der).update(clase="derivado", fuente={}, derivacion={"origenes": ["aux:a1"], "formula": 'o["aux:a1"] * 1', "conciliacion": "(prueba) el auxiliar", "unidad": "mm"})
    r = X.con(cambio, resellar=True)
    res = "apta" if r["apto_por_entradas"] else "no apta"
    marca = "" if res == esp else "   <<< distinto de lo esperado"
    n_mal += bool(marca)
    print(f"   {nombre}: {res}{marca}  {'; '.join(x[:170] for x in X.con_k(r, 'aux:a1') + X.con_k(r, k_der))}")
print(f"\n{n_mal} casos distintos de lo esperado por el revisor")
print("control positivo al final:", X.resumen(X.con(), K))
X.limpiar()
