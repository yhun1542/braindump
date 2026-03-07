#!/usr/bin/env python3
"""
패치 내용:
1. 로그인 화면: dark 로고 → light 로고 (라이트모드 디폴트이므로)
2. 로그인 화면: "최고의 답을 찾기 위한 여정을 시작하세요" 문구 삭제
3. 커스텀 달력 팝업: input[type=date] → 풀 커스텀 월간 달력 UI
"""
import re

CUSTOM_CALENDAR_CSS = """
/* ── Custom Date Picker ── */
.date-overlay {
  position: fixed; inset: 0; z-index: 700;
  background: rgba(0,0,0,0.45);
  display: flex; align-items: center; justify-content: center;
  backdrop-filter: blur(4px);
}
.date-overlay.hidden { display: none; }
.cal-box {
  background: var(--surface); border-radius: 20px;
  padding: 20px 16px 16px; width: 320px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.25);
  font-family: var(--font);
}
.cal-header {
  display: flex; align-items: center; justify-content: space-between;
  margin-bottom: 14px;
}
.cal-title {
  font-size: 17px; font-weight: 700; color: var(--text);
  cursor: pointer; user-select: none;
}
.cal-nav-btn {
  background: none; border: none; cursor: pointer;
  font-size: 20px; color: var(--text-muted);
  width: 32px; height: 32px; border-radius: 50%;
  display: flex; align-items: center; justify-content: center;
  transition: background 0.15s;
}
.cal-nav-btn:hover { background: var(--border-light); }
.cal-weekdays {
  display: grid; grid-template-columns: repeat(7, 1fr);
  margin-bottom: 6px;
}
.cal-wd {
  text-align: center; font-size: 11px; font-weight: 600;
  color: var(--text-muted); padding: 4px 0;
}
.cal-wd:first-child { color: #e05555; }
.cal-wd:last-child  { color: #4a90d9; }
.cal-days {
  display: grid; grid-template-columns: repeat(7, 1fr);
  gap: 2px;
}
.cal-day {
  aspect-ratio: 1; display: flex; align-items: center; justify-content: center;
  border-radius: 50%; font-size: 13px; cursor: pointer;
  color: var(--text); transition: background 0.12s, color 0.12s;
  position: relative;
}
.cal-day:hover:not(.cal-empty):not(.cal-selected) {
  background: var(--border-light);
}
.cal-day.cal-empty { cursor: default; }
.cal-day.cal-today {
  font-weight: 700;
  color: var(--accent);
}
.cal-day.cal-today::after {
  content: ''; position: absolute; bottom: 3px; left: 50%;
  transform: translateX(-50%);
  width: 4px; height: 4px; border-radius: 50%;
  background: var(--accent);
}
.cal-day.cal-selected {
  background: var(--accent); color: #fff; font-weight: 700;
}
.cal-day.cal-selected::after { display: none; }
.cal-day.cal-sun { color: #e05555; }
.cal-day.cal-sat { color: #4a90d9; }
.cal-day.cal-selected.cal-sun,
.cal-day.cal-selected.cal-sat { color: #fff; }
.cal-day.cal-holiday { color: #e05555; }
.cal-footer {
  display: flex; gap: 8px; margin-top: 14px;
}
.cal-btn-cancel {
  flex: 1; padding: 10px; border-radius: 10px; border: 1.5px solid var(--border-mid);
  background: none; color: var(--text-muted); font-size: 14px; cursor: pointer;
  font-family: var(--font); transition: background 0.12s;
}
.cal-btn-cancel:hover { background: var(--border-light); }
.cal-btn-today {
  flex: 1; padding: 10px; border-radius: 10px; border: none;
  background: var(--border-light); color: var(--text); font-size: 14px; cursor: pointer;
  font-family: var(--font); font-weight: 600; transition: background 0.12s;
}
.cal-btn-today:hover { background: var(--border-mid); }
/* Year picker overlay inside cal-box */
.cal-year-grid {
  display: grid; grid-template-columns: repeat(4, 1fr);
  gap: 6px; margin-top: 8px;
}
.cal-year-item {
  padding: 8px 4px; text-align: center; border-radius: 10px;
  font-size: 14px; cursor: pointer; color: var(--text);
  transition: background 0.12s;
}
.cal-year-item:hover { background: var(--border-light); }
.cal-year-item.cal-year-selected { background: var(--accent); color: #fff; font-weight: 700; }
"""

