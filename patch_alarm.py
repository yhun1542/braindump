#!/usr/bin/env python3
"""
알림 기능 전체 구현 패치 스크립트
- 스케줄 이벤트 시트에 알림 항목 UI 추가
- 알림 선택 바텀시트 (삭제/이벤트당일자정/오전9시/1일전/2일전/1주일전/사용자화)
- 드럼롤 피커 (사용자화)
- Web Push Notification 실제 발송
- Firestore alarm 필드 저장/로드
"""
import re

ALARM_CSS = """
/* ── ALARM FEATURE ── */
.alarm-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 14px 0;
  border-bottom: 1px solid var(--border, #e8e8e8);
  cursor: pointer;
  user-select: none;
}
.alarm-row:active { opacity: 0.7; }
.alarm-label { font-size: 15px; color: var(--text, #1a1a1a); }
.alarm-value { font-size: 14px; color: var(--accent, #6c63ff); font-weight: 500; }
.alarm-arrow { font-size: 12px; color: #999; margin-left: 4px; }

/* 알림 선택 바텀시트 */
.alarm-sheet-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  z-index: 3000; display: flex; align-items: flex-end;
  opacity: 0; pointer-events: none;
  transition: opacity 0.25s;
}
.alarm-sheet-overlay.open { opacity: 1; pointer-events: all; }
.alarm-sheet-box {
  width: 100%; background: #fff; border-radius: 20px 20px 0 0;
  padding: 0 0 env(safe-area-inset-bottom, 16px);
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);
}
.alarm-sheet-overlay.open .alarm-sheet-box { transform: translateY(0); }
.alarm-sheet-handle {
  width: 40px; height: 4px; background: #ddd; border-radius: 2px;
  margin: 12px auto 4px;
}
.alarm-sheet-title {
  font-size: 18px; font-weight: 700; color: #1a1a1a;
  padding: 12px 20px 8px;
}
.alarm-option {
  display: block; width: 100%; text-align: left;
  padding: 16px 20px; font-size: 16px; color: #1a1a1a;
  background: none; border: none; cursor: pointer;
  border-bottom: 1px solid #f0f0f0;
  transition: background 0.15s;
}
.alarm-option:last-child { border-bottom: none; }
.alarm-option:active { background: #f5f5f5; }
.alarm-option.selected { color: var(--accent, #6c63ff); font-weight: 600; }
.alarm-option.delete-opt { color: #e53935; }

/* 드럼롤 피커 */
.drum-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.45);
  z-index: 3100; display: flex; align-items: flex-end;
  opacity: 0; pointer-events: none;
  transition: opacity 0.25s;
}
.drum-overlay.open { opacity: 1; pointer-events: all; }
.drum-box {
  width: 100%; background: #fff; border-radius: 20px 20px 0 0;
  padding-bottom: env(safe-area-inset-bottom, 16px);
  transform: translateY(100%);
  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);
}
.drum-overlay.open .drum-box { transform: translateY(0); }
.drum-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 20px 8px;
}
.drum-title { font-size: 18px; font-weight: 700; color: #1a1a1a; }
.drum-summary { font-size: 14px; color: var(--accent, #6c63ff); font-weight: 600; }
.drum-pickers {
  display: flex; justify-content: center; gap: 0;
  padding: 0 16px 8px;
}
.drum-col {
  flex: 1; position: relative; height: 180px; overflow: hidden;
  cursor: ns-resize;
}
.drum-col::before, .drum-col::after {
  content: ''; position: absolute; left: 0; right: 0; height: 60px;
  z-index: 2; pointer-events: none;
}
.drum-col::before {
  top: 0;
  background: linear-gradient(to bottom, rgba(255,255,255,0.95), rgba(255,255,255,0));
}
.drum-col::after {
  bottom: 0;
  background: linear-gradient(to top, rgba(255,255,255,0.95), rgba(255,255,255,0));
}
.drum-selector {
  position: absolute; left: 4px; right: 4px; top: 60px; height: 60px;
  border-top: 2px solid var(--accent, #6c63ff);
  border-bottom: 2px solid var(--accent, #6c63ff);
  border-radius: 4px; pointer-events: none; z-index: 1;
}
.drum-list {
  position: absolute; top: 0; left: 0; right: 0;
  transition: transform 0.15s ease-out;
}
.drum-item {
  height: 60px; display: flex; align-items: center; justify-content: center;
  font-size: 18px; font-weight: 500; color: #bbb;
  transition: color 0.15s, font-size 0.15s;
  user-select: none;
}
.drum-item.active { color: #1a1a1a; font-size: 20px; font-weight: 700; }
.drum-sep {
  display: flex; align-items: center; justify-content: center;
  font-size: 20px; font-weight: 700; color: #1a1a1a;
  padding-top: 60px; /* align with center */
  min-width: 16px;
}
.drum-btns {
  display: flex; justify-content: space-between;
  padding: 12px 20px 8px;
  border-top: 1px solid #f0f0f0;
}
.drum-cancel-btn {
  font-size: 16px; color: #666; background: none; border: none;
  cursor: pointer; padding: 8px 16px;
}
.drum-confirm-btn {
  font-size: 16px; color: var(--accent, #6c63ff); font-weight: 700;
  background: none; border: none; cursor: pointer; padding: 8px 16px;
}
"""

