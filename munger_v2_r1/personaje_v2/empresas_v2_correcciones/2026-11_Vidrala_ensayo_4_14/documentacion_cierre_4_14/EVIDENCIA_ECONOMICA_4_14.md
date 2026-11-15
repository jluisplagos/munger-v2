# Evidencia económica · frente B · encargo de cierre (§6)

**Qué es.** La investigación de cuatro asuntos:
- (a) el fundamento de P-M1, es decir, el desglose del capex entre reposición y crecimiento;
- (b) las acciones y las fechas de Viscofan;
- (c) el perímetro de la inversión y los arrendamientos;
- (d) los documentos oficiales materiales que todavía no se conservan con sus bytes.

Separa los hechos (con su fuente), las interpretaciones y las propuestas. No adopta nada.

**Base y autoría.** Base 4.13 (ZIP SHA-256 `b1f747a1…f22a`), de solo lectura. Lo elaboró el agente del frente B (subagente de Claude) y es un trabajo **interno**. Fecha: 14-nov-2026. `E413/` abrevia `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_13/`, y `VT/` abrevia `E413/viscofan/Viscofan/texto/`.

**Acceso a la web.** La consola no tiene red. Las páginas se leyeron con la herramienta web, que devuelve texto, a veces resumido por un modelo, y nunca los bytes. Las citas web de este documento son las que devolvió la herramienta. **Ninguna fuente web se conserva con sus bytes ni con su huella.** Las citas de `VT/` y de los textos de Vidrala son literales de los textos conservados en el paquete; sus PDF están en `…_4_12/viscofan/fuentes/pdf/` y en el paquete de Vidrala.

**Accesos fallidos (declarados).**

| URL | Resultado |
|---|---|
| https://public.viscofan.com/investor-relations/financialinformation/en/Nota%20de%20resultados%202023_EN.pdf | robots_disallowed |
| https://public.viscofan.com/investor-relations/financialinformation/en/OIR_Nota%20de%20Resultados%204T21_DEF_EN.pdf | robots_disallowed |
| https://www.informeanual2021.viscofan.com/en/2021-results | robots_disallowed |
| https://ddd.uab.cat/pub/infanu/22449/iaVIDRALAa2024ispa.pdf | client_error |
| https://www.estrategiasdeinversion.com/…/viscofan-espera-alcanzar-1800-millones-de-euros-n-894213 | client_error |
| https://capital-riesgo.es/es/articles/viscofan-designa-a-kutxabank-investment-gestor-independiente-para-su-nuevo-programa-de-recompra-de-acciones/ | sin cuerpo, solo el título |
| https://www.sustainabilityreports.com/viscofan/2021/annual-report | resumen sin cifras |
| https://www.marketscreener.com/…/Viscofan-S-A-Group-releases-its-January-December-2021-results-39574499/ | total de 2021 sin desglose |

---

## (a) P-M1: desglose del capex entre reposición y crecimiento

### a.1 Viscofan: la empresa publica cada año un desglose por tipo (hecho)

El informe de gestión de Viscofan clasifica la inversión del año en cuatro tipos:
1. capacidad (y maquinaria);
2. mejoras de proceso y nueva tecnología;
3. sostenibilidad, energía y seguridad, higiene y medio ambiente (EHS);
4. inversiones ordinarias.

**Cinco de los seis años de 2016 a 2025 que se citan ya estaban en el paquete.** La fase C vigente (`E413/viscofan/Viscofan/fase_c.json`, `objetivo.informacion_no_disponible`) dice «solo consta 2025, AR_2025 p. 143», y no es exacto.