CUSTOM_CALENDAR_HTML = """<!-- Custom Date Picker -->
<div class="date-overlay hidden" id="dateOverlay">
  <div class="cal-box" id="calBox">
    <!-- normal month view -->
    <div id="calMonthView">
      <div class="cal-header">
        <button class="cal-nav-btn" id="calPrevMonth">&#8249;</button>
        <div class="cal-title" id="calTitle">2026년 3월</div>
        <button class="cal-nav-btn" id="calNextMonth">&#8250;</button>
      </div>
      <div class="cal-weekdays">
        <div class="cal-wd">일</div><div class="cal-wd">월</div>
        <div class="cal-wd">화</div><div class="cal-wd">수</div>
        <div class="cal-wd">목</div><div class="cal-wd">금</div>
        <div class="cal-wd">토</div>
      </div>
      <div class="cal-days" id="calDays"></div>
      <div class="cal-footer">
        <button class="cal-btn-cancel" id="calCancel">취소</button>
        <button class="cal-btn-today" id="calGotoToday">오늘</button>
      </div>
    </div>
    <!-- year picker view -->
    <div id="calYearView" style="display:none;">
      <div class="cal-header">
        <button class="cal-nav-btn" id="calYearPrev">&#8249;</button>
        <div class="cal-title" id="calYearRangeTitle">2020 – 2031</div>
        <button class="cal-nav-btn" id="calYearNext">&#8250;</button>
      </div>
      <div class="cal-year-grid" id="calYearGrid"></div>
    </div>
  </div>
</div>"""

CUSTOM_CALENDAR_JS = """
/* ── Custom Date Picker JS ── */
(function(){
  const KR_HOLIDAYS_CAL = {
    '2025-01-01':true,'2025-01-28':true,'2025-01-29':true,'2025-01-30':true,
    '2025-03-01':true,'2025-05-05':true,'2025-05-06':true,'2025-06-06':true,
    '2025-08-15':true,'2025-10-03':true,'2025-10-05':true,'2025-10-06':true,
    '2025-10-07':true,'2025-10-09':true,'2025-12-25':true,
    '2026-01-01':true,'2026-01-28':true,'2026-01-29':true,'2026-01-30':true,
    '2026-03-01':true,'2026-05-05':true,'2026-06-06':true,
    '2026-08-17':true,'2026-09-24':true,'2026-09-25':true,'2026-09-26':true,
    '2026-10-03':true,'2026-10-09':true,'2026-12-25':true,
    '2027-01-01':true,'2027-02-17':true,'2027-02-18':true,'2027-02-19':true,
    '2027-03-01':true,'2027-05-05':true,'2027-06-06':true,
    '2027-08-16':true,'2027-10-04':true,'2027-10-05':true,'2027-10-06':true,
    '2027-10-09':true,'2027-12-25':true,
  };
  let calPickYear, calPickMonth, calPickSelected;
  let calYearPageStart = 2020;

  function pad(n){ return String(n).padStart(2,'0'); }
  function ds(y,m,d){ return `${y}-${pad(m)}-${pad(d)}`; }

  function openCal(selDate){
    calPickSelected = selDate;
    calPickYear  = selDate.getFullYear();
    calPickMonth = selDate.getMonth();
    document.getElementById('calYearView').style.display='none';
    document.getElementById('calMonthView').style.display='';
    renderCalMonth();
    document.getElementById('dateOverlay').classList.remove('hidden');
  }
  function closeCal(){
    document.getElementById('dateOverlay').classList.add('hidden');
  }

  function renderCalMonth(){
    const y = calPickYear, m = calPickMonth;
    document.getElementById('calTitle').textContent = `${y}년 ${m+1}월`;
    const firstDay = new Date(y, m, 1).getDay();
    const daysInMonth = new Date(y, m+1, 0).getDate();
    const todayStr = ds(new Date().getFullYear(), new Date().getMonth()+1, new Date().getDate());
    const selStr = calPickSelected ? ds(calPickSelected.getFullYear(), calPickSelected.getMonth()+1, calPickSelected.getDate()) : '';
    let html = '';
    for(let i=0;i<firstDay;i++) html += '<div class="cal-day cal-empty"></div>';
    for(let d=1;d<=daysInMonth;d++){
      const dStr = ds(y, m+1, d);
      const dow = new Date(y,m,d).getDay();
      let cls = 'cal-day';
      if(dow===0) cls += ' cal-sun';
      if(dow===6) cls += ' cal-sat';
      if(KR_HOLIDAYS_CAL[dStr]) cls += ' cal-holiday';
      if(dStr===todayStr) cls += ' cal-today';
      if(dStr===selStr) cls += ' cal-selected';
      html += `<div class="${cls}" data-date="${dStr}">${d}</div>`;
    }
    document.getElementById('calDays').innerHTML = html;
    document.getElementById('calDays').querySelectorAll('.cal-day:not(.cal-empty)').forEach(el=>{
      el.addEventListener('click', ()=>{
        const d = new Date(el.dataset.date+'T00:00:00');
        currentDate = d;
        updateHeader();
        resubscribeToday();
        closeCal();
      });
    });
  }

  function renderYearGrid(){
    const range = [];
    for(let y=calYearPageStart; y<calYearPageStart+12; y++) range.push(y);
    document.getElementById('calYearRangeTitle').textContent = `${calYearPageStart} – ${calYearPageStart+11}`;
    document.getElementById('calYearGrid').innerHTML = range.map(y=>
      `<div class="cal-year-item${y===calPickYear?' cal-year-selected':''}" data-year="${y}">${y}</div>`
    ).join('');
    document.getElementById('calYearGrid').querySelectorAll('.cal-year-item').forEach(el=>{
      el.addEventListener('click', ()=>{
        calPickYear = parseInt(el.dataset.year);
        document.getElementById('calYearView').style.display='none';
        document.getElementById('calMonthView').style.display='';
        renderCalMonth();
      });
    });
  }

  document.getElementById('calTitle').addEventListener('click', ()=>{
    calYearPageStart = Math.floor(calPickYear/12)*12;
    document.getElementById('calMonthView').style.display='none';
    document.getElementById('calYearView').style.display='';
    renderYearGrid();
  });
  document.getElementById('calYearPrev').addEventListener('click', ()=>{ calYearPageStart-=12; renderYearGrid(); });
  document.getElementById('calYearNext').addEventListener('click', ()=>{ calYearPageStart+=12; renderYearGrid(); });
  document.getElementById('calPrevMonth').addEventListener('click', ()=>{
    calPickMonth--; if(calPickMonth<0){calPickMonth=11;calPickYear--;} renderCalMonth();
  });
  document.getElementById('calNextMonth').addEventListener('click', ()=>{
    calPickMonth++; if(calPickMonth>11){calPickMonth=0;calPickYear++;} renderCalMonth();
  });
  document.getElementById('calCancel').addEventListener('click', closeCal);
  document.getElementById('calGotoToday').addEventListener('click', ()=>{
    const t = new Date();
    calPickYear=t.getFullYear(); calPickMonth=t.getMonth();
    calPickSelected=t; renderCalMonth();
    currentDate=t; updateHeader(); resubscribeToday(); closeCal();
  });
  document.getElementById('dateOverlay').addEventListener('click', e=>{
    if(e.target===document.getElementById('dateOverlay')) closeCal();
  });

  // 날짜 클릭 시 커스텀 달력 열기
  hdrDateBig.addEventListener('click', ()=>{ openCal(currentDate); });
  if(document.getElementById('hdrDateSub'))
    document.getElementById('hdrDateSub').addEventListener('click', ()=>{ openCal(currentDate); });

  window.__openCustomCal = openCal;
})();
"""

