# DELE Video Bot — Contexto Técnico

> Documento vivo. Si algo cambia, actualizarlo.
> Última actualización: 2026-06-18

---

## 🧠 Reglas del nivel A1 (NO ROMPER — validación automática en _validate_a1_script)

1. **Instrucciones SIEMPRE en chino.** El alumno A1 no entiende español.
   - ❌ `"Escucha con atención"`, `"Otra vez, repite conmigo"`, `"Muy bien"`
   - ✅ `请仔细听`, `跟我读`, `很好，我们继续`

2. **Contenido-objetivo en español.** Solo lo que se está enseñando.
   - ✅ `"Buenos días. ¿Cómo está usted?"`

3. **Orden de audio por slide:** Chino PRIMERO (instrucción) → 1.5s silencio → Español DESPUÉS (contenido)

4. **Dual TTS en TODOS los slides.** No se elige un idioma; se generan ambos y se concatenan.

5. **Sin meta-texto en español TTS.** `texto_tts_es` solo contiene frases/vocabulario, nunca instrucciones.

6. **Sin español en TTS chino.** `texto_tts_zh` no debe contener palabras en español (la voz china no sabe pronunciarlas).
   - Auto-corrección: `_validate_a1_script()` limpia automáticamente.

7. **Sin caracteres basura en TTS.** `/`, `\\`, `*`, `#`, `_`, números sueltos se eliminan del TTS español.
   - Auto-corrección: `make_es_tts()` y `_validate_a1_script()` limpian automáticamente.

8. **Nunca usar "Diversa".** Siempre `"Hola西班牙语"`.
   - Auto-corrección: `_validate_a1_script()` reemplaza automáticamente.

9. **Slide y audio deben coincidir.** La frase española visible (`frase_es`) debe aparecer en `texto_tts_es`.
   - Detectado por: Regla 5c y Regla 7

10. **Cada frase española requiere traducción china.** `traduccion_zh` no puede estar vacío.
    - Si no hay ejemplo relevante, se extrae del punto (después del guion: "Hola — 你好")
    - Detectado por: Regla 8

11. **Contenido con género balanceado.** Nombres y referencias deben alternar masculino/femenino.
    - `[nombre]` alterna Pedro (M) ↔ María (F)
    - `[nombre1]` = Ana (F), `[nombre2]` = Juan (M)
    - `[profesión]` = "profesora" (F)

      6b. Portada: texto_tts_zh debe incluir el tema real EN CHINO (extraído de explicacion),
          nunca un placeholder genérico como "新课题" ni el primer punto individual
          (ej: "早上好" no es el tema — "先来看正式问候" sí lo es)

### Validación automática

Cada vez que se genera un script (vía `generate_script()` o `write_script()`), se ejecuta
`_validate_a1_script()` que:
- Detecta y **auto-corrige**: español en TTS chino, chars basura, números sueltos, "Diversa"
- **Advierte** (warning): frases instruccionales en TTS español
- Imprime los warnings en consola para revisión

---

## 🏗️ Arquitectura

```
contenido_a1.py       →  currículo (datos estructurados)
        │
        ▼
content_factory.py    →  genera scripts YAML desde currículo
        │                 aplica reglas A1 automáticamente
        ▼
scripts/A1/*/*.yaml   →  scripts por lección (108 lecciones)
        │
        ▼
┌─ pipeline.py ────────┐
│  content_parser.py   │  parsea YAML → objetos Slide
│  slide_renderer.py   │  renderiza PNGs 1080×1920
│  tts_engine.py       │  genera audio ZH + ES vía edge-tts
│  video_composer.py   │  compone video con ffmpeg
└──────────────────────┘
        │
        ▼
output/diversa/*.mp4   →  video final
```

### Voces TTS
- **Chino:** `zh-CN-XiaoxiaoNeural` (mujer, Microsoft)
- **Español:** `es-MX-DaliaNeural` (mujer, México)
- Velocidad: `-15%` (más lento para aprendices)

---

## 📂 Directorios

