# Mensaje de arranque para una ventana nueva (4.15 · hito 2)

Desde la 4.15 el proyecto se conserva en el repositorio `jluisplagos/munger-v2`, no en un ZIP adjunto. El mensaje de la 4.14 (con el ZIP) está
en `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/reproduccion/codigo_4_14/PROMPT_NUEVA_VENTANA.md.txt`.
Se pega como primer mensaje todo el texto que va debajo de la línea.

---

# Continuación del proyecto Munger v2 · verificación inicial

La fuente de verdad es el repositorio y sus pruebas, no la memoria de conversaciones anteriores. La sesión anterior no está disponible.

## Primera tarea: comprobar el estado. No debe iniciarse ningún otro trabajo.
1. Leer `README.md` y `CLAUDE.md` del repositorio, y `munger_v2_r1/CONTINUIDAD.md`.
2. Desde `main`, descargar el ZIP original de la Release `base-4.14` (si `gh release download` no funciona, por la API REST:
   `gh api -H "Accept: application/octet-stream" repos/jluisplagos/munger-v2/releases/assets/750814858 > <zip>`), comprobar su SHA-256
   (`bb51942c…7b93e`), materializarlo con `python3 -I tools/base_414.py materialize --source <zip>` y verificarlo con `verify`
   (esperado 6798/6798, `complete: true`). No modificar `main` ni el ZIP.
3. Cambiar a la rama de la entrega que se quiera comprobar (la del hito 2 es `claude/hopeful-bardeen-qap6y0`), comprobar
   `munger_v2_r1/MANIFIESTO_SHA256.txt` y leer `munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_15/hito2/HITO_2_4_15.md`
   y `PUNTO_DE_RECUPERACION.md`.
4. Sobre una copia limpia de `munger_v2_r1/` (sin `personaje_v2/.lo_perfil/` ni `__pycache__`), ejecutar `bash verificar_paquete.sh completa`.
   LibreOffice y las pruebas que lo usan van en secuencia, nunca dos a la vez. Esperado (hito 2): manifiesto, entorno y piloto (35 CUMPLEN);
   comprobadores 114/114; sintética 30/30 con los nombres de la línea de base; H5 59/59; juicio 27/27; entradas 4.14 33/33; entradas 4.15
   173/173; entrada efectiva 60/60; relevo caducado 5/5; integración V6.4 199/199; trazabilidad 78/78; integridad 103/103; auditorías 55/55;
   estados 28/28; resumen 45/45; cierre 55/55; RESULTADO GLOBAL: PASA.
5. Informar de forma breve del resultado de cada bloque y de cualquier discrepancia entre la documentación y lo que dicen los archivos o las
   pruebas. Si algo falla, se informa con precisión y no se corrige sin indicación.
6. Esperar la siguiente indicación de la persona responsable del proyecto.

## Reglas vigentes
- Comunicación en español claro, en tercera persona respecto de la persona responsable; distinguir hechos, interpretaciones y propuestas.
- Opus (esfuerzo alto) para coordinación e implementación; Fable (esfuerzo máximo) de forma selectiva para problemas difíciles y revisión
  crítica, con aviso y registro. La revisión la hace un agente distinto del autor del cambio, y se revisa específicamente lo afectado por
  cada corrección.
- La verificación de las entradas es condición necesaria, no suficiente: ninguna salida es apta para dinero real por superar controles de
  software. No se declara cerrado ningún requisito pendiente.
- No se modifican originales, fuentes ni huellas para legitimar un resultado; no se reactivan aprobaciones retiradas; no se aceptan
  auditorías de material distinto; no se inventan firmas ni política económica. No se cambian criterios financieros ni fórmulas económicas
  sin contrastar antes su especificación y sus fuentes (F1 se concilia en una tarea propia).
- Se trabaja en ramas y expedientes nuevos, con commits y puntos de recuperación (estado de las pruebas, pendientes y siguiente paso) al
  completar cada bloque. No se publican credenciales ni archivos temporales.
- Una entrega posterior de otra sesión no se incorpora automáticamente: se conserva y se importa como versión nueva siguiendo
  `docs/RECEPCION_ENTREGA_CLAUDE.md`.
