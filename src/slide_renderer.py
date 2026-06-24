"""
Slide Renderer — generates beautiful 9:16 slide images for Xiaohongshu.
Clean, readable layout with generous spacing. No emoji, no clutter.

Output: 1080x1920 (portrait) — ideal for vertical short video.
"""
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont
from .content_parser import Slide, VideoScript

# ── Emoji stripping ──
_EMOJI_RE = re.compile(
    "["
    "\U0001F600-\U0001F64F\U0001F300-\U0001F5FF\U0001F680-\U0001F6FF"
    "\U0001F700-\U0001F77F\U0001F780-\U0001F7FF\U0001F800-\U0001F8FF"
    "\U0001F900-\U0001F9FF\U0001FA00-\U0001FA6F\U0001FA70-\U0001FAFF"
    "\U00002702-\U000027B0"
    "\U0001F004\U0001F0CF\U0001F18E\U0001F191-\U0001F19A"
    "\U0001F200-\U0001F251"
    "\U00002328-\U0000232B\U000023CF\U000023E9-\U000023F3"
    "\U000023F8-\U000023FA"
    "\U00002B05-\U00002B07\U00002B1B-\U00002B1C\U00002B50\U00002B55"
    "\U0000231A-\U0000231B"
    "\U000025AA-\U000025AB\U000025B6\U000025C0\U000025FB-\U000025FE"
    "\U00002600-\U000026FF"
    "\U00002139\U00002194-\U00002199\U000021A9-\U000021AA"
    "\U000026A0-\U000026A1"
    "\U00002714\U00002716\U00002733-\U00002734\U00002744\U00002747"
    "\U0000274C\U0000274E\U00002753-\U00002755\U00002757"
    "\U00002763-\U00002764\U00002795-\U00002797"
    "\U00002122\U000000A9\U000000AE"
    "\U00002022-\U00002023\U0000203C\U00002049"
    "\U000020E3\U00003030\U0000303D\U0000FE0F"
    "]+",
    re.UNICODE,
)

def _strip_emoji(text: str) -> str:
    if not text:
        return ""
    cleaned = _EMOJI_RE.sub("", text)
    cleaned = cleaned.replace("\u200d", "")
    cleaned = re.sub(r"  +", " ", cleaned)
    cleaned = re.sub(r" ([,.!?;:，。！？；：])", r"\1", cleaned)
    return cleaned.strip()

# ── Canvas ──
W, H = 1080, 1920
MX = 80   # horizontal margin
MY = 90   # top margin
MB = 100  # bottom margin
CW = W - MX * 2  # content width

# ── Colors ──
CLR = {
    "bg_top":     (15, 18, 30),
    "bg_bot":     (30, 20, 50),
    "gold":       (255, 200, 50),
    "blue":       (80, 180, 255),
    "coral":      (255, 110, 100),
    "white":      (255, 255, 255),
    "light":      (220, 220, 240),
    "gray":       (150, 150, 170),
    "card_dark":  (40, 36, 65, 200),
    "card_blue":  (30, 50, 85, 210),
    "card_coral": (65, 40, 48, 200),
}

# ── Typography ──
FS = {
    "hero":      72,   # big Spanish titles
    "hero_zh":   58,   # big Chinese titles
    "heading":   48,   # section headings
    "body":      40,   # body / bullet text
    "body_zh":   36,   # Chinese body
    "small":     30,   # labels, chips
    "brand":     24,   # watermark
}
_FS_ORIG = dict(FS)  # never-modified originals

# Line spacing (added on top of font size)
LS = {"tight": 4, "norm": 10, "wide": 16, "hero": 22}
_LS_ORIG = dict(LS)  # never-modified originals

BRAND = "Hola西班牙语"
LOGO_PATH = None

# ═══════════════════════════════════════════════
# SETTINGS LOADER
# ═══════════════════════════════════════════════

SETTINGS_PATH = Path(__file__).resolve().parent.parent / "config" / "slide_settings.json"


def load_settings():
    """Load slide settings from JSON. Called once at module import."""
    global CLR, FS, LS, BRAND, LOGO_PATH
    if not SETTINGS_PATH.exists():
        return
    try:
        import json
        with open(SETTINGS_PATH) as f:
            s = json.load(f)
    except Exception:
        return

    # Font scale — reset to originals first, then apply scale
    global LOGO_PATH
    for k in FS:
        FS[k] = _FS_ORIG[k]
    for k in LS:
        LS[k] = _LS_ORIG[k]
    
    scale = float(s.get("font_scale", 1.0))
    if scale != 1.0:
        for k in FS:
            FS[k] = int(_FS_ORIG[k] * scale)

    # Spacing scale
    sp_scale = float(s.get("spacing_scale", 1.0))
    if sp_scale != 1.0:
        for k in LS:
            LS[k] = int(_LS_ORIG[k] * sp_scale)

    # Colors (apply to CLR dict)
    colors = s.get("colors", {})
    for key in ["gold", "blue", "coral", "bg_top", "bg_bot"]:
        if key in colors and isinstance(colors[key], list) and len(colors[key]) == 3:
            CLR[key] = tuple(colors[key])
    # Card colors need alpha channel
    for key in ["card_dark", "card_blue", "card_coral"]:
        if key in colors and isinstance(colors[key], list) and len(colors[key]) == 3:
            CLR[key] = (*tuple(colors[key]), 200)

    # Brand
    brand_cfg = s.get("brand", {})
    if brand_cfg.get("name"):
        BRAND = str(brand_cfg["name"])
    if brand_cfg.get("logo"):
        logo_p = Path(brand_cfg["logo"])
        if logo_p.exists():
            LOGO_PATH = logo_p