ALARM_HTML_SHEET = """    <div class="sheet-field alarm-row" id="alarmRow" onclick="openAlarmSheet()">
      <span class="alarm-label">알림</span>
      <span style="display:flex;align-items:center;gap:2px">
        <span class="alarm-value" id="alarmValueText">없음</span>
        <span class="alarm-arrow">›</span>
      </span>
    </div>"""

ALARM_BOTTOM_SHEETS = """
<!-- 알림 선택 바텀시트 -->
<div class="alarm-sheet-overlay" id="alarmSheetOverlay">
  <div class="alarm-sheet-box">
    <div class="alarm-sheet-handle"></div>
    <div class="alarm-sheet-title">알림</div>
    <button class="alarm-option delete-opt" data-alarm="none">삭제</button>
    <button class="alarm-option" data-alarm="day0_midnight">이벤트 당일(자정)</button>
    <button class="alarm-option" data-alarm="day0_9am">이벤트 당일(오전 9시)</button>
    <button class="alarm-option" data-alarm="day1_9am">1일 전(오전 9시)</button>
    <button class="alarm-option" data-alarm="day2_9am">2일 전(오전 9시)</button>
    <button class="alarm-option" data-alarm="week1_9am">1주일 전(오전 9시)</button>
    <button class="alarm-option" data-alarm="custom">사용자화</button>
  </div>
</div>

<!-- 드럼롤 피커 (사용자화) -->
<div class="drum-overlay" id="drumOverlay">
  <div class="drum-box">
    <div class="drum-header">
      <span class="drum-title">사용자화</span>
      <span class="drum-summary" id="drumSummary">당일 오전 9시 00분</span>
    </div>
    <div class="drum-pickers">
      <!-- 기준일 -->
      <div class="drum-col" id="drumColDay">
        <div class="drum-selector"></div>
        <div class="drum-list" id="drumListDay"></div>
      </div>
      <!-- 오전/오후 -->
      <div class="drum-col" id="drumColAmpm" style="max-width:80px">
        <div class="drum-selector"></div>
        <div class="drum-list" id="drumListAmpm"></div>
      </div>
      <!-- 시 -->
      <div class="drum-col" id="drumColHour" style="max-width:70px">
        <div class="drum-selector"></div>
        <div class="drum-list" id="drumListHour"></div>
      </div>
      <div class="drum-sep">:</div>
      <!-- 분 -->
      <div class="drum-col" id="drumColMin" style="max-width:70px">
        <div class="drum-selector"></div>
        <div class="drum-list" id="drumListMin"></div>
      </div>
    </div>
    <div class="drum-btns">
      <button class="drum-cancel-btn" id="drumCancelBtn">취소</button>
      <button class="drum-confirm-btn" id="drumConfirmBtn">확인</button>
    </div>
  </div>
</div>
"""

