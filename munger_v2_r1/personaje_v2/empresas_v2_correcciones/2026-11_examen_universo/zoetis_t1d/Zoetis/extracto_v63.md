# Extracto V6.3 · Zoetis Inc. (ZTS) · corte 9-oct-2026

Fuentes: 10-K 2016–2025 y 10-Q del T1 y T2 de 2026, y documentos de resultados del T2 2026 publicados el 6-ago-2026: comunicado (zoetis-2q2026-press-release.txt, texto de una página HTML), presentación (zoetis-2q2026-financial-results.txt) y transcripción de la conferencia (zoetis-2q2026-earnings-call.txt) (carpeta texto/). Cifras en millones de dólares salvo indicación. En lo que sale de los tres documentos del T2 2026, las frases entre «» marcadas «(paráfrasis traducida)» son traducciones de la orquestación, no citas literales. «PDF p.» es la marca `[PDF PAGE n]` del texto. Los 10-K 2020–2024 vienen de OCR: toda cifra de esos años que se cita aquí cuadra con su total (suma de segmentos, de especies o de viñetas de crecimiento) en la misma página; cuando solo hay una página, se dice. A partir del 1-ene-2026 las filiales no estadounidenses dejaron de declarar con un mes de desfase (Fiscal Year Alignment); las cifras de 2025 de los 10-Q de 2026 están reexpresadas y no coinciden con las del 10-K 2025 [zoetis-10q-2026-q2.txt, PDF p. 29].

## 0. Vigencia de las cifras heredadas de la etapa 1 (zoetis_t1d, Claude orquestación, 19-nov-2026)

Los textos heredados de la etapa 1 (sección 6 de `datos_v63.md`, `etapa1/Zoetis_respuesta.md`, observaciones del Control maestro) **no se han tocado** y citan cifras que hoy valen otra cosa. Esta tabla da, para cada una, el valor vigente del expediente, su celda y su fuente. Manda la columna «vigente». Bloque añadido por la orquestación al extracto conservado de zoetis_t1c (rastro: `resultados/vigencia_extracto_t1d.json`); no es extracción nueva de las fuentes.

| Cifra | Etapa 1 (dónde la cita) | Vigente | Celda | Fuente |
|---|---|---|---|---|
| Capitalización (C41) | 30.198 mm (C13); 30.198,4 = 73,08 × 413,223602 (acciones de la portada del 10-Q, 31-jul-2026; Control maestro de la etapa 1) | 31.053,7042578 mm = 73,08 × 424,927535, producto exacto | Análisis!C41 | fase1_metadatos.json (capitalizacion); acciones: 10-K 2025 PDF p. 68. P-O2 y Z-ACC (19-nov-2026): acciones al cierre del ejercicio con precio del 8-oct-2026, desalineación de fechas declarada; con las 414.154.046 acciones del 30-jun-2026 (10-Q T2 2026 PDF p. 5) sería 30.266,4 |
| Acciones (C55) | 417,7 m (media ponderada diluida del 2T26; respuesta.md §1 y Control maestro); 413,2 en portada (31-jul-2026) | 424,927535 m, exactas (424.927.535 acciones en circulación a 31-dic-2025, sin dilución) | Análisis!C55 | 10-K 2025 PDF p. 68 (balance); comprobado contra la cifra impresa por fase1_historia.py (historia_revision.md, «Acciones de los metadatos») |
| FCF base (C52) | 1.995 mm (C13, C25, B67, B69; respuesta.md §1); «≈2.000 mm» (respuesta.md §3) | 1.994,001 mm = C46 2.736,667 − C47 669,333 − C48 0 − C49 1,000 − C50 72,333 (con C51 = Sí, que decide la fase A) | Análisis!C52 (fórmula) | C46, C47, C49 y C50: cálculo declarado sobre el 10-K 2025 PDF p. 70 y 89 (fase1_v63.json); C48 = 0 (US GAAP) |
| Rendimiento FCF base ÷ capitalización | ≈6,6 % (C13) | 6,42 % | C52 ÷ C41 | derivado de las dos filas anteriores |
| Deuda neta | 7.575 mm (C13, C62, C76; respuesta.md §1); «≈18 USD/acción» | 7.572 mm = deuda 9.048 − caja 1.476 (30-jun-2026); 17,82 USD/acción con C55 | C54 − C53 | 10-Q T2 2026 PDF p. 5 |
| Deuda neta ÷ EBITDA (C33) | 1,92x (C20; C33 de la etapa 1) | 1,8968x (aproximación declarada; todo reexpresado ≈ 1,88x) | Análisis!C33 | TTM = 2025 (10-K) − 6M-2025 + 6M-2026 (10-Q T2 2026 PDF p. 3, 5, 8 y 10); «Fiscal Year Alignment»: mezcla bases (convención/aproximación, no derivado exacto) |
| EBIT TTM a 30-jun-2026 | 3.463 mm (EBIT derivado de la etapa 1, Control maestro M29, fundamento de C24) | 3.510 mm = BAI 3.272 + gasto por intereses 238 (EBIT = BAI + intereses: el signo de los intereses se corrigió desde zoetis_t1b); EBITDA 3.992 con D&A 482 | (dentro de C33 y C42) | 10-K 2025 PDF p. 66 y 70; 10-Q T2 2026 PDF p. 3, 8 y 10 |
| EV/EBITDA (C42) | 9,57x (C42 de la etapa 1, con capitalización 30.198) | 9,675778x = (C41 + 7.572) ÷ 3.992 (aproximación declarada; con las acciones del 30-jun-2026, 9,48x; todo reexpresado ≈ 9,61x) | Análisis!C42 | C41 exacto y el TTM de C33; desalineación de fechas declarada (Z-ACC): precio 8-oct-2026, acciones 31-dic-2025, balance 30-jun-2026 |
| FCF TTM (C40) | 2.365 mm (C25; C40 de la etapa 1, con el capex del 10-Q del T2 2025, que no está en el expediente) | 2.363 mm = CFO 2.887 − capex 524 − principal de arrendamientos financieros 0 (aproximación declarada; todo reexpresado 2.316) | Análisis!C40 | 10-K 2025 PDF p. 70 y 89; 10-Q T2 2026 PDF p. 8 y 11 |
| ROIC (C24) | 26,6 % (C14, C24), ≈27 % (C93), 26–30 % (B101; respuesta.md §6) | C24 = 0,266 conservado como convención NO reproducible con el expediente (F «Dato no verificable»): con el EBIT corregido y el capital del expediente sale ≈ 26,2–26,9 % | Análisis!C24 | registro de entradas (Análisis!C24, justificacion_clase); su fórmula y el 10-Q del T2 2025 no están en el expediente |
| Margen EBIT (Historia, EBIT = BAI + intereses) | la etapa 1 no cita el margen EBIT en cifras («márgenes crecientes», C14; el margen antes de impuestos 28,7 % → 35,5 % de C27 no depende del EBIT y no cambia) | 2016 28,5 % · 2017 32,0 % · 2018 32,5 % · 2019 32,3 % · 2020 33,4 % · 2021 34,9 % · 2022 35,6 % · 2023 37,2 % · 2024 36,3 % · 2025 37,8 % | Historia (ventas y ebit) | fase1_v63.json (Historia construida por fase1_historia.py) |
| C46 / C47 / C50 | 2.736,7 / 669,3 / 72,3 (C51: «SBC media FY23–25 de 72,3 mm») | 2.736,667 / 669,333 / 72,333 (valores exactos, cálculo declarado) | Análisis!C46, C47, C50 | 10-K 2025 PDF p. 70 (precedente E1: exactos en lugar de redondeos) |
| C48 / C49 | C48 «vacía» (C62; Control maestro M45) y C49 vacía (= 0) | C48 = 0 (US GAAP: intereses pagados dentro del CFO; cero pendiente H1) · C49 = 1,000 (principal de arrendamientos financieros — / 1 / 2) | Análisis!C48, C49 | 10-K 2025 PDF p. 70 y 89 |
| P/FCF histórico (C88) | mediana 47,1x (C68), «47x» (B102), 66,4x en 2021 (C98) | sin valor vigente verificado: C88 = 47,1 es «Dato no verificable» (Digrin, tercero sin bytes en el expediente; su FCF es CFO − capex) | Análisis!C88 | registro de entradas (lectura externa, no comprobada) |
| Valor intrínseco externo (C38) | 197,36 USD (Simply Wall St; Control maestro de la etapa 1) | sin valor vigente verificado: C38 pasa a «Dato no verificable» en zoetis_t1d (tercero sin bytes); solo contexto | Análisis!C38 | registro de entradas (lectura externa) |
| Escenarios y precio de Sí | malo ≈48,7–49 USD, normal ≈90,9–91, bueno ≈120,2, ponderado ≈88,3; precio de Sí ≈49 USD; capitalización ≈20.200 (C13, C20, C104, B101, B102; respuesta.md §1, §6 y §7) | sin cifra vigente: son estimaciones de la etapa 1 hechas sin la hoja; las calcula el libro (precio_de_si.py) tras la fase B con las palancas de este expediente | Análisis (escenarios) | — |
| Guía orgánica 2026 | «guía orgánica negativa para 2026 (datos)» (C13), «−3 % a −1 %» (C31, B102; respuesta.md §2) | misma cifra, ahora con fuente en el expediente: crecimiento orgánico operativo (3)%–(1)% (guía de la dirección, no hecho), comunicado y presentación de resultados del T2 2026 publicados el 6-ago-2026 | — | sección 5 de este extracto (decisión de la persona del 18-nov-2026: incluir la guía) |
| Precio (C37) y tasa sin riesgo (C57) | 73,08 USD; Treasury a 10 años 5,22 % | sin cambio de valor, ahora con bytes: 73,08 USD = «Closing Price $73.08» de investor.zoetis.com («Historical Stock Quote», 2026-Oct-8; captura de la persona, anexo 3 ter), en vez de stockanalysis/MarketBeat; 5,22 % del CSV oficial del Tesoro (Release, asset 766892834) | Análisis!C37, C57 | fuentes_mercado/ (Zoetis_ZTS_2026-10-08_investor_zoetis_historical_quote.png y .txt; US_Treasury_par_yield_2026_Release_766892834.csv y .txt) |

