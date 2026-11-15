#!/usr/bin/env python3
"""Dominios de las estructuras de P-M1 de Viscofan con cada perímetro de la inversión (encargo 4.13 §7: «los dominios de las estructuras
pertinentes»; «no se trasladará una cota numérica de la base antigua a otra base»). Solo lee los libros recalculados de las variantes
del expediente viscofan/Viscofan (paso 10).

Por perímetro (activa = NIIF 16; perimetro_alternativo = Caja), con las bases de cada libro:
  - Λ: λ máximo con f definida en SR1/SR2 (Rh < D_hist ⇒ λ < 1 + D_hist ÷ A) y con f_fija > 0 en SRF (Rh < F_hist ⇒ λ < 1 + F_hist ÷ A),
    donde A es la amortización que se repone (B63) y Rh = (λ − 1) × A;
  - Θ: f y f_fija en θ = 0, 0,5 y 1 (Rh = θ × exceso);
  - inversión fija para crecer negativa: S2C × f > 1 ÷ NWC; f a partir del cual ocurriría con el S2C del BUENO.
La familia Λ no está declarada en la configuración (λ no se observa): sus cotas se dan como dominio, no como alternativa calculada.
Uso (desde munger_v2_r1/): python3 -I …/scripts/dominios_perimetro_viscofan.py · Escribe viscofan/resultados/dominios_perimetro.json y .md.
"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
E413 = os.path.dirname(AQUI)
C = os.path.join(E413, "viscofan", "Viscofan")


def main():
    from openpyxl import load_workbook
    pal = json.load(open(os.path.join(C, "resultados.json"), encoding="utf-8"))["palancas"]
    s2c = {"MALO": pal["B16"], "NORMAL": pal["C16"], "BUENO": pal["D16"]}
    out = {}
    for nombre, var in (("NIIF 16", "activa"), ("Caja", "perimetro_alternativo")):
        ws = load_workbook(os.path.join(C, "variantes_v64", "recalc", f"{var}.xlsx"), data_only=True, read_only=True)["Configuración V6.4"]
        b = {k: ws[f"B{r}"].value for k, r in (("D_hist", 57), ("exceso", 60), ("F_hist", 62), ("A", 63), ("nwc", 83), ("perimetro", 154))}
        assert b["perimetro"] == nombre
        theta = {}
        for t in (0.0, 0.5, 1.0):
            rh = t * b["exceso"]
            theta[t] = {"Rh": rh, "f_SR1_SR2": b["D_hist"] / (b["D_hist"] - rh), "f_fija_SRF": 1 - rh / b["F_hist"]}
        f_neg = (1 / b["nwc"]) / s2c["BUENO"]
        out[nombre] = {"bases": b, "lambda_max_f_definida_SR1_SR2": 1 + b["D_hist"] / b["A"], "lambda_max_SRF": 1 + b["F_hist"] / b["A"], "theta": theta,
                       "uno_entre_nwc": 1 / b["nwc"], "f_umbral_inversion_fija_negativa_BUENO": f_neg,
                       "f_maximo_en_theta": theta[1.0]["f_SR1_SR2"], "inversion_fija_negativa_en_theta_0_1": theta[1.0]["f_SR1_SR2"] * s2c["BUENO"] > 1 / b["nwc"]}
    json.dump(out, open(os.path.join(E413, "viscofan", "resultados", "dominios_perimetro.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    g = lambda x, n=4: f"{x:.{n}f}".replace(".", ",")  # noqa: E731
    md = ["# Viscofan · dominios de las estructuras de P-M1 con cada perímetro (encargo 4.13 §7)", "",
          "**Qué es.** Cotas calculadas con las bases de cada libro recalculado: la activa es NIIF 16 y la variante `perimetro_alternativo` es Caja. "
          "Son hechos de la especificación con estas bases. La cota de la 4.12 (λ ≤ 1,1413 para SRF) era de la base Caja y no se traslada a la de NIIF 16.", "",
          "| | NIIF 16 | Caja |", "|---|---|---|"]
    n, c = out["NIIF 16"], out["Caja"]
    filas = [("D_hist (B57)", n["bases"]["D_hist"], c["bases"]["D_hist"], 3), ("Exceso histórico (B60)", n["bases"]["exceso"], c["bases"]["exceso"], 3),
             ("F_hist (B62)", n["bases"]["F_hist"], c["bases"]["F_hist"], 3), ("Amortización que se repone A (B63)", n["bases"]["A"], c["bases"]["A"], 3),
             ("Λ · λ máximo con f definida (SR1, SR2)", n["lambda_max_f_definida_SR1_SR2"], c["lambda_max_f_definida_SR1_SR2"], 4),
             ("Λ · λ máximo con f_fija > 0 (SRF)", n["lambda_max_SRF"], c["lambda_max_SRF"], 4)]
    for t in (0.0, 0.5, 1.0):
        filas += [(f"Θ · θ = {g(t, 1)} · f (SR1, SR2)", n["theta"][t]["f_SR1_SR2"], c["theta"][t]["f_SR1_SR2"], 4),
                  (f"Θ · θ = {g(t, 1)} · f_fija (SRF)", n["theta"][t]["f_fija_SRF"], c["theta"][t]["f_fija_SRF"], 4)]
    filas += [("1 ÷ NWC", n["uno_entre_nwc"], c["uno_entre_nwc"], 4),
              ("f a partir del cual la inversión fija para crecer sería negativa en el BUENO (S2C 1,4)", n["f_umbral_inversion_fija_negativa_BUENO"], c["f_umbral_inversion_fija_negativa_BUENO"], 4)]
    md += [f"| {a} | {g(x, d)} | {g(y, d)} |" for a, x, y, d in filas]
    md += ["", f"**Lectura.** Con Θ, las tres estructuras que reestiman están definidas en todo θ ∈ [0, 1] con los dos perímetros. El f máximo es "
               f"{g(n['f_maximo_en_theta'])} (NIIF 16) y {g(c['f_maximo_en_theta'])} (Caja), por debajo del umbral de la inversión fija negativa "
               f"({g(n['f_umbral_inversion_fija_negativa_BUENO'])}). Ninguna variante calculada sale del dominio: no hay avisos activos en `configuracion_v64_variantes.md`. "
               "Con Λ, que no está declarada, NIIF 16 amplía el dominio de SRF hasta "
               f"λ ≈ {g(n['lambda_max_SRF'], 3)}. Ninguna cota se recorta para obtener un valor."]
    open(os.path.join(E413, "viscofan", "resultados", "dominios_perimetro.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))


if __name__ == "__main__":
    main()
