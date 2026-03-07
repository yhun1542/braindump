#!/usr/bin/env python3
"""
아카이브 탭 대폭 업그레이드 패치 스크립트
적용 대상: galaxy.html, iphone.html, index.html
"""

# ─── 새 아카이브 CSS ───────────────────────────────────────────────────────────
NEW_ARC_CSS = """
/* ════════════════════════════════════════
   ARCHIVE TAB — UPGRADED v2
   ════════════════════════════════════════ */
.arc-header {
  padding: 16px 16px 8px;
  display: flex; align-items: center; gap: 10px;
}
.arc-search {
  flex: 1; padding: 10px 14px;
  background: var(--surface); border: 1.5px solid var(--border-mid);
  border-radius: 12px; font-size: 14px; color: var(--text);
  font-family: var(--font); outline: none;
}
.arc-search::placeholder { color: var(--text3); }
.arc-header-actions { display: flex; gap: 8px; align-items: center; }
.arc-upload-btn {
  width: 40px; height: 40px; border-radius: 12px;
  background: var(--hdr-bg); color: var(--hdr-text);
  border: none; font-size: 18px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.arc-sort-btn {
  width: 36px; height: 36px; border-radius: 10px;
  background: var(--surface); border: 1.5px solid var(--border-mid);
  color: var(--text2); font-size: 14px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  flex-shrink: 0;
}
.arc-cats {
  display: flex; gap: 8px; padding: 0 16px 12px;
  overflow-x: auto; -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.arc-cats::-webkit-scrollbar { display: none; }
.arc-cat-btn {
  padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;
  border: 1.5px solid var(--border-mid); background: var(--surface);
  color: var(--text2); cursor: pointer; white-space: nowrap;
  display: flex; align-items: center; gap: 4px;
}
.arc-cat-btn.active {
  background: var(--hdr-bg); color: var(--hdr-text); border-color: var(--hdr-bg);
}
.arc-cat-count {
  background: rgba(0,0,0,0.12); border-radius: 8px;
  padding: 1px 5px; font-size: 10px; font-weight: 700;
}
.arc-cat-btn.active .arc-cat-count { background: rgba(255,255,255,0.25); }
.arc-grid { padding: 0 16px 80px; }

/* ── 아카이브 카드 ── */
.arc-item {
  background: var(--surface); border-radius: 16px;
  border: 1.5px solid var(--border-mid);
  margin-bottom: 12px; overflow: hidden;
  box-shadow: var(--shadow);
  transition: transform 0.15s, box-shadow 0.15s;
  position: relative;
}
.arc-item.pinned {
  border-color: #f59e0b;
  box-shadow: 0 2px 12px rgba(245,158,11,0.18);
}
.arc-item:active { transform: scale(0.985); }

/* 핀 배지 */
.arc-pin-badge {
  position: absolute; top: 10px; right: 10px;
  font-size: 14px; line-height: 1; z-index: 2;
}

/* 헤더 */
.arc-item-header {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 14px 8px;
}
.arc-type-icon {
  width: 38px; height: 38px; border-radius: 11px;
  display: flex; align-items: center; justify-content: center;
  font-size: 19px; flex-shrink: 0;
}
.arc-type-note   { background: #fff3e0; }
.arc-type-url    { background: #e3f2fd; }
.arc-type-image  { background: #fce4ec; }
.arc-type-video  { background: #f3e5f5; }
.arc-type-file   { background: #e8f5e9; }
.arc-item-info { flex: 1; min-width: 0; }
.arc-item-title {
  font-size: 14px; font-weight: 700; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  padding-right: 24px;
}
.arc-item-meta { font-size: 11px; color: var(--text3); margin-top: 2px; display: flex; align-items: center; gap: 6px; }
.arc-ai-tag {
  font-size: 10px; padding: 3px 8px; border-radius: 6px;
  background: rgba(108,99,255,0.1); color: var(--accent);
  font-weight: 700; flex-shrink: 0; white-space: nowrap;
}

/* ── URL 링크 미리보기 카드 ── */
.arc-link-card {
  margin: 0 14px 12px;
  border: 1.5px solid var(--border-mid);
  border-radius: 12px; overflow: hidden;
  cursor: pointer;
  transition: background 0.15s;
  display: flex; align-items: stretch;
  background: var(--bg);
  text-decoration: none;
}
.arc-link-card:active { background: var(--line); }
.arc-link-accent {
  width: 4px; flex-shrink: 0;
  background: linear-gradient(180deg, #3b82f6, #6366f1);
}
.arc-link-body {
  flex: 1; padding: 10px 12px; min-width: 0;
}
.arc-link-domain {
  font-size: 11px; color: var(--accent); font-weight: 600;
  display: flex; align-items: center; gap: 5px; margin-bottom: 3px;
}
.arc-link-favicon {
  width: 14px; height: 14px; border-radius: 3px;
  object-fit: contain;
}
.arc-link-url {
  font-size: 12px; color: var(--text2);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
  line-height: 1.4;
}
.arc-link-open-icon {
  padding: 0 12px; display: flex; align-items: center;
  color: var(--text3); font-size: 16px; flex-shrink: 0;
}

/* ── 노트 미리보기 ── */
.arc-item-preview {
  padding: 0 14px 12px; font-size: 13px; color: var(--text2);
  line-height: 1.55;
}
.arc-item-preview img {
  width: 100%; border-radius: 10px; max-height: 180px; object-fit: cover;
}

/* ── 액션 버튼 ── */
.arc-item-actions {
  display: flex; border-top: 1px solid var(--line);
}
.arc-action-btn {
  flex: 1; padding: 11px 6px; border: none; background: transparent;
  font-size: 12px; font-weight: 600; color: var(--text2); cursor: pointer;
  border-right: 1px solid var(--line);
  display: flex; align-items: center; justify-content: center; gap: 3px;
  transition: background 0.12s;
}
.arc-action-btn:active { background: var(--line); }
.arc-action-btn:last-child { border-right: none; }
.arc-action-btn.danger { color: #e74c3c; }
.arc-action-btn.primary { color: var(--accent); }

/* ── 빈 상태 ── */
.arc-empty { text-align: center; padding: 60px 20px; color: var(--text3); }
.arc-empty-icon { font-size: 48px; margin-bottom: 12px; }

/* ── 컨텍스트 메뉴 ── */
.arc-ctx-menu {
  position: fixed; z-index: 9999;
  background: var(--surface); border-radius: 14px;
  border: 1.5px solid var(--border-mid);
  box-shadow: 0 8px 32px rgba(0,0,0,0.18);
  min-width: 180px; overflow: hidden;
  animation: ctxFadeIn 0.15s ease;
}
@keyframes ctxFadeIn {
  from { opacity: 0; transform: scale(0.92); }
  to   { opacity: 1; transform: scale(1); }
}
.arc-ctx-item {
  padding: 13px 18px; font-size: 14px; font-weight: 500;
  color: var(--text); cursor: pointer; display: flex; align-items: center; gap: 10px;
  border-bottom: 1px solid var(--line);
  transition: background 0.1s;
}
.arc-ctx-item:last-child { border-bottom: none; }
.arc-ctx-item:active { background: var(--line); }
.arc-ctx-item.danger { color: #e74c3c; }
.arc-ctx-overlay {
  position: fixed; inset: 0; z-index: 9998;
  background: transparent;
}

/* ── 편집 오버레이 ── */
.arc-edit-overlay {
  position: fixed; inset: 0; z-index: 9000;
  background: rgba(0,0,0,0.45); display: flex;
  align-items: flex-end; justify-content: center;
}
.arc-edit-overlay.hidden { display: none; }

/* ── 정렬 드롭다운 ── */
.arc-sort-menu {
  position: absolute; right: 16px; top: 60px;
  background: var(--surface); border-radius: 12px;
  border: 1.5px solid var(--border-mid);
  box-shadow: 0 4px 20px rgba(0,0,0,0.15);
  z-index: 500; min-width: 150px; overflow: hidden;
  animation: ctxFadeIn 0.15s ease;
}
.arc-sort-item {
  padding: 12px 16px; font-size: 13px; font-weight: 500;
  color: var(--text); cursor: pointer; display: flex; align-items: center; gap: 8px;
  border-bottom: 1px solid var(--line);
}
.arc-sort-item:last-child { border-bottom: none; }
.arc-sort-item.active { color: var(--accent); font-weight: 700; }
.arc-sort-item:active { background: var(--line); }
"""

