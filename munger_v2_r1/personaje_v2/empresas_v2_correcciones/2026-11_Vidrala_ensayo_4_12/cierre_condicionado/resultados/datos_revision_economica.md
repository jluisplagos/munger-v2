# Datos para la revisión económica · Vidrala

Libro `Vidrala/recalc/Vidrala_v63_evaluada.xlsx` (recalculado). Precio 90.1 · V [44.32, 60.21, 78.52] · p [0.2, 0.6, 0.2] · ponderado 60.70 · precio de Sí 56.02 · zona caro · t NOPAT 0.2205.

## Bases y derivados de «Configuración V6.4»

| Celda | Concepto | Valor |
|---|---|---|
| B54 | Amortización del último año (D&A₀, Historia L8) | 132.9480 |
| B55 | Σ reinversión neta total H–L (Historia H31:L31, denominador de C53) | 520.5960 |
| B56 | Σ amortización de la cartera H–L (P0; 0 con legado) | 9.4130 |
| B57 | D_hist · reinversión neta frente a la amortización que se repone | 530.0090 |
| B58 | Σ (capex − D&A) H–L | 229.3810 |
| B59 | Σ adquisiciones netas H–L (Historia H13:L13) | 12.4180 |
| B60 | Exceso histórico acumulado sobre la amortización que se repone | 238.7940 |
| B61 | Exceso histórico medio (÷ 5) | 47.7588 |
| B62 | F_hist · inversión fija neta histórica frente a la amortización que se repone, con adquisiciones | 251.2120 |
| B63 | Σ amortización que se repone H–L | 500.2090 |
| B66 | ¿P0 explícito? | 1.0000 |
| B67 | ¿Requisito adicional? (estructura distinta de «Sin requisito adicional») | 1.0000 |
| B68 | ¿Familia Λ? | 1.0000 |
| B69 | Código de la estructura | SR1 |
| B70 | Requisito a ventas constantes (nivel anual, M€) | 19.9422 |
| B71 | Rh · parte de D_hist atribuida a reposición | 75.0314 |
| B72 | f = D_hist ÷ (D_hist − Rh) (SR1, SR2) | 1.1649 |
| B73 | f_fija = 1 − Rh ÷ F_hist (SRF) | 1.0000 |
| B76 | EXPERIMENTAL ACTIVO Y VÁLIDO | 1.0000 |
| B77 | R1 activa | 1.0000 |
| B78 | P-M1 activa (requisito adicional o P0) | 1.0000 |
| B79 | Estructura H (crédito) | 0.0000 |
| B80 | Familia Λ activa | 1.0000 |
| B81 | Requisito proporcional a las ventas en los años 1–10 | 0.0000 |
| B82 | Requisito proporcional a las ventas en el terminal | 1.0000 |
| B83 | Circulante comercial ÷ ventas efectivo (0 = sin desglose) | 0.1470 |
| B84 | Factor del S2C de los años 1–10 (SR1, SR2) | 1.1649 |
| B85 | Factor del ROIC del terminal (SR2) | 1.0000 |
| B86 | Factor de la inversión fija para crecer (SRF) | 1.0000 |
| B87 | λ − 1 efectivo | 0.1500 |
| B88 | Nivel Θ efectivo (M€/año) | 0.0000 |
| B89 | Requisito a ventas constantes efectivo (valor sin crecimiento) | 19.9422 |

