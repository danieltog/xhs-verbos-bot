#!/usr/bin/env python3
"""
DELE Video Bot — Dashboard API
FastAPI server for the complete curriculum-aware web interface.
"""
import asyncio
import base64
import io
import json
import os
import re
import sys
import tempfile
from pathlib import Path
from typing import Optional

from PIL import Image

from fastapi import FastAPI, HTTPException, Form, Body, Query, UploadFile, File
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml
from src.content_parser import Slide, VideoScript
from src.slide_renderer import render_slide, RENDERERS
from src.tts_engine import generate_zh, generate_es, generate_word_by_word, generate_slide_audio
from src.video_composer import compose_video, compose_video_with_subtitles, preview_sequence

sys.path.insert(0, str(PROJECT_ROOT))

app = FastAPI(title="Hola西班牙语 · DELE Video Bot")

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")


# ── Models ──

class SlideData(BaseModel):
    tipo: str = "explicacion"
    titulo_zh: str = ""
    titulo_es: str = ""
    puntos: list[str] = []
    frase_es: str = ""
    frase_origen: str = ""
    palabras: list[dict] = []
    traduccion_zh: str = ""
    analisis: list[str] = []
    indefinido: str = ""
    imperfecto: str = ""
    texto_zh: str = ""
    texto_tts_zh: str = ""
    texto_tts_es: str = ""
    tts: str = "zh"
    # XHS cover fields
    hook_zh: str = ""
    bullets: list = []
    cta: str = ""
    # Chapter number
    capitulo: Optional[int] = None

class VideoProject(BaseModel):
    nivel: str = "A1"
    tema: str = "Sin título"
    slides: list[SlideData] = []
    duracion_base: float = 2.5

class SaveLesson(BaseModel):
    modulo_slug: str
    leccion_slug: str
    slides: list[SlideData]


# ── Helpers ──

def _load_script(path: Path) -> dict | None:
    """Load a YAML script if it exists."""
    if path.exists():
        with open(path, encoding="utf-8") as f:
            return yaml.safe_load(f)
    return None

def _slide_to_data(s: dict) -> dict:
    """Convert a YAML slide dict to the data format the frontend expects."""
    data = {
        "tipo": s.get("tipo", "explicacion"),
        "titulo_zh": s.get("titulo_zh", ""),
        "titulo_es": s.get("titulo_es", ""),
        "puntos": s.get("puntos", [""]) if isinstance(s.get("puntos"), list) else [""],
        "frase_es": s.get("frase_es", ""),
        "frase_origen": s.get("frase_origen", ""),
        "palabras": s.get("palabras", []) if isinstance(s.get("palabras"), list) else [],
        "traduccion_zh": s.get("traduccion_zh", ""),
        "analisis": s.get("analisis", [""]) if isinstance(s.get("analisis"), list) else [""],
        "indefinido": s.get("indefinido", ""),
        "imperfecto": s.get("imperfecto", ""),
        "texto_zh": s.get("texto_zh", ""),
        "texto_tts_zh": s.get("texto_tts_zh", ""),
        "texto_tts_es": s.get("texto_tts_es", ""),
        "tts": s.get("tts", "zh"),
        "hook_zh": s.get("hook_zh", ""),
        "bullets": s.get("bullets", []) if isinstance(s.get("bullets"), list) else [],
        "cta": s.get("cta", ""),
        "capitulo": s.get("capitulo"),
    }
    return data


# ── Curriculum endpoints ──

