# Viscofan · dominios de las estructuras de P-M1 con cada perímetro (encargo 4.13 §7)

**Qué es.** Cotas calculadas con las bases de cada libro recalculado: la activa es NIIF 16 y la variante `perimetro_alternativo` es Caja. Son hechos de la especificación con estas bases. La cota de la 4.12 (λ ≤ 1,1413 para SRF) era de la base Caja y no se traslada a la de NIIF 16.

| | NIIF 16 | Caja |
|---|---|---|
| D_hist (B57) | 320,599 | 296,489 |
| Exceso histórico (B60) | 64,923 | 40,813 |
| F_hist (B62) | 81,084 | 56,974 |
| Amortización que se repone A (B63) | 403,132 | 403,132 |
| Λ · λ máximo con f definida (SR1, SR2) | 1,7953 | 1,7355 |
| Λ · λ máximo con f_fija > 0 (SRF) | 1,2011 | 1,1413 |
| Θ · θ = 0,0 · f (SR1, SR2) | 1,0000 | 1,0000 |
| Θ · θ = 0,0 · f_fija (SRF) | 1,0000 | 1,0000 |
| Θ · θ = 0,5 · f (SR1, SR2) | 1,1127 | 1,0739 |
| Θ · θ = 0,5 · f_fija (SRF) | 0,5997 | 0,6418 |
| Θ · θ = 1,0 · f (SR1, SR2) | 1,2539 | 1,1596 |
| Θ · θ = 1,0 · f_fija (SRF) | 0,1993 | 0,2837 |
| 1 ÷ NWC | 2,0711 | 2,0711 |
| f a partir del cual la inversión fija para crecer sería negativa en el BUENO (S2C 1,4) | 1,4793 | 1,4793 |

**Lectura.** Con Θ, las tres estructuras que reestiman están definidas en todo θ ∈ [0, 1] con los dos perímetros. El f máximo es 1,2539 (NIIF 16) y 1,1596 (Caja), por debajo del umbral de la inversión fija negativa (1,4793). Ninguna variante calculada sale del dominio: no hay avisos activos en `configuracion_v64_variantes.md`. Con Λ, que no está declarada, NIIF 16 amplía el dominio de SRF hasta λ ≈ 1,201. Ninguna cota se recorta para obtener un valor.