## MALO · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,443.2 | 1,421.5 | 1,400.2 | 1,379.2 | 1,358.5 | 1,344.9 | 1,338.2 | 1,338.2 | 1,344.9 | 1,358.4 | 1,371.9 |  |
| maximo_conservado | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 | 1,465.2 |  |
| margen | 0.1784 | 0.1713 | 0.1642 | 0.1571 | 0.1500 | 0.1500 | 0.1500 | 0.1500 | 0.1500 | 0.1500 | 0.1500 |  |
| nopat | 200.7 | 189.8 | 179.2 | 168.9 | 158.8 | 157.2 | 156.5 | 156.5 | 157.2 | 158.8 | 160.4 | 1,683.6 |
| da | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 124.5 | 1,329.5 |
| reposicion_contable | 128.5 | 128.5 | 128.5 | 128.5 | 129.1 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 124.5 | 1,307.6 |
| requisito | 19.3 | 19.3 | 19.3 | 19.3 | 19.4 | 19.9 | 19.9 | 19.9 | 19.9 | 19.9 | 18.7 | 196.1 |
| fija_para_crecer | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 15.8 | 0.0 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | -3.2 | -3.2 | -3.1 | -3.1 | -3.0 | -2.0 | -1.0 | 0.0 | 1.0 | 2.0 | 2.0 | -15.7 |
| fija_bruta | 147.7 | 147.7 | 147.7 | 147.7 | 148.4 | 152.9 | 152.9 | 152.9 | 152.9 | 152.9 | 159.0 | 1,503.8 |
| inversion_total | 144.5 | 144.5 | 144.6 | 144.6 | 145.4 | 150.9 | 151.9 | 152.9 | 153.9 | 154.9 | 161.0 | 1,488.1 |
| fcf_motor | 189.1 | 178.2 | 167.6 | 157.2 | 146.4 | 139.3 | 137.5 | 136.5 | 136.3 | 136.9 | 123.9 | 1,525.0 |
| vp | 174.0 | 150.8 | 130.5 | 112.6 | 96.5 | 84.5 | 76.7 | 70.1 | 64.4 | 59.5 | 700.4 | 1,019.7 |

- S2C efectivo de los años 0.8154 · ROIC efectivo del terminal 0.0900 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.0953.
- Peso del terminal 0.407 · salto año 10 → terminal: requisito -0.064, FCF -0.095, ventas 0.010.
- Años con ventas bajo el máximo conservado: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] · inversión fija para crecer en esos años 0.00 · en el terminal 15.83 · circulante liberado en los años 1–10 18.67.

## NORMAL · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,487.1 | 1,509.4 | 1,532.1 | 1,555.1 | 1,578.4 | 1,603.6 | 1,630.9 | 1,660.3 | 1,691.8 | 1,725.6 | 1,760.2 |  |
| maximo_conservado | 1,465.2 | 1,487.1 | 1,509.4 | 1,532.1 | 1,555.1 | 1,578.4 | 1,603.6 | 1,630.9 | 1,660.3 | 1,691.8 | 1,725.6 |  |
| margen | 0.1844 | 0.1833 | 0.1822 | 0.1811 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 | 0.1800 |  |
| nopat | 213.7 | 215.6 | 217.6 | 219.5 | 221.5 | 225.0 | 228.8 | 232.9 | 237.4 | 242.1 | 247.0 | 2,254.1 |
| da | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 159.7 | 1,329.5 |
| reposicion_contable | 128.5 | 128.5 | 128.5 | 128.5 | 129.1 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 159.7 | 1,307.6 |
| requisito | 19.3 | 19.3 | 19.3 | 19.3 | 19.4 | 19.9 | 19.9 | 19.9 | 19.9 | 19.9 | 24.0 | 196.1 |
| fija_para_crecer | 17.7 | 18.0 | 18.3 | 18.5 | 18.8 | 20.4 | 22.0 | 23.7 | 25.4 | 27.3 | 49.8 | 210.2 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | 3.2 | 3.3 | 3.3 | 3.4 | 3.4 | 3.7 | 4.0 | 4.3 | 4.6 | 5.0 | 5.1 | 38.3 |
| fija_bruta | 165.5 | 165.7 | 166.0 | 166.3 | 167.2 | 173.3 | 174.9 | 176.6 | 178.3 | 180.2 | 233.5 | 1,713.9 |
| inversion_total | 168.7 | 169.0 | 169.3 | 169.6 | 170.7 | 177.0 | 178.9 | 180.9 | 183.0 | 185.2 | 238.6 | 1,752.2 |
| fcf_motor | 178.0 | 179.6 | 181.2 | 182.8 | 183.7 | 181.0 | 182.9 | 185.0 | 187.3 | 189.9 | 168.1 | 1,831.4 |
| vp | 163.8 | 152.0 | 141.1 | 131.0 | 121.1 | 109.8 | 102.1 | 95.0 | 88.5 | 82.5 | 1,092.4 | 1,186.9 |

