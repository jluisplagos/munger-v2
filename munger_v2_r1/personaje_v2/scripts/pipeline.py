#!/usr/bin/env python3
"""Orquestador del pipeline por empresa (encargo §4.7, pasos 0–14). Una orden por paso; cada paso deja un archivo.

Uso: pipeline.py CARPETA_EMPRESA [--config config_v2.json] [--agentes-simulados DIR] [--hasta N] [--reiniciar] [--desde N]

CARPETA_EMPRESA contiene: etapa1/<E>_evaluada.xlsx (+ respuesta.md, juicio.json, extracto.md), fase1_v63.json, texto/ (opcional).
Los pasos de agente (5 extracción, 6 fase A, 8 fase B, 10 fase C en dos turnos, 13 verificación) NO se ejecutan aquí: el pipeline
escribe prompts_generados/<paso>.md con el prompt y las entradas, deja ESPERANDO.md y termina con código 10. Cuando el archivo
de salida del agente exista (fase_a.json, fase_b.json, fase_c.json, extracto_v63.md, auditoria.md), se vuelve a lanzar y continúa.
Con --agentes-simulados DIR, toma de DIR los archivos de los agentes (fase_a.json, fase_b.json, fase_b.intento2.json, fase_c.turno1.json,
fase_c.turno2.json, auditoria.md …) para las pruebas con datos sintéticos (§10.2).
Estados finales: concluido · pendiente_de_datos · pendiente_de_investigacion · modelo_no_aplicable · no_entregable. Agotar un límite
de correcciones NUNCA aprueba: termina en no_entregable con diagnostico.md (D17, D18).
Códigos: 0 terminado (cualquier estado final, con sus salidas) · 10 esperando a un agente · 2 uso · 1 fallo mecánico no previsto ·
4 cierre rechazado (paso 14 sin una auditoría APROBADO válida del material vigente; reparación del cierre, entrega 4.6).
5 retirada pendiente: una aprobación publicada en un destino registrado del resumen no se pudo retirar (reparación 4.7).
(4.8) Una ficha que no cumple su esquema en el paso 14 termina en no_entregable por fallo de implementación con código 0 (estado final) y el
diagnóstico «continuar desde el paso 13»; en las terminaciones que no cierran, el estado fijado por terminar() se conserva aunque se
archive una ficha cerrada anterior (X-a). La última línea dice el estado, la causa y el paso desde el que se continúa.
(4.8.1, R-T1) El paso 13 registra una SOLICITUD de auditoría identificable y persistente (estado_pipeline.json → solicitudes_auditoria,
solicitud_auditoria.json), ligada al material fijado y conservada en los relanzamientos mientras esté pendiente; al registrarla anota
como conocidas todas las auditorías del expediente (también en auditorias_conocidas.json) y archiva un cierre vigente. Solo acepta
como respuesta un auditoria.md que la nombre («Solicitud de auditoría: SA-…») y que, si aprueba, no sea ninguna auditoría conocida
ni por su huella SHA-256 ni por su contenido sin formato (cierre_v2.huella_contenido); las fechas de los archivos no intervienen. Con
una solicitud pendiente no se cierra; un cierre de la 4.8.1 exige que auditoria.md sea la respuesta registrada. Código 6: el
registro auditorias_conocidas.json existe y no se puede leer (no se acepta ninguna auditoría hasta restaurarlo); (4.9) también si
estado_pipeline.json no se puede leer, después de retirar una salida oficial cerrada que ya no puede acreditarse.
(4.9, R-V1) La respuesta aceptada se registra también con su huella fiel (cierre_v2.huella_fiel: contenido y orden íntegros salvo
cierre_v2.TRANSFORMACIONES_INOCUAS). Después del cierre, la vigencia comprueba por separado la solicitud, el material y esa huella: el
contenido sin orden (huella_contenido) solo detecta reutilizaciones en el paso 13 y ya no acredita la identidad de la respuesta.
Cierre (4.6, cierre_v2.py): la fase C propone el estado; el paso 11 escribe solo material provisional (ficha_provisional.json,
informe_provisional.md); el paso 13 fija el material auditado (material_auditoria.json) y la auditoría tiene que nombrarlo; la
ficha y el informe oficiales se escriben en el paso 14 solo con esa aprobación, o por terminar() en los estados que no pasan por la
auditoría (no_entregable, pendiente_de_datos o modelo_no_aplicable tempranos).
Vigencia (4.6.1): al empezar cada ejecución, en el paso 11 y en el rechazo del paso 14, una salida oficial cerrada que ya no corresponde a
una aprobación válida del material actual se archiva en historial_cierres/ (con RETIRADA.json, la fila del resumen y el historial).
"""
import argparse
import datetime as dt
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import config_v2  # noqa: E402
import celdas_v2 as C  # noqa: E402
import cierre_v2 as CIE  # noqa: E402
import configuracion_economica as CE  # noqa: E402  (4.11: V6.4 experimental)
import seleccion_plantilla as SEL  # noqa: E402  (4.11: selección explícita de plantilla y configuración)
import estructura_json as ESTR  # noqa: E402  (4.13 §3: validación estructural)

PY = sys.executable


class Esperando(Exception):
    pass


class CierreRechazado(Exception):
    pass


def modo_entrada_efectiva(carpeta):
    """(4.15, segunda revisión independiente, N7) («estricta» | «registrada», origen de la declaración).
    - entrada_efectiva.json (lo escribe cambiar_base.py en todo expediente nuevo; por defecto «estricta»): manda; ilegible, con otro modo o
      «registrada» sin motivo → ValueError (falla en cerrado: el paso se detiene);
    - si no existe, «entrada_efectiva»: «estricta» en alcance_v2.json (forma del hito 1 de la 4.15);
    - si no hay ninguna declaración: «registrada» (expedientes anteriores a la 4.15 y línea de base v2.2: el valor de la etapa 1 prevalece,
      pero rellenar_fase1_v63.py lo registra y verificacion_entradas.py lo bloquea si fase1_v63.json no lo reproduce)."""
    p = os.path.join(carpeta, "entrada_efectiva.json")
    # (4.15, tercera revisión, T5) fase1_metadatos.json registra el modo que declaró cambiar_base.py: si falta el archivo o dice otra cosa, error
    meta_modo = None
    try:
        _m = json.load(open(os.path.join(carpeta, "fase1_metadatos.json"), encoding="utf-8"))
        meta_modo = _m.get("entrada_efectiva") if isinstance(_m, dict) else None
    except (OSError, ValueError):
        pass
    if os.path.lexists(p) and not os.path.isfile(p):
        raise ValueError("entrada_efectiva.json no es un archivo legible")
    if not os.path.exists(p) and meta_modo is not None:
        raise ValueError(f"fase1_metadatos.json registra el modo {meta_modo!r} y falta entrada_efectiva.json")
    otros = [n for n in os.listdir(carpeta) if n.lower() == "entrada_efectiva.json" and n != "entrada_efectiva.json"] if os.path.isdir(carpeta) else []
    if otros:
        raise ValueError(f"declaración con otra grafía ({', '.join(otros)}): el archivo es entrada_efectiva.json")
    if os.path.exists(p):
        try:
            d = json.load(open(p, encoding="utf-8"))
        except (OSError, ValueError) as ex:
            raise ValueError(f"no se puede leer ({type(ex).__name__})") from None
        if not isinstance(d, dict) or d.get("modo") not in ("estricta", "registrada"):
            raise ValueError("el modo tiene que ser «estricta» o «registrada»")
        if d["modo"] == "registrada" and not str(d.get("motivo") or "").strip():
            raise ValueError("el modo «registrada» exige su motivo")
        if meta_modo is not None and meta_modo != d["modo"]:
            raise ValueError(f"entrada_efectiva.json dice {d['modo']!r} y fase1_metadatos.json registra {meta_modo!r}")
        if d["modo"] == "registrada" and _alcance_modo(carpeta) == "estricta":
            # (4.15, hito 2, U6 c) dos declaraciones contradictorias: no gana la permisiva en silencio
            raise ValueError("entrada_efectiva.json dice «registrada» y alcance_v2.json declara «estricta»: declaraciones contradictorias")
        return d["modo"], "entrada_efectiva.json"
    if _alcance_modo(carpeta) == "estricta":
        return "estricta", "alcance_v2.json"
    return "registrada", None


def _ediciones(a, b):
    """(4.15, hito 2, T6) Distancia de edición (Levenshtein) entre dos textos cortos."""
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def _alcance_modo(carpeta):
    """(4.15, hito 2, U6 b) «estricta» si alcance_v2.json la declara; None si no declara nada. Falla en cerrado (ValueError) si el alcance
    existe pero no se puede leer o no es un objeto, si la clave lleva otro valor o si una clave es una errata de «entrada_efectiva»
    («entrada_efectiba», «Entrada-Efectiva»…): antes, cualquiera de esos casos dejaba el modo en «registrada» en silencio."""
    import difflib
    pa = os.path.join(carpeta, "alcance_v2.json")
    if not os.path.exists(pa):
        return None
    try:
        a = json.load(open(pa, encoding="utf-8"))
    except (OSError, ValueError) as ex:
        raise ValueError(f"alcance_v2.json no se puede leer ({type(ex).__name__}): no se puede determinar el modo de la entrada efectiva") from None
    if not isinstance(a, dict):
        raise ValueError("alcance_v2.json no es un objeto: no se puede determinar el modo de la entrada efectiva")
    # (hito 2, N9) una errata se parece mucho a «entrada_efectiva» (proporción ≥ 0,88: «entrada_efectiba», «Entrada-Efectiva», «entrda_efectiva»);
    # otra clave que solo comparte una palabra («tasa_efectiva») no es una errata
    # (T6) también a dos o tres ediciones de distancia (erratas dobles); «tasa_efectiva» queda a más de tres
    parecidas = [k for k in a if k != "entrada_efectiva" and (difflib.SequenceMatcher(None, re.sub(r"[^a-z]", "", str(k).lower()), "entradaefectiva").ratio() >= 0.88
                                                              or _ediciones(re.sub(r"[^a-z]", "", str(k).lower()), "entradaefectiva") <= 3)]
    if parecidas:
        raise ValueError(f"alcance_v2.json tiene la clave {parecidas[0]!r}, que parece una errata de «entrada_efectiva»")
    if "entrada_efectiva" in a:
        if a["entrada_efectiva"] != "estricta":  # (T5) una errata no deja el modo en «registrada» en silencio
            raise ValueError(f"alcance_v2.json declara «entrada_efectiva»: {a['entrada_efectiva']!r}; el único valor admitido es «estricta»")
        return "estricta"
    return None

