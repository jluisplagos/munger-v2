#!/usr/bin/env python3
"""jumbo_g · declaración de las entradas dependientes de la celda de juicio C76 en el registro de entradas (verificacion_entradas.json), para
que el pipeline recalcule Análisis!C46 y C40 en el paso 9, tras escribir la fase B (producto/entradas-dependientes, integrada en
examen/expedientes-f1 en e031edb; revisión independiente CONFORME: munger-v2-evidencias-mistral,
coordinacion/cierre_v2/examen/revisiones/entradas_dependientes/REVISION.md). Corrección de la orquestación («Claude orquestación»).
Solo añade «derivacion.recalculo» a esas dos entradas (C46 con «conciliacion_f1»: su partida F1-K3a de motor_a_f1.json sigue al valor) y una
frase a «nota_del_extractor_complementario». No cambia valores, fórmulas, orígenes, fuentes ni comprobaciones; la entrada de C76 (hipótesis,
160) no se toca: se pone al día tras las fases y la sella un revisor. Las dos entradas ya estaban pendientes, sin vínculo: la declaración
entra en su huella y las revisa otro agente.
Uso: python3 -I declarar_dependientes.py CARPETA_EMPRESA REGISTRO_CAMBIOS.json"""
import copy, hashlib, json, os, sys

C, REG = sys.argv[1:3]
p = os.path.join(C, "verificacion_entradas.json")
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
HOY = "2026-11-19"
REGLA = ("P-O1 (c) y J1 (DECISIONES_PARA_EL_USUARIO.md, 18-nov-2026): con la regla espejo solo se excluyen los intereses cobrados de la caja que se "
         "suma aparte en C76 (s = C76 ÷ caja media); C76 lo escribe la fase B")
DECLARACION = {"Análisis!C46": {"celdas_de_juicio": ["Análisis!C76"], "regla": REGLA, "conciliacion_f1": True},
               "Análisis!C40": {"celdas_de_juicio": ["Análisis!C76"], "regla": REGLA}}
antes_sha = h(p)
d = json.load(open(p, encoding="utf-8"))
E = {e["celda"]: e for e in d["entradas"] if isinstance(e, dict)}
cambios = []
for k, rc in DECLARACION.items():
    e = E[k]
    if e.get("clase") != "derivado" or "Análisis!C76" not in (e.get("derivacion") or {}).get("origenes", []):
        raise SystemExit(f"{k} no es una derivada con Análisis!C76 entre sus orígenes: no se declara")
    antes = copy.deepcopy(e["derivacion"].get("recalculo"))
    e["derivacion"]["recalculo"] = copy.deepcopy(rc)
    cambios.append({"celda": k, "clave": "derivacion.recalculo", "antes": antes, "despues": copy.deepcopy(rc)})
d["nota_del_extractor_complementario"] = (str(d.get("nota_del_extractor_complementario") or "") + f" (jumbo_g, {HOY}) Claude orquestación declaró en "
                                          "Análisis!C46 (con conciliacion_f1) y Análisis!C40 «derivacion.recalculo» (celda de juicio Análisis!C76; P-O1 (c) y J1) "
                                          "para que el pipeline los recalcule en el paso 9, tras escribir la fase B (resultados/registro_declaracion_dependientes_jumbo_g.json); "
                                          "no cambia valores, fórmulas, orígenes ni comprobaciones, ni la entrada de C76.")
open(p, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
json.dump({"fecha": HOY, "extractor": "Claude orquestación", "guion": "resultados/scripts/declarar_dependientes.py",
           "registro": "Jumbo/verificacion_entradas.json", "registro_antes_sha256": antes_sha, "registro_despues_sha256": h(p),
           "motivo": ("la fase B de jumbo_g escribió C76 = 150 (fase_b.json, aaa2802) y C46/C40 se prepararon con C76 = 160: con la declaración, el paso 9 "
                      "los recalcula con su fórmula registrada y la C76 de la fase B (entradas_dependientes.py), sin repetir la fase B"),
           "entradas": list(DECLARACION), "cambios": cambios,
           "no_cambia": "valores, fórmulas, orígenes, fuentes, comprobaciones ni vínculos; la entrada de Análisis!C76 (hipótesis, 160) sigue como estaba"},
          open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"declaradas {len(cambios)} entradas · registro {antes_sha[:16]}… → {h(p)[:16]}…")
