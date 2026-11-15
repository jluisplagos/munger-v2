# Réplica independiente de la escalera de precio · expedientes finales 4.14

Revisión interna (agente de réplica, contexto limpio). Fecha: 14-nov-2026. Tolerancia: 1e-6 relativa; texto y booleanos, igualdad exacta.

## Veredicto

- **Escalera de los tres expedientes: reproducida.** Comparaciones con resultados.json, precio.json y caché del libro: 185 PASA, 0 FALLA. La mayor diferencia relativa en V_MALO, V_NORMAL, V_BUENO, el ponderado y el precio de Sí es de unos 3,5e-15, es decir, error de redondeo en coma flotante.
- **Efecto aislado del denominador (Viscofan y Elis): reproducido.** 89 PASA, 0 FALLA frente a los ficheros de efecto, con todos sus casos (incluidos los de dilución).
- La zona es «caro» en los tres expedientes, y en todas las variantes del denominador.
- No he ajustado nada para que cuadre. Hubo un emparejamiento erróneo, mío, en la primera pasada (Elis, ver §5). Lo corregí cambiando con qué caso se compara, no el cálculo.

## 1. Método

- Código propio en `replica.py`. No importa ningún script del proyecto ni usa LibreOffice. Los libros se abren con openpyxl, sin guardar nada.
- **Solo se leen constantes.** `Libro.inp()` lee del libro abierto con `data_only=False` y lanza una excepción si la celda pedida es una fórmula. Así ningún resultado intermedio del libro entra en el cálculo.
- **Única lectura de caché usada para calcular:** el estado técnico del Motor (`B252` bloqueo, `B253` moneda comparable, `B254`, `B255` = «COMPLETO Y VÁLIDO»). Son 49 reglas (filas 201–249) que no he reimplementado. Solo deciden si hay lectura, no el valor.
- Cadena reimplementada a partir de las fórmulas del libro:
  - Historia: series 29–31 y anclas C43, C44, C48, C49, C52, C58 (f), C63, C64, C65, C66 y C70.
  - Análisis: C52.
  - Configuración V6.4: B5–B93, las 28 o 29 comprobaciones de §9 y la sección 11 NIIF 16 de la V6.4.1.
  - Diagnóstico V6: C5, C9–C12, C15 (r operativa) y C16.
  - Motor, filas 6–8: rama heredada y rama experimental (BU:DY), hasta BE…BK.
  - Análisis C78 y C83.
  - Tabla del DCF inverso: Motor 56–136, Análisis B108:B188, B191–B193 y C86.
  - Escalera del Anexo C: P* en forma cerrada (C.3) contrastado con una bisección propia, precio de Sí = mín(P*, V_NORMAL), zona, G, L, crecimiento implícito, distancias y regla antigua C156.
- Plantillas: el Motor de Vidrala es idéntico al de Viscofan. Su Configuración no tiene la sección 11 (B153 y B124 vacías). Elis (V6.3) no tiene la hoja Configuración V6.4 y su Motor solo tiene la rama heredada. Esto lo comprueba `difform.py`.
- Supuestos activos que la réplica tuvo que reproducir:
  - Viscofan: R1, SR1 con familia Θ (θ = 0,5), legado, perímetro NIIF 16 (Σ altas = 24,11) y t NOPAT = 22,12 %.
  - Vidrala: R1, SR1 con familia Λ (λ = 1,15), cartera P0 explícita (filas 93), m0 manual (N2 = 18,547 %), «Media del ciclo» y t = 22,05 %.
  - Elis: motor A con f = 0,04168 (Historia C58) y quiebra p = 5 % con recuperación 0.
- Pruebas propias de la forma cerrada (`pruebas_anexo_C.py`): los 5 casos del Anexo C.5 y sus propiedades (G = 3L en P*, P* ≥ mín V, P* ≤ ponderado, independencia del orden, P* decrece con k). Todo PASA.
- Comprobación adicional (`replica_sobre_recalc.py`): la réplica ejecutada sobre las copias `recalc/` da lo mismo (dif. rel. ≤ 3,4e-15). La copia `recalc/` difiere de la evaluada solo en la serialización de LibreOffice. Las constantes quedan con 15 cifras significativas (dif. rel. máxima 5,1e-15). El resto son textos de fórmula reescritos: «+(0.0)» pasa a «+(0)», «'Análisis'!» a «Análisis!» y «TRUE» a «TRUE()».

## 2. Viscofan · motor B · modo Experimental

Libro: `/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/viscofan_decisiones/Viscofan/Viscofan_v63_evaluada.xlsx`. Estado técnico (caché): {'B252': False, 'B253': True, 'B254': False, 'B255': 'COMPLETO Y VÁLIDO'}.

### Escalera frente a resultados.json y precio.json

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO (B78) | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| V_NORMAL (C78) | 43.7670991087673 | 43.7670991087673 | -4.2632564145606e-14 | 9.74e-16 | **PASA** |
| V_BUENO (D78) | 57.9469537938741 | 57.9469537938741 | 4.2632564145606e-14 | 7.36e-16 | **PASA** |
| ponderado (C83) | 43.8055904657485 | 43.8055904657485 | 3.5527136788005e-14 | 8.11e-16 | **PASA** |
| V_MALO precio.json | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| V_NORMAL precio.json | 43.7670991087673 | 43.7670991087673 | -4.2632564145606e-14 | 9.74e-16 | **PASA** |
| V_BUENO precio.json | 57.9469537938741 | 57.9469537938741 | 4.2632564145606e-14 | 7.36e-16 | **PASA** |
| ponderado precio.json | 43.8055904657485 | 43.8055904657485 | 3.5527136788005e-14 | 8.11e-16 | **PASA** |
| P* (k = 3) | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| P* por bisección (comprobación) | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| precio de Sí = mín(P*, V_NORMAL) | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| tope NORMAL aplicado | False | False | — | — | **PASA** |
| precio del escenario MALO | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| precio actual (C37) | 54.7 | 54.7 | 0 | 0.00e+00 | **PASA** |
| zona | caro | caro | — | — | **PASA** |
| G(P*) | 6.01109539593504 | 6.01109539593505 | 5.32907051820075e-15 | 8.87e-16 | **PASA** |
| L(P*) | 2.00369846531168 | 2.00369846531168 | 1.33226762955019e-15 | 6.65e-16 | **PASA** |
| tabla del DCF inverso utilizable | True | True | — | — | **PASA** |
| g implícito al precio actual | 0.100910476763644 | 0.100910476763644 | 1.52655665885959e-16 | 1.51e-15 | **PASA** |
| g implícito al precio de Sí | 0.0197733082069579 | 0.0197733082069578 | -1.11022302462516e-16 | 5.61e-15 | **PASA** |
| distancia a precio de Sí | 0.272427906122026 | 0.272427906122026 | 4.9960036108132e-16 | 1.83e-15 | **PASA** |
| distancia a MALO | 0.455581330739181 | 0.455581330739182 | 6.10622663543836e-16 | 1.34e-15 | **PASA** |
| C86 frente a g implícito réplica | 0.100910476763644 | 0.100910476763644 | -2.63677968348475e-16 | 2.61e-15 | **PASA** |
| regla antigua C156 = mín(MALO, 0,75 × ponderado) · precio.json | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| regla antigua C156 · resultados.json | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| propiedades: |G − 3L| en P* < 1e-9 · P* ≥ mín V · P* ≤ ponderado | (Anexo C.2) | /F(P*)/ = 8.88e-15 | — | — | **PASA** |

