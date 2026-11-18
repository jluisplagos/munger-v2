#!/usr/bin/env python3
"""Batería F1-SERIES-ESCALA (4.15, F1): escala de la cifra impresa y ceros sin cifra en las series F1 (guarda F1-SERIES de motor_a_f1.py).

Uso (desde personaje_v2/): python3 -B pruebas/test_f1_series_escala.py
Sin LibreOffice ni binarios: una fuente sintética con marcas de página, escrita en una carpeta temporal con su huella.
Casos de partida (examen del universo, jumbo_d): Jumbo publica en euros enteros y el modelo trabaja en millones; su PPA es cero porque no hay
intangibles de combinaciones, y el informe lo dice con una frase, sin cifra. Y, de la revisión de f1/usgaap (R1-2): un cero publicado como «—».
Grupos: ESC (escala), CC (cero comprobado por una frase), CI (cero impreso sin dígitos), LS (leer_serie: V-F1e) y ANT (lo que bloqueaba
antes sigue bloqueando). Cada aceptación tiene sus mutaciones.
"""
import copy
import hashlib
import os
import shutil
import sys
import tempfile
from fractions import Fraction as Fr

AQUI = os.path.dirname(os.path.abspath(__file__))
PV = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(PV, "scripts"))
import motor_a_f1 as M  # noqa: E402

R = []


def paso(nombre, ok, detalle=""):
    R.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


ANIOS = list(range(2016, 2026))


def fila(etiqueta, *celdas, ancho=40, col=14):
    """Una línea de tabla: la etiqueta en `ancho` caracteres y cada celda alineada a la derecha en `col` (como pdftotext -layout)."""
    return etiqueta.ljust(ancho) + "".join(c.rjust(col) for c in celdas)


FRASE = ("The Group has no intangible assets arising from business combinations; its only intangible asset is "
         "software developed for internal use.")
FRASE_IMPORTE = "The carrying amount of software amounted to 1.234.567 euros at the end of the financial year."
PAGINAS = {
    1: [fila("(Amounts in euros)", "2025", "2024", "2023"),
        fila("Depreciation of right-of-use assets", "(9.199.774)", "(8.660.374)", "(7.942.175)"),
        fila("Amortisation of acquired intangibles", "—", "–", "nil"),
        fila("- Additions", "(1.234.567)", "(1.111.111)", "(1.000.000)"),
        fila("Glued marks", "—5", "x—", "(3)"),
        fila("Dash in 2024 only", "4", "—", "6")],
    2: ["Note 5.8 Intangible assets", "", FRASE[:FRASE.rindex(" ", 0, 60)], FRASE[FRASE.rindex(" ", 0, 60) + 1:], "", FRASE_IMPORTE],
    3: ["Lease note without year headers", fila("Finance lease principal", "2", "1", "—")],
    5: ["Group (in thousands of euros)", fila("", "2025", "2024"), fila("- Additions", "(1.234.567)", "(1.111.111)")],
    # (revisión, hallazgos A y B) una nota en millones como la del 10-K de Zoetis: guion dentro de la etiqueta, negativo «- 7» con espacio,
    # y un «Year ended 2024» cuyo año queda alineado con el guion de «Lease payable - principal» (sonda S3 de la revisión)
    6: ["Leases (in millions)", "Year ended 2024", fila("", "2025", "2024", "2023"),
        fila("Financing cash flows – finance leases", "2", "1", "—"),
        fila("Amortisation of other intangibles", "- 5", "- 7", "—"),
        fila("Lease payable - principal", "(12)", "(10)", "(9)"),
        fila("Right-of-use depreciation", "(3)", "(2)", "(1)")],
    # (ronda 2 de la revisión, límites 1 y 2) página de continuación (el encabezado en millones quedó en la anterior) con otra tabla
    # «(in thousands)» debajo; y «All amounts in euros (thousands)», que no es «unidades»
    7: ["Note 7 Leases (continued)", fila("", "2025", "2024", "2023"), fila("Right-of-use depreciation", "(450)", "(430)", "(410)"), "",
        "Fees of the auditor (in thousands)", fila("Audit fees", "812", "790", "755")],
    8: ["All amounts in euros (thousands) unless otherwise stated", fila("", "2025", "2024", "2023"),
        fila("Right-of-use depreciation", "(9.200)", "(8.660)", "(7.942)")],
}
TEXTO = "".join(f"[PDF PAGE {n}]\n" + "\n".join(lineas) + "\n" for n, lineas in sorted(PAGINAS.items()))
SHA = hashlib.sha256(TEXTO.encode("utf-8")).hexdigest()
CT = tempfile.mkdtemp(prefix="f1_series_escala_")
os.makedirs(os.path.join(CT, "texto"))
open(os.path.join(CT, "texto", "ar2025.txt"), "w", encoding="utf-8").write(TEXTO)
FS = {"AR2025": {"archivo": "texto/ar2025.txt", "sha256": SHA}}