Otras correcciones de zoetis_t1d que la etapa 1 no cita:
- Minoritarios (Historia fila 26): 2022 y 2023 impresos «(2)» y «(6)» (patrimonio negativo de minoritarios) → 0 (decisión Z-MIN de la persona, 19-nov-2026; cifra impresa en `historia_revision.md`); 2018 = 0 («—» impreso en el 10-K 2018 PDF p. 73), antes vacío.
- Reparto geográfico de la r mínima (Palancas A28:B33; decisión Z-R, 19-nov-2026: se deja y se anota): «Región · Asia» incluye «Other emerging markets» (913 mm, que no son solo Asia) y «Región · Australia & New Zealand» incluye «Other developed markets» (641 mm) y «Contract manufacturing & human health» (116 mm): las etiquetas del modelo no son las del informe [zoetis-10k-fy2025.txt, PDF p. 77].
- C33, C40 y C42 son aproximaciones declaradas (TTM con la «Fiscal Year Alignment»), no derivados exactos.

## 1. Mercado y cuota

- La empresa no publica ningún tamaño de mercado en dólares ni su cuota en porcentaje en estos documentos. Dice: «nuestro negocio es el mayor por ingresos de la industria de salud animal (que incluye medicinas, vacunas y diagnóstico)» [zoetis-10k-fy2025.txt, PDF p. 42]. Definición de industria que usa: medicinas, vacunas y diagnóstico, para animales de compañía y ganado [zoetis-10k-fy2025.txt, PDF p. 41].
- Crecimiento del mercado: solo una referencia relativa. Carta 10-K 2024: crecimiento operativo medio anual de ingresos del 8% desde la salida a bolsa en 2013, «3 puntos por encima de la media de la industria» [zoetis-10k-fy2024.txt, PDF p. 3]. Una sola página (OCR); no hay segunda fuente en los textos. No dice de qué estudio sale la media de la industria.
- Objetivo de largo plazo de la empresa (propuesta de valor): «crecer ingresos en línea o más rápido que el mercado» [zoetis-10k-fy2024.txt, PDF p. 6]; ya aparecía igual en [zoetis-10k-fy2017.txt, PDF p. 3].
- Cuota que publica la empresa en la presentación del T2 2026 (definición: cuota media mensual de pacientes caninos en el canal de clínica, Kynetec; excluye canales alternativos, especialidades, urgencias y clínicas de MARS): dermatología en EE. UU. ≈ 86% en el T2 2026, −5 puntos frente al T1 y −10 frente al T2 2025 [zoetis-2q2026-financial-results.txt, PDF p. 6]; Simparica Trio en EE. UU. ≈ 21%, −2 puntos frente al T1 y −1 frente al T2 2025; ≈ 28% en cachorros [zoetis-2q2026-financial-results.txt, PDF p. 7]. Es la única cuota en porcentaje de los documentos.
- Mercados futuros que estima la empresa (TAM, «oportunidad total dentro de salud animal» (paráfrasis traducida); guía, no hecho): enfermedad renal crónica 3,0–4,0 mil millones; oncología 1,2–1,7; cardiología 0,8–1,0; obesidad y metabolismo 0,8–1,0; ansiedad 0,7–1,4 [zoetis-2q2026-financial-results.txt, PDF p. 12].
- Descripción del mercado de compañía en el T2 2026 (declaración de la dirección): las visitas a clínicas veterinarias bajaron en todos los mercados, «tendencia de varios años» (paráfrasis traducida) junto a subidas de precio por encima de la inflación general; los nuevos competidores usan «más descuentos, rebajas, paquetes de cartera y otros incentivos» (paráfrasis traducida) para competir por los pacientes existentes [zoetis-2q2026-earnings-call.txt, PDF p. 3].
- Competidores que nombra el 10-K 2025: Boehringer Ingelheim Animal Health, Merck Animal Health, Elanco e IDEXX Laboratories; además competidores medianos, start-ups y «cientos» de productores [zoetis-10k-fy2025.txt, PDF p. 17]. No da cuotas de ninguno.
- Competencia genérica: «no existe una gran empresa de genéricos de salud animal con alcance global» [zoetis-10k-fy2025.txt, PDF p. 17]. Draxxin: ventas en EE. UU. bajaron un 66% desde 2021, primer año de genérico [zoetis-10k-fy2025.txt, PDF p. 42].
- Concentración (definición: porcentaje de los ingresos totales): 2025, Simparica/Simparica Trio 16% y Apoquel 12%; los 5 primeros 42%; los 10 primeros 57% [zoetis-10k-fy2025.txt, PDF p. 44]. 2024: 15% y 11%; 5 primeros 41%; 10 primeros 55% [zoetis-10k-fy2024.txt, PDF p. 13]. 2023: 13% y 10%; 37%; 49% [zoetis-10k-fy2023.txt, PDF p. 13]. 2016: línea ceftiofur 7%; 10 primeros 40% [zoetis-10k-fy2016.txt, PDF p. 14].
- Mercados emergentes, % de ingresos de la empresa: 22% (2016), 23% (2017), 23% (2018), 22% (2019), 21% (2020) [zoetis-10k-fy2016.txt, PDF p. 16; zoetis-10k-fy2017.txt, PDF p. 14; zoetis-10k-fy2018.txt, PDF p. 14; zoetis-10k-fy2019.txt, PDF p. 14; zoetis-10k-fy2020.txt, PDF p. 14]. Los años posteriores no repiten la frase.
- Cliente mayor: un distribuidor veterinario de EE. UU. = 16% de los ingresos de 2025, 14% de 2024 y 15% de 2023 [zoetis-10k-fy2025.txt, PDF p. 78].
- Canal: los dueños de mascotas pueden comprar en internet y grandes superficies; la empresa dice que a largo plazo «podría no poder mantener sus márgenes actuales» por el poder de compra de esos minoristas [zoetis-10k-fy2025.txt, PDF p. 43].

