#!/usr/bin/env python3
"""ahold_f4 · relevo de extracción registrado (paso 5, extraccion_v63; relevo de extracción, no de juicio), pedido por la revisión independiente
(REVISION_AHOLD_F4.md @ 19c17a9, hallazgos 1 y 2) y el coordinador (19-nov-2026). Autor: «Claude orquestación».
Añade al PRINCIPIO de extracto_v63.md, que lee la fase A, un bloque «## 0.» con:
  (a) la tabla de vigencia «cifra de la etapa 1 → valor vigente → celda → fuente» de las cifras que citan los textos heredados de la sección 6 de
      datos_v63.md y etapa1/Ahold_respuesta.md (hipótesis, D3: esos textos no se tocan);
  (b) la evidencia al 3T 2026 de C25, C27 y C76 con su página, que está en la columna M del Control maestro y volcar_datos_v63.py no vuelca.
El resto del extracto no cambia (se comprueba). El anterior queda en antecedentes/revision_ahold_f4/; el rastro, en resultados/relevo_extraccion_ahold_f4.json.
Cada cifra del 3T se comprueba aquí en texto/ antes de escribirla.
Uso (desde la carpeta del expediente ahold_f4/): python3 -I resultados/scripts/relevo_extraccion_ahold_f4.py Ahold antecedentes resultados/relevo_extraccion_ahold_f4.json"""
import hashlib, json, os, re, shutil, sys
C, ANT, REG = sys.argv[1:4]
h = lambda x: hashlib.sha256(open(x, "rb").read()).hexdigest()  # noqa: E731
ex = os.path.join(C, "extracto_v63.md")
antes_sha = h(ex)
viejo = open(ex, encoding="utf-8").read()
assert viejo.startswith("## 1. Mercado y cuota"), viejo[:80]
copia = os.path.join(ANT, "revision_ahold_f4", "extracto_v63_antes_del_relevo.md")
assert not os.path.exists(copia)
shutil.copy2(ex, copia)
Q3, A25 = "AD_q3-2026-interim-report.txt", "AD_annual-report-2025.txt"
TX = {f: open(os.path.join(C, "texto", f), encoding="utf-8").read() for f in (Q3, A25)}


def pag(f, n):
    return " ".join(re.search(r"\[PDF PAGE %d\]\n(.*?)(?=\n\[PDF PAGE |\Z)" % n, TX[f], re.S).group(1).split())


for f, n, frase in ((Q3, 14, "Cash and cash equivalents 8 3,559 3,605"), (Q3, 14, "Equity attributable to common shareholders 7 14,375 14,195"),
                    (Q3, 21, "Restricted cash 36 58"), (Q3, 21, "€1,176 million"), (Q3, 24, "Gross debt 19,747 19,261 18,404"),
                    (Q3, 24, "Net debt 16,087 15,961 14,699"), (Q3, 24, "liabilities 4,321 3,625 3,301"), (Q3, 16, "Net cash from operating activities 1,531 1,397 4,030 4,288"),
                    (Q3, 16, "Purchase of non-current assets (669) (578) (1,898) (1,805)"), (Q3, 16, "Interest paid (18) (24) (196) (192)"),
                    (Q3, 16, "Repayment of lease liabilities (493) (477) (1,473) (1,461)"), (Q3, 16, "Changes in inventories 36 (9) (42) (258)"),
                    (Q3, 16, "Changes in receivables and other current assets 125 (93) 83 128"), (Q3, 16, "Changes in payables and other current liabilities (291) (150) (902) (550)"),
                    (Q3, 3, "Underlying operating margin1 4.1 % (0.1)pp (0.1)pp"), (Q3, 3, "Net sales 68,529 (0.5) % 1.9 %"), (Q3, 3, "Free cash flow1 747 (32.4) %"),
                    (Q3, 25, "Underlying operating income 946 933 2,748 2,740"), (Q3, 2, "free cash flow of around €2.1 billion (previously at least €2.3 billion)"),
                    (Q3, 12, "Operating income 4 976 902 2,736 2,643"), (Q3, 21, "865,173,863 (December 28, 2025: 886,877,259)"),
                    (A25, 42, "Underlying operating income 3,734 3,608"), (A25, 216, "Net cash from operating activities 6,989 6,224"),
                    (A25, 216, "Changes in inventories (158) (30)"), (A25, 216, "Changes in receivables and other current assets (91) (220)"),
                    (A25, 216, "Changes in payables and other current liabilities 558 143")):
    assert frase in pag(f, n), (f, n, frase)