# ─── 새 아카이브 HTML (탭 패널) ───────────────────────────────────────────────
OLD_ARC_PANE = '''    <div class="tab-pane" id="pane-archive">
      <div class="arc-header">
        <input class="arc-search" id="arcSearch" placeholder="🔍 아카이브 검색...">
        <button class="arc-upload-btn" id="arcUploadBtn">+</button>
      </div>
      <div class="arc-cats">
        <button class="arc-cat-btn active" data-cat="all">전체</button>
        <button class="arc-cat-btn" data-cat="note">노트</button>
        <button class="arc-cat-btn" data-cat="url">링크</button>
        <button class="arc-cat-btn" data-cat="image">사진</button>
        <button class="arc-cat-btn" data-cat="video">동영상</button>
        <button class="arc-cat-btn" data-cat="file">파일</button>
      </div>
      <div class="arc-grid" id="arcGrid"></div>
    </div>'''

NEW_ARC_PANE = '''    <div class="tab-pane" id="pane-archive">
      <div class="arc-header">
        <input class="arc-search" id="arcSearch" placeholder="🔍 아카이브 검색...">
        <div class="arc-header-actions">
          <button class="arc-sort-btn" id="arcSortBtn" title="정렬">⇅</button>
          <button class="arc-upload-btn" id="arcUploadBtn">+</button>
        </div>
      </div>
      <div class="arc-cats">
        <button class="arc-cat-btn active" data-cat="all">전체 <span class="arc-cat-count" id="cnt-all">0</span></button>
        <button class="arc-cat-btn" data-cat="note">📝 노트 <span class="arc-cat-count" id="cnt-note">0</span></button>
        <button class="arc-cat-btn" data-cat="url">🔗 링크 <span class="arc-cat-count" id="cnt-url">0</span></button>
        <button class="arc-cat-btn" data-cat="image">🖼 사진 <span class="arc-cat-count" id="cnt-image">0</span></button>
        <button class="arc-cat-btn" data-cat="video">🎬 동영상 <span class="arc-cat-count" id="cnt-video">0</span></button>
        <button class="arc-cat-btn" data-cat="file">📄 파일 <span class="arc-cat-count" id="cnt-file">0</span></button>
        <button class="arc-cat-btn" data-cat="pinned">⭐ 즐겨찾기 <span class="arc-cat-count" id="cnt-pinned">0</span></button>
      </div>
      <div class="arc-grid" id="arcGrid"></div>
    </div>'''