@app.get("/api/curriculo")
async def api_curriculo():
    """Return the full A1 curriculum by scanning the script filesystem."""
    import re
    output_dir = PROJECT_ROOT / "output" / "hola"
    scripts_base = PROJECT_ROOT / "scripts" / "A1"
    
    # Load calendar to get the module structure
    cal_path = PROJECT_ROOT / "scripts" / "calendario.yaml"
    cal = {}
    if cal_path.exists():
        with open(cal_path) as f:
            cal = yaml.safe_load(f)
    
    # Module display names from the modules that have directories
    MODULE_NAMES = {
        "01_saludos": "Saludos y presentaciones",
        "02_alfabeto": "El alfabeto y la pronunciación",
        "03_numeros": "Los números",
        "04_dias_meses": "Días, meses y fechas",
        "05_hora": "La hora",
        "06_articulos": "Los artículos",
        "07_genero": "Género: masculino y femenino",
        "08_plural": "El plural",
        "09_presente_ar": "Presente: verbos regulares -AR",
        "10_presente_er_ir": "Presente: verbos regulares -ER e -IR",
        "11_ser_estar": "Ser y estar",
        "12_verbos_irregulares": "Verbos irregulares: tener, hacer, ir",
        "13_vocabulario_familia": "Vocabulario: familia y colores",
        "14_descripcion": "Descripción física y personalidad",
        "15_posesivos": "Los posesivos",
        "16_demostrativos": "Los demostrativos",
        "17_gustar": "El verbo GUSTAR",
        "18_hay_esta": "Hay / Está(n)",
        "19_preposiciones": "Preposiciones básicas",
        "20_preguntas_conectores": "Preguntas y conectores básicos",
        "21_frecuencia_rutina": "La frecuencia y la rutina diaria",
        "22_comida_restaurante": "La comida y el restaurante",
        "23_la_casa": "La casa y los muebles",
        "24_la_ciudad": "La ciudad y las direcciones",
        "25_repaso_general": "Repaso general A1",
    }
    
    result = {"nivel": "A1", "modulos": []}
    
    # Build from calendar order
    for entry in cal.get("orden", []):
        mod_slug = entry["modulo"]
        leccion_slugs = entry.get("lecciones", [])
        
        mod_data = {
            "titulo": MODULE_NAMES.get(mod_slug, mod_slug.replace("_", " ").title()),
            "slug": mod_slug,
            "lecciones": [],
        }
        
        mod_dir = scripts_base / mod_slug
        for lec_slug in leccion_slugs:
            script_path = mod_dir / f"{lec_slug}.yaml"
            script = _load_script(script_path)
            tema = lec_slug
            objetivo = ""
            es_repaso = False
            if script:
                tema = script.get("tema", lec_slug)
                # Detect repaso from slides
                for s in script.get("slides", []):
                    if "repaso" in s.get("titulo_zh", "").lower() or "复习" in s.get("titulo_zh", ""):
                        es_repaso = True
                        break
            
            video_name = f"Hola_A1_{lec_slug}.mp4"
            video_path = output_dir / video_name
            video_exists = video_path.exists()
            
            mod_data["lecciones"].append({
                "slug": lec_slug,
                "tema": tema.replace("Hola西班牙语 · A1 · ", ""),
                "objetivo": objetivo,
                "script_exists": script is not None,
                "num_slides": len(script.get("slides", [])) if script else 0,
                "video_exists": video_exists,
                "video_size": f"{video_path.stat().st_size / 1024:.0f} KB" if video_exists else None,
                "es_repaso": es_repaso or "repaso" in lec_slug,
            })
        
        if mod_data["lecciones"]:
            result["modulos"].append(mod_data)
    
    return result


@app.get("/api/leccion/{modulo_slug}/{leccion_slug}")
async def api_get_leccion(modulo_slug: str, leccion_slug: str):
    """Load a lesson's slides ONLY if they already exist. No auto-generation."""
    script_path = PROJECT_ROOT / "scripts" / "A1" / modulo_slug / f"{leccion_slug}.yaml"
    
    script = _load_script(script_path)
    if script:
        slides = [_slide_to_data(s) for s in script.get("slides", [])]
        # Inject chapter number from leccion_slug into portada slide
        cap_match = re.match(r'^(\d+)', leccion_slug)
        if cap_match:
            capitulo = int(cap_match.group(1))
            for slide in slides:
                if slide.get("tipo") == "portada":
                    slide["capitulo"] = capitulo
        # Check for existing video
        video_name = f"Hola_A1_{leccion_slug}.mp4"
        video_path = PROJECT_ROOT / "output" / "hola" / video_name
        video_exists = video_path.exists()
        video_url = f"/api/video/{video_name}" if video_exists else None
        video_size = f"{video_path.stat().st_size / 1024:.0f} KB" if video_exists else None
        # Check for existing XHS description file
        desc_path = PROJECT_ROOT / "output" / "hola" / f"{leccion_slug}_xhs_description.txt"
        xhs_description = desc_path.read_text(encoding="utf-8") if desc_path.exists() else None
        return {
            "nivel": script.get("nivel", "A1"),
            "tema": script.get("tema", ""),
            "modulo": modulo_slug,
            "duracion_base": script.get("duracion_segmento", 2.5),
            "slides": slides,
            "source": "script",
            "script_exists": True,
            "video_exists": video_exists,
            "video_url": video_url,
            "video_size": video_size,
            "xhs_description": xhs_description,
        }
    
    # No script yet — return empty, let frontend show "Generar contenido"
    return {
        "script_exists": False,
        "slides": [],
        "modulo": modulo_slug,
        "tema": leccion_slug.replace("-", " ").title(),
    }