A, B = f"[{Q3}, PDF p.", f"[{A25}, PDF p."
bloque = f"""## 0. Vigencia de cifras y evidencia al 3T 2026 (relevo de extracción registrado, ahold_f4, 19-nov-2026)
Bloque añadido por la orquestación (resultados/relevo_extraccion_ahold_f4.json), no por el extractor original; el resto del extracto no cambia. Los textos heredados de la etapa 1 (sección 6 de `datos_v63.md` y `etapa1/Ahold_respuesta.md`) son hipótesis (D3) y no se han tocado: citan cifras de octubre de 2026 (precio del 23-oct, informe del 2T, definición del FCF anterior a P-O1 c) que el expediente ya no usa. Antes de mantener o cambiar una celda heredada, contrasta su cifra con esta tabla. Los LTM son 12 meses (52 semanas) a 27-sep-2026: ejercicio 2025 + 39 semanas de 2026 − 39 semanas de 2025 (decisión A-Q3 de la persona responsable, 19-nov-2026). `etapa1/extracto.md`, que lista el prompt de la fase A, no existe en este expediente: los hechos están en este archivo y en `datos_v63.md`.

| Cifra citada en la etapa 1 (celdas heredadas que la citan) | Valor vigente | Celda | Fuente |
|---|---|---|---|
| Precio 33,14 € (cierre del 23-oct-2026; C13, C20, C98, B101, B102, C104 y respuesta.md) | 36,05 € (cierre del 13-nov-2026) | Análisis!C37 | [fuentes_mercado/Euronext_AD_NL0011794037_XAMS_historico_NO_AJUSTADO_2026-01-02_a_2026-11-17.txt, PDF p. 1] |
| Capitalización 28.626 mm (33,14 € × 863,79 M acciones; C13) | 31.971,9 mm (36,05 € × 886,877259 M acciones en circulación a 28-dic-2025, P-O2 a; con las 865,173863 M a 27-sep-2026 serían 31.189,5) | Análisis!C41 y C55 | {A} 21] |
| Acciones 881 M (media diluida del 2T; respuesta.md) | 886,877259 M en circulación a 28-dic-2025 (P-O2 a); 865.173.863 a 27-sep-2026 tras recomprar 23.847.837 en 2026 | Análisis!C55 | {A} 21] |
| FCF LTM 1.821 mm (LTM a 28-jun-2026, sin la regla espejo; C13 y respuesta.md) | 2.150 mm (LTM a 27-sep-2026, con la regla espejo P-O1 c; sin ella, 1.853) | Análisis!C40 | {A} 16]; {B} 216] |
| P/FCF actual 15,7x (C13, C14, B101) | 14,9x (C41 31.971,9 ÷ C40 2.150); FCF yield 6,72 % | C41 ÷ C40 | ídem |
| P/FCF histórico mediano 14,7x (2019–2025; C13, B101) | 12,49x (misma mediana con la regla espejo): el precio actual queda POR ENCIMA de la mediana histórica, no por debajo | Análisis!C88 | AR2020–AR2025, estados de flujos (C88 en `datos_v63.md`) |
| EV/EBITDA 6,1x (C13) | 6,53x (balance a 27-sep-2026, EBITDA LTM 7.334; con las acciones a 27-sep-2026, 6,43x) | Análisis!C42 | {A} 12, 14, 16 y 24] |
| ROCE antes de impuestos 10,9 % (LTM a 28-jun-2026; C14, C93, C98, D68, B102, C103) | 10,7 % (3.635 ÷ 34.122, LTM y capital a 27-sep-2026) | Análisis!C24 | {A} 12, 14 y 24]; {B} 212] |
| ROIC después de impuestos LTM 9,2 % (C14, B102) | No recalculado. Medias 2021–2025 de la Historia: 8,78 % de todo el capital (Historia!C55) y 13,03 % del capital propio pagado todo el alquiler (sección 1 bis de `datos_v63.md`) | — | `datos_v63.md` §1 bis |
| FCF del accionista sin circulante 1.813 mm LTM (C20, C25, C67, B102) | 1.725 mm LTM (serie 1.136 / 2.149 / 2.041 / 2.059 / 1.911 en 2021–2025): ver abajo | evidencia de C25 | {A} 16]; {B} 216] |
| FCF de la empresa del 1S 2026: 302 frente a 715 (C25, B66, B102) | 39 semanas: 747 frente a 1.104 en 2025 | — | {A} 3 y 24] |
| Guía de FCF 2026 de al menos 2.300 (C25, C67, B102) | Rebajada el 4-nov-2026 a unos 2.100 (base de 53 semanas) | — | {A} 2 y 5] |
| Margen operativo subyacente del 2T 3,9 % (C19, C27, B66) y LTM 4,08 % (C66) | 3T 2026: 4,1 % (−0,1 pp a tipo constante); 39 semanas: 4,0 %; LTM 4,07 % | evidencia de C27 | {A} 3 y 25]; {B} 42] |
| Deuda neta ÷ EBITDA 2,2 veces (C20, B67) | 2,2073 (16.188 ÷ 7.334) | Análisis!C33 | {A} 12, 14, 16 y 24] |
| Caja 3.196 mm, deuda neta con arrendamientos 16.065 mm, cobertura de la deuda a corto 0,87 veces (C76) | Caja 3.559 mm, deuda neta 16.188 mm, cobertura 0,82 veces: ver abajo | Análisis!C53, C54 y C34; evidencia de C76 | {A} 14, 21 y 24] |
| FCF base 1.999,4 mm (media 2023–2025 con la definición anterior a P-O1 c; C11, C51 y respuesta.md) | 2.312 mm (C46 6.583,667 − C47 2.432,333 − C48 77 − C49 1.707,333 − C50 55) | Análisis!C52 | `datos_v63.md` §2 |
| Tasa sin riesgo 3,34 % (Trading Economics, cierre de octubre) | 3,37 % (Bundesbank, Bund a 10 años, 13-nov-2026) | Análisis!C57 | [fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt, PDF p. 1] |
| Valores por acción de la etapa 1 (escenario malo 23 €, ponderado 36,8 € o 33,7 €; C20, C56, C62, B69, B101, B102, C104) | Sin valor vigente: son resultados del libro de la etapa 1 con aquellas entradas; el libro actual no tiene escenarios hasta la fase B | — | — |

### Evidencia al 3T 2026 de C25, C27 y C76 (está en la columna M del Control maestro; `datos_v63.md` no la vuelca)
- (C25) FCF del accionista sin circulante, 12 meses a 27-sep-2026: 1.725 mm = FCF sin la regla espejo 1.853 (CFO 6.731 − capex 2.657 − intereses pagados 265 − pagos de arrendamientos 1.956) − variación favorable del circulante 128 (inventario, cobros y pagos: 309 en 2025 − 861 en 39 semanas de 2026 + 680 en 39 semanas de 2025). Misma definición que la serie de la etapa 1 (2025: 2.220 − 309 = 1.911). Con el 2T eran 1.813. {A} 16]; {B} 216]
- (C25) FCF de la empresa (su definición, que suma desinversiones y cobros) en 39 semanas: 747 frente a 1.104 en 2025; la empresa lo atribuye sobre todo al circulante, por calendario y estacionalidad. {A} 3, 10 y 24]
- (C27) Margen operativo subyacente, 12 meses a 27-sep-2026: 4,07 % = resultado operativo subyacente 3.742 (3.734 de 2025 + 2.748 − 2.740) ÷ ventas 92.019 (92.352 + 68.529 − 68.862). 3T 2026: 4,1 % (−0,1 pp a tipo constante); 39 semanas: 4,0 % (igual que en 2025). {B} 42]; {A} 3 y 25]
- (C76) Caja y equivalentes a 27-sep-2026: 3.559 mm, de los que 36 son caja restringida y 1.176 un cash pool nocional compensado por un importe igual en la deuda a corto. {A} 14 y 21]
- (C76) Deuda bruta con arrendamientos 19.747 mm; deuda neta con arrendamientos 16.188 mm (19.747 − 3.559); la de la empresa, que resta además depósitos a corto y el fondo de bonos, 16.087 mm. {A} 24]
- (C76) Deuda a corto (préstamos a corto y porción corriente de deuda y arrendamientos): 4.321 mm (3.301 a 28-dic-2025). Caja ÷ deuda a corto: 0,82 veces; sin el cash pool en los dos lados, 2.383 ÷ 3.145 = 0,76 veces; caja sin restringida ni cash pool ≈ 2.347 mm, menor que la deuda a corto sin el cash pool (3.145). {A} 14, 21 y 24]

"""
nuevo = bloque + viejo
open(ex, "w", encoding="utf-8").write(nuevo)
assert open(ex, encoding="utf-8").read().endswith(viejo)
json.dump({"fecha": "2026-11-19", "paso": "5 · extraccion_v63 (relevo de extracción, no de juicio), tras relanzar con --desde 1 por las correcciones de la revisión de ahold_f4",
           "autor": "orquestación (Claude, agente de implementación)", "guion": os.path.abspath(__file__),
           "revision": "munger-v2-evidencias-mistral, coordinacion/cierre_v2/examen/revisiones/expedientes_f1/REVISION_AHOLD_F4.md @ 19c17a9, hallazgos 1 y 2",
           "entrada_sha256": antes_sha, "salida_sha256": h(ex), "copia_anterior": os.path.relpath(copia, os.path.dirname(C)),
           "contenido": ("Bloque «## 0.» añadido al principio (tabla de vigencia de las cifras de la etapa 1 y evidencia al 3T de C25, C27 y C76, con página); las secciones "
                         "1–9 son idénticas a las del extracto consumido (se comprueba). Las cifras del 3T se comprobaron en texto/ antes de escribirlas."),
           "palabras_del_bloque": len(bloque.split())}, open(REG, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("palabras del bloque", len(bloque.split()), "· total", len(nuevo.split()))
