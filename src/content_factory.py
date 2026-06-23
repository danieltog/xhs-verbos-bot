#!/usr/bin/env python3
"""
Content Factory — genera scripts YAML desde el currículo estructurado.
Produce TTS limpio: chino puro o español puro, nunca mezclado.
"""
import re
from pathlib import Path
import yaml
import os
import json
import urllib.request

PROJECT_ROOT = Path(__file__).resolve().parent.parent
from .contenido_a1 import A1_CURRICULO

# ── LLM Translation Cache ──
_LLM_TRANSLATION_CACHE: dict[str, str] = {}  # word_lower → zh_translation
MOONSHOT_API_KEY = os.environ.get("MOONSHOT_API_KEY", "")
MOONSHOT_API_URL = "https://api.moonshot.cn/v1/chat/completions"


def _llm_translate_words(words: list[str], context_phrase: str = "") -> dict[str, str]:
    """
    Use Moonshot/Kimi LLM to translate Spanish words to Chinese.
    Returns dict of {word_lower: chinese_translation}.
    Results are cached in memory to avoid repeated API calls.
    """
    # Filter out words already cached
    uncached = [w for w in words if w.lower() not in _LLM_TRANSLATION_CACHE]
    if not uncached:
        return {w.lower(): _LLM_TRANSLATION_CACHE[w.lower()] for w in words}
    
    if not MOONSHOT_API_KEY:
        print("  ⚠ No MOONSHOT_API_KEY — usando diccionario local")
        return {}

    word_list = ", ".join(uncached)
    ctx_line = f"Context (for reference only, do NOT translate this): {context_phrase}\\n" if context_phrase else ""
    
    system_prompt = (
        "You translate Spanish words to Chinese for a DELE A1 learning app. "
        "Spanish has grammatical GENDER that Chinese lacks. "
        "Mark gender for nouns/adjectives: translate as 词义(性别). "
        "GENDER RULES YOU MUST FOLLOW:\n"
        "  1. Words ending in -o/-or → masculine (阳性): guapo=帅(阳性), profesor=老师(阳性)\n"
        "  2. Words ending in -a/-ora → feminine (阴性): guapa=漂亮(阴性), profesora=老师(阴性)\n"
        "  3. Words ending in -E, -ISTA, -NTE → GENDER-NEUTRAL (性别中性): estadounidense=美国人(性别中性), inteligente=聪明(性别中性), amable=友好(性别中性), estudiante=学生(性别中性)\n"
        "  4. Words with BOTH forms: mexicano=墨西哥人(阳性), mexicana=墨西哥人(阴性)\n"
        "  5. For grammar terms: Masculino=阳性, Femenino=阴性\n"
        "  6. For prepositions etc: de=的, vs=对比. No gender needed.\n"
        "IMPORTANT: Translate ONLY the words after 'WORDS TO TRANSLATE:'. Nothing else. "
        "Output EXACTLY one line per word: spanish=chinese. No markdown, no explanations."
    )
    user_prompt = f"{ctx_line}WORDS TO TRANSLATE:\\n{word_list}"
    
    payload = json.dumps({
        "model": "moonshot-v1-8k",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        "temperature": 0.1,
        "max_tokens": len(uncached) * 30,
    }).encode()
    
    try:
        req = urllib.request.Request(MOONSHOT_API_URL, data=payload, headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {MOONSHOT_API_KEY}",
        })
        with urllib.request.urlopen(req, timeout=15) as resp:
            result = json.loads(resp.read())
        text = result["choices"][0]["message"]["content"]
        
        # Parse: "Spanish=Chinese" lines
        translations = {}
        for line in text.strip().split("\n"):
            line = line.strip()
            if "=" in line:
                es, zh = line.split("=", 1)
                translations[es.strip().lower()] = zh.strip()
        
        # Cache results
        _LLM_TRANSLATION_CACHE.update(translations)
        print(f"  🤖 LLM tradujo {len(translations)} palabras: {list(translations.keys())[:5]}...")
    except Exception as e:
        print(f"  ⚠ LLM translation failed: {e}")
        translations = {}
    
    # Include cached translations for words we didn't need to call the API for
    for w in words:
        wl = w.lower()
        if wl not in translations and wl in _LLM_TRANSLATION_CACHE:
            translations[wl] = _LLM_TRANSLATION_CACHE[wl]
    
    return translations


def load_curriculo() -> dict:
    return A1_CURRICULO


# ── Language filtering ──

# Regex to detect Spanish/Latin characters in Chinese text
SPANISH_CHARS = re.compile(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ¿¡]+')