ALARM_JS = """
/* ══════════════════════════════════════════
   ALARM FEATURE
   ══════════════════════════════════════════ */
let selectedAlarm = 'none'; // 'none'|'day0_midnight'|'day0_9am'|'day1_9am'|'day2_9am'|'week1_9am'|{dayOffset,ampm,h,m}

const ALARM_LABELS = {
  none:          '없음',
  day0_midnight: '이벤트 당일(자정)',
  day0_9am:      '이벤트 당일(오전 9시)',
  day1_9am:      '1일 전(오전 9시)',
  day2_9am:      '2일 전(오전 9시)',
  week1_9am:     '1주일 전(오전 9시)',
};

function alarmLabel(alarm) {
  if (!alarm || alarm === 'none') return '없음';
  if (typeof alarm === 'string') return ALARM_LABELS[alarm] || '없음';
  // custom object
  const { dayOffset, ampm, h, m } = alarm;
  const dayStr = dayOffset === 0 ? '당일' : `${dayOffset}일 전`;
  const mm = String(m).padStart(2,'0');
  return `사용자화 (${dayStr} ${ampm} ${h}시 ${mm}분)`;
}

function setAlarmUI(alarm) {
  selectedAlarm = alarm || 'none';
  document.getElementById('alarmValueText').textContent = alarmLabel(selectedAlarm);
  // highlight selected option
  document.querySelectorAll('.alarm-option').forEach(btn => {
    const v = btn.dataset.alarm;
    btn.classList.toggle('selected',
      v === 'custom' ? (typeof selectedAlarm === 'object') :
      v === selectedAlarm
    );
  });
}

function openAlarmSheet() {
  const ov = document.getElementById('alarmSheetOverlay');
  ov.classList.add('open');
}
function closeAlarmSheet() {
  document.getElementById('alarmSheetOverlay').classList.remove('open');
}

// 알림 옵션 선택
document.querySelectorAll('.alarm-option').forEach(btn => {
  btn.addEventListener('click', () => {
    const v = btn.dataset.alarm;
    closeAlarmSheet();
    if (v === 'custom') {
      openDrumPicker();
    } else {
      setAlarmUI(v);
    }
  });
});
document.getElementById('alarmSheetOverlay').addEventListener('click', e => {
  if (e.target === e.currentTarget) closeAlarmSheet();
});

/* ── 드럼롤 피커 ── */
const DRUM_DAYS  = ['당일','1일 전','2일 전','3일 전','4일 전','5일 전','6일 전','1주일 전'];
const DRUM_AMPM  = ['오전','오후'];
const DRUM_HOURS = Array.from({length:12}, (_,i)=>String(i+1));
const DRUM_MINS  = Array.from({length:60}, (_,i)=>String(i).padStart(2,'0'));

let drumState = { dayIdx:0, ampmIdx:0, hourIdx:8, minIdx:0 }; // default: 당일 오전 9시 00분

function buildDrumList(listEl, items, selectedIdx) {
  listEl.innerHTML = '';
  // padding items top/bottom
  for(let i=0;i<3;i++) {
    const pad = document.createElement('div');
    pad.className = 'drum-item';
    pad.style.visibility = 'hidden';
    pad.textContent = '-';
    listEl.appendChild(pad);
  }
  items.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'drum-item' + (idx === selectedIdx ? ' active' : '');
    div.textContent = item;
    listEl.appendChild(div);
  });
  for(let i=0;i<3;i++) {
    const pad = document.createElement('div');
    pad.className = 'drum-item';
    pad.style.visibility = 'hidden';
    pad.textContent = '-';
    listEl.appendChild(pad);
  }
  scrollDrumTo(listEl, selectedIdx, false);
}

function scrollDrumTo(listEl, idx, animate=true) {
  const offset = -(idx * 60); // each item 60px
  listEl.style.transition = animate ? 'transform 0.15s ease-out' : 'none';
  listEl.style.transform = `translateY(${offset}px)`;
  // update active
  listEl.querySelectorAll('.drum-item').forEach((el, i) => {
    const realIdx = i - 3; // subtract padding
    el.classList.toggle('active', realIdx === idx);
  });
}

function updateDrumSummary() {
  const day  = DRUM_DAYS[drumState.dayIdx];
  const ampm = DRUM_AMPM[drumState.ampmIdx];
  const h    = DRUM_HOURS[drumState.hourIdx];
  const m    = DRUM_MINS[drumState.minIdx];
  document.getElementById('drumSummary').textContent = `${day} ${ampm} ${h}시 ${m}분`;
}

function attachDrumTouch(colEl, listEl, items, stateKey) {
  let startY = 0, startIdx = 0, isDragging = false;
  const onStart = e => {
    startY = (e.touches ? e.touches[0].clientY : e.clientY);
    startIdx = drumState[stateKey];
    isDragging = true;
  };
  const onMove = e => {
    if (!isDragging) return;
    e.preventDefault();
    const y = (e.touches ? e.touches[0].clientY : e.clientY);
    const delta = Math.round((startY - y) / 60);
    let newIdx = Math.max(0, Math.min(items.length-1, startIdx + delta));
    if (newIdx !== drumState[stateKey]) {
      drumState[stateKey] = newIdx;
      scrollDrumTo(listEl, newIdx, true);
      updateDrumSummary();
    }
  };
  const onEnd = () => { isDragging = false; };
  colEl.addEventListener('touchstart', onStart, {passive:true});
  colEl.addEventListener('touchmove',  onMove,  {passive:false});
  colEl.addEventListener('touchend',   onEnd);
  colEl.addEventListener('mousedown',  onStart);
  window.addEventListener('mousemove', onMove);
  window.addEventListener('mouseup',   onEnd);
}

function openDrumPicker() {
  // init from current selectedAlarm if custom
  if (typeof selectedAlarm === 'object' && selectedAlarm !== null) {
    const { dayOffset, ampm, h, m } = selectedAlarm;
    drumState.dayIdx  = Math.min(dayOffset, DRUM_DAYS.length-1);
    drumState.ampmIdx = ampm === '오후' ? 1 : 0;
    drumState.hourIdx = Math.max(0, Math.min(11, h-1));
    drumState.minIdx  = Math.max(0, Math.min(59, m));
  } else {
    drumState = { dayIdx:0, ampmIdx:0, hourIdx:8, minIdx:0 };
  }
  buildDrumList(document.getElementById('drumListDay'),  DRUM_DAYS,  drumState.dayIdx);
  buildDrumList(document.getElementById('drumListAmpm'), DRUM_AMPM,  drumState.ampmIdx);
  buildDrumList(document.getElementById('drumListHour'), DRUM_HOURS, drumState.hourIdx);
  buildDrumList(document.getElementById('drumListMin'),  DRUM_MINS,  drumState.minIdx);
  updateDrumSummary();

  attachDrumTouch(document.getElementById('drumColDay'),  document.getElementById('drumListDay'),  DRUM_DAYS,  'dayIdx');
  attachDrumTouch(document.getElementById('drumColAmpm'), document.getElementById('drumListAmpm'), DRUM_AMPM,  'ampmIdx');
  attachDrumTouch(document.getElementById('drumColHour'), document.getElementById('drumListHour'), DRUM_HOURS, 'hourIdx');
  attachDrumTouch(document.getElementById('drumColMin'),  document.getElementById('drumListMin'),  DRUM_MINS,  'minIdx');

  document.getElementById('drumOverlay').classList.add('open');
}

document.getElementById('drumCancelBtn').addEventListener('click', () => {
  document.getElementById('drumOverlay').classList.remove('open');
});
document.getElementById('drumConfirmBtn').addEventListener('click', () => {
  const customAlarm = {
    dayOffset: drumState.dayIdx,
    ampm:  DRUM_AMPM[drumState.ampmIdx],
    h:     parseInt(DRUM_HOURS[drumState.hourIdx]),
    m:     parseInt(DRUM_MINS[drumState.minIdx]),
  };
  setAlarmUI(customAlarm);
  document.getElementById('drumOverlay').classList.remove('open');
});

/* ── Web Push Notification ── */
async function requestNotificationPermission() {
  if (!('Notification' in window)) return false;
  if (Notification.permission === 'granted') return true;
  if (Notification.permission === 'denied') return false;
  const perm = await Notification.requestPermission();
  return perm === 'granted';
}

function calcAlarmTime(eventDate, alarm) {
  if (!eventDate || !alarm || alarm === 'none') return null;
  const [y,mo,d] = eventDate.split('-').map(Number);
  let base = new Date(y, mo-1, d);
  let offsetDays = 0, hour = 9, min = 0;

  if (alarm === 'day0_midnight') { offsetDays=0; hour=0; min=0; }
  else if (alarm === 'day0_9am') { offsetDays=0; hour=9; min=0; }
  else if (alarm === 'day1_9am') { offsetDays=1; hour=9; min=0; }
  else if (alarm === 'day2_9am') { offsetDays=2; hour=9; min=0; }
  else if (alarm === 'week1_9am'){ offsetDays=7; hour=9; min=0; }
  else if (typeof alarm === 'object') {
    offsetDays = alarm.dayOffset || 0;
    hour = alarm.h || 9;
    min  = alarm.m || 0;
    if (alarm.ampm === '오후' && hour < 12) hour += 12;
    if (alarm.ampm === '오전' && hour === 12) hour = 0;
  }
  const alarmDate = new Date(base);
  alarmDate.setDate(alarmDate.getDate() - offsetDays);
  alarmDate.setHours(hour, min, 0, 0);
  return alarmDate;
}

function scheduleNotification(title, eventDate, alarm) {
  if (!alarm || alarm === 'none') return;
  const alarmTime = calcAlarmTime(eventDate, alarm);
  if (!alarmTime) return;
  const now = Date.now();
  const delay = alarmTime.getTime() - now;
  if (delay <= 0) return; // 이미 지난 시간
  setTimeout(async () => {
    const granted = await requestNotificationPermission();
    if (!granted) return;
    new Notification('📅 ' + title, {
      body: `일정 알림: ${alarmLabel(alarm)}`,
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-192.png',
      tag: 'event-' + title,
    });
  }, delay);
}

/* ── openEventSheet 알림 초기화 연동 ── */
const _origOpenEventSheet = openEventSheet;
// patch: openEventSheet 내부에서 alarm 값 로드
"""

