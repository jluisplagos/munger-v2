# INVÁLIDO (14-nov-2026, ≈15:00) · no usar

El CAMBIO de la orquestación (`configuracion/cambio_decisiones_vidrala_4_14.json`, primera versión) declaró en `analisis` solo C46–C48. `cambiar_base.py` reconstruye `fase1_v63.json` y aplica solo las entradas declaradas, así que se perdieron las entradas que la rama traía de los cambios de base anteriores:
- C24, C31, C34, C42, C53 y C54 (reexpresadas);
- C49 (4,5), que pasó a 6,764 sin decisión.

Lo detectó el agente de la fase A de este expediente. Se rehace en `../vidrala_decisiones` con todas las entradas de la rama y solo C46–C48 cambiadas. Esta carpeta se conserva como evidencia del incidente; su fase A no vale.
