#!/usr/bin/env python3
"""
动词西班牙语 · Verbos — Dashboard API
FastAPI server for the verb conjugation video generator.
"""
import asyncio
import io
import json
import sys
from pathlib import Path
from typing import Optional

from PIL import Image
from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import HTMLResponse, FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import yaml
from src.content_parser import parse_yaml, Slide
from src.slide_renderer import render_slide, render_all_slides, render_xiaohongshu_portada
from src.tts_engine import generate_slide_audio
from src.video_composer import compose_video_with_subtitles
from src.xhs_description import generate_and_save as gen_xhs_desc

app = FastAPI(title="动词西班牙语 · Verbos")

static_dir = Path(__file__).parent / "static"
static_dir.mkdir(exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

SCRIPTS_DIR = PROJECT_ROOT / "scripts" / "verbos"
OUTPUT_DIR = PROJECT_ROOT / "output" / "verbos"
WORK_DIR = PROJECT_ROOT / ".work"
FREQ_FILE = PROJECT_ROOT / "verbos_frecuentes.yaml"


# ── Helpers ──

def _load_freq_list() -> list[dict]:
    if FREQ_FILE.exists():
        with open(FREQ_FILE) as f:
            data = yaml.safe_load(f)
        return data.get("verbos", [])
    return []


def _find_script(verbo: str) -> Optional[Path]:
    """Find a verbo YAML by name."""
    for f in sorted(SCRIPTS_DIR.glob("*.yaml")):
        with open(f) as fh:
            data = yaml.safe_load(fh)
        if data.get("verbo", "").lower() == verbo.lower():
            return f
    return None


def _get_script_path(verbo: str) -> Path:
    """Get or create script path for a verbo."""
    freq_list = _load_freq_list()
    for v in freq_list:
        if v["verbo"].lower() == verbo.lower():
            idx = v.get("frecuencia", 0)
            return SCRIPTS_DIR / f"{idx:03d}-{verbo}.yaml"
    return SCRIPTS_DIR / f"{verbo}.yaml"


# ── API Endpoints ──

@app.get("/")
async def index():
    return HTMLResponse((Path(__file__).parent / "templates" / "index.html").read_text(encoding="utf-8"))


@app.get("/api/verbos")
async def list_verbos():
    """List all verbos with their status: has script, has video."""
    freq_list = _load_freq_list()
    result = []
    for v in freq_list:
        verbo = v["verbo"]
        script_path = _find_script(verbo)
        has_script = script_path is not None
        has_video = False
        if script_path:
            script = parse_yaml(script_path)
            video_name = f"{script.filename_base}.mp4"
            has_video = (OUTPUT_DIR / video_name).exists()
        result.append({
            "verbo": verbo,
            "traduccion": v.get("traduccion", ""),
            "tipo": v.get("tipo", ""),
            "frecuencia": v.get("frecuencia", 0),
            "ejemplo": v.get("ejemplo", ""),
            "ejemplo_zh": v.get("ejemplo_zh", ""),
            "has_script": has_script,
            "has_video": has_video,
        })
    return JSONResponse(result)


@app.get("/api/verbo/{verbo}")
async def get_verbo(verbo: str):
    """Load a verbo's full YAML content as JSON."""
    script_path = _find_script(verbo)
    if not script_path:
        # Create from frequency list
        freq_list = _load_freq_list()
        vdata = next((v for v in freq_list if v["verbo"].lower() == verbo.lower()), None)
        if not vdata:
            raise HTTPException(404, f"Verbo '{verbo}' no encontrado")
        return JSONResponse({
            "verbo": verbo,
            "traduccion_zh": vdata["traduccion"],
            "tipo": vdata["tipo"],
            "frecuencia": vdata["frecuencia"],
            "has_script": False,
            "has_video": False,
            "slides": [],
        })

    script = parse_yaml(script_path)
    slides_data = []
    for slide in script.slides:
        sd = dict(slide.contenido)
        sd["tipo"] = slide.tipo
        sd["tts"] = slide.tts
        slides_data.append(sd)

    video_name = f"{script.filename_base}.mp4"
    cover_name = f"{script.filename_base}_cover_xhs.png"
    has_video = (OUTPUT_DIR / video_name).exists()

    return JSONResponse({
        "verbo": verbo,
        "nivel": script.nivel,
        "tema": script.tema,
        "capitulo": script.capitulo,
        "duracion_segmento": script.duracion_segmento,
        "slides": slides_data,
        "has_script": True,
        "has_video": has_video,
        "video_url": f"/api/video/{video_name}" if has_video else None,
        "cover_url": f"/api/video/{cover_name}" if (OUTPUT_DIR / cover_name).exists() else None,
    })


@app.post("/api/verbo/{verbo}/save")
async def save_verbo(verbo: str, payload: dict):
    """Save/update verbo YAML from JSON payload."""
    script_path = _get_script_path(verbo)

    # Build YAML content from payload
    yaml_data = {
        "modulo": "verbos_frecuentes",
        "tema": payload.get("tema", f"Verbo {verbo.upper()}"),
        "verbo": verbo,
        "traduccion_zh": payload.get("traduccion_zh", ""),
        "nivel": payload.get("nivel", "A1"),
        "frecuencia": payload.get("frecuencia", 0),
        "dificultad": payload.get("dificultad", "basico"),
        "tipo": payload.get("tipo_verbo", ""),
        "slides": [],
    }

    for slide in payload.get("slides", []):
        slide_data = {}
        for k, v in slide.items():
            if k not in ("tipo", "tts"):
                slide_data[k] = v
        yaml_data["slides"].append({
            "tipo": slide.get("tipo", "generic"),
            "tts": slide.get("tts", "zh"),
            **slide_data,
        })

    script_path.parent.mkdir(parents=True, exist_ok=True)
    with open(script_path, "w", encoding="utf-8") as f:
        yaml.dump(yaml_data, f, allow_unicode=True, default_flow_style=False, sort_keys=False, width=120)

    return JSONResponse({"ok": True, "path": str(script_path)})


@app.post("/api/verbo/{verbo}/preview/{slide_idx}")
async def preview_slide(verbo: str, slide_idx: int):
    """Render a single slide and return as base64 PNG."""
    script_path = _find_script(verbo)
    if not script_path:
        raise HTTPException(404, f"Verbo '{verbo}' sin script")

    script = parse_yaml(script_path)
    if slide_idx < 0 or slide_idx >= len(script.slides):
        raise HTTPException(404, f"Slide {slide_idx} fuera de rango (0-{len(script.slides)-1})")

    img = render_slide(script.slides[slide_idx])
    buf = io.BytesIO()
    img.save(buf, "PNG")
    buf.seek(0)

    import base64
    return JSONResponse({
        "base64": base64.b64encode(buf.read()).decode(),
        "tipo": script.slides[slide_idx].tipo,
        "w": img.size[0],
        "h": img.size[1],
    })


@app.post("/api/verbo/{verbo}/generate")
async def generate_verbo_video(verbo: str):
    """Generate full video for a verbo."""
    script_path = _find_script(verbo)
    if not script_path:
        raise HTTPException(404, f"Verbo '{verbo}' sin script")

    script = parse_yaml(script_path)

    # Work dirs
    slides_dir = WORK_DIR / "slides"
    audio_dir = WORK_DIR / "audio"
    slides_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    # 1. Render slides
    slide_paths = render_all_slides(script, slides_dir)

    # 2. TTS
    audio_paths = []
    for i, slide in enumerate(script.slides):
        sd = {
            "texto_tts_zh": slide.get("texto_tts_zh", ""),
            "texto_tts_es": slide.get("texto_tts_es", ""),
            "tipo": slide.tipo,
            "palabras": slide.get("palabras", []),
        }
        if not sd["texto_tts_zh"].strip() and not sd["texto_tts_es"].strip():
            if slide.tipo in ("portada", "conjugacion", "outro"):
                sd["texto_tts_zh"] = slide.get("titulo_zh", "")
            elif slide.tipo == "ejemplo":
                sd["texto_tts_es"] = slide.get("frase_es", "")
        ap = await generate_slide_audio(sd, audio_dir, i)
        audio_paths.append(ap)

    # 3. Compose video
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    video_path = OUTPUT_DIR / f"{script.filename_base}.mp4"

    slides_data = [
        {"frase_es": s.get("frase_es", ""), "titulo_es": s.get("titulo_es", ""), "tipo": s.tipo}
        for s in script.slides
    ]
    compose_video_with_subtitles(
        slide_paths, audio_paths, video_path, slides_data,
        float(script.duracion_segmento), subtitles=False,
    )

    # 4. Cover
    ps = next((s for s in script.slides if s.tipo == "portada"), script.slides[0])
    if script.capitulo is not None:
        ps.contenido["capitulo"] = script.capitulo
    cover = render_xiaohongshu_portada(ps)
    cover_path = OUTPUT_DIR / f"{script.filename_base}_cover_xhs.png"
    cover.save(cover_path, "PNG")

    # 5. XHS description
    desc_path = gen_xhs_desc(script_path, output_dir=OUTPUT_DIR, capitulo=script.capitulo, tema=script.tema)

    return JSONResponse({
        "ok": True,
        "video_url": f"/api/video/{video_path.name}",
        "cover_url": f"/api/video/{cover_path.name}",
        "video_path": str(video_path),
        "size_kb": round(video_path.stat().st_size / 1024, 1) if video_path.exists() else 0,
    })


@app.get("/api/video/{filename}")
async def serve_video(filename: str):
    """Serve generated video or cover files."""
    path = OUTPUT_DIR / filename
    if not path.exists():
        raise HTTPException(404, "Archivo no encontrado")
    return FileResponse(path)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8081)
