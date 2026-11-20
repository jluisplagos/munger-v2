# Extracto V6.3 · VINCI SA

Convenciones: cifras copiadas tal como las publica el informe, en millones de euros (€m) salvo que se diga otra cosa. URD 2025 = vinci-urd-2025.txt; URD 2024 = vinci-urd-2024.txt; URD 2023 = vinci-urd-2023.txt; semestral = vinci-hy-report-2026.txt (a 30-jun-2026, publicado antes de la fecha de análisis 2026-10-10). La información de los nueve meses de 2026 (22-oct-2026) no está en el expediente. En el semestral, la capa de texto de la prosa tiene palabras desordenadas; los cuadros se leen bien. No hay `etapa1/extracto.md` en el expediente: no se ha podido comprobar qué extrajo ya la etapa 1 (solo `etapa1/Vinci_respuesta.md`).

## 0. Vigencia de las cifras heredadas (vinci_b, Claude orquestación, 20-nov-2026)

Los textos heredados de la etapa 1 (sección 6 de `datos_v63.md`, `etapa1/Vinci_respuesta.md`, observaciones del Control maestro) **no se han tocado** y citan cifras que hoy valen otra cosa. Esta tabla da, para cada una, el valor vigente del expediente, su celda y su fuente. Manda la columna «vigente». Bloque añadido por la orquestación al extracto conservado de vinci/Vinci (rastro: `resultados/vigencia_extracto_vinci_b.json`); no es extracción nueva de las fuentes. Las cifras del motor A F1 son la previsión antes de la fase A.