@app.post("/api/leccion/{modulo_slug}/{leccion_slug}/save")
async def api_save_leccion(modulo_slug: str, leccion_slug: str, data: SaveLesson):
    """Save modified slides back to the YAML script."""
    print(f"[SAVE] modulo={modulo_slug} leccion={leccion_slug} slides={len(data.slides)}", flush=True)
    script_path = PROJECT_ROOT / "scripts" / "A1" / modulo_slug / f"{leccion_slug}.yaml"
    script_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Load existing to preserve metadata
    existing = _load_script(script_path) or {}
    
    slides_yaml = []
    for sd in data.slides:
        s = sd.model_dump(exclude_unset=True)
        # Clean up empty arrays
        for arr_field in ["puntos", "analisis"]:
            if arr_field in s:
                s[arr_field] = [x for x in s[arr_field] if x]
                if not s[arr_field]:
                    s[arr_field] = [""]
        slides_yaml.append(s)
    
    script = {
        "nivel": existing.get("nivel", "A1"),
        "tema": existing.get("tema", data.leccion_slug.replace("-", " ").title()),
        "duracion_segmento": existing.get("duracion_segmento", 2.5),
        "slides": slides_yaml,
    }
    
    with open(script_path, "w", encoding="utf-8") as f:
        yaml.dump(script, f, allow_unicode=True, sort_keys=False, width=80)
    
    return {"status": "ok", "path": str(script_path)}


@app.post("/api/leccion/{modulo_slug}/{leccion_slug}/generate")
async def api_generate_leccion(modulo_slug: str, leccion_slug: str):
    """Generate content for a specific lesson from curriculum data. Saves to YAML."""
    from src.content_factory import generate_script, write_script
    from src.contenido_a1 import A1_CURRICULO
    
    for mod in A1_CURRICULO["modulos"]:
        if mod["slug"] == modulo_slug:
            for lec in mod["lecciones"]:
                if lec["slug"] == leccion_slug:
                    script = generate_script(lec, mod, "A1")
                    out_dir = PROJECT_ROOT / "scripts" / "A1" / modulo_slug
                    out_dir.mkdir(parents=True, exist_ok=True)
                    write_script(script, mod, lec, out_dir)
                    slides = [_slide_to_data(s) for s in script.get("slides", [])]
                    return {
                        "status": "ok",
                        "tema": lec["tema"],
                        "slides": slides,
                        "nivel": "A1",
                        "duracion_base": 2.5,
                    }
    raise HTTPException(404, "Lección no encontrada en el currículo")


@app.get("/api/cover-xhs/{modulo_slug}/{leccion_slug}")
async def api_cover_xiaohongshu(modulo_slug: str, leccion_slug: str):
    """
    Generate a Xiaohongshu-style cover image for a lesson.
    Returns a PNG image optimized for RED social media.
    """
    from src.slide_renderer import render_xiaohongshu_portada
    from src.content_parser import Slide
    
    # Load lesson data
    script_path = PROJECT_ROOT / "scripts" / "A1" / modulo_slug / f"{leccion_slug}.yaml"
    tema = leccion_slug.replace("-", " ").title()
    titulo_zh = "Hola西班牙语 · A1"
    
    if script_path.exists():
        with open(script_path, encoding="utf-8") as f:
            script = yaml.safe_load(f)
            tema = script.get("tema", tema)
            # Get Chinese title from first slide's titulo_zh
            for s in script.get("slides", []):
                if s.get("tipo") == "portada":
                    titulo_zh = s.get("titulo_zh", titulo_zh)
                    break
    
    slide = Slide(tipo="xiaohongshu_portada", tts="zh", contenido={
        "titulo_es": tema,
        "titulo_zh": titulo_zh,
    })
    
    img = render_xiaohongshu_portada(slide)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    
    return Response(content=buf.getvalue(), media_type="image/png",
                    headers={"Content-Disposition": f"inline; filename=cover_{leccion_slug}.png"})