def extract_chinese_only(text: str) -> str:
    """Extract only Chinese text for clean Chinese TTS.
    Removes ALL Latin chars, Spanish special chars, and stray punctuation."""
    # Remove all ASCII letters and Spanish special chars
    cleaned = SPANISH_CHARS.sub('', text)
    # Remove list markers, emojis, stray ASCII punctuation (?! etc)
    cleaned = re.sub(r'[✅❌•·▶️⚡📖💡💬✏️🔊🔤📝🎯📍📌👥👋🎬🔄⭐❤👍👇?!¡¿]+', '', cleaned)
    # Remove arrows
    cleaned = re.sub(r'[→←↑↓]', '', cleaned)
    # Replace em dashes with Chinese comma for natural TTS pause
    cleaned = cleaned.replace('—', '，')
    cleaned = cleaned.replace('–', '，')
    # Remove any remaining ASCII punctuation/symbols
    cleaned = re.sub(r'[\u0020-\u002F\u003A-\u0040\u005B-\u0060\u007B-\u007E]+', '', cleaned)
    # Remove excessive spaces
    cleaned = re.sub(r'\s+', '', cleaned)
    # Clean up leading/trailing punctuation
    cleaned = re.sub(r'^[，,、。]+', '', cleaned)
    cleaned = re.sub(r'[，,、。]+$', '', cleaned)
    return cleaned.strip() or "学习西班牙语"


def make_zh_tts(text: str, max_len: int = 200) -> str:
    """Generate a clean Chinese-only TTS text."""
    return extract_chinese_only(text)[:max_len]


def make_es_tts(text: str) -> str:
    """Generate clean Spanish TTS text (remove Chinese, punctuation artifacts)."""
    # Remove CJK characters and Chinese punctuation
    cleaned = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef（）「」【】《》]', ' ', text)
    # Remove characters the TTS pronounces literally
    cleaned = cleaned.replace('—', ' ')
    cleaned = cleaned.replace('–', ' ')
    cleaned = cleaned.replace('«', '')
    cleaned = cleaned.replace('»', '')
    cleaned = re.sub(r'_+', ' ', cleaned)         # underscores → space
    cleaned = cleaned.replace('*', '')
    cleaned = cleaned.replace('#', '')
    # Remove chars that TTS pronounces literally: / \ - —
    cleaned = cleaned.replace('/', ' ')
    cleaned = cleaned.replace('\\', ' ')
    cleaned = cleaned.replace('—', ',')
    cleaned = cleaned.replace('–', ',')
    # Remove stray digits
    cleaned = re.sub(r'\b\d+\b', '', cleaned)
    # Replace known placeholders with real Spanish words (TTS nunca debe leer corchetes)
    # Género balanceado: nombres alternan masculino/femenino
    _GENDER_BALANCED = {"[nombre]": ("Pedro", "María")}  # alterna M/F
    _FIXED_MAP = {
        "[nombre1]": "Ana", "[nombre2]": "Juan",       # F y M fijos
        "[lugar]": "Madrid", "[ciudad]": "Barcelona", "[país]": "México",
        "[número]": "seis", "[edad]": "veinticinco", "[hora]": "las tres",
        "[comida]": "paella", "[color]": "rojo", "[objeto]": "libro",
        "[profesión]": "profesora", "[verbo]": "hablar",
        "[día]": "lunes", "[mes]": "enero",
    }
    for ph, rep in _FIXED_MAP.items():
        cleaned = cleaned.replace(ph, rep)
    # Gender-balanced: rotate through male/female
    _gb_counter = getattr(make_es_tts, '_gb_counter', 0)
    for ph, pair in _GENDER_BALANCED.items():
        if ph in cleaned:
            cleaned = cleaned.replace(ph, pair[_gb_counter % len(pair)])
            _gb_counter += 1
    make_es_tts._gb_counter = _gb_counter
    # For phonetic notation like [a] [e] [k], just remove brackets
    cleaned = re.sub(r'\[([a-zA-Záéíóúüñ])\]', r'\1', cleaned)
    # Remove any remaining bracket placeholders like [algo] or {algo}
    cleaned = re.sub(r'\[[^\]]*\]', '', cleaned)
    cleaned = re.sub(r'\{[^\}]*\}', '', cleaned)
    # Clean up stray commas and spaces
    cleaned = re.sub(r'\s*,\s*,+', ',', cleaned)  # double commas
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    cleaned = cleaned.strip(' ，,。.·、/-')
    return cleaned or "Español"


def extract_spanish_only(text: str) -> str:
    """Extract only Spanish/Latin words from mixed text (for TTS)."""
    return make_es_tts(text)
    """Generate clean Spanish TTS text (remove Chinese characters and artifacts)."""
    # Remove CJK characters
    cleaned = re.sub(r'[\u4e00-\u9fff\u3000-\u303f\uff00-\uffef]+', '', text)
    # Replace underscores (exercise blanks) with "espacio" so TTS says it naturally
    cleaned = re.sub(r'_+', ' espacio ', cleaned)
    # Collapse whitespace
    cleaned = re.sub(r'\s+', ' ', cleaned).strip()
    return cleaned or "Español"


