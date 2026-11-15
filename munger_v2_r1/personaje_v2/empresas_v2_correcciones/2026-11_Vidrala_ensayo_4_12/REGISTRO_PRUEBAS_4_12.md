# Registro de pruebas · entrega 4.12

**Qué es.** Recoge qué se ejecutó durante el desarrollo de la 4.12, con qué resultado y dónde está la salida. Las cifras son las de las ejecuciones registradas. No se presenta como ejecutado nada que no lo esté; lo que solo se conserva (pruebas de entregas anteriores que no se repitieron en el desarrollo) se dice como tal.

**Verificación final.** Sobre una copia limpia del ZIP final, con `verificar_paquete.sh completa`, los controles históricos y `comprobar_entrega_4_12.py`. Va en el registro externo `munger_v2_r1_entrega4.12_validacion_supervisada_y_Viscofan.VERIFICACION.txt`, fuera del ZIP, porque un ZIP no puede contener su propia huella.

## 1. Batería obligatoria `personaje_v2/pruebas/test_integracion_v64.py` (127 pruebas)

Se ejecuta desde `personaje_v2/` con `python3 -B pruebas/test_integracion_v64.py [A B C D E F G]`. En `verificar_paquete.sh completa` es la primera de las obligatorias y exige al menos 127 pruebas, todas en PASA. La 4.11 tenía 58 (grupos A–D).

| Grupo | Qué prueba (4.12 en negrita) | Pruebas |
|---|---|---|
| A · plantilla | reconstrucción, verificador, V6.3 intacta, cambios declarados; **reconstrucción comparada miembro a miembro, recompresión con otra huella y el mismo contenido, huella estricta del artefacto entregado** | 12 |
| B · casos | 117 libros recalculados en secuencia con la réplica independiente (sin cambios desde la 4.11) | 21 |
| C · pipeline | selección explícita, pasada V6.4, fase C, cambio después del cierre, heredado = V6.3 (sin cambios desde la 4.11) | 21 |
| D · cambio de base | preparación reproducible, sin restos (sin cambios desde la 4.11) | 7 |
| **E · vigencia (§3)** | siete alteraciones del material × cuatro primeras llamadas independientes (pipeline, ficha, informe, resumen); selección equivocada con material intacto; plantilla, referencia o verificador alterados con el mismo nombre; resumen no actualizable | 13 |
| **F · materialidad y protocolos (§4)** | los dos protocolos y la falta de protocolo; diez contradicciones; dato ausente material (S-19) con prioridad; compra con una hipótesis experimental material sin fundamento fuera de las listas heredadas; λ sin mover; θ inactivo; comprobación conjunta ausente o inválida; estructura sin alternativas o con una que no sobrevive; barrido real de las alternativas no numéricas; **rango calculado con su ámbito en la línea de estado con el objetivo bloqueado o sin protocolo; aptitud de uso separada de la auditoría en la ficha, el informe y el resumen; cobertura de los subparámetros de PM1 solo por su ámbito aislado o por la comprobación conjunta (revisión interna R3)** | 36 |
| **G · coherencia (§5)** | variantes desactualizadas por cambios económicos y reutilizadas ante cambios editoriales; instantánea de entradas; trazabilidad; dominios; cambio de protocolo después del cierre, **con el motivo ya en el turno 1 de la fase C**; fórmula alterada después del cierre; **adquisiciones de la Historia (fila 13) en la instantánea y comparación de instantáneas antiguas con la activa (R1); avisos de fecha y valor incoherentes en la cadena de trazabilidad (R4); valores de los avisos de dominio en el informe sin comillas rectas, con la verificación de citas de los dos informes juntos (la forma anterior fallaba)** | 17 |

**Ejecuciones registradas en el desarrollo.**
- A–G completa con el código final del desarrollo: **120/120** (12-nov, 21:00–21:14; `scratchpad/f412/v64/AG_final.log`).
- Después de las correcciones del cierre (12-nov, 22:30–23:15): F **35/35** (rango en la línea de estado y aptitud de uso) y G **14/14** (motivo del cambio de protocolo en el turno 1). Total de la batería entonces: 123.
- Después de las correcciones de la revisión interna (12-nov, 23:15–23:45): F **36/36** y G **16/16** (F+G 52/52). Total de la batería entonces: 126.
- Después de la corrección de los valores de los avisos en el informe (13-nov, 00:02–00:04): G **17/17**. Total de la batería: **127**. Las demás baterías se repiten en la verificación final.
- Antes: A–G 115/115 con la versión anterior del grupo F; A+G 24/25, con la prueba de la fórmula alterada que encontró el defecto del paso 13 (se corrigió con `libros_verificados`); G 13/13 tras la corrección.

## 2. Baterías V6.3 (obligatorias; mínimos sin cambios)