| Cifra | Etapa 1 o vinci/Vinci (dónde la cita) | Vigente | Celda | Fuente |
|---|---|---|---|---|
| Precio (C37) | 107,05 € (C37; respuesta.md §1, C13, C20, B101); en vinci/Vinci «pendiente de verificación» (proveedores secundarios: Boursorama, ABC Bourse, MarketScreener) | 107,05 € sin cambio de valor, ahora con bytes: cierre del 9-oct-2026 en la exportación oficial de Euronext «Historical Data» entregada por la persona (fila «2026-10-09 \| 107.8 \| 108.1 \| 106.75 \| 107.05 \| 107.05»: cierre 107,05) | Análisis!C37 | [fuentes_mercado/VINCI_DG_FR0000125486_Euronext_historical_price_2024-11-20_a_2026-11-18.txt, PDF p. 1] (XLS original 78eee9c5…afb9d en la misma carpeta); coincide con el histórico no ajustado de Euronext conservado por Mistral |
| Tasa sin riesgo (C57) | 3,49 % (C57 del libro de la etapa 1; C56: «C57: 3,49 %»); 3,486 % de Investing.com (Control maestro fila 54 de la etapa 1; vinci/Vinci, 0,03486) | 3,47 % → 0,0347 (Bund a 10 años de la Bundesbank, serie WT1010, cierre del 9-oct-2026). Efecto: r mínima (Diagnóstico V6!C17 = C57 + riesgo país 4,2 % + Palancas D34) de 9,094 % a 9,078 %; diferencial de r = 0,09 sobre rf de 5,51 % a 5,53 % | Análisis!C57 | [fuentes_mercado/Bundesbank_WT1010_bund10y_diaria_hasta_2026-11-18.txt, PDF p. 1] (CSV oficial fef9498e…1967, Release, asset 766892543); contraste, no elegidas: UMU 9–10 años 3,46 % y curva AAA del BCE 3,5112 % (fuentes_mercado/, Mistral) |
| Capitalización (C41) | 59.043 mm (C41 de la etapa 1, con 551.548.982 acciones a 30-sep-2026) | 59.516,2774127 mm = 107,05 × 555,967094, producto exacto | Análisis!C41 | fase1_metadatos.json (capitalizacion); acciones: URD 2025 PDF p. 346. P-O2 (a) y Z-ACC: acciones al cierre del ejercicio con precio del 9-oct-2026, desalineación de fechas declarada |
| Acciones (C55) | 567,06 M (media ponderada diluida; respuesta.md §1: «división entre 567,06 millones de acciones diluidas») | 555,967094 M exactas (555.967.094 en circulación a 31-dic-2025: 581.816.830 emitidas − 25.849.736 de autocartera; sin dilución) | Análisis!C55 | URD 2025 PDF p. 346 |
| FCF base (C52) | 4.382 mm (respuesta.md §1 y §3, C13: «con la base normalizada de 4.382») | 4.419,333 mm = C46 9.327,333 − C47 3.799,667 − C48 89,333 − C49 675,333 − C50 343,667 (con C51 = Sí, que decide la fase A) | Análisis!C52 (fórmula) | C46–C50: medias exactas FY2023–2025 con cálculo declarado (fase1_v63.json; precedente E1) |
| Caja operativa del FCF base (C46) | 9.290 mm (C25: «C46 (9.290) está por debajo del flujo operativo») | 9.327,333 mm = media 2023–2025 de CFO (10.540 / 11.714 / 11.886) + fila 14 (−1.463 / −2.311 / −2.496: sin la entrada de circulante, M43) + dividendos de sociedades no consolidadas (31 / 41 / 40, P-O1 c) | Análisis!C46 | cálculo declarado (fase1_v63.json; URD 2024 PDF p. 348, URD 2025 PDF p. 370); es también lo que demuestra a F1-CIRC que la caja base excluye el circulante |
| SBC (C50) | 344 mm (C51) | 343,667 mm (media exacta 2023–2025) | Análisis!C50 | cálculo declarado (fase1_v63.json) |
| FCF LTM (C40) | 7.228 mm (C25: «C40 (7.228) no coincide con el FCF publicado de 2025 (7.010)») | 4.132 mm = 2025: CFO 11.886 + fila 14 (−2.496) + dividendos de no consolidadas 40 − capex D (3.873 − cobros 179 + PPP 311 = 4.005) − intereses de arrendamientos 110 − principal 761 − SBC 422 (misma definición que el FCF base) | Análisis!C40 | cálculo declarado (fase1_v63.json), conservado de vinci/Vinci (revisión del montaje, ee1ca6a); URD 2025 PDF p. 358, 359 y 370 |
| Rendimiento del FCF | 12,2 % (C13, «C41: 12,2 %», con C40 7.228); 7,4 % con la base 4.382 | 6,94 % (C40 ÷ C41); 7,43 % con la base (C52 ÷ C41) | C40 ÷ C41; C52 ÷ C41 | derivado de las filas anteriores |
| EV/EBITDA (C42) | 6,25x (C42 de la etapa 1) | 6,27964x = (59.516,277 + DFN 22.450 + arrendamientos 2.983 + minoritarios 3.654 − puesta en equivalencia 2.051) ÷ EBITDA LTM 13.783 | Análisis!C42 | semestral a 30-jun-2026 PDF p. 3 y 55; Z-ACC declarado |
| % de insiders (C96) | 0,09 % (C97: Huillard + Anjolras sobre 581,8 M emitidas) | 0,099 % = 550.233 acciones de los 15 consejeros ÷ 555.967.094 en circulación | Análisis!C96 | URD 2025 PDF p. 148 y 346 |
| Circulante en la reinversión del motor A (F1) | etapa 1: «el circulante aportó +2.311 en 2024 y +2.496 en 2025» (C25), «nivel normal de entrada de caja por circulante» (§2). vinci/Vinci (V6.3.1 F1, sin normalizar): f 4,4899 %, reinversión media −1.514,333, flujo sin crecimiento 3.016,069, ancla S2C 5,9595 (Historia C53 = Palancas F16); F1-K3c bloqueaba | vinci_b (V6.3.2 F1, normalización declarada «circulante_a_cero» 2021–2025; decisiones V-CIRC (a) y V-ANCLA (a)): la fila 14 sigue siendo la cifra publicada y no entra en la reinversión de 2021–2025 (filas 93–97); f ≈ 1,5744 %, reinversión media ≈ +575,667 (sin los 2.090 de circulante medio de 2023–2025 que la caja base ya excluye), flujo sin crecimiento ≈ 5.190,98, ancla S2C ≈ 2,3226; caja base sin cambio (C46 excluye ya el circulante, M43). Límite declarado: el capital del balance (ROIC y S2C medios de todo el capital, Historia C54–C55, P-FOSO) sigue incluyendo el circulante negativo | Historia C53, C58, C76, filas 30–31 y 93–97; Palancas F16 | motor_a_f1.json (normalizacion_circulante); previsión F1 del ensayo de la receta (F1_CIRCULANTE.md §6–§7 bis), comprobada con el libro de vinci_b en resultados/registro_vinci_b.json |
| Escenarios y precio de Sí | precio de Sí ≈ 79 €; normal ≈ 113–115 €; ponderado ≈ 115 €; malo ≈ 79 € (respuesta.md §1, C13, C20, B101, C104) | sin cifra vigente: son estimaciones de la etapa 1 hechas sin la hoja, con C52 = 4.382 y 567,06 M acciones; las calcula el libro (precio_de_si.py) tras la fase B con las palancas de este expediente | Análisis (escenarios) | — |

