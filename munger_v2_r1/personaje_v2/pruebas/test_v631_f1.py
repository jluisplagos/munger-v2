#!/usr/bin/env python3
"""Batería de la plantilla V6.3.1 F1 sin LibreOffice (F1-IMPL, recomendación (a)): selección explícita, aplicación de la declaración al libro
y oráculo de motor_a_f1.py frente a un libro V6.3.1. Lo que exige recálculo está en v6/v631_f1/scripts/probar_v631_f1.py (a0 y f1).

Uso (desde personaje_v2/): python3 -B pruebas/test_v631_f1.py
"""
import json
import os
import shutil
import sys
import tempfile
from fractions import Fraction as Fr

PV = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
RAIZ = os.path.dirname(PV)
sys.path.insert(0, os.path.join(PV, "scripts"))
sys.dont_write_bytecode = True
import config_v2  # noqa: E402
import seleccion_plantilla as SEL  # noqa: E402
import f1_libro_v631 as V631  # noqa: E402
import cierre_v2 as CIE  # noqa: E402

RES = []


def paso(nombre, ok, detalle=""):
    RES.append((nombre, bool(ok)))
    print(("PASA " if ok else "FALLA") + " · " + nombre + (f" · {detalle}" if detalle else ""))


CFG63 = config_v2.cargar(os.path.join(PV, "config_v2.json"))
CFG631 = config_v2.cargar(os.path.join(PV, "config_v2_v631_f1.json"))
CFG64 = config_v2.cargar(os.path.join(PV, "config_v2_v64_experimental.json"))

# ------------------------------------------------------------------------------------------------ configuración y selección
pl = CFG631["plantilla"]
paso("config_v2_v631_f1.json: plantilla V6.3.1 F1 con su referencia, verificador e inventario (scripts_v63)",
     SEL.version(CFG631) == SEL.V631 and SEL.es_v631(CFG631) and not SEL.es_v64(CFG631) and SEL.registra(CFG631)
     and pl["archivo"].endswith("Plantilla_V6.3.1_F1.xlsx") and pl["referencia"].endswith("referencia_V6.3.1_F1.json")
     and pl["verificador"].endswith("verificar_v631.py") and os.path.isfile(os.path.join(pl["scripts_v63"], "inventario_entradas.py"))
     and all(os.path.isfile(pl[k]) for k in ("archivo", "referencia", "verificador", "add_sliders")))
paso("config_v2.json sigue siendo la V6.3 y no registra selección; la V6.3.1 no es la de por defecto",
     SEL.version(CFG63) == "V6.3" and not SEL.registra(CFG63) and os.path.abspath(config_v2.POR_DEFECTO) == os.path.abspath(os.path.join(PV, "config_v2.json")))
c631, c63 = {k: v for k, v in CFG631.items() if k not in ("plantilla", "_nota", "_nota_resumen", "version_config", "resumen_csv_nombre", "_ruta_config")}, \
    {k: v for k, v in CFG63.items() if k not in ("plantilla", "_nota", "version_config", "_ruta_config")}
paso("config_v2_v631_f1.json es config_v2.json salvo la plantilla, la versión y el resumen", c631 == c63 and CFG631["version_config"].startswith(CFG63["version_config"]))
paso("resumen propio: resumen_v2_v631_f1.csv (cfg y plantilla_activa.json); la V6.3 sigue en resumen_v2.csv",
     CIE.nombre_resumen("/nonexistent", CFG631) == "resumen_v2_v631_f1.csv" and CIE.nombre_resumen("/nonexistent", CFG63) == "resumen_v2.csv")

