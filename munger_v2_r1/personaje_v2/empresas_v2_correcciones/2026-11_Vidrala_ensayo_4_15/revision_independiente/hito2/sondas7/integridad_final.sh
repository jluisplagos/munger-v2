#!/bin/bash
# Séptima comprobación · integridad al terminar: el árbol congelado no ha cambiado (huellas, fechas, manifiesto), la copia ligera es el código
# congelado, no hay __pycache__, no hubo intentos de soffice y /home/user/munger-v2 sigue limpio. Solo lee (salvo sus propias salidas en fable/).
F="$(cd "$(dirname "$0")/.." && pwd)"
C="$(cd "$F/.." && pwd)/munger_v2_r1"
OUT="$F/salidas/integridad_final.txt"
ok=1
( cd "$C" && find . -type f -print0 | sort -z | xargs -0 sha256sum ) > "$F/huellas_arbol_congelado_fin.txt"
h() { x=$(sha256sum "$1" | cut -c1-64); echo "${x:0:8}…${x:56:8}"; }
{
  echo "inicio: 16-nov-2026, $(sed 's/^[0-9-]* //; s/:[0-9]* UTC/ UTC/' "$F/inicio.txt")"
  echo "fin: $(date -u +'%H:%M') UTC"
  if cmp -s "$F/huellas_arbol_congelado_inicio.txt" "$F/huellas_arbol_congelado_fin.txt"; then echo "huellas del árbol congelado: idénticas al inicio ($(wc -l < "$F/huellas_arbol_congelado_fin.txt") archivos; SHA-256 de los listados: $(h "$F/huellas_arbol_congelado_fin.txt"))"; else echo "HUELLAS DISTINTAS"; ok=0; fi
  n=$(find "$C" -newer "$F/inicio.txt" | wc -l); echo "archivos o carpetas del árbol congelado posteriores al inicio: $n"; [ "$n" = 0 ] || ok=0
  m=$( cd "$C" && sha256sum -c MANIFIESTO_SHA256.txt 2>/dev/null | grep -c ': OK$' ); echo "manifiesto al terminar: $m OK"; [ "$m" = 7559 ] || ok=0
  for d in scripts pruebas esquema; do x=$(diff -rq "$C/personaje_v2/$d" "$F/copia/munger_v2_r1/personaje_v2/$d" | wc -l); echo "diff -rq $d (congelado frente a copia): $x diferencias"; [ "$x" = 0 ] || ok=0; done
  p=$(find "$C" "$F/copia" "$F/prev" "$F/prop6" "$F/prop6t" "$F/fix7" "$F/fix7t" "$F/sondas" "$F/sondas3" "$F/sondas4" "$F/sondas7" -name __pycache__ | wc -l); echo "__pycache__ en el árbol congelado, en las copias o en las sondas: $p"; [ "$p" = 0 ] || ok=0
  if [ -e "$F/salidas/INTENTOS_SOFFICE.log" ]; then echo "HAY INTENTOS DE SOFFICE"; ok=0; else echo "INTENTOS_SOFFICE.log: no existe"; fi
  echo "huellas de verificacion_entradas.py: copia (45ff57c) $(h "$F/copia/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py") · prev (8196522) $(h "$F/prev/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py") · c876 (876bfc2) $(h "$F/c876/scripts/verificacion_entradas.py") · prop6 $(h "$F/prop6/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py") · prop6t $(h "$F/prop6t/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py") · fix7 $(h "$F/fix7/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py") · fix7t $(h "$F/fix7t/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py")"
  echo "huellas de las pruebas: test_verificacion_entradas_415.py copia $(h "$F/copia/munger_v2_r1/personaje_v2/pruebas/test_verificacion_entradas_415.py") · fix7 y fix7t $(h "$F/fix7/munger_v2_r1/personaje_v2/pruebas/test_verificacion_entradas_415.py") · test_entrada_efectiva_415.py copia $(h "$F/copia/munger_v2_r1/personaje_v2/pruebas/test_entrada_efectiva_415.py")"
  echo "SHA-256 completo de verificacion_entradas.py con el carácter repuesto (fix7): $(sha256sum "$F/fix7/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py" | cut -c1-64)"
  echo "diff de fix7 frente a la copia en verificacion_entradas.py: $(diff "$F/copia/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py" "$F/fix7/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py" | grep -c '^[<>]') líneas (una quitada y una puesta = 2)"
  st=$(git -C /home/user/munger-v2 status --short | wc -l); cab=$(git -C /home/user/munger-v2 rev-parse --short HEAD); ult=$(git -C /home/user/munger-v2 log -1 --format=%s)
  if [ "$st" = 0 ]; then echo "git: al terminar, git status está limpio y la rama está en $cab («$ult»)."; else echo "git: al terminar, git status tiene $st líneas (cambios de otra sesión, no del revisor) y la rama está en $cab («$ult»)."; fi
  [ "$(h "$F/copia/munger_v2_r1/personaje_v2/scripts/verificacion_entradas.py")" = "7abbb081…9227c41b" ] || ok=0
  [ "$ok" = 1 ] && echo "INTEGRIDAD CONFORME" || echo "INTEGRIDAD NO CONFORME"
} > "$OUT"
cat "$OUT"
