#!/bin/bash
# Séptima comprobación · las tres baterías permitidas sobre los árboles con las propuestas del revisor (NO es código entregado):
#  fix7t (pruebas propuestas + código de la candidata): la batería 4.15 tiene que FALLAR en «(V3, V7)» (demostración de X1 dentro de la batería);
#  fix7  (pruebas propuestas + corrección de un carácter en :542): las tres tienen que pasar enteras.
F="$(cd "$(dirname "$0")/.." && pwd)"
"$F/run_bateria.sh" "$F/fix7t/munger_v2_r1" test_verificacion_entradas_415.py "$F/salidas/propuestas7/fix7t_bateria_415.log"; echo "fix7t 415 rc=$?"
"$F/run_bateria.sh" "$F/fix7/munger_v2_r1" test_verificacion_entradas_415.py "$F/salidas/propuestas7/fix7_bateria_415.log"; echo "fix7 415 rc=$?"
"$F/run_bateria.sh" "$F/fix7/munger_v2_r1" test_entrada_efectiva_415.py "$F/salidas/propuestas7/fix7_bateria_ee415.log"; echo "fix7 ee415 rc=$?"
"$F/run_bateria.sh" "$F/fix7/munger_v2_r1" test_verificacion_entradas_414.py "$F/salidas/propuestas7/fix7_bateria_414.log"; echo "fix7 414 rc=$?"
date -u +"%T fin"
