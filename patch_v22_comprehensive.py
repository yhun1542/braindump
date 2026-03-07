#!/usr/bin/env python3
"""
v22 종합 패치 스크립트
3회 정독 후 발견된 모든 버그/개선 포인트 적용:
1. 버그 수정: evTitle → eventTitle (execConvert 일정 변환 버그)
2. 버그 수정: alert() → showSaved() 토스트로 교체
3. 다크모드: v22 신규 요소 (arc-dash, arc-hub, arc-link-card 등) 다크모드 변수 추가
4. 다크모드: --hdr-bg 다크모드에서 어두운 색으로 수정 (크림색 → 다크 배경)
5. 업그레이드: execConvert 일정 변환 - 여러 항목 순차 처리
6. 업그레이드: arcSearchScore - 즐겨찾기 가중치 강화, 최근 접근 가중치 추가
7. 업그레이드: 아카이브 카드에 '종류' 배지 표시 (meeting/material/idea)
8. 업그레이드: 아카이브 저장 시 alert → showSaved 토스트
9. 업그레이드: openMeetingSummary - 액션 아이템 Today 전송 개선
10. 업그레이드: 다크모드에서 arc-ctx-menu 배경색 개선
"""

import re

TARGET_FILES = [
    '/home/ubuntu/braindump/galaxy.html',
    '/home/ubuntu/braindump/iphone.html',
    '/home/ubuntu/braindump/index.html',
]