### Pasos intermedios frente a la caché del libro (diagnóstico)

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| Diagnóstico V6!C9 V0 | 1251.983 | 1251.983 | 0 | 0.00e+00 | **PASA** |
| Diagnóstico V6!C10 m0 | 0.163575703503961 | 0.163575703503961 | 3.33066907387547e-16 | 2.04e-15 | **PASA** |
| Diagnóstico V6!C11 t | 0.221190838053599 | 0.221190838053599 | -4.71844785465692e-16 | 2.13e-15 | **PASA** |
| Diagnóstico V6!C12 f | 0.0192483426422769 | 0.0192483426422769 | -2.42861286636753e-17 | 1.26e-15 | **PASA** |
| Diagnóstico V6!C15 r_op | 0.0826769373447879 | 0.0826769373447879 | -4.16333634234434e-17 | 5.04e-16 | **PASA** |
| Diagnóstico V6!C16 pasivos netos | 273.828 | 273.828 | 0 | 0.00e+00 | **PASA** |
| Configuración V6.4!B76 | True | True | — | — | **PASA** |
| Configuración V6.4!B77 | True | True | — | — | **PASA** |
| Configuración V6.4!B78 | True | True | — | — | **PASA** |
| Configuración V6.4!B83 | 0.482846013084842 | 0.482846013084842 | 2.22044604925031e-16 | 4.60e-16 | **PASA** |
| Configuración V6.4!B84 | 1.1135523703749 | 1.1135523703749 | 4.88498130835069e-15 | 4.39e-15 | **PASA** |
| Configuración V6.4!B87 | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| Configuración V6.4!B88 | 6.49230000000001 | 6.4923 | -1.15463194561016e-14 | 1.78e-15 | **PASA** |
| Configuración V6.4!B89 | 6.49230000000001 | 6.4923 | -1.15463194561016e-14 | 1.78e-15 | **PASA** |
| Configuración V6.4!B90 | True | True | — | — | **PASA** |
| Motor!BE6 MALO | 832.423401955027 | 832.423401955027 | -4.54747350886464e-13 | 5.46e-16 | **PASA** |
| Motor!BF6 MALO | 130.450606796523 | 130.450606796523 | -4.54747350886464e-13 | 3.49e-15 | **PASA** |
| Motor!BH6 MALO | 811.074277831367 | 811.074277831367 | -3.41060513164848e-13 | 4.21e-16 | **PASA** |
| Motor!BI6 MALO | 1369.66967978639 | 1369.66967978639 | 3.41060513164848e-12 | 2.49e-15 | **PASA** |
| Motor!BJ6 MALO | 1369.66967978639 | 1369.66967978639 | 3.41060513164848e-12 | 2.49e-15 | **PASA** |
| Motor!BK6 MALO | 29.7797012085668 | 29.7797012085668 | -3.5527136788005e-14 | 1.19e-15 | **PASA** |
| Motor!BD6 MALO | 133.691053806867 | 133.691053806867 | 0 | 0.00e+00 | **PASA** |
| Motor!BE7 NORMAL | 957.544263275165 | 957.544263275165 | -3.41060513164848e-13 | 3.56e-16 | **PASA** |
| Motor!BF7 NORMAL | 184.379888806939 | 184.379888806939 | 2.27373675443232e-13 | 1.23e-15 | **PASA** |
| Motor!BH7 NORMAL | 1329.28138910691 | 1329.28138910691 | 1.81898940354586e-12 | 1.37e-15 | **PASA** |
| Motor!BI7 NORMAL | 2012.99765238208 | 2012.99765238208 | -3.63797880709171e-12 | 1.81e-15 | **PASA** |
| Motor!BJ7 NORMAL | 2012.99765238208 | 2012.99765238208 | -3.63797880709171e-12 | 1.81e-15 | **PASA** |
| Motor!BK7 NORMAL | 43.7670991087673 | 43.7670991087673 | -4.2632564145606e-14 | 9.74e-16 | **PASA** |
| Motor!BD7 NORMAL | 196.954815447775 | 196.954815447775 | -8.5265128291212e-14 | 4.33e-16 | **PASA** |
| Motor!BE8 BUENO | 1098.34419123021 | 1098.34419123021 | -3.41060513164848e-12 | 3.11e-15 | **PASA** |
| Motor!BF8 BUENO | 234.944293304231 | 234.944293304231 | -3.97903932025656e-13 | 1.69e-15 | **PASA** |
| Motor!BH8 BUENO | 1840.66117544601 | 1840.66117544601 | 4.54747350886464e-13 | 2.47e-16 | **PASA** |
| Motor!BI8 BUENO | 2665.17736667622 | 2665.17736667622 | -3.18323145620525e-12 | 1.19e-15 | **PASA** |
| Motor!BJ8 BUENO | 2665.17736667622 | 2665.17736667622 | -3.18323145620525e-12 | 1.19e-15 | **PASA** |
| Motor!BK8 BUENO | 57.9469537938741 | 57.9469537938741 | 4.2632564145606e-14 | 7.36e-16 | **PASA** |
| Motor!BD8 BUENO | 260.728917989419 | 260.728917989419 | -1.13686837721616e-13 | 4.36e-16 | **PASA** |
| Motor!B191 | 80 | 80 | 0 | 0.00e+00 | **PASA** |
| Motor!B193 | ✓ PASA | ✓ PASA | — | — | **PASA** |
| Análisis!B108:B188 (máx. dif. rel.) | 81 celdas | 3.714199771559e-15 | — | 3.71e-15 | **PASA** |

