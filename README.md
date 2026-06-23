# Hola西班牙语 · Verbos

Generador de videos educativos para Xiaohongshu/TikTok enfocado en **conjugación de verbos españoles por frecuencia de uso**.

## Concepto

Videos cortos (30-60s) que presentan un verbo español con:
1. **Portada** — verbo del día
2. **Tabla de conjugación** — presente de indicativo, 6 personas
3. **Ejemplos** — 3 frases con traducción al chino
4. **Outro** — CTA + siguiente verbo

## Verbos (por frecuencia)

Los 30 verbos más usados del español, ordenados por frecuencia (CREA):
ser, estar, tener, hacer, ir, poder, decir, ver, dar, saber, querer, hablar, llegar, pasar, deber, poner, creer, parecer, llevar, dejar, seguir, encontrar, llamar, venir, pensar, salir, volver, tomar, conocer, vivir.

Ver `verbos_frecuentes.yaml` para la lista completa con ejemplos y traducciones.

## Estructura

```
xhs-verbos-bot/
├── scripts/verbos/       # YAML: un verbo por archivo
│   ├── 001-ser.yaml
│   ├── 002-estar.yaml
│   └── ...
├── src/
│   ├── slide_renderer.py  # render_conjugacion() — tabla visual
│   ├── content_parser.py  # parsea YAML → VideoScript
│   ├── tts_engine.py      # TTS bilingüe (edge-tts)
│   ├── video_composer.py  # ffmpeg composición
│   └── pipeline.py        # orquestador
├── dashboard/             # FastAPI + web UI
├── branding.yaml          # 动词西班牙语
├── verbos_frecuentes.yaml # lista maestra de verbos
└── output/verbos/         # videos generados
```

## Uso

```bash
cd /root/xhs-verbos-bot

# Generar un video
.venv/bin/python -c "
import asyncio, sys
sys.path.insert(0,'.')
from src.pipeline import generate_video
asyncio.run(generate_video('scripts/verbos/001-ser.yaml', 'output/verbos'))
"

# Dashboard
cd dashboard && ../.venv/bin/python main.py
# → http://localhost:8080
```

## Voces TTS

| Idioma | Voz |
|--------|-----|
| Chino (instrucciones) | zh-CN-XiaoxiaoNeural |
| Español (contenido) | es-MX-DaliaNeural |

## Branding

- Canal: 动词西班牙语
- Eslogan: "Cada día un verbo, cada verbo un mundo"
- Paleta: naranja vibrante + azul profundo + dorado
