#!/usr/bin/env python3
"""알림 JS를 마지막 </script> 바로 앞에 삽입"""

ALARM_JS = """
/* ══════════════════════════════════════════
   ALARM FEATURE - JS
   ══════════════════════════════════════════ */
let selectedAlarm = 'none';

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
  const { dayOffset, ampm, h, m } = alarm;
  const dayStr = dayOffset === 0 ? '당일' : dayOffset + '일 전';
  const mm = String(m).padStart(2,'0');
  return '사용자화 (' + dayStr + ' ' + ampm + ' ' + h + '시 ' + mm + '분)';
}

function setAlarmUI(alarm) {
  selectedAlarm = alarm || 'none';
  const el = document.getElementById('alarmValueText');
  if (el) el.textContent = alarmLabel(selectedAlarm);
  document.querySelectorAll('.alarm-option').forEach(btn => {
    const v = btn.dataset.alarm;
    btn.classList.toggle('selected',
      v === 'custom' ? (typeof selectedAlarm === 'object') : v === selectedAlarm
    );
  });
}

function openAlarmSheet() {
  const ov = document.getElementById('alarmSheetOverlay');
  if (ov) ov.classList.add('open');
}
function closeAlarmSheet() {
  const ov = document.getElementById('alarmSheetOverlay');
  if (ov) ov.classList.remove('open');
}

document.addEventListener('DOMContentLoaded', function() {
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
  const alarmOv = document.getElementById('alarmSheetOverlay');
  if (alarmOv) {
    alarmOv.addEventListener('click', e => {
      if (e.target === e.currentTarget) closeAlarmSheet();
    });
  }

  // 드럼롤 버튼
  const drumCancelBtn = document.getElementById('drumCancelBtn');
  const drumConfirmBtn = document.getElementById('drumConfirmBtn');
  if (drumCancelBtn) drumCancelBtn.addEventListener('click', () => {
    document.getElementById('drumOverlay').classList.remove('open');
  });
  if (drumConfirmBtn) drumConfirmBtn.addEventListener('click', () => {
    const customAlarm = {
      dayOffset: drumState.dayIdx,
      ampm:  DRUM_AMPM[drumState.ampmIdx],
      h:     parseInt(DRUM_HOURS[drumState.hourIdx]),
      m:     parseInt(DRUM_MINS[drumState.minIdx]),
    };
    setAlarmUI(customAlarm);
    document.getElementById('drumOverlay').classList.remove('open');
  });
});

/* ── 드럼롤 피커 ── */
const DRUM_DAYS  = ['당일','1일 전','2일 전','3일 전','4일 전','5일 전','6일 전','1주일 전'];
const DRUM_AMPM  = ['오전','오후'];
const DRUM_HOURS = Array.from({length:12}, (_,i)=>String(i+1));
const DRUM_MINS  = Array.from({length:60}, (_,i)=>String(i).padStart(2,'0'));
let drumState = { dayIdx:0, ampmIdx:0, hourIdx:8, minIdx:0 };

function buildDrumList(listEl, items, selectedIdx) {
  if (!listEl) return;
  listEl.innerHTML = '';
  for(let i=0;i<3;i++) {
    const pad = document.createElement('div');
    pad.className = 'drum-item'; pad.style.visibility='hidden'; pad.textContent='-';
    listEl.appendChild(pad);
  }
  items.forEach((item, idx) => {
    const div = document.createElement('div');
    div.className = 'drum-item' + (idx===selectedIdx?' active':'');
    div.textContent = item;
    listEl.appendChild(div);
  });
  for(let i=0;i<3;i++) {
    const pad = document.createElement('div');
    pad.className = 'drum-item'; pad.style.visibility='hidden'; pad.textContent='-';
    listEl.appendChild(pad);
  }
  scrollDrumTo(listEl, selectedIdx, false);
}

function scrollDrumTo(listEl, idx, animate) {
  if (!listEl) return;
  const offset = -(idx * 60);
  listEl.style.transition = animate ? 'transform 0.15s ease-out' : 'none';
  listEl.style.transform = 'translateY(' + offset + 'px)';
  listEl.querySelectorAll('.drum-item').forEach((el, i) => {
    const realIdx = i - 3;
    el.classList.toggle('active', realIdx === idx);
  });
}

function updateDrumSummary() {
  const el = document.getElementById('drumSummary');
  if (!el) return;
  const day  = DRUM_DAYS[drumState.dayIdx];
  const ampm = DRUM_AMPM[drumState.ampmIdx];
  const h    = DRUM_HOURS[drumState.hourIdx];
  const m    = DRUM_MINS[drumState.minIdx];
  el.textContent = day + ' ' + ampm + ' ' + h + '시 ' + m + '분';
}

function attachDrumTouch(colEl, listEl, items, stateKey) {
  if (!colEl || !listEl) return;
  let startY=0, startIdx=0, isDragging=false;
  const onStart = e => {
    startY = (e.touches ? e.touches[0].clientY : e.clientY);
    startIdx = drumState[stateKey]; isDragging = true;
  };
  const onMove = e => {
    if (!isDragging) return;
    e.preventDefault();
    const y = (e.touches ? e.touches[0].clientY : e.clientY);
    const delta = Math.round((startY - y) / 60);
    let newIdx = Math.max(0, Math.min(items.length-1, startIdx+delta));
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
  if (typeof selectedAlarm === 'object' && selectedAlarm !== null) {
    const { dayOffset, ampm, h, m } = selectedAlarm;
    drumState.dayIdx  = Math.min(dayOffset||0, DRUM_DAYS.length-1);
    drumState.ampmIdx = ampm === '오후' ? 1 : 0;
    drumState.hourIdx = Math.max(0, Math.min(11, (h||9)-1));
    drumState.minIdx  = Math.max(0, Math.min(59, m||0));
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
  const ov = document.getElementById('drumOverlay');
  if (ov) ov.classList.add('open');
}

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
  const parts = eventDate.split('-').map(Number);
  const base = new Date(parts[0], parts[1]-1, parts[2]);
  let offsetDays=0, hour=9, min=0;
  if (alarm === 'day0_midnight') { offsetDays=0; hour=0; min=0; }
  else if (alarm === 'day0_9am') { offsetDays=0; hour=9; min=0; }
  else if (alarm === 'day1_9am') { offsetDays=1; hour=9; min=0; }
  else if (alarm === 'day2_9am') { offsetDays=2; hour=9; min=0; }
  else if (alarm === 'week1_9am'){ offsetDays=7; hour=9; min=0; }
  else if (typeof alarm === 'object') {
    offsetDays = alarm.dayOffset || 0;
    hour = alarm.h || 9; min = alarm.m || 0;
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
  const delay = alarmTime.getTime() - Date.now();
  if (delay <= 0) return;
  setTimeout(async () => {
    const granted = await requestNotificationPermission();
    if (!granted) return;
    new Notification('📅 ' + title, {
      body: '일정 알림: ' + alarmLabel(alarm),
      icon: '/icons/icon-192.png',
      badge: '/icons/icon-192.png',
      tag: 'event-' + title,
    });
  }, delay);
}
"""

for fname in ['galaxy.html', 'iphone.html', 'index.html']:
    fpath = f'/home/ubuntu/braindump/{fname}'
    with open(fpath, 'r', encoding='utf-8') as f:
        html = f.read()

    if 'ALARM FEATURE - JS' in html:
        print(f'[{fname}] 이미 JS 있음 - 스킵')
        continue

    # 마지막 </script> 앞에 삽입
    last_idx = html.rfind('</script>')
    if last_idx == -1:
        print(f'[{fname}] </script> 없음!')
        continue

    html = html[:last_idx] + ALARM_JS + '\n</script>' + html[last_idx+9:]

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'[{fname}] JS 삽입 완료')

print('완료!')