Réplica sobre la copia recalc/:

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO | 29.7797012085668 | 29.7797012085667 | -6.03961325396085e-14 | 2.03e-15 | **PASA** |
| V_NORMAL | 43.7670991087673 | 43.7670991087672 | -8.5265128291212e-14 | 1.95e-15 | **PASA** |
| V_BUENO | 57.9469537938741 | 57.9469537938741 | -2.1316282072803e-14 | 3.68e-16 | **PASA** |
| ponderado | 43.8055904657485 | 43.8055904657485 | -7.105427357601e-15 | 1.62e-16 | **PASA** |
| P* | 39.7981935351252 | 39.7981935351251 | -6.3948846218409e-14 | 1.61e-15 | **PASA** |
| precio de Sí | 39.7981935351252 | 39.7981935351251 | -6.3948846218409e-14 | 1.61e-15 | **PASA** |
| zona | caro | caro | — | — | **PASA** |

## 3. Vidrala · motor B · modo Experimental

Libro: `/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/vidrala_decisiones/Vidrala/Vidrala_v63_evaluada.xlsx`. Estado técnico (caché): {'B252': False, 'B253': True, 'B254': False, 'B255': 'COMPLETO Y VÁLIDO'}.

### Escalera frente a resultados.json y precio.json

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO (B78) | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| V_NORMAL (C78) | 60.1901164149973 | 60.1901164149973 | 0 | 0.00e+00 | **PASA** |
| V_BUENO (D78) | 78.4785189164147 | 78.4785189164147 | 1.4210854715202e-14 | 1.81e-16 | **PASA** |
| ponderado (C83) | 60.6741181667017 | 60.6741181667017 | -7.105427357601e-15 | 1.17e-16 | **PASA** |
| V_MALO precio.json | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| V_NORMAL precio.json | 60.1901164149973 | 60.1901164149973 | 0 | 0.00e+00 | **PASA** |
| V_BUENO precio.json | 78.4785189164147 | 78.4785189164147 | 1.4210854715202e-14 | 1.81e-16 | **PASA** |
| ponderado precio.json | 60.6741181667017 | 60.6741181667017 | -7.105427357601e-15 | 1.17e-16 | **PASA** |
| P* (k = 3) | 56.0020051682446 | 56.0020051682446 | -2.1316282072803e-14 | 3.81e-16 | **PASA** |
| P* por bisección (comprobación) | 56.0020051682446 | 56.0020051682446 | -2.1316282072803e-14 | 3.81e-16 | **PASA** |
| precio de Sí = mín(P*, V_NORMAL) | 56.0020051682446 | 56.0020051682446 | -2.1316282072803e-14 | 3.81e-16 | **PASA** |
| tope NORMAL aplicado | False | False | — | — | **PASA** |
| precio del escenario MALO | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| precio actual (C37) | 90.1 | 90.1 | 0 | 0.00e+00 | **PASA** |
| zona | caro | caro | — | — | **PASA** |
| G(P*) | 7.00816949768563 | 7.00816949768565 | 1.95399252334028e-14 | 2.79e-15 | **PASA** |
| L(P*) | 2.33605649922854 | 2.33605649922855 | 2.66453525910038e-15 | 1.14e-15 | **PASA** |
| tabla del DCF inverso utilizable | True | True | — | — | **PASA** |
| g implícito al precio actual | 0.14290199276465 | 0.14290199276465 | 1.66533453693773e-16 | 1.17e-15 | **PASA** |
| g implícito al precio de Sí | -0.00833075662055754 | -0.00833075662055758 | -3.98986399474666e-17 | 4.79e-15 | **PASA** |
| distancia a precio de Sí | 0.378446113559993 | 0.378446113559993 | 2.22044604925031e-16 | 5.87e-16 | **PASA** |
| distancia a MALO | 0.508082989210856 | 0.508082989210856 | 3.33066907387547e-16 | 6.56e-16 | **PASA** |
| C86 frente a g implícito réplica | 0.14290199276465 | 0.14290199276465 | 5.55111512312578e-17 | 3.88e-16 | **PASA** |
| regla antigua C156 = mín(MALO, 0,75 × ponderado) · precio.json | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| regla antigua C156 · resultados.json | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| propiedades: |G − 3L| en P* < 1e-9 · P* ≥ mín V · P* ≤ ponderado | (Anexo C.2) | /F(P*)/ = 7.11e-15 | — | — | **PASA** |

