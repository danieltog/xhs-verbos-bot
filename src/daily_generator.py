#!/usr/bin/env python3
"""
Daily Video Generator — picks the next lesson from the calendar and generates it.
Run via cron for daily publishing.
"""
import asyncio
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from src.content_parser import parse_yaml, Slide, VideoScript
from src.slide_renderer import render_all_slides, render_xiaohongshu_portada
from src.tts_engine import generate_zh, generate_es
from src.video_composer import compose_video


# ── Voice rotation from branding ──
def load_branding():
    path = PROJECT_ROOT / "branding.yaml"
    with open(path) as f:
        return yaml.safe_load(f)


def get_voice_for_video(video_index: int, slide_idx: int, lang: str, branding: dict):
    """Rotate voices based on video index and slide position."""
    voces = branding["voces"]
    rotacion = branding["rotacion_voces"]
    pattern = rotacion[video_index % len(rotacion)]

    if lang == "zh":
        # Always use Xiaoxiao (stable, no errors)
        return "zh_explicacion"
    else:
        # Spanish: use the rotation pattern
        return pattern[slide_idx % 2]


def get_calendar():
    """Load calendar and determine the next lesson to generate."""
    cal_path = PROJECT_ROOT / "scripts" / "calendario.yaml"
    with open(cal_path) as f:
        cal = yaml.safe_load(f)

    # Build flat sequence
    lecciones = []
    for entry in cal["orden"]:
        for lec in entry["lecciones"]:
            lecciones.append({
                "nivel": entry["nivel"],
                "modulo": entry["modulo"],
                "nombre": lec,
            })

    dia = cal.get("dia_actual", 0)
    if dia >= len(lecciones):
        print("🎉 ¡Todos los videos han sido generados!")
        return None, None, dia

    leccion = lecciones[dia]
    return cal, leccion, dia


def update_calendar(cal, new_day):
    """Update the calendar with the new day index."""
    cal_path = PROJECT_ROOT / "scripts" / "calendario.yaml"
    cal["dia_actual"] = new_day
    with open(cal_path, "w") as f:
        yaml.dump(cal, f, allow_unicode=True, sort_keys=False)
    print(f"  📅 Calendario actualizado → día {new_day}")


