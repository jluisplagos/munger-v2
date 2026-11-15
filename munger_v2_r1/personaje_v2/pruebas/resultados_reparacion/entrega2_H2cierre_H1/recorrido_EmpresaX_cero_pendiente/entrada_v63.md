# Comprobación de entrada · EmpresaX_cero_pendiente_v63_evaluada.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Faltan palancas de crecimiento (Palancas B14:D14)) · estado del libro: NO LISTO · incompleto (5 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: CALCULABLE
- Motor B: CALCULABLE
- Motor C: CALCULABLE
- Motor elegido por la fase A: A → calculable

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- ninguno

## Necesario para LISTO · PROVISIONAL (no para el valor)

- evidencia Análisis!C50: Stock-based compensation (SBC): no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Historia!C13:L13: Adquisiciones netas (positivo): cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, adquisiciones; 2017): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.
- evidencia Historia!C18:L18: SBC (compensación en acciones): cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, sbc; 2023, 2024, 2025): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)
- Análisis!C88: P/FCF histórico · de dónde: fase1_v63.json
- Análisis!C38: valor intrínseco de fuente externa (contraste) · de dónde: fase1_v63.json (opcional)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
