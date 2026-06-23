// ── 动词西班牙语 · Verbos Dashboard ──

let currentVerbo = null;
let currentData = null;
let currentSlideIdx = 0;
let allVerbos = [];
let currentView = 'slide';

// ═══════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════

async function init() {
  const res = await fetch('/api/verbos');
  allVerbos = await res.json();
  renderVerboList();
}

function renderVerboList() {
  const list = document.getElementById('verboList');
  let scriptCount = allVerbos.filter(v => v.has_script).length;
  let videoCount = allVerbos.filter(v => v.has_video).length;
  document.getElementById('sidebarStats').textContent = `${videoCount}/${allVerbos.length} videos`;

  list.innerHTML = allVerbos.map(v => `
    <div class="verbo-item ${currentVerbo === v.verbo ? 'active' : ''}" onclick="selectVerbo('${v.verbo}')">
      <span class="freq">#${v.frecuencia}</span>
      <span class="name">
        ${v.verbo.toUpperCase()}
        <span class="zh">${v.traduccion}</span>
      </span>
      <span class="type-badge">${v.tipo}</span>
      <span class="status-dot ${v.has_video ? 'video' : v.has_script ? 'script' : 'none'}"
            title="${v.has_video ? 'Video' : v.has_script ? 'Script' : 'Sin contenido'}"></span>
    </div>
  `).join('');
}

// ═══════════════════════════════════════════
// VERBO SELECTION
// ═══════════════════════════════════════════

async function selectVerbo(verbo) {
  currentVerbo = verbo;
  currentSlideIdx = 0;

  // Update sidebar
  renderVerboList();

  document.getElementById('statusText').textContent = `Cargando ${verbo}...`;
  const res = await fetch(`/api/verbo/${verbo}`);
  currentData = await res.json();

  // Show video badge if has video
  const badge = document.getElementById('videoBadge');
  badge.style.display = currentData.has_video ? 'inline' : 'none';

  document.getElementById('statusText').textContent =
    currentData.has_script ? `Editando: ${verbo.toUpperCase()}` : `Nuevo: ${verbo.toUpperCase()} (sin script)`;

  renderEditor();

  // Auto-load correct view
  if (currentView === 'video' && currentData.has_video) {
    loadVideo();
  }
}

// ═══════════════════════════════════════════
// EDITOR RENDERING
// ═══════════════════════════════════════════

