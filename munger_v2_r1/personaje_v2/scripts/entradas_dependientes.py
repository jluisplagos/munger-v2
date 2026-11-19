#!/usr/bin/env python3
"""Entradas declaradas que dependen de una celda de juicio: recálculo determinista y registrado tras la fase B (4.15; examen, Jumbo, J1).

Problema (examen, jumbo_e y jumbo_g). Por la decisión J1 de la persona responsable, la caja base de Jumbo (Análisis!C46, CFO medio
2023–2025) y su FCF (Análisis!C40) suman los intereses cobrados que no son de la caja sobrante de Análisis!C76: s = C76 ÷ caja media;
intereses que entran = intereses − s × (intereses − cupones). C76 es una celda de JUICIO que escribe la fase B. La preparación calculaba
C46 y C40 con el C76 vigente entonces; cuando la fase B elegía otro (jumbo_e 200 → 160, jumbo_g 160 → 150), el libro quedaba con un valor
que su derivación registrada ya no reproducía (discrepancia en verificacion_entradas.py: el expediente no podía ser apto por entradas) y
repetir el expediente no convergía.

Declaración (nunca se adivina). La dependencia se declara en el REGISTRO de entradas (verificacion_entradas.json), en la propia entrada
derivada, junto a la fórmula y los orígenes que ya publica (cada origen con su entrada, su fuente y su comprobación):
  "derivacion": {"origenes": [..., "Análisis!C76"], "formula": "…o[\"Análisis!C76\"]…", "conciliacion": "…", "unidad": "millones de euros",
                 "recalculo": {"celdas_de_juicio": ["Análisis!C76"],
                               "regla": "decisión que lo fundamenta (p. ej. J1 de DECISIONES_PARA_EL_USUARIO.md, 18-nov-2026)",
                               "conciliacion_f1": true}}
  - celdas_de_juicio: las celdas de juicio de la fórmula (Anexo A, celdas_v2.py) que escriben la fase A o la fase B; tienen que estar entre
    sus orígenes y ninguna otra celda de juicio puede ser origen sin declararse (una de la fase C se escribe después: no se admite);
  - regla: por qué la entrada sigue a esas celdas (la decisión registrada); no cambia la fórmula ni la regla J1;
  - conciliacion_f1 (solo C46–C50): la partida de «conciliacion_fcf_base» de motor_a_f1.json con ese componente explica la diferencia
    de la entrada con la Historia (F1-K3a); con true, esa partida (una sola) sigue al valor: su importe cambia exactamente lo que cambia la
    entrada. Si el expediente tiene una partida para el componente, hay que declararlo (true o false); con false, K3a juzga la partida tal
    como está.
La entrada es una celda numérica de datos de Análisis (rellenar_fase1_v63.DATOS_ANALISIS_PERMITIDOS sin las de texto) de clase «derivado»;
la fórmula cumple las reglas de verificacion_entradas (sin cifras escritas, todos sus orígenes y solo ellos, cada uno influye); los demás orígenes son
auxiliares del registro con un número o celdas de datos del libro (nunca una fórmula del libro, que no está recalculada todavía, ni otra
entrada dependiente: no se admiten cadenas, y una derivada del registro que use una entrada dependiente tiene que declararse también).

Recálculo (paso 9 del pipeline). Después de escribir la fase B y de comprobar sus celdas, ANTES del recálculo del libro y de la fase C, el
pipeline lanza `entradas_dependientes.py aplicar`, sin ningún agente de juicio. Evalúa cada fórmula declarada con aritmética exacta (las
mismas funciones que verificacion_entradas: fracciones, round de la hoja) con los orígenes publicados del registro, las celdas de datos
del libro y la celda de juicio que acaba de escribir la fase B, y guarda el resultado con la precisión de la regla U2: un importe
(«derivacion.unidad» monetaria) es el exacto o su redondeo a 3 decimales (ROUND de la hoja, mitad lejos de cero); otra magnitud, el
exacto. Comprueba antes que todas las copias del valor coinciden (libro de datos, libro evaluado, fase1_v63.json, fase1_metadatos.json y
valor_modelo del registro: cada una tiene el valor actual del libro evaluado o ya el nuevo) y escribe el valor nuevo, el mismo número, en
todas ellas: los dos libros (Análisis y una nota en la columna N de su fila del Control maestro; mismos cambios en los dos, así que
comprobar_celdas_v2 los sigue exigiendo iguales), fase1_v63.json y fase1_metadatos.json (la vía generativa reproduce el libro:
verificacion_entradas.entradas_no_reproducibles), el registro («valor_modelo»: su fórmula con la celda de juicio del libro da el valor del
libro) y, con conciliacion_f1, la partida de motor_a_f1.json. Cada copia que cambia lleva su rastro «recalculo_dependiente» (valor
declarado, valor, exacto, celdas de juicio y su valor, precisión, huella de la fórmula); si el valor no cambia, las copias no se tocan (no
se invalida un vínculo sellado) y queda solo el rastro auditado. El rastro completo, con el antes y el después de cada aplicación y
las huellas de los archivos, queda en recalculo_dependientes.json (material auditado: cierre_v2.MATERIAL_FIJO) y en
../resultados/recalculo_dependientes_<E>.json y .md. Los libros se escriben en temporales, se verifican con el verificador de la
plantilla y solo entonces se sustituyen (primero el de datos). Cualquier defecto detiene el recálculo sin escribir nada (código 1).
Determinista: el resultado depende solo de la fórmula, sus orígenes y la celda de juicio; repetirlo con los mismos valores no cambia
ningún archivo.

Qué NO hace. No toca las fases (fase_a/b/c.json ni lo que vieron: datos_v63.md y referencias_mecanicas.json se quedan como estaban), no
pide ningún agente, no cambia comprobaciones, vínculos ni fuentes del registro (una comprobación sellada con el valor anterior queda
desactualizada: su huella incluye el valor y los orígenes; el revisor independiente la vuelve a sellar) y no debilita ningún guardián.
Un expediente que no declara dependencias no cambia en nada (el pipeline ni siquiera lanza este programa).

Uso: entradas_dependientes.py validar CARPETA
     entradas_dependientes.py previsualizar CARPETA [--fase-b fase_b.json]   (no escribe: con la celda de juicio del libro o de fase_b.json)
     entradas_dependientes.py aplicar CARPETA [--fase B] [--config CFG]      (lo lanza el pipeline en el paso 9)
Códigos: 0 correcto (también sin declaraciones) · 1 declaración no válida, copias distintas o recálculo imposible (no se escribe nada) ·
2 uso.
"""
import argparse
import datetime as dt
import fractions
import hashlib
import json
import os
import re
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import celdas_v2 as C  # noqa: E402
import verificacion_entradas as VE  # noqa: E402
from v63_xml import NS, CeldaNoPermitida, FormulaProtegida, LibroV63  # noqa: E402

