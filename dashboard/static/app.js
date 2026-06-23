/*  -- Hola西班牙语 Dashboard --  */

// -- State --
let curriculo = null;        // full curriculum tree from API
let currentMod = null;       // current module slug
let currentLec = null;       // current lesson slug
let slides = [];             // current lesson's slides
let selectedSlide = 0;       // index of selected slide in slides array
let modified = false;        // unsaved changes?
let generating = false;
let previewTimeout = null;
let autoSaveTimeout = null;
let lastModifiedTime = 0;
let currentXHSDesc = null;  // cached XHS description for current lesson

const SLIDE_TYPES = {
  portada:     { label: 'Portada',     fields: ['titulo_zh','titulo_es','hook_zh','bullets','cta'] },
  xiaohongshu_portada: { label: 'Portada XHS', fields: ['titulo_zh','titulo_es','hook_zh','bullets','cta'] },
  explicacion: { label: 'Explicación', fields: ['titulo_zh','frase_es','traduccion_zh','puntos'] },
  ejemplo:     { label: 'Ejemplo',     fields: ['frase_es','traduccion_zh','analisis'] },
  vocabulario: { label: 'Vocabulario', fields: ['frase_origen','palabras'] },
  comparacion: { label: 'Comparación', fields: ['titulo_zh','indefinido','imperfecto'] },
  ejercicio:   { label: 'Ejercicio',   fields: ['titulo_zh','frase_es','traduccion_zh','analisis'] },
  resumen:     { label: 'Resumen',     fields: ['titulo_zh','titulo_es','puntos'] },
  outro:       { label: 'Outro',       fields: ['texto_zh'] },
};
const TYPE_ICONS = { portada:'P', xiaohongshu_portada:'📕', explicacion:'X', ejemplo:'E', vocabulario:'V', comparacion:'C', ejercicio:'R', resumen:'S', outro:'O' };

const FIELD_LABELS = {
  titulo_zh:'Titulo (ZH)', titulo_es:'Titulo (ES)', puntos:'Puntos',
  frase_es:'Frase (ES)', traduccion_zh:'Traduccion (ZH)', analisis:'Analisis',
  indefinido:'Indefinido', imperfecto:'Imperfecto', texto_zh:'Texto',
  hook_zh:'Hook (ZH)', bullets:'Bullets', cta:'CTA',
};
const FIELD_PLACEHOLDERS = {
  titulo_zh:'Título en chino', titulo_es:'Título en español',
  frase_es:'Ej: Ayer compré...', traduccion_zh:'Ej: 昨天我买了...',
  puntos:'Nuevo punto...',
  hook_zh:'每天5分钟 · 轻松学西语', cta:'点击收藏 · 开始你的西语之旅',
};

function emptySlide(tipo) {
  return {
    tipo, titulo_zh:'', titulo_es:'', puntos:[''], frase_es:'', frase_origen:'',
    palabras: tipo === 'vocabulario' ? [{es:'', zh:''}] : [],
    traduccion_zh:'', analisis:[''], indefinido:'', imperfecto:'', texto_zh:'',
    texto_tts_zh:'', texto_tts_es:'', tts: ['ejemplo','ejercicio'].includes(tipo) ? 'es' : 'zh',
    hook_zh:'', bullets:[], cta:''
  };
}

function escape(s) { return String(s||'').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }


// -- Curriculum --

async function loadCurriculo() {
  const res = await fetch('/api/curriculo');
  curriculo = await res.json();
  renderCurriculo();
  updateProgress();
}

function renderCurriculo() {
  const el = document.getElementById('modulo-list');
  el.innerHTML = '';
  
  // Auto-open first module if nothing selected
  const autoOpen = !currentMod && curriculo.modulos.length > 0;
  if (autoOpen) currentMod = curriculo.modulos[0].slug;
  
  for (const mod of curriculo.modulos) {
    const div = document.createElement('div');
    div.className = 'modulo';
    const isOpen = mod.slug === currentMod;
    const done = mod.lecciones.filter(l=>l.video_exists).length;
    div.innerHTML = `
      <div class="modulo-header" onclick="toggleModulo(this)">
        <span class="arrow ${isOpen?'open':''}">></span>
        <span style="font-size:11px;color:var(--accent2);width:28px;flex-shrink:0">${mod.lecciones.length} lec</span>
        <span class="mod-title">${mod.titulo}</span>
        <span class="mod-count">${done}/${mod.lecciones.length}</span>
      </div>
      <div class="lecciones" style="display:${isOpen?'block':'none'}">
        ${mod.lecciones.map(l => `
          <div class="leccion ${l.video_exists?'video-done':'video-pending'} ${l.slug===currentLec?'active':''}"
               onclick="loadLesson('${mod.slug}','${l.slug}')">
            <span class="icon">${l.es_repaso?'(R)':''}</span>
            <span class="lec-title">${l.tema}</span>
            ${l.video_exists ? `<span class="lec-play" onclick="event.stopPropagation();playLessonVideo('${mod.slug}','${l.slug}')" title="Ver video">></span>` : ''}
            <span class="lec-num">${l.slug.slice(0,3)}</span>
            <span class="lec-status">${l.video_exists?'[OK]':''}</span>
          </div>
        `).join('')}
        <div style="font-size:10px;color:var(--text2);padding:4px 12px;text-align:center;border-top:1px solid rgba(255,255,255,.04);margin-top:4px">
           Click en una lección para abrirla
        </div>
      </div>`;
    el.appendChild(div);
  }
}

function toggleModulo(hdr) {
  const arrow = hdr.querySelector('.arrow');
  const body = hdr.nextElementSibling;
  const open = body.style.display !== 'none';
  body.style.display = open ? 'none' : 'block';
  arrow.classList.toggle('open', !open);
}