class Pipeline:
    def __init__(self, carpeta, cfg, simulados=None):
        self.c = os.path.abspath(carpeta)
        self.E = os.path.basename(self.c)
        self.cfg = cfg
        self.sim = simulados
        self.lim = cfg.get("limites", {})
        # (4.11) plantilla V6.4 experimental seleccionada explícitamente con --config; la configuración económica sale del expediente
        self.v64 = SEL.es_v64(cfg)
        # perfil de LibreOffice propio de cada empresa (recalc.sh lo crea): dos soffice sobre el mismo perfil se bloquean (§4.7, en paralelo)
        self.perfil = os.path.join(self.c, ".lo_perfil") if cfg.get("recalc", {}).get("perfil_por_empresa", True) else cfg.get("recalc", {}).get("perfil", os.path.join(self.c, ".lo_perfil"))
        self.estado_path = os.path.join(self.c, "estado_pipeline.json")
        self.st = json.load(open(self.estado_path, encoding="utf-8")) if os.path.exists(self.estado_path) else {
            "paso": 0, "estado_analisis": None, "intentos": {"fase_b": 0, "fase_c": 0, "auditoria": 0, "vueltas_c_a_b": 0, "vueltas_b_a_a": 0},
            "historial": [], "motor": None, "fase_b_escrita": False, "fase_c_escrita": False, "esperando": None, "inicio": dt.datetime.now().isoformat(timespec="seconds")}
        if not isinstance(self.st, dict):
            # (4.9, control de vigencia V-2) un JSON válido que no es un objeto es tan ilegible como uno roto
            raise ValueError("estado_pipeline.json no es un objeto JSON")
        m = CIE._motivo_estructura(self.st, None, None)
        if m:
            # (segundo control de vigencia, W-1) solicitudes sin «id», historial, cierres_archivados o paso con tipos erróneos
            raise ValueError(m)

    # ---------- utilidades ----------
    def p(self, *x):
        return os.path.join(self.c, *x)

    def guardar(self):
        json.dump(self.st, open(self.estado_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    def log(self, msg):
        self.st["historial"].append(f"{dt.datetime.now().isoformat(timespec='seconds')} · paso {self.st['paso']} · {msg}")
        print(f"[paso {self.st['paso']}] {msg}")
        self.guardar()

    def run(self, cmd, ok=(0,)):
        r = subprocess.run(cmd, capture_output=True, text=True, cwd=self.c)
        salida = (r.stdout + r.stderr).strip()
        self.st["historial"].append(f"  $ {' '.join(os.path.basename(str(x)) for x in cmd)} → {r.returncode} · {salida.splitlines()[-1][:200] if salida else ''}")
        return r.returncode, salida

    def script(self, nombre):
        return os.path.join(AQUI, nombre)

    def comprobaciones_dagger(self):
        """Criterios † de §10.2 (1 y 3), exigidos en todos los estados: libro evaluado íntegro y celdas de las fases escritas
        correctas. Devuelve None si pasan (o no hay libro evaluado todavía) o el detalle del fallo."""
        libro_ev = self.p(f"{self.E}_v63_evaluada.xlsx")
        libro_datos = self.p(f"{self.E}_v63_datos.xlsx")
        if not os.path.exists(libro_ev):
            return None
        rc, out = self.run([PY, self.cfg["plantilla"]["verificador"], libro_ev, self.cfg["plantilla"]["referencia"]])
        if rc != 0:
            return "criterio 1 †: verificar_v63.py sobre el libro evaluado: " + out[-300:]
        fases = "A" + (",B" if self.st.get("fase_b_escrita") else "") + (",C" if self.st.get("fase_c_escrita") else "")
        if os.path.exists(libro_datos):
            # el motor de la fase A manda sobre las reglas condicionales (C76, B16:D16) aunque C62 se haya corregido a «otro método»
            rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", fases] + (["--motor", self.st["motor"]] if self.st.get("motor") else []))
            if rc != 0:
                return f"criterio 3 †: comprobar_celdas_v2.py (fases {fases}): " + out[-300:]
        return None

    def terminar(self, estado, tipo, detalle, paso, comprobacion=None, categoria=None, que_hace_falta="", desde=None):
        if estado != "no_entregable":
            fallo = self.comprobaciones_dagger()
            if fallo:
                self.log(f"el estado {estado} no se puede entregar: {fallo[:160]}")
                estado, tipo, detalle = "no_entregable", "fallo_de_implementacion", f"{fallo} (estado previsto: {estado}; {detalle})"
        self.st["estado_analisis"] = estado
        self.guardar()
        self.run([PY, self.script("diagnostico.py"), self.c, "--estado", estado, "--tipo", tipo, "--detalle", detalle, "--paso", str(paso)]
                 + (["--comprobacion", comprobacion] if comprobacion else []) + (["--categoria", categoria] if categoria else [])
                 + ["--que-hace-falta", que_hace_falta or detalle, "--desde-paso", str(desde if desde is not None else paso)])
        if self.salidas_finales(cierre=False):
            # (4.8, Z-g de la auditoría interna) la ficha no cumplió su esquema: el FIN dice la causa real (la del diagnóstico)
            dg = json.load(open(self.p("diagnostico.json"), encoding="utf-8")) if os.path.exists(self.p("diagnostico.json")) else {}
            tipo, detalle = (dg.get("causa") or {}).get("tipo") or "fallo_de_implementacion", (dg.get("causa") or {}).get("detalle") or detalle
        self.log(f"FIN · estado {self.st.get('estado_analisis')} · {tipo}: {detalle[:160]}")

    def salidas_finales(self, cierre=False):
        """Escribe ficha, informe y resumen del estado de self.st. `cierre` = True solo en el paso 14 (estado que confirma una
        auditoría APROBADO); False en las terminaciones que no pasan por la auditoría (terminar()). Devuelve True si la ficha no
        cumplió su esquema y el análisis quedó en no_entregable por fallo de implementación (criterio 7 †; X-c, entrega 4.8)."""
        previsto = self.st.get("estado_analisis")
        archivados_al_empezar = len(self.st.get("cierres_archivados") or [])
        if previsto == "concluido":
            # un diagnóstico de una ejecución anterior no debe quedar junto a un resultado concluido (p. ej. al reanudar con --desde)
            for f in ("diagnostico.md", "diagnostico.json"):
                if os.path.exists(self.p(f)):
                    os.replace(self.p(f), self.p(f + ".anterior"))
        # (4.8, X-a) en una terminación que no cierra, el estado que fijó terminar() es legítimo y se conserva aunque ficha.py archive
        # la ficha cerrada anterior; en el paso 14, el archivo manda (W-e de la 4.7.1)
        conservar = not cierre
        self.run([PY, self.script("ficha.py"), self.c, "--estado", previsto])
        self.adoptar_archivo(conservar_estado=conservar)
        rc, out = self.run([PY, self.script("validar_esquema.py"), self.p("ficha.json"), "ficha", "--salida", self.p("esquema_ficha.json.txt")])
        self.st["ficha_valida"] = rc == 0
        fallo_esquema = False
        if rc != 0 and previsto == "no_entregable":
            # (4.8, Z-g) ya era no_entregable: se deja constancia de que, además, la ficha no cumple su esquema
            self.log("aviso: ficha.json (no_entregable) tampoco cumple su esquema (criterio 7 †; ver esquema_ficha.json.txt)")
        if rc != 0 and previsto != "no_entregable":
            # criterio 7 †: una ficha que no cumple su esquema es un fallo de implementación, no un aviso. (4.8, X-c) El estado previsto
            # es el que se pidió escribir (no el que haya dejado un archivo intermedio); la ficha no_entregable nunca lleva «cierre»
            # (ficha.py), y en el paso 14 la vía de subsanación es corregir el código o el esquema y pedir una auditoría nueva (paso 13):
            # la ficha cerrada anterior queda archivada en historial_cierres/ y su aprobación no se reutiliza.
            fallo_esquema = True
            paso_fallo = 14 if cierre else self.st.get("paso", 14)
            self.st["estado_analisis"] = "no_entregable"
            self.st["paso"] = paso_fallo
            self.guardar()
            que = ("corregir ficha.py o esquema/ficha.esquema.json (ver esquema_ficha.json.txt) y relanzar pipeline.py --desde 13: el cierre no se escribió, "
                   "la ficha cerrada anterior queda archivada en historial_cierres/ y hace falta una auditoría nueva del material"
                   if cierre else "corregir ficha.py o esquema/ficha.esquema.json (ver esquema_ficha.json.txt) y relanzar desde el paso indicado")
            self.run([PY, self.script("diagnostico.py"), self.c, "--estado", "no_entregable", "--tipo", "fallo_de_implementacion",
                      "--detalle", f"ficha.json no cumple su esquema (criterio 7 †; estado previsto: {previsto}): " + out[-300:], "--paso", str(paso_fallo),
                      "--que-hace-falta", que, "--desde-paso", str(13 if cierre else paso_fallo)])
            self.run([PY, self.script("ficha.py"), self.c, "--estado", "no_entregable"])
            conservar = True  # no_entregable es un estado final legítimo que no se cierra con auditoría
            self.adoptar_archivo(conservar_estado=True)  # archivar_salidas registra la aprobación archivada y la retira
            if cierre and self.st.get("auditoria") == "APROBADO":
                self.st["auditoria"] = None  # la aprobación era del material de un cierre que no se ha podido escribir
                self.guardar()
            rc2, _ = self.run([PY, self.script("validar_esquema.py"), self.p("ficha.json"), "ficha", "--salida", self.p("esquema_ficha.json.txt")])
            self.st["ficha_valida"] = rc2 == 0
            self.log(f"ficha.json no cumplía su esquema: estado {previsto} → no_entregable (fallo de implementación; ver diagnostico.md)")
        self.run([PY, self.script("informe.py"), self.c])
        self.adoptar_archivo(conservar_estado=conservar)
        csv = CIE.ruta_resumen(self.c, self.cfg)
        rc_res, _ = self.run([PY, self.script("resumen.py"), self.c, csv])
        self.adoptar_archivo(conservar_estado=conservar)
        # (4.8, Z-a de la auditoría interna) si resumen.py no pudo publicar la fila del estado final (p. ej. retirada pendiente, código 5),
        # queda anotado: la siguiente ejecución, una vez completadas las retiradas, la vuelve a publicar aunque el estado sea final
        self.st["resumen_pendiente"] = rc_res != 0
        if conservar and self.st.get("estado_analisis") and not os.path.exists(self.p("ficha.json")) \
                and len(self.st.get("cierres_archivados") or []) > archivados_al_empezar:
            # (4.8, Z-f) un estado final sin ficha oficial no se conserva cuando un generador la ARCHIVÓ en esta llamada (V-b del control de
            # vigencia: si ficha.py no llegó a escribirla, p. ej. alcance_v2.json ilegible, el estado y su diagnóstico se conservan)
            self.log(f"el estado {self.st.get('estado_analisis')} no tiene ficha oficial tras las salidas finales: queda sin estado final")
            self.st["estado_analisis"] = None
            self.st["paso"] = min(self.st.get("paso") or 13, 13)
        self.guardar()
        return fallo_esquema

    def adoptar_archivo(self, conservar_estado=False):
        """(4.7.1, W-e de la auditoría interna) ficha.py, informe.py y resumen.py pueden archivar las salidas oficiales (sustitución de
        una ficha cerrada, salida que ya no es vigente) y dejar en el disco el estado sin cierre. Ese estado manda sobre el de la
        memoria en lo que toca al cierre: no se sobrescribe, y el pipeline no declara después un cierre que ya no existe.
        (4.8, X-a) Con `conservar_estado` (terminación que no cierra: terminar(), o no_entregable por fallo de esquema) se adoptan la
        auditoría retirada, los cierres archivados y el historial, pero se conservan el estado_analisis y el paso de la memoria: son
        el resultado legítimo de esta ejecución, y el disco queda con ese mismo estado en la primera ejecución."""
        disco = json.load(open(self.estado_path, encoding="utf-8")) if os.path.exists(self.estado_path) else {}
        # (4.13.1, H5; revisión interna D2-4) la publicación que registra resumen.py (identidad de la aprobación y destino) se adopta siempre:
        # si no, el estado de la memoria la sobrescribe al guardar y la señal de publicación del propio estado se pierde
        pubs_d = disco.get("publicaciones_de_la_aprobacion") if isinstance(disco, dict) else None
        if isinstance(pubs_d, list):
            mias = self.st.setdefault("publicaciones_de_la_aprobacion", [])
            if isinstance(mias, list):
                nuevas = [x for x in pubs_d if x not in mias]
                if nuevas:
                    mias.extend(nuevas)
                    self.guardar()
        nuevos = (disco.get("cierres_archivados") or [])[len(self.st.get("cierres_archivados") or []):]
        if not nuevos:
            return False
        self.st["cierres_archivados"] = disco["cierres_archivados"]
        for k in (("auditoria",) if conservar_estado else ("estado_analisis", "auditoria", "paso")):
            self.st[k] = disco.get(k)
        ya = set(self.st.get("historial") or [])
        self.st.setdefault("historial", []).extend(h for h in (disco.get("historial") or []) if h not in ya)
        self.guardar()
        return True

    def consumir(self, salida):
        """Registra que la salida actual del agente ya se usó: una petición posterior del mismo archivo exige uno más nuevo
        (vuelta C→B, vuelta B→A, auditoría tras una corrección de la fase C)."""
        destino = self.p(salida)
        self.st.setdefault("consumidos", {})[salida] = os.path.getmtime(destino) if os.path.exists(destino) else 0
        self.st["esperando"] = None
        self.st["motivo_correccion"] = None
        self.guardar()

    def agente(self, paso, nombre, salida, entradas, alternativas=()):
        """Si existe una salida del agente NUEVA (o una simulada), la consume y sigue; si no, deja el prompt y ESPERANDO.md
        y lanza Esperando. Tras pedir una corrección (pedir_correccion), exige un archivo más nuevo que la petición; tras
        consumir una salida, exige un archivo más nuevo que el consumido (nunca se relee la misma salida como si fuera otra)."""
        destino = self.p(salida)
        marca = f"{paso}:{salida}"
        if self.sim:
            for alt in list(alternativas) + [salida]:
                src = os.path.join(self.sim, alt)
                if os.path.exists(src):
                    shutil.copy(src, destino)
                    os.utime(destino, None)
                    self.log(f"agente simulado: {alt} → {salida}")
                    self.consumir(salida)
                    return
        consumido = self.st.get("consumidos", {}).get(salida)
        if os.path.exists(destino):
            mt = os.path.getmtime(destino)
            if self.st.get("esperando") == marca:
                if mt >= self.st.get("esperando_desde", 0) and (consumido is None or mt > consumido):
                    self.consumir(salida)
                    return
            elif consumido is None or mt > consumido:
                self.consumir(salida)
                return
        motivo = self.st.get("motivo_correccion") if self.st.get("esperando") == marca else None
        self.escribir_prompt(paso, nombre, salida, entradas, motivo)
        if self.st.get("esperando") != marca or "esperando_desde" not in self.st:
            self.st["esperando_desde"] = dt.datetime.now().timestamp()
        self.st["esperando"] = marca
        self.guardar()
        raise Esperando(f"{nombre} → {salida}")

    # ---------- solicitudes de auditoría (4.8.1, R-T1) ----------
    def solicitud_auditoria_vigente(self):
        """Solicitud pendiente del material fijado: se conserva en los relanzamientos (también con --desde 13) mientras siga pendiente
        y el material sea el mismo; si no hay ninguna pendiente, o el material cambió, se registra una nueva. Las solicitudes no se
        borran: estado_pipeline.json → solicitudes_auditoria guarda todas, con su estado (pendiente, respondida, sustituida)."""
        st = self.st
        lista = st.setdefault("solicitudes_auditoria", [])
        mat = st.get("material_auditoria")
        ahora = dt.datetime.now().astimezone().isoformat(timespec="seconds")
        actual = lista[-1] if lista and lista[-1].get("estado") == "pendiente" else None
        if actual and actual.get("material") == mat:
            CIE.escribir_solicitud(self.c, actual)
            return actual
        if actual:
            actual["estado"] = "sustituida"
            actual["sustituida"] = ahora
            actual["motivo_sustitucion"] = f"el material fijado es {mat}, no {actual.get('material')}"
        motivo = (f"corrección pedida por el pipeline: {str(st.get('motivo_correccion'))[:200]}" if st.get("esperando") == "13:auditoria.md" and st.get("motivo_correccion")
                  else "auditoría del material fijado en el paso 13")
        _rels = st.get("relevos_caducados")
        rel = _rels[-1] if isinstance(_rels, list) and _rels and isinstance(_rels[-1], dict) else None
        # (hito 2, N10) solo el relevo que llevó a fijar ESTE material, y una sola vez (no se arrastra a una solicitud posterior por otra causa)
        if isinstance(rel, dict) and not rel.get("solicitud") and rel.get("material_refijado") == mat:
            # (4.15, hito 2, H9) el auditor ve que la solicitud sustituye a un relevo caducado y qué archivos cambiaron
            _arch = rel.get("archivos_cambiados")
            _arch = [str(x) for x in _arch] if isinstance(_arch, list) else [str(_arch)]  # (hito 2, T9) un registro mal formado no detiene nada
            motivo = (f"relevo caducado: el material fijado {rel.get('material_fijado')} ya no era el vigente (cambian: "
                      f"{', '.join(_arch)[:300]}); se repitió la verificación (paso 12). " + motivo)
        nueva = CIE.nueva_solicitud(mat, motivo, ahora)
        if isinstance(rel, dict) and not rel.get("solicitud") and rel.get("material_refijado") == mat:
            rel["solicitud"] = nueva.get("id")
        # (auditoría interna de la 4.8.1, Y-b; control de vigencia, V-2) todas las auditorías que ya hay en el expediente (cualquier
        # archivo de texto con forma de auditoría, con cualquier nombre y en cualquier subcarpeta, y la que registra cierre_vigente.json)
        # quedan anotadas como conocidas antes de la solicitud: ninguna puede acreditar una aprobación que la responda. Ninguna recibe una
        # solicitud: no se asigna retroactivamente. El registro persiste en auditorias_conocidas.json.
        shas, conts = CIE.auditorias_del_expediente(self.c, self.veredicto_auditoria)
        st["anteriores_sha256"] = sorted(set(st.get("anteriores_sha256") or []) | shas)
        st["anteriores_contenido"] = sorted(set(st.get("anteriores_contenido") or []) | conts)
        CIE.anotar_auditorias(self.c, shas, conts, f"solicitud {nueva['id']}")
        lista.append(nueva)
        CIE.escribir_solicitud(self.c, nueva)
        F = json.load(open(self.p("ficha.json"), encoding="utf-8")) if os.path.exists(self.p("ficha.json")) else None
        if CIE.ficha_cerrada(F) or os.path.lexists(self.p("cierre_vigente.json")):  # (4.10, §3.3) también sin marcadores, con cierre registrado
            # (Y-h) pedir una auditoría nueva retira el cierre vigente hasta su respuesta, en la misma ejecución (ficha, informe y fila del
            # resumen se archivan con su retirada; la aprobación registrada se retira)
            CIE.archivar_salidas(self.c, f"se pidió una auditoría nueva (solicitud {nueva['id']}): el cierre anterior no vale hasta su respuesta",
                                 CIE.ruta_resumen(self.c, self.cfg), st)
            self.log(f"cierre vigente archivado al registrar la solicitud {nueva['id']}")
        st["auditoria"] = None
        self.log(f"solicitud de auditoría {nueva['id']} registrada para el material {mat}" + (f" (sustituye a {actual['id']})" if actual else ""))
        self.guardar()
        return nueva

    def huellas_auditorias_usadas(self):
        return (set(self.st.get("anteriores_sha256") or []) | CIE.registro_auditorias(self.c)[0]
                | {s.get("respuesta_sha256") for s in self.st.get("solicitudes_auditoria") or [] if s.get("respuesta_sha256")})

    def contenidos_auditorias_usadas(self):
        return (set(self.st.get("anteriores_contenido") or []) | CIE.registro_auditorias(self.c)[1]
                | {s.get("respuesta_contenido") for s in self.st.get("solicitudes_auditoria") or [] if s.get("respuesta_contenido")})

    def agente_auditoria(self, sol, alternativas=()):
        """Paso 13 (4.8.1, R-T1): acepta auditoria.md solo si responde a la solicitud vigente: una sola línea «Solicitud de auditoría:
        <id>» con el id de `sol` y, si aprueba según H2, ni su huella SHA-256 ni su contenido sin formato (huella_contenido: sin
        formato, tildes ni orden de líneas) son los de una auditoría conocida del expediente o ya usada; una REPETIR puede repetir
        contenido, porque no cierra nada. Las fechas de modificación no intervienen. Si no la hay, deja el prompt (con el id) y ESPERANDO.md, con el motivo por el que no se aceptó el archivo presente,
        y lanza Esperando (código 10). La regla H2 y la vinculación al material se aplican después, sin cambios."""
        st = self.st
        destino = self.p("auditoria.md")
        marca = "13:auditoria.md"
        if self.sim:
            for alt in list(alternativas) + ["auditoria.md"]:
                src = os.path.join(self.sim, alt)
                if os.path.exists(src):
                    # agente simulado: responde a la solicitud que ve (marcador {SOLICITUD_AUDITORIA} del archivo simulado)
                    open(destino, "w", encoding="utf-8").write(open(src, encoding="utf-8").read().replace("{SOLICITUD_AUDITORIA}", sol["id"]))
                    self.log(f"agente simulado: {alt} → auditoria.md")
                    break
        no_aceptada = None
        if os.path.exists(destino):
            h = CIE.sha_archivo(destino)
            # (4.10, encargo §3.2) la misma lectura común que el cierre y la vigencia (cierre_v2.texto_fiel: solo las transformaciones
            # inocuas declaradas) antes de H2 y de los lectores de solicitud y material; las huellas de bytes siguen siendo las reales
            txt = CIE.texto_fiel(open(destino, "rb").read())
            utf8 = txt is not None
            if not utf8:
                txt = open(destino, encoding="utf-8", errors="replace").read()
            ida = CIE.id_solicitud_en_auditoria(txt)
            otras = {s["id"]: s.get("estado") for s in st.get("solicitudes_auditoria") or []}
            hc = CIE.huella_contenido(txt)
            # una auditoría ya usada no puede acreditar una APROBACIÓN nueva; una respuesta que no aprueba (REPETIR según H2) puede repetir
            # el contenido de otra (un auditor que vuelve a encontrar lo mismo), porque no cierra nada
            aprobaria = self.veredicto_auditoria(txt) == "APROBADO"
            if not utf8:
                # (tercera revisión de la 4.8.1, W-3) el cierre lee auditoria.md en UTF-8 estricto: no se consume una respuesta que no lo es
                no_aceptada = "auditoria.md no es texto UTF-8 válido: se vuelve a guardar en UTF-8 y se relanza (no se ha consumido)"
            elif aprobaria and h in self.huellas_auditorias_usadas():
                no_aceptada = "auditoria.md es una auditoría ya usada (su huella SHA-256 es la de una respuesta anterior): no responde a la solicitud vigente"
            elif aprobaria and hc in self.contenidos_auditorias_usadas():
                no_aceptada = ("auditoria.md repite el contenido de una auditoría ya usada (solo cambian la línea de solicitud o el formato): "
                               "una respuesta nueva es una auditoría hecha de nuevo sobre el material vigente")
            elif ida is None:
                no_aceptada = "auditoria.md no tiene exactamente una línea «Solicitud de auditoría: <id>»: no consta a qué solicitud responde"
            elif ida != sol["id"]:
                no_aceptada = f"auditoria.md responde a la solicitud {ida} ({otras.get(ida, 'desconocida')}), no a la vigente {sol['id']}"
            else:
                # (4.9, R-V1) además del detector (contenido sin orden, función A), la huella fiel de la respuesta aceptada (función B):
                # contenido y orden íntegros salvo cierre_v2.TRANSFORMACIONES_INOCUAS; la vigencia del cierre solo acepta esta
                hf = CIE.huella_fiel(open(destino, "rb").read())
                sol.update(estado="respondida", respuesta_sha256=h, respuesta_contenido=hc, respuesta_fiel=hf, respondida=dt.datetime.now().astimezone().isoformat(timespec="seconds"))
                st["auditoria_respuesta"] = {"solicitud": sol["id"], "sha256": h, "contenido": hc, "fiel": hf, "material": sol.get("material")}
                CIE.anotar_auditorias(self.c, [h], [hc], f"respuesta a la solicitud {sol['id']}")
                st.setdefault("consumidos", {})["auditoria.md"] = os.path.getmtime(destino)  # compatibilidad: ya no decide nada en el paso 13
                st["esperando"] = None
                st["motivo_correccion"] = None
                self.log(f"auditoría consumida: respuesta a la solicitud {sol['id']} (SHA-256 {h[:12]}…)")
                self.guardar()
                return txt
        motivo = st.get("motivo_correccion") if st.get("esperando") == marca else None
        aviso = "; ".join(x for x in (motivo, f"auditoria.md presente NO aceptada: {no_aceptada}" if no_aceptada else None) if x)
        self.escribir_prompt(13, "verificacion", "auditoria.md", ["todo lo de la carpeta (sin los prompts de las fases)", "material_auditoria.json (el material que se audita)",
                                                                  f"solicitud_auditoria.json (la solicitud a la que se responde: {sol['id']})"], aviso or None)
        if st.get("esperando") != marca or "esperando_desde" not in st:
            st["esperando_desde"] = dt.datetime.now().timestamp()
        st["esperando"] = marca
        if no_aceptada:
            st["ultima_auditoria_no_aceptada"] = {"motivo": no_aceptada, "sha256": CIE.sha_archivo(destino), "solicitud_vigente": sol["id"]}
        self.guardar()
        raise Esperando(f"verificacion → auditoria.md (solicitud {sol['id']})" + (f"; {no_aceptada}" if no_aceptada else ""))

    def validar_esquema(self, archivo, esquema, paso, nombre, turno=None):
        """Valida la salida de un agente contra su esquema (Anexo D). Inválida → corrección al mismo agente; agotadas
        max_correcciones_esquema (2) → no_entregable (nunca se sigue con un JSON que no cumple el esquema). Devuelve
        None si es válida, "continuar" si se pidió corrección, o "fin" si terminó."""
        cmd = [PY, self.script("validar_esquema.py"), self.p(archivo), esquema] + (["--turno", str(turno)] if turno else []) + ["--salida", self.p(f"esquema_{archivo}.txt")]
        rc, out = self.run(cmd)
        if rc == 0:
            return None
        if rc != 1:
            return self.terminar("no_entregable", "fallo_de_implementacion", f"validar_esquema.py no pudo validar {archivo}: " + out[-300:], paso) or "fin"
        clave = f"esquema_{nombre}"
        self.st["intentos"][clave] = self.st["intentos"].get(clave, 0) + 1
        if self.st["intentos"][clave] > self.lim.get("max_correcciones_esquema", 2):
            self.terminar("no_entregable", "fallo_de_implementacion", f"{archivo} ({nombre}) no cumple su esquema tras {self.lim.get('max_correcciones_esquema', 2)} correcciones: " + out[-300:], paso,
                          que_hace_falta=f"revisar el prompt de {nombre} (esquema del Anexo D) · ver esquema_{archivo}.txt", desde=paso)
            return "fin"
        self.pedir_correccion(paso, nombre, archivo, f"{archivo} no cumple el esquema del Anexo D (ver esquema_{archivo}.txt): " + out[:600])
        self.log(f"esquema de {archivo} inválido: corrección {self.st['intentos'][clave]} a {nombre}")
        return "continuar"

    def correccion_formato(self, archivo, paso, nombre, motivo):
        """Defecto de formato de una salida de agente detectado después del esquema (claves de celdas, Observaciones, vocabulario):
        corrección al mismo agente con el contador de esquema (max_correcciones_esquema por agente); agotado → no_entregable."""
        clave = f"esquema_{nombre}"
        self.st["intentos"][clave] = self.st["intentos"].get(clave, 0) + 1
        if self.st["intentos"][clave] > self.lim.get("max_correcciones_esquema", 2):
            self.terminar("no_entregable", "fallo_de_implementacion", f"{archivo} ({nombre}) sigue fuera de formato tras {self.lim.get('max_correcciones_esquema', 2)} correcciones: {motivo[:300]}", paso,
                          que_hace_falta=f"revisar el prompt de {nombre} (Anexo A / Anexo D)", desde=paso)
            return "fin"
        self.st["paso"] = paso
        self.pedir_correccion(paso, nombre, archivo, motivo[:600])
        self.log(f"formato de {archivo}: corrección {self.st['intentos'][clave]} a {nombre}")
        return "continuar"

    def citas_fase(self, archivo, paso, nombre):
        """v2.1: comprueba las citas de una fase en cuanto llega su salida (su .md y todos los textos de su JSON), con páginas
        estrictas y principio↔página de Damodaran (verify_quotes_v2.py). Un fallo vuelve al mismo agente como corrección de
        formato: así se corrige en la fase que lo escribió, y no lo descubre la auditoría cuando ya no hay vuelta (prueba de
        variabilidad de Rational, 3-nov-2026). Devuelve None, "continuar" o "fin"."""
        base = archivo.rsplit(".", 1)[0]
        tmp = self.p(f"citas_{base}.md")
        try:
            d = json.load(open(self.p(archivo), encoding="utf-8"))
        except Exception:
            return None  # el esquema ya lo habría rechazado
        lineas = []

        def hojas(x, ruta):
            if isinstance(x, dict):
                for k, v in x.items():
                    hojas(v, f"{ruta}.{k}")
            elif isinstance(x, list):
                for i, v in enumerate(x):
                    hojas(v, f"{ruta}[{i}]")
            elif isinstance(x, str) and x.strip():
                lineas.append(f"- {ruta}: {x}")
        hojas(d, base)
        open(tmp, "w", encoding="utf-8").write("\n".join(lineas) + "\n")
        textos = [tmp] + ([self.p(base + ".md")] if os.path.exists(self.p(base + ".md")) else [])
        cmd = [PY, self.script("verify_quotes_v2.py"), "--corpus", self.cfg.get("kit_v1", {}).get("corpus_munger", ""), "--corpus", self.cfg.get("corpus", {}).get("damodaran", ""), "--paginas-estrictas"] + textos
        rc, out = self.run(cmd)
        open(self.p(f"citas_{base}.txt"), "w", encoding="utf-8").write(out)
        if rc == 0:
            return None
        malos = [l for l in out.splitlines() if l.startswith("  ")][:20]
        return self.correccion_formato(archivo, paso, nombre, f"citas de {archivo} o {base}.md que no superan verify_quotes_v2.py (cita literal, página o principio↔página; ver citas_{base}.txt): " + " | ".join(m.strip() for m in malos))

    def pedir_correccion(self, paso, nombre, salida, motivo):
        self.st["esperando"] = f"{paso}:{salida}"
        self.st["esperando_desde"] = dt.datetime.now().timestamp()
        self.st["motivo_correccion"] = motivo
        self.escribir_prompt(paso, nombre, salida, ["gramatica.md / motivo de la corrección"], motivo)
        self.guardar()

    def escribir_prompt(self, paso, nombre, salida, entradas, motivo=None):
        os.makedirs(self.p("prompts_generados"), exist_ok=True)
        plantilla = os.path.join(AQUI, "..", "prompts", f"{nombre}.md")
        texto = open(plantilla, encoding="utf-8").read() if os.path.exists(plantilla) else f"(prompt de {nombre}: pendiente de la pieza 4)"
        texto = texto.replace("{CARPETA}", self.c).replace("{EMPRESA}", self.E).replace("{MATERIAL_AUDITORIA}", str(self.st.get("material_auditoria") or "(sin fijar)"))
        pend = [s for s in self.st.get("solicitudes_auditoria") or [] if s.get("estado") == "pendiente"]
        texto = texto.replace("{SOLICITUD_AUDITORIA}", pend[-1]["id"] if pend else "(sin solicitud registrada)")
        texto = texto.replace("{RAIZ_CORPUS}", os.path.dirname(self.cfg.get("corpus", {}).get("damodaran", "") or os.path.join(AQUI, "..", "corpus", "x"))).replace("{RAIZ}", os.path.abspath(os.path.join(AQUI, "..")))
        raiz = os.path.abspath(os.path.join(AQUI, ".."))
        rutas = [f"carpeta de la empresa: {self.c}", f"raíz del personaje v2 (personaje_munger_v2.md, ANEXO_*.md, ENCARGO_personaje_v2.md, scripts/, esquema/): {raiz}",
                 f"corpus Munger (munger.md): {self.cfg.get('kit_v1', {}).get('corpus_munger', '')}", f"corpus Damodaran (damodaran.md, si existe): {self.cfg.get('corpus', {}).get('damodaran', '')}",
                 f"modelo y esfuerzo previstos (config_v2.json → modelos): {json.dumps(self.cfg.get('modelos', {}).get(nombre.replace('_turno1', '').replace('_turno2', ''), {}), ensure_ascii=False)}"]
        cab = f"# Paso {paso} · {nombre}\n\nEntradas (en {self.c}): " + ", ".join(entradas) + f"\n\nSalida esperada: {salida}\n\nRutas:\n" + "".join(f"- {r}\n" for r in rutas) + "\n"
        if motivo:
            cab += f"**CORRECCIÓN pedida por el pipeline:** {motivo}\n\n"
        open(self.p("prompts_generados", f"{paso:02d}_{nombre}.md"), "w", encoding="utf-8").write(cab + "---\n\n" + texto)
        open(self.p("ESPERANDO.md"), "w", encoding="utf-8").write(f"ESPERANDO al agente **{nombre}** (paso {paso}). " + (f"CORRECCIÓN: {motivo} " if motivo else "") + f"Entradas: {', '.join(entradas)}. Escribe **{salida}** en esta carpeta y vuelve a lanzar pipeline.py.\n")

    # ---------- pasos mecánicos ----------
    def escribir(self, fase_json, fase, libro_in, libro_out):
        cj = self.p(f"celdas_{fase}.json")
        rc, out = self.run([PY, self.script("fase_a_celdas.py"), self.p(fase_json), fase, cj])
        if rc != 0:
            return 11, out  # 11 = claves u Observaciones de la fase ausentes (defecto del agente, no del libro)
        return self.run([PY, self.script("escribir_v63.py"), libro_in, libro_out, "--celdas", cj, "--verificar", self.cfg["plantilla"]["referencia"]])

    def bloqueo_de_lectura(self):
        """Tras la fase B, precio.json con `sin_lectura` significa que la hoja bloquea el valor o la lectura del precio
        (Motor!B252/B253/B254). Un bloqueo nunca se convierte en aviso: según su causa (reglas del Motor) termina en
        pendiente_de_datos (DATOS INVÁLIDOS), modelo_no_aplicable solo si la fase A lo declaró, o no_entregable."""
        pr = json.load(open(self.p("precio.json"), encoding="utf-8")) if os.path.exists(self.p("precio.json")) else {}
        if "sin_lectura" not in pr:
            return False
        res = json.load(open(self.p("resultados.json"), encoding="utf-8")) if os.path.exists(self.p("resultados.json")) else {}
        reglas = [r for r in (res.get("reglas_motor") or []) if r.get("aplica") and r.get("resultado") in ("DATOS INVÁLIDOS", "MODELO NO APLICABLE", "INCOMPLETO") and r.get("nivel") in (1, 2)]
        detalle = f"la hoja bloquea la lectura del precio tras la fase B: {pr['sin_lectura']} · reglas: " + "; ".join(f"{r.get('id')} {r.get('resultado')} ({r.get('causa', '')})" for r in reglas)[:400]
        if any(r.get("resultado") == "DATOS INVÁLIDOS" for r in reglas):
            self.terminar("pendiente_de_datos", "falta_de_datos", detalle, self.st["paso"], que_hace_falta="corregir el dato inválido en fase1_v63.json o en la etapa 1", desde=2)
        else:
            self.terminar("no_entregable", "fallo_de_implementacion", detalle, self.st["paso"], desde=8)
        return True

    def motor_a_f1(self, libro_recalculado, paso):
        """(4.15, F1-IMPL) Motor A con el perímetro F1 (decisiones del 17-nov-2026): con el motor A, en los expedientes que lo exigen
        (motor_a_f1.exigido: declaración motor_a_f1.json o expediente de la 4.15 con entrada_efectiva.json), evalúa las guardas V-F1a…m y
        K3 sobre el libro recalculado y escribe motor_a_f1_resultado.json/.md. Si una guarda BLOQUEA, el resultado del motor A no se usa
        para una conclusión: termina en pendiente_de_datos (falta de datos o de decisión) o en no_entregable (límite del modelo o fallo
        de implementación), con el diagnóstico F1 rotulado. Devuelve True si terminó."""
        import motor_a_f1 as F1
        if self.st.get("motor") != "A" or not F1.exigido(self.c):
            return False
        rc, out = self.run([PY, self.script("motor_a_f1.py"), "evaluar", self.c, "--libro", libro_recalculado], ok=(0, 3, 4, 5))
        r = None
        try:
            r = json.load(open(self.p(F1.RESULTADO), encoding="utf-8"))
        except (OSError, ValueError):
            pass
        if rc not in (0, 3, 4, 5) or r is None:
            self.terminar("no_entregable", "fallo_de_implementacion", "motor_a_f1.py: " + out[-300:], paso, desde=paso)
            return True
        self.st["motor_a_f1"] = {"paso": paso, "bloquea": r.get("bloquea"), "estado_propuesto": r.get("estado_propuesto"),
                                 "declaracion_sha256": r.get("declaracion_sha256"), "libro_sha256": r.get("libro_sha256")}
        self.log("motor A · F1: " + str(r.get("rotulo"))[:300])
        if rc == 0:
            return False
        bl = "; ".join(f"{g['id']} {g.get('efecto')}: {str(g.get('detalle'))[:120]}" for g in r.get("guardas") or [] if g.get("salta") and g.get("severidad") == "BLOQUEA")[:900]
        detalle = f"motor A · F1 (motor_a_f1_resultado.md): el resultado del motor A no se usa para una conclusión · {bl}"
        if rc == 3:
            self.terminar("pendiente_de_datos", "falta_de_datos", detalle, paso, comprobacion="F1", categoria="F1",
                          que_hace_falta="la declaración F1 (motor_a_f1.json) y los datos o decisiones que piden las guardas (R: M1, M2, M6; compras; transición)", desde=2)
        else:
            self.terminar("no_entregable", "limite_del_modelo" if rc == 4 else "fallo_de_implementacion", detalle, paso, comprobacion="F1",
                          categoria="límite del modelo" if rc == 4 else None,
                          que_hace_falta="ver motor_a_f1_resultado.md: un límite declarado del motor A F1 (p. ej. el libro V6.3 calcula A0) o una decisión pendiente", desde=2)
        return True

    def recalc_leer_precio(self, libro):
        rc, out = self.run(["bash", self.script("recalc.sh"), libro, self.p("recalc"), self.perfil])
        if rc != 0:
            return False, "recálculo: " + out[-300:]
        rec = self.p("recalc", os.path.basename(libro))
        rc, out = self.run([PY, self.script("leer_resultados.py"), rec, self.p("resultados.json"), "--exigir-recalculo-forzado"])
        if rc != 0:
            return False, "lectura/recálculo no forzado: " + out[-300:]
        if os.path.exists(self.p("precio.json")):
            os.remove(self.p("precio.json"))  # nunca se lee una escalera de una pasada anterior
        rc, out = self.run([PY, self.script("precio_de_si.py"), self.p("resultados.json"), self.p("precio.json"), "--k", str(self.cfg.get("convenciones", {}).get("k_asimetria", 3))])
        if rc not in (0, 5) or not os.path.exists(self.p("precio.json")):
            return False, f"precio_de_si.py terminó con código {rc}: " + out[-300:]
        return True, rec

    # ---------- flujo ----------
    def correr(self, hasta=14):
        st = self.st
        libro_base, libro_datos, libro_ev = self.p(f"{self.E}_v63_base.xlsx"), self.p(f"{self.E}_v63_datos.xlsx"), self.p(f"{self.E}_v63_evaluada.xlsx")
        while st["paso"] <= hasta and st["estado_analisis"] is None:
            paso = st["paso"]
            if paso == 0:
                rc, out = self.run(["bash", self.script("comprobar_entorno.sh")])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "entorno incompleto: " + out[-300:], 0)
            elif paso == 1:
                ev = [f for f in os.listdir(self.p("etapa1")) if f.endswith(".xlsx")] if os.path.isdir(self.p("etapa1")) else []
                if not ev:
                    return self.terminar("pendiente_de_datos", "falta_de_datos", "falta etapa1/<E>_evaluada.xlsx (V5.3 decidida por el v1, D2)", 1, que_hace_falta="José Luis: la V5.3 evaluada de la etapa 1 (S-1)", desde=1)
                rc, out = self.run([PY, self.script("migrar_v53_a_v63.py"), self.p("etapa1", ev[0]), self.cfg["plantilla"]["archivo"], libro_base])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "migración: " + out[-300:], 1)
            elif paso == 2:
                if not os.path.exists(self.p("fase1_v63.json")):
                    # pieza 7: si hay informes en texto/, la Historia y los metadatos se construyen con agentes (fase1_historia.py)
                    if not glob.glob(self.p("texto", "*.txt")):
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "falta fase1_v63.json y no hay informes en texto/ para construirlo", 2, que_hace_falta="José Luis: informes anuales de 10 años (PDF → texto/) o fase1_v63.json (S-2)", desde=2)
                    rc, out = self.run([PY, self.script("fase1_historia.py"), "preparar", self.c, self.E])
                    if rc == 10:
                        self.st["esperando"] = "2:fase1"
                        self.guardar()
                        open(self.p("ESPERANDO.md"), "w", encoding="utf-8").write(open(self.p("ESPERANDO_FASE1.md"), encoding="utf-8").read())
                        raise Esperando("fase 1 · Historia por año y metadatos (ver ESPERANDO.md)")
                    if rc != 0:
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "fase1_historia preparar: " + out[-300:], 2, que_hace_falta="informes anuales con estados financieros en texto/", desde=2)
                    rc, out = self.run([PY, self.script("fase1_historia.py"), "construir", self.c])
                    if rc != 0:
                        return self.terminar("pendiente_de_datos", "falta_de_datos", "fase1_historia construir: " + out[-400:], 2, que_hace_falta="ver historia_revision.md (datos esenciales ausentes o salidas inválidas)", desde=2)
                    self.st["esperando"] = None
                # (4.15, C48 de Elis; segunda revisión independiente, N7) modo de la entrada efectiva del expediente (entrada_efectiva.json,
                # que cambiar_base.py escribe en todo expediente nuevo, por defecto «estricta»); un archivo ilegible detiene el paso
                try:
                    _modo, _origen_modo = modo_entrada_efectiva(self.c)
                except ValueError as ex:
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"entrada_efectiva.json: {ex}", 2)
                _estricta = _modo == "estricta"
                self.st["entrada_efectiva"] = {"modo": _modo, "declarado_en": _origen_modo}  # (T5) queda en estado_pipeline.json
                rc, out = self.run([PY, self.script("rellenar_fase1_v63.py"), libro_base, self.p("fase1_v63.json"), libro_datos] + (["--estricta"] if _estricta else []))
                if rc != 0:
                    return self.terminar("no_entregable" if rc == 1 else "pendiente_de_datos", "fallo_de_implementacion" if rc == 1 else "falta_de_datos", "rellenar_fase1: " + out[-300:], 2)
                if self.v64:
                    # (4.11) la configuración económica explícita del expediente entra en el libro de datos, antes del primer recálculo
                    # y de las fases (que no pueden cambiarla: no está en su lista blanca); el verificador de la V6.4 la reconoce
                    rc, out = self.run([PY, self.script("configuracion_economica.py"), "aplicar", libro_datos, libro_datos + ".cfg.xlsx",
                                        self.p(SEL.CONF), "--config", self.cfg["_ruta_config"]])
                    if rc != 0:
                        if os.path.exists(libro_datos + ".cfg.xlsx"):
                            os.remove(libro_datos + ".cfg.xlsx")
                        return self.terminar("no_entregable", "fallo_de_implementacion", "configuración económica V6.4: " + out[-300:], 2)
                    os.replace(libro_datos + ".cfg.xlsx", libro_datos)
                    st["configuracion_economica_sha256"] = CIE._sha(self.p(SEL.CONF))
            elif paso == 3:
                rc, out = self.run([PY, self.script("comprobar_entrada_v63.py"), libro_datos, self.c])
                if rc == 1 and not os.path.exists(self.p("entrada_v63.json")):
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada_v63.py terminó con 1 sin escribir entrada_v63.json: " + out[-300:], 3)
                if rc == 1:
                    ent = json.load(open(self.p("entrada_v63.json"), encoding="utf-8"))
                    return self.terminar("pendiente_de_datos", "falta_de_datos", "bloqueante en la entrada: " + "; ".join(f"{x['dato']}: {x.get('que', '')}" for x in ent["bloqueantes"])[:600], 3,
                                         que_hace_falta="; ".join(f"{x['dato']} ← {x.get('origen_esperado', '')}" for x in ent["bloqueantes"])[:600], desde=2)
                if rc not in (0,):
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada: " + out[-300:], 3)
            elif paso == 4:
                rc, out = self.run([PY, self.script("volcar_datos_v63.py"), self.p("recalc", os.path.basename(libro_datos)), self.c])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "volcar_datos: " + out[-300:], 4)
            elif paso == 5:
                self.agente(5, "extraccion_v63", "extracto_v63.md", ["texto/", "extracto.md (etapa1)", "datos_v63.md"])
            elif paso == 6:
                self.agente(6, "fase_a", "fase_a.json", ["datos_v63.md", "extracto.md", "extracto_v63.md", "personaje_munger_v2.md"], alternativas=["fase_a.intento2.json"] if st["intentos"]["vueltas_b_a_a"] else [])
                v = self.validar_esquema("fase_a.json", "fase_a", 6, "fase_a")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                v = self.citas_fase("fase_a.json", 6, "fase_a")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                fa = json.load(open(self.p("fase_a.json"), encoding="utf-8"))
                motor = {"Sí": "A", "No · financiación cambia mucho": "B", "No · banco o aseguradora": "C"}.get((fa.get("celdas") or {}).get("C62"))
                st["motor"] = motor
                c62 = (fa.get("celdas") or {}).get("C62")
                if motor is None and c62 != "No · este tipo de empresa requiere otro método":
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"Análisis!C62 = {c62!r} fuera del vocabulario (el esquema debía rechazarlo)", 6)
                if (fa.get("limite_del_modelo") or {}).get("aplica") or motor is None:
                    rc, out = self.escribir("fase_a.json", "A", libro_datos, libro_ev)
                    if rc != 0:
                        return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase A: " + out[-300:], 6)
                    rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A"])
                    if rc != 0:
                        return self.terminar("no_entregable", "fallo_de_implementacion", "celdas de la fase A (límite del modelo): " + out[-400:], 6)
                    return self.terminar("modelo_no_aplicable", "limite_del_modelo", (fa.get("limite_del_modelo") or {}).get("porque") or "C62 = otro método", 6, comprobacion=(fa.get("limite_del_modelo") or {}).get("cual"), categoria="límite del modelo")
            elif paso == 7:
                rc, out = self.escribir("fase_a.json", "A", libro_datos, libro_ev)
                if rc == 11:  # claves u Observaciones de la fase A que faltan: es el agente quien corrige (D17), no un fallo mecánico
                    v = self.correccion_formato("fase_a.json", 6, "fase_a", "celdas u Observaciones de la fase A ausentes o mal nombradas: " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase A: " + out[-300:], 7)
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A"])
                if rc != 0:
                    v = self.correccion_formato("fase_a.json", 6, "fase_a", "celdas de la fase A fuera de regla (comprobar_celdas_v2): " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                rc, out = self.run([PY, self.script("comprobar_entrada_v63.py"), libro_ev, self.c, "--motor", st["motor"]])
                if rc == 1 and "Traceback" in out:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "comprobar_entrada_v63.py falló: " + out[-300:], 7)
                if rc == 1:
                    return self.terminar("pendiente_de_datos", "falta_de_datos", f"el motor {st['motor']} elegido por la fase A no es calculable: " + out[-300:], 7, que_hace_falta="datos de Historia que exige el motor (Contrato_de_relleno_V6.3.csv)", desde=2)
                if rc == 4:
                    # (4.11, revisión interna H3) el motor es calculable con los datos, pero la configuración experimental V6.4 solo cubre el
                    # motor B: es un límite del modelo experimental, no una falta de datos; la elección de la fase A no se fuerza
                    return self.terminar("no_entregable", "limite_del_modelo",
                                         f"la configuración experimental V6.4 solo cubre el motor B y la fase A eligió el motor {st['motor']} por los criterios del personaje: la valoración experimental no se aplica a ese motor",
                                         7, que_hace_falta="ejecutar el expediente con configuracion_economica.json en modo Heredado (V6.3 efectiva) o con la V6.3 en un expediente nuevo; la elección del motor no se cambia para encajar en la plantilla", desde=2)
                if self.motor_a_f1(self.p("recalc", os.path.basename(libro_ev)), 7):  # (4.15, F1-IMPL) guardas F1 del motor A antes de la fase B
                    return
                rc, out = self.run([PY, self.script("volcar_datos_v63.py"), self.p("recalc", os.path.basename(libro_ev)), self.c, "--referencias-mecanicas"])
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "referencias mecánicas: " + out[-300:], 7)
            elif paso == 8:
                n = st["intentos"]["fase_b"]
                if st["intentos"]["vueltas_b_a_a"] and not st.get("esperando") and not self.sim and st.get("consumidos", {}).get("fase_b.json"):
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"la fase A corrigió el motor o el caso especial tras un límite del modelo (vuelta B→A única): el motor es ahora {st.get('motor')}; traduce de nuevo las palancas con las referencias mecánicas nuevas")
                self.agente(8, "fase_b", "fase_b.json", ["fase_a.json", "datos_v63.md", "referencias_mecanicas.json", "extracto_v63.md", "gramatica.md (si hay corrección)"],
                            alternativas=[f"fase_b.intento{n + 1}.json"] if n else [])
                v = self.validar_esquema("fase_b.json", "fase_b", 8, "fase_b")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                v = self.citas_fase("fase_b.json", 8, "fase_b")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--antes-de-recalculo"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 8)
                fb = json.load(open(self.p("fase_b.json"), encoding="utf-8"))
                if (fb.get("limite_del_modelo") or {}).get("aplica") and rc != 3:
                    # la fase B señala un límite del modelo al traducir (Anexo D §D.4): misma vuelta a la fase A que el código 3
                    rc, out = 3, "límite del modelo declarado por la fase B: " + str((fb.get("limite_del_modelo") or {}).get("porque"))[:300]
                if rc == 3:
                    if st["intentos"]["vueltas_b_a_a"] >= self.lim.get("max_vueltas_fase_b_a_a_por_limite_del_modelo", 1):
                        # nadie declaró el límite (la fase A tuvo su vuelta y no corrigió el motor ni lo declaró): no es un estado legítimo, es un fallo
                        return self.terminar("no_entregable", "fallo_de_implementacion", "límite del modelo (código 3) que la fase A no resolvió ni declaró en su vuelta: " + out[-200:], 8, categoria="límite del modelo", desde=6)
                    st["intentos"]["vueltas_b_a_a"] += 1
                    st["paso"] = 6
                    self.pedir_correccion(6, "fase_a", "fase_a.json", "gramática código 3 (límite del modelo): la fase A tiene que corregir el motor o declarar el límite (una vuelta)")
                    self.log("gramática código 3: vuelve a la fase A con la pregunta concreta (una vez)")
                    continue
                if rc in (1, 2):
                    st["intentos"]["fase_b"] += 1
                    if st["intentos"]["fase_b"] > self.lim.get("max_correcciones_fase_b", 2):
                        g = json.load(open(self.p("gramatica.json"), encoding="utf-8")) if os.path.exists(self.p("gramatica.json")) else {"hallazgos": []}
                        h = next((x for x in g["hallazgos"] if x["categoria"] == "error"), next((x for x in g["hallazgos"] if x["categoria"] == "desviación" and not x["justificada"]), {}))
                        return self.terminar("no_entregable", "fallo_de_implementacion", f"gramática código {rc} tras {self.lim.get('max_correcciones_fase_b', 2)} correcciones de la fase B: {h.get('id')} {h.get('detalle', '')[:200]}", 8,
                                             comprobacion=h.get("id"), categoria=h.get("categoria"), que_hace_falta="revisar el prompt de la fase B en la regla indicada (nunca se aprueba por agotamiento)", desde=8)
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"gramática código {rc}: ver gramatica.md (corrección {st['intentos']['fase_b']})")
                    self.log(f"gramática código {rc}: corrección {st['intentos']['fase_b']} de la fase B (gramatica.md)")
                    continue
            elif paso == 9:
                rc, out = self.escribir("fase_b.json", "B", libro_ev, libro_ev + ".tmp.xlsx")
                if rc == 11:
                    v = self.correccion_formato("fase_b.json", 8, "fase_b", "celdas u Observaciones de la fase B ausentes o mal nombradas: " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase B: " + out[-300:], 9)
                os.replace(libro_ev + ".tmp.xlsx", libro_ev)
                st["fase_b_escrita"] = True
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A,B"])
                if rc != 0:
                    v = self.correccion_formato("fase_b.json", 8, "fase_b", "celdas de la fase B fuera de regla (comprobar_celdas_v2): " + out[-400:])
                    if v == "continuar":
                        continue
                    return
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 9)
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--tras-recalculo"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 9)
                if rc == 3:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "límite del modelo detectado tras el recálculo (debió detectarse antes del recálculo): " + out[-200:], 9, categoria="límite del modelo", desde=6)
                if rc < 2 and self.bloqueo_de_lectura():
                    return
                if rc >= 2:
                    g = json.load(open(self.p("gramatica.json"), encoding="utf-8")) if os.path.exists(self.p("gramatica.json")) else {"hallazgos": []}
                    solo_g19 = all(x["id"] == "G19" for x in g["hallazgos"] if x["categoria"] == "error")
                    if solo_g19:
                        # G19 (valores por acción desordenados): vuelta a la fase B UNA vez; si persiste, no_entregable (§B.3)
                        st["intentos"]["vueltas_g19"] = st["intentos"].get("vueltas_g19", 0) + 1
                        if st["intentos"]["vueltas_g19"] > 1:
                            return self.terminar("no_entregable", "fallo_de_implementacion", "G19 persiste tras su única vuelta a la fase B: " + out[-200:], 9, comprobacion="G19", categoria="error", desde=8)
                    else:
                        st["intentos"]["fase_b"] += 1
                        if st["intentos"]["fase_b"] > self.lim.get("max_correcciones_fase_b", 2):
                            return self.terminar("no_entregable", "fallo_de_implementacion", "error de gramática tras el recálculo que persiste: " + out[-200:], 9, categoria="error", desde=8)
                    st["paso"] = 8
                    self.pedir_correccion(8, "fase_b", "fase_b.json", f"gramática tras el recálculo código {rc}: ver gramatica.md (" + ("vuelta única por G19" if solo_g19 else f"corrección {st['intentos']['fase_b']}") + ")")
                    self.log(f"gramática tras recálculo código {rc}: vuelve a la fase B")
                    continue
            elif paso == 10:
                n = st["intentos"]["fase_c"]
                if st.get("turno_c") != 2:
                    if st["intentos"]["vueltas_c_a_b"] and not st.get("esperando") and not self.sim:
                        # la única vuelta C→B ya se consumió: el turno 1 nuevo tiene que saberlo (un segundo revisar_palancas termina en no_entregable)
                        self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", "la fase B ya revisó las palancas en la única vuelta C→B admitida (§4.5): el libro está recalculado con las palancas nuevas; otro revisar_palancas termina en no_entregable")
                    elif st.get("motivo_correccion_c") and not st.get("esperando") and not self.sim:
                        # (4.12, cierre de bloqueo de Vidrala) un motivo pendiente sin petición registrada (el cambio del protocolo del objetivo,
                        # que se detecta al reaplicar la configuración) llega ya al prompt del turno 1 y a ESPERANDO.md; antes solo llegaba al turno 2
                        self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", st["motivo_correccion_c"])
                    entradas_c = ["fase_a.json", "fase_b.json", "resultados.json", "precio.json", "gramatica.md", "datos_ausentes.json", "datos_v63.md", "extractos"]
                    if self.v64 and SEL.experimental(self.c):
                        # (4.11) materialidad mecánica de cada parámetro experimental y estructuras compatibles, sobre COPIAS del libro evaluado
                        v = self.variantes_v64(libro_ev)
                        if v:
                            return self.terminar("no_entregable", "fallo_de_implementacion", "variantes de la configuración V6.4: " + v, 10)
                        entradas_c += ["configuracion_economica.json", "configuracion_v64_variantes.md"]
                        # (4.14, encargo de cierre §5) contrato del juicio propio sobre el objetivo: lo fija el PIPELINE al generar el prompt de
                        # la fase C (no un campo del agente), con el contraste mecánico por parámetro que la fase C copia en juicio_objetivo
                        import objetivo_v64 as OBJ
                        if st.get("contrato_juicio_objetivo") != OBJ.FORMATO_JUICIO_OBJETIVO:
                            st["contrato_juicio_objetivo"] = OBJ.FORMATO_JUICIO_OBJETIVO
                            self.log(f"contrato del juicio sobre el objetivo {OBJ.FORMATO_JUICIO_OBJETIVO} (encargo de cierre §5)")
                            self.guardar()
                        OBJ.escribir_contraste_objetivo(self.c)
                        entradas_c += ["contraste_objetivo_v64.md"]
                    self.agente(10, "fase_c_turno1", "fase_c.json", entradas_c,
                                alternativas=[f"fase_c.turno1.intento{n + 1}.json"] if n else ["fase_c.turno1.json"])
                    v = self.validar_esquema("fase_c.json", "fase_c", 10, "fase_c_turno1", turno=1)
                    if v == "continuar":
                        continue
                    if v == "fin":
                        return
                    v = self.citas_fase("fase_c.json", 10, "fase_c_turno1")
                    if v == "continuar":
                        continue
                    if v == "fin":
                        return
                    fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                    if fc.get("revisar_palancas"):
                        if st["intentos"]["vueltas_c_a_b"] >= self.lim.get("max_vueltas_fase_c_a_b", 1):
                            return self.terminar("no_entregable", "fallo_de_implementacion", "la fase C pide revisar palancas por segunda vez (máximo una vuelta)", 10, desde=8)
                        st["intentos"]["vueltas_c_a_b"] += 1
                        st["paso"] = 8
                        self.pedir_correccion(8, "fase_b", "fase_b.json", "la fase C pide revisar palancas: " + str(fc.get("instrucciones_revision"))[:400])
                        self.log("fase C pide revisar_palancas: vuelve a la fase B una sola vez")
                        continue
                    if (fc.get("limite_del_modelo") or {}).get("aplica"):
                        fin = self.limite_declarado_por_c(fc, libro_ev)
                        if fin == "continuar":
                            continue
                        return
                    fm = fc.get("fundamento_material") or {}
                    rda = fc.get("revision_datos_ausentes") or {}
                    da = json.load(open(self.p("datos_ausentes.json"), encoding="utf-8")) if os.path.exists(self.p("datos_ausentes.json")) else []
                    revisados = {x.get("dato") for x in (rda.get("revisados") or [])}
                    sin_revisar = [x["dato"] for x in da if x["dato"] not in revisados]
                    if sin_revisar:
                        if self.correccion_c("revisión de datos ausentes incompleta (S-19): faltan " + ", ".join(sin_revisar)[:300], 10) == "continuar":
                            continue
                        return
                    if (fm.get("comprobacion_conjunta") or {}).get("procede") and not rda.get("alguno_material"):
                        if os.path.exists(self.p("comprobacion_conjunta.json")):
                            os.remove(self.p("comprobacion_conjunta.json"))  # nunca se lee la de una pasada anterior
                        rc, out = self.run([PY, self.script("comprobacion_conjunta.py"), self.c, libro_ev])
                        if rc == 3:
                            # combinación mal formada por el agente (celda ajena, de la fase C, valor no numérico): corrección a la fase C (D17), no fallo mecánico
                            if self.correccion_c("combinación de la comprobación conjunta mal formada: " + out[-300:], 10) == "continuar":
                                continue
                            return
                        if rc != 0:
                            return self.terminar("no_entregable", "fallo_de_implementacion", "comprobación conjunta: " + out[-300:], 10)
                if st.get("turno_c") != 2:
                    st["turno_c"] = 2
                    pendiente = st.get("motivo_correccion_c")
                    self.pedir_correccion(10, "fase_c_turno2", "fase_c.json", "segundo turno de la fase C: lee comprobacion_conjunta.json (si existe) y cierra fase_c.json (turno 2)" + (f" · CORRECCIÓN PENDIENTE que motivó esta pasada: {pendiente}" if pendiente else ""))
                self.agente(10, "fase_c_turno2", "fase_c.json", ["fase_c.json (turno 1)", "comprobacion_conjunta.json (si existe)"],
                            alternativas=[f"fase_c.turno2.intento{n + 1}.json"] if n else ["fase_c.turno2.json"])
                v = self.validar_esquema("fase_c.json", "fase_c", 10, "fase_c_turno2", turno=2)
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                v = self.citas_fase("fase_c.json", 10, "fase_c_turno2")
                if v == "continuar":
                    continue
                if v == "fin":
                    return
                st["turno_c"] = None
                st["estado_pendiente"] = None
                st["estado_analisis_fase_c"] = None
                st["motivo_correccion_c"] = None
                fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                if (fc.get("limite_del_modelo") or {}).get("aplica"):
                    # límite declarado en el segundo turno: mismo tratamiento que en el primero (no se escriben las 16 celdas ni hay escalera)
                    fin = self.limite_declarado_por_c(fc, libro_ev)
                    if fin == "continuar":
                        continue
                    return
                err = self.coherencia_fase_c(fc)
                if err:
                    if self.correccion_c("fase C incoherente: " + err, 10) == "continuar":
                        continue
                    return
                fin_obj = self.objetivo_sin_protocolo(fc)
                if fin_obj:
                    # (4.12 §4) el objetivo depende de hipótesis sin fundamento suficiente y la configuración no declara el protocolo: no se
                    # elige ninguno en silencio ni se emite un objetivo oficial; la fase C no se escribe en el libro y nada se entrega
                    return self.terminar("no_entregable", "limite_del_modelo", fin_obj[0], 10, que_hace_falta=fin_obj[1], desde=10)
                rc, out = self.escribir("fase_c.json", "C", libro_ev, libro_ev + ".tmp.xlsx")
                if rc == 11:
                    if self.correccion_c("celdas u Observaciones de la fase C ausentes o mal nombradas: " + out[-400:], 10) == "continuar":
                        continue
                    return
                if rc != 0:
                    return self.terminar("no_entregable", "fallo_de_implementacion", "escritura de la fase C: " + out[-300:], 10)
                os.replace(libro_ev + ".tmp.xlsx", libro_ev)
                st["fase_c_escrita"] = True
                rc, out = self.run([PY, self.script("comprobar_celdas_v2.py"), libro_ev, libro_datos, "--fases", "A,B,C"])
                if rc != 0:
                    if self.correccion_c("celdas de la fase C: " + out[-400:], 10) == "continuar":
                        continue
                    return
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 10)
                if self.bloqueo_de_lectura():
                    return
                rc, out = self.run([PY, self.script("comprobar_gramatica.py"), self.c, "--tras-recalculo", "--con-fase-c"])
                if rc not in (0, 1, 2, 3):
                    return self.terminar("no_entregable", "fallo_de_implementacion", f"comprobar_gramatica.py terminó con código {rc}: " + out[-300:], 10)
                if rc >= 1:
                    if self.correccion_c(f"gramática código {rc} tras la fase C (toda desviación tiene que estar justificada; ningún error): " + out[-200:], 10) == "continuar":
                        continue
                    return
                st["estado_analisis_fase_c"] = fc.get("estado_analisis")
            elif paso == 11:
                est = st.get("estado_analisis_fase_c") or "concluido"
                if est == "concluido":
                    for f in ("diagnostico.md", "diagnostico.json"):
                        if os.path.exists(self.p(f)):
                            os.replace(self.p(f), self.p(f + ".anterior"))
                    st["estado_pendiente"] = None
                if est != "concluido":
                    tipo = {"pendiente_de_investigacion": "incertidumbre_no_acotada", "pendiente_de_datos": "falta_de_datos", "modelo_no_aplicable": "limite_del_modelo"}[est]
                    fc = json.load(open(self.p("fase_c.json"), encoding="utf-8"))
                    fm = fc.get("fundamento_material") or {}
                    det = fm.get("hipotesis_que_mas_condiciona") or ""
                    que_falta, desde = (fm.get("que_lo_resolveria") or det or ""), "8"
                    ob = (fc.get("configuracion_v64") or {}).get("objetivo") or {} if self.v64 and SEL.experimental(self.c) else {}
                    if est == "pendiente_de_datos" and self.bloqueo_del_objetivo_v64(fc) and not (fc.get("revision_datos_ausentes") or {}).get("alguno_material"):
                        # (4.12 §4) protocolo experimental de bloqueo del objetivo: lo que falta es la información que fundaría las hipótesis
                        det = ("objetivo bloqueado (protocolo experimental bloqueo_del_objetivo; ensayo, no adopción): lo condicionan "
                               + ", ".join(ob.get("hipotesis_que_condicionan") or []) + f". {ob.get('motivo') or ''}")
                        que_falta = "; ".join(str(i) for i in ob.get("informacion_no_disponible") or [])
                        desde = "8"  # información nueva (documentos): desde la extracción, como pendiente_de_investigacion
                    elif est == "pendiente_de_datos":
                        materiales = [x for x in (fc.get("revision_datos_ausentes") or {}).get("revisados", []) if x.get("material_para_conclusion_favorable")]
                        det = "; ".join(f"{x.get('dato')}: {x.get('porque', '')}" for x in materiales)
                        que_falta = "; ".join(f"{x.get('dato')} ← {x.get('que_falta') or 'dato ausente'} (afecta a: {x.get('conclusion_afectada', '')})" for x in materiales)
                        desde = "2"  # los datos entran por fase1_v63.json / etapa 1: se reanuda desde el relleno de la fase 1
                    elif est == "pendiente_de_investigacion" and ob.get("origen_del_bloqueo") == "accion_no_sostenida_en_el_ambito":
                        # (4.12 §4) presentación condicionada sin acción sostenida en el ámbito calculado
                        det = ("acción no sostenida en el ámbito calculado (protocolo experimental objetivo_condicionado; ensayo, no adopción): "
                               + f"{ob.get('motivo') or ''} · lo condicionan " + ", ".join(ob.get("hipotesis_que_condicionan") or []))
                        que_falta = "; ".join(str(i) for i in ob.get("informacion_no_disponible") or []) or que_falta
                    st["estado_analisis"] = est
                    self.guardar()
                    self.run([PY, self.script("diagnostico.py"), self.c, "--estado", est, "--tipo", tipo, "--detalle", (det or est)[:500], "--paso", "10",
                              "--que-hace-falta", que_falta[:500], "--desde-paso", desde, "--quien", "José Luis (datos o documentos) / Claude Code"])
                    st["estado_analisis"] = None  # sigue hasta el paso 14 con las salidas
                    st["estado_pendiente"] = est
                # material PROVISIONAL para la auditoría (reparación del cierre, 4.6): la salida oficial no confirma el estado antes de
                # una auditoría APROBADO del material vigente; una salida oficial anterior no convive con un material nuevo sin auditar
                # (4.6.1) se archivan con su registro de retirada, la fila del resumen y el historial, no se renombran
                CIE.archivar_salidas(self.c, "nuevo material provisional en el paso 11: la salida oficial anterior queda como antecedente", CIE.ruta_resumen(self.c, self.cfg), self.st)
                self.run([PY, self.script("ficha.py"), self.c, "--estado", st.get("estado_pendiente") or "concluido", "--provisional"])
                self.run([PY, self.script("informe.py"), self.c, "--provisional"])
            elif paso == 12:
                if self.v64:
                    # (4.11) la configuración del libro evaluado tiene que ser la de configuracion_economica.json antes de fijar el material
                    distintas = self.configuracion_en_libros_distinta(self.p(SEL.CONF))
                    if distintas:
                        self.st["configuracion_economica_sha256"] = "distinta en los libros"
                        m_re = self.reaplicar_configuracion()
                        if m_re:
                            return self.terminar("no_entregable", "fallo_de_implementacion", m_re, 12, desde=2)
                        continue
                # se verifica siempre sobre un recálculo del libro tal como está ahora (al reanudar con --desde, resultados.json
                # y recalc/ podían ser de una pasada anterior: visto con Vidrala, 3-nov-2026)
                ok, rec = self.recalc_leer_precio(libro_ev)
                if not ok:
                    return self.terminar("no_entregable", "fallo_de_implementacion", rec, 12)
                if self.motor_a_f1(rec, 12):  # (4.15, F1-IMPL) de nuevo con las palancas finales (V-F1k numérico, flujos y K3)
                    return
                if self.v64 and SEL.experimental(self.c):
                    # (4.11, revisión interna H10) las variantes que evaluó la fase C tienen que corresponder a la valoración final: la
                    # variante «activa» es el libro evaluado con la configuración del expediente, así que da el precio.json de este recálculo
                    m_var = self.variantes_corresponden()
                    if m_var:
                        return self.terminar("no_entregable", "fallo_de_implementacion", m_var, 12, desde=10,
                                             que_hace_falta="recalcular las variantes (paso 10) y que la fase C las evalúe de nuevo")
                if self.v64:
                    # (4.12 §5) cadena de trazabilidad fuente → … → conclusión del libro final (V6.4; en la V6.3 se puede ejecutar a mano):
                    # no decide nada; sus avisos van al material de la auditoría
                    rc_t, out_t = self.run([PY, self.script("trazabilidad_v64.py"), self.c, libro_ev])
                    if rc_t != 0:
                        return self.terminar("no_entregable", "fallo_de_implementacion", "trazabilidad_v64.py: " + out_t[-300:], 12)
                rc, out = self.run(["bash", self.script("verificar_todo.sh"), self.c, libro_ev, libro_datos])
                if rc != 0:
                    fallos = [l.strip() for l in out.splitlines() if l.strip().startswith("FAIL")]
                    return self.terminar("no_entregable", "fallo_de_implementacion", "verificar_todo.sh con FAIL: " + ("; ".join(fallos) or out[-400:])[:500], 12, que_hace_falta="ver verificacion_*.txt en la carpeta")
                # (4.14, requisito de verificación completa de las entradas) el pipeline registra la verificación de las entradas financieras del
                # libro final antes de pedir la auditoría: sin el registro vigente y con cobertura completa, ninguna salida presenta la conclusión
                # como apta para dinero real (ficha.aptitud_de_uso; la ficha, el informe y el resumen lo calculan igual en una llamada a mano)
                import verificacion_entradas as VE
                _apto_e, _ve = VE.aptitud(self.c)
                st["verificacion_entradas"] = _ve
                self.log(f"verificación de las entradas financieras: {_ve.get('comprobadas_universo')} de {_ve.get('universo')} celdas del universo comprobadas · "
                         f"apta por entradas: {'sí' if _apto_e else 'no'}" + (f" ({_ve.get('motivo')[:200]})" if _ve.get("motivo") else ""))
                # (4.12 §9) huellas de los libros tal como quedan verificados (verificar_todo.sh deja el evaluado con sus cachés): el paso 13
                # no fija material ni pide auditoría con unos libros distintos de los verificados
                st["libros_verificados"] = {"evaluado": CIE._sha(libro_ev), "datos": CIE._sha(libro_datos) if os.path.exists(libro_datos) else None}
                self.guardar()
            elif paso == 13:
                n = st["intentos"]["auditoria"]
                if st.get("esperando") == "13:auditoria.md" and CIE.material_fijado(self.c):
                    # (4.15, hito 2, I19) relevo caducado: mientras se espera la auditoría, el material vigente tiene que seguir siendo el
                    # fijado. Si cambió (p. ej. verificacion_entradas.json escrito después de fijarlo), ninguna respuesta a la solicitud
                    # antigua podría cerrar nada: se registra, se repite la verificación (paso 12) y el paso 13 fija el material vigente con una
                    # solicitud nueva (la antigua queda «sustituida»). No se aprueba nada con un material distinto
                    fijado = (CIE.material_fijado(self.c) or {}).get("id")
                    vigente, huellas_v = CIE.material(self.c, self.E)
                    if fijado != vigente:
                        antes = (CIE.material_fijado(self.c) or {}).get("archivos") or {}
                        cambiados = sorted(n_ for n_ in set(antes) | set(huellas_v) if antes.get(n_) != huellas_v.get(n_))
                        if not isinstance(st.get("relevos_caducados"), list):  # (hito 2, N10) un registro mal formado se conserva aparte
                            if st.get("relevos_caducados") is not None:
                                st["relevos_caducados_mal_formado"] = st.get("relevos_caducados")
                            st["relevos_caducados"] = []
                        st["relevos_caducados"].append({"material_fijado": fijado, "material_vigente": vigente, "archivos_cambiados": cambiados,
                                                                       "detectado": dt.datetime.now().astimezone().isoformat(timespec="seconds")})
                        st["relevo_por_refijar"] = True  # (hito 2, T9) la próxima fijación del material es la de este relevo
                        self.log(f"relevo caducado: el material fijado {fijado} ya no es el vigente {vigente} (cambian: {', '.join(cambiados)[:300]}); "
                                 "se repite la verificación (paso 12) y se pide una auditoría nueva del material vigente")
                        st["paso"] = 12
                        st["esperando"] = None
                        self.guardar()
                        continue
                if st.get("esperando") != "13:auditoria.md" or not CIE.material_fijado(self.c):
                    # (4.12 §9) antes de fijar el material: los libros tienen que ser los verificados en el paso 12. Si cambiaron (p. ej. una
                    # fórmula alterada después de un cierre, cuya retirada deja el pipeline en el paso 13) o no consta su verificación, se
                    # repite el paso 12: una auditoría no puede apoyarse en un verificacion_integridad.txt de otro libro
                    # Referencia: las huellas que registró el paso 12 o, en un estado anterior a la 4.12 que no las tiene, las del último material
                    # auditado (material_auditoria.json). Sin ninguna de las dos no se repite nada (comportamiento anterior: --desde 13 directo)
                    libro_ev13, libro_datos13 = self.p(f"{self.E}_v63_evaluada.xlsx"), self.p(f"{self.E}_v63_datos.xlsx")
                    lv = st.get("libros_verificados")
                    if not lv:
                        try:
                            arch = (json.load(open(self.p("material_auditoria.json"), encoding="utf-8")) or {}).get("archivos") or {}
                        except (OSError, ValueError):
                            arch = {}
                        lv = {"evaluado": arch.get(os.path.basename(libro_ev13)), "datos": arch.get(os.path.basename(libro_datos13))} if arch else {}
                    distinto = [n for n, ruta in (("evaluado", libro_ev13), ("datos", libro_datos13)) if lv.get(n) and os.path.exists(ruta) and lv[n] != CIE._sha(ruta)]
                    if distinto:
                        self.log(f"los libros ({', '.join(distinto)}) no son los verificados en el paso 12: se repite el paso 12 antes de fijar el material")
                        st["paso"] = 12
                        st["esperando"] = None
                        self.guardar()
                        continue
                    # el material provisional se regenera después del paso 12 (verificar_todo.sh deja el libro evaluado con sus cachés: la
                    # huella de la ficha provisional tiene que ser la del libro auditado) y se fija ANTES de pedir la auditoría (no mientras
                    # se espera: un cambio posterior tiene que notarse)
                    self.run([PY, self.script("ficha.py"), self.c, "--estado", st.get("estado_pendiente") or "concluido", "--provisional"])
                    self.run([PY, self.script("informe.py"), self.c, "--provisional"])
                    st["material_auditoria"] = CIE.fijar_material(self.c, self.E)
                    _rels = st.get("relevos_caducados")
                    if (isinstance(_rels, list) and _rels and isinstance(_rels[-1], dict) and not _rels[-1].get("material_refijado")
                            and st.pop("relevo_por_refijar", False)):
                        _rels[-1]["material_refijado"] = st["material_auditoria"]  # (N10, T9) el material que se fijó justo después de ESTE relevo
                    self.guardar()
                # (4.8.1, R-T1) la auditoría responde a una solicitud identificable y persistente, ligada al material fijado; ni la fecha
                # ni el formato de un informe anterior lo convierten en la respuesta a una solicitud nueva
                sol = self.solicitud_auditoria_vigente()
                txt = self.agente_auditoria(sol, alternativas=[f"auditoria.intento{n + 1}.md"] if n else [])
                st["auditoria"] = self.veredicto_auditoria(txt)
                sol["veredicto"] = st["auditoria"]
                self.guardar()
                if st["auditoria"] == "APROBADO":
                    motivo = CIE.motivo_auditoria_no_corresponde(self.c, txt, self.E)
                    if motivo:
                        # una aprobación que no nombra el material vigente no cierra nada: se pide otra auditoría (no se aprueba ni se pasa a la fase C)
                        st["auditoria"] = None
                        st["intentos"]["auditoria_material"] = st["intentos"].get("auditoria_material", 0) + 1
                        if st["intentos"]["auditoria_material"] > self.lim.get("max_correcciones_esquema", 2):
                            return self.terminar("no_entregable", "fallo_de_implementacion", "auditoría que no corresponde al material vigente tras agotar las correcciones: " + motivo, 13, desde=13)
                        self.pedir_correccion(13, "verificacion", "auditoria.md", f"auditoría inválida para el cierre: {motivo}. El material vigente es {st.get('material_auditoria')} (material_auditoria.json): repite las dieciséis comprobaciones sobre él y escribe «Material auditado: {st.get('material_auditoria')}»")
                        self.log(f"auditoría APROBADO que no corresponde al material vigente: {motivo[:160]}")
                        continue
                if st["auditoria"] == "REPETIR":
                    st["intentos"]["auditoria"] += 1
                    if st["intentos"]["auditoria"] > self.lim.get("max_correcciones_auditoria", 2):
                        return self.terminar("no_entregable", "fallo_de_implementacion", "auditoría en REPETIR tras agotar las correcciones (nunca se aprueba por agotamiento)", 13, desde=10)
                    st["paso"] = 10
                    st["turno_c"] = 1
                    st["intentos"]["fase_c"] = max(st["intentos"]["fase_c"], 1)
                    self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", "auditoría REPETIR: ver auditoria.md")
                    self.log(f"auditoría REPETIR: corrección {st['intentos']['auditoria']} desde el paso 10 (fase C)")
                    continue
            elif paso == 14:
                pendientes = [s for s in st.get("solicitudes_auditoria") or [] if s.get("estado") == "pendiente"]
                # (4.8.1, R-T1) con una solicitud de auditoría pendiente, el cierre exige su respuesta: no lo cierra una aprobación anterior
                motivo = (f"hay una solicitud de auditoría pendiente ({pendientes[-1]['id']}): el cierre exige su respuesta, no una aprobación anterior"
                          if pendientes else CIE.motivo_rechazo_cierre(self.c, self.veredicto_auditoria, st, self.E))
                if motivo:
                    # ningún cierre oficial sin auditoría APROBADO válida del material vigente (también con --desde 14)
                    st["paso"] = 13
                    CIE.archivar_salidas(self.c, "cierre rechazado en el paso 14: " + motivo, CIE.ruta_resumen(self.c, self.cfg), st)
                    st["paso"] = 13
                    self.log(f"CIERRE RECHAZADO: {motivo}")
                    raise CierreRechazado(motivo)
                est = st.get("estado_pendiente") or "concluido"
                st["estado_analisis"] = est
                st["fin"] = dt.datetime.now().isoformat(timespec="seconds")
                self.guardar()
                if self.salidas_finales(cierre=True):
                    # (4.8, X-c) la ficha no cumplió su esquema: el análisis termina en no_entregable por fallo de implementación
                    # (diagnóstico con la causa y la vía de subsanación); no es un rechazo del cierre por la auditoría
                    self.log(f"FIN · estado no_entregable · fallo_de_implementacion: ficha.json no cumple su esquema (estado previsto: {est}); ver diagnostico.md")
                    return
                if self.st.get("estado_analisis") != est or not os.path.exists(self.p("ficha.json")):
                    # (4.7.1, W-e) un generador archivó la salida oficial (p. ej., ficha.py sustituyó la ficha cerrada y la nueva no
                    # tiene aprobación registrada): no queda ningún cierre vigente; nunca se declara completado
                    ultimo = ((self.st.get("cierres_archivados") or [{}])[-1] or {}).get("motivo") or "salida oficial archivada por un generador"
                    self.st["paso"] = min(self.st.get("paso") or 13, 13)
                    self.log(f"CIERRE RECHAZADO tras las salidas finales: {ultimo[:160]}")
                    raise CierreRechazado(f"las salidas finales archivaron la salida oficial ({ultimo[:200]}); hace falta una auditoría nueva del material vigente")
                self.log(f"FIN · estado {est} · auditoría {st.get('auditoria')}")
                return
            st["paso"] += 1
            self.guardar()

    def limite_declarado_por_c(self, fc, libro_ev):
        """Límite del modelo declarado por la fase C (en cualquiera de los dos turnos): si corrige C62, se escribe (con E/F/N de su
        fila; la clase y la confianza son convención del pipeline para esta única corrección mecánica, el apoyo es el motivo del
        personaje) y se verifica; el análisis termina en modelo_no_aplicable sin escribir las 16 celdas ni escalera (§4.7, §7.3)."""
        corr = {k: v for k, v in (fc.get("celdas_corregidas") or {}).items() if k in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes")}
        if corr:
            v = list(corr.values())[0]
            if v.get("despues") not in C.CELDAS["Análisis"]["C62"]["lista"]:
                return self.correccion_c(f"la fase C corrige C62 a {v.get('despues')!r}, fuera del vocabulario de Análisis!C62", 10)
            fila = C.CELDAS["Análisis"]["C62"]["cm"]
            obs = f"[Clase: convención] [Confianza: media]\nHereda: {v.get('antes')} → cambia (razonamiento_corregido): corregida en la fase C al declarar el límite del modelo (clase y confianza: convención del pipeline para esta corrección). Apoyo (motivo del personaje): {str(v.get('motivo'))[:550]}. Lo sustituiría: un motor que capture esta empresa."
            cj = self.p("celdas_C_limite.json")
            json.dump({"Análisis!C62": v.get("despues"), f"Control maestro!E{fila}": C.E_LISTO, f"Control maestro!F{fila}": C.F_ESTIMACION, f"Control maestro!N{fila}": obs[:900]}, open(cj, "w", encoding="utf-8"), ensure_ascii=False)
            rc, out = self.run([PY, self.script("escribir_v63.py"), libro_ev, libro_ev + ".tmp.xlsx", "--celdas", cj, "--verificar", self.cfg["plantilla"]["referencia"]])
            if rc != 0:
                if os.path.exists(libro_ev + ".tmp.xlsx"):
                    os.remove(libro_ev + ".tmp.xlsx")
                self.terminar("no_entregable", "fallo_de_implementacion", "escritura de C62 corregida por la fase C: " + out[-300:], 10)
                return "fin"
            os.replace(libro_ev + ".tmp.xlsx", libro_ev)
        self.terminar("modelo_no_aplicable", "limite_del_modelo", (fc.get("limite_del_modelo") or {}).get("porque") or "límite del modelo declarado por la fase C", 10, categoria="límite del modelo")
        return "fin"

    def correccion_c(self, motivo, paso):
        st = self.st
        st["intentos"]["fase_c"] += 1
        if st["intentos"]["fase_c"] > self.lim.get("max_correcciones_fase_c", self.lim.get("max_correcciones_fase_b", 2)):
            self.terminar("no_entregable", "fallo_de_implementacion", f"fase C tras agotar las correcciones: {motivo}", paso, desde=10, que_hace_falta="revisar el prompt de la fase C en la regla indicada")
            return "fin"
        st["turno_c"] = 1
        st["paso"] = 10
        st["motivo_correccion_c"] = motivo[:400]
        self.pedir_correccion(10, "fase_c_turno1", "fase_c.json", motivo[:400])
        self.log(f"corrección {st['intentos']['fase_c']} de la fase C: {motivo[:200]}")
        return "continuar"

    @staticmethod
    def veredicto_auditoria(txt):
        """Regla de la reparación H2 (8-nov-2026; Anexo D §D.9, prompts/verificacion.md, DECISIONES.md).

        APROBADO solo si se cumplen las tres condiciones:
          1. formato válido: los puntos 1 a 16, cada uno una sola vez y ningún otro número. Un punto es una línea
             «N. PASA» o «N. FALLA» (se admiten marcas de markdown delante y alrededor: `**`, `-`, `#`, `>`, `_`);
          2. los 16 puntos en PASA y la palabra «FALLA» en ninguna parte de la auditoría (una observación que no impide
             aprobar se escribe dentro de un punto en PASA como «Aviso: …»);
          3. exactamente una línea «Veredicto: …» y dice APROBADO, sin coletillas.
        Encabezado (cierre de H2, 8-nov-2026): toda línea que empieza, tras marcas de markdown, por un número de 1 a 3 cifras
        seguido de «.», «)», «:», «·» o un guion que no va seguido de otra cifra («17. PENDIENTE», «100. PASA», «8) PASA»,
        «(9) …», «**9.** …», «8 – …»), o seguido de una palabra en mayúsculas («8 PENDIENTE»). Cada
        encabezado tiene que ser un punto válido (número 1–16, separador «.», estado PASA o FALLA); uno solo que no lo sea basta
        para REPETIR, sea cual sea su número o su estado. No son encabezados las cifras de la evidencia: «1.036 mm», «14,6»,
        «3.463», «12:30» (separador seguido de cifra) ni los años o importes de 4 o más cifras al principio («2016: −238»).
        Cualquier otra cosa es REPETIR: la duda nunca aprueba (D17)."""
        import re
        limpio = txt.replace("\\.", ".")
        lineas = [l for l in limpio.splitlines() if re.match(r"^[\s>*#_-]*veredicto[\s*_]*:", l, re.I)]
        if len(lineas) != 1:
            return "REPETIR"
        resto = re.sub(r"^[\s>*#_-]*veredicto[\s*_]*:", "", lineas[0], flags=re.I).strip().strip("*_ ").strip()
        if not re.fullmatch(r"APROBADO[\s.]*", resto, flags=re.I):
            return "REPETIR"
        if re.search(r"\bFALLA\b", limpio, flags=re.I):
            return "REPETIR"
        encabezado = re.compile(r"^[\s>*#_|-]*\(?(\d{1,3})(?:\)|\s*[.:)·–—-])(?!\d)|^[\s>*#_|-]*(\d{1,3})\s+\**[A-ZÁÉÍÓÚÑ]{4,}\b")
        valido = re.compile(r"^[\s>*#_|-]*(\d{1,2})\.[\s*_]*(PASA|FALLA)\b", flags=re.I)
        puntos = []
        for l in limpio.splitlines():
            if not encabezado.match(l):
                continue
            m = valido.match(l)
            if not m or not 1 <= int(m.group(1)) <= 16:
                return "REPETIR"
            puntos.append((int(m.group(1)), m.group(2).upper()))
        numeros = [n for n, _ in puntos]
        if sorted(numeros) != list(range(1, 17)):
            return "REPETIR"
        if any(estado != "PASA" for _, estado in puntos):
            return "REPETIR"
        return "APROBADO"

    def reaplicar_configuracion(self):
        """(4.11) configuracion_economica.json cambió después de aplicarse al libro: se escribe de nuevo en los libros de datos y
        evaluado (solo las celdas de «Configuración V6.4») y el análisis vuelve al primer paso que depende de ella. Con la fase B ya
        escrita, al paso 9 (recálculo, gramática, variantes, fase C y auditoría nuevas); antes, al paso del volcado o de la fase A.
        Nunca reaprueba nada: la aprobación anterior ya se retiró en la vigencia (el material cambió). Devuelve un motivo de fallo o None."""
        if not self.v64:
            return None
        pc = self.p(SEL.CONF)
        sha_c = CIE._sha(pc)
        previa = self.st.get("configuracion_economica_sha256")
        paso = self.st.get("paso") or 0
        libro_datos, libro_ev = self.p(f"{self.E}_v63_datos.xlsx"), self.p(f"{self.E}_v63_evaluada.xlsx")
        if paso <= 2 and not os.path.exists(libro_datos):
            return None
        distintas = self.configuracion_en_libros_distinta(pc)
        if not distintas and (previa is None or previa == sha_c):
            if previa is None:
                self.st["configuracion_economica_sha256"] = sha_c
            return None
        if not distintas and previa != sha_c:
            # el archivo cambió de bytes pero no de contenido aplicado (p. ej., un texto de la naturaleza): los libros ya coinciden;
            # el material sí cambió (la vigencia ya lo trató); no hace falta rehacer cálculos
            self.st["configuracion_economica_sha256"] = sha_c
            # (4.12 §4) salvo el protocolo del objetivo: si cambió respecto del que evaluó la fase C, la fase C se repite (paso 10) con las
            # mismas variantes (no es un cambio económico); nunca se reaprueba nada
            try:
                fc_prev = json.load(open(self.p("fase_c.json"), encoding="utf-8")) if os.path.exists(self.p("fase_c.json")) else {}
            except (OSError, ValueError):
                fc_prev = {}
            ob_prev = ((fc_prev or {}).get("configuracion_v64") or {}).get("objetivo")
            prot = (SEL.configuracion(self.c) or {}).get("protocolo_objetivo")
            if isinstance(ob_prev, dict) and ob_prev.get("protocolo") != prot and paso >= 10:
                self.st.update({"paso": 10, "estado_analisis": None, "esperando": None, "turno_c": None, "estado_pendiente": None,
                                "estado_analisis_fase_c": None, "auditoria": None,
                                "motivo_correccion_c": f"el protocolo del objetivo cambió ({ob_prev.get('protocolo')} → {prot}): repetir la evaluación del objetivo"})
                self.log(f"protocolo del objetivo cambiado ({ob_prev.get('protocolo')} → {prot}): la fase C se repite desde el paso 10 con las mismas variantes "
                         "(cambio no económico); auditoría nueva; no se reaprueba nada")
                return None
            self.log("configuración económica con bytes distintos y las mismas celdas en los libros: no se rehace ningún cálculo")
            return None
        for libro in (libro_datos, libro_ev):
            if not os.path.exists(libro):
                continue
            rc, out = self.run([PY, self.script("configuracion_economica.py"), "aplicar", libro, libro + ".cfg.xlsx", pc, "--config", self.cfg["_ruta_config"]])
            if rc != 0:
                if os.path.exists(libro + ".cfg.xlsx"):
                    os.remove(libro + ".cfg.xlsx")
                return "configuración económica V6.4 cambiada y no aplicable: " + out[-300:]
            os.replace(libro + ".cfg.xlsx", libro)
        if self.st.get("fase_b_escrita"):
            nuevo = 9
        elif paso >= 8:
            nuevo = 7
        elif paso >= 6:
            nuevo = paso
        elif paso >= 3:
            nuevo = 3
        else:
            nuevo = paso
        self.st.update({"paso": min(paso, nuevo) if paso else nuevo, "estado_analisis": None, "esperando": None, "turno_c": None,
                        "estado_pendiente": None, "estado_analisis_fase_c": None, "auditoria": None, "configuracion_economica_sha256": sha_c})
        self.log(f"configuración económica cambiada ({str(previa)[:12]}… → {sha_c[:12]}…; celdas distintas en {', '.join(distintas)}): reaplicada en los libros; el análisis sigue desde el paso {self.st['paso']} "
                 "(recálculo, variantes, fase C y auditoría nuevas; no se reaprueba nada)")
        return None

    def variantes_corresponden(self):
        """(4.11, H10; 4.12 §5) None si configuracion_v64_variantes.json corresponde a la valoración final; si no, el motivo. Además de que
        la variante «activa» dé el ponderado y el precio de Sí de precio.json (necesario, no suficiente), las variantes tienen que ser de
        las MISMAS entradas económicas del libro evaluado final (instantánea), de la misma configuración económica (huella sin la
        trazabilidad, la naturaleza ni el protocolo) y del mismo vector de escenarios (V MALO/NORMAL/BUENO, probabilidades, ponderado,
        precio de Sí y zona)."""
        import entradas_economicas as EE
        pv, pp = self.p("configuracion_v64_variantes.json"), self.p("precio.json")
        if not (os.path.exists(pv) and os.path.exists(pp)):
            return "faltan configuracion_v64_variantes.json o precio.json en el paso 12 (modo experimental)"
        try:
            var, pr = json.load(open(pv, encoding="utf-8")), json.load(open(pp, encoding="utf-8"))
            res = json.load(open(self.p("resultados.json"), encoding="utf-8")) if os.path.exists(self.p("resultados.json")) else {}
        except (OSError, ValueError) as e:
            return f"configuracion_v64_variantes.json, precio.json o resultados.json ilegibles: {str(e)[:120]}"
        if var.get("formato") not in ("4.12", "4.13"):  # (4.13) los expedientes de la 4.12 conservan sus variantes
            return "configuracion_v64_variantes.json es de un formato anterior a la 4.12 (sin instantánea de entradas económicas ni avisos de dominio): hay que recalcularlas (paso 10)"
        libro_ev = self.p(f"{self.E}_v63_evaluada.xlsx")
        # (4.12, revisión interna R1) con la relación con que se guardaron; con la anterior, la fila 13 de la Historia (bases de P-M1)
        # se compara con el libro de la variante «activa»
        dif, inst, nota_rel = EE.comparar(var.get("entradas_economicas"), libro_ev, self.p("variantes_v64", "recalc", "activa.xlsx"))
        if dif:
            return (f"las entradas económicas del libro evaluado final no son las de las variantes ({len(dif)} celdas distintas: {', '.join(dif[:8])}"
                    + ("…" if len(dif) > 8 else "") + "): las variantes y su evaluación tienen que rehacerse")
        if nota_rel:
            self.log(nota_rel)
        if var.get("configuracion_huella_economica") != EE.huella_configuracion(SEL.configuracion(self.c)):
            return "las variantes V6.4 se calcularon con otra configuración económica (cambia alguna celda de la configuración, no solo su trazabilidad)"
        act = next((v for v in var.get("variantes") or [] if v.get("clave") == "activa"), None)
        if act is None:
            return "configuracion_v64_variantes.json no tiene la variante «activa»"
        for k in ("ponderado", "precio_si"):
            a, b = act.get(k), pr.get(k)
            if not (isinstance(a, (int, float)) and isinstance(b, (int, float)) and abs(a - b) <= 1e-9 * max(1.0, abs(b))):
                return f"la variante «activa» ({k} {a}) no es la valoración final (precio.json {k} {b}): las variantes que evaluó la fase C no corresponden al libro"
        vf, va = EE.vector_escenarios(res, pr), var.get("vector_escenarios_activa") or {}
        malos = [k for k in ("V", "probabilidades", "ponderado", "precio_si", "precio", "zona") if not EE.iguales(va.get(k), vf.get(k))]
        if malos:
            return f"el vector de escenarios de la variante «activa» no es el de la valoración final ({', '.join(f'{k}: {va.get(k)} ≠ {vf.get(k)}' for k in malos)[:300]})"
        return None

    def configuracion_en_libros_distinta(self, pc):
        """(4.11) Libros (datos y evaluado) cuyas celdas de «Configuración V6.4» no son las de configuracion_economica.json."""
        try:
            esperado = CE.celdas(json.load(open(pc, encoding="utf-8")))
        except (OSError, ValueError, KeyError):
            return ["configuracion_economica.json ilegible"]
        from v63_xml import LibroV63
        mal = []
        for nombre in (f"{self.E}_v63_datos.xlsx", f"{self.E}_v63_evaluada.xlsx"):
            ruta = self.p(nombre)
            if not os.path.exists(ruta):
                continue
            lb = LibroV63(ruta)
            if CE.HOJA not in lb.hojas():
                mal.append(nombre + " (sin la hoja de configuración)")
                continue
            for clave, v in esperado.items():
                actual = lb.leer(CE.HOJA, clave.split("!", 1)[1])
                if (actual in (None, "") and v in (None, "")) or actual == v or (isinstance(actual, (int, float)) and isinstance(v, (int, float)) and float(actual) == float(v)):
                    continue
                mal.append(f"{nombre} ({clave.split('!', 1)[1]})")
                break
        return mal

    def variantes_v64(self, libro_ev):
        """(4.11) configuracion_v64_variantes.json del libro evaluado ACTUAL: se recalcula si falta o si es de otro libro o de otra
        configuración (nunca se lee la de una pasada anterior). Devuelve None si está bien o el motivo del fallo mecánico."""
        pv = self.p("configuracion_v64_variantes.json")
        try:
            prev = json.load(open(pv, encoding="utf-8")) if os.path.exists(pv) else None
        except (OSError, ValueError):
            prev = None
        sha_l = CIE._sha(libro_ev)
        sha_c = CIE._sha(self.p(SEL.CONF))
        # (4.13 §5) solo se reutilizan las del formato vigente («4.13»: avisos de dominio de todas las variantes y contrastes aislados);
        # unas de la 4.12 se recalculan cuando el expediente vuelve al paso 10
        if prev and prev.get("aplica") and prev.get("formato") == "4.13":
            # (4.12 §5) se reutilizan solo si son de las MISMAS entradas económicas (instantánea del libro), de la misma configuración
            # económica y del mismo k: un cambio editorial (textos, Observaciones, trazabilidad, protocolo) no obliga a repetir las
            # valoraciones; uno económico sí
            import entradas_economicas as EE
            mismo = not EE.comparar(prev.get("entradas_economicas"), libro_ev, self.p("variantes_v64", "recalc", "activa.xlsx"))[0]
            misma_c = prev.get("configuracion_huella_economica") == EE.huella_configuracion(SEL.configuracion(self.c))
            mismo_k = prev.get("k") == float(self.cfg.get("convenciones", {}).get("k_asimetria", 3))
            if mismo and misma_c and mismo_k:
                if prev.get("libro_origen_sha256") != sha_l or prev.get("configuracion_economica_sha256") != sha_c:
                    self.log("variantes V6.4 reutilizadas: el libro o la configuración cambiaron solo en lo editorial (mismas entradas económicas)")
                return None
        # sin formato 4.13 (o con otras entradas económicas) se recalculan siempre
        rc, out = self.run([PY, self.script("variantes_configuracion_v64.py"), self.c, libro_ev, "--config", self.cfg["_ruta_config"]])
        if rc != 0:
            return out[-300:]
        self.log("variantes de la configuración V6.4 calculadas (configuracion_v64_variantes.json)")
        return None

    def objetivo_sin_protocolo(self, fc):
        """(4.12 §4) (detalle, qué hace falta) si el objetivo depende de hipótesis sin fundamento suficiente y configuracion_economica.json no
        declara protocolo_objetivo (V6.4 experimental); None en los demás casos. Explica las dos lecturas sin elegir ninguna."""
        if not (self.v64 and SEL.experimental(self.c)):
            return None
        import objetivo_v64 as OBJ
        ev = OBJ.evaluar(self.c, fc)
        if not ev or ev["tratamiento"] != "objetivo_sin_protocolo":
            return None
        lec = OBJ.lecturas_sin_protocolo(ev)
        vc = ev.get("valor_calculado_condicional")
        det = (f"el objetivo (valor calculado condicional: precio de Sí {vc:.2f}) depende de hipótesis sin fundamento suficiente "
               f"({', '.join(ev['hipotesis_que_condicionan'])}) y configuracion_economica.json no declara protocolo_objetivo: no se emite ningún objetivo "
               f"oficial (4.12 §4). Con bloqueo_del_objetivo: {lec['bloqueo_del_objetivo']}. Con objetivo_condicionado: {lec['objetivo_condicionado']}.")
        return det, ("declarar protocolo_objetivo (bloqueo_del_objetivo u objetivo_condicionado; ensayo, no adopción) en configuracion_economica.json y "
                     "repetir desde la fase C (paso 10), o preparar un expediente nuevo con el protocolo declarado")

    def bloqueo_del_objetivo_v64(self, fc):
        """(4.12 §4) True si el expediente es V6.4 experimental, declara el protocolo de bloqueo del objetivo y la fase C lo aplica."""
        if not (self.v64 and SEL.experimental(self.c)):
            return False
        ob = (fc.get("configuracion_v64") or {}).get("objetivo") or {}
        return ((SEL.configuracion(self.c) or {}).get("protocolo_objetivo") == "bloqueo_del_objetivo" and ob.get("tratamiento") == "objetivo_bloqueado"
                and ob.get("origen_del_bloqueo") == "protocolo_de_bloqueo")

    def coherencia_v64(self, fc):
        """(4.11) En modo experimental, la fase C evalúa expresamente cada parámetro activo y el mantenimiento (P-M1); «la zona no
        cambia» solo puede afirmarse de las variantes calculadas; ninguna configuración se presenta como adoptada.
        (4.12 §4) Además separa, por parámetro, la materialidad para la acción (true · false · null = no determinada), la materialidad
        para el objetivo, el fundamento suficiente, la información que falta y el ámbito (las variantes calculadas que lo varían: tiene
        que ser exactamente el de configuracion_v64_variantes.json), y comprueba el bloque `objetivo` contra objetivo_v64.evaluar
        (protocolo, condicionantes, ámbito, acción sostenida, tratamiento y la decisión que corresponde). Con «comprar», D10 cubre
        también los parámetros experimentales sin fundamento suficiente (lista, combinación con los numéricos ACTIVOS y alternativas
        no numéricas evaluadas de forma explícita por comprobacion_conjunta.py)."""
        if not (self.v64 and SEL.experimental(self.c)):
            return None
        import objetivo_v64 as OBJ
        conf = SEL.configuracion(self.c) or {}
        cv = fc.get("configuracion_v64")
        if not isinstance(cv, dict):
            return "falta configuracion_v64 en fase_c.json (modo experimental: evaluación de cada parámetro activo y del mantenimiento; prompt de la fase C, §V6.4)"
        params = {x.get("clave"): x for x in (cv.get("parametros") or []) if isinstance(x, dict)}
        faltan = [k for k in CE.activos(conf) if k != "modo" and k not in params]
        if faltan:
            return "configuracion_v64.parametros no evalúa los parámetros activos: " + ", ".join(faltan)
        for k, x in params.items():
            if x.get("clase") not in C.CLASES or x.get("confianza") not in C.CONFIANZAS or not str(x.get("materialidad") or "").strip() or not isinstance(x.get("material_para_conclusion"), bool):
                return f"configuracion_v64.parametros[{k}]: clase ({'/'.join(C.CLASES)}), confianza, materialidad y material_para_conclusion (booleano) obligatorios"
        m = cv.get("mantenimiento") or {}
        if not str(m.get("evaluacion") or "").strip() or m.get("adoptada") is not False:
            return "configuracion_v64.mantenimiento: evaluación del mantenimiento y de la estructura obligatoria, con adoptada = false (el ensayo no adopta ninguna estructura)"
        var = json.load(open(self.p("configuracion_v64_variantes.json"), encoding="utf-8")) if os.path.exists(self.p("configuracion_v64_variantes.json")) else {}
        afirma = cv.get("zona_igual_en_variantes_calculadas")
        if not isinstance(afirma, bool):
            return "configuracion_v64.zona_igual_en_variantes_calculadas: booleano obligatorio (solo respecto de configuracion_v64_variantes.json)"
        if afirma and not var.get("zona_igual_en_todas_las_calculadas"):
            return "configuracion_v64 afirma que la zona no cambia, pero configuracion_v64_variantes.json no lo respalda (zonas: " + ", ".join(var.get("zonas_calculadas") or []) + ")"
        # ---------------------------------------------------------------------------------------- (4.12 §4) materialidad separada
        precio = json.load(open(self.p("precio.json"), encoding="utf-8")) if os.path.exists(self.p("precio.json")) else {}
        ccj = json.load(open(self.p("comprobacion_conjunta.json"), encoding="utf-8")) if os.path.exists(self.p("comprobacion_conjunta.json")) else None
        ev = OBJ.evaluar(self.c, fc, precio, var, conf, ccj)
        if ev["variantes_sin_parametros_variados"]:
            return "configuracion_v64_variantes.json no dice qué parámetros varía cada variante (formato anterior a la 4.12): hay que recalcular las variantes (paso 10)"
        acc_prov = ev["accion_evaluada"]  # (4.13 §4) la acción final (la provisional solo si la final es nula)
        clase0 = OBJ.CLASE_ZONA.get(precio.get("zona"))
        depende_de_zona = acc_prov == "comprar" or (acc_prov == "esperar" and clase0 == "por_encima_del_precio_de_si")
        zonas = {v.get("clave"): v.get("zona") for v in var.get("variantes") or []}
        for k, x in params.items():
            if "material_para_accion" not in x or x.get("material_para_accion") not in (True, False, None):
                return f"configuracion_v64.parametros[{k}].material_para_accion: true, false o null (no determinada: ninguna variante calculada lo varía), obligatoria (4.12 §4)"
            for campo in ("material_para_objetivo", "fundamento_suficiente"):
                # (4.13, revisión interna R4) con el contrato de cobertura, la materialidad para el objetivo admite null (no determinada)
                if not isinstance(x.get(campo), bool) and not (campo == "material_para_objetivo" and ev.get("contrato_cobertura") and "material_para_objetivo" in x and x[campo] is None):
                    return f"configuracion_v64.parametros[{k}].{campo}: booleano obligatorio (4.12 §4)" + (" (o null, no determinada, con el contrato 4.13)" if campo == "material_para_objetivo" and ev.get("contrato_cobertura") else "")
            if x["fundamento_suficiente"] is False and not str(x.get("informacion_que_falta") or "").strip():
                return f"configuracion_v64.parametros[{k}]: sin fundamento suficiente exige informacion_que_falta (qué dato o documento lo fundaría)"
            if x["material_para_conclusion"] != (x["material_para_accion"] is True or x["material_para_objetivo"] is True):
                return (f"configuracion_v64.parametros[{k}].material_para_conclusion ({x['material_para_conclusion']}) tiene que ser material_para_accion o "
                        f"material_para_objetivo ({x['material_para_accion']}, {x['material_para_objetivo']}): se conserva por compatibilidad")
            amb = OBJ.ambito_parametro(var, k)
            if sorted(x.get("ambito") or []) != sorted(amb):
                return (f"configuracion_v64.parametros[{k}].ambito {sorted(x.get('ambito') or [])} no es el de configuracion_v64_variantes.json: las variantes calculadas "
                        f"que varían {k} son {sorted(amb) or 'ninguna'} (columna «Parámetros que varía»)")
            if ev.get("contrato_cobertura"):
                # (4.13 §5) contrato de cobertura: el tipo es mecánico; la materialidad para la acción solo es «calculada» con un contraste
                # aislado o una variación conjunta necesaria; si no, es un juicio económico con evidencia o queda no determinada (null)
                m = self._coherencia_cobertura_413(k, x, ev, conf, depende_de_zona, zonas, clase0, var)
                if m:
                    return m
                continue
            if x["material_para_accion"] is None and amb:
                return f"configuracion_v64.parametros[{k}].material_para_accion = null, pero {len(amb)} variantes calculadas lo varían ({', '.join(amb)}): decide true o false"
            if x["material_para_accion"] is False and depende_de_zona:
                if not amb:
                    return f"configuracion_v64.parametros[{k}].material_para_accion = false sin ninguna variante calculada que lo varíe: no está determinada (null)"
                cambian = [f"{v} ({zonas.get(v)})" for v in amb if OBJ.CLASE_ZONA.get(zonas.get(v)) != clase0]
                if cambian:
                    return f"configuracion_v64.parametros[{k}].material_para_accion = false, pero estas variantes que lo varían cambian la acción por la zona: {', '.join(cambian)}"
        # (4.12 §5) avisos de dominio: cada aviso activo (y el factor de reestimación, que se muestra siempre) evaluado con su consecuencia;
        # uno material condiciona el objetivo («limite:<id>», objetivo_v64) y nunca acompaña una compra
        import dominios_v64 as DOM
        evaluados = {a.get("id"): a for a in cv.get("avisos_de_dominio") or [] if isinstance(a, dict)}
        for aid in DOM.que_evaluar(var.get("avisos_de_dominio")):
            a = evaluados.get(aid)
            if not a or not isinstance(a.get("material_para_conclusion"), bool) or not str(a.get("consecuencia") or "").strip():
                return (f"configuracion_v64.avisos_de_dominio: falta evaluar el aviso «{aid}» de configuracion_v64_variantes.md (material_para_conclusion y consecuencia; "
                        "4.12 §5: una limitación material tiene una consecuencia verificable)")
        sobran = [k for k in evaluados if k not in DOM.que_evaluar(var.get("avisos_de_dominio"))]
        if sobran:
            return f"configuracion_v64.avisos_de_dominio evalúa avisos que no están activos en configuracion_v64_variantes.json: {sobran}"
        if var.get("formato") == OBJ.FORMATO_COBERTURA:
            # (4.13 §5) avisos de dominio de las variantes calculadas, agrupados por aviso: cada grupo activo en alguna variante (no solo
            # en la activa) se evalúa con su consecuencia y la conclusión a la que afecta
            ev_var = {a.get("id"): a for a in cv.get("avisos_de_dominio_variantes") or [] if isinstance(a, dict)}
            grupos = DOM.grupos_a_evaluar(var.get("avisos_de_dominio_variantes"))
            for aid in grupos:
                a = ev_var.get(aid)
                if not a or not isinstance(a.get("material_para_conclusion"), bool) or not str(a.get("consecuencia") or "").strip():
                    return (f"configuracion_v64.avisos_de_dominio_variantes: falta evaluar el aviso «{aid}», activo en variantes calculadas "
                            f"({', '.join((var.get('avisos_de_dominio_variantes') or {}).get(aid, {}).get('variantes') or [])[:200]}): material_para_conclusion y consecuencia")
            sobran_v = [k for k in ev_var if k not in grupos]
            if sobran_v:
                return f"configuracion_v64.avisos_de_dominio_variantes evalúa avisos que no están activos en ninguna variante calculada: {sobran_v}"
            evaluados = {**evaluados, **{f"variantes:{k}": a for k, a in ev_var.items()}}
        materiales = [k for k, a in evaluados.items() if a.get("material_para_conclusion") is True]
        if materiales and fc.get("estado_analisis") == "concluido" and (fc.get("decision") or {}).get("accion") == "comprar":
            return f"comprar con un límite del modelo material ({', '.join(materiales)}): la compra no puede apoyarse en una lectura fuera del dominio declarado"
        # bloque objetivo
        ob = cv.get("objetivo")
        if not isinstance(ob, dict):
            return "falta configuracion_v64.objetivo (4.12 §4: protocolo, hipótesis que condicionan el objetivo, ámbito, acción sostenida y tratamiento)"
        if ob.get("protocolo") != ev["protocolo"]:
            return f"configuracion_v64.objetivo.protocolo {ob.get('protocolo')!r} ≠ protocolo_objetivo de configuracion_economica.json {ev['protocolo']!r}"
        if sorted(ob.get("hipotesis_que_condicionan") or []) != sorted(ev["hipotesis_que_condicionan"]):
            return ("configuracion_v64.objetivo.hipotesis_que_condicionan no son las que corresponden: los parámetros con material_para_objetivo = true y "
                    f"fundamento_suficiente = false y toda la lista D10 (Anexo B §B.6.7) → {ev['hipotesis_que_condicionan']}")
        if sorted(ob.get("ambito") or []) != sorted(ev["ambito"]):
            return f"configuracion_v64.objetivo.ambito tiene que ser TODO el ámbito calculado (sin la activa): {ev['ambito']}"
        if ob.get("accion_sostenida_en_ambito") is not ev["accion_sostenida_en_ambito"]:
            return (f"configuracion_v64.objetivo.accion_sostenida_en_ambito = {ob.get('accion_sostenida_en_ambito')!r}; en el ámbito calculado es "
                    f"{ev['accion_sostenida_en_ambito']}" + (f" ({'; '.join(ev['motivos_no_sostenida'])[:300]})" if ev["motivos_no_sostenida"] else ""))
        if ob.get("tratamiento") != ev["tratamiento"] or (ev["tratamiento"] == "objetivo_bloqueado" and ob.get("origen_del_bloqueo") != ev["origen_del_bloqueo"]):
            return (f"configuracion_v64.objetivo.tratamiento {ob.get('tratamiento')!r} (origen {ob.get('origen_del_bloqueo')!r}) no corresponde: con el protocolo "
                    f"{ev['protocolo']!r} es {ev['tratamiento']!r}" + (f" ({ev['origen_del_bloqueo']})" if ev["origen_del_bloqueo"] else "") + f": {ev['motivo_mecanico']}")
        if not str(ob.get("motivo") or "").strip():
            return "configuracion_v64.objetivo.motivo obligatorio"
        if ev["tratamiento"] in ("objetivo_bloqueado", "objetivo_sin_protocolo") and not [i for i in (ob.get("informacion_no_disponible") or []) if str(i).strip()]:
            return f"configuracion_v64.objetivo.informacion_no_disponible: obligatoria con {ev['tratamiento']} (qué información material falta para el objetivo)"
        # (4.13 §4) contradicciones entre acción final, estado, protocolo, objetivo estructurado y objetivo de la decisión (también
        # con «sin objetivo», que hasta la 4.12 no comprobaba nada de la decisión final)
        contra = OBJ.contradicciones_salida(fc.get("estado_analisis"), fc.get("decision"), None, ev)
        if contra:
            return "contradicción en la decisión de la fase C: " + " | ".join(contra)[:600]
        if ev["estado_esperado"]:
            est, dec = fc.get("estado_analisis"), fc.get("decision") or {}
            po, po_e = dec.get("precio_objetivo"), ev["precio_objetivo_esperado"]
            po_ok = (po is None and po_e is None) or OBJ.mismo_importe(po, po_e)  # (4.13 §4) redondeo declarado (dos decimales)
            if est != ev["estado_esperado"] or dec.get("accion") != ev["accion_esperada"] or not po_ok or fc.get("cubo_final") != ev["cubo_esperado"]:
                return (f"con el tratamiento {ev['tratamiento']}" + (f" ({ev['origen_del_bloqueo']})" if ev["origen_del_bloqueo"] else "")
                        + f" corresponden estado {ev['estado_esperado']}, cubo {ev['cubo_esperado']}, acción {ev['accion_esperada']} y precio_objetivo {po_e}; "
                        f"la fase C escribe {est}, {fc.get('cubo_final')}, {dec.get('accion')} y {po}")
        # ---------------------------------------------------------------------------------------- (4.12 §4 y §9) compra y D10
        fm = fc.get("fundamento_material") or {}
        cc = fm.get("comprobacion_conjunta") or {}
        comb = {(k if "!" in k else f"Análisis!{k}"): v for k, v in (cc.get("combinacion") or {}).items()}
        activos_num = CE.numericos_activos(conf)
        mueve_cfg = [k for k in comb if k.startswith(CE.HOJA + "!")]
        inactivos = [k for k in mueve_cfg if k not in activos_num.values()]
        if inactivos:
            return f"la combinación de la comprobación conjunta mueve parámetros de la configuración que no están activos: {inactivos} (activos numéricos: {sorted(activos_num.values()) or 'ninguno'})"
        if fc.get("estado_analisis") == "concluido" and (fc.get("decision") or {}).get("accion") == "comprar":
            en_d10 = {OBJ.clave_de_celda(h.get("celda"), conf) or h.get("celda") for h in fm.get("hipotesis_sin_fundamento") or []}
            alt = set(cc.get("alternativas_no_numericas") or [])
            por_alt = (ccj or {}).get("por_alternativa") or []
            for k, x in params.items():
                if x.get("fundamento_suficiente") is not False:
                    continue
                if k not in en_d10:
                    return (f"comprar con el parámetro experimental {k} sin fundamento suficiente fuera de fundamento_material.hipotesis_sin_fundamento "
                            f"(celda {CE.celda_principal(k, conf)}): un objetivo provisional no exime una compra de D10")
                if k in activos_num:
                    if activos_num[k] not in comb:
                        return f"comprar: la comprobación conjunta no mueve {activos_num[k]} ({k} sin fundamento suficiente)"
                else:
                    if k not in alt:
                        return f"comprar: {k} es una hipótesis no numérica sin fundamento suficiente y la comprobación conjunta no evalúa sus alternativas (alternativas_no_numericas)"
                    res_k = [a for a in por_alt if a.get("clave") == k]
                    if not res_k or not all(a.get("definida") and a.get("sobrevive") for a in res_k):
                        return f"comprar: las alternativas de {k} no están todas definidas y superadas en comprobacion_conjunta.json ({[(a.get('alternativa'), a.get('zona'), a.get('sobrevive')) for a in res_k] or 'ninguna'})"
                    amb = OBJ.ambito_parametro(var, k) or []
                    fuera = [f"{v} ({zonas.get(v)})" for v in amb if OBJ.CLASE_ZONA.get(zonas.get(v)) != "cumple_la_regla"]
                    if not amb or fuera:
                        return f"comprar: las variantes calculadas que varían {k} no sostienen la compra ({', '.join(fuera) or 'ninguna variante lo varía'})"
        return None

    def _coherencia_cobertura_413(self, k, x, ev, conf, depende_de_zona, zonas, clase0, var=None):
        """(4.13 §5) Reglas del contrato de cobertura para un parámetro de la fase C. None si cumple; si no, el motivo."""
        import objetivo_v64 as OBJ
        cb = (ev.get("cobertura_por_parametro") or {}).get(k) or {}
        pref = f"configuracion_v64.parametros[{k}]"
        if x.get("cobertura") != cb.get("tipo"):
            return (f"{pref}.cobertura {x.get('cobertura')!r} no es la de las variantes calculadas: {cb.get('tipo')} (aisladas {cb.get('aisladas') or 'ninguna'}; "
                    f"conjuntas necesarias {cb.get('conjuntas_necesarias') or 'ninguna'}; conjuntas {cb.get('conjuntas') or 'ninguna'})")
        base, mpa = x.get("base_de_la_materialidad"), x.get("material_para_accion")
        if base not in OBJ.BASES_MATERIALIDAD:
            return f"{pref}.base_de_la_materialidad: una de {OBJ.BASES_MATERIALIDAD} (4.13 §5)"
        for campo in ("evidencia", "hechos"):
            v = x.get(campo)
            if not (isinstance(v, list) and [e for e in v if isinstance(e, str) and e.strip()]):
                return f"{pref}.{campo}: lista no vacía obligatoria (4.13 §5: evidencia pertinente citada; hechos separados de las inferencias)"
        if not isinstance(x.get("inferencias"), list) or not all(isinstance(e, str) for e in x["inferencias"]):
            return f"{pref}.inferencias: lista de textos obligatoria (puede ir vacía si no hay inferencias)"
        if (base == "no_determinada") != (mpa is None):
            return f"{pref}: material_para_accion = null si y solo si base_de_la_materialidad = «no_determinada» (lo no determinado no se convierte en false)"
        if base == "calculada" and cb.get("tipo") not in OBJ.TIPOS_COBERTURA[:2]:
            return (f"{pref}: materialidad «calculada» con cobertura {cb.get('tipo')}: ninguna variante calculada contrasta {k} de forma aislada ni con sus "
                    f"vinculados necesarios; es un juicio económico (con evidencia) o queda no determinada")
        if base == "juicio_economico" and not [e for e in x.get("inferencias") or [] if str(e).strip()]:
            return f"{pref}: un juicio económico declara sus inferencias (4.13 §5: no se presenta como constatación calculada)"
        contraste = (cb.get("aisladas") or []) + (cb.get("conjuntas_necesarias") or [])
        cambian = [f"{v} ({zonas.get(v)})" for v in contraste if OBJ.CLASE_ZONA.get(zonas.get(v)) != clase0]
        if depende_de_zona and cambian and mpa is not True:
            return f"{pref}.material_para_accion = {mpa!r}, pero los contrastes calculados de {k} cambian la acción por la zona: {', '.join(cambian)} (es material: true)"
        if base == "calculada" and mpa is False and depende_de_zona and not contraste:
            return f"{pref}: material_para_accion = false calculada sin ningún contraste de {k}"
        # (4.13, revisión interna R4) el mismo contrato para la materialidad para el OBJETIVO: base explícita; «calculada» solo con un
        # contraste, y «false calculada» solo si ningún contraste mueve el precio de Sí al redondeo declarado (dos decimales); si lo
        # mueve, «no material» es un juicio económico con su evidencia; null ⇔ no determinada (y entonces condiciona el objetivo)
        if self.st.get("contrato_juicio_objetivo") == OBJ.FORMATO_JUICIO_OBJETIVO:
            # (4.14, encargo de cierre §5; S3 y S11) juicio PROPIO sobre el objetivo: contraste mecánico, límites, base, criterio y comparación.
            # El contrato lo fijó el pipeline al generar el prompt de la fase C (paso 10), no el agente. Comprueba contrato y coherencia; la
            # pertinencia económica la revisa la auditoría. Sustituye a las reglas 4.13 del objetivo (_objetivo_413), que siguen para las fases C de la 4.13
            m = OBJ.validar_juicio_objetivo(k, x, cb, var, ev.get("valor_calculado_condicional"), politicas=None)
            if m:
                return m
        else:
            m = self._objetivo_413(k, x, cb, var, ev, contraste, pref)
            if m:
                return m
        disc = (ev.get("discrepancias_por_parametro") or {}).get(k) or []
        rev = {r.get("discrepancia"): r for r in x.get("contradicciones_revisadas") or [] if isinstance(r, dict)}
        sin = [d for d in disc if not str((rev.get(d) or {}).get("resolucion") or "").strip()]
        if sin:
            return (f"{pref}.contradicciones_revisadas: faltan por revisar (con su resolución) las discrepancias con configuracion_economica.json: {', '.join(sin)} "
                    "(4.13 §5; no hay umbral: se revisan, no se decide por una cifra)")
        sobran = [d for d in rev if d not in disc]
        if sobran:
            return f"{pref}.contradicciones_revisadas: {sobran} no son discrepancias de este parámetro ({disc or 'ninguna'})"
        return None

    def _objetivo_413(self, k, x, cb, var, ev, contraste, pref):
        """(4.13, revisión interna R4) reglas del objetivo del contrato 4.13 (expedientes cuya fase C no se generó con el contrato 4.14)."""
        import objetivo_v64 as OBJ
        base_o, mpo = x.get("base_de_la_materialidad_objetivo"), x.get("material_para_objetivo")
        if base_o not in OBJ.BASES_MATERIALIDAD:
            return f"{pref}.base_de_la_materialidad_objetivo: una de {OBJ.BASES_MATERIALIDAD} (4.13; revisión interna R4)"
        if (base_o == "no_determinada") != (mpo is None):
            return f"{pref}: material_para_objetivo = null si y solo si base_de_la_materialidad_objetivo = «no_determinada»"
        if base_o == "calculada" and cb.get("tipo") not in OBJ.TIPOS_COBERTURA[:2]:
            return f"{pref}: materialidad para el objetivo «calculada» con cobertura {cb.get('tipo')}: es un juicio económico (con evidencia) o queda no determinada"
        if base_o == "juicio_economico" and not [e for e in x.get("inferencias") or [] if str(e).strip()]:
            return f"{pref}: un juicio económico sobre el objetivo declara sus inferencias"
        if base_o == "calculada" and mpo is False:
            psi = {v.get("clave"): v.get("precio_si") for v in (var or {}).get("variantes") or []}
            mueven = [f"{v} ({psi.get(v)})" for v in contraste if OBJ._num(psi.get(v)) and OBJ._num(ev.get("valor_calculado_condicional"))
                      and round(psi[v], 2) != round(ev["valor_calculado_condicional"], 2)]
            if mueven:
                return (f"{pref}: material_para_objetivo = false «calculada», pero estos contrastes mueven el precio de Sí al redondeo declarado: {', '.join(mueven)[:300]}; "
                        "que ese movimiento no sea material es un juicio económico (base «juicio_economico», con evidencia e inferencias)")
        return None

    def coherencia_fase_c(self, fc):
        """Coherencia del cierre de la fase C (encargo §8, Anexo D §D.6, S-19, D10, D16). No se fía solo de lo que escribe el
        agente: cruza con precio.json (zona), comprobacion_conjunta.json (sobrevive del script) y la lista de hipótesis."""
        est = fc.get("estado_analisis")
        dec = fc.get("decision") or {}
        acc = dec.get("accion")
        cubo = fc.get("cubo_final")
        fm = fc.get("fundamento_material") or {}
        cc = fm.get("comprobacion_conjunta") or {}
        hs = fm.get("hipotesis_sin_fundamento") or []
        rda = fc.get("revision_datos_ausentes") or {}
        revisados = rda.get("revisados") or []
        precio = json.load(open(self.p("precio.json"), encoding="utf-8")) if os.path.exists(self.p("precio.json")) else {}
        ccj = json.load(open(self.p("comprobacion_conjunta.json"), encoding="utf-8")) if os.path.exists(self.p("comprobacion_conjunta.json")) else None
        zona = precio.get("zona")
        if est not in ("concluido", "pendiente_de_investigacion", "modelo_no_aplicable", "pendiente_de_datos"):
            return f"estado_analisis {est!r} no válido"
        if cubo not in C.CUBOS:
            return f"cubo_final {cubo!r} no válido"
        if acc not in C.ACCIONES + (None,):
            return f"accion {acc!r} no válida"
        # S-19: la materialidad declarada por dato manda sobre el resumen
        material_real = any(x.get("material_para_conclusion_favorable") for x in revisados)
        if bool(rda.get("alguno_material")) != material_real:
            return f"alguno_material = {rda.get('alguno_material')} pero los datos revisados dicen {material_real} (S-19)"
        if material_real and est != "pendiente_de_datos" and not (est == "concluido" and acc in ("descartar", "demasiado_dificil")) and est != "modelo_no_aplicable":
            # un dato material para la conclusión favorable solo convive con descartar/demasiado_dificil (§8: el descalificador va antes) o con el límite del modelo
            return "revisión de datos ausentes material pero estado ≠ pendiente_de_datos (S-19); solo descartar/demasiado_dificil pueden convivir con un dato material"
        if est == "pendiente_de_datos" and not material_real and not self.bloqueo_del_objetivo_v64(fc):
            # (4.12 §4) única excepción: el protocolo experimental de bloqueo del objetivo (V6.4 en modo experimental), que
            # coherencia_v64 comprueba entero (protocolo declarado, condicionantes, información no disponible y decisión)
            return "pendiente_de_datos sin ningún dato ausente declarado material (S-19)"
        if est == "pendiente_de_datos" and (acc is not None or cubo == "Sí"):
            return "pendiente_de_datos exige acción null y cubo ≠ Sí"
        if est == "pendiente_de_investigacion" and (acc is not None or cubo != "Vigilar"):
            return "pendiente_de_investigacion exige cubo Vigilar y acción null"
        if est == "modelo_no_aplicable":
            if not (fc.get("limite_del_modelo") or {}).get("aplica"):
                return "modelo_no_aplicable sin limite_del_modelo.aplica"
            if acc in ("comprar", "esperar") or cubo == "Sí":
                return "modelo_no_aplicable no admite comprar/esperar ni cubo Sí"
        # autocomprobación (P-1): diez entradas que cubran las diez tendencias de la sección 16 (se reconocen por palabras clave)
        claves = [("anclaje", "etapa 1"), ("precio|fuente externa",), ("consistencia|compromiso",), ("historia bonita|viento de cola",),
                  ("optimismo|tasa base",), ("doble castigo|mismo riesgo",), ("disponibilidad|v[ií]vido",), ("autoridad|gu[ií]a de la direcci",),
                  ("malo",), ("no numerable|no está en las palancas|no esta en las palancas",)]
        sesgos = [str(x.get("sesgo") or "").lower() for x in (fc.get("autocomprobacion") or [])]
        if len(sesgos) != 10:
            return f"autocomprobacion con {len(sesgos)} entradas (tienen que ser las diez tendencias de la sección 16)"
        for patrones in claves:
            if not any(all(re.search(pt, sg) for pt in patrones) for sg in sesgos):
                return f"autocomprobacion: falta la tendencia «{' + '.join(patrones)}» (sección 16)"
        # celdas_corregidas: solo C62 (límite del modelo) puede cambiar de valor; lo demás se documenta sin cambiar (una vuelta C→A no existe)
        for k, v in (fc.get("celdas_corregidas") or {}).items():
            if k not in ("C62", "Análisis!C62") and v.get("despues") != v.get("antes"):
                return f"celdas_corregidas[{k}] cambia el valor ({v.get('antes')!r} → {v.get('despues')!r}): la fase C no reescribe celdas de A/B; pide revisar_palancas o deja despues = antes y lo anota en incoherencias"
        # fundamento material (D10)
        sin_base = [h.get("celda") for h in hs if not ((h.get("alternativas_defendibles") or {}).get("hay_base"))]
        res_fm = fm.get("resultado")
        if est == "concluido":
            if acc is None:
                return "concluido sin acción"
            if (acc == "comprar") != (cubo == "Sí"):
                return "comprar ⇔ cubo Sí"
            if acc == "comprar":
                if "sin_lectura" in precio or "sin_escalera" in precio or zona not in ("cumple_regla_k", "bajo_malo"):
                    return f"comprar con zona {zona!r} de precio.json (solo cumple_regla_k o bajo_malo)"
                if not hs:
                    if res_fm != "sin_limitacion":
                        return f"comprar sin hipótesis sin fundamento exige resultado sin_limitacion (hay {res_fm!r})"
                else:
                    if res_fm != "comprobacion_conjunta_superada":
                        return f"comprar con {len(hs)} hipótesis sin fundamento exige comprobacion_conjunta_superada (hay {res_fm!r})"
                    if sin_base:
                        return f"comprar con hipótesis sin base para acotar: {sin_base}"
                    if not cc.get("procede") or not (cc.get("combinacion") or cc.get("alternativas_no_numericas")):
                        return "comprar con hipótesis sin fundamento pero sin comprobación conjunta (procede/combinacion o alternativas_no_numericas)"
                    if ccj is None:
                        return "comprar con comprobación conjunta declarada pero sin comprobacion_conjunta.json (el script no la ejecutó)"
                    if cc.get("sobrevive") is not True or ccj.get("sobrevive") is not True:
                        return f"comprar con comprobación conjunta no superada (fase C: {cc.get('sobrevive')}; script: {ccj.get('sobrevive')})"
            if acc == "esperar":
                if cubo != "Vigilar":
                    return "esperar ⇔ cubo Vigilar"
                po = dec.get("precio_objetivo"); psi = precio.get("precio_si")
                if zona in ("cumple_regla_k", "bajo_malo"):
                    if not (dec.get("condicion") or "").strip():
                        return f"esperar con zona {zona}: exige una condición concreta que no sea de precio"
                elif not (isinstance(po, (int, float)) and isinstance(psi, (int, float)) and abs(po - psi) <= 0.005 * max(1, abs(psi))):
                    return f"esperar: precio_objetivo {po!r} ≠ precio de Sí de precio.json {psi!r}"
            if acc == "descartar" and cubo != "No":
                return "descartar ⇔ cubo No"
            if acc == "demasiado_dificil" and cubo != "Demasiado difícil":
                return "demasiado_dificil ⇔ cubo Demasiado difícil"
            if res_fm == "pendiente_de_investigacion":
                return "fundamento_material pendiente_de_investigacion con estado concluido"
        if est == "pendiente_de_investigacion" and res_fm != "pendiente_de_investigacion":
            return f"pendiente_de_investigacion exige fundamento_material.resultado = pendiente_de_investigacion (hay {res_fm!r})"
        if cc.get("sobrevive") is not None and ccj is not None and cc.get("sobrevive") != ccj.get("sobrevive"):
            return f"sobrevive de la fase C ({cc.get('sobrevive')}) ≠ sobrevive del script ({ccj.get('sobrevive')})"
        if cc.get("sobrevive") is not None and ccj is None:
            return "sobrevive informado sin comprobacion_conjunta.json"
        # C104 (D16) coherente con el estado y la acción
        c104 = str((fc.get("celdas") or {}).get("C104") or "")
        if not c104.startswith(C.C104_PREFIJO) or "%" in c104:
            return f"C104 no empieza por «{C.C104_PREFIJO}» o contiene un porcentaje (D16)"
        esperado = {"comprar": "comprar al precio actual", "esperar": "esperar", "descartar": "descartar", "demasiado_dificil": "demasiado difícil"}.get(acc)
        if est == "pendiente_de_datos":
            esperado = "sin conclusión (pendiente de datos"
        elif est == "pendiente_de_investigacion":
            esperado = "sin conclusión (pendiente de investigación)"
        if esperado and esperado.lower() not in c104.lower():
            return f"C104 no dice «{esperado}» (estado {est}, acción {acc})"
        if est != "modelo_no_aplicable":
            # correspondencia cerrada D10 ↔ estado ↔ acción ↔ etiqueta visible de C104 (cierre_v2.FUNDAMENTO_C104; reparación 4.6)
            motivo = CIE.motivo_c104_fundamento(est, acc, res_fm, c104)
            if motivo:
                return motivo
        sin_escalera = "sin escalera aplicable" in c104.lower()
        if sin_escalera and (acc in ("comprar", "esperar") or est in ("pendiente_de_datos", "pendiente_de_investigacion")):
            return "C104 dice «sin escalera aplicable» con una conclusión que necesita la escalera"
        if not sin_escalera:
            for clave, valor in (("precio de Sí", precio.get("precio_si")), ("precio esc. MALO", precio.get("precio_escenario_malo")), ("ponderado", precio.get("ponderado"))):
                if isinstance(valor, (int, float)):
                    formas = {f"{valor:.2f}", f"{valor:.1f}", f"{valor:.0f}"}
                    formas |= {f.replace(".", ",") for f in formas}
                    if not any(f in c104 for f in formas):
                        if acc in ("descartar", "demasiado_dificil") or est == "modelo_no_aplicable":
                            return f"C104 no lleva el {clave} de precio.json ({valor:.2f}) ni dice «sin escalera aplicable»"
                        return f"C104 no lleva el {clave} de precio.json ({valor:.2f})"
        return self.coherencia_v64(fc)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("carpeta")
    ap.add_argument("--config", default=None)  # (4.11) None → MUNGER_CONFIG o config_v2.json
    ap.add_argument("--agentes-simulados")
    ap.add_argument("--hasta", type=int, default=14)
    ap.add_argument("--reiniciar", action="store_true")
    ap.add_argument("--desde", type=int)
    a = ap.parse_args()
    cfg = config_v2.cargar(a.config)
    # (4.11) los scripts que lanza el pipeline cargan la MISMA configuración (plantilla, referencia y verificador elegidos con --config)
    os.environ["MUNGER_CONFIG"] = cfg["_ruta_config"]
    # (4.11) selección explícita de plantilla, referencia y configuración económica: un expediente solo se ejecuta con su plantilla;
    # la V6.4 exige configuracion_economica.json válida. Si no se cumple, se detiene con código 2.
    # (4.12 §3) Hasta la 4.11, SEL.comprobar terminaba ANTES de la vigencia: en una copia del piloto cerrado con PM1.lambda = 0.9
    # (configuración inválida) el pipeline devolvía 2 sin tocar nada y seguían concluido · APROBADO, con la ficha oficial y el cierre
    # registrado de un material que ya no era el auditado. Ahora se distingue:
    #   - material auditado alterado, ausente, ilegible o con archivos añadidos (configuración válida modificada, inválida, eliminada o
    #     ilegible; selección registrada alterada o borrada…): la vigencia, en lectura, da un motivo y se retiran PRIMERO la aprobación
    #     y sus publicaciones (archivar_salidas conserva los antecedentes y explica el motivo); después se detiene la llamada (código 2,
    #     o 5 si una retirada queda pendiente porque un resumen no se pudo actualizar);
    #   - material intacto y llamada con la plantilla equivocada (otra configuración, o archivos de plantilla, referencia o verificador
    #     distintos de las huellas registradas): se rechaza la llamada sin escribir nada en un expediente válido.
    # La selección, las huellas y el material nunca se reescriben antes de comprobar la vigencia (SEL.registrar va después).
    # (4.13 §3) la selección se comprueba con validación estructural explícita (seleccion_plantilla y configuracion_economica) y,
    # como segunda barrera, protegida: una excepción de estructura es un motivo, nunca una salida que deje la aprobación sin retirar
    m_sel, m_exc = ESTR.protegido(SEL.comprobar, a.carpeta, cfg, contexto="selección de plantilla")
    m_sel = m_sel or m_exc
    if m_sel:
        e0 = os.path.basename(os.path.abspath(a.carpeta))
        m_vig = CIE.motivo_vigencia(a.carpeta, Pipeline.veredicto_auditoria, e0)
        if not m_vig:
            print(f"SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}")
            return 2
        motivo, archivo = CIE.asegurar_vigencia(a.carpeta, Pipeline.veredicto_auditoria, e0, CIE.ruta_resumen(a.carpeta, cfg))
        pend = CIE.sincronizar_resumenes(a.carpeta, Pipeline.veredicto_auditoria, e0) or CIE.retiradas_pendientes(a.carpeta)
        print(f"APROBACIÓN RETIRADA ANTES DE DETENER LA LLAMADA: {motivo or m_vig}"
              + (f" · salidas oficiales archivadas en {os.path.relpath(archivo, a.carpeta)}" if archivo else ""))
        print(f"SELECCIÓN DE PLANTILLA DETENIDA: {m_sel}" + (f" · RETIRADA PENDIENTE en {pend} (ver {CIE.REGISTRO_RESUMEN})" if pend else ""))
        return 5 if pend else 2
    if a.reiniciar and os.path.exists(os.path.join(a.carpeta, "estado_pipeline.json")):
        os.remove(os.path.join(a.carpeta, "estado_pipeline.json"))
    try:
        p = Pipeline(a.carpeta, cfg, a.agentes_simulados)
    except (ValueError, OSError) as e:
        # (4.9, Z-2 de la auditoría interna; V-2 del control de vigencia: también si es una carpeta) estado_pipeline.json ilegible: el pipeline no puede continuar, pero antes retira una salida
        # oficial cerrada que ya no puede acreditarse (ficha, informe y filas de todos los destinos registrados del resumen)
        motivo, archivo = CIE.asegurar_vigencia(a.carpeta, Pipeline.veredicto_auditoria, os.path.basename(os.path.abspath(a.carpeta)), CIE.ruta_resumen(a.carpeta, cfg))
        pend = CIE.sincronizar_resumenes(a.carpeta, Pipeline.veredicto_auditoria) or CIE.retiradas_pendientes(a.carpeta)
        print(f"ESTADO DEL PIPELINE ILEGIBLE (estado_pipeline.json: {str(e)[:120]}): restaurarlo desde una copia o relanzar con --reiniciar."
              + (f" Salidas oficiales archivadas en {os.path.relpath(archivo, a.carpeta)}: {motivo}." if archivo else "")
              + (f" RETIRADA PENDIENTE en {pend}." if pend else ""))
        return 5 if pend else 6
    # vigencia (4.6.1): antes de nada, una salida oficial cerrada que ya no corresponde a una aprobación válida del material actual
    # se archiva como antecedente (historial_cierres/), con la fila del resumen y el estado del pipeline; nunca sigue como vigente
    motivo, archivo = CIE.asegurar_vigencia(p.c, p.veredicto_auditoria, p.E, CIE.ruta_resumen(p.c, cfg), p.st)
    if archivo:
        p.guardar()
        print(f"SALIDAS OFICIALES ARCHIVADAS ({os.path.relpath(archivo, p.c)}): {motivo}")
    # (4.7) la aprobación publicada se retira en todos los destinos registrados del resumen (también si ficha, informe y
    # cierre_vigente.json ya estaban archivados); un destino inaccesible deja la retirada pendiente y detiene con código 5
    pend = CIE.sincronizar_resumenes(p.c, p.veredicto_auditoria, p.E) or CIE.retiradas_pendientes(p.c)
    if pend:
        print(f"RETIRADA PENDIENTE de la aprobación publicada en {pend}: no se continúa hasta completarla (ver {CIE.REGISTRO_RESUMEN})")
        return 5
    # (4.11) primera ejecución con la V6.4: plantilla_activa.json (material auditado). (4.12 §3) después de la vigencia: la selección
    # no se escribe (ni se reescribe) antes de comprobar si la aprobación existente sigue valiendo
    SEL.registrar(p.c, cfg)
    if a.desde is None and p.st.get("estado_analisis") and p.st.get("resumen_pendiente"):
        # (4.8, Z-a) la fila del estado final no se pudo publicar en la ejecución anterior: se publica ahora que las retiradas están completas
        rc_res, out_res = p.run([PY, p.script("resumen.py"), p.c, CIE.ruta_resumen(p.c, cfg)])
        p.adoptar_archivo(conservar_estado=True)
        p.st["resumen_pendiente"] = rc_res != 0
        p.log(f"publicación pendiente del resumen: resumen.py → {rc_res}")
    if a.desde is not None:
        if p.st.get("estado_analisis") not in (None, "concluido"):
            # (4.8, Z-h) al reanudar desde un estado final, su diagnóstico pasa a antecedente (como se hace con concluido)
            for f in ("diagnostico.md", "diagnostico.json"):
                if os.path.exists(p.p(f)):
                    os.replace(p.p(f), p.p(f + ".anterior"))
        p.st["paso"] = a.desde
        p.st["estado_analisis"] = None
        p.st["esperando"] = None
        p.guardar()  # verificar_todo.sh lee estado_pipeline.json del disco: no debe ver el estado final de la ejecución anterior
    m_re = p.reaplicar_configuracion()  # (4.11) después de la vigencia (que ya retiró la aprobación si el material cambió)
    if m_re:
        p.terminar("no_entregable", "fallo_de_implementacion", m_re, p.st.get("paso") or 2, desde=2)
        print(f"estado final: {p.st.get('estado_analisis')} · {m_re[:200]}")
        return _pendientes_al_terminar(p, 0)
    try:
        p.correr(a.hasta)
    except Esperando as e:
        print(f"ESPERANDO: {e} (ver ESPERANDO.md y prompts_generados/)")
        return _pendientes_al_terminar(p, 10)
    except CierreRechazado as e:
        print(f"CIERRE RECHAZADO: {e}. No queda ninguna salida oficial vigente; el pipeline vuelve al paso 13 (auditoría).")
        return _pendientes_al_terminar(p, 4)
    except CIE.RegistroAuditoriasIlegible as e:
        # (4.8.1, V-9 del control de vigencia) falla del lado seguro, con un motivo explícito
        print(f"REGISTRO DE AUDITORÍAS ILEGIBLE: {e}")
        return 6
    if os.path.exists(p.p("ESPERANDO.md")) and p.st.get("esperando") is None:
        os.remove(p.p("ESPERANDO.md"))
    causa = ""
    dg = json.load(open(p.p("diagnostico.json"), encoding="utf-8")) if p.st.get("estado_analisis") not in (None, "concluido") and os.path.exists(p.p("diagnostico.json")) else {}
    if dg and dg.get("estado_analisis") == p.st.get("estado_analisis"):
        # (4.8, X-c) la última línea dice también la causa y por dónde se sigue (diagnostico.md); (V-a del control de vigencia) solo
        # con un diagnóstico del mismo estado final, nunca sin estado
        causa = (f" · causa: {(dg.get('causa') or {}).get('tipo')}: {(str((dg.get('causa') or {}).get('detalle') or '').splitlines() or [''])[0][:140]}"
                 f" · continuar desde el paso {(dg.get('para_continuar') or {}).get('desde_que_paso')} (ver diagnostico.md)")
    print(f"estado final: {p.st.get('estado_analisis')} · paso {p.st['paso']}{causa}")
    return _pendientes_al_terminar(p, 0)


def _pendientes_al_terminar(p, rc):
    """(4.7, H-9 de la auditoría interna) una retirada pendiente nacida DENTRO de la ejecución (paso 11, rechazo del paso 14,
    resumen.py en las salidas finales) también detiene con código 5."""
    pend = CIE.retiradas_pendientes(p.c)
    if pend:
        print(f"RETIRADA PENDIENTE de la aprobación publicada en {pend} (ver {CIE.REGISTRO_RESUMEN}); código {rc} sustituido por 5")
        return 5
    return rc


if __name__ == "__main__":
    sys.exit(main())
