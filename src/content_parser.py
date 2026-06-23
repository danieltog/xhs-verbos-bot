"""
Content Parser for DELE video scripts.
Reads YAML and provides structured slide data.
"""
import yaml
import re
from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class Slide:
    tipo: str
    tts: str = "zh"  # "zh" or "es"
    contenido: dict = field(default_factory=dict)

    def __getitem__(self, key):
        return self.contenido.get(key)

    def get(self, key, default=None):
        return self.contenido.get(key, default)


@dataclass
class VideoScript:
    nivel: str
    tema: str
    slides: list[Slide]
    duracion_segmento: int = 3
    capitulo: int | None = None

    @property
    def filename_base(self) -> str:
        safe = re.sub(r'[^a-zA-Z0-9\u4e00-\u9fff]+', '_', self.tema)
        return f"DELE_{self.nivel}_{safe}"


def _extract_capitulo(path: str | Path) -> int | None:
    """Extract chapter number from filename prefix (e.g. '001-saludos-formales.yaml' -> 1)."""
    m = re.match(r"^(\d+)", Path(path).name)
    return int(m.group(1)) if m else None


def parse_yaml(path: str | Path) -> VideoScript:
    """Parse a YAML script file into a VideoScript."""
    with open(path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    slides = []
    for s in data.get("slides", []):
        slide = Slide(
            tipo=s.pop("tipo", "generic"),
            tts=s.pop("tts", "zh"),
            contenido=s
        )
        slides.append(slide)

    # Extract chapter number from filename
    capitulo = _extract_capitulo(path)

    # Inject chapter number into portada slide so all renderers see it
    if capitulo is not None:
        for slide in slides:
            if slide.tipo == "portada" and "capitulo" not in slide.contenido:
                slide.contenido["capitulo"] = capitulo

    return VideoScript(
        nivel=data.get("nivel", "A1"),
        tema=data.get("tema", "Sin título"),
        slides=slides,
        duracion_segmento=data.get("duracion_segmento", 3),
        capitulo=capitulo,
    )


def list_scripts(scripts_dir: str | Path) -> list[Path]:
    """List all YAML scripts in a directory."""
    return sorted(Path(scripts_dir).glob("*.yaml"))