## 2. Economía por segmento y geografía

Segmentos: EE. UU. e Internacional (más «contract manufacturing & human health»).

Ingresos y resultado por segmento (el 10-K no publica margen en porcentaje por segmento; «resultado» es el que declara la empresa antes de partidas corporativas y no asignadas):

| Año | Ingresos EE. UU. | Ingresos Internacional | Resultado EE. UU. | Resultado Internacional | Fuente |
|---|---|---|---|---|---|
| 2016 | 2.447 | 2.390 | 1.508 | 1.054 | [zoetis-10k-fy2017.txt, PDF p. 45 y 51] |
| 2017 | 2.620 | 2.643 | 1.637 | 1.240 | [zoetis-10k-fy2018.txt, PDF p. 46 y 52] |
| 2018 | 2.877 | 2.890 | 1.815 | 1.399 | [zoetis-10k-fy2019.txt, PDF p. 50 y 54] |
| 2019 | 3.203 | 2.972 | 2.005 | 1.487 | [zoetis-10k-fy2020.txt, PDF p. 54 y 58] |
| 2020 | 3.557 | 3.035 | 2.239 | 1.547 | [zoetis-10k-fy2021.txt, PDF p. 53 y 56] |
| 2021 | 4.042 | 3.652 | 2.569 | 1.948 | [zoetis-10k-fy2022.txt, PDF p. 46 y 49] |
| 2022 | 4.313 | 3.681 | 2.763 | 1.990 | [zoetis-10k-fy2023.txt, PDF p. 47 y 49] |
| 2023 | 4.555 | 3.911 | 2.863 | 2.037 | [zoetis-10k-fy2025.txt, PDF p. 51] |
| 2024 | 5.074 | 4.102 | 3.336 | 2.118 | [zoetis-10k-fy2025.txt, PDF p. 51] |
| 2025 | 5.097 | 4.254 | 3.438 | 2.264 | [zoetis-10k-fy2025.txt, PDF p. 51] |

Comprobación de los años OCR (2020–2022): ingresos EE. UU. + Internacional + contract manufacturing (83; 82; 86) suman 6.675; 7.776; 8.080; resultados EE. UU. + Internacional suman los totales de segmentos publicados 3.786; 4.517; 4.753. El 4.313 de 2022 sale como 4313 en el OCR y cuadra con 8.080 − 3.681 − 86.

Animal de compañía y ganado (ingresos, total empresa): 2018 2.613 y 3.154; 2019 3.145 y 3.030; 2020 3.652 y 2.940; 2021 4.689 y 3.005; 2022 5.203 y 2.791 [zoetis-10k-fy2020.txt, PDF p. 54; zoetis-10k-fy2021.txt, PDF p. 53; zoetis-10k-fy2022.txt, PDF p. 46; zoetis-10k-fy2023.txt, PDF p. 47]. 2023 5.576 y 2.890; 2024 6.278 y 2.898; 2025 6.587 y 2.764 [zoetis-10k-fy2025.txt, PDF p. 48]. Cada año cuadra con el total más contract manufacturing.

2025 por segmento y especie: EE. UU. animal de compañía 4.220 y ganado 877; Internacional animal de compañía 2.367 y ganado 1.887 [zoetis-10k-fy2025.txt, PDF p. 51]. Variación 2025/2024 operativa (a tipo de cambio constante): EE. UU. animal de compañía +4%, ganado −14%; Internacional animal de compañía +7%, ganado +2% [zoetis-10k-fy2025.txt, PDF p. 51]. La caída del ganado de EE. UU. se debe a la venta de aditivos medicados (MFA) [zoetis-10k-fy2025.txt, PDF p. 51].

Ingresos por especie 2025 / 2024 / 2023: perros y gatos 6.283 / 5.993 / 5.291; caballos 304 / 285 / 285; vacuno 1.492 / 1.531 / 1.503; porcino 466 / 516 / 543; aves 432 / 527 / 524; peces 286 / 242 / 220; ovino y otros 88 / 82 / 100 [zoetis-10k-fy2025.txt, PDF p. 78].

Ingresos por categoría 2025 / 2024 / 2023: parasiticidas 2.341 / 2.153 / 1.947; vacunas 1.959 / 1.827 / 1.771; dermatología 1.754 / 1.655 / 1.427; antiinfecciosos 1.036 / 1.100 / 1.057; dolor y sedación 840 / 851 / 602; otros farmacéuticos 697 / 658 / 678; diagnóstico 434 / 386 / 376; otros no farmacéuticos 263 / 253 / 254; aditivos medicados en pienso 27 / 293 / 354 [zoetis-10k-fy2025.txt, PDF p. 78].

Reparto geográfico 2025 / 2024 / 2023, ingresos en millones [zoetis-10k-fy2025.txt, PDF p. 77]: EE. UU. 5.097 / 5.074 / 4.555; Australia 329 / 319 / 323; Brasil 393 / 414 / 393; Canadá 290 / 277 / 255; Chile 139 / 123 / 140; China 227 / 270 / 320; Francia 165 / 156 / 142; Alemania 236 / 225 / 202; Italia 137 / 129 / 121; Japón 154 / 147 / 158; México 160 / 169 / 162; España 145 / 130 / 122; Reino Unido 325 / 314 / 277; otros desarrollados 641 / 564 / 512; otros emergentes 913 / 865 / 784. Trece países fuera de EE. UU. superaron 100 en 2025 y 2024; doce en 2023; EE. UU. fue el único país con más del 10% [zoetis-10k-fy2025.txt, PDF p. 77]. Porcentaje de ingresos 2025: EE. UU. 55%, Brasil 4%, Australia 3%, Reino Unido 3%, Canadá 3%, Alemania 3%, China 2%, Francia 2%, México 2%, Japón 2%, España 2%, Chile 1%, Italia 1%, otros emergentes 10%, otros desarrollados 7% (la carta excluye contract manufacturing y salud humana, 1%) [zoetis-10k-fy2025.txt, PDF p. 2]. Mezcla animal de compañía / ganado por país: EE. UU. 83% / 17%; Internacional 56% / 44%; China 72% / 28%; Brasil 38% / 62%; Chile 24% / 76% [zoetis-10k-fy2025.txt, PDF p. 9].