def puntos_to_zh_tts(puntos: list[str]) -> str:
    """Convert Chinese bullet points to a clean TTS paragraph."""
    parts = []
    for p in puntos:
        clean = extract_chinese_only(p)
        if clean:
            parts.append(clean)
    return "，".join(parts) if parts else "学习西班牙语"


# ── Script generation (bilingüe: chino + español por slide) ──

def generate_script(leccion: dict, modulo: dict, nivel: str) -> dict:
    """
    Genera slides bilingües: cada slide tiene contenido en chino Y español.
    El TTS alterna entre chino y español para que el estudiante escuche
    ambos idiomas sin mezclarlos en un mismo audio.
    """
    tema = leccion["tema"]
    puntos = leccion.get("puntos", [])
    ejemplos = leccion.get("ejemplos", [])
    ejercicio = leccion.get("ejercicio", {})
    refran = leccion.get("refran", "")
    es_repaso = leccion.get("es_repaso", False)

    slides = []

    # ── 1. Portada ──
    # TTS dual: chino puro para intro, español puro para el tema
    # Ambos se concatenan en el generador (ZH primero, luego ES)
    # Extraer el tema en chino: usar tema_zh del currículo si existe
    tema_zh = leccion.get("tema_zh", "")
    if not tema_zh:
        # Fallback: extraer de la primera frase de la explicación
        expl = leccion.get("explicacion", "")
        if expl:
            first_sentence = re.split(r'[。；]', expl)[0]
            chinese_only = re.findall(r'[\u4e00-\u9fff]+', first_sentence)
            tema_zh = ''.join(chinese_only)[:25] if chinese_only else ''
    if not tema_zh or len(tema_zh) < 4:
        tema_zh = "西班牙语"

    zh_intro = "大家好，欢迎来到今天的西班牙语课堂。" if not es_repaso else "今天我们复习。"
    es_tema = tema
    slides.append({
        "tipo": "portada",
        "titulo_zh": f"Hola西班牙语 · {nivel}",
        "titulo_es": tema,
        "tts": "zh",
        "texto_tts_zh": f"{zh_intro}今天我们来学习：{tema_zh}。准备好你的笔记本，我们开始吧。",
        "texto_tts_es": f"{es_tema}.",
        "hook_zh": "每天5分钟 · 轻松学西语 · A1零基础友好",
        "bullets": [
            {"title": "零基础入门", "sub": "从Hola开始", "icon": "book"},
            {"title": "DELE官方标准", "sub": "A1全套课程", "icon": "target"},
            {"title": "每天更新", "sub": "打卡学西语", "icon": "fire"},
        ],
        "cta": "点击收藏 · 开始你的西语之旅",
    })

    # ── 2-N. Slides bilingües: cada punto = 1 slide con chino + ejemplo español ──
    # Emparejamos cada punto chino con un ejemplo español
    paired = []
    for i, pt in enumerate(puntos):
        ej = ejemplos[i] if i < len(ejemplos) else None
        paired.append((pt, ej))

    # Si hay más ejemplos que puntos, añadirlos al final
    for i in range(len(puntos), len(ejemplos)):
        paired.append(("", ejemplos[i]))

    for i, (pt, ej) in enumerate(paired):
        zh_point = extract_chinese_only(pt) if pt else ""

        # ── Extraer palabra española del PUNTO (siempre debe estar en el TTS) ──
        es_from_pt = extract_spanish_only(pt) if pt else ""

        # Si hay ejemplo, extraer su frase (puede ser distinta del punto)
        ej_frase_clean = make_es_tts(ej.get("frase", "")) if ej else ""
        # ── Solo usar datos del ejemplo si es RELEVANTE (contiene la palabra del punto) ──
        ej_relevante = False
        if ej and es_from_pt and ej_frase_clean:
            ej_relevante = es_from_pt.lower() in ej_frase_clean.lower()

        # Traducción: SIEMPRE preferir la del punto (más precisa), ejemplo como fallback
        trad_zh = ""
        if pt:
            pt_parts = re.split(r'[—\-–]', pt, maxsplit=1)
            if len(pt_parts) > 1:
                candidate = pt_parts[1].strip()
                chinese = re.findall(r'[\u4e00-\u9fff（）/]+', candidate)
                if chinese:
                    trad_zh = ''.join(chinese)[:50]
        if not trad_zh:
            trad_zh = ej.get("traduccion", "") if ej_relevante else ""

        analisis = ej.get("analisis", []) if ej_relevante else []
        ej_frase_clean = ej_frase_clean if ej_relevante else ""

        # ── La frase visible en el slide es la del punto (lo que se está enseñando) ──
        frase_es = es_from_pt if es_from_pt else (ej_frase_clean if ej_frase_clean else "")

        # ── TTS español: solo la palabra del punto. Slide y TTS deben ser idénticos. ──
        tts_es = es_from_pt if es_from_pt else ""

        # ── TTS chino ──
        tts_zh = zh_point if zh_point else ""
        # Si hay ejemplo español pero falta TTS chino
        if not tts_zh and ej:
            tts_zh = "现在我们来学习这个表达。请大家注意听，然后跟我重复。"

        # Expandir TTS
        if tts_zh:
            tts_zh = f"第{i+1}个知识点：{tts_zh}。请仔细听，然后跟我读。"
        if tts_es:
            tts_es = f"{tts_es}。{tts_es}"

        slides.append({
            "tipo": "explicacion" if pt else "ejemplo",
            "titulo_zh": f"Punto {i + 1}" if pt else "Ejemplo",
            "puntos": [pt] if pt else [],
            "frase_es": frase_es,
            "traduccion_zh": trad_zh,
            "analisis": analisis,
            "tts": "zh" if tts_zh else "es",
            "texto_tts_zh": tts_zh,
            "texto_tts_es": tts_es,
        })

        # ── VOCABULARIO: insertar slide de desglose palabra×palabra ──
        # Usar la frase del PUNTO (lo que se está enseñando), no del ejemplo
        if pt and frase_es:
            palabras = _extraer_palabras(es_from_pt, ej.get("analisis", []) if ej else [])
            if palabras and len(palabras) >= 2:
                slides.append({
                    "tipo": "vocabulario",
                    "frase_origen": es_from_pt,
                    "palabras": palabras,
                    "tts": "es",
                    "texto_tts_zh": "现在我们来逐词学习刚才的句子。请仔细听每个单词的发音，然后跟我读。",
                    "texto_tts_es": " ".join(p["es"] for p in palabras),
                })

    # ── Refrán (si existe) ──
    if refran:
        slides.append({
            "tipo": "ejemplo",
            "frase_es": refran,
            "traduccion_zh": refran,
            "analisis": [],
            "tts": "es",
            "texto_tts_zh": "今天我们来学习一句西班牙语谚语。请听好，然后跟我读。",
            "texto_tts_es": make_es_tts(refran),
        })

    # ── Practica extra: solo frases ENSEÑADAS (las del punto, no ejemplos no vistos) ──
    practice_phrases = []
    for pt, ej in paired:
        if not pt:
            continue
        es_pt = extract_spanish_only(pt)
        # La práctica repite lo ENSEÑADO: la palabra del punto
        if es_pt and len(es_pt) > 1:
            practice_phrases.append(es_pt)

    if practice_phrases:
        practice_es = "。".join(practice_phrases[:6])
        slides.append({
            "tipo": "ejemplo",
            "frase_es": "Repite lo aprendido",
            "traduccion_zh": "跟我重复学过的内容",
            "analisis": practice_phrases[:6],
            "tts": "es",
            "texto_tts_zh": "现在我们来练习。请跟我重复学过的内容。",
            "texto_tts_es": practice_es,
        })

    # ── Ejercicio ──
    if ejercicio and ejercicio.get("frase"):
        # solucion: frase completa con los huecos rellenos (para TTS después de la pausa)
        solucion = ejercicio.get("solucion", "")
        slides.append({
            "tipo": "ejercicio",
            "titulo_zh": "小练习",
            "frase_es": ejercicio["frase"],        # con huecos: visual
            "traduccion_zh": ejercicio.get("traduccion", ""),
            "analisis": ejercicio.get("analisis", []),
            "tts": "es",
            "texto_tts_zh": "现在，我们来做一个练习。请思考一下。",
            "texto_tts_es": make_es_tts(solucion) if solucion else make_es_tts(ejercicio.get("frase", "")),
        })

    # ── Resumen bilingüe ──
    resumen_puntos = []
    for pt in puntos[:4]:
        clean = extract_chinese_only(pt)
        if clean and len(clean) > 2:
            resumen_puntos.append(clean)

    tts_resumen = puntos_to_zh_tts(resumen_puntos)
    if not tts_resumen:
        tts_resumen = "今天学完了。明天继续。"
    tts_resumen = f"好，我们来总结一下今天学的内容。{tts_resumen}。如果你掌握了这些内容，恭喜你，你又进步了。"

    # Build Spanish TTS for resumen from original puntos
    es_summary_parts = []
    for pt in puntos[:4]:
        es_part = extract_spanish_only(pt)
        if es_part:
            es_summary_parts.append(es_part)
    es_tts_resumen = ", ".join(es_summary_parts) if es_summary_parts else "Repasemos lo aprendido."
    es_tts_resumen = es_tts_resumen if es_tts_resumen else "Repasemos."

    slides.append({
        "tipo": "resumen",
        "titulo_zh": "总结",
        "titulo_es": "Resumen",
        "puntos": resumen_puntos,
        "tts": "zh",
        "texto_tts_zh": tts_resumen,
        "texto_tts_es": es_tts_resumen,
    })

    # ── Outro ──
    slides.append({
        "tipo": "outro",
        "texto_zh": "喜欢这个视频吗？点赞和订阅是对我们最大的支持。Hola西班牙语陪你每天进步一点点。明天见！",
        "tts": "zh",
        "texto_tts_zh": "喜欢这个视频吗？点赞和订阅是对我们最大的支持。陪你每天进步一点点。明天见！",
        "texto_tts_es": "",
    })

    # ═══════════════════════════════════════════════
    # 🛡️ VALIDACIÓN AUTOMÁTICA DE REGLAS A1
    # ═══════════════════════════════════════════════
    script = {
        "nivel": nivel,
        "modulo": modulo["slug"],
        "tema": tema,
        "duracion_segmento": 3.0,
        "slides": slides,
    }
    errors = _validate_a1_script(script)
    if errors:
        print(f"⚠️  [{tema}] Reglas A1 violadas:")
        for e in errors:
            print(f"    • {e}")
    return script


