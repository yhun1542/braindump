#!/usr/bin/env python3
"""다크모드 전체 수정 패치"""

TARGETS = ['galaxy.html', 'iphone.html', 'index.html']

# ── 패치 목록 ──
# (설명, 찾을 문자열, 교체할 문자열)
PATCHES = [

# ════════════════════════════════════════
# 1. [data-theme="dark"] 변수 확장
#    - 카드 헤더용 별도 변수 추가
# ════════════════════════════════════════
(
  "다크모드 변수 확장 (card-hdr, sheet 색상 추가)",
  '[data-theme="dark"] {\n  --bg: #0e0e0e; --surface: #1a1a1a; --hdr-bg: #f0f0ec; --hdr-text: #111111;\n  --border: #f0f0ec; --border-mid: #2c2c2c; --line: #222222;\n  --text: #f0f0ec; --text2: #888888; --text3: #444444;\n  --done-color: #3a3a3a; --shadow: 0 2px 16px rgba(0,0,0,0.4);\n}',
  '[data-theme="dark"] {\n  --bg: #0e0e0e; --surface: #1a1a1a; --hdr-bg: #f0f0ec; --hdr-text: #111111;\n  --border: #f0f0ec; --border-mid: #2c2c2c; --line: #222222;\n  --text: #f0f0ec; --text2: #888888; --text3: #444444;\n  --done-color: #3a3a3a; --shadow: 0 2px 16px rgba(0,0,0,0.4);\n  /* 다크모드 전용 추가 변수 */\n  --card-hdr-bg: #252525;\n  --card-hdr-text: #f0f0ec;\n  --sheet-bg: #1e1e1e;\n  --sheet-border: #333;\n  --input-bg: #252525;\n  --drum-fade: rgba(14,14,14,0.95);\n  --drum-text: #f0f0ec;\n  --drum-inactive: #555;\n  --alarm-hover: #2a2a2a;\n  --type-note-bg: #2a2010;\n  --type-url-bg: #0d1e2e;\n  --type-image-bg: #2a0d18;\n  --type-video-bg: #1e0d2a;\n  --type-file-bg: #0d2a14;\n  --bd-del-bg: #2a0d0d;\n  --bd-del-border: #4a1a1a;\n  --bd-highlight-bg: #2a2000;\n  --err-bg: #2a0d0d;\n  --err-border: #4a1a1a;\n}'
),

# ════════════════════════════════════════
# 2. 라이트모드 :root에 기본값 추가
# ════════════════════════════════════════
(
  "라이트모드 :root 기본 변수 추가",
  '  --accent: #6c63ff;\n  --grad: linear-gradient(135deg, #6c63ff 0%, #e040fb 100%);\n}',
  '  --accent: #6c63ff;\n  --grad: linear-gradient(135deg, #6c63ff 0%, #e040fb 100%);\n  /* 라이트모드 기본값 */\n  --card-hdr-bg: #111111;\n  --card-hdr-text: #ffffff;\n  --sheet-bg: #ffffff;\n  --sheet-border: #f0f0f0;\n  --input-bg: var(--bg);\n  --drum-fade: rgba(255,255,255,0.95);\n  --drum-text: #1a1a1a;\n  --drum-inactive: #bbb;\n  --alarm-hover: #f5f5f5;\n  --type-note-bg: #fff3e0;\n  --type-url-bg: #e3f2fd;\n  --type-image-bg: #fce4ec;\n  --type-video-bg: #f3e5f5;\n  --type-file-bg: #e8f5e9;\n  --bd-del-bg: #fdf2f2;\n  --bd-del-border: #fcc;\n  --bd-highlight-bg: #fff3cd;\n  --err-bg: #fdf2f2;\n  --err-border: #fcc;\n}'
),

# ════════════════════════════════════════
# 3. card-hdr → CSS 변수 사용
# ════════════════════════════════════════
(
  "card-hdr 배경/텍스트 CSS 변수로 교체",
  '.card-hdr {\n  background: var(--hdr-bg); color: var(--hdr-text);\n  padding: 12px 16px;\n  display: flex; align-items: center; gap: 10px;\n}',
  '.card-hdr {\n  background: var(--card-hdr-bg); color: var(--card-hdr-text);\n  padding: 12px 16px;\n  display: flex; align-items: center; gap: 10px;\n}'
),

(
  "card-hdr-edit 색상 CSS 변수로 교체",
  '.card-hdr-edit {\n  background: none; border: none; color: var(--hdr-text);\n  font-size: 14px; cursor: pointer; opacity: 0.6; padding: 4px;\n}',
  '.card-hdr-edit {\n  background: none; border: none; color: var(--card-hdr-text);\n  font-size: 14px; cursor: pointer; opacity: 0.6; padding: 4px;\n}'
),

# ════════════════════════════════════════
# 4. sheet-del → CSS 변수 사용
# ════════════════════════════════════════
(
  "sheet-del 배경 CSS 변수로 교체",
  '.sheet-del {\n  flex: 1; padding: 14px; border-radius: 12px;\n  background: #fdf2f2; border: 1.5px solid #fcc;\n  font-size: 15px; font-weight: 700; color: #e74c3c; cursor: pointer;\n  font-family: var(--font);\n}',
  '.sheet-del {\n  flex: 1; padding: 14px; border-radius: 12px;\n  background: var(--err-bg); border: 1.5px solid var(--err-border);\n  font-size: 15px; font-weight: 700; color: #e74c3c; cursor: pointer;\n  font-family: var(--font);\n}'
),

# ════════════════════════════════════════
# 5. BrainDump bd-del-btn, bd-highlight → CSS 변수
# ════════════════════════════════════════
(
  "bd-del-btn 배경 CSS 변수로 교체",
  '.bd-del-btn   { background: #fdf2f2; color: #e74c3c; }',
  '.bd-del-btn   { background: var(--bd-del-bg); color: #e74c3c; }'
),
(
  "bd-highlight 배경 CSS 변수로 교체",
  '.bd-highlight { background: #fff3cd; border-radius: 2px; }',
  '.bd-highlight { background: var(--bd-highlight-bg); border-radius: 2px; }'
),

# ════════════════════════════════════════
# 6. Archive 타입 아이콘 배경 → CSS 변수
# ════════════════════════════════════════
(
  "arc-type 아이콘 배경 CSS 변수로 교체",
  '.arc-type-note   { background: #fff3e0; }\n.arc-type-url    { background: #e3f2fd; }\n.arc-type-image  { background: #fce4ec; }\n.arc-type-video  { background: #f3e5f5; }\n.arc-type-file   { background: #e8f5e9; }',
  '.arc-type-note   { background: var(--type-note-bg); }\n.arc-type-url    { background: var(--type-url-bg); }\n.arc-type-image  { background: var(--type-image-bg); }\n.arc-type-video  { background: var(--type-video-bg); }\n.arc-type-file   { background: var(--type-file-bg); }'
),

# ════════════════════════════════════════
# 7. 알림 시트 (#fff, #1a1a1a 하드코딩 제거)
# ════════════════════════════════════════
(
  "alarm-sheet-box 배경 CSS 변수로 교체",
  '.alarm-sheet-box {\n  width: 100%; background: #fff; border-radius: 20px 20px 0 0;\n  padding: 0 0 env(safe-area-inset-bottom, 16px);\n  transform: translateY(100%);\n  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);\n}',
  '.alarm-sheet-box {\n  width: 100%; background: var(--sheet-bg); border-radius: 20px 20px 0 0;\n  padding: 0 0 env(safe-area-inset-bottom, 16px);\n  transform: translateY(100%);\n  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);\n}'
),
(
  "alarm-sheet-handle 색상 CSS 변수로 교체",
  '.alarm-sheet-handle {\n  width: 40px; height: 4px; background: #ddd; border-radius: 2px;\n  margin: 12px auto 4px;\n}',
  '.alarm-sheet-handle {\n  width: 40px; height: 4px; background: var(--border-mid); border-radius: 2px;\n  margin: 12px auto 4px;\n}'
),
(
  "alarm-sheet-title 색상 CSS 변수로 교체",
  '.alarm-sheet-title {\n  font-size: 18px; font-weight: 700; color: #1a1a1a;\n  padding: 12px 20px 8px;\n}',
  '.alarm-sheet-title {\n  font-size: 18px; font-weight: 700; color: var(--text);\n  padding: 12px 20px 8px;\n}'
),
(
  "alarm-option 색상/배경 CSS 변수로 교체",
  '.alarm-option {\n  display: block; width: 100%; text-align: left;\n  padding: 16px 20px; font-size: 16px; color: #1a1a1a;\n  background: none; border: none; cursor: pointer;\n  border-bottom: 1px solid #f0f0f0;\n  transition: background 0.15s;\n}\n.alarm-option:last-child { border-bottom: none; }\n.alarm-option:active { background: #f5f5f5; }',
  '.alarm-option {\n  display: block; width: 100%; text-align: left;\n  padding: 16px 20px; font-size: 16px; color: var(--text);\n  background: none; border: none; cursor: pointer;\n  border-bottom: 1px solid var(--line);\n  transition: background 0.15s;\n}\n.alarm-option:last-child { border-bottom: none; }\n.alarm-option:active { background: var(--alarm-hover); }'
),

# ════════════════════════════════════════
# 8. 드럼 피커 (#fff, #1a1a1a 하드코딩 제거)
# ════════════════════════════════════════
(
  "drum-box 배경 CSS 변수로 교체",
  '.drum-box {\n  width: 100%; background: #fff; border-radius: 20px 20px 0 0;\n  padding-bottom: env(safe-area-inset-bottom, 16px);\n  transform: translateY(100%);\n  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);\n}',
  '.drum-box {\n  width: 100%; background: var(--sheet-bg); border-radius: 20px 20px 0 0;\n  padding-bottom: env(safe-area-inset-bottom, 16px);\n  transform: translateY(100%);\n  transition: transform 0.3s cubic-bezier(0.32,0.72,0,1);\n}'
),
(
  "drum-title 색상 CSS 변수로 교체",
  '.drum-title { font-size: 18px; font-weight: 700; color: #1a1a1a; }',
  '.drum-title { font-size: 18px; font-weight: 700; color: var(--text); }'
),
(
  "drum-col fade 그라디언트 CSS 변수로 교체",
  '.drum-col::before {\n  top: 0;\n  background: linear-gradient(to bottom, rgba(255,255,255,0.95), rgba(255,255,255,0));\n}\n.drum-col::after {\n  bottom: 0;\n  background: linear-gradient(to top, rgba(255,255,255,0.95), rgba(255,255,255,0));\n}',
  '.drum-col::before {\n  top: 0;\n  background: linear-gradient(to bottom, var(--drum-fade), transparent);\n}\n.drum-col::after {\n  bottom: 0;\n  background: linear-gradient(to top, var(--drum-fade), transparent);\n}'
),
(
  "drum-item 색상 CSS 변수로 교체",
  '.drum-item {\n  height: 60px; display: flex; align-items: center; justify-content: center;\n  font-size: 18px; font-weight: 500; color: #bbb;\n  transition: color 0.15s, font-size 0.15s;\n  user-select: none;\n}\n.drum-item.active { color: #1a1a1a; font-size: 20px; font-weight: 700; }',
  '.drum-item {\n  height: 60px; display: flex; align-items: center; justify-content: center;\n  font-size: 18px; font-weight: 500; color: var(--drum-inactive);\n  transition: color 0.15s, font-size 0.15s;\n  user-select: none;\n}\n.drum-item.active { color: var(--drum-text); font-size: 20px; font-weight: 700; }'
),
(
  "drum-sep 색상 CSS 변수로 교체",
  '.drum-sep {\n  display: flex; align-items: center; justify-content: center;\n  font-size: 20px; font-weight: 700; color: #1a1a1a;\n  padding-top: 60px; /* align with center */\n  min-width: 16px;\n}',
  '.drum-sep {\n  display: flex; align-items: center; justify-content: center;\n  font-size: 20px; font-weight: 700; color: var(--text);\n  padding-top: 60px; /* align with center */\n  min-width: 16px;\n}'
),
(
  "drum-btns 구분선 CSS 변수로 교체",
  '.drum-btns {\n  display: flex; justify-content: space-between;\n  padding: 12px 20px 8px;\n  border-top: 1px solid #f0f0f0;\n}',
  '.drum-btns {\n  display: flex; justify-content: space-between;\n  padding: 12px 20px 8px;\n  border-top: 1px solid var(--line);\n}'
),
(
  "drum-cancel-btn 색상 CSS 변수로 교체",
  '.drum-cancel-btn {\n  font-size: 16px; color: #666; background: none; border: none;\n  cursor: pointer; padding: 8px 16px;\n}',
  '.drum-cancel-btn {\n  font-size: 16px; color: var(--text2); background: none; border: none;\n  cursor: pointer; padding: 8px 16px;\n}'
),

# ════════════════════════════════════════
# 9. 이벤트 에러 표시 (빨간 배경) CSS 변수
# ════════════════════════════════════════
(
  "이벤트 에러 배경 CSS 변수로 교체 (1)",
  '  background: #fdf2f2; border: 1.5px solid #fcc; border-radius: 14px;',
  '  background: var(--err-bg); border: 1.5px solid var(--err-border); border-radius: 14px;'
),
(
  "이벤트 에러 배경 CSS 변수로 교체 (2)",
  '  background: #fdf2f2; border: 1.5px solid #fcc;\n',
  '  background: var(--err-bg); border: 1.5px solid var(--err-border);\n'
),

# ════════════════════════════════════════
# 10. 드럼 피커 선택 원형 배경 (흰색)
# ════════════════════════════════════════
(
  "드럼 피커 선택 원형 배경 CSS 변수로 교체",
  '  width: 20px; height: 20px; border-radius: 50%; background: #fff;',
  '  width: 20px; height: 20px; border-radius: 50%; background: var(--sheet-bg);'
),

]

import sys

def apply_patches(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    applied = []
    errors = []

    for desc, old, new in PATCHES:
        if old in content:
            content = content.replace(old, new, 1)
            applied.append(desc)
        else:
            # 이미 적용됐거나 패턴 없음
            if new in content:
                applied.append(f"[이미적용] {desc}")
            else:
                errors.append(f"[패턴없음] {desc}")

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

    return applied, errors

for fname in TARGETS:
    path = f'/home/ubuntu/braindump/{fname}'
    print(f'\n=== {fname} ===')
    applied, errors = apply_patches(path)
    for a in applied:
        print(f'  [+] {a}')
    for e in errors:
        print(f'  [!] {e}')
    print(f'  → 적용: {len(applied)}, 오류: {len(errors)}')

print('\n완료!')
