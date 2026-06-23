"""
Video Composer — takes rendered slides + TTS audio, assembles final video.
Uses ffmpeg subprocess (memory-efficient streaming) for composition.
"""
import subprocess
import tempfile
from pathlib import Path

OUTPUT_WIDTH = 1080
OUTPUT_HEIGHT = 1920
FPS = 24


def _get_ffmpeg() -> str:
    """Find ffmpeg binary (bundled or system)."""
    try:
        subprocess.run(["ffmpeg", "-version"],
                       capture_output=True, check=True)
        return "ffmpeg"
    except FileNotFoundError:
        pass
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        raise RuntimeError(
            "ffmpeg not found. Install it: apt install ffmpeg"
        )


def _get_audio_duration(ffmpeg: str, path: Path) -> float:
    """Get duration of an audio file in seconds."""
    result = subprocess.run(
        [ffmpeg, "-i", str(path), "-f", "null", "-"],
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
    return 0.0


def _write_concat_list(slide_paths: list[Path],
                       durations: list[float],
                       filelist_path: Path):
    """Write ffmpeg concat demuxer file list (for image sequence)."""
    with open(filelist_path, "w") as f:
        for slide_path, dur in zip(slide_paths, durations):
            f.write(f"file '{slide_path.resolve()}'\n")
            f.write(f"duration {dur:.3f}\n")
        if slide_paths:
            f.write(f"file '{slide_paths[-1].resolve()}'\n")


def compose_video(
    slide_paths: list[Path],
    audio_paths: list[Path | None],
    output_path: str | Path,
    base_duration: float = 3.0,
    fade: float = 0.2,
) -> Path:
    """
    Compose slides + audio into a final video using ffmpeg.

    Strategy:
      1. Concatenate all audio files into one track
      2. Generate video from slide images
      3. Mix audio into video

    Args:
        slide_paths: ordered list of PNG slide images
        audio_paths: matching list of audio clips (None = no audio)
        output_path: final .mp4 path
        base_duration: default seconds per slide if no audio
        fade: (not used in ffmpeg path, kept for API compat)

    Returns:
        Path to the output video
    """
    ffmpeg = _get_ffmpeg()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    work = output_path.parent

    # ── 1. Calculate per-slide durations & build audio concat ──
    durations = []
    valid_audio_paths = []

    for slide_path, audio_path in zip(slide_paths, audio_paths):
        if audio_path and audio_path.exists():
            dur = _get_audio_duration(ffmpeg, audio_path)
            dur = max(dur, 1.5)
            valid_audio_paths.append((audio_path, dur))
        else:
            dur = base_duration
        durations.append(dur)

    total_duration = sum(durations)

    # ── 2. Concatenate all audio files ──
    mixed_audio = work / f".{output_path.stem}_audio.mp3"
    if valid_audio_paths:
        if len(valid_audio_paths) == 1:
            # Single audio — just copy
            subprocess.run(
                [ffmpeg, "-y", "-i", str(valid_audio_paths[0][0]),
                 "-c", "copy", str(mixed_audio)],
                check=True, capture_output=True,
            )
        else:
            # Multiple — concat via filter
            concat_file = work / f".{output_path.stem}_audio_list.txt"
            with open(concat_file, "w") as f:
                for ap, _ in valid_audio_paths:
                    f.write(f"file '{ap.resolve()}'\n")

            subprocess.run(
                [ffmpeg, "-y", "-f", "concat", "-safe", "0",
                 "-i", str(concat_file),
                 "-c", "copy", str(mixed_audio)],
                check=True, capture_output=True,
            )
            concat_file.unlink(missing_ok=True)

    # ── 3. Create video from slides ──
    raw_video = work / f".{output_path.stem}_novideo.mp4"

    filelist = work / f".{output_path.stem}_files.txt"
    _write_concat_list(slide_paths, durations, filelist)

    # Scale to fill 1080x1920 while maintaining aspect ratio, crop if needed
    scale_filter = (
        f"fps={FPS},"
        f"scale={OUTPUT_WIDTH}:{OUTPUT_HEIGHT}:force_original_aspect_ratio=increase,"
        f"crop={OUTPUT_WIDTH}:{OUTPUT_HEIGHT},"
        f"format=yuv420p"
    )

    print(f"  Encoding video ({len(slide_paths)} slides, {total_duration:.1f}s)...")
    subprocess.run(
        [ffmpeg, "-y",
         "-f", "concat",
         "-safe", "0",
         "-i", str(filelist),
         "-vf", scale_filter,
         "-c:v", "libx264",
         "-preset", "medium",
         "-crf", "23",
         "-pix_fmt", "yuv420p",
         "-an",
         str(raw_video)],
        check=True, capture_output=True,
    )
    filelist.unlink(missing_ok=True)

    # ── 4. Add audio ──
    if mixed_audio.exists():
        print(f"  Adding audio...")
        subprocess.run(
            [ffmpeg, "-y",
             "-i", str(raw_video),
             "-i", str(mixed_audio),
             "-c:v", "copy",
             "-c:a", "aac",
             "-b:a", "128k",
             "-map", "0:v:0",
             "-map", "1:a:0",
             "-shortest",
             str(output_path)],
            check=True, capture_output=True,
        )
        mixed_audio.unlink(missing_ok=True)
    else:
        raw_video.rename(output_path)

    raw_video.unlink(missing_ok=True)

    file_size = output_path.stat().st_size
    print(f"  ✓ Video: {output_path} ({file_size / 1024:.0f} KB)")
    return output_path


def preview_sequence(slide_paths: list[Path],
                     output_path: str | Path,
                     per_slide: float = 1.0) -> Path:
    """Fast preview without audio (low res for quick review)."""
    ffmpeg = _get_ffmpeg()
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    durations = [per_slide] * len(slide_paths)
    filelist = output_path.parent / f".{output_path.stem}_preview_files.txt"
    with open(filelist, "w") as f:
        for slide_path, dur in zip(slide_paths, durations):
            f.write(f"file '{slide_path.resolve()}'\n")
            f.write(f"duration {dur:.3f}\n")
        if slide_paths:
            f.write(f"file '{slide_paths[-1].resolve()}'\n")

    subprocess.run(
        [ffmpeg, "-y",
         "-f", "concat", "-safe", "0",
         "-i", str(filelist),
         "-vf", "fps=10,scale=540:960,format=yuv420p",
         "-c:v", "libx264",
         "-preset", "ultrafast",
         "-crf", "28",
         "-an",
         str(output_path)],
        check=True,
    )
    filelist.unlink(missing_ok=True)
    print(f"  Preview: {output_path}")
    return output_path


def compose_video_with_subtitles(
    slide_paths: list[Path],
    audio_paths: list[Path | None],
    output_path: str | Path,
    slides_data: list[dict],
    base_duration: float = 3.0,
    subtitles: bool = True,
) -> Path:
    """
    Compose video and optionally burn karaoke subtitles.
    
    Args:
        slide_paths: ordered list of PNG slide images
        audio_paths: matching list of audio clips (None = no audio)
        output_path: final .mp4 path
        slides_data: list of slide dicts with texto_tts_zh / texto_tts_es
        base_duration: default seconds per slide if no audio
        subtitles: whether to burn subtitles
    
    Returns:
        Path to the final video
    """
    # First compose the base video
    output_path = Path(output_path)
    base_video = compose_video(slide_paths, audio_paths, output_path, base_duration)
    
    if not subtitles:
        return base_video
    
    # Calculate audio durations and slide start times
    ffmpeg = _get_ffmpeg()
    audio_durations = []
    for ap in audio_paths:
        if ap and ap.exists():
            dur = _get_audio_duration(ffmpeg, ap)
            audio_durations.append(max(dur, 1.5))
        else:
            audio_durations.append(base_duration)
    
    # Calculate cumulative start times
    slide_starts = [0.0]
    for d in audio_durations[:-1]:
        slide_starts.append(slide_starts[-1] + d)
    
    # Generate ASS subtitles
    from .subtitle_generator import generate_all_ass, burn_all_subtitles
    
    ass_dir = output_path.parent / f".{output_path.stem}_subs"
    generate_all_ass(slides_data, audio_durations, slide_starts, ass_dir)
    
    # Burn subtitles into video
    subbed_video = output_path.parent / f"{output_path.stem}_subbed.mp4"
    burn_all_subtitles(base_video, ass_dir, subbed_video, audio_durations, slide_starts)
    
    # Cleanup temp files
    import shutil
    shutil.rmtree(ass_dir, ignore_errors=True)
    base_video.unlink(missing_ok=True)
    
    # Rename subbed video to original name
    subbed_video.rename(output_path)
    
    return output_path