@app.post("/api/leccion/{modulo_slug}/{leccion_slug}/full-pipeline")
async def api_full_pipeline(modulo_slug: str, leccion_slug: str):
    """
    🚀 One-click full pipeline: curriculum → YAML → video.
    Regenera el contenido desde el currículo (con todas las reglas A1),
    genera slides + TTS bilingüe (chino instrucciones, español contenido),
    compone el video y lo devuelve.
    """
    from src.content_factory import generate_script, write_script
    from src.contenido_a1 import A1_CURRICULO
    from src.slide_renderer import render_slide

    # ── 1. Find lesson in curriculum ──
    lec_data = None
    mod_data = None
    for mod in A1_CURRICULO["modulos"]:
        if mod["slug"] == modulo_slug:
            mod_data = mod
            for lec in mod["lecciones"]:
                if lec["slug"] == leccion_slug:
                    lec_data = lec
                    break
            break

    if not lec_data:
        raise HTTPException(404, f"Lección no encontrada: {modulo_slug}/{leccion_slug}")

    print(f"[PIPELINE] 🚀 Full pipeline: {modulo_slug}/{leccion_slug} — {lec_data['tema']}", flush=True)

    # ── 2. Regenerate YAML from curriculum (applies all A1 rules) ──
    print(f"[PIPELINE]   📝 Regenerando YAML...", flush=True)
    script = generate_script(lec_data, mod_data, "A1")
    out_dir = PROJECT_ROOT / "scripts" / "A1" / modulo_slug
    out_dir.mkdir(parents=True, exist_ok=True)
    yaml_path = write_script(script, mod_data, lec_data, out_dir)
    print(f"[PIPELINE]   ✅ YAML: {yaml_path.name}", flush=True)

    # ── 3. Convert to SlideData list ──
    slides_raw = script.get("slides", [])
    slides = [SlideData(**_slide_to_data(s)) for s in slides_raw]
    print(f"[PIPELINE]   📊 {len(slides)} slides", flush=True)

    # ── 4. Setup output directories ──
    name = f"Hola_A1_{leccion_slug}"
    output_dir = PROJECT_ROOT / "output" / "hola"
    output_dir.mkdir(parents=True, exist_ok=True)

    work_dir = Path(tempfile.mkdtemp(prefix="dele_pipeline_"))
    slides_dir = work_dir / "slides"
    audio_dir = work_dir / "audio"
    slides_dir.mkdir()
    audio_dir.mkdir()

    try:
        # ── 5. Render slides ──
        print(f"[PIPELINE]   🎨 Renderizando slides...", flush=True)
        slide_paths = []
        for i, sd in enumerate(slides):
            slide = Slide(tipo=sd.tipo, tts=sd.tts,
                          contenido=sd.model_dump(exclude={"tipo", "tts"}))
            img = render_slide(slide)
            sp = slides_dir / f"slide_{i:03d}.png"
            img.save(sp)
            slide_paths.append(sp)

        # ── 6. Generate dual TTS: Chinese FIRST (instructions), Spanish SECOND (content) ──
        print(f"[PIPELINE]   🔊 Generando TTS bilingüe...", flush=True)
        audio_paths = []
        for i, sd in enumerate(slides):
            slide_data = {
                "texto_tts_zh": sd.texto_tts_zh or "",
                "texto_tts_es": sd.texto_tts_es or "",
                "tipo": sd.tipo,
                "palabras": sd.palabras or [],
            }
            final_path = await generate_slide_audio(slide_data, audio_dir, i)
            audio_paths.append(final_path)

        # ── 7. Compose video ──
        print(f"[PIPELINE]   🎥 Componiendo video...", flush=True)
        output_path = output_dir / f"{name}.mp4"
        slides_data = [{"frase_es": sd.frase_es or "",
                        "titulo_es": sd.titulo_es or "",
                        "tipo": sd.tipo or ""}
                       for sd in slides]
        compose_video_with_subtitles(
            slide_paths, audio_paths, output_path,
            slides_data=slides_data,
            base_duration=script.get("duracion_segmento", 3.0),
            subtitles=False,
        )

        size_kb = output_path.stat().st_size / 1024
        print(f"[PIPELINE]   ✅ Video: {name}.mp4 ({size_kb:.0f} KB)", flush=True)

        # ── 8. Generate XHS cover ──
        print(f"[PIPELINE]   🎨 Generando portada Xiaohongshu...", flush=True)
        from src.slide_renderer import render_xiaohongshu_portada
        portada_slide = next((Slide(tipo=s.tipo, tts=s.tts,
                                     contenido=s.model_dump(exclude={"tipo", "tts"}))
                              for s in slides if s.tipo == "portada"), None)
        if portada_slide is None:
            portada_slide = Slide(tipo="xiaohongshu_portada", tts="zh", contenido={
                "titulo_zh": f"Hola西班牙语 · {lec_data['tema']}",
                "titulo_es": lec_data["tema"],
            })
        cover_img = render_xiaohongshu_portada(portada_slide)
        cover_name = f"{name}_cover_xhs.png"
        cover_path = output_dir / cover_name
        cover_img.save(cover_path, "PNG")
        print(f"[PIPELINE]   ✅ Cover: {cover_name}", flush=True)

        # ── 9. Generate XHS description ──
        print(f"[PIPELINE]   📝 Generando descripción Xiaohongshu...", flush=True)
        from src.xhs_description import generate_and_save as gen_xhs_desc, generate_xhs_description
        cap_match = re.match(r'^(\\d+)', leccion_slug)
        capitulo = int(cap_match.group(1)) if cap_match else None
        desc = generate_xhs_description(yaml_path, capitulo=capitulo, tema=lec_data["tema"])
        desc_path = gen_xhs_desc(yaml_path, output_dir=output_dir,
                                  capitulo=capitulo, tema=lec_data["tema"])
        print(f"[PIPELINE]   ✅ Descripción: {desc_path.name}", flush=True)

        # Return slides too so frontend can refresh
        slides_out = [_slide_to_data(s) for s in slides_raw]
        return {
            "status": "ok",
            "video_url": f"/api/video/{name}.mp4",
            "filename": f"{name}.mp4",
            "size_kb": size_kb,
            "cover_xhs_url": f"/api/video/{cover_name}",
            "slides": slides_out,
            "tema": lec_data["tema"],
            "xhs_description": desc,
        }

    finally:
        import shutil
        shutil.rmtree(work_dir, ignore_errors=True)


