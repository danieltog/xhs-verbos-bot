# 🎬 DELE Video Bot

Generador de videos verticales (9:16) para Xiaohongshu/小红书 con contenido DELE para estudiantes chinos de español.

TTS bilingüe (chino + español) automático. Dashboard visual para crear y previsualizar contenido.

## 🚀 Quick Start

```bash
# Arrancar el dashboard
cd dashboard
python3 main.py
# → http://localhost:8080

# O desde línea de comandos (sin dashboard):
cd ..
python3 -m src.pipeline scripts/ejemplo-b1-pretérito-indefinido.yaml
```

## 📁 Estructura

```
├── dashboard/             ← Interfaz web (FastAPI)
│   ├── main.py            ← Backend API
│   ├── templates/         ← HTML dashboard
│   └── static/            ← JS frontend
├── scripts/               ← Contenido DELE en YAML
├── src/
│   ├── slide_renderer.py  ← Genera slides 1080×1920
│   ├── tts_engine.py      ← TTS edge-tts (Xiaoxiao / Elvira)
│   ├── video_composer.py  ← Compone video con ffmpeg
│   ├── content_parser.py  ← Lee y valida scripts YAML
│   └── pipeline.py        ← Orquestador completo
└── output/                ← Videos generados
```

## 🎯 Dashboard Features

- **Añadir/duplicar/reordenar slides** con drag & drop
- **7 tipos de slide**: Portada, Explicación, Ejemplo, Comparación, Ejercicio, Resumen, Outro
- **Vista previa en vivo** del slide en formato teléfono
- **TTS bilingüe**: seleccionar idioma por slide, previsualizar audio
- **Auto-llenado TTS** desde el contenido del slide
- **Generación completa** de video con barra de progreso
- **Descarga directa** del .mp4

## 📝 Cómo crear contenido

Cada video se compone de slides. Cada slide tiene:
- Un **tipo** (portada, explicación, ejemplo, etc.)
- **Contenido** en chino y/o español
- **Idioma TTS** (chino o español para el audio)

## 🔧 Requisitos

- Python 3.10+
- Dependencias: `pip install -r requirements-core.txt`
- ffmpeg (viene incluido con imageio_ffmpeg)

## 📱 Formato de salida

- Resolución: 1080×1920 (9:16 vertical)
- Video: H.264, 24fps
- Audio: AAC, 128kbps
- Ideal para: Xiaohongshu, Douyin, TikTok, Instagram Reels