Especies del segmento 2025 (porcentaje de los ingresos del segmento): EE. UU. perros y gatos 79%, vacuno 13%, caballos 4%, aves 3%, porcino 1%; Internacional perros y gatos 53%, vacuno 19%, porcino 9%, aves 7%, peces 7%, caballos 3%, ovino y otros 2% [zoetis-10k-fy2025.txt, PDF p. 10].

Moneda: 42% de los ingresos de 2025 en divisas distintas del dólar y 58% en dólares; el cambio restó un 1% al crecimiento reportado [zoetis-10k-fy2025.txt, PDF p. 43]. Primer semestre de 2026: 46% en divisas y 54% en dólares; el cambio sumó un 2% [zoetis-10q-2026-q2.txt, PDF p. 28].

Crecimiento a tipo constante («operativo» = sin efecto del tipo de cambio) y reportado, total empresa: 2017 8% y 9%; 2018 10% y 10%; 2019 10% y 7%; 2020 9% y 7%; 2021 15% y 16%; 2022 8% y 4%; 2023 7% y 6%; 2024 11% y 8%; 2025 3% y 2% [zoetis-10k-fy2018.txt, PDF p. 47; zoetis-10k-fy2019.txt, PDF p. 51; zoetis-10k-fy2020.txt, PDF p. 54; zoetis-10k-fy2021.txt, PDF p. 53; zoetis-10k-fy2022.txt, PDF p. 46; zoetis-10k-fy2023.txt, PDF p. 47; zoetis-10k-fy2024.txt, PDF p. 46; zoetis-10k-fy2025.txt, PDF p. 48]. Segunda definición, «orgánico operativo» (sin cambio ni adquisiciones/ventas): 7% (2023), 12% (2024), 6% (2025) [zoetis-10k-fy2025.txt, PDF p. 2]. No son comparables entre sí: la segunda excluye la venta de MFA.

Primer semestre 2026 frente a 2025 (reexpresado): ingresos 4.730 frente a 4.672 (+1% reportado, −1% operativo); segundo trimestre 2.468 frente a 2.474 (0% reportado, −2% operativo) [zoetis-10q-2026-q2.txt, PDF p. 27]. Por segmento, seis meses: EE. UU. 2.356 frente a 2.539 (−7%); Internacional 2.322 frente a 2.070 (+12% reportado, +7% operativo) [zoetis-10q-2026-q2.txt, PDF p. 33]. Animal de compañía EE. UU. 1.909 frente a 2.149 (−11%); ganado EE. UU. 447 frente a 390 (+15%) [zoetis-10q-2026-q2.txt, PDF p. 33]. La empresa atribuye el descenso de EE. UU. en animal de compañía a «demanda final más débil y un entorno más competitivo», con presión competitiva en dermatología y Simparica Trio, sensibilidad al precio por la macroeconomía, genéricos de Cerenia y Convenia y menores ventas de Librela [zoetis-10q-2026-q2.txt, PDF p. 35]. El ganado de EE. UU. creció por mayor oferta y demanda por el brote del gusano barrenador del Nuevo Mundo [zoetis-10q-2026-q2.txt, PDF p. 35].

Margen bruto por segmento (declarado en el 10-Q): EE. UU. 82,7% frente a 84,0% y Internacional 71,0% frente a 70,2% en seis meses de 2026 frente a 2025 [zoetis-10q-2026-q2.txt, PDF p. 35]. Segundo trimestre: EE. UU. 83,1% frente a 84,7%; Internacional 71,0% frente a 70,4% [zoetis-10q-2026-q2.txt, PDF p. 34]. Resultado de segmento seis meses: EE. UU. 1.534 frente a 1.709; Internacional 1.300 frente a 1.119 [zoetis-10q-2026-q2.txt, PDF p. 26]. La fase de 2026 de Internacional se vio ayudada por el cambio operativo del calendario de subidas de precio y de pedidos (alineación de año fiscal) [zoetis-10q-2026-q2.txt, PDF p. 36]. En el cuarto trimestre de 2025 esa alineación añadió aproximadamente un 2,5% a 3,5% a las ventas de Internacional por adelanto de ventas, «tendencia que no esperamos que se repita» [zoetis-10k-fy2025.txt, PDF p. 47].

Segundo trimestre de 2026, crecimiento «orgánico operativo» (sin cambio ni adquisiciones/ventas, definición de la empresa): total −1%; EE. UU. −7% (compañía −11%, ganado +23%); Internacional +6% (compañía +5%, ganado +6%); compañía total −6%, ganado +11% [zoetis-2q2026-financial-results.txt, PDF p. 15]. Por país (orgánico operativo, T2 2026): China −14%, Reino Unido −9%, Francia −8%, Alemania +19%, otros emergentes +21% [zoetis-2q2026-financial-results.txt, PDF p. 21]. La dirección dice que el ganado de EE. UU. del T2 tuvo partes «transitorias» (paráfrasis traducida) (suministro y demanda de parasiticidas inyectables por el gusano barrenador) y que, normalizado, su crecimiento sería de un dígito alto [zoetis-2q2026-earnings-call.txt, PDF p. 16].

China: ingresos 320 (2023), 270 (2024), 227 (2025) [zoetis-10k-fy2025.txt, PDF p. 77]. El 10-K 2025 no da una causa en la página de ingresos por país. Hay restricciones de repatriación de caja y controles de cambio en China [zoetis-10k-fy2025.txt, PDF p. 34].

## 3. Capacidad, capex e inversión

