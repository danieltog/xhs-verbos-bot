"""
Bilingual TTS Engine.
- Chinese voice: edge-tts (Microsoft Xiaoxiao) — free, natural
- Spanish voice: edge-tts (Microsoft) or fallback
- Supports ElevenLabs as premium option for Spanish
"""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

# ── Resolve edge-tts binary path ──
def _edge_tts_bin() -> str:
    """Return the edge-tts binary path from the venv, so it works without venv in PATH."""
    venv_bin = Path(sys.executable).parent / "edge-tts"
    if venv_bin.exists():
        return str(venv_bin)
    return "edge-tts"  # fallback: hope it's in PATH

# ── edge-tts voices ──
ZH_VOICE = "zh-CN-XiaoxiaoNeural"       # Chinese (Mandarin), female — default
ZH_VOICE_ALT = "zh-CN-YunxiNeural"       # Chinese (Mandarin), male
ES_VOICE = "es-MX-DaliaNeural"           # Mexican Spanish, female — primary
ES_VOICE_MALE = "es-MX-JorgeNeural"      # Mexican Spanish, male
ES_VOICE_ES = "es-ES-ElviraNeural"        # Spain Spanish, female
SILENCE_GAP_SEC = 1.5

# Rate adjustment: slower for learning content
RATE = "-15%"   # slower, clearer for learners. can be "+10%", "-20%", etc.


def _ensure_ffmpeg():
    """Check ffmpeg is available (needed by edge-tts)."""
    try:
        subprocess.run(["ffmpeg", "-version"],
                       capture_output=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError):
        raise RuntimeError(
            "ffmpeg is required. Install it: sudo apt install ffmpeg"
        )