# ─── 새 아카이브 업로드 오버레이 ──────────────────────────────────────────────
OLD_ARC_OVERLAY = '''<!-- Archive Upload Sheet -->
<div class="arc-overlay hidden" id="arcOverlay">
  <div class="sheet">
    <div class="sheet-handle"></div>
    <div class="sheet-title">아카이브에 추가</div>
    <div class="sheet-field">
      <div class="sheet-label">유형</div>
      <select class="sheet-select" id="arcType">
        <option value="note">📝 노트</option>
        <option value="url">🔗 URL 링크</option>
        <option value="image">🖼 사진</option>
        <option value="video">🎬 동영상</option>
        <option value="file">📄 파일</option>
      </select>
    </div>
    <div class="sheet-field">
      <div class="sheet-label">제목</div>
      <input class="sheet-input" id="arcTitle" placeholder="제목...">
    </div>
    <div class="sheet-field" id="arcContentField">
      <div class="sheet-label">내용 / URL</div>
      <textarea class="sheet-textarea" id="arcContent" placeholder="내용이나 URL을 입력하세요..."></textarea>
    </div>
    <div class="sheet-field" id="arcFileField" style="display:none">
      <div class="sheet-label">파일 선택</div>
      <input type="file" id="arcFile" accept="image/*,video/*,.pdf,.doc,.docx,.txt" style="width:100%;padding:10px;background:var(--bg);border:1.5px solid var(--border-mid);border-radius:10px;color:var(--text);">
    </div>
    <div class="sheet-btns">
      <button class="sheet-cancel" id="arcCancel">취소</button>
      <button class="sheet-save" id="arcSave">저장 + AI 분류</button>
    </div>
  </div>
</div>'''

NEW_ARC_OVERLAY = '''<!-- Archive Upload Sheet -->
<div class="arc-overlay hidden" id="arcOverlay">
  <div class="sheet">
    <div class="sheet-handle"></div>
    <div class="sheet-title" id="arcOverlayTitle">아카이브에 추가</div>
    <div class="sheet-field">
      <div class="sheet-label">유형</div>
      <select class="sheet-select" id="arcType">
        <option value="note">📝 노트</option>
        <option value="url">🔗 URL 링크</option>
        <option value="image">🖼 사진</option>
        <option value="video">🎬 동영상</option>
        <option value="file">📄 파일</option>
      </select>
    </div>
    <div class="sheet-field">
      <div class="sheet-label">제목</div>
      <input class="sheet-input" id="arcTitle" placeholder="제목...">
    </div>
    <div class="sheet-field" id="arcContentField">
      <div class="sheet-label">내용 / URL</div>
      <textarea class="sheet-textarea" id="arcContent" rows="3" placeholder="내용이나 URL을 입력하세요...&#10;URL을 붙여넣으면 자동으로 링크로 저장됩니다"></textarea>
    </div>
    <div class="sheet-field" id="arcFileField" style="display:none">
      <div class="sheet-label">파일 선택</div>
      <input type="file" id="arcFile" accept="image/*,video/*,.pdf,.doc,.docx,.txt" style="width:100%;padding:10px;background:var(--bg);border:1.5px solid var(--border-mid);border-radius:10px;color:var(--text);">
    </div>
    <input type="hidden" id="arcEditId" value="">
    <div class="sheet-btns">
      <button class="sheet-cancel" id="arcCancel">취소</button>
      <button class="sheet-save" id="arcSave">저장 + AI 분류</button>
    </div>
  </div>
</div>

<!-- Archive Context Menu -->
<div class="arc-ctx-overlay hidden" id="arcCtxOverlay"></div>
<div class="arc-ctx-menu hidden" id="arcCtxMenu">
  <div class="arc-ctx-item" id="arcCtxOpen">🔗 링크 열기</div>
  <div class="arc-ctx-item" id="arcCtxPin">⭐ 즐겨찾기 추가</div>
  <div class="arc-ctx-item" id="arcCtxEdit">✏️ 편집</div>
  <div class="arc-ctx-item" id="arcCtxToday">📅 Today로 이동</div>
  <div class="arc-ctx-item danger" id="arcCtxDel">🗑 삭제</div>
</div>'''