@app.post("/api/curriculo/regenerate")
async def api_regenerate_curriculo():
    """Regenerate all YAML scripts from the curriculum data."""
    from src.content_factory import build_all
    paths = build_all(force=True)
    return {"status": "ok", "generated": [p.name for p in paths]}


@app.post("/api/curriculo/regenerate-one")
async def api_regenerate_one(modulo_slug: str = Form(...), leccion_slug: str = Form(...)):
    """Regenerate a single lesson from curriculum data."""
    for mod in A1_CURRICULO["modulos"]:
        if mod["slug"] == modulo_slug:
            for lec in mod["lecciones"]:
                if lec["slug"] == leccion_slug:
                    from src.content_factory import generate_script, write_script
                    script = generate_script(lec, mod, "A1")
                    out_dir = PROJECT_ROOT / "scripts" / "A1" / modulo_slug
                    write_script(script, mod, lec, out_dir)
                    return {"status": "ok", "slug": leccion_slug}
    raise HTTPException(404, "Lección no encontrada")


# ── Slide / Preview / Generate endpoints ──

@app.post("/api/preview-slide")
async def api_preview_slide(data: SlideData):
    """Render a single slide as base64 PNG, scaled to 540x960 for crisp preview."""
    try:
        slide = Slide(tipo=data.tipo, tts=data.tts,
                      contenido=data.model_dump(exclude={"tipo", "tts"}))
        img = render_slide(slide)
        # Scale down to half resolution for fast, crisp preview
        img = img.resize((540, 960), Image.LANCZOS)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return {"image": f"data:image/png;base64,{base64.b64encode(buf.getvalue()).decode()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/translate-es/{word:path}")