function filterLecciones(query) {
  const q = query.toLowerCase().trim();
  document.querySelectorAll('.modulo').forEach(mod => {
    const lecciones = mod.querySelectorAll('.leccion');
    let anyVisible = false;
    lecciones.forEach(l => {
      const title = l.querySelector('.lec-title').textContent.toLowerCase();
      const match = !q || title.includes(q);
      l.style.display = match ? 'flex' : 'none';
      if (match) anyVisible = true;
    });
    // Show/hide the whole module + auto-open if has matches
    const hdr = mod.querySelector('.modulo-header');
    const body = mod.querySelector('.lecciones');
    if (q) {
      hdr.style.display = anyVisible ? 'flex' : 'none';
      if (anyVisible) { body.style.display = 'block'; hdr.querySelector('.arrow').classList.add('open'); }
      else { body.style.display = 'none'; }
    } else {
      hdr.style.display = 'flex';
      body.style.display = 'none';
    }
  });
}

function updateProgress() {
  if (!curriculo) return;
  let total = 0, done = 0;
  for (const m of curriculo.modulos) for (const l of m.lecciones) { total++; if (l.video_exists) done++; }
  document.getElementById('progressStats').textContent = `${done}/${total}`;
  document.getElementById('statusText').textContent = currentLec ? `${currentLec.replace(/-/g,' ')}` : 'Ninguna lección';
}


// -- Load lesson --

async function loadLesson(modSlug, lecSlug) {
  if (generating) return;
  if (modified) {
    if (!confirm('Hay cambios sin guardar. ¿Descartarlos?')) return;
  }
  currentMod = modSlug;
  currentLec = lecSlug;  // keep dashes for API calls!
  selectedSlide = 0;
  modified = false;
  document.getElementById('saveBtn').style.display = 'none';
  document.getElementById('genBtn').disabled = true;
  document.getElementById('genBtn').textContent = 'Cargando...';
  document.getElementById('pipelineBtn').style.display = 'none';

  try {
    const res = await fetch(`/api/leccion/${modSlug}/${lecSlug}`);
    const data = await res.json();
    slides = data.slides || [];
    
    // Show play button if this lesson has a video
    if (data.video_url) {
      currentVideoUrl = data.video_url;
      document.getElementById('playBtn').style.display = '';
    } else {
      currentVideoUrl = null;
      document.getElementById('playBtn').style.display = 'none';
    }
    
    renderCurriculo();
    
    // No script: show "Generar contenido" button AND pipeline
    if (data.script_exists === false) {
      showGenerateContentUI(modSlug, lecSlug, data.tema || lecSlug);
      document.getElementById('genBtn').textContent = 'Generar Video';
      document.getElementById('genBtn').disabled = true;
      document.getElementById('pipelineBtn').style.display = '';
      document.getElementById('xhsBtn').style.display = '';
      updateProgress();
      return;
    }
    
    if (slides.length) {
      selectedSlide = 0;
      renderSlideTabs();
      renderForm(0);
      updateStats();
      // Restore to slide preview instead of video
      restoreSlidePreview();
      refreshPreview();
    }
    // Show XHS description in preview pane if available
    if (data.xhs_description) {
      showXHSDescription(data.xhs_description);
    } else {
      document.getElementById('xhsPreviewDesc').style.display = 'none';
      currentXHSDesc = null;
    }
    document.getElementById('genBtn').textContent = 'Generar Video';
    document.getElementById('genBtn').disabled = false;
    document.getElementById('pipelineBtn').style.display = '';
    document.getElementById('xhsBtn').style.display = '';
    updateProgress();
  } catch(e) {
    showToast('X Error al cargar lección');
    document.getElementById('genBtn').textContent = 'Generar Video';
    document.getElementById('genBtn').disabled = false;
  }
}


// -- Drag & Drop --
let dragIdx = -1;

function renderTabHTML(activeIdx) {
  let html = `<div class="slide-tabs" ondragover="handleDragOver(event)" ondragleave="handleDragLeave(event)" ondrop="handleDrop(event)">`;
  slides.forEach((s, i) => {
    html += `<div class="slide-tab ${i===activeIdx?'active':''}" draggable="true"
      ondragstart="startDrag(event, ${i})"
      ondragend="endDrag(event)"
      ondragover="event.stopPropagation();event.preventDefault();"
      ondragenter="dragEnterTab(event)"
      ondragleave="event.currentTarget.classList.remove('drag-over')"
      ondrop="handleDrop(event, ${i})"
      onclick="selectSlide(${i})">
      <span class="drag-handle">⠿</span>
      <span>${TYPE_ICONS[s.tipo]||''} ${i+1}</span>
      ${slides.length > 1 ? `<span class="del-tab" onclick="event.stopPropagation();removeSlide(${i})">x</span>` : ''}
    </div>`;
  });
  html += `<div class="slide-tab add-tab" onclick="addSlide()">+ Añadir</div>`;
  html += `</div>`;
  return html;
}

function startDrag(e, idx) {
  dragIdx = idx;
  e.dataTransfer.effectAllowed = 'move';
  e.dataTransfer.setData('text/plain', idx);
  e.target.classList.add('dragging');
  e.target.style.opacity = '0.4';
}

function endDrag(e) {
  e.target.classList.remove('dragging');
  e.target.style.opacity = '';
  document.querySelectorAll('.slide-tab.drag-over').forEach(el => el.classList.remove('drag-over'));
  dragIdx = -1;
}

function handleDragOver(e) {
  e.preventDefault();
  e.dataTransfer.dropEffect = 'move';
}

function dragEnterTab(e) {
  // Clear drag-over from all tabs, then highlight current
  document.querySelectorAll('.slide-tab.drag-over').forEach(el => el.classList.remove('drag-over'));
  e.currentTarget.classList.add('drag-over');
}