import os

files = [
    '/home/ubuntu/braindump/galaxy.html',
    '/home/ubuntu/braindump/iphone.html',
    '/home/ubuntu/braindump/index.html',
]

for fpath in files:
    with open(fpath, 'r', encoding='utf-8') as f:
        c = f.read()

    changed = []

    # 1. 로그인 로고 dark → light
    if 'jf_os_header_dark' in c and 'loginLogoImg' in c:
        c = c.replace(
            '<img src="/images/jf_os_header_dark_1x.png"\n           srcset="/images/jf_os_header_dark_1x.png 1x, /images/jf_os_header_dark_2x.png 2x, /images/jf_os_header_dark_3x.png 3x"\n           alt="JF OS" height="56" id="loginLogoImg">',
            '<img src="/images/jf_os_header_light_1x.png"\n           srcset="/images/jf_os_header_light_1x.png 1x, /images/jf_os_header_light_2x.png 2x, /images/jf_os_header_light_3x.png 3x"\n           alt="JF OS" height="56" id="loginLogoImg">'
        )
        changed.append('로그인 로고 light 교체')

    # 2. 문구 삭제
    if '최고의 답을 찾기 위한 여정을 시작하세요' in c:
        c = re.sub(r'\s*<div class="login-sub">최고의 답을 찾기 위한 여정을 시작하세요</div>', '', c)
        changed.append('문구 삭제')

    # 3. 커스텀 달력 CSS 교체
    old_css = r'/\* Date picker overlay \*/\s*\.date-overlay \{[^}]+\}\s*\.date-overlay\.hidden \{ display: none; \}\s*\.date-box \{[^}]+\}\s*\.date-box input\[type="date"\] \{[^}]+\}'
    if re.search(old_css, c, re.DOTALL):
        c = re.sub(old_css, CUSTOM_CALENDAR_CSS.strip(), c, flags=re.DOTALL)
        changed.append('달력 CSS 교체')

    # 4. 커스텀 달력 HTML 교체
    old_html = r'<!-- Date Picker -->\s*<div class="date-overlay hidden" id="dateOverlay">.*?</div>\s*</div>'
    if re.search(old_html, c, re.DOTALL):
        c = re.sub(old_html, CUSTOM_CALENDAR_HTML.strip(), c, flags=re.DOTALL)
        changed.append('달력 HTML 교체')

    # 5. 기존 날짜 클릭 JS 교체 (hdrDateBig.addEventListener ~ datePickerOk 블록)
    old_js = r'// btnToday removed from header\s*hdrDateBig\.addEventListener\(\'click\'.*?document\.getElementById\(\'dateOverlay\'\)\.classList\.add\(\'hidden\'\);\s*\}\);'
    if re.search(old_js, c, re.DOTALL):
        c = re.sub(old_js, CUSTOM_CALENDAR_JS.strip(), c, flags=re.DOTALL)
        changed.append('달력 JS 교체')

    with open(fpath, 'w', encoding='utf-8') as f:
        f.write(c)

    fname = os.path.basename(fpath)
    print(f"{fname}: {', '.join(changed) if changed else '변경 없음'}")

print("\n완료!")
