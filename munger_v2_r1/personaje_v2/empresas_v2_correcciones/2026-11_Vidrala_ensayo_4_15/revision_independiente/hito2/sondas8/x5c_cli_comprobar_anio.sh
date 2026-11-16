#!/bin/bash
# x5c · octava comprobación · la orden «fase1_historia.py comprobar-anio» (no usa LibreOffice) sobre COPIAS de expedientes reales
# (solo texto/ y fase1_partes/), con el código anterior (45ff57c, árbol prev/) y con el nuevo (0a0020b, árbol copia/): misma salida y mismo código.
F="$(cd "$(dirname "$0")/.." && pwd)"
E14="$(dirname "$F")/munger_v2_r1/personaje_v2/empresas_v2_correcciones/2026-11_Vidrala_ensayo_4_14"
export PATH="$F/bin:$PATH" PYTHONDONTWRITEBYTECODE=1 TMPDIR="$F/tmp"
D="$F/tmp/reales_copia"; rm -rf "$D"; mkdir -p "$D"
tot=0; dif=0; okn=0
for e in elis_decisiones/Elis viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala; do
  n="$(basename "$e")"; mkdir -p "$D/$n"
  cp -r "$E14/$e/texto" "$E14/$e/fase1_partes" "$D/$n/"
  for f in "$D/$n"/fase1_partes/AR_*.json; do
    a="$(basename "$f" .json)"; a="${a#AR_}"
    case "$a" in *[!0-9]*) continue;; esac
    o="$(python3 -I -B "$F/prev/munger_v2_r1/personaje_v2/scripts/fase1_historia.py" comprobar-anio "$D/$n" "$a" 2>&1)"; ro=$?
    m="$(python3 -I -B "$F/copia/munger_v2_r1/personaje_v2/scripts/fase1_historia.py" comprobar-anio "$D/$n" "$a" 2>&1)"; rn=$?
    tot=$((tot+1)); [ "$rn" -eq 0 ] && okn=$((okn+1))
    if [ "$o" != "$m" ] || [ "$ro" -ne "$rn" ]; then dif=$((dif+1)); echo "DIFIERE $n $a: anterior($ro) «${o:0:200}» · nuevo($rn) «${m:0:200}»"; fi
    echo "$n $a: código anterior=$ro nuevo=$rn · $(echo "$m" | head -1 | cut -c1-110)$( [ "$(echo "$m" | wc -l)" -gt 1 ] && echo " … ($(echo "$m" | wc -l) líneas)")"
  done
done
echo "años comprobados con la orden: $tot · con código 0 (nuevo): $okn · diferencias entre el código anterior y el nuevo: $dif"
# las copias no cambian al comprobarlas (la orden solo lee)
for e in elis_decisiones/Elis viscofan_decisiones/Viscofan vidrala_decisiones/Vidrala; do
  n="$(basename "$e")"
  diff -rq "$E14/$e/fase1_partes" "$D/$n/fase1_partes" > /dev/null && diff -rq "$E14/$e/texto" "$D/$n/texto" > /dev/null && echo "copia de $n: idéntica al original después de comprobar" || echo "copia de $n: CAMBIÓ"
done
[ "$dif" -eq 0 ] && echo "RESULTADO: CONFORME" || { echo "RESULTADO: NO CONFORME"; exit 1; }
