#!/usr/bin/env bash
# Verificación del paquete Munger v2 (vigente desde la entrega 3.1; ampliada en cada entrega, la última la 4.14). Ejecutar desde la raíz munger_v2_r1/ de un ZIP recién descomprimido:
#   bash verificar_paquete.sh            manifiesto + entorno + contraste del piloto Vidrala 2025 + test_comprobadores.py (≈ 1–2 min)
#   bash verificar_paquete.sh completa   lo anterior + test_pipeline_sintetico.py y comparación de nombres + batería de cierre
#                                        test_cierre_v2.py (obligatoria: si falla, no se ejecuta o se interrumpe, el resultado global
#                                        es FALLA; exige al menos 55 pruebas, todas en PASA) y batería del resumen
#                                        test_resumen_v2.py (4.7; igual de obligatoria; al menos 45 pruebas) y batería de coherencia
#                                        de estados test_estados_v2.py (4.8; igual de obligatoria; al menos 28 pruebas) y batería de
#                                        solicitudes de auditoría test_auditorias_v2.py (4.8.1; igual de obligatoria; al menos 55 pruebas;
#                                        fija ella misma las fechas en tres modos, así que no depende de la zona horaria de la descompresión)
#                                        y batería de integridad de la auditoría vigente test_integridad_auditoria_v2.py (4.9, R-V1; igual
#                                        de obligatoria; al menos 103 pruebas; va antes de la de solicitudes) y batería de trazabilidad
#                                        test_trazabilidad_v2.py (4.10: BOM, marcadores de cierre y libro final; igual de obligatoria; al
#                                        menos 78 pruebas) y, la primera de las obligatorias, la batería de la integración V6.4 experimental
#                                        test_integracion_v64.py (4.11: plantilla, 117 casos con la réplica independiente, pipeline y cambio
#                                        de base; 4.12: grupos E vigencia y selección, F materialidad y protocolos del objetivo, G coherencia,
#                                        variantes y fórmulas alteradas; 4.13: guardas de estructura, salto del protocolo, cobertura y H
#                                        V6.4.1 experimental; 4.14: cambio de base con correcciones de extracción; igual de obligatoria; al menos 199 pruebas) y, antes de ella, la batería de
#                                        vigencia H5 test_vigencia_h5.py (4.13.1; al menos 59 pruebas) y la del juicio sobre el objetivo
#                                        test_juicio_objetivo_414.py (4.14; al menos 27 pruebas) y la de la verificación de las entradas test_verificacion_entradas_414.py
#                                        (4.14; al menos 33 pruebas), igual de obligatorias (≈ 30–45 min en total); (4.15) después, la de la
#                                        corrección de la verificación de las entradas test_verificacion_entradas_415.py (al menos 173 pruebas;
#                                        105 en el hito 1 de la 4.15) y la de la entrada efectiva del FCF base test_entrada_efectiva_415.py
#                                        (al menos 60; 40 en el hito 1) y la del relevo caducado test_relevo_i19_415.py (4.15, hito 2; al
#                                        menos 5; LibreOffice), igual de obligatorias
# El modo rápido no ejecuta la batería sintética ni la de cierre: su PASA solo cubre lo que lista arriba.
# Ninguno de los dos modos sustituye a los controles de los expedientes reales ni a sus auditorías.
# Código de salida: 0 si todo PASA; distinto de 0 si algún bloque falla. Las pruebas escriben en personaje_v2/pruebas/: el manifiesto
# se comprueba ANTES de ejecutarlas (para repetir la verificación completa, descomprimir de nuevo).
set -uo pipefail
cd "$(dirname "$0")"
export PYTHONDONTWRITEBYTECODE=1   # sin __pycache__ dentro del paquete
ENTORNO_LOG="$(mktemp)"
fallos=0
echo "== versión"
cat VERSION 2>/dev/null || { echo "FALTA VERSION"; fallos=$((fallos+1)); }

echo "== manifiesto (MANIFIESTO_SHA256.txt)"
python3 - <<'PY'
import hashlib, os, sys
esperado = {}
for l in open("MANIFIESTO_SHA256.txt", encoding="utf-8"):
    if l.strip() and not l.startswith("#"):
        h, p = l.rstrip("\n").split("  ", 1)
        esperado[p] = h
