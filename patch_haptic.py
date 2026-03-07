#!/usr/bin/env python3
"""
햅틱 반응 전체 적용 패치 스크립트
- 햅틱 유틸리티 함수(haptic) 삽입
- 모든 인터랙션 포인트에 haptic() 호출 추가
"""
import re

# ─── 햅틱 유틸리티 JS 코드 ───────────────────────────────────────────────────
HAPTIC_UTIL = """
// ═══════════════════════════════════════════════════════
// HAPTIC FEEDBACK UTILITY
// ═══════════════════════════════════════════════════════
const haptic = (() => {
  // iOS Safari: DeviceMotionEvent / navigator.vibrate 모두 시도
  const canVibrate = () => !!navigator.vibrate;

  return {
    // 가벼운 탭 (버튼 탭, 탭 전환 등)
    light:   () => canVibrate() && navigator.vibrate(10),
    // 중간 (항목 선택, 토글, 저장 등)
    medium:  () => canVibrate() && navigator.vibrate(25),
    // 강한 (삭제, 오류, 경고 등)
    heavy:   () => canVibrate() && navigator.vibrate(50),
    // 성공 패턴 (저장 완료, 연동 완료 등)
    success: () => canVibrate() && navigator.vibrate([15, 50, 15]),
    // 오류 패턴 (실패, 삭제 확인 등)
    error:   () => canVibrate() && navigator.vibrate([30, 30, 30]),
    // 더블 탭 (달력 날짜 선택, 드럼롤 확인 등)
    double:  () => canVibrate() && navigator.vibrate([12, 40, 12]),
    // 롱프레스 패턴 (스와이프 오픈 등)
    longpress: () => canVibrate() && navigator.vibrate(40),
  };
})();
"""

# ─── 각 파일별 패치 규칙 ──────────────────────────────────────────────────────
# (find_str, replace_str) 형태
# 주의: 이미 haptic이 있는 경우 중복 삽입 방지

