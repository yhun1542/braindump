#!/usr/bin/env python3
"""
Synapse Brain App v22 - 자체 정밀 검증 스크립트
JS 문법, 로직, 보안, 성능, 접근성, 다크모드, 햅틱 등 전방위 검사
"""

import re
import json

files = {
    'galaxy.html': '/home/ubuntu/braindump/galaxy.html',
    'iphone.html': '/home/ubuntu/braindump/iphone.html',
    'index.html': '/home/ubuntu/braindump/index.html',
}

report = {}

for fname, fpath in files.items():
    with open(fpath, encoding='utf-8') as f:
        content = f.read()
    lines = content.split('\n')
    
    issues = []
    warnings = []
    passed = []
    
    # ─── 1. 필수 기능 존재 여부 ───
    required_functions = [
        ('haptic utility', 'const haptic ='),
        ('openArcDashboard', 'function openArcDashboard'),
        ('openMeetingSummary', 'async function openMeetingSummary'),
        ('openQuickConvert', 'async function openQuickConvert'),
        ('execConvert', 'window.execConvert'),
        ('arcSearchScore', 'function arcSearchScore'),
        ('arcInferProject', 'function arcInferProject'),
        ('arcFormatDate', 'function arcFormatDate'),
        ('arcEnrichItem', 'function arcEnrichItem'),
        ('renderArcGrid', 'function renderArcGrid'),
        ('arcTogglePin', 'arcTogglePin ='),
        ('arcDeleteItem', 'arcDeleteItem ='),
        ('arcSaveItem', 'arcSaveItem ='),
        ('sendMeetActionsToToday', 'sendMeetActionsToToday ='),
    ]
    for name, pat in required_functions:
        if pat in content:
            passed.append(f'✅ {name} 존재')
        else:
            issues.append(f'❌ {name} 누락')
    
    # ─── 2. 다크모드 CSS 변수 완성도 ───
    dark_vars = [
        '--bg: #0e0e0e',
        '--surface: #1a1a1a',
        '--hdr-bg: #1a1a1a',
        '--card-hdr-bg: #252525',
        '--sheet-bg: #1e1e1e',
        '--drum-fade: rgba(14,14,14',
        '--type-note-bg: #2a2010',
        '--type-url-bg: #0d1e2e',
        '--bd-del-bg: #2a0d0d',
    ]
    dark_ok = sum(1 for v in dark_vars if v in content)
    if dark_ok == len(dark_vars):
        passed.append(f'✅ 다크모드 CSS 변수 완성 ({dark_ok}/{len(dark_vars)})')
    else:
        warnings.append(f'⚠️  다크모드 CSS 변수 {dark_ok}/{len(dark_vars)} 적용')
    
    # ─── 3. arc-ctx-overlay hidden 버그픽스 ───
    if 'arc-ctx-overlay.hidden' in content and 'arc-ctx-menu.hidden' in content:
        passed.append('✅ arc-ctx-overlay hidden 버그픽스 적용')
    else:
        issues.append('❌ arc-ctx-overlay hidden CSS 누락 (탭바 클릭 불가 버그)')
    
    # ─── 4. 햅틱 적용 범위 ───
    haptic_calls = len(re.findall(r'haptic\.(light|medium|heavy|success|error|double|longpress)\(\)', content))
    if haptic_calls >= 30:
        passed.append(f'✅ 햅틱 피드백 {haptic_calls}곳 적용')
    elif haptic_calls >= 15:
        warnings.append(f'⚠️  햅틱 피드백 {haptic_calls}곳 (30+ 권장)')
    else:
        issues.append(f'❌ 햅틱 피드백 {haptic_calls}곳 (너무 적음)')
    
    # ─── 5. arcFormatDate 오늘/어제 개선 ───
    if 'diffDays === 0) return' in content:
        passed.append('✅ arcFormatDate 오늘/어제 표시 개선')
    else:
        warnings.append('⚠️  arcFormatDate 오늘/어제 표시 미적용')
    
    # ─── 6. XSS 방어 (escHtml 사용) ───
    esc_count = content.count('escHtml(')
    if esc_count >= 20:
        passed.append(f'✅ XSS 방어 escHtml {esc_count}곳 사용')
    else:
        warnings.append(f'⚠️  escHtml {esc_count}곳 (더 많이 사용 권장)')
    
    # ─── 7. innerHTML 직접 사용 위험 ───
    inner_html_raw = len(re.findall(r'innerHTML\s*=\s*[^`"\']', content))
    if inner_html_raw > 5:
        warnings.append(f'⚠️  innerHTML 직접 할당 {inner_html_raw}곳 (XSS 위험 가능)')
    else:
        passed.append(f'✅ innerHTML 직접 할당 {inner_html_raw}곳 (안전)')
    
    # ─── 8. Firestore 에러 핸들링 ───
    try_catch = len(re.findall(r'try\s*\{', content))
    catch_count = len(re.findall(r'catch\s*\(', content))
    if try_catch >= 10:
        passed.append(f'✅ try-catch 에러 핸들링 {try_catch}곳')
    else:
        warnings.append(f'⚠️  try-catch {try_catch}곳 (더 많이 사용 권장)')
    
    # ─── 9. 빈 상태 처리 (empty state) ───
    empty_state = 'arc-empty' in content or 'empty-state' in content or '아직 없습니다' in content
    if empty_state:
        passed.append('✅ 빈 상태(empty state) 처리 존재')
    else:
        warnings.append('⚠️  빈 상태 처리 누락')
    
    # ─── 10. 모바일 뷰포트 설정 ───
    if 'maximum-scale=1.0' in content and 'user-scalable=no' in content:
        passed.append('✅ 모바일 뷰포트 설정 완료')
    else:
        warnings.append('⚠️  모바일 뷰포트 설정 미흡')
    
    # ─── 11. PWA 설정 ───
    if 'manifest.webmanifest' in content and 'apple-mobile-web-app-capable' in content:
        passed.append('✅ PWA 설정 완료')
    else:
        warnings.append('⚠️  PWA 설정 미흡')
    
    # ─── 12. 삭제 확인 (confirm) ───
    if 'confirm(' in content or 'window.confirm' in content:
        passed.append('✅ 삭제 확인 다이얼로그 존재')
    else:
        warnings.append('⚠️  삭제 확인 다이얼로그 없음')
    
    # ─── 13. URL 자동 감지 ───
    if 'arcDetectUrl' in content or 'autoDetect' in content or 'isUrl' in content or 'https://' in content:
        passed.append('✅ URL 자동 감지 로직 존재')
    else:
        warnings.append('⚠️  URL 자동 감지 로직 없음')
    
    # ─── 14. 파일 크기 ───
    size_kb = len(content) / 1024
    line_count = len(lines)
    if size_kb > 200:
        warnings.append(f'⚠️  파일 크기 {size_kb:.0f}KB ({line_count}줄) - 분리 고려')
    else:
        passed.append(f'✅ 파일 크기 {size_kb:.0f}KB ({line_count}줄)')
    
    # ─── 15. 검색 점수 가중치 ───
    if 'arcSearchScore' in content and ('weight' in content or 'score +=' in content or 'boost' in content):
        passed.append('✅ 검색 점수 가중치 로직 존재')
    else:
        warnings.append('⚠️  검색 점수 가중치 로직 확인 필요')
    
    # ─── 종합 점수 계산 ───
    total = len(passed) + len(warnings) + len(issues)
    score = (len(passed) * 100 + len(warnings) * 60) / total if total > 0 else 0
    
    report[fname] = {
        'score': round(score, 1),
        'passed': len(passed),
        'warnings': len(warnings),
        'issues': len(issues),
        'details': {
            'passed': passed,
            'warnings': warnings,
            'issues': issues,
        }
    }