### Pasos intermedios frente a la caché del libro (diagnóstico)

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| Diagnóstico V6!C9 V0 | 1465.16 | 1465.16 | 0 | 0.00e+00 | **PASA** |
| Diagnóstico V6!C10 m0 | 0.185466721361995 | 0.185466721361995 | 1.94289029309402e-16 | 1.05e-15 | **PASA** |
| Diagnóstico V6!C11 t | 0.220541332769837 | 0.220541332769837 | 0 | 0.00e+00 | **PASA** |
| Diagnóstico V6!C12 f (vacío: caché None ≡ réplica "") | None |  | — | — | **PASA** |
| Diagnóstico V6!C15 r_op | 0.0868915167432047 | 0.0868915167432047 | 4.16333634234434e-17 | 4.79e-16 | **PASA** |
| Diagnóstico V6!C16 pasivos netos | 160.784 | 160.784 | 2.8421709430404e-14 | 1.77e-16 | **PASA** |
| Configuración V6.4!B76 | True | True | — | — | **PASA** |
| Configuración V6.4!B77 | True | True | — | — | **PASA** |
| Configuración V6.4!B78 | True | True | — | — | **PASA** |
| Configuración V6.4!B83 | 0.147037866171613 | 0.147037866171613 | -2.77555756156289e-16 | 1.89e-15 | **PASA** |
| Configuración V6.4!B84 | 1.15874757336707 | 1.15874757336707 | -3.33066907387547e-15 | 2.87e-15 | **PASA** |
| Configuración V6.4!B87 | 0.15 | 0.15 | -8.32667268468867e-17 | 5.55e-16 | **PASA** |
| Configuración V6.4!B88 | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| Configuración V6.4!B89 | 19.9422 | 19.9422 | -1.06581410364015e-14 | 5.34e-16 | **PASA** |
| Configuración V6.4!B90 | True | True | — | — | **PASA** |
| Motor!BE6 MALO | 1019.7235737058 | 1019.7235737058 | 3.97903932025656e-12 | 3.90e-15 | **PASA** |
| Motor!BF6 MALO | 123.908826562453 | 123.908826562453 | 4.12114786740858e-13 | 3.33e-15 | **PASA** |
| Motor!BH6 MALO | 700.425301382137 | 700.425301382137 | -3.41060513164848e-13 | 4.87e-16 | **PASA** |
| Motor!BI6 MALO | 1559.36487508794 | 1559.36487508794 | 6.82121026329696e-13 | 4.37e-16 | **PASA** |
| Motor!BJ6 MALO | 1559.36487508794 | 1559.36487508794 | 6.82121026329696e-13 | 4.37e-16 | **PASA** |
| Motor!BK6 MALO | 44.3217226721019 | 44.3217226721019 | -3.5527136788005e-14 | 8.02e-16 | **PASA** |
| Motor!BD6 MALO | 136.897021387343 | 136.897021387343 | 4.2632564145606e-13 | 3.11e-15 | **PASA** |
| Motor!BE7 NORMAL | 1186.04117484327 | 1186.04117484327 | 2.04636307898909e-12 | 1.73e-15 | **PASA** |
| Motor!BF7 NORMAL | 168.118681631118 | 168.118681631118 | -5.6843418860808e-14 | 3.38e-16 | **PASA** |
| Motor!BH7 NORMAL | 1092.40314398905 | 1092.40314398905 | -2.50111042987555e-12 | 2.29e-15 | **PASA** |
| Motor!BI7 NORMAL | 2117.66031883232 | 2117.66031883232 | -9.09494701772928e-13 | 4.29e-16 | **PASA** |
| Motor!BJ7 NORMAL | 2117.66031883232 | 2117.66031883232 | -9.09494701772928e-13 | 4.29e-16 | **PASA** |
| Motor!BK7 NORMAL | 60.1901164149973 | 60.1901164149973 | 0 | 0.00e+00 | **PASA** |
| Motor!BD7 NORMAL | 189.72534092582 | 189.72534092582 | 1.70530256582424e-13 | 8.99e-16 | **PASA** |
| Motor!BE8 BUENO | 1335.15701419843 | 1335.15701419843 | -3.41060513164848e-12 | 2.55e-15 | **PASA** |
| Motor!BF8 BUENO | 225.940943399256 | 225.940943399256 | -4.83169060316868e-13 | 2.14e-15 | **PASA** |
| Motor!BH8 BUENO | 1586.72557288811 | 1586.72557288811 | -3.41060513164848e-12 | 2.15e-15 | **PASA** |
| Motor!BI8 BUENO | 2761.09858708653 | 2761.09858708653 | 2.72848410531878e-12 | 9.88e-16 | **PASA** |
| Motor!BJ8 BUENO | 2761.09858708653 | 2761.09858708653 | 2.72848410531878e-12 | 9.88e-16 | **PASA** |
| Motor!BK8 BUENO | 78.4785189164147 | 78.4785189164147 | 1.4210854715202e-14 | 1.81e-16 | **PASA** |
| Motor!BD8 BUENO | 254.596346963687 | 254.596346963686 | -5.11590769747272e-13 | 2.01e-15 | **PASA** |
| Motor!B191 | 80 | 80 | 0 | 0.00e+00 | **PASA** |
| Motor!B193 | ✓ PASA | ✓ PASA | — | — | **PASA** |
| Análisis!B108:B188 (máx. dif. rel.) | 81 celdas | 4.56904069809349e-15 | — | 4.57e-15 | **PASA** |

Réplica sobre la copia recalc/:

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO | 44.3217226721019 | 44.3217226721018 | -4.9737991503207e-14 | 1.12e-15 | **PASA** |
| V_NORMAL | 60.1901164149973 | 60.1901164149973 | 0 | 0.00e+00 | **PASA** |
| V_BUENO | 78.4785189164147 | 78.4785189164147 | 1.4210854715202e-14 | 1.81e-16 | **PASA** |
| ponderado | 60.6741181667017 | 60.6741181667017 | -1.4210854715202e-14 | 2.34e-16 | **PASA** |
| P* | 56.0020051682446 | 56.0020051682446 | -2.1316282072803e-14 | 3.81e-16 | **PASA** |
| precio de Sí | 56.0020051682446 | 56.0020051682446 | -2.1316282072803e-14 | 3.81e-16 | **PASA** |
| zona | caro | caro | — | — | **PASA** |

## 4. Elis · motor A · modo V6.3 (sin hoja de configuración)

Libro: `/home/claude/trabajo_4_14/trabajo/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14/elis_decisiones/Elis/Elis_v63_evaluada.xlsx`. Estado técnico (caché): {'B252': False, 'B253': True, 'B254': False, 'B255': 'COMPLETO Y VÁLIDO'}.

### Escalera frente a resultados.json y precio.json

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO (B78) | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| V_NORMAL (C78) | 7.82436495245035 | 7.82436495245035 | 4.44089209850063e-15 | 5.68e-16 | **PASA** |
| V_BUENO (D78) | 10.89154926695 | 10.89154926695 | -3.73034936274053e-14 | 3.42e-15 | **PASA** |
| ponderado (C83) | 7.98957836734924 | 7.98957836734924 | 0 | 0.00e+00 | **PASA** |
| V_MALO precio.json | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| V_NORMAL precio.json | 7.82436495245035 | 7.82436495245035 | 4.44089209850063e-15 | 5.68e-16 | **PASA** |
| V_BUENO precio.json | 10.89154926695 | 10.89154926695 | -3.73034936274053e-14 | 3.42e-15 | **PASA** |
| ponderado precio.json | 7.98957836734924 | 7.98957836734924 | 0 | 0.00e+00 | **PASA** |
| P* (k = 3) | 7.30205532309094 | 7.30205532309094 | -4.44089209850063e-15 | 6.08e-16 | **PASA** |
| P* por bisección (comprobación) | 7.30205532309094 | 7.30205532309094 | -3.5527136788005e-15 | 4.87e-16 | **PASA** |
| precio de Sí = mín(P*, V_NORMAL) | 7.30205532309094 | 7.30205532309094 | -4.44089209850063e-15 | 6.08e-16 | **PASA** |
| tope NORMAL aplicado | False | False | — | — | **PASA** |
| precio del escenario MALO | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| precio actual (C37) | 24.18 | 24.18 | 0 | 0.00e+00 | **PASA** |
| zona | caro | caro | — | — | **PASA** |
| G(P*) | 1.03128456638746 | 1.03128456638746 | -1.11022302462516e-15 | 1.08e-15 | **PASA** |
| L(P*) | 0.343761522129152 | 0.343761522129152 | -1.66533453693773e-16 | 4.84e-16 | **PASA** |
| tabla del DCF inverso utilizable | False | False | — | — | **PASA** |
| g implícito al precio actual | no utilizable | no utilizable | — | — | **PASA** |
| g implícito al precio de Sí | no utilizable | no utilizable | — | — | **PASA** |
| distancia a precio de Sí | 0.698012600368447 | 0.698012600368448 | 1.11022302462516e-16 | 1.59e-16 | **PASA** |
| distancia a MALO | 0.769096455233864 | 0.769096455233864 | 0 | 0.00e+00 | **PASA** |
| regla antigua C156 = mín(MALO, 0,75 × ponderado) · precio.json | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| regla antigua C156 · resultados.json | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| propiedades: |G − 3L| en P* < 1e-9 · P* ≥ mín V · P* ≤ ponderado | (Anexo C.2) | /F(P*)/ = 1.11e-15 | — | — | **PASA** |