RASTRO = "recalculo_dependientes.json"  # en el expediente; forma parte del material auditado (cierre_v2.MATERIAL_FIJO)
FORMATO = "1"
DECLARACION_F1 = "motor_a_f1.json"  # motor_a_f1.DECLARACION
COMPONENTES_K3A = ("C46", "C47", "C48", "C49", "C50")  # componentes de Análisis de F1-K3a (motor_a_f1.py)
# celdas de datos de Análisis que declara la fase 1 (rellenar_fase1_v63.DATOS_ANALISIS_PERMITIDOS) salvo las de texto (B4, C28, C31, C34)
CELDAS_ADMITIDAS = ("C24", "C26", "C32", "C33", "C38", "C40", "C42", "C46", "C47", "C48", "C49", "C50", "C53", "C54", "C57", "C60", "C88", "C96")
MARCA_NOTA = " · [Recálculo dependiente tras la fase B]"
MARCA_PARTIDA = " [recálculo dependiente tras la fase B:"


class ErrorRecalculo(Exception):
    pass


# ---------------------------------------------------------------------------------------------------------------- utilidades
def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and x == x and abs(x) != float("inf")


def _frac(x):
    return fractions.Fraction(x) if isinstance(x, int) else fractions.Fraction(repr(float(x)))


def _sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest() if os.path.isfile(p) else None


def _sha_texto(t):
    return hashlib.sha256(str(t).encode("utf-8")).hexdigest()


def _es(x):
    """Número en texto con coma decimal (las notas del expediente están en español)."""
    if isinstance(x, fractions.Fraction):
        x = float(x)
    if isinstance(x, float) and x.is_integer():
        x = int(x)
    return str(x).replace(".", ",")


def _es_exacto(fr, dec=9):
    t = f"{float(fr):.{dec}f}".rstrip("0").rstrip(".")
    return t.replace(".", ",")


def _iguales(a, b):
    return _num(a) and _num(b) and _frac(a) == _frac(b)


def _json(p):
    try:
        return json.load(open(p, encoding="utf-8"))
    except (OSError, ValueError):
        return None


def _volcar_json(p, d):
    """Mismo formato que el resto del expediente (indent=1, sin escapar, sin salto final); temporal y sustitución."""
    tmp = p + ".dep.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(json.dumps(d, ensure_ascii=False, indent=1))
    os.replace(tmp, p)


def libros(carpeta):
    e = os.path.basename(os.path.abspath(carpeta))
    return os.path.join(carpeta, f"{e}_v63_datos.xlsx"), os.path.join(carpeta, f"{e}_v63_evaluada.xlsx")


def fase_de(clave):
    """Fase («A», «B», «C») de una celda de juicio del Anexo A (celdas_v2.py), o None si no es de juicio."""
    if not isinstance(clave, str) or "!" not in clave:
        return None
    hoja, ref = clave.split("!", 1)
    meta = (C.CELDAS.get(hoja) or {}).get(ref)
    return meta["fase"] if meta else None


def _texto_celda(lb, hoja, ref):
    """Texto de una celda; un texto compartido (t="s") se resuelve en sharedStrings.xml (LibroV63.leer devuelve su índice)."""
    c = lb._celda(hoja, ref)
    if c is None:
        return None
    if c.get("t") == "s":
        from lxml import etree
        v = c.find(f"{{{NS}}}v")
        sst = lb._datos.get("xl/sharedStrings.xml")
        if v is None or v.text is None or sst is None:
            return None
        si = etree.fromstring(sst).findall(f"{{{NS}}}si")
        i = int(v.text)
        return "".join(si[i].itertext()) if 0 <= i < len(si) else None
    return lb.leer(hoja, ref)


def _fila_cm(lb, clave):
    for r in range(17, 176):
        if lb.leer("Control maestro", f"B{r}") == clave:
            return r
    return None


# ---------------------------------------------------------------------------------------------------------------- declaraciones
def declaradas(reg):
    """{celda: entrada} de las entradas del registro que declaran «derivacion.recalculo» (también si la declaración está mal formada:
    se valida después). Con una celda repetida, la primera (validar lo señala)."""
    out = {}
    for e in (reg or {}).get("entradas") or []:
        if isinstance(e, dict) and isinstance(e.get("derivacion"), dict) and "recalculo" in e["derivacion"]:
            out.setdefault(str(e.get("celda")), e)
    return out


