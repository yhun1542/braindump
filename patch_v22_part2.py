#!/usr/bin/env python3
"""
v22 2차 패치 - 실제 CSS 패턴 기반으로 수정
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
    # 1. 다크모드: arc-ctx-menu 배경 변수 적용 (실제 패턴)
    # ─────────────────────────────────────────────────────────────
    old = ".arc-ctx-menu {\n  position:fixed; background:#fff; border:1px solid #e5e7eb;"
    new = ".arc-ctx-menu {\n  position:fixed; background:var(--surface); border:1px solid var(--border);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-ctx-menu 배경 var(--surface) 적용")

    # arc-ctx-menu 한 줄 패턴
    old = ".arc-ctx-menu { position:fixed; background:#fff; border:1px solid #e5e7eb;"
    new = ".arc-ctx-menu { position:fixed; background:var(--surface); border:1px solid var(--border);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-ctx-menu 배경 var(--surface) 적용 (한줄)")

    # ─────────────────────────────────────────────────────────────
    # 2. 다크모드: arc-ctx-item hover 배경 변수 적용
    # ─────────────────────────────────────────────────────────────
    old = ".arc-ctx-item:hover { background:#f3f4f6; }"
    new = ".arc-ctx-item:hover { background:var(--line); }"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-ctx-item hover var(--line) 적용")

    # ─────────────────────────────────────────────────────────────
    # 3. 다크모드: arc-dash-stat 배경 변수 적용 (실제 패턴)
    # L1305: .arc-dash-stat{background:var(--bg);border-radius:14px;...
    # ─────────────────────────────────────────────────────────────
    old = ".arc-dash-stat{background:var(--bg);border-radius:14px;padding:10px 8px;text-align:center;border:1px solid var(--border-"
    new = ".arc-dash-stat{background:var(--surface);border-radius:14px;padding:10px 8px;text-align:center;border:1px solid var(--border-"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-dash-stat 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 4. 다크모드: arc-hub-action 배경 (하드코딩 #111827 → 변수)
    # L1192: .arc-hub-action{...background:#111827;color:#fff;...
    # ─────────────────────────────────────────────────────────────
    old = ".arc-hub-action{border:none;border-radius:12px;padding:10px 12px;background:#111827;color:#fff;"
    new = ".arc-hub-action{border:none;border-radius:12px;padding:10px 12px;background:var(--text);color:var(--bg);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-hub-action 배경 var(--text) 적용")

    # ─────────────────────────────────────────────────────────────
    # 5. 다크모드: arc-link-card 배경 (v20 패턴 - 실제 패턴)
    # L1208: .arc-link-card{display:flex;gap:12px;...background:var(--bg);...
    # ─────────────────────────────────────────────────────────────
    old = ".arc-link-card{display:flex;gap:12px;align-items:center;background:var(--bg);border-radius:14px;padding:12px;border:1px "
    new = ".arc-link-card{display:flex;gap:12px;align-items:center;background:var(--surface);border-radius:14px;padding:12px;border:1px "
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-link-card(v20) 배경 var(--surface) 적용")

    # v2 패턴
    old = ".arc-link-card { display:flex; align-items:stretch; background:var(--bg);"
    new = ".arc-link-card { display:flex; align-items:stretch; background:var(--surface);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-link-card(v2) 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 6. 다크모드 변수 블록에 v22 신규 변수 추가
    # ─────────────────────────────────────────────────────────────
    dark_block_marker = "  --arc-type-note-bg: #1e2a1e;"
    dark_new_vars = """  --arc-dash-stat-bg: #252525;
  --arc-hub-action-bg: #e0e0e0;
  --arc-ctx-menu-bg: #252525;
  --arc-kind-meeting-bg: rgba(245,158,11,0.18);
  --arc-kind-material-bg: rgba(59,130,246,0.18);
  --arc-kind-idea-bg: rgba(16,185,129,0.18);
"""
    if dark_block_marker in content and '--arc-dash-stat-bg' not in content:
        content = content.replace(dark_block_marker, dark_new_vars + dark_block_marker)
        patches_applied.append("DARK: v22 신규 다크모드 변수 블록 추가")

    # ─────────────────────────────────────────────────────────────
    # 7. arc-kind-badge CSS 추가 (pin-badge 뒤에)
    # ─────────────────────────────────────────────────────────────
    kind_badge_css = """\n.arc-kind-badge { display:inline-flex; align-items:center; gap:3px; font-size:10px; font-weight:700; padding:2px 8px; border-radius:10px; margin-left:4px; vertical-align:middle; }