Sin cambio de valor frente a la etapa 1: C24 = 10,7 % (ROCE, URD 2025 PDF p. 142), C33 = 1,85x, C53 = 14.998 y C54 = 40.098 (semestral a 30-jun-2026), verificados en la revisión del registro de entradas; C26 = 2,31 y C60 = −0,002 se reproducen con la Historia (clase corregida en el registro); C38 = 111,79 € (Simply Wall St) es una lectura externa sin bytes y C88 = 9,7x una convención de la etapa 1 sin precios conservados: ninguna de las dos cuenta como comprobada.

## 1. Mercado y cuota

- Red de autopistas en concesión en Francia (sociedades controladas, «internal studies, company literature»): VINCI Autoroutes 4.443 km, Eiffage 2.560 km, Abertis 1.807 km [vinci-urd-2025.txt, PDF p. 12].
- Ingresos de VINCI Autoroutes por red en 2025: ASF 3.929 (58 %), Cofiroute 1.684 (25 %), Escota 961 (14 %), otras 159 (2 %) [vinci-urd-2025.txt, PDF p. 12].
- Posición declarada sin cifra de cuota: «VINCI is a world leader in concessions» [vinci-urd-2025.txt, PDF p. 19]; VINCI Airports «the leading private» operador aeroportuario [vinci-urd-2025.txt, PDF p. 11].
- Pasajeros de los aeropuertos gestionados por el grupo (al 100 %): 334 millones en 2025, +5,0 % frente a 2024 [vinci-urd-2025.txt, PDF p. 134]; más de 159 millones en el primer semestre de 2026, «stable» [vinci-hy-report-2026.txt, PDF p. 8].
- Mercados de Energy Solutions descritos por la empresa sin cifra de tamaño: electrificación, inteligencia artificial y centros de datos, digitalización de procesos industriales y de edificios, defensa y soberanía [vinci-urd-2025.txt, PDF p. 135].
- Tamaño del mercado, crecimiento del mercado y cuota en euros o en porcentaje de cualquier negocio: No encontrado en los documentos.

## 2. Economía por segmento y geografía

Ingresos por línea de negocio (2025 / 2024; variación real y a perímetro comparable) [vinci-urd-2025.txt, PDF p. 134]:
- Concesiones 12.219 / 11.651 (+4,9 %; +3,9 %): VINCI Autoroutes 6.733 / 6.585 (+2,3 %); VINCI Airports 4.796 / 4.526 (+6,0 %; +5,8 %); otras concesiones 690 / 540 (+27,8 %; +7,9 %).
- Energy Solutions 29.612 / 27.478 (+7,8 %; +5,8 %): VINCI Energies 21.608 / 20.373 (+6,1 %; +3,3 %); Cobra IS 8.004 / 7.105 (+12,7 %; +12,9 %).
- Construcción 33.241 / 32.927 (+1,0 %; −0,4 %): VINCI Construction 32.137 / 31.784 (+1,1 %; −0,3 %); VINCI Immobilier 1.105 / 1.143 (−3,3 %).
- Total «Revenue» 74.599 / 71.623 (+4,2 %; +2,6 %): crecimiento orgánico 2,6 %, perímetro +2,5 %, tipo de cambio −1,0 % [vinci-urd-2025.txt, PDF p. 130].

Resultado de explotación de las actividades ordinarias (Ebit) y margen sobre ventas (2025 / 2024) [vinci-urd-2025.txt, PDF p. 136]:
- Concesiones 5.935 (48,6 %) / 5.688 (48,8 %): VINCI Autoroutes 3.311 (49,2 %) / 3.265 (49,6 %); VINCI Airports 2.459 (51,3 %) / 2.334 (51,6 %); otras 164 / 90.
- Energy Solutions 2.250 (7,6 %) / 2.027 (7,4 %): VINCI Energies 1.606 (7,4 %) / 1.474 (7,2 %); Cobra IS 644 (8,0 %) / 553 (7,8 %).
- Construcción 1.356 (4,1 %) / 1.247 (3,8 %): VINCI Construction 1.353 (4,2 %) / 1.304 (4,1 %); VINCI Immobilier 3 (0,3 %) / (57) (−5,0 %).
- Holdings 16 / 35; total 9.558 (12,8 %) / 8.997 (12,6 %). El Ebit de holdings incluye 38 de amortización de los intangibles de la compra de Cobra IS (28 en 2024, con una reversión de provisiones) [vinci-urd-2025.txt, PDF p. 137].

