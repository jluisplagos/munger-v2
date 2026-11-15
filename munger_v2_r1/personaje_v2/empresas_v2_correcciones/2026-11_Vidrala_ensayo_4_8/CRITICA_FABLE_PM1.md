# Crítica independiente con Fable · P-M1 (primera versión del análisis)

**Qué es este documento:**
- es el informe final del agente que trabajó con Fable, transcrito sin cambios de contenido; solo se ha ajustado el formato;
- es salida de un modelo, no una comprobación externa;
- revisó la **primera versión** de `scripts/analisis_pm1.py`, con λ central = 1,10 y sin las alternativas P5 y P6;
- trabajó con contexto separado y en modo de solo lectura sobre el árbol, con cálculos propios en un temporal de la sesión, que no se conserva;
- su fecha es el 10-nov-2026.

Su efecto en la versión entregada está en `INFORME_PM1.md` §8 y en `REGISTRO_ENTREGA_4.8.md` §4.

---

**Veredicto.**
- La regla del hueco es correcta como identidad y el doble cómputo de X41 existe.
- La conclusión «la reposición apenas mueve el valor» (P1 +0,01; P4 −1,80) no se sostiene. Sale de fijar λ = 1,10 con el indicio más bajo disponible y de no explorar ninguna alternativa en la que el exceso de inversión sea estructural en nivel.
- La envolvente adversa coherente está entre −5 y −13 puntos de ponderado, no en −1,8 ni en −20,6.

## Bloqueante

**B1. El abanico de alternativas está truncado y descalificar X41 es excesivo.**
- **Hecho (cálculo propio).** X41 con la regla del hueco da un ponderado de 61,57 (−7,67) y un precio de Sí de 54,16 (−10,1). Se calcula con el exceso de 2025, 55,6 M€/año, descontando la inversión fija neta ya pagada y con el terminal igual. Por escenario: 35,64 / 62,79 / 83,86.
- **Interpretación:**
  - de los −20,64 de X41, unos −13 (63 %) son doble cómputo y −7,7 (37 %) no lo son;
  - lo no duplicado en diez años es 555 (MALO), 246 (NORMAL) y 93 (BUENO);
  - «sobre todo doble cómputo» es defendible; «descartada», no;
  - la distancia entre P1 y −7,7 no viene de la regla, sino de sustituir el exceso observado (1,42 × D&A) por λ = 1,10.
- **Propuesta.** Incorporar una alternativa de nivel estructural con hueco y redactar la conclusión como rango.

## Importantes

**I1. La regla del hueco es correcta, pero su suficiencia descansa en que el S2C sea un parámetro causal.**
- C53 incluye por construcción el exceso de capex sobre D&A.
- El exceso medio de 2021–2025 fue 45,9 M€/año, con ventas nominales creciendo al 8,2 %. El NORMAL crece al 2 % y solo genera 28–34 M€/año de inversión fija neta.
- Exceso medio con hueco: ponderado 64,72 (−4,52).
- El NORMAL y el BUENO son insensibles a λ hasta umbrales altos:
  - en el terminal el adicional solo aparece con λ > 1,127 (MALO), 1,249 (NORMAL) y 1,318 (BUENO);
  - P-M1 queda, de hecho, trasladada al S2C y al ROIC_lp.
- La referencia ya invierte 1,21 × D&A el año 1 en el NORMAL.
- La inversión bruta sobre ventas cae del 10,8 % al 9,3 % (NORMAL) y del 11,7 % al 8,7 % (BUENO) en el año 10.

**I2. El MALO es coherente con R1, pero no con una lectura real única.**
- −1 % nominal con un 2 % de inflación supone unas ventas reales un 20 % menores en el año 10. Caben dos lecturas:
  - erosión de precio con la capacidad conservada: λ × D&A es correcto;
  - caída de volumen: no hace falta reponerlo todo, pero faltan costes de cierre.
- El sesgo neto es pequeño y más bien prudente.
- El terminal del MALO es frágil: la holgura es de 3,5 M€; con λ = 1,20, el adicional es 9,4.

**I3. λ = 1,10 es el borde bajo de lo defendible y el indicio del Reino Unido es débil.**
- El 1,095 promedia 1,365 (2018–2022) y 0,787 (2023–2025).
- La entrada de The Park y la reestructuración de 2025 afectan al ratio, y ocho años no cubren una campaña.
- Otros ratios: todos los segmentos 2019–2025, 1,49; grupo 2016–2025, 1,32; Iberia, 1,97.
- Contraste por balance: 1 + π × valor neto ÷ dotación = 1,16–1,19 al 2 % y 1,24–1,29 al 3 %.
- Propuesta: central 1,15 y rango 1,10–1,25.
- Los bienes totalmente amortizados indican una ola de reposición y una D&A de 2025 no estacionaria; no miden λ.

**I4. Falta una alternativa: la intensidad de inversión real.** λ no recoge el encarecimiento real de conservar la competitividad (electrificación). Propone un suelo de inversión bruta en % de las ventas, con hueco:

| Suelo | Δ ponderado |
|---|---|
| 10,6 % | −0,6 a −1,9 |
| 11,5 % | −3,1 a −5,2 |
| 12,9 % perpetuo | −11,3 a −13,5 |

## Menores

- **M1.** No hay doble cómputo entre λ y el margen. La D&A subirá, y un EBIT del 18 % exige un EBITDA del 27–28 %, dentro de lo histórico; conviene declararlo.
- **M2.** Negar el escudo fiscal al desfase estacionario es correcto si la D&A crece con las ventas. En el MALO no crece, así que es una omisión prudente de unos +0,3–0,4 €/acción.
- **M3.** P0 depende de que la amortización de la cartera sea deducible. Cuando se agota, el EBIT sube unos 0,3 puntos, y eso no se modela.
- **M4.** La D&A es constante en los años 1–10 y proporcional a las ventas en el terminal. Con λ = 1,10 no tiene efecto.
- **M5.** P3 es irrelevante, y P4 no merece el nombre de combinación adversa.

## Respuesta a la pregunta (d)

−20 no es alcanzable de forma coherente, porque exigiría negar que C53 ya contiene el exceso. Lo más cercano es tomar el nivel de 2025 como estructural, sin retorno en margen: de −7,7 (exceso plano con hueco) a −13,5 (12,9 % de las ventas, perpetuo).