| Batería | Resultado con el código final del desarrollo |
|---|---|
| `test_cierre_v2.py` | 55/55 |
| `test_auditorias_v2.py` | **55/55** (repetida con el paso 13 final; una pasada intermedia dio 7/26 con la primera versión del rebote del paso 13, que rompía los escenarios «--desde 13 directo») |
| `test_estados_v2.py` | **28/28** (repetida; la pasada intermedia, 26/28, se hizo con pipeline.py editado mientras corría) |
| `test_resumen_v2.py` | 45/45 |
| `test_integridad_auditoria_v2.py` | 103/103 |
| `test_trazabilidad_v2.py` | 78/78 |

Regla aprendida: no se edita ningún script mientras corre una batería (la huella H2 lee el código fuente en caliente).

## 3. Controles y réplicas de los expedientes (no son pruebas sintéticas)

| Control | Resultado | Salida |
|---|---|---|
| Control 4.12 con las palancas de la 4.11 (Vidrala) | CONCUERDA: precio de Sí 57,74229205598012, ponderado 62,6151093424602, 13 variantes, 0 celdas económicas distintas | `control_palancas_4_11/resultados/control_palancas.md` |
| Diferencias del piloto 4.11 con el código final (repetido tras añadir la aptitud de uso) | 5 diferencias de presentación o registro, ninguna de valoración; piloto intacto | `resultados/diferencias_piloto_4_11_codigo_final.md` |
| Reproducción del fallo de vigencia | código 4.11: rechazo con la aprobación conservada; código 4.12: retirada | `resultados/reproduccion_vigencia_*.md` |
| Viscofan: reproducción del heredado (V6.3 y V6.4 heredado) | COINCIDE, \|Δ\| = 0 (precio de Sí 43.050965031270174; ponderado 46.8821465263006) | `viscofan/resultados/reproduccion_heredado.md` |
| Viscofan: contraste de la Historia con las publicaciones recuperadas (después de la segunda entrega de fuentes) | 186 celdas contrastadas, 0 no encontradas, 0 sin publicación (15 sin cifra y 9 con cifras cortas) | `viscofan/fuentes/contraste_cifras_historia.md` |
| Viscofan: cifras del análisis de la configuración | 61 de 61 en su página | `viscofan/configuracion/analisis_configuracion_viscofan.md` |
| Réplica independiente sobre los 16 libros finales del cierre de Vidrala | 16 de 16 coinciden | `cierre_condicionado/resultados/replica_independiente.txt` |
| Réplica independiente sobre los 14 libros finales del expediente de Viscofan | 14 de 14 coinciden (valores ≤ 9,9e-14 €/acción; conciliación ≤ 4,8e-12) | `viscofan/experimental/resultados/replica_independiente.txt` |
| Vidrala: separación de cambios frente al piloto 4.11 | software 0 · configuración 0 · datos 0 · juicio −1,724 € en el precio de Sí | `resultados/separacion_cambios_vidrala.md` |
| Viscofan: separación de cambios frente al heredado | mecánica 0 · datos 0 · juicio −1,245 € · configuración −2,518 € | `viscofan/resultados/separacion_cambios_viscofan.md` |
| Vidrala: los dos protocolos sobre el mismo material | mismo material económico; solicitudes, materiales y auditorías distintas; la copia retiró la aprobación heredada | `resultados/comparacion_protocolos.md` |
| Comparación homogénea heredado/experimental | Vidrala 64,75 → 56,02 €; Viscofan 41,81 → 39,29 € (precio de Sí) | `…/resultados/comparacion_homogenea.md` de cada expediente |

<!-- MAS -->

## Verificación final antes de empaquetar (13-nov)

- **Ronda provisional (00:17–01:00)**, sobre una copia limpia del árbol anterior a la respuesta a la segunda revisión interna: `verificar_paquete.sh completa` PASA (127/127 y las demás completas, 23 min). Los controles dieron los resultados del LEEME salvo el de la 4.12, con 59 de 63: tres casos por el defecto RA1 del propio control y uno porque faltaba el LEEME. Las dos cosas se corrigieron.
- **Ronda definitiva (01:03–01:57)**, sobre una copia limpia del árbol final: `verificar_paquete.sh completa` PASA en 22 min. Los 18 controles dan los resultados del LEEME (la 4.12, 63 de 63) y sus salidas son las de referencia de `resultados/controles_historicos_en_arbol_4_12/`. Después de todo, el manifiesto queda sin cambios: 0 archivos modificados, 0 ausentes y 0 de más.
- **Reinicio del contenedor.** Interrumpió los controles de la ronda definitiva en el 13.º. Se repitieron los 18 sobre la misma copia, que seguía intacta frente al manifiesto; los doce que ya habían terminado dieron la misma salida.
- **Descompresión del ZIP final:** la misma verificación y los mismos controles están en el registro externo de verificación, fuera del ZIP.

