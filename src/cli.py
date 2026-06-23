#!/usr/bin/env python3
"""
DELE Video Bot CLI — generate Xiaohongshu-optimized DELE learning videos.

Usage:
    python -m src.cli scripts/ejemplo-b1-pretérito-indefinido.yaml
    python -m src.cli scripts/ --output videos/
    python -m src.cli scripts/ --preview   # fast preview (no audio)
"""
import argparse
import sys
from pathlib import Path

# Add parent to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.content_parser import list_scripts
from src.pipeline import generate_video_sync


def main():
    parser = argparse.ArgumentParser(
        description="🎬 DELE Video Bot — generate Xiaohongshu DELE videos"
    )
    parser.add_argument(
        "input",
        help="YAML script file or directory containing .yaml scripts",
    )
    parser.add_argument(
        "--output", "-o",
        default="output",
        help="Output directory for videos (default: output/)",
    )
    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate fast preview (no audio, lower quality)",
    )
    args = parser.parse_args()

    input_path = Path(args.input)

    if input_path.is_dir():
        scripts = list_scripts(input_path)
        if not scripts:
            print(f"No .yaml scripts found in {input_path}")
            sys.exit(1)
        print(f"Found {len(scripts)} script(s)")
        for script in scripts:
            generate_video_sync(script, args.output)
    else:
        generate_video_sync(input_path, args.output)


if __name__ == "__main__":
    main()