load_settings()

# ═══════════════════════════════════════════════
# HELPERS
# ═══════════════════════════════════════════════

def _font(size: int) -> ImageFont.FreeTypeFont:
    paths = [
        Path("/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"),
        Path("/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"),
        Path.home() / ".local/share/fonts" / "NotoSansSC-Regular.ttf",
        Path("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"),
    ]
    for p in paths:
        if p.exists():
            try:
                return ImageFont.truetype(str(p), size)
            except Exception:
                continue
    return ImageFont.load_default()

def _bg(draw):
    for y in range(H):
        r = int(CLR["bg_top"][0] * (1 - y/H) + CLR["bg_bot"][0] * (y/H))
        g = int(CLR["bg_top"][1] * (1 - y/H) + CLR["bg_bot"][1] * (y/H))
        b = int(CLR["bg_top"][2] * (1 - y/H) + CLR["bg_bot"][2] * (y/H))
        draw.line([(0, y), (W, y)], fill=(r, g, b))

def _card(draw, x, y, w, h, radius=16, fill=None):
    draw.rounded_rectangle((x, y, x + w, y + h), radius=radius, fill=fill)

def _cx(draw, text, font):
    b = font.getbbox(text)
    return (W - (b[2] - b[0])) // 2

def _is_cjk(ch):
    cp = ord(ch)
    return (0x4E00 <= cp <= 0x9FFF or 0x3400 <= cp <= 0x4DBF or
            0x2E80 <= cp <= 0x2FDF or 0x3000 <= cp <= 0x303F or
            0xFF00 <= cp <= 0xFFEF)

def _wrap(text, font, max_w):
    """Smart wrap: word-wrap for Latin, char-wrap for CJK."""
    if not text:
        return []
    cjk = sum(1 for ch in text if _is_cjk(ch) and ch.strip())
    total = max(sum(1 for ch in text if ch.strip()), 1)
    return _wrap_chars(text, font, max_w) if cjk / total > 0.5 else _wrap_words(text, font, max_w)

def _wrap_words(text, font, max_w):
    lines, cur = [], ""
    for w in text.split():
        test = f"{cur} {w}".strip()
        if font.getbbox(test)[2] <= max_w:
            cur = test
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines or [text]

def _wrap_chars(text, font, max_w):
    lines, cur = [], ""
    for ch in text:
        if font.getbbox(cur + ch)[2] <= max_w:
            cur += ch
        else:
            if cur.strip():
                lines.append(cur)
            cur = ch
    if cur.strip():
        lines.append(cur)
    return lines or [text]

def _bottom_brand(draw):
    if not BRAND and not LOGO_PATH:
        return
    # Logo
    logo_x = 0
    if LOGO_PATH and LOGO_PATH.exists():
        try:
            logo = Image.open(LOGO_PATH).convert("RGBA")
            lh = 60
            lw = int(logo.width * lh / logo.height)
            logo = logo.resize((lw, lh), Image.LANCZOS)
            ly = H - MB - lh - 10
            draw._image.paste(logo, (MX, ly), logo)
            logo_x = lw + 16
        except Exception:
            pass
    # Brand text
    if BRAND:
        bf = _font(FS["brand"])
        draw.text((MX + logo_x, H - MB), BRAND, fill=CLR["gray"], font=bf)

# ═══════════════════════════════════════════════
# RENDERERS
# ═══════════════════════════════════════════════