function handleDragLeave(e) {
  // Only remove if leaving the container, not entering a child
  if (!e.currentTarget.contains(e.relatedTarget)) {
    document.querySelectorAll('.slide-tab.drag-over').forEach(el => el.classList.remove('drag-over'));
  }
}

function handleDrop(e, targetIdx) {
  e.preventDefault();
  e.stopPropagation();
  if (dragIdx < 0 || dragIdx === targetIdx) {
    endDrag(e);
    return;
  }
  // Remove from old position
  const [moved] = slides.splice(dragIdx, 1);
  // Adjust target index if source was before target
  const insertAt = dragIdx < targetIdx ? targetIdx - 1 : targetIdx;
  slides.splice(insertAt, 0, moved);
  // Update selection
  selectedSlide = insertAt;
  modified = true;
  lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
  document.querySelectorAll('.slide-tab.drag-over,.slide-tab.dragging').forEach(el => {
    el.classList.remove('drag-over', 'dragging');
    el.style.opacity = '';
  });
  dragIdx = -1;
  renderSlideTabs();
  renderForm(selectedSlide);
  updateStats();
  refreshPreview();
}

// -- Slide tabs --

function renderSlideTabs() {
  const pane = document.getElementById('formPane');
  pane.innerHTML = renderTabHTML(selectedSlide);
  renderSlideContent();
}

function selectSlide(idx) {
  selectedSlide = idx;
  renderSlideTabs();
  renderForm(idx);
  refreshPreview();
}

function addSlide() {
  const tipo = 'explicacion';
  slides.push(emptySlide(tipo));
  selectSlide(slides.length - 1);
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
  updateStats();
}

function removeSlide(idx) {
  if (slides.length <= 1) { showToast('X Debe haber al menos un slide'); return; }
  slides.splice(idx, 1);
  if (selectedSlide >= slides.length) selectedSlide = slides.length - 1;
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
  renderSlideTabs();
  if (slides.length) renderForm(selectedSlide);
  updateStats();
  refreshPreview();
}


// -- Form --

function renderSlideContent() {
  // This is a stub - renderForm fills content below the tabs
}

function renderForm(idx) {
  const pane = document.getElementById('formPane');
  const s = slides[idx];
  if (!s) return;

  // Show tabs (with drag & drop)
  let html = renderTabHTML(idx);

  // Lesson info
  html += `<div class="lesson-bar">
    <span class="lesson-tema">Slide ${idx+1}</span>
    <span class="lesson-info">${s.titulo_zh || s.frase_es || s.titulo_es || '(sin contenido)'}</span>
  </div>`;

  // Type selector
  html += `<div class="slide-type-selector">`;
  for (const [key, def] of Object.entries(SLIDE_TYPES)) {
    html += `<button class="${key===s.tipo?'active':''}" onclick="changeType(${idx},'${key}')">${def.label}</button>`;
  }
  html += `</div>`;

  // Content fields (titles, phrases, translations, points, etc.)
  const typeFields = SLIDE_TYPES[s.tipo]?.fields || [];
  for (const field of typeFields) {
    html += renderField(idx, s, field);
  }

  // TTS textareas (Spanish + Chinese) for every slide
  html += `<div style="display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:8px">
    <div class="form-group">
      <label>TTS Espanol
        <button onclick="autoTts(${idx},'es')" style="margin-left:4px;background:var(--surface2);color:var(--accent2);border:none;padding:1px 6px;border-radius:4px;font-size:10px;cursor:pointer">Auto</button>
        <button onclick="testTts(${idx},'es')" style="margin-left:2px;background:var(--surface2);color:var(--accent2);border:none;padding:1px 6px;border-radius:4px;font-size:10px;cursor:pointer">Play</button>
      </label>
      <textarea rows="2" style="font-size:11px" data-slide="${idx}" data-field="texto_tts_es" placeholder="Español (Dalia/Jorge)">${escape(s.texto_tts_es||'')}</textarea>
    </div>
    <div class="form-group">
      <label>TTS Chino
        <button onclick="autoTts(${idx},'zh')" style="margin-left:4px;background:var(--surface2);color:var(--accent2);border:none;padding:1px 6px;border-radius:4px;font-size:10px;cursor:pointer">Auto</button>
        <button onclick="testTts(${idx},'zh')" style="margin-left:2px;background:var(--surface2);color:var(--accent2);border:none;padding:1px 6px;border-radius:4px;font-size:10px;cursor:pointer">Play</button>
      </label>
      <textarea rows="2" style="font-size:11px" data-slide="${idx}" data-field="texto_tts_zh" placeholder="Chino (Xiaoxiao)">${escape(s.texto_tts_zh||'')}</textarea>
    </div>
  </div>`;

  html += `<div style="display:flex;gap:4px;margin-top:8px">
    <button onclick="saveCurrentLesson()" style="background:var(--accent);color:#fff;border:none;padding:6px 20px;border-radius:8px;cursor:pointer;font-size:13px;font-weight:600">GUARDAR AHORA</button>
    <button onclick="duplicateSlide(${idx})" style="background:var(--surface2);color:var(--accent2);border:1px solid rgba(255,255,255,.08);padding:4px 14px;border-radius:6px;cursor:pointer;font-size:11px">Duplicar</button>
    <button onclick="moveSlide(${idx},-1)" style="background:var(--surface2);color:var(--text);border:1px solid rgba(255,255,255,.08);padding:4px 14px;border-radius:6px;cursor:pointer;font-size:11px">^</button>
    <button onclick="moveSlide(${idx},1)" style="background:var(--surface2);color:var(--text);border:1px solid rgba(255,255,255,.08);padding:4px 14px;border-radius:6px;cursor:pointer;font-size:11px">v</button>
  </div>`;

  pane.innerHTML = html;
}

