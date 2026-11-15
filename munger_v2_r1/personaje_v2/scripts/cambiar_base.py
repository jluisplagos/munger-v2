#!/usr/bin/env python3
"""Cambio de base económica de un expediente: mecanismo general y reutilizable (encargo 4.11 §7; propuesta D-REBASE de la 4.10.1).

Uso (desde munger_v2_r1/):
  cambiar_base.py preparar CAMBIO.json        → crea el expediente de ensayo nuevo (nunca sobrescribe)
  cambiar_base.py comprobar CAMBIO.json [LIBRO] → concordancia de las entradas y búsqueda de restos (después del pipeline, sobre
                                                  el libro de datos o el evaluado); código 0 si concuerda y no hay restos
CAMBIO.json (formato v1; ver ESQUEMA más abajo) declara qué entradas sustituye, con valor, fecha, fuente, unidad, perímetro,
derivación y naturaleza, qué evidencias reescribe y qué notas retira. El script:
  1. copia el expediente de ORIGEN (que no se toca) a DESTINO; conserva solo las entradas de partida (`conservar`) y mueve todo lo
     demás a ANTECEDENTES con inventario y huellas (ningún cierre, fase, publicación ni estado del pipeline se hereda);
  2. deja en etapa1/ una COPIA DE ENSAYO del libro de la etapa 1 (el original va a antecedentes con su huella) en la que, a nivel XML:
     - se vacían los valores de las celdas de dato que se sustituyen (`analisis.*.vaciar_en_etapa1`), para que la fase 1 no las pierda
       ante un valor migrado (rellenar_fase1_v63.py no pisa un valor migrado: regla de producción que no cambia);
     - se escribe la evidencia ACTIVA nueva de Control maestro (columnas declaradas de E:N) de cada celda sustituida o limpiada; los
       textos anteriores quedan en antecedentes (evidencia_anterior.json). Ninguna otra celda cambia (se comprueba);
  3. escribe fase1_metadatos.json desde el de origen con las entradas de `metadatos` (precio, acciones, capitalización, tasa sin
     riesgo, fecha de análisis = fecha REAL de ejecución) y quita las notas que casan con `notas_que_se_retiran` (a antecedentes);
  4. reconstruye fase1_v63.json con fase1_historia.py construir y le aplica `analisis` (valor, fuente, página, periodo, unidad), sin
     las notas retiradas;
  5. escribe alcance_v2.json y, si se declara, configuracion_economica.json (V6.4 experimental);
  6. registra todo en DESTINO/../resultados/cambio_de_base.json y .md.
Aislamiento: el expediente nuevo no tiene estado_pipeline.json, publicaciones ni perfil de LibreOffice; su resumen es el de su carpeta
(`resumen_v2.csv` junto al expediente; con la V6.4, `resumen_v2_v64_experimental.csv`). Fechas separadas: fecha real de ejecución (D4), base económica, fecha del precio y de las acciones
y publicación de las fuentes. Repetir la preparación en otro destino da las mismas entradas activas (se comprueba en la batería).
"""
import copy
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import zipfile

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
sys.path.insert(0, AQUI)
from v63_xml import LibroV63  # noqa: E402

ESQUEMA = {
    "tipo": "cambio_de_base", "version_formato": 1, "empresa": "carpeta del expediente (p. ej. Vidrala)",
    "origen": "ruta (desde munger_v2_r1/) del expediente de origen", "destino": "ruta del ensayo nuevo (carpeta que contendrá <empresa>/)",
    "base_economica": {"fecha": "AAAA-MM-DD", "descripcion": "…"},
    "fechas": {"ejecucion": "«real» (fecha del día) o AAAA-MM-DD", "precio": "…", "acciones": "…", "publicacion_fuentes": "…"},
    "conservar": ["etapa1", "texto", "fase1_partes", "fase1_decisiones.json", "fase1_fuentes.json"],
    "fuentes_adicionales": [{"pdf": "ruta", "sha256": "…", "texto": "texto/<nombre>.txt"}],
    "metadatos": {"precio": {}, "acciones_diluidas": {}, "capitalizacion": {}, "tasa_sin_riesgo": {}},
    "notas_que_se_retiran": ["patrón regex", "…"],
    "correcciones_fase1_partes": [{"archivo": "AR_2025.json", "partida": "pensiones", "lado": "actual|anterior", "indice": 0,
                                   "esperado": {"impreso": "valor impreso que debe encontrarse"}, "nuevo": {"concepto": "…", "impreso": "…", "pagina": 0, "linea": "…"},
                                   "fuente": "documento, página y línea", "motivo": "por qué la extracción estaba mal"}],
    "analisis": {"C24": {"valor": 0, "fuente": "…", "pagina": "…", "periodo": "…", "unidad": "…", "vaciar_en_etapa1": True, "evidencia": {"M": "…", "N": "…"}}},
    "evidencia": {"Análisis!C28": {"N": "…"}},
    "control_maestro_textos": {"F5": "(4.15) texto de la cabecera del período", "D88": "(4.15) texto de la lista de comprobación C86:E102"},
    "textos_prohibidos": ["patrón regex de restos de la base anterior que no puede quedar en la evidencia activa ni en las notas"],
    "alcance": {}, "configuracion_economica": "objeto o null",
    "analisis_que_se_conservan": {"C49": "(4.15) motivo por el que se conserva una entrada `analisis` de los metadatos del origen"},
    "analisis_que_se_descartan": {"C42": "(4.15) motivo por el que se descarta"},
    "entrada_efectiva": {"modo": "estricta (por defecto) | registrada", "motivo": "obligatorio con «registrada»"},
}
ENTRADA_EFECTIVA = "entrada_efectiva.json"


