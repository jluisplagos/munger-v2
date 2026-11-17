#!/usr/bin/env python3
"""Extrae de la conciliación F1 de Elis (rama auditoria/economica-f1-frente-e @ 9cad78d, SOLO LECTURA) las cifras que la declaración F1
necesita y no están en el libro: D&A de derechos de uso, PPA, pagos de arrendamientos, BAI, gasto por impuesto, ajustes de earnout de la
nota 4.6 y la actualización financiera del earnout de México. Solo toma filas con estado OK en `resultados/verificacion_cifras.json` y
con la edición vigente; guarda documento, página, literal y el id de la fila. Guarda también la referencia de E9 (`contraste_f1.json →
referencia_especificacion`) y las cifras de T16 (`copia_investigacion_f1.json`) para las pruebas, con las huellas de los archivos de origen.

Uso: python3 -I datos_elis_f1.py RAIZ_FRENTE_E SALIDA.json
"""
import csv
import hashlib
import json
import os
import sys

IDS = {
    "da_rou": {2021: "DA_ROU_U22_2021", 2022: "DA_ROU_U23_2022", 2023: "DA_ROU_FR_2023", 2024: "DA_ROU_2024", 2025: "DA_ROU_2025"},
    "da_ppa": {2021: "DA_PPA_U22_2021", 2022: "DA_PPA_U23_2022", 2023: "DA_PPA_FR_2023", 2024: "DA_PPA_2024", 2025: "DA_PPA_2025"},
    "pagos_arrendamiento": {2023: "CF_LEASE_FR_2023", 2024: "CF_LEASE_2024", 2025: "CF_LEASE_2025"},
    "bai": {2021: "IS_BAI_U22_2021", 2022: "IS_BAI_U23_2022", 2023: "IS_BAI_FR_2023", 2024: "IS_BAI_2024", 2025: "IS_BAI_2025"},
    "gasto_impuesto": {2021: "IS_IMP_U22_2021", 2022: "IS_IMP_U23_2022", 2023: "IS_IMP_FR_2023", 2024: "IS_IMP_2024", 2025: "IS_IMP_2025"},
    "ajuste_earnout": {2021: "OOIE_EARN_U22_2021", 2022: "OOIE_EARN_U23_2022", 2023: "OOIE_EARN_FR_2023", 2024: "OOIE_EARN_2024", 2025: "OOIE_EARN_2025"},
    "actualizacion_earnout": {2023: "FIN_ACTMEX_FR_2023", 2024: "FIN_ACTMEX_2024", 2025: "FIN_ACTMEX_2025"},
    "vnc_relaciones_clientes": {2025: "INT_RC_VNC_2025"},
}


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def main():
    raiz, salida = sys.argv[1], sys.argv[2]
    p_csv = os.path.join(raiz, "datos", "cifras_fuente.csv")
    p_ver = os.path.join(raiz, "resultados", "verificacion_cifras.json")
    p_con = os.path.join(raiz, "resultados", "contraste_f1.json")
    p_inv = os.path.join(raiz, "resultados", "copia_investigacion_f1.json")
    filas = {r["id"]: r for r in csv.DictReader(open(p_csv, encoding="utf-8"), delimiter=";")}
    ver = json.load(open(p_ver, encoding="utf-8"))
    if ver["huellas"]["datos"] != sha(p_csv):
        sys.exit("la verificación no es la de este CSV")
    estado = {c["id"]: c["estado"] for c in ver["cifras"]}
    out = {"origen": {"rama": "auditoria/economica-f1-frente-e", "commit": "9cad78d",
                      "archivos": {os.path.relpath(p, raiz): sha(p) for p in (p_csv, p_ver, p_con, p_inv)}},
           "nota": "cifras publicadas verificadas por el frente E (estado OK, edición vigente); no son entradas registradas del libro", "series": {}}
    for serie, ids in IDS.items():
        out["series"][serie] = {}
        for y, i in ids.items():
            r = filas[i]
            if estado.get(i) != "OK" or r["edicion"] != "vigente":
                sys.exit(f"{i}: estado {estado.get(i)} edición {r['edicion']}: no se usa")
            out["series"][serie][str(y)] = {"id_fila": i, "documento": r["doc"], "pagina": int(r["pagina"]), "literal": r["literal"],
                                            "valor_publicado": float(r["valor_publicado"]), "etiqueta": r["etiqueta"]}
    con = json.load(open(p_con, encoding="utf-8"))["referencia_especificacion"]
    inv = json.load(open(p_inv, encoding="utf-8"))
    out["referencia_E9"] = con
    out["referencia_T16"] = {"N1": inv["P3_normalizacion"]["escenarios"]["N1 · ajustes de earnout 2023–25, no deducibles"],
                             "V3_V4": inv["V3_V4_de_que_depende_N1"]["escenarios"], "P2": inv["P2_PPA_constante"], "P4": inv["P4_arrendamientos"]}
    json.dump(out, open(salida, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"OK: {salida}")


if __name__ == "__main__":
    main()