def ent(lit, vf, sg=-1, fila_="Depreciation of right-of-use assets", pagina=1, **k):
    e = {"valor_fuente": vf, "signo": sg, "tratamiento": "publicado entre paréntesis" if sg == -1 else "ninguno", "documento": "AR2025",
         "pagina": pagina, "literal": lit}
    if fila_:
        e["fila"] = fila_
    e.update(k)
    return e


def cero(cita=FRASE, motivo="sin intangibles de combinaciones de negocios", pagina=2, **k):
    e = {"valor_fuente": 0, "signo": 1, "tratamiento": "ninguno", "documento": "AR2025", "pagina": pagina,
         "cero_comprobado": {"motivo": motivo, "cita": cita}}
    e.update(k)
    return e


def gs(serie, nombre="da_rou", fuentes=None, carpeta=CT):
    """(guarda F1-SERIES, resumen) para una serie con las entradas dadas."""
    d = {"series": {nombre: serie}, "fuentes_series": copy.deepcopy(FS if fuentes is None else fuentes)}
    G, res = M.Guardas(), {}
    M._guarda_fuentes_series(G, d, carpeta, ANIOS, res)
    ULTIMA[:] = G.lista
    return [x for x in G.lista if x["id"] == "F1-SERIES"][0], res["F1_SERIES"]


ULTIMA = []   # guardas de la última evaluación de gs (para F1-SERIES-CERO)


def aviso_cero():
    return next((x for x in ULTIMA if x["id"] == "F1-SERIES-CERO"), None)


def bloquea(g, efecto=None, texto=None):
    return g["salta"] and g["severidad"] == "BLOQUEA" and (efecto is None or g["efecto"] == efecto) and (texto is None or texto in g["detalle"])


def libre(g):
    return not g["salta"]


# ================================================================== ESC · escala de la cifra impresa
g, r = gs({"2025": ent("(9.199.774)", -9.199774, escala="unidades"), "2024": ent("(8.660.374)", -8.660374, escala="unidades"),
           "2023": ent("(7.942.175)", -7.942175, escala="unidades")})
paso("ESC · cifras impresas en euros con escala «unidades» y valor_fuente en millones → F1-SERIES no salta; 3 columnas comprobadas",
     libre(g) and r["columna_comprobada"] == 3, g["detalle"][:160])
g, r = gs({"2025": ent("(1.234.567)", -1234.567, fila_="- Additions", escala="miles", pagina=5)})
paso("ESC · escala «miles»: «(1.234.567)» miles = −1.234,567 millones → no salta (la etiqueta «- Additions» con guion no estorba)",
     libre(g) and r["columna_comprobada"] == 1, g["detalle"][:160])
F_ROU6 = "Right-of-use depreciation"
g, r = gs({"2025": ent("(3)", -3, fila_=F_ROU6, pagina=6, escala="millones"), "2024": ent("(2)", -2, fila_=F_ROU6, pagina=6)})
paso("ESC · escala «millones» explícita en una página «(in millions)» = sin escala (el comportamiento anterior) → no salta; 2 columnas",
     libre(g) and r["columna_comprobada"] == 2 and not r["columna_pendiente"], g["detalle"][:200])