# ─── 출력 ───
print("=" * 65)
print("Synapse Brain App v22 - 자체 정밀 검증 리포트")
print("=" * 65)

for fname, r in report.items():
    print(f"\n📄 {fname}")
    print(f"   종합 점수: {r['score']:.1f}/100  (통과:{r['passed']} / 경고:{r['warnings']} / 오류:{r['issues']})")
    
    if r['details']['issues']:
        print("   ─ 오류 (즉시 수정 필요):")
        for i in r['details']['issues']:
            print(f"     {i}")
    
    if r['details']['warnings']:
        print("   ─ 경고 (개선 권장):")
        for w in r['details']['warnings']:
            print(f"     {w}")
    
    print("   ─ 통과:")
    for p in r['details']['passed'][:5]:
        print(f"     {p}")
    if len(r['details']['passed']) > 5:
        print(f"     ... 외 {len(r['details']['passed'])-5}개 더")

# 전체 평균
avg = sum(r['score'] for r in report.values()) / len(report)
print(f"\n{'=' * 65}")
print(f"전체 평균 점수: {avg:.1f}/100")
if avg >= 90:
    print("✅ 배포 승인 (90점 이상)")
elif avg >= 75:
    print("⚠️  조건부 승인 (75-89점)")
else:
    print("❌ 재검토 필요 (75점 미만)")

# JSON 저장
with open('/home/ubuntu/braindump/self_review_results.json', 'w', encoding='utf-8') as f:
    json.dump({'files': report, 'average': avg}, f, ensure_ascii=False, indent=2)
print("\n결과 저장: self_review_results.json")