# ── File ops ──

def write_script(script: dict, modulo_info: dict = None, leccion_info: dict = None, output_dir: str | Path = None) -> Path:
    # 🛡️ Validar reglas A1 antes de escribir
    warnings = _validate_a1_script(script)
    if warnings:
        print(f"⚠️  [{script.get('tema','?')}] Reglas A1:")
        for w in warnings:
            print(f"    • {w}")

    if output_dir is None:
        base = PROJECT_ROOT / "scripts"
        output_dir = base / script["nivel"] / modulo_info["slug"] if modulo_info else base / script["nivel"]
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    slug = leccion_info["slug"] if leccion_info else script.get("tema", "untitled").replace(" ", "-").lower()
    path = output_dir / f"{slug}.yaml"
    with open(path, "w", encoding="utf-8") as f:
        yaml.dump(script, f, allow_unicode=True, sort_keys=False, width=80)
    return path


def build_all(output_dir: str | Path = None, force: bool = False) -> list[Path]:
    curriculo = load_curriculo()
    nivel = curriculo["nivel"]
    generated = []
    for modulo in curriculo["modulos"]:
        for leccion in modulo["lecciones"]:
            slug = leccion["slug"]
            out_dir = Path(output_dir) if output_dir else PROJECT_ROOT / "scripts" / nivel / modulo["slug"]
            out_path = out_dir / f"{slug}.yaml"
            if out_path.exists() and not force:
                print(f"  ⏩ {slug}.yaml")
                continue
            script = generate_script(leccion, modulo, nivel)
            written = write_script(script, modulo, leccion, out_dir)
            generated.append(written)
            print(f"  ✓ {written.name}")
    return generated


