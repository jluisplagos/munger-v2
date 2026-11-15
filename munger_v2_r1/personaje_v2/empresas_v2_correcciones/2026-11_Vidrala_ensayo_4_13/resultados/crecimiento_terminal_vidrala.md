# Vidrala · ¿crea valor el crecimiento terminal en el motor B? (encargo 4.13 §8)

**Qué es.** Recálculos con LibreOffice sobre copias de `empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_12/cierre_condicionado/Vidrala/Vidrala_v63_evaluada.xlsx` (4.12; el expediente no cambia). r personal 9 %; el motor B descuenta a r_op = 8,689151674 % (Diagnóstico V6 C15, calculada con las entradas). g perpetuo de la fase B: 1 % / 2 % / 2,5 %. ROIC terminal de la fase B: 9 % / 9 % / 12 %.

| Caso | V MALO | V NORMAL | V BUENO | Ponderado | Precio de Sí | Zona | r_op |
|---|---|---|---|---|---|---|---|
| activa | 44,32 | 60,21 | 78,52 | 60,70 | 56,02 | caro | 8,689152 % |
| activa_g0 | 43,71 | 59,34 | 72,00 | 58,74 | 54,45 | caro | 8,689152 % |
| SR2 | 44,73 | 61,65 | 80,41 | 62,02 | 57,08 | caro | 8,689152 % |
| SR2_g0 | 43,71 | 59,34 | 72,00 | 58,74 | 54,45 | caro | 8,689152 % |
| heredado | 54,03 | 67,94 | 87,36 | 69,04 | 64,75 | caro | 8,698969 % |
| heredado_g0 | 53,66 | 65,93 | 78,89 | 66,07 | 62,52 | caro | 8,698969 % |

**Valor que aporta el crecimiento perpetuo** (caso − el mismo con g = 0; € por acción):

| Configuración | Δ V MALO | Δ V NORMAL | Δ V BUENO | Δ ponderado | Δ precio de Sí |
|---|---|---|---|---|---|
| activa | +0,61 | +0,88 | +6,52 | +1,95 | +1,57 |
| SR2 | +1,02 | +2,31 | +8,41 | +3,27 | +2,63 |
| heredado | +0,37 | +2,01 | +8,47 | +2,97 | +2,23 |

**Lectura (interpretación).** Un ROIC terminal igual a la r personal no hace neutral el crecimiento en el motor B: la perpetuidad se descuenta a r_op, y con P-M1 el terminal carga además un requisito que crece con las ventas. El signo y el tamaño del efecto son los de la tabla, por escenario; no se deducen de la igualdad 9 % = 9 % ni de la conclusión contraria («P-M1 introduce inversión adicional, luego el crecimiento destruye valor»). La r personal sigue en el 9 % y r_op se sigue calculando con las entradas; nada de esto cambia ninguna palanca.
