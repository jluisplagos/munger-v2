# Elis SA · fase B (palancas) · motor A · plantilla V6.3 · base 31-dic-2025

Las referencias mecánicas son convención del ejercicio (`referencias_mecanicas.json`, v0.2.1), no estimaciones de Damodaran. Millones de euros. Fuentes como en la fase A: URD2025, DEU2024 (en francés, citado traducido), URD2023, URD2022, URD2021, URD2020, URD2019, RD2018, RD2017, Doc2016, H1-2026; celdas de `datos_v63.md`. Lo comprado y lo orgánico van separados en cada ancla; el lino y los artículos propios que Elis alquila (inmovilizado, capex de caja) nunca se mezclan con los derechos de uso NIIF 16 (activos que Elis arrienda, cuyo coste ya está en f como pago de arrendamientos).

## Aviso previo para la fase C: el motor A arranca por debajo del FCF base

f = 0,0417 (Historia C58) se calibra con la reinversión orgánica de la Historia (fila 30: −47,6 / −70,8 / −125,2 en 2023–25; reproduzco C58 con ella, cálculo propio). Es negativa porque la D&A de 2025 (1.019,4) incluye 149,5 de derechos de uso y 85,7 de intangibles de compras que el capex no repone [URD2025, PDF p. 350]. Con crecimiento cero el motor supone capex = D&A, así que su flujo de partida es V0·[m0·(1 − τ) − f] = 4.796,8 × (0,1313 × 0,7118 − 0,0417) = 248,6, frente a C52 = 308, antes de cobrar ninguna reinversión. Ningún S2C > 0 lo corrige y no lo compenso: tendría que meter los derechos de uso en el S2C. El valor que salga estará sesgado a la baja en los tres escenarios. No es L1, L2 ni L3 (C52 > 0, C6 = Ninguno): `limite_del_modelo.aplica = false`, y la fase C decide si es material.

## Crecimiento de ventas, años 1–5 (B14:D14)

- **MALO 0,02** (ref. −0,08; +0,10). La referencia nace de una σ de 19,3 % inflada por Berendsen y 2020 y describe perder un tercio de las ventas, algo que ni la pandemia hizo (orgánico −13,3 % y +7,4 % al año siguiente [URD2020, PDF p. 155; URD2021, PDF p. 211]). Por componentes: orgánico 1,5 % (el bajo de 2016–2018, 2,4 % [RD2017, PDF p. 187; RD2018, PDF p. 154], menos contratos perdidos por precio y Hostelería plana) + 0,5 % comprado (suelo del presupuesto de 50 mm [URD2025, PDF p. 394]).
- **NORMAL 0,045** (ref. 0,115; −0,07). La referencia es el CAGR desde el valle de 2020, con precio de más del 8 % y del 9 % en 2022–23 [URD2023, PDF p. 114, 261] y 691,5 de compras (Historia H13:L13): no se repite (PCA pp.548–549; GV p. 19; E4). Orgánico 3,0 % (2,4–3,3 % en 2016–2019, 3,8 % en 2025 [URD2025, PDF p. 307], 3,2 % en H1-2026 [H1-2026, PDF p. 5]) + 1,5 % comprado (externo +1,8 % en 2025, +1,1 % en H1-2026) + divisa 0 (−0,7 % y +0,6 %). Lo comprado se cobra en el S2C porque C52 no resta adquisiciones.
- **BUENO 0,055** (ref. 0,135; −0,08). Orgánico 4,0 % donde avanza la externalización (Europa del Sur +6,7 %, Latinoamérica +8,2 % en 2025 [URD2025, PDF p. 307]) + 1,5 % comprado. Sin inflación, el orgánico no pasó del 3,8 %.

## Margen operativo objetivo, año 5 (B15:D15), en la definición de la Historia (EBIT contable)