- Red de fabricación: 21 plantas propias en 10 países y más de 90 fabricantes por contrato (CMO) [zoetis-10k-fy2025.txt, PDF p. 28 y 16–17]. En 2023 compró una planta cerca de Atlanta (Georgia) donde planea «iniciar producción comercial en el futuro»; no da importe ni fecha [zoetis-10k-fy2025.txt, PDF p. 16]. Está ampliando capacidad en plantas existentes, sin cifra [zoetis-10k-fy2025.txt, PDF p. 16].
- Capacidad de anticuerpos monoclonales: carta 10-K 2022, en Tullamore (Irlanda) iniciaron una ampliación para producir más anticuerpos monoclonales (principio activo de los productos de dolor artrósico) y en Lincoln (Nebraska) se construye un centro de I+D [zoetis-10k-fy2022.txt, PDF p. 4]. Sin importes. Carta 10-K 2021: ampliación de capacidad de monoclonales en EE. UU. y Europa [zoetis-10k-fy2021.txt, PDF p. 6]. 10-K 2021: nueva planta en Suzhou (China) para investigar y producir vacunas [zoetis-10k-fy2021.txt, PDF p. 33].
- Instalaciones: unas 173 propiedades, 11,5 millones de pies cuadrados; Kalamazoo 1,6 millones (0,9 de I+D y 0,7 de fabricación) [zoetis-10k-fy2025.txt, PDF p. 38].
- Capex (flujos de inversión): 2025 621, 2024 655, 2023 732 [zoetis-10k-fy2025.txt, PDF p. 2 y 70]. Seis meses de 2026: 227 frente a 324 en 2025 [zoetis-10q-2026-q2.txt, PDF p. 8]. Intereses capitalizados: 47 (2025), 39 (2024), 27 (2023) [zoetis-10k-fy2025.txt, PDF p. 86]. Capex por destino: no encontrado. Inmovilizado material neto: 3.756 a 30-jun-2026 y 3.693 a 31-dic-2025 [zoetis-10q-2026-q2.txt, PDF p. 5].
- Depreciación y amortización de seis meses: 238 frente a 243 [zoetis-10q-2026-q2.txt, PDF p. 8]. Depreciación 2025: 325; amortización 34 en el ajuste del resultado ajustado [zoetis-10k-fy2025.txt, PDF p. 54].
- I+D: 698 en 2025 (7% de ingresos), 686 en 2024 (7%), 614 en 2023 (7%) [zoetis-10k-fy2025.txt, PDF p. 49]. Seis meses de 2026: 353 (7%) frente a 328 (7%) [zoetis-10q-2026-q2.txt, PDF p. 29]. Unos 1.700 empleados en I+D y más de 300 programas [zoetis-10k-fy2025.txt, PDF p. 16]. «Desde la independencia se han invertido 6.000 millones en I+D» [zoetis-10k-fy2025.txt, PDF p. 3]. Cartera: «12 posibles productos de más de 100 millones de ventas anuales» [zoetis-10k-fy2025.txt, PDF p. 6]. Productos ya con más de 100 millones en 2022 y 2023: 15 [zoetis-10k-fy2023.txt, PDF p. 13].
- Calendario de I+D que cita la propia empresa (guía, no hecho): enfermedad renal crónica, primera aprobación para perros esperada en 2027; oncología, aprobaciones iniciales proyectadas para 2028–2029; siete proyectos activos en enfermedad renal crónica [zoetis-10k-fy2025.txt, PDF p. 4]. Lenivia (perros) y Portela (gatos), monoclonales de tres meses, aprobados en la UE y Canadá en 2025 [zoetis-10k-fy2025.txt, PDF p. 12]. Se lanzaron en Internacional en 2026 [zoetis-10q-2026-q2.txt, PDF p. 35].
- Reestructuración: seis meses de 2026 99 (de ellos 94 por indemnizaciones, bajo un «programa integral de costes y productividad»); provisión de reestructuración 95 a 30-jun-2026 frente a 25 a 31-dic-2025 [zoetis-10q-2026-q2.txt, PDF p. 14]. En 2025: 51 [zoetis-10k-fy2025.txt, PDF p. 50]. Costes del programa de transformación de procesos (ERP): 29 en 2025, fuera del resultado ajustado, «no esperados en el futuro previsible» [zoetis-10k-fy2025.txt, PDF p. 54–55].
- Adquisiciones y ventas con precio:
  - Neogen (negocio de genómica animal): acuerdo firmado en el T1 de 2026, cierre esperado en el segundo semestre de 2026; precio no indicado [zoetis-10q-2026-q2.txt, PDF p. 14].
  - Veterinary Pathology Group (R. U. e Irlanda), 2025: sin impacto material; precio no indicado [zoetis-10k-fy2025.txt, PDF p. 78].
  - PetMedix (2023): 111 en efectivo al cierre (sin los 19 de caja adquirida), 5 retenidos y hasta 100 contingentes por hitos [zoetis-10k-fy2025.txt, PDF p. 78].
  - Venta de aditivos medicados y productos solubles a Phibro (31-oct-2024): precio neto 299; cobro 303; pérdida antes de impuestos 25 [zoetis-10k-fy2025.txt, PDF p. 79].
  - Venta de la mayoría de Pumpkin (seguros de mascotas), 2023: cobro neto 93, ganancia 101 [zoetis-10k-fy2025.txt, PDF p. 79].
  - Jurox (2022): precio en efectivo 226, ajustado a 240 [zoetis-10k-fy2022.txt, PDF p. 76; una sola página, OCR].
  - Abaxis (2018): 83,00 por acción en efectivo; efectivo pagado a accionistas 1.898 [zoetis-10k-fy2018.txt, PDF p. 85]. Pharmaq (2015): 765, ajustado a 668 netos [zoetis-10k-fy2016.txt, PDF p. 82].
    - VitalRADS (teleradiología veterinaria): adquisición completada en el T2 2026; precio no indicado [zoetis-2q2026-financial-results.txt, PDF p. 5 y 17].
  - Ningún documento da múltiplos de adquisición.
- Inversión acumulada de 2026 según la presentación del T2 (seis meses): ≈ 350 en I+D y ≈ 225 de capex «en fabricación, I+D e informática» (paráfrasis traducida) [zoetis-2q2026-financial-results.txt, PDF p. 17].

## 4. Precios y poder de fijación

Componentes del crecimiento operativo que declara la empresa (aproximados, en puntos de crecimiento):

| Año | Precio | Volumen y otros componentes | Fuente |
|---|---|---|---|
| 2017 | 1 (productos en línea) | dermatología y lanzamientos 7; en línea 2 (volumen 1 y precio 1); racionalizaciones −1 | [zoetis-10k-fy2018.txt, PDF p. 47] |
| 2018 | 3 | volumen en línea 3 (2 dermatología); Abaxis 2; nuevos 2 | [zoetis-10k-fy2018.txt, PDF p. 47] |
| 2019 | 2 | volumen en línea 4 (2 dermatología); Abaxis 2; nuevos 2 | [zoetis-10k-fy2019.txt, PDF p. 51] |
| 2020 | 2 | nuevos 3; en línea 3; adquisiciones 1 | [zoetis-10k-fy2020.txt, PDF p. 54] |
| 2021 | 1 | en línea 9; nuevos 5 | [zoetis-10k-fy2021.txt, PDF p. 53] |
| 2022 | 3 | nuevos 4; dermatología 2; otros en línea −1 | [zoetis-10k-fy2022.txt, PDF p. 46] |
| 2023 | 5 | nuevos 2 | [zoetis-10k-fy2023.txt, PDF p. 47] |
| 2024 | 6 | nuevos 3; dermatología 2 | [zoetis-10k-fy2024.txt, PDF p. 46] |
| 2025 | 4 | otros en línea +1; franquicias clave +1; venta MFA −3 | [zoetis-10k-fy2025.txt, PDF p. 48] |
| T1 2026 | 2 | franquicias clave −3; MFA −1; otros en línea +1 | [zoetis-10q-2026-q1.txt, PDF p. 25] |
| T2 2026 | no aparece como componente en el 10-Q; en la conferencia: «aproximadamente plano» (orgánico, volumen −1) | franquicias clave −3; MFA −1; otros en línea +2 | [zoetis-10q-2026-q2.txt, PDF p. 29; zoetis-2q2026-earnings-call.txt, PDF p. 7; zoetis-2q2026-financial-results.txt, PDF p. 3] |
| 6M 2026 | 1 | franquicias clave −3; otros en línea +1 | [zoetis-10q-2026-q2.txt, PDF p. 30] |