function renderField(idx, s, field) {
  const val = s[field] || '';
  const label = FIELD_LABELS[field] || field;
  const placeholder = FIELD_PLACEHOLDERS[field] || '';
  let input = '';

  if (field === 'puntos' || field === 'analisis') {
    const arr = Array.isArray(s[field]) && s[field].length ? s[field] : [''];
    input = `<div class="array-input">`;
    arr.forEach((item, i) => {
      input += `<div class="item">
        <input type="text" value="${escape(item)}" data-slide="${idx}" data-field="${field}" data-subidx="${i}" placeholder="${placeholder}">
        <button class="rm" onclick="removeArrayItem(${idx},'${field}',${i})">x</button>
      </div>`;
    });
    input += `<div class="add" onclick="addArrayItem(${idx},'${field}')">+ Añadir ítem</div></div>`;
  } else if (field === 'palabras') {
    // Array of {es, zh} objects — render as paired inputs
    const arr = Array.isArray(s[field]) && s[field].length ? s[field] : [{es:'', zh:''}];
    input = `<div class="array-input">`;
    arr.forEach((w, i) => {
      const es = (w && w.es) || '';
      const zh = (w && w.zh) || '';
      input += `<div class="item" style="gap:4px">
        <input type="text" value="${escape(es)}" data-slide="${idx}" data-field="palabras" data-subidx="${i}" data-key="es" placeholder="Español" style="flex:1;font-size:13px">
        <button onclick="translateWord(${idx},${i})" title="Traducir al chino" style="background:var(--surface2);color:var(--accent2);border:none;padding:2px 8px;border-radius:4px;cursor:pointer;font-size:11px;white-space:nowrap">译</button>
        <input type="text" value="${escape(zh)}" data-slide="${idx}" data-field="palabras" data-subidx="${i}" data-key="zh" placeholder="Chino" style="flex:2;font-size:12px;color:var(--accent2)">
        <button class="rm" onclick="removeArrayItem(${idx},'palabras',${i})">x</button>
      </div>`;
    });
    input += `<div class="add" onclick="addPalabraItem(${idx})">+ Añadir palabra</div></div>`;
  } else if (field === 'bullets') {
    // Array of {title, sub, icon} objects — paired inputs
    const arr = Array.isArray(s[field]) && s[field].length ? s[field] : [{title:'', sub:'', icon:'dot'}];
    input = `<div class="array-input" style="gap:6px">`;
    arr.forEach((b, i) => {
      const title = (b && b.title) || '';
      const sub = (b && b.sub) || '';
      const icon = (b && b.icon) || 'dot';
      input += `<div class="item" style="gap:4px;align-items:center">
        <select data-slide="${idx}" data-field="bullets" data-subidx="${i}" data-key="icon" style="background:var(--surface2);color:var(--accent3);border:1px solid rgba(255,255,255,.1);border-radius:4px;padding:2px;font-size:11px;width:60px">
          <option value="dot" ${icon==='dot'?'selected':''}>·</option>
          <option value="book" ${icon==='book'?'selected':''}>Book</option>
          <option value="target" ${icon==='target'?'selected':''}>Target</option>
          <option value="fire" ${icon==='fire'?'selected':''}>Fire</option>
          <option value="star" ${icon==='star'?'selected':''}>Star</option>
          <option value="check" ${icon==='check'?'selected':''}>Check</option>
        </select>
        <input type="text" value="${escape(title)}" data-slide="${idx}" data-field="bullets" data-subidx="${i}" data-key="title" placeholder="Título" style="flex:1;font-size:13px">
        <input type="text" value="${escape(sub)}" data-slide="${idx}" data-field="bullets" data-subidx="${i}" data-key="sub" placeholder="Subtítulo" style="flex:1;font-size:12px;color:var(--accent2)">
        <button class="rm" onclick="removeArrayItem(${idx},'bullets',${i})">x</button>
      </div>`;
    });
    input += `<div class="add" onclick="addBulletItem(${idx})">+ Añadir bullet</div></div>`;
  } else {
    const ph = placeholder || '';
    if (field.includes('_es') || field === 'frase_es') {
      input = `<textarea class="code" data-slide="${idx}" data-field="${field}" placeholder="${ph}">${escape(val)}</textarea>`;
    } else {
      input = `<input type="text" value="${escape(val)}" data-slide="${idx}" data-field="${field}" placeholder="${ph}">`;
    }
  }

  return `<div class="form-group"><label>${label}</label>${input}</div>`;
}

function changeType(idx, tipo) {
  slides[idx].tipo = tipo;
  for (const k of Object.keys(slides[idx])) {
    if (!['tipo','tts'].includes(k)) {
      if (k === 'bullets' || k === 'palabras') slides[idx][k] = [];
      else slides[idx][k] = Array.isArray(slides[idx][k]) ? [''] : '';
    }
  }
  if (['ejemplo','ejercicio'].includes(tipo)) slides[idx].tts = 'es';
  else slides[idx].tts = 'zh';
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
  renderForm(idx);
}

function addArrayItem(idx, field) { slides[idx][field].push(''); renderForm(idx); }
function removeArrayItem(idx, field, i) { slides[idx][field].splice(i,1); if(!slides[idx][field].length) slides[idx][field]=['']; renderForm(idx); }
function addPalabraItem(idx) {
  if (!Array.isArray(slides[idx].palabras)) slides[idx].palabras = [];
  slides[idx].palabras.push({es:'', zh:''});
  renderForm(idx);
}

function addBulletItem(idx) {
  if (!Array.isArray(slides[idx].bullets)) slides[idx].bullets = [];
  slides[idx].bullets.push({title:'', sub:'', icon:'dot'});
  renderForm(idx);
}