async def api_translate_es(word: str, force: bool = False):
    """Translate a Spanish word to Chinese using LLM (Moonshot), with local dict fallback.
    Set force=true to bypass cache and get a fresh LLM translation."""
    word_clean = word.strip()
    
    # ── 1. LLM translation (Moonshot/Kimi) ──
    try:
        from src.content_factory import _llm_translate_words, _LLM_TRANSLATION_CACHE
        if force and word_clean.lower() in _LLM_TRANSLATION_CACHE:
            del _LLM_TRANSLATION_CACHE[word_clean.lower()]
        translations = _llm_translate_words([word_clean])
        llm_zh = translations.get(word_clean.lower(), "")
        if llm_zh:
            return {"word": word_clean, "zh": llm_zh, "source": "llm"}
    except Exception as e:
        print(f"  ⚠ LLM translate failed for '{word_clean}': {e}")

    # ── 2. Fallback: diccionario local A1 español→chino ──
    DICT_ES_ZH = {
        "buenos": "好的", "días": "天/日子", "buenas": "好的",
        "tardes": "下午", "noches": "晚上", "hola": "你好",
        "qué": "什么", "tal": "如何", "cómo": "如何/怎么",
        "está": "是（状态）", "usted": "您", "tú": "你",
        "muy": "非常", "bien": "好的", "adiós": "再见",
        "hasta": "直到", "mañana": "明天", "luego": "之后",
        "gracias": "谢谢", "por": "为了", "favor": "请",
        "sí": "是", "no": "不", "yo": "我", "él": "他",
        "ella": "她", "nosotros": "我们", "ellos": "他们",
        "soy": "我是", "eres": "你是", "es": "是",
        "un": "一个", "una": "一个", "el": "定冠词(阳)",
        "la": "定冠词(阴)", "los": "定冠词(阳复)",
        "las": "定冠词(阴复)", "de": "的", "en": "在",
        "con": "和/用", "y": "和", "o": "或", "se": "代词",
        "me": "我(宾)", "te": "你(宾)", "le": "他/她(宾)",
        "hay": "有", "son": "是(复)", "tengo": "我有",
        "sobre": "关于/在…上", "entre": "在…之间", "sin": "没有",
        "desde": "从/自从", "para": "为了", "a": "到/向",
        "llamo": "叫(名字)", "nombre": "名字", "mucho": "很多",
        "gusto": "高兴", "encantado": "很高兴", "encantada": "很高兴",
        "dónde": "哪里", "eres": "你是", "soy": "我是",
        "vivo": "我住", "vives": "你住", "vive": "他/她住",
        "mexicano": "墨西哥人(男)", "mexicana": "墨西哥人(女)",
        "español": "西班牙人(男)", "española": "西班牙人(女)",
        "chino": "中国人(男)", "china": "中国人(女)",
        "número": "号码/数字", "teléfono": "电话",
        "uno": "一", "dos": "二", "tres": "三", "cuatro": "四",
        "cinco": "五", "seis": "六", "siete": "七", "ocho": "八",
        "nueve": "九", "diez": "十", "once": "十一", "doce": "十二",
        "lunes": "星期一", "martes": "星期二", "miércoles": "星期三",
        "jueves": "星期四", "viernes": "星期五", "sábado": "星期六",
        "domingo": "星期日", "enero": "一月", "febrero": "二月",
        "marzo": "三月", "abril": "四月", "mayo": "五月", "junio": "六月",
        "julio": "七月", "agosto": "八月", "septiembre": "九月",
        "octubre": "十月", "noviembre": "十一月", "diciembre": "十二月",
        "verde": "绿色", "azul": "蓝色", "amarillo": "黄色",
        "blanco": "白色", "negro": "黑色", "gris": "灰色",
        "padre": "父亲", "madre": "母亲", "hermano": "兄弟",
        "hermana": "姐妹", "hijo": "儿子", "hija": "女儿",
        "abuelo": "爷爷", "abuela": "奶奶", "amigo": "朋友(男)",
        "amiga": "朋友(女)", "casa": "房子/家", "cocina": "厨房",
        "baño": "浴室", "habitación": "房间", "mesa": "桌子",
        "silla": "椅子", "cama": "床", "puerta": "门", "ventana": "窗户",
        "restaurante": "餐厅", "menú": "菜单", "agua": "水",
        "café": "咖啡", "leche": "牛奶", "pan": "面包",
        "pollo": "鸡肉", "pescado": "鱼", "carne": "肉",
        "grande": "大", "pequeño": "小", "caro": "贵", "barato": "便宜",
        "bonito": "漂亮", "feo": "丑", "new": "新", "viejo": "旧",
        "guapo": "帅", "simpático": "和蔼", "antipático": "不友善",
        "alegre": "开朗", "triste": "悲伤", "inteligente": "聪明",
        "alto": "高", "bajo": "矮", "gordo": "胖", "delgado": "瘦",
        "cerca": "近", "lejos": "远", "aquí": "这里", "allí": "那里",
        "caminar": "走路", "comer": "吃", "beber": "喝", "dormir": "睡觉",
        "leer": "阅读", "escribir": "写", "escuchar": "听",
        # Nombres propios comunes
        "pedro": "佩德罗", "maría": "玛丽亚", "ana": "安娜", "juan": "胡安",
        "lucía": "露西亚", "carlos": "卡洛斯", "laura": "劳拉",
        "pablo": "巴勃罗", "sofía": "索菲亚", "diego": "迭戈",
        "elena": "埃莱娜", "miguel": "米格尔", "carmen": "卡门",
        "josé": "何塞", "isabel": "伊莎贝尔", "antonio": "安东尼奥",
        "rosa": "罗莎", "francisco": "弗朗西斯科", "teresa": "特蕾莎",
    }
    word_lower = word.strip().lower()
    translation = DICT_ES_ZH.get(word_lower, "")
    return {"word": word, "zh": translation, "source": "local"}


