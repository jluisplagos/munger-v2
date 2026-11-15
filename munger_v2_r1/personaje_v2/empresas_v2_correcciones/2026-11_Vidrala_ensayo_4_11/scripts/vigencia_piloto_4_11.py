#!/usr/bin/env python3
"""Vigencia del piloto 4.11 con el código final de la entrega (encargo: «los cambios posteriores relevantes requerirán revisar su vigencia»).
Las correcciones de la revisión interna (H1, H2, H3, H7, H9–H12) se hicieron después del cierre del piloto. Este script comprueba, SOLO EN
LECTURA, que con el código actual el cierre del piloto sigue vigente y que las comprobaciones nuevas lo aceptan:
  - cierre_v2.motivo_vigencia (la que usan el pipeline, ficha.py, informe.py y resumen.py) → None;
  - seleccion_plantilla.comprobar con config_v2_v64_experimental.json → None (plantilla_activa.json coincide);
  - pipeline.variantes_corresponden (paso 12, H10) → None, y configuracion_en_libros_distinta → ninguna;
  - destino del resumen con el código actual (H2) frente al destino registrado al publicar.
Antes y después toma la huella (SHA-256 y fecha) de todos los archivos de piloto/: el script falla si algo cambia.
Escribe …/2026-11_Vidrala_ensayo_4_11/resultados/vigencia_piloto_4_11.json y .md.
Uso (desde munger_v2_r1/): python3 -I …/2026-11_Vidrala_ensayo_4_11/scripts/vigencia_piloto_4_11.py
"""
import hashlib
import json
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
ENS = os.path.dirname(AQUI)
RAIZ = os.path.abspath(os.path.join(ENS, "..", "..", ".."))
PV = os.path.join(RAIZ, "personaje_v2")
PIL = os.path.join(ENS, "piloto")
C = os.path.join(PIL, "Vidrala")
sys.path.insert(0, os.path.join(PV, "scripts"))
CFG64 = os.path.join(PV, "config_v2_v64_experimental.json")
os.environ["MUNGER_CONFIG"] = CFG64
import cierre_v2 as CIE  # noqa: E402
import config_v2  # noqa: E402
import pipeline as P  # noqa: E402
import seleccion_plantilla as SEL  # noqa: E402


def huellas(d):
    out = {}
    for r, ds, fs in os.walk(d):
        for f in fs:
            p = os.path.join(r, f)
            if os.path.islink(p):
                continue
            out[os.path.relpath(p, d)] = (hashlib.sha256(open(p, "rb").read()).hexdigest(), os.path.getmtime(p))
    return out


def main():
    antes = huellas(PIL)
    cfg = config_v2.cargar(CFG64)
    # el tercer argumento es el nombre del expediente (la carpeta), como lo pasa el pipeline (Pipeline.E): con él se nombran los libros
    m_vig = CIE.motivo_vigencia(C, P.Pipeline.veredicto_auditoria, os.path.basename(C))
    m_sel = SEL.comprobar(C, cfg)
    pp = P.Pipeline(C, cfg)
    m_var = pp.variantes_corresponden()
    dist = pp.configuracion_en_libros_distinta(os.path.join(C, "configuracion_economica.json"))
    reg = json.load(open(os.path.join(C, "publicaciones_resumen.json"), encoding="utf-8"))
    registrados = sorted({os.path.relpath(e.get("csv"), RAIZ) for e in reg.get("publicaciones") or [] if e.get("csv")})
    estados = sorted({e.get("estado") for e in reg.get("publicaciones") or []})
    actual = os.path.relpath(CIE.ruta_resumen(C, cfg), RAIZ)
    despues = huellas(PIL)
    intacto = antes == despues
    ok = m_vig is None and m_sel is None and m_var is None and not dist and intacto
    out = {"expediente": os.path.relpath(C, RAIZ), "estado": {k: pp.st.get(k) for k in ("paso", "estado_analisis", "auditoria")},
           "motivo_vigencia": m_vig, "seleccion_de_plantilla": m_sel, "variantes_corresponden": m_var, "configuracion_en_libros_distinta": dist,
           "resumen_registrado_al_publicar": registrados, "estado_de_las_publicaciones": estados, "resumen_con_el_codigo_actual": actual,
           "archivos_examinados": len(antes), "piloto_intacto": intacto, "resultado": "VIGENTE" if ok else "NO VIGENTE O ALTERADO",
           "nota": ("Solo lectura. Las salidas del piloto (ficha, informe, entrada_v63.md, resumen) no se regeneran: ficha.py con el código actual "
                    "escribiría una ficha de contenido distinto (los dos límites de R1, H12), y sustituir una ficha cerrada exige una auditoría nueva "
                    "(Anexo D). Una ejecución nueva del piloto publicaría en el resumen del código actual.")}
    json.dump(out, open(os.path.join(ENS, "resultados", "vigencia_piloto_4_11.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    md = ["# Vigencia del piloto 4.11 con el código final de la entrega", "",
          "Comprobación solo en lectura, con las funciones que usan el pipeline y los generadores, después de las correcciones de la revisión interna.", "",
          f"- Expediente: `{out['expediente']}` · estado {out['estado']}.",
          f"- `cierre_v2.motivo_vigencia`: {'ninguno (el cierre sigue vigente)' if m_vig is None else m_vig}.",
          f"- Selección de plantilla con `config_v2_v64_experimental.json`: {'conforme' if m_sel is None else m_sel}.",
          f"- Paso 12, variantes frente a `precio.json` (H10): {'corresponden' if m_var is None else m_var}.",
          f"- Celdas de configuración de los libros frente a `configuracion_economica.json`: {'iguales' if not dist else dist}.",
          f"- Resumen registrado al publicar: {', '.join('`' + x + '`' for x in registrados)} ({', '.join(str(x) for x in estados)}). Con el código actual, una publicación nueva iría a `{actual}` (H2).",
          f"- Archivos de `piloto/` examinados antes y después: {len(antes)} · {'ninguno cambió' if intacto else 'ALGUNO CAMBIÓ'}.",
          "", f"**Resultado: {out['resultado']}.**", "", "**Nota.** " + out["nota"], ""]
    open(os.path.join(ENS, "resultados", "vigencia_piloto_4_11.md"), "w", encoding="utf-8").write("\n".join(md))
    print("\n".join(md))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
