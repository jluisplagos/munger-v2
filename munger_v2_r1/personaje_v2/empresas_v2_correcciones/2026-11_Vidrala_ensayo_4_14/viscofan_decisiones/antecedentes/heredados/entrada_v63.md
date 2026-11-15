# Comprobación de entrada · Viscofan_v63_evaluada.xlsx

- Íntegro (verificar_v63.py): True · estado técnico: INCOMPLETO (Faltan palancas de crecimiento (Palancas B14:D14)) · estado del libro: NO LISTO · incompleto (5 pendientes) · comparable precio↔valor: True · años con ventas: 10

## Motores calculables (simulación con palancas de prueba)

- Motor A: CALCULABLE · NO cubierto por la configuración experimental V6.4 (solo motor B): si la fase A lo elige, el expediente termina en el límite del modelo, no en una falta de datos
- Motor B: CALCULABLE
- Motor C: CALCULABLE · NO cubierto por la configuración experimental V6.4 (solo motor B): si la fase A lo elige, el expediente termina en el límite del modelo, no en una falta de datos
- (V6.4 experimental) La calculabilidad de arriba es por datos (simulada en modo heredado). El motor se elige por los criterios del personaje, como si la configuración no existiera.
- Motor elegido por la fase A: B → calculable

## BLOQUEANTE (el pipeline se detiene: pendiente_de_datos)

- ninguno

## Necesario para LISTO · PROVISIONAL (no para el valor)

- evidencia Historia!C23:L23: Pasivo por arrendamientos: no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Historia!C26:L26: Minoritarios: no verificable · de dónde: fase1_v63.json (fuente y página del dato) o etapa 1 · el dato está pero su clasificación/documento no permite LISTO·PROVISIONAL; la fase C juzga si es material
- evidencia Historia!C17:L17: Principal de arrendamientos (IFRS 16): cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, arrendamientos_principal; 2016, 2017, 2018): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.
- evidencia Historia!C18:L18: SBC (compensación en acciones): cero pendiente de verificación · de dónde: decisión humana registrada en fase1_decisiones.json (valor, fuente con página, fecha y persona) · [H1] Depende de un cero PENDIENTE DE VERIFICACIÓN (Historia, sbc; 2016, 2017, 2018): la cita del informe no se ha contrastado con la partida. El valor se conserva; solo una decisión humana registrada en fase1_decisiones.json lo confirma.

## No bloqueante

- Palancas!C24: tamaño del mercado año 10 · de dónde: extractos (solo con cifra de fuente primaria)

## Avisos de la hoja

- V19 AVISO: Probabilidad de quiebra vacía (Palancas C22): se asume 0 por convención, no es un riesgo medido
- V28 AVISO: Precio y acciones con fechas separadas más de 90 días (Palancas C45, C46)
- V31 AVISO: Fecha de análisis escrita como texto (Análisis D4): escríbela como fecha