### Pasos intermedios frente a la caché del libro (diagnóstico)

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| Diagnóstico V6!C9 V0 | 4796.8 | 4796.8 | 0 | 0.00e+00 | **PASA** |
| Diagnóstico V6!C10 m0 | 0.131337558372248 | 0.131337558372248 | 1.66533453693773e-16 | 1.27e-15 | **PASA** |
| Diagnóstico V6!C11 t | 0.2882 | 0.2882 | 0 | 0.00e+00 | **PASA** |
| Diagnóstico V6!C12 f | 0.0416814552737959 | 0.0416814552737959 | -2.77555756156289e-17 | 6.66e-16 | **PASA** |
| Diagnóstico V6!C15 r_op | — | — | — | — | **PASA** |
| Diagnóstico V6!C16 pasivos netos | — | — | — | — | **PASA** |
| Motor!BE6 MALO | 688.694086788754 | 688.694086788754 | 2.27373675443232e-13 | 3.30e-16 | **PASA** |
| Motor!BF6 MALO | 128.329299529238 | 128.329299529238 | 1.70530256582424e-13 | 1.33e-15 | **PASA** |
| Motor!BH6 MALO | 677.5960370313 | 677.5960370313 | 3.41060513164848e-13 | 5.03e-16 | **PASA** |
| Motor!BI6 MALO | 1366.29012382005 | 1366.29012382005 | 4.77484718430787e-12 | 3.49e-15 | **PASA** |
| Motor!BJ6 MALO | 1297.97561762905 | 1297.97561762905 | 2.04636307898909e-12 | 1.58e-15 | **PASA** |
| Motor!BK6 MALO | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| Motor!BD6 MALO | 131.464271789004 | 131.464271789004 | -3.97903932025656e-13 | 3.03e-15 | **PASA** |
| Motor!BE7 NORMAL | 656.646616578569 | 656.646616578568 | -5.6843418860808e-13 | 8.66e-16 | **PASA** |
| Motor!BF7 NORMAL | 208.482102060691 | 208.482102060691 | -3.69482222595252e-13 | 1.77e-15 | **PASA** |
| Motor!BH7 NORMAL | 1258.07275649665 | 1258.07275649665 | 2.72848410531878e-12 | 2.17e-15 | **PASA** |
| Motor!BI7 NORMAL | 1914.71937307522 | 1914.71937307522 | 1.36424205265939e-12 | 7.13e-16 | **PASA** |
| Motor!BJ7 NORMAL | 1818.98340442146 | 1818.98340442146 | 2.27373675443232e-13 | 1.25e-16 | **PASA** |
| Motor!BK7 NORMAL | 7.82436495245035 | 7.82436495245035 | 4.44089209850063e-15 | 5.68e-16 | **PASA** |
| Motor!BD7 NORMAL | 214.476759327578 | 214.476759327578 | 2.55795384873636e-13 | 1.19e-15 | **PASA** |
| Motor!BE8 BUENO | 943.269945012413 | 943.269945012413 | -2.27373675443232e-13 | 2.41e-16 | **PASA** |
| Motor!BF8 BUENO | 264.983256956192 | 264.983256956192 | 4.54747350886464e-13 | 1.72e-15 | **PASA** |
| Motor!BH8 BUENO | 1722.02755976481 | 1722.02755976481 | 4.09272615797818e-12 | 2.38e-15 | **PASA** |
| Motor!BI8 BUENO | 2665.29750477723 | 2665.29750477723 | -3.18323145620525e-12 | 1.19e-15 | **PASA** |
| Motor!BJ8 BUENO | 2532.03262953837 | 2532.03262953837 | -4.54747350886464e-12 | 1.80e-15 | **PASA** |
| Motor!BK8 BUENO | 10.89154926695 | 10.89154926695 | -3.73034936274053e-14 | 3.42e-15 | **PASA** |
| Motor!BD8 BUENO | 286.777628439703 | 286.777628439703 | -5.6843418860808e-14 | 1.98e-16 | **PASA** |
| Motor!B191 | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| Motor!B193 | ⚠ REVISAR · con tus palancas crecer destruye valor: el DCF inverso no aplica | ⚠ REVISAR · con tus palancas crecer destruye valor: el DCF inverso no aplica | — | — | **PASA** |
| Análisis!B108:B188 (máx. dif. rel.) | 81 celdas | 4.68807677973821e-15 | — | 4.69e-15 | **PASA** |

Réplica sobre la copia recalc/:

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| V_MALO | 5.58324771244518 | 5.58324771244518 | -3.5527136788005e-15 | 6.36e-16 | **PASA** |
| V_NORMAL | 7.82436495245035 | 7.82436495245035 | 4.44089209850063e-15 | 5.68e-16 | **PASA** |
| V_BUENO | 10.89154926695 | 10.89154926695 | -3.73034936274053e-14 | 3.42e-15 | **PASA** |
| ponderado | 7.98957836734924 | 7.98957836734924 | 0 | 0.00e+00 | **PASA** |
| P* | 7.30205532309094 | 7.30205532309094 | -4.44089209850063e-15 | 6.08e-16 | **PASA** |
| precio de Sí | 7.30205532309094 | 7.30205532309094 | -4.44089209850063e-15 | 6.08e-16 | **PASA** |
| zona | caro | caro | — | — | **PASA** |

