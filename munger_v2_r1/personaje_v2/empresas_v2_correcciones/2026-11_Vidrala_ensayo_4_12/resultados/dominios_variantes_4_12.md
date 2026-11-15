# Avisos de dominio de todas las variantes calculadas (revisión interna R7)

**Qué es.** El pipeline calcula los avisos de dominio sobre la variante «activa». Aquí se calculan, en lectura, sobre cada libro recalculado de las variantes (`dominios_v64.py`, sin umbrales adoptados): avisos activos y factor de reestimación f de la estructura de cada variante. No cambia ningún expediente.
Lectura: el extremo λ = 1,25 de Vidrala lleva f = 1,309 (la activa, 1,165); en Viscofan, θ = 1 lleva f = 1,160. En Vidrala, las dos variantes con R0 y sin P-M1 (solo_N1 y solo_N2, esta última el extremo superior del rango, 65,72 €) llevan activo el aviso de inversión fija para crecer negativa en el MALO. Los avisos son lecturas: no cambian ningún valor, y todas las variantes de las dos empresas siguen en «caro».

## Vidrala (cierre_condicionado)

| Variante | Precio de Sí | Zona | Estructura | f | f_fija | Avisos activos | Nota |
|---|---|---|---|---|---|---|---|
| heredado | 64.75 | caro | — | — | — | ninguno | — |
| activa | 56.02 | caro | SR1 | 1.1649 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| solo_N1 | 63.04 | caro | — | 1.0000 | 1.0000 | inversion_fija_para_crecer_negativa | interpretación, no comprobada celda a celda: negativos del MALO por la caída de las ventas con R0 (sin desglose del circulante: R0 libera capital al caer las ventas), no por el dominio S2C·f > 1 ÷ NWC |
| solo_N2 | 65.72 | caro | — | 1.0000 | 1.0000 | inversion_fija_para_crecer_negativa | interpretación, no comprobada celda a celda: negativos del MALO por la caída de las ventas con R0 (sin desglose del circulante: R0 libera capital al caer las ventas), no por el dominio S2C·f > 1 ÷ NWC |
| solo_R1 | 63.40 | caro | — | 1.0000 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| activa_sin_PM1 | 62.63 | caro | — | 1.0000 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| activa_solo_P0 | 63.11 | caro | — | 1.0000 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| estructura_H | 61.37 | caro | H | 1.0000 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| estructura_S | 55.52 | caro | S | 1.0000 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| estructura_SR2 | 57.08 | caro | SR2 | 1.1649 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| estructura_SRF | 58.43 | caro | SRF | 1.0000 | 0.7013 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| parametro_minimo | 58.38 | caro | SR1 | 1.1042 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| parametro_maximo | 51.29 | caro | SR1 | 1.3088 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| convencion_anios_alternativa | 55.89 | caro | SR1 | 1.1649 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |
| convencion_terminal_alternativa | 56.42 | caro | SR1 | 1.1649 | 1.0000 | terminal_r1_sin_maximo_conservado, s2c_inerte | — |

## Viscofan (experimental)

| Variante | Precio de Sí | Zona | Estructura | f | f_fija | Avisos activos | Nota |
|---|---|---|---|---|---|---|---|
| heredado | 41.81 | caro | — | — | — | ninguno | — |
| activa | 39.29 | caro | SR1 | 1.0739 | 1.0000 | ninguno | — |
| solo_N1 | 40.35 | caro | — | 1.0000 | 1.0000 | ninguno | — |
| solo_R1 | 41.81 | caro | — | 1.0000 | 1.0000 | ninguno | — |
| activa_sin_PM1 | 40.35 | caro | — | 1.0000 | 1.0000 | ninguno | — |
| estructura_H | 40.35 | caro | H | 1.0000 | 1.0000 | ninguno | — |
| estructura_S | 38.94 | caro | S | 1.0000 | 1.0000 | ninguno | — |
| estructura_SR2 | 39.64 | caro | SR2 | 1.0739 | 1.0000 | ninguno | — |
| estructura_SRF | 40.90 | caro | SRF | 1.0000 | 0.6418 | ninguno | — |
| parametro_minimo | 40.35 | caro | SR1 | 1.0000 | 1.0000 | ninguno | — |
| parametro_maximo | 38.22 | caro | SR1 | 1.1596 | 1.0000 | ninguno | — |
| convencion_anios_alternativa | 39.20 | caro | SR1 | 1.0739 | 1.0000 | ninguno | — |
| convencion_terminal_alternativa | 39.49 | caro | SR1 | 1.0739 | 1.0000 | ninguno | — |