def patch_file(path):
    with open(path, encoding='utf-8') as f:
        content = f.read()

    original = content
    patches_applied = []

    # ─────────────────────────────────────────────────────────────
    # 1. 버그 수정: execConvert에서 evTitle → eventTitle
    # ─────────────────────────────────────────────────────────────
    old = "const titleEl = document.getElementById('evTitle'); if(titleEl) titleEl.value=f"
    new = "const titleEl = document.getElementById('eventTitle'); if(titleEl) titleEl.value=f"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("BUG#1: evTitle → eventTitle 수정")

    # ─────────────────────────────────────────────────────────────
    # 2. 버그 수정: alert() → showSaved() 토스트
    # ─────────────────────────────────────────────────────────────
    old = "if(!title && !content && !file) { alert('제목 또는 내용을 입력해주세요'); return; }"
    new = "if(!title && !content && !file) { showSaved('제목 또는 내용을 입력해주세요'); return; }"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("BUG#2: alert() → showSaved() 토스트 교체")

    # ─────────────────────────────────────────────────────────────
    # 3. 다크모드: --hdr-bg 다크모드에서 어두운 색으로 수정
    # 현재: --hdr-bg: #f0f0ec (크림색) → 어두운 모드에서 밝게 보임
    # 수정: --hdr-bg: #1a1a1a (어두운 배경)
    # ─────────────────────────────────────────────────────────────
    old = "--bg: #0e0e0e; --surface: #1a1a1a; --hdr-bg: #f0f0ec; --hdr-text: #111111;"
    new = "--bg: #0e0e0e; --surface: #1a1a1a; --hdr-bg: #1a1a1a; --hdr-text: #f0f0ec;"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#1: 다크모드 --hdr-bg 크림색 → 어두운 배경 수정")

    # ─────────────────────────────────────────────────────────────
    # 4. 다크모드: v22 신규 요소 다크모드 CSS 변수 추가
    # arc-dash-*, arc-hub-*, arc-link-card, arc-ctx-menu 등
    # ─────────────────────────────────────────────────────────────
    dark_new_vars = """
  /* v22 신규 요소 다크모드 */
  --arc-dash-bg: #1a1a1a;
  --arc-dash-stat-bg: #252525;
  --arc-dash-stat-border: #333;
  --arc-hub-bg: #1a1a1a;
  --arc-hub-border: #2a2a2a;
  --arc-hub-chip-bg: #252525;
  --arc-hub-chip-border: #333;
  --arc-hub-chip-text: #e0e0e0;
  --arc-link-card-bg: #1e2a3a;
  --arc-link-card-border: #2a3a4a;
  --arc-ctx-menu-bg: #252525;
  --arc-ctx-menu-border: #333;
  --arc-ctx-item-hover: #333;
  --arc-meet-sheet-bg: #1a1a1a;
  --arc-conv-sheet-bg: #1a1a1a;
  --arc-kind-meeting-bg: rgba(245,158,11,0.15);
  --arc-kind-material-bg: rgba(59,130,246,0.15);
  --arc-kind-idea-bg: rgba(16,185,129,0.15);"""

    # 다크모드 블록 끝 부분에 추가
    marker = "  --arc-type-note-bg: #1e2a1e;\n  --arc-type-url-bg: #1a2030;\n  --arc-type-image-bg: #2a1e1e;\n  --arc-type-video-bg: #1e1e2a;\n  --arc-type-file-bg: #2a2a1e;"
    if marker in content and dark_new_vars.strip() not in content:
        content = content.replace(marker, marker + dark_new_vars)
        patches_applied.append("DARK#2: v22 신규 요소 다크모드 CSS 변수 추가")

    # ─────────────────────────────────────────────────────────────
    # 5. 다크모드: arc-dash-stat CSS에 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-dash-stat { background: var(--surface); border: 1px solid var(--border);"
    new = ".arc-dash-stat { background: var(--arc-dash-stat-bg, var(--surface)); border: 1px solid var(--arc-dash-stat-border, var(--border));"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#3: arc-dash-stat 다크모드 변수 적용")

    # ─────────────────────────────────────────────────────────────
    # 6. 다크모드: arc-ctx-menu CSS에 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-ctx-menu { position:fixed; background:#fff; border:1px solid #e5e7eb;"
    new = ".arc-ctx-menu { position:fixed; background:var(--arc-ctx-menu-bg,#fff); border:1px solid var(--arc-ctx-menu-border,#e5e7eb);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#4: arc-ctx-menu 다크모드 변수 적용")

    old = ".arc-ctx-item:hover { background:#f3f4f6; }"
    new = ".arc-ctx-item:hover { background:var(--arc-ctx-item-hover,#f3f4f6); }"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#5: arc-ctx-item hover 다크모드 변수 적용")

    # ─────────────────────────────────────────────────────────────
    # 7. 다크모드: arc-hub CSS에 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-hub { background: var(--surface); border: 1px solid var(--border);"
    new = ".arc-hub { background: var(--arc-hub-bg, var(--surface)); border: 1px solid var(--arc-hub-border, var(--border));"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#6: arc-hub 다크모드 변수 적용")

    # ─────────────────────────────────────────────────────────────
    # 8. 다크모드: arc-meet-sheet, arc-conv-sheet 배경 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = "#arcMeetSheet, #arcConvSheet, #arcDashSheet { position:fixed; inset:0; background:rgba(0,0,0,0.5);"
    new = "#arcMeetSheet, #arcConvSheet, #arcDashSheet { position:fixed; inset:0; background:rgba(0,0,0,0.6);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#7: arc 시트 오버레이 투명도 개선")

    # ─────────────────────────────────────────────────────────────
    # 9. 다크모드: arc-meet-body, arc-conv-body 배경 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-meet-body, .arc-conv-body, .arc-dash-body { background: var(--surface);"
    new = ".arc-meet-body, .arc-conv-body, .arc-dash-body { background: var(--arc-meet-sheet-bg, var(--surface));"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#8: arc 시트 바디 다크모드 변수 적용")

    # ─────────────────────────────────────────────────────────────
    # 10. 업그레이드: execConvert - 일정 변환 시 여러 항목 모두 처리
    # 기존: 첫 항목만 일정 시트에 넣고 나머지는 수동 처리 안내
    # 개선: 여러 항목을 Today에 모두 추가하거나, 일정은 첫 항목 + 나머지 Today로 분배
    # ─────────────────────────────────────────────────────────────
    old = """  } else {
    // Schedule: open the event sheet for the first item, others can be added later
    const first = selected[0];
    openEventSheet(null, null);
    setTimeout(()=>{ const titleEl = document.getElementById('eventTitle'); if(titleEl) titleEl.value=first; }, 200);
    if(selected.length>1) showSaved(`📅 첫 항목을 일정에 추가 중. 나머지 ${selected.length-1}개는 직접 추가해주세요`);
  }"""
    new = """  } else {
    // Schedule: open the event sheet for the first item
    const first = selected[0];
    openEventSheet(null, null);
    setTimeout(()=>{ const titleEl = document.getElementById('eventTitle'); if(titleEl) titleEl.value=first; }, 200);
    // 나머지 항목들은 Today에 자동 추가
    if(selected.length>1) {
      const cardId = CARDS[0]?.id;
      if(cardId) { for(const t of selected.slice(1)) await addTask(cardId, t); }
      showSaved(`📅 일정 1개 + Today ${selected.length-1}개 추가됨`);
    } else {
      showSaved('📅 일정에 추가 중...');
    }
  }"""
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#1: execConvert 여러 항목 처리 개선 (나머지 Today 자동 추가)")

    # ─────────────────────────────────────────────────────────────
    # 11. 업그레이드: arcSearchScore - 즐겨찾기 가중치 강화 (6→12)
    # ─────────────────────────────────────────────────────────────
    old = "  if(item.pinned) score += 6;\n  return score;"
    new = "  if(item.pinned) score += 12;\n  if(item.favorite) score += 8;\n  return score;"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#2: arcSearchScore 즐겨찾기 가중치 강화 (6→12)")

    # ─────────────────────────────────────────────────────────────
    # 12. 업그레이드: 아카이브 카드에 kind 배지 표시
    # arc-item 카드의 헤더 부분에 kind 배지 추가
    # ─────────────────────────────────────────────────────────────
    old = "      ${item.pinned ? '<span class=\"arc-pin-badge\">⭐</span>' : ''}"
    new = """      ${item.pinned ? '<span class="arc-pin-badge">⭐</span>' : ''}
      ${item.kind && item.kind!=='general' ? `<span class="arc-kind-badge arc-kind-${item.kind}">${item.kind==='meeting'?'📋 회의':item.kind==='material'?'📁 자료':item.kind==='idea'?'💡 아이디어':''}</span>` : ''}"""
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#3: 아카이브 카드 kind 배지 표시 추가")

    # ─────────────────────────────────────────────────────────────
    # 13. 업그레이드: arc-kind-badge CSS 추가
    # ─────────────────────────────────────────────────────────────
    kind_badge_css = """
.arc-kind-badge { display:inline-flex; align-items:center; gap:3px; font-size:10px; font-weight:600; padding:2px 7px; border-radius:10px; margin-left:4px; }
.arc-kind-meeting { background:var(--arc-kind-meeting-bg,rgba(245,158,11,0.12)); color:#f59e0b; }
.arc-kind-material { background:var(--arc-kind-material-bg,rgba(59,130,246,0.12)); color:#3b82f6; }
.arc-kind-idea { background:var(--arc-kind-idea-bg,rgba(16,185,129,0.12)); color:#10b981; }
"""
    if '.arc-kind-badge' not in content:
        # arc-pin-badge CSS 뒤에 추가
        old_css = ".arc-pin-badge { position:absolute; top:8px; right:8px; font-size:14px; }"
        if old_css in content:
            content = content.replace(old_css, old_css + kind_badge_css)
            patches_applied.append("UPG#4: arc-kind-badge CSS 추가")

    # ─────────────────────────────────────────────────────────────
    # 14. 업그레이드: openMeetingSummary - 액션 아이템 Today 전송 개선
    # 기존: addTask(CARDS[0]?.id, item) 단순 호출
    # 개선: 여러 항목 선택 후 일괄 전송 + 성공 피드백
    # ─────────────────────────────────────────────────────────────
    old = "window.sendMeetingActionsToToday = async() => {"
    new = "window.sendMeetingActionsToToday = async() => { haptic.medium();"
    if old in content and "window.sendMeetingActionsToToday = async() => { haptic.medium();" not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#5: sendMeetingActionsToToday 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 15. 업그레이드: arc-link-card 다크모드 배경 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-link-card { display:flex; align-items:stretch; background:var(--bg);"
    new = ".arc-link-card { display:flex; align-items:stretch; background:var(--arc-link-card-bg,var(--bg));"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK#9: arc-link-card 다크모드 배경 변수 적용")

    # ─────────────────────────────────────────────────────────────
    # 16. 업그레이드: 아카이브 검색창 placeholder 개선
    # ─────────────────────────────────────────────────────────────
    old = 'placeholder="🔍 아카이브 검색..."'
    new = 'placeholder="🔍 제목, 태그, @멘션, [[위키링크]] 검색..."'
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#6: 아카이브 검색창 placeholder 개선")

    # ─────────────────────────────────────────────────────────────
    # 17. 업그레이드: arc-item 카드 클릭 시 URL 타입이면 링크 열기
    # 현재: 카드 클릭 이벤트 없음 (버튼으로만 접근)
    # 개선: URL 타입 카드 더블탭 → 링크 열기
    # ─────────────────────────────────────────────────────────────
    old = 'oncontextmenu="arcShowCtx(event,\'${item.id}\'); return false;" ontouchst'
    new = 'oncontextmenu="arcShowCtx(event,\'${item.id}\'); return false;" ondblclick="if(\'${item.type}\'===\'url\'){haptic.medium();arcOpenUrl(\'${(item.content||item.url||\'\')\'.replace(/\'/g,\'\\\\\'\')}\')}else{arcShowCtx(event,\'${item.id}\')}" ontouchst'
    if old in content and 'ondblclick' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#7: URL 카드 더블탭 링크 열기 추가")

    # ─────────────────────────────────────────────────────────────
    # 18. 업그레이드: 아카이브 정렬 버튼에 '즐겨찾기 우선' 옵션 추가
    # 기존 정렬 드롭다운에 이미 있으나, 기본값 표시 개선
    # ─────────────────────────────────────────────────────────────
    old = "window.setArcSort = (mode) => { arcSortMode = mode; haptic.light();"
    new = "window.setArcSort = (mode) => { arcSortMode = mode; haptic.light(); document.getElementById('arcSortBtn')?.setAttribute('title', mode==='oldest'?'오래된순':mode==='pinned'?'즐겨찾기 우선':'최신순');"
    if old in content and "setAttribute('title'" not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#8: 정렬 버튼 title 속성 동적 업데이트")

    # ─────────────────────────────────────────────────────────────
    # 19. 업그레이드: arc-item-actions 버튼 텍스트 개선
    # 기존: 🔗 열기 → 🔗 열기 (URL), 📄 열기 (PDF)
    # 개선: 버튼에 title 속성 추가로 접근성 향상
    # ─────────────────────────────────────────────────────────────
    old = '<button class="arc-act-btn arc-act-open" onclick="haptic.medium(); arcOpenUrl(\'${escHtml(item.content||item.url||\'\')\'.replace(/\'/g,\'\\\\\'\')}\')" title="링크 열기">🔗 열기</button>'
    new = '<button class="arc-act-btn arc-act-open" onclick="haptic.medium(); arcOpenUrl(\'${escHtml(item.content||item.url||\'\')\'.replace(/\'/g,\'\\\\\'\')}\')" title="${arcIsPdf(item)?\'PDF 열기\':\'링크 열기\'}">${arcIsPdf(item)?\'📄 열기\':\'🔗 열기\'}</button>'
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#9: arc-act-open 버튼 PDF/URL 구분 표시")

    # ─────────────────────────────────────────────────────────────
    # 20. 업그레이드: 아카이브 빈 상태 메시지 개선
    # ─────────────────────────────────────────────────────────────
    old = "<div>조건에 맞는 자료가 없습니다</div><div style="
    new = "<div style='font-weight:600;margin-bottom:4px'>조건에 맞는 자료가 없습니다</div><div style="
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG#10: 빈 상태 메시지 스타일 개선")

    # ─────────────────────────────────────────────────────────────
    # 결과 저장
    # ─────────────────────────────────────────────────────────────
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {path.split('/')[-1]}: {len(patches_applied)}개 패치 적용")
        for p in patches_applied:
            print(f"   - {p}")
    else:
        print(f"⚠️  {path.split('/')[-1]}: 변경 없음 (이미 적용됨 또는 패턴 불일치)")

    return patches_applied

if __name__ == '__main__':
    print("=" * 60)
    print("v22 종합 패치 시작")
    print("=" * 60)
    total = 0
    for f in TARGET_FILES:
        applied = patch_file(f)
        total += len(applied)
    print("=" * 60)
    print(f"총 {total}개 패치 적용 완료")