def build_one(modulo_slug: str, leccion_slug: str) -> Path:
    curriculo = load_curriculo()
    nivel = curriculo["nivel"]
    for modulo in curriculo["modulos"]:
        if modulo["slug"] != modulo_slug:
            continue
        for leccion in modulo["lecciones"]:
            if leccion["slug"] != leccion_slug:
                continue
            script = generate_script(leccion, modulo, nivel)
            return write_script(script, modulo, leccion)
    raise ValueError(f"Lesson not found: {modulo_slug}/{leccion_slug}")


# ── Vocabulary extraction ──

def _extraer_palabras(frase: str, analisis: list[str]) -> list[dict]:
    """
    Extrae palabras individuales de una frase española, emparejándolas
    con sus traducciones del análisis si existen.

    Ejemplo:
        frase = "Buenos días, ¿cómo está usted?"
        analisis = ["Buenos días = 早上好", "usted = 您（正式）"]
        → [{"es": "Buenos", "zh": "好的"}, {"es": "días", "zh": "天"}, ...]
    """
    # Tokenizar la frase: extraer palabras (sin puntuación)
    tokens = re.findall(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ]+', frase)
    if len(tokens) < 2:
        return []

    # Construir diccionario de traducciones desde análisis
    trad_map = {}
    for entry in analisis:
        for part in entry.split("，"):
            part = part.strip()
            if "=" in part:
                es_part, zh_part = part.split("=", 1)
                es_word = es_part.strip().lower()
                zh_word = zh_part.strip()
                trad_map[es_word] = zh_word
            elif "＝" in part:
                es_part, zh_part = part.split("＝", 1)
                es_word = es_part.strip().lower()
                zh_word = zh_part.strip()
                trad_map[es_word] = zh_word

    # Traducciones por defecto para palabras comunes A1
    DEFAULTS = {
        "buenos": "好的", "días": "天/日子", "buenas": "好的",
        "tardes": "下午", "noches": "晚上", "hola": "你好",
        "qué": "什么", "tal": "如何", "cómo": "如何/怎么",
        "está": "是（状态）", "usted": "您", "tú": "你",
        "muy": "非常", "bien": "好的", "adiós": "再见",
        "hasta": "直到", "mañana": "明天", "luego": "之后",
        "gracias": "谢谢", "por": "为了", "favor": "请",
        "sí": "是", "no": "不", "yo": "我", "él": "他",
        "ella": "她", "nosotros": "我们", "ellos": "他们",
        "soy": "我是", "eres": "你是", "es": "是",
        "un": "一个", "una": "一个", "el": "（阳性定冠词）",
        "la": "（阴性定冠词）", "los": "（阳性复数定冠词）",
        "las": "（阴性复数定冠词）", "de": "的", "en": "在",
        "con": "和/用", "y": "和", "o": "或", "se": "（代词）",
        "me": "我（宾格）", "te": "你（宾格）", "le": "他/她（宾格）",
        "hay": "有", "son": "是（复数）", "tengo": "我有",
    }

    # Collect words missing translations
    missing = []
    for token in tokens:
        tl = token.lower()
        if tl not in trad_map and tl not in DEFAULTS:
            missing.append(token)

    # Batch-translate missing words via LLM
    llm_translations = {}
    if missing:
        llm_translations = _llm_translate_words(missing, frase)

    palabras = []
    for token in tokens:
        tl = token.lower()
        zh = trad_map.get(tl)
        if not zh:
            zh = DEFAULTS.get(tl, "")
        if not zh:
            zh = llm_translations.get(tl, "")
        palabras.append({"es": token, "zh": zh})

    return palabras


