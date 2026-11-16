#!/bin/bash
# h7 · octava comprobación · el mínimo 61→62 de verificar_paquete.sh. NO ejecuta verificar_paquete.sh: «bash -n» solo analiza la sintaxis, y
# la condición del bloque de la entrada efectiva (copiada tal cual de las líneas 169-171 del árbol) se aplica a salidas ya obtenidas.
F="$(cd "$(dirname "$0")/.." && pwd)"; S="$(cd "$F/../.." && pwd)"; R8="$(cd "$F/.." && pwd)/munger_v2_r1"
bash -n "$R8/verificar_paquete.sh" && echo "bash -n verificar_paquete.sh: sintaxis correcta (solo se analiza; no se ejecuta)"
grep -n -E "ge 6[12]|menos de 6[12]|al menos 6[12]" "$R8/verificar_paquete.sh" | cut -c1-170
cond() { SALIDA_X="$1"; rc="$2"
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de la entrada efectiva \(4\.15\) PASAN$' "$SALIDA_X" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 62 ]; then echo "PASA ($linea)"; else echo "FALLA (rc=$rc; «$linea»)"; fi; }
echo "condición con la salida de la candidata (62/62, rc 0): $(cond "$F/salidas8/bateria_ee415.log" 0)"
echo "condición con la salida de la mutación m0 (61/62, rc 1): $(cond "$F/mut8/m0_sin_el_cambio/bateria.log" 1)"
echo "condición con una salida de 61/61 y rc 0 (la batería de 45ff57c, ejecutada por la séptima: sin la prueba de X5): $(cond "$S/rev7/fable/salidas/bateria_ee415.log" 0)"