- **MALO 0,105** (ref. 0,095; +0,01). Retrocede a mitad de camino entre el 12,6 % subyacente de 2025 y el 8,6–9,7 % de 2021–22 (Historia H29, I29): −2,1 puntos. La referencia, media de diez años, mezcla perímetros y la pandemia. Personal 2.026,5 [URD2025, PDF p. 344] y salarios fijados por el Estado en Latinoamérica (−130 pb [URD2025, PDF p. 308]): la mejora va al cliente y al empleado.
- **NORMAL 0,125** (ref. 0,13; −0,005). C8 = Último año toma 2025, máximo de la serie; no lo corrijo, pero no me apoyo en él: el 13,13 % lleva +25,7 de plusvalía por bajas de inmovilizado [URD2025, PDF p. 350] (MR p. 37; E8). Sin partidas puntuales, 2023–25 dan 12,7 / 12,8 / 12,6 % [DEU2024, PDF p. 296; URD2025, PDF p. 350] y la NIIF 2 subió a 45,9 [URD2025, PDF p. 313]. Es el EBIT ajustado plano (15,85 / 16,02 / 15,98 % [DEU2024, PDF p. 291; URD2025, PDF p. 345]) traducido. No cuento la caída de la amortización de relaciones con clientes (valor neto 275,1 [URD2025, PDF p. 364]): sube el margen contable sin caja.
- **BUENO 0,135** (ref. 0,13; +0,005; G5 justificada). +0,9 puntos en cinco años sobre el 12,6 %, menos que el ritmo de 2016–2025 (EBITDA ajustado de 30,9 % a 35,4 %, 2,1 puntos de ellos por NIIF 16 [Doc2016, PDF p. 165; URD2019, PDF p. 146; URD2025, PDF p. 307]). Mecanismo: escala local (Francia 22,3 % de EBIT ajustado frente a 9,7 % en Reino Unido [URD2025, PDF p. 344]; Alemania +450 pb en 2024 [DEU2024, PDF p. 254]). Se la queda Elis en los clientes pequeños [URD2025, PDF p. 50]; en Sanidad, el cliente: «how much is going to stay home and how much is just going to flow through to the customer» (PCA pp.187–189; HIM).

## Ventas por euro reinvertido, S2C (B16:D16)

Anclas separadas. Orgánico: en 2024–25, 258,2 de inversión en activos propios por encima de su amortización (lino y otros artículos +89,6; resto del capex +157,7) más circulante (+10,9) para ≈397,9 de ventas orgánicas nuevas: 1,5 [URD2025, PDF p. 311, 350, 367; DEU2024, PDF p. 253]; 2021–25 da 3,1 con la reapertura de plantas y el precio de 2022–23. Comprado: 0,89 al precio (220,7 por 195,8 de ventas anuales [URD2025, PDF p. 340, 342]) y 0,65 en caja (300,9, Historia K13:L13). C53 = 9,04 no lo copio: parte de 2020.

- **MALO 1,0** (ref. 0,8; +0,2). Orgánico 1,2 (parte del lino repone volumen perdido) y comprado 0,65. Rentabilidad marginal 7,5 %, bajo r.
- **NORMAL 1,2** (ref. 1,0; +0,2; G7 justificada). Orgánico 1,5 y comprado 0,8: 1,16. Rentabilidad marginal 10,7 % > 9,46 % porque C55 (4,7 %) mide el capital total con un fondo de comercio del 42,2 % del activo (C32). Depende de leer que el capital orgánico rinde más que el total (C18, lectura dudosa de la fase A).
- **BUENO 1,5** (ref. 1,0; +0,5; G7 justificada). Orgánico 2,0 llenando las plantas de 2025 [URD2025, PDF p. 19] y comprado 0,9. Rentabilidad marginal 14,4 %, bajo el ≈23 % antes de impuestos del capital tangible (Análisis C24). Misma dependencia de C18.

## g para siempre (B68:D68)

- **MALO 0,01 · NORMAL 0,02 · BUENO 0,025** (ref. 0,015 / 0,025 / 0,03; −0,005 en los tres; mantienen la etapa 1). A perpetuidad no cuento compras, y el orgánico de los años normales (2,4–3,3 %, precio y volumen juntos [Doc2016, PDF p. 150; URD2019, PDF p. 145]) se modera al madurar la externalización. El MALO no tiene precio real; el BUENO, medio punto más: «most big businesses eventually fall into mediocrity or worse» (AIWTK p.140; HIM). Los tres bajo rf (3,29 %, C57) (CV p. 5; E1). Contraste del NORMAL: 1,02 ÷ 0,07 ≈ 14,6x, la mediana del P/FCF (C88).

## ROIC a largo plazo (B18:D18)