async def generate_daily_video():
    """Main daily generation routine."""
    branding = load_branding()
    cal, leccion, dia = get_calendar()

    if leccion is None:
        return

    script_path = PROJECT_ROOT / "scripts" / leccion["nivel"] / leccion["modulo"] / f"{leccion['nombre']}.yaml"
    if not script_path.exists():
        print(f"❌ Script no encontrado: {script_path}")
        return

    print(f"\n{'='*60}")
    print(f"🎬 Hola西班牙语 — Día {dia + 1}")
    print(f"📖 {leccion['nivel']} / {leccion['modulo']} / {leccion['nombre']}")
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print(f"{'='*60}\n")

    # Parse
    script = parse_yaml(script_path)

    # Work dirs
    work_dir = PROJECT_ROOT / ".work" / f"dia_{dia+1:03d}"
    slides_dir = work_dir / "slides"
    audio_dir = work_dir / "audio"
    slides_dir.mkdir(parents=True, exist_ok=True)
    audio_dir.mkdir(parents=True, exist_ok=True)

    # Render slides
    print("📸 Renderizando slides...")
    slide_paths = render_all_slides(script, slides_dir)

    # Generate TTS with voice rotation
    print("\n🔊 Generando TTS (voces rotativas, dual si aplica)...")
    audio_paths = []
    for i, slide in enumerate(script.slides):
        # Check for dual TTS: both zh and es texts
        tts_zh = slide.get("texto_tts_zh", "")
        tts_es = slide.get("texto_tts_es", "")
        lang = slide.tts

        if not tts_zh and not tts_es:
            audio_paths.append(None)
            continue

        import subprocess
        final_path = audio_dir / f"s_{i:03d}.mp3"
        temp_files = []

        # Generate Spanish TTS first (ES habla primero en cada slide)
        if tts_es:
            voice_key = get_voice_for_video(dia, i, "es", branding)
            voces = branding["voces"]
            voice = voces[voice_key]
            es_path = audio_dir / f"s_{i:03d}_es.mp3"
            try:
                subprocess.run(
                    ["edge-tts", "--voice", voice, "--rate", "-15%",
                     "--text", tts_es,
                     "--write-media", str(es_path)],
                    check=True, capture_output=True,
                )
                temp_files.append(es_path)
                print(f"  [{i}] ES {voice}: {tts_es[:30]}...")
            except Exception as e:
                print(f"  ⚠ ES TTS falló slide {i}: {e}")

        # Generate Chinese TTS second (ZH después del español)
        if tts_zh:
            voice_key = "zh_explicacion"
            voces = branding["voces"]
            voice = voces.get(voice_key, "zh-CN-XiaoxiaoNeural")
            zh_path = audio_dir / f"s_{i:03d}_zh.mp3"
            try:
                subprocess.run(
                    ["edge-tts", "--voice", voice, "--rate", "-15%",
                     "--text", tts_zh,
                     "--write-media", str(zh_path)],
                    check=True, capture_output=True,
                )
                temp_files.append(zh_path)
                print(f"  [{i}] ZH {voice}: {tts_zh[:30]}...")
            except Exception as e:
                print(f"  ⚠ ZH TTS falló slide {i}: {e}")

        # Concatenate audio files if multiple, or just use single
        if len(temp_files) == 1:
            temp_files[0].rename(final_path)
            audio_paths.append(final_path)
        elif len(temp_files) > 1:
            # Generate silence gap between ZH and ES
            silence_path = audio_dir / f"s_{i:03d}_silence.mp3"
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "lavfi",
                     "-i", "anullsrc=r=24000:cl=mono",
                     "-t", "1.5",
                     "-c:a", "libmp3lame", "-q:a", "2",
                     str(silence_path)],
                    check=True, capture_output=True,
                )
            except Exception:
                silence_path = None

            # Build concat list with silence between each pair
            list_path = audio_dir / f"s_{i:03d}_list.txt"
            with open(list_path, "w") as f:
                for j, fp in enumerate(temp_files):
                    f.write(f"file '{fp.resolve()}'\n")
                    # Insert silence between files (but not after the last)
                    if j < len(temp_files) - 1 and silence_path and silence_path.exists():
                        f.write(f"file '{silence_path.resolve()}'\n")
            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
                     "-i", str(list_path),
                     "-c", "copy", str(final_path)],
                    check=True, capture_output=True,
                )
                audio_paths.append(final_path)
            except Exception as e:
                print(f"  ⚠ Concatenación falló slide {i}: {e}")
                # Fallback: use the first one
                temp_files[0].rename(final_path)
                audio_paths.append(final_path)
            finally:
                list_path.unlink(missing_ok=True)
                for fp in temp_files:
                    fp.unlink(missing_ok=True)
                if silence_path and silence_path.exists():
                    silence_path.unlink(missing_ok=True)
        else:
            audio_paths.append(None)

    # Compose video
    print("\n🎥 Componiendo video...")
    output_dir = PROJECT_ROOT / "output" / "hola"
    output_dir.mkdir(parents=True, exist_ok=True)

    output_path = output_dir / f"Hola西班牙语_{leccion['nivel']}_{leccion['nombre']}.mp4"
    compose_video(slide_paths, audio_paths, output_path)

    # Generate XHS cover from portada slide
    print("\n🎨 Generando portada Xiaohongshu...")
    portada_slide = next((s for s in script.slides if s.tipo == "portada"), script.slides[0])
    cover_img = render_xiaohongshu_portada(portada_slide)
    cover_path = output_dir / f"Hola西班牙语_{leccion['nivel']}_{leccion['nombre']}_cover_xhs.png"
    cover_img.save(cover_path, "PNG")
    print(f"  ✓ Cover XHS: {cover_path}")

    # Generate thumbnail
    print("\n🖼️ Generando thumbnail...")
    thumb_dir = output_dir / "thumbs"
    thumb_dir.mkdir(exist_ok=True)
    thumb_path = thumb_dir / f"Hola西班牙语_{leccion['nivel']}_{leccion['nombre']}.png"

    if slide_paths:
        from PIL import Image, ImageDraw, ImageFont
        # Use first slide as base
        img = Image.open(slide_paths[0]).copy()
        draw = ImageDraw.Draw(img)

        # Overlay branding
        try:
            font_small = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 28)
        except Exception:
            font_small = ImageFont.load_default()

        draw.rectangle([(0, 0), (1080, 120)], fill=(0, 0, 0, 200))
        draw.text((540, 20), f"Hola西班牙语 · {leccion['nivel']}", fill=(255, 200, 50), font=font_small, anchor="mt")
        draw.text((540, 60), leccion['nombre'].replace('-', ' ').upper(), fill=(255, 255, 255), font=font_small, anchor="mt")

        img.save(thumb_path)
        print(f"  ✓ Thumbnail: {thumb_path}")

    # Update calendar
    update_calendar(cal, dia + 1)

    print(f"\n✅ ¡Video del día {dia + 1} listo!")
    print(f"   → {output_path}")
    print(f"   Tamaño: {output_path.stat().st_size / 1024:.0f} KB")

    return output_path


def main():
    asyncio.run(generate_daily_video())


if __name__ == "__main__":
    main()