PATCHES = [

  # ── 탭 전환 ──────────────────────────────────────────────────────────────
  (
    "btn.addEventListener('click', ()=>switchTab(btn.dataset.tab));",
    "btn.addEventListener('click', ()=>{ haptic.light(); switchTab(btn.dataset.tab); });"
  ),

  # ── 날짜 이전/다음 버튼 ────────────────────────────────────────────────
  (
    "document.getElementById('btnPrev').addEventListener('click', ()=>{",
    "document.getElementById('btnPrev').addEventListener('click', ()=>{ haptic.light();"
  ),
  (
    "document.getElementById('btnNext').addEventListener('click', ()=>{",
    "document.getElementById('btnNext').addEventListener('click', ()=>{ haptic.light();"
  ),

  # ── 헤더 날짜 클릭 → 달력 열기 ────────────────────────────────────────
  (
    "hdrDateBig.addEventListener('click', ()=>{ openCal(currentDate); });",
    "hdrDateBig.addEventListener('click', ()=>{ haptic.light(); openCal(currentDate); });"
  ),

  # ── 커스텀 달력 이전/다음 달 ──────────────────────────────────────────
  (
    "document.getElementById('calPrevMonth').addEventListener('click', ()=>{",
    "document.getElementById('calPrevMonth').addEventListener('click', ()=>{ haptic.light();"
  ),
  (
    "document.getElementById('calNextMonth').addEventListener('click', ()=>{",
    "document.getElementById('calNextMonth').addEventListener('click', ()=>{ haptic.light();"
  ),
  (
    "document.getElementById('calGotoToday').addEventListener('click', ()=>{",
    "document.getElementById('calGotoToday').addEventListener('click', ()=>{ haptic.medium();"
  ),
  (
    "document.getElementById('calCancel').addEventListener('click', closeCal);",
    "document.getElementById('calCancel').addEventListener('click', ()=>{ haptic.light(); closeCal(); });"
  ),

  # ── 달력 날짜 셀 클릭 ─────────────────────────────────────────────────
  (
    "el.addEventListener('click', ()=>{\n          haptic",
    "el.addEventListener('click', ()=>{\n          haptic"  # 이미 있으면 skip
  ),

  # ── 스케줄 탭 캘린더 날짜 클릭 ────────────────────────────────────────
  (
    "d.addEventListener('click', e => {",
    "d.addEventListener('click', e => { haptic.light();"
  ),

  # ── 스케줄 캘린더 이전/다음 ──────────────────────────────────────────
  (
    "document.getElementById('calPrev').addEventListener('click', ()=>{",
    "document.getElementById('calPrev').addEventListener('click', ()=>{ haptic.light();"
  ),
  (
    "document.getElementById('calNext').addEventListener('click', ()=>{",
    "document.getElementById('calNext').addEventListener('click', ()=>{ haptic.light();"
  ),

  # ── 스케줄 FAB (일정 추가 버튼) ──────────────────────────────────────
  (
    "document.getElementById('calFab').addEventListener('click', ()=>{",
    "document.getElementById('calFab').addEventListener('click', ()=>{ haptic.medium();"
  ),

  # ── 이벤트 시트 저장/취소/삭제 ───────────────────────────────────────
  (
    "document.getElementById('eventSave').addEventListener('click', async()=>{",
    "document.getElementById('eventSave').addEventListener('click', async()=>{ haptic.success();"
  ),
  (
    "document.getElementById('eventCancel').addEventListener('click', ()=>document.getElementById('eventOverlay').classList.add('hidden'));",
    "document.getElementById('eventCancel').addEventListener('click', ()=>{ haptic.light(); document.getElementById('eventOverlay').classList.add('hidden'); });"
  ),
  (
    "document.getElementById('eventDel').addEventListener('click', async()=>{",
    "document.getElementById('eventDel').addEventListener('click', async()=>{ haptic.error();"
  ),

  # ── 이벤트 도트 클릭 ─────────────────────────────────────────────────
  (
    "dot.addEventListener('click', ()=>{",
    "dot.addEventListener('click', ()=>{ haptic.light();"
  ),

  # ── 캘린더 월 타이틀 클릭 (연도 그리드 열기) ─────────────────────────
  (
    "calMonthTitle.addEventListener('click', ()=>{",
    "calMonthTitle.addEventListener('click', ()=>{ haptic.light();"
  ),

  # ── 연도 그리드 이전/다음 ─────────────────────────────────────────────
  (
    "document.getElementById('calYearPrev').addEventListener('click', ()=>{ calYearPageStart-=12; renderYearGrid(); });",
    "document.getElementById('calYearPrev').addEventListener('click', ()=>{ haptic.light(); calYearPageStart-=12; renderYearGrid(); });"
  ),
  (
    "document.getElementById('calYearNext').addEventListener('click', ()=>{ calYearPageStart+=12; renderYearGrid(); });",
    "document.getElementById('calYearNext').addEventListener('click', ()=>{ haptic.light(); calYearPageStart+=12; renderYearGrid(); });"
  ),

  # ── 카드 헤더 편집 버튼 ──────────────────────────────────────────────
  (
    "div.querySelector('.card-hdr-edit').addEventListener('click', () => {",
    "div.querySelector('.card-hdr-edit').addEventListener('click', () => { haptic.light();"
  ),

  # ── 태스크 시트 저장/취소/삭제 ───────────────────────────────────────
  (
    "document.getElementById('taskSave').addEventListener('click', async()=>{",
    "document.getElementById('taskSave').addEventListener('click', async()=>{ haptic.success();"
  ),
  (
    "document.getElementById('taskCancel').addEventListener('click', ()=>document.getElementById('taskOverlay').classList.add('hidden'));",
    "document.getElementById('taskCancel').addEventListener('click', ()=>{ haptic.light(); document.getElementById('taskOverlay').classList.add('hidden'); });"
  ),
  (
    "document.getElementById('taskDel').addEventListener('click', async()=>{",
    "document.getElementById('taskDel').addEventListener('click', async()=>{ haptic.error();"
  ),

  # ── 스와이프 편집/삭제 버튼 ──────────────────────────────────────────
  (
    "row.querySelector('.swipe-edit-btn')?.addEventListener('click', ()=>{",
    "row.querySelector('.swipe-edit-btn')?.addEventListener('click', ()=>{ haptic.medium();"
  ),
  (
    "row.querySelector('.swipe-del-btn')?.addEventListener('click', ()=>{",
    "row.querySelector('.swipe-del-btn')?.addEventListener('click', ()=>{ haptic.error();"
  ),

  # ── BrainDump 추가 버튼 ───────────────────────────────────────────────
  (
    "document.getElementById('bdAddBtn').addEventListener('click', async()=>{",
    "document.getElementById('bdAddBtn').addEventListener('click', async()=>{ haptic.success();"
  ),

  # ── BrainDump Today/Schedule 이동 버튼 ───────────────────────────────
  (
    "btn=>btn.addEventListener('click',()=>openMoveSheet(btn.dataset.bid,'today'))",
    "btn=>btn.addEventListener('click',()=>{ haptic.medium(); openMoveSheet(btn.dataset.bid,'today'); })"
  ),
  (
    "btn=>btn.addEventListener('click',()=>openMoveSheet(btn.dataset.bid,'schedule'))",
    "btn=>btn.addEventListener('click',()=>{ haptic.medium(); openMoveSheet(btn.dataset.bid,'schedule'); })"
  ),

  # ── BrainDump 삭제 버튼 ───────────────────────────────────────────────
  (
    "btn=>btn.addEventListener('click',async()=>{",
    "btn=>btn.addEventListener('click',async()=>{ haptic.error();"
  ),

  # ── Move 시트 확인/취소 ───────────────────────────────────────────────
  (
    "document.getElementById('moveConfirm').addEventListener('click', async()=>{",
    "document.getElementById('moveConfirm').addEventListener('click', async()=>{ haptic.success();"
  ),
  (
    "document.getElementById('moveCancel').addEventListener('click', ()=>document.getElementById('moveOverlay').classList.add('hidden'));",
    "document.getElementById('moveCancel').addEventListener('click', ()=>{ haptic.light(); document.getElementById('moveOverlay').classList.add('hidden'); });"
  ),

  # ── Archive 저장/취소 ─────────────────────────────────────────────────
  (
    "document.getElementById('arcSave').addEventListener('click', async()=>{",
    "document.getElementById('arcSave').addEventListener('click', async()=>{ haptic.success();"
  ),
  (
    "document.getElementById('arcCancel').addEventListener('click', ()=>document.getElementById('arcOverlay').classList.add('hidden'));",
    "document.getElementById('arcCancel').addEventListener('click', ()=>{ haptic.light(); document.getElementById('arcOverlay').classList.add('hidden'); });"
  ),

  # ── Archive 카테고리 버튼 ─────────────────────────────────────────────
  (
    "btn.addEventListener('click', ()=>{\n    arcCatBtns",
    "btn.addEventListener('click', ()=>{ haptic.light();\n    arcCatBtns"
  ),

  # ── 테마 토글 ─────────────────────────────────────────────────────────
  (
    "themeToggle.addEventListener('click', ()=>{",
    "themeToggle.addEventListener('click', ()=>{ haptic.medium();"
  ),

  # ── 로그아웃 버튼 (설정 탭 + 헤더) ──────────────────────────────────
  (
    "document.getElementById('logoutBtn').addEventListener('click', async()=>{",
    "document.getElementById('logoutBtn').addEventListener('click', async()=>{ haptic.heavy();"
  ),
  (
    "document.getElementById('hdrLogoutBtn').addEventListener('click', async()=>{",
    "document.getElementById('hdrLogoutBtn').addEventListener('click', async()=>{ haptic.heavy();"
  ),

  # ── OpenAI 키 설정 항목 ───────────────────────────────────────────────
  (
    "document.getElementById('openAiKeyItem').addEventListener('click', ()=>{",
    "document.getElementById('openAiKeyItem').addEventListener('click', ()=>{ haptic.light();"
  ),
  (
    "document.getElementById('openAiSave').addEventListener('click', async()=>{",
    "document.getElementById('openAiSave').addEventListener('click', async()=>{ haptic.success();"
  ),
  (
    "document.getElementById('openAiCancel').addEventListener('click', ()=>document.getElementById('openAiOverlay').classList.add('hidden'));",
    "document.getElementById('openAiCancel').addEventListener('click', ()=>{ haptic.light(); document.getElementById('openAiOverlay').classList.add('hidden'); });"
  ),

  # ── 구글 캘린더 연동/동기화 ───────────────────────────────────────────
  (
    "document.getElementById('gcalConnectItem').addEventListener('click', () => {",
    "document.getElementById('gcalConnectItem').addEventListener('click', () => { haptic.medium();"
  ),
  (
    "document.getElementById('gcalSyncItem').addEventListener('click', () => {",
    "document.getElementById('gcalSyncItem').addEventListener('click', () => { haptic.medium();"
  ),

  # ── 알림 시트 열기 ────────────────────────────────────────────────────
  (
    'onclick="openAlarmSheet()"',
    'onclick="haptic.light(); openAlarmSheet()"'
  ),

  # ── 알림 옵션 선택 ────────────────────────────────────────────────────
  (
    "alarmOv.addEventListener('click', e => {",
    "alarmOv.addEventListener('click', e => { haptic.medium();"
  ),

  # ── 드럼롤 피커 확인/취소 ─────────────────────────────────────────────
  (
    "if (drumConfirmBtn) drumConfirmBtn.addEventListener('click', () => {",
    "if (drumConfirmBtn) drumConfirmBtn.addEventListener('click', () => { haptic.double();"
  ),
  (
    "if (drumCancelBtn) drumCancelBtn.addEventListener('click', () => {",
    "if (drumCancelBtn) drumCancelBtn.addEventListener('click', () => { haptic.light();"
  ),

  # ── PWA 업데이트 버튼 ─────────────────────────────────────────────────
  (
    "btn.onclick = function() {",
    "btn.onclick = function() { haptic.success();"
  ),

  # ── PWA 설치 버튼 ─────────────────────────────────────────────────────
  (
    "installBtn.addEventListener('click', function() {",
    "installBtn.addEventListener('click', function() { haptic.medium();"
  ),

  # ── 로그인 버튼 ───────────────────────────────────────────────────────
  (
    "loginBtn.addEventListener('click', async () => {",
    "loginBtn.addEventListener('click', async () => { haptic.medium();"
  ),

  # ── 스와이프 touchstart (롱프레스 느낌) ──────────────────────────────
  (
    "row.addEventListener('touchend', ()=>{ swiping=false; });",
    "row.addEventListener('touchend', ()=>{ if(swiping) haptic.longpress(); swiping=false; });"
  ),

]

