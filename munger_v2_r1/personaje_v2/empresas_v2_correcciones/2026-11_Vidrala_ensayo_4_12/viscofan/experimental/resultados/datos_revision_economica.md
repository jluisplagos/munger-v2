# Datos para la revisión económica · Viscofan

Libro `Viscofan/recalc/Viscofan_v63_evaluada.xlsx` (recalculado). Precio 54.7 · V [30.69, 44.85, 60.0] · p [0.25, 0.6, 0.15] · ponderado 43.59 · precio de Sí 39.29 · zona caro · t NOPAT 0.2212.

## Bases y derivados de «Configuración V6.4»

| Celda | Concepto | Valor |
|---|---|---|
| B54 | Amortización del último año (D&A₀, Historia L8) | 85.1960 |
| B55 | Σ reinversión neta total H–L (Historia H31:L31, denominador de C53) | 296.4890 |
| B56 | Σ amortización de la cartera H–L (P0; 0 con legado) | 0.0000 |
| B57 | D_hist · reinversión neta frente a la amortización que se repone | 296.4890 |
| B58 | Σ (capex − D&A) H–L | 40.8130 |
| B59 | Σ adquisiciones netas H–L (Historia H13:L13) | 16.1610 |
| B60 | Exceso histórico acumulado sobre la amortización que se repone | 40.8130 |
| B61 | Exceso histórico medio (÷ 5) | 8.1626 |
| B62 | F_hist · inversión fija neta histórica frente a la amortización que se repone, con adquisiciones | 56.9740 |
| B63 | Σ amortización que se repone H–L | 403.1320 |
| B66 | ¿P0 explícito? | 0.0000 |
| B67 | ¿Requisito adicional? (estructura distinta de «Sin requisito adicional») | 1.0000 |
| B68 | ¿Familia Λ? | 0.0000 |
| B69 | Código de la estructura | SR1 |
| B70 | Requisito a ventas constantes (nivel anual, M€) | 4.0813 |
| B71 | Rh · parte de D_hist atribuida a reposición | 20.4065 |
| B72 | f = D_hist ÷ (D_hist − Rh) (SR1, SR2) | 1.0739 |
| B73 | f_fija = 1 − Rh ÷ F_hist (SRF) | 1.0000 |
| B76 | EXPERIMENTAL ACTIVO Y VÁLIDO | 1.0000 |
| B77 | R1 activa | 1.0000 |
| B78 | P-M1 activa (requisito adicional o P0) | 1.0000 |
| B79 | Estructura H (crédito) | 0.0000 |
| B80 | Familia Λ activa | 0.0000 |
| B81 | Requisito proporcional a las ventas en los años 1–10 | 0.0000 |
| B82 | Requisito proporcional a las ventas en el terminal | 1.0000 |
| B83 | Circulante comercial ÷ ventas efectivo (0 = sin desglose) | 0.4828 |
| B84 | Factor del S2C de los años 1–10 (SR1, SR2) | 1.0739 |
| B85 | Factor del ROIC del terminal (SR2) | 1.0000 |
| B86 | Factor de la inversión fija para crecer (SRF) | 1.0000 |
| B87 | λ − 1 efectivo | 0.0000 |
| B88 | Nivel Θ efectivo (M€/año) | 4.0813 |
| B89 | Requisito a ventas constantes efectivo (valor sin crecimiento) | 4.0813 |

## MALO · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,264.5 | 1,277.1 | 1,289.9 | 1,302.8 | 1,315.8 | 1,329.0 | 1,342.3 | 1,355.7 | 1,369.3 | 1,383.0 | 1,396.8 |  |
| maximo_conservado | 1,252.0 | 1,264.5 | 1,277.1 | 1,289.9 | 1,302.8 | 1,315.8 | 1,329.0 | 1,342.3 | 1,355.7 | 1,369.3 | 1,383.0 |  |
| margen | 0.1589 | 0.1541 | 0.1494 | 0.1447 | 0.1400 | 0.1400 | 0.1400 | 0.1400 | 0.1400 | 0.1400 | 0.1400 |  |
| nopat | 156.4 | 153.3 | 150.1 | 146.8 | 143.5 | 144.9 | 146.4 | 147.8 | 149.3 | 150.8 | 152.3 | 1,489.4 |
| da | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 95.1 | 852.0 |
| reposicion_contable | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 95.1 | 852.0 |
| requisito | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.6 | 40.8 |
| fija_para_crecer | 6.9 | 7.0 | 7.0 | 7.1 | 7.2 | 7.3 | 7.3 | 7.4 | 7.5 | 7.6 | 12.4 | 72.3 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | 6.0 | 6.1 | 6.2 | 6.2 | 6.3 | 6.4 | 6.4 | 6.5 | 6.5 | 6.6 | 6.7 | 63.2 |
| fija_bruta | 96.2 | 96.3 | 96.3 | 96.4 | 96.5 | 96.5 | 96.6 | 96.7 | 96.8 | 96.8 | 112.0 | 965.0 |
| inversion_total | 102.2 | 102.4 | 102.5 | 102.6 | 102.8 | 102.9 | 103.0 | 103.2 | 103.3 | 103.4 | 118.6 | 1,028.3 |
| fcf_motor | 139.4 | 136.2 | 132.8 | 129.4 | 125.9 | 127.2 | 128.5 | 129.8 | 131.2 | 132.5 | 128.7 | 1,313.0 |
| vp | 128.8 | 116.2 | 104.7 | 94.2 | 84.7 | 79.0 | 73.7 | 68.8 | 64.2 | 59.9 | 801.6 | 874.2 |

