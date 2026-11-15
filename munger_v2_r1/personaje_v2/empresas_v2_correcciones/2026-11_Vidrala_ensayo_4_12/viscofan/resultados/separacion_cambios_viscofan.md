# Viscofan · cambios de mecánica, configuración, datos y juicios frente al expediente heredado

**Qué es.** La separación que pide el encargo 4.12 §8. Solo lee. «Heredado» es el expediente de origen (`personaje_v2/empresas_v2/Viscofan`, V6.3), reproducido con el código final; «experimental 4.12» es el expediente nuevo con agentes reales.

- **Mecánica:** la reproducción del heredado con el código final COINCIDE con el origen en V6.3 y en V6.4 heredado (|Δ| = 0): efecto en la valoración 0.
- **Motor:** heredado `No · financiación cambia mucho` → 4.12 `No · financiación cambia mucho`; los dos valoran con el motor B.
- **Entradas económicas** (216; reproducción del heredado frente al expediente nuevo): 15 distintas — configuracion: Configuración V6.4!B11, Configuración V6.4!B16, Configuración V6.4!B28, Configuración V6.4!B29, Configuración V6.4!B30, Configuración V6.4!B31, Configuración V6.4!B36, Configuración V6.4!B37, Configuración V6.4!B39, Configuración V6.4!B4, Configuración V6.4!B40, Configuración V6.4!B41, Configuración V6.4!B42, Configuración V6.4!B43; juicio: Palancas!B15.
- **Juicios:** efecto en el precio de Sí -1.245 € y en el ponderado -0.623 € (variante «heredado» del expediente nuevo, con sus palancas, frente a la reproducción del heredado, con las del origen).
- **Configuración económica:** efecto en el precio de Sí -2.518 € y en el ponderado -2.674 € (activa frente a la variante «heredado»). Componentes aislados frente al heredado: solo_N1 -1.452 €; solo_R1 +0.000 €; activa_sin_PM1 -1.452 €; activa -2.518 € (no aditivos).

| Valoración | Precio de Sí | Ponderado | V MALO / NORMAL / BUENO | Zona |
|---|---|---|---|---|
| heredado_origen | 43.050965 | 46.882147 | 35.3886 / 47.5600 / 63.3265 | caro |
| variante_heredado_4_12 | 41.805836 | 46.259582 | 32.8983 / 47.5600 / 63.3265 | caro |
| activa_4_12 | 39.287701 | 43.585325 | 30.6925 / 44.8547 / 59.9959 | caro |

Celdas de juicio que cambian frente al heredado (fases A y B; texto recortado):

- fase_a: B66: 'Las pieles bovinas, el gas y el dólar suben más deprisa que los precios de venta, la mezcl' → 'Pieles bovinas, energía, CO2 y aranceles suben el coste más deprisa de lo que la empresa t'; C27: 'Estable' → 'Comprimiendo'; C66: 'El volumen crece con el mercado y algo de cuota, los precios siguen a los costes con un añ' → 'El volumen crece con el mercado (2–4 % anual) y algo de cuota por la sustitución de tripa '; D66: 'La capacidad nueva de colágeno y plásticos (EE. UU., México, Serbia, Tailandia) se llena, ' → 'La capacidad nueva de colágeno y plásticos (EE. UU., México, Serbia) se llena con volumen '
- fase_b: Palancas!B15: '0.15' → '0.14'