tmp = tempfile.mkdtemp(prefix="v631_sel_")
try:
    def carpeta(nombre, archivos=()):
        c = os.path.join(tmp, nombre)
        os.makedirs(c)
        for a in archivos:
            open(os.path.join(c, a), "w").write("{}" if a.endswith(".json") else "x")
        return c
    c = carpeta("nuevo")
    paso("expediente nuevo con la V6.3.1: se acepta y registra plantilla_activa.json con sus huellas",
         SEL.comprobar(c, CFG631) is None and SEL.registrar(c, CFG631) and (SEL.leer(c) or {}).get("version") == SEL.V631
         and SEL.leer(c)["archivo_sha256"] == SEL.seleccion(CFG631)["archivo_sha256"])
    paso("ese expediente V6.3.1 no se ejecuta con la V6.3 (config_v2.json) ni con la V6.4", bool(SEL.comprobar(c, CFG63)) and bool(SEL.comprobar(c, CFG64)),
         str(SEL.comprobar(c, CFG63))[:120])
    paso("su nombre de resumen sin cfg (llamada a mano) es el de la V6.3.1", CIE.nombre_resumen(c) == "resumen_v2_v631_f1.csv")
    r_cfg, motivo, nota = SEL.resolver(c, CFG63)
    paso("resolver: una llamada a mano con config_v2.json sobre un expediente V6.3.1 resuelve la configuración registrada (V6.3.1)",
         motivo is None and SEL.es_v631(r_cfg), str(nota)[:120])
    c = carpeta("v63_previo", ["X_v63_datos.xlsx"])
    paso("expediente V6.3 ya empezado (libros V6.3, sin plantilla_activa.json): la V6.3.1 lo rechaza sin escribir nada",
         bool(SEL.comprobar(c, CFG631)) and not os.path.exists(os.path.join(c, SEL.ARCHIVO)))
    r_cfg, motivo, _ = SEL.resolver(c, CFG631)
    paso("resolver: la V6.3.1 cargada sobre un expediente V6.3 resuelve config_v2.json", motivo is None and SEL.version(r_cfg) == "V6.3")
    c = carpeta("con_conf", [SEL.CONF])
    paso("configuración económica con la V6.3.1: se rechaza (no se ignora)", "configuracion_economica.json" in str(SEL.comprobar(c, CFG631)))
    c = carpeta("v63_nuevo")
    paso("la V6.3 sobre un expediente nuevo sigue igual (sin registro)", SEL.comprobar(c, CFG63) is None and SEL.registrar(c, CFG63) is None
         and not os.path.exists(os.path.join(c, SEL.ARCHIVO)))
finally:
    shutil.rmtree(tmp, ignore_errors=True)

# ------------------------------------------------------------------------------------------------ aplicar la declaración al libro
ANIOS = list(range(2016, 2026))
REG = {"fecha": "2026-11-18", "persona": "prueba", "motivo": "prueba"}


def entrada(v, sg=1, trat="ninguno", doc="doc", pag=1):
    return {"valor_fuente": v, "signo": sg, "tratamiento": trat, "documento": doc, "pagina": pag}


decl = {"perimetro_reinversion": {"valor": "A1_sin_ROU", "registro": REG},
        "series": {"da_rou": {"2024": entrada(-10.5, -1, "cargo entre paréntesis"), "2025": entrada(11), "2023": entrada(5, -1, "ninguno"),
                              "2022": {"valor_fuente": 3, "signo": 1, "tratamiento": "ninguno", "documento": "", "pagina": 1}},
                   "da_ppa": {"2025": entrada(0)}}}
cel = V631.celdas(decl, ANIOS)
paso("celdas: perímetro A1 en C85, magnitudes signo × valor_fuente (2024: 10,5; 2025: 11), PPA 0 explícito en 2025",
     cel["Historia!C85"] == "A1_sin_ROU" and cel["Historia!K86"] == 10.5 and cel["Historia!L86"] == 11.0 and cel["Historia!L87"] == 0.0)
paso("celdas: una entrada inválida (signo −1 sin tratamiento; sin documento) queda VACÍA, no cero; lo no declarado también",
     cel["Historia!J86"] is None and cel["Historia!I86"] is None and cel["Historia!C86"] is None and cel["Historia!K87"] is None)
paso("celdas: escribe las tres filas enteras (20 importes + perímetro + 3 fuentes) para no dejar valores anteriores",
     len(cel) == 24 and all(f"Historia!{c}{f}" in cel for c in V631.COLS for f in (86, 87))
     and all(k in cel for k in ("Historia!C85", "Historia!M85", "Historia!M86", "Historia!M87")))