def _por_celda(reg):
    por = {}
    for e in (reg or {}).get("entradas") or []:
        if isinstance(e, dict):
            por.setdefault(str(e.get("celda")), e)
    return por


def hay_declaraciones(carpeta):
    """True si el registro legible del expediente declara alguna entrada dependiente. Sin registro, o ilegible: False (la verificación
    de las entradas ya lo trata como «no verificado»; aquí no hay nada declarado que recalcular)."""
    reg, _ = VE.cargar(carpeta)
    return bool(declaradas(reg))


def _f1_decl(carpeta):
    p = os.path.join(carpeta, DECLARACION_F1)
    return _json(p) if os.path.isfile(p) else None


def _partidas_k3a(decl_f1, ref):
    lst = (decl_f1 or {}).get("conciliacion_fcf_base")
    return [i for i, e in enumerate(lst if isinstance(lst, list) else []) if isinstance(e, dict) and e.get("componente") == ref]


def validar(carpeta, reg=None, libro=None):
    """Problemas de las declaraciones (lista de textos; [] si no hay ninguna o si todas valen). Comprobaciones estáticas: no evalúa."""
    if reg is None:
        reg, err = VE.cargar(carpeta)
        if reg is None:
            return [err] if err else []
    decl = declaradas(reg)
    if not decl:
        return []
    mal = []
    vistas = [str(e.get("celda")) for e in reg.get("entradas") or [] if isinstance(e, dict)]
    rep = sorted({k for k in decl if vistas.count(k) > 1})
    if rep:
        mal.append(f"entradas dependientes repetidas en el registro: {rep}")
    por = _por_celda(reg)
    if libro is None:
        datos, ev = libros(carpeta)
        libro = ev if os.path.isfile(ev) else datos
    lb = LibroV63(libro) if libro and os.path.isfile(libro) else None
    if lb is None:
        mal.append("no hay libro del expediente: no se pueden comprobar los orígenes de las entradas dependientes")
    f1j, metaj = _json(os.path.join(carpeta, "fase1_v63.json")), _json(os.path.join(carpeta, "fase1_metadatos.json"))
    decl_f1 = _f1_decl(carpeta)
    for k, e in decl.items():
        d = e.get("derivacion") or {}
        rc = d.get("recalculo")
        hoja, _, ref = k.partition("!")
        if hoja != "Análisis" or ref not in CELDAS_ADMITIDAS:
            mal.append(f"{k}: solo se recalculan celdas de datos de Análisis que declara la fase 1 ({', '.join(CELDAS_ADMITIDAS)})")
            continue
        if e.get("clase") != "derivado":
            mal.append(f"{k}: la entrada es de clase {e.get('clase')!r}; solo una entrada «derivado» tiene fórmula que recalcular")
            continue
        if lb is not None and lb.tiene_formula("Análisis", ref):
            mal.append(f"{k}: es una fórmula del libro, no una entrada de datos")
            continue
        if not isinstance(rc, dict):
            mal.append(f"{k}: «derivacion.recalculo» tiene que ser un objeto {{celdas_de_juicio, regla[, conciliacion_f1]}}")
            continue
        extra = sorted(set(rc) - {"celdas_de_juicio", "regla", "conciliacion_f1"})
        if extra:
            mal.append(f"{k}: claves de «recalculo» no admitidas {extra}")
        org, formula = d.get("origenes"), d.get("formula")
        if not isinstance(org, list) or not org or not all(isinstance(o, str) and o for o in org) or len(set(org)) != len(org) or not isinstance(formula, str):
            mal.append(f"{k}: «origenes» tiene que ser una lista de orígenes distintos y «formula» un texto")
            continue
        try:
            ctes = VE._constantes_no_admitidas(formula)
            usadas = VE._claves_formula(formula)
        except (SyntaxError, ValueError) as ex:
            mal.append(f"{k}: fórmula no evaluable ({type(ex).__name__}: {str(ex)[:80]})")
            continue
        if ctes:
            mal.append(f"{k}: la fórmula escribe cifras {ctes!r} (solo enteros de 1 a 12, potencias de diez y los decimales de round)")
        if usadas != set(org):
            mal.append(f"{k}: la fórmula usa {sorted(map(str, usadas))} y los orígenes son {sorted(org)}")
        cj = rc.get("celdas_de_juicio")
        if not isinstance(cj, list) or not cj or not all(isinstance(x, str) for x in cj) or len(set(cj)) != len(cj):
            mal.append(f"{k}: «celdas_de_juicio» tiene que ser una lista no vacía de celdas distintas")
            cj = []
        if not str(rc.get("regla") or "").strip():
            mal.append(f"{k}: «regla» vacía: hay que decir qué decisión hace que la entrada siga a la celda de juicio")
        for x in cj:
            fx = fase_de(x)
            if x not in org:
                mal.append(f"{k}: la celda de juicio {x} no es un origen de la fórmula")
            if fx not in ("A", "B"):
                mal.append(f"{k}: {x} no es una celda de juicio que escriban la fase A o la fase B (Anexo A, celdas_v2.py)"
                           + (" (la fase C escribe después del recálculo)" if fx == "C" else ""))
        for o in org:
            fo = fase_de(o)
            if fo is not None and o not in cj:
                mal.append(f"{k}: el origen {o} es una celda de juicio (fase {fo}) que no se declara en «celdas_de_juicio»")
            if fo is not None or o in cj:
                continue
            if o.startswith("aux:"):
                ea = por.get(o)
                if ea is None or not _num(ea.get("valor_modelo")):
                    mal.append(f"{k}: el auxiliar {o} no tiene entrada en el registro con un número en «valor_modelo»")
                continue
            if o in decl:
                mal.append(f"{k}: el origen {o} es otra entrada dependiente (no se admiten cadenas de recálculo)")
                continue
            h, _, r = o.partition("!")
            if lb is not None:
                if h not in lb.partes or not re.fullmatch(r"[A-Z]{1,3}\d+", r or ""):
                    mal.append(f"{k}: el origen {o} no es una celda del libro")
                elif lb.tiene_formula(h, r):
                    mal.append(f"{k}: el origen {o} es una fórmula del libro: antes del recálculo no tiene valor vigente")
        # cadenas: ninguna otra derivada del registro puede usar esta entrada sin declararse también
        for kk, ee in por.items():
            dd = ee.get("derivacion") if isinstance(ee.get("derivacion"), dict) else {}
            if kk != k and ee.get("clase") == "derivado" and k in (dd.get("origenes") or []) and kk not in decl:
                mal.append(f"{k}: la derivada {kk} del registro la usa como origen y no es una entrada dependiente declarada")
        # la vía generativa: la entrada no puede tener a la vez un «calculo» de fase1_historia
        for nombre, dj in (("fase1_v63.json", f1j), ("fase1_metadatos.json", metaj)):
            ent = ((dj or {}).get("analisis") or {}).get(ref) if isinstance(dj, dict) else None
            if isinstance(ent, dict) and isinstance(ent.get("calculo"), dict):
                mal.append(f"{k}: {nombre} la declara con un «calculo» de fase1_historia: dos derivaciones para una entrada")
            elif ent is not None and not isinstance(ent, dict) and not _num(ent):
                mal.append(f"{k}: {nombre} la declara sin un número")
        cf = rc.get("conciliacion_f1")
        partidas = _partidas_k3a(decl_f1, ref) if ref in COMPONENTES_K3A else []
        if cf is not None and not isinstance(cf, bool):
            mal.append(f"{k}: «conciliacion_f1» tiene que ser true o false")
        elif cf is True and ref not in COMPONENTES_K3A:
            mal.append(f"{k}: «conciliacion_f1» solo existe para los componentes {COMPONENTES_K3A} de F1-K3a")
        elif cf is True and len(partidas) != 1:
            mal.append(f"{k}: «conciliacion_f1» exige una sola partida de «conciliacion_fcf_base» con el componente {ref} en {DECLARACION_F1} "
                       f"(hay {len(partidas)})")
        elif cf is None and partidas:
            mal.append(f"{k}: {DECLARACION_F1} explica el componente {ref} en «conciliacion_fcf_base»: hay que declarar «conciliacion_f1» "
                       "(true: la partida sigue al valor; false: K3a la juzga tal como está)")
    return mal


