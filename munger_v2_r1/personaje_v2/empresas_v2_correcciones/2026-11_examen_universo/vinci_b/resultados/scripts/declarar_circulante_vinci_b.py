#!/usr/bin/env python3
"""vinci_b · añade a Vinci/motor_a_f1.json (la copia conservada por cambiar_base.py) SOLO el bloque `normalizacion_circulante` de la receta del
autor (rama f1/circulante-normalizado, f1_circulante/resultados/ensayo_vinci_b/normalizacion_circulante_vinci_b.json; F1_CIRCULANTE.md §7 paso 3).
Decisiones de la persona V-CIRC (a) y V-ANCLA (a), 19-nov-2026 (DECISIONES_PARA_EL_USUARIO.md:134–135). Nada más cambia en la declaración (se
comprueba), en particular no se declara `justificacion_reinversion_negativa`. Rastro en RASTRO.json.
Uso: python3 -I declarar_circulante_vinci_b.py MOTOR_A_F1.json BLOQUE.json RASTRO.json"""
import copy, hashlib, json, sys
M, B, R = sys.argv[1:4]
h = lambda p: hashlib.sha256(open(p, "rb").read()).hexdigest()  # noqa: E731
antes = h(M)
d = json.load(open(M, encoding="utf-8"))
assert "normalizacion_circulante" not in d and "justificacion_reinversion_negativa" not in d
bloque = json.load(open(B, encoding="utf-8"))["normalizacion_circulante"]
assert bloque["regla"] == "circulante_a_cero" and bloque["anios"] == [2021, 2022, 2023, 2024, 2025]
viejo = copy.deepcopy(d)
d["normalizacion_circulante"] = bloque
assert {k: v for k, v in d.items() if k != "normalizacion_circulante"} == viejo
open(M, "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1) + "\n")
json.dump({"fecha": "2026-11-20", "autor": "Claude orquestación", "archivo": "Vinci/motor_a_f1.json", "sha256_antes": antes, "sha256_despues": h(M),
           "bloque_de": "f1/circulante-normalizado: munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/f1_circulante/"
                        "resultados/ensayo_vinci_b/normalizacion_circulante_vinci_b.json (sha256 " + h(B) + ")",
           "normalizacion_circulante": bloque, "nada_mas_cambia": True},
          open(R, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(antes, "→", h(M))