- S2C efectivo de los años 1.0484 · ROIC efectivo del terminal 0.0900 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.1471.
- Peso del terminal 0.479 · salto año 10 → terminal: requisito 0.201, FCF -0.115, ventas 0.020.
- Años con ventas bajo el máximo conservado: ninguno · inversión fija para crecer en esos años 0.00 · en el terminal 49.80 · circulante liberado en los años 1–10 0.00.

## BUENO · motor B calculable · comprobación: ✓ cuadra: identidad anual y terminal y VP iguales al motor

| Partida | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | Terminal | Σ 1–10 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ventas | 1,516.4 | 1,569.5 | 1,624.4 | 1,681.3 | 1,740.2 | 1,797.6 | 1,853.3 | 1,907.0 | 1,958.5 | 2,007.5 | 2,057.7 |  |
| maximo_conservado | 1,465.2 | 1,516.4 | 1,569.5 | 1,624.4 | 1,681.3 | 1,740.2 | 1,797.6 | 1,853.3 | 1,907.0 | 1,958.5 | 2,007.5 |  |
| margen | 0.1884 | 0.1913 | 0.1942 | 0.1971 | 0.2000 | 0.2000 | 0.2000 | 0.2000 | 0.2000 | 0.2000 | 0.2000 |  |
| nopat | 222.7 | 234.0 | 245.9 | 258.3 | 271.3 | 280.2 | 288.9 | 297.3 | 305.3 | 313.0 | 320.8 | 2,716.8 |
| da | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 186.7 | 1,329.5 |
| reposicion_contable | 128.5 | 128.5 | 128.5 | 128.5 | 129.1 | 132.9 | 132.9 | 132.9 | 132.9 | 132.9 | 186.7 | 1,307.6 |
| requisito | 19.3 | 19.3 | 19.3 | 19.3 | 19.4 | 19.9 | 19.9 | 19.9 | 19.9 | 19.9 | 28.0 | 196.1 |
| fija_para_crecer | 32.5 | 33.6 | 34.8 | 36.0 | 37.3 | 36.4 | 35.3 | 34.0 | 32.6 | 31.0 | 59.4 | 343.5 |
| credito | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |
| delta_circulante | 7.5 | 7.8 | 8.1 | 8.4 | 8.7 | 8.4 | 8.2 | 7.9 | 7.6 | 7.2 | 7.4 | 79.7 |
| fija_bruta | 180.2 | 181.3 | 182.5 | 183.7 | 185.7 | 189.3 | 188.2 | 186.9 | 185.5 | 183.9 | 274.2 | 1,847.3 |
| inversion_total | 187.7 | 189.1 | 190.6 | 192.1 | 194.3 | 197.7 | 196.4 | 194.8 | 193.1 | 191.1 | 281.5 | 1,927.0 |
| fcf_motor | 167.9 | 177.8 | 188.2 | 199.1 | 209.9 | 215.5 | 225.5 | 235.4 | 245.2 | 254.8 | 225.9 | 2,119.3 |
| vp | 154.4 | 150.5 | 146.6 | 142.7 | 138.4 | 130.7 | 125.8 | 120.9 | 115.8 | 110.7 | 1,586.7 | 1,336.6 |

- S2C efectivo de los años 1.2814 · ROIC efectivo del terminal 0.1200 · rentabilidad marginal implícita de los años (S2C × margen del año 10 × (1 − t)) 0.1998.
- Peso del terminal 0.543 · salto año 10 → terminal: requisito 0.404, FCF -0.113, ventas 0.025.
- Años con ventas bajo el máximo conservado: ninguno · inversión fija para crecer en esos años 0.00 · en el terminal 59.45 · circulante liberado en los años 1–10 0.00.

## Variantes calculadas (diferencia del precio de Sí frente a la activa)