# ---------------------------------------------------------------------------------------------------------------- cálculo
def _valor_libro(exacto, unidad):
    """(valor que se guarda, regla de precisión): la regla U2 de verificacion_entradas."""
    if VE.UNIDADES.get(VE._norm_txt(unidad)) is not None:
        v = float(VE._round_frac(exacto, 3))
        regla = "importe: el resultado exacto o su redondeo a 3 decimales (ROUND de la hoja, mitad lejos de cero; regla U2)"
        ok = VE._importe_libro_exacto(exacto, v)
    else:
        v = float(exacto)
        regla = "magnitud que no es un importe: el resultado exacto de la fórmula (un redondeo se declara en ella con round)"
        ok = VE._igual_exacto(float(exacto), v)
    if not ok:
        raise ErrorRecalculo(f"el valor {v!r} no cumple la regla U2 frente al exacto {exacto}")
    return (int(v) if v.is_integer() and abs(v) < 2 ** 53 else v), regla


def calcular(carpeta, reg=None, valores_juicio=None):
    """Evalúa cada entrada declarada sin escribir nada. {celda: {...}}. `valores_juicio` ({celda: número}) sustituye los valores de las
    celdas de juicio del libro evaluado (previsualización con fase_b.json). ErrorRecalculo si algo no se puede evaluar."""
    if reg is None:
        reg, err = VE.cargar(carpeta)
        if reg is None:
            raise ErrorRecalculo(err or f"no hay {VE.REGISTRO}")
    decl = declaradas(reg)
    datos, ev = libros(carpeta)
    if not decl:
        return {}
    if not os.path.isfile(ev):
        raise ErrorRecalculo(f"no hay libro evaluado ({os.path.basename(ev)}): la celda de juicio no está escrita")
    lb_ev = LibroV63(ev)
    lb_dat = LibroV63(datos) if os.path.isfile(datos) else None
    por = _por_celda(reg)
    out = {}
    for k, e in decl.items():
        d = e["derivacion"]
        cj = d["recalculo"]["celdas_de_juicio"]
        vals, proc = {}, {}
        for o in d["origenes"]:
            if o.startswith("aux:"):
                vals[o], proc[o] = por[o]["valor_modelo"], "registro (valor_modelo del auxiliar)"
                continue
            h, r = o.split("!", 1)
            if o in cj and valores_juicio is not None and o in valores_juicio:
                v, proc[o] = valores_juicio[o], "fase_b.json (previsualización)"
            else:
                v = lb_ev.leer(h, r)
                proc[o] = "libro evaluado tras escribir la fase B" if o in cj else "libro evaluado (celda de datos)"
                if o not in cj and lb_dat is not None and not _iguales(lb_dat.leer(h, r), v):
                    raise ErrorRecalculo(f"{k}: el origen {o} vale {v!r} en el libro evaluado y {lb_dat.leer(h, r)!r} en el de datos")
            if not _num(v):
                raise ErrorRecalculo(f"{k}: el origen {o} no es un número ({v!r})" + (": la celda de juicio está vacía o no es numérica tras la fase B, "
                                                                                    "y la fórmula declarada no se puede evaluar" if o in cj else ""))
            vals[o] = v
        try:
            exacto = VE._eval_formula_exacta(d["formula"], vals)
            inertes, locales = VE._sensibilidad(d["formula"], vals, list(d["origenes"]))
        except Exception as ex:  # noqa: BLE001
            raise ErrorRecalculo(f"{k}: fórmula no evaluable ({type(ex).__name__}: {str(ex)[:100]})") from None
        if inertes:
            raise ErrorRecalculo(f"{k}: los orígenes {inertes} no influyen en el resultado de la fórmula")
        if not locales and not (exacto == 0 and VE._suelo_cero(d["formula"])):
            raise ErrorRecalculo(f"{k}: con estos valores el resultado no depende de ningún origen")
        nuevo, regla = _valor_libro(exacto, d.get("unidad"))
        out[k] = {"celda": k, "exacto": exacto, "valor": nuevo, "precision": regla, "origenes": vals, "procedencia": proc,
                  "celdas_de_juicio": {x: vals[x] for x in cj}, "formula_sha256": _sha_texto(d["formula"]),
                  "regla": d["recalculo"].get("regla"), "conciliacion_f1": d["recalculo"].get("conciliacion_f1") is True,
                  "actual": lb_ev.leer("Análisis", k.split("!")[1])}
    return out


