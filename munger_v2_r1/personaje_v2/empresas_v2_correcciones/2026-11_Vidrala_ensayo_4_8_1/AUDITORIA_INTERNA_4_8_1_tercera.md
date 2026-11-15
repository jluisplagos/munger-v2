# Tercera revisión de la 4.8.1: correcciones de V-1 a V-10 (contexto separado)

**Qué es este documento:**
- es el informe final de un agente de Claude (Opus) con contexto separado, que revisó las correcciones posteriores al control de vigencia;
- **fecha:** 10-nov-2026, de 21:05 a 21:15 CET. El revisor dejó constancia de su avance en un archivo de progreso, que se vigiló durante la ejecución;
- **material:** `MATERIAL_VIGENCIA2_4_8_1.txt`, con SHA-256 `99c98435…7263745` y 20 archivos;
- **transcripción:** condensada pero fiel. Se conservan los veredictos, los hechos y las propuestas;
- es salida de un modelo, no una comprobación externa.

Las correcciones de W-1 a W-5 están en `REGISTRO_ENTREGA_4.8.1.md` §7b.

## Material, ejecución y reglas

**Hecho:**
- las 20 huellas coinciden al empezar y al terminar;
- la huella de H2 es `9edf6252…5422`;
- la lista de huellas de los 2.539 archivos del árbol es la misma antes y después, sin `__pycache__`;
- no se ejecutó nada que use LibreOffice.

**Ejecutado:**

| Qué | Resultado |
|---|---|
| `test_auditorias_v2.py` | 50/50 |
| `reproducir_rt1.py` | Código 0; los tres modos piden auditoría nueva |
| `analisis_reinversion_4_8_1.py --salida` | Código 0, 8 controles; 5 salidas idénticas byte a byte |
| Sondas propias | Sobre copias del expediente 4.6.1 |

**Siguen funcionando:**
- una respuesta legítima nueva cierra (código 0, fila APROBADO), y una segunda distinta tras `--desde 13` también;
- la corrección por material distinto: una solicitud nueva y, después, el cierre;
- con archivos binarios de 60 MB o textos de casi 2 MB en el expediente no hay error, y el cierre legítimo tarda unos 1,3 s.

## Veredicto de V-1 a V-10

| Hallazgo | Veredicto | Hecho que lo prueba |
|---|---|---|
| V-1 | **Resuelto** | K2e, K2f y K2g dan código 10, «repite el contenido», sin cierre. M18 y M19 se detectan. Hay un caso cercano: W-1 |
| V-2 | **Resuelto**, en los casos señalados | K1b, K1c, K1d y `.antiguo/a.md` dan código 10. Residuo: W-2 |
| V-3, V-4, V-5 y V-7 | **Resueltos** | V-5: tabla de ROIC efectivo con su definición (reinversión total para crecer), distinta de la del control de vigencia (solo la inversión fija) |
| V-6 | **En parte** | La cifra 1,1442 está en la transcripción, pero el árbol no conserva el informe original del auditor para comprobarla |
| V-8 | **En parte** | Quedan restos (W-5c) |
| V-9 | **Resuelto**, con un residuo | `{ilegible`, `[]` y el archivo vacío dan código 6. `{"sha256": 5}` da TypeError y código 1 (W-3) |
| V-10 | **Resuelto como documentación** | No se ha abierto ninguna pregunta en el JSON de decisiones |

## Hallazgos nuevos

### W-1 · importante · Volver a cortar las líneas sigue acreditando una aprobación

**Hecho:**
- La auditoría antigua, con las líneas cortadas de nuevo a 170 columnas y la línea de la solicitud añadida, sigue en APROBADO según H2.
- El pipeline cierra: código 0, concluido/APROBADO.
- **Causa:** la huella trabaja línea a línea.

**Propuesta:** una huella con el multiconjunto de palabras de todo el texto, sus pruebas y una mutación; o declararlo como límite.

### W-2 · menor · Auditorías históricas en cp1252, en UTF-16 o con más de 2 MB de relleno

**Hecho.** No se anotan y, copiadas en UTF-8, cierran. El Anexo D declara «UTF-8 y menos de 2 MB», pero otros documentos dicen «todo archivo de texto».

**Propuesta:** detectar el BOM, probar cp1252, descartar solo los binarios; o declarar el límite en todos los documentos.

### W-3 · menor · Una respuesta que no es UTF-8 válido

**Hecho:**
- con un byte `0xF3`, el paso 13 la consume, porque lee con `errors="replace"`;
- el paso 14 la lee en modo estricto y da UnicodeDecodeError, código 1 y traza en cada ejecución;
- al volver a guardarla en UTF-8, ya cuenta como usada;
- además, `{"sha256": 5}` en el registro da código 1.

**Propuesta:** rechazarla sin consumirla, validar los tipos del registro y añadir pruebas.

### W-4 · menor · Salidas desfasadas y referencias pendientes

**Hecho:**
- `resultados/test_auditorias_v2_salida.txt` da 43/43;
- la reproducción con el código 4.8 corresponde a la versión de 25 pruebas;
- el control de la 4.8.1 fallaría hasta que se regeneren;
- falta el §7b citado en el registro, y el §10 sigue vacío.

### W-5 · menor · Restos de documentación

- **a.** «Corregidos» los ocho menores del control de vigencia, cuando V-10 solo se documentó y V-6 se repuso sin una fuente comprobable.
- **b.** «Conjunto de líneas», cuando el código usa un multiconjunto.
- **c.** «Ninguna puede responder» en la nota del registro, en `cierre_v2.py` l. 71 y en `pipeline.py` l. 278–279.
- **d.** CONTINUIDAD y DECISIONES resumen el límite con solo dos casos.
- **e.** M20 no cubre la subcarpeta: hace falta una mutación que mire solo la carpeta y `historial_cierres/`.

## Límites

- Las sondas son ejemplos, no una búsqueda exhaustiva.
- No se ejecutó nada que use LibreOffice, ni `comprobar_entrega_4_8_1.py`.
- V-6 no se puede comprobar sin el informe original del auditor.