Cada fila de 2020–2024 (OCR) suma el crecimiento operativo total publicado en el mismo párrafo: 9; 15; 8; 7; 11.

- Efecto de precio en la caja: en 2025 el coste de ventas bajó del 29,4% al 28,2% de los ingresos por la venta de MFA, las subidas de precio, el cambio y menores cargos de inventario [zoetis-10k-fy2025.txt, PDF p. 49].
- En seis meses de 2026 el coste de ventas subió del 27,4% al 27,8% por mezcla desfavorable y cambio, «parcialmente compensado» por costes de fabricación y subidas de precio [zoetis-10q-2026-q2.txt, PDF p. 30].
- Resistencia del cliente: en EE. UU., animal de compañía, «sensibilidad al precio persistente por la macroeconomía» en dermatología y Simparica Trio [zoetis-10q-2026-q2.txt, PDF p. 35]. Los genéricos obligan a bajar precios y dar descuentos o rebajas [zoetis-10k-fy2025.txt, PDF p. 25]. La empresa dice que su cartera y la estabilidad de la demanda le permiten «incorporar los retos inflacionarios a los precios» [zoetis-10k-fy2025.txt, PDF p. 42] (declaración de la empresa, no medición).
- Lealtad de marca tras la pérdida de exclusividad: «creemos que una lealtad de marca significativa suele continuar» [zoetis-10k-fy2025.txt, PDF p. 17]. Contraejemplo medido: Draxxin −66% en EE. UU. desde 2021 [zoetis-10k-fy2025.txt, PDF p. 42].
- Cambio del calendario de subidas en Internacional: desde el T1 de 2026 las subidas anuales y las compras previas ocurren en el mismo año natural; hay pedidos de diciembre de 2025 trasladados a enero de 2026 [zoetis-10q-2026-q2.txt, PDF p. 29]. Distorsiona precio y volumen del T1 de 2026 frente a 2025.
- Respuesta de precio en 2026 (declaraciones de la dirección en la conferencia del T2): ajustes de precio en Cerenia y Convenia en EE. UU. por la competencia genérica e inversiones en dermatología, que «pesaron» (paráfrasis traducida) en el precio del trimestre y en la guía del año [zoetis-2q2026-earnings-call.txt, PDF p. 7]; «no estamos cambiando el precio de lista» (paráfrasis traducida), sino rebajas y otras inversiones de «gross-to-net» para defender volumen y cuota [zoetis-2q2026-earnings-call.txt, PDF p. 12]; en Apoquel el precio pasó a ser «un factor más prominente» (paráfrasis traducida) en la prescripción y las rebajas bajan el precio realizado [zoetis-2q2026-earnings-call.txt, PDF p. 8].
- Precio esperado para 2026 (guía oral del director financiero, 6-ago-2026): con la guía revisada, la realización de precio del año «podría estar en 0% a −1%, potencialmente −2%» (paráfrasis traducida) en el extremo bajo [zoetis-2q2026-earnings-call.txt, PDF p. 16].
- Ganado: ventas de cattle crecieron «sobre todo por precio» en Internacional en 2025 [zoetis-10k-fy2025.txt, PDF p. 52]; en 2026 el crecimiento de peces fue «por precio» [zoetis-10q-2026-q2.txt, PDF p. 36].
- Cliente mayor: un distribuidor con 16% de ingresos (ver sección 1). Rebajas de contrato devengadas aumentaron en 2025 [zoetis-10k-fy2025.txt, PDF p. 56]; no se da importe.

## 5. Guía y objetivos de la dirección

Todo lo de esta sección es guía o intención, no hecho.

- Guía anual de 2026 revisada el 6-ago-2026 (guía; tipos de cambio del 21-jul-2026) frente a la anterior del 7-may-2026 [zoetis-2q2026-press-release.txt, PDF p. 1; zoetis-2q2026-financial-results.txt, PDF p. 13 y 18]:
  - Ingresos: 9.120 a 9.320 (antes 9.680 a 9.960); crecimiento orgánico operativo (3)% a (1)% (antes 2% a 5%).
  - Coste de ventas ajustado: ≈ 29,0% de los ingresos (antes ≈ 28,5%). SG&A ajustado 2.330 a 2.380 (antes 2.350 a 2.400). I+D ajustada 720 a 730 (antes 735 a 745). Intereses y otros ajustados ≈ 215 (sin cambio). Tipo impositivo sobre el resultado ajustado ≈ 20,5% (sin cambio).
  - Beneficio neto ajustado 2.570 a 2.620 (antes 2.870 a 2.950); crecimiento orgánico operativo (9)% a (5)% (antes 2% a 6%). Beneficio neto reportado 2.330 a 2.380 [zoetis-2q2026-press-release.txt, PDF p. 1].
  - BPA diluido ajustado 6,15 a 6,25 (antes 6,85 a 7,00); reportado 5,55 a 5,65 (antes 6,35 a 6,50). Partidas significativas y costes de adquisiciones y ventas ≈ 150 (antes ≈ 100).
  - Supuestos que declara la empresa: persistencia de una demanda final más débil, sensibilidad al precio por la macroeconomía y presión competitiva basada en promociones, compensadas en parte por ganado, diagnóstico y control de costes; el extremo alto supone presión competitiva y de precio contenida y pérdidas de cuota «manejables» (paráfrasis traducida) en dermatología y parasiticidas; el bajo, presión acelerada, mayores pérdidas de cuota y ganado más lento en el segundo semestre [zoetis-2q2026-financial-results.txt, PDF p. 13]. Las ventas de julio «aún no indican estabilización del mercado» (paráfrasis traducida) [zoetis-2q2026-earnings-call.txt, PDF p. 10].
  - Capex de 2026: la guía no lo incluye.
