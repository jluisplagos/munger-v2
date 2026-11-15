# Elis · Historia 2016–2025 · dudas de los extractores (14-nov-2026; para la revisión independiente)

Lo que sigue son observaciones de los agentes extractores (hechos de las fuentes y sus dudas), no decisiones. Ninguna se resuelve con un umbral.

## Comunes
- **Lino frente a NIIF 16 (regla fijada):** capex y amortización incluyen el lino propio alquilado (inmovilizado), con su desglose en nota; deuda sin pasivos por arrendamiento; `arrendamientos_principal` = solo el principal NIIF 16.
- **otros_activos_financieros = 0 PENDIENTE** en 2020–2025: el balance no tiene línea de depósitos (están dentro de caja, nota 8.4). Cero comprobado solo con revisión.
- **I+D = null** (dato ausente): se describe sin importe.

## 2020–2022
- Intereses: una única línea neta que incluye los de arrendamientos; el informe no los separa.
- `circulante_lineas` incluye «Other changes» y «Employee benefits» (marcadas dudosas).
- Acciones diluidas de 2021: 241,5 M en el informe de 2022 frente a 237,4 M en el de 2021; la nota 10.3 no lo explica.
- Reexpresiones: cada informe reexpresa el año anterior (NIIF 3); el de 2021, además, por la decisión del IFRS IC sobre la NIC 19 y una reclasificación de costes.

## 2023–2025
- **2024 (informe en francés):** 10 importes con miles separados por espacio («4 573,7») que `comprobar-anio` rechazaba como «no numéricos». Corregido el analizador (los miles con espacio se aceptan); se volverá a comprobar el año.
- Intereses no homogéneos: 2023 «Net interest paid» (90,2) incluye los de arrendamientos; 2024–2025 los excluyen (van en los pagos de arrendamientos). En 2024–2025 `arrendamientos_principal` sale de la nota de derechos de uso (125,0 y 148,3).
- Pagos en acciones: importe NIIF 2 sin cargas sociales (22,9 / 27,1 / 34,7); la nota de personal de 2023 da 31,1 con ellas.
- Acciones diluidas del año anterior cambian entre informes: 2023 263,5 → 262,6 M; 2024 260,56 → 260,93 M.
- Reexpresiones: 2022 en el informe de 2023 (NIIF 3, Lavartex, nota 1.4); 2024 en el de 2025 (NIIF 3: Carsan, Wasned, Wäscherei Ernst).

## 2016–2019
- **2016 (francés, miles de EUR):** 51 importes con miles separados por espacio («1 512 764») rechazados como «no numéricos»; misma corrección del analizador que 2024. 2017–2019 (millones de EUR) dan OK.
- Ceros pendientes con cita: arrendamientos y arrendamientos_principal en 2016–2018 (antes de la NIIF 16); otros_activos_financieros en los cuatro años.
- Null: I+D en los cuatro años; en 2019, el «anterior» de arrendamientos (el balance de 2018 imprime «-») y de arrendamientos_principal (el (3,0) de esa línea es arrendamiento financiero NIC 17, no NIIF 16).
- Deuda: incluye el crédit-bail NIC 17 (2016–2018), los convertibles y el préstamo del fondo de participación de los empleados; nunca pasivos NIIF 16. La da de 2019 incluye 69,2 de derechos de uso, desglosados en nota.
- Intereses: siempre netos pagados en financiación; en 2019 incluyen los de arrendamientos.
- sbc: tomado de la nota de gastos de personal, que no coincide con la línea del estado de flujos (2016: 5,408 frente a 4,744).
- 2017: el subtotal «LOANS» 2.583,8 no cuadra con sus líneas; se usó el total «BORROWINGS», que coincide con el balance.
- 2018: en el texto extraído, los importes de adquisiciones del estado de flujos salen separados de sus conceptos; asignados por orden y contrastados con la tabla reexpresada. **Revisar contra el PDF.**
- Acciones diluidas de 2018 distintas entre los informes 2018 y 2019.
- Reexpresiones: 2015–2017 por NIIF 3; 2017 además por NIIF 5 (Clinical Solutions); 2018 solo el balance (NIIF 3); NIIF 16 aplicada sin reexpresar.