async def _generate_edge_tts(text: str, voice: str,
                              output_path: str | Path,
                              rate: str = RATE) -> Path:
    """Generate TTS audio using edge-tts CLI."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    cmd = [
        _edge_tts_bin(),
        "--voice", voice,
        "--text", text,
        "--rate", rate,
        "--write-media", str(output_path),
    ]

    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    stdout, stderr = await proc.communicate()

    if proc.returncode != 0:
        raise RuntimeError(
            f"edge-tts failed (voice={voice}): {stderr.decode()}"
        )

    return output_path


async def generate_zh(text: str, output_dir: str | Path,
                      name: str = "zh_audio") -> Path:
    """Generate Chinese TTS audio."""
    _ensure_ffmpeg()
    out = Path(output_dir) / f"{name}.mp3"
    return await _generate_edge_tts(text, ZH_VOICE, out)


async def generate_es(text: str, output_dir: str | Path,
                      name: str = "es_audio",
                      voice: str = None) -> Path:
    """Generate Spanish TTS audio.
    
    Args:
        voice: override voice. Default: ES_VOICE (es-MX-DaliaNeural)
    """
    _ensure_ffmpeg()
    out = Path(output_dir) / f"{name}.mp3"
    v = voice or ES_VOICE
    return await _generate_edge_tts(text, v, out)


async def generate_bilingual_texts(texts: list[tuple[str, str]],
                                   output_dir: str | Path) -> list[Path]:
    """
    Generate TTS for multiple texts in batch.

    Args:
        texts: list of (lang, text) where lang is "zh" or "es"
        output_dir: directory for output audio files

    Returns:
        list of Path objects to generated audio files
    """
    tasks = []
    for i, (lang, text) in enumerate(texts):
        if lang == "zh":
            tasks.append(generate_zh(text, output_dir, name=f"slide_{i:03d}"))
        else:
            tasks.append(generate_es(text, output_dir, name=f"slide_{i:03d}"))

    results = await asyncio.gather(*tasks)
    return list(results)


# ── Convenience sync wrapper ──
def generate_sync(lang: str, text: str, output_dir: str | Path,
                  name: str = "audio") -> Path:
    """Synchronous wrapper for easier scripting."""
    return asyncio.run(
        generate_zh(text, output_dir, name) if lang == "zh"
        else generate_es(text, output_dir, name)
    )


async def generate_word_by_word(words: list[dict],
                                output_dir: str | Path,
                                slide_name: str = "vocab") -> tuple[Path, list[dict]]:
    """
    Generate individual TTS for each word, concatenate with silence gaps,
    and return precise timing data for word-level subtitle highlighting.

    Args:
        words: [{"es": "Buenos", "zh": "好的"}, ...]
        output_dir: where to store temp audio files
        slide_name: prefix for filenames

    Returns:
        (combined_audio_path, timeline)
        timeline: [{"word": "Buenos", "zh": "好的", "t_start": 0.15, "t_end": 0.90}, ...]
    """
    _ensure_ffmpeg()
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    gap_between_words = 0.45
    word_files = []
    timeline = []
    current_time = 0.15

    for idx, w in enumerate(words):
        word_text = w["es"]
        word_path = output_dir / f"{slide_name}_w{idx:02d}.mp3"

        try:
            await _generate_edge_tts(word_text, ES_VOICE, word_path, rate=RATE)
            if word_path.exists():
                dur = _get_audio_duration(word_path)
                timeline.append({
                    "word": word_text,
                    "zh": w.get("zh", ""),
                    "t_start": current_time,
                    "t_end": current_time + dur,
                })
                word_files.append(word_path)
                current_time += dur + gap_between_words
        except Exception as e:
            print(f"  ⚠ Word TTS failed for '{word_text}': {e}")
            est_dur = max(0.4, len(word_text) * 0.15)
            timeline.append({
                "word": word_text,
                "zh": w.get("zh", ""),
                "t_start": current_time,
                "t_end": current_time + est_dur,
            })
            current_time += est_dur + gap_between_words

    combined = output_dir / f"{slide_name}_vocab.mp3"

    if len(word_files) == 0:
        silence = output_dir / f"{slide_name}_silence.mp3"
        subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi",
             "-i", "anullsrc=r=24000:cl=mono",
             "-t", "3.0", "-c:a", "libmp3lame", "-q:a", "2",
             str(silence)],
            check=True, capture_output=True,
        )
        return silence, timeline

    if len(word_files) == 1:
        word_files[0].rename(combined)
        return combined, timeline

    # Build concat list with silence between words
    gap_file = output_dir / f"{slide_name}_gap.mp3"
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi",
         "-i", f"anullsrc=r=24000:cl=mono",
         "-t", str(gap_between_words), "-c:a", "libmp3lame", "-q:a", "2",
         str(gap_file)],
        check=True, capture_output=True,
    )

    lst = output_dir / f"{slide_name}_list.txt"
    with open(lst, "w") as f:
        for j, fp in enumerate(word_files):
            f.write(f"file '{fp.resolve()}'\n")
            if j < len(word_files) - 1:
                f.write(f"file '{gap_file.resolve()}'\n")

    subprocess.run(
        ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
         "-i", str(lst), "-c", "copy", str(combined)],
        check=True, capture_output=True,
    )

    # Cleanup temp files
    lst.unlink(missing_ok=True)
    gap_file.unlink(missing_ok=True)
    for fp in word_files:
        fp.unlink(missing_ok=True)

    return combined, timeline


def _get_audio_duration(path: Path) -> float:
    """Get duration of an audio file in seconds using ffmpeg."""
    result = subprocess.run(
        ["ffmpeg", "-i", str(path), "-f", "null", "-"],
        capture_output=True, text=True,
    )
    for line in result.stderr.split("\n"):
        if "Duration" in line:
            try:
                ts = line.split("Duration: ")[1].split(",")[0]
                h, m, s = ts.split(":")
                return float(h) * 3600 + float(m) * 60 + float(s)
            except (ValueError, IndexError):
                pass
    return 1.0


async def generate_slide_audio(
    slide_data: dict,
    audio_dir: Path,
    slide_index: int,
    retries: int = 2,
) -> Path | None:
    """
    Generate combined audio for a single slide.
    Handles dual TTS (ZH + ES) with proper silence gaps.
    Returns path to combined MP3, or None if no audio.

    slide_data should have keys:
        texto_tts_zh, texto_tts_es, tipo, palabras (optional)
    """
    import subprocess as sp_subprocess

    tts_zh = slide_data.get("texto_tts_zh", "").strip()
    tts_es = slide_data.get("texto_tts_es", "").strip()
    tipo = slide_data.get("tipo", "")
    palabras = slide_data.get("palabras", []) if isinstance(slide_data.get("palabras"), list) else []

    temp_files = []

    # ── Chinese TTS (first) — instructions ──
    if tts_zh:
        zh_path = audio_dir / f"s_{slide_index:03d}_zh.mp3"
        for attempt in range(retries + 1):
            try:
                await generate_zh(tts_zh, audio_dir, f"s_{slide_index:03d}_zh")
                if zh_path.exists():
                    temp_files.append(zh_path)
                    break
            except Exception as e:
                if attempt < retries:
                    print(f"  🔄 ZH TTS slide {slide_index} retry {attempt+1}: {e}")
                    await asyncio.sleep(1)
                else:
                    print(f"  ❌ ZH TTS slide {slide_index} FAILED after {retries+1} attempts: {e}")

    # ── Exercise: 5s thinking silence (before Spanish) ──
    if tipo == "ejercicio":
        think_silence = audio_dir / f"s_{slide_index:03d}_think.mp3"
        try:
            sp_subprocess.run(
                ["ffmpeg", "-y", "-f", "lavfi",
                 "-i", "anullsrc=r=24000:cl=mono",
                 "-t", "5.0", "-c:a", "libmp3lame", "-q:a", "2",
                 str(think_silence)],
                check=True, capture_output=True,
            )
            if think_silence.exists():
                temp_files.append(think_silence)
        except Exception:
            pass

    # ── Spanish TTS (second) — content ──
    if tts_es:
        es_path = audio_dir / f"s_{slide_index:03d}_es.mp3"
        for attempt in range(retries + 1):
            try:
                if tipo == "vocabulario" and len(palabras) >= 2:
                    # Word-by-word TTS for vocabulary slides
                    wb_path, timeline = await generate_word_by_word(
                        palabras, audio_dir, f"s_{slide_index:03d}"
                    )
                    if not wb_path.exists():
                        raise RuntimeError("Word-by-word TTS produced no file")
                    wb_path.rename(es_path)
                else:
                    await generate_es(tts_es, audio_dir, f"s_{slide_index:03d}_es")
                    if not es_path.exists():
                        raise RuntimeError("generate_es produced no file")

                temp_files.append(es_path)
                dur = _get_audio_duration(es_path)
                print(f"  ✅ ES TTS slide {slide_index}: {len(tts_es)} chars → {dur:.1f}s")
                break
            except Exception as e:
                if attempt < retries:
                    print(f"  🔄 ES TTS slide {slide_index} retry {attempt+1}: {e}")
                    await asyncio.sleep(1)
                else:
                    print(f"  ❌ ES TTS slide {slide_index} FAILED after {retries+1} attempts")
                    print(f"     text={tts_es[:80]!r}")
                    print(f"     error={e}")

    # ── Combine segments ──
    if len(temp_files) == 0:
        return None

    final_path = audio_dir / f"slide_{slide_index:03d}.mp3"
    if len(temp_files) == 1:
        temp_files[0].rename(final_path)
        return final_path

    # Combine with silence gaps
    silence_path = audio_dir / f"s_{slide_index:03d}_silence.mp3"
    try:
        sp_subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi",
             "-i", "anullsrc=r=24000:cl=mono",
             "-t", "1.5", "-c:a", "libmp3lame", "-q:a", "2",
             str(silence_path)],
            check=True, capture_output=True,
        )
    except Exception:
        silence_path = None

    lst = audio_dir / f"s_{slide_index:03d}_list.txt"
    with open(lst, "w") as f:
        for j, fp in enumerate(temp_files):
            f.write(f"file '{fp.resolve()}'\n")
            if j < len(temp_files) - 1 and silence_path and silence_path.exists():
                f.write(f"file '{silence_path.resolve()}'\n")

    try:
        sp_subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", str(lst), "-c", "copy", str(final_path)],
            check=True, capture_output=True,
        )
    except Exception:
        # Fallback: use first segment only
        temp_files[0].rename(final_path)
    finally:
        lst.unlink(missing_ok=True)
        for fp in temp_files:
            fp.unlink(missing_ok=True)
        if silence_path and silence_path.exists():
            silence_path.unlink(missing_ok=True)

    return final_path


if __name__ == "__main__":
    # Quick test
    async def test():
        zh = await generate_zh("你好，欢迎学习西班牙语", "/tmp/dele_test")
        es = await generate_es("Hola, bienvenidos a aprender español",
                               "/tmp/dele_test")
        print(f"ZH audio: {zh}")
        print(f"ES audio: {es}")

    asyncio.run(test())