| Año | Inversión publicada (M€) | Capacidad | Proceso | Sostenibilidad / EHS | Ordinaria | Fuente y cita literal breve |
|---|---|---|---|---|---|---|
| 2016 | 86,7 | 51 % | 22 % | 8 % | 19 % | `VT/IA_2016_es.txt` l. 2971–2979: «El 51% de la inversión se destinó a inversiones de capacidad y maquinaria» |
| 2019 | 62,1 | 23 % | 41 % | 17 % | 19 % | `VT/AR_2019.txt` l. 10555–10562 (PDF p. 186): «Around 23% of investment (€14.3 million) was in capacity and machinery» |
| 2020 | 56,9 | 27 % | 20 % | 27 % | 26 % | `VT/AR_2020.txt` l. 11250–11258 (PDF p. 184): «27% of the investment was earmarked for investments in capacity and machinery» |
| 2021 | 92,0 | 44 % | 18 % | 18 % | 20 % | `VT/IA_2021_es.txt` l. 12473–12481 (PDF p. 213): «44% de la inversión se destinó a inversiones de capacidad y maquinaria» |
| 2022 | 125,6 | 40 % | 30 % | 16 % | 14 % | `VT/CF_2022_compilacion.txt` l. 8947–8954 (PDF p. 202): «40% of the investment was earmarked for investments in capacity and machinery» |
| 2023 | 77,5 | 16 % | 3 % | 26 % | 55 % | `VT/IA_2023_es.txt` l. 14212–14217 (PDF p. 250): «16% de la inversión se destinó a inversiones de capacidad y maquinaria … El 55% restante se destinó a inversiones ordinarias» |
| 2024 | 71,0 | 34 % | 14 % | 35 % | 17 % | **solo texto web:** https://www.informeanual2024.viscofan.com/en/financial-and-management-results.html (consultado el 14-nov-2026): «34% of the investment was earmarked for investments in capacity and machinery … The remaining 17% was spent on ordinary investments»; «Investment in 2024 amounted to €71.0 million (€77.5 million in 2023)» |
| 2025 | 84,1 | 37 % | 22 % | 27 % | 14 % | `VT/AR_2025.txt` l. 5948–5975 (p. 123 impresa, PDF 144): «€30.9 million (37%) corresponded to investments aimed at increasing capacity»; confirmado en https://www.informeanual2025.viscofan.com/en/economic-and-management-results.html |