- Objetivo de crecimiento a 3–5 años (guía, carta 10-K 2023): «crecer los ingresos anuales más rápido que el mercado con crecimiento operativo en el rango medio-alto de un dígito» [zoetis-10k-fy2023.txt, PDF p. 6] (OCR; una página). Resultado posterior publicado, sin interpretar: crecimiento operativo 11% en 2024 y 3% en 2025 (orgánico 12% y 6%; ver sección 2) [zoetis-10k-fy2025.txt, PDF p. 48 y 2]; −1% en seis meses de 2026 [zoetis-10q-2026-q2.txt, PDF p. 27].
- Propuesta de valor de largo plazo (guía): crecer ingresos en línea o más rápido que el mercado; crecer el beneficio neto ajustado más rápido que los ingresos; invertir en innovación, I+D y desarrollo de negocio [zoetis-10k-fy2024.txt, PDF p. 6]. Beneficio neto ajustado: 2.847 (2025), 2.693 (2024), 2.457 (2023), es decir +6% y +10% [zoetis-10k-fy2025.txt, PDF p. 53]. Reportado: 2.673, 2.486, 2.344 [zoetis-10k-fy2025.txt, PDF p. 48].
- Dividendo (guía, 6-ago-2026): «se espera mantener o aumentar el dividendo» (paráfrasis traducida) [zoetis-2q2026-financial-results.txt, PDF p. 17].
- Recompras en 2026 (hecho declarado): más de 550 en el T2 2026, «por encima de la media trimestral histórica» (paráfrasis traducida) sin contar la recompra financiada con el convertible del T4 de 2025 [zoetis-2q2026-earnings-call.txt, PDF p. 9]; 1.600 devueltos al accionista en el semestre con dividendos y recompras [zoetis-2q2026-financial-results.txt, PDF p. 17].
- Dirección financiera: el director financiero (Wetteny Joseph) deja el cargo y sigue como asesor especial hasta principios de 2027 [zoetis-2q2026-earnings-call.txt, PDF p. 7].
- Dividendo (guía): dividendo trimestral de 0,50 por acción en 2025; «esperamos seguir pagando dividendos coherentes con los pagos históricos»; sin garantía [zoetis-10k-fy2025.txt, PDF p. 39]. Dividendos declarados por acción 2,030 (2025), 1,796 (2024), 1,557 (2023) [zoetis-10k-fy2025.txt, PDF p. 66]. En 2026: 0,530 por trimestre; 1,060 en seis meses [zoetis-10q-2026-q2.txt, PDF p. 3].
- Recompras: programa multianual de hasta 6.000 autorizado en agosto de 2024; quedaban 2.400 a 31-dic-2025 y 1.300 a 30-jun-2026 [zoetis-10k-fy2025.txt, PDF p. 39; zoetis-10q-2026-q2.txt, PDF p. 44]. Hechos: 23,9 millones de acciones por 3.200 en 2025 [zoetis-10k-fy2025.txt, PDF p. 59]; 11,0 millones por 1.159 en seis meses de 2026 [zoetis-10q-2026-q2.txt, PDF p. 44]. Con el bono convertible de diciembre de 2025: 248 en 2,1 millones de acciones y 1.535 en 12,3 millones de acciones más, completadas a 31-mar-2026 [zoetis-10q-2026-q2.txt, PDF p. 43].
- Calendario esperado: eliminar el desfase de un mes de filiales no estadounidenses en 2026 (ya aplicado desde el 1-ene-2026) [zoetis-10q-2026-q2.txt, PDF p. 29]. Contribución a pensiones esperada en 2026: 8 [zoetis-10k-fy2025.txt, PDF p. 59]. Cierre de Neogen genómica: segundo semestre de 2026 [zoetis-10q-2026-q2.txt, PDF p. 14].
- Cumplimiento de la guía anterior: la guía del 7-may-2026 (ingresos 9.680 a 9.960; orgánico +2% a +5%) se rebajó el 6-ago-2026 a 9.120 a 9.320 y (3)% a (1)% [zoetis-2q2026-press-release.txt, PDF p. 1]; la dirección dice que el T2 «quedó por debajo de nuestras expectativas» (paráfrasis traducida) [zoetis-2q2026-earnings-call.txt, PDF p. 3]. Guías de años anteriores: no están en los documentos.

## 6. Financiación

- Deuda de largo plazo, valor nominal 9.150 a 31-dic-2025 (6.650 a 31-dic-2024); valor razonable 8.842 (6.097 en 2024) [zoetis-10k-fy2025.txt, PDF p. 86]. Contable (neta de descuentos y costes) 9.042 en el 10-K y 9.048 a 30-jun-2026 [zoetis-10k-fy2025.txt, PDF p. 57; zoetis-10q-2026-q2.txt, PDF p. 42].
- Bonos y cupón [zoetis-10k-fy2025.txt, PDF p. 59]: 750 al 3,000% (sep-2027); 500 al 3,900% (ago-2028); 850 al 4,150% (ago-2028); convertible 2.000 al 0,250% (jun-2029); 750 al 2,000% (may-2030); 750 al 5,600% (nov-2032); 1.000 al 5,000% (ago-2035); 1.150 al 4,700% (feb-2043); 500 al 3,950% (sep-2047); 400 al 4,450% (ago-2048); 500 al 3,000% (may-2050).
- Vencimientos del principal a 31-dic-2025: 2026 0; 2027 750; 2028 1.350; 2029 2.000; 2030 750; después de 2030 4.300; total 9.150. Pagos de intereses esperados: 296; 296; 273; 216; 206; 1.958 después; total 3.245 [zoetis-10k-fy2025.txt, PDF p. 86].
- Convertible: precio de conversión inicial unos 148,20 por acción; «capped call» con precio tope inicial unos 211,72, sobre unos 13,5 millones de acciones, coste 187; ingresos netos 1.970 [zoetis-10k-fy2025.txt, PDF p. 58].
- Coste medio de la deuda: la empresa no publica un porcentaje medio. Gasto por intereses neto de capitalizados: 222 (2025), 225 (2024), 239 (2023) [zoetis-10k-fy2025.txt, PDF p. 50]; seis meses de 2026 123 frente a 107 (+15%) [zoetis-10q-2026-q2.txt, PDF p. 29]. Ingresos por intereses (ajuste del resultado ajustado) 93 (2025), 106 (2024), 103 (2023) [zoetis-10k-fy2025.txt, PDF p. 54]. Discrepancia: el mismo 10-K 2025 da 105 para 2023 en la nota de impuestos [zoetis-10k-fy2025.txt, PDF p. 80]; 2025 y 2024 coinciden en ambas páginas (93 y 106). No hay forma de saber cuál es la correcta con estos textos.
- Covenant: línea de crédito renovable de 1.250 (ampliable a 1.750), vence en agosto de 2030, sin disponer; apalancamiento máximo (deuda neta consolidada / EBITDA) 3,50 a 1, sube a 4,00 a 1 tras una adquisición material durante cuatro trimestres; cumplido a 31-dic-2025 y 30-jun-2026 [zoetis-10k-fy2025.txt, PDF p. 57; zoetis-10q-2026-q2.txt, PDF p. 42]. Programa de papel comercial de hasta 1.000, sin saldo [zoetis-10k-fy2025.txt, PDF p. 85]. Otras líneas: 51 (2025) y 46 (30-jun-2026) [zoetis-10q-2026-q2.txt, PDF p. 42]. Los bonos obligan a recomprar al 101% en caso de cambio de control más rebaja bajo grado de inversión por ambas agencias [zoetis-10k-fy2025.txt, PDF p. 59].
- Rating: Moody's A3 estable, papel comercial P-2 (última acción enero de 2025); S&P BBB+ estable, A-2 (abril de 2025) [zoetis-10k-fy2025.txt, PDF p. 59; zoetis-10q-2026-q2.txt, PDF p. 44].
- Sensibilidad a tipos: +100 puntos básicos en SOFR añadirían unos 3 de gasto anual por los swaps de tipo fijo a variable (sobre los bonos 2028 al 3,900% y 2030 al 2,000%) [zoetis-10k-fy2025.txt, PDF p. 61].
- Arrendamientos a 31-dic-2025: pasivos operativos 52 corrientes y 196 no corrientes; financieros 1 y 6; total 255; plazo medio operativo 6,87 años; tasa de descuento 3,91% (operativos) y 4,97% (financieros) [zoetis-10k-fy2025.txt, PDF p. 89]. Pagos mínimos futuros operativos 285 (descontados 248) [zoetis-10k-fy2025.txt, PDF p. 89].
- Pensiones: obligación proyectada superior a activos del plan en 42 en 2025 y 2024; pasivo del plan complementario de ahorro 47 [zoetis-10k-fy2025.txt, PDF p. 91 y 59].
- Minoritarios: resultado atribuible a intereses minoritarios 0 en 2025, 10 en 2024, −4 en 2023 [zoetis-10k-fy2025.txt, PDF p. 48]. Patrimonio de minoritarios en balance: no encontrado en estas páginas; la historia de datos lo da como 0.
- Liquidez: caja 2.312 y circulante 4.533 a 31-dic-2025 en el 10-K [zoetis-10k-fy2025.txt, PDF p. 57]. Reexpresado en el 10-Q: caja 2.450 y circulante 4.600 a 31-dic-2025; 30-jun-2026 caja 1.476, inversiones a corto plazo 200, circulante 4.295 [zoetis-10q-2026-q2.txt, PDF p. 42]. Caja generada por explotación en seis meses: 1.056 frente a 1.120; financiación −1.653 [zoetis-10q-2026-q2.txt, PDF p. 41].
- Retornos al accionista en seis meses de 2026: compras de acciones propias pagadas 1.190 y dividendos 447 [zoetis-10q-2026-q2.txt, PDF p. 8].
- Controles de cambio y repatriación (China y otros) pueden limitar remesas [zoetis-10k-fy2025.txt, PDF p. 34].