Ebitda (flujo de las operaciones antes de impuestos y financiación) por negocio, 2025 / 2024 [vinci-urd-2025.txt, PDF p. 140]: Concesiones 8.169 (66,9 %) / 7.773; VINCI Autoroutes 4.784 (71,0 %) / 4.662; VINCI Airports 3.042 (63,4 %) / 2.883; Energy Solutions 2.805 (9,5 %) / 2.496; VINCI Energies 2.019 (9,3 %) / 1.794; Cobra IS 786 (9,8 %) / 702; Construcción 2.194 (6,6 %) / 1.988; holdings 339 / 432; total 13.507 (18,1 %) / 12.689 (17,7 %).

Resultado neto atribuido por negocio, 2025 / 2024 [vinci-urd-2025.txt, PDF p. 138]: Concesiones 2.951 / 2.726 (VINCI Autoroutes 1.760 / 1.833; VINCI Airports 1.140 / 947); Energy Solutions 1.253 / 1.159; Construcción 827 / 792; holdings (128) / 187; total 4.903 / 4.863.

Flujo de caja libre por negocio, 2025 / 2024 [vinci-urd-2025.txt, PDF p. 139]: Concesiones 3.890 / 3.554; Energy Solutions 1.204 / 1.575; Construcción 1.710 / 821; holdings 206 / 859; total 7.010 / 6.808. VINCI Autoroutes 2,6 mil millones; VINCI Airports 1,2 mil millones; VINCI Energies 1,6 mil millones; Cobra IS −365; VINCI Construction 1,4 mil millones, «a particularly high level of cash inflows from customers at the end of the year» [vinci-urd-2025.txt, PDF p. 140].

Capital empleado a 31-dic-2025: grupo 58,2 mil millones (59,4 a finales de 2024); Concesiones 46,3 (80 %), de los que VINCI Airports 24,1 y VINCI Autoroutes 16,6; Energy Solutions 9,5 (Cobra IS 5,3; VINCI Energies 4,1); Construcción 1,9 (VINCI Immobilier 1,1; VINCI Construction 0,8); excedente neto de circulante 19,7 mil millones [vinci-urd-2025.txt, PDF p. 141]. ROCE 10,7 % en 2025 (11,4 % en 2024; 11,6 % sin la contribución excepcional) y ROE 16,4 % (17,3 %) [vinci-urd-2025.txt, PDF p. 142].

Reparto geográfico de los ingresos 2025 (importe, % del total, variación real y a tipo de cambio constante) [vinci-urd-2025.txt, PDF p. 136]: Francia 30.787 (41,3 %; +2,0 %; +2,0 %); Reino Unido 7.362 (9,9 %; +9,9 %; +11,3 %); Alemania 6.485 (8,7 %; +16,8 %); España 3.780 (5,1 %; −0,6 %); Europa central y del este 3.297 (4,4 %; +4,8 %; +3,6 %); resto de Europa 7.587 (10,2 %); Norteamérica 5.434 (7,3 %; −1,2 %; +5,1 %), de los que EE. UU. 3.437 y Canadá 1.998; Centro y Sudamérica 4.294 (5,8 %; +1,7 %; +5,2 %); África 1.768 (2,4 %); resto del mundo 3.805 (5,1 %; −5,4 %; −0,2 %). La nota 2 desglosa «Rest of Europe» en Portugal 1.855 y resto 5.732 [vinci-urd-2025.txt, PDF p. 369].

Primer semestre de 2026 [vinci-hy-report-2026.txt, PDF p. 7, 9 y 10]: ingresos 35.597 (+2,1 % real; +1,3 % comparable); Concesiones 5.833 (VINCI Autoroutes 3.149, −0,7 %; VINCI Airports 2.294, +1,8 %); Energy Solutions 14.573 (+6,8 %; VINCI Energies 10.717; Cobra IS 3.855); Construcción 15.456 (−1,3 %). Ebit 4.363 (12,3 %): VINCI Autoroutes 1.617 (51,4 %), VINCI Airports 1.153 (50,3 %), VINCI Energies 807 (7,5 %), Cobra IS 323 (8,4 %), VINCI Construction 327 (2,2 %). Francia 14.717 (41,3 %, −1,3 %); fuera de Francia 20.880 (+4,7 %; +5,9 % a tipo constante).

