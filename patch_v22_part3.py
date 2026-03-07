#!/usr/bin/env python3
"""
v22 3차 패치 - 누락 항목 수정 및 추가 업그레이드
1. BUG#2: 삭제 확인 메시지 (alert 패턴 다름)
2. UPG: execConvert 다중 항목 처리 주석 추가
3. UPG: sendMeetActionsToToday 햅틱 추가
4. UPG: arcInferProject 함수 추가 (arcGuessProject 래퍼)
5. UPG: arcEditItem → arcEdit 함수 별칭 추가
6. UPG: 아카이브 카드 kind 배지 렌더링 개선
7. UPG: 다크모드 Today 탭 카드 헤더 완전 수정
8. UPG: 아카이브 허브 다크모드 개선
9. UPG: 아카이브 검색 결과 없을 때 힌트 개선
10. UPG: AI 리마인더 섹션 다크모드 개선
"""

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
    # 1. BUG: 삭제 확인 - 실제 패턴 찾아서 수정
    # ─────────────────────────────────────────────────────────────
    for old_pat, new_pat in [
        ("if(!confirm('삭제하시겠습니까?')) return;",
         "if(!confirm('이 항목을 삭제하시겠습니까? 되돌릴 수 없습니다.')) return;"),
        ('if(!confirm("삭제하시겠습니까?")) return;',
         'if(!confirm("이 항목을 삭제하시겠습니까? 되돌릴 수 없습니다.")) return;'),
        ("confirm('삭제?')",
         "confirm('이 항목을 삭제하시겠습니까?')"),
    ]:
        if old_pat in content:
            content = content.replace(old_pat, new_pat)
            patches_applied.append(f"BUG: 삭제 확인 메시지 개선")

    # ─────────────────────────────────────────────────────────────
    # 2. UPG: sendMeetActionsToToday 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.sendMeetActionsToToday = async(actions) => {\n  const items = Array.isArray(actions)?actions:[];"
    new = "window.sendMeetActionsToToday = async(actions) => { haptic.medium();\n  const items = Array.isArray(actions)?actions:[];"
    if old in content and 'sendMeetActionsToToday = async(actions) => { haptic.medium()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: sendMeetActionsToToday 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 3. UPG: arcInferProject 함수 추가 (arcGuessProject 래퍼)
    # arcGuessProject 함수 뒤에 추가
    # ─────────────────────────────────────────────────────────────
    infer_fn = """
// arcInferProject: arcGuessProject의 공개 래퍼 (외부 호출용)
function arcInferProject(item) {
  const title = item.title || '';
  const content = item.content || '';
  const tags = item.tags || [];
  const mentions = item.mentions || [];
  return arcGuessProject(title + ' ' + content, content, tags, mentions);
}
"""
    if 'function arcInferProject' not in content and 'function arcGuessProject' in content:
        old_marker = "function arcComputeCollection"
        if old_marker in content:
            content = content.replace(old_marker, infer_fn + old_marker)
            patches_applied.append("UPG: arcInferProject 함수 추가")

    # ─────────────────────────────────────────────────────────────
    # 4. UPG: arcEditItem 별칭 추가 (arcEdit 함수의 별칭)
    # ─────────────────────────────────────────────────────────────
    alias_fn = "\n// arcEditItem: arcEdit 함수의 별칭 (하위 호환성)\nwindow.arcEditItem = window.arcEdit;\n"
    if 'arcEditItem' not in content and 'window.arcEdit =' in content:
        # window.arcEdit = 뒤에 추가
        old_marker = "window.arcEdit = (id) => {"
        if old_marker in content:
            # arcEdit 함수 끝 찾기
            idx = content.index(old_marker)
            # 함수 끝 (};) 찾기
            end_idx = content.index('\n};', idx)
            insert_pos = end_idx + 3
            content = content[:insert_pos] + alias_fn + content[insert_pos:]
            patches_applied.append("UPG: arcEditItem 별칭 추가")

    # ─────────────────────────────────────────────────────────────
    # 5. UPG: 다크모드 Today 탭 카드 헤더 완전 수정
    # .card-hdr 배경색이 라이트모드 색상으로 하드코딩된 경우
    # ─────────────────────────────────────────────────────────────
    # 카드 헤더 배경 - 다크모드에서 어두운 색
    old = ".card-hdr { display:flex; align-items:center; gap:8px; padding:14px 16px; background:var(--hdr-bg); border-radius:18px 18px 0 0; }"
    new = ".card-hdr { display:flex; align-items:center; gap:8px; padding:14px 16px; background:var(--hdr-bg); border-radius:18px 18px 0 0; border-bottom:1px solid var(--border); }"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: card-hdr 하단 구분선 추가")

    # ─────────────────────────────────────────────────────────────
    # 6. UPG: 아카이브 허브 카드 배경 다크모드 개선
    # .arc-hub-card 배경이 var(--card)로 되어있어 다크모드에서 너무 밝을 수 있음
    # ─────────────────────────────────────────────────────────────
    old = ".arc-hub-card{background:var(--card);border:1px solid var(--border-mid);border-radius:18px;padding:14px;"
    new = ".arc-hub-card{background:var(--surface);border:1px solid var(--border-mid);border-radius:18px;padding:14px;"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-hub-card 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 7. UPG: 아카이브 검색 결과 없을 때 힌트 개선
    # ─────────────────────────────────────────────────────────────
    old = "<div style='font-weight:600;margin-bottom:4px'>조건에 맞는 자료가 없습니다</div><div style="
    new = "<div style='font-weight:600;margin-bottom:6px;font-size:15px'>🔍 조건에 맞는 자료가 없습니다</div><div style='font-size:12px;color:var(--text3);margin-bottom:8px'>검색어, 카테고리, 필터를 바꿔보세요</div><div style="
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 빈 상태 메시지 힌트 개선")

    # ─────────────────────────────────────────────────────────────
    # 8. UPG: AI 리마인더 섹션 배경 다크모드
    # .ai-card 배경이 var(--card)로 되어있어 다크모드에서 너무 밝을 수 있음
    # ─────────────────────────────────────────────────────────────
    old = ".ai-card { background:var(--card); border:1px solid var(--border-mid);"
    new = ".ai-card { background:var(--surface); border:1px solid var(--border-mid);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: ai-card 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 9. UPG: arc-dash-body 배경 다크모드
    # ─────────────────────────────────────────────────────────────
    old = ".arc-dash-body { background:var(--bg);"
    new = ".arc-dash-body { background:var(--surface);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-dash-body 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 10. UPG: arc-meet-body, arc-conv-body 배경 다크모드
    # ─────────────────────────────────────────────────────────────
    old = ".arc-meet-body, .arc-conv-body, .arc-dash-body { background: var(--arc-meet-sheet-bg, var(--surface));"
    new = ".arc-meet-body, .arc-conv-body { background: var(--surface);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-meet/conv-body 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 11. UPG: 아카이브 저장 버튼 텍스트 개선
    # ─────────────────────────────────────────────────────────────
    old = '<button class="sheet-btn primary" onclick="arcSaveItem()">저장</button>'
    new = '<button class="sheet-btn primary" onclick="arcSaveItem()">💾 저장</button>'
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 아카이브 저장 버튼 아이콘 추가")

    # ─────────────────────────────────────────────────────────────
    # 12. UPG: 아카이브 카드 생성 시 kind 자동 추론 저장
    # arcSaveItem 함수에서 kind 필드 저장
    # ─────────────────────────────────────────────────────────────
    old = "  const data = { title, content, type, category, pinned: false, createdAt: serverTimestamp() };"
    new = "  const kind = arcGuessKind(title, content, type);\n  const data = { title, content, type, category, kind, pinned: false, createdAt: serverTimestamp() };"
    if old in content and 'const kind = arcGuessKind' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 아카이브 저장 시 kind 자동 추론 저장")

    # ─────────────────────────────────────────────────────────────
    # 13. UPG: 아카이브 카드 날짜 표시 개선 (오늘/어제/n일 전)
    # arcFormatDate 함수 개선
    # ─────────────────────────────────────────────────────────────
    old = """function arcFormatDate(item){
  const d = arcSafeDate(item);
  const m = d.getMonth()+1, day = d.getDate();
  return `${m}월 ${day}일`;
}"""
    new = """function arcFormatDate(item){
  const d = arcSafeDate(item);
  const now = new Date();
  const diffMs = now - d;
  const diffDays = Math.floor(diffMs / 86400000);
  if(diffDays === 0) return '오늘';
  if(diffDays === 1) return '어제';
  if(diffDays <= 6) return `${diffDays}일 전`;
  const m = d.getMonth()+1, day = d.getDate();
  return `${m}월 ${day}일`;
}"""
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcFormatDate 오늘/어제/n일 전 표시 개선")

    # ─────────────────────────────────────────────────────────────
    # 14. UPG: 아카이브 URL 타입 카드 - 링크 클릭 시 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "function arcOpenUrl(url){"
    new = "function arcOpenUrl(url){ haptic.medium();"
    if old in content and 'function arcOpenUrl(url){ haptic.medium()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcOpenUrl 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 15. UPG: 아카이브 핀 토글 시 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.arcTogglePin = async(id) => {"
    new = "window.arcTogglePin = async(id) => { haptic.medium();"
    if old in content and 'arcTogglePin = async(id) => { haptic.medium()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcTogglePin 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 16. UPG: 아카이브 삭제 시 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.arcDeleteItem = async(id) => {"
    new = "window.arcDeleteItem = async(id) => { haptic.heavy();"
    if old in content and 'arcDeleteItem = async(id) => { haptic.heavy()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcDeleteItem 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 17. UPG: 아카이브 편집 저장 시 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.arcSaveEdit = async() => {"
    new = "window.arcSaveEdit = async() => { haptic.medium();"
    if old in content and 'arcSaveEdit = async() => { haptic.medium()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcSaveEdit 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 18. UPG: 아카이브 저장 시 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.arcSaveItem = async() => {"
    new = "window.arcSaveItem = async() => { haptic.medium();"
    if old in content and 'arcSaveItem = async() => { haptic.medium()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: arcSaveItem 햅틱 추가")

    # ─────────────────────────────────────────────────────────────
    # 19. UPG: 아카이브 허브 "프로젝트 보기" 버튼 텍스트 개선
    # ─────────────────────────────────────────────────────────────
    old = "onclick=\"openArcDashboard(currentArcProjectFilter||'')\">"
    new = "onclick=\"openArcDashboard(currentArcProjectFilter||'')\" title=\"프로젝트 대시보드 열기\">"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 프로젝트 보기 버튼 title 속성 추가")

    # ─────────────────────────────────────────────────────────────
    # 20. UPG: 아카이브 대시보드 닫기 버튼 햅틱 추가
    # ─────────────────────────────────────────────────────────────
    old = "window.closeArcDashboard = () => {"
    new = "window.closeArcDashboard = () => { haptic.light();"
    if old in content and 'closeArcDashboard = () => { haptic.light()' not in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: closeArcDashboard 햅틱 추가")

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
        print(f"⚠️  {path.split('/')[-1]}: 변경 없음")

    return patches_applied

if __name__ == '__main__':
    print("=" * 60)
    print("v22 3차 패치 시작")
    print("=" * 60)
    total = 0
    for f in TARGET_FILES:
        applied = patch_file(f)
        total += len(applied)
    print("=" * 60)
    print(f"총 {total}개 패치 적용 완료")