async function translateWord(idx, i) {
  const word = (slides[idx].palabras[i] && slides[idx].palabras[i].es) || '';
  if (!word.trim()) return;
  const btn = event.target;
  btn.textContent = '...';
  btn.disabled = true;
  try {
    const res = await fetch(`/api/translate-es/${encodeURIComponent(word.trim())}?force=true`);
    const data = await res.json();
    if (data.zh) {
      if (!slides[idx].palabras[i] || typeof slides[idx].palabras[i] !== 'object') {
        slides[idx].palabras[i] = {es: word, zh: ''};
      }
      slides[idx].palabras[i].zh = data.zh;
      renderForm(idx);
      modified = true;
      lastModifiedTime = Date.now();
      document.getElementById('saveBtn').style.display = '';
    }
  } catch(e) { console.error(e); }
  btn.textContent = '译';
  btn.disabled = false;
}

function duplicateSlide(idx) {
  const copy = JSON.parse(JSON.stringify(slides[idx]));
  slides.splice(idx+1, 0, copy);
  selectSlide(idx+1);
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
}

function moveSlide(idx, dir) {
  const dst = idx + dir;
  if (dst < 0 || dst >= slides.length) return;
  [slides[idx], slides[dst]] = [slides[dst], slides[idx]];
  selectSlide(dst);
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
}

function autoTts(idx, lang) {
  const s = slides[idx];
  if (lang === 'zh') {
    s.texto_tts_zh = s.texto_tts_zh || s.titulo_zh || '';
    if (!s.texto_tts_zh && s.puntos) {
      s.texto_tts_zh = s.puntos.filter(p=>p).join('，');
    }
  } else {
    s.texto_tts_es = s.texto_tts_es || s.frase_es || s.titulo_es || '';
    if (s.analisis && s.analisis.length) {
      s.texto_tts_es += '. ' + s.analisis.filter(a=>a).join('. ');
    }
  }
  modified = true; lastModifiedTime = Date.now();
  document.getElementById('saveBtn').style.display = '';
  renderForm(idx);
}

async function testTts(idx, lang) {
  const s = slides[idx];
  const text = lang === 'zh' ? s.texto_tts_zh : s.texto_tts_es;
  if (!text) { showToast('X No hay texto TTS'); return; }
  const fd = new FormData();
  fd.append('lang', lang);
  fd.append('text', text);
  try {
    const res = await fetch('/api/preview-tts', { method:'POST', body:fd });
    const data = await res.json();
    const audioId = `ttsAudio_${idx}_${lang}`;
    let audio = document.getElementById(audioId);
    if (!audio) { audio = document.createElement('audio'); audio.id = audioId; audio.controls = true; audio.style='width:100%;margin-top:4px'; }
    audio.src = data.audio;
    audio.style.display = 'block';
    audio.play();
  } catch(e) { showToast('X Error TTS'); }
}


// -- Save --

async function saveCurrentLesson() {
  if (!currentMod || !currentLec) {
    showToast('Error: No hay leccion cargada');
    return;
  }
  const btn = document.getElementById('saveBtn');
  if (!btn) return;
  btn.textContent = 'Guardando...';
  btn.disabled = true;
  try {
    const payload = { modulo_slug:currentMod, leccion_slug:currentLec, slides };
    const res = await fetch(`/api/leccion/${currentMod}/${currentLec}/save`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(payload),
    });
    const data = await res.json();
    if (!res.ok) throw new Error(data.detail || 'Error');
    modified = false;
    btn.textContent = 'Guardado';
    setTimeout(() => { btn.textContent = 'Guardar'; btn.disabled = false; btn.style.display='none'; }, 1500);
  } catch(e) {
    btn.textContent = 'Error';
    btn.disabled = false;
    showToast('Error: ' + e.message);
  }
}


// -- Preview --

function refreshPreview() {
  if (previewTimeout) clearTimeout(previewTimeout);
  previewTimeout = setTimeout(doPreview, 400);
}

async function doPreview() {
  const s = slides[selectedSlide];
  if (!s) return;
  try {
    const res = await fetch('/api/preview-slide', {
      method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(s),
    });
    const data = await res.json();
    document.getElementById('phoneFrame').innerHTML = `<img src="${data.image}" alt="preview">`;
    // Show play button if a video was generated
    if (currentVideoUrl) {
      const btn = document.getElementById('playBtn');
      if (btn) btn.style.display = '';
    }
  } catch(e) {}
}

function updateStats() {
  let totalSecs = 0, zh=0, es=0;
  for (const s of slides) {
    // Count both TTS texts per slide
    if (s.texto_tts_zh) {
      totalSecs += Math.max(s.texto_tts_zh.length/5, 2);
      zh++;
    }
    if (s.texto_tts_es) {
      totalSecs += Math.max(s.texto_tts_es.length/4, 2);
      es++;
    }
    // Add 1.5s silence gap if both exist
    if (s.texto_tts_zh && s.texto_tts_es) totalSecs += 1.5;
  }
  document.getElementById('slideNum').textContent = slides.length;
  document.getElementById('estDur').textContent = `${Math.round(totalSecs)}s`;
  document.getElementById('estLang').textContent = `${zh}ZH ${es}ES`;
}


// -- Generate --

let currentVideoUrl = null;