## 3. Capacidad, capex e inversión

- Inversiones operativas netas de cesiones 2025: 2.832 (2.708 en 2024), de las que VINCI Construction 881 (921) y Cobra IS 1.232 (1.220), con 852 en proyectos de energía renovable (637) [vinci-urd-2025.txt, PDF p. 140].
- Inversiones de crecimiento en concesiones y PPP 2025: 1.173 (1.453 en 2024): VINCI Autoroutes 565 (604), VINCI Airports 263 (445; OMA y aeropuertos de Amazonia), Cobra IS 327 (349; líneas de alta tensión PPP en Brasil) [vinci-urd-2025.txt, PDF p. 140]. Primer semestre de 2026: 723 (626), VINCI Autoroutes 206, Cobra IS 199, VINCI Airports 238 [vinci-hy-report-2026.txt, PDF p. 14].
- Inversiones financieras 2025, netas de cesiones e incluida la deuda neta de lo adquirido: casi 1,9 mil millones (Concesiones 0,4; VINCI Energies 0,4; VINCI Construction 0,7; VINCI SA 0,3 por el saldo del earn-out de Cobra IS); 7,0 mil millones en 2024 (prórroga de 30 años de Aerodom, 50,01 % de Edimburgo, 20 % de Budapest, Northwest Parkway) [vinci-urd-2025.txt, PDF p. 140].
- Precios de compras de 2024 publicados: Northwest Parkway 1.156 más 276 de deuda financiera neta; aeropuerto de Edimburgo 1.431 más 1.364; aeropuerto de Budapest 618 [vinci-urd-2025.txt, PDF p. 370]. OMA (2022): 1.169 por las acciones más 298 de deuda neta [vinci-urd-2023.txt, PDF p. 170]. No se publican múltiplos de compra en esos pasajes.
- Earn-out de Cobra IS fijado en 380 en efectivo frente a un tope de 600; el resto, 300, se pagó en septiembre de 2025 [vinci-urd-2025.txt, PDF p. 132].
- Compras de 2025: VINCI Energies, 33 sociedades con casi 700 de ventas anuales; VINCI Construction, FM Conway (unos 700 de ventas), Hub Foundation (unos 65), Peters Bros (unos 60) y Marsein [vinci-urd-2025.txt, PDF p. 131]. Precio no publicado en esos pasajes.
- 2026: acuerdo para comprar Safeway Concessions (nueve autopistas de peaje en India, casi 700 km, vencimientos 2048–2058); preferido para la concesión A154–A120 (97 km, 35 años) [vinci-hy-report-2026.txt, PDF p. 4]; Fletcher Construction (unas ventas de 630) y Modern Group (50) [vinci-hy-report-2026.txt, PDF p. 5]; oferta por All for One a 67,50 € por acción (500 de ventas en 2025) [vinci-hy-report-2026.txt, PDF p. 17].
- Zero.e (renovables de Cobra IS): más de 5,0 GW en operación, construcción o listos para construir; 1,2 GW en operación en 2025 [vinci-urd-2025.txt, PDF p. 133]; 1,6 GW en operación y 4,0 GW en construcción o listos a mediados de 2026; capital invertido en renovables desde finales de 2021: 2,6 mil millones a 30-jun-2026 [vinci-hy-report-2026.txt, PDF p. 5–6].
- Programas de inversión de concesiones: OMA, plan maestro 2026–2030 de unos 800 [vinci-urd-2025.txt, PDF p. 132]; Cabo Verde, 142 en tres años; ampliación de la segunda pista de Gatwick aprobada, hasta 80 millones de pasajeros [vinci-urd-2025.txt, PDF p. 132]; adenda de Cofiroute, unos 350 de inversiones financiadas con subidas de peaje [vinci-urd-2025.txt, PDF p. 143]; A57 en Toulon, 300 financiados por Escota [vinci-urd-2025.txt, PDF p. 132].
- Plan climático: «over €1.5 billion» de CapEx en 2026–2030, financiado sobre todo con recursos propios de los negocios [vinci-urd-2025.txt, PDF p. 231].
- Obligaciones de compra e inversión fuera de concesiones: 1.671 a 31-dic-2025, de las que 1.221 de renovables de Cobra IS [vinci-urd-2025.txt, PDF p. 396].
- I+D (importe y % de ventas): No encontrado en los documentos (las cuentas consolidadas no publican el gasto).

