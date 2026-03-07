"""
전체 시스템 아이콘/로고 교체 종합 패치
- 구 JF 앱 아이콘(파란 JF 텍스트) → JF OS 로고
- 로그인/스플래시/헤더 로고 최적화
- manifest.webmanifest 아이콘 교체
- sw.js 캐시 버전 업데이트
- HTML 3개 파일 파비콘/og/twitter 메타 추가
"""
import re, os

BASE = '/home/ubuntu/braindump'

# ── HTML 3개 파일 패치 ────────────────────────────────────────────────────────
html_files = ['galaxy.html', 'iphone.html', 'index.html']

for fname in html_files:
    path = f'{BASE}/{fname}'
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # 1. <head> 안에 파비콘 + OG 메타 추가 (없으면 추가)
    head_meta = '''  <!-- ═══ Icons & OG ═══ -->
  <link rel="icon" type="image/png" sizes="48x48" href="/icons/favicon-48.png">
  <link rel="icon" type="image/png" sizes="32x32" href="/icons/favicon-32.png">
  <link rel="icon" type="image/png" sizes="16x16" href="/icons/favicon-16.png">
  <link rel="shortcut icon" href="/favicon.ico">
  <link rel="apple-touch-icon" sizes="180x180" href="/icons/apple-touch-icon.png">
  <meta property="og:image" content="https://jasoneye.com/images/og-image.png">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:image" content="https://jasoneye.com/images/og-image.png">'''
    
    # 기존 파비콘/OG 관련 태그 제거 후 재삽입
    # apple-touch-icon 기존 태그 제거
    content = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>\n?', '\n', content)
    # rel="icon" 기존 태그 제거
    content = re.sub(r'\s*<link rel="icon"[^>]*>\n?', '\n', content)
    # rel="shortcut icon" 기존 태그 제거
    content = re.sub(r'\s*<link rel="shortcut icon"[^>]*>\n?', '\n', content)
    # og:image 기존 태그 제거
    content = re.sub(r'\s*<meta property="og:image[^>]*>\n?', '\n', content)
    # twitter 기존 태그 제거
    content = re.sub(r'\s*<meta name="twitter:[^>]*>\n?', '\n', content)
    # Icons & OG 주석 블록 제거 (중복 방지)
    content = re.sub(r'\s*<!-- ═══ Icons & OG ═══ -->.*?-->\n?', '\n', content, flags=re.DOTALL)
    
    # <link rel="manifest"> 바로 앞에 삽입
    if '<link rel="manifest"' in content:
        content = content.replace(
            '<link rel="manifest"',
            head_meta + '\n  <link rel="manifest"'
        )
    else:
        # </head> 바로 앞에 삽입
        content = content.replace('</head>', head_meta + '\n</head>')
    
    # 2. 스플래시 로고 - HD 이미지로 교체 + 크기 최적화
    # bootSplash 내 img 태그 교체
    content = re.sub(
        r'(<div id="bootSplash"[^>]*>.*?<img\s+)src="[^"]*"([^>]*?)style="[^"]*"',
        r'\1src="/images/jf_os_header_dark_hd.png"\2style="width:min(280px,60vw); height:auto; display:block; margin:0 auto; image-rendering:auto;"',
        content, flags=re.DOTALL
    )
    # onerror 폴백 교체
    content = re.sub(
        r"(bootSplash.*?onerror=\")this\.src='[^']*'(\")",
        r"\1this.src='/images/jf_os_header_dark_master.png'\2",
        content, flags=re.DOTALL
    )
    
    # 3. 로그인 화면 로고 - HD 이미지 + srcset 최적화
    # loginLogoImg img 태그 교체
    content = re.sub(
        r'(<img\s+src="/images/jf_os_header_light_hd\.png"[^>]*?)srcset="[^"]*"',
        r'\1srcset="/images/jf_os_header_light_hd.webp 2x, /images/jf_os_header_light_hd.png 1x"',
        content
    )
    # 로그인 로고 크기 최적화 (style 속성)
    content = re.sub(
        r'(<img[^>]*id="loginLogoImg"[^>]*?)style="[^"]*"',
        r'\1style="width:min(220px,55vw); height:auto; display:block; margin:0 auto 16px; image-rendering:auto;"',
        content
    )
    
    # 4. 앱 헤더 로고 (hdrLogoImg) - HD 이미지 + srcset 최적화
    content = re.sub(
        r'(<img[^>]*id="hdrLogoImg"[^>]*?)srcset="[^"]*"',
        r'\1srcset="/images/jf_os_header_light_hd.webp 2x, /images/jf_os_header_light_hd.png 1x"',
        content
    )
    content = re.sub(
        r'(<img[^>]*data-logo="header"[^>]*?)height="\d+"',
        r'\1height="40"',
        content
    )
    
    # 5. JS updateLogoTheme 함수 - HD 이미지 경로로 교체
    content = re.sub(
        r"hdrLogo\.src = `/images/jf_os_header_\$\{variant\}_1x\.png`;",
        r"hdrLogo.src = `/images/jf_os_header_${variant}_hd.png`;",
        content
    )
    content = re.sub(
        r"hdrLogo\.srcset = `/images/jf_os_header_\$\{variant\}_1x\.png 1x, /images/jf_os_header_\$\{variant\}_2x\.png 2x, /images/jf_os_header_\$\{variant\}_3x\.png 3x`;",
        r"hdrLogo.srcset = `/images/jf_os_header_${variant}_hd.webp 2x, /images/jf_os_header_${variant}_hd.png 1x`;",
        content
    )
    
    # 6. 알림 아이콘 (icon-192.png) - 유지 (PWA 알림은 icon-192 사용)
    # 이미 JF OS 로고로 교체된 icon-192.png를 사용하므로 경로는 그대로 유지
    
    # 7. login-logo CSS 최적화 (width:auto 이미 적용됨, max-width 추가)
    content = re.sub(
        r'(\.login-logo\s*img\s*\{[^}]*?)(width\s*:\s*auto;)',
        r'\1width: min(220px, 55vw);',
        content
    )
    
    # 중복 공백 라인 정리
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    if content != original:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"✅ {fname} 패치 완료")
    else:
        print(f"⚠️  {fname} 변경 없음")