paso("celdas: A3_estimado o sin declarar → C85 vacío (= A0 en el libro; la capa bloquea)",
     V631.celdas(dict(decl, perimetro_reinversion={"valor": "A3_estimado"}), ANIOS)["Historia!C85"] is None and V631.celdas({}, ANIOS)["Historia!C85"] is None)

# ------------------------------------------------------------------------------------------------ oráculo (sin LibreOffice: L sintético)
col = dict(zip(ANIOS, V631.COLS))
L = {"Historia!A84": "  PERÍMETRO F1 DE LA REINVERSIÓN · motor A", "Historia!C89": "A1_sin_ROU", "Historia!C58": 0.05, "Historia!C53": 2.0}
for y in ANIOS:
    L[f"Historia!{col[y]}8"] = 100.0
    L[f"Historia!{col[y]}86"] = 40.0
    L[f"Historia!{col[y]}88"] = 60.0
rou = {y: Fr(40) for y in ANIOS}
dx = lambda y: Fr(60)  # noqa: E731
calc = {"f": Fr("0.05"), "ancla": Fr(2)}
paso("perimetro_del_libro: V6.3.1 → C89; libro V6.3 (sin la sección) → None", V631.perimetro_del_libro(L) == "A1_sin_ROU" and V631.perimetro_del_libro({}) is None)
paso("replica_dx: D_X = D&A − ROU en A1 → sin diferencias; con una D_X manipulada → la nombra",
     V631.replica_dx(L, ANIOS, col) == [] and V631.replica_dx(dict(L, **{"Historia!H88": 61.0}), ANIOS, col) != [])
paso("corresponde: todo igual → []", V631.corresponde(L, "A1_sin_ROU", rou, {}, ANIOS, col, dx, calc, []) == [])
casos = {"perímetro declarado distinto": V631.corresponde(L, "A2_propio", rou, {}, ANIOS, col, dx, calc, []),
         "serie distinta": V631.corresponde(L, "A1_sin_ROU", {**rou, 2024: Fr(41)}, {}, ANIOS, col, dx, calc, []),
         "serie vacía en la declaración": V631.corresponde(L, "A1_sin_ROU", {y: v for y, v in rou.items() if y != 2020}, {}, ANIOS, col, dx, calc, []),
         "PPA en el libro y no en la declaración": V631.corresponde(dict(L, **{"Historia!L87": 1.0}), "A1_sin_ROU", rou, {}, ANIOS, col, dx, calc, []),
         "f distinta (10⁻¹¹)": V631.corresponde(L, "A1_sin_ROU", rou, {}, ANIOS, col, dx, dict(calc, f=Fr("0.05") + Fr(1, 10 ** 11)), []),
         "ancla vacía en la capa": V631.corresponde(L, "A1_sin_ROU", rou, {}, ANIOS, col, dx, dict(calc, ancla=None), []),
         "flujos del Motor distintos": V631.corresponde(L, "A1_sin_ROU", rou, {}, ANIOS, col, dx, calc, ["Motor!AU7"]),
         "A3 declarado": V631.corresponde(L, "A3_estimado", rou, {}, ANIOS, col, dx, calc, []),
         "libro V6.3": V631.corresponde({}, "A1_sin_ROU", rou, {}, ANIOS, col, dx, calc, [])}
paso("corresponde: cada diferencia bloquea (perímetro, serie, vacío ≠ 0, PPA, f a 10⁻¹¹, ancla, flujos, A3, libro V6.3)",
     all(casos.values()), "; ".join(f"{k}: {len(v)}" for k, v in casos.items()))

# ------------------------------------------------------------------------------------------------ ficha
esq = json.load(open(os.path.join(PV, "esquema", "ficha.esquema.json"), encoding="utf-8"))
paso("ficha.esquema.json admite la versión de plantilla «V6.3.1 F1»", "V6.3.1 F1" in esq["properties"]["versiones"]["properties"]["plantilla"]["enum"])

n = sum(ok for _, ok in RES)
print(f"{n}/{len(RES)} pruebas V6.3.1 F1 (sin LibreOffice) PASAN" if n == len(RES) else f"{n}/{len(RES)} pruebas V6.3.1 F1 (sin LibreOffice): FALLAN {len(RES) - n}")
sys.exit(0 if n == len(RES) else 1)
