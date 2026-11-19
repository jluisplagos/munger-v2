# Comprobación de entrada · Ahold_v63_evaluada.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Faltan palancas de crecimiento (Palancas B14:D14)) · estado del libro: NO LISTO · incompleto (5 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: CALCULABLE
- Motor B: CALCULABLE
- Motor C: CALCULABLE
- Motor elegido por la fase A: A → calculable

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- ninguno

## Necesario para LISTO · PROVISIONAL (no para el valor)

- evidencia Historia!C23:L23: Pasivo por arrendamientos: cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, arrendamientos; 2016, 2017): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.
- evidencia Historia!C26:L26: Minoritarios: cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, minoritarios; 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V28 AVISO: Precio y acciones con fechas separadas más de 90 días (Palancas C45, C46)
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