@app.post("/api/preview-tts")
async def api_preview_tts(lang: str = Form(...), text: str = Form(...)):
    """Generate TTS and return as base64 audio."""
    try:
        path = Path(tempfile.mktemp(suffix=".mp3"))
        if lang == "zh":
            await generate_zh(text, path.parent, path.stem)
        else:
            await generate_es(text, path.parent, path.stem)
        audio_data = path.read_bytes()
        path.unlink(missing_ok=True)
        return {"audio": f"data:audio/mp3;base64,{base64.b64encode(audio_data).decode()}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate")
async def api_generate(project: VideoProject, modulo_slug: str = Query(""), leccion_slug: str = Query("")):
    """Full pipeline: slides → TTS → video. Returns video file."""
    try:
        # Determine naming
        if modulo_slug and leccion_slug:
            name = f"Hola_A1_{leccion_slug}"
        else:
            safe_tema = project.tema.replace(" ", "_")[:30]
            name = f"DELE_{project.nivel}_{safe_tema}"

        output_dir = PROJECT_ROOT / "output" / "hola"
        output_dir.mkdir(parents=True, exist_ok=True)

        work_dir = Path(tempfile.mkdtemp(prefix="dele_gen_"))
        slides_dir = work_dir / "slides"
        audio_dir = work_dir / "audio"
        slides_dir.mkdir(); audio_dir.mkdir()

        from src.slide_renderer import render_slide

        slide_paths = []
        audio_paths = []

        for i, sd in enumerate(project.slides):
            slide = Slide(tipo=sd.tipo, tts=sd.tts,
                          contenido=sd.model_dump(exclude={"tipo", "tts"}))
            img = render_slide(slide)
            sp = slides_dir / f"slide_{i:03d}.png"
            img.save(sp)
            slide_paths.append(sp)

            # Generate dual TTS: Chinese first (instructions), Spanish second (content)
            slide_data = {
                "texto_tts_zh": sd.texto_tts_zh or "",
                "texto_tts_es": sd.texto_tts_es or "",
                "tipo": sd.tipo,
                "palabras": sd.palabras or [],
            }
            final_path = await generate_slide_audio(slide_data, audio_dir, i)
            audio_paths.append(final_path)

        output_path = output_dir / f"{name}.mp4"
        # Collect slide data for subtitles (only visible Spanish text)
        slides_data = [{"frase_es": sd.frase_es or "",
                        "titulo_es": sd.titulo_es or "",
                        "tipo": sd.tipo or ""}
                       for sd in project.slides]
        compose_video_with_subtitles(slide_paths, audio_paths, output_path,
                                     slides_data=slides_data,
                                     base_duration=project.duracion_base,
                                     subtitles=_get_subtitles_enabled())

        # ── Generate XHS description ──
        from src.xhs_description import generate_and_save as gen_xhs_desc, generate_xhs_description
        keywords = []
        for sd in project.slides:
            f = (sd.frase_es or "").strip()
            if f and f not in keywords:
                keywords.append(f)
        cap = int(re.match(r'^(\d+)', leccion_slug).group(1)) if re.match(r'^(\d+)', leccion_slug) else None
        desc = generate_xhs_description(script_path=None,
                          capitulo=cap, tema=project.tema, nivel=project.nivel,
                          keywords=keywords[:6])
        gen_xhs_desc(script_path=None, output_dir=output_dir,
                      capitulo=cap, tema=project.tema, nivel=project.nivel,
                      keywords=keywords[:6],
                      filename_base=name)

        import shutil
        shutil.rmtree(work_dir, ignore_errors=True)

        # Return JSON with video URL instead of file download
        return {
            "status": "ok",
            "video_url": f"/api/video/{name}.mp4",
            "filename": f"{name}.mp4",
            "size_kb": output_path.stat().st_size / 1024,
            "duration": output_path.stat().st_size / 1024 / 20,  # rough estimate
            "xhs_description": desc,
        }
    except Exception as e:
        import traceback; traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