# ═══════════════════════════════════════════════
# 🛡️ REGLAS A1 — Validación automática
# ═══════════════════════════════════════════════

# Frases prohibidas en TTS español (instrucciones que un A1 no entiende)
_PROHIBITED_ES_PHRASES = [
    "Escucha con atencion", "Escucha con atención",
    "Otra vez", "Repite conmigo", "repite conmigo",
    "Muy bien", "muy bien",
    "Ahora practiquemos", "ahora practiquemos",
    "Hagamos un repaso", "hagamos un repaso",
    "Si dominas esto", "si dominas esto",
    "felicidades", "Felicidades",
    "vas muy bien", "lo has hecho genial",
    "Te ha gustado", "te ha gustado",
    "Dale like", "dale like",
    "suscribete", "suscríbete",
    "Nos vemos", "nos vemos",
    "Prepara tu cuaderno", "prepara tu cuaderno",
    "Hoy vamos a aprender", "hoy vamos a aprender",
    "Diversa te acompana", "Diversa te acompaña",
]

# Frases prohibidas en TTS chino — indican repetición de contenido chino
# La repetición solo debe ocurrir en el audio ESPAÑOL (lengua objetivo)
_PROHIBITED_ZH_REPETITION = [
    "我会重复一遍",   # "I will repeat it" — shouldn't repeat Chinese
    "再来一次",       # "Once again" — shouldn't repeat Chinese  
    "再听一遍",       # "Listen once more" — shouldn't repeat Chinese
    "再说一遍",       # "Say it again" — shouldn't repeat Chinese
]

# Placeholders prohibidos en TTS chino (deben usar el tema real)
_PROHIBITED_ZH_PLACEHOLDERS = [
    "新课题",   # placeholder genérico — debe ser el nombre real del tema
]

# Caracteres prohibidos en cualquier TTS (nunca deben llegar al audio)
_PROHIBITED_TTS_CHARS = re.compile(r'[\[\]\{\}]')  # corchetes y llaves

# Caracteres prohibidos en TTS español (se pronuncian literalmente)
_PROHIBITED_ES_CHARS = re.compile(r'[/\\*#_]')
_PROHIBITED_ES_DIGITS = re.compile(r'\b\d+\b')

# Caracteres prohibidos en TTS chino (latinos — voz china no sabe pronunciarlos)
_PROHIBITED_ZH_CHARS = re.compile(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ¿¡]')