**Contraste con el texto web de 2023** (https://www.informeanual2023.viscofan.com/informe-de-gestion/assets/downloads/2-5-2-economic-and-management-results.html_en.pdf, p. 5): devuelve los mismos porcentajes que `IA_2023_es.txt`, 16/3/26/55, y «A total of €77.5 million was invested in 2023». Coinciden.

**Planes estratégicos (texto web, sin bytes).**
- **Plan 2022–2025 («Beyond25»).** https://uk.marketscreener.com/quote/stock/VISCOFAN-S-A-75245/news/Viscofan-S-A-presents-its-Strategic-Plan-2022-2025-39582673/: «The accumulated investment in the period will reach 425 million euros». Sin desglose. La inversión publicada de 2022–2025 suma 125,6 + 77,5 + 71,0 + 84,1 = 358,2 M€ (aritmética).
- **Plan «Beat'30» (2026–2030).** Hay una discrepancia entre fuentes secundarias, y no se obtuvo la presentación oficial:
  - Alimarket, 27-feb-2026 (https://www.alimarket.es/alimentacion/noticia_amp/422330/…): «una inversión de más de 600 M distribuidos durante los próximos cinco años … de los cuales 300 M serán en proyectos de crecimiento»;
  - Invest in Navarra, 9-mar-2026 (https://investinnavarra.com/en/?p=26453), titular: «Viscofan to invest €600 million in growth until 2030».
- **Transcripciones.** No se buscaron las de Viscofan, por tiempo.

**Interpretación: qué miden y qué no miden estas categorías.**
- No son «mantenimiento frente a crecimiento». «Capacidad y maquinaria» (2016–2024) puede incluir maquinaria de reposición. Solo el texto de 2025 dice «aimed at increasing capacity».
- «Mejoras de proceso» es inversión de eficiencia, ni reposición pura ni volumen. EHS es inversión obligada para seguir operando, más cercana a la reposición que al crecimiento. «Ordinaria» es lo más parecido a la reposición recurrente.
- El total publicado no coincide con el capex de caja del modelo (por ejemplo, 2022: 125,6 frente a 115,566), y en la taxonomía de 2025 incluye los derechos de uso (ver c.1).

### a.2 Viscofan: método replicable para θ con ese desglose (propuesta)

**Definición del modelo.** P-M1 SR1 · Θ, con requisito = θ × exceso histórico medio y exceso = Σ (capex + altas de derechos de uso − D&A) en 2021–2025 = 64,923 M€ (NIIF 16). La reposición total de 2021–2025 es Σ D&A + θ × exceso. Por tanto:

> θ = (Σ M − Σ D&A) ÷ (Σ (capex + altas) − Σ D&A), donde M es la inversión de reposición del año.

**Estimación de M con el desglose.** Se aplican los porcentajes al capex del perímetro del modelo, capex de caja más altas (`E413/resultados/conciliacion_arrendamientos_viscofan.md` §2), con tres definiciones:
- **estrecha:** solo la ordinaria;
- **media:** ordinaria + EHS;
- **amplia:** todo lo que no es capacidad, es decir, ordinaria + EHS + proceso.

Script: `agentes/B/scripts/theta_desglose_viscofan.py` (solo aritmética). [cálculo B]

| Definición de M | Σ M 2021–2025 | Σ D&A | θ | Año a año: M frente a D&A |
|---|---|---|---|---|
| estrecha | 108,2 | 403,1 | −4,54 | M < D&A en los cinco años |
| media | 218,5 | 403,1 | −2,84 | M < D&A en los cinco años |
| amplia | 304,5 | 403,1 | **−1,52** | M < D&A en los cinco años (el más cercano, 2022: 70,3 frente a 78,1) |
| *(contraste)* amplia, aplicada al total publicado en lugar del capex del modelo | 291,8 | 403,1 | −2,37 | M < D&A en los cinco años |

La inversión de capacidad de 2021–2025 suma 163,6 M€ (el 35 % de la base), frente a un exceso de 64,9 M€.

**Lectura (interpretación).** Con la clasificación de la propia empresa, el exceso de la inversión sobre la amortización queda explicado por la inversión de capacidad. Lo que no es capacidad ni siquiera llega a la D&A. Con θ acotado en [0, 1] por la definición de la familia, el método da **θ = 0**, el extremo inferior: precio de Sí 41,8616 € (variante parametro_minimo = estructura_H = activa_sin_PM1).

**Supuestos y límites (declarados).**
1. **Etiqueta «capacidad y maquinaria».** Si toda la inversión de capacidad de 2021–2024 fuera reposición de maquinaria, M llegaría al total y θ a 1. El método no excluye ese extremo; lo hace improbable solo si se acepta que la empresa clasifica la capacidad como capacidad.

   Prueba de sensibilidad [cálculo B]: parte de la definición amplia (M = 304,5) y mide qué fracción de los 163,6 M€ declarados como capacidad habría que tratar como reposición para llegar a cada θ, con M = 403,1 + θ × 64,9.

   | θ | M necesaria (M€) | Capacidad que habría que reclasificar como reposición (M€) | Fracción de los 163,6 M€ de capacidad |
   |---|---|---|---|
   | 0 | 403,1 | 98,7 | 60 % |
   | 0,2 | 416,1 | 111,6 | 68 % |
   | 0,5 | 435,6 | 131,1 | 80 % |
   | 1 | 468,1 | 163,6 | 100 % |
2. **D&A a coste histórico.** La D&A incluye intangibles y derechos de uso; la reposición se mide en euros corrientes. Que M sea menor que la D&A puede significar una vida útil económica mayor que la contable, o una infrainversión temporal (θ < 0, fuera del dominio). El método no distingue entre las dos.
3. **Cinco años.** 2023 es atípico (55 % ordinaria), y 2024 solo está como texto web.
4. **Familia Λ.** El método no la contrasta; sigue «no determinada».
5. No es una medición del mantenimiento. Es una **delimitación** construida con la clasificación publicada.

**Alternativas del método.**
- **(i) Greenwald:** crecimiento = (activo fijo ÷ ventas) × Δventas, y reposición = capex − crecimiento. Necesita el inmovilizado material neto de cada año, que está en los PDF conservados, y separar precio y volumen; no se calculó.
- **(ii) Capacidad anunciada:** proyectos de capacidad con su importe, por ejemplo Cáseda, fibrosa, 14 M€ en 2021 (`VT/IA_2021_es.txt` l. 12465). Es parcial.
- **(iii) Amortización como reposición:** θ = 0 por construcción. Es lo que hace la estructura H o activa_sin_PM1.

**¿Permite delimitar la incertidumbre? (interpretación)**
- Para θ, sí, en este sentido: con la clasificación de la empresa, θ ≤ 0 (acotado a 0). Cualquier θ > 0 exige tratar como reposición más del 60 % de lo que la empresa declara como capacidad. θ = 0,5, el punto de cálculo actual, exige el 80 %, y θ = 1, el 100 % [cálculo B].
- Qué fracción es creíble es un juicio económico que corresponde a la persona responsable. El agente B no fija una banda.
- El punto de cálculo actual (θ = 0,5) no tiene apoyo en esta evidencia salvo que se rechace la clasificación publicada. No cambia la zona: todas las variantes están en «caro».
- La estructura (SR1, SR2, SRF, H o S) no se delimita con el desglose. Las estructuras calculadas dan de 39,54 a 42,10 € (`configuracion_v64_variantes.json`).

### a.3 Vidrala: no hay desglose publicado (hecho) y la delimitación no es defendible con lo disponible (interpretación)

**Lo que dicen las cuentas** (textos conservados en `E413/vidrala_condicionado/Vidrala/texto/`; cita literal de la nota del inmovilizado material):

| Año | Cita | Fuente |
|---|---|---|
| 2018 | «Main additions for 2018 correspond to the investment plans for the complete update of the production plants located in Italy (Euros 27,958 thousand) and the United Kingdom (Euros 33,733 thousand)…» | CF_2018.txt l. 1911 |
| 2019–2021 | «investment plans for the complete update of the production plants located in the United Kingdom … and Portugal …» (UK 44,247 / 77,801 / 32,597; Portugal 20,250 / 29,031 / 39,792 miles €) | CF_2019 l. 1861; CF_2020 l. 2549; CF_2021 l. 2328 |
| 2022 | «… United Kingdom (Euros 23,479 thousand …) and Portugal (Euros 94,557 thousand …)» | CF_2022.txt l. 2418 |
| 2023 | «The main additions in 2023 correspond to the investments made by the Group in its subsidiaries in Portugal» (más las altas por combinación de negocios) | CF_2023.txt l. 2355 |
| 2024–2025 | «investments made, primarily in the renewal of furnaces, by the Group in its subsidiaries in Spain, Portugal, and the United Kingdom» | CF_2024.txt l. 2560; CF_2025.txt l. 2499 |
| — | Vida útil: «Furnaces, installations and production machinery 8 - 16» años | CF_2025.txt l. 685 |
| — | Pruebas de deterioro: «Vidrala's production performance shows limited fluctuations at the expense of the recurring capex captured in the valuation models» (sin cifra) | CF_2019.txt l. 2082 (y siguientes ediciones) |

**Web (solo texto, sin bytes).**
- Transcripción de la presentación de resultados de 2024 (28-feb-2025; tercero: https://www.roic.ai/quote/VDRFF/transcripts/2024-year/4-quarter). El director financiero: «€168.8 million equivalent to 10.6% of sales»; para 2025, «something in the range of 11% of sales»; y «There is more than pure replacement in that CapEx» (sostenibilidad, verticalización y crecimiento de volumen, «basically Brazil»). Sin desglose.
- Glass Worldwide, sin fecha (https://glassworldwide.co.uk/industry-announcements/vidrala-investing-%E2%82%AC100-million-iberia): la reconstrucción de un horno de Gallo Vidro (Marinha Grande) aumenta la capacidad de la planta «by over 50%». Una reconstrucción puede ser a la vez reposición y crecimiento: es exactamente la mezcla que separa H de S, SR1 y SRF.

**Método replicable para λ (propuesta, sin calcular).** La familia Λ define la reposición a coste corriente como λ × la amortización que se repone.
- λ ≈ índice de precios de los bienes de equipo en t ÷ índice en t − L, con L la vida del activo que se repone (hornos, 8–16 años según la nota).
- Fuentes posibles: el índice de precios industriales de bienes de equipo (INE) o los precios de producción de bienes de capital de Eurostat. No se descargaron.
- Sustituye el rango 1,10–1,25 de la crítica de la 4.8 por una cifra con fuente.
- **Límites:** mide la inflación, no el cambio técnico (un horno nuevo puede ser más barato por tonelada) ni el cambio de capacidad en la reconstrucción.

**¿Permite delimitar? (interpretación)**
- λ, sí, con un índice y con L entre 8 y 16 años, condicionado a la estructura.
- La estructura no: Vidrala no publica qué parte de las reconstrucciones añade capacidad, y el director financiero dice que hay «more than pure replacement» sin cuantificarlo.
- Con lo disponible, el sistema **debe abstenerse del objetivo** de Vidrala para cualquier uso que no sea el ensayo (encargo §6; decisión D2). La acción («no comprar a 90,10 €») se sostiene en todo el rango calculado (51,29–65,72 €).
- Información que lo resolvería, y que solo puede pedir la persona responsable: el número de hornos, el calendario de reconstrucción, el coste y la capacidad antes y después (Q-E1–Q-E7 de la 4.8, no enviadas).

---

## (b) Acciones y fechas de Viscofan

| Hecho | Fuente | Cita o cifra |
|---|---|---|
| **La contradicción de la nota 20 está también en el formulario oficial de la CNMV** (segunda edición, en español) | CNMV, informe financiero del II semestre de 2025, nº de registro 2026030312, 26-feb-2026, «Informe estadístico», §IV.6, p. G-11: https://www.cnmv.es/webservices/verdocumento/ver?e=exhzoYHsIwQnuEcovmFg5W1qAN8WXDbTqoji8BsOjjT1xVx9TYwe6nqlQTLZolJy (página: https://www.cnmv.es/portal/aldia/detalleifialdia.aspx?nreg=2026030312) | «Básico 1290 1,97 1,94 3,50 3,45»; «Diluido 1295 1,98 1,93 3,52 3,44» (columnas: 2.º semestre de 2025, 2.º semestre de 2024, acumulado 2025, acumulado 2024) |
| Autocartera a 31-dic-2025 en euros (no en acciones) | misma, §IV.5, p. G-10 | «Menos: Acciones y participaciones en patrimonio propias 1174 (23.641) (35.045)» |
| Acciones entregadas en el dividendo flexible de 2025 | misma, §IV.10, p. G-17 | «Nº acciones a entregar» 1.693.734 (2025); 1.338.323 (2024) |
| Dividendo flexible de noviembre de 2025: aumento de hasta 1.328.571 acciones con reducción simultánea por amortización de propias; base de 46.500.000 acciones | BORME-C-2025-6267, 19-nov-2025: https://boe.es/borme/dias/2025/11/19/pdfs/BORME-C-2025-6267.pdf | «un máximo de 1.328.571 acciones ordinarias de 0,70 euros»; «46.500.000 acciones sin deducir las acciones en autocartera» |
| Reducción a 46.000.000 acciones (amortización de 500.000 propias; junta del 24-abr-2026; inscrita el 11-may-2026) | BORME-C-2026-738, BORME-C-2026-1603 (ya en la conciliación 4.13) | `E413/fuentes/CONCILIACION_ACCIONES_VISCOFAN_4_13.md` §2 |
| Junio de 2026: aumento liberado de 1.001.717 acciones con amortización simultánea; emitidas 46.000.000 | BORME-C-2026-3155 (ya en la conciliación 4.13) | ídem |
| Autocartera a 30-jun-2026: 396.357 | CNMV, I semestre de 2026, nº 2026107196, 29-jul-2026 (ya en la conciliación 4.13) | ídem |

**Interpretación.**
- La contradicción (BPA diluido de 3,52 frente al básico de 3,50, con el mismo numerador) aparece en **dos ediciones oficiales**: el informe anual en inglés y el formulario estadístico de la CNMV. No es solo una errata de traducción.
- En el semestre (H2 de 2025), el diluido también supera al básico (1,98 frente a 1,97), mientras que en el H2 de 2024 es menor (1,93 frente a 1,94), como corresponde a una dilución. El error, si lo es, afecta al cálculo de 2025, no a una sola cifra impresa.
- Con lo disponible no se resuelve. Refuerza la recomendación de no usar 45,479209 como divisor (decisión D3).

**No obtenido (declarado).**
- Una cifra oficial de autocartera entre el 30-jun-2026 y el 3-nov-2026.
- La versión española de la nota 20 de las cuentas consolidadas de 2025. La página de la CNMV ofrece el informe en XBRL (https://www.cnmv.es/Portal/consultas/wuc/descargaxbrlipp.ashx?t={de8c989d-4267-492f-a061-cebb676463c0}), que no se puede leer desde aquí.
- El cuerpo de la noticia sobre un «nuevo programa de recompra» con Kutxabank Investment (solo el titular, sin fecha). Si fuera posterior al 30-jun-2026, cambiaría la autocartera a la fecha del precio. Hay que comprobarlo en la CNMV («Otra información relevante» de Viscofan).
- Dos anuncios del BORME encontrados al buscar no son de Viscofan: BORME-C-2026-3702 (Miquel y Costas) y BORME-C-2026-4506 (Deugro).

---

## (c) Perímetro de la inversión y arrendamientos

### c.1 Viscofan (hecho)
- La conciliación 2021–2025 ya está en el paquete: altas 24,110 y amortización de derechos de uso 27,051, con 0 errores de lectura (`E413/resultados/conciliacion_arrendamientos_viscofan.md`).
- **Dato añadido.** Viscofan define su CapEx, en la taxonomía del informe de gestión de 2025, como «CapEx. Investments in intangible assets, property, plant and equipment and rights-of-use assets» (`VT/AR_2025.txt` l. 13495). La empresa mide su inversión con un perímetro que incluye los derechos de uso.
- Interpretación: apoya documentalmente el perímetro NIIF 16 (decisión D4), sin decidirlo.

### c.2 Vidrala: altas de derechos de uso (hecho; textos del paquete)

| Año | Altas orgánicas (miles €) | Otras | Amortización de derechos de uso | Saldo del activo a fin de año | Fuente |
|---|---|---|---|---|---|
| 2019 | n/d | — | n/d | 1.672 | CF_2019.txt l. 48 |
| 2020 | n/d | — | n/d | 1.303 | CF_2020.txt l. 50 |
| 2021 | **no publicadas por separado** | — | n/d | 770 | CF_2021.txt l. 38 (sin tabla de movimientos) |
| 2022 | 2.165 (activo); 2.133 (pasivo) | — | 633 | 2.302 | CF_2023.txt l. 2693–2725 (PDF p. 51–52) |
| 2023 | 645 (activo); 643 (pasivo) | **46.123 por combinación de negocios («The Park», Bristol)** | 4.624 | 44.446 | CF_2023.txt l. 2693–2751 |
| 2024 | 1.485 (activo); 1.429 (pasivo) | — | 4.768 | 43.075 | CF_2025.txt l. 2862–2900 (PDF p. 51) |
| 2025 | 2.404 | 9.595 («price update applied to the lease instalment for the "The Park" facilities») | 6.760 | 46.681 | CF_2025.txt l. 2862–2950 (PDF p. 51–52) |

**Discrepancias declaradas.**
- Las altas del activo y del pasivo no coinciden en 2022 (2.165 frente a 2.133) ni en 2024 (1.485 frente a 1.429).
- En la tabla del activo de 2025, la fila «Additions» de la amortización (1.415) más «Others» (5.345) suman la amortización de la cuenta de resultados (6.760).

**Interpretación.**
- En Vidrala, las altas orgánicas son pequeñas: 6,7 M€ en 2022–2025, sin 2021. La amortización de derechos de uso que ya lleva la D&A es mayor (16,8 M€ en 2022–2025), porque la domina el arrendamiento adquirido con The Park.
- Para el perímetro NIIF 16 de Vidrala hay que decidir si las altas por combinación de negocios cuentan como inversión de reposición, cosa que no se planteó en Viscofan. Lo coherente con el motor B sería tratarlas como adquisición, igual que las compras de negocios, y no como capex. Es una convención por decidir, y no está calculada.

---

## (d) Documentos oficiales materiales que no se conservan con sus bytes

Para que la persona responsable los descargue y los deje en la carpeta conectada, de modo que se puedan conservar con su SHA-256. «Material» quiere decir que sostiene una cifra o una decisión de los expedientes o de este documento.

| # | Documento | URL directa | Qué sostiene | Estado |
|---|---|---|---|---|
| 1 | BORME-C-2026-738 (12-mar-2026), convocatoria de la junta de Viscofan | https://boe.es/borme/dias/2026/03/12/pdfs/BORME-C-2026-738.pdf | reducción de 500.000 acciones (D3) | leído en texto (4.13) |
| 2 | BORME-C-2026-1603 (28-abr-2026), reducción ejecutada | https://boe.es/borme/dias/2026/04/28/pdfs/BORME-C-2026-1603.pdf | 46.000.000 acciones (D3) | leído en texto (4.13) |
| 3 | BORME-C-2026-3155 (2-jun-2026), aumento liberado y reducción | https://www.boe.es/borme/dias/2026/06/02/pdfs/BORME-C-2026-3155.pdf | emitidas a junio de 2026 (D3) | leído en texto (4.13) |
| 4 | BORME-C-2025-6267 (19-nov-2025), dividendo flexible de 2025 | https://boe.es/borme/dias/2025/11/19/pdfs/BORME-C-2025-6267.pdf | movimiento de la autocartera de 2025 (D3) | leído en texto (aquí) |
| 5 | CNMV, Viscofan, I semestre de 2026 (nº 2026107196) | página https://www.cnmv.es/portal/aldia/detalleifialdia.aspx?nreg=2026107196 (enlace «Informe estadístico» en PDF de esa página) | autocartera a 30-jun-2026 (D3) | leído en texto (4.13) |
| 6 | **CNMV, Viscofan, II semestre de 2025 (nº 2026030312), Informe estadístico** | https://www.cnmv.es/webservices/verdocumento/ver?e=exhzoYHsIwQnuEcovmFg5W1qAN8WXDbTqoji8BsOjjT1xVx9TYwe6nqlQTLZolJy | **segunda edición de la contradicción del BPA** (D3) | leído en texto (aquí) |
| 7 | **Informe anual de Viscofan de 2024, resultados económicos y de gestión** (desglose por tipo de 2024) | https://www.informeanual2024.viscofan.com/en/financial-and-management-results.html (página HTML; buscar en ella el PDF descargable del informe de gestión 2024) | θ (a.2; D2, D5) | leído en texto (aquí) |
| 8 | Viscofan, presentación del plan estratégico «Beat'30» (26/27-feb-2026; CNMV, «Otra información relevante») | sin URL directa obtenida: CNMV → Viscofan → Otra información relevante, febrero de 2026 | división de los 600 M€ entre crecimiento y lo demás (a.1) | **no obtenido** |
| 9 | Viscofan, nota de resultados de 2021 y de 2023 (inversión) | https://public.viscofan.com/investor-relations/financialinformation/en/OIR_Nota%20de%20Resultados%204T21_DEF_EN.pdf · https://public.viscofan.com/investor-relations/financialinformation/en/Nota%20de%20resultados%202023_EN.pdf | contraste del desglose de 2021 y 2023 (ya en `IA_2021_es` y `IA_2023_es`) | bloqueado por robots; **opcional** |
| 10 | Deutsche Bundesbank, «Tägliche Renditen der jeweils jüngsten Bundeswertpapiere» (rf de Vidrala) | https://www.bundesbank.de/resource/blob/772218/f561ec1a8ae1e51f3cd4d15d81d454cf/472B63F073F071307366337C94F8C870/rendbund-data.pdf | C57 = 2,85 % | leído en texto (4.10.1); la revisión externa registró SHA-256 `6ace5ac7…a9dd` para su ejemplar |
| 11 | Vidrala, transcripción o grabación oficial de la presentación de resultados de 2024 (28-feb-2025) | la fuente consultada es de terceros: https://www.roic.ai/quote/VDRFF/transcripts/2024-year/4-quarter. La oficial estaría en vidrala.com, inversores | «more than pure replacement» (a.3) | texto de terceros |
| 12 | Vidrala, informe anual de 2024 (español) | https://ddd.uab.cat/pub/infanu/22449/iaVIDRALAa2024ispa.pdf | contexto de los hornos (a.3) | **acceso fallido** (client_error); **opcional** |

**Prioridad.**
- Alta, porque sostienen D3 y D5: los números 1–7.
- Media: el 8, que resolvería la discrepancia de «Beat'30».
- Opcional: 9, 11 y 12.
- El 10 ya está identificado desde la 4.10.1.