def render_portada(slide):
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    # Badge — from slide data, fallback to BRAND
    badge = slide.get("badge", f"{BRAND} · Verbos")
    bd = _font(FS["small"])
    d.text((W - MX, MY), badge,
           fill=CLR["gold"], font=bd, anchor="rt")

    # Chapter number (below badge) — from slide data
    cap_text = slide.get("capitulo_texto", "")
    if not cap_text:
        cap = slide.get("capitulo")
        if cap:
            cap_text = f"第{cap:03d}课"
    if cap_text:
        cf = _font(FS["brand"])
        d.text((W - MX, MY + FS["small"] + 12), cap_text,
               fill=CLR["gray"], font=cf, anchor="rt")

    # Spanish title — big, centered
    es = slide.get("titulo_es", "")
    if es:
        ef = _font(FS["hero"])
        lines = _wrap_words(es, ef, int(W * 0.65))
        total_h = len(lines) * (FS["hero"] + LS["hero"])
        y = (H - total_h) // 2 - 80
        for ln in lines:
            d.text((_cx(d, ln, ef), y), ln, fill=CLR["white"], font=ef)
            y += FS["hero"] + LS["hero"]

    # Chinese subtitle
    zh = slide.get("titulo_zh", "")
    if zh:
        zf = _font(FS["heading"])
        lines = _wrap_chars(zh, zf, CW)
        y = H // 2 + 40
        for ln in lines:
            d.text((_cx(d, ln, zf), y), ln, fill=CLR["blue"], font=zf)
            y += FS["heading"] + LS["norm"]

    # Line
    ly = y + 50
    d.line([(W//2 - 100, ly), (W//2 + 100, ly)], fill=CLR["gold"], width=3)

    _bottom_brand(d)
    return img


def render_explicacion(slide):
    """Clean card: Chinese header + Spanish example highlighted inside, bullets below."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    y = MY

    # ── Header: section label ──
    titulo = slide.get("titulo_zh", "")
    if titulo:
        tf = _font(FS["heading"])
        d.text((_cx(d, titulo, tf), y), titulo, fill=CLR["gold"], font=tf)
        y += FS["heading"] + LS["wide"]
    y += 14

    # ── Spanish phrase — highlighted card ──
    frase = slide.get("frase_es", "")
    if frase:
        sf = _font(FS["hero"])
        lines = _wrap_words(frase, sf, CW - 60)
        card_h = len(lines) * (FS["hero"] + LS["hero"]) + 50
        _card(d, MX, y, CW, card_h, radius=20, fill=CLR["card_blue"])
        sy = y + 26
        for ln in lines:
            d.text((_cx(d, ln, sf), sy), ln, fill=CLR["white"], font=sf)
            sy += FS["hero"] + LS["hero"]
        y += card_h + 20

    # ── Chinese translation ──
    trad = slide.get("traduccion_zh", "")
    if trad:
        tzf = _font(FS["body"])
        lines = _wrap_chars(trad, tzf, CW - 60)
        card_h = len(lines) * (FS["body"] + LS["norm"]) + 32
        _card(d, MX, y, CW, card_h, radius=16, fill=CLR["card_dark"])
        ty = y + 16
        for ln in lines:
            d.text((_cx(d, ln, tzf), ty), ln, fill=CLR["light"], font=tzf)
            ty += FS["body"] + LS["norm"]
        y += card_h + 18

    # ── Bullet points ──
    puntos = slide.get("puntos", [])
    puntos = [p for p in puntos if p and p.strip() and not p.startswith("Punto")]
    if puntos:
        bf = _font(FS["body"])
        lh = FS["body"] + LS["norm"]

        for pt in puntos:
            pt_lines = _wrap(pt, bf, CW - 60)
            ch = len(pt_lines) * lh + 28
            if y + ch > H - MB - 10:
                break
            _card(d, MX, y, CW, ch, radius=14, fill=CLR["card_dark"])
            # Gold dot
            r = 5
            d.ellipse((MX + 18, y + ch//2 - r, MX + 18 + r*2, y + ch//2 + r),
                      fill=CLR["gold"])
            ty = y + (ch - len(pt_lines) * lh) // 2
            for ln in pt_lines:
                d.text((MX + 42, ty), ln, fill=CLR["white"], font=bf)
                ty += lh
            y += ch + 12

    _bottom_brand(d)
    return img


def render_ejemplo(slide):
    """Spanish quote prominently, Chinese translation below, analysis chips."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    # Label
    lf = _font(FS["small"])
    d.text((MX, MY), "Ejemplo", fill=CLR["gold"], font=lf)

    y = MY + 56

    # Spanish phrase card
    frase = slide.get("frase_es", "")
    if frase:
        sf = _font(FS["hero"])
        lines = _wrap_words(frase, sf, CW - 60)
        card_h = len(lines) * (FS["hero"] + LS["hero"]) + 50
        _card(d, MX, y, CW, card_h, radius=20, fill=CLR["card_blue"])
        sy = y + 26
        for ln in lines:
            d.text((_cx(d, ln, sf), sy), ln, fill=CLR["white"], font=sf)
            sy += FS["hero"] + LS["hero"]
        y += card_h + 18

    # Chinese translation
    trad = slide.get("traduccion_zh", "")
    if trad:
        tzf = _font(FS["body"])
        lines = _wrap_chars(trad, tzf, CW - 50)
        card_h = len(lines) * (FS["body"] + LS["norm"]) + 32
        _card(d, MX, y, CW, card_h, radius=16, fill=CLR["card_dark"])
        ty = y + 16
        for ln in lines:
            d.text((_cx(d, ln, tzf), ty), ln, fill=CLR["light"], font=tzf)
            ty += FS["body"] + LS["norm"]
        y += card_h + 16

    # Analysis chips
    analisis = slide.get("analisis", [])
    analisis = [a for a in analisis if a and a.strip()]
    if analisis:
        af = _font(FS["small"])
        chip_h = 46
        for item in analisis:
            if y + chip_h > H - MB - 10:
                break
            _card(d, MX, y, CW, chip_h, radius=12, fill=CLR["card_dark"])
            d.text((MX + 20, y + chip_h//2), f"  {item}",
                   fill=CLR["gray"], font=af, anchor="lm")
            y += chip_h + 8

    _bottom_brand(d)
    return img


def render_ejercicio(slide):
    """Exercise drill: fill-in-the-blank + hint + options."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    # Label
    lf = _font(FS["small"])
    d.text((MX, MY), "Ejercicio", fill=CLR["gold"], font=lf)

    y = MY + 62

    # Exercise phrase
    frase = slide.get("frase_es", "")
    if frase:
        sf = _font(FS["hero"])
        lines = _wrap_words(frase, sf, CW - 60)
        card_h = len(lines) * (FS["hero"] + LS["hero"]) + 50
        _card(d, MX, y, CW, card_h, radius=20, fill=CLR["card_blue"])
        sy = y + 26
        for ln in lines:
            d.text((_cx(d, ln, sf), sy), ln, fill=CLR["white"], font=sf)
            sy += FS["hero"] + LS["hero"]
        y += card_h + 18

    # Hint
    trad = slide.get("traduccion_zh", "")
    if trad:
        tzf = _font(FS["body"])
        lines = _wrap_chars(trad, tzf, CW - 50)
        card_h = len(lines) * (FS["body"] + LS["norm"]) + 32
        _card(d, MX, y, CW, card_h, radius=16, fill=CLR["card_dark"])
        ty = y + 16
        for ln in lines:
            d.text((_cx(d, ln, tzf), ty), ln, fill=CLR["light"], font=tzf)
            ty += FS["body"] + LS["norm"]
        y += card_h + 16

    # Options
    analisis = slide.get("analisis", [])
    analisis = [a for a in analisis if a and a.strip()]
    if analisis:
        af = _font(FS["small"])
        chip_h = 46
        for item in analisis:
            if y + chip_h > H - MB - 10:
                break
            _card(d, MX, y, CW, chip_h, radius=12, fill=CLR["card_dark"])
            d.text((MX + 20, y + chip_h//2), f"  {item}",
                   fill=CLR["gold"], font=af, anchor="lm")
            y += chip_h + 8

    _bottom_brand(d)
    return img


def render_comparacion(slide):
    """Two-column comparison."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    titulo = slide.get("titulo_zh", "Comparacion")
    tf = _font(FS["heading"])
    tlines = _wrap_chars(titulo, tf, CW)
    y = MY
    for ln in tlines:
        d.text((_cx(d, ln, tf), y), ln, fill=CLR["gold"], font=tf)
        y += FS["heading"] + LS["tight"]
    y += 20

    gap = 24
    col_w = (CW - gap) // 2
    col_h = 340

    lx = MX
    rx = W - MX - col_w
    lf = _font(FS["small"])
    bf = _font(FS["body"])

    # Left — Indefinido
    _card(d, lx, y, col_w, col_h, radius=16, fill=CLR["card_blue"])
    d.text((lx + col_w//2, y + 14), "Indefinido", fill=CLR["white"], font=lf, anchor="mt")
    indef = slide.get("indefinido", "")
    if indef:
        ilines = _wrap(indef, bf, col_w - 30)
        iy = y + 55
        for ln in ilines:
            d.text((lx + col_w//2, iy), ln, fill=CLR["white"], font=bf, anchor="mt")
            iy += FS["body"] + LS["norm"]

    # Right — Imperfecto
    _card(d, rx, y, col_w, col_h, radius=16, fill=CLR["card_coral"])
    d.text((rx + col_w//2, y + 14), "Imperfecto", fill=CLR["white"], font=lf, anchor="mt")
    impf = slide.get("imperfecto", "")
    if impf:
        ilines = _wrap(impf, bf, col_w - 30)
        iy = y + 55
        for ln in ilines:
            d.text((rx + col_w//2, iy), ln, fill=CLR["white"], font=bf, anchor="mt")
            iy += FS["body"] + LS["norm"]

    # VS
    vsf = _font(FS["body"])
    d.text((W // 2, y + col_h // 2), "VS", fill=CLR["gold"], font=vsf, anchor="mm")

    _bottom_brand(d)
    return img


def render_resumen(slide):
    """Summary: numbered recap cards."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    titulo = slide.get("titulo_zh", "Resumen")
    tf = _font(FS["heading"])
    tlines = _wrap_chars(titulo, tf, CW)
    y = MY
    for ln in tlines:
        d.text((_cx(d, ln, tf), y), ln, fill=CLR["gold"], font=tf)
        y += FS["heading"] + LS["tight"]
    # Spanish subtitle
    titulo_es = slide.get("titulo_es", "")
    if titulo_es:
        esf = _font(FS["small"])
        d.text((_cx(d, titulo_es, esf), y), titulo_es, fill=CLR["blue"], font=esf)
        y += FS["small"] + LS["tight"]
    y += 20

    puntos = slide.get("puntos", [])
    puntos = [p for p in puntos if p and p.strip() and len(p.strip()) > 2]
    bf = _font(FS["body_zh"])
    lh = FS["body_zh"] + LS["norm"]
    nf = _font(FS["small"])

    for i, pt in enumerate(puntos):
        pt_lines = _wrap_chars(pt, bf, CW - 60)
        ch = len(pt_lines) * lh + 32
        if y + ch > H - MB - 10:
            break
        _card(d, MX, y, CW, ch, radius=14, fill=CLR["card_dark"])
        # Number circle
        nw = 28
        d.ellipse((MX + 16, y + ch//2 - nw//2,
                   MX + 16 + nw, y + ch//2 + nw//2),
                  fill=CLR["gold"])
        d.text((MX + 16 + nw//2, y + ch//2), str(i + 1),
               fill=CLR["bg_top"], font=nf, anchor="mm")
        ty = y + (ch - len(pt_lines) * lh) // 2
        for ln in pt_lines:
            d.text((MX + 56, ty), ln, fill=CLR["white"], font=bf)
            ty += lh
        y += ch + 12

    _bottom_brand(d)
    return img


def render_outro(slide):
    """CTA outro slide."""
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    texto = slide.get("texto_zh", slide.get("titulo_zh", ""))
    if texto:
        cf = _font(FS["hero_zh"])
        lines = _wrap_chars(texto, cf, CW)
        total_h = len(lines) * (FS["hero_zh"] + LS["norm"])
        y = (H - total_h) // 2 - 60
        for ln in lines:
            d.text((_cx(d, ln, cf), y), ln, fill=CLR["white"], font=cf)
            y += FS["hero_zh"] + LS["norm"]

    cta = slide.get("cta", "Like & Subscribe")
    sf = _font(FS["body"])
    d.text((W // 2, H // 2 + 60), cta,
           fill=CLR["gray"], font=sf, anchor="mt")

    brand_line = slide.get("brand_line", f"{BRAND} · Un verbo al día")
    d.text((W // 2, H - MB),
           brand_line,
           fill=CLR["gray"], font=sf, anchor="mb")
    return img


def render_conjugacion(slide):
    """
    Verb conjugation table — the core visual for xhs-verbos-bot.
    6 rows in a clean dark-card layout: persona | pronombre | forma.
    """
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    y = MY

    # ── Header ──
    titulo = slide.get("titulo_zh", "现在时变位")
    tf = _font(FS["heading"])
    tlines = _wrap_chars(titulo, tf, CW)
    for ln in tlines:
        d.text((_cx(d, ln, tf), y), ln, fill=CLR["gold"], font=tf)
        y += FS["heading"] + LS["tight"]

    # Tiempo label
    tiempo = slide.get("tiempo", "presente")
    sf = _font(FS["small"])
    d.text((W // 2, y + 4), f"({tiempo})", fill=CLR["gray"], font=sf, anchor="mt")
    y += FS["small"] + 30

    # ── Conjugation rows ──
    conjugacion = slide.get("conjugacion", [])
    if not conjugacion:
        return img

    # Calculate row height based on available space
    remaining_h = H - y - MB - 20
    row_h = min(110, max(80, remaining_h // max(len(conjugacion), 1)))
    gap = 10

    # Fonts
    pf = _font(FS["body"])       # persona (Spanish, restored)
    zf = _font(FS["body_zh"])    # pronombre (Chinese)
    ff = _font(FS["hero"])       # forma (conjugated verb, bigger)

    for i, entry in enumerate(conjugacion):
        if y + row_h > H - MB:
            break

        fill = CLR["card_blue"] if i % 2 == 0 else CLR["card_dark"]
        _card(d, MX, y, CW, row_h, radius=14, fill=fill)

        cy = y + row_h // 2

        # Column widths: persona 30%, pronombre 24%, forma 46%
        col1_w = int(CW * 0.30)
        col2_w = int(CW * 0.24)

        # Persona (left) — abbreviated for display
        persona = entry.get("persona", "")
        persona_abbr = {
            "él/ella/usted": "él/ella/Ud.",
            "ellos/ellas/ustedes": "ellos/ellas/Uds.",
            "nosotros/as": "nosotros/as",
            "vosotros/as": "vosotros/as",
        }.get(persona, persona)
        d.text((MX + 16, cy), persona_abbr, fill=CLR["white"], font=pf, anchor="lm")

        # Pronombre (center)
        pronombre = entry.get("pronombre", "")
        center_x = MX + col1_w + col2_w // 2
        d.text((center_x, cy), pronombre, fill=CLR["gray"], font=zf, anchor="mm")

        # Forma (right, highlighted)
        forma = entry.get("forma", "")
        ff = _font(FS["hero"])
        d.text((W - MX - 16, cy), forma, fill=CLR["gold"], font=ff, anchor="rm")

        y += row_h + gap

    _bottom_brand(d)
    return img


def render_xiaohongshu_portada(slide):
    """
    Xiaohongshu-style cover — clean, high-contrast, readable on mobile.
    Content driven by slide data (editable via YAML/dashboard).
    """
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)

    # ── Deep gradient background (dark, high-contrast base) ──
    bg_top = (18, 8, 30)
    bg_mid = (45, 12, 55)
    bg_bot = (20, 8, 40)
    for y in range(H):
        t = y / H
        r = int(bg_top[0] * (1 - t) + bg_mid[0] * (1 - abs(t * 2 - 1)) + bg_bot[0] * t)
        g = int(bg_top[1] * (1 - t) + bg_mid[1] * (1 - abs(t * 2 - 1)) + bg_bot[1] * t)
        b = int(bg_top[2] * (1 - t) + bg_mid[2] * (1 - abs(t * 2 - 1)) + bg_bot[2] * t)
        d.line([(0, y), (W, y)], fill=(r, g, b))

    # ── Top accent glow ──
    for cy in range(0, 280, 4):
        alpha = int(70 * (1 - cy / 280))
        d.line([(0, cy), (W, cy)], fill=(200, 60, 30, alpha))

    # ── Top badge ──
    bd = _font(FS["small"])
    badge_text = "Hola西班牙语 · Verbos"
    badge_w = bd.getbbox(badge_text)[2] + 30
    _card(d, MX, MY - 5, badge_w, 50, radius=20, fill=(0, 0, 0, 180))
    d.text((MX + 15, MY + 8), badge_text, fill=(255, 200, 50), font=bd)

    # ── CHAPTER NUMBER ──
    capitulo = slide.get("capitulo")
    chapter_y = MY + 42  # below badge
    if capitulo is not None:
        # chapter label
        cf_label = _font(28)
        label = "Capítulo"
        d.text((W // 2, chapter_y + 10), label, fill=(255, 200, 50, 180), font=cf_label, anchor="mt")
        # chapter number — big and bold
        cf_num = _font(120)
        num_text = str(capitulo).zfill(3) if capitulo < 100 else str(capitulo)
        d.text((W // 2 + 2, chapter_y + 48 + 2), num_text,
               fill=(0, 0, 0, 100), font=cf_num, anchor="mt")
        d.text((W // 2, chapter_y + 48), num_text,
               fill=(255, 255, 255), font=cf_num, anchor="mt")
        # thin gold line under chapter number
        line_y = chapter_y + 48 + 60 + 16
        d.line([(W // 2 - 60, line_y), (W // 2 + 60, line_y)],
               fill=(255, 200, 50, 120), width=2)
        # push title down
        title_extra_offset = 220
    else:
        title_extra_offset = 20

    # ── MAIN TITLE: big Chinese, centered ──
    titulo_es = (slide.get("titulo_es") or "").strip()
    titulo_zh = (slide.get("titulo_zh") or "").strip()
    theme_zh = titulo_zh
    for prefix in ["Hola西班牙语 · ", "Hola 西班牙语 · "]:
        if theme_zh.startswith(prefix):
            theme_zh = theme_zh[len(prefix):].strip()
    if not theme_zh:
        theme_zh = titulo_es
    if not theme_zh:
        theme_zh = "学西班牙语"

    tf = _font(84)
    lines = _wrap_chars(theme_zh, tf, int(W * 0.82))
    total_h = len(lines) * (84 + LS["hero"])
    title_y = int(H * 0.24) - total_h // 2 + title_extra_offset

    for ln in lines:
        d.text((_cx(d, ln, tf) + 3, title_y + 3), ln,
               fill=(0, 0, 0, 120), font=tf)
        d.text((_cx(d, ln, tf), title_y), ln,
               fill=(255, 255, 255), font=tf)
        title_y += 84 + LS["hero"]

    # ── Spanish-flag accent bar under title ──
    bar_y = title_y + 8
    bar_w = 200
    d.line([(W//2 - bar_w//2, bar_y), (W//2 + bar_w//2, bar_y)],
           fill=(255, 50, 50), width=5)
    d.line([(W//2 - bar_w//2 + 50, bar_y - 2), (W//2 + bar_w//2 - 50, bar_y + 2)],
           fill=(255, 200, 50), width=4)
    title_y = bar_y + 20

    # ── Spanish subtitle ──
    if titulo_es:
        sf = _font(50)
        d.text((W // 2, title_y + 16), titulo_es[:40],
               fill=(255, 180, 120), font=sf, anchor="mt")
        title_y += 50 + 40
    else:
        title_y += 20

    # ── Hook line on solid dark pill ──
    hook = (slide.get("hook_zh") or "").strip()
    if not hook:
        hook = "每天5分钟 · 轻松学西语 · A1零基础友好"
    hf = _font(36)
    hook_y = title_y + 20
    hook_w = hf.getbbox(hook)[2] + 48
    _card(d, (W - hook_w) // 2, hook_y, hook_w, 56,
          radius=28, fill=(0, 0, 0, 180))
    d.text((W // 2, hook_y + 12), hook,
           fill=(255, 200, 50), font=hf, anchor="mt")

    # ── Benefit bullets (clean list on solid dark cards) ──
    bullets_raw = slide.get("bullets") or []
    if isinstance(bullets_raw, list) and len(bullets_raw) > 0:
        if isinstance(bullets_raw[0], str):
            bullets_raw = [{"title": b, "sub": ""} for b in bullets_raw]
    if not bullets_raw:
        bullets_raw = [
            {"title": "零基础入门", "sub": "从Hola开始", "icon": "book"},
            {"title": "DELE官方标准", "sub": "A1全套课程", "icon": "target"},
            {"title": "每天更新", "sub": "打卡学西语", "icon": "fire"},
        ]

    bullets_raw = bullets_raw[:3]
    n = len(bullets_raw)
    bf = _font(36)
    sbf = _font(26)
    bullet_start_y = hook_y + 82
    col_w = (CW - 32) // max(n, 1)

    for i, b in enumerate(bullets_raw):
        if isinstance(b, dict):
            b_title = b.get("title", "")
            b_sub = b.get("sub", "")
            b_icon = b.get("icon", "dot")
        else:
            b_title = str(b)
            b_sub = ""
            b_icon = "dot"

        bx = MX + i * (col_w + 16)
        if n == 1:
            bx = (W - col_w) // 2

        # Solid dark card
        _card(d, bx, bullet_start_y, col_w, 130,
              radius=14, fill=(0, 0, 0, 160))
        icon_cx = bx + col_w // 2
        _draw_bullet_icon(d, icon_cx, bullet_start_y + 28, b_icon)
        d.text((bx + col_w // 2, bullet_start_y + 68), b_title,
               fill=(255, 255, 255), font=bf, anchor="mt")
        if b_sub:
            d.text((bx + col_w // 2, bullet_start_y + 102), b_sub,
                   fill=(180, 180, 200), font=sbf, anchor="mt")

    # ── CTA at bottom with finger icon ──
    cta = (slide.get("cta") or "").strip()
    if not cta:
        cta = "点击收藏 · 开始你的西语之旅"
    cta_f = _font(36)
    cta_y = H - 160
    cta_text_w = cta_f.getbbox(cta)[2]
    finger_s = 30
    total_w = finger_s + 16 + cta_text_w
    cta_start = (W - total_w) // 2
    _draw_point_up_icon(d, cta_start + finger_s // 2, cta_y, finger_s)
    d.text((cta_start + finger_s + 16, cta_y), cta,
           fill=(255, 220, 180), font=cta_f, anchor="lm")

    # Brand
    d.text((W // 2, H - 80), "Hola西班牙语",
           fill=(180, 180, 200), font=_font(FS["brand"]), anchor="mt")

    return img

# ── Icon drawing helpers (PIL primitives, no emoji font needed) ──

def _draw_bullet_icon(d, cx, cy, icon, scale=1.0):
    """Draw a bullet icon centered at (cx, cy)."""
    gold = (255, 200, 50)
    white_20 = (255, 255, 255, 50)
    if icon == "book":
        # Open book
        s = 14
        d.rectangle((cx - s + 2, cy - s + 4, cx - 2, cy + s - 2), fill=None, outline=gold, width=3)
        d.rectangle((cx + 2, cy - s + 4, cx + s - 2, cy + s - 2), fill=None, outline=gold, width=3)
        d.line((cx, cy - s + 4, cx, cy + s - 2), fill=gold, width=2)
    elif icon == "target":
        # Concentric circles
        for r, f in [(16, white_20), (10, None), (4, gold)]:
            if f is None:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=gold, width=2)
            else:
                d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=f, outline=gold, width=2)
        d.ellipse((cx - 2, cy - 2, cx + 2, cy + 2), fill=gold)
    elif icon == "fire":
        # Stylized flame with 3 teardrops
        s = 16
        d.ellipse((cx - s//2, cy - s, cx + s//2, cy), fill=gold)
        d.ellipse((cx - s + 6, cy - s//2, cx + s - 6, cy + s//2), fill=gold)
        d.polygon([(cx, cy + s//2), (cx - 4, cy + s - 4), (cx + 4, cy + s - 4)], fill=gold)
    elif icon == "star":
        # 5-pointed star
        s = 16
        import math
        pts = []
        for j in range(10):
            a = math.pi / 2 + j * math.pi / 5
            r = s if j % 2 == 0 else s * 0.4
            pts.append((cx + r * math.cos(a), cy - r * math.sin(a)))
        d.polygon(pts, fill=gold)
    elif icon == "check":
        # Checkmark
        s = 12
        d.line([(cx - s, cy), (cx - 3, cy + s - 3), (cx + s, cy - s + 3)], fill=gold, width=4)
    else:
        # Default: gold dot
        dot_r = 10
        d.ellipse((cx - dot_r, cy - dot_r, cx + dot_r, cy + dot_r), fill=gold)


def _draw_point_up_icon(d, cx, cy, size):
    """Draw a pointing-up finger icon at (cx, cy)."""
    gold = (255, 200, 50)
    h = size
    w = size * 0.55
    # Hand shape: rounded rectangle palm + pointing finger
    # Finger (index pointing up)
    finger_w = w * 0.4
    d.rounded_rectangle((cx - finger_w, cy - h * 0.55, cx + finger_w, cy + h * 0.15),
                        radius=6, fill=gold)
    # Palm
    palm_w = w * 0.55
    d.rounded_rectangle((cx - palm_w, cy + h * 0.05, cx + palm_w, cy + h * 0.45),
                        radius=8, fill=gold)


def _draw_circle(draw, cx, cy, r, fill):
    """Draw a circle (PIL doesn't have circle primitive)."""
    draw.ellipse((cx - r, cy - r, cx + r, cy + r), fill=fill)


def render_vocabulario(slide):
    """
    Word-by-word vocabulary breakdown.
    Shows original phrase + each word with Chinese translation.
    Word highlighting is done via video subtitles, not in the static image.
    """
    img = Image.new("RGBA", (W, H))
    d = ImageDraw.Draw(img)
    _bg(d)

    y = MY

    # ── Header: section label ──
    tf = _font(FS["heading"])
    d.text((_cx(d, "词汇分解", tf), y), "词汇分解", fill=CLR["gold"], font=tf)
    y += FS["heading"] + LS["tight"]

    # ── Original phrase subtitle ──
    frase_origen = slide.get("frase_origen", "")
    if frase_origen:
        sf = _font(FS["small"])
        display_frase = f'«{frase_origen}»'[:60]
        d.text((_cx(d, display_frase, sf), y), display_frase,
               fill=CLR["gray"], font=sf)
        y += FS["small"] + LS["wide"]

    y += 20

    # ── Word cards ──
    palabras = slide.get("palabras", [])
    if not palabras:
        return img

    bf = _font(FS["hero"])       # Spanish word — big
    zf = _font(FS["body_zh"])    # Chinese translation
    lh = FS["hero"] + LS["hero"]

    card_x = MX + 20
    card_w = CW - 40

    for word_data in palabras:
        word_es = word_data.get("es", "")
        word_zh = word_data.get("zh", "")

        if not word_es:
            continue

        # Calculate row height based on text wrapping
        es_lines = _wrap_words(word_es, bf, card_w - 120)
        zh_lines = _wrap_chars(word_zh, zf, card_w - 120)
        row_h = max(
            len(es_lines) * (FS["hero"] + LS["hero"]),
            len(zh_lines) * (FS["body_zh"] + LS["norm"])
        ) + 24

        if y + row_h > H - MB - 10:
            break

        # Subtle card background
        _card(d, card_x, y, card_w, row_h, radius=14, fill=CLR["card_dark"])

        # Spanish word (left/center)
        es_y = y + (row_h - len(es_lines) * (FS["hero"] + LS["hero"])) // 2
        for ln in es_lines:
            d.text((card_x + 30, es_y), ln, fill=CLR["white"], font=bf)
            es_y += FS["hero"] + LS["hero"]

        # Chinese translation (right)
        zh_y = y + (row_h - len(zh_lines) * (FS["body_zh"] + LS["norm"])) // 2
        for ln in zh_lines:
            d.text((card_x + card_w - 30, zh_y), ln,
                   fill=CLR["blue"], font=zf, anchor="ra")
            zh_y += FS["body_zh"] + LS["norm"]

        y += row_h + 8

    _bottom_brand(d)
    return img


# ═══════════════════════════════════════════════
# ROUTER
# ═══════════════════════════════════════════════

RENDERERS = {
    "portada": render_xiaohongshu_portada,
    "xiaohongshu_portada": render_xiaohongshu_portada,
    "explicacion": render_explicacion,
    "ejemplo": render_ejemplo,
    "comparacion": render_comparacion,
    "ejercicio": render_ejercicio,
    "resumen": render_resumen,
    "outro": render_outro,
    "vocabulario": render_vocabulario,
    "conjugacion": render_conjugacion,
}


def render_slide(slide: Slide) -> Image.Image:
    # Strip emojis from content (CJK fonts lack emoji glyphs)
    for key in list(slide.contenido.keys()):
        val = slide.contenido[key]
        if isinstance(val, str):
            slide.contenido[key] = _strip_emoji(val)
        elif isinstance(val, list):
            slide.contenido[key] = [_strip_emoji(v) if isinstance(v, str) else v for v in val]
    renderer = RENDERERS.get(slide.tipo)
    if renderer is None:
        raise ValueError(f"Unknown slide type: {slide.tipo}")
    return renderer(slide)


def render_all_slides(script: VideoScript, output_dir: str | Path) -> list[Path]:
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    paths = []
    for i, slide in enumerate(script.slides):
        img = render_slide(slide)
        out_path = output_dir / f"slide_{i:03d}.png"
        img.save(out_path, "PNG")
        paths.append(out_path)
    return paths