| Variante | Parámetros que varía | Ponderado | Precio de Sí | Zona | Δ Sí |
|---|---|---|---|---|---|
| heredado | modo, N1.tipo, N1.escudo, N2.margen, N3.regla, N3.circulante, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 69.04 | 64.75 | caro | 8.73 |
| activa | — | 60.70 | 56.02 | caro | 0.00 |
| solo_N1 | N2.margen, N3.regla, N3.circulante, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 67.17 | 63.04 | caro | 7.02 |
| solo_N2 | N1.tipo, N1.escudo, N3.regla, N3.circulante, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 70.02 | 65.72 | caro | 9.70 |
| solo_R1 | N1.tipo, N1.escudo, N2.margen, PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 68.41 | 63.40 | caro | 7.38 |
| activa_sin_PM1 | PM1.estructura, PM1.familia, PM1.parametro, PM1.convencion_anios, PM1.convencion_terminal, PM1.roic_terminal, PM1.cartera | 67.50 | 62.63 | caro | 6.61 |
| activa_solo_P0 | PM1.estructura | 67.99 | 63.11 | caro | 7.10 |
| estructura_H | PM1.estructura | 67.17 | 61.37 | caro | 5.35 |
| estructura_S | PM1.estructura | 60.00 | 55.52 | caro | -0.50 |
| estructura_SR2 | PM1.estructura, PM1.roic_terminal | 62.02 | 57.08 | caro | 1.06 |
| estructura_SRF | PM1.estructura | 63.77 | 58.43 | caro | 2.41 |
| parametro_minimo | PM1.parametro | 63.13 | 58.38 | caro | 2.37 |
| parametro_maximo | PM1.parametro | 55.84 | 51.29 | caro | -4.73 |
| convencion_anios_alternativa | PM1.convencion_anios | 60.43 | 55.89 | caro | -0.13 |
| convencion_terminal_alternativa | PM1.convencion_terminal | 61.35 | 56.42 | caro | 0.40 |

## Avisos de dominio de las variantes

```
[
 {
  "id": "inversion_fija_para_crecer_negativa",
  "activo": false,
  "valores": {
   "negativos": [],
   "nwc_efectivo": 0.147037866171613,
   "f_s2c": 1.16491216656467,
   "s2c_por_f": {
    "MALO": 0.815438516595269,
    "NORMAL": 1.0484209499082031,
    "BUENO": 1.2814033832211371
   },
   "uno_entre_nwc": 6.8009692063462435
  },
  "motivo": "la inversión fija para crecer sale negativa cuando S2C·f > 1 ÷ NWC: el modelo liberaría capital fijo al crecer (dominio declarado en la 4.11, H13)"
 },
 {
  "id": "factor_de_reestimacion",
  "activo": null,
  "valores": {
   "f": 1.16491216656467,
   "estructura": "SR1",
   "f_s2c": 1.16491216656467,
   "f_roic": 1,
   "f_fija": 1,
   "D_hist": 530.009,
   "Rh": 75.03135,
   "D_hist_menos_Rh": 454.97765000000004,
   "lambda": 1.15,
   "lambda_en_que_f_deja_de_estar_definida": 2.0595750976091995
  },
  "motivo": "f = D_hist ÷ (D_hist − Rh) no tiene cota superior adoptada: el S2C y el ROIC reestimados pierden sentido mucho antes de que f deje de estar definida (4.11, H13). Se muestra siempre que la estructura reestima (SR1, SR2, SRF); no hay umbral"
 },
 {
  "id": "terminal_r1_sin_maximo_conservado",
  "activo": true,
  "valores": {
   "regla": "R1",
   "escenarios": [
    {
     "escenario": "MALO",
     "ventas_anio_10": 1358.35071893599,
     "maximo_conservado": 1465.16,
     "inversion_fija_terminal": 15.8254771448017
    }
   ]
  },
  "motivo": "con R1, el terminal carga la inversión fija para crecer al ritmo g aunque las ventas del año 10 sigan por debajo del máximo conservado (definición prudente de la 4.7.1/4.8.1; la regla del máximo no se aplica en el terminal)"
 },
 {
  "id": "s2c_inerte",
  "activo": true,
  "valores": {
   "regla": "R1",
   "escenarios": [
    {
     "escenario": "MALO",
     "s2c": 0.7,
     "ventas_maximas_anios_1_10": 1443.1826,
     "maximo_conservado": 1465.16
    }
   ]
  },
  "motivo": "con R1, en un escenario cuyas ventas no superan el máximo conservado en ningún año 1–10, la inversión fija para crecer es 0 y la palanca S2C de ese escenario no actúa en esos años (4.11, H12)"
 }
]
```