# ── manifest.webmanifest 패치 ─────────────────────────────────────────────────
manifest_path = f'{BASE}/manifest.webmanifest'
with open(manifest_path, 'r', encoding='utf-8') as f:
    manifest = f.read()

import json
m = json.loads(manifest)

# 아이콘 교체
m['icons'] = [
    {
        "src": "/icons/icon-192.png",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "any"
    },
    {
        "src": "/icons/icon-192.png",
        "sizes": "192x192",
        "type": "image/png",
        "purpose": "maskable"
    },
    {
        "src": "/icons/icon-512.png",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "any"
    },
    {
        "src": "/icons/icon-512.png",
        "sizes": "512x512",
        "type": "image/png",
        "purpose": "maskable"
    },
    {
        "src": "/icons/apple-touch-icon.png",
        "sizes": "180x180",
        "type": "image/png",
        "purpose": "any"
    }
]

# shortcuts 아이콘도 교체
if 'shortcuts' in m:
    for sc in m['shortcuts']:
        if 'icons' in sc:
            sc['icons'] = [{"src": "/icons/icon-192.png", "sizes": "192x192"}]

# screenshots 추가 (PWA 설치 화면)
m['screenshots'] = [
    {
        "src": "/images/og-image.png",
        "sizes": "1200x630",
        "type": "image/png",
        "label": "JF OS - Synapse Brain"
    }
]

with open(manifest_path, 'w', encoding='utf-8') as f:
    json.dump(m, f, ensure_ascii=False, indent=2)
print("✅ manifest.webmanifest 패치 완료")

# ── sw.js 캐시 버전 업데이트 ─────────────────────────────────────────────────
sw_path = f'{BASE}/sw.js'
with open(sw_path, 'r', encoding='utf-8') as f:
    sw = f.read()

# 캐시 버전 업데이트 (pwa-v3 → pwa-v4)
sw_new = sw.replace("'pwa-v3'", "'pwa-v4'").replace('"pwa-v3"', '"pwa-v4"')

# SHELL_ASSETS에 새 이미지 파일 추가
if '/images/og-image.png' not in sw_new:
    sw_new = sw_new.replace(
        "'/icons/icon-512.png'",
        "'/icons/icon-512.png',\n  '/icons/apple-touch-icon.png',\n  '/favicon.ico',\n  '/images/og-image.png'"
    )

if sw_new != sw:
    with open(sw_path, 'w', encoding='utf-8') as f:
        f.write(sw_new)
    print("✅ sw.js 캐시 버전 업데이트 완료 (pwa-v3 → pwa-v4)")
else:
    print("⚠️  sw.js 변경 없음")

print("\n🎉 전체 패치 완료!")