## 4. Precios y poder de fijación

- OMA: subidas de tarifas de «reference inflation rate plus 6.9% over the period» 2026–2030, aprobadas con el plan maestro [vinci-urd-2025.txt, PDF p. 132].
- Cofiroute: los peajes subirán al 83 % de la inflación de referencia hasta el final de la concesión (antes 70 %), más subidas adicionales para vehículos ligeros de 0,472 % el 1-feb-2026 y 0,173 % al año de 2027 a 2030 [vinci-urd-2025.txt, PDF p. 143].
- Concesiones: «price increases must be validated by the grantor» y la remuneración sigue la ley de tarifas del contrato [vinci-urd-2025.txt, PDF p. 382].
- VINCI Airports: el aumento del Ebit de 2025 «reflects an increase in revenue per passenger» [vinci-urd-2025.txt, PDF p. 136] (sin cifra).
- Northwest Parkway: peaje variable día/noche desde finales de 2024, «leading to an increase in revenue» [vinci-urd-2025.txt, PDF p. 132].
- La dirección dice que el semestre «reflects the ability of Group companies to pass on inflation» [vinci-hy-report-2026.txt, PDF p. 3] (afirmación, sin cifra).
- Tráfico y precio: VINCI Autoroutes, tráfico +0,9 % en 2025 (ligeros +0,9 %, pesados +0,7 %) e ingresos +2,3 % [vinci-urd-2025.txt, PDF p. 134]; primer semestre de 2026, tráfico −2,9 % (ligeros −3,7 %, pesados +1,6 %) e ingresos −0,7 % [vinci-hy-report-2026.txt, PDF p. 7].
- Subidas anuales de peaje de ASF y Escota en porcentaje: No encontrado en los documentos.

## 5. Guía y objetivos de la dirección

- Guía 2025 (confirmada en octubre de 2025): tráfico de VINCI Autoroutes ligeramente al alza; pasajeros al alza a menor ritmo; VINCI Energies crecimiento similar al de 2024 con margen al menos estable; Cobra IS ventas de al menos 7,5 mil millones; capacidad renovable de unos 5 GW; VINCI Construction ventas cercanas a 2024 con mejor margen; ventas y beneficios al alza antes del impuesto francés. Resultado: «Those trends have been confirmed and the performance targets have been achieved or exceeded» [vinci-urd-2025.txt, PDF p. 143].
- Guía 2026 (febrero de 2026), «assuming no change in taxation»: «further growth in its revenue, operating earnings and net income»; flujo de caja libre «as an initial estimate, that could reach €6 billion», con capex de Zero.e similar al de 2025 (0,9 mil millones); Energy Solutions crecimiento de un dígito medio-alto con mejor margen; Construcción ventas similares con margen al menos igual; Zero.e de 5 GW a unos 6 GW; Ebitda de Zero.e por encima de 400 en 2030 [vinci-urd-2025.txt, PDF p. 144].
- Guía 2026 confirmada en el semestral (julio de 2026), con dos ajustes en Concesiones: pasajeros estables frente a 2025 (antes, al alza) y tráfico de autopistas francesas «may decline slightly» (antes, según la economía) [vinci-hy-report-2026.txt, PDF p. 17].
- Dividendo: 5,00 € por acción por 2025 (4,75 por 2024), con un final de 3,95 € [vinci-urd-2025.txt, PDF p. 142]; dividendo a cuenta de 2026 de 1,10 € pagadero el 15-oct-2026, fecha ex 13-oct-2026 [vinci-hy-report-2026.txt, PDF p. 18].
- Impuestos franceses: la contribución excepcional del impuesto de sociedades se prorroga en 2026 y el grupo espera «a charge in 2026 of the same magnitude as that recorded in 2025» [vinci-urd-2025.txt, PDF p. 143]; 323 en el primer semestre de 2026, 70 % del gasto anual estimado [vinci-hy-report-2026.txt, PDF p. 12].

## 6. Financiación