.arc-kind-meeting { background:var(--arc-kind-meeting-bg,rgba(245,158,11,0.12)); color:#f59e0b; }
.arc-kind-material { background:var(--arc-kind-material-bg,rgba(59,130,246,0.12)); color:#3b82f6; }
.arc-kind-idea { background:var(--arc-kind-idea-bg,rgba(16,185,129,0.12)); color:#10b981; }"""

    if '.arc-kind-badge' not in content:
        # arc-pin-badge 뒤에 삽입
        old_css = ".arc-pin-badge {"
        if old_css in content:
            # 해당 CSS 블록 끝 찾기 (닫는 })
            idx = content.index(old_css)
            close_idx = content.index('}', idx)
            insert_pos = close_idx + 1
            content = content[:insert_pos] + kind_badge_css + content[insert_pos:]
            patches_applied.append("UPG: arc-kind-badge CSS 추가")

    # ─────────────────────────────────────────────────────────────
    # 8. 아카이브 카드에 kind 배지 표시 (실제 패턴 찾기)
    # ─────────────────────────────────────────────────────────────
    old = "${item.pinned ? '<span class=\"arc-pin-badge\">⭐</span>' : ''}"
    new = """${item.pinned ? '<span class="arc-pin-badge">⭐</span>' : ''}${item.kind && item.kind!=='general' ? `<span class="arc-kind-badge arc-kind-${item.kind}">${item.kind==='meeting'?'📋 회의':item.kind==='material'?'📁 자료':item.kind==='idea'?'💡 아이디어':''}</span>` : ''}"""
    if old in content and 'arc-kind-badge' not in content.split(old)[0][-200:]:
        content = content.replace(old, new, 1)
        patches_applied.append("UPG: 아카이브 카드 kind 배지 표시 추가")

    # ─────────────────────────────────────────────────────────────
    # 9. 다크모드: arc-item 카드 배경 개선
    # ─────────────────────────────────────────────────────────────
    old = ".arc-item { background:var(--card); border:1px solid var(--border-mid);"
    new = ".arc-item { background:var(--surface); border:1px solid var(--border-mid);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-item 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 10. 다크모드: arc-meet-body 내부 요소 배경
    # ─────────────────────────────────────────────────────────────
    old = ".arc-meet-item { background:var(--bg); border:1px solid var(--border);"
    new = ".arc-meet-item { background:var(--surface); border:1px solid var(--border);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-meet-item 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 11. 다크모드: arc-conv-item 배경
    # ─────────────────────────────────────────────────────────────
    old = ".arc-conv-item { background:var(--bg); border:1px solid var(--border);"
    new = ".arc-conv-item { background:var(--surface); border:1px solid var(--border);"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-conv-item 배경 var(--surface) 적용")

    # ─────────────────────────────────────────────────────────────
    # 12. 다크모드: arc-ctx-item 텍스트 색상
    # ─────────────────────────────────────────────────────────────
    old = ".arc-ctx-item { display:flex; align-items:center; gap:8px; padding:12px 16px; font-size:14px; cursor:pointer; color:#374151; }"
    new = ".arc-ctx-item { display:flex; align-items:center; gap:8px; padding:12px 16px; font-size:14px; cursor:pointer; color:var(--text); }"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("DARK: arc-ctx-item 텍스트 var(--text) 적용")

    # ─────────────────────────────────────────────────────────────
    # 13. 업그레이드: 아카이브 저장 완료 메시지 개선
    # ─────────────────────────────────────────────────────────────
    old = "showSaved('✅ 저장됨');"
    new = "showSaved('✅ 아카이브에 저장됨');"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 아카이브 저장 완료 메시지 개선")

    # ─────────────────────────────────────────────────────────────
    # 14. 업그레이드: 아카이브 편집 완료 메시지 개선
    # ─────────────────────────────────────────────────────────────
    old = "showSaved('✅ 수정됨');"
    new = "showSaved('✅ 수정 완료');"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 아카이브 편집 완료 메시지 개선")

    # ─────────────────────────────────────────────────────────────
    # 15. 업그레이드: 아카이브 삭제 확인 메시지 개선
    # ─────────────────────────────────────────────────────────────
    old = "if(!confirm('삭제하시겠습니까?')) return;"
    new = "if(!confirm('이 항목을 삭제하시겠습니까? 되돌릴 수 없습니다.')) return;"
    if old in content:
        content = content.replace(old, new)
        patches_applied.append("UPG: 아카이브 삭제 확인 메시지 개선")

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
    print("v22 2차 패치 시작")
    print("=" * 60)
    total = 0
    for f in TARGET_FILES:
        applied = patch_file(f)
        total += len(applied)
    print("=" * 60)
    print(f"총 {total}개 패치 적용 완료")