# ---------------------------------------------------------------------------------------------------------------- aplicación
def _traza(r, valor_declarado):
    return {"valor_declarado": valor_declarado, "valor": r["valor"], "exacto": f"{r['exacto'].numerator}/{r['exacto'].denominator}",
            "exacto_decimal": _es_exacto(r["exacto"], 12).replace(",", "."), "precision": r["precision"],
            "celdas_de_juicio": dict(r["celdas_de_juicio"]), "formula_sha256": r["formula_sha256"], "regla": r["regla"],
            "formula": f"{VE.REGISTRO} → {r['celda']} → derivacion.formula", "rastro": RASTRO}


def _nota_cm(r, valor_declarado):
    cj = "; ".join(f"{c} = {_es(v)}" for c, v in r["celdas_de_juicio"].items())
    return (f"{MARCA_NOTA} {cj} → {_es(r['valor'])} (exacto {_es_exacto(r['exacto'])}; valor declarado {_es(valor_declarado)}), con la fórmula de "
            f"la derivación registrada en {VE.REGISTRO} ({r['regla']}); entradas_dependientes.py en el paso 9, antes del recálculo del libro; "
            f"rastro en {RASTRO}. Si las columnas J y M describen un cálculo, es el del valor declarado.")


def _sin_marca(texto, marca):
    t = "" if texto is None else str(texto)
    i = t.find(marca)
    return t if i < 0 else t[:i]


def _preparar_libros(rutas, celdas, cfg):
    """Escribe las mismas celdas en una copia temporal de cada libro y la verifica con el verificador de la plantilla. Devuelve
    [(temporal, libro)]; no sustituye nada (si algo falla, borra los temporales y lanza ErrorRecalculo)."""
    pl = (cfg or {}).get("plantilla") or {}
    permitidas = None
    if pl.get("scripts_v63") and os.path.isdir(pl["scripts_v63"]):
        if pl["scripts_v63"] not in sys.path:
            sys.path.insert(0, pl["scripts_v63"])
        import inventario_entradas  # noqa: E402
        permitidas = inventario_entradas.conjunto_entradas()
    if permitidas is None or not pl.get("verificador") or not pl.get("referencia"):
        raise ErrorRecalculo("la configuración no da el inventario de entradas, el verificador o la referencia de la plantilla")
    tmps = []
    try:
        for p in rutas:
            lb = LibroV63(p)
            try:
                lb.escribir_celdas(celdas, permitidas)
            except (FormulaProtegida, CeldaNoPermitida) as ex:
                raise ErrorRecalculo(f"{os.path.basename(p)}: {ex}") from None
            lb.borrar_caches()
            tmp = p + ".dep.tmp.xlsx"
            lb.guardar(tmp)
            tmps.append((tmp, p))
            r = subprocess.run([sys.executable, pl["verificador"], tmp, pl["referencia"]], capture_output=True, text=True)
            if r.returncode != 0:
                raise ErrorRecalculo(f"{os.path.basename(p)} no pasa el verificador de la plantilla con el recálculo: " + (r.stdout + r.stderr)[-300:])
    except BaseException:
        _borrar(tmps)
        raise
    return tmps


def _borrar(tmps):
    for tmp, _ in tmps:
        if os.path.exists(tmp):
            os.remove(tmp)


def _con_rastro(x):
    return isinstance(x, dict) and isinstance(x.get("recalculo_dependiente"), dict)