def validar_conf(conf):
    """(4.15, segunda revisión independiente, N5 y N7) Comprobaciones del CAMBIO antes de crear nada: motivos no vacíos, ninguna celda en
    dos listas y el modo de la entrada efectiva."""
    faltas = []
    dec = set((conf.get("analisis") or {}))
    for nombre in ("analisis_que_se_conservan", "analisis_que_se_descartan"):
        d = conf.get(nombre) or {}
        if not isinstance(d, dict):
            faltas.append(f"{nombre} tiene que ser un objeto {{celda: motivo}}")
            continue
        faltas += [f"{nombre}: {c} sin motivo" for c, m in d.items() if not str(m or "").strip()]
    cons, desc = set(conf.get("analisis_que_se_conservan") or {}), set(conf.get("analisis_que_se_descartan") or {})
    for a_, b_, n_ in ((dec, cons, "analisis y analisis_que_se_conservan"), (dec, desc, "analisis y analisis_que_se_descartan"),
                       (cons, desc, "analisis_que_se_conservan y analisis_que_se_descartan")):
        if a_ & b_:
            faltas.append(f"celdas a la vez en {n_}: {', '.join(sorted(a_ & b_))}")
    ee = conf.get("entrada_efectiva")
    if ee is not None:
        if not isinstance(ee, dict) or ee.get("modo") not in ("estricta", "registrada"):
            faltas.append("entrada_efectiva tiene que ser {\"modo\": \"estricta\" | \"registrada\", \"motivo\": …}")
        elif ee.get("modo") == "registrada" and not str(ee.get("motivo") or "").strip():
            faltas.append("entrada_efectiva «registrada» sin motivo (el modo por defecto de un expediente nuevo es «estricta»)")
    if faltas:
        raise SystemExit("CAMBIO NO VÁLIDO (no se ha creado nada): " + " | ".join(faltas))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def ruta(p):
    return p if os.path.isabs(p) else os.path.join(RAIZ, p)


def texto_con_marcas(pdf, txt):
    tmp = txt + ".tmp"
    subprocess.run(["pdftotext", "-layout", pdf, tmp], check=True)
    paginas = open(tmp, encoding="utf-8", errors="replace").read().split("\f")
    if paginas and not paginas[-1].strip():
        paginas = paginas[:-1]
    open(txt, "w", encoding="utf-8").write("".join(f"[PDF PAGE {i}]\n{p.rstrip()}\n\n" for i, p in enumerate(paginas, 1)))
    os.remove(tmp)


def fila_de(libro, hoja_cm, celda):
    """Fila de Control maestro cuya columna B nombra la celda (p. ej. «Análisis!C41»)."""
    for r in range(17, 200):
        if libro.leer(hoja_cm, f"B{r}") == celda:
            return r
    return None