# ─── 새 아카이브 JS 로직 ──────────────────────────────────────────────────────
OLD_ARC_JS = '''function renderArcGrid(filter='') {
  const kw = filter.toLowerCase();
  let items = currentArcCat==='all' ? arcItems : arcItems.filter(i=>i.type===currentArcCat);
  if(kw) items = items.filter(i=>(i.title+i.content).toLowerCase().includes(kw));
  if(!items.length) {
    arcGrid.innerHTML = `<div class="arc-empty"><div class="arc-empty-icon">🗂</div><div>아직 저장된 항목이 없습니다</div></div>`;
    return;
  }
  const typeIcon = { note:'📝', url:'🔗', image:'🖼', video:'🎬', file:'📄' };
  const typeClass= { note:'arc-type-note', url:'arc-type-url', image:'arc-type-image', video:'arc-type-video', file:'arc-type-file' };
  arcGrid.innerHTML = items.map(item=>{
    const ts = item.createdAt?.toDate ? item.createdAt.toDate().toLocaleString('ko-KR',{month:'short',day:'numeric'}) : '';
    let preview = '';
    if(item.type==='image' && item.url) preview = `<div class="arc-item-preview"><img src="${item.url}" alt="${escHtml(item.title)}" loading="lazy"></div>`;
    else if(item.content) preview = `<div class="arc-item-preview">${escHtml(item.content.slice(0,120))}${item.content.length>120?'...':''}</div>`;
    return `
      <div class="arc-item">
        <div class="arc-item-header">
          <div class="arc-type-icon ${typeClass[item.type]||'arc-type-note'}">${typeIcon[item.type]||'📝'}</div>
          <div class="arc-item-info">
            <div class="arc-item-title">${escHtml(item.title)}</div>
            <div class="arc-item-meta">${ts} · ${item.aiTag||item.type}</div>
          </div>
          ${item.aiTag?`<div class="arc-ai-tag">🤖 ${escHtml(item.aiTag)}</div>`:''}
        </div>
        ${preview}
        <div class="arc-item-actions">
          ${item.type==='url'?`<button class="arc-action-btn" onclick="window.open('${item.content}','_blank')">열기</button>`:''}
          <button class="arc-action-btn" onclick="arcToToday('${item.id}')">Today↗</button>
          <button class="arc-action-btn" style="color:#e74c3c" onclick="arcDel('${item.id}')">삭제</button>
        </div>
      </div>`;
  }).join('');
}
arcSearch.addEventListener('input', ()=>renderArcGrid(arcSearch.value));
document.querySelectorAll('.arc-cat-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    document.querySelectorAll('.arc-cat-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    currentArcCat = btn.dataset.cat;
    renderArcGrid(arcSearch.value);
  });
});
window.arcDel = async(id)=>{ await deleteDoc(arcPath(id)); showSaved(); };
window.arcToToday = (id)=>{
  const item = arcItems.find(i=>i.id===id);
  if(item) openMoveSheet(item.id, 'today');
};'''