actual = {}
for r, ds, fs in os.walk("."):
    ds[:] = [d for d in ds if d != "__pycache__"]
    for f in fs:
        p = os.path.relpath(os.path.join(r, f), ".")
        if p != "MANIFIESTO_SHA256.txt":
            actual[p] = hashlib.sha256(open(p, "rb").read()).hexdigest()
mod = sorted(p for p in esperado if p in actual and actual[p] != esperado[p])
falt = sorted(p for p in esperado if p not in actual)
extra = sorted(p for p in actual if p not in esperado)
print(f"{len(esperado)} archivos en el manifiesto · modificados {len(mod)} · ausentes {len(falt)} · de más {len(extra)}")
for etiqueta, lista in (("MODIFICADO", mod), ("AUSENTE", falt), ("DE MÁS", extra)):
    for p in lista[:20]:
        print(f"  {etiqueta}: {p}")
print("RESULTADO manifiesto:", "PASA" if not (mod or falt or extra) else "FALLA (¿se ejecutaron ya pruebas en esta copia? descomprimir de nuevo)")
sys.exit(0 if not (mod or falt or extra) else 1)
PY
[ $? -eq 0 ] || fallos=$((fallos+1))

echo "== entorno (personaje_v2/scripts/comprobar_entorno.sh)"
( cd personaje_v2 && bash scripts/comprobar_entorno.sh ) > "$ENTORNO_LOG" 2>&1; rc=$?
grep -E "^(FALTA|AVISO|ERROR|FALLA)|autotest" "$ENTORNO_LOG" || true
echo "RESULTADO entorno: $([ $rc -eq 0 ] && echo PASA || echo "FALLA (ver $ENTORNO_LOG)")"
[ $rc -eq 0 ] || fallos=$((fallos+1))

echo "== contraste del piloto Vidrala 2025 (solo lectura; salida idéntica a la de referencia)"
SALIDA_PILOTO="$(mktemp)"
python3 -I contrastes/piloto_Vidrala_2025/scripts/contraste_vidrala_2025.py > "$SALIDA_PILOTO" 2>&1; rc=$?
if [ $rc -eq 0 ] && diff -q "$SALIDA_PILOTO" contrastes/piloto_Vidrala_2025/resultados/contraste_salida.txt > /dev/null; then
  echo "$(grep -c '\[CUMPLE\]' "$SALIDA_PILOTO") comprobaciones CUMPLEN · salida idéntica a resultados/contraste_salida.txt"
  echo "RESULTADO piloto: PASA"
else
  tail -5 "$SALIDA_PILOTO"; echo "RESULTADO piloto: FALLA (ver $SALIDA_PILOTO)"; fallos=$((fallos+1))
fi

echo "== pruebas de la reparación"
( cd personaje_v2 && bash pruebas/ejecutar_pruebas_reparacion.sh $([ "${1:-}" = "completa" ] || echo rapidas) ); rc=$?
[ $rc -eq 0 ] || fallos=$((fallos+1))