## 5. Efecto aislado del denominador (Análisis C55)

Los ficheros de efecto miden cada caso **sobre el libro anterior**: `viscofan/Viscofan/…_evaluada.xlsx` (rama 4.14) y `elis_motor_A/Elis/…_evaluada.xlsx`. Por eso apliqué a esos libros, con mi réplica, las celdas de cada caso y comparé el resultado. Además medí el efecto en el **libro final**: cambié solo C55 al valor anterior y dejé todo lo demás fijo.

Entradas que cambian entre el libro anterior y el final (`diffinputs.py`):
- Viscofan: C41, C47–C50 y C55.
- Elis: C24, C31, C33, C34, C40, C41, C42, C46, C47, C50, C53, C54, C55 e Historia I25:L25.
- Palancas, Configuración y Motor no cambian en ninguno de los dos.

### Viscofan

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| [libro anterior + celdas del caso] rama 4.14 (reproducción) · precio de Sí | 40.3028176827247 | 40.3028176827247 | 2.1316282072803e-14 | 5.29e-16 | **PASA** |
| [libro anterior + celdas del caso] rama 4.14 (reproducción) · ponderado | 44.3628981996609 | 44.3628981996609 | -1.4210854715202e-14 | 3.20e-16 | **PASA** |
| [libro anterior + celdas del caso] rama 4.14 (reproducción) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] rama 4.14 (reproducción) · r operativa | 0.0826034488326509 | 0.0826034488326509 | -2.77555756156289e-17 | 3.36e-16 | **PASA** |
| [libro anterior + celdas del caso] rama 4.14 (reproducción) · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo el denominador C55 = 45,993399 (E fijo) · precio de Sí | 39.8522463773885 | 39.8522463773885 | -7.105427357601e-15 | 1.78e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo el denominador C55 = 45,993399 (E fijo) · ponderado | 43.8669366242773 | 43.8669366242774 | 4.9737991503207e-14 | 1.13e-15 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo el denominador C55 = 45,993399 (E fijo) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] D3 · solo el denominador C55 = 45,993399 (E fijo) · r operativa | 0.0826034488326509 | 0.0826034488326509 | -2.77555756156289e-17 | 3.36e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo el denominador C55 = 45,993399 (E fijo) · Δ precio de Sí | -0.450571305336211 | -0.45057130533624 | -2.8421709430404e-14 | 6.31e-14 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar) · precio de Sí | 40.2481537165748 | 40.2481537165748 | -2.1316282072803e-14 | 5.30e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar) · ponderado | 44.3008584586809 | 44.3008584586809 | 3.5527136788005e-14 | 8.02e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar) · r operativa | 0.0826769373447879 | 0.0826769373447879 | -4.16333634234434e-17 | 5.04e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar) · Δ precio de Sí | -0.0546639661498673 | -0.05466396614991 | -4.2632564145606e-14 | 7.80e-13 | **PASA** |
| [libro anterior + celdas del caso] D3 · denominador y capitalización (E recalculado) · precio de Sí | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · denominador y capitalización (E recalculado) · ponderado | 43.8055904657485 | 43.8055904657485 | 3.5527136788005e-14 | 8.11e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · denominador y capitalización (E recalculado) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] D3 · denominador y capitalización (E recalculado) · r operativa | 0.0826769373447879 | 0.0826769373447879 | -4.16333634234434e-17 | 5.04e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 · denominador y capitalización (E recalculado) · Δ precio de Sí | -0.5046241475995 | -0.50462414759955 | -4.9737991503207e-14 | 9.86e-14 | **PASA** |
| [libro anterior + celdas del caso] E1 · medias exactas C47–C50 · precio de Sí | 40.3028176827247 | 40.3028176827247 | 2.1316282072803e-14 | 5.29e-16 | **PASA** |
| [libro anterior + celdas del caso] E1 · medias exactas C47–C50 · ponderado | 44.3628981996609 | 44.3628981996609 | -1.4210854715202e-14 | 3.20e-16 | **PASA** |
| [libro anterior + celdas del caso] E1 · medias exactas C47–C50 · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E1 · medias exactas C47–C50 · r operativa | 0.0826034488326509 | 0.0826034488326509 | -2.77555756156289e-17 | 3.36e-16 | **PASA** |
| [libro anterior + celdas del caso] E1 · medias exactas C47–C50 · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] D3 + E1 · todo · precio de Sí | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 + E1 · todo · ponderado | 43.8055904657485 | 43.8055904657485 | 3.5527136788005e-14 | 8.11e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 + E1 · todo · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] D3 + E1 · todo · r operativa | 0.0826769373447879 | 0.0826769373447879 | -4.16333634234434e-17 | 5.04e-16 | **PASA** |
| [libro anterior + celdas del caso] D3 + E1 · todo · Δ precio de Sí | -0.5046241475995 | -0.50462414759955 | -4.9737991503207e-14 | 9.86e-14 | **PASA** |
| [libro anterior + celdas del caso] dilución · D3 aplicado (denominador y capitalización) · precio de Sí | 39.7981935351252 | 39.7981935351252 | -2.8421709430404e-14 | 7.14e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · D3 aplicado (denominador y capitalización) · ponderado | 43.8055904657485 | 43.8055904657485 | 3.5527136788005e-14 | 8.11e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · D3 aplicado (denominador y capitalización) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, objetivo (+0,315 M) · precio de Sí | 39.527477396492 | 39.527477396492 | 2.1316282072803e-14 | 5.39e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, objetivo (+0,315 M) · ponderado | 43.5076151244565 | 43.5076151244565 | 4.2632564145606e-14 | 9.80e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, objetivo (+0,315 M) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, máximo (+0,4725 M) · precio de Sí | 39.393495749221 | 39.393495749221 | -2.1316282072803e-14 | 5.41e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, máximo (+0,4725 M) · ponderado | 43.3601424718323 | 43.3601424718323 | -3.5527136788005e-14 | 8.19e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución · + dilución potencial del plan 2025–2027, máximo (+0,4725 M) · zona | caro | caro | — | — | **PASA** |
| [libro final con C55 = 45.479209] ≡ caso «D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar)» · precio de Sí | 40.2481537165748 | 40.2481537165748 | -2.1316282072803e-14 | 5.30e-16 | **PASA** |
| [libro final con C55 = 45.479209] ≡ caso «D3 · solo la capitalización C41 = 54,70 × 45,993399 (denominador sin cambiar)» · ponderado | 44.3008584586809 | 44.3008584586809 | 3.5527136788005e-14 | 8.02e-16 | **PASA** |
| [libro final con C55 = 45.479209] · zona (sin caso en el fichero) | caro | caro | — | — | **PASA** |

