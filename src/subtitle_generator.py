"""
Subtitle Generator — creates ASS subtitle files with karaoke word highlighting.
Estimates per-word timing from text length and audio duration.
"""
import re
from pathlib import Path


def _estimate_timings(text: str, total_duration: float) -> list[tuple[str, float]]:
    """
    Split text into words/tokens and estimate duration for each based on length.
    
    Returns list of (word, duration_seconds).
    """
    if not text or total_duration <= 0:
        return []
    
    # Tokenize: Spanish words, Chinese characters, punctuation
    tokens = re.findall(
        r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ¿¡]+|[\u4e00-\u9fff]|[,.!?;:，。！？；：]+|\s+|[^\s\w]+',
        text
    )
    
    if not tokens:
        return []
    
    # Calculate character weights (CJK chars are 1, Latin word chars are 1 per letter)
    weights = []
    for tok in tokens:
        if re.match(r'^[\u4e00-\u9fff]$', tok):
            weights.append(1.0)
        elif re.match(r'^[a-zA-ZáéíóúüñÁÉÍÓÚÜ¿¡]+$', tok):
            weights.append(len(tok))
        elif tok.strip():
            weights.append(0.5)  # punctuation
        else:
            weights.append(0.2)  # spaces
    
    total_weight = sum(weights)
    if total_weight == 0:
        return [(text, total_duration)]
    
    # Distribute duration proportionally
    result = []
    for tok, w in zip(tokens, weights):
        dur = (w / total_weight) * total_duration
        result.append((tok, dur))
    
    return result


def generate_ass_subtitle(slide_index: int,
                          slide_start: float,
                          slide_duration: float,
                          texts: list[tuple[str, str, float]],
                          output_path: str | Path) -> Path:
    """
    Generate an ASS subtitle file with karaoke timing for one slide.
    
    Args:
        slide_index: slide number (used for style layer)
        slide_start: when this slide starts in the video (seconds)
        slide_duration: total duration of this slide
        texts: list of (lang, text, audio_duration) for each spoken segment
               lang is "zh" or "es"
        output_path: where to write the .ass file
    
    Returns:
        Path to the generated .ass file
    """
    output_path = Path(output_path)
    
    # Calculate combined timing for all texts in this slide
    events = []
    current_start = slide_start
    
    for lang, text, audio_dur in texts:
        if not text or audio_dur <= 0:
            current_start += 0.5
            continue
        
        timings = _estimate_timings(text, audio_dur)
        
        # Build karaoke line
        karaoke_parts = []
        for word, dur in timings:
            cs = int(dur * 100)  # convert to centiseconds
            if cs < 1:
                cs = 1
            karaoke_parts.append(f"{{\\k{cs}}}{word}")
        
        karaoke_line = "".join(karaoke_parts)
        
        # Font color: gold for karaoke highlights
        color = "&H0032C8FF&" if lang == "es" else "&H00B4F0FF&"
        
        events.append({
            "start": current_start,
            "end": current_start + audio_dur,
            "text": karaoke_line,
            "color": color,
        })
        
        current_start += audio_dur + 0.3  # small gap
    
    # Write ASS file
    ass_content = f"""[Script Info]
Title: DELE Video Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans SC,{_get_font_size_for_video()},&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,1,2,60,60,40,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    for evt in events:
        start_ts = _secs_to_ass_time(evt["start"])
        end_ts = _secs_to_ass_time(evt["end"])
        ass_content += f"Dialogue: 0,{start_ts},{end_ts},Default,,0,0,0,,{evt['text']}\n"
    
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(ass_content, encoding="utf-8")
    return output_path


def generate_all_ass(slides_data: list[dict],
                     audio_durations: list[float],
                     slide_starts: list[float],
                     output_dir: str | Path) -> list[Path]:
    """
    Generate ASS subtitle files for all slides.
    Only subtitles the VISIBLE slide text (frase_es, titulo_es), not the full TTS narration.
    """
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    
    for i in range(len(slides_data)):
        slide = slides_data[i]
        start = slide_starts[i] if i < len(slide_starts) else sum(audio_durations[:i])
        dur = audio_durations[i] if i < len(audio_durations) else 3.0
        
        # Only subtitle Spanish visible text (not Chinese narration)
        es_visible = slide.get("frase_es", "") or slide.get("titulo_es", "") or ""
        
        if es_visible and dur > 0:
            out = generate_ass_subtitle(i, start, dur, 
                                        [("es", es_visible, dur)],
                                        output_dir / f"slide_{i:03d}.ass")
            paths.append(out)
    
    return paths


def _get_font_size_for_video() -> int:
    """Font size for subtitles in 1080x1920 video."""
    return 36


def _secs_to_ass_time(seconds: float) -> str:
    """Convert seconds to ASS time format H:MM:SS.CS."""
    h = int(seconds // 3600)
    m = int((seconds % 3600) // 60)
    s = int(seconds % 60)
    cs = int((seconds % 1) * 100)
    return f"{h}:{m:02d}:{s:02d}.{cs:02d}"


def burn_subtitles(video_path: str | Path,
                   ass_path: str | Path,
                   output_path: str | Path) -> Path:
    """
    Burn ASS subtitles into a video using ffmpeg.
    """
    import subprocess
    video_path = Path(video_path)
    ass_path = Path(ass_path)
    output_path = Path(output_path)
    
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"ass={ass_path}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "copy",
        str(output_path),
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    return output_path


def burn_all_subtitles(video_path: str | Path,
                       ass_dir: str | Path,
                       output_path: str | Path,
                       slide_durations: list[float],
                       slide_starts: list[float]) -> Path:
    """
    Burn all ASS subtitles into a video by concatenating them into one ASS file.
    """
    import subprocess
    video_path = Path(video_path)
    ass_dir = Path(ass_dir)
    output_path = Path(output_path)
    
    # Concatenate all ASS subtitle files into one
    combined_ass = ass_dir / "combined.ass"
    
    header = """[Script Info]
Title: DELE Video Combined Subtitles
ScriptType: v4.00+
Collisions: Normal
PlayDepth: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans SC,28,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,2,1,2,60,60,80,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    
    with open(combined_ass, "w", encoding="utf-8") as out:
        out.write(header)
        
        for i, slide_dur in enumerate(slide_durations):
            ass_file = ass_dir / f"slide_{i:03d}.ass"
            if not ass_file.exists():
                continue
            
            start_time = slide_starts[i] if i < len(slide_starts) else sum(slide_durations[:i])
            
            with open(ass_file, encoding="utf-8") as f:
                for line in f:
                    if line.startswith("Dialogue:"):
                        out.write(line)
    
    # Burn into video
    cmd = [
        "ffmpeg", "-y",
        "-i", str(video_path),
        "-vf", f"ass={combined_ass}",
        "-c:v", "libx264",
        "-preset", "fast",
        "-crf", "23",
        "-c:a", "copy",
        str(output_path),
    ]
    
    subprocess.run(cmd, check=True, capture_output=True)
    print(f"  Subtitles burned: {output_path}")
    return output_path