g, _ = gs({"2025": ent("(3)", -0.003, fila_=F_ROU6, pagina=6, escala="miles")})
paso("ESC · revisión B (S1): escala «miles» a la baja en una página «(in millions)» → DATOS INVÁLIDOS (la página declara otra escala)",
     bloquea(g, "DATOS INVÁLIDOS", "declara ['millones']"), g["detalle"][:200])
g, _ = gs({"2025": ent("(3)", -0.000003, fila_=F_ROU6, pagina=6, escala="unidades")})
paso("ESC · revisión B (S1b): escala «unidades» a la baja en una página «(in millions)» → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "declara ['millones']"), g["detalle"][:200])
g, _ = gs({"2025": ent("(1.234.567)", -1234.567, fila_="- Additions", escala="miles", pagina=1)})
paso("ESC · revisión B: escala «miles» en una página «(Amounts in euros)» → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "declara ['unidades']"))
g, _ = gs({"2025": ent("(1.234.567)", -1.234567, fila_="- Additions", escala="unidades", pagina=5)})
paso("ESC · revisión B: escala «unidades» en una página «in thousands of euros» → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "declara ['miles']"))
g, r = gs({"2025": ent("2", 2, sg=1, fila_="Finance lease principal", pagina=3, escala="millones")})
paso("ESC · revisión B: página sin encabezado de escala → la escala queda PENDIENTE (declarada y no comprobada; no bloquea)",
     libre(g) and any("NO comprobada" in x for x in r["columna_pendiente"]), str(r["columna_pendiente"])[:200])
g, r = gs({"2025": ent("(3)", -3, fila_=F_ROU6, pagina=6)})
paso("ESC · revisión B: sin «escala» no se contrasta nada (el comportamiento anterior, sin pendiente nuevo)",
     libre(g) and not r["columna_pendiente"])
EP = getattr(M, "_escala_de_pagina", lambda t: None)   # sin la función (código anterior) la prueba falla, no se interrumpe
paso("ESC · marcas de escala: «(amounts in Euro)», «(in millions, except per share data)», «€000», «EUR m», «en miles de euros»; la prosa no",
     EP("Note 5.8 (amounts in Euro)") == {"unidades"} and EP("(in millions, except per share data)") == {"millones"}
     and EP("Revenue (€000)") == {"miles"} and EP("EUR m 2025 2024") == {"millones"}
     and EP("Cifras en miles de euros") == {"miles"}
     and EP("Sales grew to EUR 15 million and 300 millones de euros") == set())
g, _ = gs({"2025": ent("(9.199.774)", -9.199774)})
paso("ESC · sin escala, cifra en euros y valor_fuente en millones → DATOS INVÁLIDOS (como antes)",
     bloquea(g, "DATOS INVÁLIDOS", "no es la cifra publicada"), g["detalle"][:160])
g, _ = gs({"2025": ent("(9.199.774)", -9.199774, escala="miles")})
paso("ESC · mutación: escala mal declarada («miles» para euros) → DATOS INVÁLIDOS en la escala del modelo",
     bloquea(g, "DATOS INVÁLIDOS", "en la escala del modelo (impresa en miles)"), g["detalle"][:160])
g, _ = gs({"2025": ent("(9.199.774)", -9.199774, escala="millones")})
paso("ESC · mutación: escala «millones» para una cifra en euros → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "en la escala del modelo"))
g, _ = gs({"2025": ent("(9.199.774)", -9199774, escala="unidades")})
paso("ESC · mutación: valor_fuente en euros (no en la escala del modelo) con escala «unidades» → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "en la escala del modelo"))
for mal in ("euros", "Unidades", "mil", 1000, None, ["unidades"]):
    g, _ = gs({"2025": ent("(9.199.774)", -9.199774, escala=mal)})
    paso(f"ESC · mutación: escala {mal!r} no es uno de los tres valores → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no válida"), g["detalle"][:120])
g, _ = gs({"2025": ent("(9.199.775)", -9.199775, escala="unidades")})
paso("ESC · mutación: la cita no contiene la cifra impresa («(9.199.775)», coherente con valor_fuente) → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no está, como cifra completa"), g["detalle"][:160])
g, _ = gs({"2025": ent("(9,199774)", -9.199774, escala="unidades")})
paso("ESC · mutación: «literal» con la cifra en millones y escala «unidades» → DATOS INVÁLIDOS (la conversión no la reproduce)",
     bloquea(g, "DATOS INVÁLIDOS", "en la escala del modelo"))
g, _ = gs({"2025": ent("(8.660.374)", -8.660374, escala="unidades")})
paso("ESC · mutación: cifra de 2024 declarada como de 2025, con escala → DATOS INVÁLIDOS (columna de otro ejercicio)",
     bloquea(g, "DATOS INVÁLIDOS", "columna de ['2024']"), g["detalle"][:160])
g, _ = gs({"2025": ent("9.199.774", 9.199774, sg=1, escala="unidades")})
paso("ESC · mutación: el signo publicado se cambia en valor_fuente con escala → DATOS INVÁLIDOS (R415-SIGNO)",
     bloquea(g, "DATOS INVÁLIDOS"), g["detalle"][:160])
g, _ = gs({"2025": ent("(9.199.774)", -9.199774, escala="unidades", pagina=99)})
paso("ESC · mutación: página inexistente con escala → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no existe"))

# ================================================================== CC · cero sin cifra impresa, probado por una frase
g, r = gs({"2025": cero(), "2024": cero()}, nombre="da_ppa")
paso("CC · cero_comprobado con motivo y cita literal en su página → F1-SERIES no salta; queda PENDIENTE de revisor (2)",
     libre(g) and len(r["columna_pendiente"]) == 2 and all("cero comprobado" in x for x in r["columna_pendiente"]) and "PENDIENTE en 2" in g["detalle"],
     g["detalle"][:160])
g, _ = gs({"2025": cero(cita=FRASE.upper().replace(" ", "   "))}, nombre="da_ppa")
paso("CC · la cita se compara sin distinguir espacios ni mayúsculas (la frase cruza dos líneas en la página)", libre(g), g["detalle"][:120])
g, _ = gs({"2025": cero(cita="")}, nombre="da_ppa")
paso("CC · mutación: cero sin cita → INCOMPLETO", bloquea(g, "INCOMPLETO", "sin «motivo» o sin «cita»"))
g, _ = gs({"2025": cero(motivo=" ")}, nombre="da_ppa")
paso("CC · mutación: cero sin motivo → INCOMPLETO", bloquea(g, "INCOMPLETO", "sin «motivo» o sin «cita»"))
g, _ = gs({"2025": cero(cita=FRASE, pagina=1)}, nombre="da_ppa")
paso("CC · mutación: la cita no está en la página indicada (es de la página 2, se cita la 1) → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no está en la página 1"))
g, _ = gs({"2025": cero(cita="The Group has no intangible assets arising from acquisitions of subsidiaries at all.")}, nombre="da_ppa")
paso("CC · mutación: cita inventada (no literal) → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no está en la página 2"))
g, _ = gs({"2025": cero(cita="Note 5.8 Intangible assets")}, nombre="da_ppa")
paso("CC · mutación: la cita es un encabezado (no prueba la inexistencia) → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "un fragmento no prueba"))
g, _ = gs({"2025": cero(cita=FRASE_IMPORTE)}, nombre="da_ppa")
paso("CC · mutación: la cita es una cifra (un importe del software), no la prueba de una inexistencia → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "contiene importes"), g["detalle"][:160])
g, _ = gs({"2025": cero(valor_fuente=0.5)}, nombre="da_ppa")
paso("CC · mutación: cero_comprobado con valor_fuente 0,5 → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "un cero tiene «valor_fuente» 0"))
g, _ = gs({"2025": cero(literal="(1.234)")}, nombre="da_ppa")
paso("CC · mutación: cero_comprobado con un «literal» → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no lleva cifra"))
g, _ = gs({"2025": cero(cero_comprobado="no hay intangibles")}, nombre="da_ppa")
paso("CC · mutación: cero_comprobado que no es {motivo, cita} → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "se declara {motivo, cita}"))
g, _ = gs({"2025": cero(pagina=99)}, nombre="da_ppa")
paso("CC · mutación: página inexistente → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no existe"))
g, _ = gs({"2025": cero(documento="AR2099")}, nombre="da_ppa")
paso("CC · mutación: documento sin fuente registrada → INCOMPLETO", bloquea(g, "INCOMPLETO", "sin fuente registrada"))
fs_mal = copy.deepcopy(FS)
fs_mal["AR2025"]["sha256"] = "0" * 64
g, _ = gs({"2025": cero()}, nombre="da_ppa", fuentes=fs_mal)
paso("CC · mutación: huella de la fuente distinta → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "cambió"))
g, _ = gs({"2025": cero(escala="euros")}, nombre="da_ppa")
paso("CC · mutación: escala no válida también en un cero → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no válida"))

# ================================================================== CI · cero publicado sin dígitos («—», «–», «-», «nil»)
F_PPA = "Amortisation of acquired intangibles"
g, r = gs({"2025": ent("—", 0, sg=1, fila_=F_PPA), "2024": ent("–", 0, sg=1, fila_=F_PPA), "2023": ent("nil", 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("CI · «—», «–» y «nil» en la fila y en la columna de su ejercicio → F1-SERIES no salta; 3 columnas comprobadas",
     libre(g) and r["columna_comprobada"] == 3, g["detalle"][:160])
g, r = gs({"2024": ent("—", 0, sg=1, fila_="Dash in 2024 only")}, nombre="da_ppa")
paso("CI · «—» entre dos cifras de otras columnas, en la de su ejercicio → no salta", libre(g) and r["columna_comprobada"] == 1, g["detalle"][:160])
g, r = gs({"2023": ent("—", 0, sg=1, fila_="Finance lease principal", pagina=3)}, nombre="da_ppa")
paso("CI · «—» en la fila sin encabezado de ejercicio alineado (como el 10-K de Zoetis, R1-2) → PENDIENTE, no bloquea",
     libre(g) and len(r["columna_pendiente"]) == 1 and "PENDIENTE" in g["detalle"], g["detalle"][:160])
g, _ = gs({"2025": ent("—", 0, sg=1, fila_=None)}, nombre="da_ppa")
paso("CI · mutación: «—» sin «fila» → INCOMPLETO (un guion suelto no prueba un cero)", bloquea(g, "INCOMPLETO", "sin «fila»"))
g, _ = gs({"2025": ent("—", 0, sg=1, fila_="Depreciation of right-of-use assets")}, nombre="da_ppa")
paso("CI · mutación: la fila declarada no tiene la marca → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"))
g, _ = gs({"2025": ent("—", 0, sg=1, fila_="Dash in 2024 only")}, nombre="da_ppa")
paso("CI · mutación: la marca está en la columna de otro ejercicio (2024, declarada 2025) → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "columna de ['2024']"), g["detalle"][:160])
g, _ = gs({"2024": ent("—", 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("CI · mutación: «—» declarado donde se imprime «–» (otra marca) → DATOS INVÁLIDOS (la marca impresa literal)",
     bloquea(g, "DATOS INVÁLIDOS", "columna de ['2025']"), g["detalle"][:160])
g, _ = gs({"2025": ent("-", 0, sg=1, fila_="- Additions", escala="miles")}, nombre="da_ppa")
paso("CI · mutación: el guion de la etiqueta («- Additions») no es un cero de la fila → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"))
g, _ = gs({"2025": ent("—", 0, sg=1, fila_="Glued marks"), "2024": ent("—", 0, sg=1, fila_="Glued marks")}, nombre="da_ppa")
paso("CI · mutación: marcas pegadas a una cifra o a una palabra («—5», «x—») no son ceros → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso") and g["detalle"].count("no contiene el cero impreso") == 2)
g, _ = gs({"2025": ent("—", 1.5, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("CI · mutación: «—» con valor_fuente 1,5 → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "un cero tiene «valor_fuente» 0"))
g, _ = gs({"2025": ent("—", 0, sg=1, fila_="Amortisation")}, nombre="da_ppa")
paso("CI · la fila identifica una sola línea: «Amortisation» la identifica y su «—» es de 2025 → no salta", libre(g), g["detalle"][:120])
g, _ = gs({"2025": ent("—", 0, sg=1, fila_="of")}, nombre="da_ppa")
paso("CI · mutación: la fila está en varias líneas → INCOMPLETO", bloquea(g, "INCOMPLETO", "líneas de la página"), g["detalle"][:160])
g, _ = gs({"2025": ent("cero", 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("CI · mutación: «cero» no es una marca reconocida → DATOS INVÁLIDOS (no es una cifra)", bloquea(g, "DATOS INVÁLIDOS", "no es una cifra"))

# (ronda 2 de la revisión, límites 1 y 2, y detalle menor)
g, r = gs({"2025": ent("(450)", -0.45, fila_=F_ROU6, pagina=7, escala="miles")})
paso("ESC · ronda 2, R1: la marca «(in thousands)» de otra tabla, debajo de la fila, no comprueba la escala → PENDIENTE (no comprobada)",
     libre(g) and r["columna_comprobada"] == 0 and any("NO comprobada" in x for x in r["columna_pendiente"]), str(r["columna_pendiente"])[:200])
g, r = gs({"2025": ent("(9.200)", -0.0092, fila_=F_ROU6, pagina=8, escala="unidades")})
paso("ESC · ronda 2, R2: «All amounts in euros (thousands)» no es «unidades»: declarado «unidades» → PENDIENTE, no comprobada",
     libre(g) and r["columna_comprobada"] == 0 and any("NO comprobada" in x for x in r["columna_pendiente"]), str(r["columna_pendiente"])[:200])
g, r = gs({"2025": ent("(9.200)", -9.2, fila_=F_ROU6, pagina=8, escala="miles")})
paso("ESC · ronda 2, R2b: la misma página declarada «miles» no se rechaza (PENDIENTE; antes DATOS INVÁLIDOS)",
     libre(g) and not r["invalidas"], str(r)[:200])
paso("ESC · ronda 2, detalle menor: con la escala pendiente el año no cuenta también como columna comprobada (0 comprobadas, aunque se alinea)",
     r["columna_comprobada"] == 0 and "comprobada en 0 años" in g["detalle"], g["detalle"][:200])
g, _ = gs({"2025": ent("(8.660)", -8.66, fila_=F_ROU6, pagina=8, escala="miles")})
paso("ESC · ronda 2: con la escala pendiente la columna se sigue examinando: la cifra de 2024 declarada en 2025 → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "columna de ['2024']"), g["detalle"][:200])
EP2 = getattr(M, "_escala_de_tabla", lambda *a: None)
paso("ESC · ronda 2: la escala se busca en el bloque de la tabla (de la fila hacia arriba, hasta dos líneas en blanco), no en toda la página",
     EP2("(in millions)\nRight-of-use depreciation   (3)\n\nFees (in thousands)", "(3)", "Right-of-use depreciation") == {"millones"}
     and EP2("(in thousands)\n\n\nRight-of-use depreciation   (3)", "(3)", "Right-of-use depreciation") == set()
     and EP2("(amounts in Euro)\n\nGroup\n\nDepreciation\n- Additions   (8.503.619)", "(8.503.619)", "- Additions") == {"unidades"})

# (revisión, hallazgo A) marcas que no son la celda del ejercicio
g, _ = gs({"2024": ent("-", 0, sg=1, fila_="Lease payable", pagina=6)}, nombre="da_ppa")
paso("CI · revisión A1 (S3): el guion de la etiqueta «Lease payable - principal», alineado con «Year ended 2024», no es un cero → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"), g["detalle"][:200])
g, _ = gs({"2024": ent("-", 0, sg=1, fila_="Amortisation of other intangibles", pagina=6)}, nombre="da_ppa")
paso("CI · revisión A2 (S4): «- 7» (negativo con espacio) no es un cero de 2024 → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"))
g, _ = gs({"2025": ent("-", 0, sg=1, fila_="Amortisation of other intangibles", pagina=6)}, nombre="da_ppa")
paso("CI · revisión A2 (S4b): «- 5» tampoco es un cero de 2025 → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"))
g, r = gs({"2023": ent("—", 0, sg=1, fila_="Amortisation of other intangibles", pagina=6)}, nombre="da_ppa")
paso("CI · revisión A (S10): en esa misma fila el «—» de 2023 sí es un cero → no salta, columna comprobada", libre(g) and r["columna_comprobada"] == 1,
     g["detalle"][:160])
# caso US: con la capa de f1/usgaap (SERIES_US y el parámetro «series»), la misma línea de Zoetis en una serie propia de US GAAP
import inspect  # noqa: E402
US = "pagos_arr_financiero_principal"
if "series" in inspect.signature(M._guarda_fuentes_series).parameters and US in getattr(M, "SERIES_US", ()):
    def gs_us(serie):
        d = {"series": {US: serie}, "fuentes_series": copy.deepcopy(FS)}
        G, res = M.Guardas(), {}
        M._guarda_fuentes_series(G, d, CT, ANIOS, res, series=(US,))
        return [x for x in G.lista if x["id"] == "F1-SERIES"][0], res["F1_SERIES"]
    capa = "US GAAP, " + US
else:
    def gs_us(serie):
        return gs(serie, nombre="da_ppa")
    capa = "NIIF, da_ppa (sin la capa de US GAAP en este árbol)"
F_Z = "Financing cash flows"
g, _ = gs_us({"2024": ent("–", 0, sg=1, fila_=F_Z, pagina=6)})
paso(f"CI · caso US ({capa}): «Financing cash flows – finance leases 2 1 —»: el «–» de la etiqueta no es el cero de 2024 → DATOS INVÁLIDOS",
     bloquea(g, "DATOS INVÁLIDOS", "no contiene el cero impreso"), g["detalle"][:200])
g, r = gs_us({"2023": ent("—", 0, sg=1, fila_=F_Z, pagina=6)})
paso(f"CI · caso US ({capa}): el «—» de 2023 de esa fila sí es un cero → no salta, columna comprobada", libre(g) and r["columna_comprobada"] == 1,
     g["detalle"][:200])
g, _ = gs_us({"2025": ent("2", 2, sg=1, fila_=F_Z, pagina=6, escala="miles")})
paso(f"CI · caso US ({capa}): «2» con escala «miles» en una nota «(in millions)» → DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "declara ['millones']"))

# ================================================================== VIS · el cero comprobado se ve como PENDIENTE (revisión, punto 3)
g, r = gs({"2025": cero(), "2024": cero(motivo="otro motivo declarado")}, nombre="da_ppa")
a = aviso_cero()
paso("VIS · cero_comprobado: aviso propio F1-SERIES-CERO (AVISO, PENDIENTE) con los dos años, su motivo y su cita; F1-SERIES no salta",
     libre(g) and a is not None and a["salta"] and a["severidad"] == "AVISO" and a["efecto"] == "PENDIENTE" and "PENDIENTE DE REVISOR" in a["detalle"]
     and "series.da_ppa.2024" in a["detalle"] and "series.da_ppa.2025" in a["detalle"] and "otro motivo declarado" in a["detalle"]
     and "The Group has no intangible" in a["detalle"], (a or {}).get("detalle", "")[:200])
rr = {"aplica": True, "guardas": [dict(x) for x in ULTIMA], "version": "prueba"}
gs({"2025": ent("—", 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("VIS · un cero impreso comprobado en su columna no crea el aviso de cero comprobado", aviso_cero() is None)
gs({"2025": cero(cita="")}, nombre="da_ppa")
paso("VIS · un cero comprobado que bloquea (sin cita) no crea el aviso: lo dice F1-SERIES", aviso_cero() is None)
md = M.informe_md(rr)
paso("VIS · motor_a_f1_resultado.md: la tabla de guardas lleva F1-SERIES-CERO con «PENDIENTE DE REVISOR»",
     "| F1-SERIES-CERO | sí | AVISO | PENDIENTE |" in md and "PENDIENTE DE REVISOR" in md)
import ficha as FI  # noqa: E402
src = inspect.getsource(FI)
paso("VIS · ficha: los avisos del bloque motor_a_f1 son las guardas que saltan con severidad AVISO o INFORMA (F1-SERIES-CERO entra)",
     '"avisos": [{"id": g.get("id"), "severidad": g.get("severidad"), "detalle": g.get("detalle")} for g in f1r.get("guardas") or []' in src
     and 'g.get("severidad") in ("AVISO", "INFORMA")' in src)

# ================================================================== LS · leer_serie (V-F1e)
s, p = M.leer_serie({"series": {"da_rou": {"2025": ent("(9.199.774)", -9.199774, escala="unidades")}}}, "da_rou", ANIOS)
paso("LS · leer_serie: con escala válida la magnitud del modelo es signo × valor_fuente (9,199774 millones)", s == {2025: Fr(9199774, 10 ** 6)} and not p)
s, p = M.leer_serie({"series": {"da_rou": {"2025": ent("(9.199.774)", -9.199774, escala="euros")}}}, "da_rou", ANIOS)
paso("LS · leer_serie: escala no válida → problema (V-F1e, DATOS INVÁLIDOS) y el año no entra", s == {} and any("no válida" in x for x in p))
s, p = M.leer_serie({"series": {"da_ppa": {"2025": cero()}}}, "da_ppa", ANIOS)
paso("LS · leer_serie: cero_comprobado entra como 0 (con valor_fuente 0 declarado)", s == {2025: 0} and not p)
d_ls = {"series": {"da_rou": {"2025": ent("(9.199.774)", -9.199774, escala="unidades")}, "pagos_arrendamiento": {"2025": ent("(10)", -10, escala="mil")}}}
s, p = M.leer_serie(d_ls, "pagos_arrendamiento", ANIOS)
paso("LS · leer_serie: la escala se valida también en pagos_arrendamiento", s == {} and any("no válida" in x for x in p))

# ================================================================== ANT · lo que bloqueaba antes sigue bloqueando
g, _ = gs({"2025": ent(None, 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("ANT · un cero sin «literal» ni «cero_comprobado» sigue INCOMPLETO", bloquea(g, "INCOMPLETO", "sin «literal»"))
g, _ = gs({"2025": ent("0", 0, sg=1, fila_=F_PPA)}, nombre="da_ppa")
paso("ANT · «0» que no está impreso en la página sigue DATOS INVÁLIDOS", bloquea(g, "DATOS INVÁLIDOS", "como cifra completa"))
g, _ = gs({"2025": ent("(9.199.774)", -9.199774, escala="unidades")}, carpeta=None)
paso("ANT · sin la carpeta del expediente las fuentes no se examinan → INCOMPLETO", bloquea(g, "INCOMPLETO", "no examinada"))
g, _ = gs({"2025": cero()}, nombre="da_ppa", carpeta=None)
paso("ANT · un cero comprobado sin carpeta tampoco se acepta → INCOMPLETO", bloquea(g, "INCOMPLETO", "no examinada"))
G0 = M.Guardas()
G0.add("OTRA", True, "BLOQUEA", "INCOMPLETO", "otra guarda", "(1a)")
M._guarda_fuentes_series(G0, {"series": {"da_ppa": {"2025": cero(cita="")}}, "fuentes_series": FS}, CT, ANIOS, {})
paso("ANT · si otra guarda ya bloquea, F1-SERIES avisa (no cambia el estado)",
     any(x["id"] == "F1-SERIES" and x["salta"] and x["severidad"] == "AVISO" for x in G0.lista))

shutil.rmtree(CT, ignore_errors=True)
n_ok = sum(ok for _, ok in R)
print(f"\n{n_ok}/{len(R)} pruebas de F1-SERIES con escala y ceros PASAN")
sys.exit(0 if n_ok == len(R) else 1)
