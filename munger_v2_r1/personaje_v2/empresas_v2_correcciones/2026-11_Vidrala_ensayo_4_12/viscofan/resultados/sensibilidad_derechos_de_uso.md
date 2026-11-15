# Viscofan · sensibilidad a la amortización de los derechos de uso (revisión interna R8; límite 13)

**Qué es.** Una lectura de sensibilidad sobre copias del libro evaluado, recalculadas con LibreOffice: el exceso histórico de la plantilla (Configuración V6.4!B60 = 40.813) frente al exceso sobre la amortización que se repone con capex (67.864, sumando la amortización de los derechos de uso de 2021–2025, 27.051). No es una variante del expediente ni una corrección adoptada.

Método: con la familia Θ, el requisito anual (θ × B60 ÷ 5) y Rh (θ × B60, que fija f en SR1) solo dependen de θ × B60, así que el exceso sin los derechos de uso se calcula escribiendo θ' = θ × B60' ÷ B60 (B60 es una fórmula protegida). θ' > 1 queda fuera del dominio declarado.

| Caso | θ de la lectura | θ escrito | B60 equivalente | Requisito anual (B88) | f (B72) | Ponderado | Precio de Sí | Zona | ¿Válida? |
|---|---|---|---|---|---|---|---|---|---|
| theta_0.5 | 0.5 | 0.5 | 40.813 | 4.081 | 1.0739 | 43.59 | 39.29 | caro | True |
| theta_0.5_rou | 0.5 | 0.831402 | 67.864 | 6.786 | 1.1292 | 42.88 | 38.58 | caro | True |
| theta_1 | 1.0 | 1.0 | 40.813 | 8.163 | 1.1596 | 42.52 | 38.22 | caro | True |
| theta_1_rou | 1.0 | 1.662804 | 67.864 | 0.000 | 1.2968 | — | — | None | False |

**Efecto en el precio de Sí** de contar solo la amortización que se repone con capex: θ = 0,5 → -0.71 €; θ = 1 → sin valor (fuera del dominio). En los casos calculados la zona no cambia (caro). Con θ = 0,5 el precio de Sí (38.58 €) queda por encima del extremo inferior del rango calculado del expediente (38,22 €). Con θ = 1 no hay cifra: el θ equivalente queda fuera del dominio declarado y la plantilla marca la configuración como no válida; para calcularlo habría que editar una fórmula protegida de la plantilla (B60), y no se hace. Queda como límite sin cifra. La medición es parcial: solo cambia el exceso (B60), no la base de reinversión de D_hist (B55) ni, por ella, f (revisión de lo afectado, RA2). Con el exceso corregido, θ = 0.6014 equivale exactamente a θ = 1 con el de la plantilla (38.22 €); un θ mayor queda fuera del dominio declarado.
