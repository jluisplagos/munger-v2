# Casos reales de Hermès en los que el respaldo declarado no corresponde a la partida (H1, alcance)

Fuente: resultados/alcance_lineas.json (prueba pruebas/alcance_lineas.py). Comprobación solo dentro de los JSON de extracción:
los textos de los informes (texto/) no están en el paquete, así que no se ha podido abrir la página citada.

1. `Hermes/fase1_partes/AR_2018.json` · pensiones · anterior · componente 2: impreso «6.0», página 243,
   línea declarada «Post-employment and other employee benefit obligations 26 196.0 188.2».
   «6.0» solo aparece dentro de «196.0». La línea que contiene 6.0 como importe es la de la parte corriente
   («… 26 6.9 6.0»), que el mismo archivo usa para el ejercicio actual. El valor coincide con la nota del informe
   2017 (AR_2017.json: «Corriente 6.0 + no corriente 188.2»; total 194,2 = Historia 2017).
   Clasificación: respaldo mal atribuido aceptado por coincidencia de subcadena; ninguna evidencia de cifra incorrecta.

2. `Hermes/fase1_partes/AR_2024.json` · minoritarios · actual: impreso «7», página 364,
   línea declarada «Non-current assets 7,608 6,438» (otra partida). «7» solo aparece dentro de «7,608».
   La Historia de 2024 no usa esta cifra: usa el comparativo del informe 2025 (AR_2025.json p. 358,
   «Non-controlling interests 6 7»), que también da 7.
   Clasificación: respaldo de otro concepto aceptado; sin efecto en la Historia; ninguna evidencia de cifra incorrecta.