NEW_ARC_JS = '''// ═══════════════════════════════════════════════════════
// ARCHIVE v2 — 업그레이드 로직
// ═══════════════════════════════════════════════════════
let arcSortMode = 'newest'; // newest | oldest | pinned
let arcCtxTargetId = null;

/* ── 도메인 추출 유틸 ── */
function arcGetDomain(url) {
  try { return new URL(url).hostname.replace(/^www\\./, ''); } catch(e) { return url; }
}
function arcGetFavicon(url) {
  try { const u = new URL(url); return `https://www.google.com/s2/favicons?domain=${u.hostname}&sz=32`; } catch(e) { return ''; }
}
function arcIsUrl(str) {
  return /^https?:\\/\\//i.test(str.trim());
}

/* ── 카운트 배지 업데이트 ── */
function updateArcCounts() {
  const counts = { all: arcItems.length, note:0, url:0, image:0, video:0, file:0, pinned:0 };
  arcItems.forEach(i => {
    if(counts[i.type] !== undefined) counts[i.type]++;
    if(i.pinned) counts.pinned++;
  });
  Object.keys(counts).forEach(k => {
    const el = document.getElementById(`cnt-${k}`);
    if(el) el.textContent = counts[k];
  });
}

/* ── 정렬 ── */
function sortArcItems(items) {
  if(arcSortMode === 'oldest') return [...items].sort((a,b)=>(a.createdAt?.seconds||0)-(b.createdAt?.seconds||0));
  if(arcSortMode === 'pinned') return [...items].sort((a,b)=>(b.pinned?1:0)-(a.pinned?1:0));
  return [...items].sort((a,b)=>(b.createdAt?.seconds||0)-(a.createdAt?.seconds||0));
}

/* ── 렌더 ── */
function renderArcGrid(filter='') {
  const kw = filter.toLowerCase();
  let items;
  if(currentArcCat === 'pinned') {
    items = arcItems.filter(i=>i.pinned);
  } else {
    items = currentArcCat==='all' ? arcItems : arcItems.filter(i=>i.type===currentArcCat);
  }
  if(kw) items = items.filter(i=>(i.title+(i.content||'')).toLowerCase().includes(kw));
  items = sortArcItems(items);
  updateArcCounts();

  if(!items.length) {
    arcGrid.innerHTML = `<div class="arc-empty"><div class="arc-empty-icon">🗂</div><div>아직 저장된 항목이 없습니다</div></div>`;
    return;
  }
  const typeIcon  = { note:'📝', url:'🔗', image:'🖼', video:'🎬', file:'📄' };
  const typeClass = { note:'arc-type-note', url:'arc-type-url', image:'arc-type-image', video:'arc-type-video', file:'arc-type-file' };

  arcGrid.innerHTML = items.map(item=>{
    const ts = item.createdAt?.toDate ? item.createdAt.toDate().toLocaleString('ko-KR',{month:'short',day:'numeric'}) : '';
    const pinnedClass = item.pinned ? ' pinned' : '';
    const pinBadge = item.pinned ? `<div class="arc-pin-badge">⭐</div>` : '';

    let bodyHtml = '';

    if(item.type === 'url' && item.content) {
      // 링크 미리보기 카드
      const domain  = arcGetDomain(item.content);
      const favicon = arcGetFavicon(item.content);
      const safeUrl = escHtml(item.content);
      bodyHtml = `
        <div class="arc-link-card" onclick="haptic.medium(); arcOpenUrl('${escHtml(item.content).replace(/'/g,"\\\\'")}')">
          <div class="arc-link-accent"></div>
          <div class="arc-link-body">
            <div class="arc-link-domain">
              <img class="arc-link-favicon" src="${favicon}" onerror="this.style.display='none'" loading="lazy">
              ${escHtml(domain)}
            </div>
            <div class="arc-link-url">${safeUrl}</div>
          </div>
          <div class="arc-link-open-icon">↗</div>
        </div>`;
    } else if(item.type === 'image' && item.url) {
      bodyHtml = `<div class="arc-item-preview"><img src="${item.url}" alt="${escHtml(item.title)}" loading="lazy"></div>`;
    } else if(item.content) {
      const preview = item.content.slice(0,150);
      bodyHtml = `<div class="arc-item-preview">${escHtml(preview)}${item.content.length>150?'…':''}</div>`;
    }

    const metaTag = item.aiTag ? `<span class="arc-ai-tag">🤖 ${escHtml(item.aiTag)}</span>` : '';

    return `
      <div class="arc-item${pinnedClass}" data-id="${item.id}" oncontextmenu="arcShowCtx(event,'${item.id}'); return false;" ontouchstart="arcTouchStart(event,'${item.id}')" ontouchend="arcTouchEnd(event)">
        ${pinBadge}
        <div class="arc-item-header">
          <div class="arc-type-icon ${typeClass[item.type]||'arc-type-note'}">${typeIcon[item.type]||'📝'}</div>
          <div class="arc-item-info">
            <div class="arc-item-title">${escHtml(item.title)}</div>
            <div class="arc-item-meta">${ts}${metaTag ? ' · ' : ''}${metaTag || escHtml(item.type)}</div>
          </div>
        </div>
        ${bodyHtml}
        <div class="arc-item-actions">
          ${item.type==='url' ? `<button class="arc-action-btn primary" onclick="haptic.medium(); arcOpenUrl('${escHtml(item.content).replace(/'/g,"\\\\'")}')">🔗 열기</button>` : ''}
          <button class="arc-action-btn" onclick="haptic.light(); arcEdit('${item.id}')">✏️ 편집</button>
          <button class="arc-action-btn" onclick="haptic.medium(); arcTogglePin('${item.id}')">${item.pinned ? '★ 핀해제' : '☆ 핀'}</button>
          <button class="arc-action-btn" onclick="haptic.medium(); arcToToday('${item.id}')">📅</button>
          <button class="arc-action-btn danger" onclick="haptic.error(); arcDel('${item.id}')">🗑</button>
        </div>
      </div>`;
  }).join('');
}

/* ── URL 열기 ── */
window.arcOpenUrl = (url) => {
  if(!url) return;
  const u = url.trim();
  if(arcIsUrl(u)) window.open(u, '_blank');
};

/* ── 핀 토글 ── */
window.arcTogglePin = async(id) => {
  const item = arcItems.find(i=>i.id===id);
  if(!item) return;
  await updateDoc(arcPath(id), { pinned: !item.pinned });
  showSaved();
};

/* ── 편집 ── */
window.arcEdit = (id) => {
  const item = arcItems.find(i=>i.id===id);
  if(!item) return;
  document.getElementById('arcOverlayTitle').textContent = '아카이브 편집';
  document.getElementById('arcEditId').value = id;
  document.getElementById('arcType').value = item.type;
  document.getElementById('arcTitle').value = item.title;
  document.getElementById('arcContent').value = item.content || '';
  const isFile = ['image','video','file'].includes(item.type);
  document.getElementById('arcContentField').style.display = isFile ? 'none' : '';
  document.getElementById('arcFileField').style.display = isFile ? '' : 'none';
  document.getElementById('arcOverlay').classList.remove('hidden');
};

/* ── 컨텍스트 메뉴 ── */
let arcLongPressTimer = null;
window.arcTouchStart = (e, id) => {
  arcLongPressTimer = setTimeout(()=>{
    haptic.longpress();
    arcShowCtx(e.touches[0], id);
  }, 550);
};
window.arcTouchEnd = (e) => {
  clearTimeout(arcLongPressTimer);
};
window.arcShowCtx = (e, id) => {
  arcCtxTargetId = id;
  const item = arcItems.find(i=>i.id===id);
  const menu = document.getElementById('arcCtxMenu');
  const overlay = document.getElementById('arcCtxOverlay');
  // 링크 열기 항목 표시 여부
  document.getElementById('arcCtxOpen').style.display = (item && item.type==='url') ? '' : 'none';
  // 핀 텍스트
  document.getElementById('arcCtxPin').textContent = (item && item.pinned) ? '★ 즐겨찾기 해제' : '⭐ 즐겨찾기 추가';
  // 위치
  const x = e.clientX || e.pageX || window.innerWidth/2;
  const y = e.clientY || e.pageY || window.innerHeight/2;
  menu.style.left = Math.min(x, window.innerWidth-200)+'px';
  menu.style.top  = Math.min(y, window.innerHeight-220)+'px';
  menu.classList.remove('hidden');
  overlay.classList.remove('hidden');
};
function closeArcCtx() {
  document.getElementById('arcCtxMenu').classList.add('hidden');
  document.getElementById('arcCtxOverlay').classList.add('hidden');
  arcCtxTargetId = null;
}
document.getElementById('arcCtxOverlay').addEventListener('click', closeArcCtx);
document.getElementById('arcCtxOpen').addEventListener('click', ()=>{
  haptic.medium();
  const item = arcItems.find(i=>i.id===arcCtxTargetId);
  if(item) arcOpenUrl(item.content);
  closeArcCtx();
});
document.getElementById('arcCtxPin').addEventListener('click', ()=>{
  haptic.medium();
  if(arcCtxTargetId) arcTogglePin(arcCtxTargetId);
  closeArcCtx();
});
document.getElementById('arcCtxEdit').addEventListener('click', ()=>{
  haptic.light();
  if(arcCtxTargetId) arcEdit(arcCtxTargetId);
  closeArcCtx();
});
document.getElementById('arcCtxToday').addEventListener('click', ()=>{
  haptic.medium();
  if(arcCtxTargetId) arcToToday(arcCtxTargetId);
  closeArcCtx();
});
document.getElementById('arcCtxDel').addEventListener('click', ()=>{
  haptic.error();
  if(arcCtxTargetId) arcDel(arcCtxTargetId);
  closeArcCtx();
});

/* ── 정렬 버튼 ── */
document.getElementById('arcSortBtn').addEventListener('click', (e)=>{
  haptic.light();
  const existing = document.getElementById('arcSortMenu');
  if(existing) { existing.remove(); return; }
  const menu = document.createElement('div');
  menu.id = 'arcSortMenu';
  menu.className = 'arc-sort-menu';
  const opts = [
    { key:'newest', label:'🕐 최신순' },
    { key:'oldest', label:'🕰 오래된순' },
    { key:'pinned', label:'⭐ 즐겨찾기 우선' },
  ];
  opts.forEach(o=>{
    const el = document.createElement('div');
    el.className = 'arc-sort-item' + (arcSortMode===o.key ? ' active' : '');
    el.textContent = o.label;
    el.addEventListener('click', ()=>{
      haptic.light();
      arcSortMode = o.key;
      menu.remove();
      renderArcGrid(arcSearch.value);
    });
    menu.appendChild(el);
  });
  document.getElementById('pane-archive').style.position = 'relative';
  document.getElementById('pane-archive').appendChild(menu);
  // 외부 클릭 닫기
  setTimeout(()=>{
    document.addEventListener('click', function handler(ev){
      if(!menu.contains(ev.target)) { menu.remove(); document.removeEventListener('click', handler); }
    });
  }, 50);
});

arcSearch.addEventListener('input', ()=>renderArcGrid(arcSearch.value));
document.querySelectorAll('.arc-cat-btn').forEach(btn=>{
  btn.addEventListener('click', ()=>{
    haptic.light();
    document.querySelectorAll('.arc-cat-btn').forEach(b=>b.classList.remove('active'));
    btn.classList.add('active');
    currentArcCat = btn.dataset.cat;
    renderArcGrid(arcSearch.value);
  });
});
window.arcDel = async(id)=>{ if(confirm('삭제하시겠습니까?')) { await deleteDoc(arcPath(id)); showSaved(); } };
window.arcToToday = (id)=>{
  const item = arcItems.find(i=>i.id===id);
  if(item) openMoveSheet(item.id, 'today');
};'''

