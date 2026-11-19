"""Expediente sintético tipo VINCI para las pruebas de la normalización del circulante (V-CIRC; revisión C1 del 19-nov-2026).

Escribe en una carpeta lo que F1-CIRC lee del expediente para demostrar que la caja base excluye el circulante:
  - fase1_v63.json: la Historia de cfo y circulante (las filas 11 y 14 del libro) y el cálculo declarado de C46, como el de vinci/Vinci: la media
    de la ventana (2023–2025) de cfo + circulante + dividendos de sociedades no consolidadas (31 / 41 / 40), con su fuente, su página y su cita;
  - texto/informe_tipo_vinci.txt: el texto conservado, con marcas «[PDF PAGE n]». Lleva las citas de esos componentes y otras líneas que usan las
    pruebas de los cálculos amañados: la línea del circulante del estado de flujos, dos líneas que la reparten y una línea «2090».
Son datos de prueba: no se lee ningún expediente ni ningún informe publicado. Lo usan pruebas/test_circulante_f1.py, la prueba «circ» de
v6/v632_f1/scripts/probar_v632_f1.py y sus mutaciones.
"""
import copy
import json
import os

TEXTO = "texto/informe_tipo_vinci.txt"
PAGINAS = [
    "Informe sintético tipo VINCI (datos de prueba; no es un documento publicado)",
    "Note 3.1 Other financial investments\nOther 41 31",
    "Note 3.1 Other financial investments\nDividends received from unconsolidated companies 40 41",
    "Consolidated cash flow statement\nChanges in operating working capital requirement and current provisions 2311 1463",
    "Consolidated cash flow statement\nChanges in operating working capital requirement and current provisions 2496 2311",
    "Note 5 Working capital\nChange in trade receivables 1311 1000\nChange in current provisions 1000 463",
    "Note 5 Working capital\nChange in trade receivables 1496 1311\nChange in current provisions 1000 1000",
    "Other operating cash items 2090 2090",
]
VENTANA = [2023, 2024, 2025]
DIVIDENDOS = {"2023": {"valor": 31, "fuente": TEXTO, "pagina": 2, "cita": "Other 41 31"},
              "2024": {"valor": 41, "fuente": TEXTO, "pagina": 3, "cita": "Dividends received from unconsolidated companies 40 41"},
              "2025": {"valor": 40, "fuente": TEXTO, "pagina": 3, "cita": "Dividends received from unconsolidated companies 40 41"}}
CALCULO = {"operacion": "media", "anios": list(VENTANA), "redondeo": 3,
           "terminos": [{"partida": "cfo", "signo": 1}, {"partida": "circulante", "signo": 1},
                        {"componente": "dividendos_sociedades_no_consolidadas", "signo": 1}],
           "componentes": {"dividendos_sociedades_no_consolidadas": DIVIDENDOS},
           "decision": "prueba: C46 = CFO + circulante (fila 14) + dividendos de sociedades no consolidadas, como Control maestro M43 y P-O1 (c) en VINCI"}
# componentes con fuente verdadera en el texto de prueba que devuelven el circulante (pruebas de los cálculos amañados)
CIRCULANTE_DEL_ESTADO_DE_FLUJOS = {
    "2023": {"valor": 1463, "fuente": TEXTO, "pagina": 4, "cita": "Changes in operating working capital requirement and current provisions 2311 1463"},
    "2024": {"valor": 2311, "fuente": TEXTO, "pagina": 5, "cita": "Changes in operating working capital requirement and current provisions 2496 2311"},
    "2025": {"valor": 2496, "fuente": TEXTO, "pagina": 5, "cita": "Changes in operating working capital requirement and current provisions 2496 2311"}}
CLIENTES = {"2023": {"valor": 1000, "fuente": TEXTO, "pagina": 6, "cita": "Change in trade receivables 1311 1000"},
            "2024": {"valor": 1311, "fuente": TEXTO, "pagina": 6, "cita": "Change in trade receivables 1311 1000"},
            "2025": {"valor": 1496, "fuente": TEXTO, "pagina": 7, "cita": "Change in trade receivables 1496 1311"}}
PROVISIONES = {"2023": {"valor": 463, "fuente": TEXTO, "pagina": 6, "cita": "Change in current provisions 1000 463"},
               "2024": {"valor": 1000, "fuente": TEXTO, "pagina": 6, "cita": "Change in current provisions 1000 463"},
               "2025": {"valor": 1000, "fuente": TEXTO, "pagina": 7, "cita": "Change in current provisions 1000 1000"}}
OTROS_2090 = {str(y): {"valor": 2090, "fuente": TEXTO, "pagina": 8, "cita": "Other operating cash items 2090 2090"} for y in VENTANA}


def texto():
    return "".join(f"[PDF PAGE {i + 1}]\n{p}\n" for i, p in enumerate(PAGINAS)) + f"[PDF PAGE {len(PAGINAS) + 1}]\n"


def fase1(valores, anios=tuple(range(2016, 2026)), cols="CDEFGHIJKL"):
    """fase1_v63.json del expediente sintético a partir de los valores del libro (las filas 11 y 14) con el cálculo declarado de C46."""
    return {"_nota": "Expediente sintético tipo VINCI (datos de prueba de test_circulante_f1.py; no es un expediente)",
            "historia": {"anios": list(anios), "partidas": {"cfo": {"valores": [valores[f"Historia!{c}11"] for c in cols]},
                                                            "circulante": {"valores": [valores[f"Historia!{c}14"] for c in cols]}}},
            "anios_fcf_base": 3,
            "analisis": {"C46": {"periodo": "2023–2025", "unidad": "mm", "valor": 9327.333, "calculo": copy.deepcopy(CALCULO)}}}


def escribir(carpeta, valores=None, f1=None, con_texto=True):
    """Escribe el texto conservado y fase1_v63.json (el de `fase1(valores)` o el que se pase; None y sin valores: ninguno) en `carpeta`."""
    if con_texto:
        os.makedirs(os.path.join(carpeta, "texto"), exist_ok=True)
        with open(os.path.join(carpeta, TEXTO), "w", encoding="utf-8") as f:
            f.write(texto())
    if f1 is None and valores is not None:
        f1 = fase1(valores)
    if f1 is not None:
        with open(os.path.join(carpeta, "fase1_v63.json"), "w", encoding="utf-8") as f:
            json.dump(f1, f, ensure_ascii=False, indent=1)
    return carpeta