- Deuda financiera neta: 19.075 a 31-dic-2025 (20.415 en 2024), 1,4 veces el Ebitda; 22.450 a 30-jun-2026, 1,6 veces [vinci-urd-2025.txt, PDF p. 141] [vinci-hy-report-2026.txt, PDF p. 15].
- Deuda neta por negocio a 31-dic-2025 (total; externa; deuda/Ebitda): Concesiones (29.124); (21.412); 3,6x; VINCI Autoroutes (15.001); (11.057); 3,1x; VINCI Airports (10.542); (9.056); 3,5x; Energy Solutions +1.718; Construcción +3.801; holdings +4.530 [vinci-urd-2025.txt, PDF p. 141]. A 30-jun-2026: Concesiones (28.353), 3,4x; VINCI Autoroutes (14.677), 3x; VINCI Airports (10.450), 3,4x [vinci-hy-report-2026.txt, PDF p. 16].
- Deuda financiera bruta 36.712 a 31-dic-2025: vencimientos de principal de bonos 2.980 (<1 año), 2.940 (1–2), 9.900 (2–5), 12.672 (>5); otros préstamos 300 / 1.206 / 1.903 / 2.152 [vinci-urd-2025.txt, PDF p. 404]. Vida media de la deuda a largo plazo 5,5 años (6,4 en Concesiones, 3,6 en Energy Solutions, 8,5 en Construcción, 3,8 en holdings) [vinci-urd-2025.txt, PDF p. 404].
- Coste medio de la deuda a largo plazo: 4,4 % en 2025 (4,9 % en 2024) [vinci-urd-2025.txt, PDF p. 133]; 4,5 % en el primer semestre de 2026; parte a tipo fijo 45 % [vinci-hy-report-2026.txt, PDF p. 6].
- Calificaciones a 31-dic-2025: VINCI SA y ASF, S&P A− y Moody’s A3, estables; Cofiroute S&P A−; Gatwick Funding BBB+ / Baa1 / BBB+ [vinci-urd-2025.txt, PDF p. 405]. Confirmadas en el primer semestre de 2026 [vinci-hy-report-2026.txt, PDF p. 6].
- Covenants: cláusulas en algunas financiaciones (cobertura de deuda, cobertura de intereses, deuda neta/Ebitda); a finales de 2025 «all ratios were complied with» [vinci-urd-2025.txt, PDF p. 405].
- Liquidez: 22,0 mil millones a 31-dic-2025 (15,5 de caja neta gestionada y 6,5 de línea confirmada sin usar hasta enero de 2031) [vinci-urd-2025.txt, PDF p. 141]; 18,0 a 30-jun-2026 [vinci-hy-report-2026.txt, PDF p. 15].
- Pasivos por arrendamiento: 2.849 a 31-dic-2025 (737 a menos de un año, 795 entre 1 y 2, 700 entre 2 y 5, 617 a más de 5); inmuebles 1.744 y bienes muebles 1.105 [vinci-urd-2025.txt, PDF p. 396]; 2.983 a 30-jun-2026 [vinci-hy-report-2026.txt, PDF p. 55].
- Pensiones: provisiones por obligaciones de jubilación 1.134 a 31-dic-2025 (1.074 a más de un año y 60 a menos) y otras prestaciones a largo plazo 95 [vinci-urd-2025.txt, PDF p. 415].
- Minoritarios: 3.576 a 31-dic-2025 (4.085 en 2024); participaciones materiales en London Gatwick y Edimburgo (49,99 % no de VINCI) y OMA (70,01 % no de VINCI) [vinci-urd-2025.txt, PDF p. 399]. Dividendos pagados a minoritarios 805 en 2025 (902 en 2024) [vinci-urd-2025.txt, PDF p. 358].
- Nueva financiación 2026: 1,8 mil millones al 3,2 % medio; bonos canjeables en acciones de Groupe ADP de 500 al 0,75 % (la participación en ADP bajaría a un 4,8 % si se canjean todos) [vinci-hy-report-2026.txt, PDF p. 6].

## 7. Regulación y capital