```
dele-video-bot/
├── contenido_a1.py              # Currículo estructurado
├── content_factory.py           # Genera YAMLs desde currículo
├── pipeline.py                  # Pipeline CLI
├── tts_engine.py                # Motor TTS bilingüe
├── video_composer.py            # Composición ffmpeg
├── slide_renderer.py            # Renderizado de slides PNG
├── content_parser.py            # Parser YAML
├── dashboard/
│   ├── main.py                  # FastAPI server
│   ├── templates/index.html     # Frontend
│   └── static/app.js            # Lógica frontend
├── scripts/A1/                  # YAMLs generados (108 lecciones)
├── output/diversa/              # Videos finales
└── .work/                       # Temp files (slides, audio)
```

---

## 🔌 Endpoints del Dashboard

| Endpoint | Método | Descripción |
|---|---|---|
| `/api/curriculo` | GET | Árbol completo del currículo |
| `/api/leccion/{mod}/{lec}` | GET | Slides de una lección |
| `/api/leccion/{mod}/{lec}/save` | POST | Guardar slides editados |
| `/api/leccion/{mod}/{lec}/generate` | POST | Generar YAML desde currículo |
| `/api/leccion/{mod}/{lec}/full-pipeline` | POST | 🚀 One-click: currículo → YAML → video |
| `/api/generate` | POST | Generar video desde slides en memoria |
| `/api/video/{filename}` | GET | Servir archivo de video |

---

## 🎨 Slide Types

| Tipo | Uso | TTS |
|---|---|---|
| `portada` | Título + nivel | ZH + ES |
| `explicacion` | Punto gramatical + ejemplo | ZH (instrucción) + ES (frase) |
| `ejemplo` | Frase de ejemplo / refrán | ZH (instrucción) + ES (frase) |
| `ejercicio` | Ejercicio de completar | ZH (instrucción) + ES (ejercicio) |
| `resumen` | Repaso de la lección | ZH + ES (vocabulario) |
| `outro` | Despedida y CTA | Solo ZH |
| `vocabulario` | 🆕 Desglose palabra×palabra | ZH (instrucción) + ES (word-by-word) |

---

## 🎬 Pipeline de generación de video

```
1. Parsear YAML → lista de Slides
2. Renderizar cada slide → PNG 1080×1920
3. Para cada slide:
   a. Generar TTS chino (edge-tts: Xiaoxiao)
   b. Generar TTS español (edge-tts: Dalia)
   c. Concatenar: ZH.mp3 + 1.5s silencio + ES.mp3 → slide_XXX.mp3
4. Componer video: PNGs + audios → MP4
```

---

## 🆕 Vocabulario palabra×palabra (✅ IMPLEMENTADO 2026-06-18)

### Flujo
```
Slide N:   explicacion → "Buenos días, ¿cómo está usted?"
Slide N+1: vocabulario → [Buenos] [días] [cómo] [está] [usted]
                         cada palabra con pronunciación individual
                         TTS word-by-word con gaps de 0.45s
```

### Implementación
1. `content_factory.py`: `_extraer_palabras()` extrae tokens de frases españolas
   - Empareja palabras con traducciones del análisis del currículo
   - Tiene diccionario de defaults para palabras A1 comunes
   - Auto-inserta slide `vocabulario` después de cada `explicacion` con frase
2. `tts_engine.py`: `generate_word_by_word()` genera TTS individual por palabra
   - Concatena con gaps de 0.45s entre palabras
   - Devuelve timeline con timestamps precisos
3. `slide_renderer.py`: `render_vocabulario()` — tarjeta con frase original +
   lista de palabras (español grande, traducción china a la derecha)
4. Dashboard/pipeline detecta slides tipo `vocabulario` y usa word-by-word TTS

### Ejemplo generado (001-saludos-formales)
- 11 slides originales → 14 slides (3 vocabulario insertados)
- Video: 2:27 min, 2.4 MB
- Slides de vocabulario para: "Buenos días...", "Hola! ¿Qué tal?...", "Adiós..."

---

## ⚠️ Notas importantes

- No usar `texto_tts_es` para instrucciones — solo contenido
- El orden ZH→ES es crítico para A1
- `content_factory.py` es la fuente de verdad para el contenido generado
- Los YAMLs en `scripts/` se sobrescriben al regenerar
- edge-tts requiere ffmpeg instalado
- Las voces de edge-tts son gratuitas pero requieren internet
