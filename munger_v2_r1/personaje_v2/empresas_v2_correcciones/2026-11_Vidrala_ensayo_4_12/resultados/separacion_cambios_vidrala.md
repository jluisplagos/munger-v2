# Vidrala · cambios de software, configuración, datos y juicios frente al piloto 4.11

- **Software:** el control con las palancas de la 4.11 y el código final CONCUERDA con el piloto (V, ponderado, precio de Sí, zona, 13 variantes, 0 celdas económicas distintas): efecto en la valoración 0.
- **Configuración económica:** parámetros que varían entre el piloto y el cierre: ninguno; protocolo del objetivo None → objetivo_condicionado (no es una celda económica).
- **Datos:** 216 entradas económicas; piloto frente a control: 0 distintas.
- **Juicios:** entre el control (palancas de la 4.11) y el cierre cambian 3 entradas económicas (Palancas!B14, Palancas!C14, Palancas!D14): efecto en el precio de Sí -1.724 € y en el ponderado -1.918 € (V -1.239, -1.713, -3.216).

| Valoración | Precio de Sí | Ponderado | Zona |
|---|---|---|---|
| piloto | 57.742292 | 62.615109 | caro |
| control | 57.742292 | 62.615109 | caro |
| cierre | 56.018090 | 60.696637 | caro |

Celdas de juicio que cambian frente al piloto 4.11 (fases A y B):

- fase_a: B66: 'La energía más barata se traslada al cliente por las fórmulas de precio y por las bajadas que la empresa ya supone para 2026, el volumen europeo sigue flojo y el margen vuelve hacia el de 2021-2022: la mejora se la queda el cliente.' → 'La energía más barata se va al cliente con bajadas de precio mientras el volumen europeo sigue débil y la capacidad se ajusta: el margen vuelve hacia la parte baja de su ciclo y la mejora de costes se la queda el cliente.'; C27: 'Estable' → 'Expandiendo'; C66: 'Vidrala vende algo más de volumen en un mercado maduro y mueve el precio con sus costes, con retraso, como en 2022-2024: el margen se queda en la meseta posterior a 2020 y el ahorro de energía se reparte entre la empresa y el cliente.' → 'Volumen en torno al 1 % anual con precios que siguen a los costes con retraso: el margen se queda en su media de ciclo, la escala regional sostiene un retorno por encima del sector y la energía barata se reparte entre la empresa y el cliente.'; D66: 'Brasil y Chile crecen en euros con márgenes altos y Europa conserva parte del ahorro de energía con electricidad propia y hornos renovados: la mejora se la queda Vidrala porque su coste baja más deprisa que su precio.' → 'Brasil y Chile crecen en euros con márgenes por encima de los europeos y Europa retiene parte del ahorro de energía y electrificación: la empresa se queda la mejora porque la escala local la protege, y la caja sobrante vuelve al accionista.'
- fase_b: Palancas!B14: -0.01 → -0.015; Palancas!C14: 0.025 → 0.015; Palancas!D14: 0.045 → 0.035