Efecto en el libro final (C55 45.993399 frente a 45.479209, todo lo demás fijo):

- V (MALO, NORMAL, BUENO) con C55 nuevo: [29.7797012086, 43.7670991088, 57.9469537939]; con C55 anterior: [30.1163918613, 44.2619319167, 58.6021046821].
- Ponderado: 43.8055904657485 frente a 44.3008584586809 (Δ = -0.495267992932398).
- Precio de Sí: 39.7981935351252 frente a 40.2481537165748 (Δ = -0.44996018144964). Zona: caro / caro.
- Cociente del precio de Sí = 0.988820352242286; cociente de acciones (anterior ÷ nuevo) = 0.988820352242286.
- El mismo efecto medido sobre el libro anterior, según el fichero: Δ = -0.450571305336211; mi réplica lo reproduce (tabla de arriba).

### Elis

| Magnitud | Expediente | Réplica | Diferencia (réplica − expediente) | Dif. relativa | Veredicto |
|---|---|---|---|---|---|
| [libro anterior + celdas del caso] expediente anterior elis_motor_A (reproducción) · precio de Sí | 6.5563403246103 | 6.5563403246103 | -8.88178419700125e-16 | 1.35e-16 | **PASA** |
| [libro anterior + celdas del caso] expediente anterior elis_motor_A (reproducción) · ponderado | 7.17350245848518 | 7.17350245848518 | -1.77635683940025e-15 | 2.48e-16 | **PASA** |
| [libro anterior + celdas del caso] expediente anterior elis_motor_A (reproducción) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] expediente anterior elis_motor_A (reproducción) · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo el denominador C55 = 232,47681 (E fijo) · precio de Sí | 7.30654068302828 | 7.30654068302828 | -2.66453525910038e-15 | 3.65e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo el denominador C55 = 232,47681 (E fijo) · ponderado | 7.99432075787504 | 7.99432075787504 | 2.66453525910038e-15 | 3.33e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo el denominador C55 = 232,47681 (E fijo) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · solo el denominador C55 = 232,47681 (E fijo) · Δ precio de Sí | 0.750200358417979 | 0.750200358417977 | -1.77635683940025e-15 | 2.37e-15 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo la capitalización C41 = 24,18 × 232,47681 · precio de Sí | 6.5563403246103 | 6.5563403246103 | -8.88178419700125e-16 | 1.35e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo la capitalización C41 = 24,18 × 232,47681 · ponderado | 7.17350245848518 | 7.17350245848518 | -1.77635683940025e-15 | 2.48e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · solo la capitalización C41 = 24,18 × 232,47681 · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · solo la capitalización C41 = 24,18 × 232,47681 · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] E6 · acciones y capitalización · precio de Sí | 7.30654068302828 | 7.30654068302828 | -2.66453525910038e-15 | 3.65e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · acciones y capitalización · ponderado | 7.99432075787504 | 7.99432075787504 | 2.66453525910038e-15 | 3.33e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · acciones y capitalización · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · acciones y capitalización · Δ precio de Sí | 0.750200358417979 | 0.750200358417977 | -1.77635683940025e-15 | 2.37e-15 | **PASA** |
| [libro anterior + celdas del caso] E6 · pensiones I25:L25 (déficit de prestación definida) · precio de Sí | 6.5563403246103 | 6.5563403246103 | -8.88178419700125e-16 | 1.35e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · pensiones I25:L25 (déficit de prestación definida) · ponderado | 7.17350245848518 | 7.17350245848518 | -1.77635683940025e-15 | 2.48e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · pensiones I25:L25 (déficit de prestación definida) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · pensiones I25:L25 (déficit de prestación definida) · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50 · precio de Sí | 6.55231549979876 | 6.55231549979876 | 2.66453525910038e-15 | 4.07e-16 | **PASA** |
| [libro anterior + celdas del caso] supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50 · ponderado | 7.16924699374636 | 7.16924699374636 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50 · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50 · Δ precio de Sí | -0.00402482481154554 | -0.00402482481154198 | 3.5527136788005e-15 | 8.83e-13 | **PASA** |
| [libro anterior + celdas del caso] E6 · entradas reexpresadas a 2025 (C24, C31, C33, C34, C40, C42, C53, C54) · precio de Sí | 6.5563403246103 | 6.5563403246103 | -8.88178419700125e-16 | 1.35e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · entradas reexpresadas a 2025 (C24, C31, C33, C34, C40, C42, C53, C54) · ponderado | 7.17350245848518 | 7.17350245848518 | -1.77635683940025e-15 | 2.48e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · entradas reexpresadas a 2025 (C24, C31, C33, C34, C40, C42, C53, C54) · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · entradas reexpresadas a 2025 (C24, C31, C33, C34, C40, C42, C53, C54) · Δ precio de Sí | 0 | 0 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] E6 · todo · precio de Sí | 7.30205532309094 | 7.30205532309094 | -4.44089209850063e-15 | 6.08e-16 | **PASA** |
| [libro anterior + celdas del caso] E6 · todo · ponderado | 7.98957836734924 | 7.98957836734924 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] E6 · todo · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] E6 · todo · Δ precio de Sí | 0.745714998480637 | 0.745714998480634 | -3.5527136788005e-15 | 4.76e-15 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · conversión de la OCEANE: + 23,355764 M acciones y C48 sin el cupón · precio de Sí | 7.15555822649856 | 7.15555822649855 | -3.5527136788005e-15 | 4.96e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · conversión de la OCEANE: + 23,355764 M acciones y C48 sin el cupón · ponderado | 7.81012086053621 | 7.81012086053621 | 0 | 0.00e+00 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · conversión de la OCEANE: + 23,355764 M acciones y C48 sin el cupón · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · conversión de la OCEANE: + 23,355764 M acciones y C48 sin el cupón · Δ precio de Sí | 0.599217901888253 | 0.599217901888251 | -2.66453525910038e-15 | 4.45e-15 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento vivas (+ 2,613905 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · precio de Sí | 7.22086590257594 | 7.22086590257595 | 6.21724893790088e-15 | 8.61e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento vivas (+ 2,613905 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · ponderado | 7.90074457890164 | 7.90074457890164 | -3.5527136788005e-15 | 4.50e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento vivas (+ 2,613905 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento vivas (+ 2,613905 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · Δ precio de Sí | 0.664525577965641 | 0.664525577965648 | 7.105427357601e-15 | 1.07e-14 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento al 120 % (+ 3,136686 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · precio de Sí | 7.20484419091043 | 7.20484419091044 | 7.99360577730113e-15 | 1.11e-15 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento al 120 % (+ 3,136686 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · ponderado | 7.883214347307 | 7.883214347307 | -3.5527136788005e-15 | 4.51e-16 | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento al 120 % (+ 3,136686 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · zona | caro | caro | — | — | **PASA** |
| [libro anterior + celdas del caso] dilución potencial (NO incorporada) · acciones de rendimiento al 120 % (+ 3,136686 M) · COTA: C50 (SBC) sigue restando su coste, posible doble cómputo parcial · Δ precio de Sí | 0.648503866300129 | 0.648503866300138 | 8.88178419700125e-15 | 1.37e-14 | **PASA** |
| [libro final con C55 = 259.077654] ≡ caso «supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50» · precio de Sí | 6.55231549979876 | 6.55231549979876 | 2.66453525910038e-15 | 4.07e-16 | **PASA** |
| [libro final con C55 = 259.077654] ≡ caso «supuesto de la orquestación (precedente E1) · medias exactas C46, C47, C50» · ponderado | 7.16924699374636 | 7.16924699374636 | 0 | 0.00e+00 | **PASA** |
| [libro final con C55 = 259.077654] · zona (sin caso en el fichero) | caro | caro | — | — | **PASA** |

Efecto en el libro final (C55 232.47681 frente a 259.077654, todo lo demás fijo):

- V (MALO, NORMAL, BUENO) con C55 nuevo: [5.5832477124, 7.8243649525, 10.8915492669]; con C55 anterior: [5.0099867649, 7.0209968955, 9.7732575174].
- Ponderado: 7.98957836734924 frente a 7.16924699374636 (Δ = 0.82033137360288).
- Precio de Sí: 7.30205532309094 frente a 6.55231549979876 (Δ = 0.749739823292176). Zona: caro / caro.
- Cociente del precio de Sí = 1.11442364509389; cociente de acciones (anterior ÷ nuevo) = 1.11442364509389.
- El mismo efecto medido sobre el libro anterior, según el fichero: Δ = 0.750200358417979; mi réplica lo reproduce (tabla de arriba).

**Lectura.** El efecto del denominador es un reescalado exacto, por tres razones:
- C55 solo entra en BK = BJ ÷ C55.
- La r operativa del motor B usa la capitalización C41, no C55. En el motor A, la tasa es C56.
- P*, el precio de Sí y el ponderado son homogéneos de grado 1 en V.

Por eso el cociente del precio de Sí coincide con el de acciones hasta ~1e-15, y la zona no cambia.

La pequeña diferencia entre la Δ medida en el libro anterior y la Δ medida en el libro final no es un error: el reescalado se aplica a un V distinto en cada libro.
- Viscofan: −0,450571 frente a −0,449960. Cambia C41, y con ella la r operativa: 0,0826034 frente a 0,0826769.
- Elis: +0,750200 frente a +0,749740. Cambian C46, C47 y C50, y con ellas f (Historia C58).

**Lo que corregí durante la revisión.** En la primera pasada comparé «Elis final con el C55 anterior» con el caso «solo la capitalización» del fichero (6,556340), y salió FALLA (dif. rel. 6,1e-4). La causa estaba en mi emparejamiento, no en ninguno de los dos cálculos. El libro final de Elis también lleva las medias exactas de C46, C47 y C50, que en el motor A cambian f a través de C52 → C70 → C58. Así que lo que equivale a «final con el C55 anterior» es el caso «medias exactas» (6,552315). Contra ese caso cuadra con dif. rel. 4e-16. En Viscofan (motor B) esas celdas no intervienen, y la equivalencia con «solo la capitalización» sí es correcta.

## 6. Lo que no he reproducido y por qué

- **Estado técnico del Motor (B252–B255)** y las 49 reglas de las filas 201–249: lo leo de la caché. Solo condiciona que haya lectura; en los tres libros es «COMPLETO Y VÁLIDO», sin bloqueo y con moneda comparable. Sí compruebo por mi cuenta que Palancas C48 = Control maestro H4 = «EUR», que es lo que exige C15.
- **Motor C**: no lo he implementado; ninguno de los tres expedientes lo usa.
- **Aviso de la tasa de descuento** (Diagnóstico V6 C221, tornado), `coincide_C86` y la validez V6.4 que dan los ficheros de efecto (`valida_v64`): no los he reimplementado. No forman parte de la escalera.
- **Comprobaciones de la Configuración V6.4 (§9)**: están implementadas según sus fórmulas, pero solo se han ejercitado en la rama válida (B90 = VERDADERO en Viscofan y Vidrala).
- **Precio de Elis**: la escalera cuadra, pero precio.json avisa de que la tabla del DCF inverso no es utilizable (B191 = 0: «crecer destruye valor»). La réplica también da «no utilizable». El fichero de efecto advierte además que, con arrendamientos NIIF 16 en el motor A, el precio de Sí no es una conclusión utilizable. Eso es una cuestión de modelo y queda fuera de lo que una réplica aritmética puede validar.

## 7. Archivos (todos en este directorio)

- `replica.py`: motor de réplica (Historia, Configuración, Diagnóstico, Motor, tabla inversa y escalera).
- `ejecutar.py`: ejecución y comparaciones; escribe `salida_replica.json` y `salida_consola.txt`.
- `replica_sobre_recalc.py`: la misma réplica sobre las copias `recalc/`; escribe `salida_replica_recalc.json`.
- `pruebas_anexo_C.py`: casos C.5 del Anexo C.
- `difform.py`, `diffinputs.py`, `dump.py`: inspección de fórmulas y entradas, solo lectura.
- `generar_informe.py`: genera este informe a partir de los JSON.

Se ejecuta con `python3 -B ejecutar.py && python3 -B replica_sobre_recalc.py && python3 -B pruebas_anexo_C.py && python3 -B generar_informe.py`. No se ha modificado ningún archivo del proyecto: tras la ejecución, `find -newer` no devuelve nada en la raíz del ensayo.