- S2C efectivo de los años 0.9665 · ROIC efectivo del terminal 0.0800 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.1054.
- Peso del terminal 0.478 · salto año 10 → terminal: requisito 0.116, FCF -0.029, ventas 0.010.
- Años con ventas bajo el máximo conservado: ninguno · inversión fija para crecer en esos años 0.00 · en el terminal 12.36 · circulante liberado en los años 1–10 0.00.

## NORMAL · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,308.3 | 1,367.2 | 1,428.7 | 1,493.0 | 1,560.2 | 1,622.6 | 1,679.4 | 1,729.8 | 1,773.0 | 1,808.5 | 1,844.7 |  |
| maximo_conservado | 1,252.0 | 1,308.3 | 1,367.2 | 1,428.7 | 1,493.0 | 1,560.2 | 1,622.6 | 1,679.4 | 1,729.8 | 1,773.0 | 1,808.5 |  |
| margen | 0.1639 | 0.1641 | 0.1644 | 0.1647 | 0.1650 | 0.1650 | 0.1650 | 0.1650 | 0.1650 | 0.1650 | 0.1650 |  |
| nopat | 167.0 | 174.8 | 183.0 | 191.5 | 200.5 | 208.5 | 215.8 | 222.3 | 227.8 | 232.4 | 237.0 | 2,023.6 |
| da | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 125.5 | 852.0 |
| reposicion_contable | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 125.5 | 852.0 |
| requisito | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 6.0 | 40.8 |
| fija_para_crecer | 20.5 | 21.4 | 22.4 | 23.4 | 24.4 | 22.7 | 20.7 | 18.3 | 15.7 | 12.9 | 25.6 | 202.4 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | 27.2 | 28.4 | 29.7 | 31.0 | 32.4 | 30.1 | 27.4 | 24.3 | 20.9 | 17.1 | 17.5 | 268.7 |
| fija_bruta | 109.8 | 110.7 | 111.7 | 112.7 | 113.7 | 112.0 | 109.9 | 107.6 | 105.0 | 102.2 | 157.2 | 1,095.2 |
| inversion_total | 137.0 | 139.1 | 141.4 | 143.7 | 146.2 | 142.1 | 137.4 | 131.9 | 125.9 | 119.3 | 174.6 | 1,363.9 |
| fcf_motor | 115.2 | 120.9 | 126.8 | 133.0 | 139.5 | 151.6 | 163.7 | 175.6 | 187.2 | 198.3 | 187.9 | 1,511.7 |
| vp | 106.4 | 103.1 | 99.9 | 96.8 | 93.8 | 94.2 | 93.9 | 93.0 | 91.6 | 89.7 | 1,357.4 | 962.5 |

- S2C efectivo de los años 1.1813 · ROIC efectivo del terminal 0.1100 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.1518.
- Peso del terminal 0.585 · salto año 10 → terminal: requisito 0.473, FCF -0.052, ventas 0.020.
- Años con ventas bajo el máximo conservado: ninguno · inversión fija para crecer en esos años 0.00 · en el terminal 25.63 · circulante liberado en los años 1–10 0.00.

## BUENO · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,339.6 | 1,433.4 | 1,533.7 | 1,641.1 | 1,756.0 | 1,863.1 | 1,960.0 | 2,044.2 | 2,113.7 | 2,166.6 | 2,220.8 |  |
| maximo_conservado | 1,252.0 | 1,339.6 | 1,433.4 | 1,533.7 | 1,641.1 | 1,756.0 | 1,863.1 | 1,960.0 | 2,044.2 | 2,113.7 | 2,166.6 |  |
| margen | 0.1669 | 0.1701 | 0.1734 | 0.1767 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 |  |
| nopat | 174.1 | 189.9 | 207.2 | 225.9 | 246.2 | 261.2 | 274.8 | 286.6 | 296.3 | 303.7 | 311.3 | 2,465.8 |
| da | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 151.1 | 852.0 |
| reposicion_contable | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 85.2 | 151.1 | 852.0 |
| requisito | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 4.1 | 7.2 | 40.8 |
| fija_para_crecer | 16.0 | 17.1 | 18.3 | 19.6 | 20.9 | 19.5 | 17.7 | 15.4 | 12.7 | 9.6 | 38.7 | 166.7 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | 42.3 | 45.3 | 48.4 | 51.8 | 55.5 | 51.7 | 46.8 | 40.7 | 33.6 | 25.5 | 26.2 | 441.6 |
| fija_bruta | 105.3 | 106.4 | 107.6 | 108.8 | 110.2 | 108.8 | 106.9 | 104.6 | 101.9 | 98.9 | 197.1 | 1,059.5 |
| inversion_total | 147.6 | 151.6 | 156.0 | 160.7 | 165.7 | 160.5 | 153.7 | 145.3 | 135.5 | 124.4 | 223.2 | 1,501.1 |
| fcf_motor | 111.7 | 123.5 | 136.3 | 150.4 | 165.7 | 185.9 | 206.2 | 226.4 | 246.0 | 264.5 | 239.2 | 1,816.6 |
| vp | 103.2 | 105.4 | 107.5 | 109.5 | 111.4 | 115.4 | 118.3 | 120.0 | 120.4 | 119.6 | 1,877.8 | 1,130.7 |