async function generateVideo() {
  if (generating || !slides.length) return;
  generating = true;
  const btn = document.getElementById('genBtn');
  btn.disabled = true; btn.textContent = 'Generando...';

  const modal = document.getElementById('modal');
  modal.classList.add('show');
  const log = document.getElementById('logArea');
  const prog = document.getElementById('progressFill');
  const dl = document.getElementById('downloadLink');
  dl.style.display = 'none';
  log.innerHTML = ''; prog.style.width = '0%';

  appendLog(' Generando video...', 'info');

  const project = {
    nivel: 'A1',
    tema: (currentLec||'').replace(/-/g,' '),
    duracion_base: 2.5,
    slides,
  };

  try {
    prog.style.width = '20%';
    appendLog(` ${slides.length} slides`, 'ok');
    prog.style.width = '40%';
    appendLog('Play Generando TTS...', 'info');

    const qs = currentMod && currentLec ? `?modulo_slug=${currentMod}&leccion_slug=${currentLec}` : '';
    const res = await fetch(`/api/generate${qs}`, {
      method:'POST', headers:{'Content-Type':'application/json'}, body:JSON.stringify(project),
    });
    prog.style.width = '80%';

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Error del servidor');
    }

    const data = await res.json();
    prog.style.width = '100%';
    
    currentVideoUrl = data.video_url;
    const videoFile = data.filename;
    const sizeKb = Math.round(data.size_kb);
    
    appendLog(`[OK] Video listo: ${videoFile} (${sizeKb} KB)`, 'ok');

    // Show XHS description if available
    if (data.xhs_description) {
      showXHSDescription(data.xhs_description);
      appendLog('[OK] Descripción XHS generada — copiala abajo ', 'ok');
    }

    // Set download link
    dl.href = currentVideoUrl;
    dl.download = videoFile;
    dl.style.display = 'inline-block';
    dl.textContent = 'v Descargar';
    
    // Show video in preview pane
    showVideoInPreview(currentVideoUrl, videoFile.replace('.mp4','').replace('Hola_A1_',''));
    
    appendLog('¡Video listo! Se reproduce en la vista previa ->', 'ok');

    // Refresh curriculum status
    await loadCurriculo();

  } catch(e) {
    appendLog(`X ${e.message}`, 'err');
    showToast(`X ${e.message}`);
  }

  generating = false;
  btn.disabled = false; btn.textContent = 'Generar Video';
}

function showVideoInPreview(videoUrl, label) {
  const frame = document.getElementById('phoneFrame');
  // Check if a video is already playing
  const existing = frame.querySelector('video');
  if (existing) {
    existing.src = videoUrl;
    existing.play();
    // Update label
    const lbl = document.querySelector('.preview-meta .video-label');
    if (lbl) lbl.textContent = `${label}`;
    document.getElementById('playBtn').style.display = 'none';
    return;
  }
  
  frame.innerHTML = `<video controls autoplay style="width:100%;height:100%;object-fit:contain;background:#000">
    <source src="${videoUrl}" type="video/mp4">
  </video>`;
  
  // Hide the play button since video is now showing
  document.getElementById('playBtn').style.display = 'none';
  
  // Update preview meta to show video info
  const meta = document.querySelector('.preview-meta');
  if (meta) {
    let lbl = meta.querySelector('.video-label');
    if (!lbl) {
      const stat = document.createElement('div');
      stat.className = 'stat';
      stat.innerHTML = `<div class="val video-label">${label}</div><div class="lbl">Último video</div>`;
      meta.appendChild(stat);
    } else {
      lbl.textContent = `${label}`;
    }
  }
}

function appendLog(msg, cls) {
  const el = document.getElementById('logArea');
  el.innerHTML += `<div class="${cls}">${msg}</div>`;
  el.scrollTop = el.scrollHeight;
}

function showGenerateContentUI(modSlug, lecSlug, tema) {
  // Hide slide tabs/form, show a generate button in the main area
  document.getElementById('tabBar').innerHTML = '';
  document.getElementById('formPane').innerHTML = `
    <div style="display:flex;flex-direction:column;align-items:center;justify-content:center;height:100%;gap:16px;padding:40px;text-align:center">
      <div style="font-size:18px;color:var(--text1);font-weight:600">${tema}</div>
      <div style="font-size:13px;color:var(--text2);max-width:320px">Esta lección aún no tiene contenido. Genéralo desde el currículo para poder editarlo.</div>
      <button class="btn-gen" onclick="generateContent('${modSlug}','${lecSlug}')" style="font-size:15px;padding:12px 32px">Generar Contenido</button>
    </div>`;
  document.getElementById('phoneFrame').innerHTML = '<div class="placeholder"> Contenido no generado</div>';
  document.getElementById('genBtn').disabled = true;
}

async function generateContent(modSlug, lecSlug) {
  const btn = document.querySelector('#formPane button');
  btn.disabled = true;
  btn.textContent = 'Generando...';
  try {
    const res = await fetch(`/api/leccion/${modSlug}/${lecSlug}/generate`, { method:'POST' });
    const data = await res.json();
    if (data.status === 'ok') {
      slides = data.slides || [];
      selectedSlide = 0;
      renderSlideTabs();
      renderForm(0);
      updateStats();
      restoreSlidePreview();
      refreshPreview();
      document.getElementById('genBtn').disabled = false;
      renderCurriculo();
      showToast('[OK] Contenido generado');
    } else {
      showToast('X Error al generar');
    }
  } catch(e) {
    showToast('X Error: ' + e.message);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Generar Contenido';
  }
}

function replayVideo() {
  if (currentVideoUrl) {
    showVideoInPreview(currentVideoUrl, currentLec || 'video');
    document.getElementById('playBtn').style.display = 'none';
  }
}

function generateXHSCover() {
  if (!currentMod || !currentLec) {
    showToast('X Carga una lección primero');
    return;
  }
  const url = `/api/cover-xhs/${currentMod}/${currentLec}?t=${Date.now()}`;
  window.open(url, '_blank');
  showToast('📕 Portada XHS generada en nueva pestaña');
}

function playLessonVideo(modSlug, lecSlug) {
  const videoUrl = `/api/video/Hola_A1_${lecSlug}.mp4?t=${Date.now()}`;
  currentVideoUrl = videoUrl;
  showVideoInPreview(videoUrl, lecSlug.replace(/-/g, ' '));
  document.getElementById('playBtn').style.display = 'none';
}

