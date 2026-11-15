# Especificación breve para integrar N1–N3 y P-M1 (no se construye en la 4.10)

**Objetivo.** Que la plantilla V6.3, o una versión siguiente identificada, pueda representar:
- N1, el tipo normalizado (T1 22,05 %, 4.7);
- N2, el margen de partida de continuadas (M1 18,55 %);
- N3, la regla de reinversión asimétrica (R1: solo se libera circulante);
- P-M1, la separación de reposición y crecimiento.

Todo ello sin elegir ninguna estructura por el valor que da, y conservando el S2C y el ROIC terminal.

## 1. Entradas y celdas que faltan

| Tema | Hoy | Qué falta |
|---|---|---|
| N1 · tipo | `Diagnóstico V6!C11 = Historia!C52` (media de 5 años del efectivo), el mismo en el motor y en r_op | Una celda de entrada opcional, «tipo normalizado (convención)», con su procedencia. Vacía, se usa C52. Decidir si r_op usa el mismo τ (B4 de la 4.10) |
| N2 · margen de partida | `C10` según Palancas C8 (último año o media del ciclo) | Una celda de entrada «margen de partida manual», con perímetro (continuadas) y fuente |
| N3 · reinversión | Reinversión = g ÷ ROIC, simétrica; liberación de capital en el MALO | Una regla asimétrica seleccionable (R1: solo se libera circulante) y la serie de capital liberable |
| P-M1 · reposición | Reposición = amortización en todos los escenarios | Reposición separada: λ (reposición ÷ amortización) o capex de reposición por año; crecimiento aparte; estructura SR1, SR2 o SRF y θ declarados por una persona; ROIC_lp neto o bruto de reposición (Q-ROIC1) |

## 2. Reglas que hoy no representa la plantilla

- La reposición distinta de la amortización, y su descuento histórico (D-N3e).
- La reinversión asimétrica.
- Un τ distinto en el escudo de la deuda.
- El margen de partida manual con perímetro.
- La liquidez no caja con la definición explícita (D-N4-OAF), si se activara.

## 3. Dependencias

Cada cambio alcanza a lo siguiente:
- en el Motor: el FCF por año, el terminal (reinversión g ÷ ROIC_lp) y el valor por acción;
- las anclas de la Historia (S2C marginal y medio, ROIC medio);
- la calibración de `f`;
- la escalera (`precio_de_si.py`), los diagnósticos (Diagnóstico V6 §3) y el DCF inverso (C86);
- el verificador de integridad (`v6/referencia/referencia_V6.3.json`), que necesitará una referencia nueva identificada;
- `rellenar_fase1_v63.py` y `comprobar_entrada_v63.py` (entradas nuevas) y las fases B y C (justificación de las convenciones).

## 4. Pruebas de aceptación

1. **Con las celdas nuevas vacías,** la plantilla reproduce la referencia mecánica heredada byte a byte en los valores: MALO 53,670420; NORMAL 70,772197; BUENO 86,488762; ponderado 70,495154; precio de Sí 65,688087. Es la regresión obligatoria.
2. **Con N1 y N2 informados** (T1 y M1, R1), reproduce la combinación de la 4.7: ponderado 69,24 y precio de Sí 64,26, mecánicos.
3. **Con las estructuras de P-M1,** reproduce las cifras de la 4.8.1 que les correspondan: hueco 68,92, suma 61,63, suma con el S2C reestimado 62,47 / 63,66, suma con la inversión fija reestimada 65,38 y θ de 50,2 a 69,3. Ninguna estructura se elige por defecto.
4. **Identidades comprobadas aparte,** como en `variantes_4_10.py`: r_op, puente, denominador y dividendo.
5. **Integridad:** `verificar_v63.py` ÍNTEGRO con la referencia nueva, y la 4.10 sin cambios con la anterior.
6. **Las baterías** de `verificar_paquete.sh completa` siguen pasando; además, una batería nueva de la plantilla, obligatoria, con los casos 1–4.
7. **Ninguna aprobación se hereda:** una ejecución nueva del personaje con una auditoría nueva del material.