function renderEditor() {
  const d = currentData;
  const slides = d.slides || [];
  const slide = slides.length > 0 ? slides[currentSlideIdx] : null;

  // Find conjugation slide
  const conjSlide = slides.find(s => s.tipo === 'conjugacion');
  const ejemplos = slides.filter(s => s.tipo === 'ejemplo');

  let html = '';

  // ── Header ──
  html += `<h3>${d.verbo.toUpperCase()}</h3>`;
  html += `<div class="meta">${d.traduccion_zh || ''} · Frecuencia #${d.frecuencia || '?'} · ${d.nivel || 'A1'}</div>`;

  // ── Slide tabs ──
  if (slides.length > 0) {
    html += '<div class="slide-tabs">';
    slides.forEach((s, i) => {
      const labels = {portada: '📔 Portada', conjugacion: '📊 Conjugación', ejemplo: '💬 Ejemplo', outro: '🏁 Outro'};
      const label = labels[s.tipo] || s.tipo;
      html += `<span class="slide-tab ${i === currentSlideIdx ? 'active' : ''}" onclick="switchSlide(${i})">${label}</span>`;
    });
    html += '</div>';
  }

  // ── Conjugation table ──
  const conj = conjSlide ? (conjSlide.conjugacion || []) : [];
  html += '<div class="section">';
  html += '<h4>📊 Conjugación · Presente</h4>';
  html += '<table class="conj-table">';
  html += '<tr><th>Persona</th><th>Pronombre</th><th>Forma</th></tr>';
  const personas = ['yo', 'tú', 'él/ella/usted', 'nosotros/as', 'vosotros/as', 'ellos/ellas/ustedes'];
  const pronombres = ['我', '你', '他/她/您', '我们', '你们', '他们/她们/您们'];
  personas.forEach((p, i) => {
    const entry = conj[i] || {persona: p, pronombre: pronombres[i] || '', forma: ''};
    html += `<tr>
      <td><input value="${esc(entry.persona || p)}" data-conj="${i}" data-field="persona" onchange="updateConj()"></td>
      <td><input value="${esc(entry.pronombre || '')}" data-conj="${i}" data-field="pronombre" onchange="updateConj()"></td>
      <td><input class="forma" value="${esc(entry.forma || '')}" data-conj="${i}" data-field="forma" onchange="updateConj()"></td>
    </tr>`;
  });
  html += '</table></div>';

  // ── Examples ──
  html += '<div class="section">';
  html += '<h4>💬 Ejemplos</h4>';
  for (let i = 0; i < 3; i++) {
    const ej = ejemplos[i] || {frase_es: '', traduccion_zh: ''};
    html += `<div class="example-row">
      <span class="num">${i+1}</span>
      <input class="es" value="${esc(ej.frase_es || '')}" placeholder="Frase en español" data-ej="${i}" data-field="es" onchange="updateEjemplo()">
      <input class="zh" value="${esc(ej.traduccion_zh || '')}" placeholder="Traducción al chino" data-ej="${i}" data-field="zh" onchange="updateEjemplo()">
    </div>`;
  }
  html += '</div>';

  // ── Portada info ──
  const portada = slides.find(s => s.tipo === 'portada') || {};
  html += '<div class="section">';
  html += '<h4>📔 Portada</h4>';
  html += `<div class="form-row"><label>Título ES</label><input value="${esc(portada.titulo_es || `Verbo ${d.verbo.toUpperCase()}`)}" onchange="updateField('titulo_es', this.value)"></div>`;
  html += `<div class="form-row"><label>Título ZH</label><input value="${esc(portada.titulo_zh || `动词 ${d.verbo.toUpperCase()}`)}" onchange="updateField('titulo_zh', this.value)"></div>`;
  html += '</div>';

  // ── Outro ──
  const outro = slides.find(s => s.tipo === 'outro') || {};
  html += '<div class="section">';
  html += '<h4>🏁 Outro</h4>';
  html += `<div class="form-row"><label>ZH</label><input value="${esc(outro.titulo_zh || `今天学了 ${d.verbo.toUpperCase()}！`)}" onchange="updateField('outro_zh', this.value)"></div>`;
  html += `<div class="form-row"><label>ES</label><input value="${esc(outro.titulo_es || `¡Hoy aprendiste ${d.verbo.toUpperCase()}!`)}" onchange="updateField('outro_es', this.value)"></div>`;
  html += '</div>';

  document.getElementById('editor').innerHTML = html;

  // Load first slide preview
  if (slides.length > 0) {
    loadPreview(currentSlideIdx);
  }
}

