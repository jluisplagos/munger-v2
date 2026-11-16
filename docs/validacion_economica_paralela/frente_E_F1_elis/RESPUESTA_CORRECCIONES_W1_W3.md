# Correcciones W1–W3 de la revisión F1 v3 · propuesta F1 · Elis

Fecha: 16-nov-2026. Autor: frente E (sesión «Conciliación económica Elis/F1», que actúa además como coordinadora del programa de cierre).

- **Revisión que se corrige:** `revision_externa/f1_v3_20261116/REVISION_F1_V3.md` y `CORRECCION_PARA_CLAUDE.md`, en el repositorio auxiliar `jluisplagos/munger-v2-evidencias-mistral`, rama `revision/chatgpt-f1-v3-20261116`, commit `f5775dc07a61b829df2b0e7a4a97c556869ae0f4`. Revisó `716cbd6`.
- **Base:** `716cbd6794b7fcde8b3862c9d1e7acdaf516d262`, igual al remoto y sin trabajo posterior.
- **Esta corrección:** el commit que contiene este archivo.

**Qué hace y qué no.**
- Corrige solo W1–W3 y lo que depende de ellas, en la propuesta, la especificación y las herramientas de investigación. Lo conforme de V1–V11 se conserva.
- No adopta (1a)–(5b) y no implementa nada en el producto ni en los libros. No elige un horizonte para Elis, no pone ceros por defecto y no cambia el umbral C179 ni G8.
- Se conservan C48 = 108, C49 = 128,1, el FCF base 307,933 y E1/D3/E2/E6. Elis sigue en `pendiente_de_datos`.
- No encarga ninguna revisión: la solicitud de contraste se registra en el control común (`CONTROL.json`, tarea F1-W), con revisor asignado Mistral C/F.

## W1 · coste temporal que sigue después del año 10

**Corregido como propuesta, con su límite actual declarado.**
- La regla anterior restaba X₁₁ del flujo del año 11. Con un horizonte H > 10, ese coste entraba en Gordon y se volvía perpetuo.
- Propuesta (E3):
  - el año 11 y Gordon van sobre la base sostenible, sin X;
  - la caja temporal pendiente se descuenta aparte, VP_pend = Σ_{t=11..H} X_t/(1+r)^t;
  - valor = VP(años 1–10) + VP(Gordon sobre la base sostenible) − VP_pend.

  X₁₁ solo entra en Gordon si el término es permanente y proporcional a las ventas.
- **Límite:** la plantilla no tiene ese término. Hasta que se apruebe e implemente, H > 10 no está soportado y V-F1i bloquea la conclusión afectada.
- En la propuesta, la fila de la transición en la tabla de correspondencia del §2 dice ahora lo mismo.

**Prueba** (`controles_sinteticos_f1.py`, bloque `W1_coste_temporal_despues_del_año_10`). Importes ficticios: caja sostenible 68, coste de 7 hasta H inclusive y r = 10 %. El valor presente del escenario se calcula año a año, por separado del motor.

| g | H | VP con la regla anterior | VP de la caja | VP con la propuesta |
|---|---|---|---|---|
| 0 | 5 | 653,464493 | 653,464493 | = |
| 0 | 10 | 636,988030 | 636,988030 | = |
| 0 | 11 | **610,000000** | 634,534573 | = |
| 0 | 12 | **610,000000** | 632,304157 | = |
| 2 % | 5 | 815,464493 | 815,464493 | = |
| 2 % | 10 | 798,988030 | 798,988030 | = |
| 2 % | 11 | **765,252992** | 796,534573 | = |
| 2 % | 12 | **765,252992** | 794,304157 | = |

- Con g = 0, las cifras de la regla anterior y de la caja reproducen las de la sonda de la revisión.
- La regla anterior acierta con H ≤ 10 y falla con H = 11 y 12. La propuesta acierta en los ocho casos.
- Los 32 casos anteriores se conservan sin cambios.

## W2 · signo del salto del terminal y G8

**Corregido.**
- **Signo.** La fila 178 del libro es rentabilidad marginal − ROIC: positivo significa que la rentabilidad cae en el año 11.
  - `copia_investigacion_f1.py` calculaba ROIC − marginal con el rótulo de la fila 178. Ahora usa el signo del libro y contrasta el valor derivado con la fila 178 en los tres escenarios: tres controles nuevos, de 55 a 58.
  - Elis: +0,474 / +0,677 / +2,414 puntos. Con la igualdad exacta, +0,549 / +0,891 / +2,774.
- **Aviso.** Compara la magnitud: MAX(ABS(fila 178)) frente a C179 (`patch_v62_base.py`, AVISO_TRANSICION). En la frontera no avisa.
- **G8 vigente** (`comprobar_gramatica.py`): `abs(sv) > umbral + 1e-9` lleva `requiere_justificacion=True`. Es una obligación técnica que ya existe. La propuesta y la especificación la conservan:
  - V-F1k numérico es AVISO con justificación obligatoria por encima de C179, en las dos direcciones;
  - INFORMA en la frontera y por debajo.
  - La frase de la respuesta V1–V11 que «eliminaba “debe justificarse”» queda corregida con una nota.
  - Si se quisiera cambiar G8, sería una decisión aparte; no se propone.
- **Prueba** (bloque `W2_aviso_del_terminal`, 9 casos):
  - ±6 puntos: avisa;
  - frontera ±5: no avisa;
  - ±5,01: avisa;
  - Elis MALO y BUENO: no avisa;
  - comprobación textual de que la regla replicada está en el código del producto (`comprobar_gramatica.py` y `patch_v62_base.py`, iguales en `716cbd6` y en `957af65`). Es una lectura del código, no una ejecución del producto.

## W3 · dominio de A0 frente a su guarda

**Corregido** (especificación E2 y E5; propuesta (1a), §1 y tabla de severidad):

| D&A ROU | C49 | Estado |
|---|---|---|
| > 0 | > 0 | V-F1a: BLOQUEA. Coste de arrendamiento contado dos veces bajo las premisas de §5 del informe |
| 0 | 0 | A0 admisible: sin arrendamientos |
| > 0 | 0 | **V-F1m (nuevo): BLOQUEA.** Fuera del dominio de A0: entradas incompletas o en conflicto (calendario, definición o dato) que hay que aclarar. No se afirma doble cómputo |
| 0 | > 0 | V-F1m: igual |

- Que V-F1a no salte no admite A0.
- No se cambia AND por OR ni se inventa ningún umbral. El bloqueo vigente con los dos positivos se conserva.
- **Prueba:** bloque `W3_dominio_de_A0`, con los cuatro casos.

## Pruebas ejecutadas

Desde `scripts/`, con los mismos comandos que en la respuesta V1–V11, §1. Solo se ejecuta lo afectado.

| Script | Resultado |
|---|---|
| `controles_sinteticos_f1.py` | Código 0. 32 casos sin cambios, más W1 (8), W2 (9) y W3 (4), sin errores |
| `copia_investigacion_f1.py --raiz` | Código 0. 58 controles, 0 fallidos (55 anteriores y 3 de signo frente a la fila 178) |
| `contraste_f1.py` | No se ha vuelto a ejecutar: ni su código ni sus entradas cambian |
| Manifiesto | Regenerado; `sha256sum -c` OK |

## Pendiente

- **Contraste externo** de W1–W3 (Mistral C/F, según el control común).
- **Implementar el término de W1** (VP_pend) solo tras decisión, porque es una extensión del motor.
- **Lo demás no cambia:** datos M1, M2, M6 y N2; decisiones (1a)–(5b); C20; cifras [LECTURA] al CSV.
