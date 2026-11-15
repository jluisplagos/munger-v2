# Contraste mecánico para el juicio sobre el objetivo (contrato 4.14)

Precio de Sí de la activa: 39.79819353512519. Copia en `juicio_objetivo.contraste` exactamente estas filas de cada parámetro (variante, delta_eur y atribuible). Solo son atribuibles al parámetro los contrastes aislados y las variaciones conjuntas necesarias. Sin contraste, el cambio no está definido (no es 0).

| Parámetro | Cobertura | Variante | Precio de Sí | Δ € | Δ % | Atribuible |
|---|---|---|---|---|---|---|
| N3.regla | variacion_conjunta_necesaria | solo_N1 | 41.4698 | +1.67 | +4.20 % | sí |
| N3.regla | variacion_conjunta_necesaria | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | sí |
| N3.regla | variacion_conjunta_necesaria | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.estructura | contraste_aislado | estructura_H | 41.4698 | +1.67 | +4.20 % | sí |
| PM1.estructura | contraste_aislado | estructura_S | 39.1768 | -0.62 | -1.56 % | sí |
| PM1.estructura | contraste_aislado | estructura_SRF | 41.7085 | +1.91 | +4.80 % | sí |
| PM1.estructura | contraste_aislado | estructura_SR2 | 40.3708 | +0.57 | +1.44 % | sí |
| PM1.estructura | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.estructura | contraste_aislado | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.estructura | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.estructura | contraste_aislado | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.estructura | contraste_aislado | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.cartera | variacion_conjunta | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N1.tipo | variacion_conjunta_necesaria | activa_sin_N1 | 41.3078 | +1.51 | +3.79 % | sí |
| N1.tipo | variacion_conjunta_necesaria | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N1.tipo | variacion_conjunta_necesaria | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N1.escudo | contraste_aislado | escudo_alternativo | 39.7394 | -0.06 | -0.15 % | sí |
| N1.escudo | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N1.escudo | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N1.escudo | contraste_aislado | activa_sin_N1 | 41.3078 | +1.51 | +3.79 % | no (varía otros parámetros) |
| N3.circulante | variacion_conjunta | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| N3.circulante | variacion_conjunta | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| N3.circulante | variacion_conjunta | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.familia | variacion_conjunta | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.familia | variacion_conjunta | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.familia | variacion_conjunta | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.familia | variacion_conjunta | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.familia | variacion_conjunta | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | parametro_minimo | 41.4698 | +1.67 | +4.20 % | sí |
| PM1.parametro | contraste_aislado | parametro_maximo | 38.1265 | -1.67 | -4.20 % | sí |
| PM1.parametro | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | perimetro_alternativo_parametro_minimo | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.parametro | contraste_aislado | perimetro_alternativo_parametro_maximo | 39.4321 | -0.37 | -0.92 % | no (varía otros parámetros) |
| PM1.convencion_anios | contraste_aislado | convencion_anios_alternativa | 39.6265 | -0.17 | -0.43 % | sí |
| PM1.convencion_anios | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.convencion_anios | contraste_aislado | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.convencion_anios | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.convencion_anios | contraste_aislado | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.convencion_anios | contraste_aislado | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.convencion_terminal | contraste_aislado | convencion_terminal_alternativa | 40.1687 | +0.37 | +0.93 % | sí |
| PM1.convencion_terminal | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.convencion_terminal | contraste_aislado | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.convencion_terminal | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.convencion_terminal | contraste_aislado | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.convencion_terminal | contraste_aislado | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.roic_terminal | variacion_conjunta_necesaria | estructura_SR2 | 40.3708 | +0.57 | +1.44 % | sí |
| PM1.roic_terminal | variacion_conjunta_necesaria | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.roic_terminal | variacion_conjunta_necesaria | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.roic_terminal | variacion_conjunta_necesaria | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.roic_terminal | variacion_conjunta_necesaria | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.roic_terminal | variacion_conjunta_necesaria | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | perimetro_alternativo | 40.4510 | +0.65 | +1.64 % | sí |
| PM1.perimetro | contraste_aislado | heredado | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | solo_N1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | solo_R1 | 42.9767 | +3.18 | +7.99 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | activa_R0_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | activa_sin_PM1 | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | perimetro_alternativo_parametro_minimo | 41.4698 | +1.67 | +4.20 % | no (varía otros parámetros) |
| PM1.perimetro | contraste_aislado | perimetro_alternativo_parametro_maximo | 39.4321 | -0.37 | -0.92 % | no (varía otros parámetros) |