## 7. Regulación y capital

No aplica: no es una entidad financiera. Sí hay una limitación relevante para la distribución: los instrumentos de deuda «pueden limitar la capacidad de pagar dividendos» sin cifra, y como sociedad holding depende de dividendos de filiales [zoetis-10k-fy2025.txt, PDF p. 39]. Ratio de capital exigido: no aplica.

## 8. Hechos medibles para predicciones

Último valor publicado y periodo:

- Ingresos T2 2026: 2.468 (T2 2025 reexpresado 2.474); T1 2026: 2.262 (T1 2025 2.198) [zoetis-10q-2026-q2.txt, PDF p. 27; zoetis-10q-2026-q1.txt, PDF p. 3].
- Ingresos por segmento T2 2026: EE. UU. 1.266; Internacional 1.173; animal de compañía 1.708 y ganado 731; contract manufacturing 29 [zoetis-10q-2026-q2.txt, PDF p. 33]. Animal de compañía EE. UU. T2: 1.044 frente a 1.176 (−11%); Internacional animal de compañía 664 (+5% operativo) [zoetis-10q-2026-q2.txt, PDF p. 33].
- Ingresos denominados en euros: 282 en T2 2026 y 545 en seis meses [zoetis-10q-2026-q2.txt, PDF p. 25–26].
- Beneficio neto T2 2026: 691; seis meses 1.292; ajustado 781 y 1.427 [zoetis-10q-2026-q2.txt, PDF p. 27]. BPA diluido T2 1,65; seis meses 3,08 [zoetis-10q-2026-q2.txt, PDF p. 3]. Tipo impositivo efectivo T2 20,2%; seis meses 20,4% [zoetis-10q-2026-q2.txt, PDF p. 32].
- Margen de coste de ventas T2: 27,3% (26,8% año anterior); SG&A 24% de ingresos; I+D 7% [zoetis-10q-2026-q2.txt, PDF p. 29].
- Acciones en circulación: 413.223.602 a 31-jul-2026 [zoetis-10q-2026-q2.txt, PDF p. 1] (422.127.709 a 6-feb-2026 [zoetis-10k-fy2025.txt, PDF p. 39]). Promedio diluido T2 2026: 417,7 millones [zoetis-10q-2026-q2.txt, PDF p. 3].
- Empleados a 31-dic-2025: unos 14.500 (6.800 en EE. UU.); fuerza de ventas 3.900; I+D 1.700 [zoetis-10k-fy2025.txt, PDF p. 20, 15 y 16]. Plantas propias 21; CMO más de 90; patentes concedidas más de 5.500 y solicitudes 1.600 en más de 50 países [zoetis-10k-fy2025.txt, PDF p. 28 y 17]. Unos 300 líneas de producto, ventas en más de 100 países, presencia directa en unos 45 [zoetis-10k-fy2025.txt, PDF p. 41].
- Ingresos por franquicia, T2 2026 (orgánico operativo frente al T2 2025): dermatología clave 395 (−16%); anticuerpos para el dolor artrósico 147 (−3%; caninos, Librela y Lenivia, 105, −8%; felinos 42, +12%); diagnóstico de compañía 118 (+12%); franquicia Simparica 442 (0%; Simparica Trio 350, −1%); [zoetis-2q2026-financial-results.txt, PDF p. 20]; ganado 731 (+11%) [zoetis-2q2026-financial-results.txt, PDF p. 15; zoetis-2q2026-earnings-call.txt, PDF p. 7].
- Margen bruto ajustado T2 2026: 72,9% (73,3% en el T2 2025) [zoetis-2q2026-financial-results.txt, PDF p. 16].
- Productos que superan el 1% de ingresos: suman un 71% de los ingresos de 2025 [zoetis-10k-fy2025.txt, PDF p. 14].
- Pérdidas de exclusividad con fecha: formulación de Excede en Japón hasta septiembre de 2026 y en Brasil hasta agosto de 2027; formulación inyectable de Cerenia hasta 2025–2028; Draxxin y Excede/Naxcel principio activo ya expirados [zoetis-10k-fy2025.txt, PDF p. 17].
- Cartera de pedidos, tiendas, clientes activos y unidades vendidas: no se publican.

## 9. Lo que no encontré

- Tamaño del mercado de salud animal en dólares y su crecimiento anual publicado por la empresa.
- Cuota de mercado de Zoetis en porcentaje, global o por región o especie (solo dos cuotas de clínica en EE. UU. del T2 2026: dermatología y Simparica Trio).
- Cuota de cada competidor (Boehringer Ingelheim, Merck, Elanco, IDEXX) y quién es el más peligroso.
- Guía de capex de 2026 (la guía del 6-ago-2026 no lo incluye).
- Capex previsto para 2026 y capex por destino con importes (solo «≈ 225 en fabricación, I+D e informática» (paráfrasis traducida) en seis meses, sin reparto).
- Importe y calendario de la planta de Atlanta, de la ampliación de Tullamore y de la de Lincoln.
- Precio y múltiplo de la adquisición de la genómica de Neogen, de Veterinary Pathology Group, de Basepaws y de VitalRADS.
- Fechas de pérdida de exclusividad de Simparica Trio, Apoquel, Cytopoint y Librela.
- Ingresos en dólares de cada producto (solo porcentajes de los dos primeros y de los cinco y diez primeros).
- Ventas de Librela sola en cifra (solo el total canino de Librela y Lenivia: 105 en el T2 2026).
- Margen en porcentaje por segmento en el 10-K (solo resultado en dólares; margen bruto por segmento solo en los 10-Q de 2026).
- Coste medio de la deuda publicado por la empresa y WACC o tasa de descuento propia.
- Apalancamiento real medido frente al covenant de 3,50 a 1.
- Perspectiva o acción de las agencias de calificación posterior a abril de 2025.
- Efecto en dólares de la alineación del año fiscal sobre ingresos de T1 2026.
- Causa de la caída de ingresos en China de 2023 a 2025.
- Cartera de pedidos, número de clientes, tiendas y unidades: no se publican.
- Ratios de capital regulatorio: no aplica (no financiera).
- Cifra correcta de ingresos por intereses de 2023: 103 en [zoetis-10k-fy2025.txt, PDF p. 54] frente a 105 en [zoetis-10k-fy2025.txt, PDF p. 80]; sin resolver.