def aplicar(carpeta, fase="B", cfg=None, ahora=None):
    """Recalcula y escribe las entradas dependientes (ver el docstring del módulo). Devuelve el resumen; ErrorRecalculo si no se puede
    (entonces no se ha escrito nada). Una copia con el valor que ya tenía no se toca salvo para poner al día un rastro anterior: el valor
    sin cambios no añade rastros a las copias (no invalida un vínculo sellado) y queda solo en recalculo_dependientes.json."""
    if fase != "B":
        raise ErrorRecalculo(f"solo se recalcula tras la fase B (se pidió la fase {fase!r})")
    reg, err = VE.cargar(carpeta)
    if reg is None:
        if err:
            raise ErrorRecalculo(err)
        return {"declaradas": [], "cambios": [], "sin_cambio": [], "escrito": []}
    if not declaradas(reg):
        return {"declaradas": [], "cambios": [], "sin_cambio": [], "escrito": []}
    problemas = validar(carpeta, reg)
    if problemas:
        raise ErrorRecalculo("declaración no válida: " + " | ".join(problemas))
    datos, ev = libros(carpeta)
    for p in (datos, ev):
        if not os.path.isfile(p):
            raise ErrorRecalculo(f"falta {os.path.basename(p)}")
    p_rastro = os.path.join(carpeta, RASTRO)
    rastro_prev = _json(p_rastro) if os.path.isfile(p_rastro) else None
    if os.path.isfile(p_rastro) and not isinstance(rastro_prev, dict):
        raise ErrorRecalculo(f"{RASTRO} existe y no se puede leer: el rastro anterior no se pisa")
    if cfg is None:
        import config_v2
        cfg = config_v2.cargar()
    res = calcular(carpeta, reg)
    lb_dat, lb_ev = LibroV63(datos), LibroV63(ev)
    p_f1, p_meta, p_reg, p_dec = (os.path.join(carpeta, n) for n in ("fase1_v63.json", "fase1_metadatos.json", VE.REGISTRO, DECLARACION_F1))
    f1j, metaj = _json(p_f1), _json(p_meta)
    decl_f1 = _f1_decl(carpeta)
    por = _por_celda(reg)
    celdas_libro, cambios, sin_cambio, vigente = {}, [], [], {}
    toca = {"fase1_v63.json": False, "fase1_metadatos.json": False, VE.REGISTRO: False, DECLARACION_F1: False}
    for k, r in res.items():
        ref = k.split("!")[1]
        actual, nuevo = r["actual"], r["valor"]  # valor del libro evaluado antes del recálculo · valor recalculado
        if not _num(actual):
            raise ErrorRecalculo(f"{k}: el libro evaluado no tiene un número ({actual!r})")
        # 1. todas las copias tienen el valor actual del libro evaluado o ya el nuevo (una aplicación anterior interrumpida)
        copias = {"libro de datos": lb_dat.leer("Análisis", ref), f"{VE.REGISTRO} (valor_modelo)": por[k].get("valor_modelo")}
        entradas_f1 = {}
        for nombre, dj in (("fase1_v63.json", f1j), ("fase1_metadatos.json", metaj)):
            an = dj.get("analisis") if isinstance(dj, dict) else None
            if isinstance(an, dict) and ref in an:
                entradas_f1[nombre] = an
                copias[nombre] = an[ref].get("valor") if isinstance(an[ref], dict) else an[ref]
        distintas = {n: v for n, v in copias.items() if not (_iguales(v, actual) or _iguales(v, nuevo))}
        if distintas:
            raise ErrorRecalculo(f"{k}: las copias no tienen el valor del libro evaluado ({actual!r}) ni el recalculado ({nuevo!r}): {distintas}")
        # 2. valor declarado (el anterior al primer recálculo): el del rastro del registro o, si no lo hay, el actual
        tr_prev = por[k].get("recalculo_dependiente") if _con_rastro(por[k]) else None
        vd = tr_prev["valor_declarado"] if tr_prev and _num(tr_prev.get("valor_declarado")) else actual
        traza = _traza(r, vd)
        vigente[k] = dict(traza, celda=k)
        cambia = not all(_iguales(v, nuevo) for v in list(copias.values()) + [actual])
        (cambios if cambia else sin_cambio).append({"celda": k, "antes": actual, "despues": nuevo, "valor_declarado": vd,
                                                   "celdas_de_juicio": dict(r["celdas_de_juicio"])})
        # 3. libros: el valor y una nota en la columna N de su fila del Control maestro (las mismas celdas en los dos libros)
        if not _iguales(actual, nuevo) or not _iguales(copias["libro de datos"], nuevo):
            celdas_libro[k] = nuevo
        fila = _fila_cm(lb_ev, k)
        if fila is not None:
            if _fila_cm(lb_dat, k) != fila:
                raise ErrorRecalculo(f"{k}: la fila del Control maestro no es la misma en los dos libros")
            n_ev, n_dat = (_texto_celda(lb, "Control maestro", f"N{fila}") for lb in (lb_ev, lb_dat))
            if _sin_marca(n_ev, MARCA_NOTA) != _sin_marca(n_dat, MARCA_NOTA):
                raise ErrorRecalculo(f"{k}: la evidencia N{fila} del Control maestro no es la misma en los dos libros")
            n_nuevo = _sin_marca(n_ev, MARCA_NOTA).rstrip() + _nota_cm(r, vd)
            con_marca = MARCA_NOTA in str(n_ev or "") or MARCA_NOTA in str(n_dat or "")
            if (cambia or con_marca) and (n_nuevo != n_ev or n_nuevo != n_dat):
                celdas_libro[f"Control maestro!N{fila}"] = n_nuevo
        # 4. fase1_v63.json y fase1_metadatos.json: la vía generativa reproduce el libro
        for nombre, an in entradas_f1.items():
            ent = an[ref] if isinstance(an[ref], dict) else {"valor": an[ref]}
            if not _iguales(ent.get("valor"), nuevo) or (_con_rastro(ent) and ent["recalculo_dependiente"] != traza):
                an[ref] = dict(ent, valor=nuevo, recalculo_dependiente=traza)
                toca[nombre] = True
        # 5. registro: valor_modelo y rastro (la comprobación, el vínculo, la fuente y la derivación no se tocan)
        if not _iguales(por[k].get("valor_modelo"), nuevo) or (tr_prev is not None and tr_prev != traza):
            por[k]["valor_modelo"] = nuevo
            por[k]["recalculo_dependiente"] = traza
            toca[VE.REGISTRO] = True
        # 6. F1-K3a: la partida declarada sigue al valor (su importe cambia exactamente lo que cambia la entrada)
        if r["conciliacion_f1"]:
            i = _partidas_k3a(decl_f1, ref)[0]
            it = decl_f1["conciliacion_fcf_base"][i]
            if not _num(it.get("importe")):
                raise ErrorRecalculo(f"{k}: la partida de {DECLARACION_F1} del componente {ref} no tiene un importe numérico")
            tp = it.get("recalculo_dependiente") if _con_rastro(it) else None
            if tp is not None:
                if not (all(_num(tp.get(x)) for x in ("importe_declarado", "valor_declarado", "valor"))
                        and _frac(it["importe"]) == _frac(tp["importe_declarado"]) + _frac(tp["valor"]) - _frac(tp["valor_declarado"])
                        and (_iguales(tp["valor"], actual) or _iguales(tp["valor"], nuevo))):
                    raise ErrorRecalculo(f"{k}: la partida de {DECLARACION_F1} del componente {ref} cambió después de su último recálculo (su importe "
                                         "no es el de su rastro): se revisa a mano")
                imp_d, val_d = tp["importe_declarado"], tp["valor_declarado"]
            else:
                imp_d, val_d = it["importe"], actual
            imp_x = _frac(imp_d) + _frac(nuevo) - _frac(val_d)
            imp_n = int(imp_x) if imp_x.denominator == 1 else float(imp_x)
            if _frac(imp_n) != imp_x:
                raise ErrorRecalculo(f"{k}: el importe de la partida no se puede escribir exacto ({imp_x})")
            tr_f1 = {"celda": k, "importe_declarado": imp_d, "valor_declarado": val_d, "valor": nuevo, "importe": imp_n,
                     "celdas_de_juicio": dict(r["celdas_de_juicio"]), "rastro": RASTRO}
            partida = _sin_marca(it.get("partida"), MARCA_PARTIDA).rstrip() + (
                f"{MARCA_PARTIDA} {'; '.join(f'{c} = {_es(v)}' for c, v in r['celdas_de_juicio'].items())}; {ref} {_es(val_d)} → {_es(nuevo)}; "
                f"importe {_es(imp_d)} → {_es(imp_n)} ({RASTRO})]")
            if not _iguales(it.get("importe"), imp_n) or (tp is not None and (tp != tr_f1 or it.get("partida") != partida)):
                decl_f1["conciliacion_fcf_base"][i] = dict(it, importe=imp_n, partida=partida, recalculo_dependiente=tr_f1)
                toca[DECLARACION_F1] = True
            vigente[k]["conciliacion_f1"] = tr_f1
    escrito = sorted(n for n, v in toca.items() if v) + ([os.path.basename(datos), os.path.basename(ev)] if celdas_libro else [])
    resumen = {"declaradas": sorted(res), "cambios": cambios, "sin_cambio": sin_cambio, "escrito": escrito, "rastro": RASTRO}
    if not escrito and isinstance(rastro_prev, dict) and rastro_prev.get("vigente") == vigente:
        return dict(resumen, rastro_sin_cambios=True)
    nombres = ["fase1_v63.json", "fase1_metadatos.json", VE.REGISTRO, DECLARACION_F1, os.path.basename(datos), os.path.basename(ev)]
    antes = {n: _sha(os.path.join(carpeta, n)) for n in nombres}
    # escritura: los libros se preparan y se verifican ANTES de escribir nada; después las declaraciones JSON (con su rastro) y, por
    # último, la sustitución de los libros (primero el de datos)
    tmps = _preparar_libros([datos, ev], celdas_libro, cfg) if celdas_libro else []
    try:
        for nombre, ruta, d in ((DECLARACION_F1, p_dec, decl_f1), ("fase1_metadatos.json", p_meta, metaj), ("fase1_v63.json", p_f1, f1j),
                                (VE.REGISTRO, p_reg, reg)):
            if toca[nombre]:
                _volcar_json(ruta, d)
    except BaseException:
        _borrar(tmps)
        raise
    for tmp, p in tmps:
        os.replace(tmp, p)
    despues = {n: _sha(os.path.join(carpeta, n)) for n in nombres}
    ahora = ahora or dt.datetime.now().astimezone().isoformat(timespec="seconds")
    aplicacion = {"fecha": ahora, "paso": 9, "fase": fase, "fase_b_sha256": _sha(os.path.join(carpeta, "fase_b.json")), "cambios": cambios,
                  "sin_cambio": sin_cambio, "escrito": escrito,
                  "archivos": {n: {"antes": antes[n], "despues": despues[n]} for n in nombres if antes[n] != despues[n]},
                  "origenes": {k: {o: {"valor": v, "de": r["procedencia"][o]} for o, v in r["origenes"].items()} for k, r in res.items()}}
    rastro = {"formato": FORMATO,
              "que": ("Recálculo determinista de las entradas declaradas que dependen de celdas de juicio (entradas_dependientes.py, lanzado por el "
                      "pipeline en el paso 9, tras escribir la fase B y antes del recálculo del libro y de la fase C). La declaración, la fórmula y sus "
                      f"orígenes están en {VE.REGISTRO} (derivacion.recalculo); ningún agente de juicio interviene. No acredita la revisión de "
                      "ninguna entrada ni aptitud alguna."),
              "registro": VE.REGISTRO, "vigente": vigente, "historial": list((rastro_prev or {}).get("historial") or []) + [aplicacion]}
    _volcar_json(p_rastro, rastro)
    _resultados(carpeta, rastro)
    return resumen


