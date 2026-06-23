"""
Pipeline Orchestrator — generates a full video from a YAML script.
"""
import asyncio
from pathlib import Path
from .content_parser import parse_yaml, Slide, VideoScript
from .slide_renderer import render_all_slides, render_xiaohongshu_portada
from .tts_engine import generate_slide_audio
from .video_composer import compose_video, compose_video_with_subtitles
from .xhs_description import generate_and_save as generate_xhs_desc


async def generate_video(script_path: str | Path,
                          output_dir: str | Path = "output",
                          work_dir: str | Path = ".work") -> Path:
    """
    Full pipeline: parse → render slides → generate TTS → compose video.
    """
    script_path = Path(script_path)
    script = parse_yaml(script_path)

    work_dir = Path(work_dir)
    slides_dir = work_dir / "slides"
    audio_dir = work_dir / "audio"
    slides_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    name = script.filename_base
    print(f"\n🎬 Generating: {name}")
    print(f"   Nivel: {script.nivel} | Tema: {script.tema}")
    print(f"   Slides: {len(script.slides)}")

    # ── 1. Render slides ──
    print("\n📸 Rendering slides...")
    slide_paths = render_all_slides(script, slides_dir)

    # ── 2. Generate dual TTS audio for each slide ──
    print("\n🔊 Generating bilingual TTS audio...")
    audio_paths = []

    for i, slide in enumerate(script.slides):
        slide_data = {
            "texto_tts_zh": slide.get("texto_tts_zh", ""),
            "texto_tts_es": slide.get("texto_tts_es", ""),
            "tipo": slide.tipo,
            "palabras": slide.get("palabras", []),
        }
        # Fallback for empty TTS
        if not slide_data["texto_tts_zh"].strip() and not slide_data["texto_tts_es"].strip():
            if slide.tipo == "portada":
                slide_data["texto_tts_zh"] = slide.get("titulo_zh", "DELE Español")
            elif slide.tipo == "ejemplo":
                slide_data["texto_tts_es"] = slide.get("frase_es", "")
            else:
                slide_data["texto_tts_zh"] = slide.get("titulo_zh", "")

        final_path = await generate_slide_audio(slide_data, audio_dir, i)
        audio_paths.append(final_path)

    # ── 3. Compose video ──
    print("\n🎥 Composing video with subtitles...")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"{name}.mp4"

    slides_data = []
    for slide in script.slides:
        slides_data.append({
            "frase_es": slide.get("frase_es", ""),
            "titulo_es": slide.get("titulo_es", ""),
            "tipo": slide.tipo,
        })

    compose_video_with_subtitles(
        slide_paths=slide_paths,
        audio_paths=audio_paths,
        output_path=output_path,
        slides_data=slides_data,
        base_duration=float(script.duracion_segmento),
        subtitles=False,
    )

    # ── 4. Generate XHS cover ──
    print("\n🎨 Generating Xiaohongshu cover...")
    portada_slide = next((s for s in script.slides if s.tipo == "portada"), script.slides[0])
    # Inject chapter number into slide data so the renderer can display it
    if script.capitulo is not None:
        portada_slide.contenido["capitulo"] = script.capitulo
    cover_img = render_xiaohongshu_portada(portada_slide)
    cover_path = output_dir / f"{name}_cover_xhs.png"
    cover_img.save(cover_path, "PNG")
    print(f"  ✓ Cover: {cover_path}")

    # ── 5. Generate XHS description ──
    print("\n📝 Generating Xiaohongshu description...")
    desc_path = generate_xhs_desc(script_path, output_dir=output_dir,
                                   capitulo=script.capitulo, tema=script.tema)
    print(f"  ✓ Description: {desc_path}")

    print(f"\n✅ Done! Video: {output_path}")
    return output_path


def generate_video_sync(script_path: str | Path,
                         output_dir: str | Path = "output") -> Path:
    """Synchronous entry point for CLI usage."""
    return asyncio.run(generate_video(script_path, output_dir))
