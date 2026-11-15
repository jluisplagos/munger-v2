# Vidrala · los dos protocolos del objetivo sobre el mismo material económico

Mismo material económico: celdas_de_la_configuracion sí, precio_json sí, entradas_de_las_variantes sí.
Aprobaciones distintas: solicitud sí, auditoria sí, la_copia_retiro_la_aprobacion_heredada sí.

| Campo | objetivo_condicionado | bloqueo_del_objetivo |
|---|---|---|
| protocolo_declarado | objetivo_condicionado | bloqueo_del_objetivo |
| estado | concluido | pendiente_de_datos |
| auditoria | APROBADO | APROBADO |
| cubo | Vigilar | Vigilar |
| accion | esperar | None |
| precio_objetivo_decision | 56.02 | None |
| tratamiento | objetivo_condicionado | objetivo_bloqueado |
| estado_del_objetivo | emitido_condicionado | bloqueado |
| origen_del_bloqueo | None | protocolo_de_bloqueo |
| valor_calculado_condicional | 56.01809018887024 | 56.01809018887024 |
| precio_objetivo_emitido | 56.02 | None |
| provisional | True | False |
| hipotesis_que_lo_condicionan | ['PM1.estructura', 'PM1.familia', 'PM1.parametro'] | ['PM1.estructura', 'PM1.familia', 'PM1.parametro'] |
| rango_precio_si | [51.28701235794364, 65.71813435862349] | [51.28701235794364, 65.71813435862349] |
| solicitud | SA-2dfc317a5da12a95 | SA-b485abe6363fd044 |
| historial_cierres | ['01_47e1c83dc70a3d86', '02_5025f54d0c143062', '03_sin_material'] | ['01_47e1c83dc70a3d86', '02_f7a0ba07431707e3', '03_sin_material'] |

Fila del resumen V6.4 (columnas del objetivo):

- objetivo_condicionado: accion = esperar · protocolo_objetivo = objetivo_condicionado · estado_del_objetivo = emitido_condicionado · valor_calculado_condicional = 56.01809018887024 · precio_objetivo_emitido = 56.02 · objetivo_provisional = True
- bloqueo_del_objetivo: accion =  · protocolo_objetivo = bloqueo_del_objetivo · estado_del_objetivo = bloqueado · valor_calculado_condicional = 56.01809018887024 · precio_objetivo_emitido =  · objetivo_provisional = False