- S2C efectivo de los años 1.5035 · ROIC efectivo del terminal 0.1200 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.2108.
- Peso del terminal 0.624 · salto año 10 → terminal: requisito 0.774, FCF -0.096, ventas 0.025.
- Años con ventas bajo el máximo conservado: ninguno · inversión fija para crecer en esos años 0.00 · en el terminal 38.70 · circulante liberado en los años 1–10 0.00.

## Variantes calculadas (diferencia del precio de Sí frente a la activa)

| Variante | Parámetros que varía | Ponderado | Precio de Sí | Zona | Δ Sí |
|---|---|---|---|---|---|
| heredado | modo, N1.tipo, N1.escudo, N3.regla, N3.circulante, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 46.26 | 41.81 | caro | 2.52 |
| activa | — | 43.59 | 39.29 | caro | 0.00 |
| solo_N1 | N3.regla, N3.circulante, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal | 44.65 | 40.35 | caro | 1.07 |
| solo_R1 | N1.tipo, N1.escudo, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal | 46.26 | 41.81 | caro | 2.52 |
| activa_sin_PM1 | PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal | 44.65 | 40.35 | caro | 1.07 |
| estructura_H | PM1.estructura | 44.65 | 40.35 | caro | 1.07 |
| estructura_S | PM1.estructura | 43.14 | 38.94 | caro | -0.35 |
| estructura_SR2 | PM1.estructura, PM1.roic_terminal | 44.03 | 39.64 | caro | 0.36 |
| estructura_SRF | PM1.estructura | 45.56 | 40.90 | caro | 1.61 |
| parametro_minimo | PM1.parametro | 44.65 | 40.35 | caro | 1.07 |
| parametro_maximo | PM1.parametro | 42.52 | 38.22 | caro | -1.07 |
| convencion_anios_alternativa | PM1.convencion_anios | 43.46 | 39.20 | caro | -0.09 |
| convencion_terminal_alternativa | PM1.convencion_terminal | 43.86 | 39.49 | caro | 0.20 |

## Avisos de dominio de las variantes

```
[
 {
  "id": "inversion_fija_para_crecer_negativa",
  "activo": false,
  "valores": {
   "negativos": [],
   "nwc_efectivo": 0.482846013084842,
   "f_s2c": 1.07391450019469,
   "s2c_por_f": {
    "MALO": 0.966523050175221,
    "NORMAL": 1.181305950214159,
    "BUENO": 1.5034803002725659
   },
   "uno_entre_nwc": 2.0710536545826
  },
  "motivo": "la inversión fija para crecer sale negativa cuando S2C·f > 1 ÷ NWC: el modelo liberaría capital fijo al crecer (dominio declarado en la 4.11, H13)"
 },
 {
  "id": "factor_de_reestimacion",
  "activo": null,
  "valores": {
   "f": 1.07391450019469,
   "estructura": "SR1",
   "f_s2c": 1.07391450019469,
   "f_roic": 1,
   "f_fija": 1,
   "D_hist": 296.489,
   "Rh": 20.4065,
   "D_hist_menos_Rh": 276.0825,
   "lambda": null,
   "lambda_en_que_f_deja_de_estar_definida": null
  },
  "motivo": "f = D_hist ÷ (D_hist − Rh) no tiene cota superior adoptada: el S2C y el ROIC reestimados pierden sentido mucho antes de que f deje de estar definida (4.11, H13). Se muestra siempre que la estructura reestima (SR1, SR2, SRF); no hay umbral"
 },
 {
  "id": "terminal_r1_sin_maximo_conservado",
  "activo": false,
  "valores": {
   "regla": "R1",
   "escenarios": []
  },
  "motivo": "con R1, el terminal carga la inversión fija para crecer al ritmo g aunque las ventas del año 10 sigan por debajo del máximo conservado (definición prudente de la 4.7.1/4.8.1; la regla del máximo no se aplica en el terminal)"
 },
 {
  "id": "s2c_inerte",
  "activo": false,
  "valores": {
   "regla": "R1",
   "escenarios": []
  },
  "motivo": "con R1, en un escenario cuyas ventas no superan el máximo conservado en ningún año 1–10, la inversión fija para crecer es 0 y la palanca S2C de ese escenario no actúa en esos años (4.11, H12)"
 }
]
```