ALARM_SAVE_PATCH = """
  // alarm 저장
  const alarmData = selectedAlarm === 'none' ? null : selectedAlarm;
  const data = {
    title,
    date:     document.getElementById('eventDate').value,
    time:     document.getElementById('eventTime').value,
    note:     document.getElementById('eventNote').value,
    colorIdx: selectedColorIdx,
    alarm:    alarmData,
    updatedAt: serverTimestamp()
  };"""

ALARM_LOAD_PATCH = """      document.getElementById('eventTitle').value = ev.title||'';
      document.getElementById('eventDate').value  = ev.date||'';
      document.getElementById('eventTime').value  = ev.time||'';
      document.getElementById('eventNote').value  = ev.note||'';
      selectedColorIdx = ev.colorIdx||0;
      setAlarmUI(ev.alarm || 'none');"""

ALARM_RESET_PATCH = """    document.getElementById('eventTitle').value = '';
    document.getElementById('eventDate').value  = defaultDate||dateStr(new Date());
    document.getElementById('eventTime').value  = '';
    document.getElementById('eventNote').value  = '';
    setAlarmUI('none');"""

ALARM_AFTER_SAVE = """  // 알림 스케줄링
  const savedTitle = document.getElementById('eventTitle').value.trim();
  const savedDate  = document.getElementById('eventDate').value;
  if (selectedAlarm !== 'none') {
    requestNotificationPermission().then(granted => {
      if (granted) scheduleNotification(savedTitle, savedDate, selectedAlarm);
    });
  }
  document.getElementById('eventOverlay').classList.add('hidden');"""


