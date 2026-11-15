# Vidrala · efecto mecánico de las correcciones de entradas (rama 4.14)

**Qué es.** Copias del libro evaluado 4.13 congelado con las fases A, B y C fijas, en las que se escriben los datos corregidos en la rama (por grupo y todos juntos) y, aparte, las opciones de las decisiones pendientes; recalculadas con LibreOffice. Mide el efecto de los DATOS con todo lo demás fijo. **No es la valoración de la rama** (que rehace las fases con agentes reales) y **ninguna decisión se adopta**.

**Reproducción del caso activo:** sí (precio de Sí 56,01809 frente a 56,01809 de precio.json).

**Celdas de entradas que cambian en la rama:** 2.

| Caso | Celdas (antes → después) | Precio de Sí | Δ frente a la activa 4.13 | Δ frente a la rama (todas las correcciones) | Ponderado | Zona |
|---|---|---|---|---|---|---|
| activa 4.13 (reproducción) | — | 56,01809 | 0,00000 | — | 60,697 | caro |
| corrección · Historia fila 13 | H!K13 -241,668 → -224,000 | 56,00201 | -0,01609 | — | 60,674 | caro |
| corrección · Historia fila 8 | H!F8 97,091 → 91,088 | 56,01809 | 0,00000 | — | 60,697 | caro |
| TODAS las correcciones de la rama | H!F8 97,091 → 91,088; H!K13 -241,668 → -224,000 | 56,00201 | -0,01609 | — | 60,674 | caro |
| decisión (no adoptada) · E1 · medias exactas C46 y C47 · sobre la activa | A!C46 335,400 → 335,413; A!C47 169,700 → 169,668 | 56,01809 | 0,00000 | — | 60,697 | caro |
| decisión (no adoptada) · E1 · medias exactas C46 y C47 · con todas las correcciones | A!C46 335,400 → 335,413; A!C47 169,700 → 169,668 | 56,00201 | -0,01609 | 0,00000 | 60,674 | caro |
| decisión (no adoptada) · E2 · K14 sin la plusvalía de Italia (≈34,447) · sobre la activa | H!K14 84,994 → 34,447 | 56,07066 | 0,05257 | — | 60,770 | caro |
| decisión (no adoptada) · E2 · K14 sin la plusvalía de Italia (≈34,447) · con todas las correcciones | H!K14 84,994 → 34,447 | 56,05107 | 0,03298 | 0,04906 | 60,743 | caro |
| decisión (no adoptada) · E2 · K14 alternativa (≈33,594) · sobre la activa | H!K14 84,994 → 33,594 | 56,07164 | 0,05355 | — | 60,772 | caro |
| decisión (no adoptada) · E2 · K14 alternativa (≈33,594) · con todas las correcciones | H!K14 84,994 → 33,594 | 56,05198 | 0,03389 | 0,04998 | 60,744 | caro |
| decisión (no adoptada) · E3 · pareja B de 2023 (J8 97,865; J14 89,866) · sobre la activa | H!J8 87,210 → 97,865; H!J14 78,805 → 89,866 | 56,02832 | 0,01023 | — | 60,711 | caro |
| decisión (no adoptada) · E3 · pareja B de 2023 (J8 97,865; J14 89,866) · con todas las correcciones | H!J8 87,210 → 97,865; H!J14 78,805 → 89,866 | 56,01192 | -0,00617 | 0,00991 | 60,688 | caro |
| decisión (no adoptada) · E4 · intereses en financiación C48 = 2,254 · sobre la activa | A!C48 0,000 → 2,254 | 56,01809 | 0,00000 | — | 60,697 | caro |
| decisión (no adoptada) · E4 · intereses en financiación C48 = 2,254 · con todas las correcciones | A!C48 0,000 → 2,254 | 56,00201 | -0,01609 | 0,00000 | 60,674 | caro |