def preparar(conf):
    validar_conf(conf)
    origen = ruta(conf["origen"])
    ens = ruta(conf["destino"])
    emp = conf["empresa"]
    dest = os.path.join(ens, emp)
    ant = os.path.join(ens, "antecedentes")
    res = os.path.join(ens, "resultados")
    if os.path.exists(dest) or os.path.exists(os.path.join(ant, "heredados")):
        raise SystemExit(f"ya existe {os.path.relpath(dest, RAIZ)} o sus antecedentes: no se sobrescribe (borrar a mano para regenerar)")
    os.makedirs(os.path.join(ant, "heredados"))
    os.makedirs(res, exist_ok=True)
    shutil.copytree(origen, dest, ignore=shutil.ignore_patterns(".lo_perfil", "__pycache__"))
    conservar = set(conf.get("conservar") or [])
    inv = []
    for n in sorted(os.listdir(dest)):
        if n in conservar:
            continue
        shutil.move(os.path.join(dest, n), os.path.join(ant, "heredados", n))
    for r, ds, fs in os.walk(os.path.join(ant, "heredados")):
        for f in fs:
            p = os.path.join(r, f)
            inv.append({"archivo": os.path.relpath(p, os.path.join(ant, "heredados")), "sha256": sha(p)})
    json.dump({"origen": conf["origen"], "nota": "Productos del expediente de origen que no son entradas de partida: antecedentes sin cambios; ninguno está en una ruta activa.",
               "archivos": inv}, open(os.path.join(ant, "INVENTARIO_HEREDADOS.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # --- fuentes adicionales
    adicionales = []
    for fa in conf.get("fuentes_adicionales") or []:
        pdf = ruta(fa["pdf"])
        if fa.get("sha256") and sha(pdf) != fa["sha256"]:
            raise SystemExit(f"la fuente {fa['pdf']} no tiene la huella declarada")
        txt = os.path.join(dest, fa["texto"])
        texto_con_marcas(pdf, txt)
        adicionales.append({"pdf": fa["pdf"], "pdf_sha256": sha(pdf), "texto": fa["texto"], "texto_sha256": sha(txt)})
    # --- etapa 1: original a antecedentes; copia de ensayo con los datos vaciados y la evidencia nueva
    e1_dir = os.path.join(dest, "etapa1")
    libros = [f for f in os.listdir(e1_dir) if f.endswith(".xlsx")]
    if len(libros) != 1:
        raise SystemExit(f"etapa1/ debe tener exactamente un libro (tiene {libros})")
    e1 = os.path.join(e1_dir, libros[0])
    os.makedirs(os.path.join(ant, "etapa1_original"))
    e1_orig = os.path.join(ant, "etapa1_original", libros[0])
    shutil.copy2(e1, e1_orig)
    lb = LibroV63(e1_orig)
    anteriores, escritas, vaciadas = {}, {}, []
    for celda, d in (conf.get("analisis") or {}).items():
        if d.get("vaciar_en_etapa1"):
            anteriores[f"Análisis!{celda}"] = lb.leer("Análisis", celda)
            lb.escribir("Análisis", celda, None)
            lb.marcar_modificada("Análisis")
            vaciadas.append(f"Análisis!{celda}")
    evid = {f"Análisis!{c}": d.get("evidencia") or {} for c, d in (conf.get("analisis") or {}).items() if d.get("evidencia")}
    for c, cols in (conf.get("evidencia") or {}).items():
        evid.setdefault(c, {}).update(cols)
    for celda, cols in evid.items():
        r = fila_de(lb, "Control maestro", celda)
        if r is None:
            raise SystemExit(f"la etapa 1 no tiene fila de Control maestro para {celda}")
        for col, texto in cols.items():
            if col not in "EFGHIJKLMN" or len(col) != 1:
                raise SystemExit(f"columna de evidencia no permitida: {col} ({celda})")
            ref = f"{col}{r}"
            anteriores[f"Control maestro!{ref}"] = lb.leer("Control maestro", ref)
            lb.escribir("Control maestro", ref, texto, tipo="texto" if isinstance(texto, str) else None)
            escritas[f"Control maestro!{ref}"] = {"celda": celda, "texto": texto}
        lb.marcar_modificada("Control maestro")
    lb.guardar(e1)
    # comprobación: solo cambian las celdas declaradas (las demás, iguales en valor)
    import openpyxl
    w_o, w_n = openpyxl.load_workbook(e1_orig, data_only=True), openpyxl.load_workbook(e1, data_only=True)
    cambiadas = set(vaciadas) | set(escritas)
    otras = [f"{h}!{c.coordinate}" for h in w_o.sheetnames for fila in w_o[h].iter_rows() for c in fila
             if f"{h}!{c.coordinate}" not in cambiadas and w_n[h][c.coordinate].value != c.value]
    if otras:
        raise SystemExit(f"la copia de ensayo de la etapa 1 cambia celdas no declaradas: {otras[:10]}")
    zo, zn = zipfile.ZipFile(e1_orig), zipfile.ZipFile(e1)
    miembros = sorted(i.filename for i in zo.infolist() if zo.read(i.filename) != zn.read(i.filename))
    json.dump({"etapa1_original": os.path.relpath(e1_orig, ens), "valores_y_textos_anteriores": anteriores},
              open(os.path.join(ant, "evidencia_anterior.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    # --- metadatos
    patrones = [re.compile(p) for p in conf.get("notas_que_se_retiran") or []]
    retiradas = []
    meta = json.load(open(os.path.join(ant, "heredados", "fase1_metadatos.json"), encoding="utf-8"))
    hoy = dt.date.today().isoformat()
    fe = (conf.get("fechas") or {}).get("ejecucion") or "real"
    meta["fecha_analisis"] = hoy if fe == "real" else fe
    for k, v in (conf.get("metadatos") or {}).items():
        meta[k] = v
    # (4.15, X2/H-P1) textos declarativos del Control maestro (F5 y C86:E102) que la etapa 1 trae con fechas, períodos o cifras que ya no son
    # los del expediente: van a las entradas declaradas (fase1_metadatos.json → fase1_v63.json → rellenar_fase1_v63.py, que conserva el anterior)
    if conf.get("control_maestro_textos"):
        meta["control_maestro_textos"] = dict(conf["control_maestro_textos"])
    # (4.15, revisión independiente, hallazgo 8) entradas `analisis` ya declaradas en los metadatos del ORIGEN (cambios de base de la 4.15):
    # no se heredan en silencio. El CAMBIO las vuelve a declarar, las descarta (`analisis_que_se_descartan`, y se quitan) o las reconoce
    # expresamente (`analisis_que_se_conservan`, {celda: motivo}); si no, se detiene la preparación.
    descartes_m = conf.get("analisis_que_se_descartan") or {}
    conservadas_m = conf.get("analisis_que_se_conservan") or {}
    heredadas = {c: v for c, v in (meta.get("analisis") or {}).items() if c not in (conf.get("analisis") or {})}
    sin_reconocer = sorted(c for c in heredadas if c not in descartes_m and c not in conservadas_m)
    ajenas = sorted(c for c in conservadas_m if c not in heredadas)
    if ajenas:  # (4.15, N5) solo se reconoce lo que de verdad se hereda
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(ant, ignore_errors=True)
        raise SystemExit("PREPARACIÓN DETENIDA: `analisis_que_se_conservan` reconoce entradas que los metadatos del origen no declaran (se retira el destino): "
                         + ", ".join(ajenas))
    if sin_reconocer:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(ant, ignore_errors=True)
        raise SystemExit("PREPARACIÓN DETENIDA: los metadatos del origen declaran entradas `analisis` que el CAMBIO no declara, no descarta ni reconoce "
                         f"(se retira el destino): {', '.join(sin_reconocer)}. Declárelas en `analisis`, en `analisis_que_se_descartan` o en `analisis_que_se_conservan` con su motivo.")
    for c in descartes_m:
        (meta.get("analisis") or {}).pop(c, None)
    # (4.15, C48 de Elis) las entradas `analisis` del CAMBIO quedan también en las ENTRADAS DECLARADAS del expediente (fase1_metadatos.json),
    # con su cálculo si lo declaran: `fase1_historia.py construir` las reproduce en una carpeta limpia sin depender del CAMBIO ni de un valor migrado
    for celda, d in (conf.get("analisis") or {}).items():
        if d.get("derivada"):
            continue
        ent_m = {k: d.get(k) for k in ("valor", "fuente", "pagina", "periodo", "unidad") if d.get(k) is not None}
        if isinstance(d.get("calculo"), dict):
            ent_m["calculo"] = d["calculo"]
        meta.setdefault("analisis", {})[celda] = ent_m
    notas = meta.get("_notas") or []
    meta["_notas"] = [n for n in notas if not any(p.search(str(n)) for p in patrones)] + ([conf["nota_metadatos"]] if conf.get("nota_metadatos") else [])
    retiradas += [{"de": "fase1_metadatos.json", "nota": n} for n in notas if any(p.search(str(n)) for p in patrones)]
    json.dump(meta, open(os.path.join(dest, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # --- (4.14, decisión E6 de Elis) correcciones de EXTRACCIÓN en fase1_partes/ (la Historia la construye fase1_historia.py desde
    # ellas): cada corrección declara archivo, partida, lado (actual|anterior), índice, el valor impreso que espera encontrar y la entrada
    # nueva con su fuente; si lo encontrado no es lo esperado, se detiene y retira el destino. Los originales van a antecedentes.
    corregidas_partes = []
    if conf.get("correcciones_fase1_partes"):
        partes = os.path.join(dest, "fase1_partes")
        if not os.path.isdir(partes):
            shutil.rmtree(dest, ignore_errors=True)
            shutil.rmtree(ant, ignore_errors=True)
            raise SystemExit("PREPARACIÓN DETENIDA: hay correcciones_fase1_partes pero fase1_partes no está en `conservar`")
        orig_partes = os.path.join(ant, "fase1_partes_original")
        os.makedirs(orig_partes, exist_ok=True)
        for c in conf["correcciones_fase1_partes"]:
            arch = os.path.join(partes, c["archivo"])
            if not os.path.exists(os.path.join(orig_partes, c["archivo"])):
                shutil.copy2(arch, os.path.join(orig_partes, c["archivo"]))
            d = json.load(open(arch, encoding="utf-8"))
            lista = ((d.get("partidas") or {}).get(c["partida"]) or {}).get(c["lado"])
            i = int(c.get("indice", 0))
            ent = lista[i] if isinstance(lista, list) and len(lista) > i else None
            esperado = (c.get("esperado") or {}).get("impreso")
            nuevo = c.get("nuevo") or {}
            if ent is None or esperado is None or str(ent.get("impreso")) != str(esperado) or not nuevo.get("impreso") or not nuevo.get("pagina") \
                    or not str(c.get("fuente") or "").strip() or not str(c.get("motivo") or "").strip():
                shutil.rmtree(dest, ignore_errors=True)
                shutil.rmtree(ant, ignore_errors=True)
                raise SystemExit(f"PREPARACIÓN DETENIDA: corrección de fase1_partes no aplicable ({c.get('archivo')} · {c.get('partida')} · {c.get('lado')}[{i}]): "
                                 f"se esperaba impreso {esperado!r} y hay {None if ent is None else ent.get('impreso')!r}, o falta la entrada nueva, la fuente o el motivo")
            lista[i] = dict(nuevo)
            nota_antes = None
            if c.get("nota_partida") is not None:
                # la nota de la partida (pasa a la columna de notas de la Historia) se sustituye si la corrección lo declara
                nota_antes = d["partidas"][c["partida"]].get("nota")
                d["partidas"][c["partida"]]["nota"] = c["nota_partida"]
            corregidas_partes.append({"archivo": c["archivo"], "partida": c["partida"], "lado": c["lado"], "indice": i, "antes": ent, "despues": nuevo,
                                      "nota_antes": nota_antes, "nota_despues": c.get("nota_partida"), "fuente": c["fuente"], "motivo": c["motivo"]})
            json.dump(d, open(arch, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # (4.15, hallazgo 8c) lo que daría la Historia sin las entradas declaradas por el CAMBIO (diagnóstico de §3: qué sostiene cada entrada)
    meta_hist = copy.deepcopy(meta)
    for c in list((meta_hist.get("analisis") or {})):
        if c in (conf.get("analisis") or {}):
            meta_hist["analisis"].pop(c)
    # (4.15, tercera revisión, T5) el modo de la entrada efectiva queda también en las entradas declaradas: sin su archivo, el pipeline se detiene
    meta["entrada_efectiva"] = (conf.get("entrada_efectiva") or {}).get("modo") or "estricta"
    construido_historia, diagnostico_historia = {}, False
    json.dump(meta_hist, open(os.path.join(dest, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    _r0 = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "fase1_historia.py"), "construir", dest], capture_output=True, text=True)
    if _r0.returncode == 0 and os.path.exists(os.path.join(dest, "fase1_v63.json")):
        construido_historia = {c: (v.get("valor") if isinstance(v, dict) else v)
                               for c, v in (json.load(open(os.path.join(dest, "fase1_v63.json"), encoding="utf-8")).get("analisis") or {}).items()}
        os.remove(os.path.join(dest, "fase1_v63.json"))
        diagnostico_historia = True
    json.dump(meta, open(os.path.join(dest, "fase1_metadatos.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # --- fase1_v63.json: reconstrucción y entradas declaradas
    r = subprocess.run([sys.executable, "-B", os.path.join(AQUI, "fase1_historia.py"), "construir", dest], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("fase1_historia.py construir falló: " + (r.stdout + r.stderr)[-600:])
    f1p = os.path.join(dest, "fase1_v63.json")
    f1 = json.load(open(f1p, encoding="utf-8"))
    sustituidas = {}
    for celda, d in (conf.get("analisis") or {}).items():
        if d.get("derivada"):
            continue
        antes = (f1.get("analisis", {}).get(celda) or {}).get("valor")
        if isinstance(d.get("calculo"), dict):
            # (4.15) con cálculo declarado, el valor lo calcula `construir` desde las entradas declaradas: no se sustituye por una constante
            calc = (f1.get("analisis") or {}).get(celda) or {}
            sustituidas[celda] = {"construido_por_fase1_historia": construido_historia.get(celda), "valor": calc.get("valor"), "naturaleza": d.get("naturaleza"),
                                  "perimetro": d.get("perimetro"), "fecha": d.get("fecha"), "derivacion": d.get("derivacion"), "calculo": d["calculo"]}
            continue
        f1.setdefault("analisis", {})[celda] = {"valor": d["valor"], "fuente": d["fuente"], "pagina": d.get("pagina"), "periodo": d.get("periodo"), "unidad": d.get("unidad")}
        # (4.15, N5) si la construcción de diagnóstico terminó bien, lo que da la Historia (None si no la construye); si no, se dice
        sustituidas[celda] = {"construido_por_fase1_historia": construido_historia.get(celda) if diagnostico_historia else "(sin diagnóstico: la construcción sin el CAMBIO falló)", "valor": d["valor"], "naturaleza": d.get("naturaleza"), "perimetro": d.get("perimetro"),
                              "fecha": d.get("fecha"), "derivacion": d.get("derivacion")}
    # (4.14, incidente del 14-nov-2026) una entrada `analisis` del ORIGEN que el CAMBIO no declara y que `construir` no reproduce con el
    # mismo valor se perdería en silencio (p. ej. entradas reexpresadas de un cambio de base anterior). Se detiene la preparación, salvo
    # que el CAMBIO la descarte de forma explícita en `analisis_que_se_descartan` ({celda: motivo}); el destino creado se retira.
    f1_origen = {}
    try:
        f1_origen = json.load(open(os.path.join(origen, "fase1_v63.json"), encoding="utf-8"))
    except (OSError, ValueError):
        pass
    descartes = conf.get("analisis_que_se_descartan") or {}
    _v = lambda d: d.get("valor") if isinstance(d, dict) else d  # noqa: E731
    perdidas = []
    for celda, d in (f1_origen.get("analisis") or {}).items():
        if celda in (conf.get("analisis") or {}) or celda in descartes:
            continue
        v0, v1 = _v(d), _v((f1.get("analisis") or {}).get(celda))
        igual = (v0 == v1) or (isinstance(v0, (int, float)) and isinstance(v1, (int, float)) and abs(v0 - v1) <= 1e-9 * max(1.0, abs(v0)))
        if not igual:
            perdidas.append(f"Análisis!{celda}: origen {v0!r} → {v1!r}")
    if perdidas:
        shutil.rmtree(dest, ignore_errors=True)
        shutil.rmtree(ant, ignore_errors=True)
        raise SystemExit("PREPARACIÓN DETENIDA: el CAMBIO perdería entradas `analisis` del origen que no declara ni descarta (se retira el destino): "
                         + "; ".join(perdidas) + ". Declárelas en `analisis` (para conservarlas) o en `analisis_que_se_descartan` con su motivo.")
    if descartes:
        retiradas.append({"de": "fase1_v63.json (analisis del origen descartadas por el CAMBIO)", "nota": descartes})
    notas = f1.get("_notas") or []
    f1["_notas"] = [n for n in notas if not any(p.search(str(n)) for p in patrones)]
    retiradas += [{"de": "fase1_v63.json", "nota": n} for n in notas if any(p.search(str(n)) for p in patrones)]
    f1["_notas"].append(f"(cambio de base, {conf['base_economica']['fecha']}) Entradas sustituidas por cambiar_base.py desde {os.path.basename(conf.get('_archivo', 'CAMBIO.json'))}: "
                        + "; ".join(f"{c} {x['construido_por_fase1_historia']!r} → {x['valor']!r}" for c, x in sustituidas.items()))
    json.dump(f1, open(f1p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    json.dump({"retiradas": retiradas}, open(os.path.join(ant, "notas_retiradas.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if conf.get("alcance"):
        json.dump(conf["alcance"], open(os.path.join(dest, "alcance_v2.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    # (4.15, segunda revisión independiente, N7) todo expediente nuevo declara su modo de entrada efectiva; por defecto «estricta»: el
    # pipeline pasa --estricta a rellenar_fase1_v63.py y una entrada del FCF base que solo sostiene un valor migrado detiene el relleno
    ee = dict(conf.get("entrada_efectiva") or {"modo": "estricta"})
    ee = {"formato": "4.15", "modo": ee["modo"], "motivo": ee.get("motivo") or "expediente nuevo de la 4.15 (modo por defecto)",
          "declarado_por": "cambiar_base.py", "cambio": os.path.basename(conf.get("_archivo") or "CAMBIO.json")}
    json.dump(ee, open(os.path.join(dest, ENTRADA_EFECTIVA), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    if conf.get("configuracion_economica"):
        import configuracion_economica as CE
        faltas = CE.validar(conf["configuracion_economica"])
        if faltas:
            raise SystemExit("configuracion_economica no válida: " + " | ".join(faltas))
        json.dump(conf["configuracion_economica"], open(os.path.join(dest, "configuracion_economica.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    reg = {"cambio": conf.get("_archivo"), "cambio_sha256": conf.get("_sha256"), "origen": conf["origen"], "destino": os.path.relpath(dest, RAIZ),
           "base_economica": conf["base_economica"], "fechas": {**(conf.get("fechas") or {}), "ejecucion_aplicada": meta["fecha_analisis"]},
           "heredados_movidos": len(inv), "conservados": sorted(conservar), "fuentes_adicionales": adicionales,
           "etapa1": {"original": os.path.relpath(e1_orig, ens), "original_sha256": sha(e1_orig), "copia_de_ensayo_sha256": sha(e1), "miembros_cambiados": miembros,
                      "vaciadas": vaciadas, "evidencia_escrita": escritas},
           "sustituidas_en_fase1_v63": sustituidas, "correcciones_fase1_partes": corregidas_partes, "notas_retiradas": len(retiradas),
           "configuracion_economica": bool(conf.get("configuracion_economica")), "alcance": bool(conf.get("alcance")),
           "analisis_heredadas_conservadas": dict(conservadas_m), "analisis_descartadas": dict(descartes_m), "entrada_efectiva": ee}
    json.dump(reg, open(os.path.join(res, "cambio_de_base.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Cambio de base económica · {emp} · base {conf['base_economica']['fecha']}", "", conf["base_economica"].get("descripcion", ""), "",
          f"- Origen `{conf['origen']}` (sin cambios) → expediente nuevo `{reg['destino']}`; {len(inv)} archivos heredados en `antecedentes/heredados/` con inventario.",
          f"- Etapa 1: original en `{reg['etapa1']['original']}` (SHA-256 `{reg['etapa1']['original_sha256'][:16]}…`); copia de ensayo `{reg['etapa1']['copia_de_ensayo_sha256'][:16]}…`, cambian {', '.join(miembros)}.",
          f"- Valores de dato vaciados en la copia (los da la fase 1): {', '.join(vaciadas) or 'ninguno'}.",
          f"- Evidencia activa reescrita (Control maestro): {len(escritas)} celdas en {len({x['celda'] for x in escritas.values()})} filas — "
          + "; ".join(f"{c} ({''.join(sorted(k.split('!')[1][0] for k, x in escritas.items() if x['celda'] == c))})" for c in sorted({x['celda'] for x in escritas.values()}))
          + ". Los textos anteriores están en `antecedentes/evidencia_anterior.json`.",
          f"- Entradas sustituidas en fase1_v63.json: " + "; ".join(f"{c} → {x['valor']!r}" for c, x in sustituidas.items()),
          f"- Correcciones de extracción en fase1_partes (antes de construir la Historia; originales en `antecedentes/fase1_partes_original/`): "
          + ("; ".join(f"{x['archivo']} · {x['partida']} · {x['lado']} {x['antes'].get('impreso')!r} → {x['despues'].get('impreso')!r}" for x in corregidas_partes) or "ninguna"),
          f"- Notas retiradas de los metadatos y de fase1_v63.json: {len(retiradas)} (`antecedentes/notas_retiradas.json`).",
          f"- Fechas: ejecución {meta['fecha_analisis']} (real) · base {conf['base_economica']['fecha']} · precio {(conf.get('fechas') or {}).get('precio')} · acciones {(conf.get('fechas') or {}).get('acciones')} · fuentes: {(conf.get('fechas') or {}).get('publicacion_fuentes')}.",
          f"- Configuración económica V6.4: {'sí' if conf.get('configuracion_economica') else 'no'} · alcance: {'sí' if conf.get('alcance') else 'no'}.",
          f"- Entradas `analisis` heredadas de los metadatos del origen que se conservan: " + ("; ".join(f"{c} ({m})" for c, m in conservadas_m.items()) or "ninguna")
          + " · que se descartan: " + ("; ".join(f"{c} ({m})" for c, m in descartes_m.items()) or "ninguna") + ".",
          f"- Entrada efectiva del FCF base: «{ee['modo']}» (`{ENTRADA_EFECTIVA}`; {ee['motivo']})."]
    open(os.path.join(res, "cambio_de_base.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return reg


def comprobar(conf, libro=None):
    """Concordancia de las entradas declaradas y búsqueda de restos en la evidencia activa y en las notas."""
    import openpyxl
    ens = ruta(conf["destino"])
    dest = os.path.join(ens, conf["empresa"])
    libro = libro or os.path.join(dest, f"{conf['empresa']}_v63_datos.xlsx")
    wb = openpyxl.load_workbook(libro, data_only=True)
    an, cm = wb["Análisis"], wb["Control maestro"]
    f1 = json.load(open(os.path.join(dest, "fase1_v63.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(dest, "fase1_metadatos.json"), encoding="utf-8"))
    filas = []
    for celda, d in (conf.get("analisis") or {}).items():
        v_l = an[celda].value
        v_f = (f1.get("analisis", {}).get(celda) or {}).get("valor")
        # (4.15) con cálculo declarado y sin valor fijo, lo esperado es lo que calcula `construir` (y tiene que estar en el libro)
        esp = d["valor"] if "valor" in d else (v_f if isinstance(d.get("calculo"), dict) else None)
        ok = esp is not None and ((v_l == esp) or (isinstance(v_l, (int, float)) and isinstance(esp, (int, float)) and abs(v_l - esp) < 1e-9))
        ok = ok and (d.get("derivada") or v_f == esp)
        filas.append({"celda": f"Análisis!{celda}", "configuracion": esp, "fase1_v63": v_f if not d.get("derivada") else "(derivada)", "libro": v_l, "concuerda": bool(ok)})
    for clave, celda in (("precio", "C37"), ("capitalizacion", "C41"), ("acciones_diluidas", "C55"), ("tasa_sin_riesgo", "C57")):
        if clave in (conf.get("metadatos") or {}):
            esperado = conf["metadatos"][clave]["valor"]
            v_l = an[celda].value
            filas.append({"celda": f"Análisis!{celda}", "configuracion": esperado, "fase1_metadatos": meta.get(clave, {}).get("valor"), "libro": v_l,
                          "concuerda": isinstance(v_l, (int, float)) and abs(v_l - esperado) < 1e-9 and meta.get(clave, {}).get("valor") == esperado})
    prohibidos = [re.compile(p) for p in conf.get("textos_prohibidos") or []]
    restos = []
    filas_activas = list(range(17, 83)) + list(range(107, 176))
    import celdas_v2
    juicio = set(celdas_v2.FILAS_CM)
    for r in filas_activas:
        b = cm[f"B{r}"].value
        # en las filas de juicio, E, F y N las escriben las fases (pueden citar la etapa 1 al explicar la herencia): se revisan G:M,
        # que vienen de la etapa 1 y ninguna fase reescribe; en las filas de dato, toda la evidencia E:N
        for col in ("GHIJKLM" if r in juicio else "EFGHIJKLMN"):
            v = cm[f"{col}{r}"].value
            if isinstance(v, str) and any(p.search(v) for p in prohibidos):
                restos.append({"celda": f"Control maestro!{col}{r}", "de": b, "texto": v[:200]})
    # (4.11, revisión interna H9) fuera de la evidencia activa (cabecera y bloque de auditoría heredado de la etapa 1, filas 84–106 y
    # 176 en adelante): se informa, sin contar para el resultado, porque esas filas no son la evidencia de ninguna entrada activa
    informativos = []
    for r in range(1, cm.max_row + 1):
        if r in filas_activas:
            continue
        for col in "ABCDEFGHIJKLMN":
            v = cm[f"{col}{r}"].value
            if isinstance(v, str) and any(p.search(v) for p in prohibidos):
                informativos.append({"celda": f"Control maestro!{col}{r}", "texto": v[:200]})
    for nombre, obj in (("fase1_metadatos.json", meta), ("fase1_v63.json", f1)):
        for i, n in enumerate(obj.get("_notas") or []):
            if any(p.search(str(n)) for p in prohibidos):
                restos.append({"celda": f"{nombre} → _notas[{i}]", "texto": str(n)[:200]})
    fechas = {"Análisis!D4 (fecha de análisis)": an["D4"].value, "Palancas!C45 (fecha del precio)": wb["Palancas"]["C45"].value, "Palancas!C46 (fecha de las acciones)": wb["Palancas"]["C46"].value}
    ok = all(x["concuerda"] for x in filas) and not restos
    out = {"libro": os.path.relpath(libro, RAIZ), "concordancia": filas, "restos_de_la_base_anterior": restos,
           "textos_de_la_base_anterior_fuera_de_la_evidencia_activa": informativos, "fechas": {k: str(v) for k, v in fechas.items()},
           "resultado": "CONCUERDA Y SIN RESTOS" if ok else "NO CONCUERDA O QUEDAN RESTOS"}
    base = os.path.splitext(os.path.basename(libro))[0]
    json.dump(out, open(os.path.join(ens, "resultados", f"concordancia_{base}.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1, default=str)
    md = [f"# Concordancia del cambio de base · `{out['libro']}`", "", "| Celda | Configuración | fase 1 | Libro | ¿Concuerda? |", "|---|---|---|---|---|"]
    md += [f"| {x['celda']} | {x['configuracion']!r} | {x.get('fase1_v63', x.get('fase1_metadatos'))!r} | {x['libro']!r} | {'sí' if x['concuerda'] else 'NO'} |" for x in filas]
    md += ["", f"**Restos de la base anterior en la evidencia activa o en las notas:** {len(restos)}"] + [f"- `{x['celda']}`: «{x['texto'][:140]}»" for x in restos]
    md += ["", f"**Textos de la base anterior fuera de la evidencia activa** (cabecera y bloque de auditoría heredado; informativos, no cuentan para el resultado): {len(informativos)}"]
    md += [f"- `{x['celda']}`: «{x['texto'][:140]}»" for x in informativos]
    md += ["", f"**Fechas:** {out['fechas']}", "", f"**Resultado:** {out['resultado']}"]
    open(os.path.join(ens, "resultados", f"concordancia_{base}.md"), "w", encoding="utf-8").write("\n".join(md) + "\n")
    print("\n".join(md))
    return ok


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ("preparar", "comprobar"):
        print(__doc__)
        return 2
    p = sys.argv[2]
    conf = json.load(open(p, encoding="utf-8"))
    if conf.get("tipo") != "cambio_de_base" or conf.get("version_formato") != 1:
        print("CAMBIO.json: tipo o versión desconocidos")
        return 2
    conf["_archivo"], conf["_sha256"] = os.path.relpath(os.path.abspath(p), RAIZ), sha(p)
    if sys.argv[1] == "preparar":
        preparar(conf)
        return 0
    return 0 if comprobar(conf, sys.argv[3] if len(sys.argv) > 3 else None) else 1


if __name__ == "__main__":
    sys.exit(main())