- **MALO 0,07** (ref. 0,09; −0,02). El foso se estrecha y el capital nuevo rinde como hoy el total con sus compras (C55 = 4,7 %; compras de 2024–25 ≈5–7 % después de impuestos [URD2025, PDF p. 340, 342]). Sin salto en el año 11 (7,5 % → 7 %).
- **NORMAL 0,10** (ref. 0,09; +0,01). La fase A limita el foso al capital orgánico: 10 % mezcla ≈13 % orgánico y ≈7 % comprado; un punto sobre r (MR p. 63; E2). Si C18 no se sostiene, 0,09. Salto ≈ +0,7 puntos.
- **BUENO 0,12** (ref. 0,09; +0,03). El máximo que el criterio admite a perpetuidad (MR p. 63; E2), aplicado como criterio; no más, porque la ventaja se renueva contrato a contrato cada cuatro años [URD2025, PDF p. 141]: «The question of how long your period in the sun will be is a very good one» (AIWTK p.127; HIM). Salto ≈ +2,4 puntos, mi hipótesis de pérdida parcial de ventaja.

## Probabilidades, quiebra, caja, mercado, FCF normalizado

- **0,2 / 0,6 / 0,2** (convención, argumentada). Centro estrecho (EBIT ajustado 15,85–16,02 %) y colas con mecanismo a los dos lados; subir el MALO castigaría dos veces lo que ya llevan sus palancas (PA pp. 20–21; E6). Brasil y una recesión como la de 2020 quedan fuera, y lo digo.
- **Quiebra 0,05, recuperación 0** (convención con disparadores). C34 = No (deuda a un año 800,5 frente a 398,1 de caja [URD2025, PDF p. 383]) y deuda + arrendamientos 13 veces el FCF base (C64). Son reales en la refinanciación (en 2020 hubo que ajustar el covenant [URD2020, PDF p. 154]) pero no apuntan a quiebra probable (1,75x frente a 3,75x [URD2025, PDF p. 314, 380]). Sin doble cuenta: r no lleva prima de quiebra.
- **C76 = 0.** La caja no cubre la deuda a un año, 45,8 están en Latinoamérica sin México y 8,0 en Rusia [URD2025, PDF p. 383], y los intereses de C48 son netos.
- **OCEANE 2029.** C55 (259,08 m) ya incluye 23,36 m acciones de su conversión [URD2025, PDF p. 395] y a 31-dic-2025 siguen como deuda (364,4 [URD2025, PDF p. 383]). En el motor A el efecto es el cupón (2,25 % sobre 380 ≈ 8,6 al año [URD2025, PDF p. 380]) dentro de f: ≈2,8 % del FCF base contado dos veces, sesgo pequeño a la baja. El tratamiento (E6/D3) está pendiente y no lo adopto.
- **C24 vacía** (solo hay cuotas y tamaños de 2017 [RD2017, PDF p. 42]); **C44 vacía** (C52 > 0, C43 = No aplica).

## Los dos errores opuestos

Con estas palancas y este motor tengo más cerca **regatear**. La fase A nombró el contrario, pagar de más por la calidad (17,6x la caja libre LTM frente a 14,6x de mediana, C88), y sigue siendo la tentación cualitativa: «I know it's wonderful, but is it wonderful enough to justify that big a premium?» (DR p.308; HIM). Pero los números empujan al otro lado: el motor arranca en 248,6 frente a 308, cobro las compras aunque C52 no las reste, no cuento la caída contable de la amortización de compras, el NORMAL queda medio punto bajo m0 y mantengo 0,05 de quiebra. Si la fase C lee un valor bajo sin ese sesgo delante, puede descartar un buen negocio por un artefacto: «We left a lot of money on the table through early fretting» (TCI p.79; HIM).

## Lo que no pude fundamentar

El reparto del capex entre reposición y crecimiento (no publicado): los S2C orgánicos (1,2 / 1,5 / 2,0) salen de la inversión por encima de la amortización propia, que mezcla las dos. La tasa de bajas (no publicada) y el retorno por compra después de sinergias: solo tengo el primer año de las compras de 2024–25. La lectura de C18 (capital orgánico por encima de r) sostiene el S2C del NORMAL y del BUENO y el ROIC de esos dos escenarios; si no se sostiene, S2C 1,0 y ROIC 0,09.