function restoreSlidePreview() {
  const frame = document.getElementById('phoneFrame');
  frame.innerHTML = '<div class="placeholder">Cargando preview...</div>';
  // Show the play button if there's a video from a previous generation
  if (currentVideoUrl) {
    document.getElementById('playBtn').style.display = '';
  }
}

function closeModal() {
  document.getElementById('modal').classList.remove('show');
  document.getElementById('xhsDescSection').style.display = 'none';
  document.getElementById('xhsDescText').value = '';
}

function showToast(msg) {
  const el = document.getElementById('toast');
  el.textContent = msg; el.classList.add('show');
  setTimeout(() => el.classList.remove('show'), 3000);
}

function copyXHSDesc() {
  const ta = document.getElementById('xhsDescText');
  navigator.clipboard.writeText(ta.value).then(() => {
    const ok = document.getElementById('xhsCopyOk');
    ok.style.display = 'inline';
    setTimeout(() => ok.style.display = 'none', 2000);
  });
}

function showXHSDescription(desc) {
  if (!desc) return;
  // Store for the preview pane
  currentXHSDesc = desc;
  // Show in modal
  document.getElementById('xhsDescText').value = desc;
  document.getElementById('xhsDescSection').style.display = 'block';
  // Show in preview pane permanently
  document.getElementById('xhsDescPreviewText').value = desc;
  document.getElementById('xhsPreviewDesc').style.display = 'block';
}

function copyXHSDescPreview() {
  const ta = document.getElementById('xhsDescPreviewText');
  navigator.clipboard.writeText(ta.value).then(() => showToast('📋 ¡Descripción copiada!'));
}


// -- Settings --

async function loadSettings() {
  try {
    const res = await fetch('/api/settings');
    const s = await res.json();
    document.getElementById('cfgFontScale').value = s.font_scale || 1.0;
    document.getElementById('cfgFontScaleVal').textContent = Math.round((s.font_scale||1)*100)+'%';
    document.getElementById('cfgSpacingScale').value = s.spacing_scale || 1.0;
    document.getElementById('cfgSpacingScaleVal').textContent = Math.round((s.spacing_scale||1)*100)+'%';
    const c = s.colors || {};
    document.getElementById('cfgColorGold').value = rgbToHex(c.gold || [255,200,50]);
    document.getElementById('cfgColorBlue').value = rgbToHex(c.blue || [80,180,255]);
    document.getElementById('cfgBgTop').value = rgbToHex(c.bg_top || [15,18,30]);
    document.getElementById('cfgBgBot').value = rgbToHex(c.bg_bot || [30,20,50]);
    const b = s.brand || {};
    document.getElementById('cfgBrandName').value = b.name || '';
    document.getElementById('cfgBrandShow').checked = b.show !== false;
    if (b.logo) document.getElementById('cfgLogoStatus').textContent = 'Logo cargado';
    document.getElementById('cfgSubtitles').checked = s.subtitles === true;
  } catch(e) {}
}

function rgbToHex(rgb) {
  return '#' + rgb.map(x => x.toString(16).padStart(2,'0')).join('');
}

function hexToRgb(hex) {
  const m = /^#?([a-f\d]{2})([a-f\d]{2})([a-f\d]{2})$/i.exec(hex);
  return m ? [parseInt(m[1],16), parseInt(m[2],16), parseInt(m[3],16)] : [255,200,50];
}

async function saveSettings() {
  const settings = {
    font_scale: parseFloat(document.getElementById('cfgFontScale').value),
    spacing_scale: parseFloat(document.getElementById('cfgSpacingScale').value),
    colors: {
      gold: hexToRgb(document.getElementById('cfgColorGold').value),
      blue: hexToRgb(document.getElementById('cfgColorBlue').value),
      bg_top: hexToRgb(document.getElementById('cfgBgTop').value),
      bg_bot: hexToRgb(document.getElementById('cfgBgBot').value),
    },
    brand: {
      name: document.getElementById('cfgBrandName').value,
      show: document.getElementById('cfgBrandShow').checked,
    },
    subtitles: document.getElementById('cfgSubtitles').checked
  };
  try {
    const res = await fetch('/api/settings', {
      method:'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify(settings)
    });
    if (res.ok) { showToast('Config guardada'); refreshPreview(); }
    else showToast('Error al guardar config');
  } catch(e) { showToast('Error: '+e.message); }
}

async function uploadLogo() {
  const file = document.getElementById('cfgLogoFile').files[0];
  if (!file) { showToast('Selecciona un archivo'); return; }
  const form = new FormData();
  form.append('file', file);
  try {
    const res = await fetch('/api/settings/logo', { method:'POST', body: form });
    if (res.ok) { showToast('Logo subido'); document.getElementById('cfgLogoStatus').textContent = 'OK'; }
    else showToast('Error al subir logo');
  } catch(e) { showToast('Error: '+e.message); }
}

function toggleSettings() {
  const modal = document.getElementById('settingsModal');
  if (modal.style.display === 'flex') {
    modal.style.display = 'none';
  } else {
    loadSettings();
    modal.style.display = 'flex';
  }
}


// -- Auto-save (checks every 2s, saves if dirty and idle >1.5s) --

async function autoSaveIfNeeded() {
  if (!modified || !currentMod || !currentLec || generating) return;
  if (Date.now() - lastModifiedTime < 1500) return;
  modified = false;
  try {
    const res = await fetch(`/api/leccion/${currentMod}/${currentLec}/save`, {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify({ modulo_slug:currentMod, leccion_slug:currentLec, slides }),
    });
    if (res.ok) {
      console.log('Auto-guardado OK');
      showToast('Guardado');
      document.getElementById('statusText').textContent = (currentLec||'').replace(/-/g,' ');
    }
  } catch(e) { console.error('Auto-guardado fallo:', e); }
}


