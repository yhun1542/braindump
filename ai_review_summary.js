/**
 * Synapse Brain App v22 - 아카이브 핵심 함수 요약
 * 4-AI 검증용 코드 스니펫
 * 총 파일 크기: 210979 bytes, 4748줄
 */

// === arcFormatDate (L2682) ===
function arcFormatDate(item){
  const d = arcSafeDate(item);
  if(!d || !isFinite(d.getTime())) return '';
  const now = new Date();
  const diffDays = Math.floor((now - d) / 86400000);
  if(diffDays === 0) return '오늘';
  if(diffDays === 1) return '어제';
  if(diffDays <= 6) return `${diffDays}일 전`;
  return d.toLocaleString('ko-KR',{month:'short',day:'numeric'});
}
function arcTokenize(text){
  return [...new Set(
    arcNormalizeText(text).replace(/[^\p{L}\p{N}@#._:/-]+/gu,' ').split(' ').map(s=>s.trim()).filter(v=>v && v.length>=2 && !ARC_STOPWORDS.has(v))
  )];
}
function arcExtractMentions(text){
  const m = String(text||'').match(/@([가-힣\w.-]+)/g) || [];
  return [...new Set(m.map(v=>v.replace('@','')).filter(v=>!ARC_STOPWORDS.has(arcNormalizeText(v))))].slice(0,8);
}
function arcExtractHashTags(text){

// === arcEnrichItem (L2777) ===
function arcEnrichItem(item){
  const title = (item.title || '').trim() || (item.type==='url' ? arcGetDomain(item.content||item.url||'') : '제목 없는 항목');
  const content = item.content || '';
  const mentions = [...new Set([...(item.mentions||[]), ...arcExtractMentions(title+' '+content)])].slice(0,8);
  const tags = [...new Set([...(item.tags||[]), ...arcExtractHashTags(title+' '+content), ...arcGuessTags(title, content, item.type)])].slice(0,8);
  const wikiLinks = [...new Set([...(item.wikiLinks||[]), ...arcExtractWikiLinks(title+' '+content)])].slice(0,8);
  const kind = item.kind || arcGuessKind(title, content, item.type);
  const kindLabel = kind==='meeting' ? '회의' : kind==='idea' ? '아이디어' : '자료';
  const project = item.project || arcGuessProject(title + ' ' + wikiLinks.join(' '), content, tags, mentions);
  const domain = arcGetDomain(item.content||item.url||'');
  const collection = item.collection || arcComputeCollection({type:item.type, kind, title, content, project});
  const summary = item.summary || arcSummarizeFallback(content);
  const searchBlob = arcBuildSearchBlob({ ...item, title, content, summary, project, collection, kindLabel, tags, mentions, domain, wikiLinks });
  return { ...item, title, content, summary, kind, kindLabel, tags, mentions, wikiLinks, project, collection, domain, searchBlob };
}
function arcSearchScore(item, query){
  if(!query) return 1;
  const q = arcNormalizeText(query);
  if(!q) return 1;
  const title = arcNormalizeText(item.title);

// === arcSearchScore (L2792) ===
function arcSearchScore(item, query){
  if(!query) return 1;
  const q = arcNormalizeText(query);
  if(!q) return 1;
  const title = arcNormalizeText(item.title);
  const summary = arcNormalizeText(item.summary);
  const blob = item.searchBlob || arcBuildSearchBlob(item);
  const tokens = arcTokenize(q);
  let score = 0;
  if(title===q) score += 160;
  if(title.startsWith(q)) score += 110;
  if(title.includes(q)) score += 88;
  if(arcNormalizeText(item.project)===q) score += 120;
  if(summary.includes(q)) score += 34;
  if(blob.includes(q)) score += 20;
  tokens.forEach(t=>{
    if(title.includes(t)) score += 24;
    if(summary.includes(t)) score += 11;
    if(blob.includes(t)) score += 7;
    if((item.tags||[]).some(v=>arcNormalizeText(v).includes(t))) score += 14;

// === arcGuessProject (L2744) ===
function arcGuessProject(title, content, tags, mentions){
  const explicit = arcExtractWikiLinks([title, content].join(' '));
  if(explicit.length) return explicit[0].slice(0,28);
  const mentionPriority = (mentions||[]).filter(v=>!['개인','가족','업무','today','archive'].includes(v));
  if(mentionPriority.length) return mentionPriority[0].slice(0,24);
  const tagPriority = (tags||[]).filter(v=>!['링크','자료','회의','아이디어','업무','가족','나중에보기'].includes(v));
  if(tagPriority.length) return tagPriority[0].slice(0,20);
  const words = arcTokenize([title, content].join(' ')).filter(w => w.length >= 2 && !['자료','회의','아이디어','링크','업무','개인','가족','프로젝트'].includes(w));
  return words[0] ? words[0].slice(0,20) : '';
}

// arcInferProject: arcGuessProject의 공개 래퍼 (외부 호출용)
function arcInferProject(item) {
  const title = item.title || '';
  const content = item.content || '';
  const tags = item.tags || [];
  const mentions = item.mentions || [];
  return arcGuessProject(title + ' ' + content, content, tags, mentions);
}
function arcComputeCollection(item){

// === arcInferProject (L2756) ===
function arcInferProject(item) {
  const title = item.title || '';
  const content = item.content || '';
  const tags = item.tags || [];
  const mentions = item.mentions || [];
  return arcGuessProject(title + ' ' + content, content, tags, mentions);
}
function arcComputeCollection(item){
  if(item.kind==='meeting') return '회의';
  if(item.kind==='idea') return '아이디어';
  if(item.type==='url') return '읽을거리';
  if(arcIsPdf(item)) return '문서함';
  if(item.project) return '프로젝트';
  return '자료';
}
function arcBuildSearchBlob(item){
  return arcNormalizeText([
    item.title, item.content, item.summary, item.aiTag, item.project, item.collection, item.kindLabel,
    (item.tags||[]).join(' '), (item.mentions||[]).join(' '), (item.wikiLinks||[]).join(' '), item.domain
  ].join(' '));

// === openArcDashboard (L3451) ===
function openArcDashboard(project) {
  if(!project) return;
  const sheet = document.getElementById('arcDashSheet');
  if(!sheet) return;
  const body = document.getElementById('arcDashBody');
  const enriched = arcItems.map(arcEnrichItem);
  const projItems = sortArcItems(enriched.filter(i=>i.project===project));
  const stats = arcKindStats(projItems);
  const total = projItems.length;
  const recent7 = projItems.filter(i=>Date.now()-arcSafeDate(i)<7*86400000).length;
  const progress = total ? Math.round((stats.material+stats.meeting)/Math.max(total,1)*100) : 0;

  // Build top tags and mentions
  const tagsMap = new Map(), mentMap = new Map();
  projItems.forEach(i=>{
    (i.tags||[]).forEach(t=>tagsMap.set(t,(tagsMap.get(t)||0)+1));
    (i.mentions||[]).forEach(m=>mentMap.set(m,(mentMap.get(m)||0)+1));
  });
  const topTags = [...tagsMap].sort((a,b)=>b[1]-a[1]).slice(0,4);
  const topMents = [...mentMap].sort((a,b)=>b[1]-a[1]).slice(0,4);

// === openMeetingSummary (L3623) ===
async function openMeetingSummary(id) {
  const item = arcItems.map(arcEnrichItem).find(i=>i.id===id);
  if(!item) return;
  const sheet = document.getElementById('arcMeetSheet');
  const body = document.getElementById('arcMeetBody');
  const sub = document.getElementById('arcMeetHeadSub');
  if(!sheet||!body) return;
  sub.textContent = escHtml(item.title);
  body.innerHTML = '<div class="arc-meet-loading"><div class="spin">⏳</div><div>AI 회의 요약 분석 중...</div></div>';
  sheet.classList.remove('hidden');

  let result = null;
  if(openAiKey) {
    try {
      const prompt = `다음 회의 노트를 JSON으로 정리해줘. 키: summary(한 문장 요약), decisions(결정사항 배열, 한국어, 최대5개), actionItems(액션아이템 배열 {text,person}, 최대6개), attendees(언급된 사람 배열, @없이), keyPoints(핵심 포인트 배열, 최대4개).\n제목: ${item.title}\n내용: ${String(item.content||'').slice(0,2000)}`;
      const r = await fetch('https://api.openai.com/v1/chat/completions', {
        method:'POST',
        headers:{'Content-Type':'application/json','Authorization':`Bearer ${openAiKey}`},
        body:JSON.stringify({model:'gpt-4o-mini',max_tokens:400,messages:[{role:'system',content:'JSON만 반환한다.'},{role:'user',content:prompt}]})
      });

// === openQuickConvert (L3741) ===
async function openQuickConvert(id) {
  const item = arcItems.map(arcEnrichItem).find(i=>i.id===id);
  if(!item) return;
  const sheet = document.getElementById('arcConvSheet');
  const body = document.getElementById('arcConvBody');
  if(!sheet||!body) return;
  _convSelectedItems = new Set();
  _convDest = 'today';
  sheet.classList.remove('hidden');

  body.innerHTML = `
    <div class="arc-conv-source">${escHtml((item.summary||item.content||item.title).slice(0,160))}</div>
    <div class="arc-conv-ai-label">⏳ AI가 할 일을 추출 중...</div>
    <div id="arcConvItemList" style="opacity:.4;pointer-events:none"></div>
    <div class="arc-conv-dest-row" id="arcConvDestRow" style="opacity:.4;pointer-events:none">
      <button class="arc-conv-dest-btn active" data-dest="today" onclick="setConvDest('today')">
        <div class="arc-conv-dest-icon">📅</div>
        <div class="arc-conv-dest-label">Today</div>
        <div class="arc-conv-dest-sub">오늘 할 일로</div>
      </button>

// === execConvert (L3828) ===
window.execConvert = async(sourceId) => {
  const listEl = document.getElementById('arcConvItemList');
  if(!listEl) return;
  const allItems = [...listEl.querySelectorAll('.arc-conv-item')].map(el=>el.querySelector('.arc-conv-item-text')?.textContent?.trim()).filter(Boolean);
  const selected = allItems.filter((_,i)=>_convSelectedItems.has(i));
  if(!selected.length) { showSaved('선택된 항목 없음'); return; }

  if(_convDest==='today') {
    const cardId = CARDS[0]?.id;
    if(cardId) { for(const t of selected) await addTask(cardId, t); }
    showSaved(`📅 Today에 ${selected.length}개 추가됨`);
  } else {
    // Schedule: open the event sheet for the first item
    const first = selected[0];
    openEventSheet(null, null);
    setTimeout(()=>{ const titleEl = document.getElementById('eventTitle'); if(titleEl) titleEl.value=first; }, 200);
    // 나머지 항목들은 Today에 자동 추가
    if(selected.length>1) {
      const cardId = CARDS[0]?.id;
      if(cardId) { for(const t of selected.slice(1)) await addTask(cardId, t); }

// === sendMeetActionsToToday (L3720) ===
window.sendMeetActionsToToday = async(actions) => { haptic.medium();
  const items = Array.isArray(actions)?actions:[];
  const selected = items.filter((_,i)=>_meetChecked.has(i));
  const toSend = selected.length ? selected : items.slice(0,3);
  if(!toSend.length) { showSaved(); return; }
  // Use first Today card or fallback
  const cardId = CARDS[0]?.id;
  if(!cardId) { showSaved(); return; }
  for(const a of toSend) {
    const text = typeof a==='string'?a:a.text;
    if(text?.trim()) await addTask(cardId, text.trim());
  }
  document.getElementById('arcMeetSheet')?.classList.add('hidden');
  _meetChecked.clear();
  showSaved('Today에 추가됨 ✓');
};

/* ── Quick Convert (자료→할 일/일정 즉시 변환) ── */
let _convSelectedItems = new Set();
let _convDest = 'today'; // 'today' | 'schedule'

// === arcTogglePin (L3222) ===
window.arcTogglePin = async(id) => { haptic.medium();
  const item = arcItems.find(i=>i.id===id);
  if(!item) return;
  await updateDoc(arcPath(id), { pinned: !item.pinned, updatedAt: serverTimestamp() });
  showSaved();
};
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
// arcEditItem: arcEdit 함수의 별칭 (하위 호환성)

// === arcEdit (L3228) ===
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
// arcEditItem: arcEdit 함수의 별칭 (하위 호환성)
window.arcEditItem = window.arcEdit;

let arcLongPressTimer = null;
window.arcTouchStart = (e, id) => {
  arcLongPressTimer = setTimeout(()=>{
    haptic.longpress();

// === arcOpenUrl (L3217) ===
window.arcOpenUrl = (url) => {
  if(!url) return;
  const u = String(url).trim();
  if(arcIsUrl(u)) window.open(u, '_blank');
};
window.arcTogglePin = async(id) => { haptic.medium();
  const item = arcItems.find(i=>i.id===id);
  if(!item) return;
  await updateDoc(arcPath(id), { pinned: !item.pinned, updatedAt: serverTimestamp() });
  showSaved();
};
window.arcEdit = (id) => {
  const item = arcItems.find(i=>i.id===id);
  if(!item) return;
  document.getElementById('arcOverlayTitle').textContent = '아카이브 편집';
  document.getElementById('arcEditId').value = id;
  document.getElementById('arcType').value = item.type;
  document.getElementById('arcTitle').value = item.title;
  document.getElementById('arcContent').value = item.content || '';
  const isFile = ['image','video','file'].includes(item.type);

// === renderArcGrid (L3154) ===
function renderArcGrid(filter='') {
  const kw = arcNormalizeText(filter);
  let items = arcItems.map(arcEnrichItem);
  if(currentArcCat === 'pinned') items = items.filter(i=>i.pinned);
  else if(currentArcCat !== 'all') items = items.filter(i=>i.type===currentArcCat);
  items = arcApplySmartFilter(items);
  items = arcApplyProjectAndKindFilter(items);
  if(kw) {
    items = items
      .map(i => ({...i, _score: arcSearchScore(i, kw)}))
      .filter(i => i._score > 0)
      .sort((a,b)=>b._score-a._score || (arcSafeDate(b)-arcSafeDate(a)));
  } else {
    items = sortArcItems(items);
  }
  updateArcCounts();
  renderArcHub(arcItems);
  document.querySelectorAll('.arc-smart-btn').forEach(btn=>{
    btn.classList.toggle('active', btn.dataset.smart===currentArcSmartFilter);
  });

// === updateArcCounts (L2842) ===
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
function sortArcItems(items) {
  if(arcSortMode === 'oldest') return [...items].sort((a,b)=>arcSafeDate(a)-arcSafeDate(b));
  if(arcSortMode === 'pinned') return [...items].sort((a,b)=>(b.pinned?1:0)-(a.pinned?1:0) || (arcSafeDate(b)-arcSafeDate(a)));
  return [...items].sort((a,b)=>arcSafeDate(b)-arcSafeDate(a));
}
function arcGetYoutubeThumb(url){
  try{
    const u = new URL(url);
    let id = '';

// === sortArcItems (L2853) ===
function sortArcItems(items) {
  if(arcSortMode === 'oldest') return [...items].sort((a,b)=>arcSafeDate(a)-arcSafeDate(b));
  if(arcSortMode === 'pinned') return [...items].sort((a,b)=>(b.pinned?1:0)-(a.pinned?1:0) || (arcSafeDate(b)-arcSafeDate(a)));
  return [...items].sort((a,b)=>arcSafeDate(b)-arcSafeDate(a));
}
function arcGetYoutubeThumb(url){
  try{
    const u = new URL(url);
    let id = '';
    if(u.hostname.includes('youtu.be')) id = u.pathname.slice(1);
    if(u.hostname.includes('youtube.com')) id = u.searchParams.get('v') || '';
    return id ? `https://i.ytimg.com/vi/${id}/hqdefault.jpg` : '';
  }catch(e){ return ''; }
}
function arcFindRelatedDocs(item){
  const scores = arcItems
    .filter(v => v.id !== item.id)
    .map(v => {
      let score = 0;
      if(item.project && v.project === item.project) score += 6;

// === arcApplySmartFilter (L2825) ===
function arcApplySmartFilter(items){
  const now = Date.now();
  if(currentArcSmartFilter === 'recent7') return items.filter(i => now - arcSafeDate(i).getTime() <= 7*24*60*60*1000);
  if(currentArcSmartFilter === 'meeting') return items.filter(i => i.kind === 'meeting');
  if(currentArcSmartFilter === 'material') return items.filter(i => i.kind === 'material');
  if(currentArcSmartFilter === 'idea') return items.filter(i => i.kind === 'idea');
  if(currentArcSmartFilter === 'pdf') return items.filter(i => arcIsPdf(i));
  if(currentArcSmartFilter === 'ai') return items.filter(i => i.summary || i.aiTag || (i.tags||[]).length);
  return items;
}
function arcApplyProjectAndKindFilter(items){
  return items.filter(i => {
    const okProject = !currentArcProjectFilter || i.project === currentArcProjectFilter;
    const okKind = !currentArcKindFilter || i.kind === currentArcKindFilter;
    return okProject && okKind;
  });
}
function updateArcCounts() {
  const counts = { all: arcItems.length, note:0, url:0, image:0, video:0, file:0, pinned:0 };
  arcItems.forEach(i => {