def _resultados(carpeta, rastro):
    """Copia del rastro y resumen legible en ../resultados/ (la carpeta del ensayo, junto a cambio_de_base.json)."""
    e = os.path.basename(os.path.abspath(carpeta))
    res = os.path.join(os.path.dirname(os.path.abspath(carpeta)), "resultados")
    os.makedirs(res, exist_ok=True)
    _volcar_json(os.path.join(res, f"recalculo_dependientes_{e}.json"), rastro)
    ult = rastro["historial"][-1]
    md = [f"# Recálculo de las entradas dependientes de celdas de juicio · {e}", "",
          f"Lanzado por el pipeline en el paso 9 (fase {ult['fase']}), tras escribir la fase B y antes del recálculo del libro y de la fase C; "
          f"fase_b.json `{str(ult.get('fase_b_sha256'))[:16]}…`; {ult['fecha']}. La fórmula y sus orígenes son los de la derivación registrada en "
          f"`{VE.REGISTRO}` (`derivacion.recalculo`); el rastro auditado es `{e}/{RASTRO}`. No acredita aptitud ni la revisión de ninguna entrada: "
          "el revisor independiente vuelve a sellar las que cambian.", "",
          "| Entrada | Celdas de juicio | Antes | Después | Exacto | Valor declarado |", "|---|---|---|---|---|---|"]
    for x in ult["cambios"] + ult["sin_cambio"]:
        v = rastro["vigente"].get(x["celda"]) or {}
        md.append(f"| {x['celda']} | {'; '.join(f'{c} = {_es(val)}' for c, val in x['celdas_de_juicio'].items())} | {_es(x['antes'])} | "
                  f"{_es(x['despues'])} | {v.get('exacto_decimal')} | {_es(x['valor_declarado'])} |")
    md += ["", f"Archivos escritos: {', '.join(ult['escrito']) or 'ninguno (sin cambios)'}."]
    for k, v in rastro["vigente"].items():
        if v.get("conciliacion_f1"):
            t = v["conciliacion_f1"]
            md.append(f"- {k}: partida de F1-K3a de `{DECLARACION_F1}` · importe {_es(t['importe_declarado'])} declarado → {_es(t['importe'])}.")
    open(os.path.join(res, f"recalculo_dependientes_{e}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")


def resumen_texto(r):
    cam = "; ".join(f"{x['celda']} {x['antes']!r} → {x['despues']!r} ({', '.join(f'{c} = {v!r}' for c, v in x['celdas_de_juicio'].items())})" for x in r.get("cambios") or [])
    sin = ", ".join(x["celda"] for x in r.get("sin_cambio") or [])
    return (f"{len(r.get('declaradas') or [])} entradas dependientes declaradas · recalculadas: {cam or 'ninguna'}" + (f" · sin cambio: {sin}" if sin else "")
            + (f" · rastro en {RASTRO}" if r.get("rastro") else ""))


def _valores_fase_b(p):
    import fase_a_celdas as FA
    fb = _json(p)
    if not isinstance(fb, dict):
        raise ErrorRecalculo(f"{p} no se puede leer")
    celdas, _, _ = FA.convertir(fb, "B")
    return {k: v for k, v in celdas.items() if not k.startswith("Control maestro!")}


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("orden", choices=["validar", "previsualizar", "aplicar"])
    ap.add_argument("carpeta")
    ap.add_argument("--fase", default="B")
    ap.add_argument("--fase-b", help="previsualizar: fase_b.json con las celdas de juicio que escribirá la fase B")
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    c = os.path.abspath(a.carpeta)
    reg, err = VE.cargar(c)
    if reg is None and err:
        print(f"ERROR: {err}")
        return 1
    if not declaradas(reg):
        print("sin entradas dependientes declaradas en el registro: no se hace nada")
        return 0
    try:
        if a.orden == "validar":
            mal = validar(c, reg)
            for m in mal:
                print("  - " + m)
            print(("DECLARACIÓN NO VÁLIDA: " if mal else "OK: ") + f"{len(declaradas(reg))} entradas dependientes declaradas · {len(mal)} problemas")
            return 1 if mal else 0
        if a.orden == "previsualizar":
            mal = validar(c, reg)
            if mal:
                raise ErrorRecalculo("declaración no válida: " + " | ".join(mal))
            vj = _valores_fase_b(a.fase_b) if a.fase_b else None
            for k, r in calcular(c, reg, valores_juicio=vj).items():
                print(f"{k}: actual {r['actual']!r} → {r['valor']!r} (exacto {float(r['exacto'])!r}; {r['precision']}) con "
                      + ", ".join(f"{x} = {v!r} [{r['procedencia'][x]}]" for x, v in r["celdas_de_juicio"].items()))
            print("previsualización: no se ha escrito nada")
            return 0
        import config_v2
        r = aplicar(c, a.fase, config_v2.cargar(a.config) if a.config else None)
    except ErrorRecalculo as ex:
        print(f"RECÁLCULO DETENIDO (no se ha escrito nada): {ex}")
        return 1
    print("RESUMEN_JSON " + json.dumps(r, ensure_ascii=False, default=str))
    print("OK: " + resumen_texto(r))
    return 0


if __name__ == "__main__":
    sys.exit(main())