echo "== batería de vigencia H5 (personaje_v2/pruebas/test_vigencia_h5.py; obligatoria en «completa»; reparación 4.13.1)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_H5="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_vigencia_h5.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_vigencia_h5.py ) > "$SALIDA_H5" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_vigencia_h5.py" > "$SALIDA_H5"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de vigencia H5 \(4\.13\.1\) PASAN$' "$SALIDA_H5" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 59 ]; then
    echo "$linea"; echo "RESULTADO vigencia H5: PASA"
  else
    tail -5 "$SALIDA_H5"; echo "RESULTADO vigencia H5: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 59 pruebas; ver $SALIDA_H5)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería del juicio sobre el objetivo (personaje_v2/pruebas/test_juicio_objetivo_414.py; obligatoria en «completa»; contrato 4.14)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_JO="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_juicio_objetivo_414.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_juicio_objetivo_414.py ) > "$SALIDA_JO" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_juicio_objetivo_414.py" > "$SALIDA_JO"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas del juicio sobre el objetivo \(4\.14\) PASAN$' "$SALIDA_JO" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 27 ]; then
    echo "$linea"; echo "RESULTADO juicio sobre el objetivo: PASA"
  else
    tail -5 "$SALIDA_JO"; echo "RESULTADO juicio sobre el objetivo: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 27 pruebas; ver $SALIDA_JO)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de la verificación de las entradas (personaje_v2/pruebas/test_verificacion_entradas_414.py; obligatoria en «completa»; requisito de cierre 4.14)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_VE="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_verificacion_entradas_414.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_verificacion_entradas_414.py ) > "$SALIDA_VE" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_verificacion_entradas_414.py" > "$SALIDA_VE"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de la verificación de las entradas \(4\.14\) PASAN$' "$SALIDA_VE" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 33 ]; then
    echo "$linea"; echo "RESULTADO verificación de las entradas: PASA"
  else
    tail -5 "$SALIDA_VE"; echo "RESULTADO verificación de las entradas: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 33 pruebas; ver $SALIDA_VE)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de la corrección de la verificación de las entradas (personaje_v2/pruebas/test_verificacion_entradas_415.py; obligatoria en «completa»; encargo correctivo 4.15: R1–R3, I13, I8 e I9)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_X="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_verificacion_entradas_415.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_verificacion_entradas_415.py ) > "$SALIDA_X" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_verificacion_entradas_415.py" > "$SALIDA_X"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de la corrección de la verificación de las entradas \(4\.15\) PASAN$' "$SALIDA_X" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 173 ]; then
    echo "$linea"; echo "RESULTADO verificación de las entradas 4.15: PASA"
  else
    tail -5 "$SALIDA_X"; echo "RESULTADO verificación de las entradas 4.15: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 173 pruebas; ver $SALIDA_X)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de la entrada efectiva del FCF base (personaje_v2/pruebas/test_entrada_efectiva_415.py; obligatoria en «completa»; encargo correctivo 4.15: C48 de Elis)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_X="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_entrada_efectiva_415.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_entrada_efectiva_415.py ) > "$SALIDA_X" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_entrada_efectiva_415.py" > "$SALIDA_X"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de la entrada efectiva \(4\.15\) PASAN$' "$SALIDA_X" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 60 ]; then
    echo "$linea"; echo "RESULTADO entrada efectiva: PASA"
  else
    tail -5 "$SALIDA_X"; echo "RESULTADO entrada efectiva: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 60 pruebas; ver $SALIDA_X)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería del relevo caducado (personaje_v2/pruebas/test_relevo_i19_415.py; obligatoria en «completa»; 4.15, hito 2: I19)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_X="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_relevo_i19_415.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_relevo_i19_415.py ) > "$SALIDA_X" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_relevo_i19_415.py" > "$SALIDA_X"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas del relevo caducado \(4\.15\) PASAN$' "$SALIDA_X" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 5 ]; then
    echo "$linea"; echo "RESULTADO relevo caducado: PASA"
  else
    tail -5 "$SALIDA_X"; echo "RESULTADO relevo caducado: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 5 pruebas; ver $SALIDA_X)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de la integración V6.4 experimental (personaje_v2/pruebas/test_integracion_v64.py; obligatoria en «completa»; encargos 4.11, 4.12 y 4.13)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_V64="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_integracion_v64.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_integracion_v64.py ) > "$SALIDA_V64" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_integracion_v64.py" > "$SALIDA_V64"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de integración V6.4 PASAN$' "$SALIDA_V64" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 199 ]; then
    echo "$linea"; echo "RESULTADO integración V6.4: PASA"
  else
    tail -5 "$SALIDA_V64"; echo "RESULTADO integración V6.4: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 199 pruebas; ver $SALIDA_V64)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de trazabilidad de la 4.10 (personaje_v2/pruebas/test_trazabilidad_v2.py; obligatoria en «completa»; BOM, marcadores de cierre y libro final)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_TRAZABILIDAD="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_trazabilidad_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_trazabilidad_v2.py ) > "$SALIDA_TRAZABILIDAD" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_trazabilidad_v2.py" > "$SALIDA_TRAZABILIDAD"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de trazabilidad de la 4.10 PASAN$' "$SALIDA_TRAZABILIDAD" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 78 ]; then
    echo "$linea"; echo "RESULTADO trazabilidad: PASA"
  else
    tail -5 "$SALIDA_TRAZABILIDAD"; echo "RESULTADO trazabilidad: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 78 pruebas; ver $SALIDA_TRAZABILIDAD)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de integridad de la auditoría vigente (personaje_v2/pruebas/test_integridad_auditoria_v2.py; obligatoria en «completa»; reparación 4.9, R-V1)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_INTEGRIDAD="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_integridad_auditoria_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_integridad_auditoria_v2.py ) > "$SALIDA_INTEGRIDAD" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_integridad_auditoria_v2.py" > "$SALIDA_INTEGRIDAD"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de integridad de la auditoría vigente PASAN$' "$SALIDA_INTEGRIDAD" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 103 ]; then
    echo "$linea"; echo "RESULTADO integridad: PASA"
  else
    tail -5 "$SALIDA_INTEGRIDAD"; echo "RESULTADO integridad: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 103 pruebas; ver $SALIDA_INTEGRIDAD)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de solicitudes de auditoría (personaje_v2/pruebas/test_auditorias_v2.py; obligatoria en «completa»; reparación 4.8.1, R-T1)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_AUDITORIAS="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_auditorias_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_auditorias_v2.py ) > "$SALIDA_AUDITORIAS" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_auditorias_v2.py" > "$SALIDA_AUDITORIAS"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de solicitudes de auditoría PASAN$' "$SALIDA_AUDITORIAS" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 55 ]; then
    echo "$linea"; echo "RESULTADO auditorías: PASA"
  else
    tail -5 "$SALIDA_AUDITORIAS"; echo "RESULTADO auditorías: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 55 pruebas; ver $SALIDA_AUDITORIAS)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de coherencia de estados (personaje_v2/pruebas/test_estados_v2.py; obligatoria en «completa»; reparación 4.8, X-a y X-c)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_ESTADOS="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_estados_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_estados_v2.py ) > "$SALIDA_ESTADOS" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_estados_v2.py" > "$SALIDA_ESTADOS"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de coherencia de estados PASAN$' "$SALIDA_ESTADOS" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 28 ]; then
    echo "$linea"; echo "RESULTADO estados: PASA"
  else
    tail -5 "$SALIDA_ESTADOS"; echo "RESULTADO estados: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 28 pruebas; ver $SALIDA_ESTADOS)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería del resumen (personaje_v2/pruebas/test_resumen_v2.py; obligatoria en «completa»; reparación 4.7)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_RESUMEN="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_resumen_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_resumen_v2.py ) > "$SALIDA_RESUMEN" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_resumen_v2.py" > "$SALIDA_RESUMEN"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de aceptación del resumen PASAN$' "$SALIDA_RESUMEN" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 45 ]; then
    echo "$linea"; echo "RESULTADO resumen: PASA"
  else
    tail -5 "$SALIDA_RESUMEN"; echo "RESULTADO resumen: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 45 pruebas; ver $SALIDA_RESUMEN)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "== batería de cierre (personaje_v2/pruebas/test_cierre_v2.py; obligatoria en «completa»; reparaciones 4.6 y 4.6.1)"