FILES = [
  '/home/ubuntu/braindump/galaxy.html',
  '/home/ubuntu/braindump/iphone.html',
  '/home/ubuntu/braindump/index.html',
]

def patch_file(fpath):
  with open(fpath, 'r', encoding='utf-8') as f:
    content = f.read()

  # 이미 햅틱 유틸리티가 있으면 삽입 skip
  if 'HAPTIC FEEDBACK UTILITY' not in content:
    # </script> 첫 번째 앞에 삽입
    content = content.replace('</script>', HAPTIC_UTIL + '\n</script>', 1)
    print(f"  [+] 햅틱 유틸리티 삽입")
  else:
    print(f"  [=] 햅틱 유틸리티 이미 존재, skip")

  applied = 0
  skipped = 0
  for find, replace in PATCHES:
    if find == replace:
      skipped += 1
      continue
    if find in content:
      # 이미 haptic이 포함된 replace가 있으면 skip
      if replace in content:
        skipped += 1
        continue
      content = content.replace(find, replace, 1)
      applied += 1
    else:
      skipped += 1

  with open(fpath, 'w', encoding='utf-8') as f:
    f.write(content)

  print(f"  [+] 패치 적용: {applied}개, skip: {skipped}개")
  return applied

for fpath in FILES:
  fname = fpath.split('/')[-1]
  print(f"\n=== {fname} ===")
  patch_file(fpath)

print("\n완료!")