// -- Full Pipeline: one-click curriculum → video --

async function runFullPipeline() {
  if (generating || !currentMod || !currentLec) return;
  
  // Confirm before overwriting existing content
  if (slides.length > 0) {
    if (!confirm('⚠️ Esto regenerará la lección actual desde cero.\nLos cambios manuales en ESTA lección se perderán.\nSolo afecta a esta lección, no a las demás. ¿Continuar?')) return;
  }
  
  generating = true;
  const btn = document.getElementById('pipelineBtn');
  btn.disabled = true;
  btn.textContent = '⏳ Pipeline...';
  
  // Also disable gen button
  document.getElementById('genBtn').disabled = true;
  
  const modal = document.getElementById('modal');
  modal.classList.add('show');
  document.getElementById('modalTitle').textContent = '🚀 Pipeline — ' + (currentLec || '').replace(/-/g, ' ');
  const log = document.getElementById('logArea');
  const prog = document.getElementById('progressFill');
  const dl = document.getElementById('downloadLink');
  dl.style.display = 'none';
  log.innerHTML = '';
  prog.style.width = '0%';
  
  appendLog('📝 Regenerando esta lección desde el currículo...', 'info');
  appendLog('   Reglas activas: instrucciones en chino, contenido en español, dual TTS', 'info');
  prog.style.width = '15%';
  
  try {
    const res = await fetch(`/api/leccion/${currentMod}/${currentLec}/full-pipeline`, {
      method: 'POST',
    });
    
    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || 'Error del servidor');
    }
    
    prog.style.width = '70%';
    appendLog('🎨 Renderizando slides...', 'ok');
    appendLog('🔊 Generando TTS bilingüe (ZH → ES)...', 'ok');
    
    const data = await res.json();
    prog.style.width = '100%';
    
    // Update slides with fresh content — reload from YAML for 100% consistency
    modified = false;
    document.getElementById('saveBtn').style.display = 'none';
    
    // Full reload from API (reads the YAML that was just regenerated)
    const reload = await fetch(`/api/leccion/${currentMod}/${currentLec}`);
    const fresh = await reload.json();
    if (fresh.slides && fresh.slides.length) {
      slides = fresh.slides;
    } else {
      slides = data.slides || [];
    }
    selectedSlide = 0;
    renderSlideTabs();
    renderForm(0);
    updateStats();
    restoreSlidePreview();
    refreshPreview();
    
    // Show video
    currentVideoUrl = data.video_url;
    const sizeKb = Math.round(data.size_kb);
    appendLog(`✅ Video listo: ${data.filename} (${sizeKb} KB)`, 'ok');
    
    dl.href = currentVideoUrl;
    dl.download = data.filename;
    dl.style.display = 'inline-block';
    dl.textContent = '📥 Descargar';
    
    showVideoInPreview(currentVideoUrl, currentLec.replace(/-/g, ' '));
    document.getElementById('playBtn').style.display = 'none';
    
    appendLog('🎉 ¡Video listo! Slides y reproductor actualizados.', 'ok');

    // Show XHS description if available
    if (data.xhs_description) {
      showXHSDescription(data.xhs_description);
      appendLog('[OK] Descripción XHS generada — copiala abajo ', 'ok');
    }
    
    // Refresh curriculum to update video status
    await loadCurriculo();
    
  } catch(e) {
    appendLog(`❌ ${e.message}`, 'err');
    showToast(`❌ ${e.message}`);
  }
  
  generating = false;
  btn.disabled = false;
  btn.textContent = '🚀 Pipeline';
  document.getElementById('genBtn').disabled = false;
}

// -- Boot --
document.addEventListener('DOMContentLoaded', () => {
  loadCurriculo();
  setInterval(autoSaveIfNeeded, 2000);  // check every 2 seconds
  
  // Delegated input handler — catches ALL field changes from the form pane
  document.addEventListener('input', (e) => {
    const el = e.target;
    const slideIdx = el.dataset?.slide;
    const fieldName = el.dataset?.field;
    const subIdx = el.dataset?.subidx;
    if (slideIdx === undefined || !fieldName) return;
    const idx = parseInt(slideIdx);
    if (isNaN(idx) || !slides[idx]) return;
    
    if (subIdx !== undefined) {
      const si = parseInt(subIdx);
      const key = el.dataset?.key;
      // Array field: puntos, analisis (string arrays) or palabras/bullets (object array)
      if (fieldName === 'palabras') {
        if (!Array.isArray(slides[idx].palabras)) slides[idx].palabras = [];
        if (!slides[idx].palabras[si] || typeof slides[idx].palabras[si] !== 'object') {
          slides[idx].palabras[si] = {es:'', zh:''};
        }
        if (key) slides[idx].palabras[si][key] = el.value;
      } else if (fieldName === 'bullets') {
        if (!Array.isArray(slides[idx].bullets)) slides[idx].bullets = [];
        if (!slides[idx].bullets[si] || typeof slides[idx].bullets[si] !== 'object') {
          slides[idx].bullets[si] = {title:'', sub:'', icon:'dot'};
        }
        if (key) slides[idx].bullets[si][key] = el.value;
      } else {
        if (!Array.isArray(slides[idx][fieldName])) slides[idx][fieldName] = [''];
        slides[idx][fieldName][si] = el.value;
      }
    } else {
      slides[idx][fieldName] = el.value;
    }
    modified = true; lastModifiedTime = Date.now();
    lastModifiedTime = Date.now();
    document.getElementById('saveBtn').style.display = '';
    updateStats();
    refreshPreview();
  });
});