# ─── 아카이브 저장 로직 업그레이드 ──────────────────────────────────────────
OLD_ARC_SAVE = '''document.getElementById('arcSave').addEventListener('click', async()=>{ haptic.success();
  const type    = document.getElementById('arcType').value;
  const title   = document.getElementById('arcTitle').value.trim();
  const content = document.getElementById('arcContent').value.trim();
  const file    = document.getElementById('arcFile').files[0];
  if(!title) return;
  let url = '', aiTag = '';
  // AI classify
  if(openAiKey) {
    try {
      const r = await fetch('https://api.openai.com/v1/chat/completions', {
        method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${openAiKey}`},
        body: JSON.stringify({ model:'gpt-4o-mini', max_tokens:20,
          messages:[{role:'user',content:`다음 항목을 한 단어 카테고리로 분류해줘 (예: 업무, 개인, 건강, 재정, 학습, 여행, 쇼핑): "${title} ${content.slice(0,100)}"`}]
        })
      });
      const j = await r.json();
      aiTag = j.choices?.[0]?.message?.content?.trim().slice(0,10)||'';
    } catch(e) {}
  }
  // File upload
  if(file && ['image','video','file'].includes(type)) {
    try {
      const sRef = storageRef(storage, `users/${uid()}/archive/${Date.now()}_${file.name}`);
      await uploadBytes(sRef, file);
      url = await getDownloadURL(sRef);
    } catch(e) { url=''; }
  }
  await addDoc(arcCol(), { type, title, content, url, aiTag, createdAt: serverTimestamp() });
  document.getElementById('arcOverlay').classList.add('hidden');
  showSaved();
});'''

