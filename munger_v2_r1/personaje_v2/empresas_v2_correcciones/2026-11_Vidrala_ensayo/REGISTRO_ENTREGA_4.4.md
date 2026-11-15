# Registro de ejecución y cambios · entrega 4.4 (9-nov-2026)

## Encargo
«Munger v2 · aplicación controlada del piloto Vidrala y reejecución del personaje». Pide un expediente nuevo de ensayo, con la ruta A y el motor B como hipótesis principal:
- P1;
- P8;
- la resolución del dividendo;
- el registro de hipótesis;
- las fases A, B y C;
- el contraste con el motor A y T3.

Prohíbe:
- escribir registros humanos;
- confirmar ceros;
- valoraciones comparables con el precio y decisiones de cartera.

## Ejecución
1. **Punto de partida.** SHA-256 de la 4.3.1 (`40978a91…7a00b3`): coincide. Copia de trabajo descomprimida en limpio.
2. **Fuentes del encargo.** Comunicación del dividendo (2275) y comunicación de la CNMV de la liberada: descargadas en el navegador integrado, con la huella comprobada y conservadas.
3. **Resolución del dividendo**, antes de cualquier cambio de datos: `RESOLUCION_DIVIDENDO_Y_ACCIONES.md`.
4. **Diagnóstico del procedimiento.**
   - **Prueba en seco** sobre una copia del original: `construir` no podía ejecutarse. Faltaban los textos de 2016–2022 y la regla R-c rechazaba 39 ceros heredados sin cita.
   - **P1** es una cifra incorrecta (tipo B) y exige un registro humano en `fase1_decisiones.json`.
5. **Trabajo que no depende de ese registro:**
   - **Textos:** cuentas consolidadas de 2016–2022 descargadas (7 PDF, con huella); diez textos generados con `pdf_a_texto.py`; las 535 citas de los AR originales pasan, salvo las 2 de P8.
   - **AR nuevos:** versiones con P8 (tipo A) y con la cita literal de los 39 ceros (re-extracción de esa partida y año; los ceros quedan pendientes).
   - **Expediente** en `empresas_v2_correcciones/2026-11_Vidrala_ensayo/Vidrala/`; pasos 0–1 del pipeline (libro base idéntico al original).
   - **Copias temporales:** `construir` reproduce la Historia original. Con una decisión simulada de P1, solo cambia K14. Los pasos 0–4 del pipeline sobre esa simulación dan 0 bloqueantes y el motor B calculable.
6. **Documentos:**
   - informe del ensayo;
   - registro de hipótesis;
   - propuesta exacta del registro P1;
   - fuentes y procedencia;
   - script de 72 comprobaciones y sus salidas.
7. **Detención** antes de `construir` en el expediente de ensayo, por el registro humano de P1 (bloqueo B1).

## Qué no se ha ejecutado, y por qué
**No ejecutado:** `construir` con P1, el recálculo, las fases A, B y C, la auditoría y el contraste entre motores.
**Motivo:** todo ello depende del registro de P1. No se han escrito registros, firmas ni fechas humanas, y P1 no se ha aplicado por ninguna otra vía.

## Modelos
- **Opus** en todo el procedimiento, incluidas las re-extracciones de ceros. El prompt del sistema prevé Sonnet para ellas: diferencia declarada.
- **Fable no se usó.**
- **Sin subagentes.**

## Cambios del paquete respecto a la 4.3.1
- **Nuevo:** `personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo/`, con:
  - el expediente;
  - las fuentes;
  - los documentos;
  - el script y las salidas.
- **Modificados:** `VERSION`, `CONTINUIDAD.md` y `PROMPT_NUEVA_VENTANA.md`.
- **Se regeneran:** `CAMBIOS_ARCHIVOS.txt` y `MANIFIESTO_SHA256.txt`.
- **Sin cambios:**
  - `personaje_v2/empresas_v2/` (originales);
  - el código;
  - `v6/`;
  - los contrastes anteriores y sus baterías de 43, 217, 45 y 35;
  - `verificar_paquete.sh`.
- **Limpieza:** se borraron las cachés que el pipeline crea al ejecutarse (`__pycache__` y el perfil de LibreOffice `personaje_v2/.lo_perfil/`). No forman parte del paquete.

## Verificación del paquete 4.4
Hecha sobre una descompresión limpia del ZIP candidato, con el mismo contenido que el final salvo este apartado. El ZIP final se volvió a verificar igual; su huella está en el `.sha256` y en `PARTES.txt` de la entrega, no aquí, porque cambiaría el propio paquete.

**`bash verificar_paquete.sh completa`:** código 0 y «RESULTADO GLOBAL: PASA».
- manifiesto: 938 archivos, 0 modificados, 0 ausentes y 0 de más;
- entorno: pasa;
- piloto: 35 comprobaciones, salida idéntica;
- 114/114 y 30/30, con los mismos nombres que la línea de base.

**Aparte** (código 0 y salida idéntica a la de referencia en las cuatro):
- 45 comprobaciones de la 4.2;
- 217 de la 4.3;
- 43 de la 4.3.1;
- 72 del ensayo 4.4.

**Después de las baterías:**
- los 938 archivos del manifiesto siguen intactos, incluidos los originales de `empresas_v2/Vidrala/` y el expediente de ensayo;
- los únicos archivos añadidos son salidas de las pruebas sintéticas (`personaje_v2/pruebas/sintetico/`, `resultados_reparacion/` y `resultado_comprobadores.json`) y el perfil de LibreOffice (`personaje_v2/.lo_perfil/`). No forman parte del paquete.
