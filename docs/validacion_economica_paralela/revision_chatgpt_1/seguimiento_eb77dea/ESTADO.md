# Seguimiento del autor en eb77dea

Commit contrastado: eb77dea9ce36994faaf3af1aa86ae166649e1260. Revisor independiente permanece en47551a2; su segunda pasada figura pendiente en el estado del autor. Rama técnica sin nuevos commits respecto a56fca94 en la consulta efectuada. No se infiere el estado de procesos sin publicar.

## Mejoras ejecutadas y repetidas aquí

El autor respondióO1–O17 y actualizó informe/especificación/scripts. Repetí los16 casos de test_verificar_cifras.py:16/16. Repetí prueba_mutantes.py del revisor sobre la versión nueva: el literal de2024 declarado2025 ahora se rechaza; el año2031 del mutante compuestoM4 se rechaza; fuente sinsha256 se rechaza con informe y sinKeyError; huella vacía se rechaza.

Los resultados guardados del autor declaran707/707 filas y186 comprobaciones, clasificadas en115 contra libro,58 contra fuentes y13 algebraicas. Aquí no se han repetido las186 comprobaciones completas ni emitido aceptación económica final.

## Cobertura que aún requiere examen en la segunda pasada

M4 combina año, unidad y perímetro erróneos: rechazarlo por el año no demuestra que los otros dos campos se comprueben. Ejecuté dos mutaciones SEPARADAS, con todos los años correctos:

- CREC_ORG_2025, unidad «%»→«mm EUR»: código0,707/707,0fallos.
- IS_VENTAS_2025, perímetro «consolidado IFRS, grupo Elis»→«segmento Francia»: código0,707/707,0fallos.

Esto confirma que esos metadatos alterados no provocan fallo en verificar_cifras.py. No se afirma que las cifras reales sean incorrectas ni que la mutación cambie el cálculo, que usa las magnitudes originales. Corresponde comprobar si existe una vía independiente, trazable y vigente que acredite unidad y perímetro, o dejar esa cobertura expresamente pendiente. No dar por cerrado todoO3 solo porque se rechace el mutante compuesto.

La corrección del año es real y está comprobada. El cierre de las objeciones y de la suficiencia de la evidencia requiere la segunda revisión sobreeb77dea o elcommit posterior que se fije. F1 continúa abierto y no se autoriza una implementación ni una valoración con dinero real por estos resultados.
