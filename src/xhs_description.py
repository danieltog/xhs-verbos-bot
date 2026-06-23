"""
Xiaohongshu Description Generator
Generates attractive, explanatory descriptions + hashtags for DELE video posts.
"""
import re
from pathlib import Path
from typing import Optional


def _extract_keywords(script: dict) -> list[str]:
    """Extract key Spanish phrases taught in the lesson."""
    phrases = []
    for slide in script.get("slides", []):
        frase = slide.get("frase_es", "").strip()
        if frase and frase not in phrases:
            phrases.append(frase)
        # Also grab bullet points with Spanish content
        for p in slide.get("puntos", []):
            if isinstance(p, str):
                parts = p.split("—", 1)
                es_part = parts[0].strip()
                if es_part and es_part not in phrases:
                    phrases.append(es_part)
    return phrases[:6]  # max 6 to avoid bloat


def _extract_topics(script: dict) -> list[str]:
    """Extract Chinese topic labels from explanations."""
    topics = []
    for slide in script.get("slides", []):
        titulo = slide.get("titulo_zh", "").strip()
        if titulo and titulo not in ("Punto 1", "Punto 2", "Punto 3", "Repaso", ""):
            topics.append(titulo)
    return topics


def generate_xhs_description(script_path: str | Path | None = None,
                              capitulo: Optional[int] = None,
                              tema: Optional[str] = None,
                              nivel: str = "A1",
                              modulo: str = "",
                              keywords: Optional[list[str]] = None) -> str:
    """
    Generate a Xiaohongshu post description with emojis, key content,
    and optimized hashtags for the DELE Spanish learning niche.

    Pass either script_path (reads YAML) or keywords+tema+nivel directly.
    """
    if script_path:
        import yaml
        with open(script_path, encoding="utf-8") as f:
            script = yaml.safe_load(f)
        nivel = script.get("nivel", nivel)
        tema = tema or script.get("tema", "Español")
        modulo = script.get("modulo", modulo)
        keywords = _extract_keywords(script)
        if capitulo is None:
            m = re.match(r"^(\d+)", Path(script_path).name)
            capitulo = int(m.group(1)) if m else None
    else:
        tema = tema or "Español"
        keywords = keywords or []

    # Filter: keep only short phrases (real vocab, not sentences)
    keywords = [k for k in keywords if len(k) <= 40]

    # ── Build description ──
    lines = []

    # Title line
    if capitulo:
        lines.append(f"🇪🇸 每天5分钟学西语 | 第{capitulo}课：{tema}")
    else:
        lines.append(f"🇪🇸 每天5分钟学西语 | {tema}")

    lines.append("")

    # Intro
    lines.append(f"📚 DELE {nivel} 零基础友好系列")
    lines.append("从零开始，每天进步一点点 ✨")
    lines.append("")

    # What you'll learn
    if keywords:
        lines.append("📝 今天你会学到：")
        for i, kw in enumerate(keywords, 1):
            lines.append(f"  {i}️⃣ {kw}")
        lines.append("")

    # Learning tips
    lines.append("💡 学习小贴士：")
    lines.append("• 先听中文讲解，再跟读西班牙语 👂")
    lines.append("• 每个单词都有逐词拆解，不怕记不住 📖")
    lines.append("• 建议收藏⭐，每天打卡学习")
    lines.append("")

    # CTA
    lines.append("🔔 关注我，每天更新DELE A1全套课程")
    lines.append("💬 有问题评论区留言，我来解答～")
    lines.append("")

    # ── Hashtags ──
    tags = [
        "#西班牙语学习",
        "#西语入门",
        "#DELE",
        "#DELE" + nivel,
        "#每天学西语",
        "#零基础学西语",
        "#西班牙语打卡",
    ]

    # Module-based hashtag (strip leading digits and underscores)
    if modulo:
        clean = re.sub(r'^\d+_', '', modulo)  # remove prefix like "01_"
        clean = clean.replace("_", "")
        if clean:
            tags.append(f"#西语{clean}")

    tags.extend([
        "#小语种学习",
        "#外语学习",
        "#Hola西班牙语",
        "#自学西班牙语",
        "#小红书学习",
    ])

    lines.append(" ".join(tags))

    return "\n".join(lines)


def generate_and_save(script_path: str | Path | None = None,
                       output_dir: str | Path = "output",
                       capitulo: Optional[int] = None,
                       tema: Optional[str] = None,
                       nivel: str = "A1",
                       modulo: str = "",
                       keywords: Optional[list[str]] = None,
                       filename_base: Optional[str] = None) -> Path:
    """Generate description and save as .txt alongside the video."""
    desc = generate_xhs_description(
        script_path, capitulo=capitulo, tema=tema,
        nivel=nivel, modulo=modulo, keywords=keywords
    )

    if filename_base:
        name = filename_base
    elif script_path:
        name = Path(script_path).stem
    else:
        name = "xhs_description"

    desc_path = Path(output_dir) / f"{name}_xhs_description.txt"
    desc_path.parent.mkdir(parents=True, exist_ok=True)
    desc_path.write_text(desc, encoding="utf-8")

    return desc_path