NEW_ARC_SAVE = '''document.getElementById('arcSave').addEventListener('click', async()=>{ haptic.success();
  let type    = document.getElementById('arcType').value;
  const title   = document.getElementById('arcTitle').value.trim();
  let content = document.getElementById('arcContent').value.trim();
  const file    = document.getElementById('arcFile').files[0];
  const editId  = document.getElementById('arcEditId').value;
  if(!title) { alert('제목을 입력해주세요'); return; }
  // URL 자동 감지
  if(arcIsUrl(content) && type === 'note') type = 'url';
  let url = '', aiTag = '';
  // AI classify
  if(openAiKey) {
    try {
      const r = await fetch('https://api.openai.com/v1/chat/completions', {
        method:'POST', headers:{'Content-Type':'application/json','Authorization':`Bearer ${openAiKey}`},
        body: JSON.stringify({ model:'gpt-4o-mini', max_tokens:20,
          messages:[{role:'user',content:`다음 항목을 한 단어 카테고리로 분류해줘 (예: 업무, 개인, 건강, 재정, 학습, 여행, 쇼핑): "${title} ${content.slice(0,100)}"`}]
        })
      });
      const j = await r.json();
      aiTag = j.choices?.[0]?.message?.content?.trim().slice(0,10)||'';
    } catch(e) {}
  }
  // File upload
  if(file && ['image','video','file'].includes(type)) {
    try {
      const sRef = storageRef(storage, `users/${uid()}/archive/${Date.now()}_${file.name}`);
      await uploadBytes(sRef, file);
      url = await getDownloadURL(sRef);
    } catch(e) { url=''; }
  }
  if(editId) {
    // 편집 모드
    await updateDoc(arcPath(editId), { type, title, content, aiTag, updatedAt: serverTimestamp() });
  } else {
    // 신규 저장
    await addDoc(arcCol(), { type, title, content, url, aiTag, pinned: false, createdAt: serverTimestamp() });
  }
  document.getElementById('arcEditId').value = '';
  document.getElementById('arcOverlayTitle').textContent = '아카이브에 추가';
  document.getElementById('arcOverlay').classList.add('hidden');
  showSaved();
});'''

# ─── 아카이브 업로드 버튼 초기화 로직 업그레이드 ─────────────────────────────
OLD_ARC_UPLOAD_BTN = '''document.getElementById('arcUploadBtn').addEventListener('click', ()=>{
  document.getElementById('arcType').value = 'note';
  document.getElementById('arcTitle').value = '';
  document.getElementById('arcContent').value = '';
  document.getElementById('arcContentField').style.display = '';
  document.getElementById('arcFileField').style.display = 'none';
  document.getElementById('arcOverlay').classList.remove('hidden');
});'''

NEW_ARC_UPLOAD_BTN = '''document.getElementById('arcUploadBtn').addEventListener('click', ()=>{
  haptic.medium();
  document.getElementById('arcOverlayTitle').textContent = '아카이브에 추가';
  document.getElementById('arcEditId').value = '';
  document.getElementById('arcType').value = 'note';
  document.getElementById('arcTitle').value = '';
  document.getElementById('arcContent').value = '';
  document.getElementById('arcContentField').style.display = '';
  document.getElementById('arcFileField').style.display = 'none';
  document.getElementById('arcOverlay').classList.remove('hidden');
});
// URL 자동 감지 (내용 입력 시)
document.getElementById('arcContent').addEventListener('input', ()=>{
  const val = document.getElementById('arcContent').value.trim();
  if(arcIsUrl(val)) {
    document.getElementById('arcType').value = 'url';
    // 제목이 비어있으면 도메인으로 자동 채우기
    if(!document.getElementById('arcTitle').value.trim()) {
      document.getElementById('arcTitle').value = arcGetDomain(val);
    }
  }
});'''