def _validate_a1_script(script: dict) -> list[str]:
    """
    Valida y auto-corrige un script generado contra TODAS las reglas A1.
    Devuelve lista de warnings (errores que no pudieron auto-corregirse).
    
    Reglas:
      1. texto_tts_zh NUNCA debe tener español/latín
      2. texto_tts_es NUNCA debe tener chino
      3. texto_tts_es NUNCA debe tener / barra, backslash, asterisco, numeral, guion bajo ni números sueltos
      4. texto_tts_es NUNCA debe tener frases instruccionales en español
      5. Slides vocabulario: texto_tts_zh debe ser instrucción pura (sin frase española)
      6. NUNCA usar "Diversa" — siempre "Hola西班牙语"
      7. texto_tts_es nunca vacío si el slide tiene contenido español relevante
    """
    warnings = []

    for i, slide in enumerate(script.get("slides", [])):
        tipo = slide.get("tipo", "?")
        zh = slide.get("texto_tts_zh", "")
        es = slide.get("texto_tts_es", "")

        # ── Regla 1: No español en TTS chino ──
        spanish_in_zh = _PROHIBITED_ZH_CHARS.findall(zh)
        if spanish_in_zh:
            # Auto-fix: strip Spanish words from Chinese TTS
            cleaned_zh = _PROHIBITED_ZH_CHARS.sub('', zh)
            cleaned_zh = re.sub(r'[：:，,、。]\s*[：:，,、。]', '。', cleaned_zh)
            cleaned_zh = re.sub(r'\s+', '', cleaned_zh)
            cleaned_zh = cleaned_zh.strip(' ，,。.·、:：')
            if cleaned_zh and len(cleaned_zh) > 5:
                slide["texto_tts_zh"] = cleaned_zh
            else:
                # Fallback: instruction based on slide type
                if tipo == "vocabulario":
                    slide["texto_tts_zh"] = "现在我们来逐词学习刚才的句子。请仔细听每个单词的发音，然后跟我读。"
                elif tipo == "explicacion":
                    slide["texto_tts_zh"] = "请大家注意听，然后跟我重复。"
                else:
                    slide["texto_tts_zh"] = "请注意听，然后跟我读。"

        # ── Regla 2: No chino en TTS español ──
        if re.search(r'[\u4e00-\u9fff]', es):
            warnings.append(f"Slide {i} ({tipo}): texto_tts_es contiene caracteres chinos")

        # ── Regla 2b: No corchetes/llaves en ningún TTS (se pronuncian literal) ──
        if _PROHIBITED_TTS_CHARS.search(zh):
            slide["texto_tts_zh"] = _PROHIBITED_TTS_CHARS.sub('', zh)
        if _PROHIBITED_TTS_CHARS.search(es):
            slide["texto_tts_es"] = _PROHIBITED_TTS_CHARS.sub('', es)

        # ── Regla 3: No caracteres basura en TTS español ──
        if _PROHIBITED_ES_CHARS.search(es):
            cleaned_es = _PROHIBITED_ES_CHARS.sub(' ', es)
            cleaned_es = re.sub(r'\s+', ' ', cleaned_es).strip()
            cleaned_es = cleaned_es.strip(' ，,。.·、/-')
            slide["texto_tts_es"] = cleaned_es

        if _PROHIBITED_ES_DIGITS.search(es):
            cleaned_es = _PROHIBITED_ES_DIGITS.sub('', es)
            cleaned_es = re.sub(r'\s+', ' ', cleaned_es).strip()
            cleaned_es = cleaned_es.strip(' ，,。.·、/-')
            slide["texto_tts_es"] = cleaned_es

        # ── Regla 4: No frases instruccionales en español ──
        es_lower = es.lower()
        for phrase in _PROHIBITED_ES_PHRASES:
            if phrase.lower() in es_lower:
                # Check if it's actually part of the LESSON content or meta-instruction
                # If the phrase is the ONLY thing OR it's at the start/end surrounded by punctuation
                # it's likely a meta-instruction. If it's mid-sentence in a bigger phrase, it's content.
                if phrase.lower() == es_lower.strip(' 。.，,'):
                    warnings.append(f"Slide {i} ({tipo}): texto_tts_es ES SOLO '{phrase}' — instrucción disfrazada")
                elif es_lower.startswith(phrase.lower()):
                    warnings.append(f"Slide {i} ({tipo}): texto_tts_es EMPIEZA con '{phrase}' — posible instrucción")
                elif es_lower.endswith(phrase.lower()):
                    warnings.append(f"Slide {i} ({tipo}): texto_tts_es TERMINA con '{phrase}' — posible instrucción")

        # ── Regla 5: Vocabulario slides — Chinese TTS must be pure instruction ──
        if tipo == "vocabulario":
            if _PROHIBITED_ZH_CHARS.search(zh):
                slide["texto_tts_zh"] = "现在我们来逐词学习刚才的句子。请仔细听每个单词的发音，然后跟我读。"

        # ── Regla 5b: Chinese TTS nunca debe repetir contenido chino ──
        # La repetición solo ocurre en el audio español (lengua objetivo)
        for phrase in _PROHIBITED_ZH_REPETITION:
            if phrase in zh:
                warnings.append(f"Slide {i} ({tipo}): texto_tts_zh contiene '{phrase}' — la repetición debe ser en español, no en chino")

        # ── Regla 5c: Explicacion — TTS español DEBE incluir la palabra del punto ──
        if tipo == "explicacion":
            puntos = slide.get("puntos", [])
            if puntos and puntos[0]:
                es_from_pt = extract_spanish_only(puntos[0] or "")
                if es_from_pt and es_from_pt not in es:
                    warnings.append(f"Slide {i} ({tipo}): texto_tts_es NO incluye '{es_from_pt}' (palabra clave del punto)")

        # ── Regla 6: No "Diversa" en ningún lado ──
        for field in ["titulo_zh", "titulo_es", "texto_zh", "texto_tts_zh", "texto_tts_es"]:
            val = slide.get(field, "")
            if isinstance(val, str) and "Diversa" in val:
                slide[field] = val.replace("Diversa", "Hola西班牙语")

        # ── Regla 6b: Portada — no usar placeholders genéricos en TTS chino ──
        if tipo == "portada":
            for placeholder in _PROHIBITED_ZH_PLACEHOLDERS:
                if placeholder in zh:
                    warnings.append(f"Slide {i} (portada): texto_tts_zh contiene '{placeholder}' — debe usar el nombre real del tema en chino")

        # ── Regla 7: Contenido visual y audio DEBEN coincidir ──
        # La frase española en pantalla debe estar en el TTS español
        if tipo == "explicacion":
            frase_es = slide.get("frase_es", "")
            if frase_es and frase_es.lower() not in es.lower():
                warnings.append(f"Slide {i} ({tipo}): frase_es '{frase_es}' NO aparece en texto_tts_es — slide y audio deben coincidir")

        # ── Regla 8: Frases españolas deben tener su traducción china (de la PALABRA, no del ejemplo) ──
        if tipo == "explicacion" and slide.get("frase_es"):
            trad = slide.get("traduccion_zh", "")
            frase = slide.get("frase_es", "")
            if not trad or len(trad.strip()) < 2:
                warnings.append(f"Slide {i} ({tipo}): frase_es '{frase}' no tiene traduccion_zh")
            # La traducción no debe ser más del triple de larga que la frase (indicaría que es del ejemplo, no del punto)
            elif frase and len(trad) > len(frase) * 3:
                warnings.append(f"Slide {i} ({tipo}): traduccion_zh '{trad[:30]}...' parece traducción del ejemplo, no del punto '{frase}'")

        # ── Regla 9: Slide de práctica — solo repetir lo ENSEÑADO, no frases nuevas ──
        if tipo == "ejemplo" and slide.get("frase_es", "") in ("Repite estos saludos", "Repite lo aprendido"):
            analisis = slide.get("analisis", [])
            frases_ensenadas = [s.get("frase_es", "") for s in script["slides"] if s.get("tipo") == "explicacion"]
            for frase in analisis:
                # La frase de práctica debe ser IDÉNTICA a algo enseñado (no un superconjunto)
                ensenada = any(f.strip().lower() == frase.strip().lower() for f in frases_ensenadas if f)
                if not ensenada and len(frase) > 2:
                    warnings.append(f"Slide {i} (práctica): '{frase[:50]}' NO fue enseñada — solo repetir lo ya visto")

        # ── Regla 10: Ejercicio — solo evaluar contenido ENSEÑADO ──
        if tipo == "ejercicio":
            solucion = slide.get("texto_tts_es", "")
            if solucion:
                import re as _re2
                palabras_sol = [w for w in _re2.findall(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ]{3,}', solucion) if w.lower() not in ('completa','complete')]
                ensenadas = set()
                for es in script["slides"]:
                    if es.get("tipo") == "explicacion":
                        for w in _re2.findall(r'[a-zA-ZáéíóúüñÁÉÍÓÚÜ]{3,}', es.get("frase_es", "")):
                            ensenadas.add(w.lower())
                for w in palabras_sol:
                    if w.lower() not in ensenadas:
                        warnings.append(f"Slide {i} (ejercicio): '{w}' en la solución NO fue enseñada — solo evaluar lo visto")

    return warnings


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", "-f", action="store_true")
    parser.add_argument("--one", nargs=2, metavar=("MODULO", "LECCION"))
    args = parser.parse_args()
    if args.one:
        path = build_one(args.one[0], args.one[1])
        print(f"\n✅ {path}")
    else:
        print("🎬 Regenerando scripts con TTS limpio...")
        paths = build_all(force=args.force)
        print(f"\n✅ {len(paths)} scripts generados")