# ── Scripts / Videos listings ──

@app.get("/api/video/{filename:path}")
async def api_serve_video(filename: str):
    """Serve a generated video file."""
    # Sanitize path to prevent directory traversal
    safe_name = Path(filename).name
    video_path = PROJECT_ROOT / "output" / "hola" / safe_name
    if not video_path.exists():
        # Also try subdirectories
        alt_path = PROJECT_ROOT / "output" / safe_name
        if alt_path.exists():
            video_path = alt_path
        else:
            raise HTTPException(404, "Video no encontrado")
    return FileResponse(str(video_path), media_type="video/mp4",
                       filename=safe_name,
                       headers={"Accept-Ranges": "bytes"})


@app.get("/api/videos")
async def api_list_videos():
    output_dir = PROJECT_ROOT / "output" / "hola"
    videos = []
    for p in sorted(output_dir.glob("*.mp4")):
        videos.append({
            "name": p.name,
            "size": f"{p.stat().st_size / 1024:.0f} KB",
            "path": str(p),
            "modified": p.stat().st_mtime,
        })
    return {"videos": videos}


# ── Settings endpoints ──

SETTINGS_PATH = PROJECT_ROOT / "config" / "slide_settings.json"

def _get_subtitles_enabled() -> bool:
    """Read subtitles setting from config."""
    try:
        if SETTINGS_PATH.exists():
            with open(SETTINGS_PATH) as f:
                return json.load(f).get("subtitles", False)
    except Exception:
        pass
    return False

@app.get("/api/settings")
async def api_get_settings():
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            return json.load(f)
    return {}

@app.post("/api/settings")
async def api_save_settings(data: dict = Body(...)):
    SETTINGS_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    # Reload settings in the slide renderer
    from src import slide_renderer
    slide_renderer.load_settings()
    return {"status": "ok"}

@app.post("/api/settings/logo")
async def api_upload_logo(file: UploadFile = File(...)):
    allowed = {"image/png", "image/jpeg", "image/webp"}
    if file.content_type not in allowed:
        raise HTTPException(400, "Solo PNG, JPEG o WebP")
    logo_path = PROJECT_ROOT / "config" / "logo.png"
    logo_path.parent.mkdir(parents=True, exist_ok=True)
    content = await file.read()
    # Convert to PNG if needed (using Pillow)
    from PIL import Image
    img = Image.open(io.BytesIO(content))
    img.save(logo_path, "PNG")
    # Update settings with logo path
    settings = {}
    if SETTINGS_PATH.exists():
        with open(SETTINGS_PATH) as f:
            settings = json.load(f)
    settings.setdefault("brand", {})["logo"] = str(logo_path)
    with open(SETTINGS_PATH, "w") as f:
        json.dump(settings, f, indent=2, ensure_ascii=False)
    # Reload renderer
    from src import slide_renderer
    slide_renderer.load_settings()
    return {"status": "ok", "logo": str(logo_path)}


# ── Frontend ──

@app.get("/test-save", response_class=HTMLResponse)
async def test_save_page():
    html_path = Path(__file__).parent / "templates" / "test-save.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))

@app.get("/", response_class=HTMLResponse)
async def dashboard():
    html_path = Path(__file__).parent / "templates" / "index.html"
    return HTMLResponse(html_path.read_text(encoding="utf-8"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8080, reload=True)