- VINCI no es una financiera: no hay ratios de capital regulatorio.
- Fin de las concesiones principales: ASF 2036 (2.730 km), Escota 2032 (471 km), Cofiroute red interurbana 2034 (1.100 km), A86 Duplex 2086, Arcour y Arcos 2070; aeropuertos: ANA 2062, OMA 2048, Aerodom 2060, Lyon 2047, Belgrado 2045; Gatwick y Edimburgo en plena propiedad [vinci-urd-2025.txt, PDF p. 382] [vinci-urd-2025.txt, PDF p. 9].
- Escota: programa de mantenimiento y renovación para el buen estado de la infraestructura al final del contrato (febrero de 2032), aprobado por el Estado [vinci-urd-2025.txt, PDF p. 132].
- Impuesto francés sobre los operadores de infraestructuras de transporte de larga distancia (TEITLD): aplicado desde 2024, impacto negativo de 284 en 2024, «almost exclusively targets motorway concession companies»; el grupo litiga [vinci-urd-2024.txt, PDF p. 134].
- Contribución excepcional del impuesto de sociedades: 449 en el resultado de 2025 (ASF y Cofiroute 261, VINCI SA 188) y 425 en el flujo libre [vinci-urd-2025.txt, PDF p. 138]; prorrogada en 2026 [vinci-urd-2025.txt, PDF p. 143].
- Adenda de Cofiroute (enero de 2026): compensa la subida de la tasa TAT de 2020 tras una sentencia de mayo de 2025 [vinci-urd-2025.txt, PDF p. 143].
- Límites regulatorios a la distribución de dividendos: No encontrado en los documentos.

## 8. Hechos medibles para predicciones

- Tráfico de VINCI Autoroutes: +0,9 % en 2025 [vinci-urd-2025.txt, PDF p. 134]; −2,9 % en el primer semestre de 2026 [vinci-hy-report-2026.txt, PDF p. 7].
- Pasajeros de VINCI Airports (al 100 %): 334 millones en 2025 [vinci-urd-2025.txt, PDF p. 134]; más de 159 millones en el primer semestre de 2026 [vinci-hy-report-2026.txt, PDF p. 8].
- Cartera de pedidos de Energy Solutions y VINCI Construction: 69,8 mil millones a 31-dic-2025 (VINCI Energies 17,5; Cobra IS 18,1; VINCI Construction 34,2), 71 % fuera de Francia, 14 meses de actividad [vinci-urd-2025.txt, PDF p. 144]; 76,8 mil millones a 30-jun-2026 (VINCI Energies 20,0; Cobra IS 18,3; VINCI Construction 38,5) [vinci-hy-report-2026.txt, PDF p. 16].
- Contratación: 63,0 mil millones en 2025 (VINCI Energies 22,3; Cobra IS 8,6; VINCI Construction 32,1) [vinci-urd-2025.txt, PDF p. 132]; 34,4 mil millones en el primer semestre de 2026 [vinci-hy-report-2026.txt, PDF p. 4].
- Márgenes Ebit por negocio (sección 2) y Ebitda por negocio [vinci-urd-2025.txt, PDF p. 136 y 140] [vinci-hy-report-2026.txt, PDF p. 10 y 14].
- Flujo de caja libre: 7.010 en 2025 [vinci-urd-2025.txt, PDF p. 139]; 264 en el primer semestre de 2026 (la mayor parte se genera en el segundo semestre) [vinci-hy-report-2026.txt, PDF p. 4 y 13].
- Capacidad renovable de Zero.e (GW en operación y en construcción o listos): sección 3.
- VINCI Immobilier: reservas en Francia 4.177 viviendas en 2025 (−13 %) [vinci-urd-2025.txt, PDF p. 135]; 1.749 en el primer semestre de 2026 (−16 %) [vinci-hy-report-2026.txt, PDF p. 9].
- Recompras: 16,6 millones de acciones en 2025 a 119,11 € de media (1.977) [vinci-urd-2025.txt, PDF p. 141]; 7,9 millones a 125,80 € en el primer semestre de 2026 (998) [vinci-hy-report-2026.txt, PDF p. 15]. Acciones emitidas 585.891.697 a 30-jun-2026; autocartera 5,4 % del capital (4,4 % a 31-dic-2025) [vinci-hy-report-2026.txt, PDF p. 15].
- Empleados accionistas: los fondos de empleados tienen el 11,26 % del capital [vinci-urd-2025.txt, PDF p. 397].

## 9. Lo que no encontré

- Tamaño del mercado, crecimiento del mercado y cuota de mercado en euros o en porcentaje (solo la comparación de kilómetros de red en Francia).
- Gasto de investigación y desarrollo (importe y % de ventas).
- Subidas anuales de peaje de ASF y Escota en porcentaje.
- Ingresos por pasajero o tasas aeroportuarias por aeropuerto.
- Deuda, flujos y obligaciones de fin de contrato concesión por concesión (solo VINCI Autoroutes y VINCI Airports agregados).
- Múltiplos de compra de las adquisiciones.
- Márgenes por segmento a tipo de cambio constante.
- Límites regulatorios a la distribución de dividendos.
- Calendario anual de la inversión del plan climático 2026–2030.