if [ "${1:-}" = "completa" ]; then
  SALIDA_CIERRE="$(mktemp)"
  if [ -f personaje_v2/pruebas/test_cierre_v2.py ]; then
    ( cd personaje_v2 && python3 -B pruebas/test_cierre_v2.py ) > "$SALIDA_CIERRE" 2>&1; rc=$?
  else
    rc=127; echo "FALTA personaje_v2/pruebas/test_cierre_v2.py" > "$SALIDA_CIERRE"
  fi
  linea="$(grep -E '^[0-9]+/[0-9]+ pruebas de aceptación del cierre PASAN$' "$SALIDA_CIERRE" | tail -1)"
  n_ok="${linea%%/*}"; resto="${linea#*/}"; n_tot="${resto%% *}"
  if [ $rc -eq 0 ] && [ -n "$linea" ] && [ "$n_ok" = "$n_tot" ] && [ "${n_tot:-0}" -ge 55 ]; then
    echo "$linea"; echo "RESULTADO cierre: PASA"
  else
    tail -5 "$SALIDA_CIERRE"; echo "RESULTADO cierre: FALLA (código $rc; la batería no pasó, no llegó a ejecutarse o tiene menos de 55 pruebas; ver $SALIDA_CIERRE)"; fallos=$((fallos+1))
  fi
else
  echo "omitida en el modo rápido (solo se ejecuta, y es obligatoria, en «completa»)"
fi

echo "RESULTADO GLOBAL: $([ $fallos -eq 0 ] && echo PASA || echo "FALLA ($fallos bloques)")"
exit $fallos