# ─── CSS 교체 타겟 ────────────────────────────────────────────────────────────
OLD_ARC_CSS_BLOCK = '''.arc-header {
  padding: 16px 16px 8px;
  display: flex; align-items: center; gap: 10px;
}
.arc-search {
  flex: 1; padding: 10px 14px;
  background: var(--surface); border: 1.5px solid var(--border-mid);
  border-radius: 12px; font-size: 14px; color: var(--text);
  font-family: var(--font); outline: none;
}
.arc-search::placeholder { color: var(--text3); }
.arc-upload-btn {
  width: 40px; height: 40px; border-radius: 12px;
  background: var(--hdr-bg); color: var(--hdr-text);
  border: none; font-size: 18px; cursor: pointer;
  display: flex; align-items: center; justify-content: center;
}
.arc-cats {
  display: flex; gap: 8px; padding: 0 16px 12px;
  overflow-x: auto; -webkit-overflow-scrolling: touch;
}
.arc-cat-btn {
  padding: 6px 14px; border-radius: 20px; font-size: 12px; font-weight: 600;
  border: 1.5px solid var(--border-mid); background: var(--surface);
  color: var(--text2); cursor: pointer; white-space: nowrap;
}
.arc-cat-btn.active {
  background: var(--hdr-bg); color: var(--hdr-text); border-color: var(--hdr-bg);
}
.arc-grid { padding: 0 16px; }
.arc-item {
  background: var(--surface); border-radius: 14px;
  border: 1.5px solid var(--border-mid);
  margin-bottom: 12px; overflow: hidden;
  box-shadow: var(--shadow);
}
.arc-item-header {
  display: flex; align-items: center; gap: 10px;
  padding: 12px 14px;
}
.arc-type-icon {
  width: 36px; height: 36px; border-radius: 10px;
  display: flex; align-items: center; justify-content: center;
  font-size: 18px; flex-shrink: 0;
}
.arc-type-note   { background: #fff3e0; }
.arc-type-url    { background: #e3f2fd; }
.arc-type-image  { background: #fce4ec; }
.arc-type-video  { background: #f3e5f5; }
.arc-type-file   { background: #e8f5e9; }
.arc-item-info { flex: 1; min-width: 0; }
.arc-item-title {
  font-size: 14px; font-weight: 600; color: var(--text);
  white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
}
.arc-item-meta { font-size: 11px; color: var(--text3); margin-top: 2px; }
.arc-ai-tag {
  font-size: 10px; padding: 3px 8px; border-radius: 6px;
  background: rgba(108,99,255,0.1); color: var(--accent);
  font-weight: 700; flex-shrink: 0;
}
.arc-item-preview {
  padding: 0 14px 12px; font-size: 13px; color: var(--text2);
  line-height: 1.5;
}
.arc-item-preview img {
  width: 100%; border-radius: 8px; max-height: 160px; object-fit: cover;
}
.arc-item-actions {
  display: flex; border-top: 1px solid var(--line);
}
.arc-action-btn {
  flex: 1; padding: 10px; border: none; background: transparent;
  font-size: 12px; font-weight: 600; color: var(--text2); cursor: pointer;
  border-right: 1px solid var(--line);
}
.arc-action-btn:last-child { border-right: none; }
.arc-empty { text-align: center; padding: 60px 20px; color: var(--text3); }
.arc-empty-icon { font-size: 48px; margin-bottom: 12px; }'''

FILES = [
  '/home/ubuntu/braindump/galaxy.html',
  '/home/ubuntu/braindump/iphone.html',
  '/home/ubuntu/braindump/index.html',
]

def patch_file(fpath):
  with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

  applied = 0
  errors = []

  def replace_once(old, new, label):
    nonlocal content, applied
    if old in content:
      if new in content:
        print(f"  [=] {label}: 이미 적용됨, skip")
        return
      content = content.replace(old, new, 1)
      applied += 1
      print(f"  [+] {label}: 적용")
    else:
      errors.append(label)
      print(f"  [!] {label}: 원본 없음 (skip)")

  # 1. CSS 교체
  replace_once(OLD_ARC_CSS_BLOCK, NEW_ARC_CSS, 'CSS 업그레이드')

  # 2. HTML 탭 패널 교체
  replace_once(OLD_ARC_PANE, NEW_ARC_PANE, 'HTML 탭 패널')

  # 3. 오버레이 교체
  replace_once(OLD_ARC_OVERLAY, NEW_ARC_OVERLAY, 'HTML 오버레이')

  # 4. JS renderArcGrid 교체
  replace_once(OLD_ARC_JS, NEW_ARC_JS, 'JS renderArcGrid')

  # 5. JS 저장 로직 교체
  replace_once(OLD_ARC_SAVE, NEW_ARC_SAVE, 'JS 저장 로직')

  # 6. JS 업로드 버튼 교체
  replace_once(OLD_ARC_UPLOAD_BTN, NEW_ARC_UPLOAD_BTN, 'JS 업로드 버튼')

  with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)

  print(f"  → 총 {applied}개 패치 적용, 오류: {errors}")
  return applied

for fpath in FILES:
  fname = fpath.split('/')[-1]
  print(f"\n=== {fname} ===")
  patch_file(fpath)

print("\n완료!")