function esc(s) { return (s || '').replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;'); }

// ═══════════════════════════════════════════
// SLIDE NAVIGATION
// ═══════════════════════════════════════════

function switchSlide(idx) {
  currentSlideIdx = idx;
  renderEditor();
}

// ═══════════════════════════════════════════
// PREVIEW
// ═══════════════════════════════════════════

async function loadPreview(idx) {
  if (!currentVerbo) return;
  try {
    const res = await fetch(`/api/verbo/${currentVerbo}/preview/${idx}`, {method: 'POST'});
    if (!res.ok) {
      document.getElementById('phoneFrame').innerHTML = '<div class="placeholder">Error al cargar</div>';
      return;
    }
    const data = await res.json();
    document.getElementById('phoneFrame').innerHTML = `<img src="data:image/png;base64,${data.base64}" alt="slide">`;
    document.getElementById('slideNum').textContent = idx + 1;
    document.getElementById('slideType').textContent = data.tipo;
  } catch (e) {
    document.getElementById('phoneFrame').innerHTML = '<div class="placeholder">Error</div>';
  }
}

// ═══════════════════════════════════════════
// VIEW TOGGLE
// ═══════════════════════════════════════════

function setView(view) {
  currentView = view;
  document.getElementById('viewSlideBtn').className = view === 'slide' ? 'active' : '';
  document.getElementById('viewVideoBtn').className = view === 'video' ? 'active' : '';
  document.getElementById('previewMeta').style.display = view === 'slide' ? 'flex' : 'none';
  document.getElementById('videoMeta').style.display = view === 'video' ? 'flex' : 'none';

  if (view === 'video') {
    loadVideo();
  } else if (currentData && currentData.slides && currentData.slides.length > 0) {
    loadPreview(currentSlideIdx);
  }
}

function loadVideo() {
  if (!currentData || !currentData.has_video || !currentData.video_url) {
    document.getElementById('phoneFrame').innerHTML =
      '<div class="placeholder">No hay video generado<br><small style="color:var(--text2)">Generá el video primero</small></div>';
    document.getElementById('videoSize').textContent = '-';
    document.getElementById('videoDur').textContent = '-';
    document.getElementById('videoDownload').href = '#';
    return;
  }

  const url = currentData.video_url;
  document.getElementById('phoneFrame').innerHTML = `
    <video controls autoplay loop playsinline style="width:100%;height:100%;object-fit:cover;background:#000">
      <source src="${url}" type="video/mp4">
    </video>`;
  document.getElementById('videoDownload').href = url;

  // Try to get video metadata
  const video = document.querySelector('#phoneFrame video');
  if (video) {
    video.onloadedmetadata = () => {
      const mins = Math.floor(video.duration / 60);
      const secs = Math.round(video.duration % 60);
      document.getElementById('videoDur').textContent = `${mins}:${String(secs).padStart(2, '0')}`;
    };
    // Estimate size from API response
    fetch(url, {method: 'HEAD'}).then(r => {
      const size = parseInt(r.headers.get('content-length') || 0);
      document.getElementById('videoSize').textContent = size > 1024*1024
        ? `${(size/1024/1024).toFixed(1)} MB`
        : `${Math.round(size/1024)} KB`;
    }).catch(() => {});
  }
}

// ═══════════════════════════════════════════
// FIELD UPDATES
// ═══════════════════════════════════════════

function updateField(field, value) {
  if (!currentData) return;
  const slides = currentData.slides || [];
  const portada = slides.find(s => s.tipo === 'portada');
  const outro = slides.find(s => s.tipo === 'outro');

  if (field === 'titulo_es' && portada) portada.titulo_es = value;
  if (field === 'titulo_zh' && portada) portada.titulo_zh = value;
  if (field === 'outro_zh' && outro) outro.titulo_zh = value;
  if (field === 'outro_es' && outro) outro.titulo_es = value;
}

function updateConj() {
  if (!currentData) return;
  const slides = currentData.slides || [];
  const conjSlide = slides.find(s => s.tipo === 'conjugacion');
  if (!conjSlide) return;

  conjSlide.conjugacion = conjSlide.conjugacion || [];
  document.querySelectorAll('[data-conj]').forEach(el => {
    const i = parseInt(el.dataset.conj);
    const field = el.dataset.field;
    if (!conjSlide.conjugacion[i]) {
      conjSlide.conjugacion[i] = {persona: '', pronombre: '', forma: ''};
    }
    conjSlide.conjugacion[i][field] = el.value;
  });
}

function updateEjemplo() {
  if (!currentData) return;
  const slides = currentData.slides || [];
  const ejemplos = slides.filter(s => s.tipo === 'ejemplo');

  document.querySelectorAll('[data-ej]').forEach(el => {
    const i = parseInt(el.dataset.ej);
    const field = el.dataset.field;
    if (!ejemplos[i]) {
      // Need to create the ejemplo slide
      ejemplos[i] = {tipo: 'ejemplo', tts: 'zh', frase_es: '', traduccion_zh: '', titulo_zh: `例句 ${i+1}`};
    }
    if (field === 'es') ejemplos[i].frase_es = el.value;
    if (field === 'zh') ejemplos[i].traduccion_zh = el.value;
  });
}

// ═══════════════════════════════════════════
// SAVE
// ═══════════════════════════════════════════

async function saveVerbo() {
  if (!currentVerbo || !currentData) return toast('Nada que guardar');

  document.getElementById('statusText').textContent = 'Guardando...';

  // Build slides array from current data
  const slides = [];
  const d = currentData;

  // Get portada fields
  const portadaTitleEs = document.querySelector('[data-field]') ? null : null; // We'll use currentData

  // Portada
  slides.push({
    tipo: 'portada', tts: 'zh',
    titulo_es: currentData.slides?.find(s => s.tipo === 'portada')?.titulo_es || `Verbo ${currentVerbo.toUpperCase()}`,
    titulo_zh: currentData.slides?.find(s => s.tipo === 'portada')?.titulo_zh || `动词 ${currentVerbo.toUpperCase()}`,
    capitulo: currentData.frecuencia || 1,
  });

  // Conjugacion
  const conjSlide = currentData.slides?.find(s => s.tipo === 'conjugacion') || {};
  slides.push({
    tipo: 'conjugacion', tts: 'zh',
    titulo_zh: `${currentVerbo.toUpperCase()} · 现在时变位`,
    verbo: currentVerbo,
    tiempo: 'presente',
    conjugacion: conjSlide.conjugacion || [],
  });

  // Ejemplos
  const ejemplos = currentData.slides?.filter(s => s.tipo === 'ejemplo') || [];
  for (let i = 0; i < 3; i++) {
    const ej = ejemplos[i] || {};
    slides.push({
      tipo: 'ejemplo', tts: 'zh',
      titulo_zh: `例句 ${i+1}`,
      frase_es: ej.frase_es || '',
      traduccion_zh: ej.traduccion_zh || '',
    });
  }

  // Outro
  const outroSlide = currentData.slides?.find(s => s.tipo === 'outro') || {};
  slides.push({
    tipo: 'outro', tts: 'zh',
    titulo_zh: outroSlide.titulo_zh || `今天学了 ${currentVerbo.toUpperCase()}！`,
    titulo_es: outroSlide.titulo_es || `¡Hoy aprendiste ${currentVerbo.toUpperCase()}!`,
  });

  const payload = {
    tema: `Verbo ${currentVerbo.toUpperCase()}`,
    traduccion_zh: currentData.traduccion_zh || '',
    nivel: currentData.nivel || 'A1',
    frecuencia: currentData.frecuencia || 0,
    tipo_verbo: currentData.tipo || '',
    slides: slides,
  };

  const res = await fetch(`/api/verbo/${currentVerbo}/save`, {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify(payload),
  });

  if (res.ok) {
    currentData.has_script = true;
    currentData.slides = slides;
    // Refresh verbo list
    const listRes = await fetch('/api/verbos');
    allVerbos = await listRes.json();
    renderVerboList();
    document.getElementById('statusText').textContent = `Guardado: ${currentVerbo.toUpperCase()}`;
    toast('✅ Guardado correctamente');
    renderEditor();
  } else {
    toast('❌ Error al guardar');
  }
}

// ═══════════════════════════════════════════
// GENERATE VIDEO
// ═══════════════════════════════════════════

async function generateVideo() {
  if (!currentVerbo) return toast('Selecciona un verbo primero');

  // Save first
  await saveVerbo();

  const modal = document.getElementById('modal');
  const log = document.getElementById('logArea');
  const title = document.getElementById('modalTitle');
  const download = document.getElementById('downloadBtn');

  modal.classList.add('show');
  title.textContent = `Generando ${currentVerbo.toUpperCase()}...`;
  log.innerHTML = '<span class="ok">Iniciando pipeline...</span>';
  download.style.display = 'none';

  // Update sidebar to show generating
  const items = document.querySelectorAll('.verbo-item');
  items.forEach(item => {
    if (item.querySelector('.name').textContent.trim().toLowerCase().startsWith(currentVerbo.toLowerCase())) {
      const dot = item.querySelector('.status-dot');
      dot.className = 'status-dot active-gen';
    }
  });

  try {
    const res = await fetch(`/api/verbo/${currentVerbo}/generate`, {method: 'POST'});
    const data = await res.json();

    if (data.ok) {
      log.innerHTML += '\n<span class="ok">✅ Video generado!</span>';
      log.innerHTML += `\n<span class="ok">📁 ${data.size_kb} KB</span>`;
      download.href = data.video_url;
      download.style.display = 'inline';
      title.textContent = `✅ ${currentVerbo.toUpperCase()} · Video listo`;

      // Refresh
      const listRes = await fetch('/api/verbos');
      allVerbos = await listRes.json();
      currentData.has_video = true;
      currentData.video_url = data.video_url;
      document.getElementById('videoBadge').style.display = 'inline';
      renderVerboList();
      document.getElementById('statusText').textContent = `Video: ${currentVerbo.toUpperCase()}`;

      // Auto-switch to video view
      setView('video');
    } else {
      log.innerHTML += '\n<span class="err">❌ Error</span>';
    }
  } catch (e) {
    log.innerHTML += `\n<span class="err">❌ ${e.message}</span>`;
  }
}

function closeModal() {
  document.getElementById('modal').classList.remove('show');
  renderVerboList();
  // Reload video if we're in video view
  if (currentView === 'video') loadVideo();
}

// ═══════════════════════════════════════════
// UTILS
// ═══════════════════════════════════════════

function toast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2500);
}

// ═══════════════════════════════════════════
// START
// ═══════════════════════════════════════════

init();