def patch_file(fpath):
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    changed = []

    # 1. CSS 추가 (</style> 바로 앞)
    if '/* ── ALARM FEATURE ── */' not in html:
        html = html.replace('</style>', ALARM_CSS + '\n</style>', 1)
        changed.append('CSS 추가')

    # 2. 이벤트 시트에 알림 항목 추가 (색상 필드 바로 앞)
    if 'id="alarmRow"' not in html:
        html = html.replace(
            '<div class="sheet-field">\n      <div class="sheet-label">색상</div>',
            ALARM_HTML_SHEET + '\n    <div class="sheet-field">\n      <div class="sheet-label">색상</div>'
        )
        changed.append('알림 행 HTML 추가')

    # 3. 바텀시트 + 드럼롤 HTML 추가 (<!-- BrainDump Move Sheet --> 바로 앞)
    if 'id="alarmSheetOverlay"' not in html:
        html = html.replace(
            '<!-- BrainDump Move Sheet -->',
            ALARM_BOTTOM_SHEETS + '\n<!-- BrainDump Move Sheet -->'
        )
        changed.append('알림 바텀시트 + 드럼롤 HTML 추가')

    # 4. JS 추가 (</script> 바로 앞 마지막)
    if 'ALARM FEATURE' not in html:
        # 마지막 </script> 앞에 삽입
        html = html[::-1].replace('>tpircs/<'.encode('utf-8').decode('utf-8')[::-1], (ALARM_JS + '\n</script>')[::-1], 1)[::-1]
        changed.append('알림 JS 추가')

    # 5. eventSave 핸들러에서 alarm 저장 (data 객체에 alarm 추가)
    old_data = """  const data = {
    title,
    date:     document.getElementById('eventDate').value,
    time:     document.getElementById('eventTime').value,
    note:     document.getElementById('eventNote').value,
    colorIdx: selectedColorIdx,
    updatedAt: serverTimestamp()
  };"""
    if old_data in html:
        html = html.replace(old_data, ALARM_SAVE_PATCH)
        changed.append('eventSave alarm 저장 추가')

    # 6. openEventSheet에서 alarm 로드
    old_load = """      document.getElementById('eventTitle').value = ev.title||'';
      document.getElementById('eventDate').value  = ev.date||'';
      document.getElementById('eventTime').value  = ev.time||'';
      document.getElementById('eventNote').value  = ev.note||'';
      selectedColorIdx = ev.colorIdx||0;"""
    if old_load in html and 'setAlarmUI' not in html.split(old_load)[1][:200]:
        html = html.replace(old_load, ALARM_LOAD_PATCH)
        changed.append('openEventSheet alarm 로드 추가')

    # 7. 새 이벤트 시 알림 초기화
    old_reset = """    document.getElementById('eventTitle').value = '';
    document.getElementById('eventDate').value  = defaultDate||dateStr(new Date());
    document.getElementById('eventTime').value  = '';
    document.getElementById('eventNote').value  = '';"""
    if old_reset in html and "setAlarmUI('none')" not in html.split(old_reset)[1][:200]:
        html = html.replace(old_reset, ALARM_RESET_PATCH)
        changed.append('openEventSheet 알림 초기화 추가')

    # 8. eventSave 후 알림 스케줄링 (showSaved() 호출 직전)
    old_close = """  document.getElementById('eventOverlay').classList.add('hidden');
  showSaved();
});
/* ── BRAINDUMP ── */"""
    new_close = """  // 알림 스케줄링
  const savedTitle = document.getElementById('eventTitle').value.trim() || title;
  const savedDate  = document.getElementById('eventDate').value;
  if (selectedAlarm && selectedAlarm !== 'none') {
    requestNotificationPermission().then(granted => {
      if (granted) scheduleNotification(savedTitle, savedDate, selectedAlarm);
    });
  }
  document.getElementById('eventOverlay').classList.add('hidden');
  showSaved();
});
/* ── BRAINDUMP ── */"""
    if old_close in html and 'scheduleNotification' not in html.split(old_close)[0][-500:]:
        html = html.replace(old_close, new_close)
        changed.append('eventSave 알림 스케줄링 추가')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"[{fpath.split('/')[-1]}] 변경: {', '.join(changed) if changed else '변경 없음'}")


for fname in ['galaxy.html', 'iphone.html', 'index.html']:
    patch_file(f'/home/ubuntu/braindump/{fname}')

print("완료!")
